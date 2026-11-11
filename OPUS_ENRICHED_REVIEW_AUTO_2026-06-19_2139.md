# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

_Generated 2026-06-19 ~21:39 EEST (Friday, Juneteenth holiday — US stocks CLOSED; US markets reopen Monday June 22; crypto live). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods. External web research: **not required this run** (all candidates verified via internal records <24h)._

> **⚠️ JUNETEENTH: US markets remain closed. Stocks signals stay Monday June 22 planning only. Crypto is the live actionable class.**
>
> **⚠️ CATALYST MAPPING WEAK: 76% unmapped across catalyst_events.jsonl (581/2421 lines have mapped symbols). Use catalyst layer as context, not final decision this run.**

---

## 1. Executive Summary

**Fri 2026-06-19 (Juneteenth), 21:39 EEST — "Late-session risk review" — crypto risk-off unchanged; XLM + MEGA shorts ENTERED UNRESOLVED; AVAX NEEDS REVIEW; no A-tier; advisory only.**

BTC/ETH remain in confirmed downtrends (altcoin breadth 27.5% above EMA20). Since the 18:39 "US open reaction" review: (1) **AVAX/USDT intraday B short** is no longer in the 22 active crypto signals — it has been closed between 18:39 and 21:39 EEST; outcome (TP/stop/expired) is unknown → **NEEDS REVIEW**. (2) **XLM/USDT swing B short** remains **ENTERED UNRESOLVED** — weekend gap risk is now materializing. (3) **MEGA/USDT** appears as both intraday short (B, 65.5/100) and swing short (B, 68.0/100) — both triggered this cycle. (4) **TAO/USDT swing B short** remains WAITING ~19% below current price — NOT actionable tonight. (5) Stocks: all WAITING for Monday June 22. **Late-session rule: no new swing entries; monitor active positions.**

**This slot is advisory only. No auto-trade. No changes to scoring, TP/SL, or execution logic.**

---

## 2. Data Used

