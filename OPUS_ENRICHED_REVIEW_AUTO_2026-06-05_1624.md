# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

- **Generated:** 2026-06-05 16:24 EEST (auto-enriched-review, scheduled task `opus-enriched-review-preus`, **pre-US-open decision review** slot 16:20). US cash session opens **16:30 EEST (09:30 ET) — ~6 minutes away**, essentially at the open.
- **Slot focus:** the final pre-open read — gap risk, overnight catalysts, and which A/B setups become actionable once the US session opens. Crypto is **live actionable** now; stock signals are **pre-open planning** and become actionable only on fresh post-open levels.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-05_1145.md` (≈4.6 h ago, Europe / pre-US context slot — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). This run verified the **pre-open futures gap** (Nasdaq-100 e-mini −1.12%, AVGO −13% premarket, $56B FY AI-chip guide; jobs beat +172K), **BTC ~$62.8K with overnight low ~$61.3K** (CoinDesk WebFetch opened cleanly; BlockchainReporter returned HTTP 403 → search-corroborated), and the **LLY A-tier long** fundamentals (consensus Buy, target ~$1,215–1,250, Q1 rev +56%, FY guide $82–85B).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **This is a sector-rotation gap, not a broad risk-off crash — and that is the key pre-open distinction.** Futures: **Nasdaq-100 e-mini −1.12%**, S&P futures lower, **Broadcom −13% premarket** on a soft FY AI-chip guide ($56B vs ~$57.6B est.), dragging **MRVL −7%, AMD −4%, NVDA** lower. BUT the **May jobs report beat (NFP +172K, unemployment 4.3% unchanged)** and the **Dow closed at a record Thursday** while the Nasdaq fell. So the tape is **derating the AI/semis complex specifically**, with money rotating into value/defensives — not a wholesale de-risking.
- **Crypto remains the weak, correlated mirror of the AI unwind — no clean actionable.** BTC ~**$62.8K**, with an **overnight low ~$61,351** (CoinDesk: "lowest since February"; ETF outflows a record **13-day / ~$4.4B** streak). **$60K is the line in the sand → a clean break opens $55K.** Daily/weekly RSI deeply oversold (relief-bounce risk for shorts), 30-day IV 53 (highest since April). Crypto regime **bearish trend (risk-off)**, BTC/ETH downtrend, breadth **20.8% > EMA20**, **BTC ATR percentile 94 (elevated)**. No A-tier; the only B-tier idea (**ADA short 66.4**) is below the active threshold and tagged **"late_short_after_exhaustion."**
- **The cleanest stock long for the open is the one OUTSIDE the AI trade: LLY (A-tier 86.1).** Eli Lilly is a pharma/GLP-1 mega-cap with **Q1 2026 revenue +56% YoY, FY guide raised to $82–85B, consensus Buy (~$1,215–1,250 target)** — structurally insulated from the semis derating, with no near-term earnings risk. It is the highest-conviction name that is **not fighting today's dominant catalyst.** Still: A-tier stocks are the worst-performing bucket (PF 0.20, −8R) and it would be a long into a red-futures tape → **watch for a post-open hold, half-size, no pre-open entry.**
- **Integrity carry-over STILL OPEN: UNH is STILL emitted as an A-tier (81.3) intraday LONG while under an active DOJ Medicare-fraud investigation.** Same `TODO-unh-legal-gate` flagged at 04:30 and 11:45 — **~12 h later the legal-risk gate has not blocked it.** Per §I this is a hard gate: **UNH → AVOID / MANUAL REVIEW REQUIRED regardless of score.** Fresh news also surfaces a **ZEC swing-LONG still active while ZEC crashed ~41–50% on a counterfeiting-vulnerability exploit** → INVALIDATED.
- **Net verdict for the open:** **Crypto = no-trade / watchlist, downside-skewed** — respect BTC $60–62K, beware an oversold relief bounce squeezing late shorts. **Stocks post-open:** **LLY = the watch-long (defensive, off-AI), half-size on a hold; AMD = wait for the 496–516 reclaim (in the selloff); NVDA = watch (in the selloff); UNH = AVOID (DOJ); SMCI = avoid (export-control).** No pre-open entries. Catalyst layer **context-only** (73% unmapped).

---

## 2. Data Used

**Internal — fresh (<4 h):**
- `data/reports/scalp/2026-06-05_11-35_scalp_report.md` (mtime 14:35 EEST; data freshness 11:15 UTC; ~1.8 h). Regime **bearish trend (risk-off)**; BTC/ETH downtrend; breadth 20.8% > EMA20; BTC ATR pct 94.
- `data/reports/intraday/2026-06-05_11-58_intraday_report.md` (mtime 14:58 EEST; ~1.4 h). Bearish; only B-idea SHORT ADA 66.4 (below threshold); ZEC −41% flush.
- `data/reports/stocks/intraday/2026-06-05_12-10_stocks_intraday_report.md` (mtime 15:10 EEST; ~1.2 h) — **MARKET CLOSED / after-hours** (data 12:10 UTC, pre-open); regime **bullish** (VIX 15.65) but A/B demoted to C; LLY A 86.1, NVDA B 76, UNH B 69.7.
- LLM packets: `data/processed/llm_analysis_packet.md` (intraday, 11:58 UTC), `data/processed/context_for_llm.md`. Adds the **ZEC counterfeiting-exploit catalyst** ("Zcash tumbles 50% as Hayes exits bag over unverifiable counterfeiting risk" — CryptoBriefing).

**Internal — STALE (>14 h, planning-only, excluded from final swing/invest verdicts):**
- `data/reports/swing/2026-06-04_14-44_swing_report.md` (crypto; ~22.7 h).
- `data/reports/stocks/swing/2026-06-04_14-55_stocks_swing_report.md` (~22.5 h).
- `data/reports/stocks/invest/2026-06-04_15-01_stocks_invest_report.md` (~22.4 h).

**Catalyst / narrative:** `data/catalysts/2026-06-05/` — `catalyst_events.jsonl` (**1675 rows**; 696 unique per report), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_11-58.md` (mtime 14:58).

