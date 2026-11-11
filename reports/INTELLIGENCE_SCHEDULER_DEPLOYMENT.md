# Intelligence Scheduler Deployment (PART 7)

**Date:** 2026-06-18 · **Verdict:** **INTELLIGENCE_SCHEDULER_READY**

## Steps added to `run_default_market_schedule.py` (all non-fatal, no duplicates)
| Step | When | Command | Cadence |
|---|---|---|---|
| `intelligence layer update` | every cycle (after `ohlcv archive`) | `python -m scripts.intelligence_update --limit 80` | ~2h |
| `intelligence onchain risk update (daily)` | daily long-horizon pass only | `python -m scripts.onchain_risk_update --limit 40` | daily (no-op until config) |

Health report (`reports/INTELLIGENCE_LAYER_HEALTH.md`) is written by `intelligence_update` each run (and via `--health-only`).

## What runs where (performance discipline)
- **Background (scheduler):** timeline bootstrap/compaction, derivatives trajectory, squeeze phase, on-chain (when configured), health. These do the price-frame loads + cache writes — never in the alert path.
- **Alert path:** only cached reads + the pure thesis (p95 63ms).

## Verification
- Cycle plan (long-horizon) = **24 steps, no duplicates**; both intelligence steps present as `command_nonfatal`.
- `intelligence_update --limit 30` ran: timeline bootstrap 594 events, deriv+phase cached for 31 symbols, health written.
- `onchain_risk_update` → `INTERFACE_READY_CONFIG_MISSING`, no network.
- Dry-run plan does not execute network calls (steps are subprocess argv only).

## Cadence note
The scheduler has no per-step cadence primitive beyond the daily long-horizon window, so: derivatives/squeeze/timeline ride the ~2h cycle (cheap, cache-based) and on-chain rides the daily pass (heavier, currently no-op). If finer cadence is wanted later, split into a dedicated lightweight loop — documented, not over-wired now.
