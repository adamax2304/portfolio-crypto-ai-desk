# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

_Generated 2026-06-24 16:20 EEST (Wednesday). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

---

## 1. Executive Summary

**Wed 2026-06-24, 16:20 EEST — pre-US-open decision review — advisory only / no auto-trade.**

US cash open in ~10 minutes (09:30 ET = 16:30 EEST). This is the final pre-open read.

- **Crypto: RISK-OFF maintained.** BTC ~$62,760 as of 08:38 ET, opened at 2-week lows (-2% from Tuesday), strong dollar + hawkish Fed expectations. BTC/ETH both downtrend confirmed. Altcoin breadth 33% above EMA20. Short bias holds; no altcoin long lane without BTC stabilization above $62K.
- **US Macro: GAP-UP RISK for shorts.** QQQ futures +0.46% premarket (stabilizing after Nasdaq –2.5% chip selloff). Memory chipmakers +3-4% premarket (Micron +3.8%, Sandisk +2.9%) ahead of Micron earnings tonight. Stocks regime: **chop/stabilizing** — not a clean directional read yet.
- **Key pre-open consideration:** BTC $10.6B options expiry Friday June 28. Put-call skew bearish. Volatility window elevated through weekend. Do NOT over-size into the open.
- **⚠️ ADA/USDT — Best crypto short-watch.** SecondFi exploit confirmed (wallet key flaw, $2.4M–$20M risk, Yoroi/EMURGO link — most trusted Cardano wallet). ADA –3% today, ~$0.15. Failed-bounce short setup B-tier, entry zone 0.1488–0.1496 (price just below). Regime-aligned. Wait for retest.
- **⚠️ SMH short B-tier ENTERED UNRESOLVED — Headline risk.** Micron earnings after bell today. Memory chips already +3–4% premarket. SMH short needs RTH confirmation in first 15 min. If SMH opens above entry and presses higher, set tight stop or reduce.
- **⚠️ UNH long B-tier (74.73) — AVOID.** DOJ criminal + civil probe into Medicare billing (confirmed July 2025, ongoing). Stock –55% from highs. Legal risk not reflected in score. Do NOT trigger entry. See §14 TODO.
- **JPM B-tier long ENTERED UNRESOLVED.** Financials sector strongest 20d (+5.35% RS vs SPY). Legal check clear. Wait for RTH first-15 confirmation before adding.
- **TSLA short B-tier ENTERED UNRESOLVED.** Tech stabilizing premarket. Watch first 30 min before confirming.
- **Best long-watch (crypto):** EVAA/USDT — RS leader +11.6% vs BTC, C-tier counter-tape. Trigger: pullback to 0.8637–0.8786 + BTC holds $62K.
- **No A-tier signals in any asset class.** Scanning continues — all modes active.

---

## 2. Data Used

