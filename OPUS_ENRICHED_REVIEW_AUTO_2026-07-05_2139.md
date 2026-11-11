# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

**Slot:** late-session risk review | **Time:** 2026-07-05 21:39 EEST | **Day:** Sunday (weekend mode — crypto-only)
**Previous review:** 2026-07-05 18:39 EEST (US open reaction review)
**Advisory only — no auto-trade. Weekend mode active. Stocks CLOSED (reopens Mon Jul 6 at 16:30 EEST).**

---

## 1. Executive Summary

**Slot:** late-session risk review (21:30 EEST). Sunday July 5 — weekend mode, crypto is the sole live class. Stocks closed; all stock signals are planning/carry-forward only.

**Regime:** Bullish trend (risk-on). BTC and ETH both in confirmed uptrend. Altcoin breadth 75-78% above EMA20. F&G=23 (extreme fear — divergence from bullish price action). Macro risk 35-45/100, driven by exploit/hack noise on ETH/SOL/APT (not regime-changing). Federal Reserve delivered positive crypto signals (CryptoBriefing, internal).

**Late-session status:** Cycle 8 completed 21:07 EEST (32 min ago). 50 crypto signals active, all B-tier longs. Signal stats improving: +2.5R since the 18:39 slot (76.65R total, PF 2.53, WR 23.5%). Paper monitor closed 380W/63L today.

**Key routing:** Swing is the best mode (PF 3.3, avgR 0.5). Intraday no-catalyst is structurally net-negative (14d: WR 23%/PF 0.70/−3R). Scalp is low-confidence (1W/7L, PF 0.14 over 14d per report). Shorts: failing systemically (0W/4L, −2.5R). **Do NOT chase extended names or initiate new longs in the final evening hours without retest confirmation.**

**Late-session routing:**
- **Hold:** BCH/USDT swing (entered ~234, hold above 234.04 invalidation, currently ~241)
- **Watch for Monday open:** ADA/USDT — RealFi Phase 1 Testnet **launches July 6 (CONFIRMED)**; sell-the-news risk documented
- **Avoid new entries tonight:** TLM (delisting block), HOT (extreme funding −1.05%/8h), any short
- **Best long-watch into Monday:** ADA/USDT pullback 0.64-0.66 + RTH confirmation
- **Best short-watch:** VANRY/USDT ONLY if 1h close below 0.0048 after structure failure — NOT now

Advisory only. No auto-trade. Scanning continues in all conditions.

---

## 2. Data Used

| Source | Mtime / Freshness | Status |
|---|---|---|
| scheduler.log | 2026-07-05 21:07 EEST | **FRESH** (32 min) |
| cycle_08_20-47_summary.md | 2026-07-05 21:07 EEST | **FRESH** (32 min) |
| scalp report `2026-07-05_17-53` | 2026-07-05 20:53 EEST | **FRESH** (46 min) |
| intraday report `2026-07-05_18-00` | 2026-07-05 21:00 EEST | **FRESH** (39 min) |
| swing report `2026-07-05_13-23` | 2026-07-05 16:23 EEST | **CARRY-FORWARD** (5.3h, 4-12h window) |
| stocks_intraday `2026-07-03_20-07` | 2026-07-03 23:07 EEST | **STALE** (>43h — holiday weekend) |
| stocks_swing `2026-07-02_13-03` | 2026-07-02 16:03 EEST | **STALE** (>74h) |
| stocks_invest `2026-07-02_13-05` | 2026-07-02 16:05 EEST | **STALE** (>74h) |
| catalyst_cycle_18-00.md | 2026-07-05 21:00 EEST | **FRESH** |
| catalyst_events.jsonl + narrative_baskets.jsonl | 2026-07-05 21:00 EEST | **FRESH** |
| llm_analysis_packet.md (crypto) | 2026-07-05 21:00 EEST | **FRESH** |
| active-signals CLI (crypto) | 2026-07-05 21:39 EEST | **LIVE (50 signals)** |
| signal-stats CLI (crypto) | 2026-07-05 21:39 EEST | **LIVE** |
| detect_untracked_legacy_alerts | 2026-07-05 21:39 EEST | **LIVE (20 untracked)** |
| Previous enriched review (18:39 EEST) | 2026-07-05 18:50 EEST | carry-forward (3h) |
| External: ADA RealFi | WebSearch 21:39 EEST | **CONFIRMED** (multiple sources) |
| External: BCH price | WebSearch 21:39 EEST | prediction sites only — using internal OHLCV |

**Notes:**
- Stocks CLOSED (Sunday + US holiday weekend; stale by design). Planning/carry-forward only.
- Weekend mode active: A-tier penalty, confidence step-down, overextension threshold 1.25x, require retest after impulse.
- Reddit: all 403 blocked. No live X/Telegram/KOL connectors.
- Onchain: `interface_ready_config_missing`.
- TradingView unavailable — OHLCV/ATR/EMA from reports only.
- OI numeric data sparse (MEXC fallback for most symbols).
- BCH current price confirmed ~241 via rwa_narrative basket headline (21:00); swing entry ~234 (triggered).

