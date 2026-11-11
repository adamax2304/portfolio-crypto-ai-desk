# Opus Enriched Review — Europe / Pre-US Context — Auto Cycle 11:39 EEST

**Slot:** Europe / Pre-US Context (11:30 EEST slot)
**Time:** 2026-06-28 11:39 EEST
**Date:** 2026-06-28 (Sunday — weekend mode active, stocks closed)
**Model:** claude-sonnet-4-6
**Advisory only — no auto-trade, no signal registration**

---

## 1. Executive Summary

**Slot: Europe / pre-US context — advisory only / no auto-trade.**

BTC sits near 4-month lows (~$60–61k) with the largest-ever spot ETF weekly outflow ($3.4B in early June) as macro tail from the 2026 Strait of Hormuz crisis lingers post-reopening (June 14). Today's scalp/intraday reports show **zero fresh candidates** from any exchange (Binance universe=0, Bybit/MEXC 54 failures each) — **all 11 active crypto signals are from yesterday's full scan and are in ENTERED UNRESOLVED status.** No new A/B ideas are available from today's scan cycle.

**Crypto mood: risk-off.** BTC downtrend, ETH downtrend, 0% altcoin breadth above EMA20. Shorts outperform dramatically (PF=2.62, +13R) vs longs (PF=1.15). Weekend mode active — historically the worst performance bucket (PF=0.80, -2R). Intraday mode is the worst by playbook (PF=0.00, -5R) — **no intraday entries.**

**Key legal risks requiring immediate attention:** UNH has 4+ active signals (long and short) but a **DOJ criminal Medicare fraud probe** with shares already -16% — all UNH positions must be flagged AVOID. SMCI has an active short signal plus a **federal securities lawsuit** for export-control violations — manual review required.

**Stocks closed (weekend).** JPM A-tier (81%) is planning context for Monday only, not actionable today.

**HYPE** (Hyperliquid) is the strongest catalyst-backed watch candidate: Bitwise staked $114M, no active signal, current price ~$64 off ATH $76.67, institutional ETP live on Deutsche Borse. ETH has fresh whale accumulation catalysts ($322M in 4 days, a16z +$42M) but conflicting ETF outflows and downtrend — watch for retest only.

ALWAYS-SCAN continues. No recommendation to pause or stop the scanner.

---

## 2. Data Used

| Source | File/CLI | Generated (EEST) | Age at 11:39 | Status |
|--------|----------|-----------------|--------------|--------|
| Scheduler | cycle_01_10-44_summary.md | 10:56 | 43 min | **FRESH** |
| scheduler.log | data/scheduled_runs/2026-06-28_default_schedule/ | 10:56 | 43 min | **FRESH** |
| Scalp report | 2026-06-28_07-49_scalp_report.md | 10:49 | 50 min | **FRESH** (universe=0) |
| Intraday crypto | 2026-06-28_07-49_intraday_report.md | 10:49 | 50 min | **FRESH** (universe=0) |
| Swing crypto | 2026-06-27_01-20_swing_report.md | 04:20 Jun 27 | ~31h | **STALE** |
| Stocks intraday | 2026-06-26_20-14_stocks_intraday_report.md | 23:14 Jun 26 | ~36h | STALE — weekend closed |
| Stocks swing | 2026-06-26_15-06_stocks_swing_report.md | 18:06 Jun 26 | ~41h | STALE — weekend closed |
| Stocks invest | 2026-06-26_15-13_stocks_invest_report.md | 18:13 Jun 26 | ~41h | STALE — weekend closed |
| Catalyst events | data/catalysts/2026-06-28/ | 10:49 | 50 min | **FRESH** (17 events, 1 basket) |
| LLM crypto packet | data/processed/llm_analysis_packet.md | 10:49 | 50 min | **FRESH** |
| LLM stocks packet | data/processed/llm_stocks_packet.md | 23:15 Jun 26 | ~36h | STALE |
| Active signals (crypto) | CLI live 11:39 | live | live | 11 signals |
| Active signals (stocks) | CLI live 11:39 | live | live | 50 signals |
| Signal-stats | CLI live 11:39 | live | live | crypto n=123, stocks n=24 |
| Untracked alerts | CLI live 11:39 | live | live | NONE |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-27_0439.md | 04:57 Jun 27 | ~31h | READ |
| External web research | WebSearch x5 | 11:39 | live | AVAILABLE |

