# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:27 EEST

_Generated 2026-06-17 ~16:27 EEST (13:27 UTC), ~3 min before the US cash open (16:30 EEST). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods. External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch-verified Yahoo tape)._

## 1. Executive Summary

**Wed 2026-06-17, ~16:27 EEST "pre-US-open decision review" slot — final read ~3 min before the 16:30 EEST (09:30 ET) cash open, ~4.5h before FOMC.** Two binaries frame the session: (1) the **US cash open** with **gap risk**, and (2) the **FOMC decision 21:00 EEST + Warsh presser 21:30 EEST** (2:00/2:30 PM ET) — a ~97%-priced hold where the move is the **dot plot + Warsh's first-meeting tone**. Fresh signal: **BofA survey shows 55% expect Warsh to strike a HAWKISH tone** ([thestreet 06-17](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-17-2026)). Offsetting risk-on tailwind: a **US-Iran peace deal** reopening the Strait of Hormuz. This is squarely a **wait-for-trigger / require-RTH-confirmation** window — **no naked directional size into the open or the print.**

**Crypto tape has COOLED vs the 11:30 slot — drifting from risk-on rotation toward chop/cautious-risk-off.** Desk now prints **BTC trend = transition_down**, regime range/chop, **altcoin breadth 56.8% > EMA20 (down from 60.9%)**, internal macro risk **91/100 (risk-off headwind)**. External tape confirms the slip: **BTC $64,644 (down from $65,605 open; lost the $65K shelf), ETH $1,764.79 (pulled back from the $1,843 rotation high)** as of 07:29 ET ([Yahoo 06-17, WebFetch-verified](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesdayjune-17-2026-much-higher-this-week-compared-to-last-114326169.html)). The 11:30 "lose $65K = bearish trigger" watch is now **triggered** — alt rotation is cooling, BTC is the drag.

