"""Connection construction. Foreign keys on, rows as mappings, read-only where it matters."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


def connect(path: Path, *, read_only: bool = False) -> sqlite3.Connection:
    """Open a connection with foreign keys enforced.

    Uses Path.as_uri() rather than string formatting: on Windows a bare 'file:C:/...' is not a
    valid SQLite URI, and as_uri() also percent-escapes the path. read_only matters more than it
    looks — sqlite3.connect() CREATES a missing file, so an inspection that is not mode=ro
    becomes the mutation it was meant to prevent.
    """
    uri = path.resolve().as_uri()
    if read_only:
        uri = f"{uri}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def transaction(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """All-or-nothing. A partial seed is worse than no seed."""
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield conn
    except Exception:
        conn.execute("ROLLBACK")
        raise
    conn.execute("COMMIT")


def fts5_available(conn: sqlite3.Connection) -> bool:
    """Probe once at construction, never per query."""
    try:
        conn.execute("CREATE VIRTUAL TABLE temp.fts_probe USING fts5(x)")
    except sqlite3.OperationalError:
        return False
    conn.execute("DROP TABLE temp.fts_probe")
    return True