**Critical data gap this cycle:** Binance, Bybit, MEXC all reporting exchange failures. **Zero candidates from fresh scan.** Reports use cached OHLCV from 2026-06-27 06:15 UTC (26h stale). All 11 crypto signals are from yesterday's full scan.

---

## 3. Scheduler / Data Freshness

- **Latest cycle:** `cycle_01_10-44_summary.md` completed **10:56 EEST** (43 min ago). NOT DEFERRED.
- **scheduler.log mtime:** 10:56 EEST. FRESH.
- **Crypto signals (live CLI 11:39):** 11 active. All show status `tp_hit` — ENTERED UNRESOLVED (entry filled, no TP/SL before window). All carry-forward from yesterday's full scan.
  - BERA swing B long 67% (exchange-weighted=Y) — new vs Jun 27 review
  - AAVE swing B long 65% (exchange-weighted=Y) — was WAITING yesterday, now entered
  - SOL swing B long 74% — entered unresolved
  - BTC intraday B short 66% — entered unresolved
  - ETH swing B short 65% — entered unresolved
  - HEI intraday B long 66% — entered unresolved
  - BTC swing B short 65% — entered unresolved
  - HOD swing B long 72% — entered unresolved
  - ETH swing B long 66% — entered unresolved
  - AXS swing B long 65% (exchange-weighted=Y) — entered unresolved
  - MEM swing B short 68% — entered unresolved
