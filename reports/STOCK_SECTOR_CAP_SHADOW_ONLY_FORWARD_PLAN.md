# Stock Sector-Cap — Shadow-Only Forward Plan (PART 3)

**Date:** 2026-06-17 · **Status:** measurement plan — no behavior change permitted in this stage.

## Now (this stage)
- `would_bind_sector_cap` + `would_sector_rank/bucket/reason` + `actual_concentration_status` are emitted per stocks-intraday A/B alert (payload + Control Plane).
- The **live** sizing/actionability path is unchanged (`concentration_for_live_signal` still the only thing that can affect an alert).

## Measurement window (≥10 trading days)
Collect from `signal_alerts.payload_json`:
1. Count of `would_bind_sector_cap ∈ {half_size, shadow_sector_cap, shadow_proxy_duplicate}` vs the live `actual_concentration_status` (expected ≈ 0 binds live).
2. Net R of would-shadowed names vs would-actionable names (did the cap target the losers or clip winners?).
3. Bucket/proxy correctness on real data (any misbucketed names?).

## Decision gate (after the window, with explicit approval)
- **If** would-bind frequently coincides with net-negative correlated stacking **and** does not clip net-positive clusters → propose moving the live path to a **batch-aware** check (still paper).
- **Else** keep shadow-only / reconsider eligibility.

## Constraints (unchanged)
- Cap value stays 1.0/0.5/0×. No cap=3. No soft sizing in production. No blocking. No live routing change. No change to bucket/proxy maps without separate review.

## Rollback
Remove the `would_bind_sector_cap` block from `assemble_risk_guard_fields` + delete `src/signals/sector_cap_shadow.py`. Zero trade impact (it never touched trades).
