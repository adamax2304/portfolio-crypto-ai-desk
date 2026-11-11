# Crypto Intraday Point-In-Time Execution Fix

Date: 2026-07-30

## Problem

Crypto intraday used the 15m structural OHLCV walk for both setup evaluation
and Paper entry timing. The fast pending monitor did not fetch 1m bars for
intraday candidates. A touch could therefore first be discovered from a prior
15m candle, while the current price had already moved away. Paper correctly
refused those as late/historical, but no fresh execution observation existed
to enter a new in-zone setup promptly.

## Change

- 15m remains the canonical structural timeframe. No score, tier, entry zone,
  stop, target, Model F, sizing, quality-overlay, or live policy changed.
- While a crypto intraday A/B candidate is pending, the pending monitor now
  refreshes 1m as an execution-provenance frame.
- A new Paper entry requires the latest fresh 1m close to satisfy the existing
  entry geometry at the decision time. Its recorded entry time and price are
  the observed current values, never a historical candle-open timestamp.
- Once accepted, an intraday Paper trade is evaluated from that accepted
  point-in-time entry on subsequent 1m bars. Pre-entry history can no longer
  stop or take-profit the trade before its real entry.
- Historical 15m touches remain historical diagnostics. They are not retried
  as later synthetic Paper entries.

## Operational verification

- Replaced the old pending monitor with a single new leader process.
- Its first completed cycle fetched `1m,5m,15m,1h`; a later cycle checked all
  19 selected crypto candidates successfully.
- The monitor remains Paper/shadow only. Live routing was not changed.

## Tests

- 63 targeted tracker, pending-monitor, Paper accounting, and alert timing
  tests passed after the final integration test.
- New coverage proves fresh 1m entry provenance, post-entry-only exit walks,
  persisted entry reuse across tracker cycles, and 1m monitor selection for
  crypto intraday.
