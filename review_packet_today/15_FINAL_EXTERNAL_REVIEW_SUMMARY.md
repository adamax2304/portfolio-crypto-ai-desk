# Final External Review Summary — 2026-05-25

Compact summary for an external reviewer. ~5 minutes to read.

---

## 1. Commands run

```text
python -m src.cli intraday-report           # OK → 2026-05-25_14-03_intraday_report.md
python -m src.cli scalp-report              # OK → 2026-05-25_13-52_scalp_report.md
python -m src.cli stocks-intraday-report    # OK → 2026-05-25_14-12_stocks_intraday_report.md
python -m src.cli weekend-status            # OK (Weekend Mode inactive — Monday)
python -m src.cli signal-stats --asset-class crypto   # OK (sample=1, anecdotal)
python -m src.cli signal-stats --asset-class stocks   # OK (sample=19, weak)
python -m src.cli active-signals                       # OK (19 active, all waiting)
python -m src.cli track-signals --all                  # OK (no_ohlcv=0, updated=0)
python -m src.cli active-signals --asset-class crypto  # FAIL — flag not supported
```

## 2. Reports collected
- `02_REPORT_CRYPTO_SCALP.md` — fresh, 16:52 EEST
- `03_REPORT_CRYPTO_INTRADAY.md` — fresh, 17:03 EEST
- `04_REPORT_STOCKS_INTRADAY.md` — fresh, 17:12 EEST

## 3. LLM packets collected
- `05_LLM_PACKET_CRYPTO_SCALP_OR_SHARED.md` — **STALE (2026-05-24, weekend mode active)**
- `06_LLM_PACKET_CRYPTO_INTRADAY_OR_SHARED.md` — same file as #5 (crypto desk shares one packet)
- `07_LLM_PACKET_STOCKS_INTRADAY.md` — **STALE (2026-05-25 02:00, refers to old AAPL/TSLA-only report)**

## 4. Crypto / stocks separation
- Pipelines: **separate** (`src/agents/` vs `src/stocks/agents/`).
- Reports: **separate** (different folders).
- Signal-stats: **separate** (per-asset-class flag works).
- News fixtures: **leaking** — old AAPL/NVDA/COIN/MSTR `test_source` items appear in crypto reports.
- `active-signals --asset-class` filter: **not implemented**.

## 5. Data source availability
| Source | Status |
|--------|--------|
| Crypto OHLCV (5m/15m/1h) | OK |
| Crypto derivatives (Bybit/OKX) | OK |
| Crypto RSS (4 sources) | OK |
| Stocks OHLCV 15m/1h/1d | OK (full universe) |
| Indices + sector ETFs | OK (4 indices + 12 sector ETFs) |
| Stocks RSS | **DISABLED** (MarketWatch, Yahoo Finance, Seeking Alpha all "Skipping disabled") |
| Stocks news (production) | **FAKE** (4 test_source items only) |
| Earnings calendar | **PARTIAL** (18 tracked, all per-stock evidence says "earnings:unknown") |
| Telegram / news_trader | **EMPTY** (bridge silent today; placeholder KOL) |
| Liquidations / order book / on-chain / ETF flows / DXY / macro calendar | **NOT WIRED** (explicitly acknowledged blindspots) |
| Obsidian dynamic context | **TEMPLATE ONLY** (`update-obsidian-context` is a TODO stub) |

## 6. Idea completeness — entry / invalidation / TP / risk

| Idea type | Entry | Invalidation | TP | Counter-thesis | What to monitor | Risk warning |
|-----------|-------|--------------|----|----|-----|---------|
| Crypto C-tier | ✅ | ✅ | ✅ TP1/2/3 | ⚠️ templated | ✅ | ✅ |
| Stocks A/B | ✅ | ✅ | ✅ TP1/2/3 | ⚠️ one-liner ("earnings risk: unknown") | ❌ missing | ⚠️ implicit |

## 7. Top 5 concerns

1. **LLM packets are stale.** Today's reports do NOT trigger packet regeneration. A fresh LLM session reads yesterday's data + Sunday's weekend overlay.
2. **Stocks news is fake.** All 4 surfaced items are `test_source`. AAPL A-tier evidence cites a fake buyback article.
3. **Earnings risk is "unknown" on every stocks idea**, despite 18 events allegedly tracked. Per-stock lookup not propagating to evidence.
4. **Counter-thesis is templated** (crypto) / **one-liner** (stocks). The reasoning channel is decorative, not substantive.
5. **Inconsistent rule enforcement**: `short_in_bullish_regime` applied to COIN but NOT MSTR (same direction, same regime).

## 8. Top 5 strengths

1. **Risk gates work.** 4 obvious overextended crypto movers (SAGA, RENDER, NEAR, INJ raw 95–100) correctly rejected with `>2 ATR from EMA20`.
2. **Asset-class separation** is structurally clean at code + report + DB layers.
3. **Honest about blindspots.** The Data Coverage section explicitly lists what isn't connected; KOL placeholder is flagged; "no fresh catalyst" stated openly.
4. **Signal tracker cross-asset path resolution works** (Fix #1 verified — `no_ohlcv=0`).
5. **NO TRADE is genuinely respected** — crypto produced 0 A/B today and the system did not invent ideas.

## 9. Reading order for the external reviewer

1. **`15_FINAL_EXTERNAL_REVIEW_SUMMARY.md`** (this file) — 5 min
2. **`01_DECISION_AUDIT_TODAY.md`** — 15 min, the main audit
3. **`10_DATA_COVERAGE_AUDIT.md`** — 5 min, what's actually wired
4. **`13_SCORE_AND_RISK_AUDIT.md`** — 10 min, per-idea defensibility
5. **`14_TECHNICAL_ANALYSIS_AUDIT.md`** — 10 min, chart-level review
6. **`16_SIGNAL_TRACKING_PERFORMANCE_AUDIT.md`** — 5 min, registry health
7. **`02–04` reports** — primary source, in order: stocks (best signal), intraday, scalp
8. **`05–07` LLM packets** — only to verify the staleness claim

## 10. Known missing files / data
- No fresh `prepare-analysis` LLM packet for today (crypto or stocks).
- No real stocks RSS items.
- No populated `Current_Context_For_LLM.md` (template only).
- No signal performance section in reports/packets.
- No macro/Fed/yields/DXY for stocks.
- No 4h structural context for crypto intraday ideas.
- No "What to Monitor" section on stocks ideas.
- No `active-signals --asset-class` flag.
- 18 earnings events tracked but never propagated to evidence per idea.

---

## One-line bottom line

**The desk is a credible screening tool that names candidates with explicit invalidation and rejection reasoning. It is not yet a decision-grade signal system: stale LLM packets, fake stocks news, one-liner counter-thesis, and an empty signal-performance feedback loop mean the LLM does not actually consume the full context the protocol claims it does. Today's strongest defensible idea is LLY long; AAPL's A-tier rests partly on test fixture data and should be verified manually.**
