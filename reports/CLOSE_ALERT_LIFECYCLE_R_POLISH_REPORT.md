# Close-Alert Lifecycle-R Polish Report (PART 3)

**Date:** 2026-06-19 · `src/notifiers/close_alert.py` `decide_close`. **Display wording only; dedup/routing/alert_type unchanged.**

## Change
The single `Result: {r:+.1f}R raw / {r:+.1f}R sized` line is now lifecycle-aware:
- **expired (entered, unresolved):** `Result: 0R — unresolved (entered, no TP/SL before validity window)` + `(raw …R / sized …R, no terminal exit)`.
- **genuine flat (win/loss outcome with raw_r==0):** `Result: CLOSED FLAT 0R`.
- **win/loss:** unchanged `Result: +1.0R raw / -0.8R sized` (`:+.1f`, no `+-`).
- **ambiguous:** `Result: ambiguous …R`.
- **label/R-sign contradiction** (win+neg or loss+pos): adds `⚠ data check: outcome label vs R sign mismatch` (alert_type/header untouched).

## Why it is safe (no dedup regression, no historical resend)
- Dedup key = `(signal_id, alert_type)`; `message_hash` is audit-only. Wording changes don't affect the dedup decision.
- alert_type/header still derive from `final_outcome` (unchanged) → existing sent alerts stay deduped.
- Transition guard + 4-day age backstop unchanged → historical closes never re-fire.

## Tests added (`tests/test_telegram_standardization.py`)
- `test_close_expired_after_entry_not_bare_plus_0r` — "unresolved" + reason, no `Result: +0.0R raw`, no `+-`.
- `test_close_true_flat_shows_closed_flat_0r` — `CLOSED FLAT 0R`.
- `test_close_loss_sign_no_double_sign` — `-1.0R raw`, no `+-`.
- `test_close_win_with_negative_r_flags_contradiction` — "data check", no `+-`.
- **41 passed** (telegram-standardization + alert-dispatch-gates).

## Verdicts
**CLOSE_ALERT_LANGUAGE_OK · CLOSE_ALERT_LIFECYCLE_R_READY** (applied safely; not deferred — dedup is text-independent).
