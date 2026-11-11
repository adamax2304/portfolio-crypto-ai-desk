# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:24 EEST

## 1. Executive Summary

**Tuesday 2026-06-16, 16:24 EEST "pre-US-open decision review" slot — ~6 minutes before the US cash open (16:30 EEST / 09:30 ET).** External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch-verified: BTC **~$65,940**, range $65–66K, resistance $67K, support $64K → $63.3K; **FOMC begins today, decision tomorrow Wed Jun 17, ~98% hold** at 3.50–3.75%, Warsh's first meeting).

**The pre-open read: do NOT chase the pre-market — wait for the first 15–30 min of RTH.** US index futures are **flat-to-slightly-lower into the Fed**, regime still **risk_on** (VIX 16.11, breadth 75% > EMA20, QQQ/IWM/DIA uptrending). The dominant single-stock story is **SpaceX (SPCX) +8.9% premarket** after a +19.6% debut day (>$2T valuation) — that is an IPO-momentum gap, **not** a desk signal, and the spillover narrative ("a veteran investor kicks Tesla out of the Mag-7, replaced by another tech giant") is mildly **bearish for TSLA specifically**, which contradicts the desk's lone stock B-tier (TSLA 65.96). **Gap risk is elevated and FOMC is tomorrow → keep size modest, require RTH confirmation, no pre-market chase.**

**Crypto stays risk-on but range-capped and pinned at the $67K pivot into FOMC.** BTC briefly tagged **$67,236 (2-week high)** then settled back to the **$65–66K** range as the FOMC meeting opened; resistance **$67K** (targets $68.5–70K on a clean break), support **$64K → $63.3K**. ETH ~$1,817 (now the **unusual-volume name, 2.33×**, +RWA-flow catalyst), SOL ~$74. Alt breadth **79.5% > EMA20 / 84.1% > EMA50** (improved vs morning). **Tailwinds firmed since 11:45:** BTC spot ETFs logged **+$85.9M net inflows (broke a 13-day outflow streak)** — a flip from Monday's −$64.8M; **Strategy added 1,587 BTC**; **Hyperliquid (HYPE) +10.4%** on SpaceX-IPO derivatives volume; Iran peace **signing ceremony now set for Fri Jun 19 in Switzerland**.

**Routing — longs / wait-for-confirmation; no fresh shorts (both classes).** Evidenced: crypto **A/B triggered winrate 16.9%, PF 1.25**, scalp lane **research-grade (PF 0.14 / low-confidence overlay)**; crypto **shorts PF 0.5 (−3R)** vs longs PF 1.3. Stocks **A/B winrate 20%, PF 0.93 (−1R)**; **shorts PF 0.5 (−19R)** vs longs PF 1.2 — shorting bleeds in risk-on. Route to RS-leader longs on pullbacks / RTH confirmation; do not chase.

