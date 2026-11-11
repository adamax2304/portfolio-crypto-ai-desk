# News/Catalyst Layer Hardening (2026-07-03)

**Scope:** ingest / diagnostics / advisory / shadow / UI visibility ONLY. No live, no auto-live,
no A/B trading-logic change, no score/tier/actionability change from news. Reliability + transparency
+ shadow evidence first.

## What was added

New package `src/news/`:
- **`source_health.py`** (item 1) — per-source OK/STALE/DEAD/DISABLED from `news_items` freshness vs
  `config/sources.yaml`; writes `reports/NEWS_SOURCE_HEALTH.md` + `data/diagnostics/news_source_health.json`.
  CLI `news-source-health`.
- **`edgar.py`** (item 2) — reliable SEC ingest via the official CIK map (SEC `company_tickers.json`)
  + `data.sec.gov/submissions/CIK….json`; normalizes 8-K/10-Q/10-K/S-1/S-3/424B/Form-4 into
  `news_items` (source=`SEC EDGAR`, event_type=`filing`, importance heuristic). CLI `sec-edgar-refresh`.
- **`advisory.py`** (items 3, 8) — display-only earnings risk (from `events`) + fresh SEC/legal +
  source-health warnings. Wired into stocks report + LLM packet. CLI `news-advisory`.
- **`providers.py`** (item 5) — Benzinga/Finnhub/Polygon/Tiingo adapter interface; disabled-with-reason
  when the API key env var is absent; never a hard failure; covered by source-health.
- **`symbol_audit.py`** (item 7) — match-rate by source, top unmatched high-importance headlines,
  asset_class cross-tag candidates. CLI `news-symbol-audit`.
- **`shadow_eval.py`** (item 9) — per-signal news tags → forward `paper_execution_r` edge (which tags
  help/hurt). CLI `news-shadow-eval`. Shadow/diagnostic only.

Config (`config/sources.yaml`):
- old generic `SEC EDGAR Filings` RSS **disabled** (0 rows) → replaced by `src/news/edgar.py`.
- press-release wires added (item 4): GlobeNewswire / PR Newswire / Business Wire (enabled, health-checked).
- exchange announcements (item 6): Bybit/OKX/MEXC added **disabled with reason** (no reliable public
  RSS — covered via telegram primaries) so source-health shows WHY, not silence.

Control-plane (`trading-desk-control`):
- `backend/app/news_health.py` + `GET /api/news-source-health` (reads the desk diagnostics JSON;
  read-only, `live_locked: true`).

## Source health (live)

- **DEAD (enabled but not writing):** `SEC EDGAR Filings` (old RSS, now replaced), `Reuters Business`,
  and 13 telegram channels (`DeItaone, PiQSuite, cnbci, bloomberg, forexlive, binance_announcements,
  Bybit_Announcements, MEXCEnglish, BWEnews, WuBlockchainEnglish, peckshield, RektHQ, ArkhamIntelligence,
  WatcherGuru, CoinTelegraph`), plus the 3 new PR wires (endpoints returned no data — need verification).
- **DEAD PRIMARY:** SEC-EDGAR-RSS + binance/Bybit/MEXC telegram + the 3 PR wires.
- **DISABLED (with reason):** `Coinbase Blog` (Cloudflare 403), Bybit/OKX/MEXC announcements (no RSS),
  8 optional_paid_sources, 4 structured providers (no API key).
- **Healthy (OK):** ~18 — RSS majors (CNBC, Yahoo, CryptoBriefing, CoinDesk, Cointelegraph, AMBCrypto,
  MarketWatch, Motley Fool, Benzinga, The Block, Decrypt, CryptoSlate, Binance Announcements) + the 3
  working telegram (`lookonchain, WalterBloomberg, zachxbt`).
- **SEC EDGAR (new ingest):** was 0 rows → **110 filings ingested** (28 in the last 72h); now writing.

## News volume + symbol match

- ~1.5k rows / 24h; **overall symbol match rate ≈ 17%** (many headlines land with
  `detected_symbols_json=[]` — the biggest mapping gap). Match rate varies a lot by source (CoinDesk
  ~52%, Seeking Alpha ~6%). 20 asset_class cross-tag candidates flagged (review-only, never auto-fixed).

## Shadow evidence (paper_execution_r)

- `had_fresh_news_24h` Δavg **−0.246R**, `had_primary_source_24h` Δavg **−0.245R** → current news tags
  do NOT improve edge (slightly negative). Direct evidence that news should stay **advisory**, not fed
  into score. Other tags (press/legal/earnings) lacked ≥10 paired samples — accumulate before judging.

## Advisory blocks added (display-only)
Stocks report + enriched packet now carry: earnings risk (today/tomorrow/24h + avoid/chase), fresh
SEC/legal filings, source-health warnings ("DEAD primary", "no fresh primary stock source").
Confirmed non-mutating: `changes_score=False`, `changes_tier=False`, `changes_actionability=False`.

## Confirmation
- **Live locked. A/B trading logic untouched. score/tier/actionability untouched by news.** All new
  code is read-model / ingest / advisory / shadow. Guardrail test asserts no write to
  proposed_signals/signal_outcomes/final_r and no order/live code.

## Next steps (not done, conservative)
- Verify/replace the 3 PR-wire RSS endpoints (currently return no data).
- Improve symbol match rate (17%): extend stocks entity aliases; company-name→ticker for headlines.
- Schedule `sec-edgar-refresh` + `news-source-health` in the default cycle (fail-open).
- Optional: wire a live provider once an API key exists (interface ready).
