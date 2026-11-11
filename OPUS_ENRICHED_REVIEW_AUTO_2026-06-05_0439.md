# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

- **Generated:** 2026-06-05 04:39 EEST (auto-enriched-review, scheduled task `opus-enriched-review-4h`, Asia/overnight slot 04:30).
- **Slot:** **Crypto overnight / Asia review** — overnight crypto action + the Asia session. **US stocks are CLOSED** → all stock signals are next-session **planning/watchlist context only**; **crypto is the sole live actionable class**.
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-04_2330.md` (≈5.2 h ago, post-close slot — §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified UNH DOJ/antitrust probe (5 sources), SMCI legal status (now Nasdaq-compliant), AMD sector-sympathy selloff, SUI (no fresh catalyst), and BTC macro (~$61–63K, 13-day ETF outflow streak, Fear&Greed 23). One WebFetch (CoinDesk BTC) opened cleanly; one (MedicalEconomics UNH) returned HTTP 403 → fell back to 4 corroborating sources.
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; all price/structure is local OHLCV/ATR/EMA report fields + cited external prints.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

- **Headline finding (NEW, integrity): the desk is emitting UNH as an A-tier (81.3) intraday LONG while UNH is under an active DOJ Medicare-fraud investigation AND a DOJ antitrust probe of Optum — stock down ~55% from its highs.** Prior reviews (21:39 / 23:30) treated UNH as "the cleanest catalyst + rotation name." External research this run **contradicts that** per §I: an active federal fraud investigation is a hard legal/headline-risk gate. **UNH → AVOID / MANUAL REVIEW REQUIRED, regardless of the A-tier score.** The scoring/legal-risk layer is not catching this (→ TODO-unh-legal-gate, §14, **high**).
- **Crypto is the only live class and it is risk-off / downside-skewed.** Regime **bearish trend**; BTC/ETH downtrend; breadth ~29% > EMA20; BTC ATR percentile 96 (elevated). External: **BTC slid below $63K (low ~$61.4K) — lowest since February**, **13th consecutive day of spot-ETF net outflows (>$5B over 4 weeks)**, **Fear & Greed 23 (Extreme Fear)**, Strategy disclosed its first BTC sale in years. Key support **$60K, then $50K**. The prior review's "$61–62K cascade level" is now being tested.
- **No clean *active* crypto actionable overnight.** The live desk ideas are all **conditional/late**: B-tier SHORT **SUI/USDT** (66.2) is a *failed-bounce* short needing a bounce into 0.7676–0.7751 (price ~0.766, just below the zone — not yet triggered); B-tier SHORT **NEAR/USDT** (66/70) is **catalyst-aligned but late** after a −21% RS flush (desk's own rule: "no late short after a vertical flush"). Crypto **short bucket is net-losing this week (PF 0.28, −5R)** — demand confirmation, don't chase.
- **Stocks (planning only — closed):** **AMD** is the cleanest A-tier long (swing 81.8, invest B 78.3) but **waiting_for_entry below price** after Thursday's **Broadcom-led semi-sector sell-the-news** (AVGO soft AI guide, AMD −4% to ~$521 on *no company-specific news*) — wait for the **501–516** pullback zone, don't chase; A-tier stocks remain the worst bucket (PF 0.20, −8R). **SMCI** (C-tier 76–79) **de-escalated**: it regained Nasdaq compliance Jan 27 2026, but the SDNY export-control matter keeps it a **caution/AVOID** name.
- **Net verdict:** **Overnight crypto = no-trade / watchlist, downside-skewed** (respect the $60–62K cascade zone). **Stocks next-session: AMD wait-for-pullback, UNH now AVOID (DOJ), SMCI avoid/caution, NVDA watch.** Catalyst layer is **context-only** this run (72.4% unmapped).

---

## 2. Data Used

**Internal — fresh (<4 h):**
- `data/reports/scalp/2026-06-04_23-44_scalp_report.md` (gen 02:44 EEST; ~1.9 h). Regime **bearish trend (risk-off)**; no A-tier; best idea B SHORT SUI 66.2; rest watchlist.
- `data/reports/intraday/2026-06-05_00-03_intraday_report.md` (gen 03:03 EEST; data freshness 23:45 UTC; ~1.6 h). Regime bearish; breadth 29.2% > EMA20; BTC ATR pct 96. **No A/B** — best watchlist SUI 64.2.
- `data/reports/stocks/intraday/2026-06-05_00-09_stocks_intraday_report.md` (gen 03:09 EEST; ~1.5 h) — used as planning context (US closed).

**Internal — carry-forward (4–12 h, flagged §3):**
- `data/reports/swing/2026-06-04_14-44_swing_report.md` (crypto; ~10.9 h) — carry-forward.
- `data/reports/stocks/swing/2026-06-04_14-55_stocks_swing_report.md` (~10.7 h) — carry-forward.
- `data/reports/stocks/invest/2026-06-04_15-01_stocks_invest_report.md` (~10.6 h) — carry-forward.

**Catalyst / narrative / packets:**
- `data/catalysts/2026-06-05/` — `catalyst_events.jsonl` (492 rows), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_00-03.md` (mtime 03:03).
- LLM packets: `data/processed/llm_analysis_packet.md` (gen 03:03), `llm_stocks_packet.md` (gen 03:10).

