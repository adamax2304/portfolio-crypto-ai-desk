# Opus Enriched Review — post-close final daily review — Auto Cycle 23:15 EEST

_Generated 2026-06-24 23:15 EEST (Wednesday). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

---

## 1. Executive Summary

**Wed 2026-06-24, 23:15 EEST — post-close final daily review — advisory only / no auto-trade.**

US cash session closed ~15 min ago (23:00 EEST = 16:00 ET).

- **Crypto: RISK-OFF deepening sharply post-close.** BTC crashed from $62,729 (at 21:39 review) to **$59,518** (~−5.1%, ~−$3,211 in 2h). ETH $1,566. XRP $1.05. Total 24h liquidations escalated to **$861M** (91% longs, 168,583 traders). No new A/B crypto signals generated; 15 B-tier signals remain (mostly swing).
- **BTC/USDT swing short (B-tier, active)** is the best directionally aligned signal — confirmed by tonight's breakdown below $60k. Watch $57,300 as the next liquidation cluster.
- **ETH/USDT swing long (ENTERED UNRESOLVED):** Further contradicted by $1,566 crash. Operator review required before Asia open.
- **Stocks: US session closed mildly negative.** SPY −0.17% (~732.49), recovering from yesterday's −1.12%. Session was turbulent mid-day (chip rout, VIX 20.17) but closed more calmly.
- **Micron (MU) AH beat — major post-close catalyst.** Q3 revenue $41.46B vs est $35.1B; Q4 guide $49-51B vs est $43.2B. MU +6% AH. This sets up a semiconductor reversal for tomorrow — SMH/QQQ warrant a bullish-watch setup for Thu RTH open.
- **UNH: AVOID** — DOJ criminal Medicare fraud probe confirmed (−16% today). Signal must remain AVOID.
- **ADA: AVOID** — SecondFi exploit $2.4M confirmed / >$20M potential. Ongoing.
- **Paper monitor (last known 21:21 EEST):** 0 open actionable · 1 waiting (JPM — likely triggered by close) · 29 entered unresolved · 164 review/shadow · 36 no-entry/stale/moved-away · 288W/43L closed.
- **Overnight/Asia setup:** BTC at $59.5k approaching $57.3k liquidation cluster. Asia likely sees continued pressure unless support confirmed. Best overnight watch: BTC short on bounce / ATM long only if BTC stabilizes above $60k.

---

## 2. Data Used

