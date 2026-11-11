# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:52 EEST

- **Generated:** 2026-06-10 11:52 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, **11:30 "Europe / pre-US context" slot**, executing `opus-enriched-review-4h/SKILL.md`)
- **Slot context:** EU morning crypto + macro; what changed since overnight review; BTC/ETH mood + altcoin breadth; actionable crypto setups before US flows; US macro / news calendar; stocks pre-market/planning only.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-10_0439.md` (crypto overnight / Asia review, 04:39 EEST, ~7h ago — see §4).
- **External web research:** AVAILABLE. BTC ~$61,739–$62,500 (Iran-conflict overhang, ceasefire fragile). CHZ ~$0.044, tp_hit confirmed — World Cup kickoff June 11 (tomorrow), sell-news risk imminent. SMCI -10–20% on $7B equity raise + SEC legal risk. UNH DOJ criminal probe confirmed (-16% dive). HYPE: Grayscale/21shares/Bitwise ETFs $160M+ inflows, Coinbase integration confirmed.
- **Data quality warning:** Fresh scalp and intraday reports (11:26–11:27 EEST) show universe=0, ohlcv_fetched=0 across ALL exchanges (Binance failed=1, Bybit failed=54, MEXC failed=54). Only 2 cached symbols (BTC, ETH) reached deep analysis. Swing report (04:28) had full coverage — the degradation is from the old scheduler's accumulated failures. New scheduler Cycle 1/12 just launched at 11:51; fresh OHLCV expected in ~20–30 min.
- **Chart tools:** TradingView / Chrome MCP not loaded — no fabricated chart observations. OHLCV/ATR/EMA from internal reports + cited external sources only.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

**11:52 EEST. Europe / pre-US context: risk-off regime, BTC ~$62K, exchange data degraded, World Cup Eve.**

**Key developments since 04:39 overnight review:**
- **CHZ tp_hit** — the B swing long from the overnight review hit TP1 ($0.0292). External data shows CHZ now ~$0.044, far beyond all internal TPs. World Cup starts TOMORROW June 11. CRITICAL: sell-news risk is at peak — any remaining CHZ exposure must be managed TODAY before kickoff.
- **SMCI LEGAL + DIRECTION FLIP** — swing report (7.5h old) had SMCI as B-tier LONG at 70.63. Fresh intraday report (23min ago) has SMCI as C-tier SHORT at 64.17. Catalyst: $7B equity raise announced June 9 → stock -10–20%. Legal: SEC 8-K, indictment of three individuals for export-control violation conspiracy. AVOID both directions without manual review.
- **UNH LEGAL** — B swing long signal (score 68.17) still active in DB. DOJ criminal probe confirmed: Medicare fraud, shares -16%. AVOID. Signal generated before probe confirmation.
- **HYPE catalyst confirmed** — Coinbase integration (USDC deployer, $5B supply) + HYPE ETF inflows $160M+ (Grayscale, 21shares, Bitwise). Perps_dex_narrative basket fresh <1h at report time. Playbook: wait_pullback.
- **Exchange data collapse in fresh reports** — universe=0 across all exchanges. Deep analysis covered only BTC+ETH from cache. New scheduler just launched. Most alts invisible in fresh run.
- **Multiple stocks B-tier shorts triggered overnight** — NVDA, PLTR, QQQ, TSLA, AMZN, META, GOOGL, MSFT, COIN — all B-tier intraday shorts in active signals. Market is pre-open (16:30 EEST = 09:30 ET). None are actionable until RTH confirmation.
- **No new A-tier signals either asset class.**

**Best candidates this window:**
- **Best long-watch:** SENT/USDT — B swing long waiting_for_entry, RS +21.7% vs BTC, entry zone 0.0162–0.0166 (7.5h old data — needs fresh confirmation)
- **Best short-watch:** PLTR or QQQ — B-tier intraday short triggered, wait for RTH open + first 15–30 min confirmation
- **Best catalyst-backed:** HYPE/USDT — confirmed multi-source catalyst (Coinbase + $160M ETF), wait_pullback playbook
- **What to avoid now:** SMCI (legal + dilution), UNH (DOJ probe), new crypto intraday longs (exchange failures + 0W/7L mode), stocks before RTH open

---

## 2. Data Used

**Internal — crypto reports:**

| Report | Generated | Age at 11:52 | Status |
|--------|-----------|--------------|--------|
| Scalp | 2026-06-10 11:26 EEST | 26 min | **FRESH** (exchange-degraded: universe=0) |
| Intraday | 2026-06-10 11:27 EEST | 25 min | **FRESH** (exchange-degraded: universe=0) |
| Swing | 2026-06-10 04:28 EEST | 7.5h | **carry-forward** (full coverage, 135 symbols) |

**Internal — stocks reports:**

| Report | Generated | Age at 11:52 | Status |
|--------|-----------|--------------|--------|
| Stocks intraday | 2026-06-10 11:29 EEST | 23 min | **FRESH** (indices/ETFs failed=10/12 each, symbols failed=84) |
| Stocks swing | 2026-06-10 04:31 EEST | 7.4h | **carry-forward** (full coverage) |
| Stocks invest | not requested this slot | — | — |

**CLI (captured at 11:52 EEST):**
- `active-signals crypto`: **9 active** (1 waiting_for_entry B intraday SHORT, 1 waiting_for_entry B swing LONG, 7 tp_hit)
- `active-signals stocks`: **50 active** (multiple B-tier intraday shorts triggered, all C-tier signals; no A-tier active)
- `signal-stats crypto`: PF=1.58, totalR=+15R, n=88 (B-tier); by-mode: mode3 = 0W/7L, -7R (broken — see §14)
- `signal-stats stocks`: PF=0.78, totalR=−7R (A/B, n=91); by-direction: shorts PF=0.44, -42R; A-tier 1W/12L (see §14)
- `detect_untracked_legacy_alerts`: **0 (clean)**

**Catalyst / narrative (from fresh reports, 11:26 EEST):**
- Catalyst events today: **627** (increased from 500 in overnight swing report)
- Active narrative baskets: **4** (perps_dex_narrative HYPE, rwa_narrative ONDO/XLM, ai_narrative NEAR/RENDER/TAO/FET, momentum_breakout STRAX/BABY)
- Notable: perps_dex_narrative (HYPE) fresh <1h; momentum_breakout (STRAX/BABY) fresh <1h (avoid_chase playbook)

**External research:**
- SMCI equity raise: GuruFocus, Cryptopolitan, FX Leaders, SEC EDGAR (June 9–10 2026)
- UNH DOJ probe: QuiverQuant, Yahoo Finance, Medical Economics (June 2026)
- HYPE ETFs/Coinbase: CoinDesk, KuCoin, SpotedCrypto, CNBC (June 3–10 2026)
- BTC/Iran: BeInCrypto, crypto.news, AnalyticsInsight, Memeburn (June 10 2026)
- CHZ/World Cup: CryptoBriefing, CCN, Phemex (June 10 2026)

---

## 3. Scheduler / Data Freshness

- **No defer.** Latest scheduler folder: `2026-06-10_default_schedule`, mtime 11:51 EEST (1 min ago). Scheduler.log: Cycle 1/12 START at 11:51 EEST.
- **Note:** The new scheduler just booted. The fresh reports (11:26–11:29) were generated by the OLD scheduler (`2026-06-09_default_schedule`)'s final cycles, which ran until ~11:30. Those reports ARE fresh but show exchange-API degradation accumulated across 12+ cycles.
- **Previous scheduler last cycle:** `2026-06-09_default_schedule` folder mtime 11:30 EEST. Reports: ok and timestamped.
- **Exchange data degradation (fresh reports):** Binance universe=0 (failed=1), Bybit failed=54, MEXC failed=54. Swing report (7.5h old) had full coverage. This is likely API exhaustion from the old scheduler. New scheduler Cycle 1 should recover coverage in ~30 min.
- **Crypto OHLCV:** only BTC and ETH from cache; all other alts invisible in fresh scalp/intraday runs.
- **Stocks OHLCV:** indices failed=10, sector ETFs failed=12, symbols failed=84 in fresh intraday. Market pre-open — data will refresh closer to RTH.

---

## 4. What Changed vs Previous Review (04:39 EEST)

**Previous review:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-10_0439.md` (overnight/Asia, 04:39 EEST, ~7h ago)

