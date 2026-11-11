# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:24 EEST

_Slot: 16:20 pre-US-open decision review · Friday 2026-06-12 · ~09:24 ET, ~6 min before the **US cash open (16:30 EEST / 09:30 ET)**. Focus: final pre-open read — gap risk, stale-internal-data risk, overnight catalysts + pre-market reactions, which stock A/B are actionable after the open vs which must wait the first 15–30 min for confirmation, legal/headline/earnings check for EVERY stock A/B, crypto risk mood into the open. Do NOT chase pre-market without RTH confirmation. Advisory-only, read-mostly — no auto-trade, no code edits, paper-trading. §14 TODOs only, no fixes._

## 1. Executive Summary

**Risk-on into the US open — the tape gapped up overnight on Trump's claim the Iran war has "ended," and the internal desk reports (data ~11:15–11:30 UTC) now lag the live move.** External research **AVAILABLE** this run (WebFetch verified). As of ~12:00 UTC (web, §13): **BTC ~$63,718 (+3.4%/24h)**, **ETH ~$1,671 (+3.2%)**, global crypto cap **$2.25T (+1.7%)**, BTC dominance 56.3%. US futures **edge higher** after **Dow +1.86% Thursday** (50,841); **SpaceX debuts today** priced $135/share (~$1.78T val, ~$75B raised); **UMich June prelim consumer sentiment** is today's only notable data point.

**The single most important read for this slot: BTC has reclaimed the $63.5K pivot the 11:39 review flagged as the trigger that turns "RS-leader pops into trend longs."** Crypto mood flips from the 11:39 "chop/mixed" toward **risk-on (improving)** — but the desk's own reports still print BTC "range / transition_up" because they were generated ~2h ago, *before* this push. **Treat internal levels as slightly stale vs the live gap-up; this is the dominant stale-data/gap risk this window.** The macro driver is real but fragile — Trump has made repeated unfulfilled peace claims, so a re-escalation headline reinstates risk-off.

**No A-tier signals — crypto or stocks.** All 6 active crypto signals are **B-tier swing longs that have already hit TP** (realized) — **no fresh, waiting crypto A/B to act on.** Crypto RS-leaders (STG, XPL, LUMIA, PYTH, ENSO, TRUMP) are all **extended / chase-risk / watch-only** (`momentum_breakout` = wait_pullback). On stocks, the fresh 11:48 run was generated **pre-market** and demoted A/B→C, but it scored **JPM long A (80.98), AMD long B (79.94), LLY long B (66.62), SMH long B (65.2)** and short **NFLX (B)** — and `active-signals` now shows **JPM, AMD, LLY (B longs) + NFLX (B short) triggered.** These become the actionable-at-open set, **but only after the 16:30 RTH open confirms** — into a likely gap-up, chasing pre-market levels is the trap.

**Routed verdict (this decision window only — never a stop command):**
- **Best long candidate:** **JPM** — was desk A-tier (80.98), cleanest book name: **no legal/headline risk**, 15 Buy / 9 Hold / 0 Sell, PT $336.58 (+8.5%), earnings not until July 14, and a direct beneficiary of the SpaceX/mega-IPO underwriting wave. **Actionable AFTER the open with RTH confirmation** (first 15–30 min), not on the pre-market gap. Crypto best long-watch: a **pullback in an RS-leader** (none clean now — all extended).
- **Best short candidate:** **none clean.** **NFLX** (B short, communications = weakest sector, RS −3.4%) is a **short-watch only on an RTH rejection** — fading a risk-on gap-up at the open is low-quality. Trigger: failure to reclaim the entry band in the first 15–30 min with the broad tape rolling over.
- **Best catalyst-backed:** **AMD** (Citi upgrade on GPU potential + semis the strongest sector, SMH RS +7%) and **LLY** (FDA EBGLYSS approval + orforglipron pivotal-trial wins, healthcare strong) — both clean (no legal risk) **long-watches**, but **AMD is +300%/12mo (extended → require pullback/RTH confirm).**
- **What to avoid:** **chasing the gap-up at the open** (gap risk + stale internal levels); **UNH long** (active C long but carries a **DOJ antitrust/fraud probe, −16%** — AVOID); **SMCI** (export-control indictment overhang); chasing extended crypto leaders (STG/XPL/LUMIA); fresh shorts into the risk-on tape.
- **What would change the view:** **BTC losing $63.5K back** → fade the risk-on read; **US open breadth failing / the gap reversing** in the first 30 min → caution on longs; a **UMich sentiment miss** or an **Iran re-escalation headline** → risk-off snap-back.

