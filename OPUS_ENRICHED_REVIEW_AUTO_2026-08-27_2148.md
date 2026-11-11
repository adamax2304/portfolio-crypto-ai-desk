# Opus Enriched Review — late-session risk review — Auto Cycle 21:48 EEST

## 1. Executive Summary

- **Slot:** late-session risk review (21:48 EEST / 18:48 UTC — US cash session still open, closes 23:00 EEST). **Advisory only — no auto-trade.**
- Crypto regime: range/chop (neutral) on both scalp (gen 18:42) and intraday (gen 19:32) — no fresh A/B setups produced either cycle. BTC/ETH uptrend, breadth 54.2% >EMA20, but macro risk score elevated (79–94/100, risk-off headwind from Iran/Russia geopolitical headlines).
- Stocks: regime **transition**, VIX 14.64, breadth 100%/100% >EMA20/EMA50 but only 2/4 indices actually trending up. Zero A/B actionable stocks-intraday setups this cycle — all 15 raw-A candidates gate-demoted to C (stale-post-earnings, rolling paper-R drawdown guard, or legal/headline risk). Three B-tier waiting_for_entry longs from the 18:39 cycle (NVDA, INTC, CRM) are still open and unfilled, unchanged.
- **Risk flag this cycle:** ONG/USDT carries 3 open B-tier LONG swing signals (1 triggered/live since 08-26, 1 waiting_for_entry since 08-27 04:46) while both the scalp and intraday reports independently list it in "Weakest Symbols" with bias=short and 24h return −26% to −31%. This is a fresh instance of the known bias-tag-contradiction pattern already tracked at high priority in project memory — flagged NEEDS REVIEW, see §7 and §14.
- 7 untracked legacy crypto alerts confirmed again this cycle (known bug, TODO-3 already high-priority, not re-escalating).
- No new external verification was required this cycle — all deep-dive candidates are backed by internal report/catalyst data generated within the last 3 hours and internally consistent across cycles.

## 2. Data Used

