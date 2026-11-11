# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

_Generated 2026-06-25 04:39 EEST (Thursday). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

---

## 1. Executive Summary

**Thu 2026-06-25, 04:39 EEST — crypto overnight / Asia review — advisory only / no auto-trade.**

Stocks are **CLOSED** (US pre-market, planning only). Crypto is the live actionable class.

- **Crypto: RISK-OFF confirmed overnight.** BTC crashed from $62,729 (24 Jun) → $59,518 (23:15 EEST) → bounced to **$60,753** (−3.36% 24h) at review time. ETH $1,616 (−3.23%). Fear & Greed Index: **24 (Extreme Fear)**. $861M liquidated in 24h (91% longs, 168K traders). BTC/ETH both remain in confirmed **downtrend**. Altcoin breadth above EMA20: **24–25%** (very low).
- **BTC/USDT swing short (B-tier, active):** Entry ~$62k, current $60,753 — signal is approximately **in profit** on the short side. The move is 3 days in progress. A retest of $61,200–62,000 supply zone would be the next clean short trigger; do NOT re-enter at current levels (chase risk).
- **ETH/USDT swing long (ENTERED UNRESOLVED):** Entered near $1,600 zone, crashed to $1,566, bounced to $1,616. Directly contradicted by regime. **Operator review required** before adding to this position.
- **ATM/USDT:** RS leader +27% vs BTC in 24h (score 91.6), B-tier swing long active. Best long-watch candidate in the risk-off landscape — **only valid on pullback** to $1.10–1.15 zone and only if BTC holds above $60k.
- **Playbook contradiction:** Regime says risk-off/shorts, but this week crypto longs are PF 4.0 (+24R) vs shorts PF 0.8 (−6R). Cross-exchange-confirmed swings are the winning bucket (PF 2.6). **Do not chase shorts into the bounce.** Wait for BTC retest.
- **ADA/USDT: AVOID** — SecondFi exploit $2.4M ($20M potential) confirmed. **UNH: AVOID** — DOJ criminal probe confirmed (−16%). Both carry-forward from prior review.
- **Stocks (closed / planning):** JPM B-tier likely triggered near $33x. MU/Micron AH earnings beat (+6% AH, Q3 $41.5B vs est $35.1B) sets up a semiconductor watch for Thursday RTH open — SMH/NVDA/QQQ as longs on gap-up confirmation.
- **Overnight/Asia setup:** BTC holding $60.7k; next key level $57.3k (liquidation cluster). Watch for failed bounce at $61–62k as short trigger. ATM pullback is the best long watch.

---

## 2. Data Used

