# TP3 Help / Hurt Classification (PART 7)

**Date:** 2026-06-23. From the 60d dataset. "Add-R" = TP3 contribution under production accounting (prod − capTP2). Confidence reflects sample + whether it survives the realistic hold model.

## TP3 HELPS (positive realized contribution where reached)
| cohort | n | TP3 reached | TP3 add-R | confidence | required condition |
|---|---|---|---|---|---|
| **crypto swing — narrative/RS momentum** | 89 | 16 | **+16R** | medium (n ok, TP3 reached often) | trend-aligned swing; the main TP3 engine |
| **crypto failed_bounce_short** | 29 | 9 | **+9R** | low-medium (small n, but positive even under hold→TP3 = +11.8R) | counter-bounce shorts in down/risk-off tape |
| crypto intraday — catalyst/momentum | 100 | 11 | +11R | low (mode net-negative overall; TP3 is upside but entries lose) | catalyst/continuation only |
| bearish-trend / risk-off **shorts** | ~20–40 | 5+ | + | low (small n) | trend-aligned shorts (regime down) |

Mechanism: in continuation/trend-aligned setups price runs to TP3 often enough that the extra R outweighs the rare give-back.

## TP3 HURTS — or is irrelevant (rarely reached; holding-for-it costs)
| cohort | n | TP3 reached | note |
|---|---|---|---|
| **stocks_intraday_rth_momentum** | 684 | 15 (2.2%) | TP3 almost never reached; hold→TP3 = −189R vs prod −18.7 → holding-through is ruinous |
| stocks_swing_watchlist_rs | 217 | 1 | TP3 effectively never reached |
| stocks_invest_watchlist_30d | 167 | 0 | never reached |
| crypto_scalp_momentum (shadow) | 118 | 0 | never reached (scalp shadow anyway) |
| **chop / range regime** | 165 | 3 | TP3 reached ~2% → cap at TP2 loses ≈0; TP3 is noise here |
| risk-on **shorts** / risk-off **longs** (counter-regime) | small | few | counter-trend rarely extends to TP3 |

Mechanism: mean-reverting / range / counter-regime price doesn't extend to TP3; "waiting" for it (hold model) bleeds give-backs, and even under the optimistic model TP3 adds ~nothing.

## TP3 UNKNOWN (insufficient evidence)
- Per-regime short/long splits inside small cohorts (risk-off longs, risk-on shorts, high-volatility n=3, transition n=5): **sample too small**.
- Any cohort where TP3 add-R is within ±2R of zero on n<30 → not actionable.
- Same-candle-ambiguous TP3 trades (handful) — order unknown.

## Net takeaway
TP3 is **not harmful as a recorded level** anywhere (it only adds or adds ~0). The real "hurt" is the **hold-for-far-target give-back**, concentrated in mean-reverting/stocks-momentum cohorts where TP3 is essentially unreachable — there the answer is "don't hold for TP3," i.e. take profit earlier, which is a **stop/partial** question, not a TP-count question. The only cohorts that genuinely *earn* TP3 are **crypto swing-narrative** and **crypto failed-bounce shorts** (trend/continuation), plus catalyst intraday.

## Verdict
`TP3_CONDITION_MAP_READY`
