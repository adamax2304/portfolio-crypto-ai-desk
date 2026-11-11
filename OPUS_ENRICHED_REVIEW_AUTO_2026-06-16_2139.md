# Opus Enriched Review — late-session risk review — Auto Cycle 21:30 EEST

## 1. Executive Summary

**Tuesday 2026-06-16, ~21:40 EEST "late-session risk review" slot — US cash session live (~14:40 ET, ~1h20 to the 16:00 ET / 23:00 EEST close).** External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch ×1 success on Yahoo Finance; one source 403'd and was skipped).

**The dominant fact this slot is an event overhang, not a setup: the FOMC two-day meeting opened today and the rate decision lands tomorrow, Wed June 17** ([Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-june-16-2026-highest-opening-values-in-two-weeks-113313567.html)). With ~1h20 of US trade left and a Fed decision the next morning, **this is a "protect, don't initiate" window** — late-session intraday longs are too late to enter cleanly and any fresh swing/overnight crypto long is exposed to tomorrow's Fed binary. Routing verdict: **wait-for-trigger / manage existing exposure; no fresh chase into the close or into FOMC.**

**Regime is still genuinely risk-on in both classes — this is a timing caution, not a risk-off call.** Crypto desk: BTC uptrend, ETH uptrend, alt breadth **77.3% > EMA20 / 86.4% > EMA50**, BTC ATR percentile 36 (normal vol), "selective longs, prefer pullbacks on relative strength." Stocks desk: regime **bullish**, VIX **15.86**, breadth **100% > EMA20/EMA50**, 4/4 indices uptrend, semis (SMH RS +13%) and tech leading. Live quotes corroborate: **BTC ~$66,300, ETH ~$1,795 (+4.1%)** — strongest open in two weeks, fueled by the **US–Iran ceasefire / peace framework (MOU signing June 19, Strait of Hormuz reopening)** easing oil and inflation fears ([Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-june-16-2026-highest-opening-values-in-two-weeks-113313567.html), [LatestLY](https://www.latestly.com/business/bitcoin-price-today-june-16-2026-btc-holds-steady-around-usd-66304-amid-geopolitical-relief-and-blackrocks-yield-etf-launch-7475172.html)). BTC remains **pinned under the $67K pivot** into the Fed.

**No A-tier anywhere; the cleanest idea is a stock B-long that is now too late to chase, and the loudest crypto name is a no-catalyst momentum chase.** Stocks intraday report (fresh, data 18:25 UTC) lists **JPM B-long 78.89 "actionable"** (financials RS-leader, RS +7.9% vs SPY, earnings-safe) and **SMH B-long** — but JPM's RR-to-TP1 is only **1.0 (<1.5)** and SMH carries the report's own failure-mode warning that **"SMH longs structurally lose in this regime."** Crypto's top B is **HMSTR (score 94, +15.5% 24h, RS +17%)** — but it has **no verified catalyst**, sits in the `momentum_breakout` basket (playbook `wait_pullback`), volume is fading (0.73x), and the scalp playbook flags it mean-reverts before TP1. **All three are pullback/retest-only — none is a clean late-session entry.**

**Legal/integrity flags:** **UNH (active C-tier stock long) is under a confirmed DOJ criminal+civil Medicare-Advantage fraud probe, shares −16%, with state AGs now joining** ([Healthcare Dive](https://www.healthcaredive.com/news/unitedhealth-under-investigation-department-of-justice-medicare/753913/), [QuiverQuant](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe,+Shares+Dive+16%25+on+Fraud+Investigation)) → **AVOID**. SMCI export-control indictment also re-surfaced (no active signal). **Integrity: 20 untracked legacy crypto alerts** (up 14→17→20 across today's runs) sent to Telegram with no `proposed_signal` → §14 TODO. **Catalyst mapping weak (77% unmapped) — treat the catalyst layer as context, not a final decision.** Advisory only; scanner / collection / tracking continue in all moods — nothing here says stop the system.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-16_16-13_scalp_report.md` — **FRESH** (mtime 19:13 EEST, ~2.5h; data 16:00 UTC).
- **Crypto intraday report** `data/reports/intraday/2026-06-16_16-29_intraday_report.md` — **FRESH** (mtime 19:29 EEST, ~2.2h; data 16:15 UTC).
- **Crypto swing report** `data/reports/swing/2026-06-16_13-32_swing_report.md` — **carry-forward** (mtime 16:32 EEST, ~5.1h; flagged).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-16_18-25_stocks_intraday_report.md` — **FRESH** (mtime 21:25 EEST, ~0.2h; data 18:25 UTC) — **the slot-relevant report.**
- **Stocks swing** `…13-44…` (mtime 16:44 EEST, ~5h) + **invest** `…13-54…` (mtime 16:54 EEST, ~4.8h) → **carry-forward** planning context (flagged).
- **Catalysts** `data/catalysts/2026-06-16/` present: `catalyst_cycle_16-29.md` (latest), `catalyst_events.jsonl`, `narrative_baskets.jsonl` (4 baskets). No catalyst-scan needed.
- **LLM packets** `data/processed/llm_analysis_packet.md` (crypto, 19:29) + `llm_stocks_packet.md` (stocks, 19:42) present.
- **Internal CLI:** `active-signals` crypto (**34 active, all long B**, scores 65–76) + stocks (**all C-tier** in the live signal table; JPM/SMH appear as B-tier *ideas* in the fresh stocks report but are not yet registered above C in active-signals); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-16` → **20 untracked**.
- **DB:** `db/crypto_ai_desk.sqlite` — `news_items` queried (134 rows last 4h; JPM ×3, WLD ×1, HYPE ×15; **UNH ×0** in last 24h despite catalyst-layer legal flag — see §5/§14).
- **External:** WebSearch ×2 (UNH DOJ probe; BTC/FOMC + US–Iran). WebFetch: Yahoo Finance BTC/ETH article → **HTTP 200, used**; blockchainreporter FOMC article → **HTTP 403, skipped** (fell back to search summary).
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-16T1839Z.json` (4 cited sources); ingest CLI result in §10/§13.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-16_default_schedule/`.
- `scheduler.log` mtime **19:43:28 EEST** (~2.0h old) → **FRESH**.
- Latest `cycle_*_summary.md`: `cycle_03_18-55_summary.md` mtime **19:43:27 EEST** (~2.0h); steps ok=16 failed=0.
- **Defer rule needs BOTH log AND latest cycle summary > 3h. Both ~2.0h → review proceeds.**
- Freshness labels: stocks intraday **FRESH** (~0.2h, slot-relevant); crypto scalp/intraday **FRESH** (~2.2–2.5h); crypto swing + stocks swing/invest **carry-forward** (~4.8–5.1h, inside use-but-flag band).

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-16_1842.md` (US open reaction review):

- **Window moved ~2h into RTH → late session (~14:40 ET, ~1h20 to close).** Posture shifts from "which open ideas confirmed / chase vs clean entry" → **"manage exposure into the close + tomorrow's FOMC; nothing fresh worth chasing."**
- **JPM downgraded A→B.** At 18:42 JPM was **A-tier 80.9 triggered**; the fresh stocks report now lists it as **B-tier 78.89 "actionable"** (still RS-leader, earnings-safe, RR 1.0). AMD dropped from B-tier 76.5 to **C-tier**; it had already run past TP1 at the open (chase flag confirmed — do not re-enter).
- **Untracked legacy alerts rose 17 → 20** (was 14 at 16:24). Steady climb across the day — recurring tracking-registration gap.
- **Catalyst unmapped 76.5% → 77.1%** — unchanged-bad.
- **Crypto thesis intact:** BTC still risk-on, range-capped under $67K; ETH now the visible outperformer (+4.1%). US–Iran relief tailwind persists; **FOMC overhang is the new front-of-mind item** vs the open-reaction slot.
- **Confirmed:** stock regime bullish/VIX ~16/breadth 100% holds; crypto alt breadth ~77% holds; UNH legal risk persists and is externally re-verified this run.

## 5. Catalyst Coverage

- `catalyst_events.jsonl` cumulative today: **3,231 rows**; mapped (non-null symbol): **739**; unmapped (null symbol): **2,492 → 77.1% unmapped**.
- Latest cycle (`cycle_16-29`) scanned 500 rows → 500 events, **4 narrative baskets**.
- **⚠ catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sample): "Lucky or insider info? Someone created a new wallet, spent $4.22M betting that Spain would…"; "Corning vs. QuantumScape: Which Technology Stock Is a Better Buy in 2026?"; "People in China are watching the World Cup differently this time."
- Active narrative baskets: **perps_dex_narrative** (primary HYPE/USDT; `wait_pullback`, fresh <1h), **ai_narrative** (NEAR/RENDER/TAO/FET; `related_beta_rotation`, <6h), **rwa_narrative** (ONDO/XLM; `related_beta_rotation`, <6h), **momentum_breakout** (HMSTR/USDT; `wait_pullback`, <1h).
- Top catalysts by importance: TSLA earnings (Goldman raised Q2 delivery est, 0.77 — mapped TSLA/USDT, a crypto-class mis-map artifact), SOL treasury/partnership (0.71), ONDO/Mirae RWA (0.69), PLTR partnership (0.68), BTC IREN/BlackRock yield-ETF (0.66).
- **Integrity note:** the scalp report's §5b flags **UNH/USDT [legal_risk] DOJ probe** and **SMCI/USDT [legal_risk] indictment**, yet `news_items` has **0 rows tagged "UNH" in 24h** — the legal headline is being captured in the catalyst layer but not surfacing as a symbol-tagged `news_items` row → mapping/classification gap (§14).

## 6. Market Landscape

BTC ~$66.3K holding a two-week-high zone, fourth-ish up session, **rejected at/under $67K** and consolidating into the Fed. ETH leading (+4.1%, ~$1,795). Crypto alt breadth healthy (77% > EMA20). Stocks broadly bullish — semis/tech RS leaders, financials firm (XLF), energy weakest (XLE RS −10.5%, consistent with oil falling on Iran relief). VIX 15.86 = calm. The whole tape is a **pre-FOMC drift**, not a conviction trend; the binary is tomorrow morning.

### Market Mood / Risk Routing      (REQUIRED)
- **Crypto mood:** risk-on, **range-capped under $67K + FOMC overhang** (effectively risk-on-but-pinned).
- **Stocks mood:** risk-on / bullish, **late session + pre-FOMC** (no fresh-entry edge this late).
- **Dominant narrative:** geopolitical relief (US–Iran ceasefire, Hormuz reopening) + pre-FOMC positioning; sub-narratives: perps/DEX (HYPE ATH), AI rotation (TAO/NEAR), RWA (ONDO/XLM), ETH spot-ETF inflows.
- **Preferred side now:** **wait-for-trigger / manage existing** — RS-leader longs only on a pullback/retest *after* the Fed; no fresh shorts (regime risk-on).
- **Best long candidate:** none clean for fresh entry now → **long-watch HMSTR/USDT** (only on a pullback into 0.0002 with volume; no chase) and **JPM** (retest of 328.7–329.8 next session, post-FOMC).
- **Best short candidate:** none — risk-on regime, no clean short setup. **Short-watch:** a decisive BTC failure/rejection at $67K that breaks $64K, or SMH losing its intraday trigger (its own failure-mode flag) — neither is live.
- **Best catalyst-backed candidate:** **HYPE/USDT** (perps_dex basket, ATH, fresh <1h — `wait_pullback`, overextended) and **ETH** (spot-ETF inflows, +4.1% RS) — both pullback-only.
- **What to avoid:** **UNH** (DOJ fraud probe, −16%); **SMH long** (report's own structural-loss warning); chasing **HMSTR/AMD** while extended; any fresh size carried naked into tomorrow's FOMC.
- **What would change the view:** the **June 17 FOMC decision** (hold vs surprise) + BTC reclaiming/holding **$67K** (→ $68.5–70K) or losing **$64K** (→ $63.3K, opens short-watch).

## 7. Candidate Deep Dives (≤ 5)

### 7.1 JPM — stocks B-tier long (intraday) — **WAIT (too late to initiate; retest next session)**
- Source: fresh stocks intraday report, score **78.89**, status "actionable", playbook `stocks_intraday_rth_momentum`. RS vs SPY +7.87%, RS vs sector +4.77%, above prev-day high, **earnings: safe**. Entry zone 328.67–329.81, invalidation close < 326.39, TP1 333.22.
- Reaction/chase check: regime-aligned (financials firm), but **RR-to-TP1 only 1.0 (<1.5)** and it is now **~1h20 from the close** — an intraday momentum long entered this late has almost no runway and is exposed to tomorrow's Fed. Not overextended, but the *clock* invalidates a fresh entry.
- **Headline check (§I):** `news_items` shows a background item — *"JPM Sued Over $328M Crypto Scam: Compliance Failures Under Spotlight"* (Yahoo). This is a **civil suit tied to a third-party scam, immaterial to a ~$600B+ bank's fundamentals** — note it, but it does not invalidate the technical thesis. No indictment / SEC probe of JPM itself.
- Mood-aligned: yes (long, risk-on). Actionable now: **no — wait for an RTH retest of the entry zone next session, post-FOMC.** Invalidation: close < 326.39. Chase-risk: yes if entered now extended/late.

### 7.2 SMH — stocks B-tier long (intraday) — **AVOID (contradiction / structural-loss flag)**
- Source: same report, B-tier long, semis the strongest sector (RS +13%). **But the report's own playbook failure-mode note: "A-tier overpromotion on losing names — NVDA/SMCI/SMH longs structurally lose in this regime."** Self-contradicting signal.
- Contradiction risk: the technical/sector tailwind is real, but the desk's own backtest flags this exact long as a structural loser. Per routing, demote.
- Mood-aligned: nominally (long, risk-on) but **fails the system's own evidence test.** Actionable: **no.** A cleaner semis expression would be an individual RS-leader with a catalyst, not the SMH basket long.

### 7.3 HMSTR/USDT — crypto B-tier long (scalp/intraday/swing) — **LONG-WATCH (pullback only, no chase)**
- Source: top momentum across all crypto modes — score **94.0**, 24h **+15.5%**, RS vs BTC **+17.4%**, scalp signal **74.2** (medium, low_confidence overlay). `momentum_breakout` basket, playbook `wait_pullback`.
- Reaction/chase check: **price has already run +15.5%**, **volume fading to 0.73x** (no fresh participation), **no verified catalyst** ("pure momentum cluster"). Scalp playbook explicitly warns **TP1 ~1.86R vs typical captured MFE 0.54R → mean-reverts before TP.** Entering now = chasing an extended, news-less move.
- Mood-aligned: yes (RS-leader long in a risk-on tape) **but** the setup quality is poor for fresh entry. Actionable: **only on a pullback into ~0.0002 with a volume reclaim**; otherwise watch. Invalidation: loss of the breakout base / volume never returns.

### 7.4 UNH — stocks C-tier long (active signal) — **AVOID (verified legal risk)**
- `active-signals` shows UNH C-tier intraday + swing longs still active (score 54–62). **Externally verified:** UNH is under a **DOJ criminal + civil Medicare-Advantage fraud investigation**, shares **−16%**, with **state attorneys-general coordinating** as of June 2026 ([Healthcare Dive](https://www.healthcaredive.com/news/unitedhealth-under-investigation-department-of-justice-medicare/753913/), [QuiverQuant](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe,+Shares+Dive+16%25+on+Fraud+Investigation)).
- Verdict: **AVOID** — a long here is fighting an active federal fraud probe and a −16% gap. Headline risk dominates any technical read. (C-tier, so not a final-verdict actionable anyway, but explicitly flag so it is never promoted.)
- Integrity note: catalyst layer flags it but `news_items` has 0 UNH-tagged rows in 24h → §14.

### 7.5 HYPE/USDT — perps_dex narrative primary — **CATALYST-WATCH (overextended, wait pullback)**
- Strongest catalyst-backed name: **15 news_items mentions in 24h**, perps_dex_narrative primary, **HYPE at all-time high**, Hyperliquid ETFs drew $172M since launch (per scalp §5). Basket source `single_source`, fresh <1h, playbook **`wait_pullback`**.
- Chase check: **at ATH = maximally extended**; not in active-signals (no `proposed_signal` — research/watch only). Entering at ATH into FOMC is a chase.
- Mood-aligned: yes (risk-on, leading narrative). Actionable: **no — catalyst-watch, wait for a pullback that holds; do not buy the ATH print.**

## 8. Best Candidates Ranked

No clean fresh-entry candidate this late-session / pre-FOMC window. Per routing, the best *watch* candidates with exact triggers:

1. **long-watch — JPM (stocks):** trigger = RTH **retest into 328.67–329.81** next session *after* the FOMC decision, with SPY/XLF still up; invalidation close < 326.39. (Tight RR 1.0 → modest size only.)
2. **long-watch — HMSTR/USDT (crypto):** trigger = **pullback into ~0.0002 with a volume reclaim (>1x)**; no chase of the current +15.5% extension.
3. **catalyst-watch — HYPE/USDT (crypto):** trigger = **pullback off the ATH that holds + basket upgrades beyond single_source**; do not buy the ATH.
4. **catalyst-watch — ETH (crypto):** trigger = continued **spot-ETF inflows + BTC reclaiming $67K**; ETH RS leadership (+4.1%) is the tell.
5. **short-watch — BTC/USDT:** trigger = **decisive rejection at $67K that loses $64K** post-FOMC → opens a failed-retest short toward $63.3K. Not live.

## 9. Avoid / No Trade (this decision window only)

- **UNH long** — active DOJ Medicare-fraud probe, −16%; AVOID.
- **SMH long** — flagged structural loser in this regime by the desk's own playbook.
- **Chasing HMSTR / HYPE / AMD** while extended / at ATH.
- **Any fresh size carried naked into the June 17 FOMC decision** — late-session intraday entries have no runway and overnight crypto longs face the Fed binary.
- _This applies only to the current decision window. Scanner, candidate generation, tracking, monitors and the scheduler continue uninterrupted._

## 10. Main Risks

- **FOMC decision tomorrow (Wed June 17), Warsh's first as chair** — top risk; a hawkish surprise hits both classes; positioning into it is the binary that dominates this slot.
- **BTC pinned under $67K** — a failed reclaim + loss of $64K flips crypto short-watch quickly.
- **No-catalyst momentum names (HMSTR, SENT)** prone to sharp mean-reversion (scalp horizon mismatch documented).
- **Stock-long structural drag:** season-long stocks intraday longs are the worst bucket (PF 0.3–0.7), C-tier winrate 9% — favor confirmation + modest size; the recent 14d B-tier window (WR 55%, PF 2.03) is the only encouraging subset.
- **Untracked alerts (20) + weak catalyst mapping (77%)** — measurement/integrity drag (§14).
- **§M ingest** result recorded in §13; if it failed it is non-blocking.

## 11. Action Plan — next 4 hours

1. **Do not initiate fresh intraday longs into the US close** (~1h20 left) — no runway.
2. **Do not carry fresh naked crypto longs into tomorrow's FOMC** — keep overnight exposure light; let existing tracked signals run their stops/TPs.
3. **Build the post-FOMC watchlist:** JPM retest (328.7–329.8), HMSTR pullback (~0.0002 + volume), HYPE pullback off ATH, ETH (ETF inflows + BTC>$67K).
4. **Mark UNH long as AVOID** (legal); do not let any promotion logic surface it.
5. **Re-check at the 23:15 post-close slot** — daily wrap + overnight-into-Asia crypto setup; reassess immediately after the Fed tomorrow.

## 12. Final Verdict per Mode

- **Crypto scalp:** risk-on but no clean fresh entry; HMSTR/SENT extended → **pullback-only watch**, low confidence (scalp horizon mismatch). No chase.
- **Crypto intraday:** RS-leader longs valid on pullbacks; **wait-for-trigger into FOMC**, keep size light. Best watch: HMSTR pullback / ETH.
- **Crypto swing:** carry-forward (report ~5h stale); thesis intact (risk-on, breadth 77%) but **do not open fresh swing risk ahead of the Fed.**
- **Stocks intraday:** bullish regime, but **too late to initiate**; JPM = retest next session post-FOMC, SMH = avoid (structural flag), UNH = avoid (legal). No fresh entry now.
- **Stocks swing/invest:** carry-forward planning context (~5h); no fresh action this slot.

## 13. Sources

- [Bitcoin and ethereum prices today, Tuesday June 16 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-june-16-2026-highest-opening-values-in-two-weeks-113313567.html) — 2026-06-16 (WebFetch HTTP 200) — BTC ~$66.3K, ETH ~$1,795 (+4.1%), **FOMC two-day meeting opened June 16, decision June 17**, US–Iran relief. *confirms.*
- [Bitcoin Price Today, June 16 2026 — LatestLY](https://www.latestly.com/business/bitcoin-price-today-june-16-2026-btc-holds-steady-around-usd-66304-amid-geopolitical-relief-and-blackrocks-yield-etf-launch-7475172.html) — 2026-06-16 — BTC ~$66,304, geopolitical relief, BlackRock yield ETF. *confirms.*
- [UnitedHealth confirms DOJ investigation into Medicare billing — Healthcare Dive](https://www.healthcaredive.com/news/unitedhealth-under-investigation-department-of-justice-medicare/753913/) — 2026 — UNH confirms federal Medicare-Advantage probe. *confirms legal risk (primary-ish).*
- [UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% — QuiverQuant](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe,+Shares+Dive+16%25+on+Fraud+Investigation) — 2026-06-16 — −16%, criminal+civil, state AGs joining. *confirms legal risk.*
- Internal: `news_items` (db/crypto_ai_desk.sqlite), `data/catalysts/2026-06-16/*`, crypto + stocks reports as listed in §2.
- _blockchainreporter FOMC article returned HTTP 403 — not used as a citation (search-summary only)._

## 14. Fix Requests / TODO

### TODO-untracked-legacy-alerts
- **issue:** 20 crypto Telegram alerts today have no backing `proposed_signal` → excluded from PF/winrate/avgR; count is rising within the day (14 → 17 → 20).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-16` → "20 untracked legacy crypto alert(s)" (ETH/JTO/XLM/WLD/GPS/INJ/ZRO scalp+swing).
- **suggested manual fix:** investigate the alert→`proposed_signal` registration path (PART 1 regression); ensure every Telegram-sent alert creates a trackable signal_id.
- **priority:** high
- **first observed:** carried from prior runs; re-confirmed 2026-06-16 21:40 EEST.

### TODO-catalyst-mapping-weak
- **issue:** 77.1% of catalyst_events have null symbol (2,492/3,231); persistently > 50% across runs.
- **evidence:** scan of `data/catalysts/2026-06-16/catalyst_events.jsonl`; latest cycle 16-29 (other_news 478/500).
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (ticker/entity extraction, alias table).
- **priority:** medium
- **first observed:** recurring; re-confirmed 2026-06-16 21:40 EEST.

### TODO-unh-legal-not-in-news-items
- **issue:** UNH DOJ legal_risk surfaces in the catalyst layer (scalp §5b, mapped as UNH/USDT) but `news_items` has 0 UNH-tagged rows in 24h → legal headlines not surfacing as symbol-tagged news rows; also stocks tickers being mapped to `/USDT` (crypto class) artifacts (UNH/USDT, TSLA/USDT, SMCI/USDT).
- **evidence:** `news_items` query `detected_symbols_json LIKE '%"UNH"%'` last 24h → 0; catalyst_cycle/scalp report show UNH/USDT legal_risk.
- **suggested manual fix:** audit news classification + asset-class assignment so stock legal headlines tag the equity ticker (not `/USDT`) and land in `news_items`.
- **priority:** medium
- **first observed:** 2026-06-16 21:40 EEST.

### TODO-losing-buckets
- **issue:** crypto B-tier triggered winrate 15%; weekend signals winrate 9%; stocks C-tier winrate 9% / PF 0.73; stocks B-tier 18%.
- **evidence:** `signal-stats` observations (manual approval required) for both asset classes.
- **suggested manual fix:** review entry logic for B/C-tier triggered and weekend buckets; consider tightening triggers (advisory — no scoring change here).
- **priority:** medium
- **first observed:** recurring; re-confirmed 2026-06-16 21:40 EEST.

### TODO-reddit-social-403
- **issue:** Reddit social sources (Bitcoin/Ethereum/CryptoCurrency hot.json) return 403 Blocked during scalp report generation → social attention layer empty.
- **evidence:** `cycle_03_18-55_summary.md` scalp step: repeated "Failed social source Reddit … 403 Client Error: Blocked".
- **suggested manual fix:** audit/replace Reddit social source (auth headers / alternate endpoint / drop if unfixable).
- **priority:** low
- **first observed:** 2026-06-16 (in today's cycle logs).
