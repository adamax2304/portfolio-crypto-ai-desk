# Option B Coverage Fix — Live Verification (PART 7)

**Date:** 2026-06-16 ~23:35 UTC

## Verdict

```
OPTION_B_COVERAGE_FIX_PARTIAL_WAIT_MORE_DATA
```

The fix is **deployed and mechanically verified live**; full end-to-end proof (a *fresh*
discovery-alt entry detected ≤5–10 min via the running monitor) needs forward observation
because no new alt entry triggered in the short post-deploy window.

## What is confirmed live
- **Refresh runs on the tick, before the tracker:**
  ```
  Tick 1 at 23:33:37
    pending OHLCV refresh: 23 symbols (1 skipped: unsupported market/data)
    pending tracker: checked=162 tp=156 stop=0 exp=0
  ```
  → pending A/B crypto symbols (incl. discovery alts) now have **fresh candles** before
  `track_pending_entries` reads them. The 1 skip is correctly logged (unsupported market).
- **Direct refresh-path smoke:** GPS/BCH/SOL/NIGHT cache files **REFRESHED** (mtimes
  advanced), 0 failed — the mechanism updates real cache for live pending alts.
- **No regressions:** 0 DB-lock / WAL errors, no stale locks (`.locks/` empty), 0 duplicate
  paper_entry, 0 duplicate close, no same-tick open+close, 0 new alerts mis-routed.
- **Scalp:** remains shadow_only (included in refresh for shadow-tracking freshness, never
  pushed).

## Why PARTIAL (not CONFIRMED)
Success target is "watched majors AND pending discovery alts both detected within one
monitor tick after touch; crypto intraday detection_lag ≤5–10 min for refreshed symbols."
The **prerequisite is proven** (alts' candles are now refreshed every tick, so a future
touch is visible to the tracker on the next ~5-min tick). But **no fresh alt entry has
triggered since deploy**, so the empirical end-to-end ≤5–10 min datapoint is not yet
recorded. This is the same "wait for a fresh entry" gap as before — now with the coverage
hole closed.

## Next step
Let the monitor run 30–90 min with the new code (the bounded run + the scheduler's next
cycle both carry it). When a fresh pending-alt entry triggers, re-check:
`python scripts/audit_latency_expired.py latency` → expect refreshed crypto symbols'
`detection_lag` ≤5–10 min. That flips the verdict to `OPTION_B_COVERAGE_FIX_CONFIRMED`.

## Deploy note
A running monitor process does not hot-reload code; the fix activates on a fresh monitor
(the scheduler spawns one each 2h cycle, or a manual `monitor-watchlist --interval 300`
restart — done here for the bounded verification run).

**PART 7 status: DONE — mechanism deployed + verified; latency datapoint pending a fresh
entry.**

---

**FINAL ANSWER: `OPTION_B_COVERAGE_FIX_PARTIAL_WAIT_MORE_DATA`**
