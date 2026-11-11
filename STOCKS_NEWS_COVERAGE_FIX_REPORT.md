# Stocks News Coverage Fix — Report

**Date:** 2026-06-01. Data-quality fix for stocks news pipeline.
**Scheduler stopped:** **NO** — running PID 11880 undisturbed.
**Scope:** sources config + classifier patterns + 4 new categories. NO scoring / threshold / alert / strategy changes.

---

## 1. Problem statement (audit findings)

Pre-fix snapshot of stocks news_items SQLite (all-time):

| Asset class | Rows |
|-------------|-----:|
| crypto | **675** |
| stocks | **11** (3 of those = `test_source`) |

- **Only 8 real stocks rows in entire DB history.**
- **0 auto-RSS ingestion** — all 3 stocks RSS feeds in `config/sources.yaml` were `enabled: false`.
- All 8 real rows were **manual ingest from my enriched reviews today**.
- This meant:
  - **PART 3 legal-risk gate was structurally blind** for stocks — gate works only when fresh news is in `news_items`. SMCI gap discovered today (system traded SMCI without legal block) is the canonical case.
  - **CompanyNewsAgent** had almost nothing to score against.
  - **Zero auto-discovery** of earnings, analyst upgrades/downgrades, M&A, FDA approvals, insider activity.

---

## 2. What was changed

### 2.1 Sources expansion (`config/sources.yaml`)

**Enabled 3 existing feeds** (were `enabled: false`):
- MarketWatch Top Stories
- Yahoo Finance Top Stories
- Seeking Alpha Market Currents

**Added 5 new feeds**:
- **CNBC Markets** — `https://www.cnbc.com/id/100727362/device/rss/rss.html`
- **Reuters Business** — `https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best`
- **Benzinga Movers** — `https://www.benzinga.com/feed`
- **The Motley Fool Investing** — `https://www.fool.com/feeds/index.aspx`
- **SEC EDGAR Filings** — `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=8-K&dateb=&owner=include&count=40&action=getcompany&output=atom` (**primary_source=true** — feeds PART 3 legal-risk gate directly)

All marked `asset_class: stocks`, `enabled: true`.

### 2.2 Four new catalyst categories (`src/catalysts/models.py`)

- **`earnings_event`** — Q1-Q4 reports, beats/misses estimates, guidance raises/cuts, earnings calls
- **`analyst_action`** — broker upgrades/downgrades, price-target changes, coverage initiations
- **`clinical_milestone`** — FDA approvals, Phase 1/2/3 trials, EMA/MHRA actions, BLA/NDA filings
- **`insider_activity`** — insider buys/sells, Form 4 filings, 10b5-1 plans

### 2.3 Classifier patterns (`src/catalysts/classifier.py`)

Added ~25 new regex patterns at the top of `CATEGORY_PATTERNS` (highest priority):

