# Opus Enriched Review — post-close final daily review — Auto Cycle 23:30 EEST

- **Generated:** 2026-06-04 23:30 EEST (auto-enriched-review, scheduled task `opus-enriched-review-postclose`, post-close slot 23:15).
- **Slot:** **Post-close final daily review** — after the US cash close (23:00 EEST / 16:00 ET). Focus: the daily wrap (how the US session closed, what worked/failed today), end-of-day risk & exposure, and the overnight-into-Asia setup for crypto (the live 24/7 class).
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-04_2139.md` (≈1.9 h ago — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified the US close (Dow record +1.73%, S&P +0.41%, Nasdaq −0.09%, Health Care +3.14% led, AVGO −15% sell-the-news, AMD +4.02% close $542.52, NVDA −3.62% close $214.75), and BTC ~$63.6K / sub-$62K intraday / record 20-day spot-ETF exodus (CNBC, TheStreet, Yahoo Finance, Motley Fool, BNN Bloomberg, BlockchainReporter, FXLeaders, OpenPR). One WebFetch (FXLeaders) opened cleanly; one (BlockchainReporter) returned HTTP 403 — fell back to corroborating sources.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure data is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **Daily wrap: a textbook AI-semi sell-the-news reset that the broad tape shrugged off via rotation, not contagion.** Broadcom reported a **beat-and-raise** (Q3 guide $29.4B vs $28.5B est) but **closed −15%** on a soft Q2 revenue print ($22.19B vs $22.27B) — a classic sell-the-news. Money rotated **out of chips and into Dow/value/defensives**: **Dow +1.73% to a record 51,561.93**, **S&P +0.41% (7,584.31)**, while the **Nasdaq was the only major to close red (−0.09%, 26,830.96)**. Eight of eleven S&P sectors advanced; **Health Care led (+3.14%)**, Financials +2.67%, Real Estate +1.87%. This is a **valuation reset in the most-stretched AI-semi names, not an AI-thesis break** — and it confirms the rotation thesis from the last two reviews.
- **The 21:39 "do not chase AMD / favor the defensive rotation" calls were vindicated by the close.** **AMD ran to its target and closed $542.52 (+4.02%) — essentially AT TP1 (542.46) and ~$18 above the top of its entry zone (519–525).** Anyone who chased the ~$542 print at 21:39 bought the high of the recovery into the first target; the disciplined "wait for a pullback" stance was correct (no pullback into the zone materialized before the close). **UNH and the healthcare/value bid were the day's winner** — Health Care led the entire market, exactly the rotation the desk flagged.
- **NVDA's "watch for a reclaim of 219.13" trigger never fired — and it closed red (−3.62%, $214.75), below the entry zone.** Standing aside was correct; the long was never actionable. It held up *better* than AVGO/AMD-at-open intraday but still finished lower with the chip group.
- **SMCI de-escalated at the close and remains an AVOID.** The freshest stocks snapshot (22:58 EEST / 19:58 UTC) drops **SMCI to `no_trade` / rejected (51.01)** from the B-tier 79.71 seen earlier — but the verdict is unchanged: the **active SDNY export-control indictment + compliance overhang** (§7.5) makes it AVOID regardless of score.
- **Crypto is the dominant overnight-into-Asia risk and the only live class now.** Regime **bearish trend / risk-off**; **BTC ~$63.6K, dipped sub-$62K intraday, −13% on the week**, on the **20th consecutive day of spot-ETF net outflows — a record streak (~$2.97–3.45B cumulative)** — with **SOL at a 2.5-yr low** and ~$1.5B liquidated this week. The lone active crypto idea, **B-tier SHORT NEAR/USDT (66/70)**, is **catalyst-aligned but late** (NEAR already flushed −13/−18% on the Arthur Hayes dump); the desk itself says *"no late short after a vertical flush."* **Net overnight: no clean crypto actionable; respect BTC downside — a loss of ~$61–62K risks a liquidation cascade into the Asia session.**
- **Net daily verdict:** Stocks closed risk-on-via-rotation (Dow record, healthcare/financials lead) — **the day's working trades were the defensive/value bid, not the chip names.** For tomorrow: **AMD A-tier but extended (wait for a pullback), UNH the cleanest catalyst+rotation name (don't chase the +5.7% gap), NVDA watch for a 219 reclaim, SMCI avoid.** Overnight crypto = **no-trade / watchlist**, downside-skewed.

---

## 2. Data Used

**Internal — fresh (<3 h):**
- `data/reports/scalp/2026-06-04_17-35_scalp_report.md` (gen 20:35 EEST; ~2.9 h). Regime **bearish trend (risk-off)**; no A-tier; best idea SHORT NEAR (entry 2.457–2.499).
- `data/reports/intraday/2026-06-04_18-00_intraday_report.md` (gen 21:00 EEST; data freshness 17:45 UTC; ~2.5 h). Regime bearish; breadth 20.8% > EMA20; BTC ATR pct 100. B-tier SHORT NEAR 66.0; all else watchlist.
- `data/reports/stocks/intraday/2026-06-04_19-58_stocks_intraday_report.md` (data freshness 19:58 UTC = 22:58 EEST; **~0.5 h — the at-/post-close snapshot**). Regime bullish, VIX 15.33, breadth 100%. **AMD A 84.71**, UNH B 75.9, NVDA B 74.79, LLY/SMH/AAPL B; **SMCI `no_trade` rejected 51.01**.

**Internal — carry-forward (4–12 h, flagged §3):**
- `data/reports/swing/2026-06-04_14-44_swing_report.md` (crypto; ~8.8 h) — carry-forward.
- `data/reports/stocks/swing/2026-06-04_14-55_stocks_swing_report.md` (~8.6 h) — carry-forward.
- `data/reports/stocks/invest/2026-06-04_15-01_stocks_invest_report.md` (~8.5 h) — carry-forward.

**Catalyst / narrative / packets:**
- `data/catalysts/2026-06-04/` — `catalyst_events.jsonl` (2344 rows), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_18-00.md` (latest, mtime 21:00).
- LLM packets: `data/processed/llm_analysis_packet.md` (gen 21:00), `llm_stocks_packet.md` (gen 21:17).

