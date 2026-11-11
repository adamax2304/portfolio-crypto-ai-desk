# Crypto Profit-Protection — Full Counterfactual incl. Winners (PART 4)

**Date:** 2026-06-17 · **Mode:** measurement only. **Nothing enabled. `partial_exit_model.enabled` stays false.**
**CSV:** `CRYPTO_PROFIT_PROTECTION_FULL_COUNTERFACTUAL.csv` (per-trade, all 99 closed crypto intraday/swing trades incl. winners).
**Verdict:** **DO_NOT_ENABLE** in this stage. The estimate is favorable but rests on MFE/MAE, which cannot prove it. Re-run on tick-level path data before any change.

## Population
99 closed crypto intraday/swing trades over the 7d window (winners **and** losers included, per spec). Current net realized = **−2.0R**.

## Variants modeled (MFE/MAE estimate)
| Variant | Rule | Net R (est.) | Δ vs current |
|---|---|---|---|
| A | Current (as-traded) | **−2.0R** | — |
| B | Move stop to BE after **+0.5R** | **+43.0R** | +45.0R |
| C | Move stop to BE after **+1.0R** | **+10.0R** | +12.0R |
| D | Partial 50% at **+1R**, BE on remainder | **+16.0R** | +18.0R |

Supporting counts: trades that touched **+1R** (max winners clippable by a BE-after-1R rule) = **34**; losers "saved" to BE by the +1R rule = **12**.

## ⚠️ Limitations — why these numbers are optimistic upper bounds (read before trusting)
1. **No intra-trade path order.** MFE/MAE give the best and worst excursions but **not their sequence**. A "BE after +0.5R" estimate assumes *every* trade that ever ticked +0.5R would have locked BE before reversing. In reality many of those whipsaw: they tag +0.5R, pull back through BE (stopping the trade at 0R), then run — the model credits 0R but the as-traded trade may have gone on to +1R or to −1R. So Variant B's **+43R is a hard upper bound**, almost certainly overstated.
2. **Winners clipped is under-counted.** The model only flags winners that *touched +1R*; a BE/trailing stop also clips winners that dipped to BE mid-trade before running — that dip is invisible in MFE/MAE. So real winner-clipping ≥ the 34 flagged.
3. **+0.5R is inside typical crypto noise.** A BE trigger at +0.5R on volatile alts will be hit-and-reversed frequently; the +43R figure is the least trustworthy of the four.
4. **Variant C (+1R BE) is the most defensible** of the set: +1R is a meaningful move, fewer false BE triggers, estimate +10R. Even so it's an upper bound.

## Honest read
- Direction of effect is plausible (the recent losses are exit-management, not bad entries — consistent with prior audit: 78% of crypto losers shallow-breached at −1..−1.5R MAE; 69% reached +0.5R; 19% reached +1R).
- But **magnitude is unreliable** from MFE/MAE alone. The +43R/+0.5R number should be treated as marketing, not a forecast.

## Recommendation
- **Do NOT enable** BE/partial/trailing in this stage.
- **Next (measurement, not enabling):** re-run the counterfactual on **1m OHLCV path replay** (data exists in `data/raw/ohlcv/.../1m/`) so BE/partial triggers respect actual sequence and BE-stop whipsaw is modeled. Compare net R + profit factor incl. all winners.
- Only if the **path-aware** replay is net-positive incl. winners → discuss enabling the already-present `partial_exit_model` (still paper, still your explicit approval).