| Report | File | mtime EEST | Age at review | Status |
|--------|------|------------|---------------|--------|
| Crypto scalp | `2026-06-19_16-23_scalp_report.md` | Jun 19 19:23 | ~2h16m | **FRESH** (<4h) |
| Crypto intraday | `2026-06-19_16-36_intraday_report.md` | Jun 19 19:36 | ~2h3m | **FRESH** (<4h) |
| Crypto swing | `2026-06-19_13-40_swing_report.md` | Jun 19 16:40 | ~4h59m | **CARRY-FORWARD** (4–12h) |
| Stocks intraday | `2026-06-19_18-37_stocks_intraday_report.md` | Jun 19 21:37 | ~2min | **VERY FRESH** |
| Stocks swing | `2026-06-19_13-54_stocks_swing_report.md` | Jun 19 16:54 | ~4h45m | **CARRY-FORWARD** (watchlist-only) |
| Stocks invest | `2026-06-19_14-04_stocks_invest_report.md` | Jun 19 17:04 | ~4h35m | **CARRY-FORWARD** (watchlist-only) |
| LLM packet (crypto) | `data/processed/llm_analysis_packet.md` | Jun 19 19:36 | ~2h3m | **FRESH** |
| Active signals (CLI) | `python -m src.cli active-signals` | Jun 19 21:39 | 0 min | **LIVE** |
| Signal stats (CLI) | `python -m src.cli signal-stats` | Jun 19 21:39 | 0 min | **LIVE** |
| Catalyst cycle | `data/catalysts/2026-06-19/catalyst_cycle_16-36.md` | Jun 19 19:36 | ~2h3m | **FRESH** |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-19_1839.md` | Jun 19 18:50 | ~50min | us_open_reaction slot |
| External prices | BTC ~$62,498 / ETH ~$1,687 (Yahoo Finance Jun 19, 15:30 EEST) | ~6h ago | **STALE** — directional only |

**External web research:** Not required this run — all candidates have fresh internal records (<24h) that are consistent and non-contradicted. TradingView/manual chart: **unavailable** — technical observations use OHLCV/ATR/EMA from reports only.

**Social attention:** Reddit 403 blocked (recurring). 0 symbol-level hits. No X/Telegram/Discord live feeds.

---

## 3. Scheduler / Data Freshness

| Check | Value | Status |
|-------|-------|--------|
| Latest run folder | `2026-06-19_default_schedule/` | ✓ |
| `scheduler.log` mtime (in run folder) | Jun 19 21:11 EEST (28min ago) | **FRESH** (<3h) |
| Latest `cycle_*_summary.md` | `cycle_02_19-07_summary.md` — Jun 19 19:54 EEST (1h45m) | **FRESH** (<3h) |
| Defer rule | Both <3h → **DO NOT DEFER** | ✓ |
| Cycle 2 status | ok=21 steps, failed=0 | **OK** |
| Cycle 2 tracking (pre) | checked=431, tp_hits=268, stopped=0, expired=6, not_triggered=0 | INFO |
| Crypto monitor | `crypto_monitor_1781887992.log` last entry ~21:23 EEST (16min ago) | **ACTIVE** |
| Stocks monitor | `stocks_monitor_1781887992.log` mtime 21:37 EEST (2min ago) | **ACTIVE** |
| Onchain | `interface_ready_config_missing` — no `config/onchain.yaml` | CONFIG MISSING |
| Bybit swing | No Bybit init warnings in cycle_02 | OK |
| Derivatives | MEXC fallback active; ATM no futures data | PARTIAL |
| Reddit social | 403 block (recurring) | WARNING |
| Catalyst mapping | 76% unmapped (581/2421 lines with symbol) → **WEAK** | ⚠️ |
| Untracked alerts | 0 (clean) | ✓ |

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-06-19 21:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["scheduler_fresh", "derivatives_sparse", "onchain_config_missing", "catalyst_missing"],
      "data_missing": ["onchain whale flows (config missing)", "live BTC/ETH price (6h stale)", "liquidation heatmaps", "ETF flows real-time", "Reddit 403 blocked"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log 28min old (<3h)",
        "cycle_02 summary 1h45m old (<3h) — 21 steps OK, 0 failed",
        "scalp/intraday fresh (~2h), swing carry-forward (~5h), stocks-intraday 2min",
        "crypto_monitor 16min old, stocks_monitor 2min old — ACTIVE",
        "catalyst mapping 76% unmapped > 50% threshold → WEAK",
        "MEXC fallback for several derivatives; ATM no futures data",
        "Reddit 403 recurring block",
        "onchain.yaml config missing"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["risk_off", "shorts_preferred", "danger"],
      "data_missing": ["live BTC/ETH price beyond 15:30 EEST (6h stale)", "ETF flows today", "real-time funding cross-venue"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: downtrend (all 3 crypto report cycles consistent)",
        "ETH trend: downtrend (all 3 crypto report cycles consistent)",
        "Altcoin breadth above EMA20: 27.50% (scalp/intraday) / 29.55% (swing) — depressed",
        "BTC ATR percentile 32-37% — normal volatility (not extreme)",
        "External: BTC ~$62,498 / ETH ~$1,687 at 15:30 EEST; post-FOMC selling, hawkish dot plot",
        "Spot ETF outflows: -$102M BTC+ETH June 18 (CryptoBriefing)",
        "Macro risk score 33-43/100 (calendar/watch hits, 1 risk-off hit in swing)",
        "Stocks: market closed (Juneteenth) — not a regime signal"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["no_catalyst", "mapping_weak", "narrative_supported", "stale_catalyst"],
      "data_missing": ["specific catalyst for MEGA short (none found)", "specific catalyst for XLM short (none found)", "76% catalyst events unmapped"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "777 total catalyst events today (reports); latest cycle processed 397",
        "76% unmapped (581/2421 JSONL lines) → mapping weak; threshold breached",
        "Legal: UNH DOJ probe 0.73 importance (QuiverQuant, confirmed); SMCI export-control 0.77 (SEC EDGAR, confirmed)",
        "ETH negative: UXLink exploit $8.1M to Tornado Cash; DAO relaunch; leadership exodus (2nd co-director)",
        "ETH mildly bullish: Morgan Stanley ETH+SOL ETF application (single_source); whale accumulation K3 Capital 10k ETH",
        "BTC ETF outflows -$102M June 18; whale sold 800 BTC at -$35.3M loss",
        "Baskets: perps_dex (HYPE), binance_ecosystem (BNB), ai_narrative (NEAR/RENDER/TAO/FET), momentum_breakout (ACT/BEL)",
        "No fresh verified catalyst for MEGA or XLM short candidates"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "data_unavailable", "post_unwind_chop"],
      "data_missing": ["AVAX current OI (signal closed — cannot verify squeeze outcome)", "ATM futures data unavailable", "OI numeric history sparse", "liquidation clustering unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "XLM swing short (ENTERED UNRESOLVED): OI +0.37% on price down = fresh shorts; funding -0.000140; crowding normal — MILD squeeze risk",
        "MEGA intraday short: OI -1.76% on price down = deleveraging; funding -0.000102 to -0.000200; crowding normal — FAVORABLE",
        "AVAX was OI +17.92% on price down at 18:39 = significant squeeze risk; signal now CLOSED — outcome unknown",
        "ACT/USDT: OI +10.08% on price up = fresh positioning (momentum RS leader)",
        "EDEN: OI -4.18% on price up = short covering (weaker continuation quality)",
        "BEL: negative funding across venues (bybit 0.0001, mexc -0.001119) — crowding elevated",
        "MET: funding -0.000166 to -0.000168 across venues; crowding elevated"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "ok",
      "confidence": 0.70,
      "reason_codes": ["entered_unresolved", "waiting_for_entry", "stale_before_entry", "clean_retest"],
      "data_missing": ["TradingView chart unavailable — using OHLCV/ATR/EMA only", "no live 15m/5m candle confirmation", "AVAX exit price unknown"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "XLM swing short (66.3/100): triggered at 0.2208-0.2226; ATR 0.0040; invalidation 0.2248; TP1 0.2160; clean retest",
        "MEGA intraday short (65.5/100): triggered at 0.0568-0.0574; ATR 0.0015; invalidation 0.0583; TP1 0.0549; ~2h into 4-24h window",
        "MEGA swing short (68.0/100): triggered at ~0.0572-0.0578; TP1 0.0553; fresh multi-day horizon",
        "TAO swing short (65.x): WAITING at ~22.x; current ~27.x = ~19% gap = far outside 1 ATR — NOT actionable tonight",
        "EDEN swing long (69.x): triggered; RS leader +12-14%; risk-off limits conviction for new entries",
        "EIGEN scalp long (69.x): triggered; low-confidence playbook (PF 0.14)"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["entered_unresolved", "waiting_for_entry", "needs_review"],
      "data_missing": ["AVAX outcome (TP/stop/expired) — not in 22 active signals", "exact fill prices for XLM/MEGA"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "22 crypto active signals at 21:39 EEST",
        "ENTERED UNRESOLVED (5): EIGEN scalp long, MEGA intraday short, MEGA swing short, EDEN swing long, XLM swing short",
        "WAITING for entry (2): ME... scalp (~MET), TAO swing short (far from trigger)",
        "TP HIT / tracking (15): XPL scalp short + EP... intraday long + ~13 swing longs",
        "AVAX intraday B short: NOT in 22 active signals → CLOSED since 18:39; outcome UNKNOWN → NEEDS REVIEW",
        "Cycle 2 pre-tracking: expired=6 (between-cycle expirations)",
        "Stocks: 50 signals all WAITING for Monday open (Juneteenth closed)",
        "Untracked legacy alerts: 0 (clean)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["correlation_cluster", "reduce_risk", "headline_risk", "manual_review"],
      "data_missing": ["daily P&L not visible in CLI", "AVAX outcome — was it a stop?", "weekend BTC move prediction unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Late-session Friday 21:39 EEST: swing shorts (XLM, MEGA sw) carry Sat/Sun BTC gap risk",
        "XLM: OI +0.37% fresh shorts → mild squeeze risk on BTC bounce; funding -0.000140",
        "MEGA intraday: 4-24h horizon — should resolve before Monday; manageable",
        "MEGA swing: multi-day → weekend carry risk",
        "Correlated short cluster: MEGA + XLM (both BTC-linked); AVAX closed (unknown outcome)",
        "Crypto B-tier WR 9%, PF 0.57, -33R week — longs dragging; short sub-cohort PF 2.0, +2R",
        "Scalp low confidence (PF 0.14) → EIGEN long treated as 0.5x weight",
        "Legal: UNH (DOJ probe AVOID), SMCI (export-control AVOID)",
        "Late-session rule: no new swing entries after 21:30 EEST Friday",
        "Weekend mode: NOT yet active (tomorrow Saturday)"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample", "missed_winner"],
      "data_missing": ["14d swing long closed outcomes (many in TP state)", "AVAX intraday short outcome"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto_failed_bounce_short (14d): WR 40%, PF 2.00, +9R — SHORT playbook working",
        "crypto_swing_narrative_rs_momentum (14d): WR 72%, PF 5.80, +24R — SWING LONG working (risk-off limits new longs)",
        "crypto_intraday_catalyst_or_momentum no-catalyst (14d): WR 23%, PF 0.70, -3R — failing without catalyst",
        "crypto_scalp_momentum_continuation: WR 12%, PF 0.14, -6R — low confidence, 0.5x weight",
        "Crypto B-tier week: WR 9%, PF 0.57, -33R (signal-stats) — longs drag",
        "Crypto shorts week: direction split shows longs WR ~8.8% PF ~0.53 -35R; shorts WR ~15% PF ~2.0 +2R",
        "Stocks A-tier: WR 50%, PF inf, +4R (n=4 anecdotal); B-tier: WR 12%, PF 0.78, -2R (n=25 weak)",
        "15 signals in TP state today — swing long playbook actively resolving positive",
        "stocks_swing + stocks_invest: watchlist-only (paused)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "correlation_cluster"],
      "data_missing": ["live BTC price (6h stale)", "AVAX outcome"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Risk-off confirmed all cycles; BTC/ETH both downtrend; alt breadth depressed",
        "Short playbook sub-cohort is productive (PF 2.0, +2R vs longs PF 0.53, -35R)",
        "XLM swing short: clean playbook, entered, weekend carry risk; monitor invalidation 0.2248",
        "MEGA shorts (dual-timeframe): both entered; intraday resolves before Monday; swing carries weekend risk",
        "TAO: far entry, NOT actionable tonight",
        "AVAX: NEEDS REVIEW (closed, unknown outcome)",
        "No new entries tonight; monitor existing positions"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.75,
    "preferred_side": "shorts",
    "best_long_candidate": {
      "symbol": "EDEN/USDT",
      "trigger": "BTC stabilization above $62K + pullback to swing entry zone with volume; do not chase current +12-14% move",
      "reason": "RS leader (91.6 score), swing long TP tracking; new entry only on regime shift + pullback"
    },
    "best_short_candidate": {
      "symbol": "MEGA/USDT",
      "trigger": "Already triggered: intraday at 0.0568-0.0574, swing at 0.0572-0.0578; TP1 0.0549; failed bounce into 0.0570+ = continuation",
      "reason": "Dual-timeframe short (65.5+68.0); OI deleveraging (favorable); no catalyst contradiction; aligned with risk-off"
    },
    "best_catalyst_candidate": {
      "symbol": "HYPE/USDT",
      "trigger": "perps_dex_narrative basket, wait_pullback playbook; trigger: breakdown below perps DEX support after failed bounce in Asia session",
      "reason": "Primary in perps_dex_narrative basket; Andrew Tate $86K loss narrative adds attention; risk-off limits upside"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ fraud investigation confirmed (QuiverQuant, importance 0.73); stock -16%; legal_risk = AVOID per §I protocol"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason Codes | Suggested Effect |
|-------|---------|------------|--------------|-----------------|
| data_quality | ok | 0.80 | scheduler_fresh, derivatives_sparse, onchain_config_missing, catalyst_missing | advisory_only |
| market_regime | ok | 0.85 | risk_off, shorts_preferred, danger | advisory_only |
| catalyst_narrative | caution | 0.60 | no_catalyst, mapping_weak, narrative_supported, stale_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, oi_contradicts, data_unavailable, post_unwind_chop | advisory_only |
| technical_entry | ok | 0.70 | entered_unresolved, waiting_for_entry, stale_before_entry, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.80 | entered_unresolved, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | correlation_cluster, reduce_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample, missed_winner | advisory_only |
| head_trader | caution | 0.75 | risk_off, shorts_preferred, correlation_cluster | advisory_only |

---

## 4. What Changed vs Previous Review (18:39 EEST)

| Item | Previous (18:39) | Current (21:39) | Change |
|------|-----------------|-----------------|--------|
| AVAX intraday B short | ENTERED UNRESOLVED (OI +17.92% squeeze risk) | NOT IN ACTIVE SIGNALS | **CLOSED — NEEDS REVIEW** (TP/stop/expired unknown) |
| XLM swing B short | ENTERED UNRESOLVED (triggered 0.2208–0.2226) | ENTERED UNRESOLVED | **Weekend gap risk active** |
| MEGA intraday short | In reports (B, 65.5/100) — not highlighted | ENTERED UNRESOLVED | **NEW — triggered this cycle** |
| MEGA swing short | In reports (B, 68.0/100) — not highlighted | ENTERED UNRESOLVED | **NEW — triggered this cycle** |
| TAO swing B short | WAITING (~22.x entry, ~27.x price) | WAITING (unchanged) | Far trigger; not actionable tonight |
| XPL scalp B short | TP1 HIT (confirmed 18:39) | TP state (tracking) | Resolved positively |
| Swing long cluster (~14 signals) | TP state | TP state | Unchanged; resolving positively |
| Stocks signals | All WAITING (Juneteenth) | All WAITING | Monday June 22 planning only |
| Stocks intraday run | 18:32 EEST report | 21:37 EEST (fresh cycle) | COIN B→C reconfirmed; market still closed |
| Catalyst coverage | 680–777 events; mapping weak | 777 events; 76% unmapped | Mapping still weak (recurring) |

**Thesis unchanged:** Risk-off; shorts preferred; XLM and MEGA are the clean active carries into the weekend.

---

## 5. Catalyst Coverage

- **Catalyst events today:** 777 (per reports §5b)
- **Latest cycle processed:** 397 (catalyst_cycle_16-36, mtime 19:36 EEST)
- **Narrative baskets:** 4 active (perps_dex_narrative, binance_ecosystem_teaser, ai_narrative, momentum_breakout)
- **Mapped symbols in JSONL:** ~581/2421 = **24% mapped → 76% unmapped → EXCEEDS 50% THRESHOLD**

⚠️ **CATALYST MAPPING WEAK THIS RUN — use catalyst layer as context, not final decision.**

**Top 3 unmapped / basket-level headlines worth flagging:**
1. `(basket)` — "Axelar says $4.7 million stolen in Secret Network bridge hack" (CryptoBriefing) — no specific crypto symbol mapped; potential contagion risk to bridge tokens
2. `(basket)` — "BPI calls CLARITY Act 'illicit finance-friendly'" (AMBCrypto) — regulatory sector, maps to no specific symbol
3. `(basket)` — "European Commission plans tariffs on Chinese plug-in hybrids" (CryptoBriefing) — macro/misclassified as exploit_hack

**Confirmed high-importance mapped events:**
- **UNH** [legal_risk] DOJ fraud probe — importance 0.73 — CONFIRMED → AVOID
- **SMCI** [legal_risk] Export-control indictment (3 individuals) — importance 0.77 — CONFIRMED → AVOID
- **ETH** [exploit_hack] UXLink exploit $8.1M to Tornado Cash — importance 0.71
- **ETH** [product_launch] Base Beryl upgrade / B20 token standard — fresh

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off (BTC + ETH downtrend; altcoin breadth 27.5% above EMA20; post-FOMC hawkish backdrop; $102M ETF outflows Jun 18; whale selling vs. accumulation tug-of-war)
- **Stocks mood:** closed (Juneteenth — NYSE/Nasdaq closed all day; reopens Monday June 22 09:30 ET)
- **Dominant narrative:** BTC anchored near $62K post-FOMC; XRP/DOT sentiment crash; ETH bifurcated (exploit risk vs. whale accumulation vs. Morgan Stanley ETF application); AI tokens (TAO/NEAR/RENDER) in mixed basket but risk-off suppresses
- **Preferred side now:** shorts — failed-bounce playbook (PF 2.0) is the productive sub-cohort; longs only RS-leaders on pullback with BTC stabilization
- **Best long candidate:** EDEN/USDT — RS leader; swing long already in TP tracking; new entry trigger: BTC stabilization above $62K + pullback to swing entry zone
- **Best short candidate:** MEGA/USDT — dual-timeframe B short already entered; intraday + swing both active; OI deleveraging supports continuation
- **Best catalyst-backed candidate:** HYPE/USDT — perps_dex_narrative basket (wait_pullback playbook); Andrew Tate $86K loss adds attention; trigger: breakdown below perps DEX support
- **What to avoid:** UNH (DOJ AVOID), SMCI (export-control AVOID), new swing entries tonight (weekend gap risk), chasing momentum breakouts (HEI +45-51%, ATM +17%, SYN +27% — already extended), TAO new long (AI narrative + risk-off = bad combination)
- **What would change the view:** BTC sustained close above $64K + altcoin breadth above 40% EMA20 → shift to mixed; ETF net inflow reversal over 3+ days → possible regime upgrade

---

## 7. Candidate Deep Dives (≤5)

### Candidate 1 — XLM/USDT — SWING B SHORT — ENTERED UNRESOLVED

**Score:** 66.3/100 | **Tier:** B | **Playbook:** `crypto_failed_bounce_short` (PF 2.00, WR 40%, +9R 14d) | **Status:** ENTERED UNRESOLVED

**Entry:** Triggered at 0.2208–0.2226 | **Invalidation:** 1h close above 0.2248 | **ATR:** 0.0040 | **TP1:** 0.2160 | **TP2:** 0.2119 | **TP3:** 0.2079

**Evidence:** 24h return -8–10%; RS vs BTC -8–9%; volume 0.27–0.61x (below average); downtrend; setup quality 66.8/100. Derivatives: OI +0.37% on price decline = fresh shorts (MILD squeeze risk); funding -0.000140; crowding normal; long/short 1.235.

**Chase check:** No — clean failed-bounce retest entry, not a chase.
**Overextended?** No — ATR 0.0040, entry was at zone, not >2ATR from EMA20.
**Catalyst?** No fresh specific catalyst found; no contradiction. Pure regime/technical short.
**Aligned with mood?** Yes — risk-off short.
**What invalidates?** 1h close above 0.2248 (BTC reclaim $63K+ would likely trigger this).
**Weekend carry risk:** YES — mild OI squeeze risk amplified by weekend BTC gap potential. If BTC shows strength Saturday AM, partial close reduces risk.

**Late-session verdict:** HOLD. Do not add. Monitor BTC $62K support level closely. Invalidation (0.2248) is the stop.

---

### Candidate 2 — MEGA/USDT — INTRADAY B SHORT + SWING B SHORT — ENTERED UNRESOLVED (DUAL)

**Intraday:** Score 65.5/100 | B | Playbook: `crypto_failed_bounce_short` | 4-24h horizon
**Swing (scalp report):** Score 68.0/100 | B | Playbook: `crypto_scalp_momentum_continuation` overlay | several days

**Intraday entry:** 0.0568–0.0574 | Invalidation: 0.0583 | TP1: 0.0549 | TP2: 0.0534 | ATR: 0.0015
**Swing entry (scalp report):** ~0.0572–0.0578 | Invalidation: 0.0587 | TP1: 0.0553

**Evidence:** 24h return -10.14%; RS vs BTC -11.11%; volume 1.02–1.12x (at-average); downtrend; setup quality 66.6–67.0/100. Derivatives: OI -1.76% on price decline = deleveraging/long liquidation (FAVORABLE for short continuation); funding -0.000102 to -0.000200 (short bias); crowding normal; long/short 1.106.

**Chase check:** No — failed bounce retest entry.
**Overextended?** No — ATR 0.0015, entry zone appropriate, support at 0.0537.
**Catalyst?** No fresh specific catalyst; no contradiction; pure momentum/regime.
**Aligned with mood?** Yes — risk-off short; MEGA is -14% 24h (swing data) = weak vs market.
**What invalidates?** 1h close above 0.0583 (intraday) / 0.0587 (swing).
**Weekend carry risk:** INTRADAY — should resolve before Monday (4-24h window, ~2h in). SWING — carries weekend risk like XLM.

**Late-session verdict:** HOLD both. Intraday: watch TP1 0.0549 overnight. Swing: set-and-hold. Do not let intraday become unintentional multi-day carry if TP1 not reached by Saturday noon EEST.

---

### Candidate 3 — TAO/USDT — SWING B SHORT — WAITING FOR ENTRY (NOT ACTIONABLE TONIGHT)

**Score:** 65.x/100 | **Tier:** B | **Playbook:** `crypto_failed_bounce_short` | **Status:** WAITING FOR ENTRY

**Entry zone:** ~22.x | **Current price (est.):** ~27.x | **Gap:** ~19% (~10+ ATR) | **ATR:** ~0.8–1.0

TAO swing short has an entry zone ~19% below the current estimated price. This far exceeds the 1 ATR threshold for "within range." AI narrative basket (`ai_narrative`) lists TAO as primary, but TAO is also in the weakest symbols list (-3.79% 24h, -4.76% RS vs BTC in intraday). The AI basket playbook is `related_beta_rotation` — in risk-off, this basket is not adding tail wind.

**Late-session verdict:** NOT ACTIONABLE tonight. Do not chase. The entry trigger is a specific failed-bounce zone far below. Reassess Monday if price compresses toward 22–23 range.

---

### Candidate 4 — AVAX/USDT — NEEDS REVIEW (CLOSED BETWEEN 18:39–21:39 EEST)

**Previous status (18:39):** ENTERED UNRESOLVED | B-tier intraday short | Score 66.1/100
**Entry:** 6.127–6.162 | **Invalidation:** 6.217 | **TP1:** 5.938 | **TP2:** 5.813 | **ATR:** 0.0765

**Current status:** NOT IN 22 ACTIVE CRYPTO SIGNALS → signal resolved/closed.

**Context at 18:39:** OI +17.92% on price decline = significant fresh shorts, high squeeze risk if BTC bounced from $62K. Crypto monitor was still tracking AVAX at ~20:20 EEST; by 21:39, it is absent from active signals.

**Possible outcomes:**
- **TP1 HIT (~5.938):** AVAX fell ~3–4% from entry → CLOSED WIN
- **STOPPED (~6.217):** BTC bounced → squeeze lifted AVAX above invalidation → CLOSED LOSS
- **EXPIRED (0R unresolved):** Window closed without TP/SL touch → 0R display / unresolved, no TP/SL before window

**Action:** Manual review at next session start. Query `signal_outcomes` table for AVAX intraday short resolved today.

---

### Candidate 5 — UNH — STOCKS LEGAL RISK — AVOID

**Source:** QuiverQuant — "UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation" | 2026-06-19 | importance 0.73 | single_source

UNH appears in stocks active signals as a C-tier short (61.38/100, planning only, market closed) and C-tier swing long (78/100, watchlist only). Per §I: DOJ fraud investigation = **AVOID** verdict. Legal-risk shorts can gap unpredictably and squeeze.

**Legal risk verdict:** AVOID UNH longs entirely. Short is directionally confirmed by legal news, but do NOT treat as clean actionable — flag for Monday morning manual review with fresh open levels before any consideration.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Direction | Tier | Status | Late-Session Verdict |
|------|--------|------|-----------|------|--------|---------------------|
| 1 | XLM/USDT | swing | short | B | ENTERED UNRESOLVED | Hold; monitor BTC $62K; weekend carry risk |
| 2 | MEGA/USDT | intraday | short | B | ENTERED UNRESOLVED | Hold; watch TP1 0.0549 overnight; resolve before Mon |
| 3 | MEGA/USDT | swing | short | B | ENTERED UNRESOLVED | Hold; multi-day; weekend gap risk similar to XLM |

**Best long-watch:** EDEN/USDT — swing long already triggered and TP tracking (RS leader); new entry trigger: BTC hold above $62K + pullback to original swing entry zone with volume. Do not chase current +12-14%.

**Best short-watch:** MEGA/USDT — already in. If forced to state new entry trigger: failed bounce into 0.0570+ zone. Intraday invalidation at 0.0583; swing at 0.0587.

**Best catalyst-watch:** HYPE/USDT — perps_dex_narrative basket (wait_pullback playbook, primary symbol). Trigger: breakdown below perps DEX support after failed bounce, confirmed on next Asia/Europe session. Do not enter late Friday without fresh signal.

No clean NEW entry this window — late-session Friday; all productive setups already entered or far from trigger. Creating new positions at 21:39 EEST Friday adds unnecessary weekend gap risk.

---

## 9. Avoid / No Trade (This Decision Window Only — Scanner Continues)

**Avoid tonight:**
- New swing entries — weekend gap risk
- New scalp entries — PF 0.14 low confidence; late-session EIGEN long is tracking but risky in risk-off
- Chasing momentum breakouts (HEI +45-51%, ATM +17%, SYN +27%, ACT +22%) — momentum_breakout basket = wait_pullback playbook; these have already moved significantly
- UNH longs — DOJ probe CONFIRMED, AVOID per §I
- SMCI — export-control indictment CONFIRMED, AVOID per §I
- TAO new long — AI narrative + risk-off; entry far
- ETH directional — whale accumulation vs. ETF outflows + exploit risk = no clean side; tug-of-war

**These are decisions for the current late-session window only. This is NEVER a command to stop the system. Scanning, candidate generation, and outcome tracking continue.**

---

## 10. Main Risks

1. **AVAX outcome unknown:** If stopped out, raises concern about XLM/MEGA squeeze vulnerability — manual review needed at session start.
2. **Weekend BTC gap:** BTC near $62K support. A weekend gap above $63K → XLM invalidation (0.2248); MEGA swing invalidation (0.0587). Crypto weekends can move 3–5% without warning.
3. **XLM mild squeeze risk:** OI +0.37% (fresh shorts); funding -0.000140. BTC bounce would amplify squeeze risk. Consider partial close if BTC shows Saturday AM strength.
4. **MEGA intraday window:** 4-24h horizon — if TP1 not reached by Saturday noon EEST, position risks expiring as 0R unresolved / no TP/SL before window.
5. **Catalyst mapping chronic weakness:** 76% unmapped across catalyst_events.jsonl. Unknown events in unmapped 76% could be material. Axelar $4.7M hack and macro events are in basket; others may be present but unclassified.
6. **Crypto B-tier playbook pressure:** WR 9%, PF 0.57 week. If short sub-cohort (XLM, MEGA) also starts losing, re-audit needed. Signal: 3+ short losses in one session.
7. **Stocks index NaN returns:** All SPY/QQQ/IWM/DIA show NaN returns in stocks reports — likely Juneteenth holiday data gap. Could affect Monday morning regime classification quality; investigate before open.

---

## 11. Action Plan — Next 4 Hours (21:39 → 01:39 EEST Saturday)

1. **Monitor XLM swing short** — key: invalidation 0.2248. BTC holds below $63K = position healthy for weekend carry. TP1 target: 0.2160.
2. **Monitor MEGA intraday short** — watch for TP1 0.0549 tonight. If near invalidation 0.0583 without progress by late night, note for morning review. Intraday horizon — should not be held indefinitely.
3. **Monitor MEGA swing short** — set-and-hold multi-day; same BTC risk as XLM.
4. **Morning review (04:30 EEST Saturday — crypto Asia slot):** Confirm AVAX outcome in DB; check BTC overnight move; assess XLM/MEGA health vs. BTC level.
5. **No new entries tonight** — late-session rule applies strictly.
6. **Stocks:** Carry all planning signals forward to Monday June 22; COIN B→C and MSTR B→C are the top short watchlist candidates; re-evaluate on fresh RTH levels at open.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Rationale |
|------|---------|-----------|
| Crypto scalp | NO NEW ENTRY | Low confidence (PF 0.14, WR 12%); EIGEN scalp long triggered but risky in risk-off; let current tracking resolve |
| Crypto intraday | HOLD MEGA SHORT | ENTERED UNRESOLVED; watch TP1 0.0549 overnight; intraday horizon resolves before Monday |
| Crypto swing | HOLD XLM + MEGA SHORTS | Both ENTERED UNRESOLVED; weekend carry risk flagged; also hold EDEN long (RS leader, TP tracking); no new entries |
| Stocks intraday | WAIT — MARKET CLOSED | Monday June 22 is next actionable session; COIN B→C short top watchlist |
| Stocks swing | WATCHLIST ONLY | Paused playbook (WR 11%, PF 0.15 pre-pause) |
| Stocks invest | WATCHLIST ONLY | Paused (0W/24L, -24R) |

**Overall verdict: CAUTION / RISK-OFF.** Short sub-cohort productive (PF 2.0). No new entries tonight. Monitor 3 active crypto shorts (XLM, MEGA-int, MEGA-sw). Review AVAX outcome in morning. Stocks reactivate Monday.

---

## 13. Sources

All sources verified via internal records (internal-first protocol — no WebSearch required this run).

- QuiverQuant — "UnitedHealth (UNH) Faces DOJ Probe, Shares Dive 16% on Fraud Investigation" | Jun 19 2026 | single_source | confirms AVOID
- SEC EDGAR — SMCI Form 8-K FY2026 | filed Mar 1 2026 | primary_source | export-control indictment, 3 individuals | confirms AVOID
- CryptoBriefing — "Bitcoin, Ethereum spot ETFs see over $102M in net outflows on June 18" | Jun 19 2026 | single_source | confirms risk-off
- t.me/lookonchain — ETH whale accumulation: K3 Capital 10k ETH + Chun Wang 7.65k ETH withdrawn from Binance | Jun 19 2026 | single_source
- AMBCrypto — "UXLink exploit returns as attacker sends $8.1M ETH to Tornado Cash" | Jun 19 2026 | single_source
- CryptoBriefing — "Morgan Stanley files amended applications for spot Ethereum and Solana ETFs with rock-bottom fees" | Jun 19 2026 | single_source
- BeInCrypto — "Ethereum Foundation's Leadership Exodus Claims Its Second Co-Director" | Jun 19 2026 | single_source
- CryptoBriefing — "Axelar says $4.7 million stolen in Secret Network bridge hack" | Jun 19 2026 | single_source

Internal: `data/reports/` (scalp/intraday/swing/stocks), `data/catalysts/2026-06-19/`, `data/scheduled_runs/2026-06-19_default_schedule/`, `data/processed/llm_analysis_packet.md`, CLI outputs.

---

## 14. Fix Requests / TODO

### TODO-AVAX-OUTCOME-REVIEW
- **issue:** AVAX/USDT intraday B short was ENTERED UNRESOLVED at 18:39 EEST and is no longer in the 22 active crypto signals at 21:39. Outcome (TP/stop/expired) unknown from this automated review.
- **evidence:** Active-signals CLI at 21:39 shows 22 crypto signals — AVAX absent. Crypto monitor log confirms AVAX was still tracked at ~20:20 EEST. Cycle 2 pre-tracking shows expired=6 (general expirations, source unidentifiable from this context).
- **suggested manual fix:** Query `SELECT * FROM signal_outcomes WHERE symbol='AVAX' AND asset_class='crypto' AND updated_at > '2026-06-19 15:00:00' ORDER BY updated_at DESC LIMIT 5;` to determine TP/stop/expired. If stopped, assess squeeze risk for XLM/MEGA correlation.
- **priority:** high
- **first observed:** 2026-06-19 21:39 EEST

### TODO-CATALYST-MAPPING-THRESHOLD
- **issue:** Catalyst mapping is chronically 76%+ unmapped (581/2421 JSONL lines with symbol; 97% of cycle events classified as `other_news`). Flagged in multiple consecutive reviews.
- **evidence:** `data/catalysts/2026-06-19/catalyst_events.jsonl` 2421 rows, 581 with symbol pattern. `catalyst_cycle_16-36.md`: 397 events, 384 = other_news.
- **suggested manual fix:** Improve symbol resolver in catalyst pipeline to extract symbols from headlines (NER pass); add a company-to-ticker mapping (e.g., "UnitedHealth" → "UNH"); consider keyword-based auto-tagging for common crypto entities (ETH, BTC, SOL) in unmapped events.
- **priority:** medium
- **first observed:** 2026-06-19 21:39 EEST (recurring)

### TODO-STOCKS-INDEX-NAN-RETURNS
- **issue:** All index/sector return fields are `NaN` in stocks reports (SPY/QQQ/IWM/DIA all show `return_5d: NaN, return_20d: NaN, above_ema20: false`). Breadth above EMA20=0.0%, EMA50=0.0%. Affects regime classification quality.
- **evidence:** `data/reports/stocks/intraday/2026-06-19_18-37_stocks_intraday_report.md` §1–2; `data/processed/agent_outputs/20260619_165212_stocks_stocks_market_regime.json`.
- **suggested manual fix:** Investigate yfinance OHLCV fetch for stocks indices on Juneteenth (market closed); add holiday-aware handling that uses last available close (Thursday June 18) as current price when market is closed, preventing NaN cascade. Check if `failed=0` (all symbols fetched) hides a silent NaN when the market returns no candle data.
- **priority:** medium
- **first observed:** 2026-06-19 21:39 EEST
