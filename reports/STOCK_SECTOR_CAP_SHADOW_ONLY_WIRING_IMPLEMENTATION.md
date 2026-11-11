# Stock Sector-Cap — Shadow-Only / Would-Bind Wiring Implementation (PART 3)

**Date:** 2026-06-17 · **Verdict:** **SECTOR_CAP_SHADOW_ONLY_WIRING_READY**
**Cap value unchanged (1.0/0.5/0×). No cap=3. Not soft/hard. No routing change.**

## Problem recap
The live path (`concentration_for_live_signal`) ranks a signal only against *concurrently-open* peers → fired 0× live, while the day-batch view would bind 18/92 cluster-day groups. The binding logic (`apply_stock_concentration_caps`) was never on the live path.

## What was built
- **`src/signals/sector_cap_shadow.py`**
  - `would_bind_from_batch(batch_signals, signal_id)` — runs the **existing, tested** batch cap over the day's eligible candidates and reads off this signal's would-be decision (delegates to `apply_stock_concentration_caps`; cap value untouched).
  - `would_bind_sector_cap(store, signal, now)` — store wrapper: gathers today's stocks-intraday A/B candidates via `load_signals_for_period(since=start_of_day, asset_class='stocks', mode='intraday')`, ensures the current signal participates, runs the batch cap in **shadow**, and reports the would-bind status alongside the **actual** live concentration status. Fails open.
- **Wiring:** surfaced via `assemble_risk_guard_fields` → payload + Control Plane (read-only).

## Fields emitted (diagnostic only)
`would_bind_sector_cap` (actionable/half_size/shadow_proxy_duplicate/shadow_sector_cap), `would_sector_rank`, `would_sector_bucket`, `would_sector_reason`, `actual_concentration_status`, `diagnostic_only=true`.

## Actual vs would (the measurement)
- `actual_concentration_status` = what the live per-signal path produced (≈ always `actionable`/`not_applicable` because it sees no concurrent peers).
- `would_bind_sector_cap` = what the day-batch cap would do.
- The **gap** between them is exactly the "0× live vs 18/92 day-batch" discrepancy, now visible per signal for measurement.

## Safety
- Does **not** apply to routing or sizing — the live `concentration_for_live_signal` path is unchanged and remains the only thing that can affect an alert.
- Cap weights, eligibility, bucket/proxy maps unchanged.
- Fails open to `not_applicable` on any error.

See `STOCK_SECTOR_CAP_SHADOW_ONLY_TEST_RESULTS.md` and `STOCK_SECTOR_CAP_SHADOW_ONLY_FORWARD_PLAN.md`.
