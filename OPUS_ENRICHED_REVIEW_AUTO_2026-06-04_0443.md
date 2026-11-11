# Opus Enriched Review — Auto Cycle 04:43 EEST

- **Generated:** 2026-06-04 04:43 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`)
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-04_0039.md` (≈4 h ago — §4)
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim cited in §13 with source + date + URL. Motley Fool WebFetch verified the AVGO after-hours drop independently.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from local OHLCV/ATR/EMA report fields + cited external prints.
- **Clock:** 04:43 EEST Thursday. **US stock market is CLOSED** (regular session reopens ~16:30 EEST). Stock *intraday* signals below are NOT executable this cycle; crypto trades 24/7 and is the only actionable class right now.
- **Advisory only. No auto-trade.**

---

## 1. Executive Summary

- **No clean actionable candidate this cycle.** Stocks are closed and the actionable list is poisoned by the AVGO read-through; crypto is range/chop with no clean catalyst-backed entry. Posture: **watchlist / no-trade for fresh entries**, manage existing exposure.
- **Defining contradiction of this cycle: the regenerated stocks report (00:29 UTC) STILL re-issues AVGO as A-tier LONG 89.7 with a stale pre-earnings entry zone (473.25–478.07) and `earnings: UNKNOWN` — even though AVGO reported Q2 FY2026 the prior evening and SOLD OFF HARD.** AVGO printed record rev $22.187B (+48% YoY, slight miss vs $22.27B est), AI-semi +143%, strong Q3 guide ~$29.4B — yet fell **~8% (TradingKey) to ~14% (Motley Fool) after-hours June 3** on a textbook "sell the news" / valuation reaction. The desk's A-tier long is anchored ~12% above where the stock actually trades post-print. **Verdict for AVGO: AVOID / MANUAL REVIEW REQUIRED.**
- **Negative semi read-through into the 06-04 cash open.** AVGO's drop is a fresh bearish catalyst for the whole semi complex. The desk's other semi longs — **AMD B 79.1, SMH B 77.87 (also active SMH A 82.5 triggered), XLK B 73.7** — are technically bullish *against* that catalyst and carry **gap-down / sympathy risk at the open.** Do not chase fresh semi longs pre-open.
- **Stocks A-tier remains a statistically losing bucket** — `signal-stats` stocks: **tier=A n=27, PF 0.286, totalR −5.0, winrate 5.3%**, while **tier=B PF 2.11, totalR +51**. A-tier underperforming B is a persistent regression (TODO-stocks-atier-winrate).
- **Crypto: regime softened from "bearish trend" to "range/chop (neutral)"** (breadth 43.75% > EMA20, up from 35.4% last cycle), but BTC/ETH still downtrend and BTC ATR percentile **96 (elevated)**. New crypto B-tier scalps appeared — **OPN 68.8 (+91% 24h, NO catalyst, extended → chase risk)** and **SUSHI 67.2** — but both are below the active-trade threshold and flagged watchlist/no-trade. The only verified fresh catalyst is **ENA** (Coinbase USDe savings product, launch ~June 9–10) — best crypto *watch*, but counter-tape on weak volume (0.34×). **Catalyst mapping weak this run (106/500 mapped = 21%, 79% unmapped) — use catalyst layer as context, not final decision.**

---

## 2. Data Used

**Internal — fresh (<2 h):**
- `data/reports/scalp/2026-06-04_00-04_scalp_report.md` (gen 03:04 EEST, ~1.6 h). Regime: **range/chop (neutral)**, BTC/ETH downtrend.
- `data/reports/intraday/2026-06-04_00-22_intraday_report.md` (gen 03:22 EEST, ~1.3 h). Regime: **range/chop (neutral)**.
- `data/reports/stocks/intraday/2026-06-04_00-29_stocks_intraday_report.md` (~1.2 h; session=after-hours, regular session closed). Weekday.
- `data/catalysts/2026-06-04/` — `catalyst_events.jsonl` (500 rows), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_00-22.md` (03:22 EEST).
- CLI / DB: `active-signals` (crypto 14 / stocks 50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-06-04` → **None**.
- `db/crypto_ai_desk.sqlite` `news_items` — direct read for AVGO/ENA/AMD/SMH/OPN + Telegram-source rows (last 4 h).

