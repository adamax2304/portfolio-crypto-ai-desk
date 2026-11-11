# Market Structure

## What "structure" means here

A working definition the desk uses implicitly:

- **Uptrend** — higher highs and higher lows on the chosen timeframe; close > EMA20 > EMA50.
- **Downtrend** — lower highs and lower lows; close < EMA20 < EMA50.
- **Range** — alternating highs and lows around a midline; close near EMA20 ≈ EMA50.
- **Transition** — EMA20 / EMA50 cross; close on the "other" side of one of them. See `trend_label`.

## What signals a structure break

- **Bullish break of structure (BoS)** — a new higher high on the timeframe + reclaim of EMA20.
- **Bearish BoS** — new lower low + close below EMA20/EMA50.
- **Change of character (ChoCH)** — price takes the most recent opposite swing in trend.

The desk does **not** automate BoS / ChoCH detection. The `trend_label` is the closest proxy. Recommended improvement: add explicit swing detection and emit `bos_up`, `bos_down`, `choch_up`, `choch_down` flags.

## Why structure matters

- Trades against structure require exceptional R/R + confirmation.
- Structure determines where invalidation belongs (last swing low for long, last swing high for short).
- Structure transitions are the highest-edge moments — but also the loudest (high failure rate in `transition` regime).

## How the desk approximates it

- `trend_label` for direction.
- `recent_range(20)` for level reference.
- Regime breadth as the multi-symbol cross-check.

## Common mistakes

- Trading off a 1m structure break when 4h structure says otherwise. The mode determines which TF wins.
- Calling a "reversal" on the first counter-candle — wait for actual reclaim + acceptance.

## Related

- [[Indicators_Overview]]
- [[EMA]]
- [[Support_Resistance]]
- [[Breakout_Reclaim_Structure]]
- [[Market_Regime_Overview]]

## Implemented status

- **Partially implemented** — trend label + range only. **Recommended**: explicit BoS/ChoCH detection.