**CLI / DB:** `active-signals` (crypto **9** / stocks **50**), `signal-stats` (crypto + stocks, week), `detect_untracked_legacy_alerts --since 2026-06-05` → **0 untracked** (improved from 1). DB: `db/crypto_ai_desk.sqlite` (671 MB, mtime 04:37). `news_items` queried read-only (t.me 4h, candidate 24h, legal keywords 48h).

**External (this run — cited §13):** UNH DOJ Medicare-fraud + Optum antitrust probe (Yahoo Finance, QuiverQuant, MedicalEconomics, Phemex); SMCI Nasdaq compliance regained Jan 27 2026 + historical E&Y/SEC/SDNY matters (Motley Fool, GuruFocus, times-online); AMD/AVGO semi sell-off (24/7 Wall St, FXLeaders, MSN/Yahoo); SUI no fresh catalyst (CoinGecko/CoinMarketCap, older May outages/CME futures); BTC macro (CoinDesk, Investing.com, CryptoTimes).

**Unavailable / blind:** live tick prints; TradingView/Chrome chart verification (not loaded); liquidation heatmaps, order-book/CVD, live ETF-flow feed, on-chain whale flows, token-unlock calendar (manual/unconnected); live social beyond RSS-bridged `t.me/*` (which this run was pure noise — lookonchain welcome messages + one HYPE whale-buy line).

---

## 3. Scheduler / Data Freshness

- Latest schedule folder: `data/scheduled_runs/2026-06-04_default_schedule/`.
- `scheduler.log` mtime **03:10 EEST → ~1.5 h** (fresh). Latest cycle summary `cycle_04_02-20_summary.md` mtime **03:10 EEST → ~1.5 h** (fresh, under 3 h).
- **NO DEFER** — both freshness checks under the 3 h rule. Review proceeds normally.
- **Fresh (<4 h):** crypto scalp (~1.9 h), crypto intraday (~1.6 h), stocks intraday (~1.5 h).
- **Carry-forward (4–12 h, used + flagged):** crypto swing (~10.9 h), stocks swing (~10.7 h), stocks invest (~10.6 h). None > 14 h → no stale exclusions, but swing/invest verdicts (§12) carry the carry-forward caveat. (Stocks are closed regardless, so swing/invest are planning-only.)

---

## 4. What Changed vs Previous Review (23:30 → 04:30)

