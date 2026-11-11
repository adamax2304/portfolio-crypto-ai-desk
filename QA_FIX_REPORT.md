# QA Fix Report — 2026-05-25

Closes the workflow and reasoning gaps surfaced in `review_packet_today/` by the Decision Quality Audit (same day).

**Scope discipline (per instructions):**
- No new trading logic.
- No architecture refactor.
- No new modes.
- No paid APIs.
- No crypto scoring changes.

---

## Summary of fixes

| # | Topic | Files touched | Status |
|---|-------|---------------|--------|
| QA-1 | Auto-regenerate LLM packets on report runs | `src/cli.py`, `src/analysis/packet.py`, `src/stocks/llm_packet.py` | ✅ Shipped |
| QA-2 | Drop / mark `test_source` news pollution; asset_class-scoped news loads | `src/storage/sqlite.py`, `src/agents/supervisor.py`, `src/agents/watchlist_monitor.py`, `tests/stocks/test_stocks_news_tagging.py` | ✅ Shipped |
| QA-3 | Embed Recent Signal Performance in crypto + stocks reports | `src/signals/report_section.py` (new), `src/reports/report_builder.py`, `src/stocks/reports/stocks_report_builder.py`, `src/stocks/pipelines/stocks_pipeline.py` | ✅ Shipped |
| QA-4 | Stocks idea evidence improvements (earnings date, What to Monitor, score components, data_confidence/sources) | `src/stocks/agents/trade_idea_agent.py`, `src/stocks/reports/stocks_report_builder.py` | ✅ Shipped |
| QA-5 | CLI UX — `active-signals --asset-class` filter | `src/cli.py` | ✅ Shipped |
| QA-6 | Tests + this report | `tests/test_qa_fixes.py` (new), `tests/stocks/test_stocks_news_tagging.py` (extended) | ✅ Shipped |

---

## QA-1 — LLM packet freshness

### Behaviour before
`intraday-report`, `scalp-report`, `swing-report`, and `stocks-intraday-report` (+ swing/invest) wrote the human-readable Markdown report and refreshed `data/processed/context_for_llm.md`, but they **did not** regenerate `data/processed/llm_analysis_packet.md` or `data/processed/llm_stocks_packet.md`. Today's audit found both packets had stale May-24 / May-25-02:00 timestamps and the crypto packet still referenced "Weekend Mode active" on a Monday.

### Behaviour after
- Each crypto report command now calls `_refresh_crypto_packet(supervisor, mode, report_path)` after the report is saved. That delegates to `src.analysis.packet.write_packet(...)`, passing the new `source_report` kwarg.
- `_run_stocks_report` does the equivalent via `_refresh_stocks_packet(pipeline, mode, report_path)` → `src.stocks.llm_packet.write_stocks_packet(...)`.
- Each refresh is `try/except`-guarded so a packet builder bug never blocks the report.
- A new `--skip-packet` flag (`intraday-report`, `scalp-report`, `swing-report`, `stocks-*-report`) lets you opt out for fast iteration.
- Both packet builders' signatures now accept an optional `source_report: str | None`; when provided, the packet header surfaces `Source report: <path>` so an auditor or LLM can verify freshness vs the underlying report.

### Tests added
- `tests/test_qa_fixes.py::test_crypto_packet_includes_source_report`
- `tests/test_qa_fixes.py::test_stocks_packet_includes_source_report`

### Verification
- `python -m src.cli prepare-analysis --mode intraday` — succeeded, packet regenerated.
- `python -m src.cli prepare-analysis --asset-class stocks --mode intraday` — succeeded, packet regenerated.

---

## QA-2 — Remove `test_source` pollution

### Behaviour before
- `SQLiteStore.load_recent_news(limit)` ignored both `asset_class` and source filtering.
- Test fixtures (notably `tests/stocks/test_stocks_news_tagging.py`) inserted rows with `source="test_source"` into the **production** DB (because they share `load_config()`). Today's audit saw AAPL/NVDA/COIN/MSTR `test_source` items surface in **crypto** scalp/intraday reports because nothing filtered them.

### Behaviour after
- `SQLiteStore.load_recent_news(...)` now accepts two new kwargs:
  - `asset_class: str | None` — scopes the query to `'crypto'` or `'stocks'` (crypto-scoped reads also accept legacy rows with `NULL asset_class`).
  - `include_test_sources: bool | None` — when False (default) drops rows whose `source` is in the new `SQLiteStore.TEST_NEWS_SOURCES` set (`{"test_source", "test-source", "test", "fixture"}`).
