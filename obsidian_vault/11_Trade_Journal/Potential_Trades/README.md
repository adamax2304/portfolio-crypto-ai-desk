# Potential_Trades

A/B-tier ideas being evaluated for entry, or waiting for the planned entry zone to be reached.

## How files land here

- Manual: copy [[Potential_Trade_Template]] and fill in from the latest report.
- Recommended automation: `python -m src.cli log-trade-to-obsidian --idea-id <id>` (not yet implemented).

## Filename

```
YYYY-MM-DD_SYMBOL_MODE_DIRECTION_SCORE.md
```

## Lifecycle

- **Created** when you decide to consider the idea.
- **Updated** if the desk's next monitor tick changes the tier/score (use a "Status update" section).
- **Moved** to `Executed_Trades/` if you take the trade.
- **Moved** to `Rejected_Ideas/` if you decide not to take it.

## Related

- [[Potential_Trade_Template]]
- [[Trade_Idea_Template]]

## Implemented status

- Folder ready; manual workflow.
