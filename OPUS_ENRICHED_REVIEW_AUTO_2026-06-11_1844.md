# Opus Enriched Review — US open reaction review — Auto Cycle 18:44 EEST

_Slot: 18:30 US open reaction review · Thursday 2026-06-11 · ~11:44 ET, ~2h into the US cash session. Focus: how the open actually resolved vs the 16:24 pre-open read, which pre-open ideas confirmed or failed, fake moves / gap traps, breadth broad vs narrow, whether A-tier is trustworthy, crypto reaction to US flows. Prefer retest over chase. Advisory-only, read-mostly — no auto-trade, no code edits._

## 1. Executive Summary

**The pre-open call resolved in favor of caution: the green-futures gap held into a RELIEF BOUNCE, not the red continuation the carried shorts wanted.** Live US tape is modestly green at midday — S&P +0.40%, Dow +0.69%, Nasdaq +0.61% (web-confirmed, §13) — a rebound off June 10's CPI-driven flush (Nasdaq −1.98%, S&P 7,266.99, CPI 4.2% = 3-year high). The desk's stock regime label is still **`risk_off`** (VIX **21.70**, breadth **25% > EMA20**, 0/4 indices trending up), but that label is **lagging** — computed off recent closes/elevated vol, while today's intraday tape is a bounce. Net: shorting mega-cap tech *now* is fighting the tape. The carried MSFT/PLTR shorts that show `tp2_hit`/`tp1_hit` **already banked their gains in yesterday's flush** (they expire today 19:48) — they are realized, not fresh entries. The *fresh* B-tier short signals (MSFT 74.2, GOOGL 71, META 71, TSLA 70.6, NFLX 66.8, all `waiting_for_entry`) need the bounce to **FAIL first** (RTH/failed-retest confirmation) before they are clean. **MSFT and TSLA shorts are additionally contradicted by bullish news** (MSFT: Copilot seats "well above" Wall Street outlook + "Best Tech Stocks"; TSLA: Oppenheimer lifted estimates on stronger demand) → AVOID as clean shorts. **GOOGL/META carry no bullish contradiction** and sit in the weakest sector (communications, RS −3.22%) → cleanest short-watch on a failed bounce.

