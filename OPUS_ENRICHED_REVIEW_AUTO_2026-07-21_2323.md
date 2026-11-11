# Opus Enriched Review — post-close final daily review — Auto Cycle 23:23 EEST

## 1. Executive Summary

Slot: **post-close final daily review (23:15 EEST)** — daily wrap after the US cash close; focus is what worked/failed today and the overnight-into-Asia setup. Advisory only — no auto-trade, no scoring/threshold changes.

Reports fresh: crypto intraday (22:03 EEST, ~1h20m), crypto scalp (21:55, ~1h28m), stocks intraday (22:54, ~29min — genuine post-close snapshot). Crypto swing report is now **~19h old (04:30 generation) — stale**, carried forward for open-position context only. Stocks swing/invest unchanged at 19 days stale (deprecated framework, [[project_crypto_ai_desk_stocks_position_framework]]).

Today closed with **zero A/B-tier actionable stocks setups for the entire session** (pre-open → RTH → post-close, all three checkpoints showed 0 after gates) — a clean, disciplined no-trade day for stocks, not a system fault; chop regime (VIX 16.97, breadth 75%>EMA20 but 0/4 indices trending) genuinely produced nothing clean. Crypto stayed the only live actionable class: BTC/ETH uptrend held, altcoin breadth 76.9%>EMA20, but the **macro risk-off overlay (100/100, Iran/Israel/Hormuz) persisted the entire day unchanged** — still no reversal evidence, technical risk-on and geopolitical risk-off remain an unresolved divergence into the overnight/Asia handoff.

Best long-watch / catalyst-backed: **ONDO/USDT** (RWA-basket, now entered/triggered, unresolved — RS+10% vs BTC, catalyst confirmed). Best short-watch (context only, not a trigger): **DEXE/USDT** (−76.5% 24h, exhausted breakdown, squeeze-capped to C — same guard logic that has kept crypto shorts at 0/6 wins this week). Avoid: **UNH** (DOJ probe, demoted A→C again tonight) and **new tonight: MKR/USDT** (Movement Labs Chapter-11 bankruptcy headline, importance 0.82 legal-risk catalyst). Manage-only: **ERA/USDT** (still extended, no fresh add).

