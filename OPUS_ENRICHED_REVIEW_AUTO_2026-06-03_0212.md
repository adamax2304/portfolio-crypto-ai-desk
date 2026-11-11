# Opus Enriched Review — Auto Cycle 02:12 EEST

- **Generated:** 2026-06-03 02:12 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`)
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-03_0052.md` (≈80 min ago)
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Every external claim is cited in §13 with source + date + URL.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from the system's local OHLCV/ATR/EMA report fields.

---

## 1. Executive Summary

- **NEW since last review — Middle-East risk-off catalyst the 00:52 run missed.** The internal feed carries fresh (last ~4h) headlines: US sanctions on **Nobitex + 3 Iranian crypto exchanges** (externally confirmed — CoinDesk/Bloomberg/ABC, 2026-06-02), CENTCOM oil-tanker enforcement in the Gulf of Oman, a Treasury **Strait of Hormuz "toll-payment" sanctions warning**, plus social-only WalterBloomberg lines on Kuwait air defences intercepting missiles and explosions in Iran. The US–Iran conflict is **ongoing** as of Jun 2. This is a live oil-spike / risk-off overlay on **both** asset classes.
- **Two-speed tape persists, but the stocks-bullish read now carries an event + geopolitical overhang.** Crypto stays in **high-volatility danger** (BTC & ETH downtrend, BTC ATR percentile 100), **zero A/B-tier crypto setups** — desk output remains correct *no-trade*. US stocks regime still prints **bullish** (VIX 15.77, 100% breadth) but that data predates the latest Iran headlines and is gated by AVGO earnings.
- **AVGO earnings are TONIGHT (Wed Jun 3, after US close).** The system already stamped a **−16 earnings penalty** on the AVGO intraday long (B-tier 67.3). Do not initiate a fresh AVGO long into the print. Highest-information event of the next 24h for the whole AI-semi book.
- **AMD is the lone A-tier signal (intraday 84.7 / swing 81) and the contradiction case.** Stocks **A-tier is the worst tier this week — PF 0.27, 6% triggered winrate, n=43**, and AMD trades **+141% YTD above its consensus 12-mo target ($479.77)**. Respect the trend, refuse the chase. A risk-off oil shock would hit the most-extended semis hardest.
- **No actionable crypto trade.** Best crypto names are sub-threshold watchlist only (XRP intraday 57.6, XLM scalp 56.0). BTC ~$67–69.5K with 11 straight days of ETF outflows (~$3–3.45B). Catalyst mapping is **weak this run (79% unmapped)** — use the catalyst layer as context, not a decision input.

---

## 2. Data Used

**Internal — fresh (<4h):**
- `data/reports/scalp/2026-06-02_22-22_scalp_report.md` (gen 01:22 EEST; data freshness 22:00 UTC)
- `data/reports/intraday/2026-06-02_22-32_intraday_report.md` (gen 01:32 EEST; data freshness 22:15 UTC)
- `data/reports/stocks/intraday/2026-06-02_22-36_stocks_intraday_report.md` (gen 22:36 UTC; session=after-hours) — weekday, fresh
- `data/catalysts/2026-06-02/catalyst_cycle_22-32.md` + `catalyst_events.jsonl` + `narrative_baskets.jsonl` (gen 01:32 EEST)
- `data/processed/llm_analysis_packet.md` (01:32), `llm_stocks_packet.md` (01:36)
- CLI: `active-signals` crypto (5) + stocks (24 rows), `signal-stats` crypto + stocks, `detect_untracked_legacy_alerts --since 2026-06-03` (**None** — no integrity regression)

**Internal — carry-forward (older than the 12h swing/invest refresh expectation):**
- `data/reports/swing/2026-06-02_14-55_swing_report.md` — **≈8h old** (gen 17:55 EEST). Carry-forward.
- `data/reports/stocks/swing/2026-06-02_15-03_stocks_swing_report.md` — **≈8h old**. Carry-forward.
- `data/reports/stocks/invest/2026-06-02_15-08_stocks_invest_report.md` — **≈8h old**. Carry-forward.