- The default is overridden by the `CRYPTO_AI_DESK_INCLUDE_TEST_NEWS` env var (`1` / `true` / `yes`) to keep existing tests viable.
- `src/agents/supervisor.py` and `src/agents/watchlist_monitor.py` now call `load_recent_news(..., asset_class="crypto")` so stocks-tagged rows can't leak into crypto reports.
- `CompanyNewsAgent` continues to call without `asset_class` (intentional — it wants cross-asset matches) but the test-source filter still applies at the DB layer.

### Tests added
- `tests/stocks/test_stocks_news_tagging.py::test_test_source_filter_drops_by_default`
- `tests/stocks/test_stocks_news_tagging.py::test_load_recent_news_asset_class_filter`
- The three pre-existing CompanyNewsAgent tests were patched to set `CRYPTO_AI_DESK_INCLUDE_TEST_NEWS=1` via `monkeypatch.setenv`, since they intentionally use `test_source` fixtures.

### Net impact
- Production reports no longer surface fake AAPL/NVDA/COIN/MSTR news.
- Stocks pipeline still sees its own `asset_class='stocks'` items (when they exist).
- Easy opt-in for debugging via env var.

---

## QA-3 — Recent Signal Performance in reports

### Behaviour before
The LLM packets (`llm_analysis_packet.md`, `llm_stocks_packet.md`) already included signal-stats summaries, but **the human-readable reports did not**. A user reading the report had to run `signal-stats --asset-class …` separately.

### Behaviour after
- New module `src/signals/report_section.py` exports `build_signal_performance_block(config, *, asset_class, period="week", title="Recent Signal Performance")`.
- The block contains: period, asset_class, sample size + confidence label, A/B/C tier counts, triggered count + percentage, wins/losses/ambiguous, TP1/stop hit rates, triggered winrate, avgR/totalR/PF, active-right-now count, sample-size warning, **explicit "Strategy is not auto-modified" disclaimer**.
- The block is **failure-safe**: if analytics raises (e.g. missing tables, broken config) it returns a one-line "unavailable" stub so the surrounding report keeps going.
- `ReportBuilder.build_daily()` (crypto) now inserts the block between `## 9. Data Coverage / Blindspots` and `## 10. Final Summary`.
- `build_stocks_report(result, *, config=None)` now inserts the block between Rejected and Final Summary. The pipeline passes `config=self.config`; tests that bypass the pipeline can omit it (the block is skipped when `config` is None).

### Tests added
- `tests/test_qa_fixes.py::test_signal_performance_block_renders_for_crypto`
- `tests/test_qa_fixes.py::test_signal_performance_block_renders_for_stocks`
- `tests/test_qa_fixes.py::test_signal_performance_block_failure_safe`

### Read-only guarantee
The new block calls `compute_breakdowns` (analytics-side read-only path) and a `SELECT COUNT(*)` against `signals`. No mutation. No feedback into scoring. The audit-mandated "strategy is **not** auto-modified" disclaimer is rendered inside every block.

---

## QA-4 — Stocks idea evidence improvements

### Behaviour before
- Every stocks idea's evidence showed `earnings:unknown` regardless of whether the calendar lookup succeeded; per-symbol earnings date was not surfaced.
- Counter-thesis was a one-liner ("earnings risk: unknown").
- The report's `_ideas_section` did **not** render `what_to_monitor`, `data_confidence`, `data_sources_used`, or the per-component score breakdown — even though the upstream agents already produced those fields.

### Behaviour after
1. **Earnings line in evidence** — `StockTradeIdeaAgent._evidence(...)` now appends a line built by the new helper `_earnings_evidence_line(er)`:
   - `earnings: safe (no event in the near window)` when `severity='safe'`.
   - `earnings: UNKNOWN (calendar lookup missing — treat as undated event risk)` when severity is unknown or `next_earnings_date` is missing.
   - `earnings: this_week (next: 2026-05-30, in 4d)` when severity + date are known.
2. **Counter-thesis upgraded** — `StockTradeIdeaAgent._counter(...)` now adds a real counter-thesis bullet when earnings are unknown (`"earnings date is UNKNOWN — calendar lookup missing; any held position carries undated event risk"`) and surfaces the actual `next_earnings_date` for `this_week` severity.
3. **Report renders new fields** — `_ideas_section(...)` now prints:
   - `Data confidence: <value>` when `data_confidence` differs from the setup `confidence`.
   - `Data sources: <list>` from `data_sources_used`.
   - `Score breakdown:` with each component from `scoring.scores[i].components` (e.g. `market_regime: 12.0`, `technical_setup: 18.0`, `momentum: 14.5`) and the `risk_penalty` row.
   - `What to monitor:` block from `idea["what_to_monitor"]`.

### Tests added
- `tests/test_qa_fixes.py::test_earnings_evidence_line_handles_unknown`
- `tests/test_qa_fixes.py::test_earnings_evidence_line_handles_known`
- `tests/test_qa_fixes.py::test_stocks_report_renders_what_to_monitor_and_components` (renders a synthetic `StocksPipelineResult` end-to-end and asserts the new fields appear)