**CLI / DB:** `active-signals` (crypto **15**, stocks **50**), `signal-stats` (crypto + stocks, week — read in fresh reports), `detect_untracked_legacy_alerts --since 2026-06-05` → **0 untracked** (clean, no regression).

**External (this run — cited §13):** Pre-open futures gap (TheStreet, Yahoo Finance, Bloomberg); BTC levels/ETF outflows (CoinDesk WebFetch-verified, CNBC, BlockchainReporter); LLY forecast/fundamentals (MarketBeat/StockAnalysis); UNH DOJ (Yahoo, carry-forward re-confirmed).

**Unavailable / blind:** live tick prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps, order-book/CVD, live ETF-flow feed; live social beyond RSS-bridged `t.me/*`.

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-05_default_schedule/`.
- `scheduler.log` mtime **16:01 EEST → ~0.4 h** (fresh; scheduler **actively mid-cycle 1/12**, booted 16:01, regenerating reports now). Latest cycle summary anywhere: `cycle_08_14-12_summary.md` mtime **15:12 EEST → ~1.2 h** (fresh, under 3 h). Today's folder has no cycle summary yet (cycle 1 still running).
- **NO DEFER** — `scheduler.log` is fresh (well under the 3 h rule); the BOTH-stale condition is not met.
- **Fresh (<4 h):** crypto scalp (~1.8 h), crypto intraday (~1.4 h), stocks intraday (~1.2 h).
- **STALE (>14 h, excluded from final swing/invest verdicts):** crypto swing (~22.7 h), stocks swing (~22.5 h), stocks invest (~22.4 h) — no regeneration since the 06-04 14:44–15:01 batch → `TODO-swing-invest-staleness` (§14) carries forward.
- **Note:** because the scheduler is mid-cycle, fresher 16:0x reports may land minutes after this review; re-read before acting on any signal at the open.

---

## 4. What Changed vs Previous Review (11:30 → 16:20)

- **Slot advanced from Europe/pre-US to the pre-US-open decision read. The US open is now ~6 min away (vs ~4.75 h at 11:45).** The macro thread is unchanged but now has **live pre-open prints**: the AVGO-led AI/semis derating is **confirmed gapping into the cash open** (Nasdaq-100 futures −1.12%, AVGO −13% premarket), while a **jobs beat + Dow record** reframes it as a **sector rotation, not a broad crash** — a more constructive read than the flat "risk-off" framing at 11:45.
- **`TODO-unh-legal-gate` STILL OPEN (~12 h).** UNH still emitted A-tier 81.3 intraday long under an active DOJ probe; the gate has not been patched (expected — advisory routine). **CONFIRMED still AVOID.**
- **LLY surfaced as the headline A-tier long this slot (86.1) — a genuinely new, cleaner candidate.** The 11:45 review centered on AMD as the "least-bad" stock long; this run, **LLY is the cleanest because it sits OUTSIDE the AI-trade derating** (pharma/GLP-1), with strong verified fundamentals. Reframes the best stock long from "wait on a falling semis knife" to "watch a defensive leader hold the open."
- **BTC roughly flat-to-lower vs 11:45 (~$62K then, ~$62.8K now with an overnight $61.3K probe).** Still pinned to the $60–62K cascade zone; no breakdown, no reclaim. New colour: **RSI deeply oversold + IV 53** → elevated relief-bounce risk that argues *against* chasing crypto shorts here.
- **New crypto invalidation: ZEC.** Fresh CryptoBriefing/lookonchain prints confirm **ZEC −41% (24h) / ~−50% on a counterfeiting-vulnerability exploit, Hayes exiting** — yet a **ZEC swing-LONG remains active**. Thesis is gone → INVALIDATED (was flagged at 11:45 as a −37% flush; now confirmed exploit-driven and deeper).
- **Crypto B-short list rotated again:** 11:45's FET/NEAR → this run's **ADA** as the lone (sub-threshold) B-short; FET/NEAR/PUMP now C/watchlist. Same "don't chase the flush" discipline.
- **Catalyst mapping ~unchanged:** 74.0% unmapped (11:45) → **73.4% unmapped** this run. Still context-only. Stock→/USDT mismaps persist (AVGO/USDT 42, NVDA/USDT 31, UNH/USDT 17).
- **Untracked legacy alerts: still 0** (clean, no regression).

---

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl`: **1675 rows** (report dedupes to **696 unique**).
- Mapped (non-null symbol): **445** · Unmapped (null symbol): **1230** · **Unmapped = 73.4%**.
- `narrative_baskets`: **3** — `perps_dex_narrative` (HYPE primary; `wait_pullback`; <6h), `ai_narrative` (NEAR/RENDER/TAO/FET; `related_beta_rotation`; <6h), `momentum_breakout` (BABY/LA/HEI; `avoid_chase`; <1h).
- **⚠ CATALYST MAPPING WEAK THIS RUN (73.4% unmapped > 50%) — use the catalyst layer as CONTEXT, NOT a final decision input.**
- **Top-3 unmapped headlines:** (1) "South Korea is the ultimate backdoor tech play — but stock investors now face a looming threat" (MarketWatch); (2) "'A blanket ban' — U.S. senators push regulators to ease crypto capital rules" (AMBCrypto); (3) "White House crypto adviser Witt defends Clarity Act, calls it 'pro-law enforcement'" (The Block).
- **Resolver quirk (integrity, recurring):** equities news is mapped to fake crypto pairs — AVGO/USDT (42), NVDA/USDT (31), UNH/USDT (17), TSLA/USDT (12), JPM/USDT (8), MSFT/USDT (7), COIN/USDT (6), SMCI/USDT (5), LLY/USDT (2), META/USDT (2) → `TODO-catalyst-stock-usdt-mismap` (§14).

