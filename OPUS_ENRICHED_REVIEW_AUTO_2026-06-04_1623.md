# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:23 EEST

- **Generated:** 2026-06-04 16:23 EEST (auto-enriched-review, scheduled task `opus-enriched-review-preus`, executing shared SKILL.md `opus-enriched-review-4h`).
- **Slot:** **pre-US-open decision review** — ~7 minutes before the US cash open (09:30 ET / 16:30 EEST). Focus: final pre-open read, gap risk, overnight catalysts, which A/B setups are actionable once the bell rings.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-04_1242.md` (≈3.7 h ago — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). AVGO −15% premarket, CRWD −11%, semi sympathy, and the Iran/oil + jobless-claims macro overlay independently confirmed (CNBC, ts2.tech WebFetch-verified, Motley Fool, Benzinga). One WebFetch (TheStreet) returned HTTP 403 → fell back to ts2.tech which loaded cleanly.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is from local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **This is the decision moment for the stock setups, and the decision is DEFENSIVE.** The US opens into a **semiconductor sell-off led by Broadcom's post-earnings collapse.** AVGO is **−15% premarket** (low ~$405.5 vs a $481.57 pre-earnings all-time high), dragging Micron −6/7%, Marvell −7.5%, and AMD/NVDA/INTC/QCOM down in sympathy. **Nasdaq-100 futures −1.3/1.4%, S&P −0.7%, Dow +0.5%** (classic rotation out of mega-cap tech/semis into value). Layered on top: **Iran/Middle-East tension** (oil +~2%, 10y yield ~4.5%) and **jobless claims at a 4-month high**. Posture into the open: **do not chase any semi long; let the AVGO gap absorb before touching the group.**
- **The desk's own actionable list is pointed the WRONG way for this open.** The 11:15 UTC stocks report (generated while the session was closed) still surfaces **AVGO A-tier LONG 89.7**, plus semis longs **AMD (A 87 / B 79), SMH (A 82 / B 78), XLK (B 73.7)** — all of which gap **down** against the AVGO catalyst. **AVGO verdict: AVOID — sell-the-news; the A-tier long entry (~473–478) sits ~15% ABOVE where the stock will open.** This is the **5th consecutive review** flagging AVGO; the desk has not self-corrected (TODO-stocks-stale-postearnings).
- **LLY (A-tier long 84.31) is the only relatively clean A-name** — pharma/healthcare, NOT a semi, no AVGO read-through, RS leader, earnings-safe, and internal news is supportive ("3 Reasons Eli Lilly Remains a Buy", "Another Reason to Buy Eli Lilly"). But (a) it is still subject to a broad risk-off open and (b) the A-tier stocks bucket is a statistical loser this run (PF 0.29, WR 7%). Treat as **reassess on fresh open levels, half-size if at all** — not an auto-green-light.
- **NVDA is the relative-strength tell inside the dive** ("Why Nvidia Stock Is Riding the Chip Selloff Better Than Its Rivals") — the name to watch for the first sign the semi group stabilizes, NOT a name to front-run.
- **Crypto remains the only 24/7 class and it is risk-off: regime "high-volatility danger (danger)."** BTC/ETH downtrend, breadth above EMA20 **25–27%**, BTC ATR percentile **98 (elevated)**. **Zero fresh A/B crypto setups** this run — best structured idea is **SHORT HOME/USDT 65.1 (scalp)**, but it is below the active-trade threshold → watchlist/no-trade. NEAR carries fresh AI-basket catalyst attention but only as C-tier watchlist (short, −17/−21% 24h, weak volume — late, do not chase the breakdown).
- **Net action for the next 4 hours:** stocks = stand aside at the open, no semi chase, watch NVDA for stabilization and LLY for a clean post-open level; crypto = no-trade / watchlist, respect $60k BTC floor risk. **No clean actionable A/B for either class at this open.**

---

## 2. Data Used

**Internal — fresh (<3.5 h):**
- `data/reports/scalp/2026-06-04_12-55_scalp_report.md` (gen 15:55 EEST; data freshness 12:30 UTC). Regime **high-volatility danger**, BTC/ETH downtrend, breadth 27.1% > EMA20, BTC ATR pct 98.
- `data/reports/intraday/2026-06-04_13-21_intraday_report.md` (gen 16:21 EEST; data freshness 13:00 UTC). Regime **high-volatility danger**, breadth 25.0% > EMA20.
- `data/reports/stocks/intraday/2026-06-04_11-15_stocks_intraday_report.md` (data freshness 11:15 UTC, ~5 h; session=after-hours/closed at gen). Weekday — applies. **Carry-forward, flagged**: generated pre-open, score does NOT reflect the AVGO −15% reaction.
- `data/catalysts/2026-06-04/` — `catalyst_events.jsonl` (1424 cumulative rows / 710 unique per report), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_09-14.md`.
- LLM packets: `data/processed/llm_analysis_packet.md` (gen 15:55), `llm_stocks_packet.md` (gen 14:15).
- CLI / DB: `active-signals` (crypto 9 / stocks ~40), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-06-04` → **1 untracked (EPIC/USDT)**. `news_items` queries (db/crypto_ai_desk.sqlite, 3757 rows) for AVGO/LLY/SMCI/AMD/SMH/NVDA + stocks legal-risk scan.

**Internal — carry-forward / stale:**
- `data/reports/stocks/swing/2026-06-03_13-11_stocks_swing_report.md` — ~27 h → **STALE (>14 h, flagged)**, excluded from fresh swing/invest final-verdict.
- `data/reports/stocks/invest/2026-06-03_13-15_stocks_invest_report.md` — ~27 h → **STALE (>14 h, flagged)**.
- `data/reports/swing/2026-06-03_01-20_swing_report.md` (crypto) — ~39 h → **STALE (>14 h)**; active ZEC/XLM swing *signals* used instead.

**External (this run — cited §13):** CNBC + Motley Fool transcript (AVGO Q2 FY26: EPS $2.44 vs $2.40, rev $22.19B +48% YoY, AI guide reiterated $100B FY27 — not raised → sell-the-news); ts2.tech WebFetch-verified (AVGO −15% premarket, CRWD −11%/split, Micron −6/7%, Marvell −7.5%, Nasdaq-100 fut −1.3/1.4%, S&P −0.7%, Dow +0.5%, oil +2% Iran, 10y ~4.5%, jobless claims 4-mo high); Benzinga (S&P open preview, Iran/oil).

**Unavailable / blind:** live intraday equity prints the instant of the open (only premarket prints available); TradingView/Chrome chart verification (not loaded); liquidation heatmaps, order-book depth/CVD, live ETF-flow feed, on-chain whale flows, token-unlock calendar (manual/unconnected); live social beyond RSS-bridged `t.me/lookonchain`.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-04_default_schedule/`.
- `scheduler.log` mtime **16:00 EEST → ~0.4 h** (fresh). Scheduler **re-booted 16:00** and is mid-cycle (currently running the crypto scalp report).
- Latest completed cycle summary: `cycle_06_11-21_summary.md` mtime 12:32 EEST → ~3.85 h (the prior cycle; the 16:00 cycle has not emitted a summary yet).
- **scheduler.log < 3 h → NO DEFER** (the defer rule requires BOTH log AND latest summary > 3 h; the log is 0.4 h fresh). Review proceeds normally.
- Crypto scalp ~3.5 h / intraday ~3 h → **carry-forward but usable** (current cycle is regenerating both now). Stocks intraday ~5 h → **carry-forward, flagged** (pre-open snapshot).
- Crypto swing ~39 h, stocks swing/invest ~27 h → **STALE (>14 h)**; excluded from fresh final-verdict.

