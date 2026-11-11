# Circuit Breaker — Alert-Only Test Results (PART 1)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/test_circuit_breaker.py tests/test_risk_guard_fields.py -q`
**Result:** **16 passed** (10 circuit-breaker + 6 risk-guard/paper-entry integration).

## `tests/test_circuit_breaker.py` (10)
| Test | Asserts |
|---|---|
| daily_minus_2r_triggers_would_pause | −2R day → state `would_pause`, level 2 |
| three_stops_triggers_flag_even_if_r_above_2 | 3 stops trip the flag regardless of net R |
| minus_3r_is_level_3 | −3R → level 3, consecutive=3, require-fresh-catalyst |
| crypto_long_streak_same_regime | 2 crypto long stops same regime → would_throttle_crypto_longs |
| size_stepdown_after_first_stop_is_flag_only | 1 stop → would_reduce_size flag, NOT would_pause |
| clean_day_is_ok_and_no_warning_line | no stops → ok, no Telegram line |
| other_asset_or_other_day_excluded | stocks/yesterday rows excluded from crypto-today scope |
| warning_line_present_when_would_pause | compact line says "would pause" + "diagnostic" |
| store_wrapper_fails_open_on_bad_store | broken store → ok / no pause |
| config_thresholds_are_alert_only_values | thresholds = −2/−3/3/2 |

## `tests/test_risk_guard_fields.py` (6) — integration / non-blocking / dedupe
| Test | Asserts |
|---|---|
| assembler_returns_expected_fields | all guard fields present + diagnostic_only |
| profit_protection_hint_mapping | MFE→hint mapping correct |
| paper_entry_not_blocked_and_fields_in_payload | with a −3R day the alert STILL sends; payload `circuit_breaker_state=would_pause`; routing `telegram`; CB line in message |
| circuit_breaker_warning_is_deduped_per_day_level | 1st alert warns, 2nd deduped; field still present on both |
| assembler_fails_open | broken store → diagnostic_only, state `ok` |

## Spec coverage
- ✅ fixture day with −2R triggers alert flag
- ✅ fixture day with ≥3 stops triggers flag
- ✅ diagnostic flag does NOT block paper_entry (still `telegram_status=sent`, routing unchanged)
- ✅ dedupe/cooldown works (one per asset/mode/day/level)
- ✅ no change to scoring/routing/size (asserted via `telegram_channel=telegram`, size_weight untouched)
