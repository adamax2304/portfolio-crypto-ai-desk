# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

_Generated 2026-06-17 ~18:39 EEST (15:39 UTC), ~2h into the US RTH session (open 16:30 EEST / 09:30 ET), ~2.5h before the FOMC decision (21:00 EEST / 14:00 ET). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods. External web research **AVAILABLE** this run (WebSearch ×2 + WebFetch-verified Banking Dive on the JPM suit)._

## 1. Executive Summary

**Wed 2026-06-17, ~18:30 EEST "US open reaction review" slot — ~2h into RTH, ~2.5h before Kevin Warsh's first FOMC decision (21:00 EEST).** The session is a **rally-pause into the Fed**: retail sales surprised hot (+0.9% May vs +0.5% exp), but **S&P 500 and Nasdaq turned negative on the day while the Russell 2000 (IWM) jumped** — a small-cap rotation / large-cap-de-risking tape ahead of a **~97%-priced hold at 3.50–3.75%** where the move is the **removed 2026 cut + Warsh's first-meeting tone** (May CPI ran hot at 4.2% YoY; BofA survey 55% expect hawkish, BofA's own take "Warsh leans dovish vs the committee"). Discipline this window: **confirmation over anticipation — no naked directional size into the 21:00 print.**

**The headline change vs the 16:27 pre-open review: the JPM A-tier long is BACK.** The fresh 18:33-EEST stocks intraday report re-prints **JPM long, A-tier, score 80.27, "actionable"** (it had dropped off at the 12:58 pre-open snapshot). Regime is still **bullish** (VIX 16.94, breadth 100%, semis/tech leading). **BUT JPM does not route to a clean actionable** for three reasons: (1) **LEGAL/HEADLINE RISK** — a verified **$328M crypto-Ponzi civil class action** (Goliath Ventures / Chase, filed ~Mar 11 2026); (2) the system's own evidence flags **RR-to-TP1 only 1.0 (< 1.5)**; (3) **FOMC in ~2.5h**. Verdict: **MANUAL REVIEW REQUIRED** — not a chase into the print. Note the legal item is a **months-old, already-digested civil suit** (JPM itself is *not* criminally charged or under DOJ/SEC probe — DOJ charged the Goliath CEO), so it is materially **milder than UNH/SMCI**, but per §I discipline it still bars a clean A-tier call.

**Cleaner long-watch than JPM: the B-tier index/sector RS-leader longs — SMH and XLK** (both B, score 68.7, "actionable", RS leaders, no legal flag, strongest sectors semis +14.4% / tech +6.6% RS). They align with the bullish regime and the stocks longs edge (signal-stats: stocks **longs PF 1.6 / +12R** vs **shorts PF 0.3 / −21R** — shorts structurally lose here). Still **require post-FOMC + clean-retest confirmation**, not a chase.

**Crypto: still chop / cautious-risk-off, no A/B.** BTC trend `transition_down`, ETH range, altcoin breadth 56.8% > EMA20, internal macro risk 91/100 (FOMC headwind; "$64K essential / bearish-reaction" warning). Best ideas remain **catalyst-backed long-watch on pullback**: **ASTER** (Token Buyback Program expansion, importance 1.9 — but vol 52x / overextended → don't chase) and **UNI** (Standard Chartered $100 PT, now ~1 day old, price reacted). **ID** stays a crowded-long no-catalyst chase-trap. **UNH (DOJ Medicare-fraud probe, −16%)** and **SMCI (export-control indictment 8-K)** remain verified legal overhangs → **AVOID**; both correctly held no_trade/rejected.

## 2. Data Used

- **Crypto scalp** `data/reports/scalp/2026-06-17_12-35_scalp_report.md` — mtime ~15:35 EEST (~3.1h) → **carry-forward** (data 12:30 UTC).
- **Crypto intraday** `data/reports/intraday/2026-06-17_12-46_intraday_report.md` — mtime ~15:46 EEST (~2.9h) → **carry-forward** (data 12:30 UTC).
- **Crypto swing** `data/reports/swing/2026-06-17_13-15_swing_report.md` — mtime ~16:15 EEST (~2.4h) → **carry-forward** (<4h).
- **Stocks intraday** `data/reports/stocks/intraday/2026-06-17_15-33_stocks_intraday_report.md` — mtime ~18:33 EEST (~0.1h) → **FRESH** (RTH session snapshot, JPM A-tier back).
- **Stocks swing** `…13-27…` (~2.2h) + **invest** `…13-33…` (~2.1h) → **fresh/carry-forward** (<4h) — used as planning context.
- **Catalysts** `data/catalysts/2026-06-17/`: `catalyst_cycle_12-47.md` (latest cycle 15:47 EEST), `catalyst_events.jsonl` (2,155 cumulative rows), `narrative_baskets.jsonl` (5). Folder present + fresh → no catalyst-scan CLI needed.
- **LLM packets** `data/processed/llm_analysis_packet.md` + `llm_stocks_packet.md` present.
- **Internal CLI:** `active-signals` crypto (**30 active, all B long**, scores 65–75) + stocks (**50 active**; now includes **JPM intraday A score 80 triggered, JPM B 76 triggered, XLF B 68 triggered, XLK B 66 triggered** post-open); `signal-stats` ×2; `detect_untracked_legacy_alerts --since 2026-06-17` → **None (clean)**.
- **DB** `db/crypto_ai_desk.sqlite` (1.46 GB, mtime 18:05): `news_items` last-36h JPM rows = 2 (+1 legal-keyword hit); t.me-source rows last 4h = 15 (WalterBloomberg macro/Iran/Warsh flow + Lookonchain noise, no actionable symbol news beyond a $TSLA robotaxi mention).
- **External:** WebSearch ×2 (JPM $328M suit; FOMC/Warsh + S&P tape); **WebFetch** verified Banking Dive on the JPM suit (filing date + civil-vs-criminal status).
- **§M ingest:** built `data/raw/enriched_review_sources/2026-06-17T1539Z.json`; ingest result in §13.

## 3. Scheduler / Data Freshness

- Latest run folder: `data/scheduled_runs/2026-06-17_default_schedule/`.
- `scheduler.log` mtime **16:34 EEST** (~2.08h) → within window.
- Latest `cycle_*_summary.md`: `cycle_01_12-30_summary.md` mtime **13:17 EEST** (~5.37h).
- **Defer rule needs BOTH log AND latest cycle > 3h. Log ~2.08h → review proceeds.**
- Stocks intraday FRESH (<0.2h, RTH snapshot). Crypto scalp/intraday/swing **carry-forward** (~2.4–3.1h; data 12:30 UTC — flagged). Stocks swing/invest <4h, planning context. No untracked-alert anomaly.

## 4. What Changed vs Previous Review

Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-17_1627.md` (pre-US-open decision review).

- **Clock advanced past the open:** US cash session is now ~2h in; FOMC moved from ~4.5h out to **~2.5h out (21:00 EEST)**. The open did **not** gap-trap violently — the tape is a **rally-pause**: S&P/Nasdaq slightly **negative on the day**, **Russell 2000 jumped** (small-cap rotation), chips recovering from Tuesday's slide; retail sales hot (+0.9%).
- **STOCKS — JPM A-tier RE-EMERGED:** the 18:33 RTH report re-prints **JPM long A 80.27 "actionable"** (was dropped at the 12:58 pre-open snapshot, was present at 11:30). **New this run: I verified a $328M crypto-Ponzi civil class action on JPM** → routes JPM to **MANUAL REVIEW REQUIRED** (legal + RR 1.0 + FOMC), not the clean A-tier the score implies. **SMH/XLK B-tier longs are new actionable RS-leader candidates** this cycle.
- **Crypto largely unchanged:** still chop / cautious-risk-off, BTC `transition_down`, breadth 56.8%, no A/B. ASTER (buyback) + UNI (StanChart) remain the catalyst-backed long-watches; ID remains the crowded no-catalyst chase-trap. (Carry-forward: data is the same 12:30-UTC crypto cycle as the 16:27 review — no fresher crypto pull yet.)
- **Unchanged integrity:** **UNH DOJ probe → still AVOID**; **SMCI indictment → still rejected**; untracked-legacy-alert detector **clean (0)**.
- **Confirmed:** stocks-longs-over-shorts in a bullish regime (signal-stats longs PF 1.6 vs shorts PF 0.3) — re-confirmed; the system correctly rejects all the short candidates (NFLX/TSLA/LLY/AMZN) as `short_in_bullish_regime`.
- **Carried TODO from 16:27:** the ASTER catalyst-mapping loss + the ~79.6%-unmapped catalyst figure persist this run (see §5, §14).

## 5. Catalyst Coverage

- **Cumulative today:** `catalyst_events.jsonl` = **2,155 rows**; **mapped (symbol-tagged) = 439 (20.4%); unmapped = 1,716 (79.6%)**.
- **Narrative baskets: 5** — `delisting_thin_liquidity` (avoid_low_liquidity), `perps_dex_narrative` (HYPE; wait_pullback), `rwa_narrative` (ONDO/XLM; related_beta_rotation), `ai_narrative` (NEAR/RENDER/TAO/FET; related_beta_rotation), `momentum_breakout` (UNI/ID; wait_pullback, fresh <1h).
- ⚠️ **Catalyst mapping weak this run — use the catalyst layer as context, not final decision.** Unmapped 79.6% > 50% (recurring; §14 TODO).
- **Top-3 unmapped headlines:** (1) *"White House's Anthropic move reignites AI debate in Congress"*; (2) *"US State Department steps in to help Vozinha's mother attend World Cup…"*; (3) *"Circle showcases AI agent's wallet capabilities with USDC transactions."*
- **Verified mapped legal flags (top importance):** **SMCI** (export-control indictment 8-K, SEC EDGAR), **UNH** (DOJ Medicare-fraud probe, −16%, QuiverQuant). Both correctly route to avoid/rejected. **JPM** $328M crypto-Ponzi suit surfaced via `news_items` (not the basket layer) — see §7 Candidate 1.

## 6. Market Landscape

US stocks screen **bullish on the 20d trend** (4/4 indices up, SPY +2.19% 20d, QQQ +4.41%, IWM +7.95%, DIA +5.93%; VIX 16.94; breadth 100%; semis +16.6% / tech +8.8% leading, energy −10.1% lagging). But **today's intraday tape is a cautious rally-pause into the Fed** — S&P/Nasdaq slightly negative on the day, small-caps (Russell) leading, large-caps de-risking. Crypto is a separate, softer book: chop / cautious-risk-off, BTC `transition_down`, breadth 56.8%, internal macro 91/100. The edge this window is **confirmation, not anticipation** — the 21:00 FOMC + Warsh debut is the binary that resolves the session.

### Market Mood / Risk Routing      (REQUIRED)
- **Crypto mood:**           **chop / cautious-risk-off** (BTC transition_down, breadth 56.8%, macro 91/100) — pre-FOMC coil, no A/B
- **Stocks mood:**           **bullish regime, cautious into FOMC** (20d uptrend + breadth 100%, but S&P/Nasdaq red on the day, small-cap rotation, event risk in ~2.5h)
- **Dominant narrative:**    **rally-pause / de-risking into Warsh's first FOMC** — hot retail sales + hot May CPI (4.2%) → expected removal of the 2026 cut (hawkish hold); small-caps (IWM) rotating up; US-Iran de-escalation a risk-on offset
- **Preferred side now:**    **longs (RS-leader / catalyst-backed) but wait-for-confirmation** — require post-FOMC + clean-retest; **avoid shorts** (structurally lose in bullish regime, PF 0.3); **no naked size into the 21:00 print**
- **Best long candidate:**   **SMH/XLK (B, RS-leader index/sector longs)** — trigger: hold the entry zone (SMH 630.6–634.2 / XLK 187.7–188.4) with RTH volume, ideally **post-FOMC**; cleaner than JPM (no legal flag)
- **Best short candidate:**  **none clean** — stocks shorts route to `short_in_bullish_regime` (avoid); crypto **short-watch ZRO/USDT** only on a confirmed failed retest (already −14.5%, squeeze-prone if BTC bounces post-Fed)
- **Best catalyst-backed candidate:** **ASTER/USDT** (buyback-program expansion, importance 1.9) on a pullback that holds — do NOT chase at 52x-vol extension; **UNI/USDT** (StanChart $100 PT, day-old) as secondary
- **What to avoid:**         **JPM clean A-tier entry** (legal overhang + RR 1.0 + FOMC → manual review); **UNH** (DOJ probe) / **SMCI** (indictment); **ID** (crowded no-catalyst chase); chasing ASTER at extension; **naked size into 21:00**
- **What would change the view:** **FOMC 21:00 + Warsh presser 21:30** (hawkish dots/tone → risk-off; dovish → relief); first clean RTH retest post-decision; crypto: BTC reclaim >$65.5K (bullish) vs lose $64K (bearish)

## 7. Candidate Deep Dives

### Candidate 1 — JPM (stocks intraday, A-tier 80.27) — MANUAL REVIEW REQUIRED
- **Source:** stocks intraday A long, score **80.27**, confidence high, "actionable"; thesis "uptrend | RS=leader | regime=bullish"; RS vs SPY 20d **+11.66%**, RS vs sector +6.70%; earnings safe; entry zone **335.435–336.645**, invalidation close < 333.015, TP1 340.275 / TP2 342.695 / TP3 346.325.
- **Internal-first catalyst check (`news_items`):** last 36h = *"Why JPMorgan Chase Topped the Market on Tuesday"* (Motley Fool, 06-16, **positive**) + *"JPMorgan bankers say Big Pharma M&A still outpaces biotech IPOs"* (Seeking Alpha, 06-16). Legal-keyword hit: *"JPM Sued Over $328M Crypto Scam: Compliance Failures Under Spotlight"* (Yahoo, 06-16). `news_catalyst` score in the signal = **0.00** (no positive catalyst credited).
- **LEGAL/HEADLINE RISK (§I — verified):** **$328M crypto-Ponzi civil class action**, Goliath Ventures / Chase, filed **~Mar 11 2026** in federal court (CA); >2,000 investors; alleges JPM ignored AML "red flags" while banking the scheme (~$253M processed). **Crucially: JPM itself is NOT criminally charged or under DOJ/SEC investigation** — the DOJ charged Goliath's CEO (money laundering/wire fraud), not JPM. This is a **months-old, already-digested civil liability** overhang, materially **milder than UNH (active DOJ probe) or SMCI (indictment)** — the stock outperformed Tuesday. Verified via WebSearch + WebFetch (Banking Dive, CoinDesk 2026-03-12). Cited §13.
- **Price-reaction / chase / mood (§J):** **RR-to-TP1 is only 1.0** (the report's own evidence flags "RR to TP1 below 1.5") — a structurally thin reward for a fresh entry. The A-tier playbook's own **known failure mode is "A-tier overpromotion on losing names."** Large-caps are **red on the day** into a hawkish-skewed FOMC ~2.5h out. Entering now ≈ chasing a thin-RR A-tier large-cap long into the print.
- **Actionable now?** **No — MANUAL REVIEW REQUIRED.** Not a hard AVOID (legal item is old/civil/digested, regime + RS support the long), but per §I a clean A-tier call is barred while the suit is live, and RR 1.0 + FOMC argue for patience. **If taken at all: wait for a clean retest of 335.4–336.6 with RTH volume, ideally post-FOMC; respect the 333.0 invalidation; keep size small.**

### Candidate 2 — SMH / XLK (stocks intraday, B-tier 68.71) — LONG-WATCH, POST-FOMC CONFIRMATION
- **Source:** both **B, score 68.71, "actionable"**, RS-leader longs in a bullish regime. **SMH** RS vs SPY 20d **+14.40%** (strongest sector, semis), entry 630.563–634.215, invalidation < 623.259, TP1 645.171. **XLK** RS +6.60% (tech), entry 187.744–188.440, invalidation < 186.351, TP1 190.529. Both ETFs → **no earnings/legal risk** (clean).
- **Internal-first catalyst:** none symbol-specific (ETF momentum); narrative tailwind = semis/tech sector leadership; chips recovering from Tuesday's slide (external tape).
- **Price-reaction / chase / mood (§J):** RR-to-TP1 ~1.0 (thin, same structural caveat as JPM), volume_relative_volume scored 0.00 (no volume confirmation yet). Aligns with the **stocks-longs edge (PF 1.6 / +12R)** and bullish regime, but it's into a red-on-the-day large-cap tape pre-FOMC.
- **Actionable now?** **No — long-watch.** Cleanest long ideas this window (no legal flag, RS leaders). **Trigger: hold the entry zone with RTH volume, ideally post-FOMC confirmation. Invalidation: SMH < 623.3 / XLK < 186.4.** Do not chase ahead of the print.

### Candidate 3 — ASTER/USDT (crypto, loudest mover) — CATALYST-BACKED LONG-WATCH ON PULLBACK
- **Source:** intraday strongest score **100**, 24h +10.61%, RS vs BTC +12.97%, **volume 52.24x** (tags: relative_strength, volume_expansion, breakout, **overextended**); price up + OI up (fresh positioning); member of `momentum_breakout` + perps-DEX related baskets.
- **Internal-first catalyst (`news_items`):** **VERIFIED — Token Buyback Program expansion** (*"Aster Expands its Token Buyback Program, Price Jumps 10%"*, BeInCrypto, 2026-06-17, detected_symbols=ASTER, importance 1.9 — day's highest). The catalyst layer left this **unmapped** (the `momentum_breakout` basket mislabels ASTER "no confirmed news catalyst") — §14 TODO carried from 16:27.
- **Price-reaction / chase / mood (§J):** **price already reacted (+10% on the headline, 52x vol = late-stage parabolic)** — the easy move is in. Catalyst real, but entering at 52x-vol extension is a chase into a cooling, cautious-risk-off crypto tape + pre-FOMC.
- **Actionable now?** **No — catalyst-backed long-WATCH on a pullback that holds with volume after the blow-off bases out**, NOT a chase at extension. Invalidation: loss of the buyback-breakout base / BTC breaking $64K.

### Candidate 4 — UNI/USDT (crypto, verified catalyst) — LONG-WATCH ON PULLBACK
- **Source:** intraday watchlist score 64.2 (24h +6.9%, RS +9.25%, vol 1.18x), price up + OI up; `momentum_breakout` basket primary.
- **Internal-first catalyst:** **VERIFIED** — Standard Chartered initiated UNI with a **$100 PT**, drove +22.5% yesterday (CoinDesk 06-17). Catalyst now **~1 day old; price has reacted**.
- **Price-reaction / chase / mood (§J):** consolidating +6.9% 24h after the +22.5% leg; OI+price up is constructive but entering now ≈ chasing a day-old catalyst into a cooling tape + pre-FOMC. Score below active threshold → watchlist.
- **Actionable now?** **No — catalyst-backed long-watch: trigger = a pullback that holds with volume (don't chase the day-old candle); invalidation = loss of the breakout base / BTC < $64K.**

### Candidate 5 — UNH & SMCI (stocks, legal/integrity confirm) — AVOID
- **Source:** UNH active C `wait`; catalyst layer flags **[legal_risk] UnitedHealth Faces DOJ Probe, Shares Dive 16% on Fraud Investigation** (QuiverQuant). SMCI **[legal_risk] export-control indictment 8-K** (SEC EDGAR). Both surfaced as notable mapped events.
- **LEGAL/HEADLINE (§I — verified):** UNH = **active DOJ Medicare-fraud probe, −16%**; SMCI = **export-control indictment**. Both are live, government-action overhangs (more severe than the JPM civil suit). Stocks intraday correctly holds UNH `no_trade` (34.34) and SMCI `rejected` short (32.12).
- **Actionable now?** **No — AVOID.** Correct system behavior; surfaced to confirm neither routes to a clean trade while the actions are live. No integrity anomaly.

## 8. Best Candidates Ranked

No clean actionable A/B this window (JPM A-tier blocked by legal+RR+FOMC; B-tier longs await confirmation; crypto chop, no A/B; FOMC ~2.5h out). Per routing, best watch candidates + exact triggers:

1. **Long-watch (cleanest) — SMH (B, semis RS leader):** trigger = **hold 630.6–634.2 with RTH volume, ideally post-FOMC**; invalidation = close < 623.3. No legal/earnings flag; strongest sector (+14.4% RS).
2. **Long-watch — XLK (B, tech RS leader):** trigger = hold 187.7–188.4 with volume post-FOMC; invalidation = close < 186.4.
3. **Manual-review long — JPM (A, but legal+RR):** if reviewed and taken, **wait for a clean 335.4–336.6 retest post-FOMC**, respect 333.0 invalidation, small size; not a chase into the print.
4. **Catalyst-backed long-watch — ASTER/USDT (buyback):** trigger = pullback that holds after the 52x-vol blow-off bases out; do not chase at extension; invalidation = loss of buyback base / BTC < $64K.
5. **Short-watch — ZRO/USDT (crypto, weakest):** trigger = **confirmed failed retest** of resistance; abort if BTC reclaims $65.5K (squeeze). Lower conviction — already overextended-down. (Stocks shorts: none — `short_in_bullish_regime`.)
- **Catalyst-watch secondary:** UNI/USDT on a pullback (day-old StanChart catalyst).

## 9. Avoid / No Trade  (this decision window only — scanner always continues)

- **JPM clean A-tier entry** — $328M crypto-Ponzi civil suit + RR-to-TP1 1.0 + FOMC in ~2.5h → manual review, not a clean chase.
- **UNH** (active DOJ fraud probe, −16%) and **SMCI** (export-control indictment) — verified live legal overhangs.
- **Stock shorts** (NFLX/TSLA/LLY/AMZN/XOM/etc.) — `short_in_bullish_regime`; signal-stats stocks shorts PF 0.3 / −21R. System correctly rejects them.
- **ID/USDT** and other no-catalyst crypto chases — crowded longs / mean-revert in chop.
- **Chasing ASTER at 52x-vol extension** — catalyst real but the easy move is in; pullback-only.
- **Naked directional size into the 21:00 EEST FOMC / 21:30 Warsh presser** — ~97% priced hold; the binary is the dot-plot (likely 2026 cut removed) + Warsh's first-meeting tone (BofA 55% expect hawkish).
- _This is a current-window routing, not a system stop. Scanning, candidate generation, tracking, and outcome recording continue in all moods._

## 10. Main Risks

- **FOMC tonight (21:00 EEST) + Warsh's first presser (21:30):** hawkish hold expected (hot CPI 4.2%, removed 2026 cut); tone is the swing factor (55% hawkish per BofA vs BofA's "leans dovish vs committee"). Single largest risk; resolves in the 21:30 slot.
- **Large-cap de-risking intraday:** S&P/Nasdaq red on the day despite hot retail sales — the bullish 20d regime and today's tape disagree; don't over-trust the screen-tier scores into the event.
- **Thin RR on the stock longs:** JPM/SMH/XLK all show RR-to-TP1 ≈ 1.0 — structurally low reward; an A/B score does not equal a clean entry.
- **Crypto data carry-forward (~3h, 12:30-UTC cycle):** no fresher crypto pull this run; BTC/ETH levels and breadth may have drifted — re-confirm on the next cycle.
- **No-catalyst / crowded crypto reversion:** ASTER 52x-vol + ID crowded longs mean-revert; crypto A/B headline winrate 14.4% / PF 0.88.
- **Catalyst mapping weak (79.6% unmapped):** symbol-level catalyst layer is context-only this run; high-importance symbol-tagged rows (ASTER buyback) still not propagating to baskets (§14).

## 11. Action Plan — next 4 hours

1. **Do not initiate naked directional risk into the 21:00 FOMC / 21:30 Warsh presser.** Confirmation over anticipation.
2. **Stocks:** treat **SMH/XLK B-tier longs** as the cleanest watches — alert for a hold of their entry zones with RTH volume **post-FOMC**. **JPM A-tier = manual review** (legal + RR 1.0): only consider a clean 335.4–336.6 retest post-decision, small size, respect 333.0. Keep **UNH/SMCI on avoid**; avoid all stock shorts (bullish regime).
3. **Crypto:** set alerts for **ASTER pullback-that-holds** and **UNI pullback-that-holds** (both catalyst-backed long-watch); **ZRO failed retest** (short-watch). Watch **BTC $65.5K reclaim (bullish) / $64K loss (bearish)** as the regime trigger; keep size small into 21:00.
4. **Avoid the chase:** ASTER (52x vol) and ID (crowded) — pullback-only, no entries at extension.
5. **Re-check at the 21:30 EEST late-session / FOMC-reaction slot** for the decision outcome, Warsh tone, which longs confirmed/failed post-print, and any fresh legal/earnings headlines.

## 12. Final Verdict per Mode

- **Crypto scalp:** No clean trade (carry-forward data). Leaders extended/crowded; catalyst-backed names (ASTER/UNI) are watch-on-pullback only.
- **Crypto intraday:** No clean A/B. Wait-for-trigger; catalyst-backed ASTER/UNI long-watch on pullback or ZRO failed-retest short only on confirmation.
- **Crypto swing:** Carry-forward (<4h); chop + pre-FOMC → no fresh size; reassess post-decision.
- **Stocks intraday:** **JPM A-tier back but MANUAL REVIEW REQUIRED** (legal + RR 1.0 + FOMC). **SMH/XLK B-tier longs = cleanest long-watch, post-FOMC confirmation.** Bullish regime, longs-only; avoid shorts.
- **Stocks swing / invest:** Fresh-ish (<4h) but pre-open-built; planning context, longs-biased; re-confirm post-FOMC. No fresh size into the print.
- **Overall:** **Risk-routed wait-for-confirmation into the Fed.** Best clean long-watch SMH/XLK (post-FOMC), best short-watch ZRO (failed retest), best catalyst-backed ASTER (pullback); JPM A-tier = manual review; avoid UNH/SMCI + stock shorts + FOMC-front-running. Scanner continues in all moods.

## 13. Sources

- [Banking Dive — JPMorgan sued over $328M crypto 'Ponzi' scheme (WebFetch-verified)](https://www.bankingdive.com/news/jpmorgan-sued-over-328m-crypto-ponzi-scheme/814903/) — primary_source — civil class action filed **~Mar 11 2026** by private investors; **JPM itself not criminally charged / not under DOJ-SEC probe** (DOJ charged the Goliath CEO). **confirms** JPM legal item is a months-old, digested civil overhang (milder than UNH/SMCI). **weakens** a clean A-tier call.
- [CoinDesk — Alleged Ponzi-scheme victims sue JPMorgan for banking supposed $328M scam (2026-03-12)](https://www.coindesk.com/business/2026/03/12/alleged-ponzi-scheme-victims-sue-jpmorgan-for-banking-supposed-usd328-million-scam) — primary_source — original filing date corroboration. **confirms** suit age (~3 months).
- [Yahoo Finance — JPM Sued Over $328M Crypto Scam: Compliance Failures Under Spotlight (06-16)](https://finance.yahoo.com/news/jpm-sued-over-328m-crypto-151200917.html) — single_source — the internal `news_items` row that surfaced the JPM legal flag. **confirms** the flag is real & re-circulating.
- [Intellectia — Fed Interest Rate Decision June 2026: Warsh's First FOMC Meeting Guide](https://intellectia.ai/blog/fed-interest-rate-decision-june-2026) — single_source — **97% priced hold at 3.50–3.75%**; statement 2:00 PM ET, Warsh presser 2:30 PM ET; May CPI 4.2% YoY; expected removal of the single 2026 cut. **confirms** FOMC timing + hawkish-hold setup.
- [TheStreet — Stock Market Today June 17 2026: S&P 500, Nasdaq turn negative ahead of Fed; Russell 2000 jumps](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-17-2026) — single_source — intraday tape: large-caps red on the day, small-caps up, chips recovering, retail sales +0.9%; BofA 55% expect hawkish Warsh (BofA take: leans dovish vs committee). **confirms** rally-pause / de-risking-into-Fed read.
- Internal: stocks intraday report `2026-06-17_15-33` (JPM A back), crypto scalp/intraday/swing reports, `catalyst_events.jsonl` (2,155 rows / 5 baskets), `news_items` (JPM + ASTER + UNH/SMCI flags), `active-signals`/`signal-stats` CLI, `detect_untracked_legacy_alerts` (clean).

## 14. Fix Requests / TODO

### TODO-aster-buyback-catalyst-dropped  [HIGH — recurring; concrete proof of catalyst-mapping loss]
- **issue:**            A high-importance, symbol-tagged catalyst in `news_items` is NOT propagated to `catalyst_events.jsonl` / narrative baskets, so ASTER is mislabeled "no confirmed news catalyst" in the `momentum_breakout` basket. The buyback-program expansion is the actual driver of ASTER's 52x volume + +10.6% move.
- **evidence:**         `db/crypto_ai_desk.sqlite` `news_items`: *"Aster Expands its Token Buyback Program, Price Jumps 10%"*, BeInCrypto, 2026-06-17, `detected_symbols_json=["ASTER"]`, importance 1.9 — NOT present as a mapped ASTER event in `data/catalysts/2026-06-17/catalyst_events.jsonl`; basket still lists ASTER under "no confirmed news catalyst."
- **suggested manual fix:** trace the catalyst-builder step reading `news_items` → emitting `catalyst_events`: why does a row with `detected_symbols_json=["ASTER"]` + importance 1.9 not surface as a mapped catalyst (time-window? symbol-normalization ASTER vs ASTER/USDT? dedup? per-cycle cap?). The `momentum_breakout` basket should cross-check `news_items` before declaring "no confirmed news catalyst." Root of the recurring ~79.6%-unmapped figure.
- **priority:**         high
- **first observed:**   2026-06-17 16:27 EEST (recurring; still present 18:30)

### TODO-catalyst-mapping-weak
- **issue:**            catalyst symbol-mapping ~20.4% mapped / ~79.6% unmapped (recurring across runs).
- **evidence:**         `data/catalysts/2026-06-17/catalyst_events.jsonl` — 439 symbol-tagged of 2,155 cumulative rows.
- **suggested manual fix:** improve the symbol/entity resolver in the catalyst layer (headlines like "White House's Anthropic move…", "Circle/USDC…", World-Cup fan-token noise).
- **priority:**         medium
- **first observed:**   2026-06-17 11:42 EEST (recurring)

### TODO-stock-longs-thin-rr  [medium — new observation]
- **issue:**            Every stock A/B candidate this run (JPM A, SMH B, XLK B) prints **RR-to-TP1 ≈ 1.0** and `risk_reward: 0.00` in the score breakdown, yet still scores A/B. A thin-RR setup can clear the A/B bar on regime+RS alone — risk of "overpromoted" actionables with poor reward geometry (the playbook's own stated failure mode).
- **evidence:**         `data/reports/stocks/intraday/2026-06-17_15-33_stocks_intraday_report.md` — JPM/SMH/XLK all list "RR to TP1 below 1.5 (1.0)" and `risk_reward: 0.00`.
- **suggested manual fix:** consider a manual review of whether `risk_reward: 0.00` items should be capped below A-tier, or whether TP1 placement / ATR multiple needs tightening so A/B actionables carry ≥1.5 RR. (No auto-modify here.)
- **priority:**         medium
- **first observed:**   2026-06-17 18:30 EEST

### TODO-crypto-ab-winrate
- **issue:**            crypto A/B headline winrate 14.4% / PF 0.88 / totalR −9 (reliable, n=254). Exchange-confirmed subset PF 1.2 (+7R) vs unconfirmed PF 0.6 (−17R).
- **evidence:**         `signal-stats --asset-class crypto` headline + by-exchange_confirmation split.
- **suggested manual fix:** manual entry-quality review of the no-catalyst momentum bucket; the by-exchange_confirmation split suggests weighting/requiring exchange confirmation more heavily (no auto-modify here).
- **priority:**         low
- **first observed:**   2026-06-17 11:42 EEST (recurring)

### TODO-stocks-shorts-pf
- **issue:**            stocks shorts PF 0.3 / −21R (stronger, n=90) — shorts structurally lose in the current bullish regime; longs PF 1.6 / +12R.
- **evidence:**         `signal-stats --asset-class stocks` by-direction split.
- **suggested manual fix:** confirm the short gate (`short_in_bullish_regime` rejection) stays strict; consider whether any short tier should be tradeable at all while the regime is bullish (no auto-modify here).
- **priority:**         low
- **first observed:**   2026-06-17 18:30 EEST
