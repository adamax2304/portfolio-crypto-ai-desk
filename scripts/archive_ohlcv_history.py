"""Append-only OHLCV archival (operational deploy PART 6).

The live cache `data/raw/ohlcv/{ex}/{tf}/{SYM}.csv` keeps only a rolling ~220-candle
window, so a path-aware profit-protection replay over weeks is impossible. This script
APPENDS the freshly-fetched rolling candles into a long-history archive at
`data/archive/ohlcv/{ex}/{tf}/{SYM}.csv`, deduped by timestamp and sorted.

Safety:
- READS the rolling cache; NEVER overwrites or deletes it (the trading pipeline keeps
  using `data/raw/ohlcv` exactly as before).
- Archive is append-only / grows monotonically (concat → dedup by timestamp → sort).
- No trading-logic change, no network calls, no paid APIs — it reuses whatever the
  collectors already wrote this cycle.

Usage:
  python -m scripts.archive_ohlcv_history --timeframes 5m,15m
  python -m scripts.archive_ohlcv_history --timeframes 5m,15m --dry-run
  python -m scripts.archive_ohlcv_history --coverage-report
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CACHE = ROOT / "data" / "raw" / "ohlcv"
ARCHIVE = ROOT / "data" / "archive" / "ohlcv"
EXCHANGES = ("binance", "bybit", "mexc")
REPORTS = ROOT / "reports"


def _read(path: Path) -> pd.DataFrame | None:
    try:
        df = pd.read_csv(path)
        if "timestamp" not in df.columns:
            return None
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        return df.dropna(subset=["timestamp"])
    except Exception:
        return None


def archive_one(ex: str, tf: str, sym_file: Path, *, dry_run: bool) -> dict:
    rolling = _read(sym_file)
    if rolling is None or rolling.empty:
        return {"appended": 0, "total": 0, "skipped": True}
    out_path = ARCHIVE / ex / tf / sym_file.name
    existing = _read(out_path) if out_path.exists() else None
    before = 0 if existing is None else len(existing)
    if existing is not None:
        merged = pd.concat([existing, rolling], ignore_index=True)
    else:
        merged = rolling.copy()
    # dedup by timestamp (keep the latest write), sort ascending
    merged = (merged.drop_duplicates(subset=["timestamp"], keep="last")
                    .sort_values("timestamp").reset_index(drop=True))
    appended = len(merged) - before
    if not dry_run:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        merged.to_csv(out_path, index=False)
    return {"appended": max(0, appended), "total": len(merged), "skipped": False}


def run_archive(timeframes: list[str], exchanges: list[str], *, dry_run: bool) -> dict:
    summary = {"dry_run": dry_run, "timeframes": timeframes, "per_tf": {}}
    for tf in timeframes:
        tf_stats = {"symbols": 0, "appended": 0, "archive_candles": 0}
        for ex in exchanges:
            src = CACHE / ex / tf
            if not src.exists():
                continue
            for f in sorted(src.glob("*.csv")):
                r = archive_one(ex, tf, f, dry_run=dry_run)
                if r["skipped"]:
                    continue
                tf_stats["symbols"] += 1
                tf_stats["appended"] += r["appended"]
                tf_stats["archive_candles"] += r["total"]
        summary["per_tf"][tf] = tf_stats
    return summary


def coverage_report(timeframes: list[str], exchanges: list[str]) -> str:
    lines = ["# OHLCV Archive — Coverage Report", "",
             f"**As of:** {datetime.now(timezone.utc).isoformat()} · source: `data/archive/ohlcv`",
             ""]
    any_data = False
    for tf in timeframes:
        lines.append(f"## {tf}")
        rows = []
        for ex in exchanges:
            base = ARCHIVE / ex / tf
            if not base.exists():
                continue
            files = sorted(base.glob("*.csv"))
            if not files:
                continue
            any_data = True
            oldest = None
            newest = None
            total = 0
            for f in files:
                df = _read(f)
                if df is None or df.empty:
                    continue
                total += len(df)
                tmin, tmax = df["timestamp"].min(), df["timestamp"].max()
                oldest = tmin if oldest is None else min(oldest, tmin)
                newest = tmax if newest is None else max(newest, tmax)
            span_days = round((newest - oldest).total_seconds() / 86400, 1) if (oldest is not None and newest is not None) else 0
            rows.append(f"| {ex} | {len(files)} | {str(oldest)[:16]} | {str(newest)[:16]} | {span_days} | {total} |")
        if rows:
            lines.append("| exchange | symbols | oldest | newest | span (d) | candles |")
            lines.append("|---|---|---|---|---|---|")
            lines += rows
        else:
            lines.append("_no archive yet for this timeframe — run the archive step first._")
        lines.append("")
    if not any_data:
        lines.append("> Archive is empty. It begins accumulating once the scheduler's "
                     "`ohlcv archive` step (or this script) has run at least once.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeframes", default="5m,15m")
    ap.add_argument("--exchanges", default=",".join(EXCHANGES))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--coverage-report", action="store_true")
    args = ap.parse_args()
    tfs = [t.strip() for t in args.timeframes.split(",") if t.strip()]
    exs = [e.strip() for e in args.exchanges.split(",") if e.strip()]

    if args.coverage_report:
        rep = coverage_report(tfs, exs)
        REPORTS.mkdir(parents=True, exist_ok=True)
        (REPORTS / "OHLCV_ARCHIVE_COVERAGE_REPORT.md").write_text(rep, encoding="utf-8")
        print("wrote reports/OHLCV_ARCHIVE_COVERAGE_REPORT.md")
        return

    summary = run_archive(tfs, exs, dry_run=args.dry_run)
    import json
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