| Signal / Candidate | Prior State (04:39) | Current State (11:52) | Assessment |
|---|---|---|---|
| CHZ B swing long | TRIGGERED (active), monitoring for TP1 | **tp_hit** — confirmed | Price reached $0.044, far above TP3 ($0.0311). SELL-NEWS risk: June 11 kickoff today/tomorrow |
| SENT B swing long | waiting_for_entry (best long-watch) | **still waiting_for_entry** | Unchanged. Still best long-watch. Data 7.5h old. |
| XLM? B intraday short | not in signals | **NEW: B intraday SHORT, waiting_for_entry** | New direction-switch signal (XLM swing long was tp_hit earlier) |
| SMCI stock | not in top-5 | **LEGAL RISK: $7B equity raise + SEC indictments** | Direction flip: swing B-long (7.5h old) vs fresh C-short. AVOID. |
| UNH stock | mentioned as stocks planning context (B swing 69.86) | **LEGAL RISK: DOJ criminal probe confirmed (-16%)** | Active B swing signal in DB = must flag AVOID. |
| HYPE/USDT | perps_dex_narrative basket active | **Catalyst UPGRADED: Coinbase integration confirmed + $160M ETF inflows** | wait_pullback playbook. Multi-source confirmed. |
| STG/USDT | +41% chase rejected | No longer in fresh reports (exchange failures) | Status unknown; momentum_breakout basket shifted to STRAX/BABY |
| HAEDAL/USDT short-watch | best short-watch (0.0186–0.0189 rejection) | Not visible in fresh reports (exchange failures) | Old levels stale. Requires fresh data from new scheduler. |
| Stocks B-tier shorts | not visible (pre-market) | **NVDA/PLTR/QQQ/TSLA/AMZN/META/GOOGL/MSFT/COIN triggered** | All pre-market / planning only. Require RTH confirmation. |
| BTC macro | Iran strikes ongoing, BTC ~$63.7K recovery | BTC ~$61,739–$62,500, ceasefire still fragile | Slight further deterioration. $62K support zone critical. |
| James Wynn BTC short | mentioned as macro headline | **LIQUIDATED 4× on BTC short at $62,314** | Crowded-short signal confirms $62K as key contested level |
| Intraday mode 0W/7L | flagged in §14 | UNCHANGED: still 0W/7L, -7R | Persistent. See §14. |
| Stocks A-tier 1W/12L | flagged in §14 | UNCHANGED: PF=0.08 | Persistent. See §14. |

