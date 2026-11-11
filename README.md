# Crypto AI Desk

Local-first AI crypto research terminal for disciplined scalp / intraday / swing trade idea generation across **Binance, Bybit, and MEXC**.

> **LLM Operating Protocol** — every Claude / Codex / GPT session that touches this project must read `prompts/system/AI_TRADING_DESK_SYSTEM_PROMPT.md` first, then run `python -m src.cli prepare-analysis --mode <mode>` to generate `data/processed/llm_analysis_packet.md` and follow the workflow in `prompts/system/ANALYSIS_WORKFLOW_PROTOCOL.md`. See the [LLM Operating Protocol](#llm-operating-protocol) section below for the full surface.

This project is built to behave like a skeptical research desk, not a blind signal bot. It uses public OHLCV data from multiple exchanges, deterministic indicators, structured agents, transparent scoring, **A/B/C tier classification with explicit rejection reasons**, Markdown reports, and SQLite trade idea tracking. It is designed so Codex / Claude can inspect the local files and reason from the generated context without inventing market facts.

## Current Project State

For the current trading-system state, locked rules, active verdicts, and next decision gates, read these first:

- [`PROJECT_STATE.md`](PROJECT_STATE.md) — status, verdicts, locked rules, next actions (single source of truth)
- [`docs/DECISION_LOG.md`](docs/DECISION_LOG.md) — material decisions and why
- [`docs/AGENT_HANDOFF.md`](docs/AGENT_HANDOFF.md) — what the next agent must do / must not touch
- [`docs/decisions/`](docs/decisions/) — ADRs · [`docs/WEEKLY_FORWARD_METRICS.md`](docs/WEEKLY_FORWARD_METRICS.md) — forward review template

**Every agent must update `PROJECT_STATE.md` and `docs/DECISION_LOG.md` after doing work.** The system is **NOT live-ready**; live/trade-math stays locked. Validate the doc layer with `python -m scripts.check_project_state_docs`.

## Exchange Roles

- **Binance** — primary liquidity anchor and main structure reference. Default source for clean OHLCV. Anything not listed on Binance is automatically downgraded.
- **Bybit** — derivatives / perp confirmation layer. Funding, open-interest, and short-term perp momentum.
- **MEXC** — early momentum / new-listing discovery surface. Higher noise, smaller caps. **MEXC-only setups are capped at B-tier** unless liquidity is exceptional.

The desk classifies symbols across all three venues, then fuses them: a Binance setup confirmed on Bybit OI/funding scores higher than a MEXC-only pump.

## A/B/C Tier System

Every idea is classified into one explicit bucket:

- **A-tier** — strong setup, clean invalidation, anchor + derivatives confirm, no active score caps.
- **B-tier** — valid setup but one or two confirmations missing (no derivatives, MEXC-only with strong structure, mild cap active).
- **C-tier / Watchlist** — interesting but not entry-ready. Waiting for pullback, reclaim, breakout retest, or confirmation.
- **Rejected / Not Ready** — explicit reason: no clean invalidation, stale data, extreme funding against direction, MEXC-only without confirmation, unverified rumor-only catalyst, low liquidity, etc.

The report always shows rejected ideas with reasons so you know *why* the desk is silent rather than "no trade."

### Score caps

Hard ceilings prevent A-tier on weak signals:

- No clean invalidation → score cap 50, tier=rejected.
- Stale data (>3h) → score cap 50, tier=rejected.
- MEXC-only listing → cap 70 (65 with weak structure).
- Not on anchor exchange → cap 75.
- Low liquidity → cap 60.
- Unverified rumor-only catalyst → cap 55.
- Extreme funding against the planned direction → cap 78.

Tunable in `config/scoring.yaml` (`thresholds`).

## What It Does

Implemented local MVP includes:

- Fetches Binance, **Bybit, and MEXC** spot OHLCV through `ccxt`.
- Multi-exchange universe aggregator: per-venue Stage 1 discovery + Stage 2 ranking, fused into a single ranked candidate list with `exchange_symbol_map.json`.
- `ExchangeFusionAgent` builds a confirmation score, picks `best_exchange_for_data` and `suggested_exchange_focus` per symbol, and flags MEXC-only / not-on-anchor / price-divergence risks.
- `CrowdAttentionAgent` stages symbols into silent / early / hype / euphoria / exhaustion / fear / rumor.
- Manual notes loaders for `data/manual/social_notes.yaml` and `data/manual/narrative_notes.yaml` so you can inject trusted alpha without paid APIs.
- Original Binance spot OHLCV pipeline (kept as fallback).
- Discovers the broad active Binance USDT universe, filters junk pairs, ranks opportunities, then sends only the best names to deeper agents.
- Caches candles locally as CSV.
- Calculates EMA, ATR, RSI, volume averages, returns, relative strength, and basic volatility.
- Classifies market regime from BTC, ETH, breadth, and volatility.
- Ranks momentum and weakness candidates.
- Builds technical setups with entry zones, invalidation, targets, risk/reward, and no-chase warnings.
- Scores ideas using `config/scoring.yaml`.
- Generates daily/intraday Markdown reports.
- Writes `data/processed/context_for_llm.md` for Codex/LLM inspection.
- Saves generated trade ideas into SQLite.
- Reviews prior ideas with post-idea candle checks, entry-trigger detection, and MFE/MAE tracking.
- Fetches Binance USD-M futures funding, open interest history, and long/short ratios where public endpoints support the symbol.
- Cross-checks public Bybit/OKX funding and open-interest context where available.
- Expands beyond the manual major watchlist with a two-stage Binance USDT universe scanner, including liquid majors and tradable smaller alts.
- Fetches RSS news from available free sources and detects tickers/narratives with conservative matching.
- Fetches public Reddit attention signals and separates them from manual KOL/crowd notes.
- Loads manual event/catalyst files into SQLite.
- Runs explicit derivatives, news, catalyst, risk, and critic agents before scoring.
- Builds a narrative heatmap from configured sectors, news attention, catalysts, momentum, volume, and crowding risk.
- Adds macro/geopolitical keyword scanning, crowd attention, KOL/manual notes, and a data coverage audit to `context_for_llm.md`.
- Generates simple setup charts for top active/watchlist ideas.

The system still does **not** pretend to have liquidation maps, paid social sentiment, on-chain flows, unlock APIs, or primary-source verification for every headline. Missing or failed data is shown in the report and reduces confidence. Coinbase RSS is disabled by default because it currently returns Cloudflare 403 to local CLI requests.

## Install

Use Python 3.11+ from the project root:

```powershell
cd C:\Users\adama\Documents\crypto-ai-desk
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No paid API keys are required for the MVP.

## Configure Watchlist

Edit:

```text
config/watchlist.yaml
```

You can add/remove symbols, change timeframes, and adjust narrative mappings. Symbols use ccxt format, for example:

```yaml
symbols:
  - BTC/USDT
  - ETH/USDT
  - SOL/USDT
```

If a symbol is not listed on Binance spot, the collector skips it and reports the failure instead of crashing. Known useful-but-inactive symbols can be kept under `inactive_symbols` in `config/watchlist.yaml`.

## Configure Universe Scanner

The broad scanner is configured in:

```text
config/universe.yaml
```

It controls:

- `quote_currency`: default `USDT`.
- `market_type`: `spot` now; `futures/perpetual` is supported by the collector shape for later expansion.
- `min_24h_quote_volume`: rough liquidity gate before fetching candles.
- `min_recent_candle_quote_volume`: mode-specific recent liquidity gate.
- `max_spread_pct`: skips pairs with wide quoted spreads when Binance provides bid/ask.
- `min_atr_percent`: mode-specific volatility floor.
- `max_symbols_for_rank_scan`: fast Stage 2 candle scan size.
- `max_symbols_for_deep_analysis`: usually top 30.
- `max_symbols_for_trade_ideas`: usually top 10-15 for full agent consideration.
- `excluded_symbols`, `excluded_keywords`, `stable_or_fiat_bases`: junk/stable/leveraged/synthetic filters.
- `preferred_symbols`: majors and important names to keep in the mix.

The scanner runs in two stages:

1. Stage 1 discovers active Binance USDT symbols, excludes inactive markets, stable/fiat bases, leveraged tokens, synthetic wrapped pairs, non-ASCII/broken symbols, and low-quality keyword matches. It saves:

```text
data/processed/symbol_universe.json
```

2. Stage 2 ranks the tradable subset with quick OHLCV metrics: 1h/4h/24h change, ATR %, recent quote volume, volume anomaly, relative strength vs BTC, breakout/range expansion, liquidity score, opportunity score, and risk flags. It saves:

```text
data/processed/candidates/universe_ranked_candidates.json
data/processed/candidates/universe_ranked_candidates_<mode>.json
```

Run it directly:

```powershell
python -m src.cli update-universe
python -m src.cli scan-universe --mode intraday
python -m src.cli rank-candidates --mode scalp
python -m src.cli rank-candidates --mode swing --refresh-universe
```

Modes:

- `scalp`: 1m/5m/15m focus, 1-2 hour horizon, volume anomaly and short-term expansion.
- `intraday`: 15m/1h/4h focus, 4-24 hour horizon, relative strength and clean structure.
- `swing`: 1h/4h/1d focus, several-day horizon, higher timeframe trend and catalysts.

Auto-universe reports (mode-specific timeframes + filters):

```powershell
python -m src.cli scalp-report --auto-universe       # 1m/5m/15m, 30m-2h horizon
python -m src.cli intraday-report --auto-universe    # 15m/1h/4h, 4-24h horizon (alias of daily-report --mode intraday)
python -m src.cli swing-report --auto-universe       # 1h/4h/1d, several days
python -m src.cli daily-report --auto-universe --mode intraday
```

## Multi-Exchange CLI

```powershell
python -m src.cli update-universe          # rebuild symbol_universe.json + exchange_symbol_map.json
python -m src.cli exchange-status          # per-venue role, last update, OHLCV/failed counts
python -m src.cli scan-universe --mode intraday
python -m src.cli candidate-debug --symbol SOL/USDT --mode intraday
```

`candidate-debug` explains exactly why a symbol passed or failed: exchange membership,
liquidity, ATR, momentum, RS vs BTC, risk flags, and which venue carries it.

## Manual notes

Drop short, dated lines into:

```text
data/manual/social_notes.yaml      # KOL / Telegram / X attention
data/manual/narrative_notes.yaml   # narrative biases / stage hints
```

Each note bumps an attention score but never produces a trade on its own. Rumor-tagged notes are downgraded to "rumor_driven" stage and can never reach A-tier.

The wider universe increases discovery, but it does not force trades. Wide spreads, weak volume, low ATR, missing candles, overextension, bad risk/reward, and weak invalidation still push symbols into watchlist/no-trade behavior.

## Run Data Update

```powershell
python -m src.cli update-data
```

You can also use the natural-language router:

```powershell
python -m src.cli ask "Analyze the market today and give me the best trade ideas"
python -m src.cli ask "Update the data and check if morning ideas are still valid"
python -m src.cli ask "Find where money and attention are flowing today"
python -m src.cli ask "Review today ideas and tell me what worked and failed"
```

Quick readiness check:

```powershell
python -m src.cli doctor
python -m src.cli latest --kind daily
```

Focused update:

```powershell
python -m src.cli update-data --symbols BTC/USDT SOL/USDT TAO/USDT
```

Cached candles are saved under:

```text
data/raw/ohlcv/binance/<timeframe>/<SYMBOL>.csv
```

## Generate Daily Report

```powershell
python -m src.cli daily-report
python -m src.cli daily-report --auto-universe
```

Output:

```text
data/reports/daily/YYYY-MM-DD_daily_report.md
data/processed/context_for_llm.md
```

The report includes:

- Market regime.
- Where money appears to be flowing.
- Strongest/weakest symbols.
- Unusual volume.
- Narrative heatmap.
- Derivatives overview.
- Bybit/OKX derivatives cross-check.
- Macro/geopolitics and crowd attention.
- News/catalysts.
- Trade idea cards.
- Setup charts for top ideas.
- Watchlist-only names.
- No-trade warnings.
- Missing-data disclosures.

## Generate Intraday Report

```powershell
python -m src.cli intraday-report
python -m src.cli scalp-report --auto-universe
```

This refreshes `15m` and `1h` data first, then writes:

```text
data/reports/intraday/YYYY-MM-DD_HH-MM_intraday_report.md
```

Skip refresh if you only want to reuse cached data:

```powershell
python -m src.cli intraday-report --no-update
```

## Scan Symbols

```powershell
python -m src.cli scan --symbols BTC/USDT SOL/USDT TAO/USDT
```

This prints the momentum scanner table from cached local data.

## Focused Idea

```powershell
python -m src.cli idea --symbol SOL/USDT
```

This generates a focused intraday-style report for one symbol.

## Windows Shortcuts

PowerShell wrappers live in `scripts/`:

```powershell
.\scripts\install.ps1
.\scripts\daily.ps1
.\scripts\intraday.ps1
.\scripts\review.ps1
.\scripts\latest.ps1
.\scripts\open_latest_daily.ps1
.\scripts\quick_check.ps1
```

For the shortest operating guide, open:

```text
START_HERE.md
```

## Review Prior Ideas

```powershell
python -m src.cli review
```

Output:

```text
data/reports/reviews/YYYY-MM-DD_HH-MM_review.md
```

SQLite tables are created in:

```text
db/crypto_ai_desk.sqlite
```

Main tables:

- `trade_ideas`
- `idea_checks`
- `news_items`
- `events`
- `agent_runs`
- `symbols`

## Manual Events

Manual events are loaded during `update-data` and used by the catalyst/risk agents:

```text
data/raw/events/manual_events.yaml
```

Example:

```yaml
- date: 2026-05-22
  ticker: SOL
  event: Major ecosystem announcement
  type: ecosystem
  source: https://example.com
  importance: 3
```

Supported future event types:

- listing
- unlock
- airdrop
- mainnet
- testnet
- partnership
- governance
- migration
- conference
- macro
- other

## Manual KOL / Crowd Notes

Free live X/Telegram/Discord ingestion is intentionally not automated in the MVP. To include trusted crowd observations in the next GPT analysis, edit:

```text
data/raw/social/manual_social_mentions.yaml
```

Example:

```yaml
mentions:
  - observed_at: "2026-05-21T09:30:00Z"
    source: "X / trusted_account"
    symbol: "SOL/USDT"
    topic: "SOL ecosystem rotation"
    stance: "bullish"
    confidence: "medium"
    note: "Several trusted accounts discussing fresh SOL ecosystem flows."
```

The watchlist/checklist for accounts and topics lives in:

```text
config/kol_watchlist.yaml
```

## How To Read The Scores

Scores are transparent and configured in:

```text
config/scoring.yaml
```

Default thresholds:

- `85-100`: strong idea, still requires risk management.
- `70-84`: valid idea.
- `55-69`: watchlist only.
- `<55`: no trade.

The MVP gives baseline partial credit for missing derivatives/news/narrative inputs, then applies explicit penalties. This prevents the system from handing out fake high confidence while still allowing strong price/volume/structure setups to surface.

## Current Architecture

```text
src/
  data_collectors/       public/free data ingestion
  indicators/            deterministic signal functions
  agents/                structured research agents
  reports/               Markdown rendering
  storage/               CSV/JSON and SQLite persistence
  utils/                 time, symbols, formatting, validation
```

Core workflow:

```text
update-data
  -> BinanceUniverseCollector
     -> Stage 1 broad Binance USDT discovery
     -> Stage 2 liquidity/opportunity ranking
  -> BinanceOHLCVCollector
  -> BinanceDerivativesCollector
  -> MultiExchangeDerivativesCollector
  -> RSSNewsCollector
  -> SocialCollector
  -> Manual events loader
  -> local CSV cache

daily-report
  -> MarketRegimeAgent
  -> MomentumScannerAgent
  -> DerivativesAgent
  -> MultiExchangeDerivativesAgent
  -> NewsAgent
  -> CatalystAgent
  -> MacroGeopoliticsAgent
  -> SocialAttentionAgent
  -> CrowdLeaderAgent
  -> TechnicalSetupAgent
  -> RiskAgent
  -> CriticAgent
  -> ScoringAgent
  -> TradeIdeaAgent
  -> CoverageAuditAgent
  -> Markdown report + context_for_llm.md + SQLite ideas

review
  -> ReviewAgent
  -> idea_checks + review Markdown
```

## Adding Paid APIs Later

The config already reserves optional keys in `.env.example` for:

- CoinGlass
- Coinalyze
- LunarCrush
- Santiment
- Glassnode
- CryptoQuant
- Dune
- TokenUnlocks

Suggested integration pattern:

1. Add a collector under `src/data_collectors/`.
2. Save raw responses under `data/raw/<source>/`.
3. Normalize into structured JSON/CSV.
4. Add or extend an agent under `src/agents/`.
5. Feed outputs into `ScoringAgent` and `TradeIdeaAgent`.
6. Lower confidence when a source is stale or missing.

## Priority 2 Completed

- Binance futures funding/open-interest/long-short context.
- RSS news collector with URL deduplication and conservative symbol detection.
- Manual event loader connected to SQLite.
- `NewsAgent` with source and symbol/narrative grouping.
- `CatalystAgent` with manual events plus news mentions.
- Explicit `RiskAgent` gate.
- `CriticAgent` that argues against every setup before scoring.

Remaining Priority 2 hardening:

- Add better primary-source exchange announcement feeds where RSS is blocked.
- Add event freshness/expiry controls in the CLI.
- Improve catalyst sentiment classification beyond simple event type.
- Add source-level reliability scoring.

## Priority 3 Roadmap

Implemented core:

- `NarrativeAgent` heatmap from news/events plus sector momentum.
- Narrative-aware scoring and idea evidence.
- Chart generation for top active/watchlist ideas.
- Better review analytics using candles after idea creation, entry-zone detection, and MFE/MAE.

Remaining Priority 3:

- Intraday idea revalidation instead of full report reuse.
- Streamlit dashboard.

## Intelligence Layer Added

The desk now includes the five extra context layers requested for GPT analysis:

- Macro/geopolitics scan from RSS headlines and configurable risk-on/risk-off keywords.
- Social attention scan from public Reddit sources.
- Manual KOL/crowd watchlist and notes.
- Multi-exchange derivatives cross-check from Bybit/OKX public endpoints.
- Data coverage audit that tells GPT which sources are missing, partial, or still blindspots.

Important remaining blindspots are named directly in reports: liquidation maps, order-book depth/CVD, ETF/stablecoin/macro calendar, on-chain flows, paid social sentiment, and automated token unlock calendars.

## Priority 4 Roadmap

- Paid derivatives APIs.
- On-chain data.
- Social attention/sentiment.
- Liquidation maps.
- Options data.
- Telegram/Discord alerts.
- Paper trading journal and execution simulator.

## LLM Operating Protocol

The project ships a permanent operating contract for AI sessions. It lives under `prompts/system/` and is mirrored into `obsidian_vault/15_LLM_Context/`. Every Claude / Codex / GPT session that touches the desk must follow it.

### Files

```
prompts/system/
  AI_TRADING_DESK_SYSTEM_PROMPT.md      # canonical operating contract — read first
  ANALYSIS_WORKFLOW_PROTOCOL.md         # step-by-step workflow for any analysis
  OBSIDIAN_MEMORY_PROTOCOL.md           # how to read from / write to the vault
  TRADE_IDEA_LOGGING_PROTOCOL.md        # where ideas get filed and named
  NEWS_INTELLIGENCE_PROTOCOL.md         # Telegram / news classification + caps
  MODE_SELECTION_PROTOCOL.md            # scalp / intraday / swing / invest fallback
  RISK_AND_SCORING_PROTOCOL.md          # caps, penalties, tier thresholds
  WATCHLIST_AND_TIER_PROTOCOL.md        # A/B/C/rejected classification rules
  REVIEW_AND_LEARNING_PROTOCOL.md       # per-trade, daily, weekly review loop

obsidian_vault/15_LLM_Context/
  System_Prompt_For_Analysis.md         # vault-side mirror of the system prompt
  Pre_Analysis_Checklist.md             # gate before any output
  Post_Analysis_Checklist.md            # gate before closing the session
  Current_Context_For_LLM.md            # paste-ready live snapshot
  How_LLM_Should_Read_This_Vault.md     # reading-order discipline
  Pre_Trade_Checklist_For_LLM.md        # per-trade evaluation
  Post_Trade_Review_Checklist_For_LLM.md# per-trade review after close
  News_Evaluation_Checklist_For_LLM.md  # for any "is this news useful?" ask
  System_Modification_Checklist_For_LLM.md # for any code/config change
```

### How an LLM session should start

1. Run:
   ```powershell
   python -m src.cli prepare-analysis --mode intraday
   ```
   This writes `data/processed/llm_analysis_packet.md` — a single Markdown file bundling:
   - mode + fallback announcement (`invest` → `swing`),
   - canonical system prompt excerpt,
   - latest `context_for_llm.md`,
   - `last_update.json` (data freshness),
   - latest matching report content (head only),
   - Stage 2 ranked candidates,
   - latest `trade_idea_agent` payload (A/B/C/rejected),
   - `news_trader_bridge` snapshot,
   - paths of the Obsidian rules to load,
   - latest entries from each journal folder,
   - improvement backlog,
   - pre-analysis checklist embedded,
   - required output format.

2. Read that packet. Read the Obsidian rules it references.
3. Follow `prompts/system/ANALYSIS_WORKFLOW_PROTOCOL.md` steps 0–9.
4. Close the session by completing `obsidian_vault/15_LLM_Context/Post_Analysis_Checklist.md`.

### Mode shortcuts

```powershell
python -m src.cli prepare-analysis --mode scalp      # 1m/5m/15m, 30m–2h horizon
python -m src.cli prepare-analysis --mode intraday   # 15m/1h/4h, 4–24h (default)
python -m src.cli prepare-analysis --mode swing      # 1h/4h/1d, several days
python -m src.cli prepare-analysis --mode invest     # fallback to swing with announcement
python -m src.cli prepare-analysis --mode review     # bundles latest reviews
python -m src.cli prepare-analysis --mode news-only  # attention/news-focused packet
```

### Where ideas + news get logged

- A-tier / B-tier ideas → `obsidian_vault/11_Trade_Journal/Potential_Trades/` (template: `Potential_Trade_Template.md`).
- Watchlist (C-tier with trigger) → `obsidian_vault/11_Trade_Journal/Watchlist_Ideas/`.
- Educational rejections → `obsidian_vault/11_Trade_Journal/Rejected_Ideas/`.
- Useful / useless / fake / market-moving news → respective folders in `obsidian_vault/12_News_Intelligence_Journal/`.
- Daily / weekly / per-idea reviews → `obsidian_vault/11_Trade_Journal/Reviews/`.
- Lessons that should change the system → `obsidian_vault/13_Debugging_and_Improvement/Improvement_Backlog.md`.

Filename pattern: `YYYY-MM-DD_SYMBOL_MODE_DIRECTION_TIER_SCORE.md`.

### CLI surface for the protocol layer

```powershell
python -m src.cli prepare-analysis --mode <mode>        # implemented
python -m src.cli log-idea-to-obsidian --idea-id ID     # TODO (manual today; template path emitted)
python -m src.cli log-news-to-obsidian --news-id ID     # TODO
python -m src.cli update-obsidian-context               # TODO (use prepare-analysis output)
python -m src.cli review-day --write-obsidian           # TODO (use `review` + Daily_Review_Template)
```

The TODO commands exist but emit a clear "not implemented yet — here's the manual path" message. They will be implemented in future iterations (see `Improvement_Backlog`).

### Hard rules an LLM must never break

- A-tier requires score ≥ 80 **and** no active score caps.
- No invalidation → tier = rejected (cap 50).
- Stale data > 3h → tier = rejected (cap 50).
- MEXC-only caps at 70 (65 if structure is weak).
- Unverified rumor catalyst caps at 55.
- Telegram never raises trade score directly — only attention staging in `CrowdAttentionAgent`.
- `news_trader_bridge` is **strictly read-only**.
- Only three modes are implemented (`scalp`, `intraday`, `swing`). `invest` falls back to `swing` with an explicit announcement.
- NO TRADE is a valid, often preferred answer.
- When code and protocol conflict, the code wins — flag the conflict.

## Signal Tracking & Performance Analytics

A passive layer that records every A/B (and watchlist+trigger) trade idea the desk generates, then measures whether it actually worked. The point: build evidence that A-tier signals deserve their A label, that B-tier isn't just noise, that weekend signals aren't worse than weekday signals — over hundreds of samples, not three.

### Why "proposed signals" vs "executed trades"

The tracker measures **what the desk suggested**. It does NOT know whether the operator actually entered. That's a deliberate split:

- *Proposed signal performance* answers "is the system's research worth following?".
- *Executed trade performance* (real PnL) is a separate ledger the operator maintains.

Both matter. Conflating them hides whether bad PnL was bad signals or bad execution.

### What gets tracked automatically

After every report, the supervisor auto-registers every A-tier and B-tier idea. C-tier ideas are registered only if they include an actionable entry+invalidation (controlled by `track_watchlist_with_trigger` in `config/signal_tracking.yaml`). Rejected ideas are not tracked by default.

### Workflow

```
python -m src.cli register-signals             # backfill from latest agent output (auto runs after reports)
python -m src.cli active-signals               # what is still waiting / triggered
python -m src.cli signal-detail sig_<hash>     # full plan + outcome history for one signal
python -m src.cli track-signals --all          # walk OHLCV and update outcomes
python -m src.cli signal-stats --period week   # winrate / PF / breakdowns + sample-size labels
python -m src.cli review-signals --period today --write-obsidian  # narrative review note in vault
```

Outputs land in:

- `db/crypto_ai_desk.sqlite` → tables `proposed_signals`, `signal_outcomes`, `signal_performance_snapshots`.
- `obsidian_vault/11_Trade_Journal/Signal_Performance/` (Daily/Weekly/Monthly reviews + per-signal logs).
- `data/processed/llm_analysis_packet.md` → compact section **Recent Signal Performance**.

### Metric semantics

All R-based. Default R model: stop = -1R, TP1 = +1R, TP2 = +2R, TP3 = +3R (configurable in `config/signal_tracking.yaml`).

- `winrate_triggered = wins / triggered` — excludes signals that never filled.
- `capture_rate = triggered / total` — measures whether entries are realistic.
- `profit_factor = Σ(positive_R) / |Σ(negative_R)|`.
- `MFE_R / MAE_R` — max favorable / adverse excursion in R.
- Same-candle ambiguity (stop and TP touched in one OHLCV bar) is flagged separately. Default model is conservative: assume stop hit, mark ambiguous.

### Sample-size policy

| n signals | label | rule |
|---|---|---|
| < 10 | anecdotal | mention only, no conclusions |
| 10–29 | weak | weak observation |
| 30–49 | moderate | observation possible, manual approval required |
| 50–99 | stronger | rule-change *suggestions* allowed (manual approval) |
| 100+ | reliable | strong observation, manual approval still required |

### Safety guarantees

- `automatic_rule_changes: false` — hard-coded default, enforced regardless of sample size.
- `automatic_scoring_weight_changes: false` — same.
- Every observation in `signal-stats` and reviews carries `manual_approval_required: True`.
- The tracker's failure path is wrapped in try/except inside the supervisor — a broken tracker can never block report generation.

See `obsidian_vault/13_Debugging_and_Improvement/Signal_Tracking_and_Performance.md` and `obsidian_vault/15_LLM_Context/Signal_Performance_Checklist.md` for details.

## Stocks Module (US equities + indices)

The project also analyzes US stocks and major index/sector ETFs through a parallel pipeline that lives under `src/stocks/`. It is **fully isolated** from the crypto pipeline: separate agents, separate configs, separate scoring rules, separate reports, separate LLM packet.

### Asset class flag

Every signal, trade idea, news item, and event is tagged with `asset_class` (`crypto` or `stocks`). The schema migrated automatically — existing crypto rows are backfilled to `'crypto'`. Use the `--asset-class` flag where it matters:

```bash
python -m src.cli signal-stats --asset-class stocks
python -m src.cli prepare-analysis --asset-class stocks --mode intraday
python -m src.cli register-signals --asset-class stocks
```

Without the flag, behavior is unchanged (defaults to crypto).

### Data source (MVP)

[yfinance](https://github.com/ranaroussi/yfinance) — free, unofficial. Documented limits:
- 15m bars: max 60 days history per request
- 1h bars: max ~730 days
- 1d bars: years (effectively unbounded for our use)

Cache lives at `data/raw/stocks/{interval}/{SYMBOL}.csv`. Earnings calendar is `yfinance.Ticker.calendar` merged with the manual CSV at `data/manual/stocks/earnings_calendar.csv` (manual wins on conflicts).

### Configs

Edit these three YAMLs to tune the stocks pipeline:

- `config/stocks/universe.yaml` — symbol universe, sector ETF map, indices, per-mode timeframes, liquidity floors.
- `config/stocks/scoring.yaml` — component weights, regime/mode multipliers, caps, tier thresholds.
- `config/stocks/risk.yaml` — earnings windows per mode, regime rules, sector confirmation, gap rules, macro events.

### Agents (9 + base)

[src/stocks/agents/](src/stocks/agents/):

1. **StocksMarketRegimeAgent** — SPY/QQQ/IWM/DIA + VIX → bullish / risk_on / risk_off / chop / transition / high_volatility / low_volatility.
2. **SectorRotationAgent** — ranks XLK/SMH/XLF/etc by RS vs SPY → strong / mixed / weak.
3. **StockRelativeStrengthAgent** — per-symbol RS vs SPY, QQQ, and the symbol's sector ETF.
4. **EarningsRiskAgent** — active / next_session / this_week / safe, with mode-specific blocks for swing.
5. **CompanyNewsAgent** — pulls from shared `news_items` filtered by `asset_class`.
6. **StockTechnicalAgent** — mode-aware (intraday=15m/1h, swing=1h/1d, invest=1d/1wk) with EMA stack, ATR, prev-day H/L, VWAP, structured entry/invalidation/TP/RR.
7. **StockRiskAgent** — combines regime + sector + RS + earnings + structure into flags + penalty + blocks.
8. **StockScoringAgent** — applies base weights × mode_multipliers × regime_multipliers, then risk penalties and caps. Tiers at A=80, B=65, C=50.
9. **StockTradeIdeaAgent** — orchestrates the above into `TradeIdea` objects with `asset_class='stocks'`.

### Commands

```bash
# Pull yfinance OHLCV + earnings into local cache
python -m src.cli stocks-update-data --mode intraday

# Run a full report (saves Markdown under data/reports/stocks/{mode}/)
python -m src.cli stocks-intraday-report
python -m src.cli stocks-swing-report
python -m src.cli stocks-invest-report

# Earnings calendar scan (just the earnings agent)
python -m src.cli stocks-earnings-scan --mode swing

# Single-symbol deep debug (full chain, prints JSON)
python -m src.cli stocks-candidate-debug --symbol NVDA --mode swing

# Build the stocks LLM packet (separate from crypto packet)
python -m src.cli prepare-analysis --asset-class stocks --mode intraday
# -> writes data/processed/llm_stocks_packet.md

# Reuse existing signal tracker filtered to stocks
python -m src.cli signal-stats --asset-class stocks --period week
```

### LLM packet isolation

Stocks ideas use `data/processed/llm_stocks_packet.md`. Crypto ideas use `data/processed/llm_analysis_packet.md`. The two files never reference each other; the LLM context for stocks does not include crypto symbols or rules, and vice versa.

### Obsidian notes

Stock-specific rules and templates live under `obsidian_vault/16_Stocks/` (13 notes covering regime, sectors, earnings, scoring, risk, modes). The crypto notes (folders 00–15) are unchanged.

### What's intentionally **not** in the MVP

- Fundamental snapshot agent (revenue, EPS, margins, valuation) — `invest` mode currently relies on technicals + regime + sector alone.
- Options Greeks / IV — derivatives layer for stocks is not wired.
- Live macro calendar auto-fetch — fall back to `data/manual/stocks/macro_calendar.csv` (not auto-collected yet).
- Real-time intraday relative volume — placeholder weight of 0.5 in the scoring agent.

Adding any of these is additive — they don't require touching crypto code.

### Status

Stages 1–7 complete. Crypto pipeline is untouched and continues to run normally. 35/35 existing crypto tests pass after the asset_class migration; stocks pipeline runs end-to-end and produces A/B/C tier ideas registered into the shared signal tracker with `asset_class='stocks'`.

## Discipline Rules

The desk should be sharp, but it should also be annoying in the useful way:

- No hallucinated trades.
- No ideas without invalidation.
- No high confidence from incomplete data.
- No forced trades when the tape is messy.
- No chasing extended moves.
- Missing data must be named clearly.
- Fewer good ideas beats a pile of weak ones.

This is a research tool, not financial advice or an execution system.
