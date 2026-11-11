# Opus Enriched Review — post-close final daily review — Auto Cycle 23:15 EEST

_Generated 2026-06-18 ~23:15 EEST (after US cash close, before Asia session). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods. External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch ×1: BTC ~$63,500-64,000 close Jun 18; AMD opened +3.14% Jun 18; Juneteenth June 19 — next US trading Mon Jun 22)._

---

## 1. Executive Summary

**Thu 2026-06-18, 23:15 EEST "post-close final daily review" — US session closed, stocks resilient, crypto diverged, overnight-Asia setup under risk-off.**

The US session on June 18 closed with **stocks recovering strongly** from the June 17 Fed-driven selloff: 4/4 indices uptrend, 100% EMA20/EMA50 breadth, VIX 16.61. **Crypto diverged sharply**: BTC opened at $64,450, slid to an intraday low near $62,606 (2:08 PM EDT), then recovered to ~$63,500-64,000 by close. ETH opened at $1,748 and closed near $1,744.

**Three key developments at the close:**
1. **ONDO short triggered**: Both B-tier ONDO shorts (intraday 65.2, scalp 68.0) moved from `waiting_for_entry` to `tracking`. The desk's top short idea is now live.
2. **Stocks B-tier wave triggered**: AMD, SMH, XLK, AVGO, QQQ B-tier signals all entered `tracking` by close. AMD opened +3.14% on Jun 18. **Next US trading day: Monday June 22** (Juneteenth holiday June 19).
3. **Crypto weekly stats remain poor**: B-tier crypto WR 9.7%, PF 0.545, −35R. No new wins today; 0 stops hit. 21 active swing longs mostly in `tp` (trailing).

**Dominant theme:** Fed hawkish hold absorbed asymmetrically — equities rallied (Iran deal + steady rates sentiment), crypto sold off with ETF outflows (BTC −$98M, ETH −$15M 1d). CME suing CFTC over Kalshi perps adds regulatory overhang.

**Legal/avoid carry-forward:** SMCI (export-control indictment), UNH (DOJ Medicare-fraud probe), IMX (double Aztec exploit). HARD AVOID.

**Overnight into Asia:** BTC needs to hold $62K-$63K. ONDO short is the only active live trade. Asia session will set the tone for Monday June 22 open.

---

## 2. Data Used

| Report | File | mtime EEST | Age at review | Status |
|--------|------|-----------|---------------|--------|
| Crypto scalp | `data/reports/scalp/2026-06-18_18-45_scalp_report.md` | 21:45 | 1h30m | **FRESH** (<4h) |
| Crypto intraday | `data/reports/intraday/2026-06-18_18-58_intraday_report.md` | 21:58 | 1h17m | **FRESH** (<4h) |
| Crypto swing | `data/reports/swing/2026-06-17_13-15_swing_report.md` | Jun 17 16:15 | ~31h | **STALE** (>14h) — excluded |
| Stocks intraday | `data/reports/stocks/intraday/2026-06-18_20-04_stocks_intraday_report.md` | 23:04 | 11min | **VERY FRESH** |
| Stocks swing | `data/reports/stocks/swing/2026-06-17_13-27_stocks_swing_report.md` | Jun 17 16:27 | ~31h | **STALE** — excluded |
| Catalyst events | `data/catalysts/2026-06-18/catalyst_events.jsonl` | 21:59 | 1h16m | 483 events, 6 baskets |
| LLM packet (crypto) | `data/processed/llm_analysis_packet.md` | 21:58 | 1h17m | **FRESH** |
| Prior review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-18_2139.md` | 21:39 | 1h36m | late-session review |

- **Active signals (CLI):** crypto=21 B-tier; stocks=50 total (B-tier AMD/SMH/XLK/AVGO/QQQ all `tracking`)
- **Signal stats (CLI):** crypto 7d A/B: PF 0.545, WR 9.7%, −35R; stocks 7d A/B: PF ~0.92, WR ~13.5%, −1R (A-tier +4R; B-tier −5R)
- **Untracked legacy alerts:** 0 (clean)
- **External web research (available):**
  - WebFetch: BTC opened $64,450, low $62,606 at 2:08 PM EDT, recovered ~$63,500-64,000 by close (Yahoo Finance)
  - WebSearch: AMD opened +3.14% from $512.48 (Jun 17 close) → ~$528 open; AMD B-tier triggered
  - Confirmed: June 19 = Juneteenth holiday; next US trading day = Monday June 22

---

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-18_default_schedule/`
- `scheduler.log` mtime: **22:24 EEST** (~51 min ago) → **FRESH**
- Latest cycle summary `cycle_02_21-28_summary.md` mtime: **22:24 EEST** (~51 min ago) → **FRESH** (<3h)
- **Defer rule: BOTH must exceed 3h.** Neither does. **Review proceeds.**
- Cycle 02 (21:28–22:24 EEST): 20 steps OK, 0 failed. Generated: scalp (21:45), intraday (21:58), stocks intraday (23:04). Monitors background: crypto pid 17136, stocks pid 26008.
- **No crypto swing report today.** Jun 17 stale → excluded. (See §14 TODO-CRYPTO-SWING-STALE.)
- Stocks monitor logs: 23:04 EEST (crypto), 23:06 EEST (stocks) — very fresh, reflects near-close and post-close data.
- Reddit social: **403 block** (recurring — see §14 TODO-REDDIT).
- MEXC/Bybit partial failures: routine cached fallbacks used; noted.

