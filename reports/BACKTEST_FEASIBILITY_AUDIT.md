# Backtest Feasibility Audit

**Date:** 2026-06-11 · **Scope:** Read-only audit of stored data to determine which replay levels are feasible.
**Bottom line:** Level A (signal execution replay) is feasible with caveats. Level B is partially feasible (stocks yes, crypto only for last ~9 days). Level C (full strategy replay) is **not feasible** with current archives.

---

## 1. OHLCV coverage

All stored OHLCV files are **rolling snapshots** of the last ~220 candles (i.e., the most recent scan window), not a long historical archive. Coverage in time depends only on timeframe:

### Crypto (Binance / Bybit / MEXC)
| Exchange | TF | # symbols | rows/file (median) | calendar window | usable for replay? |
|---|---|---:|---:|---|---|
| binance | 1m | 126 | 220 | **~3h40m** | ❌ only for signals < 4h old |
| binance | 5m | 126 | 220 | **~18h** | ⚠️ only for signals < 18h old |
| binance | 15m | 153 | 220 | **~55h** | ⚠️ last ~2.3 days only |
| binance | 1h | 153 | 220 | **~9 days** | ✅ covers ~last 9 days of signal history |
| binance | 1d | 120 | 180 | ~180 days | ✅ but too coarse for intraday |
| bybit | 1m..1h | 93-113 | 220 | same as binance | same |
| mexc | 1m..1h | 130-153 | 220 | same as binance | same |

### Stocks (yfinance)
| TF | # symbols | rows/file (median) | calendar window | usable for replay? |
|---|---:|---:|---|---|
| 1m | — | — | **MISSING** | ❌ |
| 5m | — | — | **MISSING** | ❌ |
| 15m | 28 | 1560 | **2026-03-17 → 2026-06-10 (~85d)** | ✅ |
| 1h | 29 | 5082 | 2023-07-14 → 2026-06-10 | ✅ |
| 1d | 35 | 1255 | 2021-06-10 → 2026-06-10 | ✅ |
| 1wk | 28 | 523 | 2016-06-06 → 2026-06-08 | ✅ |

### Candle timestamps
All files carry a `timestamp` column with explicit UTC offsets — **point-in-time replay is safe**. No silent fill-forward observed.

---

## 2. Signal history

| Metric | Value |
|---|---:|
| Total proposed signals | 1,470 |
| Crypto | 130 |
| Stocks | 1,340 (A=103 / B=620 / C=617) |
| `raw_idea_json` populated | 1,470 / 1,470 (100%) |
| Signal date range | 2026-05-22 → 2026-06-10 (~20 days) |
| Latest-outcome `final_outcome` populated | crypto 121/130, stocks 1,303/1,340 |

### Outcome distribution (latest checkpoint per signal)
| asset_class | outcome | n |
|---|---|---:|
| crypto | loss | 40 |
| crypto | expired | 34 |
| crypto | not_triggered | 29 |
| crypto | win | 18 |
| stocks | expired | 447 |
| stocks | not_triggered | 345 |
| stocks | loss | 299 |
| stocks | win | 211 |
| stocks | ambiguous | 1 |

`signal_outcomes` is a time-series of tracker checkpoints, not a single-row-per-signal table. Replay must read the **last** row per `signal_id` (we have full series, can also see the evolution).

All key replay inputs are present in `proposed_signals`:
- `created_at`, `entry_low`, `entry_high`, `entry_trigger`, `stop_loss`, `invalidation`, `tp1/tp2/tp3`, `direction`, `mode`, `tier`, `playbook` (derivable from `mode + setup_type + tier` via `src.signals.playbooks.label_for`).

Pending revalidation states (`stale_before_entry`, `entry_moved_away`) are recorded — replay can honor them.

---

## 3. News / catalysts

| Source | Coverage | Replayable point-in-time? |
|---|---|---|
| `news_items` table | 9,485 rows, 2018-11-09 → 2026-06-10 | ✅ has `published_at` |
| `data/catalysts/<date>/catalyst_events.jsonl` | 2026-06-01 → 2026-06-10 (10 days, ~25 MB total) | ✅ day-scoped JSONL |
| Narrative baskets | Computed live, not snapshotted | ❌ would have to reconstruct |
| Detected symbols JSON | Embedded in catalyst events | ✅ |

