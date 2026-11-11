# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:30 EEST

## 1. Executive Summary

**Monday 16:30 EEST "pre-US-open decision review" slot — US cash session opens right now (09:30 ET).** External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch verified on CoinGabbar BTC update; TheStreet 403'd, Yahoo/Fierce/CBS used as corroboration).

**The decisive change vs the prior (Sunday) review is a full macro reversal: RISK-OFF → RISK-ON.** Yesterday's active Israel–Iran fire has been overtaken by a **US–Iran framework/ceasefire deal to reopen the Strait of Hormuz** (MOU announced Jun 14, signing targeted Jun 19). Pre-open US futures are **gapping up hard — Nasdaq-100 +2.2%, S&P 500 +1.3%, Dow +1%** — oil is sinking, and **BTC is +2.08% at ~$65,695 with Bitcoin ETFs turning to +$85.8M net inflow** after a multi-week outflow streak (CoinGabbar/Yahoo, verified). Crypto breadth is **100% > EMA20**, BTC uptrend, ETH transition_up.

So the read into the open is **risk-on, but gap-up chase risk is the #1 trap**: futures up 1–2.2% means stocks likely gap at the open — **do NOT chase the gap; wait the first 15–30 min for RTH confirmation** before acting on any stock A/B. **No A-tier in any class.** Cleanest actionable-after-open stock ideas are **JPM long (B 69.95, financials RS+4.85%)** and **AMD long (B 66.49, semis SMH RS+8.05% — strongest sector)**, both demoted to C in the closed-market report and requiring RTH confirmation. Live crypto best idea is **ETH/USDT intraday B (68.6) RS-leader long on a pullback** into 1721.68–1727.88 (invalidation 1h close <1714.10), not a chase. **UNH (C long 63.28) is an AVOID** — it carries a confirmed **DOJ criminal + civil Medicare-fraud probe** (WSJ/Fierce/CBS; shares previously -16%), a direct long-vs-legal contradiction. Crypto A/B track record stays weak (WR 13.7% / PF 0.90 / −4R) → low conviction, size down. Stocks B-tier is the only net-positive bucket (PF 1.12 / +2R) → supports JPM/AMD once confirmed. Advisory only; scanner/data-collection continue in all moods.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-15_11-37_scalp_report.md` — mtime 14:37 EEST → **fresh** (~1h53m; data freshness 10:45 UTC).
- **Crypto intraday report** `data/reports/intraday/2026-06-15_11-38_intraday_report.md` — mtime 14:38 EEST → **fresh** (~1h52m). Source of the ETH B-tier long.
- **Crypto swing report** `data/reports/swing/2026-06-15_02-24_swing_report.md` — ~14h → **stale** (>14h; excluded from final-verdict swing — active swing read live from DB).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-15_11-41_stocks_intraday_report.md` — mtime 14:41 EEST → **fresh** (~1h49m; freshness 11:41 UTC, **pre-market / after-hours snapshot — A/B demoted to C, not yet RTH-confirmed**).
- **Stocks swing/invest** — 02:27 / 02:29 EEST, ~14h → **stale**; planning/watchlist context only.
- **Catalysts** `data/catalysts/2026-06-15/` — events.jsonl + narrative_baskets.jsonl + latest cycle md `catalyst_cycle_11-38.md` (mtime 14:38 EEST → fresh).
- **LLM packets** `data/processed/llm_analysis_packet.md` (14:38) + `llm_stocks_packet.md` (14:41), both fresh.
- **DB (read-only)** `db/crypto_ai_desk.sqlite`: news_items (TSLA/SpaceX + NVDA fresh rows; **no fresh UNH/JPM/AMD/SMCI rows** — stock legal flags sourced from catalyst layer), proposed_signals, watchlist_alerts, signal_outcomes.
- **Internal CLI:** `active-signals` (crypto: 20+ active B; stocks: JPM/AMD/UNH/SMH/LLY C waiting), `signal-stats` ×2, `detect_untracked_legacy_alerts` → **2 untracked (TAO, EDEN)**.
- **External:** WebSearch ×2 (UNH DOJ probe; US futures + BTC + Strait of Hormuz) + WebFetch (CoinGabbar BTC 06-15 — verified BTC $65,695 +2.08%, ETF +$85.8M, US–Iran de-escalation).

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-15_default_schedule/`.
- `scheduler.log` mtime **14:42 EEST** (~1h48m) → **fresh**.
- Latest cycle summary `cycle_02_14-06_summary.md` mtime **14:42 EEST** (~1h42m) → **fresh** (16/16 steps OK, 0 failed).
- Defer rule needs **BOTH** older than 3h → **not deferred**.
- Crypto scalp/intraday + stocks intraday **fresh (~2h)**; swing/invest **stale (~14h)**; catalyst layer **fresh**.
- ⚠️ Exchange discover endpoints (binance/bybit/mexc exchangeInfo) failed in the cycle → crypto OHLCV ran on cached universe (2 symbols only: BTC/ETH). Derivatives via MEXC fallback. Not blocking, but crypto candidate breadth is thin this run (§14 `exchange-discover-fail`).

