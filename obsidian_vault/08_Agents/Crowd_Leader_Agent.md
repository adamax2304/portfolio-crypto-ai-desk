# CrowdLeaderAgent

## File

[src/agents/crowd_leader_agent.py](../../src/agents/crowd_leader_agent.py).

## Role

Aggregates manual social mentions into a small "KOL watch" summary — who's talking about what.

## Inputs

- `social_mentions: list[dict]` from `SocialCollector` (Reddit + manual KOL notes from `data/raw/social/manual_social_mentions.yaml`).

## Outputs

Report-friendly summary structures (top sources, top tickers, latest notes).

## Used by agents

- Report builder renders a "crowd / KOL watch" block.
- Does **not** flow into score.

## Common mistakes

- Treating KOL mentions as catalysts — they are attention only.

## Future improvements

- Per-KOL reliability tracking (which accounts produced useful calls?).

## Related

- [[Crowd_Attention]]
- [[Social_Attention_Agent]]

## Implemented status

- **Implemented**.
