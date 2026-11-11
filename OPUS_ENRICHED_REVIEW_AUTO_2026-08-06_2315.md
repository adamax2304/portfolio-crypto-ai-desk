# Opus Enriched Review — post-close final daily review — Auto Cycle 23:15 EEST

## 1. Executive Summary

Slot: **post-close final daily review** (target 23:15 EEST; actual data-gathering window ~23:24-23:32 EEST, Δ+9-17min, within tolerance). **Advisory only — no auto-trade.** This is the daily wrap: how the US session closed, what worked/failed today, end-of-day risk/exposure, and the overnight-into-Asia crypto setup. **Quiet close: no A-tier and no new B-tier setups fired in any of the six report streams this cycle** (crypto scalp/intraday/swing all show "No A-tier setups found" / "No B-tier setups found"; stocks intraday shows "No A/B-tier actionable setups in this run") — a materially quieter cycle than the 21:46 review (which had 3 fresh crypto B-longs + XLK stocks B). **Today's one stocks A/B idea, XLK long (B-tier 74.16), closed the session `ENTERED UNRESOLVED`** — entry filled ~19:57-19:59 UTC, neither TP1 (188.62) nor invalidation (184.81) was hit before the window closed, status flipped `triggered → expired` at 20:23 UTC (23:23 EEST); this is **not a loss and not a missed entry**, it is a clean fill with no resolution before the daily window — "0R display / unresolved, no TP/SL before window." **MSFT remains hard-gated on standing legal risk** (class-action/securities-fraud, lead-plaintiff deadline Aug 11 2026, internal news confirmed fresh <24h) for a fourth+ consecutive review — never promotable regardless of its raw A-tier score (97.5 this cycle). **EPIC/USDT's OHLCV-gap-driven status desync is now unresolved for a third consecutive cycle** (18:48 → 21:46 → 23:15) — `proposed_signals.status` still `triggered`, `signal_outcomes` still logging `candles=0` on every ~20-second check with an internal `final_outcome=expired` that never propagates to the master status. **The BICO/USDT catalyst-vs-technical contradiction flagged at 21:46 has resolved itself** — the `momentum_breakout` basket's primary rotated to ACE/USDT this cycle, and ACE's own swing-scorer risk gate independently agrees with the catalyst layer's `avoid_chase` tag (ACE scored only 40/100, explicitly "more than 2 ATR from EMA20; do not chase") — catalyst and technical layers are aligned, not contradicting, for the first time in two cycles. **Untracked legacy crypto alerts worsened again: 13 today** (vs 9 at 21:46, 4 at 18:48, 0 at 11:44) — a fourth consecutive escalation within the same trading day, now 13 rows across HEI/BICO/SYN/KITE spanning scalp/intraday/swing. **BNB/USDT's `binance_ecosystem_teaser` catalyst basket has now persisted across 6 of 7 scan cycles today with zero defined technical entry the entire session** — flagged for a stronger TODO this cycle. Catalyst mapping stayed flat/weak: **66.2% unmapped** (vs 66.1% at 21:46). Crypto stays net-open into the Asia session: STO/USDT, PUMP/USDT and CTSI/USDT swing longs all remain `triggered`/open with no fresh invalidation. Macro/geopolitics risk remains pinned at **100/100** (Iran/Hormuz, Houthi) for a sixth+ consecutive review.

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-06_19-12_scalp_report.md` (~1h12m old at review start, regime bullish trend, **0 A-tier, 0 B-tier**), `data/reports/intraday/2026-08-06_19-21_intraday_report.md` (~1h03m old, regime range/chop, **0 A-tier, 0 B-tier** — ADA/USDT and HFT/USDT top the C-tier watchlist at 54.9/53.4), `data/reports/swing/2026-08-06_20-19_swing_report.md` (~5min old — freshest report of the day, regime range/chop; **0 A-tier, 0 B-tier**; 9 C-tier watchlist names: CTSI, ZBT, ADA, KITE, BICO, ERA, HFT, MMT, GIGGLE).
- Stocks: `data/reports/stocks/intraday/2026-08-06_20-01_stocks_intraday_report.md` (~23min old, regular session, 84/84 symbols ok, 10/10 indices, 12/12 sector ETFs, 0 fetch failures; regime **bullish**, VIX 15.32, breadth 100% above EMA20/50; **0 A/B-tier actionable** — all 9 raw A/B candidates demoted to C, incl. PLTR raw-A 98.33, MSFT raw-A 97.54 legal-gated, XOM raw-A 89.24 RR-gated, SPY raw-A 81.95 liquidity-gated). Stocks swing/invest: last generated 2026-07-02 — stale >1 month, excluded per standing deprecation policy.
- `data/catalysts/2026-08-06/catalyst_events.jsonl` (direct read, cumulative today: 1,350 mapped / 2,650 unmapped of 4,000 rows = **66.2% unmapped**), `narrative_baskets.jsonl` and freshest `catalyst_cycle_19-26.md` (22:26 EEST, ~58min old) — 3 active baskets: `binance_ecosystem_teaser` (BNB primary, playbook `related_beta_rotation`, present in 6/7 cycles today, all-day carry with zero entry), `perps_dex_narrative` (HYPE primary, playbook `wait_pullback`), `momentum_breakout` (ACE primary — **rotated from BICO at 21:46**, playbook `avoid_chase`, fresh<1h).
- CLI: `active-signals --asset-class crypto` (50 rows, all B-tier, 0 A-tier; STO/PUMP/CTSI-swing all `triggered`/open), `active-signals --asset-class stocks` (50 rows; mostly C-tier legacy from mid-July or earlier; COST/SMCI fresh C-tier `waiting_for_entry`), `signal-stats --asset-class crypto` (weekly: tier B n=138, PF 3.86, avgR 0.505, triggered winrate 24% — CLI flags winrate low despite strong PF; scalp sub-cohort still net-negative PF 0.00/avgR −0.14/totalR −4.0R/n=37), `signal-stats --asset-class stocks` (weekly headline A/B: n=5, triggered=1, 0 wins/0 losses, anecdotal; C-tier watchlist n=225, PF 0.25, totalR **−4.5R** — losing week, driven mostly by shorts: direction=short n=58, PF 0.125, totalR −3.5R), `detect_untracked_legacy_alerts --since 2026-08-06` (**13 untracked**, up from 9 at 21:46 — HEI/USDT scalp+intraday, BICO/USDT scalp×3+swing×2, SYN/USDT scalp+swing, KITE/USDT swing×3+scalp×2).
- DB (read-only queries, `db/crypto_ai_desk.sqlite`): `proposed_signals`/`signal_outcomes` for `sig_f6259f2dfc6f2f63` (EPIC/USDT — status still `triggered`, `signal_outcomes` last 5 checks span 20:26:33-20:27:50 UTC, all `candles=0`/`final_outcome=expired` in notes, matches the 21:46 pattern exactly); `proposed_signals`/`signal_outcomes` for `sig_4b30ce06596015a3` (XLK — status now `expired`, `entry_triggered=1`, `stop_hit=0`, `tp1_hit=0`, `tp2_hit=0`, `final_r=0.0`, confirming clean entered-unresolved close); status checks for STO/PUMP/CTSI-swing (all `triggered`, open); status check for XRP/USDT short (`tp1_hit`, still open, weekend-mode carried); re-run of the stale non-terminal backlog query (46 stocks-intraday / 16 crypto, non-terminal >7d past `expires_at`) — **identical to 21:46, unchanged**, confirmed standing backlog not actively growing; `news_items` freshness check for MSFT (fresh <24h PR Newswire "SueWallSt ... Lead Plaintiff Deadline of August 11, 2026 in Microsoft Corporation Lawsuit — MSFT" — internal record sufficient, no external research needed) and COIN (no fresh legal-specific item in the last 24h beyond routine whale-alert noise; the report's `legal_headline_risk: sec_doj` cap for COIN is treated as a standing gate flag, not independently re-verified fresh this cycle).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_2146.md` (late-session risk review, 21:46 EEST).
- **No external web research this cycle** — all candidates (EPIC, MSFT, ADA, XRP, BNB) had sufficient fresh internal news/catalyst/DB context; the missing-or-stale-internal trigger for external research (§G of the routine) was not met for any of them.

