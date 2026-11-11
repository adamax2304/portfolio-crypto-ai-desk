# Current R Overstatement Analysis (PART 4) — KEY REPORT

**Date:** 2026-06-23. Read-only. Net R by execution model, per book & window. **This is the core finding.**

## Net R by model — ACTIONABLE (Operator/Paper) book
| model | 60d (=30d, n=583) | 7d | 48h | today |
|---|---|---|---|---|
| **recorded `final_r` (DB)** | **+2.0** | −10.0 | +6.0 | 0.0 |
| M0 legacy touch (reconstructed) | +6.2 | −5.0 | +8.8 | +0.4 |
| **M1 first-TP full close** | **−104.8** | −36.0 | −7.2 | +0.4 |
| **M2 hold-to-TP3 fixed stop** | **−136.8** | −28.2 | −4.6 | −2.0 |
| M3 TP1→BE | −109.8 | −21.2 | −1.6 | −2.0 |
| M4 TP1→+0.2R | −104.4 | −19.8 | −1.0 | −2.0 |
| M5 partial50+BE runner | −107.3 | −28.6 | −4.4 | −0.8 |
| M6 partial 1/3·1/3·runner | −103.8 | −28.6 | −4.3 | −1.2 |
| dC +0.5R lock after TP1 | **−96.3** (best realistic) | −17.7 | −0.1 | −2.0 |

## Net R by model — SHADOW book (separate; C-tier/scalp/stocks-swing-invest)
| recorded | M0 | M1 first-TP | M2 hold-TP3 | M5 partial |
|---|---|---|---|---|
| −116.0 | −125.5 | −155.8 | −268.3 | −204.6 |
Shadow is deeply negative under every model — consistent with it being the non-actionable drag.

## Overstatement — ACTIONABLE, 60d
| question | answer |
|---|---|
| **TP1→stop counted as profit by current model** | **27 trades** |
| TP2→stop counted as profit by current model | 8 trades |
| trades current calls WIN but hold-TP3 calls LOSS | **27** (R overstated **+64.5R** on these alone) |
| trades where current_R − hold_R ≥ 1R | **88** |
| trades where current == realistic (match) | **495 / 583** (85%) |
| **Total book overstatement: M0 +6.2 vs hold-TP3 −136.8** | **≈ +143R** |
| vs first-TP-close (−104.8) | ≈ +111R |
| vs partial50+BE (−107.3) | ≈ +114R |
| vs best realistic dC (−96.3) | ≈ +102R |

## The four required answers
1. **If TP1 touched then stop, how many did current count as profit?** **27** (actionable; +8 more at TP2→stop).
2. **By how much is historical performance overstated?** On the actionable book over ~30–60d, recorded ≈ **+2R** but realistic execution is **−96R to −137R** → overstatement of **roughly +100 to +143R** depending on the assumed exit. (Most trades match; the gap comes from ~88 give-back/clip trades.)
3. **Is the system still profitable under realistic models?** **No.** It is breakeven-to-slightly-positive ONLY under the optimistic touch model. Under *every* realistic single-position model (first-TP-close, hold-TP3, BE, profit-lock, partial) the actionable book is **net negative** (−96 to −137R). The shadow book is far worse.
4. **Which model is closest to intended execution?** Ambiguous — the desk has **no real order execution**, so it depends on operator behavior: if you'd exit fully at TP1, that's M1 (−105R); if you'd ride to TP3, that's M2 (−137R); BE/partial sit between. None reproduce the recorded +2R, which assumes the unrealistic "captured the best TP every time."

## Why the system looks positive but isn't
Win rate is low (133 TP1 vs 276 stops ≈ 32% of resolved). The recorded +2R exists only because TP2/TP3 multiples are banked on winners **without** ever paying the give-back when those same trades later reversed. Remove that optimism and the negative expectancy of the entries shows through.

## Verdict
`CURRENT_R_OVERSTATEMENT_QUANTIFIED` — overstated by ≈+100…+143R on the actionable book; **not profitable under realistic execution.**
