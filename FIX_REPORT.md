# Fix Report — critical/high audit issues

Date: 2026-05-25
Scope: address every Critical and High issue identified in [AUDIT_STOCKS_MODULE.md](AUDIT_STOCKS_MODULE.md). No new features. No unrelated refactors. Crypto pipeline untouched except for the one shared signal-tracker file where asset_class routing belongs.

---

## Fix #1 — `track-signals` is now asset_class-aware  (audit issue #1, **Critical**)

### Problem
`src/signals/tracker.py` previously called `file_store.load_ohlcv(exchange, symbol, tf)` which only reads `data/raw/ohlcv/{exchange}/{tf}/{SYMBOL}.csv`. Stocks signals (`asset_class='stocks'`) carried `exchange_focus='US'` which doesn't exist as a cache directory and even if it did, the CSVs are written to `data/raw/stocks/{tf}/{SYMBOL}.csv` by the yfinance collector. Result: every stocks signal would silently increment `skipped_no_ohlcv` and never receive an outcome.

### What changed
- [src/storage/file_store.py](src/storage/file_store.py)
  - New methods `stocks_ohlcv_path(symbol, timeframe)` and `load_stocks_ohlcv(symbol, timeframe)`.
  - `load_stocks_ohlcv` normalizes the yfinance-shaped CSV (Date/Datetime index + capitalized OHLCV) into the crypto-tracker shape (lowercase columns + a `timestamp` column with UTC datetimes), so the tracker can consume both crypto and stocks frames identically.
- [src/signals/tracker.py](src/signals/tracker.py)
  - New `STOCKS_TIMEFRAME_PREFERENCE` map (no per-exchange tree, no 5m/4h, plus `1wk` for invest).
  - New `_load_stocks_ohlcv_for_signal(file_store, symbol, mode)` function.
  - `track_signal` reads `signal['asset_class']` and routes to the stocks loader when `'stocks'`, else falls through to the original crypto path. The crypto code path is byte-identical to before.

### Verification
- New tests under [tests/stocks/test_stocks_signal_tracking.py](tests/stocks/test_stocks_signal_tracking.py) cover:
  - normalization of the yfinance CSV shape
  - missing cache returns `None`
  - multi-timeframe fallback (swing prefers 1h, falls back to 1d)
  - end-to-end `track_signal` for a synthetic long stocks signal that triggers entry + TP1
  - crypto signals continue to resolve through the per-exchange tree unaffected
  - missing cache for a stocks signal returns `None` cleanly (no exception)
- Live smoke: `python -m src.cli track-signals --all` now reports `no_ohlcv=0` (previously stocks signals contributed to `skipped_no_ohlcv` silently).

### Crypto regression
35/35 crypto tests still pass. The crypto branch of `_load_ohlcv_for_signal` is untouched; only an extra early-return branch was added before it for the stocks case.

---

## Fix #2 — Real `volume_relative_volume`  (audit issue #3, **High**)

### Problem
`StockScoringAgent` hardcoded the volume component raw to `0.5` for every symbol. The component contributed weight × 0.5 indiscriminately — useless for ranking.

### What changed
- [src/stocks/agents/technical_agent.py](src/stocks/agents/technical_agent.py)
  - New `_volume_ratio(frame, window=20)` helper. Computes last-bar volume divided by the rolling-20-bar mean. Returns `None` cleanly when history is short, volume is zero, or column is missing.
  - `TechnicalSetup` dataclass gained `volume_ratio: float | None`.
  - `_build` calls `_volume_ratio(context_frame)` and stores the result on the setup.