Conclusion: news/catalyst point-in-time replay is feasible only for **2026-06-01 onward**. Earlier signals (May 22-31) have `news_items` but no catalyst-event JSONL.

---

## 4. Derivatives history

| Source | Status |
|---|---|
| Funding | latest-cache only inside `proposed_signals.funding_context` (string blob) — no historical funding archive |
| Open interest | same — `oi_context` string snapshot, no time series |
| Long/short ratio | not archived |

Derivatives data is **latest-cache, not point-in-time**. Replay cannot reconstruct derivatives-conditioned scoring at historical timestamps.

---

## 5. Reports / packets / watchlists

| Source | Count | Usable for Level B? |
|---|---:|---|
| `reports/**.md` | 98 | Partially (most recent only — older cycles purged) |
| `data/processed/llm_*.md` | latest only | ❌ overwritten each cycle |
| Expansion watchlist JSON snapshots | not stored as time series | ❌ |
| Archived raw idea JSON | embedded in `proposed_signals.raw_idea_json` | ✅ (idea snapshot at creation) |

`raw_idea_json` is the single best Level-B artifact: it contains the LLM's full reasoning at the moment of signal proposal. But the **upstream context** (exact regime/sector/narrative/news at that timestamp) is not snapshotted.

---

## 6. Feasibility verdicts

| Replay level | Feasible? | Confidence | Notes |
|---|---|---|---|
| **Level A — Signal execution replay** | ✅ YES | High for stocks (15m coverage = 85d > 20d signal window). **Limited for crypto** — only 1h is wide enough (~9d), so crypto signals from 2026-05-22 → 2026-06-01 can only be replayed against the already-recorded `signal_outcomes` outcomes (no re-simulation of intrabar with stored 1m/15m candles). | See §7 strategy below. |
| **Level B — Point-in-time signal replay** | ⚠️ PARTIAL | Stocks: limited (we have `raw_idea_json` snapshot of the idea, not of the regime). Crypto: limited (catalyst events from 2026-06-01+ only). | Possible to validate "would current scoring re-derive the same idea given today's data?" but not "given the past data". |
| **Level C — Full strategy replay** | ❌ NO | Requires historical OHLCV archive ≥ 30d, historical funding/OI time series, historical news+catalyst archive ≥ 30d, historical regime/sector snapshots. None exist. | Would need a sustained collection campaign before becoming feasible. |

---

## 7. What's high-confidence vs lower-confidence for Level A

| Cohort | Coverage | Confidence label |
|---|---|---|
| **Stocks** all signals last 20d | 15m available across full window | **HIGH** |
| **Crypto** signals from 2026-06-02 onward (~last 9d) | 1h available; 15m partial; 1m only for very fresh signals | **MEDIUM** (1h granularity → cannot adjudicate same-1h-bar TP-vs-stop deterministically) |
| **Crypto** signals from 2026-05-22..06-01 | No usable candles from `created_at` going forward | **LOW** — replay falls back to comparing against the tracker's already-recorded outcome, which was computed at the time when candles were fresh |
| **Crypto scalp 1m TP study** | 1m only covers last ~4h → almost no signals fall in window | **LOW / counterfactual only** — must be marked as data-limited |
| **Stocks RTH open replay** (A-tier first 15m/30m/60m) | 15m covers full window | **HIGH** |
| **Expansion watchlist follow-through** (did C → A/B?) | requires only `proposed_signals` history; no candle dependency | **HIGH** |
| **Playbook sizing walk-forward** | uses `final_r` (already in DB); no candle dependency | **HIGH** |

---

## 8. Final answer

* **Can we do full strategy replay (Level C)?** No.
* **Can we do signal-level replay (Level A)?** Yes, with the confidence labels above.
* **Can we do 1m execution replay?** Effectively no — crypto 1m archive is < 4h. Stocks have no 1m at all. Scalp 1m study will be **counterfactual / data-limited**.
* **What is missing?** Long historical OHLCV at 1m/5m/15m for crypto, any 1m/5m for stocks, historical funding/OI time series, historical narrative/regime snapshots.
* **Which results should be lower-confidence?** Anything depending on intrabar adjudication for signals older than the candle archive window; the crypto scalp 1m TP study in particular.

---

**Verdict for this audit:** **proceed with Level A only**, with explicit lower-confidence labels for crypto pre-2026-06-02 signals and for any scalp 1m results. Do not attempt Level C.
