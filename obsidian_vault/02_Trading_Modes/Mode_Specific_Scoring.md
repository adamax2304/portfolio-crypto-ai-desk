# Mode-Specific Scoring

See [[Scoring_Overview]] for the full math. This page lists only the multipliers that differ per mode.

## `scoring.yaml.mode_weights`

| Mode | momentum | execution_quality | catalyst_news | narrative | market_regime |
|---|---|---|---|---|---|
| scalp | 1.20 | 1.20 | 0.80 | 0.75 | 1.00 |
| intraday | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| swing | 0.90 | 1.00 | 1.20 | 1.30 | 1.15 |

Components not listed (e.g. `technical_setup`, `derivatives`) keep their base weight.

## Net effect, holding score components constant

For a hypothetical candidate with strong momentum + clean setup + medium narrative + verified catalyst, the same setup scored across modes shifts by roughly:

- scalp vs intraday → +3 to +5 score points (momentum + execution lift).
- swing vs intraday → +2 to +4 score points (narrative + catalyst + regime lift), but only if narrative is actually hot.

Conversely, a candidate with **no narrative and no catalyst** scores **better in scalp** than swing because swing's heavier narrative + catalyst weight on missing data hits harder.

## Why intraday is the baseline

Intraday is calibrated against the desk's history: at score ≥ 80 with no caps, you should get high-quality intraday trade ideas. Scalp and swing are tilted versions of the same calibration, not separate scales.

## Interaction with regime

Mode and regime multipliers multiply together. Example: scalp + bullish trend → momentum component weight = `15 * 1.20 (mode) * 1.25 (regime) = 22.5`. Tilt the desk hard toward momentum-strong intraday-lookalike longs in a bull tape during scalp mode.

## Implication for LLM trade evaluation

When evaluating a saved idea, **never mix modes**. A swing idea read with intraday eyes will look thinner because narrative weight drops. Stick to the mode the idea was produced in.

## Related

- [[Scoring_Overview]]
- [[How_Regime_Affects_Scoring]]
- [[Scalp_Mode]]
- [[Intraday_Mode]]
- [[Swing_Mode]]

## Implemented status

- **Implemented**.
