# Proposed Risk-Management System (PART 8) — PROPOSAL, default-OFF

**Date:** 2026-06-23. **Proposal only. Not implemented. Default off. Paper-only after approval. Production not allowed.** Evidence: PART 4–7 (Model F flips actionable book to +74R / PF 1.43, ~30d replay).

## Core design — "Early MFE-armed protection + light cohort filter"
```yaml
risk_management:
  mode: shadow_candidate          # shadow_candidate | off | paper  (only 'off'/'shadow' without approval)
  feature_flag: paper_risk.mfe_protection   # default FALSE
  paper_only: true
  default:                        # MODEL F — the winning candidate
    arm_protection_at_mfe_r: 0.6  # once price is +0.6R favorable -> stop to breakeven
    breakeven_offset_r: 0.0
    lock_profit_at_mfe_r: 1.0     # once +1R favorable -> lock +0.5R
    lock_level_r: 0.5
    runner_target: tp3            # let it run to TP3 once protected
    partial_tp1: 0.0              # no partial in the default (BE-on-runner does the work)
  trend_runner_cohorts:           # allow full TP3 runner
    - crypto_swing_narrative_rs_momentum
    - crypto_failed_bounce_short
    - { regime: [bearish trend, risk_off], direction: short }
  tighter_cohorts:                # arm BE sooner (+0.5R), lock at +0.8R
    - stocks_intraday_rth_momentum
    - { regime: [chop, range/chop, transition] }
  disabled_or_shadow_cohorts:     # do NOT trade / keep shadow
    - crypto_intraday_catalyst_or_momentum   # worst actionable (chase longs)
    - crypto_scalp_momentum
    - stocks_swing_watchlist_rs
    - stocks_invest_watchlist_30d
    - tier: C
  app_telegram_fields:            # display only
    - mfe_protect_armed: bool
    - protected_exit_r: float
    - close_reason: [be_scratch, profit_lock, tp_runner, stop, expired]
```

## Rules in words
- **Default (every actionable trade):** when price reaches **+0.6R favorable**, move stop to **breakeven**; at **+1R favorable**, lock **+0.5R**; otherwise let it run toward TP3. This protects the +0.5R→TP1 give-back zone that PART 2 identified as the loss source.
- **Trend-runner cohorts** (crypto swing, failed-bounce-short, trend-aligned shorts): keep the TP3 runner (they reach it and earn it).
- **Tighter cohorts** (stocks intraday momentum, chop): arm BE earlier (+0.5R) and lock sooner — they give back fast.
- **Disabled/shadow:** crypto_intraday_catalyst (chase longs, weakest), plus the already-shadow scalp / stocks-swing-invest / C-tier.

## Not allowed (explicit)
No change to entries, scoring, routing, TP/SL generation, or production exits. No live/auto-live. No force-close. No historical rewrite. This config is **measured in shadow** (compute the model R beside recorded R), and only graduates to a **paper feature-flag** after the PART-9 gates pass.

## Verdict
`RISK_MANAGEMENT_SYSTEM_PROPOSED` (default-off shadow candidate; Model F core + cohort filter). Implement only on operator approval, paper-only first.
