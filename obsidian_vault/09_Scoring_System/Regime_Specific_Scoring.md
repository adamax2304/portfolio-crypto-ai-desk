# Regime-Specific Scoring

See [[How_Regime_Affects_Scoring]] for the full multiplier table. This page is the scoring-side perspective.

## Regime as a global multiplier set

For each component, the regime contributes a multiplier between 0.75 and 1.30 (typical). These multipliers stack with mode multipliers and with the base weight.

## Alignment factor adds on top

`_market_alignment(direction, regime)` returns a number 0.25–0.90. This is the **quality** factor for the `market_regime` component, not a multiplier. It's already weighted by `weights["market_regime"]` (default 15) which is itself multiplied by the regime+mode multiplier.

So a long in `bullish trend`:

```
component = alignment × weight × regime_mult × mode_mult
          = 0.90 × 15 × 1.00 × 1.00
          = 13.5
```

A short in the same bullish regime:

```
= 0.25 × 15 × 1.00 × 1.00
= 3.75
```

A ~10-point swing on the regime component alone.

## How LLMs should reason about this

- Direction-vs-regime is the **biggest** structural lever in the score.
- Then setup quality (20 base × 1.10 in trending regimes).
- Then momentum + derivatives (15 each, but momentum × 1.25 in bullish, × 0.75 in chop).
- Catalyst + narrative + execution are smaller.

## Related

- [[Scoring_Overview]]
- [[How_Regime_Affects_Scoring]]
- [[Long_Short_Neutral_Bias]]

## Implemented status

- **Implemented**.
