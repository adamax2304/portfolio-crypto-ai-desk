# Opus Enriched Review — Europe / pre-US context (Sunday) — Auto Cycle 11:45 EEST

## 1. Executive Summary

**Sunday Europe-morning window: US equity markets are CLOSED (weekend), so stocks are planning/watchlist-only; crypto is the lone live actionable class.** External web research **AVAILABLE** this run (WebSearch ×4 + WebFetch verified on CoinMarketCap; two news-site WebFetches returned HTTP 403 but their claims are corroborated by multiple search-result sources — see §13).

The crypto tape has improved modestly versus Friday's risk-off chop: the desk reads **BTC transition_up / ETH range**, altcoin breadth **75% > EMA20** (up from ~57% Friday), BTC ATR percentile a very low **6** (compressed volatility). Externally, BTC was last seen **~$63.5K** and ETH **~$1,671** (Jun 12, rebounding on Iran-war de-escalation). This is a **cautious risk-on / transition** tape, not a clean trend — route, don't chase.

**No A-tier crypto signals and no A-tier in any live class.** The single non-expired A-tier in the system is **LLY (stocks invest, 82.13, triggered)** — but it is a closed-market, planning-only monthly idea, and carries a fresh demand **headwind** (employers reportedly dropping weight-loss-drug coverage, Jun 12). The most decision-relevant flag this run is **UNH (stocks invest B long): confirmed DOJ criminal + civil Medicare-fraud probe → AVOID** the long.

Live crypto reads as **wait-for-pullback longs in the AI / momentum-breakout leaders** (TAO, MEGA, FET) — best **catalyst-backed long-watch is TAO** (Bittensor subnet AI-demand narrative). **MEGA is the strongest RS leader (+24% 24h) but is chase-risk** with a **June 23 token unlock (250M, ~2.5% supply) overhang** and a tiny $72M cap with heavy future dilution. No clean short this window (breadth is up; weakest names already dumped). **Weekend signal bucket is statistically poor (WR 5%, PF 0.25, n=22)** — size down, demand clean pullback-holds.

Advisory only; scanner/data-collection continue regardless of verdict.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-14_07-04_scalp_report.md` — mtime 10:04 EEST → **fresh** (~1.7h).
- **Crypto intraday report** `data/reports/intraday/2026-06-14_07-12_intraday_report.md` — mtime 10:12 EEST → **fresh** (~1.5h).
- **Crypto swing report** `data/reports/swing/2026-06-14_01-32_swing_report.md` — mtime 04:32 EEST → **carry-forward** (~7h).
- **Stocks intraday/swing/invest** — all dated 2026-06-12 (Fri) → **stale** (markets closed Sunday; planning context only).
- **Catalysts** `data/catalysts/2026-06-14/` — events.jsonl + narrative_baskets.jsonl + cycle md (07:12) — fresh.
- **LLM packet** `data/processed/llm_analysis_packet.md` (10:12, fresh); stocks packet 06-12 (stale).
- **CLI:** active-signals crypto (13) + stocks; signal-stats crypto + stocks; detect_untracked_legacy_alerts (since today).
- **DB (read-only):** proposed_signals, news_items, catalyst_events.
- **External:** WebSearch (BTC/ETH macro, UNH DOJ, MEGA/MegaETH, LLY legal) + WebFetch (CoinMarketCap MEGA verified).

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-14_default_schedule/`.
- `scheduler.log` mtime **10:13:14 EEST** (~1.5h old).
- Latest cycle summary `cycle_03_09-55_summary.md` mtime **10:13:12 EEST** (~1.5h old).
- **Both well under the 3h defer threshold → review proceeds (no defer).**
- Crypto reports fresh; crypto swing carry-forward (~7h); all stock reports stale (Friday, expected — weekend).

