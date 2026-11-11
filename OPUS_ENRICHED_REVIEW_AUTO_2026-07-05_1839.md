# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

**Slot:** US open reaction review (Sunday — US markets CLOSED; crypto-only) | **Time:** 2026-07-05 18:39 EEST
**Previous review:** 2026-07-05 16:20 EEST (pre-US-open decision review)
**Advisory only — no auto-trade. Weekend mode active (Sunday). Stocks CLOSED (reopens Mon Jul 6).**

> **NOTE ON TIMING:** Today is Sunday, July 5, 2026. The 18:30 EEST "US open reaction" slot fires but US markets are CLOSED on Sunday. This is a **Sunday afternoon crypto continuation review**. The first post-July-4 US session is Monday July 6. All stock signals are planning/carry-forward only; **crypto is the live actionable class**.

> **External web research NOT performed this slot** — internal catalyst data is fresh (18:38 EEST), prior review's external research within 4h validity window. Declared per §N source-discipline checklist.

---

## 1. Executive Summary

**Slot:** US open reaction review — Sunday (crypto-only). Advisory only, no auto-trade. Weekend mode active.

**Regime:** Bullish trend (risk-on). BTC and ETH both in confirmed uptrend. Altcoin breadth 78.9% above EMA20. Low volatility (BTC ATR percentile = 3). Macro risk 45/100 from 2 exploit/hack risk-off hits — hack noise on ETH/SOL/APT persists but is not a regime-changer.

**What changed since 16:20:** New scalp and intraday cycle completed at 18:32/18:38 EEST (both FRESH). Untracked legacy alerts grew 10 → 17 (+7: VANRY/HOT/ETHFI scalp 15:32). VANRY 24h return compressed: +50% at swing snapshot → +13% intraday → yesterday's impulse rolling off. Momentum_breakout basket (fresh <1h): TLM/VANRY/HMSTR. SYN appeared as new intraday B #2 (volume 1.48x).

**Market routing:** LONGS preferred in risk-on tape. Swing is the best mode (PF=3.9). Intraday no-catalyst documented net-negative (-3R/14d) — require RS-leader or breakout confirmation. Shorts: failing systemically (0W/4L, -2.5R). Do NOT chase shorts.

**Best long:** BCH/USDT swing B — already entered, hold above 234.04 invalidation.
**Best long-watch:** ADA/USDT — RealFi Testnet catalyst Monday Jul 6; wait for pullback 0.64-0.66.
**Best short-watch:** VANRY/USDT — ONLY if 1h close below ~0.0048 after post-impulse support fails; NOT now.
**Best catalyst-watch:** ADA (Monday Jul 6) + HYPE (perps DEX basket fresh <6h).
**Avoid:** TLM (delisting block), HOT (extreme squeeze: funding -1.1%/8h, OI +172%), ETH/SOL/APT (exploit blocks), intraday no-catalyst, any short.

---

## 2. Data Used

| Source | Mtime / Freshness | Status |
|---|---|---|
| scheduler.log | 28 May 2026 | stale file (cycle summaries confirm scheduler active) |
| cycle_06_15-59_summary.md | 16:25 EEST today (2.2h ago) | **FRESH** |
| scalp report `2026-07-05_15-32` UTC | 18:32 EEST (7 min ago) | **FRESH** |
| intraday report `2026-07-05_15-38` UTC | 18:38 EEST (now) | **FRESH** |
| swing report `2026-07-05_13-23` UTC | 16:23 EEST (2.3h ago) | **FRESH** (<4h) |
| stocks_intraday `2026-07-03_20-07` | 07/03 23:07 EEST | **STALE** (>43h — holiday weekend) |
| stocks_swing `2026-07-02_13-03` | 07/02 16:03 EEST | **STALE** (>74h) |
| stocks_invest `2026-07-02_13-05` | 07/02 16:05 EEST | **STALE** (>74h) |
| catalyst_cycle_15-38.md | 18:38 EEST | **FRESH** |
| catalyst_events.jsonl + narrative_baskets.jsonl | 18:38 EEST | **FRESH** |
| llm_analysis_packet.md (intraday) | 18:38 EEST | **FRESH** |
| active-signals CLI (crypto) | live 18:39 EEST | **LIVE (50 signals)** |
| signal-stats CLI (crypto) | live 18:39 EEST | **LIVE** |
| detect_untracked_legacy_alerts | live 18:39 EEST | **LIVE (17 untracked)** |
| Previous enriched review (16:20 EEST) | 16:20 EEST (2.3h ago) | carry-forward |

