# Opus Enriched Review — post-close final daily review — Auto Cycle 23:24 EEST

_Slot: 23:15 post-close final daily review · Thursday 2026-06-11 · ~16:24 ET, ~24 min after the US cash close. Focus: the daily wrap — how the US session closed, what worked/failed today, end-of-day risk/exposure, what stays active overnight, and the overnight-into-Asia crypto setup. Advisory-only, read-mostly — no auto-trade, no code edits, paper-trading. §14 TODOs only, no fixes._

## 1. Executive Summary

**The day closed risk-ON and the close confirmed the de-escalation thesis the 21:39 review routed.** The US cash session ended with a broad, small-cap-led rally on Iran de-escalation: **Russell 2000 +3.06%, Nasdaq +2.53%, Dow +1.87% (50,848, +929 pts), S&P 500 +1.74% (≈7,400)** (web §13). Tech, industrials and materials led; energy, staples and real estate lagged; VIX fell sharply (desk read **19.58**; web sources cited an easing into the low-20s). Small-cap leadership + broad breadth = a genuine risk-on close, not a narrow mega-cap melt-up.

**What worked / failed today:** the 21:39 review's two key calls both aged well — (1) it **invalidated the carried mega-cap-tech SHORT thesis** ("the retest never failed, de-escalation extended"), and the rally indeed extended into the bell, so the still-active **GOOGL / NFLX B-tier shorts are wrong-side the close** (manage/avoid, likely stopping); (2) it routed the risk-on book to **long / RS-leader / financials**, and JPM/AMD-type longs were directionally correct. Net daily realized read (week, signal-stats): **crypto A/B PF 2.06, +19R** (healthy, swing the best bucket); **stocks A/B PF 1.26, +5R** but the C-tier book is bleeding (**PF 0.66, −21R**) and the **stock A-tier remains anemic (n=8, 0 wins / 6 losses, −6R)** — stocks stay the structurally weaker book even on a green day.

**Crypto DIVERGED but firmed modestly — still risk-off underneath.** BTC **$62,800 (+1.3%/24h)**, ETH **$1,647 (+0.3%/24h, still stuck < $1,700)**, BNB +1.2%, SOL +1.1%, XRP −0.6% near $1.10 (web §13). The equity de-escalation produced only a shallow crypto bid because **ETF outflows persisted another full day: BTC −$213.85M, ETH −$35.59M (combined −$249.44M)** — institutional conviction is still absent. So crypto's relief pop is **cautiously constructive but fragile**: BTC must reclaim **$63–65K** to confirm anything. Desk regime **range/chop, BTC/ETH range, alt breadth 47.8% > EMA20 / 30.4% > EMA50 (narrowing)**. **No A/B-tier crypto setups this run — everything is C-tier watchlist.**

**Overnight-into-Asia setup (the live actionable class now that stocks are closed):** relief-bounce-within-downtrend. The decision hinges on whether the equity risk-on bleeds into Asia and lifts **BTC > $63.5K** (turns RS-leader pops into trend longs) or crypto re-decouples and fades as ETF outflows dominate. Until BTC reclaims $63.5K, treat the RS-leaders (FIDA/ID/STG/HMSTR/HEMI) as **sellable strength / wait-pullback**, and ETH (laggard < $1,700) as the relative-weakness short-watch on a failed bounce.

**Routed verdict (this decision window only):**
- **Best long-watch:** **none clean / wait-for-trigger.** Crypto **ATOM/USDT** long-watch only on a *held* pullback (OI-confirmed RS-leader, B-swing active, `waiting_for_entry`) — no catalyst, demand the zone to hold. Stocks **AMD / JPM** long — but **tomorrow-RTH** (market closed; both closed green and aligned with the risk-on tape).
- **Best short-watch:** **none clean.** ETH/laggards (STRAX/OPN/HOME/MORPHO bleeding) short-watch only on a *failed* bounce; thin low-float = squeeze-prone, avoid. Stock mega-cap-tech shorts (GOOGL/NFLX) are wrong-side a risk-on close — trigger to revive: tape rolls red + VIX back > ~22 on a failed retest of today's highs.
- **Best catalyst-backed:** **HYPE/USDT** — Kalshi launched HYPE perpetuals (exchange_listing, importance 0.75) — but the perps_dex narrative playbook is **`wait_pullback`** and price has largely reacted → watch, don't chase.
- **What to avoid:** chasing extended crypto RS-leaders at the highs into persistent ETF outflows; ETH longs (< $1,700 laggard); legal/headline names **UNH** (DOJ probe, −16%) and **SMCI** (export-control indictment, stale Mar 1); thin delisting/low-float dumps.

