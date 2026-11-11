# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:40 EEST

## 1. Executive Summary

**Tuesday 2026-06-16, 04:40 EEST "crypto overnight / Asia review" slot.** Stocks are **closed** (01:40 ET) → crypto is the live actionable class; stocks are carry-forward/planning only. External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch verified BTC ~$66.3–66.5K and the BlackRock BITA ETF / FOMC calendar).

**Crypto stays risk-on but range-capped and pre-FOMC.** BTC **~$66.3–66.5K** (briefly tagged $67.2K, still pinned under the **$67.5K** band; support $64K / $61.8K), ETH **~$1.80–1.81K**, both uptrending; alt breadth **78.7% > EMA20** (scalp 01:30 read). Two dated events frame today: **BlackRock's BITA Bitcoin-income ETF debuts on Nasdaq today** (fresh positive BTC catalyst, mapped) and the **FOMC meeting starts today (Jun 16), decision tomorrow (Jun 17)** → expect consolidation/data-watch into the print. The US–Iran ceasefire / Strait-of-Hormuz narrative that drove the 2-day rally is intact and **no re-escalation headline printed in the last 4h** (the Israel–Hezbollah headline from the prior review has aged out of the window) — but it remains a headline-dependent tail risk.

**Routing — longs-only, RS-leader pullback + breakout-confirmed; no fresh shorts.** This is firmly evidenced, not a vibe: crypto week stats (A/B n=194) show **shorts 1W/7L, PF 0.43, −4R** and **breakdowns PF 0.43, −4R**, while **breakouts are 4W/0L, +8R** and **longs are breakeven (PF 1.0)**; Binance-confirmed signals are the best lane (PF 1.087, +2R). In a clean uptrend, shorting bleeds — route to RS-leader longs on pullback, demand a defended higher low + BTC holding >$64K, and prefer breakout confirmation over chasing.

