# Daily Expired / No-Stocks / Loss Review — 2026-06-18

**Type:** read-only diagnostic over the live DB (`db/crypto_ai_desk.sqlite`). **No trading logic / scoring / TP-SL / routing / filters changed.** Saved as context for tomorrow's and Friday's analysis.

> **Data caveat:** the scheduler had a gap today (2 clean cycles, then the session-launched loop stopped; restarted under the new `CryptoAIDeskMonitor` persistence task at ~15:39 UTC). No fresh cycles 12:29→15:39 UTC, so some caches were stale for part of the day. Treat the forward-test clock as restarting ~15:39 UTC.

## Executive Summary
- Expired looks **mostly old-tail**, not today's fresh failure.
- **Stocks scanner is working** (22 signals today); the perceived absence is shadow/actionability, not a bug.
- **Crypto side is thin** (only 3 new signals).
- **Filters rejected many risky crypto ideas** (70 rejects: no-chase / mixed regime / squeeze-risk cap).
- **Losses came from crypto pullback longs** (7 actionable B losses, −7R).
- **No production change recommended today.**

## Expired Family

Expired family = `expired` / `missed_no_entry` / `stale_before_entry` / `entry_moved_away`. Counted by `updated_at` = today (status finalized today).

| status | count | interpretation | symbols |
|---|---|---|---|
| `expired` | 11 | validity window elapsed | ZRO, ID (crypto); COIN×2, LLY, MSFT, PLTR, SMCI, XLK, XOM (stocks) |
| `stale_before_entry` | 8 | entry not reached / signal went stale | AMD, IWM, JPM×2, NFLX, SMH, XLK, XLY |
| `entry_moved_away` | 2 | price ran away from entry | XOM, NFLX, JPM |
| **total** | **21** | | 2 crypto · 19 stocks |

- Most were **old signals** created 06-11…06-17 (esp. swing/invest created 06-11 finally expiring after their long window).
- **Only 4 were created today** (XOM/IWM/JPM/XLK intraday from the 09:35 batch — stale / moved-away).
- `missed_no_entry` = 0 today (folded into stale/expired).

## Missed Opportunity Review

Favorable excursion (MFE) after the signal expired:

| symbol | mode | MFE after expiry | MAE | read |
|---|---|---|---|---|
| **ZRO/USDT** long | crypto intraday | **+3.28R** | −0.86R | clear missed winner |
| ID/USDT long | crypto intraday | +0.91R | −0.91R | noisy / symmetric chop |
| COIN long | stocks intraday | +0.91R | −1.05R | likely stop-first |
| MSFT short / XLK long / LLY long | stocks | +0.58…+0.80R | partial | favorable but not enough |

**Conclusion:** Only **ZRO** is a clear missed opportunity. **Do not loosen validity/entry rules from one case.**

## Stocks Review
- Stocks signals today = **22**.
- **B-tier = 6**, all `triggered`/open (actionable-eligible; outcomes still pending).
- **C-tier = 16**, shadow/review-only (blocked by `decide_paper_entry`; not in actionable Telegram).
- Stocks scanner / data source likely **working** (batches at 09:35 and 16:00 UTC).
- Issue is **visibility/actionability, not scanner failure**.

**Conclusion:** No stocks-monitor bug confirmed. Continue observing **B-tier outcomes** (not the raw stocks count).

## Crypto Review
- Only **3 crypto new signals** today.
- Rejected crypto ideas = **70**:
  - no-chase ("price > 2 ATR from EMA20; do not chase") = **26**
  - mixed regime ("breakout failure risk elevated") = **18**
  - short-squeeze risk → capped to C (thin liquidity / no derivatives / high upper wick) = **24**
  - derivatives unavailable (insufficient data) = **1**
  - counter-trend (RS-leader long vs bearish tape) = **1**

**Conclusion:** Crypto was thin because filters rejected **stretched / mixed / squeeze-risk** setups. This is **expected behavior**, but the remaining pullback longs still lost.

## Loss Review

Actionable crypto non-scalp B losses (each **−1.0R**):

| symbol | mode | playbook (setup) |
|---|---|---|
| BCH/USDT | intraday | pullback long |
| ZEC/USDT | intraday | pullback long |
| SUI/USDT | intraday | pullback long |
| GPS/USDT | intraday | pullback long |
| HOME/USDT | intraday | breakout long |
| BANK/USDT | swing | pullback long |
| ALLO/USDT | swing | pullback long |

**Total: −7R.** Shadow-only losses (excluded from the paper book): MITO/USDT scalp + all C-tier stocks (`continuation`).

**Conclusion / main hypothesis:** the **pullback-long playbook may need review during weak/mixed/stretched tape**, especially when universe-level rejects are dominated by **no-chase / mixed-regime / squeeze-cap**. Hypothesis only — **no change today**.

## Intelligence / Shadow Notes
- Intelligence fields are **missing on today's closed losses** because those alerts were emitted **before the intelligence layer reload** (stale in-memory module pre-restart).
- **Forward alerts (post-restart) should contain intelligence fields.**
- Tomorrow/Friday review should **compare new intelligence labels against outcomes** — only on alerts emitted after the monitor restart/reload.
- Circuit breaker: no warning today (last dry-run `would_pause=False`, calm). Squeeze classifier cautionary phases present (`unwind`, `post_unwind_chop`); no explicit "distribution" phase.

## Friday Review Hypotheses
1. If crypto universe rejects are dominated by no-chase / mixed / squeeze-risk, **remaining pullback longs may need review-only / lower confidence**.
2. **Separate expired old-tail from fresh expired** to avoid false panic.
3. **ZRO missed winner** should be tracked but is **not enough to loosen** entry/validity globally.
4. **Stocks are not absent** — check **B-tier outcomes**, not the raw "stocks count".
5. **Intelligence labels** should be evaluated only on alerts emitted **after the monitor restart/reload**.

## Decision
- `NO_TRADE_LOGIC_CHANGE_TODAY`
- `NEEDS_FRIDAY_REVIEW`
- `MONITORING_CONTEXT_SAVED`
- `WATCH_PULLBACK_LONGS_IN_WEAK_TAPE`
- `DO_NOT_LOOSEN_EXPIRED_RULES_YET`