**System health:** untracked-alert detector **clean (0)** — no PART-1 regression. Scheduler **fresh** (~1h). Catalyst mapping **weak again — 80.6% unmapped** → catalyst layer is context, not a decision input. §14 TODOs persist (catalyst mapper, stock A-tier overpromotion, stock C-tier losing book).

## 2. Data Used

- Crypto **scalp** — `data/reports/scalp/2026-06-11_19-09_scalp_report.md` (mtime 22:09) — **fresh** (~1.25h).
- Crypto **intraday** — `data/reports/intraday/2026-06-11_19-17_intraday_report.md` (mtime 22:17) — **fresh** (~1.1h).
- Crypto **swing** — `data/reports/swing/2026-06-11_14-18_swing_report.md` (mtime 17:18) — **carry-forward** (~6.1h; flagged §3).
- **Stocks intraday** — `data/reports/stocks/intraday/2026-06-11_19-51_stocks_intraday_report.md` (data 19:51 UTC ≈ 22:51 EEST) — **fresh near-close snapshot** (~9 min before the bell).
- **Stocks swing / invest** — `..._14-23_` / `..._14-27_` — **carry-forward** (~9h; planning context, flagged §3).
- Catalysts — `data/catalysts/2026-06-11/` (events.jsonl + narrative_baskets.jsonl + `catalyst_cycle_19-18.md`, mtime 22:18) — **fresh** (~1.1h). `catalyst-scan` NOT re-run (dir present).
- LLM packets — `data/processed/llm_analysis_packet.md` (22:18), `llm_stocks_packet.md` (22:25).
- CLI (from cycle_05 summary, mtime 22:26): `active-signals` crypto (8) + stocks (20); `signal-stats` crypto + stocks; `detect_untracked_legacy_alerts` (**clean — 0 untracked**).
- External: WebSearch ×2 (US close June 11; BTC/ETH + ETF flows June 11), WebFetch ×1 (cryptotimes June 11 — **opened, cited §13**). External research **AVAILABLE** this run.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **22:26:19** (~1h ago) — **fresh**. Latest cycle summary `cycle_05_21-56_summary.md` mtime **22:26:16** (~1h) — **fresh**. Both well inside the 3h defer threshold → **review proceeds normally**.
- Crypto scalp/intraday + stocks intraday + catalysts are **fresh** (~9 min–1.25h).
- **Carry-forward flag:** crypto **swing** (~6.1h) and stock **swing/invest** (~9h) are in the 4–12h band → usable as planning context, not fresh confirmation. No source is >14h.
- **Stocks data is a near-close snapshot** (19:51 UTC, ~9 min before the 16:00 ET bell). It does not capture the final-print tape; the actual close (Russell +3.06% etc.) is web-sourced (§13). The desk's stock label was still `chop`/neutral, VIX 19.58 — the realized close confirmed the risk-on reading the 21:39 review already flagged.

## 4. What Changed vs Previous Review

