# Opus Enriched Review — Late-session risk review — Auto Cycle 21:40 EEST

## 1. Executive Summary

**Slot: late-session risk review (advisory only / no auto-trade).** Today is **Saturday** — US cash equities are closed all day; stocks carry forward as planning-only, crypto is the only live-actionable class this window. Scheduler is fresh (`scheduler.log` 21:39 EEST, ~1m old — no defer). Crypto scalp (19:58 EEST gen), intraday (20:17 EEST gen), and swing (21:32 EEST gen) are all fresh; **no A-tier and no B-tier fresh setups fired in any of the three reports this cycle** — everything new is C-tier/watchlist only. The live book itself, however, is not empty: **52 previously-triggered crypto B-tier positions remain open (unexpired)**, and it is **100% long, zero shorts armed**. This review's central finding **generalizes and escalates** the TUT/USDT invalidation-breach TODO first raised at 18:40 EEST: cross-checking `signal_outcomes` against live exchange prices shows the note `"candles=0"` (meaning the outcome-tracker fetched zero fresh OHLCV candles for that check) attached to **78 of 88 (89%)** of today's open/recent proposed-signal rows, and it is not cosmetic — three symbols show **confirmed, independently-verified hard breaches**: `TUT/USDT` (current 0.03415 vs invalidation 0.050579, **~32% through its own stop**, worse than the ~26% found three hours ago), `RUNE/USDT` (current 0.4650 vs stop_loss 0.5342, **~13% through stop**), and `WLD/USDT` (two open longs, current 0.3763 vs stop_loss 0.40049/0.40621, **~6–7% through stop**) — all three still display `status=triggered`, not `stopped`. On the profit side, `PROM/USDT` (current ~6.58 vs tp3=5.188, entered 2026-08-27 at 4.28-4.38) and two `ONT/USDT` entries (current ~0.0576 vs their tp1≈0.0548–0.0555) have clearly cleared their take-profits without the status field updating. Macro risk remains elevated (85–100/100 depending on report, Iran/Strait-of-Hormuz + Fed Warsh sticky-inflation headlines). Catalyst mapping is weak this run (**57.8% unmapped**). A third instance of the untracked-legacy-alert bug fired today (`DEXE/USDT`, sent 14:36:42 UTC). Scanning, tracking, and the scheduler continue unmodified regardless of this window's verdict.

## 2. Data Used