**CLI / DB:** `active-signals` (crypto **10** / stocks **50**), `signal-stats` (crypto + stocks, week), `detect_untracked_legacy_alerts --since 2026-06-04` → **1 untracked (EPIC/USDT)**.

**External (this run — cited §13):** CNBC + TheStreet (Dow +874.86 record, rotation out of chips into banks/retail/defensives); Yahoo Finance (AVGO −13/−15%, AMD $542.52 +4.02%, NVDA $214.75 −3.62%); Motley Fool + BNN Bloomberg (AVGO sell-the-news despite beat-and-raise); BlockchainReporter + FXLeaders + OpenPR (BTC ~$63.6K, sub-$62K intraday, −13% week, record 20-day / ~$2.97–3.45B ETF exodus, ~$1.5B liquidated).

**Unavailable / blind:** live tick-by-tick prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps, order-book depth/CVD, live ETF-flow feed, on-chain whale flows, token-unlock calendar (manual/unconnected); live social beyond RSS-bridged `t.me/*`. UNH exact close not isolated (sector +3.14% lead corroborates direction).

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-04_default_schedule/`.
- `scheduler.log` mtime **23:18 EEST → ~0.1 h** (fresh). Latest cycle summary `cycle_02_20-02_summary.md` mtime **21:18 EEST → ~2.1 h** (fresh, under 3 h).
- **NO DEFER** — both freshness checks under the 3 h rule. Review proceeds normally.
- **Fresh (<4 h):** stocks intraday (~0.5 h, the close snapshot), crypto scalp (~2.9 h), crypto intraday (~2.5 h).
- **Carry-forward (4–12 h, used + flagged):** crypto swing (~8.8 h), stocks swing (~8.6 h), stocks invest (~8.5 h). None > 14 h → no stale exclusions, but swing/invest verdicts (§12) carry the carry-forward caveat. The crypto scalp/intraday reports are themselves now ~2.5–2.9 h old (last cycle was 20:02); the next default cycle should refresh them — flagged, not stale.

---

## 4. What Changed vs Previous Review (21:39 → 23:30)

- **The US session closed — and resolved the open calls from 21:39.** AMD's "wait, do not chase at ~$542" → **AMD closed $542.52 at TP1**: it ran the rest of the way to target, never offered the 519–525 pullback, so the disciplined stance avoided buying the high. NVDA's "watch for a reclaim of 219.13" → **never triggered; NVDA closed $214.75 (−3.62%), below the zone.** UNH's "cautious long, healthcare/defensive rotation" → **Health Care led the market (+3.14%)** — the rotation thesis was the day's winning read.
- **Index outcome confirmed the rotation, not contagion:** Dow **+1.73% to a record (51,561.93)**, S&P +0.41%, **Nasdaq the only red major (−0.09%)**. 8/11 sectors green. The AI-semi flush stayed contained to chips.
- **AVGO fully resolved:** closed **−15%** on a beat-and-raise — confirmed sell-the-news, now pure context.
- **SMCI de-escalated in the model:** dropped from B-tier 79.71 (21:33 snapshot) to **`no_trade` rejected 51.01** at the close — but the AVOID verdict is unchanged (legal/export-control overhang is the gate, not the score).
- **Crypto kept bleeding, did not stabilize:** BTC essentially flat-to-lower vs the 21:39 ~$63.8K read (**~$63.6K, sub-$62K intraday**) on the **record 20-day ETF exodus** extending; NEAR short still **late** post-flush.
- **Persisting integrity / quality flags (all re-confirmed, unchanged):** A-tier stocks loser bucket (**PF 0.20, WR 6.2%, −8R**, n=27); catalyst mapping weak (**74.6% unmapped**, identical to 21:39); **1 untracked EPIC/USDT alert** still present; crypto short bucket bleed (**short PF 0.00 / −7R**).
- **Invalidated:** nothing structurally — every 21:39 thesis (rotation winner = defensives/value, AMD chase, NVDA needs a trigger, SMCI avoid, crypto downside) played out at the close as called.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative JSONL): **2344**; mapped (non-null `symbol`): **595** (25.4%); unmapped: **1749** → **74.6% unmapped** (unchanged from 21:39).
- `narrative_baskets`: **3** — `perps_dex_narrative` (playbook `wait_pullback`, primary HYPE/USDT; sample: Arthur Hayes dumps HYPE/NEAR), `ai_narrative` (`related_beta_rotation`, primary NEAR/RENDER/TAO/FET, fresh <6h), `momentum_breakout` (`wait_pullback`, primary HOME/USDT +24.3%). All `single_source`.
- **⚠️ catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped > 50%).
- Top 3 unmapped headlines (symbol unresolved despite explicit tickers): (1) "Tilly's (**TLYS**) Q1 2026 Earnings Call Transcript"; (2) "Petco (**WOOF**) Q1 2026 Earnings Call Transcript"; (3) "ChargePoint (**CHPT**) Q1 2027 Earnings Transcript". Same resolver failure mode as prior runs (tickered names dropped into unmapped) → TODO-catalyst-mapping-weak (§14).

---

## 6. Market Landscape

**Stocks (closed — daily wrap):** Regime **bullish** into the close (VIX 15.33, breadth 100% > EMA20). The day was a **rotation story**: an AVGO-led AI-semi sell-the-news flush (**AVGO −15%** despite a beat-and-raise; Micron/Intel/AMD-at-open dragged) was **fully absorbed by a rotation into Dow/value/defensives** — **Dow +1.73% to a record (51,561.93)**, S&P +0.41%, **Nasdaq −0.09% (the lone red major)**. **Health Care led (+3.14%)**, Financials +2.67%, Real Estate +1.87%; 8/11 sectors green. **AMD recovered to close +4.02% ($542.52) — at its TP1**; **NVDA closed −3.62% ($214.75)**, below its long trigger. Read-through: the AI trade is being **de-risked at the most-stretched names, not abandoned** — semis are still the strongest 20-day sector. End-of-day posture into tomorrow: **favor the rotation winners (healthcare/value/financials); the chip names need to prove stabilization (NVDA reclaim of 219, AMD a pullback to 519–525) before they're clean longs again.**

**Crypto (24/7, risk-off — the live overnight-into-Asia class):** Regime **bearish trend**; BTC/ETH downtrend; breadth ~20.8% > EMA20; BTC ATR pct 100 (elevated). **BTC ~$63.6K (dipped sub-$62K intraday), −13% on the week**, on the **20th straight day of spot-ETF net outflows — a record streak (~$2.97–3.45B cumulative)** and ~$1.5B liquidated this week; **SOL at a 2.5-yr low**. AI is the only "rising" narrative basket yet **every AI alt is red** (NEAR −13.5/−18%, FET −14%, ICP −8%) — *bleeding, not leading.* Low-volume counter-tape green outliers (WLD +13%, EPIC +37%, ALLO, HOME +24%) are watchlist-only momentum pops in a bearish tape. **Overnight risk is skewed down: a break of ~$61–62K risks a liquidation cascade into Asia.**

---

## 7. Candidate Deep Dives (≤5)

### 7.1 NEAR/USDT — B-tier SHORT 66.0 (intraday) / 70 (swing) → **NO-TRADE / WATCHLIST overnight (late after the flush)**
- **Tier/role:** the **only active crypto B-tier idea** (the live overnight class); medium conf; bearish-regime-aligned breakdown/retest short.
- **Catalyst (verified):** **Arthur Hayes dumped his entire HYPE + NEAR stack** (NEAR −13/−18% to ~$2.33; he warns of a market top by September). Internal: `ai_narrative` basket `related_beta_rotation`; 3 catalyst items. (BeInCrypto, Cointelegraph — carried from 21:39.)
- **Price-reaction / chase check:** desk entry is a **failed bounce/retest into 2.443–2.499**, SL 1h close beyond 2.540, TP1 2.327 (RR ~1.84). Live ~2.42–2.44 after a −13/−18% flush — the move **already happened**; the desk explicitly states *"no late short after a vertical flush."* Shorting here chases exhausted sellers into support (2.294). The crypto short bucket is itself net-losing (PF 0.00 / −7R).
- **Verdict:** **NO-TRADE / WATCHLIST overnight.** Only a *conditional* short on a clean failed bounce into 2.44–2.50 (SL 2.540); do not chase. Catalyst-aligned but execution-gated and late.

### 7.2 BTC/USDT — macro driver, not a desk signal → **RISK MONITOR (downside-skewed overnight)**
- **Role:** the overnight tape-setter; no active BTC trade idea, but it governs every alt.
- **Catalyst (verified):** **20th consecutive day of US spot-ETF net outflows — a record streak (~$2.97–3.45B cumulative)**, ~$1.5B liquidated on the week, SOL at a 2.5-yr low; the one bullish macro thread (US Treasury Bitcoin-reserve / CLARITY Act progress) is being ignored by price.
- **Price-reaction / chase check:** **~$63.6K, sub-$62K intraday, −13% week.** Below the report's 17:45-UTC $67K print — the tape deteriorated through the US session. No reclaim signal; structure is lower-highs/lower-lows.
- **Verdict:** **No long until the ETF-outflow streak breaks and BTC reclaims structure; a loss of ~$61–62K risks a cascade.** Size down / stand aside across crypto overnight. This is the single most important overnight-into-Asia variable.

### 7.3 AMD — A-tier LONG 84.71 (stocks intraday, at close) → **DAILY WRAP: chase avoided; tomorrow WAIT for a pullback**
- **Tier/role:** A-tier 84.71 (high conf, RS leader +21.41% vs SPY 20d). Closed **$542.52 (+4.02%)**.
- **Outcome:** entry zone **519.19–525.01**, TP1 **542.46**. AMD **closed at TP1, ~$18 above the entry-zone top** — the recovery ran the full distance with no pullback into the zone. The 21:39 "do not chase at ~$542" was correct: chasing = buying the high into the target.
- **Statistical caveat:** A-tier stocks bucket this week **PF 0.20, WR 6.2%, −8R** (n=27) — highest-conviction tier, worst performer (TODO-stocks-atier-winrate).
- **Verdict (next day):** **WAIT — long only on a pullback into 519–525 (SL ~512), half-size given the A-tier loser context. Do not chase the close at TP1.**

### 7.4 UNH — B-tier LONG 75.9 (stocks intraday, at close) → **THESIS CONFIRMED (day's rotation winner); tomorrow cautious long on a pullback**
- **Tier/role:** B-tier 75.9 (medium conf); defensive healthcare, RS vs SPY +4.66%, earnings-safe.
- **Catalyst (verified, strengthened):** **BofA Neutral→Buy, PT $420→$450**; **Morgan Stanley OW, PT $453** (both June 4); stock **+5.7%** on the day. **Health Care was the #1 S&P sector (+3.14%)** at the close — the defensive rotation the desk flagged was the day's winning trade. (GuruFocus, Medical Daily, Investing.com — carried from 21:39.)
- **Price-reaction / chase check:** entry zone **393.47–396.01**, SL beyond 388.39, TP1 403.62 (RR ~1.0, desk-flagged). After +5.7% it has largely priced the upgrade → **demand a pullback into the zone; do not chase the gap.**
- **Verdict (next day):** **CAUTIOUS LONG on a pullback into 393–396, half-size (SL 388.39).** The cleanest catalyst + rotation name; the edge is catalyst/sector, not geometry.

### 7.5 SMCI — `no_trade` rejected 51.01 at close (was B-tier 79.71 earlier) → **AVOID / MANUAL REVIEW REQUIRED (legal/export-control overhang)**
- **Tier/role:** de-escalated to **rejected `no_trade` (51.01)** in the close snapshot; older active B-tier swing/intraday signals (76/79) still linger in `active-signals`.
- **LEGAL/HEADLINE RISK (verified):** **March 19 2026 SDNY indictment** of three SMCI-associated individuals for an alleged export-control conspiracy (**~$2.5B of AI servers diverted to China without licenses**; board member Liaw resigned; acting Chief Compliance Officer appointed). Fresh export-control scrutiny kept the overhang active today (QuiverQuant, Super Micro IR / SEC 8-K — carried from 21:39). Historical: prior SEC accounting probe + E&Y resignation. Also a semi/AI-server name in today's flush.
- **Verdict:** **AVOID / MANUAL REVIEW REQUIRED — never a clean actionable while the export-control/compliance overhang stands**, regardless of score.

_(NVDA — B 74.79, closed $214.75 −3.62%, below its 218.76–219.98 entry: WATCH → long only on a reclaim of ~219; the trigger never fired today. Listed in §8.)_

---

## 8. Best Candidates Ranked

_All stock names are next-session planning (US market is closed). Crypto is the live overnight class._

1. **UNH (stocks, next day) — CAUTIOUS LONG on a pullback into 393–396, half-size (SL 388.39).** Day's rotation winner; cleanest catalyst + sector-lead name; just don't chase the +5.7% gap.
2. **AMD (stocks, next day) — A-tier but WAIT.** Closed at TP1; only re-engage on a pullback into 519–525 (SL ~512), half-size.
3. **NVDA (stocks, next day) — WATCH → long on a reclaim of ~219.13 (SL 216.66).** Closed red below the trigger; needs to prove stabilization.
4. **NEAR/USDT (crypto, overnight) — WATCHLIST / conditional short only on a failed bounce into 2.44–2.50 (SL 2.540).** Catalyst-aligned but late; do not chase the flush.

_(SMCI excluded — AVOID, §9. No clean *active* overnight crypto actionable.)_

---

## 9. Avoid / No Trade

- **SMCI** — active export-control/compliance overhang (§7.5). AVOID / manual review.
- **Chasing AMD at the close (~$542 / TP1)** — wait for a pullback (§7.3).
- **Chasing the NEAR flush** — no late short after a −13/−18% vertical move (§7.1).
- **Crypto longs broadly overnight** — bearish regime, BTC sub-$64K with a record 20-day ETF exodus; counter-tape RS-leader pops (WLD/EPIC/ALLO/HOME) are watchlist-only.
- **AVGO** — fully reacted (−15%); context, not a trade.
- **NVDA below 219** — no trade until it reclaims the trigger.

---

## 10. Main Risks

- **Overnight crypto downside is the dominant live risk:** BTC ~$63.6K, sub-$62K intraday, **record 20-day spot-ETF exodus (~$2.97–3.45B)**, SOL 2.5-yr low, ~$1.5B liquidated. **A loss of ~$61–62K risks a liquidation cascade into the Asia session.** Crypto headline B-tier bucket is net-losing (PF 0.82, −3R; shorts PF 0.00 / −7R).
- **Highest-conviction stock tier is the worst performer:** A-tier PF 0.20 / WR 6.2% / −8R (n=27) vs B-tier PF 1.28 / +14R. Treat A-tier scores (AMD) with extra skepticism, not extra size (TODO-stocks-atier-winrate).
- **Semi recovery is fragile:** AMD closed at TP1 but the group (AVGO −15%, NVDA red) is the most-stretched cohort; a re-acceleration of AVGO weakness or NVDA losing ~$211 would pressure the rotation. The rotation into value/defensives is the more durable trade.
- **Catalyst layer is context-only:** 74.6% of events unmapped — do not let the catalyst layer drive a final decision this run.
- **Crypto reports aging:** scalp/intraday are ~2.5–2.9 h old (last cycle 20:02); read the next default cycle's snapshot before acting overnight.
- **Notifier:** if `TELEGRAM_BOT_TOKEN`/`config/notifications.yaml` lacks a token/chat_id, the §12 Telegram send is skipped (logged here), not crashed.
- **Source ingest:** if `ingest_enriched_review_sources` fails, it is logged here and the review still stands (sources are also in §13).

---

## 11. Action Plan — next 4 hours (overnight into Asia)

- **Crypto (live):** **no-trade / watchlist.** Watch **BTC ~$61–62K** — a break risks a cascade; size down or stand aside. NEAR short only on a failed bounce into 2.44–2.50 (SL 2.540) — otherwise no-trade; do not chase the flush. WLD/EPIC/HOME only for a high-volume continuation, not a counter-tape chase. Track whether the ETF-outflow streak (now 20 days) extends or breaks.
- **Stocks (closed — prep for next session):**
  - **UNH:** wait for a pullback into **393–396**; cautious half-size long, SL 388.39, TP1 403.62. Don't chase the +5.7% gap. The healthcare/defensive lead is the day's confirmed trend.
  - **AMD:** do not chase the TP1 close ($542.52). Re-engage only on a pullback into **519–525**, SL ~512, half-size.
  - **NVDA:** watch for a reclaim + hold of **~219.13**; then long, SL 216.66, TP1 ~224. Below that, no trade.
  - **SMCI:** avoid while the overhang stands.
- **Asia 04:30 slot inherits:** a fragile risk-off crypto tape (BTC sub-$64K, record ETF exodus) and a US session that **closed on a value/defensive rotation with the Dow at a record and the Nasdaq red** — i.e. AI de-risking, not AI collapse. Re-check BTC support and the ETF-flow streak first.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO-TRADE / watchlist.** Bearish regime; NEAR short is late (post-flush). Headline bucket net-losing.
- **Crypto intraday:** **NO-TRADE / conditional** — SHORT NEAR/USDT only on a failed bounce into 2.44–2.50 (SL 2.540); otherwise no-trade.
- **Crypto swing:** **NO-TRADE** (report ~8.8 h carry-forward; bearish tape, no fresh A/B).
- **Stocks intraday (closed — next-session):** **UNH cautious half-size long on a pullback (393–396, SL 388.39); AMD wait (closed at TP1 — pullback to 519–525 only); NVDA watch → long on reclaim ~219; SMCI avoid.**
- **Stocks swing (closed — next-session):** **AMD A-tier but extended — wait for the entry zone; UNH the disciplined catalyst-backed long.** (Report ~8.6 h carry-forward; corroborated by the fresh close snapshot + the day's healthcare lead.)
- **Stocks invest:** **carry-forward (~8.5 h)** — no fresh actionable; AMD/UNH long bias consistent, same level discipline applies.

---

## 13. Sources

**Stocks / US close (June 4 2026):**
- [Dow jumps 900 points, Nasdaq lags as investors rotate out of chip stocks for banks, retail — CNBC (2026-06-04)](https://www.cnbc.com/2026/06/03/stock-market-today-live-updates.html)
- [Broadcom's 13% Slide Puts AI Chip Valuations On Watch — Yahoo Finance (2026-06-04)](https://finance.yahoo.com/markets/stocks/articles/broadcoms-13-slide-puts-ai-191457169.html)
- [Why Broadcom Stock Crashed Today — The Motley Fool (2026-06-04)](https://www.fool.com/investing/2026/06/04/why-broadcom-stock-crashed-today/)
- [Market Outlook: Broadcom selloff exposes risks in AI stock surge — BNN Bloomberg (2026-06-04)](https://www.bnnbloomberg.ca/investing/market-outlook/2026/06/04/market-outlook-broadcom-selloff-exposes-risks-in-ai-stock-surge/)

**Crypto / macro:**
- [Bitcoin Price Today: BTC At $63,649 as Selloff Hits 13% on the Week, $1.5B Liquidated — BlockchainReporter (2026-06-04)](https://blockchainreporter.net/bitcoin-price-today-btc-at-63649-as-selloff-hits-13-on-the-week-1-5b-liquidated/) _(WebFetch HTTP 403 — corroborated by FXLeaders/OpenPR below)_
- [Bitcoin Trapped at $63K by a Record 20-Day ETF Exodus — FXLeaders (2026-06-04)](https://www.fxleaders.com/news/2026/06/04/bitcoin-trapped-at-63k-by-a-record-20-day-etf-exodus/)
- [Bitcoin Price Prediction Turns Urgent as $2.97 Billion in ETF Outflows Sets a Record — OpenPR (2026-06-04)](https://www.openpr.com/news/4538770/bitcoin-price-prediction-turns-urgent-as-2-97-billion-in-etf)

**Carried-forward verified context (cited in the prior 21:39 review, still in force):** BofA UNH Buy PT $450 / MS OW PT $453 (GuruFocus, Medical Daily, Investing.com); SMCI SDNY export-control indictment (QuiverQuant, Super Micro IR / SEC 8-K); Arthur Hayes dumps HYPE+NEAR (BeInCrypto, Cointelegraph).

_Dates are publisher-reported. No fabricated TradingView/chart observations. No `test_source`/fixture URLs._

---

## 13b. Source-Discipline Checklist (§N)

- Every external claim has source + title + date + URL — **yes** (§13).
- No uncited stats; no uncited legal claims — **yes** (SMCI legal carried with citation).
- No fabricated TradingView observations — **yes** (chart tools not loaded; declared).
- Missing source → wrote the limitation (UNH exact close not isolated; BlockchainReporter 403) instead of guessing — **yes**.
- `test_source` / fixture URLs filtered — **yes**.
- §13 Sources present — **yes**.
- Web available → no "External web research unavailable" declaration needed.

---

## 14. Fix Requests / TODO

### TODO-untracked-epic-alert
- **issue:** `detect_untracked_legacy_alerts` shows 1 untracked crypto alert (EPIC/USDT B scalp long, sent 2026-06-04 10:03 UTC) with no matching `proposed_signal` → excluded from PF/winrate. Persists across the 18:39 / 21:39 / 23:30 runs.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-06-04` → "1 untracked legacy crypto alert(s)"; EPIC/USDT, tier B, scalp, score 66.0, long, sent_at 2026-06-04T10:03:27+00:00, trackable NO.
- **suggested manual fix:** investigate the scalp alert→proposed_signal write path (PART-1 tracker) so Telegram-sent legacy alerts always create a tracked signal_id; backfill or reconcile the EPIC row.
- **priority:** medium
- **first observed:** 2026-06-04 18:39 EEST (re-confirmed 23:30 EEST)

