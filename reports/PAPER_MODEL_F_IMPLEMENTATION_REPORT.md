# Paper Model F — Implementation Report (PART 3)

**Date:** 2026-06-24. Active PAPER-ONLY risk model for future + recalculated trades. No live execution. No historical `final_r` rewrite.

## Storage — new additive table (Option A)
`paper_execution_outcomes` (PK `signal_id`, idempotent upsert), created via `ensure_table`. **`signal_outcomes` is never touched** (verified: no `paper_execution_*` column on it; 315,610 rows + `final_r` intact). Columns: as in the spec. Index on `economic_trade_key` for deduped read.

## Tracker integration (future paper trades)
In `src/signals/tracker.py::track_active_signals`, immediately after `store.add_signal_outcome(...)`:
```python
try:
    from src.execution.paper_execution_accounting import record_paper_execution
    record_paper_execution(store, signal=row, outcome_row=outcome.to_row(), now_iso=_iso(now))
except Exception:
    pass  # accounting must never block legacy tracking
```
**Fail-open:** any error leaves legacy tracking working and simply leaves that row's paper outcome stale (the dashboard flags `paper_unavailable`). No order logic, no scoring/entry/routing touched.

## Scheduler (non-fatal step)
`paper_execution_refresh_step()` → `_cli("paper-execution-refresh")`, marked `command_nonfatal`, inserted after `catalyst_label_refresh` and before `ohlcv_archive`. Confirmed present at **position 6/23** in the cycle plan; **zero live/exchange/order steps**; LLM-auto-invoke guard OK.

## CLI
`paper-execution-refresh` (typer) → `backfill_all(conn)`. Verified run: **scanned=1607/1610, written all, resolved all, errors=0** — "paper/accounting only; final_r untouched; no live".

## Raw-ledger sanity (per-signal, pre-dedup)
SUM `touch_r` = −41.6R vs SUM `paper_execution_r` = **+74.0R** across 1607 entered signals → early protection turns the touch-loss book net-positive in replay (deduped book numbers in PART 4).

## Verdicts
`MODEL_F_ACTIVE_FOR_PAPER_ACCOUNTING` · `NO_LIVE_EXECUTION_ENABLED`