---

## 3. Scheduler / Data Freshness

- **Scheduler freshness:** cycle_08_20-47_summary.md at 21:07 EEST — **32 minutes ago, FRESH** (well within 3h threshold). scheduler.log mtime 21:07 EEST.
- **Deferral check:** Both indicators fresh — **NO DEFER.**
- **Cycle 8 result:** ok=27 / failed=0. All key steps completed: scalp, intraday, catalyst scan, paper execution, paper structural TP/stop, entry-mode, signal tracking, paper shadow A/B, LLM intelligence.
- **Paper monitor status (21:07 EEST, cycle 8):**
  - OPEN ACTIONABLE: **6**
  - WAITING FOR ENTRY: **4**
  - ENTERED UNRESOLVED: **43** (entry filled, no TP/SL before window — NOT missed entries)
  - REVIEW/SHADOW: **150**
  - NO-ENTRY / STALE / MOVED AWAY: **46**
  - CLOSED TODAY: **380W / 63L / 0flat**
  - NEEDS REVIEW: **0**
- **Untracked legacy alerts:** **20 today** (unchanged since cycle 8; last alert BCH intraday 18:00 UTC). All B-tier Telegram alerts without matching proposed_signal → excluded from PF/winrate.
- **Mode:** Sunday / weekend crypto-only. Stocks data paused by design.
- **Paper shadow A/B (forward-only, 10d window):** A −44.12R / B +7.71R (Δ+51.83R). Promotion gate: **NOT_READY** (4/6 criteria). Forward window 10d < 14d minimum; DATA_GAP_LATE 44% of forward signals. Evaluation only — no promotion.
- **Intelligence layer (21:05 UTC):**
  - Timeline: 153 symbols, 2010 events, last_event 17:46 UTC.
  - Derivatives cached: 124 symbols; squeeze_phase distribution:
    - phase_0_unknown: 47 | phase_1_build_up: 28 | **phase_2_squeeze_expansion: 3** | phase_3_distribution_near_high: 1 | **phase_4_unwind: 3** | **phase_5_post_unwind_chop: 42**
  - Onchain: config missing (no `config/onchain.yaml`).

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-05 21:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["social_attention", "onchain_config", "liquidation_heatmaps", "oi_numeric_history"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "cycle_08 summary 21:07 EEST (32 min ago)",
        "scalp 20:53 FRESH (46 min)",
        "intraday 21:00 FRESH (39 min)",
        "swing 16:23 CARRY-FORWARD (5.3h)",
        "catalyst 21:00 FRESH",
        "stocks stale >43h (holiday weekend — by design)",
        "20 untracked alerts today (integrity flag)"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": ["social_attention", "etf_flows", "onchain_whale_flows", "dxy_yields"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC uptrend, ETH uptrend",
        "breadth 75.68-78.38% above EMA20",
        "F&G=23 (extreme fear — divergence from bullish tape)",
        "BTC ATR percentile 1 (low vol)",
        "macro risk 35-45/100 (exploit noise, not regime-changing)",
        "crypto_mode=trend (dashboard snapshot 21:04)",
        "Fed positive signals for crypto (CryptoBriefing, internal)",
        "Weekend mode: WR 24% / PF 1.8 vs non-weekend WR 29% / PF 4.0"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.62,
      "reason_codes": ["fresh_catalyst", "mapping_weak", "narrative_supported"],
      "data_missing": ["catalyst_mapping_pct_exact"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "467 events today, 5 baskets",
        "~72% unmapped (estimate, consistent with prior-review 28.3% mapped)",
        "momentum_breakout basket fresh <1h: CS/TLM/BTW primary, HOT/VANRY related",
        "rwa_narrative fresh <6h: ONDO/XLM",
        "ai_narrative fresh <6h: NEAR/RENDER/TAO/FET",
        "perps_dex_narrative fresh <24h: HYPE (9% global perp market, $4B OI)",
        "ADA RealFi Phase 1 Testnet launches Jul 6 (CONFIRMED via WebSearch)",
        "ETH Lean Ethereum roadmap (0.65 importance, single_source)",
        "APT/ETH/SOL exploit blocks active (advisory)",
        "TLM delisting operator-review block active"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["oi_numeric_history", "liquidation_levels", "exchange_volume_full"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "HOT: funding -1.05%/8h, OI 24h +191.54%, crowding unknown — extreme squeeze risk",
        "VANRY: funding -0.13%, OI 24h +69.91%, crowding unknown — elevated",
        "BCH: funding -0.002%, OI +3.5%, L/S 1.843 — crowding normal",
        "TLM: funding -0.006%, OI +8.24%, L/S 0.876 — crowding normal",
        "BTW: funding +0.030%, OI +6.05%, L/S 1.074 — crowding normal",
        "CAP: funding +0.043%, OI +34.19%, L/S 0.932 — crowding normal",
        "TRUMP: funding +0.005%, L/S 1.526 — potential squeeze if price reclaims",
        "Squeeze phases: 3 in phase_2 (expansion), 42 in phase_5 (post-unwind chop)"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest", "overextended"],
      "data_missing": ["tradingview_chart", "exact_current_prices", "spread_data"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BCH: entered at swing level ~234, currently ~241 per basket headline — in profit, hold vs inv 234.04",
        "VANRY: price ~0.0053 vs entry zone 0.0050-0.0052 — slightly extended, pullback needed",
        "HOT: 24h +15.94%, extreme funding — late entry/chase risk, TP already hit",
        "TLM: 7d +266.59%, 24h +22.59% — extreme overextension + delisting block",
        "CS: 24h +48.77%, vol 33.9x — tagged overextended in reports",
        "VANRY ATR 0.0005 (scalp report), BCH score 81.4 (swing report)"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry", "review_shadow"],
      "data_missing": ["per-signal_exact_entry_price"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE: 6",
        "WAITING FOR ENTRY: 4",
        "ENTERED UNRESOLVED: 43 (entry filled, no TP/SL before window — NOT missed entries)",
        "REVIEW/SHADOW: 150",
        "NO-ENTRY / STALE / MOVED AWAY: 46",
        "CLOSED TODAY: 380W / 63L / 0flat",
        "NEEDS REVIEW: 0",
        "BCH swing: TRIGGERED (entry ~234 filled)",
        "VANRY swing: WAITING FOR ENTRY",
        "20 untracked legacy alerts — excluded from tracking"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["correlation_cluster", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["daily_pnl_exact", "account_exposure_pct"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "All 50 active signals are long crypto — correlated directional exposure",
        "Shorts systemically failing: 0W/4L, -2.5R",
        "TLM delisting block active — do not initiate new",
        "APT/ETH/SOL exploit blocks (advisory) — operator-review required for new A/B",
        "HOT extreme funding (-1.05%/8h) — squeeze unwind risk",
        "Weekend mode: WR 24% / PF 1.8 — step-down active",
        "Intraday no-catalyst: 14d −3R structural loss playbook",
        "Late-session: avoid new entries on overextended names"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["per-cycle_breakdown", "latest_scalp_closed_count"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Swing: n=83, triggered=80, WR 37.5%, PF 2.5, avgR 0.4, +31.6R — WORKING",
        "Intraday: n=117, triggered=104, WR 4.8%, PF 1.2, avgR 0.03, +2.71R — WEAK",
        "Scalp: n=110, triggered=106, but low-confidence overlay (1W/7L/14d per report)",
        "Weekend=Y: WR 23.6% / PF 1.83 / avgR 0.17 vs Weekend=N: WR 23.2% / PF 4.02 / avgR 0.39",
        "Shorts: 0W/4L, -2.5R — failing",
        "Signal-stats live: totalR +76.65R (was +74.17R at 18:39 — +2.5R in 3h)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "All eight agents synthesised",
        "Risk-on regime confirmed; weekend PF penalty active",
        "BCH swing entered, in profit — hold vs inv",
        "ADA RealFi Testnet Jul 6 confirmed — best overnight catalyst-watch",
        "HOT/TLM: avoid (extreme conditions)",
        "VANRY: watch for pullback — do not chase",
        "No A-tier signals; B-tier all longs; swing best mode",
        "Scanning continues regardless of late-session caution"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.78,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "BCH/USDT",
      "trigger": "HOLD above 234.04 invalidation — already entered. No new entry at ~241 without retest of 234-236 zone.",
      "reason": "Swing B triggered, score 75+, momentum 5.1% RS vs BTC, normal crowding, lowest late-session risk of active setups"
    },
    "best_short_candidate": {
      "symbol": "VANRY/USDT",
      "trigger": "ONLY if 1h candle closes below 0.0048 (post-impulse support break); NOT a current recommendation",
      "reason": "Extreme negative funding, OI expansion, 7d +75% impulse — if support fails this becomes a squeeze unwind short"
    },
    "best_catalyst_candidate": {
      "symbol": "ADA/USDT",
      "trigger": "RealFi Phase 1 Testnet launches Monday Jul 6 — wait for RTH open + first 15-30 min confirmation; entry zone 0.64-0.66 on pullback",
      "reason": "CONFIRMED via multiple external sources; largest Cardano upgrade cycle; sell-the-news risk also documented — wait for direction"
    },
    "avoid_candidate": {
      "symbol": "TLM/USDT",
      "reason": "Delisting block active (operator-review), 7d +266%, extreme overextension, Binance delisting monitoring"
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
| data_quality | **ok** | 0.88 | scheduler_fresh, report_stale | advisory_only |
| market_regime | **ok** | 0.82 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | **caution** | 0.62 | fresh_catalyst, mapping_weak, narrative_supported | advisory_only |
| derivatives_squeeze | **caution** | 0.68 | squeeze_risk (HOT), oi_supports, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.72 | entry_late, chase_risk, clean_retest (BCH), overextended | advisory_only |
| execution_lifecycle | **ok** | 0.85 | open_actionable(6), waiting(4), entered_unresolved(43), no_entry(46) | advisory_only |
| risk_manager | **caution** | 0.80 | correlation_cluster, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | **ok** | 0.82 | playbook_working(swing), playbook_failing(scalp-low-conf), low_sample | advisory_only |
| **head_trader** | **normal** | **0.78** | risk_on, longs_preferred, wait_for_trigger | advisory_only |

---

## 4. What Changed vs Previous Review (18:39 EEST)

| Item | 18:39 EEST | 21:39 EEST | Change |
|---|---|---|---|
| Scheduler cycle | cycle_06 (16:25) | cycle_08 (21:07) | **+2 new cycles** |
| Scalp report | 15:32 UTC | 17:53 UTC | **Refreshed** |
| Intraday report | 15:38 UTC | 18:00 UTC | **Refreshed** |
| Swing report age | 2.3h (fresh) | 5.3h (carry-forward) | Now carry-forward |
| Active signals | ~50 (estimate) | **50 live** | Stable |
| Signal total R | +74.17R | **+76.65R** | **+2.5R improvement** |
| Signal WR | 22.8% | **23.5%** | +0.7pp |
| Signal PF | 2.48 | **2.53** | +0.05 |
| Paper closed W/L | ~379W/58L | **380W/63L** | +1W / +5L |
| Entered unresolved | ~35 (est) | **43** | +8 |
| Untracked alerts | 17 | **20** | +3 (BCH intraday 18:00, VANRY scalp 17:53, HOT scalp 17:53) |
| BCH swing | HOLD (entered) | **HOLD (in profit ~241 vs inv 234.04)** | Stable |
| VANRY swing | WAITING | **WAITING** | Not triggered |
| ADA RealFi | Carry-forward | **CONFIRMED (Jul 6) via WebSearch** | Upgraded |
| Catalyst baskets | 4 (scalp report) | **5 (rwa_narrative added)** | New basket |

**Thesis changes:** BCH unchanged (hold). VANRY unchanged (wait for pullback). ADA **UPGRADED** — testnet launch externally verified. TLM remains AVOID. HOT extreme funding confirmed.

---

## 5. Catalyst Coverage

**Today (catalyst_cycle_18-00, 21:00 EEST — fresh):**
- Total events: **467**
- Narrative baskets: **5** (rwa_narrative, binance_ecosystem_teaser, perps_dex_narrative, ai_narrative, momentum_breakout)
- Estimated mapped (non-null symbol): **~130 / 467 (~28%)** — consistent with prior reviews
- Estimated unmapped: **~337 / 467 (~72%)**

> ⚠️ **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** ~72% of events are basket-level without symbol attribution. External research required before acting on any catalyst-dependent signal.

**Top 3 unmapped events:**
1. `[legal_risk]` Bronstein, Gewirtz & Grossman: Genius Group class action (PR Newswire Stocks)
2. `[regulatory_sector_headline]` Federal Reserve delivers positive signals for crypto investors (CryptoBriefing)
3. `[exploit_hack]` Hinkal protocol smart contract flaw — $820K USDC exploit (AMBCrypto)

**Notable mapped catalysts:**
- **UNH/USDT** [legal_risk, 0.73]: DOJ probe, shares −16% — stocks CLOSED; carry-forward
- **AVAX/USDT** [partnership, 0.66]: FIFA World Cup / Kraken crypto partnership
- **ETH/USDT** [roadmap_event, 0.65]: Vitalik "Lean Ethereum" roadmap, quantum resistance by 2029
- **APT/USDT** [exploit_hack]: critical vulnerability fixed — operator-review block active
- **BTC/USDT**: options market pricing in low future volatility / optimism returning (Glassnode)
- **TLM/USDT** [delisting]: Binance delisting monitoring — operator-review block active

**Active narrative baskets:**
- **momentum_breakout** (fresh <1h): CS/TLM/BTW (primary); HOT/VANRY (related)
- **ai_narrative** (fresh <6h): NEAR/RENDER/TAO/FET
- **perps_dex_narrative** (fresh <24h): HYPE primary ($4B OI, 9% global perp market)
- **rwa_narrative** (fresh <6h): ONDO/XLM
- **binance_ecosystem_teaser** (fresh <24h): BNB/ASTER

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-on (BTC+ETH uptrend, breadth 75-78% above EMA20, low ATR percentile)
- **Stocks mood:** closed (Sunday + US holiday weekend)
- **Dominant narrative:** momentum-breakout alts (CS/TLM/BTW/HOT/VANRY); AI rotation (TAO/NEAR/FET); BTC low-vol optimism
- **F&G divergence:** 23 (extreme fear) vs bullish price action — late-cycle divergence; do not fade momentum but stay disciplined on exits
- **Preferred side now:** longs on pullbacks / RS-leaders with catalyst; no chasing extended names; no shorts
- **Best long candidate:** BCH/USDT — ENTERED, hold above 234.04 invalidation
- **Best short candidate:** VANRY/USDT — ONLY if 1h close below 0.0048 (NOT now)
- **Best catalyst-backed candidate:** ADA/USDT — RealFi Testnet Monday Jul 6 (confirmed)
- **What to avoid:** TLM (delisting), HOT (extreme funding), CS (overextended/no futures), shorts (0W/4L)
- **What would change the view:** BTC 1h close below key support → breadth drops below 65% EMA20 → reduce long exposure

**BTC/ETH context:** Low volatility (ATR pct = 1), options pricing in low future vol (Glassnode). Large BTC transfers from Kraken (1,037 + 1,624 BTC to unknown wallets) — monitoring; inconclusive. ETH/BTC = 0.028422 (ETH slight underperformance vs BTC).

**Weekend mode:** WR 24% / PF 1.83 vs non-weekend 29% / 4.02 — **confidence step-down active for all late-session signal generation.**

---

## 7. Candidate Deep Dives

### Candidate 1: BCH/USDT — Swing B (ENTERED — Hold Decision)

**Signal:** Swing B, score 75.x, direction LONG, **status: TRIGGERED** (entry filled ~234)
**Current price:** ~241 (per rwa_narrative basket headline 21:00 EEST: "BITCOINCASH 241.33 +3.82%")
**Invalidation:** 1h/4h close below **234.04**
**Momentum:** 24h +5.37%, RS vs BTC +5.13%, volume 1.31x (swing report)

**Entry situation:** Entry was triggered earlier today. This is a **HOLD vs EXIT** decision, not a new entry.

**Catalyst check (internal first):** No specific BCH catalyst in catalyst_events.jsonl. BCH appears in rwa_narrative basket as a price ticker — not a catalyst. Untracked legacy scalp alerts from 08:27, 10:45, 13:06 UTC confirm multi-cycle momentum interest. External web search returned only prediction-model pages for BCH price; internal OHLCV data is authoritative (~241 area).

**Derivatives:** Funding −0.002% (neutral), OI +3.49% 24h, long/short 1.843 (longs slightly dominant, within normal range), crowding normal. No squeeze risk.

**Late-session assessment:**
- Price ~241 vs entry ~234 = +3% in profit, 7 points of buffer above invalidation 234.04.
- No new entry needed or appropriate at current price.
- Overnight risk: low-medium. BCH is a liquid large-cap; no hack events, normal funding.
- **Verdict: OPEN ACTIONABLE — HOLD. Hold above 234.04 invalidation. No new entry at 241 without retest of 234-236 zone first.**

**No LEGAL/HEADLINE RISK identified for BCH.**

---

### Candidate 2: VANRY/USDT — Swing WAITING / Scalp+Intraday TP HIT

**Signal:** Swing B score 69.x, **status: WAITING FOR ENTRY** (entry zone 0.0050-0.0052)
**Current price:** ~0.0053 (above entry zone — slightly extended per ATR of 0.0005)
**Invalidation:** 1h close below 0.0047
**Targets (swing):** TP1 0.0058, TP2 0.0063, TP3 0.0068

**Context:** VANRY has been the strongest alt today (7d +74-75%, 24h +12-13%). Multiple scalp and intraday signals already hit TP earlier in the session. Swing remains WAITING because price is above the preferred entry zone.

**Catalyst check (internal):** No verified catalyst. In momentum_breakout basket (fresh <1h, related symbol). 5 untracked legacy alerts throughout the day (scalp 08:27, 10:45, 15:32, 17:53; swing 13:34).

**Derivatives:** Funding −0.13% (MEXC) / −0.032% (Bybit) — elevated negative funding. OI 24h +69.91% — significant expansion. Crowding: unknown (numeric sparse). This pattern (price up + OI up + negative funding) can indicate shorts already paid out or longs crowding.

**Chase risk:**
- Price 0.0053 vs entry zone 0.0050-0.0052: 1.9-5.7% above → moderate chase risk.
- Post-impulse: 7d +75% — needs consolidation or pullback for clean risk/reward.
- Late-session Sunday: NOT the right window to initiate above entry zone.

**Late-session decision:**
- Actionable NOW? **NO** — price above entry zone, elevated funding, late-session.
- Actionable condition: Pullback to 0.0050-0.0052 during Asian session + hold for 1-2 candles.
- Short watch: ONLY if 1h close below 0.0048. Not recommended proactively.
- **Verdict: WAITING FOR ENTRY — do NOT chase tonight. Wait for pullback confirmation.**

---

### Candidate 3: HOT/USDT — Scalp+Intraday TP HIT / Squeeze Warning

**Signal:** Scalp B score 70.3 (TP HIT), Intraday B score 69.9 (TP HIT)
**Status:** Signals **CLOSED / TP HIT** — assessing for new-entry risk only

**Catalyst check:** No verified catalyst. In momentum_breakout basket (related symbol). Untracked legacy alerts: scalp B 68.0 at 15:32, 70.3 at 17:53 UTC.

**Derivatives — EXTREME SQUEEZE WARNING:**
- Funding: **−1.05%/8h** (−0.010554 MEXC fallback) — extreme negative funding
- OI 24h: **+191.54%** — massive open interest expansion in one day
- Crowding: unknown (numeric history sparse)

**Assessment:** Extreme funding at −1.05%/8h on a momentum name with no catalyst is a classic pre-unwind setup. Price has already moved +15.94% 24h / +20.45% 7d. Signals have TP'd. This is the highest squeeze risk symbol in the universe tonight.

**Late-session decision:**
- New entry feasible? **NO.** Carry cost prohibitive, late-session Sunday, no catalyst.
- If funding normalizes to < −0.02% and price consolidates → reassess next cycle.
- **Verdict: TP HIT (CLOSED). AVOID new entry — extreme funding squeeze risk.**

---

### Candidate 4: ADA/USDT — Catalyst Watch (RealFi Testnet Monday Jul 6)

**Signal:** Swing B (TP HIT), Intraday B (TP HIT) — no active open position.
**Catalyst:** RealFi Phase 1 Testnet launches **Monday July 6, 2026 — CONFIRMED**

**External research (WebSearch 21:39 EEST):**
- [Cardano Price Rises 5% As RealFi Testnet Launch Drives Optimism](https://dmarketforces.com/cardano-price-rises-5-as-realfi-testnet-launch-drives-optimism/) — date unavailable (Jul 2026) — confirms launch + price reaction
- [Hoskinson: Largest Upgrade in Cardano History Imminent](https://thecryptobasic.com/2026/07/02/hoskinson-says-largest-upgrade-in-cardano-history-is-imminent-confirms-ada-fundamentals-remain-strong/) — 2026-07-02 — IOG requests 120M ADA from treasury
- [ADA RealFi Testnet Puts ADA Back in Focus](https://www.openpr.com/news/4568739/cardano-news-realfi-testnet-puts-ada-back-in-focus-as-alphapepe) — date unavailable (Jul 2026)
- [ADA Price Falls Despite Major Ecosystem Updates (KuCoin)](https://www.kucoin.com/news/flash/cardano-launches-leios-testnet-ada-price-falls-despite-major-ecosystem-updates) — **SELL-THE-NEWS RISK documented** — prior Leios testnet launch caused price to fall

**Verification status:** `confirmed` (multiple independent sources).

**Sell-the-news precedent:** ADA has a documented pattern of failing to rally on major ecosystem updates (Leios testnet: price fell). RealFi launch is real — the price reaction is uncertain. Do NOT position Sunday night based on Monday's event.

**Monday action plan:**
- Do NOT front-run overnight.
- Wait for Jul 6 RTH/crypto market open; first 15-30 min to confirm direction.
- If ADA gaps up and immediately reverses → sell-the-news, do NOT chase.
- If ADA shows RTH consolidation or breakout structure → new B-tier signal likely.
- Entry zone: 0.64-0.66 on pullback (from prior review carry-forward).
- **Verdict: CATALYST WATCH — best overnight planning candidate. Monitor for Monday signal.**

---

### Candidate 5: HYPE/USDT — Fresh Basket / Perps DEX Narrative

**Signal:** No active B-tier signal. C-tier watchlist candidate.
**Basket:** perps_dex_narrative (fresh <24h); also delisting_thin_liquidity (cautionary)
**Catalyst:** Hyperliquid captures 9% of global perpetual futures market, $4B OI (internal, catalyst_cycle_18-00)

**Basket conflict:**
- perps_dex_narrative → `wait_pullback` (positive)
- delisting_thin_liquidity → `avoid_low_liquidity` (cautionary)

**Decision:** Conflicting baskets. The thin liquidity flag overrides the positive narrative for intraday action. The perps DEX thesis (9% global market, $4B OI) is a legitimate multi-week research narrative. Wait for a clean B-tier signal before acting.

**Verdict: WATCHLIST / RESEARCH ONLY — basket conflict. No entry without B-tier signal.**

---

## 8. Best Candidates Ranked

**Assessment window:** Late-session Sunday 21:30-23:15 EEST; overnight into Monday Asian session.

| Rank | Symbol | Mode | Status | Verdict | Action |
|---|---|---|---|---|---|
| 1 | BCH/USDT | swing | ENTERED (triggered) | **HOLD** | Hold above 234.04 invalidation |
| 2 | ADA/USDT | catalyst watch | TP HIT (swing/intraday) | **CATALYST WATCH** | Best Monday planning; RealFi Jul 6 confirmed |
| 3 | VANRY/USDT | swing | WAITING FOR ENTRY | **WAIT** | Pullback 0.0050-0.0052 only; no chase |
| 4 | HYPE/USDT | watchlist | C-tier / basket conflict | **RESEARCH** | Perps DEX thesis; wait for B signal |
| 5 | HOT/USDT | — | TP HIT (closed) | **AVOID NEW** | Extreme funding; do not re-enter |

**If no position held tonight:**
- **Best long-watch:** ADA/USDT — Monday Jul 6 open + RealFi confirmation; entry zone 0.64-0.66 on pullback.
- **Best short-watch:** VANRY/USDT — ONLY after 1h close below 0.0048. Trigger: structure failure. NOT now.
- **Best catalyst-watch:** ADA/USDT (confirmed Jul 6) + HYPE (perps DEX $4B OI thesis, next cycle signal).
- **Avoid tonight:** TLM (delisting), HOT (extreme squeeze), CS (overextended), shorts (0W/4L), intraday no-catalyst longs.

---

## 9. Avoid / No Trade

**This section applies to the current late-session window only. Scanning and tracking continue without interruption.**

| Symbol | Reason | Strength |
|---|---|---|
| TLM/USDT | Delisting block active; 7d +267% extreme extension; operator-review required | **STRONG AVOID** |
| HOT/USDT | Extreme funding −1.05%/8h, OI +191%; late-session unwind risk | AVOID new entry |
| CS/USDT | 24h +48.77%, vol 33.9x, no futures data, tagged overextended | AVOID new entry |
| ETH/USDT (new signal) | Operator-review block: UXLINK hacker ETH transfers (advisory) | AVOID new A/B |
| APT/USDT (new signal) | Exploit block: Aptos vulnerability (advisory) | AVOID new A/B |
| SOL/USDT (new signal) | Exploit block: Step Finance exploiter $21M SOL sold (advisory) | AVOID new A/B |
| Any SHORT | 0W/4L, −2.5R. Systemically failing in risk-on tape | DO NOT SHORT |
| Intraday no-catalyst | 14d: WR 23% / PF 0.70 / −3R. Structural loss. Require RS-leader or breakout. | CAUTION |

---

## 10. Main Risks

1. **HOT/USDT squeeze unwind:** Funding −1.05%/8h + OI +191% — forced liquidation cascade risk in adjacent momentum names (VANRY, BTW).
2. **Weekend mode underperformance:** PF 1.83 vs 4.02 non-weekend — structural headwind for any new signal generated Sunday evening.
3. **Catalyst mapping weak (~72% unmapped):** Large fraction of market events unattributed. Missed negative catalysts are the primary blind spot.
4. **BTC whale transfers:** 1,037 + 1,624 BTC out of Kraken to unknown wallets — inconclusive but monitoring-worthy.
5. **ADA sell-the-news risk (Monday):** Prior ADA testnet launches have caused price to fall. Wait for RTH direction confirmation before acting.
6. **Correlation cluster:** All 50 active signals are long crypto — one BTC/ETH breakdown hits the full portfolio simultaneously.
7. **F&G divergence:** Extreme fear (23) while price is bullish — marks either end-of-correction (bullish) or distribution (bearish). Higher uncertainty on sustainability.
8. **Onchain blind spot:** No onchain config — whale flows, exchange netflows, stablecoin inflows all missing.
9. **Exploit noise (ETH/SOL/APT):** Not regime-changing individually but operator-review blocks are advisory for new signal consideration.
10. **VANRY impulse reversal:** If +75% 7d impulse reverses, negative funding accelerates the move down.

---

## 11. Action Plan — Next 4 Hours (21:39–01:30 EEST)

| Priority | Action | Detail |
|---|---|---|
| 1 | Monitor BCH/USDT | HOLD above 234.04. If BCH drops toward 236-238, heighten attention. Do NOT exit above invalidation. |
| 2 | Watch ADA/USDT (overnight) | Monday Jul 6 RealFi Testnet — monitor Asian session reaction. Entry ONLY after RTH open + first 30 min confirmation. |
| 3 | Watch VANRY/USDT | If price dips to 0.0050-0.0052 during Asian session and holds, swing entry re-evaluates. |
| 4 | Monitor HOT/USDT funding | If funding normalizes from −1.05% to < −0.02%, reassess for potential scalp reset. Do not act tonight. |
| 5 | Avoid all shorts | No short entries in risk-on weekend tape (0W/4L precedent). |
| 6 | Allow scanner to run | Cycle 9 expected ~23:00-23:30 EEST. New signals will be generated. Do not pre-empt. |
| 7 | Do NOT enter | TLM, HOT (new), CS, EPIC short, intraday no-catalyst setups |

---

## 12. Final Verdict per Mode

| Mode | Verdict | Confidence | Key condition |
|---|---|---|---|
| Crypto Swing | **HOLD existing / Watch new** | High | BCH entered-hold. ADA catalyst-watch Mon. VANRY wait-for-pullback. No new swing entries tonight without retest. |
| Crypto Intraday | **CAUTION** | Medium | No-catalyst intraday −3R/14d. Require RS-leader + breakout confirmation. Late session: avoid new entries. |
| Crypto Scalp | **LOW CONFIDENCE** | Low | 1W/7L over 14d (PF 0.14). Weekend mode penalty. Research/low-size only. |
| Stocks (all modes) | **CLOSED / Planning** | N/A | US markets closed Sunday. First actionable: Monday Jul 6 RTH (~16:30 EEST). |
| Shorts (any mode) | **AVOID** | Strong | 0W/4L, −2.5R. Not working in current tape. |

---

## 13. Sources

**Internal:**
- `data/scheduled_runs/2026-07-05_default_schedule/cycle_08_20-47_summary.md` — 2026-07-05 21:07 EEST
- `data/reports/scalp/2026-07-05_17-53_scalp_report.md` — 2026-07-05 20:53 EEST
- `data/reports/intraday/2026-07-05_18-00_intraday_report.md` — 2026-07-05 21:00 EEST
- `data/reports/swing/2026-07-05_13-23_swing_report.md` — 2026-07-05 16:23 EEST (carry-forward)
- `data/catalysts/2026-07-05/catalyst_cycle_18-00.md` — 2026-07-05 21:00 EEST
- `python -m src.cli active-signals --asset-class crypto` — 2026-07-05 21:39 EEST
- `python -m src.cli signal-stats --asset-class crypto` — 2026-07-05 21:39 EEST
- `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-05` — 2026-07-05 21:39 EEST
- `OPUS_ENRICHED_REVIEW_AUTO_2026-07-05_1839.md` — prior review 2026-07-05 18:39 EEST

**External (WebSearch 2026-07-05 21:39 EEST):**
- [Cardano Price Rises 5% As RealFi Testnet Launch Drives Optimism](https://dmarketforces.com/cardano-price-rises-5-as-realfi-testnet-launch-drives-optimism/) — date unavailable (Jul 2026); verification: single_source; confirms: ADA catalyst
- [Hoskinson Says Largest Upgrade in Cardano History Is Imminent](https://thecryptobasic.com/2026/07/02/hoskinson-says-largest-upgrade-in-cardano-history-is-imminent-confirms-ada-fundamentals-remain-strong/) — 2026-07-02; verification: single_source; confirms: RealFi launch, 120M ADA treasury request
- [Cardano News: RealFi Testnet Puts ADA Back in Focus](https://www.openpr.com/news/4568739/cardano-news-realfi-testnet-puts-ada-back-in-focus-as-alphapepe) — date unavailable (Jul 2026); verification: single_source; confirms: catalyst
- [Cardano Launches Leios Testnet, ADA Price Falls Despite Major Ecosystem Updates | KuCoin](https://www.kucoin.com/news/flash/cardano-launches-leios-testnet-ada-price-falls-despite-major-ecosystem-updates) — Jul 2026; verification: single_source; warns: sell-the-news risk
- [Why is Cardano (ADA) Up 15% in a Week? — CryptoNews](https://cryptonews.net/news/analytics/33099355/) — Jul 2026; verification: single_source; context

**Internal news items (news_items table, Telegram channels):**
- t.me/glassnode: BTC options low vol — 2026-07-05; single_source
- t.me/whale_alert_io: 1,037 BTC + 1,624 BTC from Kraken — 2026-07-05; single_source
- catalyst_cycle_18-00 internal: Hyperliquid 9% global perp market, $4B OI — 2026-07-05; single_source

---

## 14. Fix Requests / TODO

### TODO-untracked-alerts-growth
- **issue:** 20 untracked legacy crypto alerts today (08:27 → 18:00 UTC) — multiple B-tier Telegram alerts sent without corresponding `proposed_signal`. Repeating symbols: ETHFI (×4), ADA (×3), BCH (×4), VANRY (×5), HOT (×2).
- **evidence:** `detect_untracked_legacy_alerts --since 2026-07-05` output: 20 rows, all NO (no proposed_signal). Grew 8 → 17 → 20 across three review slots today.
- **suggested manual fix:** Investigate watchlist alert routing path — why B-tier Telegram alerts fire without creating a matching `proposed_signal` row. Untracked alerts cannot be backtested and inflate the untracked count metric, degrading winrate coverage.
- **priority:** medium
- **first observed:** 2026-07-05 11:39 EEST (8 alerts); now 20 by 21:39 EEST

### TODO-catalyst-mapping-weak
- **issue:** Catalyst mapping consistently ~28% attributed (symbol non-null). ~72% of events remain basket-level, unable to contribute to per-symbol catalyst scores. Unmapped > 50% warning fires every review this cycle.
- **evidence:** catalyst_cycle_18-00: 467 events, 5 baskets; 28.3% mapped per prior reviews. Warning triggered at 11:39, 16:20, 18:39, and 21:39 EEST today.
- **suggested manual fix:** Audit symbol_resolver in catalyst layer (`src/catalysts/`). Add keyword/regex rules for common unmapped headline patterns. Target: >50% mapped to suppress the warning.
- **priority:** medium
- **first observed:** recurring across multiple review days