**Internal — carry-forward / stale (swing/invest):**
- `data/reports/stocks/swing/2026-06-03_13-11_stocks_swing_report.md` — ~12.5 h → **borderline stale (flagged)**.
- `data/reports/stocks/invest/2026-06-03_13-15_stocks_invest_report.md` — ~12.4 h → **borderline stale (flagged)**.
- `data/reports/swing/2026-06-03_01-20_swing_report.md` (crypto) — ~24.3 h → **STALE (>14 h)**, excluded from fresh swing final-verdict; active ZEC/XLM swing *signals* used instead.

**External (this run — cited §13):** TradingKey + Motley Fool (AVGO Q2 FY26 print + AH drop, Motley Fool WebFetch-verified); CoinDesk + The Block (ENA / Coinbase USDe savings product, next-week launch).

**Unavailable / blind:** live US equity prices (market closed — last-close + after-hours prints only); TradingView / Chrome chart verification (tool not loaded); liquidation heatmaps, order-book depth/CVD, ETF-flow live feed, on-chain whale flows, token-unlock calendar (manual/unconnected); live social beyond RSS-bridged `t.me/lookonchain`.

---

## 3. Scheduler / Data Freshness

- **Scheduler: FRESH — review proceeds.** Latest run folder `data/scheduled_runs/2026-06-03_default_schedule/`. `scheduler.log` mtime **03:30 EEST (~1.2 h)**; latest `cycle_03_02-45_summary.md` mtime **03:30 EEST (~1.2 h)**. Defer rule requires BOTH > 3 h — not met.
- Crypto scalp / intraday: **fresh** (~1.3–1.6 h).
- Stocks intraday: **fresh** (~1.2 h) but **market closed** → not executable this cycle.
- Stocks swing / invest: **borderline stale** (≈12.4–12.5 h, 12–14 h band) — context only, flagged, excluded from fresh final call.
- Crypto swing report: **STALE (≈24.3 h)** — excluded from swing final-verdict.

---

## 4. What Changed vs Previous Review (00:39 EEST)

- **AVGO contradiction now PERSISTS INTO A REGENERATED SCORE.** The 00:39 review already flagged the after-hours sell-off. New this cycle: the stocks report regenerated at 00:29 UTC and **still re-issues AVGO A-tier long 89.7 at the pre-earnings entry (473–478) with `earnings: UNKNOWN`** — the negative catalyst and the ~$415 after-hours price are NOT reflected. The pipeline is scoring on stale price + missing earnings date. (TODO-avgo-stale-postearnings-signal, TODO-stocks-earnings-unknown.)
- **Crypto regime improved one notch:** prior cycle = "bearish trend (risk-off)"; now = **"range/chop (neutral)"**, breadth 43.75% > EMA20 (was 35.4%). BTC/ETH still downtrend, ATR 96 elevated. Mild stabilization, not a trend change.
- **New crypto B-tier scalps appeared:** OPN 68.8 and SUSHI 67.2 (prior cycle had "zero fresh A/B"). Both remain below active threshold (watchlist). OPN is +91% 24h with no catalyst → chase risk.
- **A-tier roster (stocks):** AVGO A re-issued; SMH A 82.5 + AMD remain triggered in active list.
- **Catalyst mapping:** **79% unmapped** (vs 80.4% prior) — still weak, recurring.
- **Telegram flow turned bearish-BTC:** `t.me/lookonchain` rows (last 4 h) flag **Mt. Gox depositing BTC to exchanges** and **James Wynn opening a 40x BTC short** — risk-off micro-signals (single-source social, low weight).
- **ENA catalyst unchanged** but now corroborated with a launch window (~June 9–10).

---

## 5. Catalyst Coverage

