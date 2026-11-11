# Opus Enriched Review — US Open Reaction Review — Auto Cycle 18:39 EEST

_Generated 2026-06-23 18:39 EEST (Tuesday). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

---

## 1. Executive Summary

**Tue 2026-06-23, 18:39 EEST — US open reaction review — advisory only / no auto-trade.**

- **SLOT: US open reaction review.** ~2 hours into US cash session (opened 16:30 EEST / 09:30 ET).
- **DEFINING EVENT: Global semiconductor selloff.** KOSPI plummeted 9.99% (auto-halt triggered), Samsung/SK Hynix each –12%. US session: SMH –6.5%, MU –11.4%, AMD –7.5%, NVDA –3.2%, INTC –9.0%, ARM –8.5%, TSLA –3.9%. Nasdaq and S&P 500 both lower.
- **Crypto: RISK-OFF confirmed.** BTC ~$62,249 (–3.0%), ETH ~$1,654 (–4.7%). Both in downtrend. Altcoin breadth 19–31% above EMA20 (deteriorating).
- **Stocks: Pre-open bullish setup CONTRADICTED by chip rout.** 4/4 index uptrend in pre-market read no longer holds in tech. Regime now: **chop trending risk-off (tech)**. Financials (XLF/JPM) holding.
- **JPM long thesis CONFIRMED post-open.** B-tier intraday long triggered ($333–334 zone). Financials RS leader vs chip selloff. RTH confirmation obtained.
- **DO NOT TRADE: AMD/SMH swing long B-tier signals.** Stocks swing report had AMD B (71.76) and SMH B (66.26) as longs — these are counter-regime with chip rout active. Swing is watchlist-only due to –12R audit anyway.
- **Crypto OPEN actionable (shorts):** ENA (scalp/intraday/swing triggered x3), NEAR (scalp/intraday triggered x2), ZEC (scalp triggered). Six signals open/tracking.
- **ETH swing short (B-tier):** WAITING for entry — key level to watch. Also 1 untracked Telegram alert on ETH swing (pipeline integrity flag, see §14).
- **SMCI and UNH: confirmed AVOID.** Legal risks unchanged (export-control indictment + DOJ Medicare probe).
- **Playbook note:** Crypto swing is the ONLY profitable mode (PF 1.50, +11R). Scalp/intraday crypto losing (PF 0.00/0.53). Weight swing signals over scalp/intraday.

---

## 2. Data Used

