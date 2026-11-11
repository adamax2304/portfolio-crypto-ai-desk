# Stocks Intraday Forward Shadow Evaluation

- generated_at: `2026-11-11T20:55:31.144068+00:00`
- activated_at: `2026-09-27T12:20:48.776127+00:00`; forward days: `45.4`
- USD net PnL is authoritative; R is secondary. Only clean, closed, forward rows count as edge.
- Dirty/no-coverage rows and historical backfill are diagnostics, not evidence.
- `REVIEW_ONLY` never changes paper routing, actionability, sizing, or live status.

| entry mode | unique rows | duplicates excluded | clean closed | dirty closed | net USD | PF | win% | max DD $ | fees $ | slip $ | verdict |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|
| PULLBACK_LIMIT | 472 | 144 | 47 | 84 | 195.87 | 1.63 | 60 | 104.52 | 2.84 | 83.09 | REVIEW_ONLY |
  - clean forward gates passed; operator review only, no automatic paper/live change
  - direction evidence: `{"changed": {"closed": 3, "net_pnl_usd": -70.2114, "profit_factor": 0.0, "rows": 3}, "unchanged": {"closed": 44, "net_pnl_usd": 266.0765, "profit_factor": 2.1021, "rows": 166}, "unknown": {"closed": 0, "net_pnl_usd": 0, "profit_factor": null, "rows": 0}}`
| BREAKOUT_CONTINUATION | 67 | 16 | 47 | 0 | 461.28 | 3.41 | 72 | 55.40 | 14.67 | 73.33 | REVIEW_ONLY |
  - clean forward gates passed; operator review only, no automatic paper/live change
  - direction evidence: `{"changed": {"closed": 1, "net_pnl_usd": -4.9808, "profit_factor": 0.0, "rows": 2}, "unchanged": {"closed": 46, "net_pnl_usd": 466.264, "profit_factor": 3.5017, "rows": 65}, "unknown": {"closed": 0, "net_pnl_usd": 0, "profit_factor": null, "rows": 0}}`

## Guardrails

- `legacy_evidence_reused=False` for every slice.
- The evaluator reads shadow outcomes and writes only `stocks_intraday_forward_shadow_evaluations`.
- No automatic promotion: more clean forward evidence is required before any human decision.
