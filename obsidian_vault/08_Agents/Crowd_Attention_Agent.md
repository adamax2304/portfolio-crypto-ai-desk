# CrowdAttentionAgent

## File

[src/agents/crowd_attention_agent.py](../../src/agents/crowd_attention_agent.py).

## Role

Per-symbol crowd-attention staging: silent / early_attention / growing_hype / euphoria / exhaustion / fear_capitulation / rumor_driven / unknown.

## Inputs

- `candidates: list[MomentumCandidate]`.
- `social_attention: dict[symbol, SocialAttentionSummary]` (Reddit / manual).
- `manual_social_notes: list[dict]` — manual notes **plus** `news_trader_bridge` notes converted via `to_manual_social_notes`.
- `derivatives: dict[symbol, DerivativesSummary]`.

## Outputs

`dict[symbol, CrowdAttention]`:

- `stage`, `attention_score`, `momentum_score`, `crowding_risk`, `confidence`.
- `evidence[]`, `warnings[]`.

## Stage rules (verbatim)

- rumor_driven — any note with `verification == "rumor"` or `sentiment == "rumor"` and attention ≥ 15.
- euphoria — attention ≥ 70 and crowding ≥ 55.
- exhaustion — attention ≥ 60 and momentum < 45.
- growing_hype — attention ≥ 55 and momentum ≥ 60.
- early_attention — attention ≥ 30 and momentum ≥ 55 and crowding < 40.
- fear_capitulation — return_24h < -10 and attention ≥ 30.
- silent — attention < 20 and momentum < 50.
- else — unknown.

## Used by agents

- Output goes into the report via `TradeIdeaAgent` (warnings may flow into setup warnings).
- It does **not** directly modify `ScoringAgent` numerics; influence is via warnings → risk_penalty.

## Common mistakes

- Treating `euphoria` as confirmation to enter — it is an exit / counter signal.
- Reading `early_attention` as a trade — it is a watchlist hint that wants confirmation.

## Future improvements

- Weight notes by source reliability (per-channel score in bridge).
- Add a "rotation" stage detection across symbols of the same narrative.

## Related

- [[Crowd_Attention]]
- [[Telegram_Integration]]
- [[Narrative_Agent]]
- [[Funding_Risk]]

## Implemented status

- **Implemented**.
