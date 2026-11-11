# What is crypto-ai-desk

`crypto-ai-desk` is a **local-first AI crypto research terminal**. It is a Python CLI project that lives entirely in `C:\Users\adama\Documents\crypto-ai-desk\` and produces Markdown research reports, ranked trade ideas, and Telegram alerts from public exchange data, RSS news, and a read-only Telegram feed it imports from a sister project (`news_trader`).

It is **not** an execution bot. It does not place orders. It does not custody funds. It writes reports and sends alerts.

## What it actually does (verified from code)

- Fetches Binance / Bybit / MEXC spot OHLCV through `ccxt`.
- Builds a fused multi-exchange universe with per-venue liquidity / ATR / spread filters (`MultiExchangeUniverseCollector`).
- Classifies market regime from BTC + ETH trend + breadth + volatility (`MarketRegimeAgent`).
- Computes deterministic indicators: EMA20/50/200, ATR14, RSI14, returns, volume SMA20, relative strength vs BTC (`src/indicators/`).
- Runs 20+ structured agents (regime, momentum, derivatives, narrative, crowd-attention, technical setup, risk, critic, scoring, trade-idea, review, watchlist monitor, etc.) — see [[Agents_Overview]].
- Tiers every idea into **A / B / C / rejected** with explicit rejection reasons and score caps — see [[Scoring_Overview]].
- Writes Markdown reports under `data/reports/{daily,intraday,scalp,swing,reviews}/` and `data/processed/context_for_llm.md`.
- Persists ideas, rejections, news, events, and alerts into `db/crypto_ai_desk.sqlite`.
- Monitors C-tier / rejected names every N minutes and sends a Telegram alert when one flips to B/A (`WatchlistMonitor` + `monitor-watchlist` CLI).
- Pulls a **read-only** stream of pre-classified Telegram signals from the `news_trader` project's `telemetry.jsonl` via [[Telegram_Integration]].

## What it deliberately does NOT do

- It does not place trades.
- It does not run its own Telethon scraper. The Telegram raw ingestion lives in `news_trader`.
- It does not pretend to have liquidation maps, on-chain flows, paid social sentiment, unlock APIs, or primary-source verification.
- It does not output A-tier ideas unless the score is ≥80 **and** no score caps are active.
- It does not output any idea without a clean invalidation level.

## Roles in this system

- **You** — operator. Triggers reports, reviews ideas, manages risk.
- **The desk (this project)** — generates ideas and alerts.
- **`news_trader` (sister project)** — separate process that scrapes Telegram. This desk consumes its state file read-only. **Never write into news_trader.**
- **LLMs (Claude / Codex / GPT)** — read `context_for_llm.md` and this vault, then reason about trades / system changes.

## Mental model

The desk is a **skeptical research analyst**, not a signal bot. Its purpose is to:

1. Tell you where attention and money are flowing.
2. Tell you why most setups should be rejected.
3. Tell you when one of the surviving setups actually crosses the threshold.

## Related

- [[System_Principles]]
- [[LLM_Operating_Instructions]]
- [[Implemented_vs_Recommended]]
- [[How_to_use_daily]]
- [[How_to_use_with_Claude_or_Codex]]

## Implemented status

- **Implemented** — everything in "What it actually does" maps to working code paths.
