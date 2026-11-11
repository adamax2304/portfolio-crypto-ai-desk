# Circuit Breaker — Would-Pause / Alert-Only Audit (PART 2)

**Date:** 2026-06-17 · **Mode:** diagnostic / alert-only counterfactual. **No hard block exists or is enabled.**
**CSV:** `CIRCUIT_BREAKER_WOULD_PAUSE_AUDIT.csv` (one row per UTC-day × asset_class).
**Verdict:** **IMPLEMENT_CIRCUIT_BREAKER_ALERT_ONLY** (would-pause flag + Telegram alert); hard auto-pause = `THRESHOLD_NEEDS_MORE_DATA` (do **not** enable hard yet).

## Method
For each UTC day × asset_class over the 7d dataset: sum realized R in exit order, count stops, track max consecutive stops, and replay each threshold variant. The counterfactual `R_if_paused_at_2R` blocks any trade *opened after* cumulative R first crosses −2R that day (entries before the trip are untouched).

## Threshold variants
| Variant | Rule | Days that would fire (7d) |
|---|---|---|
| A | daily realized ≤ −2R | **7** |
| B | daily realized ≤ −3R | **4** |
| C | ≥ 3 stops in a day | **10** |
| D | ≥ 3 consecutive stops | several (see CSV `max_consec_stops`) |
| E | A **or** C | 10+ |
| F | A **and** C (loss *and* volume) | overlaps the worst days |
| G | −2R **and** ≥3 consec | the 06-1x crypto cluster |

## Worst days (from CSV)
| Day | Asset | Trades | Realized R | Stops | Max consec | Long stops | R if paused @−2R | R saved |
|---|---|---|---|---|---|---|---|---|
| 06-11 | stocks | 36 | −16.0 | 20 | 5 | 0 | −2.0 | **+14.0** |
| 06-15 | crypto | 50 | −8.0 | 28 | 6 | 28 | −2.0 | +6.0 |
| 06-14 | crypto | 13 | −7.0 | 7 | 7 | 7 | −2.0 | +5.0 |
| 06-12 | crypto | 8 | −6.0 | 7 | 4 | 7 | −2.0 | +4.0 |
| 06-15 | stocks | 51 | −2.0 | 8 | 4 | 1 | −2.0 | 0.0 |

## Counterfactual totals (optimistic upper bound)
- Days that would have tripped the −2R breaker: **7**; the −3R breaker: **4**; the 3-stops breaker: **10**.
- Aggregate loss avoided by a −2R same-day entry-halt: **≈ 25R** across the window.
- Winners missed by the −2R halt in this window: **0R** (the halt fired only on already-deep-red days; the day's remaining trades were net-negative).

### Limitations (why "alert-only", not "hard" yet)
1. The "R saved" figure is an **upper bound** — it assumes a clean same-day halt and that no post-halt entry would have recovered the day. Real days vary.
2. 7 days is **not enough** to set a safe *hard* threshold; one or two outlier days (06-11 stocks −16R) dominate. The spec's own bar is ≥30d before any hard block.
3. Long-stop concentration on crypto (06-12/14/15 = 7/7/28 long stops) suggests the breaker should be **scoped by direction/asset**, which also argues for observing first.

## Recommendation
- **Ship now (alert-only):** in the monitor tick, compute rolling realized R per asset/day and emit a `circuit_breaker` would-pause flag into `signal_alerts` + a Telegram alert when ≤ −2R **or** ≥3 consecutive stops. No entry is blocked.
- **Do NOT** enable a hard auto-pause until a ≥30d threshold sweep confirms the −2R/−3R/N-consec choice. Re-run this CSV monthly.