- **UNH thesis REVERSED on new external evidence.** Prior review: UNH "B-tier 75.9 → cautious long, the day's rotation winner." This run UNH appears as **A-tier 81.3 intraday long (triggered)** in `active-signals`, and external research surfaced an **active DOJ Medicare-fraud investigation + DOJ antitrust probe of Optum** (§7.1). **UNH is now AVOID / MANUAL REVIEW** — a material correction the prior two reviews missed.
- **BTC kept bleeding into the cascade zone, as flagged.** 23:30 had BTC ~$63.6K with a "loss of $61–62K risks a cascade" warning; current external prints show **BTC slid below $63K to ~$61.4K intraday** — the warning level is being tested. ETF-outflow streak framed as **13 consecutive days** by current sources (CoinDesk/Investing) vs the "20-day" framing prior sources used — same direction, different counting window; either way the streak persists and Fear&Greed sits at **23 (Extreme Fear)**.
- **AMD pulled back toward its entry zone.** 23:30: AMD closed $542.52 *at TP1*, "wait for a pullback to 519–525." This run: AMD A-tier **swing** 81.8 entry **501–516** (waiting_for_entry), trading ~$521 — the pullback the desk wanted is closer; still above the zone, still wait.
- **SMCI de-escalated further (legal status improved).** Prior: AVOID on active SDNY export-control indictment + compliance overhang. New external: SMCI **regained full Nasdaq compliance Jan 27 2026**; the indictment was of three associated individuals (early 2026, historical). Verdict stays **caution/AVOID** for headline risk, but the acute delisting risk has resolved (§7.2).
- **Integrity: untracked-alert count 1 → 0 (RESOLVED).** The EPIC/USDT untracked legacy alert that persisted across 18:39/21:39/23:30 is gone this run → **TODO-untracked-epic-alert resolved** (§14).
- **Catalyst mapping marginally better but still weak:** 74.6% → **72.4% unmapped**.
- **Crypto active set:** 10 → **9**; NEAR short persists (now late post-flush); SUI is the freshest scalp idea (B 66.2 short, conditional).
- **Persisting quality flags (re-confirmed):** A-tier stocks loser bucket (PF 0.20, −8R, n=27); crypto short bucket bleed (PF 0.28, −5R, n=18). **Exchange-confirmed crypto signals strongly outperform** (PF 2.28, +9R) vs unconfirmed (PF 0.42, −4R) — a usable filter.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (`data/catalysts/2026-06-05/catalyst_events.jsonl`): **492**; mapped (non-null `symbol`): **136** (27.6%); unmapped: **356** → **72.4% unmapped**.
- `narrative_baskets`: **3** — `perps_dex_narrative` (playbook `wait_pullback`, primary HYPE/USDT, fresh <6h), `ai_narrative` (`related_beta_rotation`, primary NEAR/RENDER/TAO/FET, fresh <24h), `momentum_breakout` (`wait_pullback`, primary MEME/USDT +12.1%, fresh <1h). All `single_source`.
- **⚠️ catalyst mapping weak this run — use the catalyst layer as context, not a final decision.** (unmapped 72.4% > 50%).
- Top 3 unmapped headlines (symbol unresolved despite explicit/derivable tickers): (1) "Dimon and Musk launch SpaceX IPO roadshow in New York"; (2) "5 Top Artificial Intelligence (AI) Stocks to Buy With $5,000 Right Now"; (3) "Palantir partners with Kirkland & Ellis to develop AI tools for private equity" (**PLTR** derivable). Same resolver weakness as prior runs → TODO-catalyst-mapping-weak (§14).

---

## 6. Market Landscape

**Crypto (24/7 — the live overnight-into-Asia class):** Regime **bearish trend / risk-off**. BTC & ETH downtrend; altcoin breadth **29.2% > EMA20** (25% > EMA50); BTC ATR percentile **96 (elevated)**. External macro (June 4–5): **BTC below $63K, intraday low ~$61.4K — lowest since February**, **−14% week / −21% over 4 weeks**, **13th straight day of spot-ETF net outflows (>$5B cumulative / 4 wks)**, **Fear & Greed 23 (Extreme Fear)**, BVIV implied-vol 53.17 (highest since Apr 2). Strategy (ex-MicroStrategy) disclosed its first BTC sale in years; Mt. Gox-liquidation chatter adds supply fear. **Key support $60K, then $50K.** Narrative heatmap: **AI "rising"** on attention but **every AI alt is red** (NEAR −21%, TAO −7.8%, RENDER −13%) — bleeding, not leading. Counter-tape green outliers (HOME +43%, MEME +12%, HEI +22%, EPIC +32%) are **low-volume (0.1–0.7x) watchlist-only momentum pops** in a bearish tape, all flagged "reduce size / counter-tape." **Overnight risk is skewed down: a sustained break of ~$60–62K risks a liquidation cascade into the Asia session.**

**Stocks (CLOSED — next-session planning):** Thursday (June 4) was a **Broadcom-led AI-semi sell-the-news**: AVGO beat but guided AI Q3 ~$16B vs ~$17.3B est, **−14/−15%**, dragging AMD/Intel/Micron/ARM/MRVL on sector sympathy with **no company-specific news** for AMD (−4% to ~$521). The desk's stocks snapshot still reads constructive underneath (value/defensive bid). For the next session the live planning names are **AMD (A-tier long, wait for the 501–516 pullback)**, **UNH (now AVOID — DOJ)**, **SMCI (caution)**, **NVDA (watch for a reclaim)**.

---

## 7. Candidate Deep Dives (≤5)

