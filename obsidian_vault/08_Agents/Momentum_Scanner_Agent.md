# MomentumScannerAgent

## File

[src/agents/momentum_scanner_agent.py](../../src/agents/momentum_scanner_agent.py).

## Role

Per-symbol momentum candidate generator: scores price + RS + volume + extension and assigns `direction_bias`.

## Inputs

- `market_data`, `symbols`.

## Outputs

A list of `MomentumCandidate`:

- `symbol`, `direction_bias` ∈ {long, short, watch}.
- `score` (0–100 composite).
- `return_24h`, `return_7d`, `relative_strength_btc`.
- `volume_ratio`, `distance_from_ema20_atr`.
- `reason_tags[]`, `warnings[]`, `rank`.

## How it makes decisions

- Computes per-symbol pct_return on different windows.
- Reads volume_ratio vs SMA20.
- Computes EMA20-distance in ATR.
- Combines into a composite score.
- Tags direction_bias from trend + RS + extension.
- Outputs ranked candidate list (sorted by score).

## Used by agents

- `TechnicalSetupAgent` consumes the candidate list to build entry plans for the top N.
- `NarrativeAgent` uses candidates' membership in narratives + their scores.
- `CrowdAttentionAgent` consumes them for momentum gating.
- `ScoringAgent` reads `candidate.score` into the momentum component.

## Common mistakes

- Reading only the top of the candidate list and assuming low-rank candidates are tradable — `TechnicalSetupAgent` may reject them on ATR / extension.
- Treating `direction_bias = watch` as a trade direction.

## Future improvements

- Add RSI-state metric.
- Add session-of-day weighting.
- Add multi-timeframe RS (24h + 7d combined).

## Related

- [[Agents_Overview]]
- [[Relative_Strength]]
- [[Volume_Anomaly]]
- [[Candidate_Ranking_Agent]]

## Implemented status

- **Implemented**.