| Source | File / Path | mtime EEST | Freshness |
|---|---|---|---|
| Scheduler log | `data/scheduled_runs/2026-06-23_default_schedule/scheduler.log` | 17:21 | **FRESH** (1h18m) |
| Latest cycle | `cycle_05_16-53_summary.md` | 17:21 | **FRESH** |
| Crypto monitor log | `crypto_monitor_1782224460.log` | 18:12 | **ACTIVE** |
| Stocks monitor log | `stocks_monitor_1782224460.log` | 18:13 | **ACTIVE** |
| Scalp report | `data/reports/scalp/2026-06-23_14-00_scalp_report.md` | 17:00 | **FRESH** (1h39m) |
| Intraday report | `data/reports/intraday/2026-06-23_14-05_intraday_report.md` | 17:05 | **FRESH** (1h34m) |
| Swing report | `data/reports/swing/2026-06-23_14-15_swing_report.md` | 17:15 | **CARRY-FORWARD** (4.5h) |
| Stocks intraday | `data/reports/stocks/intraday/2026-06-23_15-37_stocks_intraday_report.md` | 18:37 | **FRESH** (~2min ago) |
| Stocks swing | `data/reports/stocks/swing/2026-06-23_14-18_stocks_swing_report.md` | 17:18 | **CARRY-FORWARD** (4.4h; watchlist-only) |
| Stocks invest | `data/reports/stocks/invest/2026-06-23_14-20_stocks_invest_report.md` | 17:20 | **CARRY-FORWARD** (4.3h) |
| Catalyst cycle | `data/catalysts/2026-06-23/catalyst_cycle_14-05.md` | 17:05 | **FRESH** |
| Catalyst JSONL | `data/catalysts/2026-06-23/catalyst_events.jsonl` | 17:05 | **FRESH** |
| Active-signals CLI | crypto (29) + stocks (50) | 18:39 | **LIVE** |
| Signal-stats CLI | crypto + stocks | cycle 05 | **LIVE** |
| Untracked alerts | `detect_untracked_legacy_alerts` | 18:39 | **LIVE — 1 untracked** |
| Prior review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-23_1620.md` | 16:37 | 2h2m ago |
| BTC/ETH price | WebSearch (Yahoo Finance, Fortune) | 18:39 | **FRESH** |
| Chip selloff / Nasdaq | WebSearch (TheStreet, CNBC, Schwab) | 18:39 | **FRESH** |

**External web research available.** BTC/ETH confirmed, global chip selloff confirmed (KOSPI data, SMH/MU/NVDA moves verified).

**Blindspots:** Reddit social blocked (403 all cycle). Liquidation heatmaps / order book not connected. Onchain config missing (`no config/onchain.yaml`). ETF flows from internal scan only (no live feed). TradingView / manual chart MCP unavailable — analysis uses OHLCV-derived ATR/EMA/RS fields only.

---

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: **17:21 EEST** (1h18m ago) — FRESH.
- Latest cycle `cycle_05_16-53_summary.md` mtime: **17:21 EEST** — FRESH.
- Both freshness checks < 3h → **NOT DEFERRED**.
- Cycle 05: started 16:53, finished 17:21. Steps: ok=26, failed=0. Monitor window: 90 min.
- `crypto_monitor` active: last log entry 18:12 EEST (27m ago). PID confirmed.
- `stocks_monitor` active: last log entry 18:13 EEST (26m ago). PID confirmed.
- Signal tracking (pre): checked=429, updated=9, tp_hits=275, expired=9.
- Revalidation pass: checked=5, stale=1.
- Untracked legacy alerts: **1** — ETH/USDT B swing short (sent 2026-06-23T14:35:43 UTC without backing proposed_signal). See §14.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-06-23 18:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.87,
      "reason_codes": ["scheduler_fresh", "report_stale_partial"],
      "data_missing": ["onchain_config_missing", "reddit_social_blocked", "yfinance_fundamentals_404_etfs"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "cycle_05 finished 17:21 EEST 1h18m ago",
        "ok=26 failed=0 all steps",
        "crypto_monitor active 18:12 EEST",
        "stocks_monitor active 18:13 EEST",
        "stocks intraday report 15:37 UTC fresh",
        "swing/invest carry-forward 4-5h within limit",
        "1 untracked ETH swing alert"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.92,
      "reason_codes": ["risk_off", "shorts_preferred", "mixed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC downtrend $62,249 -3%",
        "ETH downtrend $1,654 -4.7%",
        "altcoin breadth 19-31% above EMA20",
        "KOSPI -9.99% global chip rout (auto-halt)",
        "SMH -6.5% MU -11.4% AMD -7.5% NVDA -3.2%",
        "VIX 19.54",
        "stocks chop: 2/4 indices uptrend (IWM DIA) but tech sector risk-off",
        "financials XLF/JPM holding RS"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.77,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "narrative_supported", "mapping_weak"],
      "data_missing": ["social_attention_absent"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "KOSPI -10% chip selloff catalyst confirmed (TheStreet CNBC)",
        "$2.5B ETF outflows from BTC/ETH (CryptoSlate)",
        "ETH Foundation 20% staff cut (CryptoBriefing)",
        "UNH DOJ probe confirmed (QuiverQuant)",
        "SMCI export-control indictment confirmed (SEC EDGAR)",
        "XRP Ripple MiCA EU approval (CoinDesk) - positive",
        "Digital Asset Market Clarity Act uncertain Senate path",
        "THORChain resumed trading post $10.7M exploit",
        "9 symbols unmapped in catalyst integrity: ALGO APT COIN DOT FIL HBAR LINK QQQ TON",
        "479 events today, 6 narrative baskets"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "ok",
      "confidence": 0.68,
      "reason_codes": ["unwind", "post_unwind_chop", "data_unavailable"],
      "data_missing": ["liquidation_heatmap_unavailable", "onchain_flow_unavailable", "bybit_oi_partial"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ENA price down + OI down = deleveraging (no squeeze risk for shorts)",
        "NEAR scalp funding -0.0023 (elevated negative - longs paying shorts)",
        "EIGEN price down + OI down = deleveraging",
        "WLD price down + OI down = deleveraging",
        "squeeze phase dist: 28 post_unwind_chop, 8 unwind, 7 build_up, 2 squeeze_expansion",
        "SYN price up + OI down = short covering (weaker continuation quality)",
        "DEXE price up + OI up = fresh positioning, elevated long crowding"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.71,
      "reason_codes": ["entry_fresh", "chase_risk", "stale_before_entry"],
      "data_missing": ["chart_mcp_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ENA already -12.4% 24h before trigger (scalp/intraday may be late)",
        "SMH -6.5% session - chasing short after large gap-down",
        "NEAR -10.5% estimated 24h - similar chase risk on scalp",
        "JPM triggered in entry zone $333-$334 2h post-open (RTH confirmation obtained)",
        "ETH swing short still waiting - entry not yet triggered (cleaner entry available)",
        "ZEC swing short waiting (cleaner than triggered scalp)",
        "TradingView/manual chart check unavailable - OHLCV fields only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.83,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto OPEN actionable (triggered): ENA scalp short, ENA intraday short, ENA swing short, NEAR scalp short, NEAR intraday short, ZEC scalp short = 6 signals",
        "crypto WAITING for entry: ZEC swing short, WLD scalp short, NEAR swing short, XLM scalp short, XLM intraday short, ETH swing short = 6 signals",
        "crypto CLOSED WIN (TP hit): 17 signals (rows 13-29 in CLI output)",
        "stocks OPEN actionable: SMH B intraday short (triggered), TSLA B intraday short (triggered), JPM B intraday long (triggered)",
        "stocks WAITING: C-tier AMD UNH IWM XLF QQQ XLY COIN PLTR AVGO MSFT GOOGL",
        "NEEDS REVIEW: ETH/USDT B swing short Telegram alert sent 14:35 UTC without backing proposed_signal",
        "UNH signals WAITING but AVOID due to confirmed DOJ probe"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.86,
      "reason_codes": ["legal_risk", "headline_risk", "correlation_cluster"],
      "data_missing": ["daily_loss_tracking_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SMCI: US Attorney SDNY export-control indictment confirmed - AVOID all directions",
        "UNH: DOJ Medicare fraud investigation confirmed -16% dive - AVOID all directions",
        "AMD swing B-tier long counter-regime: global chip selloff makes this dangerous",
        "SMH swing B-tier long counter-regime: SMH -6.5% session",
        "Crypto 6 open shorts correlation cluster: ENA/NEAR/ZEC triggered simultaneously",
        "Stocks swing watchlist-only (-12R 0W/12L audit)",
        "Crypto B-tier PF 0.76 below 0.8 system threshold",
        "Weekend signals underperform WR 16% n=51 (TNSR AXS both weekend=Y active)"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "bad",
      "confidence": 0.89,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto A/B: WR 14.9% PF 0.76 avgR -0.11 total -17R n=175 reliable",
        "Crypto scalp mode: n=73 0W/10L PF 0.00 - FAILING bucket",
        "Crypto intraday mode: n=63 9W/39L PF 0.53 - FAILING bucket",
        "Crypto swing mode: n=39 14W/22L PF 1.50 +11R - ONLY profitable mode",
        "Stocks A/B: WR 7.7% PF 0.33 -4R n=15 weak sample",
        "Stocks A-tier: n=1 +2R (single sample, unreliable)",
        "Stocks swing watchlist-only per -12R audit",
        "Stocks intraday B-tier: 0W/6L latest 15-sample"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.79,
    "preferred_side": "shorts",
    "best_long_candidate": {
      "symbol": "JPM",
      "trigger": "Already triggered $333-334 zone; SL $330.88; hold if SPY not breaking broad support",
      "reason": "Financials RS leader +10.5% vs SPY 20d; confirmed RTH hold vs chip selloff; B-tier triggered 2h into session"
    },
    "best_short_candidate": {
      "symbol": "ENA/USDT",
      "trigger": "Already triggered scalp/intraday/swing; monitor failed bounce above entry for continuation",
      "reason": "Clean deleveraging (price down + OI down), multiple timeframes all triggered, regime-aligned, no reversal catalyst"
    },
    "best_catalyst_candidate": {
      "symbol": "HYPE/USDT",
      "trigger": "Pullback to perps DEX basket primary level; wait_pullback playbook; no chase",
      "reason": "Perps DEX narrative primary with fresh <1h basket; ETF outflows from BTC/ETH support DEX story; endorsed by basket not signal"
    },
    "avoid_candidate": {
      "symbol": "AMD",
      "reason": "Swing B long COUNTER-REGIME in global chip rout (-7.5% session, KOSPI -10%); stocks swing is watchlist-only; SMCI and UNH also avoid (legal)"
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
| data_quality | **ok** | 0.87 | scheduler_fresh, report_stale_partial | advisory_only |
| market_regime | **ok** | 0.92 | risk_off, shorts_preferred, mixed | advisory_only |
| catalyst_narrative | **caution** | 0.77 | fresh_catalyst, catalyst_confirmed, mapping_weak | advisory_only |
| derivatives_squeeze | **ok** | 0.68 | unwind, post_unwind_chop, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.71 | entry_fresh, chase_risk, stale_before_entry | advisory_only |
| execution_lifecycle | **ok** | 0.83 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | **caution** | 0.86 | legal_risk, headline_risk, correlation_cluster | advisory_only |
| playbook_performance | **bad** | 0.89 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | **caution** | 0.79 | shorts_preferred, correlation_cluster, legal_risk | advisory_only |

---

## 4. What Changed vs Previous Review

_Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-23_1620.md` (16:20 EEST, pre-US-open)._

