# Opus Enriched Review — post-close final daily review — Auto Cycle 23:24 EEST

_Slot: 23:15 post-close final daily review · Friday 2026-06-12 · ~16:24 ET, ~20 min after the US cash close (23:00 EEST / 16:00 ET). Focus: daily wrap — how the US session closed, what worked / failed today, end-of-day risk/exposure, overnight-into-Asia (here: into the **weekend**) crypto setup, what to avoid tomorrow. Advisory-only, read-mostly — no auto-trade, no code edits, paper-trading. §14 TODOs only, no fixes._

## 1. Executive Summary

**Daily wrap: the US cash session is closed and it is now a weekend window — stocks are planning-only until Monday, crypto is the lone live class, and the tape is risk-off chop.** External research **AVAILABLE** this run (WebSearch ×3 + WebFetch verified, §13).

**The trade of the day was AMD, and it worked — but it is now a closed-market, Monday-only idea.** Verified externally (§13): on 2026-06-12 **Citi upgraded AMD Neutral→Buy, $575 PT** on the **Meta up-to-6GW AMD Instinct (MI1450) GPU** deployment, and the upgrade was **broad, not a one-analyst event** — TD Cowen $600, Barclays $665, BofA $560, CFRA $600, Mizuho $615 all carrying elevated targets (§13). AMD closed **~$514.88, ~+3.85–4.7% on the day**, holding its gains into the bell. The desk's prior A-tier AMD long (entry 512.21–517.95) was thesis-correct, but the move is now **reacted and the market is closed** — there is no fresh entry tonight. **Monday gap risk is the dominant consideration: do not chase an AMD gap-up open; wait for a pullback-hold into ~506–513 or a clean break-hold above the prior high.**

**JPM — the other A-tier — never triggered today and closes the week red/flat below its zone.** External (§13): JPM ~**$312–313** (last indexed close $313.49 Jun 11; intraday red ~$312 today), i.e. **below the A-entry 315.40** all session. Thesis (RS-leader in a strong financial sector, earnings Jul 14 → safe) is intact, but the trigger never fired → **carry-forward wait-for-trigger; no weekend action; reclaim 315.40+ on Monday makes it live.**

**Crypto closes the week as risk-off chop — and that carries straight into a thin weekend.** Internal desk (19:15 UTC / 22:15 EEST) prints **BTC range / ETH range / altcoin breadth 57% > EMA20** (mildly constructive), style "mean reversion or wait for clean breakouts." But the external macro is unambiguously **risk-off**: **record spot-BTC ETF outflows — ~$1.72B for the week ending Jun 6 (largest weekly since Feb 2025), ~$5.4B over four consecutive negative weeks, IBIT leading** (§13); BTC chopping the **~$61–64K** band on an oversold relief bounce. **Net: the internal range is a fragile bounce inside a risk-off tape → favor only RS-leader longs with confirmation, and respect thin weekend liquidity (gappy, squeeze-prone both ways).**

**The day's crypto momentum standout is ORCA/USDT (+33%/24h, vol 9.2×) — but it is pure momentum, already extended, and flagged `momentum_breakout` / wait_pullback.** It is the best crypto long-*watch* into the weekend, **not** a fresh chase: the report itself rejected ORCA for ">2 ATR from EMA20; do not chase." No clean crypto A/B printed all day — every crypto idea is C-tier / watchlist.

**No clean short this window.** Stock shorts all rejected for `rr_below_1.5` (PLTR/META/XOM/NFLX); crypto weak names already capitulated hard today (**HMSTR −29%, BANANAS31 −20%, EPIC −14.5%, LUMIA −10%**) → overextended, too late to initiate. Short-watch: only a *fresh* failed retest, none present.

