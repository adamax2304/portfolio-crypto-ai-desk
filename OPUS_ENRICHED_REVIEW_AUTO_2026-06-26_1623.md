# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:23 EEST

**Slot:** pre-US-open decision review (16:20 EEST slot)
**Time:** 2026-06-26 16:23 EEST (~7 min before US cash open at 09:30 ET / 16:30 EEST)
**Date:** 2026-06-26 (Friday — weekday, crypto+stocks)
**Model:** claude-sonnet-4-6
**Advisory only — no auto-trade, no signal registration**

---

## 1. Executive Summary

**Slot: pre-US-open decision review — advisory only / no auto-trade.**

**BTC confirmed below $60K at US open:** BTC opened at $59,707 (−2.1% today, −18.8% since June 1). ETH opened at $1,564 (−3.4%, −21.9% since June 1). PCE data released June 25 drove further declines. Crypto regime: **bearish trend (risk-off)** — altcoin breadth 27.7% above EMA20 (deteriorated from 41% at 11:39 review), BTC ATR at 100th percentile.

**Crypto: 10 B-tier signals, ALL ENTERED UNRESOLVED (tp_hit, partials taken).** No new OPEN ACTIONABLE crypto entries. **CRITICAL: ETH/USDT carries simultaneous swing short AND swing long — both ENTERED UNRESOLVED — CONTRADICTION. Manual review required before adding any ETH exposure.**

**New from Cycle 4 (13:35–14:35):** G/USDT scalp long, BEL/USDT swing long, ETH/USDT swing long all moved OPEN ACTIONABLE → ENTERED UNRESOLVED (TP1 hit). Altcoin breadth regressed 41%→27.7% between reviews. New MiCA headwind: Binance winding down EU crypto services.

**Stocks (opening in ~7 min):** Regime: chop (VIX 20.09). B-tier triggered: AAPL short, JPM long, AMD long — **do NOT chase pre-market; wait 15–30 min RTH confirmation before entry.** JPM A-tier: ENTERED UNRESOLVED. **UNH: MANDATORY AVOID — DOJ fraud probe confirmed (criminal + civil), stock −55% from ATH. C-tier UNH long signal triggered — ignore completely.** ADA: exploit confirmed → AVOID.

**HYPE/USDT:** best catalyst-backed watch — 267K+ HYPE accumulated by whales from Coinbase Prime, Multicoin Capital bullish thesis, perps_dex_narrative fresh <1h.

**ALWAYS-SCAN continues. Scanner, data collection, monitoring unchanged.**

---

## 2. Data Used

| Source | File | Generated (EEST) | Age at 16:23 | Status |
|--------|------|-----------------|--------------|--------|
| Scheduler log | scheduler.log | 14:35 | 1h48m | FRESH |
| Cycle 4 summary | cycle_04_13-35_summary.md | 14:35 | 1h48m | FRESH (30 OK / 0 failed) |
| Scalp report | 2026-06-26_10-59_scalp_report.md | 13:59 | 2h24m | FRESH |
| Intraday crypto | 2026-06-26_11-13_intraday_report.md | 14:13 | 2h10m | FRESH |
| Swing crypto | 2026-06-26_02-25_swing_report.md | 05:25 | 10h58m | CARRY-FORWARD (borderline stale) |
| Stocks intraday | 2026-06-26_11-33_stocks_intraday_report.md | 14:33 | 1h50m | FRESH |
| Stocks swing | 2026-06-26_02-31_stocks_swing_report.md | 05:31 | 10h52m | CARRY-FORWARD (borderline stale) |
| Stocks invest | 2026-06-26_02-35_stocks_invest_report.md | 05:35 | 10h48m | CARRY-FORWARD (borderline stale) |
| Catalyst cycle | catalyst_cycle_11-14.md | 14:14 | 2h9m | FRESH |
| Active signals CLI | src.cli active-signals x2 | 16:23 | live | LIVE |
| Signal stats CLI | src.cli signal-stats x2 | 16:23 | live | LIVE |
| Untracked legacy | detect_untracked_legacy_alerts | 16:23 | live | NONE FOUND |
| External web | WebSearch BTC/ETH prices + UNH DOJ + US pre-market | 16:23 | live | LIVE |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-26_1139.md | 11:39 | 4h44m | READ |

