# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:12 EEST

## 1. Executive Summary

**16:20 EEST slot — pre-US-open decision review.** Advisory only — no auto-trade, no code/scoring changes. **Critical framing for this run: today is Saturday 2026-08-08.** There is no US cash session today, and none tomorrow (Sunday) — the next RTH open is **Monday 2026-08-10**. The slot's usual "10 minutes before cash open, final pre-open read" framing does not apply literally today; this run instead functions as a forward-looking planning pass over Friday's (2026-08-07) close data, carried toward Monday's open, plus the mandatory pre-US stocks scoring overlay (which structurally cannot produce a SUPPORT verdict today — see §5).

**Pre-US schedule check:** target 08:55 America/New_York, actual fire 08:59 ET (Δ+4min, within tolerance). No DST-window drift — 2026-08-08 is outside both documented mismatch windows (2026-03-08→03-29, 2026-10-25→11-01).

**Crypto** stays **cautious risk-on**: BTC/ETH both uptrend, altcoin breadth 60.0%/67.5% above EMA20/50 (cooled slightly from 66.7%/74.4% at the 11:45 review). Macro/geopolitical risk score **eased to 86.9/100** (from 100/100 at 11:45) despite a fresh Iran/Strait-of-Hormuz missile attack on a UAE tanker overnight — the desk's own risk-off headline count dropped, and price action (BTC ~$65k, ETH ~$1,900-1,930 per external confirmation) continues to shrug off both the Hormuz tension and the Coldcard hardware-wallet exploit (externally confirmed stable at >$130M, no new escalation this cycle). **No A-tier signals** on either asset class. The standing **ZBT/ACE open-long-vs-bias-short contradiction** persists for a **3rd consecutive review** (now 4 open triggered longs total — ZBT×2, ACE×2): ZBT improved from -23.67% to **-12.45%** 24h, ACE worsened from -19.02% to **-20.91%** 24h — the cluster is rotating in severity, not resolving. **1 untracked legacy alert today** (BICO/USDT, 12:01 UTC) — a recurrence of the standing watchlist-alert-signal-reuse TODO. Catalyst mapping is **47.8% unmapped** (2,418 cumulative events, 1,157 unmapped) — stable/slightly improved vs 48.7% at 11:45, still under the 50% "weak" auto-trigger.

**Stocks Pre-US Review Overlay** (mandatory this slot) ran against 24 code-eligible candidates (of 73 total candidate rows; 49 excluded by the code's own hard gate, mostly `EARNINGS_BLACKOUT`). Because today is a weekend with **zero** premarket/RTH/RVOL/RS data available or even possible, **SUPPORT was structurally unreachable for every candidate** (one of SUPPORT's required legs — fresh market context — cannot exist on a Saturday) — this is a data-availability fact, not a judgment call. Verdicts: **0 SUPPORT / 6 NEUTRAL / 1 CAUTION / 0 BLOCK / 17 INSUFFICIENT_DATA**. See §5 for the full breakdown and enforced (code-clamped) values.

One scheduler step failed this cycle (`paper execution accounting refresh`, 300s timeout) — 2nd consecutive cycle with the same failure; flagged in §3 and §14.

## 2. Data Used

- `data/reports/scalp/2026-08-08_11-54_scalp_report.md` (gen 14:54 EEST) — ~1.3h old, fresh
- `data/reports/intraday/2026-08-08_12-01_intraday_report.md` (gen 15:01 EEST) — ~1.2h old, fresh, freshest this cycle
- `data/reports/swing/2026-08-08_04-00_swing_report.md` (gen 07:00 EEST) — ~9.2h old, carry-forward bucket (4-12h), cross-checked consistent with fresher scalp/intraday
- `data/reports/stocks/intraday/2026-08-07_20-57_stocks_intraday_report.md` (gen Aug 7 23:57 EEST) — market closed Sat/Sun, planning-only, not a data-quality failure
- `data/reports/stocks/swing/*`, `stocks/invest/*` — retired since 2026-07-02 ([[project_crypto_ai_desk_stocks_position_framework]]), excluded by design
- `data/catalysts/2026-08-08/catalyst_events.jsonl` (2,418 events cumulative), `narrative_baskets.jsonl` (6 baskets), `catalyst_cycle_12-07.md` (latest cycle, 15:07 EEST)
- `data/processed/llm_analysis_packet.md` (15:03 EEST), `data/processed/llm_stocks_packet.md` (00:02 EEST, weekend-stale, stocks planning-only anyway)
- `active-signals --asset-class crypto` (50 rows) / `--asset-class stocks` (50 rows, mixed current + historical expiry — standing TODO)
- `signal-stats --asset-class crypto` and `--asset-class stocks`
- `detect_untracked_legacy_alerts --since 2026-08-08` → 1 untracked (BICO/USDT)
- **`python -m src.cli stocks-preus-candidates`** → `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (24 eligible / 49 excluded)
- **`python -m src.cli stocks-preus-review-ingest --json data/raw/enriched_review_sources/preus_review_2026-08-08T130759Z.json`** (see §5 for enforced results)
- `data/scheduled_runs/2026-08-07_default_schedule/cycle_06_14-46_summary.md` (mtime 15:38 EEST) — 57/58 steps `[OK]`, 1 `[FAIL]`
- Direct read-only SQL on `db/crypto_ai_desk.sqlite` (`news_items` 24-48h lookups for ZBT, ACE, and all 19 unique pre-US candidate symbols; `proposed_signals` for ZBT/ACE open-position confirmation)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-08_1145.md` (Europe / pre-US context, 11:45 EEST); prior same-slot review `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_1612.md` (pre-US-open decision review, Friday, real trading day — used only as overlay-behavior baseline, see §4)
- 2 WebSearch queries (BTC/ETH price + macro; stock market week-ahead Aug 10-14) + 1 WebFetch (Yahoo Finance BTC/ETH article, confirmed opens) — CNBC and IG.com week-ahead articles returned HTTP 403 on WebFetch, used as search-snippet-only with `verification_status: unverifiable` (see §13)

