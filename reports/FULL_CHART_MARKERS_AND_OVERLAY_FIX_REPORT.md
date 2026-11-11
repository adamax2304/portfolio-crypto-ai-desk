# FULL CHART MARKERS + OVERLAY FIX — REPORT (PART 5)

**Scope:** PAPER ONLY, read-model + UI. Date: 2026-06-24.

## Backend — `/api/trades/{id}/chart-events` (rewritten to source from the lifecycle)
Markers now come from the live position lifecycle, replacing the single misleading
"Exit" marker:
- `entry` (filled) · `tp_fill` ×N (each partial TP at its real price, with R, $, qty
  closed) · `moved_stop` (each structural/BE/lock move) · `stop` · `expired_exit` ·
  `missed` · `mfe` / `mae`.
- Lines: `entry`, `initial_stop`, `current_stop` (moved), `tp1/2/3` — each with exact R.
- `lifecycle` object attached for the detail UI.

## ETH fix (verified)
For `sig_c6df604c56ba3036` (+3R) chart-events now returns **three TP fill markers** at
1636.86 / 1623.09 / 1609.32 (cum R 0.40 / 1.12 / 2.21, $9.51 / $27.27 / $54.07) +
moved-stop markers — **no single exit marker near TP1/TP2**. Root cause was the single
A-book Model-F exit price (≈ a blended/locked exit) shown against a +3R header, plus the
trade being absent from the batch ledger; the live lifecycle removes both.

## Frontend — price-scaled SVG overlay (`ExecChart`)
Every level (entry/stop/moved-stop/TP1-3) is drawn as a horizontal line at its **true
price height**, and every fill is a dot at its true price — so a +3R TP3 fill sits at
TP3, never near TP1/TP2. Labelled with price; the timeline lists R/$/qty. Full
candlestick line-overlay (lightweight-charts) remains a documented TODO; the
price-scaled overlay already resolves the misleading-marker bug without a new heavy
dependency.

## Verdict
**FULL_CHART_OVERLAY_SHOWS_TRUE_EXECUTION_EVENTS**
