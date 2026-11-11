# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:10 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (target 09:00 America/New_York / 16:20 EEST). Advisory only / no auto-trade. **Time-critical 09:00 ET hand-off completed first**, at 09:02 ET (Δ+2min, within tolerance): `stocks-preus-candidates` found 25 eligible pre-open stocks candidates, all 25 were given a verdict and ingested via `stocks-preus-review-ingest --review-cycle preus_0900`, and `stocks-preus-review-health` reported **READY** (25/25 reviewed, 0 missing). Given the hand-off's own 5-minute window, 23 of 25 candidates were scored `INSUFFICIENT_DATA` (no fresh internal catalyst match found in `catalyst_events.jsonl`, no time for WebSearch per-candidate); ANET was scored `CAUTION` (-4, contradicted catalyst) and MSTR `NEUTRAL` (fresh catalyst but no RS confirmation available at hand-off time) — both later corroborated in the fuller review below. Crypto stays **risk-on**: BTC broke **$80,000** today for the first time since May on ETF inflows and short-covering ([Bloomberg](https://www.bloomberg.com/news/articles/2026-08-25/bitcoin-reaches-three-month-high-of-80-000-as-momentum-returns), [CoinDesk](https://www.coindesk.com/markets/2026/08/25/bitcoin-tops-usd80-000-solana-jumps-8-but-rally-now-runs-into-overbought-warning)) — externally confirmed, real, but CoinDesk itself flags the move as running into "overbought warning" territory, so chase risk is rising even as the trend stays intact. Stocks regime is **chop** (VIX 15.81, QQQ downtrend, breadth split 25%/75% above EMA20/50) with **zero A/B actionable stocks setups** pre-open — this is the expected, structural `market_closed_intraday_planning_only` demotion, not a quality signal; 15 raw-A candidates (KO 86, SBUX 84, MSFT 82, BIIB 82, UBER 81, GOOGL 80…) are pure watchlist until RTH confirms. Best long-watch: **KO** (stocks, cleanest raw-A score, defensive sector, no legal/catalyst contradiction found). Best short-watch: **AVGO** (stocks, semis sector weak into NVDA's earnings tomorrow) / **HEMI-TUT** (crypto, need confirmed breakdown, not the current extension). Best catalyst-backed: **MSTR** (externally-verified Canaccord $175 PT raise, same day as the BTC $80K move). Avoid/manual-review: **ANET short** (catalyst text is explicitly bullish "High-Growth Leadership and Momentum," contradicting the short thesis) and the recurring **watchlist-alert/signal-tracking bug** (4 fresh crypto alerts today — POL×2 modes, PROM, INJ — sent to Telegram with no backing `proposed_signal`, matching the known [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] pattern).

## 2. Data Used