---

## 6. Market Landscape

- **Macro driver (unchanged thread, now live):** Broadcom's FY AI-chip guide ($56B) → broad AI/semis derating. AVGO −13% premarket, MRVL −7%, AMD −4%. "Unwinds the AI trade" (Bloomberg). **Crucially, this is a rotation, not a rout:** NFP +172K / unemployment 4.3% (jobs beat), Dow closed at a record Thursday — value/defensives are absorbing the flow out of semis.
- **Crypto:** regime **bearish trend (risk-off)**; BTC/ETH downtrend; breadth **20.8% > EMA20 / 18.75% > EMA50**; BTC ATR percentile **94 (elevated)**. BTC ~**$62.8K** (overnight low ~$61.3K), $60K floor, $55K below. ETF outflows record **13-day / ~$4.4B**. Broad altcoin flush: **ZEC −41% (exploit), INJ −16%, NEAR −16/17%, ADA −14%, NIGHT −10%**. RSI deeply oversold + IV 53 → relief-bounce risk. Desk style: **short bias or no trade; avoid weak altcoin longs.**
- **Stocks (pre-open):** the fresh stocks-intraday report's own regime label reads **bullish (VIX 15.65, breadth 100%)** — but it is a **pre-open snapshot (12:10 UTC) that does NOT yet price the AVGO gap**; the live futures tape is **red and semis-led**. Strongest sectors on the report: **semiconductors (SMH RS +11%), technology (XLK +10%)** — exactly the complex now derating, so treat that strength as **stale/about-to-reprice**. Healthcare (XLV, +1.4% RS) is the relative haven that **LLY** sits in.

