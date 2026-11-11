# Swing Mode

## Definition

- **Horizon**: several days (typically 2–7).
- **Timeframes**: 1h, 4h, 1d.
- **Primary TF for ranking**: 4h.
- **Universe filter**: `min_recent_candle_quote_volume = 150,000`, `min_atr_percent = 0.80`.
- **Max ideas per report**: 3.
- **Setup TF in report header**: `f"{tf} thesis / 4h execution (swing several days)"`.

## Scoring posture

`scoring.yaml.mode_weights["swing"]`:

- narrative × 1.30 — narrative is the strongest swing driver.
- catalyst_news × 1.20 — multi-day moves usually need a story.
- market_regime × 1.15 — alignment with macro regime weighted more.
- momentum × 0.90 — momentum chases mean-revert at swing scale.

## Best conditions

- Clean weekly / daily structure (higher highs + higher lows for long).
- Narrative is in `hot` or `rising` per [[Narrative_Agent]].
- Catalyst pipeline (mainnet, listing, partnership, governance) verifies.
- Funding is normal or supportive.
- Relative strength sustained over 7d, not just 24h.

## What invalidates a swing idea

- 4h close past the structural invalidation, or daily close past the higher-timeframe stop.
- Narrative cooling (heat_score drop ≥ 20 points) without price holding.
- Verified bearish catalyst against direction (e.g. unlock, delisting).
- BTC regime flips against the trade and breadth confirms.

## Risk rules

- Larger invalidation distance — use 1.2 ATR on 4h, or last swing low/high ± 0.15 ATR.
- R/R to TP2 ideal ≥ 2.5–3 to justify the time on risk.
- Position size smaller per trade (capital is at risk longer).
- No swing during `high-volatility danger` regime.

## How to use Telegram / news in swing

- **High relevance.** A swing trade is more likely to hinge on a multi-day narrative or catalyst.
- A `news_trader` `tier=strong` signal that confirms a narrative is a strong evidence input.
- Verified manual events (`data/raw/events/manual_events.yaml`) feed `CatalystAgent` → swing scoring.
- Avoid swing entry within 2 days of a known token unlock — risk_events block.

## Common mistakes

- Treating a 4h momentum spike as a swing — without narrative + catalyst it tends to reverse within the swing window.
- Ignoring the 1d trend because the 4h looks clean.
- Late-narrative entries — by the time it's in mainstream Telegram, swing is usually crowded.

## Future improvements

- Daily candle weighting in the setup quality score.
- Per-narrative cool-down to suppress late swing entries.

## Related

- [[Trading_Modes_Overview]]
- [[Intraday_Mode]]
- [[Narrative_Agent]]
- [[Catalyst_Agent]]
- [[Token_Unlocks]]

## Implemented status

- **Implemented**.