- Crypto reports: scalp (gen 2026-08-27 18:42 EEST, data freshness 15:30 UTC), intraday (gen 19:32 EEST, data freshness 16:15 UTC). Both range/chop, both zero A/B.
- Stocks reports: intraday (gen 21:31 EEST, data freshness 18:31 UTC — 8 min old, very fresh). Stocks swing/invest: **stale since 2026-07-02** (~8 weeks), excluded (recurrence of already-tracked TODO, not re-raised as new).
- `active-signals --asset-class crypto` (50-row sample, capped) and `--asset-class stocks` (50-row sample, capped).
- `signal-stats --asset-class crypto` (full breakdown by tier/mode/direction/exchange) and `--asset-class stocks`.
- `detect_untracked_legacy_alerts --since 2026-08-27` → 7 hits.
- `data/catalysts/2026-08-27/catalyst_events.jsonl` — full-day count: 2500 rows, 633 mapped / 1867 unmapped (74.7% unmapped).
- `db/crypto_ai_desk.sqlite` direct query on `proposed_signals` for ONG/USDT history (10 most recent rows) to verify the bias-contradiction flag.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_1839.md` (US open reaction review, 18:39 EEST).
- External web research: **not required this cycle** — all candidates (KITE, ONG, ENA/ZRO, ZEC) are backed by internal catalyst/report data generated in the last 1–3h and consistent across at least two independent report cycles today.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 21:38 EEST (10 min old at check time) — **fresh**, no defer.
- Latest `cycle_01_13-24_summary.md` mtime unchanged from earlier in the day (~8h old) — the running scheduler.log is the authoritative freshness signal per the deferral rule (both would need to be >3h stale to defer; scheduler.log alone is fresh).
- Crypto scalp: ~1h old — fresh. Crypto intraday: ~15min old — fresh. Crypto swing: not re-read this cycle (last known gen 12:46 EEST, ~9h old at this point) — not used for regime call this cycle since scalp/intraday already agree on range/chop.
- Stocks intraday: 8 min old — very fresh, freshest report of the day.
- Stocks swing/invest: stale >14h (actually ~8 weeks) — excluded from all verdicts, consistent with prior cycles.
- No explicit paper-portfolio equity snapshot read this cycle (out of the allowed read set for this run).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-08-27 21:48 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["swing report not re-read this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 21:38 EEST", "stocks intraday report gen 21:31 EEST (8min old)", "stocks swing/invest last gen 2026-07-02 — recurring known staleness"] },
    { "agent": "market_regime", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["chop", "mixed", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp+intraday both range/chop (neutral)", "BTC/ETH uptrend but breadth only 54.2% >EMA20", "stocks regime=transition, VIX 14.64, only 2/4 indices trending up", "macro risk 79-94/100, risk-off headwind"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["74.7% of today's catalyst events unmapped (633/2500 mapped)", "ENA/USDT explicitly tagged catalyst-backed in momentum_breakout basket", "ZRO/USDT fresh LayerZero ATLAS catalyst, primary_source"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.45,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["cross-venue OI for most C-tier/watchlist names"],
      "suggested_effect": "advisory_only",
      "facts_used": ["MOVR OI +105% 24h (intraday report)", "VET OI +67%", "TRUMP/CHIP price-up+OI-up fresh positioning, crowding normal"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "overextended", "entry_late"], "data_missing": ["TradingView / manual chart check unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/CHIP >2 ATR from EMA20, rejected as chase risk in scalp report 7b", "KITE/USDT watchlist-only, conditional pullback zone not yet reached"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.55,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "needs_review"], "data_missing": ["exact entered-unresolved vs no-entry split not computed this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals (50 capped): 36 triggered, 7 tp1_hit, 7 waiting_for_entry", "stocks active-signals (50 capped): 45 C-tier waiting_for_entry (not actionable), 3 B-tier waiting_for_entry (NVDA/INTC/CRM, unchanged since 18:39), 2 C-tier tp1_hit"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["repeated_losses", "manual_review", "correlation_cluster"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONG/USDT: 3 open B-tier LONG swing signals vs bias=short/-26% to -31% 24h in two independent same-day reports — bias-tag contradiction, known pattern (project memory, escalated HIGH 2026-08-08)", "crypto RS/momentum long book (triggered names) is BTC-correlated concentration risk", "NVDA still carries operator-review flag, tag-hygiene issue tracked since 18:39 review, unresolved"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier week: PF 1.69, avgR 0.155, totalR 53.1, winrate 12.6% (n=451)", "crypto scalp mode: PF 0.05, avgR -0.086, totalR -9.5 (n=142) — net negative, matches report's own low-confidence banner", "crypto intraday mode: PF 1.98, avgR 0.389, totalR 40.1 (n=166) — strongest performer", "stocks A/B week: n=10 (weak sample), totalR 12.0, PF inf (0 losses) — too small to trust; stocks-intraday paper_execution_r 30d: -9.7R/PF0.28 (longs -7.7R/PF0.18 n42, shorts -2.0R/PF0.50 n23) — longs materially weaker than shorts on the real (non-headline) execution model" ] },
    { "agent": "head_trader", "verdict": "normal", "confidence": 0.55,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": [] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "KITE/USDT", "trigger": "1h close/pullback fill into 0.1263-0.1278 zone with volume; currently watchlist-only, score 63.7, below active threshold", "reason": "highest-scoring fresh idea in both cycles today (95-96.5 momentum rank), RS-leader, but no fresh verified catalyst — needs confirmation, not a chase at current price" },
    "best_short_candidate":    { "symbol": "ONG/USDT", "trigger": "confirms as short-watch only after operator clears/closes the contradictory open longs; do not initiate a NEW short while 3 stale longs remain open on the same symbol", "reason": "weakest RS in both reports today (-26% to -31% 24h), also flagged in discovery-expansion watchlist as weak_rs_short candidate (score 68) — but the open long book on the same symbol must be resolved first (see NEEDS REVIEW)" },
    "best_catalyst_candidate": { "symbol": "ENA/USDT", "trigger": "pullback into the intraday report's positioning zone; explicitly tagged catalyst-backed (not a no-catalyst chase) in the momentum_breakout basket — do not chase the current extended print", "reason": "primary_source-verified catalyst basket membership, price+OI both up (fresh positioning, funding not extreme), already has an open triggered swing signal" },
    "avoid_candidate":         { "symbol": "ONG/USDT", "reason": "3 open B-tier long swing signals contradicted by two independent same-day reports showing bias=short and 24h -26% to -31% — needs operator review before any new action, long or short, on this symbol" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | ok | 0.60 | chop, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.45 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, overextended, entry_late | advisory_only |
| execution_lifecycle | ok | 0.55 | open_actionable, waiting_for_entry, review_shadow, needs_review | advisory_only |
| risk_manager | caution | 0.60 | repeated_losses, manual_review, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | normal (caution overall) | 0.55 | — (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (18:39 EEST — US open reaction review)

- **NVDA/INTC/CRM (stocks B-tier waiting_for_entry)** — unchanged, none of the three has triggered a fill since 18:39; all three still sit at their original entry levels (247.61 / 92.51 / 226.95) with the same expiry windows. No new post-open confirmation candle observed.
- **Crypto scalp/intraday** — both moved to zero A/B this cycle (was also zero at 18:39; the swing report at 15:45 had the only bullish RS-momentum cohort, not re-read this cycle).
- **ONG/USDT bias contradiction** — **new this cycle.** Not flagged at 18:39 (ONG wasn't part of that review's candidate set). Newly surfaced via the weakest-symbols cross-check against the open signal book.
- **Catalyst mapping** — 74.7% unmapped today (full-day count) vs 78.2% at 18:39 (partial-day sample) — roughly stable, still weak.
- **7 untracked legacy crypto alerts** vs 6 at 18:39 — one additional alert accrued (SOL/USDT scalp at 18:21 UTC), same known bug pattern, not re-escalating.
- **NVDA tag-hygiene issue** (exploit_hack mis-tag on the Hugging Face M&A story) — persists unchanged from 18:39, still unresolved, cross-referenced not re-raised.
- **Stocks swing/invest staleness** — persists unchanged (still 2026-07-02), cross-referenced not re-raised.

## 5. Catalyst Coverage

- `catalyst_events.jsonl` (2026-08-27, full-day count): **633 mapped / 1867 unmapped → 74.7% unmapped.**
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (macro commentary, not symbol-specific):
  1. "BOJ'S HIMINO: FINANCIAL CONDITIONS STAY ACCOMMODATIVE, BELIEVE WE SHOULD EASE OFF ACCELERATOR TIMELY" (t.me/marketfeed)
  2. "BOJ'S HIMINO: THE BIGGEST CHALLENGE IN OUR COMMUNICATION IS THE ISSUE OF TIME HORIZONS" (t.me/marketfeed)
  3. "BOJ'S HIMINO: EFFECTIVE USE OF MONETARY POLICY CAN STOP ECONOMY VEERING FROM PATH TO SOLID GROWTH" (t.me/marketfeed)
- 5 narrative baskets active today (latest cycle_16-50): `rwa_narrative`, `perps_dex_narrative`, `delisting_thin_liquidity`, `binance_ecosystem_teaser`, `momentum_breakout` (the last explicitly separates ENA/USDT as catalyst-backed from the no-catalyst MOVR/CHIP/TRUMP/KITE/ZRO cohort in the same basket).
- Stocks-side: production `news_supported` only 3.4% of A/B/C signals over 7d vs a 24h exact-match shadow window of 82.0% — the production scan window materially under-fires (already-tracked known issue, catalyst-linkage TODO in project memory, not re-raised).

## 6. Market Landscape

Crypto: BTC and ETH both in uptrend on price, but breadth is middling (54.2% of tracked symbols above EMA20, 77.1% above EMA50) and both reports independently classify the regime as range/chop (neutral) rather than trending. Macro/geopolitical risk score is elevated (79.3–94.0/100 across the two cycles) driven by Russia spending cuts / war-cost headlines, Iran sanctions widening, and Saudi-Houthi escalation risk — a genuine risk-off headwind sitting underneath an otherwise BTC-led uptrend. Stocks: regime label **transition**, bias neutral, VIX low at 14.64 (not stressed), but only SPY and DIA are actually trending up (QQQ and IWM are range-bound) — index-level breadth stats (100%/100% >EMA20/EMA50) look strong but the underlying trend read is mixed. NVDA's earnings beat + Hugging Face M&A story remains the dominant single-name narrative for a second consecutive review cycle; technology and energy are the strongest sectors (RS +2.78%/+2.40% vs SPY), utilities and real estate the weakest.

### Market Mood / Risk Routing
- Crypto mood: **chop / mixed** (range/chop regime label, breadth only 54.2% >EMA20, elevated macro risk-off score)
- Stocks mood: **transition / mixed** (VIX low-normal, indices split trend vs range, session still open until 23:00 EEST)
- Dominant narrative: NVDA earnings-beat + Hugging Face M&A talk (2nd consecutive cycle); crypto RS-momentum in TRUMP/CHIP/MOVR cohort but all >2 ATR from EMA20 (chase risk, explicitly rejected in this cycle's reports)
- Preferred side now: **wait-for-trigger** — chop regime plus elevated macro risk argues against fresh chase entries on either side; existing triggered positions should be managed, not added to
- Best long candidate: KITE/USDT (watchlist-only, needs pullback fill) — see §7
- Best short candidate: ONG/USDT (weak-RS candidate, but blocked by an unresolved open-long contradiction on the same symbol — see NEEDS REVIEW)
- Best catalyst-backed candidate: ENA/USDT — catalyst-confirmed within its basket, do not chase the extended print
- What to avoid: chasing TRUMP/CHIP at current extended price (>2 ATR from EMA20, explicitly rejected in-report); any new ONG/USDT action pending operator review; AFRM/MRVL into today's earnings; HON/ATOM under live operator-review flags
- What would change the view: a pullback fill into KITE's stated zone; operator resolution of the ONG/USDT long/short contradiction; a confirmed post-open fill on NVDA/INTC/CRM before the US close (23:00 EEST, ~1h15m away)

## 7. Candidate Deep Dives

### 1. ONG/USDT (crypto) — NEEDS REVIEW / avoid new action
- **The contradiction:** `proposed_signals` shows 3 currently-open B-tier LONG swing/scalp-derived signals: `sig_5fc650550d967342` (swing, waiting_for_entry, entry 0.0940-0.1090, invalidation 0.0870, opened 04:46 UTC today) and `sig_8d3a8fd71bf0bf75` (swing, **triggered**/live, entry 0.0956-0.0982, invalidation 0.0924, opened 2026-08-26 10:08 UTC) — plus a scalp `tp1_hit` from 2026-08-25.
- Both the 18:42 scalp report and the 19:32 intraday report independently list ONG/USDT under "Weakest Symbols": bias=short, 24h -26.09% (scalp) and -30.75% (intraday), RS vs BTC -29% to -34%.
- This is the same pattern already documented in project memory (`project_crypto_ai_desk_bias_tag_contradiction.md`, escalated HIGH 2026-08-08, previously confirmed on ZBT/ACE) — ONG/USDT is a fresh third instance.
- Given a -30% 24h move, the live triggered swing signal's invalidation (0.0924) is very likely already breached, but this run's read-only tools do not expose a live tick price to confirm the exact stop status — flagged as data_missing.
- Is this candidate aligned with mood? No — it is a long book on a symbol the same-day reports independently classify as the weakest short-bias name.
- What would invalidate/resolve: operator confirms current ONG/USDT price against the 0.0924 invalidation level and either marks the triggered signal stopped or confirms it is still valid; until then, treat as NEEDS REVIEW, not tradeable in either direction.
- **Is this a chase-risk setup?** N/A — this is a risk-flag on an existing position, not a new entry.

### 2. KITE/USDT (crypto, intraday, watchlist-only C-tier) — best long-watch
- Score 63.7/100 (intraday report Trade Idea #1), confidence medium, playbook `crypto_intraday_catalyst_or_momentum`.
- 24h return +11.85%, 7d +30.89%, RS vs BTC +8.62%, volume 1.98x average — genuinely the strongest fresh-momentum name in both today's scalp (score 95, rejected for scalp kill-switch) and intraday (score 96.5) reports.
- No fresh verified catalyst — known failure mode explicitly noted in-report: "No-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation" (14d cut: WR 23% / PF 0.70 / −3R for this exact playbook-without-catalyst combination).
- Has price already reacted? Yes, current price 0.1284 is above the stated pullback entry zone (0.1263-0.1278) — a market entry now would be marginally late.
- Actionable now or after confirmation: **after confirmation only** — wait for the pullback zone or a fresh catalyst; the report itself flags this as watch-only.
- Aligned with mood: partially — RS-leader quality is good, but the no-catalyst-in-chop failure mode argues for caution given tonight's range/chop + risk-off macro backdrop.
- Invalidates on: 1h close beyond 0.1245.

### 3. ENA/USDT (crypto, catalyst-backed, open triggered swing signal) — best catalyst-watch
- Explicitly separated as catalyst-backed within the `momentum_breakout` narrative basket (cycle_16-50): "ENA/USDT — treat as catalyst-backed, watch pullback / do NOT chase; NOT a no-catalyst momentum chase."
- Derivatives: price up + OI up (fresh positioning confirms trend), funding not extreme, crowding normal (scalp report §3).
- Already has an open `triggered` B-tier swing signal (entry 0.1623-0.1642, from active-signals list) — this is management of an existing position, not a fresh entry decision tonight.
- Has price already reacted? Partially — 24h +20.89% (intraday report) — the catalyst is not brand-new but the basket confirms it is still catalyst-supported, not a pure chase.
- Actionable now: existing position stands; do not add on the current extended print.

### 4. NVDA / INTC / CRM (stocks, intraday, B-tier waiting_for_entry) — unchanged, still pending
- All three unchanged since the 18:39 review: NVDA waiting at 226.95 (invalidation 225.675, manual-review pending due to the unresolved exploit_hack mis-tag), INTC waiting at 92.51 (invalidation 91.56, no flags, semiconductor sector tailwind), CRM waiting at 247.61 (invalidation 245.36, no flags).
- None has converted to a live triggered fill in the ~3h since the last review — with the US cash session closing at 23:00 EEST (~1h remaining), these are increasingly likely to expire the day unfilled rather than trigger.
- Actionable now or after confirmation: still after confirmation only for INTC/CRM; NVDA remains manual-review-only pending tag reclassification (unresolved TODO from 18:39, cross-referenced not re-raised).
- What would invalidate: session close without a fill converts these from "waiting" to effectively stale for the day — worth flagging as likely no-entry by end of session if unfilled.

### 5. TRUMP/CHIP/RUNE/CATI cohort (crypto, swing, triggered — open positions) — manage, don't chase
- All four remain in `triggered` status per active-signals (open, running). This cycle's reports independently reject fresh entries on TRUMP/CHIP: "Price is more than 2 ATR from EMA20; do not chase" (scalp report §7b).
- Playbook `crypto_swing_narrative_rs_momentum` carries a strong stated historical track record (per playbook hint text elsewhere in the desk), but tonight's setup-quality read on this specific cohort is explicitly capped by the chase-risk rejection.
- Actionable now: no new entries; existing open positions should be managed against their stated invalidation levels, not added to at current extended prices.

## 8. Best Candidates Ranked

1. **ONG/USDT** — NEEDS REVIEW (highest priority tonight — an active risk-integrity flag, not a trade idea).
2. **KITE/USDT** (long-watch, crypto) — best fresh momentum idea, wait for pullback fill into 0.1263-0.1278, no catalyst yet.
3. **ENA/USDT** (catalyst-watch, crypto) — manage the existing open position, catalyst-confirmed, do not add at current extended price.
4. **NVDA/INTC/CRM** (stocks, watch-only) — unchanged since 18:39, increasingly likely to expire unfilled as the 23:00 EEST close approaches.
5. **TRUMP/CHIP/RUNE/CATI cohort** (crypto, manage-only) — open, chase-risk explicitly flagged for fresh entries tonight.

## 9. Avoid / No Trade (this decision window only)

- **ONG/USDT** — any new long or short action pending operator review of the bias contradiction (see §7).
- **TRUMP/CHIP** — fresh entries rejected in-report for chase risk (>2 ATR from EMA20).
- **NVDA** — manual review required (tag-hygiene issue, unresolved since 18:39).
- **AFRM, MRVL** — earnings today; do-not-chase into the print.
- **HON, ATOM** — live `block_requires_operator_review` flags (Honeywell investigation, Cosmos Labs exploit-hack warning).
- This is a decision-window verdict only — scanning, candidate generation, tracking, and the scheduler continue in all cases; nothing here recommends pausing any part of the system.

## 10. Main Risks

- **ONG/USDT bias-tag contradiction** (see §7) — the most concrete risk-integrity issue this cycle; a third recurrence of an already-HIGH-priority tracked bug pattern.
- **Session-close risk**: NVDA/INTC/CRM stocks longs have ~1h15m left in the RTH session before likely expiring unfilled for the day.
- **Crypto macro risk-off headwind** (79-94/100 macro risk score) sitting underneath an otherwise BTC-led uptrend — a genuine source of late-session reversal risk that a pure price/technical read would miss.
- **Catalyst mapping weak (74.7% unmapped)** — do not over-weight the catalyst layer for any single-name decision this cycle.
- **7 untracked legacy crypto alerts today** — confirmed recurrence of the known watchlist-alert/signal-reuse bug (TODO-3, already high priority in project memory).
- **Stocks swing/invest pipeline** still has zero fresh reports since 2026-07-02 (~8 weeks) — persists unchanged, cross-referenced not re-raised.

## 11. Action Plan — next 4 hours

- Flag ONG/USDT for operator review before market open tomorrow — verify the live triggered swing signal's status against its 0.0924 invalidation level given the -30% 24h move.
- Watch KITE/USDT for a pullback fill into 0.1263-0.1278; do not chase at the current 0.1284 print.
- Hold ENA/USDT's existing position; do not add at the current extended print; watch for a defined pullback if considering a second entry.
- Watch NVDA/INTC/CRM for a fill in the remaining ~1h15m of RTH; if unfilled by the 23:00 EEST close, treat as no-entry/stale for the day at the next review.
- Do not chase TRUMP/CHIP or the wider RS-momentum cohort at current extended prices; manage existing triggered positions against their stated invalidation levels only.
- Re-check REGN/HON/ATOM/AFRM/MRVL flags at the next cycle before considering any of them.

## 12. Final Verdict per Mode

- **Crypto scalp:** no A/B setups this cycle (report's own banner: low confidence, PF 0.14 over 14d, PF 0.05 this week's mode-level stat) — scanner continues, no new entries recommended.
- **Crypto intraday:** no A/B setups this cycle; strongest weekly performer by mode-level stats (PF 1.98) but nothing fresh to act on tonight — manage existing triggered/waiting orders only.
- **Crypto swing:** existing RS-momentum cohort (TRUMP/CHIP/RUNE/CATI etc.) open and running; no fresh entries — chase risk explicitly flagged tonight.
- **Stocks intraday:** zero fresh A/B this cycle (all 15 raw-A candidates gate-demoted to C); 3 unchanged B-tier waiting_for_entry longs (NVDA/INTC/CRM) approaching likely unfilled expiry as the session nears close.
- **Stocks swing:** stale (2026-07-02) — excluded, cross-referenced not re-raised.
- **Stocks invest:** stale (2026-07-02) — excluded, cross-referenced not re-raised.

## 13. Sources

- Internal: `data/reports/scalp/2026-08-27_15-47_scalp_report.md`, `data/reports/intraday/2026-08-27_16-34_intraday_report.md`, `data/reports/stocks/intraday/2026-08-27_18-31_stocks_intraday_report.md`
- Internal: `data/catalysts/2026-08-27/catalyst_events.jsonl`, `data/catalysts/2026-08-27/narrative_baskets.jsonl`, `data/catalysts/2026-08-27/catalyst_cycle_16-50.md`
- Internal: `active-signals`/`signal-stats` CLI output (2026-08-27 21:4x EEST), `detect_untracked_legacy_alerts --since 2026-08-27`
- Internal: `db/crypto_ai_desk.sqlite` direct query, `proposed_signals` table, ONG/USDT history
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_1839.md`
- No external web sources cited this cycle (see §1 — external research not required).

