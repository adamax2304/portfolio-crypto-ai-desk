# News Source Health

_Generated: 2026-11-11T21:02:33Z · read-only diagnostic (no ingest/scoring change)._
- Transport errors: 1

- Configured: 74 — **OK 26 · DEGRADED 0 · STALE 0 · DEAD 16 · CONFIGURED 2 · DISABLED 21**
- Dead PRIMARY sources: PR Newswire (Stocks), Business Wire (Stocks)
- Unregistered (bridge/enriched) sources writing data: 83

| Source | class | type | status | 24h | 72h | match% | primary | warnings |
|---|---|---|---|---|---|---|---|---|
| SEC EDGAR | stocks | api | ERROR | 0 | 228 | — | Y | no fresh rows in 24h (had rows in 72h); latest transport error (sec_request_fail |
| CoinDesk | crypto | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| Cointelegraph | crypto | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| Decrypt | crypto | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| The Block | crypto | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| BeInCrypto | crypto | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| AMBCrypto | crypto | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| CryptoSlate | crypto | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| CryptoBriefing | crypto | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| MarketWatch Top Stories | stocks | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| Yahoo Finance Top Stories | stocks | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| Seeking Alpha Market Currents | stocks | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| CNBC Markets | stocks | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| Benzinga Movers | stocks | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| The Motley Fool Investing | stocks | rss | DEAD | 0 | 0 | — |  | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| PR Newswire (Stocks) | stocks | rss | DEAD | 0 | 0 | — | Y | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| Business Wire (Stocks) | stocks | rss | DEAD | 0 | 0 | — | Y | enabled but NO rows in 72h — in config yet not writing data (broken feed / block |
| DefiLlama | crypto | api | CONFIGURED | 0 | 0 | — |  | enabled provider but 0 rows ingested in 72h — free/fallback source not actively  |
| Stooq (stocks/index fallback) | stocks | api | CONFIGURED | 0 | 0 | — |  | enabled provider but 0 rows ingested in 72h — free/fallback source not actively  |
| Coinbase Blog | crypto | rss | DISABLED | 0 | 0 | — | Y | Coinbase RSS currently returns Cloudflare 403 to local CLI requests. |
| Reuters Business | stocks | rss | DISABLED | 0 | 0 | — |  | Reuters Agency feed returns HTTP 404 in the current endpoint; disabled explicitl |
| SEC EDGAR Filings | stocks | api | DISABLED | 0 | 0 | — | Y | Generic browse-edgar Atom returned 0 rows. Replaced by src/news/edgar.py (CIK-ma |
| GlobeNewswire (Stocks) | stocks | rss | DISABLED | 0 | 0 | — | Y | Endpoint repeatedly times out from this host. Coverage remains through PR Newswi |
| Bybit Announcements | crypto | rss | DISABLED | 0 | 0 | — | Y | No reliable public RSS/JSON announcements endpoint; covered via telegram Bybit_A |
| OKX Announcements | crypto | rss | DISABLED | 0 | 0 | — | Y | No reliable public RSS/JSON announcements endpoint; monitor via telegram / manua |
| MEXC Announcements | crypto | rss | DISABLED | 0 | 0 | — | Y | No reliable public RSS/JSON announcements endpoint; covered via telegram MEXC_Of |
| coinglass | crypto | api | DISABLED | 0 | 0 | — |  | optional_paid_sources: disabled (no API key) |
| coinalyze | crypto | api | DISABLED | 0 | 0 | — |  | optional_paid_sources: disabled (no API key) |
| lunarcrush | crypto | api | DISABLED | 0 | 0 | — |  | optional_paid_sources: disabled (no API key) |
| santiment | crypto | api | DISABLED | 0 | 0 | — |  | optional_paid_sources: disabled (no API key) |
| glassnode | crypto | api | DISABLED | 0 | 0 | — |  | optional_paid_sources: disabled (no API key) |
| cryptoquant | crypto | api | DISABLED | 0 | 0 | — |  | optional_paid_sources: disabled (no API key) |
| dune | crypto | api | DISABLED | 0 | 0 | — |  | optional_paid_sources: disabled (no API key) |
| tokenunlocks | crypto | api | DISABLED | 0 | 0 | — |  | optional_paid_sources: disabled (no API key) |
| Benzinga News API | stocks | api | DISABLED | 0 | 0 | — |  | disabled — set BENZINGA_API_KEY to enable (benzinga.com/apis) |
| Polygon news | stocks | api | DISABLED | 0 | 0 | — |  | disabled — set POLYGON_API_KEY to enable (polygon.io/docs) |
| Tiingo/IEX news | stocks | api | DISABLED | 0 | 0 | — |  | disabled — set TIINGO_API_KEY to enable (tiingo.com/documentation) |
| FRED (macro rates/yields/DXY) | macro | api | DISABLED | 0 | 0 | — |  | disabled — set FRED_API_KEY to enable (fred.stlouisfed.org/docs/api) |
| Alpha Vantage (fallback) | stocks | api | DISABLED | 0 | 0 | — |  | disabled — set ALPHAVANTAGE_API_KEY to enable (alphavantage.co/documentation) |
| FMP (earnings/calendar) | stocks | api | DISABLED | 0 | 0 | — |  | disabled — set FMP_API_KEY to enable (site.financialmodelingprep.com/developer/d |
| t.me/AstronomicaNews | crypto | telegram | OK_IDLE | 1 | 11 | 0% |  | targeted catch-up confirmed channel reachable but zero eligible messages; retry  |
| t.me/cryptoquant_official | crypto | telegram | OK_IDLE | 2 | 5 | 100% |  | targeted catch-up confirmed channel reachable but zero eligible messages; retry  |
| t.me/forexlive | stocks | telegram | OK_IDLE | 0 | 0 | — |  | fresh successful transport; no eligible publication in the last 24h; targeted ca |
| t.me/zerohedge | stocks | telegram | OK_IDLE | 0 | 0 | — |  | fresh successful transport; no eligible publication in the last 24h; targeted ca |
| t.me/zachxbt | crypto | telegram | OK_IDLE | 0 | 0 | — |  | fresh successful transport; no eligible publication in the last 24h |
| t.me/peckshield | crypto | telegram | OK_IDLE | 0 | 0 | — |  | fresh successful transport; no eligible publication in the last 24h; targeted ca |
| t.me/lookonchain | crypto | telegram | OK_IDLE | 0 | 0 | — |  | fresh successful transport; no eligible publication in the last 24h; targeted ca |
| Telegram collector | all | telegram_collector | OK_IDLE | 0 | 0 | — | Y | fresh successful transport; no eligible publication in the last 24h |
| Finnhub company-news | stocks | api | OK | 827 | 3133 | 100% |  |  |
| t.me/marketfeed | stocks | telegram | OK | 488 | 1951 | 13% |  | low symbol_match_rate 13% (mostly untagged headlines) |
| t.me/FinancialJuice | stocks | telegram | OK | 232 | 796 | 6% |  | low symbol_match_rate 6% (mostly untagged headlines) |
| t.me/ClashReport | stocks | telegram | OK | 139 | 508 | 7% |  | low symbol_match_rate 7% (mostly untagged headlines); last targeted catch-up fai |
| t.me/WalterBloomberg | stocks | telegram | OK | 45 | 203 | 20% |  |  |
| Finnhub market-news | stocks | api | OK | 36 | 129 | 0% |  | low symbol_match_rate 0% (mostly untagged headlines) |
| t.me/whale_alert_io | crypto | telegram | OK | 27 | 111 | 70% |  |  |
| t.me/MonitoringSituation | stocks | telegram | OK | 22 | 93 | 0% |  | low symbol_match_rate 0% (mostly untagged headlines) |
| t.me/CexAlerts | crypto | telegram | OK | 22 | 73 | 13% | Y | low symbol_match_rate 13% (mostly untagged headlines); last targeted catch-up fa |
| t.me/WatcherGuru | crypto | telegram | OK | 9 | 52 | 11% |  | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/wublockchainenglish | crypto | telegram | OK | 14 | 47 | 42% |  |  |
| t.me/cointelegraph | crypto | telegram | OK | 17 | 47 | 52% |  | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/MEXC_OfficialAnnouncements | crypto | telegram | OK | 21 | 47 | 14% | Y | low symbol_match_rate 14% (mostly untagged headlines); last targeted catch-up fa |
| t.me/disclosetv | stocks | telegram | OK | 7 | 31 | 14% |  | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/BWEtradfi | stocks | telegram | OK | 6 | 26 | 0% |  | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/Middle_East_Spectator | stocks | telegram | OK | 8 | 25 | 0% |  | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/Bybit_Announcements | crypto | telegram | OK | 10 | 23 | 0% | Y | low symbol_match_rate 0% (mostly untagged headlines); last targeted catch-up fai |
| t.me/CoinMarketCapAnnouncements | crypto | telegram | OK | 9 | 23 | 33% | Y | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/OSINTdefender | stocks | telegram | OK | 6 | 20 | 0% |  |  |
| t.me/CryptoRankNews | crypto | telegram | OK | 3 | 11 | 100% |  | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/glassnode | crypto | telegram | OK | 3 | 9 | 66% |  | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/OKXAnnouncements | crypto | telegram | OK | 2 | 8 | 0% | Y | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/binance_announcements | crypto | telegram | OK | 3 | 7 | 33% |  | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/BWEnews | crypto | telegram | OK | 4 | 6 | 0% |  | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| t.me/coin_listing | crypto | telegram | OK | 2 | 4 | 50% | Y | last targeted catch-up failed; live channel heartbeat is evaluated separately |
| Binance Announcements | crypto | rss | OK | 2 | 2 | 0% | Y |  |

**Unregistered sources (writing to news_items but not in sources.yaml):**
- Coinfomania (enriched_review_or_manual): 24h 0 · 72h 0
- Investing.com (enriched_review_or_manual): 24h 0 · 72h 0
- QuiverQuant (enriched_review_or_manual): 24h 0 · 72h 0
- Phemex (enriched_review_or_manual): 24h 0 · 72h 0
- MarketBeat / StockAnalysis (enriched_review_or_manual): 24h 0 · 72h 0
- Wikipedia (enriched_review_or_manual): 24h 0 · 72h 0
- HealthExec (enriched_review_or_manual): 24h 0 · 72h 0
- TipRanks (enriched_review_or_manual): 24h 0 · 72h 0
- CoinMarketCap CMC-AI (enriched_review_or_manual): 24h 0 · 72h 0
- FierceHealthcare (enriched_review_or_manual): 24h 0 · 72h 0
- Fierce Healthcare (enriched_review_or_manual): 24h 0 · 72h 0
- CBS News (enriched_review_or_manual): 24h 0 · 72h 0
- Crypto.com (enriched_review_or_manual): 24h 0 · 72h 0
- CoinGecko (enriched_review_or_manual): 24h 0 · 72h 0
- OpenPR (enriched_review_or_manual): 24h 0 · 72h 0