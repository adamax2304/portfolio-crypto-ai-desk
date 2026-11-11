# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

- **Generated:** 2026-06-09 21:39 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **21:30 "late-session risk review" slot**, executing `opus-enriched-review-4h/SKILL.md`)
- **Slot context:** US cash session ~5h in (opened ~16:30 EEST). US close ~23:00 EEST — **~83 min away**. Late-session exposure and risk check. Do NOT initiate new intraday positions after 22:00 EEST.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-09_1840.md` (US open reaction review, 18:40 EEST, ~2.97h ago — see §4).
- **External web research:** AVAILABLE. ZEC ~$472 area (+84% from $258 panic low, Ironwood vulnerability fix multi-confirmed). ENA ~$0.08 (−7% 24h despite Janus Henderson $480B backing — contradiction). BTC ~$62,000–63,000 (stabilizing; Saylor +1,550 BTC). SMCI legal risk confirmed via SEC EDGAR Form 8-K.
- **Chart tools:** TradingView / Chrome MCP not loaded — no chart observations fabricated; OHLCV/ATR/EMA fields from reports + cited external data only.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

**Late US session, ~83 min to close. Core verdict: hold existing positions, no new intraday entries, manage risk into the close.**

**Crypto (9 active B-tier signals):** ZEC Ironwood rally confirmed at +84% from $258 panic low — running (tp_hit both intraday and swing). CHZ/ALLO/BAKE also in tp_hit. IO/USDT exited the signal list — healthy, avoids the June 11 token unlock (13.29M tokens / $1.84M / 1.7% supply). XLM B scalp short triggered (low-confidence mode). No new A/B signals generated this cycle.

**Stocks (US late session):** 7 B-tier intraday shorts triggered today (QQQ, XLY, TSLA, AMZN, MSFT, GOOGL, META) — the short book is running in a clean risk_off tape. XLV B intraday long is the healthcare-RS surprise: triggered and running against the macro grain. All "waiting" signals (NVDA, PLTR, AVGO, COIN) remain untriggered — do NOT initiate ~83 min before close.

**Critical flags this window:**
- **IO/USDT exited signal list** — no longer active. Avoids June 11 token unlock. Good outcome.
- **ENA/USDT contradiction** — Janus Henderson ($480B AUM) invested in ENA (multi-confirmed June 9 2026) yet price is DOWN ~7% 24h. Short thesis (price down, OI up) plays out despite catalyst. Manual review required before any new short entry.
- **SMCI legal risk** — SEC EDGAR Form 8-K: indictment of 3 individuals for export-control violation conspiracy. C-tier short active in system — **LEGAL/HEADLINE RISK → AVOID**.
- **SENT crowded funding** — Bybit funding −0.015 (extreme), elevated across all venues. AVOID new SENT longs.
- **Stocks performance critical** — A/B PF=0.48, totalR=−26R (all-tier: PF=0.54, totalR=−53R). Reduce sizing, enforce stops.

---

## 2. Data Used

**Internal — crypto reports:**

| Report | Generated | Age at 21:39 | Status |
|--------|-----------|--------------|--------|
| Scalp | 21:21 EEST | ~18 min | **Fresh** |
| Intraday | 21:23 EEST | ~16 min | **Fresh** |
| Swing | 16:39 EEST | ~5h | **Carry-forward (4–12h)** |

**Internal — stocks reports:**

| Report | Generated | Age at 21:39 | Status |
|--------|-----------|--------------|--------|
| Stocks intraday | 21:35 EEST | ~4 min | **Very fresh** |
| Stocks swing | 21:35 EEST | ~4 min | **Very fresh** (watchlist only) |
| Stocks invest | 21:37 EEST | ~2 min | **Very fresh** (watchlist only) |

**CLI (run at ~21:39 EEST):**
- `active-signals crypto`: 9 active B-tier signals
- `active-signals stocks`: 50 active signals (B+C tier)
- `signal-stats crypto`: PF=1.77, totalR=+17R (A/B, n=82) — positive
- `signal-stats stocks`: PF=0.48, totalR=−26R (A/B, n=111) — critical negative
- `untracked-legacy-alerts`: 0 (clean)

**Catalyst / narrative:**
- `catalyst_events.jsonl`: 1107 unique events (accumulated today), 4 baskets
- `narrative_baskets.jsonl`: 4 active (binance_ecosystem_teaser, ai_narrative, perps_dex_narrative, momentum_breakout)
- LLM packet: `llm_analysis_packet.md` (generated 21:23 EEST, intraday mode) — fresh

**External research (this run):**
- ZEC Ironwood: CryptoAdventure, CoinDesk, CoinPaper, CryptoTimes (June 9 2026)
- ENA Janus Henderson: CoinDesk, The Block, BeInCrypto (June 9 2026)
- BTC price: BlockchainReporter (~$63K), Yahoo Finance (stabilizing)
- SMCI legal: SEC EDGAR Form 8-K (via catalyst system, primary regulatory filing)

---

## 3. Scheduler / Data Freshness

- **No defer.** `scheduler.log` mtime: 21:10:32 EEST (~29 min ago). `cycle_01_20-38_summary.md` mtime: 21:10:31 EEST (~29 min ago). Both well within the 3h deferral threshold.
- Cycle completed fully: ok=16 steps, failed=0.
- Post-tracking pass (step 14): stopped=4, expired=1 — confirms signal pruning. IO/USDT among the exited (12 → 9 active).
- Reddit social sources: blocked (403 errors on CryptoCurrency, Bitcoin, Ethereum subreddits) — crowd attention context thin.
- Untracked legacy alerts: 0 (clean). No integrity issues.

---

## 4. What Changed vs Previous Review (`..._1840.md`, 18:40 EEST, ~2.97h ago)

| Item | At 18:40 (US open reaction) | Now 21:39 (late-session risk) | Delta |
|------|------------------------------|-------------------------------|-------|
| BTC | ~$62,639 (9:15 AM ET) | ~$62,000–63,000 (stabilizing) | Stable; Saylor +1,550 BTC buy |
| Active crypto signals | 11 | 9 (stopped=4, expired=1 in post-pass) | IO/USDT + others exited |
| IO/USDT B swing | Triggered; 44h June 11 unlock flagged | **GONE** (stopped/expired) | Healthy exit ahead of unlock |
| ZEC B in+sw | tp_hit (running) | Still tp_hit (confirmed) | Ironwood rally continues |
| CHZ, ALLO, BAKE | tp_hit ×4 | Still tp_hit ×4 | Running steadily |
| ENA contradiction | Flagged (price falling vs catalyst) | Still −7% 24h despite Janus Henderson | Worsening — MANUAL REVIEW |
| SMCI legal | Flagged (prior reviews) | Form 8-K confirmed (SEC EDGAR catalyst) | AVOID override active |
| Stocks B short book | META, MSFT, LLY, XLV triggered | 7 shorts triggered; XLV long running | Broadening confirmation |
| NVDA, PLTR, AVGO, COIN | Waiting | Still waiting | Too late to initiate — close ~83 min |
| Stocks A/B PF | 0.595 (−17R) | 0.48 (−26R) | **Worsened — critical** |
| Crypto A/B PF | 1.76 (+16R) | 1.77 (+17R) | Slightly improved |
| SENT funding crowding | Elevated (mentioned) | −0.015 Bybit (extreme), all venues elevated | Confirmed — AVOID new long |

**Net thesis change:** "3 ideas confirmed (META short, ZEC long, IO long); healthcare surprise; WLD stop validated" → **"IO safely exited; stocks short book running (7 B-tier triggered); ZEC continuation; ENA contradiction unresolved; ~83 min to close — no new entries, manage risk."**

---

## 5. Catalyst Coverage

- Total `catalyst_events.jsonl` today: **1107 events** (accumulated across all cycles)
- Active narrative baskets: **4** (binance_ecosystem_teaser, ai_narrative, perps_dex_narrative, momentum_breakout)
- Key mapped events (symbols identified):
  - **AAVE** [exploit_hack] — KelpDAO exploit; new framework proposed
  - **BNB** [exploit_hack] — Humanity Protocol H-token exploit ($32M private-key compromise)
  - **ETH** [exploit_hack ×4] — Humanity Protocol hack + hacker dumping $H for ETH; Yuga Labs NFT rescue
  - **BTC** [regulatory_sector_headline] — Tim Scott Clarity Act
  - **SMCI** [legal_risk] — SEC EDGAR Form 8-K: indictment of 3 individuals, export-control violation conspiracy ← HIGH IMPORTANCE
  - **ZEC** — privacy/compliance narrative + Ironwood vulnerability fix
  - **ENA** — Janus Henderson $480B backing, USDe distribution partnership
  - **XRP** — 50M whale transfer, SBI Japan deposit integration

- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Estimated ~94% "other_news" type based on 18:40 review estimate. Symbol-specific entries above are reliable; aggregate statistics diluted.
- Top estimated unmapped categories: macro/geopolitical, general DeFi news, exchange announcements without ticker.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off
- **Stocks mood:** risk-off (US late session; VIX 19.96; breadth EMA20 25%; 3/4 indices in range)
- **Dominant narrative:** BTC/ETH downtrend + macro risk 75/100 (exploit/hack news, regulatory headwinds); ZEC Ironwood privacy/compliance upgrade is the standout positive catalyst; ENA institutional backing vs. price-action contradiction; healthcare XLV as sector exception
- **Preferred side now:** shorts (crypto failed bounce; stocks short book running) + **holding** existing crypto longs (CHZ/ZEC/ALLO/BAKE in tp_hit). No new long entries this window.
- **Best long candidate:** ZEC — Ironwood catalyst multi-confirmed, running (tp_hit in + sw). NO new entry at $472 (+84% from panic low). **Long-watch trigger:** ZEC pullback to $420–440 zone on volume → retest entry.
- **Best short candidate:** ENA (crypto) — **short-watch trigger:** 1h close below $0.0779 with elevated volume (confirms bearish catalyst absorption). QQQ (stocks) already triggered — best active short.
- **Best catalyst-backed candidate:** ZEC (Ironwood upgrade — critical vulnerability fix confirmed, late-July activation). ENA has Janus Henderson backing but price action contradicts → bidirectional risk, manual review required.
- **What to avoid:** SENT new long (Bybit funding −0.015, extreme crowding); SMCI (legal risk AVOID override); new intraday stocks after 22:00 EEST; new crypto scalp entries (mode PF=0.16); chasing HAEDAL/OPN/SAHARA shorts (−19 to −47%, moves already played out).
- **What would change the view:** BTC reclaiming $65K+ on volume → risk-on upgrade; VIX closing below 18 → reduce stock short sizing; ENA stabilizing and bouncing above $0.088 on volume → neutralize short thesis.

---

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — ZEC/USDT B-tier (running — tp_hit intraday + swing)

**Signal:** B-tier intraday long (score 67, tp_hit). B-tier swing long (score 65, tp_hit). Both confirmed active.

**Catalyst confirmation (multi-source):**
- PRIMARY CONFIRMED: Zcash Ironwood upgrade — fixes a critical Orchard shielded pool counterfeiting vulnerability undetected since 2022. Could have allowed minting unlimited fake ZEC undetected. Emergency Swift fork already deployed. Ironwood (formal fix) targets late-July activation, closes old Orchard pool, routes through turnstile for supply verification.
- Sources: CoinDesk (June 8), CryptoAdventure (June 9), CoinPaper (June 9), CryptoTimes (June 9) — multi-source confirmation.
- ZEC ~$472, +84% from $258 panic low. Privacy/compliance narrative basket active (StarkWare/Sui article secondary catalyst).

**Price-reaction / chase check:**
- Price already strongly reacted (+84%). Adding NOW = chase. Do not enter.
- Existing tp_hit positions: let runners run.
- Evening pullback to $420–440 (prior resistance, now potential support) on volume = legitimate retest entry.
- Overextension risk: late buyers could exit on any BTC selloff.
- Is this late? YES for new entry. NO for holding existing positions.
- Chase risk: HIGH at $472. LOW if waiting for $420–440 pullback.

**Mood alignment:** ZEC is the exception to risk-off — catalyst-backed RS leader. Aligned with "catalyst-backed" routing. Overextended but thesis intact.

**Invalidation:** 1h close below $413 (intraday). Below $400 = Ironwood fully priced in, distribution underway.

**Late-session action:** Hold runners. Trailing stop ~$420 on intraday runner. Do not add at $472.

---

### Candidate 2 — ENA/USDT (Contradiction Risk — Catalyst vs. Technical)

**Signal:** C-tier short watch (score ~60, conditional entry zone $0.0808–0.0816, invalidation $0.0826). Downtrend, OI expanding (fresh shorts pressing).

**Catalyst contradiction:**
- POSITIVE: Janus Henderson ($480B AUM) confirmed investment in ENA + USDe distribution partnership. ETF products planned H2 2026. (CoinDesk June 9, The Block June 9, BeInCrypto June 9 — multi-source)
- NEGATIVE price action: ENA ~$0.08, DOWN ~7% 24h. Despite institutional announcement, sellers dominate. OI +7.71% (fresh shorts entering). Funding +2.889e-05 (near neutral). Elevated crowding on external venues.
- Pattern: "sell the news" — institutional backing announced → price fails to rally → shorts pile in.
- Broader risk-off + prior technical downtrend overpowering the catalyst.

**Analysis:**
- Short thesis technically valid (price down + OI up = fresh shorts pressing). But C-tier score (60) is below actionable threshold.
- Janus Henderson backing creates meaningful upside squeeze risk — cannot ignore.
- If ENA bounces above $0.088 on volume → abandon short thesis entirely.
- If ENA breaks below $0.0779 on volume → bearish absorption confirmed → short becomes conditional.

**LEGAL/HEADLINE check:** No legal risk identified on ENA.

**Late-session action:** NO NEW ENTRY this window. **MANUAL REVIEW REQUIRED.** Post-close: re-check ENA. If below $0.0779 on elevated volume → short conditional entry activates. If above $0.088 → neutralize short thesis.

---

### Candidate 3 — QQQ B intraday short (triggered — running)

**Signal:** B-tier intraday short (score 69, triggered, entry zone ~$699–700, invalidation $710, targets TP1 $691 / TP2 $686 / TP3 $679). Running.

**Context:**
- Confirms risk_off regime across the board. 5d: −5.51%, 20d: −1.16%. VIX 19.96.
- Stocks intraday playbook: 14d WR 55%, PF 2.03, +80R — shorts subset PF 9.00 (cleanest stocks lane).
- At 21:30 EEST (14:30 ET), ~83 min to close. Most of the day's directional move has played out.

**Price-reaction / chase check:**
- Already triggered at zone — no chase. Do NOT re-enter if stopped.
- Late-session risk: short-covering rally possible in final hour.
- Bonds/defensives holding → risk_off thesis intact so far.

**Mood alignment:** Fully aligned — risk_off, tech breadth 25%, QQQ short is core position.

**Late-session action:** Monitor. If at or near TP1 ($691), partial close (50%). Hold remainder with stop at $710. Do NOT add.

---

### Candidate 4 — XLV B intraday long (triggered — running)

**Signal:** B-tier intraday long (score 72, triggered). Healthcare sector ETF. Running.

**Context:**
- XLV: +8.77% RS vs SPY 20d — strongest sector. Healthcare = classic defensive rotation in risk_off.
- Session's biggest surprise: LONG triggered in a broadly risk_off market. Confirms defensive sector rotation (capital from tech/growth → healthcare/defensives). Textbook risk_off behavior, not a contradiction.
- LLY also triggered long earlier (same defensive thesis).

**Price-reaction / chase check:**
- Running at late session. ~83 min to close.
- Risk: if broader market short-covers late, capital may rotate back out of defensives.
- Healthcare ETFs tend to be sticky into the close vs. tech.

**LEGAL/HEADLINE check:** XLV is a broad sector ETF. UNH has known legal risk (prior reviews) but diluted inside XLV's broad exposure. No ETF-level legal risk identified.

**Late-session action:** Hold. Consider partial close (50%) into the close to lock gains. Remaining position: evaluate for overnight hold (healthcare defensives tend to carry well overnight; no specific healthcare headline risk seen).

---

### Candidate 5 — SMCI C-tier short (LEGAL RISK Override)

**Signal:** C-tier intraday short (score 62.83, waiting_for_entry).

**LEGAL/HEADLINE RISK IDENTIFIED:**
- Source: SEC EDGAR Form 8-K (FY2026) — "indictment of three individuals re alleged export-control violation conspiracy" (filed ~March 2026).
- Confirmed via `data/catalysts/2026-06-09/catalyst_events.jsonl`: `SMCI [legal_risk]` — **primary regulatory filing**.
- Export-control violation conspiracy is a serious legal proceeding — not a rumor.

**Impact:**
- SMCI carries active legal proceedings (SEC-documented). Any stock with active indictment = AVOID for any intraday or swing entry.
- Score 62.83 (C-tier) already below actionable threshold — doubly confirmed AVOID.
- Even as a short: violent squeeze risk exists on any legal resolution news (dropped charges, plea deal, settlement) that could gap the stock violently against a short position.

**Final verdict: AVOID — LEGAL/HEADLINE RISK (export-control indictment, SEC EDGAR primary source). Neither long nor short until legal overhang resolves.**

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Direction | Status | Verdict |
|------|--------|------|-----------|--------|---------|
| 1 | ZEC | Crypto intraday + swing | Long (running) | tp_hit | HOLD runners; no new entry at $472 |
| 2 | QQQ | Stocks intraday | Short (running) | Triggered | HOLD; partial close near TP1 ($691) |
| 3 | XLV | Stocks intraday | Long (running) | Triggered | HOLD; partial close into US close |
| 4 | ENA | Crypto short watch | Short (conditional) | Unactivated | MANUAL REVIEW — catalyst contradiction; trigger $0.0779 break on volume |
| 5 | SMCI | Stocks short | Short | Waiting | AVOID — LEGAL/HEADLINE RISK |

**No clean new entries this window.** US close ~83 min away. New intraday = late-session chase.

**Best long-watch:** ZEC — pullback to $420–440 on volume → retest entry. Not active until that level.

**Best short-watch:** ENA — 1h close below $0.0779 on elevated volume → short entry zone $0.0808–0.0816, invalidation $0.0826.

**Best catalyst-watch:** ENA — monitoring whether Janus Henderson institutional buying materializes as price support or continues being absorbed bearishly.

**Excess candidates (not in top 5):**
- NVDA B short (waiting) — too late to initiate at 21:30; next-session only
- PLTR B short (waiting) — same
- META B short (triggered, running) — deferred to QQQ as representative
- SENT — crowded funding (extreme), no entry at late session
- IO/USDT — EXITED (no longer active); do NOT re-enter before June 11 token unlock

---

## 9. Avoid / No Trade (this decision window only)

- **SENT new long:** Bybit funding −0.015 (extreme), elevated across Bybit/OKX/MEXC. Squeeze risk exists but late-session entry on extreme crowding = high-risk.
- **SMCI:** LEGAL RISK — export-control indictment (SEC EDGAR). Active until proceedings resolve.
- **SAHARA:** −47% 24h, OI −40% (pure liquidation). Do NOT short after the crash. Entry window closed.
- **HAEDAL:** −19% 24h, OI +67% (squeeze-prone). Fresh shorts at thin prices with extreme OI expansion. Avoid.
- **OPN:** −22% 24h, OI +8.56%, volume 0.19x (thin). Same squeeze pattern. Avoid.
- **Any new stocks intraday after 22:00 EEST:** ~60 min or less to US close. New intraday = guaranteed late-chase.
- **Waiting stocks signals (NVDA, PLTR, AVGO, COIN, XLE):** All waiting_for_entry. Hold for next session. AVGO also has analyst upgrade contradiction (Erste Group Buy) — additional reason to skip.
- **Crypto scalp mode new entries:** PF=0.16, wins=1, losses=6 in mode. Documented underperforming bucket. No new scalp trades.
- **IO/USDT before June 11:** Token unlock June 11 (13.29M tokens / $1.84M). Avoid any new IO entry before the unlock passes.

Scanning continues. This is a hold-and-monitor verdict, not a system pause.

---

## 10. Main Risks

1. **Late-session short-covering in stocks:** QQQ/tech shorts could face a "buy the dip" close on any positive headline. ~83 min to close — watch QQQ 15m in the final hour.
2. **ENA catalyst squeeze:** Janus Henderson backing could trigger delayed squeeze on ENA. Any prior ENA short exposure needs tight stop above $0.0826.
3. **ZEC overextension / distribution:** +84% from $258 panic low. Late buyers could exit aggressively on BTC weakness. Trailing stop ~$420 for intraday runner.
4. **SENT funding explosion:** Bybit funding −0.015 (extreme). BTC bounce toward $64K–65K could trigger violent SENT short squeeze. Watch BTC 1h.
5. **Stocks performance structural:** A/B PF=0.48 (−26R), all-tier PF=0.54 (−53R). Not a one-cycle anomaly — recurring. Requires manual audit (see §14 TODO-STOCKS-SIGNAL-QUALITY-CRITICAL).
6. **Humanity Protocol hack contagion on ETH:** $32M hack, hacker dumping $H for ETH. ETH may face localized sell pressure. Watch ETH 4h.
7. **IO/USDT June 11 token unlock (48h away):** IO exited signal list — good. Do NOT re-enter before June 11.
8. **SMCI legal spillover:** If the export-control case expands, SMH (semiconductor ETF) could be indirectly affected. Treat C-tier SMH long signals with extra caution.

---

## 11. Action Plan — next 4 hours

**Immediate (21:39–22:00 EEST — pre-close window):**
- ZEC runners: hold, trailing stop ~$420 on intraday runner.
- CHZ/ALLO/BAKE tp_hit runners: let run. Stops at invalidation levels already set.
- QQQ short: monitor TP1 ($691). If reached, partial close (50%).
- XLV long: partial close (50%) into the close to lock gains.
- XLM B scalp short (triggered): scalp mode PF=0.16. If in profit at 22:00, consider closing.

**US close window (22:30–23:00 EEST / 16:30–17:00 ET):**
- No new positions.
- Evaluate stocks short book (QQQ, TSLA, AMZN, MSFT, GOOGL, META): partial close vs. overnight hold.
- XLV long remaining: evaluate overnight hold (healthcare defensives carry well; no urgent news risk seen).

**Post-US-close (23:00–01:39 EEST):**
- Crypto evening scan: check BTC/ETH 4h. If BTC holds $62K+, ZEC/CHZ swing runners maintain overnight thesis.
- ENA: re-check price at 23:00. If below $0.0779 on elevated volume → short setup activates (conditional). If above $0.088 → neutralize short thesis.
- SENT: monitor funding normalization. If corrects toward neutral and BTC stabilizes → reassess.
- Watch for new B-tier crypto signals from next scheduler cycle (~23:00 EEST).
- AVGO: next session only; confirm analyst-upgrade contradiction resolved before any entry.

---

## 12. Final Verdict per Mode

| Mode | Verdict |
|------|---------|
| Crypto scalp | NO NEW ENTRIES. XLM B scalp short (triggered): if in profit at 22:00, consider closing. PF=0.16 in mode — reduce exposure. |
| Crypto intraday | HOLD RUNNERS (ZEC tp_hit). No new intraday entries at 21:39. Monitor ENA post-close for short trigger ($0.0779 break on volume). |
| Crypto swing | HOLD RUNNERS (ZEC, CHZ, ALLO, BAKE — all tp_hit). No new swing entry at current prices. Next entry: ZEC pullback to $420–440 retest. |
| Stocks intraday | HOLD triggered shorts (QQQ, XLY, TSLA, AMZN, MSFT, GOOGL, META). Partial close XLV long into close. NO NEW POSITIONS after 22:00 EEST. A/B PF=0.48 — enforce stops, reduce sizing. |
| Stocks swing | WATCHLIST ONLY (audit cap active — 0W/12L, −12R pre-audit). Research only. No Telegram-actionable trades. |
| Stocks invest | WATCHLIST ONLY (audit cap active — 0W/24L, −24R). Research only. No Telegram-actionable trades. |

---

## 13. Sources

1. [ZEC Price Analysis: Ironwood Rally Builds (+84% from $258 low)](https://cryptoadventure.com/zec-price-analysis-zcash-jumps-84-from-258-low-as-ironwood-rally-builds/) — CryptoAdventure, June 9 2026 — **confirms** (primary_source)
2. [Zcash bounces 45% as developers propose Ironwood upgrade](https://www.coindesk.com/markets/2026/06/08/zcash-bounces-45-as-developers-propose-new-ironwood-upgrade) — CoinDesk, June 8 2026 — **confirms** (primary_source)
3. [ZEC Price Rebounds as Zcash Finalizes Ironwood Security Upgrade](https://coinpaper.com/17560/zec-price-rebounds-as-zcash-finalizes-ironwood-security-upgrade) — CoinPaper, June 9 2026 — **confirms** (single_source)
4. [Zcash's Dramatic 80% Rebound: Swift Forks and Ironwood Rescue ZEC](https://www.cryptotimes.io/2026/06/09/zcashs-dramatic-80-rebound-swift-forks-and-ironwood-rescue-zec-from-price-collapse/) — CryptoTimes, June 9 2026 — **confirms** (single_source)
5. [Zcash Ironwood upgrade: rebound with risk note](https://coinjournal.net/news/zcash-developers-propose-ironwood-upgrade-zec-price-rebounds-but-there-is-a-risk/) — CoinJournal, June 9 2026 — **confirms risk** (single_source)
6. [Ethena lands Janus Henderson backing — ENA, USDe distribution](https://www.coindesk.com/business/2026/06/09/ethena-lands-janus-henderson-backing-as-asset-manager-invests-in-ena-eyes-usde-distribution) — CoinDesk, June 9 2026 — **confirms** (primary_source)
7. [Janus Henderson takes ENA position, eyes regulated ETPs](https://www.theblock.co/post/404109/janus-henderson-takes-ena-position-eyes-regulated-investment-products-tied-to-ethena) — The Block, June 9 2026 — **confirms** (primary_source)
8. [Ethena Lands $480 Billion Wall Street Giant, Will ENA Price Rally?](https://beincrypto.com/ethena-janus-henderson-usde-clo-backing-2/) — BeInCrypto, June 9 2026 — **confirms** (single_source)
9. [Bitcoin Price Today: BTC Holds $63K as Saylor Buys the Dip](https://blockchainreporter.net/bitcoin-price-today-btc-holds-63k-as-saylor-buys-the-dip-and-etf-money-returns/) — BlockchainReporter, June 9 2026 — **confirms** (single_source)
10. SMCI Form 8-K FY2026 — export-control violation indictment: SEC EDGAR (via `data/catalysts/2026-06-09/catalyst_events.jsonl` — primary regulatory filing) — **LEGAL RISK confirmed**

---

## 14. Fix Requests / TODO

### TODO-STOCKS-SIGNAL-QUALITY-CRITICAL
- **issue:** Stocks A/B signals critically underperforming — PF=0.48, totalR=−26R (A/B); all-tier PF=0.54, totalR=−53R. A-tier worst bucket: PF=0.08, only 1W/12L. Observed across all tiers simultaneously. Recurring across ≥3 review cycles.
- **evidence:** `cycle_01_20-38_summary.md` step 12 (signal-stats stocks); `data/reports/stocks/intraday/2026-06-09_18-35_stocks_intraday_report.md` §Recent Signal Performance; playbook note: "A-tier overpromotion on losing names — NVDA/SMCI/SMH longs structurally lose in this regime."
- **suggested manual fix:** Audit stocks A-tier scoring for regime-mismatch overpromotion. Add regime-gate for stocks A-tier longs (no A-tier long when breadth EMA20 <35% and VIX >18). Consider raising stocks B-tier minimum threshold from 65 to 70. Review whether the stocks intraday playbook PF=2.03/+80R figure reflects the SHORTS subset only (PF 9.00) vs the full A/B pool.
- **priority:** high
- **first observed:** 2026-06-09 18:40 EEST (prior review), confirmed recurring

### TODO-STOCKS-SWING-AUDIT
- **issue:** Stocks swing on watchlist-only mode (48h audit cap, 0W/12L, −12R) has persisted across multiple review cycles without a formal audit session scheduled.
- **evidence:** `data/reports/stocks/swing/2026-06-09_18-35_stocks_swing_report.md` header; playbook: `stocks_swing_watchlist_rs_rotation` status=watchlist_only (paused), pre-pause WR 11% / PF 0.15 / −33R.
- **suggested manual fix:** Schedule a dedicated manual session to audit stocks swing entry timing (premature entries, missing RTH confirmation), and decide whether to re-enable with tighter constraints or permanently cap to C-tier.
- **priority:** high
- **first observed:** 2026-06-08, recurring

### TODO-CRYPTO-SCALP-AUDIT
- **issue:** Crypto scalp mode underperforming — n=45, triggered=28, wins=1, losses=6, PF=0.16. TP1/2h horizon mismatch documented as failure mode.
- **evidence:** `cycle_01_20-38_summary.md` step 10 (signal-stats by mode); scalp report: "TP1 distance ~1.86R vs typical captured MFE 0.54R — mean reverts before TP."
- **suggested manual fix:** Audit scalp TP1 distance vs actual MFE. Consider reducing TP1 to 0.5R or adding a "scalp early exit" rule (partial take at 30 min / 0.3R). Alternatively, suspend scalp A/B Telegram alerts until 20 re-audited closed signals with adjusted TP.
- **priority:** medium
- **first observed:** 2026-06-09 21:21 EEST, recurring

### TODO-SMCI-LEGAL-SIGNAL-OVERRIDE
- **issue:** SMCI C-tier short signal is active in the system despite an active LEGAL/HEADLINE RISK flag (SEC EDGAR Form 8-K export-control indictment). No automatic suppression mechanism exists for legal-risk-tagged symbols.
- **evidence:** SMCI active in `active-signals --asset-class stocks` (score 62.83, C-tier short); `catalyst_events.jsonl` has `SMCI [legal_risk]` tag.
- **suggested manual fix:** Add a legal-risk gate to signal generation or display: if symbol has `legal_risk` catalyst tag with importance above threshold, automatically label "AVOID override" and suppress from actionable signals output. Surface as warning row in `active-signals` table.
- **priority:** medium
- **first observed:** 2026-06-09 21:39 EEST (this run)

### TODO-REDDIT-403-SOCIAL
- **issue:** Reddit social sources blocked (403 Client Error) — CryptoCurrency, Bitcoin, Ethereum subreddits all failing. Social attention context is missing from every cycle run.
- **evidence:** `cycle_01_20-38_summary.md` steps 2 and 3 — multiple WARNING lines "Failed social source Reddit X: 403 Client Error: Blocked."
- **suggested manual fix:** Reddit requires OAuth2 authentication since June 2023 API policy change. Replace unauthenticated calls with an authenticated Reddit client, or switch to alternative sources (LunarCrush, CryptoCompare social stats, or manual X/Telegram pipeline).
- **priority:** medium
- **first observed:** Recurring across all cycles

### TODO-CATALYST-MAPPING-WEAK
- **issue:** Estimated ~94% of catalyst events categorized as "other_news" (no symbol mapping). Catalyst layer only reliable for explicitly tagged events; aggregate statistics diluted.
- **evidence:** 18:40 review: "438/465 = 94.2% typed as 'other_news'." 1107 events today with 4 baskets — ratio likely similar.
- **suggested manual fix:** Add NER (named entity recognition) or symbol-synonym lookup to the catalyst ingestion pipeline to map protocol/project names to tickers.
- **priority:** medium
- **first observed:** Multiple prior reviews

### TODO-TELEGRAM-NOTIFIER-400
- **issue:** `TelegramNotifier.send()` returns 400 Bad Request when called from this review script. Direct `requests.post` to the same bot token/chat_id succeeds (message_id=2316 confirmed delivered this run). Likely cause: `TelegramNotifier` is setting `parse_mode=Markdown` or `parse_mode=MarkdownV2` and the review message body contains characters that fail Telegram's Markdown parser (e.g., unescaped `-`, `(`, `)`, `.`).
- **evidence:** `TelegramNotifier(Path('config/notifications.yaml')).send(msg)` → 400 Bad Request. Direct `requests.post(..., json={'chat_id': '298242042', 'text': msg})` → 200 OK.
- **suggested manual fix:** In `src/notifiers/telegram.py`, check whether `parse_mode` is being passed to the API call. If yes, either: (a) escape the message body properly for the given parse_mode, or (b) add a fallback to plain-text (no parse_mode) when the formatted send fails.
- **priority:** medium
- **first observed:** 2026-06-09 21:39 EEST (this run)