---

## 7. Candidate Deep Dives (≤5)

### 7.1 LLY — stocks, A-tier 86.1 intraday LONG (waiting) — **WATCH (post-open hold, half-size; cleanest off-AI long)**
- **Signal:** intraday long, A-tier 86.1 (also B-tier 65 waiting). Entry in the ~$1,2xx zone (active-signals truncated; report tier A, confidence high, penalty −4.0).
- **Catalyst (verified §G):** Eli Lilly — **Q1 2026 revenue ~$19.8B, +56% YoY**, GLP-1 (Mounjaro/Zepbound) demand; **FY guide raised to $82–85B, adj EPS $35.50–37.00**; consensus **Buy, avg target ~$1,215–1,250** (range $850–1,500). Phase 3 retatrutide/oral-GLP-1 readouts positive. Fresh tailwind: TD Cowen raised GLP-1 market to $150B by 2030; CVS news positive for LLY (internal). **No near-term earnings risk** (report: safe).
- **Price-reaction / chase (§J):** a long in a sector (**healthcare/pharma**) **outside** the AI/semis derating — the one major long not fighting today's catalyst. But it would still be a long into a **red-futures open**, and **A-tier stocks are the worst bucket (PF 0.20, −8R, 6% winrate)**. Cannot verify live structure (no chart MCP).
- **Verdict:** **WATCH** — the highest-conviction, best-insulated stock long. Actionable only on a **post-open hold/reclaim, half-size**; no pre-open entry, no chase if it gaps up with the defensive rotation.

### 7.2 UNH — stocks, A-tier 81.3 + B 70 + B 73 (swing) LONG (triggered/waiting) — **AVOID / MANUAL REVIEW REQUIRED**
- **LEGAL / HEADLINE RISK (verified §G/§I):** UnitedHealth is under an **active DOJ Medicare-fraud investigation (criminal + civil)**; shares fell ~16% on the probe; first guided revenue decline in a decade (Yahoo 2025-07-31, Phemex 2026, SEC 10-Q FY2026; catalyst layer flags 17 UNH/USDT legal_risk rows today).
- **Internal contradiction:** the desk **still emits UNH A-tier 81.3 intraday long** (stale carry-forward) while the fresh stocks report demotes it to **B/C** and prior fresh intraday scoring rejected it (long_in_risk_off). Legal gate **not enforced ~12 h after first flag.**
- **Verdict:** **AVOID** — a clean long on a stock under active federal fraud investigation. Never actionable. (`TODO-unh-legal-gate`, high.)

