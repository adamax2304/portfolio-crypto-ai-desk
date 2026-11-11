"""Append-only historical OHLCV downloader for the scalp backtest (PART 2).

Downloads 1m/5m/15m candles from Binance (ccxt) into an append-only SQLite
archive with dedup on (exchange, symbol, timeframe, ts). Resumable: re-running
continues from the newest stored candle per (symbol, tf).

Storage: db/scalp_history.sqlite (separate from production DB — never touches
crypto_ai_desk.sqlite).

Usage:
  python scripts/download_scalp_history.py --tf 5m --months 12
  python scripts/download_scalp_history.py --tf 1m --days 90
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "db" / "scalp_history.sqlite"

# Focused high-liquidity universe (Binance USDT spot). Avoids thin/delisted.
UNIVERSE = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT",
    "DOGE/USDT", "ADA/USDT", "AVAX/USDT", "LINK/USDT", "TON/USDT",
    "NEAR/USDT", "APT/USDT", "ARB/USDT", "OP/USDT", "SUI/USDT",
]

TF_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "1h": 3_600_000}


def _init(con: sqlite3.Connection) -> None:
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS ohlcv (
            exchange TEXT NOT NULL,
            symbol TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            ts INTEGER NOT NULL,
            open REAL, high REAL, low REAL, close REAL, volume REAL,
            PRIMARY KEY (exchange, symbol, timeframe, ts)
        );
        CREATE INDEX IF NOT EXISTS idx_ohlcv_sym_tf ON ohlcv(symbol, timeframe, ts);
        CREATE TABLE IF NOT EXISTS coverage (
            exchange TEXT, symbol TEXT, timeframe TEXT,
            first_ts INTEGER, last_ts INTEGER, n_candles INTEGER,
            updated_at TEXT,
            PRIMARY KEY (exchange, symbol, timeframe)
        );
        """
    )


def _newest_ts(con, exch, sym, tf) -> int | None:
    row = con.execute(
        "SELECT MAX(ts) FROM ohlcv WHERE exchange=? AND symbol=? AND timeframe=?",
        (exch, sym, tf),
    ).fetchone()
    return row[0] if row and row[0] else None


def download(tf: str, since_ms: int, exchange_id: str = "binance") -> None:
    import ccxt
    ex = getattr(ccxt, exchange_id)({"enableRateLimit": True, "timeout": 20000})
    con = sqlite3.connect(ARCHIVE)
    _init(con)
    step = TF_MS[tf]
    now_ms = ex.milliseconds()
    for sym in UNIVERSE:
        start = _newest_ts(con, exchange_id, sym, tf)
        cursor = (start + step) if start else since_ms
        got = 0
        while cursor < now_ms:
            try:
                batch = ex.fetch_ohlcv(sym, tf, since=cursor, limit=1000)
            except Exception as exc:
                print(f"  {sym} {tf}: fetch error {type(exc).__name__}; retry in 3s")
                time.sleep(3)
                continue
            if not batch:
                break
            rows = [(exchange_id, sym, tf, c[0], c[1], c[2], c[3], c[4], c[5]) for c in batch]
            con.executemany(
                "INSERT OR IGNORE INTO ohlcv VALUES(?,?,?,?,?,?,?,?,?)", rows
            )
            con.commit()
            got += len(batch)
            cursor = batch[-1][0] + step
            if len(batch) < 1000:
                break
        # coverage
        r = con.execute(
            "SELECT MIN(ts), MAX(ts), COUNT(*) FROM ohlcv WHERE exchange=? AND symbol=? AND timeframe=?",
            (exchange_id, sym, tf),
        ).fetchone()
        con.execute(
            "INSERT OR REPLACE INTO coverage VALUES(?,?,?,?,?,?,datetime('now'))",
            (exchange_id, sym, tf, r[0], r[1], r[2]),
        )
        con.commit()
        print(f"  {sym} {tf}: +{got} new, total={r[2]}")
    con.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tf", required=True, choices=list(TF_MS.keys()))
    ap.add_argument("--months", type=int, default=0)
    ap.add_argument("--days", type=int, default=0)
    ap.add_argument("--exchange", default="binance")
    args = ap.parse_args()
    import ccxt
    ex = getattr(ccxt, args.exchange)({"enableRateLimit": True})
    lookback_days = args.days or (args.months * 30) or 365
    since_ms = ex.milliseconds() - lookback_days * 24 * 3600 * 1000
    print(f"downloading {args.tf} for {len(UNIVERSE)} symbols, lookback {lookback_days}d, exchange={args.exchange}")
    download(args.tf, since_ms, args.exchange)
    print("done")


if __name__ == "__main__":
    main()