## 4. What Changed vs Previous Review

Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-14_2139.md` (Sunday late-session risk slot, US equities closed).

- **MACRO FLIPPED RISK-OFF → RISK-ON (the headline change):** Sunday's "active Israel→Beirut strike + Iran missile retaliation" risk-off has been **overtaken by a US–Iran framework/ceasefire deal to reopen the Strait of Hormuz** (MOU announced Jun 14, signing Jun 19). Oil down, US futures gapping up (Nasdaq +2.2%, S&P +1.3%), BTC +2%. Complete reversal of the prior tilt.
- **Stocks REOPENED (weekday):** prior review had all stocks paused/weekend watchlist. Now **JPM (B 69.95) and AMD (B 66.49)** are actionable-after-open ideas (pending RTH confirmation), in the two strongest sectors (financials, semis).
- **Crypto regime improved:** BTC transition_up→**uptrend**; ETH downtrend→**transition_up**; breadth **67.5% → 100% > EMA20**. BTC ~$64K wall → **~$65.7K**, ETF flows turned **positive (+$85.8M)**.
- **UNH legal flag persists** (DOJ Medicare-fraud probe) — carried from prior, now corroborated externally; still AVOID.
- **Untracked alerts rose 1 → 2** (was MEGA; now **TAO, EDEN**) — recurring, §14.
- **Catalyst mapping still weak** (~19% mapped vs ~14% prior) — recurring, §14.
- **Thesis:** materially more constructive than Sunday, but **discipline = don't chase the gap**; crypto conviction still capped by a weak A/B track record.

## 5. Catalyst Coverage

- **Catalyst events today: ~455 unique** (report) / **1,683 raw rows**; **mapped (non-null symbol): 315 (~19%)**; **unmapped: 1,368 (~81%)**; **narrative_baskets: 3** (report cites 4 active).
- ⚠️ **CATALYST MAPPING WEAK THIS RUN — USE CATALYST LAYER AS CONTEXT, NOT FINAL DECISION.**
- **Top-3 unmapped headlines (representative noise/macro):** (1) "VP Vance thanks Americans for patience on Iran deal, calls it a new era" (macro, legitimately symbol-less); (2) `t.me/lookonchain` "Hey @Alhikli, welcome to Lookonchain" (join spam — §14 `lookonchain-spam`); (3) "Saving for Retirement in a 401(k)? 3 Costly Mistakes…" (off-topic noise).
- **Active baskets (fresh <6h):** `perps_dex_narrative` (wait_pullback; HYPE) · `binance_ecosystem_teaser` (related_beta_rotation; BNB) · `ai_narrative` (related_beta_rotation; NEAR/RENDER/TAO/FET) · `momentum_breakout` (wait_pullback; BANANAS31/GPS/EDEN).
- **Legal/headline events flagged by the catalyst layer:** UNH (DOJ probe ×4 sources), SMCI (SEC 8-K export-control indictment + securities lawsuit), IMX/Aztec Connect exploit ($2.1M).
- Recurring >50% unmapped across runs → §14 `catalyst-mapping-weak`.

## 6. Market Landscape

- **Crypto (fresh, desk 10:45 UTC snapshot + live macro):** BTC **uptrend ~$65,759**; ETH **transition_up ~$1,730**; breadth **100% > EMA20 / EMA50**; BTC ATR percentile **7 (very compressed → expansion risk, now upside-skewed on risk-on)**. Strongest: **ETH (score 64.6, +3.44% 24h, RS vs BTC +1.52%, vol 1.42×)** — the RS leader; BTC (57.5, +1.92%, vol 0.45× — below avg). Funding neutral across venues (bybit/okx/mexc), crowding low/normal. Narrative heatmaps quiet (AI/Memes 9.2/100). **External:** BTC +2.08% to $65,695, **ETF net inflow +$85.8M** (iBIT +$35M, FBTC +$42M) — first positive after multi-week outflows; driver = US–Iran de-escalation.
- **External macro (RISK-ON):** US–Iran framework deal to end fighting + reopen Strait of Hormuz; MOU Jun 14, signing Jun 19, 60-day formal end. Oil tumbling pre-market; US futures **Nasdaq +2.2% / S&P +1.3% / Dow +1%**. Broad risk-on into the cash open.
- **Stocks (pre-market gap-up; report regime = chop, VIX 16.65):** indices range/uptrend (IWM +4.01% 5d, QQQ +2.31% 5d). Strongest sectors **semiconductors (SMH RS+8.05%), healthcare (XLV +5.75%), financials (XLF +4.85%)**; weakest communications (XLC −3.80%). Pre-open A/B (demoted to C, closed-market): **JPM long 69.95, AMD long 66.49**; watchlist longs SMH/XLF/IWM/DIA; shorts PLTR/META/XOM/NFLX (C, low conviction). **UNH C long 63.28 → AVOID (DOJ legal).** Fresh single-name catalyst: **NVDA plans ≥$20B high-grade bond sale** (t.me/WalterBloomberg, 12:15 UTC) — NVDA is `no_trade` (22.67) in the scanner; bond raise is neutral-to-mildly-dilutive, **not** a long trigger. TSLA news = SpaceX +19% debut halo, no direct TSLA setup.

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:** **risk-on** — BTC uptrend +2%, ETF inflows positive, breadth 100%, macro de-escalation. *But* conviction capped by weak A/B history (PF 0.90) → route to **RS-leader longs on pullback**, not chase.
- **Stocks mood:** **pre-market / gap-up risk-on** — futures +1 to +2.2%; **not yet RTH-confirmed.** Treat as planning until the first 15–30 min print.
- **Dominant narrative:** **US–Iran ceasefire / Strait of Hormuz reopening** → broad risk-on, oil down, semis + financials + tech leading.
- **Preferred side now:** **longs (RS-leaders) on confirmation / pullback** — avoid chasing the gap; shorts not favored in a risk-on gap-up.
- **Best long candidate:** **AMD** (B 66.49, semis = strongest sector, risk-on tailwind) — actionable only after **RTH confirmation** (held VWAP/opening-range reclaim, first 15–30 min); do not buy the gap. Runner-up **JPM** (B 69.95, financials).
- **Best short candidate:** **none clean** into a risk-on gap-up. Best short-watch: **PLTR** (C 56.15) **only** on a failed RTH breakout / rejection of the gap — needs the rally to fail first; stand aside while futures are green.
- **Best catalyst-backed candidate:** **ETH/USDT** (RS leader +1.52% vs BTC, fresh attention, +ETF-flow macro) — long on a held pullback into 1721.68–1727.88, not extended.
- **What to avoid:** **chasing the open gap** (the run's #1 trap); **UNH long** (DOJ criminal+civil Medicare-fraud probe); **chasing NVDA** on the bond-sale headline; **SMCI** (export-control indictment + securities lawsuit); thin/MEXC names; BTC long on below-avg volume (0.45×).
- **What would change the view:** stocks **holding gains 15–30 min into RTH** (opening-range hold) = green-light JPM/AMD pullback longs; a **failed gap / reversal back through the open** = stand down longs, watch PLTR-type short on the failed retest; BTC **losing ~$64K / breadth rolling over** = de-risk crypto; any **headline that the US–Iran MOU stumbles** before the Jun 19 signing = risk-off snap-back.

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — AMD (stocks, B long 66.49) — best long, actionable AFTER open
- **Setup:** `stocks_intraday_rth_momentum`, long, B-tier, medium confidence, risk penalty −4.0. Demoted to C in the report (market closed at 11:41 UTC snapshot).
- **Why it ranks:** semiconductors (SMH) are the **single strongest sector** (RS vs SPY +8.05%, 20d +7.20%); risk-on gap-up tailwind aligns; stocks B-tier is the only net-positive bucket (PF 1.12 / +2R).
- **Price-reaction / chase check:** futures gapping +2.2% (Nasdaq) → **AMD likely gaps up; entry NOW (pre-open) would be chasing.** Wait the **first 15–30 min RTH**; long only on a held opening-range / VWAP reclaim. No earnings risk (safe list).
- **Mood-aligned?** Yes (risk-on long, leading sector). **Long, confirmation-required.** **Invalidation:** loss of the opening range / VWAP rejection. **Chase-risk:** high if bought at the bell. **Catalyst:** sector/macro tailwind, no single-name catalyst.

### Candidate 2 — JPM (stocks, B long 69.95) — runner-up long
- **Setup:** `stocks_intraday_rth_momentum`, long, B-tier (top stock score), penalty −4.0. Demoted to C (closed-market).
- **Why it ranks:** financials (XLF) strong (RS+4.85%); large-cap liquidity; benefits from risk-on + stable-rates backdrop.
- **Chase check:** gap-up risk (Dow fut +1%, less than Nasdaq). Same discipline — **RTH confirmation first**, prefer a held pullback over the gap. No near-term earnings.
- **Mood-aligned?** Yes. **Long, confirmation-required.** **Invalidation:** opening-range failure. **Catalyst:** sector/macro only.

### Candidate 3 — ETH/USDT (crypto, intraday B long 68.6) — best live crypto idea
- **Setup:** `crypto_intraday_catalyst_or_momentum`, long, B, status actionable. RS leader (+1.52% vs BTC, vol 1.42×, +3.44% 24h). Fresh attention via 3 catalyst rows.
- **Entry plan (from report):** pullback into **1721.68–1727.88**; **invalidation 1h close beyond 1714.10**; TP1 1744.43 / TP2 1758.21 / TP3 1772.00. Current ~1730.64, ATR 13.79.
- **Price-reaction / chase check:** already +3.4% on the day and at resistance 1733.04 → **buying here is chasing; demand the pullback.** Not >2 ATR extended yet. Macro (BTC +2%, ETF inflows) supports.
- **Mood-aligned?** Yes (risk-on RS-leader long). **Long, pullback-only.** **Chase-risk:** high at current print. **Catalyst:** fresh attention + positive macro; no contradiction. **Failure mode:** no-catalyst intraday in chop is net-negative (WR 23% / PF 0.70) — ETH's RS-leader + catalyst status is the better-supported variant.

### Candidate 4 — UNH (stocks, C long 63.28) — AVOID (legal contradiction)
- **LEGAL/HEADLINE RISK (verified):** **DOJ criminal + civil investigation into Medicare-Advantage fraud**, extending to **Optum Rx and physician reimbursement**; UNH has acknowledged and is complying. WSJ first reported May 2026; shares previously fell ~16%. Sources: Fierce Healthcare, Healthcare Finance News, CBS News, SEC 8-K (FY2026).
- **Contradiction:** scanner flags a **long** while an active criminal probe overhangs the name → **headline-gap risk both ways, asymmetric to the downside.**
- **Verdict:** **AVOID / MANUAL REVIEW REQUIRED** — never a clean actionable long while the probe is live. Not size-able on a momentum read.

### Candidate 5 — BTC/USDT (crypto, watchlist 60.9) — context, not actionable
- **Setup:** intraday watchlist, long, +1.92% 24h, **RS 0.0 (lagging ETH), volume 0.45× (below average)**. Pullback zone 65464.32–65668.59, invalidation <65214.65.
- **Read:** macro-driven (+2% on de-escalation, ETF inflows) but **weak internal confirmation** (below-avg volume, no RS edge). **Watchlist only** — ETH is the cleaner crypto long. Watch BTC as the regime tell: holding $64K→$65K keeps the risk-on long thesis alive.

_Excess candidates (not deep-dived): SMH/XLF/IWM (stock watchlist longs, same gap-up-confirmation discipline as JPM/AMD); SMCI (rejected short, legal flag noted); NVDA (no_trade, bond-sale catalyst is context not a trigger)._

## 8. Best Candidates Ranked

1. **AMD — long-watch (actionable after open).** Trigger: **held opening-range / VWAP reclaim in the first 15–30 min RTH**; strongest sector + risk-on. Do not buy the gap.
2. **JPM — long-watch (actionable after open).** Trigger: same RTH-confirmation; financials leadership.
3. **ETH/USDT — long-watch (live crypto).** Trigger: **held pullback into 1721.68–1727.88 with volume**; invalidation 1h close <1714.10. Skip if it runs >2 ATR first.
- **Best short-watch:** **PLTR** — trigger: **failed RTH breakout / rejection back through the open** (no short while futures green).
- **Best catalyst-watch:** **ETH/USDT** — trigger: pullback hold + BTC holding $65K + ETF-inflow narrative intact.

## 9. Avoid / No Trade (this decision window only)

- **Chasing the open gap** — futures +1 to +2.2%; entries at the bell are buying the spike. Wait for the 15–30 min RTH print. *(window discipline, not a system stop)*
- **UNH long** — active DOJ criminal+civil Medicare-fraud probe; AVOID/manual review.
- **SMCI** — SEC 8-K export-control indictment + securities lawsuit; avoid both directions on headline risk.
- **NVDA chase** — $20B bond-sale headline is neutral-to-dilutive, not a long trigger; scanner `no_trade`.
- **BTC long on weak volume** (0.45×) — prefer ETH (RS leader).
- **Thin/MEXC discovery names** — exchange-discover failed this run; breadth unreliable.
- _Scanning, candidate generation, tracking, and monitors continue in all moods — this is a window verdict, never a stop command._

## 10. Main Risks

- **Gap-up chase risk (primary):** futures up 1–2.2% → stocks likely gap; chasing is the run's biggest trap. Confirmation-first.
- **Deal-is-an-MOU risk:** US–Iran agreement is a framework (signing Jun 19); any headline that it stumbles snaps risk-on → risk-off fast.
- **Crypto A/B net-negative history** (WR 13.7% / PF 0.90 / −4R) → low conviction; size down, respect invalidations.
- **Catalyst mapping weak (~19% mapped)** → catalyst layer is context only this run.
- **Stock legal flags via catalyst layer only** — news_items has no fresh UNH/JPM/AMD/SMCI rows; cross-check headlines manually before any stock entry.
- **Thin crypto breadth** — exchange-discover failed; only BTC/ETH deeply analyzed; alt opportunities under-covered.
- **Low BTC ATR percentile (7)** — compressed; an expansion (now upside-skewed) can whipsaw stops.
- **Source ingest:** if the ingest CLI fails, citations stay in §13 only (logged here, non-blocking).

## 11. Action Plan — next 4 hours

1. **At the open: do NOT chase.** Let the first 15–30 min of RTH print. Watch whether the gap holds (opening-range hold) or fades.
2. **AMD / JPM:** long **only** on a held opening-range / VWAP reclaim with the strong-sector tailwind intact; skip if they gap and fade through the open.
3. **ETH/USDT:** long **only** on a held pullback into 1721.68–1727.88 (invalidation 1h close <1714.10); skip if extended >2 ATR. BTC is the regime tell — needs to hold $64K→$65K.
4. **Avoid:** UNH (legal), SMCI (legal), NVDA chase, BTC-on-weak-volume, thin alts.
5. **Manage, don't initiate:** existing triggered crypto B signals (TAO/etc.) — manage toward TP/invalidation.
6. **Re-check** at the 18:30 US-open-reaction slot: did the gap hold, which names confirmed, is breadth broad or narrow.

## 12. Final Verdict per Mode

- **Crypto scalp:** No clean A/B; watchlist ETH (62.2) / BTC (53.3). Low-confidence bucket → **wait for pullback, no chase.**
- **Crypto intraday:** **ETH/USDT long-watch** — RS leader + catalyst + risk-on macro; pullback-only into 1721.68–1727.88, invalidation <1714.10. Best live idea.
- **Stocks intraday:** **gap-up risk-on; require RTH confirmation.** AMD (semis) and JPM (financials) long-watch after the first 15–30 min; **avoid UNH (DOJ legal).** Don't chase the bell.

## 13. Sources

- [Fierce Healthcare — WSJ: Feds investigating UnitedHealth for criminal Medicare fraud](https://www.fiercehealthcare.com/payers/wsj-feds-investigating-unitedhealth-criminal-medicare-fraud) — date unavailable (probe first reported May 2026); confirms UNH DOJ criminal probe. *(primary_source / single_source)*
- [Fierce Healthcare — DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) — confirms scope extension. *(single_source)*
- [CBS News — UnitedHealth says it's under federal investigation for civil fraud](https://www.cbsnews.com/news/united-healthcare-federal-investigation-civil-fraud/) — UNH acknowledges federal probe. *(primary_source)*
- [SEC EDGAR — UnitedHealth Group 8-K (FY2026)](https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000121/uhgearningsreleaseq12026.htm) — company filing. *(primary_source)*
- [Yahoo Finance — Bitcoin & Ethereum prices today, Mon Jun 15 2026: rising after US–Iran ceasefire](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-june-15-2026-prices-rising-after-us-iran-agree-to-ceasefire-deal-114616600.html) — 2026-06-15; BTC ~$65.7K +2%. *(single_source)*
- [CoinGabbar — Bitcoin News Jun 15 2026: BTC surges to $65,695](https://www.coingabbar.com/en/crypto-currency-news/bitcoin-news-2026-06-15) — 2026-06-15; **WebFetch-verified**: BTC $65,695 +2.08%, ETF +$85.8M (iBIT +$35M, FBTC +$42M), US–Iran de-escalation driver. *(single_source)*
- [NBC News — US and Iran reach framework deal to end war and reopen the Strait of Hormuz](https://www.nbcnews.com/news/us-news/deal-reached-united-states-iran-war-rcna350039) — 2026-06; MOU Jun 14, signing ~Jun 19. *(primary_source)*
- [Yahoo Finance Markets — Dow/S&P/Nasdaq futures soar on US–Iran pact to reopen Hormuz](https://finance.yahoo.com/markets/stocks/live/stock-market-today-monday-june-15-224751171.html) — 2026-06-15; Nasdaq fut +2.2% / S&P +1.3% / Dow +1%. *(single_source)*

_Internal catalyst-layer / news_items rows (UNH, SMCI, NVDA bond sale, ETH whale) cited inline in §5–§6; not repeated here._

## 14. Fix Requests / TODO

### TODO-untracked-alerts
- **issue:** 2 untracked legacy crypto alerts (TAO/USDT B scalp 76.3; EDEN/USDT B scalp 68.4) sent to Telegram without a matching `proposed_signal` → no PF/winrate/avgR contribution. Up from 1 (MEGA) in the prior review.
- **evidence:** `scripts.detect_untracked_legacy_alerts --since 2026-06-15` — both sent 2026-06-15T08:52 UTC, trackable=NO.
- **suggested manual fix:** trace the scalp alert path that emits a watchlist_alert without registering a proposed_signal; ensure signal_id linkage at send time.
- **priority:** medium
- **first observed:** 2026-06-15 16:30 EEST (recurring pattern, ≥2 runs)

### TODO-catalyst-mapping-weak
- **issue:** catalyst symbol-mapping ~19% (315/1683 raw; ~81% unmapped) — recurring >50% unmapped across runs; weakens the catalyst layer to context-only.
- **evidence:** `data/catalysts/2026-06-15/catalyst_events.jsonl` — mapped 315, unmapped 1368; top unmapped = macro/spam (Vance Iran-deal, Lookonchain welcome, 401k).
- **suggested manual fix:** improve the symbol resolver (entity/ticker extraction) and filter join-spam (`t.me/lookonchain` "welcome to" rows) before importance ranking.
- **priority:** medium
- **first observed:** 2026-06-15 16:30 EEST (recurring)

### TODO-exchange-discover-fail
- **issue:** binance/bybit/mexc `exchangeInfo` / instruments-info discover calls failed in cycle 2 → crypto OHLCV ran on a cached 2-symbol universe (BTC/ETH only); derivatives via MEXC fallback. Thin crypto candidate breadth this run.
- **evidence:** `cycle_02_14-06_summary.md` steps 2–3 — repeated "discover failed" / "Could not initialise" warnings; reports show universe=0, ohlcv_fetched=0 on all venues.
- **suggested manual fix:** investigate connectivity/rate-limit/geo-block to exchange REST endpoints (WinError 10065 unreachable host); add cached-universe-fallback warning to report header so breadth thinness is explicit.
- **priority:** medium
- **first observed:** 2026-06-15 16:30 EEST

### TODO-lookonchain-spam
- **issue:** `t.me/lookonchain` "welcome to Lookonchain" join-confirmation rows ingested as catalyst events (noise in unmapped set).
- **evidence:** catalyst_events.jsonl unmapped sample "Hey @Alhikli, welcome to Lookonchain".
- **suggested manual fix:** add a source-side filter to drop welcome/join-confirmation messages from the collector.
- **priority:** low
- **first observed:** 2026-06-15 16:30 EEST (carried from prior reviews)
