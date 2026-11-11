"""Append-only stock OHLCV archive for liquidity-shock research."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.execution.shadow_strategy_common import normalize_frame


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "research_labs" / "stocks_liquidity_shock_reclaim_v1" / "market_data.sqlite"


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    target = Path(path) if path else DEFAULT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS ohlcv (
          symbol TEXT NOT NULL, timeframe TEXT NOT NULL, ts INTEGER NOT NULL,
          open REAL NOT NULL, high REAL NOT NULL, low REAL NOT NULL,
          close REAL NOT NULL, volume REAL NOT NULL, source TEXT NOT NULL,
          PRIMARY KEY(symbol,timeframe,ts)
        );
        CREATE INDEX IF NOT EXISTS idx_stock_lsr_ohlcv ON ohlcv(timeframe,symbol,ts);
        CREATE TABLE IF NOT EXISTS coverage (
          symbol TEXT NOT NULL, timeframe TEXT NOT NULL, first_ts INTEGER,
          last_ts INTEGER, rows INTEGER NOT NULL, source TEXT NOT NULL,
          updated_at TEXT NOT NULL, PRIMARY KEY(symbol,timeframe)
        );
        """
    )
    return conn


def _cache_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        frame = pd.read_csv(path)
    except Exception:
        return pd.DataFrame()
    if frame.empty:
        return frame
    first = str(frame.columns[0])
    if "timestamp" not in {str(column).lower() for column in frame.columns}:
        frame = frame.rename(columns={first: "timestamp"})
    return normalize_frame(frame)


def insert_frame(conn: sqlite3.Connection, symbol: str, timeframe: str,
                 frame: pd.DataFrame, *, source: str = "runtime_cache") -> int:
    clean = normalize_frame(frame)
    if clean.empty:
        return 0
    before = conn.total_changes
    rows = []
    for _, row in clean.iterrows():
        values = [row.get(key) for key in ("open", "high", "low", "close", "volume")]
        if any(value is None or pd.isna(value) for value in values):
            continue
        rows.append((symbol.upper(), timeframe, int(pd.Timestamp(row["timestamp"]).timestamp() * 1000),
                     *(float(value) for value in values), source))
    conn.executemany(
        "INSERT OR IGNORE INTO ohlcv(symbol,timeframe,ts,open,high,low,close,volume,source) "
        "VALUES(?,?,?,?,?,?,?,?,?)", rows,
    )
    added = conn.total_changes - before
    stats = conn.execute(
        "SELECT MIN(ts),MAX(ts),COUNT(*),MAX(source) FROM ohlcv WHERE symbol=? AND timeframe=?",
        (symbol.upper(), timeframe),
    ).fetchone()
    conn.execute(
        "INSERT OR REPLACE INTO coverage VALUES(?,?,?,?,?,?,?)",
        (symbol.upper(), timeframe, stats[0], stats[1], stats[2], stats[3],
         datetime.now(timezone.utc).isoformat()),
    )
    return added


def archive_runtime_frames(symbols: list[str], timeframes: tuple[str, ...] = ("1m", "15m"),
                           *, root: Path | None = None) -> dict[str, int]:
    base = (root or ROOT) / "data" / "raw" / "stocks"
    conn = connect()
    added: dict[str, int] = {}
    try:
        for timeframe in timeframes:
            total = 0
            for symbol in sorted({str(value).upper() for value in symbols}):
                total += insert_frame(
                    conn, symbol, timeframe,
                    _cache_frame(base / timeframe / f"{symbol}.csv"),
                )
            added[timeframe] = total
        conn.commit()
        return added
    finally:
        conn.close()


def load_frame(conn: sqlite3.Connection, symbol: str, timeframe: str,
               start_ms: int | None = None, end_ms: int | None = None) -> pd.DataFrame:
    where = ["symbol=?", "timeframe=?"]
    params: list[object] = [symbol.upper(), timeframe]
    if start_ms is not None:
        where.append("ts>=?")
        params.append(int(start_ms))
    if end_ms is not None:
        where.append("ts<=?")
        params.append(int(end_ms))
    rows = conn.execute(
        "SELECT ts,open,high,low,close,volume FROM ohlcv WHERE "
        + " AND ".join(where) + " ORDER BY ts", params,
    ).fetchall()
    if not rows:
        return pd.DataFrame()
    frame = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
    return normalize_frame(frame)


__all__ = ["DEFAULT_PATH", "archive_runtime_frames", "connect", "insert_frame", "load_frame"]
