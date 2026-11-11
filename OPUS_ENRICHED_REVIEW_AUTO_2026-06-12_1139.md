# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:39 EEST

_Slot: 11:30 Europe / pre-US context · Friday 2026-06-12 · ~04:39 ET / EU late-morning. Focus: EU-morning crypto + macro, what changed since the overnight (04:44) review, BTC/ETH mood + alt breadth, which crypto setups are still actionable before US flows arrive, build the US-session watchlist. US cash session **opens 16:30 EEST (09:30 ET)** → stocks are **pre-market / planning** this slot; do NOT treat stock signals as confirmed before the RTH open. Crypto is the live actionable class. Advisory-only, read-mostly — no auto-trade, no code edits, paper-trading. §14 TODOs only, no fixes._

## 1. Executive Summary

**The overnight panic has not materialized — crypto is holding a constructive chop, and the two biggest macro drags from the 04:44 review have both eased.** External research **available** this run. As of ~08:30 UTC: **BTC ~$62,784 (+1.96%/24h), ETH ~$1,656 (+2.18%/24h)**, BTC dominance 58.49%, 24h market volume +4.0% (CoinMarketCap, §13). Two material updates vs the overnight review:
1. **The ETF-outflow drag has reversed.** The record **13-session, $4.33B** spot-BTC outflow streak **ended June 5** with a small net inflow ($3.05M BTC; ETH ETFs also ended a 17-day streak, +$19.3M via BlackRock ETHA) (The Block, §13). The structural headwind the 04:44 review leaned on as "still bleeding" is, on the latest data, **stabilizing** — a less bearish backdrop than overnight.
2. **Iran de-escalated from the overnight escalation scare.** Latest reporting (June 9, Al Jazeera/CNBC §13) has both sides having **halted attacks** (post the April 8 two-week suspension), with oil ~**$94** (below $100), "door left open to resumption." Fragile, but **not** the re-escalation risk-off overlay flagged at 04:44.

