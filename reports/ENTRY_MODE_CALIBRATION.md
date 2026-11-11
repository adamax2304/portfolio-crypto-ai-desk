# Entry-Mode Calibration (paper / read-model)

- generated_at: `2026-09-07T22:33:22.356788+00:00`  · activated_at: `2026-06-25T01:35:11.228365+00:00`
- risk/trade: `$25`  · USD PnL is authoritative; R auxiliary
- **Decisions are made ONLY on forward_since_activation. Historical backfill is hypothesis-only.**
- **Source tables READ-ONLY** (paper_shadow_execution_outcomes, paper_execution_outcomes, proposed_signals, signal_entry_mode, entry_latency_audit). **Read-model writes ONLY** to entry_mode_calibration_slices / entry_mode_calibration_paired + JSON/CSV.
- Live / auto-live / manual-live locked; NO writes to proposed_signals / signal_outcomes / final_r.
- paired delta is **executed_vs_executed** (both branches filled) for verdicts; **with_skips_or_avoided** is context only (avoided-bad / missed-good).

## Headline — ELIGIBLE forward evidence (new_logic_shadow)

- eligible forward slices: **3**  · DISABLE: 1  WATCH: 2
- eligible forward net USD: **$1,091**  (EXCLUDES policy-disabled [9] + legacy stocks swing/invest [7] + NO_CHASE_SKIP [3] + data-quality/insufficient-clean [2])
- **Edge metrics (net USD / PF / winrate) are CLEAN-cohort only — DATA_GAP_LATE trades are NEVER counted as edge (shown as dirty diagnostics).**
- **Legacy stocks swing/invest evidence is NOT valid for the new stocks_position_framework (stocks_swing_growth_breakout / earnings_drift / stage2_position) — evaluated separately.**

## Eligible forward evidence — by asset / mode / entry_mode (new_logic_shadow)

| asset | mode | entry_mode | trades | filled | closed | net USD | PF | maxDD $ | maxDD R | DGL% | exec Δ$ | w/skips Δ$ | verdict | reason |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|---|
| crypto | swing | MOMENTUM_TAKER_NOW | 48 | 48 | 48 | -250 | 0.62 | 254 | 10.2 | 0 | 337 | 244 | DISABLE | net_usd=-250, PF=0.62 below disable gate |
| crypto | intraday | BREAKOUT_CONTINUATION | 118 | 34 | 34 | 88 | 1.24 | 156 | 6.2 | 1 | -234 | -254 | WATCH | PF=1.24 positive but below candidate gate |
| crypto | swing | BREAKOUT_CONTINUATION | 132 | 82 | 82 | 1253 | 2.48 | 269 | 10.7 | 2 | 651 | 2934 | WATCH | PF=2.48 positive but below candidate gate |

## Historical backfill (HYPOTHESIS-ONLY — not for promotion)

| asset | mode | entry_mode | trades | filled | closed | net USD | PF | maxDD $ | maxDD R | DGL% | exec Δ$ | w/skips Δ$ | verdict | reason |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|---|
| crypto | intraday | BREAKOUT_CONTINUATION | 12 | 0 | 0 | 0 | - | 0 | 0.0 | 92 | -0 | 26 | KEEP_SHADOW | backfill/hypothesis-only — not eligible for promotion verdic |
| crypto | intraday | MOMENTUM_TAKER_NOW | 1 | 0 | 0 | 0 | - | 0 | 0.0 | 100 | 0 | 0 | KEEP_SHADOW | backfill/hypothesis-only — not eligible for promotion verdic |
| crypto | swing | BREAKOUT_CONTINUATION | 33 | 3 | 3 | 81 | 4.14 | 26 | 1.0 | 91 | 324 | 903 | KEEP_SHADOW | backfill/hypothesis-only — not eligible for promotion verdic |

