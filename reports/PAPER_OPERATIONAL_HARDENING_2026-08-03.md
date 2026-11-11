# Paper Operational Hardening - 2026-08-03

## Scope

This pass implemented the agreed operational plan without changing strategy
scores, tiers, entry geometry, stops, targets, Model F, or live eligibility.
No manual exchange order was submitted during verification.

## Implemented

1. Added one authoritative Paper audit across crypto, stocks, Shadow routing,
   MEXC handoff, news quality, latency, and forward evidence. Closed-trade PnL
   comes from the active fee-profile ledger in net USD; fees, slippage, and
   funding remain separate.
2. Added explicit warnings for weak samples, PnL concentration, weak PF,
   unresolved stocks plans, news readiness, MEXC unknown submissions, and SLA
   breaches. Reports cannot promote a lane automatically.
3. Corrected latency measurement to detection -> immutable MEXC capture. The
   old Paper/Telegram label is retained only as a compatibility alias. Forward
   acceptance starts after the fast-alert activation timestamp, so historical
   2 x 15 second Telegram timeouts do not judge the new path.
4. Added a bounded Telegram entry-alert fast path: one short attempt on the
   critical route, then durable outbox recovery. MEXC decision capture happens
   before Telegram and cannot be delayed by Telegram retries.
5. Hardened tracker locking. A fresh lock owned by a dead PID is reclaimable;
   a live owner remains protected. Full and fast tracker passes still serialize
   through the same writer lock, so duplicate lifecycle transitions remain
   blocked.
6. Hardened the crypto pending monitor: 30 second fixed-rate cadence, bounded
   concurrency, 72/72 required timeframe refresh in the observed production
   ticks, stale-data exclusion, closed exchange HTTP sessions, and bounded
   worker-memory rotation after a completed tick. Fast-path SQLite contention
   now has a one-second busy budget and retries on the next normal tick instead
   of waiting behind repeated 30-second database timeouts.
7. Added/extended crypto counterfactual evidence and MEXC parity diagnostics.
   The data remains forward-only and cannot change production decisions.
8. Hardened the stocks pre-open/RTH chain with append-only observations,
   explicit terminal states, fresh candidate rebuilding, and no silent reuse of
   stale pre-open plans.
9. Hardened news entity provenance: provider symbols are advisory unless the
   route is trusted; Finnhub company mapping and alias coverage are explicit.
   The production quality gate currently reports READY.
10. Fixed monitor diagnostics so shell commands containing monitor names are
    not misclassified as running Python workers.

## Current Seven-Day Evidence

Generated from `reports/PAPER_OPERATIONAL_AUDIT.md` at
`2026-08-03T17:18:34Z`:

| Lane | Closed in authoritative USD window | Net USD | PF | Win rate | Strict reading |
|---|---:|---:|---:|---:|---|
| Crypto intraday long | 3 | +62.31 | 3.24 | 67% | Positive, but too few and concentrated |
| Crypto swing long | 8 | +10.75 | 1.12 | 50% | Barely positive; not stable proof |
| Crypto swing short | 2 | -3.16 | 0.00 | 0% | Weak and unproven |
| Stocks intraday | 0 clean closed | 0.00 | n/a | n/a | No edge conclusion yet |

Forward clean evidence is still below the required 30 closed trades for every
production crypto slice. Crypto intraday and swing each have only 13 clean
forward resolved rows in the broader evidence table. The top three winners
account for 100% of intraday-long profit and 91% of swing-long profit in the
current window. This is a concentration warning, not a promotion signal.

MEXC parity currently has five clean forward closes per profile:

- `mexc_model_f_runner_v1`: +11.17 USD, PF 1.954.
- `mexc_partial_tp_33_33_34_v1`: +4.76 USD, PF 1.407.

This sample is useful operational evidence but is far below the promotion
threshold. Current forward latency verdicts are `INSUFFICIENT_SAMPLE`; the new
capture path must accumulate real candidates before an SLA claim is valid.

## Verification

- Full suite: `2033 passed, 5 skipped`.
- Python compile sweep: passed.
- Scheduler dry-run: 90 steps validated; all CLI surfaces passed; no automatic
  Opus/Claude invocation detected.
- MEXC monitor: live worker healthy, kill switch CLEAR, submission enabled,
  no pending outbox, no open system risk at verification time.
- Runtime monitors: scheduler, pending crypto, MEXC canary, stocks session, and
  watchlist monitor observed with role-specific leader locks.
- Pending production ticks observed with 18/18 symbols and 72/72 timeframe
  pairs refreshed, followed by 21 pending checks when the shared full-pass lock
  was free.
- Worker rotation was verified in production: the old worker completed tick 10,
  emitted `pending_monitor_recycle`, released its lease, and the replacement
  resumed a 72/72 refresh and 21 checks under a new PID.

## Decision

Operational defects found in this pass are addressed and the system can keep
collecting Paper/Shadow evidence. This does not prove profitability. Do not
expand live routing from these seven-day numbers alone. Reassess manually after
each relevant lane reaches at least 30 clean closed forward trades and 28
forward days, with positive net USD, PF at least 1.25, acceptable drawdown, and
no single-winner concentration dependency.
