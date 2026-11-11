# Intraday Lifecycle Labels — Test Results (PART 5)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/test_intraday_lifecycle.py -q` → **7 passed**.

| Test | Asserts |
|---|---|
| crypto_fresh_then_aging_then_stale | 2h→fresh, 8h→aging, 13h→stale (+revalidation) |
| crypto_carryover_requires_review_and_no_force_close | created yesterday → carryover + revalidation; **no force_close/flatten/action field** |
| crypto_expired_at_0r_candidate_past_validity | 26h → `expired_at_0R_candidate` |
| stocks_overnight_hold_flagged | stocks held overnight → `rth_overnight_hold` + revalidation |
| stocks_fresh_intraday_during_rth | inside RTH, 1h old → `fresh_intraday`, no overnight |
| terminal_or_non_intraday_not_labeled | stopped → `closed`; swing → `n/a` |
| held_hours_and_regime_change_flag | held_hours correct; regime change flagged |

## Spec coverage
- ✅ overnight intraday gets a label
- ✅ stocks RTH carryover gets a label
- ✅ **no force close** (explicitly asserted: no action/flatten/force_close key)
- ✅ label appears in payload/report (via the risk-guard assembler integration test)

## Verdict
**INTRADAY_REVALIDATION_ALERT_ONLY_READY.**
