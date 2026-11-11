"""PART 1 — Stock intraday 15m OHLCV coverage classifier + backfill (paper data quality).

Classifies each stock symbol's 15m coverage so DATA_GAP_LATE trades can be excluded from A/B edge
stats, and (where the provider allows) backfills the last 60 days of 15m bars. Read-only on trading
logic; never touches signal_outcomes / final_r / no live.

Classes:
  DATA_OK          — recent continuous 15m coverage
  PARTIAL_DATA     — some sessions missing
  DATA_GAP_LATE    — bars start well after the session open (the MSTR pattern)
  NO_INTRADAY_DATA — no 15m bars at all
"""
from __future__ import annotations

import sqlite3
import os
import uuid
from datetime import datetime, timezone

import pandas as pd

from src.config import load_config
from src.storage.file_store import FileStore
from src.stocks.market_calendar import latest_us_cash_session

_DDL = """
CREATE TABLE IF NOT EXISTS stock_intraday_coverage (
  symbol TEXT PRIMARY KEY, status TEXT, bars INTEGER, first_bar TEXT, last_bar TEXT,
  span_days REAL, first_bar_gap_min REAL, sessions INTEGER, computed_at TEXT
);
"""


def ensure_table(conn):
    conn.execute(_DDL)
    conn.commit()


def classify(df: pd.DataFrame | None) -> dict:
    if df is None or df.empty or "timestamp" not in df.columns:
        return {"status": "NO_INTRADAY_DATA", "bars": 0, "first_bar": None, "last_bar": None,
                "span_days": None, "first_bar_gap_min": None, "sessions": 0}
    d = df.copy()
    d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
    d = d.sort_values("timestamp")
    first, last = d["timestamp"].iloc[0], d["timestamp"].iloc[-1]
    span = (last - first).total_seconds() / 86400.0
    sessions = d["timestamp"].dt.date.nunique()
    # First-bar gap against the DST-aware NYSE open for the first covered session.
    day1 = d[d["timestamp"].dt.date == first.date()]
    open_utc, _, _ = latest_us_cash_session(first.to_pydatetime())
    open_utc = pd.Timestamp(open_utc)
    gap = max(0.0, (day1["timestamp"].iloc[0] - open_utc).total_seconds() / 60.0)
    # expected ~26 fifteen-min bars per RTH session; flag partial if avg far below
    avg_bars = len(d) / max(1, sessions)
    if gap > 60:
        status = "DATA_GAP_LATE"
    elif avg_bars < 13:
        status = "PARTIAL_DATA"
    else:
        status = "DATA_OK"
    return {"status": status, "bars": len(d), "first_bar": str(first), "last_bar": str(last),
            "span_days": round(span, 2), "first_bar_gap_min": round(gap, 1), "sessions": sessions}


def coverage_report(symbols: list[str] | None = None, db: str | None = None) -> dict:
    cfg = load_config()
    fs = FileStore(cfg)
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    ensure_table(conn)
    if not symbols:
        symbols = [r[0] for r in conn.execute(
            "SELECT DISTINCT symbol FROM proposed_signals WHERE asset_class='stocks'").fetchall()]
    now = datetime.now(timezone.utc).isoformat()
    by_status: dict[str, int] = {}
    rows = []
    for sym in symbols:
        df = fs.load_stocks_ohlcv(sym, "15m")
        c = classify(df)
        conn.execute(
            "INSERT OR REPLACE INTO stock_intraday_coverage "
            "(symbol,status,bars,first_bar,last_bar,span_days,first_bar_gap_min,sessions,computed_at) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (sym, c["status"], c["bars"], c["first_bar"], c["last_bar"], c["span_days"],
             c["first_bar_gap_min"], c["sessions"], now))
        by_status[c["status"]] = by_status.get(c["status"], 0) + 1
        rows.append({"symbol": sym, **c})
    conn.commit()
    conn.close()
    return {"symbols": len(symbols), "by_status": by_status, "rows": rows}


def backfill(symbols: list[str], lookback_days: int = 60, interval: str = "15m") -> dict:
    """Best-effort intraday backfill through the shared Finnhub -> yfinance provider chain."""
    cfg = load_config()
    fs = FileStore(cfg)
    fetched = {}
    try:
        from src.stocks.data_collectors.yf_client import fetch_ohlcv
    except Exception as e:
        return {"ok": False, "reason": f"stocks provider unavailable: {e}", "fetched": {}}
    for sym in symbols:
        try:
            result = fetch_ohlcv(sym, interval=interval, period=f"{int(lookback_days)}d")
            if result is not None and not result.dataframe.empty:
                frame = result.dataframe.reset_index().rename(columns={"index": "timestamp"})
                path = fs.stocks_ohlcv_path(sym, interval)
                path.parent.mkdir(parents=True, exist_ok=True)
                tmp = path.with_name(f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
                try:
                    frame.to_csv(tmp, index=False)
                    os.replace(tmp, path)
                finally:
                    try:
                        tmp.unlink(missing_ok=True)
                    except OSError:
                        pass
                fetched[sym] = {"bars": len(frame), "source": result.source}
        except Exception:
            continue
    return {"ok": True, "fetched": fetched, "count": len(fetched)}


def get_coverage(symbol: str, db: str | None = None) -> dict | None:
    cfg = load_config()
    conn = sqlite3.connect(db or cfg.db_path)
    conn.row_factory = sqlite3.Row
    try:
        ensure_table(conn)
        row = conn.execute("SELECT * FROM stock_intraday_coverage WHERE symbol=?", (symbol,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
