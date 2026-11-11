# Agent Outputs Summary — 2026-05-25

This file inventories which agents fed today's three analyses and whether their output is meaningful or placeholder.

Sources inspected:
- `src/agents/*.py` (crypto agents)
- `src/stocks/agents/*.py` (stocks agents)
- The three reports + `data/processed/context_for_llm.md`

---

## CRYPTO — Scalp + Intraday (shared agent set)

| Agent | File | Output in today's reports | Verdict |
|-------|------|--------------------------|---------|
| **Supervisor** | `src/agents/supervisor.py` | Orchestrates all below; report saved | OK |
| **MarketRegimeAgent** | `src/agents/market_regime_agent.py` | "Label: transition", BTC=transition_up, ETH=range, breadth=65.5% (intraday) / 65.5% above EMA20 (scalp). Style: "selective only" | Meaningful, used for style gating |
| **MomentumScannerAgent** | `src/agents/momentum_scanner_agent.py` | Strongest/Weakest tables populated (RENDER 100.0, SAGA 99.4, etc.); volume tags applied | Meaningful |
| **TechnicalSetupAgent** | `src/agents/technical_setup_agent.py` | Entry zones, ATR-based stops, trend labels (uptrend/downtrend/range), setup_quality 0–100 | Meaningful per idea |
| **DerivativesAgent** | `src/agents/derivatives_agent.py` | Funding, OI 24h, long/short ratio, crowding label per symbol | Meaningful |
| **MultiExchangeDerivativesAgent** | `src/agents/multi_exchange_derivatives_agent.py` | Bybit/OKX cross-check table | Meaningful |
| **NewsAgent** | `src/agents/news_agent.py` | "Top news" list (Cointelegraph, Decrypt, CoinDesk, Binance Announcements); some test_source items leaked in | Mostly meaningful; **placeholders present** (MSTR/AAPL/NVDA test_source items from earlier seeding still surfacing) |
| **CatalystAgent** | `src/agents/catalyst_agent.py` | Per-symbol catalyst tags (BTC, ETH, BNB, XRP, SOL, DOGE) | Meaningful — but the symbols flagged with catalysts are NOT the same as the top-momentum names (RENDER, SAGA, NEAR, INJ, NIL get **no fresh catalyst** flag). Big-cap news without small-cap news is a known blindspot |
| **NarrativeAgent** | `src/agents/narrative_agent.py` | Heatmap: Memes 49, AI 48.5, RWA 29.5, L2/Gaming 3.3, DePIN 0.0 | Meaningful; coverage thin |
| **CrowdAttentionAgent** | `src/agents/crowd_attention_agent.py` | Stage labels (BTC=early_attention, rest=unknown), attention scores | Meaningful for BTC/ETH; mostly "unknown" elsewhere |
| **SocialAttentionAgent** | `src/agents/social_attention_agent.py` | Reddit mentions for BTC (15), ETH (8), SOL (1), BNB (1) | Thin but real |
| **MacroGeopoliticsAgent** | `src/agents/macro_geopolitics_agent.py` | Risk 35/100, 1 risk-off hit; macro headline "BTC to attack $80K shorts on Iran peace deal" | Meaningful but a single headline; not enough for real macro framing |
| **CoverageAuditAgent** | `src/agents/coverage_audit_agent.py` | Data Coverage section (binance_futures ok 29, rss_news ok 4, social_attention 3 live sources). Blindspots listed explicitly | Meaningful — and the agent **correctly admits** what is not connected |
| **RiskAgent** | `src/agents/risk_agent.py` | Risk penalty per idea (e.g. NIL -6.3) | Meaningful |
| **ScoringAgent** | `src/agents/scoring_agent.py` | Component breakdown per idea (market_regime, technical_setup, momentum, derivatives, catalyst_news, narrative, execution_quality, risk_penalty) | Meaningful, but components hover in narrow band today (most ideas score 50–60) |
| **TradeIdeaAgent** | `src/agents/trade_idea_agent.py` | C-tier watchlist with entry/invalidation/TPs/counter-thesis | Meaningful per idea |
| **CriticAgent** | `src/agents/critic_agent.py` | Counter-thesis text per idea | Output present but **templated/canned** — "broad tape is not decisive; momentum can mean-revert" appears verbatim across multiple ideas |
| **ReviewAgent** | `src/agents/review_agent.py` | Not visible in today's reports | Possibly only used by daily-report or review CLI |
| **ExchangeFusionAgent** | `src/agents/exchange_fusion_agent.py` | Multi-Exchange Confirmation table per ticker | Meaningful |
| **WatchlistMonitor** | `src/agents/watchlist_monitor.py` | Running (bt5hnm840 + bbr5v349e); ticks every 10m | Live, but no alert fired yet today (no B/A crypto) |
| **CrowdLeaderAgent** | `src/agents/crowd_leader_agent.py` | Crowd Attention Stages section | Meaningful but mostly "stage unknown" |
| **WeekendModeOverlay** | `src/analysis/weekend_mode.py` | NOT active (Monday) | OK — correctly inactive |

### Crypto agents that did NOT produce visible output today
- **ReviewAgent** — not called in scalp/intraday flow.

