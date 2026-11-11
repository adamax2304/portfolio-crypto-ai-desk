# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:45 EEST

## 1. Executive Summary

**Advisory only / no auto-trade.** Slot: **late-session risk review** (21:30 EEST target, run at 21:45). **Sunday, 2026-09-06 — US cash markets closed all day**; stocks are planning/carry-forward context only, crypto is the only live actionable class. The scheduler restarted its 12-cycle window at 21:18 EEST (fresh `data/scheduled_runs/2026-09-06_default_schedule/`, cycle 1/12) but all monitor processes were reused healthy — no gap in live tracking. Crypto regime **improved slightly since the 18:38 review**: BTC recovered from range back to **uptrend**, ETH holds uptrend, altcoin breadth 89.6% above EMA20 — but macro risk is still pinned at **100/100** (Iran/US military escalation headlines unchanged/continuing) and catalyst mapping is **weak this run (70.4% unmapped)**, a fifth straight cycle above the 50% threshold. **0 A-tier crypto signals** in the fresh 21:38 intraday or 19:33 swing reports; the only fresh A-tier anywhere (GE/stocks, 2 rows) is ~3 weeks stale (`tp1_hit`, created 2026-08-18/19) and irrelevant with markets closed. The cleanest read tonight is the **swing** book: COTI/USDT B-tier at 78.9/100 (medium confidence, RS-leader + narrative playbook with 14d WR 72%/PF 5.80), while the **intraday** no-catalyst momentum playbook (SUSHI/ZK/COTI, scores 65-68) carries a known-negative 14d edge (WR 23%/PF 0.70/-3R) — same symbols, opposite verdict by mode. The true open crypto book (DB-verified, not the 50-row CLI cap) is **92 signals** (17 waiting / 35 triggered / 30 tp1_hit / 10 tp2_hit), **89 long / 3 short** — correcting the 18:38 review's "100% long" claim, though the 3 shorts are themselves stale/anomalous (see §14). 16 untracked legacy alerts today, unchanged since 18:38 (no new ones this window) — a known, continuing integrity gap, not new.

## 2. Data Used

- `data/reports/intraday/2026-09-06_18-38_intraday_report.md` (generated 21:38:03 EEST — ~7 min old, freshest available)
- `data/reports/swing/2026-09-06_16-33_swing_report.md` (generated 19:33:34 EEST — ~2h12m old, inside the <4h fresh bracket)
- `data/reports/stocks/intraday/2026-09-04_19-53_stocks_intraday_report.md` (Friday close — stale/context-only, expected on a weekend)
- `data/reports/stocks/swing/`, `.../invest/` — last populated 2026-07-02 (known-deprecated paths, not a freshness failure)
- `data/catalysts/2026-09-06/catalyst_events.jsonl` (2,500 events today, full-day file), `catalyst_cycle_15-18.md` (latest cycle scan, 18:18 EEST), `narrative_baskets.jsonl` (6 baskets)
- `data/processed/llm_analysis_packet.md` (fresh, 21:40 EEST)
- `python -m src.cli active-signals --asset-class crypto` / `--asset-class stocks`
- `python -m src.cli signal-stats --asset-class crypto` / `--asset-class stocks`
- `python -m scripts.detect_untracked_legacy_alerts --since 2026-09-06`
- Direct read-only SQL against `db/crypto_ai_desk.sqlite` `proposed_signals` table (status/direction breakdown) — used because the CLI's default 50-row cap under-reports the true open-book size
- `data/scheduled_runs/2026-09-06_default_schedule/scheduler.log` (fresh boot, 21:18 EEST) and `data/scheduled_runs/2026-09-05_default_schedule/scheduler.log` (prior day, final tally before rollover)
- Previous review `OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_1838.md` (~3h07m earlier) for §4 comparison
- **No external WebSearch/WebFetch run this cycle.** Internal records (macro headlines already ingested into the intraday report and catalyst JSONL, all consistent with the 18:38 read) were sufficient per §G; no candidate's verdict depended on unverified external claims this pass.

## 3. Scheduler / Data Freshness

