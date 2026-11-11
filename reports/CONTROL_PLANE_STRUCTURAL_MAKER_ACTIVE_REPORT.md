# CONTROL PLANE — STRUCTURAL + MAKER-FIRST ACTIVE (PART 6)

**Scope:** trading-desk-control read-model + UI. Read-only; live locked.
Date: 2026-06-24.

## Backend (`backend/app/portfolio.py` + `main.py`)
- New constant `STRUCTURAL_MAKER_PROFILE = "bybit_structural_maker_first"`.
- **`portfolio_compare()`** → `GET /api/portfolio/compare`: A (mechanical taker) vs
  B (structural + maker-first + fee-aware + 2x):
  - per-side equity / return% / fees / maxDD / avg+max leverage,
  - `delta_return_pct`, `fees_saved_usdt`,
  - `maker_entries`, `taker_entries`, `maker_exits`, `structural_tp_trades`,
    `atr_fallback_tp_trades` (parsed from `close_reason`),
  - `production_tp_unchanged: true`, `paper_tp: structural_maker_first`,
    `leverage_policy: max_2x_safe`, `live_locked/auto_live_locked: true`.
- **`chart_events`** now also reads the B-book row and returns
  `paper_execution_b` (entry/exit/stop order type, tp_set_label, net, fees, leverage,
  notional, margin, risk) via `_parse_b_execution`.
- `portfolio_summary(fee_profile)` already filters one profile — selecting
  `bybit_structural_maker_first` shows the B book directly (no cross-profile sums).

Live verification (real desk DB): compare available — A +3.72% / fees $1763,
**B +8.19% / fees $1585, Δ +4.47pp, fees saved $177.73, maker entries 177, maker
exits 299**.

## Frontend (`frontend/src/{types,api,query,screens}.tsx`)
- Types: `PortfolioCompare`, `PortfolioBookSide`, `ChartEvents.paper_execution_b`.
- `api.portfolioCompare()` + `usePortfolioCompare()`.
- **Dashboard**: new "Paper execution model" card — A vs B return/equity/fees cards +
  a line: `Δ +Xpp · fees saved $Y · maker entries m/total · maker exits · structural
  TP / ATR-fallback`, with the banner *"production TP unchanged · paper TP =
  structural/maker-first · leverage max_2x_safe"*.
- **Trade detail (ClosedDetail)**: new "Paper execution — structural + maker-first (B)"
  block — TP_SET_LABEL badge, entry/exit/stop order-type badges, leverage, B net vs A
  net, "production TP unchanged · paper TP = structural/maker-first".
- Existing per-trade leverage/notional/margin/risk, exact TP R, MECHANICAL_ATR_LADDER
  label and chart markers remain.

`npm run build` (tsc -b && vite build): **exit 0**, 92 modules.

## Labels (clear, non-misleading)
Production TP = MECHANICAL_ATR_LADDER (unchanged). Paper TP = structural/maker-first.
Leverage = max_2x_safe with "leverage ≠ risk" note. Full candlestick line-overlay
remains TODO (markers + structural labels shown).

## Verdict
**APP_SHOWS_ACTIVE_STRUCTURAL_TP_AND_MAKER_FIRST**