| Item | 16:20 Status | 18:39 Status | Change |
|---|---|---|---|
| JPM long | Pre-open candidate; RTH confirmation required | **CONFIRMED** B-tier triggered ($333-334) | ✅ Thesis confirmed |
| AMD swing long | Gap risk flagged; avoid pre-market | **COUNTER-REGIME** (-7.5% session) | ❌ Correctly avoided |
| SMH swing long | Gap risk flagged; avoid | **COUNTER-REGIME** (-6.5% session) | ❌ Correctly avoided |
| SMH intraday short | Not present | **B-tier SHORT triggered** (new signal added in monitors) | New |
| TSLA short | Not highlighted | **B-tier SHORT triggered** (-3.9% session) | New triggered |
| Stocks regime | Bullish (4/4 uptrend, VIX 19.76) | **Chop trending risk-off** (tech); financials held | Degraded |
| Crypto regime | Risk-off (BTC -3%, ETH -4.7%) | Risk-off (unchanged) | No change |
| Crypto active signals | 18 | 29 (+11 new; cycle 05 additions) | Expanded |
| Untracked alerts | 0 | **1** (ETH/USDT swing short, sent 14:35 UTC) | New integrity issue |
| SMCI / UNH | AVOID (confirmed) | AVOID (unchanged) | No change |
| KOSPI data | Not available pre-open | **-9.99% confirmed** (Samsung/SK Hynix -12%, auto-halt) | New external data |
| Signal expiries | — | 9 expired this cycle | Lifecycle update |

