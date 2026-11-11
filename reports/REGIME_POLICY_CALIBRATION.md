# Market-Regime Policy Calibration

Generated: `2026-11-11T21:32:27.621143+00:00`  
Version: `regime_policy_calibration_v1`

This is a read-model calibration. It does not modify scores, Paper routing, live routing, orders, `proposed_signals`, `signal_outcomes`, or `final_r`. Results from historical/backfill rows are never used for a runtime recommendation. A runtime change additionally requires at least 20 exact USD rows covering at least 80% of the selected forward cohort.

## Crypto

Only valid, resolved, point-in-time forward Paper outcomes are shown. R is diagnostic only; a policy change additionally requires adequate authoritative net-USD coverage.

Chronological split: `2026-09-03T04:00:37.300251+00:00` (oldest 2/3 train, newest 1/3 validation).

| Mode | Side | Regime | All n / USD rows / R / PF | Train n / R / PF | Validation n / R / PF |
|---|---|---|---|---|---|
| intraday | long | chop | 44 / 19 / 2.72 / 1.13 | 24 / 3.20 / 1.23 | 20 / -0.48 / 0.93 |
| intraday | long | neutral | 48 / 29 / 56.44 / 5.34 | 31 / 44.64 / 5.96 | 17 / 11.80 / 3.95 |
| intraday | long | risk_off | 15 / 2 / -2.26 / 0.72 | 10 / -5.50 / 0.08 | 5 / 3.24 / 2.62 |
| intraday | long | risk_on | 356 / 220 / 92.48 / 1.67 | 215 / 63.77 / 1.74 | 141 / 28.71 / 1.54 |
| intraday | long | unknown | 1 / 1 / -1.00 / 0.00 | 0 / 0.00 / n/a | 1 / -1.00 / 0.00 |
| intraday | short | chop | 5 / 0 / 0.00 / 1.00 | 2 / -0.50 / 0.50 | 3 / 0.50 / inf |
| intraday | short | neutral | 3 / 1 / -2.00 / 0.00 | 2 / -1.00 / 0.00 | 1 / -1.00 / 0.00 |
| intraday | short | risk_off | 10 / 4 / -5.26 / 0.12 | 0 / 0.00 / n/a | 10 / -5.26 / 0.12 |
| intraday | short | risk_on | 5 / 2 / 5.21 / 3.60 | 4 / 2.01 / 2.00 | 1 / 3.20 / inf |
| scalp | long | chop | 8 / 0 / -1.00 / 0.50 | 8 / -1.00 / 0.50 | 0 / 0.00 / n/a |
| scalp | long | neutral | 3 / 0 / -0.50 / 0.50 | 3 / -0.50 / 0.50 | 0 / 0.00 / n/a |
| scalp | long | risk_off | 3 / 0 / -0.50 / 0.50 | 3 / -0.50 / 0.50 | 0 / 0.00 / n/a |
| scalp | long | risk_on | 57 / 0 / 1.46 / 1.08 | 57 / 1.46 / 1.08 | 0 / 0.00 / n/a |
| scalp | long | unknown | 1 / 0 / -1.00 / 0.00 | 1 / -1.00 / 0.00 | 0 / 0.00 / n/a |
| scalp | short | chop | 2 / 0 / 0.50 / inf | 2 / 0.50 / inf | 0 / 0.00 / n/a |
| scalp | short | neutral | 1 / 0 / 0.00 / n/a | 1 / 0.00 / n/a | 0 / 0.00 / n/a |
| scalp | short | risk_on | 5 / 0 / -3.50 / 0.12 | 5 / -3.50 / 0.12 | 0 / 0.00 / n/a |
| swing | long | chop | 33 / 6 / 17.61 / 2.35 | 28 / 22.61 / 3.83 | 5 / -5.00 / 0.00 |
| swing | long | neutral | 29 / 6 / 19.99 / 3.00 | 22 / 14.00 / 2.75 | 7 / 5.99 / 4.00 |
| swing | long | risk_off | 3 / 1 / 1.00 / inf | 0 / 0.00 / n/a | 3 / 1.00 / inf |
| swing | long | risk_on | 197 / 25 / 120.33 / 2.94 | 135 / 70.55 / 2.36 | 62 / 49.78 / 5.98 |
| swing | short | chop | 3 / 0 / 1.80 / 1.90 | 2 / -2.00 / 0.00 | 1 / 3.80 / inf |
| swing | short | neutral | 1 / 1 / 0.00 / n/a | 1 / 0.00 / n/a | 0 / 0.00 / n/a |
| swing | short | risk_off | 4 / 1 / 5.30 / inf | 1 / 0.50 / inf | 3 / 4.80 / inf |
| swing | short | risk_on | 4 / 1 / -0.50 / 0.50 | 3 / -0.50 / 0.50 | 1 / 0.00 / n/a |