| Source | File / Path | mtime EEST | Freshness |
|---|---|---|---|
| scheduler.log (2025-06-25) | `data/scheduled_runs/2026-06-25_default_schedule/scheduler.log` | 04:26 | **FRESH** (13min) |
| Cycle 1 status | In progress (scalp done 04:37; intraday still running) | 04:37 | **IN PROGRESS** |
| Crypto scalp report | `2026-06-25_01-37_scalp_report.md` | 04:37 | **FRESH** (2min) |
| Crypto intraday report | `2026-06-25_01-17_intraday_report.md` | 04:17 | **FRESH** (22min) |
| Crypto swing report | `2026-06-24_00-58_swing_report.md` | 03:58 yesterday | **STALE** (~28h) |
| Stocks intraday report | `2026-06-25_01-23_stocks_intraday_report.md` | 01:23 | **CARRY-FORWARD** (3.2h) |
| Stocks swing report | `2026-06-24_01-03_stocks_swing_report.md` | ~04:03 yesterday | **STALE** (~28h) |
| Catalyst events | `data/catalysts/2026-06-25/catalyst_cycle_01-17.md` | 04:17 | **FRESH** (22min) |
| LLM packets | Not read (in-cycle, may be partial) | — | Not used |
| Active-signals CLI | crypto (13) + stocks (50+) | 04:39 | LIVE |
| Signal-stats CLI | crypto + stocks | 04:39 | LIVE |
| Untracked alerts | detect_untracked_legacy_alerts --since 2026-06-25 | 04:39 | **0 untracked** |
| BTC/ETH live price | CoinDesk WebFetch 04:39 EEST | 2026-06-25 04:39 | **$60,753 / $1,616** |
| $861M crash article | CryptoTimes WebFetch | 2026-06-24 | **Confirmed** |
| Prior review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-24_2315.md` | 23:45 | 5h ago |

**Blindspots:** Crypto swing stale >28h (use with caution). Stocks swing/invest stale >28h. Bybit OHLCV failed 54 symbols in intraday run (degraded derivatives context). Reddit 403 persistent. TradingView/chart MCP unavailable. Paper monitor last known 21:21 EEST yesterday (cycle 1 in progress, today's count not yet available). Onchain config missing.

**External web research available.** BTC/ETH live prices and $861M crash narrative verified via WebFetch/WebSearch.

---

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime (2026-06-25 folder): **04:26:52 EEST** — within 3h threshold ✓
- Latest cycle: **Cycle 1/12 IN PROGRESS** — scalp report completed 04:37, intraday running now
- **NOT DEFERRED** — scheduler.log is 13 min old, well within 3h.
- Yesterday's final cycle (2026-06-24, cycle 9): ended **04:25:52 EEST** — ok=22, failed=1, telegram=sent.
- Pre/post tracking from yesterday cycle 9: checked=455, tp_hits=283, stopped=4, expired=0.
- Paper monitor (last known 21:21 EEST, Jun 24): **0 OPEN actionable · 1 WAITING · 29 ENTERED UNRESOLVED · 164 REVIEW/SHADOW · 36 NO-ENTRY/stale/moved-away · 288W/43L/0flat CLOSED · Needs review: 1**.
- Active crypto signals: **13** (all B-tier). Active stocks signals: **50+** (mostly C-tier, 2 B-tier).
- Social failures: Reddit CryptoCurrency/Bitcoin/Ethereum 403 persistent. Bybit OHLCV partial (54 failures in intraday).

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-06-25 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse", "onchain_config_missing"],
      "data_missing": ["swing_report_stale_28h", "stocks_swing_invest_stale_28h", "bybit_ohlcv_failed_54_intraday", "reddit_403_persistent", "onchain_config_missing", "oi_history_sparse", "paper_monitor_cycle1_pending"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler_log_04:26_13min", "scalp_fresh_2min", "intraday_fresh_22min", "catalyst_fresh_22min", "0_untracked_alerts", "cycle1_in_progress"]
    },
    {
      "agent": "market_regime",
      "verdict": "risk_off",
      "confidence": 0.95,
      "reason_codes": ["risk_off", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC_60753_downtrend_3.36pct_24h", "ETH_1616_downtrend_3.23pct_24h", "breadth_EMA20_24to25pct", "atr_82nd_percentile_elevated", "861M_liquidations_91pct_longs_168K_traders", "fear_greed_24_extreme_fear", "fed_rate_hike_90pct_priced", "altcoin_breadth_25pct_very_low"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "stale_catalyst", "narrative_supported"],
      "data_missing": ["x_twitter_not_live", "reddit_blocked_403", "social_attention_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ADA_SecondFi_2.4M_exploit_CoinDesk_CryptoSlate", "THORChain_10.7M_exploit_AMBCrypto", "DeFi_TVL_minus39pct_2026_Cointelegraph", "MU_41.5B_Q3_beat_AH_plus6pct", "UNH_DOJ_probe_minus16pct", "Fed_rate_hike_90pct_priced", "470_events_6_baskets_94pct_other_news"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["squeeze_risk", "post_unwind_chop", "data_unavailable"],
      "data_missing": ["liquidation_heatmaps", "oi_numeric_history_sparse", "bybit_ohlcv_54_failures"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PUMP_price_down_OI_up_LS_0.604_squeeze_risk", "INJ_price_down_OI_up_LS_3.27pct_squeeze", "FIL_price_down_OI_up", "MEGA_price_down_OI_up", "BTC_bounce_59518_to_60753_partial_short_squeeze", "CELO_price_up_OI_up_22pct_fresh_positioning"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry"],
      "data_missing": ["tradingview_chart_mcp_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC_short_entry_62k_now_60753_1247_below_entry", "ATM_27pct_24h_overextended_low_vol_0.08x", "no_A_tier_any_crypto_mode", "all_scalp_C_tier_scores_56_to_63", "ETH_long_near_entry_1600_but_regime_contradiction"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "needs_review",
      "confidence": 0.60,
      "reason_codes": ["entered_unresolved", "needs_review", "waiting_for_entry"],
      "data_missing": ["paper_monitor_today_cycle1_pending", "exact_BTC_signal_status"],
      "suggested_effect": "advisory_only",
      "facts_used": ["last_known_21:21_29_entered_unresolved", "ETH_swing_long_entered_unresolved_regime_contradiction", "BTC_swing_short_likely_in_profit_entry_62k_now_60753", "13_active_crypto_signals_all_B", "1_WAITING_stocks_JPM_likely_triggered", "288W_43L_closed"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["correlation_cluster", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_shorts_PF_0.8_minus6R_week", "stocks_shorts_PF_0.1_minus20R_week", "scalp_PF_0.57_minus3R", "weekend_approaching_PF_0.68_vs_1.92_weekday", "all_altcoins_correlated_BTC_risk_off", "BTC_bounce_creates_squeeze_on_short_runners"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_PF_2.18_plus19R_best", "crypto_longs_PF_4.0_plus24R_vs_shorts_PF_0.8_minus6R", "cross_exchange_PF_2.6_vs_single_PF_0.76", "stocks_B_tier_WR_10.5pct_PF_0.375_minus5R_weak_sample", "stocks_shorts_PF_0.1_minus20R_catastrophic", "scalp_PF_0.57_low_confidence_mode"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.78,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": {
      "symbol": "ATM/USDT",
      "trigger": "Pullback to $1.10–1.15 zone + BTC holds above $60k on Asia close",
      "reason": "RS leader +27–29% vs BTC, B-tier swing long, score 91.6 all modes, low vol needs pullback before entry"
    },
    "best_short_candidate": {
      "symbol": "BTC/USDT",
      "trigger": "Failed bounce retest of $61,200–62,000 supply zone on declining volume",
      "reason": "B-tier swing short in profit from $62k, regime-aligned, $57.3k next liquidation cluster, stop ~$63k"
    },
    "best_catalyst_candidate": {
      "symbol": "SYN/USDT",
      "trigger": "Pullback to prior-session base + volume reclaim ≥0.8x 20-period avg",
      "reason": "Primary of momentum_breakout basket (fresh <1h), intraday score 91.6, +18.9% 24h — pure momentum, no news catalyst"
    },
    "avoid_candidate": {
      "symbol": "ETH/USDT (swing long) + ADA/USDT + any scalp short",
      "reason": "ETH entered unresolved vs regime; ADA SecondFi exploit $2.4M AVOID; scalp short bucket PF 0.57 / -3R"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | **ok** | 0.85 | scheduler_fresh, report_stale, derivatives_sparse, onchain_config_missing | advisory_only |
| market_regime | **risk_off** | 0.95 | risk_off, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | **caution** | 0.80 | fresh_catalyst, catalyst_confirmed, stale_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | **caution** | 0.65 | squeeze_risk, post_unwind_chop, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.72 | entry_late, chase_risk, stale_before_entry | advisory_only |
| execution_lifecycle | **needs_review** | 0.60 | entered_unresolved, needs_review, waiting_for_entry | advisory_only |
| risk_manager | **caution** | 0.75 | correlation_cluster, manual_review, reduce_risk | advisory_only |
| playbook_performance | **caution** | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |

**Head Trader synthesis:** `caution` / `wait_for_trigger` · Long-watch: ATM pullback to $1.10–1.15 · Short-watch: BTC retest $61.2–62k · Catalyst-watch: SYN pullback · Avoid: ETH long (entered/contradicted), ADA, scalp shorts

---

## 4. What Changed vs Previous Review

_Previous: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-24_2315.md` (23:15 EEST, ~5.4h ago)_