### Crypto agent flags
- **CriticAgent's counter-thesis is templated**. Every watchlist idea gets the same "broad tape is not decisive; momentum can mean-revert" sentence. It is filling a slot, not reasoning about each symbol.
- **News tagging miss**: the strongest movers (SAGA +37%, RENDER +9%, NEAR +9%, INJ +10%) have **no news catalyst flagged**, while the catalyst list is dominated by stale Cointelegraph "price prediction" articles for BTC/ETH/BNB/XRP. The catalyst pipeline is feeding off big-cap RSS only.

---

## STOCKS — Intraday

| Agent | File | Output in today's stocks report | Verdict |
|-------|------|--------------------------------|---------|
| **StocksMarketRegimeAgent** | `src/stocks/agents/market_regime_agent.py` | Label = bullish, VIX 16.64, breadth 100/100 (above EMA20 and EMA50), 4/4 indices uptrend | Meaningful, clean signal |
| **SectorRotationAgent** | `src/stocks/agents/sector_rotation_agent.py` | Strongest: SMH (+9.36% RS), XLK (+8.15%); Weakest: XLB, XLU, XLI | Meaningful |
| **StockRelativeStrengthAgent** | `src/stocks/agents/relative_strength_agent.py` | Per-symbol RS vs SPY 20d, RS vs sector ETF 20d (e.g. AMD +29.98%, LLY +16.04%) | Meaningful and well-used |
| **EarningsRiskAgent** | `src/stocks/agents/earnings_risk_agent.py` | "Earnings events tracked: 18" reported, but "Earnings lookup failed for: SPY, QQQ, IWM, DIA, SMH, XLK, XLF, XLE, XLY, XLV" — 404s; every idea's evidence section says "earnings:unknown" | **Partially broken** — index/ETF earnings 404s are expected (no earnings for ETFs), but every individual stock idea ended up with "earnings:unknown" too, which means the lookup table is not connecting actual ticker earnings to the per-symbol idea evidence |
| **CompanyNewsAgent** | `src/stocks/agents/company_news_agent.py` | AAPL: "share buyback" (test_source), NVDA: "beats earnings" (test_source), COIN: "record revenue" (test_source), MSTR: "buys more" (test_source) | **Placeholder data only** — all four entries are `test_source`. No real stocks RSS feeds are wired in. AAPL's idea uses this fake news as evidence ("1 news catalyst(s)") |
| **StockTechnicalAgent** | `src/stocks/agents/technical_agent.py` | Entry zone, invalidation, TP1/2/3, ATR-based stop per idea | Meaningful |
| **StockRiskAgent** | `src/stocks/agents/risk_agent.py` | Risk penalty per idea (-4.0 long, -12.0 short) | Meaningful, but the same `-4.0` for every long looks like a constant rather than per-symbol risk |
| **StockScoringAgent** | `src/stocks/agents/scoring_agent.py` | Score per symbol + tier mapping | Meaningful |
| **StockTradeIdeaAgent** | `src/stocks/agents/trade_idea_agent.py` | Final idea text per A/B with entry/invalidation/TP/counter-thesis | Meaningful but **counter-thesis is one-liner** ("earnings risk: unknown") for every idea |

### Stocks agent flags
- **`StockRiskAgent`** appears to apply a flat -4.0 to every long and -12.0 to every short. There is no per-symbol risk shading. Confirm by reading `src/stocks/agents/risk_agent.py` — but on the surface this looks like a placeholder penalty schedule, not real risk modeling.
- **`CompanyNewsAgent`** is consuming `test_source` items. Real Reuters / Benzinga / company filings are not wired.
- **`EarningsRiskAgent`** has 18 events tracked but every per-stock idea claims `earnings:unknown`. There is a wiring gap between the earnings calendar and the per-idea evidence builder.
- The stocks scoring funnel produced **8 A/B ideas vs 14 rejected** — a 36% pass rate. Given that the regime is loudly bullish (100% breadth, VIX 16) and counter-thesis is thin, this pass rate is high. With a less bullish tape, expect fewer ideas.

---

## Agents implemented but not used today

- **ReviewAgent** (crypto) — not invoked in scalp/intraday.
- **`update-obsidian-context`** CLI — is a TODO stub. So Obsidian's `Current_Context_For_LLM.md` was **never auto-refreshed** from any of today's reports. It is still a template file with placeholders.
- **`log-idea-to-obsidian`** / **`log-news-to-obsidian`** / **`review-day`** — all TODO stubs.

---

## Bridge to `news_trader`

- The crypto LLM packet does NOT show evidence of fresh `news_trader` Telegram items today. The packet's "KOL / Crowd Watch" section reads "Configured sources: Manual KOL notes, example_account. Manual signal count: 0. Symbols: none. No manual KOL/crowd notes found; X/Telegram/Discord context is not live yet."
- Either the bridge has no fresh items, or it ran but found nothing relevant — either way **no Telegram/external KOL signal influenced today's analyses**. The system is honest about this.

---

## Net assessment

- **All crypto agents fired and produced output**, but several are operating on thin or placeholder data (catalysts only for big-caps; templated counter-thesis; KOL placeholder).
- **All stocks agents fired**, but **CompanyNewsAgent + EarningsRiskAgent are placeholder-grade** today. The bullish regime + clean technical + RS leadership carried the analysis.
- The pipeline is structurally sound; the **inputs** are uneven.
