# Stocks 1m/5m Scalp Backtest Plan (PART 9)

**Date:** 2026-06-16 · **Research-only. No production stocks scalp.**

## ⚠️ Data feasibility blocker (read first)

A robust scalp backtest needs **6–12 months of 1m/5m RTH candles**. The current free
source (yfinance) **cannot** provide this:
- yfinance **1m** history ≈ last **7–30 days** only.
- yfinance **5m** history ≈ last **~60 days** only.
- No paid data API is permitted (constraint).

So a *robust, train/val/OOS* 6–12-month 1m/5m stock backtest is **not runnable today**.
Two honest paths:
1. **Preliminary-only (~60 days, 5m):** runnable now but **underpowered** — no real OOS,
   high overfit risk; results would be indicative, not decision-grade.
2. **Defer** until a sufficient 1m/5m source is available, then run the full plan below.

Recommended: treat any ≤60-day run as a *smoke test of the harness*, not evidence. Do not
promote stocks scalp on a 60-day sample (the crypto scalp lesson: small samples lied —
TP1@+0.5R looked good on a small set and was crushed at 12 months).

## Universe

AAPL, MSFT, NVDA, AMD, TSLA, META, AMZN, GOOGL · QQQ, SPY, SMH, XLK (+ optional high-beta
liquid: COIN, MSTR, PLTR, AVGO, SMCI).

## Data

- 1m and 5m candles; **≥ 6 months** (ideally 12); **RTH only**; premarket as a separate
  optional split. (Blocked — see above.)

## Test variants

| ID | Variant |
|----|---------|
| A | Current stocks intraday geometry compressed to scalp (15m → 5m/1m) |
| B | Opening-range breakout (first 15–30 min range) |
| C | VWAP reclaim |
| D | Relative-volume spike |
| E | Sector-confirmed momentum (symbol + sector ETF aligned) |
| F | Catalyst-backed only |
| G | No-news technical scalp |
| H | No stock scalp (baseline / control) |

## Costs (must be realistic — this is where crypto scalp died)

- **Spread:** per-symbol effective half-spread (mega-caps ~0.5–1bp; high-beta wider).
- **Commission:** model $0 retail + PFOF spread; also a sensitivity run at $0.005/share.
- **Slippage:** ≥ 1 tick on entry and on stop; model stop slippage explicitly (scalp stops
  are tight → slippage is a large fraction of R).
- **No unrealistic fills:** require the candle to trade *through* the level; conservative
  same-candle TP/stop resolution (stop-first).

## Metrics

WR · PF · avg R · max drawdown · **slippage sensitivity** (re-run at 0.5× / 1× / 2× cost) ·
session split (open/midday/close) · ticker split · catalyst-backed vs technical ·
**train / validation / OOS** (only meaningful with ≥6mo).

## Promotion bar (same as crypto scalp; nothing weaker)

A variant may be proposed for production **only if** it is net-positive (PF > 1) after
realistic spread+commission+slippage, **simultaneously in TRAIN, VALIDATION, and OOS**, on
**≥ 6 months**, ideally with 1m intrabar confirmation. Nothing less.

## Harness

A research-only skeleton is provided at `scripts/backtest_stocks_scalp_1m_5m.py`. It:
- defines the universe/variants/cost model,
- **refuses to emit a verdict** unless ≥ the minimum data window is present,
- is wired to read `data/raw/stocks/{1m,5m}/{SYMBOL}.csv` once such data exists.
It does **not** run a backtest today (no qualifying data) and does **not** touch production.

**PART 9 status: DONE — plan written; harness skeleton provided; full run blocked on
1m/5m data availability (no paid APIs). No production stocks scalp.**
