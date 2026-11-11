# Chart Markers / Overlay Fix (PART 6)

**Date:** 2026-06-24.

## Backend `/api/trades/{id}/chart-events` (enriched)
Returns level lines (entry, initial stop, TP1/2/3 with exact R, Stop->BE, Lock +0.5R) AND a `markers` array, each with: `marker_type` (entry | tp | stop | exit | expired_exit | mfe | mae), `timestamp`, `price`, `label`, `status`, `reason`, `r_at_marker`, `pnl_usdt_at_marker`. The **exit / expired_exit marker** carries the real close price + paper R + net $ (from the ledger).

## Frontend
Closed-trade detail renders a **markers timeline** (each with price · R · $) + level lines with exact R + a sizing/exit block. Entry, TP touches, stop, **exit**, **expired close**, MFE/MAE are all listed with prices/timestamps.

## Full candlestick overlay
Horizontal-line overlay directly on the lightweight `Chart.tsx` candles remains a **TODO** (component renders OHLC; line overlay is a larger change). Per the task's allowance, the marker timeline + exact exit/expired price + timestamp are shown NOW; the data is fully available for a future overlay.

## Verdict
`CHART_MARKERS_VISIBLE_FOR_ENTRY_EXIT_STOPS_TPS_EXPIRED` (timeline + endpoint live; full candle line-overlay = TODO)