---

## 4. What Changed vs Previous Review (12:42 → 16:23)

- **The AVGO/semis gap is no longer hypothetical — it is the open.** 12:42 flagged AVGO as a closed-market after-hours read (~$417, −13%). At 16:23 the premarket print has deepened to **−15% (~$405–409)**, semis are selling off broadly (Micron −6/7%, Marvell −7.5%, AMD/NVDA/INTC in sympathy), and Nasdaq-100 futures are −1.3/1.4% into the bell. The read-through is now a live gap, not a forecast.
- **New macro layer since 12:42:** **Iran/Middle-East tension** (oil +~2%, 10y yield ~4.5%) and **US jobless claims at a 4-month high** (partly Memorial Day timing). CRWD −11% on cautious guidance (offset by a 4-for-1 split) adds to the tech-tape pressure. The open is risk-off on two axes (semi earnings + geopolitics).
- **Crypto regime unchanged at "high-volatility danger"**; breadth roughly stable (22.9% → 25–27% > EMA20). Still zero fresh A/B crypto setups. HOME/USDT short re-appears as the top structured scalp idea (65.1) vs last run's pure-C-tier list.
- **Stocks A-tier loss bucket persists / marginally worse:** this run PF **0.29**, totalR −5.0, winrate **~6.7%** (n=25) vs B-tier PF 1.33 / +15 R. No improvement (TODO-stocks-atier-winrate).
- **Catalyst mapping still weak:** **76.2% unmapped** (1085/1424) — essentially identical to 12:42's 76.2%. Multi-run regression (TODO-catalyst-mapping-weak).
- **Integrity regression NEW this run:** `detect_untracked_legacy_alerts` now shows **1 untracked** — EPIC/USDT B scalp long sent to Telegram 10:03 UTC with **no matching proposed_signal** (was **None** at 12:42). Will not contribute to PF/winrate (TODO-untracked-epic-alert).
- **Confirmed since last review:** AVGO sell-the-news, semi gap-down, BTC risk-off all confirmed and intensified.
- **Invalidated:** nothing materially invalidated; the bullish stocks regime label (VIX 16.62, breadth 100%) carried in the 11:15 report is now **stale** against the actual risk-off open — do not rely on it.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative JSONL): **1424**; mapped (non-empty `symbol`): **339**; unmapped: **1085** → **76.2% unmapped**.
- `narrative_baskets`: **3** — `perps_dex_narrative` (primary HYPE), `ai_narrative` (NEAR/RENDER/TAO/FET), `momentum_breakout` (HEI/EPIC/WLD). All `single_source`, AI basket fresh <6 h.
- **⚠️ catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped > 50%).
- Top 3 unmapped headlines (symbol unresolved): (1) "Tilly's (TLYS) Q1 2026 Earnings Call Transcript"; (2) "Stock Market Today, June 3: Markets End Winning Streak on Middle East Escalation Fears"; (3) "Stock Market Today, June 3: Rivian Automotive Jumps on Strong R2 SUV Order Interest". The resolver is dropping clearly-tickered names (TLYS, RIVN) into the unmapped bucket.

