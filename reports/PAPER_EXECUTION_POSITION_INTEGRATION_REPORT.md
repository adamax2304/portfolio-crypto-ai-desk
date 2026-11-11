# Paper Execution + Position Integration (PART 7)

**Date:** 2026-06-24. Wires sizing + fees into paper accounting. PAPER ONLY.

## Per-trade flow (`src/execution/paper_portfolio.py::simulate_portfolio`)
1. Read paper equity (compounding).
2. risk target = 0.5% of equity.
3. `size_position(entry, stop)` → qty, notional, dynamic leverage, margin, caps.
4. apply max leverage/margin/notional caps (risk-capped flag if stop < 0.5%).
5. `gross_pnl_usdt = paper_execution_r × actual_risk_usdt` (R × $-value-of-1R).
6. `trade_costs(notional)` → fees + slippage (+ funding hook).
7. `net = gross − costs`; **equity += net** (never touch_r).
8. write a ledger `exit` event with all USD/sizing/leverage fields.

## Live forward path
The same modules are importable by the tracker/close-alert path; the Telegram close alert now appends a **Paper $** line (net, risk $, leverage, fees) computed via `size_position`+`trade_costs` (fail-open). Forward paper signals can write ledger events the same way; historical backfill reconstructs the derived ledger.

## Guarantees
- Equity uses `paper_execution_r`-net-USD, NOT touch_r.
- No real orders, no production exit/TP/SL change, `signal_outcomes.final_r` untouched.

## Verdict
`PAPER_EXECUTION_NOW_HAS_USD_POSITION_ACCOUNTING`
