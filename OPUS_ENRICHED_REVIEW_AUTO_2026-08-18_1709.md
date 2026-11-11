# Opus Enriched Review — US Open Reaction Review — Auto Cycle 17:09 EEST

## 1. Executive Summary
**Slot: US open reaction review (nearest fixed slot to 18:30 EEST; dispatched 17:09 EEST, ~39 min after the 16:30 EEST / 13:30 UTC cash open). Advisory only — no auto-trade.** Stocks regime label is "bullish" (VIX 15.69, breadth 100%) but the early tape is diverging: chip/AI names (NVDA, MU, SNDK) are tumbling on rising Treasury yields while GE (industrials) holds an RS-leader long thesis that already banked a TP1 earlier today and re-fired as a fresh A-tier `waiting_for_entry`. Four stocks A/B ideas are live and waiting: **GE long**, **META short**, **AVGO short**, **DIA short** — but META carries an active legal headline (29-state lawsuit reportedly in court **today**, Tuesday) and is downgraded to manual review, not a clean short. Crypto has no fresh A/B this cycle (scalp/intraday/swing all empty) — desk is carrying 9 open B-tier longs (all triggered, no shorts) against a risk-off macro overlay (Iran/Hormuz shipping attack, Ukraine drone strikes, 30Y yield at a 19-year high). Catalyst mapping is weak this run (73.8% unmapped) — treat catalyst layer as context only. One system-integrity item: **4 untracked legacy crypto alerts** today (no matching proposed_signal) — flagged to §14.

