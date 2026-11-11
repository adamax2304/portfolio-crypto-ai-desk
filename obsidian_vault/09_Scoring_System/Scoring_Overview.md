# Scoring Overview

The desk's score is **transparent** and entirely deterministic. See [config/scoring.yaml](../../config/scoring.yaml) and [src/agents/scoring_agent.py](../../src/agents/scoring_agent.py).

## Final score formula

```
for each component (market_regime, technical_setup, momentum, derivatives,
                    catalyst_news, narrative, execution_quality):
    final_weight = base_weight
                 * regime_multiplier[regime.label][component]   # default 1.0
                 * mode_multiplier[mode][component]              # default 1.0
    component_value = quality_factor[component] * final_weight

total = sum(component_values) - risk_penalty
apply score caps (lowest active cap wins)
clamp to [0, 100]
```

## Base weights (config/scoring.yaml.weights)

| Component | Base weight |
|---|---|
| market_regime | 15 |
| technical_setup | 20 |
| momentum | 15 |
| derivatives | 15 |
| catalyst_news | 15 |
| narrative | 10 |
| execution_quality | 10 |

Total possible **before** caps and penalties: 100.

## Regime multipliers

See [[How_Regime_Affects_Scoring]] for the table.

## Mode multipliers

See [[Mode_Specific_Scoring]] for the table.

## Quality factors per component

| Component | Quality factor |
|---|---|
| market_regime | `_market_alignment(direction, regime)` ∈ {0.25 … 0.90} |
| technical_setup | `setup.setup_quality / 100` |
| momentum | `candidate.score / 100` |
| derivatives | `(alignment + 1) / 2` clamped 0.15–1.0; fallback 0.6 if missing |
| catalyst_news | `baseline + importance/10`, minus 0.25 if risk_events; baseline 0.3 |
| narrative | `best_narrative.heat_score / 100`, minus 0.2 if narrative risk_score ≥ 65; clamp 0.1–1.0 |
| execution_quality | `min(rr_to_tp1 / 2, 1.0)`, fallback 0.65 |

## Risk penalties (config/scoring.yaml.risk_penalties)

| Trigger | Penalty |
|---|---|
| regime_conflict | 8 |
| overextended | 8 |
| poor_risk_reward | 10 |
| low_liquidity | 8 |
| no_clear_invalidation | 15 |
| missing_derivatives | 2 |
| missing_news | 2 |
| too_many_warnings | 5 |

Plus dynamic penalty `min(risk.risk_score * 0.18, 18)` from `RiskAgent`.

Plus critic-driven: reject verdict +10, weak_signal_dependency +4, late_or_crowded +5.

## Thresholds (config/scoring.yaml.thresholds)

- `a_tier`: 80
- `b_tier`: 65
- `c_tier`: 50
- `strong_idea`: 85 (legacy)
- `valid_idea`: 70 (legacy)
- `watchlist_only`: 55 (legacy)

A-tier requires the score ≥ 80 **and zero active caps**.

## Confidence labels

- ≥ 85 → high
- ≥ 75 → medium-high
- ≥ 60 → medium
- else → low

## Related

- [[Score_Breakdown]]
- [[Score_Caps]]
- [[A_Tier_Setups]]
- [[B_Tier_Setups]]
- [[C_Tier_Watchlist_Setups]]
- [[Rejected_Setups]]
- [[Data_Confidence]]
- [[Telegram_News_Score_Adjustments]]
- [[Regime_Specific_Scoring]]
- [[Mode_Specific_Scoring]]
- [[Scoring_Agent]]

## Implemented status

- **Implemented**.