| Source | File / Path | mtime EEST | Freshness |
|---|---|---|---|
| scheduler.log | `data/scheduled_runs/2026-06-24_default_schedule/scheduler.log` | 15:37 | **FRESH** (43m) |
| Latest cycle | `cycle_05_14-38_summary.md` | 15:24 | **FRESH** (56m) |
| Crypto scalp | `2026-06-24_11-54_scalp_report.md` | 14:54 | **FRESH** (1h26m) |
| Crypto intraday | `2026-06-24_12-06_intraday_report.md` | 15:06 | **FRESH** (1h14m) |
| Crypto swing | not found in glob — prior review cited 2026-06-24_00-58 | ~03:58 | **STALE** (~12h22m) |
| Stocks intraday | `2026-06-24_12-22_stocks_intraday_report.md` | 15:22 | **FRESH** (58m) |
| Stocks swing | not found in glob — prior review cited 2026-06-24_01-03 | ~04:03 | **STALE** (~12h17m) |
| Catalyst events | `data/catalysts/2026-06-24/catalyst_events.jsonl` | cycle 5 | **FRESH** |
| Narrative baskets | `data/catalysts/2026-06-24/narrative_baskets.jsonl` | cycle 5 | **FRESH** |
| Active-signals CLI | crypto (21) + stocks (50) | cycle 5 output | **LIVE** |
| Signal-stats CLI | crypto + stocks | cycle 5 output | **LIVE** |
| Untracked alerts | `detect_untracked_legacy_alerts --since 2026-06-24` | 16:20 | **0 untracked** |
| Prior review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-24_1139.md` | 11:49 | 4h31m ago |
| BTC price | Yahoo Finance / Polymarket | 08:38 ET | $62,760 –2% vs Tue |
| QQQ premarket | TheStreet / MarketScreener | pre-open | +0.46%, ~$716.95 |
| ADA exploit | FXStreet / CryptoTimes / BanklessTimes | Jun 24 | **CONFIRMED — severe** |
| UNH DOJ probe | QuiverQuant / Yahoo Finance | Jul 2025–2026 | **CONFIRMED — ongoing** |
| HYPE price | CoinGecko/CoinMarketCap | Jun 24 | $62.92, ATH $76.67 Jun 16 |

**Blindspots:** Crypto swing stale (>12h). Stocks swing stale (>12h). Reddit social blocked (403). TradingView/chart MCP unavailable — using report OHLCV/ATR fields only. Onchain config missing. Liquidation heatmaps not connected.

---

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: **15:37 EEST** (43 min ago) — within 3h threshold ✓
- Latest cycle `cycle_05_14-38_summary.md` mtime: **15:24 EEST** (56 min ago) — within 3h threshold ✓
- **NOT DEFERRED** — both freshness checks pass.
- Cycle 5 (14:38–15:24 EEST): **ok=23, failed=0** — clean run.
- Pre-tracking: checked=458, updated=2, tp_hits=280, stopped=0, expired=0.
- Social failures: Reddit CryptoCurrency/Bitcoin/Ethereum all 403 — persistent.
- RSS failures: Reuters Business, SEC EDGAR Filings.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-06-24 16:20 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "derivatives_sparse", "onchain_config_missing"],
      "data_missing": ["swing_report_stale_12h", "reddit_social_blocked", "onchain_config", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_5_ok=23_failed=0", "scalp_report_fresh_1h26m", "intraday_report_fresh_1h14m", "stocks_intraday_fresh_58m", "0_untracked_alerts"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["risk_off", "shorts_preferred", "wait_for_trigger", "mixed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC_downtrend", "ETH_downtrend", "altcoin_breadth_33pct", "BTC_62760_2week_lows", "QQQ_futures_plus_046pct", "stocks_regime_chop", "VIX_18.83", "SPY_5d_minus282pct"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": ["catalyst_mapped_ratio_exact"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ADA_exploit_SecondFi_20M_confirmed", "BTC_options_expiry_10.6B_Jun28", "BlackRock_selling_BTC_ETH", "HYPE_ETF_221M_institutional", "Micron_earnings_tonight", "UNH_DOJ_criminal_probe_confirmed"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["bybit_okx_cross_check_partial", "liquidation_heatmaps", "OI_not_available_for_all_symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ADA_price_down_OI_up_fresh_shorts_pressing", "XRP_price_down_OI_up", "LINK_price_down_OI_up_3.85x_volume", "LINK_funding_positive_4.62e-05", "XRP_long_short_skew_heavy_long"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["entry_fresh", "stale_before_entry", "price_moved_away"],
      "data_missing": ["chart_mcp_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ADA_price_0.1485_below_entry_zone_0.1488_0.1496", "XRP_price_1.090_below_entry_zone_1.092_1.095", "LINK_price_7.588_below_entry_zone_7.599_7.623", "all_three_waiting_for_failed_bounce_retest"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "open_actionable"],
      "data_missing": ["exact_lifecycle_breakdown_from_cycle5"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_21_B-tier_active", "stocks_50_active", "SMH_B_short_entered", "TSLA_B_short_entered", "JPM_B_long_entered", "ADA_XRP_LINK_WAITING_for_entry", "0_untracked_alerts"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.85,
      "reason_codes": ["headline_risk", "legal_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH_DOJ_criminal_probe_AVOID", "SMH_short_Micron_earnings_headline_risk", "TSLA_short_tech_stabilizing_premarket_squeeze_risk", "BTC_options_expiry_Friday_10.6B", "QQQ_plus046pct_premarket_counter_to_short_bias", "stocks_B_tier_0_of_6_wins_this_week"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["stocks_swing_stale"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_PF_2.06_plus17R_working", "crypto_longs_PF_2.8_plus15R", "crypto_shorts_PF_0.8_minus5R_underperforming", "stocks_B_tier_WR_0pct_minus6R", "scalp_PF_0.14_low_confidence", "crypto_week_total_plus10R_PF_1.19"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["wait_for_trigger", "shorts_preferred", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["all_above_agents", "pre_open_context_10min_to_cash", "require_RTH_confirmation"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.80,
    "preferred_side": "shorts",
    "best_long_candidate": {
      "symbol": "EVAA/USDT",
      "trigger": "pullback to 0.8637–0.8786 + BTC holds above $62K + volume confirms",
      "reason": "strongest RS leader vs BTC (+11.6%), C-tier; counter-tape — require confirmation before entry"
    },
    "best_short_candidate": {
      "symbol": "ADA/USDT",
      "trigger": "failed bounce/retest into 0.1488–0.1496, 1h rejection candle, invalidation 1h close above 0.1505",
      "reason": "B-tier intraday, regime-aligned (risk-off), SecondFi exploit catalyst confirmed, EMURGO/Yoroi link severe reputational damage"
    },
    "best_catalyst_candidate": {
      "symbol": "HYPE/USDT",
      "trigger": "pullback to $58–60 with volume + institutional accumulation narrative holding",
      "reason": "perps_dex_narrative basket primary, $221M ETF AUM, institutional staking, ATH $76.67 Jun 16 — wait for pullback before entry"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ criminal + civil investigation Medicare fraud, stock –55% from highs, score 74.73 not adjusted for legal risk — entry forbidden until legal resolution"
    },
    "operator_action": "wait_for_trigger",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason Codes | Suggested Effect |
|---|---|---|---|---|
| data_quality | **ok** | 0.88 | scheduler_fresh, derivatives_sparse, onchain_config_missing | advisory_only |
| market_regime | **caution** | 0.82 | risk_off, shorts_preferred, wait_for_trigger, mixed | advisory_only |
| catalyst_narrative | **caution** | 0.80 | fresh_catalyst, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | **caution** | 0.65 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.75 | entry_fresh, stale_before_entry, price_moved_away | advisory_only |
| execution_lifecycle | **ok** | 0.78 | waiting_for_entry, entered_unresolved, open_actionable | advisory_only |
| risk_manager | **caution** | 0.85 | headline_risk, legal_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | **caution** | 0.75 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | **caution** | 0.80 | wait_for_trigger, shorts_preferred, manual_review | advisory_only |

---

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-24_1139.md` (Europe/pre-US, 11:39 EEST, 4h31m ago).

