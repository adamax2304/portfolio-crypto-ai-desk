# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:39 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context** (11:30 EEST). Advisory only — no auto-trade, no scoring/threshold/routing changes. US cash market has not opened yet (11:39 EEST ≈ 04:39 ET); stocks are pre-market/planning context only, crypto is the live actionable class. Fed's July FOMC minutes release later today (per external search) is the session's biggest scheduled catalyst for both crypto and stocks — flag for the 16:20/18:30 slots.

Crypto scalp and intraday scans both came back **no A/B trade** this cycle (kill-switch off for scalp, no clean intraday setup). The one live crypto idea is a **B-tier swing long on ACE/USDT — but a second, near-duplicate ACE swing long already triggered overnight**, so ACE is now correlated double-exposure with a still-stale (6-day-old) catalyst, not a fresh trigger. Stocks intraday: **0 actionable A/B** (49 demoted to C by gates), consistent with pre-open planning-only status. A **data-integrity finding**: at least 25 of 43 "active" crypto signals (58%) carry an `expires_at` that already passed — some by a month (e.g. NEAR/USDT, expired 2026-07-17) — yet remain in `tp1_hit`/`tp2_hit` status with no final win/loss recorded; see §14. A second finding: **EDEN/USDT** is held as an open B-tier LONG (invalidation 0.045972) while today's scans independently score it as a short candidate (-10.7% to -12% 24h, `weak_rs_short`) — the same bias-tag-contradiction pattern already tracked in memory for ZBT/ACE; flagged for operator glance. Catalyst mapping is weak this run (80.3% unmapped) — use as context only. No untracked-alert integrity issues.

## 2. Data Used

- Reports: scalp (2026-08-19 07:05, fresh), intraday (07:13, fresh), swing (01:46, ~7h old → carry-forward per 4–12h band), stocks intraday (07:39, fresh but pre-market/not tradable), stocks swing/invest (deprecated, stale since 2026-07-02 — excluded).
- `data/processed/llm_analysis_packet.md` (10:14), `data/processed/llm_stocks_packet.md` (10:41) — freshness-checked, not separately re-parsed (content overlaps the reports above).
- `data/catalysts/2026-08-19/catalyst_events.jsonl` (1500 raw rows / 976 unique titles), `narrative_baskets.jsonl` (5 baskets).
- SQLite `db/crypto_ai_desk.sqlite`: `proposed_signals` (active-signal status breakdown, expiry-vs-status cross-check), `news_items` (ACE 24h catalyst check, GE 48h legal/headline check).
- CLI: `active-signals` (crypto 43 rows, stocks 50 rows), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-08-19` (0 findings).
- External: WebSearch ×2 (BTC/ETH macro mood, ACE/Fusionist catalyst check) + WebFetch ×1 (verified top BTC/ETH result opens and is dated 2026-08-19).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_0439.md` (04:39 EEST cycle).

## 3. Scheduler / Data Freshness

