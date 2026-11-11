# ExchangeFusionAgent

## File

[src/agents/exchange_fusion_agent.py](../../src/agents/exchange_fusion_agent.py).

## Role

Cross-exchange confirmation. Builds `ExchangeConfirmation` per symbol from fused candidate per-venue data.

## Inputs

- `fused_candidates: list[dict]` — from `universe_ranked_candidates.json`. Each row has `per_exchange: {exchange: {change_24h, volume_anomaly, liquidity_score, risk_flags, ...}}`.
- `exchange_symbol_map: dict[symbol, list[exchanges]]` — from `exchange_symbol_map.json`.

## Outputs

`dict[symbol, ExchangeConfirmation]`:

- `exchanges_listed[]`, `anchor_listed`, `derivatives_listed`, `discovery_listed`, `high_risk_only`.
- `price_consistency`, `volume_consistency` (0–1).
- `confirmation_score` (0–100).
- `best_exchange_for_data`, `suggested_exchange_focus`.
- `risk_flags[]` (mexc_only / not_on_anchor / no_derivatives_confirmation / price_divergence_across_exchanges).
- `interpretation`.

## How it computes (verbatim)

See [[Cross_Exchange_Confirmation]] for the exact math.

## Used by agents

- `ScoringAgent`:
  - `high_risk_only` → cap 70/65.
  - `not anchor_listed AND not high_risk_only` → cap 75.
- `TradeIdeaAgent`:
  - `exchange_focus = suggested_exchange_focus`.
  - `exchanges_confirmed = exchanges_listed`.
  - `data_confidence` adds points for `anchor_listed` and `derivatives_listed`.

## Common mistakes

- Trading on a different venue than `suggested_exchange_focus`.
- Ignoring `price_divergence_across_exchanges` — it usually means one venue is lagging or being manipulated.

## Future improvements

- Add MEXC derivatives confirmation when MEXC perps are pulled.
- Add an "OK to trade on" venue list per symbol (slippage-aware).

## Related

- [[Cross_Exchange_Confirmation]]
- [[Exchange_Overview]]
- [[MEXC_Only_Risk]]

## Implemented status

- **Implemented**.