### 7.3 AMD — stocks, B-tier 78.3 invest LONG (waiting_for_entry) — **WAIT (496–516 reclaim, half-size, post-open only)**
- **Catalyst (verified §G):** AMD is **−4% premarket**, dragged directly by the AVGO AI-chip guide miss; it is **inside** the semis derating, no AMD-specific bad news but the sector is the headwind.
- **Price-reaction / chase (§J):** entry zone **496.69–520.82** (invalidation 448.43), still `waiting_for_entry` below price → entering now = catching a falling semis knife. Actionable only on a **496–516 reclaim with post-open confirmation, half-size.**
- **Verdict:** **WAIT** — fighting the tape and the catalyst; no chase.

### 7.4 ADA/USDT — crypto, B-tier 66.4 intraday / scalp SHORT (waiting) — **NO-TRADE (sub-threshold, late)**
- **Signal:** intraday short 66.4 (entry failed-bounce 0.1651–0.1676, invalidation 0.1706, TP1 0.1585). The **lone B-tier crypto idea**, but **below the active-trade threshold** — the desk itself labels it watchlist/no-trade.
- **Price-reaction / chase (§J):** ADA **−13.82% 24h / −29.76% 7d** (6-year low), agent warning **"late_short_after_exhaustion"** + **>2 ATR considerations**; funding mildly negative, OI fallback. With BTC deeply oversold (relief-bounce risk), a fresh short here is the wrong side of a possible squeeze.
- **Verdict:** **NO-TRADE** — only on a clean failed bounce back into 0.1651–0.1676; do not chase the breakdown.

### 7.5 ZEC/USDT — crypto, swing LONG (active) — **INVALIDATED (exploit-driven crash)**
- **Catalyst (verified internal §G):** **"Zcash tumbles 50% as Hayes exits bag over unverifiable counterfeiting risk"** (CryptoBriefing); lookonchain: a counterfeiting vulnerability triggered a ~50% plunge, Garrett Jin shorted the rally for $21.5M unrealized. Report: ZEC **−41.11% 24h** (weakest symbol).
- **Verdict:** **INVALIDATED** — a swing-LONG is still active while the underlying suffered an exploit-driven ~41–50% crash; the long thesis is gone. Treat as closed/no-trade → `TODO-zec-invalidated-long` (§14).

---

## 8. Best Candidates Ranked

**No clean pre-open actionable candidates.** Ranked by least-bad / conditional quality for the open:

1. **LLY (stocks, A long)** — *WATCH, half-size on a post-open hold.* The cleanest long: defensive pharma/GLP-1, **outside** the AI derating, strong verified fundamentals. No pre-open entry.
2. **AMD (stocks, invest long)** — *conditional WAIT.* Only on a 496–516 reclaim with post-open confirmation; inside the semis selloff.
3. **NVDA (stocks, watch)** — inside the selloff; watch for a reclaim, no entry pre-open.
4. **ADA (crypto, short)** — valid bias, sub-threshold and late; wait for a failed bounce into 0.1651–0.1676. Do not chase into oversold/relief-bounce risk.

Everything else = watchlist / no-trade.

---

## 9. Avoid / No Trade

- **UNH (A 81.3 / B 70 / B 73 long)** — **AVOID.** Active DOJ criminal+civil Medicare-fraud investigation; stale A-tier carry-forward; legal gate unenforced. (§7.2)
- **SMCI (C 79.7 / 76 long)** — **AVOID/CAUTION.** Unresolved board-led export-control review + auditor history; inside the semis selloff; fresh intraday rejected (no_trade 51.58). (carry-forward)
- **ZEC (swing long)** — **INVALIDATED.** ~41–50% crash on a counterfeiting-vulnerability exploit; thesis gone. (§7.5)
- **AVGO / MSFT / TSLA (C-tier intraday shorts)** — bias aligns with the tape, but **C-tier / not actionable**, and **AVGO is already −13%** (chasing the gap). No entry.
- **All long AI/semis at the open (NVDA 76, SMH, AMD)** — fighting a confirmed semis derating + red futures; no pre-open entries, post-open reclaim only.
- **Crypto longs broadly** — bearish/elevated-vol tape; no longs.

