# Opus Enriched Review — late-session risk review — Auto Cycle 21:39 EEST

## 1. Executive Summary

Slot: **late-session risk review (21:30 EEST)** — US session is ~5h into RTH, checking exposure and lifecycle status, not hunting fresh entries. Advisory only — no auto-trade, no scoring/threshold changes.

Reports fresh: crypto intraday (20:29 EEST, ~1h10m), crypto scalp (20:23, ~1h16m), stocks intraday (21:34, ~5min — very fresh, post-open snapshot). Swing report is now **~17h old (04:30 generation) — stale**, excluded from fresh-idea consideration, carried forward only for already-open position context.

Crypto stays mixed: BTC/ETH uptrend, altcoin breadth 76.3% > EMA20, but the **macro risk-off overlay (100/100) from the Iran/Israel escalation and Hormuz/oil risk persists unchanged** through the whole day (04:40 → 11:39 → 16:29 → now). No reversal evidence — crypto continuation, not rollover. Stocks regime **improved from risk_off (pre-open) to chop/neutral (RTH)**: breadth above EMA20 moved from 0% → 50%, VIX eased to 17.13. Still **zero A/B-tier actionable stocks setups this cycle** (0 actionable after gates, same as pre-open) — everything on the board is C-tier research.

Best long-watch: **ONDO/USDT** (RWA-basket catalyst-backed B-tier, RS+10% vs BTC, not extended). Best short-watch: **NVDA** (C-tier only; RTH-confirmed short reaction, score 87.8 vs long 51.7, but not actionable — needs A/B gate clearance). Best catalyst-backed: **ONDO/USDT** (same pick — RWA narrative basket, fresh <6h). Avoid: **UNH** (live DOJ criminal-probe/Medicare-fraud risk, technical A-tier score irrelevant) and **BONK/USDT** (active exploit drainer). Caution/manage-only: **ERA/USDT** (+61% 24h, textbook chase-risk repeat idea — do not add at current levels).

The scheduler data-quality anomaly flagged at 16:29 (dry-run-only log, no real cycle summary) is **resolved** — `cycle_09_20-15_summary.md` (20:51 EEST) confirms a real cycle ran. The untracked-alert bug (signal_id reuse, [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]-class) fired **2 more times** since 16:29 (OPN/USDT 17:26, ZAMA/USDT 18:40) — 8 total today, unresolved TODO-3, logged again in §14.

## 2. Data Used

