# Bearish Trend Regime

## Conditions

- BTC trend ∈ {downtrend, transition_down}.
- Breadth above EMA20 ≤ 40%.
- ETH trend is not gated; BTC + breadth are sufficient.

## What the desk does

- `risk_mode = risk-off`.
- Style: "short bias or no trade; avoid weak altcoin longs".
- Scoring multipliers (`scoring.yaml.regime_weights["bearish trend"]`):
  - `momentum × 1.15`
  - `technical_setup × 1.10`
  - `catalyst_news × 0.85`
  - `narrative × 0.85`
- Longs are not blocked, but `_market_alignment("long", bearish)` returns 0.25.

## How to trade it

- Prefer short setups on failed reclaims, broken support, lower-high bounces.
- Demand at least 1R to TP1; many bear-tape shorts produce 2–3R within 4–24h.
- Avoid altcoin longs unless there is a confirmed catalyst **and** relative strength vs BTC.
- Avoid revenge-buying after large red candles — `distance_from_ema20_atr > 2` auto-converts to watchlist.

## What invalidates bearish

- Breadth climbs above 55 and BTC/ETH reclaim EMA20/EMA50.
- BTC ATR percentile breaks above 80 with >4% move (any direction) → flips to `high-volatility danger`.

## Common mistakes

- Shorting after a 10%+ down move — extension > 2 ATR converts to watchlist.
- Treating extreme negative funding as continuation — `funding < -0.001` caps shorts at 78 (squeeze risk).

## Related

- [[Market_Regime_Overview]]
- [[Long_Short_Neutral_Bias]]
- [[How_Regime_Affects_Scoring]]
- [[Funding_Risk]]

## Implemented status

- **Implemented**.
