# OPUS Enriched Market Review — AUTO

**Generated:** 2026-06-02 ~18:10 EEST (auto-enriched-review, fires ~25 min after default scheduler cycle)
**Cycle reviewed:** default schedule, latest cycle (crypto intraday data 14:15 UTC / stocks data 14:42–15:08 UTC; reports written ~17:33–18:08 EEST)
**Mode coverage:** crypto scalp + intraday + swing; stocks intraday + swing + invest (Tuesday = weekday, stocks active)
**External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim below carries title + source + date + URL (see Sources).
**Chart tools:** TradingView / Chrome MCP **NOT loaded** — no chart observations are fabricated; structure read from local OHLCV report fields only.

---

## 1. Executive Summary

- **Two markets, opposite tapes.** US equities are cleanly **bullish** (VIX ~16, 4/4 indices up, breadth 100% > EMA20, semis +23% / tech +21% 20d). Crypto is **risk-off**: BTC broke **below $70K** for the first time since April 7 (~$69.5K, −4.5%), triggering ~$714–767M of liquidations.
- **Stocks A-tier is the only A-tier on the desk:** **NVDA** (intraday 87, swing 84) and **AMD** (swing 82, intraday 85 triggered). Both ride the Computex 2026 AI-semis catalyst. NVDA spot (~$226) sits *inside* its intraday entry zone right now.
- **Caveat that caps conviction:** the stocks A-tier historical track record is poor — triggered winrate **10%**, profit factor **0.36** (system flag). Treat A-tier as "lean long with semis," not "high-confidence print."
- **Crypto has zero fresh A/B-tier** this cycle — every fresh idea is watchlist/C-tier (best: NEAR 59.1). The 6 "active" crypto signals (JTO, INJ, ZEC, XLM, UNI) are carry-forward, not fresh re-confirmations.
- **Divergence trade in crypto:** AI tokens (NEAR +14.5%, WLD ~+12%, ICP ~+11%, Humanity Protocol +18%) bucked the BTC drop. NEAR has a real June catalyst (dynamic resharding) but is extended and BTC-beta.
- **XLM is a head-fake:** MoneyGram's MGUSD launched *on* Stellar, but it does **not** bid the XLM token — XLM fell **8.4%**, leading the CoinDesk 20 lower. Do not read the headline as bullish XLM.
- **Top macro risk = Iran/Strait of Hormuz headlines + Strategy's BTC-sale precedent.** Fresh Telegram (WalterBloomberg) wire traffic on Iran negotiations is live; any escalation flips equities risk-off fast.

---

## 2. Data Used

**Internal reports (read):**
- Crypto scalp — `data/reports/scalp/2026-06-02_11-39_scalp_report.md` (data 11:15 UTC; **~6h old** — older scalp cycle, treat as stale).
- Crypto intraday — `data/reports/intraday/2026-06-02_14-33_intraday_report.md` (data 14:15 UTC, fresh).
- Crypto swing — `data/reports/swing/2026-06-02_14-55_swing_report.md` (written 17:55 EEST, **fresh this run** — window-2 refresh, ~3h old, within 14h threshold).
- Stocks intraday — `data/reports/stocks/intraday/2026-06-02_14-42_stocks_intraday_report.md` (data 14:42 UTC, fresh).
- Stocks swing — `data/reports/stocks/swing/2026-06-02_15-03_stocks_swing_report.md` (fresh).
- Stocks invest — `data/reports/stocks/invest/2026-06-02_15-08_stocks_invest_report.md` (fresh).
- Catalyst cycle — `data/catalysts/2026-06-02/catalyst_cycle_14-34.md` + `catalyst_events.jsonl` / `narrative_baskets.jsonl` (341–512 events, 4 baskets).

**Internal CLI (run):**
- `active-signals --asset-class crypto` → 6 active (queried DB for clean values).
- `active-signals --asset-class stocks` → 50 active rows (NVDA/AMD A-tier present).
- `signal-stats --asset-class crypto` → n=23, weak sample, PF ~4.66 (directional only).
- `signal-stats --asset-class stocks` → n=672 reliable; **A-tier winrate 10%, PF 0.36** (system warning).
- `detect_untracked_legacy_alerts --since 2026-06-02` → **None** (no PART-1 regression; every legacy crypto alert has a backing proposed_signal).

**External (WebSearch + WebFetch, all dated — see Sources §11).**

