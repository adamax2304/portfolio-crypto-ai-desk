# EXCHANGE-LIKE TRADE DETAIL UI — REPORT (PART 6)

**Scope:** trading-desk-control frontend. Date: 2026-06-24. PAPER; live locked.

## What was built
`frontend/src/screens.tsx` — new `LifecyclePanel` (+ `ExecChart`, `Row`) rendered in the
trade-detail drawer (`ClosedDetail`) from `/api/trades/{id}/lifecycle`. Sections:

- **A. Header** — symbol, direction, status badge (Waiting entry / Entry filled · waiting
  TP1 / TP1 filled · waiting TP2/TP3 / TP2 filled · runner to TP3 / Closed win / Stopped /
  Expired flat), playbook, regime (readable), tier (existing header retained).
- **B. Position summary** — risk $, risk %, notional, qty, leverage, margin, liq≈,
  `leverage_reason`, liq-distance vs stop-distance, "leverage ≠ risk", risk-capped / liq-
  buffer flags.
- **C. Price ladder** — entry, initial stop (max loss $), current/moved stop (R locked),
  TP1/TP2/TP3 with exact R + **$ per fill** (on the partial slice).
- **D. Execution timeline** — every lifecycle event with price, qty, R, $, fee, order
  type, reason, relative time.
- **E. Chart** — price-scaled `ExecChart` overlay (lines + true-price fill dots).
- **F. Setup analysis** — existing catalyst / TP-quality / fee-survival / maker-first
  (B-book) blocks retained.
- **G. Audit/debug** — touch R (optimistic), MFE/MAE, outcome, blended-vs-touch note.

## UI discipline
Compact-first: badges over text walls; advanced data (audit, B-book) below the fold;
clear "PAPER · live locked". No new chart library installed — the price-scaled SVG
overlay keeps the bundle stable (frontend build 92 modules, exit 0); full
lightweight-charts candle overlay is a documented TODO.

## Verdict
**TRADE_DETAIL_UI_EXCHANGE_LIKE_AND_CLEAR**