**Biggest new information:** KOSPI –9.99% with circuit-breaker. Pre-open tech futures showed –0.24%; actual session saw SMH –6.5%. The chip selloff was structurally larger than pre-market signals implied — rooted in Korea/Taiwan semiconductor panic, not just Nasdaq futures noise.

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 479 (as of cycle_14-05 / 17:05 EEST); swing report shows 559 unique events by 17:15
- **Narrative baskets active:** 6 — delisting_thin_liquidity, perps_dex_narrative, rwa_narrative, ai_narrative, binance_ecosystem_teaser, momentum_breakout
- **Catalyst integrity flag (cycle 05):** 9 high-importance symbol-tagged catalysts NOT mapped into `catalyst_events`: ALGO, APT, COIN, DOT, FIL, HBAR, LINK, QQQ, TON

**Mapping health: MODERATE.** 9/479 = 1.9% of events, but these are flagged as "high-importance" — meaning their absence is a coverage gap, not a rounding error. Manually verify any of these 9 symbols if they appear in active signals or reports.

**Key catalysts driving decisions:**
- [CONFIRMED] UNH DOJ Medicare fraud probe → AVOID UNH in all directions
- [CONFIRMED] Global semiconductor selloff (KOSPI -10%, Samsung/SK Hynix -12%) → SMH/AMD/NVDA short bias
- [CONFIRMED] $2.5B ETF outflows from BTC/ETH → crypto risk-off reinforced
- [CONFIRMED] ETH Foundation 20% staff cuts → ETH sentiment bearish
- [POSITIVE] Ripple MiCA EU approval → XRP watch (not in active signal set)
- [NEUTRAL] Digital Asset Market Clarity Act Senate uncertainty → regulatory overhang
- [RESOLVED] THORChain resumed trading after $10.7M exploit → potential RUNE/ecosystem catalyst

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off
- **Stocks mood:** chop / risk-off (tech sector), mixed (financials/industrials holding)
- **Dominant narrative:** Global semiconductor selloff — KOSPI circuit-breaker, Asia chip contagion → US tech drain
- **Preferred side now:** shorts (crypto + tech stocks); catalyst-backed (XRP MiCA, HYPE DEX)
- **Best long candidate:** JPM — already triggered at entry zone, financials RS leader, confirmed 2h RTH hold
- **Best short candidate:** ENA/USDT — clean deleveraging, multiple timeframes triggered, no reversal catalyst
- **Best catalyst-backed candidate:** HYPE/USDT — perps DEX basket primary, ETF outflows support DEX narrative; wait_pullback only
- **What to avoid:** AMD/SMH swing longs (counter-regime), UNH all directions (DOJ probe), SMCI all directions (export-control indictment), weak altcoin longs without catalyst
- **What would change the view:** BTC reclaim above $64,000 with strong volume would soften crypto risk-off. Nasdaq reversal + VIX back below 17 would re-open tech longs. Neither expected without a macro catalyst flip.

