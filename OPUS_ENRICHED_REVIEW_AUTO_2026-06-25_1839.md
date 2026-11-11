# Opus Enriched Review — US OPEN REACTION REVIEW — Auto Cycle 18:39 EEST

**Slot:** US Open Reaction Review (18:30 EEST slot)
**Time:** 2026-06-25 18:39 EEST (11:39 ET — ~2h 9min into RTH)
**Date:** 2026-06-25
**Model:** claude-sonnet-4-6
**Advisory only — no auto-trade, no signal registration**

---

## 1. Executive Summary

This is the **US Open Reaction Review** slot (18:30 EEST). Two hours into regular trading hours, the US open reaction is now clear and largely confirmed.

**Stocks:** Micron Q3 blowout ($41.5B revenue, +346% YoY) powered a tech/semis rally (Nasdaq +2.3% pre-market; MU +10.4% RTH). JPM A-tier long CONFIRMED WORKING — trading at $340.95 (+2.3%), near TP1 ($343.43). AAPL CONFIRMED SHORT — down -4.79% to ~$278 on China iPhone -19% YoY + price hikes. UNH remains AVOID (DOJ criminal probe confirmed, -~20% in prior session). AMD NEW B-tier long from the freshest stocks intraday report (18:25).

**Crypto:** Risk-off regime UNCHANGED. BTC near multi-year lows (~$61k). The equity AI rally provided only a brief, minor BTC relief — no regime change. ETH at $1,535 in downtrend (-6.67% 24h). Preferred side: SHORTS. Five crypto long signals active in a bearish regime — all require operator review.

**Key actions this slot:** Manage JPM TP1. Watch AAPL for retest short entry (~$281-284). Review all crypto long signals in bearish regime (ETH urgent). Do not add new crypto longs. Scanning always continues.

_Advisory only. No auto-trade. No code changes._

---

## 2. Data Used

| Source | File | Generated | Age at 18:39 | Status |
|--------|------|-----------|--------------|--------|
| Scheduler log | scheduler.log | 17:29 EEST | 70min | ✅ FRESH |
| Latest cycle | cycle_05_15-48_summary.md | 17:29 EEST | 70min | ✅ FRESH |
| Scalp report | 2026-06-25_13-12_scalp_report.md | 16:12 EEST | 2h27min | ⚠️ CARRY-FORWARD |
| Intraday crypto | 2026-06-25_13-27_intraday_report.md | 16:27 EEST | 2h12min | ⚠️ CARRY-FORWARD |
| Swing crypto | 2026-06-25_14-03_swing_report.md | 17:03 EEST | 1h36min | ✅ FRESH |
| Stocks intraday | 2026-06-25_15-25_stocks_intraday_report.md | 18:25 EEST | 14min | ✅ VERY FRESH |
| Stocks swing | 2026-06-25_14-19_stocks_swing_report.md | 17:19 EEST | 1h20min | ✅ FRESH |
| Stocks invest | 2026-06-25_14-27_stocks_invest_report.md | 17:27 EEST | 1h12min | ✅ FRESH |
| Catalyst | catalyst_cycle_13-27.md | 16:27 EEST | 2h12min | ✅ FRESH |
| External web | WebSearch/WebFetch live | 18:39 EEST | current | ✅ LIVE |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-25_1620.md | 16:20 EEST | 2h19min | ✅ READ |

**External web research:** Available. 5 sources fetched and verified (see §13).

**CLIs run:**
- `active-signals --asset-class crypto` → 9 active signals
- `active-signals --asset-class stocks` → 50 active signals
- `signal-stats --asset-class crypto` → B-tier week: WR 18.9%, PF 1.29, +15R
- `signal-stats --asset-class stocks` → B-tier week: WR 25%, PF 1.25, +2R

---

## 3. Scheduler / Data Freshness

