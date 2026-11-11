# Initial Stop Variant Backtest

- DB: `C:\Users\adama\Documents\crypto-ai-desk\db\crypto_ai_desk.sqlite`
- Window: last 14 days
- Computed at: `2026-09-02T16:57:31.092562+00:00`
- Scope: research-only; no paper/live trades changed.
- Method: same signal entry rules and R ladder; variants alter only initial stop distance.

## Backfill

- Processed stop contracts: 1878
- By source: `{"legacy_atr_stop": 1305, "atr_fallback": 542, "support_resistance": 31}`
- Skipped: `{"no_candles": 1}`

## Summary

| Asset | Mode | Entry mode | Variant | N | Entries | Total R | Avg R | WR | Stop Rate | PF |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| crypto | intraday | BREAKOUT_CONTINUATION | current | 53 | 29 | 14.69 | 0.277 | 26.4% | 28.3% | 2.15 |
| crypto | intraday | BREAKOUT_CONTINUATION | wider_125 | 53 | 30 | 19.93 | 0.376 | 32.1% | 28.3% | 2.84 |
| crypto | intraday | LEVEL_HOLD_1BAR | current | 51 | 46 | -29.46 | -0.578 | 9.8% | 78.4% | 0.26 |
| crypto | intraday | LEVEL_HOLD_1BAR | wider_125 | 51 | 46 | -28.78 | -0.564 | 9.8% | 74.5% | 0.26 |
| crypto | intraday | LEVEL_HOLD_V2 | current | 13 | 13 | -6.41 | -0.493 | 15.4% | 92.3% | 0.37 |
| crypto | intraday | LEVEL_HOLD_V2 | wider_125 | 13 | 13 | -7.56 | -0.582 | 7.7% | 92.3% | 0.21 |
| crypto | intraday | LIMIT_THEN_TAKER_TIMEOUT | current | 4 | 4 | 0.01 | 0.003 | 25.0% | 25.0% | 1.01 |
| crypto | intraday | LIMIT_THEN_TAKER_TIMEOUT | wider_125 | 4 | 4 | -0.00 | -0.000 | 25.0% | 25.0% | 1.00 |
| crypto | intraday | MOMENTUM_TAKER_NOW | current | 2 | 2 | 0.07 | 0.034 | 50.0% | 0.0% | 1.08 |
| crypto | intraday | MOMENTUM_TAKER_NOW | wider_125 | 2 | 2 | 0.27 | 0.137 | 50.0% | 0.0% | 1.34 |
| crypto | intraday | PULLBACK_LIMIT | current | 13 | 11 | -6.77 | -0.521 | 15.4% | 76.9% | 0.25 |
| crypto | intraday | PULLBACK_LIMIT | wider_125 | 13 | 11 | -5.66 | -0.435 | 7.7% | 69.2% | 0.28 |
| crypto | scalp | BREAKOUT_CONTINUATION | current | 9 | 2 | 1.94 | 0.215 | 11.1% | 11.1% | 8.07 |
| crypto | scalp | BREAKOUT_CONTINUATION | wider_125 | 9 | 2 | 0.83 | 0.093 | 11.1% | 11.1% | 4.04 |
| crypto | scalp | LIMIT_THEN_TAKER_TIMEOUT | current | 6 | 6 | -5.57 | -0.929 | 0.0% | 83.3% | 0.00 |
| crypto | scalp | LIMIT_THEN_TAKER_TIMEOUT | wider_125 | 6 | 6 | -5.48 | -0.914 | 0.0% | 83.3% | 0.00 |
| crypto | scalp | PULLBACK_LIMIT | current | 119 | 102 | -76.04 | -0.639 | 6.7% | 75.6% | 0.15 |
| crypto | scalp | PULLBACK_LIMIT | wider_125 | 119 | 102 | -73.67 | -0.619 | 8.4% | 72.3% | 0.16 |
| crypto | swing | BREAKOUT_CONTINUATION | current | 36 | 27 | 3.55 | 0.099 | 22.2% | 52.8% | 1.20 |
| crypto | swing | BREAKOUT_CONTINUATION | wider_125 | 36 | 27 | 5.99 | 0.166 | 30.6% | 52.8% | 1.43 |
| crypto | swing | LIMIT_THEN_TAKER_TIMEOUT | current | 38 | 38 | -4.25 | -0.112 | 21.1% | 73.7% | 0.82 |
| crypto | swing | LIMIT_THEN_TAKER_TIMEOUT | wider_125 | 38 | 38 | -0.00 | -0.000 | 34.2% | 65.8% | 1.00 |
| crypto | swing | MOMENTUM_TAKER_NOW | current | 4 | 4 | -4.00 | -1.000 | 0.0% | 100.0% | 0.00 |
| crypto | swing | MOMENTUM_TAKER_NOW | wider_125 | 4 | 4 | -3.22 | -0.805 | 0.0% | 100.0% | 0.00 |
| crypto | swing | PULLBACK_LIMIT | current | 72 | 68 | -32.10 | -0.446 | 15.3% | 86.1% | 0.39 |
| crypto | swing | PULLBACK_LIMIT | wider_125 | 72 | 68 | -31.58 | -0.439 | 13.9% | 80.6% | 0.39 |
| stocks | intraday | BREAKOUT_CONTINUATION | current | 18 | 17 | 13.84 | 0.769 | 50.0% | 55.6% | 3.02 |
| stocks | intraday | BREAKOUT_CONTINUATION | wider_125 | 18 | 17 | 7.16 | 0.398 | 38.9% | 66.7% | 1.89 |
| stocks | intraday | CATALYST_RS_CONTINUATION | current | 1 | 1 | -1.00 | -1.000 | 0.0% | 100.0% | 0.00 |
| stocks | intraday | CATALYST_RS_CONTINUATION | wider_125 | 1 | 1 | -1.00 | -1.000 | 0.0% | 100.0% | 0.00 |
| stocks | intraday | PULLBACK_LIMIT | current | 17 | 16 | -4.67 | -0.275 | 17.6% | 76.5% | 0.64 |
| stocks | intraday | PULLBACK_LIMIT | wider_125 | 17 | 16 | -3.72 | -0.219 | 17.6% | 70.6% | 0.69 |

## Decision Rule

Do not promote a variant just because it improves one small cell. Prefer it only if it improves total R/PF, does not cut entries materially, and lowers stop-rate across the relevant live mode.
