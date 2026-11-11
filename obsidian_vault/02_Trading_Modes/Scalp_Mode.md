# Scalp Mode

## Definition

- **Horizon**: 30 minutes to 2 hours.
- **Timeframes**: 1m, 5m, 15m (with 1h auto-appended in `WatchlistMonitor._mode_timeframes` to keep trend context).
- **Primary TF for ranking**: 5m.
- **Universe filter**: `min_recent_candle_quote_volume = 20,000`, `min_atr_percent = 0.12`.
- **Max ideas per report**: 3.
- **Setup TF in report header**: `f"{tf} thesis / 5m execution (scalp 30m-2h)"`.

## Data the desk fetches

`scalp-report --auto-universe`:

1. Stage 1 — fused multi-exchange USDT universe.
2. Stage 2 — rank with scalp filters.
3. Top-N → `update-data` for 1m/5m/15m (+1h for watchlist monitor).
4. Daily-report-style pipeline with `mode=scalp`.

## Scoring posture

`scoring.yaml.mode_weights["scalp"]`:

- momentum × 1.20 — short-term flow is everything.
- execution_quality × 1.20 — tight stops, clean R/R.
- catalyst_news × 0.80 — most catalysts are too slow for scalp; ignore unless market-moving.
- narrative × 0.75 — narratives don't drive 30-minute moves.

## Best conditions

- Active session (US, EU, Asia open + 1–2h after open).
- Volatility expansion: BTC ATR rising but not yet "high-volatility danger".
- Clear local levels (last 1h high/low) acting as entry / invalidation.
- Relative strength against BTC over the last 5–15 minutes.
- Volume ratio ≥ 1.5x SMA20.

## Risk rules

- Tight invalidation: ATR-based stop (default 1.2 ATR), no wider.
- Position size scaled for the tighter stop — do not size like intraday.
- R/R to TP1 ≥ 1; ideal 1.5R.
- No scalp during `high-volatility danger` unless you reduce size and accept whipsaw risk.

## What invalidates a scalp

- 5m close back inside the rejected level.
- BTC reversing against the trade ≥ 0.5% in 5 minutes.
- Volume drying up immediately after entry.
- Funding spike that adversely caps the trade.

## What Telegram / news mean for scalp

- **Most Telegram messages are too slow.** By the time the channel posts, the move is often half-done.
- A `news_trader` `tier=strong` signal can be useful **only** if it arrives before price has expanded > 1 ATR.
- For scalp, treat Telegram as crowding signal, not catalyst signal: if the symbol is suddenly mentioned 3+ times and price is already extended, this is exit signal, not entry.

## Common mistakes

- Chasing a 3%+ candle on a 1m chart — `distance_from_ema20_atr > 2` auto-converts to watchlist.
- Trading scalp during dead session (Sunday US night) — volume floor is too low.
- Holding a scalp into a catalyst window (e.g. CPI) — risk regime spike forces a worse exit.

## Future improvements

- Add VWAP-aware entries (recommended; not implemented — see [[VWAP]]).
- Add a session-time filter that downgrades scalps during dead hours.

## Related

- [[Trading_Modes_Overview]]
- [[Intraday_Mode]]
- [[Mode_Specific_Risk]]
- [[Volume_Anomaly]]
- [[Relative_Strength]]

## Implemented status

- **Implemented**.