---

## 6. Market Landscape

**Stocks (the live story this slot):** Pre-earnings the tape was bullish (SPY/QQQ/DIA/IWM uptrend, VIX 16.62, breadth 100%, semis the leadership — SMH RS +17.8%, XLK +14.3%). **That leadership just inverted.** Broadcom beat (EPS $2.44 vs $2.40, rev $22.19B +48% YoY) but DIDN'T raise the $100B FY27 AI target → textbook sell-the-news, −15%. The AI-semi complex is the source of the gap; money is rotating to Dow/value (Dow fut +0.5% vs Nasdaq −1.4%). Geopolitics (Iran/oil) and a soft labor print add a risk-off tilt. **First-hour expectation: gap-down semis, possible knife-catch attempts — wait for the gap to fill/hold before any long.**

**Crypto (24/7, risk-off):** Regime **high-volatility danger**; BTC/ETH downtrend; breadth 25–27% > EMA20; BTC ATR pct 98. Narrative heat concentrated in **AI (rising, heat 58–66)** — but every AI alt (NEAR −17/−21%, RENDER −15%, FET −15%, ICP −14%) is DOWN; this is the AI *narrative* basket bleeding, not leading. Lone green outliers (MEME +11–15%, OPN +82%, EPIC +13%, ZBT +10%) are low-volume counter-tape pops, all watchlist-only. BTC backdrop from prior cycle: ~$63k, lowest since February, multi-day spot-ETF outflow streak, ~$1.5B 24h liquidations, $60k = major floor. No fresh A/B; the desk says "reduce size or no trade until structure settles."

