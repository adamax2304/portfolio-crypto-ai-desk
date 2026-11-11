# Implemented vs Recommended

Truth ledger. Future LLMs must consult this before claiming a feature exists.

## Implemented (in code today)

### Modes and routing

- Three trading modes: `scalp`, `intraday`, `swing`. ([config/universe.yaml](../../config/universe.yaml), [src/cli.py](../../src/cli.py), [src/agents/trade_idea_agent.py](../../src/agents/trade_idea_agent.py))
- Mode-specific timeframes and volume floors. ([config/universe.yaml](../../config/universe.yaml))
- Mode-specific scoring multipliers (`scoring.yaml.mode_weights`).
- Auto-universe report flow (Stage 1 discovery → Stage 2 rank → top-N → deep analysis).
- `--discovery` flag widening the scan.

### Tiering and scoring

- A / B / C / rejected tier classification with hard score caps. ([src/agents/scoring_agent.py](../../src/agents/scoring_agent.py))
- Configurable weights, regime multipliers, mode multipliers, risk penalties. ([config/scoring.yaml](../../config/scoring.yaml))
- Rejection block with primary + supporting reasons in every report.

### Exchanges

- Binance / Bybit / MEXC spot OHLCV via `ccxt`.
- Multi-exchange universe aggregator and per-venue universe JSON.
- `ExchangeFusionAgent` building confirmation score, best/focus exchange, risk flags (`mexc_only`, `not_on_anchor`, `no_derivatives_confirmation`, `price_divergence_across_exchanges`).
- Binance USD-M futures funding / OI / long-short context.
- Bybit + OKX public derivatives snapshots.
- Dedicated Bybit derivatives history (OI delta + funding history).

### Indicators

- EMA20/50/200, ATR14, RSI14, returns, volume SMA20, relative strength vs BTC, ATR percentile. ([src/indicators/](../../src/indicators/))

### News / catalysts / attention

- RSS news collector (Binance Announcements, CoinDesk, Cointelegraph, Decrypt). Coinbase RSS disabled (Cloudflare 403).
- Conservative ticker/narrative detection on headlines.
- Manual events loader (`data/raw/events/manual_events.yaml`).
- Manual social and narrative notes loaders.
- Reddit public attention via `SocialCollector`.
- `news_trader_bridge` (read-only) ingesting pre-classified Telegram signals.
- `CrowdAttentionAgent` staging (silent / early / hype / euphoria / exhaustion / fear / rumor).
- `NarrativeAgent` heatmap from configured narratives.

### Output

- Markdown reports under `data/reports/{daily,intraday,scalp,swing,reviews}`.
- `data/processed/context_for_llm.md`.
- SQLite tables `trade_ideas`, `rejected_ideas`, `idea_checks`, `news_items`, `events`, `agent_runs`, `symbols`, `watchlist_alerts`.
- Setup charts for top ideas (matplotlib).

### Telegram

- Outbound bot: `src/notifiers/telegram.py`.
- A/B-tier auto-alerts from `Supervisor._maybe_send_trade_alerts`.
- `WatchlistMonitor` with `monitor-watchlist` CLI and per-symbol cooldown.
- Watchlist alerts now include `SL:` line in addition to `entry`, `TP1`, `TP2`.

### CLI surface

- `update-data`, `daily-report`, `intraday-report`, `scalp-report`, `swing-report`, `update-universe`, `scan-universe`, `rank-candidates`, `exchange-status`, `candidate-debug`, `scan`, `idea`, `status`, `doctor`, `latest`, `ask`, `telegram-setup`, `telegram-test`, `monitor-watchlist`, `review`.

## Partially implemented

- **Catalyst sentiment classification** — currently based on event type + simple keyword match. Recommended: per-source reliability scoring + ML or stronger keyword taxonomy.
- **Primary-source verification** — limited to a `primary_source: true` flag in `sources.yaml`. Recommended: full primary-source verification pipeline for headline tickers.
- **News usefulness review** — no automated link from "this news existed at T" → "this trade outcome was Y". Recommended: post-trade review job that retrofits news impact into [[12_News_Intelligence_Journal/Templates/News_Impact_Review_Template]].
- **Intraday revalidation** — `monitor-watchlist` revalidates C/rejected names but not freshly-rejected B/A; full revalidation is a TODO.
- **Long/short ratio** — only Binance global ratio; per-symbol or top-trader ratios are not yet pulled.

## Recommended (not implemented; documented for future work)

- **Long-term mode** — pages exist as `Recommended`; no code. See [[Long_Term_Mode]].
- **VWAP indicator** — referenced in this vault, not in `src/indicators/`. See [[VWAP]].
- **Liquidation maps** — no integration.
- **Options data** — none.
- **On-chain flows** — none.
- **Token unlock calendar API** — manual events only; recommended: TokenUnlocks API.
- **Paid social sentiment** (LunarCrush, Santiment, CryptoQuant, Glassnode, Dune, CoinGlass, Coinalyze) — `.env.example` reserves keys, no collector yet.
- **Paper-trading journal / execution simulator** — none.
- **Streamlit dashboard** — listed in Priority 3 remaining work.
- **Automated Obsidian export commands** (`export-knowledge-base`, `log-trade-to-obsidian`, `log-news-to-obsidian`, `review-news-impact`, `obsidian-daily-context`) — see [[Obsidian_Export_Commands]]. Templates exist; CLI does not.
- **Native Telegram inbound (Telethon inside crypto-ai-desk)** — out of scope; lives in `news_trader`.
- **Per-source reliability score** for `news_trader` channels — bridge stores source name but does not yet weight by reliability.

## Unknown (verify before relying)

- Source-side cap behavior for new exchange tokens (BNB, OKB, KCS) not in `narratives`. Recommend a quick code re-read before classifying.
- Behavior with very thin watchlist (≤ 3 symbols) — `MarketRegimeAgent` relies on breadth; small N may degrade regime label quality.

## Related

- [[System_Principles]]
- [[LLM_Operating_Instructions]]
- [[Improvement_Backlog]]

## Implemented status

- **Implemented** — this page is itself the inventory.
