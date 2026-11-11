# Stocks Pre-US OpenRouter Agent

Implemented an autonomous, structured pre-US review for stock intraday plans.

## Runtime flow

1. At 08:50 ET the scheduled wrapper builds and freezes the candidate bundle.
2. Deterministic hard gates and a zero-adjustment baseline are persisted first.
3. Existing quality agents attach entity/news, event-risk, and market-regime evidence.
4. OpenRouter reviews each remaining candidate and returns a strict JSON verdict.
5. Code derives the positive-adjustment evidence flags; the model cannot assert them.
6. Verdicts enter through `stocks_preus_review.record_verdicts`, which clamps scores,
   recomputes tiers, applies TTLs, and refreshes `stocks_preus_actionability`.
7. Paper/live stock routing continues to require the normal opening confirmation.

## Safety boundaries

- The model cannot create a signal, assign a tier, change geometry, size, or place an order.
- A network/model failure preserves the deterministic baseline and records an error audit row.
- Every request/response is stored in `quality_agent_llm_assessments`.
- Final verdict/actionability remains in the existing `stocks_preus_review` and
  `stocks_preus_actionability` tables.
- The legacy Claude Desktop scheduled task is disabled; the OpenRouter task is enabled.

## Verification

- OpenRouter smoke: strict schema returned by `anthropic/claude-sonnet-5`.
- Pre-US/overnight/actionability regression tests: 184 passed.
- Quality-agent and default-scheduler regression tests: 209 passed.
