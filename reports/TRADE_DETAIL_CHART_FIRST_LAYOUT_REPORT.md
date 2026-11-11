# TRADE DETAIL — CHART-FIRST LAYOUT (PART 4)

**Date:** 2026-06-24. Frontend. PAPER/UI.

## Change
`TradeDetail` (the page opened on any trade click) is now **chart-first**:
1. **Top:** candlestick `ChartPanel` with all execution markers + price lines (entry /
   stop / moved stop / TP1-3) from `/chart-events`.
2. **Compact PnL header** (closed): blended R + net $ + touch R + MFE/MAE.
3. **Price ladder outcome table** (`PriceLadderTable`, PART 5).
4. **Full lifecycle** (`LifecyclePanel` with `hideChart` — position summary, realized,
   execution timeline) — the SVG mini-chart is suppressed since the candlestick is above.
5. **Setup analysis** + **manual/actionability** controls (unchanged).

## Routing
All trade clicks now open this chart-first page:
- Signals tab `SignalCard` → `onChart` → TradeDetail (already).
- Trades open/pending `TradeCard` → `onChart` → TradeDetail.
- **Closed book rows now route to `onChart` (TradeDetail)** instead of the bottom drawer,
  so every click lands on the same chart-first exchange-like page (the old `ClosedDetail`
  drawer is retired from the flow).

Header now also shows the readable **regime** label.

## Verdict
**TRADE_DETAIL_OPENS_CHART_FIRST**
