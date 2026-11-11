# Mode-Specific Scoring

See [[Mode_Specific_Scoring]] (sibling under `02_Trading_Modes`) for full table. This file is the scoring-system view; it points to the same data.

## Mode multipliers (from scoring.yaml.mode_weights)

| Mode | momentum | execution_quality | catalyst_news | narrative | market_regime |
|---|---|---|---|---|---|
| scalp | 1.20 | 1.20 | 0.80 | 0.75 | 1.00 |
| intraday | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| swing | 0.90 | 1.00 | 1.20 | 1.30 | 1.15 |

## Implication for the score

- Intraday is the calibration baseline.
- Scalp tilts toward momentum + execution; narrative is muted.
- Swing tilts toward narrative + catalyst + regime alignment; momentum is muted.

## How to apply when re-evaluating an idea

- Match the mode the idea was generated in. Do not "re-score in scalp" a swing idea.
- The mode is stored on the idea (`idea.mode`) and on the trade-idea-agent payload (`payload.mode`).

## Related

- [[Mode_Specific_Scoring]] (sibling, fuller)
- [[Scoring_Overview]]
- [[Trading_Modes_Overview]]

## Implemented status

- **Implemented**.
