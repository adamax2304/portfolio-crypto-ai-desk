# Manual Live Readiness — Steady-State Post-Option-B (PART 5)

**Date:** 2026-06-16 ~15:12 UTC · **Verdict: `CRYPTO_INTRADAY_WAIT_MORE_DATA`**

## Per-mode readiness (strict rules)

| Mode | Manually mirrorable now? | Reason |
|------|--------------------------|--------|
| **Crypto scalp** | **NEVER** | 0×/shadow; net-negative after fees |
| **Crypto intraday** | **WAIT — no data** | 0 fresh post-stable crypto entries → steady-state entry_age unmeasured. Cannot clear the ≤5-min + catalyst + no-squeeze gate without data. |
| **Crypto swing** | **YES (limited)** — latency-tolerant | multi-hour/day holds; still do a live price-vs-entry check before mirroring |
| **Stocks intraday** | **NOT YET** | post-stable detection ≈16–25 min from 15m candle-open (≈1 candle). Borderline for a 15m timeframe; only if live price still within 0.25R of entry AND liquid RTH. Treat as observe-only for now. |
| **Stocks swing / invest** | NO — paper-paused | unchanged |

## Rules reaffirmed (unchanged)
- Crypto scalp: never.
- Crypto intraday: only if entry_age ≤5 min, catalyst-backed, no squeeze-risk, price not
  worse than planned entry by >0.25R.
- Crypto swing: tolerates more delay, still requires a live price check.
- Stocks intraday: only if post-stable delay acceptable vs 15m timeframe and live price
  near entry.
- No stale / moved-away entries (now auto-enforced by the `late_shadow` /
  `[LATE ENTRY DETECTED — DO NOT CHASE]` routing).

## Answer
- **Crypto intraday manually mirrorable?** Not decidable yet — need ≥1 fresh post-stable
  crypto entry to measure steady-state latency. → `CRYPTO_INTRADAY_WAIT_MORE_DATA`.
- **Crypto swing?** Yes, limited — safe to manually test now (latency-insensitive).
- **Stocks intraday?** Observe-only; ~16–25 min (15m-floored) is borderline.
- **Begin micro-live?** Swing only for now; hold intraday until a fresh crypto entry
  confirms ≤5–10 min steady-state.

**PART 5 status: DONE — `CRYPTO_INTRADAY_WAIT_MORE_DATA` (swing manual test OK).**
