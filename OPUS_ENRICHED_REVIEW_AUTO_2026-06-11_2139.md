# Opus Enriched Review — late-session risk review — Auto Cycle 21:39 EEST

_Slot: 21:30 late-session risk review · Thursday 2026-06-11 · ~14:39 ET, ~1h20m before the US cash close. Focus: active signals near TP/stop/invalidation, keep-watching vs avoid-new vs wait-for-close, intraday signals too late to enter, crypto evening continuation vs reversal, stale-setup flags, whether no-entry signals are still valid. Advisory-only, read-mostly — no auto-trade, no code edits, paper-trading._

## 1. Executive Summary

**The dominant event this slot is a macro REGIME FLIP on the equity side: Trump cancelled this-evening's Iran strikes and said "all points of a deal are essentially agreed" → a de-escalation risk-ON bounce that has held and extended into the late session** (web-confirmed §13). Indices are green (Nasdaq +0.8%, S&P +0.3%, Dow +0.5–0.66%), **VIX collapsed to 20.02 (−9.88%)**, breadth is broad (57% advancing, **Russell 2000 +1.44%** leading — classic risk-on small-cap participation), and semis are ripping (Intel +10.3%, Arm +7.8%, Applied Materials +7.8%). The desk's stock label is still **`chop`/neutral, VIX 20.14** — that label now *lags* the live de-escalation tape, which is risk-on.

**This invalidates the carried mega-cap-tech SHORT thesis.** The 18:44 review routed META/GOOGL/TSLA/NFLX as "short-watch on a *failed* retest." The retest never failed — the bounce extended on de-escalation, VIX fell, and the fresh 18:28 scan **demoted those shorts from B-tier to C-tier** (GOOGL 51.6, META 52.7, NFLX 54.5; MSTR rejected 46.9). Net: **do not initiate new mega-cap tech shorts into a de-escalation rally.** They are now wrong-side; only a *failed* close back below today's range + VIX back > ~22 would revive them.

**Crypto is DIVERGING — still risk-off.** BTC ~$61,900, ETH ~$1,660 (web-confirmed §13), with **record ETF outflow streaks (BTC 13 days / $4.33B; ETH 17 days, a record)**. Desk regime range/chop, **ETH downtrend**, alt breadth 50% > EMA20 / 33% > EMA50 (narrow). The equity de-escalation did **not** pull crypto up — the institutional bid is absent. So relief pops in the RS-leaders (CRV +22%, ID +31%, FIDA +16%, HEMI +18%) are **sellable strength / wait-pullback, not trend longs**. There are **no A/B-tier crypto setups** this run — everything is C-tier watchlist.

**Late-session timing rule:** at ~14:39 ET the only fresh stock A/B is **JPM long (B, 65.35)** — RS-leader (+5.45% vs SPY) in the strong financials sector and *aligned* with the risk-on tape, but RR-to-TP1 is only **1.0** (weak) and it is **too late to initiate a fresh intraday entry** ~80 min before the close. Carry it as a **tomorrow-RTH** idea, do not chase into the bell.

**Best actionable now = route by side (this decision window only):**
- **Best long-watch:** **JPM** (risk-on aligned, financials strong) — but **wait for tomorrow's RTH**, not a late-session chase; weak 1.0 RR. Crypto **ATOM/USDT** long-watch only on a *held* pullback into 1.925–1.943 (OI-confirmed, RS-leader) — no catalyst, so demand the zone to hold.
- **Best short-watch:** **none clean** — de-escalation killed the mega-cap short. Trigger to revive: tape rolls back red into the close (SPX red) **and** VIX > ~22, on a *failed* retest of today's highs (GOOGL the cleanest, weakest sector).
- **Best catalyst-backed:** **CRV/USDT** — real, web-confirmed Curve DAO rally (+22%/24h, strongest DeFi token in rotation), but **already largely reacted**; manage the existing triggered/tp1 signals, **do not chase fresh at the highs**.
- **What to avoid:** new mega-cap tech shorts into de-escalation; chasing extended crypto RS-leaders (CRV/ID/FIDA) at the highs into a risk-off-crypto tape; the legal/headline-risk names **UNH** (DOJ antitrust probe, −16%) and **SMCI** (export-control indictment).

