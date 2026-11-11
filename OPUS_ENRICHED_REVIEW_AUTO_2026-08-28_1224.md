# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:30 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context (advisory only / no auto-trade).** Scheduler is fresh — `scheduler.log` and the latest `cycle_04_07-14_summary.md` both stamped 11:17 EEST, ~1h07m old, well inside the 3h defer threshold. Crypto swing data is fresh (07:59 EEST, ~1h25m old); crypto intraday/scalp reports are carry-forward from 04:35–04:46 EEST (~7.5–7.9h old — no fresher intraday/scalp report has landed yet this cycle, flagged in §3). Crypto regime reads **range/chop (neutral)** on the fresher swing read with BTC/ETH still in an uptrend and altcoin breadth 52.1%/79.2% (above EMA20/EMA50) — softer than the carry-forward intraday read (68.8%/83.3%, "bullish trend risk-on"), consistent with a market cooling slightly since the overnight leg. **Zero A-tier crypto signals, zero fresh crypto shorts** — the active book remains 100% long (signal-stats: n=445, direction=long only). Macro/geopolitical risk sits at 100/100 (Iran/Strait-of-Hormuz, Kazakh oil, France inflation) under the constructive crypto tape. Stocks are closed pre-open (VIX 14.51, calm); the top scored candidate is **SNOW** (raw A-tier, score 97.56) but demoted to C purely for `market_closed_intraday_planning_only` — a clean catalyst-watch into the US open. **ONG/USDT's bias-tag contradiction is now unresolved for a 5th+ consecutive cycle**: the open swing long (`sig_8d3a8fd71bf0bf75`, triggered 2026-08-26, invalidation 0.09240) is still tagged bias=short (-8.18% 24h) in today's swing report, and a fresh WebSearch returned the same three mutually-inconsistent external prices as the prior cycle (CoinGecko $0.2479, CoinMarketCap $0.1148, Crypto.com $0.10) — escalated further in §14. Catalyst mapping is weak this run (73.1% unmapped). Scanning, tracking, and the scheduler continue regardless of this window's verdict.

## 2. Data Used

