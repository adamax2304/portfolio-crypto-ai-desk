# Shadow Promotion — Doc Update Report (PART 9)

**Date:** 2026-06-19.

## Docs updated / created
- **`docs/SHADOW_MODE_REGISTRY.md`** (NEW) — single source of truth for every shadow/advisory/display/locked-policy feature + its promotion state + the gate to promote it.
- **`PROJECT_STATE.md`** — added the audit blockquote: SAFE_PROMOTIONS_ONLY, NO_LIVE_EXECUTION_ENABLED, window too short (5 closed actionable decisions), nothing trade-affecting promoted, no trade-math change.
- **`docs/DECISION_LOG.md`** — row: trade-affecting features held NEED_MORE_DATA/KEEP_SHADOW; registry created.
- **`docs/WEEKLY_FORWARD_METRICS.md`** — Friday checklist item: re-evaluate shadow modes once ≥15/≥30 closed actionable decisions exist; promote only with a proof report.

## What the docs now state
- **What was evaluated:** all shadow/advisory modes (intelligence, risk guards, lifecycle, profit protection/exits, playbook/sizing, catalyst, Agent Council).
- **What was promoted:** only display/advisory (already live).
- **What stayed shadow / needs more data:** every trade-affecting feature.
- **What to check Friday:** re-evaluate at ≥15/≥30 closed decisions.
- **Live/execution:** not enabled; hard-locked.

Docs validator: **OK**. `test_project_state_docs`: green (re-run in PART 8/final).