**Notes:**
- Stocks CLOSED (Sunday + US holiday weekend; stale by design). Planning/carry-forward only.
- Weekend mode active: A-tier penalty, confidence step-down, require retest after impulse, MEXC-only capped C.
- OI via MEXC fallback for most symbols (Bybit OI numeric history sparse).
- Social: Reddit all 403; no live X/Telegram/KOL connectors.
- Onchain: `interface_ready_config_missing`.
- TradingView unavailable — OHLCV/ATR/EMA from reports only.
- External web research NOT performed this slot (declared).

---

## 3. Scheduler / Data Freshness

- **Scheduler.log mtime:** 28 May 2026 — old log file. NOT the freshness indicator for cycles.
- **Latest cycle summary:** `cycle_06_15-59_summary.md` at 16:25 EEST (2.2h ago) — within 3h threshold.
- **Deferral check:** scheduler.log IS stale, but cycle summary is FRESH → NOT BOTH >3h → **NO DEFER.**
- **Fresh reports at 18:32/18:38:** confirms cycle 7 completed or is in progress.
- **Mode:** Sunday / weekend crypto-only. Stocks data paused.
- **Paper monitor status (carry-forward from 16:25 EEST — 2.2h ago):**
  - OPEN ACTIONABLE: ~7
  - WAITING FOR ENTRY: ~2
  - ENTERED UNRESOLVED: ~35 (entry filled, no TP/SL before window — NOT missed entries)
  - REVIEW/SHADOW: ~160
  - NO-ENTRY / STALE / MOVED AWAY: ~38
  - CLOSED (cumulative): ~379W / ~58L / 0flat
  - NEEDS REVIEW: 0