- **Stocks signals (live CLI):** 50 active, all C-tier except JPM intraday A (81%). Market CLOSED (weekend). Planning only.
- **Paper monitor:** Carry-forward from Jun 27 04:39: ~$5,140.57 gross paper, zero-cost +50.2%, Bybit-taker: -6.2%.
- **Untracked legacy alerts:** NONE (clean).
- **Weekend mode:** ACTIVE (Sunday). All new entries subject to weekend penalty.
- **OHLCV data age:** 26h stale (from 06:15 UTC Jun 27). Exchange failures mean no fresh scan ran today.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-06-28 11:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse", "onchain_config_missing"],
      "data_missing": ["binance_universe_failed_today", "bybit_mexc_54_failures", "ohlcv_26h_stale_from_cached", "binance_futures_funding_oi", "rss_news_all_sources_failing", "social_attention_reddit_403", "swing_report_31h_stale", "stocks_reports_36_41h_stale", "onchain_config_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_01_10:56_EEST_43min_fresh", "scalp_intraday_fresh_50min_but_universe=0", "catalyst_fresh_50min_17events_1basket", "untracked_alerts_none"]
    },
    {
      "agent": "market_regime",
      "verdict": "bad",
      "confidence": 0.78,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"],
      "data_missing": ["derivatives_oi_funding", "social_sentiment_live", "fear_greed_today"],
      "suggested_effect": "advisory_only",
      "facts_used": ["btc_downtrend_4month_lows_60_61k", "eth_downtrend", "altcoin_breadth_0pct_above_ema20", "btc_atr_percentile_90_elevated", "etf_weekly_outflow_3.4B_record", "hormuz_crisis_resolved_june14_macro_tail", "weekend_mode_thin_liquidity", "fg_15_extreme_fear", "shorts_pf_2.62_vs_longs_1.15"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": ["catalyst_freshness_hours_null", "price_reaction_so_far_unknown", "volume_confirmation_unknown"],
      "suggested_effect": "advisory_only",
      "facts_used": ["btc_4month_low_61k_etf_outflows", "eth_whale_322M_accumulation_a16z_42M", "hype_bitwise_114M_staked", "unh_doj_criminal_medicare_shares_minus16pct", "smci_securities_lawsuit", "sol_624k_token_unlock", "ai_basket_tao_render_near_fet_single_source"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.25,
      "reason_codes": ["data_unavailable"],
      "data_missing": ["binance_futures_oi_funding_missing", "bybit_mexc_54_failures", "no_live_funding_rates", "no_liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": ["prev_cycle_squeeze_expansion_fading_2_from_5", "prev_cycle_post_unwind_chop_36", "no_current_derivatives_data"]
    },
    {
      "agent": "technical_entry",
      "verdict": "bad",
      "confidence": 0.60,
      "reason_codes": ["stale_before_entry", "no_entry", "chase_risk"],
      "data_missing": ["fresh_ohlcv_exchange_failures", "chart_mcp_not_loaded", "current_atr_values"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ohlcv_26h_stale_cached_only", "universe_0_no_fresh_scan_today", "all_11_signals_entered_unresolved_from_yesterday", "no_new_setup_from_todays_cycle"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "review_shadow",
      "confidence": 0.70,
      "reason_codes": ["entered_unresolved", "review_shadow"],
      "data_missing": ["paper_monitor_current_cycle_not_available"],
      "suggested_effect": "advisory_only",
      "facts_used": ["11_crypto_signals_all_tp_hit_entered_unresolved", "bera_new", "aave_was_waiting_now_entered", "hyper_jto_expired_13_to_11", "stocks_50_market_closed", "jpm_a_tier_stocks_closed", "unh_signals_legal_risk_avoid"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["legal_risk", "correlation_cluster", "headline_risk", "manual_review"],
      "data_missing": ["daily_pnl_live_tracking"],
      "suggested_effect": "advisory_only",
      "facts_used": ["unh_doj_criminal_probe_CRITICAL_LEGAL_RISK", "smci_securities_lawsuit", "weekend_mode_pf_0.80_minus2R", "intraday_mode_pf_0.00_minus5R", "exchange_unconfirmed_pf_0.69_minus7R", "shorts_confirmed_pf_2.62_plus13R"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["stocks_ab_sample_too_small_24"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_pf_2.06_plus16R_BEST", "crypto_shorts_pf_2.62_plus13R", "crypto_intraday_pf_0.00_minus5R_FAILING", "exchange_confirmed_two_pf_2.26_plus19R", "weekend_pf_0.80_minus2R", "stocks_ab_pf_0.769_minus3R"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["wait_for_trigger", "shorts_preferred"],
      "data_missing": ["fresh_ohlcv_today", "derivatives_live"],
      "suggested_effect": "advisory_only",
      "facts_used": ["all_11_entered_unresolved_no_new_setups", "risk_off_btc_downtrend_0pct_breadth", "shorts_dramatically_outperforming", "legal_risks_unh_smci", "hype_bitwise_114M_no_active_signal", "eth_whale_watch_retest"]
    }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.72,
    "preferred_side": "shorts",
    "best_long_candidate": {
      "symbol": "ETH",
      "trigger": "Retest $1,600-1,620 support on 1h chart + declining volume + whale accumulation not reversing; exchange-confirmed entry only",
      "reason": "Fresh institutional whale accumulation ($322M/4d, a16z $42M, SharpLink $7.88M) vs ETF outflows in downtrend — long only on confirmed retest, not a chase"
    },
    "best_short_candidate": {
      "symbol": "BTC",
      "trigger": "Bounce to $62k-63k zone then 4h rejection close; or break below $59k on 1h close",
      "reason": "Two active B-tier short signals, macro downtrend, record ETF outflows $3.4B, shorts PF=2.62; intraday and swing short signals both present"
    },
    "best_catalyst_candidate": {
      "symbol": "HYPE",
      "trigger": "Pullback to $58-62 range + BTC stable or neutral + fresh Bitwise/institutional flow confirmation",
      "reason": "Bitwise $114M staking fresh, Deutsche Borse ETP live, ATH $76.67 on June 16, institutional narrative intact; no active signal — shadow-watch only"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ criminal Medicare fraud probe active (WSJ-confirmed, shares -16%); conflicting long and short signals simultaneously — LEGAL/HEADLINE RISK"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason Codes | Suggested Effect |
|-------|---------|------------|--------------|-----------------|
| data_quality | **caution** | 0.68 | `scheduler_fresh, report_stale, derivatives_sparse, onchain_config_missing` | advisory_only |
| market_regime | **bad** | 0.78 | `risk_off, shorts_preferred, chop` | advisory_only |
| catalyst_narrative | **caution** | 0.65 | `fresh_catalyst, catalyst_confirmed, narrative_supported` | advisory_only |
| derivatives_squeeze | **caution** | 0.25 | `data_unavailable` | advisory_only |
| technical_entry | **bad** | 0.60 | `stale_before_entry, no_entry, chase_risk` | advisory_only |
| execution_lifecycle | **review_shadow** | 0.70 | `entered_unresolved, review_shadow` | advisory_only |
| risk_manager | **caution** | 0.78 | `legal_risk, correlation_cluster, headline_risk, manual_review` | advisory_only |
| playbook_performance | **caution** | 0.75 | `playbook_working, playbook_failing, low_sample` | advisory_only |
| **head_trader** | **caution** | 0.72 | `wait_for_trigger, shorts_preferred` | advisory_only |

---

## 4. What Changed vs Previous Review

_Previous: OPUS_ENRICHED_REVIEW_AUTO_2026-06-27_0439.md (04:39 EEST Jun 27 — ~31h ago)_

| Change | Detail |
|--------|--------|
| **REMOVED signals** | HYPER swing B (expired/closed); JTO scalp B (expired/closed) |
| **NEW signal** | BERA swing B long 67% (exchange-weighted=Y) |
| **AAVE status** | Was WAITING yesterday — now ENTERED UNRESOLVED (tp_hit) |
| **Signal count** | 13 to 11 crypto |
| **Crypto A/B stats** | PF 1.31 +16R (yesterday) to PF 1.45 +18R today (+2R week improvement) |
| **Short direction** | PF improved: ~2.3 to 2.62 (shorts strengthening) |
| **Exchange scan** | Yesterday: full scan (binance universe=413); Today: FAILED (universe=0, 54 failures) |
| **UNH legal risk** | DOJ criminal probe confirmed (-16% shares) — AVOID flag required |
| **SMCI legal risk** | Federal securities lawsuit confirmed — manual review required |
| **Hormuz context** | Strait reopened June 14 (2 weeks ago); oil fell $120 to $81; macro tail persists |
| **Catalyst count** | Previous: 488 events, 6 baskets; Today: 17 events, 1 basket (lighter weekend scan) |
| **HYPE** | Bitwise $114M stake confirmed; ATH $76.67 Jun 16; now ~$64 |
| **BTC ETF** | $3.4B record weekly outflow confirmed; Jun 23 +$39.2M (tentative stabilization) |
| **Thesis** | Regime unchanged: downtrend/risk-off persists. Shorts remain dominant bucket. |

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 17 (cycle_07-49)
- **Mapped (non-null symbol):** 16 / 17 = **94%** — GOOD coverage
- **Unmapped:** 1 / 17 — SYN (Synapse latest updates, low priority)
- **Narrative baskets:** 1 — `ai_narrative` (playbook: `related_beta_rotation`)
  - Primary: NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT; Related: WLD/USDT, ASTER/USDT
  - Evidence: single_source quality, freshness unknown — context only
- **By type:** other_news: 16 | legal_risk: 1 (UNH)
- **Top catalysts by importance:** UNH 0.73 (legal_risk); BTC Hormuz 0.52; BTC ETF outflows 0.52; BTC leverage flush 0.47; SOL unlock 0.47; SMCI lawsuit 0.47

**Note:** Previous cycle had 488 events, 6 baskets; today only 17 — lighter weekend scan. AI basket is context only (single_source, freshness unknown).

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** `risk-off` — BTC downtrend, ETH downtrend, 0% altcoin breadth above EMA20, ATR at 90th pctl, F&G = 15 extreme fear
- **Stocks mood:** `closed` (weekend, Sunday) — planning/watchlist context only until Monday RTH
- **Dominant narrative:** BTC macro pressure (ETF record outflows, Hormuz legacy, leverage flush), selective institutional crypto accumulation (ETH whales, HYPE/Bitwise), legal risk overhang (UNH, SMCI)
- **Preferred side now:** `shorts` — PF=2.62 +13R vs longs PF=1.15; prefer failed retests; **avoid intraday longs** (PF=0.00, -5R)
- **Best long candidate:** ETH — whale institutional accumulation; retest $1,600-1,620 required
- **Best short candidate:** BTC — 2 active short signals; trigger: bounce to $62k-63k then rejection or break below $59k
- **Best catalyst-backed candidate:** HYPE — Bitwise $114M staking; pullback to $58-62 range
- **What to avoid:** UNH (DOJ probe, conflicting signals), intraday longs (PF=0), weekend entries without structure, exchange-unconfirmed signals (PF=0.69, -7R)
- **What would change the view:** BTC reclaims $66k+ with ETF inflows positive 3+ consecutive days + altcoin breadth above 40%

---

## 7. Candidate Deep Dives

### Candidate 1: UNH — LEGAL/HEADLINE RISK — AVOID

**LEGAL/HEADLINE RISK — DO NOT ENTER ANY DIRECTION**

- DOJ CRIMINAL INVESTIGATION: Medicare Advantage fraud (WSJ confirmed, active DOJ healthcare-fraud unit)
- SCOPE EXPANDED: Optum Rx and physician reimbursement also under criminal probe
- CIVIL FRAUD: Separate federal civil fraud investigation (CBS News)
- Shares already -16% on these investigations
- Multiple conflicting long AND short signals simultaneously — system integrity flag

**Final verdict: AVOID across ALL directions.** Active UNH paper positions require manual review before Monday open.

Sources: [Yahoo Finance/WSJ](https://finance.yahoo.com/news/unitedhealth-under-criminal-probe-possible-231729520.html), [QuiverQuant](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe), [Fierce Healthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth)

---

### Candidate 2: ETH/USDT — Conflicting Signals, Whale Catalyst

**Active signals:** ETH swing B SHORT 65% — ENTERED UNRESOLVED; ETH swing B LONG 66% — ENTERED UNRESOLVED.

**Catalyst (confirmed via WebSearch):**
- Whales bought $322M ETH over 4 days (Investing.com) — accumulation signal
- a16z withdrew 25,560 ETH ($42M) from Binance — institutional accumulation
- SharpLink bought 5,000 ETH ($7.88M) — fresh lookonchain
- BUT: old whale wallets moving 37,806 ETH, long-term holders going negative first time since 2019 — contradicts
- Spot ETH ETF outflows Jun 22-26 — institutional net selling
- ETH failed to reclaim $1,750 resistance — bearish divergence

TradingView/manual chart check unavailable — OHLCV 26h stale.

- **Has price reacted?** ETH has not broken out despite whale buying — divergence
- **Mood alignment:** Downtrend favors short; whale catalyst creates asymmetric risk on retest
- **Verdict:** WAITING for fresh entry signal. Monitor $1,600-1,620 long-watch. Monitor rejection at $1,700+ for short confirmation.
- **Invalidation (long):** Close below $1,550 on 4h; **(short):** Close above $1,800 + ETF inflows positive

---

### Candidate 3: BTC/USDT — Short Bias, 2 Active Signals

**Active:** BTC intraday B SHORT 66% — ENTERED UNRESOLVED; BTC swing B SHORT 65% — ENTERED UNRESOLVED.

**Catalyst:**
- BTC at 4-month low ~$60-61k (confirmed)
- Record ETF weekly outflow $3.4B (Coinfomania, Investing.com — confirmed, largest since Jan 2024 launch)
- BUT: Jun 23 saw +$39.2M ETF inflows — tentative floor signal, weakens near-term short thesis
- Hormuz tail: reopened Jun 14, oil back toward $81 from $120
- Strategy (MicroStrategy) sold BTC — supply pressure
- Leverage flush in process — reduces long-squeeze risk on short side

TradingView/manual chart check unavailable.

- **Has price reacted?** YES — BTC already at 4-month lows; signals entered above current price
- **Is setup chasing?** Short at current low = potentially chasing; prefer failed bounce re-entry
- **Best short trigger:** Bounce to $62k-63k then rejection 4h; or break below $59k
- **Mood alignment:** Strong — regime risk-off, ETF flows support short bias
- **Invalidation:** Close above $65k daily; ETF inflows +$100M+ for 3 consecutive days

---

### Candidate 4: HYPE (Hyperliquid) — Catalyst-Backed Watch

**No active signal** — shadow-watch only.

**Catalyst (confirmed):**
- Bitwise deposited 1.775M HYPE ($114M) and staked it all on Hyperliquid (news.bitcoin.com)
- Bitwise Hyperliquid Staking ETP (BHYP) live on Deutsche Borse Xetra since Apr 9, 2026
- Fresh whale accumulation: 152,986 HYPE ($9.73M) from FalconX (t.me/lookonchain)
- ATH $76.67 on Jun 16, 2026; current ~$64 (-16% off ATH — healthy pullback)

- **Has price reacted?** YES — ATH $76.67 was the reaction; now pulling back
- **Chase risk:** LOW on pullback entry; HIGH if chasing near ATH
- **Mood alignment:** Mixed — risk-off crypto disfavors longs; but institutional-backed
- **Actionable now?** NO — shadow-watch until BTC stabilizes
- **Trigger:** Pullback to $58-62 + BTC stable + fresh OHLCV shows pullback structure
- **Invalidation:** BTC breaks below $57k; HYPE closes below $55

Sources: [news.bitcoin.com](https://news.bitcoin.com/bitwise-stakes-114-million-hype-hyperliquid-etf/), [The Coin Republic](https://www.thecoinrepublic.com/2026/06/02/bitwise-stacks-hyperliquid-as-projections-on-hype-price-breakout-grows/)

---

### Candidate 5: SOL/USDT — Highest Score (74%), Token Unlock Risk

**Active:** SOL swing B LONG 74% — ENTERED UNRESOLVED.

**Catalyst:**
- 624K SOL token unlock in June 2026 (Phemex) — DILUTION RISK — weakens long thesis
- Alpenglow upgrade (positive, but price reaction unknown)

- **Chase risk:** Any re-entry = chase given unlock headwind
- **Mood alignment:** Risk-off regime + 624K unlock = supply pressure on altcoin long
- **Verdict:** ENTERED UNRESOLVED — track outcome, do NOT add or re-enter
- **Invalidation:** SOL closes below $68 on 4h + unlock selling on volume

---

## 8. Best Candidates Ranked

| Rank | Symbol | Direction | Entry Trigger | Confidence |
|------|--------|-----------|---------------|------------|
| 1 | BTC (SHORT-WATCH) | short | Bounce $62k-63k then 4h rejection; or break below $59k | medium |
| 2 | HYPE (CATALYST-WATCH) | long | Pullback to $58-62 + BTC stable; shadow only | medium-low |
| 3 | ETH (LONG-WATCH) | long | Retest $1,600-1,620 + OI neutral | low-medium |
| 4 | SOL (ENTERED UNRESOLVED) | long | N/A — entered; watch $68 invalidation | low |
| 5 | JPM A-tier (PLANNING MON) | long | Monday RTH open + fresh data | planning only |

**No clean new entry available this window.** All crypto setups are ENTERED UNRESOLVED from yesterday or require fresh OHLCV unavailable due to exchange failures. Stocks closed (weekend).

- **Best long-watch:** ETH @ $1,600-1,620 retest — trigger: 1h close + whale flow not reversing
- **Best short-watch:** BTC @ bounce to $62k-63k rejection or break below $59k
- **Best catalyst-watch:** HYPE @ pullback $58-62 — trigger: BTC stabilization + Bitwise flow confirmation

---

## 9. Avoid / No Trade (This Decision Window Only)

- **UNH** — AVOID ALL DIRECTIONS — DOJ criminal probe, conflicting signals, -16% shares
- **SMCI** — AVOID new entries / MANUAL REVIEW — federal securities lawsuit active
- **Any intraday crypto long** — PF=0.00, -5R; worst-performing bucket
- **Any exchange-unconfirmed signal** — PF=0.69, -7R; prefer two-exchange-confirmed only
- **Weekend entries without retest structure** — PF=0.80, -2R bucket
- **AGLD carry-forward** — squeeze fading (expansion 5 to 2); post_unwind_chop likely
- **Chasing BTC short at 4-month low** — require failed bounce re-entry, not fresh chase

_This list applies to the current window only. ALWAYS-SCAN continues. Not a command to stop the system._

---

## 10. Main Risks

1. **Exchange connectivity failure** (HIGH) — All 3 exchanges failed today; no fresh scan. If persists to Monday, system cannot generate new signals.
2. **UNH legal/headline risk** (HIGH) — Active conflicting signals + DOJ criminal probe. Manual review before Monday open.
3. **Derivatives data blind** (HIGH) — No funding/OI today. Cannot assess squeeze risk or crowding.
4. **BTC 200-week MA breach** (MEDIUM) — If $59k fails, acceleration toward $55-57k. All altcoin longs face correlation pressure.
5. **Weekend liquidity + stale data** (MEDIUM) — System operating on 26h-old OHLCV. Signals may have moved materially.
6. **SMCI securities lawsuit** (MEDIUM) — Active short signal; manual review required.
7. **SOL token unlock** (MEDIUM) — 624K SOL unlock creates supply headwind for active swing long.
8. **RSS news all failing** (MEDIUM) — Zero RSS data; market-moving news from traditional media may be missed.

---

## 11. Action Plan — Next 4 Hours (11:39–16:00 EEST)

1. Monitor BTC for bounce toward $62k-63k — short re-entry trigger. Do not chase the low.
2. Monitor ETH at $1,600-1,620 for retest structure — long-watch trigger only.
3. Flag UNH — All active UNH positions require MANUAL REVIEW before Monday open. AVOID new entries.
4. Flag SMCI — Check if price moved significantly since signal generation. MANUAL REVIEW.
5. JPM A-tier watchlist — Planning only. Validate Sunday night futures or Monday pre-market.
6. HYPE shadow-watch — Monitor for pullback to $58-62 with BTC stabilization.
7. Investigate exchange failures — Root cause of 54 Bybit/MEXC failures + Binance universe=0.
8. Pre-US prep (16:20 slot): Re-check BTC/ETH if connectivity recovers. Verify stocks catalysts for Monday gap risk.

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Reason |
|------|-------|---------|--------|
| Scalp | Crypto | **NO TRADE** | 0 fresh candidates, exchange failures, weekend mode |
| Intraday | Crypto | **AVOID** | PF=0.00, -5R; no fresh scan; stale data; weekend mode |
| Swing | Crypto | **WATCH / SHORTS PREFERRED** | Best bucket (PF=2.06, +16R); BTC short re-entry trigger only |
| Intraday | Stocks | **PLANNING ONLY** | Closed (weekend); JPM A-tier 81% for Monday |
| Swing | Stocks | **PLANNING ONLY** | Data 41h stale; UNH legal risk unresolved |
| Invest | Stocks | **NOT APPLICABLE** | Mode not implemented |

---

## 13. Sources

**Internal:**
- `data/reports/scalp/2026-06-28_07-49_scalp_report.md`
- `data/reports/intraday/2026-06-28_07-49_intraday_report.md`
- `data/reports/swing/2026-06-27_01-20_swing_report.md` (stale, carry-forward)
- `data/catalysts/2026-06-28/catalyst_events.jsonl`, `narrative_baskets.jsonl`, `catalyst_cycle_07-49.md`
- `data/processed/llm_analysis_packet.md`
- CLI: `python -m src.cli active-signals`, `signal-stats`, `detect_untracked_legacy_alerts`
- `OPUS_ENRICHED_REVIEW_AUTO_2026-06-27_0439.md`

**External (WebSearch verified):**
- [Bitcoin ETFs Record Largest-Ever $3.4B Sell-Off (Coinfomania)](https://coinfomania.com/bitcoin-etf-outflows-june-2026-record-selloff/)
- [Bitcoin's $3.4B ETF Bleed Looks More Cyclical Than Structural (Investing.com)](https://www.investing.com/analysis/bitcoins-34-billion-etf-bleed-looks-more-cyclical-than-structural-200681474)
- [Bitcoin Falls as Record ETF Outflows and Strategy Sale Hit Sentiment (Investing.com)](https://www.investing.com/analysis/bitcoin-falls-as-record-etf-outflows-and-strategy-sale-hit-sentiment-200681446)
- [Bitcoin slides to 4-month low at $61k — Iran tensions, ETF outflows (Investing.com)](https://www.investing.com/news/cryptocurrency-news/bitcoin-slides-to-4mth-low-at-61k-as-iran-tensions-weigh-etf-outflows-continue-4725700)
- [UnitedHealth under criminal probe for Medicare fraud (Yahoo Finance/WSJ)](https://finance.yahoo.com/news/unitedhealth-under-criminal-probe-possible-231729520.html)
- [UNH Faces DOJ Probe, Shares Dive 16% (QuiverQuant)](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe)
- [DOJ probe extends to Optum Rx and physician reimbursement (Fierce Healthcare)](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth)
- [SMCI Federal Securities Lawsuit — Export-Control Violations (TipRanks)](https://www.tipranks.com/news/class-action/super-micro-computer-faces-federal-securities-lawsuit-over-alleged-export-control-violations-and-undisclosed-china-sales)
- [What the Strait of Hormuz reopening does to crypto (crypto.news)](https://crypto.news/strait-of-hormuz-reopening-crypto/)
- [Impact of 2026 Strait of Hormuz Closure on Crypto Markets (VT Markets)](https://www.vtmarkets.com/learn/impact-of-the-2026-strait-of-hormuz-closure-on-forex-and-crypto-markets/)
- [Ethereum Whale Buying at $322M Points to Accumulation Phase (Investing.com)](https://www.investing.com/analysis/ethereum-whale-buying-at-322m-points-to-accumulation-phase-200679628)
- [ETH Price Is Flat — Whales Bought $322M in 4 Days (BYDFI)](https://www.bydfi.com/en/cointalk/eth-price-whale-accumulation-etf-2026)
- [Bitwise Stakes $114M in HYPE on Hyperliquid (Bitcoin.com News)](https://news.bitcoin.com/bitwise-stakes-114-million-hype-hyperliquid-etf/)
- [Bitwise Stacks Hyperliquid as HYPE Breakout Projections Grow (The Coin Republic)](https://www.thecoinrepublic.com/2026/06/02/bitwise-stacks-hyperliquid-as-projections-on-hype-price-breakout-grows/)
- [Solana Price Today June 2026 + Alpenglow Upgrade + 624K Unlock (Phemex)](https://phemex.com/blogs/solana-price-today-june-2026-sol-alpenglow-upgrade-tvl-2030-outlook)
- [US Supreme Court turns away Eli Lilly — whistleblower law $183M (Investing.com)](https://www.investing.com/news/stock-market-news/us-supreme-court-turns-away-eli-lillys-challenge-to-whistleblower-law-4696180)

---

## 14. Fix Requests / TODO

### TODO-EXCHANGE-FAIL
- **issue:** All three exchanges (Binance, Bybit, MEXC) failed in today's 10:49 cycle — Binance universe=0 failed=1; Bybit/MEXC failed=54 each. No fresh candidates discovered. OHLCV is 26h stale.
- **evidence:** `data/reports/intraday/2026-06-28_07-49_intraday_report.md` §0: binance ohlcv_fetched=0 failed=1; bybit failed=54; mexc failed=54
- **suggested manual fix:** Check exchange API key health and rate-limit status. Inspect `data/processed/market_summary/last_update.json` for error messages. Verify Bybit/MEXC connectivity. If rate-limited, restore and trigger manual re-run.
- **priority:** high
- **first observed:** 2026-06-28 11:39 EEST

### TODO-UNH-LEGAL-SIGNAL-CONFLICT
- **issue:** UNH has 4+ active signals in both long and short directions simultaneously, PLUS active DOJ criminal Medicare fraud probe with shares -16%. System should prevent new UNH signals while legal_risk catalyst with importance>0.60 is active, or auto-flag as AVOID.
- **evidence:** Active signals CLI: UNH intraday long 60% triggered, swing long 63% triggered, intraday short 54% waiting, and more. Catalyst `cat_0546df1ba0763edf` = UNH legal_risk importance=0.73.
- **suggested manual fix:** Implement legal_risk_flag field in proposed_signals; implement catalyst_contradiction check that downgrades signals when matched legal_risk catalyst is present with importance>0.60. Manually close/void active UNH long signals now.
- **priority:** high
- **first observed:** 2026-06-28 11:39 EEST

### TODO-RSS-FAILURE-PERSISTENT
- **issue:** All 17 RSS sources consistently failing across multiple cycles (CoinDesk, Cointelegraph, CNBC, Reuters, and 13+ more). Persistent gap, not a one-off failure.
- **evidence:** `data/reports/intraday/2026-06-28_07-49_intraday_report.md` §9: "Partial/stale: RSS failures: [17 named sources]"
- **suggested manual fix:** Audit RSS fetcher for URL format changes, rate limiting, or header changes. Replace dead sources with working alternatives. Check `src/data_fetchers/rss_fetcher.py` (or equivalent).
- **priority:** high
- **first observed:** Multiple consecutive cycles; latest: 2026-06-28 11:39 EEST

### TODO-SMCI-LEGAL-SIGNAL-REVIEW
- **issue:** SMCI has active short signal (C-tier, swing short 53%) AND active federal securities lawsuit. Short direction aligns with legal risk, but system should cap tier and add LEGAL_RISK warning while lawsuit is active.
- **evidence:** Catalyst `cat_876716cfe3903e02` = SMCI securities lawsuit importance=0.467. Active signals: SMCI swing short 53% triggered.
- **suggested manual fix:** Same mechanism as TODO-UNH-LEGAL-SIGNAL-CONFLICT. For SMCI: keep short signal (direction aligns) but cap at C-tier and add LEGAL_RISK warning in Telegram alerts.
- **priority:** medium
- **first observed:** 2026-06-28 11:39 EEST