---

## 7. Candidate Deep Dives

### Candidate 1 — SMH (Stocks Intraday, B-tier SHORT — OPEN ACTIONABLE)

**Score:** 69 | **Status:** OPEN ACTIONABLE (triggered) | **Direction:** short | **Mode:** intraday

**Catalyst:** KOSPI –9.99% (auto-halt), Samsung/SK Hynix –12%, MU –11.4%, AMD –7.5%, NVDA –3.2%, INTC –9.0%, ARM –8.5%. Confirmed by TheStreet and CNBC live updates.

**Has price reacted?** Yes — SMH dropped ~6.5% from open. Signal triggered in the entry zone.

**Is the setup chasing?** Moderate. A 6.5% gap-lower session already occurred before the 2h review point. Existing triggered position is valid. **New entries at session lows = chasing.** Only add on a failed bounce back toward the opening range ($635–640 zone).

**Overextended?** For a fresh entry, yes. For existing positions already triggered, tracking is appropriate.

**What level makes it actionable?** Existing position: tracking now. New size: failed bounce to $635–640 only.

**Aligned with market mood?** Fully. Tech sector risk-off, global chip catalyst confirmed.

**Actionable now or after confirmation?** Existing position: active. New add: confirmation required (failed bounce structure on chart).

**Invalidation:** SMH reclaim above opening-range highs; KOSPI circuit-breaker re-opening with stabilization; central bank / government intervention in Korea chip sector reversing narrative.

**Chase-risk?** Moderate for new entries; low for existing triggered position.

**Legal/Headline risk for SMH?** None specific to the ETF. Component stocks (NVDA, AMD) are down on fundamental AI cooling / rate-hike fears, not legal issues.

---

### Candidate 2 — JPM (Stocks Intraday, B-tier LONG — OPEN ACTIONABLE)

**Score:** 65.09 | **Status:** OPEN ACTIONABLE (triggered) | **Direction:** long | **Entry:** $333.19–$334.34 | **SL:** $330.88 | **TP1:** $337.80 | **TP2:** $340.11

**RS vs SPY (20d):** +10.52% | **RS vs XLF sector (20d):** +5.27% | **Earnings:** safe

**Pre-open thesis:** Financials RS leader in a tech-adverse session. Triggered at planned entry zone post-open. Confirmed with 2h RTH hold.

**Has price reacted?** JPM was pre-market +0.16%. The long thesis is structural RS, not an event catalyst.

**Is the setup chasing?** No — entered at the intended zone after 30-min RTH confirmation.

**Retest structure?** Clean. JPM pulled back from pre-market high to the $333-334 entry zone and held.

**Overextended?** No unusual single-day move in JPM.

**Aligned with market mood?** Yes — financials act as a rotation beneficiary when tech selloff is sector-specific rather than broad.

**What would change this?** Broad risk-off spreading from tech to all sectors (VIX > 22-25), SPY/DIA breakdown below key support, or a JPM-specific negative headline (none identified today).

**Invalidation:** Close below $330.88 (system SL).

**Chase-risk?** Low. Already in position at intended level.

**Legal/Headline risk?** No JPM-specific legal risk in any today's sources. Earnings: safe.

---

### Candidate 3 — ENA/USDT (Crypto B-tier SHORT, 3 timeframes — OPEN ACTIONABLE)

**Score (swing):** 68 | **Status:** OPEN ACTIONABLE | **Triggered:** scalp + intraday + swing (×3)

**24h:** –12.4% | **RS vs BTC:** –8.6% | **OI:** price down + OI down = **deleveraging**

**Funding:** –3.95e-05 (mildly negative) | **Long/short ratio:** 1.937 (long-heavy, unwinding) | **Crowding:** normal

**Thesis:** Pure regime-aligned technical short. No ENA-specific catalyst needed — the downtrend + deleveraging OI structure + regime alignment create the setup.

**Chase-risk analysis:**
- Scalp: high chase risk (–12% already). Existing position tracking; no new scalp adds.
- Intraday: moderate chase risk. Existing position tracking.
- **Swing: lower chase risk** (longer validity window). PF 1.50 for swing mode. This is the mode to prioritize.

**Playbook guidance:** Crypto swing mode is the only profitable bucket (PF 1.50, +11R). The scalp bucket (PF 0.00) should not receive new size. Focus on the swing signal.

**Invalidation:** ENA reclaim above entry zone on 1h close with volume + BTC recovery above $64K.

**Catalyst?** Internal check: no ENA-specific news in `news_items` last 24h. Short is technical/regime-only.

---

