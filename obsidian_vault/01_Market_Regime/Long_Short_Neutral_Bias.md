# Long / Short / Neutral Bias

## Where the bias comes from

The desk has **two layered biases**:

1. **Regime bias** — set by `MarketRegimeAgent` and consumed in `ScoringAgent._market_alignment`. Pure function of regime label and trade direction.
2. **Candidate bias** — set by `MomentumScannerAgent` per symbol as `direction_bias` ∈ {long, short, watch}, based on price + RS + extension.

`TechnicalSetupAgent` reads `candidate.direction_bias` and sets `setup.direction`. If the regime conflicts with that direction, a warning is added and `ScoringAgent` applies `regime_conflict` penalty (8).

## Alignment table (from `ScoringAgent._market_alignment`)

| Direction | bullish trend | bearish trend | range/chop | transition | high-vol danger | other |
|---|---|---|---|---|---|---|
| long | 0.90 | 0.25 | 0.58 | 0.58 | 0.35 | 0.35 |
| short | 0.25 | 0.88 | 0.58 | 0.58 | 0.58 | 0.40 |
| watchlist / no-trade | uses `candidate.direction_bias` | — | — | — | — | 0.35 |

Multiplied by `weights["market_regime"] = 15` (default) so a long in `bullish trend` contributes `~13.5` of the regime component; the same long in `bearish trend` contributes `~3.8`.

## Practical heuristics

- In `bullish trend`, default to long. Short setups must be **exceptional** to overcome the 0.25 alignment.
- In `bearish trend`, default to short. Long altcoins almost never survive the score cap chain.
- In `range/chop` and `transition`, neither side is favored; setup quality dominates.
- In `high-volatility danger`, lean short over long, but prefer no trade.

## Hard rules

- Direction is decided **per setup**, not per portfolio. Regime is a multiplier, not a veto.
- If `setup.direction = watchlist_only`, the idea is at most C-tier regardless of score.
- If `setup.direction in {long, short}` but `setup.invalidation is None`, the score cap kicks in → tier = rejected.

## Related

- [[Market_Regime_Overview]]
- [[Scoring_Overview]]
- [[Technical_Setup_Agent]]
- [[Momentum_Scanner_Agent]]

## Implemented status

- **Implemented**.
