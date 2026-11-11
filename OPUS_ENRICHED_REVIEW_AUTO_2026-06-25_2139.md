# Opus Enriched Review — LATE-SESSION RISK REVIEW — Auto Cycle 21:39 EEST

**Slot:** Late-Session Risk Review (21:30 EEST slot)
**Time:** 2026-06-25 21:39 EEST (14:39 ET — ~3h 9min into RTH)
**Date:** 2026-06-25
**Model:** claude-sonnet-4-6
**Advisory only — no auto-trade, no signal registration**

---

## 1. Executive Summary

**Slot: Late-Session Risk Review.** 3h 9min into RTH, ~2h 20min to US close. This is the position-management window: no new trades on late-signals, manage existing, reduce risk into close.

**Critical upgrade — AAVE:** AAVE promoted from C-tier watchlist to **B-tier intraday long, TRIGGERED**. Catalyst is two-layer: (1) Standard Chartered initiated coverage with $180 YE-2026 target; (2) "Aave Will Win" (AWW) DAO framework now routes 100% of all protocol revenue directly to DAO treasury — a fundamental shift from governance token to cash-flow asset. AAVE is up ~8% on the day at $85.82. This is the strongest single catalyst in today's data. However: it is counter-tape in a risk-off crypto environment — only actionable on pullback to $79-82, not a chase at current levels.

**JPM A-tier long: TP1 confirmed hit.** Day high $343.45 vs TP1 $343.43. Currently ~$340.95. Trail stop to BE or just above entry; do not add at close.

**BTC below $60,000.** At $59,334 as of 15:37 EEST, likely lower now. B-tier swing short OPEN actionable with tp_hits. Extreme ATR (99th percentile).

**AAPL B short risk:** AAPL recovered to $292.94–$299.70 today. The B-tier short entry zone was ~$27x and invalidation ~$28x. At $293+ AAPL is above invalidation. This signal is likely NO-ENTRY/MOVED-AWAY — flag for review.

**UNH legal risk:** C-tier longs triggered in database. DOJ criminal probe confirmed. AVOID — manual review required.

**5 crypto longs in bearish regime:** HOT/ETH/AXS/FIL/WLD B swing longs all active while BTC/ETH are in confirmed downtrend. Late-session: review each for stop integrity; do not add to these positions.

_Advisory only. No auto-trade. No code changes._

---

## 2. Data Used

| Source | File | Generated (EEST) | Age at 21:39 | Status |
|--------|------|-----------|--------------|--------|
| Scheduler log | scheduler.log | 20:24 | 75 min | ✅ FRESH |
| Latest cycle | cycle_06_19-29_summary.md | 20:24 | 75 min | ✅ FRESH |
| Monitors | crypto/stocks_monitor_1782408208 | 21:39 | <1 min | ✅ LIVE |
| Scalp report | 2026-06-25_16-49_scalp_report.md | 19:49 | 110 min | ✅ FRESH |
| Intraday crypto | 2026-06-25_17-03_intraday_report.md | 20:03 | 96 min | ✅ FRESH |
| Swing crypto | 2026-06-25_14-03_swing_report.md | 17:03 | 276 min | ⚠️ CARRY-FORWARD |
| Stocks intraday | 2026-06-25_18-15_stocks_intraday_report.md | 21:15 | 24 min | ✅ VERY FRESH |
| Stocks swing | 2026-06-25_14-19_stocks_swing_report.md | 17:19 | 260 min | ⚠️ CARRY-FORWARD |
| Stocks invest | 2026-06-25_14-27_stocks_invest_report.md | 17:27 | 252 min | ⚠️ CARRY-FORWARD |
| LLM packet | llm_analysis_packet.md | 20:03 | 96 min | ✅ FRESH |
| Active signals CLI | src.cli active-signals ×2 | 21:39 | live | ✅ LIVE |
| Signal stats CLI | src.cli signal-stats ×2 | 21:39 | live | ✅ LIVE |
| Untracked legacy | detect_untracked_legacy_alerts | via cycle 06 | 75 min | ✅ None found |
| External web | WebSearch/WebFetch | 21:39 | live | ✅ LIVE |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-25_1839.md | 18:39 | 3h | ✅ READ |

**External web research:** Available. 4 sources fetched and verified (§13).

**Blindspots:** Live crypto price feed (internal OHLCV last ~20:03 EEST), real-time OI/funding, liquidation heatmaps, social attention (Reddit blocked), CVD, ETF flows.

---

## 3. Scheduler / Data Freshness

