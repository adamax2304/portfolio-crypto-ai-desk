# Opus Enriched Review — LATE-SESSION RISK REVIEW — Auto Cycle 21:39 EEST

## 1. Executive Summary

Slot: **late-session risk review** (21:30 EEST fire, current wall-clock 21:39 EEST). Advisory only — no auto-trade, no live execution, no scoring/threshold changes made or recommended. Crypto stays technically bullish (BTC/ETH uptrend, 83-85% breadth) but the macro-geopolitical layer is still pinned at 100/100 risk-off (Iran secondary sanctions, CENTCOM blockade actions, Fed-communication/bond-yield stress) — still **mixed**, not clean risk-on, unchanged in character from the 18:40 review. Zero A-tier crypto setups this cycle (intraday and swing both top out at B-tier, no fresh catalyst on either). Stocks intraday remains **fully guard-gated** — every raw A/B candidate (ABNB, BKNG, TSLA, MSFT, MSTR, etc.) demoted to C by the rolling paper-R drawdown guard; zero A/B actionable stocks setups again this cycle. The **XPL/USDT bias-tag contradiction has escalated**: the open swing long has now actually **triggered/filled** (was still `waiting_for_entry` at 18:40) while the desk's own weakest-symbols list still tags XPL bias=short — this needs an operator look tonight, not just a watch note. Catalyst mapping is weak this run (76.3% unmapped) — treat the catalyst layer as context, not proof of "no catalyst." 20 untracked legacy crypto Telegram alerts today (ongoing known leak).

## 2. Data Used

