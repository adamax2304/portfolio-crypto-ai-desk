# Transition Regime

## Conditions

- The fallback bucket when none of `bullish trend / bearish trend / range/chop / high-volatility danger` match.
- Usually: BTC trending one way, ETH or breadth disagreeing.

## What the desk does

- `risk_mode = mixed`.
- Style: "selective only; demand clean invalidation".
- Scoring multipliers (`scoring.yaml.regime_weights["transition"]`):
  - `momentum × 0.85`
  - `derivatives × 1.10`
  - `narrative × 0.90`

## How to trade it

- Take only setups with confirmed derivatives alignment (funding + OI agree with direction).
- Cap mental size — this regime is structurally lower confidence.
- Both long and short get `_market_alignment ≈ 0.58` (or 0.58 if direction = watch).
- Best edge: confirmed breakout retests, **not** initial breaks.

## What invalidates the transition call

- BTC and ETH converge in trend and breadth ≥ 55 → `bullish trend`.
- BTC trend turns down with breadth ≤ 40 → `bearish trend`.

## Common mistakes

- Treating "transition" as "wait for bullish" — it can resolve down as easily as up.
- Ignoring derivatives — `transition` is the regime where derivatives reads are weighted most relatively.

## Related

- [[Market_Regime_Overview]]
- [[Derivatives_Agent]]
- [[How_Regime_Affects_Scoring]]

## Implemented status

- **Implemented**.
