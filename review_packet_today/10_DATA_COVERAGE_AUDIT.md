# Data Coverage Audit — 2026-05-25

For each of the three analyses, what data was available, used, missing, stale, or placeholder.

Classifications: `OK` (available + used), `UNUSED` (available but ignored), `MISSING`, `STALE`, `PLACEHOLDER`, `N/A`.

---

## CRYPTO SCALP — `2026-05-25_13-52_scalp_report.md`

| Data source | Classification | Notes |
|-------------|---------------|-------|
| 1m OHLCV | UNUSED | Scalp report says it uses 1m/5m/15m, but only 5m/15m derived metrics surface. No 1m-tick context observed in the output. Confirm by reading `src/agents/momentum_scanner_agent.py` |
| 5m OHLCV | OK | Reflected in momentum / volume_ratio computation |
| 15m OHLCV | OK | Used for entry/invalidation/ATR |
| BTC/ETH short-term context | OK | "BTC trend transition_up, ETH range" — but only at 1h granularity. A scalp report could use a tighter BTC reference (5m/15m) |
| Volume data | OK | 20-period volume ratios per symbol (e.g. INJ 2.59x) |
| OI / funding (Bybit + OKX) | OK | Bybit/OKX cross-check section populated for 8 symbols |
| Exchange coverage | OK | binance/bybit/mexc all reported with universe sizes + failure counts |
| News (RSS) | OK | 4 sources, recent items present |
| Telegram / news_trader bridge | MISSING (today) | KOL watch shows "no manual notes found"; nothing fresh in the bridge |
| Obsidian / Current_Context_For_LLM | PLACEHOLDER | The Obsidian context file is a template — never populated today |
| Signal performance summary | UNUSED (in report) | The scalp report does NOT show a "recent signal performance" section. The crypto LLM packet does include `signal-stats` text, but the user-facing report does not surface it |
| Liquidation heatmap | MISSING | Acknowledged blindspot |
| Order book depth / spreads | MISSING | Acknowledged blindspot |
| On-chain whale flows | MISSING | Acknowledged blindspot |
| ETF flows / DXY / yields / macro calendar | MISSING | Acknowledged blindspot |
| Token unlock calendar | MISSING | Acknowledged blindspot |
| Live X / Discord | MISSING | Acknowledged blindspot |

**Freshness**: report data freshness = 2026-05-25 13:45 UTC. Report saved at 13:52 UTC. **7-minute lag — fresh**.

---

## CRYPTO INTRADAY — `2026-05-25_14-03_intraday_report.md`

| Data source | Classification | Notes |
|-------------|---------------|-------|
| 15m OHLCV | OK | Setup quality, entry zones use 15m |
| 1h OHLCV | OK | Trend labels, regime, ATR |
| 4h OHLCV | UNUSED in report text | Implied by intraday but no explicit 4h context section |
| BTC / ETH regime | OK | Same as scalp report |
| Relative strength data | OK | RS vs BTC per symbol |
| OI / funding | OK | Bybit + OKX cross-check populated for 6 symbols |
| Volume anomaly | OK | "Unusual Volume" section (RENDER 3.1x, INJ 3.36x, …) |
| News (RSS) | OK | Same set as scalp, freshly fetched at 17:03 (Cointelegraph 25 items, CoinDesk 25, Decrypt 25, Binance Announcements 20) |
| Telegram / news_trader bridge | MISSING (today) | Same as scalp |
| Narrative / crowd attention | OK | Heatmap populated; Crowd Attention Stages section present |
| Signal stats summary | UNUSED in report | Signal-stats data is queryable separately but not embedded in today's report |
| Weekend Mode | N/A | Today is Monday — overlay correctly inactive |

**Freshness**: report data freshness = 2026-05-25 13:45 UTC. Report saved at 14:03 UTC. **18-minute lag — fresh**.

**Note**: scalp and intraday reports share the **same data freshness timestamp** (13:45 UTC). That means both reports were built from the same OHLCV snapshot — they did not pull independent updates. Acceptable, but the intraday should typically have a slightly later snapshot. Confirm whether the pipeline reuses cache across modes within the hour.

---

## STOCKS INTRADAY — `2026-05-25_14-12_stocks_intraday_report.md`

