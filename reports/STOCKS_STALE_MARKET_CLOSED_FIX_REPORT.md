# Stocks Stale / Market-Closed Signal Validity — Fix Report (P1)

**Date:** 2026-06-04
**Scope:** stocks signal-validity only. No scoring/thresholds/stop-TP/crypto/
Telegram-cooldown changes; no data deleted; no auto-trade.

## Defects (from the 12h audit)
1. **Market-closed intraday entries:** overnight cluster (NVDA/SMCI/AMD/SMH/AAPL,
   created 01:06 UTC / 21:06 ET) issued as actionable intraday A/B longs on
   stale extended-hours prices; all stopped, MFE≈0.
2. **Post-earnings stale setup (AVGO):** AVGO reported earnings and dropped
   ~−13% to ~$417, but the desk re-issued **AVGO A-tier LONG** with a
   **pre-earnings entry 473–478** and `earnings: UNKNOWN` (yfinance calendar
   missed the event).

## Fix — two validity gates in `StockTradeIdeaAgent` (mirrors the PART 17 legal demotion)

### New module `src/stocks/market_calendar.py`
DST-aware canonical session check via `zoneinfo` (America/New_York):
- `is_us_cash_session_open(now)` — Mon–Fri 09:30–16:00 ET, excludes NYSE
  holidays (2025–2026 set), weekend floor. Fails safe if zoneinfo absent.
- `us_session_label(now)` — weekend / holiday / premarket / regular session /
  after-hours.

### New module `src/stocks/earnings_freshness.py`
`load_recent_earnings_news(db, symbols, lookback_hours=36)` — scans `news_items`
for a **past-tense earnings PRINT** (regex: "reported Q_ results", "beats/misses
estimates", "post-earnings", "Q_ … results/revenue/eps", "earnings call", …),
explicitly **excluding future-tense** ("to report", "ahead of", "preview").
Returns the latest print per symbol. Read-only.

### Gate A — market-closed intraday (PART 1)
In `StockTradeIdeaAgent.run(..., now=None)`: if `mode == "intraday"` and the US
cash session is **closed**, any A/B intraday idea is **demoted to C** with
cap_reason **`market_closed_intraday_planning_only`** + an avoid note
("re-evaluate at/after 09:30 ET open"). C-tier = planning/watchlist: registered
but not actionable and never Telegram-pushed (monitor alerts A/B only).
**Swing/invest are untouched.** Market-open behaviour is unchanged.
The stocks report prints a top banner: *"MARKET CLOSED — planning / watchlist
only."*

### Gate B — post-earnings stale setup (PART 2)
For each idea, if a **news-confirmed earnings print** exists within 36h AND the
candidate's own earnings severity is **`unknown`** (calendar blind — the AVGO
case), mark **`stale_post_earnings_setup`**, add a counter/avoid note
("entry/invalidation predate the print; requires fresh levels"), and **demote
A/B → C** (manual review). **News wins over calendar UNKNOWN** (rule #4).
- ETFs (`severity = not_applicable`) are never flagged (rule: ETF earnings N/A).
- A stock with a **known** calendar (`safe`/`today`/`this_week`/`next_session`)
  is **not** flagged stale by this gate — so once the calendar advances past the
  print (severity becomes `safe` with a future date), a freshly recomputed
  post-earnings setup is allowed again (rule #3).
- Future-tense earnings news ("to report next week") is not treated as a print.

## Tests — `tests/test_stocks_market_closed_stale.py` (13, all green)
- calendar: open during RTH, closed overnight/weekend/holiday, labels.
- Gate A: intraday A demoted when closed (+ weekend); kept when open; **swing
  unaffected** when closed.
- Gate B: AVGO (news + UNKNOWN) → demoted C + `stale_post_earnings_setup`;
  UNKNOWN without news → not flagged; **safe** calendar + news → not flagged;
  **ETF not_applicable** → never flagged; future-tense news → not a print.
- Regression updated: `test_clean_aapl_is_not_demoted` now pins a market-open
  clock so Gate A does not interfere with the legal-gate assertion.

## Verification
- Stocks regression (legal/ETF/entity/stocks dir) + new gates: **88 passed**.
- Full suite: see `POST_STOCK_SIGNAL_LOGIC_FIX_VERIFICATION_REPORT.md`.

## Safety
- ✅ No global A/B thresholds changed. ✅ No crypto logic. ✅ No stop/TP geometry.
- ✅ No Telegram cooldown/dedup change. ✅ No filters weakened (gates only DEMOTE
  unsafe/stale setups to C; clean RTH setups unchanged). ✅ No data deleted.
- ✅ No auto-trade. Pipeline calls `run()` without `now` → defaults to live UTC.

## Files
- `src/stocks/market_calendar.py` — NEW
- `src/stocks/earnings_freshness.py` — NEW
- `src/stocks/agents/trade_idea_agent.py` — Gate A + Gate B + `now` param
- `src/stocks/reports/stocks_report_builder.py` — market-closed banner
- `tests/test_stocks_market_closed_stale.py` — NEW (13)
- `tests/test_stocks_legal_persistent.py` — pinned market-open clock (1 test)