**New catalysts since overnight review:**
- CME Group launches Nasdaq CME Crypto Index Futures (BTC, ETH, SOL + 4 more) — institutional expansion
- James Wynn liquidated 4× on BTC short at $62,314 → confirms $62K as key level
- Stocks short systemic data point: stocks shorts -42R overall confirmed

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 627 (up from 500 at 04:28 — more events ingested through the morning)
- **Active narrative baskets:** 4 (perps_dex_narrative, rwa_narrative, ai_narrative, momentum_breakout)
- **Mapped/unmapped ratio:** not quantifiable without SQLite query (see §14 TODO-catalyst-mapping-visibility from prior review)
- **Notable structured events this slot:**
  - `HYPE/USDT` [regulatory_sector_headline] Hyperliquid Futures go live on Coinbase as HYPE ETF inflows top $91M (AMBCrypto) — **multi-source confirmed externally**
  - `SMCI/USDT (stocks)` [legal_risk] Export-control violation indictments (SEC EDGAR 8-K) + $7B equity raise dilution (June 9)
  - `UNH (stocks)` [legal_risk] DOJ criminal probe, Medicare fraud (QuiverQuant, Yahoo Finance)
  - `BTC/USDT` [macro] Trump strikes Iran amid fragile ceasefire; James Wynn 4× liquidated at $62,314
  - `AAVE/USDT` [exploit_hack] KelpDAO exploit governance proposal (CryptoBriefing) — ongoing
  - `BNB/USDT` [exploit_hack] Humanity Protocol H token exploit (developer machine compromise) — ongoing
  - `momentum_breakout` basket: STRAX/BABY replacing STG (STG data unavailable in fresh run)

Catalyst mapping % unavailable this run — use catalyst layer as **context, not final decision signal.** See §14 TODO-catalyst-mapping-visibility.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off (BTC downtrend, ETH downtrend; altcoin breadth 0% above EMA20 in fresh reports; exchange APIs degraded)
- **Stocks mood:** pre-market (US session opens 16:30 EEST — all signals planning/watchlist only; do NOT treat B-tier shorts as actionable before RTH)
- **Dominant narrative:** Geopolitical risk-off (US-Iran escalation, ceasefire fragile) + World Cup Eve CHZ sell-news alert + HYPE ecosystem expansion (Coinbase + ETF) + SMCI/UNH legal shocks
- **Preferred side now:** Catalyst-backed longs on pullback (HYPE wait_pullback), RS-leader swing longs on pullback (SENT), NO new crypto intraday longs (exchange failures + 0W/7L mode); stocks → wait RTH
- **Best long candidate:** SENT/USDT — B swing long waiting_for_entry, RS +21.7% vs BTC; trigger: pullback into 0.0162–0.0166 zone + 1h hold (old data, verify levels at new scheduler output)
- **Best short candidate:** PLTR B-tier intraday short triggered (score ~71, highest stocks B-tier); trigger: wait for RTH open, first 15–30 min confirmation, avoid pre-market entry
- **Best catalyst-backed candidate:** HYPE/USDT — Coinbase Futures + $160M ETF inflows confirmed; playbook wait_pullback; entry after pullback stabilization
- **What to avoid:** SMCI (legal + dilution; AVOID), UNH (DOJ probe; AVOID), new crypto intraday longs (exchange failures, 0W/7L mode), stocks shorts before 16:30 EEST, CHZ new entry (World Cup kickoff = sell-news tomorrow)
- **What would change the view:** BTC 1h close above $64K on volume → shift toward risk-on, consider RS-leader longs; BTC close below $62K → deepen risk-off, tighten all longs; RTH open with QQQ/SPY gap-down + follow-through → stocks B-tier short activation; HYPE pullback to -10% from peak → wait_pullback trigger

---

## 7. Candidate Deep Dives

### Candidate 1 — CHZ/USDT (B swing long, tp_hit)

**Status:** tp_hit (position was active, hit TP1 at ~$0.0292). External price now ~$0.044. **CRITICAL: sell-news risk TODAY/TOMORROW.**

**Setup recap:**
- Signal entered zone overnight (0.0277–0.0281). TP1 $0.0292 (hit, tp_hit status confirmed).
- TP2 $0.0302, TP3 $0.0311 (internal). External price ~$0.044 = far beyond all TPs.
- Stop at the time: 1h close below $0.0272. ATR (04:28): $0.0009.

**External catalyst — confirmed:**
- FIFA World Cup 2026 kickoff: JUNE 11 (TOMORROW). South Korea vs Czechia, 22:00 ET, Estadio Akron, Guadalajara.
- CHZ +46% in past month ahead of World Cup. Trading ~$0.044 as of external data.
- Historical pattern: CHZ +380% pre-Qatar 2022 World Cup → crashed same day kickoff. "Buy the rumor, sell the kickoff."
- Sources: CryptoBriefing June 10 2026 (primary), CCN (single_source), Phemex (single_source). Convergent across 3 sources.

**Price reaction / chase check:**
- The position was entered at the pullback (~$0.0281), tp_hit at TP1. The continued rally to $0.044 represents 55% beyond entry.
- This is NOT a new entry opportunity — the move has already happened.
- Chase risk for NEW entry: EXTREME (>4× ATR extension from overnight entry).
- Time risk: World Cup kickoff June 11 = sell-news window opens imminently.
- Aligned with mood? Counter-tape long (risk-off), justified ONLY by the now-expiring catalyst.

