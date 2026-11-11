# Context Filters Implementation Report

Date: 2026-07-16

## Scope

Seven independent context/risk additions were implemented without changing signal geometry,
targets, stops, Model F, A/B strategy logic, or live routing:

1. token-unlock long-risk context;
2. persistent multi-venue stablecoin depeg guard;
3. persistent Binance/Bybit execution-consistency guard;
4. stocks GEX regime overlay;
5. SEC Form 4 insider-cluster confirmation;
6. Catalyst RS next-session counterfactual;
7. crypto/stocks IV-RV context.

Live, auto-live and manual-live remain locked.

## Effective Routing

### Active in Production Paper

- Stablecoin depeg: USDT uses Coinbase, Kraken and Gemini; USDC uses Kraken and Gemini. A new
  crypto Paper entry is routed to Shadow only after a 1%+ depeg is confirmed on at least two
  direct-USD venues and persists for ten minutes. Missing/stale/one-venue data cannot block.
- Cross-exchange consistency: Binance and Bybit quotes are compared for the tracked universe.
  A divergence needs two recent samples inside 15 minutes. It can only reduce Paper to HALF_SIZE
  or SHADOW_ONLY; it never upgrades a signal.

Both guards affect new entries only. Existing positions are never closed or resized by them.

### Shadow / Advisory Only

- Token unlock: deterministic long-only risk classification is complete and point-in-time safe.
  Routing is disabled. The local import path works, but the production calendar currently has zero
  rows because DefiLlama unlock API access is not configured.
- Crypto IV-RV: Deribit DVOL for BTC/ETH plus 30-day realized volatility is active. IV Rank uses
  371 daily observations. It is diagnostic only.
- Stocks GEX/IV-RV: point-in-time JSON import, freshness, quality and positive-gamma/call-wall logic
  are complete. Routing is disabled and the import currently has zero rows because no licensed GEX
  feed/snapshot is configured.
- Insider cluster: 12 available SEC Form 4 quarterly datasets were imported. Only code-P open-market
  purchases are retained; 10b5-1 rows are excluded; routine vs opportunistic classification uses a
  three-year same-month history. It confirms Stocks Position candidates without changing score.
- Catalyst RS overnight: same-day execution remains authoritative. Close strength, VWAP, dual RS,
  Friday/event-risk and catalyst-validity determine eligibility; next-open/next-close USD PnL is
  stored separately and cannot affect official PnL or promotion verdict.

## Storage And Scheduling

- New provider snapshots and filter decisions live in `data/intelligence/market_intelligence.sqlite`,
  separate from the trading database.
- All tables use idempotent DDL and explicit INSERT column lists.
- Stablecoin/cross-exchange refresh runs before the tracker on a cold cycle and every five minutes in
  the derivatives monitor.
- Deribit/options context and the consolidated status report run every normal cycle.
- Token unlock and SEC Form 4 refresh run in long-horizon windows; Form 4 automatically falls back
  from an unpublished current quarter to the latest available quarter.
- Source health is recorded in the existing intelligence health table and included in Telegram/error
  monitoring. Optional unconfigured providers are marked disabled rather than counted as failures.

## Verification

- Full project: `1612 passed`, `0 failed`.
- Focused integration regression: `286 passed`, `0 failed`.
- Scheduler dry-run: complete; 75-step long-horizon weekday plan; no automatic LLM invocation.
- The resident 24-hour scheduler was restarted through its existing autostart wrapper; the new
  process completed `stablecoin + cross-exchange risk context` before `track-signals (pre)`.
- Real source smoke tests:
  - stablecoin direct-USD quotes: 5 fresh rows per poll;
  - Binance/Bybit tracked quotes: 88 symbols per venue poll set;
  - Deribit DVOL: BTC and ETH fresh;
  - SEC Form 4: 12 quarters downloaded, 99 deduplicated tracked-universe purchases stored.
- Catalyst RS refresh completed in its private Shadow table; evidence remains insufficient.
- New collectors do not write `proposed_signals`, `signal_outcomes`, `final_r`, Paper ledger, or live
  tables. Existing crypto point-in-time Paper snapshots remain additive read-model records.

## Current Limitations

- A reliable token-unlock schedule is not available from a documented free API. Production needs a
  DefiLlama/Tokenomist credential or curated `data/reference/token_unlocks.json` updates.
- GEX is model/provider dependent and needs a licensed point-in-time source or operator snapshots in
  `data/reference/stocks_options_context.json`. Stale or non-point-in-time data is rejected.
- No Shadow filter can auto-promote itself. Paper routing switches remain false until forward evidence
  and explicit operator review.

Operational status: `reports/CONTEXT_FILTERS_STATUS.md`.
