# Position / Leverage Advisor — Test Results (PART 7)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/test_position_advisor.py -q` → **8 passed**.

| Test | Asserts |
|---|---|
| normal_case_computes_notional | entry 100 / stop 98 (2%) → notional $2,500, status ok |
| wide_stop_reduces_notional | 10% stop notional < 2% stop notional |
| tight_stop_increases_notional_but_warns_on_leverage | 0.04% stop → notional > $50k, status `warning`, leverage_warning set |
| missing_stop_is_unknown | stop None → `unknown`, notional None |
| unsafe_liquidation_buffer_when_stop_too_wide | 80% stop → `unsafe`, "UNSAFE" in warning |
| invalid_entry_stop_unknown | entry/stop 0 or equal → `unknown` |
| advisor_line_renders_and_unknown_is_none | renders for ok; None for unknown |
| pure_no_side_effects | inputs untouched; no order/size mutation |

## Spec coverage
- ✅ normal case computes notional
- ✅ wide stop reduces notional
- ✅ tight stop increases notional but leverage warning triggers
- ✅ missing stop → unknown
- ✅ unsafe liquidation buffer → unsafe
- ✅ no routing/size/execution mutation (pure function)

## Verdict
**POSITION_LEVERAGE_ADVISOR_LABEL_ONLY_READY.**
