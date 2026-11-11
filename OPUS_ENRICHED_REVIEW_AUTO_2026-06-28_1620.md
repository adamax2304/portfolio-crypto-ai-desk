# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

**Slot:** pre-US-open decision review (16:20 EEST)
**Time:** 2026-06-28 16:20 EEST
**Date:** 2026-06-28 (Sunday — weekend mode active; US markets CLOSED; next US session Mon June 29 16:30 EEST)
**Model:** claude-sonnet-4-6
**Advisory only — no auto-trade, no signal registration**

---

## 1. Executive Summary

**Slot: pre-US-open decision review — advisory only / no auto-trade.**

Note: Today is Sunday; US markets are closed. This "pre-US-open" slot is planning for **Monday June 29 open at 9:30 ET = 16:30 EEST**. Treat all stock analysis as planning context only — no actionable entries until Monday RTH.

**Crypto mood: risk-off / range-chop.** BTC ~$60,148 (range $58k–$62k), ETH downtrend, F&G=18 (Extreme Fear). BTC is threatening its 200-week MA for the first time since October 2023. Weekend mode active with historically poor signal performance (WR 18% on weekend signals). System shows 0 open actionable signals; all 12 active crypto signals are in ENTERED UNRESOLVED status.

**What changed since 11:39 review:** Cycle 2 ran successfully (13:56) after exchange failures in Cycle 1. Fresh scalp (13:20) and intraday (13:51) reports generated. Catalyst events expanded from 17 → 111+. New signal: PUMP B scalp long (weekend=Y, ENTERED UNRESOLVED). ACT continued to extend (+99% by 13:20 data, rejected across all reports — do not enter). BTC held $60k support through midday.

**Head Trader routing:** Prefer **HYPE catalyst-backed long-watch** on any pullback; **ZEC short-watch** on failed bounce retest; **avoid intraday mode entirely** (PF=0.00, -5R this week). Swing mode remains best (PF=2.06, +16R). Do NOT chase ACT. Weekend liquidity thin — demand cleaner structure.

**Monday gap risk:** UNH DOJ criminal probe (stock) — any stock signals involving UNH must be AVOIDED on Monday open. BTC $59,250 is key breakdown level; a weekend break there = Monday opens with gap-down risk.

ALWAYS-SCAN continues. Scanner, scheduler, data collection continue in all conditions.

---

## 2. Data Used

| Source | File | Generated (EEST) | Age at 16:20 | Status |
|--------|------|-----------------|--------------|--------|
| Scheduler log | scheduler.log | 16:20 | ~0 min | **FRESH** |
| Latest cycle | cycle_02_12-56_summary.md | 13:56 | 2h24m | **FRESH** (<3h) |
| Scalp report | 2026-06-28_13-20_scalp_report.md | 16:20 (data 13:00 UTC) | 3h | **FRESH** |
| Intraday crypto | 2026-06-28_10-51_intraday_report.md | 13:51 | 2h29m | **FRESH** |
| Swing crypto | 2026-06-27_01-20_swing_report.md | 04:20 Jun 27 | ~36h | **STALE** (carry-forward) |
| Stocks intraday | 2026-06-26_20-14_stocks_intraday | 23:14 Jun 26 | ~41h | **STALE** — weekend closed |
| Stocks swing | 2026-06-26_15-06_stocks_swing | 18:06 Jun 26 | ~46h | **STALE** — weekend closed |
| Stocks invest | 2026-06-26_15-13_stocks_invest | 18:13 Jun 26 | ~46h | **STALE** — weekend closed |
| Catalyst events | data/catalysts/2026-06-28/ | 13:20 (scalp) | 3h | **FRESH** (111+ events, 4 baskets) |
| Catalyst cycle | catalyst_cycle_10-51.md | 10:51 | 5h29m | **CARRY-FORWARD** |
| LLM crypto packet | llm_analysis_packet.md | 13:20 UTC | 3h | **FRESH** |
| Active signals (crypto) | CLI live 16:20 | live | live | 12 signals |
| Signal-stats | CLI live 16:20 | live | live | n=123, PF=1.45 |
| Untracked alerts | CLI live 16:20 | live | live | NONE |
| Paper monitor | paper_monitor_status | cycle_02 13:56 | 2h24m | **FRESH** |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-28_1139.md | 11:39 | 4h41m | READ |
| External web research | WebSearch×3, WebFetch×1 | 16:20 | live | AVAILABLE |

---

## 3. Scheduler / Data Freshness