## Data-quality / insufficient-clean-sample diagnostics (DATA_QUALITY_BLOCKED / INSUFFICIENT_CLEAN_SAMPLE — promotion blocked, NOT evidence)

| asset | mode | entry_mode | trades | filled | closed | net USD | PF | maxDD $ | maxDD R | DGL% | exec Δ$ | w/skips Δ$ | verdict | reason |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|---|
| crypto | swing | STRUCTURAL_RETEST | 1 | 1 | 1 | -26 | 0.00 | 26 | 1.0 | 0 | -1 | -1 | INSUFFICIENT_CLEAN_SAMPLE | clean closed=1 < 30 (dirty DGL excluded: 0) |
| crypto | intraday | MOMENTUM_TAKER_NOW | 16 | 5 | 5 | 66 | 2.21 | 27 | 1.1 | 0 | 98 | 98 | INSUFFICIENT_CLEAN_SAMPLE | clean closed=5 < 30 (dirty DGL excluded: 0) |

## Policy-disabled diagnostics (DISABLED_BY_POLICY — not eligible, not ranked)

| asset | mode | entry_mode | trades | filled | closed | net USD | PF | maxDD $ | maxDD R | DGL% | exec Δ$ | w/skips Δ$ | verdict | reason |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|---|
| crypto | intraday | LIMIT_THEN_TAKER_TIMEOUT | 80 | 0 | 0 | 0 | - | 0 | 0.0 | 0 | 0 | -55 | DISABLED_BY_POLICY | crypto_entry_mode_disabled_by_policy |
| crypto | intraday | PULLBACK_LIMIT | 211 | 0 | 0 | 0 | - | 0 | 0.0 | 0 | 0 | 178 | DISABLED_BY_POLICY | crypto_entry_mode_disabled_by_policy |
| crypto | scalp | BREAKOUT_CONTINUATION | 69 | 0 | 0 | 0 | - | 0 | 0.0 | 0 | 0 | 29 | DISABLED_BY_POLICY | crypto_scalp_disabled_by_policy |
| crypto | scalp | LIMIT_THEN_TAKER_TIMEOUT | 11 | 0 | 0 | 0 | - | 0 | 0.0 | 0 | 0 | -120 | DISABLED_BY_POLICY | crypto_scalp_disabled_by_policy |
| crypto | scalp | MOMENTUM_TAKER_NOW | 8 | 0 | 0 | 0 | - | 0 | 0.0 | 0 | 0 | -69 | DISABLED_BY_POLICY | crypto_scalp_disabled_by_policy |
| crypto | scalp | PULLBACK_LIMIT | 174 | 0 | 0 | 0 | - | 0 | 0.0 | 0 | 0 | -220 | DISABLED_BY_POLICY | crypto_scalp_disabled_by_policy |
| crypto | scalp | STRUCTURAL_RETEST | 1 | 0 | 0 | 0 | - | 0 | 0.0 | 0 | 0 | 0 | DISABLED_BY_POLICY | crypto_scalp_disabled_by_policy |
| crypto | swing | LIMIT_THEN_TAKER_TIMEOUT | 108 | 0 | 0 | 0 | - | 0 | 0.0 | 3 | 0 | 1609 | DISABLED_BY_POLICY | crypto_entry_mode_disabled_by_policy |
| crypto | swing | PULLBACK_LIMIT | 206 | 0 | 0 | 0 | - | 0 | 0.0 | 3 | 0 | 1545 | DISABLED_BY_POLICY | crypto_entry_mode_disabled_by_policy |

## APPENDIX — legacy stocks swing/invest (UNSUPPORTED_LEGACY, not promotable)

