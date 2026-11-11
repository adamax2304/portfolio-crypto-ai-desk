# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

**Slot:** pre-US-open decision review | **Time:** 2026-07-05 16:20 EEST
**Previous review:** 2026-07-05 11:39 EEST (Europe / pre-US context)
**Advisory only — no auto-trade. Weekend mode active (Sunday). Stocks CLOSED (US holiday weekend, reopens Mon Jul 6).**

> **NOTE ON TIMING:** July 5, 2026 is a Sunday. US markets do NOT open today. The "pre-US-open" slot fires at 16:20 EEST = 09:20 ET, which is 10 minutes before the 09:30 ET cash open — but on a Sunday this is the pre-MONDAY planning window. The first post-July-4 holiday US session is Monday July 6. All stock signals are planning context only; crypto is the live actionable class.

---

## 1. Executive Summary

**Slot:** pre-US-open decision review (Sunday pre-Monday planning). Advisory only, no auto-trade. Weekend mode active.

**Regime:** Bullish trend (risk-on). BTC/ETH both in uptrend. Altcoin breadth 79.5% above EMA20 (swing, most recent). F&G at 23 (Fear) diverges from bullish technicals — historically this divergence supports continuation rather than reversal in trending conditions. Macro risk 55/100 (3 risk-off hits from exploit/hack news; 0 risk-on counter-hits).

**CATALYST MAPPING WEAK THIS RUN — 28.3% mapped (543/1916 events). Use catalyst layer as context, not final decision.**

**What changed since 11:39:** Cycle 6 launched ~16:05 EEST, generating fresh scalp/intraday/swing reports (16:06/16:11/16:23 EEST). BCH/USDT swing signal triggered (entered). Multiple signals reached TP level: VANRY intraday/swing, HEI intraday, HMSTR swing, OGN scalp, TRUMP intraday, DOGE intraday. Untracked alerts grew from 8 to 10 (BCH scalp 13:06 UTC + AIGENSYN swing 13:23 UTC added). Active signals: 50 (live CLI).

**Best long candidate:** BCH/USDT — swing B triggered, cleanest derivatives (OI +3.49%, near-zero funding), volume 1.31x (highest in field), multi-exchange confirmed (Binance + MEXC, 88.7%). Entry ~239-242, invalidation 237.11, TP1 246.

**Short watch:** VANRY/USDT — if price fails retest of post-impulse support after +50% 24h run. Do NOT enter short on momentum/chase.

**Catalyst watch:** ADA/USDT — RealFi Testnet launches TOMORROW (July 6, Monday), ETF SEC review window Aug 9. ADA intraday B currently triggered. Pre-Monday-open setup.

**Key avoids:** VANRY (post-impulse, +50%, massive OI), HOT (extreme funding -1.18%/8h, OI +169%, squeeze risk), ETH/SOL/APT (exploit_hack operator-review blocks), TLM (delisting block — no new entries), no-catalyst intraday (documented -3R/14d).

---

## 2. Data Used

| Source | Mtime / Freshness | Status |
|---|---|---|
| scheduler.log | 16:23 EEST today | **FRESH** |
| cycle_05_13-39_summary.md | 13:59 EEST today (~2.4h) | **FRESH** |
| scalp report `2026-07-05_13-06` UTC | 16:06 EEST (14 min ago) | **FRESH** |
| intraday report `2026-07-05_13-11` UTC | 16:11 EEST (9 min ago) | **FRESH** |
| swing report `2026-07-05_13-23` UTC | 16:23 EEST (now) | **FRESH** |
| stocks_intraday `2026-07-03_20-07` | 07/03 23:07 EEST | **STALE** (>14h, holiday weekend) |
| stocks_swing `2026-07-02_13-03` | 07/02 16:03 EEST | **STALE** (>14h) |
| stocks_invest `2026-07-02_13-05` | 07/02 16:05 EEST | **STALE** (>14h) |
| catalyst_events.jsonl | cycle ~16:06 EEST | **FRESH** |
| narrative_baskets.jsonl | cycle ~16:06 EEST | **FRESH** |
| llm_analysis_packet.md (swing) | 16:23 EEST | **FRESH** |
| active-signals CLI (crypto) | live 16:20 EEST | **LIVE (50 signals)** |
| signal-stats CLI (crypto) | live 16:20 EEST | **LIVE** |
| detect_untracked_legacy_alerts | live 16:20 EEST | **LIVE (10 untracked)** |
| paper monitor status (cycle 5) | 13:59 EEST | **carry-forward (2.4h)** |
| Previous enriched review (ADA/ETHFI research) | 11:39 EEST | external research from prior run (within 4h validity) |

