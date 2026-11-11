# Signal Quality vs Risk Management — Diagnosis (PART 2)

**Date:** 2026-06-23. Separates "is the entry good?" (favorable excursion) from "is the exit good?" (capture of that excursion). Actionable book, ~30d, n=584.

## Signal-quality metrics (ACTIONABLE n=584)
| metric | value | reading |
|---|---|---|
| MFE ≥ 0.5R | **53.8%** | over half reach +0.5R favorable — **not noise** |
| MFE ≥ 1R | 28.3% | |
| MFE ≥ 2R | 12.0% | |
| MFE ≥ 3R | 6.8% | |
| never positive (MFE ≤ 0.05R) | **6.5%** | almost every trade shows *some* favorable move |
| stop-first (stopped, MFE < 0.2R) | **10.8%** | only ~11% go straight to the stop |
| mean MFE | **+0.88R** | |
| median MFE | +0.56R | |
| mean MAE | **−0.83R** | |
| MFE/MAE ratio | ~1.06 | favorable barely exceeds adverse → thin raw edge |
| reach TP1 | 22.8% | TP1 set ~1R+ away, so most favorable excursion never reaches it |

## Risk-management metrics
| metric | value |
|---|---|
| recorded (touch) captured R | +2R |
| realistic capture (first-TP close) | −104.8R |
| realistic capture (hold-to-TP3) | −136.8R |
| **stopped trades that reached ≥0.6R favorable FIRST** | **103 (17.6%)** ← give-back to the fixed stop |
| giveback (MFE≥1R then stop) | 8.6% |
| MFE-armed protection capture (Model F) | **+74.1R** |

## The central diagnostic
- **Trades reach +0.5R favorable 53.8% of the time, but only 22.8% reach TP1.** The favorable move overwhelmingly dies in the **+0.5R → TP1 zone**, where the system has **no protective stop** — the stop stays at the original invalidation, so a +0.6R pop that reverses books a **full −1R**.
- **17.6% of actionable trades are stopped *after* having been ≥0.6R in profit.** Capturing/protecting those alone (move stop to BE at +0.6R favorable) flips the realistic book from −96…−137R to **+74R** (Model F, PART 4).
- Per the PART-6 thresholds: **">50% reach +0.5R but realistic R negative → risk-management issue."** That condition holds. The dominant problem is **risk management (no early protection), not signal quality.** Signal quality is *thin* (MFE/MAE ≈ 1.06) but real.

## Cohort classification
| cohort | class | why |
|---|---|---|
| crypto_failed_bounce_short | **GOOD_SIGNAL_BAD_EXIT** | MFE mean 1.46R, +13R even under +0.5lock, +19R under Model F |
| crypto_swing_narrative_rs | **GOOD_SIGNAL_BAD_EXIT** | MFE≥1R 42.7%; −25R first-TP-close → **+29R under Model F** |
| stocks_intraday_rth_momentum | **MIXED_SIGNAL_NEEDS_FILTER** | −17R first-TP-close → +24R Model F; many give-back longs in bullish tape |
| risk_off / bearish-trend shorts | **GOOD_SIGNAL_BAD_EXIT (low n)** | +5…+12R realistic, trend-aligned |
| crypto_intraday_catalyst_or_momentum | **MIXED→KILL/SHADOW** | worst actionable (−42.8R +0.5lock; only +2R Model F) — chase longs |
| crypto scalp / stocks swing-invest / C-tier (shadow) | **KILL_OR_SHADOW** | negative under every model; stay shadow |
| risk-off-longs / high-vol / transition | **PROMISING_BUT_LOW_SAMPLE** | n<10, not actionable evidence |

## Verdict
`SIGNAL_VS_RISK_CAUSE_SPLIT_COMPLETE` — **primary cause = risk management** (no early protective stop in the +0.5R→TP1 zone); signal quality is thin-but-real, not noise.
