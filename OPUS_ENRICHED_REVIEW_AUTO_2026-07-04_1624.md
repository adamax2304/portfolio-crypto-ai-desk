# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:24 EEST

**Slot:** pre-US-open decision review | **Time:** 2026-07-04 16:24 EEST
**Cycle:** 06 (15:51 start → 16:16 finish, 29/29 steps OK, 0 failures)
**Previous review:** 2026-07-04 04:39 EEST (crypto overnight / Asia review)
**Advisory only — no auto-trade.**

---

## 1. Executive Summary

This is the **pre-US-open decision review** slot for Saturday July 4, 2026. **US markets are CLOSED — Independence Day.** This review covers crypto-only live decisions and stocks planning for Monday July 7 open. Advisory only — no auto-trade.

**Key findings this slot:**

1. **HMSTR/USDT** is the system's top B-tier swing pick at score 78.0/100 (+53.5% 24h, OI +131.68%). No verified catalyst — pure momentum. Long/short ratio 0.491 (short-biased). WAITING for pullback entry. Demand retest, not breakout chase.

2. **DOGE/USDT** is the best catalyst-backed candidate. `news_supported` flipped from 0→1 in cycle 6 label refresh. DogeOS $6.9M raised from Polychain, TDOG ETF live on Nasdaq, regulatory commodity classification confirmed. Multiple B-tier signals (swing 73.9, intraday 69/66, scalp 77). Volume 2.1x. Cleanest catalyst narrative this session.

3. **TLM/USDT** now has a real catalyst (Aster leverage launch + drone racing tournament, +55% July 4) but **Binance delisting monitoring still active since May 22.** RSI 84.04. OI declining (-16.6%) into pump = short covering only. AVOID long. Short watch after failed retest.

4. **ETH/USDT** benefits from CLARITY Act momentum (4 steps from law, Aug recess deadline critical — Senate needs ~7 more Democratic votes). ETH intraday signal already TP HIT. Best macro catalyst-watch for Monday session.

5. **Stocks:** All stock reports stale (intraday 17.3h, swing/invest 48h). CLOSED today. Next open Monday July 7, 09:30 ET. No stock A/B actionable until RTH confirmation Monday.

6. **Weekend mode active:** thinner liquidity, wider wicks. Weekend signals historically underperform (WR 22%, PF=1.7 vs weekday PF=4.3). All entries on pullback only — no market buys into breakouts.

---

## 2. Data Used

| Source | Age | Freshness |
|---|---|---|
| scheduler.log | NOT FOUND | n/a — cycle_06 summary used as proxy |
| cycle_06_15-51 summary | 0.15h | FRESH (29/29 OK, 0 failures) |
| scalp report (2026-07-04_12-58) | 0.44h | FRESH |
| intraday report (2026-07-04_13-03) | 0.36h | FRESH |
| swing report (2026-07-04_13-14) | 0.17h | FRESH |
| stocks intraday (07/03 23:07) | 17.3h | STALE (>14h) — weekend, US closed |
| stocks swing (07/02 16:03) | 48.4h | STALE — weekend |
| stocks invest (07/02 16:05) | 48.3h | STALE — weekend |
| catalyst_events today | 0.37h (13:03 cycle) | FRESH (265 events, 4 baskets) |
| LLM analysis packet | 0.17h | FRESH (swing mode, 13:14 UTC) |
| active-signals CLI (crypto) | run now | 50 B-tier active signals |
| signal-stats CLI (crypto) | run now | week PF=2.947, WR=25%, +70.09R |
| detect_untracked_legacy | run now | 5 untracked (ADA×2, TLM×3) |
| WebSearch / WebFetch | this run | 6 external sources (see §13) |

**Notes:**
- `scheduler.log` not found at project root. Cycle summary used for freshness check. Cycle 06 completed at 16:16 EEST (29/29 OK) — within 3h window → proceed, no defer.
- Stocks excluded from final verdicts — CLOSED, stale data (US Independence Day).
- Reddit social sources BLOCKED (403) — social context unavailable this run.
- Onchain config missing (`config/onchain.yaml`) — interface ready but disabled.

---

## 3. Scheduler / Data Freshness

- **Scheduler:** Cycle 06 completed 16:16 EEST (29/29 OK, 0 failures, ~8 min ago). Monitor background PID=1936 active (90-min window). FRESH.
- **Cycle mode:** weekend (crypto-only). Stocks disabled.
- **Paper monitor status (from cycle 06 step 27):**
  - Open actionable: **9**
  - Waiting for entry: **11**
  - Entered unresolved: **55** (filled, no TP/SL before window — ENTERED UNRESOLVED lifecycle status)
  - Review/Shadow: **167**
  - No-entry / stale / moved-away: **70** (NO-ENTRY lifecycle status)
  - Closed today: **374W / 38L / 0 flat** (CLOSED WIN / CLOSED LOSS / CLOSED FLAT)
  - Needs review: **0**
