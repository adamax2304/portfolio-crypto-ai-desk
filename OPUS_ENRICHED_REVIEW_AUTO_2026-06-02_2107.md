# OPUS Enriched Market Review — Auto Run

- **Generated:** 2026-06-02 ~21:07 EEST (auto-enriched-review, 20:30 EEST firing)
- **Scheduler cycle reviewed:** `2026-06-02_default_schedule` — latest cycle `cycle_01_19-49` (scheduler.log mtime 20:30:46 EEST, ~27 min before this run → **healthy**, not stale)
- **Mode coverage:** crypto scalp + intraday (fresh), crypto swing (~3 h old), stocks intraday (fresh), stocks swing + invest (~3 h old). Tuesday = weekday → stocks in scope.
- **Web research:** WebSearch + WebFetch loaded and used (≥1 search + ≥1 fetch per candidate). Two article fetches (StockStory NVDA, GuruFocus/TheStreet AMD) returned **HTTP 403**; those claims are carried from the search-result summary and a substitute fetched source, flagged below.
- **Chart tools:** `mcp__Claude_in_Chrome__*` NOT loaded — **TradingView manual chart check unavailable.** No chart observations are fabricated; price/structure come from local OHLCV report fields only.

---

## 1. Executive Summary

- **Crypto = no-trade.** Regime is **high-volatility danger** (BTC & ETH downtrend, BTC ATR at 100th percentile, breadth 33% > EMA20). Zero A-tier and zero B-tier crypto setups across scalp + intraday. Best name is **XLM** at only 60.6/100 — watchlist, not active.
- **Macro driver is BTC breaking < $70K** (~$69.4K, first time in ~2 months) on Strategy's first BTC sale in ~4 years + an **11-session record ETF outflow streak of ~$3.4B** + Mt. Gox transfers. Sell-side (Tom Lee) calls it "bottom behavior / immaterial," but the tape is risk-off — confirmed externally.
- **Stocks = bullish, risk-on** (VIX ~16, 4/4 indices uptrend, breadth 100% > EMA20, SMH/XLK leading). Two **A-tier swing longs: NVDA (83.8) and AMD (81.8)** — both leaders, news-backed, earnings-safe.
- **NVDA catalyst confirmed:** Computex keynote (RTX Spark PC chip, Vera Rubin in full production), Goldman Buy / **$285 PT**, +6.3% intraday. **AMD** carries fresh analyst upgrades (**Barclays $665, Mizuho $615, TD Cowen $600**).
- **Two avoid flags:** **AVGO** reports earnings next session (Jun 3) → swing-blocked; **SMCI** (B-tier, RS +71%) carries an active DOJ export-control / smuggling-indictment + auditor-resignation overhang — momentum is real but it is *not* a clean A-tier-quality long.
- **RR caveat (system-wide):** every stock idea shows **RR-to-TP1 ≈ 1.0** (below the 1.5 guideline). These are trend-continuation/structure plays, not high-RR setups — size accordingly.

---

## 2. Data Used

**Internal (read):**
- `data/reports/scalp/2026-06-02_17-06_scalp_report.md` (fresh, 20:06 EEST)
- `data/reports/intraday/2026-06-02_17-21_intraday_report.md` (fresh, 20:21 EEST)
- `data/reports/swing/2026-06-02_14-55_swing_report.md` (~3 h old; window-2 refresh — usable)
- `data/reports/stocks/intraday/2026-06-02_17-40_stocks_intraday_report.md` (fresh, 20:40 EEST)
- `data/reports/stocks/swing/2026-06-02_15-03_stocks_swing_report.md` (~3 h old)
- `data/reports/stocks/invest/2026-06-02_15-08_stocks_invest_report.md` (~3 h old)
- `data/catalysts/2026-06-02/catalyst_cycle_17-21.md` + `catalyst_events.jsonl` (500 rows) + `narrative_baskets.jsonl` (4 baskets)
- CLI: `active-signals` (crypto: 6 active, all B/C; stocks: 50 active incl. NVDA-A, AMD-A), `signal-stats` (crypto/stocks), `detect_untracked_legacy_alerts --since 2026-06-02`.

