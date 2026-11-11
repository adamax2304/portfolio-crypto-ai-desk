# Expired Signal Root-Cause Audit (PART 6)

**Date:** 2026-06-16 · Source: `db/crypto_ai_desk.sqlite` (read-only)
**Per-signal data:** [EXPIRED_SIGNAL_DETAILS.csv](EXPIRED_SIGNAL_DETAILS.csv) (794 expired/no-entry)
**Generator:** `scripts/audit_latency_expired.py expired`

## Expiry types observed (production statuses)

The tracker produces two terminal "expiry" states (the spec's 10 sub-types collapse onto
these two in practice; the others — `entry_moved_away`, `stale_before_entry`,
`data_stale` — are not emitted by the current tracker):

1. **setup_expired_no_entry** (`status=missed_no_entry`) — entry zone never touched within
   validity → **no capital at risk** (protective by construction).
2. **entered_then_expired_flat** (`status=expired`, entry_triggered=1) — entered, drifted,
   ran out of validity without TP or stop.

## Rate by window

| Window | expired/no-entry | of tracked | rate |
|--------|-----------------:|-----------:|-----:|
| 24h    | 3   | 147  | 2.0% |
| 7d     | 52  | 572  | 9.1% |
| 14d    | 197 | 981  | 20.1% |
| all    | 794 | 1911 | 41.5% |

## By asset/mode (all-time — no_entry / entered_then_flat)

```
crypto  intraday   7 / 2
crypto  scalp     22 / 49   (shadow — not actionable)
stocks  intraday 335 / 354  ← dominates (689 of 794 = 87%)
stocks  swing      4 / 21
```

**Stocks intraday is the overwhelming source of expiries** (87% of all expired/no-entry).
Crypto expiries are comparatively rare.

## Missed-opportunity analysis — entered_then_expired_flat

| Window | n | avg MFE | avg MAE | reached +0.3R | +0.5R | +1R | hit stop |
|--------|--:|--------:|--------:|--------------:|------:|----:|---------:|
| 7d  | 50  | +0.64R | −0.53R | 86.0% | 72.0% | 6.0% | 0% |
| 14d | 108 | +0.58R | −0.50R | 80.6% | 59.3% | 6.5% | 0% |
| all | 426 | +0.52R | −0.47R | 68.3% | 47.4% | 3.8% | 0% |

**Reading:**
- Expired-flat trades drift in a tight band: avg MFE ~+0.5R, avg MAE ~−0.5R. About half
  reach +0.5R favorable excursion, but **only ~4–6% ever reach +1R** — so they are
  *modest* missed opportunities, not big missed winners.
- **"hit stop" is 0% by construction** — a trade that hit its stop is classified
  `stopped`, not `expired`. So expiry never *masks* a loss: these are genuinely
  indecisive/flat trades that ran out of time without committing either way.

## Is expiry a latency artifact? No.

`track_signal` walks **all** candles since signal creation each pass, so a brief entry
touch between two 2h ticks is still detected retroactively (it sets `entry_triggered_at`
to the candle ts). Therefore the ~135 min detection latency (PART 2) does **not** create
false expiries — the expiry classification reflects real price action, not missed polling.
(Latency hurts *actionability*, not *accuracy* — that's PART 10's concern, not this one.)

## Root causes

1. **Stocks intraday entry zones often don't fill within RTH** (335 no-entry). Intraday
   setups propose a pullback/breakout entry zone with finite validity; when the market
   doesn't reach the zone before the session/validity ends, the setup expires unfilled.
   This is **protective** (no fill = no risk) but indicates the entry zones / validity may
   be mildly mis-tuned for the RTH clock.
2. **Stocks intraday entered-flat** (354): entered but chopped sideways into expiry.
   Modest MFE, never stopped — expiry correctly cut the time-risk.
3. Crypto expiries are minor and mostly scalp (shadow, not actionable).

**PART 6 status: DONE** — expiry is dominated by stocks-intraday no-fill + flat-drift,
both protective; modest (not large) missed opportunity; not a latency artifact.
