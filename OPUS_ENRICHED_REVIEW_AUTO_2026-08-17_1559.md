# Opus Enriched Review — pre-US-open decision review — Auto Cycle 15:59 EEST

## 1. Executive Summary

**Pre-US-open decision review, scheduled fire 15:59 EEST (08:59 ET) — target 08:55 ET, Δ+4min, within tolerance. Publish time is delayed to ~16:40 EEST (09:40 ET) by two slow CLI commands in the stocks pre-US overlay (see §3) — the US cash session has already been open ~10 minutes by the time this review is written.** **Advisory only — no auto-trade.** No A/B-tier actionable setups anywhere this cycle (crypto scalp/intraday/swing, or stocks intraday) — everything on the desk remains C-tier watchlist/planning, unchanged from the 11:40 review. Crypto regime: still **range/chop**, BTC pinned $62.3–64K (external check: "range-bound," repeatedly rejected above $64K), ETH ~$1,900 capped. Macro/geopolitics risk is **extremely elevated and still worsening intraday**: 96.1–99.8/100 across this cycle's scalp/intraday scans (vs 93.7 at 11:40, 81.5 at 04:40) — Coldcard hardware-wallet exploit (external check: confirmed ~$116M / 1,778+ BTC stolen, still being tracked, multiple attackers suspected) plus intensifying Ukraine/Russia and Strait-of-Hormuz headline flow. **Data-integrity carry-forward, now checked a 3rd time today: the OHLCV-freeze defect is still unresolved** — 11 symbols frozen at 2026-08-15 22:30–23:00 UTC (now ~38.5h stale), 7 of them (HOLO, AVNT, PROM ×2, LUNA, MMT, BABY) are live open crypto swing positions whose displayed TP/SL state remains unverified. Stocks: US futures were "cautious/flat" pre-open per external check (Dow/S&P flat, Nasdaq +0.1%, traders waiting on Walmart/Target earnings + Wednesday FOMC minutes); 32 stocks pre-US candidates were individually scored this cycle via the new overlay — **0 SUPPORT, 9 CAUTION, 17 NEUTRAL, 6 INSUFFICIENT_DATA** — no candidate cleared the bar for genuine catalyst+RS confirmation. Cleanest stocks long-watch remains **COP** (raw A/100, no legal flag, NEUTRAL overlay). Crypto best long-watch: **PORTAL/USDT**, which has now pulled back from +67.7%/24h into its conditional entry zone but still lacks volume confirmation (0.36x avg). Best short-watch: **GRVT/USDT** — but flagged low-conviction: every short candidate scanned today (HOME, DOS, DOLO, GRVT) is capped for thin-liquidity/short-squeeze risk; there is no clean liquid short on the desk. Catalyst mapping continues to weaken through the day (51.8%→57%→**64.2%** unmapped) — use as context only.

