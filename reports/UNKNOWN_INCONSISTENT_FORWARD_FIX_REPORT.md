# UNKNOWN_INCONSISTENT — Forward Fix Report (PART 2)

**Date:** 2026-06-19 · **Type:** read-model display fix. **No writer logic / trade field / historical row changed.**

## Was there a forward writer bug?
**No.** 0 inconsistent rows were produced today; the revalidator writes the no-entry statuses with `entry_triggered=False`, and the latest outcome row always agrees with the status. So no writer change was needed or made (respecting "do not rewrite historical outcomes" and "no trade-decision change").

## What was changed (display read-model only)
The display **read queries** in `scripts/backfill_display_status.py` and `scripts/paper_monitor_status.py` were switched from `MAX(entry_triggered)` / `MIN(final_r)` aggregates (which surfaced transient earlier outcome rows) to the **authoritative latest outcome row**:
```sql
LEFT JOIN (
  SELECT signal_id, entry_triggered, final_outcome, final_r,
         ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC, id DESC) rn
  FROM signal_outcomes
) o ON o.signal_id = p.signal_id AND o.rn = 1
LEFT JOIN ( SELECT signal_id, MAX(max_favorable_excursion_r) AS mfe ... ) m ...
```
This affects **display only** — it does not write to `signal_outcomes`, `proposed_signals.status`, `entry_triggered`, `final_r`, or `final_outcome`.

## Effect
- `UNKNOWN_INCONSISTENT`: **87 → 3** (3 = genuine `ambiguous` rows, kept for review).
- Phantom `CLOSED_FLAT` (from `MIN(final_r)=0`): **204 → 0**, now correct win/loss.
- No change to any stored trading value; backfill still writes **0 rows** (display columns absent).

## Verdict
**FORWARD_INCONSISTENCY_FIXED** at the *display read-model* level (the only place that was wrong); **no forward writer bug existed** → `HISTORICAL_ARTIFACT_ONLY` for the underlying data.
