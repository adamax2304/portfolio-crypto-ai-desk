# Paper Portfolio Bugfix — Test Results (PART 10)

**Date:** 2026-06-24.

## crypto-ai-desk — 43 passed (relevant subset; full suite green)
- **Fees:** open fee on entry notional; close fee on EXIT notional (`exit_notional_usdt=1300` → close fee 1300×rate); estimated when exit omitted (`fee_estimated=True`); alias `bybit_default_futures→bybit_non_vip_usdt_perp`; conservative > bybit; zero=0.
- **Expired / exit price:** `simulate_portfolio` sets `exit_price` for all (+2R long → 104.0); expired_flat → exit at entry (100.0) + `expiry_close_price` + source; close fee uses exit notional in the sim.
- **TP R / sizing / portfolio:** sizing (2% stop → notional 1250/risk 25/lev 2; tight stop caps; short; leverage≠risk); portfolio equity W/L/BE; fees reduce equity; skips unresolved (no silent zero).
- **TP validator:** mechanical flagged, structural accepted, TP3 chop-warning, runner allowed.
- Regression: paper_execution_accounting (10), realistic_pnl_models (7), paper_features_config (4), project_state_docs.

## trading-desk-control backend — 58 passed
- **Portfolio:** summary shape + safety (deposit 5000, risk 0.5%, live_locked, open_positions 0); trades/chart-events lists.
- **NEW chart-events:** for a real ledger trade — `tp_r_exact` present, an `exit`/`expired_exit` marker exists, `tp_quality.label == MECHANICAL_ATR_LADDER`.
- books / paper_features / control_plane / display_status — pass.

## Frontend
- `npm run build` (tsc + vite) → exit 0; chart-events detail + leverage cards compile.

## Safety
- `final_r` not mutated (no paper col on signal_outcomes). Scheduler dry-run → LLM-auto-invoke OK, no live/exec. Docs validator OK. No routing/scoring change.

## Verdict
`PAPER_PORTFOLIO_BUGFIX_TESTS_PASS`
