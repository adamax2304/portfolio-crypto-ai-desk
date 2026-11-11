# CatalystAgent

## File

[src/agents/catalyst_agent.py](../../src/agents/catalyst_agent.py).

## Role

Per-symbol catalyst summary built from manual events + news mentions.

## Inputs

- `symbols: list[str]`.
- `events: list[dict]` — manual events from SQLite.
- `news_output: dict` — output of `NewsAgent` (uses `by_symbol`).

## Outputs

`CatalystSummary` per symbol:

- `symbol`, `catalysts: list[str]`, `risk_events: list[str]`.
- `verification_status` ∈ {none, news_mention, manual_event}.
- `importance_score`.
- `interpretation`, `warnings[]`.

## How it makes decisions

- Filters manual events to a window `today - 2 days .. today + 7 days`.
- Event types {unlock, delisting, migration} → `risk_events` + warnings.
- Other event types → `catalysts` + importance.
- For each symbol's news (top 3), appends `news: {title} ({source})` and bumps importance by 0.5 × news importance.
- Sets `verification_status` to `manual_event` when an event matches, else `news_mention` when news matches.

## Used by agents

- `ScoringAgent.catalyst_news` component (catalyst_quality factor).
- `ScoringAgent` rumor cap (checks for "rumor" in catalyst strings + verification status).
- `RiskAgent.risk_events` lift (+15 for risk events).
- `NarrativeAgent` per-narrative catalyst contribution.
- `TradeIdeaAgent` evidence block.

## Common mistakes

- Forgetting to re-run `update-data` after editing `manual_events.yaml` — events are loaded then.
- Adding events with stale dates outside the 2-day-back / 7-day-forward window — they're filtered out.

## Future improvements

- Per-event-type weights (mainnet vs partnership vs listing).
- Automated unlock calendar (TokenUnlocks API).
- Headline-level sentiment for news catalysts.

## Related

- [[News_System_Overview]]
- [[News_Verification]]
- [[Token_Unlocks]]
- [[News_Agent]]

## Implemented status

- **Implemented**.