**VERDICT: NO NEW ENTRY. If any partial position was held past TP1 (against the recommended time-stop from the overnight review): EXIT before June 11 kickoff. Sell-news risk is peak. Historical pattern is clear. Position management window = TODAY.**

---

### Candidate 2 — SMCI (Direction flip + Legal risk)

**LEGAL / HEADLINE RISK — MANDATORY FLAG**

**Status:** Direction flip. Swing report (7.5h, carry-forward): B-tier LONG at 70.63. Fresh intraday (23min): C-tier SHORT at 64.17.

**Legal risk — CONFIRMED:**
- SEC EDGAR Form 8-K (FY2026): indictment of three individuals for alleged export-control violation conspiracy. Source: SEC EDGAR (primary_source), March 1 2026 (still active, no resolution noted).
- $7B equity raise announcement June 9 2026: $5B underwritten offering ($1.25B common + $3.75B depositary shares) + $2B ATM program. Announced to fund $39B AI server order backlog.
- Market reaction: stock -10–20% (FX Leaders: -20% on proposed raise; Cryptopolitan/Mitrade: -10%).
- Source: GuruFocus (single_source), Cryptopolitan (single_source), FX Leaders (single_source), StockTitan (single_source), SEC EDGAR Form FWP (primary_source). Verification: multi-source dilution event.

**Contradiction analysis:**
- Swing B-tier LONG (score 70.63) was generated on 7.5h-old data (01:31 EEST, pre-equity-raise announcement confirmation propagating into OHLCV).
- Fresh intraday C-tier SHORT (64.17) reflects post-announcement price decline.
- The swing signal was likely generated on prior uptrend momentum. The dilution event reversed that momentum.
- CANNOT treat the swing B-long as valid — the catalyst that generated it is now NEGATIVE.

**Price reaction / chase check:**
- Stock already dropped 10–20% post-announcement. The initial gap may be partially priced.
- For SHORT: Entering after -20% gap risks buying into exhausted sellers. Short requires RTH confirmation + volume.
- For LONG: The equity raise is massive dilution. The $39B backlog is real, but dilution shock + ongoing legal = high uncertainty.
- Is this overextended? Yes for new short — gap already occurred.
- What makes short actionable: RTH open weak + no bounces above gap fill zone + volume continuing.
- What makes long actionable: Definitive legal resolution + equity raise priced in + new support holds.

**LEGAL/HEADLINE RISK:** Export-control indictments (ongoing) + $7B dilution = DUAL RISK.

**VERDICT: AVOID BOTH DIRECTIONS until RTH + manual review. SMCI short = wait RTH, first-bar confirmation. SMCI long = avoid without legal clarity. Do not rely on the stale swing B-tier signal.**

---

### Candidate 3 — HYPE/USDT (Catalyst-backed, perps_dex_narrative)

**Status:** C-tier expansion watchlist + perps_dex_narrative basket fresh <1h. Score from basket: unquantified (OHLCV unavailable in fresh run due to exchange failures). **Best catalyst-backed candidate.**

**Catalyst — CONFIRMED (multi-source):**
- **Coinbase integration:** Coinbase became official USDC deployer on Hyperliquid; USDC supply on Hyperliquid reached $5B.
- **Hyperliquid Futures on Coinbase:** HYPE token futures launched on Coinbase (AMBCrypto headline). Verified via KuCoin: "Hyperliquid's HYPE Token Surges 6.5% Amid Bitwise ETF Launch and Coinbase Integration."
- **ETF ecosystem:**
  - Grayscale Hyperliquid Staking ETF (HYPG) launched Nasdaq, 0.29% fee (CoinDesk June 3 2026 — primary_source).
  - 21shares HYPE ETF: $66M AUM. Bitwise HYPE ETF: $88M AUM. Total: ~$160M inflows.
  - CNBC (June 6 2026): "Bitcoin is cratering, but a new Wall Street crypto hype is on the rise" — confirms HYPE as distinct narrative.
- **Playbook context:** perps_dex_narrative basket uses `wait_pullback` playbook. This means the catalyst is confirmed but the immediate reaction has already occurred — wait for price to consolidate/pull back before entry.
- Sources: CoinDesk (primary_source), KuCoin (single_source), SpotedCrypto (single_source), CNBC (single_source).

**Price reaction / chase check:**
- Internal OHLCV for HYPE: unavailable (exchange failures in fresh run, universe=0). Cannot confirm current price, ATR, or EMA levels.
- External: "HYPE Token Surges 6.5% Amid Bitwise ETF Launch" — this reaction already occurred.
- Wait_pullback playbook specifically = do NOT enter on the immediate catalyst spike. Wait for -5–10% pullback to a support level.
- Aligned with mood? HYPE is a specific catalyst-backed setup — justified even in risk-off if pullback structure exists.
- What makes it actionable: HYPE price pullback -7–12% from the Coinbase announcement high + volume drying on the dip + BTC stable above $62K.
- Invalidation: HYPE loses the structural support that preceded the ETF/Coinbase announcements. Requires fresh OHLCV from new scheduler.
- Is this a chase? At the moment of announcement surge = YES. After pullback = NO.

