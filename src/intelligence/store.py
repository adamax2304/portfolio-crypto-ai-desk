"""Shared SQLite store for the shadow intelligence layer.

A single dedicated DB at data/intelligence/intelligence.sqlite, separate from the
trading DB and the rolling OHLCV cache. All tables are created lazily. Reads used in
the alert path are single-symbol indexed lookups (O(1)); compute/writes happen in
background scripts.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

_DB_PATH_CACHE: list[Path] = []


def db_path() -> Path:
    if _DB_PATH_CACHE:
        return _DB_PATH_CACHE[0]
    try:
        from src.config import load_config
        root = load_config().root
    except Exception:
        root = Path(__file__).resolve().parent.parent.parent
    p = Path(root) / "data" / "intelligence" / "intelligence.sqlite"
    _DB_PATH_CACHE.append(p)
    return p


def connect() -> sqlite3.Connection:
    p = db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p, timeout=15.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=15000")
    except sqlite3.DatabaseError:
        pass
    init_db(conn)
    return conn


def connect_ro() -> sqlite3.Connection | None:
    """Read-only connection for the alert path. Returns None if the DB does not
    exist yet (caller treats missing data as 'unknown')."""
    p = db_path()
    if not p.exists():
        return None
    try:
        conn = sqlite3.connect(f"file:{p.as_posix()}?mode=ro", uri=True, timeout=2.0)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception:
        return None


_INIT_DONE: list[bool] = []


def init_db(conn: sqlite3.Connection) -> None:
    if _INIT_DONE:
        return
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS timeline_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_at TEXT NOT NULL,
            payload_json TEXT,
            dedupe_key TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_tl_symbol ON timeline_events(symbol, event_at);
        CREATE UNIQUE INDEX IF NOT EXISTS idx_tl_dedupe ON timeline_events(dedupe_key);

        CREATE TABLE IF NOT EXISTS deriv_cache (
            symbol TEXT PRIMARY KEY, computed_at TEXT, fields_json TEXT);
        CREATE TABLE IF NOT EXISTS phase_cache (
            symbol TEXT PRIMARY KEY, computed_at TEXT, fields_json TEXT);
        CREATE TABLE IF NOT EXISTS phase_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL, phase TEXT, changed_at TEXT);
        CREATE INDEX IF NOT EXISTS idx_ph_symbol ON phase_history(symbol, changed_at);
        CREATE TABLE IF NOT EXISTS onchain_cache (
            symbol TEXT PRIMARY KEY, computed_at TEXT, fields_json TEXT);
        """
    )
    conn.commit()
    _INIT_DONE.append(True)


def read_cache(table: str, symbol: str) -> dict[str, Any] | None:
    """Read the cached fields_json for a symbol from a *_cache table. RO + safe."""
    conn = connect_ro()
    if conn is None:
        return None
    try:
        row = conn.execute(
            f"SELECT computed_at, fields_json FROM {table} WHERE symbol = ?",
            (symbol,),
        ).fetchone()
        if not row:
            return None
        import json
        out = json.loads(row["fields_json"] or "{}")
        out["_computed_at"] = row["computed_at"]
        return out
    except Exception:
        return None
    finally:
        conn.close()


def write_cache(conn: sqlite3.Connection, table: str, symbol: str,
                computed_at: str, fields: dict[str, Any]) -> None:
    import json
    conn.execute(
        f"INSERT INTO {table}(symbol, computed_at, fields_json) VALUES(?,?,?) "
        f"ON CONFLICT(symbol) DO UPDATE SET computed_at=excluded.computed_at, "
        f"fields_json=excluded.fields_json",
        (symbol, computed_at, json.dumps(fields)),
    )
