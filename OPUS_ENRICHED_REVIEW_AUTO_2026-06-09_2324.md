# Opus Enriched Review — post-close final daily review — Auto Cycle 23:24 EEST

- **Generated:** 2026-06-09 23:24 EEST (auto-enriched-review, scheduled task `opus-enriched-review-postclose`, **23:15 "post-close final daily review" slot**, executing `opus-enriched-review-4h/SKILL.md`)
- **Slot context:** US cash session closed (~23:00 EEST). Daily wrap — what worked, what failed, overnight-into-Asia crypto setup.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-09_2139.md` (late-session risk review, 21:39 EEST, ~1h45m ago — see §4).
- **External web research:** AVAILABLE. ZEC ~$480 (+80% from $258 panic low, Ironwood upgrade multi-confirmed). ENA ~$0.081–0.083 (−7% 24h despite Janus Henderson $480B backing — contradiction). BTC ~$62–64K (post-close consolidation). SMCI legal risk confirmed via SEC EDGAR Form 8-K (March 2026). US stocks: risk_off close confirmed.
- **Chart tools:** TradingView / Chrome MCP not loaded — no fabricated chart observations. OHLCV/ATR/EMA fields from internal reports + cited external sources only.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

**Post-close, 23:24 EEST. US session closed risk-off. Crypto stabilizing into Asia open.**

**Day verdict — controlled execution day.** The system executed cleanly on both sides:

**What worked today:**
- **Crypto long book: clean.** ZEC B intraday + B swing both tp_hit (Ironwood rally, +80% from $258 panic low to ~$480). CHZ B swing tp_hit (RS-leader, $0.0274 → $0.0282). ALLO B swing + B intraday tp_hit. BAKE B swing ×2 tp_hit.
- **Stocks short book: confirmed.** 8 B-tier shorts (PLTR, NVDA, TSLA, AMZN, MSFT, GOOGL, META, QQQ) triggered/running in clean risk_off tape. AVGO B short tp_hit. XLV B long and LLY B long triggered as healthcare RS exceptions.
- **IO/USDT: clean exit.** Exited ahead of June 11 token unlock (13.29M tokens / $1.84M / 1.7% supply). Good risk management.
- **Stocks PF recovered slightly:** −26R → −23R (A/B, week) into close.

**What failed / struggled:**
- No A-tier signals in crypto or stocks today.
- **ENA contradiction persists:** Janus Henderson ($480B AUM) invested in ENA token (confirmed), yet price is DOWN ~7%. Short thesis playing out but institutional catalyst creates unresolved contradiction.
- **Scalp mode structurally weak:** PF=0.14 (low-confidence), no A/B scalp signals.
- **SMCI AVOID override:** Export-control indictment (SEC EDGAR Form 8-K) confirms legal risk.

**Overnight/Asia setup (23:00 EEST onward):**
- BTC holding $62–64K range; no new A/B signals from latest cycle.
- Crypto regime: range/chop, BTC downtrend, altcoin breadth thin (47–50% EMA20).
- No new entries recommended. Monitor active signal stops if BTC breaks $62K.
- Humanity Protocol hacker confirmed selling $H for ETH — overnight ETH selling overhang.
- **Active crypto book: 8 signals — all tp_hit** (CHZ swing, ALLO swing+intraday, BAKE swing×2, ZEC intraday+swing, XLM swing).

---

## 2. Data Used

**Internal — crypto reports:**

| Report | Generated | Age at 23:24 | Status |
|--------|-----------|--------------|--------|
| Scalp | 23:21 EEST | ~3 min | **Very fresh** |
| Intraday | 21:23 EEST | ~2h | **Fresh** |
| Swing | 16:39 EEST | ~6.8h | **Carry-forward (4–12h)** |

**Internal — stocks reports:**

| Report | Generated | Age at 23:24 | Status |
|--------|-----------|--------------|--------|
| Stocks intraday | 22:44 EEST | ~0.7h | **Very fresh** |
| Stocks swing | 21:35 EEST | ~1.8h | **Fresh** (watchlist only) |
| Stocks invest | 21:37 EEST | ~1.8h | **Fresh** (watchlist only) |

**CLI (run at ~23:24 EEST):**
- `active-signals crypto`: **8 active B-tier signals** (all tp_hit)
- `active-signals stocks`: **50 active signals** (B+C tier mix)
- `signal-stats crypto`: PF=1.65, totalR=+15R (A/B, n=82) — positive
- `signal-stats stocks`: PF=0.54, totalR=−23R (A/B, n=111) — negative, improved from −26R at 21:39
- `detect_untracked_legacy_alerts`: **0 (clean)**

**Catalyst / narrative:**
- `catalyst_events.jsonl`: 1107 unique events (accumulated today), 4 baskets active
- `narrative_baskets.jsonl`: binance_ecosystem_teaser, ai_narrative, perps_dex_narrative, momentum_breakout
- Last cycle summary: `2026-06-09_default_schedule/cycle_01_20-38_summary.md` (21:10 EEST, 2h14m ago, ok=16/failed=0)

**External research (this run):**
- BTC price ~$62–64K: BlockchainReporter, Yahoo Finance (June 9 2026)
- ZEC Ironwood +80%: CryptoTimes, CoinPaper, CoinDesk (June 8–9 2026)
- ENA Janus Henderson contradiction: CoinDesk, The Block, BeInCrypto (June 9 2026)
- SMCI legal: SEC EDGAR Form 8-K (March 19 2026, primary_source)
- US market: Yahoo Finance QQQ range (June 9 2026)

---

## 3. Scheduler / Data Freshness

- **No defer.** Latest `cycle_01_20-38_summary.md` mtime: 21:10:31 EEST (~2h14m ago). Within 3h deferral threshold.
- `scheduler.log`: **not found** — non-blocking since cycle summary is fresh and within threshold. (See §14 TODO-scheduler-log-missing.)
- Cycle completed fully: **ok=16 steps, failed=0.**
- Pre-tracking pass: checked=329, updated=15, tp_hits=192.
- Post-tracking pass (step 14): **stopped=4, expired=1** — confirming signal pruning (12 → 8 active crypto signals).
- Reddit social sources: persistently blocked (403 errors) — crowd attention thin.
- Untracked legacy alerts: **0 (clean).** No integrity issues.
- Swing report: **carry-forward (6.8h)** — used for context only; CHZ B-tier swing thesis validated (price $0.0274 → $0.0282, tp_hit confirmed).

---

## 4. What Changed vs Previous Review (`2026-06-09_2139.md`, 21:39 EEST, ~1h45m ago)

| Item | At 21:39 (late-session risk) | Now 23:24 (post-close) | Delta |
|------|------------------------------|------------------------|-------|
| BTC | ~$62–63K stabilizing | ~$62–64K (post-close consolidation) | Stable |
| Active crypto signals | 9 | **8** (1 additional exit) | Pruning continues |
| ZEC B intraday+swing | tp_hit ×2 | tp_hit ×2 (confirmed) | Rally holds ~$480 |
| CHZ B swing | tp_hit | tp_hit | Running ($0.0274→$0.0282) |
| ALLO B swing+intraday | tp_hit ×2 | tp_hit ×2 | Running |
| BAKE B swing ×2 | tp_hit ×2 | tp_hit ×2 | Running |
| XLM B swing | tp_hit | tp_hit | Running |
| ENA contradiction | Price −7%, Janus Henderson confirmed | Still ~$0.081–0.083, down | Unresolved |
| SMCI legal | AVOID flagged | Form 8-K confirmed (March 2026) | AVOID confirmed |
| Stocks short book | 7 B-tier triggered | 8+ (AVGO tp_hit added); session closed | Short book ran cleanly |
| XLV B long | tp_hit | tp_hit | Healthcare RS confirmed |
| LLY B long | triggered | running into close | Running |
| Stocks A/B PF | 0.48 (−26R) | **0.54 (−23R)** | +3R recovered into close |
| Crypto A/B PF | 1.77 (+17R) | **1.65 (+15R)** | Minor dip (new stops/expirations) |
| IO/USDT | Exited (stopped/expired) | Not in active list | Clean exit pre-June 11 unlock ✓ |

**Net thesis change:** "no new entries ~83 min before close, manage risk" → **"US session closed: stock short book confirmed today. ZEC/CHZ/ALLO/BAKE crypto book performing. ENA contradiction unresolved — overnight watch. Asia setup: no new A/B signals; patience recommended."**

---

## 5. Catalyst Coverage

- Total `catalyst_events.jsonl` today: **1107 events** (accumulated across all cycles)
- Active narrative baskets: **4** (binance_ecosystem_teaser, ai_narrative, perps_dex_narrative, momentum_breakout)
- Latest cycle (catalyst_cycle_18-01.md) breakdown: other_news=475/500, partnership=6, exploit_hack=6, regulatory=4, product_launch=2, insider_activity=2, earnings_event=2, analyst_action=2.
- Key mapped catalyst events today:
  - **AAVE/USDT** [exploit_hack] — KelpDAO exploit, new governance framework proposed
  - **BNB/USDT** [exploit_hack] — Humanity Protocol H-token $32M private-key hack
  - **ETH/USDT** [exploit_hack ×4] — Humanity Protocol: hacker dumping $H for ETH; Yuga Labs NFT rescue
  - **BTC/USDT** [regulatory_sector_headline] — Tim Scott Clarity Act (longer-term BTC-positive)
  - **SMCI/USDT** [legal_risk] — SEC EDGAR Form 8-K: 3 individuals indicted, export-control violation conspiracy ← HIGH IMPORTANCE
  - **ENA/USDT** [partnership] — Janus Henderson $480B backing, USDe distribution + ETF plans (H2 2026)
  - **ZEC/USDT** — Ironwood upgrade consensus rules finalized; privacy/supply-integrity narrative
  - **PLTR/USDT** [partnership] — McCarthy Building multi-year AI deal (bullish catalyst; macro override)
  - **AVGO/USDT** [analyst_action] — Erste Group upgraded to Buy; Anthropic $35B expansion backed by Apollo/Blackstone

- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** ~95%+ events classified as `other_news`. Mapped symbol-specific entries above are reliable. Top 3 unmapped categories (estimated): general macro/geopolitical, DeFi/protocol news without ticker, exchange announcements.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** mixed/chop — BTC downtrend, ETH downtrend/range, altcoin breadth 47–50% EMA20. Individual RS-leader longs working (ZEC, CHZ) but regime does not support new longs without confirmation. Macro risk score 57/100.
- **Stocks mood:** risk_off (closed). Short-biased session confirmed: SPY 5d=−3.5%, QQQ 5d=−5.9%, VIX ~20.12. Healthcare (XLV) is the only RS exception for longs.
- **Dominant narrative:** Risk-off + exploit cluster. Humanity Protocol $32M hack creates ETH selling overhang overnight (hacker confirmed selling $H for ETH). BTC stabilizing at $62–64K. ZEC privacy/supply-integrity narrative intact (Ironwood).
- **Preferred side now:** Crypto — watch-for-trigger only. No clean new entries. Stocks — closed; plan for tomorrow.
- **Best long candidate:** CHZ/USDT — B swing already running (tp_hit). Pullback retest zone 0.0270–0.0273 is the trigger if Asia dips. Requires BTC holding $62K.
- **Best short candidate:** ENA/USDT — price falling despite institutional backing (Janus Henderson $480B confirmed). Fresh shorts building (OI +7.7%, price down). Short trigger: failed bounce retest 0.0815–0.0823. SL: 1h close above 0.0833.
- **Best catalyst-backed candidate:** ZEC/USDT — Ironwood upgrade multi-confirmed (CryptoTimes, CoinPaper, CoinDesk, Unchained). Both B signals tp_hit. Ironwood targets late July — thesis still intact.
- **What to avoid:** SMCI (legal risk, AVOID); SENT (extreme negative funding −0.015 Bybit, all venues); SAHARA (−45% 24h, OI collapsing); IO/USDT (June 11 token unlock); STG (high-risk flag despite RS).
- **What would change the view:** BTC loses $62K support → increase short bias, check all long stops immediately. BTC reclaims $65K+ → new RS-leader long setups viable.

---

## 7. Candidate Deep Dives

### Candidate 1 — ZEC/USDT (B tier, intraday + swing, long, tp_hit ×2)

**Internal:** catalyst_events.jsonl and narrative_baskets both have fresh ZEC Ironwood entries. System shows B intraday (67, tp_hit) and B swing (65, tp_hit). From swing report: current price $469.76, ATR $12.97, resistance $482.20.

**External research:**
- [CryptoTimes, June 9 2026](https://www.cryptotimes.io/2026/06/09/zcashs-dramatic-80-rebound-swift-forks-and-ironwood-rescue-zec-from-price-collapse/): +80% rebound from $258 to ~$480. Ironwood targets late July. `single_source` | **confirms**
- [CoinPaper, June 9 2026](https://coinpaper.com/17560/zec-price-rebounds-as-zcash-finalizes-ironwood-security-upgrade): Consensus rule changes finalized. Turnstile accounting restores supply verification. `single_source` | **confirms**
- [CoinDesk, June 8 2026](https://www.coindesk.com/markets/2026/06/08/zcash-bounces-45-as-developers-propose-new-ironwood-upgrade): Day-1 bounce +45%. `primary_source` | **confirms**

**Price-reaction / chase check:**
- Has price reacted to catalyst? Yes — massively. +80% from $258 panic low to ~$480 in ~3 days.
- Chasing? At current ~$480, entering new positions IS chasing. Do not add.
- Retest / pullback? Both active signals are in tp_hit status (entry zones already passed).
- Overextended? Yes — +80% in ~3 days. ATR ~$12.97. Price at resistance ($482.20 per swing report).
- Would entry NOW be late? Yes. Do not initiate new ZEC positions.
- Mood alignment? Yes — catalyst-backed, RS-leader, privacy narrative intact.
- Invalidation for active signals: intraday SL ~$454; swing SL ~$553.
- **Verdict: HOLD ACTIVE SIGNALS. No new entry.** Next watch: Ironwood July deployment, or consolidation retest to $440–460 zone.

---

### Candidate 2 — CHZ/USDT (B tier, swing, long, tp_hit)

**Internal:** B swing signal (65.9/100) from 16:39 EEST swing report. Price at 16:39: $0.0274; current (23:21): $0.0282 — tp_hit confirmed. RS vs BTC +10.95%, volume 1.09x, OI +17.42%, fresh positioning. No catalyst required (RS-leader playbook).

**Price-reaction / chase check:**
- Chasing at $0.0282? Entry zone was 0.0270–0.0273 — already passed. tp_hit.
- Retest structure? If Asia session dips to 0.0270–0.0273, viable re-entry with BTC confirmation.
- Aligned with mood? Yes — RS-leader long in neutral/chop market. Catalyst not required for this playbook.
- Invalidation: 1h close below 0.0266.
- **Verdict: HOLD ACTIVE SIGNAL. No new entry at $0.0282. Watch for Asia retest of 0.0270–0.0273.**

---

### Candidate 3 — ALLO/USDT (B tier, swing + intraday, long, tp_hit ×2)

**Internal:** B swing (65) and B intraday (66) both tp_hit. No external catalyst required — RS-leader continuation from earlier in the day.

- No legal flag. No catalyst contradiction.
- **Verdict: HOLD ACTIVE SIGNALS. No new entry. Monitor stops as part of overnight portfolio.**

---

### Candidate 4 — ENA/USDT (C watch — CATALYST CONTRADICTION, MANUAL REVIEW REQUIRED)

**Internal:** Intraday report: ENA C-tier (60.0), short bias (price down, OI up), catalyst_news=10.5 (fresh Janus Henderson attention). Short entry zone: 0.0815–0.0823. Invalidation: 1h close above 0.0833. Derivatives: fresh shorts pressing (OI +7.7%, L/S 1.539 — crowded long ratio).

**External research:**
- [CoinDesk, June 9 2026](https://www.coindesk.com/business/2026/06/09/ethena-lands-janus-henderson-backing-as-asset-manager-invests-in-ena-eyes-usde-distribution): Janus Henderson ($480B AUM) invested in ENA token + partnered for USDe distribution and ETF products. `primary_source` | **confirms catalyst** but price contradicts.
- [The Block, June 9 2026](https://www.theblock.co/post/404109/janus-henderson-takes-ena-position-eyes-regulated-investment-products-tied-to-ethena): Regulated ETFs/ETPs for USDe and ENA expected H2 2026. `primary_source` | **confirms**
- [BeInCrypto](https://beincrypto.com/ethena-janus-henderson-usde-clo-backing-2/): Price ~$0.08, down ~7% 24h despite $480B backing announcement. | **weakens long thesis**

**Contradiction analysis:**
- Strong bullish catalyst (confirmed institutional investment, ETF roadmap) vs. falling price + fresh shorts building.
- Possible explanations: news already priced in; ENA at $0.08 is far below 2024 high ($1.52) — macro distribution overrides news; broader crypto risk-off regime overrides individual catalyst.
- For short: failed-to-rally-on-good-news is a distribution signal. But ENA is already at ~$0.081 — NOT yet at the 0.0815–0.0823 failed-bounce zone (price needs to bounce first, then fail).
- For long: no confirmation, no floor established.
- **Verdict: MANUAL REVIEW REQUIRED.** Short trigger = failed bounce retest at 0.0815–0.0823 + price rejection. SL: 0.0833. Long trigger = stabilization above $0.09 with volume + buying interest. Neither is actionable NOW without trigger confirmation.

---

### Candidate 5 — SMCI (LEGAL/HEADLINE RISK → AVOID)

**LEGAL/HEADLINE RISK CONFIRMED:**
- Source: [SEC EDGAR Form 8-K, March 19 2026](https://www.sec.gov/Archives/edgar/data/0001375365/000137536526000011/smci-20260320.htm) — **primary_source**, Supermicro official filing.
- Three individuals indicted for export-control violation conspiracy: Yih-Shyan "Wally" Liaw (SVP/Board — resigned), Ruei-Tsang Chang (Taiwan sales manager), Ting-Wei Sun (contractor — terminated).
- Supermicro not named as defendant, but reputational/regulatory overhang is material. Prior SEC probes and accounting scandals on record.
- Stocks intraday: SMCI C-tier short (62.83, status=waiting). Stocks invest: SMCI long rejected.

**Verdict: LEGAL/HEADLINE RISK → AVOID.** Do not initiate new positions (neither long nor short). Active C-tier short signal should be flagged for manual cancellation (see §14 TODO-smci-active-signal-cancel).

---

## 8. Best Candidates Ranked

No new clean A/B candidates for entry this window. US session closed; no fresh A/B crypto signals from latest cycle.

**Running positions (do not add new entries):**

| Rank | Symbol | Mode | Status | Note |
|------|--------|------|--------|------|
| 1 | ZEC/USDT | B intraday + swing | tp_hit ×2 | Ironwood catalyst confirmed; +80% from $258. No new entry. |
| 2 | CHZ/USDT | B swing | tp_hit | RS-leader $0.0282. Watch 0.0270–0.0273 retest in Asia. |
| 3 | ALLO/USDT | B swing + intraday | tp_hit ×2 | Running. No new entry. |

**Watch — no clean new trade this window:**

- **long-watch CHZ/USDT:** trigger = Asia retest of 0.0270–0.0273 + BTC holds above $62K + price accepts in zone (no chase)
- **short-watch ENA/USDT:** trigger = failed bounce retest at 0.0815–0.0823 + price rejection confirmation. SL: 1h close above 0.0833. Do not enter before trigger.
- **catalyst-watch ZEC/USDT:** trigger = Ironwood July deployment news, or meaningful consolidation retest to $440–460 range

---

## 9. Avoid / No Trade

**This window (post-close, overnight into Asia):**

- **SMCI** — LEGAL/HEADLINE RISK (export-control indictment, SEC EDGAR primary source). **AVOID.**
- **UNH** — DOJ antitrust probe active (reported QuiverQuant / Yahoo Finance, June 9 2026; listed in swing report catalyst section). C-tier long in system — **MANUAL REVIEW REQUIRED** before any entry.
- **SENT/USDT** — extreme negative funding (−0.015 Bybit, elevated all venues). Crowded long, squeeze-prone. **AVOID new long.**
- **SAHARA/USDT** — −45% 24h collapse, OI deleveraging −39%, deeply negative funding. **AVOID both directions.**
- **IO/USDT** — June 11 token unlock (13.29M tokens / $1.84M / 1.7% supply) approaching in ~1.5 days. **AVOID until post-unlock.**
- **No new crypto intraday/scalp entries overnight** — regime is chop/downtrend, no A/B signals, scalp PF=0.14.

*(This decision window only. Scanning, tracking, and signal generation continue as always.)*

---

## 10. Main Risks

1. **BTC below $62K:** If BTC loses this level overnight, all long active signals (CHZ, ALLO, BAKE, ZEC) require immediate stop review. Short bias increases across crypto.
2. **ETH hack-driven selling overhang:** Humanity Protocol hacker confirmed dumping $H for ETH ($32M private-key hack). ETH may face overnight selling pressure. Monitor ETH funding and OI divergence vs BTC.
3. **Stocks structural failure — critical:** A/B PF=0.54, totalR=−23R (week). A-tier PF=0.08 (1W/12L). B-tier shorts PF=9.00 (good) but other direction dragging totals. High priority for manual review — see §14.
4. **ENA contradiction unresolved:** Janus Henderson ($480B AUM) is a real institutional investor. If crypto turns risk-on overnight/tomorrow, ENA short thesis could reverse sharply.
5. **ZEC overextended (+80% in 3 days):** Consolidation / sell-the-news risk elevated. Active signals are in profit; stop management critical.
6. **PLTR gap-up risk (tomorrow):** McCarthy Building AI partnership news could drive gap-up at tomorrow's US open. If gap above 134.20 (invalidation), B short signal is automatically invalidated.
7. **Social coverage thin:** Reddit 403-blocked persistently, no live X/Telegram/KOL. Crowd context unavailable overnight.
8. **Catalyst mapping weak:** ~95%+ `other_news` events. Symbol-specific hits reliable; aggregate statistics unreliable.

---

## 11. Action Plan — Next 4 Hours (23:24–03:30 EEST / Asia open approach)

1. **Active signal portfolio:** CHZ, ALLO, BAKE, ZEC, XLM — all tp_hit. No action unless BTC breaks $62K (then check all stops immediately).
2. **BTC $62K watch:** Critical overnight support. Break below → check all crypto long stops, consider ENA short trigger valid sooner.
3. **ENA:** Monitor for failed bounce at 0.0815–0.0823 zone. Price must bounce then fail before entry. Do not force.
4. **ZEC:** No new entry. If Ironwood July news drops overnight (e.g., mainnet date set), reassess.
5. **PLTR:** Tomorrow US open — check if gap moves above 134.20 (invalidation for active short).
6. **SMCI:** AVOID. No action.
7. **No new overnight crypto scalp/intraday entries** — chop/downtrend regime, PF=0.14, no signal confirmation.

---

## 12. Final Verdict per Mode

| Mode | Verdict |
|------|---------|
| Crypto scalp | NO TRADE — chop/downtrend regime, PF=0.14 (structural mismatch), no A/B signals. Scanning continues. |
| Crypto intraday | NO NEW ENTRY overnight. ENA short-watch with trigger required (0.0815–0.0823 failed bounce). |
| Crypto swing | **HOLD ACTIVE POSITIONS** (ZEC, CHZ, ALLO, BAKE — all tp_hit). No new swing entries at current prices. |
| Stocks intraday | US SESSION CLOSED. Short book ran today (+3R recovered into close). Monitor PLTR gap-up risk at tomorrow's open. |
| Stocks swing | WATCHLIST ONLY (paused: −12R, 0W/12L, 48h audit). SMCI AVOID. UNH manual review before entry. |
| Stocks invest | WATCHLIST ONLY (paused: 0W/7L, 14d audit). Advisory research only. |

**Scalp note:** Scalp mode structural low-confidence (PF=0.14). A/B scalp alerts are research-grade only until a proper TP1-vs-MFE audit is completed. Scanning and tracking continue regardless.

---

## 13. Sources

- [Zcash's Dramatic 80% Rebound: Swift Forks and Ironwood Rescue ZEC from Price Collapse](https://www.cryptotimes.io/2026/06/09/zcashs-dramatic-80-rebound-swift-forks-and-ironwood-rescue-zec-from-price-collapse/) — CryptoTimes, June 9 2026 | single_source | confirms ZEC Ironwood thesis
- [ZEC Price Rebounds as Zcash Finalizes Ironwood Security Upgrade](https://coinpaper.com/17560/zec-price-rebounds-as-zcash-finalizes-ironwood-security-upgrade) — CoinPaper, June 9 2026 | single_source | confirms
- [ZEC price: Zcash bounces 45% as developers propose Ironwood upgrade](https://www.coindesk.com/markets/2026/06/08/zcash-bounces-45-as-developers-propose-new-ironwood-upgrade) — CoinDesk, June 8 2026 | primary_source | confirms
- [Ethena lands Janus Henderson backing — invests in ENA, eyes USDe distribution](https://www.coindesk.com/business/2026/06/09/ethena-lands-janus-henderson-backing-as-asset-manager-invests-in-ena-eyes-usde-distribution) — CoinDesk, June 9 2026 | primary_source | ENA catalyst confirmed (price contradicts)
- [Janus Henderson takes ENA position, eyes regulated investment products tied to Ethena](https://www.theblock.co/post/404109/janus-henderson-takes-ena-position-eyes-regulated-investment-products-tied-to-ethena) — The Block, June 9 2026 | primary_source | confirms
- [Ethena Lands $480 Billion Wall Street Giant — Will ENA Price Rally?](https://beincrypto.com/ethena-janus-henderson-usde-clo-backing-2/) — BeInCrypto, June 9 2026 | single_source | weakens long (price not rallying)
- [SMCI Form 8-K: indictment of three individuals, export-control violation conspiracy](https://www.sec.gov/Archives/edgar/data/0001375365/000137536526000011/smci-20260320.htm) — SEC EDGAR, March 19 2026 | primary_source | LEGAL RISK confirmed
- [Bitcoin Price Today: BTC $63K — Saylor Buys the Dip, ETF Money Returns](https://blockchainreporter.net/bitcoin-price-today-btc-holds-63k-as-saylor-buys-the-dip-and-etf-money-returns/) — BlockchainReporter, June 9 2026 | single_source | BTC price reference

---

## 14. Fix Requests / TODO

### TODO-stocks-signal-performance-critical
- **issue:** Stocks A/B PF=0.54, totalR=−23R (week). A-tier: PF=0.08, 1W/12L (near-zero, model failure territory). B-tier: PF=0.61, −15R. Swing and invest modes already paused; intraday B shorts performing (PF~9.00 subset) but A-tier and long direction dragging totals negative.
- **evidence:** `signal-stats --asset-class stocks` CLI run 23:24 EEST: `sample=111, wins=20, losses=50, PF=0.54, totalR=-23R`. A-tier: `n=18, PF=0.083, 1W/12L`.
- **suggested manual fix:** Separate stocks intraday longs vs shorts in performance reporting. Full directional breakdown for intraday mode — B shorts (+PF 9.00) are masking long failures. Review A-tier criteria — PF=0.08 at n=18 is a structural failure, not statistical noise. Consider suspending stocks A-tier Telegram alerts until criteria reviewed.
- **priority:** high
- **first observed:** 2026-06-09 21:39 EEST (prior review), worsening trend confirmed

### TODO-smci-active-signal-cancel
- **issue:** SMCI has active C-tier intraday short in system (status=waiting). SMCI carries confirmed legal/headline risk (SEC Form 8-K export-control indictment, March 2026). Active waiting signal should be flagged and manually cancelled.
- **evidence:** `active-signals --asset-class stocks` CLI 23:24 EEST: SMCI C intraday short (62.83, status=waiting). Catalyst system: SMCI [legal_risk] Form 8-K March 2026 (primary_source).
- **suggested manual fix:** Manually cancel the SMCI C-tier short signal. Add LEGAL_RISK annotation to SMCI in system config to block future signal generation until legal situation resolves.
- **priority:** high
- **first observed:** 2026-06-09 21:39 EEST, confirmed now

### TODO-scalp-mode-audit
- **issue:** Crypto scalp mode PF=0.14, WR=12% (14d), structural net-negative. System notes TP1/2h horizon mismatch (TP1 ~1.84R vs captured MFE ~0.54R). Re-audit pending at 20 closed A/B scalp signals.
- **evidence:** `llm_analysis_packet.md`: "entry edge real (100% of expired scalps had positive MFE, avg +0.54R); TP1/2h horizon mismatch caps capture"
- **suggested manual fix:** Run dedicated scalp audit. Compare TP1 distance vs actual captured MFE on all expired scalp signals. Consider adjusting TP1 to 0.5R partial take to match real edge, or pause scalp A/B Telegram alerts until audit confirms path forward.
- **priority:** medium
- **first observed:** 2026-06-09 18:40 EEST (US open reaction review, multiple prior reviews)

### TODO-reddit-social-403-persistent
- **issue:** Reddit CryptoCurrency, Bitcoin, Ethereum all returning 403 errors persistently across all cycles today. Social attention context structurally unavailable.
- **evidence:** `cycle_01_20-38_summary.md` and multiple cycle logs: `"Failed social source Reddit CryptoCurrency: 403 Client Error: Blocked"`
- **suggested manual fix:** Replace Reddit API calls with alternative source (e.g., CoinGecko community feed, LunarCrush, or RSS-based Reddit alternative). Or flag as structurally unavailable and remove from pipeline.
- **priority:** low
- **first observed:** 2026-06-09 (persistent across all reviews today)

### TODO-scheduler-log-missing
- **issue:** `scheduler.log` file not found in project root. Prevents one of the two freshness checks in §D. Currently non-blocking (cycle summary is fresh), but the missing log may indicate a logging regression in the Windows Scheduler task.
- **evidence:** PowerShell `Test-Path "C:\Users\adama\Documents\crypto-ai-desk\scheduler.log"` returned `False` at 23:24 EEST.
- **suggested manual fix:** Investigate whether the Windows Scheduled Task `CryptoAIDesk_Scheduler` is configured to write stdout to `scheduler.log`. Check task XML / Action settings for output capture path.
- **priority:** low
- **first observed:** 2026-06-09 23:24 EEST