**External research gap:** No current price data for HYPE in fresh reports. All OHLCV from exchange failures. Verdict demoted to "manual review required for entry level" — catalyst thesis is strong but execution levels need new scheduler data.

**VERDICT: CATALYST-BACKED LONG-WATCH. Entry requires fresh OHLCV from new scheduler Cycle 1 (expected ~12:20 EEST). Wait_pullback playbook. Best catalyst-backed candidate this window. Do not enter the current spike.**

---

### Candidate 4 — UNH (B swing long in DB + DOJ probe)

**LEGAL / HEADLINE RISK — MANDATORY FLAG**

**Status:** C-tier signal in DB (swing long, waiting_for_entry, score ~68). Swing report (7.5h, carry-forward): B-tier LONG at 68.17. **LEGAL RISK CONFIRMED.**

**Legal risk — CONFIRMED:**
- DOJ criminal probe into UnitedHealth Group for possible Medicare fraud (billing practice inflation, risk score manipulation).
- Shares dove 16% on DOJ probe announcement (QuiverQuant June 2026 — single_source; Yahoo Finance/WSJ report — primary confirmation).
- Multiple state AGs coordinating. Congressional hearings in late 2025/early 2026.
- UnitedHealth launched third-party internal review.
- Source: QuiverQuant (single_source), Yahoo Finance/WSJ (primary_source), Medical Economics (single_source). Verification: multi-source, confirmed.

**Price reaction / chase check:**
- Shares -16% already occurred. The swing B-long signal was generated BEFORE the DOJ probe became fully public.
- The swing signal entry zone (score 68.17, waiting_for_entry) is now below the current price (stock dropped). The "entry" from the stale signal may be below the dip bottom.
- Even if price technically triggers the zone: LEGAL RISK OVERRIDES. Criminal probe = unpredictable tail risk.
- What makes it actionable: DOJ probe resolution, company statement with material update, stock stabilizes >3 sessions post-drop. NONE of these conditions met now.

**LEGAL/HEADLINE RISK:** DOJ criminal probe (Medicare fraud). Shares -16%. ACTIVE.

**VERDICT: AVOID. B swing signal is stale and based on pre-probe data. LEGAL/HEADLINE RISK overrides all technical setups. Do not enter UNH long or short without manual review of latest price levels and DOJ probe status.**

---

### Candidate 5 — Stocks B-tier intraday shorts (NVDA/PLTR/QQQ/TSLA/AMZN/META/GOOGL/MSFT/COIN)

**Status:** Multiple B-tier intraday short signals triggered in active-signals DB. All are PRE-MARKET. US session opens 16:30 EEST (09:30 ET). **Not actionable until RTH.**

**Setup:**
- PLTR B intraday short: score ~71 (highest stocks B-tier in triggered list)
- QQQ B intraday short: score ~69 (broad index — best risk-routing confirmation)
- TSLA B intraday short: score ~70
- AMZN B intraday short: score ~70
- META B intraday short: score ~68
- NVDA, GOOGL, MSFT, COIN: B-tier intraday shorts triggered, scores 65–66
- Entry levels: truncated in CLI output. Exact levels unavailable without DB query.

**Market context:**
- Stocks intraday (fresh 11:29): regime = risk_off (bias=short). VIX=18.92. Breadth EMA20=0%. All indices in "range" trend (data failed for returns).
- Macro risk-off (Iran, CHZ sell-news, SMCI/UNH shocks) supports short bias into US open.
- Note: stocks OHLCV data failed in fresh intraday (indices=10/10 fail, symbols=84/84 fail) — the B-tier signals were generated from a prior session's data.

**Performance context (critical):**
- Stocks B-tier overall: PF=1.20, +4R (week, n=73 triggered) — marginally positive.
- Stocks shorts overall: PF=0.44, -42R (all tiers, 149 triggered) — **systemically poor**.
- BUT: playbook audit (`STRATEGY_PLAYBOOK_AUDIT.md` / LLM packet) shows `stocks_intraday_rth_momentum` WR 55%, PF 2.03, +80R; shorts subset PF 9.00. **This divergence requires manual investigation (see §14).**
- Stocks A-tier: 1W/12L, PF=0.08 (ongoing regression — see §14).

**Price reaction / chase check:**
- All signals triggered overnight/pre-market. Entry zones reflect yesterday's close or overnight drift.
- The 11:30 slot rule: "Do NOT chase pre-market moves without RTH confirmation."
- First 15–30 min of RTH session should be observed before entering any intraday short.
- Gap risk: if US opens gap-down, the short may be overextended at the open. Wait for a dead-cat bounce attempt before the short.
- Aligned with mood? YES for direction (risk-off) — but only AFTER RTH confirmation.
- What makes them actionable: RTH open + 15–30 min confirmation + no massive gap-down (avoid chasing) + QQQ/SPY direction aligns.
- Best of the group: **QQQ** (broad market confirmation + B-tier) and **PLTR** (highest individual score ~71).
- Invalidation: first 30 min of RTH prints higher-high above signal's entry zone → no entry.

**VERDICT: PRE-MARKET PLANNING ONLY. QQQ and PLTR are the cleanest B-tier short setups for the 16:30 EEST open — but REQUIRE: (1) RTH open + 15–30 min confirmation, (2) no massive pre-open gap-down that overextends the short, (3) QQQ/SPY first-bar direction aligned. Do not enter before 16:30 EEST.**

---

## 8. Best Candidates Ranked

