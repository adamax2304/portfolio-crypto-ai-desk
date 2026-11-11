# Stocks-Intraday C-Tier Shadow — Test Results (PART 1)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/test_stocks_c_tier_policy.py tests/test_stock_concentration_caps.py -q` → **all passed** (9 new + the existing concentration suite, unregressed).

## `tests/test_stocks_c_tier_policy.py` (9)
| Test | Asserts |
|---|---|
| stocks_intraday_c_tier_is_restricted_by_default | restricted; reason + diagnostic_or_policy labels set |
| stocks_intraday_AB_not_restricted | A and B → not restricted |
| crypto_c_tier_unaffected | crypto C-tier → not restricted by this stocks-only rule |
| stocks_swing_invest_c_tier_not_restricted_by_this_rule | swing/invest/scalp C-tier not restricted |
| actionable_policy_disables_restriction | `actionable` policy → not restricted |
| policy_loads_from_config_default_restricted | loader never raises; safe default |
| fields_do_not_carry_scoring_or_tpsl_keys | label dict has NO tier/score/TP/SL/size keys |
| paper_entry_never_pushes_stocks_intraday_c_tier | C-tier → `sent=False`, no Telegram, reason "not actionable" |
| AB_stocks_intraday_still_actionable | B-tier path unchanged; not shadow_c_tier |

## Spec coverage
- ✅ C-tier stocks intraday → shadow/review-only (never pushed)
- ✅ A/B stocks intraday unchanged
- ✅ crypto C-tier unaffected
- ✅ no scoring / TP/SL mutation (label fields carry none)
- ✅ payload includes restriction reason
- ✅ existing stock concentration tests still pass

## Verdict
**STOCKS_INTRADAY_C_TIER_SHADOW_READY.**
