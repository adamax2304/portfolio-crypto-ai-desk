# High-Volatility Danger Regime

## Conditions

- `BTC ATR percentile ≥ 80` **and** `|BTC 24h return| > 4%`.
- This takes priority over every other label.

## What the desk does

- `risk_mode = danger`.
- Style: "reduce size or no trade until structure settles".
- Scoring multipliers (`scoring.yaml.regime_weights["high-volatility danger"]`):
  - `momentum × 0.85`
  - `execution_quality × 1.25`
  - `derivatives × 1.15`
  - `narrative × 0.80`
- `RiskAgent` adds +25 risk score and an explicit "No fresh entries during high-volatility danger unless size is reduced."

## How to trade it

- Default: skip. Whipsaw probability is structurally high.
- If trading: scalp only, half size, tight stop, take partials at 1R, no swing exposure.
- Long alignment ≈ 0.35, short alignment ≈ 0.58. Shorts get a small structural edge here.
- Critic + Risk almost always lean reject in this regime.

## What invalidates the danger call

- BTC ATR percentile drops below 80 **and** 24h move calms to ≤ 4%.
- Structure re-stabilizes (e.g. clean range printed).

## Common mistakes

- Sizing as usual because the move "looks like trend" — it is volatility, not trend.
- Using normal stops — ATR is large so invalidation jumps wider; R/R math degrades.

## Related

- [[Market_Regime_Overview]]
- [[Risk_Management_Overview]]
- [[Risk_Agent]]
- [[ATR]]

## Implemented status

- **Implemented**.
