# Reclaim Variant Backtests

Generated: `2026-10-04T13:28:34.484125+00:00`

Research only: no order submission. All data is historical and replayed point-in-time where available.
Selection uses training data only; validation and test are reported separately.

## Crypto FAST Europe

Period: `2026-09-07T22:40:00+00:00` to `2026-09-28T20:45:00+00:00`; base replay rows=465; distinct source events=465.

| Variant | Train | Validation | Test | All |
|---|---:|---:|---:|---:|
| `us_strict_control` | n=13, +6.45R, PF=5.89 | n=3, +0.47R, PF=1.408 | n=4, +2.75R, PF=None | n=20, +9.66R, PF=4.927 |
| `europe_strict` | n=0, +0.00R, PF=None | n=1, +0.11R, PF=None | n=1, -0.63R, PF=0.0 | n=2, -0.53R, PF=0.168 |
| `europe_moderate` | n=2, +1.35R, PF=None | n=4, +1.99R, PF=None | n=2, -0.09R, PF=0.865 | n=8, +3.25R, PF=6.155 |
| `europe_medium_deep` | n=2, +0.87R, PF=None | n=3, +1.65R, PF=None | n=1, +0.55R, PF=None | n=6, +3.06R, PF=None |

## Stocks HELD stop buffer

Period: `2026-08-04T14:15:00+00:00` to `2026-10-01T14:15:00+00:00`; source clean independent rows=48; reconstructed=48; paired across all buffers=48.
Training-only top candidate: `buffer_0.15_atr`.

| Buffer | Train | Validation | Test | All | Paired common | Test exits | Geometry rejects |
|---:|---:|---:|---:|---:|---|---:|---:|
| 0.10 ATR | n=25, +5.80R, PF=2.226 | n=10, +2.04R, PF=1.977 | n=13, -2.00R, PF=0.579 | n=48, +5.84R, PF=1.504 | n=48, +5.84R, PF=1.504 | tp2:2, breakeven_stop:2, time_exit:7, original_stop:2 | 0 |
| 0.15 ATR | n=25, +5.82R, PF=2.24 | n=10, +1.78R, PF=1.861 | n=13, -1.93R, PF=0.589 | n=48, +5.68R, PF=1.495 | n=48, +5.68R, PF=1.495 | tp2:2, breakeven_stop:2, time_exit:7, original_stop:2 | 0 |
| 0.20 ATR | n=25, +5.45R, PF=2.168 | n=10, +1.80R, PF=1.878 | n=13, -1.86R, PF=0.599 | n=48, +5.39R, PF=1.475 | n=48, +5.39R, PF=1.475 | tp2:2, breakeven_stop:2, time_exit:7, original_stop:2 | 0 |
| 0.25 ATR | n=25, +5.47R, PF=2.182 | n=10, +1.81R, PF=1.895 | n=13, -1.79R, PF=0.609 | n=48, +5.50R, PF=1.49 | n=48, +5.50R, PF=1.49 | tp2:2, breakeven_stop:2, time_exit:7, original_stop:2 | 0 |
| 0.30 ATR | n=25, +5.18R, PF=2.126 | n=10, +1.83R, PF=1.911 | n=13, -1.49R, PF=0.67 | n=48, +5.52R, PF=1.497 | n=48, +5.52R, PF=1.497 | tp2:2, breakeven_stop:1, time_exit:8, original_stop:2 | 0 |
| 0.40 ATR | n=25, +4.70R, PF=2.024 | n=10, +1.84R, PF=1.932 | n=13, -1.38R, PF=0.686 | n=48, +5.15R, PF=1.47 | n=48, +5.15R, PF=1.47 | tp2:2, breakeven_stop:1, time_exit:8, original_stop:2 | 0 |

## Paper Decision

Crypto Europe: run the moderate profile as exploratory Paper because it produced 8 historical trades (+3.25R), but its untouched test is only n=2 / -0.09R. This is not proven edge.
Stocks HELD: run the 0.15 ATR buffer as the training-only selected paired Paper variant against the 0.10 ATR baseline. Validation is weaker and test remains negative (-1.93R); full-sample PF is 1.504 vs 1.495. This is not a proven improvement or an optimal stop.

## Decision Boundary

A best in-sample setting is not called optimal if validation/test are weak or too small. A positive Paper-only result is not a Live promotion; forward Paper evidence and governance gates remain required.