---

## 7. Candidate Deep Dives (≤5)

### 7.1 AVGO — A-tier LONG 89.7 (stocks intraday) → **AVOID (sell-the-news, gap risk)**
- **Contradiction (priority-2):** desk score A-long 89.7 with a stale pre-earnings entry zone (~473.25–478.07); actual premarket **−15%, ~$405–409** → the printed long entry is **~15% above market**.
- **Catalyst:** Q2 FY26 beat (EPS $2.44 vs $2.40, rev $22.19B +48% YoY, AI-semi strong) but Q3 AI guide ~$16B < $17.2B expected and **$100B FY27 AI target NOT raised** → sell-the-news. Internal `news_items` (13:01Z, <1 h) corroborate: "worst 1-day destruction in shareholder value ever", "Broadcom dive", "semiconductor sector sell-off."
- **Price-reaction / chase check:** price has FULLY reacted (−15% gap); entry would be chasing a falling knife into a sector-wide flush; overextended to the downside vs the report's pre-earnings levels; no clean retest yet. **Entry now = late and wrong-direction vs the desk label.**
- **LEGAL/HEADLINE RISK:** none verified (earnings reaction, not legal).
- **Verdict: AVOID / MANUAL REVIEW REQUIRED.** Not a clean actionable. 5th consecutive flag.

### 7.2 LLY — A-tier LONG 84.31 (stocks intraday) → **WATCHLIST, reassess on fresh open levels**
- **Why it's the cleanest A:** pharma/healthcare (defensive), NOT a semi → no AVGO read-through; RS leader vs SPY (+4.9%) and sector; earnings-safe. Internal news supportive ("3 Reasons Eli Lilly Remains a Buy", "Forget Weight Loss Drugs: Another Reason to Buy Eli Lilly").
- **Price-reaction / chase check:** no idiosyncratic catalyst spike; the risk is simply opening into a broad risk-off tape. No fabricated chart read (chart tools not loaded) — levels from report fields only.
- **Caveats:** (a) A-tier stocks bucket is a statistical loser this run (PF 0.29, WR 7%); (b) market-wide risk-off open. **Verdict: WATCHLIST — only consider after a clean post-open hold on fresh levels, half-size; do not buy the first print.**

### 7.3 AMD / SMH / XLK (semis longs, A 87 / A 82 / B 73.7) → **DO NOT CHASE — gap-down sympathy**
- All three are the desk's bullish semi expression and all gap **down** against AVGO (AMD/Micron explicitly "sink as Broadcom results spark semiconductor sector sell-off" — internal news 13:01Z).
- **Chase check:** longs into a confirmed negative sector gap = wrong side at the open. AMD is the strongest-RS single name and the best *post-open reassessment* candidate, but only once the AVGO gap is absorbed and the group prints a higher low. **Verdict: STAND ASIDE pre-open; reassess AMD after stabilization.**

### 7.4 NVDA — relative-strength tell → **WATCH (not a front-run)**
- "Why Nvidia Stock Is Riding the Chip Selloff Better Than Its Rivals" (internal 12:55Z) + active A-tier swing signal (80, triggered). NVDA holding better than AMD/AVGO/Micron is the canary: if NVDA stabilizes first, the semi flush is maturing. **Verdict: WATCH as the group-health signal; no fresh entry into the gap.**

### 7.5 HOME/USDT — crypto B-tier SHORT 65.1 (scalp) → **WATCHLIST / no-trade (below threshold)**
- Best *structured* crypto idea this run: breakdown/retest short, momentum 91.1, vol 4.81x, RS vs BTC −7.2%, aligned with the high-vol-danger bear tape. Negative funding across venues (bybit/okx/mexc) → shorts somewhat crowded (squeeze risk).
- **Entry plan (from report):** failed-bounce/retest 0.0370–0.0377; **invalidation 1h close > 0.0385**; TP1 0.0353 / TP2 0.0338. Current ~0.0367–0.0372.
- **Chase check:** no late short after a vertical flush; only on a retest into the zone. Score 65.1 is **below the active-trade threshold** → not Telegram-actionable. **Verdict: WATCHLIST.** (NEAR/USDT short — fresh AI-basket catalyst attention but −17/−21% 24h on weak volume = late breakdown, watchlist-only.)

