# Position Sizing

## Status

The desk does **not** size positions. There is no code that emits a dollar / coin quantity.

`TradeIdea.risk_level` ∈ {`low`, `medium-low`, `medium`, `high`} is the only sizing hint; you must translate it to actual capital.

## Suggested rule of thumb

Let `base_risk = 1%` of trading account (your call; not enforced).

| risk_level | Suggested risk per trade |
|---|---|
| low | 1.0 × base_risk |
| medium-low | 0.85 × base_risk |
| medium | 0.7 × base_risk |
| high | 0.4 × base_risk (or skip) |

Then position size = `(risk_per_trade) / (entry - invalidation)`, expressed in the symbol's base.

## Why this is not in code

- The desk does not custody account balances.
- It does not know your leverage / margin model.
- It does not know your other open exposure.
- It is research-only.

## What the desk does help with

- Provides `entry_low`, `entry_high`, `invalidation` so risk distance is precise.
- Provides `risk_level` and `risk_score` so you can scale.
- Provides `data_confidence` so you know how much trust the inputs deserve.

## Common mistakes

- Sizing the same in every regime — in `high-volatility danger`, halve at minimum.
- Using leverage to "fix" a wide stop — better to skip the setup.
- Adding to a losing position because "the thesis is intact". The desk's invalidation is the thesis death.

## Future improvements

- Add a `recommended_risk_pct` field to `TradeIdea` derived from regime + risk_level + data_confidence.
- Add a paper-trading book module that tracks % at risk across open ideas.

## Related

- [[Risk_Management_Overview]]
- [[Stop_Loss_Logic]]
- [[Invalidation]]
- [[Risk_Reward]]

## Implemented status

- **Recommended** (not implemented).
