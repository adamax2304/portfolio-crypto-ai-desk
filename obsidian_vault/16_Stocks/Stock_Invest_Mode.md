# Stock Invest Mode

Horizon: weeks to months.
Run: `python -m src.cli stocks-invest-report`

## Timeframes

- Execution: 1d
- Context: 1wk

## Priorities (scoring multipliers)

- `market_regime_alignment` ×1.10 — macro/regime dominates over months
- `sector_confirmation` ×0.90 — sector matters less; thesis-driven
- `technical_setup` ×0.85 — invest mode doesn't optimize on entry timing
- `earnings_risk_adjustment` ×0.60 — invest tolerates a single earnings event

## Hard rules

- Block only on the actual earnings event day (intraday volatility).
- Tolerate one earnings cycle; invest mode is multi-quarter by design.

## Required confirmations for A-tier

1. Daily and weekly trend agree.
2. Index direction agrees (or VIX is low — bear-market longs need leader RS).
3. Symbol's long-term thesis is documented (not just price action).
4. Fundamental snapshot (when wired in Stage 6+) supports the direction:
   - revenue growth, EPS growth, margin trajectory
   - reasonable valuation context for longs
   - clear deterioration signal for shorts

## What invest mode does NOT need

- VWAP, prev-day H/L, 15m structure — irrelevant at this horizon.
- News catalyst — long-term theses are catalyst-agnostic; news is a tie-breaker only.

## What's missing in the MVP

The `FundamentalSnapshotAgent` from the original module spec (revenue growth, EPS, margins, debt, valuation ratios) is **not** in the Stage 1–7 build. Invest mode currently relies on technicals + regime + sector alone. Add the fundamentals collector and agent when you decide to push real money via this mode.

## How to use this mode today

Treat invest output as a screening tool that finds long-term-leader-grade RS candidates in strong sectors and weak-trend-laggard candidates in weak sectors. Add fundamentals review manually before sizing into anything.
