# Status Live Polish — Test Results (PART 7)

**Date:** 2026-06-19

## crypto-ai-desk
`pytest tests/test_display_status.py tests/test_paper_entry_alerts.py tests/test_default_market_schedule.py tests/test_telegram_standardization.py tests/test_project_state_docs.py` → **90 passed**.
- `test_display_status`: 19 tests incl. the new PART-1 sign/contradiction cases.
- Docs validator (`check_project_state_docs.py`) → **OK**.
- Scheduler dry-run: weekday 25 steps / weekend 16; **"LLM-auto-invoke check OK — no Opus/Claude tokens in plan"**.

## Control Plane (trading-desk-control)
- Backend: `pytest tests/test_display_status.py tests/test_control_plane.py` → **38 passed**.
- Frontend: `tsc -b` → **exit 0**.

## Required assertions — all verified
| Assertion | Status |
|---|---|
| no `+-` in output | ✅ `test_no_double_sign_in_labels_and_r`, `test_no_double_sign_in_telegram_output`; live report grep clean |
| expired split appears | ✅ `test_telegram_expired_split_not_single_count` |
| no raw `expired` alone | ✅ summary splits entered-unresolved vs no-entry |
| no raw `+0R` alone for unresolved | ✅ `format_r_with_lifecycle` → "0R display / no TP-SL before expiry" |
| "no active trades" never hides waiting/review | ✅ `test_telegram_summary_not_just_no_active` + the explicit note line |
| inconsistent flagged not rewritten | ✅ backfill writes 0 rows; 87→3 via read-model; 3 ambiguous kept |
| no trade logic changed | ✅ see STATUS_LIVE_POLISH_SAFETY_VERIFICATION.md |
| win/-R contradiction not CLOSED_WIN | ✅ `test_win_label_with_negative_r_is_not_closed_win` |
| missing fields don't crash | ✅ crypto + Control-Plane `test_missing_fields_do_not_crash` |

## Totals
**128 tests passed** (90 crypto-ai-desk + 38 Control Plane), tsc exit 0, docs validator OK.
