# MARKET TAB DASHBOARD REDESIGN — REPORT (PART 10)

**Scope:** data model + endpoint + frontend. Date: 2026-06-24. PAPER/display.

## Data model (desk DB, written by Opus routine, read by app)
`crypto-ai-desk/src/market/market_dashboard.py` — `market_dashboard_snapshots` table:
timestamp, crypto_fear_greed, crypto_market_mode, stocks_market_mode, crypto_main_risk,
stocks_main_risk, today_news (json), long_term_news (json), crypto_regime, stocks_regime,
btc_dominance, eth_btc, vix, spy_trend, qqq_trend, confidence, source_summary,
generated_by, raw_json, created_at.

## Endpoint
`trading-desk-control/backend/app/market_dashboard.py → latest_snapshot()` +
`GET /api/market-dashboard` (read-only). Adds `age_hours`, `stale` (>6h), `stale_warning`
(>4h).

## Frontend (Market tab redesigned)
`frontend/src/screens.tsx::Market()` now renders:
1. **Header** — crypto mode + stocks mode + regime + confidence + last-updated, with a
   stale-warning banner when aging.
2. **Fear & Greed** — crypto F&G (label + tone) + VIX / SPY / QQQ proxy.
3. **Main risk now** — crypto + stocks one-liners.
4. **Today — important news** — curated cards (title, asset/sector, impact tone, why).
5. **Long-term themes** — top 5.
6. **Extras** — BTC dominance, ETH/BTC, SPY/QQQ trend.
7. **Desk narratives** — existing narratives kept as secondary detail.
Falls back to a clear "not populated yet" message before the first Opus run.

## Verified
Endpoint returns a valid snapshot (deterministic fallback present); frontend build clean.

## Verdict
**MARKET_TAB_REDESIGNED_AS_RISK_NEWS_DASHBOARD**
