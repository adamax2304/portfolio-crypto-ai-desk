# Stocks Pre-open to Paper Chain Fix

Date: 2026-07-30

## Root causes

1. After-hours stock plans could receive the already-finished US cash close as
   their expiry.
2. The pending monitor selected current A/B signals, but not a C row restored
   to effective A/B by the pre-US review.
3. RTH revalidation required a separate new signal id. The stock report can
   update a stable signal id in place, so a real post-open recomputation was
   missed.
4. A historical terminal status caused by the bad expiry was not recoverable.

## Implemented

- Added a holiday/weekend-aware target cash session for premarket and
  after-hours stock plans.
- Tracker, Paper accounting, and Shadow simulation now use that target session.
  A configured expiry earlier than signal creation is treated as invalid.
- Added materialized `stocks_preus_actionability`. It requires:
  - immutable pre-gate A/B evidence;
  - only the market-session cap on the source plan;
  - a fresh non-blocking review with effective A/B tier;
  - valid geometry and no current hard/substantive gate.
- Added one-time lifecycle recovery for rows proven to have the impossible old
  expiry. It never changes score, tier, entry, stop, targets, accounting, or
  live routing.
- Added reviewed actionability ids to the existing one-minute pending tracker.
- RTH revalidation now accepts a post-open `updated_at` on the same signal id
  and compares it to the immutable pre-open snapshot.
- Added `stocks-preus-actionability-refresh` for explicit diagnostics.
- Restarted the long-running stocks monitor so the new code is active.

## Production verification

- Current actionable reviewed plans: 4.
- Effective review tiers:
  - AVGO: A
  - IWM: A
  - JPM: A
  - NFLX: B
- AVGO, IWM, and NFLX are being checked from current 1-minute bars by the
  ordinary Paper tracker.
- JPM reached the tracker and was explicitly rejected by the existing disabled
  `LIMIT_THEN_TAKER_TIMEOUT` policy. It was not lost in the handoff.
- Active worker: stocks monitor PID 23800, one-minute cadence.

## Verification

- Focused chain and execution tests: 132 passed.
- Stocks package tests: 184 passed.
- Top-level stocks tests: 255 passed.
- Notifier, schedule, and Paper policy tests: 141 passed, 5 skipped.
- Final changed-path regression: 117 passed.
- Scheduler dry-run: complete; all validated CLI commands OK.
- Full repository suite exceeded the five-minute command timeout; no result was
  claimed from that interrupted run.

The source C tier remains unchanged for auditability. Paper permission is a
separate bounded record, so review cannot silently rewrite historical evidence.
