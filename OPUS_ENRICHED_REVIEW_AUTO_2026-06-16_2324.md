# Opus Enriched Review — post-close final daily review — Auto Cycle 23:24 EEST

## 1. Executive Summary

**Tuesday 2026-06-16, ~23:24 EEST "post-close final daily review" slot — US cash session is now CLOSED (16:00 ET / 23:00 EEST).** External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch success on AnalyticsInsight; TheStreet and BlockchainReporter URLs returned HTTP 403 and were used as search-summary only).

**Daily wrap, the one fact that matters tonight: the day closed as a coil under an event, not a trend.** The US cash session was **mixed / rotational, not the clean "all-green bullish" the internal regime label implies** — **Dow +0.7–0.9% (~+370–469 pts, ~51,671), but Nasdaq −0.8 to −1.0%, S&P 500 −0.4%, Russell 2000 −0.6%**, i.e. **rotation OUT of tech into cyclicals/value** ([TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-16-2026)). The internal stocks desk still prints **"bullish, 100% breadth, semis/tech leading"** — that is a **20-day trend label and it masks today's actual intraday tech de-rating.** Treat the breadth=100% read as carry-forward context, not a description of how today closed.

**Crypto closed the day pinned: BTC ~$65.9–66.3K, range-bound $65–66K all session, still rejected under the $67K pivot; ETH was the day's clear outperformer** (~$1,760–1,843, cited +10.9% on the strongest source — leading BTC and +43% YTD) ([AnalyticsInsight](https://www.analyticsinsight.net/price-analysis/crypto-prices-today-bitcoin-fluctuating-between-65000-to-66000-as-fomc-opens-strategy-adds-1587-btc-hyperliquid-surges-10), [BlockchainReporter](https://blockchainreporter.net/bitcoin-price-today-btc-holds-66k-as-the-feds-big-day-arrives-and-warsh-takes-over/)). Institutional bid intact (**Strategy added 1,587 BTC, ~$100M, June 8–14 → 846,842 BTC**). The loudest tape name remained **HYPE (+10.4% session, +15.9% week, fresh ATH, perps-DEX narrative, 16 news mentions/24h)** — overextended.

