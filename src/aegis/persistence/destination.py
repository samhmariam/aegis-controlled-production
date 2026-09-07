"""Refuse to create or mutate anything that is not a demo database.

Every check here is read-only. A guard that can damage the thing it is protecting is not a guard.
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

from aegis.errors import UnsafeDestinationError
from aegis.persistence.connection import connect
from aegis.persistence.schema import DEMO_DATABASE_PURPOSE, PERSISTENCE_SCHEMA_VERSION


def assert_demo_destination(path: Path, *, demo_root: Path) -> None:
    """Raise UnsafeDestinationError unless path is a safe demo destination.

    Four checks, in order:
      1. containment — the path sits inside the configured demo directory;
      2. absence     — a non-existent path inside that directory is safe to create;
      3. readability — an existing file opens as SQLite and exposes schema_meta;
      4. identity    — it is marked as a demo database at a compatible schema version.

    Check 3 uses a read-only connection. That is not a nicety: sqlite3.connect() creates a
    missing file, so a writable inspection would itself create or touch the target.
    """
    resolved = path.resolve()
    root = demo_root.resolve()

    if root != resolved.parent and root not in resolved.parents:
        raise UnsafeDestinationError("destination is outside the configured demo directory")

    if not resolved.exists():
        return

    if not resolved.is_file():
        raise UnsafeDestinationError("destination exists and is not a file")

    try:
        with closing(connect(resolved, read_only=True)) as conn:
            row = conn.execute(
                "SELECT database_purpose, schema_version FROM schema_meta WHERE id = 1"
            ).fetchone()
    except sqlite3.DatabaseError as exc:
        raise UnsafeDestinationError("existing file is not a recognised demo database") from exc

    if row is None or row["database_purpose"] != DEMO_DATABASE_PURPOSE:
        raise UnsafeDestinationError("existing database is not marked as a demo database")
    if row["schema_version"] != PERSISTENCE_SCHEMA_VERSION:
        raise UnsafeDestinationError("existing demo database has an incompatible schema version")
