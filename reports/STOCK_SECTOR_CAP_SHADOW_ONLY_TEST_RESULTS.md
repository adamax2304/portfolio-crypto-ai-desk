# Stock Sector-Cap — Shadow-Only Test Results (PART 3)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/test_sector_cap_shadow.py tests/test_stock_concentration_caps.py -q` → **all passed** (6 new + the existing concentration-cap suite, unregressed).

## `tests/test_sector_cap_shadow.py` (6)
| Test | Asserts |
|---|---|
| three_same_bucket_third_would_bind_sector_cap | AMD/NVDA/SMCI semis → 3rd = `shadow_sector_cap` rank 3; 1st = `actionable` |
| second_same_bucket_is_half_size_candidate | 2nd semis long → `half_size` rank 2 |
| proxy_duplicate_would_label | QQQ/XLK → 2nd = `shadow_proxy_duplicate` |
| crypto_signal_not_applicable_via_store | crypto → `not_applicable` |
| store_wrapper_includes_current_signal_and_reports_actual | SMCI as 3rd semis → would `shadow_sector_cap`, while `actual_concentration_status=actionable` (the gap) |
| fails_open_on_bad_store | broken store → `not_applicable`, diagnostic_only |

## Regression safety
- The existing `tests/test_stock_concentration_caps.py` suite still passes → the cap **value and rules are unchanged**; the shadow module only *reads* them.
- The diagnostic does NOT touch routing or actionability (asserted: `actual_concentration_status` is reported separately from `would_bind_sector_cap`).

## Spec coverage
- ✅ 3 same-bucket stock intraday signals same day → 3rd gets `would_bind_sector_cap`.
- ✅ Diagnostic does not block Manual Entry / actionability (separate field; live path unchanged).
- ✅ Proxy-duplicate would-label works.
- ✅ Cap value stays unchanged.
- ✅ No regression in existing stock concentration tests.

## Verdict
**SECTOR_CAP_SHADOW_ONLY_WIRING_READY.**
