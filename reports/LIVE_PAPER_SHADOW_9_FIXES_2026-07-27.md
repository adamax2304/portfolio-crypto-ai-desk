# Live / Paper / Shadow: 9-Fix Verification

Date: 2026-07-27

## Safety State

- MEXC kill switch remains `TRIPPED`.
- Open MEXC canary positions: 0.
- Active MEXC risk, margin and notional: 0.
- No real order was submitted during this work.
- Paper strategy selection, scoring, targets and risk sizing were not changed.

## Implemented Fixes

1. Replaced the unreliable three combined MEXC TP/SL orders with one
   position-wide protective stop and three documented hedge-mode close-limit
   TP orders.
2. Model F now moves only the common protective stop. It never rewrites or
   duplicates the three take-profit orders.
3. Added dequeue-time expiry. A decision that waited too long is rejected
   before contract, book, account or order submission calls.
4. Added two-sided entry drift validation. A large nominally favorable move is
   also rejected because the frozen Paper setup no longer describes the live
   market.
5. Exit installation failures now persist the exception type, exact message,
   failed leg, created exchange order IDs and emergency-close result.
6. `mexc-canary-status` is now genuinely read-only: no DDL, migration,
   reconciliation or state repair is performed by a status request.
7. Crypto intraday alerts now record the authoritative executed entry mode
   separately from source and CQO classifier modes.
8. Close alerts inherit entry visibility. A shadow, late, failed or dry-run
   entry cannot later produce an actionable operator close alert.
9. Stocks pending execution runs independently from the slow full-universe
   report. Only one report task can run at once; RTH and forward-shadow read
   models refresh after it completes.

## Runtime Cleanup

- LA/USDT and ORDI/USDT stale queue rows were retained for audit and changed to
  `REJECTED_STALE_QUEUE`.
- Both had `attempt_count=0`; neither was sent to MEXC.
- The kill switch was not cleared by cleanup.
- MEXC and stocks monitor processes were restarted to load the new code.

## Verification

- Focused live, Paper alert, crypto intraday and stocks suites: 285 passed.
- Complete project suite after test isolation cleanup: 1805 passed.
- Two legacy stock test modules were changed to use temporary databases rather
  than writing test agent runs into the production SQLite database.
- Runtime MEXC heartbeat: OK.
- Runtime stocks log showed 1-minute pending OHLCV work proceeding while the
  full 15m/1h/1d universe report was still active.
- The stock provider emitted non-fatal Yahoo 404 messages for ETF fundamentals
  (SPY/QQQ/IWM and sector ETFs). Price bars continued to refresh and there was
  no monitor traceback or execution-lane failure.

## Residual Risk

The three-close-limit payload follows the documented MEXC contract order
schema and is covered by deterministic fakes, state reconciliation and
failure cleanup tests. It has not yet been accepted on a newly opened real
position after this change because the kill switch intentionally remained
tripped. The first future canary entry must therefore be treated as an
exchange-compatibility observation and watched until all three TP order IDs
and the single fallback stop are verified.
