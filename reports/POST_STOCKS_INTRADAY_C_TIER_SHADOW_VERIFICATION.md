# POST — Stocks-Intraday C-Tier Shadow Verification (PART 1)

**Date:** 2026-06-17 · **Verdict:** **STOCKS_INTRADAY_C_TIER_SHADOW_READY**

## Checklist
- [x] Config flag `tier_policy.stocks_intraday_c_tier = shadow_review_only` present; `actionable` reverts.
- [x] Restriction scoped to stocks+intraday+C only (unit tests for A/B, crypto, swing/invest).
- [x] Payload labels emitted (`c_tier_restriction_applied/reason/diagnostic_or_policy/c_tier_policy`).
- [x] C-tier stocks-intraday never pushed as actionable (already blocked at `decide_paper_entry`; confirmed `sent=False`).
- [x] A/B stocks-intraday still actionable (test).
- [x] No scoring/tier/TP/SL/size change (label dict carries none; concentration suite unregressed).
- [x] Control Plane already classifies C-tier non-actionable; new labels flow read-only.
- [x] All modules compile; full suite re-run in PART 9.

## Net effect
- **Behavior:** unchanged (C-tier was already non-actionable). The change removes ambiguity: the restriction is now a documented, single-source policy with explicit labels, instead of an implicit `tier=C not actionable` string scattered across the producer + consumer.
- **The −34R C-tier "leak"** is confirmed to be a **measurement artifact** (tracked-but-never-traded C-tier), so the actionable book never carried it. No live exposure was removed because none existed — which is the safest possible outcome.

## Optional follow-up (NOT done — needs your call)
If you also want to stop *tracking/registering* C-tier stocks-intraday (to clean the measured book), that's a separate change to `track_tiers` / watchlist registration — it would reduce measurement data, so it's left out by default.

## Rollback
Set `tier_policy.stocks_intraday_c_tier: actionable` (one line) or delete `src/signals/tier_policy.py` + revert the two wiring blocks. Zero trade impact.
