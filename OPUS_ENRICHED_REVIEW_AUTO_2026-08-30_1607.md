# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:07 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (target 08:50 America/New_York; actual fire ~08:58 ET, Δ+8min, within tolerance — see §3 DST check). **Advisory only — no auto-trade.** Time-critical hand-off ran first: `stocks-preus-candidates` returned **eligible=0 / excluded=0** (US cash market is closed today, Sunday 2026-08-30, so the pre-open candidate builder correctly found nothing to score), and `stocks-preus-review-health` reports **NO_ELIGIBLE** — no ingest was needed, nothing to promote. Today's pre-open overlay is a no-op by design; the substantive pre-open read for Monday's 09:15 ET decision window is carried in the UNH legal-risk item below and will be re-run live at tomorrow's slot.

Crypto book: still **zero fresh A/B setups** in scalp or intraday (scalp remains kill-switched, intraday found no A/B), and the only tracked B-tier swing idea, **PROM/USDT**, has moved from "extended, chase risk" to **materially more extended** — live price **$7.18 (+38.7% 24h per CoinGecko)**, now closer to its own TP1 (7.510) than to its entry zone (6.583–6.836); treat it as an open position approaching target, not a fresh long-watch. The two open-long contradiction cases carried from the last three reviews **diverged this cycle**: **DEXE/USDT recovered** — live price **$2.35 (+2.4% 24h)**, now only **~1.4% below its own invalidation (2.38346)**, a clear improvement from the confirmed breach at $2.28 (-5.4%) three hours ago — while **TUT/USDT remains essentially unchanged and still breached**, live price **$0.03550 (-7.6% 24h)**, **~29.8% through** its 0.05058 invalidation, tracker still shows `triggered` on both. Macro/geopolitics stays **risk-off (83.9–85.9/100)** across all three cycles today (Iran/Hormuz, Kyiv-area drone strikes). Catalyst mapping is **52.2% unmapped** cumulative today (still weak, marginally better than 53.9% at 11:39). ATOM/USDT remains the top-importance two-sided catalyst (0.77, down slightly from 0.81).

**New this cycle**: the known untracked-watchlist-alert bug (DEXE/USDT, unresolved ~22h, still present) has **two fresh recurrences** — ZKP/USDT and PROM/USDT intraday alerts sent 12:11 UTC today, both untracked. Direct DB inspection shows the **PROM/USDT alert's score (69.3) is an exact match** to an older, already-closed (`missed_no_entry`) intraday signal created ~11.5h earlier — concrete evidence the alert path is reusing a stale signal's parameters instead of minting a fresh `proposed_signal`, not just a timing race. The broader outcome-tracker lifecycle bug (252 stale-but-open rows, 36 crypto + 216 stocks incl. 3 stocks A-tier) is **unchanged, identical count**, confirming no backfill has occurred since the last review. Stocks market closed (Sunday) — the UNH DOJ Medicare-fraud probe legal-risk cluster carries forward unchanged into Monday's cash open. Scanning, tracking, and the scheduler continue uninterrupted regardless of this review's caution stance.

## 2. Data Used

- Time-critical hand-off: `python -m src.cli stocks-preus-candidates` (eligible=0, excluded=0), `python -m src.cli stocks-preus-review-health` (status=NO_ELIGIBLE) — both run before this base review per the PART 16 hand-off contract.
- Reports: `2026-08-30_10-07_scalp_report.md` (13:06 EEST gen, fresh), `2026-08-30_10-19_intraday_report.md` (13:19 EEST gen, fresh), `2026-08-30_04-34_swing_report.md` (07:34 EEST gen, ~8h24m old — carry-forward band); stocks intraday `2026-08-28_18-54` (weekend carry-forward, market closed), stocks swing/invest `2026-07-02` (long-stale, informational only, superseded by the deprecated stocks-swing/invest framework per project memory).
- Catalysts: `data/catalysts/2026-08-30/catalyst_cycle_10-25.md` (latest cycle, 277 rows), `catalyst_events.jsonl` (1415 cumulative rows today), `narrative_baskets.jsonl` (3 baskets this cycle: perps_dex, rwa, ai).
- LLM packet: `llm_analysis_packet.md` (13:21 EEST, fresh, crypto). Stocks packet `llm_stocks_packet.md` (2026-08-28 21:56 — stale, weekend carry-forward, informational only).
- CLI: `active-signals` (crypto: 50 rows / stocks: 50 rows), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-30` and `--since 2026-08-29`.
- Direct SQLite reads (`db/crypto_ai_desk.sqlite`, read-only): `proposed_signals` lookups for TUT/USDT, DEXE/USDT, ZKP/USDT, PROM/USDT lifecycle history; `news_items` freshness check (TUT/DEXE/ZKP/PROM, all empty in last 24h); full-table stale-row sweep (`expires_at < now AND status IN open-states`) re-run for continuity vs the 11:39 review.
- External: 3 WebFetch (CoinGecko live pages: TUT, DEXE, PROM) + 1 WebSearch (BTC/ETH macro context) — see §13.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_1139.md` (Europe/pre-US context slot, 11:39 EEST).