## 4. What Changed vs Previous Review

Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-12_2324.md` (Fri post-close, ~36h ago; no Saturday slot in history).

- **Regime:** Fri = risk-off chop, BTC/ETH range, breadth ~57% > EMA20. Now = **BTC transition_up**, breadth **75% > EMA20** → modest risk-on improvement over the weekend.
- **Crypto leaders rotated:** Fri leaders ORCA (+33%), STG, ENJ, XPL → now **MEGA (+24%), TAO (+16%), OPG (+12%), FET (+10%), RIF, BABY**. ORCA/ENJ no longer surfaced.
- **New / active:** crypto swing **FET, PHA triggered**; **TAO swing waiting** (news-supported); **MEGA intraday/scalp waiting**. Multiple swings at tp1/tp2 (NOT, ATOM, CHIP, ALLO, BANK, BABY, CRV).
- **Stocks:** Fri's AMD (worked, +~4%) and JPM (wait-trigger) intraday ideas are now **expired/stale**; live non-expired stock A/B are all **invest-mode** (LLY A; AMD/META/NVDA/UNH/SMH/PLTR B).
- **New catalyst flags:** **UNH DOJ Medicare-fraud probe** and **SMCI export-control indictment 8-K** surfaced in the legal_risk stream (SMCI has no live A/B now).
- **Thesis change:** crypto bias shifts from "risk-off, manage existing" → **"cautious risk-on, wait-for-pullback in AI/momentum leaders."** Stocks unchanged (closed → planning).

## 5. Catalyst Coverage

- **catalyst_events.jsonl rows today: 1,268** (report 5b dedup count: 441 unique); **baskets: 4**.
- **Mapped (non-null symbol): 202** · **Unmapped: 1,066 → 84% unmapped.**
- ⚠️ **CATALYST MAPPING WEAK THIS RUN — USE CATALYST LAYER AS CONTEXT, NOT FINAL DECISION.**
- Top 3 unmapped headlines (generic finance, no ticker): "Here's How Much a $2,400 401(k) Match Could Be Worth by Retirement"; "How Insurance Companies Turn Their Premiums Into Billions in Profit"; "Americans Are Looking at a 40% Social Security Tax Hike Unless This Happens".
- Active baskets: **ai_narrative** (related_beta_rotation; primary NEAR, RENDER, TAO, FET; fresh <24h) · **momentum_breakout** (wait_pullback; primary RIF, TAO, MEGA; fresh <1h) · **perps_dex_narrative** (wait_pullback; HYPE) · **delisting_thin_liquidity** (avoid_low_liquidity; no primary).
- Recurring high-unmapped rate (also >50% in prior runs) → see §14 TODO.

## 6. Market Landscape

- **Crypto (fresh, desk 07:00 UTC snapshot):** BTC **transition_up**, ETH **range**; breadth **75% > EMA20 / 55% > EMA50**; BTC ATR pct **6** (very compressed). Strongest: MEGA (score 92, +24%), TAO (91.6, +16%), OPG, FET, WLD, BABY, RIF. Weakest: STG (−51.7%), HMSTR (−15.4%), NIGHT, TRUMP. Narrative heat: **AI momentum 82.5/100** (mixed status), Memes mixed, RWA/Gaming/L2 quiet. Derivatives: leaders mostly price-up + OI-up (fresh positioning, crowding normal); funding broadly neutral; MEGA external funding neutral across bybit/okx/mexc.
- **External macro:** BTC ~$63.5K / ETH ~$1,671 (Jun 12, Yahoo), rebound on Trump's Iran-war-ended claim; June had been a descent month → tape is **recovery/transition, not confirmed uptrend**. Desk macro/geopolitics risk 25/100, BTC bias neutral/data-watch.
- **Stocks: CLOSED (Sunday).** Live non-expired A/B are invest-mode planning ideas only (LLY A; AMD/META/NVDA/UNH/SMH/PLTR B). Friday context: semis/healthcare/financials led. Re-evaluate at Monday's open with RTH confirmation.

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:** cautious **risk-on / transition** (BTC transition_up, breadth 75%, vol compressed) — not a clean trend.
- **Stocks mood:** **closed** (weekend) — planning only.
- **Dominant narrative:** **AI** (Bittensor/TAO, FET, RENDER, NEAR) + small-cap **momentum_breakout** (MEGA, RIF).
- **Preferred side now:** **longs on pullback** in AI/RS leaders; **catalyst-backed** preferred; **wait-for-trigger** otherwise.
- **Best long candidate:** **TAO/USDT** — catalyst-backed (Bittensor subnet AI demand), waiting pullback into 259.77–263.39.
- **Best short candidate:** **none clean** — breadth is up and weakest names (STG −52%, HMSTR −15%) already dumped; trigger: short only on a *failed retest* if BTC loses transition_up and rolls back into range.
- **Best catalyst-backed candidate:** **TAO/USDT** (AI/Bittensor narrative, news-supported).
- **What to avoid:** UNH long (DOJ probe); MEGA chase pre-unlock; no-catalyst weekend momentum longs (weekend WR 5% / PF 0.25); thin/MEXC-discovery + delisting_thin_liquidity names.
- **What would change the view:** BTC reclaiming/holding above the transition_up structure with breadth >EMA50 rising = add long conviction; BTC failing back into range = shift to failed-retest shorts; Monday RTH for any stock idea.

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — UNH (stocks, invest, LONG B 70.53, triggered) — AVOID / LEGAL RISK
- **LEGAL/HEADLINE RISK (verified):** UnitedHealth is under a **DOJ civil + criminal investigation** into Medicare Advantage billing (alleged diagnosis inflation for overpayments); probe extends to Optum Rx / physician reimbursement; DOJ interviewing former employees; UNH confirmed it is complying with formal requests. Sources: CNN Business (2025-07-24), Medical Economics, Healthcare Finance News, Fierce Healthcare (§13). Internal catalyst stream also flags it (importance 0.726, "Shares Dive 16% on Fraud Investigation").
- Mood-aligned? N/A — market closed; long thesis directly contradicted by active legal overhang.
- Long/short/wait: **was a long — now AVOID.** Has price reacted? Yes (prior −16% gap). Chase-risk? Headline-tail risk dominates.
- **Final verdict: AVOID (long). Manual review required before any UNH long is treated as actionable.**

### Candidate 2 — LLY (stocks, invest, LONG A 82.13, triggered) — PLANNING ONLY, HEADWIND NOTED
- A-tier monthly invest long, entry 1123.28–1162.98, SL 1043.88, tp1 1282.08; created 06-05, valid to 07-05.
- **Legal/headline check (mandatory for stock A):** No fresh disqualifying indictment **against LLY**. Old items: SCOTUS declined LLY's whistleblower-law challenge (May 2026) → $183M Medicaid judgment stands (aged, priced); LLY is *plaintiff* in a $200M COGIC rebate-fraud suit (not a risk). **Fresh headwind:** Jun 12 reports that employers plan to drop weight-loss-drug coverage → demand-side overhang on GLP-1 franchise.
- Mood-aligned? Market closed — planning only. Has price reacted? Dipped Jun 12 on the coverage news. Chase-risk? Re-confirm at Monday RTH.
- **Final verdict: planning-only (closed). Thesis intact but flag the weight-loss-coverage demand headwind; require Monday RTH confirmation; no weekend action.**

### Candidate 3 — TAO/USDT (crypto, swing, LONG B 65.4, waiting_for_entry) — BEST LONG-WATCH / CATALYST-BACKED
- Entry 259.77–263.39, SL 255.34, tp1 273.05; news-supported (news=1); ai_narrative + momentum_breakout basket primary; score 91.6, +16% 24h, RS vs BTC +15.5%, OI up (price-up+OI-up, crowding normal, funding ~neutral).
- **Catalyst (internal, reused — recent & consistent):** Bittensor subnet registration cost +6.5x to 1,500 TAO amid AI demand (CryptoBriefing, 06-13); AMBCrypto "ended correction after 16% break"; Benzinga price piece. Single_source but corroborated across three internal rows.
- Mood-aligned? **Yes** — AI is the dominant narrative; risk-on-transition favors RS-leader longs. Has price reacted? Partly (+16%). Setup chasing? No — signal is **waiting for a pullback into 259.77–263.39**, not a market buy. Overextended? +16%/24h is elevated but the plan demands a pullback. Actionable now? Only on pullback-hold into the zone with volume. Invalidation: loss of 255.34 / BTC rolling back into range.
- **Final verdict: LONG-WATCH (best catalyst-backed). Actionable only on pullback into 259.77–263.39 holding with volume; size down for weekend.**

### Candidate 4 — MEGA/USDT (crypto, intraday B 65.2 + scalp B 66.5, waiting) — CHASE-RISK / UNLOCK OVERHANG
- Intraday entry 0.06077–0.06250, SL 0.05866, tp1 0.06711 (valid to 06-15); scalp version **already expired 09:04**. Current ~0.0661 → price is **above** the intraday pullback zone (~0.0036 above, <1 ATR of 0.0040). Score 92, +24% 24h, +46% 7d, RS +23%; no internal catalyst (news=0).
- **External (verified, CoinMarketCap):** MEGA ~$0.0644, +24% 24h, **mcap ~$72.77M**, circulating **1.13B of 10B max** (~11% float). **Token unlock 2026-06-23 releases 250M (~2.5% supply)** — a dilution overhang ~9 days out. Launched Apr 30, already −25–30% off its $0.24 high; this is a speculative bounce, **no fresh fundamental catalyst.**
- Mood-aligned? Partially (RS-leader long fits risk-on) but **no catalyst + unlock overhang + tiny cap = high chase-risk.** Has price reacted? Yes (+24/+46%). Chasing? Buying here = chasing; plan requires pullback into 0.0608–0.0625. Overextended? Yes vs structure. Actionable? Only on a held pullback into the intraday zone, low size; do **not** market-buy extended.
- **Final verdict: LONG-WATCH (speculative) — pullback-only into 0.0608–0.0625 with volume; avoid chasing and avoid carrying size into the Jun 23 unlock.**

### Candidate 5 — FET/USDT (crypto, swing B 66.0, triggered) — AI BETA, MANAGE
- Entry 0.20687–0.20918, SL 0.20405, tp1 0.21532; triggered; ai_narrative basket primary; +10% 24h, RS +9.3%, price-up+OI-up (crowding normal), funding ~neutral; no fresh single-name catalyst (news=0) — rides the AI/Bittensor beta-rotation.
- Mood-aligned? Yes (AI narrative). Has price reacted? Yes (+10%). Chasing? Already triggered → manage rather than initiate. Actionable? Manage existing toward tp1 0.21532; trail SL 0.20405; new adds only on a clean pullback-hold.
- **Final verdict: HOLD/MANAGE (triggered) — manage to tp1, respect SL 0.20405; no fresh chase. AI-beta, not a standalone catalyst.**

## 8. Best Candidates Ranked

No clean *immediate* entry this window (crypto leaders extended/awaiting pullback; stocks closed). Per PART 9, routed watch list with triggers:

1. **TAO/USDT (long-watch, catalyst-backed)** — trigger: pullback-hold into **259.77–263.39** with volume; invalidate <255.34. *Best long + best catalyst-backed.*
2. **FET/USDT (manage, triggered long)** — manage to tp1 0.21532, SL 0.20405; add only on pullback-hold.
3. **MEGA/USDT (long-watch, speculative)** — trigger: held pullback into **0.0608–0.0625** + volume; avoid chase / avoid Jun-23-unlock exposure.
4. **LLY (stocks, planning)** — trigger: Monday RTH confirmation; mind weight-loss-coverage headwind.
- **Best long-watch:** **TAO** — trigger: pullback into 259.77–263.39 holding with volume.
- **Best short-watch:** **none clean** — trigger: BTC loses transition_up back into range, then short the *failed retest* of a weak high (no candidate qualifies now).
- **Best catalyst-watch:** **TAO** — trigger: continued Bittensor/AI demand confirmation + pullback entry.

## 9. Avoid / No Trade _(this decision window only — never "stop system")_

- **UNH long** — active DOJ criminal+civil Medicare-fraud probe (verified). AVOID until resolved/manual review.
- **MEGA gap/chase here (~0.066)** — extended +24/+46%, no catalyst, Jun-23 unlock (2.5% supply) overhang, $72M micro-cap; pullback-only, no chase.
- **No-catalyst weekend momentum longs** — weekend bucket WR **5%**, PF **0.25**, −3R (n=22); thin liquidity amplifies gap risk.
- **Initiating new shorts on already-dumped names** (STG −52%, HMSTR −15%) — too extended; wait for failed retest.
- **Thin/MEXC high-risk discovery + delisting_thin_liquidity basket names** — avoid_low_liquidity.
- **Any stock entry this window** — market closed; no fills, no confirmation until Monday RTH.
- _Scanner, candidate generation, tracking, and data collection continue as normal — this is a decision-window caution only._

## 10. Main Risks

- **Weekend gap / thin-liquidity risk** in crypto; weekend signal bucket is statistically negative.
- **Macro datapoint is 2 days old** (BTC/ETH from Jun 12) — Iran-de-escalation rebound could reverse; treat macro as context.
- **MEGA Jun-23 token unlock** and broader low-float dilution overhang on small-caps.
- **Catalyst mapping 84% unmapped** → catalyst layer is context-only this run (decisions lean on technical + verified external).
- **Compressed BTC ATR (pct 6)** → expansion risk in either direction; transition_up is not a confirmed trend.
- Two news-site WebFetches (The Hill, Healthcare Finance) returned **HTTP 403**; UNH legal claim is corroborated by multiple search-result sources but not independently page-verified this run.
- Ingest CLI for sources may fail (logged in §13 if so); does not block the review.

## 11. Action Plan — next 4 hours

1. **Crypto (live):** Wait for **TAO** pullback into 259.77–263.39 (vol confirm) as the preferred catalyst-backed long-watch. **Manage FET** toward tp1 0.21532 (SL 0.20405). Treat **MEGA** as pullback-only into 0.0608–0.0625, low size, no chase.
2. **No new no-catalyst weekend momentum longs**; size down everything for weekend gap risk.
3. **Re-check BTC structure** vs transition_up: holding+breadth rising = add long conviction; failing into range = pivot to failed-retest shorts (none qualify yet).
4. **Stocks:** no action — build Monday watchlist; **UNH = AVOID (legal)**, **LLY = planning with coverage headwind**, require RTH confirmation Monday.
5. Re-assess at the next slot (16:20 pre-US-open is the next decision-relevant one; until then crypto-only).

## 12. Final Verdict per Mode

- **Crypto scalp:** cautious risk-on chop — **wait-for-pullback**; MEGA scalp already expired; no fresh no-catalyst entries; low size for weekend.
- **Crypto intraday:** **TAO long-watch (pullback 259.77–263.39 + volume)**; MEGA pullback-only into 0.0608–0.0625, no chase; manage existing.
- **Crypto swing:** carry-forward (~7h) — **FET manage to tp1 / TAO long-watch on pullback**; ride AI beta-rotation with size discipline; respect SLs.
- **Stocks intraday:** **MARKET CLOSED — planning only.** Re-evaluate Monday RTH.
- **Stocks invest/swing:** stale (Fri) — planning only. **LLY (A) thesis intact, weight-loss-coverage headwind**; **UNH AVOID (DOJ probe)**; no weekend action.

## 13. Sources

- [Bitcoin and ethereum prices today, Friday, June 12, 2026 (rebound on war-ended claim) — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-june-12-2026-prices-rebound-this-morning-after-trump-claims-war-has-ended-115949042.html) — 2026-06-12 — confirms (single_source): BTC ~$63.5K, ETH ~$1,671.
- [UnitedHealth confirms federal investigation into its Medicare practices — CNN Business](https://www.cnn.com/2025/07/24/business/unitedhealth-investigation-doj) — 2025-07-24 — contradicts (primary_source): DOJ civil+criminal Medicare Advantage probe.
- [UnitedHealth Group under DOJ investigation over Medicare billing — Medical Economics](https://www.medicaleconomics.com/view/unitedhealth-group-under-doj-investigation-over-medicare-billing-practices) — date unavailable — contradicts (single_source).
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx — Fierce Healthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) — date unavailable — contradicts (single_source).
- [MegaETH (MEGA) live price & market cap — CoinMarketCap](https://coinmarketcap.com/currencies/megaeth/) — 2026-06-14 — confirms (primary_source, WebFetch-verified): ~$0.0644, +24% 24h, mcap ~$72.77M, 1.13B/10B circ.
- [MegaETH (MEGA) price prediction / tokenomics (Jun-23 unlock 250M) — CoinMarketCap CMC-AI](https://coinmarketcap.com/cmc-ai/megaeth/price-prediction/) — date unavailable — weakens (single_source): unlock overhang.
- [US Supreme Court turns away Eli Lilly's whistleblower-law challenge — Investing.com / Reuters](https://www.investing.com/news/stock-market-news/us-supreme-court-turns-away-eli-lillys-challenge-to-whistleblower-law-4696180) — 2026-05 — weakens (single_source): $183M judgment stands (aged).
- [Eli Lilly (LLY) latest news (weight-loss coverage-drop headwind) — Yahoo Finance](https://finance.yahoo.com/quote/LLY/news/) — 2026-06-12 — weakens (single_source).
- Internal `news_items`: Bittensor subnet registration cost +6.5x to 1,500 TAO amid AI demand (CryptoBriefing, 2026-06-13) + AMBCrypto/Benzinga TAO rows — confirms (single_source, internal), supports TAO/AI narrative.
- _Note: WebFetch on The Hill and Healthcare Finance News returned HTTP 403; UNH claim corroborated by the multiple sources above rather than independently page-verified this run._

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-low
- **issue:** Catalyst symbol mapping very low again — 202/1,268 mapped (84% unmapped); recurring >50% across runs.
- **evidence:** `data/catalysts/2026-06-14/catalyst_events.jsonl` (1,268 rows, 1,066 null-symbol; top unmapped are generic finance headlines like "How Insurance Companies Turn Their Premiums Into Billions").
- **suggested manual fix:** improve the catalyst-layer symbol resolver / pre-filter generic macro-finance RSS items before they enter the event stream; consider an allow-list of ticker-bearing sources or NER tightening.
- **priority:** medium
- **first observed:** 2026-06-14 11:45 EEST (pattern recurring from prior runs)

### TODO-weekend-bucket-negative
- **issue:** Weekend-mode signal bucket persistently negative (WR 5%, PF 0.25, total −3R, n=22) vs non-weekend (WR ~17–20%, PF 1.12).
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` → "By weekend_mode" + observation "weekend signals underperform (winrate 5%, n=22)".
- **suggested manual fix:** consider a weekend size/threshold overlay (raise activation bar or reduce size on weekend_mode_active) — advisory; do not auto-apply.
- **priority:** medium
- **first observed:** 2026-06-14 11:45 EEST

### TODO-mega-scalp-expiry-vs-display
- **issue:** MEGA scalp B (66.5) was still listed by `active-signals` though its validity window expired 09:04 (now 11:45); risk of treating expired scalps as live.
- **evidence:** proposed_signals: MEGA scalp created 07:04, expires_at 2026-06-14T09:04, status waiting_for_entry; appears in active-signals output.
- **suggested manual fix:** confirm active-signals filters out past-expiry waiting_for_entry rows (or marks them expired) so stale scalps don't surface as actionable.
- **priority:** low
- **first observed:** 2026-06-14 11:45 EEST

### TODO-tier-b-triggered-winrate
- **issue:** tier=B triggered winrate 17% (n=89) flagged low by stats observations; weak-setup bucket PF 0.42 / −4R (n=15).
- **evidence:** `signal-stats --asset-class crypto` observations + "By setup" table.
- **suggested manual fix:** human review of entry timing / weak-setup bucket scoring at next manual session (advisory; no auto-change).
- **priority:** low
- **first observed:** 2026-06-14 11:45 EEST