Prior: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-11_2139.md` (late-session risk review, 21:39 EEST).

- **The session CLOSED and confirmed the de-escalation rally.** 21:39 saw the bounce holding intraday (Nasdaq +0.8%); the **close extended it materially** (Nasdaq +2.53%, Russell +3.06%, Dow +929 pts). The risk-on read was correct and strengthened into the bell.
- **Mega-cap-tech short thesis fully invalidated by the close.** 21:39 withdrew the short-watch; the extended risk-on close means the still-active **GOOGL / NFLX B-shorts are wrong-side** → manage/avoid, not fresh entries.
- **JPM/AMD long routing aged well.** Both are still the cleanest directionally-correct stock ideas; AMD is the only fresh stock B-tier (65.09), JPM carried — both now **tomorrow-RTH** (market closed).
- **Crypto firmed but stayed decoupled.** BTC drifted **$61.9K → $62.8K**, ETH **~$1.66K → $1.647K (still < $1,700)**. The equity close did **not** trigger a crypto trend turn — **ETF outflows persisted another −$249M day**. Divergence intact; relief, not reversal.
- **Carried crypto B-longs largely realized** (CHIP tp2; CRV-scalp/ALLO/BABY/BANK tp1) — managed/closing, not fresh. ATOM still `waiting_for_entry`; ID intraday `triggered`.
- **Catalyst mapping** still weak: 80.0% → **80.6% unmapped**. TODO persists.
- **Untracked-alert detector** still **clean (0)** — no regression.

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative jsonl): **3344**.
- Mapped (non-null symbol): **650**.
- Unmapped (null symbol): **2694** → **80.6% unmapped**.
- `narrative_baskets`: **4** (perps_dex_narrative, delisting_thin_liquidity, ai_narrative, rwa_narrative).
- **⚠ catalyst mapping weak this run — use the catalyst layer as context, not a final decision input.** (>50% unmapped, persistent across every run today.)
- Top unmapped-by-importance headlines (macro / multi-entity — several legitimately symbol-less):
  1. `0.73` "UK surveillance laws face US scrutiny over Apple backdoor demand" — macro/regulatory, no single ticker.
  2. `0.73` "'No current users affected' — Raydium responds after $1.34M exploit" — SOL-related but resolver left it unmapped (should map to SOL).
  3. `~0.70` macro/geopolitics + insider-sale cluster the resolver did not map.
- Mapped catalyst clusters that matter: **HYPE** Kalshi launches HYPE perpetuals (exchange_listing, imp 0.75); **SOL** Raydium $1.34M exploit (exploit_hack); **AAVE** risk-framework after April $290M exploit; **BTC** BlackRock income-ETF / ETF-outflow cluster (regulatory_sector_headline); **SMCI** export-control indictment (legal_risk, **stale — filed Mar 1**); **UNH** DOJ probe (legal_risk, −16%).

## 6. Market Landscape

**Stocks (closed, web §13):** Russell 2000 **+3.06%**, Nasdaq **+2.53%**, Dow **+1.87%** (50,848), S&P 500 **+1.74%** (≈7,400). Driver: **Iran de-escalation** ("deal essentially agreed"). Leaders: tech, industrials, materials + semis (SMH RS +6.77% 20d). Laggards: energy, staples, real estate, communications. VIX eased sharply (desk 19.58). Small-cap leadership + broad breadth (desk 75% > EMA20) = clean risk-on close.

**Crypto (live overnight class):** BTC **$62.8K (+1.3%)**, ETH **$1,647 (+0.3%, < $1,700)**, BNB/SOL green, XRP weak near $1.10. Regime range/chop, alt breadth narrowing (47.8% > EMA20). **ETF outflows persist (−$249M combined)** → relief bounce within a risk-off institutional backdrop, decoupled from the equity rally. RS-leaders: STG +43%, ID +34%, HMSTR +25%, FIDA +23% (all C-tier watchlist, thin volume).

### Market Mood / Risk Routing  (REQUIRED)
- **Crypto mood:** **risk-off / chop** — range regime, ETH < $1,700, persistent ETF outflows; relief pops are sellable strength, not trend longs.
- **Stocks mood:** **closed — closed risk-on** (de-escalation rally, small-cap-led, VIX eased). Live US book is flat until tomorrow's open.
- **Dominant narrative:** **Iran de-escalation / deal hope** drove the equity risk-on close; **crypto institutional outflow** keeps digital assets decoupled and heavy. Secondary: perps-DEX (HYPE/Kalshi), AI rotation (NEAR/RENDER/TAO), World-Cup memecoin froth (context only).
- **Preferred side now (overnight, crypto):** **wait-for-trigger.** Longs only on RS-leader + **BTC reclaim > $63.5K**; shorts only on ETH/laggard *failed* bounce. Stocks: long-on-pullback **tomorrow-RTH**, no overnight stock action.
- **Best long candidate:** **none clean** — crypto ATOM/USDT long-watch on a held pullback; stocks AMD/JPM tomorrow-RTH. Trigger: BTC > $63.5K (crypto) / hold-above-entry at the open (stocks).
- **Best short candidate:** **none clean** — trigger: ETH fails a bounce back under $1,640 with BTC rejecting $63.5K; or stock tape rolls red + VIX > ~22 on a failed retest (GOOGL/NFLX).
- **Best catalyst-backed candidate:** **HYPE/USDT** (Kalshi HYPE perps) — playbook `wait_pullback`, largely reacted → watch, don't chase.
- **What to avoid:** chasing extended crypto RS-leaders into ETF outflows; ETH longs < $1,700; **UNH / SMCI** (legal/headline risk); thin delisting/low-float dumps; new mega-cap-tech shorts into a risk-on close.
- **What would change the view:** crypto — first net ETF *inflow* day / **BTC reclaim > $63.5K** (turns relief into trend longs) OR BTC loses $60K (re-accelerates downtrend, revives shorts); stocks — VIX back > ~22 + a red open (revives shorts) OR a confirmed Iran-deal headline (extends risk-on into tomorrow).

## 7. Candidate Deep Dives (≤ 5)

### 7.1 AMD — long · B · stocks intraday · score 65.09 · `waiting_for_entry`
- **Setup:** entry 482.93–488.70, invalidation close < 471.41, TP1 505.98 / TP2 517.51 / TP3 534.79. RS-leader (+10.24% vs SPY 20d, +3.47% vs sector), semis the strongest sector, earnings safe. Playbook `stocks_intraday_rth_momentum` (B-tier 14d: WR 55%, PF 2.03, +80R).
- **Price-reaction / chase / mood:** catalyst is the tape (risk-on close) + semi leadership; AMD is aligned, not chasing a news spike. RR-to-TP1 is weak (1.0) per the report. **Market closed → cannot act tonight.**
- **Actionable?** **Tomorrow-RTH long-watch.** Re-validate at the 11:30/16:20 slots; demand a hold above the entry zone and a persistent risk-on tape. Avoid NVDA/SMCI-style overpromoted semis longs (known failure mode in the playbook).
- **Invalidation:** close < 471.41, or VIX spike > 22 / SPX reversal red at the open.

### 7.2 JPM — long · B · stocks intraday · `waiting_for_entry`
- **Setup:** financials a top-3 strong sector, RS-leader, earnings safe; carried from 21:39 where it was the cleanest risk-on-aligned idea but too late to enter into the bell.
- **Price-reaction / chase / mood:** aligned with the risk-on close (financials green); not chasing. RR-to-TP1 was weak (~1.0).
- **Actionable?** **Tomorrow-RTH long-watch**, same as 21:39. No overnight action.
- **Invalidation:** close below the entry zone / VIX > 22 / risk-off reversal at the open.

### 7.3 GOOGL / NFLX — short · B · stocks intraday · `triggered` (active)
- **Contradiction-risk candidate (§F priority 2).** These mega-cap-tech B-shorts are **wrong-side the de-escalation close** — the 21:39 review already invalidated the short thesis, and the rally extended into the bell. They are live `triggered` signals but the tape moved against them.
- **Price-reaction / mood:** short into a broad risk-on close = fighting the tape; these are likely at/near stop. **Do NOT add; manage existing per their stops.**
- **Legal/headline check:** no fresh indictment/SEC/DOJ flag on GOOGL or NFLX in today's catalysts (the legal-risk names are UNH/SMCI, §7.5). No clean short catalyst.
- **Actionable?** **Avoid new shorts.** Revive trigger: tape rolls red + VIX back > ~22 on a *failed* retest of today's highs.

### 7.4 BTC / ETH — overnight crypto macro (the live decision)
- **State:** BTC **$62.8K (+1.3%)**, ETH **$1,647 (+0.3%, < $1,700)**. Regime range/chop; ETF outflows **−$249M combined** another day. Liquidation data mixed (longs pressured 24h, shorts squeezed shorter-term) → choppy, no clean directional conviction.
- **Price-reaction / chase:** the relief pop has already partly reacted; **BTC has not reclaimed $63–65K** so there is no confirmed trend. Entering longs here is chasing a bounce inside a downtrend with institutional outflows as a headwind.
- **Mood / side:** wait-for-trigger. **Long trigger: BTC reclaim + hold > $63.5K** (turns RS-leader pops into trend longs). **Short/avoid trigger: BTC rejects $63.5K and ETH loses $1,640** (laggard rolls over, re-accelerates risk-off).
- **Invalidation of the constructive read:** BTC loses **$60K** → downtrend resumes; first net ETF *inflow* day → constructive read upgrades.

### 7.5 UNH / SMCI — legal / headline AVOID
- **UNH:** DOJ probe / fraud investigation, shares **−16%** (legal_risk 0.73, QuiverQuant; web-confirmed in prior reviews). A C-tier long appears in the stock book — **AVOID / MANUAL REVIEW REQUIRED**, never a clean actionable long while the DOJ probe is live.
- **SMCI:** Form 8-K export-control-violation indictment of three individuals — **stale (filed Mar 1)**, carried as a standing flag; **AVOID** on the long side, do not treat as fresh.
- **Verdict:** both excluded from any actionable long; surfaced as the day's standing legal/headline risks.

## 8. Best Candidates Ranked

No clean actionable candidate this window (market closed for stocks; no A/B crypto, crypto relief-within-downtrend). Per PART 9, the routed watch-list:

1. **long-watch — ATOM/USDT (crypto):** trigger = a *held* pullback into its OI-confirmed entry zone **with BTC > $63.5K**; RS-leader, B-swing active `waiting_for_entry`, no catalyst → demand the zone to hold. Re-check 04:30 Asia slot.
2. **long-watch — AMD (stocks):** trigger = tomorrow-RTH hold above 482.93–488.70 with risk-on tape persisting; RS-leader semis. Weak 1.0 RR — partials early.
3. **long-watch — JPM (stocks):** trigger = tomorrow-RTH hold above entry, financials green; risk-on aligned.
4. **short-watch — ETH/laggards (crypto):** trigger = ETH fails a bounce back under ~$1,640 while BTC rejects $63.5K; thin alts squeeze-prone → only liquid, failed-retest shorts.
5. **catalyst-watch — HYPE/USDT:** trigger = a *pullback* (playbook `wait_pullback`) after the Kalshi-perps spike, not a chase at the highs; verify the listing held.

## 9. Avoid / No Trade  (this decision window only — system keeps scanning)

- **New mega-cap-tech shorts** (GOOGL/NFLX/META) into a risk-on close — wrong-side; manage existing `triggered` shorts to their stops only.
- **Chasing extended crypto RS-leaders** (STG +43%, ID +34%, HMSTR +25%, FIDA +23%) at the highs on thin volume into persistent ETF outflows.
- **ETH longs** while < $1,700 (laggard, relative weakness).
- **UNH** (DOJ probe −16%) and **SMCI** (export-control indictment) — legal/headline AVOID.
- **Thin delisting / low-float dumps** (`delisting_thin_liquidity` basket) — squeeze/illiquidity risk.
- _Scanning, candidate generation, tracking and outcome recording continue in all moods — this is a decision-window verdict, never a system-stop._

## 10. Main Risks

- **Crypto/equity divergence resolves down:** if the equity risk-on does NOT bleed into Asia, BTC fails $63.5K and ETF outflows keep dominating → the relief pop fades and the RS-leaders mean-revert hard (thin volume amplifies).
- **Stale stock label vs realized close:** the desk's near-close snapshot (VIX 19.58, `chop`) under-reads the actual close; tomorrow's first scan must re-anchor to the realized risk-on tape, not the lagging label.
- **Gap risk overnight:** an Iran headline reversal (deal falls through) would gap equities red and revive the very shorts just invalidated — keep VIX > ~22 + red open as the flip trigger.
- **Catalyst mapper at 80.6% unmapped** — the catalyst layer is context only; do not let an unmapped high-importance headline (e.g. Raydium/SOL) silently miss a symbol.
- **Source-ingest note:** sources JSON built + ingest attempted (§13); if ingest errored it is logged here and does not block the review.

## 11. Action Plan — next 4 hours (overnight → 04:30 Asia slot)

- **Crypto (live):** wait-for-trigger. **Long only if BTC reclaims + holds > $63.5K**; until then treat RS-leader pops as sellable strength / wait-pullback. **ATOM** long-watch on a held pullback. **ETH < $1,640 + BTC rejecting $63.5K** = short/avoid signal.
- **Manage, don't chase:** carried crypto B-longs are largely tp1/tp2 (CHIP/CRV/ALLO/BABY) — let runners work to stops/targets, no fresh adds.
- **Stocks:** none overnight. Pre-stage **AMD / JPM** long-watch for tomorrow-RTH; **GOOGL/NFLX** shorts to be managed to stops, not added.
- **Avoid:** UNH, SMCI, thin low-float dumps, chasing extended alts.
- **Re-check at 04:30 Asia slot:** did the equity risk-on bleed into Asia (BTC > $63.5K)? Did the ETF-outflow streak break? Did ETH reclaim $1,700? Re-route accordingly.

## 12. Final Verdict per Mode

- **Crypto scalp:** No A/B. Range/chop; RS-leaders are wait-pullback. **No fresh chase** — partials on any carried tp1 runners.
- **Crypto intraday:** No A/B. Wait-for-trigger; **BTC > $63.5K** is the long gate, ETH < $1,640 the short gate.
- **Crypto swing:** ATOM long-watch on a held pullback (OI-confirmed RS-leader); carried B-longs largely realized — manage, don't add.
- **Stocks intraday:** **Closed green.** AMD (B) + JPM (B) = tomorrow-RTH long-watch; GOOGL/NFLX shorts wrong-side → manage to stops. No overnight action.
- **Stocks swing/invest:** carry-forward planning only (~9h stale); no fresh verdict.

## 13. Sources

- [Stock Market Today (June 11, 2026): Nasdaq, S&P 500 rise after Iran indicates deal is close — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-11-2026) — 2026-06-11 — US close: Russell 2000 +3.06%, Nasdaq +2.53%, Dow +1.87% (50,848), S&P +1.74%; Iran de-escalation driver; tech/industrials/materials led, energy/staples/real estate lagged. _single_source (headline access 403 on fetch; levels from search snippet)._
- [Crypto Market Today (June 11, 2026): BTC, ETH, BNB, SOL Gain, XRP Slips — CryptoTimes](https://www.cryptotimes.io/2026/06/11/crypto-market-today-btc-eth-bnb-sol-gain-xrp-slips/) — 2026-06-11 — BTC $62,799.88 (+1.3%), ETH $1,647.17 (+0.3%), BNB +1.2%, SOL +1.1%, XRP −0.6% ~$1.10; BTC ETF −$213.85M, ETH ETF −$35.59M (combined −$249.44M); BTC needs $63–65K reclaim. _single_source — WebFetch opened OK._
- [Bitcoin ETF Outflows Hit 13-Day Streak as $4.3 Billion Exits the Funds — BeInCrypto](https://beincrypto.com/bitcoin-etf-outflows-record-streak-june-2026/) — 2026-06 — record BTC ETF outflow streak context. _single_source (search snippet)._
- Internal: desk reports (scalp 19-09, intraday 19-17, stocks intraday 19-51), `signal-stats` crypto/stocks, `active-signals` crypto/stocks, `detect_untracked_legacy_alerts` (clean), catalysts `2026-06-11/` (UNH DOJ probe, SMCI indictment, HYPE/Kalshi, SOL Raydium exploit).

## 14. Fix Requests / TODO

### TODO-catalyst-mapper-unmapped
- **issue:** catalyst symbol-resolver leaves ~80% of events unmapped (80.6% today, 80.0% at 21:39, persistent all day); high-importance SOL-related "Raydium $1.34M exploit" left unmapped.
- **evidence:** `data/catalysts/2026-06-11/catalyst_events.jsonl` — total 3344, mapped 650, unmapped 2694; top unmapped incl. Raydium/SOL headline (imp 0.73).
- **suggested manual fix:** extend the symbol resolver (exchange/protocol-name → ticker map, e.g. Raydium→SOL) and multi-entity ETF headline handling; re-measure mapped%.
- **priority:** medium
- **first observed:** recurring; logged again 2026-06-11 23:24 EEST

### TODO-stock-a-tier-overpromotion
- **issue:** stock A-tier remains a losing bucket — n=8, 0 wins / 6 losses, −6R this week; A-tier overpromotion on structurally-losing names (NVDA/SMCI/SMH longs) is a flagged playbook failure mode.
- **evidence:** `signal-stats --asset-class stocks` (cycle_05 summary): tier A anemic, PF 0.0, −6R; observation "tier=B triggered winrate 33% low".
- **suggested manual fix:** review A-tier promotion gate for stocks intraday; consider demoting overpromoted semis longs without a strong catalyst.
- **priority:** high
- **first observed:** recurring; logged again 2026-06-11 23:24 EEST

### TODO-stock-ctier-losing-book
- **issue:** stock C-tier watchlist book deeply negative — n=306, winrate 11%, PF 0.66, −21R week; drags all-tier to −16R.
- **evidence:** `signal-stats --asset-class stocks`: C-tier PF 0.66 below 0.8, winrate 11%.
- **suggested manual fix:** tighten C-tier entry criteria or treat C-tier purely as research (already not Telegram-actionable) and audit why it generates so many losing triggers.
- **priority:** medium
- **first observed:** recurring; logged again 2026-06-11 23:24 EEST
