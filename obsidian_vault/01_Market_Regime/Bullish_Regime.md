# Bullish Trend Regime

## Conditions

- BTC trend ∈ {uptrend, transition_up}.
- ETH trend ∈ {uptrend, transition_up}.
- Breadth above EMA20 ≥ 55%.
- BTC ATR percentile not in extreme danger zone (or |24h return| ≤ 4% if high).

## What the desk does

- `risk_mode = risk-on`.
- Style: "selective longs; prefer pullbacks on relative strength".
- Scoring multipliers (`scoring.yaml.regime_weights["bullish trend"]`):
  - `momentum × 1.25`
  - `technical_setup × 1.10`
  - `derivatives × 0.95`
- Shorts are not blocked, but `_market_alignment("short", bullish)` returns 0.25 — a heavy penalty.

## How to trade it

- Prefer pullback-style longs into EMA20 on relative-strength leaders.
- Demand ≥ 1R risk/reward to TP1; ideal 2R to TP2.
- Avoid extended setups (> 2 ATR from EMA20) — they auto-convert to watchlist.
- A short here must be exceptional (catalyst + clear failed breakout) — and even then it is structurally penalized.

## What invalidates bullish

- BTC closes below the recent local support and ETH follows.
- Breadth drops below 40 even though BTC is still up.
- BTC ATR percentile blows past 80 with a >4% intraday move → flips to `high-volatility danger`.

## Common mistakes

- Buying every dip without checking that the candidate is a **leader** (relative strength > 0) — laggards in bullish regimes underperform.
- Treating positive funding as confirmation — `funding > 0.0005` lowers score and `> 0.001` caps it at 78.

## Related

- [[Market_Regime_Overview]]
- [[Long_Short_Neutral_Bias]]
- [[How_Regime_Affects_Scoring]]
- [[Intraday_Mode]]

## Implemented status

- **Implemented**.
