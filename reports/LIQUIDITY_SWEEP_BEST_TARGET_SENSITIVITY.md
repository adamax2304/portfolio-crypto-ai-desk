# Best New Liquidity-Reclaim Profiles - Target Sensitivity

Generated: `2026-09-29T17:08:04.178625+00:00`

Only the best new liquidity-reclaim profile in each asset class is tested. Entries, initial structural stops, confirmation, 70/30 exits, breakeven after TP1, holding time, fees, slippage, stop-first ambiguity handling, and the original chronological split are frozen.

## crypto_FAST_1M_RECLAIM

Selected/reconstructed: `20/20`; baseline max delta `0.0`.

| Target policy | Coverage | Median TP R | Train | Holdout | All |
|---|---:|---:|---:|---:|---:|
| `BASELINE_R_080_135` | 20/20 | `[0.8, 1.35]` | n=15, +8.054R, PF=7.109, win=86.7%, DD=$11.94 | n=5, +1.607R, PF=2.408, win=80.0%, DD=$11.42 | n=20, +9.661R, PF=4.927, win=85.0%, DD=$11.94 |
| `EXTENDED_R_100_175` | 20/20 | `[1.0, 1.75]` | n=15, +9.458R, PF=7.972, win=80.0%, DD=$11.94 | n=5, +2.407R, PF=3.108, win=80.0%, DD=$11.42 | n=20, +11.865R, PF=5.749, win=80.0%, DD=$11.94 |
| `ATR_1X_2X` | 20/20 | `[0.715, 1.43]` | n=15, +6.860R, PF=6.057, win=80.0%, DD=$11.94 | n=5, +2.946R, PF=None, win=100.0%, DD=$0.00 | n=20, +9.806R, PF=8.229, win=85.0%, DD=$11.94 |
| `PURE_STRUCTURE` | 16/20 | `[0.968, 1.216]` | n=11, +6.144R, PF=5.661, win=81.8%, DD=$13.18 | n=5, +3.172R, PF=3.778, win=80.0%, DD=$11.42 | n=16, +9.316R, PF=4.787, win=81.2%, DD=$13.18 |
| `BOUNDED_STRUCTURE` | 20/20 | `[1.0, 1.232]` | n=15, +8.364R, PF=7.344, win=86.7%, DD=$11.94 | n=5, +2.248R, PF=2.969, win=80.0%, DD=$11.42 | n=20, +10.613R, PF=5.314, win=85.0%, DD=$11.94 |
| `BOUNDED_VWAP_PREVIOUS_CLOSE` | 20/20 | `[0.815, 1.1]` | n=15, +7.135R, PF=6.26, win=80.0%, DD=$11.94 | n=5, +1.457R, PF=2.276, win=80.0%, DD=$11.42 | n=20, +8.593R, PF=4.439, win=80.0%, DD=$11.94 |

## stocks_HELD_1M_RECLAIM

Selected/reconstructed: `33/33`; baseline max delta `0.0`.

| Target policy | Coverage | Median TP R | Train | Holdout | All |
|---|---:|---:|---:|---:|---:|
| `BASELINE_R_080_135` | 33/33 | `[0.8, 1.35]` | n=18, +5.945R, PF=3.531, win=77.8%, DD=$11.86 | n=15, +1.448R, PF=1.34, win=66.7%, DD=$16.34 | n=33, +7.393R, PF=2.118, win=72.7%, DD=$16.34 |
| `EXTENDED_R_100_175` | 33/33 | `[1.0, 1.75]` | n=18, +5.952R, PF=3.431, win=72.2%, DD=$12.00 | n=15, +1.579R, PF=1.37, win=66.7%, DD=$16.34 | n=33, +7.531R, PF=2.122, win=69.7%, DD=$16.34 |
| `ATR_1X_2X` | 33/33 | `[0.511, 1.022]` | n=18, +4.689R, PF=2.997, win=77.8%, DD=$11.86 | n=15, +0.517R, PF=1.121, win=66.7%, DD=$16.41 | n=33, +5.206R, PF=1.788, win=72.7%, DD=$16.41 |
| `PURE_STRUCTURE` | 30/33 | `[1.032, 1.391]` | n=15, +7.067R, PF=6.611, win=80.0%, DD=$11.00 | n=15, +1.759R, PF=1.413, win=66.7%, DD=$16.34 | n=30, +8.825R, PF=2.598, win=73.3%, DD=$16.34 |
| `BOUNDED_STRUCTURE` | 33/33 | `[1.0, 1.261]` | n=18, +5.651R, PF=3.308, win=72.2%, DD=$12.00 | n=15, +1.811R, PF=1.425, win=66.7%, DD=$16.34 | n=33, +7.462R, PF=2.112, win=69.7%, DD=$16.34 |
| `BOUNDED_VWAP_PREVIOUS_CLOSE` | 33/33 | `[0.8, 1.1]` | n=18, +5.246R, PF=3.233, win=77.8%, DD=$11.86 | n=15, +1.201R, PF=1.282, win=66.7%, DD=$16.34 | n=33, +6.447R, PF=1.975, win=72.7%, DD=$16.34 |

## Boundary

This is post-hoc target sensitivity on previously inspected history, not a fresh holdout. A winning alternative must receive a separate Paper profile before any promotion decision.
