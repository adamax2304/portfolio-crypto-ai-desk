# PAPER EXECUTION — STRUCTURAL TP + MAKER-FIRST INTEGRATION (PART 5)

**Scope:** PAPER ONLY. Derived ledger; `signal_outcomes.final_r` untouched.
Date: 2026-06-24.

## Integrated paper flow (per trade)
1. Mechanical TP-set from signal (production, unchanged) → kept as `mechanical_tp*`.
2. **Structural TP-set** via `generate_structural_tps` (forward: swing/range/VP;
   historical: ATR-fallback labelled).
3. Choose paper TP-set: structural if valid → HYBRID if TP3 unjustified → ATR fallback
   if no structure → NO_VALID_TP otherwise.
4. **Fee-aware check** (`assess_fees`): EXTREME_FEE_DRAG / TIGHT_STOP → skip the trade
   from the paper book; otherwise warn/cap.
5. **Safe 2x sizing** (`size_position`, max 2x, 40% margin, 80% notional).
6. **Maker-first plan** (`plan_for`): maker entry for pullback, taker for momentum,
   maker TP exits (conservative fill), stop always taker.
7. Compute paper PnL: Model-F R base × actual risk − costs (entry fee on entry
   notional, **close fee on exit notional**, maker/taker per side, slippage).
8. Equity compounding; persisted to `paper_portfolio_ledger`.

## Storage / comparison
- `scripts/structural_maker_backfill.py` builds the **B book** and persists it under
  fee_profile **`bybit_structural_maker_first`** (kept across A-rebuilds — the
  `paper_portfolio_backfill` drop-list now preserves it).
- Each ledger row's `close_reason` carries `…|<entry>E/<exit>X|<TP_SET_LABEL>` so the
  app reconstructs the per-trade execution model.
- Two comparable books coexist: `portfolio_result_mechanical_taker`
  (=`bybit_non_vip_usdt_perp`) and `portfolio_result_structural_maker_first`
  (=`bybit_structural_maker_first`).

## Result (Bybit, $5000, 0.5% risk, 587 trades)
| book | final $ | return | fees | maxDD |
|---|---|---|---|---|
| A · mechanical + taker | 5185.91 | +3.72% | 1763 | 18.3% |
| **B · structural + maker-first + fee-aware + 2x** | **5409.39** | **+8.19%** | **1585** | 17.1% |

**Δ +4.47pp · fees −$177.7 · 177 maker entries · 299 maker exits · 0 fee-drag skips.**

## Verdict
**PAPER_EXECUTION_USES_STRUCTURAL_TP_AND_MAKER_FIRST**
