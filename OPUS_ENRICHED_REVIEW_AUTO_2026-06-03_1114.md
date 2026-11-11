# Opus Enriched Review — Auto Cycle 11:14 EEST

- **Generated:** 2026-06-03 11:14 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`)
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-03_0212.md` (≈9 h ago — the intervening slots did not fire, so the 02:12 run is the most recent prior auto-review)
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim is cited in §13 with source + date + URL.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from the system's local OHLCV/ATR/EMA report fields.

---

## 1. Executive Summary

- **SMCI legal overhang is REAL and ACTIVE — and the system is still scoring it B-tier 71.26 "low risk."** This is the canonical regression case. External verification (Supermicro's own IR statement + securities-bar filings) confirms: a **March 19, 2026 SDNY criminal indictment** of three SMCI-associated individuals (incl. an SVP/board member) for an export-control conspiracy diverting **~$2.5B** of AI servers to China; **Ernst & Young resigned** as auditor (Oct 30, 2024); and an **active securities class action** (class period Feb 2, 2024 – Mar 19, 2026; lead-plaintiff deadline was May 26, 2026). **SMCI → AVOID.** The prior 02:12 run explicitly *dismissed* this ("overhang already cleared, no fresh flag") — that was wrong; the flag is live.
- **Two-speed tape, sharper than 9 h ago.** Crypto is in **high-volatility danger** (BTC & ETH downtrend, BTC ATR percentile 100), **zero A/B-tier crypto setups** — desk no-trade is correct. US stocks regime still prints **bullish** (VIX 15.77, 100% breadth) but that snapshot is from the 06:54-UTC after-hours pull and the cash session is closed until 16:30 EEST.
- **AVGO reports earnings TONIGHT (Wed Jun 3, after US close)** — externally confirmed (consensus EPS ~$2.40 on ~$22.1B rev, +47% YoY). System has it **swing-blocked / C-tier 59.32**. No fresh AVGO position into the print; it sets AI-semi direction for NVDA/AMD/SMH/SMCI.
- **AMD downgraded A → B since the last review** (intraday 84.7 → 78.45). Still the strongest single-name RS (+46.91% vs SPY) but extended; stocks A-tier remains the worst tier this week (PF 0.27, 6% triggered winrate, n=43). Trend-respect, no chase — pullback-entry only.
- **Crypto deteriorated:** BTC ~**$65.3–67K** (intraday low ~$65,372), ETH **below $1,900** (~$1,839), **$1.86B of 24 h liquidations** (mostly longs), 16 straight days of ETH ETF outflows, MicroStrategy's first disclosed BTC sale. No actionable crypto trade. **Catalyst mapping weak this run (81.2% unmapped) — context only.**

---

## 2. Data Used

**Internal — fresh (<2 h):**
- `data/reports/scalp/2026-06-03_06-31_scalp_report.md` (gen 09:31 EEST; data freshness 06:15 UTC)
- `data/reports/intraday/2026-06-03_06-45_intraday_report.md` (gen 09:45 EEST; data freshness 06:30 UTC)
- `data/reports/stocks/intraday/2026-06-03_06-54_stocks_intraday_report.md` (gen 09:54 EEST; session = after-hours) — weekday, fresh
- `data/catalysts/2026-06-03/catalyst_cycle_06-45.md` + `catalyst_events.jsonl` + `narrative_baskets.jsonl`
- `data/processed/llm_analysis_packet.md` (09:45), `llm_stocks_packet.md` (09:54)
- Cycle summary `cycle_06_09-17_summary.md` (16/16 steps OK, finished 09:55 EEST)
- CLI / DB: active-signals (crypto 4 / stocks 20 rows), signal-stats (crypto + stocks, from the 09:55 cycle), `detect_untracked_legacy_alerts --since 2026-06-03` (**None**), direct `news_items` queries on SMCI/AAPL/AMD/NVDA/AVGO/SMH.

**Internal — carry-forward (older than the 12 h swing/invest refresh expectation):**
- `data/reports/swing/2026-06-03_01-20_swing_report.md` — **≈6 h 50 m old** (gen 04:20 EEST). Carry-forward.
- `data/reports/stocks/swing/2026-06-03_01-26_stocks_swing_report.md` — **≈6 h 45 m old**. Carry-forward.
- `data/reports/stocks/invest/2026-06-03_01-30_stocks_invest_report.md` — **≈6 h 40 m old**. Carry-forward.

**External (this run — cited §13):** Supermicro IR + SEC + Hagens Berman/PRNewswire (SMCI indictment, EY resignation, class action); MarketBeat/StockTitan/AlphaStreet (AVGO earnings date + consensus); CryptoTimes / Bitcoin.com / CoinDesk / The Block (BTC price, liquidations, ETF outflows).

**Unavailable / blind:**
- TradingView / Chrome chart verification — tool not loaded.
- Live social attention (Reddit sources 403-failing; X/Telegram/Discord not connected — the RSS bridge does carry t.me/WalterBloomberg + t.me/lookonchain rows; last 4 h of t.me were lookonchain "welcome" noise + one whale line, nothing symbol-actionable).
- Liquidation heatmaps, order-book depth/CVD, ETF-flow feed, on-chain whale flows, token-unlock calendar — all still manual/unconnected.

---

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: **2026-06-03 09:55 EEST** (≈1 h 20 m before this run) → **ALIVE** (< 3 h threshold).
- Latest cycle summary: `cycle_06_09-17_summary.md` mtime **09:55 EEST** (≈1 h 20 m ago) → fresh. **Not deferred.**
- Crypto scalp/intraday + stocks intraday: **fresh** (<2 h).
- Crypto swing + stocks swing/invest: **carry-forward** (~6.7 h old; within the 4–12 h carry-forward band, not yet borderline-stale). Next refresh expected at the 16:04 EEST cycle.

---

## 4. What Changed vs Previous Review (02:12 EEST)

- **SMCI — thesis INVALIDATED vs prior run (the key delta).** The 02:12 review listed SMCI as "qualifying-but-not-deep-dived… legal overhang already cleared last run, no fresh flag." This run deep-dived it and the overhang is **confirmed live** (active class action, lead-plaintiff deadline May 26 2026; Mar 19 2026 criminal indictment; EY resignation). SMCI moves from an un-flagged B-tier to **AVOID / MANUAL REVIEW**.
- **AMD downgraded A → B.** Prior: A-tier intraday 84.7 / swing 81. Now: **B-tier intraday 78.45** (score −6.3, tier drop). Same "respect-trend-no-chase" verdict, but conviction lower.
- **AVGO downgraded B → C.** Prior: B-tier 67.3 (−16 earnings penalty). Now: **C-tier 59.32, swing-blocked by earnings.** Same event, now imminent (today after close).
- **AAPL is now the top stock score (79.64), narrowly above SMH 78.56 and AMD 78.45.** All three are new-this-cycle B-tier intraday signals (created ~09:54), status `waiting_for_entry`.
- **Iran / Strait of Hormuz risk-off (the 02:12 headline NEW catalyst) has faded from the fresh feed.** This run's macro layer reads **risk 35/100, neutral / data-watch**, top macro headline is the benign Bittensor "compute power" line — no fresh Nobitex/Hormuz/tanker headlines surfaced in the 06:45 catalyst scan. Treat the Iran overlay as **latent/unconfirmed this cycle**, not an active driver (still worth a manual eye given it was live 9 h ago).
- **Crypto deteriorated, not recovered.** BTC ~$67–69.5K (prior) → **~$65.3–67K** now; ETH broke **<$1,900**. $1.86B liquidations + 16-day ETH ETF outflow streak. Danger read confirmed and deeper.
- **Confirmed by data:** crypto no-trade (danger regime, zero A/B); stocks bullish-but-event-gated by AVGO. **Not invalidated:** no candidate's invalidation level was breached intra-review.

---

## 5. Catalyst Coverage

- `catalyst_events.jsonl` (2026-06-03) total rows: **993**
- Mapped (non-empty symbol): **187**
- Unmapped (empty/null symbol): **806** → **81.2% unmapped**
- Narrative baskets: **3** (perps_dex_narrative → HYPE; ai_narrative → NEAR/RENDER/TAO/FET; momentum_breakout → GENIUS/ONDO/ENA, fresh <1 h)
- **⚠️ catalyst mapping weak this run — use the catalyst layer as context, not final decision.** (unmapped 81.2% > 50%)

**Top 3 unmapped headlines by importance (human eye):**
1. `0.70` — *MoneyGram announces MGUSD launch despite shaky CLARITY Act approval odds* (AMBCrypto)
2. `0.70` — *Blockchain Association urges Senate to pass Clarity Act with letter from 160 former security officials* (The Block)
3. `0.65` — *Palo Alto Networks projects $3.345B–$3.355B Q4 revenue / 40% FCF margin target fiscal 2028* (Seeking Alpha)

---

## 6. Market Landscape

### Crypto — DANGER (no-trade)
- BTC trend downtrend, ETH trend downtrend; altcoin breadth above EMA20 = **33.3%**, EMA50 = 36.7%; BTC ATR percentile **100** (volatility elevated). System style: *reduce size or no trade until structure settles.*
- External: BTC tumbled to a 24 h low ~**$65,372**, briefly reclaimed **>$67K**; −6% session / −12–13% week; **$1.86B liquidated in 24 h** (BTC $896M, ETH $482M, SOL $91M — mostly longs); ETH **<$1,900** (~$1,839, −7.9% 24 h) with its **16th straight day of ETF outflows**; drivers include MicroStrategy's first disclosed BTC sale and a Mt. Gox wallet transfer. **$65K is the key support; break → $60K target.** Confirms the desk's danger read.
- Money flow: relative-strength pockets (ONDO +16.9%, EPIC +20.5%, GENIUS +29.2%, BIO, ENA, NEAR/ICP) but **every long is rejected** as *"conflicts with current market regime"* (and ONDO flagged *>2 ATR from EMA20 — do not chase*). Weakest names (short-bias) TAO/SOL/BNB/ETH/DOGE.
- Baskets live (all single_source): `momentum_breakout` (GENIUS/ONDO/ENA, fresh <1 h) is a *"pure momentum cluster, no confirmed news catalyst"* — explicitly not promotable in a danger regime.

### Stocks — BULLISH on the data (weekday; intraday fresh, swing/invest carry-forward)
- 4/4 indices uptrend; SPY +5.79% 20d, QQQ +10.89% 20d, IWM +4.96%, DIA +5.00%; **VIX 15.77**; breadth 100% above EMA20/50.
- Sector leadership: **semiconductors SMH (RS vs SPY +18.96%)** and **technology XLK (+16.53%)**; laggards utilities (−11.11%), energy (−8.20%), communications (−7.97%).
- Event risk: **AVGO earnings today after close** (swing-blocked). SMH/XLK/QQQ carry **"earnings UNKNOWN"** flags (calendar lookup missing) → undated event risk on any held position. 17 other names earnings-safe.
- Caveat: the bullish snapshot is from the 06:54-UTC after-hours pull; the US cash session is closed until 16:30 EEST. These are prep-only watchlist setups.

---

## 7. Candidate Deep Dives (≤5)

### 7.1 SMCI — B-tier stocks 71.26 ("low risk" per model) — **AVOID / MANUAL REVIEW (LEGAL OVERHANG)** ⚠️
- **Internal view:** B-tier intraday long, RS vs SPY +73.90% (highest in the book), regime-aligned, model risk penalty only **−4.0** → the system sees a clean momentum long. **No `news_items` rows for SMCI in the last 36 h** — the desk has zero internal visibility into the legal situation.
- **LEGAL / HEADLINE RISK (verified):**
  - **Mar 19, 2026** — SDNY unsealed a criminal indictment of three SMCI-associated individuals — **Yih-Shyan "Wally" Liaw (SVP Business Development & board member)**, Ruei-Tsang "Steven" Chang, and contractor Ting-Wei "Willy" Sun — for an alleged **export-control conspiracy** diverting **~$2.5B** of US AI-server technology to China (2024–2025). Per Supermicro's own IR statement, the **company itself is not a named defendant**; it placed two on leave and terminated the contractor (Supermicro IR, primary, verified via WebFetch).
  - **Oct 30, 2024** — **Ernst & Young resigned** as auditor, citing inability to rely on management/Audit-Committee representations.
  - **Active securities class action** (N.D. Cal.) against Super Micro and senior executives; class period **Feb 2, 2024 – Mar 19, 2026**; a new Hagens Berman complaint (May 12, 2026) alleges additional corrective disclosures; **lead-plaintiff deadline May 26, 2026** (Hagens Berman / PRNewswire, single_source).
- **Price-reaction / chase check:** TradingView / manual chart check unavailable. Entry zone 49.59–50.17, invalidation 48.43. The +73.9% RS is itself a *suspicious rally* given an unresolved legal/accounting overhang — exactly the SMCI-precedent pattern (clean technical score masking real legal risk).
- **Final verdict: AVOID — MANUAL REVIEW REQUIRED.** Never a clean actionable while the indictment + class action are live. The system's "low risk / −4.0" is the contradiction. `verification_status`: primary_source (indictment/IR) + single_source (class action).

### 7.2 AVGO (Broadcom) — C-tier 59.32, swing-blocked by earnings — **EVENT, NOT A TRADE TODAY**
- **Internal view:** demoted to C-tier with a −24.0 penalty; explicitly **swing-blocked by earnings**. The model is correctly defensive.
- **External (verified):** Broadcom reports **Q2 FY2026 today, Wed Jun 3, 2026, after market close** (call 2:00 PM PT); consensus **EPS ~$2.40 on ~$22.11B revenue (+47% YoY)**; semiconductor revenue guided ~$14.8B (+76% YoY) (MarketBeat / StockTitan / AlphaStreet, primary + single_source). No `news_items` rows internally — external confirms the date.
- **Price-reaction check:** binary event in hours; RR is dominated by the print, not the chart. Front-running is gambling on a number.
- **Final verdict: NO FRESH POSITION INTO THE PRINT.** Let the release set AI-semi direction (NVDA/AMD/SMH/SMCI), then trade the post-earnings structure. `verification_status`: primary_source (date) + single_source (estimates).

### 7.3 AAPL — B-tier stocks 79.64 (top score, new this cycle) — **WATCHLIST / PULLBACK-ENTRY ONLY**
- **Internal view:** highest stock score this run, confidence high, regime-aligned, RS vs SPY +8.07%, above prior-day high, **earnings-safe**, model risk "low." Status `waiting_for_entry`. The cleanest of the stock longs on the data.
- **External / legal check:** **no `news_items` for AAPL in 36 h** and no legal/headline flag surfaced in search — checked clean (no indictment/SEC/auditor/guidance issues). News-catalyst score is 0.00; this is a pure technical/trend setup.
- **Price-reaction / chase check:** TradingView unavailable. Entry zone 314.08–315.19, invalidation 311.85, TP1 318.53 (RR to TP1 only ~1.0 — below 1.5, the system's standing caveat). US cash closed until 16:30 EEST — not actionable now.
- **Final verdict: WATCHLIST — pullback-entry only at the US open, sized for the AVGO read-through.** Sub-1.5 RR caps it to opportunistic. `verification_status`: internal + clean external legal check.

### 7.4 AMD — B-tier stocks 78.45 (downgraded from A) — **WATCHLIST / NO CHASE**
- **Internal view:** B-tier (was A-tier 9 h ago), confidence high, **strongest RS in the book** (vs SPY +46.91%, vs sector +27.95%), above prior-day high, earnings-safe.
- **Contradiction risk:** stocks A-tier is the worst tier this week (**PF 0.27, 6% triggered winrate, n=43**); the downgrade to B slightly de-risks the "late A-tier entry" pattern, but AMD is the most-extended single name. Internal news benign (analyst/ETF chatter, imp ≤1.9); prior-run valuation context had AMD **above its ~$479.77 consensus 12-mo target** — extension is real.
- **Price-reaction / chase check:** entry zone 516.85–521.41, invalidation 507.72. Price sits at/near the top of its entry zone — **entry now would be late**; actionable only on a clean pullback into the lower zone with SPY/QQQ stable.
- **Final verdict: WATCHLIST ONLY / pullback-entry — do not chase.** `verification_status`: internal + single_source (valuation, prior-run).

### 7.5 BTC macro / crypto book — drives the entire crypto no-trade verdict
- **Internal view:** danger regime; BTC short rejected (>2 ATR from EMA20 / late breakdown), no long viable; best watchlist names are sub-threshold failed-bounce shorts (intraday BTC 63.3, ETH 58.5, DOGE 58.4; scalp ETH 59.0). Active tracked crypto B-tier signals (INJ intraday tp2_hit, ZEC/XLM swing) are winding on their own rules — **no adds**.
- **External (verified):** BTC ~**$65.3–67K**, **$1.86B liquidated in 24 h**, ETH <$1,900 with 16-day ETF outflow streak, MicroStrategy first BTC sale, Mt. Gox transfer; **$65K key support → $60K** on a break, relief only on a $70K reclaim (CryptoTimes / Bitcoin.com / CoinDesk / The Block, single_source ×4, corroborated).
- **Final verdict: NO TRADE.** Macro confirms the desk. Chasing breakdowns in elevated-vol with squeeze-prone funding is exactly what the gates block. `verification_status`: single_source ×4 (corroborated).

*Qualifying-but-not-deep-dived (5-candidate cap):* **SMH (78.56) / XLK (73.03) / QQQ (66.43)** B-tier stock longs — same bullish-but-event-gated thesis as AAPL/AMD, but each carries an **"earnings UNKNOWN"** undated-event flag (calendar lookup missing); treat as pullback-only watchlist with an unquantified event risk. **NVDA (66.95)** B-tier — follower RS, benign news, watchlist. Crypto `momentum_breakout` basket (GENIUS/ONDO/ENA) — fresh <1 h but single_source, no confirmed catalyst, rejected by the danger-regime gate.

---

## 8. Best Candidates Ranked

*(Internal + external alignment, in a tradeable sense.)*

1. **AVGO** — top *information* event (earnings today after close); highest read-through to the whole AI-semi book. No fresh pre-print position — trade the reaction.
2. **AAPL** — cleanest B-tier long on the data (top score, earnings-safe, clean legal check); pullback-entry only at the US open, sub-1.5 RR caps size.
3. **AMD / NVDA / SMH / XLK** — trend-aligned semi/tech longs; pullback-only, sized for the AVGO read-through. SMH/XLK carry undated-earnings risk.
4. *(crypto)* **none actionable** — best name is a sub-threshold BTC intraday short (63.3) in a danger regime.

If risk-tolerance is low: **no new positions at all** is fully defensible given the AVGO binary tonight + a deteriorating crypto tape.

---

## 9. Avoid / No Trade

- **SMCI (any direction)** — active criminal indictment of an SVP/board member + securities class action + auditor resignation; the model's "low-risk B-tier 71.26" is wrong. **AVOID / manual review.**
- **Fresh AVGO position into the print** — binary earnings event today (system swing-block agrees).
- **All fresh crypto entries** — danger regime, zero A/B, BTC ~$65–67K with $1.86B liquidations + 16-day ETH ETF outflows. Desk no-trade is correct.
- **Chasing AMD/SMH/NVDA >2 ATR from entry** — AMD above consensus target and at the top of its entry zone; stocks A-tier is the worst tier this week (PF 0.27).
- **Crypto failed-bounce shorts (ETH/DOGE/SOL/TAO)** — overextended, below-average volume, squeeze-prone funding; all sub-threshold watchlist.
- **Acting on the unmapped catalyst layer** — 81.2% unmapped this run; context only.
- **Carry-forward swing/invest** (~6.7 h) — usable but re-confirm at the 16:04 EEST refresh before any swing decision.

---

## 10. Main Risks

1. **SMCI integrity gap (system):** the scorer rates a stock with a live federal indictment + class action as a clean low-risk B-tier long, with **no internal news_items coverage** of the legal situation. The legal/headline layer is not wired into stock scoring — a recurring blind spot (the exact SMCI-precedent failure mode).
2. **AVGO earnings tonight** set the tone for NVDA/AMD/SMH/SMCI — a miss or soft AI-networking guide unwinds extended semi leadership fast.
3. **BTC contagion** — acceptance toward $65K (→ $60K) drags alt longs regardless of RS and can spill into high-beta semis; $1.86B of liquidations shows leverage being flushed.
4. **Extension risk** — AMD above consensus target; stocks A/B/C triggered winrates all low this week (A 6%, B 20%, C 19%).
5. **Catalyst mapping weak (81.2% unmapped)** — real catalysts may be under-surfaced; catalyst layer is context only.
6. **"Earnings UNKNOWN" on SMH/XLK/QQQ** — calendar lookup missing; undated event risk on any held position.
7. **Data blindspots** — no live social/on-chain/liquidation/ETF-flow feeds; Reddit social sources 403-failing; crypto crowd + leverage context thin.
8. **Carry-forward swing/invest** (~6.7 h) — re-confirm at 16:04 EEST.
9. **System integrity (clean):** `detect_untracked_legacy_alerts --since 2026-06-03` returned **None** — no untracked-alert regression. (Note: empty `data/crypto_ai_desk.db` at project root is a 0-byte decoy; the live DB is `db/crypto_ai_desk.sqlite` — no action needed.)

---

## 11. Action Plan — next 4 hours

- **SMCI:** flag for manual review; do **not** treat the B-tier score as actionable. If the desk intends any SMCI exposure, it must be a conscious decision made *with* the legal overhang in view, not the model's clean read.
- **Crypto:** no new trades. Watch BTC at **$65K** (break → $60K; reclaim of $70K = relief + squeeze setup). Let existing tracked B-tier signals (INJ/ZEC/XLM) run on their own rules — no adds.
- **Stocks (US closed until 16:30 EEST):** prep, don't act. Mark AAPL/AMD/NVDA/SMH/XLK pullback zones. **No fresh AVGO position before the after-close print.** Re-read the AVGO release tonight; let it set AI-semi direction.
- **Manual verification needed:** SMCI legal status (done this run — confirmed live); whether the Iran/Hormuz overlay from 9 h ago has genuinely faded or is just absent from the feed.
- **Next cycle:** the 16:04 EEST scheduler cycle refreshes crypto swing + stocks swing/invest — re-confirm carry-forward verdicts then.
- **No code, scoring, or threshold changes** (safety contract).

---

## 12. Final Verdict per Mode

- **Crypto scalp:** NO TRADE — danger regime; best name ETH 59.0 sub-threshold failed-bounce short. *(fresh)*
- **Crypto intraday:** NO TRADE — best name BTC 63.3, sub-threshold. *(fresh)*
- **Crypto swing:** NO fresh entry; existing ZEC/XLM/INJ signals winding on their rules. *(carry-forward ~6.7 h — re-confirm 16:04 EEST)*
- **Stocks intraday:** Bullish bias, long-only, but **AVOID SMCI (legal)** and **stand aside on AVGO into earnings**; AAPL/AMD/NVDA/SMH/XLK pullback-only at the open. *(fresh, weekday)*
- **Stocks swing:** Trend long-friendly (AAPL/SMH/AMD/XLK B-tier) but **carry-forward (~6.7 h)**, gated by tonight's AVGO print, and **SMCI excluded on legal risk** — re-confirm 16:04 EEST. *(carry-forward)*
- **Stocks invest:** Long-bias intact on AI-semi leadership but **carry-forward (~6.7 h)**; no fresh add ahead of AVGO; SMCI excluded. *(carry-forward)*
- **Overall:** **Crypto = risk-off / no-trade; Stocks = bullish-on-the-data but event-gated, with one hard AVOID (SMCI legal overhang the model is missing).** The two decisions that matter next 24 h: the **AVGO after-close print** and **not letting a clean-looking SMCI score pull capital into a live legal situation.** Patience over participation.

---

## 13. Sources

- [Super Micro Computer Issues Statement on Action by U.S. Attorney's Office — Supermicro IR, 2026-03-19](https://ir.supermicro.com/news/news-details/2026/Super-Micro-Computer-Issues-Statement-on-Action-by-U-S--Attorneys-Office/default.aspx) — SDNY indictment of 3 SMCI-associated individuals (export-control conspiracy, ~$2.5B servers to China); company not a named defendant; cooperating. *(primary_source, verified via WebFetch)*
- [Supermicro Provides Update on Investigation by Independent Board Directors — Supermicro IR, 2026](https://ir.supermicro.com/news/news-details/2026/Supermicro-Provides-Update-on-Investigation-by-Independent-Board-Directors/default.aspx) — independent board investigation context. *(primary_source)*
- [Hagens Berman Files New Securities Class Action Against SMCI and Its Senior Executives — PRNewswire, 2026-05-12](https://www.prnewswire.com/news-releases/hagens-berman-files-new-securities-class-action-against-super-micro-computer-smci-and-its-senior-executives-new-complaint-alleges-additional-corrective-disclosures-lead-plaintiff-filing-deadline-remains-may-26-2026-302780585.html) — active class action; class period Feb 2 2024 – Mar 19 2026; lead-plaintiff deadline May 26 2026; EY resignation (Oct 30 2024) referenced. *(single_source / securities-bar filing)*
- [INVESTOR NOTICE: SMCI Investors With Substantial Losses — Opportunity to Lead Class Action — PRNewswire, 2026](https://www.prnewswire.com/news-releases/investor-notice-super-micro-computer-inc-smci-investors-with-substantial-losses-have-opportunity-to-lead-investor-class-action-lawsuit-302753100.html) — corroborating class-action notice. *(single_source)*
- [Super Micro Computer, Inc. — Form 8-K (FY2026) — SEC EDGAR](https://www.sec.gov/Archives/edgar/data/0001375365/000137536526000011/a991.htm) — SMCI SEC filing reference. *(primary_source)*
- [AVGO Q2 2026 Earnings Report on 6/3/2026 — MarketBeat](https://www.marketbeat.com/earnings/reports/2026-6-3-broadcom-inc-stock/) — earnings date today after close. *(single_source)*
- [Broadcom Q2 FY2026 results set for June 3 — StockTitan](https://www.stocktitan.net/news/AVGO/broadcom-inc-to-announce-second-quarter-fiscal-year-2026-financial-04if2lwax8o1.html) — earnings date/time confirmation. *(primary_source)*
- [Broadcom (AVGO) Q2 2026 Preview: EPS Est. $2.40, Reports June 3 — AlphaStreet](https://news.alphastreet.com/broadcom-avgo-q2-2026-preview-eps-est-2-40-reports-june-3/amp/) — consensus EPS $2.40 / rev ~$22.11B / +47% YoY. *(single_source)*
- [Bitcoin Price Drops Below $66,000 While Massive Selloff Leads $1.86B in Liquidations — CryptoTimes, 2026-06-03](https://www.cryptotimes.io/2026/06/03/bitcoin-price-drops-below-66000-while-massive-selloff-leads-1-86b-in-liquidations/) — BTC <$66K, $1.86B liquidations. *(single_source, verified via WebSearch)*
- [Bitcoin Falls to $65,710 as Record ETF Outflows and Strategy Sale Rattle Market — Bitcoin.com, 2026-06-03](https://news.bitcoin.com/bitcoin-falls-under-66000-etf-outflows-strategy-sale/) — BTC ~$65.7K, ETF outflows, MicroStrategy sale. *(single_source)*
- [Bullish crypto bets lose $1.6 billion as ETH, SOL, DOGE drop 9% — CoinDesk, 2026-06-03](https://www.coindesk.com/markets/2026/06/03/bullish-crypto-bets-lose-usd1-6-billion-as-eth-sol-doge-drop-9) — ETH/SOL/DOGE −9%, long liquidations. *(single_source)*
- [Bitcoin briefly dips below $66,000 as ETF outflows, geopolitical fears weigh on crypto — The Block, 2026-06-03](https://www.theblock.co/post/403454/bitcoin-dips-below-66000) — BTC <$66K, ETF outflows / geopolitical context. *(single_source)*

_Internal CLI evidence (no external citation needed): active-signals (crypto 4 / stocks 20 rows; no A-tier this run; top stock B = AAPL 79.64); signal-stats (crypto n=23 weak, PF 3.25; stocks n=663 reliable, A-tier PF 0.27 / 6% winrate, B 20% / C 19%); detect_untracked_legacy_alerts (None); catalyst coverage 187/993 mapped (81.2% unmapped), 3 baskets; news_items queries (SMCI/AAPL/SMH/AVGO = none in 36 h; AMD/NVDA benign)._

---

## 14. Source-Discipline Final Checklist

- [x] Every external claim has source + title + date + URL (§13).
- [x] No uncited stats (BTC price, liquidations, ETF outflows, AVGO estimates, SMCI figures all sourced).
- [x] No uncited legal claims — SMCI indictment/class action/EY resignation all cited to primary IR + securities filings.
- [x] No fabricated TradingView observations — chart tools unavailable, stated explicitly.
- [x] Missing-source items written as "checked clean / unconfirmed," not guessed (AAPL legal clean; Iran overlay marked latent/unconfirmed).
- [x] test_source / fixture URLs filtered (catalyst scan reported 0 test_source rejects).
- [x] §13 Sources present with markdown hyperlinks + dates.
- [x] Web available — no "external unavailable" banner needed.

---
*Auto-generated by the `opus-enriched-review-4h` scheduled task. Read-only/advisory: no trades placed, no execution, no scoring/threshold/strategy code modified, no paid APIs added. Chart tooling not loaded — no chart observations fabricated.*