- **catalyst_events today: 500** (`data/catalysts/2026-06-04/catalyst_events.jsonl`)
- **Mapped (non-null symbol): 106 (21.2%)**
- **Unmapped (null symbol): 394 (78.8%)**
- **narrative_baskets: 3**
- ⚠️ **Catalyst mapping weak this run (79% unmapped > 50%) — use catalyst layer as context, not final decision.**
- Top unmapped headlines (symbol resolver missed):
  1. `Tilly's (TLYS) Q1 2026 Earnings Call Transcript` (ticker in title, not resolved)
  2. `Stock Market Today, June 3: Markets End Winning Streak on Middle East Escalation Fears`
  3. `Petco (WOOF) Q1 2026 Earnings Call Transcript` (ticker in title, not resolved)
- Note: several unmapped rows carry an explicit ticker in parentheses (TLYS, WOOF, CHPT) the resolver failed to extract → recurring symbol-resolver gap (TODO-catalyst-symbol-resolver).

---

## 6. Market Landscape

**Crypto (live, actionable):** Range/chop neutral; BTC & ETH downtrend; breadth 43.75% > EMA20; BTC ATR percentile 96 (elevated vol). Recommended style: mean-reversion / wait for clean breakouts. RS leaders are counter-tape momentum names (OPN +91%, WLD +41%, ENA +20%) mostly on **weak volume (0.06–0.87×)** = momentum without confirmation. Macro risk 35/100 (neutral). Narrative heat: Memes rising (attention 100), AI mixed, RWA mixed. Telegram on-chain flow leans risk-off (Mt. Gox deposits, large BTC short).

**Stocks (closed — frozen at last close + after-hours):** Regime **bullish** (VIX 16.06, breadth 100% > EMA20, all 4 indices uptrend). Semis (SMH +17.83% RS, XLK +14.27% RS) led the tape into the AVGO print — but AVGO's ~8–14% after-hours drop is a fresh negative catalyst that implies **gap-down risk for the semi complex at the 06-04 open.** The bullish regime label is from last-close data and does not yet price the AVGO read-through.

---

## 7. Candidate Deep Dives (≤5)

### 7.1 — AVGO (stocks) · A-tier 89.7 long · **AVOID / MANUAL REVIEW**
- **Signal:** A-tier long, entry 473.25–478.07, invalidation <463.61, TP1 492.5. Confidence "high". `earnings: UNKNOWN`.
- **Contradiction (verified):** AVGO reported Q2 FY2026 on **2026-06-03 ~20:00 UTC** — record rev **$22.187B (+48% YoY**, slight miss vs $22.27B est), **AI-semi +143%**, Q3 guide **~$29.4B (above est)**, AI rev guided +200% YoY. Despite the beat the stock **fell ~8% (TradingKey) to ~14% (Motley Fool) after-hours** on valuation (42× fwd) + profit-taking after a +93% 1-yr run ("sell the news"). Internal `news_items` confirms (MarketWatch "Broadcom's stock falls despite accelerating AI-chip growth", 06-04 00:13; CNBC/StockTitan/PR Newswire prints 06-03 ~20:00).
- **LEGAL/HEADLINE RISK:** none found — this is an earnings/valuation reaction, not a legal event.
- **Price-reaction / chase check:** Yes — price has fully reacted (gapped down to ~$415 AH). The A-tier entry 473–478 is **~12% above** the after-hours price → the long signal is stale (pre-earnings) and effectively **invalidated** by the gap. Entering the printed zone now would be chasing a level the stock has already left to the downside. **Not actionable.** Actionable only after the cash open clarifies whether the gap holds/fills — manual review.
- **Verdict: AVOID / MANUAL REVIEW REQUIRED.**

### 7.2 — SMH (stocks) · B 77.87 (active A 82.5 triggered) · **AVOID FRESH LONG (gap risk)**
- **Signal:** B-tier long, entry 634.50–637.89, TP1 648.07; RS vs SPY +17.83%; ETF (no earnings).
- **Read-through risk:** SMH is the semis ETF — AVGO is a top holding alongside NVDA. AVGO's ~8–14% AH drop is a **direct negative read-through**; SMH likely gaps down at the 06-04 open. The bullish technical signal predates the catalyst.
- **Price/chase check:** entry is last-close based; a gap-down would invalidate the planned zone. No fresh long until the open prints and the gap stabilizes.
- **Verdict: AVOID fresh long pre-open; reassess after cash open.**

