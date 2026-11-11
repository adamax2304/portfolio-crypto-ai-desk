# Stocks Paper Expansion - 2026-08-07

## Scope

Stocks and crypto Paper strategies are now indexed separately. Existing
authoritative configs were not moved or duplicated. Stock live routing remains
disabled.

## Implemented

1. Added navigation registries under `config/paper/crypto`,
   `config/paper/stocks`, and `config/shadow/stocks`. Validation report:
   `reports/PAPER_STRATEGY_REGISTRY.md`.
2. Expanded the shared stock universe from 28 symbols to 104 inputs: 91 liquid
   trade symbols plus market/sector benchmarks. All 91 trade symbols have an
   active, API-allowed MEXC stock-futures contract in the current catalog.
3. Kept market-data roles honest: Finnhub is used for fast company news and
   point-in-time quote revalidation; yfinance supplies structural 15m/daily
   bars because the installed Finnhub entitlement rejects candle requests.
   Polygon/Alpaca remain optional and disabled without credentials.
4. Hardened news quality. A failed redundant source is now a warning, while a
   failed primary source still blocks the trust claim. Expanded issuer aliases,
   treated untracked cashtags outside the configured universe as a review queue,
   and excluded opinion headlines from false blocking gaps.
5. Activated three isolated stock Paper profiles:
   - `stocks_intraday_pullback_vwap_paper_v1` / `PULLBACK_LIMIT`
   - `stocks_intraday_breakout_1bar_paper_v1` / `BREAKOUT_CONTINUATION`
   - `stocks_catalyst_rs_paper_v1` / `CATALYST_RS_CONTINUATION`
6. Added the separate `stocks_earnings_gap_continuation_v1` Shadow lane. Earnings
   remain excluded from Catalyst RS, so the two evidence sets cannot mix. The
   Position Swing V2 minimum observation period is now 90 forward days instead
   of an unsuitable 28 days for a 5-40-session holding strategy.

## Integrity fixes discovered during implementation

- Versioned stock profiles previously shared the legacy daily `signal_id`.
  Pullback could therefore collide with Breakout on the same symbol/day. The
  optional profile identity is now included only for versioned Paper lanes;
  ordinary legacy signal IDs remain unchanged.
- Pullback initially saw a not-yet-closed 15m bar in its resolver. The resolver
  now truncates candles to `bar_close <= now`, preventing lookahead.
- After-hours Pullback plans now roll to the next target RTH session. They no
  longer search yesterday's session or get stranded before the morning review.
- Benchmark ETFs are available to context agents but are excluded from the
  default Paper candidate list.
- Tracker routing now dispatches each tagged stock signal to exactly one profile
  resolver and revalidates the confirmed price with a fresh Finnhub quote. A
  delayed yfinance bar can therefore describe structure but cannot create a
  synthetic current fill.

## Current production state

- News Quality Gate: READY, 31/31 gold cases, 100% policy coverage, resolver p95
  31.594 seconds, zero blocking mapping gaps.
- One redundant RSS source is in ERROR; zero primary ERROR/DEAD sources.
- Current stock Paper plans: Breakout 12, Pullback 14. These are plans awaiting
  their own RTH confirmation, not claimed fills.
- Catalyst RS Paper: enabled, but zero fresh clean confirmations existed at the
  activation run. Historical Shadow winners were not replayed into Paper.
- Earnings-gap Shadow: 154 historical observations materialized; forward clean
  closed sample is still zero, so verdict is `INSUFFICIENT_CLEAN_SAMPLE`.
- Stock live routing: disabled. No stock profile can route to the crypto MEXC
  live canary.

## Verification

- Stocks/news regression: 620 passed.
- Paper/tracker regression: 96 passed.
- Scheduler dry-run: 94 steps; all old and new CLI surfaces valid; no automatic
  LLM invocation.
- Real DB activation: `proposed_signals` 4814 -> 4840, exactly 26 new isolated
  stock Paper plans. `paper_portfolio_ledger` stayed 3776. Background tracker
  continued updating `signal_outcomes`; the new activation code does not write
  that table directly.

## Expected impact and limits

The wider universe should materially increase candidate flow, while separate
profile identities preserve honest per-strategy PnL and rejection statistics.
Fresh quote revalidation prevents delayed bars from being counted as fills.
This does not prove profitability: Pullback and Catalyst RS are deliberately in
Paper to collect forward evidence at real execution time. Current yfinance
entry-detection p90 remains about 709 seconds, so stock live promotion is still
blocked until a candle-capable real-time provider is available or the measured
latency improves.
