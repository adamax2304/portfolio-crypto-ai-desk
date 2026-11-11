# Opus Enriched Review — Auto Cycle 08:39 EEST

- **Generated:** 2026-06-04 08:39 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`)
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-04_0443.md` (≈4 h ago — §4)
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim cited in §13 with source + date + URL. AVGO after-hours drop and BTC sub-$62k print independently WebFetch-verified (StockTitan, CoinDesk).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from local OHLCV/ATR/EMA report fields + cited external prints.
- **Clock:** 08:39 EEST Thursday. **US stock market is CLOSED** (regular session reopens ~16:30 EEST). Stock signals below are NOT executable this cycle; crypto trades 24/7 and is the only actionable class right now.
- **Advisory only. No auto-trade.**

---

## 1. Executive Summary

- **No clean actionable A-grade candidate this cycle.** Stocks are closed and the actionable semi list is still poisoned by the AVGO post-earnings read-through; crypto regime has **re-hardened from "range/chop" back to "bearish trend (risk-off)"** with BTC/ETH downtrend, breadth 35.4% > EMA20 (down from 43.75% last cycle) and BTC ATR percentile **100 (elevated)**. Posture: **watchlist / no-trade for fresh longs**; the only structured crypto idea is a disciplined short.
- **Persisting contradiction: the regenerated stocks report (03:17 UTC) STILL re-issues AVGO as A-tier LONG 89.7 with a stale pre-earnings entry zone (473.25–478.07) and `earnings: UNKNOWN`** — even though AVGO reported Q2 FY2026 the prior evening and **sold off −6.5% to −14.4% after-hours**. AVGO printed record rev **$22.2B (+48% YoY**, marginal miss vs $22.27B est), AI-semi **$10.8B (+143% YoY)**, strong Q3 guide **~$29.4B / AI $16B (+200% YoY)** — yet fell on a textbook sell-the-news because CEO Hock Tan **did not raise the full-year AI target**. The A-tier long is anchored ~10–12% above where the stock actually trades post-print. **Verdict for AVGO: AVOID / MANUAL REVIEW REQUIRED.** (Same finding as 04:43 review; the desk has not self-corrected — confirms TODO-stocks-stale-postearnings.)
- **Negative semi read-through into the 06-04 cash open persists.** AVGO's drop is a fresh bearish catalyst for the semi complex. The desk's other semi longs — **AMD A 90.1, SMH B 77.87 (also SMH A 82 triggered), XLK B 73.7** — are technically bullish *against* that catalyst and carry **gap-down / sympathy risk at the open.** Do not chase fresh semi longs pre-open. AMD remains the strongest-RS name (RS vs SPY +48.5%, Barclays PT $665 set June 1) and is the best post-open reassessment — but only after the AVGO gap is absorbed.
- **Stocks A-tier remains a statistically losing bucket** — `signal-stats` stocks this run: **tier=A n=25, PF 0.286, totalR −5.0, winrate 5.9%** vs **tier=B PF ~1.7, totalR +33**. A-tier underperforming B is a persistent regression (TODO-stocks-atier-winrate). Treat A-tier labels as attention flags, not green lights — AVGO is the live example.
- **Crypto:** no A-tier; only one new B-tier this cycle — **SHORT GPS/USDT 65.7 (scalp)** — below the active-trade threshold, on weak volume (0.67×) and already −20% on 24h. Tape-aligned (bearish) but late-short/exhaustion risk; failed-bounce-only into 0.0069–0.0071, no chase at spot. All other crypto names are RS-leader longs (WLD/EPIC/OPN/C) that are **counter-tape in a bearish regime** and flagged watchlist/no-chase. **Catalyst mapping weak this run (201/910 mapped = 22%, 78% unmapped) — use catalyst layer as context, not final decision.**
- **Macro backdrop is risk-off.** BTC sub-$62k intraday (~$64.2k at CoinDesk publish), **$1.5B in 24h crypto liquidations** (>$800M BTC, $386M ETH), spot-BTC-ETF **11–12 day outflow streak (~$3.45B)**, Strategy's first BTC sale in ~4 years, plus US-Iran tension. $62–63k is now overhead resistance. Cut crypto long aggression on any further BTC support loss.

