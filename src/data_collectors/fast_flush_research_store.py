"""Small append-only 1m archive for fast-flush research and Paper replay."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

import pandas as pd

from src.execution.shadow_strategy_common import normalize_frame


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "research_labs" / "fast_flush_reclaim_v3" / "market_data.sqlite"


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    target = Path(path) if path else DEFAULT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS ohlcv_1m (
          exchange TEXT NOT NULL, symbol TEXT NOT NULL, ts INTEGER NOT NULL,
          open REAL NOT NULL, high REAL NOT NULL, low REAL NOT NULL,
          close REAL NOT NULL, volume REAL NOT NULL,
          PRIMARY KEY(exchange,symbol,ts)
        );
        CREATE INDEX IF NOT EXISTS idx_ff_ohlcv_symbol_ts ON ohlcv_1m(symbol,ts);
        CREATE TABLE IF NOT EXISTS candidate_events (
          event_id TEXT PRIMARY KEY, symbol TEXT NOT NULL, event_at TEXT NOT NULL,
          liquidation_notional_usd REAL NOT NULL, liquidation_percentile REAL,
          source TEXT NOT NULL, metadata_json TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_ff_events_symbol_at ON candidate_events(symbol,event_at);
        CREATE TABLE IF NOT EXISTS coverage (
          exchange TEXT NOT NULL, symbol TEXT NOT NULL, first_ts INTEGER,
          last_ts INTEGER, rows INTEGER NOT NULL, updated_at TEXT NOT NULL,
          PRIMARY KEY(exchange,symbol)
        );
        """
    )
    return conn


def insert_rows(conn: sqlite3.Connection, exchange: str, symbol: str,
                rows: Iterable[tuple[int, float, float, float, float, float]]) -> int:
    before = conn.total_changes
    conn.executemany(
        "INSERT OR IGNORE INTO ohlcv_1m(exchange,symbol,ts,open,high,low,close,volume) "
        "VALUES(?,?,?,?,?,?,?,?)",
        ((exchange, symbol, *row) for row in rows),
    )
    added = conn.total_changes - before
    stats = conn.execute(
        "SELECT MIN(ts),MAX(ts),COUNT(*) FROM ohlcv_1m WHERE exchange=? AND symbol=?",
        (exchange, symbol),
    ).fetchone()
    conn.execute(
        "INSERT OR REPLACE INTO coverage VALUES(?,?,?,?,?,datetime('now'))",
        (exchange, symbol, stats[0], stats[1], stats[2]),
    )
    return added


def load_frame(conn: sqlite3.Connection, symbol: str, start_ms: int, end_ms: int,
               exchanges: tuple[str, ...] = ("bybit", "binance")) -> tuple[pd.DataFrame, str | None]:
    for exchange in exchanges:
        rows = conn.execute(
            "SELECT ts,open,high,low,close,volume FROM ohlcv_1m "
            "WHERE exchange=? AND symbol=? AND ts>=? AND ts<=? ORDER BY ts",
            (exchange, symbol, start_ms, end_ms),
        ).fetchall()
        if rows:
            frame = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
            frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
            return normalize_frame(frame), exchange
    return pd.DataFrame(), None


def archive_runtime_frames(symbols: list[str]) -> dict[str, int]:
    """Persist the rolling Binance/Bybit 1m caches without touching live stores."""
    from src.config import load_config
    from src.storage.file_store import FileStore

    store = FileStore(load_config())
    conn = connect()
    added: dict[str, int] = {}
    try:
        runtime_aliases = {
            "bybit": ("bybit_linear", "bybit"),
            "binance": ("binance",),
        }
        for exchange, runtime_names in runtime_aliases.items():
            total = 0
            for symbol in symbols:
                candidates = [
                    normalize_frame(store.load_ohlcv(runtime_name, symbol, "1m"))
                    for runtime_name in runtime_names
                ]
                candidates = [frame for frame in candidates if not frame.empty]
                frame = (
                    max(candidates, key=lambda value: value["timestamp"].iloc[-1])
                    if candidates else pd.DataFrame()
                )
                if frame.empty:
                    continue
                rows = []
                for _, row in frame.iterrows():
                    ts = int(pd.Timestamp(row["timestamp"]).timestamp() * 1000)
                    rows.append((ts, float(row["open"]), float(row["high"]), float(row["low"]),
                                 float(row["close"]), float(row["volume"])))
                total += insert_rows(conn, exchange, symbol, rows)
            added[exchange] = total
        conn.commit()
        return added
    finally:
        conn.close()


__all__ = ["DEFAULT_PATH", "archive_runtime_frames", "connect", "insert_rows", "load_frame"]