**External (this run):** CoinDesk ×3, CryptoNews, Yahoo Finance, StockStory, GuruFocus, TheStreet, The Motley Fool — see §10 Sources. Ingested via `ingest_enriched_review_sources` → 4 crypto rows + 5 stocks rows written to `news_items`.

**Unavailable / degraded:**
- TradingView / Chrome chart verification — unavailable (tool not loaded).
- Social attention: **missing** (Reddit Crypto/BTC/ETH sources failing; no live X/Telegram/Discord/KOL feed — manual only).
- RSS partial failures: The Block, Reuters Business, SEC EDGAR.
- Stocks earnings calendar lookup failed for ETFs (SPY/QQQ/IWM/DIA/SMH/XLK…) → SMH/XLK carry **UNKNOWN earnings** flag.
- StockStory(NVDA) + GuruFocus/TheStreet(AMD) article fetches 403'd; substitute Yahoo fetch covered NVDA; AMD analyst targets carried from search summary (single_source).
- Swing/invest data is **~3 h old** (16:04 EEST window-2 refresh) — fresh enough this run; not the stale carry-forward case.
- `detect_untracked_legacy_alerts`: **clean** — every legacy crypto alert has a backing proposed_signal (no PART 1 regression).

---

## 3. Per-Cycle Landscape

### Crypto regime — high-volatility danger
- BTC trend **downtrend**, ETH **downtrend**; BTC ATR percentile **100** (state: elevated); breadth **33.3% > EMA20 / 36.7% > EMA50**.
- Recommended style: *"reduce size or no trade until structure settles."*
- Money flow (momentum, NOT actionable in this regime): CHIP, ICP, PORTAL (+16–22%), ZEC (+10.6%, Orchard vuln hard-fork catalyst), ONDO. Weakest: **XLM −13.5%**, MEME −9%, BTC −5.8%.
- Narrative baskets: `ai_narrative` (NEAR/RENDER/TAO/FET, related-beta), `rwa_narrative` (ONDO/XLM), `perps_dex_narrative` (HYPE), `momentum_breakout` (PORTAL/ZEC — no confirmed catalyst).
- Derivatives: mostly short-covering (price-up/OI-down) on the gainers → weak continuation quality; XLM/MEME show price-down/OI-up (fresh shorts pressing).
- **Verdict: every long "conflicts with current market regime" — system correctly forces no-trade.**

### Stocks regime — bullish / risk-on
- VIX **15.95**; SPY/QQQ/IWM/DIA all uptrend (QQQ 20d **+10.55%**); breadth **100% > EMA20 & EMA50**.
- Sector leaders: **semiconductors SMH (RS +17.4%), technology XLK (+15.8%)**. Laggards: utilities, energy, staples.
- A/B-tier longs cluster in semis/megacap tech (NVDA, AMD, AAPL, SMCI, SMH, XLK). No short makes it through (all "short_in_bullish_regime").
- Stocks signal-stats (week, reliable, n=627): triggered winrate **18.7%**, avg R **0.12**, PF **1.68** — note **A-tier slice is negative (PF 0.27, −8R)** over this window: A-tier label ≠ guaranteed edge; treat conviction as directional, manage risk.

---

## 4. Candidate Deep Dives

### 4.1 NVDA — stocks A-tier (swing 83.8 / intraday B 77.4 / invest B 79.8) — **TOP PICK**
- **Internal verdict (pre-web):** A-tier swing long, leader RS, bullish regime, earnings-safe. Entry **221.58–225.64**, invalidation **close < 213.46**, TP1 **237.82** / TP2 245.95 / TP3 258.13 (RR-to-TP1 ~1.0).
- **External (confirms):** Computex 2026 keynote — **RTX Spark** PC superchip (Blackwell GPU, MediaTek Arm CPU, fall-2026 launch w/ Microsoft/Dell/HP/ASUS/Lenovo/MSI) and **Vera Rubin** platform in **full production** (OpenAI, Anthropic, xAI, Oracle, CoreWeave as early customers). Stock **+6.3%** on the session. **Goldman (J. Schneider) Buy, $285 PT** (~35% upside); cash dividend $0.25, ex-date Jun 4 2026. [Yahoo Finance, 2026-06-02 — fetched]
- **verification_status:** single_source (multiple reputable outlets corroborate; Computex is a primary public event).
- **Net:** External research *strengthens* the internal A-tier. Cleanest swing long on the desk. Only knock: RR-to-TP1 ~1.0 → use scale-outs, trail to structure.

