## Latency SLA report (read-only - general live promotion blocked; MEXC canary separately gated)
_Plan age = price/strategy wait (NOT an SLA metric). Historical touch→event records include retrospective observations. Actionable SLA requires current-price revalidation; alert dispatch is measured separately._
- PLAN AGE signal→entry (n 161, price/strategy wait only): p50 37.0min · p90 792.8min · max 969.3min
- OBSERVED touch→event (all detections, n 62): p50 13.2s · p90 58.4s · p95 73.6s · max 235.0s
- SYSTEM entry→alert (sent-only, n 0): p50 — · p90 — · max —
- market-data age: p50 — · p90 — (telemetry 42920, sent 0)
- MEXC handoff: Paper-to-capture p90 — (n0) · queue-to-preflight p90 — (n0) · preflight-to-submit p90 — (n0)
- ROSTER signal->fast monitor (n 110): p50 322.6s, p90 58232.2s
- STRATEGY WAIT signal->executable setup (n 83): p50 55.9min, p90 811.8min
- SYSTEM ready->detect (n 62): p50 13.2s, p90 58.4s
- Paper decision runtime (n 122): p50 25.2ms, p90 4647.5ms

**Current acceptance (crypto and stocks are independent):**
- crypto: **INSUFFICIENT_SAMPLE** · raw detect p90 1.1s (n7) · point-in-time p90 1.1s (n7) · accepted detect p90 0.0s (lower-timeframe / sub-hour candle estimate) · legacy lower-bound p90 0.0s · dispatch p90 — (sent n0) · fast-source share 100%
  - excluded from actionable SLA: 0 historical/non-revalidated observations
  - usable detect sample 7 < 20
  - sent-alert sample 0 < 10
- stocks intraday: **INSUFFICIENT_SAMPLE** · raw detect p90 30.1s (n21) · point-in-time p90 30.1s (n21) · accepted detect p90 30.1s (point-in-time revalidated price) · legacy lower-bound p90 0.0s · dispatch p90 — (sent n0) · fast-source share 90%
  - excluded from actionable SLA: 2 historical/non-revalidated observations
  - excluded from live A/B cohort: 132 non-live-tier observations
  - sent-alert sample 0 < 5
  - live acceptance: BLOCKED_LATENCY · provider alpaca

**By mode** (plan age vs recorded touch→event diagnostics, seconds):
- crypto intraday: plan-age p50 14.5min (n7) · recorded detect p90 1.1s (n7) · entry→alert p90 — (n0) · DATA_GAP_LATE 0%
- stocks intraday: plan-age p50 38.6min (n154) · recorded detect p90 60.2s (n55) · entry→alert p90 — (n0) · DATA_GAP_LATE 0%

- FLAG: LIVE_BLOCKED_UNTIL_LATENCY_SLA
- FLAG: CRYPTO_LATENCY_ACCEPTANCE_INSUFFICIENT_SAMPLE
- FLAG: STOCKS_INTRADAY_LATENCY_ACCEPTANCE_INSUFFICIENT_SAMPLE
