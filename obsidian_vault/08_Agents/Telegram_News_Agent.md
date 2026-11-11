# Telegram News Agent

## Status

**Not implemented as a dedicated agent.** Telegram messages enter the desk via [[Telegram_Integration]] → `news_trader_bridge` → `CrowdAttentionAgent` as social notes.

There is no `telegram_news_agent.py` in `src/agents/`.

## What plays this role today

1. `news_trader_bridge.aggregate` produces per-ticker attention (Telegram mention count, strong-tier count, bullish/bearish/macro counts, top headlines, latest_ts).
2. `news_trader_bridge.to_manual_social_notes` converts the aggregation into `manual_social_notes` shape.
3. `CrowdAttentionAgent` ingests these alongside manual notes and Reddit social_attention.

## Why no dedicated agent

- The desk treats Telegram as **attention**, not as catalyst. There's no need for a separate scoring path.
- Telegram catalysts that materialize as real events are added to `manual_events.yaml` and flow through `CatalystAgent`.

## What a dedicated agent would do (recommended)

If a future LLM wants to build one:

- Pull bridge signals.
- Score each headline for catalytic potential.
- Match headlines to symbols with higher precision than the bridge regex.
- Output a `TelegramCatalystSummary` per symbol with `tier`, `verification`, `freshness`, `direction_implied`.
- Feed into `ScoringAgent.catalyst_news` component with **strong caps** to prevent Telegram from raising A-tier on its own.

## Critical constraint

Any such agent must respect:

- Telegram never reaches A-tier on its own.
- Unverified Telegram still triggers the rumor cap (55).
- Single-source Telegram bumps attention, not score.

## Related

- [[Telegram_Integration]]
- [[Crowd_Attention_Agent]]
- [[Telegram_News_Evaluation]]

## Implemented status

- **Recommended / not implemented**. Functionality is split across `news_trader_bridge` + `CrowdAttentionAgent`.