No clean A-tier entries. Pre-US-open actionable plan:

| Rank | Symbol | Side | Asset | Status | Key Level | Why |
|---|---|---|---|---|---|---|
| 1 | HYPE/USDT | long | Crypto | **Catalyst-watch** | Wait for -7–12% pullback after Coinbase/ETF spike | Multi-source confirmed catalyst, wait_pullback playbook |
| 2 | SENT/USDT | long | Crypto | **Long-watch (B swing)** | Pullback to 0.0162–0.0166 + 1h hold (verify with new scheduler) | B swing waiting_for_entry, RS +21.7% vs BTC |
| 3 | QQQ | short | Stocks | **Short-watch (RTH only)** | RTH open + 15–30 min confirmation; no pre-open entry | B-tier triggered, highest broad-market B-tier short |
| 4 | PLTR | short | Stocks | **Short-watch (RTH only)** | RTH open + first-bar confirmation; score ~71 | Highest individual B-tier stocks short score |
| 5 | CHZ/USDT | — | Crypto | **EXIT/MANAGE existing** | Exit any remaining before June 11 kickoff | Sell-news risk imminent; tp_hit, price far above TPs |

**No clean trade this exact window:** crypto universe=0 (exchange failures), stocks market closed. Best long-watch: SENT (pullback trigger) or HYPE (pullback after catalyst). Best short-watch: QQQ or PLTR at RTH open. Best catalyst-watch: HYPE (wait_pullback). Both sides require confirmation before entry.

---

## 9. Avoid / No Trade

- **SMCI LONG:** AVOID. Stale swing B-tier signal + $7B dilution + SEC legal risk. Signal generated pre-announcement.
- **SMCI SHORT:** Wait for RTH confirmation. -20% gap partially priced; avoid chasing on Europe open.
- **UNH LONG:** AVOID. DOJ criminal probe overrides swing B-tier signal. Legal risk confirmed.
- **New crypto intraday longs:** 0W/7L mode (§14), exchange failures (universe=0), risk-off regime. No clear RS-leader visible in fresh run.
- **Stocks B-tier shorts before 16:30 EEST:** All pre-market. Require RTH confirmation. Do not treat pre-market trigger as actionable entry now.
- **CHZ new entry:** NO. World Cup starts June 11. Sell-news risk. Position already tp_hit. Sell remaining exposure.
- **STRAX/BABY (momentum_breakout basket):** avoid_chase playbook explicitly. Do not enter.

*"No clean trade this window" applies only to new entries in this 4-hour block. Scanning, tracking, data collection, and monitoring continue normally.*

---

## 10. Main Risks

1. **Iran escalation** — BTC tested $62.9K overnight; further strikes could push below $62K. BTC $62K = James Wynn liquidation level (4× liquidated at $62,314 = heavily contested). Critical support.
2. **CHZ sell-news June 11** — World Cup kickoff TOMORROW. "Buy the rumor, sell the kickoff" historical pattern (-30–50% at kickoff). Any CHZ exposure must be managed today.
3. **Exchange data degradation** — Fresh crypto reports show universe=0, ohlcv_fetched=0 across all exchanges. Altcoin signals (SENT, HYPE, etc.) are invisible until new scheduler Cycle 1 completes (~12:20 EEST). Acting on swing report data (7.5h old) carries stale-level risk.
4. **SMCI/UNH legal shocks** — Both stocks B-tier signals in DB have confirmed LEGAL/HEADLINE RISK. Neither should be treated as actionable without manual review. Contagion risk if other healthcare or AI-hardware stocks face similar scrutiny.
5. **Stocks shorts structural issue** — Stocks shorts: PF=0.44, -42R overall. Yet multiple B-tier shorts have triggered. The playbook audit (PF 9.00 for RTH shorts) and the signal-stats (-42R) are in contradiction (see §14). Entering short without understanding this divergence adds risk.
6. **Intraday crypto 0W/7L** — Crypto intraday mode broken (§14 TODO). Avoid new intraday crypto entries until resolved.
7. **Social/crowd blind spot** — Reddit 403 persistent. KOL watchlist empty. Zero social sentiment.

---

## 11. Action Plan — next 4 hours (11:52–15:52 EEST)

1. **CHZ:** If any partial position remains after TP1 — EXIT before June 11 kickoff. Hard time-stop today. Do not hold past EU pre-market June 11.
2. **HYPE:** Monitor for pullback. Do NOT enter on current spike. Trigger = HYPE -7–12% from announcement high + volume dry + BTC stable > $62K. New scheduler OHLCV needed.
3. **SENT:** Watch for pullback to 0.0162–0.0166. Trigger = 1h candle hold inside zone + BTC above $62K. VERIFY levels with new scheduler output at ~12:20 EEST.
4. **BTC:** Watch $62K. 1h close below $62K = deepen risk-off; tighten all longs; QQQ short conviction rises.
5. **New scheduler:** Wait for Cycle 1 output (~12:20 EEST). Exchange data should recover. Check if SENT, HYPE, HAEDAL, STG, MORPHO levels update cleanly.
6. **Stocks pre-market prep:** Build the short-side watchlist for 16:30 EEST open. Focus: QQQ (broad confirmation), PLTR (highest individual score). DO NOT enter before RTH. For long side: XLV (healthcare sector RS +8.37%), SMCI long only after legal/dilution manual review.
7. **SMCI:** No action. Monitor for RTH open reaction. If gap-down continues and no bounce → C-tier short may become actionable. But wait first 30 min.

