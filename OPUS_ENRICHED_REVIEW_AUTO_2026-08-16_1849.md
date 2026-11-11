# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

## 1. Executive Summary

**US open reaction review, ~18:45 EEST (nearest fired slot to 18:30).** **Advisory only — no auto-trade.** Two things dominate this cycle. First, **the C: drive disk-full incident that blocked the 11:30 and 16:00 reviews is now resolved** (57GB free vs. 0 bytes at 16:03) and the scheduler/monitor stack has restarted — `scheduler.log` is fresh (32 min old), `PAPER_MONITOR_STATUS_LATEST.md` is fresh (4 min old), catalyst files are fresh (~1h12m old). Second, and more important: **the recovery is only partial.** Independent verification of the 22 `OPEN_ACTIVE` crypto swing/intraday positions shows `signal_outcomes.max_adverse_excursion_r = 0.0` for **all 22 simultaneously** at a fresh `checked_at` (~15:42 UTC) — statistically implausible and consistent with a monitor loop that updates its timestamp without actually refreshing price. Direct OHLCV-cache inspection confirms **17 of the 22 open positions have not had a fresh candle since ~2026-08-15 22:30–23:00 UTC (~17–20h stale)**, and for 4 of those (BMT, MUBARAK, BABY, HOLO) the last *real* price already sat well through the recorded invalidation level (BMT −49.7%, MUBARAK −23.9%, BABY −25.3%, HOLO −22.9%) — the same core finding the 02:00 auto-review and the 11:39 chat-delivered review already raised. This is now a **3rd consecutive flag of the same unresolved defect** — treat the "🟢 OPEN — monitoring TP/SL" status on the swing book with active distrust until an operator confirms live price manually. No A-tier setups anywhere (crypto or stocks) this cycle; crypto regime is downtrend/risk-off; stocks are closed (Sunday, planning-only).

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-16_default_schedule/scheduler.log` — fresh, mtime 18:07 (32 min old at review start). Latest cycle-summary file (`cycle_01_15-43_summary.md`) is 0 bytes — a disk-full-era artifact — but the freshness gate only requires scheduler.log OR a recent summary; scheduler.log clears it.
- Reports: scalp `2026-08-16_16-52` (~1h50m, fresh), intraday `2026-08-16_17-31` (~1h10m, fresh), swing `2026-08-16_12-42` (~5h57m, carry-forward band, flagged), stocks intraday `2026-08-14_23-09` (Friday close, market closed Sunday — planning-only), stocks swing/invest (from 2026-07-02 — stale, not used).
- Catalysts: `data/catalysts/2026-08-16/catalyst_events.jsonl` (314 events, fresh ~1h12m), `narrative_baskets.jsonl` (5 baskets).
- LLM packets: not separately re-read this cycle (report content covers the same ground; time budget prioritized the price-integrity investigation below).
- CLI: `active-signals` (crypto n=48, stocks n=50), `signal-stats` (crypto), `detect_untracked_legacy_alerts --since 2026-08-16` → clean (no untracked alerts today).
- Direct read-only SQL against `db/crypto_ai_desk.sqlite` (`proposed_signals`, `signal_outcomes`) — read queries only, no writes.
- Direct file-timestamp/last-row inspection of `data/raw/ohlcv/binance/15m/*.csv` for all 22 open crypto positions, cross-checked against recorded `invalidation` levels.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (fresh, 18:45) and `data/autostart/pending_monitor_recovery.out.log` (stopped writing at 16:09 — still inside the disk-critical phase — superseded by newer python processes started 16:07–18:41 per `Get-Process`).
- Windows Task Scheduler state (`Get-ScheduledTask`/`Get-ScheduledTaskInfo`) for `CryptoAIDeskMonitor` (last ran 16:21, success), `CryptoAIDeskHeartbeat` (last ran 18:37, success, next 18:57), `CryptoAIDesk_TelegramCollector` (Running). `CryptoAIDesk_Scheduler` itself last fired 6/15/2026 — this is expected/known: the actual cycle loop runs under the `CryptoAIDeskMonitor` watchdog restart pattern, not the named Scheduler task (per prior session's persistence design), not a new issue.
- Prior review for comparison: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-16_0200.md` (crypto overnight, 02:00 EEST) plus the two blocked reviews `OPUS_ENRICHED_REVIEW_BLOCKED_2026-08-16T1139.md` and `OPUS_ENRICHED_REVIEW_BLOCKED_2026-08-16T1600EEST.md`.
- **External web research not run this cycle.** No candidate this cycle depends on unverified external claims — the dominant finding (price-feed staleness) is fully internally evidenced via file timestamps and DB queries, and macro catalysts (Iran/Hormuz, BTC Coldcard exploit, ETH quantum roadmap) are already multi-source corroborated inside the reports carried from the 02:00 review.

## 3. Scheduler / Data Freshness

- Scheduler: **fresh** (32 min old), actively writing.
- Disk: **recovered** — 57GB free (was 0 bytes at 16:03 EEST, the cause of both the 11:39 and 16:00 blocked reviews).
- Scalp/intraday reports: fresh (~1h10–1h50m). Swing: carry-forward (~6h). Stocks: closed for the weekend, planning-only.
- Catalyst folder: fresh (~1h12m), 314 events, 5 baskets.
- **Monitor/price-feed integrity: DEGRADED, not fully recovered.** `PAPER_MONITOR_STATUS_LATEST.md` itself is fresh (18:45) and `signal_outcomes.checked_at` is current (~15:41–15:42 UTC / ~18:41–18:42 EEST) for all 22 open positions — but the underlying OHLCV cache for 17 of those 22 symbols has not produced a fresh candle since ~2026-08-15 22:30–23:00 UTC, and `max_adverse_excursion_r = 0.0` for literally all 22 simultaneously. See §9/§14 — this means "checked" ≠ "priced."
- `detect_untracked_legacy_alerts --since 2026-08-16`: **clean**.
- 3 items in `UNKNOWN_INCONSISTENT` (AAPL, GOOGL, XOM stocks/intraday/B — unmapped status `tp2_hit` with `touched=False`) — minor, see §14.
- Gap note: no gap in the routine's own output today beyond the two disk-caused blocks — the 02:00, 11:39(blocked), 16:00(blocked) sequence is fully accounted for.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-16 18:49 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["live price for BMT/USDT, MUBARAK/USDT, BABY/USDT, HOLO/USDT, ETHFI/USDT, TST/USDT, THE/USDT, PEOPLE/USDT, BANANAS31/USDT, LUNA/USDT, PROM/USDT (x2), AVNT/USDT, MMT/USDT (x2), CYS/USDT, VELVET/USDT — OHLCV cache stuck ~17-20h despite fresh checked_at"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 18:07", "disk 57GB free vs 0 bytes at 16:03", "17/22 open-position OHLCV files last candle 2026-08-15 22:30-23:00 UTC", "signal_outcomes MAE=0.0 for all 22 open positions at checked_at ~15:42 UTC"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["intraday report: BTC downtrend, ETH downtrend, altcoin breadth 40% above EMA20", "macro risk 67.4/100, Iran/Hormuz headlines", "recommended trading style: short bias or no trade; avoid weak altcoin longs"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "mapping_weak"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl 314 total, 170 mapped / 144 unmapped (45.9% unmapped, borderline)", "SOL/USDT fresh catalyst: Bitwise staking-ETF tokenization via Superstate", "BTC/ETH catalysts flagged with risk caution (Coldcard exploit, ETH quantum roadmap)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "funding_extreme", "data_unavailable"],
      "data_missing": ["OI 24h% for all symbols listed as n/a"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PORTAL/USDT: negative funding across bybit+mexc, crowding elevated, 4.02x volume, tagged overextended", "HOME/USDT and ACE/USDT: negative funding across venues, crowding elevated"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["overextended", "chase_risk", "entry_fresh"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PORTAL/USDT +33.66% 24h, 4.02x volume, tagged overextended — chase risk if long now", "WLFI/USDT OHLCV fresh (last candle 15:15 UTC today), price 0.0615 vs invalidation 0.055757 — confirmed still valid"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PAPER_MONITOR_STATUS_LATEST.md: OPEN_ACTIVE 22, WAITING_FOR_ENTRY 3, REVIEW_ONLY_SHADOW 21, ENTERED_UNRESOLVED_EXPIRED 0, NO_ENTRY_EXPIRED 5, CLOSED 161W/7L/36flat, UNKNOWN_INCONSISTENT 3"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.85,
      "reason_codes": ["manual_review", "reduce_risk", "repeated_losses"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BMT/USDT last real price 0.01499 vs invalidation 0.029802 = -49.7%", "MUBARAK/USDT 0.01589 vs 0.020892 = -23.9%", "BABY/USDT 0.0098 vs 0.01311343 = -25.3%", "HOLO/USDT 0.0601 vs 0.07792571 = -22.9%", "same defect flagged at 02:00 review (17/24) and 11:39 blocked review (19/28) — 3rd consecutive cycle", "HOME/USDT bias-tag contradiction: report lists HOME as bias=short weakest symbol while an OPEN long HOME/USDT swing position is active"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["signal-stats crypto: tier=B PF 2.84 (n=99), mode=swing PF 5.68 (n=47, stronger), mode=intraday PF 1.33 (n=36), mode=scalp PF 3.70 but 'weak' confidence n=16", "weekend=Y signals underperform: winrate 15%, n=16 (existing CLI observation)"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.7,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.75,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "WLFI/USDT", "trigger": "already-open swing long, price confirmed via fresh OHLCV above invalidation (0.0615 vs 0.055757); add only on retest toward 0.0563-0.0568 entry band, not at current level", "reason": "only major open long with independently-confirmed fresh price data, RS-leader (+12.66% 24h), low cross-exchange crowding" },
    "best_short_candidate":    { "symbol": "ACE/USDT", "trigger": "failed retest of recent breakdown low / continuation below current level on volume confirmation", "reason": "weakest RS symbol in both scalp and intraday reports (-20.99% 24h), negative funding + elevated crowding across venues, aligned with risk-off/short-bias regime recommendation" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "confirmed follow-through news on Bitwise/Superstate staking-ETF tokenization talk plus reclaim of short-term resistance", "reason": "only crypto symbol with a fresh, single-source-but-plausible catalyst tagged in this cycle's report; needs a second source before treating as primary" },
    "avoid_candidate":         { "symbol": "BMT/USDT and MUBARAK/USDT", "reason": "confirmed deep through invalidation on last real price (-49.7% and -23.9% respectively) while dashboard still shows them 'OPEN - monitoring TP/SL' off stale data; do not treat as healthy positions until an operator manually checks live price" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.75 | risk_off, shorts_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.60 | fresh_catalyst, catalyst_confirmed, mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | overextended, chase_risk, entry_fresh | advisory_only |
| execution_lifecycle | manual_review | 0.70 | open_actionable, waiting_for_entry, review_shadow, needs_review | advisory_only |
| risk_manager | manual_review | 0.85 | manual_review, reduce_risk, repeated_losses | advisory_only |
| playbook_performance | ok | 0.60 | playbook_working, low_sample | advisory_only |
| head_trader | manual_review | 0.70 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

- **Disk-full resolved**: 02:00/11:39 reviews ran (or were blocked) under a C: 0-bytes-free condition; now 57GB free, scheduler/monitor processes restarted (new python processes since 16:07 EEST).
- **Core finding NOT resolved, only re-confirmed differently**: 02:00 review found 17/24 open positions through stop via direct price comparison; 11:39 blocked-review found 19/28 (worse, monitors dark since 05:02); this cycle's independent check confirms BMT/MUBARAK/BABY/HOLO are still through invalidation on the last *real* price available (~17-20h old), while the dashboard now falsely reports them healthy because the checked_at timestamp refreshes without a real price refresh.
- **New this cycle**: the "checked_at fresh but MAE=0.0 for all 22" pattern is a clean, simple piece of evidence that wasn't isolated this precisely before — it converts "we think the monitor is broken" into "here is the exact mechanism" for the TODO.
- No A-tier signals in either the 02:00 review or this one. No new B-tier triggers this cycle (scalp/intraday/swing reports all show "No A-tier / No B-tier setups found").
- Catalyst mapping improved from "weak" (66.3% unmapped at 02:00, Aug 15 UTC-dated folder) to 45.9% unmapped today (Aug 16 folder) — below the 50% flag threshold now.

## 5. Catalyst Coverage

- Total catalyst events today: **314**. Mapped (symbol present): **170** (54.1%). Unmapped: **144** (45.9%) — below the 50% "weak" threshold, no blanket downgrade needed, but close enough to keep watching.
- Narrative baskets: **5**.
- Sample unmapped headlines (context only, not action-driving): "Pope calls for an end to West Bank violence against Palestinians", "$10,000 in NuScale at Its 52-Week High Is Worth About $1,650 Today", "Wendy's Jumps on Report That Nelson Peltz Wants to Take His Old Company Private".
- Mapped, symbol-relevant catalysts this cycle: SOL/USDT (Bitwise/Superstate staking-ETF tokenization, single-source), BTC/ETH risk-flagged (Coldcard exploit ongoing — 1,432-1,778 BTC stolen depending on source, multi-source; ETH quantum-roadmap SHA/BLAKE migration, single-source geopolitical/risk tag).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **risk-off / chop** (BTC downtrend, ETH downtrend, altcoin breadth only 40% above EMA20, macro risk 67.4/100 driven by Iran/Hormuz Gulf tension headlines).
- Stocks mood: **closed** (Sunday) — Friday's stocks intraday report (2026-08-14 23:09) is planning-only context; nothing tradeable until Monday's US open.
- Dominant narrative: no single dominant narrative — AI (heat 40.4/100) and RWA (heat 31.5/100) are the warmest baskets, both "mixed" status, neither strongly directional. PORTAL/USDT is the standout mover (+33.66% 24h) but tagged overextended with elevated cross-venue funding crowding — reads as chase risk, not a clean trend leader.
- Preferred side now: **wait-for-trigger, lean short-biased** per the report's own recommended trading style ("short bias or no trade; avoid weak altcoin longs").
- Best long candidate: WLFI/USDT (existing open position, confirmed fresh/valid) — see §8 for the trigger for adding size; no *new* long entries recommended this cycle.
- Best short candidate: ACE/USDT — none clean without a confirmed failed-retest trigger; see §8.
- Best catalyst-backed candidate: SOL/USDT — single-source, needs confirmation before treating as primary.
- What to avoid: chasing PORTAL/USDT at current extension; trusting the "OPEN — monitoring TP/SL" badge on BMT/USDT, MUBARAK/USDT, BABY/USDT, HOLO/USDT without a manual live-price check.
- What would change the view: (a) OHLCV refresh resuming for the 17 stale symbols and MAE values becoming non-zero and differentiated (proof the monitor is genuinely tracking again); (b) BTC/ETH reclaiming key EMA levels (would flip regime from risk-off toward neutral); (c) a second, independent source corroborating the SOL/Bitwise catalyst.

## 7. Candidate Deep Dives

### 1. BMT/USDT (open long, swing, B-tier) — RISK ITEM, not a new trade
- Status shown: 🟢 OPEN — monitoring TP/SL (source=legacy touch), `stop_hit=0`, `checked_at` 2026-08-16T15:42:41Z (fresh).
- Independent check: last *real* OHLCV candle is 2026-08-15 23:00 UTC, close 0.01499. Recorded invalidation: 0.029802. That is **-49.7% through stop** on the last confirmed real price.
- Has price already reacted to any catalyst? No specific BMT catalyst found; this looks like a pure trend/liquidity move plus (possibly) continued drift since the last real print.
- Is this a chase-risk setup? N/A — not a new entry; this is an existing position that likely should already be closed.
- Actionable now? **No — flag for operator manual close/verification**, not a trade idea.
- What would invalidate/confirm: a fresh live price check against Binance/Bybit. If confirmed through stop, this should be marked stop_hit and closed in the system (a human/engineering task, not something this review can or should do).

### 2. MUBARAK/USDT (open long, swing, B-tier) — RISK ITEM
- Same pattern as BMT: last real price 0.01589 (2026-08-15 22:30 UTC) vs invalidation 0.020892 = **-23.9% through stop**. `checked_at` fresh, `stop_hit=0`. Needs the same manual verification.

### 3. BABY/USDT and HOLO/USDT (open longs, swing, B-tier) — RISK ITEMS
- BABY: last real price 0.0098 (2026-08-15 22:30 UTC) vs invalidation 0.01311343 = **-25.3%**.
- HOLO: last real price 0.0601 (2026-08-15 22:30 UTC) vs invalidation 0.07792571 = **-22.9%**.
- Both show identical "checked_at fresh / stop_hit=0" false-healthy pattern. Same manual-verification ask as BMT/MUBARAK.

### 4. WLFI/USDT (open long, swing, B-tier) — CONFIRMED HEALTHY (contrast case)
- Last real OHLCV candle: 2026-08-16 15:15 UTC (today, current), close 0.0615. Recorded invalidation 0.055757. **Genuinely still valid**, ~10% above stop.
- This is the control case proving the monitor *can* work correctly when its data feed is actually current — the failure is data-pipeline-specific to certain pairs, not a universal outage.
- Has price reacted to catalyst? WLFI has no specific fresh catalyst flagged this cycle; move is broad relative-strength (+12.66% 24h), low crowding, neutral external funding.
- Actionable now? Hold existing position; do not add fresh size at current extension — wait for a pullback toward the 0.0563-0.0568 original entry band before considering an add.

### 5. HOME/USDT — INTEGRITY FLAG (bias-tag contradiction, not a trade candidate)
- The 2026-08-16 intraday and scalp reports both classify HOME/USDT as **bias=short** in the "Weakest Symbols" table (24h -16.03% to -16.21%), while `proposed_signals`/`PAPER_MONITOR_STATUS_LATEST.md` simultaneously carries an **open long** HOME/USDT swing B-tier position (entry ~0.010261-0.010509), displayed as OPEN with no stop flag.
- This is the same recurring bias/direction-tag contradiction pattern already tracked as a HIGH-priority open item for other symbols (ZBT/ACE, flagged across 3 consecutive prior reviews) — HOME/USDT appears to be a new instance of the same underlying defect. See §14 TODO-2.

## 8. Best Candidates Ranked

Given no fresh A/B setups this cycle and a live data-integrity issue on the open book, this section is risk-routing rather than new-trade ranking:

1. **WLFI/USDT — hold / watch for pullback add.** Trigger to add: retest of 0.0563-0.0568. Trigger to exit early: close back below invalidation 0.055757 on fresh data.
2. **ACE/USDT — short-watch.** Trigger: confirmed failed retest of the most recent breakdown level with volume; do not chase the initial move.
3. **SOL/USDT — catalyst-watch.** Trigger: a second independent source on the Bitwise/Superstate staking-ETF tokenization story, plus price reclaiming short-term resistance.
4. **BMT/USDT, MUBARAK/USDT, BABY/USDT, HOLO/USDT — manual-review-watch, not a trade idea.** Trigger to resolve: any fresh live price check (manual or automated) confirming actual status; if through stop, these need to be closed in the system.

No new long entries are recommended into a risk-off, no-A-tier, largely stale-priced book this cycle.

## 9. Avoid / No Trade

*(This decision window only — never a command to stop the system; the scanner, catalyst collection, and monitors should keep running.)*

- Avoid chasing PORTAL/USDT at +33.66%/24h with 4.02x volume and elevated cross-venue funding crowding — textbook overextension.
- Avoid treating BMT/USDT, MUBARAK/USDT, BABY/USDT, HOLO/USDT (and likely several of the other 13 stale-priced open positions) as confirmed-healthy based on the current dashboard — the "OPEN" badge on these is not currently trustworthy.
- Avoid new stocks decisions until Monday's US open — Friday's data is planning-only.
- Avoid over-trusting the scalp playbook — the scalp report's own banner states "low confidence... PF 0.14 over 14d" even though this cycle's CLI `signal-stats` shows a more favorable PF 3.70 on a different/wider window; these two numbers disagree and neither should be treated as decisive without reconciling the windows (see §14 for note — not a fix task, just flagging the discrepancy for awareness).

## 10. Main Risks

1. **Price-feed/monitor integrity (highest risk this cycle).** 17 of 22 open crypto positions are being reported "OPEN — healthy" off OHLCV data that is 17-20 hours stale, with `max_adverse_excursion_r=0.0` across the board — a pattern that looks like a no-op refresh rather than genuine confirmation. At least 4 of those positions are independently confirmed deep through invalidation on the last real price. This directly affects capital-at-risk visibility, not just review quality.
2. **Recurring, unresolved defect.** This is the 3rd consecutive review cycle (02:00 today, 11:39 blocked-today, now 18:45 today) to surface materially the same issue, tracing back to the `pending_monitor` `PermissionError: [WinError 5]` worker-recycle bug first noted 2026-08-13.
3. Macro/geopolitical risk elevated (Iran/Hormuz Gulf tension, ongoing BTC Coldcard exploit narrative) — contributes to the risk-off regime read.
4. Catalyst mapping at 45.9% unmapped — usable but not far from the 50% "weak" threshold; keep monitoring trend.
5. HOME/USDT bias-tag contradiction (see §7.5, §14 TODO-2) — a data-integrity smell, not itself capital-at-risk, but erodes trust in the bias-tagging layer.

## 11. Action Plan — Next 4 Hours

1. **Operator: manually verify live price for BMT/USDT, MUBARAK/USDT, BABY/USDT, HOLO/USDT** against Binance/Bybit directly (outside this automated pipeline) and close/mark stop_hit if confirmed through invalidation — this review cannot and should not make that state change itself.
2. Watch whether the OHLCV cache for the 17 stale symbols resumes refreshing over the next cycle or two; if it does not, escalate the pending_monitor bug as a priority engineering item (already in §14).
3. No new crypto longs into current extension; only the WLFI pullback-add and the ACE short-watch trigger from §8 are worth tracking actively.
4. Re-check catalyst mapping ratio next cycle — watch for a cross above 50% unmapped.
5. Stocks: hold all planning-only context from Friday; nothing actionable until Monday's US cash open.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade — no A/B setups this cycle; playbook confidence itself flagged low by its own report banner.
- **Crypto intraday:** No trade — no A/B setups; short-bias-or-no-trade regime recommendation stands.
- **Crypto swing:** **Manual review required** on the existing open book (BMT/MUBARAK/BABY/HOLO especially) before any new swing decisions; no new entries this cycle.
- **Stocks intraday/swing/invest:** Closed (Sunday) — planning-only, no verdict due until Monday's session.

## 13. Sources

- Internal only this cycle (no external WebSearch/WebFetch run — see §2 for rationale):
  - [data/reports/intraday/2026-08-16_14-31_intraday_report.md](data/reports/intraday/2026-08-16_14-31_intraday_report.md) — generated 2026-08-16 17:31 EEST
  - [data/reports/scalp/2026-08-16_13-52_scalp_report.md](data/reports/scalp/2026-08-16_13-52_scalp_report.md) — generated 2026-08-16 16:52 EEST
  - [data/reports/swing/2026-08-16_09-42_swing_report.md](data/reports/swing/2026-08-16_09-42_swing_report.md) — generated 2026-08-16 12:42 EEST
  - [reports/PAPER_MONITOR_STATUS_LATEST.md](reports/PAPER_MONITOR_STATUS_LATEST.md) — 2026-08-16 18:45 EEST
  - [OPUS_ENRICHED_REVIEW_AUTO_2026-08-16_0200.md](OPUS_ENRICHED_REVIEW_AUTO_2026-08-16_0200.md) — prior review, 2026-08-16 02:00 EEST
  - [OPUS_ENRICHED_REVIEW_BLOCKED_2026-08-16T1139.md](OPUS_ENRICHED_REVIEW_BLOCKED_2026-08-16T1139.md), [OPUS_ENRICHED_REVIEW_BLOCKED_2026-08-16T1600EEST.md](OPUS_ENRICHED_REVIEW_BLOCKED_2026-08-16T1600EEST.md)
  - `db/crypto_ai_desk.sqlite` (`proposed_signals`, `signal_outcomes`) — direct read-only queries, 2026-08-16 ~18:40-18:48 EEST
  - `data/raw/ohlcv/binance/15m/*.csv` — file-timestamp and last-row inspection, 2026-08-16 ~18:45 EEST

## 14. Fix Requests / TODO

### TODO-price-feed-staleness-vs-checked-at
- **issue:** For 17 of 22 currently `OPEN_ACTIVE` crypto positions, `signal_outcomes.checked_at` refreshes every monitor cycle (fresh, ~15:41-15:42 UTC) but `max_adverse_excursion_r=0.0` and `stop_hit=0` for **all 22 simultaneously**, while the underlying OHLCV cache for those 17 symbols has not produced a fresh candle since ~2026-08-15 22:30-23:00 UTC (17-20h stale). For 4 of those (BMT, MUBARAK, BABY, HOLO) the last *real* price was already 22.9%-49.7% through the recorded invalidation level. The dashboard (`PAPER_MONITOR_STATUS_LATEST.md`) reports all of these as healthy "🟢 OPEN — monitoring TP/SL."
- **evidence:** `db/crypto_ai_desk.sqlite` `signal_outcomes` query (22 rows, all `stop_hit=0`, `max_adverse_excursion_r=0.0`, `checked_at` between 2026-08-16T15:24:18Z and 15:42:41Z); `data/raw/ohlcv/binance/15m/{BMT,MUBARAK,BABY,HOLO,ETHFI,TST,THE,PEOPLE,BANANAS31,LUNA,PROM,AVNT,MMT}_USDT.csv` last-row timestamps all 2026-08-15T22:30:00+00:00 or 23:00:00+00:00, file mtimes 2026-08-16 01:39-02:12 (i.e., not touched since before the disk-full outage began ~05:02); contrast with `WLFI_USDT.csv` (last row 2026-08-16T15:15:00+00:00, mtime 18:26 — genuinely fresh) proving the fetch path works for at least some pairs. Same core defect previously flagged in `OPUS_ENRICHED_REVIEW_AUTO_2026-08-16_0200.md` (§3, PermissionError WinError 5 on `pending_monitor` worker-recycle, traced back to the 2026-08-13 21:40 review) and in `OPUS_ENRICHED_REVIEW_BLOCKED_2026-08-16T1139.md`.
- **suggested manual fix:** A human/engineering session should inspect the `pending_monitor` refresh/tracker loop to confirm whether it silently skips OHLCV fetch for pairs outside its per-tick `selected_crypto` sample (the recovery log showed `selected_crypto=49` per tick against a larger open book) rather than genuinely re-checking every open position every cycle, and separately, manually verify live price on BMT/USDT and MUBARAK/USDT today and close/mark them if still through stop.
- **priority:** high (3rd consecutive review cycle raising materially the same issue).
- **first observed (this thread):** 2026-08-16 02:00 EEST; re-confirmed with new mechanism-level evidence 2026-08-16 18:49 EEST.

### TODO-2-home-usdt-bias-contradiction
- **issue:** HOME/USDT is tagged `bias=short` in the 2026-08-16 intraday/scalp "Weakest Symbols" tables while an OPEN long HOME/USDT swing B-tier position is simultaneously active with no contradiction flag surfaced to the operator.
- **evidence:** `data/reports/intraday/2026-08-16_14-31_intraday_report.md` line ~50 ("HOME/USDT: bias short, 24h -16.21%"); `reports/PAPER_MONITOR_STATUS_LATEST.md` line 83 ("HOME/USDT long (crypto/swing/B) — 🟢 OPEN").
- **suggested manual fix:** extend whatever surfaced the prior ZBT/ACE bias-tag-contradiction TODO to also catch this HOME/USDT instance; likely the same root cause (bias tag computed independently of open-position direction, no cross-check).
- **priority:** medium (recurring pattern, new symbol).
- **first observed (this thread):** 2026-08-16 18:49 EEST (prior instances on other symbols date back to 2026-08-08 per project history).

### TODO-3-stocks-unmapped-tp2-status
- **issue:** 3 stocks/intraday/B positions (AAPL, GOOGL, XOM) show `UNKNOWN_INCONSISTENT` / "unmapped status 'tp2_hit'" with `touched=False` in the lifecycle dashboard.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` lines 160, 167, 170.
- **suggested manual fix:** add `tp2_hit` to the lifecycle-status mapping table used by the display layer, or investigate why `touched=False` positions are landing in a TP-hit status at all.
- **priority:** low.
- **first observed (this thread):** 2026-08-16 18:49 EEST.

### TODO-4-scalp-pf-discrepancy
- **issue:** The scalp report's own banner states "1W/7L over 14d, PF 0.14" while this cycle's `signal-stats --asset-class crypto` CLI shows `mode=scalp` PF 3.70 (n=16, confidence "weak"). These appear to be different lookback windows but are presented without reconciliation, risking an operator reading the wrong number.
- **evidence:** `data/reports/scalp/2026-08-16_13-52_scalp_report.md` banner line; CLI output `python -m src.cli signal-stats --asset-class crypto`, "By mode" table, `mode=scalp` row.
- **suggested manual fix:** align the scalp report banner and the CLI signal-stats window (or label both explicitly with their date ranges) so the two don't silently disagree.
- **priority:** low.
- **first observed (this thread):** 2026-08-16 18:49 EEST.
