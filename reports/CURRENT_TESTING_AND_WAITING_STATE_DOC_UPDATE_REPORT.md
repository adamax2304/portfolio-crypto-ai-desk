# Current Testing & Waiting State — Doc Update Report

**Date:** 2026-06-24. Docs-only. No code, no trade logic, no `final_r`, no live touched.

## Files created / updated
- **NEW** `docs/CURRENT_TESTING_AND_WAITING_STATE.md` — 8 sections: (1) current system status, (2) active paper/accounting/display features table, (3) still-testing/waiting table (Model F forward validation, cost/slippage haircut, crypto_intraday_catalyst cohort, circuit-breaker block, sector/concentration caps block, intelligence layer, position advisor, adaptive TP3), (4) archived/superseded (`shadow_exit_manager`), (5) dangerous/locked, (6) operator approval boundaries, (7) next-7-day watchlist, (8) current verdict.
- `PROJECT_STATE.md` — pointer to the new doc in the latest callout.
- `docs/DECISION_LOG.md` — header pointer to the new doc + `config/paper_features.yaml`.
- `docs/SHADOW_MODE_REGISTRY.md` — header pointer (machine registry + plain-English status).
- `docs/WEEKLY_FORWARD_METRICS.md` — header pointer to the new doc.
- `trading-desk-control/README.md` — pointer added to the Paper Features panel note.

## Summary of active features
Model F / `paper_execution_r` (paper accounting); `touch_r` relabel, Paper Features panel, per-trade feature tags, lifecycle/status clarity, close-alert Model F line (display); catalyst label refresh/integrity, funding/OI archive, risk-guard warnings (advisory); cohort guard `warn` label. **All `affects_trades:false`.**

## Summary of still-testing features
Model F forward validation (post-2026-06-24, 7–14d, net-positive after costs, n≥30, stable ≥2 regimes); cost/slippage haircut; crypto_intraday_catalyst cohort (warn → maybe paper_review_only with sign-off); circuit-breaker block (≥10 fires); sector/concentration caps block; intelligence layer (≥30 closed, +2R); position advisor; adaptive TP3 (advisory only).

## Summary of archived / locked
Archived: `shadow_exit_manager` variants A–I (SUPERSEDED_BY_MODEL_F, research-only, not wired). Dangerous/locked: crypto scalp, stocks C-tier, stocks swing/invest actionable; live/auto-live/exchange; production exits; routing/actionability changes — all require explicit operator approval.

## Validation results
- `docs/CURRENT_TESTING_AND_WAITING_STATE.md` exists ✅.
- References present: `config/paper_features.yaml` (3), `config/cohort_guard.yaml` (2), `paper_execution_r` (7), `final_r` (3), `Model F` (12), `shadow_exit_manager` (2), `live_locked` (1) ✅.
- `scripts/check_project_state_docs.py` → `PROJECT STATE DOCS: OK` ✅.
- `pytest tests/test_project_state_docs.py` → 5 passed ✅.

## No-change confirmation
No change to: scoring, entry logic, routing, actionability, production exits, live/auto-live/exchange, historical `final_r`. Documentation only.

## Verdicts
`CURRENT_TESTING_STATE_DOC_CREATED` · `DOCS_UPDATED_FOR_FORWARD_VALIDATION` · `NO_TRADE_LOGIC_CHANGE` · `LIVE_LOCKS_UNCHANGED`
