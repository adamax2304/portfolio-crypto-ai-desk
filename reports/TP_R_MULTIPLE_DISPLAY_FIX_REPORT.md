# TP R-Multiple Display Fix (PART 4)

**Date:** 2026-06-24.

## Bug
UI risked showing TP1=+1R / TP2=+2R / TP3=+3R by NAME. Actual TP distances vs entry/stop are NOT 1/2/3R — production entry sits below `close` and the stop is structural, so a real signal shows e.g. **TP1 1.2R / TP2 2.2R / TP3 3.2R** (verified on a live ledger row).

## Fix
`/api/trades/{id}/chart-events` computes exact, sign-aware R per level: `r = ((price − entry) if long else (entry − price)) / |entry − stop|`. Returned as `tp_r_exact {tp1,tp2,tp3}` + per-level `r_multiple`; plus exact `mfe_r`, `mae_r`, `paper_execution_r`, `touch_r`, `stop_current_r`. Shorts sign-flipped.
- **App** closed-trade detail shows `TP1 1.2R / TP2 2.2R / TP3 3.2R` (exact) + MECHANICAL_ATR badge; the legacy touch number stays in its own "Touch R (optimistic)" field, NOT relabelled as exact.
- **Telegram** close alert shows `TPs (exact R): 1.2R/2.2R/3.2R · MECHANICAL_ATR`.

## Verdict
`TP_R_MULTIPLES_DISPLAY_EXACT`
