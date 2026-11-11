# Crypto Swing: Legacy Production and Versioned Shadow

Generated: 2026-07-12

## Active Production-Paper State

- Crypto swing production-paper uses the established native signal targets.
- `canonical_target_override_enabled=false`: future `proposed_signals` retain the analyst's original TP geometry.
- `main_paper_enforcement_enabled=false`: no T140-only or post-hoc latency floor can remove a native swing trade from the active paper book.
- `live_enabled=false`; no live-order path was added or enabled.
- Rebuilt active ledger, `bybit_non_vip_usdt_perp`: 240 crypto-swing exits, net `+$1,368.29`.

The active paper book is not populated from any shadow result. The existing crypto quality overlay continues to apply its normal `FULL_SIZE` / `HALF_SIZE` / shadow decisions to production-paper candidates.

## Shadow Experiments

Every row below is a paired simulation on the same 240 historical swing signals and stored separately in `crypto_swing_paper_counterfactual`.

| variant | entered | entered WR | simulated net $ | meaning |
|---|---:|---:|---:|---|
| `shadow_legacy_full_clean` | 29 | 44.8% | 14.73 | control: native targets with FULL_SIZE, clean audited data |
| `shadow_t140_full_clean` | 29 | 44.8% | 74.55 | target-only T140 experiment against the same control cohort |
| `shadow_t130_full_clean` | 29 | 44.8% | 59.56 | T130 on the same control cohort |
| `shadow_t140_allow_half_size` | 61 | 44.3% | 213.78 | T140 with clean FULL and HALF overlay decisions; HALF is 0.5x |
| `shadow_t140_no_overlay_clean` | 61 | 44.3% | 353.01 | T140 with clean data but overlay and cooldown ignored, full size |

`shadow_t140_no_overlay_clean` is now a genuine no-overlay scenario. It is not comparable one-for-one with `FULL_SIZE` control because it intentionally admits more trades. The exact target comparison is `legacy_full_clean` vs `t140_full_clean` vs `t130_full_clean`.

## Interpretation

T140 currently leads the matched historical control by `$59.82`; T130 leads it by `$44.83`. This is useful research evidence, but not a promotion decision: the matched cohort is only 29 entries and the sweep baseline still differs from the historical ledger by about `$521`. The schedule will continue to collect the variants without changing the active paper book.

## Verification

- Focused regression: `150 passed`.
- Python compilation: clean.
- Scheduler dry-run: clean; the long-horizon plan includes the versioned shadow sweep.
- The sweep persisted 1,200 additive counterfactual rows. No sweep result is read by paper actionability or live routing.
- The prior strict-T140 report is explicitly marked superseded.

## Scope

This change did not rewrite historical `proposed_signals`, `signal_outcomes`, or `final_r`. The normal background tracker can continue to append new outcomes while verification runs; neither the ledger rebuild nor the shadow sweep writes to those source tables.
