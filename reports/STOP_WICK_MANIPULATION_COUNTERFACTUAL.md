# Stop / Wick / Manipulation Counterfactual (PART 4)

**Date:** 2026-06-17 · read-only · **counterfactual only — nothing implemented.**
CSV: `STOP_WICK_MANIPULATION_COUNTERFACTUAL.csv` (per crypto loser: survives-1.25×, survives-1.5×, reached-TP1, BE-after-TP1 R, partial-0.5@TP1 R).

## Method
Computed from the tracker's already-stored `max_adverse_excursion_r` (MAE) and `max_favorable_excursion_r` (MFE) per trade — the real reconciled excursions, full sample (no sampling). A loser "survives a wider stop" if its MAE never reached the wider level; "reached TP1" if MFE ≥ +1.0R.

## Crypto (72 losers)
| metric | value |
|---|--:|
| reached ≥ +1.0R (TP1) before stop | 14 (19%) |
| reached ≥ +0.5R before stop | 50 (69%) |
| MAE in (−1.25R, −1.0R] — survives a 1.25× stop | 30 (42%) |
| MAE in (−1.5R, −1.0R] — survives a 1.5× stop | 56 (78%) |
| MAE ≤ −1.5R — genuine adverse move | 9 (12%) |

**Counterfactual sumR on the losers only:**
| variant | sumR (losers) | Δ vs current |
|---|--:|--:|
| current (−1R each) | −72 | — |
| move stop → breakeven after +1R reached | −58 | **+14** |
| take 0.5 size at TP1, rest → BE | −51 | **+21** |
| 1.5× stop (survivors no longer stopped) | up to **+56 trades survive** | not P&L-closed (need fwd path) |

## Stocks (53 losers) — different problem
reached TP1 **0%**, reached +0.5R **15%**, shallow-breach 66%, deep 2%. **Profit-protection does NOT help stocks** (they rarely get into profit) — stocks losses are weak-follow-through / entry-timing, not wick-outs.

## Read
- **Crypto: systemic, fixable.** ~61% of losers either touched TP1 or were stopped by a <1.25R dip. A **move-to-BE after +1R** and/or **partial at TP1** would have turned ~14–21R of the loss column toward flat — *gross on losers*. **Caveat:** these rules also clip some winners (a trade that dips to BE after +1R then runs to TP2/TP3 is cut), so the **net** effect needs a full counterfactual that re-prices the 64 winners too — do that before changing anything.
- **Wider stop (1.5×)** lets 78% of current losers survive, but a wider stop also (a) increases per-loss size on the 12% genuine movers and (b) changes which trades are wins — net edge unknown without a forward walk. **Higher risk than profit-protection; lower priority.**
- **Manipulation/wick:** the shallow-breach concentration (42% within −1.0…−1.15R) is consistent with **stop-hunt wicks on thin alts**, but proving intent requires intrabar/tick data the cache doesn't hold at 1m for all alts. Treat as "tight stop in high-vol alt," not provable manipulation.
- **Re-entry-on-reclaim:** plausible given the reclaim pattern, but adds complexity and chase risk → **research-only**, after profit-protection is validated.

## Verdict
**Problem is systemic for crypto (exit management), not isolated; wider stop helps the sample but is risk-ambiguous net; profit-protection (BE-after-TP1 / partial-TP1) is the safest high-leverage candidate — validate with a winners-inclusive counterfactual before any change.** Stocks need a separate fix (signal quality / entry), not stop widening.