### New since 11:39 EEST
- **Cycle 5 completed** (14:38–15:24 EEST): Fresh scalp, intraday, stocks intraday reports.
- **ADA/USDT emerged as B-tier intraday short** (score 66.5): New in cycle 5 reports. Exploit catalyst now confirmed — SecondFi/Yoroi/EMURGO link confirmed by multiple sources. Price ~$0.1485.
- **LINK/USDT emerged as B-tier scalp short** (65.8): 3.85x volume, new in cycle 5 reports.
- **UNH B-tier long (74.73), JPM B-tier long (70.01)** in latest stocks intraday report — elevated scores vs prior C-tier planning phase.
- **QQQ premarket +0.46%**: Tech stabilizing — new development since 11:39 (prior review noted QQQ 5d –4.08% with no premarket signal). This adds gap risk to all short tech/growth positions.
- **Micron earnings tonight confirmed**: Catalyst risk for SMH short.
- **SMH B-tier short, TSLA B-tier short, JPM B-tier long**: All show as ENTERED UNRESOLVED in active-signals CLI (triggered from prior cycles).

### Carried forward from 11:39 EEST
- UNH DOJ probe AVOID status: unchanged.
- BTC risk-off regime: unchanged (price flat, still near 2-week lows).
- BlackRock BTC/ETH selling: still active catalyst pressure.
- HYPE best catalyst-watch: $62.92 vs $62.92 at prior review — minimal move, thesis intact.
- ETH swing long B: still active, WAITING for entry (BTC stabilization trigger not met).
- WLD short B swing: still active.
- 0 untracked alerts: consistent.

### Upgraded
- ADA: C-tier watchlist → B-tier intraday short (exploit catalyst confirmed, regime-aligned).
- Stocks scoring: UNH/JPM elevated to B-tier (score threshold crossed with fresh regime).