## 14. Fix Requests / TODO

### TODO-ong-bias-contradiction
- **issue:** ONG/USDT carries 3 open B-tier LONG swing/scalp signals (1 currently `triggered`/live since 2026-08-26 10:08 UTC, 1 `waiting_for_entry` since 2026-08-27 04:46 UTC) while both the 2026-08-27 scalp (18:42 EEST) and intraday (19:32 EEST) reports independently classify ONG/USDT as bias=short with 24h return -26.09% and -30.75% respectively.
- **evidence:** `db/crypto_ai_desk.sqlite` `proposed_signals` query for symbol='ONG/USDT' (signal_ids `sig_5fc650550d967342`, `sig_8d3a8fd71bf0bf75`); `data/reports/scalp/2026-08-27_15-47_scalp_report.md` §2 "Weakest Symbols"; `data/reports/intraday/2026-08-27_16-34_intraday_report.md` §2 "Weakest Symbols".
- **suggested manual fix:** verify ONG/USDT's live price against the triggered signal's invalidation (0.0924); if breached, the signal should have auto-stopped and did not — investigate the stop-monitor path for this symbol/mode. This is a third recurrence of the pattern already tracked in project memory (`project_crypto_ai_desk_bias_tag_contradiction.md`, escalated HIGH 2026-08-08, previously confirmed on ZBT/ACE) — this occurrence should reinforce, not duplicate, that existing high-priority item.
- **priority:** high
- **first observed (this recurrence):** 2026-08-27 21:48 EEST

