# Stocks-Intraday C-Tier → Shadow/Review-Only — Implementation (PART 1)

**Date:** 2026-06-17 · **Verdict:** **STOCKS_INTRADAY_C_TIER_SHADOW_READY**
**Routing / actionability + labels ONLY. No scoring, tier, TP/SL, or size change. A/B and crypto untouched.**

## Key finding (honest framing)
C-tier was **already** non-actionable everywhere:
- `decide_paper_entry` → `should_send=False`, `reason_skipped="tier=C not actionable"` (all assets);
- stocks monitor `_load_active_ab` filters alerts to A/B;
- Control Plane `actionability.classify` lists "C-tier → not actionable".

So the 30d −34R C-tier figure is a **tracking artifact**, not live actionable exposure. This change therefore does **not** alter trade behavior — it makes the restriction an **explicit, configurable, labeled policy** (single source of truth + visibility), which is the safe, correct deliverable.

## What was built
- **Config flag** `config/signal_tracking.yaml` → `tier_policy.stocks_intraday_c_tier: shadow_review_only` (`actionable` would re-enable C-tier alerts).
- **`src/signals/tier_policy.py`** — `load_stocks_intraday_c_tier_policy()`, `is_restricted(signal, policy)`, `c_tier_restriction_fields(signal, policy)`. Fails safe to restricted. Scoped strictly to **stocks + intraday + C** (crypto any tier and stocks A/B/swing/invest never restricted).
- **Payload labels** (add-only): `c_tier_restriction_applied`, `c_tier_restriction_reason="stocks_intraday_c_tier_30d_negative"`, `diagnostic_or_policy="risk_restriction"`, `c_tier_policy`.
- **Wiring:**
  - `src/notifiers/paper_entry.py`: a belt-and-suspenders shadow route (`shadow_only_c_tier` / `telegram_status=shadow_c_tier`) if a restricted C-tier ever reached the alert path (it is already blocked upstream), plus the labels in the payload.
  - `src/risk/risk_guards.py`: emits the C-tier labels on every assembled payload (so reports/Control Plane show the restriction).
  - The stocks monitor's existing A/B filter remains the operative gate; the policy documents/centralizes it.
- **Telegram/Control Plane** clearly label restricted C-tier as shadow/review-only.

## What it does NOT do
- No scoring change (the signal stays C-tier with its score).
- No TP/SL, size, or sector-cap change.
- Does not touch A/B stocks intraday or any crypto tier.
- Does not change *tracking/registration* (C-tier still tracked for measurement) — only actionability/labeling.

## Verification
- A B-tier stocks-intraday entry still sends (test).
- A C-tier stocks-intraday entry is never pushed (`sent=False`, `reason_skipped` contains "not actionable") and is labeled `c_tier_restriction_applied=True` (test).
- Crypto C-tier and stocks A/B → not restricted (tests).
- Existing stock concentration suite unregressed.

See `STOCKS_INTRADAY_C_TIER_SHADOW_TEST_RESULTS.md` + `POST_STOCKS_INTRADAY_C_TIER_SHADOW_VERIFICATION.md`.
