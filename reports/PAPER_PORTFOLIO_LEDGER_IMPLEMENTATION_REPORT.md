# Paper Portfolio Ledger — Implementation Report (PART 4)

**Date:** 2026-06-24. PAPER / ACCOUNTING ONLY. No real orders; never mutates `signal_outcomes`.

## Config — `config/paper_portfolio.yaml`
initial_equity_usdt **5000**, risk_per_trade_pct **0.005** (0.5% = $25 on $5000), risk_basis **equity** (compounding), max_margin_per_trade_pct 0.20, max_notional_per_trade_pct 1.50, max_leverage 5, liquidation_buffer_to_stop 1.5, fee_profile bybit_default_futures, per-tier slippage defaults, majors list.

## Table — `paper_portfolio_ledger` (`src/execution/paper_portfolio.py::ensure_tables`)
Fields: id, signal_id, economic_trade_key, timestamp, event_type (entry|protection_armed|lock_armed|stop_moved|tp_hit|exit|fee|funding|equity_snapshot), equity_before, equity_after, realized_pnl_usdt, unrealized_pnl_usdt, gross_pnl_usdt, fees_usdt, slippage_usdt, funding_usdt, net_pnl_usdt, risk_usdt, risk_pct, position_notional_usdt, margin_used_usdt, leverage_used, qty, entry_price, exit_price, stop_initial, stop_current, paper_execution_r, close_reason, risk_model, fee_profile, created_at. `UNIQUE(economic_trade_key, event_type, fee_profile)` → idempotent.

## Read-model / positions
`simulate_portfolio(trades, cfg, fee_profile)` produces equity_curve + ledger + summary (final equity, net/gross, fees, return%, maxDD, W/L/BE). Open/closed positions are exposed via the backend `/api/portfolio` + `/api/portfolio/trades` read-model.

## Behavior
- Historical backfill reconstructs a derived ledger (PART 10).
- `replace_ledger` clears + re-inserts per fee_profile → idempotent, no double-count.
- Equity uses **net USD** = `paper_execution_r × actual_risk_usdt − costs`; never touch_r.
- Persisted: 586 exit rows (bybit profile) in `paper_portfolio_ledger`.

## Verdict
`PAPER_PORTFOLIO_LEDGER_READY`