**System health:** untracked-alert detector **clean (0)** — no PART-1 regression. Scheduler **fresh** (~1h44m). Realized stats keep stocks the weaker book and flag two structural failure modes — **stock A-tier 0% winrate / −6R this week (overpromotion)** and **stock longs PF 0.42 / −25R vs shorts PF 1.45 / +13R**; crypto B-tier healthier (PF 2.0, +18R, swing the best bucket +12R). Catalyst mapping **weak again — 80.0% unmapped** → catalyst layer is context, not a decision input. §14 TODOs persist (catalyst mapper, stock A-tier overpromotion, stock-swing losing bucket).

## 2. Data Used

- Crypto **scalp** — `data/reports/scalp/2026-06-11_16-40_scalp_report.md` (mtime 19:40) — **fresh** (~1.98h).
- Crypto **intraday** — `data/reports/intraday/2026-06-11_16-48_intraday_report.md` (mtime 19:48) — **fresh** (~1.85h).
- Crypto **swing** — `data/reports/swing/2026-06-11_14-18_swing_report.md` (mtime 17:18) — **carry-forward** (~4.4h; flagged §3).
- **Stocks intraday** — `data/reports/stocks/intraday/2026-06-11_18-28_stocks_intraday_report.md` (mtime 21:28, data 18:28 UTC) — **very fresh** (~11m).
- **Stocks swing / invest** — `..._14-23_` / `..._14-27_` (mtime 17:23 / 17:27) — **carry-forward** (~4.3h; planning context, flagged §3).
- Catalysts — `data/catalysts/2026-06-11/` (events.jsonl + narrative_baskets.jsonl + `catalyst_cycle_16-48.md`, mtime 19:48) — **fresh** (~1.85h). `catalyst-scan` NOT re-run (dir present).
- LLM packets — `data/processed/llm_analysis_packet.md` (19:48), `llm_stocks_packet.md` (19:56).
- DB (read-only) — `db/crypto_ai_desk.sqlite` (1.12 GB, mtime 21:38, live): `proposed_signals` (active A/B levels), integrity tables.
- CLI: `active-signals` crypto (10) + stocks (50); `signal-stats` crypto + stocks; `detect_untracked_legacy_alerts --since 2026-06-11` (**clean — 0 untracked**).
- External: WebSearch ×3 (US tape June 11; BTC/ETH + ETF flows June 11; CRV rally) — **loaded, used, cited §13**. External research **AVAILABLE** this run.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **19:56:43** (~1h44m ago) — **fresh**. Latest cycle summary `cycle_04_19-28_summary.md` mtime **19:56:42** (~1h44m) — **fresh**. Both well inside the 3h defer threshold → **review proceeds normally**.
- Crypto scalp/intraday + stocks intraday + catalysts are **fresh** (~11m–1.98h). 
- **Carry-forward flag:** crypto **swing** (~4.4h) and stock **swing/invest** (~4.3h) are in the 4–12h band → usable as planning context, not treated as fresh confirmation. No source is >14h (no hard-stale exclusion needed).
- **Stale-label risk:** the stock intraday regime label (`chop`, VIX 20.14) is computed off recent closes; the *live* tape is a de-escalation risk-on bounce (VIX 20.02 and falling). Treat the desk label as **lagging** — live price/VIX override it.

## 4. What Changed vs Previous Review

