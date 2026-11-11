# Signal Edge Independent of Exits (PART 6)

**Date:** 2026-06-23. The key question: do the *signals* (entries) have edge regardless of how we exit? Actionable book, ~30d, n=584.

## The 9 answers
1. **Do signals reach meaningful MFE often enough?** Yes — **53.8% reach +0.5R**, 28.3% reach +1R, mean MFE +0.88R, median +0.56R. Favorable excursion exists.
2. **Is MFE distribution positive but exits poor?** **Yes.** MFE is positive (mean +0.88R) yet realistic capture is −96…−137R → the excursion is real but **not captured** (no early protective stop). This is the dominant story.
3. **Do most signals stop before any meaningful MFE?** No — only **10.8% stop-first** and **6.5% never positive**. Most trades *do* move favorably first.
4. **Is edge only in a few cohorts?** Edge *under simple exits* is concentrated (failed-bounce-short, risk-off shorts). Under **Model F (early protection)** edge is **broad** (all regimes, both directions positive).
5. **Are stocks signals bad?** No — stocks_intraday_momentum is −17R under first-TP-close but **+23.7R under Model F** (R/trade +0.07). Thin but salvageable.
6. **Are crypto signals bad?** Mixed — crypto_intraday_catalyst is the worst actionable cohort (chase longs), but crypto_swing (+29R F) and failed-bounce-short (+19R F) are the best. Crypto-as-a-whole positive under F.
7. **Are shorts better than longs?** **Yes, dramatically.** Shorts +27R (Model F) / +21R recorded on n=66; longs −105R under first-TP-close but +47R under Model F. Shorts are the higher-quality, more robust edge.
8. **Are catalyst-supported signals better?** Slightly — catalyst-yes positive under more models (+3.5R even +0.5lock) vs catalyst-no needing Model F. But catalyst n is small (55).
9. **Is the system mostly noise?** **No.** With 6.5% never-positive and 54% reaching +0.5R, the signals carry information. The edge is **thin** (MFE/MAE ≈ 1.06) and was being **destroyed by the exit policy**, not absent.

## Threshold test (PART-6 rubric)
| condition | met? | implies |
|---|---|---|
| >50% reach +0.5R before stop but final realistic R negative | **YES** (53.8%, realistic negative) | **risk-management issue** |
| <25% reach +0.5R and stop-first dominates | no (54% / 11%) | not a pure signal-quality failure |
| only specific cohorts reach +1R/TP2 | partly | filter/cohort issue (kill crypto_intraday_catalyst) |
| MFE good but giveback high | partly (8.6% giveback; 17.6% stopped-after-0.6R) | **exit issue** |
| MFE poor and MAE high | **no** (MFE +0.88 ≈ MAE −0.83) | not primarily an entry/signal failure |

## Diagnosis
**The signals have a thin but real edge that the current exit policy throws away.** Favorable excursion (+0.5R) happens in the majority of trades but is unprotected and given back to a fixed stop. The binding constraint is **risk management (early protection), with a secondary cohort filter** (drop chase-longs), not a fundamental signal failure. Caveat: the edge is thin and the evidence is a 30-day single-epoch hindsight replay — real-world thin edges are fragile to costs/slippage and regime change.

## Verdict
`SIGNAL_EDGE_DIAGNOSIS_READY` — signals carry thin-but-real edge; current exits destroy it; fixable mainly via risk management (Model F) + one cohort filter.
