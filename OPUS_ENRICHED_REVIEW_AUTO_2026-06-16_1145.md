# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:45 EEST

## 1. Executive Summary

**Tuesday 2026-06-16, 11:45 EEST "Europe / pre-US context" slot.** US cash session is **closed / pre-market** (opens 16:30 EEST / 09:30 ET) → **crypto is the live actionable class; stocks are planning/watchlist only** until the open. External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch verified BTC **$66,304**, support 63.5–64.5K / resistance 67K, BlackRock BITA ETF launch, FOMC Jun 17).

**Crypto stays risk-on but range-capped and now pre-FOMC.** BTC **~$66.3K**, pinned under the **$67K** resistance band (support **$63.5–64.5K**, then $61.8K); ETH uptrending (~$1.80K region), SOL ~$74. Alt breadth **79.5% > EMA20 / 81.8% > EMA50** (07:30–07:44 reads), BTC ATR percentile **32 (normal vol)**. Three dated items frame the tape: (1) the **US–Iran peace accord is finalized and the Strait of Hormuz has reopened** → the multi-day risk-on rotation that drove the rally; (2) **BlackRock's iShares Bitcoin Premium Income ETF (BITA) launched on Nasdaq today** (institutional BTC tailwind); (3) **FOMC decision lands tomorrow, Wed Jun 17, 2:00pm ET — Kevin Warsh's first meeting** (hold expected at 3.50–3.75%, ~98% no-change, but a possible hawkish bias shift) → a data-watch ceiling on risk appetite into the print. Fear & Greed is **23 (still "fear")** despite the recovery from the $59,130 crash low.

**Routing — longs / wait-for-pullback; no fresh shorts (both asset classes).** Firmly evidenced, not a vibe: crypto **B-tier triggered winrate 16%** and **weekend signals 9%** (signal-stats); the **scalp lane stays research-grade only (PF 0.14, low_confidence overlay)**. On stocks, **longs PF 1.2 (+4R)** vs **shorts PF 0.5 (−19R, n=139)** — shorting bleeds in this risk-on regime. Route to RS-leader longs on pullbacks with confirmation; do not chase extended movers.

**No A-tier crypto** in scalp or intraday — all live crypto ideas are B-tier LONG continuation/pullback (scores 65–69). The cleanest crypto long-watch is **INJ** (the only unusual-volume name, momentum 96–98, +10.6%, vol 1.65–2.03×, RS leader) on a pullback, with **SOL** as the catalyst-backed alternate (ETF inflows + "new risk-on leader" narrative). Stocks carry three **A-tier signals — AMD 88.8 / SMH 82.4 / JPM 80.9 — but these triggered yesterday during RTH (2026-06-15 14:32 UTC, ~18h old) and expire ~11:32 UTC today, i.e. before the US open → stale planning context, NOT live entries.** AMD is the most catalyst-backed stock long (Citi Buy upgrade, ~$900B valuation, AI-semis rotation) and the top RTH-confirmation long-watch into the open.

