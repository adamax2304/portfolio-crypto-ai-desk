# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:30 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review**. Advisory only — no auto-trade, no scoring/threshold/routing changes. **Pre-US schedule check: target 08:55 ET, actual fire 08:58 ET (Δ+3min, within tolerance).** By the time this review completed (~35min of research), the US cash session had just opened (09:30 ET) — treat this as a final pre-open read that hands off directly into the 18:30 open-reaction slot; no fresh RTH price data was available to this run.

**Top finding this cycle: GPS/USDT — an open B-tier crypto swing LONG (entered 0.01707-0.01755, invalidation 0.01649) — is now independently scored SHORT by both today's swing and intraday scans, 24h -29.92%, RS vs BTC -30.24%.** This is the third instance of the recurring open-long-vs-current-short-score bias-tag pattern (after ZBT/ACE and EDEN/USDT), and by far the most severe: a -30% adverse move dwarfs the position's ~3.4%-wide invalidation, yet `active-signals` still shows it `triggered` (not stopped/closed). This could not be resolved from this review's allowed toolset (no live-price read) — escalated to HIGH priority, see §7.1/§14.

Crypto: no new A/B setups this cycle (scalp kill-switch off, intraday watchlist-only). ACE/USDT's correlated double-exposure (2 concurrent swing longs + 1 intraday tp1_hit, flagged in the last two reviews) persists and has **re-accelerated to +28.4% 24h with zero fresh catalyst in 24h** (still the same 7-day-stale Bitget PoolX story) — now a no-catalyst chase, not just a stale-catalyst hold.

