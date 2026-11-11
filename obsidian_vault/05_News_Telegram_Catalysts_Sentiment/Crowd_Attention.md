# Crowd Attention

## Where computed

`CrowdAttentionAgent` (see [[Crowd_Attention_Agent]]) consumes:

- `MomentumCandidate` per symbol (price, RS, volume_ratio, return_24h, distance_from_ema20_atr).
- `SocialAttentionSummary` (Reddit + manual KOL notes).
- `manual_social_notes` (manual + news_trader_bridge converted notes).
- `DerivativesSummary` (funding, OI crowding).

## Stages produced

- `silent` — attention low + momentum low.
- `early_attention` — attention 30+, momentum 55+, crowding < 40.
- `growing_hype` — attention 55+, momentum 60+.
- `euphoria` — attention 70+, crowding 55+. Warning issued.
- `exhaustion` — attention 60+ but momentum < 45. Warning.
- `fear_capitulation` — return_24h < -10% + attention ≥ 30.
- `rumor_driven` — any manual note tagged rumor + attention ≥ 15. Warning.
- `unknown` — fallback.

## How to read stages

- **silent** → nothing to do; ignore for now.
- **early_attention** → the most tradable stage; setup + verification likely to confirm.
- **growing_hype** → still tradable but check for crowding; size carefully.
- **euphoria** → exit if long; do not enter; consider counter setups.
- **exhaustion** → fade rallies; do not chase further longs.
- **fear_capitulation** → potential bottoming, but no clean entry yet; watch for reclaim.
- **rumor_driven** → attention only; no sizing.

## Crowding risk component

`_crowding_risk` adds:

- +35 if `return_24h > 15` (extreme run-up).
- +18 if `return_24h > 8`.
- +25 if `|distance_from_ema20_atr| > 2`.
- +30 if `funding_rate > 0.001`.
- +15 if `funding_rate > 0.0005`.

## How this affects scoring (indirectly)

- `CrowdAttentionAgent` does **not** directly modify score.
- Its outputs feed the report and the trade idea's evidence.
- Stages `euphoria`, `exhaustion`, `rumor_driven` produce warnings that may flow into the setup's `warnings[]` list, which feeds `ScoringAgent.risk_penalty`.

## Telegram contribution

- `news_trader_bridge` Telegram notes raise `attention_score` (their `confidence: high` adds 22 points; `medium` adds 14).
- A `tier=strong` Telegram cluster sets `verification = confirmed`, which combined with momentum can flip a C → B during a `WatchlistMonitor` tick.

## Common mistakes

- Treating "euphoria" as a trade signal — it's an exit / counter signal.
- Treating "early_attention" without confirmation as a buy — it's where you watch, not where you act.
- Ignoring stage when sizing — stage tells you how crowded the trade is.

## Related

- [[Crowd_Attention_Agent]]
- [[Telegram_Integration]]
- [[Telegram_News_Evaluation]]
- [[Narrative_Heatmap]]

## Implemented status

- **Implemented**.
