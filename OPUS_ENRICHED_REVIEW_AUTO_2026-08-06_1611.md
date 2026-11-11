# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (target 08:55 America/New_York; this run's actual data-gathering window ~08:59-09:11 ET, i.e. ~16:00-16:11 EEST — Δ+4-16min, within tolerance, not a DST-mismatch window per the schedule check below). **Advisory only — no auto-trade.** US cash market has not yet opened (opens 09:30 ET / ~16:30 EEST, ~19min after this review). Crypto tape remains constructive: BTC ~$64,580-64,876 (externally verified via WebSearch, up ~0.8-1.3% 24h), regime "bullish trend (risk-on)" across all three fresh crypto reports, altcoin breadth 61.36% above EMA20. Macro/geopolitics risk is **still pinned at the 100/100 ceiling** (Iran/Strait-of-Hormuz tension) — the same mood/risk-score divergence flagged in the last two reviews, unresolved but not worsening. **Good news: the HOME/USDT weakest-symbol-vs-active-long contradiction that ran ~19h41m+ and was escalated to high priority at 11:44 EEST has resolved** — HOME/USDT is off both fresh weakest-symbols tables this cycle. **Bad news: a new, structurally identical contradiction has appeared on FIDA/USDT** — it now sits on both fresh weakest-symbols tables (bias short, ~-9%) while carrying an active triggered long B-tier swing position (68.5, entered 2026-08-05). DODO/USDT — the prior review's cleanest long-watch — has since gone `entry_moved_away` on both its intraday and swing signals and is no longer live. In its place, a brand-new intraday B-tier long fired via the watchlist monitor only ~5 minutes before this review: **COTI/USDT (68.6, waiting_for_entry)**, today's freshest and cleanest long-watch. **3 untracked legacy crypto scalp alerts** (HEI/USDT, BICO/USDT, SYN/USDT, sent 10:44 UTC) were confirmed via `detect_untracked_legacy_alerts` — Telegram-pushed but with no matching `proposed_signal`, a recurrence of a previously-flagged integrity bug pattern. On the stocks side, the new **pre-US stocks review overlay** evaluated its 3 eligible candidates (GS, SMH, MSTR) — all three came back **CAUTION** (chase risk, sector contradiction, and technical indecision respectively); none qualified for SUPPORT/promotion, so **0 stocks names are promoted to the pre-open Paper lane this cycle**. Catalyst mapping remains weak: **64.5% unmapped** cumulative today (1612/2500), above the 50% threshold. Premarket US context (WebSearch): SPY +0.22%, DIA +0.33%, IWM +0.23%, but **QQQ -0.30% and semiconductors broadly weak premarket** (SMH -0.14%, Micron -3.4%, SK Hynix -6.1%) — a mixed, not clean risk-on, setup into the open.

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-06_10-37_scalp_report.md` (data freshness 10:30 UTC, generated 13:36 EEST — ~2.5h old; A/B empty, scalp mode kill-switched, only C-tier/rejected), `data/reports/intraday/2026-08-06_10-54_intraday_report.md` (generated 13:54 EEST — ~2.2h old; 4 B-tier longs HEI/DODO/HOME/BICO at report-generation time, since re-checked live against the DB — DODO has since moved away, COTI has since fired fresh), `data/reports/swing/2026-08-06_02-35_swing_report.md` (generated 05:35 EEST — ~10.5h old, **carry-forward band 4-12h**, flagged; 6 B-tier longs MIRA/KITE/TUT/BICO/SYN/HEI, cross-checked against fresher scalp/intraday for regime divergence — none found this cycle, both now read "uptrend").
- Stocks: `data/reports/stocks/intraday/2026-08-06_11-31_stocks_intraday_report.md` (generated ~14:31 EEST — freshest source this cycle, ~1.7h old; **market closed (after-hours/pre-market UTC overnight)** — all A/B demoted to C, `market_closed_intraday_planning_only`; 84/84 symbols ok, 10/10 indices, 12/12 sector ETFs, no fetch failures). Stocks swing/invest: last generated 2026-07-02 — stale >1 month, excluded per standing policy.
- `data/catalysts/2026-08-06/catalyst_events.jsonl` (cumulative today, direct read: 888 mapped / 1612 unmapped of 2500 rows = 64.5% unmapped), `narrative_baskets.jsonl` and freshest `catalyst_cycle_11-01.md` (500 news_items scanned, 500 events, 2 baskets — `binance_ecosystem_teaser` BNB primary/ASTER related, `momentum_breakout` HEI/ZBT/HFT primary, BICO/COTI related, playbook `avoid_chase`).
- CLI: `active-signals --asset-class crypto` (42 rows), `active-signals --asset-class stocks` (50 rows, all C-tier/legacy remnants, 0 A/B actionable), `signal-stats --asset-class crypto` (weekly: tier B n=128, PF 2.69, avgR 0.39, triggered winrate 23.97% — CLI's own observation flags this as low), `signal-stats --asset-class stocks` (weekly: tier C n=225, triggered winrate 1.9%, PF 0.79 — both below the CLI's own flag thresholds), `detect_untracked_legacy_alerts --since 2026-08-06` (**3 untracked** — HEI/USDT, BICO/USDT, SYN/USDT scalp, sent 10:44:35-10:44:38 UTC).
- DB (read-only queries): `proposed_signals` filtered by symbol for HOME/EPIC/DODO/STO/FIDA (confirms unchanged status on STO/FIDA/EPIC holds, DODO `entry_moved_away` on both rows); `proposed_signals` filtered `status='waiting_for_entry'` ordered by `created_at DESC` (surfaced COTI/USDT fired 2026-08-06T12:54:05Z, ~17min before this review's data pull); `news_items` filtered on GS/SMH/MSTR symbol tags in the last 24h (GS: 5 rows, mostly tangential "Goldman Sachs Names..." analyst-mention, not GS-as-subject; SMH: 1 generic row; MSTR: 5 rows, Saylor/Bitcoin commentary, mixed-to-cautious tone, not a fresh bullish trigger).
- New this slot — **Stocks Pre-US Review Overlay**: `python -m src.cli stocks-preus-candidates` (3 eligible: GS, SMH, MSTR; 31 excluded — 22 `NO_ENTITY_RESOLVED_CATALYST`, 8 `EARNINGS_BLACKOUT`, 1 `LEGAL_RISK`=MSFT); verdicts built and ingested via `stocks-preus-review-ingest --json data/raw/enriched_review_sources/preus_review_2026-08-06T1300Z.json` — see §5.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_1144.md` (Europe / pre-US context, 11:44 EEST).
- **External web research invoked this cycle** (WebSearch x5, WebFetch x2 — 1 succeeded, 1 returned HTTP 403 and was not re-tried against the same URL): BTC price check; general Aug-6 premarket roundup (SPY/QQQ/DIA/IWM/SMH); GS-specific price/news check; MSTR-specific price/news check; GS news search (found Aug-5 close level). WebFetch: `thestreet.com` premarket article → 403 Forbidden (not used, no data extracted); `cryptotimes.io` MSTR article → succeeded, used for MSTR technical/catalyst framing.