**Notes:**
- Stocks CLOSED (holiday weekend; reports stale by design).
- Weekend mode active: A-tier penalty, confidence step-down, require retest after impulse, MEXC-only capped C.
- Onchain: `interface_ready_config_missing` (no config/onchain.yaml).
- Social sources: Reddit all 403. No live X/Telegram/KOL connectors.
- TradingView/manual chart unavailable — using OHLCV/ATR/EMA from reports only.
- **External web research: NOT PERFORMED THIS SLOT** (internal data fresh and sufficient; prior run's ADA external research within 4h validity window). Declared here per §N source-discipline checklist.

---

## 3. Scheduler / Data Freshness

- **Scheduler (cycle 5):** Completed at 13:59 EEST, scheduler.log updated at 16:23 EEST (cycle 6 evidence). Steps: ok=27 failed=0. **FRESH.**
- **Cycle 6:** Evidence: scheduler.log at 16:23, fresh reports at 16:06/16:11/16:23, new crypto_monitor pid 1783257818 launched 16:23. Cycle 6 is running or just completed. No cycle_06 summary file yet.
- **Mode:** weekend (crypto-only). Stocks data collection paused; actionability disabled.
- **Paper monitor status (cycle 5, 13:59 EEST — carry-forward ~2.4h):**
  - OPEN ACTIONABLE: 7
  - WAITING FOR ENTRY: 2
  - ENTERED UNRESOLVED (expired-after-entry): 35 — entry filled, no TP/SL before window — NOT missed entries
  - REVIEW/SHADOW: 160
  - NO-ENTRY / STALE / MOVED AWAY: 38
  - CLOSED (cumulative): 379W / 58L / 0flat
  - NEEDS REVIEW: 0
- **Untracked legacy alerts:** 10 (grew from 8 at 11:39 review). New: BCH scalp 13:06 UTC + AIGENSYN swing 13:23 UTC. All sent to Telegram without tracking.
- **Intelligence layer:** crypto monitor running (pid 1783257818). Derivatives: OI numeric history sparse; MEXC fallback for HOT, VANRY, AIGENSYN, HEI, LAB. Squeeze phase: 52 post_unwind_chop, 6 squeeze_expansion, 25 build_up, 2 unwind.
- **Weekend mode adjustments active:** A-tier penalty, confidence step-down, overextension 1.25x, require retest, tight stop.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-05 16:20 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "derivatives_sparse", "onchain_config_missing"],
      "data_missing": ["cycle_06_summary", "stocks_reports_current", "social_attention_live", "onchain_data", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log at 16:23 EEST — FRESH; cycle 5 finished 13:59 EEST (~2.4h)",
        "scalp/intraday/swing reports from cycle 6: 16:06/16:11/16:23 EEST — all FRESH",
        "Stocks reports stale by design (holiday weekend, markets closed since Jul 3)",
        "10 untracked legacy alerts (grew from 8 at 11:39 review — BCH scalp + AIGENSYN swing added)",
        "MEXC fallback dominant for altcoins (HOT, VANRY, HEI, AIGENSYN, LAB)",
        "onchain: interface_ready_config_missing",
        "Weekend mode active: Sunday Jul 5"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.83,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": ["live_btc_price_usd", "DXY_yields", "macro_calendar_mon_jul6", "social_sentiment_live"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: uptrend; ETH trend: uptrend (all three fresh reports)",
        "Altcoin breadth: 79.5% above EMA20 (swing), 73.0% (intraday) — broad but slightly pulled back from 86.8% at 11:39",
        "Regime label: bullish trend; style: selective longs, prefer pullbacks on RS",
        "F&G: 23 (Fear) — diverges from bullish technicals; historically supports continuation",
        "VIX: 16.15 (low, risk-on); SPY: up; QQQ: down (mixed US equity signal)",
        "Macro risk 55/100 (3 risk-off: SOL exploit, ETH hack, UXLINK; 0 risk-on)",
        "Fed positive signals for crypto (CryptoBriefing basket — regulatory_sector_headline)",
        "Weekend mode: thinner liquidity, wider wicks expected"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "stale_catalyst", "narrative_supported"],
      "data_missing": ["social_feeds_live", "monday_economic_calendar", "etf_flow_data"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Catalyst JSONL: 28.3% mapped (543/1916 total) — WEAK (unmapped > 50%)",
        "ADA: RealFi Testnet launches July 6 (tomorrow), ETF SEC window Aug 9 (prior review, within 4h validity)",
        "HYPE: Hyperliquid 9% global perps market, $4B OI (CryptoBriefing, internal)",
        "ETH/SOL/APT: exploit_hack blocks active",
        "TLM: delisting block active (Binance monitoring, +107% 7d, +584% vol)",
        "Fed positive regulatory signals (advisory context only; not a score input)",
        "4 baskets: delisting_thin_liquidity (HYPE), perps_dex_narrative (HYPE), ai_narrative (NEAR/RENDER/TAO/FET), momentum_breakout (ULTIMA/BTW/NFP)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["squeeze_risk", "post_unwind_chop", "oi_supports", "funding_extreme"],
      "data_missing": ["OI_numeric_history_full", "liquidation_heatmaps", "order_book_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "HOT: funding -0.011895 (EXTREME, -1.18%/8h), OI +169.01%, crowding unknown — SQUEEZE RISK",
        "VANRY: OI +242.04% (massive), funding -0.001463 MEXC / -0.00001 Bybit, crowding unknown — post-impulse",
        "AIGENSYN: funding -0.002497 MEXC, OI +14.22%, crowding unknown — elevated",
        "BCH: OI +3.49%, funding ~0 (-2.5e-5), long/short 1.843, crowding normal — CLEANEST",
        "HEI: OI +18.33%, funding -0.000138, crowding normal — healthy",
        "BTW: OI +12.99%, funding +0.000271 (positive = longs paying), crowding normal",
        "Squeeze phase: 52 post_unwind_chop, 6 squeeze_expansion, 25 build_up — most already unwound"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "ok",
      "confidence": 0.76,
      "reason_codes": ["entry_fresh", "clean_retest", "chase_risk", "overextended"],
      "data_missing": ["live_chart", "order_book", "vwap_anchoring", "level2_data"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BCH: price ~241-242, entry zone 239.35-241.19, within 1 ATR (4.07); invalidation 237.11; resistance 242.80",
        "BCH: volume 1.31x (above average, highest in field); setup quality 68.5/100",
        "VANRY: +50.6% 24h, OI +242%, overextended — CHASE RISK",
        "HOT: price truncation issue (0.0004 entry/targets identical) — data suspect for micro-price assets",
        "ULTIMA/BTW: rejected (MEXC-only + >2 ATR from EMA20)",
        "Shorts rejected: all fight bullish tape + squeeze risk flags",
        "TradingView unavailable — OHLCV/ATR/EMA from reports only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.83,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry"],
      "data_missing": ["cycle_06_paper_monitor_status", "exact_unresolved_entry_timing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE: 7 (cycle 5 paper monitor, 2.4h carry-forward)",
        "WAITING FOR ENTRY: 2",
        "ENTERED UNRESOLVED (expired-after-entry): 35 — entry filled, no TP/SL before window — NOT missed entries, NOT a PF metric",
        "REVIEW/SHADOW: 160",
        "NO-ENTRY / STALE / MOVED AWAY: 38",
        "CLOSED (cumulative): 379W / 58L / 0flat",
        "NEEDS REVIEW: 0",
        "Active signals (live CLI): 50 crypto; many at tp_hit: BCH, VANRY, HEI, HMSTR, OGN, TRUMP, DOGE, KITE, ARB, ZEC, ZK",
        "BCH swing B: triggered (entered); DOGE swing B: triggered; ADA intraday B: triggered"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk", "manual_review"],
      "data_missing": ["daily_R_aggregate_cycle6", "portfolio_drawdown_live", "correlation_cluster_sizing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "5 production blocks active: APT (exploit), ETH (exploit), SOL (exploit), TLM (delisting), UNH (legal/stocks)",
        "Weekend mode: PF weekend=Y 1.93 vs weekend=N 4.02 (significant drag)",
        "Intraday mode: PF 1.4, avgR 0.05 (weakest; no-catalyst intraday -3R/14d)",
        "Scalp mode: PF 3.7, avgR 0.6 (strongest)",
        "Swing: PF 2.3, avgR 0.4 (solid for weekend)",
        "10 untracked alerts ongoing — systemic PART 1 regression",
        "HOT extreme funding (-1.18%/8h) + OI +169% = squeeze risk"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.79,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["A_tier_recent_performance", "intraday_catalyst_split_live"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "B-tier scalp n=105 (reliable): PF 3.7x, avgR 0.6R — BEST THIS WEEK",
        "B-tier intraday n=114 (reliable): PF 1.4x, avgR 0.05R — WEAKEST (no-catalyst driver)",
        "B-tier swing n=88 (reliable): PF 2.3x, avgR 0.4R — solid",
        "Longs PF 2.7x; Shorts PF 0.9x (shorts net-negative — avoid)",
        "Weekend=Y PF 1.93 vs Weekend=N PF 4.02 — significant drag confirmed",
        "Shadow B forward: +32.94R vs A -129.46R — B model shows edge, NOT_READY (4/6 gates, <14d window)",
        "Total: n=307, WR 23%, PF 2.63, avgR 0.39, totalR +81.67R (week)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "normal",
      "confidence": 0.78,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Regime bullish trend, breadth strong, F&G fear divergence supports continuation",
        "BCH already in position (swing B triggered) — best active setup",
        "ADA catalyst (RealFi Testnet tomorrow) — pre-Monday catalyst watch",
        "No A-tier; all B-tier with low confidence from weekend mode",
        "Catalyst weak (28.3% mapping); rely on technical + RS structure",
        "VANRY: longs captured, now short-watch on failed retest only",
        "HOT/TLM/ETH/SOL/APT: avoid new entries",
        "Intraday no-catalyst: documented negative — avoid"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.78,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "BCH/USDT",
      "trigger": "swing B already triggered; pullback to 239-241 zone if not yet in; hold while above 237.11 invalidation",
      "reason": "Cleanest derivatives (OI+3.49%, near-zero funding), volume 1.31x, multi-exchange Binance+MEXC, 7d +25%, no blocks"
    },
    "best_short_candidate": {
      "symbol": "VANRY/USDT",
      "trigger": "failed retest below post-impulse support — wait for rejection at prior breakout level with volume, NOT momentum short",
      "reason": "Post-impulse +50.64% 24h, OI +242%, negative funding across Bybit/MEXC; needs retest failure, not a chase"
    },
    "best_catalyst_candidate": {
      "symbol": "ADA/USDT",
      "trigger": "intraday B triggered; entry zone 0.1859-0.1871; invalidation 0.1847; RealFi Testnet launches Mon Jul 6 (tomorrow)",
      "reason": "Imminent catalyst (Testnet tomorrow), intraday triggered, ETF SEC window Aug 9, news_supported flips today"
    },
    "avoid_candidate": {
      "symbol": "HOT/USDT",
      "reason": "Extreme negative funding (-1.18%/8h), OI +169%, crowding unknown, price data truncation bug — squeeze risk on thin weekend liquidity"
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
|---|---|---|---|---|
| data_quality | ok | 0.88 | scheduler_fresh, derivatives_sparse, onchain_config_missing | advisory_only |
| market_regime | ok | 0.83 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.68 | squeeze_risk (HOT), post_unwind_chop, oi_supports (BCH) | advisory_only |
| technical_entry | ok | 0.76 | entry_fresh (BCH), clean_retest, chase_risk (VANRY/HOT) | advisory_only |
| execution_lifecycle | ok | 0.83 | open_actionable:7, waiting:2, entered_unresolved:35 | advisory_only |
| risk_manager | caution | 0.80 | headline_risk, legal_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | ok | 0.79 | playbook_working (scalp/swing), playbook_failing (intraday no-catalyst) | advisory_only |
| head_trader | normal | 0.78 | risk_on, longs_preferred, catalyst_watch (ADA) | advisory_only |

---

## 4. What Changed vs Previous Review

**Previous review:** 2026-07-05 11:39 EEST (Europe / pre-US context)

| Item | 11:39 state | 16:20 state | Assessment |
|---|---|---|---|
| BCH/USDT | No-entry in active signals | Swing B TRIGGERED — entered ~239-242 | **NEW — confirmed entry** |
| ADA/USDT | Top long candidate swing B (72.6), pullback 0.1890-0.1910 | Intraday B triggered; Testnet still imminent | **Thesis CONFIRMED — T-1 day to Testnet** |
| VANRY/USDT | Short watch (post-impulse +64%), elevated crowding | +50.6% 24h (slightly cooled), OI +242%, longs TP hit | **Continues as short-watch; longs captured** |
| ETHFI/USDT swing B | Active long candidate | In TP-hit zone; no re-entry | **Unchanged — TP zone, monitoring** |
| EPIC/USDT | Stale flagged (-37%) | Rejected from all reports | **Invalidated** |
| Untracked alerts | 4 (08:27 cycle) | 10 (grew +6) | **DEGRADED** |
| Active signals | ~50 (11:39) | 50 live | Stable count; composition shifted to TP-hit |
| Catalyst mapping | 28% (1478 events) | 28.3% (1916 events) | Stable-weak |
| Regime breadth | 86.84% EMA20 | 79.5% EMA20 | Slight pullback — still strong |
| HOT squeeze risk | Elevated funding noted | Extreme -1.18%/8h, OI +169% | **Worsened — explicit flag** |
| DOGE/USDT | Not featured | Swing B triggered (73.x), intraday TP hit | **NEW — activated** |
| AIGENSYN | Scalp B caution | Swing B untracked alert sent | Elevated crowding, WATCH only |

---

## 5. Catalyst Coverage

- **Total events today:** 1,916
- **Mapped (symbol identified):** 543 (28.3%)
- **Unmapped (null symbol):** 1,373 (71.7%)
- **Narrative baskets:** 4

> **CATALYST MAPPING WEAK THIS RUN — use catalyst layer as context, not final decision.**

**Active narrative baskets:**

| Basket | Playbook | Freshness | Primary symbols |
|---|---|---|---|
| delisting_thin_liquidity | avoid_low_liquidity | <6h | HYPE/USDT |
| perps_dex_narrative | wait_pullback | <24h | HYPE/USDT |
| ai_narrative | related_beta_rotation | fresh unknown | NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT |
| momentum_breakout | wait_pullback | <1h | ULTIMA/USDT, BTW/USDT, NFP/USDT |

**Notable mapped events:**
- APT: exploit_hack — Aptos critical vulnerability (CryptoBriefing) → BLOCK active
- ETH/SOL: exploit_hack — Step Finance $21M launder, UXLINK 14,336 ETH → BLOCK active
- TLM: delisting — Binance monitoring, +107% 7d, +584% vol → BLOCK active (new entries)
- HYPE: perps_dex milestone — $4B OI, 9% global perps (CryptoBriefing) → catalyst-watch
- ADA: 2 news_supported flips in catalyst label refresh (cycle 5) → confirms attention
- UNH: legal_risk — DOJ probe, -16% (QuiverQuant) → stocks closed, advisory only

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-on (BTC uptrend, ETH uptrend, breadth 79.5%, bullish regime)
- **Stocks mood:** CLOSED (US holiday weekend; Monday July 6 is first post-holiday session)
- **Dominant narrative:** RS momentum longs (BCH, ADA, HEI); exploit/hack tail risk (ETH/SOL); TLM delisting squeeze; HYPE perps DEX; Fed positive regulatory signals
- **Preferred side now:** longs (selective, pullback entry, RS-leader confirmation); shorts only on failed retest of post-impulse (VANRY)
- **Best long candidate:** BCH/USDT — already triggered swing B; pullback to 239-241 actionable above 237.11
- **Best short candidate:** VANRY/USDT — wait for failed retest of post-impulse support; NOT a momentum short
- **Best catalyst-backed candidate:** ADA/USDT — RealFi Testnet launches tomorrow (Mon Jul 6); ETF window Aug 9; intraday B triggered; entry 0.1859-0.1871
- **What to avoid:** VANRY momentum chase, HOT (squeeze risk), ETH/SOL/APT (blocks), TLM new entries (delisting block), no-catalyst intraday
- **What would change the view:** BTC closes below local support (regime flip) → reduce all long aggression; VANRY fails retest below post-impulse support → activates short; ADA loses 0.1847 → removes catalyst candidate

---

## 7. Candidate Deep Dives

### Candidate 1: BCH/USDT — Swing B, OPEN (TRIGGERED)

**Status:** OPEN ACTIONABLE — swing B triggered, entered ~239-242 zone. Score 75.x.

**Setup:**
- Price: ~241-242 | ATR: 4.071
- Entry zone: 239.35-241.19 | Invalidation: 237.11 (1h close)
- TP1: 246.07 | TP2: 250.14 | TP3: 254.21
- Volume: 1.31x (highest in field, above average)
- RS vs BTC: +6.35% 24h, +25.52% 7d (consistent RS leader)
- Multi-exchange: Binance (anchor) + MEXC, 88.7% confirmation

**Derivatives:** OI +3.49% (orderly), funding −0.0000248 (near-zero, neutral), long/short 1.843, crowding normal. **Cleanest derivatives in field.**

**Chase risk:** LOW — price within 1 ATR of entry zone. Immediate resistance at 242.80.

**Verdict:** OPEN — manage above 237.11. Pullback to 239-241 is valid continuation entry if not yet filled.

---

### Candidate 2: ADA/USDT — Intraday B, OPEN (TRIGGERED) + Pre-Monday Catalyst

**Status:** OPEN ACTIONABLE (intraday B triggered). Score 66.x.

**Setup:**
- Price: ~0.1877 | ATR: 0.0028
- Entry zone: 0.1859-0.1871 | Invalidation: 0.1847 (1h close)
- TP1: 0.1905 | TP2: 0.1933 | TP3: 0.1961
- RS vs BTC: +4.6% 24h, +29.99% 7d (multi-day RS leader)
- Volume: 0.08x (below average)

**Catalyst:** RealFi Testnet launches July 6 (TOMORROW, Monday) — imminent, T-1 day. ETF SEC window Aug 9.

**Verdict:** OPEN ACTIONABLE + CATALYST-WATCH for Monday. Highest fundamental conviction due to imminent Testnet.

---

### Candidate 3: HYPE/USDT — Catalyst-Watch Only

**Status:** NOT in B-tier. WATCH ONLY.

**Contradiction:** Both delisting_thin_liquidity (avoid) and perps_dex_narrative (wait_pullback) — wait for clean B-tier signal.

---

### Candidate 4: TLM/USDT — BLOCK Flag

**Status:** Delisting block active. No new entries. Existing open tracking continues.

---

### Candidate 5: VANRY/USDT — Post-Impulse Short Watch

**Status:** Longs at TP-hit. Short-watch only on failed retest of post-impulse support. Do NOT enter now (+50% 24h, OI +242%).

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Side | Status | Why |
|---|---|---|---|---|---|
| 1 | BCH/USDT | Swing B | Long | OPEN ACTIONABLE (triggered) | Cleanest setup, vol 1.31x, normal derivatives, multi-exchange |
| 2 | ADA/USDT | Intraday B | Long | OPEN ACTIONABLE (triggered) | Catalyst (Testnet tomorrow Mon Jul 6), RS leader, pre-Monday |
| 3 | HYPE/USDT | — | Catalyst-watch | WATCH ONLY | Perps DEX milestone, wait pullback + signal |
| 4 | DOGE/USDT | Swing B | Long | OPEN (triggered 73.x) | Major asset, triggered, regime-aligned |
| 5 | VANRY/USDT | — | Short-watch | WAITING FOR TRIGGER | Post-impulse failed retest required |

---

## 9. Avoid / No Trade

| Symbol | Reason | Block type |
|---|---|---|
| VANRY/USDT | Post-impulse +50%, OI +242%, chase risk — wait failed retest | Risk routing |
| HOT/USDT | Extreme funding (−1.18%/8h), OI +169%, price data truncation, squeeze risk | Squeeze risk |
| ETH/USDT | exploit_hack operator review required | Production block |
| SOL/USDT | exploit_hack operator review required | Production block |
| APT/USDT | exploit_hack block | Production block |
| TLM/USDT | Delisting block — no new entries | Production block |
| Any no-catalyst intraday | Documented −3R/14d | Playbook rule |

---

## 10. Main Risks

1. Exploit/hack tail (ETH/SOL/APT blocks active)
2. HOT squeeze bomb (−1.18%/8h funding, +169% OI, thin weekend)
3. Monday gap risk (ADA Testnet launch news → gap-up or post-release disappointment)
4. Catalyst mapping weak (71.7% unmapped — overnight news may be missed)
5. Weekend liquidity (wider spreads/wick-outs on BCH/ADA)
6. Untracked alert regression (10 alerts, PART 1 regression ongoing)
7. Shadow B NOT_READY (<14d window, 4/6 gates)

---

## 11. Action Plan — Next 4 Hours

| Priority | Action |
|---|---|
| HIGH | BCH/USDT swing B: monitor above 237.11; pullback 239-241 = continuation entry |
| HIGH | ADA/USDT intraday B: monitor above 0.1847; watch Testnet news tonight |
| HIGH | All blocks (ETH/SOL/APT/TLM): no new entries |
| HIGH | No new no-catalyst intraday entries on thin weekend volume |
| MEDIUM | VANRY: watch for failed retest trigger only |
| MEDIUM | HYPE: watch for B-tier signal + pullback |
| LOW | Monday open preparation: review ADA news flow |
| STANDING | Do NOT pause/stop scanner/data collection |

---

## 12. Final Verdict per Mode

| Mode | Verdict | Confidence | Action |
|---|---|---|---|
| Crypto Scalp | CAUTION | Low (weekend) | Thin liquidity; paper data only |
| Crypto Intraday | CAUTION | Low | ADA catalyst active; no new no-catalyst intraday |
| Crypto Swing | WATCH / OPEN | Medium | BCH triggered; ADA catalyst; weekend mode |
| Stocks (all) | CLOSED — Planning | N/A | Holiday weekend; reopens Mon Jul 6 |
| Paper Shadow B | NOT_READY | — | 4/6 gates; no promotion action |

---

## 13. Sources

1. "Step Finance exploiter sells $21M in SOL" — CryptoBriefing — Jul 5, 2026 — internal news_items
2. "UXLINK hacker's 14,336 ETH transfers" — AMBCrypto — Jul 5, 2026 — internal
3. ZachXBT Telegram — Jul 2-3, 2026 Tornado Cash/Circle CCTP — internal
4. LookOnChain Telegram — Jul 5, 2026 Step Finance exploiter — internal
5. "Hyperliquid captures 9% of global perps, $4B OI" — CryptoBriefing — Jul 5, 2026 — internal
6. "Aptos fixes critical vulnerability" — CryptoBriefing — Jul 5, 2026 — internal
7. "UnitedHealth DOJ Probe" — QuiverQuant — Jul 5, 2026 — internal
8. "Federal Reserve delivers positive signals for crypto" — CryptoBriefing — Jul 5, 2026 — internal
9. ADA RealFi Testnet Jul 6 + ETF SEC Aug 9 — LBank/CrowdFundInsider — [EXTERNAL, prior review 11:39, within 4h validity]
10. Internal: cycle_05 summary, scalp/intraday/swing reports, active-signals CLI (50), signal-stats CLI, detect_untracked_legacy_alerts (10), catalyst_events.jsonl (1916/543 mapped), narrative_baskets.jsonl (4), llm_analysis_packet.md

---

## 14. Fix Requests / TODO

### TODO-untracked-alerts-regression
- **issue:** 10 untracked legacy crypto alerts today. Alerts sent to Telegram without matching proposed_signal.
- **priority:** high

### TODO-catalyst-mapping-improvement
- **issue:** 28.3% mapped (543/1916). 71.7% unmapped. Empty headlines suggest JSONL formatting gap.
- **priority:** medium

### TODO-hot-price-truncation
- **issue:** HOT/USDT entry/targets show 0.0004/0.0004/0.0005 — sub-satoshi truncation makes setup unreadable.
- **priority:** medium
