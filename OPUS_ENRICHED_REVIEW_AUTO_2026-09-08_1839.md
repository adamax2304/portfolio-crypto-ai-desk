# Opus Enriched Review — US Open Reaction Review — Auto Cycle 18:30 EEST

## 1. Executive Summary
- **Slot: US open reaction review** (18:30 EEST ≈ 11:39 ET, mid-morning RTH). **Advisory only / no auto-trade.**
- Market is dominated by a geopolitical shock: Iran/Houthi strikes on Saudi energy sites, Brent ~$98, US-Iran tensions escalating — macro risk score 99.5/100. Dow sold off ~500pts on the headlines; VIX only 15.67 (elevated concern, not yet panic).
- Crypto: BTC in `transition_down`, ETH range, but altcoin breadth still high (72.9%>EMA20, 85.4%>EMA50) — a mixed tape, risk-off tilt from BTC leadership, no crypto A/B-tier actionable signals fired this cycle (all C-tier watchlist).
- Stocks: two new **A-tier** intraday signals fired live after the open — **HUT long** (94.65, RS-leader miner/AI-pivot name) and **MAR short** (91.84, clean technical laggard, no catalyst). Both still `waiting_for_entry`.
- Catalyst mapping is weak this run (~74% unmapped) — treat the catalyst layer as context, not as a final-decision driver.
- No system-integrity issues found (untracked-alert detector: clean).

## 2. Data Used
- `data/reports/intraday/2026-09-08_14-55_intraday_report.md` (generated 17:54 EEST — fresh)
- `data/reports/swing/2026-09-08_02-45_swing_report.md` (generated 05:45 EEST — **borderline stale**, ~13h old)
- `data/reports/stocks/intraday/2026-09-08_12-18_stocks_intraday_report.md` (generated 15:18 EEST, pre-market snapshot — superseded by live DB signals created after the open)
- `data/catalysts/2026-09-08/catalyst_events.jsonl`, `narrative_baskets.jsonl` (updated 18:17 EEST)
- `data/processed/llm_analysis_packet.md` (17:59 EEST), `llm_stocks_packet.md` (15:21 EEST)
- `proposed_signals`, `news_items` (SQLite `db/crypto_ai_desk.sqlite`) — direct read queries for live signal status, A-tier detail, and MAR legal/headline check
- CLI: `active-signals --asset-class crypto`, `active-signals --asset-class stocks`, `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-09-08`
- **External web research: not invoked this cycle.** Internal `news_items` records for the reviewed candidates (MAR, HUT, BNB) were fresh (<48h) and internally consistent — no fabricated/contradicted claims that required external verification per the internal-first discipline.

