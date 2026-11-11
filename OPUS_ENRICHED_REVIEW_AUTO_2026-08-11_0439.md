# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

**Slot: crypto overnight / Asia review (04:30 EEST fire). Advisory only — no auto-trade.** Scheduler fresh (cycle 3, 02:50-04:05, `scheduler.log` mtime 04:05, ~34min old at review start). US cash session closed — stocks are planning/watchlist context only (15 raw-A names all demoted to C on `market_closed_intraday_planning_only`). **No A-tier anywhere and zero new B-tier triggers this cycle** across scalp/intraday/swing — every idea produced tonight is C-tier watchlist. Crypto mood: mixed/chop (BTC/ETH internally `transition_down`, altcoin breadth 45-52% above EMA20, macro risk 99.8-100/100 risk-off on Iran/Strait-of-Hormuz oil headlines) but BTC externally still holding the $65k handle as of yesterday's last check. The desk continues to carry a large book of pre-existing open B-tier longs (HOME, PUMP, DODO, TST, BMT, TUT, THE, MUBARAK, HEI) — none new tonight. **TUT/USDT deepened sharply overnight** (-29.75% at last night's 23:30 post-close review → -45.90% in this morning's freshest scalp scan) while still carrying 3 open long swing positions — the bias-tag contradiction cluster ([[project_crypto_ai_desk_bias_tag_contradiction]]) is worsening further, not resolving. **Disk space kept falling**: 3.4GB (23:30 last night) → **1.5GB free / 100% used** now — this is now urgent, not just a watch-item. Untracked watchlist-alert count is 0 so far today (window just opened at 00:00 EEST, standing bug pattern not yet re-triggered). Catalyst mapping improved to 45.8% unmapped (from 59.5% last night) on today's fresh scan. Scanning/tracking/monitor continue uninterrupted into the Europe session.

## 2. Data Used

- `data/reports/scalp/2026-08-10_23-59_scalp_report.md` (fresh, gen 02:59 EEST, no A/B ideas)
- `data/reports/intraday/2026-08-11_00-07_intraday_report.md` (fresh, gen 03:07 EEST, no A/B ideas; C-tier only — HOME, TST)
- `data/reports/swing/2026-08-10_21-40_swing_report.md` (carry-forward, ~4h old, gen 00:40 EEST; no A/B ideas; 6 C-tier watchlist names: HOME, DODO, TST, PUMP, ACT, BICO)
- `data/reports/stocks/intraday/2026-08-11_00-43_stocks_intraday_report.md` (fresh, gen 03:43 EEST; market closed — 15 raw-A names demoted to C, planning only)
- `data/reports/stocks/swing/2026-07-02_13-03_stocks_swing_report.md`, `data/reports/stocks/invest/2026-07-02_13-05_stocks_invest_report.md` — **deprecated data source** (>1 month stale), excluded from verdicts per [[project_crypto_ai_desk_stocks_position_framework]]
- `data/catalysts/2026-08-11/catalyst_events.jsonl` (500 events), `narrative_baskets.jsonl` (2 baskets: `rwa_narrative` ONDO/XLM, `momentum_breakout` DODO/CRV), `catalyst_cycle_00-11.md` — all fresh, gen 03:11 EEST
- `python -m src.cli active-signals --asset-class crypto|stocks`
- `python -m src.cli signal-stats --asset-class crypto|stocks`
- `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-11` (0 rows)
- `data/scheduled_runs/2026-08-10_default_schedule/scheduler.log`, `cycle_03_02-50_summary.md`
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (gen 04:02 EEST, ~37min stale, fresh)
- Direct SQLite queries: `proposed_signals` (bias-cluster + candidate status), `watchlist_alerts` (today, empty), `narrative_baskets.jsonl` (raw)
- `OPUS_ENRICHED_REVIEW_AUTO_2026-08-10_2330.md` (previous review, for §4 comparison)
- 1 WebSearch (BTC/ETH overnight levels — no fresher-than-yesterday-morning data surfaced)

