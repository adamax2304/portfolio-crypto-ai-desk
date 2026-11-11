# ENA EXIT MARKER — ROOT CAUSE REPORT (PART 1)

**Date:** 2026-06-24. PAPER / read-model / UI only.

## Trade
`sig_d3feb06d58cac3c8` — ENA/USDT **short**. entry 0.08652, stop 0.08812 (risk 0.0016),
tp1 0.0846, tp2 0.083, tp3 0.0814. `signal_outcomes`: tp1_hit 03:15, tp2_hit 11:15,
**tp3_hit 15:45**, stop None, final_outcome **win**, final_r **3.0**, MFE 3.26R.

## Answers
1. **Why +3.0R on the card?** The card reads `final_r` (legacy **touch_r** = highest TP
   touched). TP3 was touched → +3.0R. Correct as a touch metric.
2. **Which metric is +3R?** Touch / `final_r` (optimistic). The partial-exit **blended R
   = 2.21** (TP1 33%@1.2R + TP2 33%@2.2R + TP3 34%@3.2R); `paper_execution_r` (Model-F) is
   a third number. Card shows touch; lifecycle shows blended.
3. **Are TP1/TP2/TP3 fill events in the backend?** **Yes.** `/api/trades/{id}/chart-events`
   already returns three `tp_fill` markers at 0.0846 / 0.083 / 0.0814 (cum R 0.40 / 1.12 /
   2.21) + entry + three `moved_stop` + MFE/MAE. No generic `exit` marker.
4. **Why does the frontend show ONE `exit` marker?** The misleading marker is **not** from
   chart-events. The full-screen candlestick **`frontend/src/Chart.tsx` (`ChartPanel`)**
   draws its markers from `useChart(...).overlays` — it pushes a **single `exit` square at
   `overlays.exit_at`** (colored win/loss) and ignores the lifecycle/chart-events partial
   fills entirely (`Chart.tsx:54-59`). That single exit square, placed at the exit
   timestamp, is what the operator sees "around the intermediate zone".
5. **Wrong book / touch vs paper / old ledger?** The *card* uses touch `final_r`; the
   *candlestick chart* uses the `overlays.exit_at` single marker. The correct partial-fill
   markers (B-book lifecycle) exist in chart-events but **`ChartPanel` never consumes
   them**. So: read-model is right; the candlestick renderer is wrong.
6. **Old rows vs all future trades?** It is a **read-model→renderer wiring gap in
   `ChartPanel`**, so it affects **every** trade (old and new) shown on the candlestick
   chart, not just derived rows. The SVG `ExecChart` in the Closed drawer already renders 3
   dots correctly — only the candlestick path is broken.

## Fix path
- PART 2: enrich chart-events markers to the full execution schema (already 3 fills; add
  cumulative/side/source_book/is_partial flags + price `lines`).
- PART 3: make `ChartPanel` consume chart-events markers + price lines (entry/stop/moved/
  TP1-3) and **drop the single generic exit marker**.
- PART 4: TradeDetail = chart-first with the lifecycle panel + price ladder below.

## Verdict
**ENA_EXIT_MARKER_CAUSE_IDENTIFIED** — backend correct (3 TP-fill markers); the
candlestick `ChartPanel` draws a single `overlays.exit_at` marker and ignores them;
affects all trades on the candlestick view.
