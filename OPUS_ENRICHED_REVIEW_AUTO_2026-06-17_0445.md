# Opus Enriched Review — CRYPTO OVERNIGHT / ASIA REVIEW — Auto Cycle 04:45 EEST

_Generated 2026-06-17 ~04:45 EEST (01:45 UTC). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

## 1. Executive Summary

**Wed 2026-06-17, ~04:45 EEST "crypto overnight / Asia review" slot.** US cash market is **CLOSED** (overnight) → stocks are planning / carry-forward only; **crypto is the live actionable class.** External web research **AVAILABLE** this run (WebSearch ×3 + WebFetch HTTP 200 on CoinDesk).

**The one fact that frames tonight: today is FOMC day.** Per last night's post-close review, the **FOMC decision lands later today, Wed June 17 — Kevin Warsh's first meeting as chair; a rate hold is ~97–98% priced**, so the binary is the dot plot + tone, not the rate. The overnight-into-Asia tape is therefore a **pre-event coil, not a fresh trend leg.** That routes the decision to *RS-leader longs on pullbacks + wait-for-trigger*, **not** naked size ahead of the Fed.

**Crypto regime is genuinely risk-on but range-bound:** the desk prints **bullish trend (risk-on)** — BTC uptrend, ETH uptrend, altcoin breadth 70.5% > EMA20 (59% on the swing horizon), BTC ATR percentile 38 (normal vol). External tape confirms **BTC ~$65.5–66K, two-week high after the US-Iran/Strait-of-Hormuz de-escalation deal sent oil lower and lifted risk** ([CoinDesk 06-15](https://www.coindesk.com/markets/2026/06/15/bitcoin-hits-a-two-week-high-above-usd65-500-as-the-us-iran-deal-sends-oil-sliding)) — but BTC is **"not fully out of danger,"** with a June 19 signing pending and Trump warning he could restart strikes ([CoinDesk 06-15](https://www.coindesk.com/tech/2026/06/15/live-markets-bitcoin-not-fully-out-of-danger-as-trump-warns-of-further-iran-strikes)). The contradictory internal RSS headlines (BTC "below $73K panic" vs "past $65K surge") are **stale/noisy artifacts** — the verified current state is **risk-on, BTC mid-$65–66K, capped under the $67K pivot.**

**Best actionable read:** the **AI / perps-DEX narrative is the only place with both momentum AND a verified catalyst.** **WLD/USDT is the desk's #1 long across all three crypto modes** (scalp 74.0, intraday 71.8, swing) — RS-leader (+13% RS vs BTC), and the catalyst is externally confirmed: **WLD +12% on the day, ~180% on the month, as an AI-linked bet (Sam Altman / OpenAI)** ([CoinDesk 06-16](https://www.coindesk.com/markets/2026/06/16/hyperliquid-uniswap-and-worldcoin-buck-crypto-slump-as-traders-chase-ai-defi-trends)). The catch: **+180% monthly is overextended → this is a pullback-only idea, never a chase.** The day's repeated trap (per last night's grade) was chasing no-catalyst momentum pumps (SENT +28%, PORTAL +37%, HMSTR) — those remain **avoid/chase-risk** tonight.

No A-tier crypto anywhere. The lone A-tier in the active table — **JPM stocks intraday long (82.6)** — is **carry-forward / planning-only** (market closed; the fresh stocks report itself prints "No A/B-tier setups in this run"). **UNH carries a verified legal overhang (DOJ Medicare-fraud probe, −16%)** and must never surface as a clean long.

## 2. Data Used

- **Crypto scalp** `data/reports/scalp/2026-06-17_00-15_scalp_report.md` — **FRESH** (mtime 03:15 EEST, ~1.5h; data 00:00 UTC).
- **Crypto intraday** `data/reports/intraday/2026-06-17_00-23_intraday_report.md` — **FRESH** (mtime 03:23, ~1.4h).
- **Crypto swing** `data/reports/swing/2026-06-17_00-40_swing_report.md` — **FRESH** (mtime 03:40, ~1.1h).
- **Stocks intraday** `data/reports/stocks/intraday/2026-06-17_00-29_stocks_intraday_report.md` — **FRESH** (mtime 03:29, ~1.3h) — but market closed → planning only.
- **Stocks swing** `…00-45…` (mtime 03:45) + **invest** `…00-49…` (mtime 03:49) — **FRESH** but planning context (US closed overnight).
- **Catalysts** `data/catalysts/2026-06-17/`: `catalyst_cycle_00-23.md`, `catalyst_events.jsonl` (498 rows), `narrative_baskets.jsonl` (4 baskets). No catalyst-scan needed.
- **LLM packets** `data/processed/llm_analysis_packet.md` + `llm_stocks_packet.md` present.
- **Internal CLI:** `active-signals` crypto (**44 active, all long B**, scores 65–76) + stocks (**50 active**, mix C/B; **JPM A 80 intraday triggered**, AMD swing C 84, NFLX shorts C); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-17` → **None (clean)**.
- **DB** `db/crypto_ai_desk.sqlite` `news_items` 24h mention counts: **BTC 78, ETH 23, HYPE 19** (loudest), JPM 5, SENT 4, UNH 2, **WLD 1, JTO 1**, SMCI 0; telegram-source last 4h = 5 (all Lookonchain welcome-bot noise → no actionable t.me symbol news).
- **External:** WebSearch ×3 (WLD/HYPE/UNI rally; UNH DOJ probe; BTC Iran/Hormuz). WebFetch CoinDesk WLD article → **HTTP 200, used**.
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-17T0145Z_crypto.json` (3 sources) + `…_stocks.json` (1 source); both ingested OK (see §13).

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-16_default_schedule/`.
- `scheduler.log` mtime **03:50:32 EEST** (~0.9h) → **FRESH**.
- Latest `cycle_*_summary.md`: `cycle_06_03-04_summary.md` mtime **03:50:31 EEST** (~0.9h).
- **Defer rule needs BOTH log AND latest cycle > 3h. Both ~0.9h → review proceeds.**
- All six reports FRESH (1.1–1.5h). No stale/carry-forward freshness penalty this run; the only "carry-forward" caveat is **market-state** (US closed), not data age.

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-16_2324.md` (post-close daily wrap):

- **Window moved from post-close daily wrap → overnight / Asia pre-FOMC.** Posture shifts from "grade the day + set overnight plan" → **"manage the pre-FOMC coil; RS-leader pullback longs only, no naked size into the Fed."**
- **FOMC is now hours away (today), not "tomorrow."** The single dominant overhang is unchanged but imminent — keep size light into the decision.
- **WLD re-rated from "chase trap" → "catalyst-backed #1 long, pullback-only."** Last night WLD was flagged as a no-news momentum pump; this run it carries a **verified AI catalyst** ([CoinDesk 06-16](https://www.coindesk.com/markets/2026/06/16/hyperliquid-uniswap-and-worldcoin-buck-crypto-slump-as-traders-chase-ai-defi-trends)) and is #1 across all 3 modes. Nuance: the catalyst is real but the move is +180% monthly → still pullback-discipline, not chase.
- **SENT / PORTAL / HMSTR remain no-fresh-catalyst momentum** → still the chase-risk avoid bucket (consistent with last night's grade).
- **Untracked legacy alerts:** `--since today` → **None/clean** (vs cumulative 23 within 2026-06-16 last night). Different window; the cumulative climb remains a known §14 item to watch.
- **Catalyst unmapped 77.7% → 77.9%** — unchanged-bad; still context-only.
- **Active-signal count grew** (crypto 20→44, stocks →50) as the overnight cycles accumulated B/C ideas — still all crypto longs B-tier; no new crypto A-tier.
- **Confirmed:** crypto risk-on regime; BTC capped under $67K mid-$65–66K; AI/perps-DEX narrative leadership (WLD/HYPE/UNI); UNH legal overhang; JPM A-tier planning-only.

## 5. Catalyst Coverage

- `catalyst_events.jsonl` today: **498 rows**; mapped (non-null symbol): **110**; unmapped: **388 → 77.9% unmapped.**
- Narrative baskets: **4**.
- **⚠ catalyst mapping weak this run (77.9% unmapped) — use the catalyst layer as context, not the final decision.**
- Top 3 unmapped headlines: "White House's Anthropic move reignites AI debate in Congress" (imp 0.44); "US State Department steps in to help Vozinha's mother attend World Cup after visa barriers" (0.44); "Circle showcases AI agent's wallet capabilities with USDC transactions" (0.44).
- Active narrative baskets: **ai_narrative** (primary NEAR/RENDER/TAO/FET; related WLD/ASTER; `related_beta_rotation`, <24h), **perps_dex_narrative** (primary HYPE; related DYDX/GMX/ASTER; `wait_pullback`, <6h), **rwa_narrative** (primary ONDO/XLM; `related_beta_rotation`, <24h), **delisting_thin_liquidity** (`avoid_low_liquidity`, <6h).
- Top mapped catalysts by importance: **HYPE** Bitwise Hyperliquid ETF $108M AUM (0.78); **UNH** DOJ Medicare-fraud probe −16% (0.78, legal_risk); **SMCI** Form 8-K indictment re export-control conspiracy (0.77, legal_risk); AVAX FIFA/Kraken partnership (0.71).

## 6. Market Landscape

Crypto is in a **risk-on but range-bound, pre-event** state: bullish trend label, healthy breadth (70.5% > EMA20), normal vol — yet BTC is pinned mid-$65–66K under the $67K pivot, and **FOMC today caps fresh conviction.** Leadership is narrow and narrative-driven: **AI (WLD) + perps-DEX (HYPE)** carry both momentum and verified catalysts; the rest of the green tape (SENT, PORTAL, HMSTR) is thin-volume momentum with no fresh news. Stocks are closed; the only A-tier (JPM) is a planning carry-forward, and the loudest stock headline is a **negative legal one (UNH DOJ probe)**.

### Market Mood / Risk Routing      (REQUIRED)
- **Crypto mood:** **risk-on but range-bound / pre-event caution** (bullish trend, breadth 70%, BTC capped <$67K, FOMC today)
- **Stocks mood:** **closed** (overnight; JPM A-tier = planning carry-forward only)
- **Dominant narrative:** AI sector rotation (WLD/TAO/NEAR/RENDER) + perps-DEX (HYPE/UNI)
- **Preferred side now:** **RS-leader longs on pullbacks + wait-for-trigger** (no naked size into FOMC)
- **Best long candidate:** **WLD/USDT** — RS-leader + verified AI catalyst, BUT only on pullback into 0.658–0.667 (chase-risk above)
- **Best short candidate:** **none clean** — risk-on regime makes shorts counter-trend; short-watch = NEAR/USDT failed-bounce or BABY/SPCXB capitulation, but both are thin/low-liquidity → avoid initiating
- **Best catalyst-backed candidate:** **WLD/USDT** (CoinDesk AI) and **HYPE/USDT** (perps-DEX basket primary, ETF inflows) — HYPE is `wait_pullback` (+200% YTD, overextended)
- **What to avoid:** chasing no-catalyst pumps (SENT +28%, PORTAL +37%, HMSTR); thin/low-liq shorts; **UNH long** (DOJ legal overhang); **any naked size into the FOMC decision**
- **What would change the view:** FOMC outcome/tone (dovish → BTC tries $67K→$68.5–70K; hawkish → $64K→$63.3K); BTC reclaim & hold > $67K (risk-on confirm) or loss of $64K (risk-off flip); WLD pullback acceptance in zone vs. rejection

## 7. Candidate Deep Dives

### Candidate 1 — WLD/USDT — LONG (best long + best catalyst) — ACTIONABLE ON PULLBACK
- **Tier/source:** B-tier #1 in scalp (74.0), intraday (71.8), swing — triple-mode convergence. RS-leader tag.
- **Levels (intraday):** entry pullback **0.6579–0.6665**, current **0.6703**, invalidation **1h close < ~0.646**, TP1 **0.6893**, TP2 0.7083. ATR ~0.019; support 0.577 / resistance 0.687.
- **Catalyst (verified):** WLD +12% day / ~180% month as the market's most direct AI bet (Sam Altman / OpenAI); part of the AI/DeFi rotation ([CoinDesk 06-16](https://www.coindesk.com/markets/2026/06/16/hyperliquid-uniswap-and-worldcoin-buck-crypto-slump-as-traders-chase-ai-defi-trends), verification single_source / primary outlet). Internal `news_items` WLD 24h = 1 (thin internal coverage; externally corroborated).
- **Has price reacted?** Yes — heavily on the month (+180%). On the 24h it's a continuation, not a fresh breakout.
- **Chasing?** Yes if bought at/above 0.67 spot. **No** if filled on the 0.658–0.667 pullback.
- **Retest structure?** Yes — desk explicitly wants pullback acceptance, "no market buy if extended."
- **Overextended?** On the monthly timeframe, strongly. Intraday it sits just above the entry zone (not >2 ATR).
- **Mood-aligned?** Yes — RS-leader long fits risk-on routing.
- **Long/short/wait?** **Long, but wait-for-pullback-trigger.**
- **Invalidation:** 1h close below ~0.646; or BTC losing $64K (regime break).
- **Chase-risk:** HIGH if chased; LOW if pullback-disciplined.
- **Caveats:** volume 0.08–0.13× average (weak confirmation); FOMC today caps size.

### Candidate 2 — HYPE/USDT — catalyst-backed, WAIT-PULLBACK (basket primary)
- **Source:** `perps_dex_narrative` basket primary; not in the active crypto A/B trade list this cycle (it's the narrative leader, loudest name 19 mentions/24h).
- **Catalyst (verified):** HYPE +13% to >$76, ~+200% YTD; Bitwise Hyperliquid ETF $108M AUM; onchain-exchange / Coinbase-USDC speculation ([CoinDesk 06-16](https://www.coindesk.com/markets/2026/06/16/hyperliquid-uniswap-and-worldcoin-buck-crypto-slump-as-traders-chase-ai-defi-trends)).
- **Has price reacted?** Yes, extensively (+200% YTD, fresh ATH). **Strongly overextended.**
- **Chasing?** Buying the ATH here is a chase. Basket playbook is explicitly `wait_pullback`.
- **Mood-aligned?** Yes (risk-on), but extension + FOMC argue for patience.
- **Long/short/wait?** **Catalyst-watch / wait-for-pullback.** No clean entry at ATH.
- **Invalidation/trigger:** actionable only on a controlled pullback that holds; avoid initiating into the Fed.

### Candidate 3 — SENT/USDT — LONG B-tier — AVOID / CHASE-RISK
- **Source:** B-tier scalp (71.2) / intraday / swing; strongest 24h (+28%), but **no fresh verified catalyst** (desk: "no fresh verified catalyst detected"; internal news 24h = 4, no primary driver).
- **Has price reacted?** Yes — +28% 24h is the reaction; entry now is late.
- **Chasing?** Yes. This is exactly the no-catalyst momentum pump flagged as the day's trap last night.
- **Long/short/wait?** **Avoid initiating;** watch only if it builds a real base + a catalyst appears.
- **Chase-risk:** HIGH. Mean-reverts before TP per the desk's own scalp horizon-mismatch flag.

### Candidate 4 — JPM (stocks) — A-tier LONG (82.6) — PLANNING / CARRY-FORWARD ONLY
- **Source:** active-signals stocks A-tier intraday long, score 80–82.6, triggered — but the **fresh stocks intraday report prints "No A/B-tier setups in this run,"** i.e. this A-tier is a carry-forward, and the **US market is closed overnight.**
- **Legal/headline check:** JPM — **no indictment / SEC-DOJ probe / restatement / delisting found.** Clean on the legal screen (the legal name in the complex is UNH, not JPM).
- **Long/short/wait?** **Wait** — not actionable until the cash open, and then only with RTH confirmation. Re-evaluate at the 11:30 / 16:20 / 18:30 stocks slots.
- **A-tier stocks stats:** n=6, +2R, PF inf but **anecdotal** — do not over-trust the A label on tiny sample.

### Candidate 5 — UNH (stocks) — LEGAL/HEADLINE RISK — AVOID
- **Source:** active stocks C-tier intraday/swing longs (scores 63–68) + a top catalyst (importance 0.78).
- **LEGAL/HEADLINE RISK (verified):** DOJ Medicare-Advantage **criminal fraud probe**; shares **−16% to a 5-year low**; CEO resignation + guidance suspension in the broader episode; >$300B market-cap loss ([QuiverQuant](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe,+Shares+Dive+16%25+on+Fraud+Investigation), [Globe&Mail mirror](https://www.theglobeandmail.com/investing/markets/stocks/UNH/pressreleases/32431512/unitedhealth-unh-faces-doj-probe-shares-dive-16-on-fraud-investigation/)). _(Note: some search results carry a May-2025 origin date for the same probe; treat the headline as an active, unresolved overhang.)_
- **Verdict:** **AVOID.** UNH must never surface as a clean actionable long while this is live. C-tier longs on UNH are research-only and contradicted by the legal tape.

_SMCI note (no active signal):_ Form 8-K indictment re an alleged export-control conspiracy (importance 0.77, SEC EDGAR). Not in the active trade list; carry the prior legal flag as context — avoid if it reappears as a long.

## 8. Best Candidates Ranked

1. **WLD/USDT — LONG, pullback-only.** Best long + best catalyst-backed. Trigger: filled on a pullback into **0.658–0.667** that *accepts* (not just wicks); invalidation 1h close < ~0.646. Keep size light into FOMC.
2. **HYPE/USDT — catalyst-watch, wait-pullback.** Strongest narrative, but ATH/+200% YTD = no clean entry; trigger = a controlled pullback that holds.
3. **JPM (stocks) — A-tier, planning-only.** Trigger: US cash open + RTH confirmation; re-check at the 11:30/16:20 slots.

**Watch (no clean *now* trade this window — pre-FOMC coil):**
- **long-watch WLD/USDT** — trigger: pullback acceptance 0.658–0.667 + BTC holding > $64K.
- **short-watch NEAR/USDT** — trigger: failed bounce / rejection at resistance with BTC losing $64K (counter-trend, only if regime flips; otherwise skip — thin & against the tape).
- **catalyst-watch HYPE/USDT** — trigger: pullback that holds + continued ETF-inflow / perps-DEX flow confirmation.

## 9. Avoid / No Trade  (this decision window only — scanner keeps running)
- **Chasing no-catalyst pumps:** SENT (+28%), PORTAL (+37%), HMSTR — thin volume, no fresh news, mean-revert risk.
- **Naked size into FOMC:** the decision lands today; do not initiate large fresh exposure ahead of it.
- **UNH long:** active DOJ fraud probe — avoid regardless of C-tier score.
- **Thin/low-liquidity shorts:** BABY, SPCXB (futures data unavailable / no external data) — do not initiate.
- **HYPE at ATH:** wait for a pullback; chasing the high is a low-RR entry.
- _This is a current-window verdict only — never a command to pause the scanner, collection, tracking, or scheduler._

## 10. Main Risks
- **FOMC today (Warsh's first meeting):** hold ~97–98% priced, but a hawkish dot plot / tone could flip risk-off fast (BTC → $64K → $63.3K). Single biggest event risk.
- **Geopolitics tail:** US-Iran deal is interim; June 19 signing pending, Trump warned of possible renewed strikes → headline-driven oil/risk reversal possible ([CoinDesk 06-15](https://www.coindesk.com/tech/2026/06/15/live-markets-bitcoin-not-fully-out-of-danger-as-trump-warns-of-further-iran-strikes)).
- **Narrow leadership / crowding:** the only clean longs are AI/perps-DEX names that are already extended (WLD +180% mo, HYPE +200% YTD) — chase risk high, pullbacks thin.
- **Catalyst mapping weak (77.9% unmapped):** symbol-level catalyst attribution is unreliable this run — context only.
- **Weak base rates:** crypto scalp PF 0.17 (−5R), crypto shorts PF 0.75; stocks shorts PF 0.32 (−26R), stocks intraday PF 0.65 (−18R). Favor crypto **intraday/swing longs**, prefer **cross-exchange-confirmed** signals (PF 1.52 vs Binance-only 0.79).
- **Ingest:** §13 ingest succeeded (no risk this run).

## 11. Action Plan — next 4 hours (into Europe / pre-FOMC)
1. **Hold posture light into FOMC** — RS-leader pullback longs only; no naked size ahead of the decision.
2. **WLD/USDT:** set an alert for the 0.658–0.667 pullback zone; only engage on *acceptance*, invalidation 1h close < ~0.646. Take partials early (scalp horizon-mismatch flag).
3. **HYPE/USDT:** watchlist `wait_pullback`; do not chase the ATH.
4. **BTC pivot watch:** reclaim+hold > $67K = risk-on confirm (improves all long-watches); loss of $64K = risk-off flip (activates short-watch NEAR, demotes longs).
5. **Stocks:** JPM A-tier and all stock ideas are planning-only until the US open — revisit at the 11:30 EU / 16:20 pre-open slots with RTH confirmation discipline. Keep UNH on the AVOID list.
6. **Avoid** SENT/PORTAL/HMSTR chases and thin-liq shorts.

## 12. Final Verdict per Mode
- **Crypto scalp:** **selective, low-confidence.** Only WLD pullback; PF 0.17 base rate → take partials fast, no chasing. Default: wait.
- **Crypto intraday:** **best mode (PF 1.32).** WLD pullback long is the cleanest idea; prefer cross-exchange-confirmed entries; light size into FOMC.
- **Crypto swing:** **hold/selective.** WLD/AI-rotation longs valid on pullbacks; breadth thinner (59% EMA20); FOMC argues for patience.
- **Stocks intraday/swing/invest:** **closed → planning only.** JPM A-tier = wait-for-open + RTH confirm; UNH = AVOID (legal); stocks shorts structurally avoid (PF 0.32).

## 13. Sources
- [CoinDesk — Hyperliquid, Uniswap and Worldcoin buck crypto slump as traders chase AI, DeFi trends (2026-06-16)](https://www.coindesk.com/markets/2026/06/16/hyperliquid-uniswap-and-worldcoin-buck-crypto-slump-as-traders-chase-ai-defi-trends) — WebFetch HTTP 200; confirms WLD +12%/+180% mo, HYPE +13%/+200% YTD, UNI +18%, AI/DeFi catalyst. _single_source (primary outlet)._
- [CoinDesk — Bitcoin hits a two-week high above $65,500 as the US-Iran deal sends oil sliding (2026-06-15)](https://www.coindesk.com/markets/2026/06/15/bitcoin-hits-a-two-week-high-above-usd65-500-as-the-us-iran-deal-sends-oil-sliding) — BTC ~$65.8K risk-on. _single_source._
- [CoinDesk — Bitcoin not fully out of danger as Trump warns of further Iran strikes (2026-06-15)](https://www.coindesk.com/tech/2026/06/15/live-markets-bitcoin-not-fully-out-of-danger-as-trump-warns-of-further-iran-strikes) — interim deal, June 19 signing risk. _single_source._
- [QuiverQuant — UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe,+Shares+Dive+16%25+on+Fraud+Investigation) — UNH legal overhang. _single_source (date origin partly May-2025; treat as active unresolved)._
- Internal: scalp/intraday/swing + stocks reports (2026-06-17 00-15…00-49); `catalyst_cycle_00-23.md`; `active-signals`/`signal-stats`/`detect_untracked_legacy_alerts` CLI; `news_items` DB.

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-mapping remains weak — 388/498 unmapped (77.9%), persistently >50% across runs (77.7% last night → 77.9% now).
- **evidence:** `data/catalysts/2026-06-17/catalyst_events.jsonl` (110 mapped / 388 unmapped); top unmapped are clearly symbol-bearing or pure noise ("White House's Anthropic move…", World Cup visa story, Circle/USDC).
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (alias/ticker dictionary, fuzzy entity match, drop sports/politics noise pre-scoring).
- **priority:** medium
- **first observed:** carried across runs; re-confirmed 2026-06-17 04:45 EEST

### TODO-narrative-baskets-null-fields
- **issue:** `narrative_baskets.jsonl` rows parse with null `basket/theme/primary_symbol/symbols/freshness/heat/status` under the field names used by readers, even though `catalyst_cycle_00-23.md` renders 4 well-formed baskets — suggests a schema/field-name mismatch between the JSONL writer and downstream consumers.
- **evidence:** `data/catalysts/2026-06-17/narrative_baskets.jsonl` → 4 rows all-null on those keys; the cycle .md has full basket detail (ai/perps_dex/rwa/delisting).
- **suggested manual fix:** align JSONL field names with the markdown renderer's schema (or document the canonical key names) so programmatic consumers can read baskets without re-parsing the .md.
- **priority:** low
- **first observed:** 2026-06-17 04:45 EEST

### TODO-untracked-legacy-alert-window
- **issue:** Last night's review reported 23 cumulative untracked legacy crypto alerts within 2026-06-16; the `--since today` detector now reads clean (0), but the metric is window-sensitive and the prior climb (20→23 intraday) was never root-caused.
- **evidence:** `detect_untracked_legacy_alerts --since 2026-06-17` → None; prior review noted 23 cumulative on 2026-06-16.
- **suggested manual fix:** confirm whether the 2026-06-16 cumulative untracked alerts ever got backing `proposed_signal` rows, or were genuine registration gaps (PART 1 regression check).
- **priority:** low
- **first observed:** carried from 2026-06-16; re-noted 2026-06-17 04:45 EEST

### TODO-contradictory-btc-rss
- **issue:** Crypto scalp report §5 surfaces directly contradictory BTC macro headlines as current ("Iran drones → BTC below $73K panic" vs "ceasefire → BTC past $65K") with no recency dedup; the verified current state is BTC ~$65–66K risk-on. Stale/contradictory headlines presented side-by-side could mislead the LLM read.
- **evidence:** `data/reports/scalp/2026-06-17_00-15_scalp_report.md` §5 News and Catalysts.
- **suggested manual fix:** add recency/dedup or "superseded" tagging to conflicting macro headlines so the latest verified state dominates.
- **priority:** medium
- **first observed:** 2026-06-17 04:45 EEST
