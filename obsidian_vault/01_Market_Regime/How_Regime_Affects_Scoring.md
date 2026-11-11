# How Regime Affects Scoring

The regime label is fed into `ScoringAgent` in two places: alignment and component weights.

## 1. Alignment factor

Per setup, `_market_alignment(direction, regime)` returns 0.25–0.90 (see [[Long_Short_Neutral_Bias]] table). This is multiplied by the (regime+mode-adjusted) `market_regime` weight.

## 2. Component weight multipliers

`scoring.yaml.regime_weights[regime_label]` provides nudges (0.75–1.30) per component. Final per-component weight is:

```
final_weight[component] = base_weight[component] * regime_multiplier[component] * mode_multiplier[component]
```

Both regime and mode multipliers default to 1.0 if absent. See [[Scoring_Overview]] for the full math.

### Multipliers in effect today

| Regime | momentum | technical_setup | derivatives | catalyst_news | narrative | execution_quality |
|---|---|---|---|---|---|---|
| bullish trend | 1.25 | 1.10 | 0.95 | 1.00 | 1.00 | 1.00 |
| bearish trend | 1.15 | 1.10 | 1.00 | 0.85 | 0.85 | 1.00 |
| range/chop | 0.75 | 1.15 | 1.00 | 1.00 | 0.85 | 1.20 |
| transition | 0.85 | 1.00 | 1.10 | 1.00 | 0.90 | 1.00 |
| high-volatility danger | 0.85 | 1.00 | 1.15 | 1.00 | 0.80 | 1.25 |
| low-volatility compression | 0.90 | 1.15 | 1.05 | 1.00 | 1.00 | 1.00 |

## 3. Risk penalty from regime conflict

If the setup warning list contains the words "conflict" or "fights" (auto-added in `TechnicalSetupAgent` for long-in-bearish and short-in-bullish), `ScoringAgent` adds the `regime_conflict` penalty (default 8).

## 4. Risk agent

`RiskAgent` adds:

- +25 in `high-volatility danger`.
- +25 for long in `bearish trend`.
- +20 for short in `bullish trend`.
- +10 in `transition` or `range/chop` ("breakout failure risk elevated").

This bumps `risk.risk_score`, which feeds `ScoringAgent.risk_penalty += min(risk.risk_score * 0.18, 18)`.

## 5. TradeIdeaAgent risk-level override

In `high-volatility danger`, `risk_level` is forced to `high` regardless of risk_score.

## Net effect

In a bull regime a clean long setup with momentum 75/100 picks up roughly **+5–6 score points** vs a flat regime, while a short in the same regime loses **~8 points** to alignment + warnings + risk.

## Related

- [[Scoring_Overview]]
- [[Long_Short_Neutral_Bias]]
- [[Risk_Agent]]

## Implemented status

- **Implemented**.