### Downgraded / Flagged
- SMH short: B-tier but adds headline risk from Micron earnings. Treat as **manual review** from 09:30 open.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today: **753**
- Active narrative baskets: **5** (delisting_thin_liquidity, perps_dex_narrative, binance_ecosystem_teaser, ai_narrative, momentum_breakout)
- Mapped (symbol-tagged) events identified in reports: ADA (exploit_hack ×2), BTC (options_expiry, BlackRock), UNH (legal_risk), ZEC (Fortitude Nasdaq), XRP, BNB, SOL, ETH — at least 10+ symbols mapped.
- Unmapped ratio: exact count requires JSONL read (not available in this pass); estimated moderate-high unmapped portion given 753 events with only 5 baskets and ~10 mapped symbols.
- **Note:** Cannot confirm unmapped > 50% threshold without direct JSONL query. Catalyst layer should be used as directional context, not precise signal decision tool, for unverified basket entries.

**Notable events confirmed today:**
- **ADA/USDT** — [exploit_hack] SecondFi wallet key flaw, 178 wallets, $2.4M confirmed/$20M risk. EMURGO/Yoroi link. **Severe, ongoing risk.**
- **BTC/USDT** — [regulatory] $10.6B options expiry Friday June 28. Put-call bearish skew.
- **UNH** — [legal_risk] DOJ criminal + civil probe Medicare billing. Confirmed ongoing since July 2025.
- **BNB/USDT** — [event] YZi Labs ends proxy war with BNB treasury company.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off — BTC downtrend (~$62,760, 2-week lows), ETH downtrend, breadth 33% above EMA20. Strong dollar + hawkish Fed headwinds. BlackRock selling flow ongoing. $10.6B options expiry Friday. Short bias.
- **Stocks mood:** chop / stabilizing pre-open — QQQ +0.46% premarket; Nasdaq recovering from 2-session selloff. Micron earnings tonight is a known unknown. VIX 18.83 (elevated but not panic). SPY 5d –2.82%, QQQ 5d –4.08% but stabilizing. Financials (XLF) and semis (SMH) leading sector divergence.
- **Dominant narrative:** Macro (strong dollar + Fed hawkish) suppresses risk assets. Crypto specific: options expiry + BlackRock selling. Stocks specific: chip sector earnings cycle (Micron tonight).
- **Preferred side now:** crypto shorts (regime-aligned) + catalyst-backed only. Stocks: wait-and-see at open — require RTH confirmation for any new entry. Do NOT add new shorts into a tech gap-up without first-15-minute confirmation.
- **Best long candidate:** EVAA/USDT (RS leader, pullback to 0.8637–0.8786, C-tier — requires BTC stabilization trigger)
- **Best short candidate:** ADA/USDT (B-tier, exploit catalyst, entry zone 0.1488–0.1496 on failed bounce)
- **Best catalyst-backed candidate:** HYPE/USDT (perps_dex_narrative, ETF institutional, pullback to $58–60)
- **What to avoid:** UNH (legal, DO NOT enter); SMH new short entry pre-Micron (headline risk); chasing any tech short into gap-up open without 15-min RTH confirmation
- **What would change the view:** BTC 1h close above $63,500 (neutralizes short bias for 4h window); QQQ RTH gap-down and retest of lows (confirms tech short lane); Micron earnings beat → SMH short squeeze risk elevates to manual review

---

## 7. Candidate Deep Dives

### Candidate 1 — SHORT ADA/USDT (B-tier, intraday)

**Status:** WAITING for entry (NO-ENTRY until retest)  
**Score:** 66.5/100 | Mode: intraday 4-24h | Direction: short

**Thesis:** Regime-aligned short (risk-off, BTC/ETH downtrend) + confirmed exploit catalyst. SecondFi wallet flaw (connected to Yoroi, one of Cardano's founding entities EMURGO's rebranded wallet) drained $2.4M with $20M+ at risk across 178+ compromised wallets. Retail sentiment broadly bearish on Cardano today.

**Price check (pre-open):**
- Current price ~$0.1485. Entry zone: 0.1488–0.1496. Price is just BELOW entry zone.
- ATR: 0.0017. Support: 0.1458. Resistance: 0.1544. Invalidation: 1h close above 0.1505.
- TP1: 0.1468, TP2: 0.1451, TP3: 0.1434.
- Chase risk: LOW — price is below entry zone. Wait for failed bounce/retest. Do NOT enter at market.
- Setup fresh? YES — generated in cycle 5 (1h14m ago). Not stale.
- Is this aligned with mood? YES — risk-off, crypto short bias.
- Overextended? No — ADA –3% today but within normal daily ATR range.
- What would invalidate: 1h close above 0.1505 (resistance zone breaks).

