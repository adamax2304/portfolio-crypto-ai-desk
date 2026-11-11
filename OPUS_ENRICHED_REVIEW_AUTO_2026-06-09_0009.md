# Opus Enriched Review — post-close final daily review — Auto Cycle 00:09 EEST

- **Generated:** 2026-06-09 00:09 EEST (auto-enriched-review, scheduled task `opus-enriched-review-postclose`, **23:15 "post-close final daily review" slot**, executing `opus-enriched-review-4h/SKILL.md`). US cash session closed ~1h ago (4 PM ET = 23:00 EEST).
- **It is Tuesday 2026-06-09 00:09 EEST.** This is the post-close daily wrap for Monday June 8, 2026. US equities closed ~1h ago; crypto is live/overnight; Asia open in ~3.5h (Tokyo ~06:00 EEST).
- **Prior review compared:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-08_1624.md` (pre-US-open decision review, 16:24 EEST, ~7.75h ago — see §4).
- **External web research:** AVAILABLE (WebSearch + WebFetch loaded). Verified: **US closed** S&P 500 +0.30% at 7,405.73 · Nasdaq +0.86% at 25,929.66 · Dow −0.16% at 50,786.01 · Semis (SOXX) **+~7%** (MU +10%, MRVL +14%, INTC +12%) · BTC ~$63,564 at 9:30 ET (Fortune/Yahoo verified) · ETH ~$1,689. TheStreet June 8 page returned HTTP 403; data confirmed via search snippet (CNBC/TheStreet).
- **Chart tools:** TradingView / Chrome MCP **not loaded** — no chart observations fabricated; structure from OHLCV/ATR/EMA fields in reports + cited external data only.
- **Advisory only. No auto-trade. Read-mostly per PART 16 permission contract.**

---

## 1. Executive Summary

**The US session closed constructively but narrowly, driven by a chip-led relief rally after Friday's −4.2% Nasdaq rout.** S&P 500 +0.30% · Nasdaq +0.86% · Dow −0.16%. Semiconductors dominated: SOXX +~7%, MU +10%, MRVL +14%, INTC +12%. The rally was selective — small caps underperformed, Dow was negative — meaning breadth did not confirm broad risk-on.

**The 16:24 pre-US-open call was vindicated.** That review correctly identified the desk's stale short-bias stock list as a gap-risk trap and required RTH confirmation before any shorts. The market went UP; META/PLTR/GOOGL shorts (all triggered) ran against the tape all session. Post-track confirms `stopped=3`. This is the defining lesson of the day.

**Crypto ended range-constructive.** BTC traded ~$62.5–63.5k all session, recovering from the weekend <$60k dip (first sub-$60k since 2024). ETH ~$1,689. Notable altcoin RS: WLD +13.26%, BIO +19.42%, LAYER +27.43%, STG +22.23%. No A/B signal generated (regime = range/chop). Nine crypto B-tier signals active; ZEC across multiple modes hitting TPs (Ironwood upgrade catalyst). BTC ETF outflows remain the structural headwind (−$1.67B weekly, 3rd consecutive outflow week, ~$4.21B over 3 weeks).

**Overnight Asia setup: mild constructive in range.** RS leaders (WLD, ZEC pullback, BIO) are the watch. BTC must hold $62k+. ETF outflow pressure and geopolitical uncertainty (Iran/Israel tensions remain) cap the upside. No forced positions.

**Signal performance divergence is critical.** Crypto B-tier: n=69, PF **1.74**, +14R week. Stocks A/B: n=142, PF **0.46**, **−29R** week. Stocks swing under 48h audit cap (−12R, 0W/12L). This is a systematic failure requiring manual strategy review (see §14).

---

## 2. Data Used

**Internal — crypto reports (freshness vs 00:09 EEST now):**
- `data/reports/scalp/2026-06-08_20-22_scalp_report.md` — gen ~23:22 EEST, **~47 min → FRESH.** Regime range/chop; BTC range; breadth EMA20 60% / EMA50 26.7%; BTC ATR pct 63. No A/B. Best watchlist WLD 60.2.
- `data/reports/intraday/2026-06-08_20-37_intraday_report.md` — gen ~23:37 EEST, **~32 min → FRESH.** No A/B. Best watchlist ZEC 59.7 / INJ 58.3 / WLD 57.4. AI narrative rising (heat 56). 3 baskets active.
- `data/reports/swing/2026-06-08_01-10_swing_report.md` — gen 04:10 EEST, **~20h → STALE** (context only; excluded from fresh swing verdict).
- `data/reports/stocks/intraday/2026-06-08_20-50_stocks_intraday_report.md` — gen ~23:50 EEST, **~19 min → FRESH.** Market-closed header (planning/watchlist only). Regime: **risk_off**, VIX 18.92, breadth EMA20 25%. A/B=0. C-tier watchlist: LLY long (64.6), XLY/META/SMH/AMZN/AMD shorts.
- `data/reports/stocks/swing/2026-06-08_01-14_stocks_swing_report.md` — gen 04:14 EEST, **~20h → STALE.** Under 48h cap (−12R, 0W/12L audit).
- `data/reports/stocks/invest/2026-06-08_01-18_stocks_invest_report.md` — gen 04:18 EEST, **~20h → STALE** (context only).

**Catalyst / narrative:** `data/catalysts/2026-06-08/` — **1,068 unique events today**, **3 baskets** (ai_narrative, perps_dex_narrative, momentum_breakout). Latest catalyst scan (cycle step 4): events=500, baskets=3.

**LLM packet:** `data/processed/llm_analysis_packet.md` — gen 20:37 UTC (23:37 EEST), FRESH.

**Scheduler:** `2026-06-08_default_schedule/`, `scheduler.log` mtime 23:52 EEST (~17 min ago), latest cycle `cycle_01_23-06_summary.md` mtime 23:52 EEST. **NO DEFER** (both inside 3h window; 17 min old).

**CLI (read-only, this run):**
- `active-signals` crypto = **9 B-tier** (ZEC scalp waiting_for_entry; ZEC swing×3 tp_hit; ZEC intraday tp_hit; NEAR intraday triggered; BAND swing×2 tp_hit; C/USD scalp tp_hit; XLM swing tp_hit).
- `active-signals` stocks = **20 signals** (XOM A-tier intraday long triggered score 80+; XLV B-tier long triggered; AAL B-tier long tp_hit; JPM B-tier long triggered; LLY B-tier long triggered; PLTR B-tier short triggered; META B-tier short triggered; GOOGL B-tier short triggered; plus C-tier mix including SMCI C-tier long triggered [LEGAL RISK]).
- `signal-stats` crypto (week, A/B): n=69, triggered winrate **27.5%**, PF **1.74**, totalR **+14R**. Observation: winrate low but PF positive — larger winners carrying.
- `signal-stats` stocks (week, A/B): n=142, triggered winrate **15.5%**, PF **0.46**, totalR **−29R**. All tiers (A/B/C) flagged below PF 0.8 by system.
- `detect_untracked_legacy_alerts` = **0** (clean).
- Post-track result: checked=321 updated=20 **stopped=3** expired=0 not_triggered=4.

**External (WebSearch/WebFetch, verified):** US close data (CNBC/TheStreet search snippet); BTC $63,564 + ETH $1,689 at 9:30 ET (Fortune WebFetch confirmed); chip-led rally details (CNBC). Full citations §13.

---

## 3. Scheduler / Data Freshness

- **No defer.** scheduler.log 23:52 EEST (~17 min), latest cycle `cycle_01_23-06` 23:52 EEST (~17 min). Both well inside 3h window.
- Crypto scalp + intraday: **FRESH** (~19–47 min). Stocks intraday: **FRESH** (~19 min, but market-closed planning-only).
- Crypto swing: ~20h → **STALE** (excluded from swing final verdict; context only).
- Stocks swing/invest: ~20h → **STALE** (excluded; swing under 48h audit cap).
- Catalyst JSONL: current (accumulating throughout session; latest cycle added 500 events).

---

## 4. What Changed vs Previous Review (`..._1624.md` pre-US-open, 16:24 EEST, ~7.75h ago)

| Item | At 16:24 (pre-open) | Now (post-close) | Delta |
|------|---------------------|------------------|-------|
| US stocks | Gapping UP pre-market; internal scan stale/risk_off vs live gap-up | **Closed: S&P +0.30%, Nasdaq +0.86%, Dow −0.16%; SOXX +7%, MU +10%, MRVL +14%** | Gap-up held; chip recovery confirmed; breadth selective |
| Stock short list | META A-tier flagged SHORT-WATCH only after RTH failed-bounce; "don't chase gap" | Market went UP; META/PLTR/GOOGL shorts triggered INTO rising tape; stopped=3 | **Pre-open call vindicated; trap confirmed; shorts failed** |
| ZEC | Two B-tier longs TRIGGERED; catalyst net-negative/unresolved; "hold to SL, don't add" | ZEC swing×3 + intraday tp_hit; scalp waiting_for_entry; Ironwood catalyst gaining clarity | **ZEC runners working; catalyst improving from "unresolvable" toward "credible roadmap"** |
| LLY | Best catalyst long (obesity/PBM); wait RTH pullback | B-tier still triggered; ACHIEVE-3 trial (Seeking Alpha June 8) reinforces catalyst | LLY catalyst fresh and reinforced |
| AAPL | WWDC resolved (Siri+Gemini); sell-the-news fade; MANUAL REVIEW | Not in active signals this cycle | Carry-forward: post-event settled; monitor next session |
| BTC | ~$62.97k (+1.74%) range; ETH-led relief | BTC ~$63.5k at US open, held range all session; alts RS broadening | Marginally firmer; range intact; alt momentum persisting |
| ETF outflows | 3rd consecutive outflow week, ~$4.21B over 3 weeks; structural cap | **Confirmed: −4,889 BTC (−$311.86M) June 8; −8,426 ETH/day** | Unchanged; persistent institutional selling |
| Catalyst mapping | 73% unmapped (390/1,442); weak | 1,068 events today, 3 baskets (same); pattern unchanged | Weak mapping persists |
| Geopolitical | Mideast tensions flagged as cap on gap-up | Iran/Israel tensions remain ("threatening fragile ceasefire"); BTC +5% on de-escalation hopes simultaneously | Dual-signal: tension + hope; net neutral; oil rose |
| Stocks signal PF | Stocks A/B PF 0.46 flagged | **Confirmed: A-tier PF 0.25 (n=22); B-tier PF 0.52 (n=120); totalR −29R** | Widening; critical TODO |
| Untracked alerts | 0 clean | **0 clean** | Unchanged |

**Net thesis change:** "Gap-up risk / RTH confirmation required" → **"Gap held; chip rally confirmed; desk's short list was wrong direction today; overnight = mild constructive in crypto range; no new stock entries tonight; focus on Asia setup and stock strategy audit."**

---

## 5. Catalyst Coverage

- **Total catalyst_events today: 1,068 unique. Baskets: 3.**
- Mapped/unmapped for this exact run: not recomputed from JSONL. Prior run (16:24) showed 73% unmapped (390/1,442). Pattern unchanged: **catalyst mapping likely weak — use as context, not final decision.**
- **Notable mapped catalysts:**
  - **ZEC/USDT** [catalyst]: "Zcash rebounds 80% as developers propose Ironwood upgrade after Orchard bug" (CryptoBriefing) + Decrypt explainer. Verified: news_mention, importance 2.85.
  - **BTC/USDT** [regulatory_sector_headline]: ETF outflows confirmed (t.me/lookonchain + CryptoBriefing + bitcoinfoundation.org): −4,889 BTC June 8, 3rd consecutive weekly outflow, ~$4.21B/3wks. IBIT single-day −$214M.
  - **ETH/USDT** [regulatory_sector_headline]: ETF outflows −8,426 ETH/day, −97,515 ETH 7d.
  - **UNH** [legal_risk ×3]: DOJ fraud probe + antitrust probe + shares −16%. (QuiverQuant, Yahoo Finance, Phemex Academy).
  - **SMCI** [legal_risk]: Form 8-K (FY2026) — indictment of 3 individuals re export-control violation conspiracy (SEC EDGAR, ~Mar 1).
  - **ENA/USDT**: $4.62M daily fees; Coinbase Ventures scoops ENA (CryptoBriefing).
  - **NEAR/USDT**: "3 Altcoins to Watch" (BeInCrypto); AI narrative heat 56/100.
  - **LLY**: ACHIEVE-3 trial boosts Foundayo outlook (Seeking Alpha, June 8).
  - **BTC/USDT** [geopolitical]: "Trump urges Netanyahu against retaliation as Bitcoin jumps 5% on de-escalation hopes" (CryptoBriefing).
  - **(basket)** [exploit_hack]: White hats rescue $500K in NFTs after Flooring exploit (Cointelegraph).
- _Reddit social sources (CryptoCurrency, Bitcoin, Ethereum) returning HTTP 403 — social attention context missing (see §14 TODO-REDDIT)._

---

## 6. Market Landscape

### Crypto
BTC range (~$63.5k at US open, recovering from weekend <$60k dip — first sub-$60k since 2024). ETH ~$1,689. Breadth EMA20 **60%** / EMA50 **26.7%** (short-term bounce broad, longer trend not reclaimed). BTC ATR pct 63 (normal vol). Regime: **range/chop (neutral)** — mean reversion or wait for clean breakouts prescribed.

Altcoin momentum: **WLD +13.26%** (best-volume RS leader; dual-exchange; vol 0.5–0.8x, below avg); **BIO +19.42%** (OI +12% confirming trend); **LAYER +27.43%** (extended; OI +60.88%; crowding unknown; negative funding −0.70%); **STG +22.23%; ONDO +10.55%; LUNC +11.13%**. ZEC +7.68–8.68% (catalyst-backed). Weakest: EPIC −31.55%, ATM −21.44%, FIDA −8.40%.

Narratives: AI rising (heat 56, primary NEAR/TAO/RENDER/FET); momentum_breakout (STG/BIO; `wait_pullback`); perps_dex (HYPE; `wait_pullback`). No DePIN/Gaming/L2 heat.

### Stocks (post-close planning)
US session closed. Internal scan label: **risk_off** (VIX 18.92, breadth EMA20 25%, DIA only trending up). Live session delivered **selective constructive** (chip-led rally). Discrepancy between label and session outcome confirms the regime label lags intraday reality for the market's fastest-moving sectors.

Strongest 20d RS sectors: healthcare (XLV +6.17%), semis (SMH +5.36%), tech (XLK +4.72%). Weakest: comms (XLC −5.22%), discretionary (XLY −4.22%). Energy notable on geopolitical oil bid (Iran/Israel).

Stocks swing under audit cap (−12R, 0W/12L). No new stock signals tonight.

### Market Mood / Risk Routing (REQUIRED — PART 4)
- **Crypto mood:** chop / range-constructive — BTC/ETH range, relief bid intact; altcoin RS alive but below-avg vol; no fresh A/B; crowded short funding on majors limits fresh shorts
- **Stocks mood:** closed / day ended selective risk-on (chip-led); next session planning only; internal label risk_off but session outcome was constructive
- **Dominant narrative:** US chip relief rally (MU/MRVL/INTC/NVDA bounce after Friday's −4.2% Nasdaq crash); BTC weekend bottom-test and recovery; ZEC Ironwood upgrade catalyst; persistent BTC/ETH ETF outflows as structural counter-narrative; Iran/Israel dual-signal (tensions + de-escalation hope)
- **Preferred side now:** mild long-lean in crypto on RS leaders (pullback hold only; no chasing); stocks = no new entries overnight; both sides require confirmation
- **Best long candidate:** crypto — **WLD/USDT** (best RS leader, dual-exchange, pullback to 0.52–0.53); **ZEC/USDT** (catalyst, runners active); stocks (next session) — **LLY** (ACHIEVE-3 catalyst fresh, healthcare RS leader) on pullback hold
- **Best short candidate:** crypto — **OPG/USDT short-watch** (downtrend, RS −7.45% vs BTC, failed-bounce retest at 0.157–0.159; watchlist only); stocks (next session) — **META short-watch** (comms weakest RS, B-tier triggered) after RTH failed-bounce only
- **Best catalyst-backed candidate:** **ZEC/USDT** (Ironwood upgrade, multiple TPs hitting); **LLY** (ACHIEVE-3, obesity portfolio)
- **What to avoid:** LAYER (>2 ATR from EMA20, crowding unknown, negative funding); all stock shorts at next open without RTH confirmation; SMCI/UNH longs (legal risk); stocks swing entries (audit cap); chasing any alt after 20%+ single-day moves
- **What would change the view:** BTC reclaiming >$64k with EMA50 breadth >35% → upgrade crypto to mild risk-on, RS-leader longs more confident; BTC losing $61k → stand down longs, shorts on failed retests only; stocks next open: if semis consolidate + broad breadth → risk-on; if gap-fade or Mideast escalation → desk's short list re-validates

---

## 7. Candidate Deep Dives (≤ 5)

### Candidate 1 — ZEC/USDT (crypto, B-tier, multiple modes, tp_hits) — CATALYST RUNNER, MANAGE NOT CHASE

- **Status (post-close):** Most active crypto cluster today. Active: ZEC swing×3 (tp_hit), ZEC intraday (tp_hit), ZEC scalp (waiting_for_entry). Multiple TP events across modes throughout the session.
- **Catalyst (VERIFIED):** "Zcash rebounds 80% as developers propose Ironwood upgrade after Orchard bug" (CryptoBriefing, June 8) + Decrypt explainer. Ironwood upgrade is a credible developer response shifting the narrative from "bug unresolved" toward "recovery roadmap." Residual: Orchard exploit cannot be cryptographically ruled out (pre-patch window); Arthur Hayes exit remains supply overhang.
- **Derivatives:** Negative funding −0.000693 (intraday) / −0.000286 (mexc fallback). Short-crowded structure = shorts paying longs. Crowding unknown per scalp report. OI +0.66% (fresh positioning trend; slight but confirming).
- **Price/chase check:** ZEC ~$454–458 at report time. ATR ~$11.4–11.7. Resistance $460.07. Support $414.91. Price is approaching resistance. Scalp entry zone: $446.70–451.82 (pullback zone). Buying near $458 = within 0.2 ATR of resistance = **not the time to add.** Existing runners with TPs being hit = correct outcome.
- **Chase risk:** YES at current price near resistance. Pullback to $446–452 = entry zone for fresh scalp. Intraday zone: $450.69–455.97.
- **Mood alignment:** Yes — catalyst-backed, range/constructive regime. Best verified crypto candidate on the desk.
- **Invalidation for existing:** 1h close below $440–444 (mode-dependent SL).
- **Verdict:** **MANAGE runners to SL. Do NOT add above $458 (near resistance). Fresh scalp entry only on pullback to $446–452 overnight. Catalyst is the desk's strongest crypto support right now.**

---

### Candidate 2 — XOM (stocks, A-tier, intraday long, TRIGGERED) — ENERGY + GEOPOLITICAL HEDGE

- **Status:** Only A-tier active stock signal. XOM shows three rows (A-tier, B-tier, C-tier intraday longs, all triggered). Session closed constructively for energy on oil price rise (Mideast tensions).
- **Catalyst check (internal first):** No direct XOM news in internal reports. External: "oil prices rose after Iran and Israel exchanged strikes, threatening fragile Middle East ceasefire" (TheStreet June 8 search). Oil price rise = XOM tailwind.
- **Legal/headline risk:** None flagged for XOM in catalyst_events or reports.
- **Sector context:** Energy (XLE C-tier triggered). Energy was weakest RS sector over 20d (XLE 20d return data not highlighted as strong), but intraday geopolitical oil bid supports XOM specifically. Stocks report has XLV, XOM, and XLE flagged in active signals.
- **Mood alignment:** A-tier long in a risk_off regime = system scored as exceptional. Day ended constructively. XOM is a hedge (energy/oil) against the same Mideast tensions that create tail risk.
- **Post-close posture:** Stocks closed. XOM position managed to SL (~$14x+ per truncated data). No new entry tonight (stock not tradeable until RTH open).
- **Verdict:** **HOLD XOM to SL. Oil geopolitical bid thesis intact. Monitor oil overnight. No new entry until next RTH open pullback hold.**

---

### Candidate 3 — WLD/USDT (crypto, C-tier, best RS leader) — OVERNIGHT ASIA LONG-WATCH

- **Status:** Top crypto RS leader. Scalp score 60.2 / intraday score 57.4 (both C-tier). No active signal — WATCHLIST ONLY.
- **Evidence:** 24h return +13.26–14.55%; RS vs BTC +11–12.31%; vol 0.5–0.81x (below avg but improving). Trend: uptrend. Setup quality 71.9/100 (highest on desk). Dual-exchange Binance+MEXC (confirmation 84.2%). Resistance 0.5789; support 0.4531. Current price ~0.538–0.544.
- **Derivatives:** Price up + OI down → **short covering** (not fresh positioning). Funding +0.0001 (longs paying slightly). Crowding: normal. Long/short 1.667. This is the weaker continuation signal (shorts exiting, not new longs adding).
- **Catalyst:** No verified WLD-specific catalyst. Narrative: AI adjacent (World ID identity project); AI basket rising (heat 56, attention 100). Crowd attention stage: unknown, momentum 91.6, crowding 18 (not crowded yet).
- **Chase risk:** +13–14% move in 24h without volume confirmation. Do NOT chase at 0.54+. Entry plan: pullback to 0.52–0.53 zone with volume confirmation (vol ≥ 0.8x avg preferred).
- **Overextended:** ATR ~0.024. If EMA20 is around 0.45, price at 0.54 = ~3.8 ATR above EMA20. **Potentially extended. Demand pullback.**
- **Verdict:** **LONG-WATCH overnight. Trigger: pullback hold to 0.52–0.53 with volume. Do NOT chase at 0.54+. Stand down if BTC loses $62k.**

---

### Candidate 4 — META (stocks, B-tier short, TRIGGERED) — REASSESS POST-UP-SESSION

- **Status:** META B-tier intraday short, triggered. Session: Nasdaq +0.86%, tech green. META shorts ran against the tape. Among the 3 stopped signals, META short is a likely candidate.
- **LEGAL/HEADLINE RISK (carry-forward, verified):** FTC "social-network monopoly" antitrust case (appeal + 29 states + DC); Texas WhatsApp false-encryption suit (May 21, 2026). Ongoing structural overhang.
- **Sector:** Communications (XLC) — weakest sector RS 20d (−5.22%). Structurally supportive of the short thesis.
- **Today's outcome:** Market went UP. Comms sector weakest RS but still lifted by the broad tape. META short was directionally wrong on the day. Fundamental short thesis (FTC/Texas) is intact but not near-term catalysts.
- **Post-close verdict:** If META short is still active (not stopped), it is in drawdown. At next open: if market gaps down or META fails a bounce in first 15–30 min RTH → re-validates; if market continues up → cut or let SL work.
- **Mood alignment:** Misaligned with today's session; aligned with structural sector weakness.
- **Verdict:** **SHORT-WATCH for next RTH session only — after failed-bounce (lower-high) in first 15–30 min open. Manage existing position to SL. Do NOT add until RTH confirmation.**

---

### Candidate 5 — UNH (stocks, C-tier long, ACTIVE LEGAL RISK) — AVOID

- **Status:** UNH C-tier intraday long, score 57.49, listed as `waiting_for_entry` in active signals. ← **Contradiction: long signal with active legal risk.**
- **LEGAL/HEADLINE RISK — VERIFIED, THREE SOURCES:**
  - "UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation" (QuiverQuant, in catalyst_events [legal_risk])
  - "DOJ Antitrust Probe Puts Focus On UnitedHealth Valuation And Integrated Model" (Yahoo Finance, in catalyst_events [legal_risk])
  - "UnitedHealth Group (UNH) Stock in 2026: DOJ Probe, Medicare Reset, Key Risks, and How to Trade" (Phemex Academy, in catalyst_events [legal_risk])
- **Verdict: AVOID / MANUAL REVIEW REQUIRED.** UNH long is blocked by active DOJ fraud + antitrust probe with shares already −16%. No long entry warranted until legal resolution. Any waiting_for_entry signal for UNH should be manually cancelled.
- **System gap note (§14):** The C-tier long signal was generated despite the [legal_risk] entry in catalyst_events. The legal flag does not auto-block signal generation. → TODO-LEGAL-RISK-CAP.

---

## 8. Best Candidates Ranked (post-close window)

**No clean actionable new trade this window** — stocks closed; crypto regime = range/chop; no A/B. Per PART 9, naming watch candidates:

1. **Long-watch: ZEC/USDT** — trigger: pullback to $446–452 overnight (scalp entry zone) with BTC holding $62k+. Catalyst-backed (Ironwood). Manage runners to SL ~$440.
2. **Long-watch: WLD/USDT** — trigger: pullback to 0.52–0.53 with vol ≥ 0.8x avg. Best RS leader. C-tier only.
3. **Short-watch: OPG/USDT** — trigger: failed bounce retest at 0.157–0.159 (intraday score 56.4, C-tier). Downtrend; RS −7.45% vs BTC; no catalyst.
4. **Catalyst-watch (next session): LLY** — trigger: RTH pullback hold above support with volume. ACHIEVE-3 catalyst reinforced June 8. Healthcare RS leader.
5. **Short-watch (next session): META** — trigger: RTH failed-bounce / lower-high in first 15–30 min open. Manage existing position.

**Excess (listed with reason):**
- BIO/USDT: momentum_breakout basket primary; +19% 24h; vol 0.14–0.42x (thin); **watchlist only — vol too thin for sizing.**
- NEAR/USDT: B-tier intraday triggered (active signal); AI narrative; score 55–66. **Manage existing NEAR intraday to SL ~$2.07–2.09.**
- ONDO/USDT: C-tier 54.8; RWA basket; short-covering quality; below-avg vol; **watchlist only.**

---

## 9. Avoid / No Trade (this decision window only)

This verdict applies to the overnight-into-Asia window only. It is NOT a command to stop the system. Scanning, tracking, and data collection continue in all moods.

- **AVOID: UNH long** — DOJ fraud + antitrust probe (3 verified sources). Waiting_for_entry signal should be manually reviewed/cancelled. See §7 Candidate 5.
- **AVOID: SMCI long** — SMCI C-tier intraday long is TRIGGERED in active signals despite export-control violation indictment (3 individuals, SEC EDGAR Form 8-K FY2026, [legal_risk] in catalyst_events). AVOID / MANUAL REVIEW REQUIRED.
- **AVOID: LAYER/USDT** — +27.43% 24h; OI +60.88%; crowding unknown; funding −0.70% (negative, shorts may be crowded on both sides); rejected from intraday (>2 ATR from EMA20). Chase risk extreme.
- **AVOID: ALLO/USDT** — momentum_breakout basket flagged `avoid_chase`; rejected from intraday; below threshold.
- **AVOID: EPIC/ATM/FIDA/OPN shorts** — short-squeeze guards in place. System correctly capped to C.
- **AVOID: Stocks swing entries** — under 48h audit cap (−12R, 0W/12L); all A/B demoted to C.
- **AVOID: Stock shorts at next open without RTH confirmation** — today proved the risk; require failed-bounce (15–30 min) before any short sizing.

---

## 10. Main Risks

1. **Stocks signal systematic failure (critical):** All three stock tiers below PF 0.80. A/B combined: PF 0.46, −29R week. A-tier alone: PF 0.25 (reliable n=22). Stopped=3 more today. → §14 TODO-STOCKS-SCORING.

2. **BTC ETF outflows structural headwind:** 3rd consecutive outflow week: −$1.67B weekly, ~$4.21B/3wks. IBIT −$214M single-day. Bernstein notes "boring cycle." Institutional selling is persistent and caps recovery attempts.

3. **BTC weekend sub-$60k test:** BTC went below $60k for the first time since 2024 over the weekend. Even though it recovered to $63.5k, this represents a significant support test. A repeat break below $60k would change the overnight crypto framework dramatically.

4. **Geopolitical tail:** Iran/Israel tensions remain active (TheStreet June 8: "exchanged strikes, threatening fragile ceasefire"). The Mideast narrative is simultaneously a BTC +5% de-escalation hope catalyst AND a potential risk-off escalation risk.

5. **Catalyst mapping weak (persistent):** ~73% unmapped events (prior run pattern). Catalyst layer is context-quality only, not decision-grade.

6. **Legal risk in active signals — system gap:** SMCI and UNH both showing as triggered/waiting in active-signals despite [legal_risk] flags in catalyst_events. Legal flag not auto-blocking signal generation. → §14 TODO-LEGAL-RISK-CAP.

7. **Social attention blind (Reddit 403):** CryptoCurrency/Bitcoin/Ethereum subreddits all blocked. Social context thin. KOL placeholder account not replaced.

---

## 11. Action Plan — Next 4 Hours (00:09 → ~04:00 EEST, overnight into Asia)

1. **ZEC runners:** Manage existing swing/intraday to SL (~$440–444 mode-dependent). Fresh ZEC scalp entry ONLY on pullback to $446–452 overnight. Do NOT add above $458 (near resistance $460.07).
2. **NEAR intraday:** Active trigger. Monitor BTC regime. If BTC loses $62k, evaluate NEAR SL tightening.
3. **WLD watch:** Alert at 0.52–0.53 pullback. Do not chase at ~0.54.
4. **BTC regime monitor:** $62k is the key overnight floor. Hold → mild constructive, RS-leader longs valid. Loss → stand down long bias.
5. **Stocks — no new entries overnight.** XOM A-tier long managed to SL. META short managed to SL (evaluate at next open). LLY in position per SL.
6. **SMCI + UNH:** No new long entries. Existing triggered signals should be flagged for manual review/cancellation at next human session.
7. **Asia setup brief (for 04:30 slot):** Watch altcoin breadth EMA20 (currently 60%) — if it drops below 50% by Asia open, rotate to defensive. If BTC holds and consolidates $62–64k range, RS leaders (WLD, ZEC, BIO, ONDO) can continue momentum into Asia flows.

---

## 12. Final Verdict per Mode

| Mode | Status | Verdict |
|------|--------|---------|
| Crypto scalp | No A/B; ZEC scalp waiting_for_entry | Watch ZEC pullback $446–452; WLD pullback 0.52–0.53. No chase. |
| Crypto intraday | NEAR triggered (manage to SL $2.07–2.09); ZEC runners (manage to SL $440–444) | No new intraday entry tonight — regime chop, no A/B. Manage runners only. |
| Crypto swing | ZEC swing multiple TP hits (working); BAND×2 TP; XLM TP | ZEC swing best performer. Manage to SL. No new swing entries in range/chop. |
| Stocks intraday | Closed. XOM A-tier long triggered; LLY B-tier triggered; META/PLTR/GOOGL B-tier shorts in drawdown | Planning only. No new entries until RTH. Evaluate shorts at open (failed-bounce required). |
| Stocks swing | **CAPPED — under 48h audit (−12R, 0W/12L)** | No swing entries. All A/B demoted to C. Audit completion required before resuming. |
| Stocks invest | STALE data (>20h) | No invest decisions. Carry-forward LLY from prior context only. |

---

## 13. Sources

- [TheStreet — Stock Market Today June 8 2026: Nasdaq Russell 2000 small comeback](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-08-2026) — June 8, 2026; HTTP 403 on WebFetch; data confirmed via search snippet. `verification: single_source`
- [Yahoo Finance — Bitcoin and Ethereum prices Monday June 8, 2026 (moving up after below $60k)](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-june-8-2026-moving-up-after-bitcoin-prices-fell-below-60000-131559331.html) — June 8, 2026; BTC $63,515–$63,564, ETH $1,689 at 8:50–9:30 ET. `verification: primary_source`
- [Fortune — Current price of Bitcoin June 8, 2026](https://fortune.com/article/price-of-bitcoin-06-08-2026/) — June 8, 2026; BTC $63,563.66 at 9:30 ET, ETH $1,688.58; **verified via WebFetch.** `verification: primary_source`
- [CNBC — S&P 500 closes higher as chips stage comeback (June 7/8)](https://www.cnbc.com/2026/06/07/stock-market-today-live-updates.html) — S&P 500 +0.30% at 7,405.73; Nasdaq +0.86% at 25,929.66; Dow −0.16% at 50,786.01; SOXX +7%; MU +10%, MRVL +14%, INTC +12%; Friday Nasdaq −4.2%. `verification: primary_source`
- [CNBC — Nasdaq falls 4%, worst day since April 2025 (June 4 2026)](https://www.cnbc.com/2026/06/04/stock-market-today-live-updates.html) — Context on Friday selloff. `verification: primary_source`
- CryptoBriefing — "Zcash rebounds 80% as developers propose Ironwood upgrade after Orchard bug" — June 8, 2026; from internal reports catalyst section. `verification: single_source`
- t.me/lookonchain — BTC ETF 1D NetFlow −4,889 BTC (−$311.86M); ETH ETF −8,426 ETH/day; 7D: −26,077 BTC (−$1.66B) / −97,515 ETH (−$164.31M) — June 8, 2026; from internal news_items. `verification: single_source`
- QuiverQuant — "UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation" — from internal catalyst_events [legal_risk]. `verification: single_source`
- Yahoo Finance — "DOJ Antitrust Probe Puts Focus On UnitedHealth Valuation And Integrated Model" — from internal catalyst_events [legal_risk]. `verification: single_source`
- SEC EDGAR (internal catalyst) — SMCI Form 8-K FY2026: indictment of 3 individuals re export-control violation conspiracy, filed ~Mar 1. `verification: primary_source`
- Seeking Alpha — "Eli Lilly stock extends rally as ACHIEVE-3 trial boosts Foundayo outlook" — June 8, 2026; from stocks intraday report §4. `verification: single_source`
- CryptoBriefing — "BlackRock's Bitcoin ETF sheds $214M in single-day outflow as institutional profit-taking accelerates" — from catalyst_events. `verification: single_source`
- The Block (via internal) — "Bernstein says bitcoin's 'boring cycle' doesn't undermine store-of-value thesis despite $2.6B ETF outflows in 2026" — from catalyst_events. `verification: single_source`
- CryptoBriefing — "Trump urges Netanyahu against retaliation as Bitcoin jumps 5% on de-escalation hopes" — June 8, 2026; from internal macro headlines. `verification: single_source`

---

## 14. Fix Requests / TODO

### TODO-STOCKS-SCORING
- **issue:** Stocks A/B signal performance systematically failing: A-tier PF 0.25 (n=22, reliable); B-tier PF 0.52 (n=120, reliable); C-tier PF 0.49 (n=213, reliable). All three tiers below PF 0.80. Total A/B week totalR = −29R. Stocks swing already under 48h cap (−12R, 0W/12L). Today added ≥3 more stops. This is not a one-day anomaly — the pattern is persistent across multiple review cycles.
- **evidence:** `data/reports/stocks/intraday/2026-06-08_20-50_stocks_intraday_report.md` §Recent Signal Performance; `cycle_01_23-06_summary.md` step 12 signal-stats output; stocks swing report header (−12R, 0W/12L audit cap).
- **suggested manual fix:** Manual deep-dive session on stocks scoring: (1) Is the regime filter (risk_off) correctly blocking inappropriate longs, or is it generating too many short signals that get timed wrongly (post-gap)? (2) Is the intraday stocks mode generating signals in high-VIX range regimes that should be filtered? (3) Review entry timing vs pre-market gap behavior. (4) Consider adding a "gap-filter" — no new signals at the open if pre-market has gapped >1% in opposite direction.
- **priority:** high
- **first observed:** 2026-06-09 00:09 EEST (pattern escalating; visible in multiple prior reviews; today confirmed critical with ≥3 additional stops)

### TODO-LEGAL-RISK-CAP
- **issue:** UNH (waiting_for_entry) and SMCI (triggered) are listed as active long signals in `active-signals` despite having verified [legal_risk] entries in `catalyst_events.jsonl`. The legal_risk classification in the catalyst layer does not automatically cap or block signal generation. Human review required to manually cancel these entries.
- **evidence:** `active-signals --asset-class stocks` output shows SMCI C-tier long triggered and UNH C-tier long waiting_for_entry; `catalyst_events` contains [legal_risk] tags for both symbols (SMCI: export-control indictment; UNH: DOJ fraud + antitrust).
- **suggested manual fix:** Implement a `legal_risk_block` scoring modifier: if a symbol has a [legal_risk] catalyst_event with importance above threshold (e.g., >0.5), cap the signal tier to `rejected` or at minimum annotate with a `legal_block` flag visible in active-signals output. Immediate action: manually cancel/reject UNH and SMCI active signals in this session.
- **priority:** high
- **first observed:** 2026-06-09 00:09 EEST (UNH legal risk first appeared in prior June 2026 reviews; SMCI indictment from ~March 2026)

### TODO-REDDIT-SOCIAL-BLOCKED
- **issue:** Reddit social sources (CryptoCurrency, Bitcoin, Ethereum) returning HTTP 403 Blocked across multiple consecutive cycles. `social_attention: missing` in every recent crypto report. KOL watchlist still contains placeholder account.
- **evidence:** `cycle_01_23-06_summary.md` steps 2 and 3 log output: multiple `WARNING Failed social source Reddit CryptoCurrency/Bitcoin/Ethereum: 403 Client Error`.
- **suggested manual fix:** (1) Reddit public JSON feeds are restricted; investigate OAuth-based Reddit API or switch to alternative crowd source (LunarCrush free tier, Santiment, or leveraging Telegram channel data already being collected). (2) Replace KOL watchlist placeholder with ≥3 verified crypto KOL accounts (e.g., on-chain analysts, Telegram channel operators).
- **priority:** medium
- **first observed:** 2026-06-09 00:09 EEST (recurring across many runs)

### TODO-CATALYST-MAPPING-WEAK
- **issue:** Catalyst symbol mapping persistently below 30% (prior run: 390/1,442 = 27%). The ~73% unmapped volume consists of generic finance/listicle noise and backward-looking corporate announcements. This limits the utility of the catalyst layer for per-symbol decisions and forces Opus to use the layer as "context only."
- **evidence:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-08_1624.md` §5: 73.0% unmapped; current run: 1,068 events/3 baskets with same 3 baskets as prior run; pattern unchanged across consecutive cycles.
- **suggested manual fix:** (1) Tighten symbol resolver to exclude generic finance/macro headlines not linked to specific crypto/stock symbols in the universe. (2) Improve deduplication (duplicate Coinbase anniversary row noted in prior review). (3) Add basket-basket: if mapped% <40%, emit basket-only guidance and suppress per-symbol catalyst scoring from unmapped events.
- **priority:** medium
- **first observed:** 2026-06-09 00:09 EEST (pattern visible since at least June 5 reviews)