Prior: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-11_1844.md` (US open reaction review, 18:44 EEST).

- **MACRO FLIPPED from escalation to de-escalation.** 18:44 carried an Iran *escalation* tail (Trump "strikes not powerful enough," Kharg Island seizure, Pentagon hazmat lockdown). This slot: **Trump cancelled this-evening's strikes, "all points of a deal essentially agreed"** → equities risk-on, VIX 21.70 → **20.02**, breadth 25% → **57% advancing**. This is the single biggest change and it re-routes the whole stock book.
- **Mega-cap tech short thesis INVALIDATED.** 18:44 best short-watch was META/GOOGL "on a failed retest." The retest never failed — bounce extended; fresh scan **demoted GOOGL/META/NFLX from B to C** and MSTR to rejected. Short-watch withdrawn → AVOID new shorts.
- **JPM long is the new fresh A/B (was not present at 18:44).** B-tier 65.35, RS-leader, risk-on-aligned — but weak 1.0 RR and late-session.
- **Crypto unchanged-heavy and now DIVERGING.** Same range/chop + record ETF outflows; BTC drifted $63.2K → **~$61.9K**, ETH confirmed downtrend ~$1.66K. The equity de-escalation did **not** lift crypto — divergence confirmed. ID/CRV/FIDA still the RS movers; CRV's catalyst now web-verified.
- **Carried crypto B-longs largely realized.** CHIP tp2, CRV-scalp/BANK/ALLO/BABY tp1 — managed/closing, **not fresh entries**. ATOM (swing+scalp) still `waiting_for_entry`; ID intraday now `triggered`.
- **Catalyst mapping** still weak: 79.3% → **80.0% unmapped**. TODO persists.
- **Untracked-alert detector** still **clean (0)** — no regression.

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative jsonl): **2844**.
- Mapped (non-null symbol): **569**.
- Unmapped (null symbol): **2275** → **80.0% unmapped**.
- `narrative_baskets`: **5** (rwa_narrative, perps_dex_narrative, ai_narrative, delisting_thin_liquidity, momentum_breakout).
- **⚠ catalyst mapping weak this run — use the catalyst layer as context, not a final decision input.** (>50% unmapped, persistent across every run today.)
- Top unmapped-by-importance headlines (macro / insider / no single symbol — many legitimately symbol-less):
  1. `0.50` "Iran targets US Fifth Fleet in Bahrain with drone strike" — macro/geopolitics, no single ticker.
  2. `0.44` "Schwab (SCHA) vs iShares (IJR): Which Small Cap ETF Should Investors Buy?" — multi-ETF, resolver missed.
  3. `0.43` "ICU Medical's General Counsel Sells…" / "Nayax CMO sells…" / "Digi International VP Trims Stake" — small-cap insider headlines the resolver did not map.
- Mapped catalyst clusters that matter: **CRV** Curve DAO +43%/5d rally (news_mention, imp 0.75); **SOL** Raydium $1.34M exploit (exploit_hack); **AAVE** risk-framework after April $290M exploit; **BTC** BlackRock income-ETF / ETF-outflow cluster (regulatory_sector_headline); **SMCI** export-control indictment (legal_risk 0.77, **stale — filed Mar 1**); **UNH** DOJ antitrust/fraud probe (legal_risk 0.73, −16%).

## 6. Market Landscape

Live tape (web §13): **Nasdaq +0.8% / S&P +0.3% / Dow +0.5–0.66%**, VIX **20.02 (−9.88%)**, breadth **57% advancing**, **Russell 2000 +1.44%** leading. Driver: **Trump cancelled this-evening Iran strikes; "all points of a deal essentially agreed"** → de-escalation. Semis lead (Intel +10.3%, Arm +7.8%, Applied Materials +7.8%); Oracle **−11.9%** on mixed earnings (stock-specific, not tape-wide). Desk sector RS: **healthcare (XLV +6.45%), semis (SMH +5.52%), financials (XLF +4.29%)** lead; **communications (XLC −3.12%), consumer-discretionary (XLY −1.89%), materials (XLB −1.22%)** lag. Crypto: BTC ~$61.9K, ETH ~$1.66K downtrend, record ETF outflow streaks → risk-off undertow intact, decoupled from the equity bounce.

### Market Mood / Risk Routing  (REQUIRED)
- **Crypto mood:** **risk-off / chop** — range regime, ETH downtrend, record BTC/ETH ETF outflows; relief pops are sellable strength, not trend longs.
- **Stocks mood:** **risk-on (de-escalation bounce)** — live tape green, VIX 20 and falling, broad breadth + small-cap leadership; desk `chop` label lags the tape.
- **Dominant narrative:** **Iran de-escalation / deal hope** drives equities risk-on; **crypto institutional outflow** keeps digital assets decoupled and heavy. Secondary: DeFi rotation (CRV/STG), World-Cup memecoin froth (context only).
- **Preferred side now:** **stocks — long-on-pullback / wait-tomorrow-RTH** (do not chase the bell); **crypto — wait-for-trigger / fade-into-strength**, no fresh chase.
- **Best long candidate:** **JPM** (stocks, risk-on aligned, financials strong) — but tomorrow-RTH, not late-session; weak 1.0 RR. Crypto: **ATOM/USDT** long-watch on a held 1.925–1.943 pullback.
- **Best short candidate:** **none clean** — trigger: tape rolls red into the close (SPX red) + VIX > ~22 on a failed retest of today's highs (GOOGL, weakest sector).
- **Best catalyst-backed candidate:** **CRV/USDT** — real Curve DAO rally, but extended → manage, not chase.
- **What to avoid:** new mega-cap tech shorts into de-escalation; chasing extended crypto RS-leaders at the highs; **UNH** / **SMCI** (legal/headline risk).
- **What would change the view:** equities — VIX back > ~22 + SPX red close (revives shorts) OR a confirmed Iran-deal headline (extends risk-on, lifts longs incl. crypto); crypto — first net ETF *inflow* day / BTC reclaim > ~$63.5K (turns relief pops into trend longs).

## 7. Candidate Deep Dives (≤ 5)

### 7.1 JPM — long · B · stocks intraday · score 65.35 · `waiting_for_entry`
- **Setup:** entry 312.32–313.48, invalidation close < 310.00, TP1 316.95 / TP2 319.26 / TP3 322.74. RS-leader (+5.45% vs SPY 20d, +1.16% vs sector), financials a top-3 strong sector, earnings safe. Playbook `stocks_intraday_rth_momentum` (B-tier 14d: WR 55%, PF 2.03, +80R; shorts subset PF 9.0).
- **Price-reaction / chase check:** the catalyst here is the *tape* (risk-on bounce), and JPM is aligned with it — not chasing a news spike. BUT **RR-to-TP1 is only 1.0** (the report itself flags "RR to TP1 below 1.5"), and it is **~80 min to the close** — far too late to open a fresh intraday momentum trade that needs room to TP1.
- **Mood alignment:** YES — long, risk-on, strong sector, RS-leader. The cleanest *directionally-correct* idea on the board.
- **Actionable now?** **No — wait-for-tomorrow-RTH.** Late-session entry has no runway and a sub-1.5 RR. Re-validate at the 11:30/16:20 slots tomorrow if JPM holds > 310 and the risk-on tape persists.
- **Invalidation:** close < 310.00, or a VIX spike back > 22 / SPX reversal red.
- **Contradiction check:** stock **A-tier 0% winrate / −6R this week** and **stock longs PF 0.42 / −25R** are the broad warning — but those failures are concentrated in A-tier overpromotion and forced longs in weak regimes; JPM is **B-tier** (PF 1.92 this week) and *with* the risk-on tape, so the bucket-level long warning is softened, not eliminated. Still: size for paper, weak RR, late.

### 7.2 CRV/USDT — long · B (catalyst-backed) · crypto · `triggered` (swing) / `tp1_hit` (scalp)
- **Setup:** swing triggered entry 0.2443–0.2481, stop/inval 0.2396, TP1 0.2583; scalp already `tp1_hit` and **expiring ~21:40** (let it expire). Current ~0.249; RS vs BTC +13.2%, 24h +14% / 7d +26%.
- **Catalyst (web-verified §13):** Curve DAO is the **strongest DeFi token in the current rotation**, +22%/24h, reclaimed the $0.20–0.21 resistance shelf, Ichimoku/CMF flipped positive. Real, not a no-news momentum cluster.
- **Price-reaction / chase check:** **price has ALREADY reacted** to the catalyst — the move is +22–27% and extended. AMBCrypto's own framing ("relief rally may not last") plus a crypto-wide risk-off tape (ETF outflows) argue the easy part is done. A *fresh* entry at the highs is a chase.
- **Mood alignment:** partial — it's an RS-leader long in a risk-off crypto tape; works as *relative* strength, fails if BTC rolls.
- **Actionable now?** **Manage existing, do not chase fresh.** The swing signal is already triggered; let it run to its own stop/TP. New entries only on a *held* pullback into 0.2443–0.2481, never at the highs.
- **Invalidation:** 1h close < 0.2396; BTC breakdown < ~$61K.

### 7.3 ATOM/USDT — long · B · crypto swing · score 67.9 · `waiting_for_entry`
- **Setup:** entry 1.925–1.943, stop/inval 1.903, TP1 1.991 (RR 1.2); current ~1.953 (price sits just *above* the zone — a genuine pullback-buy, not a chase). RS vs BTC +8.1%, 24h +8.8%, **OI up + price up = fresh positioning confirms trend** (crowding normal), vol 1.26x.
- **Price-reaction / chase check:** NOT overextended; the plan is to buy a pullback *into* support 1.737–1.974 band, entry below spot. Clean structure.
- **Mood alignment:** the weakest link — **no fresh verified catalyst**, and the playbook's own note is "no-catalyst intraday in chop is net-negative (WR 23% / PF 0.70 / −3R) — needs RS-leader or breakout confirmation." It *is* an RS-leader with OI confirmation, which is the saving grace.
- **Actionable now?** **Long-watch only** — wait for the 1.925–1.943 zone to be tagged *and hold* with BTC stable. Do not pre-position; in a risk-off crypto tape a no-catalyst long needs the zone to prove itself.
- **Invalidation:** 1h close < 1.903; BTC breakdown.

### 7.4 Carried mega-cap tech shorts (GOOGL / META / TSLA / NFLX) — short · B→demoted C · stocks intraday
- **Status:** the 18:44 "short-watch on a failed retest." This slot the retest **did not fail** — de-escalation extended the bounce, VIX fell to 20.02, and the fresh 18:28 scan **demoted all of them to C-tier** (GOOGL 51.6, META 52.7, NFLX 54.5; MSTR rejected 46.9). Active DB rows still show earlier-cycle `triggered` shorts, but those are managed remnants, not fresh ideas.
- **Decision:** **AVOID new shorts.** Shorting mega-cap tech into a de-escalation risk-on rally is fighting the tape — exactly the failure mode the desk flags. Note the *direction* stat is favourable for shorts in aggregate (PF 1.45), but that edge was earned in the prior risk-off window, not today's risk-on bounce.
- **What would revive them:** SPX rolls red into the close **and** VIX back > ~22, on a *failed* retest of today's highs (GOOGL cleanest — weakest sector, no bullish contradiction). Until then, short-watch only.

### 7.5 Legal / headline-risk names — UNH, SMCI (+ ID/USDT chase-risk)
- **UNH:** DOJ **antitrust + fraud probe**, stock −16% (catalyst_events legal_risk 0.73, multi-source: QuiverQuant + Yahoo). Currently **C-tier no-trade** in the desk — correct. **AVOID** any long; do not treat the −16% washout as a clean bounce-long without a verified resolution.
- **SMCI:** export-control **indictment** of three individuals (Form 8-K, legal_risk 0.77) — but **stale, filed Mar 1**; desk has it **rejected (47.8)**. AVOID; not actionable, flag only.
- **ID/USDT** (crypto, `triggered`, +31% 24h): **chase-risk** — pure momentum, *no* verified catalyst, vol only 0.3x (thin). The triggered signal is already in-trade; **no fresh entry at +31%**. Long-watch only on a deep pullback to 0.0341–0.0356 that holds.

## 8. Best Candidates Ranked

No clean *fresh-entry* candidate exists this decision window (late session + de-escalation re-route + crypto risk-off). Routed watch list with exact triggers:

1. **Best long-watch — JPM (stocks):** trigger = **tomorrow's RTH**, JPM holds > 310 and risk-on tape persists; enter 312.32–313.48 (weak 1.0 RR — keep small). *Not* a late-session entry today.
2. **Best long-watch (crypto) — ATOM/USDT:** trigger = pullback **tags and holds 1.925–1.943** with BTC stable + volume on the hold; inval 1.903.
3. **Best catalyst-backed — CRV/USDT:** trigger = **held pullback into 0.2443–0.2481** (not the highs); manage the already-triggered swing to its own stop/TP1 0.2583.
4. **Best short-watch — GOOGL (stocks):** trigger = **SPX red close + VIX > ~22 + failed retest of today's high**; weakest sector. Dormant while the tape is green.

## 9. Avoid / No Trade (this decision window only — scanner keeps running)

- **New mega-cap tech shorts (GOOGL/META/TSLA/NFLX/MSTR)** into a de-escalation risk-on rally — wrong side of the tape.
- **Chasing extended crypto RS-leaders** (CRV +22%, ID +31%, FIDA +16%, HEMI +18%) **at the highs** into a risk-off crypto tape — wait for held pullbacks.
- **JPM as a late-session intraday entry** — no runway to TP1 ~80 min before the close; defer to RTH tomorrow.
- **UNH** (DOJ probe, −16%) and **SMCI** (indictment) — legal/headline risk; no clean long.
- _Scanning, candidate generation, tracking, and monitors **continue** — this is a current-window caution, never a stop command._

## 10. Main Risks

- **Stale desk-label risk:** stock regime label `chop` lags the live de-escalation risk-on tape — do not let a neutral label suppress the (tomorrow-RTH) long read.
- **Macro reversal tail:** the de-escalation is a *Trump headline*, not a signed deal — a re-escalation or a failed-deal headline could snap VIX back > 22 and validate the shorts within hours. Two-sided.
- **Crypto divergence trap:** equity risk-on can lure crypto longs, but BTC/ETH ETF outflows are at record streaks — relief pops fade unless flows turn. Do not import equity risk-on into crypto sizing.
- **Catalyst layer 80% unmapped** — context only, not a decision input (persistent).
- **Structural bucket failures (paper):** stock A-tier 0% WR/−6R, stock longs PF 0.42/−25R, stock-swing PF 0.35/−11R — see §14 TODOs.
- **Source-ingest:** ran for cited sources; if the ingest CLI errors it is logged here and does not block the review.

## 11. Action Plan — next 4 hours

1. **Stocks into the close (~14:39→16:00 ET):** no fresh entries. Let the risk-on bounce resolve; the 23:15 post-close slot judges the daily wrap. Mark JPM as a **tomorrow-RTH long-watch** (holds > 310). Keep GOOGL short dormant (needs VIX > 22 + red close).
2. **Crypto evening:** **wait-for-trigger.** ATOM long-watch on a held 1.925–1.943 pullback; CRV manage the triggered swing (do not chase); ID no fresh entry at +31%. Watch BTC ~$61–63K and the ETF-flow tape — first inflow day flips the read.
3. **Let expiring scalps expire** (CRV/PYTH/ATOM-scalp ~21:40) — do not re-enter into the close.
4. **Re-check at 23:15 post-close slot:** how the US session closed, whether the de-escalation held, daily paper-trade outcome by tier; carry the crypto setup into Asia.
5. **No code changes** — §14 TODOs are handed to a manual session.

## 12. Final Verdict per Mode

- **Crypto scalp:** **no fresh trade** — chop + risk-off undertow; expiring scalps let expire. Watch RS-leaders for held pullbacks only.
- **Crypto intraday:** **wait-for-trigger** — ATOM long-watch on a held 1.925–1.943; ID no chase at +31%.
- **Crypto swing:** **manage existing** (CRV triggered, ATOM waiting) — no new at the highs; RS-leader longs only on pullbacks with BTC stable.
- **Stocks intraday:** **risk-on but too late** — JPM is the directionally-correct long, deferred to tomorrow-RTH; no new shorts into de-escalation.
- **Stocks swing / invest:** **carry-forward planning only** (reports ~4.3h); LLY A-tier longs are triggered/managed — A-tier 0% WR caveat applies, no fresh adds.

## 13. Sources

- [Stock Market Today (June 11, 2026): Nasdaq, S&P 500 rise despite mixed Oracle earnings, Iran strikes — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-11-2026) — 2026-06-11. Indices green, VIX 20.02 (−9.88%), breadth 57% advancing, R2K +1.44%; Trump cancelled this-evening Iran strikes, "deal essentially agreed"; Oracle −11.9%, Intel +10.3%, Arm +7.8%. _single_source._
- [Bitcoin ETF Outflows Hit 13-Day Streak as $4.3 Billion Exits the Funds — BeInCrypto](https://beincrypto.com/bitcoin-etf-outflows-record-streak-june-2026/) — 2026-06-11. BTC ~$61,900, ETH ~$1,660; BTC ETF 13-day / $4.33B outflow streak; ETH ETF 17-day record streak. _single_source._
- [Bitcoin remains under pressure as ETF outflows, higher oil prices weigh on crypto — CoinDesk](https://www.coindesk.com/daybook-us/2026/06/01/bitcoin-remains-under-pressure-as-etf-outflows-higher-oil-prices-weigh-on-crypto-markets) — 2026-06-01. Multi-week crypto risk-off / outflow regime context. _single_source._
- [Bitcoin Holds Steady While Curve DAO (CRV) and Stargate Finance (STG) Lead the Altcoin Rally — EdaFace](https://news.edaface.com/2026/06/11/bitcoin-holds-steady-while-curve-dao-crv-and-stargate-finance-stg-lead-the-altcoin-rally/) — 2026-06-11. CRV ~$0.2438, +22%/24h, reclaimed $0.20–0.21, strongest DeFi token in rotation, Ichimoku/CMF positive. _single_source._

_Internal: desk reports (scalp/intraday/swing crypto + stocks intraday/swing/invest), `catalyst_events.jsonl`/`narrative_baskets.jsonl`, `proposed_signals` (DB), `active-signals`/`signal-stats`/`detect_untracked_legacy_alerts` CLI. Source-discipline: every external claim carries title + source + date + URL; no fabricated chart observations (TradingView MCP not loaded — local OHLCV/ATR/EMA only); `published_at` left as the source's date, never invented._

## 14. Fix Requests / TODO

### TODO-catalyst-mapper
- **issue:** catalyst symbol-mapping is 80.0% unmapped this run (2275/2844 null-symbol), persistently >50% across every run today (79.3% at 18:44).
- **evidence:** `data/catalysts/2026-06-11/catalyst_events.jsonl`; unmapped sample incl. "Schwab (SCHA) vs iShares (IJR)" (multi-ETF), small-cap insider headlines (ICU Medical/Nayax/Digi), and genuinely symbol-less macro (Iran Fifth-Fleet).
- **suggested manual fix:** improve the symbol resolver — add a ticker-in-parens extractor (SCHA/IJR style), an insider-headline company→ticker lookup, and explicitly bucket macro/geopolitics as `symbol=null, scope=macro` so true-macro is separated from resolver misses to make the % meaningful.
- **priority:** medium
- **first observed:** 2026-06-11 11:39 EEST (recurring; re-confirmed 21:39 EEST)

### TODO-stock-atier-overpromotion
- **issue:** stock A-tier is 0% winrate / −6R this week (PF 0.000, n=8) — the desk's own playbook note flags "A-tier overpromotion on losing names (NVDA/SMCI/SMH longs structurally lose in this regime)."
- **evidence:** `signal-stats --asset-class stocks` (tier split: A-tier n=8, TotalR −6.00, PF 0.000, WR 0.0%); stocks intraday report §6 "Known failure mode" line.
- **suggested manual fix:** audit the A-tier promotion gate for stocks — tighten or add a regime/RS filter so structurally-losing megacap longs (NVDA/SMCI/SMH) cannot reach A-tier in chop/weak-long regimes.
- **priority:** high
- **first observed:** 2026-06-11 21:39 EEST

### TODO-stock-swing-losing-bucket
- **issue:** stock **swing** bucket is a reproducible loser — PF 0.35, −11R (6 wins / 17 losses); stock **longs** overall PF 0.42 / −25R vs **shorts** PF 1.45 / +13R.
- **evidence:** `signal-stats --asset-class stocks` (By mode: swing PF 0.352900 totalR −11; By direction: long PF 0.418600 totalR −25, short PF 1.4483 totalR +13).
- **suggested manual fix:** review stock-swing entry criteria and the long/short asymmetry — consider down-weighting long-swing in risk-off/weak-long regimes or requiring stronger RS/catalyst confirmation for stock longs.
- **priority:** medium
- **first observed:** 2026-06-11 21:39 EEST