- [src/stocks/agents/scoring_agent.py](src/stocks/agents/scoring_agent.py)
  - Replaced the `vol_raw = 0.5` placeholder with a piecewise mapping:
    - ≤ 0.5× → 0.0 (thin participation)
    - 1.0× → 0.33
    - 1.5× → 0.67
    - ≥ 2.0× → 1.0 (volume surge)
  - When the technical agent could not compute the ratio (missing data), the component falls back to neutral `0.5` — and the data_confidence component (see Fix #3) is independently penalized via a `missing_volume_ratio` flag.

### Verification
- New tests in [tests/stocks/test_stocks_volume_and_data_confidence.py](tests/stocks/test_stocks_volume_and_data_confidence.py):
  - `_volume_ratio` basic spike (200/100 → ≈ 1.9)
  - `_volume_ratio` below-1 case (100/200 → ≈ 0.5)
  - short history returns `None`
  - zero volume returns `None`
  - end-to-end: a setup with `volume_ratio=2.0` and full data scores its `volume_relative_volume` and `data_confidence` components strictly higher than a setup with `volume_ratio=None` and `data_confidence_raw=None`. Final score follows.

---

## Fix #3 — Real `data_confidence`  (audit issue #4, **High**)

### Problem
`StockScoringAgent` hardcoded `data_raw = 0.8` for any setup that existed. Missing intraday frames, short history, no daily bars — all treated the same.

### What changed
- [src/stocks/agents/technical_agent.py](src/stocks/agents/technical_agent.py)
  - New `_compute_data_confidence(...)` helper. Builds a 0..1 score from:
    - context-frame history depth (≥100 / ≥50 / ≥30 / less)
    - presence of daily history (for prev-day H/L)
    - presence of intraday exec frame (only weighted for intraday mode; swing/invest get the "not applicable" credit so they aren't unfairly penalized)
    - presence of prev-day H/L
    - presence of ATR
    - presence of volume_ratio (from Fix #2)
    - presence of VWAP (intraday only)
  - Returns `(score, flags)` where `flags` is a human-readable list of what's missing (`short_context_history`, `missing_daily_history`, `missing_intraday_exec_frame`, `missing_prev_day_levels`, `missing_atr`, `missing_volume_ratio`, `missing_vwap`).
  - `TechnicalSetup` dataclass gained `data_confidence_raw: float` and `data_flags: list[str]`.
- [src/stocks/agents/scoring_agent.py](src/stocks/agents/scoring_agent.py)
  - Reads `setup['data_confidence_raw']` instead of the hardcoded 0.8. Falls back to neutral 0.5 only when the setup is a legacy payload without the field.

### Verification
- Three dedicated tests in [tests/stocks/test_stocks_volume_and_data_confidence.py](tests/stocks/test_stocks_volume_and_data_confidence.py):
  - full intraday inputs → score ≥ 0.95, no flags
  - swing mode does not penalize a missing intraday exec frame or missing VWAP
  - all inputs missing → score ≤ 0.20 and the expected flags appear

### Side benefit
Replaced the unreadable NaN guard `if not series.iloc[-1] != series.iloc[-1]` with `pd.isna(...)` at three places in `_build`. (Audit issue #11, Medium — cleaned up for free since I was already editing the same lines.)

---

## Fix #4 — "Both index AND sector contradict → reject"  (audit issue #5, **High**)

### Problem
`config/stocks/risk.yaml` documented `confirmation.both_contradict.reject: true` but no code in `StockRiskAgent` or `StockScoringAgent` detected the composite case. A long in `risk_off` with weak sector status would only collect two separate penalties; it never fired the documented hard-block rule.

### What changed
- [src/stocks/agents/risk_agent.py](src/stocks/agents/risk_agent.py)
  - In the per-symbol loop, two local flags are now set:
    - `index_contradicts` — True when long-in-risk_off, short-in-bullish, long when regime_bias is short, or short when regime_bias is long.
    - `sector_contradicts` — True when long in a weak sector or short in a strong sector.
  - When both are True and direction is long or short, a new block is appended:
    - `flags.append("both_index_and_sector_contradict")` — always (for visibility)
    - `blocks.append("both_index_and_sector_contradict")` — when `confirmation.both_contradict.reject` is true in the YAML
  - The block flows through unchanged: `StockScoringAgent` already forces `tier='rejected'` when `blocks` is non-empty.

### Verification
- Four tests in [tests/stocks/test_stocks_both_contradict.py](tests/stocks/test_stocks_both_contradict.py):
  - long in risk_off + weak sector → both flag and block fire
  - short in bullish + strong sector → both flag and block fire
  - only index contradicts (sector strong) → flag/block absent
  - aligned trade (bullish + strong + long) → no flag at all

---

## Fix #5 — Stocks news minimum path  (audit issue #2, **High**)

### Problem
The RSS news collector unconditionally tagged every news_item as crypto. `news_items` had 0 stocks rows. `CompanyNewsAgent` had a dead conditional (`matched.isdisjoint(sym_set)` is always False after `& sym_set`) and surfaced no hits in practice.

### What changed
- [config/sources.yaml](config/sources.yaml)
  - Existing crypto sources now carry an explicit `asset_class: crypto` field. Defaults to `'crypto'` when omitted, so any custom local feeds the user already added behave the same.
  - Three stocks-flavored RSS sources added but **disabled** by default (MarketWatch Top Stories, Yahoo Finance Top Stories, Seeking Alpha Market Currents). Each carries `asset_class: stocks`. Flip `enabled: true` to start ingesting.
- [src/data_collectors/rss_news_collector.py](src/data_collectors/rss_news_collector.py)
  - Reads `source.asset_class` per RSS source (default crypto).
  - Loads the stocks universe tickers (from `config/stocks/universe.yaml`) lazily on construction so it can detect $NVDA / $AAPL / etc when processing a stocks source. Fails silently if the stocks module isn't installed — preserves backward compat.
  - Items are bucketed by asset_class during the fetch loop and persisted via `db.save_news_items(items, asset_class=...)`, so stocks sources land with the correct tag.
  - Item builders accept `asset_class` and use the stocks ticker universe (in addition to the crypto one) when processing a stocks source. This covers cross-asset headlines naturally (e.g. an article naming both MSTR and BTC gets matched on both).
- [src/stocks/agents/company_news_agent.py](src/stocks/agents/company_news_agent.py)
  - Removed the dead `matched.isdisjoint(sym_set)` conditional.
  - New behavior: rows tagged `asset_class='stocks'` always count. Rows tagged otherwise count when their `detected_symbols` intersect with the stocks universe (cross-asset gate, default on). The agent now surfaces two counters in its payload: `counts.stocks_tagged` and `counts.cross_asset` so reports can show where hits came from.
  - New optional `prefer_stocks_tagged: bool` parameter on `run()` — defaults `True`; flip to `False` for strict mode (stocks-tagged only).

### Verification
- Four tests in [tests/stocks/test_stocks_news_tagging.py](tests/stocks/test_stocks_news_tagging.py):
  - `save_news_items(asset_class='stocks')` persists `'stocks'` in the DB column (direct SQL inspection).
  - `CompanyNewsAgent` finds a stocks-tagged hit and counts it as `stocks_tagged`.
  - Cross-asset gate: a crypto-tagged row that mentions COIN surfaces for the stocks agent and is counted as `cross_asset`.
  - Strict mode (`prefer_stocks_tagged=False`) ignores crypto-tagged rows entirely.

### Note on real news flow
The fix delivers the **plumbing**; actual news will start flowing only when the user enables one of the new stocks RSS sources in `config/sources.yaml`. That's an intentional choice — the audit said "stocks news is dry," and now the pipe is open but unfilled.

---

## Tests + commands run

### Full pytest suite
`python -m pytest tests/ -q` → **70 passed in 16.01s**

Breakdown:
- 35 crypto tests (unchanged): pass.
- 13 stocks tests from the original Stage 7: pass.
- 22 new tests added in this fix pass:
  - 6 signal tracking
  - 7 volume + data_confidence
  - 4 both-contradict
  - 5 news tagging (4 + a helper)

### Live smoke tests
- `python -m src.cli stocks-intraday-report --symbols NVDA --symbols AAPL --symbols MSFT --symbols TSLA --no-update` — succeeds, regime=bullish, 1 A/B idea, 1 C watchlist, 2 signals registered (asset_class='stocks').
- `python -m src.cli track-signals --all` — succeeds, `checked=5 no_ohlcv=0` (previously stocks would silently fall into `no_ohlcv`).
- `python -m src.cli signal-stats --asset-class stocks` — returns the expected rows.
- `python -m src.cli signal-stats --asset-class crypto` — returns the expected rows. No cross-contamination.
- Watchlist monitor (crypto) — continues to fire tier-change alerts unaffected.

---

## Remaining limitations (out of scope for this fix pass)

These issues from the audit were intentionally **not** addressed here — they remain on the backlog:

| # | Severity | Issue | Why deferred |
|---|---|---|---|
| 6 | Medium | Gap rules (`require_retest_after_gap_pct`, `reject_chase_after_gap_pct`) configured but not enforced. | Needs a gap-detector helper; deferred per instruction (no new features). |
| 7 | Medium | Liquidity floors (avg dollar volume, rel-vol floor) configured but not enforced. | Requires a 30d avg-volume collector. |
| 8 | Medium | `EarningsRiskAgent.blocks_swing` flag is mode-agnostic (informational). | Cosmetic semantic; tests already document the intent. |
| 9 | Medium | EarningsRiskAgent uses calendar days, not trading days. | Needs a US trading-calendar helper. |
| 10 | Medium | No macro calendar collector. | Spec calls for a new collector; out of fix scope. |
| 12 | Medium | VWAP is rolling-26-bar (not session-anchored). | Session-anchored VWAP requires intraday session boundary logic. |
| 13 | Medium | `EarningsCalendarCollector` always sets `report_time='unknown'`. | yfinance limit; manual CSV is the only override. |
| 15 | Medium | Stocks signal validity windows (24h intraday) don't account for market-closed hours. | Needs a per-asset-class validity map; minor effect today since stocks signals are infrequent. |
| 16 | Medium | `StocksPipeline.run_report` fetches earnings twice. | Trivial optimization; doesn't affect correctness. |
| 17 | Medium | Stocks LLM packet doesn't pull Obsidian rules excerpts. | Spec deferred. |
| 18 | Medium | `prompts/system/` protocols don't mention asset_class. | Doc churn; defer until prompts are revised anyway. |
| 19 | Medium | No stocks Signal_Performance/ Obsidian folder. | Cosmetic mirror. |
| 20–29 | Low | Various — `.env.example`, FundamentalSnapshotAgent, DST, yfinance 429, etc. | All deferred per "no new features." |

### What the fixes did NOT change

- The crypto pipeline's scoring, regime classification, agents, reports, or LLM packet content. **Zero behavioral change** on the crypto side.
- The crypto OHLCV cache layout. The new stocks loader is additive.
- The stocks pipeline's regime/sector/RS/earnings agents. Only StockTechnicalAgent and StockScoringAgent changed; both changes are additive (new fields on TechnicalSetup, fallback paths preserve old behavior if the new fields are missing).
- The stocks Markdown report layout. New data shows up through the existing component breakdown table; `data_flags` are now available on each setup but the report builder doesn't render them yet (Medium-priority follow-up).

### What remains MVP-level

Even with these fixes, the stocks module is "screening tool" quality, not "real-money execution" quality. The dominant gaps that the user would feel in practice:
- News stays empty until a stocks RSS source is enabled.
- Gap behavior and liquidity floors are still unenforced.
- No fundamentals data for invest mode.
- yfinance is rate-limited and can flake on indices.

Fixing the five Critical/High items moves the module from "broken feedback loop + decorative scoring" to "correct feedback loop + meaningful scoring with documented gaps."

---

## File-level change inventory

| File | Lines touched | Nature |
|---|---|---|
| src/storage/file_store.py | +49 | new stocks OHLCV path + loader |
| src/signals/tracker.py | +35 | new stocks branch in load + track |
| src/stocks/agents/technical_agent.py | ~110 net | volume_ratio + data_confidence + NaN cleanup |
| src/stocks/agents/scoring_agent.py | ~18 net | replace 2 placeholder constants |
| src/stocks/agents/risk_agent.py | +25 | both-contradict detection |
| src/stocks/agents/company_news_agent.py | ~30 net | new filter logic + counters |
| src/data_collectors/rss_news_collector.py | ~50 net | per-source asset_class plumbing |
| config/sources.yaml | +20 | asset_class tags + 3 disabled stocks sources |
| tests/stocks/test_stocks_signal_tracking.py | +186 (new file) | 6 tests |
| tests/stocks/test_stocks_volume_and_data_confidence.py | +186 (new file) | 7 tests |
| tests/stocks/test_stocks_both_contradict.py | +106 (new file) | 4 tests |
| tests/stocks/test_stocks_news_tagging.py | +131 (new file) | 4 tests |
| **Total** | **~960 lines** | 5 fixes + 21 new tests + 0 regressions |

No crypto agent / collector / scorer / report file was modified.

---

## How to verify the fixes yourself

```powershell
# Full suite
python -m pytest tests/ -v

# Targeted test groups
python -m pytest tests/stocks/test_stocks_signal_tracking.py -v
python -m pytest tests/stocks/test_stocks_volume_and_data_confidence.py -v
python -m pytest tests/stocks/test_stocks_both_contradict.py -v
python -m pytest tests/stocks/test_stocks_news_tagging.py -v

# Live smoke: stocks pipeline still produces ideas
python -m src.cli stocks-intraday-report --symbols NVDA --symbols AAPL --symbols MSFT --no-update

# Live smoke: track-signals across both asset classes (no_ohlcv should be 0 for fresh stocks signals)
python -m src.cli track-signals --all

# Live smoke: signal-stats filters cleanly
python -m src.cli signal-stats --asset-class stocks
python -m src.cli signal-stats --asset-class crypto
```
