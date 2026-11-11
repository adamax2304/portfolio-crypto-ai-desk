# MARKET TAB VIX + DATA FIX (PART 9)

**Date:** 2026-06-24. PAPER/display.

## Root cause
VIX was blank because the snapshot writer set `vix=None` (no VIX provider was wired); the
Market tab then showed "—".

## Fix
- New `src/market/market_dashboard.py::fetch_market_extras()` — deterministic, fail-open
  per field: **VIX** (`yfinance ^VIX`), **SPY/QQQ trend** (last vs 10-day SMA → up/down/
  flat), **ETH/BTC** (ETH-USD ÷ BTC-USD). Returns `vix_source` ("yfinance ^VIX" or
  "unavailable").
- `_backfill_extras()` fills null vix/spy/qqq/eth_btc on any snapshot; called by
  `parse_and_store` (Opus path) and `deterministic_fallback` → **VIX is never silently
  blank**; if truly unavailable the snapshot keeps null + `vix_source` reason.
- `scripts/populate_market_dashboard_now.py` now fetches extras into the snapshot.
- Frontend Market tab VIX card shows the value (tone by level) or **"VIX unavailable"**
  explicitly, never blank.

## Live result
Snapshot now: **VIX 19.7**, SPY **down**, QQQ **down**, ETH/BTC **0.0265**, crypto F&G
**17 (extreme fear)**, crypto mode risk_off, stocks mode chop, crypto/stocks main-risk
lines + 6 today-news + 5 long-term-news; stale-warning >4–6h; source + last-updated +
confidence shown. Verified via `/api/market-dashboard` (200).

## Verdict
**MARKET_TAB_VIX_AND_DATA_LOADED_OR_EXPLAINED**
