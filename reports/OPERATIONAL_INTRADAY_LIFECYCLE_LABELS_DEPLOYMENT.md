# Operational Intraday Lifecycle Labels — Deployment (PART 4)

**Date:** 2026-06-17 · **Verdict:** **INTRADAY_LIFECYCLE_OPERATIONAL_READY**

## Wiring
- New read-only script `scripts/open_intraday_lifecycle_review.py` loads `store.load_active_signals()`, computes `compute_lifecycle_label(...)` for every open **intraday** signal (using its latest outcome's `entry_triggered_at` + the current BTC regime), and writes `reports/OPEN_INTRADAY_LIFECYCLE_REVIEW.md`.
- Wired into the scheduler support tail as a **non-fatal** step ("open intraday lifecycle review").
- The same lifecycle fields are already attached per-signal to the paper-entry payload (via the risk-guard assembler) for Telegram/Control-Plane visibility.

## Labels surfaced
Crypto: `fresh_intraday` / `aging_intraday` / `stale_intraday` / `intraday_carryover` / `intraday_carryover_requires_review` / `expired_at_0R_candidate` + `held_hours` + `next_day_revalidation_required`.
Stocks: `rth_close_approaching`, `rth_overnight_hold`, carryover → review.

## First live run
`open intraday signals: 229 · needing review: 12`. The 12 are carryover/stale/expired-at-0R candidates flagged for next-session revalidation — surfaced for the operator, **not** auto-closed.

## Safety (asserted by tests)
- No `force_close` / `flatten` / `action` field anywhere in the output (lifecycle tests).
- Closed/terminal signals are not mislabeled as open (`closed`/`n/a`).
- No expiry change, no resize. The prior audit showed carry is net-positive → relabel + revalidate, never blanket-flatten.

## Reports
`OPEN_INTRADAY_LIFECYCLE_REVIEW.md` (per cycle). Tests: `tests/test_intraday_lifecycle.py` (7).