## 3. Scheduler / Data Freshness

- **Pre-US schedule check:** target 08:55 ET, actual fire/data-gathering window ~08:59-09:11 ET (Δ+4 to +16min, within tolerance — not one of the 2026 DST-mismatch windows, which are 2026-03-08 to 2026-03-29 and 2026-10-25 to 2026-11-01; today, 2026-08-06, is outside both).
- `scheduler.log` in `data/scheduled_runs/2026-08-05_default_schedule/` (folder date-stamped from when the cycle started but continuously active past midnight, current live cycle folder) — mtime 14:53 EEST, ~1h18min old at review start — fresh, not deferred (defer threshold is 3h). Latest `cycle_06_13-24_summary.md` mtime 14:53 EEST — same freshness.
- Crypto scalp/intraday ~2.2-2.5h old (fresh-to-borderline; still inside useful window), swing ~10.5h old (**carry-forward band 4-12h**, flagged; cross-checked against fresher reports for regime divergence — none found, "uptrend" consistent across scalp/intraday/swing this cycle, unlike last review's ETH divergence).
- Stocks: 11:31 EEST-generated report (14:31 EEST-equivalent) — 84/84 symbols, 10/10 indices, 12/12 sector ETFs succeeded, no data-fetch issues.
- Data-quality anomalies this cycle: (1) 3 untracked legacy crypto scalp alerts (HEI/BICO/SYN, sent 10:44 UTC) — Telegram-pushed with no matching `proposed_signal`, confirmed via direct CLI run, a recurrence of a previously-documented watchlist-alert/signal-reuse-style integrity pattern (§14); (2) catalyst mapping weak and essentially flat, 64.5% unmapped vs 62.4% at 11:44 EEST — still above the 50% threshold; (3) FIDA/USDT weakest-symbol-vs-active-long contradiction — newly observed this cycle, structurally identical to the now-resolved HOME/USDT pattern (§14); (4) DODO/USDT's last-cycle long-watch has gone stale (`entry_moved_away` on both rows) — a reminder that report-embedded trade ideas can go stale within a single ~2-3h review cycle and must be cross-checked live against the DB, which this review did.
- **TradingView / manual chart check unavailable** — no chart MCP loaded this cycle; all price-structure statements are from local OHLCV/ATR/EMA fields in the reports plus the WebSearch/WebFetch checks cited in §13.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-06 16:11 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["no fresher swing report than ~10.5h-old 05:35 EEST snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log and latest cycle summary both ~1h18min old, well within tolerance", "crypto swing report ~10.5h old (carry-forward band, upper end), scalp/intraday ~2.2-2.5h old", "stocks report 84/84 symbols ok, no fetch issues", "3 untracked legacy scalp alerts this cycle (HEI/BICO/SYN)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["risk_on", "mixed", "longs_preferred", "wait_for_trigger"],
      "data_missing": ["no live intraday BTC/ETH tick beyond internal reports + WebSearch level check"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC ~$64,580-64,876 (externally verified), up 0.8-1.3% 24h; regime 'bullish trend (risk-on)' consistent across all 3 fresh crypto reports", "altcoin breadth 61.36% above EMA20 (scalp/intraday, fresh)", "macro/geopolitics risk still pinned at 100/100 ceiling -- unresolved but not worsening vs 11:44 EEST", "stocks premarket mixed: SPY +0.22%, DIA +0.33%, IWM +0.23% vs QQQ -0.30% and semis broadly weak (SMH -0.14% premarket, MU -3.4%, SK Hynix -6.1%)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["64.5% unmapped today (1612/2500 cumulative catalyst_events.jsonl), essentially flat vs 62.4% at 11:44 EEST, still above the 50% threshold", "freshest scan (14:01 EEST): 2 baskets -- binance_ecosystem_teaser (BNB primary) and momentum_breakout (HEI/ZBT/HFT primary, BICO/COTI related, avoid_chase playbook)", "COTI/USDT -- today's freshest long-watch -- carries no fresh verified catalyst per its own raw_idea_json (news_influence_contract.supported=false)", "GS/SMH/MSTR (stocks pre-US overlay): none had a genuinely fresh, entity-resolved, confirming catalyst -- GS's only hits were tangential analyst-mention, SMH's was one generic article, MSTR's were mixed-to-cautious Saylor/BTC commentary"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable", "squeeze_risk"],
      "data_missing": ["no fresh per-symbol funding/OI beyond what the intraday report embeds for COTI"],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/USDT: funding -0.000267, OI down (short covering), crowding normal -- no red flag but no strong confirmation either", "HFT/USDT: funding 0.0031, 'extreme long crowding' -- standing flag, carried across multiple reviews", "SPCXB/USDT: unchanged, still capped for squeeze risk and no derivatives data (carried context only this cycle, no new information)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_fresh", "chase_risk", "price_moved_away", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/USDT: fired via watchlist monitor ~17min before this review's data pull; entry zone 0.01436-0.01473, current price ~0.0149 per raw_setup snapshot -- essentially at/just above the zone, not a chase yet but close; invalidation 0.01390, RR to TP1 1.84", "DODO/USDT: both intraday and swing rows are now status=entry_moved_away -- the setup that anchored the 11:44 EEST review is no longer live, confirming the value of live DB cross-checks over report-only reads", "GS: closed Aug 5 at $1075.55 (+1.98%), already above the paper-entry trigger of $1060.53 set intraday -- chase-risk flag for a clean breakout-confirmation entry design", "SMH: -0.14% premarket with semiconductor peers (Micron -3.4%, SK Hynix -6.1%) broadly weak -- contradicts the underlying long signal's own sector"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry"],
      "data_missing": ["CLI does not label lifecycle state directly -- classification is manual, from active-signals status + DB queries"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto CLOSED since last review: none newly closed -- no fresh TP/stop hits observed on STO/FIDA/EPIC/the 6-name overnight cluster between 11:44 and 16:11 EEST", "Crypto WAITING for entry (fresh): COTI/USDT intraday (68.6, fired 12:54 UTC)", "Crypto NO-ENTRY/STALE/MOVED-AWAY: DODO/USDT intraday and swing, both entry_moved_away", "Crypto ENTERED UNRESOLVED (unchanged holds): STO/USDT swing (78.1), FIDA/USDT swing (68.5, now also flagged for the weakest-symbol contradiction), HOME/USDT x2 swing (68.5, 67.3 -- contradiction resolved this cycle), EPIC/USDT swing (69.5), 6-name overnight cluster", "Stocks: 0 OPEN, all 50 active-signals rows C-tier or legacy expiry remnants; market not yet open; pre-US overlay evaluated 3 eligible candidates, promoted 0"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["manual_review", "legal_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["FIDA/USDT: new weakest-symbol-vs-active-long contradiction this cycle, structurally identical to the just-resolved HOME/USDT pattern -- do not add fresh exposure until reconciled", "3 untracked legacy scalp alerts (HEI/BICO/SYN) -- Telegram-pushed but untrackable for PF/winrate, a recurring integrity-bug pattern worth escalating", "MSFT (stocks) still hard-gated LEGAL_RISK (class_action, securities_fraud) by the pre-US candidate builder -- never eligible, consistent with prior reviews", "GS/SMH/MSTR: all 3 pre-US-eligible candidates came back CAUTION (adjustments -4/-6/-5) -- none cleared the bar for SUPPORT; no promotion to the paper lane this cycle"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly (tier B, n=128, reliable): PF 2.69, avgR 0.39, triggered winrate 23.97% -- CLI's own observation flags this as low despite healthy PF; weekend-mode signals separately flagged as underperforming", "stocks weekly (tier C, n=225, reliable): triggered winrate 1.9%, PF 0.79 -- both below the CLI's own flag thresholds, unchanged known pattern, C-tier never actionable", "stocks-intraday 14d diagnostics: top avoidable loss bucket is no_gate_context (-375.00R over 735 rows) -- a data-labeling gap, not a live-money loss, but the largest single failure-reason bucket by far"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "longs_preferred", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: tape constructive and regime unchanged, but macro/geopolitics risk still pinned at 100/100 -- selective, not unambiguous, risk-on", "COTI/USDT is the cleanest fresh crypto long-watch this cycle -- fired minutes before this review, entry zone essentially at current price, no in-house avoid_chase tag (unlike the DODO/momentum_breakout family)", "stocks: none of the 3 pre-US-eligible names (GS/SMH/MSTR) cleared the bar for a clean pre-open long; SMH's own sector is premarket-weak, GS is already through its trigger (chase risk), MSTR is in a technical holding pattern -- no stock name is a clean pre-open long into the 09:30 ET open", "FIDA/USDT's new contradiction is the top risk-manager item this cycle, directly analogous to the just-resolved HOME/USDT case", "the 3 untracked legacy scalp alerts are a recurring integrity issue worth escalating, not a one-off"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "COTI/USDT", "trigger": "intraday B-tier (68.6) waiting_for_entry, fired ~17min before this review; fill inside 0.01436-0.01473, invalidation (1h close beyond) 0.01390, RR to TP1 1.84 -- freshest, cleanest crypto long-watch this cycle, no avoid_chase tag" },
    "best_short_candidate":    { "symbol": "SMH", "trigger": "semiconductor sector explicitly weak (RS vs SPY 20d -7.20%, 'weak' status) and premarket-weak (-0.14%, with Micron -3.4% and SK Hynix -6.1% dragging peers) -- the desk's own signal on SMH is a long (now CAUTION/demoted to rejected-tier by the pre-US overlay); no defined short structure exists yet -- watch for a confirmed breakdown through RTH support with volume at the open before treating as a tradeable short" },
    "best_catalyst_candidate": { "symbol": "BNB/USDT", "trigger": "binance_ecosystem_teaser basket (primary BNB, related ASTER, playbook related_beta_rotation, fresh <1h per the 14:01 EEST scan) -- no defined entry yet in any report; watch for a confirmed technical setup once the narrative firms up" },
    "avoid_candidate":         { "symbol": "FIDA/USDT", "reason": "new weakest-symbol-vs-active-long contradiction this cycle (bias short ~-9% on both fresh weakest-symbols tables) while carrying an active triggered long B-tier swing position (68.5) -- do not add fresh exposure either direction until reconciled, same pattern that took ~19h41m to resolve on HOME/USDT" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.65 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.6 | risk_on, mixed, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.5 | oi_supports, data_unavailable, squeeze_risk | advisory_only |
| technical_entry | caution | 0.55 | entry_fresh, chase_risk, price_moved_away, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.6 | open_actionable, waiting_for_entry, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.6 | manual_review, legal_risk, reduce_risk | advisory_only |
| playbook_performance | ok | 0.6 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.6 | mixed, longs_preferred, wait_for_trigger, manual_review | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_1144.md` (11:44 EEST, Europe / pre-US context):

- **Resolved:** HOME/USDT's weakest-symbol-vs-active-long contradiction, which ran ~19h41m+ and was the last review's top escalated TODO, is **off both fresh weakest-symbols tables this cycle** — the 2 active triggered long swing positions remain untouched, unchanged.
- **New:** FIDA/USDT now shows the **same class of contradiction** — bias short (~-9% 24h) on both fresh weakest-symbols tables while carrying an active triggered long B-tier swing position (68.5). This is a fresh instance, not a resolve-then-recur — first observed this cycle.
- **Stale/expired:** DODO/USDT, the last review's best long-watch, has gone `entry_moved_away` on both its intraday and swing signal rows — no longer live. This is a reminder that report-embedded trade ideas require a live DB cross-check, not just a report read, especially near the multi-hour edge of a review cycle.
- **New:** COTI/USDT intraday B-tier long (68.6) fired via the watchlist monitor at 2026-08-06T12:54:05Z (~15:54 EEST) — only ~17 minutes before this review's data pull. Today's freshest, cleanest crypto long-watch.
- **New this slot:** the **Stocks Pre-US Review Overlay** ran for the first time this cycle (§5) — 3 eligible candidates (GS, SMH, MSTR) evaluated, all returned CAUTION, 0 promoted.
- **Unchanged:** STO/USDT (78.1), FIDA/USDT (68.5, now also flagged), EPIC/USDT (69.5, contradiction still resolved), the 6-name overnight swing cluster — all holding, no new fills or stops.
- **Worsened slightly:** catalyst mapping 62.4% → 64.5% unmapped — still above the 50% threshold, essentially flat/slow-drift, not a sharp change.
- **Unchanged:** macro/geopolitics risk still pinned at 100/100.
- **New:** 3 untracked legacy crypto scalp alerts this cycle (0 at 11:44 EEST) — HEI/BICO/SYN sent 10:44 UTC without a matching `proposed_signal`.
- **Invalidated:** none.

## 5. Catalyst Coverage

- Cumulative today (`catalyst_events.jsonl`, direct read): mapped **888**, unmapped **1612**, total **2500** rows → **64.5% unmapped**, essentially flat vs 62.4% at 11:44 EEST.
- Freshest single scan (`catalyst_cycle_11-01.md`, 14:01 EEST): 500 `news_items` scanned, 500 events, 2 active narrative baskets — `binance_ecosystem_teaser` (primary BNB/USDT, related ASTER/USDT, playbook `related_beta_rotation`, fresh <1h) and `momentum_breakout` (primary HEI/ZBT/HFT/USDT, related BICO/COTI/USDT, playbook `avoid_chase`, fresh <1h).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** 64.5% unmapped, above the 50% threshold.
- Top unmapped headlines (sample): "Creative Technology presenta Creative XF1, el altavoz..." (non-English product PR, no ticker), "Notice of Q2 Results and Investor Presentation" (generic, no entity resolved), "Oma Savings Bank Plc to publish its Half-Year Financial Report..." (foreign small-cap earnings-wire, no US ticker match) — consistent with prior cycles' pattern of macro/earnings-wire/foreign-language items without a clean single-symbol tag.

### Pre-US Stocks Review Overlay
- candidates reviewed: 3 (SUPPORT 0 / NEUTRAL 0 / CAUTION 3 / BLOCK 0 / INSUFFICIENT_DATA 0)
- session-cap-only C's now eligible for pre-open Paper lane: **0** — all 3 candidates (GS, SMH, MSTR) were assessed CAUTION with negative adjustments; none reached the SUPPORT bar required for promotion.
  - GS: base 65.02 → adjusted 61.02 (enforced tier: C) — chase risk (already above entry trigger pre-open) + no fresh Aug-6 catalyst.
  - SMH: base 54.42 → adjusted 48.42 (enforced tier: rejected) — sector explicitly weak, premarket weak, not even pre-gate-B.
  - MSTR: base 95.71 → adjusted 90.71 (tier_from_score computed: A on the adjusted number alone) — **not treated as promoted**: my verdict was CAUTION (technical consolidation, no fresh confirming catalyst, crypto macro risk-off backdrop), and this review's operator guidance is watch-only, not actionable, regardless of the raw tier-from-score recompute.
- excluded by hard gate: 31 — 22 `NO_ENTITY_RESOLVED_CATALYST` (CAT, ORCL, NOW, BAC, PANW, GE, CRM, ADBE, XLE, XLK, IWM, XLY, QQQ, XLV, XLF, DIA, V, CRWD, NOC), 8 `EARNINGS_BLACKOUT` (SPY, AMD, META, XOM, AVGO, LLY, PLTR, NFLX, NVDA, JPM, WMT — earnings-window symbols), 1 `LEGAL_RISK` (MSFT — class_action, securities_fraud, standing gate, never promotable).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **selective risk-on**, background macro caution unchanged — BTC ~$64,580-64,876 (externally verified), up 0.8-1.3% 24h; regime "bullish trend (risk-on)" consistent across scalp/intraday/swing; altcoin breadth 61.36% above EMA20. Macro/geopolitics risk still pinned at 100/100 (Iran/Strait-of-Hormuz) — a standing background caution, not a directional call.
- Stocks mood: **pre-market, mixed** — SPY +0.22%, DIA +0.33%, IWM +0.23% (modestly constructive) vs QQQ -0.30% and semiconductors broadly weak premarket (SMH -0.14%, Micron -3.4%, SK Hynix -6.1%). VIX 15.85 (last verified level, Wednesday close), breadth 100% above EMA20/50 on that same stale-by-a-day read. This is not a clean risk-on premarket tape — treat as mixed/rotational, not broadly bullish, into the open.
- Dominant narrative: crypto — the no-catalyst momentum cluster (now COTI/USDT freshest, HEI/ZBT/HFT/BICO family) remains the desk's most active playbook, tagged `avoid_chase` at the basket level even though COTI's own signal carries no such tag; `binance_ecosystem_teaser` (BNB/ASTER) is a fresh <1h basket worth watching. Stocks — semiconductor weakness is the dominant premarket theme, cutting against the one semis-adjacent signal (SMH long) the desk is currently tracking.
- Preferred side now: **longs (crypto, selective)** — COTI/USDT is the cleanest fresh idea; **wait (stocks)** — no clean pre-open long or short exists among the 3 eligible names, build the RTH watchlist and require confirmation at/after the open.
- Best long candidate: **COTI/USDT** (crypto intraday B-tier, fresh, 68.6) — see §7/§8.
- Best short candidate: **SMH watch-only** — premarket-weak sector, but no confirmed breakdown structure exists yet; not a clean short today, see §8 for the exact trigger.
- Best catalyst-backed candidate: **BNB/USDT** (binance_ecosystem_teaser basket, fresh <1h) — watch-only, no defined entry.
- What to avoid: **FIDA/USDT** fresh exposure either direction (new contradiction); **GS** chasing above its already-cleared entry trigger; **SMH long** while its own sector reads weak premarket; the crypto scalp mode generally (still kill-switched, and today produced 3 untracked legacy alerts).
- What would change the view: macro/geopolitics risk easing off the 100/100 ceiling; a human reconciling FIDA/USDT's contradiction; the US cash open (09:30 ET / ~16:30 EEST) providing a live, confirmed read on SPY/QQQ/SMH direction; a confirmed breakdown structure appearing for SMH or a confirmed breakout with volume for GS/MSTR.

## 7. Candidate Deep Dives

### COTI/USDT (crypto intraday, B-tier long, 68.6, waiting_for_entry — today's freshest long-watch)
- Has price already reacted to the catalyst? No fresh verified catalyst exists (`news_influence_contract.supported=false` in the signal's own record) — pure momentum/RS thesis.
- Is the setup chasing? Fired ~17min before this review's data pull; entry zone 0.01436-0.01473, current price ~0.0149 per the signal's own `raw_setup` snapshot — essentially at/just above the top of the zone, not yet a clear chase but close; confirm the fill happens inside the defined zone, do not buy market if it runs further.
- Retest/pullback structure? Yes, explicitly defined: entry 0.01436-0.01473, invalidation (1h close beyond) 0.01390, TP1/TP2/TP3 0.01573/0.01656/0.01739, RR to TP1 1.84.
- Would entry now be late? Only if bought above the zone without waiting for a clean fill — the underlying playbook explicitly warns against market-buying an extended print.
- Is this aligned with market mood? Yes — bullish-trend regime, selective-longs style, RS vs BTC +10.04%, no in-house `avoid_chase` tag (unlike the DODO/HEI/ZBT/HFT `momentum_breakout` basket family).
- Long/short/wait: **wait for a clean fill inside 0.01436-0.01473; do not chase above it.**
- Chase-risk: low-to-moderate given the price is right at the zone edge, not deep inside it — treat as medium confidence.
- Catalyst confirmation/contradiction: none found; pure technical/RS setup.

### FIDA/USDT (crypto — weakest-symbol vs active-long contradiction, newly observed this cycle)
- On both the freshest scalp (10:37 EEST, 13:36 gen) and intraday (10:54 EEST, 13:54 gen) weakest-symbols tables: bias short, 24h -9.03% (scalp) / -9.32% (intraday), while carrying 1 active triggered long B-tier swing position (68.5, entered 2026-08-05T20:07:56Z, invalidation 0.01867143, untouched).
- This is structurally identical to the just-resolved HOME/USDT pattern — same class of finding, different symbol, first observed this cycle (not a resolve-then-recur yet).
- Would a fresh entry now be late (for a hypothetical short)? No defined short setup exists for FIDA/USDT in any report; this remains a data-consistency flag, not a tradeable idea.
- What level would make a short actionable? Only after the scanner generates a confirmed failed-bounce/breakdown structure — none exists currently.
- Mood alignment: the bias-short read cuts against the broader crypto risk-on tape — idiosyncratic/technical, not market-wide.
- Long/short/wait: **wait** — do not add fresh exposure in either direction; monitor whether the existing long's invalidation (0.01867143) is hit.
- Chase-risk: N/A. Catalyst confirmation/contradiction: none found; pure internal-consistency flag, new top-priority TODO (§14).

### MSTR (stocks, pre-US overlay eligible, pre_gate_tier A, base 95.71 → adjusted 90.71, verdict CAUTION)
- Catalyst: mostly Saylor/Bitcoin commentary (5 news_items hits in 24h) — "sold 1,638 BTC for $104.73M," "six consecutive weeks without buying Bitcoin," a CEO quote favoring patience over aggressive accumulation. Entity-resolved and fresh, but **mixed-to-cautious in tone**, not a clean bullish trigger for a breakout long.
- Premarket / market context: no MSTR-specific premarket figure found via WebSearch; general market premarket is mixed (QQQ -0.30%); BTC itself is modestly up (+0.8-1.3% 24h) but macro/geopolitics risk is pinned at 100/100 — a genuine headwind for a Bitcoin-proxy equity.
- Setup quality: per WebFetch (cryptotimes.io), MSTR is "trading within a symmetrical triangle... since June 2026," resistance ~$109, support ~$88 — technical indecision, not a confirmed breakout. Stock closed ~$95.14 area Aug 3, i.e. mid-range in the triangle.
- Legal/headline check: no fresh SEC/legal item for MSTR in the 48h fresh-legal list or the production risk-warnings block; the only BTC-linked risk warning in the crypto reports (`token_unlock`) is tagged to BTC itself, not MSTR specifically.
- Verdict rationale: catalyst is entity-resolved and fresh but not confirming; no genuine RS-vs-sector leadership evidence gathered; technical setup is indecisive (mid-triangle). **CAUTION, adjustment -5** (enforced by the ingest command; adjusted score 90.71, `tier_from_score` alone computes A on the number, but this review's operator guidance remains watch-only — no promotion to Paper lane).
- Long/short/wait: **watch-only** — a confirmed break above $109 with volume, or below $88, would be the actionable trigger; neither has happened.

### GS (stocks, pre-US overlay eligible, pre_gate_tier B, base 65.02 → adjusted 61.02, verdict CAUTION)
- Catalyst: news_items hits are mostly tangential ("Goldman Sachs Names 2 European Stocks It Says Can More Than Double" — GS as the analyst, not the subject); UBS price-target raise to $1,150 is dated Aug 3, not fresh for Aug 6. No genuine GS-specific fresh catalyst found.
- Premarket / market context: GS closed Aug 5 at **$1,075.55 (+1.98%)**, already **above** the paper-entry-profile trigger of **$1,060.53** set intraday on Aug 6 02:14 UTC — i.e. price has already run through the defined breakout level before this review, ahead of any fresh confirmation window. Financials sector (XLF) status "mixed," RS vs SPY 20d +2.24% — modest, not leader-grade.
- Setup quality: strong underlying fundamentals (78% net-earnings growth cited in search results) but that is known/priced information, not a fresh Aug-6 trigger; the entry design (`one_closed_15m_bar_beyond_trigger_and_vwap`) implies a fresh breakout confirmation is expected, and price is already past the level pre-open — genuine chase-risk for that specific entry profile.
- Legal/headline check: no fresh SEC/legal item for GS in the 48h fresh-legal list or production risk-warnings block.
- Verdict rationale: **CAUTION, adjustment -4** — chase risk (price already through trigger) + no fresh confirming catalyst, despite a reasonable fundamental backdrop and no hard legal/earnings gate.
- Long/short/wait: **watch-only** — would need a fresh pullback-and-reclaim of the trigger level with volume at/after the open to be clean, rather than chasing the pre-existing gap-through.

### Untracked legacy crypto scalp alerts (system-integrity anomaly, 3 today)
- `detect_untracked_legacy_alerts --since 2026-08-06` returned 3 rows: HEI/USDT (B, scalp, 74.6, long, 10:44:35 UTC), BICO/USDT (B, scalp, 71.9, long, 10:44:37 UTC), SYN/USDT (B, scalp, 67.6, long, 10:44:38 UTC) — all sent to Telegram via `watchlist_alerts` with **no matching `proposed_signal`** within the detector's window, meaning these will not contribute to PF/winrate/avgR tracking.
- This directly contradicts the standing expectation that crypto scalp mode is fully kill-switched (confirmed clean at 0 instances in the 11:44 EEST review) — the mode itself producing zero new `proposed_signals` rows does not prevent the separate `watchlist_alerts` path from firing and sending Telegram messages that reference stale or reused signal context.
- Long/short/wait: N/A — this is a pipeline-integrity finding, not a trade idea. No position implication either way.
- Escalated as a high-priority TODO (§14) given the pattern's prior history.

*(Excess candidates not given a full deep dive, per the 5-candidate cap: STO/USDT swing (78.1, triggered) — steadiest carried position, unchanged, hold; EPIC/USDT swing (69.5, triggered) — contradiction remains resolved, no new information; the 6-name overnight cluster (MIRA/KITE/TUT/BICO/SYN/HEI swing) — unchanged holds; SMH (stocks pre-US overlay, CAUTION, adjusted 48.42/rejected) — see §5/§6 for the short-watch framing; SPCXB/USDT — unchanged, still capped, no new information this cycle.)*

## 8. Best Candidates Ranked

1. **COTI/USDT (crypto intraday long, waiting_for_entry, B-tier, 68.6)** — freshest, cleanest long-watch; fill only inside 0.01436-0.01473, invalidation 0.01390.
2. **STO/USDT (crypto swing long, triggered, B-tier, 78.1)** — steadiest open position, unchanged; hold.
3. **FIDA/USDT (crypto swing long, triggered, B-tier, 68.5)** — filled, no TP yet, but now carries the new weakest-symbol contradiction; hold the existing position, do not add.
4. **MSTR (stocks, pre-US overlay, adjusted 90.71, verdict CAUTION)** — best stocks watch by raw score, but technically indecisive (mid-triangle); watch for a confirmed break of $109 or $88 with volume after the open.
5. **SMH (stocks, pre-US overlay, verdict CAUTION, best short-watch)** — sector explicitly weak and premarket-weak; watch for a confirmed breakdown through RTH support with volume; no clean entry yet.

**FIDA/USDT** carries this cycle's explicit new-contradiction flag (see §6/§9) even while ranked #3 on the hold list — its existing position is not being closed, but no fresh exposure should be added. **GS** is this cycle's clearest stocks avoid (chase risk, already through trigger) rather than a ranked watch. No stocks name is actionable pre-open; the RTH watchlist to carry into the 18:30 EEST US-open-reaction review is GS/MSTR/SMH plus the standing MSFT legal-risk exclusion.

## 9. Avoid / No Trade

*(This applies to this decision window only — scanning, tracking, and the scheduler continue unchanged.)*

- **FIDA/USDT fresh exposure, either direction** — new weakest-symbol-vs-active-long contradiction this cycle; hold the existing position, do not add.
- **Chasing GS above $1,060.53** without a fresh pullback-and-reclaim with volume — price has already cleared the paper-entry trigger pre-open.
- **SMH as a long** — the desk's own signal is long, but the underlying sector (semiconductors) reads explicitly weak both on 20d RS (-7.20% vs SPY) and premarket (-0.14%, with Micron/SK Hynix down sharply) — a direct contradiction.
- **Crypto scalp mode generally** — still kill-switched for signal registration, but produced 3 untracked legacy Telegram alerts this cycle (HEI/BICO/SYN), a separate and unresolved integrity gap (§14).
- **MSFT (stocks)** — standing hard gate, `LEGAL_RISK` (class_action, securities_fraud), never promotable regardless of score.
- **All other stocks C-tier watchlist names** (JPM, NVDA, DIA, NFLX, PLTR, XLV, QQQ, XLY, IWM, LLY, XLF, AVGO, XOM, etc.) — market not yet open, planning-only; several also carry `EARNINGS_BLACKOUT` gates per the pre-US candidate builder.

## 10. Main Risks

- **A brand-new FIDA/USDT contradiction has replaced the just-resolved HOME/USDT one** — the underlying root-cause hypothesis (a shared OHLCV-window/timeframe mismatch between the "weakest symbols" momentum table and the swing-signal scoring pipeline) is now reinforced by a second, independent instance rather than resolved; still needs a human trace (§14, carried and updated).
- **3 untracked legacy crypto scalp alerts this cycle** — a Telegram-pushed, PF/winrate-invisible alert path that is separate from (and not fixed by) the scalp-mode registration kill-switch; needs a human trace of the `watchlist_alerts` code path (§14).
- Macro/geopolitics risk remains **pinned at the 100/100 ceiling** for a third consecutive review — a standing background caution on crypto sizing, not a directional call.
- Catalyst mapping remains weak (64.5% unmapped) — treat all catalyst-basket framing as directional color only.
- **Stocks premarket is genuinely mixed, not clean risk-on** — semiconductors broadly weak (SMH, Micron, SK Hynix) against modestly positive SPY/DIA/IWM; do not treat the pre-US overlay's "0 promoted" result as evidence of a fixable gap — it correctly reflects a session where none of the 3 eligible names had a clean, fresh, confirming setup.
- DODO/USDT going stale (`entry_moved_away`) within roughly 2.5-3h of the review that surfaced it as the top long-watch is a reminder that report-embedded ideas decay fast intraday; this review's practice of cross-checking active-signal status live against the DB caught it — future cycles should keep doing the same.

## 11. Action Plan — next 4 hours

- Let COTI/USDT fill cleanly inside 0.01436-0.01473 or expire — do not chase above the zone.
- Hold STO/USDT, FIDA/USDT, EPIC/USDT, and the 6-name overnight swing cluster into their invalidations/targets; no new sizing on any of them, and specifically no fresh FIDA/USDT exposure given its new contradiction.
- Do not chase GS above $1,060.53; watch for a confirmed pullback-and-reclaim with volume at/after the 09:30 ET open instead.
- Watch MSTR for a confirmed break of $109 (bullish) or $88 (bearish) out of its current triangle, with volume, once RTH opens.
- Watch SMH for a confirmed breakdown structure through RTH support with volume — the cleanest stocks short-watch, but not yet actionable.
- Do not open any fresh position on symbols carrying an unresolved weakest-symbol contradiction (FIDA/USDT this cycle) until manually reconciled.
- Flag the 3 untracked legacy scalp alerts (HEI/BICO/SYN) for a human trace of the `watchlist_alerts` code path — do not treat this as evidence the scalp kill-switch itself has failed (registration remains at 0 new `proposed_signals`); it is a separate alert-delivery path.
- Continue scanning/tracking/monitors unchanged through the US cash open into the 18:30 EEST US-open-reaction review — this review recommends caution on specific entries and two carried/new integrity-tracking items only, never a pause of any kind.

## 12. Final Verdict per Mode

- **Crypto scalp:** should remain fully disabled per the documented kill-switch; correctly showing zero new `proposed_signals` registrations, but 3 untracked legacy Telegram alerts fired via a separate path this cycle (§14) — treat scalp as **not tradeable** regardless of any score shown, and treat the alert path as a fresh integrity concern.
- **Crypto intraday:** COTI/USDT (68.6, fresh, waiting_for_entry) is the live idea this cycle; DODO/USDT and SYN/USDT from the last review are stale/unchanged respectively.
- **Crypto swing:** the desk's steadiest bucket — STO/USDT (78.1) and FIDA/USDT (68.5, now flagged) hold unchanged; the 6-name overnight cluster unchanged; HOME/USDT's contradiction resolved this cycle (good); EPIC/USDT resolved, unchanged.
- **Stocks intraday:** market not yet open; zero actionable A/B; the new pre-US overlay evaluated 3 eligible names (GS/SMH/MSTR) and promoted 0 — all CAUTION. MSTR is the highest-score watch (technical indecision), GS carries chase-risk, SMH is the best short-watch (sector contradiction) but has no confirmed structure. MSFT remains hard-gated (legal risk).
- **Stocks swing/invest:** not evaluated — reports stale/deprecated since 2026-07-02, excluded per standing policy.

## 13. Sources

- Internal: `data/reports/scalp/2026-08-06_10-37_scalp_report.md`, `data/reports/intraday/2026-08-06_10-54_intraday_report.md`, `data/reports/swing/2026-08-06_02-35_swing_report.md`, `data/reports/stocks/intraday/2026-08-06_11-31_stocks_intraday_report.md`, `data/catalysts/2026-08-06/catalyst_events.jsonl`, `data/catalysts/2026-08-06/narrative_baskets.jsonl`, `data/catalysts/2026-08-06/catalyst_cycle_11-01.md`, `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items` read-only queries), `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_1144.md`.
- External (WebSearch x5, WebFetch x2 — 1 succeeded):
  - [Bitcoin price today, BTC to USD — CoinDesk / Fortune / Bybit / Bitget aggregate search](https://fortune.com/article/price-of-bitcoin-08-06-2026/) — BTC $64,579.64-64,876 range across venues, +0.82-1.27% 24h. Used for directional framing only.
  - Premarket roundup search (no single canonical URL, aggregate snippet): SPY +0.22%, QQQ -0.30%, DIA +0.33%, IWM +0.23%, SMH -0.14%, Micron -3.4%, SK Hynix -6.1% — [TheStreet Aug 6 2026 market today](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-6-2026), [Bloomberg Aug 6 2026 live updates](https://www.bloomberg.com/news/articles/2026-08-05/stock-market-today-dow-s-p-live-updates), [stockmarketwatch.com premarket](https://stockmarketwatch.com/live/stock-market-today).
  - [Goldman Sachs (GS) news/quote search aggregate](https://www.cnbc.com/quotes/GS) — GS closed $1,075.55 Aug 5 (+1.98%), 52wk range $705.55-$1,153.99, UBS PT raised to $1,150 (Aug 3).
  - [MicroStrategy/Strategy (MSTR) price prediction — CryptoTimes](https://www.cryptotimes.io/2026/08/04/strategy-stock-price-prediction-can-mstr-escape-its-august-slump/) — WebFetch succeeded; symmetrical triangle since June 2026, resistance ~$109/support ~$88, BTC sale 1,638 BTC July27-Aug2, CEO quote on accumulation patience.
  - WebFetch attempted on `thestreet.com` premarket article — **HTTP 403 Forbidden**, not used; premarket figures above sourced from the aggregate WebSearch snippet instead.
- No chart/TradingView source this cycle (unavailable, §3).

## 14. Fix Requests / TODO

### TODO-fida-usdt-contradiction-new (priority: high, new this cycle)
- **issue:** FIDA/USDT shows the weakest-symbol-vs-active-long conflict first observed this cycle: bias-short on both fresh weakest-symbols tables (scalp -9.03%, intraday -9.32% 24h) while carrying 1 active triggered long B-tier swing position (68.5).
- **evidence:** `data/reports/scalp/2026-08-06_10-37_scalp_report.md` and `data/reports/intraday/2026-08-06_10-54_intraday_report.md` "Weakest Symbols" tables; `db/crypto_ai_desk.sqlite` `proposed_signals` FIDA/USDT swing row (signal_id `sig_37e614d1a334af8c`, status=triggered, score 68.5, created 2026-08-05T20:07:56Z).
- **suggested manual fix:** structurally identical to the just-resolved HOME/USDT case (see the closed-out TODO history in `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_1144.md` §14) — check whether the "weakest symbols" momentum-score calculation and the long-signal scoring pipeline read the same OHLCV window/timeframe for FIDA/USDT specifically; since HOME/USDT's instance resolved on its own without a code change, first confirm whether this is a timing/window artifact common to both symbols before treating it as a standalone bug.
- **priority:** high
- **first observed:** 2026-08-06 16:11 EEST (this cycle).

### TODO-untracked-scalp-alerts-recurrence (priority: high, recurring pattern)
- **issue:** 3 untracked legacy crypto scalp alerts this cycle (0 at the last review) — HEI/USDT, BICO/USDT, SYN/USDT sent to Telegram via `watchlist_alerts` at 10:44:35-10:44:38 UTC with no matching `proposed_signal`, meaning these will never contribute to PF/winrate/avgR tracking despite being pushed live to the operator.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-06` output (3 rows, all `trackable: NO (no proposed_signal)`); crypto scalp mode's `proposed_signals` registration remains independently confirmed at 0 new rows, so this is a separate code path, not a scalp kill-switch failure.
- **suggested manual fix:** a human-driven session should trace the `watchlist_alerts` send path (likely reusing/generating a stale or orphaned `signal_id` reference) separately from the scalp-mode `proposed_signals` registration gate — this matches a previously-documented pattern of watchlist-alert/signal-reuse issues on other symbols; check whether the alert sender has its own independent trigger condition that bypasses the mode-level kill-switch.
- **priority:** high
- **first observed:** first noted informally in project history; this specific cycle's evidence: 2026-08-06 16:11 EEST (alerts sent 10:44 UTC / 13:44 EEST).

### TODO-catalyst-mapping-weak-flat (priority: low, carried forward, essentially flat)
- **issue:** Catalyst-to-symbol mapping coverage remains weak this cycle: 64.5% unmapped (1612/2500 cumulative rows) vs 62.4% at 11:44 EEST — a small further drift, continuing a pattern that has now been above the 50% weak-mapping threshold for at least 5 consecutive reviews.
- **evidence:** direct read of `data/catalysts/2026-08-06/catalyst_events.jsonl` (888 mapped / 1612 unmapped of 2500 rows); `data/catalysts/2026-08-06/catalyst_cycle_11-01.md` (freshest single scan, by-type breakdown shows `other_news: 454` of 500, i.e. the large majority of the freshest scan's events land in the generic/unmapped-style bucket).
- **suggested manual fix:** unchanged from prior cycles — a human-driven session should review the symbol-resolver logic in the catalyst layer (`src/news/` or the catalyst-scan agent) to understand why macro/earnings-wire/foreign-language headlines without an explicit US-ticker mention are not being mapped, and whether a broader fuzzy-match or sector-level fallback would reduce the unmapped rate without introducing false positives.
- **priority:** low
- **first observed:** tracked informally across several reviews; first formally escalated 2026-08-06 04:50 EEST; essentially flat this cycle (64.5% vs 62.4%).

_Note: TODO-home-usdt-contradiction (first raised 2026-08-05 15:58 EEST, escalated through 11:44 EEST as the desk's longest-running single-symbol data-consistency flag) is **resolved this cycle** — HOME/USDT is off both fresh weakest-symbols tables and its 2 active triggered longs remain untouched. Not deleting the historical record; closing it out and replacing it with TODO-fida-usdt-contradiction-new above, which may or may not be the same underlying root cause._
