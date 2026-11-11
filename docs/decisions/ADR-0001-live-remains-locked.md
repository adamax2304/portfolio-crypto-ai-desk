# ADR-0001 — Live / Auto-Live / Exchange Execution Remain Locked

## Status
Accepted (2026-06-18)

## Context
The desk runs in paper/shadow mode. Crypto intraday/swing is ~breakeven (PF≈1.0); stocks-intraday is carried by B-tier while C-tier drags; no forward-validated profitable edge exists. The Control Plane ships with live hard-locked (`enable_live_commands=False`, `auto_live_locked=True`).

## Decision
Live trading, auto-live, and any exchange execution stay **locked**. No code path may place, modify, or cancel a real order. Enabling requires an explicit, recorded operator approval + a passed micro-live gate.

## Consequences
- Positive: zero risk of unintended real-money execution; safe to iterate on diagnostics.
- Negative: no real P&L; profitability remains hypothesis-stage.
- Not allowed without a new ADR + operator approval: any execution, leverage on exchange, auto-sizing, or unlocking Control Plane live/commands.

## Evidence
- `reports/POST_FAST_SAFE_ACCELERATION_FINAL_DECISION.md`
- `reports/POST_OPERATIONAL_GUARDRAILS_DEPLOY_FINAL_DECISION.md`

## Review Date / Gate
Revisit only after the Manual Micro-Live Gate in `PROJECT_STATE.md` is fully satisfied and the operator approves a manual canary.
