# Breakout / Reclaim / Structure

## What the desk computes

`MomentumScannerAgent` produces (per symbol):

- `direction_bias` ∈ {long, short, watch}.
- `reason_tags` — short list of qualitative tags such as `breakout`, `reclaim`, `range_expansion`, `momentum`, `lagging`, `extended`, etc.
- `score` — momentum composite.

`recent_range(frame, 20)` provides local resistance + support, which `TechnicalSetupAgent` uses to anchor invalidation.

## Pattern definitions used by the desk

- **Breakout** — close above recent 20-bar high with volume_ratio ≥ 1.2.
- **Reclaim** — close back above a level the price recently broke down through.
- **Range expansion** — ATR rising while price exits the prior range box.
- **Failed breakout / breakdown** — price pokes above (or below) the level then closes back inside; high-quality short / long candidate respectively.

## How to read the report structure block

- A setup tagged `breakout` with `distance_from_ema20_atr < 2` and volume_ratio > 1.5 = healthy.
- A `breakout` with `distance > 2.5` = chase; auto-converted to watchlist.
- A `reclaim` after a clean liquidation flush = often A-tier in `transition` regime.
- A `range_expansion` without volume = noise; demand confirmation.

## Practical entries

- **Breakout** — wait for retest of the broken level + acceptance.
- **Reclaim** — enter after the close back above the level, stop just below.
- **Failed pattern** — short the failed bullish breakout; long the failed bearish breakdown.

## Common mistakes

- Chasing the breakout candle itself — entry is wrong, stop is wide, R/R is bad.
- Calling a "reclaim" without volume / structure context — it might be a wick.

## Related

- [[Indicators_Overview]]
- [[Support_Resistance]]
- [[Market_Structure]]
- [[Technical_Setup_Agent]]

## Implemented status

- **Implemented** (qualitative tagging via reason_tags).