| Change | Detail |
|---|---|
| BTC price | $59,518 (23:15) → $60,753 (04:39) — overnight bounce **+$1,235 (+2.1%)** |
| ETH price | $1,566 (23:15) → $1,616 (04:39) — bounce **+$50 (+3.2%)** |
| Active crypto signals | 15 → 13 — **2 signals closed or expired** since 23:15 |
| Stocks signals | 50 active (unchanged range) — market closed overnight |
| JPM | Was "1 WAITING" at 23:15 → now shows "triggered" in active signals table — **likely filled overnight** |
| Catalyst | ADA exploit / UNH DOJ carry-forward confirmed; MU earnings beat confirmed (+6% AH) |
| Scheduler | New day scheduler booted at 04:26, Cycle 1/12 in progress |
| New basket | momentum_breakout (SYN +18.9%) — new since prior review |
| No new A-tier | No A/B crypto signals generated in latest scalp/intraday — only C-tier watchlist |
| Thesis confirmed | BTC swing short thesis confirmed — price moved from $62k entry to $59.5k (−$2.5k), now bouncing |
| ETH long NOT invalidated YET | Price bounced $50 to $1,616 — but regime still contradicts. Needs review. |

---

## 5. Catalyst Coverage

- **Total catalyst events today (2026-06-25):** 470
- **Narrative baskets:** 6 (delisting_thin_liquidity, perps_dex_narrative, binance_ecosystem_teaser, rwa_narrative, ai_narrative, momentum_breakout)
- **By type:** other_news 444 (94.5%), exploit_hack 4, earnings_event 3, low_liquidity_event 3, regulatory_sector_headline 2, product_launch 2, analyst_action 2, rumour_only 2, insider_activity 1, buyback_burn 1, platform_growth 1, legal_risk 1
- **Symbol-mapped notable events:** ADA (SecondFi exploit, 2 articles), UNH (DOJ probe), SYN (momentum_breakout primary), HYPE (perps_dex primary), BNB/ASTER (binance ecosystem), ONDO/XLM (RWA), NEAR/RENDER/TAO/FET/WLD (AI narrative)
- **Unmapped / basket-only notable catalysts:** THORChain exploit ($10.7M), DeFi TVL −39% 2026, Micron earnings (3 articles — stock, no crypto symbol), regulatory/Clarity Act risk
- **Catalyst mapping quality:** The 94.5% "other_news" concentration is structural (news items without a specific catalyst type), not a mapping failure. Named-symbol events (ADA, UNH, SYN, HYPE, BNB etc.) are properly detected. **No mapping weakness warning triggered.**
- **Freshness:** All catalyst data from cycle_01-17 (04:17 EEST) — fresh (<1h).