### Candidate 4 — NEAR/USDT (Crypto B-tier SHORT — scalp/intraday OPEN, swing WAITING)

**Score:** 65–67 | **Status:** scalp short OPEN ACTIONABLE (triggered), intraday short OPEN ACTIONABLE (triggered), swing short WAITING for entry

**24h:** ~–10.0% | **RS vs BTC:** –6.3% | **Funding (negative):** –0.0023 (longs paying shorts — elevated)

**Basket context:** NEAR is in the **ai_narrative basket** as a primary symbol. However: basket heat is only 30-36/100, volume 0.2/100 (intraday) — the AI narrative is NOT driving NEAR higher. It's a placeholder, not active momentum.

**Chase risk:** Moderate for scalp/intraday (already –10%). Swing signal (WAITING) provides a cleaner entry if triggered.

**Funding at –0.0023:** This is an elevated negative funding rate, meaning longs are paying. For a short position this is supportive — you get paid over time. Watch for extreme negative funding (potential squeeze trigger at –0.5% or more).

**Contradiction check:** AI basket narrative is bearish by omission (not hot, not supporting). No reversal catalyst for NEAR. Short is aligned.

**What changes this?** A fresh AI catalyst directly supporting NEAR (new product launch, partnership, token utility news). None present today.

---

### Candidate 5 — ETH/USDT (Crypto B-tier SWING SHORT — WAITING for entry + pipeline flag)

**Score:** B-tier 67.5 (untracked alert) / active signal WAITING | **Status:** WAITING for entry (legitimate B-tier signal)

**Note:** Two separate entities:
1. **Active B-tier signal** (CLI row 12): ETH swing short, WAITING for entry — legitimate, will contribute to tracking
2. **Untracked Telegram alert** (detect_untracked_legacy_alerts): B swing short sent 14:35:43 UTC — no backing proposed_signal, will NOT count toward PF

**24h:** ETH –4.7% | **Downtrend confirmed** | **Catalysts supporting short:** ETH Foundation 20% staff cuts, $2.5B ETF outflows from ETH, Ethereum market drops headline

**Entry zone (inferred):** ~$1,640–1,660 (near current price $1,654 — signal may trigger soon).

**Why this is the cleanest of the ETH signals:** It hasn't triggered yet. Every tick lower toward entry is closer to a non-chase setup. The waited-for entry in a downtrend is structurally better than a chased scalp entry.

**Alignment with mood?** Full alignment. ETH downtrend, negative catalysts, crypto risk-off.

**What would prevent trigger?** ETH bounce above $1,700 before hitting entry zone would push price away from entry.

**Invalidation (if triggered):** ETH reclaim above $1,750 on volume + positive catalyst.

**Pipeline flag:** The untracked alert means this signal result cannot be tracked against historical PF. The actual B-tier active signal IS tracked. Manual review of the pipeline gap recommended (§14).

---

## 8. Best Candidates Ranked

| Rank | Symbol | Asset | Mode | Direction | Status | Entry / Trigger | Key reason |
|---|---|---|---|---|---|---|---|
| 1 | **JPM** | stocks | intraday | LONG | OPEN ACTIONABLE | Already triggered $333-334; SL $330.88 | Financials RS leader; RTH confirmed 2h; non-tech in chip-rout session |
| 2 | **ENA/USDT** | crypto | swing (priority) | SHORT | OPEN ACTIONABLE | Already triggered; monitor failed bounce | Deleveraging OI; swing mode PF 1.50; multiple TF confirmed |
| 3 | **ETH/USDT** | crypto | swing | SHORT | WAITING for entry | Entry zone ~$1,640-1,660; watch for trigger | Downtrend + bearish catalysts; cleaner entry (not yet triggered = not chasing) |
| 4 | **SMH** | stocks | intraday | SHORT | OPEN ACTIONABLE | Triggered; add only on failed bounce $635-640 | Global chip rout confirmed; B-tier; no adds at session lows |
| 5 | **HYPE/USDT** | crypto | watchlist | CATALYST LONG | WATCH | Pullback to basket primary (wait_pullback) | Perps DEX basket primary; ETF outflow supports DEX; no signal yet |

---

## 9. Avoid / No Trade

_(This decision window only — scanner, collection, tracking continue regardless.)_

