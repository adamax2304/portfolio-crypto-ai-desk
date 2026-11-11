# Opus Enriched Review — post-close final daily review — Auto Cycle 23:30 EEST

**Slot:** Post-Close Final Daily Review (23:15 EEST slot)
**Time:** 2026-06-25 23:30 EEST (20:30 ET — after US cash close)
**Date:** 2026-06-25
**Model:** claude-sonnet-4-6
**Advisory only — no auto-trade, no signal registration**

---

## 1. Executive Summary

**Slot: Post-Close Final Daily Review.** US session has closed. This is the overnight setup and daily wrap.

**BTC closed below $60K.** Confirmed intraday low ~$59,334 (midday ET), selloff driven by 6th consecutive week of ETF outflows ($5.94B total streak). BTC/ETH both in confirmed downtrend; altcoin breadth at 22.7% (deeply risk-off). The cleanest position of the day is the BTC B swing short — OPEN ACTIONABLE with TP hits, fully regime-aligned.

**JPM was today's stock winner.** A-tier intraday long: TP1 hit at day high $343.45 (vs target $343.43); stock closed ~$340.95 (+2.25%) on leadership restructuring news. AAPL B short is NO-ENTRY / MOVED-AWAY (closed above invalidation ~$293).

**AAVE is best catalyst of the day but intraday signal is stale.** Standard Chartered initiated coverage ($3,500/2030 + $180/2026 targets); AWW protocol → 100% revenue to DAO treasury. AAVE closed ~$75 (off intraday highs). The $79-82 entry zone from the 21:39 review has been breached to the downside. Next session: $70-75 support as new structure watch zone.

**UNH: DOJ criminal + civil probe confirmed → AVOID all longs.** C-tier longs in system need manual review before next RTH. `needs_review=1` in paper monitor is flagged.

**ADA exploit confirmed:** SecondFi $2.4M private key flaw. AVOID ADA longs.

**XRP positive:** RLUSD stablecoin launched in Japan (FSA regulatory approval). Confirmed by CoinDesk, CryptoBriefing, The Block — 3 primary sources. Asia session catalyst.

**Overnight crypto setup:** 5 counter-trend longs (HOT/ETH/AXS/FIL/WLD) remain ENTERED UNRESOLVED in a confirmed bearish BTC regime. All have tp_hits but overnight positioning against trend is elevated risk. Review individual stops before Asia session.

**ALWAYS-SCAN: Scanner continues in all regimes.**

---

## 2. Data Used

| Source | File | Generated (EEST) | Age at 23:30 | Status |
|--------|------|-----------|--------------|--------|
| Scheduler log | scheduler.log | 23:17 | 13 min | FRESH |
| Latest cycle | cycle_07_22-24_summary.md | 23:17 | 13 min | FRESH |
| Scalp report | 2026-06-25_19-39_scalp_report.md | 22:39 | ~51 min | FRESH |
| Intraday crypto | 2026-06-25_19-52_intraday_report.md | 22:52 | ~38 min | FRESH |
| Swing crypto | 2026-06-25_14-03_swing_report.md | 17:03 | ~6.4h | CARRY-FORWARD |
| Stocks intraday | 2026-06-25_20-14_stocks_intraday_report.md | 23:14 | 16 min | VERY FRESH (post-close) |
| Stocks swing | 2026-06-25_14-19_stocks_swing_report.md | 17:19 | ~6.2h | CARRY-FORWARD |
| LLM crypto packet | llm_analysis_packet.md | 22:53 | ~37 min | FRESH |
| LLM stocks packet | llm_stocks_packet.md | 23:16 | 14 min | FRESH |
| Active signals CLI | src.cli active-signals ×2 | 23:27 | live | LIVE |
| Signal stats CLI | src.cli signal-stats ×2 | 23:27 | live | LIVE |
| Untracked legacy | detect_untracked_legacy_alerts | cycle_07 | 13 min | None found |
| External web | WebSearch (4 queries) | 23:27 | live | LIVE |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-25_2139.md | 21:39 | ~1.8h | READ |