**Key catalysts for decisions:**
1. **ADA/USDT** — exploit_hack (SecondFi $2.4M, Cardano wallet) → **AVOID**
2. **SYN/USDT** — momentum_breakout basket primary → short-term momentum watch
3. **HYPE/USDT** — perps_dex basket (whale liquidation narrative) → watch_pullback playbook
4. **THORChain (basket)** — exploit $10.7M → DeFi sector caution
5. **UNH/USDT** — legal_risk (DOJ) → **AVOID** (stocks, closed market)

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** `risk-off` (BTC downtrend, ETH downtrend, breadth 24–25%, elevated volatility ATR 82nd pct, F&G 24)
- **Stocks mood:** `closed` — after-hours, planning only. Regime label from prior session: **chop** (VIX 18.63 → intraday spike 20.17, SPY −0.17% close)
- **Dominant narrative:** Crypto leverage bloodbath ($861M liquidations, 91% longs). Fed rate hike repricing (~90% by year-end). Semiconductor selloff spill from AI chip guidance (Broadcom disappoint) into risk assets. DeFi hacks cluster (ADA, THORChain). Micron AH beat brightens tech for tomorrow (stock, not crypto direct).
- **Preferred side now:** `wait_for_trigger` — regime favors shorts but bounce from $59.5k to $60.7k means NO new short at current price; longs remain counter-tape (RS leaders only on pullbacks)
- **Best long candidate:** ATM/USDT — pullback to $1.10–1.15, requires BTC holds ≥$60k
- **Best short candidate:** BTC/USDT — retest of $61,200–62,000 supply zone on low volume / failed bounce
- **Best catalyst-backed candidate:** SYN/USDT — momentum_breakout basket primary, pullback needed first
- **What to avoid:** Any new scalp short (PF 0.57 bucket). ETH swing long without review. ADA. UNH (stocks, AVOID).
- **What would change the view:** (bullish flip) BTC reclaims $62k with volume and closes above $64k → regime shifts to mixed; (bearish escalation) BTC loses $59k support with volume → accelerate to $57.3k liquidation cluster; (stocks shift) SMH gaps up on MU beat → tech sector turns bullish

---

## 7. Candidate Deep Dives

### 7.1 — BTC/USDT (B-tier swing short, OPEN — likely IN PROFIT)

**Status:** B-tier swing short. Entry zone ~$62k. Current price $60,753. Signal likely **TRIGGERED** — approximately in profit (~$1,247 from entry assuming $62k fill).

**Thesis:** BTC is in a confirmed downtrend. The signal captured the breakdown from ~$62k. Price crashed to $59,518 and has bounced overnight to $60,753 — a partial squeeze on leveraged shorts.

**Price reaction to catalyst:** BTC fell sharply on the $861M liquidation cascade ($600M headline) and Fed rate hike repricing. The bounce is technical, not catalyst-driven.

**Chase check:** **Entry NOW would be LATE** — price moved $1,247 below the entry zone. The clean short entry is on a retest of the $61,200–62,000 supply zone. Do NOT add to or initiate shorts at $60,753.

**Overextension:** BTC bounced ~$1,235 off lows — partial squeeze. $60,753 is inside the post-crash range. Not overextended on the short side at this level, but no clean entry structure without a retest.