---

## 12. Final Verdict per Mode

| Mode | Asset Class | Verdict |
|---|---|---|
| **Scalp** | Crypto | **No active trade.** PF=0.14. Data severely degraded (universe=0). Only BTC/ETH from cache; too thin for scalp. |
| **Intraday** | Crypto | **No new entries.** 0W/7L mode broken (§14). Exchange failures. Risk-off regime. Monitor BTC $62K; no RS-leader visible in fresh data. |
| **Swing** | Crypto | **SENT B swing: best long-watch** (pullback 0.0162–0.0166, verify with new scheduler). HYPE catalyst-backed watch (wait_pullback, needs fresh levels). CHZ: EXIT remaining exposure before June 11. Swing is only profitable bucket (PF=5.0, +16R historically — carry-forward from swing report). |
| **Intraday** | Stocks | **Pre-market only.** Wait for 16:30 EEST RTH open. QQQ + PLTR best B-tier short candidates. XLV long if healthcare RS continues. SMCI/UNH: AVOID (legal risk). |
| **Swing** | Stocks | **Watchlist only (audit mode: -12R, 0W/12L).** SMCI swing B-long = STALE + LEGAL RISK → avoid. UNH swing B-long = DOJ probe → avoid. LLY swing B-long at 66.27 (no legal flag currently — viable for research but watchlist-only audit mode). |

---

## 13. Sources

