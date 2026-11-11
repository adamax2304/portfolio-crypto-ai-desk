# Telegram / Reports Display Correction (PART 6)

**Date:** 2026-06-24. Future paper close alerts now carry the honest paper execution R. Additive + fail-open. No historical re-send.

## Close alert (`src/notifiers/close_alert.py`)
After the existing Result/Exit lines, a paper-execution block is appended (fail-open, PAPER/ACCOUNTING only):
```
Paper exec R (Model F): {+/-X.X}R [· BE @ +0.6R | · lock +0.5R @ +1R]
(touch {+/-Y.Y}R = highest TP touched · optimistic)
Closed at protected stop, not the touched TP.        # only when close_reason ∈ {breakeven_stop, profit_lock_stop}
```
- The legacy "Result" line (touch-based raw/sized) remains but is now clearly subordinate to the labelled Paper exec line — so a give-back is no longer presented as a clean "TP win".
- Protection events explained inline: "BE @ +0.6R", "lock +0.5R @ +1R", "Closed at protected stop".
- Computed via `build_record_from_signal`; if it errors, the alert sends unchanged (no block).

## Dedup / no-flood
- Close-alert dedup is keyed by `(signal_id, alert_type)`, **not message text** — the wording change cannot resend already-sent or historical alerts. Backfill-age guard (`MAX_CLOSE_AGE_DAYS`) and the prev_status terminal guard remain. No historical duplicate alerts.

## Paper monitor summary
- The Operator-book summary the monitor/app surfaces now reports **Paper Execution R today** (main) and **Touch R** separately, plus **protected-trades count** — sourced from the same `books.get_dashboard_summary` (`protected_n`, `be_scratch_n`, `giveback_n`).

## Verdict
`TELEGRAM_SHOWS_PAPER_EXECUTION_R`
