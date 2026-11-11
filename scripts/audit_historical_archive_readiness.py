"""PART 5 — Historical archive readiness audit.

Inspect existing OHLCV / derivatives / funding storage and decide:
  - Are they rolling (overwritten each cycle) or append-only?
  - What's the smallest safe change to make them append-only?

Read-only — no code change.
"""

from __future__ import annotations

import sys
import statistics
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def coverage(dirpath: Path) -> dict:
    files = list(dirpath.glob("*.csv"))
    if not files:
        return {}
    rows = []
    first_ts, last_ts = None, None
    for p in files[:50]:
        try:
            df = pd.read_csv(p, nrows=1)
            tail = pd.read_csv(p).tail(1)
            tcol = "timestamp" if "timestamp" in df.columns else next(
                (c for c in df.columns if "ime" in c.lower() or "ate" in c.lower()), df.columns[0])
            t0 = df[tcol].iloc[0]
            t1 = tail[tcol].iloc[0]
            rows.append(len(pd.read_csv(p)))
            if first_ts is None or t0 < first_ts: first_ts = t0
            if last_ts is None or t1 > last_ts: last_ts = t1
        except Exception:
            continue
    return {
        "n_files": len(files),
        "median_rows": statistics.median(rows) if rows else 0,
        "first_ts": first_ts, "last_ts": last_ts,
    }


def main() -> None:
    out = []
    out.append("# Historical Archive Readiness Audit (PART 5)")
    out.append("")
    out.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    out.append("")
    out.append("## 1. OHLCV archive — current state")
    out.append("")
    out.append("| Source | TF | n files | median rows | window | append-only? |")
    out.append("|---|---|---:|---:|---|---|")
    for exch in ("binance", "bybit", "mexc"):
        for tf in ("1m", "5m", "15m", "1h", "1d"):
            cov = coverage(ROOT / "data" / "raw" / "ohlcv" / exch / tf)
            if not cov:
                continue
            is_append = "❌ rolling (~220 rows)" if cov["median_rows"] <= 230 else "✅ growing"
            out.append(f"| {exch} | {tf} | {cov['n_files']} | {cov['median_rows']} | "
                       f"{(cov['first_ts'] or '')[:10]}..{(cov['last_ts'] or '')[:10]} | {is_append} |")
    for tf in ("15m", "1h", "1d", "1wk"):
        cov = coverage(ROOT / "data" / "raw" / "stocks" / tf)
        if not cov:
            continue
        is_append = "✅ append-only" if cov["median_rows"] > 500 else "❌ rolling"
        out.append(f"| stocks (yfinance) | {tf} | {cov['n_files']} | {cov['median_rows']} | "
                   f"{(cov['first_ts'] or '')[:10]}..{(cov['last_ts'] or '')[:10]} | {is_append} |")
    out.append("")
    out.append("## 2. Funding / OI snapshot archive")
    out.append("")
    fund_path = ROOT / "data" / "raw" / "derivatives" / "funding"
    oi_path = ROOT / "data" / "raw" / "derivatives" / "oi"
    out.append(f"- Funding archive at `{fund_path.relative_to(ROOT)}`: "
               f"{'exists' if fund_path.exists() else '❌ missing'}")
    out.append(f"- OI archive at `{oi_path.relative_to(ROOT)}`: "
               f"{'exists' if oi_path.exists() else '❌ missing'}")
    # The production `oi_context` / `funding_context` columns in `proposed_signals`
    # are latest-cache string blobs, not time series.
    out.append("- `proposed_signals.funding_context` / `oi_context` are **latest-cache string blobs**, not a time series.")
    out.append("")
    out.append("## 3. Spread / depth snapshot")
    out.append("")
    out.append("- No archive currently. Spread is implicitly estimated from candle (high-low)/close, no L2 order book stored.")
    out.append("")
    out.append("## 4. Verdict")
    out.append("")
    out.append("| Surface | Append-only? | Smallest safe change |")
    out.append("|---|---|---|")
    out.append("| Crypto 1m / 5m / 15m / 1h | ❌ rolling (~220 rows) | Switch `FileStore.save_ohlcv()` to **append + dedup-by-timestamp** for `1m` and `5m` first |")
    out.append("| Stocks 15m / 1h / 1d | ✅ append-only (yfinance returns long history) | no change needed |")
    out.append("| Funding | ❌ latest-cache only | new collector + new table `funding_snapshots(symbol, exchange, ts, rate)` |")
    out.append("| OI | ❌ latest-cache only | new table `oi_snapshots(symbol, exchange, ts, oi_usd)` |")
    out.append("| Spread / depth | ❌ none | optional `orderbook_snapshots(symbol, ts, bid_size_25bps, ask_size_25bps)` |")
    out.append("")
    out.append("## 5. Smallest safe change proposal (NOT implemented in this pass)")
    out.append("")
    out.append("```python")
    out.append("# src/storage/file_store.py")
    out.append("def save_ohlcv(self, exchange, symbol, timeframe, frame):")
    out.append("    path = self.ohlcv_path(exchange, symbol, timeframe)")
    out.append("    path.parent.mkdir(parents=True, exist_ok=True)")
    out.append("    if path.exists() and timeframe in ('1m', '5m'):")
    out.append("        # Append-only path: read old, concat, dedup by timestamp, write.")
    out.append("        old = pd.read_csv(path)")
    out.append("        old['timestamp'] = pd.to_datetime(old['timestamp'], utc=True)")
    out.append("        merged = pd.concat([old, frame]).drop_duplicates('timestamp', keep='last')")
    out.append("        merged = merged.sort_values('timestamp')")
    out.append("        merged.to_csv(path, index=False)")
    out.append("    else:")
    out.append("        frame.to_csv(path, index=False)  # legacy behavior")
    out.append("    return path")
    out.append("```")
    out.append("")
    out.append("Risk: file size grows. Cap at 30 days rolling = ~43k rows per symbol per 1m, ~9k per 5m. Acceptable.")
    out.append("")
    out.append("**Decision for this pass: document only.** A future task can implement after operator approval.")

    out_md = ROOT / "reports" / "HISTORICAL_ARCHIVE_READINESS_AUDIT.md"
    out_md.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
