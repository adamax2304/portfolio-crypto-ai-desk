# MultiExchangeDerivativesAgent

## File

[src/agents/multi_exchange_derivatives_agent.py](../../src/agents/multi_exchange_derivatives_agent.py).

## Role

Cross-checks Binance, Bybit, OKX derivatives data. Produces a per-symbol multi-venue derivatives summary.

## Inputs

- `multi_derivatives_records` — snapshot from `MultiExchangeDerivativesCollector`.
- `bybit_history` (optional) — multi-bar OI + funding history from `BybitDerivativesCollector`.

## Outputs

Per-symbol summary that includes:

- Each venue's funding + OI + interpretation.
- Cross-venue agreement / divergence.
- Notes used by report builder.

## Used by

- Report renders a "Bybit/OKX derivatives cross-check" block.
- `TradeIdeaAgent` indirectly via the report; not directly in the score path (the primary derivative input is `DerivativesAgent` on Binance).

## Common mistakes

- Treating Bybit funding as primary — `ScoringAgent` caps are on Binance funding.
- Ignoring cross-venue divergence — it often predicts a squeeze in one direction.

## Future improvements

- Add cross-venue funding standard deviation as a feature.
- Add MEXC perp data when supported.

## Related

- [[Derivatives_Agent]]
- [[Bybit_Derivatives_Confirmation]]
- [[Multi_Exchange_Derivatives_Collector]] (referenced; not in vault — it's a collector, not an agent)

## Implemented status

- **Implemented**.
