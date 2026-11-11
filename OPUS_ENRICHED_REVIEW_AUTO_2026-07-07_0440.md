---
REVIEW: OPUS ENRICHED REVIEW — ⚠ ADVISORY ONLY — NO EXECUTION
SLOT: Crypto Overnight / Asia Review · 2026-07-07 · 04:30 EEST
WRITTEN: 2026-07-07 04:40 EEST
PREV REVIEW: 2026-07-06 23:15 EEST (post-close final daily review)
STATUS: AUTOMATED SCHEDULED RUN — NO HUMAN IN SESSION
---

# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:40 EEST

## 1. Executive Summary

**Slot: crypto overnight / Asia review — advisory only / no auto-trade.**

BTC and ETH remain in uptrend, altcoin breadth at 65.12% above EMA20 — regime is **bullish trend / risk-on** as confirmed by the freshest cycle (01:42 EEST scalp report, data freshness 04:30 EEST). The Asia tape is constructive: RS leaders from last session (YFI +44% 24h, VANRY +33%, PYTH +10%, BEL +20%) are holding or consolidating. No A-tier signals generated. Seven B-tier longs exist in the intraday bucket, all no-catalyst momentum — their known failure mode (WR 23% / PF 0.70 no-news 14d) applies.

**Asia dead-zone is ACTIVE** (03:00–09:00 EEST / 00:00–06:00 UTC). New crypto scalp and intraday proposals are auto-demoted to C during this window. Existing triggered signals remain open. Await dead-zone clearing (09:00 EEST / 06:00 UTC) before treating any intraday idea as actionable.

**Key positives overnight**: Ripple secured a full MiCA CASP license across 30 EEA countries — regulatory milestone for XRP. FOMC Clarity Act odds improving (Bitmine framing). PART 1 regression resolved: 0 untracked alerts today vs 24 yesterday. No new A/B short proposals — correct for the bullish tape.

**Key risks**: FOMC minutes release July 8 (~14:00 ET) — reduce new swing sizing. SOL and ETH carry operator-review warnings (BONK governance $20M drain, UXLINK hacker). VANRY still flagged with Binance monitoring tag (July 3).

**Best ideas for Europe open**: PYTH/USDT (pullback to 0.0444–0.0450 entry zone, RS + RWA narrative, fresh OI), XRP/USDT (catalyst-backed MiCA license, wait for structure). NEAR/USDT C-tier watch at 2.030–2.048 (AI narrative, no fresh catalyst but confirmed waiting zone from prior review).

---

## 2. Data Used

