# ADR-0003 — Stocks-Intraday C-Tier → Shadow/Review-Only (Explicit Policy)

## Status
Accepted (2026-06-18)

## Context
A 30d stocks-intraday breakdown: all = +106R, B-tier = +132R, A-tier = +8R, **C-tier = −34R** (drop-C-tier counterfactual +140R). Investigation showed C-tier was **already** non-actionable: `decide_paper_entry` returns `should_send=False` ("tier=C not actionable") for all C-tier, the stocks monitor filters alerts to A/B, and the Control Plane classifies C-tier non-actionable. So the −34R is a tracking/measurement artifact, not live exposure.

## Decision
Make the restriction an **explicit, configurable, labeled policy**: `config/signal_tracking.yaml` → `tier_policy.stocks_intraday_c_tier: shadow_review_only` + `src/signals/tier_policy.py` + add-only payload labels (`c_tier_restriction_applied`, reason, `diagnostic_or_policy`). Routing/label only — no scoring, tier, TP/SL, or size change. A/B stocks and all crypto tiers untouched.

## Consequences
- Positive: single source of truth + visibility; reversible via one config line (`actionable`).
- Negative: none material (behavior already was this).
- Not allowed without a new ADR: changing scoring/tiering, or restricting A/B, or touching crypto tier routing.

## Evidence
- `reports/STOCKS_INTRADAY_C_TIER_SHADOW_IMPLEMENTATION.md`
- `reports/STOCKS_INTRADAY_SAFE_RESTRICTION_PLAN.md`
- `reports/STOCKS_INTRADAY_REWORK_DIAGNOSTIC.md`

## Review Date / Gate
Optional follow-up (separate decision): stop *registering/tracking* C-tier stocks-intraday to clean the measured book (reduces measurement data — needs approval). Revisit if A/B stocks-intraday performance degrades.