- Active scheduler folder is `data/scheduled_runs/2026-08-18_default_schedule/` (naming carries over the midnight rollover): `scheduler.log` mtime **10:54:29 EEST** (~45 min old), latest `cycle_06_09-56_summary.md` mtime **10:54:27 EEST** — both well inside the 3h defer threshold, not deferred.
- A separate, stale `2026-08-19_default_schedule/scheduler.log` exists (mtime 02:38 EEST) with no cycle summaries — a same-day-rollover artifact, not the active log (same pattern noted in the 04:39 review).
- Reports: scalp/intraday fresh (<2h), swing carry-forward (~7h, inside 4–12h band, still usable), stocks intraday fresh but pre-market (not tradable this slot).
- Catalyst data fresh (`data/catalysts/2026-08-19/` generated same-day, actively growing — 500 events at 07:05 report time → 1500 raw rows by this review).
- No monitor/paper-portfolio status file read this run (outside the allowed read set beyond active-signals/signal-stats); lifecycle status inferred directly from `proposed_signals`.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-19 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"],
      "data_missing": ["monitor/paper-portfolio status file", "live EDEN/USDT price (no OHLCV table in the allowed SQLite read set)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 10:54, cycle_06 summary mtime 10:54", "scalp 07:05 / intraday 07:13 fresh", "swing 01:46 carry-forward (~7h)", "25/43 active crypto signals have expires_at already in the past"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chop", "mixed", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["internal regime range/chop, BTC/ETH local uptrend, altcoin breadth 43.6%/46.2%", "external: BTC ~$64k, ETH ~$1,895-1,911, consolidation/wait-and-watch mood per Sunday Guardian (2026-08-19)", "Fed July FOMC minutes due today — identified externally as the session's biggest catalyst", "stocks regime label: bullish (bias=long) per stocks-intraday report, but market not yet open"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mapping_weak", "stale_catalyst", "no_catalyst", "fresh_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 295/1500 mapped (19.7%), 80.3% unmapped this run", "ACE Bitget PoolX/airdrop catalyst still dated 2026-08-13 (6d stale), confirmed via WebSearch + 0 news_items hits in 24h", "XRP: primary-source Ripple/Jeonbuk Bank catalyst still active in today's news feed", "momentum_breakout basket (BTW/USDT primary) explicitly flagged avoid_chase by its own playbook"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "data_unavailable", "oi_supports"], "data_missing": ["OI% for several MEXC-fallback names (ACE, PUMP, HEMI, KII — OI change n/a)", "SNXXB/SOXLB: futures data unavailable entirely"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE funding still negative (-0.0022 to -0.0028 across cycles), crowding elevated/unknown", "SNXXB/SOXLB short candidates explicitly capped to C-tier for thin_liquidity_short_squeeze_risk", "GPS/HEMI: price up + OI up = fresh positioning confirms trend (from earlier scalp derivatives block)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["chase_risk", "overextended", "entry_late"], "data_missing": ["current EDEN/USDT price vs its 0.045972 invalidation"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE 24h cooled from +45% (04:39 review) to +19.9-21% (this cycle) but still extended, no fresh catalyst", "BTW/USDT +65.7% 24h, momentum_breakout basket explicitly tags avoid_chase", "EDEN/USDT now scored short (-10.7% to -12% 24h, weak_rs_short) while an open LONG position exists on it"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["entered_unresolved", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 43 active B-tier (0 A-tier), all ENTERED (17 triggered / 18 tp1_hit / 8 tp2_hit) — 0 waiting_for_entry, 0 fresh open-actionable this cycle", "stocks: 50 active (3 A-tier GE all tp1_hit, 2 B-tier tp1/tp2_hit, 45 C-tier never-actionable incl. 2 waiting_for_entry)", "25/43 crypto active rows have expires_at already elapsed (oldest: NEAR/USDT, expired 2026-07-17, 33d overdue) with no closing status recorded", "detect_untracked_legacy_alerts: 0 findings"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["correlation_cluster", "reduce_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TWO concurrent ACE/USDT B-tier swing longs open simultaneously (score 65.4 entered 01:46, score 65.6 entered 2026-08-18 21:00) plus an ACE intraday tp1_hit — correlated duplicate exposure on one symbol with a stale catalyst", "EDEN/USDT bias-tag contradiction (open long vs. current short score) mirrors the ZBT/ACE pattern already tracked in memory as a HIGH-priority recurring issue", "20 open crypto B-tier longs remain mostly altcoin-beta correlated to BTC/risk mood", "WMT earnings tomorrow (2026-08-20) — do-not-chase warning already active in production risk layer"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_narrative_rs_momentum: 14d WR72%/PF5.80 — the desk's one clearly edge-positive crypto cohort, confirmed again this cycle (mode=swing PF7.40, totalR +32.0)", "crypto intraday no-catalyst momentum: WR23%/PF0.70, weak", "crypto scalp: PF0.50, weak, kill-switch off", "stocks A-tier week sample: n=12, PF=0.0, totalR -1.0 — small-sample but negative, consistent with the standing stocks A/B rolling-drawdown caution already in place"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.68,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "GPS/USDT", "trigger": "hold existing entered position (zone 0.01707-0.01755, stop 0.01649); add only on a clean retest, not a chase — no fresh catalyst so this stays pure RS/momentum, sized small", "reason": "already-open B-tier swing long, RS-leader, moderate (not extreme) extension, sits in the desk's one proven-edge cohort (crypto_swing_narrative_rs_momentum, 14d WR72%/PF5.80); cleaner than ACE because it is not carrying duplicate/correlated exposure" },
    "best_short_candidate": { "symbol": "SNXXB/USDT", "trigger": "wait for a confirmed breakdown continuation with derivatives data available (currently unavailable) before sizing; do not short the raw print — squeeze risk explicitly capped this to C-tier three reports running", "reason": "most persistent weak_rs_short across scalp/intraday/swing (-12% to -16% 24h each cycle), but thin liquidity + no futures data means this is confirmation-only, not yet actionable" },
    "best_catalyst_candidate": { "symbol": "XRP/USDT", "trigger": "watch for RS vs BTC to turn positive on continued volume alongside the still-fresh Ripple × Jeonbuk Bank cross-border payments news (The Block, primary source); no formal signal yet", "reason": "only symbol this cycle with an unambiguous, primary-sourced, uncontradicted catalyst" },
    "avoid_candidate": { "symbol": "ACE/USDT", "reason": "correlated double-exposure — two concurrent B-tier swing longs plus an intraday tp1_hit, all riding the same 6-day-stale Bitget PoolX catalyst (confirmed via WebSearch: listing dated 2026-08-13, no update since), funding still negative/crowded; this is the third consecutive review flagging ACE chase/correlation risk" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | caution | 0.65 | chop, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.70 | mapping_weak, stale_catalyst, no_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, data_unavailable, oi_supports | advisory_only |
| technical_entry | caution | 0.70 | chase_risk, overextended, entry_late | advisory_only |
| execution_lifecycle | caution | 0.70 | entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.70 | correlation_cluster, reduce_risk, manual_review | advisory_only |
| playbook_performance | ok | 0.75 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.68 | — | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_0439.md` (04:39 EEST):

- **ACE/USDT** — extension has *cooled*, not worsened: was +45.4% 24h at 04:39, now +19.9-21% (still well up, but pulling back from the overnight spike). However, a **second** ACE B-tier swing long triggered overnight (score 65.4, entered 01:46, zone 0.2287-0.2358) on top of the already-open 65.6-score position from the 04:39 review — this is a new, more serious concern (correlated duplicate exposure) than the prior single-position chase-risk call. Avoid-chase call upgraded to avoid-and-flag-duplicate.
- **GPS/USDT** — still open/triggered, unchanged plan; promoted here to best long-watch (was co-#1 in the 04:39 review) since ACE is now disqualified by the duplicate-exposure issue.
- **KORUB/USDT** — the 04:39 review's short-watch pick has dropped out of today's top-movers list entirely (not in scalp/intraday strongest/weakest this cycle); no longer a live candidate. Replaced by **SNXXB/USDT**, which has been consistently weak (weak_rs_short) across all three reports today.
- **HOLO/USDT and PROM/USDT** — both flagged as imminent expirations in the 04:39 review (04:48 and 05:40 EEST respectively) have since aged out of the active-signals list entirely (validity window closed); no longer visible in current active-signals output, consistent with an unresolved-expiry close rather than a new alert.
- **New this cycle:** the expires_at-vs-status data-integrity finding (25/43 crypto active rows past expiry, still `tp1_hit`/`tp2_hit`) — not visible in the 04:39 review's scope; discovered via direct SQL cross-check this cycle. See §14.
- **New this cycle:** EDEN/USDT bias-tag contradiction (open long vs. current short score) — not flagged in the 04:39 review; discovered by cross-referencing the open-signals table against today's "Weakest Symbols" section.
- **Stocks:** no material change — still 0 actionable A/B, market still closed/pre-open; WMT earnings-tomorrow warning persists.

## 5. Catalyst Coverage

- Total catalyst_events today (raw rows in `catalyst_events.jsonl`): **1500** (≈976 unique by title — the file accumulates near-duplicate rows across scan cycles)
- Mapped (symbol present): **295** (19.7%)
- Unmapped (null symbol): **1205** (80.3%)
- Narrative baskets: **5**

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (Consistent with the recurring gap already tracked in memory, `project_crypto_ai_desk_news_layer_hardening`.)

Top unmapped headlines:
1. "Ping An Good Doctor Announces 2026 Interim Results"
2. "SOUTH KOREA'S STOCK MARKET OPENS SHARPLY LOWER AMID HEAVY SELLING IN US TECH SHARES"
3. "GOLD GAINS ON EASING FED RATE HIKE HOPES, PHYSICAL DEMAND" (WSJ)
4. "Baidu (BIDU) Q2 2026 Earnings Call Transcript"
5. "uCloudlink (UCL) Q2 2026 Earnings Call Transcript"

None of these are crypto-specific misses — the unmapped set continues to skew toward macro/equities/earnings-transcript items the resolver isn't expected to tag tightly, a lower-severity version of the gap. Still logged per the >50% rule.

## 6. Market Landscape

### Market Mood / Risk Routing
- **Crypto mood:** range/chop internally (BTC/ETH local "uptrend" per the desk's own indicators, altcoin breadth 43.6-46.2%), sitting inside an externally-confirmed **cautious consolidation** backdrop: BTC ~$62-64k, ETH ~$1,800-1,950, described by Sunday Guardian (2026-08-19) as a "wait-and-watch phase" where "softer US inflation data has not yet delivered a decisive recovery." Today's Fed July FOMC minutes release is the identified swing factor for the rest of the session.
- **Stocks mood:** **pre-market / not yet open** (11:39 EEST ≈ 04:39 ET, US cash opens 09:30 ET / 16:30 EEST). Internal regime label reads "bullish (bias=long)" from the stocks-intraday report, but per the standing hardening rule this is planning/watchlist context only until RTH confirmation — see the 16:20 pre-open slot for the next real read.
- **Dominant narrative:** no single narrative running hot; `ai_narrative` (NEAR/RENDER/TAO/FET) and `perps_dex_narrative` (HYPE, wait_pullback) persist from this morning, and a new `momentum_breakout` basket (BTW/USDT primary) is explicitly tagged `avoid_chase` by its own playbook — a useful self-flag.
- **Preferred side now:** **wait-for-trigger**, leaning on the swing RS+momentum cohort (14d WR72%/PF5.80) for holds, not fresh intraday chases. No-catalyst intraday momentum remains a weak cohort (WR23%/PF0.70).
- **Best long candidate:** GPS/USDT (hold/retest only — see §8).
- **Best short candidate:** SNXXB/USDT (confirmation-only — see §8).
- **Best catalyst-backed candidate:** XRP/USDT (watch-only — see §8).
- **What to avoid:** ACE/USDT (duplicate exposure + stale catalyst); do not add to MMT/USDT (aging short, let it run to its own plan).
- **What would change the view:** a confirmed BTC reclaim of the local range high with OI expansion; the Fed minutes release providing a clear risk-on/risk-off signal; catalyst mapping recovering above 50%; US cash open confirming or invalidating today's "bullish" stocks-regime label.

## 7. Candidate Deep Dives

### 7.1 GPS/USDT (crypto, B-tier swing, score 72.2, ENTERED UNRESOLVED / open — best long-watch)
- Filled zone 0.01707-0.01755, invalidation 0.01649, TP1 0.01913, TP2 0.02019.
- Has price already reacted? Yes — position is filled; this is a hold/monitor, not a fresh-entry decision. New size only on a clean retest of the zone, not a chase.
- Overextension check: moderate, not extreme (consistent with the 04:39 review's read; no new data changes this).
- Catalyst: none confirmed — pure RS/momentum play under `crypto_swing_narrative_rs_momentum` (14d WR72%/PF5.80).
- Aligned with market mood: partially — crypto mood is cautious/consolidating, so this stays a small, RS-backed hold rather than a basis for adding broad risk.
- Chase risk: low for the existing position; would be moderate for fresh size above 0.0180.
- Invalidation: 0.01649, or a broad BTC breakdown dragging correlated alt-longs.

### 7.2 ACE/USDT (crypto, B-tier swing ×2 + intraday tp1_hit — AVOID adding, correlation-cluster flag)
- **Position A:** filled zone 0.2230-0.2306, stop 0.2138, TP1 0.2559, TP2 0.2728, entered 2026-08-18T21:00.
- **Position B (new this cycle):** filled zone 0.2287-0.2358, stop 0.2199, TP1 0.2549, TP2 0.2708, entered 2026-08-19T01:46 — this is a *second* concurrent swing long on the same symbol, opened roughly 4.5h after Position A, at a nearly identical entry zone.
- Plus an intraday B-tier long already at tp1_hit (zone 0.2134-0.2211).
- 24h move has cooled from +45.4% (04:39 review) to +19.9-21% across today's scans — still extended but less acute than overnight.
- Catalyst: confirmed via WebSearch (Fusionist/ACE — CoinMarketCap, Changelly, CoinGabbar) that the driving catalyst remains the Bitget PoolX listing + 110,000 ACE airdrop dated **2026-08-13** — still 6 days stale, no update found. Internal `news_items` query: **0 ACE hits in the last 24h**, confirming no fresh catalyst.
- Derivatives: funding still negative (-0.0022 to -0.0028 depending on report cycle), crowding elevated/unknown.
- **Verdict: do not add new size.** Two concurrent same-symbol swing longs plus an intraday position is correlated exposure the desk did not have at the 04:39 review — this is now a portfolio-construction flag, not just a chase-risk note. Existing positions ride their own plans unaffected.

### 7.3 EDEN/USDT (crypto, B-tier swing, score 73.2, ENTERED UNRESOLVED / open — bias-tag contradiction, NEEDS REVIEW)
- Open position: filled zone 0.049980-0.051593, invalidation 0.045972 (≈8.5% below the zone low), TP1 0.0559 (per the 04:39 review's earlier read), expires 2026-08-25T14:39:39.
- **Contradiction:** today's scalp (07:05) and intraday (07:13) "Weakest Symbols" sections both independently score EDEN/USDT as **bias short**, 24h **-10.7% to -12.2%**, and the intraday expansion watchlist explicitly lists it under `weak_rs_short` / `crypto_failed_bounce_short` (rejected to C for squeeze risk, not promoted).
- This is the same open-long-vs-current-short-score pattern already tracked in memory as a recurring, HIGH-priority issue (confirmed previously on ZBT/USDT and ACE/USDT, 3 consecutive reviews on 2026-08-08). EDEN is a new instance of the same pattern.
- **Data gap:** current EDEN/USDT live price is not available from the allowed read set (no OHLCV table in the SQLite DB used this run; the reports only give 24h % change, not a fresh spot price) — cannot directly confirm proximity to the 0.045972 invalidation this cycle. Flagged as `data_missing` for the technical_entry/execution_lifecycle agents.
- **Recommendation:** operator should pull EDEN/USDT's current price against the 0.045972 stop directly (outside this review's allowed toolset) before the next scheduled cycle, given the position is down materially against its own thesis per today's independent scoring.

### 7.4 SNXXB/USDT (crypto, C-tier / rejected, short-watch)
- 24h -12.2% to -16.1% across today's three reports, RS vs BTC similarly negative — the most persistent weak_rs_short name today (present in scalp, intraday, and swing).
- Capped to C-tier every cycle for `thin_liquidity_short_squeeze_risk` / `no_derivatives_thin_short` — "futures data unavailable" in both the direct and Bybit/OKX cross-check sections.
- Has price already reacted? Yes, the decline is already underway; shorting the raw print is chasing an extended move without derivatives confirmation.
- What would make it actionable: derivatives data becoming available (currently a hard blocker) plus a failed-retest structure, not the raw breakdown.
- Not aligned with a "high-confidence" call this cycle — this is a confirmation-only watch item, explicitly not yet tradable.

### 7.5 XRP/USDT (crypto, no formal signal — catalyst-watch)
- Catalyst: Ripple × Jeonbuk Bank (South Korea) cross-border payments partnership, sourced from The Block (primary source), still present in today's catalyst feed with no contradicting risk tag.
- No formal A/B signal has been generated on XRP this cycle — this remains a watch-only idea pending RS vs BTC turning clearly positive alongside continued volume.
- Aligned with market mood: yes, in that a primary-sourced, uncontradicted catalyst is exactly the kind of setup the desk should prefer over no-catalyst chop chasing.

## 8. Best Candidates Ranked

1. **GPS/USDT** — long-watch/hold, existing entered position; add only on a clean retest of 0.0171-0.0175, not above 0.0180.
2. **SNXXB/USDT** — short-watch, wait for derivatives data + a confirmed failed-retest structure; do not short the raw -12% to -16% print.
3. **XRP/USDT** — catalyst-watch, primary-sourced Ripple × Jeonbuk Bank news; watch for RS vs BTC to turn positive before treating as actionable.
4. **EDEN/USDT** — existing open long, NEEDS REVIEW given the bias-tag contradiction in §7.3; not a fresh entry idea, included here as an operator-attention item.
5. **ACE/USDT** — explicitly the avoid/correlation-cluster candidate this cycle (§7.2 and §9); included only because it is the most-discussed name in the scan, not as a fresh trade idea.

## 9. Avoid / No Trade (this decision window only)

- **Adding to ACE/USDT** — two concurrent B-tier swing longs already open on the same symbol, riding a 6-day-stale catalyst with negative/crowded funding; this is a portfolio-correlation issue, not just a chase-risk note.
- **Shorting SNXXB/USDT at market** — no derivatives confirmation available; only the failed-retest variant (once data exists) is actionable.
- **Chasing BTW/USDT** (+65.7% 24h) — its own `momentum_breakout` basket playbook explicitly tags this `avoid_chase`.
- This is a decision-window call only — scanning, candidate generation, tracking, and outcome recording all continue uninterrupted. Nothing here is a command to pause any part of the system.

## 10. Main Risks

- **ACE/USDT correlated double-exposure:** two concurrent same-symbol swing longs plus an intraday tp1_hit position, all dependent on the same stale catalyst thesis — if the Bitget PoolX narrative fully fades, all three positions are correlated to the same failure mode simultaneously.
- **EDEN/USDT bias-tag contradiction:** an open long held against a current independent short score is either (a) a normal "thesis is now under pressure, watch the stop" situation, or (b) a recurrence of the tracked bias-tag bug pattern (ZBT/ACE precedent). Cannot be resolved from this review's allowed toolset — needs an operator price check.
- **Stale unresolved signals:** 25/43 active crypto signals (58%) have an `expires_at` already in the past while still carrying `tp1_hit`/`tp2_hit` status — this both clutters the "active" view and may be excluding real outcomes from the win/loss stats used elsewhere in this review (see §14).
- **Catalyst mapping weak (80.3% unmapped):** reduces confidence in the aggregate catalyst_events feed as a primary filter this run; per-symbol `news_items` queries remain the more reliable check.
- **Derivatives data gaps:** SNXXB/SOXLB (today's clearest short-watch names) both have "futures data unavailable," so the derivatives_squeeze agent cannot evaluate crowding/funding on them.
- **Fed minutes today:** a scheduled macro catalyst not yet reflected in any internal report; could move both BTC/ETH and the US equity open materially in either direction.

## 11. Action Plan — next 4 hours

- Do not add to ACE/USDT in either direction; let both existing swing positions and the intraday tp1_hit ride their own plans.
- Get an operator eyes-on EDEN/USDT's current price vs. its 0.045972 invalidation before the 16:20 pre-open slot — this review could not verify it from the allowed read set.
- Watch for the Fed July FOMC minutes release and re-assess crypto mood; also treat it as a possible mover into the US cash open.
- Track XRP/USDT for RS-vs-BTC confirmation on the Ripple/Jeonbuk Bank catalyst; not yet actionable.
- Build the US-session stocks watchlist from today's C-tier scan (77 C-tier ideas, 49 gate-demoted) but do not treat any of it as confirmed until RTH — hand off to the 16:20 pre-open slot.
- Flag the 25 stale-past-expiry crypto signals for a manual DB check outside this review's scope (see §14).

## 12. Final Verdict per Mode

- **Crypto scalp:** no A/B setups this cycle; kill-switch remains off for the mode (14d WR12%/PF0.14 standing caution, unchanged).
- **Crypto intraday:** no A/B setups this cycle; ACE/USDT and PUMP/USDT sit as watchlist-only (scores 53.4 / 50.4) pending cleaner confirmation — treat as research-grade only.
- **Crypto swing:** the desk's one clearly edge-positive cohort (14d WR72%/PF5.80, this-week PF7.40/totalR+32.0); GPS/USDT is the highest-confidence hold, ACE/USDT is now a correlation-risk flag rather than a clean hold, EDEN/USDT needs an operator price check.
- **Stocks (all modes):** market not yet open — C-tier watchlist only, never actionable. 0 actionable A/B intraday, 49 gate-demoted this cycle. WMT earnings-tomorrow do-not-chase warning stands.
- **Stocks position framework (shadow):** not re-reviewed this cycle (crypto-focused pre-US slot); unchanged from the last dedicated scan per memory.

## 13. Sources

- [Bitcoin and ethereum prices today, Tuesday, August 18, 2026: Crypto prices mixed as Iran stalemate continues](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-august-18-2026-crypto-prices-mixed-as-iran-stalemate-continues-155702632.html) — Yahoo Finance, 2026-08-18.
- [Crypto Price Prediction August 19, 2026: Bitcoin Eyes $64K, Ethereum Tests $1,900 and XRP Defends $1 Ahead of Fed Minutes](https://sundayguardianlive.com/business/crypto-price-prediction-august-19-2026-bitcoin-eyes-64k-ethereum-tests-1900-and-xrp-defends-1-ahead-of-fed-minutes-263681/) — Sunday Guardian, accessed 2026-08-19 (fetched and verified).
- [Latest Fusionist News - (ACE) Future Outlook, Trends & Market Insights](https://coinmarketcap.com/cmc-ai/fusionist/latest-updates/) — CoinMarketCap, accessed 2026-08-19; confirms Bitget PoolX listing dated 2026-08-13.
- [Fusionist Price Prediction: Is ACE Breaking Its Long Downtrend?](https://www.coingabbar.com/en/price-prediction/fusionist-price-prediction-ace-breakout-attempt) — CoinGabbar, accessed 2026-08-19.
- Internal: `data/reports/scalp/2026-08-19_07-05_scalp_report.md`, `data/reports/intraday/2026-08-19_07-13_intraday_report.md`, `data/reports/swing/2026-08-19_01-46_swing_report.md`, `data/reports/stocks/intraday/2026-08-19_07-39_stocks_intraday_report.md`, `data/catalysts/2026-08-19/catalyst_events.jsonl`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items`), `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_0439.md`.

## 14. Fix Requests / TODO

### TODO-stale-active-signals-past-expiry
- **issue:** 25 of 43 "active" crypto signals returned by `active-signals --asset-class crypto` (58%) have an `expires_at` value already in the past — some by over a month (NEAR/USDT scalp short, `expires_at=2026-07-17`, status `tp1_hit`, 33 days overdue as of this review) — yet remain in a non-terminal `tp1_hit`/`tp2_hit` status with no final win/loss recorded. This both clutters operator-facing "active" views and potentially excludes real outcomes from the win/loss stats consumed by `signal-stats` and this review.
- **evidence:** SQL cross-check this run: `SELECT tier, status, COUNT(*) FROM proposed_signals WHERE asset_class='crypto' AND status IN ('waiting_for_entry','triggered','tp1_hit','tp2_hit') AND expires_at > datetime('now')` returns only 18 rows, vs. the CLI's 43 "active" rows — a 25-row gap, all past-expiry. Oldest example: `sig_b16bb9e54598333a` NEAR/USDT, `expires_at=2026-07-17T15:56:12`.
- **suggested manual fix:** have the monitor/outcome-recording pipeline sweep `tp1_hit`/`tp2_hit`/`triggered` rows past their `expires_at` and resolve them to a terminal status (e.g., `expired_after_partial_tp`) with the R captured at expiry, so `active-signals` reflects genuinely live positions and `signal-stats` isn't silently missing this tail.
- **priority:** medium
- **first observed (this thread):** 2026-08-19 11:39 EEST.

### TODO-eden-bias-tag-contradiction
- **issue:** EDEN/USDT is held as an open B-tier swing LONG (invalidation 0.045972) while today's scalp and intraday scans independently score it as a SHORT candidate (`bias short`, 24h -10.7% to -12.2%, `weak_rs_short` / `crypto_failed_bounce_short`, rejected to C for squeeze risk). This is the same open-long-vs-current-short-score pattern already tracked in memory (`project_crypto_ai_desk_bias_tag_contradiction`) as confirmed on ZBT/USDT and ACE/USDT across 3 consecutive reviews on 2026-08-08, escalated to HIGH priority there. EDEN/USDT is a new symbol instance of the same pattern.
- **evidence:** `data/reports/intraday/2026-08-19_07-13_intraday_report.md` line 52 ("EDEN/USDT: bias short, 24h -10.74%...") and line 400 (`weak_rs_short` / rejected) vs. `active-signals --asset-class crypto` row `sig_35833f0f33a66222` EDEN/USDT B swing long triggered, entry 0.049980-0.051593, invalidation 0.045972.
- **suggested manual fix:** investigate whether the bias/direction tag computed for "Weakest Symbols" display is meant to reflect an independent fresh scan (in which case this is expected — a held long simply moving against thesis) or whether it's a genuine mislabeling bug in the same code path already flagged for ZBT/ACE. If the former, consider a report-level annotation ("already held long — current scan reads short") so operators don't have to cross-reference manually, as this review had to.
- **priority:** high (escalated to match the existing memory-tracked pattern's priority)
- **first observed (this thread):** 2026-08-19 11:39 EEST (recurring pattern — see linked memory for ZBT/ACE precedent, 2026-08-08).

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-mapping coverage is weak again this run (295/1500 mapped, 80.3% unmapped) — consistent with the recurring mapping-gap pattern already tracked in memory (`project_crypto_ai_desk_news_layer_hardening`).
- **evidence:** `data/catalysts/2026-08-19/catalyst_events.jsonl` — 1205/1500 raw rows have no `symbol` field; top unmapped headlines are macro/equities/earnings-transcript items (Ping An Good Doctor, South Korea market open, gold/Fed, Baidu/uCloudlink earnings transcripts) the current resolver doesn't attempt to tag.
- **suggested manual fix:** unchanged from the 04:39 review — revisit symbol resolver coverage for macro/equities-adjacent headlines, or scope the mapping-rate metric to crypto-relevant sources only.
- **priority:** low (recurring, already tracked, no new severity this cycle)
- **first observed (this thread):** 2026-08-19 11:39 EEST (recurring — see `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_0439.md` for the prior instance).