**Blindspots:** Live real-time BTC close price (internal OHLCV data as of ~22:52 EEST), liquidation heatmaps, OI/CVD live, social attention (Reddit blocked 403), onchain config missing.

---

## 3. Scheduler / Data Freshness

- **Scheduler cycle 07:** 22:24–23:17 EEST (28 steps OK / 0 failed). Label: weekday crypto+stocks. FRESH (13 min ago). DO NOT DEFER.
- **Paper monitor (cycle 07 step 26):**
  - OPEN actionable: 3
  - WAITING for entry: 0
  - ENTERED UNRESOLVED: 20
  - REVIEW/SHADOW: 179
  - NO-ENTRY / STALE / MOVED-AWAY: 28
  - NEEDS REVIEW: 1
  - Closed today: 296W / 48L / 0flat
- **Untracked legacy crypto alerts:** None (clean, cycle 07 step 24).
- **Active crypto signals (8, all B-tier, all tp_hits):**
  - Regime-aligned shorts: BTC/USDT swing short; NEAR/USDT intraday short; MEGA/USDT swing short
  - Counter-trend longs: HOT/USDT swing long; ETH/USDT swing long; AXS/USDT swing long (weekend=Y); FIL/USDT swing long; WLD/USDT swing long
- **Active stocks signals:** 20 total from cycle 07 step 21. JPM has A-tier (tp_hits) and B-tier (triggered). AAPL B short (triggered, likely NO-ENTRY/MOVED-AWAY per analysis).
- **Intelligence layer (cycle 07):** 92 derivative symbols. Squeeze phases: build_up=10, squeeze_expansion=3, unwind=5, post_unwind_chop=34, unknown/distribution=40.
- **Onchain:** interface_ready_config_missing — no config/onchain.yaml.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-06-25 23:30 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.91,
      "reason_codes": ["scheduler_fresh", "report_stale_swing_6h"],
      "data_missing": ["onchain_config_missing", "live_btc_realtime_close", "social_attention", "liquidation_heatmap"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_07_23:17_13min_28ok", "scalp_22:39_51min_fresh", "intraday_22:52_38min_fresh", "stocks_intraday_23:14_16min_post_close", "swing_17:03_6.4h_carry_forward", "llm_packets_fresh"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.88,
      "reason_codes": ["risk_off", "chop_stocks", "shorts_preferred"],
      "data_missing": ["live_btc_close_price"],
      "suggested_effect": "advisory_only",
      "facts_used": ["btc_downtrend_59334_below_60k", "eth_downtrend", "altcoin_breadth_22.7pct", "btc_atr_99th_pct", "vix_19.16_neutral", "spy_range_qqq_range_iwm_uptrend", "etf_outflows_6wk_5.94B"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "ok",
      "confidence": 0.83,
      "reason_codes": ["fresh_catalyst", "multi_source_confirmed"],
      "data_missing": ["catalyst_unmapped_ratio"],
      "suggested_effect": "advisory_only",
      "facts_used": ["jpm_leadership_restructuring_cnbc_2source", "aave_stanchart_3500_2030_180_2026_confirmed", "aave_aww_100pct_revenue_dao", "xrp_rlusd_japan_3source_coindesk_cryptobriefing_theblock", "ada_exploit_secondfi_2.4m_3source", "btc_etf_outflows_6weeks_5.94B", "aapl_china_iphone_-19pct_ubs", "unh_doj_criminal_civil_confirmed"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["squeeze_risk_tnsr", "squeeze_risk_re", "data_unavailable"],
      "data_missing": ["realtime_oi", "liquidation_heatmap", "cvd_live"],
      "suggested_effect": "advisory_only",
      "facts_used": ["tnsr_oi_+25.4pct_neg_funding_-0.003", "re_oi_+21.55pct_neg_funding_-0.002", "mega_oi_+6.1pct_fresh_shorts", "34_symbols_post_unwind_chop", "10_build_up"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.73,
      "reason_codes": ["entry_late", "chase_risk", "no_ab_signals_generated"],
      "data_missing": ["live_chart_mcp"],
      "suggested_effect": "advisory_only",
      "facts_used": ["hei_2atr_above_ema20_reject", "syn_2atr_above_ema20_reject", "tnsr_pullback_zone_0.042-0.043_not_reached_yet", "aave_75_below_entry_zone_79-82_intraday_stale", "btc_short_existing_late_add"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.87,
      "reason_codes": ["open_actionable_3", "entered_unresolved_20", "needs_review_1"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["open_actionable_3", "waiting_0", "entered_unresolved_20", "review_shadow_179", "no_entry_stale_28", "needs_review_1", "closed_296W_48L_0flat", "aapl_b_no_entry_moved_away_above_invalidation"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["correlation_cluster", "legal_risk", "weekend_underperformance", "manual_review_required"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["5_counter_trend_longs_hot_eth_axs_fil_wld_bearish_btc", "unh_c_longs_doj_criminal_probe", "crypto_intraday_pf_0.00_-6R_0wins", "btc_atr_99th_pct", "weekend_14pct_wr_underperformance"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["swing_working", "shorts_working", "intraday_failing", "longs_failing", "stocks_c_losing"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_pf_2.05_+18R", "crypto_shorts_pf_3.5_+20R", "crypto_intraday_pf_0.00_-6R_0wins", "crypto_longs_pf_0.8_-5R", "stocks_a_tier_pf_inf_n1_jpm", "stocks_b_pf_1.11_n18_marginal", "stocks_c_pf_0.63_-13R"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["risk_off", "shorts_preferred", "catalyst_backed_xrp_asia", "no_new_entries"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["btc_below_60k_etf_6wk", "jpm_tp1_confirmed_win", "aave_stale_intraday_now_catalyst_watch", "xrp_rlusd_japan_asia_relevance", "unh_avoid_doj", "ada_avoid_exploit", "shorts_pf_3.5_dominant"]
    }
  ],
  "head_trader_synthesis": {
    "overall_verdict": "caution",
    "confidence": 0.82,
    "preferred_side": "shorts",
    "best_long_watch": {
      "symbol": "TNSR/USDT",
      "trigger": "pullback to 0.042-0.043 in Asia session AND BTC stable above $59K; confirm uptick volume; reduce size vs bearish tape",
      "reason": "top RS leader today (+31% vs BTC), OI expanding, pullback zone not yet reached — Asia wait only"
    },
    "best_short_watch": {
      "symbol": "BTC/USDT",
      "trigger": "active OPEN position; add only on failed $60K reclaim with hourly close below $59,500",
      "reason": "B swing short with TP hits; ETF outflow 6th week; regime fully aligned"
    },
    "best_catalyst_watch": {
      "symbol": "XRP/USDT",
      "trigger": "Japan RLUSD live; 15m breakout above today's intraday high at Asia open; stop below today's low; invalidation if fails $0.95",
      "reason": "RLUSD Japan FSA approval confirmed by 3 primary sources; Asia-local relevance"
    },
    "avoid": ["ADA/USDT (exploit/hack confirmed)", "UNH (DOJ criminal+civil probe)"],
    "operator_action": "watch + manual_review_unh",
    "do_not_change": ["scoring", "TP/SL", "entry_logic", "routing", "live_execution"]
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Key Reason Codes | Suggested Effect |
|-------|---------|------------|-----------------|-----------------|
| data_quality | ok | 0.91 | scheduler_fresh, swing_carry_forward | advisory_only |
| market_regime | caution | 0.88 | risk_off, chop_stocks, shorts_preferred | advisory_only |
| catalyst_narrative | ok | 0.83 | fresh_catalyst, multi_source_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk_tnsr/re, data_unavailable | advisory_only |
| technical_entry | caution | 0.73 | entry_late, chase_risk, no_ab_signals | advisory_only |
| execution_lifecycle | ok | 0.87 | open_actionable_3, entered_unresolved_20 | advisory_only |
| risk_manager | caution | 0.82 | correlation_cluster, legal_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.78 | swing/shorts working; intraday/longs failing | advisory_only |
| head_trader | caution | 0.82 | risk_off, shorts_preferred, catalyst_xrp | advisory_only |

---

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-25_2139.md` (21:39 EEST, late-session slot)

| Item | Then (21:39) | Now (23:30) | Delta |
|------|-------------|-------------|-------|
| Cycle | Cycle 06 (in progress) | Cycle 07 complete (28/28 OK) | Full fresh cycle completed |
| Paper monitor losses | 43L | 48L (+5L) | 5 more losses in final cycle |
| JPM A-tier | TP1 hit intraday ($343.45) | Closed $340.95, below TP1 | Position in ENTERED UNRESOLVED; no new entry |
| BTC | ~$59,334 midday, below $60K flagged | Confirmed close sub-$60K | Short thesis fully confirmed for overnight |
| AAPL B short | "likely NO-ENTRY/MOVED-AWAY" | CONFIRMED NO-ENTRY/MOVED-AWAY ($293+ at close) | Signal expired; remove from active watch |
| AAVE | Promoted to B-tier intraday long (advisory), "triggered" | $75 at close; intraday signal stale/expired; fallen through $79-82 entry zone | Demote to catalyst-watch next session |
| UNH | C longs flagged for manual review | DOJ criminal + civil probe confirmed | AVOID status maintained; manual review still required |
| Crypto counter-trend longs | "Review stops before close" advised | All 5 still ENTERED UNRESOLVED with tp_hits | Overnight risk elevated; no new entries |
| XRP | RLUSD Japan noted | 3-source primary confirmation | Upgraded to best catalyst-watch for Asia |

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 1,181 (scalp report §5); latest cycle scan: 500 events in final pass
- **Active baskets (6):** rwa_narrative, delisting_thin_liquidity, perps_dex_narrative, binance_ecosystem_teaser, ai_narrative, momentum_breakout

| Symbol | Event | Sources | Sentiment |
|--------|-------|---------|-----------|
| BTC/USDT | Falls below $60K, ETF outflows 6th week ($5.94B streak) | AMBCrypto, Telegram, BeInCrypto | NEGATIVE |
| AAVE/USDT | StanChart $3,500/2030 initiation; AWW 100% revenue to DAO | Benzinga, BeInCrypto, CryptoBriefing | POSITIVE |
| XRP/USDT | RLUSD stablecoin Japan FSA approval + launch | CoinDesk, CryptoBriefing, The Block | POSITIVE |
| ADA/USDT | SecondFi $2.4M wallet exploit (private key flaw) | AMBCrypto, CryptoSlate, CoinDesk | NEGATIVE/AVOID |
| JPM | Leadership restructuring (Petno/Rohrbaugh co-presidents, Lake exits) | CNBC, Yahoo Finance | POSITIVE |
| AAPL | China iPhone sales -19% YoY (May, UBS estimate) | t.me/WalterBloomberg, UBS | NEGATIVE |
| UNH | DOJ criminal + civil investigation (Medicare fraud probe) | QuiverQuant, Yahoo Finance | LEGAL RISK/AVOID |

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off / bearish trend
- **Stocks mood:** chop / neutral-closed (US closed; VIX 19.16; SPY/QQQ range; IWM/DIA uptrend)
- **Dominant narrative:** BTC ETF outflow streak (6th week, $5.94B total) + sub-$60K close → crypto bears in control
- **Preferred side:** shorts in crypto; catalyst-backed in stocks (next RTH)
- **Best long watch:** TNSR/USDT — pullback to 0.042-0.043 + BTC stabilization above $59K
- **Best short watch:** BTC/USDT — OPEN ACTIVE; failed $60K reclaim = continuation trigger
- **Best catalyst-backed:** XRP/USDT — RLUSD Japan (3 primary sources); 15m Asia breakout trigger
- **Avoid:** ADA/USDT (exploit); UNH (DOJ probe); crypto intraday (PF 0.00); counter-trend long additions
- **What changes the view:** BTC ETF inflows reversal + reclaim of $62K; VIX drop below 17 + SPY range break

---

## 7. Candidate Deep Dives

### Candidate 1 — JPM (Stocks A-tier intraday long) — TODAY'S WINNER

**Status:** OPEN ACTIONABLE — TP1 HIT ($343.45 vs target $343.43); closed $340.95

**Catalyst:** JPMorgan named Doug Petno and Troy Rohrbaugh co-presidents; Marianne Lake exits. Market +2.25%. Sources: CNBC Markets + Yahoo Finance (2 primary). Financials led today.

**For next RTH:** Watch dip to $337-340 as retest zone. Do NOT chase above $341 at open. Position: ENTERED UNRESOLVED toward TP2. No new entries until Thursday RTH.

---

### Candidate 2 — BTC/USDT (Crypto B-tier swing short) — CORE OVERNIGHT

**Status:** OPEN ACTIONABLE — TP HIT; regime-aligned

**Catalyst:** Sub-$60K close. ETF outflows 6th consecutive week ($5.94B total). BeInCrypto/AMBCrypto/Yahoo Finance confirm.

**Overnight:** Existing short active. Do NOT add into the close of the move. Add trigger: failed $60K reclaim — hourly close below $59,500 after bounce to $60K zone. Invalidation: 4h close above $62K.

---

### Candidate 3 — AAVE/USDT (Catalyst-watch, next EU/Asia session)

**Status:** REVIEW/SHADOW — intraday signal STALE/EXPIRED at US close

**Catalyst:** Standard Chartered $3,500/2030 target ($180/2026); AWW 100% protocol revenue → DAO treasury. 3 primary sources. AAVE closed ~$75 after +15% intraday spike (gave back gains vs risk-off BTC).

**Next session:** $70-75 support zone + 1h bullish engulfing in EU session = entry trigger. The $79-82 zone from 21:39 review has been breached. Thesis is multi-session; intraday signal is stale. Regime headwind = reduce size if entering.

---

### Candidate 4 — XRP/USDT (Catalyst-watch, Asia session priority)

**Status:** NOT IN ACTIVE SIGNALS — WATCHLIST

**Catalyst:** RLUSD stablecoin Japan FSA approval confirmed: CoinDesk, CryptoBriefing, The Block (3 primary sources). Japan-specific regulatory approval with local market relevance.

**Trigger:** 15m breakout above today's intraday high at Japan/Asia open. Stop below today's low. Invalidation: fails $0.95 at Asia open.

---

### Candidate 5 — UNH (AVOID) + ADA/USDT (AVOID)

**UNH — LEGAL RISK: AVOID ALL TIERS**
DOJ criminal + civil investigation confirmed (Medicare Advantage overbilling). `needs_review=1` paper monitor flag. ALL UNH longs must be reviewed before Thursday RTH. Add legal_risk override to system config.

**ADA/USDT — EXPLOIT: AVOID LONG**
SecondFi $2.4M private key exploit confirmed (3 sources). Long catalyst disqualified. Short watch if price fails pre-exploit levels. No long entries.

---

## 8. Best Candidates Ranked

| Role | Symbol | Status | Exact Trigger |
|------|--------|--------|---------------|
| Best short-watch | BTC/USDT | OPEN ACTIONABLE | Active; add on failed $60K reclaim (hourly close below $59.5K after bounce) |
| Best long-watch (Asia) | TNSR/USDT | WATCHLIST | Pullback to 0.042-0.043 + BTC stable above $59K + volume uptick |
| Best catalyst-watch (Asia) | XRP/USDT | WATCHLIST | RLUSD Japan + 15m breakout above today's high at Asia open |
| Best catalyst-watch (next EU) | AAVE/USDT | REVIEW/SHADOW | $70-75 support hold + 1h bullish engulfing in EU session |
| Avoid | ADA/USDT + UNH | AVOID | Active exploit (ADA) / DOJ criminal probe (UNH) |

---

## 9. Avoid / No Trade

- No new crypto intraday entries (PF 0.00 / 0 wins / -6R in 14d data — hard stop until 20-signal audit)
- No new crypto long entries without BTC stabilization above $60K
- No new stock entries (session closed; re-evaluate at RTH Thursday)
- UNH: AVOID all tiers; manual review before next RTH
- ADA: AVOID long (exploit confirmed)
- AAPL B short: NO-ENTRY/MOVED-AWAY — do not re-enter without fresh RTH setup
- Weekend signals: 14% WR underperformance; elevated caution (AXS has weekend=Y)
- **NEVER stop scanner** — collection continues in all regimes

---

## 10. Main Risks

| Risk | Severity | Notes |
|------|----------|-------|
| BTC overnight cascade | HIGH | Sub-$60K, extreme ATR (99th pct), 5 counter-trend longs exposed |
| TNSR squeeze | MEDIUM | OI+25.4%, neg funding -0.003 |
| RE/USDT squeeze | MEDIUM | OI+21.55%, neg funding -0.002 |
| UNH legal | HIGH | DOJ criminal+civil; must manual review before RTH |
| ADA exploit propagation | MEDIUM | Private key flaw; broader user impact possible |
| Crypto intraday playbook | HIGH | PF 0.00 / 0 wins / -6R — do not deploy |
| RSS blind spot | MEDIUM | Reuters Business + SEC EDGAR consistently failing |

---

## 11. Action Plan — Next 4-6 Hours

1. **BTC short management:** Trail stop to protect gains if Asia breaks below $59K; failed $60K reclaim = best add signal
2. **Counter-trend longs:** Manually review HOT/ETH/AXS/FIL/WLD individual stops before Asia session; no additions
3. **XRP watch at Asia open:** Japan RLUSD live; watch 15m for buying confirmation
4. **TNSR watch:** Entry trigger: pullback to 0.042-0.043; not before
5. **UNH manual review:** Handle before Thursday RTH open
6. **AAVE monitoring:** Watch $70-75 overnight; no intraday action until EU session
7. **AXS weekend flag:** Note weekend=Y tag; reduce expectations
8. **Scanner continuous**

---

## 12. Final Verdict per Mode

| Mode | Direction | Verdict | Notes |
|------|-----------|---------|-------|
| Crypto scalp | — | NO TRADE | Risk-off + low confidence playbook |
| Crypto intraday | — | NO TRADE | PF 0.00 / 0 wins / -6R — hard stop until audit |
| Crypto swing short | SHORT | ACTIVE (BTC OPEN ACTIONABLE) | Maintain; add only on failed $60K reclaim |
| Crypto swing long | LONG | ENTERED UNRESOLVED (5 counter-trend) | No additions; review stops manually |
| Stocks intraday | — | MARKET CLOSED | Re-evaluate at RTH Thursday |
| Stocks swing | LONG carry | ENTERED UNRESOLVED (JPM) | TP1 hit today; watch TP2; no new entries until RTH |
| Overnight/Asia | Watch only | XRP catalyst-watch, TNSR long pullback, BTC short active | No new live entries without Asia confirmation |

---

## 13. Sources

- [Bitcoin below $60K, ETH prices today June 25 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-june-25-2026-bitcoin-hits-its-lowest-levels-in-years-125308371.html)
- [Aave Jumps 15% Off Standard Chartered Forecasts — BeInCrypto](https://beincrypto.com/aave-price-surge-bitcoin-below-60k/)
- [Standard Chartered initiates Aave $3,500/2030 coverage — CryptoBriefing](https://cryptobriefing.com/aave-revenue-standard-chartered-coverage/)
- [UNH DOJ probe 2026 — Phemex Academy](https://phemex.com/academy/unitedhealth-group-unh-stock-2026)
- Internal: cycle_07_22-24_summary.md; scalp/intraday/swing/stocks reports; active-signals CLI; signal-stats CLI

---

## 14. Fix Requests / TODO

### TODO-intraday-playbook-audit (HIGH)
Crypto intraday: PF 0.00 / -6R / 0 wins over 14d (signal-stats). Audit closed intraday signals by sub-bucket (direction, RS status, catalyst/no-catalyst, regime). Consider tightening no-catalyst intraday filter.

### TODO-unh-c-longs-manual-review (HIGH — before Thursday RTH)
UNH C-tier longs active while DOJ criminal+civil probe confirmed. `needs_review=1` flagged. Query all active UNH signals, close or tighten longs, add legal_risk tag to system config.

### TODO-rss-reuters-edgar-fix (MEDIUM)
Reuters Business + SEC EDGAR RSS consistently failing across multiple cycles. Check URLs/auth; add alert when same RSS fails 2+ consecutive cycles.