### 7.3 — AMD (stocks) · B 79.1 long · **WAIT (sympathy gap risk)**
- **Signal:** B-tier long, entry 537.84–542.43, TP1 556.21; RS vs SPY +48.50% (strong leader); earnings safe; no fresh news catalyst (news_catalyst score 0).
- **Read-through risk:** AMD is the strongest-RS semi name but is exposed to AVGO sympathy selling at the open. No idiosyncratic catalyst to offset.
- **Price/chase check:** entry is last-close; gap-down risk. Best-quality semi long *structurally* (RS leader, earnings safe), so it is the first to reassess **after** the open confirms the semi tape held.
- **Verdict: WAIT for the open; no fresh chase. Conditional long only if SMH/AMD reclaim the planned zone after the AVGO gap is absorbed.**

### 7.4 — OPN/USDT (crypto) · B 68.8 scalp (intraday C 63.4) · **NO CHASE / WATCH**
- **Signal:** B-tier scalp long, score 68.8 (below the active threshold per report), momentum 96.5, **+91.42% 24h**, RS vs BTC +95%, volume 1.99×. Entry pullback 0.2137–0.2249, invalidation <0.2000, TP1 0.2548. Current 0.2299.
- **Internal/external check:** **NO fresh verified catalyst** (report + `news_items` returned 0 rows for OPN). Pure momentum/volume expansion on a low-cap name; multi-exchange = binance+mexc, no derivatives confirmation.
- **Price-reaction / chase check:** +91% in 24h is extreme; support 0.1160 is ~50% below spot → the move is heavily extended and any entry above the pullback zone is chasing. Range/chop regime + no catalyst = high mean-reversion risk. Actionable only on a deep pullback into 0.2137–0.2249 that *holds*, which the report itself gates as watchlist.
- **Verdict: NO CHASE — pullback-only watch; do not enter at spot.**

### 7.5 — ENA/USDT (crypto) · C/B watchlist (active B 67.x) · **WATCH (best crypto idea), pullback-only**
- **Signal:** watchlist long, score 59.9–61.7 across scalp/intraday; +20% 24h; RS vs BTC +24%; volume 0.34× (weak). Conditional pullback 0.1080–0.1120, invalidation <0.1052, TP1 0.1163. Current ~0.1113.
- **Catalyst (verified):** **Coinbase Ventures bought ENA on the open market** and Coinbase + Ethena are launching an onchain dollar-savings product for Coinbase's 100M+ users, with **USDe distributed on Base**; founder Guy Young targets a **next-week launch (~June 9–10, 2026)** (CoinDesk 06-02, The Block 06-02). Internal `news_items` row (AMBCrypto 06-04 00:00, "ENA jumps 28%") consistent. This is the only candidate with a real, dated, forward catalyst.
- **Price/chase check:** ENA spiked ~20% then pared; volume 0.34× = relative strength not confirmed by current volume. Counter-tape (BTC/ETH downtrend). Spot 0.1113 sits just above the conditional pullback zone → chasing risk if entered now.
- **Verdict: WATCHLIST — pullback-only into 0.1080–0.1120; the launch window (June 9–10) is the catalyst to monitor. Best crypto idea but not active while below threshold and counter-tape.**

---

## 8. Best Candidates Ranked

**No clean candidates.** Stocks are closed and the actionable semi list (AVGO/SMH/AMD/XLK) is exposed to a fresh negative AVGO read-through into the open; crypto is range/chop with no entry that is both fresh and not-extended.

Least-bad watch order (for monitoring, not active entry):
1. **ENA/USDT** — only verified forward catalyst (Coinbase USDe launch ~June 9–10); pullback-only into 0.1080–0.1120.
2. **AMD** (post-open) — strongest-RS semi, earnings safe; reassess only after the AVGO gap is absorbed.
3. **OPN/USDT** — momentum leader but extended + no catalyst; deep-pullback-only.

---

## 9. Avoid / No Trade

