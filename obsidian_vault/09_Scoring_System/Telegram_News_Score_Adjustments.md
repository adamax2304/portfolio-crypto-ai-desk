# Telegram News Score Adjustments

How Telegram-derived signals enter (and don't enter) the score.

## What Telegram CAN do to score (indirectly)

1. Add to `attention_score` in `CrowdAttentionAgent` (via `manual_social_notes` from `news_trader_bridge`).
2. Set verification to `confirmed` if any signal cluster was `tier=strong` in news_trader.
3. Move a symbol's `CrowdAttention.stage` (e.g. silent → early_attention → growing_hype). This can flip the symbol's behavior in subsequent ranking.

The score itself does **not** directly read Telegram. The catalyst component reads from RSS + manual events. Telegram → catalyst happens only when an operator promotes a Telegram-confirmed event to `manual_events.yaml`.

## What Telegram CANNOT do to score (by design)

- Raise the catalyst_news component on its own.
- Override a score cap.
- Push past the rumor cap (55) when the catalyst is rumor-flagged.
- Push a setup to A-tier on its own.

## How to use Telegram in trade decisions

- Treat Telegram as **attention** evidence.
- If price + volume agree with the Telegram direction, the desk's other components (momentum, derivatives, regime) will pick up the move and raise the score on their own.
- If price + volume disagree, the Telegram message stays as attention only.

## Manual upgrade path

1. Confirm a Telegram headline via a primary source (exchange page, project blog).
2. Add a corresponding entry to `data/raw/events/manual_events.yaml`.
3. Re-run `update-data` to ingest it.
4. The next report applies `CatalystAgent.verification_status = "manual_event"` and lifts the catalyst component normally.

## Related

- [[Telegram_News_Evaluation]]
- [[News_Verification]]
- [[Scoring_Overview]]
- [[Rumors_and_Unverified_News]]

## Implemented status

- **Implemented**.
