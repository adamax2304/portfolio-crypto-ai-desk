# Signal to Paper Universal Audit

Date: 2026-08-04

## Scope

This audit covers the common signal-to-Paper path for crypto scalp, intraday,
swing, stocks intraday, pre-open/RTH plans, and every Paper profile routed
through the shared tracker. It does not change strategy thresholds, scores,
stops, targets, sizing, risk policy, or live permissions.

## Authoritative path after the repair

1. A strategy registers a signal and its immutable Paper profile/mode.
2. The asset monitor records discovery and refreshes only the market-data
   timeframes required by that mode.
3. The deterministic strategy waits for its real entry condition. Candle-close,
   hold, reclaim, retest, or session waits are market/strategy time, not system
   latency.
4. Full and fast trackers serialize only the same signal_id. A slow sweep for
   one signal cannot block an unrelated fresh entry.
5. Paper actionability, quality overlay, and actual blocking guards evaluate the
   point-in-time candidate. Diagnostic-only risk scans are omitted from the
   latency-critical decision path.
6. The Paper alert and Telegram outbox row are staged atomically before network
   I/O. Lifecycle status is advanced only after durable staging.
7. Telegram is attempted once immediately. A network failure leaves a durable
   queued row for seconds-level retry and cannot erase the Paper entry.
8. Any separately permitted MEXC handoff consumes the durable Paper decision;
   it is not allowed to reconstruct an old decision from later data.

## What 47.7 minutes meant

The audited HFT/USDT intraday signal was created at 12:47:36 UTC. Its profile is
`crypto_intraday_level_hold_1bar_paper_v1`, with authoritative execution mode
`LEVEL_HOLD_1BAR`.

- The zone was first touched around 13:00 UTC.
- The required closed-bar hold was not complete until around 13:30 UTC.
- The first valid post-confirmation retest was around 13:35 UTC.
- Once that executable observation existed, the fast monitor saw it in the next
  cycle (about 17 seconds in the reconstructed timeline).

Therefore the displayed 47.7 minutes was primarily strategy maturation. Treating
it as technical latency would make the system enter before the configured
confirmation and silently change the strategy. Telemetry now reports strategy
wait and system delay separately.

## Real defects found and fixed

### 1. Wrong mode provenance

The crypto quality overlay could classify the HFT Paper signal as generic
`BREAKOUT_CONTINUATION` instead of its profile-owned `LEVEL_HOLD_1BAR` mode.
Paper profile and tracker mode are now validated together and stored in Paper
execution accounting.

### 2. Expensive decision path

Derivative context could scan millions of rows, and diagnostic risk scans ran in
the alert path. Composite latest-row indexes, bounded latest-value queries,
cached exchange metadata, and a latency-critical guard path reduced this work.

Observed query improvements included:

- BTC derivatives context: about 9569 ms to about 2.3 ms.
- HFT derivatives context: about 21.8 ms to about 1.7 ms.
- BTC liquidity context: about 456.8 ms to about 0.6 ms.

### 3. Global tracker contention

The old global writer lock could make a full sweep block every fresh signal.
Current full and fast passes use an atomic per-signal lock. The same lifecycle
cannot be mutated twice, while different signals proceed independently.

### 4. Long SQLite writer leases

Scheduled analytics wrote a row and then kept computing for tens of seconds or
minutes. This blocked both crypto and stocks Paper monitors. Compute and writes
were separated, and writes were converted to short committed batches in:

- news entity resolution and canonical events;
- catalyst labels;
- Paper execution, structural TP, structural stop, entry-mode and stock-direction models;
- entry-latency audit and Paper Shadow accounting;
- Paper portfolio ledger and crypto idea/quality read models;
- stocks pre-US actionability, RTH revalidation, coverage and post-trade diagnostics;
- Catalyst RS and stocks intraday variants Shadow read models.

### 5. Telegram could hold lifecycle progress

Network I/O no longer owns the Paper transition. The alert is staged first,
Telegram is attempted outside the authoritative lifecycle decision, and failed
sends are retried from a claimed outbox row with bounded backoff.

### 6. Worker reliability and duplicate work

- Windows worker recycling no longer uses the failing `os.execv` path.
- PID files contain the actual worker PID.
- Leader leases keep one active crypto monitor and one active stocks monitor.
- The legacy five-minute watchlist monitor skips pending-entry tracking while
  the dedicated 15-second worker is healthy.
- Crypto refresh is mode-specific: intraday uses 1m/15m, swing uses 5m/1h,
  and scalp uses 5m as required by the existing tracker.

### 7. Misleading latency accounting

Additive telemetry now records:

- signal discovery;
- strategy-ready time;
- ready-to-detect system delay;
- Paper decision runtime;
- alert queued/sent state;
- market-data timestamp and point-in-time provenance.

Historical/backfilled/reconstructed observations are not allowed to prove the
new forward SLA.

## Real runtime verification

- Warm crypto fast cycles: generally 13-15 seconds total for 25 selected
  signals, including provider fetch and Paper tracking.
- Cold/recycled cycle observed: about 23 seconds.
- Paper decision runtime in the accepted sample: p50 12.7 ms, p90 15.5 ms.
- Crypto intraday ready-to-detect sample: 0.3 seconds for the one currently
  usable observation. This sample is not yet statistically sufficient.
- A real 24-hour entity-resolver pass processed 3202 news rows in 63 seconds
  while the fast monitor completed every cycle with 25 checked signals and no
  new SQLite lock failure.
- A real canonical-event pass processed 3201 rows / 2563 clusters with no new
  SQLite lock failure.
- The current monitor audit shows fresh crypto, stocks, and MEXC leader leases.

## Tests

- Final broad Signal-to-Paper regression: 376 passed.
- Focused stocks transaction/Shadow/pre-open regression: 98 passed.
- News resolver/canonical regression: 67 passed.
- Python compilation passed for all changed modules.

These sets overlap; the counts must not be added as unique tests.

## Integrity and safety

- Strategy thresholds, guard thresholds, score, stop, TP, and sizing were not
  relaxed.
- No historical signal was retroactively announced as a new Paper entry.
- No repair writes to `final_r` or changes legacy outcomes to manufacture edge.
- Latest observed database counts (background workers remain active):
  `proposed_signals=4627`, `signal_outcomes=2038659`,
  `SUM(final_r)=1743160.0`, `signal_alerts=3344`,
  `paper_execution_outcomes=3980`.

## Honest remaining limits

Literal zero latency is not achievable with polled providers and closed-candle
strategies. The meaningful target is: act in the first fast cycle after the
entry becomes executable, without database or network serialization.

- Crypto operational target: normally within one 15-second cycle; a cold
  worker/provider cycle can be around 20-25 seconds.
- Stocks operational target: within the one-minute monitor/provider cycle.
- A 15-minute hold, one-hour close, pre-market session boundary, or retest wait
  remains intentional strategy time and must not be removed to improve an SLA.
- The post-deployment forward sample is still too small to declare a statistically
  proven latency SLA or live-grade execution parity. The old broad SLA report
  remains red because it correctly retains legacy delayed rows separately.

## Verdict

The universal Signal-to-Paper path is repaired and running. The known technical
causes of multi-minute delay (global locking, long analytics transactions,
unbounded queries, synchronous notification ownership, and worker recycle
failure) have been removed. Paper testing can continue. Promotion or wider live
routing still requires fresh forward observations rather than the repaired
historical sample.