- **AVGO** — A-tier long is stale (pre-earnings) and invalidated by the ~8–14% after-hours drop; entry is ~12% above post-print price. AVOID / manual review.
- **SMH / XLK** — semis ETFs facing direct AVGO gap-down read-through; no fresh long pre-open.
- **OPN/USDT** — +91% 24h, no catalyst, extended; do not chase at spot.
- **SMCI** — `no_trade`/rejected (score 53.75) and carries a still-live legal overhang (per prior reviews: Mar 2026 SDNY indictment / SEC probe / class actions — no June clearing event found this run). AVOID; an 8-K (Form 8-K FY2026) appears in the report but no verified clearing development. Not a candidate.
- **All crypto B-tier `waiting_for_entry`** (ENA/OPN/SUSHI/ZRO intraday) — below active threshold, range/chop tape. Watchlist only.

---

## 10. Main Risks

- **Semi gap-down at the 06-04 US open** driven by AVGO's after-hours drop — the dominant near-term risk; it would hit SMH/AMD/XLK longs and the broader QQQ.
- **Stocks A-tier is net-negative** (PF 0.286, totalR −5) — A-tier labels are attention flags, not green lights; the AVGO case is a live example.
- **Crypto chase risk** — RS leaders (OPN/WLD/ENA) are counter-tape on weak volume; range/chop + elevated ATR favors fakeouts.
- **Risk-off micro-flow** — Mt. Gox BTC exchange deposits + a large 40x BTC short flagged on `t.me/lookonchain` (single-source social).
- **Data-quality risk** — the desk re-issued a stale AVGO A-tier long on pre-earnings price with `earnings: UNKNOWN`; trusting raw scores without the post-print overlay would be a mistake this cycle.
- **Source ingest** — if the §M ingest CLI fails, citations remain in the JSON artifact (no decision depends on the ingest).

---

## 11. Action Plan — next 4 hours

1. **Crypto (actionable now):** No fresh entries. Hold watchlist. **ENA** — alert on a pullback into 0.1080–0.1120 that holds; the Coinbase USDe launch (~June 9–10) is the catalyst. **OPN/SUSHI** — pullback-only, no chase. Cut long aggression if BTC loses local support (Mt. Gox/short flow).
2. **Stocks (not executable until ~16:30 EEST):** Do NOT pre-position semis long. At the open, observe whether SMH/AMD absorb the AVGO gap; only then consider AMD (strongest RS) on a reclaim of its planned zone. Treat AVGO as manual-review until the cash session prints.
3. **Monitor:** AVGO cash-session direction (gap hold vs fill); BTC structure + on-chain flow; ENA launch headlines.
4. **System:** see §14 TODOs (stale post-earnings signal, earnings UNKNOWN, catalyst symbol resolver, A-tier winrate) for the next manual maintenance session.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** No-trade / watchlist. Best watch OPN (no chase) — range/chop, no catalyst. ENA pullback-only.
- **Crypto intraday:** No-trade. No A/B clears threshold; all watchlist. ENA best on catalyst, pullback-only.
- **Crypto swing:** No fresh call — swing report stale (24 h). Existing ZEC/XLM swing signals stand on their own levels; no new entry.
- **Stocks intraday:** Market closed + AVGO gap risk → no fresh longs. AVGO AVOID/manual. AMD/SMH reassess after open only.
- **Stocks swing / invest:** Borderline-stale data (~12.5 h) → context only, no fresh call this cycle.

---

## 13. Sources