## 2. Data Used
- Crypto reports: scalp (16:28 EEST), intraday (16:35 EEST), swing (08:11 EEST, carry-forward — 9h old)
- Stocks: intraday (17:03 EEST, fresh); swing/invest reports stale (2026-07-02, excluded)
- Catalyst layer: `data/catalysts/2026-08-18/` — catalyst_events.jsonl (2444 events today so far), narrative_baskets.jsonl (2 active)
- CLI: `active-signals` (crypto n=45, stocks n=50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-08-18`
- Direct SQLite queries against `db/crypto_ai_desk.sqlite` (`proposed_signals`) for current open/waiting/closed lifecycle counts, since the scheduled_runs `cycle_*_summary.md` files were not present for today's run folder (scheduler.log itself was fresh, <1 min old, so no defer triggered)
- External web research: not invoked this cycle — internal news_items / catalyst_events coverage was sufficient and recent (<4h) for every candidate reviewed; no candidate's verdict depended on external verification

## 3. Scheduler / Data Freshness
- `scheduler.log` mtime: 2026-08-18 17:08:55 EEST (fresh, <1 min old) → no defer
- No `cycle_*_summary.md` found in `data/scheduled_runs/2026-08-18_default_schedule/` (only monitor logs present); freshness judged off scheduler.log + report mtimes instead, all well inside the 3h defer threshold
- Scalp/intraday reports: fresh (<45 min)
- Swing (crypto) report: 08:11 EEST → ~9h old → **carry-forward**, flagged
- Stocks intraday: fresh (6 min)
- Stocks swing/invest: last generated 2026-07-02 → **stale**, excluded from final verdicts
- Paper/monitor processes: derivatives_monitor, fast_news_monitor, pending_monitor logs all updating within the last minute — monitoring is live

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-18 17:09 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["cycle_summary_md_today"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 17:08:55 EEST", "stocks intraday report 17:03 EEST", "crypto swing report 08:11 EEST (9h, carry-forward)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "shorts_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: range/chop label but BTC/ETH uptrend, breadth 47.5%/EMA20", "stocks: regime=bullish label but early tape shows chip/AI names tumbling on yields", "macro risk 100/100, Iran/Hormuz + Ukraine headlines, 30Y yield 19y high"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "stale_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["73.8% of today's catalyst_events unmapped to a symbol", "2 active narrative baskets", "GE GEK800 USAF contract confirmed multi-source", "XRP Jeonbuk Bank partnership catalyst confirmed but no technical setup backing it"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["order_book_depth", "liquidation_heatmap"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Most crypto C-tier shorts capped by short_squeeze_risk / thin_liquidity_short_squeeze_risk tags across scalp+intraday reports", "ACE/RED funding negative + elevated crowding on external venues"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["SMH/XLK/QQQ stocks shorts already missed_no_entry this cycle — price moved away before fill", "GE/META/AVGO/DIA still waiting_for_entry, not yet chased"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 13 OPEN actionable (triggered, unexpired, A/B)", "stocks A/B: 4 WAITING for entry (GE, META, AVGO, DIA), 5 NO-ENTRY/stale/moved-away (SMH, XLK, QQQ, UBER, BX)", "4 untracked legacy crypto alerts (HEMI x2, EDEN, GPS) — sent to Telegram, no proposed_signal to track"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "manual_review", "correlation_cluster"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["META: 29-state lawsuit reportedly in court today (Tuesday) — active legal headline not yet in production risk-warning block", "HD/PANW earnings today — do_not_chase flagged, both correctly not in A/B list", "all 9 open crypto positions are longs — no short hedge against risk-off macro overlay"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B weekly: WR 20%, PF 2.78, TotalR +30.2 — small-WR/big-avg-win profile intact", "stocks A/B weekly: WR 11.1%, PF 0.0, TotalR -1.0 — stocks A/B book currently net negative on tiny sample (n=18 triggered)", "stocks intraday shorts subset historically PF 9.00 vs longs structurally weak (per playbook note) — supports preferring AVGO/DIA shorts over chasing more longs"] },
    { "agent": "head_trader", "verdict": "see below", "confidence": 0.65,
      "reason_codes": [], "data_missing": [], "suggested_effect": "advisory_only", "facts_used": [] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.62,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "GE", "trigger": "long zone 369.45-370.71, stop 368.18, TP1 374.50 — already waiting_for_entry", "reason": "RS leader vs SPY/sector, GEK800 USAF contract catalyst confirmed multi-source, prior instance today already hit TP1" },
    "best_short_candidate":    { "symbol": "AVGO", "trigger": "short zone 379.36-381.60, stop 383.84, TP1 372.64 — waiting_for_entry", "reason": "Sector-confirmed by concurrent SMH/XLK/QQQ tech shorts (chip/AI names tumbling on yields), no legal/headline risk, clean vs META which is legally compromised" },
    "best_catalyst_candidate": { "symbol": "GE", "trigger": "same as best-long — GEK800/JASSM USAF engine contract, Kratos+GE multi-source", "reason": "Only candidate today with a verified, multi-source, non-crypto-legal-risk catalyst directly backing an active A-tier setup" },
    "avoid_candidate":         { "symbol": "META", "reason": "Active 29-state lawsuit reportedly reaching court today (Tuesday) per Motley Fool 2026-08-17 — legal/headline risk not yet reflected in the production risk-warning block; demote to manual review despite B-tier score and prior TP2-hit track record" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | mixed, chop, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, stale_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | ok | 0.85 | open_actionable, waiting_for_entry, no_entry | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, manual_review, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.60 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.62 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review
Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_1139.md` (Europe / pre-US context, 11:39 EEST).
- **GE**: was `tp1_hit` on an earlier instance at 11:39; a fresh A-tier GE long re-fired at 14:01-14:09 EEST, itself already TP1-hit once (14:16) and now a third fresh instance is `waiting_for_entry` — thesis confirmed and repeating, catalyst (GEK800 USAF contract) unchanged.
- **ADA/USDT**: was the prior review's best short-watch (weak-vs-market + governance-freeze catalyst); no ADA signal fired today at all — dropped out of scoring, no longer on the desk. Thesis neither confirmed nor invalidated, just stale.
- **HEMI/USDT**: was `waiting_for_entry` in the prior review; now `triggered` (open, unresolved) on the swing book.
- **Stocks session**: was closed/pre-market in the prior review (20 C-tier planning signals only); now in regular session with 4 fresh A/B (GE, META, AVGO, DIA) and 5 already `missed_no_entry` (SMH, XLK, QQQ, UBER, BX) — confirms the early reaction is broad-based tech/semis weakness.
- **Untracked alerts**: prior review found none; this cycle found **4** (HEMI x2, EDEN, GPS) — new occurrence of the known watchlist-alert/signal-reuse issue (see [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] context) → TODO-3.
- **Catalyst mapping**: prior review 70.3% unmapped; now 73.8% unmapped — trend worsening slightly, still weak.

## 5. Catalyst Coverage
- Total catalyst_events today (as of 17:09 EEST): **2444**; mapped to a symbol: **640** (26.2%); unmapped: **1804 (73.8%)**.
- Narrative baskets active: **2** (perps_dex_narrative primary HYPE; momentum_breakout primary EDEN — per the 16:35 intraday report; the swing report additionally carried rwa_narrative/ai_narrative/binance_ecosystem_teaser earlier in the day, now rolled off).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (illustrative — mostly small-cap/PR-newswire noise, not tradable):
  - "Enginprime Medical Closes $12M Series A Financing"
  - "Greenberg Traurig's Marissa A. Neufeld Appointed to Miami Homes For All Board of Directors"
  - "Aastro Roofing Company Named Deerfield Beach's Roofer of the Year"

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed** (BTC/ETH technically uptrend, altcoin breadth only 47.5% above EMA20, system regime label = range/chop; heavy risk-off macro overlay from Iran/Hormuz shipping incident + Ukraine drone strikes + 30Y yield at a 19-year high)
- Stocks mood: **mixed** (daily regime label = bullish, VIX low at 15.69, breadth 100%; but early intraday reaction is risk-off in chip/AI names — NVDA/MU/SNDK tumbling on rising yields — while defensive/value sectors (energy, healthcare, industrials) lead)
- Dominant narrative: rate-driven rotation out of AI/semis hardware into energy/industrials/healthcare; crypto largely idle, no fresh catalyst-backed momentum
- Preferred side now: **mixed / catalyst-backed** — longs only where RS-leadership + a real catalyst both confirm (GE); shorts only where sector confluence confirms (AVGO, alongside SMH/XLK/QQQ already reacting) and no legal cloud exists
- Best long candidate: **GE** (stocks) — waiting_for_entry 369.45-370.71
- Best short candidate: **AVGO** (stocks) — waiting_for_entry 379.36-381.60
- Best catalyst-backed candidate: **GE** — GEK800/JASSM USAF engine contract, multi-source, already validated once today with a TP1 hit
- What to avoid: **META** short (legal headline: 29-state lawsuit reportedly in court today) and chasing SMH/XLK/QQQ shorts that already moved away from their entry zones
- What would change the view: a confirmed RTH close reclaiming SMH/XLK above their invalidation levels (bull case for chips), or BTC losing local support (would flip crypto to risk-off short-preference)

## 7. Candidate Deep Dives

### #1 — GE long (stocks, A-tier, `waiting_for_entry`)
- Has price already reacted to the catalyst? Partially — the GEK800 contract news drove an earlier TP1 hit today (14:01→14:16 instance); the current fresh instance (14:09, still open) is a continuation entry, not a fresh reaction.
- Is the setup chasing? No — entry zone 369.45-370.71 is the current pullback/continuation zone, not extended.
- Retest/pullback structure? Yes — this is effectively a retest entry after the earlier TP1.
- Overextended (>2 ATR from EMA20)? Not flagged in the report.
- Would entry now be late? No, still waiting_for_entry.
- Actionable level: fills inside 369.45-370.71; invalidate on 1h close beyond 368.18.
- Aligned with market mood? Yes — industrials/defense is one of today's leading, non-AI/semis sectors.
- Long or short: long. Actionable now (waiting for fill) — no RTH confirmation gate needed, already deep into the session.
- Invalidation: close beyond 368.18.
- Chase risk: low.
- Catalyst confirmation: yes — GEK800 USAF engine award (Kratos + GE Aerospace), multi-source, no contradiction found.
- **TradingView / manual chart check unavailable** — using only local OHLCV/ATR/EMA fields from the report.

### #2 — AVGO short (stocks, B-tier, `waiting_for_entry`)
- Has price already reacted to the catalyst? Yes — broad chip-sector reaction to rising yields (per "Tech Futures Sink As Treasury Yields Jump; Nvidia, Micron, Sandisk All Tumble" headline); AVGO is a laggard within that move.
- Is the setup chasing? No — still waiting_for_entry, not yet triggered.
- Retest/pullback structure? Entry zone 379.36-381.60 is a short-side retest zone below the invalidation level (383.84).
- Overextended? Not flagged.
- Would entry now be late? No.
- Actionable level: fills inside 379.36-381.60; invalidates on close beyond 383.84.
- Aligned with mood? Yes — sector-confirmed by SMH/XLK/QQQ shorts already reacting in the same direction (though those three already moved away from their own entries — AVGO has not).
- Long or short: short, actionable now.
- Invalidation: close beyond 383.84.
- Chase risk: low (not yet triggered).
- Catalyst confirmation: directional (rate/yield-driven sector rotation), no company-specific negative catalyst found; no legal/headline risk on AVGO specifically.

### #3 — META short (stocks, B-tier, `waiting_for_entry`) — DOWNGRADED
- Score 71.75, entry 549.15-551.78, stop 554.42, TP1 541.25. A prior META short instance yesterday hit TP2 — playbook has a track record.
- **LEGAL/HEADLINE RISK:** "Meta Faces 29 States in Court Tuesday. The Case Could Be Big Tech's Big Tobacco Moment." (The Motley Fool Investing, 2026-08-17). Today (2026-08-18) is Tuesday — the court appearance referenced is almost certainly today. This is not yet reflected in the production risk-warning block (which lists only BTC, DXCM, HD, PANW as of this cycle).
- Per source-discipline: **Final verdict = MANUAL REVIEW REQUIRED**, not a clean actionable, even though the bearish direction happens to be directionally consistent with adverse legal headlines. Binary headline-driven gap risk on an active multi-state court case is a distinct risk from the technical short thesis and needs an operator's read before treating as a routine sector-rotation short.
- Do not auto-treat as "confirms the short" — legal headline risk changes the risk profile (gap risk, halt risk on ruling news), not just the direction.

### #4 — DIA short (stocks, B-tier, `waiting_for_entry`)
- Score 68.26, entry 533.67-534.19, stop 534.70, TP1 532.12. ATR-only/tight RR (rr_to_tp1 1.50, small absolute range — report itself flags "ATR too small for actionable move" as evidence). Index-level short, same sector-rotation logic as QQQ (which already moved away). Treat as a low-conviction hedge idea, not a standout — watch only if AVGO/QQQ confirm follow-through.

### #5 — 9 open crypto B-tier longs (ALLO, RED, POL, HEMI, ZEC, PUMP, ONG, CHIP, WLFI) — portfolio-level review, no new entries
- All triggered (open, unresolved), all long, none stopped/closed as of this run.
- Concentration risk: 100% long exposure on the crypto book against a risk-off macro overlay (Iran/Hormuz, Ukraine, yields) — no short hedge currently held.
- No single name stands out as needing urgent action this cycle (no stop-proximity or invalidation-breach flagged in the reports); routine hold/monitor.
- What would invalidate: BTC losing local support per the reports' own no-trade warning ("If BTC loses local support, reduce long aggression immediately").

## 8. Best Candidates Ranked
1. **GE long** (stocks, A-tier) — best overall: catalyst + RS-leadership + proven today (TP1 hit on a prior instance). Trigger: fill 369.45-370.71.
2. **AVGO short** (stocks, B-tier) — best clean short: sector-confirmed, no legal cloud. Trigger: fill 379.36-381.60.
3. **DIA short** (stocks, B-tier) — secondary/hedge idea only, thin RR. Trigger: fill 533.67-534.19, confirm via AVGO/QQQ follow-through first.
4. **XRP/USDT catalyst-watch** (crypto, no current score/tier) — real catalyst (Jeonbuk Bank partnership) but no technical setup backing it yet. Trigger: RS turning positive vs BTC + a scoreable technical structure on 15m-1h.
5. **META** — explicitly NOT ranked as actionable; watch-only pending operator legal review. Trigger to re-admit: court outcome known/priced, or production risk-warning block picks it up and it clears review.

## 9. Avoid / No Trade
This is a decision-window verdict only — the scanner, tracking, and monitors continue uninterrupted regardless.
- **META short**: avoid as a clean actionable this window — active 29-state lawsuit reportedly in court today; manual review required before treating as routine.
- **SMH / XLK / QQQ shorts**: avoid chasing — already `missed_no_entry`, price has moved away from the planned zone; wait for a fresh retest.
- **New crypto longs on no-catalyst momentum names** (EDEN, RED, GPS, ALLO, FIL, GPS, etc. — all currently C-tier/watchlist only): avoid — desk's own 14d cut shows no-catalyst crypto intraday is net-negative (WR 23% / PF 0.70 / -3R); nothing here clears the bar to become actionable.
- **New crypto shorts on the "weak" list** (PORTAL, KORUB, VELVET, SOXLB, SNXXB, etc.): avoid — every one is capped to C-tier by short-squeeze-risk / thin-liquidity guards across both scalp and intraday reports.

## 10. Main Risks
- **Macro/geopolitical**: risk score 100/100 — Strait of Hormuz shipping attack + Iran/US tension, Ukraine drone strikes on Moscow, 30Y Treasury yield at a 19-year high. Reduce alt-long aggression; the crypto book is 100% long with no hedge.
- **Legal/headline (stocks)**: META's active multi-state court case is a genuine gap-risk event not yet captured by the production risk-warning automation — flagged as TODO-1.
- **Catalyst mapping weak (73.8% unmapped)**: reduces confidence in "catalyst-backed" tags across the board this cycle; treat catalyst_backed source tags in the C-tier expansion watchlist with caution.
- **Untracked legacy alerts (4 today)**: HEMI x2, EDEN, GPS sent to Telegram without a trackable proposed_signal — these will not contribute to PF/winrate tracking, a recurring known issue.
- **Stocks A/B weekly performance is currently net negative** (PF 0.0, TotalR -1.0, n=18 triggered) — small sample, but do not scale up size on stocks A/B until this stabilizes.
- **BTC exploit/hack risk events** (Coldcard exploit, data-breach headline) are active `block_requires_operator_review` flags on BTC — correctly excluded from new A/B consideration this cycle.

## 11. Action Plan — next 4 hours
1. Watch GE for a fill inside 369.45-370.71; if filled, standard TP1/TP2/TP3 ladder (374.50/377.03/380.82) applies — no manual intervention needed.
2. Watch AVGO for a fill inside 379.36-381.60; treat as the cleanest sector-confirmed short of the session.
3. Do NOT act on META short until an operator manually reviews the 29-state lawsuit headline and either confirms it's priced in / non-material or the production risk-warning block picks it up.
4. Hold the 9 open crypto longs; no new crypto entries this cycle (scalp/intraday/swing all returned empty A/B). Re-check BTC support levels before the next cycle.
5. Do not chase SMH/XLK/QQQ shorts that already moved away — wait for a fresh retest signal next cycle.
6. Route any manual promotion of XRP/USDT (catalyst present, no setup yet) only if a technical structure appears on 15m-1h with RS turning positive vs BTC.

## 12. Final Verdict per Mode
- **Crypto scalp**: NO TRADE this cycle — data does not justify a fresh idea (own report's verdict); scanner continues.
- **Crypto intraday**: NO TRADE this cycle — best watchlist name EDEN/USDT at 58.1/100, below threshold; scanner continues.
- **Crypto swing**: NO TRADE this cycle (report is 9h old, carry-forward only) — best watchlist name ALLO/USDT at 61.8/100, below threshold.
- **Crypto portfolio (existing)**: HOLD — 9 open B-tier longs, monitor BTC support, no hedge currently held.
- **Stocks intraday**: WATCH / WAIT-FOR-TRIGGER — GE long and AVGO short both actionable and waiting_for_entry; META short MANUAL REVIEW REQUIRED (legal risk); DIA short low-conviction watch-only.
- **Stocks swing/invest**: data stale (>6 weeks) — no verdict possible this cycle, excluded.

## 13. Sources
- [Home Depot Beats Estimates in a "Frozen" Housing Market](https://finance.yahoo.com/markets/stocks/articles/home-depot-beats-estimates-frozen-122124759.html) — Yahoo Finance Top Stories, 2026-08-18 (internal news_items feed)
- [Stock Market Today: Tech Futures Sink As Treasury Yields Jump; Nvidia, Micron, Sandisk All Tumble](https://www.investors.com/market-trend/stock-market-today/dow-jones-sp500-nasdaq-treasury-yields-nvidia-stock-nvda/?src=A00220&yptr=yahoo) — Yahoo Finance Top Stories, 2026-08-18 (internal news_items feed)
- [Meta Faces 29 States in Court Tuesday. The Case Could Be Big Tech's Big Tobacco Moment.](https://www.fool.com/investing/2026/08/17/meta-faces-29-states-in-court-tuesday-the-case-could-be-big-techs-big-tobacco-moment/?source=iedfolrf0000001) — The Motley Fool Investing, 2026-08-17 (internal news_items feed)
- [Kratos and GE Aerospace's GEK800 Engine Receives U.S. Military Type Designation F143-ZZ-100 and EMD Contract Award for JASSM](https://www.globenewswire.com/news-release/2026/08/17/3345950/224/en/kratos-and-ge-aerospace-s-gek800-engine-receives-u-s-military-type-designation-f143-zz-100-and-emd-contract-award-for-jassm.html) — GlobeNewswire, 2026-08-17 (internal news_items feed)
- [Ripple partners with South Korea's Jeonbuk Bank for cross-border payments](https://www.theblock.co/news/business/2026-08-18-ripple-south-korea-jeonbuk-bank-412049) — The Block, 2026-08-18 (internal news_items feed)
- [Bitcoin purchases halted after data breach puts 250,000 crypto users at risk] — CryptoSlate, internal news_items feed (2026-08-18, exact URL not captured in feed row)
- Internal: `data/reports/scalp/2026-08-18_13-28_scalp_report.md`, `data/reports/intraday/2026-08-18_13-35_intraday_report.md`, `data/reports/swing/2026-08-18_05-11_swing_report.md`, `data/reports/stocks/intraday/2026-08-18_14-03_stocks_intraday_report.md`
- Internal: `db/crypto_ai_desk.sqlite` (`proposed_signals` and `news_items` tables, queried directly), `data/catalysts/2026-08-18/catalyst_events.jsonl`
- **External web research unavailable this cycle** — not invoked; internal news_items/catalyst_events coverage was sufficient (<24h) and consistent for every candidate reviewed, per §G discipline (internal-first, external only when internal is missing/stale/contradicted).

## 14. Fix Requests / TODO

### TODO-1: META legal-headline gap not yet in production risk-warning block
- **issue:** META has an active 29-state lawsuit reportedly reaching court today (2026-08-18, Tuesday) per an internal news_items row, but the production "Operator-review warning" block (§5c-style section in the stocks intraday report) only lists BTC, DXCM, HD, PANW — META is absent.
- **evidence:** `data/reports/stocks/intraday/2026-08-18_14-03_stocks_intraday_report.md`, News/Catalysts §4 META section: "Meta Faces 29 States in Court Tuesday. The Case Could Be Big Tech's Big Tobacco Moment. (The Motley Fool Investing, 2026-08-17)"; Production risk warnings section lists only BTC/DXCM/HD/GE/AMD/PANW.
- **suggested manual fix:** review the legal_risk / class_action detector's symbol-matching and severity thresholds — a "X states sue Y in court [today]" headline should likely trigger `block_requires_operator_review` the same way HD/PANW earnings-day warnings do.
- **priority:** high
- **first observed:** 2026-08-18 17:09 EEST

### TODO-2: Catalyst mapping stuck below 50% (worsening)
- **issue:** catalyst symbol-mapping coverage is 73.8% unmapped today, up from 70.3% at the 11:39 EEST review — trend is worsening, not improving.
- **evidence:** computed directly from `data/catalysts/2026-08-18/catalyst_events.jsonl` (2444 total events, 640 mapped, 1804 unmapped) this cycle; prior cycle's review stated 70.3% unmapped.
- **suggested manual fix:** audit the symbol resolver in the catalyst ingestion layer — sample of unmapped headlines this cycle are small-cap PR-newswire noise (financings, board appointments, local business awards) that likely should be filtered out entirely rather than counted as "unmapped catalyst events," which would improve the effective mapping ratio without needing better symbol resolution.
- **priority:** medium
- **first observed:** 2026-08-18 17:09 EEST (recurring; also noted 2026-08-18 11:39 EEST)

### TODO-3: Untracked legacy crypto alerts recurring (4 today)
- **issue:** `detect_untracked_legacy_alerts` found 4 watchlist_alerts sent to Telegram today (HEMI/USDT x2, EDEN/USDT, GPS/USDT) with no matching `proposed_signal` within ±6h — these alerts will never contribute to PF/winrate/avgR tracking.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-18` output, this cycle: 4 rows, all `trackable=NO (no proposed_signal)`.
- **suggested manual fix:** this is a known, previously-confirmed issue (watchlist re-fire reusing a stale/closed signal_id instead of minting a new proposed_signal on legitimate re-triggers) — escalate priority given repeated recurrence across multiple review cycles.
- **priority:** high
- **first observed:** 2026-08-18 17:09 EEST (recurring — prior confirmed instances on ALLO/USDT and BANK/USDT per project history)
