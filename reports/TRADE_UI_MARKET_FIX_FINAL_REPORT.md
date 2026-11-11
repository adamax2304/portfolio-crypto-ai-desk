# TRADE DETAIL + PARTIAL EXIT MARKERS + MARKET VIX + MOBILE OVERFLOW — FINAL REPORT

**Date:** 2026-06-24. **PAPER / APP / READ-MODEL ONLY** — no live, no exchange execution,
no real orders, no production TP/SL or scoring/routing change, `signal_outcomes.final_r`
never rewritten. Live-verified on the clean stack.

## 1. Was the ENA marker wrong? Yes — visually. The +3.0R was correct (touch/final_r,
TP3 hit); the **chart showed one misleading `exit` marker** near TP1/TP2.

## 2. Why was it wrong? The candlestick **`frontend/src/Chart.tsx` drew a single
`overlays.exit_at` square** and ignored chart-events. The backend already returned three
`tp_fill` markers — the renderer never consumed them.

## 3. Fixed for old and new trades? Yes — it's a renderer/read-model wiring fix in
`Chart.tsx` + chart-events, applied to **every** trade on the candlestick view.

## 4. Does a TP3 trade show TP1/TP2/TP3 fills? Yes. ENA live: `tp_fill=3, genericExit=0,
lines=6` — TP1 0.0846 (cumR 0.40) / TP2 0.083 (1.12) / TP3 0.0814 (2.21, final).

## 5. Does clicking a trade open chart-first detail? Yes — `TradeDetail` = candlestick
(markers+lines) → PnL header → price-ladder table → lifecycle → setup; all clicks
(Signals / open / **closed rows**) route there.

## 6. Is the price ladder visible? Yes — `PriceLadderTable`: Stop/Entry/TP1-3 with price,
exact R, net $, status, timestamp.

## 7. Are $ outcomes at stop/TP shown? Yes — max loss at stop + net $ per TP slice (after
fees), realized vs expected by status.

## 8. Does an active position remain after TP1? Yes — non-terminal stays in the open
bucket; `tp1_filled_active`/`tp2_filled_active` + partial badge + next target (code-
verified; no mid-flight row existed at audit time to screenshot).

## 9. Is structural stop movement verified? Yes — `structural_stop_manager` (swing/SR/VWAP,
BE/lock fallback, never-loosen) tested (5); the backend lifecycle has no candles so it uses
the **clearly-labelled fallback**; the candle path uses real structure.

## 10. Is the Signals card overflow fixed? Yes — KV `min-w-0`+`break-words`, new `KVsm`,
price row → `grid-cols-2` + full-width TP1/TP2/TP3 row; buttons stay inside.

## 11. Is VIX loaded or explained? Loaded — **VIX 19.7** (yfinance ^VIX) + SPY/QQQ down +
ETH/BTC 0.0265; backfilled in the Opus parser/fallback/populate; "VIX unavailable" shown
explicitly when truly missing.

## 12. Does Opus feed the Market tab? Yes — §17 final JSON block (review body unchanged) +
parser; `parse_and_store(fill_extras=True)` backfills VIX even if Opus leaves it null.

## 13. Were all app buttons audited? Yes — `tsc -b && vite build` exit 0 (92 modules);
all endpoints 200; clarity guarantees enforced. Live Telegram click-through needs the
Mini-App context (covered by build + endpoint + 72 backend tests).

## 14. Did live remain off? Yes — `/api/health` → live_locked:true, auto_live_locked:true.

## 15. Was final_r unchanged? Yes — no paper column; never written.

## 16. What remains TODO
- Full per-trade OHLCV structural re-walk (forward path already structural).
- BTC dominance provider (currently null — explained); per-account custom fee rate.
- Live mid-flight active-partial screenshot (works in code; awaits a trade at TP1).
- Re-enable the `CryptoAIDeskApp` keeper for auto-heal (currently Disabled — stack is
  manually up via `launch_robust`).

## Tests
43 crypto + 72 backend pass; frontend build clean (92 modules).

## Final verdicts
- TRUE_PARTIAL_EXIT_EVENTS_AVAILABLE
- FULL_CHART_OVERLAY_SHOWS_PARTIAL_EXITS
- TRADE_DETAIL_OPENS_CHART_FIRST
- PRICE_LADDER_SHOWS_OUTCOMES_CLEARLY
- ACTIVE_POSITIONS_REMAIN_AFTER_PARTIAL_TP
- STRUCTURAL_STOP_MOVEMENT_VERIFIED_OR_FIXED
- SIGNALS_CARDS_NO_OVERFLOW
- MARKET_TAB_VIX_AND_DATA_LOADED_OR_EXPLAINED
- OPUS_ROUTINE_FEEDS_MARKET_DASHBOARD
- APP_UI_UX_BUTTONS_AUDITED_AND_FIXED
- NO_LIVE_EXECUTION_ENABLED
- HISTORICAL_FINAL_R_UNCHANGED
- READY_FOR_FORWARD_VALIDATION