Stocks pre-US overlay (this slot's required extension): ran `stocks-preus-candidates` (35 eligible / 55 excluded) and reviewed all 35. **Zero SUPPORT verdicts** — every candidate lacked genuine RS-vs-sector/SPY confirmation (Alpha Vantage realtime quotes were rate-limited/premium-gated this run), so per the overlay's own rule none qualify for promotion; 4 BLOCK verdicts including a real catch (**WMT has earnings tomorrow, 2026-08-20** — the preus gate did not catch this) and **3 catalyst-entity-mismatch bugs** (ARM/V/ETN — ticker collisions with unrelated non-stock terms). The `stocks-preus-review-ingest` write step **failed twice (SQLite `database is locked`, then a 2min timeout)** — the live scheduler holds the DB; verdicts were NOT persisted this run, see §14.

Catalyst mapping weak this run (79.8% unmapped) — context only. No untracked-alert integrity issues.

## 2. Data Used

- Reports: scalp (2026-08-19 13:04 EEST, fresh ~2h56m), intraday (13:11, fresh ~2h48m), swing (04:46, ~11h14m old → 4-12h band, carry-forward), stocks intraday (13:40, fresh ~2h20m, pre-market at generation time), stocks swing/invest (deprecated, stale since 2026-07-02 — excluded).
- `data/processed/llm_analysis_packet.md` (13:12), `data/processed/llm_stocks_packet.md` (13:41) — freshness-checked, content overlaps reports above.
- `data/catalysts/2026-08-19/catalyst_events.jsonl` (2000 parsed rows this run), `narrative_baskets.jsonl` (5 baskets).
- SQLite `db/crypto_ai_desk.sqlite`: `proposed_signals` (active-signal status), `news_items` (per-candidate 24h catalyst checks, ~32 tickers queried).
- CLI: `active-signals` (crypto 46 rows, stocks 50 rows), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-08-19` (0 findings), `stocks-preus-candidates` (35 eligible / 55 excluded).
- External: Alpha Vantage `MARKET_STATUS` (rate-limited, failed), `GLOBAL_QUOTE` ×2 (SPY, QQQ — succeeded, delayed/prior-close data), `REALTIME_BULK_QUOTES` (premium-gated, failed). WebSearch ×3 (pre-market futures/VIX/Fed minutes, Marvell/Google deal verification, CrowdStrike downgrade/earnings verification) + implicit fetch of search-result content for all three.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_1139.md` (11:39 EEST cycle).

## 3. Scheduler / Data Freshness

- **Pre-US schedule check: target 08:55 ET, actual fire 08:58 ET (Δ+3min, within tolerance).** No DST-window flag needed (outside the 2026-03-08/03-29 and 2026-10-25/11-01 mismatch windows).
- Active scheduler folder is `data/scheduled_runs/2026-08-18_default_schedule/` (naming carries over the midnight rollover, same pattern noted in prior reviews): `scheduler.log` mtime **~13:56 EEST** (~2-3 min old at check time), latest `cycle_07_12-54_summary.md` mtime **~13:55 EEST** (~2h old) — both well inside the 3h defer threshold, not deferred.
- A separate, stale `2026-08-19_default_schedule/scheduler.log` exists (mtime 02:38 EEST) with dry-run validation entries only, no cycle summaries — same same-day-rollover artifact noted in the last two reviews, not the active log.
- Reports: scalp/intraday/stocks-intraday all fresh (<3h). Swing carry-forward (~11h, inside 4-12h band per spec, near the upper edge — treat with more caution than the 11:39 review's ~7h read).
- Catalyst data fresh (generated same-day, actively growing).
- No monitor/paper-portfolio status file read this run (outside the allowed read set); lifecycle status inferred from `proposed_signals`.
- **`stocks-preus-candidates` took ~3-5min to complete (once timed out at the 2min tool default, succeeded on retry with an extended timeout) — noted as a latency risk for this slot given the tight pre-open window.**
- **`stocks-preus-review-ingest` failed twice: first `OperationalError: database is locked`, then a clean 2-minute timeout on retry with no output** — the live scheduler process holds the DB. Verdict JSON was saved to the allowed path but NOT ingested. See §14.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-19 16:30 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["live spot price for GPS/USDT and EDEN/USDT (no OHLCV table in allowed read set)", "Alpha Vantage realtime quotes (rate-limited/premium-gated)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle_07 summary both ~2h old, not deferred", "swing report ~11h14m old, near upper edge of 4-12h carry-forward band", "stocks-preus-review-ingest failed twice (DB locked, then timeout)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"], "data_missing": ["VIX live level (MARKET_STATUS rate-limited)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH internal uptrend but regime label range/chop(neutral), altcoin breadth 43.6-48.7%", "stocks: internal regime label bullish (20d uptrend all 4 indices, breadth 100%) but 5d pullback across all 4 indices (SPY -0.40%, QQQ -0.13%, IWM -0.25%, DIA -0.81%)", "external: SPY -0.68%, QQQ -1.69% prior session (delayed quote), VIX ~15.2-15.9 rising off 2026 lows, semis sector-led selloff per WebSearch", "futures flat/mixed pre-open per WebSearch + internal t.me/marketfeed premarket-movers snippet (ES flat, NQ -0.2%, RTY flat)", "Fed July FOMC minutes due 14:00 ET today — identified as the session's swing factor"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst", "catalyst_contradicted"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 405/2000 mapped (79.8% unmapped)", "ACE/USDT: 0 news_items hits in 24h, catalyst now 7 days stale, yet price re-accelerated to +28.4% 24h — no-catalyst chase", "MA: fresh entity-resolved catalyst (Mastercard acquired BVNK, stablecoin settlement M&A, t.me/CoinMarketCapAnnouncements 04:10 UTC)", "MRVL/AVGO/TSM/NFLX: contradicted catalysts (bullish coverage on short/CAUTION-flagged names or bearish-leaning coverage on long candidate)", "3 catalyst-entity-mismatch bugs found this run: ARM (adjustable-rate-mortgage news, not Arm Holdings), ETN (Exchange-Traded-Notes/Eaton-CA-wildfire, not Eaton Corp), V (Big V Property Group, not Visa)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable", "funding_extreme"], "data_missing": ["OI% for several MEXC-fallback names", "SNXXB futures data unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE funding still negative (-0.0022 to -0.0034 across venues), crowding elevated", "SNXXB/USDT capped to C every cycle for thin_liquidity_short_squeeze_risk / no_derivatives_thin_short"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "stale_before_entry", "entry_late"], "data_missing": ["live GPS/USDT and EDEN/USDT spot price vs invalidation"],
      "suggested_effect": "advisory_only",
      "facts_used": ["GPS/USDT: independently scored bias short, -29.92% 24h, while an open long sits on it — cannot confirm proximity to invalidation 0.016491 from allowed toolset", "ACE/USDT: +28.4% 24h with 0 fresh catalyst — textbook no-catalyst chase", "semiconductors sector explicitly weak (RS vs SPY 20d -5.01%) per stocks-intraday report — lends indirect RS support to semis shorts (MU/AVGO/MRVL/QCOM/TSM) even without a symbol-specific RS read"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["entered_unresolved", "no_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 46 active B-tier (0 A-tier) rows returned by active-signals; only a handful genuinely current (many tp1_hit/tp2_hit rows dated back to mid-July, same stale-status pattern flagged in the 11:39 review's TODO)", "stocks: 3 A-tier GE rows all tp1_hit before this review (pre-market fill), 45 C-tier rows never-actionable pre-open", "detect_untracked_legacy_alerts: 0 findings", "stocks-preus overlay: 35/90 candidates eligible, 0 promoted (0 SUPPORT verdicts)"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.75,
      "reason_codes": ["correlation_cluster", "reduce_risk", "manual_review", "headline_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["GPS/USDT bias-flip is the most severe instance yet of the tracked open-long-vs-current-short-score pattern (ZBT/ACE precedent, then EDEN, now GPS) — a -30% 24h move against a ~3.4%-wide stop with no closing status recorded", "ACE/USDT correlated double-exposure persists and has worsened (re-acceleration, not just staleness)", "WMT preus long candidate has earnings tomorrow (2026-08-20) — the code's preus gate did not catch this, only this review's earnings-calendar cross-check did", "stocks-preus-review-ingest DB-lock failure means today's overlay verdicts are not yet reflected in any downstream table"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing: this-week PF7.40/totalR+32.0, avgR+0.84 — the desk's one clearly edge-positive cohort", "crypto intraday: this-week PF0.79/totalR-2.1, avgR-0.12 — weak", "crypto scalp: PF0.50/totalR-0.5 — weak, kill-switch off", "stocks A/B headline (week): winrate 6.9%, PF0.125, totalR-3.5 — deeply negative; stocks C-tier watchlist also negative (PF0.29); observations flag tier=A/B/C triggered winrate all low this week"] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.62,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "HEMI/USDT", "trigger": "hold existing open B-tier swing long (entry 0.006644-0.006780, invalidation 0.006477); add only on a clean retest, not at today's +22.3% 24h print", "reason": "RS-confirmed leader (score 91.6, +22.27% 24h, RS vs BTC +21.95%), sits in the desk's one proven-edge cohort (crypto_swing_narrative_rs_momentum), and — unlike GPS — its bias tag is consistent (still scored long in today's Strongest Symbols, no contradiction found)" },
    "best_short_candidate": { "symbol": "CRWD", "trigger": "wait for RTH open + first 15-30min confirmation of rejection near the current 52-week-high area before entry; do not chase the print — needs an actual failed-retest, not just the headline", "reason": "genuinely fresh, entity-resolved catalyst (analyst piece framing a possible 20-30% post-earnings correction at 175x forward PE, Wells Fargo/TD Cowen still bullish on target but flagging 'little room for error'; earnings 2026-08-26, outside the immediate blackout window) — the cleanest short thesis found this run, downgraded from SUPPORT to NEUTRAL only because RS-vs-sector could not be confirmed (data limits, not a flaw in the catalyst)" },
    "best_catalyst_candidate": { "symbol": "MA", "trigger": "watch RTH open reaction; would need RS vs SPY/financials turning clearly positive intraday before treating as more than a watch — no formal signal exists yet, this is the preus overlay's catalyst read only", "reason": "Mastercard acquired BVNK (stablecoin settlement infrastructure) — fresh (04:10 UTC today), entity-resolved, uncontradicted, the single cleanest catalyst found across all 35 preus candidates reviewed this run" },
    "avoid_candidate": { "symbol": "GPS/USDT", "reason": "open B-tier swing long now scored bias-short at -29.92% 24h by two independent scans — the most severe instance of the recurring bias-tag-contradiction pattern; do not add, and flag for urgent operator price/stop check (secondary avoid: WMT preus long — earnings tomorrow, 2026-08-20, gate-missed)" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.60 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.65 | mapping_weak, no_catalyst, fresh_catalyst, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable, funding_extreme | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, stale_before_entry, entry_late | advisory_only |
| execution_lifecycle | caution | 0.65 | entered_unresolved, no_entry, needs_review | advisory_only |
| risk_manager | manual_review | 0.75 | correlation_cluster, reduce_risk, manual_review, headline_risk | advisory_only |
| playbook_performance | caution | 0.75 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | manual_review | 0.62 | — | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_1139.md` (11:39 EEST):

- **GPS/USDT — new, severe.** Was the 11:39 review's #1 best-long-watch ("hold existing entered position... RS-leader, moderate extension"). It is now scored bias **short**, -29.92% 24h — a complete reversal not visible at 11:39. This supersedes GPS as a long idea entirely and becomes this cycle's top avoid/risk item.
- **ACE/USDT — worsened, not just persisted.** 24h move re-accelerated from ~19.9-21% (11:39 review) to +28.4% (this cycle), still with 0 fresh news_items hits in 24h (catalyst now 7 days stale vs. 6 at 11:39). The correlated double-exposure call stands; now compounded by a no-catalyst chase pattern on top of the stale-catalyst issue.
- **EDEN/USDT — de-escalated, not resolved.** The bias-tag contradiction flagged at 11:39 (open long vs. independently-scored short) did not re-appear in today's "Weakest Symbols" section — EDEN dropped off that list entirely this cycle. The open long position (invalidation 0.045972) is unchanged in `active-signals`. Recommend the operator still verify current price, since dropping off a top-N weakest list is not the same as the contradiction being resolved.
- **HEMI/USDT — promoted to best long-watch**, replacing GPS/USDT; RS-consistent (bias still long, no contradiction found) and already an open position.
- **CRWD — new candidate this cycle**, surfaced via the mandatory stocks-preus overlay (not reviewed at 11:39, which was crypto-only pre-market). Genuinely fresh valuation/earnings-risk catalyst found via WebSearch.
- **MA — new candidate this cycle**, also via the preus overlay; cleanest catalyst of the batch (Mastercard/BVNK acquisition).
- **WMT — new finding this cycle:** earnings tomorrow (2026-08-20) caught via the stocks-intraday report's earnings-calendar section, not by the preus-candidates gate itself — BLOCKed in this run's overlay verdict.
- **Stocks:** market was pre-market for most of this review's data-gathering window and opened (09:30 ET) only as the review was finishing — no RTH confirmation available yet, hand off to the 18:30 slot.

## 5. Catalyst Coverage

- Total catalyst_events parsed this run: **2000**
- Mapped (symbol present): **405** (20.3%)
- Unmapped (null symbol): **1595** (79.8%)
- Narrative baskets: **5**

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top unmapped headlines:
1. "Ping An Good Doctor Announces 2026 Interim Results"
2. "SOUTH KOREA'S STOCK MARKET OPENS SHARPLY LOWER AMID HEAVY SELLING IN US TECH SHARES"
3. "GOLD GAINS ON EASING FED RATE HIKE HOPES, PHYSICAL DEMAND" (WSJ)

Consistent with the recurring gap tracked in memory (`project_crypto_ai_desk_news_layer_hardening`) — unmapped items continue to skew macro/equities/earnings-transcript, not crypto-specific misses.

### Pre-US Stocks Review Overlay
- candidates reviewed: 35 (SUPPORT 0 / NEUTRAL 8 / CAUTION 6 / BLOCK 4 / INSUFFICIENT_DATA 17)
- session-cap-only C's now eligible for pre-open Paper lane: **0** — no candidate had genuine RS-vs-sector/SPY confirmation this run (Alpha Vantage realtime quotes were rate-limited/premium-gated); per the overlay's own rule, missing RS confirmation blocks SUPPORT regardless of catalyst quality.
- excluded by hard gate: 55 — dominated by `NO_ENTITY_RESOLVED_CATALYST` (44, e.g. AAPL-adjacent XLK, MCD, DDOG, ISRG, CSCO), `EARNINGS_BLACKOUT` (6: SOFI, AAPL, NET, COST, LLY, and one more), `LEGAL_RISK` (4: HD, DELL, INTU, and one more) — full list in `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`.
- **Verdict JSON built and saved** to `data/raw/enriched_review_sources/preus_review_2026-08-19T13-15-12Z.json` (35 records) but **NOT ingested** — `stocks-preus-review-ingest` hit `database is locked` then a 2-minute timeout on retry. See §14.

## 6. Market Landscape

### Market Mood / Risk Routing
- **Crypto mood:** mixed/chop. Internal indicators show BTC/ETH in a local "uptrend" with regime label "range/chop (neutral)" and altcoin breadth 43.6-48.7% (not broad participation). No single dominant narrative running hot.
- **Stocks mood:** mixed-to-cautiously-bullish going into the open. Internal regime label "bullish" (20d uptrend across SPY/QQQ/IWM/DIA, breadth 100% above EMA20/50), but 5d is negative across all four indices and semiconductors are the weakest sector (RS vs SPY 20d -5.01%). External: SPY -0.68% / QQQ -1.69% prior session (tech-led weakness), VIX up ~3.75% off 2026 lows but still low (~15.2-15.9), futures flat/mixed pre-open, Fed July FOMC minutes at 14:00 ET is the session's identified swing factor.
- **Dominant narrative:** "AI trade" debate (bull/bear split narrative in the news feed) plus semiconductor-specific weakness (Micron/Sandisk/Credo cited as AI-loss leaders); in crypto, no fresh narrative dominates — ACE's move is now unsupported by any catalyst.
- **Preferred side now:** wait-for-trigger / catalyst-backed only. Avoid chasing either the crypto no-catalyst momentum (ACE) or the stocks pre-open C-tier planning levels without RTH confirmation.
- **Best long candidate:** HEMI/USDT (crypto, existing open position — see §8).
- **Best short candidate:** CRWD (stocks, needs RTH confirmation — see §8).
- **Best catalyst-backed candidate:** MA (stocks, Mastercard/BVNK acquisition — see §8).
- **What to avoid:** GPS/USDT (bias-flip, see §7.1); adding to ACE/USDT; WMT preus long (earnings tomorrow).
- **What would change the view:** confirmed GPS/USDT live price vs. its 0.016491 invalidation; the 14:00 ET Fed minutes release; RTH open price action on CRWD/MA/MU providing real RS-vs-sector confirmation; catalyst mapping recovering above 50%.

## 7. Candidate Deep Dives

### 7.1 GPS/USDT (crypto, B-tier swing, score 72.2, ENTERED UNRESOLVED / open long — TOP RISK, bias-tag contradiction)
- Filled zone 0.017073-0.017549, invalidation 0.016491, expires 2026-08-25T14:39:39, status `triggered` (not stopped/closed).
- Both today's swing (01:46 report) and intraday (13:11 report) independently score GPS/USDT as bias **short**, 24h **-29.92%**, RS vs BTC **-30.24%**, tagged `weak_rs_short` / `crypto_failed_bounce_short`.
- Has price already reacted? If the -29.92% 24h figure is accurate, very likely yes — a move of that magnitude against an entry zone only ~3.4% above the invalidation would ordinarily already be well through the stop, yet `active-signals` shows no stopped/closed status.
- **Data gap:** current live spot price is not available from this review's allowed read set (no OHLCV/ticker table permitted) — same caveat the 11:39 review hit on EDEN/USDT, now recurring on a third symbol with a much larger move.
- Is this a chase-risk setup? N/A — this is an existing position, not a fresh entry; the question is whether it should still be held.
- What would invalidate the idea (i.e., what would resolve this either way): an operator direct price check against 0.016491, or the position's status flipping to a terminal stopped/closed state in the DB.
- **Recommendation: urgent operator price/stop check before the 18:30 slot.** This is the most severe instance yet of the tracked bias-tag pattern (ZBT/ACE → EDEN → GPS) — escalated to HIGH priority TODO.

### 7.2 ACE/USDT (crypto, B-tier swing ×2 + intraday tp1_hit — AVOID adding, correlation + no-catalyst chase)
- Two concurrent swing longs (scores 65.4 and 65.6, entered 2026-08-18 21:00 and 2026-08-19 01:46) plus an intraday tp1_hit position (score 67.8) — unchanged since the 11:39 review.
- 24h move re-accelerated to **+28.44%** (score 91.6, top of today's "Strongest Symbols"), up from ~19.9-21% at 11:39 and down from the overnight +45% peak — a re-acceleration, not a continued cooldown.
- Catalyst: confirmed again via `news_items` — **0 ACE hits in the last 24h**. The Bitget PoolX/airdrop story (dated 2026-08-13, verified via WebSearch at the 11:39 review) is now 7 days stale with no update.
- Derivatives: funding still negative (-0.0022 to -0.0034 across bybit/mexc), crowding elevated.
- **Verdict: do not add new size.** The re-acceleration with zero fresh catalyst is now a textbook no-catalyst momentum chase on top of the pre-existing correlated-exposure issue. Existing positions ride their own plans unaffected.

### 7.3 CRWD (stocks, preus overlay, pre_gate_tier B, base_score 66.1 — short-watch, needs RTH confirmation)
- Catalyst (WebSearch, verified via CNBC/Seeking Alpha/TipRanks/tradingpedia): CRWD hit a fresh 52-week high (~$227.50) before pulling back 3.8%; trading at ~175x forward non-GAAP PE ahead of Q2 FY2027 earnings (2026-08-26, ~7 days out — outside the immediate earnings-blackout window used by the gate); one analyst piece is titled around a possible 20-30% post-earnings correction risk, while Wells Fargo ($230 PT) and TD Cowen ($235 PT) remain bullish — a genuinely two-sided, fresh, entity-specific setup.
- Has price already reacted? Partially — already pulled back 3.8% from the fresh high per the sourced coverage.
- Is the setup chasing? Not if entered on a confirmed rejection; would be chasing if shorted purely off the headline without RTH structure.
- Retest/pullback structure: not yet confirmed — needs the first 15-30min of RTH to show a genuine failed-bounce, not just follow-through on the pre-existing pullback.
- Aligned with market mood: yes — semiconductors/high-multiple tech names are the market's identified weak spot this session (sector RS -5.01%, AI-panic-vs-reality framing in the same day's coverage).
- Chase-risk: moderate if entered pre-RTH-confirmation.
- **Verdict: NEUTRAL** (not SUPPORT) — catalyst is fresh and entity-resolved, but RS-vs-sector could not be confirmed this run (Alpha Vantage data unavailable); per the overlay's own rule, a missing RS leg blocks SUPPORT regardless of catalyst quality.

### 7.4 MA (stocks, preus overlay, pre_gate_tier A, base_score 99.7 — best catalyst-backed watch)
- Catalyst (internal `news_items`, t.me/CoinMarketCapAnnouncements, 2026-08-19T04:10 UTC): "Visa is looking for new stablecoin settlement partners after Mastercard acquired BVNK" — a fresh, entity-resolved, material M&A event in the stablecoin-settlement space.
- Has price already reacted? Unknown pre-open; needs RTH open to assess.
- Aligned with market mood: yes — financials sector is "mixed" (RS vs SPY +0.52% 20d), not weak, and this is a strategic-growth acquisition, not a defensive one.
- **Verdict: NEUTRAL** (not SUPPORT) — same RS-data-gap caveat as CRWD. This is the cleanest catalyst found across all 35 preus candidates reviewed this run and is the best_catalyst_candidate for that reason, even without a SUPPORT verdict.

### 7.5 WMT (stocks, preus overlay, pre_gate_tier A, base_score 83.8 — BLOCK, earnings tomorrow)
- The stocks-intraday report's own Earnings section flags **WMT: earnings next session (days_ahead=1)** and explicitly tags it `Swing-blocked by earnings` — yet the preus-candidates gate returned WMT as `eligible`/`promotable=True` (its cap reason was only `market_closed_intraday_planning_only`, not `EARNINGS_BLACKOUT`).
- This is exactly the "found something the code's hard gate could not have seen" BLOCK case the overlay is designed for.
- **Verdict: BLOCK.** Earnings tomorrow (2026-08-20) is a material, verified, pre-open risk the automated gate missed at candidate-selection time — flagged as a short-TTL veto, not a change to the underlying signal or its score.

## 8. Best Candidates Ranked

1. **HEMI/USDT** — long-watch, existing open B-tier swing position (0.006644-0.006780, stop 0.006477); RS-consistent, no bias contradiction found this cycle; add only on a clean retest.
2. **CRWD** — short-watch, wait for RTH open + 15-30min confirmation of a failed bounce near the 52-week-high area; genuinely fresh valuation/earnings-risk catalyst, but not yet RS-confirmed.
3. **MA** — catalyst-watch, Mastercard/BVNK acquisition; watch RTH reaction and RS vs SPY/financials before treating as more than a watch item.
4. **GPS/USDT** — existing open long, TOP RISK per §7.1, included here as an urgent operator-attention item, not a fresh idea.
5. **ACE/USDT** — explicit avoid/no-add per §7.2 and §9; included only because it is the most-discussed name in today's scans.

## 9. Avoid / No Trade (this decision window only)

- **GPS/USDT** — do not add; urgent operator price/stop check needed given the -29.92% 24h bias-flip against an open long (see §7.1).
- **Adding to ACE/USDT** — re-accelerated no-catalyst chase on top of pre-existing correlated double-exposure.
- **WMT (preus long)** — earnings tomorrow (2026-08-20), BLOCKed this run.
- **ARM, ETN, V (preus shorts/long)** — BLOCKed this run for catalyst-entity-mismatch, not for a trade-quality reason; their underlying signals are untouched, only this run's advisory overlay treats them as unverifiable this cycle.
- This is a decision-window call only — scanning, candidate generation, tracking, and outcome recording all continue uninterrupted. Nothing here is a command to pause any part of the system.

## 10. Main Risks

- **GPS/USDT bias-flip (new, severe):** open long against a -29.92% 24h independently-scored-short read, unresolvable from this review's allowed toolset — needs an operator price check before the next slot.
- **ACE/USDT correlated exposure + re-acceleration:** two concurrent swing longs plus an intraday tp1_hit, now compounded by a no-catalyst momentum chase.
- **stocks-preus-review-ingest DB lock:** today's 35 verdict records were built and saved but not persisted to `stocks_preus_review` — the live scheduler held the DB through two attempts (lock error, then a 2-min timeout). No downstream table reflects this run's overlay work yet.
- **Catalyst-entity-mismatch cluster (3 tickers this run: ARM, ETN, V):** a short/single-letter-ticker collision pattern in the news/catalyst resolver — worth a dedicated look, see §14.
- **WMT earnings gap in the preus gate:** the automated `stocks-preus-candidates` gate did not catch WMT's earnings-tomorrow status; only this review's manual earnings-calendar cross-check did.
- **Stale unresolved crypto signals:** the `active-signals --asset-class crypto` output continues to carry many old `tp1_hit`/`tp2_hit` rows dated back to mid-July (same pattern flagged in the 11:39 review's TODO, not yet fixed).
- **Catalyst mapping weak (79.8% unmapped):** reduces confidence in the aggregate catalyst_events feed as a primary filter this run.
- **Fed minutes at 14:00 ET:** a scheduled macro catalyst not yet reflected in any internal report; could move both crypto and the just-opened US equity session materially in either direction.
- **RS-vs-sector data gap:** Alpha Vantage realtime quotes were rate-limited/premium-gated this run, which is why 0 preus candidates could reach SUPPORT — this is a review-capability gap, not a statement that no candidate deserves promotion.

## 11. Action Plan — next 4 hours

- **Urgent:** get an operator eyes-on GPS/USDT's current price vs. its 0.016491 invalidation — top priority before the 18:30 slot.
- Do not add to ACE/USDT in either direction.
- Re-attempt `stocks-preus-review-ingest` once the scheduler's DB write window frees up (or coordinate timing with the scheduler's cycle boundaries) — the verdict JSON at `data/raw/enriched_review_sources/preus_review_2026-08-19T13-15-12Z.json` is ready to ingest as-is.
- Watch RTH open reaction on CRWD and MA for genuine RS-vs-sector confirmation (not available this run) before treating either as more than a watch item.
- Watch for the 14:00 ET Fed minutes release and re-assess both crypto and stocks mood at the 18:30 slot.
- Confirm EDEN/USDT's current price vs. 0.045972 invalidation — de-escalated but not resolved this cycle (see §4).
- Track HEMI/USDT for a clean retest entry rather than chasing the current +22.3% print.

## 12. Final Verdict per Mode

- **Crypto scalp:** no A/B setups this cycle; kill-switch remains off (standing caution, unchanged).
- **Crypto intraday:** no A/B setups this cycle; GRVT/DOS/HEMI/PUMP sit as watchlist-only ideas.
- **Crypto swing:** the desk's one clearly edge-positive cohort (this-week PF7.40/totalR+32.0); HEMI/USDT is the highest-confidence hold this cycle, GPS/USDT is now the top risk item (urgent check needed), ACE/USDT is an avoid/no-add, EDEN/USDT needs a de-escalated-but-unresolved price check.
- **Stocks (all modes):** market opened (09:30 ET) as this review was finishing — no RTH confirmation yet, hand off to 18:30 slot. Preus overlay reviewed 35 candidates, 0 promoted; CRWD/MA are the two most credible watch-only ideas, WMT is BLOCKed for earnings tomorrow.
- **Stocks position framework (shadow):** not re-reviewed this cycle (overlay work consumed the slot's stocks budget); unchanged from the last dedicated scan per memory.

## 13. Sources

- [Fed Minutes in Focus as AI Chip and Memory Stocks Diverge; Micron and Western Digital Fall Under Pressure](https://www.tradingkey.com/analysis/stocks/us-stocks/262118019-us-stock-pre-market-fed-minutes-ai-chip-memory-stocks-mu-wdc-falling-tradingkey) — TradingKey, 2026-08-19.
- [U.S. Futures Little Changed After Semiconductor-Led Selloff](https://finance.yahoo.com/markets/stocks/articles/u-futures-little-changed-semiconductor-095010099.html) — Yahoo Finance, 2026-08-19.
- [CBOE Volatility Index: VIX (VIXCLS)](https://fred.stlouisfed.org/series/VIXCLS) — FRED/St. Louis Fed, accessed 2026-08-19.
- [Marvell stock pops on report it will help Google with custom AI chips](https://www.cnbc.com/2026/04/20/marvell-stock-google-custom-ai-chips.html) — CNBC, 2026-04-20 (background, not fresh).
- [Marvell Technology's Divergent Signals: Record Growth, a $12 Billion Google Deal, and a 35% Monthly Drop](https://stockstoday.com/marvell-technologys-divergent-signals-record-growth-a-12-billion-google-deal-and-a-35-monthly-drop/) — Stocks Today, accessed 2026-08-19.
- [CrowdStrike Could Plunge 30% After Earnings](https://seekingalpha.com/article/4937308-crowdstrike-could-plunge-30-percent-after-earnings) — Seeking Alpha, accessed 2026-08-19.
- [CrowdStrike's Rally Tests Limits Ahead of Q2 FY2027 Results](https://www.tradingpedia.com/2026/08/17/crowdstrikes-rally-tests-limits-ahead-of-q2-fy2027-results/) — TradingPedia, 2026-08-17.
- [CRWD Q2 2027 Earnings Report on 8/26/2026](https://www.marketbeat.com/earnings/reports/2026-8-26-crowdstrike-holdings-inc-stock/) — MarketBeat, accessed 2026-08-19.
- Internal: `data/reports/scalp/2026-08-19_10-04_scalp_report.md`, `data/reports/intraday/2026-08-19_10-11_intraday_report.md`, `data/reports/swing/2026-08-19_01-46_swing_report.md`, `data/reports/stocks/intraday/2026-08-19_10-40_stocks_intraday_report.md`, `data/catalysts/2026-08-19/catalyst_events.jsonl`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items`), `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`, `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_1139.md`.

## 14. Fix Requests / TODO

### TODO-gps-bias-flip-severe
- **issue:** GPS/USDT is held as an open B-tier crypto swing LONG (entry 0.017073-0.017549, invalidation 0.016491, status `triggered`) while today's swing (01:46) and intraday (13:11) scans both independently score it bias **short**, 24h -29.92%, RS vs BTC -30.24%. This is the third and most severe instance of the recurring open-long-vs-current-short-score pattern (`project_crypto_ai_desk_bias_tag_contradiction`, previously confirmed on ZBT/ACE and, this week, EDEN/USDT).
- **evidence:** `data/reports/intraday/2026-08-19_10-11_intraday_report.md` "Weakest Symbols" section ("GPS/USDT: bias short, 24h -29.92%, RS vs BTC -30.24%") vs. `active-signals --asset-class crypto` row `sig_072249b271ba5109` GPS/USDT B swing long, status `triggered`, invalidation 0.016491.
- **suggested manual fix:** urgent operator price check against 0.016491; if genuinely through the stop, investigate why the position's status did not transition to a terminal stopped state. Separately, investigate whether the recurring bias-tag pattern (now 3 symbols) is a monitor-cadence gap (bias label from a fresh scan vs. an unresolved held position) or a genuine mislabeling bug in the same code path already flagged for ZBT/ACE.
- **priority:** high
- **first observed (this thread):** 2026-08-19 16:30 EEST (escalation of a recurring pattern — see linked memory for ZBT/ACE precedent 2026-08-08, and EDEN/USDT this week).

### TODO-preus-ingest-db-locked
- **issue:** `stocks-preus-review-ingest` failed twice this run: first with `sqlite3.OperationalError: database is locked` (writing to `stocks_preus_review`), then a clean 2-minute timeout with no output on retry. The live scheduler process appears to hold `db/crypto_ai_desk.sqlite` during its own write cycles, and this CLI has no apparent busy-timeout/retry-with-backoff.
- **evidence:** traceback in this run's tool output, `src/execution/stocks_preus_review.py:871` (`conn.execute(...INSERT INTO stocks_preus_review...)`) → `OperationalError: database is locked`.
- **suggested manual fix:** add a busy_timeout / short retry-with-backoff around the `stocks_preus_review` write path (SQLite supports `PRAGMA busy_timeout` cheaply), or have the scheduled-task runner check for scheduler-cycle overlap before invoking this ingest step.
- **priority:** medium
- **first observed (this thread):** 2026-08-19 16:30 EEST. The reviewed verdict JSON (35 records) is saved at `data/raw/enriched_review_sources/preus_review_2026-08-19T13-15-12Z.json` and ready to ingest once the lock clears.

### TODO-catalyst-entity-mismatch-cluster
- **issue:** 3 of the 17 promotable preus candidates reviewed this run had catalyst entries that do not actually refer to the underlying company: **ARM** (matched a BlackRock/Oaktree "ARM" news item about adjustable-rate mortgages, not Arm Holdings), **ETN** (matched "ETN" as the generic Exchange-Traded-Notes product-type abbreviation, and an unrelated "Eaton and Palisades fires" California-wildfire item, not Eaton Corp), **V** (matched "Big V Property Group," an unrelated small-cap real-estate company, not Visa). All three still passed the gate's `NO_ENTITY_RESOLVED_CATALYST` check, meaning the resolver considers these "resolved."
- **evidence:** `db/crypto_ai_desk.sqlite news_items` exact-symbol-match query this run for ARM/ETN/V — see this run's tool trace; titles quoted in §7 is not present for these three since they were BLOCKed, but the raw titles were "BLACKROCK ARM AND OAKTREE TOOK CONTROL OF MBS GROUP - FT", "BMO and REX Shares Launch MicroSectors 3x Long and -3x Short Brazil, Japan and Taiwan ETNs", and "Big V Property Group Announces Dedicated Investor-Facing Website, Big V Direct".
- **suggested manual fix:** the symbol resolver likely does simple substring/keyword matching on short tickers (1-3 letters) without a company-name/context disambiguation pass. Consider a minimum-confidence gate for tickers ≤3 characters that also appear as common English words/abbreviations (ARM, ETN, V, MA, GE, etc.) — cross-check against a company-name mention, not just the ticker string.
- **priority:** medium
- **first observed (this thread):** 2026-08-19 16:30 EEST.

### TODO-wmt-earnings-gate-miss
- **issue:** WMT was returned as `eligible`/`promotable=True` by `stocks-preus-candidates` (pre_gate_tier=A, base_score=83.8, cap_reasons only listed `market_closed_intraday_planning_only`), but the same day's `stocks-intraday` report independently flags **WMT: earnings next session (days_ahead=1)** and tags it `Swing-blocked by earnings`. The preus gate's earnings-blackout check did not catch this (compare: SOFI/AAPL/NET/COST/LLY were correctly excluded with `EARNINGS_BLACKOUT` this same run).
- **evidence:** `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (WMT listed under `## Eligible`) vs. `data/reports/stocks/intraday/2026-08-19_10-40_stocks_intraday_report.md` §3 ("WMT: earnings next session (unknown) (days_ahead=1)", "**Swing-blocked by earnings:** WMT").
- **suggested manual fix:** investigate why WMT's earnings-tomorrow status didn't trigger the same `EARNINGS_BLACKOUT` exclusion reason applied to SOFI/AAPL/NET/COST/LLY in the same run — possible off-by-one in the earnings-calendar lookahead window, or a data-source mismatch between the two commands.
- **priority:** high
- **first observed (this thread):** 2026-08-19 16:30 EEST.

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-mapping coverage is weak again this run (405/2000 mapped, 79.8% unmapped) — consistent with the recurring mapping-gap pattern already tracked in memory (`project_crypto_ai_desk_news_layer_hardening`).
- **evidence:** `data/catalysts/2026-08-19/catalyst_events.jsonl` — top unmapped headlines are macro/equities/earnings-transcript items (Ping An Good Doctor, South Korea market open, gold/Fed) the current resolver doesn't attempt to tag.
- **suggested manual fix:** unchanged from prior reviews — revisit symbol resolver coverage for macro/equities-adjacent headlines, or scope the mapping-rate metric to crypto-relevant sources only.
- **priority:** low (recurring, already tracked, no new severity this cycle)
- **first observed (this thread):** 2026-08-19 16:30 EEST (recurring — see `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_1139.md` and `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_0439.md` for prior instances).