### 4.2 AMD — stocks A-tier (swing 81.8 / intraday B 73.7 / invest B 78.0)
- **Internal verdict:** A-tier swing long, **RS vs SPY +42.65%**, RS vs sector +24.86% (strongest RS leader in the set), earnings-safe. Entry **493.27–507.05**, invalidation **< 465.72**, TP1 **548.38** / TP2 575.93 / TP3 617.26.
- **External (confirms):** Fresh post-rally analyst upgrades — **Barclays Overweight, PT $665** (from $500, 2026-06-01); **Mizuho $615** (from $515, Outperform); **TD Cowen $600** (from $500, Buy). Consensus "Strong Buy," avg PT ~$480 (lagging the rapid re-rating). Driver: AMD CPU share gains + portfolio breadth. [GuruFocus/TheStreet/MarketBeat — search summary; article fetches 403'd]
- **verification_status:** single_source (analyst actions; primary article fetch blocked → carried from search snippet, flagged).
- **Net:** Strong RS + fresh upgrade tape support the A-tier. Caveat: most extended of the megacaps after a "massive rally" — entry discipline (wait for the 493–507 zone) matters; don't chase.

### 4.3 SMCI — stocks B-tier (intraday 71.0 / swing 69.0) — **legal-risk check**
- **Internal verdict:** B-tier long, momentum leader **RS vs SPY +71–73%**, above prior-day high, earnings-safe. Entry (intraday) 48.99–49.55, inval < 47.89.
- **External (caution):** Active overhang — DOJ export-control investigation; **March 2026 smuggling indictment** of 3 individuals incl. co-founder Liaw (**SMCI itself NOT named as a defendant**, placed individuals on leave); securities-fraud lawsuits; adverse internal-control audit opinions FY24/FY25; **Ernst & Young auditor resignation**; prior 2018 SEC accounting fine ($17.5M). Q3 FY26 sales $10.24B (doubled YoY but ~17% below consensus). [The Motley Fool, 2026-03-20 — fetched; StocksToTrade]
- **verification_status:** single_source.
- **Net:** Momentum is genuine, but governance/legal tail risk makes this a *reduced-size, headline-sensitive* B — not interchangeable with the clean A-tier semis. Any fresh DOJ/SEC headline is a gap-down catalyst.

### 4.4 BTC/USDT — macro anchor (fresh Telegram + RSS news)
- **Internal verdict:** bias short / weakest-symbol list, −5.8% 24h; drives the whole crypto danger regime. Multiple t.me catalysts (lookonchain ETF netflow −7,042 BTC/−$483.6M 1D; WalterBloomberg "< $70K").
- **External (confirms):** BTC **below $70K (~$69.4K), first time in ~2 months**. Strategy sold **32 BTC @ ~$77,135 (~$2.5M)** — first sale in ~4 years, **0.004%** of 843,700 BTC; framed by Saylor as a liquidity demonstration. **11 straight sessions of US spot-BTC-ETF outflows ≈ $3.4–3.45B** (longest streak since Jan-2024 launch). Mt. Gox-linked wallet transfers + geopolitics added risk-off. **Tom Lee** (Bitmine): "bottom behavior," economically immaterial. CoinDesk daybook: slide "may have more to do with AI than Strategy's sale." [CoinDesk ×3, CryptoNews — 2026-06-02; primary fetched]
- **verification_status:** single_source (broad corroboration).
- **Net:** Confirms the danger regime is real, not a data glitch. No long until BTC reclaims structure; the only crypto edge here would be continuation-short discipline, which the system already declines to size in this volatility.

### 4.5 XLM/USDT — best crypto watchlist (60.6) — "buy-rumor-sell-news" check
- **Internal verdict:** best watchlist name but **below active threshold**; −13.5% 24h yet +51% 7d; volume only 0.05–0.22x (no confirmation); short bias, price-down/OI-up (fresh shorts). Catalysts flagged (Stellar/CLARITY, MoneyGram).
- **External (explains the dump):** **MoneyGram launched MGUSD**, a USD stablecoin, **on Stellar** Jun 2 (partners Bridge/Stripe as issuer, M0 smart contracts, Fireblocks wallets; 60M customers / ~500k retail locations). Bullish fundamental, but **XLM fell ~14% to ~$0.2319 on the day** — classic unwind of the late-May surge / sell-the-news, not a fundamental break. [CoinDesk, 2026-06-02 — fetched; BanklessTimes/BeInCrypto]
- **verification_status:** single_source.
- **Net:** Real catalyst, wrong tape. Below-average volume + danger regime = **watch only**; do not catch the knife. The system's conditional short levels are defensible but sub-threshold.

---

## 5. Best Candidates (ranked)

1. **NVDA long (swing A, 83.8)** — cleanest setup: leader RS, confirmed Computex catalyst, Goldman $285, earnings-safe. Entry 221.58–225.64; inval < 213.46; TP1 237.82.
2. **AMD long (swing A, 81.8)** — strongest RS (+42.6% vs SPY) + fresh $600–665 analyst targets; wait for 493–507 zone, don't chase. Inval < 465.72; TP1 548.38.
3. **AAPL long (intraday/swing B, ~76/66.6)** — leader RS, above prev-day high, earnings-safe; secondary megacap long. Entry ~313.5–314.6 (intraday).
4. **SMH / XLK long (B)** — sector-ETF expressions of the same semis/tech leadership; lower single-name risk, but UNKNOWN earnings flag on the ETFs.

(All carry RR-to-TP1 ≈ 1.0 → trend-continuation plays, scale out / trail.)

## 6. Avoid / No-Trade

- **All crypto longs** — regime conflict (high-vol danger). Momentum names (CHIP/PORTAL/ZEC/ICP) are short-covering pops, not entries.
- **XLM** — fundamental catalyst but −14% knife on sub-average volume; watch only.
- **SMCI oversized** — legal/DOJ/auditor overhang; if traded, reduced size + headline stop only.
- **AVGO** — **earnings next session (Jun 3)** → swing-blocked; C-tier with −16 penalty intraday.
- **Index/megacap shorts** (UNH, MSTR, META, NFLX, COIN…) — all "short_in_bullish_regime," correctly rejected.

## 7. Main Risks

1. **Crypto contagion into risk assets** — record BTC-ETF outflow streak + Mt. Gox movements; if equities catch the risk-off (VIX is calm at ~16 *for now*), the semis longs lose their regime tailwind fast.
2. **Stocks A-tier statistical caveat** — A-tier slice is net-negative this week (PF 0.27, −8R, n=43). Tier label is not a guarantee; manage every position to invalidation.
3. **Universal low RR (~1.0 to TP1)** — thin reward vs risk; a single stop wipes multiple winners. Scale-outs mandatory.
4. **SMCI / AVGO event risk** — DOJ headline (SMCI) or earnings gap (AVGO) can blow through stops overnight.
5. **Blindspots** — no social/on-chain/liquidation/ETF-flow automation; no live chart verification this run; ETF earnings-calendar gaps (SMH/XLK "unknown").

## 8. Action Plan — next 4 hours

- **Crypto:** stand down. No fresh entries in danger regime. Monitor BTC for either a reclaim of ~$70K (structure repair) or continuation toward the $65–69K zone flagged by external desks. Re-evaluate next scheduler cycle.
- **Stocks (if US session active):** treat **NVDA** as primary swing long *on a pullback into 221.58–225.64* (not chase); **AMD** secondary, only in 493–507. Keep stops at stated invalidations. **No SMCI** unless reduced size + you accept headline risk. Avoid AVGO into earnings.
- **Hygiene:** social/Reddit sources failing — don't infer crowd positioning this run. Chart-verify NVDA/AMD manually before any live entry (tool not available to this auto-run).

## 9. Final Verdict (per mode + overall)

- **Crypto scalp:** NO-TRADE. Best name XLM 60.6 (watch). Danger regime.
- **Crypto intraday:** NO-TRADE. Best name XLM 59.5 (watch).
- **Crypto swing (~3 h old, fresh enough):** NO-TRADE; no A/B. Carry-forward bias = risk-off under BTC < $70K.
- **Stocks intraday:** Selective long — NVDA/AAPL/AMD B-tier on pullback; bullish regime.
- **Stocks swing (~3 h old):** **Long — NVDA (A) & AMD (A)** the two highest-conviction names on the desk.
- **Stocks invest (~3 h old):** Same leaders as B-tier long (NVDA 79.8, AMD 78.0); multi-week semis/AI thesis intact.
- **Overall:** **Risk-off in crypto, risk-on in stocks.** Capital belongs in the semis/AI swing longs (NVDA, AMD) with disciplined entries and invalidations; crypto is a spectator until BTC structure repairs. Swing data was fresh this run (~3 h, window-2) — the NVDA/AMD A-tier calls are *not* stale carry-forward.

---

## 10. Sources

**Crypto / macro (all 2026-06-02):**
- [Tom Lee dismisses bitcoin fears over Saylor's first sale and ETF outflows — CoinDesk, 2026-06-02](https://www.coindesk.com/markets/2026/06/02/tom-lee-dismisses-bitcoin-fears-over-michael-saylor-first-bitcoin-sale-and-etf-outflows) *(fetched)*
- [Bitcoin's biggest ETF selloff yet hits $3.4 billion as AI stocks keep climbing — CoinDesk, 2026-06-02](https://www.coindesk.com/markets/2026/06/02/bitcoin-s-biggest-etf-selloff-yet-hits-usd3-4-billion-as-ai-stocks-keep-climbing)
- [Bitcoin's slide may have more to do with AI than Strategy's sale — CoinDesk Daybook, 2026-06-02](https://www.coindesk.com/daybook-us/2026/06/02/bitcoin-s-slide-may-have-more-to-do-with-ai-than-strategy)
- [Crypto News, June 2: Bitcoin Flash Crashes Below $70K, Saylor Explains Strategy Sale — CryptoNews, 2026-06-02](https://cryptonews.com/news/crypto-news-june-2-bitcoin-price-flash-crashes-below-70k-saylor-explains-strategy-sale-trump-saving-bibis-ass/)
- [MoneyGram launches stablecoin on Stellar (XLM) — CoinDesk, 2026-06-02](https://www.coindesk.com/business/2026/06/02/moneygram-launches-stablecoin-on-stellar-joining-rush-toward-digital-dollar-payments) *(fetched)*

**Stocks (2026-06-01/02):**
- [Why a massive Nvidia stock rally may be just getting started (Goldman $285 PT; Computex/Vera Rubin/RTX Spark) — Yahoo Finance, 2026-06-02](https://finance.yahoo.com/sectors/technology/article/why-a-massive-nvidia-stock-rally-may-be-just-getting-started-130659463.html) *(fetched)*
- [Why Is Nvidia (NVDA) Stock Soaring Today — StockStory, 2026-06-02](https://stockstory.org/us/stocks/nasdaq/nvda/news/why-up-down/why-is-nvidia-nvda-stock-soaring-today-4) *(fetch 403 — carried from search summary)*
- [AMD Maintained by Barclays — PT Raised to $665 (from $500, Overweight) — GuruFocus, 2026-06-01](https://www.gurufocus.com/news/8894301/amd-maintained-by-barclays-price-target-raised-to-66500) *(fetch 403 — carried from search summary)*
- [Analysts turn heads with AMD stock forecast after massive rally (Mizuho $615, TD Cowen $600) — TheStreet, 2026-06-02](https://www.thestreet.com/investing/stocks/analysts-turn-heads-with-amd-stock-forecast-after-massive-rally) *(fetch 403 — carried from search summary)*
- [AMD Stock Forecast & Price Target 2026 (consensus) — MarketBeat](https://www.marketbeat.com/stocks/NASDAQ/AMD/forecast/)
- [Super Micro Has Now Faced SEC Probes, Accounting Scandals, and Smuggling Charges — The Motley Fool, 2026-03-20](https://www.fool.com/investing/2026/03/20/super-micro-has-now-faced-sec-probes-accounting-sc/) *(fetched)*
- [Indictment Leads to Super Micro's Stock Fall Amid SEC Investigation — StocksToTrade, 2026-03-26](https://stockstotrade.com/news/super-micro-computer-inc-smci-news-2026_03_26/)

*§14 compliance: every external claim carries title + source + date + URL; no fabricated chart observations (chart tools unavailable, stated up top); `test_source` rows filtered by the ingest pipeline (0 rejected); 403-blocked fetches explicitly flagged and downgraded to search-summary sourcing.*
