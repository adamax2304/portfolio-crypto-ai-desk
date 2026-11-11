# FULL TRADE CHART OVERLAY — IMPLEMENTATION (PART 3)

**Date:** 2026-06-24. Frontend (`trading-desk-control`). PAPER/UI.

## Change — `frontend/src/Chart.tsx` (lightweight-charts, existing lib)
`ChartPanel` now accepts optional `markers` (lifecycle execution markers) + `lines`
(price levels) and renders them on the candlestick:
- **Horizontal price lines** for entry, initial stop, current/moved stop, TP1/TP2/TP3
  (from `chart-events.lines`), each axis-labelled with R.
- **Markers** for entry / TP1·TP2·TP3 fills / moved stops / stop / expired / missed,
  glyph + color per type, text = label + R, placed at the real fill time.
- The **single generic `overlays.exit_at` square is dropped** whenever lifecycle markers
  are present (it remains only as a fallback for trades with no lifecycle).

## ENA result
`ChartPanel` for the ENA +3R trade now draws **three TP-fill markers** + entry + moved
stops + TP1/TP2/TP3 price lines — no misleading single exit near TP1/TP2. Verified the
feeding endpoint returns `tp_fill=3, genericExit=0, lines=6`.

## Library
No new package — extended the existing `lightweight-charts` component (keeps the bundle
stable; frontend build 92 modules, exit 0). The SVG `ExecChart` (price-scaled) remains
available for the compact view.

## Verdict
**FULL_CHART_OVERLAY_SHOWS_PARTIAL_EXITS**
