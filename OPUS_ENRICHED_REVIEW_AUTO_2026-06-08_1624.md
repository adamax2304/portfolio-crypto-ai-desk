# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:24 EEST

- **Generated:** 2026-06-08 16:24 EEST (auto-enriched-review, scheduled task `opus-enriched-review-preus`, **16:20 "pre-US-open decision review" slot**, executing `opus-enriched-review-4h/SKILL.md`). ~6 min before the US cash open (09:30 ET = 16:30 EEST).
- **It is Monday 2026-06-08.** US cash equities **open in minutes**; this is the final pre-open read — gap risk, overnight catalysts, and what is actionable AFTER the open vs what must wait the first 15–30 min RTH. Crypto is live/actionable; stocks are pre-open (pre-market data only).
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-08_1139.md` (Europe / pre-US context, 11:39 EEST, ~4.75h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded, both verified). Live: **BTC ~$62,971 (+1.74% 24h), ETH ~$1,675 (+3.41%)**; **US pre-market gapping UP on a tech relief rally** (MRVL +8.8% on S&P-500 add, MU +7.1%, GLW +9.3% on AMZN optical-fiber deal) with **rising Mideast tensions** as an offsetting tail risk; **WWDC keynote ran today** (Siri + Google Gemini, ~$1B/yr).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; structure = local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **The single most important pre-open fact is a STALE-DATA / GAP-RISK contradiction on the stock side.** The internal stocks report (data 11:57 UTC, regime **risk_off / bias short**, A/B=0, demoted to C — market closed) is now **~4.5h stale and points the wrong way versus the live tape.** Live pre-market is **gapping UP on a broad tech relief rally** after last week's −4% Nasdaq chip slide: **MRVL +8.8%** (added to S&P 500), **MU +7.1%**, **IPGP +8.2%**, **Corning GLW +9.3%** (AMZN multibillion optical-fiber deal). **Net read: the desk's short-heavy candidate list is being generated INTO a gap-up rebound — shorting tech/indices at the open is chase/squeeze risk, not a clean entry.**
- **Therefore the pre-open routing is: do NOT chase pre-market in either direction; require RTH confirmation.** For the short book (META short A 81.41, QQQ/XLK/SMH/AMD/NVDA/GOOGL shorts B) the trigger is a **post-open failed bounce / lower-high in the first 15–30 min**, NOT a market-on-open short into green futures. For longs, the relief leaders (MRVL/MU/GLW) confirm the tone but are not in our tracked A/B universe; the clean tracked long remains **LLY** (catalyst-backed) — but at/near ATH → wait a pullback or RTH continuation.
- **AAPL's binary is no longer "upcoming" — it happened.** WWDC ran today: Siri overhauled on **Google Gemini** (chat mode, personal context, ~$1B/yr deal), iOS 27 default-assistant Extensions. **AAPL retraced to the 0.236 Fib (~$303–307) off a recent peak** — a classic **"reveal, then sell-the-news" fade** even though BofA lifted its PT to $380. **Verdict: MANUAL REVIEW — the event is priced/known now; let the RTH reaction settle, do not pre-position.**
- **Crypto is a manage-don't-chase tape into the open.** BTC ~$62,971 (+1.74%), ETH ~$1,675 (+3.41%) — the relief bounce held and ETH firmed further, but BTC/ETH are still **range**, breadth **63.6% EMA20 / 25% EMA50** (short-term bounce, longer trend not reclaimed), **no fresh A/B in scalp or intraday.** The actionable item remains **ZEC (two B-tier longs TRIGGERED, in-position)** with a **net-negative/unresolved catalyst** (Orchard bug fixed NU6.2, but supply-doubt + Hayes exit) → **hold to SL, do not add.** ETF outflows remain the structural cap; crowded-short funding keeps fresh BTC/major shorts squeeze-prone.
- **Mideast tensions are the wildcard that could flip the gap-up.** A risk-on relief open built on a chip-led bounce is fragile if the geopolitical headline escalates — that is the main reason to demand RTH confirmation rather than trust the pre-market gap.
- **System integrity clean:** untracked legacy alerts **0**; scheduler fresh (log 15:00, last cycle `cycle_07_14-17` 15:00, ~1.4h). **Scanner keeps running in all moods — this is a route-and-wait verdict, never a stop command.**

---

## 2. Data Used

**Internal — crypto reports (freshness vs 16:24 now):**
- `data/reports/scalp/2026-06-08_11-34_scalp_report.md` — gen 14:34 EEST, **~1.8h → FRESH.** Regime transition (mixed); BTC/ETH range; breadth EMA20 63.64% / EMA50 25.00%; BTC ATR pct 67. No A/B. Best watchlist WLD 63.5.
- `data/reports/intraday/2026-06-08_11-47_intraday_report.md` — gen 14:47 EEST, **~1.6h → FRESH.** No A/B. Best watchlist WLD 63.9 / ONDO 62.6. AI narrative "rising" (heat 57). ONDO unusual volume (1.56x, breakout tag).
- `data/reports/swing/2026-06-08_01-10_swing_report.md` — gen 04:10 EEST, **~12.2h → BORDERLINE STALE** (flagged §3; context only).
- Stocks: intraday `2026-06-08_11-58` (~1.4h generated, but **header = market closed/after-hours, data 11:57 UTC → pre-open planning only**); swing `2026-06-08_01-14` / invest `2026-06-08_01-18` (~12.1h **borderline stale**).

**Catalyst / narrative:** `data/catalysts/2026-06-08/` — `catalyst_events.jsonl` (**1442 raw rows**; reports count 513 *unique*), `narrative_baskets.jsonl` (**4 baskets**), latest cycle `catalyst_cycle_11-48.md`. Mapped **390/1442 (27.0%)**, unmapped **1052/1442 (73.0%) → weak (§5).**

**LLM packets:** `data/processed/llm_analysis_packet.md` (crypto, 14:47), `data/processed/llm_stocks_packet.md` (stocks, 14:58).

**Scheduler:** latest folder `data/scheduled_runs/2026-06-07_default_schedule/`; `scheduler.log` mtime **15:00 (~1.4h)**; latest cycle summary `cycle_07_14-17_summary.md` mtime **15:00 (~1.4h)**. **NO DEFER** (both inside 3h).

**CLI / DB (read-only, this run):**
- `active-signals` crypto = **9 tracked** (ZEC swing+intraday+swing ×3, BANK swing ×2, WLD intraday, ALLO intraday, XLM swing, C/USDT scalp — all B-tier; ZEC rows TRIGGERED/managed).
- `active-signals` stocks = many rows, **all C-tier `waiting_for_entry`** (overnight scan demoted to C — market was closed): shorts META/QQQ/XLK/SMH/AMD/NVDA/GOOGL/AAPL/XOM/IWM/SPY/PLTR/AVGO/COIN/DIA/SMCI; longs LLY, UNH.
- `signal-stats` crypto (week, A/B): n=71, triggered winrate **23%**, PF **~1.40** (by-narrative), +8.0R; setup split shows one losing bucket (PF 0.83 / −2R) vs a strong one (PF 2.25 / +10R). Observation: tier=B winrate 23% low.
- `signal-stats` stocks (week): A-tier **PF 0.25 / winrate 12% (weak, n=22)**, B-tier **PF 0.79 / 20%**, C-tier **PF 0.45 / 12%** — all flagged "below 0.8" (recurring §14 TODO).
- `detect_untracked_legacy_alerts --since 2026-06-08` = **0 untracked** (clean).

**External (WebSearch/WebFetch, verified):** BTC/ETH live macro; US pre-market gap-up + tech relief leaders + Mideast tensions; AAPL WWDC Siri/Gemini reveal + retrace. Full URLs §13.

---

## 3. Scheduler / Data Freshness

- **No defer.** scheduler.log 15:00 (~1.4h), latest cycle summary `cycle_07_14-17` 15:00 (~1.4h) — both inside the 3h window; the 14:00–17:00 cycle is the active one.
- Crypto scalp/intraday **FRESH (~1.6–1.8h).** Crypto swing **~12.2h → borderline stale** (context only, not a fresh swing final verdict).
- Stocks intraday freshly generated (~1.4h) but **data 11:57 UTC and market-closed header → pre-open planning only, and now contradicted by the live gap-up tape (see §1/§6).** Stocks swing/invest **~12.1h → borderline stale.**
- Catalyst JSONL last cycle 11:48 UTC (≈14:48 EEST, ~1.6h).

---

## 4. What Changed vs Previous Review (`..._1139.md`, ~4.75h ago)

- **Stocks: the regime read flipped on the tape, not in the file.** At 11:39 the desk was pre-market **risk_off / short-bias** and that matched the morning mood. By the open, **live pre-market is gapping UP** on a chip-led relief rally (MRVL S&P-add +8.8%, MU +7.1%, GLW +9.3% on the AMZN-Corning deal). The internal stocks report still prints risk_off/short — **so the desk's short list is now stale vs a relief-bounce open.** This is the defining change and the core gap/stale-data risk for this slot.
- **AAPL: event resolved.** At 11:39 WWDC was an *upcoming* binary; now the keynote has **run** (Siri+Gemini, iOS 27). AAPL **retraced to ~$303–307 (0.236 Fib)** off its recent peak — a sell-the-news fade. The idea shifts from "wait for the event" to "the event is known; read the RTH reaction."
- **Crypto: marginally firmer, structurally unchanged.** BTC ~$62.8k → **~$62.97k (+1.74%)**, ETH ~$1,641 → **~$1,675 (+3.41%)** — ETH continues to lead the relief bounce. Still range / no fresh A/B / breadth 63.6% EMA20 / 25% EMA50. New intraday tell: **ONDO unusual volume 1.56x (breakout tag)** — RWA name worth watching on a pullback.
- **ZEC: unchanged and still live.** Two B-tier longs remain TRIGGERED/managed; catalyst read identical (Orchard fixed NU6.2, trust crisis residual, Hayes exited). Manage to SL, do not add.
- **Catalyst volume grew, mapping still weak:** 882 → **1442 raw rows**; mapped 25.3% → **27.0%** (still 73% unmapped → weak). Baskets 2 → **4** (added `ai_narrative`, `delisting_thin_liquidity`).
- **New tail risk:** **Mideast tensions** now cited as the swing factor capping the futures gap-up.
- **Thesis change:** from "pre-market risk_off, plan shorts/longs for RTH" → "**the open is gapping up into a relief rally; the desk's stale short list is a trap at the open — require RTH failed-bounce for shorts, do not chase the gap, and read the AAPL/WWDC reaction.**"

---

## 5. Catalyst Coverage

- **total catalyst_events today: 1442 raw rows (513 unique per report) · mapped (non-null symbol): 390 (27.0%) · unmapped: 1052 (73.0%) · narrative_baskets: 4.**
- **⚠ catalyst mapping weak this run — use catalyst layer as context, not final decision.** (73.0% unmapped; persistent across many consecutive runs — recurring §14 TODO.) Most unmapped volume is generic stock/finance-listicle and corporate-action noise, not tradable crypto catalysts.
- **Top 3 unmapped headlines:** (1) "Coinbase celebrates three-year anniversary of SEC lawsuit as an S&P 500 company" (imp 0.73 — backward-looking, not actionable); (2) "GoHealth files for Chapter 11 to hand ownership to lenders amid restructuring" (0.712 — micro-cap, not in universe); (3) duplicate Coinbase anniversary row (dedup gap).
- **Baskets:** `perps_dex_narrative` (primary HYPE; `wait_pullback`; single_source; <6h) · `ai_narrative` (NEAR/RENDER/TAO/FET; `related_beta_rotation`; <24h) · `delisting_thin_liquidity` (`avoid_low_liquidity`; <24h) · `momentum_breakout` (ALLO/SAHARA; `avoid_chase`; **<1h**, ALLO flagged overextended).
- **Top mapped catalysts:** BTC ETF outflows (regulatory_sector_headline; 3rd consecutive outflow week ~$4.21B/3wks; IBIT −$214M single-day); stock legal cluster **SMCI (export-control indictment 8-K), UNH (DOJ antitrust/fraud probe −16%)**; **Binance Futures launching USDⓈ-margined TradFi perps (2026-06-08, exchange_listing).**

---

## 6. Market Landscape

- **Crypto:** BTC range (~$62.97k, +1.74%), ETH range (~$1.675k, +3.41%). Breadth EMA20 **63.6%** / EMA50 **25%** (short-term bounce broad, longer trend not reclaimed). BTC ATR pct 67 (normal vol). Relief bid intact, ETH leading; **but no fresh A/B and regime "selective only; demand clean invalidation."** Crowded-short funding remains squeeze fuel → fresh BTC/major shorts dangerous. AI narrative "rising" (heat 57; NEAR/TAO); RWA firming (ONDO 1.56x volume breakout tag). Offset by persistent BTC ETF outflows.
- **Crypto leaders:** BANK (+17.8–20.6% 24h, RS +16–19%, but vol 0.17–0.29x — thin), SAHARA (+13% RS +11.8%), WLD (+9.5%, vol 1.1x — best-volume leader, desk's top watchlist), ONDO (+7%, **vol 1.56x breakout**), NEAR (+12%, AI). Weakest: OPN (−22.7%), EPIC (−17.7%), HOME (−14.5%) — **but all shorts capped (short_bounce_guard / thin_liquidity / squeeze risk).** RS leadership is mostly thin-volume → chase-risk, not clean fresh longs.
- **Stocks (PRE-OPEN, open 16:30 EEST):** Internal scan = **risk_off, bias short, VIX 18.84, A/B=0** (demoted to C; data 11:57 UTC) — **but the LIVE pre-market is gapping UP** on a tech relief rally (MRVL S&P-add +8.8%, MU +7.1%, IPGP +8.2%, GLW +9.3% AMZN deal). **The stale risk_off short list collides with a relief-bounce open.** Strong sectors (from report): tech (XLK +5.4% RS 20d), healthcare (XLV +4.9%), semis (SMH +4.7%). Weak: comms (XLC −5.7%), discretionary (XLY −5.0%). **WWDC ran today** (AAPL Siri+Gemini; stock retraced ~$303–307 = sell-the-news). **Mideast tensions** = the tail risk that could reverse the gap-up. Legal cluster (META FTC/Texas, UNH DOJ, SMCI indictment) carries into the open.

### Market Mood / Risk Routing      (REQUIRED — PART 4)
- **Crypto mood:**           chop / mixed leaning constructive (range BTC+ETH, ETH-led relief, breadth 63.6% EMA20 / 25% EMA50, no fresh A/B → manage, don't chase)
- **Stocks mood:**           pre-open, **gap-up relief rally on the live tape vs a STALE risk_off short-bias report** (mixed/contradictory — treat as gap-risk, demand RTH confirmation); Mideast-tension tail risk
- **Dominant narrative:**    US chip-led relief rebound after last week's −4% Nasdaq slide (MRVL S&P-add, AMZN-Corning, MU); AAPL/WWDC Siri+Gemini reveal (sell-the-news fade); crypto ETH-led relief bounce on crowded-short funding; ZEC privacy-coin post-exploit recovery (supply-doubt residual)
- **Preferred side now:**    wait-for-trigger / manage-existing (no chasing the gap either way; RTH confirmation required for stocks; crypto = manage runners, mild long-lean only on pullback holds)
- **Best long candidate:**   **catalyst-backed: LLY** (clean PBM/obesity catalyst) — but at/near ATH → **wait pullback or RTH continuation, do not chase.** Crypto long: none clean at-market — **long-watch WLD** (best-volume RS leader) / **ONDO** (1.56x breakout) on a pullback hold
- **Best short candidate:**  **short-watch META** (top A-tier short 81.41 + FTC/Texas legal overhang) — **only after an RTH failed-bounce / lower-high; do NOT short into the gap-up.** Index shorts (QQQ/XLK/SMH) same caution
- **Best catalyst-backed candidate:** **LLY** (PBM coverage, obesity portfolio) — clean & verified; ZEC's catalyst is net-negative/unresolved
- **What to avoid:**         shorting tech/indices market-on-open into a gap-up relief rally (squeeze risk); pre-positioning AAPL on the WWDC reveal (sell-the-news / event known); chasing ALLO at extension; adding to triggered ZEC longs; fresh BTC/major crypto shorts into crowded-short funding; SMCI/UNH longs (active legal risk)
- **What would change the view:** stocks — the first 15–30 min RTH print: gap-up that *holds with breadth* → relief-rally longs / shorts stand down; a gap-and-fade (especially on a Mideast headline) → the desk's short list re-validates. Crypto — BTC reclaiming+holding range-high with EMA50 breadth >30% (→ RS-leader longs) OR losing local support (→ shorts after failed retests)

---

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — META (stocks, SHORT, A-tier 81.41, pre-open/demoted-C) — TOP SHORT but DO-NOT-CHASE-THE-GAP
- **Status:** highest-conviction stock candidate this run (intraday short A 81.41, high confidence). Pre-open only; demoted to C (market was closed). Live tape is gapping up on a mega-cap tech rebound.
- **LEGAL/HEADLINE RISK (VERIFIED, supports the short, but ongoing not fresh-today):** FTC "social-network monopoly" antitrust case on appeal with **29 states + DC**; **Texas WhatsApp false-encryption suit (May 21, 2026).** Overhang, not a same-day catalyst.
- **Reaction/chase/mood check:** mood-aligned to the *report's* risk_off short-bias, but **MIS-aligned to the live gap-up open** — a chip-led relief rally can lift mega-cap tech including META → **shorting market-on-open is squeeze/chase risk.** Aligned: comms sector weakest RS (−5.7%). Actionable only after a **post-open failed bounce / lower-high.** Invalidation: META reclaiming and holding above the prior swing / a broad risk-on close.
- **Verdict:** **SHORT-WATCH — RTH failed-bounce confirmation only; AVOID at the open into green futures.**

### Candidate 2 — AAPL (stocks, WWDC binary now RESOLVED) — MANUAL REVIEW (sell-the-news)
- **Status:** carry-forward invest long (A-tier in prior runs) but this run's intraday scan has AAPL as a **short C**; WWDC keynote **ran today** (Siri overhaul on Google Gemini ~$1B/yr, iOS 27 Extensions). AAPL **retraced to the 0.236 Fib (~$303–307)** off a recent peak.
- **LEGAL/HEADLINE RISK:** none material this run; the risk is event/expectations (now realized), not legal.
- **Reaction/chase check:** the binary is **priced/known** — a "reveal, then fade" pattern is already visible (retrace despite BofA PT→$380). Pre-positioning now is event-chase on a resolved catalyst. Actionable only AFTER the RTH reaction settles (hold of ~$303 base = constructive; loss = sell-the-news continuation).
- **Verdict:** **MANUAL REVIEW REQUIRED — do not pre-position; read the first 30–60 min RTH reaction.**

### Candidate 3 — ZEC/USDT (crypto, B-tier LONG ×2, TRIGGERED) — CATALYST CONTRADICTION, manage don't add
- **Status:** two longs TRIGGERED/managed (swing entry ~424, intraday entry ~428; SL ~409–412, TP1 ~442–448). Live positions; current scan watchlist 52–53.6.
- **Catalyst (VERIFIED — net-negative/unresolved):** Orchard infinite-mint/double-spend bug **fixed via NU6.2 (June 3)**; **BUT** devs cannot cryptographically prove no pre-patch exploitation, and **Arthur Hayes exited** (drove the $624→$309 cascade). Funding negative (−0.0009), shorts may be crowded → squeeze-prone both ways.
- **Reaction/chase check:** recovery + short-covering bounce vs structurally unresolvable supply-doubt = contradiction. Positions already on with defined stops.
- **Verdict:** **HOLD to SL ~409–412 with discipline; do NOT add, do NOT treat as a clean catalyst long.**

### Candidate 4 — LLY (stocks, invest LONG, catalyst-backed) — BEST CLEAN LONG, chase-risk at ATH
- **Status:** carry-forward invest long; this run's stocks watchlist long (intraday C 63.91, swing-active). Pre-open only.
- **Catalyst (VERIFIED prior run, still valid):** all three major PBMs now cover Lilly's full obesity/GLP-1 portfolio (CVS Caremark Foundayo coverage began Jun 1); LLY at/near ATH; healthcare RS +4.9% (defensive RS leader).
- **LEGAL/HEADLINE RISK:** none found — catalyst is clean positive.
- **Reaction/chase check:** price has already reacted (ATH) → entry now = chasing an extended long. A defensive RS-leader long is the *most* defensible long even in a mixed/gap-risk open, but only on a controlled entry. Actionable on a **pullback to the breakout base or RTH continuation with volume.**
- **Verdict:** **Best clean catalyst-backed long, but WAIT — do not chase ATH; pullback/RTH-continuation entry only.**

### Candidate 5 — QQQ / XLK (stocks, index SHORTS, B-tier 74.x) — the "short tech into the gap" TRAP
- **Status:** QQQ short B 74.47, XLK short B 74.33 (also SMH 68.9, AMD 72.14, NVDA 66.16) — the desk's index/semis short cluster, all from the stale risk_off scan.
- **LEGAL/HEADLINE RISK:** none symbol-specific; the relevant risk is **regime-timing** — these shorts were generated before the gap-up relief rally and before MRVL's S&P-add / AMZN-Corning catalysts hit the tape.
- **Reaction/chase check:** shorting the indices/semis market-on-open into a chip-led gap-up = textbook squeeze/chase. **Only re-validates if the gap fails** (gap-and-fade, breadth rolls over, or a Mideast headline escalates).
- **Verdict:** **AVOID at the open; short-watch only on a confirmed RTH failed-bounce / breadth rollover.**

**Excess qualifiers (>5, logged per §F):** AMZN (short B 76.99 in report, but **POSITIVE catalyst** — Corning optical-fiber data-center deal → short is contra-catalyst, avoid); WLD/ONDO/NEAR (crypto long-watch on pullback — WLD best volume, ONDO 1.56x breakout, NEAR AI); BANK/ALLO/SAHARA (thin-volume RS leaders — chase-risk, watch only); SMCI (export-control indictment) & UNH (DOJ probe) — legal-risk, **AVOID / manual review**; AMD/NVDA/GOOGL shorts share the QQQ/XLK gap-trap caution.

---

## 8. Best Candidates Ranked

1. **LLY (stocks, long, catalyst-backed)** — best clean idea (PBM/obesity catalyst, healthcare RS-leader, no legal flag). **Action: WAIT for a pullback / RTH continuation — do not chase ATH.**
2. **META (stocks, short, A 81.41)** — top-conviction short + FTC/Texas legal overhang, BUT mis-timed vs the gap-up. **Action: short-watch, RTH failed-bounce only; avoid at open.**
3. **ZEC (crypto, long ×2, TRIGGERED)** — live positions, defined stops, catalyst contradiction. **Action: hold to SL ~409–412, do not add.**
4. **AAPL (stocks, WWDC resolved)** — binary now known, retracing (sell-the-news). **Action: manual review, read RTH reaction.**
5. **QQQ/XLK (stocks, index shorts B)** — the short-into-gap trap. **Action: avoid at open; short-watch on a failed-bounce / breadth rollover only.**

**Watch triggers (no clean fresh at-market trade this window):**
- **long-watch (catalyst) LLY:** trigger = RTH pullback to breakout base **or** confirmed continuation off the open with volume; avoid the ATH chase.
- **short-watch META (and QQQ/XLK):** trigger = post-open **failed bounce / lower-high** with breadth rolling over (and ideally a Mideast-driven risk-off turn); stand aside if the gap-up holds with broad participation.
- **long-watch WLD/USDT (crypto):** trigger = pullback into ~0.465–0.474 that **holds with volume ≥1x**; ONDO long-watch on a hold of the 0.361–0.366 zone with the 1.56x volume sustained.

---

## 9. Avoid / No Trade (this decision window only — never "stop system")

- **Shorting tech/indices market-on-open** (META/QQQ/XLK/SMH/AMD/NVDA) into a gap-up relief rally — squeeze/chase risk; wait the RTH failed-bounce.
- **Pre-positioning AAPL on the WWDC reveal** — event is resolved and the stock is fading (sell-the-news); read the RTH reaction first.
- **AMZN short** — contradicted by a same-day POSITIVE catalyst (Corning data-center deal); short is fighting the news.
- **Chasing crypto RS leaders at extension** (ALLO/BANK/SAHARA on thin volume) — desk's losing chase bucket.
- **Adding to triggered ZEC longs** — catalyst net-negative/unresolved; manage existing only.
- **Fresh BTC/major crypto shorts** — crowded-short funding = squeeze-prone; require a failed retest first.
- **SMCI / UNH longs** — active legal risk (export-control indictment / DOJ probe).
- *(Reminder: decision-window verdict only. Scanner, candidate generation, tracking, and monitors keep running.)*

---

## 10. Main Risks

- **Gap / stale-data risk (headline this slot):** the stocks report is risk_off/short while the live open gaps up — acting on the stale short list at the open is the biggest trap; demand RTH confirmation.
- **Mideast tensions:** a relief rally built on a chip bounce is fragile to a geopolitical escalation — the gap-up could reverse intraday.
- **AAPL sell-the-news:** a disappointing read of the Siri/Gemini reveal could drag the tech tape (semis still recovering); an upside surprise could squeeze the META/index shorts.
- **ZEC tail risk:** any evidence/rumor the Orchard bug WAS exploited pre-patch could re-crash supply-doubt names; SL discipline mandatory.
- **Catalyst mapping weak (73.0% unmapped):** treat catalyst layer as context only this run.
- **Stock A-tier bucket underperforming (PF 0.25 / winrate 12% week):** weight A-tier conviction as planning context, not blind trust — §14 TODO.
- **Data gaps:** no live social/on-chain/ETF-flow/liquidation feeds; swing reports ~12h (borderline stale).
- **Source ingest:** enriched-review sources JSON built + ingest CLI attempted this run; outcome noted in §13 footer.

---

## 11. Action Plan — next 4 hours

1. **At the US open (16:30 EEST):** do NOT chase the gap. **Wait the first 15–30 min RTH print.** If the gap-up holds with breadth → relief-rally tone, shorts stand down; if it gaps-and-fades (or a Mideast headline hits) → the desk's short list (META/QQQ/XLK/SMH) re-validates on a failed-bounce / lower-high.
2. **AAPL:** read the WWDC RTH reaction (hold of ~$303 Fib base = constructive; loss = sell-the-news). No pre-position.
3. **LLY:** best clean long — take a pullback to the breakout base or confirmed RTH continuation with volume; no ATH chase.
4. **Crypto (live):** manage ZEC longs to **SL ~409–412 / TP1 ~442–448**; do not add. No fresh long unless WLD/ONDO/NEAR give a clean pullback hold with volume. No fresh shorts (squeeze risk).
5. **Re-check at the 18:30 US-open-reaction sibling slot** for which pre-open ideas confirmed/failed and whether entries were clean.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** No fresh A/B. Manage runners; long-watch WLD/ONDO on pullback holds with volume. No chase.
- **Crypto intraday:** No fresh A/B. ZEC intraday long triggered → hold to SL. ONDO 1.56x breakout — watch on a pullback hold; NEAR (AI) long-watch.
- **Crypto swing:** ZEC swing long triggered (hold to SL); report borderline stale (~12h). No fresh swing A/B.
- **Stocks intraday:** Pre-open; report risk_off/A-B=0 is **stale vs a gap-up open** → planning only, RTH confirmation mandatory; do not short into the gap.
- **Stocks swing/invest:** Carry-forward LLY long (best clean, no ATH chase) + META short A (RTH failed-bounce only) + AAPL (manual, post-WWDC RTH); borderline-stale reports → plan, do not pre-position.

---

## 13. Sources

- [U.Today — XRP/BTC/ETH/HYPE price analysis for June 8](https://u.today/xrp-bitcoin-btc-ethereum-eth-and-hyperliquid-hype-price-analysis-for-june-8-are-top-tier-assets) — BTC ~$62,971 (+1.74%), ETH ~$1,675 (+3.41%); oversold relief-bounce context. *single_source; confirms crypto macro.* (2026-06-08)
- [TheStreet — Stock Market Today, June 8 2026: S&P 500 futures edge higher amid rising Mideast tensions](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-08-2026) — futures higher into the open; Mideast-tension tail risk. *single_source; confirms gap-up + tail risk.* (2026-06-08) — *note: WebFetch returned HTTP 403; headline/summary captured via WebSearch result, URL not independently re-opened.*
- [CNBC — Nasdaq falls 4% worst day since April 2025 as traders flee chip stocks](https://www.cnbc.com/2026/06/04/stock-market-today-live-updates.html) — last week's −4% chip-led selloff (the base the relief rally bounces from). *single_source; confirms prior selloff.* (2026-06-04)
- [TheStreet — Nasdaq falls 4% as semiconductor slide wipes $1T](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-05-2026) — $1T semis slide June 5; Broadcom AI-guidance + jobs/yields. *single_source; confirms context.* (2026-06-05)
- [Investing.com — S&P 500 selloff looks more like rotation than breakdown](https://www.investing.com/analysis/sp-500-selloff-looks-more-like-rotation-than-market-breakdown-200681625) — frames the move as rotation, not breakdown. *single_source; weakens the pure-risk_off read.*
- [heygotrade — Gemini-powered Siri headlines Apple's WWDC 2026 (verified via WebFetch)](https://www.heygotrade.com/en/news/apple-wwdc-2026-siri-ai-gemini/) — Siri on Google Gemini (~$1B/yr), iOS 27 Extensions; AAPL +~50% past year. *single_source; confirms WWDC reveal.* (2026-06-08)
- [TradingKey — Apple Intelligence is live: WWDC 2026 begins today](https://www.tradingkey.com/analysis/stocks/us-stocks/261952325-apple-intelligence-is-live-can-wwdc-2026-spark-an-iphone-supercycle-tradingkey) — AAPL ~$307 June 8, retrace to 0.236 Fib ~$303.63 (sell-the-news). *single_source; confirms AAPL reaction.* (2026-06-08)
- [Motley Fool — Apple's biggest AI test arrives June 8 (WWDC)](https://www.fool.com/investing/2026/06/02/apple-biggest-ai-test-june-8-whats-stake-wwdc/) — WWDC stakes, PT≈price pre-event. *single_source; confirms event framing.* (2026-06-02)

*Carry-forward verified prior run (`..._1139.md` §13): LLY PBM/obesity catalyst, META FTC/Texas legal overhang, ZEC Orchard fix + trust crisis (Hayes exit) — not re-fetched this slot (unchanged, <5h old). No fabricated chart observations; structure from local OHLCV/ATR/EMA + cited prints. Source-discipline checklist (§N): every external claim carries source+title+date+URL; no uncited stats/legal claims; no fixture/test URLs; web AVAILABLE this run (one URL returned 403, flagged inline).*

---

## 14. Fix Requests / TODO

### TODO-catalyst-mapping
- **issue:** catalyst symbol-mapping still weak — 1052/1442 rows unmapped (73.0%); persistent across many consecutive runs. Also a visible dedup gap (duplicate "Coinbase SEC anniversary" rows in the unmapped top-3).
- **evidence:** `data/catalysts/2026-06-08/catalyst_events.jsonl` (1442 rows, 390 mapped); top unmapped are generic finance-listicle / corporate-action noise + a duplicated headline.
- **suggested manual fix:** improve the symbol resolver / pre-filter generic finance-listicle sources; add headline-level dedup before importance ranking; consider importance-gating low-relevance feeds.
- **priority:** medium
- **first observed:** recurring (re-confirmed 2026-06-08 16:24 EEST)

### TODO-stocks-A-tier-bucket
- **issue:** stocks A-tier actionable bucket reproducibly losing — PF 0.25 / winrate ~12% (week, n=22), yet META is promoted A-tier short 81.41 this run.
- **evidence:** `signal-stats --asset-class stocks` (tier=A PF 0.25, winrate 12%, "below 0.8" observations).
- **suggested manual fix:** audit A-tier promotion criteria for stocks in risk_off/regime-transition tapes; consider tighter confirmation before A-tier in bias-short scans, especially when pre-market gaps contradict the overnight regime label.
- **priority:** medium
- **first observed:** recurring (re-confirmed 2026-06-08 16:24 EEST)

### TODO-stocks-stale-regime-vs-premarket
- **issue:** the stocks intraday report's overnight regime label (risk_off/bias-short, data 11:57 UTC) can be ~4–5h stale and directly contradicted by the live pre-market tape at the cash open (today: gap-up relief rally vs a short-heavy list). Acting on the stale list at the open is a structural trap.
- **evidence:** report header "market closed / after-hours, data 11:57 UTC", regime risk_off bias-short, A/B short cluster; live pre-market gapping up (MRVL/MU/GLW) per WebSearch (2026-06-08).
- **suggested manual fix:** add a pre-open refresh (or a futures/pre-market gap check + freshness banner) before the cash open so the regime label reflects the open, not the overnight snapshot; or auto-demote directional bias when pre-market gaps oppose the overnight regime.
- **priority:** medium
- **first observed:** 2026-06-08 16:24 EEST

### TODO-crypto-B-tier-winrate
- **issue:** crypto B-tier triggered winrate ~23% flagged low (week, n=71), though PF stays >1 (~1.40) on asymmetric R.
- **evidence:** `signal-stats --asset-class crypto` observations ("tier=B winrate 23% low").
- **suggested manual fix:** review B-tier entry timing / RR calibration; investigate why triggered winrate stays low while PF holds (large-R winners carrying many small losers).
- **priority:** low
- **first observed:** recurring (re-confirmed 2026-06-08 16:24 EEST)

### TODO-rss-source-health
- **issue:** recurring RSS/social source failures (Reuters Business, SEC EDGAR Filings, Yahoo Finance Top Stories; Reddit CryptoCurrency/Bitcoin/Ethereum).
- **evidence:** §9 Data Coverage in scalp/intraday reports (2026-06-08).
- **suggested manual fix:** audit the failing RSS/Reddit source configs (auth/rate-limit/URL drift).
- **priority:** low
- **first observed:** recurring (re-confirmed 2026-06-08 16:24 EEST)