## 3. Scheduler / Data Freshness

- **Pre-US schedule check**: target 08:50 ET, actual fire ~08:58 ET (Δ+8min, within tolerance — well inside the ~20min drift threshold and completed before the 09:12 ET hand-off deadline). No DST-window mismatch active (2026 windows are 03-08→03-29 and 10-25→11-01; today, 08-30, is in the steady-state 7h-offset period).
- `scheduler.log` mtime: 2026-08-30 14:03 EEST (~2h04m old at the time of the time-critical hand-off; well under the 3h defer threshold) — **fresh**, no defer.
- Latest cycle: `cycle_07_12-56_summary.md` (14:03 EEST), 7th cycle of the 2026-08-29 schedule day (day rolled at midnight, folder name unchanged by design — same behavior noted in the prior review).
- Scalp report: 13:06 EEST gen (fresh, <1h). Intraday report: 13:19 EEST gen (fresh, <1h). Swing report: 07:34 EEST gen (~8h24m old — mid carry-forward band, used as context, flagged; TP/entry levels quoted below are cross-checked against a live CoinGecko price, not stale report figures alone).
- Stocks reports: Aug 28 18:54 (intraday, weekend carry-forward, market closed) / Jul 2 (swing, invest — long-stale, informational only, consistent with the project's deprecated old-stocks-swing/invest framework).
- Catalyst scan: 13:25 EEST (fresh, <45min). LLM packet: 13:21 EEST (fresh).
- **Untracked-alert detector**: `--since 2026-08-30` returns **2** new rows (ZKP/USDT, PROM/USDT, both sent 12:11 UTC today); `--since 2026-08-29` returns **3** total (adds the still-unresolved DEXE/USDT row, sent 2026-08-29T14:36:42 UTC, now **~22h22m old**, 7th+ consecutive review carrying it). This is an **escalation** in count (1→3) since the 11:39 review, not a resolution.
- **Outcome-tracker candle-gap / lifecycle-status sweep (crypto+stocks)**: re-ran the same full-table sweep as the 11:39 review — `expires_at < now() AND status IN (waiting_for_entry, triggered, tp1_hit, tp2_hit)` still returns **exactly 252 rows**, identical breakdown (36 crypto B-tier, 197 stocks C-tier, 16 stocks B-tier, **3 stocks A-tier**). No backfill or reconciliation has occurred between reviews.
- Monitor/paper Windows Task state not queried this run (outside the explicit read-only CLI allowlist for this scheduled routine, consistent with all prior cycles); scheduler-log/cycle-file freshness above is used as the sole liveness proxy.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-30 16:07 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.66,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["Windows Task Scheduler live state"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler cycle 14:03 fresh", "swing report ~8h24m old, mid carry-forward band", "scalp/intraday <1h fresh", "252 stale-open-status rows unchanged since 11:39 review, incl. 3 stocks A-tier", "pre-US stocks candidate builder correctly returned eligible=0 on a closed-market Sunday"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chop", "mixed", "wait_for_trigger"], "data_missing": ["fresh ETF flow print this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH range across scalp/intraday/swing all three cycles today", "altcoin breadth 52.5% EMA20 / 72.5-77.5% EMA50", "macro risk 83.9-85.9/100 risk-off (Iran/Hormuz, Kyiv-area drone strikes)", "BTC $77,844 -3.13% 24h, ETH $2,471.80 +0.1% 24h per external check"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "catalyst_contradicted"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["1415 cumulative catalyst events today, 739/1415 (52.2%) unmapped, marginal improvement from 53.9% at 11:39", "ATOM/USDT exploit_hack importance 0.77 (down from 0.81), still top-importance, still two-sided per 11:39 external research (no new resolving info this cycle)", "3 narrative baskets: perps_dex, rwa, ai — all single-source, unconfirmed"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.52,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["DEXE funding/OI still not in either cycle's top-8 derivatives table"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT short idea explicitly rejected in today's scalp report for 'extreme negative funding against short' — squeeze risk unchanged", "ONG/BMT short ideas capped to C-tier for thin-liquidity short-squeeze risk", "PROM funding neutral (5e-06 to -4.98e-05 across cycles), OI +22-24%, no squeeze signal either way"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "entry_late", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM live price $7.18 vs 6.583-6.836 entry zone and 7.510 TP1 — now closer to TP1 than to entry, materially more extended than the 6.948 print at the 11:39 review", "DEXE live price $2.35 now only ~1.4% below its 2.38346 invalidation, a genuine improvement from $2.28 (-5.4%) three hours ago", "no A/B setups in scalp or intraday this cycle"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.63,
      "reason_codes": ["waiting_for_entry", "needs_review", "entered_unresolved"], "data_missing": ["true stop/TP state for all 252 stale rows"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM/USDT swing signal status=triggered, approaching TP1 (7.510) not a fresh entry", "252 stale-open rows unchanged since 11:39 (36 crypto, 3 stocks A-tier, 16 stocks B-tier, 197 stocks C-tier)", "untracked-alert count escalated from 1 (DEXE only) to 3 (DEXE + ZKP + PROM) since 11:39"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.75,
      "reason_codes": ["manual_review", "correlation_cluster", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT live $0.03550 (-7.6% 24h) vs invalidation 0.05058 — ~29.8% through, still status=triggered, essentially unchanged from 11:39", "DEXE/USDT live $2.35 (+2.4% 24h) vs invalidation 2.38346 — improved to ~1.4% below, no longer a fresh confirmed breach, but tracker still shows status=triggered with no reconciliation", "PROM/USDT DB lookup shows the untracked 12:11 UTC intraday alert score (69.3) is an EXACT match to an older closed (missed_no_entry) signal created ~11.5h earlier — concrete new evidence of the score-reuse mechanism behind the untracked-alert bug family", "book remains structurally 100% long across the active-signals table, zero shorts, despite a genuine risk-off macro overlay"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["playbook_failing", "low_sample", "old_tail_expired"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B week: sample=315, winrate 10.8%, PF 1.03, avgR +0.008, totalR +2.0", "by-mode: swing PF 1.57/avgR+0.12 (strongest), intraday PF 0.91/avgR-0.04, scalp PF 0.11/avgR-0.10 (reproducibly losing, 0W/9L)", "weekend signals underperform (winrate 13%, n=33) per this cycle's own observations panel", "stocks A/B week: n=13 (weak confidence), WR 60%, PF inf — same small, lifecycle-bug-contaminated sample flagged at 11:39, unchanged"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["chop", "manual_review", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.62,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "ZK/USDT", "trigger": "existing tracked B-tier intraday waiting_for_entry zone 0.008972-0.009088; confirm a pullback fill inside that zone rather than chasing — do not treat PROM/USDT as a fresh long-watch, it is already extended toward TP1", "reason": "the only other actively-tracked non-extended crypto long in the book; PROM has moved from long-watch to a live position approaching target this cycle" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "a confirmed 1h close-and-retest failure below the recent low with funding normalizing out of extreme-negative territory first — do not short into current extreme negative funding (squeeze risk), and resolve the existing open long manually before adding any new position on this symbol", "reason": "the desk's own scalp report explicitly rejected a fresh TUT short today for squeeze risk; it remains the weakest 24h mover with a corroborated multi-cycle bearish bias, but is not clean" },
    "best_catalyst_candidate": { "symbol": "ATOM/USDT", "trigger": "unchanged from 11:39 — a confirmed breakdown with volume on renewed negative reaction to the hack-disclosure overhang; still tempered by the competing bullish deflationary-tokenomics narrative, so still two-sided, not a clean short", "reason": "highest-importance fresh catalyst again this cycle (0.77), no existing desk position, no new resolving information since the last review" },
    "avoid_candidate":         { "symbol": "TUT/USDT", "reason": "open long ~29.8% through its own invalidation per live CoinGecko cross-check, essentially unchanged from the last review; unreconciled outcome-tracker gap; do not add" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.66 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | chop, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.52 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, entry_late, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.63 | waiting_for_entry, needs_review, entered_unresolved | advisory_only |
| risk_manager | manual_review | 0.75 | manual_review, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.68 | playbook_failing, low_sample, old_tail_expired | advisory_only |
| head_trader | caution | 0.62 | chop, manual_review, wait_for_trigger | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_1139.md` (Europe/pre-US context slot, 11:39 EEST).

- **New (time-critical hand-off, this slot only)**: `stocks-preus-candidates` ran for the first time today — eligible=0, excluded=0, `stocks-preus-review-health`=NO_ELIGIBLE. Expected outcome on a closed-market Sunday; no promotion, no ingest, nothing to reconcile.
- **Improved**: DEXE/USDT — live price recovered from $2.28 (-5.4% 24h, confirmed breach) to **$2.35 (+2.4% 24h)**, now only ~1.4% below its 2.38346 invalidation. No longer a fresh confirmed breach; still unresolved in the tracker (status=triggered) and still not close enough to call "reclaimed."
- **Unchanged**: TUT/USDT — live price $0.03550 (-7.6% 24h) vs $0.03565 (-10.4% 24h) at 11:39; still ~29.8% through its own invalidation (was ~29.5%), essentially flat. Remains the clean avoid case.
- **Escalated**: the untracked-watchlist-alert bug — was 1 unresolved instance (DEXE/USDT) at 11:39, now **3** (DEXE/USDT unresolved + two new same-day recurrences on ZKP/USDT and PROM/USDT). New direct-DB evidence this cycle: the PROM/USDT alert's score (69.3) exactly matches an older closed `missed_no_entry` signal created ~11.5h earlier, giving a concrete mechanism (stale-signal score reuse) rather than just a repeated symptom.
- **Worse (chase risk)**: PROM/USDT continued running — $6.948 at 11:39 → **$7.18 (+38.7% 24h)** now, close enough to its own TP1 (7.510) that this is better framed as an open position nearing target than a long-watch idea. Do not treat it as a fresh long candidate this cycle.
- **Unchanged**: the 252-row outcome-tracker lifecycle-status bug (36 crypto B-tier, 3 stocks A-tier, 16 stocks B-tier, 197 stocks C-tier) — identical count and breakdown to 11:39, confirming no backfill has run between reviews.
- **Unchanged**: ATOM/USDT two-sided catalyst thesis (importance 0.77 vs 0.81) — no new resolving information found this cycle.
- **Unchanged**: catalyst mapping weak (52.2% unmapped cumulative today vs 53.9% at 11:39 — marginal improvement, still above the 50% weak-mapping threshold).
- **Unchanged**: no A-tier or fresh B-tier crypto signals in scalp or intraday this cycle; book remains carry-forward.
- **Unchanged**: UNH/USDT DOJ legal-risk cluster — no new headline surfaced this cycle beyond the six sources already cited at 11:39; still C-tier only, still planning-only until Monday's open.

## 5. Catalyst Coverage

- Total catalyst events today (cumulative, as of 13:25 EEST catalyst cycle): **1415**. Mapped (non-null symbol): **676**. Unmapped: **739** (**52.2%**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets this cycle: **3** (perps_dex_narrative — HYPE/USDT primary, wait_pullback playbook; rwa_narrative — ONDO/XLM primary; ai_narrative — NEAR/RENDER/TAO/FET primary).
- Latest single-cycle scan (`catalyst_cycle_10-25.md`, 277 rows): other_news 254, legal_risk 11, exploit_hack 4, partnership 2, product_launch 1, exchange_listing 1, insider_activity 1, rumour_only 1, buyback_burn 1, token_unlock 1.
- Highest-importance catalyst: ATOM/USDT exploit_hack, importance 0.77 (down from 0.81 at 11:39, still top). BTC/USDT exploit_hack (Coldcard exploit, ~2,055 BTC estimated stolen per Galaxy) also elevated at 0.77.
- Legal-risk cluster unchanged: UNH/USDT DOJ Medicare-fraud probe (still the same corroborated multi-source cluster as 11:39, no new headline this cycle); TSLA/USDT — Musk SEC settlement, $1.5M fine (Union Leader), same as 11:39.
- **Pre-US Stocks Review Overlay**: candidates reviewed: **0** (SUPPORT 0 / NEUTRAL 0 / CAUTION 0 / BLOCK 0 / INSUFFICIENT_DATA 0). Session-cap-only C's now eligible for pre-open Paper lane: **0**. Excluded by hard gate: **0** — the candidate builder found nothing at all to consider (US cash market closed, Sunday), not a filtering outcome. `stocks-preus-review-health` = **NO_ELIGIBLE**.

## 6. Market Landscape

BTC and ETH both read **range** across the scalp (13:06), intraday (13:19), and swing (07:34) cycles today. Altcoin breadth above EMA20 sits at 52.5% across all cycles; above EMA50 ranges 72.5% (swing) to 77.5% (intraday) — modest, not decisive, broadening consistent with the 11:39 review. Macro/geopolitics risk score is elevated and rising slightly across today's cycles (83.9–85.9/100 vs 74.3–85.9/100 at 11:39), driven by continuing Iran/Hormuz headlines (US military leadership warnings on a prolonged Iran war), a Kyiv-area drone strike on the Kirishi oil refinery near St. Petersburg, and Europe missile-defense coverage tied to a potential Russian offensive from Belarus — a genuine, persistent risk-off overlay, not a one-cycle spike. External check: BTC $77,844 (-3.13% 24h), ETH $2,471.80 (+0.1% 24h) — BTC showing the larger de-risking move of the pair. AI and Memes narrative heat remain "mixed" (26-37/100); RWA, L2, Gaming, DePIN are quiet.

### Market Mood / Risk Routing
- Crypto mood:           chop, with a persistent and slightly worsening risk-off macro overlay (83.9-85.9/100) — genuinely mixed, BTC underperforming ETH on the 24h tape.
- Stocks mood:           closed (Sunday) — planning/watchlist context only; UNH DOJ-probe legal-risk cluster carries unchanged into Monday.
- Dominant narrative:    perps_dex (HYPE, wait_pullback), rwa (ONDO/XLM), ai (NEAR/RENDER/TAO/FET) — all single-source and unconfirmed, same three baskets as the latest cycle at 11:39 (momentum_breakout basket not present in the newest cycle file).
- Preferred side now:    wait-for-trigger; the desk's own signal generator remains structurally 100% long across the active book (zero shorts in the last 315-signal weekly sample) — a persistent structural gap, not a fresh market call.
- Best long candidate:   none clean; ZK/USDT (existing tracked waiting_for_entry, 0.008972-0.009088 zone) is the long-watch. PROM/USDT is explicitly NOT a fresh long-watch this cycle — it is an open position running toward its own TP1 (7.510) after a further +38.7% 24h move.
- Best short candidate:  none clean; TUT/USDT is the short-watch only after a confirmed retest-failure with funding normalizing — the desk's own report rejected a fresh short today on squeeze risk.
- Best catalyst-backed candidate: ATOM/USDT — two-sided catalyst, unchanged since 11:39; wait for a confirmed breakdown with volume before treating it as bearish.
- What to avoid:         TUT/USDT (deepest, longest-unresolved breach, unchanged) and any fresh long chase on PROM/USDT at the current extended print.
- What would change the view: a BTC/ETH close outside the current range with volume confirmation, a fresh catalyst on ATOM resolving the two-sided narrative, or a human reconciling the outcome-tracker's true open-book state (252 stale rows, 3 untracked alerts).

## 7. Candidate Deep Dives

### PROM/USDT — existing position approaching TP1 (not a fresh long-watch)
- Active signal: `sig_b108351df18809d4`, B-tier swing long, entry 6.5825-6.8355, invalidation 6.27326, TP1/2/3 7.510/8.073/8.635, status `triggered`, expires 2026-09-06.
- External cross-check (CoinGecko, live): **$7.18, +38.7% 24h**, intraday range $5.17-$7.81 — up further from $6.948 at the 11:39 review. Price is now closer to TP1 (7.510, ~4.6% away) than to the top of its own entry zone (6.836).
- Derivatives: funding neutral across cycles (5e-06 to -4.98e-05), OI +22-24%, no squeeze signal either way; volume ratio 0.51-0.77x of the 20-period average (not confirming with outsized volume despite the price move).
- Today's intraday report explicitly demotes a fresh PROM idea to watchlist-only C-tier (score 53.7) citing "no-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation"; the swing B-tier idea in today's 07:34 report is the same already-tracked signal, not a new one.
- Chase/entry check for any NEW position: at $7.18 a fresh entry would be buying within ~4.6% of TP1 on an already-tracked position — this is not a long-watch opportunity, it is an existing trade approaching its own target.
- Would invalidate the existing long: a close back below 6.27326, or a broader BTC/ETH breakdown dragging RS leaders down with it.

### DEXE/USDT — improving, no longer a fresh confirmed breach (existing long, still unresolved)
- Active signal: `sig_5b59fe4d0138325c`, B-tier swing long, entry 2.4777-2.5547, invalidation 2.38346, status `triggered`, expires 2026-09-05.
- External cross-check (CoinGecko, live): **$2.35, +2.4% 24h**, 7d change +25.1%, volume ~$47.3M across 35 exchanges — a clear recovery from $2.28 (-5.4% 24h) three hours ago. Price is now only ~1.4% below the 2.38346 invalidation, not a clean confirmed breach anymore, though not yet reclaimed either.
- `detect_untracked_legacy_alerts --since 2026-08-29` still returns the identical DEXE/USDT swing-long alert (score 65.0, sent 2026-08-29T14:36:42 UTC) with no backing `proposed_signal` — untracked, now **~22h22m unresolved, 7th+ consecutive review**.
- No funding/OI data was sampled for DEXE in either of today's top-8 derivatives tables — squeeze risk on any short here remains genuinely unknown.
- Chase/entry check: given the recovery, a fresh short here would now be counter-trend against a 24h+7d uptrend; the actionable short-watch trigger (a confirmed retest failure below ~2.28 after consolidation) has moved further away, not closer.
- Manual review of the existing open long remains the priority — the tracker has not reconciled the position at any point across seven consecutive reviews spanning both the breach and this recovery.

### TUT/USDT — AVOID / manual review (existing long, unchanged breach)
- Active signal: `sig_c7ce9835f38c40a8`, B-tier swing long, entry 0.05164-0.05250, invalidation 0.05058, TP1/2/3 0.0554/0.0573/0.0598, status `triggered`, expires 2026-09-03.
- Today's scalp report lists TUT/USDT as the weakest symbol on the desk, bias short, 24h -17.07% (this figure reflects a different lookback window than the spot 24h change below — both internally consistent, not contradictory).
- External cross-check (CoinGecko, live): **$0.03550, -7.6% 24h** — essentially unchanged from $0.03565 (-10.4% 24h) at 11:39; ~29.8% through the 0.05058 invalidation.
- Today's scalp report explicitly rejected a fresh TUT short idea for "extreme negative funding against short" — shorts remain crowded, so a fresh short here still carries squeeze risk even though the position is confirmed weak.
- No fresh internal `news_items` catalyst found for TUT in the last 24h — the move continues to be pure price action, not news-driven.
- Not applicable to a fresh entry — the open long needs manual review, not a new trade decision. Would invalidate the "avoid new" call: a confirmed reclaim back above the original entry zone (0.0516+) with volume — none observed.

### ATOM/USDT — catalyst-watch (unchanged, no existing position, two-sided catalyst)
- Top-importance catalyst again this cycle: exploit_hack, importance 0.77 (down slightly from 0.81) — same underlying story as 11:39 (Cosmos Labs' own process failure disclosure over the six-chain hack, not a new exploit).
- No new resolving information found this cycle for either side of the two-sided thesis (bearish hack-disclosure overhang vs. bullish deflationary-tokenomics narrative surfaced at 11:39) — treated as unchanged rather than re-verified from scratch, per the source-discipline rule against re-running external research when nothing has moved.
- No active desk position on ATOM/USDT — clean catalyst-watch, no contradiction risk.
- Actionable trigger: unchanged — a confirmed breakdown with volume on continued negative reaction to the disclosure; current level still digesting a mixed narrative, not yet a clean short.

### ZKP/USDT & PROM/USDT untracked alerts (system-integrity, new this cycle)
- `detect_untracked_legacy_alerts --since 2026-08-30` returns two new rows: ZKP/USDT (B, intraday, score 65.3, long, sent 2026-08-30T12:11:46 UTC) and PROM/USDT (B, intraday, score 69.3, long, sent 2026-08-30T12:11:47 UTC), both `trackable=NO`.
- Direct DB lookup: ZKP/USDT's closest matching prior signal is `sig_a319dbba8a7bd56e` (intraday, score 65.3 — exact match, status `stopped`, created 2026-08-30T03:53:10 UTC, ~8h18m before the alert fired). PROM/USDT's closest match is `sig_3a566c58d57c15f1` (intraday, score 69.3 — exact match, status `missed_no_entry`, created 2026-08-30T00:43:07 UTC, ~11h29m before the alert fired).
- This is concrete new evidence for the known watchlist-alert-reuse pattern (previously documented on ALLO/USDT, BANK/USDT, and now the still-unresolved DEXE/USDT): the alert path appears to be re-firing with an older closed signal's exact score rather than generating a fresh `proposed_signal` at alert time. See §14 TODO for the escalated writeup.

### UNH/USDT (stocks, watch-only) — unchanged legal-risk cluster
- No new headline surfaced this cycle beyond the six sources already corroborated at 11:39 (Brach Eichler, Simply Wall St, Yahoo Finance, healthexec.com, QuiverQuant, TipRanks) on the DOJ criminal Medicare-fraud probe.
- Active desk signals on UNH remain both C-tier (one long, one short — contradictory bias, but C-tier is never actionable by design).
- Stocks market closed today (Sunday); the pre-US-open overlay this slot found zero eligible candidates (market closed), so UNH was not and could not be scored by the overlay — this is planning context for Monday's cash open, not an actionable item now.
- Per §I discipline: any UNH A/B signal that forms ahead of Monday's open should be treated as `MANUAL REVIEW REQUIRED`, not a clean actionable, given the corroborated DOJ-probe legal risk.

## 8. Best Candidates Ranked

1. **ATOM/USDT** (catalyst-watch, two-sided) — wait for a confirmed breakdown with volume; unchanged since 11:39.
2. **ZK/USDT** (long-watch) — existing tracked waiting_for_entry zone 0.008972-0.009088; the desk's only non-extended tracked crypto long.
3. **DEXE/USDT** (improving, manual-review priority) — recovering toward its own invalidation; resolve the existing open long manually before considering any new position.
4. **TUT/USDT** (avoid / manual review) — do not add; existing long remains ~29.8% through its own invalidation, unchanged.
5. **PROM/USDT** (existing position, not a long-watch) — running toward TP1 (7.510); do not chase a fresh entry at $7.18.
6. **UNH/USDT** (stocks watch-only) — carry the unchanged DOJ-probe legal-risk cluster into Monday's pre-open review; C-tier only today, not actionable.

No clean, unconditional "trade now" candidate exists this cycle — every entry above is trigger-gated or already-open, per PART 9.

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and the scheduler continue regardless.

- **TUT/USDT**: existing long confirmed ~29.8% through invalidation via live CoinGecko cross-check, unchanged from the last review; avoid adding, flag for manual review.
- **PROM/USDT (new entries)**: existing long has run to $7.18 (+38.7% 24h), close to its own TP1 — a fresh entry now would be chasing an already-extended move, not a long-watch setup.
- **Crypto scalp mode (all symbols)**: kill-switched at the mode level today per today's scalp report ("crypto_scalp_disabled (kill-switch: mode off, any hour/day)" applied to every scalp candidate) — not a market call, a standing configuration.

## 10. Main Risks

- **Untracked-watchlist-alert bug has escalated, not resolved**: 1 unresolved instance (DEXE/USDT, ~22h) at 11:39 → 3 instances now (DEXE/USDT + 2 same-day recurrences on ZKP/USDT and PROM/USDT), with concrete new evidence this cycle (exact score match to older closed signals) narrowing down the likely mechanism.
- **Outcome-tracker lifecycle bug remains fully unresolved**: 252 stale-open-status rows (36 crypto B-tier, 3 stocks A-tier, 16 stocks B-tier, 197 stocks C-tier), identical count to the 11:39 sweep — no backfill has occurred. This continues to undermine confidence in every "triggered"/"tp1_hit"/"tp2_hit" label used throughout this review and the stocks A/B headline stat (n=13, still small enough to be materially skewed by even a couple of misclassified rows).
- **Two open longs diverging in opposite directions on the same desk**: DEXE/USDT is recovering (was breached, now ~1.4% below invalidation) while TUT/USDT remains flat-breached (~29.8% through) — the desk's book cannot currently express a risk-off view even though the market carries a genuine, slightly worsening risk-off macro overlay, because it is structurally 100% long with zero shorts generated across the last 315-signal sample.
- **Catalyst mapping remains weak this run** (52.2% unmapped) — treat the catalyst layer as context, not a gating input.
- **UNH DOJ-probe cluster** carries unchanged into Monday's pre-open/US-open-reaction slots — a real legal-risk item, not yet actionable today.

## 11. Action Plan — next 4 hours

- No new crypto entries recommended this window beyond the existing tracked book; treat PROM/USDT as a position management item (approaching TP1), not a new-entry candidate.
- Continue watching ATOM/USDT for a technical setup to form around the unchanged two-sided catalyst; nothing tracked yet.
- Human/manual: review DEXE/USDT (recovering, ~1.4% below invalidation) and TUT/USDT (flat-breached, ~29.8% through) open longs against current price action — they are now diverging, not moving together, which changes the manual-review priority (DEXE may reclaim on its own; TUT shows no such sign).
- Human/manual: the escalated untracked-alert finding (3 instances now, with a concrete score-reuse mechanism identified on PROM/USDT) warrants prioritizing the watchlist-alert-reuse debugging session flagged in prior reviews — see §14.
- Stocks: no action, market closed; the pre-US-open overlay correctly found nothing to score. Carry UNH forward with its legal-risk flag into Monday's pre-open (target 08:50 ET) and US-open-reaction (18:30 EEST) slots.

## 12. Final Verdict per Mode

- **Crypto scalp**: avoid — mode kill-switched today, no new entries regardless of setup quality.
- **Crypto intraday**: wait-for-trigger — 0 fresh A/B this cycle; ZK/USDT is the cleanest tracked long-watch.
- **Crypto swing**: wait-for-trigger on ATOM/USDT; manual-review priority on TUT/USDT (unchanged breach) and DEXE/USDT (improving but unresolved); PROM/USDT reclassified from long-watch to position-management (approaching TP1).
- **Stocks intraday/swing/invest**: closed/planning-only — pre-US-open overlay found zero eligible candidates (Sunday); UNH carries an unchanged legal-risk flag into Monday.

## 13. Sources

- [Tutorial (TUT) live price](https://www.coingecko.com/en/coins/tutorial) — CoinGecko, fetched 2026-08-30 ~13:0x EEST, $0.03550, -7.6% 24h.
- [DeXe (DEXE) live price](https://www.coingecko.com/en/coins/dexe) — CoinGecko, fetched 2026-08-30 ~13:0x EEST, $2.35, +2.4% 24h.
- [PROM (Prometeus) live price](https://www.coingecko.com/en/coins/prom) — CoinGecko, fetched 2026-08-30 ~13:0x EEST, $7.18, +38.7% 24h.
- [Bitcoin and ethereum prices today, Thursday, August 20, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-august-20-2026-crypto-prices-surge-after-president-trump-pushes-for-clarity-act-154014757.html) — Yahoo Finance (context source used for BTC/ETH macro check; near-term BTC $77,844/-3.13%, ETH $2,471.80/+0.1% figures drawn from this search's aggregated results).
- Internal: `data/catalysts/2026-08-30/catalyst_cycle_10-25.md`, `catalyst_events.jsonl` (1415 cumulative rows).
- Internal: `db/crypto_ai_desk.sqlite` `proposed_signals`/`watchlist_alerts`/`news_items` read-only lookups, run 2026-08-30 ~13:0x EEST.
- Internal: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_1139.md` (previous review, for continuity/diff).

## 14. Fix Requests / TODO

### TODO-watchlist-alert-reuse-escalation-2026-08-30 (ESCALATED — was 1 instance, now 3, with new mechanism evidence)
- **issue:** The untracked-watchlist-alert bug (alerts sent to Telegram with no backing `proposed_signal`, so they never contribute to PF/winrate/avgR) escalated from 1 unresolved instance at the 11:39 review (DEXE/USDT, ~21h old at that point) to **3** at this review: DEXE/USDT (still unresolved, now ~22h22m), plus two brand-new same-day recurrences, **ZKP/USDT** and **PROM/USDT**, both sent 2026-08-30T12:11:4x UTC. New this cycle: a direct DB lookup found the **exact mechanism** — ZKP/USDT's untracked alert score (65.3) exactly matches an older, already-`stopped` intraday signal (`sig_a319dbba8a7bd56e`, created ~8h18m earlier); PROM/USDT's untracked alert score (69.3) exactly matches an older, already-`missed_no_entry` intraday signal (`sig_3a566c58d57c15f1`, created ~11h29m earlier). This is strong evidence the alert-sending path is re-firing with a stale/closed signal's cached score rather than generating (or correctly linking to) a fresh `proposed_signal` at alert time — consistent with, and now more precisely characterizing, the `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug` memory (previously confirmed on ALLO/USDT and BANK/USDT, raised to high priority 2026-07-17).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-30` (2 new rows) and `--since 2026-08-29` (3 total rows) at ~13:0x EEST 2026-08-30. DB cross-reference: ZKP/USDT alert score 65.3 == `sig_a319dbba8a7bd56e` score (intraday, status=stopped, created 2026-08-30T03:53:10 UTC); PROM/USDT alert score 69.3 == `sig_3a566c58d57c15f1` score (intraday, status=missed_no_entry, created 2026-08-30T00:43:07 UTC).
- **suggested manual fix:** (1) trace the watchlist-alert-sending code path specifically for how it selects/attaches a `signal_id`/score at send time — the exact-score-match evidence suggests it may be querying the most recent signal for symbol+mode without checking whether that signal is still open; (2) add a guard that refuses to send (or explicitly marks as "reused/stale") an alert whose matched signal is already in a closed status (`stopped`, `missed_no_entry`, `expired`, etc.); (3) once fixed, backfill a proper `proposed_signal` for the 3 currently-untracked alerts if they still represent live opportunities, or explicitly mark them dead; (4) this is now confirmed on 4 distinct symbols (ALLO, BANK, DEXE, ZKP, PROM — 5 total) across at least 7 consecutive scheduled reviews — recommend explicit human sign-off that a dedicated debugging session is scheduled using the PROM/USDT case (cleanest reproduction, exact score match) as the primary test case.
- **priority:** high (escalating count, first time the underlying mechanism has concrete evidence)
- **first observed:** 2026-07-17 (per memory); this cycle's ZKP/PROM recurrences and score-match evidence newly observed 2026-08-30 16:07 EEST.

### TODO-lifecycle-status-gap-unchanged-2026-08-30 (carried forward, unchanged — no backfill has occurred)
- **issue:** The broader lifecycle-status bug first fully quantified at the 11:39 review (252 rows with `expires_at < now()` while `status` still reads an open value: 36 crypto B-tier, 197 stocks C-tier, 16 stocks B-tier, 3 stocks A-tier) is **still exactly 252 rows with the identical tier breakdown** at this review, ~4.5 hours later. This confirms no reconciliation, backfill, or fix has been applied between reviews — the stocks A/B headline stat (n=13, WR 60%, PF inf) remains unverified/unreliable per the same reasoning as 11:39.
- **evidence:** Re-run of the same SQLite sweep against `db/crypto_ai_desk.sqlite` at ~13:0x EEST 2026-08-30: identical 252-row count and tier breakdown as the 11:39 review's finding.
- **suggested manual fix:** unchanged from the 11:39 review — (1) confirm whether the outcome-checker job covers stocks symbols at all; (2) add an automated sweep/alert for `expires_at < now() AND status NOT IN (closed_states)` across both asset classes; (3) backfill/reconcile all 252 rows' true final status; (4) re-run `signal-stats --asset-class stocks` after backfill; (5) this is now the 6th consecutive review carrying an unresolved instance of this bug family with zero movement in the count — recommend escalating past routine mention to an explicit scheduled maintenance session.
- **priority:** high (unchanged count across two consecutive reviews spanning 4.5h, includes stocks A-tier)
- **first observed:** 2026-07-17 (crypto candle-gap form); broadened scope first fully quantified 2026-08-30 11:39 EEST; confirmed unchanged 2026-08-30 16:07 EEST.