| Data source | Classification | Notes |
|-------------|---------------|-------|
| Stock OHLCV 15m | OK | All 19 individual stocks have 15m CSVs on disk |
| Stock OHLCV 1h | OK | All 19 + ETFs + indices have 1h CSVs |
| Stock OHLCV 1d | OK | All present |
| Index data SPY/QQQ/IWM/DIA | OK | Used for regime + RS denominator |
| Sector ETF data | OK | 11 sector ETFs (XLB/XLC/XLE/XLF/XLI/XLK/XLP/XLRE/XLU/XLV/XLY) + SMH |
| Volume ratio | OK | Used in setup_quality scoring |
| Data confidence flags | OK | Fix #3 (real data_confidence) applied; ideas show confidence high/medium/low |
| Earnings risk | PLACEHOLDER | 18 events "tracked" but every idea's evidence says `earnings:unknown`. Lookups 404'd for SPY/QQQ/IWM/DIA/SMH/XLK/XLF/XLE/XLY/XLV (expected — they are ETFs). But the per-stock earnings should resolve for AAPL/LLY/AMD/etc. and they did not surface to evidence |
| Company news | PLACEHOLDER | All 4 news items in the report are `test_source`. Real Reuters/Benzinga/company filings not wired |
| Stock-specific news tagging | PARTIAL | The 4 test items are tagged to symbols (AAPL/NVDA/COIN/MSTR) — wiring works; data is fake |
| Sector rotation | OK | Strongest / weakest sectors with RS vs SPY 20d |
| Relative strength vs index | OK | Used in evidence per idea |
| Relative strength vs sector | OK | Used in evidence per idea |
| VIX | OK | 16.64, used in regime |
| Signal stats summary | UNUSED in report | Not embedded; only available via `signal-stats --asset-class stocks` |
| Stocks RSS feeds (MarketWatch, Yahoo Finance, Seeking Alpha) | DISABLED | The intraday log shows: "Skipping disabled RSS source MarketWatch Top Stories / Yahoo Finance Top Stories / Seeking Alpha Market Currents" |
| Macro/geopolitics for stocks | MISSING | Stocks pipeline does not call MacroGeopoliticsAgent; macro context for equities (Fed, CPI, yields) is not surfaced |

**Freshness**: report data freshness = 2026-05-25 14:12 UTC. Report saved at 14:12 UTC. US market opened at 13:30 UTC, so the data is from **42 min into the session — fresh and intraday**.

---

## Cross-cutting blindspots (acknowledged by the system itself)

The crypto reports' "Data Coverage / Blindspots" section explicitly lists these as not implemented:
- Liquidation heatmaps and leverage clusters
- Order book depth, spreads, and CVD
- ETF flows, stablecoin liquidity, DXY/yields, macro calendar
- On-chain whale flows and exchange inflow/outflow
- Token unlock calendar (manual)
- Live X/Telegram/Discord/KOL feeds (manual)

These are not failures — they are flagged blindspots. **Credit to the system for surfacing them**; the audit confirms they are still gaps.

---

## Summary

| Pillar | Crypto Scalp | Crypto Intraday | Stocks Intraday |
|--------|--------------|-----------------|-----------------|
| OHLCV coverage | OK (1m unverified) | OK | OK |
| Regime data | OK | OK | OK |
| Volume anomaly | OK | OK | OK |
| Relative strength | OK | OK | OK |
| Derivatives | OK | OK | N/A |
| Sector / index rotation | N/A | N/A | OK |
| Real news | OK (RSS) | OK (RSS) | **PLACEHOLDER (test_source only)** |
| Earnings risk | N/A | N/A | **PLACEHOLDER (always "unknown")** |
| Telegram / KOL | MISSING | MISSING | N/A |
| Obsidian live context | PLACEHOLDER (template) | PLACEHOLDER | PLACEHOLDER |
| Signal stats in report | UNUSED | UNUSED | UNUSED |
| Liquidation / orderbook / on-chain | MISSING | MISSING | N/A |
| Macro calendar | MISSING (1 headline only) | MISSING | MISSING |

**The single biggest data gap today is the stocks news/earnings layer.** It is structurally present in code (CompanyNewsAgent + EarningsRiskAgent) but operating on fake / disabled inputs. Until real RSS or earnings APIs are wired, every stocks idea ships with "earnings:unknown" — a known unknown the LLM should weight heavily.
