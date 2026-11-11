# 2-Day Loss Analysis + Trade-Data Integrity Audit (read-only)

**Date:** 2026-06-20. **Window:** since stable monitor restart 2026-06-18 15:39 UTC (~2 days).
**Nothing changed** — analysis, conclusions and proposals only. No scoring/TP-SL/entry/routing/filters/live touched.

## 0. Headline — it is NOT "одни убытки"
Deduped to **economic trades** (collapsing duplicate signal_ids) with **entry in the last 2 days**:

| Bucket | n | net R | breakdown |
|---|---|---|---|
| **ACTIONABLE (sent to phone)** | 13 | **−1.0R** | win 3 (+5R) · loss 6 (−6R) · expired 4 (0R) |
| SHADOW — gate (C-tier/scalp/stocks-swing) | 19 | −3.0R | expired 14 · loss 4 · win 1 |
| SHADOW — sector-cap (stocks) | 6 | −1.0R | expired 5 · loss 1 |
| SHADOW — late-entry (latency) | 2 | **+4.0R** | win 2 |
| SHADOW — Telegram error (not delivered) | 1 | −1.0R | loss 1 |

So the actionable paper book is **3 wins / 6 losses / 4 expired = net −1R** on **9 resolved** trades.
That is loss-tilted but it is **noise-level**, not a blown-up book. Expectancy ≈ −0.1R/trade on n=9.
The "all losses" feeling comes from recency: 06-20 fired 5 stop alerts (2 intraday + 3 swing) close together.

## 1. Why the losses happened (the 6 actionable stops)
| sym | dir | mode | playbook | regime | R | MFE | MAE |
|---|---|---|---|---|---|---|---|
| ONDO | short | intraday | failed_bounce_short | bearish tr | −1 | 0.09 | −1.06 |
| JTO | long | intraday | intraday_catalyst | (blank) | −1 | 0.49 | −1.06 |
| EDEN | long | swing | swing_narrative | (blank) | −1 | 0.87 | −1.03 |
| TAO | short | swing | failed_bounce_short | (blank) | −1 | 0.58 | −1.55 |
| ORDI | long | intraday | intraday_catalyst | (blank) | −1 | 0.31 | −0.98 |
| EIGEN | long | swing | swing_narrative | (blank) | −1 | 0.50 | −1.03 |

**Patterns (hypotheses, sample too small to "prove"):**
1. **Give-back stops dominate.** 4 of 6 losers reached **+0.5R…+0.87R favorable first**, then fully reversed to −1R (JTO, EDEN, TAO, EIGEN). The book has **no break-even / partial protection**, so half-way winners become full losers. (NB: a prior regime-wide shadow replay found BE/partial net-negative — so this is a *re-test candidate*, not a confirmed fix.)
2. **Swing-narrative longs are the weakest cohort:** 0 wins / 2 losses / **4 expired** (EDEN, EIGEN lost; ALICE, AXS, BEL, BTC expired). All longs; none reached TP. The 3 wins were elsewhere (XLM/MEGA failed_bounce shorts +3R; MET intraday_catalyst +2R).
3. **Tape was choppy/weak.** Of the entered crypto signals that *recorded* a regime, all were **range/chop or bearish trend** — entering longs into chop is consistent with the give-back stops. (Caveat: regime was blank on most rows — see §2.3.)
4. **Direction is not the cause** — both longs and shorts lost; it is setup/tape, not a long/short bias.

## 2. DATA-INTEGRITY findings (components feeding the analysis) — the important part
The user asked to verify the analysis inputs. **Several are wrong or stale**, so confident attribution is currently **not possible**:

### 2.1 signal_id duplication → counts inflate up to ~10×
The same economic setup is registered under multiple signal_ids. A naive "latest-row per signal_id" count over *recently-checked* rows returned **147 wins / 215R**; after dedup-by-setup + entry-in-window it is **~4 wins**. Any report/dashboard that counts by signal_id (not by economic setup) massively overstates both wins and losses. The latest-outcome read model fixes per-signal_id double counting but **not** cross-signal_id setup duplication. **Analysis must dedupe by (symbol,direction,mode,entry,stop) and filter by entry time.**

