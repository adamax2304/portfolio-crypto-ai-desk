# MarketRegimeAgent

## File

[src/agents/market_regime_agent.py](../../src/agents/market_regime_agent.py).

## Role

Detects regime from BTC/ETH 4h trend + universe breadth + BTC ATR percentile.

## Inputs

- `market_data: dict[symbol, dict[timeframe, DataFrame]]` — full OHLCV cache.

## Outputs

A `MarketRegime` model:

- `label`, `confidence`, `risk_mode`, `recommended_style`.
- `btc_trend`, `eth_trend`, `alt_breadth`, `volatility`, `key_levels`, `warnings`.

## How it makes decisions

See [[How_Regime_Is_Detected]] for the exact decision tree.

## Used by agents

- `ScoringAgent` for regime alignment + regime multipliers.
- `TechnicalSetupAgent` for direction conflict warnings.
- `RiskAgent` for regime-based risk_score lifts.
- `TradeIdeaAgent` for `risk_level = high` override in `high-volatility danger`.
- `NarrativeAgent` indirectly via candidate momentum (per-candidate score).
- Every report rendering.

## Common mistakes

- Tiny universe → low confidence regime → don't trust it. `alt_breadth.symbols_counted < 8` is the canary.
- BTC frame missing → degraded confidence + warnings. Re-run `update-data`.

## Future improvements

- Wire `low-volatility compression` properly.
- Add 15m or 1h regime overlay for scalp users.

## Related

- [[Market_Regime_Overview]]
- [[How_Regime_Is_Detected]]
- [[How_Regime_Affects_Scoring]]
- [[Long_Short_Neutral_Bias]]

## Implemented status

- **Implemented** (with `low-volatility compression` partial).
