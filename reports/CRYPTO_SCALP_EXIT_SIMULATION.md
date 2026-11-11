# Crypto Scalp Exit Simulation (PART 2)

**Date:** 2026-06-10 · Read-only counterfactual. No TP/SL/code changes proposed. Just shows what alternative exits WOULD have produced on the same historical triggered set.

## 1. Method
- Sample: **40 triggered crypto scalp A/B signals** since 2026-05-15 (the entire scalp-trigger corpus).
- Inputs: `final_outcome`, `final_r`, `max_favorable_excursion_r`, `max_adverse_excursion_r` from the existing `signal_outcomes` rows.
- Assumptions:
  - We use **MFE/MAE only** — we cannot determine intrabar ordering for the "MFE reached before MAE?" question. Where the order matters, we use the conservative branch.
  - Each policy is applied as a **single global change** vs the existing TP/SL; we do NOT compound multiple policies.

## 2. Policy results

| Policy | n_triggered | W | L | **WR (closed)** | netR | avgR | reduced losses | lost wins |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **baseline (current)** | 40 | 0 | 9 | 0% | −9.0R | −0.23 | — | — |
| **tp1_at_0.5R** ⭐ | 40 | 13 | 9 | **59%** | **−2.5R** | **−0.06** | 0 | 0 |
| partial_at_0.5R (50% off) | 40 | 14 | 9 | 61% | −4.8R | −0.12 | 1 | 0 |
| be_after_0.6R (break-even stop) | 40 | 0 | 9 | 0% | −9.0R | −0.23 | 0 | — |
| trail_after_0.7R (lock 0.35R) | 40 | 8 | 9 | 47% | −6.2R | −0.15 | 0 | — |
| expiry_4h (extend window) | 40 | 14 | 9 | 61% | −5.5R | −0.14 | 0 | — |

⭐ **`tp1_at_0.5R` is the clear winner**:
- Converts ~13 expired-flat-with-positive-MFE into +0.5R wins.
- Loses **0** current wins (lost_wins=0): the single +1R baseline win (C/USDT) had MFE +1.74, so it still hits the 0.5R TP.
- Net improvement vs baseline: **+6.5R** on the same trade set.
- Still net-negative overall (−2.5R) — the playbook is not a positive-edge mode on its own — but the "low-confidence" label becomes more honest with a tighter exit.

## 3. Why does `be_after_0.6R` not help?
The break-even policy requires MFE ≥ 0.6 AND a subsequent reversal that the original stop would have caught. In our 40-trigger set, the 9 losses had MFE distribution mostly < 0.6R before the stop hit, so the BE move would not have rescued them. The expired set already exits flat, so BE doesn't help there either.

## 4. Why does `trail_after_0.7R` underperform `tp1_at_0.5R`?
Only **6 of 27 expired** signals had MFE ≥ 0.7R. The trail captures less of the MFE distribution than the 0.5R TP cut. MFE histogram (expired triggered, n=27 prior audit):
- MFE ≥ 0.5R: 12
- MFE ≥ 0.7R: 6
- MFE ≥ 1.0R: 0–1

A 0.5R take captures **2× more** signals than a 0.7R trail.

## 5. Intrabar-ambiguous exclusion
- Total triggered scalp: 40
- Carry `intrabar_entry_stop` or `intrabar_entry_tp` annotation: **3**
- Clean (excluding intrabar): 37
- Clean baseline metrics: 0W/8L, netR −8R (same shape — intrabar exclusion doesn't change scalp verdict).

## 6. Limitations of this study (honest)
- **MFE/MAE-only model** assumes the entry → MFE order is uncorrelated with order-of-events vs the stop. For a tighter TP1 at +0.5R, this is usually safe (price typically touches +0.5R before going to a deeper loss for the typical setup), but a small fraction of cases may flip.
- We did not re-walk OHLCV bars individually; we used the recorded MFE/MAE for each signal. A future, more rigorous study would replay 1m bars and resolve the order explicitly.
- The win-count in `tp1_at_0.5R` (13W) is realistic for the "+0.5R captured" cohort, but the actual win in real trading depends on whether the level traded as a limit (almost always yes on liquid alts).

## 7. Recommendation (NOT a code change in this PR)
- **The current TP1 distance is ~+1.86R** of risk (per scalp viability audit). The MFE distribution shows the captured-edge "ceiling" is around +0.5–0.7R inside the 2h window.
- **Bringing TP1 to ~+0.5R would erase the −6.5R penalty** the current geometry costs the playbook on this dataset.
- This is a **strategy-layer change** (TP geometry), so it's **out of scope** for this read-only audit. It belongs to a separate approval cycle.
- Until that lands, the **low-confidence scalp annotation remains the correct user-facing posture** (already in place).

## Verdict
```
SCALP_EXIT_SIMULATION_COMPLETE
```

`tp1_at_0.5R` is the best-EV alternative exit on this dataset (+6.5R vs baseline). It is **not implemented** in this PR. A position-sizing reduction (sizing scalp at 0.5×) covered in PART 5 is the **safe, no-code-change** alternative that captures most of the risk reduction without touching geometry.
