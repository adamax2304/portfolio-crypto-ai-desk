# SocialAttentionAgent

## File

[src/agents/social_attention_agent.py](../../src/agents/social_attention_agent.py).

## Role

Builds a per-symbol attention summary from Reddit mentions + manual notes.

## Inputs

- `social_mentions: list[dict]` — Reddit (from `SocialCollector`) and manual notes.
- `candidates: list[MomentumCandidate]` — for symbol filtering.

## Outputs

`dict[symbol, SocialAttentionSummary]`:

- `mention_count`, `attention_score`, `sources[]`, `top_topics[]`.

## How it scores

- Each mention adds to the count.
- High-confidence manual notes get higher weight.
- Reddit upvote / comment counts (where available) bias attention_score.

## Used by agents

- `CrowdAttentionAgent` reads it to combine with manual + bridge notes.

## Common mistakes

- Treating Reddit attention as predictive — it lags.
- Not adding manual notes for genuinely high-signal mentions.

## Future improvements

- Twitter/X scraper (out of scope; reserved).
- Per-source weighting.

## Related

- [[Crowd_Attention_Agent]]
- [[Crowd_Leader_Agent]]

## Implemented status

- **Implemented**.
