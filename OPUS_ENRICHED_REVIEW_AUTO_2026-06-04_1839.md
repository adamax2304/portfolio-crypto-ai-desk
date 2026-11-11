# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

- **Generated:** 2026-06-04 18:39 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, US-open-reaction slot 18:30).
- **Slot:** **US open reaction review** — ~2 h after the US cash open (09:30 ET / 16:30 EEST). Focus: how the AVGO/semis gap actually traded in the first session hours, which A/B setups confirmed or invalidated, early rotation read.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-04_1623.md` (≈2.0 h ago — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). AVGO −15%, Micron −6%, SanDisk −4%, **NVDA +0.73%**, the rotation to value (Dow +1.08% vs Nasdaq −0.76%), the BofA UNH upgrade, and the SMCI legal history all independently confirmed (Yahoo Finance WebFetch-verified, GuruFocus, Motley Fool, SEC EDGAR, TheStreet).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **The feared semi flush was orderly, and the rotation thesis from the 16:23 pre-open review is confirmed.** ~2 h into the cash session: **S&P −0.14%, Dow +1.08%, Nasdaq −0.76%.** AVGO is **~−15%** (AI guide reiterated not raised → sell-the-news), Micron −6%, SanDisk −4%, Intel/AMD/Arm/Marvell lower — **but NVDA is GREEN +0.73%**, exactly the relative-strength "tell" flagged pre-open. Money rotated **out of mega-cap semis into value/Dow and defensives**, not out of the market. TSMC's CEO reiterated multi-year AI chip undersupply — this is a **valuation/sell-the-news pullback, not an AI-thesis break.**
- **The one clean actionable this slot is UNH (A-tier long 80.8) — and it now has a fresh, independently-verified catalyst.** BofA upgraded **UNH Neutral→Buy, PT $420→$450 (June 4)**, confirming the desk's "health insurers flashing buy signals" read. UNH is defensive healthcare, **zero AVGO read-through**, and aligned with today's Dow/value bid. Caveat: the **A-tier stocks bucket is a statistical loser this week (PF 0.20, WR 6.7%, −8R)** → treat as **cautious long on a clean reclaim of the 397.3–399.6 entry zone, half-size**, not an auto-green-light.
- **AMD is the priority contradiction: A-tier long in swing (81.8) / B-tier invest (78.3), but REJECTED no_trade in the live intraday report (50.4).** The swing/invest models are pointing long into a name that is **selling off today on the AVGO sympathy**. Cross-timeframe conflict resolves in favor of the live tape: **AVOID / WAIT — do not chase a semi long into the flush.** Watch NVDA (+0.73%) as the group-stabilization signal before touching AMD.
- **SMCI (B-tier swing/invest 76.3/76.4, high conf) is an AVOID on structural legal/headline overhang.** Confirmed: E&Y auditor resignation, prior SEC accounting probe, DOJ export-control/smuggling matter, a Nasdaq delisting scare, and an **ongoing board-led export-control review**. Good news for data hygiene: the fresh "8-K (FY2026)" the desk surfaced is **benign** — it's the April-15 annual-meeting filing (equity-comp plan + BDO auditor ratification), **not** a new adverse event. Net: **MANUAL REVIEW REQUIRED — never a clean B-tier actionable while the legal overhang stands**, and it is also a semi/AI-server name caught in today's selloff.
- **Crypto remains the 24/7 risk-off class with no fresh A/B.** Regime **high-volatility danger**, BTC/ETH downtrend, breadth ~21% > EMA20, BTC ATR percentile 100. Active B signals are all **waiting/triggered shorts on broken AI alts (NEAR, ICP, RENDER)** — late and extended — plus **counter-tape RS-leader longs (OPN +79%, MEME) below the active threshold**. Verdict: **NO-TRADE / WATCHLIST.**
- **Net action, next 4 h:** Stocks = **UNH is the only name aligned with the tape (cautious half-size long on a clean level); LLY is the defensive backup; AMD/SMCI/AVGO = stand aside.** Crypto = no-trade/watchlist, respect BTC downside. **One cautious actionable (UNH), everything else watch/avoid.**

---

## 2. Data Used

**Internal — fresh (<3 h):**
- `data/reports/scalp/2026-06-04_13-32_scalp_report.md` (gen 16:32 EEST; data freshness 13:15 UTC, ~2.1 h). Regime **high-volatility danger**, BTC/ETH downtrend, breadth 20.8% > EMA20, BTC ATR pct 100.
- `data/reports/intraday/2026-06-04_13-57_intraday_report.md` (gen 16:57 EEST; ~1.7 h). Regime **high-volatility danger**, breadth 20.8% > EMA20.
- `data/reports/stocks/intraday/2026-06-04_15-16_stocks_intraday_report.md` (gen 18:16 EEST; data freshness 15:16 UTC, ~0.4 h). **Fresh, live-session snapshot.** Regime bullish, VIX 15.76. UNH A 80.8, LLY B 75.5; AMD/SMH/SMCI rejected no_trade.
- `data/reports/stocks/swing/2026-06-04_14-55_stocks_swing_report.md` (gen 17:55 EEST; ~0.7 h) — **fresh.** AMD A 81.8, SMCI B 76.3.
- `data/reports/stocks/invest/2026-06-04_15-01_stocks_invest_report.md` (gen 18:01 EEST; ~0.6 h) — **fresh.** AMD B 78.3, SMCI B 76.4.
- `data/reports/swing/2026-06-04_14-44_swing_report.md` (crypto, gen 17:44 EEST; ~0.9 h) — fresh.
- `data/catalysts/2026-06-04/` — `catalyst_events.jsonl` (1844 cumulative rows), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_13-57.md`.
- LLM packets: `data/processed/llm_analysis_packet.md` (gen 17:45), `llm_stocks_packet.md` (gen 18:01).
- CLI / DB: `active-signals` (crypto 13 / stocks 50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-06-04` → **1 untracked (EPIC/USDT)**.

**External (this run — cited §13):** Yahoo Finance (WebFetch-verified: AVGO −15%, Micron −6%, SanDisk −4%, NVDA +0.73%, AI guide miss, pub 2026-06-04); GuruFocus (UNH BofA Neutral→Buy, PT $450, 2026-06-04); Motley Fool (SMCI SEC probe / E&Y resignation / DOJ smuggling history, 2026-03-20); SEC EDGAR (SMCI 8-K smci-20260415 = benign annual-meeting filing); TheStreet (June-4 market wrap: S&P −0.14%, Dow +1.08%, Nasdaq −0.76%, Iran/oil easing, TSMC chip-undersupply note).

**Unavailable / blind:** live tick-by-tick equity prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps, order-book depth/CVD, live ETF-flow feed, on-chain whale flows, token-unlock calendar (manual/unconnected); live social beyond RSS-bridged `t.me/*`.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-04_default_schedule/`.
- `scheduler.log` mtime **18:02 EEST → ~0.6 h** (fresh). Latest cycle summary `cycle_01_16-00_summary.md` mtime **18:02 EEST → ~0.6 h** (fresh).
- **NO DEFER** — both freshness checks well under the 3 h rule. Review proceeds normally.
- All six report families are **fresh (<3 h)** this run — crypto scalp ~2.1 h, intraday ~1.7 h; stocks intraday ~0.4 h, swing ~0.7 h, invest ~0.6 h. No carry-forward/stale exclusions needed this slot (a notable improvement over the 16:23 run, which had stale crypto-swing and pre-open stocks snapshots).

---

## 4. What Changed vs Previous Review (16:23 → 18:39)

- **The pre-open forecast became the realized session, and it landed on the milder/orderly end.** 16:23 feared Nasdaq-100 futures −1.3/1.4%; the actual ~2 h read is **Nasdaq −0.76%, S&P −0.14%, Dow +1.08%** — the rotation to value held, the broad market did NOT break. **NVDA confirmed green (+0.73%)** — the relative-strength tell was correct.
- **AVGO is no longer the central candidate — it has fully reacted (−15%) and is now context, not a decision.** The desk's stale pre-earnings AVGO A-tier long has aged out of the fresh intraday report (AVGO now rejected/short-rejected); the multi-run "AVGO stale post-earnings long" flag is **resolving on its own** as the reports refresh post-open.
- **UNH upgraded to the lead actionable with a NEW catalyst.** 16:23 had LLY as the lone clean A-name (UNH was not yet A-tier in the pre-open snapshot). The fresh 15:16 intraday report now scores **UNH A-tier 80.8**, and external research adds a **same-day BofA Buy upgrade (PT $450)** — a genuine upgrade in conviction vs last run.
- **AMD contradiction is NEW and sharper:** the freshly-regenerated swing/invest reports score AMD **A 81.8 / B 78.3 long**, while the live intraday report rejects it **no_trade 50.4**. A clean cross-timeframe conflict that did not exist this explicitly at 16:23.
- **Crypto regime unchanged (high-volatility danger);** breadth slipped slightly (25–27% → ~20.8% > EMA20), BTC ATR pct 98 → 100. Still zero fresh A/B. Active B short signals (NEAR/ICP/RENDER) persist.
- **Stocks A-tier loss bucket persists:** PF **0.20**, WR **6.7%**, totalR **−8.0** (n=27) vs B-tier PF 1.26 / +13R. No improvement (TODO-stocks-atier-winrate).
- **Catalyst mapping still weak:** **75.2% unmapped** (1387/1844) — essentially unchanged from 16:23's 76.2%. Multi-run regression (TODO-catalyst-mapping-weak).
- **Integrity flag carried forward:** `detect_untracked_legacy_alerts` still shows **1 untracked** — EPIC/USDT B scalp long sent 10:03 UTC, no matching proposed_signal (TODO-untracked-epic-alert).
- **Confirmed since last review:** AVGO sell-the-news, semi sympathy selloff, NVDA relative strength, value rotation, crypto risk-off — all confirmed.
- **Invalidated:** the pre-open "deep risk-off open" fear — the realized open was orderly/mixed, not a broad flush.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative JSONL): **1844**; mapped (non-empty `symbol`): **457**; unmapped: **1387** → **75.2% unmapped**.
- `narrative_baskets`: **3** (per latest report) — `perps_dex_narrative` (primary HYPE), `ai_narrative` (NEAR/RENDER/TAO/FET), `momentum_breakout` (HEI/EPIC/WLD). All `single_source`; AI basket fresh <6 h.
- **⚠️ catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped > 50%).
- Top 3 unmapped headlines (symbol unresolved, all clearly tickered): (1) "Tilly's (**TLYS**) Q1 2026 Earnings Call Transcript"; (2) "Petco (**WOOF**) Q1 2026 Earnings Call Transcript"; (3) "ChargePoint (**CHPT**) Q1 2027 Earnings Transcript". The resolver continues to drop explicitly-tickered names into the unmapped bucket — same failure mode as prior runs.

---

## 6. Market Landscape

**Stocks (the live story this slot):** The session opened into the Broadcom-led semi selloff and it traded **orderly, not panicky**. ~2 h in: **S&P −0.14%, Dow +1.08%, Nasdaq −0.76%**, VIX low-16s. AVGO −15% (beat on EPS/rev but reiterated rather than raised the AI target → sell-the-news), Micron −6%, SanDisk −4%, Intel/AMD/Arm/Marvell lower; **NVDA +0.73%** the standout. The leadership that inverted is **mega-cap semis**, and the bid rotated to **Dow/value and defensives (healthcare)** — classic late-cycle rotation, not a de-risking event. TSMC's CEO reiterating multi-year AI chip undersupply caps the downside narrative: **the AI buildout thesis is intact; this is a valuation reset in the most-stretched names.** Iran/oil overlay eased intraday. **Posture: favor the rotation winners (healthcare/value), avoid chasing the semi knife; NVDA stabilization is the green-light for the group.**

**Crypto (24/7, risk-off):** Regime **high-volatility danger**; BTC/ETH downtrend; breadth ~20.8% > EMA20; BTC ATR pct 100 (elevated). Narrative heat concentrated in **AI (rising, heat 58–63)** — but every AI alt is **down** (NEAR −23%, ICP −14/−16%, RENDER −14%, FET −18%): the AI *narrative basket is bleeding, not leading*. Lone green outliers (OPN +79%, MEME +11/12%, ZBT +9/11%) are low-volume counter-tape pops, watchlist-only. Headline news is uniformly bearish (SOL 2.5-yr low, XRP 4-month low, "Crypto Crashes / New Lows In Sight"). No fresh A/B; the desk says "reduce size or no trade until structure settles."

---

## 7. Candidate Deep Dives (≤5)

### 7.1 UNH — A-tier LONG 80.8 (stocks intraday) → **CAUTIOUS ACTIONABLE (half-size, on a clean level)**
- **Tier/role:** A-tier intraday long 80.8 (high conf); also B-tier swing 73.6 / invest 70.5 — consistent long across all three timeframes.
- **Catalyst (verified, fresh):** **BofA upgrade Neutral→Buy, PT $420→$450, June 4, 2026** (GuruFocus); internal RSS "UNH, CVS Lead S&P 500 Health Insurers Flashing Buy Signals" (Yahoo, 2026-06-04). Consensus rating Buy (62% Buy / 24% Strong Buy).
- **Tape alignment:** Healthcare/defensive, **zero AVGO/semis read-through**, and squarely in today's Dow/value rotation (Dow +1.08%). RS vs SPY +5.88%, RS vs XLV +4.43%. Earnings-safe.
- **Price-reaction / chase check:** entry zone **397.31–399.64**, current near zone; not overextended; **SL (invalidation) close beyond 392.65**; TP1 406.63 / TP2 411.29 / TP3 418.28. RR to TP1 only ~1.0 (the desk flags low RR) — so the edge is the catalyst + rotation, not the geometry. Actionable on a clean reclaim/hold of the entry zone; do not chase if >2 ATR extended.
- **Risk caveat:** A-tier stocks bucket PF 0.20 / WR 6.7% this week → **half-size, demand a clean level.**

### 7.2 AMD — swing A 81.8 / invest B 78.3 LONG vs intraday REJECTED no_trade 50.4 → **AVOID / WAIT (catalyst-vs-technical contradiction, priority-2)**
- **Contradiction:** the longer-timeframe models (swing/invest) rank AMD a top long (RS vs SPY +19.7/+20.8%, "RS leader", 3 news catalysts), while the **live intraday report rejects it no_trade** — because AMD is **down today in the AVGO semis sympathy selloff** (Yahoo: "Intel, AMD, Micron shares sink…"). The longer-frame RS is real; the intraday entry is wrong-footed.
- **Price-reaction / chase check:** AMD has already reacted **down** with the group; an intraday long would be a knife-catch into a sector-wide flush on the exact day of the AVGO guide miss. **Entry now = fighting the live tape.** Local swing entry zone ~$49–52 (NB: an external "current price $542" print surfaced in search but conflicts with the desk's ~$50 level — **treated as unverified/mismatched, not cited as fact**).
- **What makes it actionable later:** group stabilization — **NVDA reclaiming/holding green (+0.73% today is the early tell)** and AMD reclaiming its intraday structure. Until then, the swing A-tier long is a **MANUAL REVIEW**, not a same-day execution.

### 7.3 SMCI — B-tier swing/invest 76.3/76.4 (high conf) → **AVOID / MANUAL REVIEW REQUIRED (legal/headline overhang, §I)**
- **LEGAL/HEADLINE RISK (verified):** Super Micro carries a stacked overhang — **E&Y auditor resignation** (internal-controls concerns), a prior **SEC accounting probe**, a **DOJ export-control / smuggling matter**, a past **Nasdaq delisting scare**, and a **board-led independent export-control review still ongoing** (Motley Fool, 2026-03-20; corroborated by SEC filing history). Per §I a stocks B-name with active legal flags **cannot be a clean actionable.**
- **Data-hygiene note (good news):** the fresh "Form 8-K (FY2026)" the desk surfaced with "date unava" is **benign** — it is the **April-15, 2026 annual-meeting filing** (equity-comp plan amendment + BDO auditor ratification), **not** a new adverse event (SEC EDGAR, smci-20260415). So there is no *new* bad headline today — but the structural overhang stands, and SMCI is also an AI-server/semi-adjacent name caught in today's group selloff.
- **Verdict:** **AVOID / MANUAL REVIEW** regardless of the 76+ score. The "date unava" parsing is logged as TODO-smci-8k-date.

### 7.4 LLY — B-tier LONG 75.5 (stocks intraday) → **WATCH / cautious defensive long (backup to UNH)**
- **Tier/role:** B-tier intraday long 75.5 (medium conf), RS leader; also B swing 68.3 / invest 65.9. RS vs SPY +12.0%, RS vs XLV +10.6%. Earnings-safe.
- **Tape alignment:** Pharma/healthcare, **no AVGO read-through**, aligned with the defensive/value bid — same tailwind as UNH.
- **Catalyst gap:** unlike UNH, **no fresh news catalyst this run** (news_catalyst component 0.0) — the case is pure technical + RS + rotation. RR to TP1 ~1.0 (low).
- **Price-reaction / chase check:** entry zone **1128.46–1134.02**, SL (invalidation) close beyond **1117.33**, TP1 1150.71. Actionable only on a clean level; **secondary to UNH** (which has the live catalyst). Do not chase >2 ATR extended.

### 7.5 Crypto bucket (NEAR / OPN) — no A/B; both watchlist → **NO-TRADE / WATCHLIST**
- **NEAR/USDT** (active B scalp/intraday short ~64–70; catalyst-backed, AI basket): −23% 24h, RS vs BTC −18%, **already broken down and extended** ("late breakdown" counter-thesis, volume 0.9x). Fresh attention is real (importance 4.2) but the move has happened — **chasing the short here is late.** Watch a failed bounce into 2.38–2.43, not a market entry.
- **OPN/USDT** (top RS leader, +79% 24h, score ~58–64): a **counter-tape RS-leader long in a high-volatility danger regime** with sub-1x volume and no verified catalyst → watchlist-only, half-size at best, demand a defended pullback (0.217–0.229). Not actionable.
- **Net:** crypto has no clean A/B; the structured edges are all late/counter-tape. **No-trade.**

---

## 8. Best Candidates Ranked

1. **UNH (A long 80.8)** — the only name aligned with today's tape + a fresh BofA Buy/$450 catalyst. **Cautious half-size long on a clean reclaim of 397.3–399.6; SL 392.65.**
2. **LLY (B long 75.5)** — defensive backup, same rotation tailwind, but no fresh catalyst. Watch 1128–1134; SL 1117.33.
3. *(No third clean actionable.)* AMD, SMCI, AVGO and all crypto names are watch/avoid this slot.

---

## 9. Avoid / No Trade

- **AMD** — swing/invest A/B long contradicts the live intraday no_trade; selling off in the AVGO sympathy. Do not chase the semi long; wait for NVDA-led group stabilization.
- **SMCI** — legal/headline overhang (SEC/E&Y/DOJ/export-control review). AVOID / manual review regardless of 76+ score.
- **AVGO** — fully reacted (−15%, sell-the-news). Falling knife; no clean retest. Context only.
- **Crypto longs (OPN/MEME)** — counter-tape RS pops in a danger regime, low volume, no catalyst.
- **Crypto shorts (NEAR/ICP/RENDER)** — directionally right but late/extended; entering now is chasing a flushed move.

---

## 10. Main Risks

- **A-tier stocks bucket is a statistical loser this week (PF 0.20, WR 6.7%, −8R).** The single actionable (UNH) sits in that bucket → size down, treat the score with skepticism, lean on the catalyst + rotation, not the tier label.
- **Semi selloff could deepen if NVDA loses its green.** NVDA +0.73% is holding the group together; if it rolls over, the "orderly rotation" read flips to "broad tech de-risk" and even defensives can wobble.
- **Macro overlay (Iran/oil, 4-month-high jobless claims)** can re-introduce risk-off intraday even though it eased this morning.
- **Crypto downside:** high-volatility danger regime, BTC/ETH downtrend, ETF-outflow context, multiple alts at multi-month/multi-year lows — long beta is dangerous, short beta is late.
- **Catalyst layer is 75% unmapped** — do not let the narrative/catalyst score drive a decision this run; it is context only.
- **Source ingest** (§M) may fail silently if the DB schema changed — logged, non-blocking.

---

## 11. Action Plan — next 4 hours

1. **Stocks — UNH:** if it holds/reclaims **397.3–399.6** on the live tape, cautious **half-size long**, SL 392.65, first target 406.6. Skip if it gaps >2 ATR away or SPY breaks down hard.
2. **Stocks — LLY:** secondary defensive long on a clean **1128–1134** level, SL 1117.33. Only if UNH-style rotation persists.
3. **Stocks — AMD/SMH/AVGO/SMCI:** **stand aside.** Re-evaluate AMD only after NVDA confirms group stabilization (holds green / reclaims).
4. **Crypto:** **no-trade / watchlist.** Track NEAR/ICP/RENDER for *failed-bounce* short setups (not market entries) and OPN for a defended pullback. Respect BTC downside.
5. **Monitor:** NVDA tape (group tell), VIX, oil/Iran headlines, BTC local support.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO-TRADE.** Best structured names (NEAR/ICP/RENDER shorts, OPN/MEME longs) are below threshold / late / counter-tape. Watchlist only.
- **Crypto intraday:** **NO-TRADE / WATCHLIST.** Same as scalp; AI-alt shorts are extended, RS-leader longs are counter-tape in a danger regime.
- **Crypto swing:** **NO-TRADE.** Downtrend regime; no fresh A/B.
- **Stocks intraday:** **ONE CAUTIOUS LONG — UNH (half-size, clean level, SL 392.65);** LLY as defensive backup. Avoid all semis.
- **Stocks swing:** **NO clean execution.** AMD A-tier long contradicts the live selloff (manual review); UNH/LLY longs valid but better expressed intraday.
- **Stocks invest:** **NO same-day action.** AMD/SMCI B-tier longs are either tape-conflicted (AMD) or legally encumbered (SMCI). Defensive healthcare (UNH/LLY) is the cleaner long-term lean.

---

## 13. Sources

- [Intel, AMD, Micron shares sink as Broadcom results spark semiconductor sector sell-off — Yahoo Finance, 2026-06-04 (WebFetch-verified: AVGO −15%, Micron −6%, SanDisk −4%, NVDA +0.73%)](https://finance.yahoo.com/markets/article/intel-amd-micron-shares-sink-as-broadcom-results-spark-semiconductor-sector-sell-off-130128609.html) — verification: single_source; confirms semi selloff + NVDA relative strength.
- [UnitedHealth (UNH) Upgraded to Buy by BofA with Increased Price Target ($420→$450) — GuruFocus, 2026-06-04](https://www.gurufocus.com/news/8900702/unitedhealth-unh-upgraded-to-buy-by-bofa-with-increased-price-target) — verification: single_source; confirms UNH catalyst.
- [Super Micro Has Now Faced SEC Probes, Accounting Scandals, and Smuggling Charges — The Motley Fool, 2026-03-20](https://www.fool.com/investing/2026/03/20/super-micro-has-now-faced-sec-probes-accounting-sc/) — verification: single_source; confirms SMCI legal/headline overhang.
- [Super Micro Computer, Inc. — Form 8-K FY2026 (annual meeting: equity-comp plan + BDO ratification) — SEC EDGAR, filed 2026-04-15](https://www.sec.gov/Archives/edgar/data/0001375365/000137536526000012/smci-20260415.htm) — verification: primary_source; the surfaced 8-K is benign/governance, not a new adverse event.
- [Stock Market Today (June 4, 2026): stocks mixed, oil eases on Iran; semis breather after Broadcom — TheStreet, 2026-06-04](https://www.thestreet.com/stock-market-today/stock-market-today-june-4-2026-nasdaq-futures-slide-amid-iran-war-concerns) — verification: single_source; market-wrap levels (S&P −0.14%, Dow +1.08%, Nasdaq −0.76%) and TSMC chip-undersupply note (cross-checked against WebSearch aggregate).

## 14. Fix Requests / TODO

### TODO-stocks-atier-winrate
- **issue:** A-tier stocks bucket is a persistent statistical loser — PF 0.20, winrate 6.7%, totalR −8.0 (n=27) this week, vs B-tier PF 1.26 / +13R. The headline-actionable tier is the worst-performing tier.
- **evidence:** `python -m src.cli signal-stats --asset-class stocks` (by-tier table: A-tier weak, PF 0.2, WR ~6.7%); `data/reports/stocks/intraday/2026-06-04_15-16_stocks_intraday_report.md` §"Recent Signal Performance" → A-tier n=27 Total R −8.00 PF 0.200 WR 6.7%.
- **suggested manual fix:** audit the A-tier promotion gate for stocks — A-tier may be over-promoting low-RR (RR-to-TP1 ~1.0) trend-follow longs in a bullish regime that then mean-revert; consider an RR floor or a regime/extension penalty before A promotion. Multi-run regression (also flagged 12:42, 16:23).
- **priority:** high
- **first observed:** carried forward from earlier 2026-06-04 reviews; re-confirmed 2026-06-04 18:39 EEST

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-mapping below 25% — 75.2% of events unmapped (1387/1844), with clearly-tickered names (TLYS, WOOF, CHPT, RIVN) dropped into the unmapped bucket. Multi-run regression (~76% at 16:23 and 12:42).
- **evidence:** parse of `data/catalysts/2026-06-04/catalyst_events.jsonl` → mapped 457 / unmapped 1387; top unmapped headlines contain explicit parenthetical tickers the resolver ignored.
- **suggested manual fix:** extend the catalyst symbol resolver to extract parenthetical/`$`-prefixed tickers from headline text (e.g. regex `\(([A-Z]{1,5})\)`), and add an earnings-transcript title pattern. Would recover a large share of the unmapped equity headlines.
- **priority:** medium
- **first observed:** carried forward; re-confirmed 2026-06-04 18:39 EEST

### TODO-untracked-epic-alert
- **issue:** A Telegram-sent B-tier alert has no matching `proposed_signal`, so it will not contribute to PF/winrate/avgR (tracker has no signal_id to follow).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-04` → EPIC/USDT, B, scalp, score 66.0, long, sent_at 2026-06-04T10:03:27Z, trackable=NO.
- **suggested manual fix:** investigate the scalp alert path that emitted EPIC/USDT without persisting a `proposed_signal` (the PART-1 alert→signal linkage); backfill or reconcile so the alert is trackable. Carried forward from 16:23.
- **priority:** medium
- **first observed:** first seen ~16:23 EEST 2026-06-04; re-confirmed 18:39 EEST

### TODO-smci-8k-date
- **issue:** SMCI Form 8-K from the SEC EDGAR feed surfaces with "date unava" (date not parsed) and no event classification, so a benign April-15 annual-meeting filing appears in the live News/Catalysts block as if it were a fresh catalyst.
- **evidence:** `data/reports/stocks/intraday/2026-06-04_15-16_stocks_intraday_report.md` §4 → "SMCI — Super Micro Computer, Inc. - Form 8-K (FY2026) (SEC EDGAR, date unava)"; actual filing smci-20260415 is dated 2026-04-15 (equity-comp + BDO ratification).
- **suggested manual fix:** parse the EDGAR filing date (from the accession/filing index) instead of leaving "date unava", and classify routine 8-K item types (e.g. Item 5.07 annual-meeting votes) so governance filings are not mistaken for market-moving catalysts.
- **priority:** low
- **first observed:** 2026-06-04 18:39 EEST

### TODO-cli-active-signals-exit255
- **issue:** `active-signals` CLI renders its Rich table with box-drawing characters that fail on a non-UTF-8 Windows console and the process exits 255 despite producing output (signal-stats works once `PYTHONIOENCODING=utf-8` is set). A non-zero exit could break downstream automation that checks return codes.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` → exit code 255 with mojibake column headers; same command exits clean for `signal-stats` after `$env:PYTHONIOENCODING="utf-8"`.
- **suggested manual fix:** force UTF-8 on the Rich console (or set `PYTHONIOENCODING`/`console.encoding`) inside the CLI entrypoint, and ensure the command returns exit 0 on success.
- **priority:** low
- **first observed:** 2026-06-04 18:39 EEST