- **Untracked legacy alerts:** 17 today (grew from 10 at 16:20, from 8 at 11:39). New 7: VANRY scalp 15:32, HOT scalp 15:32, ETHFI scalp 15:32, VANRY swing 13:34, SENT swing 13:42, ADA swing 13:55, ETHFI swing 14:04. All Telegram without `proposed_signal` — excluded from PF/winrate tracking.
- **Weekend mode adjustments active:** A-tier penalty, confidence step-down, overextension 1.25x, require retest.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-05 18:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["social_attention", "onchain_config", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_06 summary 16:25 EEST (2.2h)", "scalp 18:32 FRESH", "intraday 18:38 FRESH", "swing 16:23 (2.3h fresh)", "catalyst 18:38 FRESH", "stocks stale >43h (holiday weekend)", "17 untracked alerts today"]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": ["social_attention", "etf_flows", "onchain_whale_flows", "dxy_yields"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC uptrend", "ETH uptrend", "breadth 78.9% above EMA20/EMA50", "BTC ATR percentile 3 (low vol)", "macro risk 45/100 (2 exploit risk-off hits)", "Fed positive signals for crypto"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.62,
      "reason_codes": ["fresh_catalyst", "mapping_weak", "narrative_supported"],
      "data_missing": ["catalyst_mapping_pct_current"],
      "suggested_effect": "advisory_only",
      "facts_used": ["640 events today", "momentum_breakout basket fresh <1h (TLM/VANRY/HMSTR)", "perps_dex_narrative fresh <6h (HYPE)", "ai_narrative fresh <6h (NEAR/RENDER/TAO/FET)", "prior review: 28.3% mapped (weak)", "ADA RealFi Testnet Monday carry-forward", "ETH Lean Ethereum roadmap (0.65-0.67 importance)", "Fed positive signals (0.66)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["squeeze_risk", "post_unwind_chop", "oi_supports"],
      "data_missing": ["liquidation_heatmaps", "order_book_depth", "OI_numeric_history_bybit"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOT funding -0.01113/8h + OI +172% swing (crowding unknown) = extreme squeeze_risk", "VANRY OI +242% swing (now normalizing, -0.000238 funding)", "BCH OI +3.49% funding near-zero = clean oi_supports", "TLM funding -0.000208 OI stable = fresh positioning", "MEXC fallback for most OI reads"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.73,
      "reason_codes": ["clean_retest", "chase_risk", "stale_before_entry"],
      "data_missing": ["tradingview_chart", "orderbook_depth", "cvd"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BCH current ~237-238, entry zone 236-238 = within zone (clean)", "VANRY current 0.0053-0.0054, intraday zone 0.0051-0.0053 = at edge", "SYN current 0.4295, entry zone 0.41-0.42 = slightly above (retest needed)", "TLM current 0.0032, entry 0.0030-0.0031 = above zone (post-impulse)", "HMSTR ATR ~0 = precision entry unreliable", "Weekend mode: require retest after impulse"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.77,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved"],
      "data_missing": ["current_cycle_paper_monitor"],
      "suggested_effect": "advisory_only",
      "facts_used": ["50 active B-tier crypto signals (all long)", "BCH swing: TRIGGERED/ENTERED (tr status)", "HMSTR/SYN/WLFI intraday: WAITING (wa status)", "OGN/HEI/VANRY/TRUMP/DOGE: TP status", "~35 ENTERED UNRESOLVED (carry-forward)", "17 untracked alerts (signal tracking gap)"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.83,
      "reason_codes": ["headline_risk", "manual_review", "reduce_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TLM: Binance delisting block ALL new entries", "HOT: extreme squeeze (funding -1.1%/8h, OI +172%)", "ETH/SOL/APT: exploit_hack operator-review blocks", "Shorts: 0W/4L PF=0.10 -2.5R = systemically failing", "VANRY: post-impulse +50% yesterday OI spike", "Weekend liquidity thin", "17 untracked alerts (integrity gap growing)"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["playbook_working", "playbook_failing", "fresh_expired_problem"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing: PF=3.9 WR=34% +47.4R/week (WORKING)", "scalp: PF=2.4 WR=48% +29.8R (working but TP1 mismatch)", "intraday: PF=1.1 WR=3% +1.1R (borderline; no-catalyst -3R/14d)", "shorts: PF=0.10 0W/4L (FAILING)", "weekend mode: PF≈1.9 (underperforms weekday)", "~35 ENTERED UNRESOLVED (0R display, NOT missed entries)"]
    },
    {
      "agent": "head_trader",
      "verdict": "normal",
      "confidence": 0.78,
      "reason_codes": ["risk_on", "longs_preferred", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Synthesised all eight agents above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.78,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "BCH/USDT",
      "trigger": "already entered swing B at ~236-238; hold above 234.04 invalidation; TP1 ~243.50",
      "reason": "Cleanest active: swing B triggered, OI +3.49% clean positioning, near-zero funding, volume 1.31x, best mode PF=3.9, multi-exchange 88.7%"
    },
    "best_short_candidate": {
      "symbol": "VANRY/USDT",
      "trigger": "1h close below ~0.0048 post-impulse support after OI flush; NOT actionable now",
      "reason": "OI was +242% at swing snapshot; negative funding; if impulse fails and support breaks, short thesis forms. Current tape too bullish."
    },
    "best_catalyst_candidate": {
      "symbol": "ADA/USDT",
      "trigger": "RealFi Testnet launch Monday July 6; pullback to 0.64-0.66 before Monday open; BTC must hold",
      "reason": "Confirmed event catalyst Monday; intraday B triggered; expansion watchlist ready-for-promotion"
    },
    "avoid_candidate": {
      "symbol": "TLM/USDT + HOT/USDT",
      "reason": "TLM: Binance delisting monitoring active +252% 7d block_requires_operator_review ALL new entries. HOT: extreme squeeze funding -1.1%/8h OI +172% crowding unknown."
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
| data_quality | **ok** | 0.82 | `scheduler_fresh`, `report_stale` | advisory_only |
| market_regime | **ok** | 0.85 | `risk_on`, `longs_preferred` | advisory_only |
| catalyst_narrative | **caution** | 0.62 | `fresh_catalyst`, `mapping_weak`, `narrative_supported` | advisory_only |
| derivatives_squeeze | **caution** | 0.70 | `squeeze_risk`, `post_unwind_chop`, `oi_supports` | advisory_only |
| technical_entry | **caution** | 0.73 | `clean_retest`, `chase_risk`, `stale_before_entry` | advisory_only |
| execution_lifecycle | **ok** | 0.77 | `open_actionable`, `waiting_for_entry`, `entered_unresolved` | advisory_only |
| risk_manager | **caution** | 0.83 | `headline_risk`, `manual_review`, `reduce_risk`, `correlation_cluster` | advisory_only |
| playbook_performance | **ok** | 0.80 | `playbook_working`, `playbook_failing`, `fresh_expired_problem` | advisory_only |
| head_trader | **normal** | 0.78 | `risk_on`, `longs_preferred`, `manual_review` | advisory_only |

---

## 4. What Changed vs Previous Review (16:20 EEST)

| Dimension | 16:20 Review | Now (18:39) |
|---|---|---|
| Active signals | 50 | 50 (stable) |
| Untracked alerts | 10 | **17** (+7 new) |
| BCH/USDT swing | TRIGGERED (entering) | **ENTERED — monitoring** |
| VANRY 24h return | +50% (swing 13:15) | +13% intraday → post-impulse rolling off |
| Report freshness | Swing fresh | **Scalp + intraday refreshed (cycle 7)** |
| Momentum_breakout basket | Not present | **NEW: TLM/VANRY/HMSTR fresh <1h** |
| SYN/USDT | Not in B-tier | **NEW: intraday B #2 (69.3, volume 1.48x)** |
| BCH thesis | Entering | **CONFIRMED — actively managed** |
| ADA thesis | Monday catalyst carry-forward | Unchanged — still pending Monday |

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 640
- **Catalyst cycle 15-38 scanned rows:** 302
- **Narrative baskets active:** 4
  - `momentum_breakout` — **fresh <1h** — TLM/VANRY/HMSTR (pure momentum, no news catalyst)
  - `perps_dex_narrative` — fresh <6h — HYPE/USDT (Hyperliquid 9% global perps, $4B OI)
  - `delisting_thin_liquidity` — fresh <24h — HYPE/USDT (Gold $100 flash crash thin liquidity)
  - `ai_narrative` — fresh <6h — NEAR/RENDER/TAO/FET
- **Top importance catalysts:** UNH DOJ probe 0.73, AVAX FIFA/Kraken 0.69, ETH Lean Ethereum roadmap 0.65-0.67, Fed positive signals 0.66, HYPE thin liquidity 0.61
- **Catalyst mapping:** Prior review: 28.3% (543/1916 events mapped). **CATALYST MAPPING WEAK THIS RUN — use catalyst layer as context, not final decision.**
- **Top 3 unmapped headlines:** (1) Mbappé World Cup meme token speculation (rumour), (2) PHR class action deadline (basket/legal), (3) CALX class action deadline (basket/legal)

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-on (BTC/ETH uptrend, breadth 79%, low volatility, Fed positive signals)
- **Stocks mood:** CLOSED (Sunday + US holiday weekend; reopens Monday July 6)
- **Dominant narrative:** Momentum continuation. Altcoin breadth broad and stable. Exploit/hack noise (ETH/SOL/APT) is background, not regime-changing. Momentum_breakout basket freshly formed (TLM/VANRY/HMSTR).
- **Preferred side now:** longs (RS-leaders with pullback structure; catalyst-backed for Monday open)
- **Best long candidate:** BCH/USDT — entered swing B; hold above 234.04
- **Best short candidate:** none clean — VANRY watch only if 0.0048 fails
- **Best catalyst-backed candidate:** ADA/USDT (Monday RealFi Testnet) + HYPE/USDT (perps DEX narrative — basket conflict note)
- **What to avoid:** TLM (delisting), HOT (extreme squeeze), ETH/SOL/APT (exploit blocks), intraday no-catalyst, shorts
- **What would change the view:** BTC loses local support → reduce longs immediately; HOT squeeze unwind → potential short setup; ADA delays Monday launch → downgrade catalyst thesis

---

## 7. Candidate Deep Dives

### Candidate 1 — BCH/USDT | B-tier | Swing | ENTERED — MONITORING

**Status:** ENTERED — swing B triggered at ~236-238 (active-signals `tr` status). Now in monitoring phase.

- 24h: +2.24-2.37%, 7d: +23-24% — healthy multi-day momentum, not chasing a gap
- Volume 1.31x (highest confirmed volume ratio across all candidates)
- Derivatives: OI +3.49%, funding -2.49e-05 (near-zero) → cleanest positioning in the field
- Multi-exchange: Binance + MEXC, 88.7% confirmation
- Setup quality: 62-67%. Not overextended.
- ATR 4.2 → well-defined risk parameters. Invalidation 234.04. TP1 243.50, TP2 247.80, TP3 252.10.
- No fresh catalyst — relying on swing momentum continuation (swing mode works without catalyst per PF=3.9 playbook stats).
- No exploit/delisting/legal block.

**Mood alignment:** YES — risk-on, swing long, RS-leader, volume confirmed. Optimal mode in current conditions.

**Chase check:** No. Entry at lower end of 24h range, pullback structure confirmed before trigger.

**Verdict:** OPEN ACTIONABLE — hold and manage. Best live position in portfolio.

---

### Candidate 2 — TLM/USDT | B-tier | Intraday + Scalp | WAITING — OPERATOR REVIEW BLOCK

**Status:** WAITING FOR ENTRY. **BLOCK: `block_requires_operator_review` — Binance delisting monitoring active (CoinMarketCap AI Summary).**

- Momentum score 100/100. 7d return +252%, 24h +22-29%. Volume 3.12-3.56x. Momentum_breakout basket primary.
- Intraday score 68.9 (below 70 active threshold). Scalp score 75 — but scalp report explicitly notes "watchlist/no-trade."
- Current price 0.0032, entry zone 0.0030-0.0031 → slightly above zone (post-impulse chase risk).
- OI +1.28% (intraday scalp timeframe), negative funding (shorts paying longs).
- Intraday counter-thesis: "the move may be late relative to EMA20/ATR."

**LEGAL/HEADLINE RISK:** **DELISTING** — TLM Alien Worlds: Binance delisting monitoring active. +252% 7d may represent distribution into impending delisting. ALL new entries require human operator sign-off.

**Verdict:** MANUAL REVIEW REQUIRED. No new entries. Existing exposure: consider taking profit into strength given delisting risk and potential adverse exit liquidity.

---

### Candidate 3 — VANRY/USDT | B-tier | Scalp + Intraday + Swing | WAITING — POST-IMPULSE DYNAMICS

**Status:** WAITING across all modes. 7 untracked alerts sent today across scalp/swing cycles.

- Post-impulse: swing (13:15) showed +50.64% 24h with OI +242%, funding -0.00124524 → extreme crowding.
- Now (18:38): intraday shows +13% 24h, OI still elevated (+69% scalp), funding -0.000238.
- Yesterday's +50% impulse rolling out of 24h window — dynamics calming but not fully reset.
- Scalp entry zone: 0.0050-0.0052, current 0.0053 → at zone edge (entry possible on tiny dip).
- Volume: 0.48-0.55x below average → momentum may be fading.

**Short-watch trigger:** 1h close below 0.0048 (scalp invalidation level) after OI normalizes further → post-impulse short thesis. NOT actionable now.

**Long entry:** Wait for OI to fully normalize from yesterday's spike AND volume to confirm. Do not enter intraday without fresh catalyst.

**Verdict:** WAITING — no long entry now. Short-watch at 0.0048 only.

---

### Candidate 4 — ADA/USDT | B-tier | Intraday + Expansion Watchlist | WAITING (CATALYST-BACKED)

**Status:** WAITING FOR ENTRY. Active-signals shows intraday B (tp status — TP1 touched). Expansion watchlist: `ready-for-promotion`.

- Catalyst: RealFi Testnet launch Monday July 6 (carry-forward from 16:20 review's external research; not re-verified externally this slot).
- RS vs BTC: -0.7 to -1.0% → NOT an RS-leader. This is purely a catalyst play.
- Volume: 0.6x (below average — no pre-event accumulation visible yet).
- Score: 49-66 across expansion/intraday (borderline).
- Intraday B already triggered (tp) — TP1 level touched from prior cycle.

**Chase check:** If price is already at TP1 level → do NOT enter now. Wait for Monday pullback.
**Catalyst risk:** Single-source. If testnet delayed/underwhelming → no trade thesis.

**Best entry:** Sunday evening/early Monday pullback to 0.64-0.66, BTC holding, before RTH open. If gap up Monday → skip.

**Verdict:** WAITING — catalyst watch. Pre-Monday setup only.

---

### Candidate 5 — HYPE/USDT | Basket primary | Perps DEX narrative | REVIEW/SHADOW

**Status:** REVIEW/SHADOW — basket primary for `perps_dex_narrative` (fresh <6h). NOT in B/A active `proposed_signals`. Playbook: `wait_pullback`.

- Catalyst: Hyperliquid captures 9% global perps market, $4B OI (CryptoBriefing, single_source, importance 0.61).
- CONFLICT: HYPE is simultaneously in `perps_dex_narrative` (positive, buy pullback) AND `delisting_thin_liquidity` (negative, Gold flash crash exposed thin liquidity risks).
- Two contradicting baskets on the same symbol → NOT actionable until conflict resolves.

**Verdict:** REVIEW/SHADOW only. Monitor for basket conflict resolution. Do not enter.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Status | Verdict | Trigger |
|---|---|---|---|---|---|
| 1 | BCH/USDT | swing B | ENTERED | Hold active | Above 234.04 invalidation |
| 2 | ADA/USDT | intraday B | WAITING (catalyst) | Watch — Monday | Pullback 0.64-0.66 before Jul 6 open |
| 3 | SYN/USDT | intraday B | WAITING | Watch | Retest 0.4116-0.4240; volume confirm |
| 4 | WLFI/USDT | intraday B | WAITING | Watch | Pullback 0.0593-0.0597 |
| 5 | HYPE/USDT | basket | REVIEW/SHADOW | Watch — conflict | Basket conflict must resolve |

**Best long-watch:** ADA/USDT — trigger: pullback 0.64-0.66 before Monday open, BTC holding.
**Best short-watch:** VANRY/USDT — trigger: 1h close below 0.0048 (NOT now).
**Best catalyst-watch:** ADA (Monday Jul 6 RealFi Testnet) + HYPE (perps DEX, conflict pending).

---

## 9. Avoid / No Trade (This Window Only)

| Symbol | Reason |
|---|---|
| TLM/USDT | Binance delisting block — ALL new entries need operator sign-off |
| HOT/USDT | Extreme squeeze: funding -1.1%/8h, OI +172% (crowding unknown) |
| ETH/USDT | exploit_hack operator-review block |
| SOL/USDT | exploit_hack operator-review block |
| APT/USDT | exploit_hack operator-review block |
| Intraday no-catalyst | Documented -3R/14d; require RS-leader or breakout confirmation |
| Any short | Systematically failing in bullish tape (0W/4L, PF=0.10) |
| VANRY new long | Post-impulse +50% yesterday; OI elevated; wait for structure reset |

_This verdict applies to the current decision window only. Scanning and data collection continue uninterrupted._

---

## 10. Main Risks

1. **Exploit noise (ETH/SOL/APT):** Multiple confirmed hacks (UXLINK 14,336 ETH, Step Finance $21M SOL → Tornado Cash). Monitor for sentiment contagion to altcoins.
2. **HOT squeeze unwind:** Funding at -1.1%/8h unsustainable. Forced covering may trigger sharp reversal. No new entries.
3. **TLM delisting:** Binance delisting → potential price crater. Any TLM long exposure needs exit plan.
4. **VANRY post-impulse OI overhang:** If long overhang flushes → fast drop to 0.0042 support. Watch 0.0048.
5. **Weekend liquidity:** Thin markets → wider wicks, faster stop-outs. Prefer Monday for new entries.
6. **Untracked alerts (17):** Growing tracking gap. Signal performance data is incomplete — winrate/PF undercounting actual results.
7. **Intraday no-catalyst edge:** PF=1.1 week-to-date; known -3R/14d per no-catalyst cut. B-tier intraday signals without catalyst are watchlist quality despite `actionable` label.

---

## 11. Action Plan — Next 4 Hours (18:39 → 22:39 EEST)

1. **BCH swing:** Manage active. Hold above 234.04. TP1 at 243.50 — let it run unless BTC breaks structure.
2. **ADA watch:** Monitor Sunday evening. If BTC holds and ADA pulls back to 0.64-0.66 → Monday pre-open setup. Set alert 0.66.
3. **TLM:** No new entries. Existing exposure: take profit into strength (delisting risk).
4. **HOT:** Avoid. Set alert if funding turns positive (squeeze unwind signal).
5. **VANRY:** No new longs. Alert at 0.0048 for potential short watch.
6. **SYN:** Wait for pullback to 0.41-0.42. Volume must confirm breakout retest.
7. **HYPE:** Monitor basket conflict resolution. Do not enter.
8. **General:** No new intraday entries without RS-leader confirmation. No shorts. Swing mode only for new entries.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|---|---|---|
| **Scalp** | watch only | Low confidence (14d PF 0.14). No A-tier. B-tier: WLFI/VANRY/BTW waiting. Weekend mode: require retest. |
| **Intraday** | caution — RS-leader only | PF=1.1 week, no-catalyst -3R/14d. HMSTR/SYN/WLFI waiting. Only with RS-leader or breakout confirm. |
| **Swing** | active — manage BCH | Best mode PF=3.9. BCH entered. ADA catalyst-watch for Monday. |
| **Stocks** | planning only | Closed Sunday. Reopens Monday July 6. No intraday entries before RTH. |
| **Shorts** | avoid | 0W/4L, PF=0.10 in current bullish tape. |

---

## 13. Sources

_Internal data only (external web research not performed this slot). All claims traceable to internal reports._

- Scalp `2026-07-05_15-32` UTC — `data/reports/scalp/2026-07-05_15-32_scalp_report.md`
- Intraday `2026-07-05_15-38` UTC — `data/reports/intraday/2026-07-05_15-38_intraday_report.md`
- Swing `2026-07-05_13-23` UTC — `data/reports/swing/2026-07-05_13-23_swing_report.md`
- Catalyst cycle 15-38 EEST — `data/catalysts/2026-07-05/catalyst_cycle_15-38.md`
- Catalyst events / narrative baskets JSONL — `data/catalysts/2026-07-05/`
- LLM analysis packet (intraday) — `data/processed/llm_analysis_packet.md`
- Active signals CLI: `python -m src.cli active-signals --asset-class crypto` (live 18:39)
- Signal stats CLI: `python -m src.cli signal-stats --asset-class crypto` (live 18:39)
- Untracked alerts: `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-05` (live 18:39)
- Previous enriched review (BCH entry, ADA catalyst context): `OPUS_ENRICHED_REVIEW_AUTO_2026-07-05_1620.md`
- TLM delisting risk: production risk warning (CoinMarketCap AI Summary, single_source, in reports)
- HOT squeeze: derivatives data from scalp/intraday reports (Bybit OI history, MEXC fallback)
- Untracked alerts report (17 today): `scripts.detect_untracked_legacy_alerts`

---

## 14. Fix Requests / TODO

### TODO-untracked-alerts-growing
- **issue:** Untracked legacy alerts grew 8 → 10 → 17 across today's reviews. All sent to Telegram without `proposed_signal` backing → excluded from PF/winrate tracking. Gap is widening every cycle.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-05` → 17 records, all `NO (no proposed_signal)`. Includes ETHFI/ADA/BCH/VANRY scalp (08:27, 10:46, 15:32), AIGENSYN swing (13:23), VANRY/SENT/ADA/ETHFI swing (13:34-14:04).
- **suggested manual fix:** Trace why scalp and swing cycles generate `watchlist_alerts` without writing `proposed_signals`. Disconnect may be in alert routing vs signal-creation pipeline for certain mode/symbol combos. Manual session should audit the `watchlist_alerts → proposed_signals` path for these symbols.
- **priority:** high
- **first observed:** 2026-07-04, worsening on 2026-07-05

### TODO-intraday-no-catalyst-playbook-gate
- **issue:** Intraday mode fires B-tier `actionable` signals without catalyst that are documented net-negative (-3R/14d). These signals reach Telegram as actionable despite the known failure mode.
- **evidence:** `signal-stats`: intraday PF=1.1, WR=3%, +1.1R (barely positive, week); intraday report: "14d no-news cut: WR 23% / PF 0.70 / −3R"; playbook note: "Without catalyst, prefer RS-leader long or wait for breakout confirmation."
- **suggested manual fix:** Add a scoring gate that prevents no-catalyst intraday signals from reaching `actionable` status without RS-leader tag OR breakout_confirmation OR analyst_override flag. Alternatively, change the `status` label to `watch_only` for this sub-bucket and suppress Telegram routing.
- **priority:** medium
- **first observed:** 2026-07-03, documented in multiple reviews
