# Entry-Detection Latency — Post-Option-B Audit (PART 2)

**Date:** 2026-06-16 ~11:16 UTC · Data: `ENTRY_DETECTION_LATENCY_POST_OPTION_B.csv`
(1,371 entered signals; **0** paper-entry alerts after the 10:25 UTC impl boundary).

## ⚠️ Headline: no post-Option-B data exists yet — measured latency is unchanged

Because the live monitor process predates the implementation (PART 1), **zero** entries
have been detected by the new 5-min pending pass. The numbers below are therefore the
**same pre-Option-B baseline**, not a post-fix measurement.

## Measured latency (current data)

| Window | n entered | n w/ age | median | mean | p90 | max | fresh ≤2m | accept ≤5m | late 5–15m | very_late >15m | already_closed | unknown |
|--------|----------:|---------:|-------:|-----:|----:|----:|----------:|-----------:|-----------:|---------------:|---------------:|--------:|
| 24h | 85 | 52 | **131.0m** | 128.6m | 191.5m | 235m | 0 | 0 | 0 | 39 | 15 | 31 |
| 7d  | 404 | 148 | **134.9m** | 287.5m | 339.5m | 2636m | 0 | 0 | 0 | 116 | 51 | 237 |
| 14d | 758 | 170 | **143.2m** | 1279m | 4736m | 12746m | 0 | 0 | 0 | 133 | 126 | 499 |

By asset/mode (24h, fresh/acceptable/late/very_late/already_closed):
`crypto intraday 0/0/0/7/5 · crypto scalp 0/0/0/8/4 · crypto swing 0/0/0/11/5 · stocks intraday 0/0/0/13/1`.

## Comparison vs prior baseline

| Metric | Prior baseline | Now (post-impl, pre-live) | Target |
|--------|---------------|---------------------------|--------|
| median entry_age | ~135 min | **131–143 min** (unchanged) | ≤ 5–7 min |
| fresh/acceptable/late ≤15m | 0% | **0%** (unchanged) | some non-scalp fresh |
| very_late share | dominant | **dominant** (unchanged) | drops sharply |

## Why unchanged — and what it does NOT mean

This is **not** evidence Option B failed. It is evidence Option B **has not executed yet**:
the running monitor was started at 10:07 UTC (pre-10:25 impl) and runs old code; no
`track_pending_entries` pass has fired; no new entries have been detected since 10:07.
A single manual pass now would only measure a **catch-up batch** (entries that touched
hours ago during the idle window) — which would *understate* the steady-state gain — so it
is deliberately not used as the measurement.

## What must happen to measure the gain

1. A **fresh monitor process** loads Option B (next 2h scheduler cycle, or a manual
   `monitor-watchlist --interval 300` restart).
2. Let it run **2–3 hours** so newly-triggered A/B entries are detected within one 5-min
   tick (not from backlog).
3. Re-run `python scripts/audit_latency_expired.py latency` and read the **24h** row —
   expect median ≤5–7 min and a non-zero fresh/acceptable share for crypto intraday/swing
   and stocks intraday (during RTH).

**PART 2 status: DONE — audit run; baseline confirmed; post-Option-B measurement pending a
live cycle (verdict reflects this in PART 7).**
