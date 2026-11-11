# Stocks Signals — 12h Outcome Audit (READ-ONLY)

**Window:** last ~14h. Regime: **bullish** throughout (VIX ~16, breadth 100% on
indices). Unique setups deduped. Headline = **A/B only**; C-tier separate.

## A/B headline (week, signal-stats)
`A/B: n=294 PF 1.30 avgR +0.074 totalR +16 winrate 20%` ·
`C-tier: n=138 PF 1.15 totalR +4` (watchlist, separate) ✅.
→ A/B softened from ~1.96 (12h ago) to **1.30** — driven by a cluster of
overnight stops (below).

## A/B signals (14h) — key outcomes
| time(UTC) | symbol | mode | tier | score | status | R | mfe | mae |
|---|---|---|---|---|---|---|---|---|
| 06-03 01:06 | NVDA | intraday | B | 78.0 | stopped | −1 | 0.23 | −1.16 |
| 06-03 01:06 | SMCI | intraday | B | 71.3 | stopped | −1 | 0.00 | −1.34 |
| 06-03 01:06 | AMD | intraday | B | 79.1 | stopped | −1 | 0.12 | −1.32 |
| 06-03 01:06 | SMH | intraday | B | 77.9 | stopped | −1 | 0.48 | −1.37 |
| 06-03 01:06 | AAPL | intraday | B | 77.4 | stopped | −1 | 0.17 | −1.05 |
| 06-03 01:06 | XLK | intraday | B | 73.7 | **tp1** | **+1** | 1.34 | −0.93 |
| 06-03 01:06 | QQQ | intraday | B | 69.5 | **tp1** | **+1** | 1.06 | −0.84 |
| 06-03 09:35 | AVGO | intraday | B | 69.7 | **tp1** | **+1** | 1.17 | −0.38 |
| 06-03 09:35 | SMCI | intraday | A | 82.3 | stopped | −1 | 0.00 | −1.34 |
| 06-03 13:46 | AAPL | intraday | A | 90.0 | stopped | −1 | 0.40 | −1.11 |
| 06-03 13:46 | AMD | intraday | A | 87.5 | triggered | 0 | 1.25 | −0.14 |
| 06-03 13:46 | SMH | intraday | A | 82.5 | triggered | 0 | 0.83 | −0.07 |
| 06-03 15:00 | TSLA | intraday | B | 77.1 | stopped | −1 | 0.12 | −1.07 |
| 06-04 00:29 | AVGO | intraday | A | 89.7 | waiting | — | — | — |
| 06-04 00:29/09:31 | LLY/AMD/SMH/XLK | intraday | A/B | 73–90 | waiting | — | — | — |

## Fix verification (live)
- **SMCI legal gate:** ✅ latest SMCI rows are **C-tier with `ACTIVE LEGAL
  HEADLINE RISK (class_action, indictment, securities_fraud)`**. The only
  A-tier SMCI (06-03 09:35) predates the code reload; post-reload SMCI is C.
  No other stock A/B carries a legal marker.
- **ETF earnings false-positive:** ✅ report shows `earnings: N/A (ETF — does
  not report earnings)` for SMH/XLK/QQQ; no "UNKNOWN" penalty.
- **A-tier worse than B:** ✅ confirmed — A PF ~0.2–0.29 (−5R) vs B PF ~1.4–2.2
  (+33→+56R historically). **B remains the workhorse.**
- **C-tier watchlist-only + separated:** ✅ headline split working.
- **ETF vs single-name:** single names carry the action; ETFs (SMH/XLK/QQQ)
  mixed.

## ⚠️ NEW issue Opus caught (P1) — AVGO stale post-earnings
- AVGO **reported Q2 FY2026 and dropped ≈−13% to ~$417**, but the stocks report
  **re-issues AVGO A-tier LONG 89.7 with entry zone 473–478 and
  `earnings: UNKNOWN`** — entry ~13% above market. The earnings-risk agent's
  yfinance calendar **missed AVGO's event** (UNKNOWN, not blocked), so a
  stale pre-earnings setup persists. → `TODO-stocks-stale-postearnings` (P1).

## Why losses lost (classified)
- **#11 market-closed / stale overnight data (PRIMARY):** the 06-03 **01:06 UTC
  (21:06 ET)** cluster — NVDA/SMCI/AMD/SMH/AAPL all stopped, **MFE ≈ 0.0–0.48**
  (never went favorable) — are *intraday* signals generated **after the cash
  session closed**, on stale/extended-hours prices; the next-session move hit
  the stops. Entry/stop computed on non-actionable data.
- **#9 earnings/event risk (AVGO):** stale pre-earnings entry, sell-the-news.
- **#10 legal (SMCI):** correctly demoted to C now; the pre-fix A-tier SMCI lost.
- **Not sector rotation / not bad RS:** regime bullish, names are RS-positive
  leaders (the gate-sim already confirmed A/B are RS-filtered). The losses are
  **timing/stale-data**, not bad candidate selection.

## Net
Stocks A/B is **+16R, PF 1.30** (week) — positive but softened by overnight
stop-outs and the AVGO staleness. **B-tier healthy; A-tier overpromoted; the
big actionable defect is generating/holding intraday stock signals while the US
market is closed on stale prices.**