## 3. Scheduler / Data Freshness
- `scheduler.log`: mtime 18:36 EEST — **fresh** (3 min old at read time).
- Latest cycle summary: `cycle_05_14-13_summary.md`, mtime 15:42 EEST — **~3h old**, within the "not deferred" threshold (defer requires BOTH >3h; scheduler.log is fresh so no defer).
- Crypto intraday report: fresh (~45min old).
- Crypto swing report: **borderline stale** (~13h old, in the 12–14h bracket) — used only as background context, not for fresh directional calls; live DB swing signals (e.g. BNB) used instead where fresher.
- Stocks intraday report: file itself predates the US cash open (pre-market snapshot, all A-tier demoted to C in the file) — **superseded** by live `proposed_signals` rows created at 14:12–15:27 UTC (after the 13:30 UTC open), which are the actionability source of truth for this review.
- Catalyst data: fresh (18:17 EEST, ~20min old).
- `CryptoAIDesk_Scheduler` Windows Task shows **State=Disabled** in Task Scheduler, but `scheduler.log` is actively updating (3 min old) and cycles are completing on cadence — the running process is evidently alive and is presumably supervised by `CryptoAIDeskMonitor`/`CryptoAIDeskHeartbeat` rather than by re-triggering this task. Flagged as a low-priority TODO for a human to confirm this is intended (see §14) — not treated as a freshness failure since actual log/cycle evidence contradicts it.
- No monitor/paper-portfolio status file was read this cycle (out of scope for the allowed read set); scheduler+cycle freshness above stands in as the liveness signal.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-09-08 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["monitor/paper status file"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 18:36", "cycle_05 mtime 15:42", "swing report ~13h old", "stocks intraday report predates open"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["risk_off", "mixed", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["macro risk score 99.5/100", "Iran-Saudi oil strikes, Brent ~$98", "BTC transition_down / ETH range", "altcoin breadth 72.9%/85.4%", "SPY/QQQ/XLY below VWAP, VIX 15.67"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "stale_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["73.7% of today's catalyst_events unmapped", "6 active narrative baskets (perps_dex/HYPE, binance_ecosystem/BNB, rwa, ai)", "HUT catalyst_quality=none (1-day-old AI-deal news)", "MAR catalyst_quality=none"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "funding_extreme", "oi_supports"],
      "data_missing": ["OI history for most MEXC-fallback symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["SOPH funding -0.0177 to -0.02 across bybit/okx/mexc, crowding elevated", "INJ price+OI up, funding neutral", "DOT global long/short heavily long-skewed"] },
    { "agent": "technical_entry", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["entry_fresh", "clean_retest", "waiting_for_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HUT above prev-day high, RS-leader, sector confirmation provisional", "MAR laggard short, sector confirmation confirmed, both SPY/QQQ/XLY below VWAP", "both A-tier signals still waiting_for_entry, no chase yet"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["open_actionable", "waiting_for_entry", "closed_flat"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 11 open/partial, 2 waiting, 12 no-entry/stale/moved-away, 1 closed win, 6 closed loss (24h)", "stocks: 5 open/partial, 24 waiting_for_entry, 5 closed win (24h)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["operator-review warnings on AMZN/BTC/ORCL/TAO/XRP", "MAR checked directly for legal/fraud/SEC/DOJ risk — none found, prior hits were ticker-collision false positives (Mar-a-Lago, Marín airport)", "weekend-mode crypto underperformance (known, WR 10% n=105)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["playbook_working", "low_sample"],
      "data_missing": ["stocks loss-resolution sample too thin (n=3 losses on 322 triggered, mostly still open)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier week: WR 18.5%, PF 2.45, totalR +49.3 (asymmetric TP-touch dynamic per known project history)", "stocks B-tier WR 15%, C-tier WR 4% (reliable samples, but mostly unresolved/open, not final loss counts)"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "HUT", "trigger": "RTH hold above 93.50 with volume confirmation (entry zone 92.47-93.50); do not chase pre-confirmation", "reason": "A-tier 94.65, RS-leader vs SPY (+5.99% 20d), above prev-day high, but catalyst is 1-day-old (AI-pivot/Anthropic-deal news) — technical leadership, not a fresh catalyst" },
    "best_short_candidate":    { "symbol": "MAR", "trigger": "RTH failed-bounce/breakdown confirmation into 336.51-337.44 zone, stop 338.37", "reason": "A-tier 91.84, clean laggard in downtrend, sector (XLY) and SPY/QQQ both below VWAP confirm broad weakness, no catalyst contamination" },
    "best_catalyst_candidate": { "symbol": "BNB/USDT", "trigger": "pullback long fill in 759.24-761.96 zone, invalidation 755.92", "reason": "backed by binance_ecosystem_teaser basket (fresh <6h), B-tier 73.8, swing continuation in a bullish-trend classification" },
    "avoid_candidate":         { "symbol": "SOPH/USDT", "reason": "up 67.6%/24h and 120.7%/7d with negative funding (-0.0177 to -0.02) and elevated crowding across bybit/okx/mexc — classic squeeze-prone parabolic; chasing long here is high-risk, and shorting into negative funding against strong momentum is also crowded" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.80 | risk_off, mixed, chop | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, stale_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, funding_extreme, oi_supports | advisory_only |
| technical_entry | ok | 0.65 | entry_fresh, clean_retest, waiting_for_entry | advisory_only |
| execution_lifecycle | ok | 0.85 | open_actionable, waiting_for_entry, closed_flat | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.55 | playbook_working, low_sample | advisory_only |
| head_trader | ok | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review
Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1603.md` (16:20 EEST, pre-US-open slot):
- **New:** HUT A-tier long (94.65) and MAR A-tier short (91.84) — both fired live after the open (14:25–15:27 UTC), neither existed in the pre-open review.
- **Carried forward / still valid:** NFLX B-tier short (86.25, `waiting_for_entry`, entry 78.24-78.65) — same signal, unchanged status.
- **Expired NO-ENTRY since last review:** MU (was "best long candidate" at 16:20, score 88.34) and MS (was "best catalyst-backed candidate", score 80.83) — both now `missed_no_entry`; neither ever triggered. This is a **no-entry/stale expiry**, not a missed-winner signal by itself — the market simply never traded into their zones.
- **Thesis change:** market mood has hardened from "pre-open gap risk" to confirmed **risk-off intraday** (SPY/QQQ/XLY below VWAP, trend_down regime) — consistent with, not contradicting, the prior review's caution.
- Catalyst coverage: mapping weakness (~74% unmapped) persists across both reviews — not a new finding.

## 5. Catalyst Coverage
- Catalyst events file: ~2,500 raw event rows logged today; **657 mapped to a symbol, ~1,843 unmapped (≈73.7% unmapped)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets: 6 active (per intraday report) — perps_dex_narrative (HYPE, `wait_pullback`), binance_ecosystem_teaser (BNB, `related_beta_rotation`), delisting_thin_liquidity (no primary), rwa_narrative (ONDO/XLM), ai_narrative (NEAR/RENDER/TAO/FET).
- Top 3 unmapped headlines (illustrative — mostly macro/bond-market noise, not symbol-specific):
  1. "Investigators recover black boxes from cargo plane crash in Miami" (Reuters)
  2. "30-YEAR JAPANESE GOVERNMENT BOND YIELD DROPS 4.0 BPS TO 3.980%"
  3. "5-YEAR JAPANESE GOVERNMENT BOND YIELD DROPS 2.0 BPS TO 2.230%"

## 6. Market Landscape

Crypto tape is caught between a bearish BTC leader (`transition_down`) and still-elevated altcoin breadth (72.9% above EMA20, 85.4% above EMA50) — money is rotating into select alts (INJ, SOPH, PENDLE, XPL, AERO) even as BTC/ETH stay soft, but the desk's own no-catalyst-intraday-momentum playbook carries a documented -3R / 23% WR failure mode in chop, so none of today's C-tier momentum names cleared the A/B bar. Stocks are trading risk-off intraday (SPY -0.34%, QQQ -0.62% RTH, both below VWAP, sector rotation favoring energy/healthcare and punishing industrials/discretionary) against a VIX that is still calm (15.67) relative to the headline severity — a gap worth watching for a volatility catch-up move. The dominant macro driver by far is the Iran/Houthi strike on Saudi energy infrastructure (Brent ~$98, Dow -500pts on the headline, IRGC submarine-capture claim — unverified, single-source, treat as propaganda-grade noise) which is generating a 99.5/100 macro risk-off score and should be the lens through which every new long is filtered today.

### Market Mood / Risk Routing
- Crypto mood: **mixed / risk-off tilt** (BTC-led downside, alt breadth still resilient)
- Stocks mood: **risk-off / cautious** (indices + sector ETFs below VWAP, but VIX not yet confirming panic)
- Dominant narrative: Iran-Israel/Saudi energy-infrastructure conflict → oil spike → broad risk-off, secondarily AI-hardware/chip strength (ASML/TSMC EUV, semis) as a local pocket of strength
- Preferred side now: **mixed — shorts on confirmed laggards (stocks, e.g. MAR-type technical laggards), selective RS-leader longs only with volume/catalyst confirmation (crypto/miner names)**
- Best long candidate: HUT — trigger: RTH hold above 93.50 with volume; do not chase without confirmation
- Best short candidate: MAR — trigger: RTH failed-bounce/breakdown confirmation near 336.51-337.44; tight stop at 338.37
- Best catalyst-backed candidate: BNB/USDT — trigger: pullback fill 759.24-761.96, invalidation 755.92 (binance_ecosystem_teaser basket, fresh <6h)
- What to avoid: SOPH/USDT (squeeze-prone parabolic, negative funding across venues, both long-chase and short-into-momentum are crowded)
- What would change the view: a de-escalation headline on Iran/Saudi (oil giving back the spike) would likely unlock the risk-on alt rotation already visible in breadth data; a further escalation would likely finally move VIX and confirm the risk-off regime more forcefully

## 7. Candidate Deep Dives

### HUT (long, stocks intraday, A-tier 94.65)
- Has price already reacted to the catalyst? Partially — the Anthropic-deal AI-pivot news is from 2026-09-07 (~1 day old), already priced in to some degree; today's strength (above prev-day high) is more technical/RS-leadership than fresh-news-driven.
- Is the setup chasing? Not yet — still `waiting_for_entry`, entry zone 92.47-93.50 not yet filled at last scan (data ~13min old at signal creation).
- Retest / pullback structure? Entry zone is defined as a breakout-hold zone just above prior resistance — this is a continuation entry, not a deep pullback.
- Overextended (>2 ATR from EMA20)? Not flagged in the raw score (no risk penalty applied, cap_reasons empty).
- Would entry now be late? Only if price has already run past 93.50 by the time this review is read — reconfirm live price before acting.
- What makes it actionable? A confirmed close above 93.50 on volume, with sector confirmation upgrading from "provisional" to "confirmed."
- Aligned with market mood? Partially — it's a long in a risk-off tape, so it needs RS-leadership to justify going against the broad-market grain (which it has, +5.99% vs SPY 20d).
- Long, short, or wait-for-trigger? Wait-for-trigger (zone not yet filled).
- Actionable now or after confirmation? After confirmation — do not chase the stale catalyst alone.
- Invalidation: close back below 91.44 (stop level).
- Chase-risk setup? Moderate — RS-leader names in a risk-off tape can reverse fast if the broad market rolls over further.
- Catalyst confirmation or contradiction? Catalyst is stale (`catalyst_quality: none`), not contradicted, just not fresh enough to lean on.

### MAR (short, stocks intraday, A-tier 91.84)
- Has price already reacted? No fresh catalyst at all — pure technical/relative-strength laggard short (RS vs SPY -4.52%, RS vs sector -0.79%).
- Chasing? No — `waiting_for_entry`, zone 336.51-337.44 not yet filled.
- Retest structure? Entry is a short-the-bounce zone into resistance, which is the cleaner of the two constructions (fading strength into a laggard, not chasing new lows).
- Overextended? No risk penalty applied.
- Would entry now be late? Reconfirm live price — zone is tight (~0.3% wide).
- What makes it actionable? A confirmed rejection/close back below 336.51 after touching the zone, ideally with SPY/QQQ still below VWAP.
- Aligned with mood? Yes — this is the cleanest expression of the risk-off, broad-market-weak thesis today (both SPY and sector ETF confirm below VWAP).
- Long/short/wait? Short, wait-for-trigger.
- Legal/headline risk checked directly: searched `news_items` for MAR over the trailing 72h — no indictment, SEC/DOJ investigation, class action, auditor resignation, or delisting risk found. The only "MAR" hits were ticker-collision false positives (Trump's Mar-a-Lago Club, Luis Muñoz Marín airport in Puerto Rico) plus one operationally-minor item ("Major Marriott resort plans extended closure") — none of which rises to a legal/headline-risk block. **Verdict stands as a clean technical candidate, not AVOID/MANUAL REVIEW.**
- Invalidation: close beyond 338.37.
- Chase-risk? Low — fading strength into resistance, not chasing a breakdown.
- Catalyst confirmation/contradiction? None either way — pure technical setup.

### NFLX (short, stocks intraday, B-tier 86.25, carried forward)
- Unchanged from the 16:20 review — still `waiting_for_entry`, zone 78.24-78.65. No new information this cycle; treat as a still-valid but aging idea (created 14:12 UTC, now ~1h20m old with no fill) — if it hasn't triggered by the next review, downgrade to stale-watch.

### BNB/USDT (long, crypto swing, B-tier 73.8, catalyst-backed)
- Has price already reacted to the catalyst? The `binance_ecosystem_teaser` basket is fresh (<6h per report), and one earlier BNB long (score 65.4, entry 766.97-770.96) already triggered — price has partially responded.
- Chasing? The newer 73.8-score signal has a lower pullback zone (759.24-761.96) than the already-triggered one, i.e. it's waiting for a retracement, not chasing the highs.
- Retest structure? Yes — classic pullback-into-continuation construction, "bullish trend" regime classification with momentum score 76.3/100.
- Aligned with mood? Crypto mood is mixed/risk-off-tilt from BTC, so a BNB long needs the basket-level catalyst support to justify going long — which it has.
- Actionable now or after confirmation? Actionable on a fill into the stated zone; not a chase.
- Invalidation: 755.92.
- Catalyst confirmation: `binance_ecosystem_teaser`, single-source, fresh <6h — moderate confidence, not multi-source-verified.

### SOPH/USDT (avoid — crypto intraday, C-tier only, not actionable)
- Up 67.6% (24h) / 120.7% (7d), volume ratio only 0.31x (thin relative to the move — a red flag for a move this size), funding deeply negative (-0.0177 to -0.02) across bybit/okx/mexc with crowding flagged "elevated."
- This combination (huge run, thin volume, deeply negative funding, external cross-check confirming crowding) is a textbook squeeze setup — dangerous to chase long, and dangerous to short into strong momentum against negative funding (short squeeze risk cuts both ways here). Score capped at C-tier by the desk's own risk gate (43/100) — the system is already treating this correctly as not actionable; flagging it here only as an explicit avoid for manual attention given the size of the move.

## 8. Best Candidates Ranked
1. **MAR short** — cleanest setup today: no catalyst contamination, aligned with confirmed broad-market weakness (SPY/QQQ/XLY all below VWAP), tight defined risk (338.37 stop vs 331.14 TP1, ~2.9R).
2. **HUT long** — best long expression, but catalyst is stale and it's a long against a risk-off tape, so it needs the volume/close confirmation more than MAR does.
3. **BNB/USDT long** — best catalyst-backed idea, moderate confidence (single-source basket), swing timeframe gives more room for the pullback to develop.
4. **NFLX short** — carried forward, aging without a fill; watch for stale-before-entry expiry next cycle.
5. Watch-only: INJ/USDT, PENDLE/USDT (crypto C-tier momentum, no catalyst, chop-mode failure history — do not treat as active).

## 9. Avoid / No Trade
*(This decision window only — scanning, tracking, and monitoring continue regardless.)*
- **SOPH/USDT** — parabolic + thin volume + negative funding + elevated crowding = high squeeze risk in either direction.
- **TAO/USDT, XRP/USDT, BTC/USDT** (exploit_hack risk warnings, `block_requires_operator_review`) — not new A/B candidates today, but any future TAO/XRP/BTC proposal this cycle should get manual review before treating as clean.
- **ORCL** — earnings tomorrow (2026-09-09); `do_not_chase_warning` already flagged by the production risk layer — avoid new positioning into the print regardless of setup quality.
- General: avoid chasing any crypto C-tier no-catalyst momentum name (INJ, PENDLE, XPL, SAHARA, CATI, DOT, SOPH) — the desk's own playbook stats show this bucket runs -3R / 23% WR in the current chop regime.

## 10. Main Risks
- Geopolitical: Iran/Saudi energy-infrastructure conflict is live and escalating (macro risk 99.5/100) — headline risk can move both crypto and stocks sharply intraday; size accordingly.
- VIX (15.67) not yet confirming the headline severity — a volatility catch-up spike is a real tail risk for any position held into the close.
- Crypto catalyst mapping is weak (~74% unmapped) this cycle — don't over-trust the catalyst layer for symbol-specific decisions today.
- Both new A-tier stocks signals (HUT, MAR) are duplicated across two different paper-execution profiles (`breakout_1bar` and `pullback_vwap` lanes) — this is the entry-mode calibration framework working as designed, not a signal-reuse bug (confirmed by differing `report_id`/`paper_lane` values), but worth noting so it isn't miscounted as "4 A-tier signals" when it's really 2 ideas × 2 execution lanes.
- SOPH's cross-venue negative funding + elevated crowding is a live squeeze risk that could spill into correlated small-caps if it unwinds violently.

## 11. Action Plan — next 4 hours
- Watch MAR for a confirmed RTH rejection into 336.51-337.44 before considering the short live (paper/manual review context).
- Watch HUT for a confirmed close/hold above 93.50 on volume before treating the long as validated; do not act on the stale catalyst alone.
- Watch BNB/USDT for a fill into 759.24-761.96; if missed, no chase above that zone.
- Re-check NFLX short next cycle — if still unfilled, treat as stale-before-entry and drop from active watch.
- Monitor Brent/oil headlines and VIX for signs of the risk-off regime either confirming (VIX spike) or fading (oil giving back the spike) — this is the single biggest swing factor for the next 4 hours.
- No action on SOPH, TAO, XRP, BTC beyond continued read-only monitoring.

## 12. Final Verdict per Mode
- **Crypto scalp:** no fresh reports since Aug 30 — mode appears deprecated/inactive; no verdict possible, not scanned this cycle.
- **Crypto intraday:** NO CLEAN A/B TRADE this window — C-tier watchlist only (INJ, PENDLE, XPL, SAHARA, CATI, DASH, DOT, SOPH); wait for RS-leader or breakout confirmation per the desk's own no-catalyst-chop playbook guidance.
- **Crypto swing:** BNB/USDT long is the actionable idea (catalyst-backed, B-tier); swing report itself is borderline stale (~13h) so treat with normal caution, not urgency.
- **Stocks intraday:** two live A-tier ideas (MAR short, HUT long), both `waiting_for_entry` — actionable on confirmation only, not on the stale pre-open report. Market is genuinely open and both are within the live-scan lifecycle.
- **Stocks swing / invest:** deprecated (no reports since late June/early July per prior project history) — not evaluated.

## 13. Sources
- Internal: [proposed_signals / news_items SQLite queries — this session, 2026-09-08 18:30-18:50 EEST]
- [data/reports/intraday/2026-09-08_14-55_intraday_report.md] (generated 2026-09-08 17:54 EEST)
- [data/reports/swing/2026-09-08_02-45_swing_report.md] (generated 2026-09-08 05:45 EEST)
- [data/reports/stocks/intraday/2026-09-08_12-18_stocks_intraday_report.md] (generated 2026-09-08 15:18 EEST)
- [data/catalysts/2026-09-08/catalyst_events.jsonl / narrative_baskets.jsonl] (updated 2026-09-08 18:17 EEST)
- No external web sources cited this cycle (internal-first discipline satisfied; no WebSearch/WebFetch invoked).

## 14. Fix Requests / TODO

### TODO-scheduler-task-disabled
- **issue:** Windows Task Scheduler shows `CryptoAIDesk_Scheduler` as `State=Disabled`, even though `scheduler.log` and cycle summaries are actively updating on cadence (last cycle 15:42 EEST, log 18:36 EEST).
- **evidence:** `Get-ScheduledTask` output this run: `CryptoAIDesk_Scheduler  Disabled`; `data/scheduled_runs/2026-09-07_default_schedule/scheduler.log` mtime 2026-09-08 18:36; `cycle_05_14-13_summary.md` mtime 2026-09-08 15:42.
- **suggested manual fix:** Confirm this is intended (e.g. the task is only used to auto-start the long-running process at boot and `CryptoAIDeskMonitor`/`CryptoAIDeskHeartbeat` supervise restarts thereafter, per prior project notes). If not intended, a human session should re-enable the task or document why it's deliberately disabled so future auto-reviews don't need to re-flag it.
- **priority:** low
- **first observed:** 2026-09-08 18:39 EEST

### TODO-catalyst-mapping-weak-persistent
- **issue:** Catalyst → symbol mapping is weak again this cycle (~73.7% of today's ~2,500 catalyst_events rows unmapped), consistent with the known low symbol-match-rate issue from the news-layer hardening work.
- **evidence:** `data/catalysts/2026-09-08/catalyst_events.jsonl` — 657 mapped / 1,843 unmapped of 2,500 total rows.
- **suggested manual fix:** No new action needed beyond what's already tracked — this is a recurring/known condition, not a new regression. Surfaced again here only per the standing instruction to log it whenever observed >50% unmapped.
- **priority:** low
- **first observed (this recurrence):** 2026-09-08 18:39 EEST (previously tracked in project memory from news-layer hardening work)
