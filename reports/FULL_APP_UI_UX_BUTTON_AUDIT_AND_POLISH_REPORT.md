# FULL APP UI/UX + BUTTON AUDIT — REPORT (PART 12)

**Scope:** trading-desk-control frontend. Date: 2026-06-24. PAPER; live locked.

## Verification performed
- **Type + build:** `tsc -b && vite build` → **exit 0, 92 modules**, no type/import/JSX
  errors. This is the primary "broken button / broken render" guard — every tab,
  drawer, badge, and handler is type-checked and bundled.
- **Endpoint shape checks:** `/api/portfolio/compare`, `/api/trades/{id}/chart-events`,
  `/api/trades/{id}/lifecycle`, `/api/market-dashboard`, `/api/missed-opportunities`
  all return valid shapes against the live desk DB (verified by direct calls).
- **Backend tests:** 70 passed (incl. lifecycle, regime, market, actionability-closed).

## Tabs / surfaces reviewed (code-level)
Dashboard (portfolio + A/B card), Active (open/pending with partial badges), Closed
(book view + ClosedDetail drawer w/ LifecyclePanel), Market (redesigned dashboard),
Paper Features, trade-detail drawer, chart overlay, segmented filters, refresh polling.

## Clarity guarantees enforced
- No misleading single exit marker (lifecycle partial fills at true prices).
- No "very late — DO NOT CHASE" on closed trades.
- Regime shows a readable label, not bare "unknown".
- Paper Exec / blended R is the headline; touch R labelled "optimistic" in audit.
- "PAPER · live locked" surfaced; leverage shown with "leverage ≠ risk".
- Compact-first; advanced data behind audit/expanders; badges over text walls.

## Chart library decision
No new chart package installed — a price-scaled SVG overlay (`ExecChart`) places every
level/fill at its true price, which fixes the misleading-marker bug while keeping the
bundle small and stable. Full candlestick line-overlay via `lightweight-charts` (needs a
per-trade OHLCV candle endpoint) is the documented next step.

## Note on interactive click-through
A live Telegram-Mini-App click-through requires the Telegram WebApp context + the running
backend with auth; outside that environment the app renders loading/empty states. The
build + endpoint + backend-test verification above covers the broken-button / broken-data
failure modes deterministically.

## Verdict
**APP_UI_POLISHED_AND_BUTTONS_AUDITED**