- Time-critical hand-off: `stocks-preus-candidates` (25 eligible / 56 excluded), `data/raw/enriched_review_sources/preus_review_2026-08-25T130040Z.json` (25 verdicts), `stocks-preus-review-ingest --review-cycle preus_0900`, `stocks-preus-review-health` (READY).
- Scalp report `2026-08-25_10-34` (~2.5h old, fresh), Intraday report `2026-08-25_10-42` (~2.3h old, fresh).
- Swing report `2026-08-25_12-30` (~0.6h old, fresh).
- Stocks intraday report `2026-08-25_11-38` (~1.4h old, fresh) — explicit "MARKET CLOSED — planning / watchlist only" banner.
- Stocks swing `2026-07-02_13-03` / invest `2026-07-02_13-05` — **stale (>14h, ~54 days)**; confirmed **intentionally deprecated/removed** per `llm_analysis_packet.md` playbook table and [[project_crypto_ai_desk_stocks_position_framework]], not a pipeline failure — excluded from final verdict.
- `data/catalysts/2026-08-25/catalyst_events.jsonl` — 2000 events read (rolling file), 474 mapped / 1526 unmapped; `narrative_baskets.jsonl` — 4 active baskets per latest swing-report snapshot.
- `data/processed/llm_analysis_packet.md` (15:39 EEST), `llm_stocks_packet.md` (14:41 EEST).
- CLI: `active-signals` ×2 (crypto 50 rows, stocks 50 rows), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-08-25` (4 untracked).
- External: 3 WebSearch queries (BTC/Iran-Hormuz macro, MSTR/Canaccord price-target verification, BTC $80K rally verification) — all resolved with primary-source-grade hits (Bloomberg, CoinDesk); no WebFetch needed since WebSearch snippets themselves were sufficiently sourced and dated.

## 3. Scheduler / Data Freshness

- Pre-US schedule check: target 09:00 ET, actual hand-off completion 09:02 ET (Δ+2min, within tolerance) — no DST-window mismatch (today, 2026-08-25, is outside both documented 2026 drift windows of 2026-03-08→03-29 and 2026-10-25→11-01).
- `scheduler.log`: last write **12:53 EEST today**, ~0.15h old — fresh (well under the 3h defer threshold).
- Latest `cycle_*_summary.md`: `cycle_01_13-14_summary.md` under today's folder, same mtime — fresh. **Not deferred.**
- This resolves the prior review's `TODO-scheduler-log-cycle-summary-gap` (11:39 review): scheduler.log and cycle-summary writing are both current again today; treating that TODO as **resolved**, not carried forward.
- `detect_untracked_legacy_alerts --since 2026-08-25`: **4 untracked** crypto alerts (POL/USDT scalp+swing, PROM/USDT swing, INJ/USDT swing) — up from 0 in the last two reviews. See §7/§14.
- Monitor/paper status: `crypto_invest_forward_monitor` log not re-checked this cycle (time budget prioritized the time-critical stocks hand-off); no evidence of failure, just not re-verified.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-25 16:10 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["stocks swing/invest confirmed intentionally deprecated, not missing"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log + cycle_01 summary both ~9min old", "scalp/intraday/swing/stocks-intraday reports all <2.5h", "stocks-preus-review-health returned READY 25/25"] },
    { "agent": "market_regime", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["risk_on", "chop", "mixed", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["BTC broke $80K today, externally verified (Bloomberg/CoinDesk), ETF inflows + short-covering", "altcoin breadth 100% above EMA20/50 in intraday report", "stocks regime label chop, VIX 15.81, QQQ downtrend -3.23% 5d, breadth 25%/75% split"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["fresh_catalyst", "mapping_weak", "catalyst_contradicted"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["catalyst_events.jsonl: 2000 events, 474 mapped (23.7%) / 1526 unmapped (76.3%) — weak mapping this run", "MSTR Canaccord $175 PT raise externally verified same-day as BTC $80K", "ANET catalyst text ('High-Growth Leadership and Momentum') contradicts the short signal direction", "COST catalyst match is an entity-resolution false positive (headline used the word 'cost', not the ticker)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["oi_supports", "squeeze_risk", "data_unavailable"], "data_missing": ["stocks options/short-interest data not read this cycle"],
      "suggested_effect": "advisory_only", "facts_used": ["INJ/USDT price up + OI up +3.41%, crowding normal, funding neutral", "POL/USDT price up + OI up +9.69%, crowding normal", "ONG/USDT +35% 24h / +70% 7d — extended, volume only 0.5x — weak confirmation for a fresh chase"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "clean_retest", "entry_fresh"], "data_missing": ["TradingView / manual chart check unavailable — used only local OHLCV/ATR/EMA fields from the reports"],
      "suggested_effect": "advisory_only", "facts_used": ["INJ/USDT current price 5.870 sits right inside its own pullback entry zone 5.785-5.844, only +6.73% 24h — not overextended", "ONG/USDT and AMP/USDT both flagged by their own counter-thesis as extended/weak-volume — chase risk", "all 25 pre-US stocks candidates are pre-open planning levels only, no live tape to judge chase risk against yet"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["waiting_for_entry", "open_actionable", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto: 50 active signals, all B-tier, all long, mix of triggered/tp1_hit/waiting_for_entry, 0 expired", "stocks: 50 active signals, mostly ENTERED UNRESOLVED (tp1_hit/tp2_hit, no fresh close), 3 A-tier GE legs from 08-18/08-19 still open", "pre-US overlay: 25/25 reviewed, 0 promoted to SUPPORT (23 INSUFFICIENT_DATA, 1 NEUTRAL, 1 CAUTION), all still C-tier pre-open"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "manual_review", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["ANET short contradicted by its own catalyst text — needs manual review before RTH, not a clean short", "BLK, UNH, INTU, NVDA, BAC, SMCI all hard-excluded from pre-US eligibility on LEGAL_RISK — code gate working as intended", "NVDA/CRM/CRWD/MRVL/AFRM all in EARNINGS_BLACKOUT exclusion, INTU earnings today — do not chase any of these into the print", "4 untracked watchlist alerts today (was 0 last two reviews) — tracking-integrity regression to flag, not fixed"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto tier B: n=392, PF 2.0, totalR +67.3 (touch-based, likely overstates realistic PnL per [[project_crypto_ai_desk_touch_based_pnl]])", "crypto by-mode: one mode n=112 PF~0.0x totalR -5.5R (matches prior reviews' worst-mode = scalp pattern)", "stocks headline A/B: sample 93, winrate 5.4%, PF 1.25, totalR +2.50 — thin edge; stocks C-tier PF 0.46 — weak", "stocks intraday paper_execution_r all-direction 7d -6.7R/PF0.29/n48 — still net-negative live-like execution" ] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "KO", "trigger": "wait for RTH confirmation of the 91.97 entry / no gap-fade in the first 15-30min; defensive sector, no legal/earnings/catalyst contradiction found", "reason": "highest-scoring raw-A pre-US candidate (86.2), consumer-staples defensive, zero hard-gate flags, INSUFFICIENT_DATA verdict means neutral not negative" },
    "best_short_candidate":    { "symbol": "AVGO", "trigger": "wait for RTH confirmation of the 358.77 short trigger; needs a confirmed rejection, not a pre-market chase — semis sector weak into NVDA's earnings print tomorrow (2026-08-26)", "reason": "score 78.0, sector-level chip weakness ('every major chip stock fell Monday' per Motley Fool), but no symbol-specific catalyst found — treat as sector-thesis not catalyst-thesis" },
    "best_catalyst_candidate": { "symbol": "MSTR", "trigger": "confirmed BTC-correlation long already open (swing, score 79.6); size only on RTH confirmation, do not chase the pre-market gap", "reason": "Canaccord raised MSTR PT to $175 from $130 today, externally verified (Bloomberg/CoinDesk corroborate same-day BTC $80K context) — genuine fresh, entity-resolved, positive catalyst" },
    "avoid_candidate":         { "symbol": "ANET", "reason": "signal direction is SHORT but its own linked catalyst ('High-Growth Leadership and Momentum', NYSE:ANET explicit) is bullish — contradicted thesis, CAUTION-adjusted -4 in the pre-US overlay; needs manual review before any RTH entry either direction" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale (stocks swing/invest, intentional) | advisory_only |
| market_regime | ok | 0.70 | risk_on, chop, mixed, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | fresh_catalyst, mapping_weak, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.55 | oi_supports, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, clean_retest, entry_fresh | advisory_only |
| execution_lifecycle | caution | 0.70 | waiting_for_entry, open_actionable, needs_review | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis — see JSON) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-25_1139.md` (11:39 EEST, Europe/pre-US context slot):

