# Manual Live Readiness — Post-Option-B (PART 5)

**Date:** 2026-06-16 · **Verdict: `MANUAL_MICRO_LIVE_WAIT_24H`**

## Why wait

Option B is **implemented and correct**, but its latency benefit is **not yet visible in
live data** — the running monitor predates the code change, so measured entry-age is still
the old baseline (median **131–143 min**, 0% fresh/acceptable). Manual mirroring of
latency-sensitive modes (intraday) requires entry_age ≤5 min, which cannot be confirmed
until a fresh monitor cycle runs the new code and new entries are detected within one
5-min tick. Acting on intraday now would be acting on the *unimproved* latency.

## Per-mode readiness

| Mode | Manually mirrorable now? | Reason |
|------|--------------------------|--------|
| **Crypto scalp** | **NO — forbidden always** | 0×/shadow; net-negative after fees (12m backtest) |
| **Crypto intraday** | **NOT YET** — wait for live latency confirmation | fix in, but measured entry-age still ~131 min; need ≤5 min confirmed + catalyst + no squeeze-risk |
| **Stocks intraday** | **NOT YET** — wait + RTH-liquid + fresh | same latency caveat; only during liquid RTH |
| **Crypto swing** | **YES (limited)** — latency-insensitive | multi-hour/day holds; a 5–135 min detection delay is immaterial to a swing entry zone |
| **Stocks swing/invest** | NO — paper-paused | unchanged |

## Strict manual rules (unchanged, reaffirmed)

- No scalp manual entry, ever.
- Intraday: only if `entry_age ≤ 5 min` AND price not worse than planned entry by >0.25R
  AND (crypto-long) a catalyst is present AND no squeeze-risk / conflicting funding-OI.
- Stocks intraday: only if entry fresh AND during liquid RTH.
- The Telegram freshness label + `[LATE ENTRY DETECTED — DO NOT CHASE]` banner now make
  this self-policing once the new code is live.

## Answers

1. **Crypto intraday manually mirrorable?** Not yet — wait for live latency confirmation.
2. **Stocks intraday manually mirrorable?** Not yet — latency + RTH-liquidity gate.
3. **Swing still the only safe category?** Yes, for now — and it is genuinely safe to
   manually test (latency-insensitive).
4. **Begin manual micro-live or wait?** **Wait ~24h.** Restart the monitor (or let the next
   2h cycle do it) so Option B goes live, run for a few hours, then re-run
   `python scripts/audit_latency_expired.py latency`. If the 24h row shows median ≤5–7 min
   and a non-zero fresh/acceptable share, **then** begin LIMITED intraday micro-live under
   the rules above.

**PART 5 status: DONE — `MANUAL_MICRO_LIVE_WAIT_24H` (swing manual test OK in the interim).**
