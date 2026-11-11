# Intraday Mode

## Definition

- **Horizon**: 4 to 24 hours.
- **Timeframes**: 15m, 1h, 4h.
- **Primary TF for ranking**: 1h.
- **Universe filter**: `min_recent_candle_quote_volume = 75,000`, `min_atr_percent = 0.35`.
- **Max ideas per report**: 4.
- **Setup TF in report header**: `f"{tf} thesis / 15m execution (intraday 4-24h)"`.
- **The default mode** — picked by `Supervisor.ask` and by every "what should I look at right now" workflow.

## Scoring posture

`scoring.yaml.mode_weights["intraday"] = {}` — pure base weights, no multipliers. This is the calibration baseline.

## Best conditions

- BTC has set a clean 4h structure (clear higher-low or lower-high).
- Breadth is decisive (≥ 55 for bullish, ≤ 40 for bearish).
- Funding is not extreme in either direction.
- Symbol has relative strength vs BTC over the last 4–24h.
- Volume on the breakout / reclaim candle confirms.

## Required ingredients in an intraday A/B-tier idea

- Clean 1h structure: resistance / support clearly identifiable from `recent_range(frame, 20)`.
- ATR > 0 (else `TechnicalSetupAgent` rejects with "ATR unavailable").
- Setup quality ≥ ~60 (`setup_quality` is a composite of momentum × 0.45 + trend bonus + R/R bonus).
- Distance from EMA20 in ATR ≤ 2 (else auto-watchlist).
- Risk/reward to TP1 ≥ 1 (else `poor_risk_reward` penalty).

## What invalidates an intraday idea

- 1h close past the invalidation level.
- Regime flips to `high-volatility danger`.
- BTC breaks structure against the trade thesis.
- A confirmed catalyst (verified news) appears against direction.

## What Telegram / news mean for intraday

- Telegram has **medium relevance** here. A `tier=strong` signal can flip a C → B tick (via attention boost), but it should be confirmed by price/volume within 30–60 minutes.
- News matters more than scalp. A confirmed listing / partnership / unlock changes the 4–24h thesis.
- Rumors still cap at 55. Do not promote.

## Risk rules

- Default invalidation is 1.2 ATR from the entry, or recent local support/resistance ± 0.15 ATR, whichever is closer.
- R/R to TP2 ideal ≥ 2.
- Stop must be respected on 1h close, not on wicks (unless extreme).

## Common mistakes

- Treating a 4h trend reversal as a confirmed intraday setup before the 1h structure agrees.
- Sizing an intraday trade like a scalp because the entry is tight — the stop is wider.

## Related

- [[Trading_Modes_Overview]]
- [[Scalp_Mode]]
- [[Swing_Mode]]
- [[Mode_Specific_Risk]]
- [[Technical_Setup_Agent]]

## Implemented status

- **Implemented** — this is the calibration baseline of the desk.