## Stocks

Only valid, resolved, point-in-time forward Paper outcomes are shown. R is diagnostic only; a policy change additionally requires adequate authoritative net-USD coverage.

Chronological split: `2026-10-13T18:31:40.994432+00:00` (oldest 2/3 train, newest 1/3 validation).

| Mode | Side | Regime | All n / USD rows / R / PF | Train n / R / PF | Validation n / R / PF |
|---|---|---|---|---|---|
| intraday | long | chop | 10 / 0 / 1.50 / 2.50 | 3 / 0.00 / 1.00 | 7 / 1.50 / inf |
| intraday | long | neutral | 82 / 0 / -16.54 / 0.39 | 52 / -8.77 / 0.46 | 30 / -7.77 / 0.28 |
| intraday | long | risk_off | 21 / 0 / -4.26 / 0.30 | 17 / -3.46 / 0.30 | 4 / -0.79 / 0.30 |
| intraday | long | risk_on | 33 / 0 / -11.52 / 0.15 | 28 / -10.00 / 0.17 | 5 / -1.52 / 0.00 |
| intraday | short | chop | 2 / 0 / 0.50 / inf | 2 / 0.50 / inf | 0 / 0.00 / n/a |
| intraday | short | neutral | 47 / 0 / -3.92 / 0.66 | 33 / -7.33 / 0.29 | 14 / 3.41 / 3.54 |
| intraday | short | risk_off | 78 / 0 / -2.01 / 0.90 | 47 / -1.60 / 0.87 | 31 / -0.42 / 0.95 |
| intraday | short | risk_on | 16 / 0 / -1.57 / 0.66 | 9 / -0.50 / 0.83 | 7 / -1.07 / 0.32 |
| swing | long | neutral | 4 / 0 / -2.50 / 0.17 | 4 / -2.50 / 0.17 | 0 / 0.00 / n/a |

## Policy Conclusions

- **crypto intraday long / risk_off**: `KEEP_CURRENT_UNTIL_USD_EVIDENCE`. R diagnostics are negative, so there is no case to relax the existing protective block; USD coverage is still below the threshold for any policy rewrite.
- **crypto swing long / chop**: `KEEP_CURRENT_INSUFFICIENT_USD_EVIDENCE`. R-only splits are encouraging, but terminal USD coverage is not sufficient to change routing or size.
- **crypto intraday long / chop**: `KEEP_CURRENT_INSUFFICIENT_USD_EVIDENCE`. Validation is not consistently positive; keep BREAKOUT confirmation and do not upgrade chop to FULL_SIZE.
- **crypto valid data + unknown label**: `NO_FALSE_WEAK_DEMOTION`. Unknown is a data-classification state, not affirmative risk-off evidence.
- **stocks intraday / all regimes**: `KEEP_CURRENT_INSUFFICIENT_USD_EVIDENCE`. Forward point-in-time outcomes are not profitable across the observed regimes; improve entry/exit quality before reducing gates.

## Guardrails

- `unknown` is not treated as a confirmed weak regime when BTC price data are present.
- A regime action is only considered stable after a chronological validation split; small cohorts remain size-capped.
- This analysis does not infer a tradable edge for any disabled Shadow-only lane, especially scalp.
