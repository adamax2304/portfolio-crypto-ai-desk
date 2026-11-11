# UNKNOWN_INCONSISTENT Provenance Report (PART 2)

**Date:** 2026-06-19 · **Type:** read-only investigation. **No historical row rewritten.**

## Question
The first display backfill flagged **87** rows as `UNKNOWN_INCONSISTENT` — mostly a no-entry status (`stale_before_entry` / `entry_moved_away` / `missed_no_entry`) carrying `entry_triggered=1`.

## Who writes these statuses
- `src/signals/revalidator.py` writes `stale_before_entry` (Rule R1: age ≥ mode freshness horizon, no fill) and `entry_moved_away` (Rule R2: favorable excursion ≥ 2R, never filled) — **always with `entry_triggered=False`**.
- `src/signals/tracker.py` writes `triggered` / `expired` / `missed_no_entry` from the OHLCV walk, with `entry_triggered` derived from candle/zone overlap.
- `signal_outcomes` is **append-only** — many rows per signal across re-walks/revalidations.

## Root cause: read-model aggregation artifact (not a writer bug)
The first backfill used `MAX(entry_triggered)` **over all** outcome rows. A signal could have a transient earlier row with `entry_triggered=1` (e.g. a tracker re-walk that briefly recorded a touch, later superseded), while the **authoritative latest** row says `0`. `MAX` surfaced the stale 1 → false "inconsistent".

**Evidence (decisive):**
- Of the 87 flagged, **84 have `latest_outcome.entry_triggered = 0`** (latest row by `checked_at` agrees with the no-entry status — consistent).
- **0** inconsistent rows were updated **today** (after the latest fixes). All span **2026-05-27 … 2026-06-18** — historical only.

| status | asset/mode | n | updated range |
|---|---|---|---|
| stale_before_entry | stocks intraday | 23 | 06-09..06-16 |
| missed_no_entry | stocks intraday | 16 | 06-02..06-08 |
| missed_no_entry | crypto scalp | 12 | 05-29..06-16 |
| entry_moved_away | crypto intraday | 6 | 06-15..06-16 |
| … (others) | mixed | rest | ≤ 06-18 |

## Fix applied (read-model only, forward-safe)
Both `scripts/backfill_display_status.py` and `scripts/paper_monitor_status.py` now read the **latest outcome row** (`ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC)`) for `entry_triggered` / `final_outcome` / `final_r`, plus `MAX(max_favorable_excursion_r)` for the peak. This is a *display read-model* change — **no trade field, status, or outcome rewritten**.

**Result: UNKNOWN_INCONSISTENT dropped 87 → 3.** It also fixed a second artifact: the previous `MIN(final_r)` produced **204 phantom `CLOSED_FLAT`** (a non-terminal 0 row), now correctly resolved to win/loss via the terminal row.

## The 3 genuine remainders
All are **`ambiguous`-status** tracker outcomes (stop & TP in the same candle → tracker can't order them): `SMH` (05-27), `TAO/USDT` (06-16, 06-17). These are a legitimate tracker classification, correctly shown as "⚠️ STATUS NEEDS REVIEW", **left untouched**.

## Verdicts
- **UNKNOWN_INCONSISTENT_REVIEWED**
- **HISTORICAL_ARTIFACT_ONLY** — no forward writer bug (0 today; revalidator writes `entry_triggered=False`; latest row always consistent). The 84 were a read-model artifact (fixed); the 3 are genuine `ambiguous` historical rows (kept for review).