- Crypto swing report: `data/reports/swing/2026-08-28_07-59_swing_report.md` (fresh, ~1h25m old)
- Crypto intraday report: `data/reports/intraday/2026-08-28_04-46_intraday_report.md` (carry-forward, ~7.5h old)
- Crypto scalp report: `data/reports/scalp/2026-08-28_04-35_scalp_report.md` (carry-forward, ~7.9h old)
- Stocks intraday report: `data/reports/stocks/intraday/2026-08-28_06-42_stocks_intraday_report.md` (fresh, ~2.7h old, market closed)
- Stocks swing/invest reports: both dated 2026-07-02 (~57 days stale — excluded from verdicts, known long-standing gap, not re-raised as new)
- `data/catalysts/2026-08-28/catalyst_events.jsonl` (1000 events), `narrative_baskets.jsonl` (3 baskets)
- CLI: `active-signals --asset-class crypto` (50 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-28`
- Direct read-only SQL against `proposed_signals` + `signal_outcomes` + `news_items` (last 8h/24h/48h windows) — scoped to the allowed tables only
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_0448.md`
- 1 WebSearch (ONG/USDT external price cross-check) — see §13
- **TradingView / manual chart check unavailable** — all technical read (entry zones, ATR, EMA, RR) taken directly from report-stated OHLCV/ATR/EMA fields, no chart tool loaded this run.

## 3. Scheduler / Data Freshness

- `scheduler.log`: 2026-08-28 11:17:16 EEST (~1h07m old) — **fresh**.
- Latest cycle summary `cycle_04_07-14_summary.md`: same mtime — **fresh**. No defer triggered (rule requires BOTH >3h stale).
- Swing report: 07:59 EEST generation (~1h25m old) — **fresh**.
- Intraday report: 04:46 EEST (~7.5h old) — **carry-forward**; no newer intraday report exists yet this cycle. Treated as context, not a fresh read.
- Scalp report: 04:35 EEST (~7.9h old) — **carry-forward**, same caveat; scalp is the most time-sensitive mode and this gap is the widest of the three.
- Stocks intraday: 06:42 UTC / 09:42 EEST (~2.7h old) — **fresh** for a closed-market planning report.
- Stocks swing/invest: 2026-07-02 — **stale** (>14h band, in fact ~57 days) — excluded from final verdict per rule, cross-referenced only.
- No monitor/paper-status file was read this run (not in the allowed CLI/read list); no claim made about it.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-28 12:24 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_04_07-14 both 11:17 EEST", "swing report 07:59 EEST fresh", "intraday report 04:46 EEST (~7.5h) carry-forward", "scalp report 04:35 EEST (~7.9h) carry-forward", "stocks swing/invest ~57d stale"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "longs_preferred", "chop"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing: range/chop (neutral), BTC/ETH uptrend, breadth 52.1%/79.2%", "intraday (carry-forward): bullish trend risk-on, breadth 68.8%/83.3%", "macro risk 100/100 risk-off overlay", "stocks: transition/neutral, VIX 14.51, market closed"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["1000 catalyst_events, 269 mapped (26.9%), 731 unmapped (73.1%)", "ai_narrative basket sample headline is Russian-strikes news, unrelated to AI — evidence mismatch persists", "momentum_breakout basket flags ENA/USDT catalyst-backed (token_unlock risk also present)"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["MSTRB/USDT and several swing candidates: futures data unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HEI/HEMI/ENA/TRUMP/CHIP: price up + OI up, crowding normal", "BMT: price up + OI down, short-covering pattern"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "clean_retest", "entry_fresh"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HEI/USDT +19.9% 24h, pullback zone 0.1590-0.1620 vs current 0.1633 (near top of zone)", "HEMI/USDT +37.2% 24h, extended", "SNOW score 97.56 raw A, needs RTH confirmation"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "no_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 0 A-tier, ~10 waiting_for_entry, ~30+ triggered/tp1_hit unresolved", "stocks active-signals: all 50 rows historical/expired (oldest to 2026-07-29), several tp1_hit/tp2_hit rows never transitioned to a closed state", "8h window: stocks 55 missed_no_entry + 31 stale_before_entry (market closed), crypto 6 expired + 1 missed_no_entry + 1 entry_moved_away + 2 stopped"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.7,
      "reason_codes": ["manual_review", "correlation_cluster", "headline_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONG/USDT bias-tag contradiction unresolved 5th+ cycle, open long still triggered vs invalidation 0.09240", "correlated RS-momentum swing cohort (HEI/HEMI/TAO/etc.) shares one playbook's BTC-dump failure mode", "CRM/CRWD carry stale_post_earnings_setup + earnings-calendar UNKNOWN caps"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto tier=B PF 1.41 (n=445); mode=swing PF 1.66, intraday PF 1.55, scalp PF 0.10 (avgR -0.08, totalR -9.0, 1W/10L)", "crypto exchange_confirmation=Binance-only PF 0.96 (negative) vs cross-exchange PF 1.76", "stocks tier=C triggered winrate 6%, PF 0.36 (correctly gated non-actionable)", "stocks sector: financials PF 2.67, consumer_discretionary PF 5.0 vs semiconductors/healthcare/communications negative"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.65,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "HEI/USDT", "trigger": "pullback fill 0.1590-0.1620, no market buy at 0.1633", "reason": "score 70/100, RS-leader, actionable crypto_swing_narrative_rs_momentum playbook, primary of fresh momentum_breakout basket, but already +19.9% 24h — fill only, do not chase" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "confirm bearish HTF structure break + volume before promoting out of watch — no scored short setup exists this cycle", "reason": "weakest symbol in today's swing report (-19.69% 24h, RS -20.38%), but this is a bias tag, not an audited playbook candidate" },
    "best_catalyst_candidate": { "symbol": "SNOW", "trigger": "RTH confirmation at/after 16:30 EEST open, reclaim pre-market structure with volume", "reason": "raw A-tier, score 97.56, only capped for market_closed_intraday_planning_only — cleanest catalyst/score-backed name into the US open" },
    "avoid_candidate":         { "symbol": "ONG/USDT", "reason": "bias-tag contradiction unresolved 5th+ consecutive cycle; open triggered long vs. mutually-inconsistent external price reads; do not add to or close the position without operator confirmation" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | mixed, longs_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, clean_retest, entry_fresh | advisory_only |
| execution_lifecycle | needs_review | 0.70 | waiting_for_entry, entered_unresolved, no_entry, needs_review | advisory_only |
| risk_manager | manual_review | 0.70 | manual_review, correlation_cluster, headline_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (04:48 EEST)

- **ONG/USDT contradiction persists, now worse than "4th consecutive cycle"** — the 04:48 review escalated it to 4th cycle; it is still open (`triggered`, unresolved) and still tagged bias=short in the 07:59 swing report. A fresh WebSearch this cycle returned the **identical** three external prices as the last review (CoinGecko $0.2479, CoinMarketCap $0.1148, Crypto.com $0.10) — this looks less like independently-refreshed data and more like a cached/stale search index, itself worth flagging (see §14 TODO-ong).
- **ai_narrative basket evidence mismatch persists unchanged** — still Israel/Russia conflict headlines under an "AI sector rotation" label (primary NEAR/RENDER/TAO/FET). Same bug as flagged 04:48, not yet fixed (expected, per the permission contract — fixes are human-only).
- **New this cycle:** HEI/USDT and HEMI/USDT (momentum_breakout basket) replace TAO/SOL as the top-scored swing names — HEI is now the desk's best fresh long (score 70, vs TAO's carried 89-momentum-but-no-fresh-signal read last cycle). TAO/SOL remain open/managed positions, not fresh ideas.
- **Catalyst mapping improved slightly but still weak:** 73.1% unmapped today vs 77.0% at 04:48 — still above the 50% "context only" threshold.
- **Narrative baskets grew from 2 to 3** — momentum_breakout (BMT/TRUMP/HEI) is new since 04:48, carrying a catalyst-backed ENA/USDT tag (with a token_unlock risk flag also present in the swing report — treat as a two-sided catalyst, not a clean confirm).
- **Stocks:** SNOW is a new top candidate this cycle (raw A, 97.56) — did not appear as a named candidate at 04:48 (market was overnight then too, but with a different top-15 mix). CRM/CRWD carry an additional `stale_post_earnings_setup` + calendar-UNKNOWN cap not present on the rest of the top-15 — flagged as its own TODO below (see also known "earnings calendar UNKNOWN" pattern).
- Stocks swing/invest (2026-07-02) — unchanged, persists.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **1000**. Mapped (non-null symbol): **269 (26.9%)**. Unmapped: **731 (73.1%)**.
- `narrative_baskets` today: **3** — ai_narrative (NEAR/RENDER/TAO/FET, evidence-mismatched), perps_dex_narrative (HYPE), momentum_breakout (BMT/TRUMP/HEI, catalyst-backed ENA).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sampled): "Japan should not raid its forex reserves for Takaichi's food tax cut" (macro/political); "Judge blocks key parts of Trump-backed rule restricting mail-in voting" (US politics); "Philippine peso falls to record low against USD" (macro FX) — legitimate macro-context items that don't map to a single symbol by design, consistent with the pattern in prior reviews, not a new pipeline regression.

## 6. Market Landscape

Crypto: the fresher swing read (07:59 EEST) shows BTC/ETH still in an uptrend but altcoin breadth cooling to 52.1%/79.2% (above EMA20/EMA50) and the desk's own regime label softening to **range/chop (neutral)**, versus the carry-forward intraday read (04:46 EEST, still "bullish trend risk-on," breadth 68.8%/83.3%). Read together, this looks like a genuine intraday cool-off since the overnight leg rather than a data error — treat the swing read as the more current signal. Underneath, macro/geopolitical risk sits at 100/100 (Iran/Strait-of-Hormuz tension, Kazakh oil-output disruption, France inflation surprise) — a real risk-off overlay under a still-constructive tape. The active crypto book remains **100% long** (signal-stats: n=445, zero shorts triggered) — structurally expected given every short-side name in recent reports is a bias tag rather than an audited playbook candidate, but a real concentration risk if BTC breaks down. Weekly-window performance: swing PF 1.66 and intraday PF 1.55 are both solid; **scalp is a clear laggard (PF 0.10, avgR -0.08R, totalR -9.0R, 1W/10L)** — consistent with scalp being the desk's known-weakest mode.

Stocks: session closed pre-open (VIX 14.51, calm; regime "transition," neutral bias). SNOW is the standout scored name (raw A, 97.56) but every top-15 candidate is capped to C purely for `market_closed_intraday_planning_only` — a session-timing cap, not a thesis problem. CRM and CRWD carry an additional `stale_post_earnings_setup` cap (earnings print confirmed by news, but the calendar field itself reads UNKNOWN) — treat both as manual-review, not just session-closed. Sector rotation: technology/semiconductors/energy strongest vs. utilities/real-estate/staples weakest — aligned with the long-only top-15 (all tech/growth names). Weekly signal-stats: tier=C (the bulk of raw output) shows a 6% triggered winrate and PF 0.36 — the actionability gates are correctly keeping this cohort out of A/B. Stocks swing/invest remain ~8 weeks stale, excluded, not re-raised as new.

### Market Mood / Risk Routing
- Crypto mood: **mixed** — swing read cooling to range/chop, intraday carry-forward still risk-on; macro overlay risk-off (100/100)
- Stocks mood: **closed** (pre-US-open; VIX calm at 14.51, regime "transition/neutral")
- Dominant narrative: momentum_breakout basket (BMT/TRUMP/HEI, catalyst-backed ENA with a token_unlock risk caveat); ai_narrative basket evidence-mismatched, treat with reduced confidence
- Preferred side now: **longs (pullback-only), wait-for-trigger on stocks (session closed)**
- Best long candidate: HEI/USDT — pullback fill 0.1590-0.1620 only, current 0.1633 is already near the top of the zone
- Best short candidate: none clean — best short-watch is TUT/USDT (-19.69% 24h, weakest symbol in swing report), not an audited playbook candidate
- Best catalyst-backed candidate: SNOW — RTH confirmation at/after the US open
- What to avoid: ONG/USDT (bias-tag contradiction, needs operator review); CRM/CRWD (earnings-calendar UNKNOWN + stale post-earnings cap); crypto scalp fresh entries (PF 0.10 this window); chasing HEI/HEMI at current print (both >15% extended)
- What would change the view: BTC losing local uptrend structure (invalidates the correlated RS-momentum swing cohort); a single trusted live ONG quote settling the price contradiction; the US cash open providing RTH confirmation on SNOW/CRM/CRWD; catalyst mapping recovering toward symbol-specific coverage

## 7. Candidate Deep Dives

### 1. ONG/USDT — NEEDS REVIEW / AVOID (top priority, escalated further)
- Open swing long `sig_8d3a8fd71bf0bf75`, triggered 2026-08-26T02:59:24, entry 0.09561-0.09824, invalidation 0.09240, score 73.9 — confirmed still `status=triggered` via direct `proposed_signals` query, i.e. still open this cycle.
- Today's swing report (07:59 EEST) again tags ONG/USDT in the **Weakest Symbols** list: bias=short, 24h -8.18%, RS vs BTC -8.87%.
- `news_items` check: **0 matches** for ONG/USDT in the last 48h — still no internal catalyst to explain a move in either direction.
- Fresh WebSearch this cycle returned the same three external reads as the 04:48 review, essentially unchanged: CoinGecko $0.2479 (+160% 24h), CoinMarketCap $0.1148, Crypto.com $0.10 (+28% 24h) — mutually inconsistent, and none confirms or cleanly refutes the internal -8.18% tag. The Crypto.com print sits closest to the open long's invalidation (0.09240). Classified `single_source` each, directionally suggestive only.
- Has price already reacted to a catalyst? No catalyst exists internally or externally — this remains a data/tagging problem, not a news-driven move.
- Actionable now or after confirmation? Neither direction is actionable until a human confirms the live price against 0.09240.
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** — unchanged from 04:48, now a 5th+ consecutive cycle unresolved.

### 2. HEI/USDT — LONG (best fresh long candidate)
- Score 70.0/100, playbook `crypto_swing_narrative_rs_momentum` (14d WR 72% / PF 5.80 / +24R), status actionable, primary of the fresh `momentum_breakout` narrative basket.
- Has price already reacted? Yes — 24h +19.9%, 7d +20.43%, RS vs BTC +19.21%, volume 1.68x. Current price 0.1633 vs. planned pullback entry 0.1590-0.1620 — already near the top of the zone.
- Chasing? Yes for a market buy at 0.1633; the plan is explicitly pullback-only ("no market buy if extended").
- Retest/pullback structure? Yes, defined entry zone with invalidation at a 1h close beyond 0.1554.
- Overextended? RR to TP1 is 1.84R and setup quality 73.5/100 — not flagged >2 ATR, but the known failure mode for this exact playbook is "chase risk after a vertical 24h move," which applies directly here.
- Catalyst: no fresh verified catalyst detected for HEI specifically — basket membership (momentum cluster) is technical/momentum-based, not news-confirmed.
- Mood alignment: aligned with the swing-read cooling-but-still-uptrend tape; part of a correlated RS-momentum cohort sharing the same BTC-dump failure mode as the rest of the swing book.
- Actionable level: fill only into 0.1590-0.1620; do not chase at 0.1633.

### 3. SNOW — CATALYST-WATCH, best stocks candidate
- Raw tier A, score 97.56, high confidence, risk penalty 0.0 — demoted to C solely for `market_closed_intraday_planning_only`, not for thesis quality.
- Price reaction: not stated in the planning-only excerpt read this cycle; treat as pre-market-only until RTH data is available.
- Actionable now or after confirmation? Not actionable pre-open; watch for a clean reclaim of pre-market structure with volume at/after the 16:30 EEST (09:30 ET) open.
- Legal/headline/earnings risk: none surfaced for SNOW in this cycle's data; earnings not listed in the "within the week" table.
- Verdict: catalyst/score-backed watch, confirm at the open before treating as actionable.

### 4. CRM / CRWD — NEEDS REVIEW (earnings-calendar integrity issue, not a clean candidate)
- Both raw A-tier (CRM 96.62, CRWD 94.38) but carry a second cap beyond session-closed: `stale_post_earnings_setup` — a verified earnings print exists in `news_items` (CRM 2026-08-27T17:27:47-04:00, CRWD 2026-08-26T21:39:20+00:00) while the earnings calendar field reads UNKNOWN, meaning pre-earnings levels are stale and require fresh post-print levels.
- Actionable now or after confirmation? Neither — explicitly flagged "manual review required" by the report itself, independent of the market-closed cap.
- Not treated as a clean long-watch this cycle; do not add these two to the SNOW-style catalyst-watch list without a human resetting the levels post-earnings.

### 5. TUT/USDT — SHORT-WATCH (best available short, not actionable)
- Weakest symbol in today's swing report: bias=short, 24h -19.69%, RS vs BTC -20.38% — the sharpest down-move in the tracked universe this cycle.
- Not a scored/audited playbook candidate in the sections read this cycle (no derivatives/liquidity cap detail available for TUT specifically, unlike the 04:48 review's SNXXB deep dive) — treat as a raw bias tag, not a structured setup.
- Trigger to promote: a defined bearish HTF structure break with volume and derivatives confirmation, and a genuine regime shift (BTC/ETH losing the current uptrend) — none of these conditions are established this cycle.
- Not actionable — the cleanest short-side name available in an otherwise 100%-long book.

## 8. Best Candidates Ranked

1. **ONG/USDT** — NEEDS REVIEW (top priority, unresolved 5th+ consecutive cycle, worsening in duration if not magnitude).
2. **HEI/USDT** (long, fill-only) — best fresh crypto score this cycle, momentum-basket primary, but already extended — pullback fill 0.1590-0.1620 only.
3. **SNOW** (catalyst-watch, stocks) — cleanest score-backed name into the US open, capped only for session timing.
4. **CRM / CRWD** (needs review) — earnings-calendar integrity issue on top of session-closed cap; do not treat as clean watch names.
5. **TUT/USDT** (short-watch, not actionable) — best available short in a 100%-long book, requires regime shift and structured confirmation to promote.

## 9. Avoid / No Trade (this decision window only)

- **ONG/USDT** — any new long or short action pending operator review of the bias contradiction and current live price vs. 0.09240 invalidation.
- **CRM/CRWD** — do not treat as actionable watch names; earnings-calendar UNKNOWN + stale post-earnings levels require a human reset, independent of the market-closed cap.
- **Chasing HEI/USDT or HEMI/USDT at market** — both >15-37% extended over 24h; fill-only discipline applies.
- **Crypto scalp mode** — weekly PF 0.10 (1W/10L, -9.0R) this window; no fresh scalp entries warranted regardless of individual setup quality until performance recovers.
- **Fresh crypto shorts at market** — no audited short candidate exists this cycle; TUT/USDT is a bias tag only, not a structured setup.
- Stocks broadly — market closed pre-open; nothing actionable until RTH confirmation.
- This is a decision-window verdict only — scanning, candidate generation, tracking, and the scheduler continue in all cases; nothing here recommends pausing any part of the system.

## 10. Main Risks

- **ONG/USDT bias-tag contradiction, unresolved for a 5th+ consecutive cycle** — now compounded by a WebSearch returning what appears to be the same cached external prices as last cycle rather than independently refreshed data (see §14 TODO-ong). The single most concrete integrity risk again this cycle.
- **Crypto book remains 100% long, 0 shorts triggered** (signal-stats: direction=long n=445/445) — structurally expected given no audited short candidates exist, but a real concentration risk if BTC breaks the current uptrend structure.
- **Intraday/scalp report staleness** — no fresher intraday (7.5h) or scalp (7.9h) report has landed this cycle; decisions in those modes lean on carry-forward data while swing is fresh.
- **Crypto scalp underperformance** — PF 0.10, avgR -0.08R, totalR -9.0R (1W/10L) this window — a real, currently-losing bucket, not a one-off.
- **Macro risk-off headwind (100/100) under a cooling-but-still-constructive crypto tape** — Iran/Strait-of-Hormuz tension, Kazakh oil disruption, France inflation surprise.
- **Catalyst mapping weak (73.1% unmapped)** — mostly legitimate macro noise, not a symbol-mapping regression, but the catalyst layer should not carry single-name decisions this run.
- **CRM/CRWD earnings-calendar UNKNOWN despite a confirmed earnings print in news** — a data-integrity gap between the earnings calendar and news-based earnings detection.
- **Stocks swing/invest pipeline** still zero fresh reports since 2026-07-02 (~8 weeks) — persists unchanged, cross-referenced not re-raised.
- **Stocks/crypto "active" signals that never reach a terminal closed state** — several stocks rows (e.g. GE ×3, tp1_hit, expired weeks ago) and several crypto scalp tp1_hit rows past their `expires_at` still surface in `active-signals` (see §14 TODO-stale-active).

## 11. Action Plan — next 4 hours (Europe into US pre-open)

- Flag ONG/USDT for operator review — a human with a live order-book quote should settle the internal bias-tag vs. external price conflict and confirm the open triggered long's status against 0.09240; also flag the WebSearch-data-freshness concern itself (§14 TODO-ong).
- Watch HEI/USDT for a pullback fill into 0.1590-0.1620; do not chase at 0.1633. Manage HEMI/USDT similarly if it retraces toward its own stated zone.
- Build the SNOW watchlist entry for the US open: watch for a clean reclaim of pre-market structure with volume at/after 16:30 EEST; do not treat pre-market strength alone as confirmation.
- Do not treat CRM/CRWD as clean pre-open watch names until a human resets post-earnings levels against the calendar-UNKNOWN gap.
- Manage the existing triggered/waiting crypto swing-intraday cohort (TAO, RUNE, S, GIGGLE, SOL, VET, etc.) against their stated invalidations only; no new correlated adds given the shared BTC-dump failure mode and today's elevated (100/100) macro risk score.
- No new crypto scalp entries this window (PF 0.10); let the mode's own weekly stats recover before reconsidering.
- Track TUT/USDT for a possible short promotion only if BTC/ETH actually break the current uptrend structure and a structured setup appears — do not force a short into today's regime.
- Re-check ONG resolution, intraday/scalp report freshness, and the CRM/CRWD earnings-calendar gap at the next cycle (18:30 US open reaction review).

## 12. Final Verdict per Mode

- **Crypto scalp:** carry-forward data (7.9h old); weekly PF 0.10 (1W/10L, -9.0R) — scanner continues, no new entries this window regardless of setup quality.
- **Crypto intraday:** carry-forward data (7.5h old, "bullish trend risk-on"); weekly PF 1.55 — manage existing triggered/waiting orders only, no chase; awaiting a fresher report next cycle.
- **Crypto swing:** fresh data (07:59 EEST); RS-momentum cohort (PF 1.66 weekly) open and running; HEI/USDT is the one fresh actionable idea, fill-only.
- **Stocks intraday:** market closed pre-open; SNOW is the cleanest catalyst-watch into the open; CRM/CRWD need a human earnings-level reset before being treated as watch names.
- **Stocks swing:** stale (2026-07-02) — excluded, cross-referenced not re-raised.
- **Stocks invest:** stale (2026-07-02) — excluded, cross-referenced not re-raised.

## 13. Sources

- [Ontology Gas Price: ONG/USD Live Price Chart, Market Cap & News Today | CoinGecko](https://www.coingecko.com/en/coins/ontology-gas) — accessed 2026-08-28, price $0.2479 (+160% 24h)
- [Ontology Gas price today, ONG to USD live price, marketcap and chart | CoinMarketCap](https://coinmarketcap.com/currencies/ontology-gas/) — accessed 2026-08-28, price $0.1148
- [Ontology Gas (ONG) Price Today: ONG Live Price, Charts, News - Crypto.com US](https://crypto.com/us/price/ontology-gas) — accessed 2026-08-28, price $0.10 (+28.03% 24h)
- Internal: `data/reports/swing/2026-08-28_07-59_swing_report.md`, `data/reports/intraday/2026-08-28_04-46_intraday_report.md`, `data/reports/scalp/2026-08-28_04-35_scalp_report.md`, `data/reports/stocks/intraday/2026-08-28_06-42_stocks_intraday_report.md`, `data/catalysts/2026-08-28/*`, `proposed_signals` / `signal_outcomes` / `news_items` (read-only SQL), `signal-stats` / `active-signals` CLI outputs, `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_0448.md`

## 14. Fix Requests / TODO

### TODO-ong-bias-contradiction (carried forward, escalated)
- **issue:** ONG/USDT's open swing long (`sig_8d3a8fd71bf0bf75`, triggered 2026-08-26, invalidation 0.09240) has been tagged bias=short with a large negative internal 24h move for 5+ consecutive review cycles (first noted 2026-08-08 per project memory, escalated at 04:48 today, still unresolved at 12:24), with no internal news to explain either direction and mutually-inconsistent external prices on every check.
- **evidence:** `proposed_signals` (signal_id `sig_8d3a8fd71bf0bf75`, status=triggered), swing report 07:59 EEST Weakest Symbols (ONG/USDT bias=short, -8.18% 24h), `news_items` 0 matches last 48h, WebSearch this cycle: CoinGecko $0.2479 / CoinMarketCap $0.1148 / Crypto.com $0.10.
- **suggested manual fix:** a human should pull a live order-book quote (not an aggregator) to settle ONG's actual 24h direction, resolve or close the open long against 0.09240, and separately investigate why the internal bias tag and the price feed used for that tag disagree so persistently for this one symbol.
- **priority:** high
- **first observed:** 2026-08-08 (per project memory); this run: 2026-08-28 12:24 EEST

### TODO-websearch-staleness
- **issue:** the WebSearch run this cycle for ONG/USDT returned the identical three prices/percentages as the 04:48 review's WebSearch (same CoinGecko/CoinMarketCap/Crypto.com figures to the exact cent/percent) — suggests the search index may be serving cached results rather than live data for this query pattern, undermining the external-verification step's value for fast-moving crypto prices.
- **evidence:** compare §13 of this review to §13/§7 of `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_0448.md` — figures match exactly across a ~7.5h gap despite ONG's internal tag also being volatile.
- **suggested manual fix:** a human session should test whether a different WebSearch phrasing, an exchange-direct query, or a dedicated market-data MCP source returns fresher figures for fast-moving crypto pairs, and consider that as the standard verification path for future ONG-style contradictions.
- **priority:** medium
- **first observed:** 2026-08-28 12:24 EEST

### TODO-ai-narrative-mismatch (carried forward, unfixed)
- **issue:** the `ai_narrative` narrative basket (primary NEAR/RENDER/TAO/FET, playbook `related_beta_rotation`) still carries an unrelated sample headline ("Russian strikes hit Nova Poshta...") under an "AI sector rotation" label — same mismatch flagged at 04:48, still present now.
- **evidence:** `data/catalysts/2026-08-28/narrative_baskets.jsonl`, first entry, `catalyst_summary` field.
- **suggested manual fix:** review the keyword/classification logic that assigns headlines to the `ai_narrative` basket — likely a keyword-collision bug pulling unrelated geopolitical headlines into a crypto/AI-labeled basket.
- **priority:** medium
- **first observed:** 2026-08-28 04:48 EEST (this cycle: still unresolved)

### TODO-stale-active-signals
- **issue:** `active-signals` for both asset classes surfaces rows that appear to have reached a terminal outcome (tp1_hit / tp2_hit / triggered) weeks past their `expires_at`, with no visible transition to a closed state — e.g. stocks GE ×3 (tp1_hit, expired 2026-08-18/19), several crypto scalp tp1_hit rows expired 2026-08-24/25 still returned in today's 50-row crypto active-signals list.
- **evidence:** `active-signals --asset-class stocks` (oldest row expires_at 2026-07-29, still listed as active with tp1_hit status); `active-signals --asset-class crypto` (e.g. `sig_343150d6ec1fca6b` ONG/USDT scalp, tp1_hit, expires_at 2026-08-25).
- **suggested manual fix:** a human should check whether the active-signals query/view is missing a closed/expired-terminal filter, or whether a downstream job that should mark these closed is not running — this affects the reliability of "active signals" as a decision input, not just cosmetics.
- **priority:** medium
- **first observed:** 2026-08-28 12:24 EEST
