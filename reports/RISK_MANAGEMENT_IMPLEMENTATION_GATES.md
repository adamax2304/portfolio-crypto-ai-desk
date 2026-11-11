# Risk-Management Implementation Gates (PART 9)

**Date:** 2026-06-23. Gates that must pass before any future implementation. Current status vs each gate shown.

## Paper-only candidate gate (shadow → paper feature-flag)
| gate | threshold | current (Model F, actionable) | pass? |
|---|---|---|---|
| realistic replay positive **after cost/slippage buffer** | net R > 0 after haircut | +74.1R gross; **cost haircut not yet applied** (BE-heavy = 42% scratch → many exits) | ⚠️ **unverified** |
| sample size | n ≥ 100 total or ≥30/cohort | 584 total ✓; failed-bounce-short n=31 ✓; some sub-cohorts <30 | ✅ (total) / ⚠️ (some cohorts) |
| PF | > 1.15 | **1.43** | ✅ |
| avg R/trade | > 0.05 | **+0.127** (hybrid +0.149) | ✅ |
| max drawdown < baseline | yes | BE-scratches reduce loss tail vs fixed-stop | ✅ (proxy) |
| stable across ≥2 windows | both positive | window1 +17.6R, window2 +56.5R ✓ **but same 30d epoch** | ⚠️ **not independent regimes** |
| no single-symbol dependency | no symbol > ~20% | top symbol 18% (SMCI +13.5/+74); −top3 still +44.7R | ✅ |
| feature-flag default-off | required | designed (PART 8) | ✅ (on build) |
| tests available | required | `tests/test_realistic_pnl_models.py` (Model F covered) | ✅ |

**Verdict on paper gate:** **NOT yet cleared.** Two blockers: (1) no **cost/slippage haircut** applied to a BE-heavy strategy; (2) "2 windows" are the **same 30-day market epoch**, not independent regimes. Both must be resolved (cost model + ≥2–4 weeks fresh forward paper spanning a non-bullish stretch) before a paper flag.

## Production gate (paper flag → production, later)
| gate | threshold |
|---|---|
| forward paper validation | 2–4 weeks, model still net-positive after costs |
| same model positive out-of-epoch | holds in ≥1 non-bullish/chop regime |
| Telegram/app accounting correct | realistic_r shown; no touch-based illusion |
| manual operator review | explicit sign-off |
| no live automation initially | manual paper → manual micro-live only |

## Required sequence
1. **Shadow ledger** (compute Model F R beside recorded R every cycle) — measurement only, default-off.
2. Apply **cost/slippage haircut** + re-confirm > 0.
3. **Forward paper** ≥2–4 weeks across a fresh epoch.
4. Re-check all paper gates → operator approval → **paper feature-flag**.
5. Only after sustained paper success: manual production review (still no auto-live).

## Verdict
`RISK_IMPLEMENTATION_GATES_DEFINED` — paper gate **partially met** (PF/avgR/robustness pass; cost-haircut + independent-window/forward-validation outstanding).