**Key AVOID: UNH** — internal `news_items` (4 sources, Jun 15) confirm a **DOJ criminal Medicare-Advantage fraud probe extending to Optum Rx, shares −16%** → **AVOID** despite being an active C-tier long signal. **SMCI** carries an export-control indictment (8-K). **Integrity:** **1 untracked legacy crypto alert** reappeared (ETH/USDT B scalp, sent 08:37 UTC) — re-logged as §14 watch (was 0 at the 04:40 slot). **Catalyst mapping weak this run (77.0% unmapped)** — use the catalyst layer as context, not final decision. **Advisory only. Scanner / collection / tracking continue in all moods — nothing here says stop the system.**

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-16_07-30_scalp_report.md` — mtime ~10:30 EEST → **FRESH** (~1.2h; data freshness 07:15 UTC).
- **Crypto intraday report** `data/reports/intraday/2026-06-16_07-44_intraday_report.md` — mtime ~10:45 EEST → **FRESH** (~0.9h; data freshness 07:30 UTC).
- **Crypto swing report** `data/reports/swing/2026-06-16_02-05_swing_report.md` — mtime ~05:05 EEST → **carry-forward** (~6.6h, 4–12h band; flagged §3).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-16_08-09_stocks_intraday_report.md` — mtime ~11:09 EEST → **FRESH** (~0.5h) but **market closed → planning/watchlist only**.
- **Stocks swing** `…02-11…` (~6.5h) + **invest** `…02-16…` (~6.4h) → carry-forward planning context.
- **Catalysts** `data/catalysts/2026-06-16/` present: `catalyst_cycle_07-45.md` (latest), `catalyst_events.jsonl`, `narrative_baskets.jsonl` (3 baskets). No catalyst-scan needed.
- **LLM packets** `data/processed/llm_analysis_packet.md` (crypto) + `llm_stocks_packet.md` (stocks).
- **Internal CLI:** `active-signals` crypto (**44 active**, all long B) + stocks (**A-tier AMD 88 / SMH 82 / JPM 80** carry-forward, plus B-tier AMD/SMH/JPM/PLTR/XLK/DIA/XLY); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-16` → **1 untracked** (ETH/USDT).
- **DB** `db/crypto_ai_desk.sqlite` (1.37 GB) — read-only queries: A-tier stock signals (created 2026-06-15 14:32 UTC, triggered); `t.me` last-5h = noise (lookonchain welcomes + Bitwise HYPE buy, no symbol-moving catalyst); legal-risk sweep → UNH DOJ probe (4 sources), SMCI indictment.
- **External:** WebSearch ×2 (BTC level Jun 16; FOMC/Iran) + WebFetch (LatestLY → BTC $66,304, BITA ETF launch, support/resistance).
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-16T0845Z.json` (4 cited sources, all crypto/macro); ingest CLI run for **crypto** — `input: 4 | valid: 4 | rejected: 0; wrote 4 row(s)` (see §10). No external stock-specific sources cited (UNH/AMD claims came from internal `news_items`), so no stocks ingest.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-16_default_schedule/`.
- `scheduler.log` mtime **11:38:25 EEST** (~7m old) → **FRESH**. The default scheduler **just booted CYCLE 1/12 at 11:38** and is mid-cycle (generating the crypto scalp report at read time).
- No `cycle_*_summary.md` in today's folder yet (cycle 1 in progress). Prior cycle reports (07:30–08:09) are the freshest completed outputs and are used.
- **scheduler.log < 3h → review proceeds** (defer requires BOTH log AND latest cycle summary > 3h; log is 7m fresh).
- Freshness labels: crypto scalp/intraday **fresh**; crypto swing **carry-forward (~6.6h)**; stocks intraday **fresh but market-closed → planning**; stocks swing/invest **carry-forward (~6.5h)**. No hard stale exclusions. The **A-tier stock signals are ~18h-old intraday triggers expiring pre-open → treated as stale planning context, not live.**

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-16_0440.md` (crypto overnight / Asia review):

