# TRADE UI + MARKET FIX — FINAL AUDIT (PART 13/14)

**Date:** 2026-06-24. PAPER ONLY. Live-verified on the clean stack.

| check | result |
|---|---|
| ENA marker fixed | `/chart-events` → tp_fill=3, genericExit=0, lines=6 (TP1 0.0846 / TP2 0.083 / TP3 0.0814). ✅ |
| TP3 trade shows TP1/TP2/TP3 fills | yes — 3 partial markers, cum R 0.40/1.12/2.21, last is_final_exit. ✅ |
| click → chart-first detail | TradeDetail = candlestick(markers+lines) → PnL → price ladder → lifecycle → setup; all trade clicks route here. ✅ |
| active lifecycle after TP1 | non-terminal stays open; `tp1_filled_active`/`tp2_filled_active` + partial badge + next-target. ✅ (code-verified; no mid-flight row at audit time) |
| price ladder $ outcomes | `PriceLadderTable` shows price·R·net$·status per Stop/Entry/TP1-3. ✅ |
| signals card overflow | KV min-w-0+break-words, KVsm, grid-cols-2 + full-width TP row. ✅ |
| VIX loaded/explained | VIX 19.7 (yfinance ^VIX); else "VIX unavailable" + source. ✅ |
| Opus feeds market | §17 block + parser + `_backfill_extras` fills VIX even if Opus null; fallback. ✅ |
| all buttons audited | tsc+vite build exit 0 (92 modules); endpoints 200. ✅ |
| live locked | `/api/health` live_locked:true, auto_live_locked:true. ✅ |
| final_r untouched | no paper column on `signal_outcomes`; never written. ✅ |

## Bugs found & fixed this pass
1. `Chart.tsx` drew a single `overlays.exit_at` marker, ignoring chart-events partial
   fills → now consumes lifecycle markers + lines (ENA root cause).
2. chart-events markers lacked the full schema → enriched (cumulative R/$, side,
   source_book, is_partial/final, event_type, marker_id, lines).
3. Closed rows opened a non-chart-first drawer → now route to chart-first TradeDetail.
4. KV/SignalCard overflow on narrow widths → min-w-0 + break-words + 2-col + KVsm.
5. Market VIX blank → deterministic `fetch_market_extras` + backfill in parser/fallback/populate.
6. Type errors (Chart predicate, ce.lines) fixed; transient backend-restart port race
   resolved via the canonical `launch_robust.ps1` (keeper disabled, no race).

## Verdict
**FINAL_AUDIT_TRADE_UI_MARKET_FIX_COMPLETE**
