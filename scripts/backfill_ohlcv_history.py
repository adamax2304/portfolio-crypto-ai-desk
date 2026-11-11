"""Historical OHLCV backfill (FAST SAFE ACCELERATION PART 2).

Paginates exchange OHLCV (via ccxt, rate-limited) for trade-relevant symbols and
APPENDS into the long-history archive at data/archive/ohlcv/{ex}/{tf}/{SYM}.csv.

Safety:
- Writes ONLY to data/archive/ohlcv; NEVER touches data/raw/ohlcv (rolling cache).
- Append-only: concat → dedup by timestamp → sort ascending → write. Idempotent.
- Resumable: resumes from the archive's newest timestamp per (symbol,tf).
- Rate-limited (ccxt enableRateLimit); per-symbol retry with backoff; one bad
  symbol/timeframe is skipped + reported, never crashes the run.
- Dry-run prints the plan and writes nothing. No trading-logic change.

Usage:
  python -m scripts.backfill_ohlcv_history --timeframes 5m,15m --lookback-days 60 --limit 12
  python -m scripts.backfill_ohlcv_history --dry-run
"""
from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DB = ROOT / "db" / "crypto_ai_desk.sqlite"
ARCHIVE = ROOT / "data" / "archive" / "ohlcv"
REPORTS = ROOT / "reports"
CORE = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"]
TF_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "1h": 3_600_000}


def trade_relevant_symbols(limit: int) -> list[str]:
    """Core liquid names + symbols with recent closed crypto intraday/swing trades."""
    syms = list(CORE)
    try:
        conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
        since = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
        for r in conn.execute(
            "SELECT DISTINCT symbol FROM proposed_signals "
            "WHERE (asset_class='crypto' OR asset_class IS NULL) "
            "AND mode IN ('intraday','swing') AND created_at >= ?", (since,)):
            s = r[0]
            if s and s not in syms:
                syms.append(s)
        conn.close()
    except Exception:
        pass
    return syms[:limit] if limit else syms


def _archive_path(ex, tf, sym):
    return ARCHIVE / ex / tf / f"{sym.replace('/', '_').upper()}.csv"


def _existing(path: Path):
    if not path.exists():
        return None
    try:
        df = pd.read_csv(path)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        return df.dropna(subset=["timestamp"])
    except Exception:
        return None


def _merge_write(path: Path, fresh: pd.DataFrame) -> tuple[int, int]:
    existing = _existing(path)
    before = 0 if existing is None else len(existing)
    merged = pd.concat([existing, fresh], ignore_index=True) if existing is not None else fresh
    merged = (merged.drop_duplicates(subset=["timestamp"], keep="last")
                    .sort_values("timestamp").reset_index(drop=True))
    path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(path, index=False)
    return before, len(merged)


def _build_exchange(ex_id: str):
    import ccxt
    cls = getattr(ccxt, ex_id)
    return cls({"enableRateLimit": True, "options": {"defaultType": "spot"}})


