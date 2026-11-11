# Stock Sector-Cap — Shadow-Only Fix Plan (PART 3)

**Date:** 2026-06-17 · **Status:** plan only — not implemented in this stage (no behavior change permitted).
**Constraints honored:** cap value unchanged (1.0/0.5/0×), no cap=3, not made soft/hard, no blocking.

## Goal
Make the **binding** the day-batch view already detects (18/92 groups) *visible and measured* in production, without changing what trades fire. Turn the cap from "wired but blind" into "wired + observable", so a future enable decision rests on real live binding counts, not just a replay.

## Proposed change (shadow/label only)
1. **On the stocks monitor tick** (`src/stocks/monitor.py`, where `load_active_signals()` is already called):
   - Gather today's eligible A/B stock-intraday candidates (open + already-alerted), run them through the existing **batch** `apply_stock_concentration_caps(...)` in-memory.
   - For each signal, record a **shadow** field `would_bind_sector_cap` ∈ {`actionable`,`half_size`,`shadow_proxy_duplicate`,`shadow_sector_cap`} and `would_bind_rank`.
   - Write these into `signal_alerts` metadata / a `sector_cap_shadow` row — **never** into the live sizing/actionability decision.
2. **Telegram/Control-Plane visibility (add-only):** surface `would_bind_sector_cap` as an informational line on the existing stocks-intraday alert (see PART 7). No routing/channel change.
3. **Keep the live `concentration_for_live_signal` path exactly as is** — it remains the only thing that can affect an alert, and it still effectively no-ops.

## Why shadow-first (not just widen the live check)
Widening the live per-signal check to a batch-aware check *would change behavior* (some 2nd/3rd correlated names would flip to half/shadow). That is a production change and is out of scope. Shadow-first lets us:
- Count how often the cap **would** bind live over ≥2–4 weeks.
- Confirm the day-batch eligibility (bucket assignment, proxy groups) is sound on real data.
- Quantify the R impact of those would-bind names before clipping any size.

## Acceptance / measurement
- After ≥10 trading days of shadow, compare: # would_bind_sector_cap events vs the 0 the live path produced; net R of would-shadowed names vs would-actionable.
- Only if shadow shows the cap would meaningfully cut correlated drawdown **without** clipping net-positive clusters → propose moving the live path to batch-aware (still paper, still your explicit approval).

## Rollback
Remove the shadow field write + the Telegram line. Zero impact on trades (it never touched them).

## Explicitly NOT in this plan
- No change to cap weights, eligibility tiers, or bucket/proxy maps.
- No switch to cap=3, no soft sizing in production, no blocking, no live routing change.