**Key level:** $57,300 = next liquidation cluster (cited CryptoTimes/CryptoSlate). $59,500 = overnight low support. $61,200–62,000 = supply / signal entry zone (short trigger). $63,000 = stop for the existing signal.

**Derivatives:** BTC swing short signal has score 65. Existing short positioning from $62k zone. Bounce from $59.5k = partial squeeze on latecomers. OI data sparse on bybit (54 failures in intraday run).

**Invalidation:** 1h close above $63,000 (signal invalidation level).

**Alignment with mood:** ALIGNED — regime is risk-off, BTC in downtrend. Short is the correct directional bias.

**Verdict: OPEN actionable (if triggered from $62k). WAIT FOR RETEST to add or initiate. Do NOT chase at $60,753. Target: $57,300.**

---

### 7.2 — ETH/USDT (B-tier swing long, ENTERED UNRESOLVED — CONTRADICTION)

**Status:** B-tier swing long. Entry zone ~$1,600–1,620. Price was $1,566 at 23:15 EEST (loss), now $1,616. **ENTERED UNRESOLVED / NEEDS REVIEW.**

**Thesis (signal's original):** ETH relative strength vs BTC, swing long setup at a key support zone.

**Price reaction to catalyst:** ETH was caught in the $861M liquidation flush — dropped to $1,566 post-entry, now bouncing to $1,616 (near break-even zone depending on exact fill).

**Contradiction check:** ETH is in a confirmed **downtrend** (breadth 24–25%, BTC regime bearish). The swing long was generated before the most aggressive sell-off. The regime now actively contradicts this position.

**Current situation:** ETH at $1,616 is approximately at the entry zone. The position is either at scratch or slightly in loss depending on exact fill. The bounce provides a potential exit point at reduced loss or scratch.

**Squeeze check:** ETH OI/funding from prior run showed ETH in a complex position (23:15 review: ETH −11.25% weekly, downtrend confirmed). No sign of short squeeze that would validate the long.

**Invalidation:** Below $1,566 on a 4h close = position invalidated. Above $1,700 = first area where thesis could recover.

**Alignment with mood:** CONTRADICTED — ETH downtrend, BTC downtrend, altcoin breadth 24%.

**Verdict: ENTERED UNRESOLVED. Operator should consider exiting at scratch ($1,616 area) or tightening stop to $1,565. DO NOT add to this position. Needs manual review before Asia session deepens.**

---

### 7.3 — ATM/USDT (B-tier swing long — RS LEADER, WATCH PULLBACK)

**Status:** B-tier swing long (score 67, entry ~$1.1x zone). Strongest RS leader in the universe: +27–29% vs BTC in 24h. Score 91.6 in both scalp and intraday (highest of all scanned symbols).

**Why it matters:** ATM is the best relative strength exception in a risk-off tape. This is the type of setup that produces the "crypto longs PF 4.0" bucket — RS leaders outperforming BTC even in downtrends.

**Derivatives:** Futures data unavailable for ATM across Bybit/OKX. Crowd attention: 0.0/100 (no social hits). Volume ratio: 0.08–0.23x (LOW) — this is a key concern. Low volume means the move lacks broad market participation.

**Chase check:** ATM is up 27% in 24h with volume only 0.08–0.23x average. **This is an overextended, low-volume RS move.** Do NOT enter at current price. The signal entry zone is ~$1.10–1.15 (pullback zone). Entry at current levels = chasing a move with no volume confirmation.

**Catalyst:** No confirmed catalyst for ATM specifically. The signal exists purely on RS + technical momentum.

**Squeeze risk:** No futures data = no OI/funding picture. Unknown squeeze potential.

**Entry structure:** Wait for pullback to $1.10–1.15 zone with volume confirmation ≥0.5x. Only valid if BTC holds above $60k on Asia session close.

**Invalidation:** BTC loses $60k support → ATM RS thesis weakens regardless of its own price action. Signal invalidation: close below ATM support zone (report says support ~$1.1x area, data in scalp report).

**Alignment:** Counter-tape long. Playbook data says RS-leader longs have been working (PF 4.0 for longs this week). But risk-off regime + low vol = reduce size and demand pullback.

**Verdict: WAITING FOR ENTRY — pullback to $1.10–1.15 zone. Single best long watch candidate overnight. Counter-tape; reduce size by 50%. No catalyst backing requires stricter volume threshold.**

---

### 7.4 — WLD/USDT (B-tier swing long — AI narrative, score 75)

**Status:** B-tier swing long (score 75 — highest-scored active swing long). Entry zone at ~$0.xx (truncated from table). AI narrative basket: WLD is a related symbol in the ai_narrative basket (NEAR/RENDER/TAO/FET as primary, WLD as related).

**Thesis:** WLD (Worldcoin) is an AI-adjacent token in the AI narrative basket. The basket has been active for <24h. Score 75 is above average for swing signals.

**Derivatives:** From intraday report — WLD appeared in the derivatives overview. Not shown in the scalp report's specific OI data (likely via fallback). Prior swing report stale 28h.

**Chase check:** Without current price (table truncated), using regime context: risk-off means even AI narrative plays face headwinds. WLD is a related (not primary) symbol in the basket — Binance ecosystem teaser is separate. Need price at or near entry zone to be actionable.

**Catalyst:** AI narrative basket is "fresh <24h" — a weaker signal than "fresh <6h." The AI sector had mixed momentum in the narrative heatmap (attention 35/100, momentum 45.8/100, volume 7.2/100 — low volume, mixed regime).

**Key filter:** Cross-exchange confirmation is the main performance driver this week (PF 2.6 vs 0.76). WLD's exchange confirmation status is unknown from truncated table.

**Alignment:** Counter-tape long in risk-off. AI basket is multi-week thesis (related_beta_rotation playbook = wait_pullback).

**Verdict: WAITING FOR ENTRY — best swing-long bucket entry is at the signal's entry zone (pullback only). Requires BTC stabilization. Second-tier candidate behind ATM. Lower priority until AI narrative basket shows volume. Do not chase.**

---

### 7.5 — SYN/USDT (C-tier / basket primary, momentum_breakout — FRESH WATCH)

**Status:** NOT a formal B-tier active signal. Primary symbol of **momentum_breakout** basket (fresh <1h, basket generated 04:17 EEST). Intraday score 91.6 (tied with ATM — the two highest-scored symbols this cycle). 24h return +12.83–18.9%. Volume ratio 0.82x (best in the basket — close to 1x, meaningful).

**Thesis:** SYN is the top momentum mover in the basket. No confirmed news catalyst — pure price/volume momentum. The momentum_breakout playbook is `wait_pullback` — this means the basket itself recommends waiting for a pullback before entry.

**Volume check:** 0.82x — best volume ratio among any scanned candidate this cycle. Meaningfully better than ATM (0.08–0.23x). This is what makes SYN interesting despite no catalyst.

**Derivatives:** Fallback via MEXC: funding −0.000107, 24h move 12.8%. OI data via MEXC only (bybit failed). Funding slightly negative — market paying shorts, not overly crowded.

**Chase check:** Intraday report: SYN is listed as strongest symbol. The basket playbook says `wait_pullback`. Current price is post-move (up 12–19%). An immediate entry = chasing. Wait for a pullback to prior session consolidation base.

**Catalyst:** **No confirmed news catalyst.** Momentum only. High risk of fade without backing. Per prior playbook data: no-catalyst intraday in chop/risk-off = WR 23% / PF 0.70 / −3R (negative bucket). This significantly lowers conviction.

**Entry trigger:** Pullback to yesterday's close zone + volume ≥0.8x on reclaim. Only if BTC holds.

**Verdict: WATCH ONLY — basket primary qualification, not a formal signal. Best pure-momentum watch, but no-catalyst intraday bucket is net-negative per playbook stats. Treat as discovery-level tracking, not actionable without confirmation.**

---

## 8. Best Candidates Ranked

_No A-tier signals exist in this window. All candidates are B-tier or basket primaries._

| Rank | Symbol | Direction | Tier | Status | Score | Trigger | Risk |
|---|---|---|---|---|---|---|---|
| 1 | BTC/USDT | Short | B-tier swing | OPEN / in profit est. | 65 | Retest $61,200–62,000 for new entry | Medium (squeeze if $62k breaks back up) |
| 2 | ATM/USDT | Long | B-tier swing | WAITING pullback | 91.6 / 67 signal | Pullback to $1.10–1.15 + BTC ≥$60k | Medium (no derivatives data, low vol) |
| 3 | ETH/USDT | Long | B-tier swing | ENTERED UNRESOLVED | 66 | Exit at scratch ($1,616) or tighten stop | High (regime contradiction) |
| 4 | WLD/USDT | Long | B-tier swing | WAITING pullback | 75 | Pullback to signal entry zone | Medium (AI basket, wait_pullback playbook) |
| 5 | SYN/USDT | Long | Basket primary | WATCH ONLY | 91.6 | Pullback to prior base + vol ≥0.8x | Medium-High (no catalyst, discovery) |

**Long-watch: ATM/USDT** — trigger: pullback to $1.10–1.15 + BTC holds $60k on Asia close.

**Short-watch: BTC/USDT** — trigger: retest of $61,200–62,000 supply zone on low volume / rejection candle.

**Catalyst-watch: SYN/USDT** — trigger: pullback to prior-session base + volume reclaim ≥0.8x 20-period avg. Note: no-catalyst bucket carries negative expected value; only trade if volume confirms.

**No new scalp shorts in this window** — scalp short bucket PF 0.57 (-3R). Weekend approaching (Thu close → weekend mode PF 0.68 vs 1.92). Do not initiate new scalp shorts.

---

## 9. Avoid / No Trade

_This window only — never a command to stop the system. Scanner continues in all moods._

- **ADA/USDT: AVOID** — SecondFi exploit ($2.4M, $20M potential) confirmed. Ongoing risk. Score in expansion watchlist is counter-thesis (exploit = negative catalyst).
- **UNH (stocks): AVOID** — DOJ criminal Medicare fraud probe confirmed, −16% yesterday. Signal must remain AVOID until legal risk resolves.
- **Any new scalp shorts:** PF 0.57 bucket, −3R this week. Low confidence mode. Avoid generating new short scalps in this session.
- **PUMP/USDT:** Price down + OI up + L/S 0.604 — fresh shorts pressing but squeeze risk is real. Do not add shorts into a crowding setup without confirmation.
- **ETH/USDT swing long (new entry):** Contradicted by regime. Only review/manage the existing ENTERED UNRESOLVED position.
- **INJ/USDT:** Price down + OI up + fresh short pressing. Squeeze-prone. C-tier watchlist only; not actionable given OI build and no clear catalyst.
- **RE/USDT:** −14.71% RSvsBTC −11.4%, extended move. Chase risk. 2 ATR below EMA20 — rejection noted in scalp report.
- **Stocks intraday shorts (any): AVOID** — PF 0.1, −20R this week. Catastrophic bucket.

---

## 10. Main Risks

1. **BTC bounce continues through $62k:** Would squeeze the swing short and flip the regime signal. Key stop level is $63k. If BTC closes above $63k with volume, the short thesis fails.
2. **Weekend performance degradation:** Today is Thursday. Weekend mode PF 0.68 vs 1.92 weekday. As we approach Friday/Saturday, swing signals generated now will carry into the worst-performing time window. Reduce size on any new swing entries.
3. **Derivatives data sparse:** Bybit OHLCV 54 failures in this cycle. OI/funding data for many symbols is via MEXC fallback only. Squeeze risk on PUMP/INJ/FIL is possible without full OI history — monitor these.
4. **No A-tier signals:** All current crypto setups are B-tier or C-tier. Signal quality is lower than average. Operator should demand higher confirmation before acting.
5. **ETH ENTERED UNRESOLVED contradiction:** If ETH drops below $1,566 on Asia session, the ENTERED UNRESOLVED position moves to loss territory. This is the most urgent manual action item.
6. **Fed rate hike repricing:** ~90% chance of hike priced in per CoinStats. Macro environment is systematically risk-off. Any risk-on narrative faces persistent headwinds.
7. **DeFi hack cluster:** ADA exploit + THORChain $10.7M + DeFi TVL −39% 2026 — negative sector backdrop. Avoid long exposure to any DeFi-adjacent symbol without catalyst.
8. **Social blind spots:** Reddit 403 persistent, no live X/Telegram/Discord KOL feeds. Crowd context is minimal — could miss emerging narratives or coordinated moves.

---

## 11. Action Plan — Next 4 Hours (04:39–08:39 EEST)

1. **ETH/USDT position: manual review FIRST.** Decide: exit at scratch (~$1,616) or set hard stop at $1,565. Do NOT let this drift into a deeper loss given regime contradiction.
2. **BTC/USDT short:** Hold the existing B-tier signal. Do not add or re-enter at $60,753. Wait for a retest of $61,200–62,000 (with volume ≤0.5x of prior bearish candle) before any new short entry.
3. **ATM/USDT watch:** Monitor for a pullback to $1.10–1.15. Only consider entry if BTC holds $60k on the Asia close (06:00–07:00 EEST Nikkei/Shanghai). Volume must be ≥0.5x for entry.
4. **WLD/USDT:** Monitor for pullback to signal entry zone. No rush — AI basket is multi-week thesis.
5. **SYN/USDT:** Track in the basket primary slot. Treat as C-tier/discovery until volume confirms and catalyst appears.
6. **Stocks planning:** MU beat (+6% AH) sets up SMH/NVDA/QQQ as bullish gap-watch for Thursday RTH. Build your levels before 16:30 EEST (09:30 ET) but DO NOT chase pre-market. Require RTH confirmation before entry.
7. **New scalp shorts:** AVOID in this session. Weekend approaching, scalp short bucket negative.

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Reasoning |
|---|---|---|---|
| Crypto scalp | crypto | **NO NEW ENTRIES** | All C-tier (scores 56–63). Scalp short bucket PF 0.57. Weekend approaching. |
| Crypto intraday | crypto | **WATCH ONLY** | No A/B intraday signals. Regime risk-off. No-catalyst intraday bucket negative. |
| Crypto swing | crypto | **HOLD + WAIT** | BTC short: hold, wait for retest. ATM long: wait for pullback. ETH long: manual review immediately. WLD: wait for pullback. |
| Stocks intraday | stocks | **CLOSED — PLANNING** | Market closed. JPM likely triggered. MU catalyst sets up SMH/NVDA Thursday gap watch. All signals WAITING, not actionable until RTH 09:30 ET. |
| Stocks swing | stocks | **CARRY-FORWARD ONLY** | Swing report stale 28h. Treat all stocks swing signals as planning context only. |
| Paper portfolio | all | **MONITOR ETH position urgently.** BTC short: carry. No new paper trades in this window. | Risk-off, weekend approaching, ETH contradiction. |

---

## 13. Sources

- [Crypto Market Crash: $861M Liquidations Jun 24 2026 (CryptoTimes)](https://www.cryptotimes.io/2026/06/24/crypto-market-crash-wipes-out-861m-as-btc-eth-xrp-bnb-sol-price-drops/) — 2026-06-24
- [Bitcoin live price BTC $60,753 / ETH $1,616 (CoinDesk)](https://www.coindesk.com/price/bitcoin) — 2026-06-25 04:39 EEST
- [Bitcoin (BTC) Daily Market Analysis 24 June 2026 — F&G 24, Fed hike 90% (CoinStats AI)](https://coinstats.app/ai/a/latest-news-for-bitcoin) — 2026-06-24
- [BTC & ETH prices Jun 24 context — opened at lowest in ~2 weeks (Yahoo Finance)](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-june-24-2026-opened-at-lowest-levels-in-about-two-weeks-125349040.html) — 2026-06-24
- Internal: `data/reports/scalp/2026-06-25_01-37_scalp_report.md` — 2026-06-25 04:37 EEST
- Internal: `data/reports/intraday/2026-06-25_01-17_intraday_report.md` — 2026-06-25 04:17 EEST
- Internal: `data/reports/stocks/intraday/2026-06-25_01-23_stocks_intraday_report.md` — 2026-06-25 01:23 EEST
- Internal: `data/catalysts/2026-06-25/catalyst_cycle_01-17.md` — 2026-06-25 04:17 EEST
- Internal: `active-signals` CLI — 2026-06-25 04:39 EEST (crypto 13, stocks 50+)
- Internal: `signal-stats` CLI — 2026-06-25 04:39 EEST
- Internal: `detect_untracked_legacy_alerts --since 2026-06-25` — 0 untracked

---

## 14. Fix Requests / TODO

### TODO-BYBIT-OHLCV-INTRADAY
- **issue:** Bybit OHLCV returned 0 symbols (54 failures) in the intraday cycle run; only MEXC/OKX fallback available for derivatives in that run.
- **evidence:** `data/reports/intraday/2026-06-25_01-17_intraday_report.md` §0 — `bybit: ohlcv_fetched=0, failed=54`
- **suggested manual fix:** Check Bybit API rate limit / credential rotation in the 01:00–01:17 UTC window. If structural, add Bybit circuit-breaker fallback notification to Telegram.
- **priority:** medium
- **first observed:** 2026-06-25 04:39 EEST

### TODO-PAPER-MONITOR-LAG
- **issue:** Paper monitor data is last known from 21:21 EEST yesterday (~7.3h at review time). Cycle 1 started at 04:26 but paper monitor status has not yet been reported for today's cycle.
- **evidence:** scheduler.log shows cycle 1 still in progress (intraday report running); paper monitor telegram step not yet reached.
- **suggested manual fix:** This will self-resolve when cycle 1 completes; however if cycle 1 takes >90 min total, check for hung processes. No action required unless cycle 1 doesn't complete by 06:30 EEST.
- **priority:** low
- **first observed:** 2026-06-25 04:39 EEST