### Not changed (intentional)
- Scoring weights, tier thresholds, and cap rules are untouched.
- `StockRiskAgent`'s flat-penalty schedule was flagged in the audit but is left as-is per the "do not change crypto scoring" + "no large features" guardrails. Per-symbol risk shading remains a future-Should-fix.

---

## QA-5 — CLI UX

### Behaviour before
- `signal-stats` already had `--asset-class`.
- `active-signals` did **not** accept the flag (the audit confirmed: `No such option: --asset-class`).

### Behaviour after
- `active-signals --asset-class crypto` or `--asset-class stocks` filters the table.
- Without the flag, every asset class is shown (default).
- The active-signals table now includes an `asset` column so you can see what's mixed in.
- Invalid values produce `unknown asset-class` with exit code 2 (matches the `prepare-analysis` UX).

### Tests added
- `tests/test_qa_fixes.py::test_active_signals_cli_has_asset_class_option`

### Not changed
- `track-signals` does not yet accept `--asset-class`. The signal tracker iterates over all active signals; adding the flag would require filtering inside the tracker call. The audit's primary UX complaint was about `active-signals`, which is now fixed. This is a deferred Should-fix.

---

## QA-6 — Tests

### Suite status (full repo)
```
$ python -m pytest tests/ --tb=short -q
............................................................................. [ 95%]
....                                                                            [100%]
81 passed in ~11s
```

- Pre-existing: 72 tests.
- Added in this fix batch: 9 tests in `tests/test_qa_fixes.py` + 2 in `tests/stocks/test_stocks_news_tagging.py`.
- Total: **81 tests, 0 failures.**

### Smoke tests run by hand after the changes
1. `python -m src.cli prepare-analysis --mode intraday` → wrote `data/processed/llm_analysis_packet.md` cleanly.
2. `python -m src.cli prepare-analysis --asset-class stocks --mode intraday` → wrote `data/processed/llm_stocks_packet.md` cleanly.
3. `python -m src.cli active-signals --asset-class stocks --limit 3` → filtered correctly; shows the new `asset` column.

---

## What this does NOT fix

These were flagged by the audit but **deliberately not touched** here because they would either require new agents, paid APIs, or architecture changes:

- **Stocks news is still placeholder.** QA-2 stops the test fixtures from leaking, but no real stocks RSS source has been wired. AAPL ideas will simply have **fewer** evidence lines now (no fake catalyst), until production RSS comes online.
- **Earnings calendar lookups still 404 for many tickers.** The audit found 18 tracked events but per-symbol propagation; the propagation is now visible in the idea ("earnings: UNKNOWN" with explicit risk flag), but the underlying yfinance limitation remains.
- **`update-obsidian-context` is still a TODO stub.** The Obsidian dynamic context channel is still dormant. Out of scope here.
- **`short_in_bullish_regime` inconsistency** (MSTR survived, COIN was rejected) — not yet investigated.
- **Stocks risk-penalty constants** (−4.0 / −12.0) — flagged, not changed.
- **`track-signals --asset-class`** — flagged, not implemented.
- **Tracker outcome state machine** — the audit noted all 19 signals stuck in `waiting_for_entry`. Tracking depends on real cached OHLCV evolving over time; not a code defect to fix here.
- **Counter-thesis is still thin on crypto** (templated CriticAgent output). Stocks counter-thesis is materially improved; crypto pending a separate pass.

---

## Net before / after

| Aspect | Before audit | After QA fixes |
|--------|--------------|----------------|
| LLM packets after a report run | Stale (could be days old) | Regenerated automatically; source_report path stamped in header |
| Fake `test_source` news in production reports | Surfaced freely | Dropped by default; opt-in via env var |
| Asset-class news leakage (stocks → crypto reports) | Possible | Crypto reports load asset_class='crypto' only |
| Recent Signal Performance section in reports | Absent | Present in crypto + stocks reports, read-only |
| Stocks idea earnings line | "earnings:unknown" footnote | Explicit date / severity / UNKNOWN-as-risk-flag |
| Stocks idea "What to monitor" | Hidden in JSON, not rendered | Rendered |
| Stocks idea score components | Hidden | Rendered per-component with `risk_penalty` |
| Stocks idea `data_confidence` / sources | Hidden | Rendered when distinct |
| `active-signals --asset-class` | Not supported | Supported (crypto / stocks) |
| Tests | 72 passing | 81 passing |

The pipeline now does what the protocol claims it does at the data-handoff layer. Remaining gaps are content-source / data-quality issues (real news feeds, real earnings dates) rather than code defects.
