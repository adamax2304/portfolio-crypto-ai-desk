# Signal vs Risk — Final Diagnosis (PART 7)

**Date:** 2026-06-23. Strict decision matrix. Actionable book, ~30d, n=584. **Relative-leaning evidence; no production change.**

## Decision matrix
| candidate verdict | fits evidence? | why |
|---|---|---|
| SIGNALS_BAD_RISK_CANNOT_SAVE | ✗ | only 6.5% never-positive, 54% reach +0.5R; risk (Model F) flips book to +74R |
| SIGNALS_OK_RISK_BAD | partial | risk is the binding constraint, but signal edge is *thin* (MFE/MAE 1.06), not "OK/strong" |
| **SIGNALS_MIXED_RISK_CAN_HELP** | ✓ **primary** | thin-but-real edge; the right risk model (early MFE protection) turns it positive |
| ONLY_SPECIFIC_COHORTS_HAVE_EDGE | ✓ (secondary) | under *simple* exits only failed-bounce-short / risk-off shorts are positive |
| SYSTEM_NOT_VIABLE_CURRENTLY | ✓ **as-is** | with the **current** production exits (touch / fixed-stop) the realistic book is −96…−137R |
| **SYSTEM_HAS_VIABLE_CORE_WITH_FILTERS_AND_RISK** | ✓ **conditional** | with Model F + drop crypto_intraday_catalyst → +72R, PF 1.43, not symbol-dependent |

## Chosen verdict (two-part, honest)
1. **As currently run (no risk change): SYSTEM_NOT_VIABLE_CURRENTLY** — recorded +2R is touch-based illusion; realistic is strongly negative.
2. **With risk-management change: SIGNALS_MIXED_RISK_CAN_HELP → SYSTEM_HAS_VIABLE_CORE_WITH_FILTERS_AND_RISK** — a viable core exists *conditional on* adopting early MFE-armed protection (Model F) + filtering chase-longs.

## Evidence / confidence per cohort
| cohort | sample | exp. R after Model F | confidence | action |
|---|---|---|---|---|
| crypto_failed_bounce_short | n=31 | +0.62/trade | medium (positive even under simple exits) | KEEP — safest core |
| crypto_swing_narrative_rs | n=89 | +0.33/trade | medium | KEEP (with Model F) |
| stocks_intraday_rth_momentum | n=364 | +0.07/trade | low-medium (thin per-trade; large n) | KEEP under Model F + monitor |
| risk-off / bearish-trend shorts | n~40 | +0.1–0.4/trade | low (small n) | KEEP — trend-aligned shorts |
| crypto_intraday_catalyst_or_momentum | n=100 | +0.02/trade | low (worst, chase longs) | **SHADOW / filter** |
| crypto scalp, stocks swing/invest, C-tier | shadow | negative all models | n/a | **stay shadow** |

## Overall confidence
**MODERATE, with material caveats:** 30-day single epoch (bullish/chop), MFE-trigger hindsight reconstruction (no bear regime, no cost/slippage), per-cohort n small for the strongest names. The result is strong enough to justify a **paper-shadow validation**, not a production switch.

## Verdict
`SIGNAL_VS_RISK_DECISION_READY` — **risk-management is the binding constraint; a viable core exists conditional on Model F + cohort filter; not viable under current exits; evidence supports paper-shadow validation, not production.**
