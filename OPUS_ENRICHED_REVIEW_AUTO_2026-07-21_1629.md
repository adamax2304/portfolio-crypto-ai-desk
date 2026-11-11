# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:29 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review (16:20 EEST)** — final read ~10 min before/at the US cash open (09:30 ET = 16:30 EEST). Advisory only — no auto-trade, no scoring/threshold changes.
Reports fresh: intraday (15:01 EEST, ~1h27m), scalp (14:54, ~1h35m), stocks intraday (15:26, ~1h03m, generated pre-open). Swing report is **12h old (04:30 EEST generation) — borderline stale**, carried forward only for symbols with corroborating fresher data. The `data/scheduled_runs/2026-07-21_default_schedule/scheduler.log` file itself only contains dry-run CLI-validation entries today (no `cycle_*_summary.md` written yet this date) — **flagged as a data-quality anomaly in §14**, but not a defer trigger per §D since the underlying report/catalyst/CLI data (which the review actually consumes) is fresh and heartbeat is alive (12:37 UTC, ~1h52m ago, no recent warn).
Crypto stays **mixed**: BTC/ETH uptrend, altcoin breadth 73.8% > EMA20, but a **risk-off geopolitical/macro overlay (100/100)** persists — Iran-Bahrain strike on Amazon infra, Strait of Hormuz disruption, oil could exceed $120/bbl — unchanged in severity since the 11:39 review. Stocks regime is explicitly **risk_off** (VIX 17.72, 0% breadth > EMA20, QQQ -6.02% 20d) and the cash session is **about to open right now** — every stock idea on the board is still C-tier/planning as of the last report snapshot (15:26 EEST); treat NVDA and the semis/tech short basket as **needing first 15-30min RTH confirmation**, not a pre-open trade. Best long: **VIRTUAL/USDT** (tp2_hit, managed, no fresh catalyst but not extended). Best catalyst: **ADA/USDT** (Cardano hard-fork catalyst genuine but now aging ~22-26h — borderline, not "fresh" anymore; swing leg hit **tp3** since the last review). Best short-watch: **NVDA** (unchanged, pre-RTH). Avoid: **UNH** (active DOJ criminal-probe/legal risk, never a clean actionable regardless of technical setup) and **BONK/USDT** (exploit drainer still active). **HEMI/USDT got stopped in all three modes (scalp/intraday/swing) since the last review** — validates the chase-risk warning issued at 11:39 and 04:40. The untracked-alert bug (signal_id reuse) fired **3 more times** this cycle (VIRTUAL ×2, ADA ×1) — 5 total today — logged to §14, not fixed here.

## 2. Data Used

