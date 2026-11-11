# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:30 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context** (11:30 EEST — EU morning, build the US-session watchlist; US cash market not yet open, stocks are planning-only). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** External web research was available and used this run. Only **one crypto position is genuinely open**: **DEXE/USDT** intraday short (B-tier, entered 04:48 UTC, touch_r=0.0, expires 2026-07-31 04:48 UTC) — funding is deeply negative on both Bybit and MEXC, which is a squeeze-risk caveat against the short, not a reason to add. The last monitor snapshot (10:08 EEST) still shows **HOLO/USDT** and **RE/USDT** swing longs as "OPEN"; a direct DB check (more current) shows **both stopped out at -1.0R around 08:00 UTC** — both were no-catalyst counter-tape longs from the `momentum_breakout` basket, and both failed today, consistent with that basket's own documented weak edge. **COTI/USDT** swing long also closed -1.0R today. Net: three no-catalyst counter-tape crypto longs opened this morning, all three lost. Macro backdrop is a real, live driver today: the Fed held rates with 3 FOMC dissents and new Chair Kevin Warsh's hawkish inflation comments tanked stocks and spiked yields overnight (~01:00-02:30 UTC), and the US-Iran conflict in the Strait of Hormuz is ongoing (oil elevated, shipping war-risk premiums rising) — both verified externally. Stocks show a broad, high-scored (82-96) short bias across SPY/QQQ/IWM/NVDA/AVGO/META/PLTR/AMD/TSLA/SMCI/JPM, but every one is correctly gated to C-tier/planning-only because the US cash session is closed — needs RTH confirmation, not a chase signal. **META** and **PLTR** carry internal `legal_headline_risk` flags ("indictment" / "sec_doj"); external verification confirms real (but civil, not criminal) litigation risk for META plus a same-day earnings miss, while the PLTR flag looks like it may be triggered by routine, months-old law-firm shareholder-solicitation boilerplate rather than an actual government investigation — flagged for manual review, not treated as confirmed. Catalyst mapping is weak this run (67.3% unmapped). AAPL, AMZN, COIN, MSTR, MA report earnings today — do not chase into the print. Scanning, tracking, and monitors continue in every mood; this review recommends selective caution, never a stop.

## 2. Data Used

| File / Source | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-30_06-38_scalp_report.md` | 09:38 EEST | ~2h13m |
| `data/reports/intraday/2026-07-30_06-45_intraday_report.md` | 09:45 EEST | ~2h06m |
| `data/reports/swing/2026-07-30_01-36_swing_report.md` | 04:36 EEST | ~7h15m — **carry-forward** (4-12h bucket) |
| `data/reports/stocks/intraday/2026-07-30_07-02_stocks_intraday_report.md` | 10:02 EEST | ~1h49m |
| `data/reports/stocks/swing/…` / `invest/…` (2026-07-02) | deprecated/removed playbooks — see [[project_crypto_ai_desk_stocks_position_framework]], not a freshness failure |
| `data/catalysts/2026-07-30/catalyst_events.jsonl` (1500 rows) + `narrative_baskets.jsonl` (4) | today | live re-count this run |
| `data/processed/llm_analysis_packet.md` / `llm_stocks_packet.md` | 09:46 / 10:04 EEST | ~2h / ~1h47m |
| `reports/PAPER_MONITOR_STATUS_LATEST.md` | 10:08 EEST | ~1h43m — **superseded**: predates HOLO/USDT and RE/USDT stopping out at ~08:00 UTC, cross-checked directly against `paper_execution_outcomes` |
| `python -m src.cli active-signals --asset-class crypto` / `stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` / `stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-30` | live query | now — none found |
| `db/crypto_ai_desk.sqlite` `proposed_signals` / `paper_execution_outcomes` / `news_items` (direct query) | live query | now |
| `data/scheduled_runs/2026-07-29_default_schedule/scheduler.log` (most-recently-written folder; cycle numbering runs past midnight) | 10:10 EEST | ~1h41m |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-30_0447.md` | 04:47 EEST | for §4 diff |
| WebSearch: Meta Platforms indictment/legal 2026, Palantir DOJ/SEC investigation 2026, Iran/Strait of Hormuz/oil July 2026 | live | now |

**External web research was available and used this run.**

## 3. Scheduler / Data Freshness