- [Super Micro stock plunges after $7B capital raise — Cryptopolitan](https://www.cryptopolitan.com/super-micro-stock-drops-7-billion-raise/) — single_source, confirms June 10 price drop
- [SMCI Stock Falls 20% on $7B Equity Raise — FX Leaders](https://www.fxleaders.com/news/2026/06/09/smci-stock-falls-20-on-proposed-7-billion-equity-raise-while-buyers-fail-at-resistance/) — single_source, confirms -20% on June 9
- [SMCI Plans $7B Equity Raise for AI Equipment — GuruFocus](https://www.gurufocus.com/news/8908818/smci-plans-7-billion-equity-raise-for-ai-equipment) — single_source, confirms use of proceeds
- [Super Micro Computer Form FWP FY2026 — SEC EDGAR](https://www.sec.gov/Archives/edgar/data/0001375365/000119312526264046/d53641dfwp.htm) — primary_source, equity offering filing
- [UnitedHealth Faces DOJ Probe, Shares Dive 16% — QuiverQuant](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe,+Shares+Dive+16%25+on+Fraud+Investigation) — single_source, confirms DOJ probe and -16% share price
- [UnitedHealth under criminal probe for possible Medicare fraud — Yahoo Finance / WSJ](https://finance.yahoo.com/news/unitedhealth-under-criminal-probe-possible-231729520.html) — primary_source, confirms DOJ criminal probe
- [Grayscale launches lowest-fee Hyperliquid ETF — CoinDesk, June 3 2026](https://www.coindesk.com/markets/2026/06/03/grayscale-launches-lowest-fee-u-s-hyperliquid-etf-as-competition-heats-up-around-hype) — primary_source, confirms Grayscale HYPG ETF
- [Hyperliquid HYPE Surges Amid Bitwise ETF Launch and Coinbase Integration — KuCoin](https://www.kucoin.com/news/flash/hyperliquid-s-hype-token-surges-6-5-amid-bitwise-etf-launch-and-coinbase-integration) — single_source, confirms Coinbase integration + 6.5% surge
- [HYPE ETF Debut 2026: Record Market Cap Absorption — SpotedCrypto](https://www.spotedcrypto.com/hype-etf-debut-market-cap-record-2026/) — single_source, confirms ETF market impact
- [Bitcoin is cratering but HYPE is rising — CNBC, June 6 2026](https://www.cnbc.com/2026/06/06/bitcoin-price-crash-crypto-hype-hyperliquid-etfs.html) — single_source, confirms HYPE vs BTC divergence narrative
- [Bitcoin Falls Below $63,000 as Iran-Israel Conflict Reignites — Memeburn](https://memeburn.com/bitcoin-falls-below-63000-as-iran-israel-conflict-reignites/) — single_source, confirms BTC price drop on Iran news
- [Crypto Prices Today: Bitcoin Holds $63,210 Amid Iran-Israel Ceasefire — AnalyticsInsight](https://www.analyticsinsight.net/price-analysis/crypto-prices-today-bitcoin-holds-63210-solana-jumps-244-xrp-gains-231-amid-iran-israel-ceasefire) — single_source, June 10 price snapshot
- [Trump Strikes Iran Amid Fragile Ceasefire: Bitcoin, Gold, Oil React — BeInCrypto](https://beincrypto.com/united-states-attacks-iran-bitcoin-gold-oil-june-2026/) — single_source, confirms June 10 macro context
- [FIFA World Cup 2026 kicks off June 11, fan tokens eye breakout — CryptoBriefing](https://cryptobriefing.com/world-cup-2026-crypto-fan-tokens/) — single_source, confirms June 11 kickoff date
- [Will Chiliz Price Repeat 2022 Boom-and-Bust in 2026? — CCN](https://www.ccn.com/analysis/crypto/chiliz-price-analysis-chz-prediction-world-cup-2026-rally/) — single_source, confirms historical pattern + ~$0.044 price context
- Internal: `data/reports/scalp/2026-06-10_08-26_scalp_report.md`, `data/reports/intraday/2026-06-10_08-27_intraday_report.md`, `data/reports/swing/2026-06-10_01-28_swing_report.md`, `data/reports/stocks/intraday/2026-06-10_08-29_stocks_intraday_report.md`, `data/reports/stocks/swing/2026-06-10_01-31_stocks_swing_report.md`

---

## 14. Fix Requests / TODO

### TODO-intraday-0wins *(carried from 04:39 — unresolved)*
- **issue:** Crypto intraday mode shows 0 wins / 7 losses (PF=0.00, totalR=−7R) in signal-stats by-mode (mode3: n=45, stronger, trig=30, wins=0, losses=7, avgR=-0.23). Still present at 11:52 review.
- **evidence:** `signal-stats --asset-class crypto` by-mode output, mode3 row; also flagged in scalp/intraday reports "14d no-news cut: WR 23% / PF 0.70 / -3R"
- **suggested manual fix:** Audit which playbook / no-catalyst intraday sub-bucket drives the 0W/7L. Consider requiring verified catalyst for intraday to reach B-tier. Review `crypto_intraday_catalyst_or_momentum` playbook threshold.
- **priority:** high
- **first observed:** 2026-06-10 04:39 EEST | **still present:** 2026-06-10 11:52 EEST

### TODO-stocks-atier-broken *(carried from 04:39 — unresolved)*
- **issue:** Stocks A-tier: 1W/12L, PF=0.08 (n=18, weak confidence). Structural regression.
- **evidence:** `signal-stats --asset-class stocks` by-tier: tier=A, n=18, wins=1, losses=12, PF=0.08, stopR=1.00
- **suggested manual fix:** Audit 12 losing A-tier stock signals — check RTH vs after-hours triggering, earnings risk missed, scoring over-fit. Confirm A-tier stocks respect RTH session gate.
- **priority:** high
- **first observed:** 2026-06-10 04:39 EEST | **still present:** 2026-06-10 11:52 EEST

### TODO-stocks-shorts-structural-loss
- **issue:** Stocks shorts overall: PF=0.44, -42R (all tiers, n=149 triggered). Yet playbook audit shows `stocks_intraday_rth_momentum` shorts subset PF=9.00. Major contradiction.
- **evidence:** `signal-stats --asset-class stocks` by-direction: short row (n=202, trig=149, wins=21, losses=72, PF=0.44, totalR=-42R). vs `llm_stocks_packet.md` playbook table: `stocks_intraday_rth_momentum` status=actionable, shorts subset PF=9.00.
- **suggested manual fix:** Investigate the population difference. The -42R likely includes C-tier and after-hours triggered signals. The PF=9.00 may be from RTH-only manually confirmed shorts. Align the signal-stats filter to show only RTH-triggered A/B shorts, and validate whether the playbook audit figure is current.
- **priority:** high
- **first observed:** 2026-06-10 11:52 EEST

### TODO-exchange-api-degradation
- **issue:** Fresh scalp and intraday reports (11:26–11:27 EEST) show universe=0 for all exchanges (Binance failed=1, Bybit failed=54, MEXC failed=54). Only BTC+ETH from cache reached deep analysis. All altcoins invisible.
- **evidence:** `data/reports/scalp/2026-06-10_08-26_scalp_report.md` §0: "binance: universe=0, ohlcv_fetched=0, failed=1; bybit: universe=0, failed=2; mexc: universe=0, failed=2" (scalp); intraday: bybit failed=54, mexc failed=54.
- **suggested manual fix:** The degradation is likely API rate limit exhaustion across the old scheduler's 12-cycle run. The new scheduler should recover. But add a health-check alert if universe=0 persists beyond Cycle 2. Also confirm exchange API rate limits are not being hit by concurrent requests across cycles.
- **priority:** medium
- **first observed:** 2026-06-10 11:52 EEST

### TODO-reddit-403-persistent *(carried from 04:39)*
- **issue:** Reddit social sources return 403 on every cycle. Social crowd context completely absent.
- **evidence:** Persistent across multiple cycles, multiple reviews.
- **suggested manual fix:** Replace Reddit JSON API with Reddit OAuth, Pushshift, or extend Telegram channel monitoring.
- **priority:** medium
- **first observed:** recurring; confirmed present 2026-06-10 11:52 EEST

### TODO-catalyst-mapping-visibility *(carried from 04:39)*
- **issue:** Catalyst mapping % (mapped vs null-symbol events) not surfaced in CLI output or cycle summary.
- **evidence:** Cycle output only shows total event count, not mapped/unmapped split.
- **suggested manual fix:** Add `mapped=X, unmapped=Y` to catalyst scan CLI stdout.
- **priority:** low
- **first observed:** 2026-06-10 04:39 EEST | **still present:** 2026-06-10 11:52 EEST

### TODO-telegram-parsemode-400 *(carried from 04:39)*
- **issue:** TelegramNotifier defaults to parse_mode="Markdown" causing 400 errors on review messages containing brackets/dashes.
- **evidence:** `src/notifiers/telegram.py` line 58.
- **suggested manual fix:** Change default to parse_mode="" or use parse_mode="HTML" with safe escaping.
- **priority:** medium
- **first observed:** 2026-06-10 04:39 EEST | **still present:** 2026-06-10 11:52 EEST
