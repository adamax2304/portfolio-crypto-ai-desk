# POST-Backfill Profit-Protection Replay (PART 5)

**Date:** 2026-06-18 · **Script:** `scripts/replay_profit_protection_path_aware.py` (archive-first) · **CSV:** `POST_BACKFILL_PROFIT_PROTECTION_REPLAY.csv`
**Verdict:** **PARTIAL_TP1_SHADOW_CANDIDATE / BE_AFTER_1R_SHADOW_CANDIDATE** → still **PROFIT_PROTECTION_STILL_DISABLED.**

## Coverage (the headline win)
After the 60d 5m/15m backfill, the path-aware replay covers **146 / 146 (100%)** of the 30d crypto intraday/swing closed trades, all on 5m — up from 17.8%. Coverage target (≥70%) **met**.

## Variant results (path-aware, 100% coverage, 5m, conservative same-candle)
| Variant | net R | PF | winrate | winners_clipped | losers_saved |
|---|---|---|---|---|---|
| A_current (shadow) | −39.2 | 0.68 | 16.4% | — | — |
| **B_BE_0.5R** | **−1.2** | **0.97** | 6.8% | 39 | 60 |
| C_BE_1R | −21.9 | 0.72 | 11.0% | 33 | 20 |
| E_partial50_1R+BE | −20.5 | 0.73 | 30.1% | 47 | 20 |
| D_partial50_1R | −31.3 | 0.68 | 33.6% | 45 | 0 |
| G_candle_close_stop | −30.7 | 0.74 | 17.8% | 26 | 2 |
| F_trail_1R | −35.8 | 0.53 | 47.3% | 46 | 20 |
| H/I (reentry variants) | −30.7 / −39.2 | — | — | — | — |

## ⚠ Critical honesty caveat — read before interpreting
**The shadow replay is PESSIMISTIC vs the real book.** Shadow `A_current` = −39.2R, but the **actual recorded** outcomes for the same 146 trades sum to **+6.0R (PF 1.06)**. The gap is an artifact of the shadow method: it walks **5m** candles with a **conservative same-candle (stop-first)** rule, whereas the production tracker reconciles on coarser per-mode timeframes — so the 5m replay registers many more stops. **Therefore only the RELATIVE deltas between variants are meaningful; the absolute levels are not the real book.**

## Read
- Relative to the (pessimistic) shadow baseline, **BE-after-+0.5R** cuts drawdown the most (−39→−1.2, PF 0.68→0.97; saves 60 losers, clips 39 winners), with **partial-50%@+1R+BE** and **BE-after-+1R** next.
- BUT this 30d window was a **net-losing crypto stretch**, and even the best variant is only ~breakeven on the shadow basis (PF<1). So no variant turns the strategy profitable here — they reduce bleed.
- The high winners_clipped counts (39–47) confirm the known trade-off: BE/partial in chop saves losers but clips winners; on a trending-up month the balance flips.

## Decision
- **PROFIT_PROTECTION_STILL_DISABLED.** `partial_exit_model.enabled` stays false.
- **Shadow candidates to measure FORWARD:** partial-TP1 (best winrate-preserving) and BE-after-+1R (fewer false BE triggers than +0.5R). BE-after-+0.5R looks best here but is the most regime-sensitive (clips the most winners) — treat with caution.
- **Before any enable:** (a) reconcile the 5m-shadow-vs-tracker timeframe discrepancy so absolute R is trustworthy; (b) confirm the candidate is net-positive across an **up/trending** month too, not just this losing window; (c) only then discuss enabling (still paper, with explicit approval).