- **New this cycle — the pre-US-open stocks decision hand-off**: 25 eligible candidates scored and ingested (READY), none promoted to SUPPORT given the 5-minute time budget; this is a new mechanism versus the 11:39 review, which only had the raw C-tier watchlist without any structured pre-open verdict layer.
- **Scheduler logging-path gap — resolved.** The 11:39 review's `TODO-scheduler-log-cycle-summary-gap` (scheduler.log stuck at 01:32, no cycle summary file) is gone: both are fresh as of ~12:53-13:00 EEST today. Retracting that TODO.
- **ACE/USDT invalidation-breach — improved, not fully cleared.** The 11:39 review's headline finding (open long trading through its own invalidation, bias=short tagged 3+ cycles) has partially resolved: ACE/USDT no longer appears in this cycle's "Weakest Symbols" bias=short list (only in "Unusual Volume", tagged `volume_expansion`, 24h -0.1%). The position (`sig_3e43cb2f2336cff7`) is still `status=triggered` with `invalidation=0.224443`; this read-only report set does not carry an absolute current price for ACE this cycle, so the invalidation-vs-price breach cannot be independently re-confirmed or cleared. Downgrading from "headline AVOID" to "carried-forward NEEDS REVIEW, contradiction eased" — still flagged in §14, not resolved.
- **Untracked-alert count — regression, 0 → 4.** The 11:39 and 04:39 reviews both reported 0 untracked legacy alerts; this cycle shows **4** (POL/USDT scalp 68.7 + swing 76.0, PROM/USDT swing 72.4, INJ/USDT swing 71.1) — all sent to Telegram between 09:51-12:29 EEST today with no matching `proposed_signal`. This is a fresh, concrete recurrence of [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] (previously confirmed on ALLO/USDT and BANK/USDT, escalated to HIGH 2026-07-17) — worth re-flagging with today's date as continued evidence the bug is still live.
- **VIRTUAL/USDT, NEAR/USDT (best-long / best-catalyst from 11:39)** — not in this cycle's fresh swing report top-6 ideas at all (POL/ONG/PROM/INJ/RE/AMP now rank higher); not a reversal, just rotation — no data this cycle to confirm or deny their prior theses, so not carried forward as "still best," simply superseded by fresher-ranked ideas.
- **New this cycle**: MSTR externally-verified catalyst (Canaccord PT raise) coincident with BTC's $80K break — neither appeared in the 11:39 review.
- **Crypto scalp mode** — still the worst-performing mode by loss concentration (one mode bucket this cycle: n=112, totalR -5.5R, consistent in magnitude with the 11:39 review's scalp PF 0.083/totalR -5.5R/n=111) — unchanged, still open per [[project_crypto_ai_desk_bias_tag_contradiction]]-adjacent scalp-mode TODO from prior reviews.
- **XPL/USDT bias-tag question** — still open, still `status=triggered`, not independently re-checked this cycle (time budget prioritized the stocks hand-off); carried forward unchanged.

## 5. Catalyst Coverage

- `catalyst_events.jsonl` (rolling file, 2000 events read this cycle): **474 mapped (23.7%)** / **1526 unmapped (76.3%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets: **4** active per the latest (12:30) swing-report snapshot — `perps_dex_narrative` (HYPE, fresh <1h), `ai_narrative` (NEAR/RENDER/TAO/FET, fresh <1h), `binance_ecosystem_teaser` (BNB, fresh <1h), `rwa_narrative` (ONDO/XLM, fresh <6h).
- Top unmapped headlines (RBA monetary-policy wires — macro noise, not symbol-specific, expected not a mapper defect):
  1. "RBA SAYS CASH RATE IS AT TOP END OF NEUTRAL RATE ESTIMATES FROM MODELS AND MARKETS..."
  2. "RBA BOARD: CURRENT CASH RATE SEEN AS EFFECTIVE IN MOVING ECONOMY TOWARD BALANCE..."
  3. "RBA: BOARD TO RECEIVE FRESH INFLATION, LABOUR MARKET AND GDP DATA BEFORE SEPTEMBER MEETING..."
- **Entity-mismatch example found this cycle**: a "COST" catalyst match (`catalyst_id cat_aee250166bf0d7da`) is actually a macro headline using the word "cost" ("RBA SAYS OIL PRICES, COST PASS-THROUGH...") mis-tagged with `symbol: "COST/USDT"` — not genuinely about Costco. Treated as no-match for the pre-US COST candidate (verdict INSUFFICIENT_DATA, not SUPPORT); flagged as a mapper false-positive, see §14.

### Pre-US Stocks Review Overlay
- candidates reviewed: 25 (SUPPORT 0 / NEUTRAL 1 / CAUTION 1 / BLOCK 0 / INSUFFICIENT_DATA 23)
- session-cap-only C's now eligible for pre-open Paper lane: 0 (none promoted — 5-minute hand-off window did not allow per-candidate WebSearch verification)
- excluded by hard gate: 56 — LEGAL_RISK (NVO, UNH, INTU, NVDA, SMCI, BAC, BLK), EARNINGS_BLACKOUT (NET, INTC, AMD, MU, MA), NO_ENTITY_RESOLVED_CATALYST (remaining 45)

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **risk-on** (BTC broke $80K today, externally verified, ETF inflows + short-covering; altcoin breadth 100% above EMA20/50; ATR percentile 80 — elevated/trending vol; CoinDesk flags the rally as running into "overbought" territory — risk-on but increasingly stretched)
- Stocks mood: **chop / pre-market** (VIX 15.81 calm; regime label chop; QQQ downtrend -3.23% 5d while SPY/IWM/DIA merely range; breadth split 25% above EMA20 vs 75% above EMA50 — short-term pullback inside a still-intact medium-term uptrend; all setups pre-open planning-only)
- Dominant narrative: **BTC $80K breakout** (crypto) / **AI-chip earnings week** (stocks — NVDA/CRM/CRWD/MRVL/AFRM all report within days, INTU today)
- Preferred side now: **crypto — selective longs, prefer less-extended RS names over vertical movers**; **stocks — wait for RTH confirmation on both sides, defensive-sector longs and chip-sector shorts are the cleanest raw setups pre-open**
- Best long candidate: **INJ/USDT** (crypto, actionable now, near its own pullback zone) / **KO** (stocks, watch for RTH)
- Best short candidate: **HEMI/USDT or TUT/USDT** (crypto, watch only — need a confirmed breakdown retest, not the current -19% to -24% extension) / **AVGO** (stocks, watch for RTH)
- Best catalyst-backed candidate: **MSTR** (externally verified Canaccord PT raise, BTC-correlated)
- What to avoid: **ANET short** (catalyst contradicts direction); chasing **ONG/USDT** (+35% 24h, already extended, weak volume confirmation); the **4 untracked crypto watchlist alerts** should not be treated as tracked/scoreable trades
- What would change the view: a confirmed US-open reaction that resolves the stocks "chop" regime into a clear direction; BTC losing $78-79K support and confirming the "overbought" warning; NVDA's earnings tomorrow re-rating the whole semis complex before AVGO/QCOM/TSM shorts get a clean read

## 7. Candidate Deep Dives

### 1. KO — LONG-WATCH (best stocks long, pre-open)
- Status: pre-US candidate `sig_f4e604b51366471c`, pre_gate_tier A, base_score 86.18, demoted to C only by `market_closed_intraday_planning_only`; entry_trigger 91.97, stop 91.48.
- Pre-US overlay verdict: **INSUFFICIENT_DATA** (no internal catalyst_events.jsonl match found for KO this cycle; time budget did not allow a WebSearch check within the 5-min hand-off window) — INSUFFICIENT_DATA is a neutral read, not a negative one; no legal/earnings/headline risk surfaced either.
- Has price already reacted? Unknown pre-open — no RTH tape yet.
- Is this aligned with mood? Defensive consumer-staples name in a "chop" stocks regime with tech under earnings-week pressure — a reasonable rotation candidate if breadth stays weak in tech.
- Actionable now or wait? **Wait for RTH confirmation** — no chase into the pre-open gap; require the first 15-30min to confirm the level holds.
- What would invalidate: a gap-down open, or the level trading straight through 91.97 without acceptance.
- Chase risk: unknown pre-open by definition; re-assess live at the 18:30 US-open-reaction slot.

### 2. MSTR — LONG (best catalyst-backed candidate)
- Status: open crypto-equity swing long, score 79.57 (crypto book) / also a pre-US stocks-style candidate `sig_1a8852c320f71d45` in the same universe, pre_gate_tier B, base_score 79.57; pre-US overlay verdict **NEUTRAL** (catalyst fresh and entity-resolved, but no relative-strength-vs-sector confirmation was available inside the hand-off window, so SUPPORT was correctly withheld per the overlay's own honesty rule).
- Catalyst confirmation: Canaccord raised its Strategy (MSTR) price target to $175 from $130, maintaining Buy, published 2026-08-25 — externally verified via [Bloomberg](https://www.bloomberg.com/news/articles/2026-08-25/bitcoin-reaches-three-month-high-of-80-000-as-momentum-returns)-adjacent coverage of the same-day BTC $80K move; internal `catalyst_events.jsonl` also carries the same headline from `t.me/marketfeed` and `t.me/WalterBloomberg`, entity-resolved (`$MSTR` explicit), timestamp ~10:33-10:39 UTC (~2.5-3h before this review) — genuinely fresh.
- Has price already reacted? Partially — BTC's own $80K move is already priced into crypto-correlated names; MSTR-specific analyst re-rating is same-day, so some upside may still be ahead of the print.
- Chase risk: moderate — BTC itself is flagged overbought by CoinDesk; MSTR amplifies BTC beta, so a BTC pullback would hit MSTR harder.
- Actionable now or wait? Existing open leg can be held; fresh size only on confirmed RTH follow-through, not a pre-market chase.
- Invalidation: BTC losing the $78-79K support zone, or MSTR fading the pre-market catalyst reaction at the open.

### 3. ANET — CAUTION / AVOID this direction (contradicted catalyst)
- Status: pre-US candidate `sig_11e2f72fd180c04b`, direction **short**, pre_gate_tier B, base_score 77.81; pre-US overlay verdict **CAUTION (-4)**, adjusted score 73.81, still B-tier (clamped, not zeroed, by the ingest code).
- Catalyst confirmation/contradiction: the only linked catalyst is "Arista Networks (NYSE:ANET): High-Growth Leadership and Momentum" (Finnhub company-news, 2026-08-25, entity-resolved) — explicitly **bullish framing**, directly contradicting a short thesis.
- Is this aligned with mood? No — a bearish trade with a bullish-titled catalyst attached is an internal contradiction, not a clean short.
- Actionable now or wait? **Manual review required before any RTH entry**, either direction — the short needs independent technical justification since its own catalyst argues the other way; do not simply flip to long without a fresh technical case either.
- What would invalidate the caution flag: a same-day contradicting headline (guidance cut, downgrade) that would restore alignment with the short thesis.

### 4. INJ/USDT — LONG (best crypto long, actionable)
- Status: open crypto swing long `sig_3fe0e69af8a63169`, score 71.1, status=triggered, entry 5.8581-5.9356 (active-signals) / fresh Trade Idea #4 in the 12:30 swing report shows an entry-plan pullback zone of 5.785-5.844 with **current price 5.870** — i.e. price sits essentially right inside its own planned entry zone, not chasing.
- Has price already reacted? Only mildly — 24h +6.73%, 7d +43.94% (most of the move is older, not today's chase).
- Chase risk: low — RR to TP1 quoted at 1.84R, volume 0.24x (below-average, a mild caution per the report's own counter-thesis, but not a chase-risk flag).
- Aligned with mood? Yes — selective RS-leader long in a risk-on crypto regime, less extended than ONG (+35% 24h) or AMP (+21.65% 24h), both flagged by their own reports as chase-risk/weak-volume watchlist-only.
- **Data-integrity note**: this exact signal (INJ/USDT swing, score 71.1) also appears in today's `detect_untracked_legacy_alerts` output — a watchlist alert was sent to Telegram at 12:29:15 EEST with no matching fresh `proposed_signal`, meaning today's re-fire of this idea will not be tracked for PF/winrate purposes even though the underlying position is real and open. See §14.
- Actionable now or wait? Already open/actionable on the existing leg; fresh size only within the 5.785-5.844 zone, not above it.
- Invalidation: 1h close beyond 5.714.

### 5. Watchlist-alert / signal-tracking integrity anomaly (system-integrity, not a single symbol)
- Issue: `detect_untracked_legacy_alerts --since 2026-08-25` returned **4** untracked alerts today (POL/USDT scalp 68.7, POL/USDT swing 76.0, PROM/USDT swing 72.4, INJ/USDT swing 71.1), all sent to Telegram between 09:51-12:29 EEST with no matching `proposed_signal` within the 6h detector window — up from 0 in both of the last two reviews (04:39, 11:39).
- Why this matters: these are real desk ideas (POL/USDT is Trade Idea #1 this cycle, score 76.0, "actionable"; INJ/USDT is Trade Idea #4, also "actionable" and already open) — the alerts themselves are legitimate, but because no fresh `proposed_signal` backs today's re-fire, none of today's specific alert instances will contribute to PF/winrate accounting, consistent with the known [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] pattern (previously confirmed on ALLO/USDT and BANK/USDT, escalated to HIGH 2026-07-17).
- Actionable now or wait? Not a trade decision — this is a tracking/accounting-integrity issue. The underlying trade ideas (POL, PROM, INJ) can still be evaluated on their own technical merits (see §7.4 for INJ); just do not expect today's alert-firing to show up correctly in future `signal-stats` runs.

**Excess candidates not deep-dived:** AVGO/QCOM/TSM/MRVL (stocks, chip-sector short-watch, all INSUFFICIENT_DATA, needs RTH + sector confirmation given NVDA earnings tomorrow); GOOGL/UBER/MSFT/SBUX/BIIB (stocks, all raw-A, all INSUFFICIENT_DATA, pure pre-open watchlist); HEMI/USDT, TUT/USDT (crypto short-watch, weakest-symbols bias=short but no dedicated Trade Idea this cycle — need confirmed breakdown retest before actionable); ZAMA/USDT, NEAR/USDT, VIRTUAL/USDT (crypto, carried from 11:39 review, not re-confirmed this cycle — rotated out of the fresh top-6, not invalidated).

## 8. Best Candidates Ranked

1. **INJ/USDT** — LONG, crypto, actionable now, least-extended RS-leader with price inside its own entry zone.
2. **MSTR** — LONG, catalyst-backed (externally verified), hold existing leg, size only on RTH confirmation.
3. **KO** — LONG-WATCH, stocks, cleanest raw-A pre-open candidate, wait for RTH.
4. **AVGO** — SHORT-WATCH, stocks, sector-thesis (chip weakness into NVDA earnings), wait for RTH + a symbol-specific catalyst check.
5. **ANET** — CAUTION / do-not-trade-as-scored — catalyst contradicts the short direction; needs manual review before either direction is actionable.

## 9. Avoid / No Trade

*(This decision window only — never a command to stop scanning, tracking, or the scheduler.)*

- **ANET short (as currently scored)** — catalyst text is bullish, contradicting the short thesis; manual review required.
- **Chasing ONG/USDT** — +35% 24h, +70% 7d, volume only 0.5x (below average) — the report's own counter-thesis already flags weak volume confirmation; not a fresh chase candidate.
- **Chasing AMP/USDT** — +21.65% 24h, volume 0.25x, own counter-thesis explicitly states "watchlist/no-trade" (score below active-trade threshold).
- **Today's 4 untracked crypto watchlist alerts (POL×2, PROM, INJ)** — do not treat as scoreable/tracked trades even though the underlying setups are real; see §7.5/§14.
- **All 23 INSUFFICIENT_DATA pre-US stocks candidates** — not a "no," just genuinely unverified; require RTH confirmation plus (time permitting at the 18:30 slot) an external catalyst check before any of them can be upgraded.
- **Fresh crypto scalp adds generally** — one mode bucket this cycle (n=112) shows totalR -5.5R, consistent with prior reviews' worst-performing-mode pattern; let existing legs run rather than adding new scalp exposure.

## 10. Main Risks

- **BTC "overbought" warning at $80K**: CoinDesk explicitly flags the rally running into overbought territory the same day it happened — a pullback here would hit BTC-beta names (MSTR, COIN, crypto-equity longs) hardest; watch $78-79K as the near-term support to hold.
- **Untracked-alert regression (0 → 4 today)**: concrete, dated recurrence of [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] — affects PF/winrate accounting integrity for today's POL/PROM/INJ alerts specifically, not just a one-off.
- **ACE/USDT invalidation question, only partially resolved**: no longer tagged bias=short in weakest-symbols, but absolute current price vs. its 0.224443 invalidation could not be independently re-confirmed this cycle from read-only sources — carried forward, not cleared.
- **XPL/USDT bias-tag question**: unresolved since 2026-08-08, not re-checked this cycle (time budget prioritized the stocks hand-off) — still open, still `triggered`.
- **Catalyst mapping weak (76.3% unmapped)** — plus a concrete entity-mismatch example found this cycle (COST/"cost" false positive) — treat the catalyst layer as context only, not a final decision input, for anything not independently verified.
- **Earnings-heavy tech week**: NVDA/CRM/CRWD/MRVL/AFRM all report within 1-2 sessions, INTU reports today — elevated gap/chase risk for any tech-sector stocks candidate regardless of score; several (NVDA, CRM, CRWD, MRVL, INTU) are already hard-excluded from the pre-US eligible list by the code's `EARNINGS_BLACKOUT` gate.
- **Touch-based `final_r` accounting caveat** (per [[project_crypto_ai_desk_touch_based_pnl]]): crypto tier-B totalR +67.3R this run is directionally positive but likely overstates realistic net PnL.

## 11. Action Plan — next 4 hours

1. Hold INJ/USDT and MSTR open legs; fresh INJ sizing only within 5.785-5.844, fresh MSTR sizing only on confirmed RTH follow-through.
2. At the 18:30 US-open-reaction slot: re-check KO, AVGO, GOOGL, UBER, MSFT, SBUX, BIIB against real RTH tape — only then consider upgrading any of today's 23 INSUFFICIENT_DATA pre-US verdicts.
3. Do not enter ANET in either direction until the catalyst-contradiction is manually resolved.
4. Do not chase ONG/USDT or AMP/USDT at market; both are already flagged extended/weak-volume by their own reports.
5. Treat today's 4 untracked watchlist alerts (POL×2, PROM, INJ) as real trade ideas but expect them to be invisible to next cycle's `signal-stats` — do not use their absence from PF stats as a quality signal.
6. Watch BTC's $78-79K support level; a break would raise chase-back risk on all BTC-beta longs (MSTR, COIN, etc.) held from before this review.
7. Keep crypto scalp adds minimal given the mode's continued -5.5R showing this window.
8. Re-verify ACE/USDT's absolute current price vs. its 0.224443 invalidation and the XPL/USDT bias-tag question at the next slot with DB access if available — both remain open questions this cycle only re-confirmed as "not worsening," not resolved.

## 12. Final Verdict per Mode

- **Crypto scalp**: CAUTION — worst-performing mode again this window (totalR -5.5R), let existing legs run, minimal new adds.
- **Crypto intraday/swing**: NORMAL, selective-longs — INJ/USDT and MSTR are the cleanest current theses; avoid chasing ONG/AMP.
- **Stocks (all modes)**: WATCHLIST-ONLY / PRE-OPEN — 25 candidates reviewed and ingested (READY), 0 promoted to SUPPORT this cycle; KO best long-watch, AVGO best short-watch, ANET flagged CAUTION; require RTH confirmation before anything becomes actionable.
- **Overall**: CAUTION — risk-on crypto trend intact but stretched (BTC overbought flag); stocks structurally non-actionable until the open; one fresh data-integrity regression (untracked alerts) to monitor.

## 13. Sources

- Internal: [`reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`](reports/STOCKS_PREUS_REVIEW_CANDIDATES.md) (generated 2026-08-25T12:58:46Z)
- Internal: `data/raw/enriched_review_sources/preus_review_2026-08-25T130040Z.json` (this run's own hand-off verdicts)
- Internal: [`data/reports/swing/2026-08-25_12-30_swing_report.md`](data/reports/swing/2026-08-25_12-30_swing_report.md), [`data/reports/stocks/intraday/2026-08-25_11-38_stocks_intraday_report.md`](data/reports/stocks/intraday/2026-08-25_11-38_stocks_intraday_report.md), [`data/reports/intraday/2026-08-25_10-42_intraday_report.md`](data/reports/intraday/2026-08-25_10-42_intraday_report.md)
- Internal: `data/catalysts/2026-08-25/catalyst_events.jsonl`, `narrative_baskets.jsonl`
- Internal: `active-signals` / `signal-stats` CLI outputs (crypto + stocks), `detect_untracked_legacy_alerts --since 2026-08-25`, captured 2026-08-25 ~16:00-16:10 EEST
- Internal: prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-08-25_1139.md` (11:39 EEST)
- External: [Bitcoin (BTC) Reaches Three-Month High of $80,000 as Momentum Returns — Bloomberg, 2026-08-25](https://www.bloomberg.com/news/articles/2026-08-25/bitcoin-reaches-three-month-high-of-80-000-as-momentum-returns)
- External: [What next as bitcoin tops $80,000... rally now runs into overbought warning signs — CoinDesk, 2026-08-25](https://www.coindesk.com/markets/2026/08/25/bitcoin-tops-usd80-000-solana-jumps-8-but-rally-now-runs-into-overbought-warning)
- External: [Bitcoin Clears $80K – And Wall Street Is Raising Its Bets On MSTR, COIN, XYZ Stocks — Stocktwits, 2026-08-25](https://stocktwits.com/news-articles/markets/equity/mstr-coin-stocks-see-price-target-hikes-amid-bitcoin-rally-to-80-k-goldman-cautiously-optimistic-on-coinbase/cZYkZppRJ8S)

## 14. Fix Requests / TODO

### TODO-untracked-alerts-regression (new, high priority)
- **issue:** `detect_untracked_legacy_alerts --since 2026-08-25` returned **4** untracked crypto alerts today (POL/USDT scalp 68.7, POL/USDT swing 76.0, PROM/USDT swing 72.4, INJ/USDT swing 71.1), all sent 09:51-12:29 EEST, none with a matching `proposed_signal` within the detector's 6h window — up from 0 in the last two reviews (04:39, 11:39 EEST today). All 4 correspond to real, currently-"actionable" desk ideas (POL is this cycle's Trade Idea #1, INJ is Trade Idea #4 and already has an open triggered position), so this is a live re-occurrence of the bug, not a stale artifact.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-25` output; cross-checked against `data/reports/swing/2026-08-25_12-30_swing_report.md` Trade Idea #1 (POL/USDT, score 76.0) and #4 (INJ/USDT, score 71.1); `active-signals --asset-class crypto` confirms `sig_3fe0e69af8a63169` (INJ/USDT) is a genuine open position with a signal_id, separate from today's untracked alert firing.
- **suggested manual fix:** operator session with DB access should check `watchlist_alerts` vs `proposed_signals` join logic for these 4 rows specifically — per [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]], the known root cause is a watchlist re-fire reusing a stale/closed `signal_id` instead of minting a fresh `proposed_signal`.
- **priority:** high
- **first observed (this instance):** 2026-08-25 16:10 EEST (pattern first confirmed 2026-07-17 on ALLO/USDT and BANK/USDT).

### TODO-ace-invalidation-still-open (carried forward, downgraded severity)
- **issue:** the 11:39 review's headline finding (ACE/USDT open long `sig_3e43cb2f2336cff7` trading through its own invalidation 0.224443, bias=short tagged 3+ cycles) has partially eased — ACE no longer appears in this cycle's "Weakest Symbols" bias=short list — but this read-only report set does not surface an absolute current ACE price this cycle, so the invalidation breach cannot be independently re-confirmed as resolved either.
- **evidence:** `active-signals --asset-class crypto` row `sig_3e43cb2f2336cff7` still `status=triggered`, invalidation=0.224443; `data/reports/swing/2026-08-25_12-30_swing_report.md` shows ACE/USDT only under "Unusual Volume" (tags `volume_expansion`, 24h -0.1%), not under "Weakest Symbols."
- **suggested manual fix:** operator DB check of ACE/USDT's live price vs. its invalidation level and its `bias_tag` vs `direction` fields, same as previously requested for XPL/USDT.
- **priority:** high (downgraded from "headline AVOID" since the bias contradiction itself has eased; the underlying invalidation question is unresolved, not proven fine)
- **first observed:** 2026-08-08 (pattern); escalated 2026-08-25 11:39 EEST; re-confirmed-as-partially-eased 2026-08-25 16:10 EEST.

### TODO-catalyst-entity-mismatch-cost (new, low priority)
- **issue:** a catalyst event tagged `symbol: "COST/USDT"` (`catalyst_id cat_aee250166bf0d7da`, title "RBA SAYS OIL PRICES, COST PASS-THROUGH AND DATA CENTER BOOM POSE UPSIDE INFLATION RISKS...") is actually a macro/RBA headline using the word "cost," not a genuine Costco-ticker catalyst — an entity-resolution false positive that could inflate apparent catalyst coverage for COST if consumed naively downstream.
- **evidence:** `data/catalysts/2026-08-25/catalyst_events.jsonl`, catalyst_id `cat_aee250166bf0d7da`.
- **suggested manual fix:** tighten the entity resolver to require a `$COST` cashtag or explicit "Costco" mention rather than bare keyword match on common English words that coincide with tickers (COST, NOW, ALL, etc.).
- **priority:** low
- **first observed:** 2026-08-25 16:10 EEST.

### Resolved: TODO-scheduler-log-cycle-summary-gap (from 11:39 review)
- **why resolved:** `scheduler.log` and `cycle_01_13-14_summary.md` under today's folder are both fresh (~12:53-13:00 EEST), versus ~10h-stale and missing entirely at the 11:39 review. The logging-path gap did not recur this cycle.