**Best actionable-after-open stock long: AMD** (active B-tier 77 intraday triggered + swing 88; AI-semis rotation, Citi Buy upgrade; yesterday's A-tier triggers have now **expired pre-open** → use fresh RTH levels, not the stale trigger). **Cleanest crypto longs: INJ** (B 74.8, RS leader, pullback 5.866–5.928) and **ETH** (B 71, unusual-volume + RWA catalyst, pullback 1805.88–1813.79). **AVOID: UNH** (active DOJ Medicare-fraud probe, −16%), **SMCI** (export-control indictment). **Integrity regression: untracked legacy crypto alerts jumped 1 → 14** (scalp/intraday alerts with no proposed_signal) — §14 TODO. **Catalyst mapping weak (76.5% unmapped) — context only.** Advisory only; scanner/collection/tracking continue in all moods — nothing here says stop the system.

## 2. Data Used

- **Crypto scalp report** `data/reports/scalp/2026-06-16_12-33_scalp_report.md` — **FRESH** (~0.85h; data freshness 12:15 UTC).
- **Crypto intraday report** `data/reports/intraday/2026-06-16_12-48_intraday_report.md` — **FRESH** (~0.6h; data freshness 12:30 UTC).
- **Crypto swing report** `data/reports/swing/2026-06-16_02-05_swing_report.md` — **carry-forward** (~11.3h, borderline-stale band; flagged §3).
- **Stocks intraday report** `data/reports/stocks/intraday/2026-06-16_13-08_stocks_intraday_report.md` — **FRESH** (~0.3h) but **market closed/pre-market → planning until the 16:30 open**.
- **Stocks swing** `…02-11…` (~11.2h) + **invest** `…02-16…` (~11.1h) → borderline-stale planning context (flagged §3).
- **Catalysts** `data/catalysts/2026-06-16/` present: `catalyst_cycle_12-49.md` (latest), `catalyst_events.jsonl`, `narrative_baskets.jsonl` (5 baskets). No catalyst-scan needed.
- **LLM packets** `data/processed/llm_analysis_packet.md` (crypto, ~0.59h) + `llm_stocks_packet.md` (stocks, ~0.27h).
- **Internal CLI:** `active-signals` crypto (**44 active, all long B**, scores 65–76) + stocks (**50 active**; B-tier AMD 77 / SMH 72 / JPM 67 / PLTR 65 triggered, rest C-tier); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-16` → **14 untracked** (regression).
- **External:** WebSearch ×2 (BTC level + FOMC; US premarket + SpaceX/Fed) + WebFetch (AnalyticsInsight verified BTC $65,940 / FOMC / HYPE +10.4% / Strategy +1,587 BTC / ETF +$85.9M). TheStreet stock URL returned **HTTP 403** → fell back to the search summary for the equity tape (declared here).
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-16T1324Z.json` (3 cited sources); ingest CLI run for **crypto** (`input 3 | valid 3 | wrote 3`) and **stocks** (`input 3 | valid 3 | wrote 3`).

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-16_default_schedule/`.
- `scheduler.log` mtime **16:08:38 EEST** (~0.26h old) → **FRESH**.
- Latest `cycle_*_summary.md`: `cycle_01_12-29_summary.md` mtime **13:08 EEST** (~3.27h).
- **Defer rule needs BOTH log AND latest cycle summary > 3h. Log is 0.26h fresh → review proceeds.**
- Freshness labels: crypto scalp/intraday **fresh**; crypto swing **carry-forward / borderline (~11.3h)**; stocks intraday **fresh but market-closed → planning**; stocks swing/invest **borderline-stale (~11.1h)** — excluded from fresh-swing verdict, used as planning context only. **Yesterday's stock A-tier triggers (AMD/SMH/JPM, 2026-06-15 14:32 UTC) have now expired pre-open** → not live entries; they re-appear as today's B-tier active signals (planning, RTH-confirmation required).

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-06-16_1145.md` (Europe / pre-US context):

- **Window moved pre-US → final pre-open (T-6 min).** Posture shifts from "build the RTH watchlist" → **"what to do at/after the cash open; gap + stale-data risk."**
- **BTC tested higher:** $66,304 (11:45) → **briefly $67,236 (2-week high), now ~$65,940** in the $65–66K range. The **$67K pivot was tagged and rejected** rather than just "pinned under" — still the decisive level into FOMC.
- **ETF flow flipped positive:** prior review had **BTC ETF −$64.8M Monday**; now **+$85.9M net inflows, breaking a 13-day outflow streak** — a genuine sentiment improvement.
- **Crypto leadership rotated:** INJ remains clean RS, but the **unusual-volume name is now ETH (2.33×)** with a fresh **RWA-flow catalyst** (was INJ this morning). JTO **+29%** and **PORTAL +41%** are the new overextended names (SYN faded). HYPE **+10.4%** on SpaceX-IPO derivatives volume — new.
- **FOMC now opening today** (was "tomorrow" framing at 11:45) — decision still Wed Jun 17; hold prob nudged to **~98%**. Iran signing **scheduled Fri Jun 19 in Switzerland** (concretized vs "finalized").
- **Stocks A-tier expired:** the AMD/SMH/JPM A-tier intraday triggers flagged at 11:45 as "expiring pre-open" **have now expired**; they re-surface as B-tier active signals. Fresh 13:08 stocks intraday report shows **no A/B, all C-tier** (market-closed demotion). TSLA is the lone B-tier top candidate but carries a **bearish Mag-7-removal narrative contradiction**.
- **Integrity regressed sharply:** untracked legacy crypto alerts **1 (11:45) → 14 (now)** — escalated §14 TODO (was a single ETH alert, now spans ETH/JTO/XLM/WLD/ZRO/XPL/GPS/INJ scalp+intraday).
- **Catalyst mapping still weak** (76.5% unmapped vs 77.0% at 11:45) — recurring §14.

## 5. Catalyst Coverage

- Raw `catalyst_events.jsonl` today: **2,731 rows; mapped (non-null symbol) 642; unmapped 2,089 = 76.5%.** (Intraday report dedups to "750 unique events; 5 baskets" — raw-vs-unique gap persists, §14.)
- **⚠ Catalyst mapping weak this run (76.5% unmapped) — use the catalyst layer as context, not final decision.**
- **Top 3 unmapped (by importance, all sector/macro/exploit):** (1) "Deprecated Thetanuts Vault Exploited for $2.1 Million in Latest DeFi Attack" (BeInCrypto, 0.75); (2) "Humanity Protocol sunsets H token after hack, launches airdrop to restore holders" (CryptoBriefing, 0.75); (3) "Exploit-Driven TVL Drop Pushes DeFi Leverage Back to 2021 Levels" (BeInCrypto, 0.73). DeFi-exploit cluster dominates the high-importance unmapped tail again → background risk-off tail in alts, not symbol-specific.
- **Narrative baskets (5):** **perps_dex_narrative** primary **HYPE/USDT** (<1h); **RWA/ONDO–XLM** (ONDO/XLM, <1h); **ai_narrative** (NEAR/RENDER/TAO/FET, <6h — but TAO −5.5% today, AI lane lagging); **delisting_thin_liquidity** (avoid_low_liquidity, <24h); **momentum_breakout** primary **PORTAL/USDT** (<1h, overextended +41%).
- **Legal/regulatory flags from the catalyst layer:** **SMCI** (export-control indictment, SEC EDGAR 8-K), **UNH** (DOJ Medicare-fraud probe, QuiverQuant, −16%). Both still mislabelled as `…/USDT` pairs (§14 resolver quirk).

## 6. Market Landscape

- **Crypto:** bullish trend / risk-on, range-capped, **pinned at the $67K pivot into FOMC**. BTC + ETH uptrend; alt breadth **79.5% > EMA20 / 84.1% > EMA50**, BTC ATR percentile **32 (normal vol)**. **BTC ~$65,940** (briefly $67,236), resistance **$67K** (→ $68.5–70K on break), support **$64K → $63.3K**. Funding broadly neutral, crowding normal. Strongest RS (scalp/intraday): **JTO 91.6 (+29%, OI +44% — overextended), INJ 84–85 (+9–10%), XLM 82 (+13%), WLD 80–83, PORTAL 79.9 (+41% — overextended), XPL 77.** **ETH is now the only unusual-volume name (2.33×)** + RWA-flow catalyst. Weakest: OPG −15%, MEGA −12%, BABY −6%, **TAO −5.5%** (AI lane lagging), TRUMP −4.8%. Tailwinds: ETF **+$85.9M inflows** (streak broken), Strategy +1,587 BTC, HYPE +10.4%.
- **Stocks (pre-market, opening in ~6 min):** regime **risk_on, bias long, VIX 16.11**, breadth 75% > EMA20; QQQ/IWM/DIA uptrend, SPY range. **Index futures flat-to-slightly-lower into the Fed.** Strongest sectors semis (SMH +16.3% 20d) / tech. **No fresh A/B in the 13:08 report (all C-tier, market-closed demotion);** active B-tier carry-overs **AMD 77 / SMH 72 / JPM 67 / PLTR 65** (planning, RTH-confirmation). Dominant catalyst: **SpaceX (SPCX) +8.9% premarket** (IPO momentum, not a signal); TSLA narrative mildly negative (Mag-7 removal). Week stats: **longs PF 1.2, shorts PF 0.5 (−19R)** — long-only edge; A/B winrate 20%.

### Market Mood / Risk Routing  (REQUIRED — PART 4)
- **Crypto mood:**           **risk-on but range-capped + pre-FOMC** ($67K tagged & rejected, decision tomorrow, ETF inflows positive).
- **Stocks mood:**           **pre-market / opening** (regime risk_on; futures flat-to-lower into Fed; SpaceX-driven gap risk).
- **Dominant narrative:**    **SpaceX $2T IPO momentum** (SPCX +8.9% pre, HYPE +10.4% on its derivatives volume); **AI/semis rotation** (AMD/SMH leadership); **BTC ETF inflows return** + Strategy accumulation; Iran peace signing Fri Jun 19.
- **Preferred side now:**    **longs / wait-for-confirmation** (RS-leader + RTH/retest); **no fresh shorts** (crypto shorts PF 0.5, stock shorts −19R).
- **Best long candidate:**   **AMD** (stocks) — actionable **after RTH confirmation** post-open on fresh levels; crypto: **INJ** long-watch on pullback 5.866–5.928 (BTC >$64K).
- **Best short candidate:**  **none clean** — risk-on disfavours shorts. Short-watch only **after a failed retest of broken support AND BTC losing $64K** (weakest: OPG/MEGA, but thin/squeeze-prone).
- **Best catalyst-backed candidate:** **ETH** (crypto — unusual-volume 2.33× + RWA-flow news) / **AMD** (stocks — Citi Buy + AI-semis rotation, after RTH confirmation).
- **What to avoid:**         **UNH** (DOJ probe — legal AVOID), **SMCI** (indictment), **chasing SPCX/SPCX-spillover & TSLA pre-market**, overextended crypto (JTO +29%, PORTAL +41%), stock shorts, crypto scalp lane (PF 0.14), sizing into tomorrow's FOMC.
- **What would change the view:** BTC **clean acceptance >$67K on volume** (→ $68.5–70K continuation) or **loses $64K** (→ flush to $63.3K); **FOMC tomorrow hawkish surprise / Warsh hawkish bias** (→ risk-off); first 30-min RTH breadth confirming or fading the risk-on open.

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — AMD (stocks, active B-tier 77 intraday / swing 88) · best stock long — RTH-confirmation required
- **Setup:** strongest stock long; active B-tier intraday 77 (triggered) + swing 88 + C across modes. Yesterday's A-tier intraday trigger (2026-06-15 14:32 UTC) has **now expired pre-open** → do NOT use the stale 549.26 level.
- **Catalyst check (internal-first):** strongly catalyst-backed — Citi Buy upgrade (Jun 12), ~$900B valuation / memory-tech expansion, AI-inference rotation (semis +16.3% 20d). No legal/earnings risk in the sweep.
- **Price/chase:** A-tier trigger stale; stock longs carry the edge (PF 1.2) but A/B winrate is only 20% and A-tier has 0 closed (overpromotion caveat). Has price reacted? Part of the AI-semis run but not parabolic. Overextended? No. Mood-aligned: yes (risk_on, semis leadership). Long/short/wait: **long, only after RTH confirmation**. Actionable now? **No — wait first 15–30 min RTH** on fresh levels. Invalidation: loss of the opening-range low / prior-day support. Chase-risk: moderate if entered on the gap; low on a confirmed retest. Catalyst confirmation: yes.
- **Decision:** **PLANNING LONG → actionable after RTH confirmation post-16:30 EEST** on fresh levels. Top stock long into the open; do not act on the expired overnight trigger or chase the pre-market gap.

### Candidate 2 — INJ/USDT (crypto, B-tier 74.8 LONG) · cleanest crypto long
- **Setup:** RS leader, momentum **84–85**, **+9–10% 24h**, RS vs BTC +9%, **volume 1.15×**, B-tier score 74.8, intraday `actionable`. Tags: relative_strength. Derivatives: price up + OI up (fresh positioning, crowding normal); funding ~neutral.
- **Catalyst check (internal-first):** light — "Bitcoin rallies after Japan rate increase with XLM, INJ, UNI advancing" (CoinDesk, single_source); mostly technical RS. No legal flags.
- **Price/chase:** has price reacted? Yes (+9–10%) but cleanest non-parabolic RS of the cohort (cf. JTO +29%, PORTAL +41%). Entry now mid-range → **demand pullback into 5.866–5.928**. Overextended >2 ATR? No (current 5.955, ATR 0.137). Mood-aligned: yes. Long/short/wait: **long, pullback-only**. Actionable: on the pullback with BTC >$64K. Invalidation: 1h close beyond 5.791. Chase-risk: moderate. Catalyst: thin (technical).
- **Decision:** **LONG-WATCH, pullback-only (5.866–5.928), BTC-gated >$64K.** Best clean crypto long. Note scalp lane is research-grade (PF 0.14) — prefer the intraday/1h framing.

### Candidate 3 — ETH/USDT (crypto, B-tier 71 LONG) · best catalyst-backed crypto long
- **Setup:** B-tier 71, momentum 70.5, **the only unusual-volume name (2.33×)**, tags relative_strength + volume_expansion, **3 fresh catalyst items** (catalyst_news 12.3 — highest of cohort). +2.24% 24h / +8.37% 7d. Derivatives: price up + OI **down** (short-covering → weaker continuation quality); funding ~neutral.
- **Catalyst check (internal-first):** "XRP just beat ETH/SOL in 90-day RWA flows as traders pile back" (CryptoSlate); "Standard Chartered $100 UNI target / 40x" spillover (AMBCrypto). RWA narrative basket active (ONDO/XLM). single_source each but consistent and fresh.
- **Price/chase:** modest move (+2.2%) → not overextended; clean geometry. Pullback into 1805.88–1813.79 (current 1817.31, ATR 17.6). Mood-aligned: yes. Long/short/wait: **long, pullback-only**. Actionable: on pullback, BTC >$64K. Invalidation: 1h close beyond 1796.20. Chase-risk: low-moderate. Catalyst confirmation: yes (RWA flows + unusual volume) — but OI-down means it's partly short-covering, so size modestly.
- **Decision:** **LONG-WATCH (best catalyst-backed crypto), pullback into 1805.88–1813.79, BTC-gated >$64K.**

### Candidate 4 — TSLA (stocks, B-tier 65.96 intraday) · CONTRADICTION RISK — RTH-confirmation, no pre-market chase
- **Setup:** lone stock B-tier top candidate (65.96, long, medium confidence, risk penalty −4.0) in the fresh 13:08 report — but the report is market-closed → demoted to planning.
- **LEGAL/HEADLINE check:** no indictment/SEC/auditor/delisting flags found. **However, contradiction risk:** the desk's TSLA news rows are actually **SpaceX-driven** — "SpaceX +5/+8.9% premarket," "SpaceX overtaking Amazon," and a **bearish-for-TSLA** "veteran investor kicks Tesla out of the Mag-7, replaces it with another tech giant" (MarketWatch, 2026-06-16). The catalyst is mis-attributed sentiment, not a TSLA-specific bullish driver.
- **Price/chase:** acting on a pre-market move tied to SpaceX's IPO halo into an FOMC-eve session is chase-risk. Mood-aligned: partially (risk_on) but the symbol-level narrative is mixed-to-negative. Long/short/wait: **wait**. Actionable: only after RTH confirmation with TSLA holding its own level independent of the SpaceX pop. Invalidation: fade back below opening range. Chase-risk: high pre-market.
- **Decision:** **MANUAL REVIEW / RTH-CONFIRMATION REQUIRED — do NOT chase pre-market.** The B-tier long is weakened by a SpaceX-attributed, partly-bearish narrative; require independent RTH strength before treating as actionable.

### Candidate 5 — SMH + JPM (stocks, active B-tier 72 / 67) · semis + financials — planning, RTH confirmation
- **Setup:** B-tier active (SMH 72, JPM 67, triggered), carry-overs from yesterday's expired A-tier batch. SMH = semis ETF (sector RS leader, +16.3% 20d); JPM = financials (risk-on beneficiary).
- **Catalyst check:** SMH rides the AI-semis rotation (AMD/NVDA strength); JPM benefits from risk-on financials. No legal/earnings flags. PLTR (B 65) is the third carry-over — same treatment.
- **Price/chase:** same staleness logic as AMD — A-tier expired pre-open; A-tier has 0 closed (overpromotion caveat). Mood-aligned: yes. Long/short/wait: **long, RTH-confirmation only**. Actionable: post-open confirmation, not the gap.
- **Decision:** **PLANNING WATCH — semis (SMH) + financials (JPM) longs into the open; require RTH confirmation, do not chase the gap or the expired trigger.**

## 8. Best Candidates Ranked

1. **AMD — stocks PLANNING LONG (best stock long).** Trigger: **RTH confirmation after 16:30 EEST** on fresh levels (NOT the expired 549.26); catalyst Citi Buy + AI-semis rotation.
2. **INJ/USDT — crypto LONG-WATCH (cleanest crypto long).** Trigger: pullback **5.866–5.928**, BTC >$64K; invalidation 1h close < 5.791.
3. **ETH/USDT — crypto LONG-WATCH (best catalyst-backed).** Trigger: pullback **1805.88–1813.79**, BTC >$64K; RWA-flow + 2.33× volume; invalidation 1h close < 1796.20.
4. **SMH / JPM — stocks PLANNING WATCH (semis/financials).** Trigger: RTH confirmation post-open; sector-leadership longs.
5. **BTC — macro anchor / catalyst-watch.** Trigger: **clean acceptance >$67K on volume** → $68.5–70K; ETF inflows + Strategy accumulation are structural tailwinds; loses $64K → flush to $63.3K.

**Watch-side triggers (no fully clean entry pre-open):**
- **long-watch** AMD: first 15–30 min RTH holding above opening range (stocks); INJ pullback 5.866–5.928 + BTC >$64K (crypto).
- **short-watch** none clean → only **after a failed retest of broken support AND BTC losing $64K** (e.g. OPG/MEGA, thin/squeeze-prone — require confirmation).
- **catalyst-watch** ETH: hold above pullback zone + a second independent RWA-flow/inflow source.

## 9. Avoid / No Trade  (this decision window only)

- **UNH** — active DOJ criminal Medicare-fraud probe (−16%); legal **AVOID** despite active C-tier long signal.
- **SMCI** — export-control indictment (8-K); avoid on legal grounds.
- **Chasing the pre-market** — **SPCX +8.9%** (IPO momentum, not a signal) and **TSLA** (SpaceX-attributed, partly-bearish narrative); no entry without RTH confirmation.
- **Fresh shorts (both classes)** — risk-on; crypto shorts PF 0.5, stock shorts PF 0.5 / −19R. Shorts only after failed retest + BTC < $64K.
- **Overextended crypto** — **JTO (+29%, OI +44%), PORTAL (+41%)** — chase-risk; long-watch only on a deep defended pullback.
- **Crypto scalp lane** — PF 0.14, low-confidence overlay; research-grade only.
- **Sizing into tomorrow's FOMC** — keep size modest; decision Wed Jun 17, Warsh's first.
- **Note:** "no clean trade now" applies to **this pre-open window only** — scanner, candidate generation, tracking, and monitors continue in all moods.

## 10. Main Risks

- **FOMC tomorrow (Wed Jun 17) — Warsh's first meeting.** Hold ~98% priced; the dot plot / forward guidance is the catalyst. A hawkish bias shift flips risk-off → BTC back toward $64K then $63.3K, stock longs at risk. Expect compression into the print.
- **Gap / stale-data risk at the open.** Stock A-tier expired pre-open; the 13:08 report is market-closed (planning). Acting on stale levels or the SpaceX-driven gap risks a gap trap — require RTH confirmation.
- **BTC at the $67K pivot, just rejected.** Tagged $67,236 then back to $65–66K; failure to accept above + loss of $64K opens a flush; the rally remains headline/Fed-dependent.
- **TSLA narrative contradiction.** The B-tier long is propped by SpaceX sentiment with a bearish Mag-7-removal overlay — symbol-level conviction is weak.
- **Losing buckets:** stock shorts PF 0.5 / −19R; crypto A/B winrate 16.9%; crypto scalp PF 0.14. Execution discipline (pullbacks + RTH confirmation) matters more than candidate count.
- **§M ingest:** ran for **crypto** and **stocks** from the cited sources JSON (idempotent UPSERT, `wrote 3 row(s)` each). No ingest error. TheStreet stock URL 403'd → equity tape from search summary (declared §2).

## 11. Action Plan — next 4 hours (at/after the US open)

1. **Stocks (open 16:30 EEST):** do **NOT** chase the gap. Watch **AMD, SMH, JPM, PLTR** (longs) for **RTH confirmation in the first 15–30 min** on fresh levels; **suppress UNH** (legal); treat **TSLA** as manual-review (SpaceX-attributed narrative); ignore the expired A-tier triggers.
2. **Crypto:** watch **INJ** pullback 5.866–5.928 and **ETH** pullback 1805.88–1813.79 — pullback-only, BTC-gated >$64K; do not chase JTO/PORTAL.
3. **BTC level read:** **$67K** is the pivot — accept-above-on-volume = continuation toward $68.5–70K; lose **$64K** = step aside / flush risk to $63.3K.
4. **No fresh shorts** either class; **no new risk into tomorrow's FOMC** — keep size modest into the print.
5. **Re-check at the 18:30 US-open-reaction slot:** which pre-open ideas confirmed/failed, whether AMD/SMH triggered cleanly, fake moves / gap traps, breadth broad vs narrow, and BTC's $67K resolution.

## 12. Final Verdict per Mode

- **Crypto scalp:** research-grade only (PF 0.14, low-confidence). No conviction entries; data-collection continues.
- **Crypto intraday:** **selective LONG, pullback-only** — INJ (clean) / ETH (catalyst-backed), BTC-gated >$64K, no chase. No shorts.
- **Crypto swing:** carry-forward / borderline-stale; RS-leader longs (INJ/SOL/ETH/ZRO active) managed to invalidation; no fresh adds into FOMC.
- **Stocks intraday:** **closed → planning into the open.** Long bias (AMD/SMH/JPM/PLTR) for **RTH confirmation** after 16:30; UNH AVOID; TSLA manual-review; no shorts; no chase.
- **Stocks swing/invest:** borderline-stale carry-forward; semis/financials long bias intact; await RTH + post-FOMC clarity before fresh adds.

## 13. Sources

- [Crypto Prices Today: Bitcoin Fluctuating Between $65,000 to $66,000 as FOMC Opens, Strategy Adds 1,587 BTC, Hyperliquid Surges 10%](https://www.analyticsinsight.net/price-analysis/crypto-prices-today-bitcoin-fluctuating-between-65000-to-66000-as-fomc-opens-strategy-adds-1587-btc-hyperliquid-surges-10) — AnalyticsInsight, 2026-06-16 (WebFetch-verified: BTC $65,940; resistance $67K → $68.5–70K; support $64K/$63.3K; FOMC begins today, decision Jun 17, ~98.2% hold; HYPE +10.44%; Strategy +1,587 BTC; ETF +$85.9M, 13-day outflow streak broken).
- [Bitcoin Price Today: BTC At $66,000 — June 16, 2026 (Fed's big day, Warsh takes over)](https://blockchainreporter.net/bitcoin-price-today-btc-holds-66k-as-the-feds-big-day-arrives-and-warsh-takes-over/) — BlockchainReporter, 2026-06-16 (BTC ~$65,940 holding $65K; briefly $67,236 2-week high).
- [Stock Market Today (June 16, 2026): Dow futures hold steady ahead of Fed meeting](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-16-2026) — TheStreet, 2026-06-16 (futures flat-to-lower into FOMC; SpaceX/SPCX +8.9% premarket after +19.6% debut, >$2T valuation; rate hold expected; Iran peace signing Switzerland) — **URL returned HTTP 403 on WebFetch; content from WebSearch summary.**
- [When Is the Next FOMC Meeting? Full 2026 Schedule](https://coingape.com/trending/when-is-the-next-fomc-meeting-full-2026-schedule/) — CoinGape (FOMC Jun 16–17 schedule).
- **Internal:** `news_items` (UNH DOJ probe — QuiverQuant; SMCI 8-K indictment — SEC EDGAR; AMD Citi upgrade/$900B — MarketWatch/Benzinga/TipRanks; TSLA/SpaceX Mag-7-removal — MarketWatch); scalp + intraday + stocks-intraday reports; `signal-stats` / `active-signals`; `catalyst_events.jsonl` / `narrative_baskets.jsonl`.

## 14. Fix Requests / TODO

### TODO-untracked-legacy-alert
- **issue:**            Untracked legacy crypto alerts spiked to **14** (sent to Telegram, no matching proposed_signal → excluded from PF/winrate). Sharp regression vs 1 at the 11:45 slot.
- **evidence:**         `detect_untracked_legacy_alerts --since 2026-06-16` → 14 rows: ETH/JTO/XLM/WLD/ZRO/XPL/GPS/INJ B scalp+intraday longs, sent 08:37–12:58 UTC, all "NO (no proposed_signal)".
- **suggested manual fix:** Investigate the PART-1 alert→proposed_signal linkage for scalp/intraday legacy alerts; ensure every Telegram alert writes a trackable signal_id. The 1→14 jump in ~5h suggests a systematic break, not a one-off.
- **priority:**         high
- **first observed:**   2026-06-16 11:45 EEST (1); escalated 2026-06-16 16:24 EEST (14)

### TODO-catalyst-mapping
- **issue:**            Catalyst mapping weak again — 76.5% of events unmapped (null symbol).
- **evidence:**         `catalyst_events.jsonl`: 2,731 rows, mapped 642, unmapped 2,089 (76.5%). Recurring (77.0% at 11:45, 76.8% at 04:40).
- **suggested manual fix:** Improve the symbol resolver (entity→ticker mapping, alias table; handle headline-only macro/exploit items separately so they don't count as "unmapped").
- **priority:**         medium
- **first observed:**   recurring (pre-2026-06-16); re-confirmed 2026-06-16 16:24 EEST

### TODO-stock-short-bucket
- **issue:**            Stock SHORT signals remain a reproducibly losing bucket.
- **evidence:**         `signal-stats --asset-class stocks`: by direction, shorts 18W/44L, **PF 0.5, total −19R**; longs PF 1.2. Risk-on regime.
- **suggested manual fix:** Tighten/gate stock-short scoring (require stronger confirmation / suppress shorts in risk_on breadth>70%).
- **priority:**         medium
- **first observed:**   recurring; re-confirmed 2026-06-16 16:24 EEST

### TODO-stocks-rs-nan
- **issue:**            Stock sector-rotation / index RS fields render as `+nan%` (SPY 20d return, all sector RS vs SPY, several index 5d/20d).
- **evidence:**         `2026-06-16_13-08_stocks_intraday_report.md` §2: "Benchmark (SPY) 20d return: +nan%"; XLK/SMH/XLF RS "+nan%"; SPY trend "5d=+nan% 20d=+nan%". Earnings lookup also failed for 10 ETFs (SPY/QQQ/IWM/DIA/SMH/XLK/XLF/XLE/XLY/XLV).
- **suggested manual fix:** Audit the SPY/ETF history fetch feeding RS + 20d-return calcs (NaN propagates into sector-rotation ranking); separately, the ETF earnings-lookup failures are expected (ETFs have no earnings) but should be suppressed rather than logged as "failed."
- **priority:**         medium
- **first observed:**   2026-06-16 16:24 EEST

### TODO-catalyst-raw-vs-unique
- **issue:**            Raw `catalyst_events.jsonl` line count (2,731) far exceeds the report's "750 unique events" — possible duplication / dedup drift inflating the unmapped %.
- **evidence:**         Raw 2,731 lines vs report §5b "Unique events today: 750". High-importance unmapped headlines appear duplicated 2–3× (Thetanuts exploit, DeFi TVL).
- **suggested manual fix:** Audit dedup keying in the catalyst writer; confirm whether unmapped% should be computed on unique events.
- **priority:**         low
- **first observed:**   recurring; re-confirmed 2026-06-16 16:24 EEST

### TODO-symbol-resolver-stocks-as-usdt
- **issue:**            Stock legal-risk events (UNH, SMCI) still surface as `…/USDT` crypto pairs in the catalyst layer.
- **evidence:**         catalyst notable events: "SMCI/USDT [legal_risk]", "UNH/USDT [legal_risk]".
- **suggested manual fix:** Add asset-class awareness to the catalyst symbol resolver so equities are not coerced into `/USDT` pairs.
- **priority:**         low
- **first observed:**   recurring; re-confirmed 2026-06-16 16:24 EEST
