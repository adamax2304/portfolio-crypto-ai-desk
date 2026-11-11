# Stocks Invest — Watchlist-Only Soft Pause (Fix Report)

**Date:** 2026-06-09 · **Scope:** Mirror the existing stocks-swing pause gate for stocks-invest. No scoring/threshold/TP/SL changes. No crypto changes. No auto-trade.
**Audit reference:** [STOCKS_INVEST_VIABILITY_AUDIT.md](STOCKS_INVEST_VIABILITY_AUDIT.md) + [MODE_ROUTING_DECISION_RECOMMENDATION.md](MODE_ROUTING_DECISION_RECOMMENDATION.md).

## 1. What changed

### 1.1 Gate (mirror of swing-pause)
File: [src/stocks/agents/trade_idea_agent.py](src/stocks/agents/trade_idea_agent.py)

Added an `if mode == "invest":` block right after the existing `if mode == "swing":` block (Gate D). When mode is invest:
- The `cap_reasons` list gets `stocks_invest_paused_after_mode_viability_audit` appended.
- If the candidate is A or B, it is demoted to **C** (the idea is not deleted — it stays visible as watchlist), and a human-readable demotion reason is appended to `cap_reasons`.
- The `avoid_conditions` list gets the explanatory note: "Stocks invest is temporarily watchlist-only after mode viability audit: 0W/7L over 14d; same failure mode as paused stocks swing."

### 1.2 Report banner
File: [src/stocks/reports/stocks_report_builder.py](src/stocks/reports/stocks_report_builder.py)

Added a sibling `if result.mode == "invest":` banner right after the existing swing banner. Renders only on invest runs; never appears on intraday or swing runs.

### 1.3 No other surfaces touched
- `src/stocks/agents/scoring_agent.py` — unchanged.
- `src/stocks/pipelines/stocks_pipeline.py` — unchanged.
- All TP/SL/risk geometry — unchanged.
- All stocks-intraday paths — unchanged.
- All crypto paths — unchanged.

## 2. Scope guardrails (verified)
- `if mode == "invest":` block is strictly scoped to `asset_class=stocks` (the agent is `StockTradeIdeaAgent` — crypto goes through a different path).
- Stocks intraday signals are untouched by the new gate (verified by `test_intraday_not_invest_paused`).
- Stocks swing keeps its own existing pause (verified by `test_swing_not_carrying_invest_cap_marker` — swing demotes to C via swing gate; invest cap marker does NOT appear on swing ideas).
- Crypto signals untouched (verified by full regression).

## 3. Tests
File: [tests/test_stocks_invest_pause.py](tests/test_stocks_invest_pause.py) — 10 new tests:

| Test | Asserts |
|---|---|
| `test_invest_Atier_demoted_to_C` | A-tier invest demotes to C |
| `test_invest_Btier_demoted_to_C` | B-tier invest demotes to C |
| `test_invest_demotion_records_demote_reason` | Both the marker and "tier demoted A→C" appear |
| `test_invest_existing_C_still_capped_not_deleted` | C-tier invest stays present with cap |
| `test_invest_carries_watchlist_avoid_note` | avoid_conditions contains the explanatory note |
| `test_intraday_not_invest_paused` | Stocks intraday A-tier stays A; invest cap not on intraday |
| `test_swing_not_carrying_invest_cap_marker` | Swing keeps swing cap; invest cap absent |
| `test_report_renders_invest_watchlist_note` | Invest report has the banner with "0W/7L over 14d" |
| `test_report_intraday_has_no_invest_note` | Intraday report has no invest banner |
| `test_report_swing_has_no_invest_note` | Swing report has swing banner only, no invest banner |

Existing tests updated for behavior change:
- `tests/test_stocks_swing_pause.py::test_invest_not_swing_paused` renamed to `test_invest_not_affected_by_swing_cap` — now asserts only that the *swing* cap marker is absent on invest (the invest cap is expected via the new gate).
- `tests/test_stocks_market_closed_stale.py::test_invest_not_affected_by_market_closed` renamed to `test_invest_not_affected_by_market_closed_or_swing_caps` — now asserts only that the market-closed and swing markers don't leak onto invest (invest is C-tier by its own gate; tested elsewhere).
- `tests/stocks/test_stocks_scoring_and_ideas.py::test_trade_idea_agent_produces_stocks_asset_class` — relaxed `tier in ("A","B")` to `tier in ("A","B","C")` for swing mode (the swing pause caps it to C); added a positive check for the swing cap marker when tier=C.

All 25 invest/swing/scalp pause tests + 15 regression tests in the focused subset pass. Full regression run: 477 passed, 2 failed before the test updates (the two tests called out above); 0 failures after.

## 4. Verification — live invest report
Ran `python -m src.cli stocks-invest-report` against fresh data. Output:
```
Regime=bullish | A/B ideas=0 | C watchlist=10 | rejected=15 | signals registered=0
Stocks LLM packet refreshed: data/processed/llm_stocks_packet.md
```
- **A/B ideas = 0** ✅ — gate is actively demoting.
- **C watchlist = 10** ✅ — ideas stay visible as research.
- **signals registered = 0** ✅ — no Telegram A/B alert path activated.
- Report renders the new banner on line 8:
  > `> **STOCKS INVEST — watchlist / research only after mode viability audit: 0W/7L over 14d, same failure mode as paused stocks swing.** ...`
- LLM packet refreshed in lockstep.

## 5. What this fix does NOT do
- It does not change invest TP/SL/horizon — the 30-day validity window and stop placements remain as-is.
- It does not delete or block invest scanning/scoring — invest candidates are scored normally; the gate sits at the trade-idea layer, after scoring.
- It does not affect intraday, swing (swing has its own pause), or any crypto mode.
- It does not suppress C-tier reporting — invest C-tier ideas still appear on the report for research.
- It does not auto-trade or restart the scheduler.

## 6. Re-audit trigger
Per [MODE_ROUTING_DECISION_RECOMMENDATION.md](MODE_ROUTING_DECISION_RECOMMENDATION.md), re-audit invest **after 20 closed C-tier invest outcomes** (current count: 8 of 39 closures across 14d). Estimated 1 full US trading week of accumulation, then revisit.

## Final
```
STOCKS_INVEST_WATCHLIST_PAUSE_DEPLOYED
```