**No A-tier crypto** in scalp or intraday — all live ideas are B-tier LONG continuation/pullback (scores 65–69), and the **scalp lane stays research-grade only (PF 0.14, low_confidence overlay)**. The clean overnight long-watch is the **AI / RS-leader cohort — NEAR (ai_narrative basket primary), plus GPS / ZEC / WLD** — pullback-only. **Avoids:** **ZRO** (RS leader but into a confirmed **$23M LayerZero token unlock** — supply/sell-the-news headwind, even though it's an active triggered signal), **JTO (+28–34%) / SPCXB (+25.7%, vol 6.11×, tagged overextended)** chase-risk, **UNH** (active DOJ Medicare-fraud probe — legal AVOID), and **fresh shorts**.

**Integrity improved overnight:** `detect_untracked_legacy_alerts --since 2026-06-16` = **0** (yesterday closed at 10). Early-day zero is encouraging but not yet a confirmed fix of the PART-1 regression — re-logged as a lower-urgency §14 watch. **Catalyst mapping weak this run (76.8% unmapped)** — use the catalyst layer as context, not final decision. **Advisory only. Scanner / collection / tracking continue in all moods — nothing here says stop the system.**

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-16_01-38_scalp_report.md` — mtime **04:38 EEST** → **FRESH** (data freshness 01:30 UTC).
- **Crypto intraday report** `data/reports/intraday/2026-06-15_23-15_intraday_report.md` — mtime **02:15 EEST** → **carry-forward** (~2h25m, <4h; flagged §3).
- **Crypto swing report** `data/reports/swing/2026-06-15_14-49_swing_report.md` — mtime **17:49 EEST** → **carry-forward** (~11h, 4–12h band; used, flagged §3).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-15_23-23_stocks_intraday_report.md` (mtime 02:23) + **swing** `…15-02…` (18:02) + **invest** `…15-08…` (18:08) — US **closed** → planning/carry-forward context only.
- **Catalysts** `data/catalysts/2026-06-16/` — generated this run via allowed `catalyst-scan --no-print` (dir was missing): `catalyst_cycle_01-43.md` (474 rows), `catalyst_events.jsonl`, `narrative_baskets.jsonl` (4 baskets).
- **LLM packets** `data/processed/llm_analysis_packet.md` (04:38, crypto) + `llm_stocks_packet.md` (02:23, stocks).
- **Internal CLI:** `active-signals` crypto (34 active, all long B) + stocks (50 active, A-tier AMD 88 / SMH 82 / JPM 80 carry-forward); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-16` → **0 untracked**.
- **DB** `db/crypto_ai_desk.sqlite` — `news_items` total **14,192**. §F priority-6 `t.me` last-4h = **9 items** (all lookonchain — welcomes + James Wynn gold/HYPE + OTC-whale ETH sell); **no fresh single-symbol crypto catalyst that changes a candidate.** Legal/hack/unlock keyword sweep (24h): ZRO unlock, IMX Aztec exploit (old), Huobi UK sanctions, Tether $72M freeze — none new vs prior beyond ZRO.
- **External:** WebSearch ×2 (BTC level Jun 16; overnight crypto news) + WebFetch (Fortune BTC page → $66,521.59, +3.51%).
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-16T0440Z.json` (3 cited sources); ingest CLI run for crypto (see §10).

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-15_default_schedule/`.
- `scheduler.log` mtime **04:38:22 EEST** (~2m old) → **FRESH**.
- Latest cycle summary `cycle_06_01-54_summary.md` mtime **02:24:25 EEST** (~2h16m old) → **fresh** (< 3h).
- **Both under the 3h defer threshold → review proceeds.**
- Freshness labels: scalp **fresh**; crypto intraday **carry-forward (~2h25m)**; crypto **swing carry-forward (~11h, 4–12h band — used, flagged)**; stocks reports = US closed → planning only. No hard stale exclusions, but the **scalp `waiting_for_entry` batch (ZEC/ZRO/JTO/ETH/BABY/XLM/WLD/INJ) all show `expires_at 03:38` → already EXPIRED ~1h ago** (these are the 01:38-cycle signals; the fresh 04:38 scalp batch had not yet surfaced in the active-signals snapshot — minor ingestion-lag, noted §14).

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-15_2324.md` (post-close final daily review):

- **Window moved from post-close → overnight/Asia.** Posture shifts from "book the day / set overnight plan" → **"work the overnight crypto tape into Europe."** Stocks remain closed (as planned for tomorrow's RTH).
- **Macro character unchanged but now pre-FOMC.** BTC essentially flat overnight (~$66.5K → ~$66.3K), still capped under $67.5K. **New framing element:** FOMC starts today / decision tomorrow → a data-watch ceiling on risk appetite that was not the operative driver at 23:24. **BITA ETF launch is now "today," not "tomorrow"** (was flagged as next-day catalyst in the prior run).
- **Geopolitical re-escalation risk cooled** — the Israel–Hezbollah rocket headline that was fresh at 23:24 has aged out of the 4h window; no new re-escalation headline overnight. Still a live tail risk, lower immediacy.
- **Integrity improved:** untracked legacy alerts **10 (end of Mon) → 0 (today, --since 2026-06-16)**. Encouraging but it's a fresh-day reset, not a verified fix.
- **Candidate cohort stable:** NEAR / GPS / ZEC / WLD remain the RS-leader long-watch; **ZRO AVOID re-confirmed** (token unlock); **UNH AVOID re-confirmed** (DOJ probe); JTO/SPCXB overextension flagged again.
- **Catalyst mapping still weak** (76.8% unmapped today vs >50% all of yesterday) — recurring §14 TODO.

## 5. Catalyst Coverage

- This run (`catalyst_cycle_01-43.md`): **474 events scanned, 4 narrative baskets.** Type mix: other_news 458, regulatory_sector_headline 4, partnership 3, legal_risk 3, analyst_action 1, buyback_burn 1, exploit_hack 1, product_launch 1, platform_growth 1, rumour_only 1.
- **Mapped (non-null symbol): 110 / 474. Unmapped: 364 / 474 = 76.8%.**
- **⚠ Catalyst mapping weak this run — use the catalyst layer as context, not final decision.**
- **Top 3 unmapped (by importance, all macro/sector noise):** (1) "One Indicted Over Crypto 'Wrench Attack' in France" (Decrypt, 0.68); (2) "Hyperbridge relaunches with decentralized overhaul after April exploit" (AMBCrypto, 0.68); (3) "Lawmakers face tight deadline to resolve issues for Clarity Act before July 4" / "Congress moves to rebuild crypto crime task force" / "CFTC hires SEC crypto task-force adviser" (CryptoBriefing/CryptoSlate/Cointelegraph, 0.62).
- **Narrative baskets:** **ai_narrative** (NEAR/RENDER/TAO/FET + WLD/ASTER — related_beta_rotation, single_source, <6h); **perps_dex_narrative** (HYPE + DYDX/GMX/ASTER — wait_pullback, <1h); **binance_ecosystem_teaser** (BNB/ASTER — sell-the-news risk, <24h); **momentum_breakout** (SPCXB/XLM/ZEC — pure momentum, no confirmed catalyst, wait_pullback).
- **Legal/regulatory flags from the catalyst layer:** **SMCI** (export-control indictment, SEC EDGAR 8-K — not in active stock signals), **UNH** (DOJ criminal Medicare-fraud probe — active C-tier long, AVOID), basket "Wrench Attack" indictment (France, macro). Note: SMCI/UNH are surfaced as `…/USDT` rows — a symbol-resolver quirk (stocks mislabelled as crypto pairs), part of the catalyst-mapping TODO.

## 6. Market Landscape

- **Crypto:** bullish trend / risk-on, range-capped, pre-FOMC. BTC + ETH uptrend; alt breadth **78.7% > EMA20 / 83.0% > EMA50** (scalp 01:30), BTC ATR percentile **29 (normal/low vol)**. **BTC ~$66.3–66.5K into $67.5K resistance**, support $64K / $61.8K; ETH ~$1.80–1.81K. Funding broadly neutral, crowding normal-to-low across leaders; several leaders show **OI-down-on-price-up = short-covering (weaker continuation quality)** (BABY). Strongest RS (scalp): SPCXB 91.6 (+25.7%, vol 6.11×, **overextended**), GPS 91.6, ZRO 91.6, JTO 91.5 (+28.7%), BABY 87.2, XLM 87.1, ZEC 86.8, WLD 84.5; NEAR +14% (ai_narrative). Weakest: OPG −44% (blow-up, neg funding, thin), RIF −22/−25%, STG −13%, GENIUS −8/−11%, EDEN −7/−9%.
- **Stocks (closed):** carry-forward. A-tier cluster in **semis/AI — AMD 88.8, SMH 82.4, JPM 80.9**; AMD appears across every mode (B 77.4, C-intraday 97.5, C-invest 71, C-swing 75.2). Week stats: **longs PF 1.095 (+2R), shorts PF 0.625 (−18R)**, swing best (PF 1.05, +1R), intraday worst (PF 0.66, −17R), A-tier n=5 all open (0 closed). These stock A/B expire ~14:32 EEST today — **before the 16:30 EEST US open → they expire pre-open and are stale planning context, not live.**

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:** **risk-on but range-capped + pre-FOMC** ($67.5K ceiling, FOMC decision tomorrow, headline-dependent rally).
- **Stocks mood:** **closed** (was risk-on into Mon's bell; overnight gap risk) — plan tomorrow's RTH.
- **Dominant narrative:** US–Iran peace deal / Strait-of-Hormuz reopen → oil down → risk-on; **AI / RS-leader rotation** in alts (NEAR/TAO/RENDER/FET + WLD); **BlackRock BITA BTC-income ETF debuts today** as an institutional BTC tailwind.
- **Preferred side now:** **longs / wait-for-pullback** (RS-leader + breakout-confirmed); **no fresh shorts** (risk-on + short −4R / breakdown −4R history).
- **Best long candidate:** **NEAR** (ai_narrative basket primary, RS leader) — long-watch on a defended pullback, BTC-gated >$64K; cohort alternates GPS / ZEC / WLD.
- **Best short candidate:** **none clean** — risk-on disfavours shorts; weakest names (OPG −44%, RIF, STG) thin/squeeze-prone. Short-watch only **after a failed retest of broken support AND BTC losing $64K.**
- **Best catalyst-backed candidate:** **BTC** itself (BITA ETF launch today) as the macro anchor — accept-above-$67.5K-on-volume; secondary **NEAR** (ai_narrative, single_source — wants a second source).
- **What to avoid:** ZRO (token unlock), JTO/SPCXB (overextended chase), UNH/SMCI (legal), crypto scalp lane (PF 0.14), fresh shorts.
- **What would change the view:** BTC **accepting above $67.5K on volume** (→ continuation) or **losing $64K** (→ flush toward $61.8K); **FOMC tomorrow** hawkish surprise (→ risk-off); a credible **geopolitical re-escalation** headline flipping the tape.

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — NEAR (crypto, RS-leader long-watch / ai_narrative basket primary)
- **Setup:** RS leader, +14% 24h, trend uptrend, risk-on regime; primary in the **ai_narrative** basket (related_beta_rotation). Active swing signal `tp1_hit` (entry was 2.436–2.462, invalidation 1h close < 2.405) — so the swing leg already paid TP1; the fresh idea is a pullback re-entry, not a chase.
- **Catalyst check (internal-first):** ai_narrative basket is **single_source, <6h**; 1 NEAR catalyst event today ("NEAR gains 14% — yet here's ONE warning traders can't ignore", AMBCrypto). No fresh independent confirmation.
- **Price/chase:** has price reacted? Yes (+14%) — so demand a **pullback, not a market buy**. Overextended? Less than JTO/SPCXB but watch >2 ATR from EMA20. Actionable now? **Only on a defended higher low with BTC holding >$64K** and volume on the retest. Mood-aligned: yes (risk-on RS-leader long). Invalidation: lose the pullback structure / BTC < $64K. Chase-risk: moderate. Catalyst confirmation: single_source only → wants a second AI-sector source.
- **Decision:** **overnight LONG-WATCH, pullback-only — best clean crypto long-watch into Europe.** Cohort alternates: GPS (91.6 RS, no catalyst), ZEC (momentum_breakout basket), WLD (ai_narrative related, +8–14%).

### Candidate 2 — ZRO (crypto, active intraday `triggered` B + scalp waiting) · TOKEN-UNLOCK CONTRADICTION
- **Setup:** RS leader (momentum 91.6, RS vs BTC +14–15%, +32% 7d). Active **intraday signal `triggered`** (entry 1.089–1.106), current price **1.114 → already slightly above entry** (mild chase if entered now).
- **Contradiction (material):** catalyst layer + `news_items` confirm a **$23M LayerZero token unlock** ("LayerZero rallies 14% ahead of $23mln token unlock", AMBCrypto, 2026-06-15) and ZRO appears in a "3 Token Unlocks to Watch" list. Supply headwind + classic sell-the-news. 7d +32% → extended; "move may be late vs EMA20/ATR."
- **Decision:** **AVOID-NEW / caution** despite being live and an RS leader — strong RS does not offset a known supply unlock + extension. Manage any existing exposure to invalidation; do **not** initiate fresh here. Re-assess only after the unlock clears and price holds a higher low.

### Candidate 3 — JTO / SPCXB (crypto, overextended momentum) · CHASE-RISK
- **Setup:** JTO momentum 91.5, **+28.7% 24h (intraday read +33.7%)**, RS vs BTC +27–33%; SPCXB 91.6, **+25.7% 24h, vol 6.11× (the only unusual-volume name), explicitly tagged `overextended`**. Both in/near the momentum cluster (SPCXB primary in `momentum_breakout`).
- **Price/chase:** price has reacted hard; both are **>2 ATR-type extended**; entry now would be **late**. No clean pullback structure yet. Catalyst: none verified (pure momentum). SPCXB futures data unavailable (thin/illiquid risk).
- **Decision:** **AVOID chasing / watch-for-pullback only.** JTO actionable only on a deep pullback into its zone (0.685–0.704 scalp) with continuation confirmation; SPCXB too thin/extended to touch. Mood-aligned direction (long) but execution timing is wrong — this is exactly the "don't chase extended movers overnight" case.

### Candidate 4 — AMD (stocks, A-tier 88.8 / B 77.4) · CLOSED — carry-forward, A-tier-overpromotion caveat
- **Setup:** best semis/AI technical name; A-tier 88.8 intraday (entry 542.67–549.26) but **US closed** → not live. Mirrors the crypto AI-rotation narrative (TAO/NEAR strength).
- **Contradiction check:** desk track record flags **stock A-tier longs as overpromoted (0% WR, n=5)** while the B-tier RTH-momentum lane is the clean one; the A-tier 88 also expires ~14:32 EEST (pre-open) → it's a stale carry, not tomorrow's signal.
- **Decision:** **PLANNING ONLY — tomorrow-RTH retest into ~539–545, B-grade not A-tier conviction, require first 15–30 min confirmation, no gap-chase.** Not an overnight action (stocks closed).

### Candidate 5 — UNH (stocks, active C-tier long, intraday + swing + invest) · LEGAL/HEADLINE RISK
- **LEGAL/HEADLINE RISK:** **confirmed active DOJ criminal Medicare-fraud probe, extended to Optum Rx; shares −16%** (catalyst layer QuiverQuant + prior-run TipRanks/Fierce Healthcare verification, 2026-06-15). No charges filed yet.
- **Decision:** **AVOID / MANUAL REVIEW REQUIRED — never a clean long** regardless of score. A momentum/RS read on a name under an active criminal probe is precisely the contradiction this section exists to catch. (Stocks closed anyway → not live, but flagged so it cannot become a clean actionable at the open.)

## 8. Best Candidates Ranked

Overnight/Asia window → crypto is live; stocks are plan-for-tomorrow. Leaders are extended → these are **pullback-only watches**, not market entries.

1. **NEAR (crypto long-watch)** — best clean crypto long-watch; *trigger: defended pullback / higher low with BTC holding >$64K and volume on the retest; bonus on a second AI-sector catalyst source.*
2. **GPS / ZEC / WLD (crypto RS-leader long-watch)** — same cohort, pullback-only; *trigger: defended higher low + BTC risk-on intact (>$64K), prefer breakout-retest confirmation.*
3. **AMD (stocks, plan-for-tomorrow)** — best semis/AI name; *trigger: tomorrow RTH retest ~539–545 after the open, B-grade, with SPY/QQQ not breaking down — not an overnight trade.*

**No clean fresh market entry exists right now (leaders extended + pre-FOMC + stocks closed), so per PART 9:**
- **best long-watch:** NEAR — trigger: defended pullback higher-low, BTC >$64K, volume on retest.
- **best short-watch:** none clean — trigger: a crypto RS-loser (OPG/RIF/STG) **only after a failed retest of broken support AND BTC losing $64K**; do not pre-empt shorts in a risk-on tape (short PF 0.43 / −4R).
- **best catalyst-watch:** BTC — trigger: **acceptance above $67.5K on volume** post-BITA-ETF launch (continuation); or NEAR ai_narrative confirmed by a second independent source.

## 9. Avoid / No Trade  (this decision window only — never "stop system")

- **ZRO** — $23M LayerZero token-unlock headwind + extended; AVOID-NEW (even though live/triggered).
- **JTO (+28–34%) / SPCXB (+25.7%, vol 6.11×, overextended, thin)** — chase-risk; pullback-only, no market entries.
- **UNH** — active DOJ criminal Medicare-fraud probe; AVOID / manual review.
- **SMCI** — export-control indictment (SEC EDGAR 8-K); AVOID (not in active set, flagged pre-emptively).
- **Crypto scalp lane** — PF 0.14, low_confidence overlay → **research-grade only**, not Telegram-actionable.
- **Fresh shorts (either class)** — risk-on tape + short −4R (crypto) / −18R (stocks) history.
- *(Decision-window guidance only. Scanner, candidate generation, tracking, and outcome recording continue overnight in all moods.)*

## 10. Main Risks

- **Pre-FOMC ceiling:** Fed decision tomorrow (Jun 17) → risk appetite likely capped / chop into the print; a hawkish surprise = fast risk-off. Don't over-size overnight.
- **BTC at $67.5K resistance with prior 7D ETF distribution** — a rejection + loss of $64K opens a flush toward $61.8K (thin overnight liquidity amplifies). BITA ETF launch is a tailwind but a single-source/new-product catalyst, not a guaranteed bid.
- **Geopolitical re-escalation** (Israel/Iran) — the 2-day rally rests on the peace narrative; a reversal headline flips risk-off quickly. Cooled in the last 4h but live.
- **Leaders extended:** JTO/SPCXB/ZRO are stretched; chasing into Asia thin books is the classic overnight trap.
- **Track-record fragility:** crypto A/B WR 15%, PF 0.92, −4R week; scalp PF 0.14. One trend day doesn't change weak base rates — stay disciplined, longs-only-with-confirmation.
- **§M ingest:** if the ingest CLI failed this run, cited sources may not be UPSERTed — see §10/§14; does not affect conclusions.

## 11. Action Plan — next 4 hours (overnight into Europe)

1. **Crypto, primary watch:** NEAR (and GPS/ZEC/WLD) — pullback-only long-watch; act only on a defended higher low with **BTC holding >$64K** and volume on the retest. No chasing extended leaders.
2. **BTC level discipline:** **$67.5K** = headroom trigger (accept-above-on-volume, BITA-ETF tailwind); **$64K** = risk line (loss → step back, expect $61.8K test). Size light into FOMC.
3. **Avoid overnight:** ZRO (unlock), JTO/SPCXB (extended), UNH/SMCI (legal). No fresh shorts.
4. **Stocks:** no overnight action (closed). Pre-stage **AMD tomorrow-RTH-retest** (~539–545, B-grade, confirm first 15–30 min, no gap-chase); keep UNH on the AVOID list so it can't become a clean open.
5. **Macro/geopolitics:** watch for any FOMC leak / re-escalation headline; if a credible risk-off catalyst prints, downgrade crypto longs to wait-and-flip routing (clean shorts only after failed retest + BTC < $64K).
6. **System:** scanner/collection/tracking continue. No stop, no config change.

## 12. Final Verdict per Mode

- **Crypto scalp:** research-grade only (PF 0.14, low_confidence). RS-leader pullback ideas exist (NEAR/GPS/ZEC/WLD) but low-confidence; the active waiting batch already expired (03:38) — no fresh Telegram-actionable scalp.
- **Crypto intraday:** longs-only, RS-leader + pullback, breakout-confirmed. NEAR/GPS/ZEC/WLD watch; ZRO triggered but AVOID-NEW (unlock). Overnight = wait-for-pullback, BTC-gated, light into FOMC.
- **Crypto swing:** carry-forward report (~11h); risk-on bias intact but capped at resistance — manage active (many tp1/tp2_hit), no fresh chase into extension/unlock (ZRO avoid).
- **Stocks intraday:** **closed** — AMD best long for tomorrow's RTH retest (B-grade), SMH semis-cohort caution, UNH AVOID (legal). No overnight entries.
- **Stocks swing / invest:** playbook-paused / planning context only.

## 13. Sources

- [Bitcoin News Today: BTC Jumps +3% as Trump Cancels Iran Strikes — Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/bitcoin-news-today-btc-jumps-090335706.html) (2026-06-15/16; BTC ~$66.3K, briefly $67.2K; FOMC Jun 16–17; ceasefire/Strait-of-Hormuz risk-on — single_source via WebSearch summary).
- [Current price of Bitcoin for June 15, 2026 — Fortune](https://fortune.com/article/price-of-bitcoin-06-15-2026/) (2026-06-15; BTC $66,521.59, +3.51% 24h — WebFetch verified).
- [Best Altcoins to Watch in June 2026 — Crypto.com](https://crypto.com/en/market-updates/best-altcoins-june-2026) (2026-06; BlackRock BITA ETF debuts Nasdaq Jun 16; AI tokens Bittensor/Render + RWA Ondo as BTC consolidates — single_source via WebSearch summary).
- Internal: `data/catalysts/2026-06-16/catalyst_cycle_01-43.md`, `narrative_baskets.jsonl`, `signal-stats` (crypto/stocks), `detect_untracked_legacy_alerts --since 2026-06-16`, `db/crypto_ai_desk.sqlite` (`news_items` n=14,192; t.me 4h sweep; ZRO unlock row 2026-06-15).
- ZRO token-unlock + UNH/SMCI legal flags corroborated internally (AMBCrypto/QuiverQuant/SEC EDGAR rows; UNH web-verified prior run 2026-06-15).

## 14. Fix Requests / TODO

### TODO-untracked-alerts-regression (downgraded — monitor)
- **issue:** Untracked legacy crypto alerts climbed 2→5→8→10 across Monday; today's `--since 2026-06-16` reads **0**. Improvement, but likely a fresh-day reset rather than a verified fix of the registration path.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-16` → "None"; contrast 23:24 review (10).
- **suggested manual fix:** confirm the watchlist-alert → proposed_signal registration writes a tracked `signal_id` for every Telegram-sent crypto B alert; re-check the count at the next 2–3 slots to confirm it stays clean under live alert flow before closing the PART-1 TODO.
- **priority:** medium (was high)
- **first observed:** 2026-06-15; re-evaluated 2026-06-16 04:40 EEST.

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-mapping ran **76.8% unmapped** this run (364/474), continuing yesterday's >50% pattern; stock tickers (SMCI/UNH) also surface as `…/USDT` pairs (resolver mislabels equities as crypto).
- **evidence:** `catalyst_cycle_01-43.md` (other_news 458/474); computed mapped=110/unmapped=364 from `catalyst_events.jsonl`.
- **suggested manual fix:** improve the symbol resolver / entity extraction (alias table, ticker disambiguation, equity-vs-crypto + macro-vs-symbol classifier).
- **priority:** medium
- **first observed:** 2026-06-15 (recurring; re-logged 2026-06-16 04:40 EEST).

### TODO-scalp-active-signals-expiry-lag
- **issue:** At 04:40 the fresh **04:38 scalp batch** was generated, but `active-signals` still showed the **01:38 scalp `waiting_for_entry` batch with `expires_at 03:38` (already expired ~1h)** — the new batch had not surfaced, so the active-signals view briefly shows only expired scalps.
- **evidence:** scalp report mtime 04:38 vs `active-signals --asset-class crypto` scalp rows all `expires_at 2026-06-16T03:38:10`.
- **suggested manual fix:** verify the scalp signal-persistence/ingestion step runs (and commits) before `active-signals` is queried, or confirm this is a benign few-minute lag between report render and DB upsert.
- **priority:** low
- **first observed:** 2026-06-16 04:40 EEST.

### TODO-stocks-A-tier-overpromotion (carry-forward)
- **issue:** Stock A-tier longs show **0% WR (n=5, all open)** while B-tier RTH-momentum is the clean lane; A-tier names (AMD/SMH 82–88) are carry-forward promotions that also expire pre-open (~14:32 EEST) → stale by the next RTH.
- **evidence:** `signal-stats --asset-class stocks` tier split (A n=5, 0 closed); active-signals expiry times.
- **suggested manual fix:** review A-tier promotion/expiry logic for stocks; gate A-promotion on catalyst confirmation and/or align expiry with the next RTH window.
- **priority:** medium
- **first observed:** 2026-06-15 (re-logged 2026-06-16 04:40 EEST).
