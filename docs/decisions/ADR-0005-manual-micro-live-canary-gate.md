# ADR-0005 — Manual Micro-Live: Canary Review Only After 7–10 Days

## Status
Accepted (2026-06-18)

## Context
Diagnostics and guardrails are deployed (alert-only/shadow), data is now decision-grade for the recent window, but no forward-validated profitable edge exists and the shadow exit evidence is regime-specific. Jumping to live would be premature.

## Decision
Manual micro-live is **not approved**. It may only be **reviewed** (a "canary review") after ≥7–10 days of forward data, and only if every gate item holds:
tests green · scheduler stable · Telegram clean · Control Plane safe · catalyst ASTER flag cleared · circuit-breaker dry-run reasonable · no scalp · no C-tier · no live automation · strict manual-only execution · tiny risk/trade · operator confirms every trade.

## Consequences
- Positive: forces forward evidence + an explicit human checklist before any real risk.
- Negative: slower path to live.
- Not allowed without a new ADR + operator approval: any live execution, even a manual canary, before the gate passes. A passing gate is a *review*, not an automatic enable.

## Evidence
- `reports/POST_FAST_SAFE_ACCELERATION_FINAL_DECISION.md`
- `../PROJECT_STATE.md` → "Manual Micro-Live Gate"
- `docs/WEEKLY_FORWARD_METRICS.md` (forward evidence template)

## Review Date / Gate
Canary review ~2026-06-25 to 2026-06-28 (7–10 days), contingent on the gate. Record the outcome in `DECISION_LOG.md` + `WEEKLY_FORWARD_METRICS.md`.
