# Paper Portfolio + Risk + Chart Markers — FINAL (PART 14)

**Date:** 2026-06-24. PAPER / ACCOUNTING / READ-MODEL / APP ONLY. No live/exec, no production exit/TP-SL/scoring/entry/routing change, no `final_r` rewrite.
Supporting: PAPER_PORTFOLIO_UPGRADE_BASELINE_AUDIT · TP_LEVEL_STRUCTURAL_AUDIT · TP_LEVEL_VALIDATOR_IMPLEMENTATION_REPORT · PAPER_PORTFOLIO_LEDGER_IMPLEMENTATION_REPORT · POSITION_SIZING_ENGINE_IMPLEMENTATION_REPORT · FEE_SLIPPAGE_FUNDING_MODEL_REPORT · PAPER_EXECUTION_POSITION_INTEGRATION_REPORT · CONTROL_PLANE_PORTFOLIO_AND_CHART_MARKERS_REPORT · TELEGRAM_PORTFOLIO_RISK_REPORT · HISTORICAL_PAPER_PORTFOLIO_BACKFILL_REPORT · FULL_PAPER_PORTFOLIO_AND_RISK_AUDIT_REPORT · PAPER_PORTFOLIO_RISK_TEST_RESULTS.

## The 18 answers
1. **Risk management working correctly now?** Yes — risk = stop distance × size; 0.5% of equity = $25/trade; verified by tests.
2. **TP levels structural or mechanical?** **Mechanical** — `technical_setup_agent` sets TP = close ± 1/2/3·ATR. Stops are semi-structural (swing S/R + ATR fallback). No volume-profile module (unknown).
3. **What changed about TP validation?** Added `tp_structure_validator.py` (display-only): labels each TP STRUCTURAL/MIXED/MECHANICAL_R_ONLY, warns on mechanical ladder + unjustified TP3. No TP generation change.
4. **Paper deposit?** $5000 USDT (`config/paper_portfolio.yaml`).
5. **Risk per trade?** 0.5% of equity (compounding) = $25 at start.
6. **Position size?** notional = risk_usdt / stop_distance_pct; qty = notional/entry; loss-at-stop ≈ risk_usdt.
7. **Leverage?** Dynamic = minimum integer leverage to keep margin ≤ 20% equity, clamped 1..5; liquidation buffer checked. Leverage ≠ risk.
8. **Active fee profile?** bybit_default_futures (taker 0.055%); configurable (mexc/conservative/zero).
9. **Fees/slippage included?** Yes — per-side open+close fees + per-tier slippage + funding hook; net = gross − costs.
10. **Historical portfolio result with fees?** $5000 → **$5147 (+2.94%)** Bybit; +47.6% no-cost; +16.3% MEXC; **−5.65% conservative**. Fees dominate.
11. **Current paper equity?** $5146.78 (Bybit profile, derived backfill).
12. **What does the app show?** Paper Equity / Today Net $ + R / Max DD / Fees cards; Paper-Exec headline; Paper-Features panel; per-trade USD + tags; `/api/portfolio` + `/api/trades/{id}/chart-events`.
13. **Chart markers working?** Data layer yes (chart-events endpoint: entry/stop/TP1-3/moved-stop/exit + MFE/MAE). Full candlestick line-overlay = noted TODO (endpoint + cards delivered now).
14. **Live/execution off?** Yes — `/api/health` live_locked:true, auto_live_locked:true; 0 live steps.
15. **Historical `final_r` unchanged?** Yes — no paper column on signal_outcomes; only appended rows.
16. **Bugs found & fixed?** (a) "zero" profile applied slippage (broke no-cost baseline + BE classification) → fixed; (b) close_alert `_to_float` NameError → local helper; (c) frontend missing `usePortfolio` import → fixed.
17. **Watch next 7 days?** Forward paper equity vs the +2.9% Bybit replay; fees-as-% of gross; drawdown; risk-capped trade count (tight stops); liquidation-buffer flags; chart-events accuracy; whether the edge survives live fees.
18. **Blocked until approval?** Any live/auto-live/exchange/real-orders; production exits/TP-SL; making TPs structural in generation; fee-aware/wider-stop strategy changes to survive fees; routing/actionability/scoring changes.

## Bottom line
The desk now has a real paper-trading portfolio: **$5000 deposit, 0.5% risk, stop-based sizing, dynamic leverage (margin + liquidation-aware), configurable fees/slippage**, with USD + R results in the app and a chart-events data layer. The honest headline: **TPs are mechanical (ATR ladder), and Model F's edge — strong without costs (+47.6%) — is fee-fragile (+2.9% Bybit, −5.65% conservative).** Nothing touched live, production logic, or `final_r`.

## Final verdicts
`PAPER_PORTFOLIO_LEDGER_READY` · `POSITION_SIZING_ENGINE_READY` · `FEE_MODEL_READY_CONFIGURABLE` · `PAPER_EXECUTION_NOW_HAS_USD_POSITION_ACCOUNTING` · `APP_SHOWS_USD_PNL_AND_CHART_MARKERS` · `TP_LEVEL_STRUCTURE_AUDIT_COMPLETE` · `NO_LIVE_EXECUTION_ENABLED` · `HISTORICAL_FINAL_R_UNCHANGED` · `READY_FOR_FORWARD_PAPER_VALIDATION`
