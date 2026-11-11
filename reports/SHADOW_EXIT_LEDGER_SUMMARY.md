# Shadow Exit Ledger — Summary (PART 3)

**Trades in ledger:** 146 · **covered:** 146 (100.0%) · **missing_data:** 0
**Shadow measurement only — real exits unchanged, `partial_exit_model.enabled` stays false.**

## Net R / PF / winrate by variant (covered trades)
| variant | n | net_R | PF | winrate | winners_clipped | losers_saved |
|---|---|---|---|---|---|---|
| A_current | 146 | -39.2 | 0.68 | 16.4 | 26 | 0 |
| B_BE_0.5R | 146 | -1.2 | 0.97 | 6.8 | 39 | 60 |
| C_BE_1R | 146 | -21.9 | 0.72 | 11.0 | 33 | 20 |
| D_partial50_1R | 146 | -31.3 | 0.68 | 33.6 | 45 | 0 |
| E_partial50_1R_BE | 146 | -20.5 | 0.73 | 30.1 | 47 | 20 |
| F_trail_1R | 146 | -35.8 | 0.53 | 47.3 | 46 | 20 |
| G_candle_close_stop | 146 | -30.7 | 0.74 | 17.8 | 26 | 2 |
| H_no_reentry | 146 | -39.2 | 0.68 | 16.4 | 26 | 0 |
| I_one_reentry | 146 | -30.7 | 0.74 | 17.8 | 26 | 2 |

## Recommendation
- shadow_candidate: B_BE_0.5R reduces drawdown (net -1.2R, PF 0.97) vs shadow-current (-39.2R) on 100.0% coverage. still net-negative / PF<1 on this window, so measure FORWARD as a SHADOW rule across up+down regimes; DO NOT enable in trade logic yet. NOTE: shadow A_current (5m + conservative same-candle) is PESSIMISTIC vs the real recorded book (actual net 6.0R) — only the RELATIVE variant deltas are meaningful, not absolute levels.

Actual (A_current) baseline: net 6.0R, PF 1.06, winrate 33.6% over 146 covered trades.

_Per-mode/tier/regime cuts are available in the ledger CSV; this summary headlines the variant comparison. No production change._