---

## 2. Data Used

**Internal — fresh (<3 h):**
- `data/reports/scalp/2026-06-04_02-51_scalp_report.md` (gen 05:51 EEST, ~2.8 h). Regime: **bearish trend (risk-off)**, BTC/ETH downtrend, breadth 35.4%.
- `data/reports/intraday/2026-06-04_03-09_intraday_report.md` (gen 06:09 EEST, ~2.5 h). Regime: **bearish trend (risk-off)**, macro risk 65/100.
- `data/reports/stocks/intraday/2026-06-04_03-17_stocks_intraday_report.md` (~2.4 h; session=after-hours, regular session closed). Weekday — applies.
- `data/catalysts/2026-06-04/` — `catalyst_events.jsonl` (910 rows today), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_03-10.md` (06:10 EEST).
- LLM packets: `data/processed/llm_analysis_packet.md` (~2.5 h), `llm_stocks_packet.md` (~2.4 h).
- CLI / DB: `active-signals` (crypto 18 / stocks 50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-06-04` → **None**.
- `db/crypto_ai_desk.sqlite` `news_items` — direct read for AVGO/AMD/SMCI/SMH/WLD/GPS/NVDA/TSLA + `t.me/` source rows (last 4 h).

**Internal — carry-forward / stale (swing/invest):**
- `data/reports/stocks/swing/2026-06-03_13-11_stocks_swing_report.md` — ~16.5 h → **STALE (>14 h, flagged)**.
- `data/reports/stocks/invest/2026-06-03_13-15_stocks_invest_report.md` — ~16.4 h → **STALE (>14 h, flagged)**.
- `data/reports/swing/2026-06-03_01-20_swing_report.md` (crypto) — ~28.3 h → **STALE (>14 h)**, excluded from fresh swing final-verdict; active ZEC/XLM swing *signals* used instead.

**External (this run — cited §13):** CNBC + StockTitan + MarketWatch (AVGO Q2 FY26 print + after-hours drop, StockTitan WebFetch-verified); GuruFocus/Barclays + CNBC (AMD PT $665 / +130% YTD); Motley Fool + FinancialContent (SMCI SEC probe / class action / Mar-2026 indictment / Jan-2026 Nasdaq compliance); CoinDesk + Bitcoin Magazine (BTC sub-$62k + $1.5B liquidations, CoinDesk WebFetch-verified).