### 7.1 UNH — stocks A-tier LONG 81.3 (intraday, triggered) → **AVOID / MANUAL REVIEW REQUIRED (active DOJ investigation)**
- **Tier/role:** A-tier 81.3 intraday long (also B invest 70.5, B swing 73.6) — the model's top-scored stock long. US closed → planning only.
- **LEGAL/HEADLINE RISK (verified, §I):** UNH is under an **active DOJ investigation into Medicare Advantage billing** (alleged inflated risk scores / diagnoses added without physician confirmation — potential fraud), **and a separate DOJ antitrust probe of the Optum–insurance relationship.** UNH disclosed in a securities filing that it is cooperating with formal DOJ requests and launched a third-party policy review (expected complete by end of Q3). The stock is **~55% off its highs** on the DOJ probe + Medicare rate pressure + rising medical costs + leadership turnover + its first revenue decline in a decade. Internal `news_items` carried only a bullish "UNH/CVS flashing buy signals" item — the desk's catalyst layer **did not surface the DOJ overhang**.
- **Price-reaction / chase check:** entry 394.02–396.56, SL 388.95. Irrelevant to the verdict — an active federal fraud investigation is a hard gate.
- **Verdict:** **AVOID / MANUAL REVIEW REQUIRED.** Never a clean actionable long while the DOJ Medicare-fraud + antitrust investigations are open, regardless of the A-tier score. The model emitting this as A-tier is itself the issue → TODO-unh-legal-gate (§14).

### 7.2 SMCI — stocks C-tier 76–79 (intraday/swing/invest, several triggered) → **CAUTION / AVOID (headline risk; acute delisting risk resolved)**
- **Tier/role:** C-tier 79.7 intraday (triggered), 76.3 swing (triggered), 76.4 invest — carries a prior legal flag (standing watch). US closed → planning only.
- **LEGAL/HEADLINE RISK (verified, updated):** SMCI's saga (whistleblower accounting allegations → **Ernst & Young resignation** → Nasdaq non-compliance/delisting threat → **SDNY indictment of three associated individuals** for an alleged export-control conspiracy diverting AI servers to China) is **largely historical (late 2025–early 2026)**. As of **Jan 27 2026 SMCI regained full Nasdaq compliance** by filing its delayed reports. So the **acute delisting risk has resolved**, but the export-control matter + accounting history leave **elevated headline risk**.
- **Price-reaction / chase check:** N/A overnight (closed). Was a semi/AI-server name in Thursday's flush.
- **Verdict:** **CAUTION / AVOID for a clean A/B actionable** while the headline overhang stands; the de-escalation (compliance restored) is noted vs the prior unconditional AVOID. Not a fresh hard-gate this run, but not a name to chase.

### 7.3 AMD — stocks A-tier LONG 81.8 (swing, waiting_for_entry) / B invest 78.3 → **PLANNING: WAIT for the 501–516 pullback (do not chase)**
- **Tier/role:** A-tier swing 81.8 (waiting_for_entry, entry 501.05–515.74, SL 471.67); B invest 78.3 (entry 496.69–520.82, SL 448.43). US closed → planning only.
- **Catalyst (verified):** **No AMD-specific catalyst** — the weakness is pure **sector sympathy** to Broadcom's soft AI guide (AMD −4% to ~$521 on no company news). Internal `news_items`: "Why AMD Stock Is Sinking Today" (Motley Fool) + AVGO −15% premarket semis-sympathy — consistent.
- **Price-reaction / chase check:** trading ~$521, **above** the 501–516 swing entry zone → not yet actionable. The thesis isn't invalidated (sector-wide de-risk, not AMD fundamentals), but **A-tier stocks are the worst bucket this week (PF 0.20, −8R)** → discipline, half-size, no chase.
- **Verdict:** **WAIT — long only on a pullback into 501–516 (SL ~472), half-size given the A-tier-loser context.** Cleanest stock long once price comes in; respect the fresh semi-sector risk-off.

