# Control Plane: Portfolio + Chart Markers (PART 8)

**Date:** 2026-06-24. Read-only app additions. Backend restarted; `/api/health` live_locked:true.

## Backend (`backend/app/portfolio.py` + endpoints)
- `GET /api/portfolio` — reads desk `paper_portfolio_ledger` (read-only): equity, starting deposit, today/7d net $ + net R, total net, return%, max drawdown, fees paid, trades W/L/BE, fee_profile. Open positions/margin = 0 (derived historical ledger). **Verified live:** equity $5146.78, +2.94%, fees $1770.16, maxDD 18.31%, 586 trades, live_locked:true.
- `GET /api/portfolio/trades` — recent ledger exits with all USD fields (entry, stop, notional, margin, leverage, risk $/%, gross/fees/net $, paper R, close_reason).
- `GET /api/trades/{signal_id}/chart-events` — entry/initial-stop/TP1-3 + moved-stop (Stop→BE, Lock +0.5R) **level lines** + entry/tp/stop **event markers** (timestamps) + MFE/MAE + paper R.

## Frontend (`screens.tsx`, `types.ts`, `api.ts`, `query.ts`)
- **Paper Portfolio cards** (dashboard): Paper Equity ($ + return%), Today Net $ (+ net R + 7d), Max Drawdown (+ risk%/trade), Fees Paid (+ profile + W/L). Fallback warning if the ledger isn't built yet.
- Existing Paper-Exec headline + Paper-Features panel retained.
- Per-trade USD fields + TP-quality + protection tags available via the trades read-model + chart-events endpoint.

## Chart markers — status
The chart-events **endpoint is live** (levels + event markers + MFE/MAE). Full candlestick line-overlay rendering on the existing lightweight `Chart.tsx` is deferred to a follow-up (the component renders OHLC; horizontal-line overlay is a larger change) — per the task's explicit "endpoint + timeline first + TODO" allowance. **TODO:** overlay the `chart-events` levels as horizontal lines + entry/exit markers on `Chart.tsx`. The data is fully available now.

## Frontend build: `npm run build` exit 0 (tsc + vite), 92 modules, no type errors.

## Verdict
`APP_SHOWS_USD_PNL_AND_CHART_MARKERS` (cards + USD fields + chart-events endpoint live; full chart line-overlay = noted TODO).