- Crypto scalp report: `data/reports/scalp/2026-08-29_16-59_scalp_report.md` (generated 19:58:28 EEST, data freshness 16:45 UTC — **fresh**; "No trade" final summary)
- Crypto intraday report: `data/reports/intraday/2026-08-29_17-18_intraday_report.md` (generated 20:17:32 EEST, data freshness 17:00 UTC — **fresh**; best watchlist ZKP/USDT 63.6/100)
- Crypto swing report: `data/reports/swing/2026-08-29_18-32_swing_report.md` (generated 21:32:07 EEST, data freshness 18:15 UTC — **fresh**; best watchlist GIGGLE/USDT 64.5/100)
- Stocks intraday report: `data/reports/stocks/intraday/2026-08-28_18-54_stocks_intraday_report.md` (~27h old — **stale**, expected: no weekend stocks cycle; planning-only)
- Stocks swing/invest reports: both dated 2026-07-02 — deprecated pipeline per `project_crypto_ai_desk_stocks_position_framework` memory, excluded
- `data/catalysts/2026-08-29/catalyst_events.jsonl` (2,579 rows counted today: 1,089 mapped / 1,490 unmapped), `narrative_baskets.jsonl`, `catalyst_cycle_17-29.md` (latest cycle, 20:29 EEST, ~1h11m old)
- CLI/DB reads: `active-signals --asset-class crypto` (50 rows shown, truncated columns — cross-checked directly against `db/crypto_ai_desk.sqlite` `proposed_signals`/`signal_outcomes` tables for full precision), `active-signals --asset-class stocks` (all rows historical/expired, 0 live), `signal-stats --asset-class crypto` (n=349 reliable, tier B, winrate 11.85%, PF 1.20, avgR 0.051), `detect_untracked_legacy_alerts --since 2026-08-29` (1 alert: DEXE/USDT)
- Direct SQL reads (read-only) against `proposed_signals` and `signal_outcomes` for asset_class=crypto/stocks, filtered to `expires_at > now` and non-terminal status, to get unrounded entry/stop/TP values the CLI table truncates
- Live spot prices cross-checked via public Binance ticker (`api.binance.com/api/v3/ticker/24hr`) for BTC, ETH, DOGE, SOL, COTI, NIL, BANK, ZKP, ONT, RUNE, PROM, TAO, ENA, TUT, HEMI, MOVR, ROBO, BNB, ASTER, WLD — used only to verify internal stop/TP status against real-time price, not as a new data source for scoring
- Latest scheduler cycle summary: `data/scheduled_runs/2026-08-29_default_schedule/cycle_01_16-03_summary.md` (mtime 17:48 EEST; `scheduler.log` itself is fresher at 21:39 EEST, confirming the scheduler process is alive between cycle-summary writes)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-29_1840.md` (US open reaction slot, 18:40 EEST — collapsed to crypto-only due to Saturday)
- **External web research not used this run** — the central finding (outcome-tracking gap) is a direct internal DB-vs-live-price comparison; no candidate's verdict depended on unverified external claims.
- **TradingView / manual chart check unavailable** — all technical reads taken from report-stated OHLCV/ATR/EMA/RS/funding/OI/current-price fields plus the live ticker cross-check above.

## 3. Scheduler / Data Freshness

- `scheduler.log`: 2026-08-29 21:39 EEST (~1m old) — **fresh**, no defer.
- Latest `cycle_01_16-03_summary.md`: mtime 17:48 EEST (~3h52m old) — older, but `scheduler.log` freshness alone clears the defer bar per the routine's rule (defer only if BOTH are >3h stale).
- Crypto scalp/intraday/swing: all generated within the last ~2h, data-as-of within the last ~5h — **fresh**.
- Stocks intraday: ~27h old — **stale but expected**; no stocks cycle runs on a Saturday. Stocks swing/invest: 2026-07-02, deprecated/excluded per memory.
- **New this cycle — execution-lifecycle data-integrity gap:** of 88 open/recently-open crypto proposed-signal rows (`expires_at` in the past or future, tier A/B, non-terminal `proposed_signals.status`), the latest `signal_outcomes` row for **78 (89%)** carries `notes` containing `"candles=0"` — i.e., the outcome-checker's OHLCV fetch returned zero candles on its most recent pass, meaning stop/TP touches cannot be detected for those rows going forward until the feed recovers. This is not evenly distributed by symbol age — it affects rows from same-day (`ZKP/USDT`, created 17:03 EEST today) is one of the few *without* the flag, but most rows created 3–7 days ago (RUNE, PROM, ONT, TUT, WLD, TAO, SPK, ZEC, and 20+ others) do carry it consistently across repeated checks.
- Monitor cadence: per prior cycle's summary, crypto watchlist monitor (5m), crypto pending monitor (30s/45s), derivatives monitor, and fast news monitor all reported "already running" as of the last full cycle write — background processes appear alive; the gap is specifically in the OHLCV candle fetch step of the outcome-checker, not in whether the checker runs (it clearly runs — `checked_at` timestamps are current, some rows checked twice within 19 seconds of each other, itself worth a lower-priority note in §14).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-08-29 21:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "derivatives_sparse"],
      "data_missing": ["OHLCV candle feed powering the outcome-checker is returning zero candles for 89% of open crypto proposed-signal rows on its latest pass"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~1m old, no defer", "scalp/intraday/swing all fresh (data as-of within 5h)", "78/88 open crypto signal_outcomes rows carry notes containing candles=0", "stocks intraday ~27h old but expected (Saturday, no cycle)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chop", "risk_off", "mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH both trend range across all three timeframes", "macro/geopolitical risk 85.3-100/100 depending on report (Iran Strait-of-Hormuz dispute, Fed Chair Warsh sticky-inflation remarks, Coldcard exploit ~2,055 BTC)", "altcoin breadth 47.5%/67.5% above EMA20/50 — mixed, not trending", "live crypto book remains 100% long, 0 shorts armed across 52 open positions"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["57.8% unmapped in catalyst_events.jsonl today (1,490/2,579)", "5 active narrative baskets this cycle: momentum_breakout (PROM/GIGGLE/NIL, fresh<1h), ai_narrative, rwa_narrative, binance_ecosystem_teaser, perps_dex_narrative", "ENA/USDT token-unlock buyback catalyst is fresh but the open ENA/USDT long predates it and carries the same candles=0 tracking gap", "PROM/GIGGLE/NIL/COTI/ZKP rally cluster has no verified fresh catalyst — pure momentum, all watchlist-only in every report"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "funding_extreme", "oi_contradicts"],
      "data_missing": ["bybit_okx derivatives partial for several strongest symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/USDT negative funding across bybit(-0.008)/mexc(-0.0014) through a +9-14% rally — squeeze-not-trend signature, consistent across scalp/intraday/swing reports", "TUT/USDT extreme negative funding (bybit -0.0036 to -0.0042, mexc -0.004 to -0.0046) sitting under an open long that is deeply through its own stop — crowded shorts against an already-broken long is a genuine two-sided risk pocket", "ONG/USDT persistent negative funding through a +7-16% rally across all three reports — same squeeze framing as the 18:40 review"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "stale_before_entry", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM/GIGGLE/DASH/ZEC/ADA all explicitly rejected in 7b sections for 'more than 2 ATR from EMA20; do not chase'", "ZKP/USDT scalp position (triggered 17:03 EEST) expires 19:03 EEST — ~1h38m past expiry as of this write-up if unresolved, needs lifecycle check, not a fresh entry", "DOGE/USDT swing waiting_for_entry (0.092952-0.093878) expires 21:04:58 EEST — expired or expiring within minutes of this review with no confirmed fill; live price 0.08532 never reached the zone", "RE/USDT-style clean unfilled zones were absent from this cycle's active list (RE/USDT's own row is currently `waiting_for_entry`, unchanged, but its underlying report context is 4+ days old)"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.85,
      "reason_codes": ["entered_unresolved", "needs_review", "open_actionable", "waiting_for_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["52 open (unexpired) crypto B-tier positions, all long, 0 shorts", "CONFIRMED hard stop breaches not reflected in status: TUT/USDT (0.03415 vs invalidation 0.050579, ~32% through), RUNE/USDT (0.4650 vs stop 0.5342, ~13% through), WLD/USDT x2 (0.3763 vs stop 0.40049/0.40621, ~6-7% through) — all still show status=triggered", "CONFIRMED missed take-profits not reflected in status: PROM/USDT (~6.58 vs tp3 5.188, entered at 4.28-4.38), ONT/USDT x2 (~0.0576 vs tp1 0.05484/0.05548) — still show status=triggered", "78/88 (89%) open signal_outcomes rows carry candles=0 in their latest check note", "DOGE/USDT waiting_for_entry expires 21:04:58 EEST, at or past expiry as of this review with no fill", "ZKP/USDT scalp triggered 17:03 EEST, 2h validity window (expires 19:03 EEST) — past its own window as of this write-up, unresolved", "3rd untracked-legacy-alert instance today: DEXE/USDT swing long, score 65.0, sent 14:36:42 UTC, no matching proposed_signal"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.8,
      "reason_codes": ["correlation_cluster", "reduce_risk", "manual_review", "repeated_losses"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["100% long book (52 open, 0 shorts) against elevated macro risk-off (85-100/100) into the weekend, when liquidity is typically thinner and gaps on reopen are more likely", "TUT/USDT and RUNE/USDT are open longs trading materially below their own invalidation and have been for multiple review cycles without reconciliation — real (paper) risk exposure is being systematically understated on the dashboard", "WLD/USDT (x2) adds a second, independently-confirmed symbol to the same breach pattern — this is not a single-symbol anomaly, it is a book-wide tracking gap", "recurring untracked-alert bug (3rd instance, same DEXE/USDT-pattern as 18:40 review) continues unresolved"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["low_sample", "playbook_working", "playbook_failing"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto tier B headline (n=349, reliable): triggered=329, wins=39/losses=111, winrate 11.85%, PF 1.20, avgR 0.051 — thin edge, consistent with recent cycles", "weekend-mode signals structurally weaker than regular-mode per prior cycle's stats (13% vs higher regular winrate) — most of today's open book was generated on a Saturday", "crypto swing is the primary mode carrying PF (per by-mode table, mode with n=120 shows PF~1.5) vs scalp-like mode near PF~0 — consistent with known 'scalp entry-edge, TP-horizon mismatch' finding in the scalp report's own header warning"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.75,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.75,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "NIL/USDT", "trigger": "already triggered (swing, entry 0.052362-0.053898, current 0.05735) and holding above entry with RS vs BTC +14%; treat any add as chasing — the actionable trigger for anyone flat is a pullback into 0.0536-0.0557 on falling volume, not a fresh breakout chase", "reason": "the cleanest RS-leader long in the current book that is not already deeply extended past 2 ATR (unlike PROM/GIGGLE) and does not carry a confirmed tracking-integrity problem" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "no fresh short entry — the desk's own prior 0.0378-0.0386 failed-bounce watch zone has already been broken to the downside (current 0.03415); a fresh short now would be chasing a move that has run ~10% past the original watch trigger. Wait for a retest of 0.0378-0.0386 from below (as resistance) before considering a fresh short; funding remains extreme-negative (crowded), so treat any bounce-fade as squeeze-prone, not a chase", "reason": "still the cleanest bearish structural read in the book, but the entry window described three hours ago is now stale — this is a watch-for-retest, not an active trigger" },
    "best_catalyst_candidate": { "symbol": "none", "trigger": "would need a second independent source confirming continued binance_ecosystem_teaser (BNB/ASTER) or perps_dex_narrative (HYPE) basket strength before treating narrative heat as a fresh entry", "reason": "PROM/GIGGLE/NIL/COTI rally cluster has no verified catalyst behind it (pure momentum) and existing catalyst-tagged names (BNB, ASTER) already have open exposure or unresolved tracking status" },
    "avoid_candidate":         { "symbol": "PROM/USDT", "reason": "existing open long already blew through tp1/tp2/tp3 (current ~6.58 vs tp3 5.188) without status updating — a fresh add here would be chasing a move that is +54% beyond its own original entry zone (4.28-4.38) and every report this cycle explicitly rejects it for being >2 ATR from EMA20" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, derivatives_sparse | advisory_only |
| market_regime | caution | 0.60 | chop, risk_off, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, funding_extreme, oi_contradicts | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, stale_before_entry, entry_late | advisory_only |
| execution_lifecycle | needs_review | 0.85 | entered_unresolved, needs_review, open_actionable, waiting_for_entry | advisory_only |
| risk_manager | manual_review | 0.80 | correlation_cluster, reduce_risk, manual_review, repeated_losses | advisory_only |
| playbook_performance | caution | 0.60 | low_sample, playbook_working, playbook_failing | advisory_only |
| head_trader | manual_review | 0.75 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

(vs `OPUS_ENRICHED_REVIEW_AUTO_2026-08-29_1840.md`, 18:40 EEST US-open-reaction slot)

- **Escalated, generalized:** the 18:40 review confirmed a single hard finding — `TUT/USDT`'s invalidation breach (~26% through stop). This review re-checked TUT/USDT (now **~32% through**, price fell further to 0.03415 from 0.0374) and, by systematically cross-checking `signal_outcomes.notes` for `candles=0` against live prices, found the **same pattern independently confirmed on two more symbols**: `RUNE/USDT` (~13% through its stop) and `WLD/USDT` (two open longs, ~6-7% through stop each). It is no longer reasonable to treat this as a single-symbol tracking glitch — **89% of open crypto proposed-signal rows (78/88) carry the `candles=0` note**, and take-profit misses were also found (`PROM/USDT` past tp3, `ONT/USDT` x2 past tp1).
- **New:** `DOGE/USDT` (`waiting_for_entry`, zone 0.092952-0.093878) expires 21:04:58 EEST — at or just past expiry as of this review, with live price (0.08532) never having reached the zone; this closes out as a clean no-entry/stale case, not a tracking problem.
- **New:** `ZKP/USDT` scalp (triggered 17:03 EEST, 2h window, expires 19:03 EEST) is past its own validity window as of this write-up with no visible resolution in the CLI snapshot — worth a lifecycle check alongside the broader candles=0 finding, though scalp positions expiring unresolved is a known, separately-documented pattern (see the scalp report's own header note on TP1/TP2-vs-2h-horizon mismatch).
- **Same, unresolved:** the `DEXE/USDT` untracked-alert bug (18:40 review) is a *different* DEXE/USDT alert than the one seen at 16:05 — this makes at least 3 distinct untracked-alert instances across today's cycles, all matching the escalated `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug` pattern.
- **Macro:** risk score sits in the 85.3–100/100 range across the three reports (intraday reads highest at 99.9/100, driven by the Coldcard exploit + Iran headlines); broadly consistent with the 18:40 review's 94.4/100, i.e. still sharply risk-off, not receding.
- **Catalyst mapping:** 57.8% unmapped today (cumulative), comparable to 58.0% at 18:40 — flat, still above the 50% weak-mapping threshold.
- **Book composition:** still 100% long / 0 shorts across the crypto swing book — unchanged concentration risk profile from 18:40, now compounded by the wider tracking-gap finding.

## 5. Catalyst Coverage

- Total `catalyst_events` today (direct JSONL count, cumulative across all cycles): **2,579**
- Mapped (non-null symbol): **1,089**
- Unmapped (null symbol): **1,490** (**57.8%**)
- `narrative_baskets` count: **5** this cycle (momentum_breakout/PROM+GIGGLE+NIL fresh<1h; ai_narrative/NEAR+RENDER+TAO+FET; rwa_narrative/ONDO+XLM; binance_ecosystem_teaser/BNB; perps_dex_narrative/HYPE)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top unmapped-symbol headlines this cycle are macro/security/legal, not single-asset: "Elon Musk settles SEC lawsuit over Twitter disclosures, $1.5 million fine imposed"; "BABA Investors Have Opportunity to Lead Alibaba Group Holding Limited Securities Fraud Lawsuit"; "BZAI Investors Have Opportunity to Lead Blaize Holdings Securities Fraud Lawsuit"; "Swiss wealth managers urge delay to ownership register after Liechtenstein hack".

## 6. Market Landscape

BTC and ETH both trend "range" across all three fresh reports; altcoin breadth sits at a middling 47.5%/67.5% above EMA20/50 — not a clean directional tape. Macro risk remains elevated and, if anything, slightly worse on the intraday read (99.9/100) than the swing read (85.3/100), driven by the Coldcard hardware-wallet exploit (up to 2,055 BTC estimated stolen, offset partly by ~$800M in fresh ETF inflows) and ongoing Iran/Strait-of-Hormuz rhetoric plus Fed Chair Warsh's sticky-inflation remarks. The PROM/GIGGLE/NIL/COTI/ZKP cluster is the standout mover (24h returns 9-37%) but every report explicitly rejects fresh entries into it for being more than 2 ATR from EMA20 — a momentum move without a verified catalyst, not a clean setup. Weekend liquidity and the elevated macro backdrop argue for caution on the long-only book heading into the Asia session.

### Market Mood / Risk Routing
- Crypto mood:           chop with a persistent risk-off macro overlay (85-100/100 depending on report)
- Stocks mood:           closed (Saturday — no cash session; planning-only for Monday)
- Dominant narrative:    momentum_breakout (PROM/GIGGLE/NIL, fresh <1h) — pure price momentum, no verified catalyst backing any of the three
- Preferred side now:    wait-for-trigger, with a bias toward risk reduction/reconciliation over adding — the long-only book's real exposure is understated by the tracking gap described in §3/§14
- Best long candidate:   NIL/USDT — already triggered and holding gains; a fresh add should wait for a pullback into 0.0536-0.0557, not chase the current print
- Best short candidate:  TUT/USDT — watch-for-retest only; the earlier 0.0378-0.0386 zone is now stale (price broke below it); wait for a retest from underneath before considering a fresh short, funding still extreme-negative
- Best catalyst-backed candidate: none clean this cycle — momentum cluster has no verified catalyst; BNB/ASTER and HYPE baskets already have open exposure or need independent confirmation
- What to avoid:         adding to PROM/USDT, GIGGLE/USDT, or any >2-ATR-extended name; treating TUT/USDT's stale watch zone as still live; assuming the "triggered" status on any position older than ~2 days is accurate without a manual price check
- What would change the view: macro risk score receding toward 60-70; the outcome-tracker's OHLCV feed recovering (candles>0 on repeat checks) and status fields reconciling to reflect true price vs stop/TP; BTC/ETH breaking range with confirming breadth expansion

## 7. Candidate Deep Dives

### TUT/USDT (crypto, swing, B-tier, status=triggered — open long, invalidation breach worsening)
- Catalyst: none mapped — pure technical/lifecycle issue, no news driving either side this cycle.
- Has price reacted? Yes, severely and further — live price 0.03415 (Binance, -13.5% 24h) vs entry zone 0.051638-0.052505 and invalidation 0.050579. The gap widened from ~26% through stop (18:40 review) to **~32% through stop** now.
- Is this a chase-risk setup for a fresh short? Yes if forced — funding remains extreme-negative (bybit/mexc both deeply negative per the swing report), meaning shorts are crowded and a squeeze bounce is a live risk.
- Actionable level for a fresh short: the previously-cited 0.0378-0.0386 watch zone is now **stale** — price has broken below it. Wait for a retest of that zone from underneath (as resistance) before considering entry; do not chase the current print.
- Mood alignment: bearish bias aligns with the broader risk-off mood, but the open position itself remains a data-integrity problem, not a trading decision this run can act on.
- Invalidation: breached and worsening; needs manual reconciliation, escalating for the second consecutive cycle.
- Catalyst confirmation/contradiction: none — pure lifecycle/tracking issue. See §14.

### RUNE/USDT (crypto, swing, B-tier, status=triggered — open long, NEW confirmed invalidation breach)
- Catalyst: none mapped.
- Has price reacted? Yes — live price 0.4650 (Binance, -1.06% 24h) vs entry zone 0.55015-0.5632 and stop_loss 0.5342. Price sits **~13% below its own stop_loss** while status still reads `triggered`.
- Chasing? N/A — existing unresolved open position, not a new entry.
- Actionable level: none new; this is a reconciliation item, not a trade idea.
- Mood alignment: N/A — tracking issue, not a market call.
- Invalidation: breached, unresolved — first surfaced this cycle via the systematic candles=0 cross-check (signal_outcomes for this signal_id shows `notes` containing `candles=0`, `entry_triggered=1`, `stop_hit=0`).
- Catalyst confirmation/contradiction: none. See §14.

### WLD/USDT (crypto, swing, B-tier x2, status=triggered — two open longs, NEW confirmed invalidation breach)
- Catalyst: none mapped.
- Has price reacted? Yes — live price 0.3763 (Binance, -0.79% 24h) vs two open-long entries: (a) entry 0.41097-0.41487, stop 0.40621; (b) entry 0.40535-0.40933, stop 0.40049. Price sits **~6-7% below both stop levels**, both still `triggered`.
- Actionable level: none new; reconciliation item.
- Mood alignment: N/A.
- Invalidation: breached on both entries, unresolved. Third distinct symbol (after TUT, RUNE) confirming the systemic tracking-gap pattern this cycle.
- Catalyst confirmation/contradiction: none. See §14.

### PROM/USDT (crypto, swing, B-tier, status=triggered — open long, confirmed missed take-profits)
- Catalyst: none verified — the +25-37% 24h move (report-dependent) and +133% 7d move are pure momentum; every report this cycle explicitly rejects fresh PROM entries for being >2 ATR from EMA20.
- Has price reacted? Dramatically — live price ~6.58 (Binance) vs original entry 4.28492-4.38051 and tp1/tp2/tp3 of 4.699/4.912/5.188. Price is **~27% above tp3** yet status still reads `triggered`, not `tp3_hit`.
- Chasing? A fresh add here would be badly chasing an already-extended move; existing position should not be added to.
- Actionable level: none new — avoid candidate, not a watch idea.
- Mood alignment: contrarian to the broader risk-off backdrop — a single-name momentum spike, not leadership confirmed by breadth.
- Catalyst confirmation/contradiction: none — technical-only. See §14 for the tracking-status gap.

### DOGE/USDT / ZKP/USDT (crypto, swing/scalp, B-tier — expiry-window items, late-session relevance)
- `DOGE/USDT` swing `waiting_for_entry` (zone 0.092952-0.093878, created 2026-08-22T21:04:58 UTC) expires 2026-08-29T21:04:58 UTC — at or just past expiry as of this review. Live price 0.08532 never reached the zone (price has been well below it for the signal's entire life). Clean **no-entry/stale**, not a tracking problem — the entry-zone thesis simply never played out.
- `ZKP/USDT` scalp `triggered` (entry 0.04594-0.04681, tp1 0.04914, created 2026-08-29T17:03:12 UTC, 2h window, expires 19:03:12 UTC) is past its own validity window as of this write-up with live price 0.0469 sitting between entry and tp1 — an **entered-unresolved** case (entry filled, neither TP nor SL touched before the window closed), consistent with the scalp report's own header warning about TP1/TP2 vs 2h-horizon mismatch (100% of expired scalps show positive MFE but only ~11% convert to TP1 within the window per the report's own stats).

## 8. Best Candidates Ranked

1. **Long-watch: NIL/USDT** — already triggered and in profit; fresh-add trigger only on a pullback into 0.0536-0.0557 on falling volume, not the current spike.
2. **Short-watch: TUT/USDT** — watch-for-retest only; prior 0.0378-0.0386 zone is stale (price already broke below it); wait for a retest from underneath, funding still extreme-negative (squeeze risk on any bounce).
3. **Catalyst-watch: BNB/USDT or HYPE/USDT** — trigger: independent second-source confirmation of continued binance_ecosystem_teaser or perps_dex_narrative basket strength before treating either as tradeable.
4. **Avoid: PROM/USDT (new size)** — already +27% beyond its own tp3 on the existing open position; a fresh add would be chasing an extreme, unconfirmed-catalyst move.

No A-tier or B-tier setup fired fresh this cycle in any of scalp/intraday/swing. The most consequential item this window is not a trade idea — it is the confirmed, now three-symbol-wide (TUT/RUNE/WLD) invalidation-tracking gap in §7/§14, which needs manual reconciliation before any of the 52 open positions' displayed status can be trusted at face value.

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and the scheduler continue unmodified regardless:
- **New PROM/USDT, GIGGLE/USDT, or other >2-ATR-extended longs** — every report this cycle explicitly rejects these for chase risk.
- **A fresh TUT/USDT short at the current print** — the prior watch zone (0.0378-0.0386) is now stale; wait for a retest.
- **Trusting the `status` field on any crypto position older than ~2 days without a manual live-price check** — 89% of open rows carry the `candles=0` tracking gap this cycle.
- **New ONG/USDT longs** — persistent negative funding through a multi-day rally, squeeze-not-trend signature, unchanged from the 18:40 review.
- **All stocks** — market closed (Saturday); planning-only until Monday.

## 10. Main Risks

- **Systemic execution-lifecycle tracking gap (escalated from single-symbol to book-wide this cycle):** 78/88 (89%) of open crypto proposed-signal rows show `candles=0` in their latest `signal_outcomes` check, and three symbols (`TUT/USDT` ~32% through stop, `RUNE/USDT` ~13% through stop, `WLD/USDT` x2 ~6-7% through stop) are confirmed hard breaches still displaying `status=triggered`. `PROM/USDT` and `ONT/USDT` x2 show confirmed missed take-profits. The dashboard is materially understating real (paper) drawdown risk on the open book. See §14.
- **Concentration into the weekend:** the entire live crypto book is 100% long (52 open positions, 0 shorts armed) against a macro risk score sitting at 85-100/100 — a risk-off shock over a low-liquidity weekend would hit every open position simultaneously, and several of them (per the finding above) are already worse off than their displayed status suggests.
- **Recurring untracked-alert bug:** a third distinct instance this cycle-day (culminating in today's `DEXE/USDT`, sent 14:36:42 UTC) — matches the escalated `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug` pattern (previously confirmed on ALLO/USDT, BANK/USDT, and DEXE/USDT again at 18:40).
- **Catalyst mapping weak:** 57.8% of today's events are unmapped — catalyst layer is context only this run.
- **Weekend-mode underperformance:** most of today's open book was generated on a Saturday; prior-cycle stats show weekend-tagged signals underperform regular-mode signals.
- **Scalp TP-horizon mismatch (known, unchanged):** the scalp report's own header confirms 100% of expired scalps show positive MFE but the 2h TP1/TP2 horizon caps realized capture (PF 0.14 over 14d) — `ZKP/USDT` this cycle is a live example of the same pattern (entered-unresolved at window close).

## 11. Action Plan — next 4 hours

- **Priority:** escalate the tracking-gap finding for manual reconciliation — this is no longer a single-symbol issue. At minimum, manually verify and correct `TUT/USDT`, `RUNE/USDT`, and `WLD/USDT` (x2) against live price and mark them `stopped` if confirmed; spot-check a sample of the remaining 74 `candles=0`-flagged rows for the same pattern.
- Manually verify `PROM/USDT` and `ONT/USDT` (x2) against live price and mark `tp3_hit`/`tp1_hit` as appropriate if confirmed — the paper PnL/winrate stats are being computed off a book that likely understates both realized wins and realized losses simultaneously.
- Do not add to `PROM/USDT`, `GIGGLE/USDT`, or `ONG/USDT`; watch `NIL/USDT` for a genuine pullback into its stated zone.
- Watch for a `TUT/USDT` retest of 0.0378-0.0386 from underneath before considering any fresh short; do not chase the current print.
- `DOGE/USDT` waiting_for_entry has effectively expired unfilled (zone never reached) — no action needed, let it close out as no-entry.
- Stocks: no action possible or needed until Monday pre-market cycles resume.
- Scanning, candidate generation, and tracking continue as normal in the background regardless of this window's manual-review verdict.

## 12. Final Verdict per Mode

- **Crypto scalp:** watch-only — no A/B fired this cycle; `ZKP/USDT` entered-unresolved at window close, consistent with the known TP-horizon mismatch.
- **Crypto intraday:** watch-only — no A/B fired; best watchlist ZKP/USDT (63.6/100) does not clear the active-trade threshold.
- **Crypto swing:** manual review required — no fresh A/B fired, but the existing 52-position open book contains at least 3 confirmed invalidation/TP tracking failures (TUT, RUNE, WLD x2) plus 2 confirmed missed-TP cases (PROM, ONT x2) that need reconciliation before the book's displayed risk can be trusted.
- **Stocks (all modes):** market closed — planning-only, no live verdict applicable today.
- **Overall:** `caution` / `wait_for_trigger` on new entries, `manual_review` on the existing book (elevated from `watch_only` at 18:40, driven by the escalation of the tracking-gap finding from one symbol to a confirmed book-wide pattern).

## 13. Sources

- All facts sourced from internal reports/CLI/DB reads listed in §2, plus a live public Binance ticker cross-check (`api.binance.com/api/v3/ticker/24hr`, accessed 2026-08-29 ~21:42 EEST) used only to verify internal price-vs-stop/TP status, not as an independent trading signal. No external news URLs cited this run — the central finding is a direct internal-DB-vs-live-price comparison.

## 14. Fix Requests / TODO

### TODO-outcome-tracker-candle-gap-systemic-2026-08-29
- **issue:** The outcome-tracking pipeline that updates `proposed_signals.status` / `signal_outcomes` for open crypto positions is failing to detect stop and take-profit touches for the large majority of the open book. Of 88 open/recently-open crypto proposed-signal rows (tier A/B, non-terminal status), **78 (89%)** have a latest `signal_outcomes` row whose `notes` field contains `"candles=0"` (i.e., the OHLCV fetch for that check returned zero candles). This generalizes and escalates the single-symbol `TUT/USDT` finding first raised in `OPUS_ENRICHED_REVIEW_AUTO_2026-08-29_1840.md` (itself tracked in the `project_crypto_ai_desk_bias_tag_contradiction` memory, escalated HIGH on 2026-08-08). Independently cross-checking live Binance spot prices against stored entry/stop/TP levels confirms concrete, material mismatches on at least 4 symbols / 6 signal rows: `TUT/USDT` (price ~32% through its own stop_loss, still `triggered`), `RUNE/USDT` (price ~13% through stop_loss, still `triggered` — new this cycle), `WLD/USDT` x2 open longs (price ~6-7% through stop_loss on both, still `triggered` — new this cycle), `PROM/USDT` (price ~27% beyond tp3, still `triggered`, not `tp3_hit`), and `ONT/USDT` x2 (price above tp1 on both, still `triggered`, not `tp1_hit`). The practical effect: the active-signals dashboard and any risk view built on `proposed_signals.status` currently misrepresents both the downside (unflagged stop-outs) and upside (unflagged TP hits) of the live book, and the paper PnL/winrate stats computed from `signal_outcomes` are likely materially skewed by the same gap for the affected rows.
- **evidence:** Direct SQLite reads against `db/crypto_ai_desk.sqlite`: `SELECT ... FROM proposed_signals WHERE asset_class='crypto' AND tier IN ('A','B') AND status IN ('triggered','tp1_hit','tp2_hit','waiting_for_entry') AND expires_at > now` returned 52 unexpired rows (88 including recently-expired-but-unresolved), all long, mostly `swing` mode. Joining to `signal_outcomes` on `signal_id` (latest row per signal) shows 78/88 with `notes LIKE '%candles=0%'`. Example row for RUNE/USDT (`signal_id='sig_413560265abf107d'`, `checked_at='2026-08-29T18:42:53+00:00'`): `entry_triggered=1, entry_price_used=0.56, stop_hit=0, tp1_hit=0, final_outcome='expired', notes='...candles=0...'` while the live Binance RUNEUSDT price at the same time was 0.4650 — well below the recorded `stop_loss=0.5342`. Same pattern independently confirmed for `WLD/USDT` (two signal_ids, both `candles=0`, both with live price below their recorded `stop_loss`) and reconfirmed worsening for `TUT/USDT` (`sig_c7ce9835f38c40a8`, previously ~26% through stop at 18:40, now ~32% through). `PROM/USDT` (`sig_740562ba764dcd4d`) and two `ONT/USDT` signal_ids show the same `candles=0` note with live price past their respective TP levels.
- **suggested manual fix:** A human-driven session should (1) identify why the OHLCV fetch used by the outcome-checker (`src=binance/1h` per the notes field) is returning zero candles for the majority of open positions — likely candidates: symbol-format mismatch, rate-limiting/backoff silently swallowing errors, a stale or misconfigured data window, or an exchange-side gap specific to the pairs/timeframe requested; (2) once the feed is confirmed working, backfill/reconcile the 78 affected rows' true stop/TP status against historical OHLCV so `proposed_signals.status`, `signal_outcomes`, and any downstream PnL/winrate stats reflect reality; (3) add a monitoring alert for the `candles=0` condition itself (e.g., alert if candles=0 persists across >N consecutive checks for the same signal_id) so this class of gap surfaces immediately rather than being discovered by a periodic manual review; (4) note that two `checked_at` timestamps only 19 seconds apart were observed for the same signal_ids (e.g., RUNE/USDT checked at 18:42:34 and again at 18:42:53) — worth checking whether two monitor processes are running concurrently against the same signal set (possible double-scheduling / leader-lock gap), which would also explain wasted API calls without fixing the candles=0 root cause.
- **priority:** high (generalizes and escalates an already-HIGH item; now confirmed across 4 symbols / 6 signal rows and a systemic 89% incidence rate, not a single-symbol anomaly)
- **first observed:** 2026-07-17 (bias-tag form, per `project_crypto_ai_desk_bias_tag_contradiction` memory); invalidation-breach form confirmed on TUT/USDT 2026-08-29 18:40 EEST; systemic candles=0 pattern and RUNE/WLD confirmations this run, 2026-08-29 21:45 EEST.

### TODO-untracked-alert-dexe-recurrence-2026-08-29
- **issue:** A third distinct untracked-legacy-alert instance was detected this cycle-day: `detect_untracked_legacy_alerts --since 2026-08-29` again returns `DEXE/USDT` swing long, score 65.0, direction long, sent 2026-08-29T14:36:42 UTC — the same timestamp/instance already logged in the 18:40 review's `TODO-untracked-alert-dexe-2026-08-29`, confirming the alert still has no matching `proposed_signal` several hours later (not transient). Matches the escalated `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug` pattern (previously confirmed on ALLO/USDT, BANK/USDT).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-29` output at 21:4x EEST: "1 untracked legacy crypto alert(s)" — DEXE/USDT, tier B, swing, score 65.0, long, sent_at 2026-08-29T14:36:42+00:00, trackable=NO — identical row to the one reported at 18:40, confirming it is still unresolved rather than a new occurrence.
- **suggested manual fix:** unchanged from the 18:40 TODO — investigate the watchlist-alert path for stale/closed signal_id reuse on symbol+mode combinations; this specific DEXE/USDT instance also offers a concrete reproduction case (alert sent 14:36:42 UTC, still untracked ~7h later) for a human session to trace end-to-end.
- **priority:** high (unresolved recurrence of an already-escalated bug, now with a durable reproduction window)
- **first observed:** 2026-07-17 (per memory); this specific instance 2026-08-29 14:36:42 UTC, confirmed still unresolved as of 21:4x EEST.