**Crypto = beaten-down chop with a risk-off undertone.** Desk regime range/chop (BTC range, ETH range, alt breadth 41.3% > EMA20 / 23.9% > EMA50 — narrow). Macro overhang is heavy: **record spot-BTC-ETF outflows (~$3.4B single week, IBIT's worst week ever ~$980M; ETH ETFs ~−$712M/3wk)**, BTC slipped below $72K (intraday low ~$65,710 on Jun 3) — web-confirmed, §13. The live B-tier crypto signals are **all longs**, and most (CHIP tp2, BANK/ALLO/BABY tp1) **already moved** — managed/closing, not fresh. The one fresh momentum name, **ID/USDT +34.6% 24h**, is a *pure momentum cluster with NO confirmed news catalyst* (basket playbook = `wait_pullback`) → chase risk; long-watch only on a pullback that *holds* its 0.0341–0.0356 entry zone, never at the highs.

**Best actionable now = none clean; route by side (this decision window only):**
- **Best short-watch:** **META** (or GOOGL) intraday short — **RTH failed-retest only**. META entry 560.81–563.86 / inval 569.97 / weakest-sector tailwind. Valid only if the bounce fails and the tape rolls red (SPX red, VIX > ~23). Do **NOT** short into the green relief tape.
- **Best long-watch:** none clean. Crypto **CRV/USDT** (RS-leader B-swing, entry 0.2443–0.2481) on a *held* pullback with BTC stable; **ID/USDT** only on a pullback to 0.0341–0.0356 that holds — not at +34.6% highs.
- **Best catalyst-backed:** none long-actionable. TSLA carries the strongest *bullish* catalyst (Oppenheimer) but our signal is a *short* → that makes it an **AVOID short**, catalyst-watch only.
- **What to avoid:** shorting **MSFT / TSLA** into a green tape + bullish news; chasing **ID/USDT** at +34.6%; treating the **tp-hit crypto longs** (CHIP/BANK/ALLO/BABY) as fresh; pre-positioning against the **Iran "tonight" / Kharg Island** tail (Trump pushing for stronger strikes; Pentagon hazmat lockdown headline today).

**System health:** untracked-alert detector **clean (0)**; scheduler **fresh** (~1h17m). Realized stats keep stocks the weaker book (tier-C PF **0.73**, winrate 10%, −9R) vs crypto (tier-B PF **1.94**, +17R but triggered winrate 26%). Catalyst mapping **weak again — 79.3% unmapped** → catalyst layer is context, not a decision input. §14 TODO persists.

## 2. Data Used

- Crypto **scalp** — `data/reports/scalp/2026-06-11_13-53_scalp_report.md` (mtime 16:53, data 13:45Z) — **fresh** (~1.9h).
- Crypto **intraday** — `data/reports/intraday/2026-06-11_14-01_intraday_report.md` (mtime 17:01, data 13:45Z) — **fresh** (~1.7h).
- Crypto **swing** — `data/reports/swing/2026-06-11_14-18_swing_report.md` (mtime 17:18) — **fresh** (~1.4h).
- **Stocks intraday** — `data/reports/stocks/intraday/2026-06-11_15-38_stocks_intraday_report.md` (mtime 18:38, data 15:38 UTC) — **very fresh** (~7m).
- **Stocks swing/invest** — `..._14-23_` / `..._14-27_` (mtime 17:23 / 17:27) — **fresh** (~1.3h), planning context.
- Catalysts — `data/catalysts/2026-06-11/` (events.jsonl + narrative_baskets.jsonl + `catalyst_cycle_14-01.md`, mtime 17:01) — **fresh** (~1.7h). `catalyst-scan` NOT re-run (dir present).
- LLM packets — `data/processed/llm_analysis_packet.md` (17:18), `llm_stocks_packet.md` (17:27).
- DB (read-only) — `db/crypto_ai_desk.sqlite` (1.1GB, mtime 18:43, live): `news_items` (RSS + t.me), `proposed_signals`, integrity tables. _(Note: `data/crypto_ai*.db` are 0-byte stubs; the live DB is `db/crypto_ai_desk.sqlite`.)_
- CLI: `active-signals` crypto (7) + stocks (50); `signal-stats` crypto + stocks; `detect_untracked_legacy_alerts --since 2026-06-11` (**clean — 0 untracked**).
- External: WebSearch ×2 (US market June 11; BTC/ETF June 11) — **loaded & used, cited §13**. WebFetch ×3 attempts (TheStreet, bitcoinfoundation, earlier session) — **all HTTP 403 (anti-bot)**. External research is **AVAILABLE** (WebSearch returned usable cited content); only the fetch-*open* step is blocked — noted, NOT declared "unavailable."

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **17:28** (~1h17m ago) — **fresh**. Latest cycle summary `cycle_03_16-43_summary.md` mtime **17:28** (~1h17m) — **fresh**. Both well inside the 3h defer threshold → **review proceeds normally**. `daily_2026-06-11_window2.done` present (window 2 closed). Crypto monitor log live (18:38).
- All six reports + catalysts are **fresh** (~7m–1.9h) — no carry-forward/stale flags this run (improvement vs 16:24, where swing/invest were ~11h carry-forward).
- **Stale-label risk:** the stock intraday regime (`risk_off`, VIX 21.70) is computed off recent closes; the *live* tape is a green bounce. Treat the desk label as lagging — RTH price action overrides it. The `tp2_hit`/`tp1_hit` on MSFT/PLTR are **realized from yesterday's flush**, not signals to re-enter now.

## 4. What Changed vs Previous Review

Prior: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-11_1624.md` (pre-US-open decision review, 16:24 EEST).

- **The open resolved → relief bounce, gap held.** 16:24 flagged "knife-edge: green futures over a risk_off desk; require RTH confirmation; do NOT pre-position the gap." Outcome: the gap **held into a green session** (S&P +0.40% / Nasdaq +0.61% midday). The "require confirmation, don't chase the gap" routing was correct — entering shorts pre-open would have been fighting the bounce.
- **Carried shorts realized, not re-entry candidates.** MSFT (75.2) → `tp2_hit`; PLTR (68.9) → `tp1_hit`; these banked in the June 10 flush and expire 19:48 today. **New fresh B shorts appeared** from today's intraday scan (MSFT 74.2, GOOGL 71, META 71, TSLA 70.6, NFLX 66.8 — all `waiting_for_entry`) — these now fight the bounce.
- **TSLA short still contradicted (carried AVOID).** 16:24 upgraded TSLA short to AVOID on bullish Oppenheimer/FSD catalysts; still valid + new Iran-threat-to-Musk headline adds two-sided risk.
- **MSFT short newly contradicted.** New bullish MSFT news today (Copilot seats "well above" Wall St outlook; "Best Tech Stocks Right Now") → MSFT short downgraded from "clean retest short" to **AVOID clean / failed-retest only**. GOOGL/META inherit the "cleanest short-watch" slot.
- **Crypto unchanged-heavy.** Same beaten-down chop + record ETF outflows. ID/USDT now the top RS mover (+34.6%, score 100) but **no news catalyst** → chase risk. Prior CRV/HMSTR scalps expired; CRV reappears as a B-swing `waiting_for_entry`.
- **Macro leg evolved.** 16:24 had green futures on "swift-resolution hope." Now: Trump **furious strikes "not powerful enough," pushing for stronger impact + Kharg Island**, Iran warns "crushing response," **Pentagon hazmat lockdown** (t.me/WalterBloomberg, today) — geopolitical tail intact; ECB July-hike chatter added.
- **Catalyst mapping** essentially unchanged-weak: 79% → **79.3% unmapped**. TODO persists.
- **Untracked-alert detector:** still **clean (0)** — no regression.

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative jsonl): **2344**.
- Mapped (non-null symbol): **486**.
- Unmapped (null symbol): **1858** → **79.3% unmapped**.
- `narrative_baskets`: **5** (rwa, perps_dex, ai, delisting_thin_liquidity, momentum_breakout).
- **⚠ catalyst mapping weak this run — use the catalyst layer as context, not a final decision input.** (>50% unmapped, persistent across runs.)
- Top 3 unmapped-by-importance headlines (macro / no single symbol — legitimately symbol-less):
  1. `0.73` Raydium responds after $1.34M exploit (AMBCrypto) — sector/no-symbol.
  2. `0.73` UK surveillance laws face US scrutiny over Apple backdoor demand — macro/no-symbol.
  3. BTC ETF outflows / Binance TradFi-perp listing (basket-level, mapped to (basket) not a single coin).
- Mapped top catalysts: BTC ETF-flow/BlackRock income-ETF cluster (regulatory_sector_headline, imp 0.69–0.78), SMCI export-control indictment (legal_risk 0.77, **stale — filed Mar 1**), UNH DOJ probe (legal_risk 0.73, −16%), Raydium $1.34M exploit (0.71), Binance USDⓈ TradFi perps listing (primary_source 0.65).

## 6. Market Landscape

Live tape (web, §13): **S&P +0.40%, Dow +0.69%, Nasdaq +0.61%** midday — relief bounce off June 10's flush (Nasdaq −1.98%, CPI 4.2% 3-yr high). Oil **up** on Iran ground-invasion fears (Trump → Kharg Island seizure / "total control" of energy sector). VIX **21.70** (elevated). Sector RS: **healthcare (XLV +6.91%), semis (SMH +5.06%), financials (XLF +4.31%)** lead; **communications (XLC −3.22%), consumer-discretionary (XLY −1.96%), materials (XLB −1.44%)** lag. Crypto: BTC/ETH range, record ETF outflows, BTC sub-$72K.

### Market Mood / Risk Routing  (REQUIRED)
- **Crypto mood:** **chop / risk-off undertone** — range regime but record ETF outflows + BTC beaten down; relief bounces are sellable, not trend longs.
- **Stocks mood:** **mixed / fragile-bounce-over-risk-off** — live tape green (+0.4–0.6%) but desk label `risk_off`, VIX 21.70, breadth narrow (25% > EMA20), geopolitical tail open.
- **Dominant narrative:** Iran-war escalation + hot inflation (CPI 4.2%) capping risk; one-day relief bounce after the June 10 flush; crypto institutional-outflow exodus.
- **Preferred side now:** **wait-for-trigger.** Stocks: shorts only on a *failed retest* (RTH confirmation). Crypto: RS-leader longs only on a *held* pullback. No clean fresh entry into the bounce.
- **Best long candidate:** none clean — crypto **CRV/USDT** (RS-leader) or **ID/USDT** only on a pullback that holds entry; trigger below.
- **Best short candidate:** **META** (or GOOGL) — failed bounce retest into weakest sector; trigger: tape rolls red + reject of entry band.
- **Best catalyst-backed candidate:** none long-actionable (TSLA's bullish catalyst opposes our short → AVOID, not a long).
- **What to avoid:** shorting MSFT/TSLA (bullish news + green tape); chasing ID +34.6%; treating tp-hit crypto longs as fresh; pre-positioning the Iran tail.
- **What would change the view:** SPX rolling red with VIX > ~23 and indices breaking lower → confirms the mega-cap shorts (META/GOOGL/MSFT). A clean Iran **de-escalation** headline + oil reversal → flips to risk-on, favors RS-leader crypto longs and kills the short thesis.

## 7. Candidate Deep Dives  (5 — overflow listed at end of section)

### 1) MSFT — stocks, B intraday SHORT (sc 74.2 waiting / 75.2 tp2_hit / 67 swing) — **AVOID clean short, failed-retest only**
- Entry 388.13–389.91 / inval 393.47 / a 398.13 leg already `tp2_hit` (realized in June 10 flush, expires 19:48).
- **CONTRADICTION (catalyst vs technical):** fresh bullish MSFT news today — "Microsoft Copilot seats could be 'well above' Wall Street's outlook" (Seeking Alpha, 14:07) + "Best Tech Stocks Right Now" (Benzinga, 11:19). Shorting a mega-cap with a positive AI-monetization headline **into a green tape** is fighting both catalyst and price.
- Price-reaction/chase: yes — the profitable short leg already played out yesterday; re-entering now at the retest is late unless the bounce fails. Not overextended on the short side, but no fresh edge.
- Mood-aligned? Partially (desk risk_off) but NOT vs the live bounce. Actionable only after RTH failure (price rejects ~389–393 and rolls). Invalidation: 393.47 / a hold above ~393 with the Copilot bid → thesis dead.
- **Verdict: AVOID as a clean short; short-watch only on a confirmed failed retest.**

### 2) TSLA — stocks, B intraday SHORT (sc 70.6 waiting / 65.5 triggered) — **AVOID short / MANUAL REVIEW**
- Entry 388.13–391.34 / inval 397.77.
- **CONTRADICTION (two-sided):** Oppenheimer **lifted estimates on stronger demand** (t.me/WalterBloomberg, 12:18 — bullish) vs Iran **threatens Musk's companies in the Middle East** (CNBC, 13:37 — bearish headline) + SpaceX IPO "referendum on Musk" (neutral). Net = two-sided, not a clean short.
- Chase/overextension: the bullish analyst note caps downside; shorting into it + a green tape = poor R:R.
- Mood-aligned? No clean alignment. Actionable: neither side clean — manual review. Invalidation of short: 397.77 / any continuation of the Oppenheimer-driven bid.
- **Verdict: AVOID short (carried from 16:24); catalyst-watch only. No long signal exists, so not a long either.**

### 3) META — stocks, B intraday SHORT (sc 71.0 waiting) — **BEST short-watch (failed-retest only)**
- Entry 560.81–563.86 / inval 569.97.
- **No bullish contradiction surfaced** (DB: no fresh META news last 14h). Sits in the **weakest sector (communications XLC, RS −3.22%)** → cleanest risk-off-aligned short of the mega-cap set.
- Price-reaction: has NOT yet triggered (`waiting_for_entry`); not chasing a completed move. But the live tape is green → entering now shorts into strength.
- Mood-aligned? Yes vs desk risk_off + weak sector, but requires the bounce to fail. Actionable **only after** a failed retest of the 560.81–563.86 band with the tape rolling red. Invalidation: 569.97 / index bounce broadening.
- **Verdict: short-watch — best of the mega-cap shorts; trigger = failed retest + red tape. Do NOT short into the green bounce.**

### 4) GOOGL — stocks, B intraday SHORT (sc 71.0 waiting) — **short-watch (failed-retest only)**
- Entry 347.83–350.10 / inval 354.64.
- No fresh bullish contradiction surfaced (DB clean last 14h). Communications-adjacent / mega-cap; mirrors META.
- Same routing as META: actionable only on a failed retest + red tape. Invalidation 354.64.
- **Verdict: short-watch alongside META; secondary to META (META has the weaker-sector tailwind).**

### 5) ID/USDT — crypto, B intraday LONG (sc 65.3 waiting / scalp leg EXPIRED 15:53) — **long-watch on held pullback only**
- Entry 0.034115–0.035559 / inval 0.032351 (intraday leg expires tomorrow 14:01; the scalp leg already expired).
- **CONTRADICTION (momentum vs no-catalyst):** ID is the #1 RS mover (+34.57% 24h, RS vs BTC +33%, vol 3.1x, score 100) but the `momentum_breakout` basket flags it as a **pure-momentum cluster with NO confirmed news catalyst** (playbook `wait_pullback`). DB shows no ID-specific news in 24h.
- Price-reaction/chase: **yes, heavily** — +34.6% is overextended; entry now = chasing the top. The entry band (0.0341–0.0356) sits *below* the spike, i.e. it requires a pullback that holds.
- Mood-aligned? Crypto is chop/risk-off → a no-news +34% spike is exactly the kind of move to fade, not chase. Actionable **only** if it pulls back into 0.0341–0.0356 and holds with BTC stable. Invalidation 0.0323.
- **Verdict: long-watch on a held pullback only; do NOT chase. No catalyst = low conviction.**

**Overflow (qualified but beyond the 5-cap):**
- **CRV/USDT** (crypto B-swing long, sc 65.1, `waiting_for_entry` 0.2443–0.2481) — RS-leader long-watch on held pullback; cleaner structure than ID but lower momentum. Reason cut: similar routing to ID, ranked behind.
- **NFLX** (stocks B intraday short, sc 66.8) — risk-off-aligned short but lowest-tier of the set; same failed-retest routing as META/GOOGL.
- **CHIP / BANK / ALLO / BABY** (crypto B-swing longs, tp1/tp2_hit) — already moved, managed/closing, not fresh entries. Reason cut: realized, no fresh edge.

## 8. Best Candidates Ranked

No clean fresh entry this window — routed by side (per anti-over-conservatism rule):
1. **short-watch — META/USDT… (META stock)** — failed retest of 560.81–563.86 + tape rolls red → short toward inval 569.97. Best mega-cap short (weakest sector, no bullish news).
2. **short-watch — GOOGL** — failed retest of 347.83–350.10 + red tape; inval 354.64.
3. **long-watch — CRV/USDT** — held pullback into 0.2443–0.2481 with BTC stable → RS-leader long; inval 0.2396.
4. **long-watch — ID/USDT** — held pullback into 0.0341–0.0356 (do NOT chase +34.6%); inval 0.0323. Low conviction (no catalyst).
5. **catalyst-watch — TSLA** — only if a *long* setup ever forms on the Oppenheimer demand thesis; current signal is a short → AVOID short.

## 9. Avoid / No Trade  (this decision window only)

- **MSFT short** into a green tape + bullish Copilot/Best-Tech news → AVOID clean; failed-retest only.
- **TSLA short** — two-sided (Oppenheimer bullish vs Iran-threat headline) → AVOID / manual review.
- **ID/USDT chase** at +34.6% with no catalyst → do not chase; pullback-hold only.
- **tp-hit crypto longs** (CHIP/BANK/ALLO/BABY) → already moved, not fresh.
- **Pre-positioning the Iran tail** (Trump pushing stronger strikes / Kharg Island; Pentagon hazmat lockdown) → headline-driven gap risk both ways.
- _Scanning, candidate generation, tracking, and monitors continue as normal — this is a current-window caution, NOT a system stop._

## 10. Main Risks

- **Regime-label lag:** desk `risk_off` (VIX 21.70) vs live green tape → shorting the label instead of the tape is the primary trap this window. RTH price overrides the label.
- **Geopolitical gap tail:** Iran escalation (Kharg Island, "crushing response," Pentagon hazmat lockdown today) can gap the tape either direction overnight; oil already rising.
- **Crypto outflow overhang:** record spot-ETF outflows ($3.4B/wk, IBIT worst week ever) → relief bounces are fragile; no-catalyst momentum (ID) prone to sharp reversal.
- **Source-verification:** WebFetch fetch-open is 403-blocked (anti-bot) across all attempts; index/price levels rest on WebSearch summaries + internal reports. Treated as `single_source` where not cross-confirmed.
- **Catalyst mapping 79.3% unmapped** → catalyst layer is context only; do not let it drive a verdict.
- **Sources ingest:** if the ingest CLI errors, logged here and review continues (see §13/§14).

## 11. Action Plan — next 4 hours (into late US session)

1. **Watch META/GOOGL for a failed retest** of their entry bands with the tape rolling red (SPX red, VIX > ~23). Only then are the mega-cap shorts clean. Do NOT short the green bounce.
2. **Do NOT re-enter MSFT/PLTR** — their profitable legs are realized (tp2/tp1) and expire 19:48; let them close.
3. **Hold MSFT/TSLA shorts as AVOID** while the bullish news + green tape persist; re-evaluate only on a confirmed RTH failure.
4. **Crypto:** wait for ID to pull back into 0.0341–0.0356 (hold) or CRV into 0.2443–0.2481 (hold) with BTC stable before any RS-leader long. No chase.
5. **Track the Iran/oil tail** — a de-escalation headline + oil reversal flips the routing risk-on (favor longs, kill shorts); an escalation gap favors the shorts but with whipsaw risk.
6. **Let the scanner run** — C-tier/watchlist generation continues for research; no pause.

## 12. Final Verdict per Mode

- **Crypto scalp:** no clean fresh entry — chop/risk-off; ID scalp leg expired, no-catalyst momentum. Wait-for-trigger.
- **Crypto intraday:** long-watch ID/CRV on held pullbacks only; do not chase. Low conviction.
- **Crypto swing:** tp-hit longs (CHIP/BANK/ALLO/BABY) managed/closing; CRV the only fresh RS-leader watch.
- **Stocks intraday:** short-watch META/GOOGL on failed retest + red tape; AVOID MSFT/TSLA (bullish news). No clean entry into the green bounce.
- **Stocks swing/invest:** planning context only; risk_off label lagging the bounce — defer to RTH confirmation.

## 13. Sources

- [TheStreet — Stock Market Today (June 11, 2026): Nasdaq, S&P 500 rise despite mixed Oracle earnings, Iran strikes](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-11-2026) — 2026-06-11, single_source (WebSearch summary; fetch-open 403). Confirms: S&P/Nasdaq/Dow green midday; Iran-strike driver.
- [Yahoo Finance — Stock market today: Dow, S&P 500, Nasdaq rise after US completes fresh round of Iran strikes](https://finance.yahoo.com/markets/live/stock-market-today-thursday-june-11-dow-sp-500-nasdaq-222511784.html) — 2026-06-11, single_source. Confirms green tape + Iran escalation (Kharg Island, oil up).
- [TheStreet — Stock Market Today (June 10, 2026): Dow dips 900 points as US signals more strikes in Iran](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-10-2026) — 2026-06-10, single_source. Confirms June 10 flush (Dow −953, CPI 4.2%).
- [NBC News — Inflation jumps to 4.2%, the highest since early 2023](https://www.nbcnews.com/business/energy/may-inflation-report-gas-prices-iran-rcna349059) — 2026-06, single_source. Confirms CPI 4.2% (3-yr high).
- [Coinfomania — Bitcoin ETFs Record Largest-Ever $3.4B Sell-Off](https://coinfomania.com/bitcoin-etf-outflows-june-2026-record-selloff/) — 2026-06, single_source. Confirms ~$3.4B weekly BTC-ETF outflow, IBIT ~$980M worst week.
- [bitcoinfoundation.org — Bitcoin ETF Outflows June 2026: $1.67B Weekly](https://bitcoinfoundation.org/news/crypto-etfs-news/crypto-etfs-june/) — 2026-06, single_source (fetch-open 403; WebSearch summary). ETH ETFs ~−$712M/3wk.
- [Bitrue — Why Bitcoin Fell Below $72K in June 2026 Amid ETF Outflows](https://www.bitrue.com/blog/bitcoin-price-june-2026) — 2026-06, single_source. BTC sub-$72K, intraday low ~$65,710 (Jun 3).
- Internal (read-only): `db/crypto_ai_desk.sqlite` `news_items` — TSLA Oppenheimer estimate raise (t.me/WalterBloomberg, 2026-06-11 12:18, primary social), TSLA Iran-threat (CNBC, 13:37), MSFT Copilot-seats (Seeking Alpha, 14:07), MSFT Best-Tech-Stocks (Benzinga, 11:19); t.me/WalterBloomberg macro feed (Iran/Kharg, Pentagon hazmat lockdown, ECB July-hike, 15:02–15:43).
- Internal reports/CLI per §2 (desk regimes, active-signals, signal-stats, untracked-alert detector).

_Verification note: every external claim carries source + date + URL; index/price levels are WebSearch-summary `single_source` (WebFetch fetch-open 403 across all attempts — research AVAILABLE, fetch-open blocked); no fabricated chart/TradingView observations (chart MCP not loaded — local OHLCV/RS/ATR only); SMCI legal flag noted as stale (filed Mar 1); no `test_source` rows; §13 present._

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-unmapped
- **issue:** Catalyst symbol mapping persistently weak — 79.3% of `catalyst_events` unmapped (1858/2344), unchanged across the day's runs (80%→79%→79.3%). Catalyst layer cannot drive decisions.
- **evidence:** `data/catalysts/2026-06-11/catalyst_events.jsonl`; top unmapped = legitimately symbol-less macro headlines (Raydium exploit, Apple-backdoor surveillance) AND basket-level items mapped to "(basket)" instead of a coin.
- **suggested manual fix:** improve the symbol resolver in the catalyst layer — (a) map basket-level events to their primary basket symbols, (b) add a macro/no-symbol class so macro headlines are excluded from the "unmapped" ratio rather than inflating it.
- **priority:** medium
- **first observed:** 2026-06-11 11:39 EEST (carried)

### TODO-stocks-tierC-pf-below-threshold
- **issue:** Stocks tier-C realized profit factor **0.73** (< 0.8 threshold), triggered winrate **10%**, totalR **−9R** (n=297). The stock book's C-tier is a net loser; CLI emits the observation each run.
- **evidence:** `python -m src.cli signal-stats --asset-class stocks` → "(reliable, n=297) tier=C: profit factor 0.73 below 0.8" + "triggered winrate 10% is low."
- **suggested manual fix:** tighten tier-C stock entry/scoring (continuation setup is the only bucket; review entry timing vs RTH confirmation) OR demote tier-C stocks to research-only so they don't dilute the actionable book.
- **priority:** medium
- **first observed:** 2026-06-11 (recurring across slots)

### TODO-crypto-tierB-low-winrate
- **issue:** Crypto tier-B triggered winrate **26%** (CLI flags "low, consider reviewing entries") though R-positive (PF 1.94, +17R) via good R:R. Worth an entry-timing audit; setup=breakdown (PF 1.875, stopR 0.52) lags setup=pullback (PF 2.0).
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` observations + By-setup table.
- **suggested manual fix:** audit crypto B-tier breakdown-setup entries (higher stop-out rate); consider requiring a retest before the breakdown entry arms.
- **priority:** low
- **first observed:** 2026-06-11

### TODO-webfetch-403-antibot
- **issue:** WebFetch fetch-open returns HTTP 403 (anti-bot) on all news/finance domains attempted (TheStreet, bitcoinfoundation, and prior-run CNBC/RFE-RL). External *verification depth* is limited to WebSearch summaries; URLs cannot be opened to extract primary-source figures.
- **evidence:** three 403s this run; consistent with the 16:24 run's three 403s.
- **suggested manual fix:** out of routine scope (no code edits) — a human session could add a fetch fallback (cached reader / allowed-domain proxy) or accept WebSearch-summary as the verification tier and label accordingly.
- **priority:** low
- **first observed:** 2026-06-11 16:24 EEST (carried)
