# EXECUTION UI + MARKET DASHBOARD — TEST RESULTS (PART 13)

**Date:** 2026-06-24. PAPER ONLY.

## crypto-ai-desk — `tests/` (24 targeted passed)
- `tests/test_paper_portfolio.py` (15) — **max-5x sizing**: 5x notional/leverage, 0.5%
  fits at 4x, 0.3% caps + too_tight, **wide-stop liquidation-safe leverage reduction**,
  leverage≠risk, liq buffer.
- `tests/test_structural_stop_manager.py` (5) — long→higher-low after TP1, BE fallback,
  +0.5R lock after TP2, never loosens current stop, short→lower-high.
- `tests/test_market_dashboard.py` (4) — Opus block extraction, missing→None, persist
  snapshot, deterministic fallback.

## trading-desk-control — `backend/tests/` (70 passed)
- `test_execution_ui.py` (new) — regime normalization (empty→unknown, free-text maps,
  unmapped low-conf); **actionability closed-trade has no chase label** (MSTR), open-late
  still warns; lifecycle shape + safety; **partials ordered + blended R ≤ touch R + max
  lev ≤ 5**; missed-opportunities; market-dashboard shape + safety locks.
- `test_portfolio.py` — chart-events now asserts lifecycle marker vocabulary
  (`tp_fill`/`stop`/`expired_exit`/`entry`); portfolio compare; B max-lev.
- Existing books / control-plane / paper-features / display-status tests pass.

## Frontend
`npm run build` (tsc -b && vite build): **exit 0, 92 modules**, no type errors.
Market tab renders, trade detail renders the lifecycle panel + price-scaled chart,
active positions show partial badges, no missing required fields.

## Safety assertions
- No `signal_outcomes.final_r` rewrite (read-models only).
- No live/exec: `/api/health` → `live_locked:true`.
- No production TP/SL or scoring/routing change.

## Verdict
**EXECUTION_UI_MARKET_DASHBOARD_TESTS_PASS**
