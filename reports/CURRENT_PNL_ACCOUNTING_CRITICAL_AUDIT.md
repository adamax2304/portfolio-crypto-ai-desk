# Current PnL Accounting — Critical Audit (PART 1)

**Date:** 2026-06-23. Read-only (code + DB). **No production logic / no `final_r` changed.**

## Where & how `final_r` is computed
`src/signals/tracker.py` → `_evaluate_signal_walk` walks OHLCV candles after entry and records `tp1/2/3_hit`, `stop_hit` + timestamps; `_classify` sets `final_r`:
| situation | recorded final_r |
|---|---|
| TP3 touched (ever) | **+r_tp3** |
| TP2 touched (not TP3) | **+r_tp2** |
| TP1 touched (not TP2/3) | **+r_tp1** |
| **TP1 touched → later stop** | **+r_tp1 (WIN)** ← key |
| **TP2 touched → later stop** | **+r_tp2 (WIN)** ← key |
| stop, no TP touched | −1R (loss) |
| same-candle stop+TP | **stop-first, −1R, flagged ambiguous** (conservative) |
| no TP, no stop, window ends | 0R (expired) |

So **`final_r` = R of the HIGHEST TP level the price ever touched** ("touch-based"). Stop matters only when **no** TP was touched.

## The 8 checks
1. Stop after TP1/TP2 → **never moves** (fixed `invalidation` whole trade).
2. Partial close → **none.** One R per trade.
3. Remaining position → **no such concept.**
4. BE / profit-lock / trailing → **none in production**; exist only in `src/exits/shadow_exit_manager.py` (shadow, not wired — confirmed zero imports in tracker/scheduler).
5. Close alerts (`src/notifiers/close_alert.py`) → describe the recorded terminal outcome (the touch-based win/loss); they do not model a partial/remaining.
6. App/Telegram (`trading-desk-control` `books.py`/`desk_adapter.py`) → surface `final_r`/`realized_r` = the same touch-based number, labelled "Today R / realized" with **no "touch-based" caveat** today.
7. crypto/stocks, intraday/swing/scalp → identical logic; mode only changes the OHLCV timeframe.
8. Number of TP levels → whatever the idea agent emits (≈3); not adaptive.

## Plain-language verdict
- **The current system computes `final_r` as the highest TP touched.**
- **A TP1 touch is recorded as a WIN even if the price later hit the stop** (and likewise TP2).
- **This is correct ONLY under a full-close-at-best-TP / resting-limit-at-every-TP assumption with no give-back.**
- **It is NOT realistic if a position remains open after TP1** (a single manual position can ride TP1→stop and lose, which this model never records as a loss).

## Verdicts
`CURRENT_ACCOUNTING_IS_TOUCH_BASED` · `STOP_DOES_NOT_MOVE_AFTER_TP` · `NO_PARTIAL_CLOSE_IN_PRODUCTION` · `CURRENT_FINAL_R_MAY_BE_OPTIMISTIC`
