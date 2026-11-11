# Opus Enriched Review — LATE-SESSION RISK REVIEW — Auto Cycle 21:39 EEST

## 1. Executive Summary

**Monday 21:39 EEST "late-session risk review" slot — ~5h into US RTH (opened 16:30 EEST / 09:30 ET), ~1h20m before the US cash close (23:00 EEST / 16:00 ET).** External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch verified on Decrypt BTC live page; Fierce Healthcare 403'd but the UNH probe is corroborated by Healthcare Finance / Newsweek / TipRanks / Becker's / Medical Economics).

**The two-day risk-on move is still intact but maturing — this is a manage-and-protect window, not a fresh-entry window.** Stocks: **risk_on, VIX 16.25, breadth 100% > EMA20/EMA50**, semis the leadership sector (SMH RS vs SPY +14.34%, 20d +16.47%). Crypto: **bullish trend / risk-on, alt breadth 81.8% > EMA20, BTC + ETH uptrend, BTC ATR percentile 25 (low vol)**. BTC pushed to **$66,794 (+4.79% 24h)** on the confirmed US–Iran Strait-of-Hormuz peace framework — **but it is now pressing the $66–67K resistance that the desk's own macro feed flagged for "price rejection," and the rally is headline-driven and fragile** (verified: **$4.8B of US BTC-ETF outflows since May, 25-delta skew −4/−5%, Myriad assigns 67% odds to a $55K flush**). So crypto is risk-on at the index level but **late and into resistance** — not a place to chase new longs ~1h before a US close.

**Routing this window:** risk-on **longs only**, but **prefer protect-active / wait-for-pullback over new entries** given (a) lateness in the US session and (b) BTC at resistance. The cleanest *technical* name remains **AMD (intraday long, active A-tier 88 / freshest-report B 77.36, RS leader +26.8% vs SPY, semis-rotation + Citi Buy upgrade Jun 12)** — but it is almost certainly trading at/above its 540.82–546.74 entry zone, so it is a **pullback-into-zone idea, NOT a chase**, and with ~80 min to the close a fresh intraday entry is late. **SMH (active A 82 / report B 72)** gives the same semis exposure but is flagged by the desk's own playbook as a **known structural-loser cohort** ("NVDA/SMCI/SMH longs structurally lose in this regime") → prefer AMD over SMH for semis.

**One hard AVOID: UNH** sits in active C-tier longs (intraday + swing) but carries a **confirmed DOJ criminal Medicare-Advantage fraud probe now extended to Optum Rx / physician reimbursement** (shares −16% to a 5-yr low; DOJ has **not** filed charges) → **AVOID / MANUAL REVIEW — never a clean long.** Secondary avoids: overextended crypto chasers **JTO (+44%)** and **XLM (+24%, vol 2.01×, tagged overextended)**; **SMCI** (export-control indictment, SEC EDGAR 8-K); **ZRO** (active B swing into a **$23M token unlock** headwind).

