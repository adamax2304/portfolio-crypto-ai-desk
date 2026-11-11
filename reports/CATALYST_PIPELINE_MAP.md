# Catalyst Pipeline Map (PART 1)

**Date:** 2026-06-15 · Read-only. Pipeline from raw news → catalyst → LLM packet → signal → Telegram.

## 1. Sources (all live)

| Source | Module | Freq | Storage | Timestamp | Symbol extraction | Dedup | Point-in-time? |
|---|---|---|---|---|---|---|---|
| RSS feeds | `data_collectors/rss_news_collector.py` | per scheduler cycle | `news_items` table + `data/raw/news/rss_latest.json` | `published_at` | regex + EntityAliasMatcher → `detected_symbols_json` | URL `ON CONFLICT` | latest-cache per fetch (rows persist) |
| Telegram channels | `data_collectors/telegram_collector.py` | real-time streaming | `news_items` | `msg.date` | EntityAliasMatcher (crypto) | synthetic `t.me/<h>/<id>` URL | streaming |
| news_trader bridge | `data_collectors/news_trader_bridge.py` | on-demand, 240-min lookback | in-memory + `data/processed/news_trader_bridge_latest.json` | `ts_iso` | signal.symbol + cashtag | (ticker, headline) per window | point-in-time snapshot |
| Catalyst classifier | `catalysts/collector.py` + `classifier.py` | per cycle, 12h lookback | `data/catalysts/<date>/catalyst_events.jsonl` + `narrative_baskets.jsonl` | inherited `published_at` + `freshness_hours` | `detected_symbols_json` → alias fallback | `catalyst_id` hash | append-per-cycle (JSONL), baskets overwrite |
| Stocks company news | `stocks/agents/company_news_agent.py` | per stocks cycle | `agent_outputs/*_company_news.json` | published_at | ticker match | — | latest |
| Derivatives (funding/OI) | `data_collectors/*_derivatives_collector.py` | on-demand per symbol | `data/raw/funding/*.json`, `data/raw/open_interest/*.json` | `fetched_at` | config symbol → exchange symbol | last-write-wins | **latest-cache only** |

## 2. Data volume (live, last 14d)

| Metric | Value |
|---|---:|
| news_items total | 13,748 (2018→now) |
| news_items last 48h | 1,718 |
| news_items last 7d | 7,250 (crypto 5,284 / stocks 7,547 over 14d) |
| news_items with detected symbols (7d) | 1,240 / 7,250 (**17%**) |
| catalyst_events.jsonl | written daily, latest 2026-06-15 (1.77 MB) |
| top sources | Yahoo Finance, CryptoBriefing, Motley Fool, Seeking Alpha, t.me/WalterBloomberg, t.me/lookonchain, BeInCrypto, AMBCrypto, CoinDesk, Cointelegraph, CNBC |

The 17% symbol-detection rate is **expected** — most macro/market headlines carry no specific ticker. Coin/stock-specific stories do get symbols via `detected_symbols_json` + EntityAliasMatcher.

## 3. Does each stage reach the next?

| Stage | Reaches reports? | Reaches LLM packet? | Reaches proposed_signals? | Reaches Telegram? |
|---|---|---|---|---|
| RSS/Telegram news | ✅ | ✅ (`packet._build_catalyst_block`) | indirectly via scorer | ⚠️ only if signal `news_supported=1` |
| Catalyst events (JSONL) | ✅ | ✅ (high-conf + legal + rumours sections) | via `catalyst_quality` scoring component | indirectly |
| Narrative baskets | ✅ | ✅ (up to 6, with freshness labels) | no (enrichment only) | no |
| Funding/OI | ✅ | ✅ (DerivativesSummary) | ✅ (`funding_context`/`oi_context` on every crypto signal + scoring alignment penalty) | ⚠️ not in current message body |
| Stocks company news | ✅ | ✅ | scorer uses binary internally, but **`news_supported` flag stays 0** | ❌ not labelled |

## 4. Key structural facts

- **Catalyst pipeline is real and wired end-to-end** for crypto: news → `news_items` → catalyst classifier → JSONL → packet → `catalyst_quality` scoring component → `news_supported` flag on crypto signals.
- **Funding/OI is 100%-covered but latest-cache** — stored as a string blob (`funding=…, crowding=normal`) on each crypto signal at creation time. **No `funding_snapshots` / `oi_snapshots` archive table exists** (confirmed: no such table in DB).
- **Stocks `news_supported` flag is never set** — the stocks scorer reads `news_payload` binary internally, but the signal row's `news_supported` column remains 0 for all 533 closed stocks A/B signals. Catalyst-backed stocks signals are therefore unlabelled (PART 5 / failure mode).
- **No Opus/LLM Telegram path** (confirmed in prior Telegram audit) — catalysts reach Opus via packets only.

See [CATALYST_USAGE_BY_PLAYBOOK_AUDIT.md](CATALYST_USAGE_BY_PLAYBOOK_AUDIT.md) and [OPUS_CATALYST_VISIBILITY_AUDIT.md](OPUS_CATALYST_VISIBILITY_AUDIT.md).
