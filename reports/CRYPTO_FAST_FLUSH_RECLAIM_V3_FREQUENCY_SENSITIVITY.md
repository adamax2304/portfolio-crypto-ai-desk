# Crypto Fast Flush Reclaim v3 - Frequency Sensitivity

Generated: `2026-09-28T22:58:03Z`

This analysis explains the low trade count in the original strict FAST profile and defines the parallel BALANCED Paper profile. It is a sensitivity study, not a fresh holdout proof: the earlier holdout had already been inspected before BALANCED was created.

## Historical funnel

Usable point-in-time replay period: approximately 21 days.

| Stage | Raw FAST candidates | Cascade-adjusted |
|---|---:|---:|
| Confirmed reclaim with valid geometry | 465 | 214 |
| US session | 260 | 94 |
| ATR range | 179 | 74 |
| Flush percent range | 140 | 61 |
| RVOL and liquidation percentile | 139 | 61 |
| OI range | 96 | 40 |
| Stop distance 1.0%-1.5% | 30 | 20 |

The system detected many flush/reclaim events. The strict session and stop-distance gates caused most of the final reduction.

## Sensitivity result

| Variant | Cascade-adjusted trades | Raw signals | Net | PF | Win rate | Max DD |
|---|---:|---:|---:|---:|---:|---:|
| STRICT FAST | 20 | 30 | +9.66R | 4.93 | 85.0% | $11.94 |
| BALANCED FAST | 45 | 74 | +7.20R | 1.54 | 71.1% | $25.26 |
| BROAD / weak gates | 152 | 297 | -8.21R | 0.87 | 61.8% | $110.99 |

BALANCED produced about 15 independent opportunities or 25 raw signals per week. Broad relaxation reached dozens of independent entries per week but lost money after modeled costs.

## Parallel Paper definitions

STRICT keeps:

- US session only;
- OI decrease of 0.50%-3.00%;
- stop distance of 1.00%-1.50%.

BALANCED changes only:

- Europe and US sessions;
- OI decrease of 0.25%-3.00%;
- stop distance of 0.75%-1.50%.

All other setup, confirmation, exit, cost and fixed-risk mechanics remain identical. This isolates the frequency/quality trade-off.

## Decision rule

Do not combine the profiles and do not promote either from this sensitivity study. Compare them after at least 28 forward days and 30 clean closed trades per profile. Primary comparison: net R, PF, maximum drawdown, cost per trade, simultaneous-cascade concentration and performance by session.
