# Opus Enriched Review — US open reaction review — Auto Cycle 18:47 EEST

## 1. Executive Summary
Slot: **US open reaction review** (target 18:30 EEST / 11:30 ET, actual write ≈18:47 EEST, within tolerance). Advisory only — no auto-trade, no scoring/threshold changes. US cash session ~2h17min old: S&P +0.30%, Nasdaq +0.59% (semis/software rebound), Dow +0.11%, VIX ~14.9, tame CPI (3.4% YoY) plus strong AI-infra earnings reactions (CoreWeave, SuperMicro, Nebius +16.5%) driving the tape — regime reads **bullish/risk-on**, not chase-everything. TSM (last cycle's catalyst-watch) **confirmed**: +1.68% intraday vs SPY +0.30%, genuine outperformance on the July-revenue-beat catalyst. Crypto stayed in **chop with a risk-off macro overlay** (BTC/ETH downtrend, macro risk 100/100 on Harmony ONE exploit, XRP bridge hack, Aave bad debt, Iran/Strait-of-Hormuz tension); no A-tier and no fresh B-tier fired in either asset class this cycle — both intraday reports conclude "no trade, data does not justify a fresh idea." Catalyst mapping is **weak this run (73.96% unmapped, 651/2500 mapped)** — treat as context only. **Carried-forward system-integrity finding, still unresolved**: TUT/USDT and HEI/USDT (×2) open crypto swing longs remain `status=triggered` in the DB with invalidation levels that were confirmed breached as of the 16:19 review; a live price recheck was not possible this cycle (no fresh scan coverage on these symbols today), so the breach is **not re-quantified** but the underlying `status` has not changed — still flagged high-priority manual review. Stocks intraday: 0 actionable A/B after gates (47 raw-A/B demoted this cycle by the rolling 7-day drawdown guard, which the 14d diagnostic shows is net-protective: demoted-only cohort would have been −3.0R). CSCO earnings today; AMAT tomorrow — both blackout.

## 2. Data Used
- Reports: `2026-08-12_14-26_scalp_report.md` (~2h20min old), `2026-08-12_14-37_intraday_report.md` (~2h10min old), `2026-08-12_04-48_swing_report.md` (~10h55min old, **carry-forward**, beyond the 4h fresh cutoff but inside the 12h flag threshold — HOLO/USDT remains the swing desk's own best idea), `2026-08-12_15-37_stocks_intraday_report.md` (~5min old, fresh)
- `data/catalysts/2026-08-12/` — catalyst_events.jsonl (2500 rows), narrative_baskets.jsonl (3 baskets), catalyst_cycle_14-47.md (latest, 17:47 EEST)
- `data/processed/llm_analysis_packet.md` (14:37 UTC / 17:37 EEST), `data/processed/llm_stocks_packet.md` (15:30 UTC / 18:30 EEST)
- CLI: `active-signals` (crypto n=50, stocks n=50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-12` (clean — 0 untracked)
- Read-only SQLite query against `proposed_signals` for the 4 carried-forward invalidation-breach signal IDs (TUT/HEI×2/HOLO) — status unchanged (`triggered`), within the §A.1 read-only allowance
- Scheduler log tail (`scheduler.log`) — confirmed alive/fresh; noted a `CMD TIMEOUT: paper structural stop plan` at 17:56 EEST, part of a recurring but rotating pattern of non-fatal step timeouts today
- 2 WebSearch (TSM price/day-range; broad US market open recap) + 1 WebFetch (stockanalysis.com/stocks/tsm — confirmed live, TSM +1.68%) — internal news_items used first per source discipline; TSM is not in today's scored stocks universe (excluded upstream by `NO_ENTITY_RESOLVED_CATALYST` gate), so external check was the only way to close the loop on the prior review's explicit watch item
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-12_1619.md` (16:19 EEST, pre-US-open slot)

## 3. Scheduler / Data Freshness
- `scheduler.log` mtime 18:13 EEST (~34min old at review start) — **not deferred**. Latest cycle summary `cycle_06_13-30_summary.md` mtime 15:00 EEST (a live cycle 07 is running now, still mid-flight past the "stocks intraday report" step as of 18:13; not required for this review since both LLM packets and the newest stocks intraday report file are already fresh).
- Pending-monitor: log `pending_monitor_1786543364.log` last touched 17:10 EEST — alive within this cycle window.
- Stocks intraday report is ~5min old — fresh. Crypto scalp/intraday ~2h10-20min old — fresh (well inside the 2.5h cycle cadence). Crypto swing ~10h55min old — carry-forward, flagged.
- Stocks swing/invest reports remain from 2026-07-02 (stale, >14h) — **expected**: deprecated/removed playbooks, excluded from actionable set by design.
- Untracked-alert detector: **0** — no signal-reuse integrity issue this run.
- Scheduler step timeouts today (non-fatal, cycle continues): `paper structural TP refresh` (03:31), `paper stock direction` (06:46), `entry latency audit` (06:51, 14:16), `refresh obsidian dashboard` (08:01), `stocks pre-US review candidate bundle` (11:21), `paper portfolio ledger refresh` (14:24), `intelligence layer update` (14:32), `stocks intraday pullback VWAP hold` (14:47), `paper structural stop plan` (17:56) — 9 timeouts across 9 *different* steps today, none repeating back-to-back; pattern looks like general scheduler load/perf pressure rather than one broken step (see §14).

## 3A. Agent Council JSON
```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-12 18:47 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["live re-quantification of TUT/HEI/HOLO invalidation breach (no fresh per-symbol scan today)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 18:13 EEST, 34min old", "stocks intraday report 5min old", "crypto swing report 10h55min old (carry-forward)", "73.96% catalyst_events unmapped today"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.7,
      "reason_codes": ["risk_on", "risk_off", "chop", "shorts_preferred", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["stocks: bullish regime, VIX 14.88, all 4 indices uptrend, S&P +0.30%/Nasdaq +0.59% intraday", "crypto: range/chop, BTC/ETH downtrend, macro risk 100/100 risk-off overlay", "energy/healthcare/materials strongest stock sectors; utilities/communications/semis weakest"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["2500 catalyst_events, 651 mapped (26.04%) / 1849 unmapped (73.96%)", "TSM July revenue +45% YoY catalyst confirmed by today's +1.68% RTH move vs SPY +0.30%", "3 narrative baskets: binance_ecosystem_teaser, perps_dex_narrative, momentum_breakout"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["premarket/intraday RVOL for stocks candidates", "fresh derivatives read on TUT/HEI/HOLO this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/USDT price down + OI up: fresh shorts pressing, squeeze risk if reclaimed", "DODO/PROM/RARE negative funding across venues, crowding elevated"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "stale_before_entry", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["DODO/USDT best crypto watchlist name at 63.7/100, momentum_breakout=avoid_chase playbook", "KAITO/USDT still weakest mover, -26.72% 24h, >2 ATR from EMA20, do-not-chase", "TSM day range $427.02-$433.28 mid-session, already up meaningfully off the open"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.55,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: ~49 B-tier open (triggered/tp1_hit), 1 waiting_for_entry, 0 A-tier", "stocks: 0 A/B actionable, all 50 active rows are C-tier (review/shadow only)", "TUT/USDT + HEI/USDT x2 still status=triggered despite prior-confirmed invalidation breach"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["REGN/MSFT/INTU/BLK carry active legal/headline risk, never promotable", "CSCO earnings today, AMAT tomorrow — both blackout", "CRCL flagged stale_post_earnings_setup — earnings print confirmed but calendar shows UNKNOWN", "TUT/HEI invalidation-breach integrity gap unresolved"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier headline: PF 2.44, WR 16.4%, avgR 0.31, totalR +64.9 (week)", "crypto swing sub-mode strongest lane (avgR 0.49, totalR +45.4)", "stocks A/B headline: PF 0.0, 0W/3L, n=10 weak sample, avgR -0.5", "stocks intraday drawdown guard demoted-only cohort would have net -3.0R over 14d — guard appears net-protective right now"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "AMGN", "trigger": "watchlist only (C-tier, drawdown-guard demoted from A); would need the stocks_intraday_7d_drawdown_guard cohort to recover before any actionable promotion — track RTH follow-through in healthcare (today's strongest sector, XLV +3.80% RS/20d)", "reason": "base score 100, RS vs SPY +13.71%, RS vs sector +9.92%, classified RS leader, fresh 3-item news catalyst" },
    "best_short_candidate":    { "symbol": "KAITO/USDT", "trigger": "wait for a failed-bounce rejection back below 24h VWAP with confirmed bearish HTF structure; do not chase the existing breakdown (already >2 ATR from EMA20)", "reason": "still the weakest mover in today's universe, -26.72% 24h, weak_vs_market/breakdown/overextended tags" },
    "best_catalyst_candidate": { "symbol": "TSM", "trigger": "already confirming (+1.68% vs SPY +0.30% intraday) on the July revenue +45% YoY beat; not in today's scored universe (entity-resolution gate) so track manually, prefer a pullback/hold-above-VWAP entry over chasing the current extension", "reason": "genuine fresh material catalyst, now RTH-confirmed with real outperformance, semis/AI-infra tailwind (Nasdaq +0.59%, CoreWeave/SuperMicro reactions)" },
    "avoid_candidate":         { "symbol": "REGN / MSFT / INTU / BLK", "reason": "active class_action/securities_fraud legal risk — demoted A→C, never promotable regardless of score" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | mixed | 0.70 | risk_on, risk_off, chop, shorts_preferred, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.40 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, stale_before_entry, entry_late | advisory_only |
| execution_lifecycle | manual_review | 0.55 | open_actionable, waiting_for_entry, review_shadow, needs_review | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | ok | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review
Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-12_1619.md` (16:19 EEST, pre-US-open slot).
- **TSM confirmed**: the 16:19 review flagged TSM as INSUFFICIENT_DATA (genuine catalyst, no premarket RS data). This review's external check confirms real RTH outperformance: +1.68% vs SPY +0.30% at time of writing. Upgraded from catalyst-watch/pending to catalyst-watch/confirmed — still not in the scored universe (entity-resolution gate), so still not a scored/actionable idea, but the thesis held up.
- **PROM/USDT chase-risk unchanged**: still well past its entry zones; not re-checked in detail this cycle, no new information.
- **KAITO/USDT short-watch unchanged**: still the standing best short-watch, same setup, no new confirmation of a failed-bounce trigger yet.
- **TUT/HEI/HOLO invalidation-breach TODO carried forward, unresolved**: DB re-query this cycle confirms `status` is still `triggered` on all 4 signal rows (unchanged since 16:19). Could not re-quantify the live % breach this cycle (these symbols did not appear with fresh price data in today's 14:26/14:37 scalp/intraday scans) — treat the underlying integrity question as **still open**, not resolved and not worsened-or-improved on new evidence.
- **CRCL stale-post-earnings flag is new this cycle**: today's stocks intraday report flags CRCL with `stale_post_earnings_setup` — a verified earnings print exists in news_items but the earnings calendar still shows UNKNOWN for it, so pre-earnings levels are invalid. This is a fresh instance of a known pattern (earnings-calendar gaps) — see §14.
- **Market mood shifted mildly more constructive on stocks**: 16:19's read was "cautiously optimistic, not risk-on" pre-CPI-reaction; by 18:47 the confirmed RTH tape (S&P +0.30%, Nasdaq +0.59%, broad semis/software rebound, Nebius +16.5% on AI infra demand) supports calling it a real (if not euphoric) risk-on session.
- **Crypto regime unchanged**: still chop with a risk-off macro overlay; no new A/B fired since 16:19 in either scalp or intraday.
- Catalyst mapping: 73.96% unmapped now vs 72.65% at 16:19 — essentially flat, still weak.

## 5. Catalyst Coverage
- Total catalyst_events today: **2500** | mapped (symbol present): **651 (26.04%)** | unmapped: **1849 (73.96%)**
- Narrative baskets: **3** (binance_ecosystem_teaser, perps_dex_narrative, momentum_breakout)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped examples (from this cycle's file): earnings-call-transcript items missing symbol resolution (Global Industrial/GIC, Tanger/SKT, GXO, Fortune Brands Innovations/FBIN Q2 2026 earnings-call transcripts) — same root-cause family as the carried-forward `TODO-catalyst-symbol-misattribution`.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **chop**, risk-off macro overlay (macro risk 100/100 — Harmony ONE unauthorized-mint exploit, XRP Coreum-bridge hack ~200k XRP, Aave $195M bad debt from KelpDAO exploit, Iran/Strait-of-Hormuz tension, BTCPay exploit bounty). BTC/ETH both downtrend, altcoin breadth 57.5% >EMA20 (directionless, not broadly weak).
- Stocks mood: **bullish / risk-on (confirmed intraday)** — S&P +0.30%, Nasdaq +0.59%, Dow +0.11%, VIX ~14.9, tame CPI plus strong AI-infra earnings reactions (CoreWeave, SuperMicro, Nebius +16.5%) driving the tape; CSCO reports today, AMAT tomorrow (both blackout).
- Dominant narrative: crypto — `momentum_breakout` (DODO/PROM/RARE, no confirmed catalyst, avoid-chase) and `binance_ecosystem_teaser` (BNB/ASTER, aging); stocks — AI-infrastructure buildout confirmation (TSM, CoreWeave, SuperMicro) plus a broad semis/software rebound.
- Preferred side now: **longs for stocks, wait-for-trigger for crypto** — stocks: RTH-confirmed risk-on favors RS-leader longs in energy/healthcare (today's strongest sectors) once the drawdown guard allows it, still no actionable A/B this cycle; crypto: no clean side, prefer a confirmed KAITO/USDT failed-bounce short over any fresh long into chop/risk-off macro.
- Best long candidate: **AMGN** (stocks, watchlist-only, drawdown-guard demoted) — healthcare RS leader in today's strongest sector; no clean crypto long — HOLO/USDT remains flagged needs-review pending the invalidation-breach question.
- Best short candidate: **KAITO/USDT** (crypto) — wait for failed-bounce rejection, do not chase the current breakdown; no clean stocks short this cycle (all short C-tier candidates are watchlist-only under the same drawdown guard).
- Best catalyst-backed candidate: **TSM** (stocks) — RTH-confirmed (+1.68% vs SPY +0.30%) on the July-revenue-beat catalyst; not in the scored universe (entity-resolution gate), so still not actionable via the desk's own pipeline — track manually.
- What to avoid: REGN/MSFT/INTU/BLK (legal risk), AMAT/CSCO (earnings blackout), CRCL (stale post-earnings setup, invalid pre-earnings levels), chasing PROM/USDT or the current KAITO/USDT breakdown candle, treating TUT/HEI/HOLO as clean open positions until the invalidation-breach question is resolved.
- What would change the view: a human confirmation (or fix) on the TUT/HEI/HOLO invalidation/stop-check integrity question; the drawdown guard cohort recovering enough to let a stocks A/B through; a clean pullback/retest on TSM or a KAITO/USDT failed-bounce structure forming.

## 7. Candidate Deep Dives

### 1. TSM (stocks, catalyst-watch — confirmed this cycle)
- Not in today's scored stocks universe (excluded upstream by `NO_ENTITY_RESOLVED_CATALYST` hard gate per the 16:19 review's pre-US overlay run), so no internal score/tier this cycle.
- Catalyst: internal news_items carried the July revenue +45% YoY beat (confirmed at 16:19); this cycle's external check (WebFetch, stockanalysis.com) confirms live RTH price action: **+1.68%** intraday, day range $427.02-$433.28, clearly outperforming SPY's +0.30% same-session move.
- Has price already reacted? Yes, and it's continuing — this is now a "confirmed, not chasing the open print" situation rather than a fresh trigger.
- Chasing risk: moderate — the stock is already meaningfully extended off the pre-market reference; a fresh entry at the current level is closer to chasing than confirming. Prefer a pullback/hold-above-VWAP structure.
- Aligned with market mood? Yes — broad semis/AI-infra risk-on tape supports the move.
- Actionable level: none scored by the desk (gate exclusion) — this is manual/advisory tracking only, never Telegram-actionable via this pipeline today.
- TradingView/manual chart check unavailable — using WebFetch quote data only, no intraday chart structure.

### 2. TUT/USDT, HEI/USDT ×2 (crypto, needs-review — invalidation-breach anomaly, carried forward)
- `sig_e4875989af64bab7` (TUT, invalidation 0.09882), `sig_a4e763ceaf1df917` (HEI, invalidation 0.18750), `sig_2f2c8c4a003b4a97` (HEI, invalidation 0.18323) — all three re-queried directly against `proposed_signals` this cycle: **all still `status=triggered`**, unchanged from the 16:19 confirmed-breach finding.
- Could not re-quantify the live % breach this cycle: none of these three symbols appear with fresh price data in today's 14:26 scalp or 14:37 intraday reports (they are swing-mode names, and today's swing report is the same 04:48 snapshot already used at 16:19). No live-price CLI tool is in this run's allowed command set.
- Verdict unchanged: **manual review required** — this is a system-integrity question about the invalidation/stop-check job for `triggered`-status swing signals, not a new entry decision. Do not add to any of these three names until resolved.
- TradingView/manual chart check unavailable — local OHLCV/report fields only, and none were fresh for these three symbols this cycle.

### 3. KAITO/USDT (crypto, short-watch, carried forward)
- Score 94.2 (16:19 snapshot; not independently re-scored this cycle since no A/B fired), 24h **-26.72%** per this cycle's llm_analysis_packet "Lower-Cap / Expanded Universe Leaders" — still the weakest mover in the universe. Tags: weak_vs_market, overextended.
- Has price already reacted? Yes, sharply — breakdown already well underway.
- Chasing? Yes at current levels — more than 2 ATR from EMA20 per the standing flag; do not short the current candle.
- Retest structure needed: confirmed bearish HTF structure + a clear stop above the recent swing high before entering; squeeze risk exists if shorts get crowded and price reclaims.
- Aligned with market mood? Yes — crypto chop/risk-off macro favors clean shorts on failed bounces over fresh longs.
- Catalyst confirmation/contradiction: none — pure momentum/RS-driven.
- TradingView/manual chart check unavailable — local OHLCV/report fields only.

### 4. AMGN (stocks, long-watch, watchlist-only)
- Pre-gate tier A (base_score 100.0), demoted to C this cycle by `stocks_intraday_7d_drawdown_guard` + `stocks_intraday_long_guard` — rolling paper-R drawdown guard, not a data-quality issue.
- Thesis: RS vs SPY (20d) +13.71%, RS vs sector (XLV) +9.92%, classification "leader," 3 fresh news catalysts in lookback window, earnings safe (no event in the near window, next earnings 2026-11-03).
- Healthcare (XLV) is today's #2 strongest sector (RS vs SPY 20d +3.80%), reinforcing the sector-alignment case.
- Has price already reacted? Entry plan was 414.28-415.71 as of the 15:22 UTC agent snapshot; no fresher intraday quote confirmed this cycle (not in this session's allowed live-quote toolset).
- Chasing risk: unknown without a fresh quote — treat as watchlist only regardless, since the guard blocks actionability independent of price level.
- Actionable level: none — this stays watchlist/paper-only until the 7-day drawdown-guard cohort recovers; the 14d diagnostic (`Would-have-been-A/B ... demoted-only net -3.0R`) suggests the guard is currently doing its job, so do not treat this as an unfair block.
- Legal/headline/earnings check: none found for AMGN.

### 5. CRCL (stocks, integrity flag — new this cycle)
- Flagged `stale_post_earnings_setup` in today's 15:37 UTC stocks intraday report: news_items confirms an earnings print at 2026-08-12T09:40:59-04:00, but the earnings calendar source still shows CRCL as UNKNOWN, so the pre-earnings entry levels are treated as invalid pending fresh post-earnings levels.
- Base score 91 (was pre-gate A), tier now C — correctly conservative given the calendar gap, no criticism of the demotion itself.
- Actionable level: none — manual review required to regenerate levels off the post-earnings price structure; do not use the stale pre-earnings entry/invalidation numbers if this symbol is manually revisited.
- This is a fresh instance of a recurring pattern (earnings-calendar coverage gaps) — logged as a TODO (§14) rather than fixed here.

## 8. Best Candidates Ranked
1. **TSM catalyst-watch, confirmed** (stocks) — RTH-confirmed outperformance (+1.68% vs SPY +0.30%) on a genuine fresh catalyst; not scored by the desk pipeline (entity-resolution gate), so manual-track only. Invalidator: loses the SPY/sector RS edge or fails to hold above intraday VWAP.
2. **KAITO/USDT short-watch** (crypto) — wait for a failed-bounce rejection below 24h VWAP with confirmed bearish HTF structure; do not chase the current candle. Invalidator: a reclaim/close back above the recent swing high.
3. **AMGN long-watch, guard-blocked** (stocks) — cleanest fundamentally-aligned long in today's strongest sector (healthcare), but structurally watchlist-only until the drawdown guard cohort recovers. Invalidator: loses RS leadership vs XLV/SPY.
4. **DODO/USDT watchlist** (crypto) — the crypto desk's own best current name at 63.7/100, but the routed playbook is explicitly `avoid_chase` / `wait_pullback`. Invalidator: no clean pullback/retest forms.
5. **BNB/USDT catalyst-watch** (crypto) — `binance_ecosystem_teaser` basket, now aging past <6h into <24h; wait for a clean breakout or pullback with volume, do not chase the initial move.

## 9. Avoid / No Trade
This applies to the current decision window only — never a command to stop scanning, tracking, or the scheduler.
- **REGN, MSFT, INTU, BLK** (stocks) — active class_action/securities_fraud legal risk, never actionable regardless of score.
- **AMAT, CSCO** (stocks) — earnings blackout today/tomorrow, do not chase into the print.
- **CRCL** (stocks) — stale post-earnings setup, pre-earnings entry/invalidation levels are invalid until regenerated.
- **Chasing TSM** at the current extended level — prefer a pullback/VWAP-hold structure over the open print.
- **Chasing KAITO/USDT's current breakdown candle** and **PROM/USDT** at its extended level — wait for structure, not the initial move.
- **TUT/USDT, HEI/USDT** as "clean open positions" — both remain past their stated invalidation with `status=triggered` unchanged; treat as needs-review, not validated risk, until a human confirms the stop logic.

## 10. Main Risks
- **Invalidation-monitoring integrity gap (carried forward, unresolved)**: TUT/USDT and HEI/USDT (×2) open longs remain `status=triggered` in the DB despite the 16:19 review's confirmed invalidation breach; this cycle could not re-verify the live % breach (no fresh price coverage for these symbols today) but the underlying `status` field is unchanged, meaning the gap has not been addressed. This affects the trustworthiness of every "active signals" risk read.
- **Catalyst mapping weak** (73.96% unmapped) — treat catalyst layer as context only this cycle.
- **Recurring, rotating scheduler step timeouts**: 9 different steps timed out today (non-fatal, cycle always continued) — no single broken step, but the breadth of the pattern suggests general load/performance pressure worth a capacity check.
- **Earnings-calendar coverage gap resurfaced** (CRCL `stale_post_earnings_setup`) — same known-pattern family as prior earnings-calendar TODOs.
- **Geopolitical overhang unchanged**: Iran/Strait-of-Hormuz tension, active exploit/hack headlines (Harmony ONE, XRP bridge, Aave/KelpDAO) — live tail risk for crypto risk appetite specifically.

## 11. Action Plan — next 4 hours
- Stocks: watch AMGN/XOM/SMCI/other guard-demoted C-tier names for whether the rolling 7-day drawdown guard cohort recovers; do not treat any of them as actionable until it does. Track TSM manually for a pullback/VWAP-hold entry rather than chasing the current extension.
- Crypto: watch for a KAITO/USDT failed-bounce short setup; avoid fresh longs into the chop/risk-off macro overlay; DODO/USDT and BNB/USDT remain the closest watchlist names, both wait-and-confirm.
- Do not add to TUT/USDT, HEI/USDT, or HOLO/USDT until a human confirms whether the invalidation breaches are a real stop-logic bug or a display/monitoring lag (see §14).
- CSCO reports earnings today — do not treat any CSCO signal as tradeable pre/post-print; AMAT reports tomorrow, same rule applies from now.
- If the rotating scheduler-timeout pattern (§10) continues into the next 1-2 cycles on the same or new steps, escalate the capacity question in the next review's §14.

## 12. Final Verdict per Mode
- **Crypto scalp**: no trade — report's own final summary: "data does not justify a fresh idea right now."
- **Crypto intraday**: no trade — best watchlist name DODO/USDT at 63.7/100, avoid-chase playbook, wait for cleaner execution.
- **Crypto swing**: strongest lane by 14d stats (avgR 0.49, totalR +45.4 this week) but the one open idea (HOLO/USDT) needs the invalidation question resolved before treating as clean; the standing report-level idea is otherwise unchanged.
- **Stocks intraday**: 0 actionable A/B after gates this cycle (47 raw-A/B demoted by the rolling drawdown guard) — the guard's 14d diagnostic shows it net-protective right now (demoted-only cohort would have been −3.0R), so this is guard-working-as-intended, not a false block. Regime is bullish/risk-on and TSM confirmed today's best external catalyst story, but neither is scored-actionable via this pipeline this cycle.
- **Stocks swing/invest**: excluded — deprecated/stale data source, not evaluated.
- **System integrity**: manual review still required on the TUT/HEI/HOLO invalidation-breach finding (unresolved, carried forward 3rd cycle in a row: 11:39 suspicion → 16:19 confirmed → 18:47 unchanged).

## 13. Sources
- [Taiwan Semiconductor Manufacturing Company (TSM) Stock Price & Overview — stockanalysis.com](https://stockanalysis.com/stocks/tsm/) (fetched live via WebFetch, confirmed +1.68% intraday, day range $427.02-$433.28)
- [Taiwan Semiconductor Stock Price Today | NYSE: TSM Live — Investing.com](https://www.investing.com/equities/taiwan-semicond.manufacturing-co)
- [Taiwan Semiconductor Manufacturing Company Limited (TSM) — Yahoo Finance](https://finance.yahoo.com/quote/TSM/)
- [Stock Market Today (Aug. 12, 2026): S&P 500 climbs following key inflation report — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-12-2026) (WebFetch returned 403; not used beyond the search snippet)
- Internal: `data/reports/scalp/2026-08-12_14-26_scalp_report.md`, `data/reports/intraday/2026-08-12_14-37_intraday_report.md`, `data/reports/swing/2026-08-12_04-48_swing_report.md`, `data/reports/stocks/intraday/2026-08-12_15-37_stocks_intraday_report.md`, `data/catalysts/2026-08-12/catalyst_cycle_14-47.md`
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-12_1619.md`

## 14. Fix Requests / TODO

### TODO-invalidation-breach-no-status-change (carried forward, unresolved 3rd cycle)
- **issue:** Three open crypto swing longs continue trading (per the 16:19 review's confirmed finding) through their own stated invalidation level while `status` still reads `triggered`: **TUT/USDT** `sig_e4875989af64bab7` (invalidation 0.09882), **HEI/USDT** `sig_a4e763ceaf1df917` (invalidation 0.18750) and `sig_2f2c8c4a003b4a97` (invalidation 0.18323). This run re-queried `proposed_signals` directly and confirms the `status` field is unchanged since 16:19 — the underlying gap has not been addressed. Could not re-quantify the live % breach this cycle (no fresh price coverage for these symbols in today's scalp/intraday reports, and no live-price CLI tool is in this run's allowed set).
- **evidence:** Read-only SQLite query against `db/crypto_ai_desk.sqlite` `proposed_signals` this run (18:47 EEST) returned `status=triggered` unchanged for all three rows vs the 16:19 review's confirmed-breach snapshot.
- **suggested manual fix:** Same as 16:19's TODO — audit the invalidation-check/stop-monitor job for crypto swing-mode `triggered` rows; confirm it runs per-tick against the correct OHLCV feed/timeframe, not just for `waiting_for_entry` rows. Cross-check against the ZBT/ACE bias-tag-contradiction fix history (escalated 2026-08-08) to see if that fix only touched display labels, not the underlying stop-check path.
- **priority:** high — unresolved for 3 consecutive reviews now (11:39 suspicion → 16:19 confirmed → 18:47 unchanged); directly affects the trustworthiness of every "active signals" risk read.
- **first observed (this exact confirmed form):** 2026-08-12 16:19 EEST; unchanged as of 2026-08-12 18:47 EEST (this run); precursor suspicion 2026-08-12 11:39 EEST.

### TODO-scheduler-rotating-step-timeouts
- **issue:** 9 different scheduler steps timed out today (non-fatal, `CMD TIMEOUT`, cycle always continued): `paper structural TP refresh`, `paper stock direction`, `entry latency audit` (×2), `refresh obsidian dashboard`, `stocks pre-US review candidate bundle`, `paper portfolio ledger refresh`, `intelligence layer update`, `stocks intraday pullback VWAP hold`, `paper structural stop plan`. No single step repeats back-to-back, suggesting general load/performance pressure across the cycle rather than one broken command.
- **evidence:** `data/scheduled_runs/2026-08-11_default_schedule/scheduler.log`, `grep "CMD TIMEOUT"` — 9 distinct ERROR lines spanning 03:31 EEST through 17:56 EEST on 2026-08-12.
- **suggested manual fix:** Review per-step timeout thresholds and whether the cycle is running long enough (cycle_06 alone ran ~13:30→15:00+) that later steps are starved of wall-clock budget; consider whether any of these steps can run in parallel or on a longer allowance, or whether host resource contention (CPU/IO) during the cycle is the root cause.
- **priority:** medium — no visible tracking/data failures yet since each step is non-fatal, but the breadth (9 different steps) is a pattern worth catching before something time-sensitive (e.g. the stop-monitor job related to the TODO above) starts missing its window.
- **first observed:** 2026-08-12 18:47 EEST (this run, aggregated from today's full log).

### TODO-earnings-calendar-gap-crcl
- **issue:** CRCL shows a verified earnings print in `news_items` (2026-08-12T09:40:59-04:00) but the earnings calendar source still returns UNKNOWN for it, forcing the desk to correctly mark it `stale_post_earnings_setup` and invalidate its pre-earnings levels. This is a fresh instance of the earnings-calendar coverage-gap pattern.
- **evidence:** `data/reports/stocks/intraday/2026-08-12_15-37_stocks_intraday_report.md`, line ~426: "CRCL (long) (was A): score 91 · watchlist / not actionable — tier demoted A→C: stale_post_earnings_setup ... verified earnings print (2026-08-12T09:40:59-04:00) while calendar is UNKNOWN."
- **suggested manual fix:** Audit the earnings-calendar ingest/coverage for CRCL specifically (recent IPO/spin-off names are the usual gap case) and check whether the calendar source needs a manual backfill or a broader coverage-provider fix.
- **priority:** medium — the demotion behavior is correct (fail-conservative), so no incorrect trade risk, but the coverage gap itself should be closed.
- **first observed:** 2026-08-12 18:47 EEST (this run).

### TODO-catalyst-symbol-misattribution (carried forward, unchanged)
- **issue:** Catalyst mapping remains weak (73.96% unmapped today vs 72.65% at 16:19, 71.7% at 11:39) — the underlying unmapped rate has not improved across three reviews today.
- **evidence:** This run's mapped/unmapped count (651/1849 of 2500) vs the 16:19 review's (547/1453 of 2000); today's top unmapped examples are again earnings-call-transcript sources (Global Industrial/GIC, Tanger/SKT, GXO, Fortune Brands Innovations/FBIN) missing symbol resolution.
- **suggested manual fix:** Audit the earnings-call-transcript source path's symbol resolver (unchanged suggestion from the 11:39/16:19 reviews).
- **priority:** high (unchanged).
- **first observed:** 2026-08-12 11:39 EEST; still open at 18:47 EEST.
