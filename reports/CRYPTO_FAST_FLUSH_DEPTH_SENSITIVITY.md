# Crypto Fast Flush - Sweep Depth Sensitivity

- generated: `2026-10-04T12:43:34.681782+00:00`
- source period: `2026-09-07T22:40:00+00:00` to `2026-09-28T20:45:00+00:00`
- split: train through `2026-09-21T07:30:00+00:00`, validation through `2026-09-26T13:10:00+00:00`, then chronological test
- replay rows: `1159`; distinct events: `608`

All figures are net of modeled fees and slippage. The replay remains point-in-time, uses stop-first handling inside ambiguous bars, and counts one strongest trade per 15-minute market liquidation cascade.

Important limitation: these historical rows were used by earlier fast-flush research. The last 20% is chronological out-of-development evidence for this depth comparison, but it is not a never-before-seen final holdout for the overall strategy.

## Fixed Candidates

### Shallow

- parameters: `{"max_flush_atr": 2.25, "max_flush_pct": 1.2, "max_oi_drop_pct": 5.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 1.25, "min_flush_pct": 0.6, "min_liq_percentile": 0.8, "min_oi_drop_pct": 1.0, "min_rvol": 1.0, "min_stop_distance_pct": 0.005, "sessions": ["europe", "us"]}`
- train: n=9, +2.432R, PF=1.945, win=77.8%, DD=$13.51
- validation: n=5, +2.923R, PF=None, win=100.0%, DD=$0.00
- test: n=3, -0.595R, PF=0.499, win=66.7%, DD=$11.88
- all: n=17, +4.760R, PF=2.266, win=82.4%, DD=$13.51

### Deep

- parameters: `{"max_flush_atr": 5.0, "max_flush_pct": 2.75, "max_oi_drop_pct": 5.0, "max_spread_bps": 18.0, "max_stop_distance_pct": 0.015, "min_flush_atr": 2.0, "min_flush_pct": 1.5, "min_liq_percentile": 0.9, "min_oi_drop_pct": 0.25, "min_rvol": 1.0, "min_stop_distance_pct": 0.0075, "sessions": ["europe", "us"]}`
- train: n=11, +4.550R, PF=4.764, win=81.8%, DD=$11.61
- validation: n=9, +2.131R, PF=1.895, win=77.8%, DD=$14.97
- test: n=5, +3.334R, PF=None, win=100.0%, DD=$0.00
- all: n=25, +10.015R, PF=3.791, win=84.0%, DD=$14.98

## One-Dimensional Sensitivity

### Move size

| Band | All | Latest test |
|---|---:|---:|
| `micro_0.20_0.60pct` | n=8, +1.438R, PF=2.457, win=87.5%, DD=$9.87 | n=0, +0.000R, PF=None, win=0.0%, DD=$0.00 |
| `shallow_0.60_1.00pct` | n=15, +0.180R, PF=1.032, win=53.3%, DD=$30.42 | n=4, -1.883R, PF=0.272, win=25.0%, DD=$25.87 |
| `ordinary_1.00_1.50pct` | n=30, -0.455R, PF=0.96, win=60.0%, DD=$37.63 | n=5, -0.359R, PF=0.81, win=60.0%, DD=$18.86 |
| `deep_1.50_2.75pct` | n=45, +4.920R, PF=1.363, win=68.9%, DD=$32.32 | n=10, +1.076R, PF=1.306, win=70.0%, DD=$23.14 |
| `ultra_2.75_5.00pct` | n=4, -0.666R, PF=0.715, win=50.0%, DD=$15.10 | n=2, -0.343R, PF=0.711, win=50.0%, DD=$11.88 |

### ATR depth

| Band | All | Latest test |
|---|---:|---:|
| `small_0.65_1.50atr` | n=23, +0.175R, PF=1.018, win=65.2%, DD=$36.70 | n=6, -1.845R, PF=0.473, win=50.0%, DD=$26.57 |
| `moderate_1.50_2.50atr` | n=38, +2.133R, PF=1.175, win=68.4%, DD=$37.22 | n=7, -2.441R, PF=0.439, win=42.9%, DD=$37.22 |
| `deep_2.50_4.00atr` | n=28, +8.857R, PF=2.567, win=78.6%, DD=$18.92 | n=7, +2.470R, PF=3.08, win=85.7%, DD=$11.88 |
| `extreme_4.00_7.00atr` | n=10, -1.689R, PF=0.586, win=40.0%, DD=$27.21 | n=1, +0.821R, PF=None, win=100.0%, DD=$0.00 |
| `disorderly_7.00_12.00atr` | n=1, +0.031R, PF=None, win=100.0%, DD=$0.00 | n=0, +0.000R, PF=None, win=0.0%, DD=$0.00 |

## Robustness

- eligible nearby deep configurations: `3826`
- positive in train: `85.4%`
- positive in validation: `72.5%`
- positive in latest test: `75.2%`
- positive in all three slices: `51.1%`
- median latest-test result: `+0.949R` over `3` trades
- deep candidate uses `15` symbols; largest symbol share `16.0%`
- after removing the most frequent symbol: n=21, +7.579R, PF=3.112, win=81.0%, DD=$14.98

## Verdict

The shallow variant is rejected: it was positive in development but lost money in the latest chronological test. The very deepest/extreme sweeps also underperformed. The useful zone is bounded rather than monotonic: roughly 2.5-4 ATR and 1.5-2.75% flushes.

The broader deep candidate (2-5 ATR, 1.5-2.75%, strong liquidation percentile, Europe/US) is suitable for a separate Paper profile. It is not ready for Live: the full sample is still small and the final slice is not a globally untouched holdout.
