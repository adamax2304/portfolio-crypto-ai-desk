# TRUE PARTIAL-EXIT CHART-EVENTS — FIX REPORT (PART 2)

**Date:** 2026-06-24. PAPER / read-model. `/api/trades/{id}/chart-events`.

## What changed
The chart-events markers (sourced from the live position lifecycle) were enriched to the
full execution schema in `backend/app/portfolio.py`:
`marker_id, marker_type, event_type, timestamp, price, label, side, qty_closed,
remaining_qty, realized_r, realized_pnl_usdt, cumulative_realized_r,
cumulative_realized_pnl_usdt, fee_usdt, order_type, reason, source_book
(paper_B_structural_maker | paper_A_mechanical_taker | touch_legacy), is_partial_exit,
is_final_exit`. Added a top-level `lines` array (alias of `levels`) and `source_book`.

## Rule enforced
If TP1/TP2/TP3 were all reached → three `tp_fill` markers at TP1/TP2/TP3 prices, the last
flagged `is_final_exit`. **No generic `exit` marker** when the result is a multi-TP win.

## Live verification (ENA `sig_d3feb06d58cac3c8`)
```
tp_fill=3 · genericExit=0 · lines=6 · source_book=paper_B_structural_maker
TP1 @ 0.0846 cumR 0.396 partial=True  final=False
TP2 @ 0.0830 cumR 1.122 partial=True  final=False
TP3 @ 0.0814 cumR 2.210 partial=False final=True
```

## Tests
`backend/tests/test_execution_ui.py`: a 3-TP trade returns ≥3 `tp_fill` markers, **no
`exit`**, each with `cumulative_realized_r`/`source_book`/`is_partial_exit`, and `lines`
present; marker-schema fields on entry/tp/stop/expired/moved markers.

## Verdict
**TRUE_PARTIAL_EXIT_EVENTS_AVAILABLE**
