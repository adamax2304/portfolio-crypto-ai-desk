# ADR-0002 — Profit Protection (BE / Partial / Trailing) Stays Disabled

## Status
Accepted (2026-06-18)

## Context
Recent crypto losses are mostly exit-management (tight stops, no profit protection). A path-aware replay (now 100% coverage on 146 crypto intraday/swing trades, 5m archive) shows BE-after-0.5R / partial-TP1 / BE-after-1R reduce drawdown vs the shadow baseline. **But** the shadow baseline (A_current −39R, 5m + conservative stop-first) is pessimistic vs the actual recorded book (+6R) for the same trades, and the tested 30d window was net-losing — so only relative deltas are valid and no variant is profitable, only less-bleeding.

## Decision
`partial_exit_model.enabled` stays **false**. BE / partial / trailing are NOT added to real trade logic. They remain **shadow-only** measurement.

## Consequences
- Positive: no risk of clipping winners in a trending regime on unproven evidence.
- Negative: known give-back (reach +1R then back to −1R) continues until a rule is proven.
- Not allowed without a new ADR + approval: enabling any BE/partial/trailing in `src/signals` execution or flipping `partial_exit_model.enabled`.

## Evidence
- `reports/POST_BACKFILL_PROFIT_PROTECTION_REPLAY.md`
- `reports/SHADOW_EXIT_LEDGER_SUMMARY.md`

## Review Date / Gate
Revisit after: (a) the 5m-shadow-vs-tracker timeframe gap is reconciled so absolute R is trustworthy, AND (b) a candidate (partial-TP1 or BE-after-1R) is net-positive across an up/trending month, not just this losing window. Then shadow-forward first; enable only with operator approval.