**Unavailable / blindspots:**
- TradingView / chart MCP — not loaded (no chart reads).
- Social attention — missing (no live X/Telegram/Discord symbol-level feed; KOL watchlist still placeholder).
- Liquidation heatmaps, order-book depth/CVD, ETF flows, DXY/yields, on-chain whale flows, token-unlock calendar — still not automated.
- RSS partial failures this cycle: The Block, Reuters Business, SEC EDGAR Filings, CryptoSlate; Reddit social sources failing.
- Stocks earnings calendar lookup failed for SMH/XLK and the index ETFs (treat SMH swing as undated event risk; AVGO has earnings next session → swing-blocked).

---

## 3. Per-Cycle Landscape

### Crypto regime — RISK-OFF / high-volatility danger
- BTC trend **downtrend**, ETH **downtrend**; BTC ATR percentile **91–92** (elevated). Scalp regime = "high-volatility danger"; intraday = "range/chop." Recommended style: **reduce size or no trade until structure settles.**
- BTC **broke below $70K** (~$69.5K, −4.5%), lowest since April 7; ~$714–767M liquidated (CoinDesk, Decrypt — §11). Drivers: Strategy/Saylor's first BTC sale in ~4 years (32 BTC / $2.5M disclosed, plus $30M BTC moved to Coinbase Prime) + Mt. Gox transfer fears.
- Breadth deceptively firm (58% > EMA20) — propped by the AI-token rotation, not BTC.
- Narrative heat: **AI rising** (attention 100/100; NEAR/RENDER/TAO/FET), RWA mixed (ONDO/XLM), perps-DEX (HYPE) wait-pullback, momentum_breakout (EPIC/OPG/PARTI). Memes cooling (Solana DEX volume −82%).
- **No fresh A/B-tier.** Best fresh watchlist: NEAR 59.1 (intraday), RENDER 57.5, ONDO 57.1, XLM 57.6 (scalp, short-bias).

### Stocks regime — BULLISH / risk-on
- Label **bullish**, bias long, VIX **~16**, breadth **100%** > EMA20 & EMA50; SPY +5.7% / QQQ +10.5% 20d.
- Sector leadership: **semiconductors (SMH) +17.5% RS, technology (XLK) +15.7% RS**. Laggards: utilities, energy, consumer staples (defensive groups out of favor = clean risk-on).
- Event risk: **AVGO earnings next session** (swing-blocked). SMH/XLK earnings lookup missing (undated risk flag).
- A-tier: NVDA + AMD (both long, semis). B-tier: SMCI, SMH, XLK, AAPL, MSFT, TSLA. MSTR/LLY/NFLX/TSLA-short all rejected.

---

## 4. Candidate Deep Dives

### 4.1 NVDA — A-tier long (intraday 87 / swing 84 / invest B 80) — **PRIORITY**
- **Internal verdict (pre-web):** strongest name on the desk. Intraday A 87.02 (high conf), waiting_for_entry **226.32–228.01**, stop/inval **222.92**, TP1 233.11 / TP2 236.50 / TP3 241.59. Swing A 83.78, entry 221.58–225.64, stop 213.46, TP1 237.82. RS vs SPY +9.2% (20d). **Flag: intraday RR to TP1 is only 1.0** (< 1.5 minimum) — the swing structure has the better reward geometry.
- **External confirm:** Spot ~**$226.93** (Motley Fool, 2026-05-31) / traded $225–232 on June 2 — i.e. **price is sitting inside the intraday entry zone now.** Jensen Huang's **Computex 2026 keynote (June 1)** unveiled the RTX Spark chip, a fall "super PC chip" aimed at Intel/AMD, and the Vera Rubin platform ramping to full production; **Goldman Sachs (J. Schneider) reportedly reiterated Buy, $285 target** post-keynote (WebSearch aggregate — treat as single_source, not a primary filing). Dividend $0.25, ex-date Jun 4.
- **verification_status:** single_source (reputable outlets; Goldman target is reported-not-primary).
- **Net:** Confirm. Catalyst + leadership intact, price actionable. Conviction capped by (a) A-tier historical PF 0.36 and (b) thin 1.0 intraday RR. **Prefer the swing expression over the intraday for reward geometry.**