**Crypto regime: transition (mixed), range BTC / downtrend ETH, with a selective alt-momentum rotation underneath.** Desk read (data 06:45 UTC): BTC trend **range**, ETH trend **downtrend**, btc_atr_percentile 42 (normal vol), style **"selective only; demand clean invalidation."** Alt breadth **63.8% > EMA20** (softer than overnight's 68.3%) but **only 34.0% > EMA50** (down from 46.3%) — **the rotation is narrowing**: a handful of momentum leaders are carrying the tape while the median alt slips below its EMA50. Leaders: **HMSTR +42% (new top), XPL +31%, STG +24%, DEXE +10%, KAT +6.8%**. ETH remains the relative laggard, still capped **< $1,700** and in a desk downtrend.

**No A-tier signals — crypto or stocks.** All 9 active crypto signals are **B-tier longs**, and most have **already realized** (ATOM/CRV/CHIP/ALLO/BANK at tp). The only fresh-ish *waiting_for_entry* B's are **HMSTR (scalp 67.9)** and **DEXE (scalp 66.6)** — both RS-leaders, but **HMSTR is +42% and extended (chase-risk)** while **DEXE is the cleaner, OI-confirmed, less-extended long-watch**. Stocks: fresh intraday run is **A/B=0** (closed-market demotion); carry-forward B-shorts **NFLX** and **PLTR** require RTH confirmation. System health clean: untracked-alert detector **0**, scheduler fresh (~1.5h).

**Routed verdict (this decision window only — never a stop command):**
- **Best long-watch (crypto):** **DEXE/USDT** — scalp B 66.6 *waiting_for_entry*, RS +10% vs BTC, vol 2.1×, OI-confirmed (price↑+OI↑). Cleanest non-parabolic RS-leader. Trigger: **held pullback into 21.41–21.72, invalidation 1h close < 21.03**, BTC holding > $62K. No chase at 21.86 highs.
- **Best short-watch:** **none clean crypto.** ETH/USDT is the relative-weakness short-watch **only on a failed bounce / rejection at $1,700 with BTC losing $61K** (avoid — it just bounced +2%). Stock side: **NFLX** (B short) / **SMCI** (C short, legal-backed) short-watches — **require RTH confirmation after 16:30 EEST**, not pre-market.
- **Best catalyst-backed:** **STG/USDT** — only momentum name with a verified news catalyst ("Will a new price rally follow STG's latest 25% surge?", AMBCrypto, importance 0.75), momentum_breakout basket primary. **But +24%/24h, +183%/7d (extremely extended) and funding deeply negative (−0.017, crowded shorts → squeeze-prone both ways).** Playbook = wait_pullback. Catalyst-watch only, no chase.
- **What to avoid:** chasing HMSTR/STG/XPL at extended highs; ETH longs < $1,700; thin low-float momentum dumps (delisting_thin_liquidity basket); **fresh stock entries before the 16:30 EEST RTH open** (gap risk); shorting into the US open without confirmation given healthy stock breadth (75% > EMA20).
- **What would change the view:** BTC reclaim + hold **> $63.5K** on firm breadth → RS-leader pops become trend longs; **BTC loses $61K** → flip to risk-off laggard shorts; clean Iran resolution → risk-on; US open breadth confirmation (or rejection) for the stock book.

**System health:** untracked-alert detector **clean (0)** — no PART-1 regression. Scheduler **fresh** (~1.5h). Catalyst mapping **weak again — 78.1% unmapped** → catalyst layer is context, not a decision input. §14 TODOs persist (catalyst mapper; stock A-tier 0/8 wins PF 0.0; stock C-tier losing book −24R).

## 2. Data Used

- Crypto **scalp** — `data/reports/scalp/2026-06-12_06-57_scalp_report.md` (generated 09:57 EEST, data 06:45 UTC) — **fresh** (~1.7h; report header flags scalp **low-confidence**: PF 0.14 / TP1-horizon mismatch).
- Crypto **intraday** — `data/reports/intraday/2026-06-12_07-05_intraday_report.md` (generated 10:05 EEST, data 06:45 UTC) — **fresh** (~1.6h).
- Crypto **swing** — `data/reports/swing/2026-06-11_14-18_swing_report.md` — **stale** (~21.4h; > 14h → excluded from fresh swing verdict, planning context only; flagged §3).
- **Stocks** intraday — `data/reports/stocks/intraday/2026-06-12_07-10_stocks_intraday_report.md` (data 07:10 UTC) — **fresh data, but closed-market/pre-market** (demoted A/B→C; US RTH opens 16:30 EEST). Stocks **swing/invest** — `..._14-23_` / `..._14-27_` (~21h) → **stale**, planning only.
- Catalysts — `data/catalysts/2026-06-12/` (events.jsonl + narrative_baskets.jsonl + `catalyst_cycle_07-05.md`, mtime 10:05) — **fresh** (~1.6h). `catalyst-scan` NOT re-run (dir present).
- LLM packets present: `data/processed/llm_analysis_packet.md`, `llm_stocks_packet.md`.
- CLI (this run): `active-signals` crypto (9) + stocks (~50); `signal-stats` crypto + stocks; `detect_untracked_legacy_alerts` (**clean — 0 untracked**).
- DB reads (`db/crypto_ai_desk.sqlite`): `news_items` fresh Telegram (7 in last 4h) + stock-candidate legal/headline scan (last 36h).
- External: WebSearch ×2 (BTC/ETH + ETF flows June 12; Iran/oil June 12), WebFetch ×2 (Al Jazeera Iran ceasefire **opened & cited §13**; CNBC oil June 9 **HTTP 403 → search-snippet only, single_source**). External research **AVAILABLE** this run.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **10:11** (~1.5h) — **fresh**, well inside the 3h defer threshold → **review proceeds normally**. (Both freshness checks were not > 3h; no defer.)
- Crypto scalp/intraday + catalysts are **fresh** (~1.6–1.7h).
- **Stale flag:** crypto **swing** report is ~21.4h (> 14h) → excluded from the fresh swing verdict; planning context only. Stock swing/invest (~21h) likewise planning-only.
- **Stocks data is pre-market.** The ~50 active stock signals are last-session carry-forward (Thursday US session). They are **planning/watchlist context** until the 16:30 EEST RTH open; the demoted A/B-shorts (NFLX, PLTR) need RTH confirmation before being treated as live.

## 4. What Changed vs Previous Review

Prior: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-12_0444.md` (crypto overnight / Asia review, 04:44 EEST).

- **ETF-outflow drag reversed.** 04:44 leaned on a "13-session, $4.33B outflow streak, still bleeding" as a decisive structural headwind. Latest data (The Block, §13): the streak **ended June 5** with a small net inflow; ETH ETFs also ended a 17-day streak. **Backdrop is stabilizing, not deteriorating** — the single most important bullish revision.
- **Iran de-escalated from the overnight escalation scare.** 04:44 flagged overnight "re-escalation" headlines (ceasefire-meaningless, Sirik explosion) as a risk-off overlay. Current read (June 9, §13): attacks **halted**, oil ~$94, fragile truce. **Macro risk eased** (desk macro 49–59/100 vs the overnight risk-off tilt).
- **Alt rotation narrowed.** Breadth > EMA20 softened 68.3% → **63.8%**, and > EMA50 fell 46.3% → **34.0%** — fewer alts participating; a thinner momentum-leader-led tape.
- **Leadership rotated.** Overnight leaders (CRV/ID/STG) matured: **CRV/ATOM now show tp_hit in the active book** (prior long-watch CRV thesis played out). **HMSTR emerged as the new top RS-leader (+42%)**, with XPL/STG/DEXE/KAT behind.
- **BTC/ETH roughly unchanged / still capped.** BTC ~$62.5K → ~$62.8K; ETH ~$1.649K → ~$1.656K (still < $1,700, still desk-downtrend laggard).
- **Catalyst mapping** marginally better but still weak: 81.4% → **78.1% unmapped**. TODO persists.
- **Untracked-alert detector** still **clean (0)** — no regression.
- **Stocks** moved from **closed (overnight)** → **pre-market** (Friday RTH ahead); fresh intraday run is A/B=0.

## 5. Catalyst Coverage

- Total `catalyst_events` today (`2026-06-12/catalyst_events.jsonl`): **1591** (cumulative across cycles).
- Mapped (non-null symbol): **348**.
- Unmapped (empty symbol): **1243** → **78.1% unmapped**.
- `narrative_baskets`: **4** (perps_dex_narrative `wait_pullback`; delisting_thin_liquidity `avoid_low_liquidity`; ai_narrative `related_beta_rotation` — NEAR/RENDER/TAO/FET; momentum_breakout `wait_pullback` — HMSTR/XPL/STG, related DEXE).
- **⚠ catalyst mapping weak this run — use the catalyst layer as context, not a final decision input.** (>50% unmapped, persistent across every run.)
- Top 3 unmapped / basket-level headlines (context only):
  1. "SPACEX'S IPO … points upward to a $2.4 trillion valuation" / SpaceX-perps pricing chatter (t.me/WalterBloomberg — rumour/basket).
  2. "BlackRock files 8-A for yield-bearing bitcoin ETF; analyst expects launch next week" (The Block — regulatory, importance 0.80, basket-level).
  3. Iran macro lines ("explosion near Sirik coast", de-escalation/oil) (t.me/WalterBloomberg — macro, basket).
- Mapped top catalysts: **SMCI** (export-control indictment 8-K, legal_risk 0.77), **XRP** (Ripple CEO vs Dimon over Clarity Act, 0.75), **UNH** (DOJ antitrust probe, legal_risk 0.73), **BTC** (BlackRock yield-bearing ETF filing 0.80; ETF flows 0.69).

## 6. Market Landscape

- **BTC** ~$62,784 (+1.96%/24h), trend **range**; key reclaim **$63.5K**, downside pivot **$61K** (web §13 + desk). Dominance 58.49%.
- **ETH** ~$1,656 (+2.18%/24h), trend **downtrend**, still capped **< $1,700** (relative laggard).
- **Alt breadth:** 63.8% > EMA20 / **34.0% > EMA50** — narrowing rotation (leader-led, not broad risk-on).
- **Volatility:** btc_atr_percentile 42 — normal.
- **Leaders (RS vs BTC):** HMSTR +41.8% (vol 2.31×), XPL +31% (1.14×), STG +24% (0.85×), DEXE +10% (2.1×), KAT +6.8% (2.48×), ENSO +7.9%, ATOM +6%. **Laggards / short-bias:** BANANAS31 −18%, HOME −16%, ID −13%, JST −5.5%, BABY −4.7% (thin, squeeze-prone).
- **Derivatives:** HMSTR price↑+OI↑ (funding +4.7e-05, L/S 1.27, crowding normal) — fresh positioning. DEXE price↑+OI↑ (funding +0.0005, OI +11.7%, crowding normal) — clean. STG price↑+OI↓ short-covering, funding **−0.017** (crowded shorts across bybit/mexc → squeeze risk). HMSTR/STG/XPL all in momentum_breakout (avoid_chase).
- **Narratives:** momentum_breakout (HMSTR/XPL/STG, wait_pullback — dominant); perps_dex (HYPE, wait_pullback); AI rotation (NEAR/RENDER/TAO/FET, related-beta); delisting_thin_liquidity (avoid). Macro overlay: Iran fragile-halt (de-escalated), oil ~$94; BlackRock yield-bearing BTC ETF filing (forward catalyst, "launch next week").
- **Stocks (pre-market):** regime **chop**, bias neutral, VIX 19.44, breadth healthy (75% > EMA20, 100% > EMA50). SPY/QQQ **range** (5d −2.6% / −3.2%), IWM/DIA uptrend. Leading sectors: **semis (SMH RS +7.1%), healthcare (XLV +5.6%), tech (XLK +4.2%)**; weak: communications (XLC −3.4%). Fresh A/B=0. Carry-forward shorts NFLX/PLTR + legal-flagged SMCI await RTH. Book remains structurally weak (A-tier 0/8 wins PF 0.0; C-tier −24R PF 0.61).

### Market Mood / Risk Routing      (REQUIRED — PART 4)
- **Crypto mood:**           **chop / mixed** (range BTC / downtrend ETH + narrowing alt-leader rotation; macro drags easing — ETF outflows stabilized, Iran de-escalated)
- **Stocks mood:**           **pre-market** (Friday; US RTH opens 16:30 EEST; chop regime, healthy breadth, fresh A/B=0)
- **Dominant narrative:**    momentum_breakout (HMSTR/XPL/STG); secondary perps_dex (HYPE), AI rotation; macro: Iran fragile-halt + BlackRock yield-bearing BTC ETF filing
- **Preferred side now:**    **wait-for-trigger** — selective RS-leader longs *only on pullback* (crypto); stocks await RTH confirmation
- **Best long candidate:**   **none clean now — DEXE/USDT** long-watch; trigger: held pullback into 21.41–21.72 (invalidation 1h < 21.03), BTC > $62K
- **Best short candidate:**  **none clean — ETH/USDT** short-watch (failed bounce/rejection at $1,700 + BTC < $61K); stock NFLX/SMCI short-watch only after RTH confirmation
- **Best catalyst-backed candidate:** **STG/USDT** (verified 25%-surge news + momentum_breakout primary) — wait_pullback, extremely extended → watch only
- **What to avoid:**         chasing HMSTR/STG/XPL at extended highs; ETH longs < $1,700; thin low-float dumps; fresh stock entries before the 16:30 RTH open
- **What would change the view:** BTC reclaim+hold > $63.5K (→ trend longs) · BTC loses $61K (→ risk-off shorts) · clean Iran resolution (→ risk-on) · US-open breadth confirmation/rejection

## 7. Candidate Deep Dives        (≤ 5)

### 1. DEXE/USDT — B scalp(66.6, waiting_for_entry) + C intraday(61.1) — long — **BEST LONG-WATCH**
- Desk score 92.7, RS vs BTC +10%, 24h +10.3%, 7d +7.5%, **vol 2.1×**. OI-confirmed: price↑+OI↑ (OI +11.7%, funding +0.0005, crowding normal). momentum_breakout *related* (not the parabolic primary).
- Internal: active scalp B `waiting_for_entry` (entry 21.41–21.72, invalidation 1h < 21.03, TP1 22.54). No adverse `news_items`/catalyst for DEXE.
- **Price already reacted?** Modestly (+10%, far less than HMSTR/STG). **Chasing?** Entry at 21.86 spot would be a small chase; the 21.41–21.72 pullback is clean. **Retest structure?** Yes (defined pullback zone). **Overextended (>2 ATR from EMA20)?** No — the least-extended of the leaders. **Entry now late?** Marginally; no on a held pullback. **Actionable level:** 21.41–21.72 holding > 21.03.
- **Mood-aligned?** Yes — selective RS-leader long fits the routing. **Side:** long, **wait-for-trigger**. **Invalidates:** 1h close < 21.03, or BTC < $61K. **Chase-risk:** low-moderate. **Catalyst:** none required (RS/flow); no contradiction.

### 2. HMSTR/USDT — B scalp(67.9, waiting_for_entry) + C intraday(62.3) — long — **CHASE-RISK / DEMOTE**
- Desk score 98.1 (top of flows), RS vs BTC +42%, **24h +42%, 7d +86%**, vol 2.31×. momentum_breakout **primary**. OI-confirmed (price↑+OI↑, funding +4.7e-05, crowding normal).
- **Price already reacted?** Strongly (+42%). **Chasing?** Yes — buying a +42% pop is a chase. **Retest?** Needs a deep pullback (sub-cent levels are noisy; ATR ~0). **Overextended?** Almost certainly > 2 ATR. **Entry now late?** Yes. **Actionable level:** only a sharp held pullback into the entry band; otherwise let it run without you.
- **Mood-aligned?** Marginal (extended). **Side:** long but **avoid fresh** — manage only if already in. **Invalidates:** failure to hold breakout / loss of entry band. **Chase-risk:** **high** (parabolic). **Catalyst:** none confirmed (pure momentum) → treat as such.

### 3. STG/USDT — C scalp(64.7) + C intraday(63.3, actionable) — long — **CATALYST-WATCH / SQUEEZE-PRONE**
- Desk score 91.6, RS vs BTC +24%, **24h +24%, 7d +183%** (extremely extended), vol 0.85×. **Verified catalyst:** "Will a new price rally follow STG's latest 25% surge?" (AMBCrypto, importance 0.75, news_mention). momentum_breakout primary.
- **Derivatives red flag:** price↑+OI↓ (short-covering, weaker continuation) and **funding −0.017** across bybit/mexc (deeply negative = crowded shorts). Squeeze-prone **both ways** — can spike on a squeeze, then mean-revert hard.
- **Price already reacted?** Yes (+183%/7d). **Chasing?** Severe chase-risk. **Retest?** Conditional pullback 0.6128–0.6392 (watch-only per report). **Overextended?** Yes. **Entry now late?** Yes at 0.6509. **Actionable level:** only a deep held pullback with volume returning.
- **Mood-aligned?** As a *catalyst-watch* yes; as a fresh long no. **Side:** long-watch (catalyst). **Invalidates:** loss of 0.5805 / volume failing to confirm. **Chase-risk:** **high**. **Catalyst:** present but single_source news_mention — context, not confirmation.

### 4. NFLX (stock) — B short intraday (triggered, carry-forward) — short — **PRE-MARKET / NEEDS RTH**
- Active stock B short, intraday, `triggered` (entry ~80.x, score ~66). Fresh intraday run demoted A/B→C (closed market). Sector: communications (XLC) is the **weakest sector** (RS −3.4%) → short is sector-aligned. No fresh legal/headline risk found (only a "better buy vs Roku" Motley Fool piece, 06-11).
- **Price reacted?** Carry-forward from Thursday. **Chasing?** Can't tell pre-market. **Actionable?** **No until the 16:30 EEST RTH open confirms** — pre-market shorts into a chop regime with healthy overall breadth (75% > EMA20) are gap-trap-prone. **Side:** short-watch. **Invalidates:** reclaim of entry band on the open. **Chase-risk:** moderate. **Legal:** none flagged.

### 5. SMCI (stock) — C short (swing+intraday) — short — **LEGAL-BACKED SHORT-WATCH / NEEDS RTH**
- Active C-tier short. **LEGAL/HEADLINE RISK:** Super Micro 8-K (FY2026) — indictment of three individuals re alleged export-control-violation conspiracy (SEC EDGAR, importance 0.77, filed Mar 1). News flow: "Why Is Super Micro Stock Crashing" (Motley Fool, 06-12) alongside "$39B AI server orders / $7B financing" — mixed but with a crash + legal overhang.
- **Price reacted?** Yes — already crashing (catalyst largely priced). **Chasing?** Shorting after a crash = chase-risk. **Actionable?** C-tier only; **needs RTH confirmation** and a retest rather than chasing the breakdown. **Side:** short-watch (legal-backed). **Verdict per §I:** **MANUAL REVIEW / AVOID clean-actionable** — C-tier + legal overhang + already-reacted price = not a clean entry. **Invalidates:** reclaim above the breakdown level. **Catalyst:** legal_risk verified (SEC EDGAR, single_source).

## 8. Best Candidates Ranked

No clean fresh-entry candidate this window (live crypto A/B longs are extended or already realized; stocks pre-market). Per PART 9, the routed watch-list:

1. **Best long-watch — DEXE/USDT.** Trigger: **held pullback into 21.41–21.72, above invalidation 1h-close 21.03, BTC holding > $62K.** OI-confirmed RS-leader (+10%, vol 2.1×), least-extended leader. Highest-conviction watch.
2. **Best short-watch — ETH/USDT (crypto) · NFLX/SMCI (stocks).** Crypto trigger: **failed bounce / rejection at $1,700 while BTC loses $61K** (low conviction; it just bounced +2%). Stock trigger: **RTH confirmation after 16:30 EEST** — NFLX (weakest-sector short), SMCI (legal-backed but already-reacted → manual review). Avoid thin low-float crypto laggards (squeeze-prone).
3. **Best catalyst-watch — STG/USDT.** Trigger: **deep held pullback into 0.6128–0.6392 with volume returning** (currently +183%/7d, funding −0.017 crowded shorts → squeeze-prone). Watch only; no chase. Secondary catalyst-watch: HYPE/USDT (perps_dex, wait_pullback) and the **BlackRock yield-bearing BTC ETF filing** ("launch next week") as a forward BTC catalyst to monitor.

## 9. Avoid / No Trade  (this decision window only — never "stop system")

- **Chasing extended RS-leaders at highs** — HMSTR (+42%), STG (+24%/+183%/7d), XPL (+31%) into a *narrowing* breadth tape (EMA50 only 34%). Wait for pullbacks.
- **ETH longs < $1,700** — desk downtrend, relative laggard; only a reclaim flips it.
- **Thin low-float dumps** — BANANAS31/HOME/ID/JST/BABY (delisting_thin_liquidity basket; squeeze-prone).
- **Fresh stock entries before the 16:30 EEST RTH open** — pre-market gap risk; carry-forward shorts (NFLX/PLTR/SMCI) need RTH confirmation, not pre-market chase.
- **SMCI short as a clean actionable** — legal overhang + already-crashed price → MANUAL REVIEW, not a clean entry.

## 10. Main Risks

- **ETH laggard < $1,700** drags risk appetite if it leads a leg down; BTC < $61K flips the whole tape risk-off.
- **Narrowing breadth (EMA50 34%)** — leader-led rallies are fragile; a single BTC flush can unwind HMSTR/STG/XPL fast.
- **Crowded-short squeeze risk** on STG (funding −0.017) — works both directions, unpredictable.
- **Iran fragile-halt** — "door open to resumption"; a re-escalation headline reinstates the risk-off overlay and oil spike.
- **Stock book structurally weak** — A-tier 0/8 wins (PF 0.0), C-tier −24R (PF 0.61), B-tier WR 30%. Treat stock signals with low confidence; RTH-confirm everything.
- **Catalyst mapping 78.1% unmapped** — narrative layer is context only; do not let an unmapped headline drive a decision.
- **Ingest:** sources JSON written to `data/raw/enriched_review_sources/2026-06-12T1139.json`; ingest attempted (see §13).

## 11. Action Plan — next 4 hours

1. **Crypto, into the US session:** watch **DEXE** for a held pullback into 21.41–21.72 (the one cleanish RS-leader long). Let HMSTR/STG/XPL run without chasing; only re-engage on a real pullback + volume.
2. **BTC pivots:** a reclaim+hold **> $63.5K** turns leader pops into trend longs; **< $61K** flips to laggard shorts. ETH < $1,700 = no longs.
3. **Stocks (16:30 EEST RTH open):** do NOT act pre-market. After the open, look for RTH confirmation on **NFLX short** (weakest-sector aligned) and watch **SMCI** (legal-backed, but manual-review given already-crashed price). Respect the chop regime + healthy breadth — prefer retest over chase, require the first 15–30 min to confirm.
4. **Forward catalysts to monitor:** BlackRock yield-bearing BTC ETF ("launch next week"); any Iran re-escalation headline; US macro/data into the cash session.
5. **System:** scanning/tracking continue in all moods. No stop. Re-check at the 16:20 pre-US-open slot.

## 12. Final Verdict per Mode

- **Crypto scalp:** **low-confidence** (report header: PF 0.14, TP1/2h-horizon mismatch). Selective RS-leader longs **on pullback only** — DEXE-watch; HMSTR chase-risk. No fresh chase. Active for data collection.
- **Crypto intraday:** no-catalyst momentum is net-negative in chop (14d: WR 23% / PF 0.70 / −3R). Require **RS-leader + breakout/pullback confirmation**. DEXE/STG watch; no clean fresh entry.
- **Crypto swing:** report **stale (~21h)** → planning only, **no fresh swing verdict**.
- **Stocks intraday:** **pre-market / planning**. Fresh run A/B=0; carry-forward B-shorts (NFLX/PLTR) + legal-flagged SMCI **require RTH confirmation** after 16:30 EEST. Chop regime, healthy breadth → prefer longs-on-confirmation or sector-aligned shorts only post-open. Book weak — low confidence.
- **Stocks swing/invest:** **stale (~21h)** → planning only, no fresh verdict.

## 13. Sources

- [CoinMarketCap — BTC $62,784 / ETH $1,656 / dominance 58.49% (June 12 2026)](https://coinmarketcap.com/) — single_source — confirms desk price band.
- [The Block — Spot Bitcoin ETF Flows: 13-day $4.33B outflow streak ended June 5 (+$3.05M); ETH ETFs ended 17-day streak (+$19.3M BlackRock)](https://www.theblock.co/data/etfs/bitcoin-etf/spot-bitcoin-etf-flows) — single_source — **weakens** prior "ETF still bleeding" thesis (stabilizing).
- [bitcoinfoundation.org — Bitcoin ETF Outflows June 2026: 13-Day $4.4B record (context)](https://bitcoinfoundation.org/news/crypto-etfs-news/etf-outflows-june-first-week/) — single_source — corroborates the streak size/date.
- [Al Jazeera — Trump announces two-week Iran ceasefire; oil slides, stocks surge (Apr 8 2026)](https://www.aljazeera.com/news/2026/4/8/oil-prices-slide-stocks-surge-as-trump-announces-two-week-iran-ceasefire) — single_source (WebFetch opened & verified) — Iran de-escalation context.
- [CNBC — Oil rises slightly as investors await clarity after Iran-Israel halt attacks (June 9 2026)](https://www.cnbc.com/amp/2026/06/09/oil-rises-slightly-as-investors-await-clarity-after-iran-israel-halt-attacks.html) — single_source (HTTP 403 → search-snippet only) — confirms attacks halted, fragile, oil ~$94.

_No fabricated TradingView/chart observations (chart MCP not loaded — local OHLCV/ATR/EMA only). No uncited stats or legal claims. test_source/fixture URLs filtered. External web research AVAILABLE this run._

## 14. Fix Requests / TODO

### TODO-catalyst-mapper
- **issue:** Catalyst symbol-mapping persistently weak — **78.1% unmapped** this run (1243/1591 events null-symbol); same pattern every run (81.4% at 04:44).
- **evidence:** `data/catalysts/2026-06-12/catalyst_events.jsonl` — `symbol==''` for 1243 of 1591 rows.
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (ticker/entity extraction from headline + source); add a mapping-coverage gate/alert.
- **priority:** medium
- **first observed:** recurring; logged again 2026-06-12 11:39 EEST

### TODO-stocks-A-tier-zero-wins
- **issue:** Stock **A-tier 0/8 wins, PF 0.000, Total R −6.00** (week); A-tier on stocks is net-losing with zero winners.
- **evidence:** `signal-stats --asset-class stocks` → "A-tier: n=8 | Total R: -6.00 | PF: 0.000 | Winrate: 0.0%".
- **suggested manual fix:** audit stock A-tier promotion criteria; consider gating A-tier on stocks until the sample turns or thresholds tighten.
- **priority:** high
- **first observed:** recurring; logged again 2026-06-12 11:39 EEST

### TODO-stocks-C-tier-losing-book
- **issue:** Stock **C-tier −24R, PF 0.61, WR 9.7%** (n=302) — large losing research book; all-tier diagnostic −23R.
- **evidence:** `signal-stats --asset-class stocks` observations: "tier=C: triggered winrate 9% is low … profit factor 0.61 below 0.8".
- **suggested manual fix:** tighten C-tier stock entry filters or treat C-tier stocks as research-only (already excluded from headline metric); review `stocks_intraday_rth_momentum` entries.
- **priority:** medium
- **first observed:** recurring; logged again 2026-06-12 11:39 EEST

### TODO-scalp-horizon-mismatch
- **issue:** Crypto scalp playbook flags a structural TP1/horizon mismatch (TP1 ~1.86R vs typical captured MFE 0.54R; PF 0.14, 1W/7L 14d) — entry edge exists but capture is capped.
- **evidence:** `data/reports/scalp/2026-06-12_06-57_scalp_report.md` header + per-idea "Known failure mode".
- **suggested manual fix:** consider a closer TP1 / partial-take rule for scalp, or re-audit at 20 closed A/B scalp signals as noted.
- **priority:** low
- **first observed:** recurring; logged again 2026-06-12 11:39 EEST

### TODO-kol-placeholder
- **issue:** KOL/crowd watchlist still contains the placeholder account; X/Telegram/Discord crowd context not live (social attention = "no symbol-level hits").
- **evidence:** scalp/intraday §4 "KOL watchlist still contains the placeholder account; replace it with trusted sources."
- **suggested manual fix:** replace placeholder KOL accounts with trusted curated sources to activate the social-attention signal.
- **priority:** low
- **first observed:** recurring; logged again 2026-06-12 11:39 EEST