## 3. Scheduler / Data Freshness

- Two `scheduler.log` files exist concurrently: `data/scheduled_runs/2026-08-06_default_schedule/scheduler.log` (mtime 23:28 EEST, ~1-4min old — freshest) and `data/scheduled_runs/2026-08-05_default_schedule/scheduler.log` (mtime 22:00 EEST, ~1h30m old, the folder date-stamped from the original cycle start and continuously active past midnight in prior reviews). The 08-05 folder's latest `cycle_08_20-52_summary.md` has mtime 21:58 EEST (~1h32m old) — the most recent completed cycle summary found. Both freshness checks are well within the 3-hour defer threshold; **no defer triggered**. The coexistence of two concurrently-updating `scheduler.log` files (one continuing to write past 22:00 in the 08-05 folder, a second appearing under a new 08-06 folder from ~22:01 EEST) is noted as a low-priority data-hygiene observation, not a freshness failure — see §14.
- Crypto scalp ~1h12m old, intraday ~1h03m old, swing ~5min old (freshest report of the day) — all fresh, no carry-forward needed this cycle.
- Stocks: 20:01 EEST report (~23min old) — fresh, 84/84 symbols, 10/10 indices, 12/12 sector ETFs succeeded, 0 fetch failures.
- Monitor/paper heartbeat: `data/scheduled_runs/2026-08-05_default_schedule/fast_news_monitor_1785969315.log` mtime 23:30 EEST (~near-live), `derivatives_monitor_1786042909.log` (new 08-06-folder PID) mtime 22:01 EEST. `signal_outcomes` write cadence confirms the pending-signal tracker is live (~20-30 second check interval, last check 20:27:50 UTC = 23:27:50 EEST, essentially real-time relative to this review).
- Data-quality anomalies this cycle: (1) **EPIC/USDT stop-breach/OHLCV-gap desync, still unresolved, third consecutive cycle** (§7/§14); (2) **13 untracked legacy crypto alerts, up from 9** — fourth consecutive same-day escalation (§14); (3) catalyst mapping weak, 66.2% unmapped, flat vs 66.1% at 21:46; (4) 46 stocks-intraday + 16 crypto non-terminal-past-expiry signals — unchanged count vs 21:46, confirmed standing backlog; (5) **resolved this cycle**: the BICO/USDT catalyst-vs-technical contradiction flagged at 21:46 is no longer present — the `momentum_breakout` basket's primary rotated to ACE/USDT, and ACE's own gate independently agrees (avoid_chase); (6) two concurrently-updating `scheduler.log` files, noted above, low-priority.
- **TradingView / manual chart check unavailable** — no chart MCP loaded this cycle; all price-structure statements are from local OHLCV/ATR/EMA fields in the reports and DB.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-08-06 23:24 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["no fresh 1h OHLCV for EPIC/USDT (candles=0 on every recent tracker check, unchanged 3rd cycle)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Two scheduler.log files concurrently updating (08-06 folder mtime 23:28, freshest; 08-05 folder mtime 22:00, latest cycle summary mtime 21:58) -- both well within the 3h defer threshold", "crypto scalp/intraday/swing all fresh (~5min-1h12m old), stocks report ~23min old, 84/84 symbols ok", "13 untracked legacy crypto alerts this cycle (up from 9 at 21:46, 4th consecutive same-day escalation)", "EPIC/USDT signal_outcomes shows candles=0 on the last 5 consecutive checks (20:26:33-20:27:50 UTC), unchanged pattern from 21:46"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": ["no live intraday BTC/ETH tick beyond internal reports"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto: all three fresh reports (scalp, intraday, swing) agree BTC/ETH uptrend but overall regime label range/chop (neutral); altcoin breadth 53.2% above EMA20, 61.7-63.8% above EMA50 -- mixed breadth, not a clean risk-on tape", "Stocks: bullish, VIX 15.32, breadth 100% above EMA20/50, all 4 indices uptrend at the close -- but 0 of 9 raw A/B candidates cleared the actionability gates this cycle (worse than 21:46's 1-of-15)", "Sector rotation: energy/financials/materials strongest, semiconductors/utilities/technology weakest -- same laggard-tech pattern as 21:46"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["66.2% unmapped today (2650/4000 direct JSONL read), flat vs 66.1% at 21:46, still well above the 50% threshold, 6th+ consecutive review above threshold", "freshest scan (19:26 EEST, 22:26 mtime): 3 baskets -- binance_ecosystem_teaser (BNB, related_beta_rotation, present 6/7 cycles today, zero entry all day), perps_dex_narrative (HYPE, wait_pullback), momentum_breakout (ACE, avoid_chase, fresh<1h)", "BICO/USDT catalyst-vs-technical contradiction from 21:46 has resolved -- momentum_breakout primary rotated to ACE/USDT, whose own swing risk gate independently agrees (score 40, 'more than 2 ATR from EMA20; do not chase') -- catalyst and technical layers aligned this cycle, not contradicting"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["data_unavailable", "squeeze_risk", "oi_supports"],
      "data_missing": ["no fresh per-symbol funding/OI beyond what the intraday/swing reports embed"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HFT/USDT: extreme long crowding, funding +0.02 (swing) / -0.0013 (intraday, external venues), 24h OI +33.34% -- crowded-long signature, unchanged risk profile from 21:46", "ACE/USDT: negative funding across venues (bybit -0.0114, mexc -0.0091), crowding elevated/unknown, price up 68.9-76.3% over 24h -- an overextended long with crowded short-side funding, consistent with the avoid_chase tag", "CTSI/USDT (swing, filled/triggered): price up + OI up 75.17% at last read -- fresh positioning still supports the thesis, no deterioration signal", "EPIC/USDT: no fresher derivatives read available given the confirmed OHLCV gap -- last known (2026-08-01) was price-down/OI-down, deleveraging pattern"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ADA/USDT (crypto swing, B-tier 70.2, waiting_for_entry): entry zone 0.199451-0.201354, current price ~0.2023 (per today's freshest C-tier watchlist read) -- only ~0.4% above the zone top, effectively at-trigger, closest thing to a live actionable this cycle", "XRP/USDT (crypto swing short, B-tier 67.4, tp1_hit): entry 1.0598-1.0610, already in profit and carried through the weekend-mode window -- hold, no fresh entry context", "ACE/USDT: 24h +68.9% to +76.3% depending on report, more than 2 ATR from EMA20 per the swing scorer's own gate -- textbook chase risk, matches the catalyst avoid_chase tag", "XLK (stocks): entry filled 185.51-186.20, closed the session at final_r=0.0, neither TP1 (188.62) nor invalidation (184.81) reached before expiry -- clean entered-unresolved, not a chase or a loss"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.6,
      "reason_codes": ["entered_unresolved", "needs_review", "open_actionable", "waiting_for_entry"],
      "data_missing": ["CLI does not label lifecycle state directly -- classification is manual, from active-signals status + DB queries"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Stocks: XLK (B-tier 74.16) is the day's one A/B idea -- ENTERED UNRESOLVED at session close (entry_triggered=1, stop_hit=0, tp1/tp2=0, final_r=0.0, status triggered->expired at 20:23 UTC)", "Crypto OPEN actionable / holding: STO/USDT (78.1, triggered, steadiest carried), PUMP/USDT (66.3, triggered, carried), CTSI/USDT swing (67.1, triggered, filled cleanly at 21:46, still open toward TP1 0.0368/invalidation 0.0297), XRP/USDT short (67.4, tp1_hit, carried through weekend mode)", "Crypto NEEDS REVIEW: EPIC/USDT swing (69.5, still triggered, 3rd consecutive cycle stuck on OHLCV gap, see §7/§14)", "Crypto WAITING for entry: ADA/USDT swing (70.2, effectively at-trigger, see technical_entry above)", "13 untracked legacy crypto Telegram alerts today, invisible to PF/winrate tracking -- NEEDS REVIEW, worsened again from 9"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.65,
      "reason_codes": ["manual_review", "legal_risk", "reduce_risk", "repeated_losses"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["EPIC/USDT: still triggered, still stuck on a confirmed OHLCV gap, third consecutive cycle unresolved -- top standing risk item", "MSFT (stocks) still hard-gated LEGAL_RISK (class_action, securities_fraud, lead-plaintiff deadline Aug 11 2026 confirmed fresh internally) -- unchanged, fourth+ consecutive review", "13 untracked legacy scalp/swing/intraday alerts today (HEI, BICO, SYN, KITE) -- Telegram-pushed but untrackable for PF/winrate, worsened for a fourth consecutive same-day review (0->3->4->9->13)", "Stocks C-tier watchlist is a losing week: n=225, PF 0.25, totalR -4.5R -- shorts specifically net-negative (n=58, PF 0.125, totalR -3.5R), a repeated-losses pattern worth flagging even though C-tier is never actionable", "Crypto scalp mode remains net-negative all week (PF 0.00, avgR -0.14, totalR -4.0R, n=37) -- unchanged weak lane, contributes most of today's untracked-alert volume"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly (tier B, n=138, reliable): PF 3.86, avgR 0.505, triggered winrate 24% -- CLI flags winrate low despite healthy PF; scalp mode alone stays net-negative (PF 0.00, avgR -0.14, n=37)", "crypto swing 14d: WR 72%, PF 5.80, +24R -- still the desk's strongest bucket, underlying today's CTSI/STO/PUMP/ADA theses", "stocks headline A/B (weekly): n=5, anecdotal, 1 triggered, 0 wins/0 losses -- too small a sample to judge, XLK's entered-unresolved close is this week's only data point", "stocks C-tier watchlist (weekly): n=225, PF 0.25, totalR -4.5R, driven by a weak short cohort (n=58, PF 0.125, totalR -3.5R) -- a standing weak-lane pattern, watchlist-only so no live-money impact"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.55,
      "reason_codes": ["mixed", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["A genuinely quiet close: zero new A/B setups across all six report streams -- the desk's job into the Asia session is holding the existing book (STO, PUMP, CTSI, XRP-short), not adding exposure", "ADA/USDT swing is the closest thing to a live long trigger, sitting right at its entry zone top -- watch for a fill or a clean pullback, not a chase", "EPIC/USDT's data-gap desync is now a 3-cycle-old standing issue that needs a human session, not another review cycle re-confirming the same finding", "13 untracked alerts and the resolved-but-still-worth-noting BICO/ACE catalyst rotation are both operator-trace items for the next maintenance window", "MSFT stays the clearest 'avoid' -- highest raw score in stocks (97.5) but permanently legal-gated"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "ADA/USDT", "trigger": "crypto swing B-tier 70.2, waiting_for_entry, zone 0.199451-0.201354, current price ~0.2023 (~0.4% above zone top) -- fill on a pullback into the zone, or treat any fresh confirmed touch as the trigger; invalidation 0.197126" },
    "best_short_candidate":    { "symbol": "XRP/USDT", "trigger": "crypto swing B-tier 67.4, already tp1_hit and open -- hold into TP2/TP3 or invalidation 1.0626; no fresh short entries elsewhere this cycle (GOOGL stocks C-tier short remains gated, unchanged from 21:46)" },
    "best_catalyst_candidate": { "symbol": "BNB/USDT", "trigger": "binance_ecosystem_teaser basket, present in 6 of 7 scan cycles today, zero defined technical entry the entire session -- watch for a technical setup to finally attach to the narrative; if none appears by the next review, treat the basket as narrative-only for this news cycle" },
    "avoid_candidate":         { "symbol": "MSFT", "reason": "highest raw stocks score today (A-tier, 97.54) but permanently hard-gated on standing legal risk (class_action, securities_fraud, lead-plaintiff deadline Aug 11 2026, confirmed fresh internally) -- never promotable regardless of score" },
    "operator_action": "watch_only",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.6 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.55 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.5 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.5 | data_unavailable, squeeze_risk, oi_supports | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, clean_retest, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.6 | entered_unresolved, needs_review, open_actionable, waiting_for_entry | advisory_only |
| risk_manager | manual_review | 0.65 | manual_review, legal_risk, reduce_risk, repeated_losses | advisory_only |
| playbook_performance | caution | 0.55 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.55 | mixed, wait_for_trigger, manual_review | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_2146.md` (21:46 EEST, late-session risk review):

- **Resolved (no fresh signals fired anywhere):** all three crypto reports (scalp, intraday, swing) and stocks intraday show **zero A-tier and zero B-tier** this cycle — a much quieter close than 21:46 (which had 3 fresh crypto B-longs and XLK stocks B). HFT/USDT and BICO/USDT, both flagged as extended/chase-risk at 21:46, no longer carry fresh actionable status (BICO is now C-tier watchlist 55.5, matching its own risk read).
- **Closed (entered-unresolved): XLK (stocks, B-tier 74.16).** Was `triggered` and holding toward TP1/invalidation at 21:46 with ~1h15m of RTH left; the session closed with neither level reached — `proposed_signals.status` flipped `triggered → expired` at 20:23 UTC (23:23 EEST), `signal_outcomes` confirms `entry_triggered=1, stop_hit=0, tp1_hit=0, tp2_hit=0, final_r=0.0`. This is the day's only A/B idea and it closed flat/unresolved, not a win or a loss.
- **Resolved: BICO/USDT catalyst-vs-technical contradiction** (flagged new at 21:46) is gone this cycle. The `momentum_breakout` narrative basket's primary rotated from BICO/USDT to ACE/USDT, and ACE's own swing-scorer risk gate independently agrees with the catalyst layer's `avoid_chase` framing (ACE scored only 40/100, "more than 2 ATR from EMA20; do not chase") — catalyst and technical layers are aligned, not contradicting, for the first time in two cycles.
- **Worse: untracked legacy crypto alerts jumped from 9 to 13** — a fourth consecutive same-day escalation (0 at 11:44 → 3 at 16:11 → 4 at 18:48 → 9 at 21:46 → 13 now), still concentrated in HEI/BICO/SYN/KITE across scalp/intraday/swing.
- **Unchanged, third consecutive cycle: EPIC/USDT stop-breach/OHLCV-gap desync.** Still `triggered` in `proposed_signals`, `signal_outcomes` still logging `candles=0` on every ~20-second check with an internal `final_outcome=expired` note that never propagates to the master `status` field. No human intervention visible in the DB across three review cycles (18:48 → 21:46 → 23:15).
- **Unchanged, fourth+ consecutive review: MSFT** still hard-gated `LEGAL_RISK`, highest raw stocks score today (97.54, up from 80.61 at 21:46 due to a fresh Azure-earnings-beat rally, but the legal gate is unaffected by score).
- **New this cycle: BNB/USDT's catalyst basket has now been observed in 6 of 7 scan cycles today with zero technical entry the entire session** — a full-day narrative-without-execution pattern, worth its own TODO this cycle (see §14).
- **Unchanged:** catalyst mapping 66.1% → 66.2% unmapped — flat, still above the 50% threshold, now a sixth+ consecutive review at the ceiling. Macro/geopolitics risk still pinned at 100/100.
- **Unchanged (confirmed, not growing):** 46 stocks-intraday + 16 crypto signals non-terminal >7 days past `expires_at` — re-queried this cycle, identical counts to 21:46.
- **Unchanged, carried and open:** STO/USDT (78.1, swing, triggered), PUMP/USDT (66.3, swing, triggered), CTSI/USDT (swing, filled at 21:46, still triggered/open toward TP1 0.0368), XRP/USDT short (67.4, tp1_hit, carried through weekend mode).
- **New this cycle: two concurrently-updating `scheduler.log` files** (08-05 folder and a new 08-06 folder) — a low-priority data-hygiene observation, not seen flagged in prior reviews today (§14).

## 5. Catalyst Coverage

- Cumulative today (`catalyst_events.jsonl`, direct read): mapped **1,350**, unmapped **2,650**, total **4,000** rows → **66.2% unmapped**, flat vs 66.1% at 21:46 EEST.
- Freshest single scan (`catalyst_cycle_19-26.md`, 22:26 EEST mtime, ~58min old): 3 active narrative baskets — `binance_ecosystem_teaser` (BNB/USDT primary, ASTER related, playbook `related_beta_rotation`, present in 6/7 catalyst-cycle files scanned today, zero technical entry attached all day), `perps_dex_narrative` (HYPE/USDT primary, related DYDX/GMX/ASTER, playbook `wait_pullback`), `momentum_breakout` (ACE/USDT primary — rotated from BICO/USDT at 21:46, playbook `avoid_chase`, fresh<1h, and independently confirmed by ACE's own swing-scorer risk gate).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** 66.2% unmapped, above the 50% threshold for a sixth+ consecutive review running.
- Top unmapped headlines (sample, direct JSONL read, tail of today's file): "Bombardier Statement on Achieving Top Rankings in Industry Product Support Surveys" (GlobeNewswire Stocks, no symbol tag), "Houthi attacks kill at least 30 Yemeni government troops" (Finnhub market-news, no symbol tag), "DuPont Wins R&D 100 Award for Innovation in Healthcare" (PR Newswire Stocks, no symbol tag) — consistent with prior cycles' pattern of company-name-only wire items and geopolitical headlines without a clean primary-symbol tag in the crypto-facing pipeline.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed / range-bound at the close** — all three fresh reports (scalp, intraday, swing) agree BTC/ETH remain in uptrend, but the overall regime label across all three is range/chop (neutral); altcoin breadth is middling (53.2% above EMA20, 61.7-63.8% above EMA50) — not a clean risk-on tape, not a breakdown either. Macro/geopolitics risk still pinned at 100/100 (Iran/Hormuz, Houthi) for a sixth+ consecutive review — a standing background caution on alt-long aggression, not a directional call.
- Stocks mood: **risk-on / bullish at the close** — VIX 15.32, breadth 100% above EMA20/50, all 4 indices uptrend (SPY +3.65% 5d, QQQ +4.61% 5d). Sector rotation: energy/financials/materials strongest, semiconductors/utilities/technology weakest — same laggard-tech pattern as 21:46. Despite the bullish tape, **zero of nine raw A/B candidates cleared the actionability gates this cycle** (worse than 21:46's 1-of-15) — gates (legal risk, RR<1.5, liquidity/RVOL, trend-continuation requirement) did their job filtering a strong-looking but ungated tape.
- Dominant narrative: crypto — `binance_ecosystem_teaser` (BNB) is now a full-day narrative with zero technical attachment (6/7 cycles, no entry); `momentum_breakout` rotated from BICO to ACE, both flagged avoid_chase and both now consistent with their own technical gates. Stocks — semiconductor/technology relative weakness remains the standing sector-level caution even as the tape closed green.
- Preferred side now: **hold into the Asia session, do not add (crypto)** — STO/USDT, PUMP/USDT, CTSI/USDT longs and the XRP/USDT short all remain open/triggered with no fresh invalidation; ADA/USDT swing is the one live long trigger to watch, right at its entry zone. **No new stocks exposure (session closed)** — XLK closed entered-unresolved, MSFT stays legal-gated, everything else is C-tier/gated.
- Best long candidate: **ADA/USDT** (crypto swing, B-tier 70.2, waiting_for_entry) — zone 0.199451-0.201354, current price ~0.2023, effectively at-trigger; see §7/§8.
- Best short candidate: **XRP/USDT** (crypto swing, B-tier 67.4, already tp1_hit) — hold into TP2/TP3 or invalidation 1.0626; no fresh short entries elsewhere this cycle.
- Best catalyst-backed candidate: **BNB/USDT** (binance_ecosystem_teaser basket, present 6/7 cycles today) — watch-only, still no defined entry after a full session.
- What to avoid: **EPIC/USDT** in either direction until the OHLCV-gap/status desync is fixed by a human session (top priority, now 3 cycles unresolved); **MSFT** (standing legal-risk hard gate, highest raw score today at 97.5 — score is irrelevant while the gate holds); **chasing ACE/USDT** (>2 ATR from EMA20, catalyst-confirmed avoid_chase); all remaining stocks C-tier names post-close.
- What would change the view: a human-driven fix to the EPIC/USDT OHLCV feed; ADA/USDT filling cleanly inside its zone (or pulling back further before filling); a fresh technical setup finally attaching to the BNB/USDT narrative; the Asia-session crypto open bringing fresh volume/breadth confirmation to resolve the range/chop label.

## 7. Candidate Deep Dives

### EPIC/USDT (crypto swing, active triggered long, 69.5 — top finding, THIRD consecutive cycle unresolved)
- Position unchanged since 2026-08-01T17:57:00Z: entry zone 0.88456964-0.90522143, invalidation 0.85932857, `proposed_signals.status = triggered` as of this review's DB read (~23:27 EEST).
- **Unchanged from 21:46:** direct read of `signal_outcomes` for `sig_f6259f2dfc6f2f63` shows the tracker re-evaluating this signal roughly every 20 seconds (5 consecutive checks spanning 20:26:33-20:27:50 UTC sampled), every single check logging `src=binance/1h, candles=0`, alongside `stop_hit=0`, `final_r=0.0`, and a `final_outcome=expired` note buried in the per-check `notes` field that is **still never propagated to the master `proposed_signals.status` column**.
- Has price already reacted to a catalyst? No — internal `news_items` returned zero rows for EPIC/USDT at the original 18:48 review; not re-verified this cycle given the confirmed data-gap finding supersedes it (same reasoning as 21:46).
- Is the setup chasing? N/A — existing position; the open question remains a **data-pipeline** question, not a technical one.
- Aligned with market mood? Unknown/stale — cannot be assessed without fresh price data, third cycle running.
- Long/short/wait: **hold-and-escalate, not add** — this has now spanned three consecutive review cycles (18:48 → 21:46 → 23:15) with the identical `candles=0` symptom and no visible human fix in the DB. Escalating priority in §14 given the persistence.
- Derivatives/catalyst: no fresher data available this cycle given the confirmed OHLCV gap.

### MSFT (stocks, raw A-tier 97.54, permanently legal-gated — highest score, still an avoid)
- Raw score climbed from 80.61 at 21:46 to 97.54 this cycle (Azure-earnings-beat momentum, "Citi Raises MSFT Target to $600," "MSFT Stock Gains After Microsoft Opens Its Biggest India Data Center Yet") — but the gate that demotes it (A→C) is unrelated to score: `legal_headline_risk: class_action,securities_fraud`.
- Internal `news_items` check (fresh <24h): "SueWallSt Reminds Shareholders of a Lead Plaintiff Deadline of August 11, 2026 in Microsoft Corporation Lawsuit - MSFT" (PR Newswire Stocks, published 2026-08-06T14:09:00Z) — confirms the legal risk is current, not a stale/expired flag; internal record sufficient per §G, no external research triggered.
- Has price already reacted? Yes — the stock is rallying on fundamentals (cloud/AI momentum) independent of the litigation, which is a lead-plaintiff-deadline notice (a routine securities-litigation marketing item, common for large-cap names with any prior stock-drop history) rather than a fresh adverse development.
- Long/short/wait: **avoid** — per §I, any stocks A/B candidate with verified legal/headline risk becomes AVOID or MANUAL REVIEW REQUIRED, never a clean actionable, regardless of score. Score strength this cycle does not change that.
- This is the fourth+ consecutive review MSFT has appeared hard-gated; the pattern is stable, not escalating — no new TODO needed beyond noting it persists.

### ADA/USDT (crypto swing, B-tier 70.2, waiting_for_entry — closest live trigger this cycle)
- Entry zone 0.199451-0.201354, invalidation 0.197126, expires 2026-08-13T20:23:26 (plenty of runway). Current price per today's freshest watchlist read (~0.2023, swing report 23:19 EEST) sits **~0.4% above the zone top** — effectively at-trigger, well within 1 ATR (ATR ~0.0040-0.0042 across reports).
- Has price already reacted to a catalyst? No — no fresh verified catalyst for ADA/USDT in any of today's three reports; this is a pure RS/momentum thesis (24h +6-8%, RS vs BTC +6.6-8.3%) inside the desk's strongest playbook (`crypto_swing_narrative_rs_momentum`, 14d WR 72%/PF 5.80/+24R).
- Is the setup chasing? No — price is essentially at the defined zone, not extended above it; this would be a clean fill, not a chase, if it triggers on the next candle.
- Retest/pullback structure? The zone itself functions as the pullback level relative to ADA's 7d return (+18-18.4%).
- Aligned with market mood? Reasonably — ADA is trending up alongside BTC/ETH even though the overall regime label is range/chop; RS-leader-in-chop is the playbook's own preferred setup type.
- Long/short/wait: **watch for the fill** — no action needed beyond monitoring; this is the single closest-to-actionable long in the entire crypto book this cycle.
- What would invalidate: a 1h close beyond 0.197126, or a broader BTC breakdown against the range/chop-but-uptrend thesis.

### XRP/USDT (crypto swing short, B-tier 67.4, tp1_hit — best short-watch, carried and in profit)
- Entry 1.0598-1.0610, invalidation 1.0626, weekend-mode carried, `tp1_hit` confirmed via DB status check this cycle (unchanged from 21:46's active-signals read).
- No fresh technical or catalyst context surfaced for XRP/USDT in today's three crypto reports (it does not appear in the Strongest/Weakest Symbols lists) — this is purely a hold-into-target assessment from the DB, not a re-analyzed thesis.
- Long/short/wait: **hold into TP2/TP3 or invalidation** — already in profit, no new short entries elsewhere in the crypto book this cycle to compare against.
- This remains the desk's only open short exposure; GOOGL (stocks C-tier short, gated, unchanged from 21:46) is the next-best short-watch if a liquidity/market-context gate ever clears.

### BNB/USDT (crypto, catalyst basket only, no technical entry — full-day narrative-without-execution pattern)
- `binance_ecosystem_teaser` basket (primary BNB/USDT, related ASTER/USDT, playbook `related_beta_rotation`) appeared in 6 of the 7 catalyst-cycle scan files reviewed today (01-48, 05-00, 11-01, 14-20, 18-17, 19-26 — absent only from 01-40 and 07-52). Across the entire session, **no crypto scalp/intraday/swing report has ever attached a technical entry to BNB/USDT** — it remains narrative-only.
- Has price already reacted to the catalyst? Unknown — BNB/USDT does not appear in any Strongest/Weakest Symbols list today, meaning it is not currently among the desk's top movers despite the persistent basket tag.
- Long/short/wait: **watch only, still no trigger** — the pattern (all-day narrative persistence with zero technical confirmation) is itself worth flagging for a human look at whether the basket→scorer linkage is working as intended (see §14), separate from any single-cycle trade decision.

*(Excess candidates not given a full deep dive, per the 5-candidate cap: STO/USDT swing (78.1, triggered, carried, steadiest — unchanged, hold), PUMP/USDT swing (66.3, triggered, carried — unchanged, hold), CTSI/USDT swing (67.1, triggered since 21:46, holding toward TP1 0.0368/invalidation 0.0297 — unchanged, hold), XLK stocks (B-tier 74.16, closed entered-unresolved this cycle — see §4/§8 for the close framing), COST/SMCI stocks C-tier fresh `waiting_for_entry` (73.8/58.1, not actionable, watchlist only), 13 untracked legacy crypto alerts (HEI, BICO×5, SYN×2, KITE×5 — see §14 for the aggregate finding), ACE/USDT (catalyst avoid_chase, technical gate agrees — no contradiction, no deep dive needed this cycle).)*

## 8. Best Candidates Ranked

1. **EPIC/USDT (crypto swing long, triggered, B-tier, 69.5) — DATA-INFRASTRUCTURE ESCALATION, not a ranked trade idea** — flagged ahead of the ranked list; now 3 consecutive cycles unresolved, needs a human fix to the OHLCV feed for this symbol, not another review cycle.
2. **ADA/USDT (crypto swing long, waiting_for_entry, B-tier, 70.2)** — closest live trigger, essentially at the entry zone; watch for a clean fill, not a chase.
3. **CTSI/USDT (crypto swing long, triggered since 21:46, B-tier, 67.1)** — holding toward TP1 0.0368 / invalidation 0.0297; no action needed.
4. **STO/USDT (crypto swing long, triggered, B-tier, 78.1)** — steadiest carried position, unchanged; hold.
5. **XRP/USDT (crypto swing short, tp1_hit, B-tier, 67.4)** — best short in the book, already in profit; hold into TP2/TP3 or invalidation.

XLK (stocks, B-tier 74.16) closed the session `entered-unresolved` this cycle (final_r=0.0) — not re-ranked as an open idea; see §4/§7 for the close framing. No new stocks A/B exists to rank tonight.

## 9. Avoid / No Trade

*(This applies to this decision window only — scanning, tracking, and the scheduler continue unchanged.)*

- **EPIC/USDT, either direction** — active long stuck on a confirmed OHLCV data gap for a third consecutive cycle, status not resolving; treat as neither safely open nor safely closed until a human fixes the feed.
- **MSFT (stocks)** — standing hard gate, `LEGAL_RISK` (class_action, securities_fraud), never promotable regardless of score (97.5 raw this cycle, the highest in stocks).
- **Chasing ACE/USDT** — >2 ATR from EMA20 per its own swing gate, catalyst-confirmed `avoid_chase`; both layers agree, this is a clean avoid.
- **New crypto scalp-mode exposure generally** — 0 new ideas this cycle (matching the standing net-negative weekly PF 0.00), and continues to be the largest source of untracked legacy alerts (see §14).
- **All remaining stocks C-tier watchlist names** (PLTR, XOM, SPY, NVDA, NFLX, XLK-legacy-rows, QQQ, AVGO, META, LLY, XLV, SMH, COIN, SMCI, plus rejected JPM/XLE/AMZN/UNH/GOOGL/MSTR/DIA/XLY/AAPL/AMD/XLF/IWM) — gated by the SI-1..5 actionability layer, RR-below-min, or simply no_directional_setup; planning-only, market is closed until tomorrow's session.
- **New stocks exposure generally** — regular session has closed; nothing to add until pre-market/next-session context refreshes.

## 10. Main Risks

- **EPIC/USDT's stop-breach-with-open-status is now unresolved for a third consecutive review cycle** (18:48 → 21:46 → 23:15) with no visible human intervention in the DB — if the underlying price genuinely moved beyond invalidation during this window, real (paper) risk has been accruing purely because the monitor cannot see fresh candles for this symbol (§14, priority raised this cycle).
- **13 untracked legacy crypto alerts today, a fourth consecutive same-day escalation** (0→3→4→9→13) — a Telegram-pushed, PF/winrate-invisible alert path now spanning HEI/BICO/SYN/KITE across scalp/intraday/swing; the recurring pattern (TODO-3, first raised 2026-07-17) shows no sign of stabilizing (§14).
- **Stocks C-tier watchlist is a losing week** (n=225, PF 0.25, totalR −4.5R), driven mostly by a weak short cohort (n=58, PF 0.125, totalR −3.5R) — watchlist-only, no live-money impact, but worth tracking if the pattern persists into next week's C-tier promotion decisions.
- Macro/geopolitics risk remains pinned at the **100/100 ceiling** for a sixth+ consecutive review — a standing background caution on crypto long sizing.
- Catalyst mapping remains weak (66.2% unmapped) — treat all catalyst-basket framing as directional color only.
- **BNB/USDT's basket has now persisted a full session (6/7 cycles) with zero technical entry** — either a genuinely narrative-only setup (no problem) or a linkage gap between the catalyst layer and the scorers (worth a look, see §14).
- 46+16 stale non-terminal signals — confirmed unchanged vs 21:46, a standing (not worsening) data-hygiene backlog that continues to pollute `active-signals` counts.
- Two concurrently-updating `scheduler.log` files observed this cycle (§3) — low-priority, but worth a human glance to confirm there is only one live scheduler process, not a duplicate.

## 11. Action Plan — next 4 hours (overnight-into-Asia)

- **Escalate EPIC/USDT to a human session as a data-infrastructure issue, priority raised** — three consecutive review cycles with the identical `candles=0` symptom on binance/1h and no visible fix; this needs a feed/exchange-listing check (possible delisting, symbol-mapping break, or thin-liquidity data gap) plus the separate status-propagation fix (`final_outcome=expired` in `signal_outcomes.notes` never updates `proposed_signals.status`).
- Watch ADA/USDT for a clean fill inside 0.199451-0.201354 as the Asia session opens — this is the closest live long trigger in the book; do not chase above the zone.
- Let STO/USDT, PUMP/USDT, and CTSI/USDT run into their invalidations/targets unchanged — no new sizing on any of them.
- Hold XRP/USDT short into TP2/TP3 (1.0626 invalidation) — already in profit, no action needed.
- Continue treating ACE/USDT as an avoid-chase name; watch only for a genuine pullback/retest before reconsidering.
- Watch BNB/USDT for a confirmed technical setup to finally attach to the binance_ecosystem_teaser basket after a full day of narrative-only status — flag for the next scheduled review (04:30 crypto overnight/Asia slot) if it remains basket-only.
- Flag the 13 untracked legacy alerts (now spanning HEI/BICO×5/SYN×2/KITE×5) and the two concurrently-updating scheduler.log files for a human trace at the next available maintenance window — neither is evidence of a strategy-level problem, both are integrity/consistency items (§14).
- Continue scanning/tracking/monitors unchanged through the overnight and into the 04:30 EEST crypto overnight/Asia review — this review recommends one data-infrastructure escalation (raised priority) and several hold/watch items only, never a pause of any kind.

## 12. Final Verdict per Mode

- **Crypto scalp:** 0 new ideas this cycle (0 A-tier, 0 B-tier), consistent with its standing net-negative weekly PF; largest contributor to today's untracked legacy alerts (HEI, BICO, SYN, KITE all trace partly to the scalp path).
- **Crypto intraday:** 0 new ideas this cycle — a fully quiet cycle after 21:46's 3 fresh B-longs; ADA/USDT (54.9) and HFT/USDT (53.4) top the C-tier watchlist, neither actionable.
- **Crypto swing:** the desk's steadiest bucket; this cycle's top risk item (EPIC/USDT) persists unresolved for a third cycle, but the book otherwise held cleanly — STO/PUMP/CTSI all open/triggered, ADA at-trigger and the closest live setup, XRP short in profit.
- **Stocks intraday:** session closed for the day. Today's one A/B idea (XLK) closed entered-unresolved (final_r=0.0, neither TP nor stop hit). 0 of 9 raw A/B candidates cleared the actionability gates this cycle; MSFT remains the standing legal-gated highest-score name.
- **Stocks swing/invest:** not evaluated — reports stale/deprecated since 2026-07-02, excluded per standing policy.

## 13. Sources

- Internal only this cycle (no external web research triggered — see §2): `data/reports/scalp/2026-08-06_19-12_scalp_report.md`, `data/reports/intraday/2026-08-06_19-21_intraday_report.md`, `data/reports/swing/2026-08-06_20-19_swing_report.md`, `data/reports/stocks/intraday/2026-08-06_20-01_stocks_intraday_report.md`, `data/catalysts/2026-08-06/catalyst_events.jsonl`, `data/catalysts/2026-08-06/narrative_baskets.jsonl`, `data/catalysts/2026-08-06/catalyst_cycle_19-26.md` (and cross-referenced `catalyst_cycle_01-40.md` through `catalyst_cycle_18-17.md` for the BNB basket persistence check), `db/crypto_ai_desk.sqlite` (`proposed_signals`, `signal_outcomes`, `news_items` read-only queries), `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_2146.md`, `data/scheduled_runs/2026-08-05_default_schedule/` and `data/scheduled_runs/2026-08-06_default_schedule/` logs.

## 14. Fix Requests / TODO

### TODO-epic-usdt-ohlcv-gap-confirmed (priority: high, escalated further — THIRD consecutive cycle unresolved)
- **issue:** EPIC/USDT's active triggered long swing position (`sig_f6259f2dfc6f2f63`, score 69.5, entered 2026-08-01T17:57:00Z, invalidation 0.85932857) remains `triggered` in `proposed_signals` for a third consecutive review cycle (18:48 → 21:46 → 23:15 EEST, all identical). Direct read of `signal_outcomes` for this signal_id shows the tracker re-evaluating the position roughly every 20 seconds, with every recent check (this cycle: 20:26:33-20:27:50 UTC) logging `src=binance/1h, candles=0` and an internal `final_outcome=expired` note in the `notes` field that is never propagated to the master `proposed_signals.status` column.
- **evidence:** `db/crypto_ai_desk.sqlite` query `SELECT checked_at, status, stop_hit, final_r, final_outcome, notes FROM signal_outcomes WHERE signal_id='sig_f6259f2dfc6f2f63' ORDER BY checked_at DESC LIMIT 5` → 5 rows spanning 2026-08-06T20:26:33Z-20:27:50Z, all `status=triggered`, `stop_hit=0`, `final_r=0.0`, `notes` containing `candles=0` and `final_outcome=expired` — pattern identical to the 21:46 read two hours earlier.
- **suggested manual fix:** unchanged from 21:46 — (a) check whether EPIC/USDT is still actively listed/tradeable on binance spot, (b) trace why the OHLCV fetch path returns 0 candles for this specific symbol, (c) fix the status-propagation gap so a `final_outcome=expired` recorded in `signal_outcomes.notes` actually updates `proposed_signals.status`. Given this is now a third consecutive cycle with zero visible progress, this should be treated as the top-priority item for the next available human session, not deferred further.
- **priority:** high (raised urgency this cycle given 3-cycle persistence with no change)
- **first observed:** 2026-08-06 18:48 EEST; unresolved and re-confirmed identical at 21:46 and 23:15 EEST.

### TODO-untracked-alerts-recurrence (priority: high, recurring pattern, worsening for a fourth consecutive same-day review — 9→13)
- **issue:** 13 untracked legacy crypto alerts today (9 at 21:46, 4 at 18:48, 3 at 16:11, 0 at 11:44) — HEI/USDT (scalp+intraday), BICO/USDT (scalp×3, swing×2), SYN/USDT (scalp+swing), KITE/USDT (swing×3, scalp×2) — all sent to Telegram via `watchlist_alerts` with no matching `proposed_signal`. The count has more than tripled since the last review within the same trading day (9→13 in ~1h30m alone).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-06` output (13 rows, all `trackable: NO (no proposed_signal)`), spanning `sent_at` 10:44:35 UTC through 20:23:30 UTC.
- **suggested manual fix:** matches the existing project-level TODO-3 (first raised 2026-07-17, per project memory) — a human-driven session should trace why the `watchlist_alerts` Telegram-delivery path fires independently of `proposed_signals` registration for scalp/swing-mode alerts specifically. Given the count has grown every single review today (0→3→4→9→13), this now looks like an active, ongoing leak rather than a static backlog — worth prioritizing over the stale-signals backlog below.
- **priority:** high
- **first observed:** 2026-07-17 (project history); this cycle confirms continued, accelerating, same-day-repeated recurrence, 2026-08-06 23:15 EEST.

### TODO-bnb-basket-full-day-no-entry (priority: low, new this cycle, pattern observation)
- **issue:** The `binance_ecosystem_teaser` catalyst basket (primary BNB/USDT) appeared in 6 of the 7 catalyst-cycle scan files generated today (absent only from the 01-40 and 07-52 cycles), spanning the entire trading day, with zero crypto scalp/intraday/swing report ever attaching a technical entry to BNB/USDT. BNB/USDT also never appears in any Strongest/Weakest Symbols list today.
- **evidence:** `grep -A1 "binance_ecosystem_teaser" data/catalysts/2026-08-06/catalyst_cycle_*.md` → present in `01-48, 05-00, 11-01, 14-20, 18-17, 19-26` (6/7), absent in `01-40, 07-52`; no BNB/USDT entry found in any of today's scalp/intraday/swing "Top Trade Ideas" or "C-tier/Watchlist" sections.
- **suggested manual fix:** a human-driven session should check whether this is expected behavior (a genuinely narrative-only, no-technical-setup day for BNB) or a linkage gap where the catalyst-basket layer never feeds a corresponding technical scan trigger for its own primary symbol — low urgency since no live-money or paper-money impact occurred, but worth a look if the pattern repeats across multiple days for the same basket.
- **priority:** low
- **first observed:** 2026-08-06 23:15 EEST (pattern only visible in aggregate across the full day's catalyst-cycle files).

### TODO-duplicate-scheduler-log (priority: low, new this cycle, observation only)
- **issue:** Two `scheduler.log` files were observed updating concurrently this cycle: `data/scheduled_runs/2026-08-05_default_schedule/scheduler.log` (mtime 22:00 EEST, the folder continuously active since 2026-08-05 per prior reviews) and `data/scheduled_runs/2026-08-06_default_schedule/scheduler.log` (mtime 23:28 EEST, a new folder that began appearing ~22:01 EEST per its `derivatives_monitor_1786042909.log`). Neither is stale (both well within the 3h defer threshold), so this did not affect this review, but two concurrently-written scheduler logs could indicate a duplicate scheduler process rather than the expected single continuously-running one.
- **evidence:** `ls -la data/scheduled_runs/2026-08-05_default_schedule/scheduler.log data/scheduled_runs/2026-08-06_default_schedule/scheduler.log` → mtimes 22:00 EEST and 23:28 EEST respectively; `data/scheduled_runs/2026-08-06_default_schedule/derivatives_monitor_1786042909.log` first appears ~22:01 EEST.
- **suggested manual fix:** a human-driven session should confirm whether exactly one scheduler process is running (e.g. via Task Manager / `Get-Process`) and, if two are found, stop the duplicate to avoid double-counting cycles or double-sending Telegram alerts (which could also help explain part of the untracked-alerts pattern above, though that is speculative and unverified this cycle).
- **priority:** low
- **first observed:** 2026-08-06 23:15 EEST (this cycle).

### TODO-stale-nonterminal-signals-backlog (priority: medium, unchanged — re-confirmed this cycle, not actively growing)
- **issue:** 46 stocks-intraday and 16 crypto `proposed_signals` rows remain non-terminal (`triggered`, `tp1_hit`, `tp2_hit`, or `waiting_for_entry`) more than 7 days past `expires_at`. Re-queried this cycle with identical counts to the 21:46 review — confirms this is a standing backlog, not an actively growing leak, but still unresolved.
- **evidence:** `SELECT COUNT(*) FROM proposed_signals WHERE asset_class='stocks' AND mode='intraday' AND status IN ('triggered','tp1_hit','tp2_hit','waiting_for_entry') AND expires_at < datetime('now','-7 days')` → 46; same query for crypto (all modes) → 16, both re-run 2026-08-06 ~23:28 EEST, unchanged from 21:46 EEST.
- **suggested manual fix:** unchanged — a human-driven session should review the position-close/expiry job so that signals never reaching a terminal outcome within a reasonable window past `expires_at` are force-closed or flagged separately from genuinely live positions.
- **priority:** medium
- **first observed:** 2026-08-06 18:48 EEST; re-confirmed unchanged at 21:46 and 23:15 EEST.