- **scheduler.log mtime:** 16:20 EEST — exactly current. FRESH.
- **Latest cycle:** `cycle_02_12-56_summary.md` completed **13:56 EEST** (2h24m ago). Steps: ok=27, failed=0. NOT DEFERRED.
- **Weekend mode:** ACTIVE (Sunday). All signals carry weekend penalty overlay.
- **Crypto signals (live CLI 16:20):** 12 active B-tier signals. All ENTERED UNRESOLVED.
  - PUMP scalp B long 65% (weekend=Y) — NEW since 11:39 review
  - BERA swing B long 67% (weekend=Y)
  - AAVE swing B long 65% (weekend=Y)
  - SOL swing B long 74%
  - BTC intraday B short 66%
  - ETH swing B short 65%
  - HEI intraday B long 66%
  - BTC swing B short 65%
  - HOD swing B long 72%
  - ETH swing B long 66%
  - AXS swing B long 65% (weekend=Y)
  - MEM swing B short 68%
- **Paper monitor (cycle_02):**
  - Open actionable: 0
  - Waiting for entry: 0
  - Entered unresolved: 22
  - Review/Shadow: 185
  - No-entry/stale/moved-away: 8
  - Closed today: 304W / 2L / 0flat (paper structural TP labels — not live signal resolutions)
  - Needs review: 0