| Source | File / Path | mtime EEST | Freshness |
|---|---|---|---|
| scheduler.log | `data/scheduled_runs/2026-06-24_default_schedule/scheduler.log` | 23:24 | **FRESH** (<10min) |
| Latest cycle | `cycle_07_20-09_summary.md` | 21:21 | **FRESH** (114min) |
| Crypto scalp | `2026-06-24_17-31_scalp_report.md` | 20:31 | **FRESH** (2.75h) |
| Crypto intraday | `2026-06-24_17-48_intraday_report.md` | 20:48 | **FRESH** (2.5h) |
| Crypto swing | `2026-06-24_00-58_swing_report.md` | 03:58 | **STALE** (~19.3h) |
| Stocks intraday | `2026-06-24_19-36_stocks_intraday_report.md` | 22:36 | **FRESH** (0.75h) |
| Stocks swing | latest 2026-06-24_01-03 | ~04:03 | **STALE** (~19.2h) |
| Stocks invest | latest 2026-06-24_01-07 | ~04:07 | **STALE** (~19.2h) |
| Catalyst events | `data/catalysts/2026-06-24/catalyst_cycle_17-48.md` | ~18:00 UTC | FRESH |
| Prior review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-24_2139.md` | 21:39 | 1h36min ago |
| Active-signals CLI | crypto (15) + stocks (50) | ~23:15 | LIVE |
| Signal-stats CLI | crypto + stocks | ~23:15 | LIVE |
| Untracked alerts | detect_untracked_legacy_alerts | ~23:15 | **0 untracked** |
| BTC price | WebFetch: CryptoTimes ~23:28 EEST | Jun 24 ~23:28 | **$59,518** |
| ETH price | WebFetch: CryptoTimes | Jun 24 ~23:28 | **$1,566** |
| MU earnings | WebSearch: Yahoo Finance / TheStreet | Jun 24 post-close | **AH +6%** |
| UNH DOJ probe | WebSearch: QuiverQuant / Nasdaq | Jun 24 | **Confirmed −16%** |
| SPY/S&P close | WebSearch | Jun 24 close | **7,353 / −0.17%** |

**Blindspots:** Crypto swing/stocks swing/invest stale >19h. Reddit 403 persistent. TradingView/chart MCP unavailable. Onchain config missing. Derivatives OI numeric history sparse. Paper monitor data 94min stale (last at 21:21 cycle).

**External web research available and used.** BTC price, MU earnings, UNH DOJ probe all verified via WebSearch/WebFetch.

---

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: **23:24 EEST** — within 3h threshold ✓
- Latest cycle `cycle_07_20-09_summary.md` mtime: **21:21 EEST** (114min ago) — within 3h threshold ✓
- **NOT DEFERRED** — both freshness checks pass.
- Cycle 7 (20:09–21:21 EEST): **ok=23, failed=0** — clean run; last completed cycle of the day.
- Pre-tracking: checked=461, updated=12, tp_hits=283, stopped=4, expired=0.
- Post-tracking: checked=455, updated=13, tp_hits=283, stopped=4, expired=0. Revalidation: stale=3, moved_away=0.
- Paper monitor (21:21): **0 OPEN actionable · 1 WAITING · 29 ENTERED UNRESOLVED · 164 REVIEW/SHADOW · 36 NO-ENTRY/stale/moved-away · 288W/43L/0flat closed · Needs review: 1.**
- Stocks intraday report refreshed at 22:36 EEST by background stocks_monitor after cycle 7.
- Social failures: Reddit CryptoCurrency/Bitcoin/Ethereum 403 — persistent. Binance/MEXC universe lazy-cache (normal pattern).

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-06-24 23:15 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse", "onchain_config_missing"],
      "data_missing": ["swing_report_stale_19h", "stocks_swing_invest_stale_19h", "reddit_social_blocked_403", "onchain_config_missing", "oi_numeric_history_sparse", "paper_monitor_94min_lag"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_7_ok=23_failed=0_21:21_EEST", "scalp_fresh_2.75h", "intraday_fresh_2.5h", "stocks_intraday_fresh_0.75h", "0_untracked_alerts", "catalyst_events_1097_today_5_baskets_full_day"]
    },
    {
      "agent": "market_regime",
      "verdict": "risk_off",
      "confidence": 0.95,
      "reason_codes": ["risk_off", "shorts_preferred", "mixed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC_59518_down_5.1pct_since_21:39", "ETH_1566_downtrend_2.67x_volume", "altcoin_breadth_33pct_above_EMA20", "ETF_BTC_1D_-155M_7D_-410M_6_consecutive_weeks", "liquidations_861M_91pct_longs_168583_traders", "SPY_close_-0.17pct_732.49", "VIX_19.77_report_20.17_spike_late_session"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "ok",
      "confidence": 0.87,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": ["reddit_blocked", "x_twitter_not_live"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ADA_SecondFi_exploit_2.4M_20M_potential_5_sources", "BTC_ETF_outflows_lookonchain_confirmed_6_weeks", "MU_Q3_41.46B_vs_35.1B_Q4_49_51B_AH_+6pct_new_post_close", "UNH_DOJ_criminal_probe_Medicare_confirmed_QuiverQuant_Nasdaq_WSJ_-16pct", "Nasdaq_chip_rout_Jun23_semi_stocks_-11pct_reversal_pending"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["squeeze_risk", "post_unwind_chop", "data_unavailable"],
      "data_missing": ["liquidation_heatmaps", "oi_numeric_history_sparse", "bybit_oi_mexc_fallback"],
      "suggested_effect": "advisory_only",
      "facts_used": ["phase_5_post_unwind_chop_24_symbols", "phase_2_squeeze_expansion_3", "phase_1_build_up_10", "BTC_57300_liquidation_cluster_cited_CryptoSlate", "FIL_price_down_OI_up_squeeze_risk", "DOGE_long_short_2.26_deleveraging"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["entry_late", "chase_risk", "overextended"],
      "data_missing": ["tradingview_chart_mcp_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC_59518_after_5pct_crash_overextended_new_short", "ATM_31pct_24h_no_derivatives_entry_unclear", "ETH_swing_long_entered_now_in_loss_with_crash", "SMH_tomorrow_MU_beat_gap_watch_not_chase", "no_A_tier_any_mode"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.83,
      "reason_codes": ["no_entry", "waiting_for_entry", "entered_unresolved", "review_shadow", "needs_review"],
      "data_missing": ["paper_monitor_94min_lag"],
      "suggested_effect": "advisory_only",
      "facts_used": ["0_open_actionable_at_21:21", "JPM_B_long_triggered_in_current_cli", "LLY_B_long_triggered", "MSO_B_short_tp_hit", "29_entered_unresolved_at_21:21", "164_review_shadow", "36_no_entry_stale_moved_away", "needs_review_1_ETH_contradiction", "crypto_active_15_down_from_18", "stocks_active_50_monitor_generated"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.84,
      "reason_codes": ["daily_loss_pressure", "headline_risk", "legal_risk", "correlation_cluster", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ETH_swing_long_ENTERED_UNRESOLVED_contradicted_by_1566_crash", "BTC_approaching_57300_liquidation_cluster", "ADA_exploit_confirmed_AVOID", "UNH_DOJ_-16pct_AVOID_legal", "crypto_shorts_week_PF=0.8_historically_weak", "stocks_B_WR=0pct_n19_weak_sample", "861M_liquidation_cascade_overnight_risk"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.73,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_mode_n36_PF2.18_WR39pct_+19R_best", "crypto_longs_n44_PF4.0_WR54pct_+24R", "crypto_shorts_n106_PF0.8_WR14pct_-6R_net_negative_week", "crypto_exchange_confirmed_n57_PF2.60_+24R_quality_gate", "scalp_PF=0.57_losing", "intraday_PF=1.06_marginal", "stocks_B_n19_WR=0pct_PF=0.0_-7R", "stocks_C_n185_PF=0.50_-9R"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.88,
      "reason_codes": ["shorts_preferred", "wait_for_trigger", "manual_review", "catalyst_backed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC_59518_post_close_crash_key_event", "MU_AH_beat_semi_reversal_tomorrow_new", "ETH_needs_operator_review_contradicted", "BTC_swing_short_best_aligned_active", "ATM_only_RS_leader_long_watch_BTC_60k_trigger", "SMH_catalyst_watch_MU_RTH_tomorrow", "57300_watch_overnight"]
    }
  ],
  "head_trader": {
    "overall_verdict": "risk_off",
    "confidence": 0.88,
    "preferred_side": "shorts",
    "best_long_candidate": {
      "symbol": "ATM/USDT",
      "trigger": "BTC stabilizes and reclaims $60k + ATM pullback to ~$1.68–1.73 retest zone + volume > 1.0x avg — do NOT chase current extended price",
      "reason": "Only RS leader +31% vs BTC in risk-off; momentum_breakout basket; no specific catalyst confirmed — requires BTC regime stabilization before entry"
    },
    "best_short_candidate": {
      "symbol": "BTC/USDT",
      "trigger": "Active B-tier swing short already running; new entry only on dead-cat bounce retest $61,000–61,500 on 1h timeframe with 15m rejection confirmation",
      "reason": "BTC crashed to $59,518 breaking $60k; $57,300 liquidation cluster next; ETF 6-week outflow streak; $861M liquidations 91% longs; regime deeply risk-off; directionally aligned"
    },
    "best_catalyst_candidate": {
      "symbol": "SMH",
      "trigger": "RTH open Thursday — gap-up above $620 with volume; wait 15-30min for RTH stabilization (09:45-10:00 ET = 16:45-17:00 EEST) before entry; do NOT pre-market chase",
      "reason": "MU Q3 $41.46B vs est $35.1B beat; Q4 $49-51B vs est $43.2B guide; MU +6% AH; semis led prior-day rout, beat reversal could lift SMH/QQQ Thu"
    },
    "avoid_candidate": {
      "symbol": "ETH/USDT",
      "reason": "B-tier swing long ENTERED UNRESOLVED; ETH crashed to $1,566; contradicted by $69M 1D ETF outflows, $172M 7D, $861M total liquidations 91% longs; operator must review before Asia open"
    },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason Codes | Suggested Effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale (swing/invest >19h), derivatives_sparse, onchain_config_missing | advisory_only |
| market_regime | risk_off | 0.95 | risk_off, shorts_preferred, mixed (stocks mild negative close) | advisory_only |
| catalyst_narrative | ok | 0.87 | fresh_catalyst (MU beat AH + ADA exploit confirmed), catalyst_confirmed (ETF outflows), narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk ($57.3k cluster), post_unwind_chop (24 symbols), data_unavailable (heatmaps/OI) | advisory_only |
| technical_entry | caution | 0.72 | entry_late/chase_risk (BTC after -5%), overextended (most crypto), SMH wait RTH | advisory_only |
| execution_lifecycle | ok | 0.83 | no_entry (0 open), waiting→triggered (JPM/LLY), entered_unresolved (29+), needs_review (ETH contradiction) | advisory_only |
| risk_manager | caution | 0.84 | daily_loss_pressure, headline_risk (MU/UNH/ADA), legal_risk (UNH confirmed -16%), correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | ok | 0.73 | playbook_working (crypto swing PF=2.18, longs PF=4.0), playbook_failing (scalp/intraday, stocks B WR=0%), low_sample | advisory_only |
| head_trader | caution | 0.88 | shorts_preferred, wait_for_trigger (ATM/SMH), manual_review (ETH), catalyst_backed (SMH Thu RTH) | advisory_only |

---

## 4. What Changed vs Previous Review (21:39)

| Metric | 21:39 Review | Now (23:15) | Delta |
|---|---|---|---|
| BTC price | ~$62,729 | **~$59,518** | **−$3,211 (−5.1%)** ⚠️ |
| ETH price | not quoted | ~$1,566 | post-close crash |
| 24h liquidations | $706M (84% longs) | **$861M (91% longs)** | **+$155M escalation** |
| Open actionable | 0 | 0 (est) | unchanged |
| Waiting for entry | 1 (JPM) | 0 (JPM triggered) | −1 |
| Crypto active signals | 18 | 15 | −3 (resolved overnight) |
| Stocks active signals | 20 | 50 | +30 (monitor RTH additions) |
| SPY close | open session | 732.49 (−0.17%) | US closed mildly neg |
| VIX | 20.17 (spike) | ~19.77 (from report) | slight pullback at close |
| MU Micron | expected AH | **+6% AH** | **NEW catalyst** |
| UNH DOJ | flagged | **Confirmed −16%** | AVOID confirmed |
| BTC $60k level | above | **BROKEN** | key level lost |

**Key developments since 21:39:**
1. **BTC broke $60k and fell to $59,518** — $57,300 liquidation cluster now exposed ($2.2k away).
2. **MU massive AH beat** — semi reversal setup for Thu RTH (new vs prior review).
3. **Liquidations escalated** $706M → $861M with long dominance rising 84% → 91%.
4. **JPM B long** and **LLY B long** both triggered during RTH session; **MSO B short** hit TP.
5. **3 crypto signals resolved** since cycle 7 (WLFI scalp/swing, likely STX intraday — natural lifecycle).
6. **ADA exploit**: no new development; thesis unchanged — AVOID all longs.
7. **ETH entered unresolved**: further deteriorated with crash — now more urgently needs operator review.

---

## 5. Catalyst Coverage

**Full day:** 1,097 unique events processed, 5 baskets generated.
**Latest scan (cycle_17-48):** 500 events scanned, 3 baskets.

| Metric | Value |
|---|---|
| Total catalyst events (full day) | 1,097 |
| Narrative baskets (full day) | 5 |
| exploit_hack | 4 (ADA ×3, DeFi TVL basket) |
| partnership | 4 |
| analyst_action | 4 |
| regulatory_sector_headline | 3 |
| other_news (dominant type) | 474+/500 in latest scan |
| Estimated unmapped (null symbol) | >50% (estimated from basket quality) |

⚠️ **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** `other_news` dominates (474+/500). `delisting_thin_liquidity` basket shows no primary/related symbol with sports headlines (Atlético Madrid, Lionel Messi) — spurious. Estimated >50% of events lack symbol mapping.

**Top 3 unmapped/basket-only headlines:**
1. "TWO DEAD IN ISRAELI DRONE STRIKE ON VEHICLE IN SOUTHERN LEBANON" — geopolitical rumour, no crypto symbol
2. "How memecoin marketing moved from online speculation to real-world risk" — basket-level, no primary symbol
3. "Atlético Madrid agrees to sign Alejandro Grimaldo for €20M as fan token ecosystem grows" — sports, in `delisting_thin_liquidity` spuriously

**High-confidence catalysts (symbol-mapped / primary source):**
- ADA: SecondFi exploit ×5 sources (importance 0.86–0.88)
- BTC: ETF outflows + $10.6B options expiry (confirmed)
- BNB/ASTER: YZi Labs BNB ecosystem (0.65)
- PLTR: Zeta-Palantir partnership (0.68)
- MU: Earnings beat post-close (external; not yet in JSONL)
- UNH: DOJ criminal probe (external; not in JSONL)

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off (deepening). BTC crashed below $60k to $59,518. ETH $1,566. $861M liquidations (91% longs). Altcoin breadth 33% above EMA20. ETF 6-week outflow streak. System recommendation: "short bias or no trade; avoid weak altcoin longs."
- **Stocks mood:** chop → mildly negative close (SPY −0.17%). Session was turbulent (VIX 20.17 spike, chip sector rout) but closed calmly. Post-close MU beat changes tomorrow's semi setup.
- **Dominant narrative:** Crypto risk-off driven by macro (Nasdaq chip rout from Asia, Fed rate-hike expectations ~90% year-end, ETF 6-week outflow). ADA structural exploit. Stocks: chop with semiconductor reversal pending.
- **Preferred side now:** Shorts on crypto (BTC active). Catalyst-backed watch on SMH (Thu RTH only).
- **Best long candidate:** ATM/USDT — trigger: BTC above $60k + retest $1.68–1.73 + volume. Do not chase.
- **Best short candidate:** BTC/USDT — active swing short running. New entry on bounce to $61k–61.5k retest only.
- **Best catalyst-backed candidate:** SMH (stocks) — MU AH +6% beat. Wait RTH open Thursday.
- **What to avoid:** ETH long (entered unresolved, contradicted), ADA (exploit), UNH (DOJ), weak altcoin longs, new shorts on overextended breakdowns.
- **What would change the view:** BTC 1h close above $62,500 → flip to neutral/watch. MU beat sustaining semis through first 30 min RTH → SMH long entry. BTC break of $57,300 → cascade watch, do not add longs.

---

## 7. Candidate Deep Dives

### Candidate 1 — ETH/USDT swing long B-tier (ENTERED UNRESOLVED — operator review required)

- **Status:** ENTERED UNRESOLVED (entry was filled; no TP/SL confirmed before window; 0R display = unresolved, not a flat close — NOT a missed entry)
- **Score:** 66.3 (B-tier swing long)
- **Current ETH price:** ~$1,566 (post-close, down significantly)

**Contradiction analysis:**
- ETH ETF outflows: 1D −$69M / 7D −$172M (6-week streak)
- $861M total crypto liquidations, long-dominated (91%)
- ETH trend: downtrend. Volume 2.67× average — breakdown structure
- L2 ecosystem: negative (broader)
- AAVE v4 deposits ($200M) = only partial counter — not a price catalyst
- **Contradiction verdict: STRONG.** This swing long is contradicted by trend, ETF flows, and market structure.
- Entry fresh? No — position entered; now in the hole as ETH fell with BTC.
- Chase risk: N/A (already entered). Risk = continuation of loss.
- Actionable NOW? No. **OPERATOR REVIEW REQUIRED before Asia open.** Determine if stop was set by post-cycle tracking; if still open without stop, consider manual close or stop placement.
- Invalidation of the thesis: Any 1h close below prior swing support level (TradingView unavailable; chart check needed by operator). At $1,566 post-crash, thesis is functionally invalidated.

### Candidate 2 — BTC/USDT swing short B-tier (OPEN — directionally aligned, best active signal)

- **Score:** 65.5 (B-tier swing short)
- **Direction:** short — ALIGNED with crash
- **BTC current:** $59,518 (broke $60k post-US close)
- **$57,300:** next liquidation cluster (cited: CryptoSlate, multiple sources)

**Analysis:**
- Regime: BTC downtrend, altcoin breadth 33%, ETF outflow 6 weeks → perfectly aligned
- Catalyst: ETF outflows confirmed (BTC 1D −$155M, 7D −$410M), whale closed 800 BTC long at −$1.26M loss (t.me/lookonchain), Binance sees $479M panic-selling inflows
- Price reaction to catalyst: Yes — price already moved with catalyst (−5.1% since 21:39)
- Setup chasing NOW? **Yes** — BTC after −5.1% crash is overextended. Do NOT open new short at $59.5k.
- New entry trigger: dead-cat bounce retest to $61,000–61,500 zone on 1h, then 15m rejection candle.
- ATR/EMA stretch: likely >2 ATR from EMA20 (chart unavailable; inferred from 5.1% single-session move)
- Playbook note: week shorts PF=0.8 (net negative). BTC directional swing is the highest-quality short in the system (multi-source catalyst, regime-aligned, B-tier confirmed).
- Invalidation: 1h close above $62,500. $60k reclaim would weaken the thesis.

### Candidate 3 — ATM/USDT B-tier swing long (WAITING — best long-watch in risk-off)

- **Score:** 67.3 (B-tier swing long, weekend flag not set)
- **24h performance:** +31.79% vs BTC (+36.05% RS) — strongest RS in the system
- **Derivatives:** futures data unavailable — significant blind spot

**Analysis:**
- In `momentum_breakout` basket (primary: ATM, SYN, SAHARA) — basket fresh <1h
- RS 31-36% vs BTC in a deeply risk-off session is exceptional; implies accumulation or unverified catalyst
- Regime risk: BTC now below $60k, heading for $57.3k cluster. ATM is NOT immune to BTC cascade.
- Has price already reacted to catalyst? Unclear — no specific verified catalyst found in news_items or catalyst_events. RS leadership may be exchange-listing or social hype (not verified).
- Chase risk: HIGH. +31% in one day without verified catalyst or derivatives data.
- Retest/pullback structure: wait for retest to ~$1.68–1.73 if ATM has moved from a lower base. Do not buy extension.
- Would entry now be late? Yes — current extended price is not the entry.
- Actionable now? **No — WATCHLIST ONLY.** Trigger: BTC stabilizes above $60k + ATM pullback to zone + volume > 1.0× avg + derivatives data available.
- Catalyst confirmation: MISSING. External search for "ATM/USDT catalyst June 24 2026" not performed (no clear ticker to search). Remains unverified.

### Candidate 4 — UNH stocks (LEGAL/HEADLINE RISK — AVOID)

- **Status:** Active C-tier long (triggered during RTH)
- **⛔ LEGAL/HEADLINE RISK CONFIRMED:**
  - DOJ criminal investigation for Medicare Advantage fraud (WSJ, QuiverQuant, Nasdaq — multi-source)
  - DOJ investigation extends to Optum Rx and physician reimbursements (FierceHealthcare)
  - UNH −16% today; five-year low
- **Verdict: AVOID ALL UNH LONGS.** Any active C-tier UNH long signal must be flagged for lifecycle review. This is a structural legal event.
- **UNH short possibility:** −16% today is overextended for new short entry. Watch for dead-cat bounce to resistance → short retest. Not actionable today; plan for Thu if relief bounce occurs.
- Cite: [QuiverQuant](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe,+Shares+Dive+16%25+on+Fraud+Investigation) Jun 24, 2026.

### Candidate 5 — SMH / semiconductor setup (CATALYST-WATCH for Thu RTH — Micron AH beat)

- **Status:** C-tier short (system, score 58.37) + NEW post-close AH catalyst reversing the thesis
- **MU catalyst (post-close):**
  - Q3 revenue: $41.46B vs est $35.1B (+18% beat)
  - Q4 guidance: $49–51B vs est $43.2B (+13–18% beat)
  - MU +6% AH
- **Context:** Semi sector led prior-day Nasdaq rout (chip stocks −11% Jun 23, KOSPI circuit breaker). MU beat creates reversal setup for the whole sector.
- **System signal contradiction:** C-tier SMH short is now CONTRADICTED by MU AH beat for tomorrow. Do not trade the short on SMH Thursday.
- **Tomorrow setup (Thu RTH):**
  - Watch: SMH gap-up likely at open (MU is a major SMH constituent, ~9% weight)
  - Action plan: Wait 15–30 min after RTH open (09:45–10:00 ET) for stabilization
  - Entry trigger: SMH opens above $620 + first 15-min candle closes green + volume confirmation + QQQ above open level
  - Do NOT pre-market chase: gap-up may exhaust early
- **Legal risk bleed:** UNH (−16%) is in XLV, not SMH. No direct semi correlation.
- Actionable overnight? No. Planning note only.

---

## 8. Best Candidates Ranked

Post-close/overnight context — planning and watches only, not active entries:

| Rank | Symbol | Class | Side | Status | Trigger | Confidence |
|---|---|---|---|---|---|---|
| 1 | BTC/USDT | crypto swing | short | ACTIVE (entered, running) | Already running; new entry only on bounce to $61k–$61.5k retest | high |
| 2 | SMH | stocks intraday | long | CATALYST-WATCH Thu | RTH open Thursday: gap above $620 + 15-min RTH confirmation | medium |
| 3 | ATM/USDT | crypto swing | long | WATCHLIST | BTC above $60k + ATM pullback $1.68–1.73 + volume | low-medium |
| 4 | WLD/USDT | crypto swing | short | WATCHLIST | Failed bounce retest 0.507–0.515 + BTC below $60k | medium |

**On shorts:** Historical week PF on crypto shorts = 0.8 (net negative). Only trade the BEST-confirmed short (BTC, directionally aligned, active). Do not open new altcoin shorts on overextended breakdowns — wait for retest.

No clean new entries exist for the overnight window (23:15–04:30 EEST). Best overnight actions: monitor ETH unresolved position, watch BTC around $57.3k.

---

## 9. Avoid / No Trade

**This decision window only — does not stop the system. Scanning and tracking continue.**

- **ETH/USDT long:** ENTERED UNRESOLVED, deeply contradicted. Operator review required NOW, before Asia liquidity increases.
- **ADA/USDT:** AVOID all longs. Exploit ongoing, systemic Cardano wallet vulnerability. Short only on confirmed dead-cat bounce to resistance (not actionable today — overextended).
- **UNH:** AVOID all longs. DOJ criminal probe confirmed. −16% today.
- **Weak altcoin longs:** Regime risk-off, 67% of tracked coins below EMA20. No new altcoin longs without RS-leader qualification AND BTC above $60k.
- **Scalp (overnight):** Scalp mode PF=0.57 (losing). No A/B scalp signals. Not suitable for overnight Asia session with low liquidity.
- **SMH short (system C-tier):** Contradicted by MU AH beat. Do not execute system short on SMH Thursday.
- **New crypto shorts on current breakdown:** BTC at $59.5k post −5.1% move is overextended. Wait for retest to $61k–$61.5k before any new short entry.

---

## 10. Main Risks

1. **BTC cascade to $57,300** — liquidation cluster. BTC at $59,518, only $2.2k away. A break below $57,300 could trigger forced closes across the 29 entered-unresolved crypto positions.
2. **ETH swing long unresolved** — if BTC falls to $57.3k, ETH follows. Unresolved long position amplifies downside. Requires operator intervention before Asia open.
3. **MU beat gap-trap** — semis gap-up Thu morning, then fail as early buyers exhaust. Do not pre-market chase. RTH 15-min confirmation required.
4. **ADA contagion** — $20M+ Cardano exploit could spread confidence crisis to other PoS chains; monitor narrative contagion overnight.
5. **PCE data watch** — upcoming economic release (date not confirmed). If PCE hot, reinforces rate-hike pricing (~90% year-end), negative for risk assets including crypto and QQQ.
6. **Derivatives blind spots** — OI history sparse; no liquidation heatmaps. The $57,300 cluster is from external news, not internal data.
7. **Stocks B-tier performance** — WR=0%, PF=0.0 (n=19 weak sample). JPM and LLY triggered today; outcomes unclear until tomorrow's tracking.

---

## 11. Action Plan — next 4 hours (23:15–03:15 EEST / Asia early session)

1. **IMMEDIATE — ETH operator review:** Check ETH/USDT swing long in DB. If still OPEN without stop → evaluate manual close (ETH $1,566, thesis contradicted). Do not carry an unprotected long into Asia.
2. **BTC watch — $57,300:** Monitor BTC. If price breaks $58,000 → do not add any long exposure. If BTC reaches $57,300–57,500 → watch for capitulation/bounce signal; do not chase new short below $59k.
3. **ATM/USDT conditional watch:** If BTC stabilizes above $59k-60k overnight and ATM retests ~$1.68–1.73, becomes conditional long watch. Volume required. No entry until BTC regime confirms.
4. **WLD/USDT:** Still the best C-tier short-watch. If price retests 0.507–0.515 on failed bounce + BTC below $60k → entry consideration.
5. **SMH/MU Thu planning:** Prepare thesis. No pre-market action. Wait RTH open ~16:30 EEST Thursday.
6. **Scanning continues normally.** No pauses in data collection, signal generation, or paper tracking overnight.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Rationale |
|---|---|---|
| **Crypto scalp** | NO-TRADE (this window) | Scalp PF=0.57 (losing), no A/B signals, BTC overextended, overnight low liquidity |
| **Crypto intraday** | WAIT FOR TRIGGER | WLD/USDT short-watch needs retest confirmation; no clean new intraday entries in risk-off |
| **Crypto swing** | ACTIVE — monitor | BTC swing short running (best active position); ETH swing long needs urgent operator review |
| **Stocks intraday (today's session)** | CLOSED | JPM/LLY triggered, MSO short TP'd; outcomes tracked tomorrow |
| **Stocks intraday (Thu RTH)** | CATALYST-WATCH — SMH/MU | Wait RTH confirmation; UNH AVOID; do not pre-market chase |
| **Stocks swing/invest** | PLANNING ONLY | Reports stale 19h. Context only. |
| **Paper portfolio** | REVIEW — ETH urgent | ETH entered-unresolved requires operator decision before Asia open |

---

## 13. Sources

- [Crypto Market Crash: Wipes out $861M — CryptoTimes](https://www.cryptotimes.io/2026/06/24/crypto-market-crash-wipes-out-861m-as-btc-eth-xrp-bnb-sol-price-drops/) — Jun 24, 2026 (~23:28 EEST) — BTC $59,518, ETH $1,566, $861M liquidations, 91% longs
- [Bitcoin price today Jun 24 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-june-24-2026-opened-at-lowest-levels-in-about-two-weeks-125349040.html) — BTC opened at two-week low; $62,729 mid-session
- [Bitcoin price Jun 24 — Fortune](https://fortune.com/article/price-of-bitcoin-06-24-2026/) — BTC $62,520 early EDT; −4.47% weekly; down $13,961 from May peak
- [America's Bitcoin buying turns negative — CryptoSlate/StealthEx](https://stealthex.io/blog/why-is-bitcoin-dropping/) — $57,300 liquidation cluster cited
- [Micron tops Q3 estimates — Yahoo Finance](https://finance.yahoo.com/technology/article/micron-to-report-third-quarter-earnings-amid-sky-high-demand-from-data-centers-113000152.html) — Jun 24, 2026 — MU Q3 $41.46B revenue, Q4 guide $49-51B, +6% AH
- [Micron June 24 Earnings Preview — TradingKey](https://www.tradingkey.com/analysis/stocks/us-stocks/261975340-mu-q3-earnings-preview-june-2026-tradingkey) — consensus est. $35.1B revenue, EPS $20.39
- [Micron Q3 Earnings Call — TheStreet](https://www.thestreet.com/latest-news/micron-mu-q3-2026-earnings-call-updates) — Jun 24, 2026 live updates
- [UNH DOJ Probe — QuiverQuant](https://www.quiverquant.com/news/UnitedHealth+(UNH)+Faces+DOJ+Probe,+Shares+Dive+16%25+on+Fraud+Investigation) — Jun 24, 2026 — UNH −16%, criminal Medicare fraud probe confirmed
- [UNH DOJ Probe — Nasdaq](https://www.nasdaq.com/articles/unitedhealth-unh-faces-doj-probe-shares-dive-16-fraud-investigation) — Jun 24, 2026 — multi-source confirmation
- [UnitedHealth under criminal probe — Yahoo Finance/WSJ](https://finance.yahoo.com/news/unitedhealth-under-criminal-probe-possible-231729520.html) — DOJ criminal probe Medicare Advantage
- [DOJ probe extends to Optum Rx — FierceHealthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) — scope expansion
- [SPY Rebound — InteractiveCrypto](https://www.interactivecrypto.com/spy-s-rebound-must-prove-it-can-survive-micron-and-pce-jun-2026) — SPY +0.33% intraday / PCE data upcoming
- Internal: `cycle_07_20-09_summary.md` (2026-06-24 20:09–21:21 EEST)
- Internal: `2026-06-24_17-31_scalp_report.md`, `2026-06-24_17-48_intraday_report.md`, `2026-06-24_19-36_stocks_intraday_report.md`
- Internal: `data/catalysts/2026-06-24/catalyst_cycle_17-48.md`, `catalyst_events.jsonl`
- Internal: active-signals CLI, signal-stats CLI, detect_untracked_legacy_alerts (~23:15 EEST)

---

## 14. Fix Requests / TODO

### TODO-swing-stale-daily
- **issue:** Crypto swing report (and stocks swing/invest) consistently stale >19h at post-close slot — last cycle runs only scalp/intraday; swing not regenerated since 00:58 EEST
- **evidence:** `data/reports/swing/2026-06-24_00-58_swing_report.md` mtime 03:58 EEST; cycle_07 steps confirm no swing refresh during evening
- **suggested manual fix:** Add swing report refresh to the evening scheduler cycle (e.g. cycle 7); or trigger swing on-demand in the post-close slot
- **priority:** medium
- **first observed:** 2026-06-24 23:15 EEST

### TODO-catalyst-mapping-weak-persistent
- **issue:** Catalyst mapping estimated >50% unmapped for multiple runs; `delisting_thin_liquidity` basket contains sports/geopolitical headlines (Atlético Madrid, Israeli drone strike) with no primary/related symbol — symbol resolver over-broad
- **evidence:** `data/catalysts/2026-06-24/catalyst_cycle_17-48.md` — delisting basket: primary=empty, related=empty; sample headlines = non-crypto; `other_news` dominates 474/500
- **suggested manual fix:** Tighten symbol-resolver logic; add domain/category filter to discard sports/geopolitical text from crypto baskets; audit `other_news` mapping completeness
- **priority:** medium
- **first observed:** 2026-06-24 23:15 EEST (pattern across multiple daily reviews)

### TODO-eth-swing-long-operator-review
- **issue:** ETH/USDT B-tier swing long ENTERED UNRESOLVED; actively contradicted by ETF outflows ($69M 1D, $172M 7D), $861M liquidations, ETH downtrend. No confirmed stop in place per paper monitor status. Needs urgent operator decision.
- **evidence:** active-signals CLI shows ET B sw lo 66.x; paper monitor 21:21 shows 29 entered-unresolved + needs_review=1; ETH market ~$1,566 post-close (down with BTC crash)
- **suggested manual fix:** Operator session: check ETH signal stop placement; if no stop set, consider manual close or place stop at prior swing low. Add automated step to assign stops to entered-unresolved swing signals within 1 cycle.
- **priority:** high
- **first observed:** 2026-06-24 21:39 EEST (escalated 23:15 with further ETH decline)

### TODO-stocks-B-winrate-zero
- **issue:** Stocks B-tier performance this week: WR=0%, PF=0.0, −7R (n=19, weak confidence). Flags persistently appear across multiple cycle runs. Signals generating but not converting.
- **evidence:** cycle_07 signal-stats stocks: `(weak, n=19) tier=B: triggered winrate 0%`; `profit factor 0.00 below 0.8`; stocks intraday report confirms WR=10.5% even in its local week window (slightly better sample)
- **suggested manual fix:** Manual Opus session: review stocks B-tier scoring criteria for chop/VIX>20 regime; consider regime-gate (suppress B-tier stocks intraday when VIX > 20 + SPY in range); check whether RR_below_1.5 rejections indicate entry zone calibration issue
- **priority:** medium
- **first observed:** 2026-06-24 23:15 EEST
