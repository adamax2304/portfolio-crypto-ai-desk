# Paper Risk Upgrade — Doc Update Report (PART 10)

**Date:** 2026-06-24.

## Updated
- **`PROJECT_STATE.md`** — Last Updated → 2026-06-24; new callout: paper-risk upgrade verdicts, Model F definition, files, locks intact, `final_r` not rewritten, forward-validation pending.
- **`docs/DECISION_LOG.md`** — new Active row: `paper_execution_r` (Model F) is authoritative paper PnL; touch `final_r` relabelled optimistic; paper/accounting only; no live/exec/rewrite.
- **`docs/WEEKLY_FORWARD_METRICS.md`** — new "Paper execution accounting (Model F)" block: track forward `paper_execution_r`, paper-vs-touch divergence, protected/stops-avoided, `paper_unavailable_n` stays 0, cost-haircut gate, weak-cohort watch.
- **`docs/SHADOW_MODE_REGISTRY.md`** — note: early-MFE-protection graduated from shadow-candidate to **active paper accounting** (display/accounting only; NOT a production exit).
- **`trading-desk-control/README.md`** — note: dashboard headline is now Paper Execution R (Model F); Touch R is secondary/optimistic.

## Docs assert
- old `final_r` is **touch-based** (highest TP touched, optimistic — not real PnL);
- new main paper PnL = **`paper_execution_r`** (Model F);
- Model F is active for **paper accounting only**;
- **live/execution still off**; no historical `final_r` rewrite;
- **next 7 days:** watch forward paper_execution_r (Operator), paper-vs-touch divergence, protected counts, `paper_unavailable_n`=0, apply cost haircut before any paper-flag, watch the chase-long cohort.

Docs validator: `PROJECT STATE DOCS: OK`.

## Verdict
`DOCS_UPDATED_FOR_PAPER_RISK_UPGRADE`