---

## 8. Best Candidates Ranked

1. **LLY (long)** — cleanest A, but watchlist-only into a risk-off open; reassess on fresh levels, half-size at most.
2. **HOME/USDT (short)** — best structured crypto idea, but below threshold → watchlist.
3. **AMD (long)** — best *post-open* semi reassessment AFTER the AVGO gap absorbs; not now.

_No candidate clears a clean actionable bar at this open._

## 9. Avoid / No Trade

- **AVGO (long)** — sell-the-news, −15% gap, entry ~15% above market. AVOID.
- **Semis longs into the open (AMD/SMH/XLK pre-stabilization)** — gap-down sympathy; do not chase.
- **AI-narrative crypto alts as longs** (NEAR/RENDER/FET/ICP) — narrative bleeding, all −14/−21% on weak volume; not long material.
- **Counter-tape crypto pops** (OPN +82%, MEME, EPIC, ZBT) — low-volume, watchlist-only, no chase.

## 10. Main Risks

- **Gap-down knife-catch risk** in semis at the open — the single biggest trap this slot.
- **Geopolitical tail (Iran/Middle East)** — oil +2%, headline-driven; can whip the tape both ways intraday.
- **Stocks intraday report is a pre-open (~5 h, market-closed) snapshot** — its bullish regime label and A-tier longs do NOT reflect the actual open; treat as stale for execution.
- **BTC $60k floor** — a break opens $55k; cut crypto long aggression on further BTC support loss.
- **Source-ingest** (§13) may write 0 rows if the CLI errors — non-blocking; logged here.

## 11. Action Plan — next 4 hours

