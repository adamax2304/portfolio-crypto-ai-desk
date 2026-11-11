# Exchange Data Confidence

The desk surfaces three confidence fields on every trade idea:

1. `tier` — A / B / C / rejected.
2. `confidence` — high / medium-high / medium / low (from score).
3. `data_confidence` — high / medium / low (from data presence).

## How `data_confidence` is built

`TradeIdeaAgent._data_confidence(derivative, catalyst, confirmation, score)`:

| Condition | +points |
|---|---|
| derivatives available | +1 |
| catalyst events / risk_events present | +1 |
| anchor listed | +1 |
| derivatives listed | +1 |
| score.data_quality == "strong" | +1 |

| Total | Result |
|---|---|
| ≥ 4 | high |
| ≥ 2 | medium |
| else | low |

## Score data quality

`ScoreBreakdown.data_quality`:

- `strong` — 0 missing of {derivatives, catalyst}.
- `good` — 1 missing.
- `acceptable` — 2 missing.

## Operator interpretation

| data_confidence | Action |
|---|---|
| high | size as normal |
| medium | reduce size by 30-50% |
| low | watchlist only or skip |

## Caveats

- A `high` data_confidence + `low` score still = no trade. You must clear both axes.
- `data_confidence = high` does not mean the data is correct, only that it's present. Always check `coverage_audit` for stale subsystems.

## Related

- [[Data_Confidence]]
- [[Scoring_Overview]]
- [[Coverage_Audit_Agent]]

## Implemented status

- **Implemented**.