The untracked-alert bug ([[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] TODO-3) fired **1 more time** since the 21:39 review (OPN/USDT 19:14 EEST) — **9 total today**, still unresolved. The NVDA short signal's expiry/status mismatch flagged at 21:39 is **still unresolved** three hours later — same TODO reconfirmed.

## 2. Data Used

- Reports: crypto intraday (2026-07-21_19-03, fresh ~1h20m), crypto scalp (2026-07-21_18-55, fresh ~1h28m), stocks intraday (2026-07-21_19-54, fresh ~29min, genuine post-close snapshot)
- Crypto swing: 2026-07-21_01-30 report — **~19h old, stale**, excluded from fresh candidates, carry-forward for open-position context only
- Stocks swing/invest: last dated 2026-07-02 (19 days) — excluded, deprecated framework
- Catalyst layer: `data/catalysts/2026-07-21/` — `catalyst_cycle_19-05.md` (latest, generated ~19:05 EEST content-time, file mtime 22:05 EEST), `catalyst_events.jsonl` (3,975 events today), `narrative_baskets.jsonl` (3 baskets)
- LLM packets: `llm_analysis_packet.md` (22:03 EEST), `llm_stocks_packet.md` (22:22 EEST)
- CLI: `active-signals` (crypto ×26, stocks ×50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-07-21` (9 hits)
- Direct computation of catalyst mapping ratio from `catalyst_events.jsonl` (3,975 total, 915 mapped)
- Heartbeat: `data/autostart/heartbeat_state.json` — last OK 2026-07-21T20:17:36Z (~6min ago EEST-relative), last warn 2026-07-20T12:57Z (>24h stale)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-21_2139.md` (late-session slot)
- **External web research not invoked this run** — internal `news_items`/report/catalyst data for every candidate (ONDO RWA confirmation, DEXE breakdown/squeeze data, UNH DOJ demotion re-stated verbatim in tonight's report, MKR Chapter-11 headline sourced CoinDesk single_source) was fresh (<1h–3h), internally consistent, and already source-attributed; per §G this satisfies the internal-first bar without a fresh WebSearch/WebFetch pass.

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-07-21_default_schedule/scheduler.log`: mtime 22:48 EEST (~35 min ago) — **fresh**.
- Latest cycle summary: `cycle_01_21-46_summary.md` (mtime 22:29 EEST, ~54 min old) — **fresh**.
- Heartbeat: OK 2026-07-21T20:17:36Z (~6min ago); no active warn. Monitor alive.
- Crypto intraday/scalp reports: fresh (~1h20–1h28m).
- Stocks intraday report: fresh (~29min, genuine post-close/late-session snapshot, not a pre-open estimate).
- Crypto swing report: **stale (~19h)** — excluded from fresh candidate selection.
- Stocks swing/invest: **stale (19 days)**, excluded — deprecated framework.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-07-21 23:23 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest fresh data (deprecated, excluded)", "TradingView/chart MCP not loaded", "liquidation heatmaps / order book depth / on-chain flows (never automated)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 22:48 EEST (~35min), cycle_01_21-46_summary.md mtime 22:29 EEST (~54min)", "crypto intraday/scalp reports ~1h20-1h28m fresh", "stocks intraday report ~29min fresh (post-close snapshot)", "crypto swing report ~19h old (stale, excluded)", "heartbeat OK 20:17:36Z (~6min ago)"] },
    { "agent": "market_regime", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["risk_on", "mixed", "chop", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 76.9% breadth>EMA20, style=selective longs prefer pullbacks on RS", "macro risk 100/100 risk-off overlay unchanged all day (Iran/Israel, Hormuz, oil) through 04:30->11:39->16:29->21:39->now", "stocks regime: chop/neutral, VIX 16.97, breadth 75%>EMA20 (up from 50% at 21:39) but 0/4 indices trending, all range-bound"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "catalyst_contradicted"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 3975 total, 915 mapped (23.0%), 3060 unmapped (77.0%) -> mapping weak this run, consistent with prior cycles", "rwa_narrative basket fresh <6h, primary ONDO/XLM, confirmed via 'Ondo Finance up 14%' headline", "perps_dex_narrative basket fresh <1h, primary HYPE/related DYDX,GMX,ASTER -- new since 21:39 review, no active signal riding it yet", "MKR/USDT legal_risk catalyst importance 0.82: Movement Labs Chapter-11 bankruptcy (CoinDesk) -- new tonight", "ADA/BNB/ETH/SOL/BONK still carrying exploit_hack operator-review flags, unresolved all day"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "post_unwind_chop", "oi_supports"],
      "data_missing": ["liquidation heatmap", "order book depth/CVD"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT: -76.55% 24h, funding -0.0105 (bybit -0.024, mexc -0.0105, crowding elevated), score demoted 87.7->24.7 via high_upper_wick_short_squeeze_risk -- exhausted breakdown, not a clean short entry", "ONDO/USDT: price up + OI up +20.31%, funding 5e-05, crowding normal -- fresh positioning confirms trend", "ERA/USDT: funding -0.0079 to -0.0082 across venues, OI +238% (fresh leverage into the move), still crowded-short-into-rally pattern flagged at 21:39"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chase_risk", "entry_fresh", "clean_retest", "overextended"],
      "data_missing": ["chart/TradingView MCP not loaded — no manual chart confirmation"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONDO/USDT price 0.4023 vs fresh pullback entry 0.3961-0.4004 -- modest, not extended, RR 1.84R to TP1", "ERA/USDT price 0.1021 vs pullback 0.0963-0.1003 -- shallow dip only from a +66% 24h blow-off, same chase-risk read as 21:39", "DEXE/USDT price >2 ATR from EMA20, explicit 'do not chase' flag in report", "no-catalyst intraday momentum playbook stat unchanged: 14d WR 23% / PF 0.70 / -3R"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 26 active signals -- 22 open/managed (tp1_hit/tp2_hit), 3 entered-unresolved (ONDO, DOT, PROM triggered), 1 waiting_for_entry (GRAM, entry 1.4963-1.5079)", "stocks: 0 A/B actionable this cycle (same as pre-open and RTH checkpoints today); NVDA short sig_e0fceb60a6327886 STILL shows status=triggered with expires_at=2026-07-21T15:03:27 UTC, now ~8h in the past relative to this 23:23 EEST review -- unresolved lifecycle gap, recurs from 21:39"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ/sec_doj legal risk, tier demoted A->C again tonight (score 87.47), manual review required", "MKR: new tonight -- Movement Labs Chapter-11 bankruptcy, legal_risk importance 0.82, single_source (CoinDesk)", "BONK/ETH/SOL/ADA/BNB exploit_hack operator-review flags unresolved all day", "9 untracked legacy watchlist alerts today (up from 8 at 21:39) -- tracking integrity gap continues"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto headline A/B (week): n=167, winrate 35.4%, PF 1.84, avgR 0.27 -- working overall, unchanged from 21:39", "crypto intraday mode: PF 2.08, avgR 0.37, n=81 -- working, carried ONDO/ERA-style ideas today", "crypto scalp mode: PF 0.72, avgR -0.10, n=39 -- losing bucket, correctly kill-switched", "crypto direction=short: PF 0.125, 0 wins/6 losses, n=8 -- crypto shorts remain a clear avoid-new-adds bucket", "stocks headline A/B (week): n=7 anecdotal, PF 1.50, winrate 28.6% -- thin sample, do not over-read", "stocks C-tier: PF 0.895, winrate 14.0%, n=190 reliable -- confirms C-tier correctly excluded from actionable consideration", "stocks Model-F paper_execution_r 14d: all-direction -2.5R/PF0.50/n11, 30d same -- stocks intraday paper edge remains negative in the forward-postfreeze window"] },
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
    "best_long_candidate":     { "symbol": "ONDO/USDT", "trigger": "already entered (triggered, entered-unresolved); manage toward TP1 0.4118 / invalidation 1h close < 0.3909; fresh adds only on a clean retest of 0.3961-0.4004", "reason": "RWA-basket catalyst-backed (fresh <6h), RS+10% vs BTC, not extended, cleanest technical-catalyst alignment on the board all day" },
    "best_short_candidate":    { "symbol": "DEXE/USDT", "trigger": "watch-only -- becomes a genuine short-watch idea only after the squeeze guard clears (upper-wick exhaustion resolves) and a confirmed lower-high forms; do not chase the existing -76.5% move", "reason": "system's own squeeze-cap (score demoted 87.7->24.7) plus a dismal 0/6-win crypto-short base rate this week both argue against treating this as actionable now" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "same as long candidate -- rwa_narrative basket fresh <6h, headline-confirmed", "reason": "only candidate tonight with both a fresh basket and a corroborating single-source headline that is internally consistent with the technical setup" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "active DOJ criminal-probe/Medicare-fraud investigation overrides an 87.47 raw score for the third consecutive review; never a clean actionable regardless of technicals" },
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
| derivatives_squeeze | caution | 0.5 | squeeze_risk, post_unwind_chop, oi_supports | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, entry_fresh, clean_retest, overextended | advisory_only |
| execution_lifecycle | caution | 0.7 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.7 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.7 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (21:39 late-session)

- **New**: MKR/USDT legal-risk catalyst (Movement Labs Chapter-11 bankruptcy, importance 0.82) — not present at 21:39, added to Avoid/Main Risks this cycle.
- **New basket**: `perps_dex_narrative` (HYPE/USDT primary, DYDX/GMX/ASTER related, fresh <1h) replaced `binance_ecosystem_teaser` in the active-basket rotation; no signal currently rides it — watch-only for now.
- **ONDO/USDT**: was "pullback fill" long-watch at 21:39 (entry 0.3904-0.3946) — is now `status=triggered` in `active-signals` (entered, unresolved), and tonight's fresh report re-proposes a continuation pullback (0.3961-0.4004) as the position management level. Same underlying RWA thesis, now live not hypothetical.
- **Stocks regime**: breadth improved further into the close, 50%→75%>EMA20, VIX eased 17.13→16.97 — still 0/4 indices trending and still **0 A/B actionable for a full third checkpoint today** (pre-open, RTH, post-close all showed 0).
- **Untracked-alert bug**: 8 total at 21:39 → **9 total now** (OPN/USDT 19:14 EEST added). Same unresolved TODO-3.
- **NVDA status/expiry mismatch**: unresolved, now ~8h stale relative to this review (was ~3.5h at 21:39) — the gap is widening, not resolving.
- **ERA/USDT**: unchanged guidance — still extended, no fresh add, manage existing tp2_hit position only.
- **UNH**: legal-risk avoid call remains valid and unchanged for a third consecutive review.
- Catalyst mapping: 23.0% mapped today (77.0% unmapped) — consistent with the persistent weak-mapping pattern.

## 5. Catalyst Coverage

- Total catalyst events today: **3,975**
- Mapped (non-null symbol): **915 (23.0%)**
- Unmapped (null symbol): **3,060 (77.0%)**
- Narrative baskets: **3** active this cycle (perps_dex_narrative, ai_narrative, rwa_narrative)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top unmapped-headline patterns (majority exchange-ops/macro-wire noise, not trade-relevant):
- "Binance Further Expands VIP Access with Updated Holder and OTC Criteria" (×7)
- "HunterLab launches Vista L2 with an extended 710nm measurement range" (×6, unrelated instrument-industry noise, false-positive keyword match)
- "This 40%-Yielding ETF Just Got 20% Cheaper -- Are You Missing Out?" (×6)
- JGB/Nikkei macro-wire copy (×5 each) with no ticker match

## 6. Market Landscape

The day closed the way it opened: crypto technically risk-on (BTC/ETH uptrend, 76.9% breadth>EMA20) but sitting under an unresolved 100/100 macro risk-off score all session (Iran/Israel/Hormuz/oil) — this divergence has now persisted through all five reviews today (04:30→11:39→16:29→21:39→23:23) without resolving in either direction. Stocks improved technically into the close (breadth 75%>EMA20, VIX 16.97) but produced **zero actionable A/B setups across the entire session** — energy/healthcare/financials stayed the relative-strength leaders, semis/tech the laggards, and the SI-1..5 actionability gates correctly kept the board on watch-only (market_context_conflict + liquidity_rvol + no-catalyst reasons recurring across AMZN/META/NFLX shorts).

### Market Mood / Risk Routing

- Crypto mood: **mixed** (technical risk-on / macro risk-off overlay, unresolved all day)
- Stocks mood: **chop** (neutral bias, VIX 16.97, breadth 75%, 0/4 indices trending, market now closed)
- Dominant narrative: RWA/tokenization (ONDO/XLM) still primary; perps-DEX (HYPE/DYDX/GMX/ASTER) newly forming <1h; AI-sector rotation (NEAR/RENDER/TAO/FET) ongoing
- Preferred side now: **longs** in crypto (selective, RS-leader/catalyst-backed only); **wait-for-trigger / closed** in stocks (0 A/B all session, market closed until tomorrow's pre-open)
- Best long candidate: **ONDO/USDT** — already entered (triggered), manage toward TP1 0.4118, invalidation 1h close < 0.3909; fresh size only on a clean retest of 0.3961-0.4004
- Best short candidate: **none clean** — DEXE/USDT is the closest directional read (-76.5% 24h) but is squeeze-capped to C-tier and crypto shorts carry a 0/6-win base rate this week
- Best catalyst-backed candidate: **ONDO/USDT** (rwa_narrative basket, fresh <6h, headline-confirmed)
- What to avoid: **UNH** (DOJ legal risk, third consecutive review), **MKR/USDT** (fresh Chapter-11 bankruptcy headline), **BONK/USDT** (active exploit drainer), fresh chases on **ERA/USDT** and **DEXE/USDT**
- What would change the view: de-escalation or major escalation on Iran/Hormuz (unresolved all day, single biggest overnight risk into Asia); a genuine A/B stocks setup clearing SI-1..5 gates at tomorrow's pre-open; resolution of the ADA/BNB/ETH/SOL exploit-hack situations (still open)

## 7. Candidate Deep Dives

### 1. ONDO/USDT — LONG, best long-watch / best catalyst-backed (entered, unresolved)

- Has price already reacted to the catalyst? Partially — 24h +12.91%, 7d +27.59%, RS vs BTC +11.3%. A grinding RS-leader move, not a fresh spike.
- Is the setup chasing? No — current price 0.4023 sits close to the fresh continuation pullback zone 0.3961-0.4004.
- Retest/pullback structure? Yes — the system's own idea explicitly requires a pullback fill, not a market buy, for any fresh size.
- Overextended (>2 ATR from EMA20)? No — passed the system's extension filter.
- Would entry now be late? Only if filled above 0.4004 without a retest.
- Level that makes fresh size actionable: fill inside 0.3961-0.4004, invalidation on 1h close below 0.3909.
- Aligned with market mood? Yes — RS-leader long inside a risk-on crypto tape, RWA basket fresh <6h.
- Long/short/wait: long, already entered (triggered/entered-unresolved per `active-signals`); manage toward TP1 0.4118 / TP2 0.4214 / TP3 0.4309.
- Catalyst confirmation or contradiction? Confirmation — rwa_narrative basket (single_source, fresh <6h) plus the "Ondo Finance up 14% as entity buys $61M ONDO" headline, unchanged and still the cleanest catalyst-technical alignment on the board.
- Caveat: this playbook (`crypto_intraday_catalyst_or_momentum`, no-catalyst-labeled variant) carries a 14d WR 23%/PF 0.70/-3R note in its own metadata; the basket linkage is what differentiates this instance — if the basket goes stale overnight, downgrade confidence for tomorrow's fresh reads.

### 2. ERA/USDT — LONG, manage-only / caution (do not chase)

- Has price already reacted? Yes, extremely — 24h move has flattened slightly to +66.0% (intraday report) from +61% at 21:39, still an extended blow-off.
- Is the setup chasing? Effectively yes at current price (0.1021); the pullback zone (0.0963-0.1003) is a shallow 2-6% dip only, not a real reset.
- Overextended? Borderline — funding remains negative and crowded across venues (bybit -0.0069 to -0.0079 range tonight), and OI is now **+238% 24h** (fresh leverage piling into the move, not a clean signal) vs the deleveraging-adjacent read at 21:39.
- Would entry now be late? Yes for anything but the exact defined pullback band.
- Aligned with market mood? Directionally yes (risk-on longs), but this is the same idea flagged at 11:39, 16:29, and 21:39 without a genuine reset.
- Chase-risk setup? Yes, explicitly.
- Catalyst confirmation? None — "no fresh verified catalyst detected"; pure no-catalyst momentum, the playbook's own known-losing configuration (WR 23%/PF 0.70/-3R over 14d).
- Verdict: manage the existing tp2_hit position only; do not add fresh size, and treat the OI spike as a squeeze/unwind risk flag for tomorrow, not a bullish continuation signal.

### 3. NVDA — short-context, data-integrity NEEDS REVIEW (recurring)

- Has price already reacted? RTH produced a triggered short signal (score 87.8, entry 205.28-206.74, invalidation 208.20) — same instance flagged at 21:39.
- Is this actionable? No — stocks intraday §6 confirms 0 A/B actionable setups for the entire session (pre-open through post-close); NVDA short is C-tier research only, alongside a separately-triggered weaker long (score 51.7).
- Data-integrity note: `sig_e0fceb60a6327886` still shows `status=triggered` with `expires_at=2026-07-21T15:03:27` UTC — now **~8h in the past** relative to this 23:23 EEST review (was ~3.5h at 21:39). The gap is widening across three consecutive reviews without resolution to a closed/stopped/expired state.
- What would make an NVDA short genuinely actionable in a future cycle: clearing the SI-1..5 gates (market_context_conflict, sector_confirmation, liquidity/rvol) plus a fresh RTH candle re-confirming below ~205 tomorrow.
- Legal/headline check: no NVDA-specific legal flag; only general semis/AI-hardware headline noise (Vera Rubin chip commentary, neutral-positive).

### 4. UNH — AVOID (legal/headline risk overrides technicals, 3rd consecutive review)

- Raw score 87.47, would be A-tier on technicals alone.
- Tier demoted A→C **again tonight**: active legal/headline risk (sec_doj) — manual review required, per the stocks intraday report's explicit gate output, unchanged wording from 21:39 and 16:29.
- Legal/headline risk check (per §I discipline): DOJ criminal-probe/Medicare-fraud angle previously corroborated multi-source (FierceHealthcare, TipRanks); tonight's report reiterates the same demotion reason unchanged for a third straight cycle.
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** — never a clean actionable regardless of score, per §I policy, until the DOJ situation is formally resolved.

### 5. MKR/USDT — AVOID / NEW legal-risk flag (Movement Labs Chapter-11)

- New tonight: "Movement Labs files for Chapter 11 bankruptcy months after token scandal" (CoinDesk, single_source, importance 0.82, catalyst type legal_risk) — top-ranked catalyst-by-importance in tonight's cycle file.
- Has price already reacted? Not independently verified this run — MKR was not in either crypto report's top-ideas/watchlist section tonight (not a scored candidate), so no technical read is available; flagging purely as a legal/headline risk item to avoid new exposure on MKR-adjacent tokens.
- Is this actionable? No — not a trade candidate, a risk flag only. No MKR proposed_signal exists in today's active-signals.
- Legal/headline check: single_source (CoinDesk) — per §G/§I discipline this is not yet independently multi-source corroborated; treat as a fresh, credible-but-single-sourced legal risk pending independent confirmation, not yet a fully verified event.
- Verdict: **AVOID any fresh MKR exposure** pending independent source corroboration; carried into tomorrow's watch list as a fresh legal-risk item to re-check.

## 8. Best Candidates Ranked

1. **Long / catalyst-backed: ONDO/USDT** — already entered (triggered, unresolved); manage toward TP1 0.4118, invalidation 1h close < 0.3909; fresh adds only on retest of 0.3961-0.4004.
2. **Manage-only: ERA/USDT** — hold existing tp2_hit position; do not add at current +66% extension, note fresh +238% OI as an overnight squeeze-risk flag.
3. **Short-watch (research only): NVDA** — not actionable (C-tier); data-integrity issue (expiry mismatch) needs a human look; trigger for future promotion = SI-1..5 gate clearance + fresh RTH re-confirmation below ~205.
4. **Avoid: UNH** — legal/DOJ risk, manual review required, third consecutive review with the same call.
5. **Avoid (new): MKR/USDT** — fresh single-sourced Chapter-11 bankruptcy legal risk; re-check for independent corroboration tomorrow.

## 9. Avoid / No Trade

_(this decision window only — never a command to stop the system)_

- **UNH** — active DOJ criminal-probe/Medicare-fraud investigation; hard avoid regardless of score, third consecutive review.
- **MKR/USDT** — new tonight: Movement Labs Chapter-11 bankruptcy headline (single-source, importance 0.82); avoid fresh exposure pending corroboration.
- **BONK/USDT, ETH, SOL, BNB, ADA** — open exploit_hack operator-review flags, unresolved all day.
- **ERA/USDT fresh entries** — +66% 24h, OI +238% (fresh leverage), no-catalyst momentum playbook is a known -3R/23%WR bucket; manage the open position, do not chase.
- **DEXE/USDT** — -76.5% 24h, squeeze-capped (`high_upper_wick_short_squeeze_risk`), >2 ATR from EMA20, explicit do-not-chase flag; not a short-watch trigger despite the clean-looking breakdown.
- **Crypto shorts generally** — direction=short stats remain dismal this week (n=8, 0% winrate, PF 0.125); bullish tape also caps most short setups to C via squeeze guards.
- **Stocks entirely tonight** — market closed after a full session of 0 A/B actionable; entire board (NVDA/JPM/XOM/COIN/AAPL etc.) is research/planning only.
- **GOOGL, TSLA, NOW, LMT** — earnings tomorrow (2026-07-22); NOC reported today; `do_not_chase_warning` active on all.

## 10. Main Risks

- **Geopolitical**: Iran/Israel escalation + Hormuz/oil risk — macro score 100/100, unresolved through all five reviews today; the single largest unpriced tail risk sitting under an otherwise-uptrending crypto tape heading into the Asia session.
- **Leverage/squeeze risk**: ERA's OI jumped +238% 24h on top of an already-crowded-negative-funding +66% move — a classic pre-unwind setup; DEXE is the mirror image (exhausted short squeeze on the downside). Neither should be chased in either direction overnight.
- **Data-integrity risk**: 9 untracked legacy crypto alerts today (unresolved [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]); NVDA's status/expiry mismatch has now persisted ~8h without pipeline resolution across three consecutive reviews — worth escalating priority.
- **Catalyst mapping weak (77.0% unmapped)** — treat catalyst tags as directional color, not confirmation, for any candidate not independently cross-checked.
- **Legal risk live** on UNH (DOJ, 3rd review) and now MKR (fresh, single-sourced Chapter-11) — both hard avoids.
- **Earnings gap risk**: GOOGL, TSLA, NOW, LMT report tomorrow; correlated-name volatility risk into tomorrow's US session.
- **Full-session stocks dry spell**: zero actionable setups across pre-open, RTH, and post-close checkpoints today — a real pattern (3 consecutive zero-A/B checkpoints), not itself a fault, but worth noting if it persists into tomorrow.

## 11. Action Plan — Next 4 Hours (overnight into Asia)

- Manage existing crypto positions toward remaining targets (22 of 26 active signals already tp1_hit/tp2_hit, partial-profit managed) — no new size on ERA/DEXE-style extended movers in either direction.
- ONDO/USDT: manage the entered/triggered position toward TP1 0.4118; only add fresh size on a genuine retest into 0.3961-0.4004, invalidation 1h close < 0.3909.
- GRAM/USDT (`sig_12a1dafc8671bd84`, waiting_for_entry, expires 2026-07-22T17:37) — was rejected in tonight's scalp re-scan (anchor listed, no derivatives confirmation); let it expire naturally if unfilled, do not force.
- Stocks: market closed; no new positions until tomorrow's pre-open review. Zero A/B all session today — re-evaluate cleanly at the pre-open slot ahead of GOOGL/TSLA earnings.
- Hold UNH as a hard avoid; add MKR to the watch list for independent-source corroboration tomorrow.
- Monitor Iran/Hormuz headlines directly through the Asia session — either escalation or de-escalation would be the single biggest driver of tomorrow's crypto regime read.
- Scanning, tracking, and monitors continue running unchanged overnight — this review changes nothing in the pipeline.

## 12. Final Verdict per Mode

- **Crypto scalp**: kill-switched (mode off) — consistent with negative-leaning stats (PF 0.72, avgR -0.10, n=39 this week). No action.
- **Crypto intraday**: working overall (PF 2.08, avgR 0.37, n=81) — manage ONDO/ERA/ADA/VIRTUAL/ALLO positions; selective RS-leader/catalyst-backed longs only for anything fresh overnight.
- **Crypto swing**: working well (PF 2.70, avgR 0.44, n=47) but today's report is 19h stale — no fresh swing read this cycle; existing positions carry forward, unmanaged-review only.
- **Stocks intraday**: chop regime, 0 A/B actionable all session (3rd zero-checkpoint today) — watch/research only; re-evaluate at tomorrow's pre-open slot ahead of GOOGL/TSLA earnings.
- **Stocks swing/invest**: no fresh data (framework deprecated, 19 days stale) — no verdict this cycle.

## 13. Sources

_No new external WebSearch/WebFetch performed this cycle (per §G, internal report/catalyst/news_items data was fresh, consistent, and sufficient for every candidate). Citations below are internal report-attributed sources already carrying title/outlet/date:_

- "Ondo Finance up 14% as entity buys $61M ONDO – Is more upside coming?" — via `rwa_narrative` basket, catalyst_cycle_19-05.md, fresh <6h (ONDO catalyst confirmation)
- "Movement Labs files for Chapter 11 bankruptcy months after token scandal" — CoinDesk, single_source, catalyst_cycle_19-05.md, importance 0.82 (MKR legal-risk flag, new tonight)
- UNH DOJ criminal-probe / sec_doj legal risk — carried forward from stocks intraday report gate output, previously multi-source corroborated (FierceHealthcare, TipRanks) per the 16:29/21:39 reviews
- "Novo Nordisk's lawsuit against Eli Lilly over ads highlights intense competition in GLP-1 market" — MarketWatch Top Stories, 2026-07-21 (LLY legal/headline context)
- "Tesla earnings are on deck, and investors will be looking to settle this major debate" — MarketWatch Top Stories, 2026-07-21 (TSLA earnings-risk context)
- "*NVIDIA SAYS MAJOR CUSTOMERS ARE ALREADY TESTING VERA RUBIN GEAR" — t.me/BWEtradfi, 2026-07-21 (NVDA context, neutral-positive, not a legal/headline risk)
- "Digging deep into Wanchain's Cardano-BNB Bridge exploit – How $9M NIGHT vanished in hours" — AMBCrypto, 2026-07-21 (ADA/BNB exploit risk, still open)
- "Allbridge(@Allbridge_io) was exploited for ~$1.65M" — t.me/lookonchain, 2026-07-21 (ETH/SOL exploit risk, still open)
- "The trader who legally drained 4.426T $BONK($21.2M)..." — t.me/lookonchain, 2026-07-21 (BONK exploit risk, still open)
- Catalyst mapping ratio (23.0% mapped / 77.0% unmapped) — computed directly from `data/catalysts/2026-07-21/catalyst_events.jsonl` (3,975 rows)
- All other candidate context sourced from internal reports/CLI listed in §2.

## 14. Fix Requests / TODO

### TODO-untracked-alerts-recurrence
- **issue:** Untracked legacy watchlist alerts (Telegram-sent but no backing `proposed_signal`) continue to fire daily — 9 today (INJ 07:55, ADA 08:29, VIRTUAL 09:14, ADA 10:01, VIRTUAL 12:47, VIRTUAL 15:54, OPN 17:26, ZAMA 18:40, OPN 19:14), up from 8 as of the 21:39 review.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-21` output, this run.
- **suggested manual fix:** matches [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] TODO-3 (raised to high priority 2026-07-17) — watchlist re-fire is reusing a stale/closed signal_id instead of minting a new `proposed_signal`. Still unresolved 4 days later; recommend prioritizing in the next human-driven maintenance session.
- **priority:** high (recurrence continues, now 9/day)
- **first observed:** 2026-07-17 (this run reconfirms ongoing recurrence, 2026-07-21 23:23 EEST)

### TODO-nvda-signal-status-expiry-mismatch
- **issue:** Tracked stocks signal `sig_e0fceb60a6327886` (NVDA, C-tier, short, score 87.8) still shows `status=triggered` with `expires_at=2026-07-21T15:03:27` UTC — now ~8h in the past relative to this 23:23 EEST review (was ~3.5h at 21:39, confirmed the same gap widening across the 16:29→21:39→23:23 reviews). No resolution to a closed/stopped/expired state visible via `active-signals` across three consecutive checkpoints.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` output, this run (row for NVDA short, `sig_e0fceb60a6327886`).
- **suggested manual fix:** check whether the stocks pending/outcome monitor is correctly resolving C-tier intraday signals once their `expires_at` passes; the persistence across 3 review cycles without resolution suggests this is a genuine lifecycle-sweep gap, not a one-off display artifact.
- **priority:** medium (escalate to high if still unresolved at tomorrow's pre-open review)
- **first observed:** 2026-07-21 21:39 EEST (this run reconfirms, gap widened from ~3.5h to ~8h)

### TODO-catalyst-mapping-persistent-weak
- **issue:** Catalyst mapping has been below 50% for multiple consecutive review cycles across multiple days (23.0% today; same pattern at every checkpoint today and in prior days' reviews).
- **evidence:** direct computation from `data/catalysts/2026-07-21/catalyst_events.jsonl` — 915/3975 mapped (23.0%).
- **suggested manual fix:** revisit the symbol resolver in the catalyst layer — a large share of unmapped volume appears to be exchange-ops/VIP-tier notices, unrelated instrument-industry keyword false-positives (e.g. "HunterLab Vista L2" matching an "L2" narrative keyword), and general macro wire copy that may not need ticker mapping at all; worth separating "genuinely unmappable" noise from "should have mapped but didn't" to get an accurate signal on resolver health.
- **priority:** low (mapping weakness is being correctly flagged as advisory-context-only each cycle, not driving any decision silently)
- **first observed:** recurring pattern, reconfirmed 2026-07-21 23:23 EEST
