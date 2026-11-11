# Shadow Feature Promotion Gates (PART 4)

**Date:** 2026-06-24.

## Paper promotion gate (trade-affecting features)
A feature may move to a paper trade-affecting state ONLY if ALL hold:
1. `paper_execution_r` improvement **> +2R** on ≥30 affected closed trades, OR a clear safety/clarity benefit (display/accounting).
2. n ≥ 30 affected trades (waived for display-only).
3. PF improvement OR drawdown reduction.
4. No single-symbol dependency (no symbol > ~20% of the effect).
5. No catastrophic false-positive risk.
6. Does NOT enable live/auto-live/exchange execution.
7. Feature flag exists (default-off / reversible).
8. Tests exist.
9. Rollback is one config flip.
10. App/Telegram can display it clearly.

## Immediate paper implementation allowed ONLY for
- display / read-model features;
- accounting features;
- non-trading annotation features;
- risk features already proven in replay **with no production order impact**.

## Do NOT promote if
- n too small;
- evidence is touch-based only;
- effect disappears under `paper_execution_r`;
- feature hurts Model F;
- requires production/live order logic;
- changes actionability/routing without explicit approval.

## Application to this audit
- **Model F / paper_execution_r / touch relabel / status clarity / risk-guard warnings / catalyst labels** → pass as **display/accounting/advisory** (no trade impact) → already active.
- **cohort guard warn** → display-only (label, no routing) → passes the display path.
- **circuit-breaker block, sector-cap block, position advisor, intelligence layer** → fail gate #1/#2 (no ≥+2R / n evidence) → stay shadow.
- **shadow exit manager A–I** → fails ("effect disappears / hurts vs Model F") → archive.
- **scalp / C-tier / stocks swing-invest actionable** → fail #5/#6 + explicit lock → dangerous, stay locked.

## Verdict
`PROMOTION_GATES_DEFINED`
