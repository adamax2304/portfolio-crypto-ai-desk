# ADR-0006 — Shadow Intelligence Layer

## Status
Accepted (2026-06-18)

## Context
Analysis of another AI-desk suggested 5 context modules — symbol timeline memory,
derivatives trajectory, squeeze phase, thesis/invalidation formatter, on-chain risk.
We want the desk "smarter" (more context per signal) without making the monitor
slower or the trade logic riskier, and while live/trade-math is locked.

## Decision
Add `src/intelligence/` as a **separate shadow/diagnostic/add-only layer**:
- 5 modules + an aggregator (`intelligence_layer.assemble_intelligence_fields`).
- Heavy compute (timeline, derivatives, squeeze, on-chain) runs in **background
  scheduler scripts** (`intelligence_update`, `onchain_risk_update`), writing to a
  dedicated `data/intelligence/intelligence.sqlite`.
- The **alert path reads only pre-computed caches** + a pure deterministic thesis;
  no network, no LLM; time-budgeted with `timeout_partial`; fails open per submodule.
- Fields are **add-only** in the paper-entry payload (`setdefault`), surfaced as
  ≤3 compact Telegram lines and read-only Control-Plane fields.

## Consequences
- Positive: richer per-signal context (phase / derivatives / thesis / timeline /
  on-chain) for analysis + a forward shadow-vs-outcome comparison; p95 enrichment 63ms.
- Negative / limits: funding/OI numeric history is sparse → derivatives slopes mostly
  `unknown` (price-primary, accumulates forward); on-chain has no config →
  `INTERFACE_READY_CONFIG_MISSING`; shadow phase/derivatives are not yet validated.
- Not allowed without a new ADR + operator approval: letting ANY intelligence field
  influence routing, scoring, TP/SL, size, leverage, exits, or live; auto-short on
  phase_3; hard filters.

## Evidence
- `reports/SHADOW_INTELLIGENCE_LAYER_MODULES_IMPLEMENTATION.md`
- `reports/INTELLIGENCE_SCHEDULER_DEPLOYMENT.md`
- `reports/SHADOW_INTELLIGENCE_LAYER_PERFORMANCE_REPORT.md`
- `reports/SHADOW_INTELLIGENCE_LAYER_TEST_RESULTS.md`

## Review Date / Gate
Friday forward comparison (`SHADOW_INTELLIGENCE_FORWARD_COMPARISON_TEMPLATE.md`).
A field may be proposed for **soft warning / review-only** only after it shows forward
predictive value across up+down regimes — default stays keep_shadow.