### 7.4 SUI/USDT — crypto B-tier SHORT 66.2 (scalp, waiting_for_entry) → **CONDITIONAL SHORT only (live, but not yet triggered)**
- **Tier/role:** the **best-scored live crypto idea** and the freshest scalp name; medium conf; bearish-regime-aligned breakdown/retest short. Multi-exchange confirmation 82.7 (binance+mexc), **no derivatives confirmation**.
- **Catalyst:** **none** — internal `news_items` shows 0 fresh SUI rows; external shows no June-5 catalyst (older May outages + CME-futures listing). Pure technical short.
- **Price-reaction / chase check:** current **0.7642–0.766**, short entry **0.7676–0.7751** (a *failed bounce* into the zone), SL 1h close beyond 0.7844, TP1 0.7474 (RR ~1.84), ATR 0.0168. Price is **just below the entry zone** → needs a bounce up into 0.7676–0.7751 to trigger; **not chasing a flush** (good structure) but **not yet active**. Support 0.7580.
- **Verdict:** **CONDITIONAL SHORT — only on a failed bounce/acceptance into 0.7676–0.7751 (SL 0.7844, TP1 0.7474).** No-trade until it sets up; demand confirmation given the crypto short-bucket bleed (PF 0.28). Prefer it over NEAR (better structure, not late).

### 7.5 NEAR/USDT — crypto B-tier SHORT 66.0 (intraday) / 70.5 (swing, tp1_hit) → **NO-TRADE / WATCHLIST (catalyst-aligned but late after the flush)**
- **Tier/role:** active B-tier short, the catalyst name; bearish-aligned. Swing leg already **tp1_hit**.
- **Catalyst (verified, internal-consistent):** **Arthur Hayes sold his entire HYPE + NEAR positions** (citing AI IPOs + US midterms), confirmed by 4 internal sources (The Block, CoinDesk, Cointelegraph, CryptoBriefing) + "NEAR gets demolished." NEAR is in the `ai_narrative` basket. No external lookup needed — internal is recent, multi-source, consistent.
- **Price-reaction / chase check:** NEAR **already flushed −21% RS**, current ~2.42–2.44; intraday short entry **2.443–2.487**, SL 2.540, swing TP1 already hit. The move **already happened** — the desk's own rule is **"no late short after a vertical flush,"** and shorting here presses exhausted sellers. Crypto short bucket is net-losing (PF 0.28, −5R).
- **Verdict:** **NO-TRADE / WATCHLIST.** Only a *conditional* short on a clean failed bounce into 2.44–2.49 (SL 2.540); do not chase the flush. Catalyst-aligned but execution-gated and late.

---

## 8. Best Candidates Ranked

_Stocks are next-session planning (US closed). Crypto is the live overnight class._

1. **AMD (stocks, next session) — A-tier long, WAIT for a pullback into 501–516 (SL ~472), half-size.** Cleanest stock long once price comes in; weakness is sector-sympathy, not AMD-specific. Do not chase ~$521.
2. **SUI/USDT (crypto, live) — CONDITIONAL SHORT only on a failed bounce into 0.7676–0.7751 (SL 0.7844, TP1 0.7474).** Best-structured live crypto idea; not yet triggered, demand confirmation.
3. **NEAR/USDT (crypto, overnight) — WATCHLIST / conditional short on a failed bounce into 2.44–2.49 (SL 2.540).** Catalyst-aligned but late; no chasing the flush.
4. **NVDA (stocks, next session) — WATCH → long only on a reclaim + hold of its entry zone.** Closed red with the chip group; needs to prove stabilization.

_(UNH excluded — AVOID, DOJ §7.1. SMCI excluded — caution/AVOID §7.2. No clean **active** overnight crypto actionable — all live crypto ideas are conditional.)_

---

## 9. Avoid / No Trade

- **UNH** — active DOJ Medicare-fraud investigation + DOJ Optum antitrust probe (§7.1). **AVOID / MANUAL REVIEW**, regardless of the A-tier 81.3 score.
- **SMCI** — residual export-control/accounting headline risk (§7.2). Caution/AVOID for a clean actionable (acute delisting risk resolved Jan 27 2026).
- **Chasing NEAR's flush** — no late short after a −21% vertical move (§7.5).
- **Crypto longs broadly overnight** — bearish regime, BTC sub-$63K (low ~$61.4K) with a 13-day ETF exodus and Extreme Fear; counter-tape RS-leader pops (HOME/MEME/HEI/EPIC) are low-volume watchlist-only.
- **Chasing AMD at ~$521** — wait for the 501–516 pullback (§7.3).
- **Unconfirmed crypto shorts** — exchange-unconfirmed signals are the losing bucket (PF 0.42, −4R); prefer derivatives/multi-exchange confirmation.

---

## 10. Main Risks