- Reports: `2026-08-24_18-19_scalp_report.md` (21:19 EEST gen, freshest), `2026-08-24_18-30_intraday_report.md` (21:30 EEST gen, freshest), `2026-08-24_15-35_swing_report.md` (18:34 EEST gen, ~3h old, carry-forward), `2026-08-24_14-55_stocks_intraday_report.md` (17:55 EEST gen, freshest available — no newer stocks scan post-close-approach)
- `data/catalysts/2026-08-24/catalyst_events.jsonl` (2500 events), `narrative_baskets.jsonl` (2 baskets)
- `data/processed/llm_analysis_packet.md` (21:33 EEST gen, fresh)
- `python -m src.cli active-signals --asset-class crypto` / `--asset-class stocks`
- `python -m src.cli signal-stats --asset-class crypto` / `--asset-class stocks` (week window)
- `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-24`
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_1840.md` (18:40 EEST, US open reaction review)
- **External web research unavailable this run** (WebSearch/WebFetch not invoked — no candidate this cycle required external verification beyond what internal `news_items`/catalyst records already covered; BLK legal-risk status carried forward from the 18:40 review's verified WebSearch, not re-verified tonight)

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-08-24 21:44 EEST (< 5 min old) — **fresh**, not deferred. Scheduler is mid-cycle (paper entry-mode classify running at review time), no errors in the last 30 log lines.
- Scalp report: ~20 min old (fresh). Intraday report: ~9 min old (fresh). Swing report: ~3h old — **carry-forward** band (4-12h rule), still usable, no new swing scan this cycle. Stocks intraday: ~3h44min old — also carry-forward; no fresher post-close-approach stocks scan has landed yet.
- Crypto LLM packet: 21:33 EEST, fresh.
- Stocks swing/invest (old, deprecated) reports remain from 2026-07-02 — expected, per [[project_crypto_ai_desk_stocks_position_framework]] these are permanently deprecated/removed, not a freshness issue.
- Monitor/paper status: scheduler's `paper execution accounting refresh`, `paper structural TP refresh`, and `paper structural stop plan` all completed exit=0 in this cycle (21:36-21:44 EEST) — paper book accounting is current.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-08-24 21:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 21:44 EEST, mid-cycle no errors", "scalp/intraday reports <25min old", "swing/stocks-intraday reports ~3-4h old, carry-forward band"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 83.3-85.4% breadth, macro risk 100/100 unchanged", "stocks: guard fully engaged since post-open, no new regime read this cycle (report carry-forward)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["2500 catalyst events, 1907 unmapped (76.3%)", "PROM/AERO B-tier ideas both explicitly no-catalyst momentum", "rwa_narrative and perps_dex_narrative baskets still the only active baskets"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["bybit ohlcv 5 failed fetches this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH/BNB/SOL: price up + OI up, funding ~1e-4 (neutral, not extreme)", "TAO: price up + OI down = short covering, weaker continuation quality"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM current 3.729 vs entry zone 3.570-3.680 (already through the zone)", "AERO current 0.5295 vs entry zone 0.5179-0.5259 (already through the zone)", "both no-catalyst, low-risk-gate B-tier only"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: ~34 triggered/tp1/tp2 open, ~13 waiting_for_entry across 50 rows sampled", "stocks: 14 today's-cycle rows (tp1_hit/triggered/waiting) expiring 2026-08-25T14:54-15:00, plus older resolved rows", "20 untracked legacy crypto alerts today (up from 17 at 18:40)"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.7,
      "reason_codes": ["reduce_risk", "legal_risk", "correlation_cluster"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["XPL/USDT long has now TRIGGERED while bias-tag still says short — escalation from waiting_for_entry at 18:40", "BLK class-action investigation still open (carried forward, not re-verified tonight)", "stocks headline A/B week: winrate 5.3%, PF 1.25, totalR +2.5 (still weak, sample small)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto intraday PF2.51/+53R, swing PF1.92/+20.2R this week (still the strongest crypto lanes)", "crypto scalp PF0.10/-4.5R (known weak lane, unchanged)", "stocks B-tier PF0.56/winrate 3%, C-tier PF0.46/winrate 11% this week — both below 0.8 PF threshold per system's own observation flags"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": ["watch_only", "wait_for_trigger", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "NEAR/USDT", "trigger": "already open (swing leg, triggered), catalyst-backed, intraday leg already closed at TP2", "reason": "quantum-resistant pilot catalyst still the freshest verified name on the desk; swing leg riding a realized win" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "1h close below current swing/intraday structure low, ideally with volume", "reason": "still the weakest symbol in the intraday Lower-Cap leaders list (24h -13.19%, RS/BTC -15.42%), no conflicting open position" },
    "best_catalyst_candidate": { "symbol": "NEAR/USDT", "trigger": "already open", "reason": "same as best-long — only clean catalyst-confirmed name carrying a realized partial win tonight" },
    "avoid_candidate":         { "symbol": "XPL/USDT", "reason": "open swing long has now TRIGGERED (filled) while the desk's own weakest-symbols data still tags it bias=short — do not add to this position or trust it as clean until the contradiction is manually resolved" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.75 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.60 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | manual_review | 0.70 | reduce_risk, legal_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | 0.60 | watch_only, wait_for_trigger, manual_review | advisory_only |

## 4. What Changed vs Previous Review (18:40 EEST — US open reaction review)

- **NEAR/USDT intraday leg CLOSED WIN**: the intraday NEAR position that was "already open" at 18:40 has since hit TP2 and its window has expired (`sig_7b65f164ba9c6c9d`, tp2_hit, expired 2026-08-24T14:40:54 UTC). The swing leg (`sig_844ebda1635aaf1d`) remains triggered/open — the catalyst thesis is intact and partially realized.
- **XPL/USDT contradiction escalated**: at 18:40 the open swing long was still `waiting_for_entry` (not yet filled), so the bias-tag mismatch was a watch item. As of this cycle the signal shows status `triggered` — **the long has actually filled** while the swing report's weakest-symbols list (same data source, carried forward, XPL/USDT bias=short, 24h -9.33%, RS/BTC -12.76%) still contradicts it. This is now a live position with an unresolved bias conflict, not just a pending one — escalating from watch to manual_review (§9, §14).
- **Untracked alert count grew again**: 20 today (vs 17 at 18:40) — confirms the leak is continuous through the session, not a one-off burst.
- **Stocks intraday guard unchanged**: still fully engaged (no fresher stocks scan has landed since 17:55 EEST; the 14:00:02-UTC-vintage ABNB/MA/V A/B signals remain open and unfilled, same guard-vs-open tension noted at 18:40).
- **BLK avoid unchanged**: no new information this cycle; carried forward from the 18:40 verified finding, not re-checked.
- **TUT/USDT short-watch unchanged**: still the weakest name, still no conflicting position, still unconfirmed (no 1h close below structure yet).
- **No new A-tier anywhere** (crypto intraday, crypto swing, stocks intraday) — consistent with 18:40, no change.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **2500**; mapped (symbol present): **593**; unmapped: **1907** (**76.3% unmapped**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets: **2** active — `rwa_narrative` (ONDO/XLM primary, freshness <1h) and `perps_dex_narrative` (HYPE primary, freshness <6h) — unchanged from 18:40.
- Top unmapped headlines (symbol resolution failed):
  1. "Bybit now supports $GROVE deposits and withdrawals on Mantle Network..."
  2. "NOMURA INTERNATIONAL FUNDING SECURED AN 'A-' CREDIT RATING FROM FITCH RATINGS..."
  3. "Pulnovo Medical Announces First Two U.S. Patients Enrolled in PULSE-LHD IDE Clinical Trial..."

## 6. Market Landscape

**Crypto:** BTC/ETH both in uptrend, 83.3% of tracked symbols above EMA20 / 85.4% above EMA50, desk regime label "bullish trend (risk-on)." Macro-geopolitical risk score is independently pinned at **100/100** — Iran secondary-sanctions escalation continuing (Treasury sanctions on ~60 Iran-linked entities announced today), CENTCOM confirms active blockade-enforcement boarding actions as of today, oil pulling back on the sanctions news. This is the same two-layer tension flagged at 18:40 (technically bullish, macro-fragile) — unchanged in character, not resolved, not worsened.

**Stocks:** No fresher post-17:55-EEST stocks scan has landed this cycle, so tonight's read carries forward the post-open "chop" regime from 18:40: QQQ 5d downtrend, SPY/IWM/DIA range-bound, thin breadth. The rolling paper-R drawdown guard remains fully engaged on both long and short intraday sides — every raw A/B candidate this session (ABNB, BKNG, COP, UBER, TSLA, MSTR, MSFT, BLK, DIS, KO, GOOGL, SOFI, MRVL, NOW, BA) demoted to C. No basis to call this "improved" or "worsened" tonight — treat as unresolved/unconfirmed pending the next stocks scan.

### Market Mood / Risk Routing
- Crypto mood: **mixed** (technically risk-on, macro risk-off — size conservatively, prefer catalyst-confirmed or already-open positions over fresh no-catalyst chases)
- Stocks mood: **chop** (carried forward from post-open read; guard-driven caution remains appropriate, cash-hours winding down toward the close)
- Dominant narrative: crypto — perps_dex (HYPE) and rwa (ONDO/XLM) baskets still freshest; PROM/AERO momentum names are both no-catalyst and already extended past their planned pullback entry zones. Stocks — no dominant theme surfaced this cycle (carried-forward data).
- Preferred side now: **crypto: hold existing catalyst-backed/open positions (NEAR/USDT); avoid chasing PROM/AERO at spot; watch TUT/USDT for a confirmed short trigger. Stocks: no new entries either side — guard still blocking, and it is late in the session for fresh RTH entries regardless.**
- Best long candidate: **NEAR/USDT** (crypto, catalyst-backed, swing leg open, intraday leg already closed win)
- Best short candidate: **TUT/USDT** watch (crypto, weakest symbol, no conflicting position) — trigger: 1h close below current structure/swing low
- Best catalyst-backed candidate: **NEAR/USDT** (same as best long)
- What to avoid: **XPL/USDT** (open long filled, bias-tag says short — unresolved, see §9); **BLK** (legal risk, carried forward); chasing PROM/AERO at spot (both already through their pullback entry zones); new stocks entries into any guard-demoted name
- What would change the view: the XPL bias contradiction being manually resolved one way or the other; the stocks drawdown guard clearing on the next scan; de-escalation on the Iran sanctions/blockade headlines

## 7. Candidate Deep Dives

### 7.1 NEAR/USDT — LONG, catalyst-backed (crypto, swing open + intraday closed win)
- Catalyst: banks/regulators joining a quantum-resistant crypto transfer pilot on NEAR testnet — unchanged, still the freshest verified catalyst on the desk (carried forward from 18:40, no new confirmation or contradiction tonight).
- Price reaction: intraday leg already captured (tp2_hit, window expired) — a realized partial win, not a chase. Swing leg remains triggered/open.
- Actionable: yes, already open on the swing leg. Aligned with mood (catalyst-confirmed inside a bullish-breadth market, macro tension notwithstanding).
- Is this a chase-risk setup? No — already filled, holding not entering.
- Would invalidate: 1h close below swing invalidation (~1.97 per active-signals row), or a reversal/contradiction of the quantum-pilot story.

### 7.2 XPL/USDT — AVOID / MANUAL REVIEW, contradiction escalated (crypto, swing, B-tier, now TRIGGERED)
- Desk holds an open B-tier swing **long**, entry zone 0.104536-0.106512, invalidation 0.102120, score 69.2 — status has moved from `waiting_for_entry` (18:40) to **`triggered`** (this cycle), meaning the position has filled.
- The swing report's weakest-symbols list (same 15:35/18:34-EEST report, carried forward, no fresher swing scan available) still tags XPL/USDT **bias=short**: 24h -9.33%, RS vs BTC -12.76%.
- This is the same recurring pattern documented in [[project_crypto_ai_desk_bias_tag_contradiction]] (escalated to HIGH priority 2026-08-08) and the PUMP/USDT case resolved earlier in today's session.
- Actionable: **no new exposure** — the existing filled long should get an operator bias check tonight given the fill has already happened; this is no longer a "don't let it convert" watch item, it converted.
- Would invalidate the avoid: a fresher swing scan showing XPL back on the RS-leader/strong side, or a manual confirmation that the weakest-symbols tag is stale relative to the entry.

### 7.3 ABNB / MA / V — stocks, guard-vs-open contradiction (A/A/B-tier, still `waiting_for_entry`)
- Unchanged from 18:40: registered at the pre-open scan (14:00:02 UTC) with strong scores (ABNB 95.5, MA 84.3, V 78.7), still sitting unfilled.
- No fresher stocks scan has landed to confirm whether the guard is still demoting ABNB-class candidates tonight — treating the 18:40 guard-engaged read as still authoritative (carry-forward), not re-verified this cycle.
- Actionable: **manual review** — if these fill, treat with the same skepticism the guard was applying to fresh candidates at 17:55 EEST, not as pre-cleared setups.

### 7.4 PROM/USDT & AERO/USDT — WATCH ONLY, chase risk (crypto intraday, B-tier, no catalyst)
- Both are the desk's top B-tier intraday ideas this cycle (score 66.1 each), explicitly flagged no fresh verified catalyst, playbook `crypto_intraday_catalyst_or_momentum` (no-catalyst cut: 14d WR 23% / PF 0.70 / -3R — a known weak lane).
- PROM current price 3.729 is already above its planned entry zone (3.570-3.680); AERO current price 0.5295 is already above its zone (0.5179-0.5259) — both are through their pullback zones without a confirmed retest.
- Actionable: **no** — do not chase at spot; only actionable if price comes back into the stated entry zone.
- Would invalidate: a clean pullback into zone with volume support would make either tradeable at low size; continued extension without a retest keeps both as watch-only.

### 7.5 TUT/USDT — SHORT-WATCH (crypto, not currently an active signal)
- Still the weakest name in the intraday Lower-Cap/Expanded Universe leaders list: 24h -13.19%, RS vs BTC -15.42%, tags weak_vs_market.
- No existing open position on this symbol — no bias-tag conflict (unlike XPL).
- Actionable: **only on confirmation** — 1h close below current structure low, ideally with volume.
- Would invalidate: a reclaim of the recent range, or a broad BTC/ETH breakdown that turns this into a beta short rather than a clean RS short.

## 8. Best Candidates Ranked

1. **NEAR/USDT** — LONG, catalyst-backed, swing leg open/actionable, intraday leg already a realized win. Best overall candidate this cycle (unchanged from 18:40).
2. **TUT/USDT** — SHORT-WATCH, cleanest relative-weakness idea with no conflicting position; trigger: 1h close below structure low.
3. **XPL/USDT** — AVOID / MANUAL REVIEW (escalated) — open long has filled while bias-tag still says short; needs operator resolution tonight.
4. **ABNB / MA / V** — stocks, NEEDS REVIEW (guard-vs-open contradiction, carried forward, unverified this cycle).
5. **BLK** — AVOID (legal risk, carried forward from 18:40, not re-verified tonight).

## 9. Avoid / No Trade

*(This decision window only — never a command to stop scanning, tracking, or the scheduler.)*

- **XPL/USDT** — open long has triggered/filled while the desk's own bias data says short; do not add to the position, and flag for manual bias resolution (§7.2, §14).
- **BLK** — carried-forward securities class-action finding; do not take new long exposure.
- **PROM/USDT and AERO/USDT at spot** — both already through their planned pullback entry zones; only actionable on a confirmed retest.
- **New stocks A/B entries generally** — drawdown guard was fully engaged as of the last confirmed scan (17:55 EEST); no fresher scan to say it has cleared.
- **Fresh crypto scalp signals** — PF 0.10 / -4.5R this week, known weak lane, research-grade only.

## 10. Main Risks

- **XPL/USDT bias contradiction now live in a filled position** — this is the most actionable risk item tonight; unlike the PUMP case (which resolved itself as the market moved), this position is open and the conflict is unresolved.
- **Crypto stats methodology caveat**: touch-based `final_r` accounting (highest-TP-touched) historically overstates realized PnL vs. realistic execution — per [[project_crypto_ai_desk_touch_based_pnl]], treat the week's crypto headline totals as directionally positive, not literal achievable P&L.
- **Stocks book-wide weakness**: B-tier PF 0.56 (winrate 3%) and C-tier PF 0.46 (winrate 11%) this week, both below the system's own 0.8 PF observation threshold — consistent with the drawdown guard's continued engagement.
- **Untracked alert leakage continuing to grow**: 20 crypto Telegram alerts today (up from 17 at 18:40, 9 earlier) with no backing `proposed_signal` — those outcomes will never be counted in PF/winrate stats. Matches [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] (raised to HIGH 2026-07-17), still unresolved.
- **Stale-relative-to-carry-forward stocks read**: no stocks scan has landed since 17:55 EEST (~3h44min); tonight's stocks verdicts lean on that carried-forward guard state rather than a fresh confirmation.
- **Macro risk unresolved**: Iran sanctions/blockade enforcement is an active, developing situation — the 100/100 macro risk score is not a one-off headline, it is describing an ongoing event.

## 11. Action Plan — next 4 hours

1. Hold NEAR/USDT swing long; the intraday leg is already closed as a win — no size addition on the catalyst alone.
2. **Flag XPL/USDT for operator bias review tonight** — the long has filled while bias data says short; do not add, and get a human read on whether the position should be trimmed or the bias tag is stale.
3. Watch TUT/USDT for a confirmed 1h close below structure before treating it as a short idea — still watch-only, not a system signal.
4. Do not chase PROM/USDT or AERO/USDT at spot — wait for a retest into their stated pullback zones.
5. Do not treat ABNB/MA/V waiting stocks signals as pre-cleared if they fill overnight/pre-market — guard state as of 17:55 EEST was fully engaged.
6. Avoid BLK entirely pending fresh resolution of the securities investigation (carried forward, not re-checked tonight).
7. Continue scanning/tracking as normal in all modes — no pause, no stop, regardless of the caution/manual_review verdicts above.

## 12. Final Verdict per Mode

- **Crypto scalp:** caution — PF~0.10 this week, unchanged low-confidence lane; research-grade only.
- **Crypto intraday:** watch/actionable — PF~2.51 this week, strongest crypto lane; no fresh A-tier or catalyst-backed idea tonight (PROM/AERO both no-catalyst and extended past entry).
- **Crypto swing:** watch/actionable, with one manual-review item — PF~1.92 this week; NEAR/USDT remains the cleanest open idea; XPL/USDT needs operator attention now that it has filled with an unresolved bias conflict.
- **Stocks intraday:** manual_review — drawdown guard state carried forward as fully engaged from the last confirmed scan (17:55 EEST); zero fresh A/B actionable confirmed tonight.
- **Stocks swing/invest (old):** not applicable — deprecated/removed, never actionable.
- **Stocks swing growth-breakout (new):** shadow-only research; no change to that status this run (latest shadow scan 15:38 EEST, 5 open candidates: JPM, BAC, BLK, MRK, LLY — research only, not sized).

## 13. Sources

- Internal only this cycle — no external web research was required/performed (§2). BLK legal-risk citations carried forward from the 18:40 review's WebSearch verification (Rosen Law Firm PR Newswire/GlobeNewswire releases, 2026-08-24 and 2026-08-10 recurrences) — see `OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_1840.md` §13 for the original source list.
- `data/catalysts/2026-08-24/catalyst_events.jsonl`, `narrative_baskets.jsonl`
- `data/reports/scalp/2026-08-24_18-19_scalp_report.md`, `data/reports/intraday/2026-08-24_18-30_intraday_report.md`, `data/reports/swing/2026-08-24_15-35_swing_report.md`, `data/reports/stocks/intraday/2026-08-24_14-55_stocks_intraday_report.md`
- `data/scheduled_runs/2026-08-24_default_schedule/scheduler.log`
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_1840.md`

