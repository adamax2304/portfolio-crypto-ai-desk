# Opus Enriched Review — Auto Cycle 12:42 EEST

- **Generated:** 2026-06-04 12:42 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`)
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-04_0839.md` (≈4 h ago — §4)
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim cited in §13 with source + date + URL. AVGO post-earnings price (~$417, −12.99%) and BTC sub-$63k print independently WebFetch-verified (StockTitan, CoinDesk).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from local OHLCV/ATR/EMA report fields + cited external prints.
- **Clock:** 12:42 EEST Thursday. **US regular session is CLOSED** (after-hours/pre-market; regular session reopens ~16:30 EEST). Stock signals below are NOT executable this cycle; crypto trades 24/7 and is the only actionable class right now.
- **Advisory only. No auto-trade.**

---

## 1. Executive Summary

- **No clean actionable A-grade candidate this cycle.** Stocks are closed and the actionable semi list stays poisoned by the AVGO post-earnings read-through; crypto regime has **deteriorated further from "bearish trend" to "high-volatility danger (danger)"** — BTC/ETH downtrend, breadth above EMA20 **22.9%** (down from 35.4% last cycle), BTC ATR percentile **98 (elevated)**. Posture: **watchlist / no-trade**; this run the desk produced **zero fresh A/B-tier crypto setups** at all (last cycle had one GPS short).
- **Persisting contradiction (now externally price-confirmed): the regenerated stocks report (09:31 UTC) STILL re-issues AVGO as A-tier LONG 89.7 with a stale pre-earnings entry zone (473.25–478.07) and `earnings: UNKNOWN`** — even though AVGO reported Q2 FY2026 the prior evening and **sold off ~−13% to ≈$417**. AVGO printed record rev **$22.2B (+48% YoY)**, non-GAAP EPS **$2.44 (+54%)**, AI-semi **$10.8B (+143% YoY)**, strong Q3 guide **~$29.4B (+84% YoY)** — yet fell on a textbook sell-the-news (full-year AI target not raised). **The A-tier long entry zone now sits ~13% ABOVE where the stock actually trades.** **Verdict for AVGO: AVOID / MANUAL REVIEW REQUIRED.** This is the 4th consecutive review flagging it; the desk has not self-corrected (TODO-stocks-stale-postearnings, now with a hard price gap).
- **Negative semi read-through into the cash open persists.** The desk's other semi longs — **AMD A 90 (also B 79.1), SMH B 77.87 (A 82 triggered), XLK B 73.7** — are technically bullish *against* the AVGO catalyst and carry **gap-down / sympathy risk at the open.** Do not chase fresh semi longs pre-open. AMD is the strongest-RS name (RS vs SPY +48.5%, earnings safe) and the best post-open reassessment — but only after the AVGO gap is absorbed.
- **LLY (A-tier long 84.31) is the cleanest stock idea** — uptrend, RS leader vs SPY (+4.9%) and sector (+7.5%), **earnings safe** (no near event), healthcare (defensive). Not a semi, so no AVGO read-through. Still not executable (market closed) and still subject to the A-tier loss-bucket caveat below.
- **Stocks A-tier remains a statistically losing bucket** — `signal-stats` stocks this run: **tier=A n=25, PF 0.2, totalR −5.0, winrate ~6.7% (1 win / 7 losses triggered)** vs **tier=B PF ~1.4, totalR +21**. A-tier underperforming B is a persistent regression (TODO-stocks-atier-winrate). Treat A-tier labels as attention flags, not green lights — AVGO is the live example.
- **Macro backdrop is risk-off and worsening.** BTC ~$63k (briefly sub-$62k), **lowest since February**, −14% on the week; **13-day spot-BTC-ETF outflow streak (~$3.45–4.4B)**; ~$1.5B 24h liquidations (>208k traders; BTC ~$800M, ETH ~$386M); crypto volatility index **53.17 (highest since Apr 2)**. **$60k is the major floor** (local low ~$59.9k + 200-week MA); a break opens $55k. Cut crypto long aggression on any further BTC support loss.

---

## 2. Data Used