**Catalyst confirmation:** CONFIRMED — SecondFi exploit is multi-source verified (FXStreet, CryptoTimes, BanklessTimes, BeInCrypto, MEXC News). EMURGO link is damaging to Cardano's institutional credibility.

**Derivatives:** Price down + OI up = fresh shorts pressing. Possible squeeze if price reclaims. OI 24h +14.38%, funding –0.00023. Long/short ratio heavy long-skewed. Squeeze risk: moderate, manageable with tight SL (1.505 zone).

**Legal/headline check:** ADA itself has no securities fraud issue. Exploit is a protocol-adjacent risk (third-party wallet), not Cardano protocol itself. Risk is sentiment/confidence damage to ecosystem.

**Pre-open decision:** WAIT for entry. Do not enter at market pre-open. If price retraces to 0.1488–0.1496 with a rejected 15m candle between 09:30–10:00 ET → SHORT with invalidation 1h close above 0.1505.

---

### Candidate 2 — SHORT SMH (B-tier stocks, entered/triggered)

**Status:** ENTERED UNRESOLVED — pre-RTH (entry from prior cycle)  
**Score:** 73.x/100 | Mode: intraday | Direction: short

**Legal/headline check:** No SEC/DOJ risk on SMH ETF itself. **HEADLINE RISK: Micron Technology (MU) reports earnings tonight after market close.** Memory chips +3.8% premarket (Micron) and +2.9% (Sandisk). SMH is semiconductor ETF — Micron is a top holding.

**Pre-open situation:** SMH short is already ENTERED UNRESOLVED from a prior trigger. QQQ +0.46% premarket and memory chips rallying = counter-movement to the short position. Gap risk: possible gap UP at open.

**Chase risk:** Not applicable — already entered. But maintaining risk is the question.
**Is this still aligned with mood?** Partially — stocks in chop, not clean short lane with tech stabilizing.
**What would invalidate:** If SMH opens above entry zone and sustains the first 15 min. Micron earnings beat tonight → SMH could squeeze significantly after bell.

**Pre-open decision for ENTERED position:**
- At 09:30 open, observe first 15 minutes. If SMH opens gap-up and fails to reverse within 15 min → consider reducing position size or moving stop tighter.
- If SMH gaps up >1% at open: MANUAL REVIEW — the overnight catalyst (Micron premarket rally) may negate the short thesis for the session.
- If SMH opens flat/down and maintains bearish structure: maintain with original invalidation.

**Note for new entries:** Do NOT add to SMH short pre-Micron earnings. The unresolved headline risk makes new entries inadvisable until post-earnings.

---

### Candidate 3 — LONG JPM (B-tier stocks, entered/triggered)

**Status:** ENTERED UNRESOLVED — pre-RTH  
**Score:** 76.x/100 | Mode: intraday | Direction: long

**Legal/headline check:** No current DOJ/SEC investigation flagged. No earnings this week for JPMorgan. **Legal check: CLEAR.**

**Sector context:** Financials (XLF) is strongest sector 20d (+5.35% RS vs SPY, +3.74% 20d return). JPM is a primary financials leader. Higher interest rate environment benefits net interest margins → JPM is regime-supported.

**Pre-open situation:** JPM B-tier long is ENTERED UNRESOLVED. QQQ +0.46% premarket. Stocks stabilizing = supportive of long. Financials sector: strong.

**Chase risk:** Not applicable — already entered. Price ~$330s.
**Is this aligned with mood?** YES (stocks stabilizing, financials strongest sector).
**What would invalidate:** SPY gap-down and broad risk-off at open; JPM fails to hold entry on RTH open.

**Pre-open decision:** Hold ENTERED position. At 09:30 open, if JPM opens flat/up and holds within first 15 min → maintain. If SPY gaps down sharply and JPM breaks below entry → stop applies. Strongest intraday candidate for stocks after legal/headline check.

---

### Candidate 4 — LONG UNH (B-tier, score 74.73) — INTEGRITY CHECK / AVOID

**Status:** WAITING for entry — DO NOT TRIGGER  
**Legal/headline check:** ⚠️ **CONFIRMED AVOID**

