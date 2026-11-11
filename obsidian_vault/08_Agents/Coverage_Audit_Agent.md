# CoverageAuditAgent

## File

[src/agents/coverage_audit_agent.py](../../src/agents/coverage_audit_agent.py).

## Role

Names which data subsystems are healthy, partial, or missing. The truth-telling layer of the desk.

## Inputs

- `latest_update` — `data/processed/market_summary/last_update.json`.
- `market_data`, `derivatives`, `social_attention`, `multi_derivatives_records`.

## Outputs

A report-friendly summary that calls out:

- OHLCV per exchange — fetched vs failed counts.
- Derivatives per exchange — fetched vs failed counts.
- RSS news — sources OK vs failed.
- Social — sources OK vs failed.
- Manual events — count loaded this run.
- news_trader_bridge — available / unavailable.
- Major blindspots — items the desk explicitly does NOT have (liquidation maps, on-chain flows, paid social, unlocks).

## How to read it

- Healthy: every subsystem ≥ 80% data coverage.
- Partial: 50–80%; reduce sizing.
- Degraded: < 50%; halt new entries.

## Used by

- Report builder.
- LLMs reading `context_for_llm.md` to assess trust.

## Common mistakes

- Skipping this block. It is the single most useful "should I trade today?" signal.

## Future improvements

- Per-symbol coverage matrix (which symbols are missing which streams).
- Auto-throttle: if coverage degrades, force-cap all ideas at C.

## Related

- [[Exchange_Failure_Handling]]
- [[Data_Confidence]]

## Implemented status

- **Implemented**.
