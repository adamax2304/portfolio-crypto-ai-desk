# Audit: crypto-ai-desk after stocks module integration

Date: 2026-05-25
Scope: every Stage 1–7 deliverable for the stocks module, plus regression surface for the existing crypto pipeline.
Method: filesystem inspection, code reading, SQLite state inspection, test run, smoke tests of every new CLI command. No code modified during this audit.

---

## 1. Current project structure

### Top-level
```
crypto-ai-desk/
├── config/             (10 crypto YAMLs + 1 new stocks/ subdir)
├── data/
│   ├── raw/            (crypto OHLCV in ohlcv/, stocks OHLCV in stocks/ NEW)
│   ├── processed/      (llm_analysis_packet.md crypto + llm_stocks_packet.md NEW)
│   ├── reports/        (daily/intraday/scalp/reviews + stocks/{mode}/ NEW)
│   ├── manual/         (events.csv crypto + stocks/earnings_calendar.csv NEW stub)
│   └── ...
├── obsidian_vault/     (15 crypto folders + 16_Stocks/ NEW with 13 notes)
├── prompts/system/     (crypto-only; no stocks-specific protocol added)
├── src/
│   ├── agents/         (22 crypto agents, untouched)
│   ├── analysis/       (packet builder for crypto, untouched)
│   ├── data_collectors/(15 crypto collectors, untouched)
│   ├── indicators/     (asset-agnostic, reused by stocks)
│   ├── reports/        (crypto report builder, untouched)
│   ├── notifiers/      (telegram, untouched)
│   ├── signals/        (asset_class param threaded through — backward compat)
│   ├── storage/        (asset_class column added to 7 tables)
│   ├── utils/          (untouched)
│   ├── stocks/         (NEW — 27 files)
│   │   ├── agents/                (9 agents + base)
│   │   ├── configs/loader.py      (reads config/stocks/*.yaml)
│   │   ├── data_collectors/       (yf_client, OHLCV, market_index, sector_etf, earnings)
│   │   ├── pipelines/stocks_pipeline.py
│   │   ├── reports/stocks_report_builder.py
│   │   ├── scoring/ pipelines/ prompts/  (empty placeholders for future)
│   │   └── llm_packet.py
│   ├── cli.py          (extended: 6 stocks commands + --asset-class flag on 3 existing)
│   ├── config.py       (crypto loader, untouched)
│   ├── models.py       (TradeIdea gained `asset_class` and `invest` mode)
│   └── ...
├── tests/
│   ├── (12 crypto tests, untouched, 35 pass)
│   └── stocks/         (NEW — 3 test files, 13 tests, all pass)
└── README.md           (extended with a Stocks Module section)
```

### File counts in the stocks module
- 27 Python files (~80 KB)
- 3 config YAMLs
- 13 Obsidian notes
- 3 test files (13 tests)
- 25 cached CSVs after the smoke test (1 mode × 12 sector ETFs + 5 indices + 4 mega-caps × 2 timeframes)
- 2 generated reports (intraday + swing)

### Database state (live)
After the Stage 5 smoke test the SQLite shows:
| table | crypto rows | stocks rows |
|---|---|---|
| proposed_signals | 1 | 3 |
| trade_ideas | 1042 | 3 |
| news_items | 206 | **0** ⚠ |
| events | 0 | 4 |
| rejected_ideas | 425 | 0 |
| watchlist_alerts | 16 | 0 |
| agent_runs | 10062 | 50 |

The "news_items has 0 stocks rows" is one of the audit findings — see §7.

---

## 2. Crypto system preservation

### Test surface
`python -m pytest tests/ -q` ⇒ **48 passed in 9.80s** (35 crypto + 13 stocks). No regressions.

### Existing crypto commands smoke-checked
- `monitor-watchlist --interval 600 --iterations 1` — still firing tier-change alerts, EDEN B-tier alert fired during this session. ✓
- `signal-stats` (no flag) — returns combined crypto + stocks rows; identical behavior for crypto by default since legacy NULLs are treated as `'crypto'`. ✓
- `signal-stats --asset-class crypto` — returns only crypto rows. ✓
- `intraday-report`, `update-data`, `prepare-analysis` (no flag) — code path unchanged.

### Files modified in the crypto tree
Only the following crypto-touching files changed during the stocks build:
- `src/storage/sqlite.py` — added `asset_class TEXT NOT NULL DEFAULT 'crypto'` to 7 CREATE TABLE statements; new `_migrate_asset_class` helper; new optional `asset_class` keyword on `save_*` and `load_*` methods. **All existing callers keep working** because the keyword defaults to `'crypto'`.
- `src/signals/models.py` — `ProposedSignal` gained `asset_class: str = "crypto"` field.
- `src/signals/registry.py` — added optional `asset_class` kwarg (defaults `'crypto'`) to `register_ideas`, `register_from_agent_output`, and `build_signal_from_idea`. Reads `idea.asset_class` if present.
- `src/signals/analytics.py` — added optional `asset_class` kwarg to `collect`, `compute_breakdowns`, `compact_packet_summary`.
- `src/models.py` — `TradeIdea` Pydantic model gained `asset_class: Literal["crypto", "stocks"] = "crypto"` and `mode` Literal expanded to include `"invest"`.
- `src/cli.py` — `--asset-class` added to `signal-stats`, `register-signals`, `prepare-analysis`; appended ~150 lines of stocks-specific commands at the end of the file.
- `README.md` — appended a Stocks Module section.

### Cross-import check
`grep -r "from src.stocks" src/agents src/data_collectors src/analysis src/reports src/storage src/indicators` ⇒ **zero matches.** No crypto module reaches into stocks. ✓

`src/cli.py` imports `src.stocks` only inside function bodies (`_build_stocks_pipeline` and the prepare-analysis stocks branch). yfinance is therefore never imported when running crypto-only commands. ✓

