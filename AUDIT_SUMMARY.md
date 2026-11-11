# Audit Summary — stocks module

Date: 2026-05-25
Full report: [AUDIT_STOCKS_MODULE.md](AUDIT_STOCKS_MODULE.md)

## Headline

- **Crypto pipeline:** not regressed. 35/35 existing tests pass. Live monitor kept firing during the build. No crypto agent / collector / scorer / report file was touched.
- **Stocks pipeline:** Stages 1–7 delivered. Runs end-to-end. Produces tier-labeled A/B/C/rejected ideas. Persists signals tagged `asset_class='stocks'`. Builds Markdown reports and a dedicated LLM packet.
- **Quality bar:** **MVP**. About a third of the documented scoring/risk surface is placeholder or unenforced.

## Overall risk: **Medium**

- One **Critical** issue blocks the stocks feedback loop.
- Five **High** issues affect signal quality.
- ~15 **Medium** and ~10 **Low** issues are polish/coverage gaps.

## Top 5 issues to fix first

1. **Critical — `track-signals` is not asset_class-aware.** Stocks signals will never get outcomes because the tracker looks for OHLCV under `data/raw/ohlcv/{exchange}/`, not `data/raw/stocks/`. Every stocks signal is silently skipped as `no_ohlcv`. ([src/signals/tracker.py](src/signals/tracker.py))
2. **High — Stocks news is dry.** RSS collector never tags news with `asset_class='stocks'`; `news_items` has 0 stocks rows. `news_catalyst` weight is dead. ([src/data_collectors/rss_news_collector.py](src/data_collectors/rss_news_collector.py:91))
3. **High — `volume_relative_volume` is hardcoded `0.5`.** No real intraday relative-volume signal. Component cannot discriminate. ([src/stocks/agents/scoring_agent.py](src/stocks/agents/scoring_agent.py))
4. **High — `data_confidence` is hardcoded `0.8`.** Doesn't reflect actual data coverage; missing intraday frames score the same as full coverage.
5. **High — "Both index AND sector contradict → reject" rule is configured but not implemented.** ([config/stocks/risk.yaml](config/stocks/risk.yaml) → confirmation.both_contradict)

## What works (verified live)

- All 6 new stocks CLI commands run without errors: `stocks-update-data`, `stocks-intraday-report`, `stocks-swing-report`, `stocks-invest-report` (code path; not full smoke this session), `stocks-earnings-scan`, `stocks-candidate-debug`.
- `prepare-analysis --asset-class stocks` writes the real packet (not a stub).
- `signal-stats --asset-class stocks` correctly filters; `--asset-class crypto` excludes stocks rows; bare command unions both.
- Schema migration ran cleanly on the existing live SQLite (1042 crypto trade_ideas, 425 rejected_ideas, 16 watchlist alerts, etc all backfilled to `'crypto'`).
- Full pytest suite: 48/48 (35 crypto + 13 stocks).

## What is documented but not implemented

| Surface | Configured in | Implemented? |
|---|---|---|
| Gap rules (require_retest, reject_chase) | risk.yaml | ✗ |
| Liquidity floors (avg dollar volume, rel vol floor) | risk.yaml | ✗ |
| Macro calendar / event-day caution | risk.yaml | ✗ (no collector) |
| "Both contradict → reject" | risk.yaml | ✗ |
| Real `volume_relative_volume` | scoring.yaml | ✗ (0.5 placeholder) |
| Real `data_confidence` | scoring.yaml | ✗ (0.8 placeholder) |
| Real `earnings_risk_adjustment` (as component) | scoring.yaml | ✗ (0.5 placeholder; real effect comes from risk_penalty) |
| Fundamental snapshot | spec | ✗ (invest mode is technicals-only) |
| Paid-API key stubs | spec | ✗ (no `.env.example`) |
| `prompts/system/` asset-class-aware protocols | spec | ✗ |
| Stocks `Signal_Performance/` Obsidian folder | mirror of crypto | ✗ |
| Stocks news RSS source list | spec | ✗ |

## What is fragile but functional

- yfinance is unofficial and rate-limited. No 429 retry. No cache TTL.
- `EarningsCalendarCollector` always sets `report_time='unknown'` from yfinance; manual CSV is the only way to set BMO/AMC.
- `EarningsRiskAgent` uses calendar days, not trading days (Friday-to-Monday = 3, not 1).
- `StockTechnicalAgent` uses a rolling-26-bar VWAP rather than session-anchored.
- Several `__init__.py` files in stocks subpackages are empty placeholders.

## Files / locations to check first

- [src/signals/tracker.py](src/signals/tracker.py) — fix asset_class routing (#1)
- [src/data_collectors/rss_news_collector.py](src/data_collectors/rss_news_collector.py) — add asset_class on save (#2)
- [src/stocks/agents/scoring_agent.py](src/stocks/agents/scoring_agent.py) — fix placeholder components (#3, #4)
- [src/stocks/agents/risk_agent.py](src/stocks/agents/risk_agent.py) — implement both-contradict rule + gap + liquidity (#5, #6, #7)
- [src/stocks/agents/company_news_agent.py](src/stocks/agents/company_news_agent.py) — clean up dead conditional (#8)
- [src/stocks/llm_packet.py](src/stocks/llm_packet.py) — pull Obsidian rules excerpts (#17)

## Bottom line

The stocks module compiles, runs, and integrates correctly with the shared infrastructure (storage, signal tracking schema, LLM packet pipeline). It is **isolated from crypto** as required. But it is **not production-ready** in the sense that real money should not act on its A/B-tier output today, because:
- Several score components are placeholders.
- News coverage is empty.
- Several risk gates are configured but not enforced.
- And — most importantly — the **signal performance feedback loop does not work for stocks** until `tracker.py` is fixed.

Fix the five items in "Top 5 issues to fix first" and the module moves from MVP to "usable for real-money screening with caveats."