### 2.2 Catalyst / news linkage is broken for entered trades  ⚠ highest-value finding
- `signal_catalyst_labels` is **frozen**: all 1016 rows stamped a single time **2026-06-15T16:32:53**; **0** of the last-2-day entered signals have a label. It is a *derived/display* table that was backfilled once and is **not refreshed by any cycle step** → the Obsidian "derived catalyst labels" panel and any label-based analysis are stale since 06-15.
- On entered crypto setups: `news_supported`=4/27, `telegram_supported`=**0/27**.
- **But `news_items` is fresh and HAS direct hits for the losers:** ORDI 20 items, ONDO 10, EDEN 8, TAO 2 (latest 06-20). So `news_supported=0` is **wrong** for those symbols — exactly the regression signature you flagged on ASTER. **Do NOT trust the "no catalyst" flag**; the catalyst→signal enrichment is under-firing at scan/score time, so we are trading several news-driven names blind and cannot analyse "catalyst vs no-catalyst" from the DB.

### 2.3 market_regime missing on ~69% of entered crypto
20 of 29 entered crypto setups have **blank** `market_regime`; only 9 carry one (bearish trend / range-chop). Loss-by-regime analysis is therefore unreliable — the regime field is not consistently persisted onto the signal.

### 2.4 "expired 0R" hides near-winners (validity-window / OHLCV coverage)
**7 of 23 expired trades reached MFE ≥ 0.8R** before expiring at 0R (e.g. ALICE swing MFE 1.12R). For swing especially, the validity window (and/or the rolling OHLCV coverage, 1h≈9d) closes the trade before TP/SL resolves, so the book looks worse than reality and real R is uncaptured. Treat "expired" as *unresolved*, never as a true 0R outcome.

### 2.5 Telegram delivery gaps mis-attribute a few trades
Of 35 paper-entry alerts: 13 sent, 13 shadow_only(scalp), 6 shadow_sector_cap(stocks), **2 late_shadow**, **1 error:ReadTimeout**. The 2 late-shadow trades were **winners (+4R)** routed out by latency; the 1 ReadTimeout actionable entry never reached the phone (and lost). "What the operator saw" ≠ "what the system decided" — reconcile via `telegram_status`, not raw alert counts.

## 3. Shadow trades — verdict
Shadow buckets are mostly **expired** (unresolved) with small net-negative R (gate −3R, sector-cap −1R), i.e. the blocked cohorts (C-tier, crypto scalp, stocks swing/invest) are **correctly kept out of the actionable book** — no evidence they should be promoted. The **only** place shadow cost us was **latency** (late_shadow = 2 winners, +4R) — a delivery-speed problem, not a strategy problem.

## 4. Conclusions
1. **No edge is broken.** −1R on 9 resolved actionable trades is statistical noise; far below the ≥15/≥30 sample needed to judge anything. Verdict: **NEED_MORE_DATA**.
2. The loss *texture* is real and worth watching: **give-back stops** + **swing-narrative longs into a chop/bearish tape**.
3. **The bigger problem than the losses is the trade-data plumbing**: catalyst linkage stale/under-firing, regime often blank, expired hides near-winners, signal_id duplication, and delivery gaps. Until these are fixed, **loss attribution cannot be trusted**.

## 5. Proposals (no changes made — for approval)
**A. Fix the analysis inputs first (operational, not trade-logic):**
- A1. Refresh `signal_catalyst_labels` per cycle (or stop reading the stale table) **and** investigate why `news_supported`/`telegram_supported` is ~0 on crypto entries while `news_items` has hits — verify the symbol-mapping/join at scan time. *(highest priority)*
- A2. Persist `market_regime` on every signal at creation.
- A3. In all trade reports/dashboards, dedupe by **economic setup** and key off **entry time**; reconcile alerts by `telegram_status`.
- A4. Report "expired" separately as **unresolved**, and surface `expired-with-MFE≥0.8R` as "uncaptured near-winners" (already partly in the Friday checklist).

**B. Strategy hypotheses — only to *measure in shadow*, do NOT change live yet:**
- B1. Track a shadow **break-even-after-+0.6R** variant specifically on the give-back losers, and re-decide once n≥15 resolved.
- B2. Track **swing-narrative-long** as its own cohort; if it stays 0-win after ~15 resolved, consider watchlist-only (shadow first).
- B3. Reduce **entry-detection latency** so late_shadow winners aren't lost (this is the one shadow finding with positive R).

**C. Re-evaluate on Friday / at n≥15** resolved actionable trades — not before.

## Verdicts
`NOT_ALL_LOSSES (3W/6L/4exp, −1R)` · `SAMPLE_TOO_SMALL_NEED_MORE_DATA` · `CATALYST_LINKAGE_STALE` · `REGIME_FIELD_SPARSE` · `EXPIRED_HIDES_NEAR_WINNERS` · `SIGNALID_DUP_INFLATES_COUNTS` · `NO_TRADE_LOGIC_CHANGE`