**The dominant overhang is unchanged and now <24h away: the FOMC decision lands tomorrow, Wed June 17 — Kevin Warsh's first meeting as chair.** A **rate hold is ~97–98% priced** (3.50–3.75% range per CME FedWatch); the binary is the **dot plot + Warsh's tone**, not the rate itself ([AnalyticsInsight](https://www.analyticsinsight.net/price-analysis/crypto-prices-today-bitcoin-fluctuating-between-65000-to-66000-as-fomc-opens-strategy-adds-1587-btc-hyperliquid-surges-10)). Dovish → BTC tries **$67K → $68.5–70K**; hawkish → back to **$64K → $63.3K** support. **This makes tonight a "protect / wait-for-trigger, don't initiate" window** — no fresh naked size into the Fed, and overnight-into-Asia crypto most likely keeps coiling $65–67K.

**What worked / failed today:** the **ETH RS-leader long read worked** (best call of the day — fork catalyst + ETF flows + relative leadership); the **BTC range view also worked** (it never broke $67K or lost $64K — chop, correctly "no clean trade"); the **day's main trap was chasing the no-catalyst momentum pumps (SENT +37%, HMSTR, WLD)** — thin volume, zero news, mean-revert-before-TP per the desk's own scalp flag. Stocks intraday longs stayed structurally weak (A/B WR 16.7%, PF 0.88, totalR −2.0 on the week; C-tier PF 0.79, totalR −10). **No A-tier crypto anywhere; JPM hit A-tier 82.2 in the final stocks read but the market closed, so it is demoted to planning-only.** Advisory only; scanner / collection / tracking continue in all moods — nothing here says stop the system.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-16_19-01_scalp_report.md` — **FRESH** (mtime 22:01 EEST, ~1.4h; data 18:45 UTC).
- **Crypto intraday report** `data/reports/intraday/2026-06-16_19-14_intraday_report.md` — **FRESH** (mtime 22:14 EEST, ~1.2h; data 19:00 UTC).
- **Crypto swing report** `data/reports/swing/2026-06-16_13-32_swing_report.md` — **carry-forward** (mtime 16:32 EEST, ~6.9h; flagged).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-16_20-10_stocks_intraday_report.md` — **FRESH** (mtime 23:10 EEST, ~0.2h; data 20:10 UTC) — **the slot-relevant report; it self-labels "MARKET CLOSED — planning / watchlist only."**
- **Stocks swing** `…13-44…` (mtime 16:44, ~6.7h) + **invest** `…13-54…` (mtime 16:54, ~6.5h) → **carry-forward** planning context (flagged).
- **Catalysts** `data/catalysts/2026-06-16/` present: `catalyst_cycle_19-14.md` (latest), `catalyst_events.jsonl`, `narrative_baskets.jsonl` (4 baskets). No catalyst-scan needed.
- **LLM packets** `data/processed/llm_analysis_packet.md` (crypto) + `llm_stocks_packet.md` (stocks) present.
- **Internal CLI (from cycle_04 summary, 22:36):** `active-signals` crypto (**20 active, all long B**, scores 65–74) + stocks (mix of B/C; JPM B/A ideas, AMD B, XLF B); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-16` → **23 untracked** (rose from 20).
- **DB:** `db/crypto_ai_desk.sqlite` — `news_items`: **114 rows last 4h / 942 last 24h**; 24h mention counts HYPE ×16, ETH ×16, BTC ×73, SOL ×13, **UNH ×2** (was 0 last run — improved), JPM ×3; WLD ×1, SENT/JTO/HMSTR **×0** (pure momentum, no news).
- **External:** WebSearch ×2 (BTC/ETH + FOMC June 17; US stock close June 16). WebFetch: AnalyticsInsight crypto article → **HTTP 200, used**; TheStreet + BlockchainReporter → **HTTP 403, search-summary only**.
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-16T2024Z.json` (3 cited sources); ingest CLI result in §10/§13.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-16_default_schedule/`.
- `scheduler.log` mtime **22:36:28 EEST** (~0.8h old) → **FRESH**.
- Latest `cycle_*_summary.md`: `cycle_04_21-43_summary.md` mtime **22:36:27 EEST** (~0.8h); steps ok=16 failed=0.
- **Defer rule needs BOTH log AND latest cycle summary > 3h. Both ~0.8h → review proceeds.**
- Freshness labels: stocks intraday **FRESH** (~0.2h, slot-relevant, post-close); crypto scalp/intraday **FRESH** (~1.2–1.4h); crypto swing + stocks swing/invest **carry-forward** (~6.5–6.9h, inside use-but-flag band).

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-16_2139.md` (late-session risk review):

- **Window moved from late-session (~1h20 to close) → post-close daily wrap.** Posture shifts from "manage into the close + FOMC" → **"the day is done; grade it + set the overnight-into-Asia + pre-FOMC plan."**
- **The US close was mixed/rotational, NOT the clean bullish the desk's regime label implies:** Dow green, **Nasdaq −1% / S&P −0.4% / Russell −0.6%, tech rotated out** ([TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-16-2026)). New, decision-relevant nuance vs the "100% breadth" internal read.
- **ETH accelerated:** ~+4.1% at the late-session slot → cited **+10.9%** post-close — ETH is the standout daily winner and the crypto RS tell.
- **JPM A↔B oscillated to A again at the close (82.2) but is now planning-only** (market closed) — net no actionable change, retest next session post-FOMC.
- **Untracked legacy alerts 20 → 23** — continued intraday climb (§14).
- **Catalyst unmapped 77.1% → 77.7%** — unchanged-bad.
- **UNH:** now `news_items` ×2 in 24h (was 0) AND the fresh stocks report rejects it as **no_trade 36.03** — the legal-risk name is no longer surfacing as an active long. Improvement.
- **Confirmed:** FOMC June 17 overhang (hold ~97–98% priced, Warsh first meeting); BTC pinned under $67K; crypto risk-on regime; ETH RS leadership.

## 5. Catalyst Coverage

- `catalyst_events.jsonl` cumulative today: **3,731 rows**; mapped (non-empty symbol): **833**; unmapped: **2,898 → 77.7% unmapped**.
- Latest cycle (`cycle_19-14`) scanned 500 rows → 500 events, **4 narrative baskets**.
- **⚠ catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sample): "Lucky or insider info? Someone created a new wallet, spent $4.22M betting that Spain would…"; "Corning vs. QuantumScape: Which Technology Stock Is a Better Buy in 2026?"; "People in China are watching the World Cup differently this time."
- Active narrative baskets: **perps_dex_narrative** (primary HYPE/USDT; `wait_pullback`, fresh <1h), **ai_narrative** (NEAR/RENDER/TAO/FET; `related_beta_rotation`, <6h), **rwa_narrative** (ONDO/XLM; `related_beta_rotation`, <6h), **delisting_thin_liquidity** (`avoid_low_liquidity`, <1h).
- Top mapped catalysts by importance: TSLA SpaceX/DOJ legal_risk (0.90, a crypto-class mis-map artifact → TSLA/USDT), HYPE Bitwise ETF AUM (0.82), SOL Forward treasury (0.69), State Street GENIUS-Act stablecoin fund (0.68), BlackRock BTC yield ETF launch (0.66).
- **Integrity note (carried):** legal headlines still tagged to `/USDT` (UNH/USDT, TSLA/USDT, SMCI/USDT) — stock tickers being assigned crypto asset-class (§14).

## 6. Market Landscape

**Stocks (closed):** a rotational tape — value/cyclicals (Dow) up, tech/growth (Nasdaq, S&P, semis-heavy) down today, even as the 20d trend stays up. VIX ~16 (calm). Energy weakest sector (XLE RS −10%, consistent with oil falling on Iran relief). SpaceX +20% intraday on an AI deal was the single biggest stock story but did not lift the Nasdaq. **Net: the index "bullish" label is a trend artifact; today's session was a tech de-rate into the Fed.**

**Crypto:** BTC spent the whole day coiling **$65–66K under the $67K pivot**; ETH led (+10.9%, ~$1,760–1,843), the clearest RS signal; alt breadth softened intraday (**67.4% > EMA20** vs ~77% at midday) but stayed constructive; BTC ATR percentile 38 (normal vol). Institutional bid intact (Strategy +1,587 BTC; BlackRock BTC yield ETF launching). HYPE the loudest narrative (ATH, perps DEX). The tape is a **pre-FOMC coil**, not a conviction breakout — the binary is tomorrow morning.

### Market Mood / Risk Routing      (REQUIRED)
- **Crypto mood:** **risk-on but coiled / pinned under $67K + FOMC overhang** → effectively *wait-for-trigger*.
- **Stocks mood:** **closed** (post-cash); today's close **mixed / rotational** (Dow +, Nasdaq/S&P −, tech out).
- **Dominant narrative:** pre-FOMC positioning (June 17, Warsh) + tech→value rotation; crypto sub-narratives: perps/DEX (HYPE ATH), ETH (Glamsterdam fork final stage + ETF inflows), RWA (ONDO/XLM), AI rotation (TAO/NEAR, but those were *down* today).
- **Preferred side now:** **wait-for-trigger / manage existing** — RS-leader longs (ETH) only on a pullback *after* the Fed; no fresh shorts (regime risk-on); no naked size into FOMC.
- **Best long candidate:** none clean for fresh entry tonight → **long-watch ETH/USDT** (pullback that holds + BTC reclaim $67K) and **JPM** (RTH retest 328–330 next session, post-FOMC).
- **Best short candidate:** none live → **short-watch BTC/USDT** — only a decisive **$67K rejection that loses $64K** post-Fed opens a failed-retest short toward $63.3K.
- **Best catalyst-backed candidate:** **HYPE/USDT** (perps-DEX, ATH, 16 news/24h — but overextended, `wait_pullback`) and **ETH** (fork + ETF inflows, RS leader) — both pullback-only.
- **What to avoid:** chasing the **no-catalyst pumps (SENT +37%, HMSTR, WLD)** while extended/thin-volume; **UNH** (DOJ Medicare-fraud probe, −16% — now correctly rejected by the desk); any **fresh naked size carried into the June 17 FOMC.**
- **What would change the view:** the **June 17 FOMC outcome** (dot plot + Warsh tone) and BTC **reclaiming/holding $67K** (→ $68.5–70K) or **losing $64K** (→ $63.3K, opens short-watch).

## 7. Candidate Deep Dives (≤ 5)

### 7.1 ETH/USDT — crypto RS-leader long — **LONG-WATCH (best long idea; pullback / post-FOMC)**
- The day's standout: BTC trend up, **ETH up ~+10.9% and leading** (+43% YTD per source), with a real catalyst — **Ethereum's "Glamsterdam" fork entered its final development stage** (CryptoBriefing/CoinDesk, scalp §5) plus ETF inflow tailwind. RS-leader long in a risk-on tape = the cleanest *directional* read.
- Reaction/chase check: **price has already run hard today (+10.9%)** → entering at the high into the Fed is a chase. Not in the active-signals B-list as a fresh trigger; this is a *watch*, not a market-buy.
- Mood-aligned: yes (risk-on, RS leader). Actionable now: **no — long-watch on a pullback that holds + BTC reclaiming $67K post-Fed.** Invalidation: ETH loses its RS leadership / BTC loses $64K. Chase-risk: yes if bought at today's high into FOMC.

### 7.2 HYPE/USDT — perps_dex narrative primary — **CATALYST-WATCH (overextended, wait pullback)**
- Strongest catalyst-backed name: **+10.4% session, +15.9% week, fresh ATH, 16 news_items/24h**, perps_dex_narrative primary, Bitwise Hyperliquid ETF AUM growing, SpaceX-IPO derivatives volume routing through its L1 DEX. Basket source `single_source`, fresh <1h, playbook **`wait_pullback`**.
- Chase check: **at/near ATH = maximally extended**; not in active-signals (no `proposed_signal` — research/watch only). Buying the ATH print into the Fed is the textbook chase.
- Mood-aligned: yes (risk-on, leading narrative). Actionable: **no — catalyst-watch, wait for a pullback that holds + basket upgrade beyond single_source.**

### 7.3 BTC/USDT — the macro pivot — **WAIT-FOR-TRIGGER (range $65–67K into FOMC)**
- Coiled $65–66K under $67K all day; institutional bid intact (Strategy +1,587 BTC; BlackRock yield ETF). Levels: resistance **$67K / $68.5K / $70K**, support **$64K / $63.3K**.
- Reaction/chase check: no breakout, no breakdown — there is **no clean BTC entry tonight**; it is the *condition variable* for the alt book. Entering either side ahead of a binary Fed = gambling the event.
- Mood-aligned: risk-on but event-gated. Actionable: **no fresh entry — wait for the post-Fed reaction.** Long-trigger: reclaim + hold $67K. Short-trigger: reject $67K and lose $64K.

### 7.4 WLD/USDT — top crypto B (scalp 71.9 / intraday momentum 91.6) — **LONG-WATCH (pullback only, no catalyst)**
- Highest momentum score in the crypto reports (intraday 91.6, +13% 24h, +25% 7d, RS +14%), top B-tier scalp idea **71.9**. But: **volume 0.35x (thin / fading), no fresh verified catalyst** (1 news mention/24h), `crypto_scalp_momentum_continuation` flagged **low_confidence** with the desk's own failure mode — **TP1 ~1.86R vs typical captured MFE 0.54R → mean-reverts before TP.**
- Chase check: extended move on declining participation; the report itself says **pullback-only entry into 0.6447–0.6561, no market buy if extended.**
- Mood-aligned: nominally (RS long) but poor setup quality for fresh entry. Actionable: **only on the specified pullback with a volume reclaim; otherwise watch.** Invalidation: 1h close beyond 0.6307.

### 7.5 JPM — stocks A-tier long (final read 82.2) — **PLANNING-ONLY (market closed; retest next session post-FOMC)**
- Final stocks intraday read scored JPM **A-tier 82.23, high confidence**, financials/RS-leader, **earnings: safe** — but the report self-labels **"MARKET CLOSED — A/B entries demoted to C, NOT actionable."** Financials (Goldman/AmEx) were among the day's green names, consistent with the value rotation.
- Headline check (§I): background civil item — *"JPM Sued Over $328M Crypto Scam"* — a third-party-scam civil suit, **immaterial to a ~$600B+ bank**; no indictment/SEC probe of JPM itself. Does not invalidate the technical thesis.
- Mood-aligned: yes (long, value-rotation beneficiary). Actionable now: **no — market closed.** Trigger: RTH **retest into ~328–330** next session, *after* the FOMC, with SPY/XLF firm; invalidation close < 326.4. RR-to-TP1 was tight (~1.0) earlier → modest size only.

## 8. Best Candidates Ranked

No clean fresh-entry candidate in this post-close / pre-FOMC window (market closed for stocks; crypto event-gated). Per routing, the best *watch* candidates with exact triggers:

1. **long-watch — ETH/USDT (crypto):** trigger = **pullback that holds + BTC reclaiming $67K** post-Fed; ETH RS leadership (+10.9% today, fork + ETF) is the tell. Best directional idea once the event clears.
2. **long-watch — JPM (stocks):** trigger = RTH **retest 328–330 next session after the FOMC** with SPY/XLF firm; invalidation close < 326.4. (Tight RR → modest size.)
3. **catalyst-watch — HYPE/USDT (crypto):** trigger = **pullback off the ATH that holds + basket upgrades beyond single_source**; do not buy the ATH.
4. **wait-for-trigger — BTC/USDT (crypto):** long only on **reclaim + hold $67K**; this is the gate for the whole alt book.
5. **short-watch — BTC/USDT (crypto):** trigger = **$67K rejection that loses $64K** post-Fed → failed-retest short toward $63.3K. Not live (risk-on).

## 9. Avoid / No Trade (this decision window only)

- **Chasing the no-catalyst pumps** — SENT (+37%, thin, negative funding = squeeze-prone but extended), HMSTR, WLD (volume fading, mean-revert-before-TP flag).
- **UNH long** — active DOJ Medicare-fraud probe, −16%; the desk now rejects it (no_trade 36.03) — keep it rejected.
- **Buying HYPE/ETH at today's highs** into the Fed.
- **Any fresh naked size carried into the June 17 FOMC decision** — overnight crypto longs face the Fed/dot-plot binary; stock ideas are closed anyway.
- _This applies only to the current decision window. Scanner, candidate generation, tracking, monitors and the scheduler continue uninterrupted._

## 10. Main Risks

- **FOMC tomorrow (Wed June 17), Warsh's first meeting** — top risk; hold is priced (~97–98%) so the **dot plot + tone is the binary**; a hawkish lean hits both classes; positioning into it dominates this slot.
- **Geopolitical re-risk:** a fresh telegram-tape headline — *"IRAN CAN THREATEN HORMUZ CLOSURE AGAIN, US INTEL WARNS"* — partly counters the US–Iran relief tailwind that drove this week's risk-on; watch oil/BTC if it escalates.
- **BTC pinned under $67K** — a failed reclaim + loss of $64K flips crypto short-watch quickly post-Fed.
- **Stock tech rotation:** today's Nasdaq/S&P weakness vs the "100% breadth / semis-leading" internal label is a contradiction — do not treat the regime label as a description of how today actually traded; favor confirmation.
- **No-catalyst momentum names** (SENT, HMSTR, WLD) prone to sharp mean-reversion (scalp horizon mismatch documented; PF 0.14 over 14d scalp).
- **Untracked alerts (23) + weak catalyst mapping (77.7%)** — measurement/integrity drag (§14).
- **§M ingest** result recorded in §13; if it failed it is non-blocking.

## 11. Action Plan — next 4 hours (overnight → Asia, into FOMC)

1. **No fresh naked crypto longs overnight** — keep exposure light into tomorrow's FOMC; let existing tracked signals run their stops/TPs.
2. **Treat overnight-into-Asia as a coil:** BTC most likely holds $65–67K; do not pre-position the Fed in either direction.
3. **Build the post-FOMC watchlist:** ETH pullback (+ BTC>$67K), JPM retest (328–330), HYPE pullback off ATH, BTC reclaim-$67K vs lose-$64K.
4. **Keep UNH rejected** (legal); do not let promotion logic surface it.
5. **Re-check at the 04:30 Asia / overnight slot**, then reassess immediately after the Fed decision tomorrow morning.

## 12. Final Verdict per Mode

- **Crypto scalp:** risk-on but no clean fresh entry; SENT/HMSTR/WLD extended on thin volume → **pullback-only watch**, low confidence (scalp horizon mismatch, PF 0.14/14d). No chase into the Fed.
- **Crypto intraday:** RS-leader longs (ETH) valid on pullbacks; **wait-for-trigger into FOMC**, size light. ETH is the best directional idea once the event clears.
- **Crypto swing:** carry-forward (report ~6.9h stale); thesis intact (risk-on, breadth ~67%) but **do not open fresh swing risk ahead of the Fed.**
- **Stocks intraday:** **CLOSED — planning only.** JPM = retest next session post-FOMC (was A 82.2); the actual session rotated *out* of tech → favor value/financials confirmation, not semis longs. No fresh entry.
- **Stocks swing/invest:** carry-forward planning context (~6.5h); no fresh action this slot.

## 13. Sources

- [Crypto Prices Today: Bitcoin $65–66K as FOMC Opens, Strategy Adds 1,587 BTC, Hyperliquid +10% — AnalyticsInsight](https://www.analyticsinsight.net/price-analysis/crypto-prices-today-bitcoin-fluctuating-between-65000-to-66000-as-fomc-opens-strategy-adds-1587-btc-hyperliquid-surges-10) — 2026-06-16 (WebFetch HTTP 200) — BTC ~$65,940, ETH ~$1,760 (res $1,820), **FOMC June 17 hold ~98.2% priced**, BTC res $67K/$68.5K/$70K, supp $64K/$63.3K, Strategy +1,587 BTC, HYPE +10.44%. *confirms.*
- [Bitcoin Price Today: BTC Holds $66K as the Fed's Big Day Arrives and Warsh Takes Over — BlockchainReporter](https://blockchainreporter.net/bitcoin-price-today-btc-holds-66k-as-the-feds-big-day-arrives-and-warsh-takes-over/) — 2026-06-16 (search-summary; WebFetch 403) — BTC ~$66,340, ETH +10.9% ~$1,843, FOMC June 17 hold 97.4%, Warsh first meeting, dot-plot/tone is the driver. *confirms.*
- [Stock Market Today (June 16, 2026): SpaceX jumps 20%; Nasdaq, S&P 500 decline — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-16-2026) — 2026-06-16 (search-summary; WebFetch 403) — **Dow +0.7–0.9%, Nasdaq −0.8 to −1.0%, S&P −0.4%, Russell −0.6%, rotation out of tech.** *confirms / contradicts internal "100% breadth bullish" label.*
- Internal: `news_items` (db/crypto_ai_desk.sqlite), `data/catalysts/2026-06-16/*`, crypto + stocks reports as listed in §2.

## 14. Fix Requests / TODO

### TODO-untracked-legacy-alerts
- **issue:** 23 crypto Telegram alerts today have no backing `proposed_signal` → excluded from PF/winrate/avgR; count is still rising within the day (14 → 17 → 20 → 23).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-16` → "23 untracked legacy crypto alert(s)" (ETH/JTO/XLM/WLD/GPS/INJ/ZRO scalp+swing).
- **suggested manual fix:** investigate the alert→`proposed_signal` registration path (PART 1 regression); ensure every Telegram-sent alert creates a trackable signal_id.
- **priority:** high
- **first observed:** carried from prior runs; re-confirmed 2026-06-16 23:24 EEST.

### TODO-catalyst-mapping-weak
- **issue:** 77.7% of catalyst_events have empty symbol (2,898/3,731); persistently > 50% across runs.
- **evidence:** scan of `data/catalysts/2026-06-16/catalyst_events.jsonl`; latest cycle 19-14 (other_news 466/500).
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (ticker/entity extraction, alias table).
- **priority:** medium
- **first observed:** recurring; re-confirmed 2026-06-16 23:24 EEST.

### TODO-stock-tickers-mapped-to-usdt
- **issue:** stock legal/earnings headlines tagged to crypto `/USDT` symbols (UNH/USDT, TSLA/USDT, SMCI/USDT) in the catalyst layer → asset-class mis-assignment artifacts.
- **evidence:** `cycle_19-14` "Top catalysts by importance" lists `TSLA/USDT [legal_risk]`, scalp §5b lists `UNH/USDT`, `SMCI/USDT`.
- **suggested manual fix:** audit news classification + asset-class assignment so stock headlines tag the equity ticker (not `/USDT`).
- **priority:** medium
- **first observed:** 2026-06-16 (carried from late-session run).

### TODO-regime-label-vs-session
- **issue:** stocks "regime: bullish, 100% breadth, semis/tech leading" is a 20-day-trend label and contradicted today's actual cash session (Nasdaq −1%, S&P −0.4%, tech rotation out). Risk of treating the label as a real-time session description.
- **evidence:** internal stocks intraday report §1 vs [TheStreet June 16 close](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-16-2026).
- **suggested manual fix:** surface a short-horizon (1d/intraday) breadth/return alongside the 20d trend label so the regime block reflects how the session actually closed.
- **priority:** low
- **first observed:** 2026-06-16 23:24 EEST.

### TODO-losing-buckets
- **issue:** crypto B-tier triggered winrate 15%; weekend signals winrate 9%; stocks A/B winrate 16.7% / PF 0.88 / totalR −2.0; stocks C-tier winrate 10% / PF 0.79 / totalR −10.
- **evidence:** `signal-stats` observations (manual approval required) for both asset classes (cycle_04 summary).
- **suggested manual fix:** review entry logic for B/C-tier triggered and weekend buckets; consider tightening triggers (advisory — no scoring change here).
- **priority:** medium
- **first observed:** recurring; re-confirmed 2026-06-16 23:24 EEST.

### TODO-reddit-social-403
- **issue:** Reddit social sources (Bitcoin/Ethereum/CryptoCurrency hot.json) return 403 Blocked during scalp/intraday report generation → social attention layer empty.
- **evidence:** `cycle_04_21-43_summary.md` scalp + intraday steps: repeated "Failed social source Reddit … 403 Client Error: Blocked".
- **suggested manual fix:** audit/replace Reddit social source (auth headers / alternate endpoint / drop if unfixable).
- **priority:** low
- **first observed:** 2026-06-16 (in today's cycle logs).
