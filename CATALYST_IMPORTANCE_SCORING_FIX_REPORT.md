# Catalyst Importance Scoring — Fix Report

- **Date:** 2026-06-03
- **Scope:** catalyst prioritization / review quality only. **No** trading-logic, scoring-threshold, or auto-trade changes.
- **Status:** ✅ Implemented, unit-tested (44/44 catalyst tests + 82/82 catalyst·report·collector tests pass), verified on live data.

---

## 1. Problem

`catalyst_events.jsonl` carried `importance: 0.0` for **every** row, so any "top catalysts by importance" ranking (enriched-review §5, report builder §5b "Notable events") was meaningless and fell back to insertion order. Genuinely consequential events (legal, exploit, regulatory, major-symbol) were not surfaced ahead of routine `other_news`.

## 2. Root cause

It was **not** a scorer returning 0.0 — there was **no scorer and no field at all**:

- `src/catalysts/models.py::CatalystEvent` had no `importance` attribute, and `to_dict()` never emitted one.
- Every consumer read it as `row.get("importance", 0)` → always the `0` default.

(Separately, `news_items.importance`, set by the RSS/Telegram collectors, lives on a different ~1.0+ scale. The catalyst JSONL is consumed only for *ranking*, so the fix introduces a self-contained, normalized **[0, 1]** score rather than reusing that scale.)

## 3. Design

A pure, deterministic function `score_importance(...)` in `src/catalysts/classifier.py` (the no-I/O module), returning a value in **[0, 1]** (rounded to 3 dp). It blends the seven signals requested, as a weighted average of [0,1] sub-scores (weights sum to 1.0, so the result stays bounded), then applies a rumour/social discount modifier:

| Signal | Component | Weight | How |
|---|---|---:|---|
| Catalyst-type severity | `TYPE_SEVERITY` map (covers all `CATALYST_TYPES`) | 0.30 | exploit/legal 0.95 … other_news 0.15 |
| Source quality (official vs social) | `SOURCE_QUALITY_WEIGHT` | 0.22 | primary 1.0 / single 0.6 / social 0.3 / unverifiable 0.1 |
| Freshness | `_freshness_subscore` | 0.18 | ≤1h→1.0, decaying to 0.10 at >72h; unknown→0.30 |
| Symbol-mapping confidence | `_mapping_subscore` | 0.12 | 1 clean symbol→1.0; 2–3→0.85; >3 (diffuse)→0.70; basket/unmapped→0.30 |
| Market relevance | `_market_relevance_subscore` | 0.10 | tier-1 `MAJOR_SYMBOLS`→1.0; market-wide type→0.60; other mapped→0.55; none→0.35 |
| Legal/security/geopolitical severity | `_severity_subscore` | 0.08 | legal/exploit/infra→1.0; geopolitical keyword→0.90; regulatory/delisting→0.60; else 0.20 |

**Confidence modifier (official vs social-only axis):** `rumour_only`/`is_rumour` ×0.70; `unverifiable` source ×0.70; `social_only` source ×0.90.

**Geopolitical detection** is a new helper `detect_geopolitical_severity(...)` (war/sanctions/missile/strike/Iran/Israel/Hormuz/CENTCOM/tariff/…) — motivated by the Strait-of-Hormuz / Iran risk-off cluster the 02:12 enriched-review surfaced, which previously had no way to rank above routine news.

## 4. Files changed

| File | Change |
|---|---|
| `src/catalysts/models.py` | Added `importance: float = 0.0` field to `CatalystEvent` + emit it in `to_dict()`. |
| `src/catalysts/classifier.py` | New `score_importance(...)`, `detect_geopolitical_severity(...)`, and the `TYPE_SEVERITY` / `SOURCE_QUALITY_WEIGHT` / `MAJOR_SYMBOLS` tables + sub-score helpers. |
| `src/catalysts/collector.py` | Compute importance in `_row_to_event` and pass it to `CatalystEvent`; rank the cycle-summary catalyst lists by importance and add a **"Top catalysts by importance"** section (values shown). |
| `src/reports/report_builder.py` | §5b "Notable events" now **sorted by importance** (falls back to 0.0 for legacy rows → graceful migration). |
| `src/catalysts/__init__.py` | Export `score_importance`, `detect_geopolitical_severity`. |
| `tests/test_catalyst_layer.py` | +10 tests (range, non-zero, severity/source/freshness/mapping/major ordering, rumour discount, geopolitical detection+boost, end-to-end collector ranking) and added `importance` to the to_dict required-fields assertion. |

## 5. Verification

**Unit tests:** `tests/test_catalyst_layer.py` → **44 passed**. Targeted catalyst·report·collector run → **82 passed**.

**Live data (read-only, `write_files=False`, 12h lookback, 500 events):**

```
events=500  nonzero_importance=500  min=0.292  max=0.748  mean=0.424
distribution:  0.3:1  0.4:391  0.5:69  0.6:33  0.7:6
top:    0.748 [regulatory_sector_headline] BTC/USDT  "BITCOIN SLIDES BELOW $70K…"
        0.748 [regulatory_sector_headline] HYPE/USDT "HYPE enters price discovery as ETF inflows…"
        0.692 [partnership] ENA/USDT          "Coinbase buys ENA stake…"
        0.626 [platform_growth] BTC/USDT      "Bitcoin Miner Hive Reports Revenue Surge…"
        0.582 [clinical_milestone] (basket)   "Roche … FDA priority review"
bottom: 0.292 [rumour_only] (basket)          "Exclusive-SpaceX … sources say"
        0.372 [other_news] (basket)           routine headlines
```

Before: every row 0.0. After: full spread, with legal/regulatory/major-symbol/clinical events on top and rumours at the bottom — exactly the prioritization that was missing.

## 6. Migration note

Legacy JSONL rows already written without the field sort as `0.0` (last) — no rewrite needed; the next `catalyst-scan` cycle writes scored rows. The append-only events file will briefly mix legacy-0.0 and scored rows for the current UTC day; this self-heals at the next UTC day-roll.

## 7. Safety / constraints honored

- ❌ No trading logic changed — importance is a **ranking aid only**; nothing reads it into signal scoring, the risk gate, or any execution path.
- ❌ No scoring thresholds changed.
- ❌ No auto-trade / order placement (the existing `test_no_auto_trade_in_scheduler_or_catalyst_paths` guard still passes).
- ✅ Pure, deterministic, no new I/O, no new dependencies, no paid APIs.
- ✅ Read-only w.r.t. `news_items`; writes only to `data/catalysts/<date>/` as before.

## 8. Out-of-scope note (pre-existing, unrelated)

A full `pytest tests/` run shows **7 pre-existing failures** in `tests/stocks/test_stocks_news_tagging.py` and `tests/test_stocks_monitor_alerts.py`. These are **not** caused by this change — they insert into the **populated live** `db/crypto_ai_desk.sqlite` and then assert against a `limit=500` recency window / Telegram-disabled state, so they fail when run against a non-empty DB. They do not import or exercise the catalyst layer, models, classifier, collector, or report builder. Flagged for separate cleanup (tests should use an isolated fixture DB).
