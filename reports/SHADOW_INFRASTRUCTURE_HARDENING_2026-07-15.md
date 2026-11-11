# Shadow Infrastructure Hardening - 2026-07-15

## Scope

Three approved changes were applied to shadow/read-model and monitor infrastructure only. Paper
entry policy, strategy scoring, risk sizing, actionability, live controls, `proposed_signals`,
`signal_outcomes`, and `final_r` were not changed by these changes.

## 1. Disk/cache integrity for the crypto pending monitor

- `FileStore.save_ohlcv()` now writes a temporary CSV, flushes it, and atomically replaces the
  prior cache only after a successful non-empty write. An `ENOSPC` or interrupted write therefore
  leaves the last known-good OHLCV file intact.
- Empty OHLCV DataFrames are rejected before a cache replacement. Empty or malformed existing CSVs
  load as unavailable data rather than raising `EmptyDataError` through the whole tracker.
- `pending-monitor` now reports disk state. Below 5 GB it logs one warning per monitor run; below
  1 GB it skips refresh and tracking for that tick, records `market_data_refresh_skipped`, and does
  not act on a potentially stale or partial cache.
- At application time the workspace had about 75 GB free, so the normal monitor is in the healthy
  state. The critical path is covered by a hermetic test, not forced against production storage.

## 2. Scheduler heartbeat correctness

- The end-of-cycle heartbeat now reports the actual monitor lifetime: 90 minutes for the broad
  crypto monitor and 180 minutes for pending, derivatives, and stocks monitors under the current
  schedule. It no longer describes every background process as a 90-minute process.
- The active scheduler was restarted through its existing `autostart_scheduler.bat` restart loop.
  The fresh process started at `2026-07-15T02:34:18+03:00` and validates the new CLI surface.

## 3. Separate stocks-intraday forward evaluator

- Added `stocks-intraday-forward-shadow-evaluate` and the additive
  `stocks_intraday_forward_shadow_evaluations` table.
- It evaluates only the dedicated `stocks_intraday_forward` / `new_logic_shadow` lane, only
  `PULLBACK_LIMIT` and `BREAKOUT_CONTINUATION`, only the authoritative stock fee profile, and only
  clean closed `forward_since_activation` outcomes for edge metrics.
- Historical backfill, dirty/no-coverage rows, stale cost-model rows, and legacy stocks
  swing/invest evidence are excluded. `legacy_evidence_reused=False` is stored explicitly.
- It is scheduled immediately after the cache-only stock coverage gate, so its clean/dirty marks
  are current in the same cycle. Its strongest verdict is `REVIEW_ONLY`: it never promotes a mode,
  changes paper routing, or affects live.

## Current evidence

The initial real-DB evaluation is deliberately inconclusive:

| entry mode | clean closed | dirty closed | clean net USD | verdict |
|---|---:|---:|---:|---|
| PULLBACK_LIMIT | 2 | 1 | 17.87 | INSUFFICIENT_CLEAN_SAMPLE |
| BREAKOUT_CONTINUATION | 1 | 0 | 20.40 | INSUFFICIENT_CLEAN_SAMPLE |

The lane was activated on `2026-07-13T08:21:22+00:00`; it has only about 1.6 forward days and
requires 30 clean closed trades plus 28 forward days. These figures are diagnostics, not an edge
claim and not a promotion trigger.

## Verification

- YAML parse and Python compilation: passed.
- Targeted shadow, stocks coverage, evaluator, scheduler, pending-monitor, and cache integrity
  regression suite: `216 passed`.
- Scheduler dry-run: all CLI surface checks passed, including the new evaluator; no automatic LLM
  command was introduced.
- Real evaluator run: wrote only the additive evaluator table, JSON, and
  `STOCKS_INTRADAY_FORWARD_SHADOW_EVALUATION.md`; shadow outcome count remained unchanged during
  that run.

## Operational note

The first fresh scheduler cycle's `crypto scalp report` completed successfully but took 460.7
seconds. That pre-existing report-generation cost does not block the independent fast pending
monitor, but it should be profiled separately if long full-cycle duration becomes recurrent.
