# TP Reach-Rate Analysis (PART 4)

**Date:** 2026-06-23. N=1404 entered economic trades (60d); actionable subset n=582. Read-only.

## Reach rates — ALL entered (1404)
| event | n | % |
|---|---|---|
| TP1 reached | 248 | 17.7% |
| TP2 reached | 113 | 8.0% |
| TP3 reached | 52 | **3.7%** |
| stop hit | 561 | 40.0% |
| expired (no resolution) | 637 | 45.4% |
| reached TP1 but NOT TP3 | 196 | 14.0% |
| reached TP2 but NOT TP3 | 61 | 4.3% |
| reached TP1 then later stop (give-back) | 42 | **3.0%** |

## Reach rates — ACTIONABLE (582)
TP1 132 (22.7%) · TP2 78 (13.4%) · TP3 **45 (7.7%)** · stop 276 (47%) · expired 201 (35%).

## Net R by exit model (R reconstructed from recorded path)
| model | ALL (1404) | ACTIONABLE (582) |
|---|---|---|
| **production (best-TP-touched) = recorded** | **−118.5R** | **+5.0R** |
| cap at TP2 (VARIANT A, remove TP3) | −170.5R | **−40.0R** |
| hold→TP1 only | −259.8R | −106.0R |
| hold→TP2 only | −341.3R | −115.6R |
| hold→TP3 only | −403.1R | −136.8R |
| BE after TP1 (on hold-TP3 base) | −361.1R | −109.8R |
| partial@TP1 + runner (on hold-TP3 base) | −310.5R | −107.9R |

**TP3 contribution under production accounting (prod − capTP2): ALL +52R · ACTIONABLE +45R.** → TP3, *as scored today*, ADDS R; removing it clips winners and saves nothing.
**Under realistic hold accounting:** hold→TP1 (−106) beats hold→TP3 (−137) by +31R (actionable) → if you actually hold-through to a single target, lower is better. Both still net-negative.

## By mode (actionable)
| mode | n | prod R | capTP2 (no TP3) | hold→TP3 | hold→TP1 | TP3 reached |
|---|---|---|---|---|---|---|
| crypto intraday | 120 | −33.8 | −49.8 | −42.8 | −66.8 | 16 |
| **crypto swing** | 98 | **+22.8** | +2.8 | −13.0 | −22.2 | **20** |
| stocks intraday (B) | 364 | +16.0 | +7.0 | −81.0 | −17.0 | 9 |

## By regime (all)
| regime | n | prod R | hold→TP3 | TP3 reached |
|---|---|---|---|---|
| bullish | 680 | −105.3 | −233.7 | 8 |
| chop | 142 | +18.0 | −27.3 | 1 |
| risk_off | 138 | +6.0 | −36.7 | 5 |
| bullish trend | 132 | −10.4 | −40.0 | 10 |
| risk_on | 108 | −3.3 | −24.7 | 2 |
| bearish trend | 20 | +9.0 | +9.0 | 5 |

## By playbook (TP3 contribution under production)
| playbook | n | prod R | TP3 reached | TP3 add-R | hold→TP3 |
|---|---|---|---|---|---|
| crypto_swing_narrative_rs | 89 | +11.8 | 16 | **+16** | −21.8 |
| crypto_failed_bounce_short | 29 | +15.2 | 9 | **+9** | **+11.8** |
| crypto_intraday_catalyst/momo | 100 | −38.0 | 11 | +11 | −45.8 |
| stocks_intraday_rth_momentum | 684 | −18.7 | 15 | +15 | −189.0 |
| stocks_swing_watchlist_rs | 217 | −30.0 | 1 | +1 | −86.3 |
| stocks_invest_watchlist_30d | 167 | −36.0 | 0 | 0 | −47.0 |
| crypto_scalp_momentum (shadow) | 118 | −22.8 | 0 | 0 | −25.0 |

Long/short, catalyst-yes/no, squeeze splits are in the CSV; the decisive signal is mode×playbook above (catalyst/short subsets are small and dominated by the swing/failed-bounce cohorts already shown).

## Verdict
`TP_REACH_RATES_COMPUTED`