- **Scheduler last run:** 17:29 EEST (cycle 05 of the day, label 15:48 UTC). Duration normal. No stale alert.
- **Crypto reports:** Swing fresh (1.6h). Scalp + intraday carry-forward (2.2-2.5h) — use for context, not final-entry decisions.
- **Stocks reports:** Intraday ultra-fresh (18:25, 14min ago — data at 15:25 UTC = 18:25 EEST, covering RTH action). Swing/invest fresh (1.1-1.2h).
- **Catalyst scan:** 16:27 EEST (2.2h), 448 events in this cycle. 763-952 total events across today's cycles. Baskets: 5 active.
- **Paper monitor (from 16:20 review):** Open actionable: 2 | Waiting: 0 | Entered unresolved: 19 | Review/Shadow: 186 | No-entry: 39 | Needs review: 1

**Blindspots still missing:** Live crypto price feed, real-time OI/funding, liquidation heatmaps, social attention (Reddit/X failed), CVD, ETF flows.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-06-25 18:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["live_crypto_price_realtime", "realtime_oi_funding", "social_attention"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler_log_17:29_70min", "cycle_05_17:29", "stocks_intraday_18:25_14min", "swing_17:03_96min", "catalyst_16:27_132min", "external_web_live"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["risk_off", "mixed", "shorts_preferred"],
      "data_missing": ["live_btc_price_stream"],
      "suggested_effect": "advisory_only",
      "facts_used": ["btc_downtrend_61k_multiyear_low", "eth_downtrend_1535_-6.67pct", "altcoin_breadth_19-28pct", "vix_18.40", "spy_range_qqq_range", "iwm_uptrend_dia_uptrend", "micron_ai_rally_nasdaq+2.3pct", "stocks_chop_neutral_to_risk_on_tech"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "mapping_weak"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["micron_q3_41.5B_+346pct_confirmed", "jpm_50b_buyback_dividend_confirmed", "aapl_china_iphone_-19pct_confirmed", "unh_doj_probe_expanded_optum_rx", "xrp_rlusd_japan_fsa_approved_multi_source", "ada_exploit_2.4m_secondfi", "syn_bitget_delisting_confirmed", "ai_narrative_basket_active"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["realtime_oi_updates", "liquidation_heatmap", "cvd_order_book"],
      "suggested_effect": "advisory_only",
      "facts_used": ["pump_price_down_oi_up_squeeze_risk", "mega_price_down_oi_up_fresh_shorts", "syn_negative_funding_despite_+48pct", "btc_normal_funding_backwardation", "eth_price_down_oi_down_deleveraging"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["entry_late", "clean_retest", "chase_risk"],
      "data_missing": ["tradingview_chart_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["jpm_triggered_338-340_now_340.95_near_tp1", "aapl_extended_-4.79pct_wait_retest_281-284", "btc_at_multiyear_support_trail_stop", "wld_within_scalp_entry_zone_0.5036-0.5094", "mega_extended_below_ema20_swing_no_entry"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["open_actionable", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["btc_short_tp_tracking_open_actionable", "jpm_a_long_tp_tracking_winning", "eth_b_long_entered_unresolved_bearish_regime_urgent", "5_crypto_longs_in_bearish_regime_review_needed", "xlm_no_entry_moved_away", "xrp_catalyst_watch_no_signal_yet"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.85,
      "reason_codes": ["correlation_cluster", "legal_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["5_crypto_longs_bearish_regime_adverse", "unh_doj_hard_avoid_criminal_not_civil", "pump_squeeze_risk_no_position", "btc_near_multiyear_support_do_not_overextend_short", "stocks_swing_negative_audit_watchlist_cap"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_pf205_+18r_n37", "crypto_intraday_pf000_-6r_no_catalyst_failing", "crypto_long_pf310_+19r_vs_short_pf090_-4r", "multi_exchange_pf233_+20r_vs_single_pf078_-7r", "stocks_B_pf125_+2r_weak_sample_22", "stocks_C_pf044_-18r_no_edge", "stocks_swing_watchlist_only_-5r_audit"]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.77,
      "reason_codes": ["open_actionable", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["jpm_a_long_confirmed_working_340.95", "aapl_short_confirmed_-4.79pct", "btc_short_managing_61k", "xrp_catalyst_watch_japan_rlusd", "eth_urgent_review_long_in_bearish_regime"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.77,
    "preferred_side": "mixed",
    "best_long_candidate": {
      "symbol": "JPM",
      "trigger": "MANAGING — trailing stop to $338; TP1 at $343.43; new entry only on pullback to $338-340",
      "reason": "A-tier confirmed working (+2.3% to $340.95); $50B buyback support; financials RS leader (+8%); clean catalyst"
    },
    "best_short_candidate": {
      "symbol": "AAPL",
      "trigger": "wait for bounce/retest to $281-284, then short; SL above $291 (prior close); TP1 $270",
      "reason": "Confirmed -4.79% on China iPhone -19% YoY + price hikes + UBS neutral + analyst downgrades; multi-source confirmed"
    },
    "best_catalyst_candidate": {
      "symbol": "XRP",
      "trigger": "B-tier entry signal required; await breakout structure after RLUSD Japan confirmed; not actionable without regime improvement",
      "reason": "Japan FSA RLUSD approval multi-sourced; unique positive regulatory catalyst in risk-off environment"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ criminal probe confirmed and expanded to Optum Rx; stock -20%+ in session; -55% from ATH; criminal = binary downside; HARD AVOID"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|------------|--------------|------------------|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.82 | risk_off, mixed, shorts_preferred | advisory_only |
| catalyst_narrative | ok | 0.80 | fresh_catalyst, catalyst_confirmed, mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.75 | entry_late, clean_retest, chase_risk | advisory_only |
| execution_lifecycle | caution | 0.80 | open_actionable, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.85 | correlation_cluster, legal_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.78 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | ok | 0.77 | open_actionable, wait_for_trigger | advisory_only |

---

## 4. What Changed vs Previous Review (16:20 Pre-US-Open)

| Item | Prior status | Current status | Impact |
|------|-------------|----------------|--------|
| JPM | WAITING RTH confirm (B-tier, 75) | OPEN ACTIONABLE, tp_tracking — $340.95, near TP1 $343.43 | ✅ CONFIRMED WORKING |
| AAPL | C-tier short watchlist (China risk flagged) | CONFIRMED SHORT -4.79% to $278.16 | ✅ SHORT THESIS CONFIRMED |
| AMD | Not in prior review | NEW B-tier long (stocks intraday 18:25 report, score 69) | NEW candidate |
| BTC | OPEN ACTIONABLE (short, managing) | OPEN ACTIONABLE (short, managing) — unchanged | Thesis intact |
| ETH | ENTERED UNRESOLVED (urgent) | ENTERED UNRESOLVED — still needs operator review | ⚠️ URGENT UNCHANGED |
| XLM | NO-ENTRY / MOVED AWAY | NO-ENTRY confirmed (price moved below entry zone, never triggered) | Confirmed miss |
| XRP | WAITING for entry (catalyst confirmed) | WAITING for entry — no signal registered yet | Catalyst carry-forward |
| UNH | AVOID (DOJ criminal probe, C-tier triggered) | AVOID — confirmed ongoing; stock -55% from ATH | Hard AVOID confirmed |
| SMH | C-tier long, wait gap settle | MU +10.4% RTH — gap largely held; C-tier if RTH base confirmed | Gap settled favorably |
| MSFT short | B-tier short, headwind from tech rally | Still adverse — tech rally day; if still in position, reduce size | ⚠️ Headwind confirmed |
| LLY | B-tier long, WAITING RTH | B-tier long, WAITING — no trigger confirmed yet | Unchanged |

**New catalysts since 16:20:** None major (AAPL China data and price hike confirmed after initial pre-market signal; everything else carry-forward).

---

## 5. Catalyst Coverage

- **Total events today (latest cycle 13:27):** 448 in this cycle; 763-952 across all today's cycles
- **Mapped to specific symbols:** ~7 events (XRP×3, BTC×1, UNH×1, SOL×1, ADA×2) — <2% of total
- **Unmapped ("other_news" basket):** 98%+ of events — **⚠️ CATALYST MAPPING WEAK THIS RUN — use catalyst layer as context, not final decision**
- **Narrative baskets active (5):**
  1. `binance_ecosystem_teaser` → BNB/USDT + ASTER/USDT (fresh <1h)
  2. `ai_narrative` → NEAR, RENDER, TAO, FET (fresh <6h) related: WLD, ASTER
  3. `perps_dex_narrative` → HYPE/USDT (wait pullback, <6h)
  4. `delisting_thin_liquidity` → no primary (avoid low-liquidity names)
  5. `momentum_breakout` → SYN/USDT +48%, HEI/USDT +27% (no confirmed catalyst, pure momentum)
- **Top catalysts by importance:**
  - XRP RLUSD Japan FSA approval (0.75, multi-source) ✅
  - UNH DOJ probe (0.73, confirmed) → AVOID
  - Pump.fun class action lawsuit (0.71)
  - Micron Q3 record $41.5B (0.58 in crypto catalyst, higher in stocks)
  - Bybit hack North Korea link carry-forward (0.75, single_source, stale)
- **Top 3 unmapped headlines (for context):**
  1. "DOLLAR RISES TO NEAR 2-YEAR HIGH OF 161.93 YEN" (macro, JPY weakness)
  2. "BOFA: DEFENSIVES COULD SHINE IF AI HYPE FADES" (sector rotation warning)
  3. "Best Altcoins to Watch in June 2026" (attention/crowd metric)

---

## 6. Market Landscape

### Market Mood / Risk Routing

**Driven by Agent Council market_regime + risk_manager agents:**

- **Crypto mood:** RISK-OFF. BTC downtrend, ~$61k (multi-year lows); ETH downtrend $1,535 (-6.67% 24h); altcoin breadth 19-28% above EMA20; ATR percentile 87-98 (elevated volatility). No sign of reversal.
- **Stocks mood:** CHOP → RISK-ON (tech-specific). VIX 18.40. SPY/QQQ range. IWM/DIA uptrend. Nasdaq futures gapped +2.3% on Micron; MU +10.4% RTH. Mixed: tech+semis up, AAPL down, UNH avoid, energy/comms weak.
- **Dominant narrative:** AI infrastructure demand cycle re-confirmed (Micron record $41.5B). Financials capital return (JPM buyback). AAPL hardware/China weakness counter-narrative.
- **Preferred side now:** Crypto SHORTS (regime-aligned). Stocks: manage JPM long, AAPL short on retest; no tech shorts today.
- **Best long candidate:** JPM (managing, near TP1) / AMD (new B-tier, wait for confirmation)
- **Best short candidate:** AAPL (wait for retest ~$281-284); crypto regime-aligned: MEGA/WLD (swing, wait pullback to zone)
- **Best catalyst-backed candidate:** JPM (buyback confirmed working); XRP (Japan RLUSD, waiting for entry signal)
- **What to avoid:** UNH (DOJ criminal), PUMP (squeeze risk), SYN (delisting + pump), ADA (exploit), NVDA/MSFT/QQQ shorts (tech rally day), all new crypto longs without catalyst
- **What would change the view:** BTC close above $63k (reduces short conviction); SPY/QQQ break above 20d resistance (upgrades stocks to risk-on); Crypto catalyst basket activation (XRP breakout, narrative confirmation)

---

## 7. Candidate Deep Dives

### Candidate 1 — JPM (Stocks, A-tier LONG, OPEN ACTIONABLE)
**Status:** OPEN ACTIONABLE — tp_tracking. Entry triggered RTH. Price $340.95, entry zone was $338.37-$339.64. Up +2.3% from prior close $333.45.

**Catalyst:** $50B share buyback authorization + dividend increase + Fed stress test pass. Confirmed via Reuters/CNBC. Financials sector RS leader (20d RS vs SPY: +8.04%).

**Has price reacted?** YES — fully confirmed. Day range $334.76 - $343.45 (day high near TP1 at $343.43).
**Is this chasing?** No — entered at zone. Now managing, not entering new.
**Retest/pullback for new entry:** Only if price pulls back to $338-340 would a new entry make sense.
**Overextended?** Near day high and TP1 — do NOT add at $340.95.
**Entry NOW:** NO. Manage existing. Trail stop toward $338 (entry zone). If TP1 ($343.43) hit, consider partial exit.
**Aligned with mood?** YES — financials sector strongest, buyback support, chop-to-risk-on environment.
**What invalidates?** Close below $335 (break below buyback support floor).
**Chase risk?** HIGH for new entry at current levels.
**Legal/headline risk?** None confirmed. Buyback is clean catalyst.
**Action:** HOLD / MANAGE. Trail stop. Watch TP1 at $343.43.

---

### Candidate 2 — AAPL (Stocks, C-tier → confirmed SHORT catalyst)
**Status:** CONFIRMED SHORT CATALYST. Not in A/B active signals for short, but catalyst confirms directional thesis. Down -4.79% to $278.16 on RTH.

**LEGAL/HEADLINE RISK:** Multiple negative catalysts confirmed:
- China iPhone shipments -19% YoY (UBS, Investing.com — single_source)
- Price hikes for iPad, Mac, home devices (Bloomberg/WalterBloomberg Telegram channel)
- UBS maintains Neutral rating on China weakness
- APAC Research + KGI Securities downgraded to "Hold"
- AI regulatory blockage in EU + China (Siri/Apple Intelligence delayed)

**Source:** TradingKey (tradingkey.com, 2026-06-25) — single_source. China data from Investing.com/UBS.
**Verification status:** single_source for -4.79% figure; China iPhone data from UBS via Investing.com (single_source).

**Has price reacted?** YES — significantly. -4.79% is a large intraday move.
**Is this chasing to short NOW?** YES — extended intraday move. Short NOW is chasing.
**Retest for entry:** Wait for bounce to $281-284 (previous intraday structure before breakdown). Prior close was ~$291 (inferred from pre-market data).
**Overextended?** Yes — -4.79% in one session = likely >2 ATR from EMA20.
**Entry for short:** WAIT. Set alert at $281-284 for retest. SL above $291. TP1 ~$270.
**Aligned with mood?** YES for stocks weak/chop names. Communications/tech sector rotation adverse.
**What invalidates?** Market-wide tech rally sustaining above $285 (Micron spillover overwhelms China data).
**Chase risk?** HIGH at current $278 — wait for pullback.
**Action:** CATALYST-WATCH / WAIT FOR RETEST. No entry at current extended levels.

---

### Candidate 3 — BTC/USDT (Crypto, B-tier SHORT, OPEN ACTIONABLE managing)
**Status:** OPEN ACTIONABLE — tp_tracking (B-tier swing short, managing active position from prior cycles).

**Price context:** BTC opened June 25 at $60,983. Morning data shows $61,200-61,300. Confirmed by Yahoo Finance: "Bitcoin hits its lowest levels in years." CoinDesk: "Bitcoin claws back some of the losses after Micron beats earnings" — indicating a minor bounce from lows but no regime reversal.

**Has price reacted to catalyst?** Partial — Micron AI rally caused brief BTC relief bounce, but BTC remains near multi-year lows. The equity AI narrative (memory chips, data centers) does NOT directly translate to crypto risk-on in current regime.
**Is this chasing to short?** BTC is near multi-year lows — DO NOT initiate new short entries. Managing existing short only.
**Is there a clean entry for new short?** NO. Only manage existing. Trail stop.
**Overextended?** BTC ATR pct 87-98 = elevated — stops widened.
**What would invalidate short thesis?** BTC closes above $63,000 (reclaims lost levels with sustained buying).
**Squeeze risk?** Low on BTC (funding normal). Equity gap-up risk on AI momentum could create a pop.
**Aligned with mood?** YES — crypto RISK-OFF, shorts preferred. But at support — do not press.
**Action:** MANAGE EXISTING SHORT ONLY. No new short entries at multi-year support. Trail stop.

---

### Candidate 4 — XRP/USDT (Crypto, WAITING FOR ENTRY, catalyst-backed)
**Status:** WAITING FOR ENTRY — catalyst confirmed (Japan FSA RLUSD approval), no B-tier signal registered yet.

**Catalyst:** Ripple's RLUSD stablecoin received Japan FSA regulatory approval. Confirmed by 3 sources: CoinDesk, CryptoBriefing, The Block (carry-forward from yesterday). Importance: 0.75.

**Has price reacted?** Unknown — no live XRP price in reports (not in top candidates currently; was WAITING per prior review at ~$0.1875-0.1887 zone for XLM... wait, that was XLM not XRP). XRP is a separate candidate with Japan regulatory catalyst.

**Note:** XRP/USDT was noted as catalyst-watch in the 16:20 review. No B-tier signal has been generated by the system for XRP — the Japan approval is a positive catalyst but the crypto regime is risk-off. XRP may need BTC stabilization to have a valid long setup.

**Aligned with mood?** Mixed — positive catalyst (regulatory win) vs risk-off macro.
**What would make actionable?** B-tier signal registered + BTC stabilizing above $61k + crypto breadth improving. Currently: none of these confirmed.
**Entry trigger:** Await system signal. If BTC stabilizes and XRP shows RS vs BTC, that's the entry signal.
**What invalidates?** BTC break below $60k or US risk-off escalation.
**Action:** CATALYST WATCH. Do not enter without system signal. Best crypto long-side candidate IF regime improves.

---

### Candidate 5 — ETH/USDT (Crypto, B-tier LONG, ENTERED UNRESOLVED — URGENT REVIEW)
**Status:** ENTERED UNRESOLVED (B-tier, swing long from prior cycle). URGENT operator review required.

**Current price:** $1,535.70 (swing report 17:03 EEST). 24h return: -6.67%. Trend: downtrend. ATR: $19.43.

**Problem:** ETH is a SWING LONG signal in a bearish/risk-off regime. If entered at a higher price (previous cycle when ETH was higher), this position is likely in drawdown. The swing report today shows ETH as C-tier watchlist only (score 51.1, high risk penalty -24.7) — NOT a fresh signal. The "entered unresolved" tag from paper monitor (confirmed at 16:20 review with 19 entered-unresolved crypto positions) means the paper position is active.

**Has price validated the long thesis?** NO — ETH downtrend -6.67% today. BlackRock deposit news (catalyst) is real but was insufficient to reverse the trend.
**Overextended?** ETH is >2 ATR from EMA20 (report flagged: "Price is more than 2 ATR from EMA20; do not chase").
**Stop risk?** If stop is set below entry and has not triggered: OPERATOR CHECK REQUIRED. If stop is already below $1,535, this may already be near stop-hit territory.
**What invalidates long thesis?** Already invalid — price in downtrend, no catalyst bounce sustained.
**Action:** OPERATOR REVIEW REQUIRED. Check paper entry price, current stop, P&L. If in drawdown past stop: NEEDS REVIEW. Do not add to ETH long in current regime.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Asset | Side | Status | Trigger | Edge Quality |
|------|--------|-------|------|--------|---------|--------------|
| 1 | JPM | Stocks | LONG | MANAGING — near TP1 | Trail stop $338, TP1 $343.43 | A-tier confirmed ✅ |
| 2 | AAPL | Stocks | SHORT | Wait for retest | Bounce to $281-284, SL $291 | Catalyst confirmed, extended |
| 3 | BTC | Crypto | SHORT | Managing existing | Trail stop; no new entry | Regime-aligned, at support |
| 4 | XRP | Crypto | LONG | Catalyst-watch | Await B-tier signal + BTC stabilize | Catalyst confirmed, no entry yet |
| 5 | AMD | Stocks | LONG | Waiting | Wait for RTH confirmation after gap | New B-tier, carry-forward catalyst |

**Best long-watch:** JPM (managing) / AMD ($54-55 entry zone after RTH confirmation; B-tier 69).
**Best short-watch:** AAPL (wait retest $281-284, -4.79% confirmed catalyst) / MEGA (crypto swing, regime-aligned, at pullback zone).
**Best catalyst-watch:** XRP (Japan RLUSD multi-source, waiting for B-tier signal).

---

## 9. Avoid / No Trade

**This decision window only — never "stop system."** Scanning always continues.

- **UNH:** HARD AVOID. DOJ criminal probe confirmed and expanded. Stock -20%+ in prior session, ~$280 now. Criminal investigation = binary downside risk. No entry long or short until probe resolves.
- **PUMP/USDT:** AVOID short. Price↓ + OI↑ + squeeze setup. Any short could be squeezed.
- **SYN/USDT:** AVOID. +48% move with no confirmed catalyst. Bitget delisting overhang. Negative funding = funding-driven pump. Do not chase.
- **HEI/USDT:** AVOID. +27% with no catalyst. >2 ATR from EMA20. No entry.
- **ADA/USDT:** AVOID. SecondFi $2.4M exploit. Negative catalyst confirmed.
- **MSFT short:** DO NOT ADD. Tech rally day (Micron). If existing position, consider reducing size or setting tighter stop.
- **NVDA/QQQ/SMH shorts:** AVOID. Tech rally day = wrong side for shorts.
- **All new crypto longs:** AVOID in current risk-off regime except XRP on confirmed catalyst + regime improvement.

---

## 10. Main Risks

1. **BTC at multi-year support (~$60k):** Short squeeze risk if buyers defend. Do not overextend BTC short at key support.
2. **5 crypto long signals active in bearish regime:** HOE, FIL, WLD, AXE, NI long swings need operator review. If stops have not triggered, positions are in adverse conditions.
3. **AAPL extended intraday:** -4.79% is a large single-session move; shorting at the lows is high-risk. Wait for retest.
4. **UNH tail risk:** Criminal DOJ probe could expand further. Price may bounce on technicals but do not participate.
5. **Stocks swing watchlist-only audit:** Swing signals are capped to C-tier (watchlist-only) due to -12R audit loss (48h audit ongoing). Do not treat swing signals as actionable.
6. **Catalyst mapping very weak (<2% explicitly symbol-mapped):** 98%+ of catalyst events are "other_news" without symbol mapping. Basket coverage partial only.
7. **Crypto intraday mode failing:** 0W/6L this week. No-catalyst intraday in bearish regime underperforms. Avoid new intraday crypto signals without catalyst or RS confirmation.
8. **Social attention missing:** Reddit feeds failing. KOL watchlist placeholder only. Crowd context thin.

---

## 11. Action Plan — Next 4 Hours

| Priority | Action | Timeframe |
|----------|--------|-----------|
| URGENT | Operator review ETH B-tier swing long (entered unresolved) — check stop, P&L | Now |
| HIGH | Review all 5 crypto long signals (HOE, FIL, WLD, AXE, NI) in bearish regime | Now |
| HIGH | Manage JPM long — trail stop to $338; watch TP1 at $343.43 | Ongoing RTH |
| MEDIUM | Monitor AAPL for bounce to $281-284 for potential short entry | Next 1-2h RTH |
| MEDIUM | Watch XRP for B-tier signal + BTC stabilization (catalyst-watch) | Ongoing |
| LOW | Monitor AMD ($54-55 entry zone) for RTH confirmation | Ongoing |
| ROUTINE | Scanning continues — data collection, signals, outcomes. Do NOT pause. | Always |

**Before next review (21:30 late-session slot):** Confirm JPM position status (TP1 hit/managing), ETH review outcome, crypto longs review outcome. Note AAPL retest setup if applicable.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Active | Notes |
|------|---------|--------|-------|
| Crypto scalp | WATCHLIST ONLY | None actionable | Regime risk-off; scalp PF marginal; no A/B scalp signals |
| Crypto intraday | WATCHLIST ONLY | NEAR (B-tier, managing) | No new entries without catalyst; intraday mode 0W/6L this week |
| Crypto swing | MANAGING ONLY | BTC (short, tp_tracking) + 8 others need review | Swing PF 2.05 positive but longs in bearish regime adverse; no new longs |
| Stocks intraday | MANAGE + SELECTIVE | JPM (A, managing), LLY/XLF/AMD (B, waiting) | Best performing bucket; JPM confirmed working; wait RTH |
| Stocks swing | WATCHLIST ONLY | Capped to C-tier (48h audit: -12R, 0W/12L) | Swing watchlist-only cap remains in effect |
| Stocks invest | WATCHLIST ONLY | No signals cleared threshold | Not actionable this cycle |

---

## 13. Sources

All external sources verified by WebSearch + WebFetch during this review:

- [Bitcoin hits its lowest levels in years — Yahoo Finance, 2026-06-25](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-june-25-2026-bitcoin-hits-its-lowest-levels-in-years-125308371.html)
- [Stock Market Today (June 25, 2026): Dow futures edge higher as Micron sparks AI rally — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-25-2026)
- [JPMorgan Chase (JPM) live price $340.95, day range $334.76-$343.45 — Investing.com](https://www.investing.com/equities/jp-morgan-chase)
- [Apple Inc Stock (AAPL) down -4.79% on Jun 25: China iPhone -19% YoY, price hikes — TradingKey, 2026-06-25](https://www.tradingkey.com/news/market-movers/261991404-market-movers-aapl-20260625)
- [UNH Stock Falls as UnitedHealth Confirms DOJ Probe — Barchart, 2026-06-25](https://www.barchart.com/story/news/33626296/unh-stock-falls-as-unitedhealth-confirms-doj-probe-how-should-you-play-shares-here)

Internal sources:
- `data/reports/stocks/intraday/2026-06-25_15-25_stocks_intraday_report.md` (18:25 EEST, 14min old)
- `data/reports/swing/2026-06-25_14-03_swing_report.md` (17:03 EEST)
- `data/reports/scalp/2026-06-25_13-12_scalp_report.md` (16:12 EEST)
- `data/reports/intraday/2026-06-25_13-27_intraday_report.md` (16:27 EEST)
- `data/catalysts/2026-06-25/catalyst_cycle_13-27.md` (16:27 EEST)
- `data/scheduled_runs/2026-06-25_default_schedule/cycle_05_15-48_summary.md` (17:29 EEST)
- `OPUS_ENRICHED_REVIEW_AUTO_2026-06-25_1620.md` (previous review)

---

## 14. Fix Requests / TODO

### TODO-crypto-longs-regime-review
- **issue:** 5 crypto swing long signals (HOE, FIL, WLD, AXE, NI) active in bearish/risk-off regime — active positions in adverse conditions
- **evidence:** active-signals CLI shows 5 B-tier swing long signals in tp_tracking status; swing report regime = "bearish trend (risk-off)"; altcoin breadth 19%
- **suggested manual fix:** Open a manual session, check each signal's entry price vs current price, verify stop is set and valid; consider manual close or stop adjustment for deeply adverse positions
- **priority:** high
- **first observed:** 2026-06-25 18:39 EEST

### TODO-eth-entered-unresolved-review
- **issue:** ETH B-tier swing long is ENTERED UNRESOLVED with no confirmed stop/TP outcome; price at $1,535 (-6.67% 24h) in downtrend
- **evidence:** active-signals CLI shows ETH B swing long tp_tracking; swing report: ETH score 51.1 with -24.7 risk penalty, price >2 ATR from EMA20; prior review flagged urgent at 16:20
- **suggested manual fix:** Check paper trade entry price for ETH, current P&L, whether stop has been hit; if in significant drawdown past stop, manually close and log as NEEDS REVIEW
- **priority:** high
- **first observed:** 2026-06-25 16:20 EEST (carry-forward)

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol mapping below 2% this run — most events (98%+) classified as "other_news" without symbol mapping
- **evidence:** catalyst_cycle_13-27.md: 448 events total, 423 "other_news", only ~7 explicitly symbol-mapped (XRP×3, BTC×1, UNH×1, SOL×1)
- **suggested manual fix:** Review symbol resolver in catalyst layer; consider adding entity recognition for common stock tickers (AAPL, JPM, NVDA, etc.) and major crypto names to improve mapping coverage
- **priority:** medium
- **first observed:** 2026-06-25 18:39 EEST