- **Scheduler cycle 06:** Ran 19:29–20:24 EEST (55-min run, 28 steps OK, 0 failed). Label: weekday crypto+stocks. ✅ FRESH.
- **Monitors:** crypto_monitor_1782408208 and stocks_monitor_1782408208 both wrote at 21:39 (this slot). Background monitors are LIVE.
- **Crypto reports:** Scalp (110min, fresh), Intraday (96min, fresh), Swing (4.6h, carry-forward — use for context only).
- **Stocks reports:** Intraday ultra-fresh (21:15 EEST, 24min ago — covers full RTH through 18:15 UTC). Swing/invest carry-forward (4.3h).
- **Paper monitor (cycle 06 status):** Open actionable: 3 · Waiting: 0 · Entered unresolved: 20 · Review/Shadow: 179 · No-entry/stale/moved: 29 · Needs review: 1 · Closed today: 296W / 43L / 0flat.
- **Intelligence layer:** Updated at 17:06 UTC (20:06 EEST). Derivatives cache: 92 symbols. Squeeze phase distribution: build_up=8, squeeze_expansion=4, unwind=5, post_unwind_chop=35.
- **Onchain:** interface_ready_config_missing — no `config/onchain.yaml`.
- **Untracked legacy crypto alerts:** None (clean pass in cycle 06).

