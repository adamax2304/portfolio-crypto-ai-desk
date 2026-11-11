# Telegram Entry Freshness Label + Late-Entry Routing (PART 5)

**Date:** 2026-06-16 · File: `src/notifiers/paper_entry.py`

## What was implemented

A pure `entry_freshness(entry_triggered_at, now)` helper + a routing branch in
`send_paper_entry_alert`. The label is computed from the **entry-touch timestamp vs send
time** — it never fabricates a fresher age (constraint honored).

### Classification (threshold `LATE_ENTRY_SHADOW_MINUTES = 15`)

| Age (touch → send) | Label line | Routing |
|--------------------|-----------|---------|
| ≤ 2 min | `Entry freshness: fresh 45s` | **sent** |
| ≤ 5 min | `Entry freshness: acceptable 3.4m` | **sent** |
| 5–15 min | `Entry freshness: late 12m — check price before manual entry` | **sent** (with caveat) |
| > 15 min | `Entry freshness: very late 40m — NOT actionable manually` + header `[LATE ENTRY DETECTED — DO NOT CHASE]` | **late_shadow** (recorded, NOT pushed) |
| unknown ts | `Entry freshness: unknown — treat as NOT actionable` | **late_shadow** |
| crypto scalp (any age) | `[SHADOW ONLY — DO NOT TRADE]` + freshness line | **shadow_only** (unchanged) |

### Verified sample output

```
FRESH        → status=sent        first line "[🟢 PAPER ENTRY — TRIGGERED]"   "Entry freshness: fresh 0s"
LATE 12m     → status=sent        "Entry freshness: late 12m — check price before manual entry"
VERY-LATE 40m→ status=late_shadow first line "[LATE ENTRY DETECTED — DO NOT CHASE]"  "Entry freshness: very late 40m — NOT actionable manually"
```

## Rules honored

- ✅ `entry_age > 15 min` → `[LATE ENTRY DETECTED — DO NOT CHASE]` banner.
- ✅ very-late / unknown / already-terminal → **not pushed** as actionable; routed
  `late_shadow` (recorded in `signal_alerts` with `telegram_channel="shadow_only_late"`,
  `reason_skipped="late_entry"`) so journal/research keep visibility.
- ✅ non-late valid entries are **not** suppressed (fresh/acceptable/late all `sent`).
- ✅ no scoring / TP / SL / threshold change — notification layer only.
- ✅ does not make late alerts look fresh — the age is measured, clamped to ≥0 only for
  candle/clock alignment, and labelled honestly.
- ✅ crypto scalp still `shadow_only` (predicate runs first; freshness is informational).

## Honest note on the current effect

Per PART 2, current median entry-age is **~135 min** (detection only at the 2h
`track-signals` cadence). So **today, essentially all non-scalp paper-entries are
>15 min old and will route `late_shadow` (not pushed)**. That is the correct, honest
behavior: the system stops pinging the operator with entries that cannot be acted on.
Once the Phase-2 cadence fix (PART 4 Option B/A) lands and entry-age drops below 5–15 min,
those same alerts will classify fresh/acceptable/late and **push normally** — no further
code change needed. The threshold is a single named constant for easy tuning.

Close/outcome alerts are unchanged — they report results (not entry-timing-sensitive) and
continue to send.

## Tests (in `tests/test_alert_dispatch_gates.py`)

- `test_entry_freshness_classification` — fresh/acceptable/late/very-late/unknown.
- `test_very_late_nonscalp_entry_routes_late_shadow` — >15m → `late_shadow`, not sent,
  `[LATE ENTRY DETECTED — DO NOT CHASE]` present.
- `test_fresh_nonscalp_entry_sends_with_label` — fresh → `sent`, `Entry freshness:` line.
- Updated `test_scalp_downgrade` (5–8) + `test_paper_entry_alerts` (10) to use fresh
  timestamps so they test the intended "fresh non-scalp entry sends" guarantee.

**PART 5 status: DONE (implemented + tested).**
