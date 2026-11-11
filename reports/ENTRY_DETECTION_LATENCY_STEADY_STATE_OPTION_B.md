# Entry-Detection Latency — Steady-State (Post-Option-B) (PART 1–2)

**Date:** 2026-06-16 ~15:12 UTC · CSV: `ENTRY_DETECTION_LATENCY_STEADY_STATE_OPTION_B.csv`

## PART 1 — Stable window

`OPTION_B_STABLE_FROM = 2026-06-16T12:08:15Z` — first reliable pending-tracker tick of the
fresh (fixed-code) monitor. Since then: **34 ticks** over ~3h, spacing ~3–9 min (a few
~14–16 min gaps during re_evaluate/network), no DB-lock errors. Monitor is live and
current (last tick 15:07Z).

All metrics shown two ways: **full** (all entered signals in CSV) and **post-stable**
(entry_touch_at ≥ 12:08:15Z — excludes pre-restart backlog).

## PART 2 — Latency metrics

### Post-stable (touch ≥ 12:08:15Z) — n=16
| metric | value |
|--------|-------|
| n entered | 16 (all **stocks**; 0 crypto) |
| with measurable age | 4 (stocks intraday) |
| median entry_age | **24.6 min** |
| mean | 22.5 min |
| p90 / max | 24.6 / 24.6 min |
| fresh ≤2m / acceptable ≤5m / late 5–15m | 0 / 0 / 0 |
| very_late >15m | 4 |
| already_closed | 0 |
| unknown (no paper-entry alert) | 12 (stocks swing — paper-paused, no alert) |

By asset/mode (post-stable):
- **stocks intraday** n=4 → all very_late (age ~16–25 min)
- **stocks swing** n=12 → unknown (paused, no alert)
- **crypto intraday / swing / scalp** → **n=0** (no entry touched after stable)

### Full window (all entered, lagging — still backlog-dominated)
median 306.7 min — meaningless for the verdict; dominated by pre-restart backlog and
historical entries. Use post-stable only.

## Interpretation

- The only measurable post-stable latency is **stocks intraday ≈ 16–25 min** from the 15m
  **candle-open** touch. Since a 15m candle covering a 14:30 touch only *closes* at 14:45,
  detection at 14:46–14:54 is ~1–9 min **after candle close** — i.e. essentially
  one-candle latency, floored by the 15m timeframe, not an Option-B deficiency. It reads
  "very_late" only because the ≤15m thresholds are calibrated for 1–5m crypto candles.
- **Crypto steady-state latency is not yet measurable** — no crypto entry has triggered
  since the monitor stabilized (quiet market). Crypto uses 1m/5m candles, so the expected
  steady-state is ≤5–10 min, but this is **unproven** until a fresh crypto touch occurs.

**PART 1–2 status: DONE.** Infra confirmed live; post-stable stocks ≈16–25 min (15m-floored);
crypto pending a fresh touch.
