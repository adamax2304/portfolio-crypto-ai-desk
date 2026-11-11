# Crypto Recent Losing-Streak Audit (PART 2)

**Date:** 2026-06-17 · read-only · window 7d (focus last 3d). CSV: `STOP_WICK_REENTRY_STUDY.csv` (72 crypto losers).

## What happened
72 crypto losing (stopped) trades in 7d; **54 in the last 3 days, 100% LONG**. Crypto stops per UTC day:

| day | crypto stops | BTC day % |
|---|--:|--:|
| 06-11 | 3 | +3.44 |
| 06-12 | 7 | −0.07 |
| 06-13 | 2 | +1.38 |
| 06-14 | 7 | +2.00 |
| **06-15** | **27** | +0.89 |
| 06-16 | 10 | −0.99 |
| **06-17** | **16** | −0.96 (intraday −2.36%) |

Two distinct clusters, two different causes (see below).

## Per-loss classification (72 crypto losers)
| class | n | % |
|---|--:|--:|
| STOP_TOO_TIGHT_SHALLOW_BREACH (MAE −1.0…−1.25R) | 30 | 42% |
| VALID_STOP_NORMAL | 16 | 22% |
| STOP_AFTER_TP1_REACHED (hit ≥+1R then reversed) | 14 | 19% |
| ENTRY_TOO_EARLY_FAST_STOP (≤15min to stop) | 6 | 8% |
| VALID_STOP_BAD_SIGNAL (MAE ≤ −1.6R) | 4 | 6% |
| OVERNIGHT_CARRY_PROBLEM | 2 | 3% |

**61% (44/72) either reached TP1 first or were stopped by a shallow (<1.25R) dip.** Only ~6% were deep "bad signal" moves.

## Excursion profile (the key fact)
- **69%** of crypto losers reached **≥ +0.5R** favorable before stopping; **19%** reached **≥ +1.0R (TP1 level)**.
- **78%** had MAE in **(−1.5R, −1.0R]** — i.e. they were stopped by a dip that only just exceeded the −1R stop; **42%** barely (−1.0…−1.15R). Only **12%** had MAE ≤ −1.5R.
- Examples (last 3d): TAO +2.26R MFE → −1R stop; MEME +1.11R; GPS +1.15R; SOL +1.03R; FIL +1.14R; HMSTR +1.17R; ALLO +1.07R.

**Interpretation:** these are mostly **"had it, gave it back"** trades, not bad entries. Stops are tight relative to alt intraday volatility, and there is **no profit protection** — `config/signal_tracking.yaml: partial_exit_model.enabled = false`, no move-to-breakeven after +1R, and the conservative same-candle model marks a stop when one candle straddles both TP1 and stop. So a trade can touch +1R and still book a full −1R.

## Answers to PART-2 questions
- **Is this a normal series within edge?** Partly. crypto/intraday + swing are PF≈1.0 over 7d (breakeven), so the *system* isn't broken — but the **loss shape is fixable** (tight stops + no profit-taking) and the **06-16/06-17 cluster is a regime-lag problem** (longs into a falling BTC, see REGIME report).
- **Is the system longing the wrong regime?** On **06-15 (BTC +0.89%) the regime label was correct** — 27 stops there are alt whipsaw/over-trading, not regime. On **06-16/06-17 (BTC −1% to −2.4% intraday) the "bullish trend" label lagged** the turn → longs fired into risk-off. Mixed: half tight-stops, half regime-lag.
- **Expiry/stop/revalidation broken?** Not a code crash, but **no max-holding/EOD/next-session revalidation for *triggered* intraday trades** (see CARRYOVER report) and **no circuit breaker** (see DAILY_LOSS report).
- **Stops too tight?** Yes for crypto alts — 78% shallow-breach + 19% reached TP1. Counterfactual in `STOP_WICK_MANIPULATION_COUNTERFACTUAL.md`.
- **Add wick/re-entry logic?** Worth testing (counterfactual is positive-leaning) but **not urgent / not now** — profit-protection (move-to-BE / partial at TP1) is the higher-leverage, lower-risk change to validate first.

**Bottom line:** the recent crypto losses are **dominated by tight-stop / no-profit-protection mechanics (≈61% of losers) plus a 2-day regime-lag long cluster**, NOT by broken signals. Edge is intact (breakeven PF≈1.0); the leak is exit management + late-cycle long throttle.
