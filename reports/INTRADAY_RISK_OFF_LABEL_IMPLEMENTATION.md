# Intraday Risk-Off / Long-Bias Label — Implementation (PART 6)

**Date:** 2026-06-17 · **Verdict:** **RISK_OFF_LABEL_READY** (visibility label; throttle NOT enabled).
**Mode:** label only. **No throttle, no half-size, no score change, no block.**

## What was built
- **`src/risk/risk_off.py`**
  - `classify_risk_off(day_change_pct, h1_trend, h4_trend, *, threshold=-0.75)` — pure classifier.
  - `compute_risk_off(file_store, now)` — reads BTC OHLCV (binance 1d/1h/4h), fails open to `unknown`.
- Wired via `assemble_risk_guard_fields` → payload + Control Plane; a compact risk-off context line is added to crypto-long alerts.

## Fields emitted
`btc_intraday_risk_off`, `btc_day_change_pct`, `btc_1h_trend`, `btc_4h_trend`, `regime_context` (btc_up/btc_flat/btc_risk_off/unknown), `would_throttle_long` (diagnostic), `risk_off_diagnostic`, `diagnostic_only=true`. (`alt_breadth_change` / `macro_risk_level` are left `None` — not faked when unavailable.)

## Rule
`btc_intraday_risk_off = (BTC day change ≤ −0.75%) OR (1h trend down AND day < 0)`. The −0.75% threshold cleanly separates the 06-15 up day from the 06-16/17 down days.

## Validation (replay)
| Day | BTC day % | Flag | Expected |
|---|---|---|---|
| 06-15 | +0.89% | not risk-off | ✅ must not trigger |
| 06-16 | −0.99% | risk-off | ✅ must trigger |
| 06-17 | −0.96% | risk-off | ✅ must trigger |

## Safety
- `would_throttle_long` is a flag only — longs are not blocked, half-sized, or rescored.
- Returns `unknown` (not a fake value) when BTC data is missing.
