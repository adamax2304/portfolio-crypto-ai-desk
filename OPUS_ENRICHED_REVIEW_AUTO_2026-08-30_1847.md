# Opus Enriched Review — US open reaction review — Auto Cycle 18:47 EEST

## 1. Executive Summary

Slot: **US open reaction review** (18:30 EEST target). **Advisory only — no auto-trade.** Today is **Sunday 2026-08-30** — the US cash market is closed all day, so there is no "US open reaction" to score; this slot's stocks content is planning/watchlist context only, carried into Monday's actual open. Crypto is the live actionable class this window. The desk's technical regime flipped to **bullish trend (risk-on)** in the 13:18–14:38 EEST reports (BTC/ETH both uptrend, altcoin breadth 55–82% above EMA20/50) even as the **macro/geopolitics score pinned at 100.0/100 risk-off** (Iran/Hormuz, Kyiv-area strikes) — a genuinely two-layer read: technical momentum up, macro overlay maximally cautious. **DEXE/USDT re-breached**: live price round-tripped from the $2.35 recovery seen at 16:07 back down to **$2.28 (-2.0% 24h)**, ~4.3% below its own 2.38346 invalidation — worse than three hours ago, not better. **TUT/USDT** ticked up slightly to $0.03587 (+2.1% 24h) but remains ~29% through its invalidation, essentially unchanged. **PROM/USDT** cooled from +38.7%→+29.5% 24h ($7.18→$7.01), still an open position running toward TP1, not a fresh long-watch. The known **untracked-alert bug** partially self-resolved this cycle (ZKP/USDT and PROM/USDT's 12:11 UTC alerts now have a matching signal within the detector's window) but **DEXE/USDT remains genuinely and persistently untracked, now ~25h old** — confirming it as the real, non-transient instance. The **252-row outcome-tracker lifecycle-status gap is unchanged**, identical breakdown to the last two reviews. **New this cycle**: a recurring pipeline failure — `refresh_obsidian_dashboard` timing out at 300s — was found in **43 of the last several days' cycle summaries**, a reproducible operational bug (§14). Scanning, tracking, and the scheduler continue uninterrupted regardless of this review's caution stance.

## 2. Data Used