### 4.2 AMD — A-tier long (swing 82 / intraday 85 triggered / invest B 78) — **PRIORITY**
- **Internal verdict:** Swing A 81.79, entry 493.27–507.05, stop 465.72, TP1 548.38. Intraday A 85 **triggered** (entry 505.55–510.02, stop 496.61). **Important nuance:** in the *fresh* 14:42 intraday cycle, a new AMD intraday idea was **rejected / no_trade at 48.01** — the active A-tier intraday signal is a **carry-forward triggered position from an earlier cycle, not a fresh re-confirmation.** Manage, don't re-add.
- **External confirm:** AMD ~**$510–527**, **+138% YTD** on AI/data-center demand (FX Leaders, 2026-06-02). Consensus **Buy** (34 analysts, Jun 2); MI300-series accelerators now ~⅓ of data-center revenue, Q1 sales +38% to $10.3B. Note: published analyst price targets are **scattered and lagging** ($375 DA Davidson up to $665 high) — many sit *below* spot, i.e. the move has outrun the sell-side.
- **verification_status:** single_source.
- **Net:** Confirm trend, but **chase risk is the dominant danger** (price already extended +138% YTD and through the intraday entry). Respect the "do not enter >2 ATR from planned entry" gate. The swing zone (493–507) is the disciplined add-back, not current spot.

### 4.3 NEAR/USDT — crypto AI-narrative leader (watchlist 59.1 intraday) — fresh news
- **Internal verdict:** best fresh crypto name but **below threshold** — watchlist only. Intraday: 24h +12.25%, RS vs BTC +16.75%, uptrend, but volume only 0.25x (no volume confirmation), regime range/chop. Conditional pullback 2.634–2.669, inval 2.591, TP1 2.763. Swing scores 56.2 in high-vol-danger regime (risk penalty −17).
- **External confirm:** NEAR **+14.5% / 24h**, leading the AI-token rotation while BTC fell (CoinDesk, Decrypt, FXStreet — §11). Real catalyst: **dynamic resharding upgrade shipping in June** (auto-shard scaling + post-quantum-safe signing) per FXStreet. But the article explicitly notes NEAR is **"flat since midnight UTC following profit-taking."**
- **verification_status:** single_source.
- **Net:** Confirm narrative, **weaken timing.** Real catalyst, but extended, low-volume, BTC-beta, in a risk-off tape. Watch the 2.58–2.67 pullback zone; do not chase the +14% candle.

### 4.4 XLM/USDT — RWA-narrative headline, active B-tier swing — **contradiction found**
- **Internal verdict:** scalp report flags XLM **short-bias** (24h −10.7%, RS vs BTC −6.6%, downtrend), watchlist 57.6. An active B-tier *swing* signal exists (carry-forward).
- **External CONTRADICTS the bull read:** MoneyGram launched **MGUSD on Stellar** (CoinDesk, 2026-06-02) — real network adoption (Bridge/Stripe issuer, 60M users) — but the article confirms it gives **no direct economic benefit to the XLM token**, and **XLM fell 8.4%, leading the CoinDesk 20 lower.**
- **verification_status:** single_source (corporate launch + index print).
- **Net:** **Avoid XLM long.** The "RWA catalyst" is a network event, not a token bid; price action is weak/short-biased. If anything the system's short-bias read is the correct one.

### 4.5 Macro / BTC — Iran + Strategy precedent (dominant cross-asset risk)
- **Internal:** macro risk 27–45/100; headline "Bitcoin drops toward $69,000 as Saylor sale spooks investors." ETF netflows red (BTC 1D −$483M, ETH −$44M; SOL green via t.me/lookonchain).
- **External + fresh Telegram wire:** Strategy's first BTC sale in ~4 years (Saylor frames it as "economic arbitrage" / liquidity proof; proceeds met dividend obligations while staying a net buyer) — CoinDesk, cryptonews, blockhead (§11). Simultaneously, **live WalterBloomberg Telegram traffic (14:25–15:04 UTC)** on **Iran / Strait of Hormuz negotiations** (Rubio: "in talks with Iran," conditions on reopening Hormuz) and "BITCOIN SLIDES BELOW $70K AS BEARISH BETS BUILD."
- **verification_status:** mix — CoinDesk single_source; Telegram wire = **social_only** (treat as directional, unverified by primary).
- **Net:** This is the swing risk for BOTH books. Equities are ignoring it (VIX 16); a hard Iran/Hormuz escalation or a confirmed *larger* Strategy sale would flip that.