DOJ criminal + civil investigation into Medicare Advantage billing practices confirmed (cooperating since July 2025). Probe targets inflated patient diagnoses and inappropriate reimbursements from Medicare Advantage (UNH's largest revenue segment). Stock is –55% from highs. Third-party review launched. "Most challenging period in UNH's history" per multiple sources.

**Pre-open decision:** **AVOID. Do not enter UNH regardless of intraday action.** The B-tier score (74.73) does not reflect legal risk — this is a scoring system blind spot flagged in §14. Any intraday bounce is likely a bear bounce in a structurally broken name under federal criminal investigation.

---

### Candidate 5 — LONG EVAA/USDT (C-tier watchlist, RS leader)

**Status:** WATCHLIST ONLY — best long candidate for routing  
**Score:** 64.6/100 scalp | 58.3/100 intraday | Direction: long

**Thesis:** EVAA/USDT is the top RS leader today vs BTC (+11.6%), with 1.82x volume and uptrend structure (setup quality 73.8%). Price $0.8852. MEXC-only (high-risk exchange, low confirmation=38%). No fresh catalyst — no-catalyst long in risk-off = dangerous without BTC support.

**Chase risk:** Price has already moved +12.28% today. Entry zone (pullback) 0.8637–0.8786 vs current $0.8852 — price is ABOVE conditional pullback zone. Chasing current price is explicitly forbidden. Wait for pullback.

**Pre-open decision:** Do NOT enter now. If BTC stabilizes above $62K AND EVAA pulls back to 0.8637–0.8786 AND volume holds AND a fresh catalyst emerges → revisit. Currently: best long-watch only, not actionable. MEXC-only confirmation requires anchor/Bybit upgrade.

**TradingView / manual chart check unavailable.**

---

## 8. Best Candidates Ranked

| Rank | Symbol | Direction | Tier | Status | Trigger | Aligned? |
|---|---|---|---|---|---|---|
| 1 | ADA/USDT | SHORT | B-tier | WAITING for entry | Failed bounce to 0.1488–0.1496, 1h rejection candle | YES — regime + catalyst |
| 2 | JPM | LONG | B-tier | ENTERED UNRESOLVED | RTH open hold + 15 min confirmation | YES — financials strong |
| 3 | HYPE/USDT | LONG (catalyst) | C-tier watch | WAITING | Pullback to $58–60 + institutional narrative holds | YES — catalyst-backed |
| 4 | EVAA/USDT | LONG | C-tier watch | WAITING (pullback) | Pullback to 0.8637–0.8786 + BTC $62K + fresh catalyst | CONDITIONAL |
| 5 | SMH | SHORT | B-tier | ENTERED UNRESOLVED | RTH open first-15 confirmation — reduce if gap-up | CONDITIONAL (Micron risk) |

**Short-watch (if none triggered):** ADA/USDT — exact trigger: 1h failed bounce rejection at 0.1488–0.1496. Re-check at 10:00 ET.  
**Long-watch (if none triggered):** EVAA/USDT — exact trigger: pullback to 0.8637 + BTC stabilization. Re-check at 11:30 review.  
**Catalyst-watch:** HYPE/USDT — exact trigger: pullback to $58 + volume on 15m + institutional basket narrative active.

---

## 9. Avoid / No Trade

This window's avoid decisions (does NOT mean stop system — scanning continues):

- **UNH** — AVOID: DOJ criminal probe. Do not enter under any circumstance.
- **SMH new short entry** — AVOID pre-Micron: Do not add new shorts to SMH before Micron earnings tonight (after bell). Current ENTERED UNRESOLVED position: monitor first 15 min only.
- **TSLA short new entry** — AVOID until RTH confirmation: QQQ stabilizing premarket creates squeeze risk for TSLA short. Current ENTERED UNRESOLVED: watch first 30 min.
- **HEI/USDT longs** — AVOID: +41–45% 24h, extreme chase, negative funding. Verified no-touch.
- **Counter-tape altcoin longs (no catalyst)** — AVOID in current risk-off regime. RS leaders without confirmed catalysts (ALICE, G, ID, LAB) are speculative C-tier only; do not size up.

---

## 10. Main Risks

1. **Micron earnings tonight (after bell):** SMH short may face significant gap risk if Micron beats expectations. Memory chips already +3–4% premarket = market pricing upside. SMH ENTERED UNRESOLVED position is exposed.
2. **BTC options expiry Friday ($10.6B, Jun 28):** Max pain uncertainty, elevated volatility through weekend. Avoid over-sizing any setup with a multi-day horizon into expiry.
3. **QQQ gap-up stabilization vs short bias:** If QQQ continues to recover at open (>+0.5% RTH), it may create short squeezes in TSLA, NEAR, and any tech-adjacent altcoin shorts. Monitor closely in first 30 min.
4. **ADA squeeze risk:** Price down + OI up = fresh shorts pressing = squeeze risk if ADA reclaims 0.1505. Long/short ratio already heavily long-skewed. If a broader Cardano ecosystem recovery narrative emerges (e.g., SecondFi remediation announcement), the short could squeeze fast.
5. **Crypto swing stale (>12h):** Swing setups (ETH, WLD, others) are based on carry-forward data. Treat swing signals as planning-only until next fresh swing report.
6. **Social data unavailable:** Reddit blocked (403) persistent. No live crowd context from Reddit. Telegram channel news is the only social input.
7. **Unmapped catalyst ratio unknown:** 753 events, exact mapped % unclear without JSONL query. Catalyst layer may be weaker than apparent. Use as directional context, not single-source decision.

---

## 11. Action Plan — next 4 hours

**16:20–16:30 EEST (pre-open, now):**
- Review this document. No new entries before open.
- Note: SMH short and TSLA short ENTERED UNRESOLVED — check pre-market levels vs entry prices.

**16:30–16:45 EEST (RTH open + first 15 min):**
- Watch SMH direction at 09:30 ET: if opens gap-up >0.5% and fails to reverse → tighten stop on entered short. If opens flat/red and holds structure → maintain.
- Watch JPM at 09:30 ET: if opens flat/up and holds entry → maintain long.
- Watch TSLA: if opens up significantly (tech stabilizing) → reassess short, tighten stop.

**16:45–18:00 EEST (15–90 min into session):**
- Monitor ADA/USDT for failed bounce to 0.1488–0.1496 zone. If rejected → SHORT entry with 1h close above 0.1505 as invalidation. If price continues lower without retest → NO-ENTRY / skip.
- Monitor BTC structure: hold above $62K = regime neutral; break below $62K = increase crypto short weight.

**18:00–20:20 EEST (US session mid-morning):**
- 18:30 EEST review fires (US open reaction review) — next scheduled auto-review will assess how the open went.
- If SMH short maintains and approaches TP1 before Micron earnings: consider partial-profit target.
- Do NOT add new SMH shorts before Micron earnings.

**20:20 EEST+ (pre-Micron earnings):**
- Reduce SMH short exposure ahead of Micron after-bell announcement.
- Watch HYPE/USDT for pullback to $58–60 entry zone.

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Bias | Top Pick | Notes |
|---|---|---|---|---|---|
| Scalp (crypto) | Crypto | caution | short | XRP (watchlist) / ADA (wait for retest) | Low-confidence scalp playbook — prefer B-tier intraday over scalp |
| Intraday (crypto) | Crypto | caution | short | **ADA — WAIT for 0.1488–0.1496 retest** | Regime + catalyst aligned. No entry until failed bounce |
| Swing (crypto) | Crypto | caution (stale data) | short | WLD carry-forward watch | Swing report stale >12h — planning only |
| Intraday (stocks) | Stocks | **manual review** | mixed | JPM long (entered) / SMH short monitor | Require RTH confirmation. Avoid UNH. Watch Micron risk on SMH. |
| Swing (stocks) | Stocks | caution (stale data) | neutral | No clean picks | Stale report, poor B-tier performance (0/6 wins). |

**Overall system verdict: CAUTION — wait_for_trigger.** Best near-term trade window: ADA short at failed bounce (crypto) and JPM long RTH confirmation (stocks). Scanner and paper tracking continue in all modes. No system pause.

---

## 13. Sources

- [Bitcoin and ethereum prices today, June 24, 2026 — opened at lowest in about two weeks](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-june-24-2026-opened-at-lowest-levels-in-about-two-weeks-125349040.html) — Yahoo Finance, 2026-06-24
- [Stock Market Today (June 24, 2026): S&P 500 futures edge higher with Micron earnings in focus](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-24-2026) — TheStreet, 2026-06-24
- [S&P 500, Nasdaq futures tick up as tech shares stabilize](https://www.marketscreener.com/news/s-p-500-nasdaq-futures-tick-up-as-tech-shares-stabilize-ce7f5fdbdd80f626) — MarketScreener, 2026-06-24
- [Cardano Price Forecast: ADA vulnerable to deeper losses amid SecondFi exploit](https://www.fxstreet.com/cryptocurrencies/news/cardano-price-forecast-ada-vulnerable-to-deeper-losses-amid-secondfi-exploit-202606241037) — FXStreet, 2026-06-24
- [Cardano Project SecondFi Halts Services as Hack Estimates Hit $20M](https://www.cryptotimes.io/2026/06/24/cardano-project-secondfi-halts-services-as-hack-estimates-hit-20m/) — CryptoTimes, 2026-06-24
- [SecondFi Exploit Drains Cardano Wallets, Losses May Top $20M](https://www.banklesstimes.com/articles/2026/06/24/secondfi-exploit-drains-cardano-wallets-losses-may-top-20m/) — BanklessTimes, 2026-06-24
- [Cardano Project SecondFi Hit by Major Exploit, Losses Could Top $20 Million](https://beincrypto.com/secondfi-exploit-cardano-losses-20-million/) — BeInCrypto, 2026-06-24
- [SecondFI's $2M exploit: A wallet flaw leaves Cardano users exposed](https://ambcrypto.com) — AMBCrypto, 2026-06-24
- [UnitedHealth Group Stock (UNH) Opinions on DOJ Investigation and Sentiment Shift](https://www.quiverquant.com/news/UnitedHealth+Group+Stock+(UNH)+Opinions+on+DOJ+Investigation+and+Sentiment+Shift) — QuiverQuant, 2026
- [UnitedHealth Group under DOJ investigation over Medicare billing practices](https://www.medicaleconomics.com/view/unitedhealth-group-under-doj-investigation-over-medicare-billing-practices) — Medical Economics, 2025–2026
- [Hyperliquid (HYPE) Price — live price, marketcap](https://coinmarketcap.com/currencies/hyperliquid/) — CoinMarketCap, 2026-06-24
- [Hyperliquid (HYPE) Price Today on CoinGecko](https://www.coingecko.com/en/coins/hyperliquid) — CoinGecko, 2026-06-24
- Internal sources: scalp_report 2026-06-24_11-54, intraday_report 2026-06-24_12-06, stocks_intraday_report 2026-06-24_12-22, cycle_05_14-38_summary.md, active-signals CLI, signal-stats CLI

---

## 14. Fix Requests / TODO

### TODO-UNH-LEGAL-SCORE-BLIND
- **issue:** UNH generates B-tier long score (74.73) despite confirmed DOJ criminal investigation. Scoring layer has no legal-risk gate for stocks.
- **evidence:** `data/reports/stocks/intraday/2026-06-24_12-22_stocks_intraday_report.md` §5 top candidates; QuiverQuant DOJ probe confirmed.
- **suggested manual fix:** Add a `legal_risk_override` field to stock signals; if `catalyst_events.jsonl` contains `[legal_risk]` for a symbol, force score to AVOID regardless of fundamentals. Alternatively, add a hard AVOID flag to the stock signal generator when legal_risk catalyst_type is present.
- **priority:** high
- **first observed:** 2026-06-24 16:20 EEST (flagged in 11:39 review too)

### TODO-SWING-REPORT-GLOB
- **issue:** Swing reports (`data/reports/swing/*_swing_report.md`) and stocks swing reports not findable via glob pattern — may be missing from today's cycle or stored in an unexpected path.
- **evidence:** Glob `data/reports/swing/*_swing_report.md` returned no results for 2026-06-24. Prior reviews cite `2026-06-24_00-58_swing_report.md` as existing.
- **suggested manual fix:** Verify swing report generation in scheduler cycle config. Check if swing is being skipped on some cycles (cycle 5 did not mention swing report in steps output).
- **priority:** medium
- **first observed:** 2026-06-24 16:20 EEST

### TODO-CATALYST-MAPPED-RATIO
- **issue:** Catalyst coverage diagnostics cannot determine mapped vs unmapped ratio without a direct JSONL query. The 753 event count makes manual estimation impractical.
- **evidence:** `data/catalysts/2026-06-24/catalyst_events.jsonl` — 753 events, ratio unknown.
- **suggested manual fix:** Add a summary metadata file to each catalyst session folder (e.g., `catalyst_stats.json`) with counts: total, mapped, unmapped, baskets. This would allow enriched-review to read ratio instantly without JSONL parsing.
- **priority:** medium
- **first observed:** 2026-06-24 16:20 EEST
