# Opus Enriched Review — late-session risk review — Auto Cycle 21:39 EEST

_Slot: 21:30 late-session risk review · Friday 2026-06-12 · ~14:39 ET, ~2h into US RTH with ~2h20m left to the cash close (23:00 EEST / 16:00 ET). Focus: late-session risk / exposure — active signals near TP / stop / invalidation; keep-watching vs avoid-new vs wait-for-close; intraday signals too late to enter; crypto evening continuation vs reversal; flag stale setups; check whether no-entry signals are still valid or should expire. Advisory-only, read-mostly — no auto-trade, no code edits, paper-trading. §14 TODOs only, no fixes._

## 1. Executive Summary

**Late-session read: this is a manage-exposure / no-new-chase window, not a fresh-entry window.** External research **AVAILABLE** this run (WebSearch ×3 + WebFetch verified, §13).

**The strongest single-name story is AMD, and it is genuinely catalyst-backed — but the move has already happened.** Verified externally (§13): on 2026-06-12 **Citi upgraded AMD Neutral→Buy, $575 PT**, citing AMD as a credible second-source AI GPU vendor and **Meta deploying up to 6GW of AMD Instinct (MI1450) GPUs**; AMD is **+4.71% on the day**, intraday range **$490.85–$521.69, last ~$514.80**. Internal A-tier **AMD intraday long (sc=80.63, created 17:35 UTC, entry 512.21–517.95, inval 500.74, `waiting_for_entry`)** has its lower band right at current price. **This is a real catalyst — unlike the structural NVDA/SMH A-tier losers the report warns about — but +4.71% with price near the intraday high ($521) means entering at market here is chasing a reacted move.** Routed verdict: **AMD long is actionable only on a pullback/retest into ~506–513 that holds**, or a clean break-and-hold above 514–517 late in the day; **do not chase ~520+.**

**The second A-tier — JPM intraday long (sc=80.82, created 14:17 UTC, entry 315.40–316.58, inval 313.04) — is NOT triggered and is red on the day.** External (§13): **JPM ~$312.37, down ~1.1% intraday**, i.e. **below both the A-entry (315.40) and the newer B-entry (318.59–319.74).** JPM is an RS leader vs financials (a strong sector) with constructive bank commentary, but at –1.1% it has not reclaimed the entry zone → **wait-for-trigger, reclaim 315.40+; no chase, no late-session market entry.** Earnings Jul 14 → safe.

**Crypto = chop with a risk-off overhang — caution into the evening.** Internal desk (16:45 UTC) prints **BTC transition_up / ETH range / altcoin breadth 53% > EMA20** (mild), recommended style "mean reversion or wait for clean breakouts." But external macro (§13) is clearly **risk-off**: **record spot-BTC ETF outflows (~$2.97B over 10 sessions, ~$5.4B over 4 weeks)**, strong US jobs trimming rate-cut odds, Iran risk-off — and the internal lookonchain catalyst confirms it (**1D −1,423 BTC / 7D −12,045 BTC ETF netflow**). **The internal "transition_up" is a short-term bounce inside a risk-off tape → favor only RS-leader longs with confirmation; do NOT add no-catalyst momentum longs in chop (14d no-news cut: WR 23% / PF 0.70 / −3R).** The only fresh crypto **LONG** idea is **ALLO/USDT** (RS leader, +8%/24h, vol 5.91×) — best long-watch, but no catalyst → breakout-confirmation only. All other crypto ideas are watchlist-only.

**No clean short this window.** Stock shorts all rejected for `rr_below_1.5` (PLTR/META/XOM/NFLX/AVGO); crypto weak names already dumped hard (**HMSTR −25%, EPIC −19%, BANANAS31 −14%**) → overextended, too late to short. Short-watch: none actionable.

**Active-book risk (late-session):** crypto B-tier book is in decent shape — several at TP (ATOM/CRV/CHZ/ALT/BAND `tp*`), **XPL triggered and +41%/24h = overextended, manage/trail not add.** Stock B-tier **DIA & LLY long triggered (in-trade)**; older **AMD/JPM B at tp2_hit (in profit).** New intraday entries with ~2h left are **late** — prefer manage-existing / wait-for-close over initiating.

