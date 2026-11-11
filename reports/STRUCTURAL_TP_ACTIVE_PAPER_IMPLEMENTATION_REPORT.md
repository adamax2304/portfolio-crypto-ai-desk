# STRUCTURAL TP GENERATOR — ACTIVE FOR PAPER (PART 2)

**Scope:** PAPER ONLY. Production TP generation (mechanical ATR ladder in
`technical_setup_agent.py`) is UNCHANGED. Date: 2026-06-24.

## New modules
- `src/analysis/market_structure_levels.py` — swing highs/lows (fractal pivots),
  range high/low, round numbers. Pure, takes candle dicts/tuples.
- `src/analysis/volume_profile.py` — POC / HVN / LVN histogram. **Returns
  `supported=False` and NO levels when volume is missing or candles < 40** — never
  invents VP levels.
- `src/execution/structural_tp_engine.py` — `generate_structural_tps(...)` →
  `StructuralTP` dataclass with `paper_structural_tp1/2/3`, exact R per TP, per-TP
  source, confidence (0–100), `volume_profile_supported`, reasons, warnings.

## Level priority
swing H/L → range bound → volume-profile POC/HVN (only if supported) → round numbers
(only when chart candles are present) → ATR extension (fallback only).

## Rules enforced
- **TP1** = nearest high-quality level in the profit direction, **≥ 0.60R after fees**
  (`min_tp1_r_after_fees`). Candidates beyond `max_tp_r` (15R) are discarded.
- **TP2** = next stronger structural level, or ATR-2x → label becomes `HYBRID`.
- **TP3** only for trend-runner / failed-bounce / catalyst-continuation playbooks
  (`tp3_requires_runner`); **disabled in chop/range regimes**.
- No valid level → **STRUCTURAL_FALLBACK_ATR**; if even ATR isn't viable after fees →
  **NO_VALID_TP**.
- Round numbers are gated on having chart context (too coarse to be primary structure
  standalone), so a candle-less call degrades cleanly to ATR-fallback.

## Config
`config/paper_execution_policy.yaml → paper_structural_tp`:
`enabled: true · apply_to_paper: true · production_unchanged: true ·
min_tp1_r_after_fees: 0.60 · tp3_requires_runner: true · volume_profile_enabled: true
· fallback_to_atr: true`.

## Storage
Structural choice is attached to the derived paper ledger (`close_reason` carries the
`TP_SET_LABEL`; backend exposes it as `paper_execution_b.tp_set_label`). **Never
written to `signal_outcomes`.**

## Forward vs historical
- **Forward paper trades** (live OHLCV at signal time) get the full swing/range/VP
  structural set.
- The **historical backfill has no per-trade OHLCV slice**, so it labels structural
  TPs as `STRUCTURAL_FALLBACK_ATR` (honest — no fake swing/VP). The economic A/B win
  in the backfill is therefore carried by maker-first + fee-aware + 2x, with structural
  TP active for the live path.

## Tests
`tests/test_structural_maker.py`: swing detection, no-fake-VP, TP3 disabled in chop,
TP3 allowed for runner, fallback labelled, TP1 ≥ 0.6R. All pass.

## Verdict
**STRUCTURAL_TP_ACTIVE_FOR_PAPER_ONLY**
