# OPUS Enriched Market Review — Auto Run

- **Generated:** 2026-06-03 00:52 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`)
- **Scheduler cycle reviewed:** `2026-06-02_default_schedule` cycle 02 (22:30 EEST window); `scheduler.log` mtime 2026-06-02 23:10 EEST → **alive** (≈1h42m before this run, < 3h threshold).
- **Modes covered:** crypto scalp + intraday (fresh); crypto swing + stocks swing/invest (**carry-forward**, see Data Used); stocks intraday (fresh, weekday).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim below carries title + source + date + URL (skill §14).
- **Chart tools:** TradingView / Chrome MCP **not loaded** in this environment — no chart observations are fabricated; all price/structure data comes from the system's local OHLCV report fields.

---

## 1. Executive Summary

- **Two-speed tape.** Crypto is in a **high-volatility danger** regime (BTC & ETH downtrend, BTC ATR percentile 100) with **zero A/B-tier setups** across scalp and intraday — the desk's correct output is *no trade*. US stocks are simultaneously **bullish** (VIX 15.88, 100% breadth above EMA20/50, SMH/XLK leading).
- **BTC lost $70K.** Confirmed externally: BTC ~$69,400 on Jun 2, an **11-session record ETF outflow streak of $3.45B** (longest since the Jan-2024 launch), plus MicroStrategy's first BTC sale since Dec 2022 and a Mt. Gox $739M transfer. Capital is visibly rotating from BTC into AI/semis.
- **Dominant stocks catalyst = AVGO earnings TODAY (Jun 3, after close).** Consensus EPS ~$2.40 on ~$22.1B revenue (+47% YoY), AI-semi revenue guided ~$10.7B (+~140% YoY). The system already applied a **−16 earnings risk penalty** to the AVGO intraday long — do not hold a fresh intraday long into the print.
- **A-tier stocks (NVDA, AMD) are triggered but extended.** AMD is +141% YTD with a consensus 12-mo target ($479.77) *below* its current price ($521.54). Note the internal stat: stocks **A-tier is the worst-performing tier this week (PF 0.27, avg R −0.22, total −8R over 43)** — treat A-tier longs as "respect the trend, don't chase the extension."
- **No actionable crypto trade.** Best crypto watchlist name is XLM (intraday 62.6) — still below threshold, in a danger regime. SMCI legal-overhang concern is **resolved/stale** (recovered fundamentals, filings current).

---

## 2. Data Used

**Internal (fresh):**
- `data/reports/scalp/2026-06-02_19-46_scalp_report.md` (gen 22:46 EEST, data freshness 19:30 UTC)
- `data/reports/intraday/2026-06-02_20-01_intraday_report.md` (gen 23:01 EEST, data freshness 19:45 UTC)
- `data/reports/stocks/intraday/2026-06-02_20-09_stocks_intraday_report.md` (gen 20:09 UTC, regular session) — weekday, < 24h, used.
- `data/catalysts/2026-06-02/catalyst_cycle_20-01.md` + `catalyst_events.jsonl` (911 events) + `narrative_baskets.jsonl` (4 baskets)
- CLI: `active-signals --asset-class crypto` (5 active), `active-signals --asset-class stocks` (50 active), `signal-stats` crypto + stocks, `detect_untracked_legacy_alerts --since 2026-06-03` (**none** — no PART 1 regression).

**Internal (carry-forward — older than the 12h refresh expectation, per the 00:30-firing cadence note):**
- `data/reports/swing/2026-06-02_14-55_swing_report.md` — **≈10h old** (gen 17:55 EEST). Swing data is carry-forward this run, not fresh.
- `data/reports/stocks/swing/2026-06-02_15-03_stocks_swing_report.md` — **≈7h old** (gen 18:03 EEST). Carry-forward.
- `data/reports/stocks/invest/2026-06-02_15-08_stocks_invest_report.md` — **≈7h old** (gen 18:08 EEST). Carry-forward.

**External (this run — all dated & cited in §10):** CoinDesk, CNBC, crypto.news (BTC macro); StockTitan + AlphaStreet/Zacks (AVGO earnings); StockAnalysis, MarketBeat (AMD/NVDA); StockTitan 10-Q (SMCI). Ingested into `news_items` (3 crypto + 5 stocks rows).

**Unavailable / blind:**
- TradingView/Chrome chart verification — tool not loaded (noted above).
- Live social attention (Reddit sources failing; X/Telegram/Discord not connected). Crypto crowd context is thin.
- Liquidation heatmaps, order-book depth/CVD, ETF-flow feed, on-chain whale flows, token-unlock calendar — all still manual/unconnected (per report §9 blindspots).
- No `data/catalysts/2026-06-03/` directory yet (next scan runs with the next scheduler cycle).

---

## 3. Per-Cycle Landscape

### Crypto regime — DANGER (no-trade)
- BTC trend downtrend, ETH trend downtrend; altcoin breadth above EMA20 = 43.3%; BTC ATR percentile **100** (volatility elevated).
- Recommended style (system): *reduce size or no trade until structure settles.*
- Money flow: relative-strength pockets in EPIC, ZEC, ONDO, ENA (RWA/AI rotation) but every long "conflicts with current market regime"; SOL/AVAX/TAO shorts all rejected as ">2 ATR from EMA20, do not chase."
- Funding broadly neutral; SOL/AVAX funding mildly negative (shorts pressing — squeeze risk if BTC reclaims).
- Narrative baskets live: `perps_dex` (HYPE), `ai` (NEAR/RENDER/TAO/FET), `rwa` (ONDO/XLM), `momentum_breakout` (PORTAL/ZEC) — all single-source, playbooks `wait_pullback` / `related_beta_rotation`. None promote to a tradeable signal in a danger regime.

### Stocks regime — BULLISH (long bias)
- 4/4 indices uptrend; SPY +5.79% 20d, QQQ +10.89% 20d; VIX 15.88; breadth 100% above EMA20/50.
- Sector leadership: **semiconductors (SMH RS +18.96%)** and **technology (XLK RS +16.53%)**; laggards utilities/energy/communications.
- Event risk: **AVGO earnings next session** (swing-blocked by earnings). 17 other tracked names earnings-safe.

---

## 4. Candidate Deep Dives (≤5)

### 4.1 AVGO (Broadcom) — long, B-tier (intraday 67.3, −16 earnings penalty) — **EVENT, NOT A TRADE TONIGHT**
- **Internal verdict (pre-web):** B-tier long, RS +9.84% vs SPY, above prior-day high, but the system stamped a **−16 risk penalty** because earnings are next session.
- **External confirm:** Broadcom reports **Q2 FY2026 on Wed Jun 3, 2026 after market close**, call 2:00pm PT / 5:00pm ET ([StockTitan announcement, dated 2026-05-04](https://www.stocktitan.net/news/AVGO/broadcom-inc-to-announce-second-quarter-fiscal-year-2026-financial-04if2lwax8o1.html)). Consensus **EPS ~$2.40 on ~$22.1B revenue (+47% YoY)**, AI-semiconductor revenue guided **~$10.7B (+~140% YoY)**, AI networking ~40% of AI revenue ([AlphaStreet/Zacks preview, 2026-06-01](https://news.alphastreet.com/broadcom-avgo-q2-2026-preview-eps-est-2-40-reports-june-3/amp/)).
- **Take:** Highest-information event of the next 24h and the read-through for the entire AI-semi complex (NVDA/AMD/SMH). The system is right to de-rate a fresh long into a binary print. **Action: do not initiate a fresh AVGO intraday long pre-print; let the report set direction, then trade the post-earnings structure.**
- `verification_status`: primary_source (date) + single_source (estimates).

### 4.2 NVDA — long, A-tier (intraday 84.7 / swing 83.8) — trend respect, no chase
- **Internal verdict:** A-tier, triggered, regime-aligned, RS leader/follower.
- **External confirm:** Consensus **Strong Buy**; S&P Global avg target ~**$296.81** (61 analysts); other aggregators ~$305. Computex-2026 product push (new AI compute architecture); **Deutsche Bank maintains Hold** as a dissent ([MarketBeat forecast, 2026-06-02](https://www.marketbeat.com/stocks/NASDAQ/NVDA/forecast/)).
- **Counter-signal (internal):** stocks **A-tier is this week's worst tier — PF 0.27, avg R −0.22, total −8R (n=43)**. A-tier scores are catching extended late-trend entries.
- **Take:** Bullish structure intact and AVGO print is the swing factor. Trade only on a clean pullback to the entry zone; do not chase >2 ATR. `verification_status`: single_source.

### 4.3 AMD — long, A-tier (intraday 84.7) / B-tier invest 78.0 — **most extended**
- **Internal verdict:** A-tier, RS vs SPY +46.92%, RS vs sector +27.95% — strongest RS in the book.
- **External confirm:** Price **$521.54 (+2.24% Jun 2)**, **+141% YTD**, forward P/E ~74. Banks raised aggressively (Barclays $665, Mizuho $615, TD Cowen $600), **yet the blended consensus 12-mo target is $479.77 — ~8% BELOW the current price** ([StockAnalysis, 2026-06-02](https://stockanalysis.com/stocks/amd/)). MI400 inference roadmap; customer visibility into 2027.
- **Take:** Leadership name but valuation has run past the average target. This is the textbook "respect trend, refuse to chase" case the desk's >2-ATR gate exists for. `verification_status`: single_source.

### 4.4 SMCI (Super Micro) — long, B-tier intraday 71.3 — **legal overhang resolved/stale**
- **Internal verdict:** B-tier long, RS vs SPY +73.91% (highest RS in the stocks book), but tiny relative volume (0.24x) — thin participation.
- **External check (the user's standing legal-risk concern):** Q3 FY2026 **net sales $10.24B, net income $483M**, FY26 guidance **raised to ≥$36B**; **next earnings Aug 11, 2026**; filings current ([StockTitan 10-Q, 2026-05-06](https://www.stocktitan.net/sec-filings/SMCI/10-q-super-micro-computer-inc-quarterly-earnings-report-33fa356d1d43.html)). The Ernst & Young resignation is **historical (Oct 30, 2024)**, not a fresh catalyst.
- **Take:** No fresh legal red flag — thesis is now a pure momentum/RS call, weakened by thin volume. `verification_status`: single_source.

### 4.5 BTC macro — drives the entire crypto no-trade verdict
- **Internal verdict:** danger regime, BTC short rejected (>2 ATR from EMA20), no long viable.
- **External confirm:** BTC ~**$69,400** Jun 2 (−2.7% 24h), broke the $72.5–73K support; **11 straight sessions of ETF outflows = $3.45B** (longest streak since Jan-2024 launch), 2026 YTD ETF flows now negative for the first time ([CoinDesk, 2026-06-02 06:47](https://www.coindesk.com/markets/2026/06/02/bitcoin-s-biggest-etf-selloff-yet-hits-usd3-4-billion-as-ai-stocks-keep-climbing); [CNBC, 2026-06-02](https://www.cnbc.com/2026/06/02/bitcoin-drops-back-under-70000-strategy-extends-its-slide.html)). Drivers: **Strategy's first BTC sale since Dec 2022**, **Mt. Gox $739M transfer**, **$744M / 152k traders liquidated**. CryptoQuant: "a market of holders rather than buyers." Downside watch toward $65K ([crypto.news, 2026-06-02](https://crypto.news/will-bitcoin-price-fall-to-65k-next-as-etf-outflows-deepen/)).
- **Take:** Macro confirms the desk — no fresh BTC entry. Watch for a reclaim of $70K (would relieve the SOL/AVAX short-squeeze setup) or acceptance toward $65K. `verification_status`: single_source ×3 (corroborated).

---

## 5. Best Candidates (ranked)

1. **AVGO** — top *information* event (earnings tonight). No fresh pre-print position; trade the reaction. Highest read-through to the whole AI-semi book.
2. **NVDA** — cleanest A-tier trend; only on a pullback into entry, sized for the AVGO read-through.
3. **SMH / XLK (ETFs)** — basket expression of semi leadership; less single-name binary risk than AVGO/AMD into earnings.
4. **AMD** — strongest RS but most extended; wait-for-pullback only.
5. *(crypto)* **none actionable** — XLM intraday 62.6 is the best name and still sub-threshold in a danger regime.

---

## 6. Avoid / No-Trade

- **All fresh crypto entries** — danger regime, zero A/B setups, BTC sub-$70K with record ETF outflows. The desk's no-trade is correct.
- **Fresh AVGO long into the print** — binary event risk (system −16 penalty agrees).
- **Chasing AMD/NVDA >2 ATR from entry** — AMD already trades above consensus target; A-tier is the worst-performing stock tier this week.
- **SOL / AVAX / TAO shorts** — all rejected as overextended (>2 ATR from EMA20); negative funding adds squeeze risk if BTC reclaims $70K.
- **Crypto shorts generally** — short direction stat is anecdotal/breakeven (0.0 R), and a BTC reclaim would whipsaw.

---

## 7. Main Risks

1. **AVGO earnings tonight** sets the tone for NVDA/AMD/SMH/SMCI — a miss or soft AI-networking guide could unwind the extended semi leadership fast.
2. **BTC contagion** — if BTC accepts toward $65K, alt longs (RWA/AI rotation names) get dragged regardless of relative strength; risk-off could spill into high-beta stocks.
3. **Extension risk** — AMD +141% YTD above its consensus target, NVDA near targets; A-tier scores are catching late entries (−8R this week).
4. **Data blindspots** — no live social/on-chain/liquidation feeds; crypto crowd and leverage context is thin, so squeeze risk is under-measured.
5. **Carry-forward swing/invest** — crypto swing ~10h old, stocks swing/invest ~7h old; swing verdicts below are stale, re-confirm at the 04:04 EEST refresh.

---

## 8. Action Plan — next 4 hours

- **Crypto:** no new trades. Monitor BTC at $70K (reclaim = relief / squeeze setup; rejection = drift toward $65K). Let existing tracked signals (ZEC/XLM swing tp1/tp2-hit, winding to expiry Jun 7) run on their own rules — no adds.
- **Stocks (US closed overnight; cash session resumes 16:30 EEST):** prep, don't act. Mark NVDA/SMH/XLK pullback entry zones. **No fresh AVGO long before the after-close print.** Re-read the AVGO release tonight and let it set the AI-semi direction for the next session.
- **Next cycle:** the 04:04 EEST scheduler cycle refreshes crypto swing + stocks swing/invest — re-confirm those verdicts then (they are carry-forward now). A fresh `data/catalysts/2026-06-03/` scan should also appear.
- **No code, scoring, or threshold changes** (safety contract).

---

## 9. Final Verdict (per mode + overall)

- **Crypto scalp:** NO TRADE — danger regime, no setup. (fresh)
- **Crypto intraday:** NO TRADE — best name XLM 62.6, sub-threshold. (fresh)
- **Crypto swing:** NO fresh entry; existing ZEC/XLM longs winding to expiry. *(carry-forward, ~10h old — re-confirm at 04:04 EEST)*
- **Stocks intraday:** Bullish, long-only, but **stand aside on AVGO into earnings**; NVDA/SMH/XLK on pullback only. (fresh)
- **Stocks swing/invest:** Trend long-friendly (NVDA A-tier, AMD/SMH/AAPL B-tier), but **carry-forward (~7h old)** and gated by tonight's AVGO print — re-confirm at the 04:04 EEST refresh. *(carry-forward)*
- **Overall:** **Crypto = risk-off / no-trade; Stocks = bullish but event-gated.** The single decision that matters in the next 24h is the AVGO after-close report. Patience over participation.

---

## 10. Sources

- [Bitcoin's biggest ETF selloff yet hits $3.4 billion as AI stocks keep climbing — CoinDesk, 2026-06-02](https://www.coindesk.com/markets/2026/06/02/bitcoin-s-biggest-etf-selloff-yet-hits-usd3-4-billion-as-ai-stocks-keep-climbing) — BTC slid toward $70K; 11-session $3.45B ETF outflow streak (longest since Jan-2024); CryptoQuant "market of holders." *(single_source, verified via WebFetch)*
- [Bitcoin drops back under $70,000, Strategy extends its slide — CNBC, 2026-06-02](https://www.cnbc.com/2026/06/02/bitcoin-drops-back-under-70000-strategy-extends-its-slide.html) — sub-$70K break; MicroStrategy first BTC sale since Dec 2022. *(single_source)*
- [Will Bitcoin price fall to $65K next as ETF outflows deepen? — crypto.news, 2026-06-02](https://crypto.news/will-bitcoin-price-fall-to-65k-next-as-etf-outflows-deepen/) — downside scenario toward $65K. *(single_source)*
- [Broadcom to Announce Q2 FY2026 Results on June 3, 2026 (after close) — StockTitan, 2026-05-04](https://www.stocktitan.net/news/AVGO/broadcom-inc-to-announce-second-quarter-fiscal-year-2026-financial-04if2lwax8o1.html) — earnings date/time confirmed. *(primary_source, verified via WebFetch)*
- [Broadcom (AVGO) Q2 2026 Preview: EPS Est. $2.40 — AlphaStreet/Zacks, 2026-06-01](https://news.alphastreet.com/broadcom-avgo-q2-2026-preview-eps-est-2-40-reports-june-3/amp/) — consensus EPS $2.40, rev $22.1B (+47% YoY), AI-semi ~$10.7B. *(single_source)*
- [AMD Stock Overview — StockAnalysis, 2026-06-02](https://stockanalysis.com/stocks/amd/) — price $521.54, +141% YTD, consensus 12-mo target $479.77 (below price), Strong Buy. *(single_source, verified via WebFetch)*
- [NVIDIA (NVDA) Stock Forecast — MarketBeat, 2026-06-02](https://www.marketbeat.com/stocks/NASDAQ/NVDA/forecast/) — Strong Buy consensus, avg target ~$296.81; Deutsche Bank Hold post-Computex 2026. *(single_source)*
- [Super Micro Computer Q3 FY2026 10-Q — StockTitan, 2026-05-06](https://www.stocktitan.net/sec-filings/SMCI/10-q-super-micro-computer-inc-quarterly-earnings-report-33fa356d1d43.html) — net sales $10.24B, FY26 guidance raised ≥$36B, next earnings Aug 11 2026; EY resignation historical (Oct 2024). *(single_source)*

_Internal CLI evidence (no external citation needed): active-signals (crypto 5 / stocks 50), signal-stats (crypto sample 23 weak, PF 3.5; stocks sample 629 reliable, A-tier PF 0.27 / −8R), detect_untracked_legacy_alerts (none). 8 external rows ingested to `news_items`._

---
*Auto-generated by the `opus-enriched-review-4h` scheduled task. Read-only: no trades placed, no scoring/threshold/strategy code modified, no paid APIs added. Chart tooling not loaded — no chart observations fabricated.*