**System health:** untracked-alert detector **clean (0)** — no PART-1 regression. Scheduler **fresh** (~1.5h, last cycle 20:10). Catalyst mapping **weak — 77.6% unmapped (2472/3186)** → **catalyst layer = context only, not a decision input** this run (recurring; §14 TODO persists). Paper books: crypto A/B **PF 1.30 / +6R but WR 19.7%, shorts subset losing (PF 0.42)**; stocks A/B **PF 1.12 / +2R, WR 30.2%; A-tier still 0-win small-sample (n=3, PF 0.0)** — A-tier-overpromotion caution stands, but AMD's verified catalyst differentiates it.

**Routed verdict (this decision window only — never a stop command):**
- **Best long:** **AMD** (verified Citi/Meta catalyst, semis strongest sector) — **pullback-only into ~506–513, or break-hold >514**; no chase near 520+.
- **Best short:** **none clean** — stock shorts fail RR; crypto weak names overextended. Short-watch: re-check only on a *fresh* failed retest, none present now.
- **Best catalyst-backed:** **AMD** (Citi Neutral→Buy $575, Meta 6GW Instinct GPU — verified §13).
- **What to avoid:** chasing AMD ~520+; market-entering JPM below its zone; chasing **XPL/TRUMP** extended crypto pumps (+41%/+22%); no-catalyst crypto momentum longs in chop; initiating fresh intraday stock entries with ~2h to close.
- **What would change the view:** **AMD pullback into 506–513 holding** → actionable long; **JPM reclaiming 315.40** → trigger live; **BTC losing the bounce / ETF outflows accelerating** → full risk-off, fade crypto longs; **US breadth narrowing into the close** → trim/avoid.

## 2. Data Used

