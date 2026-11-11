# Opus Enriched Review — Europe / pre-US context — Auto Cycle 12:04 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context** (11:30 slot, fired ~12:04 EEST due to dispatch jitter). **Advisory only — no auto-trade, no scoring/threshold/routing changes.**

Crypto technicals are genuinely risk-on (BTC/ETH uptrend, altcoin breadth 90.9% above EMA20) but macro/geopolitical risk is scored **100/100** by the desk's own macro layer (Iran vs. Strait-of-Hormuz sanctions escalation) — this is a real tension, not noise, and argues for tighter invalidations rather than a blanket no-trade. No A-tier crypto setups exist anywhere (intraday or swing); every one of the 50 open crypto positions is a **B-tier long** — the system is not generating any short candidates right now because the trend genuinely is up.

Stocks: US cash session is **closed** (pre-open) — every stocks A-tier idea (ABNB, SHOP, TSLA, SNOW, ADBE, CMCSA, PLTR, CRM, UBER, HOOD, MA, SBUX, SMCI, COP, COIN) is demoted to C/watchlist-only per the desk's own `market_closed_intraday_planning_only` gate. This week's realized stocks performance is a clean directional signal in its own right: **A/B longs are −16.5R (PF 0.08, n=334) vs. shorts +1.5R (PF 1.30, n=384)** — shorts are the higher-probability side once RTH confirms a setup.

**Integrity note:** `SMCI` still carries an internal `active legal/headline risk (indictment) — manual review required` flag, but external verification (Supermicro IR, Aug 20 2026) shows the independent board investigation **concluded and cleared current senior management** four days ago — the internal flag is stale relative to that resolution. Flagged as TODO-3, not auto-corrected.

Catalyst mapping is weak this run (74.6% unmapped) — treat the catalyst layer as context, not a final decision input. This review also surfaces a 5-day gap in the scheduled-review cadence (last successful run 2026-08-19 16:33 EEST) — see TODO-1.

## 2. Data Used

