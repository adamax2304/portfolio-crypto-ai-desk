# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:19 EEST

## 1. Executive Summary
Slot: **pre-US-open decision review**. Advisory only — no auto-trade, no scoring/threshold changes. **Pre-US schedule check: target 08:55 ET, actual fire ≈08:58 ET (Δ+3min, within tolerance) — no DST mismatch, outside the documented 2026 drift windows.** July CPI landed at 08:30 ET as expected (3.4% YoY, cooling slightly from June's 3.5%) — futures reacted mildly positive (SPX +0.4%, NDX +0.8%, VIX ~15.3) but the mood is "cautiously optimistic, not risk-on" per fresh WebSearch — Fed-hold odds firmed, oil sits near $90 on Iran/Strait-of-Hormuz tension. Crypto stayed in chop with a risk-off macro overlay (BTC downtrend, ETH transition_up, macro risk 100/100 on geopolitical + exploit headlines: Harmony ONE mint exploit, XRP bridge hack, Aave/KelpDAO bad debt). No A-tier fired in either asset class this cycle. Catalyst mapping is weak this run (72.65% unmapped). **Ran the full stocks pre-US-open review overlay**: 23 eligible candidates scored — 0 SUPPORT, 5 CAUTION, 5 INSUFFICIENT_DATA, 13 NEUTRAL (see §5). **Correction made at 16:26 EEST**: the enforcement ingest (`stocks-preus-review-ingest`) took ~14 minutes wall-clock (≈35-40s/candidate, not stuck — it returned cleanly at 16:26 with all 23 rows `status: OK`) and confirmed every requested verdict/adjustment applied exactly as submitted, with **zero clamping** (no SUPPORT was submitted, so no zero-out case triggered; all 5 CAUTION adjustments of -4/-5 landed inside the allowed [-7,-3] range unchanged). The tier/score effects below are now **enforcement-confirmed**, not just requested. Separately, this run **confirmed** (not just suspected, as the 11:39 review flagged for HEI) that 3 crypto swing longs are open past their own invalidation level without a status change: **TUT/USDT (−22% through invalidation), HEI/USDT (−30%), HOLO/USDT (−2.7%, marginal)** — see §14, escalated to high.

## 2. Data Used
- Reports: `2026-08-12_10-43_scalp_report.md` (~2h20min old), `2026-08-12_10-53_intraday_report.md` (~2h10min old), `2026-08-12_04-48_swing_report.md` (~8h10min, carry-forward), `2026-08-12_08-04_stocks_intraday_report.md` (~4h55min, carry-forward/borderline)
- `data/catalysts/2026-08-12/` — catalyst_events.jsonl (2000 rows, rolling window), narrative_baskets.jsonl (5 baskets), catalyst_cycle_11-01.md (latest)
- `data/processed/llm_analysis_packet.md` (10:53 UTC), `data/processed/llm_stocks_packet.md` (11:12 UTC)
- CLI: `active-signals` (crypto n=50, stocks n=50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-12` (clean — 0 untracked)
- **Pre-US overlay CLI**: `stocks-preus-candidates` → `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (23 eligible / 41 excluded); `stocks-preus-review-ingest --json data/raw/enriched_review_sources/preus_review_2026-08-12T13-10-29Z.json` (submitted, still running at write time — see §3/§14)
- Read-only SQLite queries (`db/crypto_ai_desk.sqlite`, mode=ro) against `news_items` (per-candidate freshness check for the 23 pre-US candidates) and `proposed_signals` (invalidation-vs-price check on TUT/HEI/HOLO) — both explicitly within the §A.1 allowance for read-only table queries
- 2 WebSearch (S&P/Nasdaq futures + VIX post-CPI; CPI print confirmation) + 1 WebFetch (Yahoo Finance live-blog, to confirm CPI number, futures reaction, and sector mood) — internal news_items otherwise used first per source discipline
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-12_1139.md` (11:39 EEST, Europe/pre-US slot)

## 3. Scheduler / Data Freshness
- **Pre-US schedule check: target 08:55 ET, actual fire ≈08:58 ET (Δ+3min, within tolerance).**
- `scheduler.log` mtime 15:00 EEST (~1h old at time of writing) — **not deferred**. Latest cycle summary `cycle_06_13-30_summary.md` mtime 15:00 EEST — fresh.
- Pending-monitor alive and ticking (last log line 13:42 EEST, tick 10, 78 crypto tracked, 48/48 refresh succeeded, tp=2/stop=0 this tick) — but its own log shows `pending-monitor recycle failed: PermissionError: [WinError 5] Access is denied` on a worker-memory rotation step (see §14).
- Stocks intraday report is ~4h55min old — borderline the 4h "fresh" cutoff, treated as **carry-forward** per the freshness rule, flagged here.
- Stocks swing/invest reports are from 2026-07-02 (stale, >14h) — **expected**: old stocks swing/invest playbooks are deprecated/removed per project design, excluded from this review's actionable set.
- Untracked-alert detector: **0** — no signal-reuse integrity issue this run.
- **Pre-US overlay ingest status — RESOLVED**: `stocks-preus-review-ingest` was launched with 23 verdicts at 16:11 EEST and returned at 16:26 EEST (~14min wall-clock, ≈35-40s/candidate — slow but not stuck; `stocks-preus-candidates` completed faster in its own background window). All 23 rows returned `status: OK`; every requested verdict/adjustment/tier was applied exactly as submitted with zero clamping. §5 below reflects the confirmed-enforced numbers.

## 3A. Agent Council JSON
```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-12 16:19 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks-preus-review-ingest enforcement confirmation (still running at write time)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 15:00 EEST", "stocks intraday report ~4h55min old", "72.65% catalyst_events unmapped today"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend / ETH transition_up, altcoin breadth 56% >EMA20", "SPX fut +0.4%, NDX fut +0.8%, VIX ~15.3 post-CPI", "CPI 3.4% YoY, cooling slightly, Fed-hold odds firmed", "oil ~$90 on Iran/Strait-of-Hormuz tension"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "stale_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["2000 catalyst_events, 547 mapped (27.35%) / 1453 unmapped (72.65%)", "TSM +45% July revenue (fresh, entity-resolved)", "LMT defense-tech demo + hot-fire test (fresh, entity-resolved)", "ETN Evercore PT raise to $515 (fresh, single-source)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["premarket RVOL/order-flow for all 23 stocks pre-US candidates"],
      "suggested_effect": "advisory_only",
      "facts_used": ["KAITO/USDT fresh shorts pressing OI+2.8%, funding negative", "TUT/HEI derivatives show fresh short pressure historically", "no live premarket quote tool in this session's allowed toolset"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "price_moved_away", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM/USDT ran to 3.286 vs 2.49-2.59/2.08-2.20 entries — deep in profit, chase risk on fresh entry", "5/23 stocks pre-US candidates show a fresh catalyst that contradicts or weakens the scored direction (APP, TSLA, VRT, NVO, UBER)"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.5,
      "reason_codes": ["open_actionable", "no_entry", "needs_review"],
      "data_missing": ["stocks-preus-review-ingest enforced outcome"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 0 A-tier, ~50 B-tier open (mix triggered/waiting_for_entry)", "stocks: 0 A/B actionable pre-open, 23 C-tier candidates reviewed under the overlay", "TUT/HEI/HOLO invalidation-breach-without-status-change confirmed via direct DB read"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["REGN/MSFT/INTU/BLK carry active legal/headline risk — never promotable regardless of score", "AMAT/CSCO earnings blackout", "TUT/HEI/HOLO invalidation breach = open-position risk-tracking integrity gap"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "low_sample", "playbook_failing"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier headline: PF 2.58, WR 17.5%, avgR 0.34, totalR +71.3 (week)", "crypto swing sub-mode PF 5.13 (strongest lane)", "stocks A/B headline: PF 0.0, 0W/3L, n=10 (weak sample)", "stocks C-tier PF 0.227, totalR −8.5 (week)"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "HOLO/USDT", "trigger": "already open (B-tier swing, entry 0.0822-0.0857); fresh add only above 0.0822 reclaim with volume — currently trading marginally through its own invalidation (0.0758 vs 0.07793), so treat as needs-review, not a clean add", "reason": "RS vs BTC +25%, momentum 99.4/100, but no fresh catalyst and now inside its own invalidation zone" },
    "best_short_candidate":    { "symbol": "KAITO/USDT", "trigger": "wait for bearish HTF structure confirmation + a rejection back below 24h VWAP before shorting; do not chase the breakdown (already >2 ATR from EMA20)", "reason": "score 94.2, 24h -22%, volume 6.8-8x, weak_vs_market/breakdown/overextended tags, fresh shorts pressing OI" },
    "best_catalyst_candidate": { "symbol": "TSM", "trigger": "RTH confirmation of the July-revenue beat translating into RS vs SMH/XLK on the open; no premarket RS data available to confirm now", "reason": "genuine fresh entity-resolved catalyst (July revenue +45% YoY, stock 13% below high) with a supportive tech/AI-infra market backdrop, but INSUFFICIENT_DATA verdict pending RS confirmation" },
    "avoid_candidate":         { "symbol": "REGN / MSFT / INTU / BLK", "reason": "active class_action / securities_fraud legal risk — demoted A→C and never promotable regardless of score or RR" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.60 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, stale_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.40 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, price_moved_away, stale_before_entry | advisory_only |
| execution_lifecycle | manual_review | 0.50 | open_actionable, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, low_sample, playbook_failing | advisory_only |
| head_trader | ok | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review
Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-12_1139.md` (11:39 EEST, Europe/pre-US slot, written ~4h before today's CPI print).
- **CPI is now known**: 3.4% YoY, cooling slightly from June's 3.5% — the prior review's "route around CPI, size down" instruction is resolved; futures reacted mildly positive (SPX +0.4%, NDX +0.8%) but the mood read is "cautiously optimistic, not risk-on," with Fed-hold odds firming and oil elevated on Iran tension.
- **New**: full stocks pre-US-open review overlay run for the first time this cycle (23 eligible candidates scored — see §5); 0 SUPPORT, 5 CAUTION, 3 INSUFFICIENT_DATA, 15 NEUTRAL.
- **Escalated, not new**: the 11:39 review's `TODO-hei-open-long-vs-fresh-short-bias` asked "confirm whether either invalidation has already been breached." This review directly queried the DB and **confirms breach on HEI/USDT (both open longs, −30% through invalidation)**, and additionally finds the **same pattern on TUT/USDT (−22%)** and a marginal case on **HOLO/USDT (−2.7%)** — see §14.
- **Unchanged**: catalyst mapping remains weak (72.65% unmapped today vs 71.7% at 11:39); `TODO-catalyst-symbol-misattribution` from the 11:39 review is still open (not re-verified this cycle — no new CoreWeave/GOOGL-style example spotted, but the underlying unmapped rate hasn't improved).
- **PROM/USDT** (11:39's best long-watch) has run hard since — now at 3.286 vs the 2.639-2.755 planned pullback zone, meaning that specific entry idea is stale/moved-away; the two open swing longs on it remain in deep profit.
- **TUT/USDT** (11:39's best short-watch) is superseded by the invalidation-breach finding above — the short-watch retest idea (0.0757-0.0790 zone) is no longer the most relevant fact about this symbol; the open-position integrity issue is.
- No A-tier fired in either asset class in either review.

## 5. Catalyst Coverage
- Total catalyst_events today: **2000** (rolling window) | mapped (symbol present): **547 (27.35%)** | unmapped: **1453 (72.65%)**
- Narrative baskets: **5** (perps_dex_narrative, ai_narrative, binance_ecosystem_teaser, delisting_thin_liquidity, momentum_breakout)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines by importance:
  1. `0.748` [legal_risk] "HTZ Investors Have Opportunity to Lead Hertz Global Holdings, Inc. Securities Fraud Lawsuit" (PR Newswire (Stocks))
  2. `0.748` [exploit_hack] "AI agents' 'alarming' hacking skills creates rush to spend on cybersecurity" (CNBC Markets)
  3. `0.73` [legal_risk] "Wix.com Ltd. (NASDAQ: WIX) Investors with Substantial Losses Have Opportunity to Lead Class Action Lawsuit" (PR Newswire (Stocks))

### Pre-US Stocks Review Overlay
- candidates reviewed: **23** (SUPPORT 0 / NEUTRAL 13 / CAUTION 5 / BLOCK 0 / INSUFFICIENT_DATA 5) — **enforcement-confirmed** by `stocks-preus-review-ingest` (returned 16:26 EEST, all 23 `status: OK`, zero clamping)
- session-cap-only C's now eligible for pre-open Paper lane: **23** (all capped only by `market_closed_intraday_planning_only`, i.e. not blocked for a substantive reason) — of these, **0** received a SUPPORT-grade catalyst+RS adjustment; confirmed enforced score/tier changes: APP 58.68→53.68 (C), TSLA 62.35→57.35 (C), VRT 81.06→76.06 (B, was pre_gate A, already demoted to C by the base pipeline's own market-closed cap — enforcement applies to the pre-cap tier), NVO 71.08→67.08 (B), UBER 81.15→76.15 (B) — all 5 CAUTION cases, -4 to -5 points, no clamping needed since all requests were already inside [-7,-3]. The 13 NEUTRAL and 5 INSUFFICIENT_DATA candidates keep their base score/tier unchanged (adjustment 0.0 confirmed for all).
- excluded by hard gate: **41** — 30 × `NO_ENTITY_RESOLVED_CATALYST` (GE, COST, AFRM, CLSK, IWM, XLI, DELL, DDOG, KLAC, NET, IBM, SBUX, ABNB, PYPL, BKNG, ASML, CRWD, XOM, DXCM, HD, SNOW, CRCL, GILD, XLE, COP, CMCSA, ANET), 7 × `EARNINGS_BLACKOUT` (V, GOOGL, MAR, HOOD, PLTR, AMGN, LLY, VRTX, SMCI, BX), 4 × `LEGAL_RISK` (BLK, INTU, MSFT, REGN)
- CAUTION detail (catalyst contradicts or weakens the scored direction): **APP** (short, but fresh coverage argues bullish "market got it wrong"), **TSLA** (long, but fresh insider unlock overhang), **VRT** (long, but fresh coverage titled "Why Vertiv Plunged in July"), **NVO** (long, but Lilly's competing drug just got EU approval), **UBER** (long, but Waymo/Serve Robotics partnership friction)
- INSUFFICIENT_DATA detail (genuine fresh catalyst present, but no per-symbol premarket RS-vs-sector data available to confirm): **TSM** (July revenue +45% YoY), **LMT** (fresh defense-tech demo + hot-fire test, geopolitically-tailwinded, base_score 99.91/pre_gate A), **ETN** (Evercore PT raise to $515, base_score 100.0/pre_gate A), **WMT** (base_score 83.25/pre_gate A — sparse fresh coverage), **PANW** (headline too content-free to assess)

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **chop**, with a risk-off macro overlay (macro risk score 100/100 — Harmony ONE unauthorized-mint exploit, XRP Coreum-bridge hack, Aave $195M bad debt from KelpDAO exploit, Iran/Strait-of-Hormuz rhetoric, N. Korea missile test). BTC downtrend, ETH transition_up, altcoin breadth 56.1% >EMA20 (not broadly weak, just directionless).
- Stocks mood: **neutral-to-slightly-positive, cautiously optimistic** post-CPI (SPX fut +0.4%, NDX fut +0.8%, VIX ~15.3) — CPI cooled slightly to 3.4% YoY as expected; Fed-hold odds firmed for September; **not** a clean risk-on read — oil near $90 on Iran tension is an active headwind, and CSCO reports earnings today with AMAT tomorrow (both flagged do-not-chase).
- Dominant narrative: crypto — `momentum_breakout` (PROM/DODO, no confirmed catalyst, avoid-chase playbook) and `binance_ecosystem_teaser` (BNB/ASTER, aging past <6h into <24h fresh); stocks — AI-infrastructure buildout chatter (Vertiv vs Eaton, TSM AI-driven revenue beat) alongside a scattering of legal/earnings landmines (REGN/MSFT/INTU/BLK legal, AMAT/CSCO earnings).
- Preferred side now: **wait-for-trigger**, asset-class-separated — crypto: RS-leader longs only after a pullback, or failed-bounce shorts on a confirmed retest; stocks: **RTH confirmation required** for every pre-US name (none of the 23 pre-US candidates cleared to SUPPORT this cycle).
- Best long candidate: **HOLO/USDT** (crypto, already open B-tier swing) — but flagged needs-review, see §14; no clean stocks long — closest is TSM (INSUFFICIENT_DATA, needs RTH RS confirmation).
- Best short candidate: **KAITO/USDT** (crypto) — wait for bearish HTF structure + rejection, do not chase the existing -22% breakdown; no clean stocks short — 4 of 23 pre-US shorts/longs were actually CAUTION-flagged as catalyst-contradicted (APP short specifically contradicted by bullish earnings-reaction commentary).
- Best catalyst-backed candidate: **TSM** (stocks, INSUFFICIENT_DATA — genuine fresh earnings-adjacent catalyst, needs RTH RS-vs-SMH/XLK confirmation) alongside **BNB/USDT** (crypto, ecosystem-teaser basket, now aging, still wait-for-confirmation not chase).
- What to avoid: REGN/MSFT/INTU/BLK (legal risk, never actionable), AMAT/CSCO (earnings blackout, do not chase), APP/TSLA/VRT/NVO/UBER (pre-US CAUTION — catalyst contradicts the scored direction), chasing PROM/USDT at current price (3.286, well past the 2.49-2.59 entries), TUT/HEI/HOLO as "clean opens" until the invalidation-breach question is resolved (see §14).
- What would change the view: RTH open + first 15-30min price action on TSM/LMT/ETN (resolves the missing RS leg); resolution of whether TUT/HEI/HOLO's stated invalidations are stale-but-real or a monitoring bug; confirmation that `stocks-preus-review-ingest` actually applied the 23 verdicts.

## 7. Candidate Deep Dives

### 1. TUT/USDT (crypto, needs-review — invalidation-breach anomaly)
- Open swing long `sig_e4875989af64bab7`: entry 0.12303-0.14284, invalidation 0.09882, created 2026-08-09, status **triggered**. Current price (per 10:53 intraday report Desk Notes): **0.0769** — roughly **22% below the stated invalidation**.
- Has price already reacted? Yes, dramatically — this position is deep underwater relative to its own risk level.
- Would treating this as still-open be correct? Not per the stated invalidation — if the invalidation rule fired correctly, this should show `status=stopped`, not `triggered`.
- Separately, a fresh independent scan this cycle tags TUT/USDT bias=**short** (score 80.2, 24h -19.69%, `crypto_failed_bounce_short` candidate zone 0.0784-0.0819) — the same short-vs-open-long tension the 11:39 review flagged for HEI.
- Actionable level for a *fresh* idea: none — this is a risk-tracking question about an *existing* position, not a new entry. Do not add to this name until the invalidation status is resolved.
- TradingView/manual chart check unavailable — using local OHLCV/ATR fields only.

### 2. HEI/USDT (crypto, needs-review — invalidation-breach anomaly, confirmed)
- Two open swing longs: `sig_a4e763ceaf1df917` (invalidation 0.18750) and `sig_2f2c8c4a003b4a97` (invalidation 0.18323), both status **triggered**. Current price: **0.1304** — roughly **30% below both invalidations**.
- This directly confirms what the 11:39 review flagged as a suspicion ("confirm whether either invalidation has already been breached") — it has, by a wide margin, on both positions.
- Fresh independent scan this cycle again tags HEI/USDT bias=**short** (score 80.2, 24h -20.54%), consistent with the 11:39 finding.
- Verdict: **manual review required** — this is a system-integrity question (why hasn't the invalidation/stop logic closed these), not a new trade idea.

### 3. HOLO/USDT (crypto, best-long-candidate but flagged)
- Open swing long `sig_95f38f65aadc4c47`: entry 0.08218-0.08565, invalidation 0.07793, status **triggered**. Current price: **0.0758** — marginally (**~2.7%**) below invalidation. Smaller breach than TUT/HEI, possibly a very recent cross or a reporting-lag artifact rather than a stale bug — flagged for the same investigation, lower confidence than the TUT/HEI cases.
- Thesis otherwise strong: RS vs BTC +25.14%, momentum 99.4/100, volume 2.57x, playbook `crypto_swing_narrative_rs_momentum` (14d WR 72%/PF 5.80 — the strongest crypto lane). No fresh verified catalyst.
- Has price reacted already? Yes — up 24.75%/31.52% (24h/7d) into the entry zone, now pulling back through it.
- Chasing? A fresh add now would be chasing into a level that has already broken the plan's own invalidation — not recommended until this clears.
- Aligned with market mood? Partially — chop favors mean-reversion entries, which this thesis originally was, but the pullback has now overshot the stated risk level.
- Direction: long, but **needs-review, not a clean add** right now.

### 4. KAITO/USDT (crypto, short-watch)
- Score 94.2 (strongest mover today), 24h -22.11% to -23.60% depending on report snapshot, RS vs BTC ~-22%, volume 6.85-8.07x (unusual), tags: weak_vs_market, volume_expansion, breakdown, overextended. Routed to `crypto_failed_bounce_short` in the expansion watchlist.
- Has price already reacted? Yes, sharply — the breakdown is underway.
- Chasing? Yes at current price — flagged "more than 2 ATR from EMA20; do not chase" in the rejected/not-ready section.
- Retest/pullback structure needed: confirm bearish HTF structure + derivatives + a clear stop above the swing high before shorting; squeeze risk noted (price down + OI up = fresh shorts pressing, possible squeeze if price reclaims).
- Actionable level: wait for a failed bounce/rejection, not the current breakdown candle.
- Aligned with market mood? Yes — chop/risk-off macro favors clean shorts on failed bounces over fresh longs.
- Catalyst confirmation/contradiction: none — pure momentum/RS-driven, no fresh verified catalyst.
- TradingView/manual chart check unavailable — local OHLCV/derivatives fields only.

### 5. TSM (stocks, catalyst-watch, INSUFFICIENT_DATA)
- Pre-US overlay: pre_gate_tier B, base_score 66.92, capped only by `market_closed_intraday_planning_only` (not a substantive block — genuinely eligible).
- Catalyst: internal `news_items` shows a genuine fresh item — "Taiwan Semiconductor's July Revenue Rose 45% and the Stock Sits 13% Below Its High" (Motley Fool, 2026-08-12T03:38 -04:00, ~5.5h old at review time) — entity-resolved, material (hard revenue data, not opinion).
- Market context: fresh (SPX fut +0.4%, NDX fut +0.8% post-CPI; broader search noted tech leading after CoreWeave/SuperMicro earnings affirmed AI-trade confidence) — directionally supportive of a semis/AI-infra long.
- Missing leg: **no per-symbol premarket RS-vs-SMH/XLK data available** in this session's toolset — cannot confirm genuine relative strength, so this is **INSUFFICIENT_DATA**, not SUPPORT, per the overlay's strict criteria.
- Would entry now be late? Unknown without RTH/premarket price action — needs first 15-30min confirmation post-open.
- Legal/headline/earnings check: none found for TSM this cycle.
- Actionable level: none scored — treat as catalyst-watch pending RTH RS confirmation.

## 8. Best Candidates Ranked
1. **KAITO/USDT short-watch** (crypto) — wait for a failed-bounce rejection back below 24h VWAP with confirmed bearish HTF structure; do not short the current breakdown candle. Invalidator: a reclaim/close back above the recent swing high.
2. **TSM catalyst-watch** (stocks) — wait for RTH open + first 15-30min RS confirmation vs SMH/XLK; genuine fresh catalyst (July revenue +45%) but no premarket RS data to confirm now. Invalidator: open gaps down or fails to hold intraday VWAP.
3. **LMT catalyst-watch** (stocks) — fresh defense-tech demo/hot-fire-test catalyst plus a supportive geopolitical backdrop (Iran, Ukraine tension); same missing-RS caveat as TSM. Invalidator: no RTH follow-through in the first 30min.
4. **BNB/USDT catalyst-watch** (crypto) — ecosystem-teaser basket now aging past <6h into <24h; wait for a clean breakout or pullback with volume, don't chase the initial pop (single-source, sell-the-news risk noted).
5. **HOLO/USDT long-watch, conditional** (crypto) — strongest crypto swing playbook (14d WR 72%/PF 5.80) and RS+25% vs BTC, but only re-qualifies as a clean long once the invalidation-breach question in §14 is resolved; do not add blind right now.

## 9. Avoid / No Trade
This applies to the current decision window only — never a command to stop scanning, tracking, or the scheduler.
- **REGN, MSFT, INTU, BLK** (stocks) — active class_action/securities_fraud legal risk, demoted A→C, never actionable regardless of score.
- **AMAT, CSCO** (stocks/crypto-adjacent) — earnings blackout today/tomorrow, do not chase into the print.
- **APP, TSLA, VRT, NVO, UBER** (stocks, pre-US CAUTION) — each has a fresh catalyst that contradicts or weakens its scored direction (see §5).
- **Chasing PROM/USDT** at 3.286 — well past the 2.49-2.59/2.08-2.20 entries where the two open longs already sit in deep profit; a fresh entry here is chasing, not confirming.
- **Chasing KAITO/USDT's current breakdown candle** — wait for the failed-bounce structure, not the initial move.
- **TUT/USDT, HEI/USDT** as "clean open positions" — both show confirmed invalidation breaches without a status change; treat as needs-review, not as validated risk until a human confirms the stop logic.

## 10. Main Risks
- **Invalidation-monitoring integrity gap (new, high-confidence finding)**: TUT/USDT and HEI/USDT open longs are both meaningfully past their stated invalidation level while still showing `status=triggered`; HOLO/USDT shows a marginal breach. This affects the accuracy of every "active signals" risk read used by this and future reviews.
- **Catalyst mapping weak** (72.65% unmapped) — treat catalyst layer as context only, not a final decision input this cycle.
- **Geopolitical overhang**: Iran/Strait-of-Hormuz tension (oil ~$90), Ukraine drone strikes on Russian port infrastructure, N. Korea missile test — a live tail risk for both crypto risk appetite and stocks (energy/defense names).
- **Earnings/legal landmines concentrated in the stocks pre-US pool**: 4 legal-risk exclusions (REGN/MSFT/INTU/BLK) and 7 earnings-blackout exclusions out of 64 total candidates scanned — a meaningfully "dirty" pre-open universe today.
- **Missing RS-vs-sector data**: this review has no live premarket per-symbol quote/RVOL tool, so every stocks catalyst-backed idea (TSM/WMT/LMT/ETN) is capped at INSUFFICIENT_DATA rather than SUPPORT, regardless of catalyst quality.

## 11. Action Plan — next 4 hours
- At/after the US cash open: watch TSM, LMT, ETN for the first 15-30min of RTH price action; only treat as actionable if they show genuine RS vs SMH/XLK/sector and hold above the pre-market reference level — do not chase the open print itself.
- Do not add to HOLO/USDT, TUT/USDT, or HEI/USDT until a human confirms whether the invalidation breaches are a real stop-logic bug or a display lag (see §14 TODO — check current price against `proposed_signals.invalidation` directly and whether `status` should already read `stopped`).
- Crypto: watch for a KAITO/USDT failed-bounce short setup; avoid fresh longs into the chop/risk-off macro overlay unless a clean RS-leader pullback appears (BNB/USDT ecosystem-teaser basket is the closest catalyst-backed candidate, still wait-and-confirm).
- Continue monitoring for the `pending-monitor recycle failed: PermissionError` line recurring — if it repeats across cycles, escalate (see §14).

## 12. Final Verdict per Mode
- **Crypto scalp**: no trade — data does not justify a fresh idea (per the report's own final summary); mode remains low-confidence per its own re-audit note (14d PF 0.14, TP/2h horizon mismatch).
- **Crypto intraday**: no trade — best watchlist name DODO/USDT at 63.7/100, wait for cleaner execution.
- **Crypto swing**: strongest lane (14d WR 72%/PF 5.80) but the one open B-tier idea from today's report (HOLO/USDT) needs the invalidation question resolved before treating as clean.
- **Stocks intraday**: planning-only until RTH — 0 A/B actionable pre-open; of the 23 pre-US overlay candidates (enforcement-confirmed), 0 reached SUPPORT, TSM/WMT/LMT/ETN/PANW are the closest (5 INSUFFICIENT_DATA, need RTH RS confirmation), 5 are CAUTION (catalyst contradicts direction, scores docked -4/-5), REGN/MSFT/INTU/BLK remain permanently avoid on legal risk.
- **Stocks swing/invest**: excluded — deprecated/stale data source, not evaluated.
- **System integrity**: manual review required on the TUT/HEI/HOLO invalidation-breach finding before trusting "active signals" risk levels at face value.

## 13. Sources
- [US Stock Market Today: S&P 500 Futures Stall As Traders Eye Inflation Signals](https://finance.yahoo.com/markets/stocks/articles/us-stock-market-today-p-081201698.html)
- [US Stock Futures Rise as Tech Rally Resumes Before Key CPI Data — Bloomberg](https://www.bloomberg.com/news/articles/2026-08-12/us-stock-futures-rise-as-tech-rally-resumes-before-key-cpi-data)
- [Stock market today: Dow, S&P 500, Nasdaq futures rise after CPI data cools slightly — Yahoo Finance](https://finance.yahoo.com/markets/live/stock-market-today-wednesday-august-12-dow-sp-500-nasdaq-cpi-report-091555133.html) (fetched for CPI number, futures reaction, sector mood confirmation)
- [U.S. July CPI to be released on August 12, 2026 — KuCoin](https://www.kucoin.com/news/flash/u-s-july-cpi-to-be-released-on-august-12-2026)
- Internal: `data/reports/scalp/2026-08-12_10-43_scalp_report.md`, `data/reports/intraday/2026-08-12_10-53_intraday_report.md`, `data/reports/swing/2026-08-12_04-48_swing_report.md`, `data/reports/stocks/intraday/2026-08-12_08-04_stocks_intraday_report.md`, `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`, `data/catalysts/2026-08-12/catalyst_cycle_11-01.md`
- Internal news_items (per-candidate, dated inline in §5/§7 deep dives): Motley Fool Investing (TSM revenue, VRT/ETN, NVO), Finnhub company-news (LRCX, ETN/Evercore PT), PR Newswire (Stocks) (LMT partnership demo), CryptoBriefing/CryptoSlate/BeInCrypto (MSTR)

## 14. Fix Requests / TODO

### TODO-invalidation-breach-no-status-change (escalated from 11:39's TODO-hei-open-long-vs-fresh-short-bias)
- **issue:** Three open crypto swing longs are trading through their own stated invalidation level while `status` still reads `triggered` (not `stopped`): **TUT/USDT** `sig_e4875989af64bab7` (invalidation 0.09882, current 0.0769, ~22% through), **HEI/USDT** `sig_a4e763ceaf1df917` (invalidation 0.18750, current 0.1304, ~30% through) and `sig_2f2c8c4a003b4a97` (invalidation 0.18323, same breach), **HOLO/USDT** `sig_95f38f65aadc4c47` (invalidation 0.07793, current 0.0758, ~2.7% through, marginal/recent). The 11:39 review only *suspected* this for HEI ("confirm whether either invalidation has already been breached... if breached, investigate why the position hasn't auto-closed") — this run directly queried `proposed_signals` and **confirms** it on 2 symbols with a wide margin plus a 3rd marginal case, meaning this is very likely a systemic gap in the invalidation/stop-check job, not a one-off.
- **evidence:** Direct read-only SQLite queries against `db/crypto_ai_desk.sqlite` `proposed_signals` table (signal_id/entry/invalidation/status/created_at listed above) cross-referenced with current price fields in `data/reports/intraday/2026-08-12_10-53_intraday_report.md` Desk Notes sections for TUT/USDT (0.0769), HEI/USDT (0.1304), HOLO/USDT (0.0758).
- **suggested manual fix:** Audit the invalidation-check/stop-monitor job for crypto swing-mode signals — confirm it is actually running per-tick for `triggered` status rows (not just for `waiting_for_entry`), and confirm it compares against the correct OHLCV feed/timeframe. Also re-check whether the separately-tracked ZBT/ACE bias-tag-contradiction fix (escalated 2026-08-08, see `project_crypto_ai_desk_bias_tag_contradiction` memory) ever addressed the underlying stop-check path, or only the bias-label display.
- **priority:** high — directly affects whether every "open position" risk figure this and future reviews rely on is trustworthy.
- **first observed (this exact confirmed form):** 2026-08-12 16:19 EEST (this run); precursor suspicion 2026-08-12 11:39 EEST (HEI only); related pattern first escalated 2026-08-08 (ZBT, ACE).

### TODO-pending-monitor-recycle-permission-error
- **issue:** The live pending-monitor process log shows `pending-monitor recycle failed: PermissionError: [WinError 5] Access is denied` during a "rotating worker memory" step. The monitor is otherwise healthy this cycle (tick 10, 78/78 crypto tracked, 48/48 refresh succeeded), but a recurring failed recycle could indicate a slow memory/handle leak over long uptimes on Windows.
- **evidence:** `data/scheduled_runs/2026-08-11_default_schedule/pending_monitor_1786530738.log`, tail lines around 13:42 EEST: "pending-monitor rotating worker memory" immediately followed by "pending-monitor recycle failed: PermissionError: [WinError 5] Access is denied".
- **suggested manual fix:** Check whether the recycle step is trying to replace/restart a worker process or file handle that's still locked by another thread/process on Windows (common WinError 5 cause); consider whether the recycle needs a short unlock/retry-with-backoff, or whether it's safe to skip and just log without failing.
- **priority:** medium — not causing visible tracking failures yet, but worth catching before it does.
- **first observed:** 2026-08-12 16:19 EEST (this run).

### TODO-stocks-preus-review-ingest-slow (resolved this run, perf note only)
- **issue:** `stocks-preus-review-ingest --json data/raw/enriched_review_sources/preus_review_2026-08-12T13-10-29Z.json` (23 verdicts) took **~14 minutes wall-clock** (launched 16:11 EEST, returned 16:26 EEST) — roughly 35-40 seconds per candidate. It completed cleanly with all 23 rows `status: OK` and zero clamping (confirmed in §5), so this was **not a hang or bug in outcome**, just unusually slow relative to `stocks-preus-candidates` (the read-only companion command), which returned faster.
- **evidence:** `ps -ef` showed the python process alive continuously 16:11→16:26; the `review_expires_at` timestamps in the command's own JSON output step forward by ~30-80s per candidate (e.g. `14:41:41` → `14:41:50` → `14:42:01` → ...), consistent with genuine per-candidate processing time rather than a stall.
- **suggested manual fix:** Profile the per-candidate path in `stocks-preus-review-ingest` (legal/earnings hard-gate recheck, score-clamp, tier recompute) to see whether ~35-40s/candidate is expected (e.g. deliberate SQLite write pacing, TTL-timestamp generation) or has an avoidable bottleneck (e.g. a per-call sleep, an uncached repeated lookup, or DB lock contention with the concurrently-running pending-monitor process). Not urgent since the outcome was correct, but 23 candidates × ~35s does not scale well if the eligible list grows.
- **priority:** low — outcome was correct and fully enforcement-confirmed; this is a performance observation, not a correctness bug.
- **first observed:** 2026-08-12 16:11-16:26 EEST (this run); resolved (returned cleanly) by 16:26 EEST, same run.

### TODO-catalyst-symbol-misattribution (carried forward, unchanged)
- **issue:** Catalyst mapping remains weak (72.65% unmapped today vs 71.7% at the 11:39 review) — carried forward from the 11:39 review's TODO of the same name; not independently re-verified for a fresh misattribution example this cycle, but the underlying unmapped rate has not improved.
- **evidence:** This run's mapped/unmapped count (547/1453 of 2000) vs the 11:39 review's (425/1075 of 1500).
- **suggested manual fix:** See the 11:39 review's original TODO — audit the earnings-call-transcript source path's symbol resolver.
- **priority:** high (unchanged).
- **first observed:** 2026-08-12 11:39 EEST; still open at 16:19 EEST.