| Source | File / Timestamp | Age at 04:40 EEST | Quality |
|--------|-----------------|-------------------|---------|
| Scalp report | `data/reports/scalp/2026-07-07_01-42_scalp_report.md` | ~3h (data 04:30) | **FRESH** ✓ |
| Intraday report | `data/reports/intraday/2026-07-06_23-59_intraday_report.md` | ~1.7h (data 02:45) | **FRESH** ✓ |
| Swing report | `data/reports/swing/2026-07-06_14-19_swing_report.md` | ~11h | **STALE** ⚠ (use swing signal carry-forward only) |
| Stocks intraday | `data/reports/stocks/intraday/2026-07-07_00-07_stocks_intraday_report.md` | ~4.5h | **CARRY-FORWARD** (US closed) |
| Stocks swing | `data/reports/stocks/swing/2026-07-02_13-03_stocks_swing_report.md` | 5 days | **STALE** ⚠ (exclude from decisions) |
| Stocks invest | `data/reports/stocks/invest/2026-07-02_13-05_stocks_invest_report.md` | 5 days | **STALE** ⚠ |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-06_2315.md` | ~5.5h | CONTEXT |
| Active signals (crypto) | CLI `active-signals --class crypto` | ~0m | LIVE (44 signals) |
| Active signals (stocks) | CLI `active-signals --class stocks` | ~0m | LIVE (50 signals, all C) |
| Signal stats (crypto) | CLI `signal-stats --class crypto` | ~0m | LIVE |
| Signal stats (stocks) | CLI `signal-stats --class stocks` | ~0m | LIVE |
| Untracked alerts | CLI `detect_untracked_legacy_alerts --since 2026-07-07` | ~0m | LIVE (0 alerts ✓) |
| Catalyst cycle | `data/catalysts/2026-07-07/catalyst_cycle_01-48.md` | ~1h | FRESH |
| Catalyst events | `data/catalysts/2026-07-07/catalyst_events.jsonl` | 4:48 EEST | FRESH |

**Notes:**
- TradingView / manual chart check unavailable. All technical observations from local OHLCV / ATR / EMA fields only.
- External web research not performed (internal data complete and consistent for all key candidates).
- Swing report shows "transition/mixed" regime from 14:15 UTC July 6 — superseded by scalp/intraday bullish trend reading. Treated as STALE.

---

## 3. Scheduler / Data Freshness

- **Last completed cycle**: `data/scheduled_runs/2026-07-07_default_schedule/` — mtime 04:35 EEST (5 min before this review)
- **Scheduler health**: FRESH. Run completed <10 min ago.
- **Data freshness**:
  - Scalp OHLCV: fresh at ~04:30 EEST (~10 min old)
  - Intraday OHLCV: fresh at ~02:45 EEST (~2h old)
  - Swing: STALE (17:15 EEST July 6, 11h old) — carry swing signals only
  - Stocks: closed session; planning context only until US open
- **Staleness flags**:
  - Swing report STALE — regime was "transition/mixed" at July 6 14:15 UTC; overridden by scalp/intraday bullish trend
  - Stocks swing/invest: 5 days old — exclude from actionable decisions
  - Social attention: missing (Reddit 403 errors)
  - Onchain: `interface_ready_config_missing` — no `config/onchain.yaml`
  - Reuters Business RSS: still failing
  - KOL placeholder not replaced
- **Asia dead-zone**: ACTIVE — 03:00–09:00 EEST / 00:00–06:00 UTC. New crypto scalp/intraday proposals → C for ~4.3 more hours (dead-zone clears at 09:00 EEST)
- **PART 1 regression**: RESOLVED — 0 untracked alerts today (was 24 at 23:15 EEST July 6 — significant improvement)
- **Paper portfolio**: bybit_non_vip net +$1,658 / +33.2% / maxDD 13.43% (818 deduped trades); shadow A/B forward NOT_READY (DATA_GAP_LATE 40%)

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-07 04:40 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "social_attention_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Scheduler last run 04:35 EEST (5m ago)",
        "Scalp report FRESH (data 04:30 EEST)",
        "Intraday report FRESH (data 02:45 EEST, ~2h ago)",
        "Swing report STALE (data 17:15 EEST Jul 6, ~11h ago)",
        "No onchain.yaml config — whale/exchange flows blind",
        "Social attention missing (Reddit 403, no KOL live)"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: uptrend (confirmed scalp + intraday)",
        "ETH trend: uptrend",
        "Altcoin breadth: 65.12% above EMA20, 79.07% above EMA50",
        "BTC ATR percentile: 39 (normal volatility, not extended)",
        "Style: selective longs; prefer pullbacks on relative strength"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["no_catalyst", "narrative_supported", "mapping_weak"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "500 catalyst events today, 5-6 baskets",
        "JSONL sample >50% unmapped (stocks feed dominated by general news/legal)",
        "Top longs (PYTH, YFI, VANRY, DEXE, BEL) have NO fresh verified catalyst",
        "Positive: XRP MiCA license (30 EEA), ETH Clarity Act/Bitmine $74M",
        "Risk: SOL (BONK governance attack $20M), ETH (UXLINK hacker)",
        "AI/RWA/BNB/perps_dex baskets active with NEAR, TAO, FET, RENDER, ONDO/XLM, BNB, HYPE"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["oi_supports", "funding_extreme"],
      "data_missing": ["oi_24h_missing_for_vanry_hmstr_bel_zro_dexe_yfi"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "YFI: negative funding all venues (Bybit -0.074%, OKX -0.1%, MEXC -0.066%) — crowded shorts squeezed on +44% move",
        "BLUR: strongly negative funding all venues (-0.5% to -1.06%) — elevated crowding",
        "PYTH: positive funding 5e-05, OI +2.14% — fresh positioning, normal crowding",
        "VANRY: mixed funding, OI data unavailable (MEXC fallback only)",
        "DEXE/ZRO/BEL/HMSTR: MEXC fallback only, OI unavailable"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["chase_risk", "clean_retest"],
      "data_missing": ["tradingview_chart_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "PYTH: current 0.0453, entry zone 0.0444-0.0450 (price slightly above, ~0.2ATR)",
        "YFI: current 2710, entry zone 2599-2676 (above zone by 34-111 pts, ~0.5ATR)",
        "VANRY: current 0.0075, entry zone 0.0069-0.0073 (above zone by 3-9%, chase risk)",
        "DEXE: current 27.771, entry zone 27.313-27.630 (within 0.2ATR of upper entry)",
        "NEAR: C-tier waiting at zone 2.030-2.048 (clean zone, no chase)",
        "BLUR: rejected overextended (>2ATR from EMA20, +43% 24h)"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto: 44 active B-tier signals total",
        "OPEN / triggered: ~10 (BLUR x2, ZRO x2, YFI x2, SOL, DEXE x2, BTC intraday)",
        "WAITING FOR ENTRY: 2 (JTO intraday, ALLO intraday)",
        "TP-hit / partial: ~32 (prior cycle wins in swing/intraday)",
        "Stocks: 50 C-tier all WAITING (US closed, planning only)",
        "Untracked alerts: 0 (improved from 24 at last night's post-close)",
        "Asia dead-zone ACTIVE until 09:00 EEST: new scalp/intraday proposals demoted to C"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["headline_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "FOMC minutes July 8 14:00 ET — reduce new swing sizing ahead of release",
        "SOL: block_requires_operator_review (BONK governance attack, $20M drained)",
        "ETH: block_requires_operator_review (UXLINK hacker 14,336 ETH transfers)",
        "HYPE: block_requires_operator_review (fake HyperSwap airdrop $12,300 drained)",
        "APT: token_unlock risk_warning (Token Unlocks July week 2)",
        "VANRY: Binance monitoring tag active (from July 3 prior review)"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["playbook_working", "playbook_failing"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto week: WR 15.1%, PF 1.67, +45.4R (n=388, reliable confidence)",
        "By mode: Scalp -6.6R (kill-switch active) / Intraday +27.8R / Swing +24.1R",
        "Scalp kill-switch ACTIVE (crypto_scalp_disabled) — no new proposals",
        "No-catalyst intraday 14d: WR 23% / PF 0.70 / -3R — applies to all current B-tier",
        "Stocks A/B: PF 0.44 / -9R all tiers this week; drawdown guards active, all C",
        "Stocks intraday guard: -3.0R / PF 0.00 this week"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Regime bullish trend risk-on confirmed by two fresh reports",
        "Asia dead-zone active until 09:00 EEST: await clearing before new intraday entry",
        "Best long: PYTH/USDT pullback to 0.0444-0.0450 after dead-zone",
        "Best short: MUB/USDT — wait failed bounce + derivatives in bullish tape",
        "Best catalyst: XRP/USDT — Ripple MiCA license, pullback to support",
        "Avoid: VANRY (monitoring), BLUR (overextended + funding elevated)"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.75,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "PYTH/USDT",
      "trigger": "Pullback to 0.0444-0.0450 after 09:00 EEST dead-zone clears; BTC must hold uptrend; volume expansion on retest",
      "reason": "Best RS B-tier with RWA narrative, fresh OI, normal crowding; entry near zone; no chase"
    },
    "best_short_candidate": {
      "symbol": "MUB/USDT",
      "trigger": "Failed bounce above current levels + derivatives data available + BTC loses local support",
      "reason": "Weakest RS -7.9% vs BTC; rejected overextended + bullish tape; requires specific confirmation before shorting"
    },
    "best_catalyst_candidate": {
      "symbol": "XRP/USDT",
      "trigger": "Pullback to support + volume confirmation + fresh catalyst_events for MiCA follow-through",
      "reason": "Ripple full MiCA CASP license across 30 EEA countries — confirmed regulatory milestone, positive for EU institutional access"
    },
    "avoid_candidate": {
      "symbol": "VANRY/USDT",
      "reason": "Binance monitoring tag active (July 3), +149% 7d overextended, volume 0.33x, entry zone well below current price — chase risk + regulatory flag"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason Codes | Suggested Effect |
|-------|---------|-----------|--------------|-----------------|
| data_quality | **ok** | 0.82 | scheduler_fresh, report_stale | advisory_only |
| market_regime | **ok** | 0.85 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | **caution** | 0.65 | no_catalyst, narrative_supported, mapping_weak | advisory_only |
| derivatives_squeeze | **caution** | 0.70 | oi_supports, funding_extreme | advisory_only |
| technical_entry | **caution** | 0.68 | chase_risk, clean_retest | advisory_only |
| execution_lifecycle | **ok** | 0.75 | open_actionable, waiting_for_entry | advisory_only |
| risk_manager | **caution** | 0.78 | headline_risk, manual_review | advisory_only |
| playbook_performance | **ok** | 0.80 | playbook_working, playbook_failing | advisory_only |
| head_trader | **ok** | 0.75 | risk_on, longs_preferred, wait_for_trigger | advisory_only |

**Council summary**: 4 ok / 4 caution / 0 bad. Risk-on bias confirmed. Caution flags: no catalyst on top longs (historical failure mode), YFI/BLUR elevated funding, mild chase on YFI/VANRY, FOMC risk + operator flags on SOL/ETH. Head trader: **normal** overall, preferred side **longs**, Asia dead-zone reduces urgency.

---

## 4. What Changed vs Previous Review

Previous review: post-close final daily review, 2026-07-06 23:15 EEST.

| Change | Detail |
|--------|--------|
| ✅ PART 1 regression RESOLVED | 0 untracked alerts today vs 24 at 23:15 — significant improvement |
| ✅ Asia dead-zone activated | As expected at 03:00 EEST; scalp/intraday demoted to C |
| 🔄 Fresh scalp report | 04:42 EEST — confirms bullish trend still intact overnight |
| 🔄 New catalyst scan | 500 events, 5-6 baskets for July 7 |
| ↗ PYTH/USDT top intraday | Score 73.7 — now top B-tier for Europe open watch |
| ↔ NEAR/USDT still waiting | C-tier, entry zone 2.030–2.048; overnight setup from prior review valid |
| ↔ YFI/USDT still in play | B-tier triggered; negative funding across all venues; chase risk slightly higher |
| ↔ VANRY monitoring flag | July 3 Binance monitoring tag persists |
| ✅ XRP MiCA license: new catalyst | Not in prior review; Ripple MiCA CASP authorized — new catalyst-backed idea |
| ⚠ FOMC reminder | July 8 14:00 ET — reduce new swing sizing |
| ⚠ SOL/ETH/HYPE flags | Operator review flags unchanged |

No signals invalidated since 23:15. No thesis reversals. Market continued constructively overnight.

---

## 5. Catalyst Coverage

- **Total catalyst events today**: 500 (cycle 01-48, July 7)
- **Narrative baskets**: 5–6 (binance_ecosystem_teaser, rwa_narrative, ai_narrative, delisting_thin_liquidity, perps_dex_narrative)
- **Mapping rate**: JSONL sample (first 20 rows) shows >50% unmapped; dominated by stocks general news, legal filings without symbol tags
- **⚠ CATALYST MAPPING WEAK THIS RUN — use catalyst layer as context, not final decision.**
  - Top unmapped headlines: "Bleichroeder Acquisition Corp. III IPO $300M," "3 Networking Chip Stocks Riding AI Data Center Boom," "Stock Market Today July 6: Semiconductor Momentum"
  - Crypto catalysts are mapped: XRP (MiCA), BTC (Strategy sale + Bitmine), ETH (Clarity Act), SOL (BONK exploit), ZEC (whale short)

**Active baskets this cycle:**

| Basket | Playbook | Primary | Freshness |
|--------|----------|---------|-----------|
| binance_ecosystem_teaser | related_beta_rotation | BNB/USDT, ASTER/USDT | <24h |
| rwa_narrative | related_beta_rotation | ONDO/USDT, XLM/USDT | <24h |
| ai_narrative | related_beta_rotation | NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT | <24h |
| delisting_thin_liquidity | avoid_low_liquidity | — | <1h |
| perps_dex_narrative | wait_pullback | HYPE/USDT | <24h |

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood**: risk-on / bullish trend
- **Stocks mood**: closed (US after-hours); prior session bullish (Dow >53,000, NASDAQ semiconductor-led); planning/carry-forward only
- **Dominant narrative**: RS-leader momentum (YFI, VANRY, PYTH altcoin leaders); regulatory positive (XRP MiCA); AI/RWA baskets active
- **Preferred side now**: longs — pullbacks on RS leaders after dead-zone clears (09:00 EEST)
- **Best long candidate**: PYTH/USDT — pullback to 0.0444–0.0450, after dead-zone (trigger: 09:00 EEST + BTC stable)
- **Best short candidate**: MUB/USDT — weakest RS; trigger: failed bounce + derivatives data + BTC support loss (not actionable yet)
- **Best catalyst-backed candidate**: XRP/USDT — Ripple MiCA license; trigger: pullback to support + volume confirmation
- **What to avoid**: VANRY (monitoring + 149% 7d chase), BLUR (>2ATR + elevated negative funding), SOL/ETH/HYPE (operator review required)
- **What would change the view**: BTC breaks daily support; Asia session triggers unexpected macro shock; altcoin breadth drops below 50% EMA20

---

## 7. Candidate Deep Dives

### Candidate #1 — PYTH/USDT (B-tier, intraday, LONG — WATCH until 09:00 EEST)

**Status**: OPEN ACTIONABLE (triggered); Asia dead-zone → WATCH ONLY until 09:00 EEST

- Score: 73.7/100 (intraday); 24h +10–12%; 7d +25.35%; RS vs BTC +11.39%
- Volume: 1.07x (above average — positive)
- Derivatives: OI +2.14% (fresh positioning), funding 5e-05 (normal), L/S 1.293 (normal crowding)
- Narrative: RWA basket member (heat 38.4, mixed)
- Entry zone: 0.0444–0.0450; Current: 0.0453 (0.3% above upper zone = NOT chasing)
- Invalidation: 1h close below 0.0436 | TP1: 0.0467 / TP2: 0.0481 / TP3: 0.0495 | ATR: 0.0014
- **Chase check**: NO — price just 0.3% above entry upper; normal pullback gets us in zone
- **Catalyst**: No fresh catalyst. Known failure mode: no-catalyst intraday WR 23%/PF 0.70. Await volume on retest.
- **Dead-zone**: C until 09:00 EEST. WATCH ONLY now; re-evaluate at 09:00 for Europe session.

---

### Candidate #2 — YFI/USDT (B-tier, intraday + scalp, LONG — WAIT FOR PULLBACK)

**Status**: OPEN / TRIGGERED (both modes active); Asia dead-zone → shadow

- Score: 67.9/100 (intraday); 24h +44.61%; 7d +64.84%; RS vs BTC +44.01%
- Volume: 1.21x (healthy); Funding: negative all venues (Bybit -0.074%, OKX -0.1%) — crowded shorts squeezed
- Entry zone: 2,599–2,676; Current: ~2,710 (above zone by 0.5ATR — mild chase)
- Invalidation: 1h close below 2,506 | TP1: 2,880 / TP2: 3,050 / TP3: 3,220 | ATR: 170
- **Chase check**: MILD RISK — 34–111 pts above entry zone. Big +44% move already made without catalyst.
- **Squeeze dynamics**: Negative funding = shorts paying longs. Bullish but late-squeeze entry risk.
- **Dead-zone + guidance**: DO NOT CHASE AT 2,710+. Wait for pullback to 2,599–2,676. Not for Asia dead-zone period.

---

### Candidate #3 — NEAR/USDT (C-tier watchlist, intraday, LONG — WATCH)

**Status**: WAITING FOR ENTRY (C-tier; not Telegram-actionable)

- Score: 56.1/100; 24h +1.93%; 7d +10.24%; RS vs BTC +1.33%; Volume 0.41x (below avg)
- Narrative: AI basket primary (NEAR, ai_narrative active)
- OI down (short covering, weaker quality); crowding normal
- Entry zone: 2.030–2.048; Price: ~2.056 (at zone edge); Invalidation: 1h close below 2.009
- **Chase check**: NO — waiting at zone, no chase
- **Catalyst**: AI basket soft support; no specific NEAR catalyst verified
- **Note**: Was best overnight setup from 23:15 review; still valid as watchlist. C-tier = NOT Telegram-actionable.

---

### Candidate #4 — XRP/USDT (Catalyst-backed WATCH — no current signal)

**Status**: REVIEW / SHADOW — catalyst-backed watch; no B-tier signal this cycle

**Catalyst** (internal, verified):
- Ripple full **MiCA CASP license** for crypto services across **30 EEA countries** (The Block, Cointelegraph, July 7)
- XRP Binance Scarcity Index at 2-year high (BeInCrypto)
- Verification: single_source (two independent outlets confirming)

**Why**: MiCA CASP is a tier-1 regulatory milestone — Ripple can operate across all EU/EEA legally. European institutional demand catalyst. Not yet scored into a B-tier signal (volume 0.5x below threshold, current cycle).
**Action**: WATCH. If XRP pulls back to support and cycle rescan upgrades to B-tier, this becomes the cleanest catalyst-backed idea.
**Chase**: Do not chase without entry structure and volume confirmation.

---

### Candidate #5 — MUB/USDT (SHORT watch — currently REJECTED, not actionable)

**Status**: REJECTED (both scalp and intraday); not actionable

- Score: 22.7/100 (scalp) / 15.4/100 (intraday); 24h -7.55%; RS vs BTC -7.96%
- Volume: 1.47x unusual (scalp); No futures data available
- **Why not**: >2ATR from EMA20 (overextended), no derivatives, fights bullish tape, squeeze risk flags
- **Trigger for actionable short**: Price bounces back into 2ATR zone + BTC breaks down + derivatives data appears + volume expansion confirms rejection. Multi-condition, not imminent.

---

## 8. Best Candidates Ranked

No "enter now" candidates — Asia dead-zone active + all top longs are no-catalyst momentum (known failure mode).

| Rank | Symbol | Direction | Tier | Status | Trigger |
|------|--------|-----------|------|--------|---------|
| 1 | **PYTH/USDT** | Long | B | WATCH (dead-zone) | Pull to 0.0444–0.0450 AFTER 09:00 EEST |
| 2 | **YFI/USDT** | Long | B | OPEN (wait for pull) | Pullback to 2,599–2,676; no chase at 2,710+ |
| 3 | **XRP/USDT** | Long | Watch | Catalyst-backed | Pullback to support + volume; MiCA confirmed |
| 4 | **NEAR/USDT** | Long | C | WAITING | Zone 2.030–2.048; watchlist only, NOT actionable |
| 5 | **MUB/USDT** | Short | Watch | REJECTED | Failed bounce + BTC breakdown + deriv data |

**Best long-watch**: PYTH/USDT — trigger: pullback to 0.0444–0.0450 after dead-zone clears (09:00 EEST)
**Best short-watch**: MUB/USDT — trigger: failed bounce + derivatives + BTC loses support (multi-condition, not now)
**Best catalyst-watch**: XRP/USDT — trigger: pullback to support + volume + fresh cycle rescan upgrade

---

## 9. Avoid / No Trade (This Decision Window Only)

**Current window (04:40–09:00 EEST)**: Asia dead-zone active → NO new crypto scalp/intraday entries regardless of setup quality.

**Specific avoids:**
- **VANRY/USDT**: Binance monitoring tag, +149% 7d chase, volume 0.33x. Do not enter.
- **BLUR/USDT**: +43% 24h, >2ATR overextended, very negative funding (elevated crowding). Avoid.
- **SOL/USDT**: operator_review required (BONK governance attack). New entry blocked pending review.
- **BONK/USDT**: Governance attack + thin liquidity + squeeze risk. Avoid both sides.
- **ETH/USDT**: operator_review required (UXLINK hacker). Existing signals may continue; no new A/B.
- **HYPE/USDT**: Fake airdrop exploit. Operator review required.
- **Stocks (all)**: US closed; all 50 signals C-tier; planning only until pre-market/open.

*This restriction applies to this decision window only. Scanner, data collection, and tracking always continue.*

---

## 10. Main Risks

1. **FOMC minutes July 8 14:00 ET**: Hawkish surprise → crypto risk-off. Reduce new swing sizing before release.
2. **No-catalyst intraday failure mode**: WR 23%/PF 0.70/−3R (14d) applies to ALL current B-tier longs.
3. **Operator-review flags active**: SOL, ETH, HYPE — do not size without manual review.
4. **Asia dead-zone 4+ more hours**: Scalp/intraday shadow until 09:00 EEST; any breakout before then disadvantaged.
5. **YFI/BLUR elevated negative funding**: Short-squeeze dynamics — if BTC reverses, unwind could be sharp.
6. **Swing report stale**: No fresh swing analysis since 11h ago; carry-forward only for swing decisions.
7. **APT token unlock**: July week 2 unlock risk — avoid.
8. **Catalyst mapping >50% unmapped**: Catalyst layer stocks context only; crypto baskets more reliable.
9. **Social/KOL blind**: Reddit blocked, no live KOL feeds; crowd context thin.
10. **Onchain blind**: No `config/onchain.yaml` — whale flows, exchange inflows completely missing.

---

## 11. Action Plan — Next 4 Hours

| Time (EEST) | Action |
|------------|--------|
| 04:40–09:00 | **MONITOR ONLY** — Asia dead-zone. Watch BTC/ETH hold support. Monitor PYTH pullback to 0.0444 zone. Check YFI for pullback to 2,600–2,676 zone. |
| 09:00 | **Dead-zone clears** — re-evaluate PYTH and YFI for intraday entry. Require volume on retest. |
| 09:00–11:30 | Europe session. Check fresh scalp/intraday cycle. Evaluate PYTH at entry zone. XRP catalyst-watch — monitor for pullback structure. |
| Before 11:30 | NEAR/USDT watchlist: if dips to 2.030–2.048 with AI narrative confirmation, flag for next cycle. C-tier, not actionable. |
| All hours | Scanner + catalyst + tracking always ON (ALWAYS-SCAN rule). |

---

## 12. Final Verdict per Mode

| Mode | Verdict | Reason |
|------|---------|--------|
| Crypto scalp | **INACTIVE** | Kill-switch active (crypto_scalp_disabled). No proposals. |
| Crypto intraday | **WATCH — dead-zone** | Active until 09:00 EEST. Post-zone: PYTH pullback top watch. No-catalyst failure mode applies. |
| Crypto swing | **CARRY-FORWARD** | Swing report stale. Carry existing signals. Reduce new sizing (FOMC July 8). |
| Stocks intraday | **PLANNING ONLY** | US closed. All 50 signals C-tier; drawdown guard -3.0R/PF 0.00 this week. |
| Stocks swing | **STALE / PLANNING** | 5 days old. Carry-forward context only. |
| Stocks invest | **INACTIVE** | Not implemented, report stale. |

---

## 13. Sources

- [Ripple MiCA license — Cointelegraph](https://www.cointelegraph.com) — "Ripple secures full MiCA license for crypto services across Europe" — July 7, 2026 (internal news_items)
- [Ripple MiCA CASP — The Block](https://www.theblock.co) — "Ripple secures full MiCA CASP authorization for crypto services across 30 EEA countries" — July 7, 2026 (internal news_items)
- [BONK governance attack — Decrypt](https://www.decrypt.co) — "Solana Meme Coin Bonk Treasury Drained of $20 Million in 'Malicious' Governance Attack" — July 7, 2026 (internal news_items)
- [Bitmine $74M ETH / Clarity Act — Cointelegraph](https://www.cointelegraph.com) — "Bitmine announces $74M Ether buys as chair says greater chances of Clarity Act passage" — July 7, 2026 (internal news_items)
- [Strategy BTC sale — Cointelegraph](https://www.cointelegraph.com) — "Strategy sells $216M Bitcoin, Bollinger bullish on BTC: Hodler's Digest" — July 7, 2026 (internal news_items)
- [XRP Scarcity Index — BeInCrypto](https://www.beincrypto.com) — "XRP Binance Scarcity Index Hits 2-Year High" — July 7, 2026 (internal news_items)
- [ETH UXLINK hacker — AMBCrypto](https://www.ambcrypto.com) — "UXLINK hacker's 14,336 ETH transfers raise fresh questions for DeFi" — July 7, 2026 (internal news_items)
- Internal: `data/reports/scalp/2026-07-07_01-42_scalp_report.md`
- Internal: `data/reports/intraday/2026-07-06_23-59_intraday_report.md`
- Internal: `data/catalysts/2026-07-07/catalyst_cycle_01-48.md`
- Internal: `python -m src.cli active-signals` (live, 04:40 EEST)
- Internal: `python -m src.cli signal-stats` (live, 04:40 EEST)
- Internal: `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-07` (0 alerts)

---

## 14. Fix Requests / TODO

### TODO-catalyst-mapping
- **issue:** Catalyst mapping >50% unmapped in aggregate (JSONL sample: 18/20 stocks entries have empty symbol field). Prevents catalyst layer from contributing meaningfully to stock setups.
- **evidence:** `data/catalysts/2026-07-07/catalyst_events.jsonl` first 20 rows, 18 have symbol=""; crypto section has only 6 symbol-specific entries.
- **suggested manual fix:** Audit symbol resolver in catalyst layer; improve entity-to-ticker mapping for PR Newswire / Motley Fool stocks feed; add ticker-extraction regex pass.
- **priority:** medium
- **first observed:** 2026-07-07 04:40 EEST

### TODO-swing-report-staleness
- **issue:** No swing report generated since July 6 17:19 EEST (~11h). Swing analysis carry-forward only. Regime was "transition/mixed" at last swing scan; scalp/intraday now confirm bullish trend — discrepancy unresolved until next swing scan.
- **evidence:** `data/reports/swing/2026-07-06_14-19_swing_report.md` mtime 7/6/2026 5:19 PM; no newer file.
- **suggested manual fix:** Verify swing scheduler step frequency; consider triggering swing scan more frequently to keep regime reads aligned.
- **priority:** low
- **first observed:** 2026-07-07 04:40 EEST