---

## 5. Best Candidates (ranked)

1. **NVDA long (swing expression)** — A-tier, semis leadership, Computex catalyst, price actionable. Best reward geometry on the swing zone (entry 221.6–225.6, stop 213.5, TP1 237.8). Lean long.
2. **NVDA long (intraday)** — same thesis, price *in* zone 226.3–228.0 now, but only 1.0R to TP1 — scalp-grade, tight management.
3. **AMD long (swing add-back only)** — A-tier trend intact but +138% YTD = chase risk; disciplined entry is the 493–507 swing zone, not spot. Intraday A is carry-forward, not fresh.
4. **NEAR/USDT (watchlist)** — best crypto momentum + real June catalyst, but sub-threshold, extended, low-volume, BTC-beta. Pullback-only.

No crypto candidate clears the active-trade threshold this cycle.

---

## 6. Avoid / No-Trade

- **XLM long** — headline ≠ token bid; XLM −8.4% and short-biased. Avoid (or respect system short-bias).
- **Chasing AMD / NVDA intraday > 2 ATR** above entry — both extended; the system's own "do not chase" gate applies.
- **New crypto longs broadly** — high-volatility danger regime + BTC sub-$70K breakdown. Best watchlist names lack volume confirmation.
- **MSTR** (rejected short, but headline-driven) — Strategy BTC-sale story is live; don't trade the noise.
- **AVGO swing** — earnings next session (swing-blocked).
- **Memecoins / Solana-DEX beta** — Solana DEX volume −82%, narrative cooling.

---

## 7. Main Risks

1. **Iran / Strait of Hormuz escalation** (live WalterBloomberg wire) — equities are priced for calm (VIX 16); a headline flip is the fastest path to risk-off across both books. *(social_only — unverified.)*
2. **Strategy / Saylor sale precedent** — a confirmed *larger* BTC sale would deepen the crypto liquidation cascade beyond the $69K April low.
3. **Stocks A-tier reliability** — historical triggered winrate 10% / PF 0.36. The A-tier label is a momentum/leadership read, not a validated edge; size accordingly.
4. **Chase risk** — NVDA and AMD both extended; entering late into AI-semis euphoria is the most likely way to take a stop.
5. **Data blindspots** — no chart confirmation, no liquidation heatmap, no live social; RSS/Reddit partial failures. Conviction should not be upgraded on imagined context.
6. **BTC/equity correlation flip** — if BTC's breakdown bleeds into Nasdaq risk appetite, the bullish stocks regime is the carry-forward assumption most at risk.

---

## 8. Action Plan — next 4 hours

- **NVDA:** primary watch. Spot ~$226 is inside the intraday entry (226.3–228.0). Look for clean acceptance + SPY/QQQ confirmation before treating intraday as live (1.0R only → scalp-grade). Favor the **swing** entry (221.6–225.6) for a real R-multiple. Inval 222.9 (intraday) / 213.5 (swing).
- **AMD:** triggered/carry-forward — **manage only, do not re-add at spot.** Disciplined add-back is the 493–507 swing zone. Stop 465.7 (swing) / 496.6 (intraday).
- **Crypto:** **no new longs** while BTC < $70K and regime = high-vol danger. NEAR is the only name worth a pullback bid (2.58–2.67) *if* BTC stabilizes and volume confirms — otherwise pass. Avoid XLM long.
- **Watch triggers:** BTC defense of the ~$69K April low (loss → risk-off accelerates); fresh Iran/Hormuz headlines; any new Strategy SEC filing; VIX break above ~18 (would invalidate the clean stocks-bullish read).
- **Posture:** lean long US semis (small, disciplined entries), flat/defensive crypto.

---

## 9. Final Verdict — per mode + overall

