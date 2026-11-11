# Opus Enriched Review — EUROPE / PRE-US CONTEXT — Auto Cycle 11:30 EEST

_Generated 2026-06-17 ~11:42 EEST (08:42 UTC). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

## 1. Executive Summary

**Wed 2026-06-17, ~11:42 EEST "Europe / pre-US context" slot.** US cash market is **CLOSED** (opens 16:30 EEST) → stocks are pre-market / planning only; **crypto is the live actionable class.** External web research **AVAILABLE** this run (WebSearch ×3 + WebFetch-grade verification via CoinDesk/Yahoo/blockchainreporter).

**The one fact that frames the whole day: today is FOMC decision day.** The rate announcement lands **21:00 EEST (2:00 PM ET)** — **Kevin Warsh's first meeting as Fed chair**, with a hold ~97% priced (target 3.50–3.75%). The binary is the **dot plot + Warsh's tone**, not the rate. Dovish dots → BTC room toward $66–70K; hawkish → risk of a retest to $58–60K. History is a tail-risk warning: *"Bitcoin has dropped after 8 of 9 Fed meetings."* This 11:30 slot is therefore squarely **pre-event coil ~9.5h before the decision** → route to **wait-for-trigger / RS-leader-pullback longs**, **never** naked directional size into the print.