**External web research used this cycle** (BTC/ETH levels, Coldcard-exploit follow-up, US stock-futures pre-open mood) — corroborates internal chop/risk-off/cautious-futures read, does not contradict; see §13.

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-16_default_schedule/scheduler.log` — fresh (mtime 15:39 EEST, ~20min old at session start). Latest `cycle_06_13-36_summary.md` (mtime 15:38 EEST, same). Both well under the 3h defer threshold.
- Reports: scalp `2026-08-17_11-13` (gen 14:13 EEST, fresh), intraday `2026-08-17_11-54` (gen 14:54 EEST, fresh, freshest crypto read), swing `2026-08-17_04-22` (gen 07:22 EEST, ~9h old — **carry-forward**, no fresher swing scan this cycle), stocks intraday `2026-08-17_12-22` (gen 15:22 EEST, fresh but market pre-open at generation time — planning-only), stocks swing/invest `2026-07-02` (6+ weeks stale — expected/deprecated per prior project context).
- Catalysts: `data/catalysts/2026-08-17/catalyst_events.jsonl` (1172 events today, mtime 14:59 EEST), `narrative_baskets.jsonl` (5 baskets, same mtime), `catalyst_cycle_11-58.md` (latest cycle summary).
- LLM packets: `llm_analysis_packet.md` (14:55 EEST, fresh), `llm_stocks_packet.md` (15:24 EEST, fresh — no live premarket/gap feed available in this pipeline, confirmed by grep; regime context only).
- CLI: `active-signals` (crypto n=42, stocks n=50), `signal-stats` (crypto: n=66 stronger-confidence, PF 3.18, totalR +28.3, scalp mode weak PF 0.5/-0.5R n=12; stocks: A/B headline sample=8 anecdotal PF 0.0 totalR -1.0, C-tier watchlist n=564 PF 0.18 totalR -9.0 — small-sample/not-actionable), `detect_untracked_legacy_alerts --since 2026-08-17` → **clean**.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 15:35 EEST) — authoritative lifecycle counts, cross-checked against raw OHLCV for the frozen-symbol set.
- Direct OHLCV CSV timestamp re-check (`data/raw/ohlcv/binance/15m/*.csv`) for the 13 previously-flagged symbols — 3rd consecutive cycle today.
- **New this cycle:** `python -m src.cli stocks-preus-candidates` (64 eligible-batch rows / 32 unique symbols, 66 excluded-batch rows / 33 unique symbols with enum reasons) and `stocks-preus-review-ingest` — 32 candidates individually scored, verdicts confirmed via direct DB read of `stocks_preus_review` (all 32 rows, no clamps applied — every requested adjustment was accepted as-is).
- Prior review for comparison: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_1140.md` (Europe/pre-US context, 11:40 EEST).
- **External web research this cycle** (1 WebSearch: BTC/ETH levels Aug 17 2026; 1 WebSearch + 1 WebFetch: US stock-futures pre-market mood; 1 WebSearch: Coldcard exploit follow-up) — corroborates internal regime/risk read, does not contradict.

## 3. Scheduler / Data Freshness

- **Pre-US schedule check: target 08:55 ET, actual fire 08:59 ET (Δ+4min, within tolerance).** Steady-state DST window (not in either 2026 mismatch window: 03-08→03-29 or 10-25→11-01) — Nicosia/NY 7h offset holds.
- **Publish-time drift (NOT a scheduling/DST issue — a processing-latency issue):** this review's write-out completed ~16:40 EEST (09:40 ET), ~41 minutes after the 15:59 EEST fire. Root cause: the two new stocks-preus overlay commands are slow — `stocks-preus-candidates` took ~3 min (500 signals scanned), `stocks-preus-review-ingest` took ~11 min for 32 candidates (~20s/candidate, likely per-row DB re-verification). **By the time this review publishes, the US cash session (09:30 ET) has already been open ~10 minutes.** No fresher intraday/stocks scan exists past the 12:22 UTC (15:22 EEST) stocks-intraday report, so none of the actual post-open price action is reflected here — treat this as the final pre-open snapshot only, not a post-open confirmation read. See TODO-5.
- Scalp: fresh (~1.5h at session start). Intraday: fresh (~1h). Swing: **carry-forward** (~9h, within the 4–12h band, still latest snapshot). Stocks intraday: fresh at generation (~40min old) but was pre-open at generation time. Stocks swing/invest: stale (6+ weeks, expected/deprecated).
- Catalyst folder: fresh (1172 events today), 5 narrative baskets, mapping **weak and worsening** — 64.2% unmapped (vs 57% at 11:40, 51.8% at 04:40); see §5.
- **Monitor/price-feed integrity: CONFIRMED STILL DEGRADED, checked a 3rd time today.** Direct re-check of raw OHLCV (binance 15m) for the 13 symbols flagged at 04:40/11:40:
  - **Still frozen at 2026-08-15 22:30:00+00:00 (now ~38.5h stale), unchanged:** HOLO, MUBARAK, THE, AVNT, PROM, LUNA, MMT, BABY, PEOPLE, BANANAS31, TST. Control symbols (PORTAL, WLFI last row 2026-08-17 12:45 UTC; CHIP 10:30 UTC) all fresh — confirms this remains pair-specific, not a global outage.
  - `PAPER_MONITOR_STATUS_LATEST.md`: **AVNT, MMT (short), PROM ×2, HOLO, LUNA, BABY are all still shown 🟢 OPEN — entry filled, monitoring TP/SL** on the same frozen feed. BMT/MUBARAK/MMT(long) remain `⚪ CLOSED FLAT 0R (expired_flat)` via the same timeout-close path flagged at 11:40, not a genuine resolution.
  - No new symbols joined the frozen set this cycle; no progress on remediation in over 14h of tracking (first observed 02:00 EEST).
- **Authoritative lifecycle counts (PAPER_MONITOR_STATUS_LATEST.md, mtime 15:35 EEST):** OPEN_ACTIVE=16, WAITING_FOR_ENTRY=0, REVIEW_ONLY_SHADOW=0, ENTERED_UNRESOLVED_EXPIRED=0, NO_ENTRY_EXPIRED=155, CLOSED_WIN=159, CLOSED_LOSS=6, CLOSED_FLAT=38, UNKNOWN_INCONSISTENT=0.
- `detect_untracked_legacy_alerts --since 2026-08-17`: **clean**.
- **New this cycle:** stocks-preus overlay ingest completed and verified via direct DB read of `stocks_preus_review` — 32/32 rows present, `clamped_by_gate: false` on every row (my requested adjustments were all within the allowed clamp ranges, so nothing was silently overridden). 0 SUPPORT verdicts issued → 0 candidates promoted toward pre-open Paper-lane eligibility this cycle (SUPPORT is required for promotion; CAUTION/NEUTRAL/INSUFFICIENT_DATA do not unlock it).
- See §14 TODO-1 (updated, still critical), TODO-4 (carried forward, no new check needed), TODO-5 (new — pipeline latency), TODO-6 (new — catalyst-mapping degradation trend).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-17 16:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "bad", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks swing/invest 6wk+ stale (expected/deprecated)", "no live premarket/gap feed", "on-chain whale flows not connected"],
      "suggested_effect": "advisory_only",
      "facts_used": ["3rd consecutive cycle today with 11 symbols on frozen OHLCV (2026-08-15 22:30 UTC, ~38.5h stale)", "7 live crypto positions running on unverified pricing", "review publish delayed ~41min past fire by slow overlay CLI commands, market already open ~10min at publish"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["chop", "risk_off", "mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC range, ETH transition_up, breadth ~51%", "external: BTC $62.3-64K range-bound, ETH ~$1900 capped", "macro risk 96.1-99.8/100, up from 93.7 at 11:40 and 81.5 at 04:40", "stocks: bullish regime label, VIX 14.92, breadth 100%, but futures were flat/cautious pre-open per external check"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": ["most watchlist symbols: zero internal catalyst hits"],
      "suggested_effect": "advisory_only",
      "facts_used": ["1172 events today, 64.2% unmapped (worsening from 57% at 11:40, 51.8% at 04:40)", "momentum_breakout basket: GPS/ACE/TUT/RARE (overextended, avoid_chase)", "BTC exploit_hack + delisting_risk baskets still active", "32 stocks pre-US candidates individually reviewed: 0 SUPPORT / 9 CAUTION / 17 NEUTRAL / 6 INSUFFICIENT_DATA"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["OI 24h% n/a for several MEXC-fallback symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["every short candidate scanned today (HOME, DOS, DOLO, GRVT) is capped by the code for thin_liquidity_short_squeeze_risk", "PORTAL/ONG: price up + OI up, fresh positioning confirms trend"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "entry_late", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PORTAL has pulled back from +67.7% to +35.97%/24h and now sits near (not yet cleanly inside) both its swing (0.0170-0.0179) and intraday (0.0155-0.0163) conditional pullback zones, volume still 0.36x avg — not yet confirmed", "GPS/ACE flagged >2 ATR from EMA20, do-not-chase", "no A/B setups cleared entry-freshness anywhere this cycle"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PAPER_MONITOR_STATUS_LATEST.md authoritative counts: open=16, waiting=0, entered_unresolved=0, review/shadow=0, no-entry/stale=155, closed=159W/6L/38flat", "7 of the 16 open positions run on frozen OHLCV, needs_review"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["headline_risk", "legal_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["5 of 32 pre-US candidates hard-excluded for LEGAL_RISK (HD, SMCI, BLK, INTU, DELL, REGN — some appear twice across batches)", "9 of the 32 reviewed candidates downgraded to CAUTION this cycle for contradicted catalysts, regulatory risk, or upcoming earnings (CRM, MA, V, WMT, NFLX, AMD, COST, AMZN, META)", "BTC Coldcard exploit ~$116M confirmed, multiple attackers suspected, still an overhang", "macro risk 96-99.8/100 driven by Ukraine/Russia + Hormuz headline flow"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["low_sample", "playbook_working", "playbook_failing"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto overall PF 3.18, totalR +28.3R (n=66) — working; scalp mode specifically weak PF 0.5, -0.5R (n=12)", "stocks A/B headline PF 0.0, totalR -1.0 (n=8, anecdotal)", "stocks C-tier watchlist PF 0.18, totalR -9.0 (n=564, reliable but not actionable by definition)"] },
    { "agent": "head_trader", "verdict": "advisory_synthesis_only", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["see section 8 below"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "PORTAL/USDT", "trigger": "1h close and hold inside 0.0155-0.0179 with volume ≥0.7x 20d avg (currently 0.01746, 0.36x avg — not yet confirmed)", "reason": "top-scored crypto C-tier idea across both swing and intraday scans, RS-leader with OI/price confirmation, has pulled back materially from +67.7%/24h into its watch zone but lacks volume confirmation" },
    "best_short_candidate":    { "symbol": "GRVT/USDT", "trigger": "1h close below 0.2918-0.2941 confirming rejection toward 0.2857 — LOW CONVICTION, code-capped for thin_liquidity_short_squeeze_risk same as every other short candidate scanned today", "reason": "least-bad of the squeeze-capped short set (HOME, DOS, DOLO, GRVT); RS negative, 2.49x volume from the last swing scan, but MEXC-only thin liquidity means a genuine squeeze bounce is a real risk, not just a caveat" },
    "best_catalyst_candidate": { "symbol": "PYPL", "trigger": "confirmed (non-rumor) deal news or RTH price/volume confirmation post-open", "reason": "fresh, material, entity-resolved catalyst (reported sale talks with a Stripe/Advent consortium, Yahoo Finance, single-source/rumor-grade) — genuinely watch-worthy but NEUTRAL verdict this cycle because it is unconfirmed and carries elevated gap risk into the open, not a clean long trigger" },
    "avoid_candidate":         { "symbol": "INTU", "reason": "A-raw score 100 but active securities-fraud class-action with a named Sept 8 2026 filing deadline — hard-excluded from the pre-US overlay batch (LEGAL_RISK), consistent with the 11:40 review; do not treat as clean even after the cash open. DELL/REGN/BLK/SMCI carry the same hard exclusion." },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | bad | 0.85 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.75 | chop, risk_off, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.5 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.6 | chase_risk, entry_late, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.7 | open_actionable, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.75 | headline_risk, legal_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.5 | low_sample, playbook_working, playbook_failing | advisory_only |
| head_trader | advisory_synthesis_only | 0.6 | — | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_1140.md` (11:40 EEST, Europe/pre-US context):

- **Macro risk still worsening intraday**: 96.1–99.8/100 this cycle vs 93.7/100 at 11:40 vs 81.5/100 at 04:40 — a consistent, monotonic deterioration across all four reviews today, driven by Ukraine/Russia escalation, Strait-of-Hormuz tension, and continued Coldcard-exploit follow-through.
- **TODO-1 (OHLCV freeze) — unresolved, checked a 3rd time today, no change.** Same 11 symbols frozen, same 7 live positions unverified. No remediation in 14+ hours of tracking.
- **New this cycle: the stocks pre-US overlay ran for the first time** — 32 candidates individually scored (0 SUPPORT / 9 CAUTION / 17 NEUTRAL / 6 INSUFFICIENT_DATA). This is new machinery, not present at 11:40; no candidate was strong enough to earn SUPPORT, so it does not change the "no actionable stocks setup" conclusion, but it materially sharpens the risk picture: CRM (guidance cut/debt-funded buyback), MA/V (Credit Card Competition Act regulatory risk), WMT (earnings in 3 days), AMD (active debt-offering/dilution risk_warning), NFLX (large recent decline, contradicted catalyst), AMZN/META (short-direction signals contradicted by strongly positive fundamentals) were all newly downgraded this cycle — none of these were called out with this level of detail at 11:40.
- **Catalyst mapping weakened further**: 64.2% unmapped vs 57% at 11:40 vs 51.8% at 04:40 — a clear worsening trend across the day (see TODO-6).
- **Crypto regime unchanged**: still range/chop, BTC range / ETH transition_up, no A/B setups in any crypto mode.
- **PORTAL/USDT has pulled back materially**: +67.7%/24h at 04:40/11:40 → +35.97%/24h in the freshest intraday scan → current raw price (0.01746) sits between the two conditional pullback zones defined across snapshots (0.0155-0.0163 intraday / 0.0170-0.0179 swing) — genuinely closer to actionable than at 11:40, still missing volume confirmation.
- **GRVT/USDT downgraded in quality**: still the top short-watch idea, but this cycle's scans explicitly cap it (along with HOME, DOS, DOLO) for `thin_liquidity_short_squeeze_risk` — this caveat was not surfaced at 11:40; treat as lower-conviction than previously implied.
- **Publish-time drift is new and process-related, not market-related**: this review completed ~41 minutes after its scheduled fire (see §3, TODO-5) — a first for this slot since the DST-aware schedule was introduced.
- Thesis on BTC/ETH range/chop and stocks pre-market caution: **confirmed**, not invalidated, by external check.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **1172**. Mapped (non-null symbol): **419** (35.8%). Unmapped: **753** (64.2%). `narrative_baskets`: **5**.
- **Catalyst mapping weak this run and worsening across the day (51.8%→57%→64.2%) — use the catalyst layer as context, not final decision.** See TODO-6.
- Top 3 unmapped headlines (sample): "SK Hynix's Stock Trades at Around 5 Times Next Year's Earnings Even After Revenue Grew 257%..." (duplicate variant also present); "Navy SEALs criticize Trump over Pacific military base readiness issues" — none of these are genuinely unmappable trading-relevant news; they read as generic macro/political wire content that the resolver correctly leaves unmapped, consistent with the pattern flagged at 11:40 (PR-Newswire wire noise, not a resolver defect on its own — but the growing volume is worth tracking, see TODO-6).
- Active narrative baskets: `ai_narrative` (NEAR/RENDER/TAO/FET), `perps_dex_narrative` (HYPE), `delisting_thin_liquidity` (BTC), `rwa_narrative` (ONDO/XLM), `momentum_breakout` (GPS/ACE/TUT/RARE — avoid_chase).

### Pre-US Stocks Review Overlay
- candidates reviewed: 32 (SUPPORT 0 / NEUTRAL 17 / CAUTION 9 / BLOCK 0 / INSUFFICIENT_DATA 6)
- session-cap-only C's now eligible for pre-open Paper lane: **0** (SUPPORT is required for promotion; none issued this cycle)
- excluded by hard gate: 7 unique symbols (33 rows across two duplicate batches) — HD (LEGAL_RISK, earnings-adjacent), SMCI (LEGAL_RISK: indictment), BLK (LEGAL_RISK: class_action), INTU (LEGAL_RISK: class_action/securities_fraud), DELL (LEGAL_RISK: indictment), REGN (LEGAL_RISK: class_action), LLY (EARNINGS_BLACKOUT); remaining exclusions were NO_ENTITY_RESOLVED_CATALYST (26 symbols: NVO, NKE, QCOM, MAR, AMAT, RIOT, TXN, PEP, XLC/XLY/XLU/IWM sector ETFs, AFRM, VRTX, DDOG, KO, CMCSA, BA, SOFI, GILD, ARM, ASML, LRCX, LMT, XLE, DIS)
- Full CAUTION detail (enforced, confirmed via direct DB read of `stocks_preus_review`): CRM −5 (100→95, guidance cut/debt-funded buyback contradicts long), MA −4 (92.8→88.8, Credit Card Competition Act regulatory headline), NFLX −5 (82.1→77.1, dropped to B tier — contradicted by large recent decline), AMD −6 (81.3→75.3, dropped to B tier — active offering_dilution production risk_warning), V −4 (71.0→67.0, same regulatory headline as MA), WMT −5 (77.0→72.0, earnings in 3 trading days), AMZN −5 (55.8→50.8, short signal contradicted by bullish capex-guidance headline), META −6 (60.3→54.3, short signal contradicted by strong ARPU/user-growth print), COST −3 (62.8→59.8, valuation-concern headline).

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **chop, risk-off leaning, worsening intraday** (range regime, macro risk 96.1–99.8/100 vs 93.7 at 11:40 vs 81.5 at 04:40 — a clean monotonic deterioration across today's cycles; external check corroborates BTC range-bound $62.3-64K, ETH capped ~$1,900).
- Stocks mood: **pre-open, cautious/flat underlying** — regime label bullish, VIX 14.92, breadth 100%, all 4 indices in 5d/20d uptrend, but external check confirms US futures were flat/barely-moved pre-open (Dow flat, S&P flat, Nasdaq +0.1%) with traders waiting on Walmart/Target earnings and Wednesday's FOMC minutes after a sharp retail-sales miss reshaped rate expectations — this is a genuinely quiet, wait-and-see setup, not a risk-on gap-up morning.
- Dominant narrative: momentum-breakout/chase-risk names (GPS/ACE/TUT/RARE) in crypto; AI-capex mega-cap story (Google/Amazon/Meta ~$600B raised guidance) and the Coldcard hardware-wallet exploit overhang in crypto/crypto-equities (MSTR, RIOT).
- Preferred side now: **wait-for-trigger** — chop regime, worsening macro risk score, and a flat/cautious pre-open stocks tape all argue against forcing directional risk; none of the four candidates below are actionable without further confirmation.
- Best long candidate: PORTAL/USDT (crypto, watch — pulled back into range but volume unconfirmed) / COP (stocks, watch — needs RTH confirmation, now ~10min post-open with no fresher scan yet).
- Best short candidate: GRVT/USDT (crypto, watch, low-conviction — squeeze-risk capped along with every other short candidate scanned today).
- Best catalyst-backed candidate: PYPL (stocks, watch — fresh sale-talks rumor, single-source, elevated gap risk, needs confirmation not chase).
- What to avoid: INTU, DELL, REGN, BLK, SMCI (stocks — active legal/headline risk, hard-excluded from the overlay, do not treat as clean even post-open); CRM/MA/V/WMT/NFLX/AMD/COST/AMZN/META (stocks — this cycle's CAUTION downgrades, contradicted catalysts/regulatory/earnings risk); HOLO, AVNT, PROM (×2), LUNA, MMT, BABY (crypto, currently "open" positions on frozen OHLCV — do not treat displayed TP/SL as reliable).
- What would change the view: a clean BTC reclaim/hold above $64K or ETH clearing ~$1,922 would flip crypto mood toward risk-on; a confirmed OHLCV-feed fix would clear the data-integrity caution; RTH price/volume confirmation (not yet available — no post-open scan has run) would make the non-legal-risk, non-CAUTION stocks names genuinely actionable.

## 7. Candidate Deep Dives

### PORTAL/USDT (crypto, best long-watch)
- Has price already reacted to the catalyst? No verified catalyst exists; this is a pure `momentum_breakout` basket member (no news attached) that has now partially mean-reverted (+67.7%/24h at 04:40/11:40 → +35.97%/24h in the 11:15 UTC intraday scan → current raw close 0.01746 at 12:45 UTC).
- Is the setup chasing? Less than at 11:40 — the pullback has already happened; chasing risk is now lower, but confirmation risk (volume) is still open.
- Retest/pullback structure? Price is now sitting between the two conditional zones defined across today's scans: intraday-mode zone 0.0155-0.0163 (from an 11:15 UTC snapshot at price 0.0167) and swing-mode zone 0.0170-0.0179 (from a 04:00 UTC snapshot at price 0.0184). Current price (0.01746) is just inside the swing zone and just above the intraday zone — genuinely in the target retracement area, not yet a clean confirmed hold.
- Overextended (>2 ATR from EMA20)? Less so than earlier today; the pullback has partially resolved this.
- Would entry now be late? Borderline — closer to on-time than at 11:40, but volume (0.36x 20d avg) still does not confirm.
- What level makes it actionable? A 1h close and hold inside 0.0155-0.0179 with volume picking up toward ≥0.7x avg.
- Aligned with market mood? Partially — chop/wait-for-trigger mood argues for waiting on volume confirmation rather than entering on price alone.
- Long, short, or wait-for-trigger? Wait-for-trigger (long bias if volume confirms the hold).
- Actionable now or after confirmation? After confirmation only.
- Invalidation: 1h close below 0.0146 (intraday-mode level, tighter than the swing-mode 0.0159).
- Chase-risk setup? Reduced vs 11:40, not eliminated.
- Catalyst confirmation/contradiction? No catalyst either way — pure momentum/derivatives read (funding near-zero, OI +84% confirming fresh positioning).

### GRVT/USDT (crypto, best short-watch — low conviction)
- Has price already reacted? Yes, and further than at 11:40 — 24h move has deepened from -1.02% (04:22 swing snapshot) to -6.40% (11:15 UTC intraday snapshot); this is a continuation short, not a fresh breakdown chase.
- Chasing? No — volume (2.49x from the last full swing scan) confirms distribution rather than a low-volume drift.
- Retest structure? Yes — conditional failed-bounce/retest zone 0.2918-0.2941 (swing-mode, from the 04:22 scan at price 0.2908); no fresher intraday-mode trade idea exists for GRVT this cycle to update the level.
- **Squeeze risk — new this cycle:** the intraday scan explicitly caps GRVT (score 46.3) for `thin_liquidity_short_squeeze_risk`, and this is not unique to GRVT — every short-biased symbol scanned today (HOME -9.07%/24h, DOS -8.61%/24h, DOLO -7.02%/24h, GRVT -6.40%/24h) carries the identical cap. This means there is currently **no clean liquid short on the desk** — GRVT is the least-bad of a systematically squeeze-flagged set, not a genuinely clean setup. GRVT is also MEXC-only (`high_risk_only=True`, confirmation 38/100).
- Overextended? No — moderate decline, not vertical.
- Late entry risk? Low if triggered on the retest zone; the deepening 24h move argues for tighter risk than the 11:40 framing implied.
- Actionable level: 1h close beyond 0.2969 invalidates; short thesis wants rejection at/below 0.2918-0.2941 toward TP1 0.2857.
- Aligned with mood? Directionally yes (risk-off macro backdrop favors shorts on RS-negative names), but the squeeze-risk cap is a genuine structural caution, not just a footnote.
- Long/short/wait? Short, wait-for-trigger, low-conviction given the squeeze cap.
- Catalyst confirmation/contradiction? None either way.

### COP (stocks intraday, C-tier watchlist — best stocks long-watch, pre-open planning only)
- Raw tier A, base score 100.0, overlay verdict **NEUTRAL** (adjustment 0, adjusted score 100.0) — reviewed this cycle: the only catalyst found was a generic "Best Energy Stocks" listicle mention, not a material event; energy sector (XLE) is one of today's strongest sectors (+7.33% 20d, RS +2.89% vs SPY), which is genuinely supportive context but does not itself clear the bar for a SUPPORT verdict (no entity-resolved material catalyst).
- Demoted to C purely for `market_closed_intraday_planning_only` — a session-state gate, not a quality problem with the setup.
- Actionable now or after confirmation? By publish time (~09:40 ET) the cash session has technically been open ~10 minutes, but **no post-open scan has run yet** — treat the pre-open planning level (entry ~126.78, stop ~125.83) as context only until a fresh intraday report confirms RTH price/volume action.
- Legal/headline risk: none found for COP.
- Sector context: energy strength is a genuine tailwind for the thesis, just not a hard catalyst.

### PYPL (stocks intraday, C-tier watchlist — best catalyst-watch, elevated gap risk)
- Raw tier A, base score 99.68, overlay verdict **NEUTRAL** (adjustment 0) — catalyst is fresh and material (Yahoo Finance, 2026-08-17: PayPal "reportedly in sale talks with a consortium including Stripe and Advent") but explicitly single-source/rumor-grade, not confirmed. Per the overlay's SUPPORT bar, a rumor-only catalyst cannot earn SUPPORT regardless of how material it looks.
- Has price already reacted? Unknown — no post-open scan available yet (see §3 publish-drift note); this kind of headline is a classic gap-risk driver, so pre-open planning levels should be treated with extra caution until RTH price action confirms or the rumor is denied/confirmed by a primary source.
- Actionable level: needs either (a) a primary-source confirmation/denial of the sale talks, or (b) RTH price/volume action once a fresh post-open scan runs.
- Legal/headline risk: none found beyond the M&A-rumor gap-risk itself.

### INTU (stocks intraday, C-tier watchlist) — avoid candidate
- Raw tier A, score 100, hard-excluded from this cycle's overlay batch (`LEGAL_RISK`) — internal catalyst event: "APPROACHING DEADLINE ALERT: Intuit Inc. (INTU) Investors: September 8, 2026, Filing Deadline in Securities Fraud Class Action" (PR Newswire), unchanged from the 11:40 review.
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED**, never a clean actionable, even after the cash open, until the legal situation is resolved or the flag is manually cleared by a human review. DELL, REGN, BLK, SMCI carry the same hard exclusion this cycle.

## 8. Best Candidates Ranked

1. **PORTAL/USDT** — long-watch (crypto), now inside its conditional retracement zone but needs volume ≥0.7x avg to confirm; do not enter on price alone.
2. **COP** — long-watch (stocks), cleanest raw-A pre-open name (no legal flag), needs RTH confirmation — none available yet at publish time.
3. **GRVT/USDT** — short-watch (crypto), low-conviction — squeeze-risk capped along with the entire short-biased watchlist today.
4. **PYPL** — catalyst-watch (stocks), fresh but rumor-grade M&A headline, needs primary-source confirmation or RTH action before acting; elevated gap risk either way.

No clean actionable trade exists in this decision window for any mode — this applies only to the current window, not a system-wide stop.

## 9. Avoid / No Trade

- **INTU, DELL, REGN, BLK, SMCI** (stocks) — active legal/headline risk (securities fraud, indictment, class action); hard-excluded from the pre-US overlay, avoid even if they trigger a clean technical setup post-open.
- **CRM, MA, V, WMT, NFLX, AMD, COST, AMZN, META** (stocks) — this cycle's CAUTION-downgraded candidates: contradicted catalysts (CRM guidance cut, AMZN/META short-direction contradicted by bullish fundamentals, NFLX large decline), regulatory risk (MA/V — Credit Card Competition Act), upcoming earnings (WMT, 3 days out), active production risk_warning (AMD — debt/dilution offering), or valuation-concern headline (COST). None of these should be treated as clean even with a favorable raw score.
- **HOLO, AVNT, PROM (×2), LUNA, MMT, BABY** (crypto, currently "open" positions) — running on a frozen OHLCV feed (~38.5h stale, 3rd consecutive confirmed-unresolved check today); do not treat their displayed TP/SL/invalidation state as reliable until the feed is confirmed fixed. Data-integrity caution only, no execution action authorized by this review.
- This is a decision-window caution only. Scanning, tracking, and candidate generation continue uninterrupted across all modes.

## 10. Main Risks

- **OHLCV-freeze defect, now ~38.5h old, confirmed unresolved a 3rd time today** — directly contaminates the displayed state of 7 live crypto positions; the closest thing to a live-risk issue this review has surfaced (see TODO-1).
- **Publish-time drift**: this review completed ~41min after its scheduled fire, ~10min after the US cash open, with no fresher post-open data available — decisions based on this review's stocks section should be treated as pre-open context, not post-open confirmation (see TODO-5).
- Elevated and still-worsening macro risk (96.1–99.8/100 this cycle, up from 81.5 at 04:40) driven by Ukraine/Russia and Strait-of-Hormuz headline flow — a broad risk-off headwind for crypto beta.
- Coldcard exploit overhang: external check confirms ~$116M / 1,778+ BTC stolen across 5,000+ addresses, multiple attackers suspected, still an active tracking situation — a standing liquidation/dump risk.
- Systemic short-side squeeze-risk cap today (HOME, DOS, DOLO, GRVT all flagged) — no genuinely clean liquid short exists on the crypto desk.
- Weak and worsening catalyst mapping (64.2% unmapped, up from 51.8% at 04:40) reduces confidence in any catalyst-backed read this cycle (see TODO-6).
- 9 of 32 stocks pre-US candidates carry newly-surfaced CAUTION flags (regulatory, earnings, contradicted catalysts, active risk warnings) that a naive score-only read would have missed entirely.

## 11. Action Plan — next 4 hours

- Watch PORTAL/USDT for a 1h close/hold inside 0.0155-0.0179 with volume ≥0.7x avg before considering a long; do not enter on the pullback alone.
- Watch GRVT/USDT for a 1h close below 0.2918-0.2941, but size down or skip given the systemic squeeze-risk cap across the entire short-biased watchlist today.
- Run (or wait for) the next post-open stocks intraday scan before treating COP, PYPL, or any of the other 15 non-excluded overlay candidates as genuinely actionable — none of this review's stocks levels reflect actual RTH price action yet.
- Do not act on INTU/DELL/REGN/BLK/SMCI regardless of score until legal flags clear; do not act on CRM/MA/V/WMT/NFLX/AMD/COST/AMZN/META without independently re-verifying the specific CAUTION reason no longer applies.
- Re-check HOLO/AVNT/PROM/LUNA/MMT/BABY OHLCV freshness next cycle; if still frozen, this becomes a 4th-consecutive-today confirmed-unresolved cycle and should be escalated further (TODO-1).
- Flag pipeline latency (TODO-5) and catalyst-mapping trend (TODO-6) for a human maintenance session.

## 12. Final Verdict per Mode

- **Crypto scalp**: No trade — no A/B setups, weak mode-level stats this window (PF 0.5, -0.5R, n=12).
- **Crypto intraday**: No trade — no A/B setups; RARE/ONG/PORTAL/PUMP watchlist only, all low-confidence.
- **Crypto swing**: Wait-for-trigger — PORTAL (long, needs volume confirmation) and GRVT (short, low-conviction/squeeze-capped) are the two watch candidates.
- **Stocks intraday**: Planning only — market technically open ~10min at publish but no post-open scan exists yet; watch COP + PYPL + 15 other non-excluded, non-CAUTION overlay names for RTH confirmation; hard-avoid the 5 legal-risk names and treat the 9 CAUTION names as degraded even if they trigger.
- **Stocks swing/invest**: N/A — deprecated/stale, not evaluated.

## 13. Sources

- [Crypto Price Prediction August 17, 2026: Bitcoin, Ethereum and XRP Face Key Support Levels](https://sundayguardianlive.com/business/crypto-price-prediction-august-17-2026-bitcoin-ethereum-and-xrp-face-key-support-levels-as-traders-await-breakout-signals-262800/) — Sunday Guardian Live, 2026-08-17
- [Ethereum Price is $1,900.69 today](https://metamask.io/price/ethereum) — MetaMask, 2026-08-17
- [Bitcoin, Futures, and Pre-Market Sentiment on August 17, 2026](https://en.cryptonomist.ch/2026/08/17/bitcoin-stock-futures-update/) — Cryptonomist, 2026-08-17
- [The Largest Hardware Wallet Exploit of 2026: Inside the USD 116 Million Coldcard Hack](https://www.trmlabs.com/resources/blog/the-largest-hardware-wallet-exploit-of-2026-inside-the-usd-116-million-coldcard-hack) — TRM Labs, date unavailable (recent)
- [Coldcard wallet exploit leads to theft of over 1,778 Bitcoin worth $112M](https://cryptobriefing.com/coldcard-wallet-exploit-bitcoin-theft-112m/) — CryptoBriefing, date unavailable
- Internal: `data/catalysts/2026-08-17/catalyst_events.jsonl` (1172 events), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_11-58.md`
- Internal: `data/reports/scalp/2026-08-17_11-13_scalp_report.md`, `data/reports/intraday/2026-08-17_11-54_intraday_report.md`, `data/reports/swing/2026-08-17_04-22_swing_report.md`, `data/reports/stocks/intraday/2026-08-17_12-22_stocks_intraday_report.md`
- Internal: `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 15:35 EEST), `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (generated 13:01:04 UTC), `stocks_preus_review` DB table (32 rows, direct-read verified)

## 14. Fix Requests / TODO

### TODO-1: Stale OHLCV / false-"OPEN" defect — still unresolved, checked a 3rd time today, no remediation
- **issue:** binance 15m OHLCV fetch remains frozen at 2026-08-15 22:30:00+00:00 (now ~38.5h stale) for 11 symbols (HOLO, MUBARAK, THE, AVNT, PROM, LUNA, MMT, BABY, PEOPLE, BANANAS31, TST). Of these, 7 (HOLO, AVNT, PROM ×2, LUNA, MMT, BABY) are currently live `triggered`/open positions — their TP/SL/invalidation display cannot be trusted. First flagged 02:00 EEST 2026-08-17; confirmed present at 04:40, 11:40, and now 15:59/16:40 EEST — unchanged across all four checks today, no progress in 14+ hours.
- **evidence:** `data/raw/ohlcv/binance/15m/{HOLO,MUBARAK,THE,AVNT,PROM,LUNA,MMT,BABY,PEOPLE,BANANAS31,TST}_USDT.csv` last row still `2026-08-15 22:30:00+00:00` (re-checked 2026-08-17 ~16:00 EEST); control symbols (PORTAL, WLFI, CHIP) fresh (12:45/12:45/10:30 UTC respectively). `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 15:35 EEST) still shows AVNT/MMT/PROM×2/HOLO/LUNA/BABY as 🟢 OPEN.
- **suggested manual fix:** unchanged from 11:40 — identify why the OHLCV ingest job has not recovered for these specific symbols across 14+ hours despite unaffected pairs refreshing normally; add an automated staleness alarm (any active-signal symbol whose latest candle is >2h behind the batch's freshest candle should page/flag); audit whether the expiry-timeout close path should be allowed to resolve a signal to `CLOSED FLAT` when its underlying OHLCV is itself known-stale.
- **priority:** critical (unchanged — unresolved across 4 review cycles today, still directly affecting 7 live position displays).
- **first observed:** 2026-08-17 02:00 EEST; confirmed unresolved again 2026-08-17 15:59/16:40 EEST (3rd re-confirmation today).

### TODO-4 (carried forward, unrelated): long-tail `active-signals` rows lingering weeks past expires_at
- **issue:** per the 11:40 review, a large share of `active-signals` rows carry `status` in `{triggered, tp1_hit, tp2_hit}` with `expires_at` weeks in the past, unrelated to the OHLCV-freeze bug. Not re-verified in detail this cycle — `PAPER_MONITOR_STATUS_LATEST.md`'s cleaner lifecycle-group counts (NO_ENTRY_EXPIRED=155, CLOSED_WIN/LOSS/FLAT=159/6/38) suggest this view is more reliable than the raw `active-signals` CLI table for lifecycle questions; recommend preferring it going forward.
- **evidence:** `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_1140.md` §14 TODO-4.
- **suggested manual fix:** unchanged — a human session should confirm intended `active-signals` semantics ("ever opened" vs "currently open") and whether a CLI filter/archival job is needed.
- **priority:** medium (data-hygiene, not live-risk).
- **first observed:** 2026-08-17 11:40 EEST.

### TODO-5 (new): stocks-preus overlay pipeline is too slow for its own decision window
- **issue:** the two new stocks-preus overlay commands (`stocks-preus-candidates`, `stocks-preus-review-ingest`) took ~3 min and ~11 min respectively this run (32 candidates, ~20s/candidate on the ingest side). Combined with research time, this pushed the review's publish time to ~16:40 EEST (09:40 ET) — ~41 minutes after the 15:59 EEST scheduled fire, and ~10 minutes after the actual 09:30 ET US cash open. A review whose stated purpose is "the final pre-open read" should not itself finish after the open.
- **evidence:** `stocks-preus-candidates` background command ran ~15:59:26→16:01:04 EEST (per `generated_at` in `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`); `stocks-preus-review-ingest` background command (PID 21924) ran 16:09:26→~16:20 EEST per process creation time and completion notification.
- **suggested manual fix:** profile `stocks_preus_review.record_verdict` for the per-candidate latency source (looked like per-row DB re-verification/locking, ~20s/row); consider batching the DB writes in a single transaction instead of one connection/transaction per candidate; consider whether `stocks-preus-candidates`'s ~500-signal full scan can be narrowed or cached for the pre-US slot specifically, since this slot has a hard real-world deadline (the cash open) that other slots don't.
- **priority:** medium-high (doesn't corrupt data, but undermines the slot's stated purpose if it recurs).
- **first observed:** 2026-08-17 16:40 EEST (first run of this overlay).

### TODO-6 (new): catalyst-mapping coverage degrading monotonically through the day
- **issue:** unmapped catalyst-event share has risen every single review today: 51.8% (04:40) → 57% (11:40) → 64.2% (15:59/16:40). This is a consistent trend, not noise, across three consecutive independent checks in one calendar day.
- **evidence:** `data/catalysts/2026-08-17/catalyst_events.jsonl` — 1172 total events, 419 mapped / 753 unmapped this cycle, computed directly from the JSONL (not just the latest catalyst_cycle_*.md snapshot).
- **suggested manual fix:** a human session should pull a larger unmapped-headline sample (this review only spot-checked 3) and determine whether the growth is purely volume-driven (more late-day wire/PR-Newswire noise as the day progresses) or a genuine resolver regression; if volume-driven, consider whether the >50% mapping-weak threshold should be time-of-day-aware rather than a flat cutoff.
- **priority:** medium.
- **first observed:** 2026-08-17 15:59/16:40 EEST (trend first quantified across the whole day this cycle; individual readings were noted at 04:40 and 11:40 but not tracked as a trend until now).
