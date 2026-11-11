# EMA

## Implementation

`technicals.ema(series, period)` — pandas EWM with `adjust=False, min_periods=period`.

## Bands computed

`enrich_ohlcv` adds:

- `ema20` — fast trend / pullback reference.
- `ema50` — intermediate trend.
- `ema200` — slow / regime context.

## How the desk uses them

- **Trend label** (`trend_label`):
  - close > EMA20 > EMA50 → uptrend
  - close < EMA20 < EMA50 → downtrend
  - close > EMA50 and EMA20 < EMA50 → transition_up
  - close < EMA50 and EMA20 > EMA50 → transition_down
  - else → range
- **Distance from EMA20 in ATR** (`distance_from_ema20_atr`) — used as extension gate (> 2 warns, > 2.5 forces watchlist).
- **Setup entry zone** — long entries target the pullback into EMA20 ± a fraction of ATR.
- **Regime breadth** — % of universe above EMA20 / EMA50.

## Reading

- Price above EMA20 and EMA50 with both rising = clean uptrend.
- Price between EMA20 and EMA50 = transition; demand confirmation.
- Price below all three = downtrend; do not chase longs.

## Common mistakes

- Forcing trades when price is far from EMA20 — invalidation widens, R/R degrades.
- Confusing EMA200 hold as bullish in `bearish trend` — breadth and BTC structure can still override.

## Related

- [[Indicators_Overview]]
- [[Market_Structure]]
- [[Overextension_Risk]]

## Implemented status

- **Implemented**.
