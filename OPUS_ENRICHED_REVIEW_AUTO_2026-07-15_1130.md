# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:30 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context** (11:30 EEST, 2026-07-15). **Advisory only — no auto-trade, no code/scoring/routing changes.** Crypto is in range/chop with BTC/ETH nominally in uptrend but weak breadth (43.9% above EMA20) and a risk-off macro overlay (US-Iran Strait of Hormuz strikes, macro risk 100/100) — no fresh A/B ideas this cycle, only C-tier watch names. Stocks pre-market is **risk_on** (VIX 16.5, breadth 75%/100%) with a wide pre-gate-A breadth (JPM, META, NVDA, PLTR, XLF, GOOGL, AMZN, COIN) currently demoted to C purely by the "market closed" planning gate — a genuinely constructive setup for the US session if it survives the open. UNH stays AVOID (confirmed DOJ probe + earnings tomorrow). No system-integrity blockers; one untracked crypto alert (FF/USDT) and a large stale-status backlog in stocks tracking are flagged as TODOs, not fixed.

## 2. Data Used

- Reports: `2026-07-15_07-13_scalp_report.md`, `2026-07-15_07-19_intraday_report.md` (crypto), `2026-07-15_07-31_stocks_intraday_report.md` (stocks). Crypto `swing` report last generated `2026-07-14_02-15` (>24h — carried forward as stale, see §3). Stocks `swing`/`invest` reports last `2026-07-02` — these are the deprecated legacy playbooks (see Playbook Context in the LLM packet); not used for verdicts.
- `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md` (both ~1h old).
- `data/catalysts/2026-07-15/catalyst_events.jsonl` (2,000 rows today, cumulative), `narrative_baskets.jsonl` (2 active baskets).
- Internal `news_items` / `proposed_signals` SQLite tables (direct queries) for UNH legal-risk verification and lifecycle counts.
- CLI: `active-signals` (crypto, stocks), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts`.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-15_0430.md`.
- **External web research not attempted this run** — internal news_items + catalyst_events were recent (<24h), present, and consistent for every candidate reviewed (UNH DOJ probe, JPM earnings), so no candidate required the external-research fallback per the routine's internal-first rule.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 10:36 EEST, latest `cycle_04_10-06_summary.md` mtime 10:36 EEST — both ~1h old at review time (11:39 EEST UTC 08:39). **Not deferred.**
- crypto_monitor / derivatives_monitor / pending_monitor logs all updating within the last few minutes — monitors healthy.
- Crypto `swing` report: **stale** (last full run 2026-07-14 02:15, ~33h old). Today's cycles 01–04 all show `Daily long-horizon swing/invest included: False` — this matches the normal intermittent cadence (swing/invest is not run every 2.5h cycle, unlike scalp/intraday), not a new regression; the individual active swing *signals* in the tracker are still live and used below. Full swing report content itself is excluded from this review's verdicts per the >14h staleness rule.
- Stocks `swing`/`invest` full reports: last 2026-07-02 — expected, these are the deprecated `stocks_swing_watchlist_rs_rotation` / `stocks_invest_watchlist_30d_thesis` playbooks (removed from active analysis per project memory); not used.
- Paper/monitor status: derivatives monitor writing ~352 rows/cycle across 5 venues (binance/bybit/hyperliquid/okx/mexc), healthy. No paper-portfolio status file consulted this run (out of scope for this slot).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-15 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_04 mtime ~1h old", "crypto swing report 33h old (expected cadence)", "monitors updating within minutes"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mixed", "chop", "risk_off"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: range/chop, BTC/ETH uptrend label but breadth 43.9%/46.3%, macro risk 100/100 risk-off (Iran/US strikes)", "stocks: risk_on, VIX 16.5, breadth 75%/100%, financials strongest sector"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 334/2000 mapped (16.7%), 83.3% unmapped", "2 active narrative baskets: perps_dex_narrative (HYPE), momentum_breakout (DODO, PUMP)", "UNH DOJ probe confirmed via news_items 2026-07-14"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["OI 24h% for most named movers shows n/a"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH: price up + OI up (fresh positioning)", "VANRY: negative funding, elevated crowding across venues", "ALLO: price down + OI down (deleveraging)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "entry_fresh", "stale_before_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZBT/DEXE/HEI already -9% to -34% 24h — late for fresh shorts without retest", "stocks pre-gate A basket (JPM/META/NVDA/PLTR/XLF/GOOGL/AMZN/COIN) untested until RTH confirmation"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 22 active (20 open_actionable, 2 waiting_for_entry), clean — no stale backlog beyond CLI limit", "stocks: 264 non-terminal signals in DB (only top 50 shown by CLI), 132 of them >24h past expiry without a terminal status — flagged as TODO, not asserted as closed/open"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ criminal probe into Medicare billing confirmed (Yahoo Finance, FierceHealthcare, 2026-07-14) + earnings 2026-07-16", "JPM: pre-gate A (score 100) demoted for stale-post-earnings setup — manual review required before use"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp playbook PF 0.44/-2.8R (n=41, low_confidence per playbook doc)", "crypto short direction PF 0.5, setup=breakdown PF 0.5, setup=breakout 0/7 wins PF 0.125", "crypto swing PF 1.39/+6.7R (best crypto bucket), weekend=Y PF 3.23 vs weekend=N PF 0.67", "stocks A/B headline n=10 weak-confidence PF 1.64; stocks C-tier n=206 PF 0.63 (expected — never actionable)"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.65,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of the eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "NVDA", "trigger": "RTH confirmation above 210.72 (pre-gate A, market-closed-only demotion) with SPY/QQQ holding uptrend at the open" },
    "best_short_candidate":    { "symbol": "DEXE/USDT", "trigger": "clean retest/rejection of prior support-turned-resistance after the current -9.3% 24h leg; avoid chasing the move already made" },
    "best_catalyst_candidate": { "symbol": "JPM", "trigger": "fresh post-earnings level recompute at/after the 09:30 ET open — do not use the pre-gate-A zone as-is (earnings-stale)" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "confirmed DOJ criminal probe into Medicare billing + earnings tomorrow (2026-07-16) — legal + event risk stacked" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.70 | mixed, chop, risk_off | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, entry_fresh, stale_before_entry | advisory_only |
| execution_lifecycle | caution | 0.75 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | manual_review | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (04:30)

- **UNH**: unchanged — still avoid (DOJ probe + earnings 07-16, now one day closer).
- **ZEC/TAO/HYPE** (04:30's long/short/catalyst picks): ZEC and TAO no longer feature in this cycle's top-movers/watch list; KAITO and PORTO have taken over the top RS-score slots (91.6 each). HYPE remains the primary of `perps_dex_narrative` basket, still no fresh entry structure.
- **New this cycle**: stocks pre-gate-A breadth (JPM/META/NVDA/PLTR/XLF/GOOGL/AMZN/COIN) is a materially wider risk-on stocks setup than the 04:30 review saw (which was overnight/no fresh RTH data) — this is the standout change into the US session.
- **FF/USDT** newly appears as an untracked legacy alert (see §14 TODO-1) — not present as an integrity issue in the 04:30 review.
- Crypto macro risk-off overlay (Iran/Strait of Hormuz headlines) persists unchanged from overnight.

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative across cycles): **2,000**; mapped (symbol present): **334 (16.7%)**; unmapped: **1,666 (83.3%)**.
- Narrative baskets: **2** active (`perps_dex_narrative` primary HYPE/USDT; `momentum_breakout` primary DODO/USDT, PUMP/USDT). A third basket (`delisting_thin_liquidity`) has no primary symbol.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped headlines (sample, non-symbol-tagged noise filtered): "Guidewire's CEO Sold $166,000 in Stock…", "Oil Climbs to a 1-Month High as the U.S. and Iran Trade Attacks in the Strait of Hormuz…", "SoundHound AI Stock Is Down 37% in 2026…".

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed / chop** — BTC/ETH labeled uptrend but breadth only 43.9% above EMA20; macro overlay is risk-off (100/100, Iran-US Strait of Hormuz strikes).
- Stocks mood: **risk-on (pre-market/planning)** — VIX 16.5, breadth 75%/100%, financials strongest sector (XLF RS +3.97% vs SPY 20d), semiconductors/materials/staples weakest.
- Dominant narrative: crypto — memes/AI mixed-heat, no dominant breakout theme; stocks — broad tech/mega-cap RS leadership (JPM, META, NVDA pre-gate A on relative strength + technical setup, not one specific news catalyst).
- Preferred side now: **wait-for-trigger** on crypto (chop + risk-off macro argues against chasing either side); **longs, RTH-confirmation required** on stocks (risk-on breadth is real but nothing is actionable until the cash open resets the market-closed gate).
- Best long candidate: NVDA (stocks, pre-gate A, watch — see §7).
- Best short candidate: DEXE/USDT (crypto, weak-vs-market with real volume confirmation — see §7).
- Best catalyst-backed candidate: JPM (stocks, highest pre-gate score of the session but earnings-stale — needs fresh levels, see §7).
- What to avoid: UNH (legal + earnings risk); chasing ZBT/USDT or HEI/USDT shorts that have already made most of their move without a retest; treating any of today's crypto C-tier watch names (DEXE 53.0, KAITO 52.2, ZEC 50.6) as tradeable — they are watchlist-only.
- What would change the view: a clean RTH open in stocks that holds SPY/QQQ uptrend for the first 15–30 min (confirms the risk-on breadth is real, not a pre-market gap trap); a crypto breadth improvement above ~55–60% over EMA20 or a de-escalation in the Iran/Strait of Hormuz headlines (would unlock more aggressive alt longs).

## 7. Candidate Deep Dives

### 1. JPM — stocks, long, catalyst/contradiction-risk (manual review)
- Score 100.0 (pre-gate A), demoted to C via two independent gates: `stale_post_earnings_setup` (verified earnings print 2026-07-14T11:57 ET, calendar lookup UNKNOWN — pre-earnings levels invalid) and `market_closed_intraday_planning_only`.
- Has price already reacted to the catalyst? Yes — the earnings print already happened; today's pre-gate levels were computed from pre-earnings structure and are stale.
- Chasing? Would be, if traded on the stale zone (341.33–343.04) as-is.
- Retest/pullback structure? Unknown until fresh post-earnings 1h/15m levels are recomputed at/after the open.
- Overextended? Cannot assess — data is stale by definition here.
- Actionable now? **No.** Needs fresh levels recomputed after RTH open before it can be treated as a real signal.
- Mood alignment: aligned with risk-on stocks mood; financials sector RS is genuinely strong (RS vs SPY 20d +3.97%).
- Side: long. Invalidation: recompute at open, do not use 339.61 (stale).
- Chase risk: high if used with today's stale levels.
- Catalyst confirmation/contradiction: earnings print confirmed (news-verified), but the setup itself is a contradiction risk (score says A, gate says manual review) — this is exactly the "A/B with contradiction risk" case this routine prioritizes.
- **Verdict: MANUAL REVIEW REQUIRED. Not actionable on current levels.**

### 2. UNH — stocks, avoid / manual review (existing exposure only)
- Confirmed via internal `news_items` (2026-07-14): "DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement" (FierceHealthcare) and "UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices" (Yahoo Finance).
- Earnings confirmed next session (days_ahead=1, i.e. 2026-07-16) — swing-blocked by earnings per the stocks report.
- Active tracker exposure: UNH intraday short C-tier (score 73.2, triggered) and UNH intraday long C-tier (score 80.0, tp1_hit) both still open in the tracker.
- Legal/headline risk: **LEGAL/HEADLINE RISK — DOJ criminal probe, confirmed 2026-07-14.**
- **Verdict: AVOID / MANUAL REVIEW. No new UNH exposure in either direction; existing tracker positions need human review given the DOJ + earnings stack.**

### 3. NVDA — stocks, long, best long-watch
- Score 91.43 (pre-gate A), demoted to C **only** by `market_closed_intraday_planning_only` — no stale-data or legal flag.
- Has price already reacted? 24h context shows semiconductors as the *weakest* sector (SMH RS vs SPY 20d -4.53%) even as NVDA individually scores high on RS/technical-setup components — a genuine stock-specific divergence from its sector, worth confirming isn't a single-name anomaly at the open.
- Chasing? Not yet — nothing has traded since this is a planning-only zone (210.72–211.80).
- Retest structure: to be confirmed at RTH open.
- Actionable now? No — planning/watchlist only until 09:30 ET.
- Mood alignment: aligned with stocks risk-on mood, but sector context (semis weak) argues for confirmation rather than an automatic chase at the open.
- Side: long. Invalidation: close beyond 209.63 (pre-gate, to be re-verified after open).
- Catalyst confirmation: no single dominant news catalyst — AI-chip-selloff headline exists (CryptoBriefing, "custom silicon threatens Nvidia's dominance") but is a **risk** note, not support; the setup is RS/technical, not catalyst-driven.
- **Verdict: WATCH. Best stocks long-watch for the session — require first-15-30min RTH confirmation before treating as live, given the sector divergence.**

### 4. FF/USDT — crypto, long, integrity flag + waiting_for_entry
- B-tier intraday long, score 68.5, status `waiting_for_entry`, entry zone 0.065592–0.066006, invalidation 0.065086.
- Flagged by `detect_untracked_legacy_alerts`: a Telegram alert was sent for FF/USDT at 2026-07-15T07:36:38Z with no matching tracked `proposed_signal` at detection time — it does now appear in `active-signals`, so this looks like a timing/registration lag rather than a fully orphaned alert, but it means this alert did **not** contribute to PF/winrate tracking. See §14 TODO-1.
- No internal news found for FF/USDT in the last 24h (checked `news_items`, no rows) — pure technical/RS setup, no catalyst backing.
- Actionable now? It's a live B-tier waiting-for-entry zone; treat as WAITING, not chased.
- **Verdict: WAITING for entry. Track the untracked-alert discrepancy separately (TODO), not a reason to distrust the signal itself.**

### 5. DEXE/USDT — crypto, short, best short-watch
- Bias short, score 81.1 (raw mover score, not a tier), 24h -9.29%, RS/BTC -12.99%, volume 1.45x (real volume confirmation, unlike several other weak-vs-market names showing 0.05-0.16x quiet volume).
- Has price already reacted? Yes — most of the -9.3% move already happened.
- Chasing? A fresh short at current price would be chasing the move already made.
- Retest/pullback structure? Needed — wait for a bounce/retest of the breakdown level rather than shorting the low directly.
- Overextended? Borderline — real volume confirms the move is not just illiquid noise, but entering without a retest risks poor R:R.
- Actionable now? **Not as a fresh chase.** Best treated as a short-watch pending a clean retest/rejection.
- Mood alignment: aligned with crypto's mixed/risk-off overlay (short bias makes sense given macro headwind), and matches the `crypto_failed_bounce_short` playbook (14d WR 40%, PF 2.00) rather than a raw breakdown chase.
- No internal news found for DEXE in the last 24h — pure technical/RS weakness, no catalyst.
- **Verdict: SHORT-WATCH. Wait for retest/rejection, not a chase of the already-made move.**

## 8. Best Candidates Ranked

1. **NVDA — long-watch (stocks)** — best long, RTH confirmation required, sector divergence to monitor.
2. **JPM — catalyst-watch / manual review (stocks)** — highest score of the session but earnings-stale; needs fresh post-open levels.
3. **DEXE/USDT — short-watch (crypto)** — best clean short, wait for retest not a chase.
4. **FF/USDT — waiting for entry (crypto)** — live B-tier zone, separate integrity note on the alert-tracking gap.
5. **UNH — avoid / manual review (stocks)** — DOJ + earnings risk stack, existing exposure needs human review.

No clean immediately-actionable trade exists in either asset class at 11:30 EEST (crypto: chop + risk-off macro; stocks: market closed). This is a **decision-window** read, not a system pause — scanning, tracking, and monitors continue unchanged.

## 9. Avoid / No Trade (this decision window only)

- UNH — confirmed legal risk + earnings tomorrow.
- Any fresh crypto short chase on ZBT/USDT (-33.85% 24h, already tagged `overextended`) or HEI/USDT (quiet 0.05x volume — thin, unreliable) without a retest.
- Any use of JPM's current pre-gate levels (341.33–343.04) — stale, earnings-invalidated.
- This is a no-new-entries read for the listed names only; the scanner, monitors, and scheduler continue running unchanged.

## 10. Main Risks

- Macro/geopolitical: Iran/US Strait of Hormuz escalation is the dominant crypto risk-off driver (macro risk 100/100) — a further escalation headline could pressure BTC/alts broadly regardless of technical setup.
- Catalyst mapping is running at 83.3% unmapped today — treat the catalyst layer as context only, not a decision input, until mapping improves (see TODO-2).
- Stocks tracker has a large (264 non-terminal, 132 >24h past expiry) backlog of unresolved statuses — doesn't block this review's verdicts (which use fresh report/agent-output data, not the stale tracker rows) but reduces confidence in any stocks PF/winrate stat that includes old unresolved rows (see TODO-3).
- Sector divergence on NVDA (individually strong vs. weak semiconductors sector) is a flag to watch at the open, not yet a red flag.

## 11. Action Plan — next 4 hours

- Watch NVDA, JPM, META, PLTR, XLF, GOOGL, AMZN, COIN at/after the 09:30 ET cash open for RTH confirmation of the pre-gate-A breadth; do not treat any of them as live before then.
- Watch DEXE/USDT for a retest/rejection structure before considering a short.
- Monitor FF/USDT and PENGU/USDT (both B-tier waiting_for_entry) for entry-zone touches.
- No new UNH exposure; flag existing UNH tracker rows for human review given the DOJ + earnings stack.
- Continue scanning/tracking as normal — no system changes.

## 12. Final Verdict per Mode

- Crypto scalp: no fresh ideas this cycle; existing scalp playbook remains low-confidence (PF 0.44) — treat any new scalp alert as research-grade only.
- Crypto intraday: no fresh A/B; FF/USDT and PENGU/USDT waiting_for_entry are the only live entries to watch.
- Crypto swing: report stale (33h); existing tracked swing positions (BTC, ETH, TAO, KAT, JST, APE, SENT, ALLO, PYTH, BCH) continue to be managed per their existing TP/SL — no new swing ideas this cycle.
- Stocks intraday: **planning/watchlist only** — market closed; pre-gate A breadth (JPM/META/NVDA/PLTR/XLF/GOOGL/AMZN/COIN) is the watchlist for the open.
- Stocks swing/invest (legacy): deprecated, not used. `stocks_swing_growth_breakout` (new framework): shadow-only research, 1 open candidate (AAPL, reclaim_after_shakeout) as of the last scan — not actionable.

## 13. Sources

- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement](https://www.fiercehealthcare.com) — FierceHealthcare, 2026-07-14 (internal `news_items`).
- [UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices](https://finance.yahoo.com) — Yahoo Finance, 2026-07-14 (internal `news_items`).
- UnitedHealth UNH Faces DOJ Probe Shares Dive 16% on Fraud Investigation — QuiverQuant, collected 2026-07-15T07:20:52Z (internal `catalyst_events.jsonl`, single_source).
- Internal: `data/processed/agent_outputs/20260715_073043_stocks_stock_trade_idea.json`, `20260715_073042_stocks_stock_scoring.json` (JPM/NVDA/META pre-gate tiers and cap reasons).
- Internal: `data/reports/intraday/2026-07-15_07-19_intraday_report.md`, `data/reports/stocks/intraday/2026-07-15_07-31_stocks_intraday_report.md`.
- No external WebSearch/WebFetch performed this run — all cited claims sourced from internal `news_items` / `catalyst_events.jsonl` / agent-output JSON, all <24h old and internally consistent.

## 14. Fix Requests / TODO

### TODO-1: FF/USDT untracked legacy alert
- **issue:** A Telegram alert for FF/USDT (B, intraday, score 68.5) sent at 2026-07-15T07:36:38Z has no matching `proposed_signal` per `detect_untracked_legacy_alerts`, even though FF/USDT now appears correctly in `active-signals` as `waiting_for_entry`. Looks like a registration-timing lag between the alert and the tracker write, not a fully orphaned alert.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-15` → 1 result (FF/USDT); cross-checked against `active-signals --asset-class crypto` which shows `sig_f7e08a4945ba4182 FF/USDT ... waiting_for_entry`.
- **suggested manual fix:** investigate the alert→proposed_signal write ordering/timing for this cycle; confirm whether this is a one-off race or a recurring pattern worth widening the detector's lookback window for.
- **priority:** low
- **first observed:** 2026-07-15 11:39 EEST

### TODO-2: Catalyst mapping weak (83.3% unmapped today)
- **issue:** `catalyst_events.jsonl` for today shows 334/2000 (16.7%) events mapped to a symbol; 83.3% unmapped. This has been a recurring theme in project memory (catalyst-linkage under-fires) but the raw rate today is worth a fresh look.
- **evidence:** direct count of `data/catalysts/2026-07-15/catalyst_events.jsonl` — mapped=334, unmapped=1666, total=2000.
- **suggested manual fix:** revisit the symbol resolver in the catalyst layer; consider whether generic "Motley Fool" style multi-ticker/analysis articles (which dominate the unmapped sample) should be filtered pre-ingest rather than counted against mapping rate.
- **priority:** medium
- **first observed:** 2026-07-15 11:39 EEST

### TODO-3: Stocks proposed_signals backlog past expiry without terminal status
- **issue:** 264 stocks `proposed_signals` rows are in a non-terminal status (`triggered`/`tp1_hit`/`tp2_hit`), far more than the 50 shown by default in `active-signals`. Of those, 132 have an `expires_at` more than 24h in the past (oldest dating to 2026-05-27) with no terminal status (`stopped`/`expired`/`tp3_hit`/final) recorded. Crypto has no equivalent backlog (22 non-terminal total, none hidden beyond the CLI limit).
- **evidence:** SQL: `SELECT count(*) FROM proposed_signals WHERE asset_class='stocks' AND status IN ('triggered','tp1_hit','tp2_hit')` → 264; same filtered to `expires_at < now()-24h` → 132, date range 2026-05-27 to 2026-07-10.
- **suggested manual fix:** investigate whether the pending-monitor's stocks coverage is failing to sweep old tp1_hit/tp2_hit/triggered rows to a final state, or whether this status set is intentionally left open-ended for stocks and the apparent "backlog" is expected — either way, `signal-stats` and PF/winrate figures that include these rows should be treated with reduced confidence until clarified.
- **priority:** medium
- **first observed:** 2026-07-15 11:39 EEST