- **Untracked legacy alerts:** 5 (ADA/USDT×2, TLM/USDT×3) — sent to Telegram without backing proposed_signal → excluded from PF/winrate tracking.
- **Catalyst label refresh (cycle 06):** `news_supported 0→1: DOGE`. Telegram label flips: 2.
- **Paper shadow (forward-valid):** A −97.57R / B +67.98R (Δ+165.5R). Gate: NOT_READY (4/6 lanes, 9d window < 14d required). No promotion.
- **Derivatives / squeeze phase (118 symbols):** phase_5_post_unwind_chop=44, phase_0_unknown=40, phase_1_build_up=25, phase_2_squeeze_expansion=5, phase_4_unwind=4. High post-unwind chop count — crowded re-entries carry reversal risk.
- **Onchain:** interface_ready_config_missing. No network performed.
- **Social:** Reddit 403 blocked (all 3 subreddits). Social context unavailable this run.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-04 16:24 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["scheduler_log_missing", "social_attention", "onchain_config", "reddit_feeds", "stocks_fresh_data"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "cycle_06 completed 16:16 EEST, 29/29 OK",
        "scalp 0.44h / intraday 0.36h / swing 0.17h — all FRESH",
        "stocks stale 17-48h — excluded (US Independence Day)",
        "catalyst_events.jsonl 0.37h — FRESH (265 events, 4 baskets)",
        "scheduler.log NOT FOUND — cycle summary used as proxy"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.76,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"],
      "data_missing": ["etf_flows_today", "dxy_live", "btc_exact_price_confirmed"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: uptrend (all three reports)",
        "ETH trend: uptrend (all three reports)",
        "Altcoin breadth above EMA20: 84.62%",
        "Altcoin breadth above EMA50: 84.62%",
        "BTC ATR percentile: 7.0 (normal/low volatility)",
        "Dashboard: BTC above $60K post-Warsh comments; F&G=22, VIX=16.15, SPY up, QQQ down",
        "Recommended style: selective longs, prefer pullbacks on RS leaders",
        "Weekend mode: PF=1.7, WR=22% vs weekday PF=4.3"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "ok",
      "confidence": 0.70,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": ["tlm_binance_official_delist_date", "hmstr_catalyst_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ETH: Clarity Act 4 steps from law; Senate floor vote pending (~7 Dems short); Aug recess deadline",
        "DOGE: news_supported flipped 0→1 cycle 6; DogeOS $6.9M Polychain; TDOG ETF; X Money beta; commodity classification",
        "TLM: Aster leverage launch + tournament CONFIRMED; Binance delisting monitoring ACTIVE since May 22",
        "ARB: Robinhood Chain $50M TVL mainnet launch (CryptoBriefing)",
        "4 narrative baskets: delisting_thin_liquidity, perps_dex_narrative (HYPE), ai_narrative, momentum_breakout (avoid_chase)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["squeeze_risk", "post_unwind_chop", "data_unavailable"],
      "data_missing": ["full_oi_history", "liquidation_heatmaps", "bybit_full_oi_breakdown"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "HMSTR: OI +131.68% (extreme), long/short 0.491 (short-biased) — short squeeze risk if breakout sustained",
        "MIRA: negative funding bybit -0.01146, mexc -0.008164 — shorts paying; elevated crowding",
        "TLM: OI -16.6% while price +55% — short covering into pump; funding -0.0008",
        "DOGS: OI +44.16%, funding neutral",
        "EPIC: OI +13.33%, funding neutral, crowding normal",
        "118 symbols: 44 phase_5_post_unwind_chop — high chop environment",
        "5 symbols in phase_2_squeeze_expansion"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["chase_risk", "overextended", "clean_retest"],
      "data_missing": ["tradingview_charts", "intraday_structure_detail"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "TLM RSI 84.04 — overbought; +55% 24h, 107% 7d — EXTREME CHASE RISK",
        "HMSTR +53.46% 24h, 86.7% 7d — overextended; needs retest at 0.0003 zone",
        "EPIC: entry 0.6442-0.6635, current ~0.6720 — entry zone reachable, RR 1.84",
        "DOGE: multiple signals in triggered state — entry already near/at zone",
        "ANSEM: +93.77% 24h — extreme; MEXC-only cap applies",
        "All swing entries require pullback confirmation (weekend mode)"
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
        "Open actionable: 9 (OPEN actionable lifecycle)",
        "Waiting for entry: 11 (WAITING FOR ENTRY lifecycle)",
        "Entered unresolved: 55 (ENTERED UNRESOLVED — filled, no TP/SL before window)",
        "Review/Shadow: 167",
        "No-entry/stale/moved-away: 70 (NO-ENTRY lifecycle)",
        "Closed today: 374W / 38L / 0 flat",
        "Needs review: 0",
        "5 untracked legacy alerts: ADA×2, TLM×3 (UNTRACKED, excluded from PF)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["headline_risk", "correlation_cluster", "reduce_risk"],
      "data_missing": ["daily_pnl_live", "stock_legal_fresh_2026-07-04"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "TLM: Binance delisting monitoring since May 22 — HEADLINE RISK confirmed",
        "Weekend mode: PF=1.7, WR=22% — reduce sizing",
        "Correlation cluster: HMSTR/EPIC/DOGE/MIRA/DOGS all long — zero hedge",
        "5 untracked alerts (ADA/TLM) — system integrity gap",
        "All 50 active signals are LONG — no short signal coverage",
        "Post-unwind chop: 44/118 symbols — crowded re-entries risky",
        "MIRA: elevated crowding + negative funding — long crowding risk"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["14d_breakdown_by_symbol"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto_swing_narrative_rs_momentum: 14d WR 72%, PF 5.80, +24R (n=18) — STRONG",
        "crypto_intraday_catalyst_or_momentum WITH catalyst: WR 50%, PF 2.75, +7R — actionable",
        "crypto_intraday_catalyst_or_momentum WITHOUT catalyst: WR 23%, PF 0.70, -3R — WEAK",
        "crypto_scalp_momentum_continuation: WR 12%, PF 0.14, -6R — LOW CONFIDENCE",
        "crypto_failed_bounce_short: WR 40%, PF 2.00, +9R — viable short playbook",
        "Overall weekly: PF=2.947, WR=25%, +70R (n=242, reliable)",
        "Weekend cohort: WR=22%, PF=1.7 (n=102) — confirmed underperformance"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.74,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Bullish trend confirmed: BTC/ETH uptrend, 84.6% breadth",
        "Best long: DOGE/USDT — news_supported confirmed, multi-modal, cleanest catalyst",
        "Best short-watch: TLM/USDT after failed retest $0.0025 (NOT now)",
        "Best catalyst-watch: ETH/USDT — Clarity Act macro + ARB L2 momentum",
        "Avoid: TLM long (delist + overbought); scalp signals (low_confidence)",
        "Weekend mode: pullback entries only; no chasing",
        "5 untracked alerts: manual investigation TODO"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.74,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "DOGE/USDT",
      "trigger": "pullback + hold above entry zone on 15m structure; intraday signals already triggered",
      "reason": "news_supported=1 confirmed cycle 6; DogeOS $6.9M Polychain + TDOG ETF + commodity classification; multiple B-tier signals (swing 73.9, scalp 77)"
    },
    "best_short_candidate": {
      "symbol": "TLM/USDT",
      "trigger": "1h close below $0.00208 after failed $0.0025 retest; NOT a live short now",
      "reason": "Binance delisting monitoring active; RSI 84.04 overbought; OI -16.6% into pump = short covering exhausting"
    },
    "best_catalyst_candidate": {
      "symbol": "ETH/USDT",
      "trigger": "Senate CLARITY Act floor vote announced, or BTC holds $60K+ into Monday open",
      "reason": "Clarity Act 4 steps from law (Aug recess deadline); ETH = CFTC commodity; ARB/Robinhood Chain $50M TVL confirms L2 momentum"
    },
    "avoid_candidate": {
      "symbol": "TLM/USDT",
      "reason": "Binance delisting monitoring active since May 22; +107% 7d = pump driven by delist-avoidance speculation; Aster leverage adds catalyst but does NOT override delist risk"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh (cycle 06), report_stale (stocks weekend) | advisory_only |
| market_regime | ok | 0.76 | risk_on, longs_preferred, mixed (F&G=22 vs price uptrend) | advisory_only |
| catalyst_narrative | ok | 0.70 | fresh_catalyst (DOGE/ETH), catalyst_confirmed (DOGE news_supported), narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.68 | squeeze_risk (HMSTR shorts), post_unwind_chop (44/118), data_unavailable (liquidation maps) | advisory_only |
| technical_entry | caution | 0.65 | chase_risk (TLM/HMSTR), overextended, clean_retest (EPIC entry zone) | advisory_only |
| execution_lifecycle | ok | 0.82 | open_actionable=9, waiting_for_entry=11, entered_unresolved=55 | advisory_only |
| risk_manager | caution | 0.78 | headline_risk (TLM delist), correlation_cluster (all-long), reduce_risk (weekend) | advisory_only |
| playbook_performance | ok | 0.75 | playbook_working (swing WR 72%/PF 5.80), playbook_failing (scalp PF 0.14) | advisory_only |
| head_trader | ok | 0.74 | risk_on, longs_preferred, wait_for_trigger (DOGE pullback / TLM failed-bounce) | advisory_only |

---

## 4. What Changed vs Previous Review (2026-07-04 04:39 EEST)

| Change | Detail |
|---|---|
| New cycle | Cycle 06 (15:51–16:16, 29/29 OK) vs cycle 01 in prev review |
| HMSTR advances to #1 B-tier | Score 78.0 (prev: caution flag, not top pick). +53% 24h, OI +131%. Now #1 swing candidate. |
| DOGE news_supported confirmed | Cycle 6 label refresh: DOGE flipped 0→1. Prev review: DOGE not flagged catalyst-backed. Major upgrade. |
| TLM deepened catalyst (partial) | Aster leverage + tournament confirmed. Still Binance delisting monitoring active. New: RSI 84.04, OI declining (-16.6%). |
| ARPA moved to weak/short side | ARPA -10.38% 24h now in weakest symbols basket. Prev review flagged caution on new longs — confirmed. |
| ADA untracked alerts: 5 (prev 0) | ADA sent to Telegram (B swing 69.6 + B scalp 68.3) without backing proposed_signal. System integrity issue new this cycle. |
| ETH intraday TP HIT | ETH/USDT B intraday signal CLOSED WIN (tp_hit). Previous review: no ETH active signal. |
| Paper shadow forward improved | B forward: +67.98R vs prev +55.39R; A: -97.57R vs -92.06R. B gap widening. NOT_READY gate unchanged. |
| CLARITY Act July 4 deadline missed | Target was July 4 White House signing but Senate floor vote not yet scheduled. 4 steps still remain. |
| Open actionable reduced | 9 now vs 24 in prev review (cycle 01). Many signals resolved during cycles 02–06. |

---

## 5. Catalyst Coverage

- **Events today:** 265 (13:03 cycle), scalp cycle shows 607, swing cycle shows 681 (grows each cycle throughout day)
- **Baskets:** 4 (delisting_thin_liquidity, perps_dex_narrative, ai_narrative, momentum_breakout)
- **Unmapped flag:** NOT triggered — no "unmapped >50%" flag raised by any cycle today
- **Legal/regulatory (crypto):**
  - ETH: Congress + Clarity Act (regulatory_sector_headline, 0.80 importance) — BULLISH
  - TLM: exchange_delisting flag in notable events — RISK
  - Hinkal protocol: $820K USDC exploit (exploit_hack basket) — RISK for DeFi basket
- **Legal/regulatory (stocks, all basket, closed today):** Hub Group, Erasca, Zillow, PicS, Sportradar, AeroVironment, ADMA Biologics, GeneDx Holdings, Futu Holdings, UNH/DOJ probe — monitor for Monday
- **Key narrative baskets:**
  - `delisting_thin_liquidity` (avoid_low_liquidity) — primary: TLM → AVOID
  - `perps_dex_narrative` (wait_pullback) — primary: HYPE/USDT
  - `ai_narrative` (related_beta_rotation) — primary: NEAR/RENDER/TAO/FET — mixed heat 26.8/100
  - `momentum_breakout` (avoid_chase) — primary: LAB/TLM/EPIC — DO NOT CHASE
- **Missing:** Reddit social context (403 blocked), onchain data (config missing)

---

## 6. Market Landscape

### Market Mood / Risk Routing

*(Driven by Agent Council market_regime + risk_manager agents)*

- **Crypto mood:** risk-on / bullish trend. BTC uptrend, ETH uptrend, 84.6% alts above EMA20 and EMA50. BTC above $60K (post-Warsh-comments per dashboard snapshot). F&G=22 (fear) diverges from price — caution on fragility. VIX=16.15 (normal). Weekend mode: demand cleaner structure.
- **Stocks mood:** CLOSED — US Independence Day (July 4, 2026). Next open Monday July 7, 09:30 ET. All stock signals = planning/watchlist only until RTH confirmation.
- **Dominant narrative:** Post-Warsh alt catch-up momentum; DOGE multi-catalyst (DogeOS + TDOG + commodity); TLM delisting-pump; ETH Clarity Act macro; HMSTR/EPIC RS leaders without verified catalyst; AI narrative (NEAR/TAO/FET) mixed heat, not hot.
- **Preferred side now:** Longs on pullback at RS leaders with catalyst. Scalp signals: LOW CONFIDENCE (PF 0.14) — no action. Intraday without catalyst: WR 23% — prefer catalyst-backed.
- **Best long candidate:** DOGE/USDT — news_supported=1 confirmed; multiple B signals; DogeOS + TDOG + commodity classification catalyst stack. Entry on pullback only.
- **Best short candidate:** TLM/USDT — failed retest of $0.0025 after Aster/tournament pump exhausts. NOT a live short yet. Trigger: 1h close below $0.00208 support.
- **Best catalyst-backed candidate:** ETH/USDT — Clarity Act macro (Aug recess deadline); ETH as CFTC commodity; ARB/Robinhood Chain $50M TVL confirms L2 ecosystem momentum.
- **What to avoid:** TLM long (Binance delist monitoring + overbought + OI declining); HMSTR breakout chase (no catalyst + OI extreme); MIRA (elevated funding crowding); ANSEM (MEXC-only +93% extreme); scalp signals (low_confidence playbook).
- **What would change the view:** BTC 4h close below EMA20 → shift to risk-off; TLM Binance official delist announcement → immediate AVOID all correlated; Senate CLARITY Act floor vote scheduled → upgrade ETH to active watch.

---

## 7. Candidate Deep Dives (5)

### Candidate 1 — HMSTR/USDT (B swing 78.0 — WAITING FOR ENTRY)

**STATUS: WAITING FOR ENTRY. Highest B-tier score this cycle. No verified catalyst.**

- **System:** B swing 78.0/100, waiting. Entry pullback ~0.0003. RR 1.84. B intraday already TP HIT.
- **Market data:** 24h +53.46%, 7d +86.7%. OI +131.68% (extreme fresh positioning). Long/short 0.491 (more shorts than longs — short squeeze risk on continued breakout). Funding: 2.206e-05 (neutral).
- **Catalyst (internal):** "no fresh verified catalyst detected" across all three reports.
- **Catalyst (external):** Hamster Kombat is a tap-to-earn Telegram game. Daily cipher on July 4 — routine game event, NOT a market catalyst. Future airdrop risk (past airdrops caused -26.82% drops). 100B total supply / 64.38B circulating — persistent sell pressure risk. **No confirmed July 4 catalyst.**
- **Chase risk:** YES at current price. 53% 24h is overextended. Entry requires pullback to 0.0003 zone with 15m structure acceptance. No market buy above current price.
- **Overextended:** Likely >2 ATR from EMA20. TradingView/chart unavailable — manual check required.
- **Mood alignment:** Risk-on supports momentum longs but no catalyst + weekend mode = lower conviction (weekend WR 22%).
- **Invalidation:** 1h close below 0.0003.
- **Verdict: WAITING FOR ENTRY. If pullback to 0.0003 with volume acceptance → paper-trade only, reduced weekend size. No catalyst = do not size up. Chase = skip entirely.**

---

### Candidate 2 — DOGE/USDT (B swing 73.9 / B intraday 69/66 / B scalp 77 — BEST LONG)

**STATUS: WAITING (swing) / TRIGGERED (intraday + scalp). news_supported=1 confirmed. BEST LONG CANDIDATE.**

- **System:** B swing 73.9/100 (waiting), B intraday 66-69/100 (triggered), B scalp 77.2/100 (triggered). Volume 2.1x. OI +43.75%. Funding: -2.785e-05 (neutral). 24h +22.52%, 7d +21.25%.
- **Catalyst stack (confirmed):**
  - `news_supported=1` flipped cycle 6 label refresh (confirmed internal)
  - Dashboard: "Ether, solana, dogecoin in the green after Warsh comments push bitcoin above $60,000" (market snapshot)
  - **DogeOS:** $6.9M raised from Polychain Capital for DeFi/gaming/AI on Dogecoin chain — summer 2026 launch target
  - **TDOG ETF:** First spot DOGE ETF trading on Nasdaq since January 2026 — institutional access
  - **SEC/CFTC commodity:** March 2026 classification (not security) — reduces regulatory overhang
  - **X Money:** Closed beta with possible DOGE integration (unconfirmed but speculated by 600M+ user base)
- **Chase risk:** LOW-MODERATE. 22.5% 24h — strong but manageable. Volume 2.1x confirms buying. Intraday/scalp signals already in triggered state → entry already happening.
- **Mood alignment:** STRONG. Risk-on + catalyst-backed + institutional product + commodity status. Best candidate for the `catalyst_backed` overlay (lifts crypto intraday + swing PF).
- **Invalidation:** BTC drop below $60K, X Money launch with no DOGE integration, DogeOS delays/adverse news.
- **Verdict: BEST LONG CANDIDATE. Catalyst-backed, news_supported confirmed, multi-modal. Intraday/scalp TRIGGERED — monitor for TP hit. Swing: pullback + 15m hold before entry. Paper-trade at standard weekend size.**

---

### Candidate 3 — TLM/USDT (B system score — HEADLINE RISK — AVOID LONG, SHORT WATCH)

**STATUS: HEADLINE RISK CONFIRMED. AVOID long. Short-watch setup building.**

- **System:** B swing, high score; B intraday + scalp (3 untracked alerts). 24h +55%. OI -16.6% while price +55% = **short covering only, not fresh long positioning**. Funding: -0.0008 (shorts losing, being forced out).
- **New catalysts (confirmed external):**
  - Aster Exchange: leveraged perpetual contracts up to 5x on TLM — July 4 launch
  - Alien Worlds tournament: 7,000 TLM/day through July 9 (200,000 TLM total prize pool)
  - Volume: 11x 30-day average (July 2 data)
- **Delisting risk (confirmed):** Binance delisting monitoring ACTIVE since May 22, 2026. INDODAX migrating TLM from BEP20 to ERC20 (deposits/withdrawals suspended since May 29). Not resolved.
- **RSI:** 84.04 — overbought. Current price ~$0.0025. Support $0.00208.
- **Pattern read:** Classic pre-delist pump. Shorts are covering (OI declining). When short covering exhausts, profit-taking begins. Aster leverage launch could temporarily sustain but doesn't resolve the delist risk.
- **Legal/headline:** ACTIVE exchange_delisting catalyst. Basket: delisting_thin_liquidity (avoid_low_liquidity playbook). **Verdict overrides score.**
- **Short watch trigger:** 1h close below $0.00208 (support) after failed retest of $0.0025 resistance. Confirm OI starts rising again (new shorts entering, not just covering ending). RSI crosses below 70. **NOT a live short now — need the structure first.**
- **Verdict: AVOID LONG. Short-watch (not yet live). 3 untracked TLM alerts today = system integrity gap (→ TODO). Do not act on system score — headline risk overrides.**

---

### Candidate 4 — EPIC/USDT (B swing 73.9 / B intraday 68 / B scalp 75 — WAITING FOR ENTRY)

**STATUS: WAITING FOR ENTRY (swing) / TRIGGERED (intraday + scalp). Cleanest no-catalyst entry structure.**

- **System:** B swing 73.9/100 (waiting), entry 0.6442-0.6635, current ~0.6720. B intraday 68.1/100 (triggered). B scalp 75.0/100 (triggered). OI +13.33%. Funding: 4.368e-05 (neutral). Long/short 0.714 (long-biased). 24h +24.21%, 7d +51.69%. Volume 1.83x.
- **Catalyst:** None verified internally or externally. In momentum_breakout basket (avoid_chase playbook). No-catalyst intraday playbook: WR 23%, PF 0.70 (losing).
- **Entry quality:** Swing entry zone 0.6442-0.6635 is within 1.3-4.2% of current price 0.6720. ATR 0.0427 → ~1 ATR below current. Reasonable pullback target. RR to TP1: 1.84 (TP1 0.7147). Invalidation: 1h close below 0.6207.
- **Chase risk:** MODERATE. 24.2% 24h with 1.83x volume — less overextended than HMSTR but still extended. Wait for the zone.
- **Mood alignment:** Risk-on supports but no catalyst. Swing playbook (WR 72%) is strong regardless. No-catalyst intraday (WR 23%) is weak — scalp even weaker (avoid).
- **Verdict: WATCHLIST / WAITING FOR ENTRY. Cleaner than HMSTR for risk/reward (neutral funding, lower OI, more structured move). No catalyst reduces conviction vs DOGE. Act on swing entry only if price returns to 0.6442-0.6635 with structure. Skip scalp (low_confidence).**

---

### Candidate 5 — ETH/USDT (B intraday TP HIT — CATALYST WATCH for Monday open)

**STATUS: B intraday CLOSED WIN (TP HIT). Macro catalyst-watch — best for Monday session.**

- **System:** B intraday 66.2/100 (tp_hit = CLOSED WIN). B scalp 67.1/100 (triggered). ETH trend: uptrend. ETH/BTC = 0.028159. Estimated ETH ~$1,689 (BTC ~$60K).
- **Catalysts (confirmed external):**
  - **CLARITY Act:** ETH classified as CFTC digital commodity. Bill is 4 steps from law. Senate Banking Committee passed May 14 (15-9). Needs 60-vote threshold — ~7 Democratic votes short. August recess = critical deadline (failure could push to 2030 per Senator Lummis). Polymarket: 59% odds passage in 2026. White House targeted July 4 signing — NOT achieved, Senate floor vote not yet scheduled.
  - **ARB/Robinhood Chain:** $50M TVL just days after mainnet launch (CryptoBriefing July 4) — validates Ethereum L2 ecosystem.
  - **Ethereum eyes $2K:** Multiple analyst reports; regulatory clarity is the primary driver cited.
- **Chase risk:** Intraday signal already CLOSED WIN (resolved). Scalp low_confidence — skip. Swing entry not in current top-20.
- **What makes ETH actionable for Monday:** Senate schedules CLARITY Act floor vote → positive catalyst upgrade. BTC holds $60K+ through weekend → supports ETH continuation.
- **Verdict: CATALYST WATCH (not a live trade this window). Intraday CLOSED WIN. Monitor Senate CLARITY Act news over weekend. Best candidate for Monday pre-open if news confirms. Do not enter scalp (low_confidence).**

---

## 8. Best Candidates Ranked

*(Weekend mode — all entries require pullback confirmation, no market buys)*

| Rank | Symbol | Mode | Status | Score | Side | Catalyst | Trigger |
|---|---|---|---|---|---|---|---|
| 1 | DOGE/USDT | Swing/Intraday/Scalp | WAITING/TRIGGERED | 73.9-77.2 | Long | ✅ news_supported=1 | Intraday triggered; swing: pullback + 15m hold |
| 2 | HMSTR/USDT | Swing | WAITING | 78.0 | Long-watch | ❌ none | Pullback to 0.0003 zone with volume; no catalyst = lower conviction |
| 3 | EPIC/USDT | Swing | WAITING | 73.9 | Long-watch | ❌ none | Pullback into 0.6442-0.6635 zone |
| 4 | ETH/USDT | — | TP HIT (CLOSED WIN) | 66.2 | Catalyst-watch | ✅ Clarity Act | Monday: Senate floor vote news; BTC holds $60K+ |
| 5 | TLM/USDT | Short-watch | AVOID long | HIGH | Short-watch | ⚠️ mixed (delist + Aster) | Failed $0.0025 retest → 1h close below $0.00208 |

**Best long-watch:** DOGE/USDT — intraday already TRIGGERED (monitor TP); swing: pullback + confirm hold
**Best short-watch:** TLM/USDT — trigger: 1h close below $0.00208 after $0.0025 failed retest
**Best catalyst-watch:** ETH/USDT — Senate CLARITY Act floor vote announcement is the primary trigger for Monday

---

## 9. Avoid / No Trade (this window only — system continues scanning)

1. **TLM/USDT long:** Binance delisting monitoring active. RSI 84.04. Aster catalyst real but delist risk dominates. AVOID.
2. **Scalp signals (all):** `crypto_scalp_momentum_continuation` WR 12%, PF 0.14, -6R. LOW CONFIDENCE. No action.
3. **MIRA/USDT new longs:** Negative funding (-0.008 bybit, -0.008 mexc). Elevated crowding. OI +48% with crowding unknown. MEXC-only cap concern.
4. **HMSTR/USDT breakout chase:** At current price only. Demand pullback to 0.0003 first.
5. **ANSEM/USDT:** +93.77% 24h, 0.09x volume (extremely thin). MEXC-only listing cap.
6. **Stocks (all):** CLOSED today. No RTH confirmation possible until Monday 09:30 ET.
7. **Intraday without catalyst:** Playbook WR=23%, PF=0.70. Only intraday WITH catalyst (DOGE confirmed) is valid.

*This list applies to the current decision window only. The scanner continues, candidates keep generating, and outcomes keep being recorded in all market conditions.*

---

## 10. Main Risks

1. **TLM contagion:** Binance official delist announcement → TLM -50-80%; SYN (also Watch Label) may cascade. Monitor Binance.
2. **Weekend liquidity wicks:** Thin volume = gap-through stops. Size down on all weekend entries.
3. **HMSTR reversal:** No catalyst + OI extreme (131%) + L/S short-biased. If longs get trapped, rapid reversal possible. 44/118 symbols in post-unwind chop.
4. **F&G divergence:** F&G=22 (Fear) while price uptrends — retail is scared. Either continuation (smart money buys) or fragile (retail right). BTC 4h close below EMA20 = early warning.
5. **CLARITY Act Senate failure:** Bill may slip past August recess → delay to 2030 (Senator Lummis warning). ETH loses biggest macro catalyst if this happens.
6. **All-long correlation cluster:** 50 active signals all LONG. Zero hedge. BTC drop = simultaneous deterioration across all.
7. **Untracked alerts (5):** ADA and TLM signals sent to Telegram without proposed_signal backing. Unknown outcome impact on PF stats.
8. **Hinkal protocol exploit ($820K USDC):** Minor for now, but DeFi exploit news can dampen sentiment in smart contract / DeFi tokens.

---

## 11. Action Plan — next 4 hours

*(US markets CLOSED — Independence Day. Crypto-only session.)*

| Priority | Action | Symbol | Trigger | Notes |
|---|---|---|---|---|
| 1 | Monitor | DOGE/USDT intraday/scalp | Already triggered — watch for TP | Catalyst-backed, news_supported=1 |
| 2 | Wait for pullback | DOGE/USDT swing | Pullback + 15m structure hold | Don't chase current level |
| 3 | Watch-only | HMSTR/USDT | Pullback to 0.0003 zone | No catalyst — lower conviction |
| 4 | Watch-only | EPIC/USDT | Pullback to 0.6442-0.6635 | Clean entry if price retraces |
| 5 | Monitor for short | TLM/USDT | 1h close below $0.00208 | NOT live short yet; need structure |
| 6 | Catalyst watch | ETH/USDT | Senate CLARITY Act news; BTC structure | Best candidate for Monday open |
| 7 | No action | All stocks | CLOSED — Monday 07/07 09:30 ET | Plan Monday watchlist over weekend |
| 8 | No action | All scalp signals | Low_confidence (PF 0.14) | Skip; data collection only |
| 9 | Manual review | Untracked alerts | ADA/TLM without proposed_signal | 5 alerts — TODO for manual session |

**Monday July 7 open planning:**
- ETH: Clarity Act weekend news could drive gap — check Senate developments Sunday
- DOGE: X Money DOGE integration announcement = major catalyst upgrade if confirmed
- Stocks: Require fresh intraday report before acting — do NOT use stale 48h swing/invest data

---

## 12. Final Verdict per Mode

| Mode | Playbook | Status | Verdict |
|---|---|---|---|
| Crypto swing | crypto_swing_narrative_rs_momentum | actionable | DOGE pullback (catalyst), HMSTR/EPIC wait-for-zone. TLM AVOID. |
| Crypto intraday (catalyst) | crypto_intraday_catalyst_or_momentum | actionable | DOGE TRIGGERED. ETH TP HIT. |
| Crypto intraday (no catalyst) | crypto_intraday_catalyst_or_momentum | weak | AVOID — WR 23%, PF 0.70 |
| Crypto scalp | crypto_scalp_momentum_continuation | low_confidence | DO NOT TRADE — WR 12%, PF 0.14 |
| Crypto short | crypto_failed_bounce_short | watch_only | TLM short-watch (trigger needed). SYN: extended, squeeze risk. |
| Stocks intraday | stocks_intraday_rth_momentum | CLOSED | No action — Independence Day. Monday 07/07. |
| Stocks swing | stocks_swing_growth_breakout | shadow_only | Research only — never Telegram-actionable. |

**Paper portfolio (bybit fee profile, $5,000 base):** $1,914.72 net (+38.3%). MEXC: $2,267 (+45.3%). Conservative: $1,667 (+33.4%). Shadow B forward +67.98R vs A -97.57R — B gap widening but NOT_READY (4/6 lanes, 9d < 14d required).

---

## 13. Sources

- [TLM Rockets 55% on Leveraged Contracts and Alien Worlds Tournament Amid Broader Crypto Rally](https://www.interactivecrypto.com/tlm-rockets-55-on-leveraged-contracts-and-alien-worlds-tournament-amid-broader-crypto-rally-jul) — InteractiveCrypto, 2026-07-04. *Confirms Aster leverage + tournament catalysts; Binance delisting monitoring still active; RSI 84.04; OI declining.*
- [CLARITY Act Is Four Steps Away From Becoming Law Before August Recess](https://finance.yahoo.com/markets/crypto/articles/clarity-act-four-steps-away-111715412.html) — Yahoo Finance, 2026-07-04. *Senate committee cleared May 14; 60-vote threshold needed; 7 Dems short; Aug recess deadline critical.*
- [Congress Is Moving Forward With the Clarity Act — Ethereum Best Buy This Summer](https://finance.yahoo.com/markets/crypto/articles/congress-moving-forward-clarity-act-111500182.html) — Yahoo Finance / Motley Fool, 2026-07-04. *ETH CFTC commodity classification narrative.*
- [Dogecoin Price Prediction as DogeOS Targets Summer Launch](https://www.openpr.com/news/4567361/dogecoin-price-prediction-as-dogeos-targets-summer-launch) — OpenPR, 2026-07-02. *DogeOS $6.9M Polychain, TDOG ETF, DOGE commodity classification, X Money beta.*
- [Clarity Act still faces long road despite Senate progress](https://www.coindesk.com/policy/2026/06/30/jefferies-warns-of-crypto-market-volatility-as-clarity-act-faces-senate-test) — CoinDesk, 2026-06-30. *Jefferies on Senate volatility risk.*
- Internal: cycle_06 summary, scalp/intraday/swing reports (fresh), catalyst_cycle_13-03.md, LLM analysis packet, active-signals CLI, signal-stats CLI, detect_untracked_legacy_alerts, paper_monitor_status, market dashboard snapshot (cycle 06 step 15).

---

## 14. Fix Requests / TODO

### TODO-untracked-alerts-surge
- **issue:** 5 untracked legacy crypto alerts today (ADA×2, TLM×3) — signals sent to Telegram without backing `proposed_signal` within ±6h
- **evidence:** `detect_untracked_legacy_alerts --since 2026-07-04`: ADA/USDT B scalp 68.3 (08:16 UTC), TLM/USDT B intraday 67.1 (08:21 UTC), TLM/USDT B scalp 69.8 (10:36 UTC), TLM/USDT B scalp 74.2 (12:57 UTC), ADA/USDT B swing 69.6 (13:25 UTC)
- **suggested manual fix:** Investigate why ADA and TLM generate watchlist_alerts without proposed_signal match. Check if signal_registration is silently failing for these symbols. Verify ±6h window is correct for alert timing.
- **priority:** medium
- **first observed:** 2026-07-04 16:24 EEST

### TODO-scheduler-log-missing
- **issue:** `scheduler.log` not found at expected project root path
- **evidence:** `Get-Item "C:\Users\adama\Documents\crypto-ai-desk\scheduler.log"` → NOT FOUND. Cycle summaries present and fresh (scheduler is running). Log file not at expected location.
- **suggested manual fix:** Check scheduler launch config / Windows Task settings for log path. Verify stdout/stderr redirect is correctly targeting the expected path. May need to update CryptoAIDeskMonitor task configuration.
- **priority:** low (cycle summaries serve as proxy, system operational)
- **first observed:** 2026-07-04 16:24 EEST

### TODO-tlm-delist-catalyst-mapping-consistency
- **issue:** TLM Binance Watch Label / delisting monitoring coverage in catalyst layer was inconsistent across prior cycles (missing in 04:39 review, present in 16:24 cycle)
- **evidence:** 04:39 review noted "TLM Binance Watch Label NOT in catalyst_events.jsonl for TLM." Current cycle 13-03 shows TLM as exchange_delisting in notable events — mapping improved but consistency needs verification.
- **suggested manual fix:** Verify that exchange_delisting catalyst events for TLM appear consistently every cycle with the TLM symbol correctly mapped. If intermittent, check catalyst symbol resolver logic for tokens under delisting monitoring.
- **priority:** medium
- **first observed:** 2026-07-04 04:39 EEST (first), reconfirmed 16:24 EEST

### TODO-scalp-low-confidence-telegram-filter
- **issue:** B scalp signals continue generating Telegram alerts despite playbook flagged as low_confidence (WR 12%, PF 0.14, -6R 14d). 3 untracked TLM scalp alerts sent today.
- **evidence:** signal-stats observation: `crypto_scalp_momentum_continuation: low_confidence`. LLM packet playbook table explicitly labels it low_confidence. Yet TLM scalp 69.8 and 74.2 were sent to Telegram today without proposed_signal match.
- **suggested manual fix:** Add pre-send filter for scalp signals that checks playbook_status = low_confidence. If low_confidence, require manual approval before Telegram send or prefix alert with "⚠️ low_confidence scalp — research only."
- **priority:** medium
- **first observed:** 2026-07-04 16:24 EEST