1. **At the open: stand aside on stocks.** No semi longs. Watch the AVGO gap (does it fill toward ~$430 or keep bleeding?) and **NVDA** for the first sign of semi stabilization.
2. **LLY:** if it holds a clean higher low on fresh post-open levels and the broad tape steadies, a half-size long is defensible — but only after the first 15–30 min, not the opening print.
3. **AMD:** reassessment candidate only AFTER the AVGO gap is absorbed and the group prints a higher low.
4. **Crypto:** no-trade / watchlist. HOME/USDT short only on a retest into 0.0370–0.0377 with invalidation 1h>0.0385 (and it's still below threshold). Respect BTC $60k.
5. **Monitor** Iran/oil headlines and the jobless-claims/labor follow-through for a risk tone change.

## 12. Final Verdict per Mode

- **Crypto scalp:** No clean actionable. Best structured idea SHORT HOME/USDT 65.1 is below threshold → **watchlist / no-trade**; high-vol-danger tape.
- **Crypto intraday:** No active trade clears threshold; NEAR 62.9 watchlist (late short). **No-trade.**
- **Crypto swing:** Report stale (>14 h); rely on active ZEC/XLM carry-forward signals only. **No fresh verdict.**
- **Stocks intraday:** **Stand aside at the open.** AVGO AVOID; semis longs do-not-chase; LLY watchlist (reassess on fresh levels). A-tier loss-bucket caveat applies.
- **Stocks swing / invest:** Reports stale (>14 h) → **excluded from fresh verdict**; no actionable.

## 13. Sources

- [Broadcom (AVGO) earnings report Q2 2026 — CNBC](https://www.cnbc.com/2026/06/03/broadcom-avgo-earnings-report-q2-2026.html) — 2026-06-03, single_source (AVGO beat EPS $2.44 vs $2.40, rev $22.19B +48% YoY; stock slid on AI guide / $100B FY27 target not raised).
- [US Stock Market Update June 4 2026 — ts2.tech](https://ts2.tech/en/stock-market-today-04-06-2026/) — 2026-06-04, single_source, **WebFetch-verified** (AVGO −15% premarket; CRWD −11%/4:1 split; Micron −6/7%, Marvell −7.5%, AMD/NVDA/INTC sympathy; Nasdaq-100 fut −1.3/1.4%, S&P −0.7%, Dow +0.5%; oil +2% Iran, 10y ~4.5%; jobless claims 4-month high).
- [Broadcom (AVGO) Q2 2026 Earnings Call Transcript — The Motley Fool](https://www.fool.com/earnings/call-transcripts/2026/06/03/broadcom-avgo-q2-2026-earnings-transcript/) — 2026-06-03, single_source.
- [S&P 500 June 4 open preview (Iran/oil) — Benzinga](https://www.benzinga.com/markets/prediction-markets/26/06/52993239/sp500-june-4-open-up-or-down-polymarket-iran-tensions-oil-prices) — 2026-06-04, single_source.
- Internal: `news_items` (db/crypto_ai_desk.sqlite) AVGO/AMD/Micron premarket rows (Yahoo/CNBC, 12:14–13:01Z); stocks legal-risk keyword scan → no hits; `catalyst_cycle_09-14.md`; reports as listed §2.

**Source-discipline checklist (§14/N):** every external claim has source + title + date + URL ✓ · no uncited stats ✓ · no uncited legal claims (none made) ✓ · no fabricated TradingView observations (chart tools declared not loaded) ✓ · missing source → declared, not guessed ✓ · test_source/fixture filtered ✓ · §13 present ✓ · web available (declared) ✓.

## 14. Fix Requests / TODO

### TODO-stocks-stale-postearnings
- **issue:** Stocks intraday report still surfaces AVGO as A-tier LONG 89.7 with a stale pre-earnings entry zone (~473–478) while AVGO is −15% (~$405–409) post-earnings — the score never absorbed the sell-the-news reaction.
- **evidence:** `data/reports/stocks/intraday/2026-06-04_11-15_stocks_intraday_report.md` §5 (AVGO A 89.7 long); external AVGO −15% (CNBC, ts2.tech); internal `news_items` 12:14–13:01Z "Broadcom dive / worst 1-day destruction".
- **suggested manual fix:** gate A/B scoring on a same-day earnings-reaction / price-vs-entry sanity check; demote or invalidate a long whose entry sits >X% above the live print after an earnings event.
- **priority:** high
- **first observed:** 2026-06-03 (now 5th consecutive review) — re-confirmed 2026-06-04 16:23 EEST.

### TODO-stocks-atier-winrate
- **issue:** Stocks A-tier is a persistent statistical loser vs B-tier.
- **evidence:** `signal-stats --asset-class stocks` this run: tier=A n=25, PF 0.29, totalR −5.0, winrate ~6.7% vs tier=B PF 1.33, totalR +15.
- **suggested manual fix:** audit the A-tier promotion threshold / penalty stack for stocks; A should not underperform B over a 25+ sample.
- **priority:** medium
- **first observed:** carried from prior reviews; re-confirmed 2026-06-04 16:23 EEST.

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol resolver leaves >75% of events unmapped, including clearly-tickered names (TLYS, RIVN).
- **evidence:** catalyst_events.jsonl 1424 total / 339 mapped / 1085 unmapped = 76.2% unmapped; top unmapped headlines name TLYS and RIVN explicitly.
- **suggested manual fix:** improve the symbol resolver to catch parenthetical tickers `(XXXX)` and common-name → ticker mapping in headlines.
- **priority:** medium
- **first observed:** multi-run regression; re-confirmed 2026-06-04 16:23 EEST.

### TODO-untracked-epic-alert
- **issue:** A B-tier crypto alert was sent to Telegram with no matching proposed_signal → it cannot contribute to PF/winrate/avgR.
- **evidence:** `detect_untracked_legacy_alerts --since 2026-06-04` → EPIC/USDT B scalp long, sent 2026-06-04T10:03:27Z, trackable=NO (no proposed_signal).
- **suggested manual fix:** investigate the alert→proposed_signal registration path for scalp B-tier (PART 1 regression); ensure every Telegram-sent alert writes a signal_id.
- **priority:** medium
- **first observed:** 2026-06-04 16:23 EEST (was None at 12:42 — new this run).
