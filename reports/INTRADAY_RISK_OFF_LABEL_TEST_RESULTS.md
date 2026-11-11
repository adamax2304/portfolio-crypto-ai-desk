# Intraday Risk-Off Label — Test Results (PART 6)

**Date:** 2026-06-17 · **Command:** `python -m pytest tests/test_risk_off_label.py -q` → **8 passed**.

| Test | Asserts |
|---|---|
| up_day_does_not_trigger | +0.89% (06-15) → not risk-off, `btc_up`, no throttle |
| down_days_trigger | −0.99% / −0.96% (06-16/17) → risk-off, `btc_risk_off` |
| flat_day_is_btc_flat | +0.1% → `btc_flat` |
| threshold_boundary | exactly −0.75% triggers; −0.74% does not |
| unknown_when_data_missing | None input → `unknown`, no throttle |
| 1h_down_with_negative_day_triggers | day −0.4% + 1h down → risk-off |
| compute_risk_off_from_frames | builds −1.0% day from fake OHLCV frames → risk-off |
| compute_risk_off_fails_open | broken file_store → `unknown` |

## Spec coverage
- ✅ 06-15-like up day does NOT over-trigger
- ✅ 06-16/17-like down day flags risk-off context
- ✅ longs NOT blocked / NOT half-sized / score unchanged (flag only)

## Verdict
**RISK_OFF_LABEL_READY.** See `INTRADAY_RISK_OFF_LABEL_30D_MEASUREMENT.md` for whether acting on it is justified (it is not, yet).