**System health:** untracked-alert detector **clean (0)** — no PART-1 regression. Scheduler **fresh** (~1.6h, last cycle 14:49). Catalyst mapping **weak again — 77.0% unmapped** → catalyst layer is context, not a decision input. §14 TODOs persist (catalyst mapper; stock A-tier 0/8 wins PF 0.0; stock C-tier −23R losing book).

## 2. Data Used

- Crypto **scalp** — `data/reports/scalp/2026-06-12_11-31_scalp_report.md` (data 11:15 UTC) — **fresh** (~1.9h; header flags scalp **low-confidence**: PF 0.14 / TP1-horizon mismatch).
- Crypto **intraday** — `data/reports/intraday/2026-06-12_11-40_intraday_report.md` (data 11:30 UTC) — **fresh** (~1.7h).
- Crypto **swing** — `data/reports/swing/2026-06-11_14-18_swing_report.md` — **stale** (~23.1h; > 14h → excluded from fresh swing verdict, planning context only; flagged §3).
- **Stocks** intraday — `data/reports/stocks/intraday/2026-06-12_11-48_stocks_intraday_report.md` (data 11:48 UTC) — **fresh data but pre-market** (report header: "MARKET CLOSED — planning/watchlist only"; A/B demoted→C; US RTH opens 16:30 EEST). Stocks **swing/invest** — `..._14-23_` / `..._14-27_` (~23h) → **stale**, planning only.
- Catalysts — `data/catalysts/2026-06-12/` (events.jsonl + narrative_baskets.jsonl + `catalyst_cycle_11-40.md`, mtime 14:40) — **fresh** (~1.7h). `catalyst-scan` NOT re-run (dir present).
- LLM packets present: `data/processed/llm_analysis_packet.md` (~1.7h), `llm_stocks_packet.md` (~1.6h).
- CLI (this run): `active-signals` crypto (**6**, all B-swing longs already tp_hit) + stocks (**50**); `signal-stats` crypto + stocks (from cycle_02 14:49, ~1.6h); `detect_untracked_legacy_alerts` (**clean — 0 untracked**).
- Latest scheduler cycle: `cycle_02_14-19_summary.md` (finished 14:49, steps ok=16 failed=0).
- External: WebSearch ×4 (JPM/AMD/LLY premarket + ratings; US premarket/futures/data calendar; BTC/ETH June 12; LLY/NFLX legal/headline); WebFetch ×2 (Yahoo BTC/ETH June 12 **opened & cited §13**; TheStreet market-today **HTTP 403 → search-snippet only, single_source**). External research **AVAILABLE** this run.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **14:49** (~1.6h) — **fresh**, well inside the 3h defer threshold → **review proceeds normally**. Latest `cycle_*_summary.md` also 14:49 (~1.6h). Neither freshness check was > 3h; **no defer.**
- Crypto scalp/intraday + catalysts are **fresh** (~1.7–1.9h).
- **Stale flag:** crypto **swing** report ~23.1h (> 14h) → excluded from the fresh swing verdict; planning only. Stock swing/invest (~23h) likewise planning-only.
- **⚠ Gap / stale-internal-data risk (key for this slot):** the fresh stock report is **pre-market** (data 11:48 UTC, on Thursday-session carry-forward levels) and the crypto reports (data ~11:15–11:30 UTC) **predate the overnight risk-on push** — live BTC is ~$63.7K vs the desk's "range/transition_up." Into a likely **gap-up at 16:30 EEST**, internal entry/level numbers may be stale. Require RTH confirmation; do not act on pre-market levels alone.

## 4. What Changed vs Previous Review

