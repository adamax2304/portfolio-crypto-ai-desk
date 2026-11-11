# TRADE UI + MARKET FIX — TEST RESULTS (PART 13)

**Date:** 2026-06-24. PAPER ONLY.

## crypto-ai-desk — `tests/` (43 passed)
- `test_market_dashboard.py` — Opus block extract / missing→None / persist / fallback;
  **fetch_market_extras shape + fail-open (VIX/SPY/QQQ/ETH-BTC keys)**; **parse_and_store
  backfills VIX when Opus null** (monkeypatched).
- `test_structural_stop_manager.py` (5) — long→higher-low / BE fallback / +0.5R lock /
  never-loosen / short→lower-high.
- `test_paper_portfolio.py` (15) — max-5x sizing + liq-safety.
- `test_structural_maker.py` (17) — structural TP / fee-aware / maker-first.

## trading-desk-control — `backend/tests/` (72 passed)
- `test_execution_ui.py` — regime normalize; actionability **closed-trade no chase
  label**; lifecycle shape + partials + max-lev≤5; missed-opportunities; market shape +
  **VIX field present**; **chart-events 3 tp_fill + no generic exit + full marker schema +
  lines**; marker-schema fields (marker_id/event_type/source_book).
- `test_portfolio.py` — chart-events marker vocabulary (tp_fill/stop/expired/entry);
  portfolio compare; B max-lev. Plus books / control-plane / paper-features / display.

## Frontend
`npm run build` (tsc -b && vite build): **exit 0, 92 modules** — Chart (markers+lines),
chart-first TradeDetail, PriceLadderTable, Signals overflow fix (KV/KVsm), Market VIX card
all typecheck.

## Live (clean stack)
`/api/health` 200 live_locked; ENA `/chart-events` tp_fill=3 genericExit=0 lines=6;
`/market-dashboard` VIX 19.7. No `signal_outcomes.final_r` write; live locked.

## Verdict
**TRADE_UI_MARKET_FIX_TESTS_PASS**
