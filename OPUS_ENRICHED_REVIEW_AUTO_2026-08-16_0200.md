# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

**Crypto overnight / Asia review, run at ~02:00 EEST (nearest fired slot to 04:30; scheduler's Cycle 2/12 was mid-run at execution time).** **Advisory only — no auto-trade.** Headline finding: **17 of 24 currently-open crypto B-tier swing/intraday longs are priced through their recorded stop/invalidation level** (range −0.3% to −49.2%, worst offenders BMT/USDT −49.2%, MUBARAK/USDT −23.9%, BABY/USDT −25.3%, HOLO/USDT −22.9%), yet `PAPER_MONITOR_STATUS_LATEST.md` still shows most of them as `🟢 OPEN — entry filled, monitoring TP/SL (source=legacy touch)` and `proposed_signals.status` is still `triggered`. The `pending_monitor` process logged the **same `PermissionError: [WinError 5] Access is denied` on worker-recycle** that the 2026-08-13 21:40 auto-review flagged — this looks like a recurring, still-unfixed bug, not a one-off. No A-tier anywhere (crypto or stocks). Crypto regime is downtrend/risk-off (BTC downtrend, weak altcoin breadth 30–36% above EMA20, macro risk 88.6/100 driven by Iran/Hormuz tanker incidents + a large BTC Coldcard-wallet exploit, ~1,778–2,055 BTC stolen per Galaxy Research, multi-source corroborated). Stocks are closed (Sunday) — planning-only context. Catalyst mapping is weak this run (66.3% unmapped). This is a risk-manager/operator item first, a new-trade cycle second.

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-15_default_schedule/scheduler.log` — fresh, actively writing through 01:37 EEST; Cycle 2/12 (weekend, crypto-only) started 01:28 EEST and was mid-run (crypto intraday report generating) at review time.
- Latest cycle summary: `cycle_01_22-26_summary.md` (23:28 EEST, ~2.5h old at review start — clears the defer gate).
- Reports: scalp `2026-08-15_22-36` (~3h20m old, used as primary), intraday `2026-08-15_19-41` (~6h stale — Cycle 2's intraday report was regenerating at review time, not yet written; used prior as best-available, flagged stale), swing `2026-08-15_20-23` (~5.5h — carry-forward band).
- Stocks intraday/swing/invest: all >24h old, market closed (Sunday) — planning/context only, not scored fresh.
- Catalysts: `data/catalysts/2026-08-15/catalyst_events.jsonl` (3,776 events) + `narrative_baskets.jsonl` (3 baskets) — this remains the live-dated folder (system runs on UTC date, still Aug 15 UTC at review time).
- LLM packet: `data/processed/llm_analysis_packet.md` (01:37 EEST, fresh).
- CLI: `active-signals` (crypto, stocks), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-16` (clean — no untracked alerts).
- Direct read-only SQL against `db/crypto_ai_desk.sqlite` (`proposed_signals`) for open crypto B-tier stop/invalidation levels — read query only, no writes.
- Direct read of cached OHLCV (`data/raw/ohlcv/binance/15m/*.csv`, last row ~22:30 UTC / ~3h20m stale) to check current price vs. recorded stop for all 24 non-expired open crypto signals.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` and `pending_monitor_1786822025.log` / `pending_monitor_1786832954.log` for lifecycle-status cross-check and monitor-health evidence.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-13_2140.md` (late-session risk review, 2026-08-13 21:40 EEST) — **~2.3 days old, the most recent prior auto-review found**; used for comparison and to confirm the pending_monitor recycle error is recurring, not new.
- **External web research not run this cycle.** The one high-impact external-facing item (BTC Coldcard exploit) is already corroborated across 5+ independent internal sources (CoinMarketCapAnnouncements, whale_alert_io, cryptoquant_official, crypto.news, Bitcoin Magazine) with consistent loss figures — internal-first discipline (§G) judged this sufficient without a fresh WebSearch. No candidate's verdict this cycle depends on unverified external claims.

## 3. Scheduler / Data Freshness

- Scheduler: **fresh**, actively writing.
- Cycle 2/12 in progress at review time (weekend crypto-only mode); crypto scalp report just regenerated (01:37), crypto intraday report was mid-generation — this review used the prior (19:41) intraday report, flagged stale (~6h).
- Swing report ~5.5h old — carry-forward band (4–12h), used with a flag.
- Stocks reports 24h+ old — market closed Sunday, planning-only, not scored fresh.
- **`pending_monitor`: logs a `PermissionError: [WinError 5] Access is denied` on worker-recycle in both the 22:26 and 01:29 sub-cycle logs tonight** — identical signature to the 2026-08-13 21:40 review's finding. It keeps fetching candles every tick (`checked=55 tp=0 stop=0` on all 10 sampled ticks) but is not flagging any of the confirmed stop breaches below.
- Paper monitor status (Telegram, from cycle 1 summary): Open actionable 33 · Waiting for entry 1 · Entered unresolved 4 · Review/Shadow 22 · No-entry/stale/moved-away 109 · Needs review 3 · Closed today 165W/11L/40flat.
- `detect_untracked_legacy_alerts --since 2026-08-16`: **clean**.
- Gap note: the most recent prior `OPUS_ENRICHED_REVIEW_AUTO_*.md` on disk is dated 2026-08-13 21:40 — a ~2.3-day gap in this routine's own output before tonight. Informational only (cause unknown from inside this run); see TODO-3.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-16 02:00 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "bad", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["cycle 2 intraday report (regenerating at review time)", "fresh derivatives snapshot at current price for open swing longs"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log fresh through 01:37 EEST, cycle 2/12 mid-run", "intraday report 19:41 EEST ~6h stale, regen in progress", "swing report 20:23 EEST ~5.5h carry-forward", "pending_monitor PermissionError WinError5 on worker-recycle recurring since at least 2026-08-13"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend on both scalp and swing scans", "ETH range (scalp) / downtrend (swing)", "altcoin breadth 30-36% above EMA20 (weak)", "macro risk 88.6/100 risk-off: Iran/Hormuz tanker incidents, Yemen port halt, BTC Coldcard exploit", "weekend crypto-only cycle mode, stocks closed"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["66.3% of today's 3,776 catalyst events unmapped (2,503/3,776)", "3 active narrative baskets: perps_dex_narrative (HYPE), rwa_narrative (ONDO/XLM), momentum_breakout (HEMI/COW/AKE)", "BTC Coldcard exploit multi-source corroborated ~1,778-2,055 BTC stolen", "SOL/USDT fresh catalyst: Bitwise mulls tokenizing Solana staking ETF via Superstate (The Block)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "squeeze_risk"],
      "data_missing": ["fresh derivatives snapshot for the 17 breached-stop longs at current price"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scalp report derivatives table ~3h20m stale", "several C-tier short candidates (HEI, ROBO, HOME, ACE, ALICE, CASHCAT) capped for thin_liquidity/high_upper_wick short-squeeze risk"] },
    { "agent": "technical_entry", "verdict": "bad", "confidence": 0.85,
      "reason_codes": ["price_moved_away", "stale_before_entry", "overextended"],
      "data_missing": ["TradingView / manual chart check unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["17/24 non-expired open crypto B-tier longs priced through recorded stop/invalidation, worst: BMT/USDT -49.2%, TUT/USDT -66.1% (scalp-vintage stop; swing TUT was correctly flat-closed separately), MUBARAK/USDT -23.9%, BABY/USDT -25.3%, HOLO/USDT -22.9%, HOME/USDT -10.2%, PEOPLE/USDT -13.0%, SAGA/USDT -12.4%", "HEMI/USDT (open long, RS +46% vs BTC) and COW/USDT flagged 'counter-tape long - reduce size' by fresh scans; both currently rejected for fresh entry due to crypto_scalp_disabled kill-switch"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.85,
      "reason_codes": ["open_actionable", "needs_review", "entered_unresolved"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["paper monitor status: open actionable 33, waiting for entry 1, entered unresolved 4, review/shadow 22, no-entry/stale/moved-away 109, needs review 3, closed today 165W/11L/40flat", "PAPER_MONITOR_STATUS_LATEST.md shows BMT/HOLO/LUNA/BABY/HOME/THE/PENGU/MUBARAK/PEOPLE/SAGA/SYN(swing)/DODO all as '🟢 OPEN - entry filled, monitoring TP/SL (source=legacy touch)' despite deep stop breaches computed independently from cached OHLCV", "swing TUT/USDT correctly shows CLOSED FLAT 0R via paper execution (expired_flat) - the paper-execution layer itself works; the legacy-touch status field is what's stale"] },
    { "agent": "risk_manager", "verdict": "bad", "confidence": 0.85,
      "reason_codes": ["manual_review", "reduce_risk", "headline_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["pending_monitor worker-recycle PermissionError (WinError 5) recurring across at least 3 days (2026-08-13 and tonight)", "mass stop-breach-without-closure across legacy-touch tracked swing longs means the displayed 'OPEN' book overstates real risk-adjusted exposure and should not be trusted at face value", "BTC operator-review warning active (Coldcard exploit, block_requires_operator_review) - advisory only, does not gate execution"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["headline A/B week stats: n=152, triggered=150, winrate 21.3%, PF 3.95, avgR 0.53, totalR +59.01", "system self-flagged observation: weekend signals underperform (winrate 22%, n=63)", "0 A-tier signals in the full week sample"] },
    { "agent": "head_trader", "verdict": null, "confidence": null,
      "reason_codes": [], "data_missing": [], "suggested_effect": "advisory_only", "facts_used": [] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.75,
    "preferred_side": "shorts",
    "best_long_candidate":     { "symbol": "HEMI/USDT", "trigger": "pullback into $0.0068-0.0070 (prior breakout shelf) with momentum_breakout basket still active and RS vs BTC holding positive; currently extended and counter-tape, not fresh-actionable now", "reason": "RS leader (+46% vs BTC), catalyst basket primary, but scans reject fresh entries as counter-tape long in a downtrend tape" },
    "best_short_candidate":    { "symbol": "BICO/USDT", "trigger": "failed retest/lower-high below ~$0.0205-0.0210 with derivatives confirmation; thesis already validated (tp1_hit, price has since traded well below tp3)", "reason": "existing short already proved the bearish RS thesis; weak_rs_short expansion-watchlist entry still active (RS -20.6%)" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "confirm follow-through on Bitwise/Superstate staking-ETF tokenization headline (The Block) + RS vs BTC turning positive intraday", "reason": "fresh attention/catalyst detected this cycle, single clean source, no contradicting risk flags" },
    "avoid_candidate":         { "symbol": "BMT/USDT", "reason": "recorded status is stale/unreliable - shown 'OPEN, monitoring TP/SL' while price is 49.2% through its invalidation level; do not use its displayed stop/entry as a live risk reference until the legacy-touch tracking bug is fixed" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | bad | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.75 | risk_off, shorts_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, squeeze_risk | advisory_only |
| technical_entry | bad | 0.85 | price_moved_away, stale_before_entry, overextended | advisory_only |
| execution_lifecycle | manual_review | 0.85 | open_actionable, needs_review, entered_unresolved | advisory_only |
| risk_manager | bad | 0.85 | manual_review, reduce_risk, headline_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, low_sample | advisory_only |
| head_trader | manual_review | 0.75 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-13_2140.md` (late-session risk review, 2026-08-13 21:40 EEST, ~2.3 days ago).

- **Recurring, not resolved:** the `pending_monitor` `PermissionError: [WinError 5]` on worker-recycle that the Aug-13 review flagged is present again tonight — same error signature, same process. That review found 5 specific stop-breach cases (MMT, BICO, ADA×2, PROM, ACE); tonight's independent check found a much larger set (17/24 open longs breached), suggesting the underlying tracking gap has been ongoing and possibly widening, not a one-off.
- Market regime: Aug-13 was range/chop (neutral) with stocks cleanly bullish; tonight crypto is more clearly downtrend/risk-off and stocks are closed (weekend).
- Catalyst mapping: 71.7% unmapped on Aug-13 vs 66.3% unmapped tonight — still weak, marginally better.
- No A-tier then, no A-tier now — consistent.
- New this cycle: BTC Coldcard exploit (~$150M+) as the dominant risk-off macro driver, not present in the Aug-13 review.

## 5. Catalyst Coverage

- Total catalyst events today (`data/catalysts/2026-08-15/catalyst_events.jsonl`): **3,776**.
- Mapped (symbol resolved): **1,273** (33.7%).
- Unmapped (no symbol): **2,503 (66.3%)**.
- Narrative baskets: **3** (`perps_dex_narrative` → HYPE, `rwa_narrative` → ONDO/XLM, `momentum_breakout` → HEMI/COW/AKE).

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top unmapped headlines (sample):
- "$250,000,000 USDC minted at USDC Treasury" (stablecoin flow, no symbol resolver hit)
- "OCC conditionally approved a bank charter for World Liberty Financial" (USD1 stablecoin issuer, unmapped)
- "CFTC reviewing 'mention markets' on prediction platforms" (regulatory, no symbol)
- "Ireland launched first national AML strategy for crypto wallets" (regulatory, no symbol)
- "Trump expected at White House crypto/prediction-market meeting next week" (macro/regulatory, no symbol)

## 6. Market Landscape

- BTC: ~$63,156 (downtrend, both scalp and swing scans agree).
- ETH: ~$1,885 (range per scalp scan, downtrend per swing scan — leaning bearish either way).
- Altcoin breadth above EMA20: 30–36% (weak, confirms narrow/bearish tape).
- Volatility: BTC ATR percentile ~6–7 (normal, not compressed or extreme).
- Stocks: closed (Sunday) — all "signals" in the active list are resolved historical (tp1_hit/tp2_hit) from the prior week; treat as planning-only carry-forward into Monday, not live.

### Market Mood / Risk Routing

- Crypto mood: **risk-off** (BTC/ETH downtrend, weak breadth, macro risk 88.6/100)
- Stocks mood: **closed** (weekend)
- Dominant narrative: momentum_breakout (HEMI/COW/AKE) fighting against a risk-off tape; Coldcard exploit and Iran/Hormuz tensions dominating the macro overlay
- Preferred side now: **shorts, or wait-for-trigger on longs**
- Best long candidate: none clean actionable — HEMI/USDT is the best long-**watch**, but scans reject it as counter-tape and it's currently extended
- Best short candidate: none freshly actionable — BICO/USDT is the best short-**watch**, its short thesis already proved out once (tp1_hit) and price has since fallen well past tp3
- Best catalyst-backed candidate: SOL/USDT (Bitwise/Superstate staking-ETF tokenization headline)
- What to avoid: chasing any of the counter-tape RS-leader longs (HEMI, COW, ETHFI, ENSO) into a downtrend tape; treating any of the 17 breached-stop swing longs as reliable risk references until the legacy-touch tracking bug is fixed
- What would change the view: BTC reclaiming and holding above its local range highs, or a clean pullback-and-hold on the RS leaders that would validate a counter-tape long with tighter risk

## 7. Candidate Deep Dives

### 1. System-integrity: mass stop-breach without closure (legacy-touch tracking)

- **Not a trade idea — an operational risk finding.** Independently checked all 24 non-expired open crypto B-tier `proposed_signals` (status `triggered`/`tp1_hit`/`tp2_hit`) against last cached 15m close (~22:30 UTC, ~3h20m stale but internally consistent, no data-glitch/wrong-symbol jump found on spot-check of BMT and TUT price history).
- 17/24 are priced through their recorded `stop_loss`/`invalidation`: AVNT −0.6%, PUMP −4.8%, PROM −7.6%, HOLO −22.9%, LUNA −5.0%, BABY −25.3%, HOME −10.2%, TST −16.6%, PENGU −6.3%, THE −3.2%, MUBARAK −23.9%, BMT −49.2%, PEOPLE −13.0%, TUT −66.1% (scalp-vintage entry; the separate swing TUT signal was correctly flat-closed), SAGA −12.4%, SYN −0.3%, DODO −2.9%.
- Cross-checked against `PAPER_MONITOR_STATUS_LATEST.md`: most of these (BMT, HOLO, LUNA, BABY, HOME, THE, PENGU, MUBARAK, PEOPLE, SAGA, SYN-swing, DODO) are shown `🟢 OPEN — entry filled, monitoring TP/SL (source=legacy touch)` — the human-facing status disagrees with price by double digits in several cases.
- The `paper execution` layer itself (separate from `legacy touch`) is working correctly elsewhere in the same report (e.g. swing TUT closed flat via `expired_flat`, several scalp/intraday positions closed win via `profit_lock_stop`) — this narrows the bug to the `legacy touch` status path specifically, likely tied to the `pending_monitor` worker-recycle `PermissionError`.
- **Do not treat the displayed "open" book as an accurate live risk picture until this is fixed.** See TODO-1.

### 2. HEMI/USDT — best long-watch, not actionable now

- Currently an **open B-tier intraday long** (`sig_8796f24580a84cc2`, triggered, entry ~0.0065–0.0068, stop 0.006167, expires 2026-08-16T19:49). Current price ~$0.0072, +16.8% clear of stop — one of the few genuinely healthy open positions tonight.
- RS vs BTC +46.3%, top strongest symbol both scalp and swing scans, `momentum_breakout` narrative basket primary.
- Fresh scans (this cycle) explicitly **reject** new HEMI longs: "counter-tape long — reduce size", "Relative-strength leader long against a bearish tape — reduce size and demand confirmation", plus `crypto_scalp_disabled` kill-switch on the scalp mode.
- Price already reacted (46% 24h move) — chasing now would be late; the existing open position is fine, but a *fresh* entry is not clean.
- Actionable only after: a pullback into the $0.0068–0.0070 shelf that holds, with the basket still active and BTC stabilizing.
- Invalidation: RS vs BTC turning negative, or basket losing its primary tag.

### 3. BICO/USDT — best short-watch

- Existing B-tier intraday short (`sig_c3dc07c440c55626`) already hit tp1 and current price (~$0.0202) is well past tp3 (~$0.0277) — the short thesis was strongly validated, though the signal's own expiry window (2026-08-12) has passed, so it now reads as entered-unresolved/expired-in-profit rather than a live tracked position.
- Still flagged `weak_rs_short` on the current expansion watchlist (RS vs BTC −20.6%, score 74) — the underlying weakness thesis is still current.
- Chase risk: entering fresh here without a bounce/retest would be chasing an already-large move.
- Actionable only after: a failed bounce / lower-high forms with anchor-exchange + derivatives confirmation (currently missing — anchor-listed but no derivatives confirmation per Multi-Exchange Confirmation table).
- Invalidation: a reclaim and hold above the prior swing high.

### 4. SOL/USDT — best catalyst-backed watch

- Fresh catalyst this cycle: "Bitwise mulls tokenizing its Solana staking ETF via Superstate partnership" (The Block) — single clean source, no contradicting risk flags in tonight's news scan.
- Not in the current top-8 strongest/weakest symbol lists, no fused/deep-analysis signal generated tonight — this is a catalyst-only lead, not yet technically confirmed.
- Has price already reacted? Not verifiable tonight (SOL wasn't in the deep-analysis set) — treat as unconfirmed.
- Actionable only after: SOL/USDT shows up in a fresh scan with RS vs BTC turning positive and an entry structure on 15m–1h, per the standard catalyst-promotion rule.
- Invalidation: no technical confirmation within the next 1–2 cycles, or the catalyst is denied/walked back.

### 5. BTC/USDT — avoid / macro risk context

- Not a trade idea — the dominant risk-off driver tonight. Galaxy Research: ~1,778–2,055 BTC (~$113–150M+) stolen in a Coldcard seed-recreation exploit across 3+ waves, corroborated across 5 independent sources (CoinMarketCapAnnouncements, whale_alert_io, cryptoquant_official, crypto.news, Bitcoin Magazine) with converging loss figures.
- `block_requires_operator_review` risk flag is active on BTC (advisory/display only — does not gate routing or execution).
- Combined with Iran/Hormuz tanker incidents and a Yemen port halt, this is driving the 88.6/100 macro risk-off score that underlies tonight's short-bias market-mood call.
- Note: BTC ETF flows reportedly still net positive despite the exploit headline (per one cited source) — mixed signal, not a clean "BTC is breaking down" narrative, just elevated headline risk.

## 8. Best Candidates Ranked

No clean actionable trade tonight (no A-tier, no fresh B-tier triggers, weekend/thin liquidity). Routed per PART 9:

1. **Long-watch:** HEMI/USDT — trigger: pullback into $0.0068–0.0070 holding, basket + BTC stabilization confirming.
2. **Short-watch:** BICO/USDT — trigger: failed bounce/lower-high with derivatives confirmation.
3. **Catalyst-watch:** SOL/USDT — trigger: technical confirmation (fresh scan entry + positive RS vs BTC) on the Bitwise/Superstate headline.
4. **Avoid:** BMT/USDT (and the other 16 stop-breached longs listed in §7.1) — displayed status is unreliable until the legacy-touch tracking bug is fixed; do not size or hedge against these levels.

## 9. Avoid / No Trade

This is a decision-window call only — scanning, tracking, and the scheduler continue as normal.

- Avoid chasing counter-tape RS-leader longs (HEMI, COW, ETHFI, ENSO, CHIP) into a confirmed downtrend tape without a pullback/hold.
- Avoid treating any of the 17 stop-breached "OPEN" swing/intraday longs (§7.1) as valid risk references — their displayed entry/stop/status may be stale.
- Avoid fresh short entries on thin-liquidity C-tier names capped for squeeze risk (HEI, ROBO, HOME, ACE, ALICE, CASHCAT) without confirmation — high_upper_wick / thin_liquidity flags are active on all of them tonight.
- Stocks: closed, no action — Monday pre-market context should be rebuilt fresh, not carried forward from Friday's stale reports.

## 10. Main Risks

- **Legacy-touch tracking gap** (§7.1): the displayed "open" book likely overstates real exposure quality; a human should verify actual live risk before treating any of these 17 positions as a hedge reference.
- **`pending_monitor` worker-recycle failure** recurring across ≥3 days — if this is silently degrading other monitor functions beyond stop-detection, the blast radius could be wider than currently visible.
- Macro/geopolitical: Iran/Hormuz tanker incidents are live and could produce a fast risk-off gap over the weekend with thin liquidity.
- BTC Coldcard exploit: headline risk elevated; watch for further wallet-drain updates that could extend the sell pressure narrative.
- Catalyst mapping weak (66.3% unmapped) — treat the catalyst layer as context, not a decision driver, tonight.

## 11. Action Plan — next 4 hours

- Monitor BTC/ETH for any break of the current range as Asia session progresses; downside break would confirm short-bias, a reclaim of local resistance would open the door to the HEMI pullback-long thesis.
- Watch for SOL/USDT to appear in the next fresh scan (intraday/scalp) with technical confirmation on the staking-ETF catalyst.
- No fresh crypto entries recommended until either (a) a clean retest/pullback structure forms on a leader, or (b) the legacy-touch tracking issue is confirmed fixed by a human session.
- Stocks: no action, market closed; rebuild watchlist fresh at Monday pre-market.

## 12. Final Verdict per Mode

- **Scalp:** No trade (system's own conclusion this cycle — "Data does not justify a fresh idea right now"). Agrees with this review.
- **Intraday:** No trade — no A/B setups in the last-available (stale, ~6h) report; fresh cycle-2 intraday report was still generating at review time.
- **Swing:** No new trade — no A/B setups fresh this cycle; existing open swing book needs manual review per §7.1/§9 before being treated as reliable.
- **Stocks (intraday/swing/invest):** Market closed — no verdict, planning-only.

## 13. Sources

- Internal: `data/reports/scalp/2026-08-15_22-36_scalp_report.md`, `data/reports/intraday/2026-08-15_19-41_intraday_report.md`, `data/reports/swing/2026-08-15_20-23_swing_report.md`
- Internal: `data/catalysts/2026-08-15/catalyst_events.jsonl`, `narrative_baskets.jsonl`
- Internal: `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items`, read-only)
- Internal: `data/raw/ohlcv/binance/15m/*.csv` (cached, ~22:30 UTC 2026-08-15)
- Internal: `reports/PAPER_MONITOR_STATUS_LATEST.md`
- Internal: `data/scheduled_runs/2026-08-15_default_schedule/pending_monitor_1786822025.log`, `pending_monitor_1786832954.log`, `scheduler.log`
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-13_2140.md`

**BTC Coldcard exploit (multi-source, 2026-08-14/15):**
- [UPDATE: Galaxy Research says over 1,778 BTC has been stolen in the Coldcard exploit](https://t.me/CoinMarketCapAnnouncements/15222) — CoinMarketCapAnnouncements (t.me), 2026-08-15
- [Galaxy says Coldcard seed-recreation exploit has drained over 1,778 BTC](https://t.me/whale_alert_io/102456) — whale_alert_io (t.me), 2026-08-14
- [Coldcard Bitcoin Thefts Slow, But Losses Could Top $150 Million: Galaxy](https://decrypt.co/375656/coldcard-bitcoin-thefts-slow-losses-top-150-million) — Decrypt, 2026-08-14
- [Coldcard wallet exploit leads to theft of over 1,778 Bitcoin worth $112M](https://cryptobriefing.com/coldcard-wallet-exploit-bitcoin-theft-112m/) — CryptoBriefing, 2026-08-14

**SOL/USDT catalyst-watch (2026-08-14):**
- [Bitwise is exploring putting its Solana staking ETF on-chain, partnering with Superstate](https://t.me/CoinMarketCapAnnouncements/15185) — CoinMarketCapAnnouncements (t.me), 2026-08-14
- [Bitwise partners with Superstate to explore tokenizing Solana staking ETF](https://cryptobriefing.com/bitwise-superstate-tokenize-solana-etf/) — CryptoBriefing, 2026-08-14

**Other stocks/crypto legal & regulatory (context, not this cycle's candidates):**
- [OCC grants conditional approval for Trump-backed World Liberty National Trust bank](https://www.theblock.co/news/regulation/2026-08-14-occ-grants-conditional-approval-trump-world-liberty-national-trust-bank-411906) — The Block, 2026-08-14
- [Trump, CFTC Chair Selig expected at Wednesday White House meeting with crypto and prediction market executives](https://www.theblock.co/news/regulation/2026-08-15-trump-cftc-chair-selig-expected-at-wednesday-white-house-meeting-with-crypto-and-prediction-market-executives-411919) — The Block, 2026-08-15

All URLs above were already present in the internal `news_items` table (ingested by the standing news pipeline before this review ran) — no fresh WebSearch/WebFetch was performed this cycle (see §2), so no new rows were written via `scripts.ingest_enriched_review_sources` (nothing new to ingest).

## 14. Fix Requests / TODO

### TODO-1: legacy-touch position tracking not detecting large stop breaches
- **issue:** 17/24 open crypto B-tier `proposed_signals` (status `triggered`/`tp1_hit`) are priced through their recorded `stop_loss`/`invalidation` by −0.3% to −49.2%, but `PAPER_MONITOR_STATUS_LATEST.md` still shows most of them (BMT, HOLO, LUNA, BABY, HOME, THE, PENGU, MUBARAK, PEOPLE, SAGA, SYN-swing, DODO) as `🟢 OPEN — entry filled, monitoring TP/SL (source=legacy touch)`. The separate `paper execution` closure path works correctly on other positions in the same report (e.g. swing TUT correctly closed flat via `expired_flat`), so the defect appears isolated to the `legacy touch` status-update path.
- **evidence:** `db/crypto_ai_desk.sqlite` `proposed_signals` query (24 open crypto rows, stop/invalidation columns) cross-checked against `data/raw/ohlcv/binance/15m/{SYMBOL}.csv` last close (~2026-08-15 22:30 UTC), then cross-checked against `reports/PAPER_MONITOR_STATUS_LATEST.md`. Worst cases: BMT/USDT stop 0.029802 vs price 0.01515 (−49.2%), TUT/USDT (scalp vintage) stop 0.09882 vs price 0.03346 (−66.1%), MUBARAK/USDT stop 0.020892 vs price 0.01589 (−23.9%).
- **suggested manual fix:** investigate the `legacy touch` status-update path in the pending/position monitor; check whether it's tied to the `pending_monitor` worker-recycle `PermissionError: [WinError 5]` (see TODO-2) — the recycle failure may be silently halting the stop-check subroutine while candle-fetching continues (`checked=55 tp=0 stop=0` every tick despite confirmed breaches).
- **priority:** high
- **first observed (this thread of evidence):** 2026-08-13 21:40 EEST (prior auto-review, 5 cases); confirmed still present and much larger tonight, 2026-08-16 02:00 EEST (17 cases).

### TODO-2: `pending_monitor` worker-recycle PermissionError recurring
- **issue:** `pending_monitor` logs `pending-monitor recycle failed: PermissionError: [WinError 5] Access is denied` at the end of its sub-cycle log, at least on 2026-08-13 and again tonight (2026-08-16). Candle-fetching continues afterward, but this may be the root cause of TODO-1.
- **evidence:** `data/scheduled_runs/2026-08-15_default_schedule/pending_monitor_1786822025.log` and `pending_monitor_1786832954.log`, final lines: `pending-monitor rotating worker memory` → `pending-monitor recycle failed: PermissionError: [WinError 5] Access is denied`. Same signature reported in `OPUS_ENRICHED_REVIEW_AUTO_2026-08-13_2140.md` §3.
- **suggested manual fix:** identify what file/handle the worker-recycle step is trying to access on Windows and why it's permission-denied (likely a log file or lock file still held by the previous worker process); consider whether this needs a retry-with-backoff or a different recycle strategy on Windows.
- **priority:** high
- **first observed:** 2026-08-13 (prior review); still present 2026-08-16 02:00 EEST.

### TODO-3: ~2.3-day gap in this review routine's own output
- **issue:** the most recent `OPUS_ENRICHED_REVIEW_AUTO_*.md` found on disk before tonight's run was dated 2026-08-13 21:40 EEST — no auto-review output for roughly 2.3 days despite this being a 6x/day scheduled routine.
- **evidence:** `ls -t OPUS_ENRICHED_REVIEW_AUTO_*.md` — most recent prior file is `OPUS_ENRICHED_REVIEW_AUTO_2026-08-13_2140.md`.
- **suggested manual fix:** check whether the scheduled task(s) driving this routine (`opus-enriched-review-4h` and siblings) were paused, erroring silently, or intentionally disabled during this window; this run cannot see its own scheduler-side history to diagnose further.
- **priority:** medium
- **first observed:** 2026-08-16 02:00 EEST (this run).
