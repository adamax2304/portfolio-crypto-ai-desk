# Paper Portfolio + Risk — Test Results (PART 12)

**Date:** 2026-06-24.

## crypto-ai-desk — 88 passed
- NEW `tests/test_paper_portfolio.py` (16): sizing (2% stop → notional 1250/risk 25/lev 2; tight stop caps risk; 0.5% stop maxed; short; liq buffer; leverage≠risk); fees (taker open+close; profiles parse; conservative > bybit; net = gross − costs); portfolio (equity updates W/L/BE; fees reduce equity; skips unresolved/bad-geometry, no silent zero).
- NEW `tests/test_tp_structure_validator.py` (4): mechanical ATR ladder flagged; structural TPs accepted; TP3 chop warning; TP3 runner allowed.
- Regression: paper_execution_accounting (10), paper_features_config (4), realistic_pnl_models (7), display_status, default_market_schedule, project_state_docs — all pass.

## trading-desk-control backend — 57 passed
- NEW `tests/test_portfolio.py` (2): `/api/portfolio` shape + safety (deposit 5000, risk 0.5%, live_locked True, open_positions 0); trades/chart-events return lists/dicts.
- `test_books.py`, `test_paper_features.py`, `test_control_plane.py`, `test_display_status.py` — pass.

## Frontend
- `npm run build` (tsc -b + vite) → exit 0; portfolio cards + types compile.

## Scheduler / safety / docs
- Scheduler dry-run → `LLM-auto-invoke check OK`; no live/exec steps.
- Docs validator → `PROJECT STATE DOCS: OK`.
- No `signal_outcomes.final_r` mutation (no paper column on signal_outcomes).
- C-tier/scalp/stocks swing-invest still not actionable (unchanged gates).

## Verdict
`PAPER_PORTFOLIO_RISK_TESTS_PASS`
