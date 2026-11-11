# Data Confidence

A composite score the desk uses to gate confidence claims.

## Where computed

`TradeIdeaAgent._data_confidence(derivative, catalyst, confirmation, score)`:

| Condition | +points |
|---|---|
| `derivative.data_available == True` | +1 |
| `catalyst.catalysts or catalyst.risk_events` | +1 |
| `confirmation.anchor_listed == True` | +1 |
| `confirmation.derivatives_listed == True` | +1 |
| `score.data_quality == "strong"` | +1 |

Then maps:

| Points | data_confidence |
|---|---|
| ≥ 4 | high |
| ≥ 2 | medium |
| else | low |

## Related score quality

`ScoreBreakdown.data_quality` is `strong / good / acceptable`, based on how many evidence streams (derivatives, catalyst) are missing:

- 0 missing → strong.
- 1 missing → good.
- ≥ 2 missing → acceptable.

## Reading

- `data_confidence = high` + score ≥ 80 + zero caps = A-tier with full confidence.
- `data_confidence = medium` + score ≥ 70 = B-tier; act, but smaller.
- `data_confidence = low` = anything from the desk should be treated as **probabilistic only**. Verify externally.

## What the desk shows in the report

```
{ tier }-tier {direction} {symbol}
score X | mode Y | confidence Z
focus E | data {data_confidence}
```

The `data` field is exactly this.

## Common mistakes

- Treating `data_confidence = low` as fixable by adding narrative — it usually means anchor or derivatives data is missing. The fix is data, not story.
- Promoting a `low` data confidence idea because the chart looks good — the desk does not know what the chart looks like beyond the metrics.

## Related

- [[Scoring_Overview]]
- [[Trade_Idea_Agent]]
- [[Exchange_Data_Confidence]]

## Implemented status

- **Implemented**.