### Risk that stocks logic polluted crypto logic
- **Schema:** the migration adds a NOT NULL DEFAULT column. SQLite cannot enforce NOT NULL on legacy rows via ALTER, so the migration adds it nullable and backfills `'crypto'` — legacy rows are now non-NULL after migration. New rows from crypto paths use the DEFAULT `'crypto'`. **Low risk.**
- **Pydantic model:** adding fields with defaults is backward-compat. JSON deserialization from old `raw_idea_json` blobs still works (new fields default in).
- **Signal registry:** `register_ideas(..., asset_class="crypto")` is the new default; supervisor's auto-register call (which doesn't pass the kwarg) keeps producing crypto signals. **Verified live during this session — EDEN registered as crypto.**

### Broken imports?
None found. `python -c "from src.cli import app"` succeeds. `pytest` collects all 48 tests without error.

**Conclusion §2: Crypto pipeline is intact and untouched in spirit, even though the asset_class column was added schema-wide. No regression risk identified.**

---

## 3. Stocks module

### Files added (28 src files + configs + tests + docs)
See §1 tree.

### Agents implemented (all 9 + base)
| Agent | File | Status |
|---|---|---|
| StocksBaseAgent | agents/base.py | Done |
| StocksMarketRegimeAgent | agents/market_regime_agent.py | MVP |
| SectorRotationAgent | agents/sector_rotation_agent.py | MVP |
| StockRelativeStrengthAgent | agents/relative_strength_agent.py | MVP |
| EarningsRiskAgent | agents/earnings_risk_agent.py | MVP |
| CompanyNewsAgent | agents/company_news_agent.py | **Stub / partially broken** (see §6) |
| StockTechnicalAgent | agents/technical_agent.py | MVP |
| StockRiskAgent | agents/risk_agent.py | MVP |
| StockScoringAgent | agents/scoring_agent.py | MVP |
| StockTradeIdeaAgent | agents/trade_idea_agent.py | MVP |

Per-agent details in §6.

### Data collectors
| Collector | File | Source |
|---|---|---|
| StockOHLCVCollector | data_collectors/stock_ohlcv_collector.py | yfinance (CSV cache) |
| MarketIndexCollector | data_collectors/market_index_collector.py | yfinance via OHLCV collector |
| SectorETFCollector | data_collectors/sector_etf_collector.py | yfinance via OHLCV collector |
| EarningsCalendarCollector | data_collectors/earnings_calendar_collector.py | yfinance + manual CSV merge |
| yf_client | data_collectors/yf_client.py | shared retry/normalize layer |

### Data source for OHLCV
**yfinance ≥ 0.2.40.** Documented limits:
- 15m bars: max 60 days history per request.
- 1h bars: max ~730 days.
- 1d bars: years.
- Unofficial API; rate-limited; flakiness on indices like `^VIX` requires a `yf.download` fallback (implemented).

