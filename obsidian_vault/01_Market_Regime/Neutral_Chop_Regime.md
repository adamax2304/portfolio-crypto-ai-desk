# Range / Chop Regime

## Conditions

- Breadth above EMA20 between 40 and 60 (inclusive).
- BTC trend may be anything; not gated.

## What the desk does

- `risk_mode = neutral`.
- Style: "mean reversion or wait for clean breakouts".
- Scoring multipliers (`scoring.yaml.regime_weights["range/chop"]`):
  - `momentum × 0.75` (heavily muted)
  - `technical_setup × 1.15`
  - `execution_quality × 1.20`
  - `narrative × 0.85`

## How to trade it

- Prefer range-fade setups: long support, short resistance, both with tight invalidation.
- Demand cleaner R/R because the regime expects failures; ideal ≥ 1.5R to TP1.
- Breakouts are punished by the momentum mute — wait for retest + acceptance.
- Both directions get `_market_alignment ≈ 0.58` — no directional bias from regime alone.

## What invalidates the chop call

- Breadth swings above 60 (with confirming BTC/ETH trend) → `bullish trend`.
- Breadth drops below 40 with BTC downtrend → `bearish trend`.

## Common mistakes

- Sizing as if it were a trend regime — momentum is intentionally suppressed.
- Trading without a defined level — chops eat undefined invalidations.

## Related

- [[Market_Regime_Overview]]
- [[Long_Short_Neutral_Bias]]
- [[How_Regime_Affects_Scoring]]
- [[Execution_Quality]]

## Implemented status

- **Implemented**.