- Crypto **scalp** — `data/reports/scalp/2026-06-12_16-51_scalp_report.md` (mtime 19:51) — **fresh** (~1.8h). Regime transition_up/range chop; breadth 53% > EMA20.
- Crypto **intraday** — `data/reports/intraday/2026-06-12_17-01_intraday_report.md` (mtime 20:01) — **fresh** (~1.6h). BTC transition_up, ETH range; only LONG idea ALLO, rest watchlist-only.
- Crypto **swing** — `data/reports/swing/2026-06-12_14-28_swing_report.md` (mtime 17:28) — **carry-forward** (~4.2h, flagged §3).
- **Stocks intraday** — `data/reports/stocks/intraday/2026-06-12_18-28_stocks_intraday_report.md` (mtime 21:28) — **very fresh** (~11 min, RTH). Regime chop (VIX 18.29, breadth 75% > EMA20); A/B = AMD + JPM longs.
- **Stocks swing** — `..._14-34_stocks_swing_report.md` (mtime 17:34) — **carry-forward** (~4h); **stocks invest** — `..._14-38_` (mtime 17:38) — **carry-forward** (~4h).
- Catalysts — `data/catalysts/2026-06-12/` (events.jsonl 3186 lines + narrative_baskets.jsonl 6 baskets + `catalyst_cycle_17-01.md`, mtime 20:01) — **fresh** (~1.6h). `catalyst-scan` NOT re-run (dir present).
- LLM packets present: `data/processed/llm_analysis_packet.md`, `llm_stocks_packet.md`.
- CLI (this run): `active-signals` crypto (**12**, all B-tier) + stocks (**50**); `signal-stats` crypto + stocks; `detect_untracked_legacy_alerts --since 2026-06-12` (**clean — 0**). DB: `db/crypto_ai_desk.sqlite`.
- Latest scheduler cycle: `data/scheduled_runs/2026-06-12_default_schedule/cycle_04_19-39_summary.md` (mtime 20:10).
- External: WebSearch ×3 (AMD Citi/Meta; JPM banks; BTC ETF outflows); WebFetch ×1 (TradingKey AMD — **opened, verified, cited §13**; invezz 403'd → swapped). External research **AVAILABLE**.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **2026-06-12 20:10:22**, latest `cycle_*_summary.md` mtime **20:10:20** — both **~1.5h old** → **fresh** (defer rule requires BOTH > 3h; not met → review proceeds).
- Reports: scalp/intraday/stocks-intraday **fresh** (≤1.8h); swing/stocks-swing/stocks-invest **carry-forward** (~4–4.2h, in the 4–12h band → used, flagged here; not stale-excluded).
- Catalysts + LLM packets fresh (~1.6h).

## 4. What Changed vs Previous Review

Prior: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-12_1839.md` (18:30 US-open reaction slot).

- **Slot shift:** US-open reaction (18:39) → late-session risk (21:39); ~3h later, now ~2h to the close.
- **AMD:** prior had AMD as a **B-tier pullback-only long** (entry 508.69–514.22). Now there is a **fresh A-tier AMD** (sc=80.63, entry 512.21–517.95) **AND** the external catalyst is now **fully verified (Citi Buy $575, Meta 6GW Instinct, +4.71%)** — thesis **upgraded & confirmed**, but the move is now **more reacted** (price ~514.80 near intraday high 521) → chase risk **higher** than at the open.
- **JPM:** prior flagged JPM A-tier entry "likely below market / chasing." **Now reversed** — JPM is **red on the day (~$312.37)** and sits **below** both A (315.40) and B (318.59) zones → from "above zone, chasing" to **"below zone, wait-for-reclaim, not triggered."** Thesis intact, trigger not met.
- **NFLX short:** prior best short-watch (B sc=71). This run NFLX short is **stopped** (DB) and the fresh report rejects all shorts (`rr_below_1.5`) → **removed** as a candidate.
- **Crypto macro:** prior read = risk-on relief bounce on Iran "war ended" (BTC ~$63.4K). This run the **ETF-outflow / risk-off overhang dominates** (record outflows, weaker rate-cut odds) → tone shifts **risk-on → cautious chop**. UNH stale-headline issue from prior **not re-surfaced** this run (UNH only appears as C-tier).
- **Crypto fresh long:** XPL (prior, +40% momentum) → still active & **triggered, now +41% = overextended/manage**; new fresh long-watch is **ALLO** (RS leader).
- **Catalyst mapping:** 76.7% unmapped (prior) → **77.6% unmapped** (this run) — persistently weak, §14 TODO stands.
- **System health:** untracked-alert detector **clean (0)** both runs; scheduler fresh both runs.
- **Confirmed:** semis/financials/healthcare strongest sectors; A-tier small-sample 0-win caution. **Invalidated:** none.

## 5. Catalyst Coverage

- Latest cycle `catalyst_cycle_17-01.md`: scanned 500 `news_items`, **500 catalyst events**, **6 narrative baskets**.
- Cumulative `catalyst_events.jsonl` today: **total 3186 | mapped (symbol) 714 | unmapped 2472 → 77.6% unmapped.**
- **⚠ Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped > 50%)
- Top 3 unmapped headlines: "Why Viasat Stock Went to the Moon Today"; "Amazon's Hidden Anthropic Stake Could Be Worth More Than Investors Realize"; "Why Stitch Fix Stock Surged Today".
- Narrative baskets: `binance_ecosystem_teaser` (BNB/ASTER, <1h, sell-the-news risk), `delisting_thin_liquidity` (XRP, avoid), `ai_narrative` (NEAR/RENDER/TAO/FET, <6h), `rwa_narrative` (ONDO/XLM, <6h), `perps_dex_narrative` (HYPE, <6h), `momentum_breakout` (TRUMP +22.5% / ZBT +15% — pure momentum, wait_pullback).
- Mapped catalysts of note: **ALGO** partnership (Algorand × Token Terminal, importance 0.67 — real but low-tier); BTC ETF netflow; legal_risk Kenneth Leech SEC-obstruction guilty plea (not a tradable single-name here).

## 6. Market Landscape

- **Stocks (RTH, very fresh 21:28):** regime **chop**, bias neutral, VIX **18.29**, breadth **75% > EMA20 / 100% > EMA50**. Indices: SPY range (5d +0.43%), QQQ range (+2.21%), **IWM uptrend (+4.12%), DIA uptrend (+0.70%).** Strongest sectors **semis (SMH RS +8.21%), healthcare (XLV +5.88%), financials (XLF +4.75%)**; weakest **communications (XLC −3.46%).** No near-term earnings on the 18 tracked names.
- **Crypto (fresh 16:45):** BTC **transition_up**, ETH **range**, altcoin breadth **53% > EMA20 / 38% > EMA50**, BTC ATR pct 41 (normal). Strongest: ALLO (+8%, vol 5.9×), CHZ (vol 3.9× but −7%, breakdown), TRUMP (+22.5%), XPL (+41.5%). Weakest (already dumped): HMSTR −25%, EPIC −19%, BANANAS31 −14%. **Risk-off macro overhang** (ETF outflows §13).

### Market Mood / Risk Routing
- **Crypto mood:** **chop / risk-off-overhang** (internal transition_up bounce vs external record ETF outflows + risk-off macro → net cautious chop).
- **Stocks mood:** **chop** (neutral bias, late US session, VIX 18.3; semis/financials/healthcare leading).
- **Dominant narrative:** AI-GPU single-name strength (**AMD Citi/Meta**) inside a broad-index chop; crypto ETF-outflow risk-off.
- **Preferred side now:** **longs in RS-leaders with catalyst, on pullback/confirmation** · otherwise **wait-for-trigger / manage existing**.
- **Best long candidate:** **AMD** — pullback into ~506–513 or break-hold >514 (no chase ~520+).
- **Best short candidate:** **none clean** — trigger: a *fresh* failed retest (none present; stock shorts fail RR, crypto weak names overextended).
- **Best catalyst-backed candidate:** **AMD** (Citi Neutral→Buy $575, Meta 6GW Instinct GPU — verified §13).
- **What to avoid:** chasing AMD ~520+; JPM market entry below zone; XPL/TRUMP extended crypto pumps; no-catalyst crypto momentum longs in chop; fresh intraday entries with ~2h to close.
- **What would change the view:** AMD pullback into 506–513 holding (long live); JPM reclaim 315.40 (trigger live); BTC losing the bounce / outflows accelerating (full risk-off); breadth narrowing into the close (trim/avoid).

## 7. Candidate Deep Dives (≤ 5)

### 7.1 AMD — stocks intraday long — A-tier (sc=80.63) · B-tier co-signal (77.73) — *best long / best catalyst-backed*
- **Signal:** A-tier `waiting_for_entry`, entry **512.21–517.95**, inval 500.74, created 17:35 UTC (~1h, fresh). B-tier co-signal entry 506.91–512.94 (price now above it). Targets (B idea): TP1 531.0 / TP2 543.1 / TP3 561.2. RS vs SPY +15.06%, RS vs sector +6.85%, semis strongest sector.
- **Catalyst (verified §13):** Citi **Neutral→Buy, $575 PT**; AMD a credible second-source AI GPU vendor; **Meta deploying up to 6GW AMD Instinct (MI1450) GPUs**; AI rev ramp cited to ~$33B (2027)/$50.8B (2028). AMD **+4.71%** on the day, intraday **490.85–521.69, last ~514.80**. Internal news confirms (Seeking Alpha "Citi upgrades on GPU potential" 07:23; MarketWatch 16:04).
- **Price-reaction / chase:** **Yes, price has largely reacted** (+4.71%, near intraday high 521). Setup is **chasing if entered at market now.** Pullback structure: a retest into 506–513 (B-zone / lower A-band) is the clean entry. Not >2 ATR from EMA20 yet, but extension is meaningful intraday.
- **Mood alignment:** **Yes** — RS-leader long with a real catalyst in the strongest sector = exactly the routed-preferred trade. **Long.** Actionable **only on pullback/confirmation**, not now at the high.
- **Invalidation:** close below 500.74 (A) / 494.86 (B).
- **LEGAL/HEADLINE RISK:** **none** — catalyst is a positive analyst upgrade; no indictment/SEC/fraud/auditor/delisting found (§13). Clean.
- **Verdict:** **ACTIONABLE on pullback into ~506–513 holding, or break-hold >514** — NOT a clean market entry at ~520. Late-session: ~2h to close → prefer a confirmed pullback over a chase.

### 7.2 JPM — stocks intraday long — A-tier (sc=80.82) · B-tier co-signal (65.09) — *wait-for-trigger*
- **Signal:** A-tier `waiting_for_entry`, entry **315.40–316.58**, inval 313.04, created 14:17 UTC. B-tier entry 318.59–319.74. RS vs SPY +7.61%, financials strong sector. Earnings Jul 14 → safe.
- **External (§13):** JPM **~$312.37, down ~1.1% intraday**, up ~2.6%/month; analyst Buy, ~9.5–20% upside; constructive bank commentary (Dimon "clients gung ho").
- **Price-reaction / chase:** price is **BELOW** both entry zones (312.37 < 315.40) → **not triggered, not reacted up.** Entering now would be *below* the planned long zone with no trigger — invalid per the playbook.
- **Mood alignment:** RS-leader long thesis intact, but **red on the day** → momentum not confirmed. **Wait-for-trigger.**
- **Invalidation:** close below 313.04.
- **LEGAL/HEADLINE RISK:** **none** found. Clean.
- **Verdict:** **WAIT-FOR-TRIGGER** — actionable only on a reclaim of **315.40+** with strength; no late-session market entry below the zone.

### 7.3 BTC / crypto macro — *risk context (not a trade)*
- **Internal:** BTC transition_up / ETH range / breadth 53% > EMA20; lookonchain catalyst **1D −1,423 BTC / 7D −12,045 BTC ETF netflow** (outflows).
- **External (§13):** **record spot-BTC ETF outflows (~$2.97B / 10 sessions, ~$5.4B / 4 weeks)**, strong US jobs trimming rate-cut odds, Iran risk-off; BTC quoted weak (~$61.7K on Jun 10 — note: 2-day-old price, the internal transition_up likely reflects a more recent bounce → **contradiction flagged**).
- **Verdict:** **risk-off overhang on crypto longs.** Internal bounce is real short-term but fragile; favor only RS-leader longs with confirmation, avoid no-catalyst momentum. Not a single-name trade — sets the cautious routing for the crypto book.

### 7.4 ALLO/USDT — crypto intraday long — *best crypto long-watch*
- **Signal:** report Trade Idea #1 (only non-watchlist LONG), RS leader, **+8.13%/24h, RS vs BTC +5.94%, volume 5.91×** (unusual volume, relative_strength tag). Playbook `crypto_intraday_catalyst_or_momentum`.
- **Catalyst:** **none fresh verified** → momentum-only. In chop, no-catalyst intraday is net-negative (WR 23% / PF 0.70).
- **Price-reaction / chase:** +8% with 5.9× volume = active move; entering mid-move risks chasing. Needs a **breakout-and-hold or pullback-hold** confirmation.
- **Mood alignment:** partial — RS-leader long fits the "longs only if RS-leader" routing, but lacks catalyst and sits under a risk-off macro overhang.
- **Verdict:** **LONG-WATCH** — actionable only on a clean breakout-hold (or pullback that holds) with sustained volume; not a fresh entry without confirmation.

### 7.5 ALGO/USDT — crypto B-tier long (catalyst-backed) — *catalyst-watch*
- **Signal:** 3 active B-tier signals (intraday/scalp/swing long, sc 65–69, `waiting_for_entry`). Catalyst: **Algorand × Token Terminal partnership** (CryptoBriefing 14:14 UTC, importance 0.67) — real but low-tier; also a low-quality "price prediction" headline (Benzinga, ignore).
- **Price-reaction / chase:** low-importance partnership, unlikely to drive a sustained move alone; ALGO not in the strongest-symbols list → no momentum confirmation.
- **Mood alignment:** catalyst-backed long fits routing, but the catalyst is weak and unconfirmed by price/volume.
- **Verdict:** **CATALYST-WATCH** — only if price/volume confirms the partnership narrative (entry-zone reclaim + RS turn); otherwise context, not an entry. Catalyst-mapping-weak caveat applies.

## 8. Best Candidates Ranked

1. **AMD (stocks, long)** — A-tier + **verified catalyst** (Citi Buy $575, Meta 6GW GPU), strongest sector. **Best overall — but pullback-only**: actionable into **~506–513 holding** or **break-hold >514**; not at ~520.
2. **JPM (stocks, long)** — A-tier RS-leader, clean, but **not triggered** (red on day). **Long-watch — trigger: reclaim 315.40+.**
3. **ALLO/USDT (crypto, long)** — RS-leader momentum, no catalyst. **Long-watch — trigger: breakout-hold with sustained 5×+ volume.**
4. **ALGO/USDT (crypto, long)** — weak partnership catalyst, no price confirmation. **Catalyst-watch — trigger: entry-zone reclaim + volume on the Token Terminal narrative.**

**No clean immediate entry this window.** Per PART 9:
- **Best long-watch:** AMD — trigger: pullback into 506–513 that holds, or break-hold above 514.
- **Best short-watch:** none — trigger: a *fresh* failed retest on a liquid name (none present; stock shorts fail RR, crypto weak names overextended).
- **Best catalyst-watch:** AMD (verified) primary; ALGO (weak) secondary — trigger: AMD pullback confirmation / ALGO price-volume confirmation.

## 9. Avoid / No Trade _(this decision window only — never "stop system")_

- **AMD at ~520+** — chasing a +4.71% reacted move near the intraday high; wait for pullback/break-hold.
- **JPM market entry below 315.40** — not triggered, red on day; would be entering below the planned long zone.
- **XPL/USDT (+41%/24h, triggered)** — overextended momentum; manage/trail if held, do not add.
- **TRUMP/USDT (+22.5%), ZBT (+15%)** — `momentum_breakout`, no confirmed catalyst, wait_pullback only.
- **Dumped crypto shorts (HMSTR −25%, EPIC −19%, BANANAS31 −14%)** — too extended to initiate short.
- **No-catalyst crypto momentum longs in chop** — net-negative bucket (WR 23% / PF 0.70).
- **Fresh intraday stock entries with ~2h to the close** — late; prefer manage-existing / wait-for-close.
- _Scanning, candidate generation, tracking, and monitors continue in all moods — this is a caution routing, not a stop._

## 10. Main Risks

- **Chase risk on AMD** — the catalyst is real but largely priced today; a late entry at the high is the single biggest avoidable error this window.
- **Crypto risk-off overhang** — record ETF outflows + weaker rate-cut odds; the internal "transition_up" bounce can fail → crypto longs fragile.
- **Late-session timing** — ~2h to the cash close; new intraday entries have little runway; manage exposure over initiation.
- **A-tier small-sample 0-win (n=3, PF 0.0)** — A-tier-overpromotion caution stands generically; AMD's verified catalyst is the exception, JPM is untriggered.
- **Catalyst mapping 77.6% unmapped** — catalyst layer unreliable as a decision input this run (context only).
- **Data:** swing/stocks-swing/invest are carry-forward (~4h); external BTC price quote is 2 days old (used only for the outflow backdrop, not a level). Ingest of cited sources **succeeded** (5 rows; no errors).

## 11. Action Plan — next 4 hours

1. **AMD:** set a **pullback alert into 506–513** (and a break-hold-above-514 alert); enter long only on a confirmed hold — **no chase ~520+.** Respect inval 500.74.
2. **JPM:** alert on **reclaim of 315.40+ with strength**; until then no action (red, untriggered).
3. **Manage open book into the close:** XPL (+41%, trail/manage, no add); DIA/LLY long triggered (let run to TP / honor invalidation); crypto names at `tp*` (ATOM/CRV/CHZ/ALT/BAND — bank/trail per plan).
4. **Crypto:** treat as cautious chop; **ALLO long-watch on breakout-hold**, ALGO catalyst-watch; avoid no-catalyst momentum longs and dumped-name shorts.
5. **Into the close (23:00 EEST):** prefer wait-for-close on undecided intraday ideas; re-evaluate at the post-close (23:15) slot.
6. Scanning/tracking/monitors continue unchanged.

## 12. Final Verdict per Mode

- **Crypto scalp:** cautious chop — **wait-for-breakout**; no fresh no-catalyst entries; manage existing.
- **Crypto intraday:** **ALLO long-watch on breakout-hold** (RS leader); ALGO catalyst-watch; risk-off overhang → no chase.
- **Crypto swing:** carry-forward (~4h) — no fresh action; range/transition, wait for clean structure.
- **Stocks intraday:** **AMD long — pullback-only (506–513 / break-hold >514), no chase**; **JPM long — wait reclaim 315.40**; all shorts rejected (RR). Late session → manage > initiate.
- **Stocks swing / invest:** carry-forward (~4h) — planning context only, no fresh confirmation this run.

## 13. Sources

- [AMD Is No Longer Just a CPU Stock, Says Citi — GuruFocus, 2026-06-12](https://www.gurufocus.com/news/8913952/amd-is-no-longer-just-a-cpu-stock-says-citi) — Citi Neutral→Buy, $575 PT, GPU $281/CPU $204 sum-of-parts. _single_source · confirms AMD long._
- [AMD moved up 4.71% on Jun 12 — TradingKey, 2026-06-12](https://www.tradingkey.com/news/market-movers/261964456-market-movers-amd-20260612) — **WebFetch-verified**: +4.71%, Citi Neutral→Buy, Meta GPU sales growth. _single_source · confirms (primary verification of the move)._
- [AMD stock surges as Citi sees major AI GPU opportunity with Meta — Invezz, 2026-06-12](https://invezz.com/news/2026/06/12/amd-stock-surges-5-as-citi-sees-major-ai-gpu-opportunity-with-meta/) — Meta up to 6GW AMD Instinct (MI1450); AI rev ramp. _single_source · confirms (note: URL returned 403 on fetch; corroborated by GuruFocus + TradingKey)._
- [JPMorgan Chase (JPM) quote — CNN Markets, 2026-06-12](https://www.cnn.com/markets/stocks/JPM) — ~$312.37, −1.1% intraday, analyst Buy, earnings Jul 14 2026. _single_source · confirms JPM below entry / untriggered._
- [Bitcoin Falls as Record ETF Outflows and Strategy Sale Hit Sentiment — Investing.com, 2026-06-12](https://www.investing.com/analysis/bitcoin-falls-as-record-etf-outflows-and-strategy-sale-hit-sentiment-200681446) — ~$2.97B / 10-session record outflow streak; risk-off. _single_source · contradicts internal transition_up (risk-off overhang)._
- [Bitcoin ETF Fund Flows — CoinGlass, 2026-06-12](https://www.coinglass.com/etf/bitcoin) — 4th consecutive negative week, ~$5.4B withdrawn. _single_source · confirms outflow backdrop._

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-mapping persistently weak — 77.6% of events unmapped this run (2472/3186), ~77% prior run; catalyst layer demoted to context-only repeatedly.
- **evidence:** `data/catalysts/2026-06-12/catalyst_events.jsonl` (mapped 714 / unmapped 2472); top unmapped have clear tickers ("Why Viasat Stock Went to the Moon Today", "Amazon's Hidden Anthropic Stake…", "Why Stitch Fix Stock Surged Today").
- **suggested manual fix:** strengthen the symbol resolver in the catalyst layer (company-name → ticker dictionary; headline-pattern "Why <Company> Stock …" extraction) to lift mapping above ~50%.
- **priority:** medium
- **first observed:** recurring (logged in prior reviews); re-confirmed 2026-06-12 21:39 EEST

### TODO-stocks-A-tier-zero-win
- **issue:** Stocks A-tier paper book remains 0-win (n=3, Total R −1.0, PF 0.0, WR 0%) while B-tier is positive (PF 1.20) — A-tier-overpromotion failure mode the report itself flags.
- **evidence:** `signal-stats --asset-class stocks` (By tier: A n=3 PF 0.0; B n=42 PF 1.20); report "Known failure mode: A-tier overpromotion on losing names."
- **suggested manual fix:** review A-tier promotion thresholds for stocks (sample still small, n=3 — gather more before tuning); confirm A-tier requires a *verified* catalyst, not score alone (AMD passes, generic NVDA/SMH longs don't).
- **priority:** low
- **first observed:** recurring; re-confirmed 2026-06-12 21:39 EEST

### TODO-duplicate-tier-signals-same-symbol
- **issue:** Same symbol/mode/direction carries both an A-tier and a B-tier `waiting_for_entry` signal with **different entry zones** (AMD: A 512.21–517.95 vs B 506.91–512.94; JPM: A 315.40–316.58 vs B 318.59–319.74), created at different cycles — can confuse "which zone is live" and double-count exposure.
- **evidence:** `proposed_signals` query (AMD A 17:35 UTC + B 14:17 UTC; JPM A 14:17 + B 14:45) — both active.
- **suggested manual fix:** consider superseding/expiring an older same-symbol/same-direction signal when a fresher one is emitted, or surface them as one merged idea with a zone range, to avoid ambiguous entries.
- **priority:** low
- **first observed:** 2026-06-12 21:39 EEST

_(All TODOs are advisory hand-offs for a separate elevated-permission session. No code edited this run.)_