## 3. Scheduler / Data Freshness

- Latest cycle folder: `data/scheduled_runs/2026-08-10_default_schedule/`. `scheduler.log` mtime 04:05:53 EEST (~34min old at review start). `cycle_03_02-50_summary.md` mtime 04:05, same age. **Not deferred** — well under the 3h threshold.
- Cycle 3 (02:50-04:05) completed; fast_news_monitor log still actively writing (mtime 04:39, live).
- Crypto scalp/intraday: fresh (~1.5-1.7h old at review time). Crypto swing: carry-forward (~4h old, right at the fresh/carry-forward boundary) — no fresher swing scan ran overnight.
- Stocks intraday: fresh (~56min old at review start) but market is closed — all content is planning-only per the report's own banner.
- `PAPER_MONITOR_STATUS_LATEST.md`: gen 04:02 EEST, fresh (~37min old). Counts: OPEN_ACTIVE 49, WAITING_FOR_ENTRY 2, REVIEW_ONLY_SHADOW 41, ENTERED_UNRESOLVED_EXPIRED 2, NO_ENTRY_EXPIRED 242, CLOSED_WIN 160, CLOSED_LOSS 9, CLOSED_FLAT 33, UNKNOWN_INCONSISTENT/needs-review 3 (AAPL, GOOGL, XOM — all stocks/intraday, legacy `tp2_hit` unmapped-status inconsistency, pre-existing).
- Disk: **1.5GB free / 379GB / 100% used** — down from 3.4GB at 23:30 last night, continuing the 21:48→23:30 reversal. Re-escalating further (see §14).
- Untracked legacy alerts: 0 rows for `--since 2026-08-11` (window only ~4.5h old; the standing bug from [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] has not yet re-fired today, but has recurred nearly every day since 2026-07-17 — treat 0 as "not yet observed today," not "resolved").

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-11 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["fresher-than-yesterday-morning external BTC/ETH tick"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle 3 completed 04:05, scheduler.log 34min old", "crypto swing report ~4h old, right at carry-forward boundary", "catalyst files fresh, gen 03:11", "paper monitor snapshot 37min old, consistent with active-signals"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mixed", "chop", "risk_off", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH internally transition_down across scalp/intraday/swing all night", "altcoin breadth 45.45-52.27% above EMA20 depending on report", "macro risk 99.8-100/100 risk-off (Iran/Hormuz oil headlines) all night", "external check: BTC ~$65,209 / ETH ~$1,914 as of yesterday morning ET, no fresher overnight tick available"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["fresh_catalyst", "mapping_weak", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["45.8% unmapped (229/500) today's scan, improved from 59.5% last night", "2 active baskets: momentum_breakout (DODO/CRV, fresh<1h), rwa_narrative (ONDO/XLM, fresh<6h) — narrower than last night's 4 baskets"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["oi_supports", "data_unavailable", "squeeze_risk"],
      "data_missing": ["Bybit/OKX cross-check sparse for most tonight's movers"],
      "suggested_effect": "advisory_only",
      "facts_used": ["EPIC/USDT: price down + OI up 34-41% — fresh shorts pressing, possible squeeze if price reclaims", "DODO/USDT: negative funding across venues, crowding elevated per cross-check"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["stale_before_entry", "chase_risk", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing report ~4h old, the only source for tonight's C-tier ideas (HOME/DODO/TST/PUMP/ACT/BICO)", "no fresh A/B trigger produced in any of the 3 crypto reports tonight"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["04:02 snapshot: 49 OPEN_ACTIVE, 2 WAITING_FOR_ENTRY, 41 REVIEW_ONLY_SHADOW, 2 ENTERED_UNRESOLVED_EXPIRED, 242 NO_ENTRY_EXPIRED, 3 UNKNOWN_INCONSISTENT (legacy tp2_hit mapping, pre-existing, stocks-only)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["correlation_cluster", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT deepened -29.75%→-45.90% overnight while holding 3 open long swing positions", "BMT/USDT roughly flat/mixed (-36.29% last night → -30 to -33% this morning across reports) while holding 1 open long", "disk space 3.4GB→1.5GB overnight, 100% used"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.55,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier (week, n=292): PF 3.09, winrate 19.2%, totalR +87.60 — touch-based (highest-TP-touched), materially overstates realistic net execution per [[project_crypto_ai_desk_touch_based_pnl]]", "crypto scalp mode alone: n=65, PF 1.8x, avgR 0.03 — weak, consistent with the scalp report's own low-confidence banner", "stocks B-tier (week, n=12): winrate 0%, PF 0.0, totalR -8.00 — real negative, guard correctly keeping the desk flat"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.55,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "HOME/USDT", "trigger": "hold existing open swing long; only add on a fresh scan confirming price hasn't run further past the 0.0090-0.0092 band, RS-leader momentum intact", "reason": "cleanest fresh idea across all 3 reports tonight, RS +3.6-8.4% vs BTC, OI-confirmed positioning, no catalyst dependency to re-verify" },
    "best_short_candidate": { "symbol": "EPIC/USDT", "trigger": "wait for a failed reclaim of local resistance (0.0089-0.0090 area per swing report) before considering — currently >2 ATR from EMA20, do not chase the existing -21% to -25% move", "reason": "weakest-symbols list consistently, OI up 34-41% with price down (fresh shorts pressing, squeeze risk both ways), no clean short scored A/B tonight" },
    "best_catalyst_candidate": { "symbol": "DODO/USDT", "trigger": "momentum_breakout basket, fresh <1h as of 03:11 scan — wait for a pullback into a defendable zone rather than chasing the +13-24% move; already carries an open long from 08-09, any add needs its own re-confirmation", "reason": "only <1h-fresh basket tonight; CRV/USDT is the basket's other primary but has no open exposure and is >2 ATR extended per every report tonight" },
    "avoid_candidate": { "symbol": "TUT/USDT", "reason": "3 open long swing positions against a symbol that deepened from -29.75% to -45.90% 24h overnight — bias-tag contradiction cluster worsening specifically on this name; do not add, monitor invalidation levels only" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.55 | mixed, chop, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | fresh_catalyst, mapping_weak, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | oi_supports, data_unavailable, squeeze_risk | advisory_only |
| technical_entry | caution | 0.50 | stale_before_entry, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | ok | 0.75 | open_actionable, waiting_for_entry, review_shadow, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.55 | correlation_cluster, manual_review, reduce_risk | advisory_only |
| playbook_performance | ok | 0.55 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (2026-08-10 23:30 EEST, post-close final daily review)

- **TUT/USDT deepened sharply overnight.** -29.75% 24h at 23:30 last night → **-45.90%** in this morning's freshest scalp scan (02:59), -41.12% in the 03:07 intraday scan, -33.38% in the 00:40 swing scan. This is the single largest overnight move in the bias-tag contradiction cluster and still carries 3 open long swing positions (`sig_e4875989af64bab7`, `sig_d4b6e6c99e56865e`, `sig_7e26c4beb3fef840`).
- **BMT/USDT roughly stable-to-improved.** -36.29% at 23:30 → ranging -30.36% to -33.39% across tonight's 3 reports — still weak, still holding 1 open long (`sig_c00027d7dcde7b55`), but not deteriorating further like TUT.
- **THE/USDT, MUBARAK/USDT, HEI/USDT** — MUBARAK reappeared in tonight's weakest-symbols lists (-15 to -24% depending on report); THE and HEI did not surface in tonight's weakest-symbols top-5 but remain open longs (unchanged, not independently re-cleared).
- **Disk space fell further.** 3.4GB (23:30) → **1.5GB (this run)** — continuing the reversal flagged last night, now materially more urgent (drive essentially full).
- **Untracked watchlist alerts reset to 0** for the new `--since 2026-08-11` window (last night ended at 6 for 2026-08-10). Too early to call this "fixed" — the bug has recurred almost every day since 2026-07-17 and the day is only ~4.5h old.
- **Catalyst layer refreshed.** New scan at 03:11 EEST (vs. the stale 19:33 scan flagged all night last night) — unmapped dropped from 59.5% to 45.8%, baskets narrowed from 4 (delisting_thin_liquidity, binance_ecosystem_teaser, rwa_narrative, momentum_breakout) to 2 (rwa_narrative, momentum_breakout — DODO/CRV replacing HOME/GUN/RE as momentum_breakout's primary set).
- **MSFT legal-risk flag dropped off tonight's risk-warning lists** (was active last night with a "deadline effectively tomorrow" note — that date has now passed). Worth a same-day check on whether the underlying class action itself resolved or just the immediate deadline passed.
- **HOME/USDT, PUMP/USDT** — both still open/triggered, unchanged status from last night; no fresher swing scan ran to justify adding size.
- **No new CLI timeouts observed** in cycle 3's summary (need a fuller log read to confirm zero vs. last night's 3-timeout cycle-1 baseline — not independently re-verified this run).

## 5. Catalyst Coverage

- Total catalyst_events today (2026-08-11 scan, gen 03:11 EEST): 500. Mapped (non-null symbol): 271. Unmapped: 229 (**45.8%**).
- Narrative baskets: 2 — `momentum_breakout` (playbook `wait_pullback`, fresh <1h, primary DODO/USDT + CRV/USDT — "top gainers without confirmed news catalyst, pure momentum cluster"), `rwa_narrative` (playbook `related_beta_rotation`, fresh <6h, primary ONDO/USDT + XLM/USDT).
- Improved vs. last night (59.5% unmapped) but still material — **catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped-adjacent notable events tonight (sample, from `catalyst_cycle_00-11.md`): BTC/USDT exploit_hack (Spot Bitcoin ETF inflows post-Coldcard-hack), ETH/USDT exploit_hack (Coinsbuy $7.9M hack), BTC/USDT regulatory_sector_headline (Senate CLARITY Act vote pushed to Sept 15).

## 6. Market Landscape

- **Stocks — closed (Asia session).** Regime label from the last intraday scan (03:43 EEST) was "bullish" (VIX 15.46, breadth 100%), but this reflects yesterday's cash session — the report itself demotes all 15 raw-A names to C via `market_closed_intraday_planning_only`. No new stocks data will be actionable until 09:30 ET.
- **Crypto — still open, mid-Asia session.** BTC/ETH internally labeled `transition_down` on both trend axes across scalp/intraday/swing all night; altcoin breadth 45.45-52.27% above EMA20 (range/chop). Macro/geopolitics internal risk score 99.8-100/100 risk-off (Iran/Strait-of-Hormuz oil headlines) persisted through the whole overnight window. External check: BTC ~$65,209 / ETH ~$1,914 as of yesterday morning ET ([Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-august-10-2026-btc-breaking-past-65000-yet-again-125722282.html), published 2026-08-10) — no fresher overnight tick surfaced via WebSearch; treat as directionally consistent with the internal "holding, not breaking down" read, not confirmed for the current Asia hour.
- **What worked / failed overnight:** No fresh A/B signal fired in scalp, intraday, or swing across the whole overnight window — the desk is purely managing an existing book (49 open-actionable positions). Crypto B-tier week-to-date remains PF 3.09/winrate 19.2%/totalR +87.60 (touch-based, not realistic net — see playbook_performance agent). Scalp mode specifically remains the weakest cohort (PF 1.8x but avgR only 0.03, TP1/2h horizon mismatch per the scalp report's own low-confidence banner).

### Market Mood / Risk Routing
- Crypto mood: mixed/chop (technical transition_down + persistent risk-off macro overlay, but BTC holding $65k per last external check)
- Stocks mood: closed (Asia hours) — no fresh action, planning-only
- Dominant narrative: momentum_breakout (DODO/CRV, no confirmed news catalyst) and rwa_narrative (ONDO/XLM) — both narrower and more contained than last night's 4-basket spread
- Preferred side now: hold-existing / wait-for-trigger — no fresh A/B anywhere tonight to route into; manage the existing book, especially the worsening TUT position
- Best long candidate: HOME/USDT (hold, confirm before adding — §7.1)
- Best short candidate: EPIC/USDT (watch only — needs a failed reclaim before actionable, currently too extended to chase — §7.2)
- Best catalyst-backed candidate: DODO/USDT (`momentum_breakout` basket, fresh <1h — §7.3)
- What to avoid: adding to TUT/USDT long exposure (bias-tag cluster, worst overnight deterioration in the whole book), chasing HOME/DODO off a ~4h-stale swing band without a re-scan, any new stocks entries (market closed)
- What would change the view: a fresh crypto swing scan (current one is ~4h old, right at the carry-forward boundary); TUT's root-cause determination (is -45.9% a real breakdown or a data/liquidity artifact — worth a manual chart check); disk space needs an actual fix, not just monitoring, given it's now at 100% used with only 1.5GB free

## 7. Candidate Deep Dives

### 7.1 LONG HOME/USDT — best current idea, hold/confirm-before-add (crypto, swing, B-tier, score 67.0)

- **Status:** `triggered` per `active-signals` (`sig_fdde2c4132592ba0`, created 2026-08-10T17:48Z). Unchanged since last night.
- **Catalyst check:** no fresh verified catalyst — pure momentum/RS play, 24h +6.73% (swing report), RS vs BTC +8.39%, volume 0.73x.
- **Has price already reacted?** Yes — this is the same swing report price band used since yesterday evening; no fresher swing scan has run overnight.
- **Chase risk:** Elevated on any add — the underlying report is now ~4h old, right at the carry-forward boundary, no confirmation the entry zone (0.0090-0.0092) is still valid.
- **Retest/pullback structure?** Not independently re-verified this run — would need a fresh 1h/4h chart check (chart MCP not loaded; using OHLCV/ATR/EMA fields only, no fabricated chart read).
- **Actionable now?** Position already open/triggered — hold, no fresh sizing without a re-scan.
- **Invalidates at:** 1h close beyond 0.0089 (report) / 0.009957 (older live signal parameters — verify against current signal record before any manual action).
- **Aligned with mood?** Yes — RS-leader long remains the routing's preferred crypto side, though data staleness caps confidence on any add.
- **Chase-risk verdict:** Yes for new size; no for holding the existing position.

### 7.2 WATCH-SHORT EPIC/USDT — no clean short scored, needs confirmation (crypto, C-tier watchlist territory)

- **Status:** No open position; last proposed signal `entry_moved_away` (2026-08-08). Not currently in `active-signals`.
- **Evidence:** Weakest-symbols across all 3 reports tonight, 24h -21% to -25%, RS vs BTC -22% to -25%. Derivatives: price down + OI up 34-41% ("fresh shorts pressing, possible squeeze if price reclaims").
- **Chase risk:** High if entering now — price is >2 ATR from EMA20 per every report tonight ("do not chase" flag present in all 3 rejected-list entries).
- **Actionable now?** No — needs a failed reclaim of local resistance (0.0089-0.0090 area) before this becomes a clean setup; current state is squeeze-prone given the OI buildup against a falling price.
- **What would invalidate the idea?** A clean reclaim and hold above resistance would flip this to a squeeze risk rather than a short opportunity.

### 7.3 CATALYST-WATCH DODO/USDT — momentum_breakout basket, fresh <1h (crypto, swing, B-tier, existing open long + watchlist re-confirmation)

- **Status:** Already `triggered` per `active-signals` (`sig_60c8e6ef093e6886`, created 2026-08-09T03:10Z). The C-tier watchlist entry in tonight's swing report (score 61.8) is a re-confirmation of the same symbol, not a new signal.
- **Catalyst check:** `momentum_breakout` basket (fresh <1h as of 03:11 scan) — "top gainers without confirmed news catalyst, pure momentum cluster," 24h +13-24% depending on report, volume 0.8-1.1x.
- **Has price already reacted?** Yes, substantially (7d +34-96% depending on which report's window). Any fresh add here is chasing an already-extended move.
- **Actionable now?** Existing position — hold. Do not add without a pullback into the basket's stated re-entry structure; the basket's own suggested playbook is `wait_pullback`, not chase.
- **Counter-thesis:** No fresh verified catalyst backs the move — this is a "beta bounce inside range/chop" risk per every report's standard counter-thesis language; RS is not backed by strong current volume in most reads.

### 7.4 MANUAL-REVIEW — Bias-tag contradiction cluster, TUT worsening sharply overnight (crypto, risk flag, escalating)

- Tonight's freshest scalp scan (gen 02:59): **TUT/USDT -45.90%** 24h, RS vs BTC -44.44% — the single worst overnight move in the tracked weakest-symbols set, down from -29.75% at last night's 23:30 review. Intraday scan (03:07) shows -41.12%; swing scan (00:40) shows -33.38% — consistent worsening trend across the night regardless of which report window is used.
- TUT/USDT carries **3 open long swing positions** (`sig_e4875989af64bab7`, `sig_d4b6e6c99e56865e`, `sig_7e26c4beb3fef840`, created 2026-08-06 through 08-09) — all still `triggered` per `active-signals`.
- BMT/USDT (1 open long, `sig_c00027d7dcde7b55`) is comparatively stable: -36.29% last night → -30.36% to -33.39% tonight, not deteriorating further.
- MUBARAK/USDT reappeared in tonight's weakest-symbols lists (-15% to -24%); THE/USDT and HEI/USDT did not surface tonight but remain open longs, not independently re-cleared.
- **This is the third consecutive review flagging the same unresolved question** ([[project_crypto_ai_desk_bias_tag_contradiction]]): is "Weakest Symbols / bias short" purely descriptive momentum ranking, or should it gate/flag open-position risk review when it coincides with live long exposure? TUT's magnitude tonight (-45.9%) is the strongest evidence yet that this deserves a real answer.
- **Actionable now?** Manual review required — hold existing positions, monitor invalidation levels (particularly TUT given the magnitude of overnight deterioration), no forced exit implied, do not add.

## 8. Best Candidates Ranked

1. **Long-hold (already open, confirm before adding):** HOME/USDT — cleanest idea tonight, RS-leader momentum, hold; re-scan before adding size (§7.1).
2. **Catalyst-watch, existing exposure:** DODO/USDT — `momentum_breakout` basket fresh <1h; hold existing long, wait for pullback before adding (§7.3).
3. **Short-watch, not yet actionable:** EPIC/USDT — needs a failed reclaim of resistance before this becomes a clean short; too extended to chase now (§7.2).
4. **Manual-review cluster, most urgent name:** TUT/USDT (3 open longs, -45.9% overnight) + BMT/THE/MUBARAK/HEI (standing, less acute) — bias-tag contradiction worsening sharply on TUT specifically (§7.4).
5. **Avoid (planning only):** All 15 stocks-intraday raw-A names — market closed, `market_closed_intraday_planning_only` demotion; re-evaluate at/after 09:30 ET.

## 9. Avoid / No Trade (this decision window only)

- **New longs in TUT/USDT specifically** — sharpest overnight deterioration in the whole book (-29.75%→-45.90%) while holding 3 open positions; hold and monitor, don't add.
- **New longs in BMT/THE/MUBARAK/HEI** — bias-tag contradiction standing, less acute than TUT tonight but unresolved.
- **Chasing HOME/USDT or DODO/USDT** off a ~4h-stale swing report price without a fresh scan.
- **Chasing EPIC/USDT short** without a failed-reclaim confirmation — currently squeeze-prone (OI up, price down).
- **All 15 stocks-intraday raw-A names** — market closed, planning only; no path to actionable until 09:30 ET.
- This is a decision-window verdict only — scanning, tracking, and monitor operation all continue uninterrupted into the Europe session, no system pause implied.

## 10. Main Risks

1. **TUT/USDT overnight deterioration is the sharpest single-symbol move in the bias-tag cluster to date** (-29.75%→-45.90% across ~5h), against 3 open long positions — highest-priority open question tonight.
2. **Disk space continues to fall and is now critical**: 3.4GB→1.5GB overnight, 100% used — needs an actual fix, not just continued monitoring.
3. **Crypto swing data is ~4h old**, right at the carry-forward boundary, and is the only source for tonight's watchlist ideas (HOME, DODO, TST, PUMP, ACT, BICO).
4. **Untracked watchlist-alert bug** — 0 today so far, but has recurred almost daily since 2026-07-17; too early in the day to call it resolved.
5. **Catalyst mapping still material at 45.8% unmapped**, though improved from last night's 59.5%.
6. **MSFT legal-risk flag dropped off tonight's risk lists** — worth confirming whether the underlying class action resolved or just the immediate deadline passed.
7. **PAPER_MONITOR_STATUS_LATEST.md's 3 UNKNOWN_INCONSISTENT rows (AAPL, GOOGL, XOM)** — legacy `tp2_hit` unmapped-status issue, stocks-only, pre-existing, not re-diagnosed this run.

## 11. Action Plan — next 4 hours (into Europe session)

- Hold HOME/USDT and DODO/USDT swing longs; do not add without a fresh crypto scan confirming entry zones aren't chased.
- Do not add to TUT/USDT, BMT/USDT, THE/USDT, MUBARAK/USDT, or HEI/USDT long exposure; monitor invalidation levels only, with TUT as the priority watch given tonight's sharp deterioration.
- EPIC/USDT: watch only for a failed reclaim of resistance before considering a short.
- No new stocks entries — market closed; re-evaluate the 15 raw-A names at/after 09:30 ET with fresh RTH data.
- Watch for the next crypto scalp/intraday/swing cycle refresh to get a current read heading into the Europe session.
- Check disk space at the next review — 1.5GB free at 100% used is now a same-day operational concern, not a background watch-item.
- Confirm whether MSFT's legal-risk gate has genuinely cleared or is just between review cycles.

## 12. Final Verdict per Mode

- **Crypto scalp:** no A/B ideas overnight — no action; mode's own performance banner flags TP1/2h horizon mismatch (PF 0.14 on closed trades, low confidence by design).
- **Crypto intraday:** no A/B ideas overnight — watch only; used for the freshest Weakest Symbols cross-check (TUT/BMT).
- **Crypto swing:** hold/monitor the open book; HOME/USDT the cleanest existing idea (aging data, re-scan before adding), DODO/USDT catalyst-backed but extended, TUT/BMT/THE/MUBARAK/HEI bias-cluster needs manual review — TUT specifically escalating — no new longs in the affected names.
- **Stocks intraday:** 0 actionable, market closed — all raw-A names planning-only until 09:30 ET.
- **Stocks swing/invest:** deprecated data source, excluded, no verdict issued.

## 13. Sources

- [Bitcoin and ethereum prices today, Monday, August 10, 2026: BTC breaking past $65,000 yet again](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-august-10-2026-btc-breaking-past-65000-yet-again-125722282.html) (Yahoo Finance, published 2026-08-10) — most recent externally-verifiable BTC/ETH levels; no fresher overnight tick surfaced via WebSearch this run.
- `db/crypto_ai_desk.sqlite` `proposed_signals` table (internal) — bias-cluster (TUT/BMT/THE/MUBARAK/HEI), candidate (HOME/DODO/EPIC/PUMP/TST) open-position status, direct query this run.
- `db/crypto_ai_desk.sqlite` `watchlist_alerts` table (internal) — 0 rows since 2026-08-11T00:00, direct query this run.
- `data/catalysts/2026-08-11/catalyst_events.jsonl` / `narrative_baskets.jsonl` (internal, gen 03:11 EEST) — source for §5/§6/§7.3.
- `data/scheduled_runs/2026-08-10_default_schedule/scheduler.log`, `cycle_03_02-50_summary.md` (internal) — source for §3 freshness and disk-space findings.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (internal, gen 04:02 EEST) — source for §3 lifecycle counts.

## 14. Fix Requests / TODO

### TODO-disk-space-critical (re-escalate from medium to high)
- **issue:** C: drive free space continued falling overnight — 5.2GB (23:30 -1) → 3.4GB (23:30) → **1.5GB (04:39, this run)**, 100% used throughout. The drive is now materially close to full.
- **evidence:** `df -h /c` this run: `1.5G Avail, 100% use`, vs. 3.4GB/100% at 23:30 last night.
- **suggested manual fix:** identify what is consuming space now — root cause has never been identified across 7+ reviews despite oscillating readings; given the sustained decline (not a one-off spike) and near-zero headroom, treat as same-day priority before any log-heavy scheduler cycle risks failing on disk-full.
- **priority:** high (re-escalated from medium; the 21:48→23:30→04:30 trend is now 3 consecutive declining readings with the lowest free-space level observed yet).
- **first observed:** 2026-08-09 (escalated across 7+ reviews, oscillating); continued decline confirmed 2026-08-11 04:39 (this run).

### TODO-bias-tag-contradiction-tut-acute (update — TUT specifically escalating overnight, priority unchanged high)
- **issue:** TUT/USDT — carrying 3 live open long swing positions — deepened from -29.75% (23:30 last night) to -45.90% (this morning's freshest scalp scan), the sharpest single overnight move observed in this standing cluster since it was first flagged 2026-08-08.
- **evidence:** `data/reports/scalp/2026-08-10_23-59_scalp_report.md` (gen 02:59) vs. `OPUS_ENRICHED_REVIEW_AUTO_2026-08-10_2330.md` §7.3 (23:30 reading); `active-signals --asset-class crypto` for TUT open-position confirmation (`sig_e4875989af64bab7`, `sig_d4b6e6c99e56865e`, `sig_7e26c4beb3fef840`).
- **suggested manual fix:** unchanged — determine whether "Weakest Symbols / bias short" should feed a position-review flag when it coincides with open long exposure. TUT's magnitude tonight is the strongest single data point yet for treating this as more than descriptive.
- **priority:** high (unchanged; TUT's acute overnight move strengthens the case).
- **first observed:** 2026-08-08 (ZBT/ACE); widened 2026-08-10 (BMT/TUT worsening trend); TUT acute overnight deterioration confirmed 2026-08-11 04:39 (this run).

### TODO-watchlist-alert-untracked-signals (carried forward, high — 0 occurrences so far today)
- **issue:** Standing bug where Telegram watchlist alerts fire without a matching `proposed_signal`. 0 rows for `--since 2026-08-11` as of this run, but the pattern has recurred almost daily since 2026-07-17 (6 rows as of last night's 23:30 review for 2026-08-10) — too early in today's window (~4.5h old) to treat as resolved.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-11` — 0 rows this run.
- **suggested manual fix:** unchanged from [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] — trace why the watchlist-alert path isn't minting a fresh `proposed_signal`/`signal_id`.
- **priority:** high (unchanged, escalated to high 2026-07-17).
- **first observed:** 2026-07-17 (carried forward, recurring almost daily).

### TODO-msft-legal-risk-recheck (new, low)
- **issue:** MSFT dropped off tonight's production risk-warning lists (was `block_requires_operator_review` on securities-fraud class action last night, deadline "effectively tomorrow" i.e. 2026-08-11 = today).
- **evidence:** `data/reports/scalp/2026-08-10_23-59_scalp_report.md` and `data/reports/intraday/2026-08-11_00-07_intraday_report.md` §5c — MSFT absent from tonight's operator-review list (AAVE, BTC, ISRG, RIOT/CSCO, SMCI only).
- **suggested manual fix:** confirm whether the underlying class action genuinely resolved/quieted or the flag just expired on the calendar date without the news flow being re-checked; low priority since stocks are closed regardless until 09:30 ET.
- **priority:** low.
- **first observed:** 2026-08-11 04:39 EEST (this run).

_None further._
