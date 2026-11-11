# Support / Resistance

## How computed

`recent_range(frame, lookback=20)`:

- `resistance = max(high)` over the last 20 bars (excluding the most recent one).
- `support = min(low)` over the same window.

This is intentionally simple. No swing-high / swing-low detection, no Fibonacci, no pivot points.

## Where used

- **`TechnicalSetupAgent`** — to position invalidation closer than 1.2 ATR when possible.
- **`MarketRegimeAgent.key_levels`** — local support/resistance for BTC and ETH, exposed in the report.
- **`MomentumScannerAgent`** — informs breakout / reclaim tags.

## Reading

- The "level" is a horizontal price band, not a single tick.
- The desk does not draw trendlines; only horizontal levels.
- 20-bar window is mode-dependent via the underlying timeframe:
  - On 1h: ~20 hours of structure.
  - On 4h: ~3 days.
  - On 1d: ~3 weeks.

## When the level looks wrong

- If price has been in a tight range for the entire 20-bar window, `support` and `resistance` are close together — invalidation distance is small.
- If a single spike (wick) is in the window, the level is distorted upward. Mentally trim.

## Recommended improvements

- Swing-high / swing-low detection (not just window extrema).
- Volume-profile high-volume node detection.

## Related

- [[Breakout_Reclaim_Structure]]
- [[Market_Structure]]
- [[Technical_Setup_Agent]]

## Implemented status

- **Implemented** (simple window extrema).
