# Opus Enriched Review — US OPEN REACTION REVIEW — Auto Cycle 18:40 EEST

## 1. Executive Summary

**Monday 18:40 EEST "US open reaction review" slot — ~2h10m into the US RTH cash session (opened 09:30 ET / 16:30 EEST).** External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch verified on Analytics Insight US-market live page; TipRanks/Benzinga 403'd but corroborated by Yahoo + TheStreet + Analytics Insight).

**The gap-up the prior (16:30 pre-open) review flagged as "do not chase" has now HELD into the session — risk-on is confirmed, not a fade.** The US–Iran Strait-of-Hormuz peace deal ("now complete," signing targeted Friday in Switzerland) drove oil down and a clean rotation into growth/tech/semis. Cash-session prints: **S&P 500 +1.49%, Nasdaq +2.38%, Dow +1.20%, VIX 16.24**, stock breadth **100% > EMA20**, semiconductors the strongest sector (SMH RS vs SPY +13.69%). Crypto mirrors it: **BTC uptrend, ETH uptrend, alt breadth 91% > EMA20, BTC ATR percentile 19 (low vol)** — bullish trend, risk-on.

So the read is **risk-on longs, but two days into a one-way move the #1 trap is chasing extension, not direction.** Stocks have flipped from pre-market-demoted-to-C → **RTH-confirmed actionable**. The cleanest names are **AMD (intraday long, A-tier 88 / report-B 79.38, RS leader +27.3% vs SPY, Citi upgraded to Buy Jun 12)** and **JPM (intraday long, B 71, financials confirmed, RS follower)**. **Caveat on AMD: it is up ~+4–7.6% on the day (verified) — likely already trading at/above its 542.54–548.90 entry zone, so it is a pullback-into-zone idea, NOT a chase.** JPM is the less-extended of the two.

**Two explicit AVOIDs.** **UNH (long B 69.9)** is a long-vs-legal contradiction — the DOJ **criminal + civil** Medicare-Advantage fraud probe is confirmed and still active (Fierce Healthcare / TipRanks; shares previously −16%) → **AVOID / MANUAL REVIEW**. **SMH (long, active A-tier 82 / report-B 73.97)** is flagged by the system's own playbook as a **known structural-loser cohort** ("NVDA/SMCI/SMH longs structurally lose in this regime") — despite the high score, prefer AMD for semis exposure → **MANUAL / caution**. On crypto, **JTO (+40.9%, vol 8.49×)** is the top mover but massively overextended → **wait-pullback, do not chase**; **SMCI** carries an export-control indictment (SEC EDGAR 8-K) → avoid.

Track-record routing: crypto A/B stays weak (WR 14.7% / PF 1.07 / +3R, **shorts −4R PF 0.4**); stock A/B is net-positive (WR 30.8% / PF 1.13 / +2R) but **stock shorts are −17R** → longs-only this window, no fresh shorts in either class. Crypto scalp lane is structurally broken (PF 0.14 / −6R) → research-grade only. Advisory only; scanner / data-collection / tracking continue in all moods.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-15_14-03_scalp_report.md` — mtime 17:03 EEST → **fresh** (~1h37m).
- **Crypto intraday report** `data/reports/intraday/2026-06-15_14-17_intraday_report.md` — mtime 17:17 EEST → **fresh** (~1h23m).
- **Crypto swing report** `data/reports/swing/2026-06-15_14-49_swing_report.md` — mtime 17:49 EEST → **fresh** (~51m; <4h).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-15_15-30_stocks_intraday_report.md` — mtime 18:30 EEST → **fresh** (~10m; data freshness 15:30 UTC, **RTH / mid-session — A/B now confirmed, not pre-market**).
- **Stocks swing report** `data/reports/stocks/swing/2026-06-15_15-02_stocks_swing_report.md` — 18:02 EEST → fresh, but playbook **watchlist_only (paused)** → planning context only.
- **Stocks invest report** `data/reports/stocks/invest/2026-06-15_15-08_stocks_invest_report.md` — 18:08 EEST → fresh, but **watchlist_only (paused, 0W/24L)** → context only.
- **Catalysts** `data/catalysts/2026-06-15/` — events.jsonl + narrative_baskets.jsonl + `catalyst_cycle_14-17.md` (mtime 17:17 EEST → fresh).
- **LLM packets** `data/processed/llm_analysis_packet.md` (17:49) + `llm_stocks_packet.md` (18:09), both fresh.
- **Internal CLI:** `active-signals` (crypto 27 active B; stocks 50 — incl A-tier AMD 88 / SMH 82 / JPM 80 waiting_for_entry), `signal-stats` ×2, `detect_untracked_legacy_alerts` → **5 untracked (TAO, EDEN, CHIP×2, XPL)**.
- **DB note:** `data/crypto_ai.db` / `data/crypto_ai_desk.db` returned no tables to a read-only sqlite3 connection this run → news_items not queryable directly; fell back to catalyst_events.jsonl + report News sections (consistent, recent) per §G internal-first. Logged as §14 TODO.
- **External:** WebSearch ×2 (US session reaction + AMD/semis; UNH DOJ probe) + WebFetch verified (Analytics Insight US-market live page).

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-15_default_schedule/`.
- `scheduler.log` mtime **18:10:15 EEST** (~30m old) → **fresh**.
- Latest cycle summary `cycle_03_16-42_summary.md` mtime **18:10:11 EEST** (~30m old) → **fresh**.
- **Both well under the 3h defer threshold → review proceeds.**
- All crypto reports <2h, stock intraday ~10m → fresh. Stock swing/invest fresh but playbook-paused. No stale-data exclusions this run.

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-15_1630.md` (pre-US-open slot):