**Internal — fresh (<3 h):**
- `data/reports/scalp/2026-06-04_08-51_scalp_report.md` (gen 11:51 EEST, ~0.8 h). Regime: **high-volatility danger (danger)**, BTC/ETH downtrend, breadth 22.9% > EMA20.
- `data/reports/intraday/2026-06-04_09-13_intraday_report.md` (gen 12:13 EEST, ~0.43 h). Regime: **high-volatility danger**, macro risk 45/100; headline "Over $600M in Bitcoin longs liquidated as BTC dips toward $60K".
- `data/reports/stocks/intraday/2026-06-04_09-31_stocks_intraday_report.md` (~0.15 h; session=after-hours, regular session closed). Weekday — applies.
- `data/catalysts/2026-06-04/` — `catalyst_events.jsonl` (1424 rows today / 629 unique per report), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_09-14.md`.
- LLM packets: `data/processed/llm_analysis_packet.md`, `llm_stocks_packet.md`.
- CLI / DB: `active-signals` (crypto 12 / stocks 50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-06-04` → **None**.

**Internal — carry-forward / stale (swing/invest):**
- `data/reports/stocks/swing/2026-06-03_13-11_stocks_swing_report.md` — ~20.5 h → **STALE (>14 h, flagged)**.
- `data/reports/stocks/invest/2026-06-03_13-15_stocks_invest_report.md` — ~20.4 h → **STALE (>14 h, flagged)**.
- `data/reports/swing/2026-06-03_01-20_swing_report.md` (crypto) — ~32.3 h → **STALE (>14 h)**, excluded from fresh swing final-verdict; active ZEC/XLM swing *signals* used instead.

**External (this run — cited §13):** StockTitan + SEC EDGAR 8-K (AVGO Q2 FY26 print + ~−13% drop to ~$417, StockTitan WebFetch-verified); CoinDesk + BlockchainReporter (BTC ~$63k, lowest since Feb, 13-day ETF outflow streak, $1.5B liquidations, vol index 53.17 — CoinDesk WebFetch-verified).

