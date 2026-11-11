---
REVIEW: OPUS ENRICHED REVIEW — ⚠ ADVISORY ONLY — NO EXECUTION
SLOT: pre-US-open decision review · 2026-07-07 · 16:20 EEST
WRITTEN: 2026-07-07 16:20 EEST
PREV REVIEW: 2026-07-07 11:39 EEST (Europe / pre-US context)
STATUS: AUTOMATED SCHEDULED RUN — NO HUMAN IN SESSION
---

# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

## 1. Executive Summary

**Slot: pre-US-open decision review — advisory only / no auto-trade. US cash open in ~10 minutes (09:30 ET / 16:30 EEST).**

BTC $63,099 (+2.25%), ETH $1,769 (+1.51%) — crypto regime firmly risk-on, uptrend intact. Monday BTC/ETH ETF inflows were strong ($265.7M BTC, $20.7M ETH), though note 8 consecutive weeks of net weekly outflows — institutional base remains cautious despite daily spike. USDT dominance declining (8.54%) signals fresh risk-appetite rotation into crypto.

US stocks pre-market MIXED: QQQ $714.88 vs close $722.82 (-1.1%) on Samsung earnings miss dragging semiconductors -7%; Dow was record 53,000+ yesterday; financials sector leading. Critical macro event: **FOMC minutes tomorrow July 8 14:00 ET / 21:00 EEST** (June FOMC was hawkish surprise) — reduces sizing for any overnight swing position opened today.

**Action at the open (~10 minutes)**:
- **Crypto**: CHIP/USDT B-tier intraday long is the cleanest setup — watch for pullback into 0.0350–0.0356 zone (current 0.0359, do NOT market-buy). BTC/USDT B-tier swing is WAITING FOR ENTRY near $63k — monitor for fill. Do NOT chase BLUR (78% extended, token unlock July 14).
- **Stocks**: NO action before 09:30 ET open. After open: wait 15 min price discovery. JPM (was-A, score 93, financials leader) and XLF/XLV sector ETFs are priority long-watches — require clean RTH open, no gap-down reversal. **AVOID UNH** (DOJ civil fraud probe, -16%). **MANUAL REVIEW only for MSFT** (securities fraud lawsuit, operator flag active). AMD B-tier already in TP status.
- **Avoid**: UNH (legal), MSFT (legal), BLUR (extended+unlock), SOL (BONK hack operator review), OPG (negative funding + thin volume), tech names before 15-min RTH discovery given QQQ softness.

---

## 2. Data Used

