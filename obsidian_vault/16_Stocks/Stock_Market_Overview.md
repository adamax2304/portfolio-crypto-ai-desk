# Stock Market Overview

## What this module is

The stocks pipeline analyzes US equities and major index/sector ETFs the same way the crypto pipeline analyzes spot crypto pairs: it ingests OHLCV, classifies the regime, ranks sectors, computes relative strength, checks earnings risk, evaluates per-symbol setups, applies risk rules, scores, and produces tiered trade ideas.

## Key differences from crypto

| Topic | Crypto | Stocks |
|---|---|---|
| Trading hours | 24/7, no gaps | NYSE/NASDAQ 9:30–16:00 ET; pre/after-hours thin; weekend closed |
| Regime anchors | BTC trend, alt breadth | SPY/QQQ trend, breadth, VIX |
| Relative strength | vs BTC, ETH | vs SPY, QQQ, sector ETF |
| Catalysts | Listings, narrative pumps, funding | Earnings, analyst upgrades, macro prints (CPI/FOMC) |
| Derivatives | Funding rate, OI, long/short ratio | Optional (options Greeks) — not in MVP |
| Liquidity | 24h $ volume | 30-day avg $ volume, premarket gaps |
| Gap risk | None | High — overnight/weekend gaps invalidate stops |

## Universe

Default universe lives in [config/stocks/universe.yaml](../../config/stocks/universe.yaml). It mixes mega-caps (AAPL/MSFT/NVDA/META/AMZN/GOOGL/TSLA), AI/semi specials (AMD/AVGO/SMCI/PLTR), crypto-equity proxies (COIN/MSTR), and major indices/sector ETFs (SPY/QQQ/IWM/DIA, XLK/SMH/XLF/...).

Edit the YAML to add or remove symbols. Sector classification is per-symbol via `symbol_sector_map`.

## Data source

yfinance for MVP. Unofficial, free, rate-limited. Caps:
- 15m bars: max 60 days history
- 1h bars: max ~730 days
- 1d bars: years

Cached CSVs land under `data/raw/stocks/{interval}/{SYMBOL}.csv`. Earnings calendar comes from `yfinance.Ticker.calendar` merged with manual overrides in `data/manual/stocks/earnings_calendar.csv`.

## Isolation guarantee

Stocks agents never import crypto agents. Stocks scoring never references funding/OI. The signal tracker and reports tag every record with `asset_class='stocks'` so analytics never blend crypto and stocks performance.
