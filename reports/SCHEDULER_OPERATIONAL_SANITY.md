# Scheduler Operational Sanity (PART 4)

**Date:** 2026-06-17 · **Verdict:** OK.

## Dry-run plan
`python -m scripts.run_default_market_schedule --run-once --dry-run` → LLM-auto-invoke check OK (no Opus/Claude tokens in plan).

## Step inventory (build_cycle_steps, weekday, no long-horizon)
- **Total steps: 19 · duplicates: none.**
- The 3 prior-deploy additions are present and **non-fatal**:
  - `catalyst integrity scan` → `command_nonfatal` (runs after `catalyst / narrative scan`)
  - `ohlcv archive (5m/15m)` → `command_nonfatal`
  - `open intraday lifecycle review` → `command_nonfatal`
- This sprint added **no new scheduler steps** (the backfill is a manual/occasional job, not per-cycle; the shadow ledger is run on demand or can be added later).

## Checks
- [x] expected steps present
- [x] new steps non-fatal (a failure logs + continues)
- [x] no LLM auto-invoke accidentally added
- [x] no duplicate steps

## Note on cadence / cost
- The per-cycle additions are light (catalyst integrity scan + lifecycle review are read-only DB scans; ohlcv archive is a local CSV merge). No frequency reduction needed.
- The **historical backfill** is intentionally NOT in the per-cycle plan (it's a heavier network job); run it manually / occasionally until coverage is sufficient.