### TODO-nvda-indictment-tag-mismatch
- **issue:** The current (21:31 EEST) stocks intraday report's §7 C-tier demotion reason for NVDA reads "tier demoted A→C: active legal/headline risk (**indictment**) — manual review required," but the same report's §5c production risk-warning block still tags NVDA under `exploit_hack` citing the Hugging Face M&A/acquisition-talk headline (the same mis-tag already tracked as `TODO-nvda-mistag` in the 18:39 review) — no separate "indictment" news item is visible anywhere in this report's news/catalyst sections for NVDA.
- **evidence:** `data/reports/stocks/intraday/2026-08-27_18-31_stocks_intraday_report.md` line ~382 ("NVDA (long) (was A): ... legal_headline_risk: indictment") vs the same file's §5c NVDA entry (`exploit_hack`, Hugging Face acquisition-talk headline).
- **suggested manual fix:** trace where the "indictment" label in the C-tier demotion reason originates — it may be a stale/cached legal-risk classification from an earlier, unrelated cycle that never cleared, distinct from the exploit_hack mis-tag already logged. Confirm whether NVDA has ever actually carried a genuine indictment-type legal event, or whether this is a second, independent tag-hygiene bug on the same symbol.
- **priority:** medium
- **first observed:** 2026-08-27 21:48 EEST

### TODO-recurring (cross-reference, not new)
- **issue:** 7 untracked legacy crypto alerts again today (EDEN scalp, SOL intraday, S/BICO/SOL/ONT swing, SOL scalp) — same watchlist-alert/signal-reuse bug already tracked as TODO-3 (high priority) in project memory as of 2026-07-17.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-27` → 7 rows, all "NO (no proposed_signal)".
- **suggested manual fix:** no new fix suggested here — confirms the existing high-priority TODO is still unresolved.
- **priority:** high (inherited, not newly raised)
- **first observed (this recurrence):** 2026-08-27 21:48 EEST

### TODO-recurring-stocks-swing-invest-stale (cross-reference, not new)
- **issue:** `data/reports/stocks/swing/` and `data/reports/stocks/invest/` still have not produced a new report since 2026-07-02 — persists unchanged from the 18:39 review's TODO.
- **evidence:** latest files still dated 2026-07-02_13-03 / 2026-07-02_13-05.
- **suggested manual fix:** see prior review's TODO-stocks-swing-invest-stale for the suggested investigation path (intentional deprecation vs silent scheduler failure).
- **priority:** medium (inherited, not newly raised)
- **first observed (this recurrence):** 2026-08-27 21:48 EEST
