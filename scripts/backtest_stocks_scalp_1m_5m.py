"""Stocks 1m/5m scalp backtest — RESEARCH-ONLY harness skeleton (2026-06-16).

This is NOT a production mode and does NOT trade. It is the runnable scaffold for the
plan in reports/STOCKS_SCALP_BACKTEST_PLAN.md.

IMPORTANT — data gate: a decision-grade scalp backtest needs >= 6 months of 1m/5m RTH
candles. Free sources (yfinance) cannot supply that (1m ~30d, 5m ~60d). So this harness
*refuses to emit a verdict* unless the qualifying data is present under
data/raw/stocks/{1m,5m}/{SYMBOL}.csv. With <60d it prints a SMOKE-TEST-ONLY banner.

Promotion bar (do not weaken): net-positive (PF>1) after realistic spread+commission+
slippage in TRAIN, VALIDATION and OOS simultaneously, >= 6 months. Crypto scalp failed
this; stocks scalp must clear it before any production proposal.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOCK_TF_DIR = ROOT / "data" / "raw" / "stocks"

UNIVERSE = ["AAPL", "MSFT", "NVDA", "AMD", "TSLA", "META", "AMZN", "GOOGL",
            "QQQ", "SPY", "SMH", "XLK"]

VARIANTS = {
    "A": "current intraday geometry compressed to scalp",
    "B": "opening-range breakout",
    "C": "VWAP reclaim",
    "D": "relative-volume spike",
    "E": "sector-confirmed momentum",
    "F": "catalyst-backed only",
    "G": "no-news technical scalp",
    "H": "no stock scalp (control)",
}

# Realistic cost model knobs (research). Scalp dies on cost — keep these honest.
COST = {
    "half_spread_bps": 1.0,        # effective half-spread on mega-caps; wider for high-beta
    "commission_per_share": 0.0,   # retail $0 + PFOF; sensitivity run at 0.005
    "slippage_ticks_entry": 1,
    "slippage_ticks_stop": 1,
    "round_trip_bps_estimate": 4.0,  # conservative all-in for sensitivity
}

MIN_DAYS_FOR_VERDICT = 180          # >= 6 months
MIN_DAYS_FOR_SMOKE = 20


def _available_data():
    """Return (tf, n_symbols_with_data, approx_days) for the finest tf present."""
    for tf in ("1m", "5m"):
        d = STOCK_TF_DIR / tf
        if not d.exists():
            continue
        files = [p for p in d.glob("*.csv")]
        syms = [p.stem for p in files if p.stem in UNIVERSE]
        if not syms:
            continue
        # crude day estimate from the largest file's line count / (~390 bars/RTH-day for 1m)
        bars_per_day = 390 if tf == "1m" else 78
        try:
            biggest = max(files, key=lambda p: p.stat().st_size)
            lines = sum(1 for _ in biggest.open(encoding="utf-8", errors="ignore"))
            days = max(0, (lines - 1)) // bars_per_day
        except Exception:
            days = 0
        return tf, len(syms), days
    return None, 0, 0


def main() -> int:
    print("Stocks 1m/5m scalp backtest — RESEARCH-ONLY harness")
    print(f"Universe: {len(UNIVERSE)} symbols · Variants: {','.join(VARIANTS)}")
    print(f"Cost model: {COST}")
    tf, nsym, days = _available_data()
    if not tf or nsym == 0:
        print("\nDATA GATE: no 1m/5m stock candles under data/raw/stocks/{1m,5m}/.")
        print("Cannot run. Acquire >= 6 months of 1m/5m RTH data first "
              "(no paid APIs permitted -- currently BLOCKED).")
        print("VERDICT: STOCKS_SCALP_BACKTEST_REQUIRED (data unavailable).")
        return 0
    print(f"\nFound {tf} data for {nsym}/{len(UNIVERSE)} symbols, ~{days} RTH days.")
    if days < MIN_DAYS_FOR_SMOKE:
        print("Insufficient even for a smoke test. BLOCKED.")
        print("VERDICT: STOCKS_SCALP_BACKTEST_REQUIRED (data too short).")
        return 0
    if days < MIN_DAYS_FOR_VERDICT:
        print(f"\n*** SMOKE-TEST ONLY: {days}d < {MIN_DAYS_FOR_VERDICT}d. ***")
        print("Results are INDICATIVE, not decision-grade. No train/val/OOS. "
              "Do NOT promote stocks scalp on this sample (crypto-scalp lesson).")
    # NOTE: the per-variant walk + cost application + metrics are implemented when
    # qualifying data exists. Intentionally not fabricating results without data.
    print("\n[harness ready] Implement variant walk once qualifying data is present.")
    print("Promotion bar: PF>1 net of spread+commission+slippage in TRAIN+VAL+OOS, >=6mo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