**Unavailable / blind:** live US equity prices (market closed — last-close + after-hours prints only); TradingView / Chrome chart verification (tool not loaded); liquidation heatmaps, order-book depth/CVD, ETF-flow live feed, on-chain whale flows, token-unlock calendar (manual/unconnected); live social beyond RSS-bridged `t.me/lookonchain`.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-03_default_schedule/`.
- `scheduler.log` mtime 08:18 EEST → **~0.35 h** (fresh).
- Latest cycle summary `cycle_04_05-30_summary.md` mtime 06:18 EEST → **~2.35 h** (fresh).
- **Both < 3 h → no defer.** Review proceeds normally.
- Crypto scalp/intraday reports ~2.5–2.8 h → **fresh**. Stocks intraday ~2.4 h → **fresh**.
- Crypto swing ~28 h, stocks swing/invest ~16.5 h → **STALE (>14 h)**; excluded from fresh final-verdict for those modes.

---

## 4. What Changed vs Previous Review (04:43 → 08:39)

- **Crypto regime re-hardened:** 04:43 reports read "range/chop (neutral)"; the 02:51/03:09 reports read **"bearish trend (risk-off)"** again. Breadth above EMA20 fell 43.75% → **35.4%**; BTC ATR percentile 96 → **100**. Net: more defensive than last cycle.
- **New crypto B-tier:** **GPS/USDT short 65.7** is now the top scalp B-tier idea (was not present at 04:43). OPN/SUSHI still float as B-tier `waiting_for_entry`; **ENA fell from B-tier to C-tier watchlist** (scalp #10, 55.7) — the Coinbase USDe launch catalyst still exists (~June 9–10) but the desk no longer ranks it actively.
- **AVGO contradiction unchanged / re-confirmed:** the regenerated 03:17 UTC stocks report STILL issues A-tier AVGO long with stale entry + `earnings: UNKNOWN`. External evidence now firmer: StockTitan/CNBC confirm the sell-the-news drop (−6.5% to −14.4% AH). Thesis **not** changed — still AVOID.
- **Stocks A-tier loss bucket persists:** PF 0.286 / winrate ~5.9% (was 0.286 / 5.3%). No improvement.
- **Catalyst mapping still weak:** ~22% mapped (was 21%). Unchanged regression.
- **Untracked legacy alerts:** None this run (was None) — integrity stable.
- **Confirmed since last review:** AVGO sell-the-news; semi gap-risk into open; BTC risk-off deepening (ETF outflow streak, Strategy BTC sale now cited).
- **Invalidated:** nothing materially invalidated; ENA simply de-ranked, not invalidated.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative JSONL): **910**; mapped (non-null symbol): **201**; unmapped (null symbol): **709** → **77.9% unmapped**.
- `narrative_baskets`: **3** — `binance_ecosystem_teaser` (BNB/ASTER, `related_beta_rotation`), `perps_dex_narrative` (HYPE/DYDX/GMX/ASTER, `wait_pullback`), `momentum_breakout` (OPN/EPIC/WLD + STO/C, **`avoid_chase`**, fresh <1 h).
- **⚠ Catalyst mapping weak this run (22% mapped) — use catalyst layer as context, not final decision.**
- Top unmapped (by importance) — symbol resolver failed to attach a ticker:
  1. `imp 0.68 [legal_risk]` "69-year-old furniture store chain files for Chapter 11 bankruptcy" (Yahoo Finance) — generic macro, correctly unmapped.
  2. `imp 0.68 [exploit_hack]` "Trezor Reveals Hardware Wallet Vulnerability, But Funds 'Safe'" (Decrypt) — sector headline, no single ticker.
  3. `imp 0.65 [earnings_event]` **"Broadcom reports record Q2 revenue of $22B, driven by AI growth"** (CryptoBriefing) — **this SHOULD map to AVGO and does not.** Direct evidence the resolver misses obvious issuer names in earnings headlines (feeds TODO-catalyst-resolver).

---

## 6. Market Landscape

**Crypto (actionable now):** Bearish trend / risk-off. BTC downtrend, sub-$62k intraday (~$64.2k at CoinDesk publish), ETH downtrend. $1.5B 24h liquidations (>$800M BTC, $386M ETH); spot-BTC-ETF outflow streak 11–12 days (~$3.45B); Strategy's first BTC sale in ~4 years; US-Iran tension adds risk-off. $62–63k flips to resistance. Narrative heat concentrated in Memes (DOGE) and a pure-momentum altcoin cluster (OPN/EPIC/WLD/C/STO) with **no confirmed news catalyst** → `avoid_chase`. `t.me/lookonchain` flow (last 4 h) is bearish/noise: Mt. Gox BTC exchange deposits, FG Nexus −$85M on ETH treasury, 7-Siblings ETH dip-buy — single-source social, context only.

**Stocks (NOT executable — market closed until ~16:30 EEST):** Regime label bullish (VIX 16.06, breadth 100% > EMA20, semis strongest sector RS +17.8% / tech +14.3%), BUT the dominant near-term fact is **AVGO's after-hours sell-off**, a fresh negative read-through into the semi complex (AMD/SMH/XLK/QQQ) at the open. Weakest sectors: utilities, communications, staples.

---

## 7. Candidate Deep Dives (≤ 5)

### 7.1 AVGO — stocks A-tier long 89.7 → **AVOID / MANUAL REVIEW REQUIRED**
- **Setup as scored:** A-tier long, entry 473.25–478.07, invalidation <463.61, TP1 492.5. Thesis: uptrend + RS leader + bullish regime. Flagged `earnings: UNKNOWN` (counter-thesis: undated event risk).
- **Reality (external-verified):** AVGO reported **Q2 FY2026 on June 3** — record rev **$22.2B (+48% YoY)**, non-GAAP EPS **$2.44** (beat $2.40 est), AI-semi **$10.8B (+143% YoY)**, Q3 guide **~$29.4B** / AI **$16B (+200% YoY)**. Despite the beat, the stock **fell −6.5% to −14.4% after-hours** (StockTitan/Benzinga/CNBC) because the **full-year AI target was not raised** → sell-the-news + valuation reset.
- **LEGAL/HEADLINE RISK:** none found. This is an earnings-reaction contradiction, not a legal one.
- **Price-reaction / chase (§J):** Catalyst (earnings) has **already fully reacted** — hard. The desk's entry zone is **pre-earnings and now ~10–12% above** post-print price; entering the printed long zone is impossible/invalid and would be chasing a knife. Entry NOW would be late and wrong-side. Actionable level: none until the **cash session prints and stabilizes**.
- **Verdict:** **AVOID / MANUAL REVIEW.** A-tier score is anchored on stale pre-event data; do not trade the printed long.

### 7.2 AMD — stocks A-tier long 90.1 → **MANUAL / post-open reassess (no pre-open chase)**
- **Setup:** A-tier long, entry 537.84–542.43, invalidation <528.66, TP1 556.2. RS vs SPY +48.5%, RS vs sector +30.7%, earnings **safe** (no near event), 1 news catalyst.
- **External:** AMD is the strongest-RS large semi — **+~130% YTD**, Barclays raised PT to **$665 (from $500) on June 1** (Overweight), consensus "Buy". Data-center momentum strong (Q1 data-center +57% YoY). No legal/headline risk found.
- **Price-reaction / chase (§J):** Fundamentally clean and tape-aligned (bullish stock regime), BUT **US market is closed** and AMD faces **AVGO sympathy gap-down risk at the open**. Cannot confirm whether price still sits in/below the 537–542 zone after the AVGO read-through. Entry NOW = not possible (closed).
- **Caveat:** stocks A-tier bucket is net-negative (PF 0.286) — score is an attention flag, not a green light.
- **Verdict:** **Best post-open watch.** Only consider after the AVGO gap is absorbed AND AMD reclaims/holds its planned zone on the cash session. No pre-positioning.

### 7.3 SMCI — stocks no_trade / rejected 53.75 → **AVOID (legal overhang)**
- **Why on the list:** §I legal-flag symbol; jumped **+68% in May** (Motley Fool), 8-K (FY2026) in the feed — suspicious-rally + known accounting history warrant a check.
- **LEGAL/HEADLINE RISK (external-verified):** SMCI carries a **still-live overhang** — an **ongoing SEC investigation**, a **forensic-accounting internal investigation** by independent board directors, a **March 19 2026 export-control indictment** (two employees + a contractor; SMCI itself not named/charged), and an **investor class action** alleging concealment of restricted AI-server sales to China. Background: Ernst & Young resigned as auditor Oct 2024; SMCI **regained Nasdaq compliance Jan 27 2026** after filing overdue reports. No June-2026 clearing event found this run.
- **Price-reaction / chase (§J):** The +68% May move is the reaction; no fresh verified clearing catalyst. Chasing into an unresolved SEC/forensic overhang is exactly the headline-risk the desk's `no_trade` correctly flags.
- **Verdict:** **AVOID.** Desk's rejection is correct. Not a candidate.

### 7.4 GPS/USDT — crypto B-tier short 65.7 (scalp) → **WATCH-ACTIONABLE short, discipline-gated (below threshold)**
- **Setup:** short, entry (failed bounce/retest) **0.0069–0.0071**, invalidation 1h close >0.0074, TP1 0.0063 / TP2 0.0057, RR 1.84R, current 0.0068, ATR 0.0005.
- **Evidence:** bearish regime + breakdown structure; 24h −20.4%, RS vs BTC −15.5%, **volume 0.67× (below average)**, downtrend. No fresh verified catalyst (news_items: 0 GPS rows in 24 h).
- **Price-reaction / chase (§J):** Price already broke down ~20%; the setup is a **retest short above spot (0.0069–0.0071)**, i.e. it explicitly avoids chasing the flush — good. Risk: late-short into exhausted sellers with weak volume; a BTC reclaim would squeeze it. Not overextended on the short side relative to the entry zone. Actionable only on a bounce INTO the zone, no chase at 0.0068.
- **Verdict:** **The only structured crypto idea this cycle**, but B-tier below active threshold and low-volume — small size, failed-bounce-only, hard invalidation >0.0074.

### 7.5 WLD/USDT — crypto C-tier watchlist (scalp 64.4 / intraday 58.3) → **WATCH, no chase**
- **Setup:** RS leader (+36% vs BTC, +31–33% 24h), uptrend, momentum 95, but **counter-tape long in a bearish regime**; member of the `momentum_breakout` basket with playbook **`avoid_chase`**. Pullback-only zone ~0.499–0.518.
- **Catalyst:** no fresh verified catalyst (AMBCrypto "overextended Worldcoin can still rally" is 2026-06-03, single-source, ~25 h old). Multi-exchange confirmation 82.9 (binance+mexc).
- **Price-reaction / chase (§J):** already extended; entry NOW would be chasing a counter-trend long on a weak tape. Only a deep, held pullback makes it actionable.
- **Verdict:** **Watchlist / no chase.** Representative of the whole RS-leader-long cluster (EPIC/OPN/C/STO) — reduce-size, pullback-only, not active.

---

## 8. Best Candidates Ranked

**No clean A-grade candidate.** Stocks are closed and the actionable semi list (AVGO/AMD/SMH/XLK) is exposed to a fresh negative AVGO read-through into the open; crypto is bearish with no fresh, non-extended, catalyst-backed long.

Least-bad order (mostly monitoring, one disciplined entry):
1. **GPS/USDT short** (crypto, actionable now) — only structured idea; failed-bounce-only 0.0069–0.0071, small size, invalidation >0.0074, below active threshold so treat as scalp-discretionary not a headline signal.
2. **AMD** (stocks, post-open only) — strongest-RS semi, earnings safe, PT $665; reassess only after the AVGO gap is absorbed and it holds its zone.
3. **WLD/OPN/EPIC cluster** (crypto) — RS leaders, pullback-only, no chase (`avoid_chase` basket).

---

## 9. Avoid / No Trade

- **AVGO** — A-tier long is stale (pre-earnings) and invalidated by the −6.5/−14.4% after-hours drop; printed entry ~10–12% above post-print price. AVOID / manual review.
- **SMCI** — live SEC investigation + forensic-accounting probe + Mar-2026 export-control indictment + class action; no June clearing event. AVOID.
- **SMH / XLK / QQQ** — semis/tech facing direct AVGO gap-down read-through; no fresh long pre-open.
- **Crypto RS-leader longs (WLD / EPIC / OPN / C / STO)** — counter-tape in a bearish regime, `avoid_chase` momentum basket, weak/low confirmation volume. Watchlist only.
- **Extended breakdown shorts (CHIP / CHZ / GIGGLE / TON / HOME)** — desk-rejected, >2 ATR from EMA20; do not chase the flush.

---

## 10. Main Risks

- **Semi gap-down at the 06-04 US open** from AVGO's after-hours drop — dominant near-term equity risk; would hit AMD/SMH/XLK/QQQ longs.
- **Stocks A-tier is net-negative** (PF 0.286, totalR −5) — A-tier labels are attention flags, not green lights (AVGO is the live example).
- **Crypto downside continuation** — BTC sub-$62k with an 11–12 day ETF outflow streak + Strategy BTC sale; further support loss invalidates any RS-leader long and accelerates GPS-style shorts (manage, don't over-add).
- **Crypto chase risk** — RS leaders (WLD/OPN/EPIC) are counter-tape on weak volume; bearish trend + ATR pct 100 favors fakeouts.
- **Data-quality risk** — the desk re-issued a stale AVGO A-tier long on pre-earnings price with `earnings: UNKNOWN`; trusting raw scores without the post-print overlay would be a mistake.
- **Source ingest** — if the §M ingest CLI fails, citations remain in the JSON artifacts (no decision depends on the ingest).

---

## 11. Action Plan — next 4 hours

1. **Crypto (actionable now):** No fresh longs. **GPS/USDT** — short only on a failed bounce into 0.0069–0.0071, small size, invalidation 1h close >0.0074, TP1 0.0063; skip if it just flushes vertically (no chase). Cut all crypto long aggression if BTC loses local support (sub-$62k continuation, Mt. Gox deposits, ETF outflows).
2. **Stocks (NOT executable until ~16:30 EEST):** Do NOT pre-position semis long. At the open, watch whether AMD/SMH absorb the AVGO gap; only then consider **AMD** (strongest RS) on a reclaim/hold of its planned zone. Treat **AVGO** as manual-review until the cash session prints; **SMCI** AVOID.
3. **Monitor:** AVGO cash-session direction (gap hold vs fill) and semi sympathy; BTC structure + on-chain/ETF flow; the `avoid_chase` momentum cluster for any deep, held pullback.
4. **System:** see §14 TODOs (stale post-earnings A-tier signal, `earnings: UNKNOWN` regression, catalyst symbol resolver, A-tier winrate) for the next manual maintenance session.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** Watchlist-plus. One disciplined idea: SHORT GPS/USDT on a bounce into 0.0069–0.0071 (below active threshold, small size). No longs — bearish tape.
- **Crypto intraday:** No-trade. No A/B clears threshold; AVAX best watch (63.9) but no catalyst, downtrend. Pullback-only.
- **Crypto swing:** No fresh call — swing report stale (28 h). Existing ZEC/XLM swing signals stand on their own levels; no new entry.
- **Stocks intraday:** Market closed + AVGO gap risk → no fresh longs. AVGO AVOID/manual; AMD best post-open reassess; SMCI AVOID. (Weekday — section applies but not executable now.)
- **Stocks swing / invest:** STALE data (~16.5 h) → context only, no fresh call this cycle.

---

## 13. Sources

**AVGO (Broadcom Q2 FY2026 earnings + after-hours reaction):**
- [Broadcom Inc. Announces Q2 FY2026 Financial Results — StockTitan, 2026-06-03](https://www.stocktitan.net/news/AVGO/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial-if4yrbje8hq6.html) *(primary_source; WebFetch-verified: rev $22.2B +48%, EPS $2.44, AI $10.8B +143%, Q3 ~$29.4B, stock down −6.5% to −14.4% AH)*
- [Broadcom (AVGO) earnings report Q2 2026 — CNBC, 2026-06-03](https://www.cnbc.com/2026/06/03/broadcom-avgo-earnings-report-q2-2026.html) *(single_source; EPS $2.44 vs $2.40 est, rev $22.19B vs $22.27B est, full-year AI target not raised)*
- [Broadcom's stock falls despite accelerating AI-chip growth — MarketWatch, 2026-06-04](https://www.marketwatch.com/) *(single_source; internal news_items row, 2026-06-04 00:13 UTC)*

**AMD:**
- [AMD Maintained by Barclays — PT raised to $665 — GuruFocus, 2026-06-01](https://www.gurufocus.com/news/8894301/amd-maintained-by-barclays-price-target-raised-to-66500) *(single_source; Overweight, PT $665 from $500)*
- [AMD's Su explains forecast change as stock roars 19% on earnings — CNBC, 2026-05-06](https://www.cnbc.com/2026/05/06/amd-lisa-su-stock-forecast-earnings.html) *(single_source; data-center momentum)*

**SMCI (legal/headline overhang):**
- [Super Micro Has Now Faced SEC Probes, Accounting Scandals, and Smuggling Charges — Motley Fool, 2026-03-20](https://www.fool.com/investing/2026/03/20/super-micro-has-now-faced-sec-probes-accounting-sc/) *(single_source; SEC probe, Mar-2026 indictment, class action)*
- [Super Micro (SMCI) Regains Nasdaq Compliance After Accounting Saga — FinancialContent, 2026-01-27](https://markets.financialcontent.com/stocks/article/marketminute-2026-1-27-super-micro-computer-smci-regains-nasdaq-compliance-after-high-stakes-accounting-saga-igniting-fresh-market-volatility) *(single_source; Jan-2026 compliance, E&Y resignation history)*

**BTC macro:**
- [Bitcoin drops below $62,000 as $1.5B in crypto longs get wiped out — CoinDesk, 2026-06-04](https://www.coindesk.com/markets/2026/06/04/bitcoin-drops-below-usd62-000-as-usd1-5-billion-in-crypto-longs-get-wiped-out) *(single_source; WebFetch-verified: ~$64.2k at publish, $1.5B liq, ETF outflows ~$1B/week)*
- [Bitcoin Price Plunges Below $62,000, Erasing Months of Recovery — Bitcoin Magazine, 2026-06-04](https://bitcoinmagazine.com/markets/bitcoin-price-plunges-below-62000-erasing-months-of-recovery-as-sell-off-accelerates) *(single_source; Strategy BTC sale, ETF outflow streak)*

*Source-discipline: every external claim above carries source + title + date + URL. No uncited stats or legal claims. No fabricated chart observations (chart tools not loaded). No `test_source`/fixture URLs.*

---

## 14. Fix Requests / TODO

### TODO-stocks-stale-postearnings
- **issue:** Stocks intraday report re-issues an A-tier LONG (AVGO 89.7) on a **pre-earnings** entry zone after the symbol already reported and sold off −6.5/−14.4% AH; the score never overlays the just-printed earnings reaction.
- **evidence:** `data/reports/stocks/intraday/2026-06-04_03-17_stocks_intraday_report.md` Idea #2 (entry 473.25–478.07, `earnings:unknown`); StockTitan/CNBC confirm the AH drop; `news_items` AVGO rows 2026-06-03 20:30 → 2026-06-04 00:13 UTC. Same issue flagged in the 04:43 review and NOT corrected.
- **suggested manual fix:** when a symbol has a `news_items`/catalyst `earnings_event` within the last ~18 h, suppress or demote A-tier directional longs anchored on pre-event price (post-earnings overlay / freshness gate on the entry zone).
- **priority:** high
- **first observed:** 2026-06-04 00:39 EEST (recurring; re-confirmed 08:39 EEST)

### TODO-earnings-unknown-regression
- **issue:** AVGO tagged `earnings: UNKNOWN` ("calendar lookup missing") on the very day it reported Q2 FY2026 — earnings-calendar lookup is failing for a large, well-covered name.
- **evidence:** stocks intraday report §3 "Earnings lookup failed for: SPY,QQQ,IWM,DIA,SMH,XLK,XLF,XLE,XLY,XLV" and AVGO Idea #2 `earnings:unknown`, while `catalyst_events.jsonl` carries "Broadcom reports record Q2 revenue of $22B".
- **suggested manual fix:** audit the earnings-calendar provider/fallback; cross-check against `news_items` `earnings_event` catalysts before stamping UNKNOWN.
- **priority:** high
- **first observed:** 2026-06-04 00:39 EEST (recurring)

### TODO-catalyst-resolver
- **issue:** Catalyst symbol resolver maps only ~22% of events (201/910); high-importance, obviously-tickerable headlines are left null (e.g. "Broadcom reports record Q2 revenue of $22B" not mapped to AVGO).
- **evidence:** `data/catalysts/2026-06-04/catalyst_events.jsonl` — 709/910 null-symbol; top unmapped incl. the AVGO earnings headline (imp 0.65).
- **suggested manual fix:** add a company-name → ticker dictionary pass (Broadcom→AVGO, etc.) and entity extraction for issuer names in earnings/legal headlines.
- **priority:** medium
- **first observed:** 2026-06-03 (recurring; ~21–22% mapped for multiple runs)

### TODO-stocks-atier-winrate
- **issue:** Stocks A-tier bucket is reproducibly net-negative (PF 0.286, totalR −5.0, winrate ~5.9%) while B-tier is profitable — A-tier scoring/gating is inverted relative to outcome quality.
- **evidence:** `signal-stats --asset-class stocks` By-tier: A n=25 PF 0.286 totalR −5.0; B PF ~1.7 totalR +33.
- **suggested manual fix:** review what pushes a stock to A-tier (RR-below-1.5 ideas still scoring 89–90 via regime/RS); consider an RR gate and an earnings-freshness penalty before A-tier promotion.
- **priority:** medium
- **first observed:** 2026-06-04 00:39 EEST (recurring)
