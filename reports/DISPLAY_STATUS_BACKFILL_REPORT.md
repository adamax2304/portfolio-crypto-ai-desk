# Display-Status Backfill Report

**Generated:** 2026-06-19T12:28:45.569453+00:00 · rows analysed: 2077 · display columns present: False · rows written: 0

> Display semantics only. Original `status` / `entry_triggered` / `final_r` / `final_outcome` are untouched. This is the lifecycle-aware view, not a rewrite.

## Counts by display group

| display_group | count |
|---|---|
| OPEN_ACTIVE | 5 |
| WAITING_FOR_ENTRY | 0 |
| REVIEW_ONLY_SHADOW | 138 |
| ENTERED_UNRESOLVED_EXPIRED | 483 |
| NO_ENTRY_EXPIRED | 629 |
| CLOSED_WIN | 313 |
| CLOSED_LOSS | 506 |
| CLOSED_FLAT | 0 |
| UNKNOWN_INCONSISTENT | 3 |

## Key splits (for reports / Telegram)
- expired_after_entry_count: **483**
- no_entry_expired_count: **629**
- open_actionable_count: **5**
- waiting_for_entry_count: **0**
- review_shadow_count: **138**
- closed_flat_count: **0**
- unknown_inconsistent_count: **3**

## Inconsistent rows (need review — not auto-fixed)
| symbol | mode | status | entry_triggered | display_reason |
|---|---|---|---|---|
| TAO/USDT | scalp | ambiguous | 1 | ambiguous lifecycle — needs review |
| TAO/USDT | intraday | ambiguous | 1 | ambiguous lifecycle — needs review |
| SMH | intraday | ambiguous | 1 | ambiguous lifecycle — needs review |

## Notes
- `ENTERED_UNRESOLVED_EXPIRED` = `expired` + `entry_triggered=1` → the trade was entered but didn't hit TP/SL before the window ended (NOT a missed entry).
- `NO_ENTRY_EXPIRED` = no-entry / stale / moved-away / expired-without-touch.
- Inconsistent = a no-entry status carrying `entry_triggered=1`, or an `ambiguous` status — surfaced for review; the underlying rows are left exactly as-is.
- No migration is required for display; columns are optional (`--add-columns`).