# EXCHANGE-LIKE PRICE LADDER / OUTCOME TABLE (PART 5)

**Date:** 2026-06-24. Frontend. PAPER/UI.

## Component
`PriceLadderTable` (in `screens.tsx`) renders, for every trade, a compact table:

| row | columns |
|---|---|
| Initial stop · Current stop (if moved) · Entry · TP1 · TP2 · TP3 | price · exact R · net $ (partial slice, after fees) · status · |

- **Status** per row: `filled` (with timestamp), `waiting` (active), `not reached`
  (closed), `protective`/`moved · active` for stops.
- Net $ uses the realized partial PnL when filled, else the expected $ on the slice.
- For an **active** position: TP1 shows `filled`, TP2/TP3 show `waiting`, current stop
  shows `moved · active`.
- For a **closed** position: all reached TPs show `filled`; footer shows the close status.

Rendered in the chart-first `TradeDetail` (below the chart) and available in the
lifecycle panel. Fed by `/api/trades/{id}/lifecycle` (`price_ladder` + `partials` +
`events`).

## Verdict
**PRICE_LADDER_SHOWS_OUTCOMES_CLEARLY**
