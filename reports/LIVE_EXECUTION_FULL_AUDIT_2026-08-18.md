# Live Execution Full Audit - 2026-08-18

## Scope

Audited the complete point-in-time path from a Production Paper entry through
the MEXC live outbox, contract/book/account preflight, fixed-USD-risk sizing,
order submission, partial TP/protective-stop installation, reconciliation,
watchdog, and process recovery. Crypto swing, crypto intraday, crypto invest,
and stock intraday routes were included. Strategy scoring and Paper economics
were not changed.

## Material findings and fixes

1. The crypto pending monitor was disappearing after its ten-tick Windows
   self-recycle. Self-recycle is disabled; the worker now runs continuously.
2. A warm pending-monitor cycle took about 24 seconds because swing diagnostic
   5m bars were fetched every tick. Swing-only 5m probes are now cached until
   the next closed 5m bucket. Scalp 5m and intraday 1m remain fast. The observed
   warm cycle fell to 14.2 seconds while all required pairs succeeded.
3. Live decision capture could wait 30 seconds on the general SQLite writer.
   The live outbox now uses a bounded five-second connection and retries the
   idempotent loop instead of making an entry stale.
4. The MEXC worker created fresh HTTP sessions repeatedly and its persistent
   reconciliation client did not receive configured safe-read retries. One
   persistent configured client is now reused; burst workers retain isolated
   sessions to avoid sharing a Session across threads.
5. MEXC safe-read timeout is now four seconds, with safe GET retries. Order
   POST remains exactly-once and is never blindly retried.
6. A formally alive but stalled MEXC or pending monitor could not be recovered:
   the starter refused to duplicate it. The watchdog now verifies the exact
   command line, stops only that monitor, preserves its old lease as an audit
   artifact, and starts a replacement. Unrelated Python processes cannot match.
7. The stock live bridge depended on a later one-minute poll. A valid Paper
   stock entry could close or age out before the poll. The Paper notifier now
   freezes the exact versioned stock entry into the live outbox before Telegram
   network I/O. The poll remains an idempotent recovery path.
8. Stock and fast workers can be started by Windows without inherited MEXC arm
   variables. Their launchers now restore only the named user-scoped MEXC
   credential/arm environment, without logging values.
9. A parsed MEXC business rejection was incorrectly treated as an unknown
   submission. This tripped the kill switch for AVGOSTOCK even though MEXC
   explicitly said no opening order was accepted. Parsed business rejects are
   now `REJECTED_SUBMISSION`, release reserved risk, emit a warning, and do not
   trip the kill switch. Transport/non-JSON/malformed-success responses remain
   critical `SUBMISSION_UNKNOWN` events.
10. The historical AVGOSTOCK unknown row was reclassified and its reservation
    released. AVGOSTOCK is now blocked in the stock live bridge because MEXC
    explicitly disallows opening that contract in the current region.
11. Duplicate stock handoffs now render an explicit idempotency message rather
    than looking like a missing live result.
12. Two unrelated stale tests were corrected without changing production:
    one news fixture used an expired absolute date, and one invariant still
    expected the retired hard Asia intraday block.

## Real-system verification

- MEXC read probe: 12/12 successful.
- Median reads: contract 390 ms, depth 361 ms, account 363 ms, positions 379 ms.
- Warm crypto fast tick: 14.2 s, 45 signals checked, 24/24 required pairs
  refreshed, zero fetch failures.
- Live DB invariants: zero eligible decisions without outbox, zero submitted
  outbox rows without orders, zero filled orders without positions, zero open
  positions without open risk, zero closed positions with open risk, zero stale
  PROCESSING rows, zero ready queued rows, and zero duplicate signal decisions.
- Current live state at close of audit: armed, submission enabled, kill switch
  CLEAR, queue 0, heartbeat OK, reconciliation OK.
- Current INTCSTOCK short: open and reconciled; stop at breakeven, two native
  close-limit TPs plus monitored TP3, all three local exit legs ACTIVE. Local
  actual stop risk is about USD 3.50.

## Tests

- Final full repository run: 2240 passed, 5 skipped, 0 failed.
- Live/stock/notifier/latency regression after the submission-rejection and
  symbol-block refinements: 160 passed, 0 failed.
- Earlier focused suites: 299 live/Paper/latency tests, 204 tests/stocks tests,
  and 280 top-level stock tests all passed.

## Expected rejections that remain

- A MEXC contract can be unavailable, region-restricted, too coarse for a USD
  risk budget, or geometrically detached from its underlying stock. Such a
  candidate must be rejected; loosening this would create a different trade.
- GESTOCK produced `MEXC_NATIVE_GEOMETRY_INVALID`. This is a valid safety reject,
  not a delivery delay. The underlying signal and MEXC contract quote did not
  preserve executable entry/stop/target geometry.
- Real adverse price drift, excessive spread, missing contract, invalid stop or
  liquidation geometry, duplicate same-symbol bot exposure, the USD 50 bot-risk
  cap, and a genuinely unknown order POST remain blocking conditions.
- An external MEXC outage cannot be eliminated locally. The corrected path now
  retries safe reads inside the entry window, preserves exactly-once POST
  semantics, alerts on failures, and self-recovers dead/stalled monitors.

## Operational processes at close

- crypto pending monitor: active, configuration cadence 15 seconds
- stocks monitor: active, one-minute entry observation
- MEXC monitor: active, three-second reconciliation loop
- default scheduler and watchlist monitor: active