- Reports: crypto intraday (2026-07-21_17-29, fresh ~1h10m), crypto scalp (2026-07-21_17-23, fresh ~1h16m), stocks intraday (2026-07-21_18-34, fresh ~5min)
- Crypto swing: 2026-07-21_01-30 report — **~17h old, stale**, excluded from fresh candidates, used only for open-position carry-forward context
- Stocks swing/invest: last dated 2026-07-02 (19 days) — excluded, deprecated framework per [[project_crypto_ai_desk_stocks_position_framework]]
- Catalyst layer: `data/catalysts/2026-07-21/` — `catalyst_cycle_17-31.md` (latest, 20:31 EEST), `catalyst_events.jsonl` (3,475 events today), `narrative_baskets.jsonl`
- LLM packets: `llm_analysis_packet.md` (20:30 EEST), `llm_stocks_packet.md` (20:46 EEST)
- CLI: `active-signals` (crypto ×27, stocks ×50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-07-21`
- Direct computation of catalyst mapping ratio from `catalyst_events.jsonl` (3,475 total events, symbol-field presence)
- Heartbeat: `data/autostart/heartbeat_state.json` — last OK 2026-07-21T17:37:35Z (~1h02m ago EEST-relative), last warn 2026-07-20T12:57Z (>24h ago, stale warn)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-21_1629.md` (pre-US-open slot)
- **External web research not invoked this run** — internal `news_items`/report catalyst data for every candidate (ONDO RWA basket, ERA momentum, NVDA earnings-adjacent tech context, UNH DOJ probe, BANK/USDT squeeze) was fresh (<1h–6h), internally consistent, and already source-attributed in the reports; per §G this satisfies the internal-first bar without a fresh WebSearch/WebFetch pass.

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-07-20_default_schedule/scheduler.log`: mtime 20:51 EEST (~48 min ago) — **fresh**.
- Latest real cycle summary: `cycle_09_20-15_summary.md` (20:51 EEST, ~48 min old) — **fresh, confirms the 16:29-review data-quality anomaly (dry-run-only log) is resolved**; a real cycle executed and wrote a summary this time.
- Heartbeat: OK 2026-07-21T17:37:35Z (~1h02m ago); no active warn (last warn >24h stale). Monitor alive.
- Crypto scalp/intraday reports: fresh (~1h10–1h16m).
- Stocks intraday report: very fresh (~5min, genuine post-open RTH snapshot, not a pre-open estimate).
- Crypto swing report: **stale (~17h)** — excluded from fresh candidate selection; any swing idea from that report should be treated as carry-forward only, not re-verified today.
- Stocks swing/invest: **stale (19 days)**, excluded — deprecated framework.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-21 21:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest fresh data (deprecated, excluded)", "TradingView/chart MCP not loaded", "liquidation heatmaps / order book depth / on-chain flows (never automated)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle_09_20-15_summary.md both mtime 20:51 EEST (~48min)", "crypto intraday/scalp reports ~1h10-1h16m fresh", "stocks intraday report ~5min fresh (genuine RTH snapshot)", "crypto swing report ~17h old (stale, excluded)", "heartbeat OK 17:37:35Z (~1h02m ago)"] },
    { "agent": "market_regime", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["risk_on", "mixed", "chop", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 76.3% breadth>EMA20, style=selective longs prefer pullbacks on RS", "macro risk 100/100 risk-off overlay unchanged all day (Iran/Israel, Hormuz, oil)", "stocks regime improved risk_off(pre-open)->chop/neutral(RTH): breadth 0%->50%>EMA20, VIX 17.13", "0/4 stock indices trending, all range-bound"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "catalyst_contradicted"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 3475 total, 794 mapped (22.8%), 2681 unmapped (77.2%) -> mapping weak this run", "rwa_narrative basket fresh <6h, primary ONDO/USDT+XLM/USDT", "momentum_breakout basket fresh <1h, primary ONDO/ALLO/CRCLB", "ADA/BNB/ETH/SOL carrying exploit_hack risk flags (Wanchain/Allbridge bridge exploits)", "UNH/MSFT carrying legal_risk flags (DOJ sec_doj / securities_fraud)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "funding_extreme", "oi_supports"],
      "data_missing": ["liquidation heatmap", "order book depth/CVD"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ERA/USDT: funding -0.0113 (negative/crowded shorts), 24h move +61%, OI n/a on primary venue", "BANK/USDT: -38.6% 24h, OI down 20.4% (deleveraging), capped to C via high_upper_wick_short_squeeze_risk", "LA/USDT, DEXE/USDT: negative funding across venues, crowding elevated per cross-check"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chase_risk", "overextended", "entry_fresh", "clean_retest"],
      "data_missing": ["chart/TradingView MCP not loaded — no manual chart confirmation"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ERA/USDT +61% 24h, price 0.0996 vs planned pullback entry 0.0934-0.0977 (modest pullback only, still a blow-off move)", "ONDO/USDT price 0.3964 vs pullback entry 0.3904-0.3946, not extended (RS+10%, vol 0.32x)", "no-catalyst intraday momentum playbook stat: 14d WR 23% / PF 0.70 / -3R — both ONDO and ERA ride this playbook"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 27 active signals — 22 open/managed (10 tp1_hit + 12 tp2_hit), 3 entered-unresolved (triggered), 2 waiting_for_entry", "ONDO/USDT scalp waiting_for_entry expires ~22:26 EEST (<1h left) — likely to lapse NO-ENTRY", "stocks: 0 A/B actionable; NVDA short (C-tier, score 87.8) shows status=triggered with expires_at already in the past (18:03 EEST) — status/expiry mismatch, flagged NEEDS REVIEW not a live trade"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ/sec_doj legal risk, tier demoted A->C, manual review required", "MSFT: securities_fraud legal risk, tier demoted B->C", "BONK/ETH/SOL/ADA/BNB carrying exploit_hack operator-review flags", "8 untracked legacy watchlist alerts today (no backing proposed_signal) -> tracking integrity gap"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto headline A/B (week): n=167, winrate 35.6%, PF 1.84, avgR 0.27 -- working overall", "crypto scalp mode: PF 0.72, avgR -0.10, n=39 -- losing bucket, mode kill-switched in production", "crypto direction=short: PF 0.125, 0 wins/6 losses, n=8 -- avoid new crypto shorts", "stocks headline A/B: n=7 anecdotal, PF 1.50 but winrate 28.6%; stocks C-tier: PF 0.895, negative", "stocks direction=short PF1.25 (positive) vs long PF0.708 (negative) this week -- shorts working better in stocks, but 0 A/B actionable to exploit it"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "ONDO/USDT", "trigger": "pullback fill into 0.3904-0.3946 on 15m, invalidation 1h close below 0.3853", "reason": "RWA-basket catalyst-backed (fresh <6h), RS+10% vs BTC, not extended, B-tier actionable" },
    "best_short_candidate":    { "symbol": "NVDA", "trigger": "C-tier only -- becomes watch-actionable only if a future cycle clears SI-1..5 gates (market_context, sector_confirmation, liquidity rvol) with a fresh RTH candle re-confirming below ~205", "reason": "RTH reaction favored the short side today (score 87.8 vs long 51.7) but the specific signal instance has an expiry/status mismatch -- treat as directional color, not a live trade" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "same as long candidate -- rwa_narrative basket fresh <6h", "reason": "cleanest catalyst-technical alignment on the board this cycle" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "active DOJ criminal-probe/Medicare-fraud investigation overrides an 86.55 raw A-tier score; never a clean actionable regardless of technicals" },
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
| market_regime | ok | 0.75 | risk_on, mixed, chop, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.5 | squeeze_risk, funding_extreme, oi_supports | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, overextended, entry_fresh, clean_retest | advisory_only |
| execution_lifecycle | caution | 0.7 | open_actionable, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.7 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.7 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (16:29 pre-US-open)

- **Resolved**: scheduler data-quality anomaly (dry-run-only log at 16:29) — a real cycle (`cycle_09_20-15_summary.md`) has since run and written a summary.
- **Stocks regime improved**: risk_off (pre-open, breadth 0%>EMA20, VIX 17.72) → chop/neutral (RTH, breadth 50%>EMA20, VIX 17.13). Still 0 A/B actionable stocks setups both times — regime improvement did not translate into actionable setups.
- **NVDA**: was "short-watch, needs RTH confirmation" at 16:29 → RTH did confirm short bias more strongly (score 87.8 short vs 51.7 long) but the specific tracked signal instance now shows an expiry-already-passed / status ambiguity — downgraded from "confirmed short-watch" to "needs review, directional color only."
- **Untracked-alert bug**: 5 total at 16:29 → **8 total now** (OPN/USDT 17:26, ZAMA/USDT 18:40 added since). Same unresolved TODO-3.
- **ERA/USDT, ONDO/USDT**: both were flagged "manage existing position, no fresh chase" at 16:29 (ERA +60.4% 24h then) — now ERA is +61.2%, essentially unchanged/still extended, same guidance holds. ONDO is effectively unchanged too (RS+10% both times).
- **UNH**: legal-risk avoid call from 16:29 remains valid and unchanged — DOJ probe still cited in today's stocks report.
- Catalyst mapping: 22.8% mapped today (77.2% unmapped) — consistent with the "weak mapping" pattern noted in recent reviews; use catalyst layer as context, not confirmation.

## 5. Catalyst Coverage

- Total catalyst events today: **3,475**
- Mapped (non-null symbol): **794 (22.8%)**
- Unmapped (null symbol): **2,681 (77.2%)**
- Narrative baskets: **5** active this cycle (binance_ecosystem_teaser, rwa_narrative, ai_narrative, perps_dex_narrative, momentum_breakout)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped-symbol headline types (delisting/exchange-ops notices, not trade-relevant):
- "MEXC to Delist STM and WULF USDT-M Stock Futures #Delistings"
- "Delisting of UTYAUSDT Perpetual Futures Pair [Jul 23, 2026, 13:00 UTC]"
- (majority of unmapped volume is exchange-ops/delisting noise and general macro wire copy without a ticker match — not a scoring-relevant gap today)

## 6. Market Landscape

BTC/ETH remain in an uptrend with broad altcoin participation (76.3% > EMA20), but the desk's own macro layer has held a **100/100 risk-off score all day** on Iran/Israel/Hormuz escalation and oil-price risk — an unusual, prolonged divergence between technical risk-on and geopolitical risk-off that has not resolved either direction. Stocks improved from an ugly pre-open snapshot (0% breadth, VIX 17.72) to a merely choppy RTH session (50% breadth, VIX 17.13, all 4 indices range-bound) — energy/healthcare/financials are the relative-strength leaders, semis/tech are the relative laggards. Neither market produced a genuine A-tier idea today.

### Market Mood / Risk Routing

- Crypto mood: **mixed** (technical risk-on / macro risk-off overlay, unresolved all day)
- Stocks mood: **chop** (neutral bias, VIX 17.13, breadth 50%, 0/4 indices trending)
- Dominant narrative: RWA/tokenization (ONDO/XLM) and AI-sector rotation (NEAR/RENDER/TAO/FET) in crypto; energy/healthcare/financials relative strength in stocks
- Preferred side now: **longs** in crypto (selective, RS-leader/catalyst-backed only, per working intraday PF2.08); **wait-for-trigger** in stocks (0 A/B all session, chop regime)
- Best long candidate: **ONDO/USDT** — pullback entry 0.3904-0.3946, invalidation 1h close < 0.3853
- Best short candidate: **none clean** — NVDA is the closest directional read but is C-tier only; trigger would be A/B gate clearance + fresh RTH re-confirmation below ~205
- Best catalyst-backed candidate: **ONDO/USDT** (rwa_narrative basket, fresh <6h)
- What to avoid: **UNH** (legal risk), **BONK/USDT** (active exploit), fresh chases on **ERA/USDT** (+61% 24h, crowded-short funding, no-catalyst momentum playbook is a known -3R/23%WR bucket)
- What would change the view: de-escalation or major escalation on Iran/Hormuz (would resolve the crypto risk-on/risk-off divergence either direction); a genuine A-tier stocks setup clearing all SI-1..5 gates; ADA/BNB/ETH exploit-hack situations reaching resolution (currently open risk flags, not closed)

## 7. Candidate Deep Dives

### 1. ONDO/USDT — LONG, best long-watch / best catalyst-backed

- Has price already reacted to the catalyst? Partially — 24h +11.35%, 7d +25.36%, RS vs BTC +10.0%. Not a fresh spike; a grinding RS-leader move.
- Is the setup chasing? No — current price 0.3964 is close to (not far above) the planned pullback entry 0.3904-0.3946.
- Retest/pullback structure? Yes — plan explicitly requires a pullback fill, not a market buy.
- Overextended (>2 ATR from EMA20)? No — passed the system's extension filter (report did not reject for extension).
- Would entry now be late? Only if filled above the 0.3946 upper bound without a retest; otherwise no.
- Level that makes it actionable: fill inside 0.3904-0.3946, invalidation on a 1h close below 0.3853.
- Aligned with market mood? Yes — RS-leader long inside a risk-on crypto tape, RWA basket fresh <6h.
- Long/short/wait: long, actionable now on a pullback fill (not a market entry at current price).
- Catalyst confirmation or contradiction? Confirmation — rwa_narrative basket (ONDO/XLM primary, single_source, fresh <6h) plus a "Ondo Finance up 14% as entity buys $61M ONDO" headline in the catalyst cycle file.
- Caveat: this exact playbook (`crypto_intraday_catalyst_or_momentum`, no-catalyst-labeled variant) carries a 14d WR 23%/PF 0.70/-3R note in its own metadata — the catalyst basket linkage is what differentiates this instance from that losing bucket; if the basket goes stale, downgrade confidence.

### 2. ERA/USDT — LONG, manage-only / caution (do not chase)

- Has price already reacted? Yes, extremely — +61.17% 24h, +24.5% 7d. This move has already happened.
- Is the setup chasing? Effectively yes at current price (0.0996); the plan's pullback zone (0.0934-0.0977) is only a shallow 2-6% dip from the blow-off high, not a real reset.
- Retest/pullback structure? Shallow only — not a multi-day base.
- Overextended? Borderline — passed the system's 2-ATR filter narrowly but funding is negative and crowded (bybit -0.0117, mexc -0.0113) across venues, i.e., shorts are crowded into a still-rising move (squeeze fuel, not a clean signal).
- Would entry now be late? Yes for anything but the exact defined pullback band.
- Aligned with market mood? Directionally yes (risk-on longs), but this specific instance is the same idea flagged at both 11:39 and 16:29 reviews without a genuine reset.
- Chase-risk setup? Yes, explicitly.
- Catalyst confirmation? None — report states "no fresh verified catalyst detected"; this is pure no-catalyst momentum, the playbook's own known-losing configuration (WR 23%/PF 0.70/-3R over 14d).
- Verdict: manage the existing tp2_hit position only; do not add fresh size here.

### 3. UNH — AVOID (legal/headline risk overrides technicals)

- Raw score 86.55, would be A-tier on technicals alone.
- Tier demoted A→C: **active legal/headline risk (sec_doj)** — manual review required, per the stocks intraday report's explicit gate output.
- Legal/headline risk check (per §I discipline): DOJ criminal-probe/Medicare-fraud angle previously corroborated multi-source in the 16:29 review's sourcing (FierceHealthcare, TipRanks); today's report reiterates the same demotion reason unchanged.
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** — never a clean actionable regardless of score, per §I policy.

### 4. NVDA — short-watch context (C-tier, not actionable; needs review)

- Has price already reacted? Yes — RTH produced a triggered short signal (score 87.8, entry 205.28-206.74, invalidation 208.20) alongside a much weaker triggered long (score 51.7). The market's own signal generation leaned short today.
- Is this actionable? No — stocks intraday §6 explicitly states 0 A/B actionable setups after SI-1..5 gates this cycle; NVDA is C-tier research only.
- Data-integrity note: the tracked NVDA short instance shows `status=triggered` with `expires_at=2026-07-21T15:03:27` (UTC, ≈18:03 EEST) — **already past** relative to this 21:39 EEST review. That is a status/expiry mismatch (should have resolved to a closed/expired state by now if the pipeline is behaving correctly) — flagged as **NEEDS REVIEW**, not treated as a live trade either direction.
- What would make a NVDA short genuinely actionable: clearing the SI-1..5 gates (market_context_conflict, sector_confirmation status, liquidity/rvol) plus a fresh RTH candle re-confirming below ~205 in a later cycle.
- Legal/headline check: no NVDA-specific legal flag today; only general semis/AI-hardware headline noise (Vera Rubin chip commentary, positive).

### 5. BANK/USDT — short-context, why-not-actionable (squeeze risk education)

- Weakest symbol on the board: 24h -38.62%, RS vs BTC -39.97%.
- Derivatives: price down + OI down (-20.43% 24h) = deleveraging/long-liquidation, a genuine breakdown signature.
- Why not actionable: capped to C-tier by `high_upper_wick_short_squeeze_risk` (thin liquidity, high upper wick pattern) — the system's squeeze guard, not a data gap.
- Crypto direction=short stats this week are dismal (0 wins/6 losses, PF 0.125, n=8 anecdotal) — even if the squeeze cap were lifted, this would fight both the guard and the base-rate.
- What would make it actionable: a confirmed lower-high rejection with the upper-wick squeeze signature clearing, plus fresh corroborating catalyst (currently "catalyst_backed" tag exists per discovery agent but is not independently verified in §G's internal-first check for this candidate).
- Verdict: **watch only, not a short-watch trigger** — squeeze risk and weak short base-rate both argue against it despite the clean technical breakdown.

## 8. Best Candidates Ranked

1. **Long: ONDO/USDT** — pullback fill 0.3904-0.3946, invalidation 1h close < 0.3853. Best long-watch and best catalyst-backed pick this cycle.
2. **Manage-only: ERA/USDT** — hold existing tp2_hit position; no fresh add at current +61% extension.
3. **Short-watch (research only): NVDA** — not actionable (C-tier); trigger for future promotion = SI-1..5 gate clearance + fresh RTH re-confirmation below ~205.
4. **Avoid: UNH** — legal/DOJ risk, manual review required, never a clean actionable.
5. **Watch only, not a trigger: BANK/USDT** — genuine breakdown but squeeze-capped; needs upper-wick risk to clear first.

## 9. Avoid / No Trade

_(this decision window only — never a command to stop the system)_

- **UNH** — active DOJ criminal-probe/Medicare-fraud investigation; hard avoid regardless of score.
- **MSFT** — active securities-fraud legal flag, demoted B→C; same treatment as UNH, lower priority mention.
- **BONK/USDT** — active exploit drainer, operator-review flag live.
- **ERA/USDT fresh entries** — +61% 24h, crowded negative funding, no-catalyst momentum playbook is a known -3R/23%WR bucket; manage the open position, do not chase.
- **Crypto shorts generally** — direction=short stats remain dismal this week (n=8, 0% winrate, PF 0.125); bullish tape also caps most short setups to C via squeeze guards.
- **Stocks C-tier intraday broadly** — 0 A/B actionable after gates all session; the entire board (including NVDA/JPM/XOM/COIN/AAPL etc.) is research/planning only today.
- **TSLA, GOOGL, NOW, LMT (stocks)** — earnings tomorrow (2026-07-22) or today (NOC); `do_not_chase_warning` active.
- **ADA, BNB, ETH, SOL** — open exploit_hack risk flags (Wanchain/Cardano bridge, Allbridge); operator-review advisory live, treat cautiously even where technicals look fine.

## 10. Main Risks

- **Geopolitical**: Iran/Israel escalation + Hormuz/oil risk — macro score 100/100, unresolved all day; this is the single largest unpriced tail risk sitting under an otherwise-uptrending crypto tape.
- **Squeeze/reversal risk**: ERA's crowded-negative-funding +61% move is the same pattern that stopped out HEMI and LA earlier this week (per 16:29 review) — do not assume this one resolves differently without a genuine reset.
- **Data-integrity risk**: 8 untracked legacy crypto alerts today (no backing `proposed_signal`) — these will not contribute to PF/winrate tracking; separately, NVDA's status/expiry mismatch suggests the stocks pipeline may have a similar lifecycle-resolution gap worth a human look.
- **Catalyst mapping weak (77.2% unmapped)** — treat catalyst tags as directional color, not confirmation, for any candidate not independently cross-checked.
- **Legal risk live** on UNH (DOJ) and MSFT (securities fraud) — both hard avoids regardless of technical score.
- **Earnings gap risk**: GOOGL, TSLA, NOW, LMT report tomorrow; NOC reports today — elevated post-print volatility risk for correlated names into tomorrow's sessions.
- **Zero actionable stocks setups for a full session** (pre-open through late-session, same 0 A/B result both times) — worth noting as a pattern, not a one-off, though not itself a system fault (chop regime genuinely produces fewer clean setups).

## 11. Action Plan — Next 4 Hours

- Manage existing crypto positions toward remaining targets (22 of 27 active crypto signals are already tp1_hit/tp2_hit, i.e., partial-profit managed) — no new size on ERA/LA/HEMI-style extended movers.
- ONDO/USDT: watch for the 0.3904-0.3946 pullback fill; only add there, not at current price.
- ONDO/USDT scalp (`sig_c2231bf2c6c8decd`, waiting_for_entry) expires ~22:26 EEST — under an hour left; if it lapses, that's an expected NO-ENTRY, not a missed opportunity (scalp mode's own stats are negative, PF 0.72).
- Stocks: no new positions tonight — 0 A/B actionable, chop regime, and TSLA/GOOGL earnings loom tomorrow. Treat the NVDA short reaction as directional research only.
- Hold UNH and MSFT as hard avoids into any future cycle until their respective legal situations are formally resolved.
- Monitor Iran/Hormuz headlines directly — either escalation or de-escalation would be the single biggest catalyst for tomorrow's regime read.
- Scanning, tracking, and monitors continue running unchanged — this review changes nothing in the pipeline.

## 12. Final Verdict per Mode

- **Crypto scalp**: kill-switched (mode off) — consistent with its own negative-leaning stats (PF 0.72, avgR -0.10, n=39 this week). No action.
- **Crypto intraday**: working overall (PF 2.08, avgR 0.37, n=81) — manage ONDO/ERA/ADA/VIRTUAL positions; selective RS-leader/catalyst-backed longs only for anything fresh.
- **Crypto swing**: working well (PF 2.70, avgR 0.44, n=47) but today's report is 17h stale — no fresh swing read this cycle; existing positions carry forward unmanaged-review only.
- **Stocks intraday**: chop regime, 0 A/B actionable all session — watch/research only; re-evaluate at tomorrow's pre-open slot ahead of GOOGL/TSLA earnings.
- **Stocks swing/invest**: no fresh data (framework deprecated, 19 days stale) — no verdict this cycle.

## 13. Sources

_No new external WebSearch/WebFetch performed this cycle (per §G, internal report/catalyst/news_items data was fresh, consistent, and sufficient for every candidate). Citations below are internal report-attributed sources already carrying title/outlet/date:_

- "Ondo Finance up 14% as entity buys $61M ONDO – Is more upside coming?" — via `rwa_narrative` basket, catalyst_cycle_17-31.md, fresh <6h (ONDO catalyst confirmation)
- "Chainlink Becomes Top 20 Best Performer, 3 Reasons Behind the Move" — BeInCrypto, 2026-07-21 (ONDO/ZEC context)
- "Digging deep into Wanchain's Cardano-BNB Bridge exploit – How $9M NIGHT vanished in hours" — AMBCrypto, 2026-07-21 (ADA/BNB exploit risk, still open)
- "Allbridge(@Allbridge_io) was exploited for ~$1.65M" — t.me/lookonchain, 2026-07-21 (ETH/SOL exploit risk, still open)
- "The trader who legally drained 4.426T $BONK($21.2M)..." — t.me/lookonchain, 2026-07-21 (BONK exploit risk, still open)
- UNH DOJ criminal-probe / sec_doj legal risk — carried forward from stocks intraday report gate output, previously multi-source corroborated (FierceHealthcare, TipRanks) per the 16:29 review
- "Novo Nordisk's lawsuit against Eli Lilly over ads highlights intense competition in GLP-1 market" — MarketWatch Top Stories, 2026-07-21 (LLY legal/headline context)
- "Tesla earnings are on deck, and investors will be looking to settle this major debate" — MarketWatch Top Stories, 2026-07-21 (TSLA earnings-risk context)
- "*NVIDIA SAYS MAJOR CUSTOMERS ARE ALREADY TESTING VERA RUBIN GEAR" — t.me/BWEtradfi, 2026-07-21 (NVDA context, neutral-positive, not a legal/headline risk)
- Catalyst mapping ratio (22.8% mapped / 77.2% unmapped) — computed directly from `data/catalysts/2026-07-21/catalyst_events.jsonl` (3,475 rows)
- All other candidate context sourced from internal reports/CLI listed in §2.

## 14. Fix Requests / TODO

### TODO-untracked-alerts-recurrence
- **issue:** Untracked legacy watchlist alerts (Telegram-sent but no backing `proposed_signal`) continue to fire daily — 8 today (INJ 07:55, ADA 08:29, VIRTUAL 09:14, ADA 10:01, VIRTUAL 12:47, VIRTUAL 15:54, OPN 17:26, ZAMA 18:40), up from 5 as of the 16:29 review.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-21` output, this run.
- **suggested manual fix:** this matches the previously-raised [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] TODO-3 (raised to high priority 2026-07-17) — watchlist re-fire is reusing a stale/closed signal_id instead of minting a new `proposed_signal`. Still unresolved 4 days later; recommend prioritizing in the next human-driven maintenance session.
- **priority:** high (already elevated; recurrence continues to grow — now 8/day vs the ALLO/USDT and BANK/USDT cases originally confirmed)
- **first observed:** 2026-07-17 (this run reconfirms ongoing recurrence, 2026-07-21 21:39 EEST)

### TODO-nvda-signal-status-expiry-mismatch
- **issue:** Tracked stocks signal `sig_e0fceb60a6327886` (NVDA, C-tier, short, score 87.8) shows `status=triggered` with `expires_at=2026-07-21T15:03:27` (UTC) — already ~3.5h in the past relative to this 21:39 EEST review, with no resolution to a closed/stopped/expired state visible via `active-signals`. Possible lifecycle-resolution gap for stocks C-tier signals whose decision window has elapsed without a monitor sweep, or simply a display/query artifact — worth a human look to determine which.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` output, this run (row for NVDA short, `sig_e0fceb60a6327886`).
- **suggested manual fix:** check whether the stocks pending/outcome monitor is correctly resolving C-tier intraday signals once their `expires_at` passes, or whether this is a stale row that should have been swept.
- **priority:** medium
- **first observed:** 2026-07-21 21:39 EEST

### TODO-catalyst-mapping-persistent-weak
- **issue:** Catalyst mapping has been below 50% for multiple consecutive review cycles (22.8% today; prior reviews in this same day cited a similarly weak ratio at the pre-open slot).
- **evidence:** direct computation from `data/catalysts/2026-07-21/catalyst_events.jsonl` — 794/3475 mapped (22.8%).
- **suggested manual fix:** revisit the symbol resolver in the catalyst layer — a large share of unmapped volume appears to be exchange-ops/delisting notices and general macro wire copy that may not need ticker mapping at all; worth separating "genuinely unmappable" noise from "should have mapped but didn't" to get an accurate signal on resolver health.
- **priority:** low (mapping weakness is being correctly flagged as advisory-context-only each cycle, not driving any decision silently)
- **first observed:** recurring pattern, reconfirmed 2026-07-21 21:39 EEST
