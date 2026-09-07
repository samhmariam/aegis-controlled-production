from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from aegis.persistence.seed import SeedSummary, run_seed

FIXTURES_DIR = Path("data/synthetic")
PRINCIPALS_FILE = Path("controls/demo-principals.json")


def seed_into(tmp_path: Path) -> tuple[Path, SeedSummary]:
    demo_root = tmp_path / "demo"
    demo_root.mkdir(exist_ok=True)
    db_path = demo_root / "aegis-demo.db"
    summary = run_seed(
        database_path=db_path,
        demo_root=demo_root,
        fixtures_dir=FIXTURES_DIR,
        principals_file=PRINCIPALS_FILE,
    )
    return db_path, summary


@pytest.fixture(scope="session")
def seeded_template(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Seeded once per session. Never mutate this file; take a copy."""
    db_path, _ = seed_into(tmp_path_factory.mktemp("template"))
    return db_path


@pytest.fixture
def seeded_db(seeded_template: Path, tmp_path: Path) -> Path:
    """A private copy per test, so tampering tests cannot leak into their neighbours."""
    demo_root = tmp_path / "demo"
    demo_root.mkdir()
    db_path = demo_root / "aegis-demo.db"
    shutil.copyfile(seeded_template, db_path)
    return db_path
