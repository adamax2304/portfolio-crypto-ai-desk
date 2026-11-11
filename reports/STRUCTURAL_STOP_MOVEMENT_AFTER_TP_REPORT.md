# STRUCTURAL STOP MOVEMENT AFTER TP — REPORT (PART 4)

**Scope:** PAPER ONLY. Date: 2026-06-24. Never moves a production/real stop.

## Module
`crypto-ai-desk/src/execution/structural_stop_manager.py` —
`structural_stop_after_tp(...)` → `StopMove` (previous_stop, new_stop, moved,
stop_move_reason, structure_used, structure_confidence, protection_r,
remaining_qty_affected). Event name: `stop_moved_structural`.

## Logic
After TP1/TP2, move the stop to a **structural** protective level when one exists:
- **long** → below a recent higher-low / range support / VWAP;
- **short** → above a recent lower-high / range resistance / VWAP.
Else fall back to **BE** (after TP1) / **+0.5R lock** (after TP2). Guards:
- never worse than current protection (keeps the tighter stop);
- structural candidate must be ≥ the fallback protection R;
- after TP2 the lock floor is tighter than after TP1.

## Integration
The backend lifecycle read-model emits `stop_moved_structural` events at each TP using
the R-based fallback (BE/lock) because the backend has no candles; the candle-based
structural selection lives in this module and is used on the **forward** path (live
OHLCV) and is unit-tested. UI shows previous→new stop, reason, structure_used,
protection R.

## Tests (`tests/test_structural_stop_manager.py`, 5 passed)
long→higher-low after TP1; BE fallback when no structure; +0.5R lock after TP2; never
loosens a tighter current stop; short→lower-high.

## Verdict
**STRUCTURAL_STOP_MOVEMENT_AFTER_TP_READY_FOR_PAPER**