---

## 10. Main Risks

- **Oversold relief-bounce squeezes late crypto shorts.** BTC RSI deeply oversold (daily+weekly), IV 53 (highest since April) — the ADA/altcoin shorts could get squeezed on any BTC reclaim of $63–64K. The desk's own "late_short_after_exhaustion" tag is the warning.
- **Gap-direction misread:** treating the AVGO semis gap as broad risk-off would over-short. The jobs beat + Dow record say **rotation**, not rout — value/defensives (incl. LLY's healthcare) may be *bid* even as semis bleed.
- **Stale-carry-forward A/B signals contradict fresh scoring + the live tape.** UNH (A 81.3) under DOJ; the stocks report's "bullish / semis-strong" regime is a **pre-gap 12:10-UTC snapshot** that does not price the AVGO open. Anyone reading `active-signals` raw could be misled. (→ §14)
- **Legal-risk gate not enforced (UNH)** — a federal-fraud name still top A-tier long. High-priority defect, ~12 h open.
- **BTC $60K cascade** — a clean break opens $55K; elevated ATR (pct 94) demands wide stops.
- **Catalyst layer 73.4% unmapped + stock→/USDT mismaps** — low signal; context only.
- **Swing/invest reports ~22 h stale** — excluded from final swing/invest verdicts.
- **Source-ingest note:** if `ingest_enriched_review_sources` fails for the cited JSON it is logged here; the review still stands (ingest is idempotent, advisory-only).

---

## 11. Action Plan — next 4 hours (into / through the 16:30 EEST US open)

1. **At the open (16:30 EEST / 09:30 ET):** expect **semis/AI to gap down** (AVGO/MRVL/AMD/NVDA) and **value/defensives to hold or bid**. Do **not** read the semis gap as broad risk-off.
2. **Stocks — watch, do not pre-position:** **LLY** = the cleanest long (off-AI, defensive); only a **post-open hold/reclaim, half-size**. **AMD** = watch the **496–516** invest zone for a post-open reclaim, half-size. **NVDA** = watch for a reclaim. **UNH = do-not-touch (DOJ). SMCI = avoid (export-control).** Re-read the post-open stocks report (fresh 16:0x levels) before any entry.
3. **Crypto — stand aside / watchlist:** respect BTC **$60–62K**; **do not chase shorts** into deeply-oversold conditions (relief-bounce risk). Only consider an ADA short on a **failed bounce into 0.1651–0.1676**, not at current extended prints. No longs.
4. **Monitor:** BTC $60K line + any reclaim of $63–64K (squeeze); AVGO/semis follow-through vs stabilization at the open; whether LLY/healthcare actually catches the rotation bid; any fresh UNH DOJ headline.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO-TRADE / watchlist.** Bearish/elevated-vol; ADA short sub-threshold + "late after exhaustion"; oversold relief-bounce risk; B-tier triggered winrate 25%.
- **Crypto intraday:** **NO-TRADE.** No fresh A/B above threshold; only a conditional ADA short on a failed bounce; otherwise stand aside.
- **Crypto swing:** **NO-TRADE.** Report ~22.7 h stale (excluded); **ZEC swing-long INVALIDATED** by the exploit-driven ~41–50% crash.
- **Stocks intraday (pre-open):** **LLY = WATCH (post-open hold, half-size, off-AI) — best long; AMD watch 496–516 reclaim (half-size, post-open); NVDA watch; UNH AVOID (DOJ); SMCI avoid.** No pre-open entries.
- **Stocks swing (stale ~22 h — planning only):** **LLY/AMD long bias intact (wait for confirmation); UNH excluded (legal).** Not actionable on stale data.
- **Stocks invest (stale ~22 h — planning only):** **AMD entry 496–520 bias consistent; LLY long-term bias constructive; SMCI/UNH excluded.** Re-confirm on fresh data.

---

## 13. Sources

- [Stock Market Today (June 5, 2026): S&P 500 futures fall on chip stock weakness — TheStreet, 2026-06-05](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-05-2026)
- [Nasdaq Futures Plunge as Broadcom Sinks on Disappointing AI Chip Sales Forecast — Yahoo Finance, 2026-06-05](https://finance.yahoo.com/markets/stocks/articles/nasdaq-futures-plunge-broadcom-sinks-103616197.html)
- [Tech Stocks Retreat as Broadcom Outlook Unwinds AI Trade, S&P 500 Futures Down — Bloomberg, 2026-06-04](https://www.bloomberg.com/news/articles/2026-06-04/nasdaq-100-futures-drop-as-broadcom-forecast-spooks-traders)
- [Bitcoin selloff continues as prices slide below $63,000 for the first time since February — CoinDesk, 2026-06-04 (WebFetch-verified: low-$60k support, $50k below, IV 53.17)](https://www.coindesk.com/markets/2026/06/04/bitcoin-selloff-continues-as-prices-slide-below-usd63-000-for-the-first-time-since-february)
- [Bitcoin set to slump to new lows for 2026 after recent sell-off, traders forecast — CNBC, 2026-06-03](https://www.cnbc.com/2026/06/03/bitcoin-to-slump-to-new-lows-after-recent-sell-off-traders-predict.html)
- [Bitcoin Price Today: BTC at $62,875 as ETF outflows hit record $4.4B over 13 days — BlockchainReporter, 2026-06-05 (WebFetch HTTP 403; search-corroborated)](https://blockchainreporter.net/bitcoin-price-today-btc-at-62875-as-etf-outflows-hit-record-4-4b-over-13-days/)
- [Eli Lilly (LLY) Stock Forecast and Price Target 2026 — MarketBeat, date unavailable](https://www.marketbeat.com/stocks/NYSE/LLY/forecast/)
- [Eli Lilly (LLY) Stock Forecast & Price Targets — StockAnalysis, date unavailable](https://stockanalysis.com/stocks/lly/forecast/)
- [With UnitedHealth Under DOJ Investigation, Should You Buy, Sell, or Hold UNH Stock Now? — Yahoo Finance, 2025-07-31 (carry-forward, re-confirmed)](https://finance.yahoo.com/news/unitedhealth-under-doj-investigation-buy-110002685.html)
- Internal: `data/catalysts/2026-06-05/` ("Zcash tumbles 50% as Hayes exits bag over unverifiable counterfeiting risk" — CryptoBriefing, single_source; "Crypto's worst week since July 2024 deepens" — CoinDesk, single_source; UNH legal_risk rows — QuiverQuant/Yahoo/Phemex).

---

## 14. Fix Requests / TODO

### TODO-unh-legal-gate
- **issue:** UNH still emitted as A-tier 81.3 intraday LONG (plus B 70 / B 73 swing) while under an active DOJ criminal+civil Medicare-fraud investigation; the legal/headline-risk gate does not block or demote it. Same defect flagged at 04:30 and 11:45, still open ~12 h later.
- **evidence:** `active-signals --asset-class stocks` shows a UNH A-tier 81.3 triggered long; DOJ probe verified (Yahoo 2025-07-31, Phemex, SEC 10-Q); catalyst layer carries 17 UNH legal_risk rows today.
- **suggested manual fix:** add a hard legal-risk gate (DOJ/SEC/indictment/antitrust/fraud keyword → cap tier at C or force AVOID) in the stocks scoring/risk-penalty layer; backtest against UNH/SMCI.
- **priority:** high
- **first observed:** 2026-06-05 04:30 EEST (re-confirmed 11:45 and 16:24 EEST)

### TODO-zec-invalidated-long
- **issue:** A ZEC swing-LONG remains active while ZEC crashed ~41% (24h) / ~50% on a counterfeiting-vulnerability exploit (Hayes exiting). A long signal should be auto-invalidated when its symbol suffers an exploit/security-risk catalyst + a >X% adverse move.
- **evidence:** `active-signals --asset-class crypto` shows a ZEC swing long; report §2 lists ZEC −41.11% (weakest); LLM packet/CryptoBriefing: "Zcash tumbles 50% ... unverifiable counterfeiting risk."
- **suggested manual fix:** wire the catalyst `exploit_hack`/security-risk type into an invalidation/auto-expire path for active same-direction longs; alert on contradiction (active long vs exploit catalyst).
- **priority:** medium
- **first observed:** 2026-06-05 16:24 EEST

### TODO-stocks-regime-pregap-snapshot
- **issue:** The fresh stocks-intraday report (12:10 UTC, pre-open) labels the regime **bullish** with semiconductors/technology as the strongest sectors — exactly the complex now derating in pre-open futures (AVGO −13%, Nasdaq-100 −1.12%). The pre-gap snapshot can mislead a reader into a long-semis bias right before a semis-led gap down.
- **evidence:** `data/reports/stocks/intraday/2026-06-05_12-10_stocks_intraday_report.md` §1–2 (bullish, VIX 15.65, SMH RS +10.98%) vs external pre-open futures (Yahoo/TheStreet/Bloomberg, 2026-06-05).
- **suggested manual fix:** when generating a pre-open (market-closed) stocks report, ingest index/sector **futures** (or at least stamp "pre-gap, does not reflect overnight futures") so the regime label degrades gracefully into the open.
- **priority:** medium
- **first observed:** 2026-06-05 16:24 EEST

### TODO-swing-invest-staleness
- **issue:** Crypto swing, stocks swing, and stocks invest reports are all ~22 h old (06-04 14:44–15:01) — not regenerated overnight, so swing/invest verdicts run on stale data.
- **evidence:** mtimes — `swing/2026-06-04_14-44` (~22.7 h), `stocks/swing/2026-06-04_14-55` (~22.5 h), `stocks/invest/2026-06-04_15-01` (~22.4 h).
- **suggested manual fix:** confirm the swing/invest cadence in the scheduler config; if intended (lower frequency), surface the expected next-regen time in reports so staleness is not mistaken for a failure.
- **priority:** low
- **first observed:** 2026-06-05 11:45 EEST (recurring)

### TODO-catalyst-stock-usdt-mismap
- **issue:** The catalyst symbol resolver maps equities news to fake crypto pairs — AVGO/USDT (42), NVDA/USDT (31), UNH/USDT (17), TSLA/USDT (12), JPM/USDT (8), MSFT/USDT (7), COIN/USDT (6), SMCI/USDT (5), LLY/USDT (2), META/USDT (2). Pollutes crypto catalyst mapping and inflates noise.
- **evidence:** `data/catalysts/2026-06-05/catalyst_events.jsonl` top mapped symbols include 10+ stock tickers suffixed `/USDT`.
- **suggested manual fix:** gate `/USDT` suffixing to known crypto bases (or carry asset_class through) so equity tickers don't resolve to crypto pairs.
- **priority:** low
- **first observed:** 2026-06-05 11:45 EEST (recurring)

### TODO-catalyst-mapping-weak (recurring)
- **issue:** Catalyst unmapped rate 73.4% this run (74.0% at 11:45, 72.4% at 04:30) — persistently above 50%, keeping the catalyst layer context-only across runs.
- **evidence:** 1230/1675 unmapped today; 11:45 review 74.0%; 04:30 review 72.4%.
- **suggested manual fix:** improve the catalyst→symbol resolver (alias table, entity extraction) to push mapped rate above 50% so the layer can contribute to decisions.
- **priority:** medium
- **first observed:** 2026-06-05 04:30 EEST (recurring)