- Reports: `2026-08-30_13-18_scalp_report.md` (~5h29m old at time of writing, carry-forward band), `2026-08-30_13-27_intraday_report.md` (~5h20m old, carry-forward), `2026-08-30_14-38_swing_report.md` (~4h09m old, carry-forward, at the fresher edge of the band) — no newer scalp/intraday/swing generation exists yet this cycle despite the scheduler starting a fresh `cycle_01_16-07` run (that cycle's step list covers monitors/dashboards/daily-review, not a new report generation pass).
- Stocks: `2026-08-28_18-54_stocks_intraday_report.md` (weekend carry-forward, market closed both Sat/Sun); stocks swing/invest `2026-07-02` (long-stale, informational only, per the deprecated old-stocks-swing/invest framework — see `project_crypto_ai_desk_stocks_position_framework` memory).
- Catalysts: `data/catalysts/2026-08-30/catalyst_cycle_13-35.md` (latest cycle, 414 rows), `catalyst_events.jsonl` (1829 cumulative rows today), `narrative_baskets.jsonl` (6 baskets this cycle).
- LLM packet: `llm_analysis_packet.md` (17:40 EEST, fresh, crypto). Stocks packet `llm_stocks_packet.md` (2026-08-28 21:56 — stale, weekend carry-forward).
- CLI: `active-signals` (crypto: 50 rows / stocks: 50 rows, mostly historical/closed-status on the stocks side), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-30` and `--since 2026-08-29`.
- Direct SQLite reads (`db/crypto_ai_desk.sqlite`, read-only): `watchlist_alerts` vs `proposed_signals` lookups for DEXE/ZKP/PROM (untracked-alert continuity check); full-table stale-row sweep (`expires_at < now AND status IN open-states`); `news_items` freshness check for DEXE/TUT/PROM/ATOM/MANTRA (all empty in last 24h except ATOM, one row).
- External: 3 WebFetch (CoinGecko: DEXE, TUT, PROM live pages) + 3 WebSearch (BTC/ETH macro price check, ATOM/Cosmos exploit follow-up, MANTRA/OM price) — see §13. The MANTRA/OM price check returned **contradictory results across sources** (a CoinMarketCap page explicitly labeled "MANTRA (old)" showing $0.006071 vs. a Binance-sourced search snippet showing $3.89 — clearly a stale/mismatched aggregation) and is treated as **unverifiable** this cycle; the ingest script itself rejected that source as not citable.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_1607.md` (pre-US-open decision review, 16:07 EEST).

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-08-30 17:50 EEST (~57min old at time of writing) — **fresh**, no defer.
- Latest cycle: `cycle_01_16-07_summary.md` (17:49 EEST) — this is **cycle 01 of a freshly restarted schedule day** (the scheduler process restarted at 16:07 today, resetting the cycle counter; the prior schedule day had reached cycle 7 before the restart). The cycle's step list is monitor/dashboard/daily-review focused, not a new scalp/intraday/swing report generation — hence no fresher reports than 13:18–14:38 exist yet.
- Scalp/intraday/swing reports: all in the **4–12h carry-forward band** (swing freshest at ~4h09m, scalp/intraday ~5h20-29m) — used as context, cross-checked against live external prices for the three open-long candidates.
- Stocks reports: Aug 28 18:54 (intraday, weekend carry-forward) / Jul 2 (swing, invest — long-stale, informational, deprecated framework).
- Catalyst scan: 16:35 EEST (fresh, <15min at time of writing). LLM packet: 17:40 EEST (fresh).
- **Untracked-alert detector**: `--since 2026-08-30` now returns **0** rows (was 2 new rows — ZKP/USDT, PROM/USDT — at the 16:07 review); `--since 2026-08-29` returns **1** row (DEXE/USDT only, sent 2026-08-29T14:36:42 UTC, now **~25h10m** unresolved) — down from 3 at 16:07. Direct DB cross-check: DEXE/USDT's closest `proposed_signals` row (`sig_5b59fe4d0138325c`, created 2026-08-29T02:54:07 UTC) was created **~11h42m before** the alert fired, well outside the detector's ±6h matching window — this is a genuine, persistent gap, not a timing artifact. The ZKP/PROM recurrences flagged at 16:07 have since picked up a matching signal within the detector's window as later same-day signals were generated for those symbols — **this looks like the two same-day cases were timing-window artifacts, not a repeat of the DEXE-style true gap**, though the underlying score-reuse mechanism documented at 16:07 (exact score match to an older closed signal) is unaffected by this and remains worth investigating.
- **Outcome-tracker lifecycle-status sweep (crypto+stocks)**: re-ran the identical sweep — `expires_at < now() AND status IN (waiting_for_entry, triggered, tp1_hit, tp2_hit)` still returns **exactly 252 rows**, identical breakdown (36 crypto B-tier, 197 stocks C-tier, 16 stocks B-tier, 3 stocks A-tier) — no backfill or reconciliation since the 16:07 or 11:39 reviews.
- **New this cycle**: `refresh_obsidian_dashboard` step timing out at 300s appears in **43** recent `cycle_*_summary.md` files across the last several schedule days, including today's `cycle_01_16-07_summary.md` — a reproducible, non-transient pipeline failure (§14).
- Monitor/paper Windows Task state not queried this run (outside the explicit read-only CLI allowlist).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-30 18:47 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["Windows Task Scheduler live state", "fresher scalp/intraday/swing generation this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler restarted at 16:07 (cycle_01), fresh at 17:50", "scalp/intraday/swing reports all in 4-12h carry-forward band, no fresher generation this cycle", "252 stale-open-status rows unchanged since 11:39/16:07 reviews", "refresh_obsidian_dashboard step timed out at 300s in 43 recent cycle summaries, including today's"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["risk_on", "mixed", "wait_for_trigger"], "data_missing": ["fresh ETF flow print this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scalp/intraday/swing all read 'bullish trend (risk-on)' with BTC/ETH uptrend, breadth 55-82% above EMA20/50 (up from 52.5%/72.5-77.5% at 16:07)", "macro/geopolitics risk score pinned at 100.0/100 risk-off across scalp/intraday/swing (up from 83.9-85.9 at 16:07) — Iran/Hormuz, Kyiv-area strikes, helium-shortage headline", "external check: BTC $78,266.32 +0.81% 24h, ETH $2,460.36 (roughly flat) — BTC recovering vs the -3.13% seen at 16:07"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "catalyst_contradicted"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["1829 cumulative catalyst events today, 971/1829 (53.1%) unmapped — flat vs 52.2% at 16:07 and 53.9% at 11:39, effectively steady all day", "ATOM/USDT exploit_hack still top-importance (0.77), no new resolving info found this cycle (same Cosmos Labs 'wrongly cleared the bug' story from 2026-08-29)", "new correlation found: the same Cosmos EVM exploit directly halted the MANTRA chain on 2026-08-21, and the desk holds an active MANTRA/USDT swing long opened 2026-08-28 (after that halt)", "6 narrative baskets this cycle: perps_dex, delisting_thin_liquidity (AAVE), binance_ecosystem_teaser, rwa, ai, momentum_breakout (UNI catalyst-backed, AUCTION not)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["DEXE and MANTRA funding/OI not in today's top-8 derivatives tables"],
      "suggested_effect": "advisory_only",
      "facts_used": ["intraday report: ZKP/ZKC funding negative (-0.0034/-0.0032), 'shorts may be crowded' flagged explicitly on the scalp side for those symbols", "TUT short idea structurally rejected in prior cycles for extreme negative funding against short — unchanged, still crowded", "PROM funding -6e-06 (near-neutral), OI n/a via MEXC fallback — no squeeze signal either way"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["chase_risk", "price_moved_away", "clean_retest"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM live $7.01 (+29.5% 24h), cooled from $7.18 (+38.7%) at 16:07 — still ~6.7% from TP1 (7.510), not a fresh long-watch, but decelerating rather than breaking down", "DEXE live $2.28 (-2.0% 24h) — round-tripped down from the $2.35 recovery at 16:07, now ~4.3% below its 2.38346 invalidation again", "TUT live $0.03587 (+2.1% 24h), essentially flat vs $0.03550 at 16:07, still ~29% through its invalidation", "no A-tier setups in scalp or intraday this cycle ('No A-tier setups found. Do not force a trade.')"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.63,
      "reason_codes": ["waiting_for_entry", "needs_review", "entered_unresolved"], "data_missing": ["true stop/TP state for all 252 stale rows"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM/USDT swing signal status=triggered, still approaching TP1, not a fresh entry", "252 stale-open rows unchanged since 11:39/16:07 (36 crypto, 3 stocks A-tier, 16 stocks B-tier, 197 stocks C-tier)", "untracked-alert count de-escalated from 3 (16:07) to 1 (DEXE/USDT only) as ZKP/PROM's 12:11 UTC alerts picked up matching signals within the detector's window — DEXE remains the one genuinely unresolved case at ~25h"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.72,
      "reason_codes": ["manual_review", "correlation_cluster", "reduce_risk"], "data_missing": ["verified live MANTRA/OM price (external sources contradictory)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT re-breached: $2.28 (-2.0% 24h), ~4.3% below invalidation, worse than the $2.35 recovery seen 3h ago — a reversal, not an improvement", "TUT/USDT unchanged breach, ~29% through invalidation", "MANTRA/USDT open swing long (sig_7645e0e74b394b42, triggered) sits on a chain that was directly halted by the same Cosmos EVM exploit story now dominating today's top catalyst (ATOM) — external price verification for MANTRA/OM returned contradictory, unusable data this cycle, so the position's true P&L cannot be confirmed externally; internal invalidation level (0.00428457) is the only reliable reference right now", "book remains structurally 100% long across the active-signals table despite a maximal 100/100 macro risk-off overlay"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["playbook_failing", "low_sample", "old_tail_expired"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier week: n=323, triggered winrate 11%, PF 1.07, avgR +0.017", "by-mode: swing PF 1.57/avgR+0.12 (best), intraday PF 0.98/avgR-0.01 (roughly flat), scalp PF 0.11/avgR-0.10 (reproducibly losing, 1W/9L)", "weekend signals underperform (winrate 14%, n=44) per this run's own observations panel", "stocks C-tier: triggered winrate 7%, PF 0.40 — reproducibly losing, consistent with the desk's own C-tier-never-actionable policy"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "manual_review", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "ZK/USDT", "trigger": "existing tracked B-tier waiting_for_entry zone ~0.008972-0.009137 (intraday+swing); confirm a pullback fill inside that zone, do not chase the momentum-table print (score 84.6-91.8, RS +11-12% vs BTC)", "reason": "the desk's cleanest non-extended tracked crypto long; regime has turned technically risk-on which supports RS-leader longs, but PROM is already extended toward TP1 so ZK is the better-positioned idea" },
    "best_short_candidate":    { "symbol": "ONG/USDT", "trigger": "a confirmed 1h close-and-retest failure below the recent low with volume, and funding checked for crowding first (thin-liquidity name, squeeze risk flagged on this bucket in prior cycles) — do not chase the -8.75% to -11.63% RS print without that confirmation", "reason": "consistently bias-short across both today's intraday and swing cycles (RS vs BTC -9.9% to -11.6%), the cleanest repeat-appearing short-side idea on the desk today; TUT remains structurally rejected for extreme negative funding" },
    "best_catalyst_candidate": { "symbol": "ATOM/USDT", "trigger": "unchanged since 11:39/16:07 — a confirmed breakdown with volume on renewed negative reaction to the hack-disclosure overhang; still two-sided (bearish disclosure vs bullish deflationary-tokenomics narrative), so still not a clean short without that confirmation", "reason": "highest-importance fresh catalyst again this cycle (0.77), no existing desk position, no new resolving information — but now linked to a live desk position (MANTRA/USDT) via the same underlying Cosmos EVM story, raising the stakes on watching this one resolve" },
    "avoid_candidate":         { "symbol": "DEXE/USDT", "reason": "re-breached this cycle: live $2.28 (-2.0% 24h), ~4.3% below its own 2.38346 invalidation, a reversal from the $2.35 recovery seen three hours ago — the existing open long needs manual review, not a new position; do not add" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.65 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | risk_on, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.62 | chase_risk, price_moved_away, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.63 | waiting_for_entry, needs_review, entered_unresolved | advisory_only |
| risk_manager | manual_review | 0.72 | manual_review, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.68 | playbook_failing, low_sample, old_tail_expired | advisory_only |
| head_trader | caution | 0.60 | mixed, manual_review, wait_for_trigger | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_1607.md` (pre-US-open decision review, 16:07 EEST).

- **Worse (reversal)**: DEXE/USDT — live price round-tripped from $2.35 (+2.4% 24h, ~1.4% below invalidation, "recovering") back down to **$2.28 (-2.0% 24h)**, ~4.3% below its 2.38346 invalidation. The improvement flagged at 16:07 did not hold.
- **Slightly improved (noise-level)**: TUT/USDT — $0.03550 (-7.6% 24h) → $0.03587 (+2.1% 24h), still ~29% through invalidation, essentially unchanged.
- **Improved (cooling, not breaking)**: PROM/USDT — 24h change decelerated from +38.7% ($7.18) to +29.5% ($7.01); still an open position running toward TP1, not a long-watch, but no longer accelerating.
- **De-escalated**: the untracked-watchlist-alert count dropped from 3 (16:07: DEXE + ZKP + PROM) to **1** (DEXE only) — the ZKP/PROM same-day recurrences picked up a matching signal within the detector's ±6h window as later signals were generated; this reframes those two as likely timing-window artifacts rather than repeats of the DEXE-style true gap. DEXE itself remains genuinely unresolved and is now ~25h10m old (was ~22h22m).
- **Unchanged**: the 252-row outcome-tracker lifecycle-status gap (36 crypto B-tier, 3 stocks A-tier, 16 stocks B-tier, 197 stocks C-tier) — identical count and breakdown across three consecutive reviews spanning ~7 hours.
- **Unchanged**: ATOM/USDT two-sided catalyst thesis (importance 0.77) — no new resolving information.
- **New this cycle**: technical regime label upgraded from "chop"/"range" (16:07 and earlier) to **"bullish trend (risk-on)"** across scalp, intraday, and swing simultaneously, with breadth improving (55-82% vs 52.5-77.5%) even as the macro score rose to its ceiling (100.0/100, up from 83.9-85.9).
- **New this cycle**: a new cross-link identified — the Cosmos EVM exploit story behind today's top catalyst (ATOM, 0.77) is the same incident that halted the MANTRA chain on 2026-08-21; the desk holds an active MANTRA/USDT swing long opened 2026-08-28 (after that halt), and MANTRA/OM's external price could not be verified this cycle (contradictory sources).
- **New this cycle**: `refresh_obsidian_dashboard` pipeline step found timing out at 300s in 43 of the recent cycle summary files, including today's — a reproducible operational bug not previously flagged in this review series.
- **Unchanged**: catalyst mapping weak (53.1% unmapped cumulative today vs 52.2% at 16:07 — effectively flat, still above the 50% weak-mapping threshold).
- **Unchanged**: no A-tier or fresh B-tier crypto signals in scalp or intraday this cycle.
- **Unchanged**: stocks market closed (Sunday) — UNH/USDT DOJ Medicare-fraud legal-risk cluster carries forward unchanged into Monday's actual US open (no new headline found this cycle; not re-verified per source-discipline since nothing has moved).

## 5. Catalyst Coverage

- Total catalyst events today (cumulative, as of 16:35 EEST catalyst cycle): **1829**. Mapped (non-null symbol): **858**. Unmapped: **971** (**53.1%**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (all `other_news`, non-crypto/off-topic financial content): "AEVEX Corp. (AVEX) Class Action Lawsuit: Investors Face October 20, 2026, Deadline" (PR Newswire); "Here's How Much You Should Have Saved for Retirement by Age 67..." (Motley Fool); "Here's the Maximum Social Security Increase You Could Get From a 3.6% 2027 COLA" (Motley Fool) — these three are generic personal-finance/legal-notice content with no tradable symbol, consistent with prior cycles' mapping-gap composition.
- Narrative baskets this cycle: **6** — perps_dex_narrative (HYPE primary, wait_pullback), delisting_thin_liquidity (AAVE primary, avoid_low_liquidity — new basket this cycle), binance_ecosystem_teaser (BNB/ASTER, related_beta_rotation — new), rwa_narrative (ONDO/XLM), ai_narrative (NEAR/RENDER/TAO/FET), momentum_breakout (UNI catalyst-backed vs AUCTION not — new, explicit "do NOT chase" framing on AUCTION).
- Highest-importance catalysts: ATOM/USDT exploit_hack (0.77, unchanged) and BTC/USDT exploit_hack — Coldcard exploit, ~2,055 BTC estimated stolen per Galaxy, alongside ETFs adding ~$800M inflows in the same window (0.77, two-sided: theft overhang vs institutional inflow strength).
- Legal-risk cluster unchanged: UNH/USDT DOJ Medicare-fraud probe (same corroborated multi-source cluster, no new headline); TSLA/USDT — Musk SEC settlement, $1.5M fine (Union Leader), unchanged.
- New correlation (this cycle): the ATOM/USDT top catalyst and the desk's active **MANTRA/USDT** swing long share the same root story (Cosmos EVM exploit, six chains including MANTRA halted 2026-08-21) — see §7 deep dive.

## 6. Market Landscape

BTC and ETH both read **uptrend** across the scalp (13:18), intraday (13:27), and swing (14:38) cycles today — a change from the "range"/"chop" read at 16:07 and earlier. Altcoin breadth above EMA20 ranges 55.0% (scalp/intraday) to 71.8% (swing); above EMA50 ranges 80.0% (scalp/intraday) to 82.1% (swing) — a genuine broadening from the 16:07 review's 52.5%/72.5-77.5%. Macro/geopolitics risk score is at its **ceiling, 100.0/100**, up from 83.9-85.9 at 16:07, driven by continuing Iran/Hormuz coverage (including a helium-shortage angle tied to the Iran war) and Kyiv-area strike headlines — the risk-off overlay intensified even as the technical tape improved, a genuine two-layer divergence rather than a single consistent mood. External check: BTC $78,266.32 (+0.81% 24h), ETH $2,460.36 (roughly flat) — BTC recovering from the -3.13% seen at 16:07, ETH steady. Movers: UNI/USDT +19.5% (catalyst-backed per the momentum_breakout basket), AUCTION/USDT elevated but explicitly flagged "without confirmed catalyst — do not chase." SOLY/USDT shows a -70.5% 24h move with bias-short flagged in the intraday report and zero internal news coverage — consistent with a thin-liquidity/no-catalyst capitulation, not a tradable short idea (no desk position, no catalyst, avoid).

### Market Mood / Risk Routing
- Crypto mood:           technically risk-on (BTC/ETH uptrend, broadening breadth) layered under a maximal risk-off macro overlay (100/100) — genuinely mixed, treat as two separate signals rather than collapsing to one label.
- Stocks mood:           closed (Sunday) — planning/watchlist context only; UNH DOJ-probe legal-risk cluster carries unchanged into Monday's actual US open.
- Dominant narrative:    perps_dex (HYPE, wait_pullback), delisting_thin_liquidity (AAVE, avoid), momentum_breakout (UNI catalyst-backed vs AUCTION chase-risk) — three of six baskets are new this cycle vs 16:07.
- Preferred side now:    mixed — the technical broadening supports RS-leader longs (ZK/USDT), but the maximal macro risk-off overlay argues against adding size; the desk's own signal generator remains structurally 100% long across the active book (zero shorts in the last 323-signal weekly sample) — a persistent structural gap, not a fresh market call.
- Best long candidate:   ZK/USDT (existing tracked waiting_for_entry zone 0.008972-0.009137) — the cleanest non-extended tracked long; PROM/USDT is explicitly NOT a fresh long-watch, it is an open position cooling toward its own TP1 after a further extended move.
- Best short candidate:  ONG/USDT (long-watch requires a confirmed breakdown-with-volume retest, funding-checked first for thin-liquidity squeeze risk) — the most consistent bias-short print across today's cycles; TUT/USDT remains structurally rejected for extreme negative funding against a fresh short.
- Best catalyst-backed candidate: ATOM/USDT — two-sided catalyst, unchanged since 11:39/16:07, now newly linked to the desk's live MANTRA/USDT position via the shared Cosmos EVM exploit story.
- What to avoid:         DEXE/USDT (re-breached this cycle, worse than 3h ago) and TUT/USDT (unchanged deep breach) — no new entries on either; do not chase AUCTION/USDT (no confirmed catalyst) or SOLY/USDT (no catalyst, thin liquidity, -70.5% 24h).
- What would change the view: a BTC/ETH close outside the current uptrend range with volume, a fresh catalyst resolving the ATOM two-sided narrative, verified live MANTRA/OM pricing, or a human reconciling the outcome-tracker's 252-row stale-status gap.

## 7. Candidate Deep Dives

### DEXE/USDT — AVOID / manual review (existing long, re-breached this cycle)
- Active signal: `sig_5b59fe4d0138325c`, B-tier swing long, entry 2.4777-2.5547, invalidation 2.38346, status `triggered`, expires 2026-09-05.
- External cross-check (CoinGecko, live): **$2.28, -2.0% 24h**, 24h volume $31.88M — a reversal from $2.35 (+2.4% 24h) three hours ago, now ~4.3% below the 2.38346 invalidation again (worse than the ~1.4%-below reading at 16:07).
- `detect_untracked_legacy_alerts --since 2026-08-29` still returns this identical DEXE/USDT swing-long alert (score 65.0, sent 2026-08-29T14:36:42 UTC) with no backing `proposed_signal` — untracked, now **~25h10m unresolved**, confirmed via direct DB lookup to be a genuine gap (closest signal predates the alert by ~11h42m, well outside the ±6h match window), not a timing artifact.
- No funding/OI data sampled for DEXE in today's top-8 derivatives tables — squeeze risk on any short here remains genuinely unknown.
- Chase/entry check: the move that looked like a recovery at 16:07 did not hold; a fresh short here would still be counter-trend against the 7d uptrend (+25.1% at 16:07's check), so the actionable short-watch trigger (a confirmed retest failure with consolidation) has not yet formed either.
- Manual review of the existing open long is the priority — the tracker has not reconciled this position across eight consecutive reviews spanning both the original breach, the brief recovery, and now the re-breach.

### PROM/USDT — existing position cooling toward TP1 (not a fresh long-watch)
- Active signal: `sig_b108351df18809d4`, B-tier swing long, entry 6.5825-6.8355, invalidation 6.27326, TP1/2/3 7.510/8.073/8.635, status `triggered`, expires 2026-09-06.
- External cross-check (CoinGecko, live): **$7.01, +29.5% 24h** — down from $7.18 (+38.7% 24h) at 16:07; the move is decelerating rather than reversing. Price is ~6.7% away from TP1 (was ~4.6% at 16:07).
- Derivatives: funding near-neutral (-6e-06), OI n/a via MEXC fallback, no squeeze signal.
- Scalp report explicitly kill-switches all scalp-mode PROM ideas ("crypto_scalp_disabled") regardless of score; the swing B-tier idea is the same already-tracked signal, not a new one.
- Chase/entry check for any NEW position: at $7.01, still buying within ~7% of TP1 on an already-tracked position — not a long-watch opportunity.
- Would invalidate the existing long: a close back below 6.27326, or a broader BTC/ETH breakdown dragging RS leaders down with it.

### TUT/USDT — AVOID / manual review (existing long, essentially unchanged)
- Active signal: `sig_c7ce9835f38c40a8`, B-tier swing long, entry 0.05164-0.05250, invalidation 0.05058, TP1/2/3 0.0554/0.0573/0.0598, status `triggered`, expires 2026-09-03.
- External cross-check (CoinGecko, live): **$0.03587, +2.1% 24h** — a mild bounce from $0.03550 (-7.6% 24h) at 16:07, still ~29% through the 0.05058 invalidation, no material change.
- Both today's intraday and (implicitly, via bias-short list) swing reports continue to flag TUT/USDT bias-short; funding remains extreme-negative against a fresh short per prior cycles' explicit rejection — shorts stay crowded, squeeze risk unchanged.
- No fresh internal `news_items` catalyst found for TUT in the last 24h — pure price action, not news-driven.
- Not applicable to a fresh entry — the open long needs manual review, not a new trade decision.

### ATOM/USDT — catalyst-watch (unchanged, no existing position, two-sided catalyst, now linked to a live desk position on MANTRA)
- Top-importance catalyst again this cycle: exploit_hack, importance 0.77 — same underlying story (Cosmos Labs' own delayed/mishandled disclosure of the six-chain Cosmos EVM bug: MANTRA, TAC, KiiChain, Nesa affected, ~$5.7M drained between Aug 20-25).
- No new resolving information found this cycle for either side of the two-sided thesis (bearish disclosure-failure overhang vs. bullish deflationary-tokenomics narrative surfaced in earlier reviews).
- **New this cycle**: the same exploit story directly halted the MANTRA chain on 2026-08-21 (price crashed to a record low near $0.0041 before the halt, per CoinDesk). The desk's active MANTRA/USDT swing long (`sig_7645e0e74b394b42`, entry 0.00444-0.00457, invalidation 0.00428457, TP1 0.00500422, status `triggered`, created 2026-08-28 — after the halt) is therefore exposed to the same underlying narrative currently driving ATOM's top-importance catalyst score.
- No active desk position on ATOM itself — clean catalyst-watch, no contradiction risk there.
- Actionable trigger: unchanged — a confirmed breakdown with volume on continued negative reaction to the disclosure.

### MANTRA/USDT — existing position, external price UNVERIFIABLE this cycle (manual review recommended)
- Active signal: `sig_7645e0e74b394b42`, B-tier swing long, entry 0.00444289-0.00457243, invalidation 0.00428457, TP1 0.00500422, status `triggered`, created 2026-08-28 (a week after the chain's 2026-08-21 exploit-halt), expires 2026-09-04.
- External price check returned **contradictory, unusable results**: a CoinMarketCap page explicitly labeled "MANTRA (old)" showed $0.006071, while a separate Binance-sourced search snippet showed $3.89 (clearly a stale/mismatched historical figure, likely conflating a pre-2025-crash data point). Per source-discipline (§N), this is logged as "source unavailable / unverifiable" rather than guessed — the ingest script itself rejected the CoinMarketCap source as not citable.
- No fresh internal `news_items` catalyst found for MANTRA specifically in the last 72h.
- Given the position sits on a chain with an ongoing, still-unfolding security-disclosure story (Cosmos Labs' 2026-08-29 admission of mishandling the original bug) and unverifiable external pricing, this position is flagged for **manual review** — not a clean AVOID (no confirmed breach of the internal invalidation level), but not confirmable as healthy either.

### ZKP/USDT & PROM/USDT untracked-alert de-escalation (system-integrity, resolved this cycle — informational)
- `detect_untracked_legacy_alerts --since 2026-08-30` now returns **0** rows (was 2 at 16:07: ZKP/USDT and PROM/USDT, both sent 2026-08-30T12:11:4x UTC).
- Direct DB check: both symbols have since generated additional same-day signals/alerts (ZKP scalp alert 13:24 UTC, swing alert 14:37 UTC; PROM scalp alert 13:24 UTC, swing alert 14:37 UTC) that now fall within the detector's ±6h matching window of the original 12:11 UTC alerts — this reclassifies those two as likely **timing-window artifacts**, not confirmed instances of the score-reuse mechanism documented at 16:07. That mechanism (an alert's score exactly matching an older closed signal created hours earlier) remains worth investigating on its own merits, but the count of *currently unresolved* instances is 1 (DEXE), not 3.

## 8. Best Candidates Ranked

1. **ATOM/USDT** (catalyst-watch, two-sided, now linked to MANTRA exposure) — wait for a confirmed breakdown with volume; unchanged since 11:39/16:07.
2. **ZK/USDT** (long-watch) — existing tracked waiting_for_entry zone 0.008972-0.009137; the desk's cleanest non-extended tracked crypto long, supported by the improving technical regime.
3. **ONG/USDT** (short-watch) — consistent bias-short across today's cycles; needs a confirmed breakdown-with-volume retest and a funding check first (thin-liquidity squeeze risk).
4. **DEXE/USDT** (avoid / manual-review priority, worse this cycle) — re-breached to $2.28, ~4.3% below invalidation; resolve the existing open long manually, do not add.
5. **TUT/USDT** (avoid / manual review, unchanged) — do not add; existing long remains ~29% through its own invalidation.
6. **MANTRA/USDT** (manual review, unverifiable pricing) — existing long on a chain with an unresolved security-disclosure story; verify price through a reliable source before any action.
7. **PROM/USDT** (existing position, not a long-watch) — cooling toward TP1 (7.510); do not chase a fresh entry at $7.01.
8. **UNH/USDT** (stocks watch-only) — carry the unchanged DOJ-probe legal-risk cluster into Monday's actual US open; C-tier only, not actionable today.

No clean, unconditional "trade now" candidate exists this cycle — every entry above is trigger-gated, already-open, or pending manual review, per PART 9.

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and the scheduler continue regardless.

- **DEXE/USDT**: existing long re-breached this cycle (~4.3% below invalidation via live CoinGecko cross-check), worse than the recovery seen three hours ago; avoid adding, flag for manual review.
- **TUT/USDT**: existing long confirmed ~29% through invalidation, unchanged; avoid adding, flag for manual review.
- **AUCTION/USDT**: elevated momentum print but explicitly flagged by today's catalyst scan as "without confirmed catalyst" — do not chase.
- **SOLY/USDT**: -70.5% 24h move, zero internal news coverage, thin-liquidity profile consistent with the delisting_thin_liquidity narrative basket — no desk position, avoid treating as a short opportunity without a catalyst.
- **Crypto scalp mode (all symbols)**: kill-switched at the mode level today per today's scalp report — not a market call, a standing configuration.

## 10. Main Risks

- **DEXE/USDT reversed, not resolved**: the recovery flagged at 16:07 ($2.35, ~1.4% below invalidation) did not hold — live price is back to $2.28, ~4.3% below invalidation, essentially matching the original confirmed-breach level from earlier today. The open long remains unreconciled across eight consecutive reviews.
- **Outcome-tracker lifecycle bug remains fully unresolved**: 252 stale-open-status rows, identical count and breakdown across three consecutive reviews spanning ~7 hours — this continues to undermine confidence in every "triggered"/"tp1_hit"/"tp2_hit" label used throughout this review, including the stocks A/B headline stats.
- **New: MANTRA/USDT position sits on a chain with an unresolved security-disclosure story and unverifiable external pricing** — cannot currently confirm the true health of this position from outside sources; internal invalidation level is the only reliable check available.
- **New: `refresh_obsidian_dashboard` pipeline step is reproducibly timing out** (43 recent cycle summaries) — a genuine, non-transient operational bug, not previously surfaced in this review series (§14).
- **Book remains structurally 100% long** across the active-signals table (zero shorts in the last 323-signal weekly sample) even as the macro overlay sits at its maximum risk-off reading (100/100) — the desk cannot currently express a risk-off view even if conditions warranted one.
- **Catalyst mapping remains weak this run** (53.1% unmapped) — treat the catalyst layer as context, not a gating input.
- **UNH DOJ-probe cluster** carries unchanged into Monday's actual US-open slot — a real legal-risk item, not yet actionable today.

## 11. Action Plan — next 4 hours

- No new crypto entries recommended this window beyond the existing tracked book; treat PROM/USDT as a position-management item (cooling toward TP1), not a new-entry candidate.
- Continue watching ATOM/USDT for a technical setup to form around the unchanged two-sided catalyst; note its new linkage to the desk's MANTRA/USDT exposure.
- Human/manual: re-review DEXE/USDT now that its recovery has reversed — the manual-review priority should be elevated back to where it was before the brief 16:07 improvement.
- Human/manual: verify MANTRA/OM's true live price through a reliable source (external checks this cycle were contradictory/unusable) and confirm whether the existing swing long is still within its invalidation band.
- Human/manual: investigate the `refresh_obsidian_dashboard` 300s timeout — reproducible across 43 recent cycles, a genuine pipeline defect worth a dedicated fix session (§14).
- Stocks: no action, market closed; carry UNH forward with its legal-risk flag into Monday's actual US-open-reaction and late-session-risk slots.

## 12. Final Verdict per Mode

- **Crypto scalp**: avoid — mode kill-switched today, no new entries regardless of setup quality.
- **Crypto intraday**: wait-for-trigger — 0 fresh A/B this cycle; ZK/USDT is the cleanest tracked long-watch.
- **Crypto swing**: wait-for-trigger on ATOM/USDT and ONG/USDT (short-watch, needs confirmation); manual-review priority elevated on DEXE/USDT (re-breached) and newly flagged on MANTRA/USDT (unverifiable pricing); TUT/USDT unchanged manual-review; PROM/USDT remains position-management (cooling toward TP1), not a long-watch.
- **Stocks intraday/swing/invest**: closed/planning-only (Sunday); UNH carries an unchanged legal-risk flag into Monday's actual open.

## 13. Sources

- [DeXe (DEXE) live price](https://www.coingecko.com/en/coins/dexe) — CoinGecko, fetched 2026-08-30 ~15:4x UTC, $2.28, -2.0% 24h.
- [Tutorial (TUT) live price](https://www.coingecko.com/en/coins/tutorial) — CoinGecko, fetched 2026-08-30 ~15:4x UTC, $0.03587, +2.1% 24h.
- [PROM (Prometeus) live price](https://www.coingecko.com/en/coins/prom) — CoinGecko, fetched 2026-08-30 ~15:4x UTC, $7.01, +29.5% 24h.
- BTC/ETH aggregated price check (Yahoo Finance / CoinDesk / Coinbase search results) — 2026-08-30, BTC $78,266.32 +0.81% 24h, ETH $2,460.36.
- [Cosmos Labs says it wrongly cleared the bug behind a $5.7 million six-chain hack](https://www.theblock.co/news/defi/2026-08-29-cosmos-labs-says-it-wrongly-cleared-the-bug-behind-a-5-7-million-six-chain-hack-413061) — The Block, 2026-08-29.
- [Cosmos EVM Flaw Exploited After Cosmos Labs Knew Every Blockchain Running It Was Vulnerable](https://thehackernews.com/2026/08/cosmos-evm-flaw-exploited-after-cosmos.html) — The Hacker News, 2026-08-29.
- [MANTRA token plunges 18% to record low as blockchain halts after exploit](https://www.coindesk.com/tech/2026/08/21/mantra-token-plunges-18-to-record-low-as-blockchain-halts-after-exploit) — CoinDesk, 2026-08-21.
- MANTRA (old) / OM live price — **source unavailable / contradictory**: CoinMarketCap page ($0.006071) vs. a Binance-sourced search snippet ($3.89) disagree by ~640x; not cited as fact, flagged for manual verification instead.
- Internal: `data/catalysts/2026-08-30/catalyst_cycle_13-35.md`, `catalyst_events.jsonl` (1829 cumulative rows).
- Internal: `db/crypto_ai_desk.sqlite` `proposed_signals`/`watchlist_alerts`/`news_items` read-only lookups, run 2026-08-30 ~18:4x EEST.
- Internal: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-30_1607.md` (previous review, for continuity/diff).

## 14. Fix Requests / TODO

### TODO-obsidian-dashboard-refresh-timeout-2026-08-30 (NEW — reproducible pipeline failure)
- **issue:** The `refresh_obsidian_dashboard` scheduler step (`python -m scripts.refresh_obsidian_dashboard`) times out at exactly 300 seconds. Found in **43** recent `cycle_*_summary.md` files across the last several schedule days (2026-08-28 through 2026-08-30), including today's `cycle_01_16-07_summary.md`. This is a reproducible, non-transient failure, not a one-off.
- **evidence:** `grep -rl "timed out after 300" data/scheduled_runs/2026-08-2*/cycle_*.md data/scheduled_runs/2026-08-30*/cycle_*.md` → 43 matches; example: `data/scheduled_runs/2026-08-30_default_schedule/cycle_01_16-07_summary.md`, step "### 71. [FAIL] refresh obsidian dashboard (exit=-1, 306.3s, attempts=1)".
- **suggested manual fix:** (1) profile `scripts/refresh_obsidian_dashboard.py` to find the slow step (likely a full-vault rewrite or a large query without pagination); (2) either raise the scheduler's timeout for this specific step or make the script incremental/faster; (3) confirm whether the Obsidian dashboard is still stale as a result and whether that has any downstream effect on the (separate, working) "telegram dashboard refresh" step that follows it.
- **priority:** medium (does not block trading/scanning, but has been silently failing for days — a genuine data-freshness gap for whoever relies on the Obsidian dashboard specifically).
- **first observed (this review series):** 2026-08-30 18:47 EEST; historical occurrences trace back at least to 2026-08-28 per the grep above and likely further.

### TODO-watchlist-alert-reuse-mechanism-2026-08-30 (carried forward, scope narrowed)
- **issue:** The untracked-watchlist-alert bug's currently-*unresolved* count is back down to **1** (DEXE/USDT, ~25h10m old) from 3 at the 16:07 review — the ZKP/USDT and PROM/USDT recurrences flagged at 16:07 appear to have been timing-window artifacts (they picked up a matching signal within the detector's ±6h window as later same-day signals were generated), not confirmed repeats. However, the underlying **score-reuse mechanism** documented at 16:07 (ZKP's alert score exactly matching an older `stopped` signal; PROM's exactly matching an older `missed_no_entry` signal) is a real, concerning finding independent of whether those two specific alerts eventually got a nearby match — it suggests the alert-sending path may not always be selecting the correct/freshest signal, even when a matching row later happens to exist within the window.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-30` (0 rows now vs 2 at 16:07) and `--since 2026-08-29` (1 row, DEXE, now vs 3 at 16:07). DB cross-reference confirms DEXE's alert (2026-08-29T14:36:42 UTC) has no `proposed_signal` within ±6h (closest is ~11h42m before it).
- **suggested manual fix:** unchanged core recommendation from 16:07 — (1) trace the watchlist-alert-sending code path for how it selects/attaches a `signal_id`/score at send time; (2) add a guard against sending an alert whose matched signal is already closed; (3) specifically resolve the DEXE/USDT case (now the longest-lived confirmed instance, ~25h and counting) as the primary test case, since it is not a timing artifact; (4) treat the ZKP/PROM 16:07 findings as supporting evidence of the mechanism rather than as separately-unresolved cases.
- **priority:** high (DEXE case is now ~25h unresolved with a confirmed non-artifact gap).
- **first observed:** 2026-07-17 (per memory); DEXE case first observed as untracked 2026-08-29 ~14:37 UTC; scope re-assessed 2026-08-30 18:47 EEST.

### TODO-lifecycle-status-gap-unchanged-2026-08-30 (carried forward, unchanged — no backfill has occurred)
- **issue:** The lifecycle-status bug (252 rows with `expires_at < now()` while `status` still reads an open value: 36 crypto B-tier, 197 stocks C-tier, 16 stocks B-tier, 3 stocks A-tier) is **still exactly 252 rows with the identical tier breakdown** at this review, across three consecutive reviews spanning ~7 hours (11:39 → 16:07 → 18:47).
- **evidence:** Re-run of the same SQLite sweep against `db/crypto_ai_desk.sqlite` at ~18:4x EEST 2026-08-30: identical 252-row count and tier breakdown as both prior reviews.
- **suggested manual fix:** unchanged from prior reviews — (1) confirm whether the outcome-checker job covers stocks symbols at all; (2) add an automated sweep/alert for `expires_at < now() AND status NOT IN (closed_states)` across both asset classes; (3) backfill/reconcile all 252 rows' true final status; (4) re-run `signal-stats --asset-class stocks` after backfill; (5) this is now the 7th+ consecutive review carrying an unresolved instance of this bug family with zero movement in the count — recommend escalating past routine mention to an explicit scheduled maintenance session.
- **priority:** high (unchanged count across three consecutive reviews spanning ~7h, includes stocks A-tier).
- **first observed:** 2026-07-17 (crypto candle-gap form); broadened scope first fully quantified 2026-08-30 11:39 EEST; confirmed unchanged 2026-08-30 16:07 and 18:47 EEST.
