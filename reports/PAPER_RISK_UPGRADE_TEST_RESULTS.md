# Paper Risk Upgrade — Test Results (PART 8)

**Date:** 2026-06-24.

## crypto-ai-desk — `tests/test_paper_execution_accounting.py` (10 tests, pass)
| scenario | asserted |
|---|---|
| long TP1→stop, MFE +0.7R | touch +1.0, **paper 0.0 (BE)**, giveback=True |
| long TP1→stop, MFE +1.3R | **paper +0.5 (lock)** |
| stop before +0.6R (MFE 0.3R) | **paper −1.0** |
| TP3 runner | touch 3.0, paper 3.0 |
| **short** TP1→stop, MFE +0.8R | touch +1.0, paper 0.0; `r_multiple` short sign-flip ✓ |
| expired-after-entry, MFE 0.2R | paper 0.0 (resolved, not "open") |
| not entered | paper None |
| **storage idempotent + no signal_outcomes mutation** | two upserts → 1 row; `final_r` unchanged before==after |
| legacy_touch / first_tp_close models | available + correct |

Full sweep `paper_execution_accounting + realistic_pnl_models + catalyst_label_refresh + display_status + default_market_schedule + project_state_docs` → **74 passed**.

## trading-desk-control backend — `backend/tests/test_books.py` (extended)
- paper_execution_r: BE @ +0.6R = 0.0; lock @ +1R = +0.5; stop <0.6R = −1.0; TP3 = 3.0; missing MFE → None + `paper_execution_available` False (no silent 0).
- dashboard headline exposes `today_paper_execution_r` + `risk_model`; operator d7 paper (0.0) distinct from touch (+1.0) on a give-back; label mentions "Touch R".
- Full backend suite → **53 passed**.

## Frontend
- `npm run build` (tsc -b + vite build) → **exit 0**, 92 modules, no type errors; displays both Paper Exec R and Touch R.

## Scheduler / safety
- New step `paper execution accounting refresh` present at **position 6/23**; `command_nonfatal`; **no live/exchange/order steps**; LLM-auto-invoke guard OK.
- Docs validator → `PROJECT STATE DOCS: OK`.
- **No `signal_outcomes.final_r` mutation** (315,610 rows + final_r intact; no `paper_execution_*` column added to signal_outcomes). New `paper_execution_outcomes` table populated (1610 rows).

## Verdict
`PAPER_RISK_UPGRADE_TESTS_PASS`