Prior: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-12_1139.md` (Europe / pre-US context, 11:39 EEST).

- **Risk-on shift since 11:39.** 11:39 read the tape as "chop/mixed, range BTC / downtrend ETH." Live web now shows **BTC +3.4% to ~$63.7K and ETH +3.2% to ~$1,671**, with stocks/silver/crypto all gapping up on Trump's claim the **Iran war has ended** (§13). **Mood upgraded chop → risk-on (improving).**
- **BTC reclaimed the $63.5K trigger.** The 11:39 review said a reclaim+hold > $63.5K "turns leader pops into trend longs." That level is now reclaimed — though desk reports lag and still print "range."
- **Iran: de-escalation → "war ended" claim.** 11:39 had a "fragile halt." Now a stronger (but **skepticism-flagged**, repeatedly-unfulfilled) "war ended" claim driving the gap. More bullish, still fragile.
- **New event: SpaceX IPO debuts today** ($135/share, ~$1.78T val) — sentiment driver + bank-underwriting tailwind (JPM beneficiary).
- **Crypto active book fully realized.** 11:39 had 9 active B's (DEXE/HMSTR waiting). Now **6 B-swing longs, all tp_hit** — no fresh waiting crypto A/B. DEXE no longer an active waiting long-watch.
- **Stocks moved pre-market → minutes-to-open.** Same demoted-A/B set, but now `active-signals` shows JPM/AMD/LLY (B longs) + NFLX (B short) **triggered**; the 16:30 RTH open is the decision point.
- **Catalyst mapping** marginally changed: 78.1% → **77.0% unmapped** (still weak). TODO persists.
- **Untracked-alert detector** still **clean (0)** — no regression.

## 5. Catalyst Coverage

- Total `catalyst_events` today (`2026-06-12/catalyst_events.jsonl`): **2244** (cumulative across cycles; the per-cycle scan reports ~356/cycle and ~772 unique).
- Mapped (non-null symbol): **516**.
- Unmapped (empty symbol): **1728** → **77.0% unmapped**.
- `narrative_baskets`: **4** — `momentum_breakout` (wait_pullback; primary **TRUMP/USDT** +23.6%), `perps_dex_narrative` (wait_pullback; HYPE + DYDX/GMX/ASTER), `binance_ecosystem_teaser` (related_beta_rotation; BNB/ASTER), `delisting_thin_liquidity` (avoid_low_liquidity).
- **⚠ catalyst mapping weak this run — use the catalyst layer as context, not a final decision input.** (>50% unmapped, persistent every run.)
- Top 3 unmapped / basket-level headlines (context only):
  1. SpaceX IPO debut / valuation chatter (t.me/WalterBloomberg, basket-level — rumour/macro).
  2. "BlackRock files 8-A for yield-bearing bitcoin ETF; analyst expects launch next week" (The Block — regulatory, importance 0.75, basket-level).
  3. Iran "war ended"/oil macro lines (t.me/WalterBloomberg — macro, basket).
- Mapped top catalysts: **SMCI** (export-control indictment 8-K, legal_risk 0.77), **UNH** (DOJ antitrust/fraud probe, −16%, legal_risk 0.73), **BTC** (BlackRock yield-bearing ETF filing 0.75; Babylon $5B staked BTC + Aave 0.69).

## 6. Market Landscape

- **BTC** ~$63,718 (+3.4%/24h, web) — **reclaimed the $63.5K pivot**; desk report lags at "range/transition_up" (data 11:15–11:30 UTC). Dominance 56.3%. Downside pivot $63.5K then $61K.
- **ETH** ~$1,671 (+3.2%, web) — bounced but still **capped near $1,700** (desk trend "range/downtrend," relative laggard). A clean break+hold > $1,700 would confirm broad risk-on.
- **Alt breadth (desk):** 62.5% > EMA20 / **37.5% > EMA50** — still a leader-led, not-broad tape; the web gap-up may have lifted breadth since.
- **Crypto leaders (RS vs BTC, desk):** STG +28–29% (24h, +160%/7d!), XPL +37%, LUMIA +20%, ENSO +12%, PYTH +12%, TRUMP +22% (vol 1.65×) — **all extended, watch-only** (`momentum_breakout` = wait_pullback). Laggards / short-bias: BANANAS31 −28%, HOME −16%, HMSTR −11% (thin, squeeze-prone). **No clean fresh crypto long — chase-risk dominates.**
- **Derivatives:** STG funding **−0.011** (crowded shorts → squeeze-prone both ways); PYTH price↑+OI↑ (clean). Most leaders MEXC-fallback derivatives (positioning thin).
- **Stocks (pre-market → opening):** regime **chop**, bias neutral, **VIX 18.85**, breadth healthy (75% > EMA20, 100% > EMA50). SPY/QQQ **range** (5d −2.6% / −3.2%), IWM/DIA uptrend. Leading sectors: **semis (SMH RS +7.1%), healthcare (XLV +5.6%), tech (XLK +4.2%)**; weakest: communications (XLC −3.4%). Risk-on backdrop into open (Dow +1.86% Thu, futures higher, SpaceX debut). Book structurally weak (A-tier 0/8 wins PF 0.0; C-tier −23R PF 0.62; B-tier WR 30%).

### Market Mood / Risk Routing      (REQUIRED — PART 4)
- **Crypto mood:**           **risk-on (improving)** — BTC reclaimed $63.5K, +3.4% on Iran "war ended"; but leaders extended + ETH still < $1,700 + macro fragile
- **Stocks mood:**           **pre-market → risk-on lean into the 16:30 EEST open** (chop regime, healthy breadth, gap-up backdrop)
- **Dominant narrative:**    macro risk-on (Iran "war ended", fragile) + SpaceX IPO debut; crypto `momentum_breakout` (TRUMP) / BlackRock yield-bearing BTC ETF (forward)
- **Preferred side now:**    **longs / wait-for-trigger** — long-side bias into a risk-on open, but **require RTH confirmation**; no chasing the gap
- **Best long candidate:**   **JPM** (clean, no legal, desk-A 80.98) — actionable AFTER the open w/ RTH confirm. Crypto: **none clean — RS-leader pullback** (all extended now)
- **Best short candidate:**  **none clean — NFLX** short-watch only on RTH rejection (weakest sector, but fighting the risk-on tape)
- **Best catalyst-backed candidate:** **AMD** (Citi GPU upgrade + semis leadership; extended → pullback) · **LLY** (FDA EBGLYSS + orforglipron trials)
- **What to avoid:**         chasing the gap-up at the open; **UNH long (DOJ probe)**; SMCI (legal); extended crypto leaders (STG/XPL/LUMIA); fresh shorts into risk-on
- **What would change the view:** BTC loses $63.5K (→ fade risk-on) · gap reverses / open breadth fails first 30 min (→ caution) · UMich sentiment miss or Iran re-escalation (→ risk-off snap-back)

## 7. Candidate Deep Dives        (≤ 5)

### 1. JPM (stock) — long, desk-A 80.98 (demoted→C/B pre-market), B/C triggered — **BEST LONG**
- **LEGAL/HEADLINE RISK: none found.** 15 Buy / 9 Hold / 0 Sell this month; avg PT $336.58 (+8.5% upside); earnings **July 14** (no near-term event risk); deploying AI agents across banking/dealmaking; flagged as a **beneficiary of the SpaceX + mega-IPO underwriting wave** (§13). Financials (XLF) mid-pack but improving.
- **Price already reacted?** Carry-forward from Thursday's +1.86% Dow day; will likely gap up. **Chasing?** Buying the pre-market gap = chase; wait for the open. **Retest structure?** Needs RTH confirmation (hold above the entry band first 15–30 min). **Overextended?** Not egregiously (bank, not a parabolic). **Entry now late?** Pre-market yes; on a confirmed RTH hold, no. **Actionable level:** held entry band post-open with the broad tape green.
- **Mood-aligned?** Yes — long into a risk-on open. **Side:** long, **actionable after RTH confirmation.** **Invalidates:** loss of entry band / gap fully reverses in first 30 min. **Chase-risk:** moderate (gap). **Catalyst:** clean fundamentals + IPO-wave tailwind; no contradiction.

### 2. AMD (stock) — long, B 79.94 (demoted→C pre-market), B triggered — **CATALYST LONG-WATCH (EXTENDED)**
- **LEGAL/HEADLINE RISK: none found.** **Citi upgrade on GPU potential** (Seeking Alpha, §13); semis (**SMH RS +7%**) the strongest sector — strong tailwind. **But +300%/12mo, ~$491** → extended, chase-risk.
- **Price already reacted?** Heavily (+300%/yr) and to the upgrade. **Chasing?** Buying the gap is a chase given the run. **Retest?** Prefer a pullback or a clean RTH base. **Overextended?** Likely yes on HTF. **Entry now late?** At the gap, yes; on a pullback/confirmed continuation, no. **Actionable level:** RTH pullback that holds + sector confirmation.
- **Mood-aligned?** Yes (risk-on + semis leadership). **Side:** long-watch. **Invalidates:** loss of the RTH base / semis rolling over. **Chase-risk:** **high** (extended). **Catalyst:** Citi upgrade verified; positive, no contradiction.

### 3. LLY (stock) — long, B 66.62 (demoted→C pre-market), B triggered — **CATALYST LONG-WATCH**
- **LEGAL/HEADLINE RISK: none found.** **FDA approval EBGLYSS** (every-8-week maintenance dosing) + **orforglipron** (oral GLP-1) superior A1C/weight-loss in 3 pivotal type-2 diabetes trials (§13). Healthcare (**XLV RS +5.6%**) a strong sector.
- **Price already reacted?** Likely partially priced (positive drug news flow). **Chasing?** Watch for a clean RTH entry rather than the gap. **Retest?** Prefer post-open confirmation. **Overextended?** Less so than AMD. **Entry now late?** Pre-market yes; RTH confirm no. **Actionable level:** held RTH entry band, sector green.
- **Mood-aligned?** Yes. **Side:** long-watch. **Invalidates:** RTH entry-band failure. **Chase-risk:** moderate. **Catalyst:** FDA/trial wins verified; supportive.

### 4. NFLX (stock) — short, B ~66, triggered — **SHORT-WATCH / NEEDS RTH REJECTION**
- **LEGAL/HEADLINE RISK: none found.** Communications (**XLC**) is the **weakest sector** (RS −3.4%) → short is sector-aligned. **But the broad tape is risk-on into the open** — fading a gap-up is low-quality.
- **Price reacted?** Carry-forward Thursday. **Chasing?** Shorting into a green open = adverse. **Actionable?** **No until an RTH rejection** — failure to reclaim the entry band in the first 15–30 min with the tape rolling over. **Side:** short-watch. **Invalidates:** reclaim of entry band on the open / broad tape stays bid. **Chase-risk:** moderate-high (counter-trend). **Catalyst:** none; sector-weakness only.

### 5. UNH (stock) — C long active (triggered) — **LEGAL-FLAGGED → AVOID**
- **LEGAL/HEADLINE RISK: VERIFIED.** **DOJ antitrust/fraud probe; shares −16%** (QuiverQuant / Yahoo Finance, catalyst importance 0.73, §5/§13). UNH appears as an **active C-tier long** in `active-signals` — a long into a fresh DOJ-probe selloff is exactly the contradiction-risk this slot must catch.
- **Price reacted?** Yes (−16% on the probe). **Verdict per §I:** **AVOID** as a clean long — legal overhang + sharp selloff = no clean long-actionable; if anything it is a weak-side name, not a buy. **Side:** avoid (long). **Invalidates (the avoid):** only a full legal resolution. **Catalyst:** legal_risk verified (single_source DOJ-probe reporting).

## 8. Best Candidates Ranked

No clean *fresh-entry* candidate **before** the open (everything needs the 16:30 RTH confirmation; crypto A/B all realized or extended). Per PART 9, the routed list:

1. **Best long — JPM (stock).** Trigger: **after the 16:30 EEST open, a held RTH entry band (first 15–30 min) with the broad tape green.** Cleanest book name (no legal, A-grade desk score, IPO-wave tailwind). Do NOT buy the pre-market gap.
2. **Best long-watch (catalyst) — AMD + LLY (stocks).** AMD trigger: RTH pullback that holds + semis confirmation (extended → no gap-chase). LLY trigger: held RTH entry band, healthcare green. Crypto long-watch: **a pullback in an RS-leader** (STG/XPL/LUMIA all extended now — wait_pullback, no clean entry; re-engage only on a held pullback + volume).
3. **Best short-watch — NFLX (stock).** Trigger: **RTH rejection** — failure to reclaim the entry band first 15–30 min with the broad tape rolling over (weakest-sector aligned, but counter to the risk-on open). Crypto short-watch: **none clean** — laggards (BANANAS31/HOME/HMSTR) are thin/squeeze-prone; only a failed bounce with BTC losing $63.5K.
4. **Best catalyst-watch (forward) — BlackRock yield-bearing BTC ETF** ("launch next week," The Block) and the **SpaceX IPO debut** reaction as a sentiment tell for the broad tape.

## 9. Avoid / No Trade  (this decision window only — never "stop system")

- **Chasing the gap-up at the open** — both for stocks (pre-market levels stale) and crypto (BTC already +3.4%). Wait for RTH confirmation / pullbacks.
- **UNH long** — active C long into a **fresh DOJ antitrust/fraud probe (−16%)**; AVOID the long.
- **SMCI** — export-control indictment overhang (legal_risk 0.77); not a clean actionable either side.
- **Chasing extended crypto leaders** — STG (+160%/7d, funding −0.011 crowded shorts), XPL (+37%), LUMIA/PYTH/ENSO; `momentum_breakout` = wait_pullback.
- **Fresh shorts into the risk-on tape** — NFLX/PLTR/META short-watches need an RTH rejection, not a green-open chase.
- **ETH longs < $1,700** — relative laggard; only a clean break+hold flips it.

## 10. Main Risks

- **Gap / stale-data risk (slot-specific):** internal reports predate the overnight risk-on push; entry/level numbers may be stale into a gap-up open. RTH-confirm everything.
- **Macro fragility:** the "Iran war ended" driver is **Trump-claimed and repeatedly unfulfilled** (web flags skepticism); a re-escalation headline snaps the tape risk-off and spikes oil.
- **BTC at the pivot:** holding > $63.5K sustains risk-on; losing it back flips the read; ETH still capped < $1,700.
- **Narrow / leader-led crypto breadth (EMA50 37.5%)** — leader-led rallies are fragile; a BTC flush unwinds STG/XPL/LUMIA fast.
- **Stock book structurally weak** — A-tier 0/8 wins (PF 0.0, −6R), C-tier −23R (PF 0.62), B-tier WR 30%. Treat stock signals low-confidence; RTH-confirm.
- **Catalyst mapping 77.0% unmapped** — narrative layer is context only.
- **Today's data:** UMich June prelim consumer sentiment — a miss could fade the open.
- **Ingest:** sources JSON written to `data/raw/enriched_review_sources/2026-06-12T1624.json`; ingest attempted (see §13).

## 11. Action Plan — next 4 hours

1. **At/after the 16:30 EEST RTH open (do NOT act pre-market):** watch **JPM** for a held RTH entry band (first 15–30 min) with the broad tape green — the cleanest long. Watch **AMD** (pullback, not gap-chase; semis leadership) and **LLY** (FDA/trial-backed) as catalyst long-watches.
2. **Short side:** only **NFLX** on an RTH rejection (weakest sector); no fresh shorts into a green open. **Avoid UNH long (DOJ probe)** and SMCI.
3. **Crypto:** BTC holding > **$63.5K** sustains the risk-on read → RS-leader **pullbacks** become longs (none clean now — all extended; wait_pullback). **BTC < $63.5K** → fade; ETH > $1,700 break+hold = broad risk-on confirmation; ETH < $1,700 = no longs. No chasing STG/XPL/LUMIA.
4. **Forward catalysts:** SpaceX IPO debut reaction (sentiment tell); BlackRock yield-bearing BTC ETF ("launch next week"); any Iran re-escalation headline; UMich sentiment print.
5. **System:** scanning/tracking continue in all moods. No stop. Re-check at the 18:30 US-open-reaction slot.

## 12. Final Verdict per Mode

- **Crypto scalp:** **low-confidence** (report header PF 0.14, TP1/horizon mismatch). RS-leader longs **on pullback only**; all leaders extended now → no clean fresh entry. Active for data collection.
- **Crypto intraday:** no-catalyst momentum net-negative in chop (14d WR 23% / PF 0.70 / −3R). Require **RS-leader + pullback/breakout confirmation**. Watch-only; risk-on tilt favours longs on a held pullback if BTC holds $63.5K.
- **Crypto swing:** report **stale (~23h)** → planning only, **no fresh swing verdict**.
- **Stocks intraday:** **pre-market → opening.** Fresh run A/B=0 (closed-market demotion), but desk scored JPM-A / AMD-B / LLY-B / SMH-B longs + NFLX-B short, now triggered. **All require RTH confirmation after 16:30 EEST** — risk-on lean favours longs (JPM best, AMD/LLY catalyst-backed); shorts only on rejection; **avoid UNH (legal).** Book weak — low confidence.
- **Stocks swing/invest:** **stale (~23h)** → planning only, no fresh verdict.

## 13. Sources

- [Yahoo Finance — Bitcoin & Ethereum prices today June 12 2026: BTC $63,718 (+3.4%), ETH $1,671.71 (+3.2%); rally after Trump claims Iran war ended (skepticism noted)](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-june-12-2026-prices-rebound-this-morning-after-trump-claims-war-has-ended-115949042.html) — single_source — **WebFetch opened & verified** — confirms live crypto price band + macro driver.
- [CoinGabbar — Crypto market June 12 2026: cap $2.25T (+1.7%), vol $79.33B, BTC dominance 56.3%](https://www.coingabbar.com/en/crypto-currency-news/crypto-market-update-june-12-2026-bitcoin-btc-price-defi-rise) — single_source — corroborates risk-on crypto tape.
- [TheStreet — Stock market today June 12 2026: Dow futures edge higher on possible Iran deal + SpaceX debut; Dow +1.86% Thu; SpaceX $135/share ~$1.78T; UMich sentiment today; FOMC June 16-17](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-12-2026) — single_source (HTTP 403 → search-snippet only) — premarket/equities + data calendar.
- [TipRanks — JPM forecast: 15 Buy / 9 Hold / 0 Sell, avg PT $336.58 (+8.5%)](https://www.tipranks.com/stocks/jpm/forecast) — single_source — JPM ratings, no legal risk.
- [Robinhood — AMD ~$491.62, +300%/12mo; Citi upgrade on GPU potential](https://robinhood.com/us/en/stocks/AMD/) — single_source — AMD price/upgrade, no legal risk.
- [Yahoo Finance — Eli Lilly (LLY) news: FDA EBGLYSS approval + orforglipron pivotal-trial wins](https://finance.yahoo.com/quote/LLY/news/) — single_source — LLY catalysts, no legal risk.

_No fabricated TradingView/chart observations (chart MCP not loaded — local OHLCV/ATR/EMA only). No uncited stats or legal claims. test_source/fixture URLs filtered. External web research AVAILABLE this run._

## 14. Fix Requests / TODO

### TODO-catalyst-mapper
- **issue:** Catalyst symbol-mapping persistently weak — **77.0% unmapped** this run (1728/2244 events null-symbol); same pattern every run (78.1% at 11:39).
- **evidence:** `data/catalysts/2026-06-12/catalyst_events.jsonl` — `symbol==''` for 1728 of 2244 rows.
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (ticker/entity extraction from headline + source); add a mapping-coverage gate/alert.
- **priority:** medium
- **first observed:** recurring; logged again 2026-06-12 16:24 EEST

### TODO-stocks-A-tier-zero-wins
- **issue:** Stock **A-tier 0/8 wins, PF 0.000, Total R −6.00** (week); A-tier on stocks is net-losing with zero winners — yet the fresh run again scored an A-tier long (JPM 80.98).
- **evidence:** `signal-stats --asset-class stocks` → "A-tier: n=8 | Total R: -6.00 | PF: 0.000 | Winrate: 0.0%".
- **suggested manual fix:** audit stock A-tier promotion criteria; consider gating A-tier on stocks until the sample turns or thresholds tighten.
- **priority:** high
- **first observed:** recurring; logged again 2026-06-12 16:24 EEST

### TODO-stocks-C-tier-losing-book
- **issue:** Stock **C-tier −23R, PF 0.62, WR 9.8%** (n=301) — large losing research book; all-tier diagnostic −22R.
- **evidence:** `signal-stats --asset-class stocks` observations: "tier=C: triggered winrate 10% is low … profit factor 0.62 below 0.8".
- **suggested manual fix:** tighten C-tier stock entry filters or treat C-tier stocks as research-only; review `stocks_intraday_rth_momentum` entries.
- **priority:** medium
- **first observed:** recurring; logged again 2026-06-12 16:24 EEST

### TODO-scalp-horizon-mismatch
- **issue:** Crypto scalp playbook flags a structural TP1/horizon mismatch (TP1 ~1.86R vs typical captured MFE 0.54R; PF 0.14) — entry edge exists but capture is capped.
- **evidence:** `data/reports/scalp/2026-06-12_11-31_scalp_report.md` header + per-idea "Known failure mode".
- **suggested manual fix:** consider a closer TP1 / partial-take rule for scalp, or re-audit at 20 closed A/B scalp signals as noted.
- **priority:** low
- **first observed:** recurring; logged again 2026-06-12 16:24 EEST

### TODO-kol-placeholder
- **issue:** KOL/crowd watchlist still contains the placeholder account; X/Telegram/Discord crowd context not live (social attention = "no symbol-level hits"); Reddit social sources 403-blocked.
- **evidence:** scalp/intraday §4 "KOL watchlist still contains the placeholder account"; cycle log "Failed social source Reddit … 403".
- **suggested manual fix:** replace placeholder KOL accounts with trusted curated sources; audit Reddit social-source fetch (403 Blocked).
- **priority:** low
- **first observed:** recurring; logged again 2026-06-12 16:24 EEST
