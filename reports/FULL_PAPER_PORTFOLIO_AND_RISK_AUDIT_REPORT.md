# Full Paper Portfolio + Risk Audit (PART 11)

**Date:** 2026-06-24. Post-implementation audit + bugfixes.

## Crypto desk
- `paper_execution_r` correct — unchanged Model F; 88 tests pass incl. prior Model F suite.
- Portfolio equity updates correct — net USD = R × actual_risk − costs; verified by tests + backfill.
- No double-counting / duplicate signals — economic-key dedup (most-resolved) before sim; ledger `UNIQUE(economic_trade_key,event_type,fee_profile)`; `replace_ledger` clears per-profile before insert (idempotent — re-run yields identical 586 rows).
- No `final_r` rewrite — `signal_outcomes` has no paper column; only appended rows.
- Fees correct — per-side open+close + per-tier slippage (tested).
- Sizing correct — worked examples match (notional 1250 @ 2% stop; capped @ <0.5%).
- Dynamic leverage sane — min int for margin cap, clamped 1..5; liquidation buffer flagged.
- Model F tests still pass.

## Control Plane
- Dashboard portfolio cards = ledger values (equity $5146.78 etc.).
- `/api/portfolio`, `/api/portfolio/trades`, `/api/trades/{id}/chart-events` return correct shapes; fallback when ledger absent (no silent zero).
- Headline = Paper Execution R / portfolio equity; touch R remains labelled "optimistic" (not headline).
- Frontend build clean.

## Bugs found & fixed during build
1. **"zero" fee profile still applied slippage** → BE-in-R trades wrongly counted as losses + the "no-cost" baseline wasn't truly cost-free. Fixed: `simulate_portfolio` zeroes slippage when `fee_profile == "zero"`.
2. **`close_alert.py` Paper-$ line used undefined `_to_float`** → would NameError and the line would never render (silently caught). Fixed with a local `_tf` helper.
3. **Frontend missing `usePortfolio` import** → tsc build error. Fixed import.

## Operational
- Single scheduler instance; backend health 200, live_locked:true; ledger fresh (586 rows); live locked.

## Verdict
`FULL_PORTFOLIO_RISK_AUDIT_COMPLETE`