---

## 4. What Changed vs Previous Review

**Prior review:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-18_2139.md` (late-session risk review, 21:39 EEST)

| Item | 21:39 EEST (late session) | 23:15 EEST (post-close) |
|------|--------------------------|-------------------------|
| BTC | ~$63,908 (sliding, below $64K) | Low $62,606 at 2:08 PM EDT; recovered ~$63,500-64,000 close |
| ETH | ~$1,744 | ~$1,744 (flat; no catalyst) |
| VIX | 16.67 | 16.61 (session closed; stable) |
| Stocks breadth | 100% EMA20+EMA50 | **100%** — closed strong all day |
| JPM B-tier | `tp` tracking vs invalidation $331.42 | **No longer in B-tier active list** (TP1 hit; likely closed post-session) |
| AMD B-tier | ~$526.60 — BELOW entry zone $529-$535 | **TRIGGERED — `tracking`** (opened +3.14% Jun 18; touched entry) |
| SMH B-tier | Below entry zone $654-$659 | **TRIGGERED — `tracking`** |
| XLK B-tier | Below entry zone | **TRIGGERED — `tracking`** |
| AVGO B-tier | Below entry zone | **TRIGGERED — `tracking`** |
| QQQ B-tier | Watching | **TRIGGERED — `tracking`** |
| ONDO short (intraday) | `waiting_for_entry` | **TRIGGERED — `tracking`** |
| ONDO short (scalp) | `waiting_for_entry` | **TRIGGERED — `tracking`** |
| Active crypto signals | 20 (cycle snapshot) | 21 (+1) |
| Active stocks signals | 20 (cycle snapshot) | **50** (monitor updated) |
| Crypto 7d PF | 0.545 | **0.545** (unchanged; 0 stops, 0 new wins) |
| Stocks A-tier | JPM TP1 in `tp` status | A-tier +4R confirmed (JPM closed out) |
| SYN | +107% avoid-chase | +70-73% (24h; pulled back slightly) |
| Untracked alerts | 0 | **0** (clean) |

**New since 21:39:**
- AMD B-tier triggered (opened +3.14%; semiconductor recovery from Jun 17 Fed selloff).
- ONDO short is live — first active crypto short in the system.
- BTC intraday low $62,606 confirmed bearish trend extends; found support and recovered, but no new catalyst.
- Next US session: Monday June 22 (3-day holiday weekend — heightened gap risk for stocks B-tiers).
- AMD CEO Lisa Su ($57.6M, Jun 12) + CTO Mark Papermaster (Jun 17) insider selling flagged — reduces conviction (see §14 TODO-AMD-INSIDER-SELL).

---

## 5. Catalyst Coverage

- **Total events today:** 483 unique rows (466 from cycle scan + updated); **6 narrative baskets**
- **Baskets active:**
  - `rwa_narrative` (related_beta_rotation, <6h): ONDO/USDT, XLM/USDT
  - `delisting_thin_liquidity` (avoid_low_liquidity): —
  - `perps_dex_narrative` (wait_pullback, <1h): HYPE/USDT
  - `binance_ecosystem_teaser` (related_beta_rotation, <24h): BNB/USDT
  - `ai_narrative` (related_beta_rotation, <6h): NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT
  - `momentum_breakout` (wait_pullback, <1h): HEI/USDT — playbook `avoid_chase`
- **Unmapped:** >50% estimated (recurring — consistent with prior runs). ⚠️ **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

**High-importance verified catalysts today:**

| Symbol | Type | Headline | Impact |
|--------|------|----------|--------|
| BTC/ETH | institutional_flow | BTC ETF −$98M 1d; ETH ETF −$15M 1d (Lookonchain, Jun 18) | Institutional risk-off confirmed |
| BTC | regulatory | CME Group suing CFTC over Kalshi Bitcoin perps (Decrypt/AMBCrypto/BeInCrypto) | Regulatory overhang; bearish for crypto perps sentiment |
| BTC/ETH | macro | Fed hawkish hold; Iran deal → equities rallied, crypto sold (Yahoo Finance) | Crypto diverges from equities risk-on |
| ETH | exploit_hack | UXLink exploit $8.1M to Tornado Cash (AMBCrypto); DAO $130M security fund relaunch | Sentiment negative |
| IMX | exploit_hack | Aztec $2M exploit (The Block); second exploit in <1 week | **HARD AVOID IMX** |
| SMCI | legal_risk | SEC EDGAR 8-K export-control indictment (3 individuals, filed Mar 2026) | **HARD AVOID** |
| UNH | legal_risk | DOJ Medicare-fraud probe; shares −16% | **HARD AVOID** |
| INJ | partnership | Native INJ deposits on Coinbase via MultiVM (CryptoBriefing) | Positive; watch volume follow-through |
| AMD | insider_sell | CEO Su $57.6M sale (Jun 12); CTO Papermaster options (Jun 17) | Insider distribution at highs — flag (not hard avoid) |

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off / bearish trend (BTC downtrend, ETH transition_down, 33% breadth above EMA20)
- **Stocks mood:** risk-on (closed; bullish — 100% breadth, VIX 16.61, 4/4 uptrend) → next session Monday June 22
- **Dominant narrative:** Stocks-crypto divergence closed the US session entrenched. Stocks recovered sharply from Jun 17 Fed selloff (Iran deal + steady-rates rotation). Crypto sold off on institutional outflows, CME/CFTC regulatory uncertainty. Semiconductors (SMH +16% 20d RS vs SPY) are the top sector. AI narrative active. BTC building a range floor near $62-64K — not a confirmed base.
- **Preferred side now:** Crypto → shorts on failed retests (ONDO active); RS-leader longs only on deep confirmed pullbacks with verified catalyst. Stocks → carry B-tier longs to Monday June 22 open; no new entries.
- **Best long candidate:** AMD stocks B-tier (`tracking`) — carry to Monday; conditional on holding above $519. For crypto: INJ/HEI long-watch only on deep pullback + catalyst + volume.
- **Best short candidate:** ONDO/USDT B-tier (`tracking`) — entry $0.3549-$0.3589, TP1 $0.3445, SL 1h close above $0.3637. Active signal.
- **Best catalyst-backed candidate:** INJ/USDT — Coinbase native deposits catalyst via MultiVM; watch $5.17-5.21 retest zone + volume.
- **What to avoid:** SYN new longs (no catalyst, +70% chase, `avoid_chase` basket); UNH/SMCI/IMX HARD AVOID; new crypto longs against bearish trend; AMD/SMH new entries if Monday gaps open >3% above entry zone.
- **What would change the view:** BTC reclaims $65K + altcoin breadth returns above 50% → crypto shifts to chop; AMD/SMH hold above entry zones on Monday open → B-tier longs confirmed; ONDO 1h close above $0.3637 → short invalidated.

---

## 7. Candidate Deep Dives

### Candidate 1: ONDO/USDT SHORT (B-tier — intraday + scalp, `tracking`)

**Scores:** Intraday 65.2 | Scalp 68.0 | **Status:** ACTIVE — `tracking`
**Playbook:** `crypto_failed_bounce_short` (intraday: 14d WR 40%, PF 2.00, +9R); `crypto_scalp_momentum_continuation` (scalp: low_confidence, avg MFE +0.54R)

**Thesis:** ONDO/USDT breaks down in a bearish trend market with expanding short OI. RWA basket member but basket momentum heat only 31/100 (declining). Volume expansion at 1.56x average at last read.

**Price action:** Current ~$0.3532. Entry zone intraday: $0.3549-$0.3589. Price at/below zone → entry valid if not already chasing.

**Mood alignment:** ✅ Perfectly aligned with crypto risk-off. Short bias, bearish trend, breakdown structure.

**Derivatives:** OI +2.33%, funding −0.00013 (slightly negative), long/short 1.38 (slightly short-heavy). Not a crowded squeeze setup.

**Catalyst check:** No fresh verified catalyst for ONDO in 24h. RWA basket context only (context, not signal).

**Targets:**
- Intraday: TP1 $0.3445 / TP2 $0.3358 / TP3 $0.3271 | SL: 1h close above $0.3637
- Scalp: TP1 $0.3425 / TP2 $0.3338 / TP3 $0.3251 | SL: 1h close above $0.3616

**Overnight risk:** Asia thin liquidity. If BTC drops to $62K and holds → ONDO bearish continuation likely. If BTC bounces hard (>$65K) → ONDO squeeze risk increases.

**Chase check:** Entry zone was $0.3549-$0.3589. Price at ~$0.3532 = already slightly below zone. Tracking only. Do not re-enter if ONDO already at TP1 ($0.3445) or below.

**Action:** HOLD active signal vs invalidation. Target TP1 $0.3445 overnight.

---

### Candidate 2: SYN/USDT (RS-leader LONG-WATCH — no catalyst, avoid chase)

**Score:** Scalp 59.0, Intraday 52.8 | **Status:** C-tier watchlist — NOT active

**Performance:** +70-73% (24h), 7d +309%. RS vs BTC: +74-77%.

**Why watchlist only (not actionable):**
- No verified catalyst — momentum_breakout basket with playbook `avoid_chase`
- Funding deeply negative (−0.000728) = crowded shorts; squeeze risk for longs
- Volume below average (0.23-0.4x) — not confirmed breakout volume
- Scalp score 59.0, intraday 52.8 — well below B-tier threshold

**Conditional long setup:** Pullback to $0.1156-$0.1217 + volume expansion >1.5x + BTC stable + verified catalyst → promote to active watch. NOT tonight.

**Overnight watch:** If SYN reverses sharply in Asia (no catalyst = pure speculative move), a 30-40% fade is possible.

---

### Candidate 3: AMD (Stocks B-tier, `tracking`, carry to Monday)

**Score:** B-tier 74.0 | **Status:** TRACKING (triggered at/near close)

**Thesis:** AMD opened +3.14% on Jun 18 from $512.48 (Jun 17 close). AI/compute narrative + semiconductor sector leadership. B-tier signal triggered as AMD recovered into entry zone ~$529-535 during the session.

**Mood alignment:** ✅ Stocks risk-on, semiconductor sector strongest (SMH +16% 20d RS vs SPY).

**Catalyst:** Positive — AMD Rackspace AI compute deal + MEXT acquisition.
**Contra-catalyst flag:** CEO Lisa Su sold $57.6M (Jun 12); CTO Mark Papermaster stock options liquidation (Jun 17). Insider distribution near ATH — reduces conviction but not HARD AVOID.

**Critical overnight risk:**
- Juneteenth June 19 = US market closed. Next session: Monday June 22.
- If weekend news hits before Monday → gap risk.
- Do NOT add new AMD exposure on Monday if it gaps up >3% — chase risk.

**Invalidation:** ~$519.

**Action:** HOLD existing B-tier signal. Do not add on Monday gap. Review Sunday night 04:30 EEST auto-review and Monday 16:20 EEST pre-US-open review.

---

### Candidate 4: BTC/ETH Macro — Overnight Asia Context

**No direct signal. Context for all crypto candidates.**

**Jun 18 BTC range:**
- Open: $64,450 | Low: ~$62,606 (2:08 PM EDT) | Close: ~$63,500-64,000
- Key levels: Support $62,000-$62,600 (tested today) | Resistance $64,450 → $65,000-$65,500

**Jun 18 ETH range:**
- Open: $1,748.91 | Close: ~$1,740-$1,750

**Bearish drivers active:**
1. ETF outflows: BTC −$98M (1d), −$167M (7d); ETH −$15M (1d)
2. CME vs CFTC legal battle over Kalshi perps
3. Altcoin breadth 33% above EMA20 — deeply weak

**Asia setup:** Risk-off cautious. BTC needs to hold $62K. Break below $62K → liquidation cascade risk; all 21 crypto swing long B-tiers under heightened pressure.

---

### Candidate 5: INJ/USDT (LONG-WATCH — Coinbase catalyst, conditional)

**Score:** Scalp 60.0, Intraday 60.0 | **Status:** C-tier watchlist, NOT triggered

**Catalyst:** "Injective enables native INJ deposits on Coinbase with MultiVM technology" (CryptoBriefing, Jun 18). Importance 0.95. Positive catalyst.

**Why NOT active now:**
- Market regime: bearish trend — catalyst needs volume follow-through
- Volume ratio: 0.46-0.55x (below average)
- OI up +6.72% on price down = fresh shorts pressing

**Conditional long setup:** Price holds $5.17-5.21 zone, volume expands to >1.2x average, BTC stabilizes above $63K → promote to active watch.

**Tonight:** Watch for Coinbase-related volume surge overnight. INJ is most likely Asian session watch.

---

## 8. Best Candidates Ranked

**No clean new entries this window. ONDO short is the only live active trade.**

| Rank | Symbol | Dir | Tier | Status | Entry / Level | SL | Notes |
|------|--------|-----|------|--------|---------------|----|-------|
| 1 | ONDO/USDT | Short | B | **Tracking** | $0.3549-$0.3589 | $0.3637 | Active. Target TP1 $0.3445 overnight |
| 2 | AMD | Long | B | **Tracking** | ~$529-535 | ~$519 | Carry to Monday June 22; insider sell flag |
| 3 | SMH | Long | B | **Tracking** | ~$654-659 | ~$644 | Semiconductor momentum; carry |
| 4 | INJ/USDT | Long-watch | C | Not triggered | $5.173-5.208 | $5.251 | Catalyst real; needs volume confirmation |
| 5 | HEI/USDT | Long-watch | C | Not triggered | $0.0881-0.0910 | $0.0852 | RS leader; needs catalyst |

_Also tracking (carry):_ XLK B (triggered), AVGO B (triggered), QQQ B (triggered).

---

## 9. Avoid / No Trade

_(Scanner and data collection continue in all moods)_

- **SMCI:** Export-control indictment (SEC EDGAR 8-K, 3 individuals, filed Mar 2026). **HARD AVOID.**
- **UNH:** Confirmed DOJ Medicare-fraud probe; shares −16%. **HARD AVOID.** C-tier long signals still active in system — flag for manual invalidation (§14 TODO-UNH-INVALIDATION).
- **IMX:** Double Aztec exploit within <1 week. **HARD AVOID** until post-mortem complete.
- **SYN new longs:** No catalyst, +70% 24h, `avoid_chase` basket. Do not enter.
- **New crypto longs (non-RS-leader):** Bearish trend, 33% breadth. No A-tier anchor.
- **AMD/SMH Monday gap-chase:** If stocks gap open >3% Monday, do NOT enter fresh.

---

## 10. Main Risks

1. **BTC breaks $62,000 overnight (Asia)** → liquidation cascade; 21 active swing long B-tiers at heightened stop risk.
2. **AMD/semiconductor gap-down Monday** → Juneteenth weekend gap risk; AMD B-tier SL at ~$519.
3. **AMD insider selling** (CEO $57M + CTO, both near ATH) — distribution signal; reduces B-tier conviction.
4. **ONDO short squeeze** — OI expanding but funding mildly negative. If ONDO reclaims $0.3637 on 1h close, exit.
5. **CME vs CFTC regulatory battle** — ongoing overhang suppresses crypto perps sentiment into weekend.
6. **Catalyst mapping weak** (>50% unmapped) — catalyst layer unreliable as sole decision basis. Use as context.
7. **Social data blackout** — Reddit 403 blocked. Crowd context thin; SYN +70% move unverifiable via social.
8. **UNH C-tier long signals** — system has active UNH longs despite confirmed DOJ probe. Manual invalidation required.
9. **No crypto swing report (Jun 18)** — 18 active B-tier swing longs tracked from stale Jun 17 basis.
10. **Stocks-crypto convergence risk** — if negative weekend event causes stocks to sell off Monday, crypto has no buffer.

---

## 11. Action Plan — next 4 hours (23:15–03:15 EEST)

1. **ONDO short:** Monitor. TP1 = $0.3445. SL = 1h close above $0.3637. Hold vs invalidation. Do not add size.
2. **BTC $62,600 support:** If BTC tests and holds → neutral Asia setup. If BTC breaks $62,000 → crypto-wide risk; all swing longs flagged.
3. **SYN:** Watch for catalyst announcement. If none by 04:30 EEST Asia review, move is speculative.
4. **INJ:** Watch Coinbase volume pickup overnight. If volume >1.2x and BTC holds $63K → promote to active watch at 04:30 EEST.
5. **No new crypto entries tonight.** Risk-off; no A-tier.
6. **AMD/SMH/XLK/QQQ/AVGO:** Carry. No action until Monday June 22 open.
7. **UNH:** Flag for manual invalidation session (§14). Do not trade in any direction.

---

## 12. Final Verdict per Mode

| Mode | Verdict |
|------|---------|
| Crypto scalp | ONDO short active (scalp 68.0 — `tracking`). Track TP1 $0.3425. No new scalp entries. |
| Crypto intraday | ONDO short active (intraday 65.2 — `tracking`). No new intraday ideas without fresh catalyst. |
| Crypto swing | No fresh swing report (Jun 18). 18 active B-tier swing longs in `tp` from stale Jun 17 levels. No new swing longs in bearish trend. |
| Stocks intraday | Market closed. AMD/SMH/XLK/AVGO/QQQ B-tier all triggered, `tracking`. Carry to Monday June 22. |
| Stocks swing | Stale (Jun 17). A-tier JPM TP1 confirmed (+4R, closed out). B-tier stocks now tracking. |

---

## 13. Sources

| # | Title | Source | Date | Verification | Relation |
|---|-------|--------|------|-------------|----------|
| 1 | Bitcoin and ethereum prices today, Thursday, June 18, 2026: Prices sliding despite Iran peace deal | Yahoo Finance | Jun 18 2026 | primary_source | BTC/ETH prices, Fed catalyst, Iran deal |
| 2 | Advanced Micro Devices Inc Stock (AMD) Opened Up by 3.14% on Jun 18 | TradingKey | Jun 18 2026 | single_source | AMD open +3.14%, ATH $547.26 Jun 15 |
| 3 | Bitcoin Price is $63,961 today | MetaMask | Jun 18 2026 | single_source | BTC live price confirmation |
| 4 | Bitcoin, Ethereum Traders Grow Even More Bearish as Prices Fall After Fed Decision | Decrypt | Jun 18 2026 | single_source | BTC/ETH bearish sentiment, Fed |
| 5 | CME to Sue CFTC Over Bitcoin Perpetual Futures Approval: CEO | Decrypt | Jun 18 2026 | single_source | Regulatory overhang BTC |
| 6 | June 18 Update: BTC ETFs 1D NetFlow −$98.45M; ETH ETFs 1D NetFlow −$15.63M | Lookonchain/t.me | Jun 18 2026 | single_source | Institutional outflows confirmed |
| 7 | Injective enables native INJ deposits on Coinbase with MultiVM technology | CryptoBriefing | Jun 18 2026 | single_source | INJ Coinbase catalyst |
| 8 | UXLink exploit: attacker sends $8.1M ETH to Tornado Cash | AMBCrypto | Jun 18 2026 | single_source | ETH negative catalyst |
| 9 | Aztec investigates $2 million exploit of deprecated payments product | The Block | Jun 18 2026 | single_source | IMX HARD AVOID |

Internal sources: `data/reports/scalp/2026-06-18_18-45_scalp_report.md`, `data/reports/intraday/2026-06-18_18-58_intraday_report.md`, `data/reports/stocks/intraday/2026-06-18_20-04_stocks_intraday_report.md`, `data/catalysts/2026-06-18/catalyst_events.jsonl`, `data/scheduled_runs/2026-06-18_default_schedule/cycle_02_21-28_summary.md`, `OPUS_ENRICHED_REVIEW_AUTO_2026-06-18_2139.md`, active-signals/signal-stats CLI.

---

## 14. Fix Requests / TODO

### TODO-UNH-INVALIDATION
- **issue:** UNH has active C-tier long signals in the system despite a confirmed DOJ Medicare-fraud probe and −16% share drop
- **evidence:** C-tier active signals table (stocks): UNH C intraday `tp`; catalyst_events.jsonl: `legal_risk` entries for UNH; flagged in prior review at 21:39 EEST
- **suggested fix:** Manually invalidate all active UNH signals. Add UNH to hard-avoid list until DOJ investigation is resolved. Consider adding system trigger: if `legal_risk: confirmed` in catalyst layer, auto-cap matching signal to `rejected` tier.
- **priority:** high | **first observed:** 2026-06-18 21:39 EEST

### TODO-AMD-INSIDER-SELL
- **issue:** AMD has active B-tier long signals while CEO Lisa Su ($57.6M, Jun 12) and CTO Mark Papermaster (Jun 17) executed significant insider sales near ATH ($547.26 on Jun 15)
- **evidence:** TradingKey AMD article Jun 18 2026; AMD B-tier signals in `tracking`
- **suggested fix:** Flag AMD for manual review before Monday June 22 open. Assess whether to lower conviction or tighten SL. Insider distribution near ATH can precede selling pressure.
- **priority:** medium | **first observed:** 2026-06-18 23:15 EEST

### TODO-REDDIT
- **issue:** Reddit RSS sources returning 403 (Blocked) consistently across all subreddits (CryptoCurrency, Bitcoin, Ethereum)
- **evidence:** cycle_02_21-28_summary.md — multiple 403 errors for Reddit hot.json endpoints
- **suggested fix:** Evaluate alternative social data sources or authenticated Reddit API access (OAuth). Consider disabling Reddit sources until compliant access method is restored.
- **priority:** medium | **first observed:** 2026-06-04 (recurring)

### TODO-CRYPTO-SWING-STALE
- **issue:** No crypto swing report generated on June 18; all swing context relies on Jun 17 stale report (>31h old)
- **evidence:** No `2026-06-18_*_swing_report.md` in `data/reports/swing/`; cycle_02 did not include swing step
- **suggested fix:** Check if swing cycle was intentionally suppressed or silently skipped. Run manual swing report before Monday open to refresh levels for 18 active swing B-tiers.
- **priority:** medium | **first observed:** 2026-06-18 23:15 EEST

### TODO-CATALYST-MAPPING
- **issue:** Catalyst mapping consistently >50% unmapped; 483 events today with estimated >50% unmapped (prior run confirmed 79.6% unmapped)
- **evidence:** `data/catalysts/2026-06-18/catalyst_events.jsonl` event counts vs mapped symbols in reports; recurring across multiple weeks
- **suggested fix:** Improve symbol resolver in catalyst layer — expand entity extraction, add fuzzy matching for company names, improve news-to-ticker mapping.
- **priority:** medium | **first observed:** recurring (prior sessions)
