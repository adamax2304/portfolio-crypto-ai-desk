# Stocks Active Trading Hardening - 2026-08-19

## Scope

This pass covers only active stock trading:

- Pre-US news continuation;
- production `BREAKOUT_CONTINUATION`;
- production `PULLBACK_LIMIT`;
- their price, news, LLM, Paper and small-live execution envelope.

Invest, position and other long-horizon research modes are out of scope and were not promoted.

## Implemented mechanics

### Pre-US

1. Outside-RTH stock ideas remain plans, not fills.
2. The pre-US candidate builder separates eligible candidates from deterministic exclusions.
3. The 08:55 ET Opus review may return only `SUPPORT`, `NEUTRAL`, `CAUTION`, `BLOCK` or `INSUFFICIENT_DATA` plus evidence. It cannot set a price, tier or order.
4. Code clamps any proposed score adjustment, rechecks hard blocks and recomputes the tier through the shared tier policy.
5. Entry still requires the deterministic Paper trigger and a fresh current-price revalidation.
6. The small live canary accepts only long `BREAKOUT_CONTINUATION`, score >=70, at approximately $5 stop risk.

### Production breakout

1. A closed 15-minute bar must confirm the structural break and VWAP condition.
2. Market/sector/RVOL context must confirm a catalyst-free technical setup.
3. The Paper sample remains unchanged; the small live canary separately requires score >=70.
4. Long and short are allowed only after the same point-in-time revalidation and exchange-native preflight.

### Production pullback

1. Price must touch the pullback zone and then close a 15-minute bar holding VWAP/structure.
2. Paper collection remains enabled.
3. Live promotion remains disabled. The clean forward production-direction slice is currently negative and is not rescued by the positive experimental direction-flip slice.

## Evidence corrected

Repeated scans could create several signal ids for one economic setup. The forward evaluator and candidate simulator now deduplicate by `economic_trade_key` and keep the earliest point-in-time observation. Reports expose `duplicate_rows_excluded`.

Corrected forward evidence:

| Mode | Clean closed | Net USD | PF | Important qualification |
|---|---:|---:|---:|---|
| Pre-US | 22 | +518.21 | 2.37 | Seven sessions, all long, underpowered |
| Breakout | 6 | +68.39 | 3.61 | Only three unchanged-direction closes; underpowered |
| Pullback | 15 | +35.15 | 1.24 | Unchanged production direction: -62.57 USD, PF 0.57 |

Pre-US remains positive after removing its best session (+231.40 USD), but five symbols generated 75% of positive profit. The score >=70 in-sample slice had 20 closes, +590.89 USD and PF 2.93. This is sufficient for a small canary threshold, not for scaling or a profitability claim.

## News and LLM envelope

- News health after remediation: 42 active sources OK, 0 stale, 0 dead, 0 transport errors; 21 sources are explicitly disabled rather than silently failing.
- Finnhub company news, SEC EDGAR, PR Newswire, Business Wire, RSS and Telegram all feed the canonical news store.
- A revoked Telethon session no longer kills Telegram coverage: public `t.me/s/<channel>` polling runs every 120 seconds through the same normalization, timestamp and entity-resolution path.
- `published_at`, `ingested_at` and `available_at` are kept separately. Decisions use what was available to the system at decision time.
- Entity health after the fallback catch-up was 100% for the inspected 24-hour window.
- The Pre-US LLM task is checked against the current NY session. When overnight plans exist and the session review is missing after the expected window, watchdog raises an explicit problem.
- The LLM is a conservative risk/scoring overlay, not an entry generator. Current closed results do not prove incremental LLM PnL: most profit is in `NEUTRAL`, while `CAUTION` is near flat.

No additional news vendor is required for the current canary. The main remaining market-data limitation is OHLCV: Finnhub supplies fast quotes/news but this account has no candle entitlement, so yfinance remains the 15-minute fallback. Paper revalidates against a fresh Finnhub quote. Scaling stock live beyond a small canary should wait for a true live-grade US OHLCV feed.

## Live execution hardening

- The stock bridge now freezes explicit venue symbols: MEXC `TICKERSTOCK_USDT`, Bybit `TICKERUSDT`.
- MEXC-specific contract blocks no longer block an otherwise valid Bybit route.
- MEXC and Bybit private preflight both passed; the worker is armed for both venues.
- Venue preflights run in parallel and one venue is selected by executable cost/latency. The decision is never split across exchanges.
- The standard and Pre-US bridges share a source-signal dedupe check, preventing one Paper fill from being queued twice through two lanes.
- Score >=70 is a live-only quality floor. It does not remove lower-score rows from Paper evidence.
- Native rounding, stop geometry, risk, liquidation buffer and protective-order checks remain fail-closed. They were not weakened to increase frequency.
- Worker heartbeat now records its actual `armed_venues`, so status is accurate even when the diagnostic shell itself does not inherit exchange credentials.

## Operational verification

- Targeted regression: 455 passed, 5 skipped.
- Additional worker/status regression after heartbeat observability change: 31 passed.
- Scheduler dry-run: 12 cycles, 99 steps in cycle 1 and 81 in later cycles; all CLI checks passed; no automatic LLM invocation leaked into the deterministic scheduler.
- Watchdog: scheduler, pending monitor, stock monitor, Telegram collector and live monitor healthy; no current problems.
- News source health: OK 42, STALE 0, DEAD 0, transport errors 0.
- Live worker heartbeat: `OK`, both `mexc` and `bybit` armed, kill switch clear.

## Strict deployment decision

1. **Pre-US:** keep Paper fully active and continue the existing approximately $5-risk live canary at score >=70. Do not scale before at least 30 clean closed forward trades and more independent sessions/short evidence.
2. **Breakout:** keep Paper active and allow only the existing approximately $5-risk live canary at score >=70. Six clean closes are promising but not proof.
3. **Pullback:** keep Paper active, do not send to live yet. Require at least 30 clean closes and PF >=1.25 in the unchanged production-direction slice, not pooled with experimental direction flips.
4. Do not tune or promote the raw 499-trade technical control: it is negative after costs (PF 0.85).
5. Keep thresholds frozen while the next forward sample accumulates. The next decision must use net USD PnL, PF, drawdown, concentration and venue-realistic costs, not win rate alone.

## Expected effect

The changes should improve trust and execution quality more than raw trade count. Duplicate evidence is removed, live receives only the stronger score slice, Telegram failures no longer create a silent news gap, missed Pre-US LLM runs become visible, and stock orders can use the actually available/better of MEXC and Bybit. Paper remains broad enough to learn whether lower-score setups or pullbacks improve; live remains deliberately narrower until the production-direction evidence is positive.
