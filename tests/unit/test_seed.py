from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from aegis.domain.base import canonical_json, content_hash
from aegis.errors import UnsafeDestinationError
from aegis.persistence.connection import connect
from aegis.persistence.destination import assert_demo_destination
from aegis.persistence.schema import CANONICAL_TABLES, apply_schema
from aegis.persistence.seed import run_seed
from tests.conftest import FIXTURES_DIR, PRINCIPALS_FILE, seed_into


def table_digest(db_path: Path) -> dict[str, str]:
    conn = connect(db_path, read_only=True)
    try:
        return {
            table: content_hash(
                {
                    "rows": sorted(
                        canonical_json(dict(row))
                        for row in conn.execute(f"SELECT * FROM {table}")  # noqa: S608
                    )
                }
            )
            for table in CANONICAL_TABLES
        }
    finally:
        conn.close()


def test_first_seed_loads_the_expected_fixture_counts(tmp_path):
    _, summary = seed_into(tmp_path)

    assert summary.inserted["policy_versions"] == 7
    assert summary.inserted["policy_clauses"] == 14
    assert summary.inserted["claims"] == 12
    assert len(summary.rejected_invalid) == 6
    assert summary.rejected_conflict == ()


def test_second_seed_changes_nothing(tmp_path):
    db_path, first = seed_into(tmp_path)
    before = table_digest(db_path)

    second = seed_into_existing(db_path, tmp_path)

    assert second.inserted == {}
    assert second.unchanged["claims"] == first.inserted["claims"]
    assert table_digest(db_path) == before


def seed_into_existing(db_path, tmp_path):
    return run_seed(
        database_path=db_path,
        demo_root=db_path.parent,
        fixtures_dir=FIXTURES_DIR,
        principals_file=PRINCIPALS_FILE,
    )


def test_non_demo_destination_is_rejected_without_modification(tmp_path):
    protected = tmp_path / "production-like.db"
    protected.write_bytes(b"important bytes that are not a sqlite database")
    before = protected.read_bytes()

    with pytest.raises(UnsafeDestinationError):
        assert_demo_destination(protected, demo_root=tmp_path / "demo")

    assert protected.read_bytes() == before


def test_well_named_database_without_the_demo_marker_is_rejected(tmp_path):
    """Proves the guard does not trust the filename."""
    demo_root = tmp_path / "demo"
    demo_root.mkdir()
    impostor = demo_root / "aegis-demo.db"
    conn = sqlite3.connect(impostor)
    conn.execute("CREATE TABLE unrelated (x TEXT)")
    conn.commit()
    conn.close()
    before = impostor.read_bytes()

    with pytest.raises(UnsafeDestinationError):
        assert_demo_destination(impostor, demo_root=demo_root)

    assert impostor.read_bytes() == before


def test_foreign_keys_are_enforced(tmp_path):
    db_path = tmp_path / "fk.db"
    conn = connect(db_path)
    apply_schema(conn)

    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO policies VALUES ('policy-x-0001','tenant-missing-001','motor')")