## 14. Fix Requests / TODO

### TODO-untracked-alerts-growth (continuing)
- **issue:** 20 untracked legacy crypto Telegram alerts today (no backing `proposed_signal`), up from 17 at 18:40 EEST and 9 earlier in the session — the leak is continuous throughout the day, not a one-off. Matches previously-escalated bug [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] (confirmed on ALLO/USDT + BANK/USDT, raised to HIGH priority 2026-07-17).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-24` → 20 rows, all `NO (no proposed_signal)`, spanning 10:11-18:40 UTC today (symbols: PENGU, FF, INJ, TAO, PENDLE, PROM, ONG across scalp/swing modes).
- **suggested manual fix:** investigate the watchlist-alert-to-proposed-signal linkage per the existing TODO-3 write-up; this run adds no new diagnosis, only confirms the leak rate is steady/growing.
- **priority:** high (already escalated)
- **first observed (this pattern):** 2026-07-17; **reconfirmed:** 2026-08-24 21:39 EEST

### TODO-xpl-bias-contradiction-filled
- **issue:** XPL/USDT open B-tier swing long has moved from `waiting_for_entry` (18:40 EEST) to `triggered` (this cycle) while the swing report's own weakest-symbols data continues to tag XPL/USDT bias=short (24h -9.33%, RS vs BTC -12.76%). The desk has now taken on a filled position with an internally contradictory bias read. Same class of issue as [[project_crypto_ai_desk_bias_tag_contradiction]] (escalated HIGH 2026-08-08) but this is the first instance in the tracked recurrence where the contradiction persisted through an actual fill rather than resolving itself pre-entry (contrast with the PUMP/USDT case earlier today, which resolved as price moved before the desk had to act).
- **evidence:** `python -m src.cli active-signals --asset-class crypto` (`sig_096dc71b2ffff61c`, XPL/USDT, status=triggered, entry 0.104536-0.106512) vs `data/reports/swing/2026-08-24_15-35_swing_report.md` line 51 (`XPL/USDT: bias short, 24h -9.33%, RS vs BTC -12.76%`).
- **suggested manual fix:** a human session should (a) check whether a fresher swing scan (once available) still tags XPL bias=short, and (b) decide whether to trim/flatten the filled long given the conflict, since this is now live risk rather than a pending-entry watch item.
- **priority:** high
- **first observed:** 2026-08-24 18:40 EEST (as pending-entry contradiction); **escalated:** 2026-08-24 21:39 EEST (as filled-position contradiction)

### TODO-stocks-scan-staleness
- **issue:** no fresh stocks intraday scan has landed since 17:55 EEST (~3h44min as of this review) — tonight's stocks verdicts (guard-engaged, ABNB/MA/V open) are carried forward rather than confirmed against current data. This is within the carry-forward policy band but is worth a look if the gap continues to grow into the post-close slot.
- **evidence:** `ls -la data/reports/stocks/intraday/` — latest file `2026-08-24_14-55_stocks_intraday_report.md` (mtime 17:55 EEST).
- **suggested manual fix:** confirm the stocks intraday scheduler cadence is on track for the post-close slot; not urgent if it lands before 23:15 EEST.
- **priority:** low
- **first observed:** 2026-08-24 21:39 EEST
