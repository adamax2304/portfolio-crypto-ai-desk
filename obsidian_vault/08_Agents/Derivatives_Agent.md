# DerivativesAgent

## File

[src/agents/derivatives_agent.py](../../src/agents/derivatives_agent.py).

## Role

Per-symbol derivatives summary from Binance USD-M futures.

## Inputs

- `market_data` — for price context.
- `raw_records: dict[symbol, dict]` — `{premium_index, open_interest, open_interest_hist, long_short_ratio}` for each symbol from `BinanceDerivativesCollector`.

## Outputs

`DerivativesSummary` per symbol:

- `data_available`, `funding_rate`, `open_interest`, `oi_change_pct`, `price_change_pct`, `long_short_ratio`.
- `interpretation`, `crowding_risk`, `squeeze_potential`.
- `alignment_score` ∈ [-1, +1].
- `warnings[]`.

## How it makes decisions

- Maps funding bands to `crowding_risk` labels and alignment adjustments (see [[Funding_Rate]]).
- Computes OI change % and maps `(price_24h, oi_change_24h)` to an interpretation (see [[Open_Interest_Risk]]).
- Adjusts alignment if funding is extreme.
- Warns when long/short ratio is heavily skewed.

## Used by agents

- `ScoringAgent`: derivative component = `weights["derivatives"] * derivative_quality`, where `derivative_quality` depends on `alignment_score`.
- `ScoringAgent`: extreme funding caps (78) check the `funding_rate` directly.
- `RiskAgent`: bumps risk_score on extreme/elevated crowding.
- `CrowdAttentionAgent`: feeds `_crowding_risk` and evidence.

## Common mistakes

- Treating `data_available = False` as bearish — it just means we have no read.
- Reading the snapshot funding without history — funding history is in Bybit's dedicated collector, not Binance.

## Future improvements

- Add Binance top-trader long/short ratio.
- Add 8h funding trajectory (slope).
- Add per-symbol open-interest dollar value.

## Related

- [[Multi_Exchange_Derivatives_Agent]]
- [[Funding_Rate]]
- [[Open_Interest]]
- [[Funding_Risk]]
- [[Open_Interest_Risk]]

## Implemented status

- **Implemented**.