- **Crypto scalp:** NO-TRADE. High-vol danger, BTC breakdown, ~6h-old scalp data. (Scalp report is the stalest input — treat as carry-forward.)
- **Crypto intraday:** NO-TRADE / watchlist only (best NEAR 59.1, sub-threshold, no volume).
- **Crypto swing:** WATCHLIST only — **fresh this run** (window-2 refresh). NEAR 56.2 in danger regime; nothing clears threshold.
- **Stocks intraday:** LEAN LONG NVDA (in-zone, but 1.0R — scalp-grade). AMD manage-only.
- **Stocks swing:** LEAN LONG NVDA (best geometry); AMD add-back at 493–507 only. **Fresh this run.**
- **Stocks invest:** Constructive long bias NVDA/AMD B-tier (semis secular), **fresh this run** — accumulate on pullbacks, not spot.
- **Overall:** **Risk-on equities / risk-off crypto.** The desk's only A-tier edge is US AI-semis (NVDA > AMD on entry discipline), tempered by a poor A-tier track record and visible chase risk. Crypto is a stand-aside until BTC reclaims $70K. The binary that overrides everything is the Iran/Hormuz + Strategy-sale macro tape.

---

## 10. §14 Compliance Note
- Every external claim carries title + source + date + URL (§11).
- No fabricated TradingView/chart observations — chart MCP not loaded; structure read from local OHLCV fields only.
- Telegram wire items flagged **social_only** (unverified). Goldman $285 NVDA target flagged as **reported, not primary filing.**
- `test_source` rows filtered by the ingestion pipeline (0 rejected on ingest).
- Swing/invest data was **fresh this run** (window-2 refresh, ~3h old) — not carry-forward.

---

## 11. Sources

**Crypto / macro**
- [Bitcoin drops toward $69,000 as Saylor sale spooks investors while AI tokens buck the trend — CoinDesk, 2026-06-02](https://www.coindesk.com/markets/2026/06/02/bitcoin-drops-toward-usd69-000-as-saylor-sale-spooks-investors-while-ai-tokens-buck-the-trend)
- [Bitcoin retreats under $72,000 as Strategy unloads BTC for first time in four years — CoinDesk, 2026-06-01](https://www.coindesk.com/markets/2026/06/01/live-markets-bitcoin-retreats-under-usd72-000-as-strategy-unloads-btc-for-first-time-in-four-years)
- [Crypto News, June 2: Bitcoin Flash Crashes Below $70K, Saylor Explains Strategy Sale — cryptonews.com, 2026-06-02](https://cryptonews.com/news/crypto-news-june-2-bitcoin-price-flash-crashes-below-70k-saylor-explains-strategy-sale-trump-saving-bibis-ass/)
- [NEAR, Worldcoin Post Double-Digit Gains as Market Sees $714M in Liquidations — Decrypt, 2026-06-02](https://decrypt.co/369708/near-worldcoin-post-double-digit-gains-as-market-sees-714m-in-liquidations)
- [NEAR Protocol Price Forecast: NEAR extends rally, defying broader collapse (dynamic resharding in June) — FXStreet, 2026-06-02](https://www.fxstreet.com/cryptocurrencies/news/near-protocol-price-forecast-near-extends-rally-defying-broader-collapse-202606020551)
- [MoneyGram launches stablecoin MGUSD on Stellar — CoinDesk, 2026-06-02](https://www.coindesk.com/business/2026/06/02/moneygram-launches-stablecoin-on-stellar-joining-rush-toward-digital-dollar-payments)

**Stocks**
- [NVDA: NVIDIA Corp — Stock Price, Quote and News — CNBC (Computex coverage), 2026-06-02](https://www.cnbc.com/quotes/NVDA)
- [Will Nvidia Stock Rise From CEO Jensen Huang's COMPUTEX 2026 Participation? — The Motley Fool, 2026-05-31](https://www.fool.com/investing/2026/05/31/nvda-stock-jensen-huang-keynote-computex/)
- [AMD Stock Hits $527 — 138% Surge on AI & Data Center Demand 2026 — FX Leaders, 2026-06-02](https://www.fxleaders.com/news/2026/06/02/amd-amd-stock-hits-527-138-surge-on-ai-data-center-demand-2026/)
- [Advanced Micro Devices (AMD) Stock Forecast and Price Target 2026 — MarketBeat (accessed 2026-06-02)](https://www.marketbeat.com/stocks/NASDAQ/AMD/forecast/)

**Telegram wire (social_only — unverified, directional context)**
- t.me/WalterBloomberg — Iran / Strait of Hormuz / Rubio negotiation headlines + "Bitcoin slides below $70K as bearish bets build," 2026-06-02 14:25–15:04 UTC (ingested via RSS/Telegram collector; not independently verified against a primary source).
- t.me/lookonchain — BTC/ETH/SOL ETF netflow update, 2026-06-02 (single_source).