**Unavailable / blind:** live US equity prices (regular session closed — after-hours/last-close prints only); TradingView / Chrome chart verification (tool not loaded); liquidation heatmaps, order-book depth/CVD, ETF-flow live feed, on-chain whale flows, token-unlock calendar (manual/unconnected); live social beyond RSS-bridged `t.me/lookonchain`.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-03_default_schedule/`.
- `scheduler.log` mtime 12:32 EEST → **~0.12 h** (fresh).
- Latest cycle summary `cycle_06_11-21_summary.md` mtime 12:32 EEST → **~0.13 h** (fresh).
- **Both < 3 h → no defer.** Review proceeds normally.
- Crypto scalp ~0.8 h / intraday ~0.43 h → **fresh**. Stocks intraday ~0.15 h → **fresh**.
- Crypto swing ~32 h, stocks swing/invest ~20.5 h → **STALE (>14 h)**; excluded from fresh final-verdict for those modes.

---

## 4. What Changed vs Previous Review (08:39 → 12:42)

- **Crypto regime degraded one notch:** 08:39 read "bearish trend (risk-off)"; the 08:51/09:13 reports read **"high-volatility danger (danger)"** — now volatility-driven (BTC ATR pct 98–100). Breadth above EMA20 fell **35.4% → 22.9%** (continued deterioration). More defensive than last cycle.
- **Crypto A/B disappeared:** last cycle had a structured **GPS/USDT short B-tier 65.7**; this run there are **no A-tier and no B-tier fresh crypto setups** — only C-tier watchlist (MEME/HEI/WLD/EPIC/OPN). The active-signals list still carries older B-tier carry-forwards (ETH short `waiting`, EPIC, OPN, ZRO, INJ, ZEC/XLM swing) on their own levels.
- **AVGO contradiction re-confirmed and now price-hardened:** the regenerated 09:31 UTC stocks report STILL issues A-tier AVGO long with the stale 473.25–478.07 entry + `earnings: UNKNOWN`. External evidence is now firmer — StockTitan WebFetch shows the stock at **~$417 (−12.99%)**, so the printed long entry is **~13% above market**. Thesis **not** changed — still AVOID.
- **Stocks A-tier loss bucket persists:** PF 0.2 / totalR −5.0 / winrate ~6.7% (was PF 0.286 / ~5.9%). No improvement.
- **Catalyst mapping still weak:** ~23.8% mapped (was 22%). Unchanged regression.
- **Untracked legacy alerts:** None this run (was None) — integrity stable.
- **Confirmed since last review:** AVGO sell-the-news now reflected in an explicit post-print price; semi gap-risk into open; BTC risk-off deepening (lowest since February, 13-day ETF outflow streak, vol index 53.17 highest since Apr 2).
- **Invalidated:** nothing materially invalidated; GPS short simply rolled off the fresh B-tier list (still a carry-forward only on bounce).

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative JSONL): **1424** (629 unique per report); mapped (non-empty symbol): **339**; unmapped: **1085** → **76.2% unmapped**.
- `narrative_baskets`: **3** — `perps_dex_narrative` (HYPE, `wait_pullback`, fresh <1 h), `binance_ecosystem_teaser` (BNB, `related_beta_rotation`, fresh <24 h), `momentum_breakout` (WLD, `wait_pullback`, fresh <1 h).
- **⚠ Catalyst mapping weak this run (23.8% mapped, 76.2% unmapped) — use catalyst layer as context, not final decision.**
- Top unmapped — symbol resolver failed to attach a ticker (issuer name present in headline):
  1. "Tilly's (TLYS) Q1 2026 Earnings Call Transcript" — ticker literally in the title, still unmapped.
  2. "C3.ai (AI) Q4 2026 Earnings Transcript" — ticker in title, unmapped.
  3. "ChargePoint (CHPT) Q1 2027 Earnings Transcript" — ticker in title, unmapped.
- Direct evidence the resolver misses obvious issuer/ticker names even when they are parenthesized in the headline (feeds TODO-catalyst-resolver).

---

## 6. Market Landscape

**Crypto (actionable now):** High-volatility danger / risk-off. BTC downtrend, ~$63k (briefly sub-$62k) — lowest since February, −14% on the week; ETH downtrend. ~$1.5B 24h liquidations (BTC ~$800M, ETH ~$386M, >208k traders); spot-BTC-ETF **13-day outflow streak (~$3.45–4.4B)**; crypto volatility index **53.17 (highest since Apr 2)**. **$60k is the major floor** (local low ~$59.9k + 200-week MA); break opens $55k. Narrative heat concentrated in **AI (rising, attention 100)** and a momentum altcoin cluster (MEME/HEI/WLD/EPIC/OPN) that are **RS-leaders longing a weak BTC tape** with no confirmed catalyst → counter-tape, watchlist only. `t.me/lookonchain` flow is bearish/noise: 7-Siblings ETH dip-buys, FG Nexus −$85M ETH treasury loss — single-source social, context only.

**Stocks (NOT executable — regular session closed until ~16:30 EEST):** Regime label bullish (VIX 16.46, breadth 100% > EMA20, semis strongest sector RS +17.8% / tech +14.3%), BUT the dominant near-term fact is **AVGO's ~−13% post-earnings drop** — a fresh negative read-through into the semi complex (AMD/SMH/XLK/QQQ) at the open. The report's own news feed confirms it: "Nasdaq futures slide as Broadcom results fail to cheer investors", "Broadcom's stock falls despite accelerating AI-chip growth". Weakest sectors: utilities, communications, staples.

---

## 7. Candidate Deep Dives (≤ 5)

### 7.1 AVGO — stocks A-tier long 89.7 → **AVOID / MANUAL REVIEW REQUIRED**
- **Setup as scored:** A-tier long, entry 473.25–478.07, invalidation <463.61, TP1 492.5. Thesis: uptrend + RS leader + bullish regime. Flagged `earnings: UNKNOWN` (counter-thesis: undated event risk).
- **Reality (external-verified):** AVGO reported **Q2 FY2026 on June 3** — record rev **$22.2B (+48% YoY)**, non-GAAP EPS **$2.44 (+54%, beat ~$2.32 est)**, AI-semi **$10.8B (+143% YoY)**, Q3 guide **~$29.4B (+84% YoY)**. Despite the beat, the stock **fell ~−12.99% to ≈$417** (StockTitan WebFetch) because the **full-year AI target was not raised** → sell-the-news + valuation reset.
- **LEGAL/HEADLINE RISK (§I):** none found. This is an earnings-reaction contradiction, not a legal one.
- **Price-reaction / chase (§J):** Catalyst (earnings) has **already fully reacted** — hard. The desk's entry zone is **pre-earnings and now ~13% ABOVE** post-print price (~$417 vs 473–478); entering the printed long is impossible/invalid and would be catching a falling knife. Entry NOW would be late and wrong-side. Actionable level: none until the **cash session prints and stabilizes** post-gap.
- **Verdict:** **AVOID / MANUAL REVIEW.** A-tier score is anchored on stale pre-event data; do not trade the printed long.

### 7.2 AMD — stocks A-tier long 90 (also B 79.1) → **MANUAL / post-open reassess (no pre-open chase)**
- **Setup:** A-tier long, entry 537.84–542.43, invalidation <528.66, TP1 556.2. RS vs SPY **+48.5%**, RS vs sector +30.7%, earnings **safe** (no near event), trend uptrend, regime bullish.
- **External / internal:** AMD is the strongest-RS large semi in the book. No legal/headline risk found. (Barclays PT $665 set June 1 per prior-review citation; not re-verified this run — treat as context.)
- **Price-reaction / chase (§J):** Fundamentally clean and tape-aligned, BUT **US regular session is closed** and AMD faces **AVGO sympathy gap-down risk at the open**. Cannot confirm whether price still sits in/below the 537–542 zone after the AVGO read-through. Entry NOW = not possible (closed).
- **Caveat:** stocks A-tier bucket is net-negative (PF 0.2) — score is an attention flag, not a green light.
- **Verdict:** **Best post-open watch.** Consider only after the AVGO gap is absorbed AND AMD reclaims/holds its planned zone on the cash session. No pre-positioning.

### 7.3 LLY — stocks A-tier long 84.31 → **CLEANEST idea, but post-open only (market closed)**
- **Setup:** A-tier long, entry 1078.43–1083.46, invalidation <1068.38, TP1 1098.5. Trend uptrend, **above prev-day high**, RS vs SPY +4.9%, RS vs sector ETF +7.5%, 1 news catalyst, **earnings: safe**.
- **Why it stands out:** healthcare (defensive, XLV) — **not** a semiconductor, so it carries **no AVGO read-through / sympathy gap risk**. Technical-setup score is the highest of the A/B list (18.48). News: "Forget Weight Loss Drugs: Here Is Another Reason to Buy Eli Lilly Stock" (Motley Fool, 2026-06-04) — single-source, bullish-leaning, not a hard catalyst.
- **LEGAL/HEADLINE RISK (§I):** none found this run.
- **Price-reaction / chase (§J):** above prev-day high but RR-to-TP1 is only 1.0 (sub-1.5) — a thin reward structure typical of these A-tier longs. Not overextended on the report fields. Entry NOW = not possible (regular session closed).
- **Verdict:** **Cleanest stock long if the tape cooperates at the open** — but still A-tier-bucket-caveated (PF 0.2) and RR-light. Post-open reclaim/hold of 1078–1083 only; no pre-position.

### 7.4 SMH — stocks B-tier long 77.87 (A 82 triggered) → **AVOID fresh long (direct AVGO read-through)**
- **Setup:** B-tier long, entry 634.50–637.89, invalidation <627.71, TP1 648.1. RS vs SPY +17.8%, ETF (no earnings), trend uptrend.
- **Reality:** SMH is the semiconductor ETF — **AVGO is a top holding**. A ~−13% AVGO drop is a direct drag, not a sympathy second-order effect. The desk also has an SMH **A-tier 82 already triggered** in the active-signals table, i.e. a live long exposed to the gap.
- **Price-reaction / chase (§J):** the AVGO read-through has **not yet been priced** into SMH (cash session closed). Buying the printed zone pre-open ignores a known negative open driver.
- **Verdict:** **No fresh long pre-open.** Reassess only after the open absorbs the AVGO gap and SMH holds its zone. Same applies to XLK B 73.7 and QQQ C 63.

### 7.5 Crypto landscape (no fresh A/B) → **NO CLEAN CANDIDATE — watchlist / no-trade**
- **State:** zero fresh A/B-tier crypto setups this run. C-tier leaders MEME (60.9–64.4), HEI (60.3), WLD (60.2) are **RS-leader longs counter-tape in a high-volatility-danger regime**, members of the `momentum_breakout` / `wait_pullback` baskets, on weak/below-average confirmation volume (WLD 0.39–0.54×, OPN 0.04–0.38×). No fresh verified catalyst for any of them.
- **Price-reaction / chase (§J):** already extended; entry NOW would be chasing counter-trend longs on a weak, high-ATR tape (fakeout risk elevated). Only deep, held pullbacks make them actionable.
- **Carry-forward shorts:** active ETH short (`waiting_for_entry`) and the rejected extended-breakdown shorts (CHZ/NEAR/RENDER/PORTAL, all >2 ATR from EMA20) are **do-not-chase the flush**.
- **Verdict:** **Watchlist / no-trade.** No structured crypto entry clears the bar this cycle; defend the BTC $60k floor thesis and avoid both counter-tape longs and exhausted-flush shorts.

---

## 8. Best Candidates Ranked

**No clean A-grade candidate.** Stocks are closed and the actionable semi list (AVGO/AMD/SMH/XLK) is exposed to a fresh negative AVGO read-through into the open; crypto is high-volatility-danger with no fresh, non-extended, catalyst-backed setup.

Least-bad order (all monitoring — nothing executable right now):
1. **LLY** (stocks, post-open only) — cleanest A-tier long: earnings safe, RS leader, defensive healthcare, **no AVGO read-through**. Reclaim/hold 1078–1083 on the cash session.
2. **AMD** (stocks, post-open only) — strongest-RS semi, earnings safe; reassess only after the AVGO gap is absorbed and it holds 537–542.
3. **Crypto** — no entry; defend BTC $60k floor view, watch the momentum cluster (MEME/HEI/WLD) for deep held pullbacks only, no chase.

---

## 9. Avoid / No Trade

- **AVGO** — A-tier long is stale (pre-earnings) and invalidated by the ~−13% drop to ≈$417; printed entry ~13% above market. AVOID / manual review.
- **SMH / XLK / QQQ** — semis/tech facing direct AVGO read-through (AVGO is a top SMH holding); no fresh long pre-open.
- **Crypto RS-leader longs (MEME / HEI / WLD / EPIC / OPN)** — counter-tape in a high-volatility-danger regime, momentum baskets, weak/low confirmation volume. Watchlist only, no chase.
- **Extended breakdown shorts (CHZ / NEAR / RENDER / PORTAL / TON / GPS)** — desk-rejected/below-threshold, >2 ATR from EMA20; do not chase the flush.
- **SMCI** — not on the A/B list this run (no_trade, 53.75) but carries a known live legal overhang (SEC probe + Mar-2026 export-control indictment + class action per prior-review citations); AVOID if it surfaces.

---

## 10. Main Risks

- **Semi gap-down at the US open** from AVGO's ~−13% drop — dominant near-term equity risk; would hit AMD/SMH/XLK/QQQ longs (SMH directly, AVGO being a top holding).
- **Stocks A-tier is net-negative** (PF 0.2, totalR −5) — A-tier labels are attention flags, not green lights (AVGO is the live example).
- **Crypto downside continuation** — BTC ~$63k with a 13-day ETF outflow streak; **$60k is the major floor** (local low $59.9k + 200-week MA), a break opens $55k. Further support loss invalidates any RS-leader long.
- **Crypto chase risk** — RS leaders (MEME/HEI/WLD) are counter-tape on weak volume; high-volatility-danger + ATR pct 98 favors fakeouts.
- **Data-quality risk** — the desk re-issued a stale AVGO A-tier long on pre-earnings price with `earnings: UNKNOWN` (4th consecutive review); trusting raw scores without a post-print overlay would be a mistake.
- **Source ingest** — if the §M ingest CLI fails, citations remain in the JSON artifact (no decision depends on the ingest).

---

## 11. Action Plan — next 4 hours

1. **Crypto (actionable now):** No fresh longs and no fresh shorts that clear the bar. Defend the BTC **$60k floor** thesis — cut all crypto long aggression on a break of local support (sub-$60k continuation toward $55k). Watch the momentum cluster (MEME/HEI/WLD) only for a deep, held pullback; no chase at spot, no counter-tape adds.
2. **Stocks (NOT executable until ~16:30 EEST):** Do NOT pre-position semis long. At the open, watch whether AMD/SMH absorb the AVGO gap; **LLY** is the cleanest non-semi long to reassess on a reclaim/hold of 1078–1083. Treat **AVGO** as manual-review until the cash session prints and stabilizes.
3. **Monitor:** AVGO cash-session direction (gap hold vs fill) and semi sympathy; BTC structure around $60k + ETF/on-chain flow; LLY/AMD zone behavior at the open.
4. **System:** see §14 TODOs (stale post-earnings A-tier signal — now with a hard price gap, `earnings: UNKNOWN` regression, catalyst symbol resolver, A-tier winrate) for the next manual maintenance session.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** No-trade. No A/B clears threshold; best watch MEME 64.4 (counter-tape long, no chase). High-volatility-danger tape — preserve capital.
- **Crypto intraday:** No-trade. No A/B; MEME/HEI/WLD are counter-tape RS-leader longs, pullback-only. Defend BTC $60k.
- **Crypto swing:** No fresh call — swing report stale (32 h). Existing ZEC/XLM swing signals stand on their own levels; no new entry.
- **Stocks intraday:** Market closed + AVGO gap risk → no fresh longs. AVGO AVOID/manual; **LLY best post-open reassess (non-semi, clean)**; AMD post-open after gap absorbed; SMH/XLK no fresh long. (Weekday — section applies but not executable now.)
- **Stocks swing / invest:** STALE data (~20.5 h) → context only, no fresh call this cycle.

---

## 13. Sources

**AVGO (Broadcom Q2 FY2026 earnings + post-earnings reaction):**
- [Broadcom Inc. Announces Q2 FY2026 Financial Results — StockTitan, 2026-06-03](https://www.stocktitan.net/news/AVGO/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial-if4yrbje8hq6.html) *(primary_source; WebFetch-verified: rev $22.2B +48%, non-GAAP EPS $2.44 +54%, AI $10.8B +143%, Q3 guide ~$29.4B; stock down ~−12.99% to ≈$417 after the print)*
- [Broadcom Inc. — Form 8-K — FY2026 (Q2 results exhibit) — SEC EDGAR, 2026-06-03](https://www.sec.gov/Archives/edgar/data/0001730168/000173016826000051/avgo-05032026x8kxex99.htm) *(primary_source; official earnings release exhibit)*

**BTC macro:**
- [Bitcoin selloff continues as prices slide below $63,000 for the first time since February — CoinDesk, 2026-06-04](https://www.coindesk.com/markets/2026/06/04/bitcoin-selloff-continues-as-prices-slide-below-usd63-000-for-the-first-time-since-february) *(single_source; WebFetch-verified: ~$63k, lowest since Feb, −14% week, 13-day ETF outflow streak, vol index 53.17 highest since Apr 2, support low-$60k / $59.9k / 200-week MA)*
- [Bitcoin Price Today: BTC At $63,649 as selloff hits 13% on the week, $1.5B liquidated — BlockchainReporter, 2026-06-04](https://blockchainreporter.net/bitcoin-price-today-btc-at-63649-as-selloff-hits-13-on-the-week-1-5b-liquidated/) *(single_source; ~$1.5B liquidations, >208k traders, BTC ~$800M / ETH ~$386M, ETF outflow ~$3.45B)*

*Source-discipline: every external claim above carries source + title + date + URL. No uncited stats or legal claims. No fabricated chart observations (chart tools not loaded). No `test_source`/fixture URLs.*

---

## 14. Fix Requests / TODO

### TODO-stocks-stale-postearnings
- **issue:** Stocks intraday report re-issues an A-tier LONG (AVGO 89.7) on a **pre-earnings** entry zone (473.25–478.07) after the symbol already reported and sold off to ≈$417 (−12.99%); the score never overlays the just-printed earnings reaction. The printed entry is now ~13% above market — a hard, externally-verified gap.
- **evidence:** `data/reports/stocks/intraday/2026-06-04_09-31_stocks_intraday_report.md` Idea #1 (entry 473.25–478.07, `earnings:unknown`); StockTitan WebFetch ≈$417 / −12.99%; report's own news feed ("Broadcom's stock falls despite accelerating AI-chip growth", "Nasdaq futures slide as Broadcom results fail to cheer investors"). Flagged in the 00:39 / 04:43 / 08:39 reviews and NOT corrected.
- **suggested manual fix:** when a symbol has a `news_items`/catalyst `earnings_event` within the last ~18 h, suppress or demote A-tier directional longs anchored on pre-event price (post-earnings overlay / freshness gate on the entry zone vs last trade).
- **priority:** high
- **first observed:** 2026-06-04 00:39 EEST (recurring; re-confirmed 12:42 EEST with a hard price gap)

### TODO-earnings-unknown-regression
- **issue:** AVGO tagged `earnings: UNKNOWN` ("calendar lookup missing") the day after it reported Q2 FY2026 — earnings-calendar lookup is failing for a large, well-covered name. Earnings lookup also failed for SPY/QQQ/IWM/DIA/SMH/XLK/XLF/XLE/XLY/XLV.
- **evidence:** stocks intraday report §0 "Earnings lookup failed for: SPY,QQQ,IWM,DIA,SMH,XLK,XLF,XLE,XLY,XLV" and AVGO Idea #1 `earnings:unknown`, while the SEC 8-K and StockTitan confirm the Q2 print.
- **suggested manual fix:** audit the earnings-calendar provider/fallback; cross-check against `news_items` `earnings_event` catalysts before stamping UNKNOWN.
- **priority:** high
- **first observed:** 2026-06-04 00:39 EEST (recurring)

### TODO-catalyst-resolver
- **issue:** Catalyst symbol resolver maps only ~23.8% of events (339/1424); high-importance, obviously-tickerable headlines are left unmapped — including ones with the ticker parenthesized in the title.
- **evidence:** `data/catalysts/2026-06-04/catalyst_events.jsonl` — 1085/1424 empty-symbol; top unmapped incl. "Tilly's (TLYS) ...", "C3.ai (AI) ...", "ChargePoint (CHPT) ..." — tickers literally in the headline.
- **suggested manual fix:** add a company-name → ticker dictionary pass plus a regex for parenthesized `(TICKER)` tokens in earnings/transcript headlines.
- **priority:** medium
- **first observed:** 2026-06-03 (recurring; ~22–24% mapped across multiple runs)

### TODO-stocks-atier-winrate
- **issue:** Stocks A-tier bucket is reproducibly net-negative (PF 0.2, totalR −5.0, winrate ~6.7% — 1 win / 7 losses triggered of n=25) while B-tier is profitable (PF ~1.4, totalR +21) — A-tier scoring/gating is inverted relative to outcome quality.
- **evidence:** `signal-stats --asset-class stocks` By-tier: A n=25 PF 0.2 totalR −5.0; B n=269 PF ~1.4 totalR +21.
- **suggested manual fix:** review what pushes a stock to A-tier (RR-below-1.5 ideas still scoring 84–90 via regime/RS); consider an RR gate and an earnings-freshness penalty before A-tier promotion.
- **priority:** medium
- **first observed:** 2026-06-04 00:39 EEST (recurring)