**Blindspots:** Swing/invest reports 11h+ old (borderline stale — flagged); Bybit partial OI data (cycle 4 partially restored); Reddit social blocked; onchain config missing; no live CVD/liquidation heatmaps; no live tick data (using open-session externals).

---

## 3. Scheduler / Data Freshness

- **Scheduler log** mtime: 14:35 EEST (1h48m ago). **NOT DEFERRED.**
- **Cycle 4**: 2026-06-26 13:35–14:35 EEST. Steps: 30 OK / 0 failed. CLEAN.
- **Active crypto signals**: 10 B-tier (ALL tp_hit = ENTERED UNRESOLVED).
- **Active stocks signals**: 50 total (1 A-tier tp_hit; 3+ B-tier triggered; 40+ C-tier mix of waiting/triggered).
- **Untracked legacy alerts**: NONE (clean).
- **Signal stats crypto (week):** A/B sample n=150, PF=1.24, WR=21.1%, +13R. By mode: swing 1.94 PF (+18R) ✓; intraday 1.03 PF (+1R); scalp 0.14 PF (−6R) ✗. By direction: longs 2.39 PF (+15R) ✓; shorts 0.93 PF (−2R) ✗ despite bearish tape.
- **Signal stats stocks (week):** A/B sample n=19 (weak), PF=1.11, +1R. C-tier −13R (watchlist only).
- **Bybit API**: partially restored in Cycle 4 (BEL, PUMP, BNB, INJ, HYPER fetched).

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-06-26 16:23 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["risk_off", "shorts_preferred", "chop", "wait_for_trigger"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["data_unavailable", "oi_contradicts", "squeeze_risk"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry", "wait_for_trigger"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["entered_unresolved", "open_actionable", "waiting_for_entry", "needs_review"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.85,
      "reason_codes": ["manual_review", "legal_risk", "headline_risk", "correlation_cluster", "reduce_risk"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["wait_for_trigger", "manual_review", "reduce_risk"],
      "suggested_effect": "advisory_only"
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.82,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "JTO/USDT", "trigger": "Pullback into 0.7373-0.7494, BTC >$59K, vol ≥1.5x" },
    "best_short_candidate": { "symbol": "ENA/USDT", "trigger": "Failed bounce/retest 0.0787-0.0793, inval. 0.0801" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "Pullback after RTH mood confirmed, perps_dex basket entry" },
    "avoid_candidate": { "symbol": "UNH", "reason": "DOJ criminal+civil Medicare fraud probe — MANDATORY AVOID" },
    "operator_action": "wait_for_trigger",
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|------------|--------------|-----------------|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale, derivatives_sparse | advisory_only |
| market_regime | caution | 0.82 | risk_off, shorts_preferred, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.75 | fresh_catalyst, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.60 | data_unavailable, oi_contradicts, squeeze_risk | advisory_only |
| technical_entry | caution | 0.75 | entry_late, chase_risk, stale_before_entry, wait_for_trigger | advisory_only |
| execution_lifecycle | ok | 0.88 | entered_unresolved, open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.85 | manual_review, legal_risk, headline_risk, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | ok | 0.78 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.82 | wait_for_trigger, manual_review, reduce_risk | advisory_only |

---

## 4. What Changed vs Previous Review

**Previous:** OPUS_ENRICHED_REVIEW_AUTO_2026-06-26_1139.md (11:39 EEST)

| Change | Detail |
|--------|--------|
| G/USDT scalp long | OPEN ACTIONABLE → ENTERED UNRESOLVED (TP1 hit Cycle 4) |
| BEL/USDT swing long | OPEN ACTIONABLE → ENTERED UNRESOLVED (TP1 hit) |
| ETH/USDT swing long | OPEN ACTIONABLE → ENTERED UNRESOLVED (TP1 hit) — **now contradicts ETH swing short** |
| ETH dual position | **NEW CONTRADICTION**: swing short + swing long both ENTERED UNRESOLVED simultaneously |
| Altcoin breadth | Regressed: 41% → 27.7%. Regime did not sustain morning improvement. |
| BTC $60K break | Confirmed at $59,707 at US open. Psychological level lost. |
| MiCA/Binance EU | **NEW**: Binance winding down EU crypto services. Not in previous review. |
| JTO basket membership | JTO now in momentum_breakout basket (fresh <1h). |
| Signal stats | PF declined 1.28→1.24. Shorts continue losing (0.93). Swing dominant (1.94 PF). |

---

## 5. Catalyst Coverage

- **Cycle 11-14 (14:14 EEST, 2h9m ago):** 323 events, 6 baskets.
- **Top catalyst:** UNH DOJ probe (0.73) — MANDATORY AVOID.
- **Key baskets:** momentum_breakout (G/HEI/JTO fresh <1h), perps_dex_narrative (HYPE fresh <6h), ai_narrative (NEAR/RENDER/TAO/FET fresh <1h).
- **New regulatory headwind:** MiCA forces Binance EU wind-down (bearish crypto macro).
- **Mapping quality:** STRONG (majority of 323 events mapped via detected_symbols).

---

## 6. Market Landscape

**Crypto regime:** bearish trend (risk-off). BTC $59,707 open. ETH $1,564 open. Altcoin breadth 27.7%. BTC ATR percentile 100.

**Stocks regime:** chop (VIX 20.09, 50% breadth EMA20, 2/4 indices uptrend). SPY/QQQ range, IWM/DIA uptrend. Strongest sectors: semiconductors (+9.1% RS), industrials (+7.8%), healthcare (+6.8%).

### Market Mood / Risk Routing

- **Crypto mood:** risk-off → prefer shorts after failed retest; catalyst-backed RS leaders for any long
- **Stocks mood:** chop + RTH opening → wait 15-30 min bar before any new entry
- **Best long:** JTO/USDT — pullback into 0.7373-0.7494, BTC >$59K, vol ≥1.3x
- **Best short:** ENA/USDT — failed bounce 0.0787-0.0793, inval. 0.0801
- **Best catalyst:** HYPE/USDT — pullback entry after RTH mood confirmed
- **Avoid:** UNH (DOJ/legal), G/USDT scalp (losing bucket, chase risk), ADA (exploit), pre-market chasing
- **Regime change trigger:** BTC above $61K + alt breadth >45% → neutral/mixed; all 4 indices green + SMH leading → stocks upgrade

---

## 7. Candidate Deep Dives

### 7.1 ETH/USDT — NEEDS REVIEW (Dual Position Contradiction)
- **Status:** Swing short ENTERED UNRESOLVED + Swing long ENTERED UNRESOLVED — simultaneously.
- **Risk:** Undefined net ETH exposure. Short is regime-aligned. Long was counter-trend TP1 capture.
- **No new ETH exposure until manually resolved.** Short thesis is primary.

### 7.2 BTC/USDT — Both Shorts ENTERED UNRESOLVED (aligned)
- Regime-aligned bearish. ETF outflows $500M. $1.48B liquidations. $59K support next.
- Do NOT add new BTC short. Monitor $59K.

### 7.3 JTO/USDT — Best Long-Watch
- RS leader +14.9% vs BTC, vol 1.77x, momentum_breakout basket (fresh <1h).
- Pullback zone: 0.7373-0.7494. Current: $0.7548. **Do not enter above $0.7600.**
- Stop: 1h close below 0.7226.

### 7.4 JPM — A-tier Entered + B-tier OPEN ACTIONABLE
- A-tier ENTERED UNRESOLVED (hold). B-tier triggered pre-market. Legal: CLEAN.
- **Wait 15-30 min RTH bar before treating B-tier as actionable.**

### 7.5 UNH — MANDATORY AVOID
- DOJ criminal+civil Medicare fraud probe confirmed. −55% from ATH. C-tier long triggered — **ignore completely.**

---

## 8. Best Candidates Ranked

| Rank | Symbol | Direction | Type | Trigger | Notes |
|------|--------|-----------|------|---------|-------|
| 1 | **JTO/USDT** | Long-watch | Crypto | Pullback 0.7373-0.7494, BTC >$59K, vol ≥1.3x | RS leader, momentum basket, clean deriv |
| 2 | **ENA/USDT** | Short-watch | Crypto | Failed bounce/retest 0.0787-0.0793 | Weak RS, fresh shorts OI, no catalyst |
| 3 | **HYPE/USDT** | Catalyst-watch | Crypto | Pullback after RTH mood confirmed | Whale accum, Multicoin thesis, fresh basket |
| 4 | **JPM** (B-tier) | Long-watch | Stock | RTH + 15-30 min bar confirmation | OPEN ACTIONABLE pending RTH; legal clean |
| 5 | **ETH swing short** | Managing | Crypto | Monitor SL $1,558.87 | ENTERED UNRESOLVED, no add |

---

## 9. Avoid / No Trade

1. **UNH** — DOJ probe MANDATORY AVOID, all tiers.
2. **ADA** — wallet exploit confirmed.
3. **G/USDT scalp new entries** — losing playbook, extended.
4. **Pre-market stock chasing** — wait 15-30 min RTH.
5. **New crypto shorts without retest** — PF 0.93, squeeze risk.
6. **ETH new exposure** — dual position contradiction unresolved.

---

## 10. Main Risks

1. BTC squeeze bounce (oversold -18.8%, ATR 100th pct)
2. US open gap shock → crypto leg down through $58K
3. ETH dual position undefined net exposure
4. UNH signal generation bug (legal risk not suppressing signal)
5. Swing reports 11h stale
6. MiCA/Binance EU wind-down (liquidity headwind)
7. PCE/Fed hawkish repricing (rate cuts → 2027)
8. Friday pre-weekend gap risk

---

## 11. Action Plan — Next 4 Hours

**16:23–16:45 (opening 15 min):** Monitor BTC first bar, JPM B-tier direction. No ETH add. No UNH.
**16:45–18:30 (US first hour):** JTO pullback watch, ENA retest watch, HYPE catalyst watch. AAPL/AMD RTH confirmation.
**18:30 (reaction review):** Re-evaluate all ENTERED UNRESOLVED. ETH dual position should be resolved before this review.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Rationale |
|------|---------|-----------|
| Scalp | AVOID | PF 0.14 losing |
| Intraday crypto | WATCH/WAIT | JTO/ENA watch; BTC must stabilize |
| Swing crypto | MANAGE EXISTING | No new swings; ETH contradiction pending |
| Stocks intraday | RTH CONFIRMATION | Wait 15-30 min bar; avoid UNH |
| Stocks swing | WATCHLIST ONLY | 11h stale; −12R 48h audit |
| Catalyst-backed | BEST OPPORTUNITY | HYPE pullback, JTO momentum basket |

---

## 13. Sources

- Yahoo Finance 2026-06-26: BTC $59,707 / ETH $1,564 open
- QuiverQuant + catalyst_cycle_11-14: UNH DOJ probe (0.73 importance)
- BeInCrypto + catalyst_cycle_11-14: MiCA/Binance EU wind-down
- AMBCrypto + internal: BTC ETF outflows $500M, $1.48B liquidations
- lookonchain + catalyst_cycle_11-14: HYPE whale accumulation 267K+
- CryptoBriefing + catalyst_cycle_11-14: Multicoin Capital HYPE $319 target
- Internal catalyst_cycle_11-14: JTO momentum_breakout basket (fresh <1h)
- CNBC 2026-06-24: S&P -1.44%, QQQ -3.29% tech selloff

---

## 14. Fix Requests / TODO

### TODO-UNH-SIGNAL-LEGAL-BYPASS (HIGH)
UNH C-tier long generated/triggered despite legal_risk catalyst (importance 0.73). Add legal_risk suppression rule → auto-demote or flag signals when active legal_risk catalyst ≥ 0.60 for same symbol.

### TODO-ETH-DUAL-POSITION (HIGH)
ETH swing short + swing long both ENTERED UNRESOLVED simultaneously. Add same-symbol/same-timeframe contradiction check to block or flag opposing-direction entries. First noted 11:39 EEST, unresolved at 16:23.

### TODO-SCALP-PLAYBOOK-AUDIT (MEDIUM)
Scalp PF 0.14, -6R over week. Review TP1/horizon mismatch vs MFE distribution. Consider pausing scalp A/B generation until 20-trade audit completes.
