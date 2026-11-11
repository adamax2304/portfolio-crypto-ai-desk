# TP-Level Validator — Implementation Report (PART 3)

**Date:** 2026-06-24. Module: `src/execution/tp_structure_validator.py`. **DISPLAY-ONLY** — does not change TP generation, routing, or execution.

## Inputs
entry, stop, tp1/2/3, direction, atr, swing_levels (swing H/L + support/resistance + range bounds), volume_profile_levels (if available), market_regime, playbook.

## Rules
1. A TP near a structural level (swing/SR within 0.4%, volume-profile node, or psychological round number) → structural.
2. Else if TP ≈ entry ± k·ATR (k≈1/2/3) → `atr_extension` (weak-structural).
3. Else → `mechanical_r_ladder`.
4. **TP3 requires stronger justification:** near structure, OR a trend-runner playbook (crypto_swing_narrative / failed_bounce_short / intraday_catalyst) and NOT chop/transition; otherwise `tp3_warning`.

## Outputs
`tp_quality_score` (0-100), `tp_quality_label` (STRUCTURAL | MIXED | MECHANICAL_R_ONLY | UNKNOWN), `tp1/2/3_source`, `tp_is_mechanical_r_ladder`, `tp_near_chart_level`, `nearest_structure_distance_pct`, `volume_profile_supported` (yes|unknown), `tp_reasons`, `tp_warnings`, `tp3_allowed_reason`, `tp3_warning`.

## Behavior on current production TPs
Since production TPs are an ATR ladder with no structural placement, the validator labels them **MECHANICAL_R_ONLY** (or MIXED when a TP coincidentally lands near a level) and emits the mechanical-ladder warning + (in chop/non-runner) a TP3 warning. No trade is blocked.

Tests: `tests/test_tp_structure_validator.py` (4 — mechanical flagged, structural accepted, TP3 chop-warning, TP3 runner allowed).

## Verdict
`TP_LEVEL_VALIDATOR_READY_DISPLAY_ONLY`