- Reports: intraday crypto (2026-08-24 09:47 EEST, fresh ~2h17m), scalp crypto (09:37, fresh ~2h27m), swing crypto (07:10, ~4h54m old → 4-12h band, **carry-forward**), stocks intraday (10:21, fresh ~1h43m, pre-open at generation and now).
- Stocks swing/invest: deprecated framework, stale since 2026-07-02 — excluded per prior guidance.
- `data/processed/llm_analysis_packet.md` (09:50), `data/processed/llm_stocks_packet.md` (10:24).
- `data/catalysts/2026-08-24/catalyst_events.jsonl` (1000 rows this run), `narrative_baskets.jsonl` (4 baskets), `catalyst_cycle_06-53.md`.
- CLI: `active-signals` (crypto 50 rows, stocks 50 rows — all stocks rows have `expires_at` in the past, i.e. historical/closed, not live), `signal-stats` (crypto + stocks, week window), `detect_untracked_legacy_alerts --since 2026-08-24` (0 findings).
- External: WebSearch ×2 (SMCI indictment/investigation status; BTC/ETH price action Aug 24 2026) + implicit fetch of the top SMCI result content.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_1630.md` — **5-day gap**, see §4 and TODO-1.

## 3. Scheduler / Data Freshness

- Active scheduler folder: `data/scheduled_runs/2026-08-23_default_schedule/`. `scheduler.log` mtime **10:38 EEST** (~1h26m old), latest `cycle_05_09-26_summary.md` mtime **10:38 EEST** (~1h26m old) — both well inside the 3h defer threshold. **Not deferred.**
- Intraday/scalp/stocks-intraday reports all fresh (<3h). Crypto swing report ~4h54m old — inside the 4-12h carry-forward band, used with that caveat.
- Catalyst data fresh (generated same-day, 1000 events collected this cycle, actively growing).
- No monitor/paper-portfolio status file read this run (outside the allowed read set); lifecycle status inferred from `active-signals` + reports.
- **Cadence gap:** the most recent prior `OPUS_ENRICHED_REVIEW_AUTO_*.md` on disk is dated 2026-08-19 16:33 EEST — no deferred/blocked marker exists for the intervening ~5 days, meaning this scheduled task simply did not fire (or did not complete) across that window. Not diagnosable further from this run's allowed toolset. See TODO-1.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-24 12:04 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["cause of the 2026-08-19 to 2026-08-24 review-cadence gap", "live monitor/paper-portfolio status file"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle_05 summary both ~1h26m old", "crypto swing report ~4h54m old, inside 4-12h carry-forward band", "5-day gap since last OPUS_ENRICHED_REVIEW_AUTO_*.md with no deferred/blocked marker"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_on", "mixed", "longs_preferred"],
      "data_missing": ["live intraday US futures/VIX read (no chart/quote MCP loaded)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, altcoin breadth 90.9% above EMA20/EMA50, desk label 'bullish trend (risk-on)'", "macro layer: geopolitical risk 100/100 from Iran/Strait-of-Hormuz sanctions escalation headlines — 6 risk-off hits, 0 risk-on hits", "stocks: desk regime label 'transition/neutral', VIX 15.13 (low), breadth 75%/100% (EMA20/EMA50), 2/4 indices uptrend, market closed pre-open"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 254/1000 mapped (74.6% unmapped) this cycle", "NEAR/USDT: importance-0.80 regulatory/partnership catalyst (quantum-resistant transfer pilot), fresh <1h, ai_narrative basket primary", "momentum_breakout basket (SPK/PROM/TUT/ZAMA/ETHFI) explicitly labeled 'top gainers without confirmed news catalyst — pure momentum cluster'", "ETH/USDT: importance-0.86 exploit_hack catalyst (Term Finance $8.5M vault exploit) — risk-flagged, not a long-thesis catalyst"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.55,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["OI% for MEXC-fallback names (ZAMA, MORPHO, ETHFI, TUT, PROM)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["SPK/PENGU: price up + OI up, funding ~5e-05 (neutral), crowding normal", "INJ: price up + OI down (short covering, weaker continuation quality)", "Bybit/OKX/MEXC cross-check funding neutral, crowding 'low' for ZAMA/MORPHO/ETHFI/TUT/PROM", "no funding_extreme reading anywhere in today's derivatives block"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["overextended", "chase_risk", "clean_retest", "entry_fresh"],
      "data_missing": ["TradingView / manual chart check unavailable — using local OHLCV/ATR/EMA fields only"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PENGU/SPK/ZAMA/TUT/PROM already up 10-30% over 24h, 24-60% over 7d — market-buy chase risk high", "every intraday/swing idea in today's reports explicitly plans a pullback entry zone, not a market order", "NEAR triggered swing entry 1.9948-2.0129, current desk price context consistent with an already-filled entry, not a fresh chase"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry"],
      "data_missing": ["exact live PnL / distance-to-invalidation for each open position (no live-price read in allowed toolset)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: ~38 of 50 active B-tier signals are ENTERED (triggered/tp1_hit/tp2_hit), 12 WAITING FOR ENTRY, 0 stopped/closed in the visible window", "stocks: 0 OPEN ACTIONABLE — all A-tier ideas demoted to C (market-closed planning-only gate), 15 symbols in NEEDS-REVIEW/WATCH via C-tier list"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["SMCI: internal legal/headline flag (indictment) still active, but Supermicro IR (2026-08-20) shows the independent board probe concluded and cleared current senior management — flag likely stale, needs reconciliation (TODO-3)", "INTU: earnings tomorrow 2026-08-25, do-not-chase warning already active in production", "Iran/Strait-of-Hormuz headline risk elevated across multiple sources today"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing RS-momentum playbook (PENGU/ENA/MORPHO/ETHFI/SPK): 14d WR 72% / PF 5.80 / +24R — the desk's best-performing cohort", "crypto intraday overall: PF 2.49, totalR +50.8 (week, n=156) — strong", "crypto scalp mode: PF 0.17, totalR -2.5, 0 wins / 3 losses (week, n=91) — clearly broken (TODO-4)", "stocks A/B intraday longs: PF 0.083, totalR -16.5 (n=334) vs shorts PF 1.30, totalR +1.5 (n=384) — directional edge has flipped to shorts (TODO-5)"] },
    { "agent": "head_trader", "verdict": "caution",
      "reason_codes": ["route_not_block", "selective_longs_crypto", "selective_shorts_stocks"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "NEAR/USDT", "trigger": "already triggered swing long 1.9948-2.0129, inv 1.9727; RS-leader in ai_narrative basket with a fresh (<1h) importance-0.80 regulatory/partnership catalyst", "reason": "catalyst-backed + RS-leader combination is the desk's cleanest current long" },
    "best_short_candidate":    { "symbol": "none live", "trigger": "crypto: wait for BTC/ETH to break uptrend structure, or a confirmed breakdown (with volume) in a weakest-symbol name (SNDKB, SKHYB, PUMP, BOME); stocks: wait for RTH confirmation of a failed bounce or weak-sector (XLU/XLRE/XLI) breakdown post-open — historical stats favor shorts (PF1.30) over longs (PF0.083) this week", "reason": "no directional short setup exists in either asset class right now; trend genuinely is up in crypto and stocks market is closed" },
    "best_catalyst_candidate": { "symbol": "NEAR/USDT", "trigger": "regulatory/partnership catalyst (quantum-resistant transfer pilot), importance 0.80, fresh <1h, basket-confirmed", "reason": "only current long candidate with both a verified fresh catalyst and RS leadership" },
    "avoid_candidate":         { "symbol": "SMCI", "reason": "internal legal/headline-risk flag (indictment) still active and forces manual-review status; external verification shows the underlying investigation concluded favorably 4 days ago, so the flag needs reconciliation before any new consideration either way" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | risk_on, mixed, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.55 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | overextended, chase_risk, clean_retest, entry_fresh | advisory_only |
| execution_lifecycle | ok | 0.70 | open_actionable, waiting_for_entry, no_entry | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.75 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | — (synthesis) | route_not_block, selective_longs_crypto, selective_shorts_stocks | advisory_only |

## 4. What Changed vs Previous Review

Previous review unavailable in the normal cadence — the last one is `OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_1630.md`, roughly **5 days / ~30 review cycles old**. Treat any comparison below as low-precision; it is a coarse before/after, not a cycle-to-cycle diff (see TODO-1).

- **Crypto regime:** was chop/range-ish with the desk regime label caution on 08-19; now clearly labeled "bullish trend (risk-on)" with 90.9% breadth above EMA20 — a genuine regime shift toward trend-following longs.
- **Catalyst mapping:** was 79.8% unmapped on 08-19, now 74.6% unmapped — marginally better but still weak; the underlying symbol-resolver issue from the prior review persists (see TODO-2, echoes [[project_crypto_ai_desk_catalyst_linkage]] in memory).
- **Bias-tag contradiction pattern** (open long scored short by the desk's own current scan — GPS/USDT, ZBT/ACE, EDEN/USDT in prior reviews): not observed in today's active-signals snapshot, but this review did not re-run the same live-price cross-check the 08-19 review used (outside today's allowed toolset), so absence of evidence is not confirmation it's resolved.
- **Untracked-alert integrity bug** ([[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]): 0 findings today, consistent with the 08-19 review.
- **New this cycle:** SMCI stale-legal-flag / investigation-cleared contradiction (TODO-3); crypto scalp mode's profit factor has collapsed to 0.17 (TODO-4); stocks A/B intraday long-side edge has flipped decisively negative vs. a positive short-side edge (TODO-5).

## 5. Catalyst Coverage

- Total catalyst events today: **1000** (scanned from `news_items`).
- Mapped (non-null symbol): **254** (25.4%).
- Unmapped (null symbol): **746** (74.6%).
- Narrative baskets: **4** (`ai_narrative`, `perps_dex_narrative`, `binance_ecosystem_teaser`, `momentum_breakout`).

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped headlines (sample):
- "Bybit now supports $GROVE deposits and withdrawals on Mantle Network with @Mantle_Official..."
- "NOMURA INTERNATIONAL FUNDING SECURED AN 'A-' CREDIT RATING FROM FITCH RATINGS FOR ITS NEWLY ISSUED SOUTH KOREAN WON (KRW) SENIOR UNSECURED DEBT..."
- "Pulnovo Medical Announces First Two U.S. Patients Enrolled in PULSE-LHD IDE Clinical Trial..."

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **risk-on (technical) with a macro overhang** — BTC/ETH uptrend, 90.9% breadth above EMA20/EMA50, but the desk's own macro layer scores geopolitical risk 100/100 (Iran vs. Strait-of-Hormuz sanctions escalation, 6 risk-off headline hits, 0 risk-on hits today).
- Stocks mood: **neutral/transition, pre-open** — VIX 15.13 (low), breadth 75%/100% (EMA20/EMA50), 2/4 indices in uptrend; empirically the week's realized A/B performance favors shorts (PF 1.30) over longs (PF 0.08) despite the neutral regime label.
- Dominant narrative: crypto — RS-leader/narrative-basket momentum (AI names, perps-DEX names, momentum-breakout cluster) with almost no verified fresh catalysts behind the biggest movers; stocks — AI/chip-supply-chain headlines (NVDA earnings in 2 days, AMD-TSMC packaging investment) plus a fresh legal-risk headline cluster (multiple securities-fraud-lawsuit PR items).
- Preferred side now: **mixed** — selective RS-leader/catalyst-backed longs in crypto; wait for RTH confirmation before any stocks trade, with a short-side lean once confirmed.
- Best long candidate: **NEAR/USDT** (see §8).
- Best short candidate: **none live** — crypto trend is up-only right now; stocks market is closed. See §8 for exact triggers.
- Best catalyst-backed candidate: **NEAR/USDT**.
- What to avoid: **SMCI** (stale legal flag, needs reconciliation — see §7/§9), and chasing any of the momentum-breakout names (SPK/PROM/TUT/ZAMA/ETHFI) at market price — all four are explicitly labeled "no fresh verified catalyst" and are 10-30% extended over 24h.
- What would change the view: a confirmed break of BTC/ETH uptrend structure (flips crypto mood), any de-escalation or escalation headline out of the Strait of Hormuz situation (moves the macro-risk score off 100/100), or the first 15-30 minutes of RTH price action for the stocks C-tier watchlist names.

## 7. Candidate Deep Dives

### 7.1 NEAR/USDT — LONG (crypto swing, catalyst-backed, active)

- Status: **OPEN actionable / triggered.** Signal `sig_844ebda1635aaf1d`, entry 1.9948-2.0129, invalidation 1.9727, score 67.4, expires 2026-08-30T21:22:56.
- Catalyst: importance-0.80 regulatory/partnership headline — "Banks and regulators join quantum-resistant crypto transfer pilot on NEAR testnet" (CryptoBriefing, fresh <1h) — basket-confirmed as `ai_narrative` primary alongside RENDER/TAO/FET.
- Has price already reacted? Partially — NEAR is an active RS-leader within its basket, not a fresh breakout; the catalyst is fresh but the position was likely entered before this specific headline printed.
- Chasing? No — this is an already-filled swing entry, not a chase.
- Retest/pullback structure? Yes, within the swing playbook's normal pullback framework.
- Overextended (>2 ATR from EMA20)? Not flagged in today's reports.
- Would entry now be late? For a fresh entry, moderately — prefer waiting for the desk's stated pullback zone rather than market-buying.
- Aligned with market mood? Yes — RS-leader long in a technically risk-on crypto tape.
- Long/short/wait-for-trigger? Long, already actionable.
- Actionable now or after confirmation? Already actionable (triggered).
- Invalidation: 1h close beyond 1.9727 per swing playbook convention.
- Chase-risk setup? Low — catalyst supports the existing position rather than being the entry trigger.
- Catalyst confirmation or contradiction? Confirmation (partnership/regulatory headline consistent with the AI-narrative RS-leadership thesis).

### 7.2 ETH/USDT — LONG (crypto, catalyst risk vs. open position)

- Status: **OPEN actionable / triggered.** Active ETH signal: `sig_3cf3360220e568b9`, swing, entry 2437.85-2448.37, invalidation 2425.00, score 67.8, expires 2026-08-31T05:21:10.
- Catalyst: **highest-importance event today (0.86)** — Term Finance DeFi lending protocol lost an estimated $8.5M to a governance exploit (Cointelegraph). This is an ecosystem exploit_hack tag, not a direct ETH protocol failure, but it sits inside the ETH DeFi risk surface.
- Also flagged: "fresh catalyst exists but risk events require caution" — geopolitical_risk (Coinbase/ETH-holdings pushback narrative) and Bitcoin Core encrypted-routing debate (BTC-adjacent, spills into general crypto risk sentiment).
- Has price already reacted? Not clearly separable from the broader uptrend in today's data.
- Chasing? No — existing swing position.
- Overextended? Not flagged.
- Aligned with market mood? Yes directionally (uptrend), but the exploit headline is a genuine counter-thesis risk that a pure technical read would miss.
- Actionable now or after confirmation? Existing position stays open; **no fresh ETH long entry recommended** until the Term Finance exploit's ecosystem impact (contagion, other protocols) is clearer.
- Would invalidate: 1h close beyond 2425.00, or evidence the exploit has broader DeFi-on-ETH contagion.
- Catalyst confirmation or contradiction? **Contradiction** — a risk headline sits alongside an active long; not disqualifying but worth the extra caution flag.

### 7.3 SMCI — Legal/headline risk contradiction (stocks, no live signal — market closed)

- Status: watchlist/not actionable (market-closed gate); was A-tier (score 85) before demotion.
- Internal flag: "active legal/headline risk (indictment) — manual review required."
- External verification ([Supermicro Provides Update on Investigation by Independent Board Directors](https://ir.supermicro.com/news/news-details/2026/Supermicro-Provides-Update-on-Investigation-by-Independent-Board-Directors/default.aspx), Supermicro IR, 2026-08-20): the underlying March-2026 indictment named three individuals (a former SVP/board member, a Taiwan sales manager, and a contractor) — **Supermicro itself was not indicted**. The independent board-led investigation concluded on 2026-08-20 and **cleared current senior management of wrongdoing**, confirming no direct illegal sales occurred. Corroborated by [StockTitan's coverage of the related 8-K](https://www.stocktitan.net/sec-filings/SMCI/8-k-super-micro-computer-inc-reports-material-event-9d00fa321743.html).
- Legal/headline risk final verdict per §I: **MANUAL REVIEW REQUIRED** (not a clean AVOID, not a clean actionable) — the internal flag and the external resolution are in tension, and reconciling which one the scoring system should trust is a human decision, not this review's to make.
- Not actionable regardless today (market closed).

### 7.4 PENGU/USDT — LONG (crypto swing, best-performing playbook, no catalyst)

- Status: **WAITING for entry.** Signal `sig_231db3f23db57656`, entry 0.009178-0.009357, invalidation 0.008959, score 72.4, expires 2026-08-31T04:09:54.
- Playbook: `crypto_swing_narrative_rs_momentum` — 14d WR 72% / PF 5.80 / +24R, the desk's single best-performing cohort right now.
- RS vs BTC: +16.0%. 24h return +16.55% to +17.52% (varies by report snapshot), 7d +57.82% to +59.89% — **already extended**.
- Catalyst/news: explicitly "no fresh verified catalyst detected" in both intraday and swing reports.
- Would entry now be late? Yes for a market order — the desk's own plan is a pullback entry into 0.0092-0.0094, not chasing spot.
- Chase-risk setup? Yes if entered at market; the playbook's known failure mode is exactly "chase risk after a vertical 24h move."
- Aligned with market mood? Yes (RS-leader long in a risk-on tape), but this is the pure-momentum sub-cohort, not the catalyst-backed one the playbook notes as "cleanest."
- Invalidates on: 1h close beyond 0.0090.

### 7.5 SPK/USDT — LONG (crypto, top momentum score, playbook-flagged risk)

- Status: mixed across timeframes — intraday `tp1_hit` (already partially won), swing `triggered` and a separate swing `waiting_for_entry`.
- Score: highest momentum score of the cycle (91.6/100), 24h +30.19%, RS vs BTC +28.67%, part of the `momentum_breakout` narrative basket (SPK/PROM/TUT primary) — but that basket is explicitly labeled **"pure momentum cluster... without confirmed news catalyst."**
- Intraday playbook carries its own warning: "No-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation" (14d cut: WR 23% / PF 0.70 / −3R for that specific no-catalyst intraday cohort).
- Derivatives: price up + OI up (fresh positioning confirms trend), funding neutral, crowding normal — no squeeze red flag.
- Would entry now be late? Yes for a fresh position — 30%/24h is a chase at market; desk plan is pullback into 0.0215-0.0222 (intraday) / 0.0201-0.0208 (swing).
- Catalyst confirmation or contradiction? No catalyst — pure technical momentum. Treat as a lower-conviction, no-catalyst long relative to NEAR.

## 8. Best Candidates Ranked

1. **NEAR/USDT** — LONG, catalyst-backed, RS-leader, already actionable. Best overall candidate this cycle.
2. **PENGU/USDT** — LONG-WATCH, best-performing playbook cohort, but wait for the 0.0092-0.0094 pullback zone rather than chasing; no catalyst.
3. **ETH/USDT** — HOLD existing long only; do not add fresh exposure until the Term Finance exploit's DeFi-on-ETH contagion risk is clearer.
4. **Short-watch (crypto):** none live. Trigger: a confirmed 1h-close break of BTC/ETH uptrend structure, or a volume-confirmed breakdown in a weakest-symbol name (SNDKB, SKHYB, PUMP, BOME — all currently RS-negative vs BTC).
5. **Short-watch (stocks):** none live (market closed). Trigger: RTH confirmation (first 15-30min) of a failed bounce or a breakdown in a weak sector (utilities XLU, real estate XLRE, industrials XLI); historical stats this week favor shorts (PF 1.30) over longs (PF 0.08) once confirmed.

## 9. Avoid / No Trade

*(This decision window only — never a command to stop scanning, tracking, or the scheduler.)*

- **SMCI** — manual review required due to the stale-flag/investigation-cleared contradiction (§7.3); not actionable today regardless (market closed).
- **Momentum-breakout cluster at market price** (SPK, PROM, TUT, ZAMA, ETHFI) — no verified catalyst, already 10-30% extended over 24h; only actionable at the desk's stated pullback zones, not at spot.
- **Fresh ETH long exposure** — hold existing position, but do not add until the Term Finance exploit's broader contagion risk clarifies.
- **New stocks longs before RTH confirmation** — this week's realized data (PF 0.08) argues against chasing the pre-open C-tier watchlist longs without a confirmed post-open setup.

## 10. Main Risks

- **Macro/geopolitical:** Iran vs. Strait-of-Hormuz sanctions escalation — desk macro-risk score 100/100, six risk-off headline hits today and zero risk-on hits. This is the single biggest tail risk to the crypto risk-on thesis.
- **Catalyst mapping weak (74.6% unmapped)** — reduces confidence in any catalyst-driven read; treat catalyst tags as directional color, not proof.
- **SMCI legal-flag/resolution contradiction** — a system-of-record risk, not a market risk, but it means at least one A-tier-scored name's risk gate may be miscalibrated right now (TODO-3).
- **Crypto scalp mode actively losing** (PF 0.17, totalR -2.5R this week) — a live drag on aggregate performance if scalp signals are still being pushed (TODO-4).
- **Stocks intraday long-side edge has flipped negative** (PF 0.08 vs shorts PF 1.30) — a real directional-bias risk if the system keeps surfacing long-heavy A-tier ideas into a session where longs have been losing (TODO-5).
- **INTU earnings tomorrow (2026-08-25)** — do-not-chase warning already active; NVDA/CRM/CRWD also report within 2-3 sessions (swing-blocked already).

## 11. Action Plan — Next 4 Hours

- Hold existing crypto B-tier longs; do not add fresh no-catalyst exposure (SPK/PENGU/ZAMA/TUT/PROM) at market — wait for stated pullback zones.
- Treat NEAR/USDT as the highest-conviction current long; no action needed, it is already open.
- Watch the Strait-of-Hormuz headline flow — any material escalation should be treated as a reason to tighten invalidations across open crypto longs, not to close them pre-emptively.
- For stocks, build the RTH watchlist from the C-tier list (ABNB, SHOP, TSLA, SNOW, ADBE, CMCSA, PLTR, CRM, UBER, HOOD, MA, SBUX, COP, COIN — excluding SMCI pending reconciliation) but do not treat any of them as confirmed until the first 15-30 minutes of the cash session; lean toward short setups over long chases given this week's realized stats.
- No action on SMCI until a human reconciles the internal flag against the Aug 20 investigation conclusion.

## 12. Final Verdict per Mode

- **Crypto scalp:** AVOID new entries — PF 0.17, totalR -2.5R this week; broken mode, needs human review (TODO-4).
- **Crypto intraday:** SELECTIVE LONGS ONLY — PF 2.49 overall, but prefer catalyst-backed/RS-leader names (NEAR-style) over pure no-catalyst momentum (SPK/PENGU/ZAMA-style) at market price.
- **Crypto swing:** SELECTIVE LONGS, best mode this week (RS-momentum playbook PF 5.80) — NEAR is the standout; PENGU/others fine but wait for pullback.
- **Stocks intraday:** WATCHLIST ONLY until RTH open; once open, lean SHORT-CONFIRMATION over long-chase given this week's PF 0.08 (longs) vs PF 1.30 (shorts) split; SMCI excluded pending manual review.
- **Stocks swing/invest:** deprecated framework — no verdict, not evaluated this run.

## 13. Sources

- [Supermicro Provides Update on Investigation by Independent Board Directors](https://ir.supermicro.com/news/news-details/2026/Supermicro-Provides-Update-on-Investigation-by-Independent-Board-Directors/default.aspx) — Supermicro Investor Relations, 2026-08-20.
- [Indictment hits associates as Supermicro (NASDAQ: SMCI) reshapes board and compliance role](https://www.stocktitan.net/sec-filings/SMCI/8-k-super-micro-computer-inc-reports-material-event-9d00fa321743.html) — StockTitan / 8-K filing, 2026-08-20.
- Internal: `data/reports/intraday/2026-08-24_06-47_intraday_report.md`, `data/reports/swing/2026-08-24_04-10_swing_report.md`, `data/reports/scalp/2026-08-24_06-37_scalp_report.md`, `data/reports/stocks/intraday/2026-08-24_07-21_stocks_intraday_report.md`, `data/catalysts/2026-08-24/catalyst_events.jsonl`, `data/catalysts/2026-08-24/catalyst_cycle_06-53.md`.
- BTC/ETH broader price-action commentary from WebSearch (Yahoo Finance, Coinpedia, Pickaxe) was cross-source-inconsistent on exact price levels/dates — used only as directional color for the risk-on read already supported by internal OHLCV/regime data, not cited as a standalone fact.

## 14. Fix Requests / TODO

### TODO-1: 5-day gap in scheduled-review cadence
- **issue:** No `OPUS_ENRICHED_REVIEW_AUTO_*.md`, `_DEFERRED_*`, or `_BLOCKED_*` file exists between 2026-08-19 16:33 EEST and this run (2026-08-24 12:04 EEST) — roughly 30 missed cycles across the four :30 slots plus the 16:20/23:15 sibling tasks.
- **evidence:** `ls -t OPUS_ENRICHED_REVIEW_AUTO_*.md` and `OPUS_ENRICHED_REVIEW_DEFERRED_*.md` / `_BLOCKED_*.md` in the project root — most recent entries before this run are all dated 2026-08-19 or earlier.
- **suggested manual fix:** check the Windows Task Scheduler / `scheduled-tasks` registration for `opus-enriched-review-4h`, `opus-enriched-review-preus`, and `opus-enriched-review-postclose` — confirm they are still enabled and firing.
- **priority:** high
- **first observed:** 2026-08-24 12:04 EEST

### TODO-2: Catalyst mapping stuck at ~75-80% unmapped across multiple runs
- **issue:** Unmapped catalyst-event rate was 79.8% on 2026-08-19 and is 74.6% today — a persistent, not one-off, symbol-resolution gap (echoes the known issue in [[project_crypto_ai_desk_catalyst_linkage]]).
- **evidence:** this run: 746/1000 unmapped; prior review (`OPUS_ENRICHED_REVIEW_AUTO_2026-08-19_1630.md` §5): 79.8% unmapped.
- **suggested manual fix:** improve the symbol resolver in the catalyst layer (macro/regulatory/legal headlines without a ticker mention are a large share of the unmapped set — consider a macro/no-symbol bucket instead of trying to force-map them).
- **priority:** medium
- **first observed:** 2026-08-24 12:04 EEST (recurring, first noted 2026-08-19 or earlier)

### TODO-3: SMCI legal/headline-risk flag appears stale vs. resolved investigation
- **issue:** Production risk gate still surfaces SMCI as "active legal/headline risk (indictment) — manual review required," but the underlying independent board investigation concluded 2026-08-20 (4 days before this run) and cleared current senior management; Supermicro itself was never indicted (only 3 individuals, none currently with the company in a decision-making role).
- **evidence:** internal: `data/reports/stocks/intraday/2026-08-24_07-21_stocks_intraday_report.md` line ~462 ("SMCI ... active legal/headline risk (indictment) — manual review required"); external: [Supermicro IR update](https://ir.supermicro.com/news/news-details/2026/Supermicro-Provides-Update-on-Investigation-by-Independent-Board-Directors/default.aspx), 2026-08-20.
- **suggested manual fix:** review the SMCI legal-risk record/flag source and refresh it against the Aug-20 resolution, or add an explicit "investigation concluded, management cleared" annotation so future runs don't treat this as an open indictment against the company.
- **priority:** medium
- **first observed:** 2026-08-24 12:04 EEST

### TODO-4: Crypto scalp mode profit factor collapsed
- **issue:** `signal-stats --asset-class crypto` shows scalp mode at PF 0.17, totalR -2.5, 0 wins / 3 losses over the trailing week (n=91, confidence=stronger) — a clearly broken cohort relative to intraday (PF 2.49) and swing (PF 1.80).
- **evidence:** `python -m src.cli signal-stats --asset-class crypto` → "By mode" table, `mode=scalp` row.
- **suggested manual fix:** review scalp-mode entry criteria/thresholds, or confirm the scalp kill-switch mentioned in the 2026-08-19 review is (or isn't) currently active.
- **priority:** medium
- **first observed:** 2026-08-24 12:04 EEST

### TODO-5: Stocks A/B intraday long-side edge has flipped negative
- **issue:** `signal-stats --asset-class stocks` → by-direction table shows longs at PF 0.083 / totalR -16.5 (n=334) vs shorts at PF 1.30 / totalR +1.5 (n=384) over the trailing week — a large, consistent directional-edge gap, not sampling noise given both sample sizes are >300.
- **evidence:** `python -m src.cli signal-stats --asset-class stocks` → "By direction" table.
- **suggested manual fix:** review whether the stocks intraday long-side scoring/entry logic needs recalibration, or whether this is a regime-appropriate short-bias week that should just be routed around (no code change) — a human call, not this review's to make.
- **priority:** medium
- **first observed:** 2026-08-24 12:04 EEST