- **AMD swing LONG (B-tier 71.76):** Counter-regime. Global chip selloff –7.5% session. Stocks swing watchlist-only. Do not enter.
- **SMH swing LONG (B-tier 66.26):** Counter-regime. SMH –6.5% session. Stocks swing watchlist-only. Do not enter.
- **UNH (all directions):** DOJ Medicare fraud investigation confirmed. UNH –16% dive. All active UNH signals (C-tier intraday/swing) are disqualified. Do not enter.
- **SMCI (all directions):** Export-control indictment (SDNY, 3 individuals). Any SMCI signal is disqualified. Do not enter.
- **Weak altcoin longs without catalyst:** BTC/ETH downtrend, breadth 19-31% above EMA20. No long signals for alts without RS-leader status + confirmed catalyst.
- **Crypto scalp new entries:** PF 0.00, 0W/10L historically. Existing triggered scalp signals track. No new scalp size.
- **TNSR, AXS (weekend=Y, TP hit):** Weekend signals underperform WR 16% (n=51). Both in TP-hit territory. Review lifecycle; do not add.

---

## 10. Main Risks

1. **Chip selloff broadens to full risk-off.** If Korea/Taiwan panic spreads beyond tech to financials/credit, JPM long and all longs rotate to avoid. Monitor IWM + VIX threshold ~22-25.
2. **BTC –15% scenario.** CoinDesk cites a long-time indicator suggesting BTC may need to drop 15% or more to find bottom. From $62K, target ~$52,800. Existing crypto shorts aligned; expiry windows may not cover full move.
3. **ETF outflow continuation.** $2.5B already exited from BTC/ETH ETFs. Continued outflows = sustained secondary selling pressure on altcoins.
4. **Crypto short correlation cluster.** ENA + NEAR + ZEC + XLM + WLD + ETH all short simultaneously. A sudden BTC reversal (whale accumulation, macro surprise) would unwind all shorts at once.
5. **ETH Foundation staff cut narrative expansion.** 20% headcount reduction may trigger ecosystem questions (development capacity, roadmap pace). Watch for secondary ETH ecosystem news.
6. **Reddit/social blind spot.** All Reddit sources 403. X/Telegram KOL placeholder. Social squeeze signals (memecoin pumps, narrative shifts) cannot be detected.
7. **Catalyst mapping gap (9 symbols).** ALGO, APT, COIN, DOT, FIL, HBAR, LINK, QQQ, TON have high-importance news not mapped to catalyst_events. LINK and TON specifically have active narratives (RWA, Telegram ecosystem) that could matter.
8. **Untracked ETH alert integrity.** Telegram already notified about ETH swing short without a tracking signal. Outcome won't be recorded. Pipeline integrity gap creates a black hole in PF accounting.

---

## 11. Action Plan — Next 4 Hours

| Priority | Action | Timeframe | Level / Condition |
|---|---|---|---|
| 1 | **Monitor ENA swing short** (primary) | Now → 4h | Existing position; SL system-defined; no new scalp adds |
| 2 | **Monitor JPM long** | Now → close | SL $330.88; watch if SPY breaks broad support levels |
| 3 | **Watch ETH swing short trigger** | Next 1-2h | Entry zone ~$1,640-1,660; prioritize over any scalp adds |
| 4 | **Do NOT enter AMD/SMH longs** | Rest of session | Chip selloff active; stocks swing watchlist-only |
| 5 | **HYPE/USDT watch** | 2-4h | Pullback to perps DEX basket level; no chase entry |
| 6 | **SMH intraday short — no new adds** | Now | Only add on failed bounce to $635-640; not from session lows |
| 7 | **Investigate ETH untracked alert** | Manual task | Find why proposed_signal was missing at alert send time (see §14) |
| 8 | **Late-session risk check** | 21:30 EEST slot | Review ENA/NEAR if still open; check if chip selloff stabilized or deepened |

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Action |
|---|---|---|---|
| Crypto scalp | crypto | **AVOID new entries** | Existing triggered signals track (PF 0.00 historically); no new scalp opens |
| Crypto intraday | crypto | **watch** | ENA/NEAR intraday shorts tracking; no new intraday opens in weak alts |
| Crypto swing | crypto | **OPEN ACTIONABLE** | ENA swing tracking; ETH swing waiting (best new entry); prioritize swing over scalp/intraday |
| Stocks intraday | stocks | **watch (selective)** | JPM long tracking; SMH short tracking (no new adds at session low); UNH/SMCI avoid |
| Stocks swing | stocks | **WATCHLIST ONLY** | AMD/SMH longs counter-regime; watchlist-only per –12R audit |
| Stocks invest | stocks | **WATCHLIST ONLY** | Carry-forward; no new invest signals this session |

---

## 13. Sources

