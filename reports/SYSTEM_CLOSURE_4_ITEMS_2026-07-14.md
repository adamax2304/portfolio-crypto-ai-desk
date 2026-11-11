# System closure: four audit items (2026-07-14)

## Scope and safety

- All changes are paper, shadow, display, read-model, telemetry, or scheduler wiring.
- Live, auto-live, and manual-live remain locked.
- No score, tier, entry, TP, SL, sizing, or strategy thresholds were loosened.
- The crypto cohort guard remains warning-only in production until two independent keys are enabled.

## 1. Regression failures and cohort routing safety

- The three full-suite failures were fixed by isolating tests from unrelated current overlay state.
- `cohort_guard.yaml` now has a genuine second routing key: `routing_enabled`.
- `mode: paper_review_only` alone cannot demote a candidate. Routing requires both the mode and
  `routing_enabled: true`; production currently keeps the second key false.
- Decisions and the overlay report expose the routing-key state for auditability.
- Focused tests cover warning-only behavior and explicit two-key activation.

Current production evidence remains insufficient: 0/30 narrow-target resolved forward trades.
The cohort guard therefore remains warning-only, as intended.

## 2. Stocks coverage and DATA_GAP_LATE

- Coverage is based on the latest relevant US cash session, including DST, weekends, and holidays.
- A complete closed RTH session can be clean; partial sessions and internal missing bars are dirty.
- Outside-RTH stock signals are classified as `SESSION_GAP`, not falsely as `DATA_GAP_LATE`.
- The operational DGL verdict uses actionable A/B stock signals; C-tier planning rows remain visible
  in totals but cannot block the lane.
- Cache-only coverage classification now runs after the current-cycle stocks report, so it evaluates
  the candles just fetched in that cycle.

Production refresh: 28 symbols, 112 symbol/mode series, 112 clean and 0 dirty. Current A/B stocks
intraday has 0 `DATA_GAP_LATE` rows. This fixes false data-quality rejection; it does not manufacture
trade opportunities or prove edge.

## 3. Independent latency acceptance

- Crypto and stocks intraday now have independent acceptance verdicts and sample requirements.
- Candle timestamps are treated as bar opens. Reports publish raw upper-bound latency and a
  conservative after-bar-close lower bound; raw bar-open latency is diagnostic, not an SLA verdict.
- Exact detect-to-alert dispatch latency and fast-source attribution are measured separately.
- A latency acceptance report is generated every scheduler cycle.
- The fast crypto `pending-monitor` is now a first-class background scheduler process with:
  - 45-second cadence;
  - pending crypto A/B scope only;
  - existing idempotent tracker and shared writer mutex;
  - its own PID lock plus the module's leader lock;
  - 130-minute lifetime, covering the scheduler's two-hour between-cycle gap.

The process was also started immediately on production paper. First tick: 24 crypto candidates
selected, 60/60 OHLCV pairs refreshed, 24 checked, no fetch errors. The monitor is alive with a
fresh crypto leader lock.

The persistent scheduler was restarted so its in-memory module includes the new step. The existing
autostart keeper replaced the stopped scheduler; a temporary manual duplicate was detected and
removed by exact PID. Final process audit shows one scheduler and one fast pending monitor.

Current 7-day acceptance is still honestly red:

- Crypto: `SLA_BREACH`; pre-deployment fast-source share is 0%. Raw detect p90 is 2199.9s, while the
  after-close lower bound is 146.1s and dispatch p90 is 15.9s. New forward transitions must establish
  the `pending-monitor` source share before this can pass.
- Stocks intraday: `SLA_BREACH`; actionable DGL is 0, but after-close lower-bound p90 is 8290.7s,
  fast-source share is 0%, sent sample is 2/5, and `yfinance` is explicitly not live-grade.

No latency report can unlock live automatically.

## 4. Lifecycle reconciliation

- Display status now prefers authoritative terminal Model F paper outcomes over ambiguous legacy
  statuses, while preserving legacy fallback when no paper outcome exists.
- Reports expose the display R source and whether paper execution was authoritative.
- The production lifecycle report now has:
  - `UNKNOWN_INCONSISTENT = 0`;
  - entered unresolved / expired-after-entry = 0;
  - 389 closed wins, 19 closed losses, and 135 closed flat rows in the current report window.
- The Windows report command now configures UTF-8 stdout, preventing a successful calculation from
  failing while printing Unicode status symbols.

This is display/reconciliation only. Historical source rows are not rewritten.

## Verification

- Full suite: **1516 passed** in 250.40s.
- Final focused lifecycle/scheduler suite: **57 passed**.
- Latency/pending/scheduler focused suite: **91 passed**.
- Scheduler dry-run: 63-step weekday plan; all CLI surfaces valid; no automatic Opus/Claude call.
- Live remains locked.

Production counts after refresh/deployment:

- `proposed_signals`: 3642 (unchanged from the pre-refresh snapshot).
- `paper_execution_outcomes`: 2950 (unchanged).
- `paper_shadow_execution_outcomes`: 2287 (unchanged).
- `signal_outcomes`: 1,077,530; `SUM(final_r)`: 1,310,552. These operational tracker fields moved
  while the persistent scheduler and the newly started paper pending tracker were running. That is
  expected paper lifecycle activity, not a schema migration or strategy rewrite.

## Strict conclusion

The four engineering/audit items are closed. The system is in a materially more trustworthy state
for continued paper/shadow evidence collection, but this is not proof that every strategy has edge
and it is not a live-readiness sign-off. The remaining work is evidence accumulation: fast-path
latency transitions, a live-grade stocks feed if low-latency stocks execution is required, and enough
resolved forward trades per strategy slice before promotion decisions.