- **Untracked legacy alerts:** NONE — clean.
- **Data gaps:** Swing crypto 36h stale. All stocks reports 41-46h stale (weekend-closed expected). Reddit social 403 blocked (multiple cycles). On-chain: config missing.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-06-28 16:20 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["swing_crypto_stale_36h", "stocks_all_stale_41-46h", "onchain_config_missing", "social_attention_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log mtime 16:20 EEST — live",
        "cycle_02 completed 13:56 EEST (2h24m ago), ok=27 failed=0",
        "scalp report 13:20 fresh, intraday 13:51 fresh",
        "swing report 36h stale — carry-forward flagged",
        "stocks reports 41-46h stale — weekend closed, not actionable",
        "catalyst events 111+ today, 4 baskets"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["risk_off", "chop", "shorts_preferred"],
      "data_missing": ["live_btc_price_from_exchange", "etf_flow_today"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: downtrend (both scalp and intraday reports)",
        "ETH trend: downtrend",
        "F&G=18 Extreme Fear (cycle_02 market dashboard)",
        "VIX=18.41 SPY down QQQ down",
        "ETH/BTC=0.026211 — historically very low",
        "Altcoin breadth EMA20: 56-59% (borderline)",
        "BTC near 200-week MA (external: investinglive.com Jun 28 2026)",
        "BTC key support $58,000-58,400, resistance $60,750-61,000",
        "Crypto mode=chop from market dashboard snapshot id=12"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["stale_catalyst", "fresh_catalyst", "mapping_weak"],
      "data_missing": ["etf_flow_today", "on_chain_whale_flows"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC catalyst: quarterly loss, IBIT investors -40%, Grayscale/Strategy narrative",
        "ETH catalyst: ETF outflows $12.85M (AMBCrypto), 3 consecutive losing quarters",
        "HYPE catalyst: Bitwise $114M staking confirmed, BHYP ETF live NYSE + Xetra",
        "ACT: no verified catalyst, pure momentum +99% — mapping=weak",
        "ZEC: whale shorts $4.92M (AMBCrypto) + Coinbase CEO controversy",
        "13 high-importance symbol-tagged catalysts unmapped (catalyst_integrity): ADA,ALGO,AVAX,COIN,DOT,FIL,HBAR,INJ,MSFT,TON",
        "Legal: UNH DOJ criminal probe flagged (2 events)",
        "Regulatory: CLARITY Act approval window narrowing"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["post_unwind_chop", "data_unavailable"],
      "data_missing": ["oi_numeric_history_sparse", "liquidation_heatmap", "order_book_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Squeeze phase distribution (95 symbols): post_unwind_chop=39 (41%), unknown=36, build_up=11, squeeze_expansion=3, distribution=1, unwind=5",
        "Dominant: post_unwind_chop — market already deleveraged, now in choppy drift",
        "ACT OI 24h +277.9% (intraday report) — fresh long positioning, crowding unknown",
        "S/USDT OI +42.51% — fresh positioning, crowding unknown",
        "ZEC price down + OI up = fresh shorts pressing, potential squeeze if reclaim",
        "Funding numeric OI history noted as sparse in intelligence layer"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["chase_risk", "stale_before_entry", "clean_retest"],
      "data_missing": ["tradingview_chart_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ACT: rejected across ALL reports — >2ATR from EMA20, do not chase",
        "PUMP: scalp rejected at 13:20 (score 48.8, >2ATR, extended). Signal generated earlier when lower",
        "S/USDT: best watchlist candidate scalp (55.8) and intraday (59.6) — pullback zone 0.0241-0.0246",
        "HYPE: not in top reports but catalyst-backed; perps DEX basket primary member",
        "ZEC: conditional retest short zone 385.25-387.60, OI building",
        "All 12 active signals are ENTERED UNRESOLVED — no fresh clean entries this window",
        "TradingView/manual chart check unavailable — using internal OHLCV/ATR/EMA fields only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["entered_unresolved", "no_entry", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Open actionable: 0",
        "Waiting for entry: 0",
        "Entered unresolved: 22 (paper); 12 live active signals all ENTERED UNRESOLVED",
        "Review/Shadow: 185",
        "No-entry/stale/moved-away: 8",
        "Needs review: 0",
        "Untracked alerts: NONE",
        "Expired split: entered-after-entry=22, no-entry/stale=8"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["stock_positions_detail"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Weekend mode active — weekend signals historically WR 18%, underperform (signal-stats obs)",
        "Intraday mode: PF=0.00, -5R, wins=0 from 5 losses triggered — AVOID new intraday longs",
        "BTC $59,250 = breakdown trigger (external: investinglive.com). Break = Monday gap-down risk",
        "UNH DOJ criminal Medicare fraud probe — stock signals with UNH = AVOID Monday open",
        "SMCI ongoing legal risk (flagged in previous reviews)",
        "ACT >2ATR — if any prior entry exists, it is entered in an extended zone",
        "F&G=18: extreme fear environment reduces stop-and-reverse reliability"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["forward_shadow_sample_too_small_3d"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "A/B headline: n=123, triggered=111, wins=24, losses=40, WR=21.6%, PF=1.45, totalR=18R",
        "By mode — swing: PF=2.06, +16R (BEST — prefer this playbook)",
        "By mode — scalp: PF=1.35, +7R (acceptable)",
        "By mode — intraday: PF=0.00, wins=0, -5R (WORST — avoid new intraday entries)",
        "By setup — trend/momentum n=35: PF=2.62, +13R",
        "By setup — fvg/retest n=86: PF=1.15, +5R",
        "Weekend signals n=25, WR 18% — underperform observation",
        "Paper-shadow FORWARD: B +2.38R vs A -19.65R (NOT_READY, 5/6 criteria, 3d window)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["wait_for_trigger", "shorts_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Risk-off crypto: prefer catalyst-backed RS-leader longs with pullback, or clean short retests",
        "All 12 active signals entered unresolved — no new entries needed this window",
        "HYPE: strongest catalyst narrative (Bitwise $114M, BHYP ETF) — long-watch on pullback",
        "ZEC: fresh shorts building, catalyst present, short-watch on failed retest",
        "ACT: most extended move (+99%) — not enterable, chase risk maximum",
        "Intraday mode fails (PF=0) — avoid all new intraday entries",
        "Monday planning: UNH avoid, BTC $59,250 breakdown watch",
        "Weekend mode: demand cleaner structure, prefer retests over breakouts",
        "ALWAYS-SCAN continues — no recommendation to stop system"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.75,
    "preferred_side": "catalyst_backed",
    "best_long_candidate": {
      "symbol": "HYPE/USDT",
      "trigger": "Pullback to $58-60 zone with volume confirmation; BHYP institutional demand as floor support",
      "reason": "Bitwise $114M staking + BHYP ETF live on NYSE+Xetra = verified institutional catalyst. Perps DEX narrative basket primary. Wait for pullback, do not chase current price"
    },
    "best_short_candidate": {
      "symbol": "ZEC/USDT",
      "trigger": "Failed bounce/retest zone 385.25-387.60 with 1h close confirmation. Current price ~384-385",
      "reason": "Whale shorts $4.92M, OI building (price down + OI up = fresh shorts pressing), Coinbase CEO controversy, downtrend -15% 7d"
    },
    "best_catalyst_candidate": {
      "symbol": "HYPE/USDT",
      "trigger": "Any pullback toward $58-60 after BHYP ETF + $114M staking confirmation",
      "reason": "Strongest verified institutional catalyst this cycle. Bitwise BHYP spot ETF trading NYSE and Deutsche Borse Xetra. Perps DEX narrative basket primary member"
    },
    "avoid_candidate": {
      "symbol": "ACT/USDT",
      "reason": "Chase risk maximum: >2ATR from EMA20 across all reports, +99% 24h, rejected by system filters. Wait for pullback before any consideration. Meme/AI token (Act I The AI Prophecy on Solana) with no verified catalyst supporting current move"
    },
    "operator_action": "wait_for_trigger",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason Codes | Suggested Effect |
|-------|---------|-----------|-------------|-----------------|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.82 | risk_off, chop, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.68 | stale_catalyst, fresh_catalyst, mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.60 | post_unwind_chop, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, stale_before_entry, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.78 | entered_unresolved, no_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.82 | headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | ok | 0.82 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.75 | wait_for_trigger, shorts_preferred | advisory_only |

---

## 4. What Changed vs Previous Review (11:39 EEST)

**Previous review:** Europe / pre-US context, 11:39 EEST (4h41m ago)
File: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-28_1139.md`

| Change | Previous (11:39) | Current (16:20) |
|--------|-----------------|----------------|
| Cycle | Cycle_01 (10:44, exchange failures) | Cycle_02 (12:56, ok=27 failed=0) |
| Fresh scan | FAILED — universe=0, all exchanges | SUCCESS — binance 56, bybit 2, mexc 58 scanned |
| Crypto signals | 11 active (all ENTERED UNRESOLVED) | 12 active (+PUMP B scalp long weekend=Y) |
| Catalyst events | 17 events, 1 basket | 111+ events, 4 baskets |
| ACT | +37% (intraday report), rejected (>2ATR) | +99% intraday score 98.6, rejected again |
| S/USDT | Top watchlist scalp/intraday | Still top watchlist (55.8 scalp / 59.6 intraday) |
| HYPE | Top catalyst-backed candidate | Confirmed stronger (external: Bitwise $114M + BHYP ETF) |
| BTC | ~$60-61k holding | ~$60,148 — holding $60k support through midday |
| Thesis changed? | HYPE catalyst thesis | Unchanged — confirmed stronger externally |
| Invalidated? | Exchange failure narrative | RESOLVED — cycle_02 ran clean |
| UNH legal risk | Flagged (DOJ probe, 4+ stock signals) | Carry-forward — AVOID for Monday open |

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 111 (cycle_10-51 at 10:51) / 114 (scalp report 13:20)
- **Narrative baskets:** 4
  - `delisting_thin_liquidity` — playbook: avoid_low_liquidity (fresh <6h)
  - `perps_dex_narrative` — primary: HYPE/USDT; related: DYDX, GMX, ASTER (playbook: wait_pullback)
  - `ai_narrative` — primary: NEAR, RENDER, TAO, FET (playbook: related_beta_rotation)
  - `momentum_breakout` — primary: ACT, S, PUMP (fresh <1h at scan time) (playbook: wait_pullback)
- **By catalyst type:** other_news=107, legal_risk=2, regulatory_sector_headline=1, low_liquidity_event=1
- **Legal/regulatory flags:**
  - UNH: DOJ criminal probe into Medicare fraud + Optum Rx extension → AVOID all UNH stock signals Monday open
  - CLARITY Act approval window narrowing (regulatory/sector context only)
- **Catalyst integrity alert:** 13 high-importance symbol-tagged catalysts NOT mapped into catalyst_events: ADA, ALGO, AVAX, COIN, DOT, FIL, HBAR, INJ, MSFT, TON. These symbols may have active signals without catalyst context in this review.
- **Coverage note:** 107/111 events are "other_news" category with variable symbol precision. Use catalyst layer as supplementary context rather than sole decision input.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off / chop — BTC downtrend, ETH downtrend, F&G=18 (Extreme Fear), VIX=18.41, SPY/QQQ down, BTC near 200-week MA (first time since Oct 2023)
- **Stocks mood:** closed (Sunday weekend) — planning context only; next actionable: Monday June 29 RTH 9:30 ET (16:30 EEST)
- **Dominant narrative:** BTC on track for rare back-to-back quarterly loss; Fed hawkishness (Kashkari potential rate hike signals); AI stock rotation pulling capital from crypto; ETH ETF outflows $12.85M; ETH/BTC at 0.026211 (multi-year low)
- **Preferred side now:** catalyst-backed (HYPE institutional) + swing shorts on failed retests (ZEC) — avoid intraday longs
- **Best long candidate:** HYPE/USDT — trigger: pullback to $58-60 zone; Bitwise BHYP ETF institutional floor
- **Best short candidate:** ZEC/USDT — trigger: failed bounce retest 385.25-387.60 (1h close rejection); OI building, whale shorts pressing
- **Best catalyst-backed candidate:** HYPE/USDT — Bitwise $114M staking + BHYP spot ETF (NYSE + Deutsche Borse Xetra) — verified externally
- **What to avoid:** ACT (>2ATR chase risk), all new intraday longs (PF=0.00/-5R), PUMP B without confirmed pullback entry, any entry after vertical candle (weekend scalp rule)
- **What would change the view:** BTC reclaim $60,750-61,000 → mild bullish repair, RS-leader longs possible; BTC break below $59,250 → escalate risk-off, avoid all longs; HYPE pullback to $58-60 with volume → long trigger confirmed

---

## 7. Candidate Deep Dives

### Candidate 1: HYPE/USDT — Best Catalyst-Backed Long-Watch

**Tier:** C-watch (no active signal) | **Direction:** long | **Mode:** catalyst-watch

- **Has price already reacted?** Partially — institutional accumulation ongoing (BHYP ETF live, Bitwise staking). Not a one-time event; institutional demand is structural.
- **Is the setup chasing?** No active signal. ATH ~$76.67; current level well below. Perps DEX basket playbook: `wait_pullback`. Not chasing — waiting.
- **Is there a retest/pullback structure?** Yes — need pullback from current level to $58-60 zone before entry. Institutional ETF buyers act as demand floor.
- **Would entry NOW be late?** Unknown without current chart. TradingView unavailable. Demand pullback as per basket playbook.
- **What level makes it actionable?** Pullback to $58-60 range + volume acceptance + 1h stability. ATR/EMA20 check required on next cycle report.
- **Aligned with mood?** Partially — risk-off hurts alts broadly, but institutional catalyst creates differentiated demand. This is a catalyst-specific trade, not beta momentum.
- **Long, short, or wait-for-trigger?** WAIT FOR TRIGGER — pullback required first.
- **Actionable now?** Not actionable this window. Wait for pullback + RTH-equivalent confirmation Monday.
- **Invalidation:** Break below BHYP ETF institutional buy zone; BTC breaks $59,250 hard; Bitwise BHYP AUM significant outflow.
- **Catalyst confirmation:** YES — verified externally: Bitwise deposited 1.775M HYPE (~$114M), staked entire amount on Hyperliquid network via Bitwise Onchain Solutions. BHYP spot ETF trades NYSE and Deutsche Borse Xetra. In-house staking distinguishes BHYP from competitors.
- **Sources:** [Bitwise Stakes $114M](https://news.bitcoin.com/bitwise-stakes-114-million-hype-hyperliquid-etf/) | [BHYP ETF](https://bitwiseinvestments.com/newsroom/bitwise-launches-spot-hyperliquid-etf-bhyp) | [AMBCrypto institutional](https://ambcrypto.com/hyperliquid-demand-deepens-as-institutions-chase-staking-yields-just-a-fad/) (June 2026)

---

### Candidate 2: ZEC/USDT — Short-Watch (Catalyst Supported)

**Tier:** C-watch | **Direction:** short | **Score:** 53.1 scalp / 51.9 intraday

- **Has price already reacted?** Yes — ZEC -6.33% (scalp data) / -5.67% (intraday). Already moving down.
- **Is setup chasing?** Short entry needs failed bounce. Current price ~384-385. Conditional retest zone: 385.25-387.60 (scalp) / 386.49-388.94 (intraday).
- **Is there a retest/pullback structure?** Yes — price down + OI up = fresh shorts pressing. If price bounces to 385-390 and fails, short trigger activates.
- **Would entry NOW be late?** Yes at current lows. Wait for retest — not new low short.
- **What level makes it actionable?** Bounce to 385.25-387.60 + 1h close rejection. Stop above 390-391.
- **Aligned with mood?** YES — risk-off, shorts preferred, relative weakness (-15% 7d), OI building on downside.
- **Actionable now?** NOT until retest. Monitor for Sunday evening bounce.
- **Invalidation:** 1h close above 391.94; BTC significant reclaim of $61k+.
- **Catalyst:** Whale shorts $4.92M (AMBCrypto); Coinbase CEO controversy with ZEC founder; OI +3.46-4.15% while price down.
- **Chase-risk:** Only if entering at current lows — wait for retest to avoid.

---

### Candidate 3: S/USDT — Best No-Catalyst Long-Watch

**Tier:** C | **Direction:** long | **Score:** 59.6 intraday / 55.8 scalp (top watchlist candidate across both reports)

- **Context:** Momentum breakout basket primary. +24-25% 24h, OI +42.51%, RS vs BTC +24.73%. Not entering: score below threshold, no catalyst verified, chop regime.
- **Has price reacted?** Yes — already ran +24%. OI building (unknown crowding).
- **Entry if triggered:** Pullback to 0.0241-0.0246 (intraday) with BTC stabilizing above $60k. Funding negative (-0.002) = shorts paying → possible squeeze fuel if BTC holds.
- **Invalidation:** 1h close below 0.0235.
- **Aligned with mood?** Partially — no catalyst. No-catalyst intraday in chop has PF=0.70/-3R historically (report playbook note). Only viable if RS-leader + volume + BTC stable.
- **Actionable?** WAITING for pullback + regime confirmation. Not this window.
- **Trigger for upgrade:** BTC reclaim $60,750 + S/USDT pullback to 0.0241-0.0246 with volume acceptance.

---

### Candidate 4: ACT/USDT — AVOID / Maximum Chase Risk

**Tier:** Rejected all reports | **Direction:** momentum long | **Score:** 43.0 intraday / 36.0 scalp (rejected)
**What is ACT:** "Act I The AI Prophecy" — Solana-based meme/AI token launched on pump.fun (Oct 2024). 99% below ATH ($0.92).

- **Has price already reacted?** Maximum yes — +99.7% RS vs BTC (intraday 10:51 data), likely extended further by 13:20. Rejected in BOTH reports: ">2ATR from EMA20; do not chase."
- **Is the setup chasing?** YES — system rejected due to overextension. Chase risk: maximum.
- **Is there a retest structure?** No — price is vertical. No retest yet.
- **Would entry NOW be late?** Yes, extremely. All system filters correctly rejected.
- **Catalyst?** No verified catalyst detected in any report. Pure momentum basket (wait_pullback playbook). Note: CoinGecko daily price ~$0.0088 (+10% 24h) — intraday move may have partially reversed.
- **Verdict:** AVOID this window. Watchlist for pullback to EMA20 zone only.

---

### Candidate 5: PUMP/USDT B Scalp (ENTERED UNRESOLVED) — Monitor Only

**Tier:** B | **Direction:** long (scalp) | **Status:** ENTERED UNRESOLVED | **Weekend=Y**

- **Context:** New B scalp signal from cycle_02. Momentum breakout basket member. +15% 24h (intraday), 2.05x volume, OI +6.28% (price up + OI up = fresh positioning). However, 13:20 scalp report rejected PUMP (score 48.8, ">2ATR from EMA20") — signal generated when price was lower.
- **Lifecycle:** ENTERED UNRESOLVED. System has the position. Monitoring for TP or stop.
- **Risk:** Scalp mode PF=1.35 (+7R) acceptable playbook. Weekend=Y penalty applies (WR 18% obs). Price now extended vs EMA20 at time of latest report.
- **Action:** No new entry. Monitor existing entered signal. If BTC breaks $59,250, this is a weekend stop candidate.

---

## 8. Best Candidates Ranked

No clean new entries this window. All 12 active signals ENTERED UNRESOLVED. No fresh A/B from today's scan threshold.

Per PART 9 (anti-over-conservatism), watch candidates with exact triggers:

| Rank | Candidate | Direction | Trigger | Reason |
|------|-----------|-----------|---------|--------|
| 1 | HYPE/USDT | **Long-watch** | Pullback $58-60 + volume + BHYP institutional floor | Strongest verified catalyst (Bitwise $114M + ETF). Institutional demand floor. |
| 2 | ZEC/USDT | **Short-watch** | Failed bounce retest 385.25-387.60 + 1h rejection (stop >391) | Whale shorts pressing, OI building, catalyst present, downtrend |
| 3 | S/USDT | **Long-watch** | Pullback 0.0241-0.0246 + BTC reclaim $60,750 + volume | Best no-catalyst watchlist. OI building. RS leader. Needs macro support. |
| 4 | PUMP/USDT (active B) | **Monitor only** | ENTERED UNRESOLVED — no new entry | Active signal, scalp mode PF=1.35. Weekend=Y. Monitor stop. |
| 5 | ACT/USDT | **Watch-only** | Wait for pullback to EMA20 zone; entry after extended move resolves | Chase risk maximum. Not enterable now. |

---

## 9. Avoid / No Trade (This Decision Window Only)

**This window only. NOT a system stop command. Scanner continues.**

- **ACT/USDT:** Chase risk maximum. >2ATR extended, rejected all reports. Watch-only until pullback.
- **All new intraday longs:** Mode PF=0.00, wins=0, -5R this week. Do not open new intraday long positions.
- **PUMP/USDT new entry:** Signal ENTERED — do not add. Price extended per 13:20 report.
- **UNH stocks (any active signals):** DOJ criminal probe. AVOID on Monday open without RTH confirmation.
- **SMCI:** Ongoing legal risk (carry-forward from previous reviews). Manual review required.
- **Weekend scalp longs without catalyst:** Weekend WR=18%. Only enter with clear RS-leader + catalyst + clean structure.
- **BEL/USDT short:** >2ATR from EMA20, score 36 (rejected). Rejected.
- **VELVET/USDT:** MEXC-only (confirmation=38%), elevated long crowding. Speculative only.

---

## 10. Main Risks

1. **BTC $59,250 breakdown:** External analysis identifies this as the critical trigger (investinglive.com Jun 28 2026). Break → Monday opens with gap-down risk across all crypto longs. Active swing long signals (BERA, SOL, HOD, ETH long, AXS, AAVE) face stop risk.
2. **Intraday mode failure ongoing:** PF=0.00, -5R this week. Two active intraday B signals (BTC short, HEI long) — BTC short is the safer; HEI long is in worst-performing playbook.
3. **Weekend liquidity:** Thin markets amplify wicks and false breakouts. All ENTERED UNRESOLVED signals face wider adverse excursion risk over the weekend.
4. **Monday gap risk — stocks:** UNH -16% DOJ probe. MSFT/COIN unmapped in catalyst events. Stock signals are 41-46h stale — revalidate all Monday pre-market before any entry.
5. **F&G = 18 (Extreme Fear):** In downtrend, extreme fear means continued downside more often than contrarian bounce. Do not fade fear alone.
6. **Reddit social 403:** Multiple cycles blocked. Social attention missing for all signals. Crowd context thin.
7. **Paper shadow 3d window:** NOT_READY (5/6 criteria). B lane shows promise (+2.38R forward) but window too short for promotion. Advisory context only.

---

## 11. Action Plan — Next 4 Hours (16:20–20:20 EEST)

1. **Monitor BTC $59,750–$60,250 support.** Hold → no action. Break of $59,250 → review all swing long signals for stop risk.
2. **Watch HYPE for pullback.** If HYPE retraces toward $58-60 zone Sunday evening, flag for potential long entry Monday with volume confirmation.
3. **Watch ZEC for failed bounce.** If ZEC bounces to 385.25-387.60 and rejects (1h close), that is the short trigger. Do not short at current lows.
4. **Let active signals run.** All 12 ENTERED UNRESOLVED. No manual closes without clear invalidation.
5. **No new intraday longs.** Mode PF=0.00 this week. The BTC short and ETH short are the active intraday signals — monitor but do not add.
6. **Prepare Monday watchlist.** UNH AVOID. SMCI MANUAL REVIEW. Recheck all stock signals against fresh Monday pre-market data (41h stale now). Check stocks gap risk at Monday open.
7. **Scanner keeps running.** Next cycle expected Monday morning. Crypto monitor running in background (pid 18184 from cycle_02).

---

## 12. Final Verdict Per Mode

| Mode | Verdict | Action |
|------|---------|--------|
| Scalp | CAUTION (weekend mode) | PUMP B ENTERED UNRESOLVED only. No new scalp entries without pullback + clear trigger |
| Intraday | AVOID new longs | PF=0.00/-5R this week. BTC short ENTERED: ok. HEI long ENTERED: monitor for stop. No new entries |
| Swing | WATCH ONLY | Best performing (PF=2.06/+16R). 10 active swing signals ENTERED UNRESOLVED. No new entries — wait for cycle_03 fresh scan Monday |
| Crypto overall | CAUTION / catalyst-backed | Prefer HYPE on pullback; ZEC short on retest; avoid extended momentum (ACT) and intraday longs |
| Stocks | PLANNING ONLY | Closed (Sunday). Monday pre-open review required. UNH AVOID. All signals 41-46h stale — revalidate Monday. |

---

## 13. Sources

External sources cited (retrieved 2026-06-28 ~16:20 EEST):

- [Bitcoin analysis over the weekend, 28 June 2026 — investingLive](https://investinglive.com/Cryptocurrency/bitcoin-analysis-over-the-weekend-28-june-2026-20260628/) — BTC structure, key levels, 200-week MA context (published 2026-06-28; verification: primary_source; confirms: BTC bearish structure, key levels $59,250 / $60,750-61,000)
- [BTC Price Plunges to $59K, $1B Liquidations — Bitcoin Foundation](https://bitcoinfoundation.org/news/bitcoin/crypto-market-june-25/) — Jun 25 liquidation context (published 2026-06-25; verification: single_source; confirms: macro pressure, $59k low)
- [Hyperliquid demand deepens as institutions chase staking yields — AMBCrypto](https://ambcrypto.com/hyperliquid-demand-deepens-as-institutions-chase-staking-yields-just-a-fad/) — HYPE institutional context (published ~June 2026; verification: single_source; confirms: narrative_supported)
- [Bitwise Launches Spot Hyperliquid ETF (BHYP) — Bitwise Investments](https://bitwiseinvestments.com/newsroom/bitwise-launches-spot-hyperliquid-etf-bhyp) — BHYP ETF official announcement (verification: primary_source; confirms: BHYP live NYSE + Xetra)
- [Bitwise Stakes $114 Million in HYPE on Hyperliquid — Bitcoin.com News](https://news.bitcoin.com/bitwise-stakes-114-million-hype-hyperliquid-etf/) — $114M staking event (published June 2026; verification: single_source; confirms: 1.775M HYPE deposited+staked)
- [Bitwise Stacks Hyperliquid — The Coin Republic](https://www.thecoinrepublic.com/2026/06/02/bitwise-stacks-hyperliquid-as-projections-on-hype-price-breakout-grows/) — earlier accumulation context (published 2026-06-02; verification: single_source)
- Internal: `data/reports/scalp/2026-06-28_13-20_scalp_report.md` (generated 16:20 EEST)
- Internal: `data/reports/intraday/2026-06-28_10-51_intraday_report.md` (13:51 EEST)
- Internal: `data/catalysts/2026-06-28/catalyst_cycle_10-51.md` (10:51 EEST)
- Internal: `data/scheduled_runs/2026-06-28_default_schedule/cycle_02_12-56_summary.md` (13:56 EEST)
- Internal: CLI `active-signals --asset-class crypto` (live 16:20 EEST)
- Internal: CLI `signal-stats --asset-class crypto` (live 16:20 EEST)

*ZEC catalyst sources (AMBCrypto whale shorts, CryptoBriefing Coinbase controversy) found in internal news_items via scalp/intraday reports §5. Publication dates noted as June 2026 per report ingestion; not independently re-fetched this run. Verification: news_mention.*

---

## 14. Fix Requests / TODO

### TODO-INTRADAY-MODE-PF-ZERO
- **issue:** Intraday mode PF=0.00, wins=0 from 5 losses this week (-5R total). Two active intraday signals (BTC short, HEI long) are entered. The mode is the worst-performing bucket by a large margin.
- **evidence:** `signal-stats --asset-class crypto` cycle_02 step 21: mode_1 n=45, triggered=34, wins=0, losses=5, PF=0.00, totalR=-5.00R
- **suggested manual fix:** Manual review session: audit intraday entry conditions, score thresholds, TP distances, and no-catalyst performance (playbook note says no-catalyst intraday in chop is net-negative). Consider temporarily requiring A-tier threshold for new intraday entries, or pausing new intraday signal generation until root cause identified.
- **priority:** high
- **first observed:** 2026-06-28 16:20 EEST

### TODO-REDDIT-403-BLOCKED
- **issue:** Reddit social sources (r/CryptoCurrency, r/Bitcoin, r/Ethereum) returning 403 errors across multiple consecutive cycles. Social attention layer consistently missing.
- **evidence:** cycle_02 steps 2+3: `WARNING Failed social source Reddit CryptoCurrency: 403 Client Error: Blocked` (repeated in both scalp and intraday build steps)
- **suggested manual fix:** Replace Reddit endpoints with valid Reddit API v2 access pattern, or substitute with alternative social sources (Stocktwits, CryptoCompare social, LunarCrush). Log persistent 403 as recurring error rather than warning.
- **priority:** medium
- **first observed:** 2026-06-28 16:20 EEST (observed in multiple prior cycles)

### TODO-CATALYST-SYMBOL-MAPPING-GAP
- **issue:** 13 high-importance symbol-tagged catalysts not mapped into catalyst_events: ADA, ALGO, AVAX, COIN, DOT, FIL, HBAR, INJ, MSFT, TON. Signals for these symbols lack catalyst context.
- **evidence:** cycle_02 step 5 (catalyst integrity scan): `WARNING: 13 high-importance symbol-tagged catalysts not mapped into catalyst_events: ADA, ALGO, AVAX, COIN, DOT, FIL, HBAR, INJ, MSFT, TON`
- **suggested manual fix:** Audit symbol_resolver in catalyst layer. Check ticker alias or exchange symbol mismatch (e.g. INJ might map to a different key). This is a recurring integrity warning that reduces catalyst coverage precision.
- **priority:** medium
- **first observed:** 2026-06-28 16:20 EEST (recurring)

### TODO-TELEGRAM-SHADOW-DIGEST-CONFIG
- **issue:** Paper-shadow A/B Telegram digest fails with `TelegramNotifier.__init__() missing 1 required positional argument: 'config_path'`. Digest NOT SENT. This is distinct from the working paper_monitor_status Telegram (step 25 sends OK).
- **evidence:** cycle_02 step 14 stdout: `send error: TelegramNotifier.__init__() missing 1 required positional argument: 'config_path'`
- **suggested manual fix:** Fix TelegramNotifier instantiation in the paper-shadow digest script to pass config_path argument (likely `config/telegram.yaml` or equivalent). Compare with working instantiation pattern in paper_monitor_status script.
- **priority:** medium
- **first observed:** 2026-06-28 16:20 EEST

### TODO-ONCHAIN-CONFIG-MISSING
- **issue:** On-chain data layer reports `interface_ready_config_missing` with configured=false every cycle. On-chain whale flows, exchange inflow/outflow unavailable. This is a persistent blind spot.
- **evidence:** cycle_02 step 18 intelligence_layer: `"onchain": {"status": "interface_ready_config_missing", "cached_symbols": 0}`
- **suggested manual fix:** Create `config/onchain.yaml` with on-chain data provider credentials. Minimum viable: BTC exchange flow metrics from Glassnode/Nansen/CryptoQuant. Even a basic free-tier connection would improve signal quality materially.
- **priority:** low
- **first observed:** Recurring across multiple review cycles