**System health clean.** Untracked-alert detector **0** — no PART-1 regression. Scheduler **fresh** (~44 min, last cycle 22:40). Catalyst mapping **weak — 78.2% unmapped (2882/3686)** → **catalyst layer = context only, not a decision input** this run (recurring; §14 TODO persists). Paper books (daily/weekly): crypto A/B **PF ~1.22 / +5R but WR ~20%, weak-setup subset losing (PF 0.42 / −4R)**; stocks A/B **PF ~1.12–1.20, B-tier WR ~31%, A-tier still 0-win small-sample**; stocks all-tier **−6R** — A-tier-overpromotion caution stands (AMD's verified catalyst is the exception that worked).

**Routed verdict (this decision window only — never a stop command):**
- **Best long:** **none clean for immediate entry** (US closed; crypto extended). **Long-watch: AMD** (Monday, pullback-only into ~506–513 / break-hold above prior high — no gap chase) and **ORCA/USDT** (crypto, only on a pullback-hold back toward its entry zone with sustained volume).
- **Best short:** **none clean** — stock shorts fail RR; crypto weak names already dumped. Short-watch: a *fresh* failed retest only (none now).
- **Best catalyst-backed:** **AMD** (Citi Neutral→Buy $575 + broad PT raises, Meta 6GW Instinct — verified §13) — but market-closed → Monday.
- **What to avoid:** chasing an AMD Monday gap-up; market-entering JPM below 315.40; chasing **ORCA +33%** / other extended crypto pumps; no-catalyst crypto momentum longs over a thin weekend; shorting already-dumped names.
- **What would change the view:** **BTC losing the ~$61K area / ETF outflows accelerating** → full risk-off, fade crypto longs; **BTC reclaiming and holding above the weekly range high with ETF flows turning** → re-open RS-leader longs; **ORCA pulling back and holding its entry zone** → actionable long-watch; **AMD pullback into 506–513 on Monday** → actionable.

## 2. Data Used

- Crypto **scalp** — `data/reports/scalp/2026-06-12_19-22_scalp_report.md` (gen 22:22 EEST) — **fresh** (~1h). Regime range/chop; breadth 57% > EMA20; no A/B, best watch ENJ 58.0.
- Crypto **intraday** — `data/reports/intraday/2026-06-12_19-31_intraday_report.md` (gen 22:31 EEST) — **fresh** (~53 min). BTC/ETH range; no A/B, best watch STG 53.1 / ENJ 52.8.
- Crypto **swing** — `data/reports/swing/2026-06-12_14-28_swing_report.md` — **carry-forward/borderline-stale** (~9h, flagged §3); not used for fresh verdict.
- **Stocks intraday** — `data/reports/stocks/intraday/2026-06-12_20-04_stocks_intraday_report.md` (data freshness 20:04 UTC = 23:04 EEST, **captures the close**) — **fresh**, explicitly **MARKET CLOSED — planning/watchlist only**. A/B = 0; AMD B (76.5) + JPM B (69.8) demoted; regime chop, VIX 18.21.
- **Stocks swing** — `..._14-34_` / **stocks invest** — `..._14-38_` — **carry-forward/stale** (~9h); planning context only.
- Catalysts — `data/catalysts/2026-06-12/` (events.jsonl **3686** lines + narrative_baskets.jsonl 6 baskets + `catalyst_cycle_19-31.md`, mtime 22:31) — **fresh** (~53 min). `catalyst-scan` NOT re-run (dir present).
- LLM packets present: `data/processed/llm_analysis_packet.md`, `llm_stocks_packet.md`.
- CLI (this run): `active-signals` crypto (**9**, all B-tier) + stocks (~24 rows, B = AMD/DIA/LLY + JPM-C/others); `signal-stats` crypto + stocks; `detect_untracked_legacy_alerts --since 2026-06-12` (**clean — 0**).
- Latest scheduler cycle: `data/scheduled_runs/2026-06-12_default_schedule/cycle_05_22-10_summary.md` (mtime 22:40).
- External: WebSearch ×3 (AMD close/Citi/Meta; BTC price/ETF outflows; JPM close); WebFetch ×1 (StocksToTrade AMD — **opened, verified, cited §13**). External research **AVAILABLE**.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **2026-06-12 22:40:27**, latest `cycle_*_summary.md` mtime **22:40:24** — both **~44 min old** → **fresh** (defer rule needs BOTH > 3h; not met → review proceeds).
- Reports: scalp/intraday/stocks-intraday **fresh** (≤1h; stocks captures the 20:04 UTC close). Swing/stocks-swing/stocks-invest **~9h** → carry-forward/borderline-stale, flagged, excluded from fresh swing/invest verdicts.
- Catalysts + LLM packets fresh (~53 min).

## 4. What Changed vs Previous Review

Prior: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-12_2139.md` (21:30 late-session risk slot).

- **Slot shift:** late-session risk (21:39, ~2h to close) → **post-close daily wrap** (23:24, ~20 min after close). The decision frame moved from "manage into the close" to "weekend carry + Monday setup."
- **AMD — resolved as the day's winner:** prior had AMD as the best long, pullback-only, with chase risk near the $521 intraday high. **Outcome:** AMD **held into the close ~$514.88 (+~3.85–4.7%)** and the upgrade proved **broad** (TD Cowen/Barclays/BofA/CFRA/Mizuho all elevated, not just Citi). Thesis **confirmed**; status moves from "live pullback idea" to **"closed-market, Monday pullback-only, gap risk."**
- **JPM — confirmed untriggered:** prior = below zone, wait-for-reclaim. **Outcome:** never reclaimed 315.40, closes the week red/flat ~$312–313 → **carry-forward wait-for-trigger** (unchanged thesis, trigger still unmet).
- **Crypto leader rotation:** prior crypto long-watch was **ALLO** (RS leader); this run's standout is **ORCA (+33%, vol 9.2×)** — a fresh `momentum_breakout` name, but extended/no-catalyst. XPL/TRUMP pumps from earlier (+41%/+22%) have **cooled** (XPL now ~+24%, TRUMP ~+15%) and dropped off the active-leader chase list.
- **Crypto macro:** risk-off overhang **persists and is reaffirmed** — record ETF outflows ($1.72B wk / $5.4B 4-wk) still the dominant external read; internal "transition_up" from the prior run has **softened to flat range** (BTC range, not transition_up).
- **Catalyst mapping:** 77.6% unmapped (prior) → **78.2% unmapped** (this run, 2882/3686) — persistently weak, §14 TODO stands.
- **System health:** untracked-alert detector **clean (0)** both runs; scheduler fresh both runs.
- **Confirmed:** semis/financials/healthcare strongest sectors; A-tier small-sample 0-win caution; AMD-as-verified-catalyst exception. **Invalidated:** none. **SMCI export-control indictment** legal_risk flag still present in catalyst notables (carry-forward; SMCI only a rejected short here).

## 5. Catalyst Coverage

- Latest cycle `catalyst_cycle_19-31.md`: scanned 500 `news_items`, **500 catalyst events**, **6 narrative baskets**.
- Cumulative `catalyst_events.jsonl` today: **total 3686 | mapped (symbol) 804 | unmapped 2882 → 78.2% unmapped.**
- **⚠ Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped > 50%)
- Top 3 unmapped headlines (clear tickers, resolver miss): "Why Viasat Stock Went to the Moon Today"; "Amazon's Hidden Anthropic Stake Could Be Worth More Than Investors Realize"; "Why Stitch Fix Stock Surged Today."
- Top mapped symbols by event count: BTC 304, TSLA 54, ETH 53, XRP 45, HYPE 32, UNH 26, SOL 25, NVDA 25, SMCI 21, AVAX 21.
- Narrative baskets: `binance_ecosystem_teaser` (BNB/ASTER, <6h, sell-the-news risk), `delisting_thin_liquidity` (XRP, avoid), `ai_narrative` (NEAR/RENDER/TAO/FET, <6h), `rwa_narrative` (ONDO/XLM, <24h), `perps_dex_narrative` (HYPE + DYDX/GMX/ASTER, <24h — SpaceX-IPO/$SPCX-on-Hyperliquid driven), `momentum_breakout` (**ORCA +33.2% vol 9.2×**, <1h — pure momentum, wait_pullback).
- Top mapped catalysts of note: **AMD** analyst_action (Citi Buy $575 / Meta GPU, importance 0.69/0.66 — verified, **worked**); **ALGO × Token Terminal** partnership (0.65, low-tier); **Metaplanet** securities-arm via Siiibo (BTC, 0.66); legal_risk **Kenneth Leech SEC-obstruction guilty plea** + **Tennessee crypto Ponzi indictment** (basket, not single-name tradable).

## 6. Market Landscape

- **Stocks (closed, snapshot 20:04 UTC / 23:04 EEST):** regime **chop**, bias neutral, VIX **18.21**, breadth **100% > EMA20 / 100% > EMA50** (narrow-but-up indices). SPY range (5d +0.57%, 20d −0.86%), QQQ range (5d +2.31%), **IWM uptrend (+4.02%), DIA uptrend (+0.66%)**. Strongest sectors **semis (SMH RS +8.05%), healthcare (XLV +5.75%), financials (XLF +4.86%)**; weakest **communications (XLC −3.89%)**. No near-term earnings on the 18 tracked names. **Event of the day: SpaceX IPO (SPCX) on Nasdaq — Musk becomes first trillionaire** — fed the AI/perps-DEX euphoria (HYPE/$SPCX), not a desk single-name.
- **Crypto (fresh 19:15 UTC):** BTC **range**, ETH **range**, altcoin breadth **57.45% > EMA20 / 42.55% > EMA50**, BTC ATR pct 41 (normal). Strongest: **ORCA (+33%, vol 9.2×)**, STG (+10.7%, 7d +166%), TRUMP (+15%), ENJ (+18.9%), ZBT (+15%), XPL (+24%). Weakest (capitulated today): HMSTR −29%, BANANAS31 −20%, EPIC −14.5%, LUMIA −10%, KAT −9%. **Risk-off macro overhang** (record ETF outflows §13). Memes narrative rising (DOGE, Musk-trillionaire driven); AI mixed.

### Market Mood / Risk Routing
- **Crypto mood:** **chop / risk-off-overhang** (internal flat range + 57% breadth vs external record ETF outflows + thin weekend → net cautious chop).
- **Stocks mood:** **closed** (weekend; was **chop/neutral** at the bell, VIX 18.2, semis/financials/healthcare-led).
- **Dominant narrative:** AI-GPU single-name strength (**AMD**, broad PT raises) + **SpaceX-IPO euphoria** (SPCX / HYPE perps) inside a broad-index chop; crypto **ETF-outflow risk-off**.
- **Preferred side now:** **wait-for-trigger / manage existing** into the weekend · crypto: **RS-leader longs only on a pullback-hold**, clean shorts only on a *fresh* failed retest.
- **Best long candidate:** **none clean now** — long-watch **AMD** (Monday, pullback into ~506–513 / break-hold above prior high, no gap chase) · **ORCA/USDT** (pullback-hold to entry + sustained volume).
- **Best short candidate:** **none clean** — trigger: a *fresh* failed retest on a liquid name (none; stock shorts fail RR, crypto weak names overextended).
- **Best catalyst-backed candidate:** **AMD** (Citi Buy $575 + broad PTs, Meta 6GW Instinct — verified §13; market-closed → Monday).
- **What to avoid:** AMD Monday gap-up chase; JPM market entry below 315.40; ORCA +33% / extended crypto pumps; no-catalyst crypto momentum longs over thin weekend; shorting already-dumped HMSTR/EPIC/BANANAS31.
- **What would change the view:** BTC losing ~$61K / outflows accelerating (full risk-off); BTC reclaiming + holding the weekly range high with flows turning (re-open RS-leader longs); ORCA pullback-hold (long-watch live); AMD pullback into 506–513 Monday (long live).

## 7. Candidate Deep Dives (≤ 5)

### 7.1 AMD — stocks intraday long — *day's winner / best catalyst-backed (market-closed → Monday)*
- **Signal:** B-tier (76.46, demoted post-close) `waiting_for_entry`, entry ~512–518 zone (prior A-tier), RS vs SPY strong, semis strongest sector. A/B demoted to C at close per the report's market-closed rule.
- **Catalyst (verified §13):** Citi **Neutral→Buy $575** on **Meta up to 6GW AMD Instinct (MI1450)** deployment; AMD a credible second-source AI-GPU vendor; AI rev ramp ~$33B (2027)/$50.8B (2028). **Broad** PT support (TD Cowen $600, Barclays $665, BofA $560, CFRA $600, Mizuho $615). Also a £2B UK AI-infra investment headline. Closed **~$514.88, +~3.85–4.7%**, held into the bell.
- **Price-reaction / chase:** **fully reacted** (two-day surge off low-$400s; near the day's high at close). Entering a Monday gap-up would be chasing. Clean entry = pullback-hold into ~506–513 or break-hold above the prior high.
- **Mood alignment:** **Yes** — RS-leader long with a real, broad catalyst in the strongest sector. **Long.** But **market is closed** → no action until Monday.
- **Invalidation:** prior A/B inval ~500.74 / 494.86.
- **LEGAL/HEADLINE RISK:** **none** — positive analyst catalyst; no indictment/SEC/fraud/auditor/delisting (§13). Clean.
- **Verdict:** **WATCH (Monday) — pullback-only into ~506–513 or break-hold above prior high; do NOT chase a gap-up open.** Today's thesis = confirmed/worked.

### 7.2 JPM — stocks intraday long — A-tier (untriggered) — *carry-forward wait-for-trigger*
- **Signal:** A/B `waiting_for_entry`, A-entry **315.40–316.58**, inval 313.04; B-entry 318.59–319.74. RS-leader in strong financials, earnings Jul 14 → safe.
- **External (§13):** JPM ~**$312–313** (last close $313.49 Jun 11; red ~$312 intraday today) — **below the A-entry all session, never triggered.**
- **Price-reaction / chase:** price **below** the zone → not triggered, not reacted up. A market entry would be below plan.
- **Mood alignment:** thesis intact (RS-leader, strong sector) but momentum unconfirmed (red on day). **Wait-for-trigger.**
- **Invalidation:** close below 313.04.
- **LEGAL/HEADLINE RISK:** **none** found. Clean.
- **Verdict:** **CARRY-FORWARD WAIT-FOR-TRIGGER — reclaim 315.40+ with strength (Monday) makes it live; no weekend/gap action.**

### 7.3 BTC / crypto macro — *overnight-into-weekend risk context (not a trade)*
- **Internal:** BTC range / ETH range / breadth 57% > EMA20; mean-reversion style. Macro risk 35/100 (1 risk-off hit).
- **External (§13):** **record spot-BTC ETF outflows — ~$1.72B wk-ending-Jun-6 (largest since Feb 2025), ~$5.4B over 4 consecutive negative weeks, IBIT leading**; BTC chopping **~$61–64K** on an oversold relief bounce (SpaceX-IPO "$64K" headline internal). Risk-off backdrop intact.
- **Price-reaction / chase:** the internal range is a fragile bounce inside a risk-off, outflow-driven tape; thin weekend liquidity amplifies both squeezes and flushes.
- **Verdict:** **risk-off overhang on crypto longs into the weekend.** Favor only RS-leader longs with confirmation; avoid no-catalyst momentum; respect weekend gap risk. Sets the cautious routing for the whole crypto book — not a single-name trade.

### 7.4 ORCA/USDT — crypto long — *day's momentum standout / best crypto long-watch*
- **Signal:** strongest symbol both scalp & intraday (**score 100, +33.2%/24h, RS vs BTC +33%, volume 9.2×**, tags relative_strength/volume_expansion/breakout/**overextended**). `momentum_breakout` basket, playbook `wait_pullback`. **Rejected** in both reports: ">2 ATR from EMA20; do not chase → watchlist, wait for pullback."
- **Catalyst:** **none verified** — pure momentum cluster (basket explicitly "without confirmed news catalyst").
- **Price-reaction / chase:** **heavily reacted** (+33%, 9.2× vol, overextended). Entering now = textbook chase.
- **Mood alignment:** partial — RS-leader fits "longs only if RS-leader," but no catalyst + extended + risk-off macro + thin weekend = high failure risk.
- **Verdict:** **LONG-WATCH — only on a pullback that holds back toward the entry zone with sustained volume; not a fresh chase at +33%.**

### 7.5 ENJ/USDT — crypto scalp/intraday long — *secondary crypto long-watch*
- **Signal:** best watchlist name across scalp (58.0) and intraday (52.8); RS-leader **+17.96–18.85%/24h, RS vs BTC +17.8%**, uptrend, setup quality ~71. But **volume 0.25–0.33×** (below average) and **no catalyst** → status low-confidence/watchlist.
- **Catalyst:** none verified.
- **Price-reaction / chase:** up ~18% but on weak volume → unconfirmed; conditional pullback zone 0.0333–0.0344, inval 1h close beyond ~0.0322.
- **Mood alignment:** partial — RS-leader long, but thin volume + no catalyst + chop/risk-off → not actionable.
- **Verdict:** **LONG-WATCH — only if a pullback into 0.0333–0.0344 holds with a volume pickup; otherwise watchlist.**

## 8. Best Candidates Ranked

1. **AMD (stocks, long)** — A/B thesis **confirmed and worked today** (closed ~$514.88, +~4%, broad analyst PT raises). **Best name — but market-closed.** Monday: **pullback-only into ~506–513 / break-hold above prior high; no gap chase.**
2. **JPM (stocks, long)** — A-tier RS-leader, clean, **never triggered** (closed red/flat below zone). **Wait-for-trigger — reclaim 315.40+ (Monday).**
3. **ORCA/USDT (crypto, long)** — day's momentum leader (+33%, vol 9.2×), no catalyst, **overextended**. **Long-watch — pullback-hold to entry + sustained volume.**
4. **ENJ/USDT (crypto, long)** — best scalp/intraday watch name, RS-leader but thin volume / no catalyst. **Long-watch — pullback into 0.0333–0.0344 holding with volume.**

**No clean immediate entry this window** (US closed; crypto extended/risk-off). Per PART 9:
- **Best long-watch:** **AMD** — trigger: Monday pullback into ~506–513 that holds (or break-hold above the prior high); **ORCA** — trigger: pullback-hold to entry with 5×+ volume.
- **Best short-watch:** **none** — trigger: a *fresh* failed retest on a liquid name (none present; stock shorts fail RR, crypto weak names overextended/already dumped).
- **Best catalyst-watch:** **AMD** (verified Citi/Meta + broad PTs) — trigger: Monday pullback confirmation, not a gap chase.

## 9. Avoid / No Trade _(this decision window only — never "stop system")_

- **AMD Monday gap-up chase** — reacted +~4% two-day move at the highs; wait for pullback/break-hold.
- **JPM market entry below 315.40** — never triggered, closed red/flat; would be entering below the planned zone.
- **ORCA/USDT (+33%, vol 9.2×)** — overextended `momentum_breakout`, no catalyst; wait_pullback only.
- **Other extended crypto pumps (XPL ~+24%, TRUMP ~+15%, STG, ZBT +15%)** — momentum without confirmed catalyst; pullback only.
- **Already-dumped crypto shorts (HMSTR −29%, BANANAS31 −20%, EPIC −14.5%, LUMIA −10%)** — too extended to initiate short.
- **No-catalyst crypto momentum longs over a thin weekend** — net-negative bucket (weak-setup PF 0.42 / −4R) amplified by weekend gap risk.
- **Thin-liquidity / delisting names (XRP `delisting_thin_liquidity` basket, MEXC high-risk discovery names)** — avoid chasing low-float dumps.
- _Scanning, candidate generation, tracking, and monitors continue in all moods — this is caution routing, not a stop._

## 10. Main Risks

- **Weekend gap risk** — Friday close into a thin, ETF-outflow-pressured weekend; both squeezes and flushes are amplified, and Monday can gap stocks away from tonight's levels (esp. AMD).
- **Crypto risk-off overhang** — record ETF outflows ($1.72B wk / $5.4B 4-wk, IBIT-led); the internal range is a fragile relief bounce → crypto longs fragile, BTC ~$61K is the line.
- **Chase risk on the day's leaders** — AMD (reacted) and ORCA (+33% extended) are the two most tempting and most chase-prone names; late entry at the highs is the biggest avoidable error.
- **A-tier small-sample 0-win** (stocks) + crypto B-tier WR ~20% — A-tier-overpromotion caution stands; AMD's verified catalyst is the exception that worked, not a green light for score-only A-tiers.
- **Catalyst mapping 78.2% unmapped** — catalyst layer unreliable as a decision input this run (context only).
- **Data:** swing/stocks-swing/invest are ~9h (carry-forward/borderline-stale, excluded from fresh verdicts); external BTC price is a band, not a precise level. Source ingest result logged in §14.

## 11. Action Plan — next 4 hours (overnight → weekend)

1. **Crypto (only live class):** treat as cautious chop / risk-off. **ORCA & ENJ long-watch on a pullback-hold with volume** — no chase. Avoid no-catalyst momentum longs and already-dumped shorts. Respect BTC ~$61K as the risk line and weekend gap risk.
2. **BTC:** alert on a **loss of ~$61K** (full risk-off, fade longs) and on a **reclaim-and-hold of the weekly range high with ETF flows turning** (re-open RS-leader longs).
3. **AMD (Monday):** set a **pullback alert into ~506–513** and a **break-hold-above-prior-high** alert; **no gap-up chase**; respect inval ~500.74.
4. **JPM (Monday):** alert on **reclaim of 315.40+ with strength**; until then no action.
5. **Manage open book over the weekend:** crypto B-tier names at `tp*` (ATOM/CRV/CHZ/ALT/BAND — bank/trail per plan); stock DIA/LLY triggered intraday now in weekend hold (honor invalidation Monday). No fresh weekend stock entries (market closed).
6. **Re-evaluate at the 04:30 Asia/overnight slot** — check whether the crypto bounce held or BTC broke down overnight. Scanning/tracking/monitors continue unchanged.

## 12. Final Verdict per Mode

- **Crypto scalp:** cautious chop / risk-off — **wait-for-pullback**; no fresh no-catalyst entries; ORCA/ENJ long-watch on pullback-hold; manage existing.
- **Crypto intraday:** same — **ORCA long-watch (pullback-hold + volume)**, ENJ secondary; risk-off overhang + thin weekend → no chase.
- **Crypto swing:** carry-forward/borderline-stale (~9h) — no fresh action; range, wait for clean structure.
- **Stocks intraday:** **MARKET CLOSED — planning only.** AMD = day's winner, Monday pullback-only (no gap chase); JPM = wait reclaim 315.40; all shorts rejected (RR).
- **Stocks swing / invest:** carry-forward/stale (~9h) — planning context only, no fresh confirmation; re-evaluate on Monday's open.

## 13. Sources

- [AMD Stock Jumps As Wall Street Supercharges AI Price Targets — StocksToTrade, 2026-06-12](https://stockstotrade.com/news/advanced-micro-devices-inc-amd-news-2026_06_12/) — **WebFetch-verified**: AMD ~$514.88, +3.85% (close-day snapshot); broad PT raises TD Cowen $600 / Barclays $665 / BofA $560 / CFRA $600 / Mizuho $615; £2B UK AI-infra. _single_source · confirms AMD worked._
- [AMD stock surges as Citi sees major AI GPU opportunity with Meta — Invezz, 2026-06-12](https://invezz.com/news/2026/06/12/amd-stock-surges-5-as-citi-sees-major-ai-gpu-opportunity-with-meta/) — Citi Neutral→Buy, $575 PT; Meta up to 6GW AMD Instinct (MI1450). _single_source · confirms catalyst._
- [AMD Is No Longer Just a CPU Stock, Says Citi — GuruFocus, 2026-06-12](https://www.gurufocus.com/news/8913952/amd-is-no-longer-just-a-cpu-stock-says-citi) — Citi Buy $575, GPU sum-of-parts. _single_source · confirms catalyst._
- [JPMorgan Chase (JPM) historical price — StockAnalysis, 2026-06-12](https://stockanalysis.com/stocks/jpm/history/) — last close $313.49 (Jun 11); intraday ~$312 red Jun 12, below A-entry 315.40. _single_source · confirms JPM untriggered._
- [Bitcoin Falls as Record ETF Outflows and Strategy Sale Hit Sentiment — Investing.com, 2026-06-12](https://www.investing.com/analysis/bitcoin-falls-as-record-etf-outflows-and-strategy-sale-hit-sentiment-200681446) — record outflow streak, risk-off. _single_source · confirms risk-off overhang._
- [Bitcoin ETF Outflows June 2026: Record $1.72B Weekly Exit — BitcoinFoundation, 2026-06-12](https://bitcoinfoundation.org/news/crypto-etfs-news/etf-outflows-june-2/) — ~$1.72B wk-ending-Jun-6 (largest since Feb 2025), ~$5.4B / 4 wks, IBIT-led. _single_source · confirms outflow backdrop._

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-mapping persistently weak — **78.2% of events unmapped this run (2882/3686)**, ~77–78% across prior runs today; catalyst layer demoted to context-only repeatedly.
- **evidence:** `data/catalysts/2026-06-12/catalyst_events.jsonl` (mapped 804 / unmapped 2882); top unmapped have clear tickers ("Why Viasat Stock Went to the Moon Today", "Amazon's Hidden Anthropic Stake…", "Why Stitch Fix Stock Surged Today").
- **suggested manual fix:** strengthen the symbol resolver (company-name → ticker dictionary; headline-pattern "Why <Company> Stock …" extraction) to lift mapping above ~50%.
- **priority:** medium
- **first observed:** recurring (logged in prior reviews); re-confirmed 2026-06-12 23:24 EEST

### TODO-stocks-A-tier-zero-win
- **issue:** Stocks A-tier paper book remains 0-win small-sample while B-tier is positive (B-tier WR ~31%, PF ~1.20) — A-tier-overpromotion failure mode the report flags. Stocks all-tier book closes the day **−6R** (n=338, PF ~0.9).
- **evidence:** `signal-stats --asset-class stocks` (tier B WR 31%; C WR 15%; all-tier Total R −6); report "Known failure mode: A-tier overpromotion on losing names."
- **suggested manual fix:** review A-tier promotion thresholds for stocks (small sample — gather more before tuning); confirm A-tier requires a *verified* catalyst, not score alone (AMD passes; generic NVDA/SMH longs don't).
- **priority:** low
- **first observed:** recurring; re-confirmed 2026-06-12 23:24 EEST

### TODO-crypto-weak-setup-bucket-losing
- **issue:** Crypto "weak setup" subset (no-catalyst momentum in chop) remains net-negative — **n=16, PF 0.42, −4R** — dragging the otherwise-positive crypto book (strong-setup subset n=53, PF 1.60, +9R).
- **evidence:** `signal-stats --asset-class crypto` By setup: strong n=53 PF 1.60 / +9R vs weak n=16 PF 0.42 / −4R; report "no-catalyst intraday in chop is net-negative (WR 23% / PF 0.70)."
- **suggested manual fix:** tighten or gate the no-catalyst momentum bucket in chop regimes (require RS-leader + breakout confirmation before B-tier promotion); sample now meaningful — candidate for review.
- **priority:** medium
- **first observed:** 2026-06-12 23:24 EEST

_(All TODOs are advisory hand-offs for a separate elevated-permission session. No code edited this run.)_