### TODO-catalyst-mapping-weak
- **issue:** catalyst symbol-resolver maps only ~25% of events (74.6% unmapped); explicitly-tickered names are dropped into the unmapped bucket. Multi-run regression (76.2% → 75.2% → 74.6%, now stable at 74.6%).
- **evidence:** `catalyst_events.jsonl` 2026-06-04: total 2344, mapped 595, unmapped 1749 (74.6%). Top unmapped: "Tilly's (TLYS) Q1 2026 Earnings Call Transcript", "Petco (WOOF) …", "ChargePoint (CHPT) …" — all carry a parenthetical ticker.
- **suggested manual fix:** add a parenthetical-ticker regex (e.g. `\(([A-Z]{1,5})\)`) and an earnings-transcript-title resolver to the catalyst symbol-mapping layer; validate against the unmapped sample.
- **priority:** medium
- **first observed:** prior runs (re-confirmed 2026-06-04 23:30 EEST)

### TODO-stocks-atier-winrate
- **issue:** A-tier stocks bucket is a reproducible loser — PF 0.20, WR 6.2%, totalR −8.0 (n=27) — while B-tier is positive (PF 1.28, +14R). Today's A-tier name (AMD) closed exactly at TP1 after the entry had aged into a chase, consistent with the bucket selecting overextended/late entries.
- **evidence:** `python -m src.cli signal-stats --asset-class stocks` (week): tier split A-tier PF 0.200 / WR 6.2% / −8R; B-tier PF 1.28 / +14R; C-tier PF 1.21 / +6R. Observation engine flags: "tier=A profit factor 0.20 below 0.8".
- **suggested manual fix:** audit what pushes a stock setup into A-tier (score ≥ ~80) vs B-tier; consider an overextension/chase penalty (price > N ATR above entry, or already at/through TP1) before A-tier promotion.
- **priority:** medium
- **first observed:** prior runs (re-confirmed 2026-06-04 23:30 EEST)

### TODO-crypto-short-bucket-bleed
- **issue:** crypto short-direction signals are net-losing — direction "short" PF 0.00, totalR −7.0 (n=17), while longs are positive (PF 1.36, +4R) — yet the desk keeps emitting B-tier shorts into post-flush, exhausted-seller setups (e.g. NEAR after −13/−18%).
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` (week): By direction — short PF 0.00 / −7R; long PF 1.36 / +4R.
- **suggested manual fix:** add a "no late short after a vertical flush" gate (e.g. reject/demote shorts where 24h move < −12% and price is within ~1 ATR of support) so catalyst-late shorts go to watchlist instead of active B-tier.
- **priority:** low
- **first observed:** 2026-06-04 21:39 EEST (re-confirmed 23:30 EEST)