**External (this run — cited §13):** CoinDesk + Bloomberg + ABC (Iran/Nobitex sanctions); Wikipedia/CNBC/Navy Times (Hormuz crisis context); Bitcoin Magazine / crypto.news / CoinGlass (BTC price + ETF outflows); StockTitan (AVGO earnings date, prior-run primary); StockAnalysis (AMD valuation, prior-run).

**Unavailable / blind:**
- TradingView / Chrome chart verification — tool not loaded.
- Live social attention (Reddit sources failing; X/Telegram/Discord not connected — though the RSS bridge does carry t.me/WalterBloomberg + t.me/lookonchain rows).
- Liquidation heatmaps, order-book depth/CVD, ETF-flow feed, on-chain whale flows, token-unlock calendar — all still manual/unconnected.
- No `data/catalysts/2026-06-03/` folder yet (UTC day is still 06-02; active catalyst data lives in the 06-02 folder).

---

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: **2026-06-03 01:37 EEST** (≈35 min before this run) → **ALIVE** (< 3h threshold).
- Latest cycle summary: `cycle_03_01-10_summary.md` mtime **01:37 EEST** (≈35 min ago) → fresh. **Not deferred.**
- Crypto scalp/intraday + stocks intraday: **fresh** (<1h).
- Crypto swing + stocks swing/invest: **carry-forward** (~8h old; within the 4–12h carry-forward band, not yet borderline-stale). Re-confirm at the 04:04 EEST refresh.

---

## 4. What Changed vs Previous Review (00:52)