- Reports: intraday (15:01 EEST, fresh), scalp (14:54, fresh), stocks intraday (15:26, fresh, pre-open snapshot), swing (04:30, **12h — borderline stale**, carried forward selectively)
- Stocks swing/invest: last dated 2026-07-02 (19 days) — excluded, deprecated framework per project history
- Catalyst layer: `data/catalysts/2026-07-21/` (catalyst_cycle_12-05.md latest, catalyst_events.jsonl, narrative_baskets.jsonl)
- LLM packets: `llm_analysis_packet.md` (15:03), `llm_stocks_packet.md` (15:28)
- CLI: `active-signals` (crypto ×27, stocks ×50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-07-21`
- Direct SQL against `proposed_signals` (recent status/tier/entry data — CLI table columns were too narrow to read symbol names reliably) and `news_items` (verified VIRTUAL/ADA/INJ catalyst freshness directly, not taken from report labels)
- Direct computation of today's catalyst mapping ratio from `catalyst_events.jsonl` (2,475 events)
- Heartbeat: `data/autostart/heartbeat_state.json` — last OK 2026-07-21T12:37:35Z (~1h52m ago), last warn 2026-07-20T12:57Z (>24h ago, stale warn)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-21_1139.md` (11:30 Europe/pre-US slot)
- **External web research unavailable this run** (not invoked — internal `news_items`/report data was fresh, internally consistent, and sufficient for every candidate; no thesis depended on unverified external claims)

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-07-21_default_schedule/scheduler.log`: mtime 16:09 EEST (~20 min old) but content-inspection shows **only two dry-run CLI-validation passes today (01:27 and 16:07), no real cycle execution, no `cycle_*_summary.md` file present in this date's folder** — the most recent real `cycle_*_summary.md` on disk is from **yesterday's** folder (`2026-07-20_default_schedule/cycle_07_14-45_summary.md`, ~25.5h old). This is unusual and flagged in §14.
- Despite that, the actual report/catalyst/CLI outputs the review consumes (§2) are all fresh (≤1h35m except swing at 12h) — **no defer triggered**, since §D's rule keys off report/catalyst freshness reaching the review, and those are current.
- Heartbeat: OK 2026-07-21T12:37:35Z (~1h52m ago); last warn was >24h ago — monitor alive, no active alarm.
- Swing report (04:30 generation): **borderline stale (~12h)** — used only for context (HEMI/LA chase-risk lesson, already validated by live stops), not as a fresh-idea source.
- Stocks swing/invest: **stale (19 days)**, excluded — deprecated framework, consistent with prior reviews.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-21 16:29 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["report_stale", "scheduler_stale"],
      "data_missing": ["real cycle_*_summary.md for 2026-07-21 (only dry-run validation entries found)", "stocks swing/invest fresh data (deprecated, excluded)", "TradingView/chart MCP not loaded"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log today contains only DRY RUN entries at 01:27 and 16:07, no cycle_XX_summary.md written for 2026-07-21", "most recent real cycle summary is 2026-07-20 14:45 (~25.5h old)", "actual reports consumed (intraday/scalp/stocks-intraday) are all <=1h35m fresh", "heartbeat OK 12:37 UTC"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["risk_on", "risk_off", "mixed", "longs_preferred", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 73.8% breadth>EMA20, macro risk 100/100 risk-off (Iran/Bahrain/Hormuz, oil >$120/bbl risk)", "stocks: risk_off, VIX 17.72, breadth 0%>EMA20, QQQ -6.02% 20d downtrend", "US cash open imminent/concurrent with this review (09:30 ET = 16:30 EEST)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "stale_catalyst", "narrative_supported", "catalyst_contradicted"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl today: 2,475 rows, 523 mapped / 1,952 unmapped = 78.9% unmapped", "ADA/USDT: Cardano hard-fork news_items rows now 21.5-26h old (Decrypt 2026-07-20T18:50 UTC, CoinDesk 2026-07-20T14:31 UTC) — aging out of 'fresh' window; also a same-day exploit_hack headline referencing 'Cardano-BNB Bridge' (NIGHT token, 08:30 and 11:30 UTC today) creates a caution flag alongside the bullish catalyst", "INJ/USDT: still the identical 2026-07-19T18:25 UTC single-source item, now ~46h old — confirmed stale again, 3rd consecutive review cycle", "VIRTUAL/USDT: no dedicated news_items row found in last 30h — long is RS-led, not catalyst-backed, consistent with report's own label"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme", "unwind"],
      "data_missing": ["OI% n/a for several mexc-fallback venues"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ERA/USDT: funding -0.0138 (mexc) while +60.4% 24h — crowded shorts, squeeze fuel, but move already extremely extended", "LA/USDT: negative funding across bybit/okx/mexc while +24.2% 24h — same crowded-short/squeeze-fuel pattern; already stopped out once today (07:27 intraday signal)", "HEMI/USDT: stopped in scalp, intraday, AND swing since the 11:39 review — the earlier chase-risk/overextension call played out as a real loss, not just theory", "VIRTUAL/ADA: price+OI up, funding near-neutral, normal crowding — healthier profile"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["entry_late", "overextended", "chase_risk", "clean_retest", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ERA/USDT: +60.4% 24h, today's #1 scored intraday idea (73.9) — fresh entry at current levels is chase risk despite the high score; managing the existing tp2_hit position is different from a new entry", "VIRTUAL: managed band, not extended, tp2_hit", "HEMI/LA: both validated overextended/chase-risk calls via live stops this cycle", "momentum_breakout narrative basket (HEMI primary, seen in the 04:30 swing report) is NOT present in the current 15:01 intraday report's basket list — narrative has cooled/rotated out"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["open_actionable", "entered_unresolved", "no_entry", "closed_win", "closed_loss"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals n=27: majority OPEN actionable managing toward remaining TP legs (tp1/tp2/tp3_hit across VIRTUAL/ADA/ALLO/ERA/KITE/ZAMA/OPN/PENGU), 2 triggered/entered-unresolved (INJ intraday, PROM swing), some CLOSED LOSS this cycle (HEMI x3, LA, BANK x2, ACE, KAITO, JTO, PROM x2 modes)", "ADA/USDT swing leg reached CLOSED WIN TP3 since the last review — thesis fully played out", "stocks active-signals n=50: all C-tier watchlist/review-shadow, market_closed_intraday_planning_only gate active for the whole prior snapshot"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "legal_risk", "repeated_losses", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: active DOJ criminal-probe/Medicare-fraud investigation, multiple corroborating headlines (FierceHealthcare, TipRanks, QuiverQuant) — legal_headline_risk gate already demoted it in production", "BONK: block_requires_operator_review, exploit drainer still selling (unchanged from 11:39)", "AMZN: geopolitical_risk (Bahrain infra strike) — directly relevant to the imminent US open", "GOOGL/TSLA: earnings 2026-07-22 (tomorrow), do_not_chase_warning active on both", "crypto direction=short stats remain anecdotal but consistently bad (n=8, 0% winrate, PF 0.125)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing PF 2.34 avgR 0.36 (n=47) and crypto intraday PF 2.10 avgR 0.34 (n=78) — both working per week signal-stats", "crypto scalp PF 0.98 avgR -0.003 (n=34, kill-switched, mode off) — losing, already handled", "stocks C-tier headline winrate 14.9% (n=187, reliable) — system's own observation, consistent with prior reviews", "stocks A/B sample anecdotal (n=7, 28.6% WR, PF 1.5) — too small to trust"] },
    { "agent": "head_trader", "verdict": "see below", "confidence": 0.6,
      "reason_codes": [], "data_missing": [], "suggested_effect": "advisory_only", "facts_used": [] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "VIRTUAL/USDT", "trigger": "already managed tp2_hit; fresh add only on pullback into 0.6532-0.6564 (intraday band) or 0.6417-0.6465 (swing band), invalidation 0.6492/0.6359", "reason": "RS-leader, not extended, OI+price up, crypto tape still bullish-trend despite macro overlay" },
    "best_short_candidate":    { "symbol": "NVDA", "trigger": "RTH open, first 15-30min candle confirming below ~205, no gap-fill reclaim", "reason": "C-tier score 87.8 short, semiconductors weakest sector (RS -14.7% vs SPY 20d), stocks regime risk_off; still planning-only until RTH confirms" },
    "best_catalyst_candidate": { "symbol": "ADA/USDT", "trigger": "manage existing tp2_hit(intraday)/tp3_hit(swing, CLOSED WIN) positions; fresh add only on retest of 0.1693-0.1704, invalidation 0.1680", "reason": "Cardano hard-fork catalyst is genuine and multi-source but now aging (~22-26h) — treat as borderline, not freshly-actionable; today's swing leg already closed at TP3" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "active DOJ criminal probe / Medicare fraud investigation, multiple corroborating headlines; legal_headline_risk gate already demoted it — never a clean actionable regardless of technical score" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | report_stale, scheduler_stale | advisory_only |
| market_regime | caution | 0.60 | risk_on, risk_off, mixed, longs_preferred, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, stale_catalyst, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, oi_supports, funding_extreme, unwind | advisory_only |
| technical_entry | caution | 0.65 | entry_late, overextended, chase_risk, clean_retest, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.70 | open_actionable, entered_unresolved, no_entry, closed_win, closed_loss | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, legal_risk, repeated_losses, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution (synthesis) | 0.60 | see JSON | advisory_only |

## 4. What Changed vs Previous Review (11:39 EEST slot)

- **VIRTUAL/USDT** — progressed tp1_hit → **tp2_hit** on both intraday and swing legs; thesis intact, unchanged as best long.
- **ADA/USDT** — major progress: swing leg went tp2_hit → **CLOSED WIN at TP3**; intraday leg still tp2_hit. Catalyst freshness has aged from "genuinely fresh ~17h" at 11:39 to **~22-26h now — borderline, no longer clean-fresh**. A new same-day exploit_hack headline ("Cardano-BNB Bridge" / NIGHT token hack, two more corroborating articles at 08:30 and 11:30 UTC today) adds a fresh caution flag alongside the aging bullish catalyst.
- **INJ/USDT** — stale-catalyst mislabel confirmed for a **3rd consecutive cycle**: same 2026-07-19T18:25 UTC single-source item, now ~46h old. Swing leg moved to entry_moved_away; intraday leg is triggered/unresolved. Still demoted from catalyst-watch, holds only as a plain RS-leader long.
- **HEMI/USDT** — was flagged chase-risk/do-not-chase at both 04:40 and 11:39; **now confirmed CLOSED LOSS (stopped) in all three modes — scalp, intraday, AND swing** since the last review. The narrative-basket cooling observed at 11:39 (rotated out of `momentum_breakout`) has fully played out as a real stop-out, not just a theoretical caution.
- **LA/USDT** — similarly flagged squeeze-prone/do-not-chase at 11:39; the 07:27 intraday signal is now CLOSED LOSS (stopped). Today's fresh 15:01 intraday report still surfaces LA as a top idea again (score 73.3) — treat any fresh entry with the same caution, the prior stop-out is direct evidence the chase-risk call was correct.
- **ERA/USDT** — new development: today's #1-scored intraday idea (73.9), position is tp2_hit and progressing well, but the underlying move is now +60.4% over 24h — entering fresh here would be a clear chase, not a repeat of the same mistake as HEMI/LA.
- **NVDA** — short-watch thesis carries forward unchanged: still C-tier (87.8), still planning-only, semis still weakest sector; **the US cash open is now imminent/concurrent with this review — this is the decision point** for whether the thesis gets RTH confirmation.
- **UNH** — newly surfaced this cycle as an explicit AVOID: DOJ criminal-probe/legal risk already gates it in production (score 77, short, tier B→C demoted for `legal_headline_risk` + market-closed).
- **BONK/USDT** — avoid carries forward unchanged; exploit drainer still active, same headlines recurring.
- **Untracked-alert bug** — 3 more instances fired this cycle (VIRTUAL/USDT ×2 at 09:14 and 12:47 UTC, ADA/USDT ×1 at 10:01 UTC), bringing today's total to 5. Same signal_id-reuse pattern as TODO-3 (raised 2026-07-17). See §14.
- **New this cycle**: scheduler.log for today's date folder contains only dry-run validation passes, no real `cycle_*_summary.md` — a data-quality anomaly not previously flagged. See §14.

## 5. Catalyst Coverage

- Total catalyst events in today's file: **2,475** | mapped (non-null symbol): **523** | unmapped: **1,952** → **78.9% unmapped**
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets active (15:01 intraday snapshot): 4 (binance_ecosystem_teaser/BNB, rwa_narrative/ONDO+XLM, perps_dex_narrative/HYPE, ai_narrative/NEAR+RENDER+TAO+FET). Notably **`momentum_breakout` (HEMI) is no longer active** — confirms the cooling/reversal already realized in live stops.
- Top unmapped headlines (symbol resolver missed these):
  1. "MEXC to Delist STM and WULF USDT-M Stock Futures"
  2. "Delisting of UTYAUSDT Perpetual Futures Pair [Jul 23, 2026]"
  3. "IREN raises AI cloud revenue target above $4B on $2.8B in new multi-year contracts"
  4. "SEC alleges Mining Automatic raised $22M in fraudulent crypto mining scheme"
  5. "Hedge funds slash U.S. tech exposure as AI valuation concerns fuel broader risk-off sentiment"

## 6. Market Landscape

**Crypto**: BTC & ETH both in uptrend, 73.8% of tracked symbols above EMA20, volatility normal (ATR percentile 63). Desk style: selective longs, prefer pullbacks on RS. Strongest symbols: ERA (+60.4% 24h, extremely extended), ALLO (+9.9%), LA (+24.2%, already stopped once today), ONDO (+13.1%), CRCLB (+11.3%). Weakest/short candidates remain thin and mostly capped to C-tier by short-squeeze guards — the bullish tape continues refusing most shorts.

**Stocks**: Regime explicitly risk_off. VIX 17.72 (down slightly from 18.65 at 11:39, still elevated-normal), 0% of names above EMA20, QQQ -6.0% 20d downtrend. Sector rotation defensive: energy/healthcare/financials strong, semiconductors/technology weak (SMH -14.7% RS vs SPY, -15.3% 20d). **The 15:26 EEST report snapshot predates the cash open by only a few minutes** — every stock signal on the board (NVDA, XLF, XLK, META, QQQ, LLY, SMH, XLY, DIA, JPM, UNH, NFLX, GOOGL, XLV, PLTR) is still tier-demoted to C via `market_closed_intraday_planning_only`; this gate will lift automatically once fresh RTH data flows in, but **this review's snapshot is pre-open and must not be read as post-open confirmation.**

**Macro overlay (relevant to both)**: Iran-Bahrain strike on Amazon infrastructure and Strait-of-Hormuz disruption persist unchanged in severity from the 11:39 review — macro risk score still 100/100, oil could exceed $120/bbl per Goldman Sachs. This is a live risk-off input **directly into the US cash open** (AMZN specifically named) — treat any post-open bullish reaction in AMZN/broad indices with extra scrutiny given the active geopolitical overlay.

### Market Mood / Risk Routing
- Crypto mood: **mixed** (technical risk-on regime, unchanged macro risk-off overlay)
- Stocks mood: **risk-off, at-the-open** (session opening now — first RTH prints not yet in the data this review consumed)
- Dominant narrative: AI rotation (NEAR/RENDER/TAO/FET, <6h), RWA (ONDO/XLM), perps/DEX (HYPE); Cardano hard-fork (ADA) aging past clean-fresh (~22-26h)
- Preferred side now: **crypto — manage existing RS-leader/catalyst longs, do not chase the extended movers (ERA/LA); stocks — wait for first 15-30min RTH confirmation before acting on any short-watch idea**
- Best long candidate: VIRTUAL/USDT (managed, not chasing)
- Best short candidate: NVDA (planning-only until RTH confirms)
- Best catalyst-backed candidate: ADA/USDT (genuine but aging catalyst; today's swing leg already closed WIN at TP3)
- What to avoid: UNH (active legal/DOJ risk), BONK/USDT (live exploit), fresh chase entries into ERA/LA (both validated overextended this cycle)
- What would change the view: Iran/Hormuz de-escalation (removes crypto macro headwind) or escalation (flips crypto mood fully risk-off); the actual first 15-30min of US RTH price action (confirms or kills the NVDA/semis short thesis and the broader risk-off stock regime read)

## 7. Candidate Deep Dives

### 1. VIRTUAL/USDT (crypto, B-tier, intraday + swing, long) — Best Long
- Score 67.9-69.4 across modes; both legs now **tp2_hit** (progressed from tp1_hit at the 11:39 review). RS vs BTC positive, OI+price up, funding near-neutral (normal crowding).
- Has price already reacted? Yes, partially — managing toward remaining targets, not a fresh chase.
- Chasing? No — not flagged overextended in either report.
- Retest/pullback structure? Yes — desk's own preferred fresh-add zone is 0.6532-0.6564 (intraday) / 0.6417-0.6465 (swing).
- Overextended >2 ATR from EMA20? No.
- Actionable now or after confirmation? Actionable within the defined pullback bands; no market-buy if extended.
- Aligned with market mood? Yes — RS-leader long fits "selective longs, prefer pullbacks."
- Catalyst confirmation? None found in `news_items` for VIRTUAL in the last 30h — this is a pure RS/technical long, not catalyst-backed (consistent with the report's own "no fresh verified catalyst" label, verified directly).
- Invalidation: 1h close beyond 0.6492 (intraday) / 0.6359 (swing).
- TradingView/manual chart check unavailable — using local OHLCV/ATR/EMA fields only.

### 2. ADA/USDT (crypto, B-tier, intraday tp2_hit + swing CLOSED WIN TP3, long) — Best Catalyst (aging)
- Verified directly against `news_items`: Cardano hard-fork catalyst (Decrypt 2026-07-20T18:50 UTC, CoinDesk 2026-07-20T14:31 UTC) is genuinely multi-source but is now **~21.5-26h old** — aging past the cleanest "fresh" window, though still the best catalyst story on the board today.
- Swing leg **CLOSED WIN at TP3** since the 11:39 review — thesis fully played out on that leg. Intraday leg still managing toward remaining target at tp2_hit.
- New same-day risk flag: two fresh headlines today (08:30 and 11:30 UTC, AMBCrypto) about a "Cardano-BNB Bridge" exploit tied to the NIGHT token — this is a bridge-infrastructure hack, not a direct ADA-protocol compromise, but it is enough to keep ADA on the production `block_requires_operator_review` list. Treat as a caution overlay on an otherwise-working catalyst thesis, not a contradiction that invalidates it.
- Actionable now? Managing existing positions; fresh add only on retest of 0.1693-0.1704, invalidation 0.1680.
- Contrast: **INJ/USDT's** catalyst label remains stale for a 3rd straight cycle — the same 2026-07-19T18:25 UTC item, now ~46h old, re-verified directly against `news_items`. INJ holds only as a plain RS-leader long, never a catalyst play, this cycle.

### 3. ERA/USDT (crypto, B-tier, intraday, long, tp2_hit) — Manage Only, Do Not Chase
- Score 73.9, today's #1 intraday idea, but 24h return is **+60.4%** — an extremely large move already happened.
- Has price already reacted? Yes, dramatically — this is a textbook "already priced" move.
- Chasing? Very likely for any fresh entry at current extended levels; no explicit scalp-report rejection line for ERA specifically today, but the same 2-ATR-from-EMA20 chase-risk logic that stopped out HEMI and LA this cycle applies directly.
- Retest structure? Not yet confirmed — no pullback signal this cycle; treat any fresh entry as chase risk until a genuine retest into 0.0921-0.0975 forms.
- Derivatives: negative funding across bybit/mexc while price is up sharply — crowded shorts, squeeze fuel, but also the same setup pattern that already reversed on HEMI/LA today.
- Actionable now? Only for managing the existing tp2_hit position toward remaining targets (TP2 0.1238, TP3 0.1358); **no fresh entry recommended** given the scale of the move and the pattern already validated as a loss twice this cycle (HEMI, LA).
- Catalyst: none verified fresh for ERA specifically.
- Invalidation for the existing position: 1h close beyond 0.0856 (do not use to size a fresh entry at current extended levels).

### 4. UNH (stocks, B-tier raw / C-tier final, intraday, short) — Legal/Headline AVOID
- Score 77.02, short direction, but tier demoted B→C for **both** `legal_headline_risk` (sec_doj) and `market_closed_intraday_planning_only`.
- **LEGAL/HEADLINE RISK**: active DOJ criminal probe into Medicare fraud / Optum Rx reimbursement, corroborated across multiple independent sources — FierceHealthcare ("DOJ's criminal probe into UnitedHealth extends to Optum Rx"), TipRanks ("UnitedHealth Stock Sinks as DOJ Criminal Probe into Medicare Fraud Deepens"), QuiverQuant (×2), Yahoo Finance ("UnitedHealth CFO sends stark warning after earnings," 2026-07-19).
- Per §I: this candidate's final verdict is **AVOID / MANUAL REVIEW REQUIRED**, never a clean actionable, regardless of the technical short setup's score.
- Has price already reacted? Partially — prior headline-driven declines already cited in the news feed; a legal-driven short thesis into an active DOJ probe carries binary/event risk beyond normal technical management.
- Actionable now? No, on legal-risk grounds alone, independent of the market-closed gate.
- Would entry now be late? N/A — this is an avoid, not a timing question.

### 5. NVDA (stocks, C-tier, intraday, short) — Best Stock Short-Watch (planning only, decision point NOW)
- Score 87.8, but the 15:26 EEST report snapshot is **pre-open** — not actionable per the stocks-intraday hardening rule (C-tier never actionable) and the report's own "MARKET CLOSED — planning/watchlist only" banner.
- Sector context: semiconductors is the weakest sector (RS -14.7% vs SPY 20d, -15.3% 20d absolute) — directly supports the short thesis.
- Has price already reacted? Pre-market AI-stock headlines circulating (IREN AI-cloud deal, Apple-vs-Nvidia "biggest company" pieces) — a gap reaction at the open is plausible in either direction.
- Chasing? Cannot assess pre-open; do not chase a pre-market gap without RTH confirmation.
- **This review's timing IS the decision point** — the US cash open (09:30 ET = 16:30 EEST) is concurrent with or immediately after this review. The correct action is to wait for the first 15-30min RTH candle, not act on the pre-open score alone.
- Actionable trigger: first 15-30min RTH candle confirming below ~205 without a gap-fill reclaim.
- Legal/headline risk: none specific to NVDA found this cycle beyond normal AI-sector chatter.
- TradingView/manual chart check unavailable — using local OHLCV/sector fields only.

_No excess candidates beyond these 5 — GOOGL and TSLA (both C-tier, earnings 2026-07-22 tomorrow, `do_not_chase_warning` active) were considered but excluded from deep-dive since they are pure "wait for earnings to clear" holds; HEMI/LA are covered via §4 (validated chase-risk lesson) rather than repeated as separate deep dives; BONK is covered as an avoid item in §9._

## 8. Best Candidates Ranked

1. **Long (manage): VIRTUAL/USDT** — hold the existing tp2_hit position; add only on a fresh pullback into 0.6532-0.6564 (intraday)/0.6417-0.6465 (swing), invalidation 0.6492/0.6359.
2. **Catalyst (manage): ADA/USDT** — swing leg already CLOSED WIN TP3; manage intraday tp2_hit position; fresh add only on retest of 0.1693-0.1704, invalidation 0.1680; catalyst genuine but aging (~22-26h), no longer clean-fresh.
3. **Short-watch: NVDA (+ correlated SMH/XLK basket)** — trigger: first 15-30min RTH candle confirming below ~205 without a gap-fill reclaim; this is the live decision point given the slot timing.
4. **Manage only, no fresh entry: ERA/USDT** — +60.4% 24h already happened; manage the existing tp2_hit position, wait for a genuine retest into 0.0921-0.0975 before considering a fresh add.
5. **Avoid (legal risk), not an entry: UNH** — DOJ criminal-probe risk overrides the technical short score; manual review required if ever reconsidered.

## 9. Avoid / No Trade

_(this decision window only — never a command to stop the system)_

- **UNH** — active DOJ criminal-probe/Medicare-fraud investigation, multi-source corroborated; never a clean actionable regardless of score.
- **BONK/USDT** — active exploit drainer still distributing stolen funds; operator-review flag live.
- **ERA/USDT, HEMI/USDT, LA/USDT (fresh entries)** — all overextended/chase-risk; HEMI and LA are now confirmed losses this cycle (stopped in all modes attempted), ERA carries the identical pattern (+60.4% 24h, crowded-short funding squeeze setup).
- **INJ/USDT (as a catalyst play)** — stale-catalyst label confirmed stale for a 3rd consecutive cycle; holds only as a plain RS-leader long.
- **GOOGL, TSLA (stocks)** — earnings tomorrow (2026-07-22), `do_not_chase_warning` active on both.
- **Crypto shorts generally** — direction=short stats remain anecdotal but consistently bad (n=8, 0% winrate, PF 0.125); bullish tape caps most short setups to C-tier via squeeze guards anyway.
- **Stocks C-tier intraday broadly, and any stock idea acted on before RTH confirms** — headline winrate 14.9% (n=187, reliable); the entire board is pre-open planning data as of this review's snapshot.

## 10. Main Risks

- **Geopolitical**: Iran-Bahrain strike on Amazon infra + Strait of Hormuz disruption — macro risk 100/100, unchanged severity since 11:39. This is a live input into the US cash open itself (AMZN directly named).
- **Gap/stale-data risk (this slot specifically)**: the stocks report snapshot (15:26 EEST) predates the cash open by minutes — any pre-market gap will not be reflected in the C-tier scores this review cites. Do not treat NVDA/other short-watch levels as post-open-confirmed.
- **Earnings gap risk**: GOOGL and TSLA report tomorrow (2026-07-22) — elevated volatility risk for correlated tech/semis names.
- **Squeeze/reversal risk, now with live evidence**: HEMI and LA's crowded-negative-funding pumps both reversed into stop-outs this cycle — ERA carries the identical setup right now (+60.4% 24h, crowded shorts across venues).
- **Catalyst mapping weak (78.9% unmapped)** — reduces confidence in catalyst-driven scoring; treat catalyst tags as directional color, not confirmation.
- **Legal risk live on UNH** — DOJ criminal probe; treat as a hard avoid, not a manageable technical short.
- **Known system bug recurring**: untracked watchlist alerts (5 today: INJ, ADA ×2, VIRTUAL ×2) fired without a backing proposed_signal — won't contribute to PF/winrate tracking.
- **Scheduler data-quality anomaly (new this cycle)**: today's scheduler.log folder contains only dry-run validation passes, no real `cycle_*_summary.md` — worth a human look even though it did not block this review (underlying report data is fresh).

## 11. Action Plan — Next 4 Hours

- Continue managing VIRTUAL/USDT (both legs tp2_hit) and ADA/USDT (intraday tp2_hit; swing already closed win) toward remaining targets; do not add size above the defined pullback/retest bands.
- Do not chase ERA/USDT, HEMI/USDT, or LA/USDT at current/recent extended levels — HEMI and LA already proved this out as losses this cycle.
- **Watch the US cash open directly (concurrent with this review)**: require the first 15-30min RTH candle before treating NVDA or the semis/tech short basket as confirmed; do not act on the pre-open C-tier snapshot.
- Treat UNH as a hard avoid regardless of any technical short signal, given the live DOJ probe.
- Monitor Iran/Hormuz headlines for escalation/de-escalation — either would meaningfully shift the crypto mood read and the broader risk-off tone into the US session.
- No action on GOOGL/TSLA until after their 2026-07-22 earnings clear.
- Scanning, tracking, and monitors continue running unchanged — this review changes nothing in the pipeline.

## 12. Final Verdict per Mode

- **Crypto scalp**: kill-switched (mode off) — consistent with its own negative stats (PF 0.98, avgR -0.003, n=34). No action needed.
- **Crypto intraday**: selective longs on RS-leaders/catalyst-backed only (PF 2.10, avgR 0.34, n=78 — working). Manage VIRTUAL and ADA; do not chase ERA at current extended levels.
- **Crypto swing**: working well (PF 2.34, avgR 0.36, n=47); today's report is 12h carry-forward — HEMI idea from that report is now confirmed stopped, do not revisit at the stale levels.
- **Stocks intraday**: planning/watchlist only as of the last snapshot (pre-open); **re-evaluate immediately at/after 09:30 ET RTH open** — this is the live decision point for this slot.
- **Stocks swing/invest**: no fresh data (framework deprecated, last report 19 days old) — no verdict this cycle.

## 13. Sources

_No new external WebSearch/WebFetch was performed this cycle (per §G, internal records were fresh/consistent/sufficient) — citations below are existing internal `news_items` rows (source + title + published_at; URLs were not selected by the query used, so none is fabricated here):_

- "Cardano Triggers Hard Fork With First Community-Voted Upgrade" — Decrypt, 2026-07-20T18:50 UTC (verifies ADA catalyst, now aging ~22h)
- "Inside Cardano's 'Van Rossum' hard fork, and what it means for users" — CoinDesk, 2026-07-20T14:31 UTC (corroborating, ~26h old)
- "Digging deep into Wanchain's Cardano-BNB Bridge exploit – How $9M NIGHT vanished in hours" — AMBCrypto, 2026-07-21T11:30 UTC (fresh caution flag on ADA)
- "Midnight's 515M NIGHT hack sends token down 32% – Will $0.015 hold?" — AMBCrypto, 2026-07-21T08:30 UTC (same bridge-exploit story, earlier article)
- "Injective highlights SEC registration, Robinhood listing for INJ at Summit" — CryptoBriefing, 2026-07-19T18:25 UTC (confirms INJ catalyst is stale, now ~46h old, 3rd cycle re-verified)
- "UnitedHealth CFO sends stark warning after earnings" — Yahoo Finance, 2026-07-19 (UNH legal/headline context)
- "DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement" — FierceHealthcare (via stocks intraday report, 2026-07-21) — UNH legal risk
- "UnitedHealth Stock (UNH) Sinks as DOJ Criminal Probe into Medicare Fraud Deepens" — TipRanks (via stocks intraday report, 2026-07-21) — UNH legal risk
- All other candidate context sourced from internal reports/CLI listed in §2.

## 14. Fix Requests / TODO

### TODO-untracked-alert-recurrence-0721b
- **issue:** `detect_untracked_legacy_alerts` found 5 untracked crypto watchlist alerts today total (INJ 07:55:44 UTC, ADA 08:29:15 UTC, VIRTUAL 09:14:12 UTC, ADA 10:01:03 UTC, VIRTUAL 12:47:50 UTC) — 3 new since the 11:39 review's count of 2.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-21` output: "5 untracked legacy crypto alert(s)... will NOT contribute to PF / winrate / avgR."
- **suggested manual fix:** continue work on the existing signal_id-reuse bug (raised 2026-07-17, high priority in project memory) — this run's additional INJ/ADA/VIRTUAL instances are new evidence, not a new bug.
- **priority:** high (already tracked, adding evidence, recurrence rate increasing intraday)
- **first observed (this recurrence):** 2026-07-21 16:29 EEST

### TODO-scheduler-log-dry-run-only-0721
- **issue:** `data/scheduled_runs/2026-07-21_default_schedule/scheduler.log` contains only two dry-run/CLI-validation passes today (01:27 and 16:07 EEST) and no real cycle execution entries or `cycle_*_summary.md` files for 2026-07-21. The most recent real cycle summary on disk is from yesterday's folder (`2026-07-20_default_schedule/cycle_07_14-45_summary.md`, ~25.5h old at review time). The actual reports (intraday/scalp/stocks-intraday) ARE being generated and are fresh, so the pipeline that matters is running — but the scheduler.log/cycle-summary bookkeeping for today's date folder appears disconnected from it.
- **evidence:** `tail -40 data/scheduled_runs/2026-07-21_default_schedule/scheduler.log` shows only "=== DRY RUN ===" / "validate <step> OK" lines; `ls data/scheduled_runs/2026-07-21_default_schedule/` shows only `scheduler.log`, no `cycle_*_summary.md` files, vs. 7 such files present in yesterday's folder.
- **suggested manual fix:** a human-driven session should check whether the real (non-dry-run) scheduled cycle process is writing its log/summary to a different location or folder-naming scheme today, or whether it silently stopped writing cycle summaries while still producing reports through some other path. Worth confirming this isn't masking a partial pipeline regression.
- **priority:** medium (did not block this review — underlying report data is fresh — but the freshness-check mechanism described in this routine's own §D relies on files that are not being populated as expected)
- **first observed:** 2026-07-21 16:29 EEST

### TODO-catalyst-freshness-mislabel-0721b
- **issue:** INJ/USDT's `canonical_news_event` "fresh attention/catalyst" label (importance 0.95) continues to trace to the identical single-source 2026-07-19T18:25 UTC item across 3 consecutive review cycles now (04:40, 11:39, and this 16:29 cycle), now ~46h old. Recurring false-fresh signal, not a one-off.
- **evidence:** `SELECT published_at, source, title FROM news_items WHERE detected_symbols_json LIKE '%INJ%' AND published_at > now-48h` still returns exactly the same single row.
- **suggested manual fix:** unchanged from prior reviews — add an explicit "hours since publish" decay/expiry field to the catalyst_news score component so a 46h-old single-source item stops presenting as "fresh."
- **priority:** medium (reviewer manually verifies each cycle, so no trade correctness impact, but affects trust in the automated label; 3rd consecutive cycle without a fix)
- **first observed:** 2026-07-21 04:40 EEST (3rd recurrence this cycle)