| asset | mode | entry_mode | trades | filled | closed | net USD | PF | maxDD $ | maxDD R | DGL% | exec Δ$ | w/skips Δ$ | verdict | reason |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|---|
| stocks | swing | LIMIT_THEN_TAKER_TIMEOUT | 22 | 13 | 13 | 23 | 1.18 | 88 | 3.5 | 0 | - | - | UNSUPPORTED_LEGACY | retired stocks swing/invest framework — legacy, not promotab |
| stocks | invest | BREAKOUT_CONTINUATION | 32 | 22 | 22 | 29 | 1.34 | 39 | 1.6 | 0 | - | - | UNSUPPORTED_LEGACY | retired stocks swing/invest framework — legacy, not promotab |
| stocks | invest | PULLBACK_LIMIT | 2 | 2 | 2 | 36 | inf | 0 | 0.0 | 0 | - | - | UNSUPPORTED_LEGACY | retired stocks swing/invest framework — legacy, not promotab |
| stocks | swing | BREAKOUT_CONTINUATION | 28 | 12 | 12 | 90 | 2.17 | 26 | 1.0 | 0 | - | - | UNSUPPORTED_LEGACY | retired stocks swing/invest framework — legacy, not promotab |
| stocks | swing | MOMENTUM_TAKER_NOW | 7 | 5 | 5 | 97 | inf | 0 | 0.0 | 0 | - | - | UNSUPPORTED_LEGACY | retired stocks swing/invest framework — legacy, not promotab |
| stocks | swing | PULLBACK_LIMIT | 16 | 11 | 11 | 206 | 9.02 | 26 | 1.0 | 0 | - | - | UNSUPPORTED_LEGACY | retired stocks swing/invest framework — legacy, not promotab |
| stocks | invest | LIMIT_THEN_TAKER_TIMEOUT | 28 | 20 | 20 | 260 | 17.30 | 6 | 0.2 | 0 | - | - | UNSUPPORTED_LEGACY | retired stocks swing/invest framework — legacy, not promotab |

## Skip-policy diagnostics (NO_CHASE_SKIP — not an economic entry mode)

| asset | mode | entry_mode | trades | skipped | verdict |
|---|---|---|--:|--:|---|
| crypto | intraday | NO_CHASE_SKIP | 4 | 4 | SKIP_POLICY |
| crypto | scalp | NO_CHASE_SKIP | 9 | 9 | SKIP_POLICY |
| crypto | swing | NO_CHASE_SKIP | 1 | 1 | SKIP_POLICY |

## Paired old_paper vs new_logic_shadow (forward — ELIGIBLE modes)

_executed_vs_executed (both branches filled) — drives verdicts:_

| asset | mode | entry_mode | exec common | new✓ | old✓ | flat | exec sum Δ$ | exec avg Δ$ | exec sum ΔR |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|
| crypto | intraday | BREAKOUT_CONTINUATION | 33 | 11 | 22 | 0 | -234 | -7.09 | -9.36 |
| crypto | swing | STRUCTURAL_RETEST | 1 | 0 | 1 | 0 | -1 | -0.86 | -0.03 |
| crypto | intraday | MOMENTUM_TAKER_NOW | 5 | 2 | 3 | 0 | 98 | 19.65 | 3.93 |
| crypto | swing | MOMENTUM_TAKER_NOW | 43 | 23 | 20 | 0 | 337 | 7.84 | 13.48 |
| crypto | swing | BREAKOUT_CONTINUATION | 67 | 24 | 43 | 0 | 651 | 9.72 | 26.05 |

_with_skips_or_avoided (skips = 0 PnL) — CONTEXT ONLY, not verdict-driving:_

| asset | mode | entry_mode | w/skips common | w/skips sum Δ$ | avoided bad (n / $) | missed good (n / $) |
|---|---|---|--:|--:|--:|--:|
| crypto | intraday | BREAKOUT_CONTINUATION | 118 | -254 | 4 / 114 | 2 / 154 |
| crypto | swing | STRUCTURAL_RETEST | 1 | -1 | 0 / 0 | 0 / 0 |
| crypto | intraday | MOMENTUM_TAKER_NOW | 16 | 98 | 0 / 0 | 0 / 0 |
| crypto | swing | MOMENTUM_TAKER_NOW | 48 | 244 | 0 / 0 | 0 / 0 |
| crypto | swing | BREAKOUT_CONTINUATION | 132 | 2934 | 49 / 1312 | 0 / 0 |

