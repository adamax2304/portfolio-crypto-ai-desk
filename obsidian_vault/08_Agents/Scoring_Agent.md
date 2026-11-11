# ScoringAgent

## File

[src/agents/scoring_agent.py](../../src/agents/scoring_agent.py).

## Role

Single source of truth for `final_score`, `tier`, `cap_reasons`, `reasons[]`, `warnings[]`, `risk_penalty`.

## Inputs

- `setups`, `candidates`, `regime`, `derivatives`, `catalysts`, `risks`, `critiques`, `narratives`.
- `exchange_confirmations` (from `ExchangeFusionAgent`).
- `mode: str`.
- `data_freshness_minutes: float | None`.

## Components

Default base weights (overridable by regime / mode multipliers — see [[Scoring_Overview]]):

- market_regime 15
- technical_setup 20
- momentum 15
- derivatives 15
- catalyst_news 15
- narrative 10
- execution_quality 10

## Score formula

```
final_weight = base * regime_multiplier * mode_multiplier
component_value = quality_factor * final_weight
total = sum(components) - risk_penalty
apply caps (min of all active caps)
clamp to [0, 100]
```

## Quality factors

- `market_regime` — `_market_alignment(direction, regime)` ∈ {0.25, 0.4, 0.58, 0.88, 0.90}.
- `technical_setup` — `setup.setup_quality / 100`.
- `momentum` — `candidate.score / 100`.
- `derivatives` — based on `alignment_score` and direction; clamp 0.15–1.0; fallback baseline 0.6.
- `catalyst_news` — `min(1.0, baseline + importance/10)`; reduced if risk_events present.
- `narrative` — `best_narrative.heat_score / 100`; reduced if narrative risk_score ≥ 65.
- `execution_quality` — `min(rr_to_tp1 / 2, 1.0)`, fallback 0.65.

## Caps (in order of evaluation; lowest wins)

| Condition | Cap |
|---|---|
| Setup invalidation missing AND direction in {long, short} | 50 |
| Direction not in {long, short, watchlist_only, no_trade} | 50 |
| MEXC-only listing | 70 (65 if technical_setup component < 14) |
| Not on anchor exchange (and not MEXC-only) | 75 |
| Low liquidity in risk warnings | 60 |
| `data_freshness_minutes > 180` | 50 (stale data) |
| Catalyst contains "rumor" AND verification ∈ {none, rumor, single_source} AND no risk_events | 55 |
| Funding > +0.001 AND direction == long | 78 |
| Funding < -0.001 AND direction == short | 78 |

If any cap fires and the score exceeds it, score is set to the cap and a `cap_reasons` line is added.

## Tier assignment

```
if invalidation_missing OR stale_cap:
    tier = rejected
elif direction in {long, short} AND total >= a_tier_threshold (80) AND no caps:
    tier = A
elif direction in {long, short} AND total >= b_tier_threshold (65):
    tier = B
elif total >= c_tier_threshold (50):
    tier = C
else:
    tier = rejected
```

## Confidence

- ≥ 85 → high
- ≥ 75 → medium-high
- ≥ 60 → medium
- else → low

## Used by agents

- `TradeIdeaAgent` consumes scores 1:1.
- `WatchlistMonitor` reads stored scores to detect upgrades.
- Report renders score components per idea.

## Common mistakes

- Trying to override a cap "for one symbol" — caps are non-negotiable.
- Ignoring `data_quality` — when it says `acceptable`, multiple components are missing.

## Future improvements

- Re-calibrate weights periodically against actual outcomes (a desk learning loop).
- Per-mode setup_timeframe (currently global) would let `setup_quality` be more accurate.

## Related

- [[Scoring_Overview]]
- [[Score_Caps]]
- [[A_Tier_Setups]]
- [[B_Tier_Setups]]
- [[C_Tier_Watchlist_Setups]]
- [[Rejected_Setups]]

## Implemented status

- **Implemented**.
