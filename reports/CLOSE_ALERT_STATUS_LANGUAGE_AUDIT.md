# Close-Alert Status Language Audit (PART 3)

**Date:** 2026-06-19 · `src/notifiers/close_alert.py`.

## Dedup / hash analysis (is a wording change safe?)
- **Dedup is by `(signal_id, alert_type)`** — `has_existing_close_alert(store, signal_id, alert_type)` queries `signal_alerts WHERE signal_id=? AND alert_type=?`. 
- `message_hash` is **recorded for audit only**, never used to decide whether to send.
- Additional resend guards: the **transition guard** (`prev_status` already terminal → skip), the **4-day age backstop**, and the per-(signal_id, alert_type) dedup.
- **Conclusion: changing the message TEXT cannot cause a resend** of an already-sent or historical close alert. Safe to improve wording.

## Ambiguities found (pre-fix)
1. `Result: {raw_r_f:+.1f}R raw / {sized_r:+.1f}R sized` for an **expired-after-entry** (raw_r=0) → `+0.0R`, reads like a flat/profit close.
2. No explicit `CLOSED FLAT 0R` for a genuine 0R close.
3. No guard if `final_outcome` (win/loss) contradicts the R sign (no `+-` though, since `:+.1f`).

Note: `:+.1f` already prevented `+-` here; raw `expired` was already accompanied by a "Reason:" line + the HEADER_CLOSE_EXPIRED header (not bare).

## Fix applied (dedup-safe, see CLOSE_ALERT_LIFECYCLE_R_POLISH_REPORT.md)
Lifecycle-aware Result wording in `decide_close`; alert_type/header/dedup key unchanged.

## Verdict
**CLOSE_ALERT_LIFECYCLE_R_READY** (safe wording change applied; dedup semantics preserved; no historical resend).