- Scheduler folder: `data/scheduled_runs/2026-09-06_default_schedule/` (new boot). `scheduler.log` mtime ~21:43 EEST (2 min old); this is a fresh 12-cycle window (`total=86400s interval=7200s cycles=12 deadline=2026-09-07T21:18:38+03:00`), cycle 1/12 in progress. All monitors (`CRYPTO MONITOR`, `PENDING MONITOR`, `MEXC-CANARY MONITOR`, `CRYPTO-INVEST-FORWARD MONITOR`, `DERIVATIVES MONITOR`, `FAST-NEWS MONITOR`, `TELEGRAM DASHBOARD`) reported "already healthy, reusing" — no tracking gap from the restart. No defer needed (well inside the 3h gate).
- Cycle 1's `crypto intraday report` step ran 21:20:48→21:40:28 (1,179.7s) and produced the fresh report used above. `track-signals (pre)` completed in 76.1s with exit=0.
- **Zero `CMD TIMEOUT` lines in today's (fresh) log so far** — too early to judge; the previous log (`2026-09-05_default_schedule/scheduler.log`) ended at **51 total `CMD TIMEOUT` lines** before rollover (up from 47 at the 18:38 review), with `refresh obsidian dashboard` timing out again at 19:47:47 EEST (its 7th failure of that day) plus new timeouts on `crypto swing versioned shadow sweep (counterfactual)` and `agent run summary retention (daily)`. This is a **continuing pattern carried into the new log**, not resolved by the restart — see §14.
- No monitor/paper-portfolio status file read beyond the scheduler log; paper P&L visibility should still be treated as potentially lagging given yesterday's repeated `paper execution accounting refresh` / `paper-shadow A/B execution` timeouts.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-09-06 21:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["today's fresh-log timeout history (log just rolled over)"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log fresh boot 21:18 EEST", "intraday report 21:38 EEST (~7min old)", "swing report 19:33 EEST (~2h12m old, inside 4h bracket)", "stocks reports Friday carry-forward, market closed"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mixed", "risk_off", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["BTC back to uptrend (was range at 18:38)", "ETH uptrend", "altcoin breadth 89.58% above EMA20", "macro risk still 100/100, Iran/US escalation unchanged", "US markets closed (Sunday)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["70.4% unmapped catalyst events today (739/2500 mapped)", "momentum_breakout basket explicitly flags UNI/USDT as catalyst-backed, fresh <1h", "binance_ecosystem_teaser (BNB) fresh <6h", "perps_dex_narrative (HYPE) carries $860M unlock risk flag"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["oi_supports", "funding_extreme", "data_unavailable"], "data_missing": ["order-book depth", "cross-venue liquidation heatmap"],
      "suggested_effect": "advisory_only", "facts_used": ["COTI: price up + OI up +12.43%, funding negative (-0.00064), crowding unknown", "SUSHI/ARB/ZAMA: price up + OI up, crowding normal", "ZEC: price up + OI down -2.05%, short-covering / weaker continuation"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "clean_retest", "overextended"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["ARB +28.61%/24h (intraday) and +41.4%/24h (swing timestamp), volume 0.08-0.19x avg — thin-volume overextension", "COTI swing pullback zone 0.0169-0.0174 vs current 0.0176 — close to fillable, not yet extended", "SUSHI intraday/swing both show 13.55%/24h, pullback zone 0.2551-0.2595 vs current 0.2614 — near zone"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": ["exact TP/stop distance per open position (not queried individually)"],
      "suggested_effect": "advisory_only", "facts_used": ["DB-verified crypto open book: 92 total (17 waiting_for_entry, 35 triggered, 30 tp1_hit, 10 tp2_hit); 89 long / 3 short", "3 short signals (NEAR from 2026-07-17, BICO from 2026-08-11, ZEC from 2026-07-28) are weeks-old and flagged needs_review — see TODO", "stocks open book 230 (163 tp1_hit, 53 tp2_hit, 14 triggered), all carry-forward/market closed", "0 fresh crypto A/B this cycle; only stale A-tier (GE, ~3wk old, tp1_hit)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "reduce_risk", "correlation_cluster"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["macro risk 100/100 on live Iran/US military escalation, unchanged from 18:38", "weekend-mode cohort underperforms historically (12% winrate, n=105, per this run's signal-stats)", "book is overwhelmingly long-direction (89/92) with only 3 (stale) shorts as nominal offset"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto A/B headline: winrate 18.6%, PF 2.24, avgR 0.28, totalR 38.3 (n=204 reliable, 188 triggered)", "crypto swing RS-momentum playbook: 14d WR 72%/PF 5.80/+24R — strong, and is the source of tonight's best candidate", "crypto no-catalyst intraday momentum playbook: 14d WR 23%/PF 0.70/-3R — known-negative, source of tonight's SUSHI/ZK/COTI intraday ideas", "stocks C-tier: winrate ~7% (n=598), PF 0.75 — reliably weak bucket, never actionable by design"] },
    { "agent": "head_trader", "verdict": "advisory_only", "confidence": 0.65,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "COTI/USDT", "trigger": "swing pullback fill into 0.0169-0.0174 (current price 0.0176, just above the zone) with the 1h invalidation at 0.0162 holding; the crypto_swing_narrative_rs_momentum playbook (14d WR72%/PF5.80) backs this, not the weaker no-catalyst intraday variant of the same symbol", "reason": "Highest-scoring signal in either fresh report tonight (78.9/100, medium confidence), RS vs BTC +17.92%, OI +12.43% confirming fresh positioning, and it sits on the desk's strongest recent playbook rather than the known-negative no-catalyst intraday bucket." },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "no clean technical/derivatives confirmation available this cycle beyond the 'bias short' momentum tag (-10.23%/24h, -10.16% RS vs BTC) — treat as watch-only until a failed-bounce or derivatives read (funding/OI) is confirmed in a later cycle", "reason": "Weakest symbol in tonight's intraday report by 24h return and RS vs BTC, but the report supplies no derivatives/funding detail for it (unlike HEMI in the prior review) — data is genuinely insufficient to call this more than a watch." },
    "best_catalyst_candidate": { "symbol": "UNI/USDT", "trigger": "the desk's own momentum_breakout basket (fresh <1h) explicitly labels UNI 'CATALYST-BACKED ... watch pullback / do NOT chase' — wait for a defended pullback rather than the +19.5%-day move already on the tape; UNI also fired an untracked Telegram alert twice today (11:45, 15:29) with no backing proposed_signal, so any operator action here should go through a fresh signal, not the stale alert", "reason": "Only candidate tonight with an explicit system-generated catalyst-backed label (not just a narrative-basket association), giving it more structural backing than the pure-momentum ARB/SUSHI ideas." },
    "avoid_candidate":         { "symbol": "SUSHI/USDT (intraday mode)", "reason": "Same symbol, same 24h move (+13.55%) scores respectably on the swing playbook (73.9, legit RS-momentum edge) but only 65.5-67.5 on the intraday no-catalyst momentum playbook, whose 14d track record is WR 23%/PF 0.70/-3R. SUSHI intraday has also fired 4 untracked legacy alerts today (09:08, 11:45, 15:29, 18:38) with no backing proposed_signal — avoid treating any of those Telegram pings as an entry signal." },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.70 | mixed, risk_off, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | oi_supports, funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, clean_retest, overextended | advisory_only |
| execution_lifecycle | ok | 0.75 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, reduce_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution (overall) | 0.65 | synthesis | advisory_only |

## 4. What Changed vs Previous Review (18:38 EEST, ~3h07m earlier)

- **BTC trend improved:** range (15:10 report, used at 18:38) → **uptrend** (21:38 report, used now). ETH holds uptrend both times. Altcoin breadth ticked down slightly (91.1% → 89.6% above EMA20) but stays elevated.
- **Macro risk unchanged at the ceiling:** 100.0/100 both reviews — same Iran/US escalation headline cluster (US strikes on Iranian tankers/vessels, missile strike affecting a wedding party, Iran vowing a "more painful response"); no de-escalation signal yet.
- **No tier changes among tonight's top candidates:** COTI/SUSHI/ARB/ZAMA remain the same names across both intraday and swing reads; COTI's swing score is essentially flat (78.9 now vs the same bucket's framing at 18:38).
- **Untracked legacy alerts held flat at 16** — no new ones fired between 18:38 and now (last one was SUSHI at 18:38:03, coinciding with this report's own generation time). Same systemic pattern, not worsening this window.
- **Catalyst mapping slightly better:** 70.4% unmapped now vs (per the 18:38 review) 70.4% at that time too — flat, still a fifth straight cycle above the 50% gate.
- **Scheduler restarted:** a fresh 12-cycle window began at 21:18 EEST (`2026-09-06_default_schedule`), replacing yesterday's log which ended at 51 total timeouts. This is an operational restart, not a data gap — all monitors reported healthy/reused.
- **Corrected from 18:38 review:** the prior review stated "book is 100% long-direction with no short exposure." A direct SQL check this run found **3 short positions** open (NEAR, BICO, ZEC) — the prior review's claim came from the 50-row-capped CLI table, which happened to show none. The true picture is still heavily long-skewed (89/92) but not literally 100%; the 3 shorts are themselves weeks-old and flagged for review (§14).
- HEMI/USDT (prior review's short-watch) is no longer in tonight's top-5 weakest list; TUT/USDT has taken its place as the weakest symbol, with less derivatives detail available.

## 5. Catalyst Coverage

- Total catalyst events today (full-day file): **2,500**. Mapped (non-null symbol): **739**. Unmapped: **1,761** (**70.4%**).
- Latest cycle scan (`catalyst_cycle_15-18.md`, 18:18 EEST): 500 news_items scanned → 500 catalyst events, 6 narrative baskets. By type: other_news 465, exchange_listing 16, legal_risk 4, product_launch 3, partnership 3, regulatory_sector_headline 3, buyback_burn 2, token_unlock 1, rumour_only 1, platform_growth 1, exchange_delisting 1.
- Narrative baskets: `perps_dex_narrative` (HYPE, fresh<1h, playbook wait_pullback), `rwa_narrative` (ONDO/XLM, fresh<1h), `binance_ecosystem_teaser` (BNB, fresh<6h), `ai_narrative` (NEAR/RENDER/TAO/FET, fresh<24h), `delisting_thin_liquidity` (no primary symbol, avoid_low_liquidity), `momentum_breakout` (UNI/AUCTION, fresh<1h — UNI explicitly catalyst-backed per the desk's own labeling).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (70.4% unmapped, ≥50% threshold breached for a fifth straight cycle; continuing, not a fresh TODO.)
- Top unmapped headlines sampled (all legitimately symbol-less geopolitical/macro items, not resolver failures): "KREMLIN: KUSHNER AND WITKOFF AGREED TO CONSIDER PUTIN'S ASSESSMENTS OF POSSIBLE WAYS TO RESOLVE THE UKRAINE CONFLICT" (t.me/marketfeed); "CZ: YZi Labs' Investments Made Near the Depths of the Crypto Winter Could Be Among Its Best Performers" (t.me/wublockchainenglish); "WHITE HOUSE OFFICIAL: US AND RUSSIAN OFFICIALS DISCUSSED DETAILED PLANS FOR NEXT STEPS IN RUSSIA-UKRAINE WAR TALKS" (t.me/marketfeed).

## 6. Market Landscape

BTC has recovered from range back to uptrend while ETH continues uptrend uninterrupted; altcoin breadth stays high (89.6% above EMA20). The tape looks constructive on pure technicals, but macro risk is unchanged at the maximum reading (100/100) on live, unresolved Iran/US military escalation — the desk's own scorer still tags this "BTC bias risk-off headwind." Today being Sunday keeps stocks fully out of the live picture. The dominant crypto cluster remains L2/DeFi beta (ARB, SUSHI, UNI, ZAMA, COTI) running on relative-strength momentum with thin trailing volume (0.0-0.8x avg across the board) — a tape that is broadly up but not obviously backed by fresh volume conviction.

### Market Mood / Risk Routing

- Crypto mood: **mixed / cautiously constructive** (BTC/ETH technicals improved, breadth still elevated, but macro risk stays pinned at maximum on live geopolitical escalation)
- Stocks mood: **closed** (Sunday — no cash session; Friday-close data is context-only)
- Dominant narrative: L2/DeFi beta rotation (ARB, SUSHI, UNI, ZAMA cluster) plus a swing-mode RS-leader in COTI — same cluster flagged in recent reviews, still running, still mostly thin on confirming volume
- Preferred side now: **longs, RS-leader/swing-mode preferred over no-catalyst intraday chase** — the swing playbook (WR72%/PF5.80) is materially stronger evidence than the intraday no-catalyst playbook (WR23%/PF0.70) for the same names
- Best long candidate: COTI/USDT (swing) — see §7/§8 for exact trigger
- Best short candidate: TUT/USDT — watch-only, insufficient derivatives confirmation this cycle
- Best catalyst-backed candidate: UNI/USDT (momentum_breakout basket, explicit catalyst-backed label)
- What to avoid: chasing SUSHI/ARB/COTI on the intraday no-catalyst momentum read (known-negative 14d edge); treating any of today's 16 untracked Telegram alerts as a live entry signal (no backing proposed_signal exists for them)
- What would change the view: a de-escalation headline on the Iran/US situation (macro risk score would likely retrace from 100), or confirmed volume expansion on COTI/ARB that would strengthen the swing thesis beyond "low confidence"

## 7. Candidate Deep Dives

### COTI/USDT — B-tier swing, long (score 78.9/100, medium confidence)

- Has price already reacted to the catalyst? No verified fresh catalyst — this is a pure RS-momentum/derivatives-positioning setup (24h +17.51%, 7d +34.84%), on the desk's strongest recent playbook (crypto_swing_narrative_rs_momentum, 14d WR72%/PF5.80).
- Is the setup chasing? Marginally — current price 0.0176 sits just above the system's own pullback zone (0.0169-0.0174), so a small pullback would put it in the preferred entry range rather than requiring a chase.
- Retest/pullback structure? Yes — explicit conditional zone defined, not yet filled.
- Overextended? Not flagged explicitly; RR to TP1 is 1.84R per the report, consistent with the desk's standard setup geometry, not an outlier.
- Would entry now be late? Borderline — better to wait for the 0.0169-0.0174 fill than buy at 0.0176 outright.
- Actionable level: pullback fill into 0.0169-0.0174, invalidation on a 1h close below 0.0162.
- Aligned with market mood? Yes — RS-leader long in a longs-preferred, mixed-but-improving tape.
- Long/short/wait: long, entry conditional on the pullback fill (or accept modest chase risk at 0.0176).
- Catalyst confirmation or contradiction? No fresh verified catalyst; funding is negative (-0.00064), meaning shorts are somewhat crowded — a mild tailwind for the long thesis (short-squeeze potential) rather than a contradiction, but crowding is marked "unknown" on the primary derivatives read.
- Chase-risk? Low-to-moderate given proximity to the defined pullback zone.

### SUSHI/USDT — mode-split verdict: swing watch (73.9) vs intraday avoid (65.5-67.5)

- Same 24h move (+13.55%) scores acceptably on the swing RS-momentum playbook but sits on the intraday no-catalyst momentum playbook's known-negative bucket (WR23%/PF0.70/-3R over 14d) when evaluated on the intraday timeframe.
- Has price already reacted? No fresh catalyst on either read — pure momentum.
- Chasing? Current price 0.2614 vs pullback zone 0.2551-0.2595 on both reads — close to the zone, not badly extended.
- Actionable level (swing only): pullback fill into 0.2551-0.2595, invalidation 1h close below 0.2498.
- Catalyst confirmation? None. Volume ratio only 0.54x avg — breakout confirmation is weak on both reads.
- Integrity note: SUSHI fired 4 untracked Telegram alerts today (09:08, 11:45, 15:29, 18:38 UTC), none with a backing `proposed_signal` — any of those pings should not be treated as an actionable entry.
- Verdict: swing-mode watch only (not yet filled); intraday-mode avoid (known-negative playbook + integrity gap).

### UNI/USDT — catalyst-backed watch (momentum_breakout basket, fresh <1h)

- Has price reacted to the catalyst? The basket note says UNI is already +19.5%/24h on 0.84x volume — some of the move has likely already happened; the system explicitly warns "do NOT chase."
- Chasing? Yes if entered at the current extended price; the system's own label confirms this.
- Retest structure? Not explicitly quantified in tonight's data (UNI did not appear as a full deep-dive candidate in either fresh report) — treat the basket's own "watch pullback" instruction as the operative guidance until a dedicated pullback zone is published in a later cycle.
- Actionable level: wait for a defined pullback per the basket playbook (`wait_pullback`); do not chase the already-elevated price.
- Catalyst confirmation: single-source basket attribution — not yet primary-source confirmed, but the system's own catalyst-backed label carries more weight than the pure-momentum names.
- Integrity note: UNI fired 2 untracked alerts today (11:45, 15:29) with no backing `proposed_signal`.

### TUT/USDT — weakest symbol, short-watch only (data-limited)

- Has price already reacted? Already -10.23%/24h — the move is underway.
- Chasing? A fresh short now would be chasing an already-large down move with no derivatives confirmation available in tonight's data (unlike HEMI in the 18:38 review, which had explicit funding/crowding detail).
- Actionable level: cannot be specified with confidence this cycle — needs a failed-bounce structure and/or a funding/OI read in a later cycle before this becomes more than a name on a list.
- Verdict: watch-only; do not initiate.

### GE (stocks) — stale A-tier, not a live candidate

- Two A-tier `tp1_hit` rows exist (created 2026-08-18/19), ~3 weeks old, market closed today (Sunday) regardless. Not evaluated as a fresh candidate; carried only to confirm the "0 fresh A-tier" claim in §1 is accurate (the only A-tier rows in the system are this stale pair).

## 8. Best Candidates Ranked

No A-tier crypto or stocks candidate is fresh and actionable this window (Sunday, weekend-mode, cash markets closed, and no A-tier crypto signal exists in either fresh report). Ranked by conviction as watch/conditional-entry items:

1. **COTI/USDT (long-watch, swing)** — trigger: pullback fill 0.0169-0.0174, invalidation below 0.0162. Highest score (78.9) and best-performing playbook (14d WR72%/PF5.80) of anything read tonight.
2. **UNI/USDT (catalyst-watch)** — trigger: defined pullback per `momentum_breakout` basket's own `wait_pullback` playbook; do not chase the existing +19.5%/24h move.
3. **SUSHI/USDT (long-watch, swing mode only)** — trigger: pullback fill 0.2551-0.2595, invalidation below 0.2498. Do NOT treat the intraday-mode version of the same symbol (65.5-67.5, no-catalyst playbook) as equivalent.
4. **TUT/USDT (short-watch, low confidence)** — trigger: undefined this cycle; needs a failed-bounce or derivatives read before it is more than a name on a list.

## 9. Avoid / No Trade

This is a **decision-window-only** call, not a system pause — scanning, tracking, and outcome recording all continue normally.

- **SUSHI/USDT on the intraday timeframe specifically** (not the swing timeframe) — known-negative no-catalyst playbook (WR23%/PF0.70/-3R) plus 4 untracked Telegram alerts today with no backing signal.
- Treating any of today's 16 untracked legacy alerts (SUSHI×4, UNI×2, FIL, ADA, ENA, CHIP, ETH×2, FF, and others) as a live entry — they carry no `proposed_signal`, so they will not be tracked in PF/winrate stats even if acted on.
- Initiating any *new* crypto exposure into the weekend-mode cohort generally — historically the weaker-performing bucket (12% winrate, n=105, per tonight's signal-stats), and today's macro backdrop (100/100 risk) adds incremental headline risk on top of that known handicap.
- Stocks: nothing to avoid or take — market is closed; the two ~3-week-old GE `tp1_hit` rows and the broader 230-row stocks open book are historical/carry-forward only.

## 10. Main Risks

- **Geopolitical/macro:** Iran/US military escalation remains live and unresolved; macro risk sits at the maximum reading (100/100), unchanged since the 18:38 review. A further escalation (or de-escalation) could move BTC/crypto risk appetite sharply before the next review.
- **Long-only concentration, corrected:** the true open crypto book is 89 long / 3 short (not literally 100% long as the 18:38 review stated) — but the 3 shorts are themselves weeks-old and flagged `needs_review` (see §14), so the *effective* live short exposure is closer to zero in practice.
- **Weekend-mode drag:** signal-stats this run shows the weekend=Y cohort at 12% winrate (n=105) — a known structural headwind independent of tonight's specific setups.
- **Untracked-alert integrity gap:** 16 crypto alerts sent to Telegram today have no backing `proposed_signal` and will not contribute to tracked PF/winrate stats — flat since 18:38, not worsening this window, but still a live gap between what operators see on Telegram and what the tracker can measure.
- **Scheduler reliability:** yesterday's log ended at 51 total `CMD TIMEOUT` lines before the 21:18 restart; the recurring `refresh obsidian dashboard` and paper-execution-step timeout patterns are almost certainly still present (today's log is too young to confirm) — paper P&L visibility should be treated as potentially lagging.
- **Data-hygiene on the open book:** 3 short signals (NEAR from 2026-07-17, BICO from 2026-08-11, ZEC from 2026-07-28) remain in non-terminal status (`tp1_hit`/`tp2_hit`) weeks after creation — worth a manual check on whether these should have closed out already (see §14).

## 11. Action Plan — Next 4 Hours

- Watch COTI/USDT for a fill into the 0.0169-0.0174 pullback zone; treat a 1h close below 0.0162 as invalidation if entered.
- Watch UNI/USDT for a defined pullback per the `momentum_breakout` basket; do not chase the existing +19.5%/24h move.
- Watch SUSHI/USDT swing-mode pullback zone (0.2551-0.2595) separately from the intraday-mode read, which stays avoid.
- Continue monitoring the Iran/US headline stream — a materially better or worse headline would likely move the macro risk score and could flip routing (de-escalation → strengthens the RS-leader-long thesis; further escalation → tighten invalidations / reduce new entries further).
- No action needed on stocks until Monday's real pre-US-open review.
- Scanning, tracking, and outcome recording continue uninterrupted regardless of the above — no pause/disable action is recommended or implied.

## 12. Final Verdict per Mode

- **Crypto scalp:** No fresh data this cycle (scalp reports last populated 2026-08-30, ~1 week stale) — treat as currently deprioritized/inactive, not evaluated this run.
- **Crypto intraday:** No A-tier; B-tier ideas (SUSHI/ZK/COTI, 65.5-67.5) sit on a known-negative no-catalyst playbook. Verdict: **watch-only, avoid-new on this specific playbook.**
- **Crypto swing:** No A-tier; B-tier ideas led by COTI (78.9) on the desk's strongest recent playbook (14d WR72%/PF5.80). Verdict: **watch/conditional-entry on pullback fills, do not chase current prices.**
- **Stocks intraday/swing/invest:** Market closed (Sunday). Friday's data and the ~3-week-old GE A-tier rows are historical context only. Verdict: **N/A — planning only, resume normal evaluation at Monday's pre-US-open review.**

## 13. Sources

- Macro headlines as surfaced in `data/reports/intraday/2026-09-06_18-38_intraday_report.md` §4: US denies Iran's claim of striking an unmanned vessel in the Strait of Hormuz; Dow Jones futures commentary referencing US-Iran attacks; Kushner/Zelensky Ukraine commentary — all sourced from the desk's existing internal macro/news pipeline, no fresh external WebSearch performed this cycle (see §2).
- Narrative baskets and catalyst mapping counts: `data/catalysts/2026-09-06/catalyst_events.jsonl`, `data/catalysts/2026-09-06/narrative_baskets.jsonl`, `data/catalysts/2026-09-06/catalyst_cycle_15-18.md` (internal, read-only).
- Signal/lifecycle stats: internal SQLite via `python -m src.cli active-signals` / `signal-stats` (read-only CLI, §A.4) and a direct read-only query against `db/crypto_ai_desk.sqlite` (`proposed_signals` table) for the accurate open-book breakdown.
- Scheduler timeline: `data/scheduled_runs/2026-09-06_default_schedule/scheduler.log` (fresh boot) and `data/scheduled_runs/2026-09-05_default_schedule/scheduler.log` (prior day, final tally), internal, read-only.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_1838.md`, internal, read-only.

## 14. Fix Requests / TODO

### TODO-stale-short-signals-non-terminal-status (new, low)
- **issue:** 3 crypto short signals remain in non-terminal status (`triggered`/`tp1_hit`/`tp2_hit`) weeks after creation, well past any reasonable evaluation window: `NEAR/USDT` (created 2026-07-17, `tp1_hit`), `BICO/USDT` (created 2026-08-11, `tp1_hit`), `ZEC/USDT` (created 2026-07-28, `tp2_hit`, entry zone 469.62-472.62, invalidation 476.29 — ZEC has since rallied past $1,000 per tonight's own news feed, i.e. ~2x above the short's invalidation level, yet the row is not marked closed/stopped).
- **evidence:** direct query against `db/crypto_ai_desk.sqlite` `proposed_signals` table, filtered to `asset_class='crypto' AND direction='short' AND status IN ('waiting_for_entry','triggered','tp1_hit','tp2_hit')`; cross-referenced against `data/reports/intraday/2026-09-06_18-38_intraday_report.md` §5 (Zcash breaks $1,000 headline).
- **suggested manual fix:** confirm whether these 3 rows represent genuinely still-open (partially booked) positions the lifecycle tracker intentionally leaves open after a TP hit (in which case this is expected behavior, not a bug), or whether they are stale rows that should have transitioned to a closed/expired state; if the latter, this is the same class of issue as the previously-flagged 1000CAT-invalidation and bias-tag-contradiction patterns (stale signal state on symbols that have since reversed hard).
- **priority:** low (no live risk exposure implied — profit was already locked at TP1/TP2 on all 3 — this is a bookkeeping/accounting-hygiene question, not a trading risk)
- **first observed:** 2026-09-06 21:45 EEST.

### TODO-cli-active-signals-default-limit-undercounts (new, low)
- **issue:** `python -m src.cli active-signals --asset-class crypto` (and `--asset-class stocks`) defaults to `--limit 50`, silently truncating the displayed table to 50 rows even when the true open book is larger. Tonight's true crypto open book is 92 rows (DB-verified) vs the 50 shown by the CLI default; a prior review (18:38 EEST) stated "book is 100% long-direction with no short exposure" based on the capped 50-row view, which happened not to include any of the 3 existing short rows — an avoidable inaccuracy.
- **evidence:** CLI output header reads "Armed Watch / active signals (50) — asset_class=crypto" both this run and at 18:38; direct SQL count returns 92 open crypto rows (17 waiting_for_entry + 35 triggered + 30 tp1_hit + 10 tp2_hit).
- **suggested manual fix:** either raise the default `--limit` for scheduled-review usage, or have this routine's own instructions call it with an explicit higher `--limit` (or paginate) so future reviews don't silently under-report book composition; alternatively add a total-count line to the CLI output independent of the row limit.
- **priority:** low (does not affect live trading; affects only the accuracy of advisory review commentary)
- **first observed:** 2026-09-06 21:45 EEST (surfaced by this run's decision to cross-check via direct SQL; likely present in all prior reviews using the CLI default).

_Recurring note (not a new TODO, already tracked): `detect_untracked_legacy_alerts` found **16** untracked legacy crypto alerts today, flat since the 18:38 review (no new ones fired this window) — same watchlist-alert/signal-reuse pattern already raised as a high-priority item on 2026-07-17._

_Recurring note (not a new TODO, already tracked): catalyst mapping weak this run (70.4% unmapped, a fifth straight cycle above 50%, flat vs 18:38) — already covered by existing/standing project context._

_Recurring note (not a new TODO, already tracked): scheduler timeout pattern (`refresh obsidian dashboard`, `paper execution accounting refresh`, `paper-shadow A/B execution`, etc.) — yesterday's log ended at 51 total `CMD TIMEOUT` lines before tonight's 21:18 restart; today's fresh log has not yet reached these steps, so this run cannot confirm whether the restart changed anything, but there is no reason to believe the underlying cause (unchanged code/config) has been addressed._