| Source | File / Timestamp | Age at 16:20 EEST | Quality |
|--------|-----------------|-------------------|---------|
| Scalp report | `data/reports/scalp/2026-07-07_11-44_scalp_report.md` (gen 14:44 EEST) | ~96 min | **FRESH** ✓ |
| Intraday report | `data/reports/intraday/2026-07-07_11-50_intraday_report.md` (gen 14:50 EEST) | ~90 min | **FRESH** ✓ |
| Stocks intraday | `data/reports/stocks/intraday/2026-07-07_11-58_stocks_intraday_report.md` (gen 14:58 EEST) | ~82 min | **FRESH** ✓ |
| Swing report | `data/reports/swing/2026-07-07_02-03_swing_report.md` | ~14.3h | **STALE** ✗ (>14h — excluded) |
| Stocks swing/invest | stale >5d | 5 days | **STALE** ✗ (excluded) |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-07_1139.md` | ~4h41m | CONTEXT |
| Cycle 01 (14:37) summary | `data/scheduled_runs/2026-07-07_default_schedule/cycle_01_14-37_summary.md` | ~79 min | FRESH |
| Active signals (crypto) | CLI `active-signals --asset-class crypto` | live | LIVE (47 signals) |
| Active signals (stocks) | CLI `active-signals --asset-class stocks` | live | LIVE (50 signals) |
| Signal stats (crypto+stocks) | CLI `signal-stats` × 2 | live | LIVE |
| Paper monitor status | `reports/PAPER_MONITOR_STATUS_LATEST.md` | cycle 15:01 | FRESH |
| Catalyst events | `data/catalysts/2026-07-07/catalyst_events.jsonl` | cycle | 912 events / 4 baskets |
| Intelligence layer | Cycle step 18 (15:01 EEST) | cycle | 129 symbols; OI sparse |
| External: BTC/ETH | CoinDesk live markets 2026-07-07 | live | primary_source |
| External: US pre-market | StockTwits/Yahoo Finance 2026-07-07 | live | single_source |
| External: FOMC | CoinDesk Crypto Week Ahead 2026-07-06 | 2026-07-06 | primary_source |

**Notes:** TradingView unavailable — all technical levels from local OHLCV/ATR/EMA. Swing stale, excluded. Social attention blind (Reddit 403). Onchain config missing. 11 dead news sources.

---

## 3. Scheduler / Data Freshness

- **Last completed cycle**: `cycle_01_14-37_summary.md` — finished 15:01 EEST (79 min ago), 32/32 steps OK.
- **Monitor status**: crypto_monitor active (log 16:12 EEST), stocks_monitor active (log 15:47 EEST).
- **Scheduler health**: FRESH. Not deferred.
- **Staleness flags**: Swing stale 14.3h (excluded). Stocks swing/invest 5d stale (excluded). Social missing (Reddit 403). Onchain config missing. Derivatives OI numeric sparse.
- **Squeeze phase distribution** (129 symbols): post_unwind_chop=46, build_up=32, unknown=37, squeeze_expansion=6, unwind=5, distribution=3.
- **Paper portfolio** (bybit_non_vip, 845 trades, paper only): net $2,339.36 / +46.79% / maxDD 13.62%.
- **Paper shadow B vs A** (12d forward valid): A −235.09R / B +37.41R; NOT_READY 4/6; DATA_GAP_LATE 37%.
- **Untracked alerts**: **6** (HMSTR, VANRY, ALLO×2, JTO×2 — up from 0 at 11:39 review) → integrity flag.
- **Paper monitor** (cycle 15:01 EEST):
  - OPEN ACTIONABLE: 4
  - WAITING FOR ENTRY: 2
  - ENTERED UNRESOLVED: 22 (entry filled, no TP/SL before window — NOT missed entries)
  - REVIEW/SHADOW: 146
  - NO-ENTRY/STALE/MOVED-AWAY: 96
  - CLOSED TODAY: 370W / 72L / 0 flat
  - NEEDS REVIEW: 1

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-07 16:20 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.83,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "social_attention_missing", "derivatives_sparse"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Cycle 01 (14:37) completed 15:01 EEST, 32/32 OK",
        "Crypto monitor active 16:12 EEST, stocks monitor 15:47 EEST",
        "Scalp/intraday/stocks intraday: FRESH (<96 min)",
        "Swing: STALE 14.3h — excluded",
        "Stocks swing/invest: 5d STALE — excluded",
        "6 untracked alerts (up from 0 at 11:39) — integrity concern",
        "11 dead news sources incl SEC EDGAR, Business Wire, t.me channels",
        "OI numeric history sparse; onchain config missing"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": ["social_attention_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC $63,099 (+2.25%), ETH $1,769 (+1.51%) — uptrend confirmed",
        "Altcoin breadth above EMA20: 60.87%",
        "F&G=27 (fear — not extended)",
        "VIX=15.96, all 4 stock indices uptrend",
        "QQQ pre-market $714.88 vs close $722.82 (-1.1%) — tech-specific softness",
        "Samsung miss -7% — SMH/semiconductor drag at open",
        "Financials (XLF +8.34% RS 20d) leading vs SPY",
        "USDT dominance 8.54% declining — risk-on rotation",
        "crypto_mode=trend, stocks_mode=risk_on (dashboard snapshot)"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["fresh_catalyst", "catalyst_contradicted", "mapping_weak"],
      "data_missing": ["mapping_percentage_unconfirmed"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "912 events today, 4 baskets — mapping % not confirmed (use as context)",
        "SOL BONK hack $20M treasury — block_requires_operator_review active",
        "HYPE fake airdrop exploit — block_requires_operator_review active",
        "FOMC minutes TOMORROW July 8 14:00 ET — limits overnight swing sizing",
        "June FOMC hawkish surprise — minutes may be hawkish",
        "BTC ETF Monday +$265.7M (bullish daily) but 8 consecutive weekly net outflows",
        "NY Fed Williams optimistic on inflation — dovish read",
        "MSFT securities fraud lawsuit, UNH DOJ civil fraud probe"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["post_unwind_chop", "oi_contradicts", "funding_extreme"],
      "data_missing": ["oi_numeric_sparse", "liquidation_heatmap_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "46/129 symbols in post_unwind_chop — most alts exhausted",
        "Only 6 symbols in squeeze_expansion",
        "BLUR: negative funding across Bybit/OKX/MEXC — crowding elevated",
        "OPG: negative funding elevated (-0.00445), crowding unknown",
        "CHIP/ALLO/JTO: funding neutral (5e-05) — not crowded",
        "BTC OI declining on rally (CoinDesk) — rally quality in question",
        "ALLO: price up + OI down = short covering, weaker continuation"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.76,
      "reason_codes": ["entry_fresh", "chase_risk", "overextended", "stale_before_entry"],
      "data_missing": ["tradingview_chart_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "CHIP/USDT: price 0.0359, entry zone 0.0350-0.0356 — pullback needed (~1 ATR)",
        "BTC/USDT swing: WAITING, entry ~$63k, current $63,099 — near entry, monitor fill",
        "OPG/USDT: triggered, volume 0.52x average — weak confirmation, chase_risk",
        "BLUR: >2ATR from EMA20, rejected — do not chase; token unlock July 14",
        "Most stocks: plan-only until RTH confirmation — 15-min discovery needed"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE: 4 (crypto)",
        "WAITING FOR ENTRY: 2",
        "ENTERED UNRESOLVED: 22 (filled, no TP/SL before window)",
        "REVIEW/SHADOW: 146",
        "NO-ENTRY/STALE/MOVED-AWAY: 96",
        "CLOSED TODAY: 370W / 72L / 0 flat",
        "NEEDS REVIEW: 1",
        "6 untracked alerts — PART 1 integrity concern"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["headline_risk", "legal_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "UNH: DOJ civil fraud probe, shares -16% — AVOID all directions",
        "MSFT: securities fraud lawsuit, block_requires_operator_review",
        "SOL/BONK: $20M hack, operator review flag",
        "FOMC minutes tomorrow: reduce overnight swing size",
        "QQQ pre-market -1.1%: tech gap risk at open",
        "Stocks A/B week: 0 wins / 4 losses (n=28, weak sample but cautionary)",
        "6 untracked alerts: integrity anomaly vs 0 at 11:39 review",
        "BTC OI declining on rally — fragility signal"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.73,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto B-tier (n=420): PF 1.63, WR 16.5%, +49R — working",
        "No-catalyst intraday (14d): WR 23%/PF 0.70/-3R — sub-breakeven",
        "Stocks A/B (n=28 weak): 0 wins/4 losses, PF 0.00 this week",
        "Stocks intraday bullish regime: -6.5R/n18/WR 11% — worst bucket",
        "Paper shadow B +37.41R forward but NOT_READY (4/6), DATA_GAP_LATE 37%"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["wait_for_trigger", "longs_preferred", "catalyst_backed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto uptrend holds; BTC near swing entry $63k",
        "QQQ -1.1% sector-specific, not broad; financials/healthcare intact",
        "FOMC minutes tomorrow: limit overnight swing sizing",
        "CHIP/USDT best crypto long (pullback entry, RS+volume, not extended)",
        "BTC swing near entry — most macro-aligned crypto long available",
        "JPM/XLF best stocks plays post-open (financials leading, legal-clean)",
        "UNH AVOID; MSFT MANUAL REVIEW; BLUR/SOL skip",
        "Stocks A/B underperforming bullish regime — no aggressive stocks entry"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.78,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "CHIP/USDT",
      "trigger": "pullback into 0.0350-0.0356 (current 0.0359 — wait for dip, no market buy)",
      "reason": "RS leader +15.2% vs BTC, 1.55x volume, B-tier intraday triggered; not extended; cleanest structure in the scan; no catalyst is the weakness"
    },
    "best_short_candidate": {
      "symbol": "BEL/USDT",
      "trigger": "confirmed lower high on 1h + derivatives data available + clear stop above swing high",
      "reason": "Weakest RS -17.9% vs BTC, 24h -16.61%; squeeze risk and bullish tape require manual-review before entry — do not auto-enter"
    },
    "best_catalyst_candidate": {
      "symbol": "BTC/USDT",
      "trigger": "swing entry fill near $63k confirmed (signal status flips to triggered)",
      "reason": "ETF inflow $265.7M Monday + USDT dominance declining + NY Fed dovish = catalyst-narrative stack; swing B-tier waiting for fill"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ civil fraud investigation confirmed, shares -16% — AVOID all directions per §I legal/headline risk"
    },
    "operator_action": "wait_for_trigger",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.83 | scheduler_fresh, report_stale | advisory_only |
| market_regime | ok | 0.80 | risk_on, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.72 | fresh_catalyst, catalyst_contradicted, mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.68 | post_unwind_chop, oi_contradicts, funding_extreme | advisory_only |
| technical_entry | caution | 0.76 | entry_fresh, chase_risk, overextended, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.82 | open_actionable, waiting_for_entry, entered_unresolved | advisory_only |
| risk_manager | caution | 0.75 | headline_risk, legal_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.73 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.78 | wait_for_trigger, longs_preferred, catalyst_backed | advisory_only |

---

## 4. What Changed vs Previous Review (11:39 EEST)

| Dimension | 11:39 EEST | 16:20 EEST | Change |
|---|---|---|---|
| Slot | Europe/pre-US context | pre-US-open decision | US open NOW in ~10 min |
| Scheduler | Cycle 03 (09:55 EEST) | Cycle 01-window2 (15:01 EEST) | FRESH new cycle |
| BTC | ~$63,182 | ~$63,099 | Minor pullback (-0.1%) |
| ETH | uptrend | $1,769 (+1.51%) | Continues up |
| Reports | From 06:38–06:51 cycle | From 14:37 cycle (fresh) | Updated |
| AMD stocks | Not in focus | B-tier stocks at TP | Already resolved |
| QQQ pre-market | N/A (closed) | $714.88 (-1.1%) | Samsung miss → tech soft |
| Untracked alerts | 0 | **6** (HMSTR, VANRY, ALLO, JTO) | **NEW integrity flag** |
| ETF inflows | N/A | Monday $265.7M BTC | Fresh catalyst |
| FOMC minutes | Confirmed risk | 1 day closer | Reduce swing sizing |
| Best long | PYTH/USDT (entry zone) | CHIP/USDT (triggered, pullback) | Changed |
| Best short | BONK (manual review) | BEL/USDT (manual review) | Changed |
| Stocks priority | AAPL/TSLA/XLV/XLF | JPM/XLF/XLV (financials) | Financials confirmed leader |
| BLUR | Retest-watch (0.0187–0.0195) | Still extended, AVOID new entry | Token unlock July 14 unchanged |

New since 11:39: Samsung miss → semi drag; SPCX Nasdaq-100 addition; NY Fed Williams dovish; USDT dominance declining; UNH DOJ probe now confirmed in data.

---

## 5. Catalyst Coverage

- **Total events today**: 912 (up from 488 at morning review). **Baskets**: 4.
- **Basket primaries**: delisting_thin_liquidity (none), binance_ecosystem (BNB), ai_narrative (NEAR/RENDER/TAO/FET), momentum_breakout (BLUR/VANRY/RE).
- **Mapping %**: Not explicitly computed from current run. Many events are stock legal filings landing in baskets without crypto symbols.
- **⚠ Advisory**: catalyst mapping percentage unconfirmed — **use catalyst layer as context, not final decision** for this run.
- **Notable events**:
  - SOL/BONK: $20M treasury drained (exploit_hack, operator-review flag active)
  - HYPE: fake airdrop exploit $12,300 (operator-review flag active)
  - XRP: Ripple full MiCA license (positive — but price backfired per 11:39 review)
  - BTC: Bitmine $74M ETH purchase + Clarity Act optimism (macro positive)
  - APT: token unlock alert (3 unlocks second week of July 2026)
  - MSFT: securities fraud lawsuit (block_requires_operator_review)
  - UNH: DOJ civil fraud probe (in news section; operator_review NOT yet flagged in production — see TODO)
  - Stocks basket: BRCB, ERAS, RBLX, PODD, WGS securities fraud lawsuits

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood**: risk-on (BTC +2.25%, ETH +1.51%, 60.87% alts above EMA20, USDT dominance declining, ETF daily inflow $265.7M, F&G=27 not extended)
- **Stocks mood**: mixed / pre-open (all indices uptrend, but QQQ pre-market -1.1%; Samsung miss → tech/semi specific weakness; financials and healthcare ex-UNH leading)
- **Dominant narrative**: Crypto ETF rotation + USDT risk-on rotation; Stocks financials leadership (XLF, JPM); Tech-specific softness (Samsung/SMH); FOMC minutes overhang (tomorrow)
- **Preferred side now**: longs, catalyst-backed — pullback entries only, no chase
- **Best long candidate**: CHIP/USDT (pullback 0.0350–0.0356) | JPM/XLF post-RTH-open (financials, legal-clean, RTH confirmation required)
- **Best short candidate**: BEL/USDT (weakest RS -17.9%, but manual review only — squeeze risk in bullish tape)
- **Best catalyst-backed candidate**: BTC/USDT (ETF inflow + USDT rotation; swing entry near $63k)
- **What to avoid**: UNH (DOJ legal), MSFT (legal — manual review), BLUR (extended + unlock July 14), SOL (hack review), OPG (funding/volume), tech names pre-15-min discovery
- **What would change the view**: BTC loses $62,500 → reduce longs; FOMC minutes today early release or hawkish leak → close overnight swings; QQQ reversal above $720 → re-add tech to watchlist; UNH DOJ expanded to sector → avoid XLV entirely

---

## 7. Candidate Deep Dives

### Candidate 1 — CHIP/USDT (B-tier Intraday) — BEST LONG WATCH

**Status**: OPEN ACTIONABLE / TRIGGERED | **Score**: 71.7 · B-tier | **Price**: 0.0359 | **Entry zone**: 0.0350–0.0356 | **ATR**: 0.0013 | **Invalidation**: 1h close below 0.0343 | **TP1**: 0.0372 | **TP2**: 0.0385 | **TP3**: 0.0398 | **RR**: 1.84R

- Has price reacted to catalyst? — No catalyst confirmed. RS+volume driven.
- Is the setup chasing? — NOT in zone. Price 0.0359 is above entry 0.0350–0.0356 (~0.5 ATR above entry). Wait for pullback; do NOT market-buy.
- Overextended? — No, unlike BLUR/RE/RIF (>2ATR rejected). CHIP within normal range.
- Aligned with mood? — Yes: risk-on, RS leader (+15.2% vs BTC), volume 1.55x.
- Actionable now or after confirmation? — After pullback to 0.0350–0.0356 zone. May coincide with BTC open dip.
- Key weakness: no-catalyst intraday 14d: WR 23% / PF 0.70 / −3R. Treat as momentum/RS play, smaller size.
- **Verdict**: BEST LONG WATCH. Enter only on pullback to zone. Size smaller (no catalyst).

---

### Candidate 2 — BTC/USDT (B-tier Swing) — WAITING FOR ENTRY

**Status**: WAITING FOR ENTRY | **Score**: ~66 · B-tier swing | **Current price**: ~$63,099 | **Entry**: ~$63k zone | **Signal**: wa (waiting)

- At/near entry zone? — Yes. BTC $63,099. If entry zone is $63,000–$63,200, price is at/near fill level.
- Catalyst support? — ETF inflow $265.7M Monday, USDT dominance declining, Williams dovish. Counter: 8 consecutive weeks net outflows, OI declining on rally.
- FOMC risk: tomorrow. Any overnight swing — **reduce size ~50%**.
- Aligned with mood? — Yes: primary macro trend; strongest institutional narrative.
- **Verdict**: WAITING FOR ENTRY. Most macro-aligned crypto long. If filled, confirm with 15-min structure. Size −50% for FOMC exposure.

---

### Candidate 3 — JPM / XLF / XLV (Stocks) — WAIT FOR RTH CONFIRMATION

**Status**: WAITING FOR RTH OPEN (in ~10 min) | **JPM was-A score**: 92.68 | **XLF was-A**: 85.89 | **XLV was-A**: 88.20

**Legal/headline check (§I)**:
- JPM: "Shares flat since Cramer commented" — Cramer noise only. No DOJ/SEC/fraud. CLEAR.
- XLF (sector ETF): No legal flag. CLEAR.
- XLV: Check for UNH contagion — UNH is a large XLV component. If UNH opening gap-down causes sector spread, XLV entry must be aborted. Check first 15 min.

**Assessment**:
- Financials sector strongest 20d RS vs SPY (+8.34%). QQQ weakness is tech-specific, NOT financials.
- Samsung miss hits SMH/chips — JPM/XLF are not semiconductor-exposed.
- Stocks A/B playbook underperforming this week (WR 11%, −6.5R in bullish regime, n=18) — half-size if any entry.
- **Verdict**: WAIT FOR RTH CONFIRMATION. 09:30 ET open → wait until 09:45 ET (16:45 EEST) for 15-min price discovery. Enter JPM/XLF only if: (a) no gap-down reversal, (b) directional expansion, (c) XLV not showing UNH contagion. Half-size.

---

### Candidate 4 — OPG/USDT (B-tier Intraday) — CONTRADICTION / CAUTION

**Status**: TRIGGERED | **Score**: 68.3 | **Price**: 0.1434 | **Entry zone**: 0.1365–0.1413

**Contradictions**: Negative funding across OKX/Bybit/MEXC (crowding elevated). Volume 0.52x (below average). Price 0.1434 is above entry zone — already extended past the planned entry. No derivatives confirmation (binance-anchor only).

**Verdict**: DO NOT ENTER at current price. If price pulls back to 0.1365–0.1413 WITH volume improvement and funding normalization, reconsider. Lower priority than CHIP.

---

### Candidate 5 — UNH (AVOID) + MSFT (MANUAL REVIEW) — LEGAL/HEADLINE RISK

**UNH — LEGAL/HEADLINE RISK: AVOID**
- DOJ civil fraud investigation confirmed. Sources: QuiverQuant, CBS News (date_unavailable but price -16% confirms materiality).
- Active in C-tier stocks signals (multiple "triggered" rows). These predate the DOJ news.
- **Operator action required**: Any UNH signal should be flagged/blocked. UNH is also a large XLV component — potential sector contagion. Verdict: AVOID all directions.

**MSFT — LEGAL/HEADLINE RISK: MANUAL REVIEW**
- Securities fraud lawsuit (PR Newswire). block_requires_operator_review flag active.
- MSFT C-tier score 63.66. Not A/B. But flag for any operator who may consider MSFT.
- Verdict: MANUAL REVIEW REQUIRED. Do not treat as clean.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Type | Direction | Status | Trigger |
|---|---|---|---|---|---|
| 1 | CHIP/USDT | crypto intraday B | Long | OPEN ACTIONABLE — wait pullback | Pullback to 0.0350–0.0356 |
| 2 | BTC/USDT | crypto swing B | Long | WAITING FOR ENTRY | Fill ~$63k swing entry confirmed |
| 3 | JPM / XLF | stocks C (was-A) | Long | WAITING FOR RTH OPEN | 09:45 ET discovery + no gap-reversal + XLV clean |
| Best long-watch | CHIP/USDT | — | Long | Pullback 0.0350–0.0356 | — |
| Best short-watch | BEL/USDT | crypto C | Short | MANUAL REVIEW | Confirmed lower high 1h + derivatives + clear stop |
| Best catalyst-watch | BTC/USDT | crypto swing | Long | Near entry | Swing fill + ETF inflow narrative |
| Avoid | UNH | stocks | ALL | AVOID | DOJ civil fraud investigation |

**Excess candidates**: ALLO (already at TP, resolved), BLUR (>2ATR extended + July 14 unlock), VANRY/JTO (scalp disabled), OPG (contradiction), AMD stocks (B-tier already TP).

---

## 9. Avoid / No Trade (this decision window only — scanning continues)

| Symbol / Category | Reason | Duration |
|---|---|---|
| UNH | DOJ civil fraud probe — AVOID all directions | Until legal resolution |
| MSFT | Securities fraud lawsuit — MANUAL REVIEW only | Until operator clears |
| BLUR/USDT | Extended >2ATR, token unlock July 14, crowding | Wait retest zone only |
| SOL/USDT | BONK hack operator-review flag | Until operator clears |
| HYPE/USDT | Fake airdrop exploit operator-review flag | Until operator clears |
| OPG/USDT | Negative funding + thin volume contradiction | Until volume normalizes |
| Tech stocks (QQQ/NVDA/AMD) | Samsung miss, pre-market -1.1% | 15-min RTH discovery first |
| XLV | Potential UNH sector contagion | Monitor first 15 min |
| No-catalyst intraday crypto | 14d WR 23%/PF 0.70/-3R | Prefer RS+catalyst combos |
| Stocks A/B (full-size) | Bullish regime WR 11%/-6.5R/n18 | Half-size until playbook improves |

The scanner continues running in all conditions. This is decision-window guidance only.

---

## 10. Main Risks

1. **FOMC minutes tomorrow (July 8 14:00 ET / 21:00 EEST)**: June was hawkish. Minutes may reveal more hawkish discussion — any overnight crypto/swing position carries event risk. Reduce swing sizes ~50%.
2. **Tech gap risk at open (QQQ -1.1% pre-market)**: Samsung miss → SMH/semiconductor drag. Tech names at gap-down risk at 09:30 ET. Wait 15-min price discovery for all tech.
3. **BTC ETF weekly outflow trend**: 8 consecutive weeks net negative despite daily $265.7M spike. Institutional base not yet turning. Single day is not reversal proof.
4. **UNH DOJ probe sector contagion**: UNH DOJ probe can spread to XLV (healthcare ETF). XLV was-A score 88 but UNH weight is material.
5. **OI declining on BTC rally**: BTC OI declining while price rises = fragility. If institutional longs aren't building positions, rally may be retail-driven only.
6. **Untracked alerts (6)**: From 0 at 11:39 to 6 now. If PART 1 regression, untracked signals from Telegram → no outcome recording → performance metrics become unreliable over time.
7. **Stocks A/B playbook**: 0 wins this week. Bullish regime bucket worst (-6.5R). Not definitive at n=28 but signals caution for aggressive stocks entries.
8. **No clean short setups**: All crypto shorts are in bullish tape / squeeze-risk / rejected. Short exposure is near-zero this session — asymmetric long-only risk if BTC reverses.

---

## 11. Action Plan — Next 4 Hours (16:20–20:20 EEST)

**Now → 16:30 EEST (US open)**:
- Monitor CHIP/USDT for pullback to 0.0350–0.0356
- Monitor BTC swing signal for status flip from "wa" → "tr" (fill near $63k)
- No stocks action

**16:30 EEST (09:30 ET — cash open)**:
- Observe first 5-min candle: JPM, XLF, XLV, QQQ
- QQQ expected gap down ~1% (Samsung). Does it stabilize or cascade?
- JPM/XLF: should not gap down if financials leading
- XLV: watch for UNH contagion bleed into sector

**16:30–16:45 EEST (15-min discovery)**:
- No stocks entries
- If CHIP/USDT pulls back into zone during BTC open dip → primary crypto entry
- BTC swing: confirm fill status

**16:45–17:30 EEST (first RTH hour)**:
- JPM/XLF/XLV: enter if clean expansion, no reversal, XLV no contagion — half-size
- CHIP/USDT: enter on pullback to zone; missed zone → move to watchlist
- XRP/USDT: catalyst-watch for daily close (monitor through session)
- Swing positions: committed size capped for FOMC tomorrow

**17:30–20:20 EEST (mid/late session)**:
- Monitor BTC/ETH for afternoon continuation
- Watch untracked alert count — if >10, flag as PART 1 regression
- No new swing entries after 18:00 EEST given FOMC exposure
- Check open-intraday lifecycle review for any signals NEEDING REVIEW

---

## 12. Final Verdict per Mode

| Mode | Status | Verdict |
|---|---|---|
| Crypto scalp | kill-switch OFF | NO TRADE (disabled) |
| Crypto intraday | active | SELECTIVE LONG-WATCH — CHIP pullback 0.0350–0.0356; size smaller (no catalyst headwind) |
| Crypto swing | active | WAITING FOR ENTRY — BTC near $63k; size −50% for FOMC tomorrow |
| Stocks intraday | RTH opening | WAIT FOR RTH CONFIRMATION — JPM/XLF/XLY if clean; avoid UNH/MSFT; half-size (playbook WR 11% bullish bucket) |
| Stocks swing | stale report 14.3h | PLANNING ONLY — no actionable entry this slot |
| Stocks invest | stale 5d | EXCLUDED |

---

## 13. Sources

- [Bitcoin and ethereum prices today, July 7, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-july-7-2026-another-strong-opening-for-btc-and-eth-prices-120355126.html) — BTC $63,099/ETH $1,769 confirm / date: 2026-07-07 / verification: primary_source / label: confirms
- [Live markets: BTC and ETH ETFs drew inflows on Monday — CoinDesk](https://www.coindesk.com/tech/2026/07/07/live-markets-bitcoin-and-ether-etfs-drew-inflows-on-monday) — ETF $265.7M, Samsung miss, Williams dovish, 8-week outflow context / date: 2026-07-07 / verification: primary_source / label: confirms
- [FOMC minutes, SpaceX Nasdaq-100 — Crypto Week Ahead, CoinDesk](https://www.coindesk.com/markets/2026/07/06/fomc-minutes-spacex-joins-nasdaq-100-crypto-week-ahead) — July 8 FOMC minutes date confirmed / date: 2026-07-06 / verification: primary_source / label: confirms
- [FOMC June 2026 Impact on Crypto — Intellectia](https://intellectia.ai/blog/fomc-june-2026-crypto-impact) — June FOMC hawkish surprise context / date: 2026-06 / verification: single_source / label: context
- [S&P 500, Nasdaq Futures Mixed after Record Session — StockTwits](https://stocktwits.com/news-articles/markets/equity/s-and-p-500-nasdaq-dow-futures-mixed-after-record-session-why-mu-sndk-rivn-spcx-stocks-are-trending-overnight/cZmleiCR7ma) — QQQ $714.88 pre-market, mixed futures / date: 2026-07-07 / verification: single_source / label: confirms
- [Bitcoin Has Rallied 10% In July — Forbes](https://www.forbes.com/sites/digital-assets/2026/07/06/bitcoin-has-rallied-10-in-july-as-stronger-sentiment-fuels-gains/) — BTC July +10% rally context / date: 2026-07-06 / verification: single_source / label: context
- Internal: `data/reports/scalp/2026-07-07_11-44_scalp_report.md` — FRESH, BLUR/CHIP/ALLO/OPG signals, scalp regime
- Internal: `data/reports/intraday/2026-07-07_11-50_intraday_report.md` — FRESH, CHIP/OPG/ALLO B-tier, derivatives
- Internal: `data/reports/stocks/intraday/2026-07-07_11-58_stocks_intraday_report.md` — FRESH, JPM/XLF/XLV/UNH/MSFT legal flags
- Internal: `data/scheduled_runs/2026-07-07_default_schedule/cycle_01_14-37_summary.md` — paper monitor, squeeze phases, active signals

---

## 14. Fix Requests / TODO

### TODO-untracked-alerts-spike
- **issue**: 6 untracked legacy alerts this cycle (HMSTR, VANRY, ALLO×2, JTO×2) — up from 0 at 11:39 review. Alerts sent to Telegram but no proposed_signal → outcomes cannot be tracked.
- **evidence**: `cycle_01_14-37_summary.md` step 28 output: "6 untracked legacy crypto alert(s)"
- **suggested manual fix**: Investigate why HMSTR/VANRY/ALLO/JTO alerts fire without corresponding proposed_signals in the same cycle window. Check whether the watchlist_alert dispatch path creates proposed_signals first; if not, fix the alert dispatch to always register a signal_id before sending to Telegram.
- **priority**: high
- **first observed**: 2026-07-07 16:20 EEST (was 0 at 11:39 EEST review)

### TODO-unh-operator-review-missing
- **issue**: UNH DOJ civil fraud probe confirmed (shares -16%) but block_requires_operator_review is NOT set for UNH in production risk warnings (only HYPE/MSFT/SOL flagged). The DOJ news may have arrived after the catalyst scan window.
- **evidence**: Stocks intraday report §4 shows UNH DOJ probe items with date_unavailable. UNH active in C-tier stocks signals (multiple "triggered" rows). Production risk warnings block section does not mention UNH.
- **suggested manual fix**: Manually add a UNH operator-review note. Audit news risk scanner to catch DOJ/investigation/fraud patterns for active symbols even when publication date is unavailable.
- **priority**: high
- **first observed**: 2026-07-07 16:20 EEST

### TODO-stocks-session-mislabel
- **issue**: Stocks intraday report labels session as "after-hours (UTC overnight)" when data was generated at 11:57 UTC = 07:57 ET = US pre-market. Label is incorrect.
- **evidence**: `data/reports/stocks/intraday/2026-07-07_11-58_stocks_intraday_report.md` line 7
- **suggested manual fix**: Fix session-detection logic to correctly classify 04:00–09:30 ET as "pre-market" not "after-hours". While the demote gate outcome is the same, the label causes confusion in reviews.
- **priority**: low
- **first observed**: 2026-07-07 16:20 EEST
