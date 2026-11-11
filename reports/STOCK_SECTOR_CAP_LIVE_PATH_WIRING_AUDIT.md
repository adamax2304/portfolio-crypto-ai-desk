# Stock Sector-Cap — Live-Path Wiring Audit (PART 3)

**Date:** 2026-06-17 · **Mode:** read-only verification. **No cap value changed, no soft/hard switch, no cap=3.**
**CSV:** `STOCK_SECTOR_CAP_WOULD_BIND_REPLAY.csv` (day × direction × cluster).
**Verdict:** cap is **WIRED but EFFECTIVELY INERT on the live path** → proceed to shadow-only fix (see `STOCK_SECTOR_CAP_SHADOW_ONLY_FIX_PLAN.md`).

## Two cap implementations exist
| Function | What it does | Where it runs |
|---|---|---|
| `apply_stock_concentration_caps(signals, existing_positions)` | **Batch / day-level**: ranks the *whole set* of candidates within (day, direction, bucket); this is what would bind correlated clusters | **only** in `tests/` and `scripts/counterfactual_stock_concentration.py` — **NOT on any live path** |
| `concentration_for_live_signal(store, signal)` | **Per-signal**: ranks THIS one signal against `store.load_active_signals()` (currently-open A/B stock-intraday peers) at alert time | `src/notifiers/paper_entry.py:491` — the **live** path |

## Why it fired 0× live (root cause)
The live path (`concentration_for_live_signal`) only binds when, **at the exact instant a paper-entry alert fires**, there are already ≥1 (half-size) or ≥2 (shadow) *non-terminal* A/B stock-intraday positions in the **same (risk_bucket, direction)**. Three structural reasons that almost never holds:

1. **Per-signal vs batch.** The live check ranks one signal against *concurrently-open* peers — not against the day's full candidate set. The would-bind replay (18/92 cluster-day groups) is a **day-batch** view; those names rarely co-exist as open positions at one moment.
2. **Fast terminal transitions.** Intraday A/B signals frequently reach a terminal status (stop/tp/expire) quickly, so by the time the next same-bucket name alerts, `load_active_signals()` (filtered to `_NON_TERMINAL`) no longer counts the earlier one.
3. **Narrow eligibility + timing lag.** Requires `asset_class=stocks` AND `mode=intraday` AND `tier∈{A,B}` AND known `risk_bucket`; near-simultaneous triggers in one monitor tick may not yet see each other registered as open.

So the code is **not a dead no-op** — it is correctly wired and would set `half_size`/`shadow_sector_cap` if peers were concurrently open. It simply almost never sees the concurrency it needs. The *binding* logic (day-batch) lives in a function that the live path never calls.

## Evidence (replay)
| Metric | Value |
|---|---|
| Cluster-day groups (stocks intraday) | 92 |
| Groups that would bind under cap-2 (day-batch view) | **18** |
| Times the cap actually shadowed/half-sized **live** | **0** |

The 18 vs 0 gap is exactly the per-signal-concurrency vs day-batch discrepancy.

## Conclusion
- The cap **value and rules are fine and untouched**.
- The live path is structurally unable to observe the correlation the day-batch view sees.
- Next step is **observation, not enforcement**: run the day-batch cap in **shadow** on the monitor and record a `would_bind_sector_cap` label so we can measure real binding before deciding whether to move the live path to a batch-aware check. No value change, no blocking.
