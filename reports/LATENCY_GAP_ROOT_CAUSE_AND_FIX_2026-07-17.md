# Latency Gap Root Cause and Fix - 2026-07-17

## Scope

End-to-end review of signal creation, market-data refresh, entry detection,
Paper accounting, Telegram dispatch, MEXC fan-out, stocks monitoring, and
Shadow evidence timestamps.

## Baseline (7 forward days before the fix)

- Crypto detection: raw p90 2874.8s; candle-bounded lower estimate p90 215.9s.
- Stocks intraday detection: raw p90 8148.0s; lower estimate p90 7248.0s.
- Detection-to-Telegram dispatch itself was fast: crypto p90 13.7s, stocks p90 1.9s.
- Only 19% of crypto detections came from the pending monitor and 4% of stock
  detections came from the stocks monitor. Most were found by the two-hour pass.
- The historical telemetry used candle-open timestamps as if they were exact
  entry touches. This materially overstated some delays and understated other
  execution risks.

## Root causes

1. The candle walker records the bar open, not the intrabar touch time.
2. Paper freshness and the MEXC policy consumed that approximate timestamp as
   an exact point-in-time entry.
3. The fast crypto refresh was Binance-only. Bybit/MEXC discoveries could be
   monitored from an older fallback cache.
4. The tracker preferred the first cached venue/timeframe even when it was
   older than another available copy.
5. The pending loop slept for `interval + work`, so a 30s loop with a 10s fetch
   actually ran about every 40s.
6. Stocks pending execution used 15m yfinance bars only.
7. Monitors were launched near the end of a long scheduler cycle, were killed
   at cycle boundaries, and their finite three-hour lifetimes could leave gaps.
8. The SLA mixed current-window evidence with old rolling-cache backfills.

## Implemented

- Preserved `entry_bar_open_at` for historical reconstruction and added an
  independent `detected_at`/`decision_at`, current executable price, timeframe,
  time basis, and current-price-revalidated flag.
- A current entry is actionable only when the latest available price still
  satisfies the original zone/trigger and invalidation. Breakout catch-up is
  capped at 0.25R to prevent chasing.
- Paper accounting freezes the actual decision time and executable price for a
  verified entry. New candle-range-only reconstructions remain research rows
  and cannot move the authoritative Paper balance.
- MEXC policy and worker independently reject any decision without
  `point_in_time_current_bar` plus `current_price_revalidated=true`, including
  legacy rows already queued before this deployment.
- Crypto pending refresh now retries unresolved Binance pairs on Bybit and
  MEXC, and the tracker selects a fresh venue/timeframe instead of a stale
  first match.
- Pending cadence is fixed-rate. Work time is subtracted from the sleep budget.
- Stocks pending refresh now stores 1m plus 15m bars. The 1m lane narrows entry
  observation; 15m remains the deterministic fallback.
- Pending and MEXC monitors are continuous. Stocks and derivatives monitors run
  for 24 hours. Healthy processes are reused across scheduler cycles rather
  than killed and restarted.
- Latency-critical monitors start immediately after the pre-entry safety
  context, before heavy reports/news/shadow jobs.
- SLA stores typed provenance columns, reports exact point-in-time samples
  separately, and filters DATA_GAP_LATE to signals created inside the requested
  window.

## Mode coverage

- Crypto scalp/intraday/swing: common tracker provenance and multi-exchange
  refresh apply. Scalp remains Shadow-only by policy.
- Stocks intraday: 1m observation plus 15m fallback apply. yfinance remains a
  delayed, non-live-grade provider.
- Stocks swing/invest and Stocks Position Framework: these are Shadow/research
  horizons, not realtime Paper execution lanes. Their coverage/decision times
  stay explicit and do not claim live fillability.
- Derivatives Reset and Catalyst RS: deterministic Shadow decision timestamps
  remain isolated. This change does not promote or alter either strategy.

## Verification

- Full regression: 1649 passed.
- Existing DB migrations were idempotent. Counts were unchanged during schema
  migration: proposed_signals 3816, signal_outcomes 1206856,
  paper_execution_outcomes 3169.
- Real crypto refresh smoke test: BANK/USDT 1h succeeded in about 8s.
- New continuous pending monitor first tick: 1 symbol, 2/2 pairs refreshed,
  total 6.6s, no errors.
- MEXC status after restart: live armed, submission enabled, kill switch CLEAR,
  active risk/margin/notional all zero, no queued legacy decisions.

## Remaining acceptance work

Historical candle events cannot be made exact retroactively. The current
7-day report therefore still shows an SLA breach and zero new point-in-time
samples. Do not judge the fix by those old rows. Re-evaluate after at least 20
new revalidated detections per asset lane. Stocks cannot be considered
live-grade until yfinance is replaced by a realtime provider, even if Paper
latency improves.
