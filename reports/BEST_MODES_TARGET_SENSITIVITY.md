# Best Existing Modes - Target Sensitivity

Generated: `2026-09-29T16:48:09.205686+00:00`

Research only. Recorded entries and initial stops are frozen. Every variant uses the same 33/33/34 exits, stop-first candles, breakeven after TP1, +0.5R lock after TP2, time exit, fees, and slippage. The test therefore isolates target placement.

## stocks_intraday_BREAKOUT_CONTINUATION_new_logic_shadow

Coverage: `51/55` paths; missing `4`.

| Variant | Median target R | Train | Validation | Latest test | All |
|---|---:|---:|---:|---:|---:|
| `CURRENT_STORED` | `[1.052, 2.075, 3.745]` | n=30, +20.97R, PF=6.605, win=80.0%, DD=1.48R | n=12, +4.62R, PF=10.68, win=75.0%, DD=0.27R | n=9, +8.78R, PF=9.138, win=88.9%, DD=1.08R | n=51, +34.37R, PF=7.488, win=80.4%, DD=1.48R |
| `FIXED_R_1_2_3` | `[1.0, 2.0, 3.0]` | n=30, +20.19R, PF=6.586, win=80.0%, DD=1.48R | n=12, +7.16R, PF=27.217, win=83.3%, DD=0.27R | n=9, +8.07R, PF=8.475, win=88.9%, DD=1.08R | n=51, +35.41R, PF=8.13, win=82.4%, DD=1.48R |
| `ATR_1X_2X_3X` | `[0.465, 0.929, 1.394]` | n=30, +16.03R, PF=7.526, win=90.0%, DD=1.26R | n=12, +6.53R, PF=256.299, win=83.3%, DD=0.03R | n=9, +3.73R, PF=4.446, win=77.8%, DD=1.08R | n=51, +26.29R, PF=8.377, win=86.3%, DD=1.26R |
| `STRUCTURE_ENGINE` | `[0.929, 1.79, 2.224]` | n=30, +21.43R, PF=6.729, win=80.0%, DD=1.48R | n=12, +4.92R, PF=11.318, win=75.0%, DD=0.27R | n=9, +7.96R, PF=8.377, win=88.9%, DD=1.08R | n=51, +34.31R, PF=7.478, win=80.4%, DD=1.48R |
| `HYBRID_STRUCTURE_BOUNDED` | `[0.929, 1.569, 3.0]` | n=30, +21.26R, PF=9.4, win=83.3%, DD=1.48R | n=12, +6.92R, PF=26.322, win=83.3%, DD=0.27R | n=9, +8.60R, PF=8.966, win=88.9%, DD=1.08R | n=51, +36.77R, PF=10.47, win=84.3%, DD=1.48R |

## crypto_intraday_BREAKOUT_CONTINUATION_paper_v1

Coverage: `17/41` paths; missing `24`.

| Variant | Median target R | Train | Validation | Latest test | All |
|---|---:|---:|---:|---:|---:|
| `CURRENT_STORED` | `[0.829, 1.503, 2.721]` | n=10, -1.75R, PF=0.682, win=50.0%, DD=2.54R | n=3, -0.53R, PF=0.625, win=33.3%, DD=1.42R | n=4, -1.13R, PF=0.393, win=50.0%, DD=1.13R | n=17, -3.41R, PF=0.611, win=47.1%, DD=3.41R |
| `FIXED_R_1_2_3` | `[1.0, 2.0, 3.0]` | n=10, -1.60R, PF=0.709, win=50.0%, DD=2.65R | n=3, +0.56R, PF=1.394, win=33.3%, DD=1.42R | n=4, -4.03R, PF=0.0, win=0.0%, DD=4.03R | n=17, -5.07R, PF=0.537, win=35.3%, DD=5.45R |
| `ATR_1X_2X_3X` | `[0.407, 0.814, 1.221]` | n=10, -0.40R, PF=0.822, win=80.0%, DD=1.18R | n=3, -0.12R, PF=0.891, win=66.7%, DD=1.06R | n=4, -0.50R, PF=0.516, win=75.0%, DD=1.04R | n=17, -1.02R, PF=0.766, win=76.5%, DD=2.33R |
| `STRUCTURE_ENGINE` | `[0.822, 1.173, 1.504]` | n=10, -0.32R, PF=0.941, win=50.0%, DD=2.73R | n=3, -0.30R, PF=0.79, win=33.3%, DD=1.42R | n=4, -1.13R, PF=0.392, win=50.0%, DD=1.13R | n=17, -1.75R, PF=0.8, win=47.1%, DD=2.73R |
| `HYBRID_STRUCTURE_BOUNDED` | `[0.822, 1.5, 3.0]` | n=10, -1.33R, PF=0.757, win=50.0%, DD=2.32R | n=3, +0.21R, PF=1.148, win=33.3%, DD=1.42R | n=4, -1.51R, PF=0.192, win=50.0%, DD=1.51R | n=17, -2.63R, PF=0.7, win=47.1%, DD=2.93R |

## Constraint

These are local-path replays, not a new untouched market sample. Missing paths are disclosed and no result is promoted automatically. Forward Paper A/B remains the final check.
