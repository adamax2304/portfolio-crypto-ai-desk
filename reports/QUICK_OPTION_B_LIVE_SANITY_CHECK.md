# Quick Option B — Live Sanity Check

**Date:** 2026-06-16 ~19:51 UTC · Read-only. No code changed (no critical bug found).

## 1. Stable window + infra
`OPTION_B_STABLE_FROM = 2026-06-16T12:08:15Z` (first reliable pending-tracker tick of the
fixed monitor).
- Pending-tracker ticks since: **84** (last 19:50Z, ~5.5 min cadence, continuous ~7.7h).
- Outcome checks since 12:00Z: **15,387**.
- Monitor live now: PID 14008 (`monitor-watchlist`) + scheduler PID 3336.
- **DB-lock / WAL / Operational errors: 0.** Stale locks: **none** (`.locks/` empty).

## 2. Post-stable alerts (n=26)
| type / status | count |
|---------------|------:|
| paper_entry `late_shadow` | 10 |
| paper_entry `shadow_only` (scalp) | 2 |
| close_stop `sent` | 7 |
| close_tp `sent` | 3 |
| close_expired `shadow_only` (scalp) | 4 |
| **paper_entry `sent` (pushed)** | **0** |
| duplicate paper_entry | **0** |
| duplicate close | **0** |
| same-tick paper_entry+close | **0** |

Only 10 legit non-scalp closes were pushed; every fresh entry was routed late_shadow /
scalp shadow_only (freshness + scalp guards working). No phone spam, no double-alerts.

## 3. Post-stable fresh entries (40; detection lag = det − touch)
- **Crypto (6):** ASTER, HMSTR, RIF, XPL, ALLO, HMSTR — touched 13:00–17:00Z, **detected
  16:07 / 18:53Z → multi-hour lag** (NOT ≤5–10 min). These are discovery alts; their
  detection aligns with full-cycle times, not the 5-min monitor — i.e. the monitor's
  per-tick OHLCV refresh doesn't cover these alt symbols, so Option B's speed-up doesn't
  reach them yet. All routed `late_shadow` (correct).
- **Stocks intraday:** DIA 14:30→14:46 (**16 min**), SMH/AMD/XLF 14:30→14:54 (**~24 min**),
  JPM(A) 14:30→15:20 (~50 min). Improved from the ~131 min baseline but above the 15-min
  "late" threshold (15-min stock candle floor) → still `late_shadow`.

## 4. Answers
- **Fresh crypto intraday/swing after stable?** Yes (6) — but all discovery alts detected
  multi-hour late, **not ≤5–10 min**. No fresh *watched-major* crypto entry occurred to
  measure the target.
- **entry_age ≤5–10 min?** No.
- → **`CRYPTO_LATENCY_NOT_YET_MEASURABLE_WAIT_MORE_DATA`** for the crypto target.
- **Stocks intraday improved?** Yes — detection ~16–24 min (from ~131 min), floored by the
  15-min candle; still classified late so routed `late_shadow`.
- **DB lock errors?** None.
- **Same-tick open+close recurrence?** None (0).
- **Scalp still shadow_only?** Yes (6 shadow_only, 0 sent).

## Observations (no code change — not critical bugs)
1. **Alt coverage gap:** the monitor refreshes OHLCV for its watch universe; discovery alts
   outside it still detect at the ~2h full-cycle cadence. Option B helps watched symbols;
   alts need watch-set inclusion or their own refresh to benefit. → follow-up, not a bug.
2. **15-min stock-candle floor vs 15-min "late" threshold:** stock intraday entries can
   rarely be detected in <15 min, so they almost always classify `late_shadow`. Threshold
   calibration is a separate (forbidden-here) decision.

## Verdict
Infra sanity is clean (ticking, no locks, no dups, no same-tick, scalp shadow). The crypto
≤5–10 min target remains unproven because the only fresh crypto entries were slow-detected
alts.

---

**FINAL ANSWER: `CRYPTO_LATENCY_NOT_YET_MEASURABLE_WAIT_MORE_DATA`**
(infra sanity OK; no bug; one coverage follow-up noted)
