# STRUCTURAL STOP MOVEMENT — VERIFICATION (PART 7)

**Date:** 2026-06-24. PAPER. Module `src/execution/structural_stop_manager.py`.

## Verified behaviour
`structural_stop_after_tp(...)` after TP1/TP2:
- **long** → moves stop to a recent **higher-low** / range support / VWAP above the
  current stop; **short** → recent **lower-high** / resistance / VWAP below the current
  stop;
- requires the structural candidate to give **≥ the fallback protection R** and to be
  **better than the current stop** (never loosens);
- else **fallback** to BE (after TP1) / +0.5R lock (after TP2), tighter after TP2;
- records `previous_stop, new_stop, moved, stop_move_reason, structure_used (higher_low |
  lower_high | support | resistance | vwap | be | lock | none), structure_confidence,
  protection_r, remaining_qty_affected`.

Tests (`tests/test_structural_stop_manager.py`, 5 passed): long→higher-low after TP1; BE
fallback when no structure; +0.5R lock after TP2; never loosens a tighter current stop;
short→lower-high.

## Live read-model labelling (honest)
The backend lifecycle has **no per-trade OHLCV candles**, so its `stop_moved_structural`
events use the **R-based fallback** (BE → +0.5R → +2R) and are **labelled explicitly**
("after TPn → … (structural fallback: BE/lock)") so the UI never implies a structural
level was used when it wasn't. The candle-based structural selection (this module) runs on
the **forward** path where live candles exist; when structure is available it is used, and
the chosen `structure_used` is surfaced.

No structure-available-but-ignored case was found: the fallback only fires when candles are
absent (backend) or no qualifying level exists (engine).

## Verdict
**STRUCTURAL_STOP_MOVEMENT_VERIFIED_OR_FIXED** (verified; fallback clearly labelled where
candles are unavailable).