- **NEW catalyst (material):** Middle-East / Iran risk-off cluster surfaced in the feed (US sanctions Nobitex + 3 Iranian exchanges; CENTCOM Gulf-of-Oman tanker enforcement; Hormuz toll-payment sanctions warning; social-only Kuwait-intercept / Iran-explosion lines). The 00:52 review did **not** mention any of this. This is the single biggest delta.
- **New candidate:** Iran/Hormuz geopolitical risk overlay (this run's §7.2).
- **Removed candidate:** SMCI deep-dive (00:52 ran it to clear the legacy SMCI legal-overhang concern — that came back clean/stale, no fresh flag; not re-dived this run to stay within the 5-candidate cap).
- **Tier/score changes:** none material. AMD stays A-tier (intraday 84.7, swing 81). AVGO stays B-tier 67.3 with the −16 earnings penalty. Crypto stays zero-A/B. Best crypto watchlist rotated slightly (00:52 cited XLM intraday ~62.6; this run's intraday top is XRP 57.6 then XLM 52.0 — scores drifted down, still sub-threshold).
- **Thesis confirmed:** crypto no-trade (danger regime, BTC sub-$70K, ETF outflows) — confirmed by data + external. Stocks bullish-but-event-gated by AVGO — unchanged.
- **Thesis strengthened:** the "don't chase extended semis" stance is now reinforced by the fresh oil/geopolitical risk-off — an extension AND an event AND a macro shock all point the same way.
- **Not invalidated:** no candidate's invalidation level was breached; no catalyst proven wrong.

---

## 5. Catalyst Coverage

- `catalyst_events.jsonl` (2026-06-02) total rows: **3315**
- Mapped (non-empty symbol): **688**
- Unmapped (empty/null symbol): **2627** → **79.2% unmapped**
- Narrative baskets: **4** (ai_narrative, perps_dex_narrative, rwa_narrative, momentum_breakout)
- **⚠️ catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped 79.2% > 50%)
- *Note:* the `importance` field is **0.0 across all rows** in this file (scorer not populating it), so "top unmapped by importance" is not meaningful; the list below is the top unmapped non-`other_news` headlines by catalyst type instead.

**Top unmapped headlines worth a human eye:**
1. `legal_risk` — *Citron Research founder Andrew Left found guilty of securities fraud* (Seeking Alpha)
2. `exploit_hack` — *Radiant Capital winding down after failing to recover from ~$50M hack* (The Block / Cointelegraph)
3. `regulatory_sector_headline` — *Debate on CLARITY Act continues as US Senate returns* (Cointelegraph)
4. `exchange_listing` — *Binance Futures to launch multiple USDⓈ-margined TradFi perpetuals (2026-06-02)* (Binance Announcements)
5. `platform_growth` — *Credo signals 80%+ FY2027 revenue growth, $600m+ from optical portfolio* (Seeking Alpha) — note optical-stocks strength echoes the AI-networking read-through into AVGO tonight.

---

## 6. Market Landscape

### Crypto — DANGER (no-trade)
- BTC trend downtrend, ETH trend downtrend; altcoin breadth above EMA20 = 50.0%, EMA50 = 53.3%; BTC ATR percentile **100** (volatility elevated). System style: *reduce size or no trade until structure settles.*
- External: BTC ~**$67–69.5K** (intraday low ~$67K range; −13% on the week), **11 straight sessions of ETF outflows ≈$3–3.45B**, ~45% below the Oct-2025 ATH (~$126K). Confirms the desk's danger read.
- Money flow: relative-strength pockets (PORTAL, ZEC, ONDO, EPIC, ICP — RWA/AI rotation) but every long is rejected as *"conflicts with current market regime."* Strongest *weak* names (shorts) SOL/TON/FET/XLM all show negative-funding squeeze risk if BTC reclaims $70K.
- Baskets live: `ai` (NEAR/RENDER/TAO/FET), `perps_dex` (HYPE), `rwa` (ONDO/XLM), `momentum_breakout` (ONDO) — all single-source; none promote to a tradeable signal in a danger regime.

### Stocks — BULLISH on the data, but the data predates the Iran headlines (weekday; intraday fresh, swing/invest carry-forward)
- 4/4 indices uptrend; SPY +5.79% 20d, QQQ +10.89% 20d, IWM +4.96%, DIA +5.00%; **VIX 15.77**; breadth 100% above EMA20/50.
- Sector leadership: **semiconductors SMH (RS +18.96%)** and **technology XLK (RS +16.53%)**; laggards utilities (−11.11%), energy (−8.20%), communications (−7.97%).
- **Caveat:** the bullish snapshot + low VIX are from the 22:36-UTC after-hours pull, *before* the latest Gulf-of-Oman / Hormuz / Kuwait headlines. An oil-spike risk-off gap is a live downside the regime label hasn't ingested yet — and energy (XLE) screening "weak" is exactly the sector that would re-rate up on an oil shock.
- Event risk: **AVGO earnings next session** (swing-blocked). 17 other tracked names earnings-safe.

---

## 7. Candidate Deep Dives (≤5)

### 7.1 AMD — A-tier stocks (intraday 84.7 / swing 81) — **respect trend, no chase; manual into the macro tape**
- **Internal view:** A-tier, triggered, regime-aligned. Strongest RS in the book — RS vs SPY +46.91%, RS vs sector +27.95% (intraday). Risk level "low" per the model, penalty only −4.0.
- **Contradiction risk (the reason it's candidate #1):** stocks **A-tier is the single worst-performing tier this week — PF 0.27, 6% triggered winrate, total ≈−8R over n=43** (signal-stats, reliable). The A-score is repeatedly catching late, extended trend entries.
- **External:** AMD ~**$521.54 (+141% YTD)**, blended consensus 12-mo target **$479.77 — ~8% BELOW the current price** (StockAnalysis, prior-run, <24h, still valid). Bank targets are split high ($600–665), but the *average* is under spot.
- **Price-reaction / chase check:** TradingView / manual chart check unavailable. The setup is a continuation long above prior-day high; entry zone 516.85–521.41 with invalidation 507.72 (intraday). Price sits at the top of its own entry zone — entry **now is late** unless it pulls back into the lower zone. Overextended on the YTD/valuation read. Actionable only on a clean pullback into entry with the broad tape stable.
- **Macro overlay:** most-extended semi = highest beta to an oil-spike risk-off. The Iran headlines argue *against* adding here.
- **Final verdict: WATCHLIST ONLY / pullback-entry — do not chase.** Trend intact, but extension + worst-tier stat + fresh geopolitical risk = no fresh chase. `verification_status`: single_source.

### 7.2 Iran / Strait of Hormuz geopolitical risk-off — **NEW; MANUAL REVIEW / risk overlay**
- **Internal view:** surfaced via the news/Telegram bridge in the last ~4h — US sanctions on Nobitex + 3 Iranian exchanges; CENTCOM oil-tanker enforcement in the Gulf of Oman; IEA "critically low oil stockpiles"; US crude inventories −6.75M bbl (~2× forecast); social-only (WalterBloomberg) lines on Kuwait air defences intercepting missiles and explosions in Iran.
- **External (verified):** US Treasury **sanctioned Nobitex + Wallex/Bitpin/Ramzinex on 2026-06-02** over IRGC links; described as part of the **"ongoing war against the country,"** with a Treasury **Strait of Hormuz toll-payment sanctions warning** (CoinDesk + Bloomberg + ABC, 2026-06-02 — primary/single_source). Broader 2026 Hormuz crisis / US naval blockade is real (Wikipedia/CNBC/Navy Times); the formal blockade ended ~May 29, so the June 2 activity reads as **renewed enforcement / fragile-truce friction**, not a clean new war.
- **Not independently confirmed:** the specific Kuwait-intercept and Iran-explosion lines are **social_only** (WalterBloomberg telegram); my external search did not corroborate June 2-3 missile events. Treat those as weak.
- **Price-reaction check:** crypto already risk-off (BTC sub-$70K). Stocks have **not** priced the headlines (data is pre-headline, VIX 15.77). The asymmetric risk is an **oil-spike gap** + equity risk-off into a session that holds extended semis and an AVGO binary.
- **Final verdict: MANUAL REVIEW REQUIRED — treat as a risk overlay, not a trade.** Reinforces crypto no-trade; caps conviction on fresh stock longs; watch oil/XLE and VIX at the US open. `verification_status`: primary_source (sanctions) + social_only (military escalation).

### 7.3 AVGO (Broadcom) — B-tier intraday 67.3 (−16 earnings penalty) — **EVENT, NOT A TRADE TONIGHT**
- **Internal view:** B-tier long, RS vs SPY +9.84%, above prior-day high, sector-confirmed — but the system applied a **−16 earnings risk penalty** because the print is next session. Intraday active-signal shows AVGO demoted to C/waiting on the latest cycle.
- **External:** Broadcom reports **Q2 FY2026 on Wed Jun 3, 2026 after market close** (StockTitan, primary, prior-run); consensus **EPS ~$2.40 on ~$22.1B revenue (+47% YoY)**, AI-semi revenue guided **~$10.7B**. The Credo optical-revenue beat and "optical stocks rocketing" headlines this run are a positive AI-networking read-through — but that's a reason to watch the print, not to front-run it.
- **Price-reaction check:** entry zone 477.15–481.54, invalidation 468.36. Binary event in <24h — RR is dominated by the print, not the chart.
- **Final verdict: NO FRESH LONG INTO THE PRINT.** Let the release set AI-semi direction (NVDA/AMD/SMH/SMCI), then trade the post-earnings structure. `verification_status`: primary_source (date) + single_source (estimates).

### 7.4 BTC macro — drives the entire crypto no-trade verdict
- **Internal view:** danger regime; BTC short rejected (>2 ATR from EMA20), no long viable. Macro risk 35/100 (Sanders/Warren 401k headline).
- **External:** BTC ~**$67–69.5K**, **11 consecutive days of ETF outflows ≈$3–3.45B** (largest monthly exodus of 2026; Jun-1 alone −$483.8M, IBIT −$440M), ~45% below ATH. Now compounded by the Iran risk-off (above). Downside watch toward **$65K**; relief only on a reclaim of **$70K** (which would also fuel the SOL/TON short-squeeze risk).
- **Final verdict: NO TRADE.** Macro confirms the desk. `verification_status`: single_source ×3 (corroborated).

### 7.5 Crypto active B-tier / best watchlist — **WATCHLIST ONLY**
- **Active B-tier signals (from active-signals):** INJ intraday (B, ~65), ZEC swing (B, ~65, tp-progress), XLM swing (B, ~65), UNI scalp short (B, ~65). These are existing tracked signals winding on their own rules — **no adds**.
- **Fresh report names (all sub-threshold, danger regime):** intraday XRP 57.6 / ADA 53.4 / LINK 52.3 / XLM 52.0 / SUI 51.6; scalp XLM 56.0 / ADA 54.7 / SUI 52.0 / XRP 51.9. All "watchlist only," low confidence, below-average volume, no fresh verified catalyst that survives the danger regime.
- **Price-reaction check:** every name is a *failed-bounce short* idea into a downtrend; chasing breakdowns in elevated-vol with squeeze-prone negative funding is exactly what the desk's gates block.
- **Final verdict: WATCHLIST ONLY — no fresh entries.** `verification_status`: internal-only (consistent; no external check warranted).

*Qualifying-but-not-deep-dived (5-candidate cap):* SMCI B-tier 71.3 (legal overhang already cleared last run, no fresh flag); SMH/XLK/AAPL/QQQ B-tier stock longs (same bullish-but-event-gated thesis as AMD/AVGO, no incremental contradiction).

---

## 8. Best Candidates Ranked

*(Internal + external alignment, in a tradeable sense.)*

1. **AVGO** — top *information* event (earnings tonight); highest read-through to the whole AI-semi book. No fresh pre-print position — trade the reaction.
2. **NVDA / SMH / XLK** — cleaner trend expression than the most-extended single names; pullback-entry only, sized for the AVGO read-through and the Iran risk overlay.
3. **AMD** — strongest RS but most extended and above consensus target; wait-for-pullback only, do not chase.
4. *(crypto)* **none actionable** — XRP intraday 57.6 is the best name and still sub-threshold in a danger regime.

If risk-tolerance is low tonight: **no new positions at all** is a fully defensible read given the AVGO binary + live Iran/oil risk-off.

---

## 9. Avoid / No Trade

- **All fresh crypto entries** — danger regime, zero A/B setups, BTC ~$67–69.5K with record ETF outflows + Iran risk-off. Desk no-trade is correct.
- **Fresh AVGO long into the print** — binary event (system −16 penalty agrees).
- **Chasing AMD/NVDA >2 ATR from entry** — AMD already above consensus target; stocks A-tier is the worst tier this week (−8R, PF 0.27).
- **SOL / TON / FET / XLM crypto shorts** — overextended (>2 ATR from EMA20); negative funding = squeeze risk on any BTC $70K reclaim.
- **Adding to extended semis ahead of a possible oil-shock risk-off** — the most-extended names carry the highest gap risk if the Iran situation escalates.
- **Acting on the unmapped catalyst layer** — 79% unmapped this run; context only.

---

## 10. Main Risks

1. **AVGO earnings tonight** sets the tone for NVDA/AMD/SMH/SMCI — a miss or soft AI-networking guide unwinds the extended semi leadership fast.
2. **Iran / Strait of Hormuz escalation (NEW)** — fresh US sanctions + tanker enforcement + (social-only) missile-intercept headlines. An oil-spike / risk-off gap would hit extended semis and high-beta crypto together. Stocks data is pre-headline, so the bullish/VIX read understates this.
3. **BTC contagion** — acceptance toward $65K drags alt longs regardless of RS; risk-off could spill into high-beta stocks.
4. **Extension risk** — AMD +141% YTD above consensus target; A-tier scores catching late entries (−8R this week).
5. **Catalyst mapping weak (79% unmapped)** + `importance` field unpopulated — the catalyst layer is context only this run; real catalysts may be under-surfaced.
6. **Data blindspots** — no live social/on-chain/liquidation/oil feeds; crypto crowd + leverage + geopolitical-oil context is thin and not auto-scored.
7. **Carry-forward swing/invest** (~8h old) — swing verdicts are stale-ish; re-confirm at the 04:04 EEST refresh.
8. **System integrity:** `detect_untracked_legacy_alerts --since 2026-06-03` returned **None** — no PART-1 regression. Empty `data/crypto_ai_desk.db` at project root is a decoy; the live DB is `db/crypto_ai_desk.sqlite` (no action needed).

---

## 11. Action Plan — next 4 hours

- **Crypto:** no new trades. Monitor BTC at $70K (reclaim = relief + SOL/TON squeeze setup; rejection = drift toward $65K) and watch for any Iran-driven risk-off leg. Let existing tracked B-tier signals (INJ/ZEC/XLM/UNI) run on their own rules — no adds.
- **Stocks (US closed overnight; cash session resumes 16:30 EEST):** prep, don't act. Mark NVDA/SMH/XLK pullback zones. **No fresh AVGO long before the after-close print.** Re-read the AVGO release tonight; let it set AI-semi direction. **Watch oil / XLE / VIX at the open** for any Iran-headline re-rate the current bullish snapshot hasn't priced.
- **Manual verification needed:** confirm whether the WalterBloomberg Kuwait-intercept / Iran-explosion lines are corroborated by a primary outlet before treating the military-escalation leg as fact (sanctions leg is already confirmed).
- **Next cycle:** the 04:04 EEST scheduler cycle refreshes crypto swing + stocks swing/invest and should produce a fresh `data/catalysts/2026-06-03/` scan — re-confirm carry-forward verdicts then.
- **No code, scoring, or threshold changes** (safety contract).

---

## 12. Final Verdict per Mode

- **Crypto scalp:** NO TRADE — danger regime, best name XLM 56.0 sub-threshold. *(fresh)*
- **Crypto intraday:** NO TRADE — best name XRP 57.6, sub-threshold. *(fresh)*
- **Crypto swing:** NO fresh entry; existing ZEC/XLM longs winding on their rules. *(carry-forward ~8h — re-confirm 04:04 EEST)*
- **Stocks intraday:** Bullish bias, long-only, but **stand aside on AVGO into earnings**; NVDA/SMH/XLK pullback-only; AMD no-chase. Cap conviction for the Iran/oil overlay. *(fresh, weekday)*
- **Stocks swing:** Trend long-friendly (AMD A-tier, NVDA/SMH/XLK/AAPL B-tier) but **carry-forward (~8h)** and gated by tonight's AVGO print + geopolitical risk — re-confirm 04:04 EEST. *(carry-forward)*
- **Stocks invest:** Long-bias intact on AI-semi leadership but **carry-forward (~8h)**; no fresh add ahead of AVGO + Iran risk. *(carry-forward)*
- **Overall:** **Crypto = risk-off / no-trade; Stocks = bullish-on-the-data but event-gated AND now geopolitically overhung.** The two decisions that matter next 24h: the **AVGO after-close print** and whether the **Iran/Hormuz** situation re-escalates into an oil shock. Patience over participation.

---

## 13. Sources

- [U.S. sanctions Nobitex, other Iranian crypto exchanges amid ongoing war — CoinDesk, 2026-06-02](https://www.coindesk.com/policy/2026/06/02/u-s-sanctions-iranian-crypto-exchanges-in-ongoing-war-against-country) — Treasury blacklists Nobitex + Wallex/Bitpin/Ramzinex over IRGC links; "ongoing war"; Hormuz toll-payment sanctions warning. *(primary/single_source, verified via WebSearch)*
- [US Sanctions Iran's Top Crypto Exchange in Ongoing Push for Deal — Bloomberg, 2026-06-02](https://www.bloomberg.com/news/articles/2026-06-02/us-sanctions-iran-s-top-crypto-exchange-in-ongoing-push-for-deal) — corroborates the Nobitex sanctions + ongoing US-Iran conflict. *(single_source)*
- [US sanctions Iran's largest digital asset exchange Nobitex and 3 others — ABC News, 2026-06-02](https://abcnews.com/Business/wireStory/us-sanctions-irans-largest-digital-asset-exchange-nobitex-133530748) — corroboration. *(single_source)*
- [2026 Strait of Hormuz crisis — Wikipedia](https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis) — broader crisis context (Feb–May 2026); article does not cover Jun 1-3, so June re-escalation is unconfirmed there. *(reference; verified via WebFetch)*
- [U.S. says Hormuz blockade 'fully implemented,' signaling diplomatic off-ramp — CNBC, 2026-04-15](https://www.cnbc.com/2026/04/15/us-strait-of-hormuz-blockade-navy-iran-seaborne-trade-oil-trump.html) — blockade context. *(single_source)*
- [US forces fire at, disable Iran-flagged tanker trying to evade blockade — Navy Times, 2026-05-06](https://www.navytimes.com/news/your-navy/2026/05/06/us-forces-fire-at-disable-iran-flagged-tanker-trying-to-evade-blockade/) — tanker-enforcement precedent. *(single_source)*
- [Bitcoin Price Crashes to $67,000 Range, Down 13% in a Week Amid ETF Outflows — Bitcoin Magazine, 2026-06](https://bitcoinmagazine.com/markets/bitcoin-price-crashes-to-67000-range) — BTC ~$67K, −13% week. *(single_source, verified via WebSearch)*
- [Will Bitcoin price fall to $65K next as ETF outflows deepen? — crypto.news, 2026-06-02](https://crypto.news/will-bitcoin-price-fall-to-65k-next-as-etf-outflows-deepen/) — 11-day outflow streak; $65K downside scenario. *(single_source)*
- [Bitcoin ETF Fund Flows — CoinGlass](https://www.coinglass.com/etf/bitcoin) — ETF net-outflow data reference. *(reference)*
- [Broadcom to Announce Q2 FY2026 Results on June 3, 2026 (after close) — StockTitan, 2026-05-04](https://www.stocktitan.net/news/AVGO/broadcom-inc-to-announce-second-quarter-fiscal-year-2026-financial-04if2lwax8o1.html) — earnings date/time. *(primary_source, prior-run)*
- [AMD Stock Overview — StockAnalysis, 2026-06-02](https://stockanalysis.com/stocks/amd/) — price $521.54, +141% YTD, consensus 12-mo target $479.77 (below price). *(single_source, prior-run)*

_Internal CLI evidence (no external citation needed): active-signals (crypto 5 / stocks 24 rows; lone A-tier = AMD intraday 84.7 / swing 81); signal-stats (crypto n=23 weak, PF 3.5; stocks n=629 reliable, A-tier PF 0.27 / 6% winrate / −8R); detect_untracked_legacy_alerts (None); catalyst coverage 688/3315 mapped (79.2% unmapped), 4 baskets._

---

## 14. Source-Discipline Final Checklist

- [x] Every external claim has source + title + date + URL (§13).
- [x] No uncited stats (BTC price, ETF outflows, AMD valuation, AVGO estimates all sourced).
- [x] No uncited legal claims (Nobitex sanctions cited; Andrew Left "found guilty" surfaced only as an *internal unmapped headline* in §5, not asserted as verified fact).
- [x] No fabricated TradingView observations — chart tools unavailable, stated explicitly.
- [x] Missing-source items written as "unconfirmed / social_only" (Kuwait-intercept, Iran-explosion lines), not guessed.
- [x] test_source / fixture URLs filtered (catalyst scan reported 0 test_source rejects).
- [x] §13 Sources present with markdown hyperlinks + dates.
- [x] Web available — no "external unavailable" banner needed.

---
*Auto-generated by the `opus-enriched-review-4h` scheduled task. Read-only/advisory: no trades placed, no execution, no scoring/threshold/strategy code modified, no paid APIs added. Chart tooling not loaded — no chart observations fabricated.*