### TODO-doge-waiting-for-entry-expiring-no-fill
- **issue:** Minor/informational: `DOGE/USDT` swing `waiting_for_entry` (zone 0.092952-0.093878, created 2026-08-22T21:04:58 UTC) expires 2026-08-29T21:04:58 UTC — a 7-day validity window on a `waiting_for_entry` row that price never approached (live price 0.08532, ~9% below the zone's lower bound for the signal's entire life). Not a bug — the entry thesis simply never triggered — but a 7-day `waiting_for_entry` window on a swing signal is unusually long relative to how far price needs to move to invalidate the thesis; worth a human sanity-check on whether `waiting_for_entry` validity windows should scale with distance-to-zone rather than being fixed at the mode's default.
- **evidence:** `proposed_signals` row for DOGE/USDT, `status='waiting_for_entry'`, `created_at='2026-08-22T21:04:58+00:00'`, `expires_at='2026-08-29T21:04:58+00:00'`; live Binance DOGEUSDT price 0.08532 vs entry_low 0.09295.
- **suggested manual fix:** low-priority — a human session could review whether `waiting_for_entry` validity windows for swing-mode signals should be capped or made distance-aware, since a 7-day-old unfilled entry zone provides little decision value by the time it expires.
- **priority:** low
- **first observed:** 2026-08-29 21:4x EEST (this cycle, informational).