- Scheduler is writing into the `2026-07-29_default_schedule` folder (cycle numbering continues past midnight; that folder's `scheduler.log` and latest `cycle_07_09-30_summary.md` both have mtime 10:10 EEST, ~1h41m old) — well within the 3h defer threshold; **not deferred**.
- Crypto scalp/intraday reports fresh (~2h). Crypto swing report is ~7h15m old — carry-forward bucket, used with a freshness flag, not treated as brand-new.
- Stocks-intraday report fresh (~1h49m) but the US cash session is **closed** until the open — every stocks candidate this cycle is correctly gated `market_closed_intraday_planning_only`.
- Catalyst JSONL re-counted live this run: **1500** unique events today, **491 mapped (32.7%)**, **1009 unmapped (67.3%)** — weak-mapping threshold breached (see §5).
- `detect_untracked_legacy_alerts --since 2026-07-30`: **None** — every legacy crypto alert has a backing proposed_signal.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (10:08 EEST) shows OPEN_ACTIVE=3 (DEXE, HOLO, RE) — this **predates** a live development confirmed by direct DB query: HOLO/USDT (`sig_a572f2096109979d`) and RE/USDT (`sig_b14897bdcd1d8ee1`) both hit `original_stop`, `paper_execution_r=-1.0`, `lifecycle_state=CLOSED`, `exit_at=2026-07-30T08:00:00Z` (~3h51m before this review). Only **DEXE/USDT** (`sig_8e4d318888bf6884`, intraday short, `lifecycle_state=OPEN`, touch_r=0.0) remains genuinely open.
- **Recurring lifecycle-mapping anomaly, still present**: the monitor's `UNKNOWN_INCONSISTENT` bucket (5 items) shows **AAPL, GOOGL, XOM** (stocks/intraday/B) with `unmapped status 'tp2_hit'` and **MSTR, PLTR** (stocks/intraday/C) with `labelled loss but final_r>0 — inconsistent`. The prior review flagged XOM specifically as unresolved for ≥5 consecutive cycles; that particular XOM signal has since closed (`stopped`), but the same unmapped-status pattern has now reappeared on AAPL and GOOGL — this is a **class of bug**, not a one-off (see §14 TODO-3).
- Crypto DB direct query (signals created/closed since prior review at 04:47 EEST): DEXE/USDT intraday short opened 04:48 UTC (still open); HOLO/USDT and RE/USDT swing longs opened earlier today, both stopped -1.0R by 08:00 UTC; COTI/USDT swing long closed -1.0R; ZAMA/USDT intraday short closed -1.0R; BANK/USDT swing short (carried from prior review) closed **flat** (breakeven stop); ACH/USDT swing long (carried from prior review) closed **win +2.0R**; the previously-flagged gating-bypass DEXE/USDT scalp short closed **flat 0R** (`expired_flat`) — no scalp-kill-switch bypass has recurred since (no new `mode=scalp` crypto signals created since 04:47 EEST).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-30 11:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["PAPER_MONITOR_STATUS_LATEST.md (10:08 EEST) predates HOLO/RE stopping out; cross-checked directly against paper_execution_outcomes"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler last write 10:10 EEST (~1h41m)", "scalp/intraday ~2h fresh, swing ~7h15m carry-forward", "stocks-intraday ~1h49m fresh, market closed", "catalyst JSONL live-recounted: 1500 rows, 491 mapped/1009 unmapped", "detect_untracked_legacy_alerts: none"] },
    { "agent": "market_regime", "verdict": "risk_off", "confidence": 0.78,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"],
      "data_missing": ["no fresh RTH stock price action yet — cash session closed"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Internal regime label: bearish trend (risk-off) across scalp/intraday/swing", "BTC downtrend, ETH range, altcoin breadth 23.68% above EMA20 (weak)", "Macro/geopolitics internal risk score 100/100 from 7 risk-off hits", "External: Fed held rates 07-29, 3 FOMC dissents, Chair Warsh hawkish inflation remarks sent stocks tumbling / yields up overnight", "External: US-Iran Strait of Hormuz conflict ongoing, oil elevated, shipping war-risk premiums rising", "Stocks funnel shows 13 short-side candidates scored 82-96 (all currently gated to C, planning-only)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": ["fresh HYPE/perps_dex_narrative contradiction not re-checked this run (last verified in the 04:47 EEST review)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 1500 rows, 491 mapped (32.7%), 1009 unmapped (67.3%) — weak-mapping threshold breached", "4 narrative baskets today; report cites 3 active: ai_narrative (NEAR/RENDER/TAO/FET), perps_dex_narrative (HYPE), momentum_breakout (RE/BANK)", "momentum_breakout's own primaries (RE, BANK) both resolved non-positive today: RE -1.0R stop, BANK flat breakeven", "DEXE, HOLO, COTI open/recent trades all explicitly 'no fresh verified catalyst detected' in the source reports"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "funding_extreme", "data_unavailable"],
      "data_missing": ["OI change unavailable ('n/a') for most symbols this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT (open short): funding -0.001349 (MEXC), -0.00547 (Bybit) — deeply negative on both external venues, meaning shorts are paying to hold — a real squeeze-risk caveat against the open position, not a reason to add", "MUB/USDT, SOXLB/USDT, SNXXB/USDT: 'derivatives unavailable' — confidence reduced on any C-tier idea in these names", "COTI/USDT: funding -0.000786, external Bybit funding near-neutral, crowding 'moderate' per external cross-check"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "entry_late", "stale_before_entry"],
      "data_missing": ["TradingView / manual chart check unavailable this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/USDT: 24h +50.3%, 7d +145.7%, RS vs BTC +51.0% — explicitly flagged 'counter-tape long — reduce size' in the source report, and the swing attempt at this exact RS-leader thesis already closed -1.0R today", "Stocks funnel: 13 short candidates scored 82-96, but all gated market_closed_intraday_planning_only — entering off pre-market/stale levels before RTH confirmation would be chase risk", "DEXE/USDT: already filled at 2.629, current price ~2.567-2.57 per report — inside the zone, not a fresh-entry decision"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.75,
      "reason_codes": ["open_actionable", "no_entry", "needs_review", "closed_flat"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["OPEN actionable = 1 (live DB, corrects the stale 10:08 EEST monitor snapshot's count of 3): DEXE/USDT intraday short, entered 04:48 UTC, touch_r=0.0, expires 2026-07-31T04:48 UTC", "CLOSED since the last monitor snapshot: HOLO/USDT swing long -1.0R (08:00 UTC), RE/USDT swing long -1.0R (08:00 UTC)", "Also closed since prior review: COTI/USDT swing long -1.0R, ZAMA/USDT intraday short -1.0R, BANK/USDT swing short flat (breakeven), ACH/USDT swing long +2.0R win, legacy DEXE/USDT scalp short flat 0R (expired_flat, the prior gating-bypass artifact)", "NEEDS REVIEW = 5 (monitor bucket): AAPL/GOOGL/XOM stocks/intraday/B unmapped status 'tp2_hit'; MSTR/PLTR stocks/intraday/C 'labelled loss but final_r>0'", "detect_untracked_legacy_alerts: none — no alert-without-signal integrity failure this cycle"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["cannot confirm or deny the PLTR sec_doj flag with certainty from a single research pass"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Book's own weekly stats show direction=short at PF 0.33 (n=14, losing) vs direction=long at PF 2.35 (n=66, winning) — tension against today's short-biased regime call; favor selective, well-confirmed shorts only, not broad short exposure", "AAPL, AMZN, COIN, MSTR, MA all report earnings today (2026-07-30) — do_not_chase_warning active on all five", "META: real litigation headline risk confirmed externally (New Mexico $375M child-safety verdict Mar 2026, similar CA verdict, federal trial set Aug 2026) plus same-day earnings miss (-6.6%, tepid Q3 guide) — genuine AVOID for new entries", "PLTR: internal 'sec_doj' flag not corroborated by external search — only found routine, ~9-month-old law-firm shareholder-solicitation boilerplate, structurally identical to the PICS/MVST/PLAB/RBLX boilerplate seen in today's catalyst feed — demote to manual_review rather than confirmed AVOID"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample", "fresh_expired_problem"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto B-tier weekly headline: n=80, winrate 24.7%, PF 1.99, avgR +0.313, totalR +16.9 — healthy despite low winrate", "By mode: intraday PF 4.25 (n=30, strong), swing PF 1.99 (n=30, positive), scalp PF 0.20 avgR -0.25 (n=20, losing) — scalp is correctly disabled via crypto_scalp_disabled kill-switch, no recurrence of the prior gating-bypass bug", "Stocks: A/B headline n=2 anecdotal PF 0.0; C-tier watchlist PF 0.20 (n=185, badly losing) — consistent with C-tier being correctly non-actionable by design", "Today specifically: 3 of 3 no-catalyst counter-tape crypto longs (HOLO, RE, COTI) opened this morning all closed -1.0R — small sample but directionally consistent with the momentum_breakout basket's own documented weak edge"] },
    { "agent": "head_trader", "verdict": "advisory_only",
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of the eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.62,
    "preferred_side": "shorts",
    "best_long_candidate":     { "symbol": "none — watch COTI/USDT", "trigger": "pullback fill into 0.0174-0.0182 with volume confirmation; today's earlier swing long already stopped -1.0R, demand a cleaner retest before re-entry", "reason": "RS-leader vs BTC (+51%) but counter-tape in a bearish regime and no fresh catalyst; reduce size if taken" },
    "best_short_candidate":    { "symbol": "DEXE/USDT", "trigger": "already open (entry 2.629, stop 2.7295, expires 2026-07-31 04:48 UTC) — no new entry, manage existing risk; funding deeply negative on Bybit+MEXC is a squeeze-risk caveat", "reason": "aligned with bearish crypto regime; no fresh catalyst, pure technical breakdown" },
    "best_catalyst_candidate": { "symbol": "SPY / broad-index shorts (SPY, QQQ, IWM, DIA)", "trigger": "wait for RTH open and first 15-30min confirmation before treating pre-market short levels as actionable", "reason": "Fed Chair Warsh's hawkish hold + ongoing Iran/Strait-of-Hormuz oil shock are both externally-verified, live macro catalysts behind the broad 82-96-scored short funnel" },
    "avoid_candidate":         { "symbol": "META", "reason": "same-day earnings miss (-6.6%, tepid Q3 guide) + real (civil, not criminal) child-safety litigation headline risk with a federal trial set for August 2026 — do not chase into the print" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | risk_off | 0.78 | risk_off, shorts_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, entry_late, stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.75 | open_actionable, no_entry, needs_review, closed_flat | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample, fresh_expired_problem | advisory_only |
| head_trader (synthesis) | caution | 0.62 | — | advisory_only |

## 4. What Changed vs Previous Review (04:47 EEST)

- **Resolved**: BANK/USDT swing short closed **flat** (breakeven stop) — was "dormant, favorable drift" in the prior review. ACH/USDT swing long closed **win +2.0R** — was "OPEN, lock armed at +0.5R" in the prior review. XOM's specific unmapped-`tp2_hit` signal from the prior review has closed (`stopped`) — but the same bug pattern reappeared on AAPL and GOOGL this cycle (see §14 TODO-3, it's a class of bug, not fixed). The prior gating-bypass DEXE/USDT scalp short (§14 high-priority item) expired flat 0R with no repeat — no new `mode=scalp` crypto signals have been created since 04:47 EEST, consistent with the kill-switch holding.
- **New**: DEXE/USDT intraday short opened 04:48 UTC (still open). HOLO/USDT and RE/USDT swing longs opened and both closed -1.0R by 08:00 UTC. COTI/USDT swing long opened and closed -1.0R. ZAMA/USDT intraday short closed -1.0R.
- **New macro catalyst**: Fed held rates with 3 dissents; Chair Warsh's hawkish inflation comments (~01:00-02:30 UTC) sent stocks down and yields up — this postdates the prior review and is a fresh, externally-verified driver behind today's broad stocks short funnel.
- **Thesis change**: the prior review's best long-watch (KAITO/USDT) resolved `entry_moved_away` overnight and has dropped out of the active list entirely.
- **Catalyst mapping**: weak in both reviews (60.6% unmapped at 04:47, 67.3% now) — persistent, not a one-off (§14 TODO-5).

## 5. Catalyst Coverage

- Total `catalyst_events` today: **1500**. Mapped (non-null symbol): **491 (32.7%)**. Unmapped: **1009 (67.3%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets today: **4** rows in `narrative_baskets.jsonl`; 3 cited as active in the freshest intraday report: `ai_narrative` (NEAR/RENDER/TAO/FET), `perps_dex_narrative` (HYPE), `momentum_breakout` (RE/BANK — both of today's live attempts on this basket's primaries failed to hold: RE -1.0R, BANK flat).
- Top 3 unmapped headlines (illustrative, not tradable as-is):
  1. "California Water Service Group Reports Strong Second Quarter 2026 Financial Results"
  2. "$250,000,000 USDC minted at USDC Treasury Details" (Telegram whale-alert style post, no resolvable symbol)
  3. "Grayscale parent Digital Currency Group wrote to Senate leaders urging a CLARITY Act floor vote" (policy-level, no single-symbol mapping)

## 6. Market Landscape

Crypto regime is unambiguously risk-off: BTC in a downtrend, ETH range-bound, only 23.7% of tracked alts above EMA20. The desk's own scalp mode remains correctly disabled (net-negative, PF 0.20 over the trailing week) and no scoring gates were bypassed this cycle. Every crypto B-tier idea scored below the actionable threshold this cycle (best was DEXE at 64.4, all others watchlist-only) — nothing forced. On the stocks side the picture is a coiled, high-conviction (score 82-96) broad short funnel across major indices and mega-caps, entirely a function of the overnight Fed/Warsh shock plus the live Iran/Strait-of-Hormuz conflict, but every one of those ideas is correctly held to C-tier/planning-only until the cash session actually opens and confirms.

### Market Mood / Risk Routing
- Crypto mood: **risk-off** (BTC downtrend, ETH range, weak breadth, negative funding on the one open short)
- Stocks mood: **pre-market, directionally risk-off but unconfirmed** (broad short funnel, cash session closed)
- Dominant narrative: Fed Chair Warsh's hawkish inflation stance (post-FOMC hold, 3 dissents) + live US-Iran Strait-of-Hormuz conflict (oil elevated, shipping war-risk premiums up) — both externally verified
- Preferred side now: **shorts** in crypto (selectively — book's own stats show shorts historically underperform, PF 0.33 vs longs PF 2.35, so favor only well-confirmed setups); **catalyst-backed / wait-for-RTH-confirmation** in stocks
- Best long candidate: none clean — watch COTI/USDT for a pullback into 0.0174-0.0182 with volume; today's earlier swing attempt on the same RS-leader thesis already stopped -1.0R
- Best short candidate: DEXE/USDT (already open, manage don't add — funding is deeply negative on both external venues, a real squeeze-risk caveat)
- Best catalyst-backed candidate: SPY / broad-index shorts (SPY, QQQ, IWM, DIA) — pending RTH confirmation
- What to avoid: META (earnings miss + real civil litigation headline risk), and do not chase AAPL/AMZN/COIN/MSTR/MA into today's earnings prints
- What would change the view: a clean RTH open/retest confirming the pre-market short bias in stocks; a BTC/ETH reclaim of local resistance that would invalidate the crypto short bias; any fresh, verified DOJ/SEC filing on PLTR that would upgrade the current unverified flag to a confirmed one

## 7. Candidate Deep Dives

### 1. DEXE/USDT — intraday short, B-tier, **OPEN** (already live, not a new entry)
- Entry 2.62909-2.67428 zone, filled at 2.62909 (04:48 UTC); stop/invalidation 2.72951; TP1 2.50857 / TP2 2.40814 / TP3 2.30771. Touch_r=0.0, no TP touched yet. Expires 2026-07-31 04:48 UTC.
- Has price already reacted? Yes, price is inside the zone, already filled — this is risk management, not a fresh decision.
- Chasing? No — already entered.
- Retest/pullback structure? N/A, position is open.
- Overextended? No (price ~2.567-2.57 vs entry ~2.629, well inside 2 ATR).
- Would entry now be late? N/A.
- Aligned with mood? Yes — short, matches bearish crypto regime.
- Actionable now or pending confirmation? Already actionable/open.
- What would invalidate it? 1h close beyond 2.72951 (stop), or a BTC/ETH regime reclaim.
- Chase risk? No.
- Catalyst confirmation/contradiction? No catalyst either way — pure technical breakdown, `crypto_intraday_catalyst_or_momentum` playbook, known failure mode "no-catalyst intraday in chop is net-negative."
- **Risk note**: funding is deeply negative on both Bybit (-0.00547) and MEXC (-0.001349) — shorts are paying, a real squeeze-risk signal against this exact position. Manage the existing risk; do not add.

### 2. SPY (and the broader index-short cluster: QQQ, IWM, DIA) — stocks, raw tier A, demoted to C
- Score 91 (SPY, short). Demoted `market_closed_intraday_planning_only` — the US cash session is not open yet at 11:30 EEST.
- Has price already reacted? Yes, overnight — Fed/Warsh hawkish hold sent stocks down and yields up; this is baked into the pre-market read.
- Chasing? Would be, if entered off stale pre-market levels without RTH confirmation.
- Retest/pullback structure? Not yet establishable — need the open.
- Overextended? Cannot assess pre-open with local OHLCV alone (no live chart tool this run).
- Would entry now be late? Entry now is not possible — market closed.
- Aligned with mood? Yes — broad short cluster matches the risk-off macro read.
- Actionable now or pending confirmation? **Pending RTH confirmation only.**
- What would invalidate it? A gap-up open that reclaims pre-market resistance, or the Iran conflict de-escalating and oil pulling back sharply.
- Chase risk? High if entered pre-confirmation.
- Catalyst confirmation? Yes — externally verified: Fed hold + Warsh hawkish tone (3 dissents), plus live Iran/Strait-of-Hormuz escalation (oil elevated, war-risk shipping premiums rising).

### 3. META — stocks, raw tier A (score 94), demoted to C — **AVOID**
- Demoted for `legal_headline_risk: indictment` + `stale_post_earnings_setup` (Q2 2026 earnings printed 05:03 UTC today) + `market_closed_intraday_planning_only`.
- External verification: **no criminal indictment found.** What is real and current: a New Mexico jury verdict (March 2026, $375M) and a California jury verdict (March 2026) against Meta for child-safety/addiction design failures, plus a federal trial set for **August 2026** in the Northern District of California on the same theme — genuine, material, ongoing legal exposure, just civil rather than criminal (the internal "indictment" label is inaccurate — see §14 TODO-2).
- Same-day earnings: net income -14%, stock -6.6% on the print, tepid Q3 AI-cost guidance from Zuckerberg — pre-earnings technical levels are stale by design.
- Verdict: **AVOID / manual review required** for any new META position today — the combination of a live earnings reaction and a real ongoing litigation overhang (not the specific "indictment" the system claims) is real risk, not a chase opportunity either direction.

### 4. PLTR — stocks, raw tier A (score 88), demoted to C — **manual review, flag likely false positive**
- Demoted for `legal_headline_risk: sec_doj` + `market_closed_intraday_planning_only`.
- External verification: **no confirmed active 2026 DOJ or SEC investigation into Palantir found.** What surfaced: routine law-firm shareholder-solicitation press releases dated ~October 2025 (Frank R. Cruz, Glancy Prongay & Murray — boilerplate "investigation announced, shareholders who lost money should contact us" releases that are issued for hundreds of volatile stocks and are not evidence of a real government inquiry), plus unrelated news about Palantir's IRS contracts facing public-records scrutiny from an advocacy group (about government use of the tool, not a PLTR-targeted investigation).
- The same boilerplate template ("Shareholders Who Lost Money Have Opportunity to Lead Securities Fraud Lawsuit") appears verbatim in today's catalyst feed for **PicS N.V., Microvast, Photronics, and Roblox** — strong circumstantial evidence the internal `sec_doj` / `legal_headline_risk` classifier may be pattern-matching this generic solicitation language rather than a real, symbol-specific investigation (see §14 TODO-1, high priority).
- Verdict: **manual review, not a confirmed AVOID** — the underlying score (88, short) and setup would otherwise be actionable-tier once RTH confirms; treat the legal flag as unverified pending a human look at the source, don't clear it automatically either.

### 5. COTI/USDT — crypto swing/intraday, C-tier watchlist — best long-watch, not actionable yet
- Current price 0.0186 (intraday scan), 24h +50.3%, 7d +145.7%, RS vs BTC +51.0%, score 54.3 (low confidence, below active threshold).
- Has price already reacted? Yes — this is a large move already in progress.
- Chasing? Yes if entered at market; the report explicitly labels this a "counter-tape long — reduce size" against the bearish regime.
- Retest/pullback structure? Conditional pullback zone 0.0174-0.0182 defined, not yet filled.
- Overextended? Volume ratio only 0.58x average — the move is not backed by strong current volume, a real red flag for a breakout long.
- Would entry now be late? Yes, at current price.
- Aligned with mood? No — it's a long in a short-preferred regime; only interesting as a relative-strength leader.
- Actionable now or pending confirmation? Pending a clean pullback fill with volume.
- What would invalidate it? 1h close beyond 0.0165.
- Chase risk? High at current price.
- Catalyst confirmation? None found — no fresh verified catalyst despite the large move.
- **Important context**: a swing-long attempt on this exact symbol already closed **-1.0R today** (per `paper_execution_outcomes`) — this is not a fresh, clean idea, it's a repeat of a setup that just failed. Demand a materially better entry/confirmation before treating it as anything but a watch.

## 8. Best Candidates Ranked

1. **DEXE/USDT short** — already open, manage risk, do not add (squeeze-risk caveat).
2. **SPY / broad-index shorts** — best catalyst-backed idea, pending RTH confirmation only.
3. **COTI/USDT long** — best long-watch, pullback-only, reduced size, already failed once today.
4. **PLTR** — potentially actionable (score 88, short) once the legal flag is manually cleared or confirmed; do not treat as tradable until then.
5. **META** — explicitly not ranked as tradable; avoid.

## 9. Avoid / No Trade (this decision window only)

- **META**: real earnings-day volatility + real (civil) litigation overhang. Avoid new entries either direction until both settle.
- **AAPL, AMZN, COIN, MSTR, MA**: earnings today — `do_not_chase_warning` active on all five, avoid chasing into the print.
- **Crypto scalp mode**: correctly disabled desk-wide (kill-switch), not a per-symbol avoid.
- This is a decision-window call only — scanning, tracking, and monitors continue in every mood; nothing here is a stop-the-system instruction.

## 10. Main Risks

- Live geopolitical risk: the US-Iran Strait-of-Hormuz conflict is ongoing and could escalate further intraday, with direct oil/macro spillover into both crypto and equities.
- Fed/rates risk: Chair Warsh's hawkish tone is fresh (overnight) and could extend if he speaks again or if incoming data reinforces the inflation narrative.
- Squeeze risk on the one open crypto position (DEXE short) given deeply negative funding on both external venues.
- Data-quality risk: the recurring `UNKNOWN_INCONSISTENT` lifecycle-mapping bug (unmapped `tp2_hit`, "labelled loss but final_r>0") means a small number of stocks signals cannot currently be trusted at face value in the monitor view — always cross-check against `paper_execution_outcomes` directly, as done in this review.
- Legal-flag reliability risk: at least one of the two legal_headline_risk flags reviewed this cycle (PLTR) could not be corroborated externally — treat these flags as a starting point for manual review, not as settled fact, until §14 TODO-1 is investigated.

## 11. Action Plan — next 4 hours

- Hold DEXE/USDT short as-is; do not add given the funding-driven squeeze-risk caveat; manage to stop 2.72951 or TP ladder.
- Watch for a clean COTI/USDT pullback into 0.0174-0.0182 with volume confirmation before considering any long; size down given today's earlier -1.0R stop on the same thesis.
- Do not enter any stocks position pre-open; wait for RTH confirmation on the SPY/QQQ/IWM/DIA short cluster before treating it as actionable.
- Do not chase AAPL, AMZN, COIN, MSTR, MA into today's earnings prints; do not initiate META positions given the live litigation + earnings overhang.
- Flag PLTR for a human look at the `sec_doj` source data before either clearing or confirming the AVOID.
- Continue monitoring the Iran/Strait-of-Hormuz situation and Fed commentary for further escalation into the US open.

## 12. Final Verdict per Mode

- **Crypto scalp**: disabled (kill-switch), no change — correctly net-negative and off.
- **Crypto intraday**: 1 open position (DEXE short), manage only; no new entries scored high enough this cycle.
- **Crypto swing**: watch-only; today's 3 no-catalyst counter-tape attempts (HOLO, RE, COTI) all failed -1R — demand catalyst or RS+volume confirmation before the next attempt.
- **Stocks intraday**: planning-only until RTH confirms; broad short bias noted but not actionable pre-open.
- **Stocks swing/invest**: deprecated/removed frameworks, no active signals this run (see [[project_crypto_ai_desk_stocks_position_framework]]).

## 13. Sources

- [Landmark Verdicts Against Meta and YouTube Signal New Era of Social Media Platform Liability (Crowell & Moring)](https://www.crowell.com/en/insights/client-alerts/landmark-verdicts-against-meta-and-youtube-signal-new-era-of-social-media-platform-liability)
- [New Mexico Department of Justice Wins Landmark Verdict Against Meta (NM DOJ)](https://nmdoj.gov/press-release/new-mexico-department-of-justice-wins-landmark-verdict-against-meta/)
- [Four states seeking $1.4 trillion in penalties in child social media addiction trial, Meta says (Fox Business)](https://www.foxbusiness.com/technology/four-states-seeking-1-4-trillion-penalties-child-social-media-addiction-trial-meta-says)
- [Securities Fraud Investigation Into Palantir Technologies Inc. (PLTR) Announced (Businesswire, Oct 2025 — law-firm solicitation)](https://www.businesswire.com/news/home/20251007500265/en/Securities-Fraud-Investigation-Into-Palantir-Technologies-Inc.-PLTR-Announced-Shareholders-Who-Lost-Money-Urged-To-Contact-The-Law-Offices-of-Frank-R.-Cruz)
- [Palantir is reportedly helping the IRS investigate financial crimes (TechCrunch, Apr 2026)](https://techcrunch.com/2026/04/24/palantir-is-reportedly-helping-the-irs-investigate-financial-crimes/)
- [Oil surges as US strikes Iran, reversing return to pre-war prices (Al Jazeera)](https://www.aljazeera.com/news/2026/7/8/oil-prices-surge-as-us-strikes-iran-reversing-fall-to-pre-war-levels)
- [U.S. targets military assets in latest round of strikes against Iran (CNBC)](https://www.cnbc.com/2026/07/14/us-iran-hormuz-strikes-oil-toll.html)
- Internal: `news_items` rows dated 2026-07-30 00:22-02:30 UTC (Finnhub company-news, CNBC Markets) — "Fed Holds Rates Steady As 3 FOMC Members Dissent", "2 Words From Fed Chair Kevin Warsh Sent the Stock Market Tumbling", "Stocks Tank, Long-Term Treasury Yields Jump After Warsh Starts Talking"
- Internal: `news_items` row dated 2026-07-30 07:13 UTC (Finnhub company-news) — "Meta net income falls 14% to $15.8bn as costs rise in Q2 2026"

## 14. Fix Requests / TODO

### TODO-1: PLTR `legal_headline_risk: sec_doj` flag looks like a false positive from law-firm solicitation boilerplate
- **issue:** The stocks report demotes PLTR from A→C citing "active legal/headline risk (sec_doj)". External WebSearch found no confirmed 2026 DOJ/SEC investigation into Palantir — only ~9-month-old (Oct 2025) shareholder-solicitation press releases from securities-fraud law firms, which are boilerplate issued for hundreds of stocks and are not evidence of an actual government inquiry.
- **evidence:** WebSearch "Palantir Technologies DOJ SEC investigation 2026" (see §13); today's `catalyst_events.jsonl` contains structurally identical boilerplate ("Shareholders Who Lost Money Have Opportunity to Lead Securities Fraud Lawsuit") for PicS N.V. (PICS), Microvast (MVST), Photronics (PLAB), and Roblox (RBLX) — same law-firm-press-release pattern.
- **suggested manual fix:** Audit the `legal_headline_risk` / `sec_doj` classifier's source data for PLTR; consider excluding or down-weighting generic shareholder-solicitation press-release boilerplate (identifiable by template phrases like "Shareholders Who Lost Money Have Opportunity to Lead") from the legal-risk detector, since it appears to fire for essentially any volatile stock rather than genuine investigations.
- **priority:** high
- **first observed:** 2026-07-30 11:45 EEST

### TODO-2: META `legal_headline_risk` mislabeled as "indictment"
- **issue:** The stocks report labels META's legal risk category as "indictment". External verification shows META's actual current legal exposure is civil litigation (New Mexico and California jury verdicts, March 2026; federal child-addiction-design trial set for August 2026), not a criminal indictment.
- **evidence:** WebSearch "Meta Platforms indictment legal 2026" (see §13) — no indictment found; multiple civil verdicts/trials found instead.
- **suggested manual fix:** Correct the legal-risk taxonomy/label for META from "indictment" to something like "civil_litigation" or "child_safety_verdict" so operators aren't misled about the nature of the risk.
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST

### TODO-3: Recurring `UNKNOWN_INCONSISTENT` lifecycle mapping — unmapped status `'tp2_hit'`
- **issue:** `PAPER_MONITOR_STATUS_LATEST.md` shows AAPL and GOOGL (stocks/intraday/B) with "STATUS NEEDS REVIEW — inconsistent lifecycle fields · unmapped status 'tp2_hit'". This is the same bug class the 04:47 EEST review flagged on XOM for ≥5 consecutive cycles (that specific XOM signal has since closed, but the underlying mapping gap has now surfaced on different symbols) — a persistent regression, not a one-off.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` lines showing AAPL/GOOGL/XOM "unmapped status 'tp2_hit'"; prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-30_0447.md` §14 flagged the same pattern on XOM.
- **suggested manual fix:** Find and fix the lifecycle-state mapping for legacy-touch signals with raw status `tp2_hit` in the stocks/intraday/B path so it resolves to a proper CLOSED_WIN/OPEN state instead of falling through to UNKNOWN_INCONSISTENT.
- **priority:** high
- **first observed:** 2026-07-29 (per prior review), reappeared 2026-07-30 11:45 EEST on different symbols

### TODO-4: Separate lifecycle inconsistency — "labelled loss but final_r>0"
- **issue:** MSTR and PLTR (stocks/intraday/C) show "labelled loss but final_r>0 — inconsistent" in the monitor status — a different inconsistency pattern from TODO-3, also unresolved.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md`, MSTR and PLTR lines.
- **suggested manual fix:** Audit the loss-labelling logic for legacy-touch signals where `final_r` is computed as positive but the status field still says "loss" — likely the same underlying lifecycle/status-mapping component as TODO-3.
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST

### TODO-5: Catalyst mapping weak again this run (67.3% unmapped)
- **issue:** 1009 of 1500 catalyst events today have no resolved symbol — above the 50% weak-mapping threshold, consistent with a recurring pattern noted in project memory ([[project_crypto_ai_desk_catalyst_linkage]]).
- **evidence:** live count of `data/catalysts/2026-07-30/catalyst_events.jsonl` this run: 491 mapped / 1009 unmapped.
- **suggested manual fix:** Continue widening/improving the symbol resolver in the catalyst layer per the deferred work noted in project memory.
- **priority:** low (known, deferred, not a new regression)
- **first observed:** recurring; re-confirmed 2026-07-30 11:45 EEST