- **Overnight crypto downside is the dominant live risk:** BTC sub-$63K, intraday ~$61.4K, **13-day spot-ETF exodus (>$5B/4wk)**, Fear&Greed 23, Strategy selling, Mt. Gox chatter. **A sustained loss of ~$60–62K risks a liquidation cascade into Asia.** Crypto short bucket is net-losing (PF 0.28, −5R) — even correct-direction shorts are underperforming; size down / demand confirmation.
- **Model integrity — UNH A-tier on a stock under federal fraud investigation:** the legal-risk gate is not catching the DOJ overhang; an A-tier *actionable* long on UNH is a real exposure if traded off the score (→ TODO-unh-legal-gate, high).
- **Highest-conviction stock tier is still the worst performer:** A-tier PF 0.20 / −8R (n=27). Treat A-tier scores (AMD) with extra skepticism, not extra size (TODO-stocks-atier-winrate).
- **Catalyst layer is context-only:** 72.4% of events unmapped — do not let the catalyst layer drive a final decision this run.
- **Semi recovery is fragile:** AMD/NVDA are the most-stretched cohort post-AVGO; a re-acceleration of semi weakness pressures any long. Wait for the entry zone.
- **Notifier:** if `TELEGRAM_BOT_TOKEN`/`config/notifications.yaml` lacks a token/chat_id, the §12 Telegram send is skipped (logged here), not crashed.
- **Source ingest:** if `ingest_enriched_review_sources` fails, it is logged here (§10) and the review still stands (sources are in §13).

---

## 11. Action Plan — next 4 hours (overnight into Asia)

- **Crypto (live):** **no-trade / watchlist.** Watch **BTC ~$60–62K** — a break risks a cascade; size down or stand aside. **SUI short** only on a failed bounce/acceptance into **0.7676–0.7751** (SL 0.7844, TP1 0.7474) — otherwise no-trade. **NEAR short** only on a failed bounce into **2.44–2.49** (SL 2.540) — do not chase the flush. Counter-tape pops (HOME/MEME/HEI/EPIC) only on a high-volume continuation, not a chase. Track whether the ETF-outflow streak extends or breaks, and prefer exchange-confirmed setups.
- **Stocks (closed — prep for next session):**
  - **AMD:** do not chase ~$521. Re-engage only on a pullback into **501–516**, SL ~472, half-size (A-tier-loser discipline).
  - **UNH:** **AVOID** — active DOJ investigation; do not trade the A-tier long.
  - **NVDA:** watch for a reclaim + hold of its entry zone, then long with a tight SL; below that, no trade.
  - **SMCI:** avoid/caution while the headline overhang stands.
- **Next slot (11:30 Europe / pre-US) inherits:** a risk-off crypto tape testing the $60–62K cascade zone, and a US setup where the AI-semi de-risk (AVGO) is the dominant stock story. Re-check BTC support, the ETF-flow streak, and whether the UNH legal-risk gate has been addressed.

---

## 12. Final Verdict per Mode

- **Crypto scalp:** **NO-TRADE / watchlist.** Best idea B SHORT SUI is conditional (failed-bounce into 0.7676–0.7751, SL 0.7844) and not yet triggered. Short bucket net-losing.
- **Crypto intraday:** **NO-TRADE** — no A/B fresh; conditional SUI/NEAR shorts only on a failed bounce, otherwise stand aside.
- **Crypto swing:** **NO-TRADE** (report ~10.9 h carry-forward; bearish tape; NEAR swing already tp1_hit, no fresh A/B).
- **Stocks intraday (closed — next-session):** **AMD wait for 501–516 pullback (half-size); UNH AVOID (DOJ); SMCI avoid/caution; NVDA watch → long on a reclaim.**
- **Stocks swing (closed — next-session):** **AMD A-tier but extended — wait for the entry zone.** UNH AVOID. (Report ~10.7 h carry-forward.)
- **Stocks invest (closed):** **carry-forward (~10.6 h)** — AMD long bias consistent (entry 496–520), UNH excluded on legal risk; same level discipline.

---

## 13. Sources

