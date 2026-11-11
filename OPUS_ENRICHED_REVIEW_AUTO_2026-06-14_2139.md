# Opus Enriched Review — late-session risk review (Sunday — US equities CLOSED) — Auto Cycle 21:39 EEST

## 1. Executive Summary

**Sunday 21:39 EEST "late-session risk" slot — US cash equities are CLOSED (weekend); crypto is the only live actionable class.** External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch verified on Al Jazeera live blog).

The decisive change since the 18:39 review is the **macro overlay flipping from "two-sided binary at the wall" to confirmed risk-off escalation.** Fresh internal Telegram headlines (18:36–18:42 EEST, WalterBloomberg) report an **Israeli attack on Beirut's southern suburbs and Iran cancelling flights in its western provinces**, and external corroboration confirms **Israel struck Beirut suburbs Sunday and Iran retaliated with a wave of missiles at northern Israel — the most serious escalation since the April truce** (explosions reported in Tehran/Tabriz/Isfahan). The US–Iran de-escalation draft that gave a mild risk-on tilt at 16:23/18:39 has been **overtaken by an active exchange of fire**. Net: the geopolitical tail the prior review flagged ("Israeli military preparing for possible fire") **has materialised** → crypto bias tilts **risk-off into the evening**.

BTC remains pinned on the **~$64K weekend wall** with a very compressed ATR percentile of **3** (desk 13:00 UTC snapshot, now ~8.6h carry-forward) — but with escalation live, the likely volatility expansion is **skewed downside**. **No A-tier in any class. No A/B in crypto scalp or intraday — both entirely C-tier watchlist.** A/B performance is weak and **net-negative**: the in-report block (16:21 snapshot) showed WR 16.9% / PF 1.00 / stop 39.8%, but the **fresh `signal-stats` CLI (authoritative, dedup'd) now reads WR 16.7% / PF 0.93 / avgR −0.024 / totalR −2.0R / 14W-30L / stopR 41%** over n=89 (B-tier only) — two more losses resolved since the report → below breakeven, not at it. The weekend bucket is especially poor (live **PF 0.16, 1W-6L, −5R**).

Active-signal changes since 18:39: a **new OPG/USDT intraday B (65.8, long) appeared `waiting_for_entry` (created 17:17)** — but it has **zero catalyst rows in news_items (24h)** and the same desk report flagged OPG ">2 ATR from EMA20; do not chase… converted to watchlist only." That is a **contradiction-risk chase** into a risk-off tape → **do-not-chase / pullback-only / effectively avoid this window**. **MEGA intraday B has STOPPED (18:03)** and is also the day's **1 untracked legacy alert** (sent 16:47, no proposed_signal link → no PF contribution). **TAO swing B and PHA swing B remain `triggered` → manage, not initiate.** Best fresh **long-watch MITO** (pullback-only, no catalyst); best **short-watch STG/NIGHT** on a failed retest — and shorts now have **macro support** if BTC loses the wall. Weekend bucket is statistically poor (prior signal-stats WR ~5%, PF 0.25). Advisory only; scanner/data-collection continue regardless.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-14_12-46_scalp_report.md` — mtime 15:46 EEST → **carry-forward** (~5.9h; data freshness 12:30 UTC). No newer scalp report since.
- **Crypto intraday report** `data/reports/intraday/2026-06-14_13-22_intraday_report.md` — mtime 16:22 EEST → **carry-forward** (~5.3h; data freshness 13:00 UTC). **Same snapshot the 18:39 review used — no new desk run since.**
- **Crypto swing report** `data/reports/swing/2026-06-14_01-32_swing_report.md` — ~17h → **stale** (>14h; excluded from final-verdict swing — active swing signals read live from DB instead).
- **Stocks intraday/swing/invest** — dated 2026-06-12 (Fri), ~50h → **stale**; markets CLOSED Sunday → planning context only.
- **Catalysts** `data/catalysts/2026-06-14/` — events.jsonl + narrative_baskets.jsonl (3) + latest cycle md `catalyst_cycle_09-29.md` (mtime 12:29 EEST). ⚠️ Catalyst layer last refreshed **12:29 EEST (~9.2h old)** → stale, context only.
- **LLM packet** `data/processed/llm_analysis_packet.md` (16:22 EEST, carry-forward); stocks packet 2026-06-12 (weekend, stale).
- **DB (read-only)** `db/crypto_ai_desk.sqlite`: proposed_signals (17 crypto rows last 30h), news_items (247 today / 407 in 24h), watchlist_alerts (7 today), signal_outcomes, signal_alerts.
- **External:** WebSearch ×2 (BTC price/liquidations + Israel-Beirut/Iran escalation) + WebFetch (Al Jazeera Iran-war live blog — verified, Jun 7–8 escalation pattern; recurring fresh Jun 14).
- **Note — CLI:** the read-only `src.cli active-signals` / `signal-stats` subcommands were **extremely slow** (no output for the full drafting window; recurring — see §14 `cli-latency`), so figures were first derived via **direct read-only SQL** on the DB (permitted under §A.1) + the in-report block. Both CLIs **eventually returned and confirmed/refined** the set: `active-signals` → **11 active crypto** (OPG intraday B `waiting`, TAO+PHA swing B `triggered`, NOT/ALLO/ATOM/CRV/CHIP/BANANAS/BABY at tp1/tp2 managed); `signal-stats` → **WR 16.7% / PF 0.93 / totalR −2.0R** (authoritative, slightly more bearish than the 16:21 report block). `detect_untracked_legacy_alerts` returned fast: **1 untracked alert (MEGA/USDT intraday B)**.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-14_default_schedule/`.
- `scheduler.log` mtime **21:03 EEST** (~36 min) → **fresh**.
- Latest cycle summary `cycle_05_14-29_summary.md` mtime **18:39 EEST** (~3h) → borderline, but scheduler.log fresh.
- Defer rule needs **BOTH** older than 3h → **scheduler.log fresh → review proceeds (no defer)**.
- Crypto scalp/intraday **carry-forward (~5–6h)**; crypto swing **stale (~17h)**; all stock reports stale (Friday — weekend, expected). Catalyst layer **~9h stale**. ⚠️ **news_items latest row is 18:42 EEST — no Telegram/news ingested for ~3h → collector appears stalled** (§14 `telegram-collector-stalled`).

## 4. What Changed vs Previous Review

Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-14_1839.md` (Sunday US-open-reaction slot, ~3h ago).

- **MACRO FLIPPED RISK-OFF (the headline change):** the prior review's "Israeli military preparing for possible fire" tail has **materialised**. Fresh Telegram (18:36–18:42): Israel attack on Beirut's southern suburbs + Iran cancels western-province flights; external confirms Israel→Beirut strike Sunday and Iran missile retaliation at northern Israel. The US–Iran de-escalation draft is now **overtaken by active fire** — the mild risk-on tilt is gone. Bias → **risk-off into the evening.**
- **New crypto B appeared then context worsened:** **OPG/USDT intraday B (65.8) created 17:17, `waiting_for_entry`** — but **no catalyst** (0 news_items 24h) and the desk report itself flagged OPG ">2 ATR; do not chase; watchlist only." Contradiction-risk chase (see §7 Candidate 1).
- **MEGA intraday B → STOPPED (18:03)** (was "triggered/managed" at 18:39). It is also the **1 untracked legacy alert** (sent 16:47, no proposed_signal link).
- **Carried managed A/B unchanged:** **TAO swing B and PHA swing B still `triggered`** (manage). WLD/FET/OPG-swing/RIF still stopped; NOT swing tp1_hit.
- **Desk snapshot identical:** no new scalp/intraday report since 16:21 — regime read (BTC transition_up @ wall, ETH downtrend, breadth 67.5%) is unchanged; the change is **time decay (now ~5–6h) + the materialised escalation**, not a new desk read.
- **Catalyst layer aged further (~9h)** and the **importance-overflow defect is worse than reported** (154 rows today with importance >1.0, not just the handful of Lookonchain spam). Collector stalled at 18:42.
- **Thesis:** **more cautious / tilted risk-off** vs 18:39 — same $64K-wall structure, but the binary has resolved toward the risk-off side.

## 5. Catalyst Coverage

- **news_items today: 247**; **mapped (non-null symbol): 35**; **unmapped: 212 → 85.8% unmapped.** **narrative_baskets: 3.**
- ⚠️ **CATALYST MAPPING WEAK THIS RUN — USE CATALYST LAYER AS CONTEXT, NOT FINAL DECISION.**
- ⚠️ **importance-overflow defect is large this run: 154/247 rows today carry `importance > 1.0`** (expected range 0–1). This inflates the importance ranking broadly, not just on Lookonchain spam → §14 `importance-overflow` (priority raised).
- **Top-3 unmapped headlines (representative noise/macro):** (1) `t.me/lookonchain` "Hey @K6501, welcome to Lookonchain" (join spam, see §14 `lookonchain-spam`); (2) `t.me/WalterBloomberg` "Iran's Tasnim says flights in western parts of the country canceled" (macro, not a coin catalyst); (3) `t.me/WalterBloomberg` "Advisor to Iran's Supreme Leader on Israel attack against Beirut's southern suburbs" (macro). The two WalterBloomberg rows are **real risk-off macro** but legitimately symbol-less (no ticker), so they correctly stay unmapped — they belong in the macro overlay, not the symbol map.
- **Active baskets (created 09:29 EEST, ~12h stale):** `momentum_breakout` (wait_pullback; primary MITO, CHIP; pure momentum, no news catalyst) · `perps_dex_narrative` (wait_pullback; HYPE — **stale, bearish, avoid**, Hayes exit ~Jun 4) · `delisting_thin_liquidity` (avoid_low_liquidity; World-Cup fan-token noise, no primary).
- Recurring >50% unmapped across runs → §14 `catalyst-mapping-weak`.

## 6. Market Landscape

- **Crypto (carry-forward, desk 13:00 UTC snapshot):** BTC **transition_up**, ETH **downtrend**; breadth **67.5% > EMA20 / 55% > EMA50**; BTC ATR pct **3** (very compressed → expansion risk, now **downside-skewed** given live escalation). Strongest: ZKC (100, +39%, 12.4× vol, chase), BANANAS31 (94, +27%), OPG (92, +19%, overextended), MEGA (92, +17%, vol 0.43× — thin), MITO (84, +20%), RIF (81). Weakest/short-bias: STG (−37%, but 7d +22% → mean-reversion off a pump, OI-up squeeze-prone), TRUMP (−9%), HMSTR (−8%), NIGHT (−8%). Narrative: **AI mixed** (TAO/FET/NEAR), Memes mixed; RWA/L2/Gaming quiet.
- **External macro (RISK-OFF):** BTC ~$64K weekend wall (carry from prior MetaMask read); broader June tape is a liquidation regime (early-June cascade to ~$59–61K, multi-$B liquidations). **Geopolitics escalating:** Israel struck Beirut suburbs Sunday; Iran retaliated with missiles at northern Israel — most serious escalation since the April 7 truce; Iran cancelled western-province flights. This is a **clear risk-off input** for crypto into the evening; with ATR coiled, a downside expansion is the higher-probability break.
- **Stocks: CLOSED (Sunday) — no US session.** Live A/B are invest/swing-mode, **paused (watchlist_only, 0× sizing)**: LLY (A long), AMD/SMH (B long), META/NFLX (B short), UNH (B long — **DOJ probe legal flag, see §7 Candidate 4**). Planning only; re-evaluate **Monday RTH**.

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:** **risk-off / cautious** — BTC pinned at the $64K wall, ATR coiled (pct 3), and a **live Israel-Iran escalation** has resolved the prior binary toward the downside. Route to defense/short-bias; longs require BTC to hold.
- **Stocks mood:** **closed** (weekend) — planning only; no RTH confirmation until Monday.
- **Dominant narrative:** **macro/geopolitics (Israel-Iran escalation)** overriding coin-level narratives; AI (TAO/FET) + small-cap momentum (MITO/CHIP) remain the only constructive crypto threads, but subordinate to macro.
- **Preferred side now:** **manage existing / wait-for-trigger; short-bias on confirmation** (failed retest if BTC loses the wall). Fresh longs only if BTC reclaims/holds $64K→$65K *despite* the escalation.
- **Best long candidate:** **none fresh-clean.** TAO (best catalyst-backed) is **triggered → manage, not initiate**. Fresh long-watch: **MITO/USDT** — trigger: held pullback into **0.0202–0.0209** with volume **and** BTC holding the $64K wall; stand aside while escalation is live.
- **Best short candidate:** **none clean yet**, but the side now has macro support. Trigger: **BTC loses transition_up / the $64K wall**, then short the **failed retest** of a weak high — **STG into 0.2638–0.2732** (stop >0.2848; OI-up squeeze caution, do not press the breakdown) or **NIGHT into 0.0316–0.0319**.
- **Best catalyst-backed candidate:** **TAO/USDT** (Bittensor AI; 1 corroborating news row 24h) — triggered → manage toward tp1, add only on a held pullback.
- **What to avoid:** **OPG intraday B chase** (no catalyst, >2 ATR, report says do-not-chase); chasing extended leaders (ZKC/BANANAS31 >2 ATR); MEGA (just stopped + thin 0.43× vol + Jun-23 unlock overhang); HYPE/perps-DEX (stale bearish); thin/MEXC World-Cup fan-token names; any new long into the escalation without BTC confirmation; all stocks (closed).
- **What would change the view:** BTC **holding/reclaiming $64K→$65K despite the escalation** + breadth rising = cautiously re-enable pullback longs; **BTC losing the wall** (or further Israel-Iran escalation headlines) = green-light failed-retest shorts; Monday RTH for any stock idea; a verified **de-escalation/ceasefire headline** would neutralise the risk-off tilt.

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — OPG/USDT (crypto, intraday, LONG B 65.8, **waiting_for_entry**, NEW 17:17) — CONTRADICTION-RISK CHASE → AVOID/DO-NOT-CHASE
- Entry 0.20523–0.20978, SL 0.19967, tp1 0.22191. OPG was a desk leader (+19.04% 24h, RS +18.67%, vol 3.17×) — but tagged **overextended**, and the intraday report explicitly scored it **36.1 (long): "Price is more than 2 ATR from EMA20; do not chase… Entry quality is weak because the move is extended… Converted to watchlist only: wait for pullback."**
- **Catalyst:** **NONE** — 0 news_items rows for OPG in 24h; not a basket primary. Pure momentum.
- **Contradiction risk:** a B-tier `waiting_for_entry` signal exists for a symbol the same report converted to watchlist-only as a do-not-chase. Mood-aligned? **No** — a momentum long into a live risk-off escalation. Reacted? Yes (+19%). Chasing? **Yes — textbook chase.** Overextended? **Yes (>2 ATR).** Actionable now? **No.** Late-session + escalation + no catalyst → stand aside.
- **Final verdict: AVOID / DO-NOT-CHASE (pullback-only). Only reconsider on a deep held pullback into 0.205–0.210 with volume AND BTC holding the wall; otherwise no entry. Below clean-actionable bar this window.** (Also feeds §14 `opg-contradiction`.)

### Candidate 2 — TAO/USDT (crypto, swing, LONG B 65.4, **triggered**) — BEST CATALYST-BACKED, MANAGE
- Entry 259.77–263.39, SL 255.34, tp1 273.05; AI / Bittensor narrative; 1 corroborating news_items row 24h (consistent with prior external corroboration).
- Mood-aligned? Partially (AI is the constructive thread) but subordinate to the risk-off macro. Reacted? Partly. Chasing? Already **triggered** → manage, do not initiate. Actionable now? **Manage** toward tp1; respect SL 255.34 / BTC losing the wall as invalidation.
- **Final verdict: HOLD / MANAGE (triggered). Manage toward tp1 ~273; SL 255.34; tighten if BTC loses the $64K wall on escalation; add only on a held pullback into 259.77–263.39. Size down (weekend + risk-off).**

### Candidate 3 — STG/USDT (crypto, C — WATCHLIST) — BEST SHORT-WATCH (NOW MACRO-SUPPORTED, SQUEEZE-CAUTION)
- Failed-bounce/retest short zone **0.2638–0.2732**; invalidation 1h close >0.2848; tp1 ~0.2386. 24h **−36.99%** but **7d +21.65%** (dump is mean-reversion off a pump). Derivatives: **price-down + OI-up = fresh shorts pressing → squeeze risk if price reclaims.** 0 news 24h.
- Mood-aligned? **Yes now** — risk-off macro supports the short side **if** BTC loses the wall. Reacted? Yes (−37%) — late to initiate fresh. Chase-risk? **Yes on the breakdown** (OI-up). Actionable? Only on a **failed retest** into 0.2638–0.2732 with stop >0.2848, ideally with BTC losing $64K.
- **Final verdict: SHORT-WATCH (caution). Failed-retest only into 0.2638–0.2732, stop >0.2848; do NOT press the breakdown (squeeze risk). Trigger strengthened by macro if BTC loses the wall. Alt: NIGHT failed retest 0.0316–0.0319.**

### Candidate 4 — UNH (stocks, invest/swing, LONG — paused) — LEGAL/HEADLINE RISK, AVOID
- **LEGAL/HEADLINE RISK (carried):** UnitedHealth faces a **DOJ criminal probe** (Optum Rx / physician reimbursement); shares fell ~16% on the news (internal catalyst rows, single_source). A **long** UNH signal contradicts an active DOJ-probe headline.
- Mood-aligned? N/A — stocks closed. Actionable? No.
- **Final verdict: AVOID / MANUAL REVIEW REQUIRED. Do not treat UNH long as actionable while the DOJ probe is live; revisit only with verified resolution at Monday RTH.**

### Candidate 5 — BTC/USDT (macro proxy, no live A/B) — THE WALL, NOW UNDER RISK-OFF PRESSURE
- No tradable A/B; this is the regime gate for every crypto idea. **~$64K weekend wall**, ATR pct 3 (coiled). The prior two-sided macro has resolved **risk-off** (live Israel-Iran exchange of fire). A volatility expansion is likely and now **downside-skewed**.
- Mood-aligned? It **defines** the mood. Actionable? Not directly — it is the trigger. **Hold/reclaim $64K→$65K despite escalation** = cautiously green-light pullback longs; **lose the wall** = green-light failed-retest shorts (STG/NIGHT).
- **Final verdict: REGIME GATE — risk-off lean. No direct trade; gates all candidates. Watch the wall closely into the evening; escalation headlines are the live catalyst.**

## 8. Best Candidates Ranked

No clean Telegram-actionable A/B this window (crypto scalp/intraday all C-tier; OPG B is a do-not-chase contradiction; carried A/B are triggered-manage or stopped; stocks closed). Per PART 9, watch list with exact triggers:

1. **Short-watch (now macro-supported):** **STG/USDT** — trigger: **failed retest** into 0.2638–0.2732, stop >0.2848, **and** BTC losing the $64K wall; do not press the breakdown (OI-up squeeze). Alt: **NIGHT** failed retest 0.0316–0.0319.
2. **Catalyst-backed (manage):** **TAO/USDT** (triggered) — manage toward tp1 ~273, SL 255.34; tighten on BTC losing the wall.
3. **Long-watch (fresh, conditional):** **MITO/USDT** — trigger: held pullback into **0.0202–0.0209** with volume **and** BTC holding the wall *despite* escalation; invalidate <0.0193. Stand aside while macro is risk-off.
4. **Avoid:** **OPG intraday B** (no-catalyst >2 ATR chase), MEGA (stopped + thin + unlock), HYPE/perps-DEX (stale bearish), ZKC/BANANAS31 (>2 ATR chase), UNH (DOJ probe).

## 9. Avoid / No Trade (this decision window only — scanner continues)

- **OPG/USDT intraday B chase:** no catalyst, >2 ATR, report says watchlist-only — do not chase; pullback-only.
- **Chase-extended longs:** ZKC (+39%, 12.4×), BANANAS31 (+27%) — >2 ATR from EMA20; wait for pullback.
- **MEGA/USDT:** just stopped (18:03), thin 0.43× vol, Jun-23 unlock overhang — no fresh entry.
- **HYPE / perps-DEX basket:** catalyst (Hayes $18M exit ~Jun 4) is stale/bearish — avoid as a long thesis.
- **STG breakdown chase (short):** OI-up squeeze risk; failed-retest only.
- **Thin/MEXC + World-Cup fan-token names** (delisting_thin_liquidity): avoid low-float dumps.
- **New longs into the live Israel-Iran escalation** without BTC reclaiming/holding the wall.
- **All stocks:** closed (Sunday); UNH additionally legal-flagged.
- This "no clean trade" verdict applies to **this window only** — it is **never** an instruction to pause the scanner, tracking, or data collection.

## 10. Main Risks

- **Geopolitical escalation is live and headline-driven:** Israel-Iran exchange of fire on Sunday with BTC ATR coiled (pct 3) → a sharp expansion is likely and downside-skewed; reversal risk on any de-escalation/ceasefire headline.
- **Weekend bucket is statistically poor** (prior signal-stats weekend WR ~5%, PF 0.25); thin liquidity amplifies fakeouts and squeeze risk (STG OI-up).
- **Authoritative performance is weak and net-negative:** the **live `signal-stats` CLI (dedup'd) reads WR 16.7%, PF 0.93, avgR −0.024, totalR −2.0R, stopR 41%** over n=89 — *below* breakeven (the 16:21 in-report block showed PF 1.00 / 28 losses; two more have since resolved to losses). By mode, one bucket runs PF 0.50 (−7R) and another PF 0.00 (0W-1L) while one is PF 1.40 (+6R); shorts PF 0.42 (−4R) vs longs PF 1.08; **weekend bucket PF 0.16 (1W-6L, −5R)**. (Raw `signal_outcomes` row-counts give absurd 94–100% winrates because the table stores repeated per-cycle snapshots — do **not** use for performance; see §14 `outcomes-snapshot-overcount`.)
- **Data-freshness degradation:** Telegram/news collector appears stalled at 18:42 (~3h gap); catalyst layer ~9h stale and 85.8% unmapped; desk reports ~5–6h carry-forward → reduced confidence, lean conservative.
- **CLI degraded:** `active-signals`/`signal-stats` hung again — DB read directly instead (no data loss, but the convenience path is broken). `ingest_enriched_review_sources` status at end of §13.

## 11. Action Plan — next 4 hours

1. **Watch the BTC $64K wall into the evening under risk-off pressure.** Hold/reclaim toward $65K *despite* escalation → cautiously enable pullback longs (MITO zone first). Lose the wall (or further Israel-Iran headlines) → enable failed-retest shorts (STG 0.2638–0.2732 / NIGHT 0.0316–0.0319).
2. **Manage, don't initiate, the triggered crypto A/B:** TAO swing (→ tp1 ~273, SL 255.34), PHA swing — respect stops; tighten on a wall break; no fresh size into weekend + risk-off chop.
3. **OPG intraday B:** treat as **do-not-chase / watchlist** — no entry unless a deep held pullback into 0.205–0.210 with volume AND BTC firm.
4. **No shorts pressed into squeeze risk** (STG OI-up); require a failed retest.
5. **Stocks:** nothing actionable until **Monday RTH**; UNH = AVOID pending DOJ-probe resolution; re-confirm LLY/AMD/SMH/META/NFLX at the open.
6. Scanner, tracking, catalyst collection, and outcome recording continue unchanged — but see §14 on the stalled collector / CLI latency / importance overflow.

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO clean A/B — watchlist only.** Best name MITO pullback-only; stand aside in risk-off chop.
- **Crypto intraday:** **NO clean A/B.** OPG B is a do-not-chase contradiction (avoid); MITO/STG/NIGHT watch with triggers; late-session — intraday entries are mostly too late to initiate fresh.
- **Crypto swing:** report stale (~17h); live A/B = TAO/PHA triggered (manage), others stopped. **Manage existing; no fresh swing initiation off stale data into escalation.**
- **Stocks intraday/swing/invest:** **CLOSED (Sunday)** — planning only; UNH AVOID (legal). Re-evaluate Monday RTH.

## 13. Sources

External (this run):
- [Israeli Military Strikes Beirut Suburbs in the Lead-up to Anticipated US-Iran Deal — Military.com (Jun 2026)](https://www.military.com/israeli-military-strikes-beirut-suburbs-in-the-lead-up-to-anticipated-us-iran-deal)
- [Iran war live: Israel/Lebanon strikes, Iranian missile retaliation — Al Jazeera live blog (Jun 7–8, 2026, WebFetch-verified)](https://www.aljazeera.com/news/liveblog/2026/6/7/iran-war-live-israel-kills-lebanon-general-pakistan-urges-end-to-war)
- [Israel steps up strikes in central Beirut — AOL/Reuters (Jun 2026)](https://www.aol.com/articles/israeli-strike-hits-central-beirut-042536657.html)
- [Bitcoin falls below $64,000, triggers $1.1B in liquidations — CryptoBriefing](https://cryptobriefing.com/bitcoin-falls-below-64000-triggers-11b-in-liquidations/)
- [Bitcoin June 2026 liquidation cascade explained — WazirX Blog](https://wazirx.com/blog/bitcoin-liquidation-cascade-june-2026/)

Internal (read-only): `data/reports/scalp/2026-06-14_12-46_scalp_report.md`; `data/reports/intraday/2026-06-14_13-22_intraday_report.md`; `data/catalysts/2026-06-14/{catalyst_events.jsonl,narrative_baskets.jsonl,catalyst_cycle_09-29.md}`; `db/crypto_ai_desk.sqlite` (proposed_signals, news_items, watchlist_alerts, signal_outcomes). Fresh internal Telegram macro rows: `t.me/WalterBloomberg` (Israel-Beirut strike / Iran flight cancellations, 18:36–18:42 EEST). UNH legal rows: DOJ-probe (single_source, internal news_items).

_Source-ingest CLI (`scripts.ingest_enriched_review_sources --asset-class crypto`) status: **succeeded** — `input: 5 | valid: 5 | rejected: 0; wrote 5 row(s) to news_items` (idempotent UPSERT on url). Citations JSON: `data/raw/enriched_review_sources/2026-06-14T21-39-00.json`._
_No fabricated TradingView/chart observations — only local OHLCV/ATR/EMA fields used. Lookonchain "welcome" rows filtered as non-news. No uncited stats; unavailable figures marked so. Web research AVAILABLE this run._

## 14. Fix Requests / TODO

### TODO-telegram-collector-stalled
- **issue:** No news_items ingested for ~3h — latest row is 18:42 EEST while the review runs at 21:39; the Telegram/news collector appears to have stalled.
- **evidence:** `select max(published_at) from news_items` → `2026-06-14T18:42:07Z`; `news last 4h = 6` (all ≤18:42).
- **suggested manual fix:** check the `CryptoAIDesk_TelegramCollector` Windows task / process health and restart if hung; add a freshness watchdog/alert when no news row lands for >60–90 min.
- **priority:** high
- **first observed:** 2026-06-14 21:39 EEST

### TODO-importance-overflow
- **issue:** `news_items.importance` exceeds its expected 0–1 range on a large fraction of rows (not just spam) — 154/247 rows today carry importance >1.0 — inflating the importance ranking used by catalyst diagnostics.
- **evidence:** `select count(*) from news_items where date(published_at)='2026-06-14' and importance>1.0` → 154 of 247.
- **suggested manual fix:** audit the importance-scoring/normalization step; clamp or renormalize to [0,1]; investigate why a majority of rows score >1.
- **priority:** high (raised from medium — far broader than the prior Lookonchain-only finding)
- **first observed:** carried (2026-06-14 18:39); breadth re-quantified 2026-06-14 21:39 EEST

### TODO-opg-contradiction
- **issue:** A B-tier intraday signal (OPG/USDT, 65.8, `waiting_for_entry`) was created (17:17) for a symbol the same desk report scored 36.1 and "converted to watchlist only: Price is more than 2 ATR from EMA20; do not chase," with no catalyst — a self-contradiction between the deep-analysis gate and the signal generator.
- **evidence:** `proposed_signals` OPG/USDT intraday B 65.8 created 2026-06-14T17:17; intraday report "OPG/USDT: score 36.1 (long) — … do not chase … Converted to watchlist only"; `news_items` OPG 24h = 0.
- **suggested manual fix:** ensure the signal generator inherits the "do-not-chase / >2 ATR / watchlist-only" demotion from the analysis layer so overextended no-catalyst names cannot be emitted as B `waiting_for_entry`.
- **priority:** medium
- **first observed:** 2026-06-14 21:39 EEST

### TODO-untracked-alert-mega
- **issue:** 1 untracked legacy crypto alert — MEGA/USDT intraday B was sent to Telegram (16:47) but has no matching proposed_signal, so it will not contribute to PF/winrate/avgR.
- **evidence:** `detect_untracked_legacy_alerts --since 2026-06-14` → 1 row (MEGA/USDT intraday B 65.8 long, sent 2026-06-14T16:47Z, "NO (no proposed_signal)").
- **suggested manual fix:** investigate the alert→proposed_signal linkage for MEGA intraday (PART 1 regression check); ensure every Telegram alert writes a trackable signal_id.
- **priority:** medium
- **first observed:** 2026-06-14 21:39 EEST

### TODO-cli-latency
- **issue:** `python -m src.cli active-signals` / `signal-stats` read-only subcommands hang with no output for the full drafting window (recurring — also 16:23 and 18:39). Forces a fallback to direct read-only SQL.
- **evidence:** both background CLIs produced only the echo header, no rows, after several minutes; `detect_untracked_legacy_alerts` and `ingest_enriched_review_sources` (same storage imports) return fast → latency specific to the `src.cli` entrypoint.
- **suggested manual fix:** profile the `src/cli` entrypoint; lazy-load heavy deps (exchange clients, agents, models) so read-only subcommands start in seconds.
- **priority:** medium
- **first observed:** carried (recurring; re-confirmed 2026-06-14 21:39 EEST)

### TODO-catalyst-mapping-weak
- **issue:** symbol mapping for catalysts remains <50% (14.2% mapped this run; ~84–86% unmapped across recent runs).
- **evidence:** 35/247 news_items mapped today (85.8% unmapped); same picture at 18:39.
- **suggested manual fix:** improve the symbol resolver (ticker/entity extraction); route symbol-less macro headlines (WalterBloomberg geopolitics) to a macro-overlay channel rather than counting them as unmapped catalyst failures; track mapped% as a health metric.
- **priority:** medium
- **first observed:** carried (re-confirmed 2026-06-14 21:39 EEST)

### TODO-catalyst-layer-stale
- **issue:** Catalyst cycle output last refreshed 12:29 EEST (~9h old at review time); narrative baskets stamped 09:29 (~12h).
- **evidence:** latest `catalyst_cycle_09-29.md` mtime 12:29; `narrative_baskets.jsonl` created_at 09:29.
- **suggested manual fix:** confirm the catalyst cycle is still scheduled on weekends; add a staleness flag when the latest cycle md is >4h old.
- **priority:** medium
- **first observed:** 2026-06-14 21:39 EEST

### TODO-lookonchain-spam
- **issue:** `t.me/lookonchain` join/welcome messages ("Hey @user, welcome to Lookonchain") are ingested as news_items and surface as top catalysts.
- **evidence:** top unmapped row today is `t.me/lookonchain` "Hey @K6501, welcome to Lookonchain" (18:12).
- **suggested manual fix:** add a source/title filter to drop welcome/join/share-link messages before they enter news_items.
- **priority:** medium
- **first observed:** carried (2026-06-14 18:39; re-confirmed 21:39 EEST)

### TODO-outcomes-snapshot-overcount
- **issue:** `signal_outcomes` stores repeated per-cycle snapshot rows; naive row-count aggregation yields impossible winrates (tens of thousands of rows / 94–100% WR) vs the authoritative `signal-stats` (n=89, WR 16.9%).
- **evidence:** raw group-by over 14d returns n in the tens of thousands; report `signal-stats` returns n=89 same week.
- **suggested manual fix:** document/ensure ad-hoc analytics dedupe to latest-per-signal_id; the `signal-stats` CLI already does.
- **priority:** low
- **first observed:** carried (2026-06-14 18:39; re-confirmed 21:39 EEST)