## Profit-protection metrics (authoritative Model F book, by entry_mode slice)

_Protection is the authoritative Model-F paper book, aggregated over EACH slice's own signal_ids (never mixing forward/backfill). Δ vs legacy-touch = paper_execution_r − touch_r (touch_r is the legacy highest-TP baseline). `aux` = auxiliary_non_comparable (coverage < 50%)._

_`evidence` gates whether these numbers may be cited as proof of edge: FORWARD_VALIDATED (≥30 resolved forward_postfreeze trades) is the only status usable as evidence. INSUFFICIENT_FORWARD_SAMPLE and NO_FORWARD_EVIDENCE mean the numbers above are backfill_pretrained (in-sample replay that chose Model F's own thresholds) — hypothesis/context only, NEVER "profitable" evidence._

| asset | mode | entry_mode | model | cov% | aux | armed% | lock% | BE-exit% | lock-exit% | giveback% | TP3run% | avg prot R | Δ vs legacy-touch $ | evidence |
|---|---|---|---|--:|:-:|--:|--:|--:|--:|--:|--:|--:|--:|:-:|
| crypto | intraday | BREAKOUT_CONTINUATION | early_mfe_protection_v1 | 100 | n | 65 | 50 | 12 | 18 | 29 | 29 | 1.17 | -1 | FORWARD_VALIDATED |
| crypto | swing | BREAKOUT_CONTINUATION | early_mfe_protection_v1 | 85 | n | 40 | 29 | 10 | 14 | 24 | 13 | 0.70 | -6 | FORWARD_VALIDATED |
| crypto | swing | MOMENTUM_TAKER_NOW | early_mfe_protection_v1 | 92 | n | 55 | 39 | 14 | 18 | 32 | 16 | 0.67 | -3 | FORWARD_VALIDATED |

### Evidence-class breakdown (forward_postfreeze vs backfill_pretrained vs unclassified)

| asset | mode | entry_mode | forward_postfreeze n/resolved/netR | backfill_pretrained n/resolved/netR | unclassified n |
|---|---|---|--:|--:|--:|
| crypto | intraday | BREAKOUT_CONTINUATION | 34/34/39.62 | 0/0/- | 0 |
| crypto | swing | BREAKOUT_CONTINUATION | 70/70/49.01 | 0/0/- | 0 |
| crypto | swing | MOMENTUM_TAKER_NOW | 44/44/29.64 | 0/0/- | 0 |

## Policy (paper_entry_mode_policy.yaml) reflected against slices

- integrity_ok (no disabled mode in promoted paper): **True**
- disabled slices: 18 (forward trades actually affected: 877)
- promoted-to-paper slices: 0 (forward trades: 0)

## Recommendations

### Promising — PROMOTE_REVIEW / PAPER_CANDIDATE  (0)

### Watch — WATCH / KEEP_SHADOW  (2)
- `crypto/swing/BREAKOUT_CONTINUATION` — WATCH (closed=82, PF=2.48, net=$1253, exec Δ=$651) PF=2.48 positive but below candidate gate
- `crypto/intraday/BREAKOUT_CONTINUATION` — WATCH (closed=34, PF=1.24, net=$88, exec Δ=$-234) PF=1.24 positive but below candidate gate

### Disable — DISABLE  (1)
- `crypto/swing/MOMENTUM_TAKER_NOW` — DISABLE (closed=48, PF=0.62, net=$-250, exec Δ=$337) net_usd=-250, PF=0.62 below disable gate

### Blocked — DATA_QUALITY_BLOCKED / DISABLED_BY_POLICY  (0)

### Insufficient data — NEED_MORE_DATA  (0)