### Limitations (acknowledged in code and Obsidian)
- No paid-API support yet (Alpha Vantage / FMP / Finnhub / Polygon / Alpaca stubs not wired; `.env.example` for them not created).
- No options Greeks / IV data for stocks (crypto's "derivatives" layer has no stocks equivalent).
- No real-time intraday relative volume — scoring weight uses a hardcoded `0.5` placeholder.
- No macro calendar collector — `config/stocks/risk.yaml → macro.events_of_note` lists events but nothing is auto-fetched.
- No fundamental snapshot agent — invest mode is technicals + regime + sector only.
- No avg_dollar_volume_30d enforcement (config has the floor, code doesn't check).

### Isolation from crypto
- 100 % of stock-module imports stay within `src/stocks/*` or shared utilities (`src/indicators`, `src/storage`, `src/models`, `src/signals`, `src/utils`, `src/config`, `src/logger`).
- No `from src.agents.*` or `from src.data_collectors.*` import in any stocks file. ✓
- No stocks reference in any crypto agent / collector / scoring / report file. ✓

### Stocks configs present
- `config/stocks/universe.yaml` — symbols, indices, sector ETFs, sector map, per-mode timeframes, liquidity floors.
- `config/stocks/scoring.yaml` — weights, mode/regime multipliers, caps, tier thresholds.
- `config/stocks/risk.yaml` — earnings/regime/confirmation/liquidity/gap/macro/news rules.

All three loaded by `StocksConfig` (`src/stocks/configs/loader.py`).

---

## 4. Shared layer

### What is truly shared
- `src/storage/sqlite.py` — schema and CRUD for `trade_ideas`, `proposed_signals`, `signal_outcomes`, `news_items`, `events`, `rejected_ideas`, `watchlist_alerts`, `agent_runs`. Asset-class aware.
- `src/storage/file_store.py` — JSON / CSV file I/O.
- `src/indicators/technicals.py` (EMA, ATR, RSI, enrich_ohlcv, pct_return, recent_range) — used by stocks agents.
- `src/signals/{models,registry,tracker,analytics,obsidian_export}.py` — accept `asset_class` via kwarg.
- `src/utils/{symbols,formatting,validation,time}.py` — generic helpers.
- `src/config.py` — `load_yaml`, `PROJECT_ROOT`, `ProjectConfig` (crypto-flavored but the helper functions and root resolver are reusable by stocks).
- `src/models.py` — `TradeIdea` (carries asset_class), and a handful of crypto-flavored models that stocks does not use (`DerivativesSummary`, `CrowdAttention`, `SocialAttentionSummary`).
- `src/logger.py` — generic.

### Cleanliness
**`src/indicators/relative_strength.py` and `src/indicators/derivatives_metrics.py`** are crypto-only — they reference BTC/ETH and funding/OI semantics. They live under `src/indicators/` but are not generic. Stocks intentionally does NOT import them. They are not in the "true shared" layer despite their location. Cosmetic concern, not a bug.

**`src/models.py`** mixes asset-agnostic models (TradeIdea, NewsItem) with crypto-specific ones (DerivativesSummary, ExchangeConfirmation, CrowdAttention, SocialAttentionSummary, MomentumCandidate). Stocks pipeline only constructs TradeIdea. Cosmetic; safer than splitting models.py and risking import churn.

**`src/storage/sqlite.py`** has crypto-flavored columns on `proposed_signals` (`oi_context`, `funding_context`, `derivatives_supported`, `listed_exchanges_json`, `exchange_confirmation_type`). For stocks rows these are empty strings / 0 / `'unknown'` — schema works, semantics are wasted columns. Not a bug; a future cleanup item.

### Crypto-specific logic accidentally in shared?
- `src/models.MarketRegime` is BTC/ETH biased (`btc_trend`, `eth_trend`, `altcoin_breadth`). Stocks regime model is its own dataclass in `src/stocks/agents/market_regime_agent.py` — no overlap.
- `src/signals/registry._exchange_confirmation_type` is hardcoded for `{binance, bybit, mexc, mexc-only}` labels. For stocks signals it returns `"unknown"` (or `"Bybit"` if `exchange_focus="US"` happened to match — it does not). This is functional but produces an unhelpful label for stocks signals. **Low impact: stocks rows will have `exchange_confirmation_type='unknown'`.**

### Stocks-specific logic accidentally in shared?
None found.

### asset_class usage consistency
| Surface | Uses asset_class? | Notes |
|---|---|---|
| SQLite schema (7 tables) | ✓ | NOT NULL DEFAULT 'crypto', backfilled |
| `load_signals_for_period` | ✓ | filter param; treats NULL legacy as 'crypto' |
| `save_news_items` | ✓ kwarg | default 'crypto' |
| `save_events` | ✓ kwarg | reads event-level override first |
| `save_trade_ideas` | ✓ kwarg | reads idea.asset_class first |
| `save_rejected_ideas` | ✓ kwarg | |
| `record_watchlist_alert` | ✓ kwarg | |
| `save_agent_run` | ✓ kwarg | |
| `ProposedSignal` dataclass | ✓ field | default 'crypto' |
| `register_ideas` | ✓ kwarg | |
| `compute_breakdowns` | ✓ kwarg | |
| CLI `--asset-class` | ✓ on 3 commands | signal-stats, register-signals, prepare-analysis |
| RSS news collector | **✗** | always saves with default 'crypto' — see §7 finding |
| Watchlist monitor | **✗** | crypto-only by design (config/watchlist.yaml) |
| Signal tracker (tracker.py) | **✗** | **does not branch on asset_class for OHLCV lookup** — critical bug, see §6 / §11 |

---

## 5. Asset class separation

| Concern | Separated? | Notes |
|---|---|---|
| Signal table rows | ✓ | filtered queries respect asset_class |
| Signal-stats CLI | ✓ | `--asset-class stocks` returns stocks only |
| Reports | ✓ | `data/reports/stocks/{mode}/…` vs `data/reports/{daily,intraday,scalp,reviews}/…` |
| LLM packets | ✓ | `llm_analysis_packet.md` (crypto) vs `llm_stocks_packet.md` |
| Obsidian | ✓ | `obsidian_vault/16_Stocks/` is the only stocks folder |
| CLI commands | partial | crypto commands keep their names, stocks commands are prefixed `stocks-…`. `prepare-analysis` and `signal-stats` and `register-signals` are shared and take `--asset-class`. |
| Agent outputs | ✓ | stocks agents write `data/processed/agent_outputs/<stamp>_stocks_<name>.json` |
| OHLCV cache | ✓ | crypto at `data/raw/ohlcv/{exchange}/{tf}/`, stocks at `data/raw/stocks/{tf}/` |
| Events table | ✓ | stocks earnings events tagged asset_class='stocks' |
| News table | ✗ | RSS collector always tags 'crypto' — see §7 |
| Signal outcomes | ⚠ | tracker doesn't yet know to load stocks OHLCV — see §11 |

---

## 6. Stocks agents quality

### StocksMarketRegimeAgent — `agents/market_regime_agent.py`
- **Purpose:** classify the broad market regime from SPY/QQQ/IWM/DIA daily bars + VIX level.
- **Inputs:** cached 1d OHLCV for indices.
- **Outputs:** `{"regime": {label, bias, risk_on, high_volatility, breadth, vix_level, explanation}, "indices": [...]}`.
- **Implementation:** EMA20/EMA50 stack + slope direction → uptrend/downtrend/range per index. Aggregates to a label using simple thresholds (breadth ≥ 0.75 = bullish, etc.).
- **Limitations:**
  - Hardcoded VIX_HIGH=25.0 / VIX_LOW=14.0 with no calibration.
  - Heuristic NaN guard `if not series.iloc[-1] != series.iloc[-1]` is correct but stylistically dangerous — should be `pd.isna(...)`.
  - No detection of "narrow mega-cap rally" or "tech-led rally" sub-labels listed in the spec.
- **Production-ready?** MVP. Good enough for "bull / bear / chop / vol regime" filtering. **Not** good enough for regime-change detection or alpha edge.

### SectorRotationAgent — `agents/sector_rotation_agent.py`
- **Purpose:** rank sector ETFs by 20d RS vs SPY; tag strong / mixed / weak.
- **Inputs:** cached 1d OHLCV for each sector ETF (XLK/SMH/...).
- **Outputs:** ranked list of sector snapshots + top-3 strongest / bottom-3 weakest.
- **Limitations:** thresholds (+3 / -3) are arbitrary. Doesn't compute rolling sector momentum (would need rate-of-change of RS over time).
- **Production-ready?** MVP. Correctly identifies clearly strong/weak sectors; subtle rotation signals are missed.

### StockRelativeStrengthAgent — `agents/relative_strength_agent.py`
- **Purpose:** per-symbol RS vs SPY, QQQ, and configured sector ETF.
- **Inputs:** cached 1d OHLCV per symbol + benchmarks.
- **Outputs:** rows with rs_vs_spy_20d, rs_vs_qqq_20d, rs_vs_sector_20d, classification {leader / follower / laggard / weak / unknown}.
- **Limitations:**
  - Classification uses only index average (RS_SPY + RS_QQQ)/2 — sector RS is computed but unused in the classifier.
  - 5d and 20d only; no shorter (1d/3d) or longer (60d) windows.
  - Symbols with `sector='crypto_equity'` (COIN, MSTR) get empty `sector_etf` → `sector_r20=None` → `rs_vs_sector_20d=None`. Documented; scoring uses 'mixed' default for these.
- **Production-ready?** MVP. Reasonable for daily/swing decisions; thin for intraday rotation.

### EarningsRiskAgent — `agents/earnings_risk_agent.py`
- **Purpose:** classify days-until-earnings severity per symbol per mode.
- **Inputs:** list of `EarningsEvent`, target mode.
- **Outputs:** per-symbol severity (active / next_session / this_week / safe / unknown) + `blocks_swing` flag + `intraday_high_risk` flag.
- **Limitations:**
  - **`blocks_swing` is computed regardless of input mode** — it always means "swing would block this," not "the current mode blocks this." Tests assert this informational semantic, but downstream code (StockRiskAgent) only honors it when mode==swing, so the downstream effect is correct. Worth refactoring to two flags for clarity.
  - Trading-day vs calendar-day is conflated (`(target - today).days`). Friday earnings + Monday entry = `days_ahead=3` calendar, but the next trading session is just 1 trading day away.
  - `report_time` from yfinance is always `"unknown"` — yfinance doesn't expose BMO/AMC reliably. Manual CSV can fix it.
- **Production-ready?** MVP. Correct for the basic "is there earnings within N days" logic; trading-day awareness needed for production.

### CompanyNewsAgent — `agents/company_news_agent.py`  ⚠ partially broken
- **Purpose:** surface stock-relevant news hits per symbol.
- **Inputs:** shared `news_items` table.
- **Outputs:** `{symbols, hits_by_symbol, has_catalyst}`.
- **Bug #1:** the conditional `if asset_class != "stocks" and matched.isdisjoint(sym_set): continue` is dead code — `matched` is already `& sym_set`, so `matched.isdisjoint(sym_set)` is always False when matched is non-empty. The `continue` never fires. Effect: the agent includes any news row that mentions a tracked symbol regardless of asset_class. Not catastrophic; just muddled.
- **Bug #2 (more important):** **the RSS news collector never tags news as `asset_class='stocks'`.** The news_items table currently has 206 crypto rows and 0 stocks rows. The agent's hits dictionary is empty in practice because no RSS source is wired for stock-relevant feeds and the crypto feeds rarely mention stock tickers. The Stage 5 smoke test confirmed `has_catalyst: []`.
- **Production-ready?** No. Needs: (a) a stocks RSS source list, (b) the RSS collector to tag news with asset_class when the source is stocks-flavored, (c) richer classification (company / sector / index / analyst / earnings) which the spec called out but Stage 5 deferred.

### StockTechnicalAgent — `agents/technical_agent.py`
- **Purpose:** per-symbol mode-aware setup with entry zone, invalidation, targets, quality score.
- **Inputs:** cached OHLCV for the mode's exec + context timeframes.
- **Outputs:** TechnicalSetup dataclass per symbol.
- **Limitations:**
  - Hard-to-read NaN guard: `if not ema20_series.iloc[-1] != ema20_series.iloc[-1] else None`. **Functionally correct** (NaN != NaN is True → not True is False → returns None) but should use `pd.isna(...)`.
  - VWAP is a rolling 26-bar window (not session-anchored). Documented in module docstring and Obsidian.
  - Entry / invalidation / TP formulas are pure ATR multiples: no respect for prev-day H/L when picking stop levels (uses prev-day only for the quality_score bonus).
  - For `intraday` mode the exec_frame can be missing (15m bars not cached) — VWAP returns None silently. The chain still produces a setup using only the context (1h) frame.
- **Production-ready?** MVP. Good baseline setup generator; production should support: explicit support/resistance levels, structural stops (not just ATR offsets), VWAP truly anchored to session open.

### StockRiskAgent — `agents/risk_agent.py`
- **Purpose:** combine regime / sector / RS / earnings / structure into per-symbol flags + penalty + hard blocks.
- **Inputs:** all upstream agent payloads.
- **Outputs:** per-symbol assessment.
- **Limitations:**
  - Liquidity rule (`reject_if_relative_volume_lt`) is not enforced — no relative volume signal in the chain yet.
  - Gap rules (`require_retest_after_gap_pct`, `reject_chase_after_gap_pct`) are not enforced — no gap detection in the chain.
  - Macro rules (`block_new_entries_on_event_day`) are not enforced — no macro calendar collector.
  - Block label `earnings_today_blocks_swing` is only added when `mode=='swing'`. Other modes silently skip the block even if `severity=='active'`. This is intentional but worth surfacing in the report.
- **Production-ready?** MVP for what it covers. Three documented but unenforced rule families (liquidity floors, gap rules, macro) are real gaps.

### StockScoringAgent — `agents/scoring_agent.py`
- **Purpose:** aggregate component scores into a final 0–100 with tier + confidence.
- **Inputs:** all upstream payloads + risk payload.
- **Outputs:** scored rows with full component breakdown.
- **Limitations / placeholders:**
  - `volume_relative_volume` raw is **hardcoded to 0.5** (placeholder until a real intraday relative-volume metric is wired). Every symbol gets the same value; this component cannot discriminate today.
  - `earnings_risk_adjustment` raw is **hardcoded to 0.5** in the components. The real earnings effect comes from StockRiskAgent's `penalty`, which is applied after the components — so this component is decorative noise (worth ~5 points equally distributed).
  - `data_confidence` raw is **hardcoded to 0.8** for any setup. Doesn't reflect actual coverage (e.g. missing exec_frame for intraday).
  - Component values use a clamp formula `min(value, max_score * mode_mult * regime_mult)` that can produce a different effective ceiling per component depending on whether multipliers are >1 or <1. Works but subtle.
- **Production-ready?** MVP. Tiering is correct; component shaping is rough.

### StockTradeIdeaAgent — `agents/trade_idea_agent.py`
- **Purpose:** orchestrate scoring + upstream payloads into `TradeIdea` Pydantic objects with `asset_class='stocks'`.
- **Outputs:** `{ideas: [...], rejected_count}`.
- **Limitations:**
  - `exchanges_confirmed=["US"]` — placeholder. The model expects exchange-style labels (Binance/Bybit/MEXC for crypto). Stocks signals therefore look weird in `exchange_confirmation_type` analytics (`"unknown"`).
  - `risk_level` is read from the risk payload; if missing, defaults to `"medium"`. Pydantic does not validate this field's vocabulary.
- **Production-ready?** MVP.

---

## 7. Data collectors

### yfinance client (`yf_client.py`)
- Retries (default 2), throttles, falls back to `yf.download` if `Ticker.history` returns empty (helpful for `^VIX`).
- Multi-version compat (older yfinance returns DataFrame for `.calendar`, newer returns dict; both handled).
- Normalizes columns to lowercase `open,high,low,close,volume`.
- **Limitation:** no retry on HTTP 429 (rate limit) — first failure after retries returns None.
- **Limitation:** no cache TTL — `collect()` always re-fetches when called.

### StockOHLCVCollector
- Caches per-symbol CSVs to `data/raw/stocks/{interval}/{SYMBOL}.csv`.
- `load_cached` reads back with `parse_dates=True`.
- **Limitation:** no incremental updates — every collect rewrites the whole window for that interval.

### MarketIndexCollector
- Hardcodes `["1d", "1h"]` intervals when called from the pipeline. Fine for regime + sector RS.
- Includes `^VIX` by default.

### SectorETFCollector
- Pulls 1d only by default. Hardcoded.

### EarningsCalendarCollector
- Manual CSV (`data/manual/stocks/earnings_calendar.csv`) merged with yfinance per-symbol calendar; manual wins on (date, symbol) conflicts.
- `report_time` from yfinance is always `"unknown"` — manual CSV can override.
- **Bug-light:** the manual CSV stub is just headers + comment lines; running `EarningsCalendarCollector.load_manual()` on a fresh repo silently returns no events. Documented but worth noting that the file feels empty by default.

### Rate limits / missing-data handling
- Per-call `retries=2`, `sleep_between=0.4s`, `throttle_seconds=0.5` between symbols.
- Failed fetches go to `summary.failed[key]` with the error string — preserved and surfaced in the report's Section 0 (Data Coverage) and in the CLI output.
- The chain tolerates missing data: agents that don't see cached frames silently skip the symbol. No exception propagates up.

### Data confidence warnings
- The scoring agent's `data_confidence` component is hardcoded 0.8 regardless of actual coverage. **It does not reflect missing intraday frames, stale data, or stocks with thin history.** This is a real correctness gap — `data_confidence` is decorative today.

---

## 8. Scoring and risk logic

### Stocks scoring config (`config/stocks/scoring.yaml`)
- Base weights total 100 before penalties.
- Mode multipliers per component per mode (intraday/swing/invest).
- Regime multipliers per regime per component (8 regime labels supported).
- Caps for partial-data / earnings-active / macro-event-today scenarios.
- Tier thresholds A=80, B=65, C=50.

### Stocks risk config (`config/stocks/risk.yaml`)
- Earnings rules per mode.
- Regime rules (risk_off / bullish / chop / high_volatility).
- Confirmation rules (index contradicts, sector contradicts, both).
- Liquidity floors.
- Structure rules (min RR, max-ATR-from-entry).
- Gap rules.
- Macro rules.
- News reliability gates.

### A/B/C/rejected classification
- A ≥ 80, B ≥ 65, C ≥ 50, rejected otherwise.
- Forced rejection if `blocks` list non-empty.
- Caps applied before tiering.

### Earnings effect
- Applied twice: once as risk_penalty (StockRiskAgent), once as decorative component (StockScoringAgent's earnings_risk_adjustment raw=0.5).
- Hard blocks at `days_ahead ≤ 2` for swing mode (configurable).

### Sector / index confirmation
- Sector status (strong/mixed/weak) read from SectorRotationAgent.
- Index status read from RS rows (rs_vs_spy_20d sign).
- "Both contradict → reject" rule is configured but **not implemented** — no check in StockRiskAgent or StockScoringAgent that detects the both-contradict case and forces rejection.

### Relative strength logic
- Computed once (StockRelativeStrengthAgent) → used by scoring (`relative_strength` component) + risk (`weak_relative_strength` penalty).

### Volume logic
- **Not implemented.** Placeholder `0.5` raw in scoring. No relative-volume collector exists.

### Invalidation and RR logic
- ATR-based: invalidation = entry ± 1 ATR, TP1 = entry ± 1.5 ATR.
- Min RR check (`require_rr_to_tp1_gte: 1.5` in risk.yaml) is enforced by StockRiskAgent → penalty `-4` if below.
- Missing invalidation → hard block `no_invalidation`.

### Separation from crypto scoring
- 100% separate — different config files, different agent classes, different weights, no shared scoring code path.
- No funding/OI/derivatives references in stocks scoring. ✓

---

## 9. CLI commands

### Crypto commands (existing, untouched)
| Command | Status | Notes |
|---|---|---|
| update-data | works | |
| daily-report / intraday-report / scalp-report / swing-report | works | |
| auto_universe_report | works | |
| scan-universe / rank-candidates | works | |
| candidate-debug | works | |
| monitor-watchlist | works | live during this session |
| review / idea | works | |
| status / doctor / latest / ask | works | |
| weekend-status | works | |
| telegram-setup / telegram-test | works | |
| log-idea / log-news / update-obsidian-context / review-day | TODO stubs | unchanged from before |

### Shared commands (asset_class-aware)
| Command | Flag default | Tested |
|---|---|---|
| signal-stats `--asset-class {crypto, stocks}` | none = all | ✓ both values smoke-tested |
| register-signals `--asset-class {crypto, stocks}` | crypto | crypto path tested (existing); stocks path tested via pipeline auto-register |
| prepare-analysis `--asset-class {crypto, stocks}` | crypto | ✓ both branches smoke-tested |

### Stocks commands (new)
| Command | Status | Tested | Expected output | Known limitation |
|---|---|---|---|---|
| stocks-update-data | works | ✓ | summary line + failures | re-fetches earnings even on update-data; no incremental fetch |
| stocks-intraday-report | works | ✓ | report path + tier counts | reports for empty intraday cache fall back to context frame (1h); doesn't warn |
| stocks-swing-report | works | ✓ | report path + tier counts | |
| stocks-invest-report | works | not smoke-tested in this session | report path + tier counts | invest mode is technicals-only |
| stocks-earnings-scan | works | ✓ | severity table | report_time always "unknown" from yfinance |
| stocks-candidate-debug | works | ✓ | full chain JSON for one symbol | re-runs full pipeline for one symbol — slow |

### Signal-tracking commands
| Command | asset_class aware? | Notes |
|---|---|---|
| register-signals | ✓ | flag works |
| active-signals | ✗ | no filter; returns all open signals |
| signal-detail | ✗ | single-ID lookup, doesn't care |
| track-signals | **✗ Critical** | does NOT branch on asset_class; loads OHLCV from `data/raw/ohlcv/{exchange}/{tf}/` which has no stocks data → stocks signals will be skipped_no_ohlcv forever. See §11. |
| signal-stats | ✓ | flag works |
| review-signals | ✗ | no filter |

### Obsidian commands
- `log-idea-to-obsidian`, `log-news-to-obsidian`, `update-obsidian-context`, `review-day` — all are TODO stubs from before the stocks work and remain TODO. Not stocks-aware.

---

## 10. LLM context

### Files
- `data/processed/llm_analysis_packet.md` — crypto. Built by `src/analysis/packet.py`.
- `data/processed/llm_stocks_packet.md` — stocks. Built by `src/stocks/llm_packet.py`.

### Stocks packet contents
- Read-me-first guardrails (no crypto symbols, index direction is first-class, earnings risk overrides, yfinance is best-effort).
- Latest stocks report (first 6000 chars of the most recent `data/reports/stocks/{mode}/*.md`).
- Latest agent outputs (trade idea, scoring, regime, sector rotation) — truncated to 4000 chars each.
- Stocks signal performance (compact summary from `compact_packet_summary(asset_class='stocks')`).
- Upcoming earnings (next 7 days) from events table filtered to stocks.
- Stocks scoring & risk rules summary.
- Pre-output checklist.

### Crypto packet contents (unchanged)
The crypto packet has not changed shape. It does not include any stocks references.

### Pollution check
- Crypto packet: read top to bottom, found 0 stocks references. ✓
- Stocks packet: read top to bottom, found 0 crypto references. ✓
- Both packets include independent "read me first" sections that reinforce isolation.

### Information density
- The stocks packet bundles ~3 JSON snippets (trade idea, scoring, regime, sector) at 4000 chars each + a 6000-char report excerpt. Total length is moderate. **No risk of overload** for a frontier LLM.
- **Missing:** Obsidian rules / template excerpts. The crypto packet pulls excerpts from `obsidian_vault/10_Trade_Idea_Format` and `obsidian_vault/03_Risk_Management`. The stocks packet **does not** pull from `obsidian_vault/16_Stocks/`. The LLM gets a "rules summary" inline but not the actual Obsidian notes. Worth wiring before production use.

---

## 11. Signal tracking

### Stocks signals registered with asset_class
- Verified live: 3 stocks rows in `proposed_signals` after Stage 5 smoke test (AAPL, TSLA, plus a re-registration). All carry `asset_class='stocks'`.
- The stocks pipeline calls `register_ideas(..., asset_class='stocks')` after producing TradeIdea objects.

### Crypto / stocks stats separation
- `signal-stats --asset-class stocks` returns 2-3 stocks rows.
- `signal-stats --asset-class crypto` returns crypto rows (+ legacy NULLs treated as crypto).
- `signal-stats` (no flag) returns the union.

### A/B saved correctly
- Confirmed in DB inspection.

### Performance stats can filter
- ✓ via `--asset-class`.

### **Critical bug: tracker.py is not asset_class-aware**

`src/signals/tracker.py` is the module that reads cached OHLCV bars and updates `signal_outcomes` (entry triggered, stop hit, TP hit, MFE, MAE, final_R). It calls:

```python
frame = file_store.load_ohlcv(exchange, symbol, tf)
```

`file_store.load_ohlcv` looks under `data/raw/ohlcv/{exchange}/{tf}/{SYMBOL}.csv`. For a stocks signal:
- `exchange = idea.exchange_focus = "US"` (per StockTradeIdeaAgent) — no such directory exists.
- Even if it did, the stocks bars are at `data/raw/stocks/{tf}/{SYMBOL}.csv`, not `data/raw/ohlcv/US/{tf}/`.

Result: every stocks signal will increment `skipped_no_ohlcv` and never get an outcome computed. `signal-stats --asset-class stocks` will perpetually show sample=N, triggered=0, wins/losses/amb=0, avgR/totalR=None.

**Severity: Critical.** Stocks signals are persisted but cannot be evaluated. The whole feedback loop is broken until tracker.py learns to route based on asset_class.

### Tracker doesn't break crypto
The bug is asymmetric: tracker.py works correctly for crypto signals (it always has). The stocks path silently fails because no exception is raised; the signals just stay open until `expires_at`.

---

## 12. Obsidian

### Stock-specific notes added
13 notes in `obsidian_vault/16_Stocks/`:
- README, Stock_Market_Overview, Stock_Market_Regime, Sector_Rotation, Earnings_Risk, Stock_News_Analysis, Stock_Technical_Setups, Stock_Scoring, Stock_Risk_Management, Stock_Trade_Idea_Template, Stock_Intraday_Mode, Stock_Swing_Mode, Stock_Invest_Mode.

### Separation from crypto rules
- All stocks notes are under `16_Stocks/`. Crypto folders 00–15 are unchanged.
- Stocks templates reference `asset_class: stocks` explicitly.

### LLM operating instructions
- The existing crypto operating protocols in `prompts/system/` (9 protocol files) are **not updated** to mention asset_class separation. An LLM running the crypto workflow would not know the stocks module exists from those files alone.
- `obsidian_vault/15_LLM_Context/` has system prompt + checklists for the crypto workflow. **No equivalent stocks LLM context document was added.** The stocks LLM packet embeds its own checklist inline, which works for one-shot use but doesn't carry forward into multi-turn LLM sessions.

### Signal performance & journal
- Crypto signal performance docs in `obsidian_vault/11_Trade_Journal/Signal_Performance/` are unchanged.
- **No stocks equivalent** of the Trade_Journal / Signal_Performance folder was created. Stocks signal outcomes would (if tracker.py worked) need a place to live.

---

## 13. Tests and smoke checks

### Tests added (13 in `tests/stocks/`)
- `test_stocks_config.py` — 6 tests: loader basics, sector map, timeframes per mode, weights, multipliers, risk rules.
- `test_stocks_earnings_agent.py` — 4 tests: swing blocks within 2 days, intraday warns, unknown symbol, picks-nearest-future.
- `test_stocks_scoring_and_ideas.py` — 3 tests: A/B for clean long, rejected when no invalidation, TradeIdea produces asset_class=stocks.

### Tests missing
- StocksMarketRegimeAgent — no unit test; only smoke-tested via end-to-end run.
- SectorRotationAgent — no unit test.
- StockRelativeStrengthAgent — no unit test.
- CompanyNewsAgent — no unit test (and has bugs §6).
- StockTechnicalAgent — no unit test for the setup formulas, NaN guard, VWAP fallback.
- StockRiskAgent — no unit test for individual flag/penalty triggers (only tested transitively via scoring tests).
- StocksPipeline — no test (entire orchestrator only smoke-tested).
- yf_client — no test (network-dependent; needs mocking).
- StockOHLCVCollector cache round-trip — no test.
- EarningsCalendarCollector manual CSV parsing — no test.
- StocksReportBuilder Markdown output — no test.
- Stocks LLM packet builder — no test.

### Commands smoke-tested in the build session
- `stocks-update-data` (implicit via pipeline)
- `stocks-intraday-report` ✓
- `stocks-swing-report` ✓
- `stocks-earnings-scan` ✓
- `stocks-candidate-debug` ✓
- `prepare-analysis --asset-class stocks` ✓
- `signal-stats --asset-class stocks` ✓
- `signal-stats --asset-class crypto` ✓
- `signal-stats` (no flag) ✓

### Commands NOT smoke-tested
- `stocks-invest-report` — code path exists but never run end-to-end in this session.
- `register-signals --asset-class stocks` — only tested via the pipeline's auto-register; the explicit CLI was not invoked.
- `track-signals` against stocks signals — would expose the §11 bug if run.

### Failing tests
None. 48/48 pass.

### Untested critical paths
- The track-signals path for stocks — **broken**, see §11.
- Sad path: yfinance returns empty for a sector ETF — agent silently skips. Not asserted in a test.
- Sad path: corrupted CSV cache.
- The `intraday` mode end-to-end with real 15m bars cached.

---

## 14. Risk assessment

### Overall rating: **Medium**

The crypto pipeline is unaffected (verified). The stocks pipeline runs end-to-end and produces tier-labeled ideas. The high-risk surface is:
- The signal tracker can't compute outcomes for stocks (no feedback loop).
- Several scoring components are placeholder values (volume, earnings adjustment, data confidence).
- News flow into the stocks side is dry (no RSS source produces stocks-tagged rows).
- Multiple documented rules (gap, liquidity floors, macro events) are configured but not enforced.

### Individual issues (classified)

| # | Severity | Issue | Location |
|---|---|---|---|
| 1 | **Critical** | `track-signals` does not branch on asset_class — stocks signals never get outcomes. | `src/signals/tracker.py` |
| 2 | **High** | RSS news collector never tags news with `asset_class='stocks'`; news_items has 0 stocks rows. | `src/data_collectors/rss_news_collector.py:91` |
| 3 | **High** | `StockScoringAgent.volume_relative_volume` is hardcoded 0.5 (no real relative-volume signal). | `src/stocks/agents/scoring_agent.py` |
| 4 | **High** | `StockScoringAgent.data_confidence` is hardcoded 0.8 (no coverage check). | same |
| 5 | **High** | Configured "both index AND sector contradict → reject" rule is **not implemented** in code. | `src/stocks/agents/risk_agent.py` and scoring |
| 6 | **High** | Gap rules (`require_retest_after_gap_pct`, `reject_chase_after_gap_pct`) are configured but not enforced. | `src/stocks/agents/risk_agent.py` |
| 7 | **High** | Liquidity floor (`min_avg_dollar_volume_30d`, `reject_if_relative_volume_lt`) is configured but not enforced. | same |
| 8 | **Medium** | `CompanyNewsAgent` has dead conditional (`matched.isdisjoint(sym_set)` always False). | `src/stocks/agents/company_news_agent.py` |
| 9 | **Medium** | `EarningsRiskAgent.blocks_swing` is always computed regardless of input mode — easy to misread. | `src/stocks/agents/earnings_risk_agent.py` |
| 10 | **Medium** | Macro calendar collector missing; macro rules silently inert. | (collector absent) |
| 11 | **Medium** | `StockTechnicalAgent` NaN guard `not x != x` is correct but unreadable; use `pd.isna()`. | `src/stocks/agents/technical_agent.py` |
| 12 | **Medium** | VWAP is rolling-26-bar, not session-anchored. | same |
| 13 | **Medium** | `EarningsCalendarCollector` always sets `report_time='unknown'` from yfinance. | `src/stocks/data_collectors/earnings_calendar_collector.py` |
| 14 | **Medium** | `EarningsRiskAgent` uses calendar days, not trading days (Friday → Monday counts as 3, not 1). | `src/stocks/agents/earnings_risk_agent.py` |
| 15 | **Medium** | Signal tracker validity windows (24h intraday, 168h swing) are crypto-tuned; do not account for market-closed hours. | `src/signals/config.py` |
| 16 | **Medium** | `StocksPipeline.run_report` fetches earnings twice (once in update_data, once at the chain start). | `src/stocks/pipelines/stocks_pipeline.py` |
| 17 | **Medium** | LLM stocks packet does not pull excerpts from `obsidian_vault/16_Stocks/`. | `src/stocks/llm_packet.py` |
| 18 | **Medium** | `prompts/system/` protocols are not updated to mention asset_class separation. | `prompts/system/` |
| 19 | **Medium** | No stocks equivalent of `obsidian_vault/11_Trade_Journal/Signal_Performance/`. | obsidian_vault |
| 20 | **Low** | No `.env.example` for the spec's paid-API keys (ALPHA_VANTAGE / FMP / FINNHUB / POLYGON / ALPACA). | repo root |
| 21 | **Low** | No `FundamentalSnapshotAgent` — invest mode is technicals-only. | (agent absent) |
| 22 | **Low** | COIN/MSTR have sector `crypto_equity` with no ETF; sector RS is always None for them. | `config/stocks/universe.yaml` + scoring |
| 23 | **Low** | `report_time='unknown'` is rendered as 'unknown' in the report (cosmetic). | report builder |
| 24 | **Low** | `_market_session_label` does not respect DST (EST vs EDT). | `src/stocks/reports/stocks_report_builder.py` |
| 25 | **Low** | Several `src/stocks/{scoring, pipelines, prompts, reports}/__init__.py` are empty placeholders. | various |
| 26 | **Low** | `src/indicators/relative_strength.py` and `derivatives_metrics.py` are crypto-specific but live in the generic indicators folder. | `src/indicators/` |
| 27 | **Low** | `data/manual/stocks/earnings_calendar.csv` ships with only headers + comments. | data/manual |
| 28 | **Low** | `proposed_signals` table carries crypto-only columns (`oi_context`, `funding_context`, `derivatives_supported`) that are wasted for stocks rows. | `src/storage/sqlite.py` |
| 29 | **Low** | yfinance is unofficial / rate-limited / no 429 handling. | `src/stocks/data_collectors/yf_client.py` |

---

## 15. Recommended next steps

### Must fix now (Critical / High)
1. **Make `track-signals` asset_class-aware (issue #1).** Branch on `asset_class` in `tracker.py` to select the cache path:
   - `crypto` → `data/raw/ohlcv/{exchange}/{tf}/{SYMBOL}.csv` (existing)
   - `stocks` → `data/raw/stocks/{tf}/{SYMBOL}.csv` (new)
   Update `_load_ohlcv_for_signal` to read the signal row's `asset_class` and route accordingly. Without this, stocks signal analytics is permanently empty.
2. **Wire stocks RSS sources or tag company news (issue #2).** Either add a stocks-specific RSS source (e.g. Seeking Alpha, MarketWatch headlines) and tag at insert time, OR have CompanyNewsAgent be more generous by matching ticker-only on crypto-tagged news. Without this, the `news_catalyst` weight does nothing.
3. **Compute real `volume_relative_volume` (issue #3).** Add a rolling 20-bar volume baseline per symbol on the exec timeframe; expose ratio to the scoring agent.
4. **Compute real `data_confidence` (issue #4).** Check what frames are present per symbol; reflect missing intraday cache or short history.
5. **Implement the "both contradict → reject" rule (issue #5).** Add the check in StockRiskAgent → add `both_contradict_reject` to the blocks list when active.

### Should fix soon (Medium)
6. Implement gap detection + apply `require_retest_after_gap_pct` / `reject_chase_after_gap_pct` (#6).
7. Enforce liquidity floors (#7) — compute avg_dollar_volume_30d (close × volume) and reject below floor.
8. Clean up `CompanyNewsAgent` dead conditional and document classification roadmap (#8).
9. Split `EarningsRiskAgent.blocks_swing` into a per-mode `blocks` list to make the semantic explicit (#9).
10. Add a macro calendar collector or document the manual-only path (#10).
11. Replace `not x != x` NaN guards with `pd.isna()` (#11).
12. Tune signal validity windows for stocks (e.g. 8h intraday accounting for market hours) (#15).
13. De-duplicate the earnings fetch in `StocksPipeline.run_report` (#16).
14. Wire `obsidian_vault/16_Stocks/` excerpts into the stocks LLM packet (#17).
15. Update `prompts/system/` to reference asset_class separation; add a stocks-specific protocol document (#18).
16. Mirror `11_Trade_Journal/Signal_Performance/` under `16_Stocks/` for stocks-tracked outcomes (#19).
17. Add unit tests for: market regime classification thresholds, sector rotation thresholds, technical agent setup formulas, risk agent flag accumulation, yf_client.fetch_calendar parsing both DataFrame and dict shapes (mocked).
18. Add a sad-path test: tracker.py with a stocks signal but no stocks OHLCV cache → should not throw.

### Nice to have later (Low)
19. Add `.env.example` with the spec's paid API key stubs (#20).
20. Build `FundamentalSnapshotAgent` for invest mode (#21).
21. Decide on a benchmark ETF for crypto-equity bucket (e.g. compare COIN/MSTR vs BITQ) (#22).
22. Add DST awareness to the market-session label (#24).
23. Refactor `src/indicators/` to split crypto-specific helpers into `src/indicators/crypto/` or move them under `src/agents/_crypto_helpers/` (#26).
24. Consider splitting `proposed_signals` columns: keep `oi_context`/`funding_context`/`derivatives_supported` in a side table or `raw_idea_json` instead of as flat columns (#28).
25. Wrap yfinance calls with proper 429 / rate-limit handling and TTL caching (#29).
26. Add real entries to `data/manual/stocks/earnings_calendar.csv` for live use (#27).

---

## Honest one-liners

- **Crypto pipeline:** not regressed, not at risk. 35/35 tests still pass; live monitor still firing alerts.
- **Stocks pipeline:** runs end-to-end, produces tiered ideas, registers signals, builds reports and packets. **But the signal feedback loop is broken until tracker.py learns about stocks paths.**
- **Scoring quality:** acceptable as a screening tool, **not** acceptable for real-money decisions — three of ten components are placeholder values today.
- **News coverage for stocks:** effectively zero. The pipeline runs but news_catalyst always reads as 0.
- **Documented but unenforced:** gap rules, liquidity floors, macro events, "both contradict → reject."
- **MVP-level overall.** Everything in the spec exists in name or shape; about a third is placeholder or unenforced.
