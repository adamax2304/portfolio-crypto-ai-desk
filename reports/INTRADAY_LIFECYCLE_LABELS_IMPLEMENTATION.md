# Intraday Lifecycle Labels / Revalidation — Implementation (PART 5)

**Date:** 2026-06-17 · **Verdict:** **INTRADAY_REVALIDATION_ALERT_ONLY_READY**
**Mode:** labels/flags only. **No force-close, no hard expire, no size change.**

## What was built
- **`src/signals/lifecycle.py`** — `compute_lifecycle_label(signal, *, now, entry_triggered_at, status, regime_at_entry, regime_now)`: pure, fail-open.
- Wired via `assemble_risk_guard_fields` → payload + Control Plane; warning line added to actionable alerts when revalidation is required.

## Fields emitted
`lifecycle_label`, `held_hours`, `next_day_revalidation_required`, `carryover_warning`, `rth_close_approaching`, `rth_overnight_hold`, `catalyst_stale`, `regime_changed_since_entry`, `diagnostic_only=true`.

## Label rules (intraday only; terminal/non-intraday → `closed`/`n/a`)
**Crypto:** `fresh_intraday` (<6h) → `aging_intraday` (6–12h) → `stale_intraday` (≥12h) → `expired_at_0R_candidate` (≥24h, past validity). Created on an earlier UTC day or regime change → `intraday_carryover` / `intraday_carryover_requires_review`.
**Stocks (RTH-aware):** `rth_close_approaching` (within the hour before ~20:00 UTC cash close); `rth_overnight_hold` (held outside RTH or across a day); carryover → `intraday_carryover_requires_review`; else fresh/aging by age.
`next_day_revalidation_required=True` on carryover / overnight / ≥16h crypto / ≥24h.

## Why label-only (not force-close)
The prior audit showed overnight carry was **net-positive** (crypto intraday >12h = +10R; overnight carry +17R). A hard EOD-flatten/expire would destroy positive R. So the system **relabels + flags for revalidation** and lets the operator (or the existing revalidator) decide — it never auto-closes.

## Safety
- The result dict contains only labels/flags — there is **no** `action`/`force_close`/`flatten`/size field (asserted in tests).
- Fails open; pure function (no I/O).
- `catalyst_stale` is set only when derivable (news-supported + aged past validity); otherwise `None` (never faked).
