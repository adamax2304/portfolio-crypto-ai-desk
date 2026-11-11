# Review Template (per idea)

Use after a trade closes or after the time window expires.

```
# Review — {{symbol}} — {{date_of_original_idea}} → {{date_of_review}}

## Original
- Tier / score / mode / direction:
- Entry zone / invalidation / TP1/TP2/TP3:
- Confidence / data_confidence / caps:
- Critical thesis sentence:

## What happened
- Did price enter the entry zone? (Y/N)
- Highest point reached (relative to entry):
- Lowest point reached (relative to entry):
- Did TP1 / TP2 / TP3 hit?
- Did invalidation hit?
- Outcome (winner / loser / unresolved):
- R multiple (if entered):

## Which agent was right
- MarketRegimeAgent — regime call was {{correct|wrong|partly}}
- MomentumScannerAgent — direction_bias was {{correct|wrong}}
- DerivativesAgent — alignment was {{correct|wrong}}
- CatalystAgent — verification was {{correct|wrong}}
- RiskAgent — warnings were {{useful|noise}}
- CriticAgent — counter_thesis was {{useful|noise}}
- NarrativeAgent — heat assessment was {{correct|wrong}}

## Lessons
- What I should keep doing:
- What I should stop doing:
- What the desk should do better (potential improvement backlog entry):

## News / Telegram impact
- Did Telegram messages help, mislead, or do nothing?
- Did news during the trade window invalidate or support?
- Should source X be trusted more / less next time?

## Filing
- Move original Potential_Trade or Executed_Trade to {{folder}}.
- Add cross-link to Daily_Review for the day.
```

## Related

- [[Post_Trade_Review_Checklist_For_LLM]]
- [[Daily_Review_Template]]
- [[Weekly_Review_Template]]
- [[Review_Agent]]

## Implemented status

- **Template**.