- **Gap-up HELD → risk-on confirmed.** Prior review: "futures gapping up, do NOT chase, wait first 15–30 min RTH confirmation." Now ~2h10m into RTH the move is sustained (S&P +1.49%, Nasdaq +2.38%) — the regime call is validated, not faded.
- **Stocks upgraded from pre-market-C → RTH-confirmed A/B.** JPM (B 69.95→71) and AMD (B 66.49→79.38, also active A-88) are now actionable in-session rather than "wait for confirmation."
- **AMD gained a catalyst.** Prior review treated AMD as pure-technical RS; web research now adds a **Citi Buy upgrade (Jun 12)** + semis-rotation tailwind → catalyst-backed.
- **New contradiction flag: SMH.** The stock playbook's own "known failure mode" marks NVDA/SMCI/SMH longs as structural losers in this regime — newly material because SMH is now an active A-tier 82.
- **UNH AVOID — unchanged / re-confirmed.** DOJ criminal+civil Medicare-fraud probe still active (re-verified this run).
- **Untracked alerts worsened: 2 → 5** (added CHIP×2, XPL alongside TAO, EDEN). Integrity regression trending the wrong way.
- **Catalyst mapping still weak** (~80.6% unmapped, ≈ prior's 81%). No improvement.
- **Crypto:** JTO emerged as the top mover (+40.9%) but overextended — replaces the prior ETH-pullback idea as the headline crypto name, though as a *do-not-chase*, not an entry.

## 5. Catalyst Coverage

- `catalyst_events.jsonl` (cumulative today): **total 2067, mapped 401, unmapped 1666 → 80.6% unmapped.**
- This-cycle scan (`catalyst_cycle_14-17.md`): 384 rows, 4 narrative baskets.
- **⚠ Catalyst mapping weak this run — use the catalyst layer as context, not final decision.** (unmapped > 50%, recurring across runs.)
- Top 3 unmapped (noise/macro): (1) "VP Vance thanks Americans for patience on Iran deal…", (2) "Hey @Alhikli, welcome to Lookonchain" (join-spam), (3) "Saving for Retirement in a 401(k)? 3 Costly Mistakes…".
- Narrative baskets: **ai_narrative** (NEAR/RENDER/TAO/FET — TAO surge 31.9%, related_beta_rotation), **perps_dex_narrative** (HYPE + DYDX/GMX, wait_pullback), **binance_ecosystem_teaser** (BNB/ASTER, sell-the-news risk), **momentum_breakout** (JTO/ZRO/ZEC — pure momentum, wait_pullback).
- Legal/regulatory flags surfaced by catalyst layer: **UNH** (DOJ probe), **SMCI** (export-control indictment, SEC EDGAR 8-K), **IMX** (Aztec Connect $2M exploit — old abandoned contract, low live impact).

## 6. Market Landscape

- **Stocks:** risk_on, VIX 16.24, breadth 100% > EMA20/50. QQQ/IWM/DIA uptrend, SPY range-but-positive. Strongest sectors: **semiconductors (SMH RS +13.69%)**, technology (XLK +6.43%), healthcare (XLV +3.50%). Weakest: energy (XLE −8.46%, US–Iran oil-down driven), communications (XLC −5.52%). 18 symbols earnings-safe (no near-term events).
- **Crypto:** bullish trend / risk-on. BTC uptrend, ETH uptrend, alt breadth 91% > EMA20 / 98% > EMA50, BTC ATR percentile 19 (low realized vol). Strongest: JTO (+40.9%, vol 8.49× — overextended), EIGEN (+16.9%), INJ (+12.2%), XLM (+16.9%), WLD (+23%, vol only 0.61×), GPS, BABY. Weakest (short bias): ZKC (−15.3%), OPG (−11.4%), STG (−9.3%), RIF, TRUMP.

### Market Mood / Risk Routing  (REQUIRED — PART 4)

- **Crypto mood:** risk-on (bullish trend, low vol)
- **Stocks mood:** risk-on (RTH-confirmed, semis-led)
- **Dominant narrative:** US–Iran Hormuz peace deal → oil down → rotation into growth/tech/**semiconductors** + AI; crypto risk-appetite supported
- **Preferred side now:** **longs** — RS-leader + catalyst-backed; no fresh shorts (both short books net-negative)
- **Best long candidate:** **AMD** (RS leader +27.3% vs SPY, Citi Buy upgrade, semis strongest sector) — but **pullback-into-zone only, do not chase the +4–7% day**
- **Best short candidate:** none clean — trigger: a **SPY/QQQ intraday breakdown back below the open** would re-open crypto failed-bounce shorts on ZKC/OPG/STG; until then shorts are counter-trend and the short books are −4R (crypto) / −17R (stocks)
- **Best catalyst-backed candidate:** **AMD** (Citi upgrade + semis macro). Crypto catalyst alt: ZRO (LayerZero $23M token unlock, +14% into it) — but **sell-the-news risk after the unlock**, watch-only
- **What to avoid:** UNH long (DOJ probe), SMH long (system structural-loser flag), JTO chase (+40.9% extended), SMCI (indictment), all fresh shorts, crypto scalp (PF 0.14)
- **What would change the view:** SPY/QQQ losing the opening range and VIX reclaiming ~18+ (flips to caution/short-watch); or AMD/JPM pulling back into entry zones cleanly (upgrades them from watch → actionable)

## 7. Candidate Deep Dives (≤5)

### 1. AMD — intraday long — A-tier 88 (active) / B 79.38 (report) — TOP PICK (on pullback)
- Thesis: AMD long, trend=uptrend, **RS=leader (+27.3% vs SPY, +13.6% vs semis sector)**, regime=risk_on. Earnings-safe.
- Entry zone 542.54–548.90; invalidation **close beyond 529.81**; TP1 567.99 / TP2 580.72 / TP3 599.82.
- **Catalyst:** Citi upgraded AMD to **Buy** from Neutral (Jun 12) on AI second-source thesis; US–Iran oil-down → growth rotation (verified Yahoo/TheStreet/Analytics Insight/Benzinga).
- **Price-reaction / chase check:** AMD is **up ~+4–7.6% on the day** → very likely already at/above the 542.54–548.90 zone. **Entry NOW would be late / a chase.** Actionable only on a **pullback into the zone**; report's own rule: do not chase if >2 ATR from entry.
- Mood-aligned: yes (risk-on long, RS leader, catalyst). Long / pullback-trigger idea. Invalidation clean.

### 2. JPM — intraday long — A-tier 80 (active) / B 71 (report)
- Thesis: JPM long, trend=uptrend, RS=follower (+5.6% vs SPY, +2.4% vs XLF), regime=risk_on, financials confirmed. Earnings-safe.
- Entry 320.02–321.11; invalidation **close beyond 317.83**; TP1 324.39 / TP2 326.58 / TP3 329.86.
- **Less extended than AMD** (RS follower, not a +7% mover) → cleaner risk/reward into the entry zone if price is near it. Counter-note: news_catalyst 0 (pure technical) and RR-to-TP1 below 1.5.
- Mood-aligned: yes. Long, actionable-near-zone. Lower conviction than AMD on RS but better entry geometry.

### 3. SMH — intraday long — active A-tier 82 / B 73.97 — CONTRADICTION → MANUAL/caution
- Thesis: SMH long, RS leader (+13.69% vs SPY), regime risk_on — semis strongest sector.
- **Contradiction:** the playbook's own "known failure mode" explicitly lists **NVDA/SMCI/SMH longs as structural losers in this regime**, and the stocks_swing lane on the same names is paused (pre-pause −33R). Despite A-tier 82, this is an over-promotion-risk cohort.
- Routing: prefer **AMD as the semis expression** (single-name RS leader + catalyst) over the SMH ETF. SMH long = **manual review / caution**, not a clean actionable.

### 4. UNH — intraday/swing long — B 69.9 / active C — AVOID (legal)
- **LEGAL/HEADLINE RISK:** DOJ **criminal + civil** Medicare-Advantage fraud probe (inflated risk-scores / diagnoses without physician confirmation); probe extends beyond Medicare to Optum Rx. Confirmed active this run (Fierce Healthcare; TipRanks "UNH sinks as DOJ criminal probe deepens"; shares previously −16%).
- A long signal directly contradicts an active criminal probe with prior −16% gap risk → **AVOID / MANUAL REVIEW REQUIRED**. Never a clean actionable regardless of score.

### 5. Crypto AI-narrative / momentum — WLD, TAO (long, primary lane) vs JTO (avoid-chase)
- **Primary lane** `crypto_swing_narrative_rs_momentum` is the system's best cohort (14d WR 72% / PF 5.80 / +24R). AI-narrative basket (TAO surge 31.9%, NEAR/RENDER/FET) + WLD (RS +19% vs BTC) fit it.
- **Chase check:** **JTO +40.9% / vol 8.49× is overextended** (momentum_breakout basket playbook = wait_pullback) → do NOT chase. WLD vol only 0.61× (weak confirmation). Cleanest crypto long is an **RS-leader pullback within the AI basket**, not the parabolic mover.
- **ZRO** catalyst: LayerZero +14% into a $23M token unlock → **sell-the-news risk post-unlock**, watch-only.
- Mood-aligned: yes (risk-on long). Actionable only on pullback/retest; crowding watch on the AI basket.

## 8. Best Candidates Ranked

1. **AMD long** (A-88/B-79.38) — best RS + catalyst, but **pullback-into-542.54–548.90 only**; do not chase the +4–7% day. Invalidation close <529.81.
2. **JPM long** (A-80/B-71) — cleaner entry geometry (320.02–321.11), financials confirmed, less extended. Invalidation close <317.83.
3. **Crypto AI-narrative RS-leader long** (WLD/TAO, primary lane PF 5.80) — on pullback/retest within the basket; crowding watch.

**Watch triggers (if none of the above sets up cleanly this window):**
- **long-watch AMD** — trigger: pullback into 542.54–548.90 with SPY/QQQ holding the open.
- **long-watch JPM** — trigger: tag of 320.02–321.11, hold above 317.83.
- **short-watch ZKC/OPG/STG (crypto)** — trigger: **SPY/QQQ break back below opening range + a failed bounce** on the weak name (counter-trend until then; do not pre-empt).
- **catalyst-watch ZRO** — trigger: post-unlock reaction (avoid the sell-the-news; only consider strength that holds AFTER the $23M unlock clears).

## 9. Avoid / No Trade (this decision window only)

- **UNH long** — active DOJ criminal+civil fraud probe; long-vs-legal contradiction.
- **SMH long** — system flags SMH/NVDA/SMCI longs as structural losers despite A-82; use AMD for semis instead.
- **SMCI** — export-control indictment (SEC EDGAR 8-K).
- **JTO chase** — +40.9% / vol 8.49×, overextended; wait_pullback.
- **All fresh shorts** — crypto short book −4R (PF 0.4), stock short book −17R; counter-trend in a confirmed risk-on session.
- **Crypto scalp entries** — lane PF 0.14 / −6R; research-grade only.

_(Scanner, candidate generation, tracking, and monitors continue in all moods — this is a current-window routing call, never a stop command.)_

## 10. Main Risks

- **Chase risk is the dominant trap** — two days into a one-way risk-on move; AMD already +4–7%, entering at extension invites the pullback. Demand the zone, not the print.
- **Rally-may-be-short-lived** — strategists warn the US–Iran deal's inflationary legacy persists; gold +2.7% to >$4,330 signals lingering inflation hedging even amid risk-on. A VIX reclaim of ~18+ flips the routing.
- **DB read failure** — `crypto_ai.db` / `crypto_ai_desk.db` exposed no tables to the read-only connection this run; news_items couldn't be queried directly (fell back to JSONL + report news). Verification depth on per-symbol Telegram news was reduced.
- **Catalyst layer ~80.6% unmapped** — context only, do not let it drive a final verdict.
- **Untracked alerts (5)** — TAO/EDEN/CHIP×2/XPL sent to Telegram won't contribute to PF/winrate; performance stats understate true alert flow.
- **Source ingest:** sources JSON built at `data/raw/enriched_review_sources/2026-06-15T184000.json`; ingest attempted per §M (see TODO if the DB-table issue blocks the UPSERT).

## 11. Action Plan — next 4 hours

1. **AMD** — watch for a pullback into **542.54–548.90**; only then a long, invalidation close <529.81, scale at 567.99/580.72. Do not chase above the zone.
2. **JPM** — long on a tag of **320.02–321.11** holding >317.83; cleaner-entry alternative to AMD.
3. **Crypto AI basket (WLD/TAO/NEAR)** — long only on pullback/retest within the basket; skip JTO (extended). Watch for crowding/rotation exhaustion.
4. **Short side** — stand down unless SPY/QQQ lose the opening range; then re-assess crypto failed-bounce shorts (ZKC/OPG/STG) only.
5. **Avoid:** UNH, SMH-long, SMCI, JTO-chase, crypto scalps.
6. **Re-check at 21:30 late-session slot:** did AMD/JPM tag entries? Did the rally hold into the close or fade (VIX/gold)? Are A/B near TP vs invalidation?

## 12. Final Verdict per Mode

- **Crypto scalp:** NO fresh entries — lane PF 0.14/−6R, research-grade only; bullish regime doesn't rescue the scalp horizon mismatch.
- **Crypto intraday:** longs-only, RS-leader/AI-narrative on pullback; no fresh shorts; skip overextended movers (JTO).
- **Crypto swing:** primary lane (PF 5.80) — AI-narrative RS-leader longs on pullback (WLD/TAO/NEAR), crowding watch; best risk-adjusted crypto lane.
- **Stocks intraday:** RTH-confirmed risk-on longs — **AMD (pullback) / JPM (near-zone)**; AVOID UNH (legal), caution SMH (structural-loser flag); no shorts (−17R).
- **Stocks swing / invest:** **watchlist_only (paused)** — planning context only, not Telegram-actionable.

## 13. Sources

- [Stock market today: Dow, S&P 500, Nasdaq soar on US-Iran pact to reopen Hormuz — Yahoo Finance (2026-06-15)](https://finance.yahoo.com/markets/stocks/live/stock-market-today-monday-june-15-224751171.html)
- [US Stock Market Live Updates: surge after US-Iran truce breakthrough — Analytics Insight (2026-06-15, WebFetch-verified)](https://www.analyticsinsight.net/stocks/us-stock-market-live-updates-dow-sp-500-and-nasdaq-futures-surge-after-us-iran-truce-breakthrough)
- [Stock Market Today (June 15, 2026): Nasdaq, S&P 500 jump after U.S.-Iran peace deal — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-15-2026)
- [Why Is AMD Stock Gaining Monday (Citi Buy upgrade Jun 12, semis rotation) — Benzinga (2026-06-15)](https://www.benzinga.com/markets/tech/26/06/53189543/why-is-amd-stock-gaining-monday-2)
- [Why AI Chip Stocks NVDA, AMD, INTC, AVGO Are Rising Today — TipRanks (2026-06-15)](https://www.tipranks.com/news/why-ai-chip-stocks-nvda-amd-intc-and-avgo-are-rising-today-june-15-2026)
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx — Fierce Healthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth)
- [UnitedHealth stock UNH sinks as DOJ criminal probe into Medicare fraud deepens — TipRanks](https://www.tipranks.com/news/unitedhealth-stock-unh-sinks-as-doj-criminal-probe-into-medicare-fraud-deepens)

_Internal sources: stocks/crypto reports (scalp 14-03, intraday 14-17, swing 14-49, stocks intraday 15-30), `catalyst_cycle_14-17.md`, narrative_baskets.jsonl, LLM packets, `active-signals`/`signal-stats`/`detect_untracked_legacy_alerts` CLI. SMCI/UNH/IMX legal+exploit flags from catalyst layer (SEC EDGAR 8-K / Fierce Healthcare / Cointelegraph)._

## 14. Fix Requests / TODO

### TODO-untracked-alerts
- **issue:** **5** untracked legacy crypto alerts (TAO/USDT B scalp 76.3; EDEN/USDT B scalp 68.4; CHIP/USDT B scalp 76.8; XPL/USDT B scalp 75.8; CHIP/USDT B swing 71.6) sent to Telegram without a matching `proposed_signal` → no PF/winrate/avgR contribution. **Up from 2 at the 16:30 run** — regression worsening.
- **evidence:** `scripts.detect_untracked_legacy_alerts --since 2026-06-15` — all 5 trackable=NO; scalp alerts at 08:52 & 14:02–14:03 UTC, swing 14:49 UTC.
- **suggested manual fix:** trace the scalp/swing alert path emitting a watchlist_alert without registering a proposed_signal; ensure signal_id linkage at send time (PART 1 regression).
- **priority:** high (count rising run-over-run)
- **first observed:** 2026-06-15 16:30 EEST (recurring, now growing)

### TODO-db-tables-empty
- **issue:** `data/crypto_ai.db` and `data/crypto_ai_desk.db` returned an **empty `sqlite_master`** (no tables) to a plain read-only sqlite3 connection this run → could not query `news_items` for fresh Telegram/per-symbol news; fell back to catalyst JSONL + report news sections.
- **evidence:** `SELECT name FROM sqlite_master WHERE type='table'` → `[]` on both files. (Prior reviews referenced `db/crypto_ai_desk.sqlite` — path/handle may have moved or the canonical DB lives elsewhere / under WAL with a different attach path.)
- **suggested manual fix:** confirm the canonical news_items DB path used by the review skill (`db/crypto_ai_desk.sqlite` vs `data/*.db`); update §E read step to the correct handle so per-symbol news verification is restored.
- **priority:** medium
- **first observed:** 2026-06-15 18:40 EEST

### TODO-catalyst-mapping-weak
- **issue:** catalyst symbol-mapping ~19% (mapped 401 / unmapped 1666; **80.6% unmapped**) — recurring >50% unmapped across runs; keeps the catalyst layer at context-only.
- **evidence:** `data/catalysts/2026-06-15/catalyst_events.jsonl`; top unmapped = macro/spam (Vance Iran deal, Lookonchain welcome, 401k article).
- **suggested manual fix:** improve the symbol/ticker resolver and filter macro/join-spam before importance ranking.
- **priority:** medium
- **first observed:** 2026-06-15 16:30 EEST (recurring)

### TODO-lookonchain-spam
- **issue:** `t.me/lookonchain` "welcome to Lookonchain" join-confirmation rows ingested as catalyst events (noise in unmapped set).
- **evidence:** catalyst_events.jsonl unmapped sample "Hey @Alhikli, welcome to Lookonchain".
- **suggested manual fix:** drop welcome/join-confirmation messages at the collector source.
- **priority:** low
- **first observed:** 2026-06-15 16:30 EEST (carried forward)

### TODO-mexc-scalp-discover
- **issue:** scalp report shows thin MEXC/bybit coverage (bybit universe=0, mexc ohlcv_fetched=0, failed=45) while swing/intraday cycles fetched normally — partial discover/connectivity failure persists on the scalp cycle's MEXC/bybit legs.
- **evidence:** `data/reports/scalp/2026-06-15_14-03_scalp_report.md` §0 Exchange Coverage.
- **suggested manual fix:** investigate scalp-cycle MEXC/bybit instrument-discovery (rate-limit / geo / handle reuse); surface a thin-breadth warning in the scalp report header.
- **priority:** low
- **first observed:** 2026-06-15 18:40 EEST (related to prior TODO-exchange-discover-fail)
