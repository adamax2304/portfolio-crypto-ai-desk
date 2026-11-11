# AI Coins

Configured narrative in `config/watchlist.yaml`. Symbols: TAO, FET, RNDR, NEAR. Keywords: AI, artificial intelligence, machine learning, compute.

## What usually moves this sector

- BTC risk-on regime; AI is a high-beta narrative.
- AI partnership / integration headlines (OpenAI, Anthropic, NVIDIA mentions).
- BTC dominance falling (alt season tailwind).
- New AI model launches that mention crypto integrations.

## What news matters

- **Real partnerships** with FAANG-tier or AI-lab companies (rare, real ones move).
- **GPU / compute supply changes** (RNDR sensitive).
- **TAO subnet launches** — TAO-specific.
- **Generic "AI is the future" tweets** — noise.

## Telegram / social signals

- Be skeptical: AI is the most over-shilled crypto narrative.
- `news_trader_bridge` tags `partnership / integration` as bullish — frequent false positives.
- Verify with a primary source (project blog).

## Best regime

- `bullish trend` + breadth ≥ 60 + BTC dominance falling.
- Worst: `bearish trend` — AI coins lead the down move.

## Indicators that matter most

- Relative strength vs BTC.
- Sector leader RS (TAO often leads).
- Volume_ratio on the breakout candle.

## Common risk

- High beta — moves 2-3x BTC magnitude.
- Crowded longs at peaks of cycles.
- Funding can spike to +0.001 fast.

## Common fake signals

- Generic "AI revolution" tweets.
- Repeats of old partnerships.
- Pump groups targeting low-cap AI tokens before listings.

## Scoring posture

- Narrative weight 10 base × regime mult.
- In `bullish trend`, narrative quality boosts score noticeably.
- In `bearish trend`, narrative is muted (×0.85).

## Example good setup

- TAO in `bullish trend` regime, RS vs BTC +5%, volume_ratio 1.8x, breakout retest of recent range high, funding < 0.0005.

## Example bad setup

- Random small-cap AI alt only on MEXC, `tier=single_source` Telegram hype, no derivatives data → MEXC cap (70) + rumor cap if rumor present.

## Related

- [[Sector_Overview]]
- [[Narrative_Agent]]
- [[Narrative_Heatmap]]

## Implemented status

- **Implemented** as configured narrative.