- **Window moved overnight/Asia → Europe/pre-US.** Posture shifts from "work the overnight crypto tape into Europe" → **"set up the US day; build the RTH watchlist."** Stocks still closed but now ~5h from the open.
- **BTC essentially flat overnight:** ~$66.3–66.5K (04:40) → **$66,304** (now), still capped under **$67K** (resistance band tightened from $67.5K → $67K per fresh sources). Support firmed to **$63.5–64.5K**.
- **FOMC now imminent:** the decision is **tomorrow** (was "starts today, decision tomorrow" at 04:40). The data-watch ceiling intensifies into the print; **Warsh's first meeting** + possible hawkish bias shift is the key macro risk for the next 24–48h.
- **BITA ETF confirmed LIVE today** (was "debuts today" at 04:40; WebFetch now confirms it launched on Nasdaq as an actively-managed covered-call fund, 15–25% target yield).
- **Iran deal upgraded:** ceasefire → **finalized peace accord + Strait of Hormuz reopened**. Re-escalation risk lower but remains a headline tail.
- **Integrity regressed slightly:** untracked legacy alerts **0 (04:40) → 1 (now, ETH/USDT B scalp 08:37 UTC)**. Single instance, re-logged §14.
- **Crypto candidate cohort rotated:** prior RS-leaders NEAR/GPS/ZEC/WLD give way to **INJ** as the cleanest (now the sole unusual-volume name, vol 1.65–2.03×); SYN (+41%) / JTO (+27%) flagged overextended again. **UNH AVOID re-confirmed** (DOJ probe). ZRO no longer the headline avoid but remains caution (prior $23M unlock).
- **Catalyst mapping still weak** (77.0% unmapped vs 76.8% at 04:40) — recurring §14 TODO.

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl` today: **1,580 rows; mapped (non-null symbol) 364; unmapped 1,216 = 77.0%.** (Report dedups to "553 unique events, 3 baskets" — raw-vs-unique gap noted §14.)
- **⚠ Catalyst mapping weak this run (77.0% unmapped) — use the catalyst layer as context, not final decision.**
- **Top 3 unmapped (by importance, all sector/macro):** (1) "Deprecated Thetanuts Vault Exploited for $2.1 Million in Latest DeFi Attack" (BeInCrypto, 0.75); (2) "Exploit-Driven TVL Drop Pushes DeFi Leverage Back to 2021 Levels" (BeInCrypto, 0.73); (3) "One Indicted Over Crypto 'Wrench Attack' in France" (Decrypt, 0.68).
- **Narrative baskets (3):** **perps_dex_narrative** (`wait_pullback`, <1h) primary **HYPE/USDT**; **ai_narrative** (`related_beta_rotation`, <6h) primary **NEAR/RENDER/TAO/FET**; **delisting_thin_liquidity** (`avoid_low_liquidity`, <6h) primary —.
- **Legal/regulatory flags from the catalyst layer:** **UNH** (DOJ criminal Medicare-fraud probe — active C-tier long, AVOID), **SMCI** (export-control indictment, SEC EDGAR 8-K — in rejected/short bucket). Both surfaced as `…/USDT` rows (symbol-resolver quirk mislabelling stocks as crypto pairs — §14).

## 6. Market Landscape

- **Crypto:** bullish trend / risk-on, range-capped, **pre-FOMC**. BTC + ETH uptrend; alt breadth **79.5% > EMA20 / 81.8% > EMA50**, BTC ATR percentile **32 (normal vol)**. **BTC ~$66.3K into $67K resistance**, support $63.5–64.5K / $61.8K. Funding broadly neutral, crowding normal. Strongest RS (scalp/intraday): **INJ 96–98 (+10.6%, vol 1.65–2.03× — only unusual-volume name)**, SYN 91.6 (**+41.6%, overextended, neg funding**), JTO 91.4 (**+27.2%, OI +53%**), WLD 90.1, XLM 87.3, SPCXB 84.6, AAVE 82.6. Weakest: OPG −15%, CHIP −15%, ADX −12%, MEGA −9%, STG −8%. ETF flow split: **BTC ETF −$64.8M outflows Monday while ETH/SOL/XRP funds drew capital** → SOL framed as "new risk-on leader heading into Q3."
- **Stocks (closed / pre-market):** regime **risk_on, bias long, VIX 16.19**, breadth 75% > EMA20; QQQ/IWM/DIA uptrending, SPY range. Strongest sectors semis (SMH +16.3% 20d) / tech. **A-tier cluster in semis/financials — AMD 88.8, SMH 82.4, JPM 80.9** (yesterday's RTH triggers, expiring pre-open → planning only). AMD catalyst-backed (Citi Buy upgrade Jun 12, ~$900B valuation, AI-inference rotation). Week stats: **longs PF 1.2 (+4R), shorts PF 0.5 (−19R)** — long-only edge. A/B headline winrate 20% (n=50) — review manually.

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:**           **risk-on but range-capped + pre-FOMC** ($67K ceiling, FOMC decision tomorrow, Fear&Greed 23).
- **Stocks mood:**           **pre-market / closed** (regime risk_on into the 16:30 EEST open; overnight gap risk).
- **Dominant narrative:**    US–Iran peace accord / Strait-of-Hormuz reopen → risk-on; **AI/semis rotation** (AMD/SMH leadership; AI-alt basket NEAR/TAO/RENDER/FET); **BlackRock BITA BTC-income ETF live today**.
- **Preferred side now:**    **longs / wait-for-pullback** (RS-leader + confirmation); **no fresh shorts** (crypto B-tier 16% winrate; stock shorts PF 0.5 / −19R).
- **Best long candidate:**   **INJ** (crypto, sole unusual-volume RS leader) — long-watch on a pullback into 5.71–5.77, BTC-gated >$64K; stocks: **AMD** on RTH confirmation after the open.
- **Best short candidate:**  **none clean** — risk-on disfavours shorts. Short-watch only **after a failed retest of broken support AND BTC losing $64K**; weakest names (OPG/CHIP/ADX) thin/squeeze-prone.
- **Best catalyst-backed candidate:** **SOL** (ETF inflows + "risk-on leader Q3" narrative) / **BTC** (BITA ETF launch); stocks: **AMD** (Citi upgrade + AI-semis rotation, after RTH confirmation).
- **What to avoid:**         **UNH** (DOJ Medicare-fraud probe — legal AVOID), **SMCI** (indictment), stock shorts, overextended crypto (SYN +41%, JTO +27%), crypto scalp lane (PF 0.14), fresh shorts.
- **What would change the view:** BTC **clean daily close >$67K on volume** (→ continuation, retest higher) or **loses $64K** (→ flush toward $61.8K); **FOMC tomorrow hawkish surprise / Warsh bias shift** (→ risk-off); Iran-deal re-escalation headline.

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — INJ/USDT (crypto, B-tier LONG, best clean long-watch)
- **Setup:** RS leader, momentum **96.2 (scalp) / 98.3 (intraday)**, **+10.6% 24h**, RS vs BTC +9.6%, **vol 1.65–2.03× — the ONLY unusual-volume name** (tags: relative_strength, volume_expansion, breakout). B-tier score 75.7. Active intraday signal `tp1_hit`.
- **Catalyst check (internal-first):** no fresh verified single-symbol catalyst; pure technical RS/volume. Derivatives: price up + OI **down** (−3.06%) = short-covering → weaker continuation quality; funding ~neutral, crowding normal.
- **Price/chase:** has price reacted? Yes (+10.6%) but it has the cleanest volume confirmation of the cohort. Overextended? Less than SYN/JTO. Entry now would be mid-range — **demand a pullback into 5.71–5.77, no market buy if extended**. Mood-aligned: yes (risk-on RS-leader long). Long/short/wait: **long, pullback-only**. Invalidation: 1h close beyond **5.644**. Chase-risk: moderate. Catalyst confirmation: none (technical only).
- **Decision:** **LONG-WATCH, pullback-only (5.71–5.77), BTC-gated >$64K.** Best clean crypto long into Europe. Caveat: scalp lane is research-grade (PF 0.14) — treat scalp execution with lower confidence; prefer the 1h/intraday framing.

### Candidate 2 — UNH (stocks, active C-tier LONG) · LEGAL/HEADLINE RISK — AVOID
- **Setup:** appears as an active C-tier long stock signal (intraday 61, swing 67).
- **LEGAL/HEADLINE RISK (verified, internal `news_items`, Jun 15, 4 sources):** **DOJ criminal probe into UnitedHealth's Medicare-Advantage practices, extending to Optum Rx / physician reimbursement; shares −16%.** Sources: Fierce Healthcare, TipRanks, Healthcare Finance News, Newsweek (UNH called the report "deeply irresponsible"). Consistent, recent (<36h), multi-source → no external verification needed.
- **Price/chase:** the −16% drop means a long here is catching a falling knife into an active criminal investigation. Mood-aligned? No. Long/short/wait: **AVOID** (neither side clean; do not short into an oversold legal gap either).
- **Decision:** **AVOID / MANUAL REVIEW REQUIRED.** A C-tier momentum/mean-reversion long must not be treated as actionable while a DOJ criminal probe is live. Flag to suppress UNH from any long alert.

### Candidate 3 — AMD (stocks, A-tier 88.8 / B 77.4) · CLOSED — planning, RTH-confirmation required
- **Setup:** A-tier intraday (88.8) + B intraday (77.4) + C across modes; the strongest stock long. **Created 2026-06-15 14:32 UTC (~18h ago), status `triggered`, expires ~11:32 UTC today → expires BEFORE the 16:30 EEST open.** Entry 549.26, stop 529.49, TP1 569.03.
- **Catalyst check (internal-first):** strongly catalyst-backed — Citi upgrade to Buy (Jun 12), "~$900B valuation after beefing up memory technology" (MarketWatch), AI-inference rotation (Benzinga/TipRanks, semis +16.3% 20d). No legal/earnings risk found in the 36h sweep.
- **Price/chase:** the A-tier trigger is stale (pre-open, ~18h old) → **do NOT treat as a live entry**. Stocks longs carry the edge (PF 1.2, +4R) but A/B headline winrate is only 20% and A-tier has 0 closed (overpromotion caveat). Mood-aligned: yes (risk-on, semis leadership). Long/short/wait: **long, but only after RTH confirmation** post-09:30 ET on fresh levels.
- **Decision:** **PLANNING LONG-WATCH — top stock long into the US open; require RTH confirmation (first 15–30 min) on fresh levels, do not act on the stale overnight trigger.**

### Candidate 4 — SOL/USDT (crypto, B-tier LONG) · catalyst-backed
- **Setup:** B-tier ~66–68, momentum 69.4, +4.3% 24h, RS vs BTC +3.2%, **fresh attention via 3 catalyst/news items** (catalyst_news 10.4 — highest of the cohort). Active intraday signal `waiting_for_entry` near 73.9, swing `triggered`.
- **Catalyst check (internal-first):** **ETF rotation — "Bitcoin ETF sees $64.8M outflows while ETH, SOL, XRP funds attract fresh capital" (CryptoBriefing); "Is Solana emerging as market's new risk-on leader heading into Q3?" (AMBCrypto).** single_source each but directionally consistent and fresh.
- **Price/chase:** modest move (+4.3%) → not overextended; cleaner entry geometry than SYN/JTO. Derivatives: short-covering (OI −0.4%), long/short heavily skewed long (crowding caution). Mood-aligned: yes. Long/short/wait: **long, pullback into 73.9–74.2**. Invalidation: 1h close beyond 73.47. Chase-risk: low-moderate.
- **Decision:** **LONG-WATCH (catalyst-backed alternate to INJ), pullback into 73.9–74.2, BTC-gated >$64K.** Best catalyst-supported crypto long this window.

### Candidate 5 — SMH + JPM (stocks, A-tier 82.4 / 80.9) · CLOSED — planning, A-tier overpromotion caveat
- **Setup:** A-tier intraday with AMD (same 2026-06-15 14:32 UTC batch, `triggered`, expiring pre-open). SMH = semis ETF (sector RS leader, +16.3% 20d); JPM = financials. Entries SMH 642.65 / JPM 322.24.
- **Catalyst check:** SMH rides the AI-semis rotation (AMD/NVDA strength); JPM benefits from risk-on financials. No legal/earnings flags in the sweep.
- **Price/chase:** same staleness as AMD — **18h-old triggers expiring before the open → planning context only.** A-tier has 0 closed signals (sample-bias / overpromotion caveat); stock shorts are the losing bucket, so the long bias is correct but unconfirmed.
- **Decision:** **PLANNING WATCH — semis (SMH) + financials (JPM) longs into the US open; require RTH confirmation, do not chase the stale trigger or the pre-market gap.**

## 8. Best Candidates Ranked

1. **INJ/USDT — crypto LONG-WATCH (best clean long).** Trigger: pullback into **5.71–5.77** with BTC holding **>$64K**; invalidation 1h close < 5.644.
2. **SOL/USDT — crypto LONG-WATCH (best catalyst-backed).** Trigger: pullback into **73.9–74.2**, BTC >$64K; ETF-inflow/risk-on-leader thesis; invalidation 1h close < 73.47.
3. **AMD — stocks PLANNING LONG (best stock long).** Trigger: **RTH confirmation after 16:30 EEST open** on fresh levels (do not use the stale 549.26 trigger); catalyst: Citi Buy + AI-semis rotation.
4. **SMH / JPM — stocks PLANNING WATCH (semis/financials A-tier).** Trigger: RTH confirmation post-open; sector-leadership longs.
5. **BTC — macro anchor / catalyst-watch.** Trigger: **clean daily close >$67K on volume** → continuation; BITA ETF launch is a structural tailwind, exchange reserves multi-year lows.

**Watch-side triggers (no fully clean entry this window):**
- **long-watch** INJ: pullback 5.71–5.77 + BTC >$64K.
- **short-watch** none clean → only **after a failed retest of broken support AND BTC losing $64K** (e.g. OPG/CHIP/ADX, but thin/squeeze-prone — require confirmation).
- **catalyst-watch** SOL: hold above pullback zone + a second independent ETF-flow/leadership source.

## 9. Avoid / No Trade  (this decision window only)

- **UNH** — active DOJ criminal Medicare-fraud probe (−16%); legal **AVOID** despite C-tier long signal.
- **SMCI** — export-control indictment (8-K); avoid on legal grounds (currently in rejected/short bucket anyway).
- **Fresh shorts (both classes)** — risk-on regime; crypto B-tier 16% winrate, stock shorts PF 0.5 / −19R. Shorts only after failed retest + BTC < $64K.
- **Overextended crypto** — **SYN (+41.6%, neg funding), JTO (+27.2%)** — chase-risk; long-watch only on a deep defended pullback.
- **Crypto scalp lane** — PF 0.14, low_confidence overlay; research-grade only, not Telegram-actionable conviction.
- **Note:** "no clean trade now" applies to **this 4h window only** — the scanner, candidate generation, tracking, and monitors continue in all moods.

## 10. Main Risks

- **FOMC tomorrow (Wed Jun 17, 2:00pm ET) — Warsh's first meeting.** Hold expected (~98%) but a hawkish bias shift (easing→neutral/tightening) with inflation at 4.2% could flip risk-off. Expect consolidation/compression into the print → avoid sizing into the decision.
- **BTC pinned under $67K, Fear&Greed 23.** A rejection here + loss of $64K opens a flush toward $61.8K; the rally is still headline-dependent.
- **Iran-deal re-escalation tail.** The peace accord is the rally's foundation; any re-escalation headline reverses the risk-on rotation.
- **Stale stock A-tier triggers.** AMD/SMH/JPM expire pre-open; acting on the stale levels (vs RTH confirmation) risks a gap trap. A-tier has 0 closed signals (unproven sample).
- **Stock-short losing bucket (PF 0.5, −19R)** and **crypto B-tier 16% winrate** — execution discipline (pullbacks + confirmation) matters more than candidate count.
- **§M ingest:** ran for **crypto** from the cited sources JSON (idempotent UPSERT, `wrote 4 row(s)`). External citations were all crypto/macro → no stocks ingest. No ingest error.

## 11. Action Plan — next 4 hours (into the US open)

1. **Crypto:** watch **INJ** for a pullback into 5.71–5.77 (BTC >$64K) and **SOL** into 73.9–74.2 — pullback-only, no chasing; both gated on BTC holding $64K and not rejecting hard at $67K.
2. **BTC level read:** treat **$67K** as the pivot — accept-above-on-volume = continuation bias; lose **$64K** = step aside / flush risk to $61.8K.
3. **Stocks:** build the RTH watchlist — **AMD, SMH, JPM** (longs) for **confirmation after 16:30 EEST**, on fresh levels; **suppress UNH** (legal); ignore the stale overnight A-tier triggers as entries.
4. **No fresh shorts** either class; no new risk into **tomorrow's FOMC** — keep size modest into the print.
5. **Re-check at the 16:20 pre-US-open slot:** gap risk, pre-market reactions, RTH-confirmation status for AMD/SMH/JPM, and whether BTC has resolved the $67K pivot.

## 12. Final Verdict per Mode

- **Crypto scalp:** research-grade only (PF 0.14, low_confidence). No conviction entries; data-collection continues. If anything, INJ pullback partial with early profit-take — lower confidence.
- **Crypto intraday:** **selective LONG, pullback-only** — INJ (clean) / SOL (catalyst-backed), BTC-gated >$64K, no chase. No shorts.
- **Crypto swing:** carry-forward; RS-leader longs (INJ/SOL/ZRO active) managed to invalidation; no fresh adds into FOMC.
- **Stocks intraday:** **closed — planning only.** Long bias (AMD/SMH/JPM) for **RTH confirmation** after the open; UNH AVOID; no shorts.
- **Stocks swing/invest:** carry-forward; semis/financials long bias intact; await RTH + post-FOMC clarity before fresh adds.

## 13. Sources

- [Bitcoin Price Today, June 16, 2026: BTC Holds Steady Around USD 66,304 (BlackRock BITA launch, Iran relief)](https://www.latestly.com/business/bitcoin-price-today-june-16-2026-btc-holds-steady-around-usd-66304-amid-geopolitical-relief-and-blackrocks-yield-etf-launch-7475172.html) — LatestLY, 2026-06-16 (WebFetch-verified: BTC $66,304; support 63.5–64.5K; resistance 67K).
- [Bitcoin Price Today: BTC Holds $66K As The Fed's Big Day Arrives and Warsh Takes Over](https://blockchainreporter.net/bitcoin-price-today-btc-holds-66k-as-the-feds-big-day-arrives-and-warsh-takes-over/) — BlockchainReporter, 2026-06-16 (BTC ~$66K, recovered from $59,130 low, F&G 23).
- [Fed meeting preview June 16-17: FOMC decision and potential bias shift](https://www.indexbox.io/blog/fed-meeting-preview-june-1617-fomc-decision-and-potential-bias-shift/) — IndexBox, 2026-06-15 (decision Wed Jun 17 2:00pm ET, Warsh's first, hold 3.50–3.75% ~98%, inflation 4.2%).
- [Bitcoin and ethereum prices today, June 15, 2026: Prices rising after U.S., Iran agree to ceasefire deal](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-june-15-2026-prices-rising-after-us-iran-agree-to-ceasefire-deal-114616600.html) — Yahoo Finance, 2026-06-15 (US–Iran deal driving risk-on).
- **Internal:** `news_items` (UNH DOJ probe ×4 sources: Fierce Healthcare / TipRanks / Healthcare Finance News / Newsweek, 2026-06-15; AMD Citi-upgrade/$900B: MarketWatch / Benzinga / TipRanks, 2026-06-15; SMCI 8-K indictment: SEC EDGAR); scalp + intraday + stocks-intraday reports; `signal-stats` / `active-signals`; `catalyst_events.jsonl` / `narrative_baskets.jsonl`.

## 14. Fix Requests / TODO

### TODO-catalyst-mapping
- **issue:**            Catalyst mapping weak again — 77.0% of events unmapped (null symbol).
- **evidence:**         `data/catalysts/2026-06-16/catalyst_events.jsonl`: 1,580 rows, mapped 364, unmapped 1,216 (77.0%). Recurring (76.8% at 04:40 slot, >50% all of yesterday).
- **suggested manual fix:** Improve the symbol resolver in the catalyst layer (entity→ticker mapping, alias table, handle headline-only macro items separately so they don't count as "unmapped").
- **priority:**         medium
- **first observed:**   recurring (pre-2026-06-16); re-confirmed 2026-06-16 11:45 EEST

### TODO-untracked-legacy-alert
- **issue:**            1 untracked legacy crypto alert reappeared (sent to Telegram, no matching proposed_signal → excluded from PF/winrate).
- **evidence:**         `detect_untracked_legacy_alerts --since 2026-06-16` → ETH/USDT B scalp long, sent_at 2026-06-16T08:37:25+00:00, "NO (no proposed_signal)". Was 0 at the 04:40 slot.
- **suggested manual fix:** Investigate the PART-1 alert→proposed_signal linkage for scalp-mode ETH alerts; ensure every Telegram alert writes a trackable signal_id.
- **priority:**         medium
- **first observed:**   2026-06-16 11:45 EEST (regression vs 0 at 04:40)

### TODO-stock-short-bucket
- **issue:**            Stock SHORT signals are a reproducibly losing bucket.
- **evidence:**         `signal-stats --asset-class stocks`: by direction, shorts n=140 trig=139, 18W/44L, **PF 0.5, total −19R**; longs PF 1.2, +4R. Risk-on regime.
- **suggested manual fix:** Tighten or gate stock-short scoring (require stronger confirmation / regime filter so shorts are suppressed in risk_on breadth>70%).
- **priority:**         medium
- **first observed:**   recurring (−18R at 04:40); re-confirmed 2026-06-16 11:45 EEST

### TODO-catalyst-raw-vs-unique
- **issue:**            Raw `catalyst_events.jsonl` line count (1,580) far exceeds the report's "553 unique events" — possible duplication / dedup drift inflating the unmapped %.
- **evidence:**         Raw file 1,580 lines vs report §5b "Unique events today: 553". Manual count: mapped 364 / unmapped 1,216 on raw.
- **suggested manual fix:** Audit dedup keying in the catalyst writer; confirm whether the unmapped% should be computed on unique events (would change the 77% figure).
- **priority:**         low
- **first observed:**   2026-06-16 11:45 EEST

### TODO-symbol-resolver-stocks-as-usdt
- **issue:**            Stock legal-risk events (UNH, SMCI) surface as `…/USDT` crypto pairs in the catalyst layer.
- **evidence:**         catalyst notable events: "SMCI/USDT [legal_risk]", "UNH/USDT [legal_risk]".
- **suggested manual fix:** Add asset-class awareness to the catalyst symbol resolver so equities are not coerced into `/USDT` pairs.
- **priority:**         low
- **first observed:**   recurring (noted 04:40); re-confirmed 2026-06-16 11:45 EEST