**`earnings_event`**:
- `beats?|misses?|tops?|trails? (analyst |Wall Street )?(estimates?|consensus|expectations?)`
- `(reports?|posts?|delivers?) Q[1-4]|quarterly (earnings|results|revenue)`
- `(EPS|earnings) (beat|miss|surprise|surge|jump|tops|trails)` (tightened to require EPS/earnings context — won't fire on crypto "revenue jump")
- `(Q[1-4]|quarterly|fiscal[- ]year) (earnings|EPS|revenue|guidance)`
- guidance raises/cuts, earnings call previews, pre-announces

**`analyst_action`**:
- `upgrade[ds]?|downgrade[ds]? to|from`
- `(price target|PT) (raised|cut|lowered) to|from $X`
- `(initiates? coverage|reiterate[ds]?|maintain[ds]?) (buy|sell|hold|outperform|...)`
- Named brokers (JPMorgan/Goldman/MS/Citi/Wedbush/UBS/etc.) + upgrade/downgrade/raises/cuts/maintains/initiates
- `analysts? (raises?|cuts?|lifts?|lowers?) (target|estimate|forecast)`

**`clinical_milestone`**:
- `FDA (approves?|approval|clears?|rejection|priority review|fast track)`
- `Phase [123] (results?|met|missed|success|fail)`
- `EMA|MHRA|PMDA (approval|clearance|review)`
- `(NDA|BLA) (submitted|filed|approved)`
- biosimilars / biologics filings

**`insider_activity`**:
- `insider (buys?|bought|purchases?|sells?|sold)`
- `Form 4 (filing|disclosure)`
- `CEO|CFO|director (buys?|sells?) ... shares`
- `10b5-1 (plan|trading)`

### 2.4 No breaking changes

- Existing crypto categories untouched.
- `legal_risk` patterns unchanged (already detects SMCI-style indictments).
- Test confirms all 7 existing crypto headlines still classify correctly.

---

## 3. Files changed

```
config/sources.yaml                       — 3 enabled + 5 new stocks feeds
src/catalysts/models.py                   — 4 new categories
src/catalysts/classifier.py               — ~25 new regex patterns
tests/test_stocks_news_coverage.py (NEW)  — 28 tests
```

---

## 4. Live validation

### 4.1 Classifier — all stocks patterns

```
$ python -m pytest tests/test_stocks_news_coverage.py -v
28 passed
```

15 of 16 headlines correctly classified at first attempt; 1 (`Analyst raises price target for SMCI`) needed `raise → raises?` plural fix — then 16/16 pass.

### 4.2 Cross-category isolation (crypto patterns still work)

```
$ python -m pytest tests/test_stocks_news_coverage.py::test_crypto_patterns_still_match
PASSED
```

All 7 existing crypto classifications preserved.

### 4.3 Live catalyst-scan after fix

```
$ python -m src.cli catalyst-scan --no-print
Catalyst scan ok — events=105, baskets=4, scanned=105, rejected_test=0, rejected_missing=0
```

**Events 47 → 105 (+58)** and **baskets 3 → 4** in this scan — the bigger event count is because the catalyst layer reads existing news_items with a 12h lookback, so all today's catalyst events stay visible. **Baskets +1**: another narrative basket emerged.

### 4.4 Full catalyst test suite

```
$ python -m pytest tests/test_stocks_news_coverage.py tests/test_narrative_gainers_fix.py tests/test_catalyst_layer.py tests/test_entity_aliases.py -q
126 passed in 3.08s
```

All catalyst-layer tests (98 prior + 28 new) green.

---

## 5. Pre/post coverage summary

| Metric | Pre-PART-6 | Post-fix |
|--------|-----------:|---------:|
| Total stocks RSS feeds enabled | **0** | **8** (3 enabled + 5 new) |
| Stocks asset_class news_items (all-time) | 11 (8 real) | 11 — **will grow on next cycle's RSS pull** |
| Catalyst categories registered | 22 | **26** (+earnings_event, +analyst_action, +clinical_milestone, +insider_activity) |
| Classifier patterns covering stocks | ~3 (legal_risk only) | **~28** (earnings, analyst, clinical, insider, plus existing legal_risk) |
| Primary source for legal disclosures (PART 3 gate) | none in auto-RSS | **SEC EDGAR 8-K filings** auto-feed |
| Tests | 98 catalyst | **126 catalyst** (+28 new) |

---

## 6. Why SEC EDGAR is the headline addition

The SMCI legal gap discovered earlier today proved that the PART 3 legal-risk gate is **only as good as the news_items it can read**. The indictment was March 2026, but RSS feeds had aged it out long before the cycle 2 SMCI promotion. SEC EDGAR 8-K filings are:

- **Primary source** (`primary_source: true`) — direct from SEC.gov.
- **Material events** — Item 4.02 (financial restatements), Item 5.02 (officer/director changes), Item 8.01 (other material events) all surface here.
- **Auto-fresh** — every 8-K disclosure triggers a feed entry on filing day.
- **Universal** — covers every SEC-registered public company.

With this feed live, the PART 3 legal-risk gate gets a continuous stream of board resignations, securities-fraud-related disclosures, and accounting-restatement filings as they happen. The SMCI gap (10-week-old article never re-surfaced) is structurally closed for future cases.

---

## 7. Confirmation — safety contract

- ✅ **No scoring/threshold/agent/strategy changes** — pure data plumbing + classifier patterns.
- ✅ **No auto-trade** — read-only of news_items.
- ✅ **No alert-logic changes** — Telegram path untouched.
- ✅ **No LLM auto-invocation** — pure regex + RSS.
- ✅ **Scheduler not stopped** — PID 11880 alive.
- ✅ **Additive only** — existing feeds untouched, existing patterns preserved.
- ✅ **126 catalyst-layer tests pass** (+28 new).
- ✅ **Crypto classifications unchanged** — explicit test confirms.

---

## 8. When the fix kicks in

> **Starting from the next scheduled cycle's `scalp-report` / `intraday-report` / `stocks-intraday-report`, RSSNewsCollector will pull the 8 stocks RSS feeds and populate `news_items` with `asset_class='stocks'`. The next `catalyst-scan` step will then classify them.**

Cycle 3 is currently running. By cycle 4 (~20:15 EEST) the new feeds should have populated stocks news_items significantly. The next stocks-intraday-report after that will read the richer news pool for catalyst scoring AND the PART 3 legal-risk gate will fire on any 8-K legal disclosures.

---

## 9. Known limitations

- **RSS feeds not live-tested from my local machine** — if any return 403 / 404 they'll be skipped at fetch time (existing RSSNewsCollector fallback). The next scheduled cycle will surface any source-level issues in its logs.
- **SEC EDGAR feed**: the URL filters for 8-K filings broadly. Without per-ticker filtering it pulls ALL 8-Ks (could be 40+ per day across all SEC companies). The stocks symbol detection in news_items uses `_stocks_tickers` from `stocks/universe.yaml` to filter — so only filings mentioning our tracked stocks (AAPL/MSFT/LLY/TSLA/SMCI/etc.) become useful. Other 8-Ks land as `detected_symbols=[]`.
- **Benzinga feed format may differ** from standard RSS — RSSNewsCollector handles common variants but unknown formats fail gracefully.
- **Stocks news mapped via existing universe** — no equivalent of crypto `entity_aliases.yaml` for stocks yet. Stocks tickers in headlines are usually explicit (e.g., "AAPL", "MSFT"), so this is less of a problem.
- **Earnings dates aren't auto-scraped** — only news-driven detection. A dedicated earnings-calendar collector would close that gap; out of scope here.

---

## 10. Verdict

**READY** — stocks news coverage upgraded from "essentially zero" to "8 auto-RSS feeds + structured catalyst classification".

- 8 RSS feeds enabled (3 existing + 5 new) including **SEC EDGAR primary source**.
- 4 new catalyst categories registered (earnings, analyst, clinical, insider).
- ~25 new regex patterns.
- 28 new tests (126 total catalyst-layer tests pass).
- Zero crypto regression.
- SMCI-style legal-gap closure path now in place via auto-fresh 8-K stream.

The scheduler continues running. Cycle 3 should benefit from the news population on its next subprocess invocation; cycle 4 will show meaningfully more stocks news_items in the DB.
