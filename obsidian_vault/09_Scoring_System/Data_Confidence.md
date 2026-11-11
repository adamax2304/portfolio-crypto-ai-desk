# Data Confidence (Scoring side)

This page documents `data_confidence` as it appears on the **trade idea**. The detailed definition is in [[Data_Confidence]] (under 04_Indicators_and_Metrics).

## Stored on every trade idea

- `data_confidence` ∈ {high, medium, low}.
- `data_quality` (on ScoreBreakdown) ∈ {strong, good, acceptable}.

## Why this matters for scoring

- `data_confidence = high` should be required for A-tier in practice (the desk doesn't formally cap on it, but in real reports the two correlate).
- `data_confidence = low` usually means the idea is missing derivatives + catalyst + sometimes anchor — these are the same things that trigger caps.

## How LLMs should use it

- When stating a verdict, always cite `data_confidence`.
- When `data_confidence = low`, frame the answer as "if data improves, this might become tradable".
- Never claim "high confidence" if the data field says otherwise.

## Related

- [[Data_Confidence]] (full definition)
- [[Score_Breakdown]]
- [[Trade_Idea_Agent]]

## Implemented status

- **Implemented**.
