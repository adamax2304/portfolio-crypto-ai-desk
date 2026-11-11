# Superseded: Crypto Swing Strict Paper Policy

> Historical record only. On 2026-07-12 the production-paper book was returned to the legacy/native swing geometry. T140/T130 and overlay variations now run exclusively as versioned shadow counterfactuals. See `CRYPTO_SWING_VERSIONED_PAPER_SHADOW_REPORT.md` and `CRYPTO_SWING_ENTRY_SWEEP.md` for the active design.

Generated: 2026-07-12

## What Changed

- Main production-paper lane for crypto swing is now strict:
  - overlay action must be `FULL_SIZE`;
  - entry-latency audit must be clean (`data_gap_min <= 60`, no `DATA_GAP_LATE`, no `LEGITIMATE_LATE`, no `NO_DATA`);
  - signal TP geometry must already match `1.40 / 2.40 / 3.80 ATR`;
  - `HALF_SIZE`, `SHADOW_ONLY`, `BLOCK`, `NO_OVERLAY`, dirty latency, and old-target rows are excluded from the main paper ledger.
- New crypto swing signals are created with the production paper target ladder `1.40 / 2.40 / 3.80 ATR`.
- Old crypto swing rows were not rewritten. Their original TP hit flags were produced under the old target ladder, so treating them as if they had used 1.40/2.40/3.80 would be invalid.
- Historical what-if is now handled by the additive read-model table `crypto_swing_paper_counterfactual`.

## Shadow / Counterfactual Lanes

The scheduled sweep now persists these variants:

- `production_t140_full_clean`
- `shadow_t130_full_clean`
- `shadow_t140_allow_half_size`
- `shadow_t140_allow_no_overlay`

Latest persisted sweep:

| variant | rows | entered | net $ | entered WR |
|---|---:|---:|---:|---:|
| `production_t140_full_clean` | 240 | 29 | 74.55 | 44.8% |
| `shadow_t130_full_clean` | 240 | 29 | 59.56 | 44.8% |
| `shadow_t140_allow_half_size` | 240 | 61 | 213.78 | 44.3% |
| `shadow_t140_allow_no_overlay` | 240 | 29 | 74.55 | 44.8% |

Interpretation: `allow_half_size` looks larger historically, but stays shadow because the main objective was higher-quality production-paper evidence, not simply more historical PnL. It needs forward confirmation before promotion.

## Current Production-Paper State

- Active paper ledger after rebuild: `bybit_non_vip_usdt_perp` net `+717.69 USDT`, final equity `5717.69`.
- Crypto swing rows in active production-paper ledger: `0`.
- This is intentional: old crypto swing rows do not have the new target profile in their actual stored signal geometry. New crypto swing signals will qualify only if they are `FULL_SIZE + clean + T140`.

## Guardrails

- `proposed_signals`: unchanged at `3563`.
- `signal_outcomes`: unchanged at `1015476`.
- `SUM(signal_outcomes.final_r)`: unchanged at `1228806.0`.
- Live remains untouched.
- No historical `final_r` or source outcome rows were rewritten.

## Verification

- `py_compile` on changed modules: OK.
- Focused regression: `147 passed`.
- Scheduler dry-run: OK.
- Long-horizon plan contains:
  - `paper portfolio ledger refresh`
  - `crypto quality overlay report (counterfactual)`
  - `crypto swing strict policy sweep (counterfactual)`

## Changed Files

- `config/crypto_swing_paper_policy.yaml`
- `src/execution/crypto_swing_paper_policy.py`
- `src/execution/paper_actionability.py`
- `src/notifiers/paper_entry.py`
- `src/signals/registry.py`
- `scripts/paper_portfolio_backfill.py`
- `scripts/crypto_swing_entry_sweep.py`
- `scripts/run_default_market_schedule.py`
- `tests/test_crypto_swing_paper_policy.py`
- `tests/test_paper_entry_alerts.py`
- `tests/test_scalp_downgrade.py`
