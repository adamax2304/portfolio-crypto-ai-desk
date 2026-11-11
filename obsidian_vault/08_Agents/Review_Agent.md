# ReviewAgent

## File

[src/agents/review_agent.py](../../src/agents/review_agent.py).

## Role

Loads saved trade ideas from SQLite and checks how they performed against subsequent candles. Produces a Markdown review report.

## Inputs

- `market_data: dict[symbol, dict[tf, DataFrame]]` (loaded by Supervisor).

## Outputs

- Returns a Markdown string for the review report.
- Persists `idea_checks` rows into SQLite (entry-triggered? max favorable excursion? max adverse excursion? hit TP1 / TP2 / TP3?).

## How it reviews

- For each prior TradeIdea, load post-creation candles on the relevant timeframe.
- Detect whether price entered the entry zone (entry_low..entry_high).
- Compute MFE / MAE relative to the entry midpoint.
- Detect TP1/TP2/TP3 hits and invalidation hits.

## Output report content

- Per-idea status: entered? winner / loser / unresolved.
- Per-symbol metrics: MFE, MAE, R multiple if entered.
- Summary stats: hit rate, average R.

## Used by

- User-invoked via `python -m src.cli review`.
- The trade journal: copy the per-idea result into [[Executed_Trade_Template]] entries.

## Common mistakes

- Reviewing too soon — short-horizon trades may not have had time to play out.
- Reading "unresolved" as failed — it's pending.

## Future improvements

- Per-mode review (scalp vs intraday vs swing should be reviewed on their own horizons).
- Tag each idea with which agent was most predictive (regime / setup / catalyst).

## Related

- [[Trade_Idea_Agent]]
- [[Post_Trade_Review_Checklist_For_LLM]]
- [[Daily_Review_Template]]
- [[Weekly_Review_Template]]

## Implemented status

- **Implemented**.