**Stocks / UNH legal (verified):**
- [UnitedHealth Group under DOJ investigation over Medicare billing practices — Medical Economics](https://www.medicaleconomics.com/view/unitedhealth-group-under-doj-investigation-over-medicare-billing-practices) _(WebFetch HTTP 403 — corroborated below)_
- [With UnitedHealth Under DOJ Investigation, Should You Buy, Sell, or Hold UNH Stock Now? — Yahoo Finance](https://finance.yahoo.com/news/unitedhealth-under-doj-investigation-buy-110002685.html)
- [UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation — QuiverQuant](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe,+Shares+Dive+16%25+on+Fraud+Investigation)
- [DOJ Antitrust Probe Puts Focus On UnitedHealth Valuation And Integrated Model — Yahoo Finance](https://finance.yahoo.com/sectors/healthcare/articles/doj-antitrust-probe-puts-focus-030638086.html)
- [UnitedHealth Group (UNH) Stock in 2026: DOJ Probe, Medicare Reset, Key Risks — Phemex Academy](https://phemex.com/academy/unitedhealth-group-unh-stock-2026)

**Stocks / SMCI legal (verified):**
- [Super Micro Has Now Faced SEC Probes, Accounting Scandals, and Smuggling Charges — The Motley Fool (2026-03-20)](https://www.fool.com/investing/2026/03/20/super-micro-has-now-faced-sec-probes-accounting-sc/)
- [Super Micro Computer (SMCI) Regains Nasdaq Compliance After Accounting Saga — times-online (2026-01-27)](http://business.times-online.com/times-online/article/marketminute-2026-1-27-super-micro-computer-smci-regains-nasdaq-compliance-after-high-stakes-accounting-saga-igniting-fresh-market-volatility)
- [Super Micro Computer Faces Delisting Threat Amid Ongoing Challenges — GuruFocus](https://www.gurufocus.com/news/2584226/super-micro-computer-faces-delisting-threat-amid-ongoing-challenges)

**Stocks / AMD–AVGO semi selloff (June 4 2026):**
- [Broadcom Sinks 14% on Soft AI Chip Outlook, Dragging Down AMD and Intel — 24/7 Wall St.](https://247wallst.com/investing/2026/06/04/broadcom-sinks-14-on-soft-ai-chip-outlook-despite-earnings-beat-dragging-down-amd-and-intel/)
- [Intel, AMD, Micron shares sink as Broadcom results spark semiconductor sector sell-off — MSN/Yahoo](https://www.msn.com/en-us/money/markets/intel-amd-micron-shares-sink-as-broadcom-results-spark-semiconductor-sector-sell-off/ar-AA24Pq3z)
- [AVGO Stock Risks Breakdown Under $400 after Broadcom Earnings on the AI Guidance Shortfall — FXLeaders](https://www.fxleaders.com/news/2026/06/04/avgo-stock-risks-breakdown-under-400-after-broadcom-earnings-on-the-ai-guidance-shortfall/)

**Crypto / macro (June 4–5 2026):**
- [Bitcoin selloff continues as prices slide below $63,000 for the first time since February — CoinDesk (2026-06-04)](https://www.coindesk.com/markets/2026/06/04/bitcoin-selloff-continues-as-prices-slide-below-usd63-000-for-the-first-time-since-february) _(WebFetch opened cleanly — verified ~$63K, 13-day ETF outflows, $60K/$50K support)_
- [Bitcoin Falls as Record ETF Outflows and Strategy Sale Hit Sentiment — Investing.com](https://www.investing.com/analysis/bitcoin-falls-as-record-etf-outflows-and-strategy-sale-hit-sentiment-200681446)
- [Bitcoin Price Tumbles 50% from All-Time High – Is This the Bottom? — CryptoTimes (2026-06-04)](https://www.cryptotimes.io/2026/06/04/bitcoin-price-tumbles-50-from-all-time-high-is-this-the-bottom-or-further-pain-ahead/)

**Crypto / NEAR catalyst (internal, verified multi-source):** Arthur Hayes sells entire HYPE + NEAR positions — The Block, CoinDesk, Cointelegraph, CryptoBriefing (2026-06-04, internal `news_items`).

_Dates are publisher-reported. No fabricated TradingView/chart observations. No `test_source`/fixture URLs._

---

## 13b. Source-Discipline Checklist (§N)

- Every external claim has source + title + date + URL — **yes** (§13).
- No uncited stats; no uncited legal claims — **yes** (UNH/SMCI legal each carried with citations).
- No fabricated TradingView observations — **yes** (chart tools not loaded; declared).
- Missing source → wrote the limitation (MedicalEconomics 403 → 4 corroborating sources) instead of guessing — **yes**.
- `test_source` / fixture URLs filtered — **yes**.
- §13 Sources present — **yes**.
- Web available → no "External web research unavailable" declaration needed.

---

## 14. Fix Requests / TODO

### TODO-unh-legal-gate
- **issue:** The desk emits **UNH as A-tier 81.3 (intraday long, triggered)** — its top-scored stock long — while UNH is under an **active DOJ Medicare-fraud investigation AND a DOJ Optum antitrust probe** (stock ~55% off highs). The legal/headline-risk gate is not flagging or demoting UNH; the catalyst layer only ingested a bullish "buy signals" item. A scored A-tier *actionable* long on a stock under federal fraud investigation is a real exposure.
- **evidence:** `active-signals --asset-class stocks` → UNH A 81.3 intraday long (sig_aba948056b8fc1ab) + B invest 70.5 + B swing 73.6, all long; internal `news_items` legal-keyword scan for UNH (48h) → 0 rows; external (Yahoo Finance, QuiverQuant, Medical Economics, Phemex) → active DOJ Medicare-fraud + antitrust probe.
- **suggested manual fix:** wire a legal/headline-risk gate for stocks (DOJ/SEC investigation, indictment, antitrust probe, fraud) that demotes or hard-blocks A/B long signals; seed a watchlist of names under active federal investigation (UNH) so the score can't promote them to actionable longs without a manual override.
- **priority:** high
- **first observed:** 2026-06-05 04:39 EEST

### TODO-catalyst-mapping-weak
- **issue:** catalyst symbol-resolver maps only ~28% of events (72.4% unmapped); explicitly/derivably-tickered names are dropped into the unmapped bucket. Multi-run pattern (76.2% → 74.6% → **72.4%**, slowly improving but still > 50%).
- **evidence:** `catalyst_events.jsonl` 2026-06-05: total 492, mapped 136, unmapped 356 (72.4%). Top unmapped: "Dimon and Musk launch SpaceX IPO roadshow…", "5 Top AI Stocks to Buy With $5,000…", "Palantir partners with Kirkland & Ellis… (PLTR)".
- **suggested manual fix:** add a parenthetical/embedded-ticker regex (e.g. `\(([A-Z]{1,5})\)`) + a known-entity name→ticker map ("Palantir"→PLTR, "Tesla"→TSLA) and an earnings-transcript-title resolver to the catalyst symbol-mapping layer; validate against the unmapped sample.
- **priority:** medium
- **first observed:** prior runs (re-confirmed 2026-06-05 04:39 EEST)

### TODO-stocks-atier-winrate
- **issue:** A-tier stocks bucket remains a reproducible loser — PF 0.20, totalR −8.0 (n=27) — while B/C tiers are positive (B-tier PF ~1.3 / +17R, C-tier PF ~1.4 / +12R). The model's highest-conviction tier is its worst performer.
- **evidence:** `signal-stats --asset-class stocks` (week): tier split — A-tier PF 0.20 / −8R (n=27); other tiers positive. Today's A-tier name (AMD) is a sector-sympathy dip with the entry above price.
- **suggested manual fix:** audit what promotes a stock setup to A-tier (score ≥ ~80); add an overextension/chase penalty and a legal/headline-risk demotion (see TODO-unh-legal-gate) before A-tier promotion.
- **priority:** medium
- **first observed:** prior runs (re-confirmed 2026-06-05 04:39 EEST)

### TODO-crypto-short-bucket-bleed
- **issue:** crypto short-direction signals are net-losing — direction "short" PF 0.28, totalR −5.0 (n=18) — while longs are positive (PF 1.54, +6R) — yet the desk keeps emitting B-tier shorts into post-flush, exhausted-seller setups (NEAR after −21%).
- **evidence:** `signal-stats --asset-class crypto` (week): By direction — short PF 0.28 / −5R; long PF 1.54 / +6R. By exchange_confirmation — confirmed PF 2.28 / +9R vs unconfirmed PF 0.42 / −4R (confirmation is the stronger usable filter).
- **suggested manual fix:** add a "no late short after a vertical flush" gate (reject/demote shorts where 24h move < −12% and price is within ~1 ATR of support) so catalyst-late shorts go to watchlist; weight exchange/derivatives confirmation higher in short-signal promotion.
- **priority:** low
- **first observed:** 2026-06-04 21:39 EEST (re-confirmed 2026-06-05 04:39 EEST)

### TODO-untracked-epic-alert — ✅ RESOLVED this run
- **status:** `detect_untracked_legacy_alerts --since 2026-06-05` → **0 untracked** (was 1 EPIC/USDT across 18:39/21:39/23:30). The EPIC/USDT legacy alert now has a backing `proposed_signal` or has aged out. No action needed unless it recurs; retained here for diff continuity.
- **first observed:** 2026-06-04 18:39 EEST | **resolved observed:** 2026-06-05 04:39 EEST
