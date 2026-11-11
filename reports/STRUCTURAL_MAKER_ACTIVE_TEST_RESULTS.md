# STRUCTURAL + MAKER-FIRST — TEST RESULTS (PART 9)

**Date:** 2026-06-24. PAPER ONLY.

## crypto-ai-desk — `tests/` (targeted, 44 passed)
- `tests/test_paper_portfolio.py` (14) — **leverage**: max 2x enforced, leverage ≠
  risk, position capped when 0.5% can't fit, `too_tight_stop`/`too_wide_stop`,
  liquidation buffer; plus exit-notional fee, exit/expiry, alias.
- `tests/test_structural_maker.py` (17) — **structural TP**: swing/SR level selected,
  no fake VP (supported=false without volume), TP3 disabled in chop, TP3 allowed for
  runner, fallback labelled, TP1 ≥ 0.6R. **Fee-aware**: fee_r_cost, high/extreme drag
  skip, FEE_SURVIVAL_FAIL, maker rate < taker rate. **Maker-first**: maker entry for
  pullback / taker for momentum, stop always taker, maker-entry-missed → taker
  fallback, maker-TP fill only if rested (no free maker fills).
- `tests/test_tp_structure_validator.py`, `tests/test_paper_execution_accounting.py` —
  unchanged, pass.

```
44 passed in 0.36s
```

## trading-desk-control — `backend/tests/test_portfolio.py` (6 passed)
- summary shape + safety locks; trades/chart-events shapes; exact-R + exit marker;
  **`portfolio_compare`** (A vs B, live-locked, production_tp_unchanged,
  leverage_policy=max_2x_safe, B max_leverage ≤ 2, maker counts, fees_saved);
  **B book max_leverage ≤ 2**; **chart_events.paper_execution_b** (stop=taker, entry
  ∈ maker/taker, tp_set_label valid).

```
6 passed in 0.17s
```

## Frontend
`npm run build` (tsc -b && vite build): **exit 0**, 92 modules, no type errors.

## Safety assertions (in-test + audit)
- No `signal_outcomes.final_r` rewrite (no paper column; final_r intact).
- No live/exec: `/api/health` → `live_locked:true, auto_live_locked:true`.
- No production TP generation change (mechanical ATR ladder untouched).
- No routing/scoring/actionability change.
- B and A ledgers stored under separate fee_profiles — no double-counting.

## Verdict
**STRUCTURAL_MAKER_ACTIVE_TESTS_PASS**
