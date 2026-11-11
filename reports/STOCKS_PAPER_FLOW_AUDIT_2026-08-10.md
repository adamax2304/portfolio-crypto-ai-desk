# Stocks Paper Flow Audit - 2026-08-10

## Scope and safety

- Stocks remain Paper-only. No stock live routing was enabled or widened.
- Existing premarket C-tier planning, legal/headline gates, SI1-SI5, ATR caps,
  and one-minute execution tracking remain in place.
- The goal of this pass was to remove technical losses of valid candidates,
  not to manufacture daily trades by lowering edge filters.

## Implemented fixes

### 1. Delayed-provider bars can be used after explicit price revalidation

`provider_delayed_current_bar` is accepted by Stocks Paper accounting and
entry notification only when `current_price_revalidated=1` and the dedicated
stocks config flag is enabled. Point-in-time evidence remains preferred, and
the delayed cohort keeps its own provenance label for later analysis.

Production materialization after refresh:

- 38 delayed-provider rows with current-price revalidation;
- 38 are now `execution_validity=valid`;
- no delayed row was silently relabeled as point-in-time.

### 2. Pre-open plans no longer suppress the RTH executable decision

- Only a genuine market-closed planning cap can register a C-tier pre-open
  plan. Legal-only or unrelated C-tier rows cannot enter through this route.
- Deduplication now separates the pre-open planning slot from the later RTH
  A/B executable slot.
- Breakout and Pullback profiles reuse the already computed stock decision,
  avoiding a second inconsistent pipeline run.

### 3. The fast monitor now serves every Stocks Paper profile

- Breakout, Pullback, and Catalyst RS registration run from the same fresh
  decision callback.
- Registration happens before slow Markdown report rendering.
- Catalyst RS is no longer limited by the old two-hour adapter cadence while
  its confirmation validity lasts only 30 minutes.
- Profile failures are isolated and reported instead of aborting the whole
  stock cycle.

### 4. Closed-bar freshness is correct

- An incomplete current 15-minute bar is excluded from RVOL and gate context.
- Data age is measured from the bar close, not from the bar open.
- The 900-second freshness threshold was not loosened; the false 15-minute
  penalty was removed instead.
- Diagnostics now expose the last closed bar and its actual age.

### 5. MEXC Stocks Paper lifecycle is race-safe

- One leader lease serializes the capacity-check and order-write transaction.
- Duplicate active orders per ticker/session are reconciled without deleting
  history; surplus unfilled rows become auditable `INVALIDATED` rows.
- A filled order cannot be demoted by a later repeated rejection/upsert.
- If a legacy position exists while its order is not `FILLED`, the order is
  restored automatically from the position.

Production state after repair:

- active ticker/session duplicates: 0;
- position/order lifecycle mismatches: 0;
- current positions include open CRM and BX; the latest BKNG trade closed at
  its original stop and remains linked to a `FILLED` order.

### 6. Monitor load and provider boundary fixes

- One-minute pending/order/position tracking remains unchanged.
- The full 104-symbol report/data rebuild runs every 15 minutes instead of
  keeping the worker almost permanently busy at a five-minute cadence.
- The fast RTH rebuild fetches only 15-minute data; normal scheduler cycles
  maintain cached 1-hour, daily, index, sector, and earnings context.
- Yahoo's one-hour request was reduced from 730 to 729 days to remain inside
  its real rolling boundary.

## Audit findings

### Overnight expiry

The historical `invalid_stock_intraday_overnight_event` rows were not near
misses. Their first observed outcome was at least 17.5 hours after expiry,
consistent with next-session data. Adding a small grace period would not
recover them and would only weaken lifecycle semantics, so no grace was added.

### Market context and RVOL

The principal false-stale cause was bar-open versus bar-close age and is fixed.
SPY/QQQ unknown or genuinely stale context remains conservative. Exploratory
evidence did not justify lowering RVOL thresholds globally.

### Current evidence

- MEXC Stocks Paper settled USD ledger before the latest still-open/just-closed
  trades: 4 closed trades, net +$36.75, PF 1.54, win rate 50%.
- This is operational evidence, not enough trades to claim a durable edge.
- Catalyst RS: 17 clean closed forward trades, net -$85.86, PF 0.66,
  win rate 29.4%, verdict `INSUFFICIENT_CLEAN_SAMPLE`.
- Therefore Catalyst RS must continue as evidence collection; higher signal
  throughput must not be described as proof of profitability.

## Production verification

- Pre-US health: `OK`, 20 actionable / 20 processed.
- Stock monitor: alive after restart, one-minute tracking and 15-minute report
  refresh, heartbeat `problems=[]`.
- Scheduler dry-run: 94 steps, every stocks CLI surface valid, no automatic
  LLM invocation.
- Test suite: 527 passed.
- Python compilation of all touched runtime modules: passed.

## Readiness conclusion

The stock flow is now operational end-to-end: overnight candidates are kept,
pre-US actionability is materialized, RTH decisions can replace planning rows,
profiles are registered promptly, and Paper orders/positions are tracked every
minute without duplicate or terminal-state corruption.

The system can now produce trades when setups qualify, but it must not promise
a trade every day. Forcing frequency by removing legal, freshness, market
context, or structural-entry checks would make the sample larger and less
trustworthy. The next decision should be evidence-driven: accumulate at least
30 clean closed forward trades per profile and judge net USD PnL, costs, PF,
drawdown, and rejection distribution separately for Breakout, Pullback, and
Catalyst RS.

## Same-day operational follow-up

- Three Stocks Paper positions filled today: CRM, BKNG, and BX. BKNG later
  closed at its original stop; CRM and BX were still open at the final check.
- No additional order filled after the 14:05 UTC monitor restart. The pipeline
  continued to evaluate candidates: AAPL, MU, DDOG, APP, GE, COST, and WMT were
  fresh RTH decisions, but their pre-gate scores were only 55-64 and they had
  no additional cap reasons. They were weak technical candidates, not lost or
  blocked by data/news infrastructure.
- The realtime Telegram collector had stopped on August 1 despite an existing
  logon task. The heartbeat now supervises and restarts that scheduled task.
  It is connected and listening to 30 channels; the task's own loop retries a
  disconnected collector after 20 seconds.
- GlobeNewswire's obsolete feed URL was replaced with the current official
  Public Companies RSS endpoint. A live refresh returned 10 items.
- Reputable-headline entity resolution was completed for Apple, Nike, and AMD
  while preserving the Apple common-noun false-positive guard.
- Benzinga remains enabled in the normal redundant RSS set but was removed from
  the two-minute fast set because repeated seven-second timeouts delayed every
  fast cycle. Fast refresh latency fell from 21.7 seconds to 6.5 seconds.
- Final news gate: READY, 31/31 gold cases, 0 blocking mapping gaps, 0 stale and
  0 dead sources. The remaining Benzinga transport error is non-primary and
  non-blocking.
- Final combined stocks/news regression: 613 passed.