**Integrity regression:** untracked legacy crypto alerts climbed **5 (18:40) → 8 now** (TAO, EDEN, CHIP×3, ADA, XPL×2) — Telegram-sent B alerts with no `proposed_signal`, so they never feed PF/winrate. Logged as a §14 TODO. **Track record routing:** crypto A/B stays weak (B-tier triggered WR 15%); stock headline A/B WR 20.8% / PF 1.00 with **A-tier longs 0% WR (n=5)** and **stock shorts −18R** → **longs-only, B-grade-clean only, no fresh shorts** in either class; crypto scalp lane structurally broken (PF 0.14) → research-grade only. **Advisory only. Scanner / collection / tracking continue in all moods — nothing here says stop the system.**

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-15_17-28_scalp_report.md` — mtime 20:28 EEST → **fresh** (~1h11m).
- **Crypto intraday report** `data/reports/intraday/2026-06-15_17-41_intraday_report.md` — mtime 20:41 EEST → **fresh** (~58m).
- **Crypto swing report** `data/reports/swing/2026-06-15_14-49_swing_report.md` — mtime 17:49 EEST → **carry-forward** (~3h50m; <4h, flag in §3).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-15_18-38_stocks_intraday_report.md` — mtime 21:38 EEST → **fresh** (~1m; data freshness 18:38 UTC, **live RTH / late session**).
- **Stocks swing report** `data/reports/stocks/swing/2026-06-15_15-02_stocks_swing_report.md` — mtime 18:02 EEST → fresh but playbook **watchlist_only (paused)** → planning context only.
- **Stocks invest report** `data/reports/stocks/invest/2026-06-15_15-08_stocks_invest_report.md` — mtime 18:08 EEST → fresh but **watchlist_only (paused, 0W/24L)** → context only.
- **Catalysts** `data/catalysts/2026-06-15/` — `catalyst_events.jsonl` + `narrative_baskets.jsonl` + `catalyst_cycle_17-42.md` (mtime 20:42 EEST → fresh).
- **LLM packets** `data/processed/llm_analysis_packet.md` (20:42) + `llm_stocks_packet.md` (20:58) — both fresh.
- **Internal CLI:** `active-signals` (crypto **33 active B**; stocks **50** incl carry-forward A-tier AMD 88 / SMH 82 / JPM 80), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-06-15` → **8 untracked**.
- **DB note:** the live store is `db/crypto_ai_desk.sqlite` (per `config/settings.yaml`, **not** the empty `data/*.db` files). It is **healthy** — `news_items` total 13,916; **§F priority-6 `t.me` last-4h = 37 items** (sources: WalterBloomberg ×29, lookonchain ×8 — all macro/equity headlines, only BTC/ETH symbol-mapped → **no fresh single-symbol Telegram catalyst that changes any candidate**). §M ingest ran successfully against this store (see below).
- **External:** WebSearch ×2 (UNH DOJ probe; BTC US-Iran rally) + WebFetch verified (Decrypt BTC page opened, returned price/skew/ETF-flow detail).
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-15T1839Z.json` (7 cited sources) and ran `ingest_enriched_review_sources` for **stocks** and **crypto** → "input: 7 | valid: 7 | rejected: 0; wrote 7 row(s)" each (idempotent UPSERT on url).

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-15_default_schedule/`.
- `scheduler.log` mtime **21:00:56 EEST** (~39m old) → **fresh**.
- Latest cycle summary `cycle_04_20-10_summary.md` mtime **21:00:51 EEST** (~39m old) → **fresh**.
- **Both well under the 3h defer threshold → review proceeds.**
- Freshness labels: all crypto scalp/intraday <1.5h and stocks intraday ~1m → **fresh**. Crypto **swing carry-forward** (~3h50m; used, flagged). Stocks swing/invest fresh but **playbook-paused** → context only. No stale-data exclusions this run.

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-15_1840.md` (US-open reaction slot):

- **Session aged from ~2h10m → ~5h into RTH; ~1h20m to the close.** Decision posture shifts from "confirm the gap-up hold" → **"manage active exposure, don't initiate late."**
- **BTC pushed higher AND into resistance.** 18:40 had BTC reclaiming $65K; now **$66,794 (+4.79%)** — but verified it is pressing **$66–67K resistance** with **$4.8B ETF outflows since May** and a **negative options skew**. Risk-on but **less sustainable headroom** than the open.
- **JPM demoted in the freshest report.** 18:40: JPM B-71 RTH-confirmed long. Now the 18:38 intraday report ranks **JPM C-tier 62.24 (watchlist)** — the active-signals A-tier 80 is a stale carry-forward, not a fresh signal. AMD/SMH remain the only A/B-grade semis names.
- **AMD/SMH unchanged in character** — AMD still cleanest semis long (B 77.36, RS leader), SMH still the named structural-loser-cohort contradiction.
- **UNH AVOID re-confirmed** (DOJ criminal probe re-verified; explicitly extends to **Optum Rx / physician reimbursement** this run).
- **Integrity regression worsened again: 5 → 8 untracked alerts** (added CHIP, ADA, XPL — trend 2→5→8 across the day, wrong direction).
- **Catalyst mapping flat-weak:** 80.6% → **80.4% unmapped**. No improvement.
- **Crypto leadership broadened:** GPS (91.6), ZEC (90.5), BABY (89.3), NEAR (89.3), CHIP (88.8) now lead RS; **JTO still overextended (+44%)** and **XLM newly overextended (+24%, vol 2.01×)** → both chase-risk. **ZRO** added as a token-unlock avoid.

## 5. Catalyst Coverage

- `catalyst_events.jsonl` (cumulative today): **total 2,567, mapped 504, unmapped 2,063 → 80.4% unmapped.**
- This-cycle scan (`catalyst_cycle_17-42.md`): 500 rows, **4 narrative baskets**.
- **⚠ Catalyst mapping weak this run — use the catalyst layer as context, not final decision.** (unmapped > 50%, recurring all day; see §14 TODO.)
- **Top 3 unmapped (by importance — all macro/sector noise, not symbol-actionable):** (1) "One Indicted Over Crypto 'Wrench Attack' in France" (Decrypt, 0.71); (2) "Did Tether just freeze $72M in USDT … Monero money-laundering sting?" (CryptoSlate, 0.71); (3) "Lawmakers face tight deadline to resolve issues for Clarity Act before July 4" (CryptoBriefing, 0.70).
- **Narrative baskets:** **ai_narrative** (NEAR/RENDER/TAO/FET + WLD/ASTER — related_beta_rotation, single_source, fresh <6h), **perps_dex_narrative** (HYPE + DYDX/GMX/ASTER — wait_pullback, <1h), **binance_ecosystem_teaser** (BNB/ASTER — sell-the-news risk, <6h), **momentum_breakout** (JTO/XLM/WLD — pure momentum, no confirmed catalyst, wait_pullback, <1h).
- **Legal/regulatory flags surfaced by catalyst layer:** **UNH** (DOJ criminal probe), **SMCI** (export-control indictment, SEC EDGAR 8-K), **ZRO** (token unlock), **IMX** (Aztec Connect $2M exploit — old abandoned contract, low live impact).

## 6. Market Landscape

- **Crypto (intraday):** bullish trend, risk-on (confidence 100/100). BTC + ETH uptrend; alt breadth 81.8% > EMA20, 88.6% > EMA50; BTC ATR percentile 25 (low vol). Style: selective longs, prefer pullbacks on RS. BTC **$66.8K into $66–67K resistance** — fragile. ETF flows: 1D +1,000 BTC but **7D −6,155 BTC / −$410M**, ETH 7D −24,405 / −$44M → distribution under the rally.
- **Stocks (intraday, live RTH):** risk_on, bias long, VIX 16.25, breadth 100% > EMA20. QQQ/IWM/DIA uptrend, SPY range. Leadership: **semiconductors (SMH RS +14.34%)**, technology, healthcare-ex-UNH. Weak: energy (XLE −8.15% on oil drop), communications.
- **Derivatives/crowding (crypto):** funding broadly neutral / low crowding across venues (ZEC, BABY, NEAR, CHIP, GPS all "crowding low"); NEAR shows **OI down on price up = short-covering (weaker continuation quality)**. No crowded-long blowoff signal — but no fresh-positioning confirmation on the leaders either.

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:** risk-on but **late / into-resistance** (BTC pressing $67K, ETF distribution, skeptical options skew).
- **Stocks mood:** risk-on (live RTH, ~1h20m to close) — **manage, don't initiate late**.
- **Dominant narrative:** US–Iran peace framework → oil down, risk-on rotation into semis/tech (stocks) + BTC relief bid (crypto); AI/RS-leader rotation in alts.
- **Preferred side now:** **longs / wait-for-pullback** — protect active, no fresh chase into the close; **no fresh shorts** (risk-on + stock-short −18R history).
- **Best long candidate:** **AMD** (semis RS leader) — but **pullback-into-zone only**, late for a fresh intraday entry.
- **Best short candidate:** **none clean** — risk-on disfavors shorts; weakest names (STG −17%, HOME −13%) are thin/low-vol and squeeze-prone. Short-watch only after a failed retest.
- **Best catalyst-backed candidate:** **AMD** (Citi Buy upgrade + semis rotation) on stocks; **NEAR** (ai_narrative basket) on crypto as watch-only.
- **What to avoid:** UNH (legal), JTO/XLM (overextended chase), SMCI (indictment), ZRO (unlock), crypto scalp lane (broken PF).
- **What would change the view:** BTC **accepting above $67K on volume** (→ crypto longs get headroom) or **losing $65K** (→ flush risk, the 67% Myriad case); for stocks, the **first 30 min after tomorrow's open** re-confirming or fading today's risk-on.

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — AMD (stocks intraday long) · active A-tier 88 / freshest-report B 77.36
- **Setup:** RS leader, trend uptrend, regime risk_on. Entry zone **540.82–546.74**, invalidation **close beyond 528.996**, TP1 564.47 / TP2 576.30 / TP3 594.04. RR-to-TP1 only 1.0 (thin).
- **Evidence:** RS vs SPY 20d **+26.80%**, RS vs sector +12.46%, above prev-day high, earnings safe. Catalyst: Citi Buy upgrade (Jun 12) + semis rotation (carried from 18:40 web research).
- **Contradiction check:** active A-tier 88 vs freshest report **B 77.36** — the A-tier is a carry-forward; the desk's own playbook marks **A-tier longs as overpromoted (0% WR, n=5, sized 0.5×)** while the **B-tier RTH-momentum lane is the clean one (WR 55%, PF 2.03)**. Treat AMD as a **B-grade actionable, not an A-tier conviction trade.**
- **Price reaction / chase:** AMD was +4–7% on the day at the open review → almost certainly **at/above the 540.82–546.74 entry now**. Entering NOW = chasing extension. RR already thin (1.0).
- **Mood-aligned?** Yes (risk-on, semis-leadership long). **Long, pullback-into-zone.** **Actionable only on a pullback into 540.82–546.74; with ~80 min to the close a fresh intraday entry is late** → prefer next-session retest. Invalidation: close < 528.996. Chase-risk: **high** if entered at market now.

### Candidate 2 — SMH (stocks intraday long) · active A-tier 82 / freshest-report B 72.06
- **Setup:** Entry **643.96–647.84**, invalidation **close beyond 636.19**, TP1 659.49. RS vs SPY +14.34%, semis the strongest sector. ETF (no earnings risk).
- **Contradiction check (material):** the stock playbook's **known failure mode explicitly names "NVDA/SMCI/SMH longs structurally lose in this regime."** High score (82/72) directly conflicts with the cohort's recorded behaviour.
- **Decision:** same semis thesis as AMD but with a documented structural-loser tag → **MANUAL / caution; prefer AMD for semis exposure.** Long-only-if-taken, on pullback into 643.96–647.84, invalidation < 636.19. Not a fresh chase late in the session.

### Candidate 3 — UNH (stocks, active C-tier intraday + swing longs) · LEGAL/HEADLINE RISK
- **LEGAL/HEADLINE RISK (verified):** DOJ **criminal** Medicare-Advantage fraud probe (upcoding / inflated risk scores), **now extended to Optum Rx and physician reimbursement**; shares fell **−16% to a ~5-yr low** when revealed. DOJ has **not** alleged misconduct or filed charges; a **separate civil** fraud probe also runs. Sources: Healthcare Finance News, Newsweek, TipRanks, Becker's Payer, Medical Economics, Fierce Healthcare (2026-06-15 cluster).
- **Decision:** a long here is a long-vs-legal contradiction. **Final verdict: AVOID / MANUAL REVIEW — never a clean actionable long.** Headline-driven gap risk in both directions; not a desk trade.

### Candidate 4 — NEAR (crypto intraday/swing long) · best crypto long-watch
- **Setup:** RS leader, score 89.3, RS/BTC **+14.52%**, 24h +19.2%; **ai_narrative basket primary** (related_beta_rotation). Active as B-tier swing (~69).
- **Weakening factors:** narrative is **single_source**, no per-symbol verified catalyst; **volume quiet 0.38×**; derivatives show **OI down on price up = short-covering (weaker continuation quality)**; ai_narrative carries crowding risk; macro BTC at $67K resistance caps alt upside.
- **Decision:** **long-watch, not a chase.** Trigger: a **pullback that holds + volume expansion (>1×) + BTC accepting above $67K**. Invalidation: loss of the basket's RS leadership / BTC losing $65K. Chase-risk: moderate (already +19% 24h).

### Candidate 5 — System integrity: 8 untracked legacy crypto alerts
- **Anomaly:** `detect_untracked_legacy_alerts` returns **8** (TAO B/scalp 76.3, EDEN B/scalp 68.4, CHIP B ×3 [scalp 76.8/swing 71.6/scalp 71.0], XPL B ×2 [scalp 75.8/intraday 65.7], ADA B/scalp 65.9) — Telegram-sent B alerts with **no matching `proposed_signal`**, so they will **not** contribute to PF / winrate / avgR. Count trend today: **2 → 5 → 8** (worsening).
- **Decision:** not a trade — **integrity regression**, surfaced as §14 TODO. The affected symbols (CHIP, XPL, TAO) are otherwise legitimate RS names; the issue is tracking-pipeline, not signal quality.

## 8. Best Candidates Ranked

No clean *fresh-entry* candidate this window (late session + BTC at resistance). Per PART 9, the routed watch list:

1. **Best long-watch — AMD** (stocks): trigger = **pullback into 540.82–546.74** (do not chase ~80 min from close); cleaner as a **next-session retest**. Invalidation close < 528.996.
2. **Best long-watch (semis alt) — SMH**: same pullback logic (643.96–647.84) **but** structural-loser-cohort caution → AMD preferred.
3. **Best crypto long-watch — NEAR**: trigger = pullback-hold + volume >1× + **BTC accepts > $67K**. ai_narrative beta, watch crowding.
4. **Best short-watch — none clean**: risk-on; only after a **failed retest** on a liquid weak name (avoid thin STG/HOME). Re-check if BTC loses $65K.
5. **Best catalyst-watch — AMD** (Citi Buy + semis rotation) / **NEAR** (ai_narrative): both confirmation-gated as above.

## 9. Avoid / No Trade  *(this decision window only — scanner keeps running)*

- **UNH** — DOJ criminal + civil Medicare-fraud probe (Optum Rx extension); legal contradiction → AVOID.
- **JTO (+44%) / XLM (+24%, vol 2.01×, overextended)** — pure-momentum, >2 ATR extended, no confirmed catalyst → no chase; wait-pullback only.
- **SMCI** — export-control indictment (SEC EDGAR 8-K) → avoid.
- **ZRO** — active B swing into a **$23M token unlock** → unlock-headwind, avoid fresh longs.
- **SMH** — actionable only with structural-loser caution; AMD preferred for semis.
- **Fresh intraday entries generally** — ~1h20m to the US close; prefer manage-active / next-session.
- **No fresh shorts** (crypto risk-on; stock shorts −18R historically).
- **Crypto scalp lane** — PF 0.14 / −6R, structurally broken → research-grade only, not Telegram-actionable.

## 10. Main Risks

- **BTC at $66–67K resistance with distribution underneath** ($4.8B ETF outflows since May, 7D −6,155 BTC, negative options skew, Myriad 67% odds of a $55K flush) → relief rally may fade; a loss of $65K opens downside. Crypto longs have limited headroom.
- **Late-session chase risk** on AMD/SMH — both likely above entry; thin RR-to-TP1 (1.0).
- **A-tier overpromotion** (stock A-tier longs 0% WR n=5) — do not trust the active A-tier 88/82/80 labels at face value; the freshest report already demoted JPM to C.
- **Headline reversal risk** — the entire risk-on leg rests on the US–Iran framework (signing targeted later); Trump has claimed imminent deals "38 times" → reversal would hit oil/risk both ways.
- **Data/infra:** resolved — the live store is `db/crypto_ai_desk.sqlite` (config-defined), healthy (13,916 news_items; t.me last-4h = 37). The earlier "DB unreadable" note in prior runs was a wrong-path artifact (querying empty `data/*.db`), not a real regression. §M ingest succeeded (7 stocks + 7 crypto rows). Minor doc-pointer TODO in §14.

## 11. Action Plan — next 4 hours

1. **Do not initiate fresh intraday stock longs into the close** (~1h20m left). Let active AMD/SMH B-grade ideas work only if price **pulls back into zone**; otherwise carry to tomorrow's open.
2. **Watch BTC $67K** — acceptance above on volume re-opens alt longs (NEAR first); loss of **$65K** = step back, expect the $55K-test scenario.
3. **Hold UNH as AVOID** — no long regardless of score until the DOJ probe resolves.
4. **Let the scanner run overnight into Asia** — crypto is the live class after the US close; re-evaluate RS leaders (NEAR/GPS/ZEC/CHIP) on the 23:15 post-close + 04:30 Asia slots for clean pullback entries.
5. **No fresh shorts**; only a failed-retest on a liquid weak name would qualify, and only if BTC rolls over.

## 12. Final Verdict per Mode

- **Crypto scalp:** NO fresh trade — lane structurally broken (PF 0.14); research-grade only.
- **Crypto intraday:** Risk-on but late/into-resistance — **long-watch NEAR on pullback + BTC>$67K**, no chase; JTO/XLM overextended = avoid.
- **Crypto swing:** Carry-forward report; RS leaders (NEAR/GPS/ZEC/CHIP) valid as **pullback long-watch**; avoid ZRO (unlock).
- **Stocks intraday:** Risk-on, **AMD B-grade long on pullback only** (late-session caution); SMH same with structural caution; **UNH AVOID**; JPM demoted to watchlist; **no shorts**.
- **Stocks swing / invest:** **Watchlist-only (paused)** — informational, never Telegram-actionable.

## 13. Sources

- [UnitedHealth under DOJ criminal Medicare-Advantage fraud investigation — Healthcare Finance News](https://www.healthcarefinancenews.com/news/unitedhealth-group-reportedly-under-investigation-criminal-medicare-advantage-fraud) (2026-06-15)
- [DOJ criminal probe extends to Optum Rx / physician reimbursement — Fierce Healthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) (2026-06-15; page returned HTTP 403 on fetch, headline/title verified via search index)
- [UnitedHealth responds to fraud-probe report — Newsweek](https://www.newsweek.com/unitedhealth-group-medicare-fraud-investigation-doj-wsj-2072533) (2026-06-15)
- [UNH stock sinks as DOJ criminal probe deepens — TipRanks](https://www.tipranks.com/news/unitedhealth-stock-unh-sinks-as-doj-criminal-probe-into-medicare-fraud-deepens) (2026-06-15)
- [Bitcoin Tops $65K on US-Iran Deal, But Traders Remain Skeptical — Decrypt](https://decrypt.co/371121/bitcoin-tops-65k-on-us-iran-deal-but-traders-remain-skeptical) (2026-06-15; WebFetch verified: BTC $66,794 +4.79%, $4.8B ETF outflows since May, 25-delta skew −4/−5%, Myriad 67% odds $55K)
- [US-Iran peace deal sends Bitcoin past $65K — is the rally priced in? — Cryptonomist](https://en.cryptonomist.ch/2026/06/15/us-iran-peace-deal-markets/) (2026-06-15)
- [Bitcoin Rebounds: US–Iran Peace Deal Sparks Risk-On — Coinspeaker](https://www.coinspeaker.com/bitcoin-rebounds-66k-us-iran-peace-deal/) (2026-06-15)
- Internal: `catalyst_cycle_17-42.md`, `narrative_baskets.jsonl`, `llm_analysis_packet.md`, `llm_stocks_packet.md`, stocks intraday report `2026-06-15_18-38`, `active-signals`/`signal-stats`/`detect_untracked_legacy_alerts` CLI (2026-06-15, this run).

## 14. Fix Requests / TODO

### TODO-untracked-alerts-regression
- **issue:** Untracked legacy crypto alerts climbed 2 → 5 → 8 across the day; 8 Telegram-sent B alerts (TAO, EDEN, CHIP×3, ADA, XPL×2) have no matching `proposed_signal` and never feed PF/winrate/avgR.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-15` → "8 untracked legacy crypto alert(s)"; trend vs prior reviews (1840: 5; 1630: 2).
- **suggested manual fix:** investigate the PART-1 alert→proposed_signal linkage regression in the crypto Telegram/watchlist path; ensure every sent watchlist alert creates a trackable `proposed_signal` with a `signal_id`.
- **priority:** high
- **first observed:** 2026-06-15 (worsening through the day; flagged here 21:39 EEST)

### TODO-review-skill-db-path-doc
- **issue:** This review skill (and the 18:40 run) wasted steps querying the empty `data/crypto_ai.db` / `data/crypto_ai_desk.db` files before discovering the live store is `db/crypto_ai_desk.sqlite` (per `config/settings.yaml` `db_path`). The "DB unreadable / news_items missing" note in prior runs was a wrong-path artifact, **not** a real regression — the store is healthy (13,916 news_items; t.me last-4h = 37; ingest works).
- **evidence:** `config/settings.yaml:14` → `db_path: db/crypto_ai_desk.sqlite`; raw query on that file returns counts and the §F t.me set; ingest wrote 7+7 rows.
- **suggested manual fix:** add the canonical `db/crypto_ai_desk.sqlite` path to the review SKILL.md §E/§F so future runs query the right store directly (and drop the stale "DB unreadable" fallback note carried since 18:40).
- **priority:** low
- **first observed:** 2026-06-15 21:39 EEST (corrects the 18:40 mis-diagnosis)

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol mapping ~80% unmapped all day (80.6% → 80.4%), so the catalyst layer is context-only, not decision-grade.
- **evidence:** `catalyst_events.jsonl` 2026-06-15 → total 2,567 / mapped 504 / unmapped 2,063 (80.4%); top unmapped are macro/sector headlines with empty `symbol`.
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (entity extraction for ticker/coin mentions; map sector/macro headlines to basket-level tags rather than null) to lift mapped-rate above 50%.
- **priority:** medium
- **first observed:** 2026-06-15 (persistent all day)

### TODO-stock-a-tier-overpromotion
- **issue:** Active A-tier stock longs (AMD 88 / SMH 82 / JPM 80) carry A-tier labels while the headline metric shows A-tier longs 0% WR (n=5) and the playbook flags NVDA/SMCI/SMH longs as structural losers; A-tier labels mislead vs the cleaner B-tier RTH-momentum lane.
- **evidence:** stocks `signal-stats` "tier=A n=5 Winrate 0.0%"; intraday report "Known failure mode: A-tier overpromotion on losing names"; sizing weight A-tier long 0.5×.
- **suggested manual fix:** review the A-tier promotion criteria for stocks intraday longs (cap or down-weight named structural-loser cohorts before they reach A), per the existing manual-approval lane — do NOT auto-change scoring.
- **priority:** low
- **first observed:** 2026-06-15 18:40 EEST (re-confirmed 21:39 EEST)
