# Post Stock-Signal-Logic Fix — Verification Report (P1)

**Date:** 2026-06-04 · **Mode:** no-trade verification. No scoring/threshold/
stop-TP/crypto/Telegram-cooldown changes; no data deleted; no auto-trade.

## Tests
| Suite | Result |
|---|---|
| `tests/test_stocks_market_closed_stale.py` (NEW) | **13 passed** |
| stocks regression (legal/ETF/entity/stocks dir + new) | **88 passed** |
| **Full suite** `pytest -q` | **438 passed, 0 failed** (was 425; +13) |

Updated 1 existing test (`test_clean_aapl_is_not_demoted`) to pin a market-open
clock so the new market-closed gate doesn't interfere — legitimate, expected.

## Live no-trade verification (US cash session CLOSED at run time)
Run clock: 11:10 UTC = **premarket** → `is_us_cash_session_open()=False`.

`stocks-intraday-report` (fresh, new code) →
`data/reports/stocks/intraday/2026-06-04_11-10_stocks_intraday_report.md`:
- **"MARKET CLOSED — planning / watchlist only" banner present** ✅
- **0 actionable A/B intraday idea headers** ✅ (all demoted)
- LLM packet refreshed ✅ (`registered=5`)

Registry check (just-registered intraday signals) — names that score A/B are all
**C-tier** because the market is closed:
```
XLK 73.7→C | SMH 77.9→C | AMD 79.1→C | LLY 84.3→C | AVGO 89.7→C
```
AVGO C-tier row carries:
- cap_reasons: `market_closed_intraday_planning_only: US cash session closed …`
  + `tier demoted A→C: market_closed_intraday_planning_only` ✅
- no_entry_conditions: `"US market closed — do not treat as a live intraday
  entry; re-evaluate … at/after the cash open (09:30 ET)."` ✅

Because they are C-tier, they are **not Telegram-actionable** (monitor alerts
A/B only) and are recorded as planning/watchlist — exactly the intended outcome.

## Gate-by-gate verification matrix
| # | Requirement | Result | Evidence |
|---|---|---|---|
| 1 | No actionable A/B stocks intraday when market closed | ✅ | live report: banner + 0 A/B ideas; AVGO 89.7→C |
| 2 | AVGO stale pre-earnings blocked/demoted | ✅ | unit `test_avgo_stale_post_earnings_demoted` (market-open isolates Gate B) + live AVGO detector found the June-3 21:04 ET print |
| 3 | SMCI legal gate still works | ✅ | `test_stocks_legal_persistent` green; live scheduler reports show SMCI C + legal flag |
| 4 | ETF earnings N/A still works | ✅ | `test_stocks_etf_earnings` green; full-fetch report shows "N/A (ETF…)" |
| 5 | Normal RTH stock intraday still works | ✅ | `test_intraday_Atier_kept_when_market_open` (A stays A); swing unaffected when closed |
| 6 | LLM packet updates | ✅ | "Stocks LLM packet refreshed" on the run |
| 7 | No auto-trade | ✅ | report/registry only; no orders |

## Live detector evidence
- Gate A: `is_us_cash_session_open(now)=False` at 11:04 UTC (premarket) → active.
- Gate B: `load_recent_earnings_news(['AVGO',…])` → **AVGO** "Broadcom outlines
  $29.4B Q3 revenue outlook…" published 2026-06-03 21:04 ET (within 36h) — the
  news-confirmed print that invalidates a calendar-UNKNOWN AVGO setup.

## Safety checklist
- ✅ Global A/B thresholds unchanged. ✅ Crypto logic untouched. ✅ Stop/TP
  geometry untouched. ✅ Telegram cooldown/dedup untouched. ✅ Filters only
  DEMOTE stale/closed-session setups to C (clean RTH setups unchanged). ✅ No
  data deleted. ✅ No auto-trade. ✅ Scheduler not restarted (alive — runs old
  code until its next natural restart; new code is live for all fresh CLI/manual
  runs and will be live on the next scheduler restart).

## Note
A long-running `--update` manual report was throttled by yfinance contention
with the live scheduler; the `--no-update` (cached-bars) run above provided the
same end-to-end proof faster and is authoritative for this verification.

## Final answer
```
READY_AFTER_STOCK_SIGNAL_LOGIC_FIX
```
