# TP-Level Structural Audit (PART 2)

**Date:** 2026-06-24. Read-only. Where TPs come from + are they structural.

## How TPs are generated
`src/agents/technical_setup_agent.py` (lines 64-66 long / 95-97 short):
```
tp1 = close + 1.0*atr   (short: close - 1.0*atr)
tp2 = close + 2.0*atr
tp3 = close + 3.0*atr
```
TPs are a **pure mechanical ATR ladder** (close ± 1/2/3·ATR). They are NOT placed at swing highs/lows, support/resistance, liquidity pools, volume-profile nodes, VWAP bands, prior-day H/L, range bounds, order blocks/FVG, or fib levels.

## The stop IS partially structural (contrast)
`invalidation` = support/resistance ± 0.15·ATR **if within 1.8·ATR**, else the ATR fallback (close ∓ 1.2·ATR). So stops use swing S/R when available — TPs do not.

## Derived per-signal fields (validator, PART 3)
`tp1_source / tp2_source / tp3_source` (swing_or_sr | volume_profile | round_number | atr_extension_kx | mechanical_r_ladder), `tp_structure_confidence` (tp_quality_score 0-100), `tp_is_mechanical_r_ladder`, `tp_distance_r`, `tp_near_chart_level`, `nearest_structure_distance_pct`, `volume_profile_supported` (**unknown** — no VP module), `tp_quality_label` (STRUCTURAL | MIXED | MECHANICAL_R_ONLY | UNKNOWN).

## Answers
- **Are TP levels chart-based?** No — they are an ATR ladder off `close`.
- **Are they just +R levels?** Effectively yes (ATR multiples ≈ fixed R given the stop geometry).
- **Which agents/playbooks produce structural TP?** None — all playbooks inherit the same ATR-ladder TPs from `technical_setup_agent`. (The validator can still *recognize* structure when a TP happens to land near a swing/round level.)
- **Which produce mechanical TP?** All.
- **Is TP3 structurally justified?** No — 3·ATR is the furthest mechanical extension with no structural basis; it only "earns" in trend-runner cohorts (crypto swing / failed-bounce-short / catalyst), per the earlier TP audit.

## Volume profile
No volume-profile module exists. `volume_profile_supported=unknown` (never fabricated). **Proposal:** a future `src/analysis/volume_profile.py` (HVN/LVN/POC from the OHLCV+volume archive) would let the validator place/justify TPs at real nodes. Default-off until built.

## Verdict
`TP_LEVEL_STRUCTURE_AUDIT_COMPLETE` — TPs are MECHANICAL (ATR ladder); stops semi-structural; volume-profile unknown.