- [Broadcom Q2 — Shares Slump 8% After Hours (TradingKey, 2026-06-03)](https://www.tradingkey.com/analysis/stocks/us-stocks/261944759-avgo-q2-earnings-broadcom-outlook-investors-ai-stock-after-tradingkey)
- [Broadcom's AI Revenue Soared 143% — So Why Is the Stock Falling? (The Motley Fool, 2026-06-03, WebFetch-verified: ~14% AH drop)](https://www.fool.com/investing/2026/06/03/broadcom-s-ai-revenue-just-soared-143-so-why-is-the-stock-falling/)
- [Coinbase backs Ethena ahead of savings product launch for 100M users (CoinDesk, 2026-06-02)](https://www.coindesk.com/business/2026/06/02/coinbase-backs-ethena-ahead-of-savings-product-launch-for-exchange-s-100-million-users)
- [Coinbase invests in Ethena via open-market ENA purchase, flags partnership (The Block, 2026-06-02)](https://www.theblock.co/post/403403/coinbase-invests-ethena-open-market-purchase-ena-flags-new-partnership)

_Internal corroboration (no external citation needed): `news_items` rows — AVGO (MarketWatch 2026-06-04T00:13; CNBC/StockTitan/PR Newswire 2026-06-03 ~20:00), ENA (AMBCrypto 2026-06-04T00:00). Telegram flow: `t.me/lookonchain` (Mt. Gox BTC deposits; 40x BTC short), single-source social._

---

## 14. Fix Requests / TODO

### TODO-avgo-stale-postearnings-signal
- **issue:** Stocks pipeline re-issued AVGO A-tier long 89.7 at a pre-earnings entry zone (473–478) in the 00:29 UTC report, ~12% above the actual after-hours price (~$415) following the 06-03 earnings drop. The signal is scored on stale price and ignores the just-completed earnings event.
- **evidence:** `data/reports/stocks/intraday/2026-06-04_00-29_stocks_intraday_report.md` Idea #1 (entry 473.25–478.07, `earnings: UNKNOWN`); external AVGO AH drop ~8–14% (TradingKey, Motley Fool 2026-06-03); `news_items` AVGO prints 2026-06-03 ~20:00 UTC.
- **suggested manual fix:** Gate A/B equity signals on an "earnings reported in last 24h" check that (a) forces an event-risk freeze / re-pull of post-print price before scoring, and (b) blocks re-issuing a pre-earnings entry zone once the event has occurred.
- **priority:** high
- **first observed:** 2026-06-04 04:43 EEST

### TODO-stocks-earnings-unknown
- **issue:** AVGO flagged `earnings: UNKNOWN` despite earnings being reported the prior evening; earnings-calendar lookup also failed for SPY/QQQ/IWM/DIA/SMH/XLK/XLF/XLE/XLY/XLV (ETFs, expected) but the AVGO miss is a real regression.
- **evidence:** stocks intraday report §0 "Earnings lookup failed for: …" and Idea #1 "earnings: UNKNOWN (calendar lookup missing — treat as undated event risk)".
- **suggested manual fix:** Audit the earnings-calendar source for single-stock coverage; AVGO's date was knowable (it reported 06-03). Recurring from prior reviews.
- **priority:** high
- **first observed:** carried from prior cycles; re-confirmed 2026-06-04 04:43 EEST

### TODO-catalyst-symbol-resolver
- **issue:** Catalyst mapping weak again — 106/500 mapped (21%), 79% unmapped. Several unmapped rows carry an explicit ticker in parentheses (TLYS, WOOF, CHPT) the resolver failed to extract.
- **evidence:** `data/catalysts/2026-06-04/catalyst_events.jsonl` (500 events, 106 mapped); top unmapped: "Tilly's (TLYS) Q1 2026 Earnings Call Transcript", "Petco (WOOF) Q1 2026 Earnings Call Transcript", "ChargePoint (CHPT) Q1 2027 Earnings Transcript".
- **suggested manual fix:** Add a parenthetical-ticker regex pass to the catalyst symbol resolver; recurring across multiple reviews (>50% unmapped for several runs).
- **priority:** medium
- **first observed:** carried from prior cycles; re-confirmed 2026-06-04 04:43 EEST

### TODO-stocks-atier-winrate
- **issue:** Stocks A-tier is a reproducibly losing bucket vs B-tier.
- **evidence:** `signal-stats --asset-class stocks`: tier A n=27 PF 0.286 totalR −5.0 winrate 5.3%; tier B PF 2.11 totalR +51 winrate 24.7%.
- **suggested manual fix:** Investigate why A-tier (highest-conviction) underperforms B; likely the A threshold over-weights regime/RS alignment and under-weights event/valuation risk (AVGO is a live example).
- **priority:** medium
- **first observed:** carried from prior cycles; re-confirmed 2026-06-04 04:43 EEST
