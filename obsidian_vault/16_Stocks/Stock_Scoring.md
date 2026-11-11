# Stock Scoring

[src/stocks/agents/scoring_agent.py](../../src/stocks/agents/scoring_agent.py) is the only place that converts upstream agent outputs into a final 0–100 score and a tier label.

## Base weights (config/stocks/scoring.yaml → weights)

| Component | Weight |
|---|---|
| market_regime_alignment | 15 |
| index_confirmation | 10 |
| sector_confirmation | 10 |
| relative_strength | 15 |
| technical_setup | 20 |
| volume_relative_volume | 10 |
| news_catalyst | 10 |
| earnings_risk_adjustment | 0 (signed) |
| risk_reward | 10 |
| data_confidence | 10 |

Sum ≈ 100 before penalties and multipliers.

## Mode multipliers

`config/stocks/scoring.yaml → mode_weights[mode][component]` applies on top of the base weight. Examples:

- **intraday** boosts `technical_setup` ×1.10, `volume_relative_volume` ×1.15, `news_catalyst` ×1.10
- **swing** boosts `sector_confirmation` ×1.10 and `earnings_risk_adjustment` ×1.30
- **invest** boosts `market_regime_alignment` ×1.10 and softens `technical_setup` ×0.85

## Regime multipliers

`regime_weights[regime][component]`:

- **risk_off** → `relative_strength` ×1.15 (winners stand out in weak tape)
- **bullish** → `relative_strength` ×1.05, `technical_setup` ×1.05
- **chop** → `technical_setup` ×0.90 (breakouts fail more often)
- **high_volatility** → `risk_reward` ×1.10 (demand bigger reward)

## Final score formula

```
component_value = raw[0..1] × base_weight × mode_multiplier × regime_multiplier
base_total = sum(component_values)
final = base_total + risk_penalty   # penalty is negative
final = apply_caps(final, blocks)
```

## Caps (config → caps)

- `max_score_if_data_partial: 70` — applied when blocks include `no_invalidation`
- `max_score_if_earnings_active: 60` — applied for `earnings_today_blocks_swing`
- `max_score_if_macro_event_today: 70`

## Tier thresholds

- **A** ≥ 80
- **B** ≥ 65
- **C** ≥ 50
- **rejected** otherwise

Plus: if `blocks` is non-empty, tier is forced to **rejected** regardless of score.

## Confidence label

- **high** if base_total ≥ 80 and no blocks
- **medium** if base_total ≥ 60 and no blocks
- **low** otherwise (or any blocks)

## How to tune

If A-tiers feel too easy or rejections too aggressive, edit the YAML — no code changes needed. Re-run the report to see the new distribution. Keep an eye on `signal-stats --asset-class stocks` after enough A/B ideas are tracked.