def fetch_paginated(exchange, symbol, tf, since_ms, retries=3):
    """Fetch [since_ms, now] in batches of 1000. Retry with backoff; raise on
    repeated failure so the caller can skip+report."""
    out: list[list[float]] = []
    step = TF_MS.get(tf, 300_000)
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    cursor = since_ms
    while cursor < now_ms:
        ok = False
        for attempt in range(retries):
            try:
                batch = exchange.fetch_ohlcv(symbol, timeframe=tf, since=cursor, limit=1000)
                ok = True
                break
            except Exception:
                time.sleep(1.5 * (attempt + 1))
        if not ok:
            raise RuntimeError(f"fetch failed for {symbol} {tf} at {cursor}")
        if not batch:
            break
        out.extend(batch)
        last = batch[-1][0]
        if last <= cursor:
            break
        cursor = last + step
        if len(batch) < 1000:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeframes", default="5m,15m")
    ap.add_argument("--exchanges", default="binance")
    ap.add_argument("--lookback-days", type=int, default=60)
    ap.add_argument("--limit", type=int, default=12, help="max symbols (0=all relevant)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    tfs = [t.strip() for t in args.timeframes.split(",") if t.strip()]
    exs = [e.strip() for e in args.exchanges.split(",") if e.strip()]
    symbols = trade_relevant_symbols(args.limit)
    since_ms = int((datetime.now(timezone.utc) - timedelta(days=args.lookback_days)).timestamp() * 1000)

    print(f"plan: {len(symbols)} symbols x {len(tfs)} tf x {len(exs)} ex, "
          f"lookback {args.lookback_days}d, dry_run={args.dry_run}")
    print("symbols:", ", ".join(symbols))
    if args.dry_run:
        return

    gaps_rows = []
    progress = []
    for ex_id in exs:
        try:
            exchange = _build_exchange(ex_id)
            exchange.load_markets()
        except Exception as exc:
            print(f"SKIP exchange {ex_id}: {exc}")
            gaps_rows.append({"exchange": ex_id, "symbol": "*", "timeframe": "*",
                              "status": f"exchange_init_failed:{type(exc).__name__}",
                              "candles": 0, "oldest": "", "newest": "", "expected": 0})
            continue
        for sym in symbols:
            if sym not in exchange.markets:
                gaps_rows.append({"exchange": ex_id, "symbol": sym, "timeframe": "*",
                                  "status": "symbol_not_on_exchange", "candles": 0,
                                  "oldest": "", "newest": "", "expected": 0})
                continue
            for tf in tfs:
                path = _archive_path(ex_id, tf, sym)
                # Historical backfill: fetch the FULL lookback window so we fill the
                # deep history that the archive is MISSING (the archive may already
                # hold today's rolling window, so resuming from its newest would only
                # re-fetch today). Dedup-on-merge makes re-runs idempotent/resumable.
                resume_ms = since_ms
                try:
                    rows = fetch_paginated(exchange, sym, tf, resume_ms)
                except Exception as exc:
                    print(f"  skip {ex_id} {sym} {tf}: {exc}")
                    gaps_rows.append({"exchange": ex_id, "symbol": sym, "timeframe": tf,
                                      "status": f"fetch_failed:{type(exc).__name__}",
                                      "candles": 0, "oldest": "", "newest": "", "expected": 0})
                    continue
                if not rows:
                    progress.append((ex_id, sym, tf, 0))
                    continue
                fresh = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
                fresh["timestamp"] = pd.to_datetime(fresh["ts"], unit="ms", utc=True)
                fresh = fresh[["timestamp", "open", "high", "low", "close", "volume"]]
                before, total = _merge_write(path, fresh)
                merged = _existing(path)
                oldest = str(merged["timestamp"].min())[:16]
                newest = str(merged["timestamp"].max())[:16]
                span_d = (merged["timestamp"].max() - merged["timestamp"].min()).total_seconds() / 86400
                expected = int(args.lookback_days * 86400_000 / TF_MS.get(tf, 300_000))
                gap_pct = round(max(0.0, 1 - total / expected) * 100, 1) if expected else 0
                gaps_rows.append({"exchange": ex_id, "symbol": sym, "timeframe": tf,
                                  "status": "ok", "candles": total, "oldest": oldest,
                                  "newest": newest, "expected": expected})
                progress.append((ex_id, sym, tf, total - before))
                print(f"  {ex_id} {sym} {tf}: +{total - before} (total {total}, "
                      f"{oldest}..{newest}, span {span_d:.1f}d, gap {gap_pct}%)")

    REPORTS.mkdir(parents=True, exist_ok=True)
    gaps_csv = REPORTS / "OHLCV_HISTORICAL_BACKFILL_GAPS.csv"
    if gaps_rows:
        with gaps_csv.open("w", newline="", encoding="utf-8") as fo:
            w = csv.DictWriter(fo, fieldnames=["exchange", "symbol", "timeframe", "status",
                                               "candles", "oldest", "newest", "expected"])
            w.writeheader(); w.writerows(gaps_rows)
    print(f"done: {sum(1 for r in gaps_rows if r['status']=='ok')} ok, "
          f"{sum(1 for r in gaps_rows if r['status']!='ok')} skipped/failed; gaps -> {gaps_csv}")


if __name__ == "__main__":
    main()