- [Bitcoin and ethereum prices today, June 23, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-june-23-2026-values-slipping-as-possible-rate-hikes-weigh-on-prices-135817007.html) — BTC ~$62,249, ETH ~$1,654; 2026-06-23
- [Stock Market Today (June 23, 2026) — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-23-2026) — KOSPI –9.99%, SMH –6.5%, MU –11.4%, NVDA –3.2%; 2026-06-23
- [S&P 500 falls on global chip rout — CNBC](https://www.cnbc.com/2026/06/22/stock-market-today-live-updates.html) — global semiconductor selloff context; 2026-06-22/23
- [Tech Stress Test: Chips Slammed in Early Plunge — Schwab](https://www.schwab.com/learn/story/stock-market-update-open) — session open chip selloff analysis; 2026-06-23
- Internal: `data/reports/scalp/2026-06-23_14-00_scalp_report.md` — crypto regime, RS leaders, narrative heatmap, OI data
- Internal: `data/reports/intraday/2026-06-23_14-05_intraday_report.md` — crypto candidates, derivatives, macro
- Internal: `data/reports/swing/2026-06-23_14-15_swing_report.md` — crypto swing candidates, OI, DEXE crowding
- Internal: `data/reports/stocks/intraday/2026-06-23_15-37_stocks_intraday_report.md` — stocks regime VIX, JPM B-tier, chip selloff names, signal performance
- Internal: `data/reports/stocks/swing/2026-06-23_14-18_stocks_swing_report.md` — stocks swing watchlist-only note, AMD/SMH B-tier longs (counter-regime)
- Internal: `data/catalysts/2026-06-23/catalyst_cycle_14-05.md` — catalyst events, UNH legal, THORChain, Binance listings, basket summaries
- Internal: `data/scheduled_runs/2026-06-23_default_schedule/cycle_05_16-53_summary.md` — scheduler freshness, all 26 steps, signal stats, intelligence layer

---

## 14. Fix Requests / TODO

### TODO-eth-untracked-swing-alert
- **issue:** ETH/USDT B swing short Telegram alert sent 2026-06-23T14:35:43 UTC without a backing `proposed_signal`; trade outcome will not contribute to PF/winrate tracking
- **evidence:** `detect_untracked_legacy_alerts --since 2026-06-23` output: `ETH/USDT | B | swing | 67.5 | short | 2026-06-23T14:35:43+00:00 | NO (no proposed_signal)`
- **suggested manual fix:** Investigate signal pipeline between alert dispatch and `proposed_signals` table write. Check if `proposed_signal` INSERT failed or was rolled back before alert was sent. Add a pre-send assertion that `signal_id` exists in `proposed_signals` before dispatching any Telegram alert.
- **priority:** high
- **first observed:** 2026-06-23 18:39 EEST

### TODO-catalyst-mapping-9-symbols
- **issue:** 9 high-importance symbols with events in `news_items` are NOT mapped into `catalyst_events`: ALGO, APT, COIN, DOT, FIL, HBAR, LINK, QQQ, TON
- **evidence:** Cycle 05 step 5 catalyst integrity scan: `WARNING: 9 high-importance symbol-tagged catalysts not mapped into catalyst_events`
- **suggested manual fix:** Review symbol resolver in catalyst scan pipeline. QQQ/SMH are ETF tickers (not crypto tokens — may need disambiguation). COIN may conflict between exchange-name and token. TON/LINK/HBAR need explicit alias mapping rules. Add disambiguation or explicit mapping entries for each of the 9.
- **priority:** medium
- **first observed:** 2026-06-23 18:39 EEST (recurring; visible in cycle 05)

### TODO-reddit-social-blocked
- **issue:** All Reddit social sources returning 403 Client Error every cycle; social attention signal for BTC/ETH/CryptoCurrency completely absent
- **evidence:** `WARNING: Failed social source Reddit CryptoCurrency/Bitcoin/Ethereum: 403 Client Error` — recurring across scalp, intraday, and swing report generation steps
- **suggested manual fix:** Replace Reddit RSS with an alternative social signal source (e.g., LunarCrush API, Santiment, or alternative forum feed). Or investigate rate-limiting mitigation (user-agent rotation, request delays). Current state: 0 social attention data.
- **priority:** medium
- **first observed:** 2026-06-23 18:39 EEST (recurring pattern)

### TODO-kol-watchlist-placeholder
- **issue:** KOL watchlist contains a placeholder account; no real KOL/influencer signals are being captured
- **evidence:** All scalp/intraday reports state: "KOL watchlist still contains the placeholder account; replace it with trusted sources."
- **suggested manual fix:** Replace placeholder with 3-5 curated crypto KOL accounts or Telegram channels. Candidates: on-chain flow channels (lookonchain already feeding news_items), macro sentiment channels (WalterBloomberg already feeding), add 2-3 altcoin-specific or alpha-leak channels.
- **priority:** low
- **first observed:** 2026-06-23 18:39 EEST (recurring)