External web research **was** available this cycle (partial — 2 of 3 target URLs blocked, snippet-only fallback used and labeled).

## 3. Scheduler / Data Freshness

- **Pre-US schedule check:** target 08:55 ET, actual fire 08:59 ET (Δ+4min, within tolerance, no DST-window flag).
- `data/scheduled_runs/2026-08-07_default_schedule/scheduler.log` — mtime **Aug 8 15:38 EEST** (~34min old at review start) → **fresh**, well under the 3h defer threshold.
- Latest cycle summary `cycle_06_14-46_summary.md` (mtime 15:38 EEST) — **57 OK / 1 FAIL**. The one failure: `paper execution accounting refresh` (exit=-1, 306.7s — hit the 300s subprocess timeout). This is the **2nd consecutive cycle** with the identical failure (`cycle_05_11-54` also failed at 300.3s; `cycle_04_09-07` was OK at 103.2s) — a genuine regression candidate, flagged §14.
- Crypto scalp report: 14:54 EEST → fresh (~1.3h old).
- Crypto intraday report: 15:01 EEST → fresh, freshest this cycle.
- Crypto swing report: 07:00 EEST, ~9.2h old → carry-forward bucket (4-12h); regime read cross-checked against fresher scalp/intraday — consistent (bullish trend, uptrend BTC/ETH both times).
- Stocks intraday report: Aug 7 23:57 EEST, ~16h old → stale relative to now but market is closed (weekend) — planning/watchlist context only, not a data-quality failure.
- Stocks swing/invest: retired since 2026-07-02 — excluded by design.
- Market intelligence health (from cycle_06, step 41): `status: ok`-pattern per source, 0 consecutive_failures across sampled sources.
- Latency: crypto acceptance = **SLA_BREACH** (raw detect p90 6699.1s / 6022.6s > 180s threshold, n113), stocks intraday acceptance = **SLA_BREACH** (fast-source share 12% < 80%, provider yfinance) — both standing under [[project_crypto_ai_desk_latency_layer]], unchanged this cycle.
- Paper portfolio ledger refresh (step 37): `[OK]`, 3,343 scanned/written, 2,916 resolved, 0 errors; 800 deduped actionable paper trades, active fee profile `bybit_non_vip_usdt_perp` net +$5,753.86 (115.08% ret, 25.15% maxDD, 242W/504L/54BE).
- Paper monitor status (step 55, Telegram): Open actionable **34**, Waiting for entry **2**, Entered unresolved **16**, Review/Shadow **29**, No-entry/stale/moved-away **243**, Closed today **156W / 32L / 32flat**, Needs review **5**.
- Monitors: crypto watchlist monitor, crypto pending monitor, MEXC canary monitor, derivatives monitor, fast Finnhub news monitor, telegram dashboard callbacks all `[OK]` / continuous-background this cycle.
- Social source degradation (non-blocking): Reddit Bitcoin/Ethereum/CryptoCurrency social scrape failing with 403 (multiple hits this cycle) — standing, low-priority, does not affect news_items ingestion from primary sources.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-08 16:12 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~34min old, cycle_06 57/58 steps OK, 1 FAIL (paper execution accounting refresh, 2nd consecutive cycle timeout)", "swing report ~9.2h old (carry-forward, cross-checked consistent)", "paper portfolio ledger refresh OK, 0 errors, 3343 scanned"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"], "data_missing": ["stocks premarket data (weekend, structurally unavailable)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC+ETH uptrend, breadth 60.0%/67.5% above EMA20/50 (cooled from 66.7/74.4 at 11:45)", "macro risk score eased to 86.9/100 (from 100/100 at 11:45) despite fresh Iran/Hormuz tanker-attack headlines", "WebSearch confirms BTC ~$65k / ETH ~$1,900-1,930 holding, dovish jobs-report tailwind", "stocks: no session today or tomorrow (weekend) — Monday RTH is the next live data point"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported", "catalyst_confirmed"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 52.2% mapped / 47.8% unmapped (1261/2418 cumulative) — stable/slightly improved vs 48.7% at 11:45", "6 active narrative baskets: perps_dex, delisting_thin_liquidity (BONK), binance_ecosystem_teaser (BNB/ASTER), ai_narrative, rwa_narrative (ONDO/XLM), momentum_breakout (TUT/TST/SYN, fresh <1h)", "ZBT/ACE: 0 fresh (24h) news_items rows each — pure technical/momentum divergence, no catalyst either side", "stocks pre-US overlay: 6 candidates (LMT x2, CRCL, ORCL, MSTR, SHOP) had genuinely fresh entity-resolved catalysts internally, none could reach SUPPORT due to missing weekend market context"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["data_unavailable", "oi_contradicts"], "data_missing": ["OI 24h% n/a for most active symbols this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BICO/USDT negative funding across bybit/okx/mexc despite long-biased report placement, crowding elevated", "DODO/USDT (top intraday idea) negative funding across mexc, crowding elevated", "KAITO/USDT negative funding across all 3 external venues, crowding elevated, bias short and on weakest-symbols list", "no fresh OI-change data for ZBT/ACE this cycle"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest"], "data_missing": ["TradingView / manual chart check unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DODO/USDT is the freshest top intraday idea (score 73.4), waiting_for_entry structure, pullback zone 0.0217-0.0223 vs current 0.0226 — near the zone, not yet chasing", "BICO/USDT remains highest swing score (79.5) but already +46.5%/24h — pullback-only, chase risk if bought at market", "TST/USDT is now the single strongest symbol overall (score 99.1, +24.68%/24h, vol 2.5x) but tagged overextended in the report's own unusual-volume tags"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["paper monitor status: open actionable 34, waiting for entry 2, entered unresolved 16, review/shadow 29, no-entry/stale/moved-away 243, closed today 156W/32L/32flat, needs review 5", "crypto active-signals: 50 rows, 0 A-tier, all B-tier; XRP/USDT short still tp1_hit, unresolved, expires 2026-08-08T18:02 UTC (~5h from this review)", "detect_untracked_legacy_alerts: 1 today (BICO/USDT, 12:01 UTC) — recurrence of standing TODO-3"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": ["correlation_cluster", "reduce_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZBT/USDT (2 open swing longs, confirmed via proposed_signals) and ACE/USDT (2 open swing longs, confirmed) both tagged bias=short with negative 24h in the freshest intraday scan for a 3rd consecutive review — ZBT improved to -12.45%, ACE worsened to -20.91%", "crypto scalp mode still structurally losing (PF 0.14-0.17 across recent windows, standing kill-switch candidate)", "1 untracked legacy alert this cycle (BICO/USDT) — signal-reuse integrity risk, standing TODO"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing mode: PF 5.35 this window, 14W/11L, avgR +0.45 (n=63) — still the working edge", "crypto intraday mode: PF 1.36, 14W/36L, avgR +0.16 (n=79) — moderate, winrate 16% system-flagged 'low'", "crypto scalp mode: PF 0.17, 1W/4L, avgR -0.078 (n=42) — structurally losing", "stocks all-tier: n=448, PF 0.17, avgR -0.23, tier=C triggered winrate 1%, PF 0.22 below 0.8 — known issue per [[project_crypto_ai_desk_stocks_intraday_hardening]]"] },
    { "agent": "head_trader", "verdict": "ok",
      "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents below"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "DODO/USDT", "trigger": "waiting_for_entry, pullback zone 0.0217-0.0223 (current 0.0226, near the zone); score 73.4, top intraday idea this cycle, no chase required if it ticks back into the zone" },
    "best_short_candidate":    { "symbol": "XRP/USDT", "trigger": "already-open swing short (tp1_hit, entry 1.0598-1.0610, invalidation 1.0626, expires 2026-08-08T18:02 UTC — resolves before the next review) — manage existing only, no fresh short setup scored this cycle" },
    "best_catalyst_candidate": { "symbol": "SHOP (stocks, planning-only)", "trigger": "AI-referred-traffic-tripling story is the freshest, most multi-source-converged, most specific catalyst found this cycle (2026-08-08, same-day) — NEUTRAL not SUPPORT because no weekend market context exists; would need Monday premarket + RS-vs-sector confirmation before any actionability" },
    "avoid_candidate":         { "symbol": "ZBT/USDT, ACE/USDT (open swing longs)", "reason": "3rd consecutive review with a bias=short + negative-24h tag on open longs; ZBT improving, ACE worsening — do not add size until resolved by a stop-out or a bias-flip back to long" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | risk_on, longs_preferred, mixed | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.45 | data_unavailable, oi_contradicts | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.75 | open_actionable, waiting_for_entry, review_shadow, no_entry | advisory_only |
| risk_manager | manual_review | 0.60 | correlation_cluster, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-08_1145.md` (Europe / pre-US context, 11:45 EEST):

- **Macro risk score improved materially**: 100/100 → **86.9/100**. Despite a fresh overnight escalation (Iran missile attack on a UAE tanker in the Strait of Hormuz), the desk's own risk-off hit-count dropped (6 risk-off hits now vs. the prior cycle's broader set) — price action continues to outweigh the headline layer.
- **Altcoin breadth cooled slightly**: 66.7%/74.4% (EMA20/50) → **60.0%/67.5%** — still bullish-trend, mildly less broad.
- **ZBT/ACE contradiction persists a 3rd consecutive review, composition intensity rotated**: ZBT **improved** -23.67% → **-12.45%** 24h (still tagged bias=short, still 2 open longs); ACE **worsened** -19.02% → **-20.91%** 24h (still 2 open longs). Neither has stopped out or flipped bias — escalating toward the "3rd consecutive cycle" threshold noted in the standing TODO as a trigger for a priority bump.
- **Untracked legacy alerts: 0 → 1** (BICO/USDT, sent 12:01 UTC, no matching `proposed_signal` within 6h) — the TODO-3 pattern (watchlist re-fire reusing/missing signal linkage) recurred this cycle after being quiet at 11:45.
- **Catalyst mapping**: 48.7% unmapped (730/1500, 3 cycles) → **47.8% unmapped** (1157/2418, 5 cycles cumulative) — flat/slightly improved, still under the 50% threshold.
- **Top crypto idea rotated**: BICO/USDT (79.5, chase-risk, +46.5%/24h) was the 11:45 pick; this cycle's freshest intraday report promotes **DODO/USDT** (73.4, `waiting_for_entry`, price sitting just above its stated pullback zone) — a cleaner, less-extended setup.
- **New this cycle — Stocks Pre-US Review Overlay** (this slot's mandatory addition, not present in the 11:30/11:45 slot): 24 eligible candidates reviewed, 0 SUPPORT (structurally impossible today — see §5), 6 NEUTRAL, 1 CAUTION, 17 INSUFFICIENT_DATA. For contrast, the same overlay on **Friday** (`OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_1612.md`, a real trading day with live premarket data) produced 0 SUPPORT / 1 NEUTRAL / 6 CAUTION / 3 INSUFFICIENT_DATA over 10 candidates with real adjustment clamps applied (e.g. CSCO 85.35→80.35) — today's much higher INSUFFICIENT_DATA share (17/24 vs 3/10) is the direct, expected consequence of the weekend removing the market-context leg entirely, not a quality regression in the review itself.
- **New scheduler regression**: `paper execution accounting refresh` failed for a 2nd consecutive cycle (300s timeout) — was OK as recently as `cycle_04_09-07` (103.2s). Flagged §14.
- **XRP/USDT short still unresolved** (tp1_hit, same as 11:45) — now within ~5h of its 18:02 UTC expiry; should resolve by the next (18:30 US open reaction) review.
- **No new A-tier signals** on either asset class.

## 5. Catalyst Coverage

- Total catalyst events today (cumulative, 5 cycles): **2,418**
- Mapped (non-null symbol): **1,261** (52.2%)
- Unmapped: **1,157** (47.8%)
- Narrative baskets: **6** (perps_dex_narrative, delisting_thin_liquidity, binance_ecosystem_teaser, ai_narrative, rwa_narrative, momentum_breakout)
- Latest single cycle (`catalyst_cycle_12-07.md`, 428 events) by type: other_news 387, legal_risk 20, exploit_hack 7, regulatory_sector_headline 4, partnership 3, earnings_event 3, exchange_delisting 1, product_launch 1, buyback_burn 1, token_unlock 1.
- 47.8% unmapped stays **under** the 50% "weak this run" threshold. Top unmapped headline samples this cycle:
  1. Tradfin geopolitical wire (Ukraine tanker attacks / Black Sea Kazakhstan oil terminal, no symbol resolver hit)
  2. "PNR Investors Have Opportunity to Lead Pentair plc Securities Fraud Lawsuit" (recurring law-firm investor-alert prose-ticker miss pattern, flagged in prior reviews)
  3. "Ant Group's Ling 3.0 Flash packs 124B parameters..." (AI model news, no crypto/stock symbol expected)
  4. "Russia shuts down 9 crypto exchanges in major Moscow crackdown" (regulatory, no single symbol)
  5. "Why Redwire Stock Keeps Gaining" (stock ticker embedded in prose, resolver miss)

### Pre-US Stocks Review Overlay

- Candidates reviewed: **24** signal_ids (19 unique symbols: V, TXN, DELL, LMT, BAC, CSCO, IBM, MCD, CRCL, VRTX, ORCL, MSTR, SHOP, AMGN, SNOW, HD, CRWD, BKNG, CRM) — **SUPPORT 0 / NEUTRAL 6 / CAUTION 1 / BLOCK 0 / INSUFFICIENT_DATA 17**.
- Session-cap-only C's now eligible for pre-open Paper lane review: 24 (all carried a `market_closed_intraday_planning_only` cap reason only, no substantive gate).
- Excluded by hard gate: **49** signal_ids — `EARNINGS_BLACKOUT` (majority: HOOD, TSLA, AMAT, MA, NVO, QCOM, ASML, PEP, MS, BIIB, BA, SMCI, NET, JPM, AMZN, LLY, GILD, KO, DIS, ETN, CMCSA, COP, ABNB, BX, each appearing 1-2x across the two profile passes), `NO_ENTITY_RESOLVED_CATALYST` (KLAC, DXCM, TSM, PYPL), `LEGAL_RISK` (COIN, BLK, INTU, REGN).
- Verdicts (enforced values per the ingest command's own re-verification — see below):
  - **NEUTRAL** (fresh, entity-resolved catalyst confirmed internally; barred from SUPPORT only by missing weekend market context): **LMT** ×2 signal_ids (Pentagon "Golden Dome" space-defense funding, Finnhub, 2026-08-07 18:01 UTC), **CRCL** (Q2 earnings/guidance lift + Arc token presale, Finnhub, 2026-08-07 07:10 UTC), **ORCL** (post-close rally headline, Finnhub, 2026-08-07 21:30 UTC), **MSTR** (BTC-proxy strength/Saylor commentary, Finnhub, 2026-08-07 22:30 UTC), **SHOP** (AI-referred-traffic-tripling, multi-source-converging Finnhub+CryptoBriefing+Motley Fool, 2026-08-08 10:34 UTC — same-day, the freshest and most specific of the six).
  - **CAUTION**: **CRM** (Salesforce 4th layoff round in <1yr, Finnhub+CryptoBriefing, 2026-08-07 19:15-19:21 UTC — genuine negative narrative for a long-pullback setup, not a hard legal/earnings block).
  - **INSUFFICIENT_DATA** (17 signal_ids): V×2, TXN×2, DELL×2, BAC×2, CSCO, IBM, MCD, VRTX, AMGN, SNOW, HD, CRWD, BKNG — internal 48h `news_items` scan found only generic/sector-adjacent chatter or speculative opinion pieces (e.g. HD's leadership-overhaul piece was opinion/speculative, not a confirmed hard event — deliberately not inflated to NEUTRAL), combined with the structural weekend market-context gap.
- Ingested via `stocks-preus-review-ingest --json data/raw/enriched_review_sources/preus_review_2026-08-08T130759Z.json`. **Enforcement confirmed (post-hoc, after a ~16min background delay caused by SQLite write contention from ~19 concurrent scheduler/monitor processes — see resolved §14 TODO):** direct SQL against `stocks_preus_review` (`review_cycle='preus'`, all 24 rows timestamped 2026-08-08T13:09-13:21 UTC) confirms **all 24 items landed with `status: OK` and zero clamping** — every enforced `review_verdict` / `review_score_adjustment` matches exactly what I requested (CRM: CAUTION, -4.0, 100.0→96.0; all 6 NEUTRAL rows: 0.0 adjustment; all 17 INSUFFICIENT_DATA rows: 0.0 adjustment). Note `review_tier` in this audit table is a pure `tier_from_score(adjusted_score)` recompute (e.g. shows "A" for several rows) — this is **not** the live signal tier; the underlying `proposed_signals.tier` stays C for all of them (the `market_closed_intraday_planning_only` session cap from `stocks-preus-candidates` is untouched by this overlay, exactly as designed — no promotion to actionable A-tier occurred or was possible without the separate, unauthorized `stocks-preus-actionability-refresh` step).

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **cautious risk-on** — BTC/ETH uptrend, breadth 60.0%/67.5% above EMA20/50, macro risk-off overlay eased to 86.9/100 (from 100/100) even after a fresh Hormuz-tanker-attack headline; technical + external price action continues to outweigh the headline risk.
- Stocks mood: **closed (weekend)** — no session today or tomorrow; all stock signals are Monday-planning context only. The pre-US overlay found a handful of genuinely fresh, entity-resolved stock catalysts (LMT, CRCL, ORCL, MSTR, SHOP) worth carrying into Monday's premarket check, but none are actionable until real RTH/premarket data exists.
- Dominant narrative: RWA/tokenization (ONDO/XLM) remains the most durable multi-week basket; momentum_breakout (TUT/TST/SYN, fresh <1h, no verified catalyst) is the freshest and most extreme (TUT +67.4%/24h).
- Preferred side now: **longs, selective** — DODO/USDT is the cleanest non-extended setup this cycle; avoid chasing the 24-67% 24h movers already triggered (TST, TUT, SYN, BICO, MMT).
- Best long candidate: **DODO/USDT** (score 73.4, `waiting_for_entry`, pullback zone 0.0217-0.0223 vs current 0.0226 — close to the zone, not a chase).
- Best short candidate: **XRP/USDT** — only open short in the book (tp1_hit, invalidation 1.0626, expires today 18:02 UTC); manage existing, no fresh short setup scored this cycle.
- Best catalyst-backed candidate: **SHOP** (stocks, planning-only) — freshest, most specific, most multi-source-converged catalyst of the cycle (AI-traffic data beating the bear thesis), but NEUTRAL not actionable until Monday premarket confirms.
- What to avoid: adding size to **ZBT/USDT and ACE/USDT** open longs (3rd consecutive review with a bias=short + negative-24h tag); chasing any of TST/TUT/SYN/BICO/MMT at current extended levels; treating any stock signal as actionable before Monday RTH.
- What would change the view: a confirmed BTC breakdown below its current uptrend structure, a material escalation of either the Hormuz tanker conflict or the Coldcard-exploit contagion beyond self-custody, or ZBT/ACE breaking their swing invalidation levels (would convert the contradiction into a clean stop-out).

## 7. Candidate Deep Dives

### 1. ZBT/USDT — open swing longs vs. fresh short-bias tag (contradiction risk, manual review, 3rd consecutive review)
- Status: 2 open swing longs, both `triggered` and confirmed live via direct `proposed_signals` SQL (`sig_0be20040e229aec5` entry 0.1407-0.1491/inval 0.1253/exp 2026-08-14; `sig_66ffd2ccca900b8f` entry 0.1573-0.1626/inval 0.1510/exp 2026-08-13).
- Has price already reacted to a catalyst? No — 0 fresh (24h) `news_items` rows for ZBT this cycle (re-verified). Pure technical divergence.
- Aligned with market mood? No — mood is cautious risk-on/longs-preferred, but ZBT is tagged bias=short with -12.45% 24h (improved from -23.67% at 11:45, but still negative and still tagged).
- Actionable now or wait? Do not add size. Watch for a break of the swing invalidation (0.1253 / 0.1510), which would resolve the contradiction into a clean stop-out, or a bias flip back to long.
- What invalidates: a confirmed close below 0.1253 (first entry's invalidation) triggers a stop.
- Catalyst confirmation/contradiction: no catalyst either way — pure technical.

### 2. ACE/USDT — open swing longs vs. fresh short-bias tag (contradiction risk, manual review, worsening)
- Status: 2 open swing longs, confirmed live (`sig_9d70822c7254b39f` score 79.3, entry 0.1204-0.1284/inval 0.1106/exp 2026-08-14; `sig_cdf7e02cf2a4274c` score 68.5, entry 0.0977-0.1017/inval 0.0928/exp 2026-08-13).
- Has price already reacted to a catalyst? No — 0 fresh (24h) `news_items` rows for ACE this cycle.
- Aligned with market mood? No — ACE's bias=short tag **worsened** this cycle (-19.02% → -20.91% 24h), the opposite direction from ZBT's improvement — the cluster is not resolving as a unit.
- Actionable now or wait? Manual-review hold only; do not add size.
- What invalidates: a confirmed close below 0.1106 (first entry) or 0.0928 (second) triggers a stop.
- Catalyst confirmation/contradiction: no catalyst either way — pure technical, and per the 11:45 review the intraday report's own deep-setup table has previously shown ACE scored both long and short simultaneously in the same report (internally conflicted signal, not just vs. the open position).

### 3. DODO/USDT — best long candidate this cycle (clean, non-extended)
- Status: top-scoring active intraday idea (score 73.4, `crypto_intraday_catalyst_or_momentum` playbook, status `actionable`, `waiting_for_entry` structure).
- Has price already reacted? Partially — +12.74%/24h, +26.81%/7d, but current price (0.0226) sits just above the stated pullback entry zone (0.0217-0.0223), not deep into an extended chase like BICO/TST/TUT.
- Is the setup chasing? No — the desk's own entry plan explicitly requires a pullback into 0.0217-0.0223; do not market-buy at 0.0226.
- Retest/pullback structure? Yes — this is the defining feature of the idea.
- Overextended? Support 0.0187 / resistance 0.0260 vs current 0.0226 — mid-range, not stretched.
- Aligned with market mood? Yes — RS-leader long (RS vs BTC +12.84%) in a bullish-trend tape.
- Actionable now or after confirmation? Wait for the 0.0217-0.0223 zone with volume confirmation.
- What invalidates: 1h close beyond 0.0209.
- Chase risk: low (mitigated by the waiting_for_entry structure), unlike BICO/TST/TUT this cycle.
- Catalyst confirmation/contradiction: none detected — pure technical/RS thesis; known failure-mode warning applies (no-catalyst intraday in chop is net-negative per the 14d cut, WR 23%/PF 0.70/-3R) — treat as low-confidence per the playbook's own labeling.
- Derivatives: negative funding across mexc, crowding unknown — mild caution flag, not disqualifying.

### 4. XRP/USDT — only open short in the book (manage existing, resolves before next review)
- Status: 1 open swing short, `tp1_hit` (`sig_c1e2871dd5fcaf1a`, entry 1.0598-1.0610, invalidation 1.0626, expires **2026-08-08T18:02 UTC** — ~5h from this review, weekend-mode flagged).
- Has price already reacted? Partially — TP1 already hit, partial win in progress.
- Actionable now or wait? Manage existing only; **this will resolve before the 18:30 US-open-reaction review** — confirm win/loss/no-further-TP outcome next cycle.
- What invalidates: a confirmed break back above 1.0626.
- Catalyst confirmation/contradiction: no XRP-specific catalyst found in the last 24h.

### 5. SHOP (stocks, pre-US overlay) — best catalyst-backed candidate, planning-only
- Status: C-tier (session-cap `market_closed_intraday_planning_only`), pre_gate_tier A, base_score 95.03, `stocks_intraday_pullback_vwap_paper_v1` profile, `sig_1bc97d18b76a486c`.
- Has price already reacted to a catalyst? Yes, per external/internal convergence — "Shopify Was Supposed to Be an AI Casualty. Its AI-Referred Traffic Just Tripled." (Finnhub, CryptoBriefing, and Motley Fool all carried variants of this story 2026-08-08 06:14-10:34 UTC, same day) — a specific, data-backed, multi-source-converging positive catalyst directly rebutting a prior bear thesis.
- Is the setup chasing? Cannot be assessed — no premarket price/volume data exists today (weekend).
- Aligned with market mood? Directionally plausible (positive, entity-specific, fresh) but **not confirmable** — no SPY/QQQ/sector RS data possible until Monday.
- Actionable now or after confirmation? Not actionable — requires Monday premarket + RTH confirmation (per the base slot rule: never chase premarket moves without RTH confirmation, and today there isn't even a premarket to chase).
- What invalidates: contradicting Monday premarket/RTH price action, or the AI-traffic story failing to hold up under scrutiny.
- Legal/headline/earnings check: none found — no SEC/DOJ/legal/going-concern flags on SHOP this cycle.
- Catalyst confirmation/contradiction: confirmed internally by 3 converging sources, verdict NEUTRAL (not SUPPORT) purely because of the missing market-context leg, not because the catalyst itself is weak.

## 8. Best Candidates Ranked

1. **DODO/USDT (long-watch)** — wait for the 0.0217-0.0223 pullback zone with volume confirmation; cleanest non-extended setup this cycle, top intraday score (73.4).
2. **SHOP (stocks, catalyst-watch, planning-only)** — freshest, most specific, multi-source-converging catalyst (AI-traffic beat); requires Monday premarket + RTH + RS-vs-sector confirmation before any actionability.
3. **XRP/USDT (short — manage existing)** — only open short in the book, tp1_hit, resolves by 18:02 UTC today (before the next review).
4. **ZBT/USDT & ACE/USDT (manual review, avoid new size)** — 3rd consecutive review with the contradiction; ZBT improving, ACE worsening, watch invalidation levels.
5. Other pre-US NEUTRAL candidates not deep-dived (LMT ×2 — Pentagon Golden Dome funding; CRCL — Q2 guidance lift; ORCL — post-close rally; MSTR — BTC-proxy strength) — all genuine fresh catalysts, all equally blocked from actionability by the weekend market-context gap; worth a first look Monday premarket alongside SHOP.
6. Excess crypto B-tier ideas not deep-dived: BICO/USDT (79.5 swing / already +46.5%/24h, chase-risk-flagged, same caution as 11:45), TST/USDT (99.1 momentum score / +24.68%/24h, tagged overextended by the report itself), MMT/USDT, EPIC/USDT, HEI/USDT — all long-only, chase-risk-flagged, none displacing the candidates above.

## 9. Avoid / No Trade

This applies to the **current decision window only** — scanning, tracking, and monitoring continue uninterrupted regardless.

- **Do not add size to ZBT/USDT or ACE/USDT** open longs while the bias=short + negative-24h contradiction persists (3rd consecutive review, §7.1-7.2).
- **Do not chase** TST/TUT/SYN/BICO/MMT at current extended prices (24-67% 24h already realized) — wait for stated pullback zones, or skip.
- **Do not treat any stock signal as actionable this weekend** — market closed until Monday RTH; all `active-signals --asset-class stocks` rows and all 24 pre-US overlay candidates (even the 6 NEUTRAL ones with genuine fresh catalysts) are planning-only until real premarket/RTH data exists.
- **Do not add new scalp-mode risk** — structurally losing (PF 0.14-0.17 across recent windows, 1W/7L over 14d in the freshest report); standing kill-switch candidate.
- **CRM** carries a genuine negative narrative flag (4th layoff round in <1yr) on top of its already-planning-only status — treat with extra caution even after Monday RTH confirmation, not just the standard weekend caveat.

## 10. Main Risks

- **Geopolitical risk (Hormuz)**: fresh missile attack on a UAE tanker overnight — macro risk score eased to 86.9/100 but this is a live, escalating conflict; a material escalation (e.g. a confirmed strait closure) would flip the risk-off overlay from "headline pressure" to "market-moving."
- **Contradiction-cluster risk**: ZBT/ACE open longs vs. bias=short tags, now a 3rd consecutive review — if this resolves via reversal rather than stop-out, it represents unrecognized directional risk that has now persisted across 3 review cycles without either resolving or escalating enough to force action.
- **Chase risk**: TST (+24.68%), TUT (+67.45%), SYN (+24.27%), BICO (+46.5%), MMT (+37.1%) are all already deep into their 24h moves; entries above stated pullback zones carry materially worse RR than reported.
- **Data-integrity risk**: 1 untracked legacy alert today (BICO/USDT) — the standing watchlist-alert-signal-reuse pattern (TODO-3) recurred after being quiet at 11:45; `active-signals --asset-class stocks` still mixes current and month-old-expired rows under the same "active" status.
- **Scheduler regression risk**: `paper execution accounting refresh` has now timed out (300s) for 2 consecutive cycles — was fine 3 cycles ago (103.2s); worth root-causing before it becomes chronic.
- **Standing latency risk**: crypto and stocks intraday both SLA_BREACH — general live promotion stays blocked (known, not new).
- **Weekend data-gap risk (this slot specifically)**: the pre-US overlay's normal function (catching pre-open gap risk, legal/headline surprises, RTH confirmation gating) is structurally degraded today because there is no premarket session to review — the 6 NEUTRAL catalysts found here should be re-checked fresh Monday morning, not assumed to still hold.

## 11. Action Plan — next 4 hours

- Watch DODO/USDT for a pullback into 0.0217-0.0223; do not chase at 0.0226.
- Watch ZBT/USDT (0.1253 / 0.1510) and ACE/USDT (0.1106 / 0.0928) invalidation levels — a break resolves the contradiction into a clean stop-out; a bias flip back to long would validate the holds.
- Watch XRP/USDT into its 18:02 UTC expiry (~5h away) — confirm resolution by the next (18:30 US-open-reaction) review; note this slot is also nominally mistimed today since there is no real US open on a Saturday — treat that review similarly as a planning/carry-forward pass.
- No stock action possible before Monday RTH; re-run the pre-US catalyst check fresh Monday morning for LMT, CRCL, ORCL, MSTR, SHOP (and CRM's caution flag) rather than reusing today's snapshot, since premarket conditions can change materially over a weekend.
- Continue monitoring the Hormuz tanker-attack thread and the Coldcard exploit thread for any material escalation that would flip the risk-off overlay from headline-pressure to market-moving.
- Confirm the `stocks-preus-review-ingest` enforced values (pending at review time, see §5) once the background process completes, and cross-check against the requested verdicts recorded here.

## 12. Final Verdict per Mode

- **Crypto scalp**: caution / near-avoid — structurally losing (PF 0.14-0.17, 1W/7L over 14d in the freshest report); no new scalp risk recommended.
- **Crypto intraday**: caution — moderate edge (PF 1.36) but most active ideas are no-catalyst chase-risk longs already extended; DODO/USDT is the one clean non-extended exception this cycle.
- **Crypto swing**: watch/selective-long — still the working edge (PF 5.35); DODO is intraday but structurally similar to swing's pullback discipline; ZBT/ACE need manual review before any further action.
- **Stocks (all modes)**: closed / planning-only through the weekend — the pre-US overlay surfaced 6 genuine fresh catalysts (LMT, CRCL, ORCL, MSTR, SHOP ×2 signal_ids) worth a fresh look Monday premarket, but nothing is actionable until real RTH/premarket data exists; C-tier remains never-actionable regardless of day per [[project_crypto_ai_desk_stocks_intraday_hardening]].

## 13. Sources

- [Bitcoin and ethereum prices today, Friday, August 7, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-august-7-2026-crypto-prices-moving-higher-following-july-jobs-report-131451960.html) — Yahoo Finance, 2026-08-07 15:14 (WebFetch-verified, opens)
- Stock market outlook for the week of Aug 10-14, 2026 — CNBC ("Stock market next week: Outlook for Aug. 10-14, 2026", cnbc.com/2026/08/07/...) — **search-snippet only, WebFetch returned HTTP 403**, `verification_status: unverifiable`; snippet indicates bullish sentiment (S&P/Dow record highs, Nasdaq 100 +10% from last week's low) and flags Wed CPI (July) as the key risk event
- Week ahead Aug 10, 2026 — IG.com (ig.com/ae/news-and-trade-ideas/week-ahead-august-10th-2026-260807) — **search-snippet only, WebFetch returned HTTP 403**, `verification_status: unverifiable`
- Internal: `data/reports/scalp/2026-08-08_11-54_scalp_report.md`, `data/reports/intraday/2026-08-08_12-01_intraday_report.md`, `data/reports/swing/2026-08-08_04-00_swing_report.md`, `data/catalysts/2026-08-08/catalyst_cycle_12-07.md`, `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`
- Internal (pre-US overlay catalyst evidence, all `verification_status: primary_source` via Finnhub company-news feed unless noted): LMT — Pentagon Golden Dome funding (Finnhub, 2026-08-07 18:01 UTC); CRCL — Q2 earnings/Arc presale (Finnhub, 2026-08-07 07:10 UTC); ORCL — rally headline (Finnhub, 2026-08-07 21:30 UTC); MSTR — Saylor/BTC-proxy commentary (Finnhub, 2026-08-07 22:30 UTC); SHOP — AI-traffic tripling (Finnhub + CryptoBriefing + Motley Fool, converging, 2026-08-08 06:14-10:34 UTC); CRM — 4th layoff round (Finnhub + CryptoBriefing, 2026-08-07 19:15-19:21 UTC)

## 14. Fix Requests / TODO

### TODO-zbt-ace-contradiction
- **issue:** Open long swing signals on ZBT/USDT (×2) and ACE/USDT (×2) are simultaneously tagged `bias=short` with negative 24h returns for a **3rd consecutive review cycle**. Composition is stable (no longer rotating symbols) but severity is diverging: ZBT improving (-23.67%→-12.45%), ACE worsening (-19.02%→-20.91%).
- **evidence:** `active-signals --asset-class crypto` + direct `proposed_signals` SQL rows `sig_0be20040e229aec5`, `sig_66ffd2ccca900b8f` (ZBT), `sig_9d70822c7254b39f`, `sig_cdf7e02cf2a4274c` (ACE); `data/reports/intraday/2026-08-08_12-01_intraday_report.md` §2 "Weakest Symbols".
- **suggested manual fix:** Investigate whether the bias-tagging logic and the open-signal-hold logic read from different lookback windows; consider an automatic manual-review flag on open positions when a bias flip occurs against them, especially once a 3-cycle threshold is crossed.
- **priority:** **escalated to high** (per the 04:39 review's own escalation criterion: "3rd consecutive cycle recurs with the same or an expanding symbol set" — symbol set is now stable at 2, not expanding, but the 3-cycle persistence threshold itself has been crossed).
- **first observed:** 2026-08-08 04:39 EEST (3-symbol cluster: ZBT/STG/SYN); confirmed 11:45 (2-symbol: ZBT/ACE); confirmed again this run (still ZBT/ACE, 3rd consecutive cycle).

### TODO-paper-execution-accounting-refresh-timeout
- **issue:** Scheduler step `paper execution accounting refresh` has now timed out at the 300s subprocess limit for **2 consecutive cycles** (`cycle_05_11-54`: 300.3s FAIL; `cycle_06_14-46`: 306.7s FAIL) — was OK 3 cycles ago (`cycle_04_09-07`: 103.2s, ~3x faster).
- **evidence:** `data/scheduled_runs/2026-08-07_default_schedule/cycle_06_14-46_summary.md` §24, `cycle_05_11-54_summary.md` §24.
- **suggested manual fix:** Investigate whether the underlying query/dataset this step scans has grown (e.g. paper ledger row count) to the point of needing an index, a batching change, or a raised timeout; confirm whether the paper portfolio ledger refresh (step 37, which ran fine at 88s) is doing overlapping work that could be deduplicated.
- **priority:** medium (escalate to high if a 3rd consecutive cycle fails).
- **first observed:** 2026-08-08 (11:54 cycle); confirmed recurring this run (14:46 cycle).

### TODO-untracked-alert-recurrence
- **issue:** `detect_untracked_legacy_alerts` found 1 untracked alert this cycle (BICO/USDT, sent 2026-08-08T12:01:41 UTC, no matching `proposed_signal` within 6h) — recurrence of the standing watchlist-alert-signal-reuse bug after a quiet reading at 11:45.
- **evidence:** `scripts.detect_untracked_legacy_alerts --since 2026-08-08` output this run.
- **suggested manual fix:** per the existing standing TODO ([[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]) — investigate whether the watchlist re-fire path is reusing a stale/closed signal_id instead of minting a new `proposed_signal` for BICO/USDT specifically.
- **priority:** high (already raised to high 2026-07-17 per memory; this is a fresh recurrence, not a new issue).
- **first observed:** 2026-07-17 (standing); this specific recurrence 2026-08-08 12:01 UTC.

### TODO-stocks-preus-ingest-slow-confirmed-resolved
- **issue:** `stocks-preus-review-ingest --json ...` (24 items) took **~16 minutes** to complete in the background (each item's DB write spaced ~20-55s apart per `stocks_preus_review.reviewed_at` timestamps, 13:09:49→13:21:28 UTC) — far slower than the ~1s/item expected for a simple upsert, consistent with heavy SQLite write contention from ~19 concurrent scheduler/monitor `python.exe` processes observed via `tasklist` at the time.
- **evidence:** background task output empty for >15 minutes during the run; post-hoc `tasklist` showed ~19 concurrent `python.exe` processes; post-hoc SQL against `stocks_preus_review` confirms all 24 rows eventually landed correctly with `status: OK` and zero clamping, matching every requested verdict exactly — **no data-integrity issue, only a latency issue**.
- **suggested manual fix:** consider whether idempotent single-row UPSERT commands like this one should get lock-retry/backoff, or whether this specific overlay's ingest should run with `PRAGMA busy_timeout` raised, given ~19 concurrent scheduler processes are typically active at this slot's fire time (15:55 local cron, mid-cycle for the 2h default schedule).
- **priority:** low (confirmed no live-execution or data-integrity impact — all verdicts landed exactly as requested, zero clamps; the only cost was this run's own wall-clock time).
- **first observed:** 2026-08-08 16:12 EEST (this run); resolved/confirmed by 16:35 EEST same run via background-task completion notification.

### TODO-stocks-active-signals-stale-expiry
- **issue:** `active-signals --asset-class stocks` still returns rows with `expires_at` months in the past alongside genuinely current rows, making the command's "active" framing misleading for operator review — unchanged since first flagged.
- **evidence:** this run's CLI output (e.g. rows carrying 2026-07-xx expiry alongside 2026-08-08 rows).
- **suggested manual fix:** add an `expires_at >= now` filter by default, or an explicit `--include-expired` flag.
- **priority:** low/medium.
- **first observed:** 2026-08-08 11:45 EEST; unresolved, recurring.