**Best actionable read: no clean A/B trade this window.** Two **verified catalysts**: **UNI** (Standard Chartered $100 PT init; scalp 92.9, vol 3.64x; OI up + price up; price already reacted +22.5% yesterday → +6.9–8.5% 24h now) and — **[CORRECTED post-run]** **ASTER** (Token Buyback Program expansion). ASTER is **NOT a no-catalyst pump**: `news_items` carries *"Aster Expands its Token Buyback Program, Price Jumps 10%"* (BeInCrypto, 15:22 EEST, **detected_symbols=ASTER, importance 1.9 — the day's highest**). The catalyst layer FAILED to map it → `momentum_breakout` basket mislabeled ASTER "no confirmed news catalyst," and I compounded it by not verifying `news_items` directly (wrong column name, see §14). Correct read: ASTER is **catalyst-backed (buyback) but vol 52.24x / overextended → catalyst-backed long-WATCH on pullback, not a chase** (same routing as UNI), NOT "AVOID no-catalyst." ID/USDT persists as a no-catalyst RS leader with **crowded longs (negative funding, elevated external crowding)** → long-watch pullback only.

**Stocks: the 11:30 JPM A-tier has DROPPED OFF** — the fresh 12:58 stocks intraday report prints **"No A/B-tier setups in this run"** and JPM is no longer even in the watchlist. Regime is still **bullish** (VIX 16.28, breadth 100%, semis/tech leading), S&P futures **mixed-to-higher** into the Fed, but everything is demoted to **planning / C-tier watchlist**. With **gap risk + a hawkish-skewed FOMC tonight**, the discipline is **wait for the first 15–30 min of RTH to confirm, ideally post-FOMC** — do NOT chase the pre-market. **UNH (DOJ Medicare-fraud probe, −16%)** and **SMCI (export-control indictment 8-K)** remain verified legal overhangs → **AVOID**; both are correctly held `no_trade`/rejected by the system.

## 2. Data Used

- **Crypto scalp** `data/reports/scalp/2026-06-17_12-35_scalp_report.md` — generated 15:35 EEST (~0.9h) → **FRESH** (data 12:30 UTC).
- **Crypto intraday** `data/reports/intraday/2026-06-17_12-46_intraday_report.md` — generated 15:46 EEST (~0.7h) → **FRESH**.
- **Crypto swing** `data/reports/swing/2026-06-17_13-15_swing_report.md` — generated ~13:15 EEST (~3.2h) → **fresh/borderline carry-forward** (<4h).
- **Stocks intraday** `data/reports/stocks/intraday/2026-06-17_12-58_stocks_intraday_report.md` — generated ~15:58 EEST (~0.5h), but a **pre-open snapshot** ("Market closed — planning/watchlist only").
- **Stocks swing** `…00-45…` + **invest** `…00-49…` (~15.7h) → **STALE (>14h)** — excluded from final swing/invest verdict, planning context only.
- **Catalysts** `data/catalysts/2026-06-17/`: `catalyst_cycle_12-47.md` (392 events, 5 baskets), `catalyst_events.jsonl` (2,155 cumulative rows), `narrative_baskets.jsonl` (5). Folder present + fresh → no catalyst-scan CLI needed.
- **LLM packets** `data/processed/llm_analysis_packet.md` + `llm_stocks_packet.md` present.
- **Internal CLI:** `active-signals` crypto (**32 active, all long B**, scores 65–76) + stocks (**50 active, all C** — market-closed demotion; AMD swing 84, XLF/JPM intraday 82–83 screen-tier but not actionable); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-17` → **None (clean)**.
- **DB** `db/crypto_ai_desk.sqlite`: telegram-source rows last 4h = **28** (Lookonchain-class flow noise, no actionable t.me symbol news). (Note: `detected_symbols` column absent in this schema — 24h per-symbol mention counts not re-derived this run; relied on catalyst layer + reports.)
- **External:** WebSearch ×2 (BTC/ETH pre-open tape; S&P futures + FOMC); **WebFetch** verified Yahoo BTC/ETH article (open). thestreet article 403 on fetch → search snippet retained, labeled single_source.
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-17T1327Z.json`; ingest result in §13.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-17_default_schedule/`.
- `scheduler.log` mtime **16:15 EEST** (~12 min) → **FRESH**.
- Latest `cycle_*_summary.md`: `cycle_01_12-30_summary.md` mtime **13:17 EEST** (~3.2h).
- **Defer rule needs BOTH log AND latest cycle > 3h. Log ~0.2h → review proceeds.**
- Crypto scalp/intraday FRESH (<1h); swing ~3.2h (borderline). Stocks intraday a fresh pre-open snapshot. **Stocks swing + invest STALE (~15.7h) → excluded from final verdict.** No untracked-alert anomaly.

## 4. What Changed vs Previous Review

Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-17_1130.md` (Europe / pre-US context slot).

- **Clock advanced into the decision window:** FOMC moved from ~9.5h out to **~4.5h out (21:00 EEST)**; US cash open is now imminent (16:30 EEST). New: **BofA 55% expect a hawkish Warsh tone**; **US-Iran peace / Strait of Hormuz** added as a risk-on offset.
- **Crypto cooled / risk slipped:** BTC **$66K → $64,644**, **lost the $65K shelf** (11:30's bearish trigger now hit); trend **range → transition_down**; breadth **60.9% → 56.8%**; ETH **$1,843 → $1,765** (rotation leg fading). Mood downgraded **risk-on-coiled → chop / cautious-risk-off**.
- **UNI:** promoted from 11:30 "catalyst-watch (not on desk)" to **desk RS leader** (scalp 92.9, vol 3.64x; OI+price up) — but the Standard Chartered catalyst is now ~1 day old and **price has reacted** → still watch-on-pullback, not a fresh trigger.
- **NEW mover — ASTER/USDT:** **vol 52.24x**, score 100 intraday, +10.6%, overextended, **no catalyst** → joins the no-catalyst chase-trap list (with ID/SENT-type names).
- **ID/USDT:** still RS leader but **volume cooled (0.57–0.69x)** and **funding negative + crowding elevated** on external venues → crowded-long, lower-quality continuation.
- **Stocks: JPM A-tier (11:30) → REMOVED.** Fresh 12:58 report prints "No A/B-tier setups"; JPM not in watchlist. All stocks demoted to C/planning. Regime still bullish.
- **Unchanged integrity:** **UNH DOJ probe → still AVOID**; **SMCI indictment → still rejected**; untracked-legacy-alert detector still **clean (0)**.
- **Confirmed:** "chasing no-catalyst extended momentum is the day's repeat trap" → re-confirmed (ASTER 52x vol no-news; ID crowded).
- **Invalidated:** the 11:30 "risk-on rotation leg" thesis is **fading** — BTC under $65K + breadth slipping argue the rotation was pre-event positioning, not a trend.

## 5. Catalyst Coverage

- **This cycle (`cycle_12-47`):** 392 events scanned, types: other_news 373, partnership 6, earnings_event 3, low_liquidity 3, **legal_risk 3**, regulatory 2, analyst_action 1, product_launch 1.
- **Cumulative today:** `catalyst_events.jsonl` 2,155 rows; **mapped (symbol-tagged) ≈ 439 / 2,155 ≈ 20.4%; unmapped ≈ 79.6%.**
- **Narrative baskets: 5** — `perps_dex_narrative` (HYPE; related DYDX/GMX/ASTER, wait_pullback), `delisting_thin_liquidity` (avoid_low_liquidity; World-Cup fan-token noise), `rwa_narrative` (ONDO/XLM), `ai_narrative` (NEAR/RENDER/TAO/FET; +WLD/ASTER), `momentum_breakout` (ID/BIO/ASTER, fresh <1h, wait_pullback).
- ⚠️ **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Unmapped >50% (recurring; §14 TODO).
- Top-3 unmapped headlines: (1) *"White House's Anthropic move reignites AI debate in Congress"*; (2) *"US State Department steps in to help Vozinha's mother attend World Cup…"*; (3) *"Circle showcases AI agent's wallet capabilities with USDC transactions."*
- Verified mapped legal flags (top importance): **SMCI** (0.77, export-control indictment 8-K, SEC EDGAR), **UNH** (0.73, DOJ Medicare-fraud probe, QuiverQuant). Both correctly route to avoid/rejected.

## 6. Market Landscape

BTC has slipped under $65K into the cash open while the morning's alt rotation (UNI/ETH) cools — a **de-risking-into-FOMC** tape, not a fresh trend. Crypto breadth is softening (56.8%) and internal macro reads risk-off (91/100). US stocks screen **bullish** (4/4 indices up, VIX 16.28, semis/tech leading) and futures are mixed-to-higher, but the cash session hasn't opened, there are **no A/B setups**, and a **hawkish-skewed FOMC** lands tonight. Gap risk + event risk dominate; the edge is in **confirmation, not anticipation**.

### Market Mood / Risk Routing      (REQUIRED)
- **Crypto mood:**           **chop / cautious-risk-off** (BTC transition_down, lost $65K, breadth 56.8%, macro 91/100) — pre-FOMC coil
- **Stocks mood:**           **bullish regime but pre-market / pre-FOMC** → planning; futures mixed-to-higher; gap + event risk
- **Dominant narrative:**    **pre-FOMC de-risking** — BTC slips under $65K while the UNI/ETH alt rotation fades; AI + perps-DEX baskets secondary; US-Iran peace deal a risk-on offset; hawkish-Warsh skew the swing factor
- **Preferred side now:**    **wait-for-trigger** / require RTH + post-FOMC confirmation; catalyst-backed RS-leader longs **only on pullback**; **no naked size into the open or the 21:00 print**
- **Best long candidate:**   none clean now — **catalyst-backed long-watch UNI/USDT** on a pullback (do not chase post-reaction); RTH-independent but caution into FOMC
- **Best short candidate:**  none clean — **short-watch ZRO/USDT** (weakest, −14.5%, RS −12.4%) **only on a failed retest**; caveat: already overextended-down + squeeze risk if BTC bounces post-Fed
- **Best catalyst-backed candidate:** **UNI/USDT** (Standard Chartered $100 PT) and **ASTER/USDT** (buyback-program expansion, importance 1.9) — both watch on pullback; price already reacted
- **What to avoid:**         **ID** (crowded longs, no catalyst) chase-trap; **ASTER** at 52x-vol overextension (catalyst real but don't chase the blow-off); **UNH** (DOJ probe); **SMCI** (indictment); chasing pre-market without RTH; naked size into FOMC
- **What would change the view:** **FOMC 21:00 + Warsh presser 21:30**; **BTC reclaim >$65.5K** (bullish) or **lose $64K** (deeper bearish); first 15–30 min RTH confirmation post-open

## 7. Candidate Deep Dives

### Candidate 1 — UNI/USDT (crypto, best catalyst-backed) — LONG-WATCH ON PULLBACK
- **Source:** scalp strongest score **92.9** (24h +8.45%, RS +11.03%, **vol 3.64x**); intraday score 78.8 (RS +9.25%); derivatives "price up + OI up: fresh positioning confirms trend"; external bybit funding slightly negative (−4.2e-05), crowding normal.
- **Internal-first catalyst:** **VERIFIED** — Standard Chartered initiated UNI coverage with a **$100 PT (by 2030)**, drove +22.5% to ~$3.53 yesterday ([CoinDesk 06-17](https://www.coindesk.com/markets/2026/06/17/uniswap-jumps-22-and-altcoins-rip-while-bitcoin-stalls-before-the-fed)). Catalyst real but ~1 day old.
- **Price reaction / chase:** **price already reacted hard** (the +22.5% leg was yesterday; now consolidating +6.9–8.5% 24h). OI+price up is constructive but entering now ≈ chasing a day-old catalyst into a cooling tape + pre-FOMC.
- **Mood alignment:** the only verified-catalyst RS leader → best-quality long idea, **but** crypto mood is cooling and BTC lost $65K → wait for a pullback that holds.
- **Actionable now?** No — **catalyst-backed long-watch: trigger = pullback that holds with volume (don't chase the post-init candle); invalidation = loss of the breakout base / BTC breaking down through $64K.** Crypto trades 24/7 so not RTH-gated, but keep size small into the 21:00 print.

### Candidate 2 — ASTER/USDT (crypto, loudest new mover) — CATALYST-BACKED LONG-WATCH ON PULLBACK  [CORRECTED post-run]
- **Source:** intraday strongest score **100**, 24h +10.6%, RS +12.97%, **volume 52.24x** (tags: relative_strength, volume_expansion, breakout, **overextended**); member of `momentum_breakout` + `perps_dex` related baskets.
- **Internal-first catalyst:** **VERIFIED — Token Buyback Program expansion.** `news_items` row *"Aster Expands its Token Buyback Program, Price Jumps 10%"* (BeInCrypto, 2026-06-17 12:22 UTC / 15:22 EEST, `detected_symbols_json=["ASTER"]`, **importance 1.9**). External confirms a buyback-and-burn program (earlier stages up to ~80% of platform fees; June 17 expansion) — see Sources. _The original run wrongly logged "NONE verified": the catalyst layer left this event unmapped and the `momentum_breakout` basket labeled ASTER "no confirmed news catalyst," and the §G `news_items` per-symbol check was skipped due to a wrong column name (§14). This is the actual driver of the 52x volume + 24h move._
- **Price reaction / chase:** price has **already reacted** (+10% on the headline, 52x volume = late-stage parabolic). Catalyst is real but the easy move is in → entering at 52x-vol extension is still a chase.
- **Mood alignment:** catalyst-backed RS leader, but extended into a cooling, cautious-risk-off tape + pre-FOMC.
- **Actionable now?** No — **catalyst-backed long-WATCH on a pullback** (same routing as UNI), NOT a blanket avoid. Trigger = a pullback that holds with volume after the blow-off bases out; invalidation = loss of the buyback-breakout base / BTC breaking $64K. Do not enter at 52x-vol overextension.

### Candidate 3 — ID/USDT (crypto, RS leader, crowded) — LONG-WATCH (CHASE-RISK)
- **Source:** scalp 91.1 / intraday 90.5, 24h +18–20%, RS +20–22.5%, **volume cooled to 0.57–0.69x**; derivatives funding **−0.0064 to −0.0162** across mexc/bybit, **crowding elevated** on external venues.
- **Internal-first catalyst:** **NONE** — pure momentum (momentum_breakout basket).
- **Price reaction / chase:** strong 24h move already in; **negative funding + elevated crowding = crowded longs / squeeze-prone**, weaker continuation quality. Volume fading off the highs.
- **Mood alignment:** fits the RS-leader theme but no-catalyst + crowded + cooling tape = low quality.
- **Actionable now?** No — **long-watch on a pullback only**; do not add to crowded longs; invalidation = momentum failure / 1h close back into the pre-breakout range.

### Candidate 4 — Stocks pre-open (regime bullish, NO A/B) — PLANNING / WAIT-FOR-RTH + FOMC
- **Source:** stocks intraday 12:58 regime **bullish** (VIX 16.28, breadth 100%, SPY/QQQ/IWM/DIA uptrends; SMH +11.2% RS, XLK +5.4% RS); **§6 "No A/B-tier setups."** C-tier watchlist actionable: DIA/AAPL/XLY/TSLA/SPY (long), NFLX (short), COIN (long). **JPM A-tier from 11:30 has dropped off.**
- **Legal/headline (§I, every stock A/B):** **No stock A/B exists this run** → none to clear; for the flagged names: **UNH DOJ probe → no_trade (correct), SMCI indictment → rejected (correct).** Headlines: NFLX "slide getting worse" (consistent with the C-tier short bias, weakness not a legal flag); XLF "most overbought since 2020" (Bespoke — caution on financials longs); COIN "everything-exchange" (positive narrative).
- **Price reaction / chase:** can't confirm RTH structure pre-open; S&P futures mixed-to-higher into a **hawkish-skewed Fed** → **gap + event risk**.
- **Actionable now?** No — **planning only. Wait for the first 15–30 min of RTH (post-16:30 EEST) to confirm, ideally hold through the 21:00 FOMC.** Long bias intact at the index level; do not chase the pre-market gap.

### Candidate 5 — UNH (stocks, legal/integrity confirm) — AVOID
- **Source:** active C `wait`; catalyst layer flags **[legal_risk 0.73] UnitedHealth Faces DOJ Probe, Shares Dive 16% on Fraud Investigation** (QuiverQuant).
- **Legal/headline (§I):** **VERIFIED legal overhang** — DOJ Medicare-fraud probe, −16% move. Stocks intraday correctly holds UNH at **`no_trade` 36.44 (no_directional_setup).**
- **Actionable now?** **No — AVOID.** Correct system behavior; surfaced to confirm UNH never routes to a clean long while the probe is live. No integrity anomaly. (SMCI export-control indictment same treatment.)

## 8. Best Candidates Ranked

No clean actionable A/B this window (BTC under $65K + cooling crypto + pre-open stocks with no A/B + hawkish-skewed FOMC tonight). Per routing, best watch candidates + exact triggers:

1. **Catalyst-backed long-watch — UNI/USDT:** trigger = a pullback that **holds with volume** (don't chase the day-old Standard Chartered candle); invalidation = loss of breakout base / BTC breaks $64K. Best-quality long if the tape stabilizes.
2. **Short-watch — ZRO/USDT:** trigger = **confirmed failed retest** of resistance (currently −14.5%, RS −12.4%, overextended-down); abort if BTC reclaims $65.5K (squeeze). Lower conviction — already extended.
3. **Long-watch (chase-risk) — ID/USDT:** trigger = pullback only; do not add to crowded longs (neg funding, elevated crowding); invalidation = momentum failure.
4. **Planning — US stocks (index longs):** trigger = first 15–30 min RTH confirmation post-16:30 EEST + ideally post-FOMC clarity; bullish regime intact, no A/B yet.
5. **Catalyst-backed long-watch — ASTER/USDT [CORRECTED]:** buyback-program expansion (importance 1.9) drove the 52x-vol move; trigger = pullback that holds after the blow-off bases out; do not chase at extension. (Originally mis-ranked as no-catalyst avoid — see §14.)

## 9. Avoid / No Trade  (this decision window only — scanner always continues)

- **Chasing ID (crowded longs)** and other no-catalyst extended pumps — the day's repeat trap. **(NOTE: ASTER is catalyst-backed — buyback expansion, importance 1.9 — not a no-catalyst pump; it is a long-watch on pullback, only "avoid" at 52x-vol extension. Correction logged §14.)**
- **UNH** (active DOJ fraud probe) and **SMCI** (export-control indictment) — verified legal overhangs.
- **Chasing the US pre-market gap without RTH confirmation** — wait for the first 15–30 min after 16:30 EEST.
- **Naked directional size into the 21:00 EEST FOMC / 21:30 Warsh presser** — hold ~97% priced; dot-plot + tone binary; **55% expect a hawkish tone**; *"BTC dropped after 8 of 9 Fed meetings."*
- **Fresh ZRO short on a breakdown chase** (already overextended-down; squeeze risk).
- _This is a current-window routing, not a system stop. Scanning, candidate generation, tracking, and outcome recording continue._

## 10. Main Risks

- **FOMC tonight (21:00 EEST) + Warsh presser (21:30):** hawkish skew (BofA 55%) → risk-off; dovish dots → relief. Single largest risk; lands in the 21:30 slot.
- **US cash-open gap:** futures mixed-to-higher but pre-event; gap can fade or trap on the first prints.
- **BTC lost $65K:** the 11:30 bearish trigger is live; a break of $64K opens a deeper retest; alt rotation fades with it.
- **No-catalyst momentum reversion:** ASTER/ID thin/crowded, mean-revert before TP (scalp PF 0.14, B-tier triggered winrate 15% — low confidence).
- **Stale stocks swing/invest data (~15.7h):** excluded from final verdict; re-confirm on fresh cycle.
- **Catalyst mapping weak (~79.6% unmapped):** symbol-level catalyst layer is context-only this run.
- **Coverage gaps:** binance intraday OHLCV partial (scalp anchor fetched=0/failed=1); bybit failures; `detected_symbols` column absent → DB mention re-derivation skipped this run.

## 11. Action Plan — next 4 hours

1. **Do not initiate naked directional risk into the open or the FOMC.** Confirmation over anticipation.
2. **Crypto:** set alerts for **UNI pullback-that-holds** (catalyst-backed long-watch) and **ZRO failed retest** (short-watch). Watch **BTC $65.5K reclaim (bullish) / $64K loss (bearish)** as the regime trigger. Keep any size small ahead of 21:00.
3. **Avoid the chase:** ASTER (52x vol) and ID (crowded) — pullback-only, no entries at extension.
4. **Stocks:** index bias bullish but planning-only — **wait for first 15–30 min RTH (post-16:30 EEST) confirmation, ideally hold through the 21:00 FOMC.** Keep UNH/SMCI on avoid; note XLF overbought (Bespoke) and NFLX weakness.
5. **Re-check at the 18:30 US-open reaction slot** for which pre-open ideas confirmed/failed, gap traps, and any fresh legal/earnings headlines.

## 12. Final Verdict per Mode

- **Crypto scalp:** No clean trade. Low confidence; leaders extended/crowded/no-catalyst → watchlist only (UNI pullback).
- **Crypto intraday:** No clean A/B. Wait-for-trigger; catalyst-backed UNI long-watch on pullback or ZRO failed-retest short only on confirmation.
- **Crypto swing:** Fresh-ish (~3.2h); rotation cooling + pre-FOMC → no fresh size; reassess post-decision.
- **Stocks intraday:** Pre-open, **no A/B** (JPM dropped). Bullish regime = planning; wait RTH + FOMC. No actionable now.
- **Stocks swing / invest:** **STALE (~15.7h)** — excluded from verdict; planning only; re-confirm on fresh cycle.
- **Overall:** **Risk-routed wait-for-trigger / require-confirmation.** Best catalyst-backed long-watch UNI, best short-watch ZRO, avoid ASTER/ID chase + UNH/SMCI + FOMC-front-running. Scanner continues in all moods.

## 13. Sources

- [Yahoo Finance — Bitcoin & Ethereum prices today, Wed June 17, 2026 (WebFetch-verified)](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesdayjune-17-2026-much-higher-this-week-compared-to-last-114326169.html) — primary_source — BTC open $65,605 → $64,644 (07:29 ET), ETH $1,790.68 → $1,764.79; investors cautious into the Fed; US-Iran peace / Strait of Hormuz tailwind. **confirms** crypto cooling/BTC<$65K.
- [TheStreet — Stock Market Today, June 17, 2026: S&P futures edge higher ahead of Fed](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-17-2026) — single_source (HTTP 403 on fetch; search snippet) — Fed decision 2:00 PM ET, Warsh presser 2:30 PM ET, BofA 55% expect hawkish tone, US-Iran peace deal. **confirms** FOMC timing + hawkish skew.
- [CoinDesk — Uniswap jumps 22% and altcoins rip while bitcoin stalls before the Fed (06-17)](https://www.coindesk.com/markets/2026/06/17/uniswap-jumps-22-and-altcoins-rip-while-bitcoin-stalls-before-the-fed) — primary_source (carried from 11:30) — UNI +22.5% on Standard Chartered $100 PT init. **confirms** UNI catalyst (now ~1 day old).
- **[CORRECTED post-run] ASTER buyback catalyst** — internal: `news_items` "Aster Expands its Token Buyback Program, Price Jumps 10%" (BeInCrypto, 2026-06-17 12:22 UTC, detected_symbols=ASTER, importance 1.9). External corroboration: [Bitget — Aster launches sixth phase of buyback (up to 80% of fees)](https://www.bitget.com/news/detail/12560605180720), [AMBCrypto — ASTER wipes 77.8M tokens as buybacks hit $173M](https://ambcrypto.com/aster-wipes-77-8m-tokens-as-buybacks-hit-173m-can-price-reclaim-1/) — single_source; exact "99%" figure unconfirmed (search shows up to ~80% of platform fees in prior stages). **confirms** ASTER move is catalyst-backed (buyback), not no-catalyst.
- Internal: scalp/intraday/swing crypto reports, stocks intraday report (pre-open, no A/B), `catalyst_events.jsonl` (392 events this cycle / 5 baskets), `active-signals`/`signal-stats` CLI, `detect_untracked_legacy_alerts` (clean), `narrative_baskets.jsonl`.

## 14. Fix Requests / TODO

### TODO-aster-buyback-catalyst-dropped  [HIGH — concrete proof of catalyst-mapping loss]
- **issue:**            A high-importance, symbol-tagged catalyst in `news_items` was NOT propagated to `catalyst_events.jsonl` / narrative baskets, causing ASTER to be mislabeled "no confirmed news catalyst" in the `momentum_breakout` basket and (originally) routed to AVOID. The buyback-program expansion was the actual driver of ASTER's 52x volume + +10.6% move.
- **evidence:**         `db/crypto_ai_desk.sqlite` `news_items`: title *"Aster Expands its Token Buyback Program, Price Jumps 10%"*, source BeInCrypto, published 2026-06-17 12:22 UTC, `detected_symbols_json=["ASTER"]`, **importance 1.9** (day's highest). NOT present as a mapped ASTER event in `data/catalysts/2026-06-17/catalyst_events.jsonl`; `narrative_baskets.jsonl` `momentum_breakout` lists ASTER under "Top gainers without confirmed news catalyst." → news_items→catalyst_events→basket linkage is dropping symbol-tagged, high-importance rows.
- **suggested manual fix:** trace the catalyst-builder step that reads `news_items` and emits `catalyst_events`: why is a row with `detected_symbols_json=["ASTER"]` + importance 1.9 not surfacing as a mapped catalyst (time-window filter? symbol-normalization ASTER vs ASTER/USDT? dedup? per-cycle row cap?). Ensure high-importance symbol-tagged rows always map; the `momentum_breakout` basket should cross-check `news_items` before declaring "no confirmed news catalyst." This is the root of the recurring ~79.6%-unmapped figure (see below).
- **priority:**         high
- **first observed:**   2026-06-17 16:27 EEST (surfaced via user feedback post-run)

### TODO-newsitems-column-name-in-routine  [process — review routine]
- **issue:**            The review routine's §G internal-first per-symbol `news_items` check used the wrong column name (`detected_symbols`) and was abandoned after the error instead of inspecting the schema and retrying — directly contributing to the ASTER miss above.
- **evidence:**         actual column is `detected_symbols_json` (per `PRAGMA table_info(news_items)`); the wrong query returned `no such column: detected_symbols`. Correct check: `select title,importance from news_items where detected_symbols_json like '%ASTER%' order by published_at desc`.
- **suggested manual fix:** update the routine's documented SQL to `detected_symbols_json`; the §G internal-first check on EACH candidate (esp. any "no-catalyst momentum" symbol) must be mandatory and must not be silently skipped — never trust a basket's "no catalyst" label without the direct `news_items` lookup.
- **priority:**         high
- **first observed:**   2026-06-17 16:27 EEST

### TODO-catalyst-mapping-weak
- **issue:**            catalyst symbol-mapping ~20.4% mapped / ~79.6% unmapped (recurring across runs).
- **evidence:**         `data/catalysts/2026-06-17/catalyst_events.jsonl` — ~439 symbol-tagged of 2,155 cumulative rows.
- **suggested manual fix:** improve the symbol/entity resolver in the catalyst layer (headlines like "White House's Anthropic move…", "Circle/USDC…", World-Cup fan-token noise).
- **priority:**         medium
- **first observed:**   2026-06-17 11:42 EEST (recurring)

### TODO-crypto-b-tier-winrate
- **issue:**            crypto B-tier triggered winrate 15% (reliable, n=256) — flagged by signal-stats.
- **evidence:**         `signal-stats --asset-class crypto` → "(reliable, n=256) tier=B: triggered winrate 15% is low."
- **suggested manual fix:** manual entry-quality review of crypto B-tier (no auto-modify); inspect the no-catalyst momentum bucket (ASTER/ID-type).
- **priority:**         low
- **first observed:**   2026-06-17 11:42 EEST (recurring)

### TODO-stocks-c-tier-pf
- **issue:**            stocks C-tier PF 0.74 / winrate 9% and B-tier PF 0.75 / winrate 17% (below 0.8).
- **evidence:**         `signal-stats --asset-class stocks` observations (reliable n=263 tier=C; stronger n=36 tier=B).
- **suggested manual fix:** manual review of stocks C/B entry logic; keep C-tier watchlist out of headline but tracked.
- **priority:**         low
- **first observed:**   2026-06-17 11:42 EEST (recurring)

### TODO-weekend-signal-underperformance
- **issue:**            weekend crypto signals underperform (winrate 9%, n=22) per signal-stats.
- **evidence:**         `signal-stats --asset-class crypto` → "(weak, n=22) weekend=Y: weekend signals underperform."
- **suggested manual fix:** consider a weekend confidence/size de-rate in manual review (no auto-modify here).
- **priority:**         low
- **first observed:**   2026-06-17 16:27 EEST