**Crypto regime: genuinely risk-on but range-bound and rotation-driven.** Desk prints **transition (mixed)** with BTC range / ETH uptrend, altcoin breadth 60.9% > EMA20. External tape confirms the rotation story: **BTC ~$65.8K flat (briefly $67.1K), ETH +10.9% to ~$1,843, UNI +22.5% to $3.53 after Standard Chartered initiated coverage ($100 PT by 2030)** ([CoinDesk 06-17](https://www.coindesk.com/markets/2026/06/17/uniswap-jumps-22-and-altcoins-rip-while-bitcoin-stalls-before-the-fed)). Capital is rotating **out of stalling BTC into alts** — but it's a **pre-event rotation, not a fresh trend leg.**

**Best actionable read:** there is **no clean A/B crypto trade this window.** The desk's loudest movers — **ID/USDT (+27–30% 24h, vol 2.86x), SENT, EPIC** — are RS leaders but **carry zero verified news (24h mention count = 0 each)** and are **>2 ATR extended → chase-risk, pullback-only watch.** The only **verified** catalysts sit in names the desk does **not** have an active long on: **UNI (Standard Chartered), ETH-rotation, HYPE (perps-DEX narrative, 16 mentions).** Treat those as catalyst-watch, not chase.

**Stocks:** lone A-tier is **JPM intraday long (active 80 / screening 82.6, regime bullish).** Legal/headline check is **CLEAN** — no fresh adverse news; JPM actually *won* the Tricolor dismissal (Jun 10), announced EU retail expansion (Jun 16), closed +3.27% Jun 16, analysts Buy (avg PT $337). But it is **pre-open + pre-FOMC**, and the fresh stocks report itself prints *"No A/B-tier setups in this run"* → **planning / RTH-confirmation only.** **UNH carries a verified DOJ Medicare-fraud probe (−16%)** and is correctly held `no_trade` — must never surface as a clean long.

## 2. Data Used

- **Crypto scalp** `data/reports/scalp/2026-06-17_08-20_scalp_report.md` — mtime 11:20 EEST (~0.4h) → **FRESH** (data 08:15 UTC).
- **Crypto intraday** `data/reports/intraday/2026-06-17_08-34_intraday_report.md` — mtime 11:35 (~0.1h) → **FRESH**.
- **Crypto swing** `data/reports/swing/2026-06-17_00-40_swing_report.md` — mtime 00:40 (~11h) → **carry-forward** (4–12h; flagged §3).
- **Stocks intraday** `data/reports/stocks/intraday/2026-06-17_06-00_stocks_intraday_report.md` — mtime 06:00 (~5.7h) → carry-forward; market closed → planning only.
- **Stocks swing** `…00-45…` (~11h) + **invest** `…00-49…` (~11h) — **carry-forward**, planning context (US closed pre-open).
- **Catalysts** `data/catalysts/2026-06-17/`: `catalyst_cycle_08-35.md` (mtime 11:35), `catalyst_events.jsonl` (1,469 raw rows / report cites **590 unique events**), `narrative_baskets.jsonl` (**5 baskets**). No catalyst-scan CLI needed (folder present + fresh).
- **LLM packets** `data/processed/llm_analysis_packet.md` + `llm_stocks_packet.md` present.
- **Internal CLI:** `active-signals` crypto (**41 active, all long B**, scores 65–76) + stocks (**50 active**; **JPM A 80 intraday triggered**, JPM/XLF/XLK/DIA B intraday, AMD swing C 84, NFLX shorts C, UNH C `wait`); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-17` → **None (clean)**.
- **DB** `db/crypto_ai_desk.sqlite` `news_items` 24h mention counts: **BTC 69, HYPE 16, ETH 15, UNI 9** (loud), JPM 1, UNH 1, WLD 1, **ID/SENT/EPIC/NEAR = 0** (no-catalyst momentum); telegram-source last 4h = 5 (Lookonchain-class noise, no actionable t.me symbol news).
- **External:** WebSearch ×3 (FOMC June 17 + BTC reaction; JPM legal/analyst; BTC/ETH/UNI pre-Fed tape). All loaded; CoinDesk 06-17 rotation article verified.
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-17T0842Z_crypto.json` + `…_stocks.json`; ingest result in §13.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-16_default_schedule/` (rolls across midnight).
- `scheduler.log` mtime **11:35:07 EEST** (~7 min) → **FRESH**.
- Latest `cycle_*_summary.md`: `cycle_08_08-17_summary.md` mtime **09:01:49 EEST** (~2.7h).
- **Defer rule needs BOTH log AND latest cycle > 3h. Log ~0.1h → review proceeds.**
- Crypto scalp/intraday FRESH (<0.5h). **Swing + all stock reports are carry-forward (~5.7–11h)** — used for planning, flagged; not treated as fresh confirmation. No stale (>14h) exclusion required.

## 4. What Changed vs Previous Review

Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-17_0445.md` (crypto overnight / Asia slot).

- **Macro frame unchanged but clock advanced:** FOMC is still the dominant event; it has moved from "later today" to **~9.5h out (21:00 EEST tonight)**. FOMC two-day meeting opened 06-16; decision today.
- **BTC:** ~unchanged, **mid-$65–66K, capped under $67K** (prior: $65.5–66K two-week high). Still range / pre-event coil.
- **ETH:** **upgraded read** — external tape now shows **ETH +10.9% intraday (~$1,843)**, the rotation leg is more pronounced than overnight.
- **Rotation catalyst sharpened:** overnight pick was **WLD (AI / Sam Altman)**; this morning the **verified** standout is **UNI +22.5% on Standard Chartered $100 initiation** (new, externally confirmed). WLD demoted to "ready-for-promotion" momentum_7d_leader, still active B swing.
- **New movers:** **ID/USDT** jumped to desk #1 momentum (score 100 intraday, +30% RS, vol 2.86x) — **new, no-catalyst, overextended.** SENT/EPIC persist as RS leaders.
- **Removed:** overnight WLD-as-#1-long thesis no longer the cleanest; no fresh verified catalyst on the desk's current momentum leaders.
- **Unchanged integrity:** JPM A-tier still carry-forward/planning; **UNH DOJ probe still active → still AVOID**; untracked-legacy-alert detector still **clean (0)**.
- **Confirmed:** "chasing no-catalyst momentum pumps is the day's repeated trap" (SENT/PORTAL overnight) → **re-confirmed** today (ID/SENT/EPIC, 0 mentions, >2 ATR).
- **Invalidated:** none materially; the contradictory "BTC panic <$73K" RSS artifacts remain stale noise, not current state.

## 5. Catalyst Coverage

- **Unique catalyst events today: 590** (report figure); raw JSONL rows 1,469.
- **Mapped (symbol-tagged): ~303 / 1,469 raw ≈ 20.6%; unmapped ≈ 79.4%.**
- **Narrative baskets: 5** — `perps_dex_narrative` (HYPE, wait_pullback), `rwa_narrative` (ONDO/XLM), `delisting_thin_liquidity` (avoid_low_liquidity), `ai_narrative` (NEAR/RENDER/TAO/FET), `momentum_breakout` (SENT/TIA, fresh <1h).
- ⚠️ **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Unmapped >50% (recurring; see §14 TODO).
- Top-3 unmapped headlines: (1) *"White House's Anthropic move reignites AI debate in Congress"*; (2) *"Circle showcases AI agent's wallet capabilities with USDC transactions"*; (3) *"In 6 Words, Fed Governor Lisa Cook Issued a Stark Warning to Wall Street."*
- Verified mapped legal flags carried in the structured layer: **SMCI** (export-control indictment 8-K), **UNH** (DOJ fraud probe). Both correctly route to avoid/rejected.

## 6. Market Landscape

BTC stalls under the $67K pivot while alts rotate (UNI, ETH, HYPE) — a classic **pre-FOMC risk-on-but-coiled** tape. Breadth is constructive (60.9% > EMA20) but volume on the crypto leaders is thin/extended, and the binary event is tonight. Stocks screen bullish (desk regime long/risk-on) but the cash session hasn't opened and also sits pre-FOMC.

### Market Mood / Risk Routing      (REQUIRED)
- **Crypto mood:**           risk-on but range-bound / **pre-FOMC coil** (rotation-driven)
- **Stocks mood:**           bullish regime (desk) but **closed / pre-market** → planning; pre-FOMC
- **Dominant narrative:**    pre-FOMC capital rotation **out of stalling BTC into altcoins** — UNI +22.5% (Standard Chartered $100 PT), ETH +10.9%, HYPE perps-DEX; AI narrative secondary
- **Preferred side now:**    **wait-for-trigger**; RS-leader **longs only on pullback**; no naked size into the 21:00 print
- **Best long candidate:**   none clean now — **long-watch EPIC/USDT** (RS leader, cleaner vol) on pullback 0.652–0.661, or **ID/USDT** only on a pullback (currently >2 ATR, chase-risk)
- **Best short candidate:**  none clean — **short-watch NEAR/USDT** failed-bounce 2.297–2.315 with stop above 2.337; caveat: counter-rotation + squeeze risk into risk-on tape
- **Best catalyst-backed candidate:** **UNI / ETH rotation** (verified Standard Chartered + ETH +10.9%) — watch-only, not in desk top setups; **HYPE** perps-DEX basket secondary
- **What to avoid:**         chasing no-catalyst extended pumps (**ID / SENT / EPIC**, 0 mentions, >2 ATR); **UNH** (DOJ probe); **SMCI** (indictment); naked directional size into 21:00 FOMC
- **What would change the view:** FOMC dot plot + Warsh tone at **21:00 EEST**; **BTC reclaim >$67K** (bullish trigger) or **lose $65K** (bearish trigger); a verified catalyst appearing on a desk RS-leader

## 7. Candidate Deep Dives

### Candidate 1 — JPM (stocks, A-tier intraday long) — PLANNING / WAIT-FOR-RTH
- **Source:** active-signals A 80 (triggered); stocks intraday screening **JPM long A 82.57**, regime bullish/long/risk-on.
- **Legal/headline (§I, REQUIRED):** **CLEAN.** No fresh adverse catalyst. JPM *won* dismissal of the Tricolor subprime-auto investor suit (Jun 10, Judge Rakoff); announced retail-banking expansion into France/Italy/Spain (Jun 16); stock +3.27% Jun 16; analysts Buy, avg PT $337 ([TradingKey 06-16](https://www.tradingkey.com/news/market-movers/261970991-market-movers-jpm-20260616)). Legacy Charlie Javice/Frank matters are old/known, not a fresh catalyst.
- **Price reaction / chase:** can't verify RTH structure (market closed); the fresh 06:00 stocks report itself prints *"No A/B-tier setups in this run"* → gating held it back pre-open.
- **Mood alignment:** aligned with bullish stocks regime, **but** pre-open + pre-FOMC.
- **Actionable now?** No — **planning only; require RTH confirmation after 16:30 EEST AND ideally post-FOMC clarity.** Long bias, not a clean entry this window.
- **Invalidation:** loss of the index/regime long bias, or a hawkish FOMC repricing risk-off.

### Candidate 2 — ID/USDT (crypto, best momentum / RS leader) — LONG-WATCH (CHASE-RISK)
- **Source:** intraday score 100, 24h +27.8%, RS vs BTC +30.1%, **vol 2.86x** (unusual_volume + breakout + **overextended** tags).
- **Internal-first catalyst:** **none** — `news_items` 24h mention = **0**; no catalyst_events match. Pure technical momentum.
- **Price reaction / chase:** **already reacted hard; >2 ATR from EMA20 → "do not chase"** (desk rejected the active long at score 41, converted to watchlist pullback-only). External funding negative on bybit (−0.02) → crowded longs / squeeze dynamic, weaker continuation quality.
- **Mood alignment:** fits risk-on rotation, but no-catalyst + extended + pre-FOMC = low-quality chase.
- **Actionable now?** No. **Long-watch only on a pullback into ~0.0297–0.0303**, invalidation 1h close < 0.0290. Don't enter >2 ATR extended.

### Candidate 3 — EPIC/USDT (crypto, RS leader, cleaner) — LONG-WATCH PULLBACK
- **Source:** scalp/intraday RS leader, 24h +15.9%, RS +18.1%, vol 0.85x (less extended than ID/SENT), external funding neutral, crowding low.
- **Catalyst:** **none verified** (mention = 0). RS-leader-without-catalyst → per playbook, prefer pullback + breakout confirmation.
- **Price reaction / chase:** less overextended than ID; desk gives a conditional pullback zone **0.652–0.661**, TP1 0.684, invalidation 1h close < 0.6417.
- **Mood alignment:** best-quality long-watch in the rotation if it pulls back; not a chase at 0.668.
- **Actionable now?** No — **long-watch; trigger = accept inside 0.652–0.661 with volume, not a breakout chase.**

### Candidate 4 — NEAR/USDT (crypto, best short-watch, weak RS) — SHORT-WATCH (SQUEEZE RISK)
- **Source:** weakest-symbol short bias, 24h −8.3%, RS −6.0%, AI-narrative member; `crypto_failed_bounce_short` playbook.
- **Catalyst:** none fresh (mention = 0); AI narrative is "mixed," not a clean bearish driver.
- **Price reaction / chase:** desk failed-bounce/retest zone **2.297–2.315**, invalidation 1h close > 2.337, TP1 2.249. Derivatives: deleveraging/long-liquidation; long/short still skewed long → **squeeze risk if BTC reclaims.**
- **Mood alignment:** **counter to the risk-on rotation** → only a short *after* a failed bounce, never a fresh breakdown chase into a pre-FOMC risk-on tape.
- **Actionable now?** No — **short-watch only on a confirmed failed retest of 2.297–2.315 with a stop above 2.337.**

### Candidate 5 — UNH (stocks, legal/integrity check) — AVOID (CONFIRM)
- **Source:** active C `wait`; structured catalyst layer flags **[legal_risk] UnitedHealth Faces DOJ Probe, Shares Dive 16% on Fraud Investigation** (QuiverQuant).
- **Legal/headline (§I):** **VERIFIED legal overhang** — DOJ Medicare-fraud probe, −16% move. Stocks intraday report correctly holds UNH at **`no_trade` 36.44 (no_directional_setup).**
- **Actionable now?** **No — AVOID.** This is correct system behavior; surfaced to confirm UNH never routes to a clean long while the probe is live. No integrity anomaly.

## 8. Best Candidates Ranked

No clean actionable A/B this window (pre-open stocks + pre-FOMC + no-catalyst crypto leaders). Per routing, the best watch candidates + exact triggers:

1. **Long-watch — EPIC/USDT:** trigger = pullback acceptance into **0.652–0.661** with volume; invalidation 1h close < 0.6417. Cleanest RS-leader-pullback long if it stops extending.
2. **Long-watch (chase-risk) — ID/USDT:** trigger = pullback into **0.0297–0.0303** only; never >2 ATR extended; invalidation 1h close < 0.0290.
3. **Short-watch — NEAR/USDT:** trigger = confirmed **failed retest of 2.297–2.315** with stop > 2.337; abort if BTC reclaims $67K (squeeze).
4. **Catalyst-watch — UNI / ETH (rotation):** trigger = verified-catalyst follow-through that the desk picks up as an RS-leader setup with a real entry structure; today it's watch-only (not in desk top setups).
5. **Planning — JPM (stocks A):** trigger = RTH confirmation after 16:30 EEST, ideally post-FOMC clarity; bullish bias intact, legal clean.

## 9. Avoid / No Trade  (this decision window only — scanner always continues)

- **Chasing ID / SENT / EPIC breakouts** while >2 ATR extended with **0 verified catalyst** — the day's repeat trap.
- **UNH** (active DOJ fraud probe) and **SMCI** (export-control indictment) — verified legal overhangs.
- **Naked directional size into the 21:00 EEST FOMC print** — Warsh's first meeting, dot-plot binary; *"BTC dropped after 8 of 9 Fed meetings."*
- **Fresh NEAR short on a breakdown chase** (squeeze risk into risk-on rotation).
- _This is a current-window routing, not a system stop. Scanning, candidate generation, tracking, and outcome recording continue._

## 10. Main Risks

- **FOMC tonight (21:00 EEST):** dovish dots → BTC $66–70K; hawkish → $58–60K retest. Single largest risk; lands during the 21:30 slot.
- **No-catalyst momentum reversion:** ID/SENT/EPIC thin-volume, extended; mean-revert before TP (scalp PF 0.14 / 1W-7L 14d — low confidence).
- **Data carry-forward:** swing + all stock reports 5.7–11h old; treat as planning, re-confirm on fresh cycle.
- **Coverage gaps:** bybit intraday OHLCV fetch = 0 (54 failures); social_attention missing; Reddit/SEC EDGAR/Reuters RSS failing; liquidation/orderbook/ETF-flow blindspots persist.
- **Catalyst mapping weak (~79% unmapped):** symbol-level catalyst layer is context-only this run.

## 11. Action Plan — next 4 hours

1. **Hold flat / watch into Europe → US pre-open.** No new naked directional risk ahead of FOMC.
2. **Crypto:** set alerts for **EPIC pullback 0.652–0.661** (long-watch) and **NEAR failed retest 2.297–2.315** (short-watch). Watch **BTC $67K reclaim / $65K loss** as the regime trigger.
3. **Catalyst-watch UNI/ETH/HYPE rotation** — only act if a desk RS-leader setup with a real entry forms; do not chase the rip.
4. **Stocks:** JPM long bias is planning-only; **wait for RTH (16:30 EEST) confirmation**, ideally post-FOMC. Keep UNH/SMCI on avoid.
5. **Re-check at the 16:20 pre-US-open slot** for gap/pre-market reactions and any fresh legal/earnings headlines on stock A/B.

## 12. Final Verdict per Mode

- **Crypto scalp:** No clean trade. Low-confidence regime; leaders extended/no-catalyst → watchlist only (EPIC/ID pullbacks).
- **Crypto intraday:** No clean A/B. Wait-for-trigger; RS-leader pullback long (EPIC) or failed-bounce short (NEAR) only on confirmation.
- **Crypto swing:** Carry-forward data; rotation constructive but pre-FOMC → no fresh size; reassess post-decision.
- **Stocks intraday:** Closed/pre-market. JPM A = planning, wait RTH + FOMC. No actionable now.
- **Stocks swing / invest:** Carry-forward, planning only; pre-FOMC.
- **Overall:** **Risk-routed wait-for-trigger.** Best long-watch EPIC, best short-watch NEAR, catalyst-watch UNI/ETH, avoid UNH/SMCI and FOMC-front-running. Scanner continues.

## 13. Sources

- [CoinDesk — Uniswap jumps 22% and altcoins rip while bitcoin stalls before the Fed (06-17)](https://www.coindesk.com/markets/2026/06/17/uniswap-jumps-22-and-altcoins-rip-while-bitcoin-stalls-before-the-fed) — primary_source — confirms BTC ~$66K flat, ETH +10.9%, UNI +22.5%/$3.53 on Standard Chartered $100 PT, rotation into alts.
- [StockTitan — Fed Rate Decision June 17, 2026: What to Watch](https://www.stocktitan.net/articles/fed-rate-decision-june-17-2026) — single_source — FOMC decision 2:00 PM ET, ~97% hold, dot plot + Warsh debut the focus.
- [CryptoTimes — Bitcoin Has Dropped After 8 of 9 Fed Meetings (06-16)](https://www.cryptotimes.io/2026/06/16/bitcoin-has-dropped-after-8-of-9-fed-meetings-will-today-be-different/) — single_source — historical FOMC-day BTC weakness; tail-risk context.
- [blockchainreporter — Bitcoin holds $66K as the Fed's big day arrives and Warsh takes over (06-16)](https://blockchainreporter.net/bitcoin-price-today-btc-holds-66k-as-the-feds-big-day-arrives-and-warsh-takes-over/) — single_source — BTC $66,340, FOMC opens under Warsh.
- [TradingKey — JPM moved up 3.27% on Jun 16 (06-16)](https://www.tradingkey.com/news/market-movers/261970991-market-movers-jpm-20260616) — single_source — JPM +3.27%, EU retail expansion, no fresh adverse legal news.
- Internal: scalp/intraday/swing reports, stocks intraday/swing/invest reports, `catalyst_events.jsonl` (590 events / 5 baskets), `active-signals`/`signal-stats` CLI, `news_items` mention counts (DB), `detect_untracked_legacy_alerts` (clean).

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak
- **issue:**            catalyst symbol-mapping ~20.6% mapped / ~79.4% unmapped (recurring across recent runs).
- **evidence:**         `data/catalysts/2026-06-17/catalyst_events.jsonl` — 303 symbol-tagged of 1,469 raw rows; report cites 590 unique events.
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (entity/ticker extraction for headlines like "White House's Anthropic move…", "Circle/USDC…").
- **priority:**         medium
- **first observed:**   2026-06-17 11:42 EEST (recurring)

### TODO-bybit-intraday-ohlcv-zero
- **issue:**            bybit OHLCV fetch = 0 with 54 failures in the intraday cycle (derivatives venue blind on intraday OHLCV).
- **evidence:**         `data/reports/intraday/2026-06-17_08-34_intraday_report.md` §0 — `bybit: ohlcv_fetched=0, failed=54`; scalp cycle bybit failed=11.
- **suggested manual fix:** investigate bybit OHLCV client/ratelimit/endpoint regression for the intraday timeframe.
- **priority:**         medium
- **first observed:**   2026-06-17 11:42 EEST

### TODO-crypto-b-tier-winrate
- **issue:**            crypto B-tier triggered winrate 15% (PF 1.08, n=258) — flagged by signal-stats observation.
- **evidence:**         `signal-stats --asset-class crypto` → "(reliable, n=258) tier=B: triggered winrate 15% is low."
- **suggested manual fix:** manual entry-quality review of B-tier crypto (no auto-modify); inspect no-catalyst momentum bucket.
- **priority:**         low
- **first observed:**   2026-06-17 11:42 EEST (recurring)

### TODO-stocks-c-tier-pf
- **issue:**            stocks C-tier PF 0.72 / winrate 9% and B-tier PF 0.75 / winrate 17% (below 0.8).
- **evidence:**         `signal-stats --asset-class stocks` observations (reliable n=263 tier=C; stronger n=36 tier=B).
- **suggested manual fix:** manual review of stocks C/B entry logic; watchlist C-tier excluded from headline but track.
- **priority:**         low
- **first observed:**   2026-06-17 11:42 EEST

### TODO-stocks-screening-vs-tradeidea-mismatch
- **issue:**            stocks intraday §5 screening lists JPM long **A 82.57** / XLF **B**, but §6 "Trade Ideas (A/B-tier)" prints "No A/B-tier setups in this run" — likely intended pre-open/penalty gating, but the display reads contradictory.
- **evidence:**         `data/reports/stocks/intraday/2026-06-17_06-00_stocks_intraday_report.md` §5 vs §6.
- **suggested manual fix:** confirm whether the screening-tier vs trade-idea-gating divergence is intended; if so, annotate the report so "A-tier screen ≠ actionable" is explicit.
- **priority:**         low
- **first observed:**   2026-06-17 11:42 EEST
