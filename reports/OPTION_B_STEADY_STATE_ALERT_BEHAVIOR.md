# Option B — Steady-State Alert Behavior (PART 3–4)

**Date:** 2026-06-16 ~15:12 UTC · Window: post-stable (≥ 2026-06-16T12:08:15Z)

## PART 3 — Fresh crypto entry proof

**Fresh post-stable crypto entries (intraday or swing): 0.**

No crypto signal triggered an entry after `OPTION_B_STABLE_FROM`. Every crypto entry seen
this session touched **before** the monitor stabilized (09:45–10:15Z backlog) and was
detected on catch-up. Therefore:

```
CRYPTO_LATENCY_NOT_YET_MEASURABLE_WAIT_MORE_DATA
```

(Per-entry table for fresh crypto entries is empty — nothing to list.)

## PART 4 — Alert behavior (post-stable, 19 alerts)

| alert_type | telegram_status | count | meaning |
|------------|-----------------|------:|---------|
| paper_entry | `late_shadow` | 6 | late entries (4 stocks @16–25m + 2 crypto backlog) — **not pushed**, no chase ✅ |
| paper_entry | `shadow_only` | 2 | crypto scalp — **not pushed** ✅ |
| close_expired | `shadow_only` | 4 | crypto scalp closes — **not pushed** ✅ |
| close_stop | `sent` | 5 | legit non-scalp closes — **pushed** ✅ |
| close_tp | `sent` | 2 | legit non-scalp closes — **pushed** ✅ |

| Check | Expected | Observed |
|-------|----------|----------|
| same-tick paper_entry+close pairs | 0 | **0** ✅ |
| duplicate paper_entry / signal | 0 | **0** ✅ |
| duplicate close / (signal,type) | 0 | **0** ✅ |
| DB-lock / OperationalError alerts | 0 | **0** ✅ |
| stale locks (`.locks/`) | none | **none** ✅ |
| monitor tick count (since stable) | — | **34** |
| pending checks (since 12:00Z) | — | ~5,900 across ticks |
| scalp routing | shadow_only | **shadow_only** ✅ |
| non-scalp fresh entries | send | (none fresh yet; legit closes sent ✅) |
| very-late entries | late_shadow | **late_shadow** ✅ |

**Only pushed to phone post-stable:** 7 legitimate non-scalp closes (5 stop, 2 TP). **No
stale-entry chasing, no scalp pings, no double alerts.** The freshness + shadow routing is
doing exactly its job on live data.

**PART 3–4 status: DONE.** Alert integrity perfect; crypto entry latency not yet
measurable (0 fresh crypto entries).