**Defer rule check:** Both scheduler.log (75min) and latest cycle summary (75min) are well under 3 hours. ✅ Do NOT defer.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-06-25 21:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "live_crypto_price_realtime", "social_attention"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_06_20:24_75min_28steps_ok", "monitors_21:39_live", "stocks_intraday_21:15_24min", "scalp_19:49_110min", "intraday_20:03_96min", "swing_17:03_276min_carry_forward", "external_web_live_4sources"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["risk_off", "chop", "mixed", "shorts_preferred"],
      "data_missing": ["live_btc_stream"],
      "suggested_effect": "advisory_only",
      "facts_used": ["btc_downtrend_59334_below_60k", "eth_downtrend_1561", "altcoin_breadth_20.45pct", "btc_atr_99th_pct_elevated_extreme", "vix_18.93", "spy_range_qqq_range", "iwm_uptrend", "dia_uptrend", "stocks_chop_neutral", "etf_outflows_btc_-7439_eth_-21234"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "ok",
      "confidence": 0.83,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["aave_standard_chartered_180_2026ye_confirmed", "aave_aww_100pct_revenue_dao_treasury_fundamental", "jpm_day_high_343.45_vs_tp1_343.43_confirmed_hit", "aapl_china_iphone_-19pct_price_hikes_confirmed", "unh_doj_criminal_probe_confirmed", "btc_etf_outflows_-7439btc", "xrp_rlusd_japan_fsa_approved_multisource", "ada_exploit_2.4m_secondfi", "syn_hei_momentum_basket_fresh"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.58,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["realtime_oi_updates", "liquidation_heatmap", "cvd_order_book"],
      "suggested_effect": "advisory_only",
      "facts_used": ["re_negative_funding_-0.003_extreme_oi_+18.4pct", "syn_negative_funding_-0.000222_despite_+19pct_rally_squeeze_fuel", "mega_oi_+7.39pct_fresh_shorts", "pump_oi_+9.41pct_fresh_shorts", "spk_oi_+9.39pct_fresh_positioning", "35_symbols_post_unwind_chop_phase5"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["entry_late", "chase_risk", "price_moved_away"],
      "data_missing": ["tradingview_chart_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["jpm_tp1_343.43_hit_now_340.95_late_to_add", "aave_entry_81_now_85.82_chase_risk_wait_pullback_79-82", "btc_below_60k_extreme_atr_whipsaw_possible", "aapl_recovered_292-299_above_invalidation_28x"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["open_actionable", "entered_unresolved", "needs_review", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["jpm_a_tp_hits_open_actionable", "aave_b_triggered_open_actionable_new", "btc_b_short_tp_hits_open", "aapl_b_short_possibly_moved_away_above_invalidation", "5_crypto_longs_bearish_regime_entered_unresolved", "paper_3_open_20_unresolved_1_needs_review", "unh_c_long_triggered_doj_probe_needs_review"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.77,
      "reason_codes": ["legal_risk", "headline_risk", "correlation_cluster", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["late_us_session_14:39et_2h20min_to_close", "unh_doj_confirmed_legal_risk_avoid_longs", "5_crypto_longs_vs_bearish_regime_reduce", "btc_atr_99th_pct_extreme_vol_whipsaw", "mega_pump_re_squeeze_risk_on_shorts", "stocks_c_tier_pf0.64_losing_bucket_avoid"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_b_wr18.66_pf1.26_+14r_declining_1_new_loss", "crypto_scalp_wr0_pf0_7_losses_failing", "crypto_intraday_wr37.8_pf2.05_+18r_working", "stocks_b_wr27.78_pf1.11_+1r_weak_conf_n19", "stocks_a_wr100_pf_inf_+1r_n1", "stocks_c_pf0.64_losing", "no_catalyst_intraday_14d_wr23_pf0.70_-3r"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.75,
      "preferred_side": "catalyst_backed",
      "best_long": "AAVE — pullback to $79-82; catalyst confirmed dual-layer; counter-tape = reduce size",
      "best_short": "BTC — relief bounce to $61-62K then failed retest; do not short into flush",
      "best_catalyst": "AAVE — Standard Chartered $180 + AWW 100% revenue-to-treasury = strongest catalyst today",
      "avoid": "UNH (DOJ probe), AAPL short (above invalidation), no-catalyst crypto longs (bearish regime)",
      "operator_action": "manual_review",
      "suggested_effect": "advisory_only"
    }
  ]
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|------------|--------------|-----------------|
| data_quality | **ok** | 0.88 | scheduler_fresh, report_stale (swing 4.6h) | advisory_only |
| market_regime | **caution** | 0.82 | risk_off (crypto), chop (stocks), shorts_preferred | advisory_only |
| catalyst_narrative | **ok** | 0.83 | fresh_catalyst, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | **caution** | 0.58 | squeeze_risk (RE/MEGA/PUMP/SYN), data_unavailable | advisory_only |
| technical_entry | **caution** | 0.72 | entry_late (JPM), chase_risk (AAVE), price_moved_away (AAPL) | advisory_only |
| execution_lifecycle | **caution** | 0.80 | open_actionable (JPM/AAVE/BTC), entered_unresolved (5 longs), needs_review (UNH/AAPL) | advisory_only |
| risk_manager | **caution** | 0.77 | legal_risk (UNH), reduce_risk (crypto longs), manual_review | advisory_only |
| playbook_performance | **caution** | 0.65 | playbook_working (intraday), playbook_failing (scalp), low_sample (stocks B) | advisory_only |
| **head_trader** | **caution** | **0.75** | catalyst_backed long (AAVE pullback), regime-aligned short (BTC bounce) | advisory_only |

---

## 4. What Changed vs Previous Review (18:39 EEST)

| Item | 18:39 State | 21:39 State | Delta |
|------|-------------|-------------|-------|
| **JPM A long** | Near TP1 ($340.95), TP1 at $343.43 | TP1 HIT — day high $343.45; now $340.95 | ✅ CONFIRMED WIN |
| **AAPL B short** | Confirmed triggered, $278 region | Recovered to $292-299; above invalidation ~$28x | ⚠️ POSSIBLE INVALIDATION |
| **BTC** | ~$61K, multi-year lows | $59,334 (–2.7% on day); below $60K | ❌ LOWER, bearish confirmed |
| **ETH** | $1,535 | $1,561 (slight relief) | ↔️ FLAT |
| **AAVE** | C-tier watchlist only | **B-tier triggered** — Standard Chartered + AWW catalyst | 🆕 MAJOR UPGRADE |
| **AMD B long** | Waiting for entry | Waiting — AMD ~$523-529 entry zone | ↔️ UNCHANGED |
| **BTC swing short** | OPEN actionable | OPEN actionable, tp_hits | ✅ IN PLAY |
| **MEGA B swing short** | Active | tp_hits (OI expanding, shorts pressing) | ✅ WORKING |
| **NEAR B intraday short** | Active | tp_hits (regime-aligned) | ✅ WORKING |
| **SYN momentum basket** | Fresh <1h | Still in momentum_breakout basket | ↔️ PERSISTS |
| **Crypto B WR/PF** | WR 18.9%, PF 1.29, +15R | WR 18.66%, PF 1.26, +14R | ↘️ 1 new loss |
| **Stocks B WR/PF** | WR 25%, PF 1.25, +2R | WR 27.78%, PF 1.11, +1R | ↘️ mixed (more triggered) |
| **UNH legal** | DOJ probe confirmed | C-tier longs still in DB | ⚠️ NEEDS OPERATOR REVIEW |

**New catalysts since 18:39:** AAVE Standard Chartered initiation (confirmed primary source + FXStreet). BTC acceleration below $60K ($59,334 confirmed Yahoo Finance). XRP RLUSD Japan FSA launch confirmed (multi-source).

---

## 5. Catalyst Coverage

- **Total events today:** 952 (across all cycles, latest cycle scan 19:29 → events=500)
- **Baskets active:** 6 (momentum_breakout, binance_ecosystem_teaser, ai_narrative, perps_dex_narrative, delisting_thin_liquidity + 1 unnamed)
- **Rejected_missing=0** → strong mapping, no processing failures
- **Catalyst mapping quality:** NORMAL — no weak-mapping warning needed
- **Fresh baskets (<1h at review time):**
  - `momentum_breakout` — SYN/HEI, fresh <1h, `wait_pullback`
  - `binance_ecosystem_teaser` — BNB, fresh <1h, `related_beta_rotation`
- **Notable risk events confirmed:** UNH DOJ criminal probe (legal_risk), ADA exploit $2.4M SecondFi (security_exploit), Bybit $2B hack basket (macro context)
- **New since 18:39:** AAVE Standard Chartered initiation + AWW framework (institutional), XRP RLUSD Japan FSA regulatory approval (regulatory_positive)
- **No weak catalyst coverage warning.** Mapping is strong.

---

## 6. Market Landscape

### Market Mood / Risk Routing

**Crypto mood: `risk-off`**
BTC at $59,334 (15:37 EEST; likely lower by 21:39). Below $60K multi-year support — confirmed bearish signal. ETH $1,561 downtrend (-6.7% 24h). Altcoin breadth above EMA20: 20.45% (only 1 in 5 alts above trend). BTC ATR at 99th percentile = extreme vol. ETF outflows: -7,439 BTC / -21,234 ETH (1D). Macro risk score: 51/100 (risk-off tilt). Headlines: "$1B loss triggered below $60K," "$427M long liquidations."

**Stocks mood: `chop`**
VIX 18.93. SPY/QQQ in range. IWM/DIA uptrend (small-cap/value outperforming). Breadth above EMA20: 50% (neutral). Strongest sectors: semiconductors (SMH +9.53% RS), industrials (XLI +7.79%), healthcare (XLV +6.91%). Weakest: communications (XLC -6.96%), consumer_disc (XLY -4.32%), energy (XLE -2.70%). 2h 20min to US close — this is management territory, not fresh-entry territory.

**Preferred side:**
- Crypto: **Shorts** (regime-aligned) or **catalyst-backed isolated longs** (AAVE only, pullback only)
- Stocks: **Catalyst-backed B-tier** (JPM managing / AMD watching). No blanket direction — chop requires selectivity.

**Do NOT default to no-trade:** Route to management decisions. Existing positions need trail-stop management. AAVE pullback is a real action item.

**What would change the view:**
- BTC reclaim above $62K on volume → regime shift → crypto neutral
- JPM/XLF sector breakdown → stocks bearish flip
- AAVE below $77 → invalidate long thesis
- VIX spike above 25 → risk-off in stocks too

---

## 7. Candidate Deep Dives

### 7.1 — JPM (Stocks A-tier intraday long) — LIFECYCLE: TP1 HIT

**Signal:** A-tier intraday long, OPEN actionable, tp_hits. Score 74.11 (B in report; A-tier per active-signals CLI).
**Entry zone:** $334.62–$335.97. Day range today: $334.76–$343.45. TP1: $343.43 → **CONFIRMED HIT** (day high $343.45). TP2: $342.71. TP3: $346.75. Invalidation: close below $331.92.

**Catalyst verified:** (1) JPMorgan names Doug Petno and Troy Rohrbaugh co-presidents, Marianne Lake exits — leadership succession signals stability. (2) "$50B buyback" (per prior session data). (3) Financials sector leading today (XLF), IWM uptrend supporting small-cap/value rotation.
Source: "Stock Market Today: Indexes Mixed; Financials Lead As JPMorgan Tops Buy Point" (Yahoo Finance, 2026-06-25).

**Late-session action:**
- Trail stop to breakeven (~$335-336) or to just above TP1 zone ($342) depending on position size.
- Do NOT add new exposure at $340.95 — 2h 20min to close, risk/reward for new entry is poor (chasing).
- Watch for EOD fade — large-caps often give back intraday gains in the last 30 minutes.
- If price tests $342 and holds → potential hold into Friday for TP3 ($346.75). If price fades below $338 → tighten to breakeven.

**Regime alignment:** ✅ YES — stocks chop with financials leading, IWM/DIA uptrend. Catalyst-backed, not a blind regime bet.

---

### 7.2 — AAVE (Crypto B-tier intraday long) — LIFECYCLE: TRIGGERED, OPEN ACTIONABLE

**Signal:** B-tier intraday long, triggered at ~$81 entry zone. Score: 57–81 (lower in reports due to bearish regime penalty, higher in active-signals CLI).
**Entry zone:** $79.23–$80.37. Current price: ~$85.82 (+8% on day). Invalidation: 1h close below $77.83.

**Catalyst — DUAL-LAYER, CONFIRMED:**
1. **Standard Chartered Bank** initiated AAVE coverage with $180 target by YE-2026. Institutional DeFi narrative entering. Source: bitcoinist.com (2026-06-25).
2. **"Aave Will Win" (AWW) framework:** 100% of all Aave protocol revenue (core protocol + Aave Pro + Aave App + Horizon RWA) flows directly to the DAO treasury, converting AAVE from a governance token into a cash-flow asset. Protocol generated $140M revenue in 2025. Source: FXStreet (2026-06-25).
3. USDT deposits flowing back into Aave (on-chain confirmation per FXStreet article).
4. CoinDesk 20 index showing AAVE gaining 10.1%.

**Is this a chase?** At $85.82 vs entry zone $79-80, current price is +7.3% above entry = ~2.3 ATR from zone. YES, chasing at $85+ is not recommended for new positions.

**What makes it actionable?** Pullback to $82–84 = acceptable secondary entry zone. Pullback to $79–80 = high-confidence entry (original zone). Volume on the pullback matters — a low-volume fade to $82 is more reliable than a high-volume dump.

**Derivatives:** OI +3.89% with price up = fresh positioning (genuine buying, not a short squeeze). Funding neutral (+4.0e-5) — not overheated.

**Regime headwind:** BTC at $59K and falling creates macro headwind. AAVE has isolated catalyst that does NOT depend on BTC direction (institutional DeFi + DAO revenue model), but in a systemic risk-off move, all alts fall. Reduce size vs normal B-tier.

**Existing position (entered ~$81):** Hold. Trail stop to entry zone ($79.83). Partial close at $85+ is reasonable if uncomfortable overnight in extreme ATR environment.

**Verdict:** HOLD existing. NEW entry only on pullback to $79-84. Do NOT chase at $85+.

---

### 7.3 — BTC (Crypto B-tier swing short) — LIFECYCLE: OPEN ACTIONABLE, TP HITS

**Signal:** B-tier swing short, OPEN actionable, tp_hits ongoing.
**BTC price:** $59,334 (15:37 EEST); likely $58-60K range at 21:39 EEST.

**Bearish thesis confirmed:**
- BTC crossed below $60,000 for the first time in the 2026 decline — multi-year support violated
- ETF outflows: -7,439 BTC ($441.88M) in 1 day; -12,619 BTC ($749.58M) in 7 days (Lookonchain confirmed)
- Whale long liquidations: 809.9 BTC long ($47.68M) and 27.92M XRP long wiped this session
- Matrixport-linked whale -$92.5M on ETH + BTC positions
- ATR at 99th percentile = extreme volatility in both directions
- Macro risk score 51/100, headlines confirm institutional selling

**Is this a new-entry setup?** NO — existing short is working. New short at $59,334 into a flush is a chase. Adds into a momentum run create squeeze risk on relief.

**Cleanest new-short entry:** Relief bounce to $61-62K (prior $60K support → potential resistance). Wait for 1h close back below $60.5K as failed retest confirmation. This could come in next 2-4 hours or Asia session.

**ATR risk:** 99th percentile ATR means BTC can swing $2-4K in hours. A relief bounce to $62K before next leg down is statistically likely. Shorts entered at $59K could see -$3K adverse move before resuming.

**Late-session action:** Trail stop on existing short. Do not add at $59K. Monitor $61-62K for re-entry opportunity.

**Regime alignment:** ✅ YES — crypto risk-off confirmed. This is the core regime trade.

---

### 7.4 — AAPL (Stocks B-tier intraday short) — LIFECYCLE: NEEDS REVIEW / POSSIBLE NO-ENTRY

**Signal:** AAPL B-tier intraday short, triggered. Score 67 (B in active-signals CLI, C at 56.94 in latest stocks report).
**Entry zone (from signal):** approximately $27x. Invalidation: approximately $28x.

**Current situation:**
- AAPL day range today: $292.94–$299.70 (Yahoo Finance confirmed at 21:39)
- AAPL open: $295.36
- Current price: approximately $292-$299 range

**Assessment:** AAPL at $292-$299 is ABOVE the estimated invalidation level (~$28x). The signal's entry zone (~$274-$278) and invalidation (~$280-$285) are both well below current price. The B short was triggered on AAPL's initial decline, which included: iPhone China sales -19% YoY, -5.1% intraday decline, iPad/Mac price hikes. AAPL recovered significantly through the session.

**Late-session assessment:** This signal is **NO-ENTRY/MOVED-AWAY**. If an operator entered at the entry zone ($274-278), the position would now be stopped out (above invalidation). If not yet entered, the entry zone no longer exists — do NOT enter AAPL short at $292-299.

The 21:15 stocks report shows AAPL as C-tier short (score 56.94) — a demotion from the B-tier trigger status — consistent with price recovery invalidating the setup.

**Action:** Mark for NEEDS REVIEW. Check whether the tracking pass recorded a stop/invalidation. Do NOT re-enter.

**Note for §14:** AAPL B short tracking gap flagged.

---

### 7.5 — UNH (Stocks C-tier longs) — LIFECYCLE: TRIGGERED → LEGAL RISK OVERRIDE

**Signal:** UNH C-tier intraday long AND C-tier swing long, both triggered (active-signals CLI shows `wa-` and `tr-` status). Scores 59–65.

**LEGAL RISK — CONFIRMED:** DOJ criminal probe on Medicare Advantage fraud (UnitedHealth Group). Expanded to include Optum Rx operations. Source: catalyst JSONL today ("UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16%"). Prior session: UNH -~20%.

**Assessment:** The legal_risk event was present in today's catalyst JSONL but the signal scores (59-65) do not reflect a criminal probe penalty. Scores appear to have been generated before the DOJ news was fully integrated — or the legal event was not routed into the scoring penalty.

**Verdict:** **AVOID / MANUAL REVIEW REQUIRED.** Do NOT act on any UNH long signals. Legal risk overrides any technical score. C-tier is not Telegram-actionable anyway, but the lifecycle status should be updated to NEEDS REVIEW / AVOID by the operator.

**What would make UNH actionable again?** DOJ probe formally dropped or settled. CMS legal clarity. Unlikely intra-week.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Side | Tier | Status | Action | Trigger |
|------|--------|------|------|--------|--------|---------|
| 1 | **AAVE** | Long | B | OPEN actionable (triggered) | Hold existing; NEW entry only on pullback $79-84 | Catalyst confirmed; wait consolidation/dip |
| 2 | **BTC** | Short | B | OPEN actionable (tp_hits) | Hold/trail; NO new short into flush | Relief bounce to $61-62K → failed retest |
| 3 | **JPM** | Long | A | OPEN actionable (tp_hits ✅) | Trail stop to BE; manage TP2/TP3 | EOD hold with trail |
| 4 | **MEGA** | Short | B | OPEN actionable (tp_hits) | Hold with squeeze awareness | Do not add; OI expanding |
| 5 | **NEAR** | Short | B | OPEN actionable (tp_hits) | Hold; regime-aligned | Trail stop |

**Best long-watch (no clean entry now):** AAVE pullback to $79-82.
**Best short-watch:** BTC relief bounce to $61-62K.
**Best catalyst-watch:** AAVE (strongest catalyst today — Standard Chartered + AWW framework, multi-day thesis).

---

## 9. Avoid / No Trade (This Decision Window)

**This window (21:39 EEST — US late session → Asia pre-open):**

- **UNH all longs:** DOJ criminal probe confirmed. AVOID. Legal risk overrides all scores.
- **AAPL B short:** Above invalidation. NO-ENTRY/MOVED-AWAY. Do not re-enter at $292-$299.
- **No-catalyst intraday crypto (bearish trend):** Known failing playbook — 14d WR 23%, PF 0.70, -3R. WLD/POL/CELO/SAHARA/ALLO without verified catalyst = avoid.
- **Counter-tape crypto longs (without isolated catalyst):** HOT/ETH/AXS/FIL/WLD swing longs in active-signals are ENTERED UNRESOLVED positions needing review — not addition candidates.
- **AAVE above $85+:** Chase risk. Wait for pullback.
- **ADA:** Wallet exploit hack confirmed, $2.4M SecondFi. Avoid.
- **New intraday entries after 22:30 EEST (3:30 PM ET):** Late-session intraday entries have poor time-value.
- **Stocks C-tier:** PF 0.64, -12R on 230 samples. Not Telegram-actionable.

_Scanning continues. "No new entry" ≠ "stop scanning." The above is a routing decision for this 4-hour window only._

---

## 10. Main Risks

1. **BTC extreme ATR whipsaw:** ATR at 99th percentile. Relief bounce of $2-4K is likely before next leg. Shorts entered below $60K could see adverse $3K+ temporary move.
2. **5 crypto longs in bearish regime:** HOT/ETH/AXS/FIL/WLD B-tier swing longs active while BTC is at $59K and declining. These 5 positions need immediate stop-integrity review. Are their stops valid relative to current BTC pricing?
3. **UNH legal spillover:** DOJ probe in managed care could affect broader XLV/healthcare signals. Monitor XLV and LLY for sympathy moves.
4. **AAPL late recovery stops:** If AAPL B short was entered at $274-278 and hit $299 today, that's a ~-8% loss. Check whether stops were executed and lifecycle status was updated.
5. **AAVE squeeze after AWW news:** Current OI data shows neutral. But if shorts have been building against the rally, AWW announcement could trigger a short squeeze. Existing longs benefit. New shorts at this level = high risk.
6. **EOD institutional rebalancing (22:30-23:00 EEST / 3:30-4PM ET):** Last 30 minutes of RTH often see sharp flush or ramp on institutional rebalancing. Do not initiate new positions in this window.
7. **Social attention gap:** Reddit/social/KOL feeds unavailable. Market sentiment/crowd positioning unknown.
8. **Onchain data absent:** config/onchain.yaml missing. No whale flow confirmation available for crypto candidates.

---

## 11. Action Plan — Next 4 Hours (21:39–01:39 EEST)

### 21:39–23:00 EEST (US late session — 2h 20min to close):
1. **JPM A:** Trail stop to $335-336 (breakeven). If JPM holds $342, consider holding through Friday for TP3 ($346.75). If JPM fades below $338, tighten to $337.
2. **AAVE B:** Hold existing position (entered ~$81). No new entries above $85. If pulls back to $82-84, monitor for secondary entry with reduced size.
3. **BTC short:** Let trail run. Do not add at $59K. Watch $61-62K for re-entry setup (post-bounce fade).
4. **MEGA/NEAR shorts:** Hold with trail stops. OI expanding on MEGA — squeeze guard active.
5. **AAPL:** Mark as NEEDS REVIEW. Verify stop status. Do not re-enter.
6. **UNH:** Flag all signals as MANUAL REVIEW REQUIRED. Legal risk override.
7. **AMD B:** Still WAITING. Late session timing (2h 20min to close) makes intraday trigger challenging. Re-evaluate Friday.
8. **5 crypto longs (HOT/ETH/AXS/FIL/WLD):** Review each stop level against current BTC pricing ($59K). If any stop is stale/too wide, tighten manually.

### 23:00–01:39 EEST (US close → Asia pre-open):
1. **BTC close below $60K confirmation:** If confirmed at daily close → bearish regime deepens. Asia session short setups on bounces.
2. **AAVE overnight:** Tighten stop to entry zone ($79-80) if holding overnight. 99th percentile ATR overnight = wide swings.
3. **XRP/RLUSD:** Japan FSA approval confirmed. Watch for Asia-session reaction. Potential overnight catalyst-watch (no active signal currently — carry-forward watchlist).
4. **SYN/HEI momentum:** Both in momentum_breakout basket. Monitor for follow-through or fade into Asia.
5. **SPK:** OI +9.39% with price up = fresh positioning. Watch for continuation.

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Notes |
|------|-------|---------|-------|
| **Scalp** | Crypto | ❌ AVOID | Net-negative (WR ~0%, PF ~0 recent). No A/B scalp active. Extreme ATR = whipsaw kills scalps. |
| **Intraday** | Crypto | ⚠️ CATALYST-BACKED ONLY | AAVE B triggered (confirmed catalyst). No other clean crypto intraday active. Avoid no-catalyst. |
| **Swing** | Crypto | ⚠️ MANAGE EXISTING | BTC short working. 5 longs need stop review. No new longs vs bearish trend. |
| **Intraday** | Stocks | ✅ SELECTIVE, MANAGE | JPM A TP1 hit → manage trail. AMD B waiting. AAPL B review needed. Late session = manage only. |
| **Swing** | Stocks | ⚠️ CARRY-FORWARD | Stocks swing data 4.3h old. Carry-forward only. No new entries without fresh cycle. |
| **Invest** | Stocks | ⚠️ CARRY-FORWARD | Invest data 4.3h old. Same rule. |

**Overall:** **CAUTION — MANAGE EXISTING, SELECT NEW ONLY ON CATALYST (AAVE PULLBACK)**. No aggressive new entries. Crypto short bias confirmed by regime. Stocks chop = finesse existing wins. Scanning always continues.

---

## 13. Sources

| # | Title | Source | Date | URL | Detected Symbols | Effect |
|---|-------|--------|------|-----|-----------------|--------|
| 1 | Aave Rallies Against Bitcoin As Institutional DeFi Narrative Strengthens | bitcoinist.com | 2026-06-25 | [Link](https://bitcoinist.com/aave-rallies-against-bitcoin-as-institutional-defi-narrative-strengthens/) | AAVE/USDT | Confirms Standard Chartered $180 target |
| 2 | AAVE surges as capital flows return to DeFi | FXStreet | 2026-06-25 | [Link](https://www.fxstreet.com/cryptocurrencies/news/aave-price-forecast-aave-surges-as-capital-flows-return-to-defi-202606250355) | AAVE/USDT | Confirms AWW 100% revenue-to-DAO |
| 3 | Bitcoin tumbles further below $60,000 | Yahoo Finance | 2026-06-25 | [Link](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-june-25-2026-bitcoin-hits-its-lowest-levels-in-years-125308371.html) | BTC/USDT, ETH/USDT | Confirms BTC $59,334, bearish |
| 4 | JPM Stock Quote (Yahoo Finance) | Yahoo Finance | 2026-06-25 | [Link](https://finance.yahoo.com/quote/JPM/) | — | Confirms day range $334.76-$343.45, TP1 hit |
| 5 | AAPL Stock Quote (Yahoo Finance) | Yahoo Finance | 2026-06-25 | [Link](https://finance.yahoo.com/quote/AAPL/) | — | Confirms range $292-$299, above invalidation |

**Internal sources (not ingested):** cycle_06 summary, scalp/intraday/stocks intraday reports, active-signals CLI, signal-stats CLI, catalyst JSONL, LLM packet.

---

## 14. Fix Requests / TODO

### TODO-1: SHIB price/ATR data shows 0.0000
**Issue:** SHIB/USDT displays price=0.0000 and ATR=0.0000 in both the scalp report (2026-06-25_16-49) and intraday report (2026-06-25_17-03). This is a data pipeline bug — SHIB price should be in the $0.000012–$0.000015 range.
**Evidence:** scalp report §RS: `SHIB ... price/ATR: 0.0000 / 0.0000`. Intraday report shows same.
**Suspected cause:** Float formatting for extremely small-magnitude prices (SHIB ~$0.000012) — Python's default float display or round() truncation to 4 decimal places returns 0.0000 instead of using scientific notation or increasing decimal precision.
**Suggested fix:** For symbols where price < 0.001, display with 8 decimal places or use scientific notation in the report formatter. Check `src/reports/` formatters for price/ATR display logic.
**Priority:** Low (cosmetic, not affecting scoring)
**First observed:** 2026-06-25 ~20:03 EEST

### TODO-2: UNH legal_risk → signal scoring gap
**Issue:** UNH C-tier intraday and swing long signals show as "triggered/waiting" in active-signals despite confirmed DOJ criminal probe (legal_risk confirmed in catalyst JSONL today, "UNH Faces DOJ Probe, Shares Dive 16%"). Signal scores 59-65 do not reflect legal disqualification.
**Evidence:** active-signals CLI output at 21:39 shows two UNH longs active. Catalyst JSONL contains legal_risk-tagged entry for UNH.
**Suggested fix:** Post-scoring legal filter: for confirmed DOJ/SEC/criminal probe events, either (a) hard cap signals to "needs_review" tier, or (b) apply -25 to -30 point risk penalty to demote below actionable threshold. Filter should run after standard scoring, before signal promotion.
**Priority:** High (risk management gap — legal events can cause -20%+ moves)
**First observed:** 2026-06-25 21:39 EEST

### TODO-3: AAPL B short stop-tracking gap
**Issue:** AAPL B intraday short shows "triggered" in active-signals CLI at 21:39. However AAPL price today ($292-$299) is well above the signal's estimated invalidation level (~$28x), suggesting the position was stopped out but lifecycle status was not updated to NO-ENTRY/MOVED-AWAY or CLOSED-LOSS.
**Evidence:** active-signals shows AAPL B active. Yahoo Finance confirms $292.94-$299.70 range, above estimated invalidation. Stocks intraday report (21:15) shows AAPL as C-tier only (score 56.94 — demoted from B), consistent with recovery.
**Suggested fix:** Verify that the track-signals pass (step in cycle) correctly compares current close vs invalidation level for signals in "triggered" state. Check whether there is a timing gap between intraday invalidation cross and the next track-signals execution. cycle_06 showed stopped=8 — AAPL may have been one of them, but the CLI still shows it triggered.
**Priority:** Medium (affects lifecycle accuracy and operator trust)
**First observed:** 2026-06-25 21:39 EEST

---

*End of review. Advisory only. No auto-trade. No code changes. Scanning continues.*
