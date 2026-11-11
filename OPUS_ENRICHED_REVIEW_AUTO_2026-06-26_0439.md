# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:39 EEST

**Slot:** Crypto Overnight / Asia Review (04:30 EEST slot)
**Time:** 2026-06-26 04:39 EEST (01:39 UTC)
**Date:** 2026-06-26 (Friday — weekday, crypto+stocks)
**Model:** claude-sonnet-4-6
**Advisory only — no auto-trade, no signal registration**

---

## 1. Executive Summary

**Slot: Crypto Overnight / Asia Review.** Advisory only — no auto-trade.

**BTC remains in confirmed downtrend, bounced off 2026 lows.** Catalyst: 6 consecutive weeks of ETF outflows ($5.94B total), $1.48B liquidations triggered BTC below $60K intraday. As of June 24 external data, BTC ~$62.7K; swing report notes "Bitcoin bounces off new 2026 price lows" — Asia session appears to be a relief bounce, not reversal. Risk-off regime intact.

**9 active crypto signals, all at tp_hits status.** Regime-aligned shorts (BTC/NEAR/MEGA) are OPEN ACTIONABLE having captured partial profits. Six counter-trend longs (HEI/HOT/ETH/AXS/FI/WLD) are ENTERED UNRESOLVED but hit TPs during Asia bounce. No new A/B signals generated in Cycle 9.

**CATALYST MAPPING WEAK: 73.9% unmapped — use catalyst layer as context, not final decision.**

**UNH: mandatory AVOID.** DOJ criminal+civil probe confirmed and expanded; A-tier score (81) is irrelevant — legal risk rule forces automatic demotion.

**HEI is best long-watch** (RS +57% vs BTC, OI confirming, momentum basket primary). **NEAR is best short-watch** (active signal, fresh short pressure, regime-aligned). No new entries are clean in this session — wait for Europe/Asia confirmation before adding.

**ALWAYS-SCAN: Scanner and data collection continue in all regimes. Do not disable.**

---

## 2. Data Used

| Source | File | Generated (EEST) | Age at 04:39 | Status |
|--------|------|-----------|--------------|--------|
| Scheduler log | scheduler.log | 04:14 | 25 min | FRESH |
| Cycle 9 (active) | scheduler.log | 03:50 → running | active | LIVE |
| Scalp report | 2026-06-26_01-02_scalp_report.md | 04:02 | 37 min | FRESH (cycle 9) |
| Intraday crypto | 2026-06-26_01-10_intraday_report.md | 04:10 | 29 min | FRESH (cycle 9) |
| Swing crypto | 2026-06-26_01-31_swing_report.md | 04:31 | 8 min | VERY FRESH (cycle 9) |
| Stocks intraday | 2026-06-26_01-20_stocks_intraday_report.md | 04:20 | 19 min | FRESH (cycle 9) |
| Stocks swing | 2026-06-26_01-37_stocks_swing_report.md | 04:37 | 2 min | VERY FRESH (cycle 9) |
| Stocks invest | (pending) | running | n/a | CYCLE 9 IN PROGRESS |
| Catalyst scan | catalyst_cycle_01-10.md | 04:10 | 29 min | FRESH |
| Active signals | src.cli active-signals ×2 | 04:40 | live | LIVE |
| Signal stats | src.cli signal-stats ×2 | 04:40 | live | LIVE |
| Untracked legacy | detect_untracked_legacy_alerts | 04:40 | live | NONE FOUND |
| External web | WebSearch (BTC, UNH) | 04:40 | live | LIVE |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-06-25_2330.md | 23:30 | 5h9m | READ |

**Data freshness note:** Cycle 9 started at 03:50 and is still running (stocks invest report in progress). Crypto scalp, intraday, and swing are complete; stocks intraday and swing complete. No stocks invest report available yet for this review.

**Blindspots:** Live BTC/ETH tick price, liquidation heatmaps, live OI/CVD aggregates, social attention (Reddit 403), onchain config missing, stocks invest report pending.

---

## 3. Scheduler / Data Freshness

- **Scheduler log** mtime: 04:14 EEST (25 min ago). NOT DEFERRED.
- **Cycle 8**: Finished 01:50 EEST (28 steps OK / 0 failed). Clean.
- **Cycle 9**: Started 03:50 EEST. Still running — stocks invest report CMD START 04:38.
  - Completed: scalp (04:02) · intraday (04:10) · catalyst scan (04:10) · paper overlays (04:10–04:13) · OHLCV archive (04:14) · intelligence layer (04:14) · stocks intraday (04:21) · crypto swing (04:31) · stocks swing (04:38)
  - In progress: stocks invest report
- **Active crypto signals**: 9 (all B-tier, all tp_hits). See §3A/lifecycle.
- **Active stocks signals**: 50 (C-tier + 2 B-tier triggered from prior cycle). All WAITING — US market closed.
- **Untracked legacy crypto alerts**: NONE (clean).
- **Onchain risk**: interface_ready / config_missing — no data available.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-06-26 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["scheduler_fresh", "packet_missing"],
      "data_missing": ["llm_packets_unread", "onchain_config_missing", "social_attention", "stocks_invest_report_pending"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 04:14 (25 min)", "cycle 9 active since 03:50", "scalp 04:02 / intraday 04:10 / swing 04:31 fresh", "catalyst_cycle_01-10 at 04:10", "untracked alerts = 0"]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.88,
      "reason_codes": ["risk_off", "shorts_preferred", "wait_for_trigger"],
      "data_missing": ["live_btc_price", "live_orderbook"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend all three timeframe reports", "ETH downtrend all three timeframe reports", "altcoin breadth EMA20 26-32% (deeply risk-off)", "BTC ATR 97-99th pct = elevated volatility", "ETF outflows 6-week streak $5.94B", "BTC fell below $60K + $1.48B liquidations", "swing news: bounces off 2026 price lows", "regime and signal reality diverge: longs PF 3.1 vs shorts PF 0.9 in signal history"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_contradicted", "narrative_supported"],
      "data_missing": ["primary_source_verification for 73.9% of events"],
      "suggested_effect": "advisory_only",
      "facts_used": ["126/482 mapped = 26.1% WEAK (< 50% threshold)", "BTC: ETF outflows + below $60K (confirmed bearish)", "ETH: SharpLink +5000 ETH bought (bullish) vs Base outage (negative, resolved)", "ADA: wallet exploit confirmed SecondFi $2.4M private key flaw (AVOID)", "XRP: RLUSD Japan FSA approval (positive, from prior review)", "RWA basket fresh <6h (ONDO/XLM primary)", "momentum_breakout basket: HEI/G/ATM/ETHFI (no verified catalyst, pure momentum)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "watch",
      "confidence": 0.58,
      "reason_codes": ["oi_supports", "squeeze_risk", "data_unavailable"],
      "data_missing": ["liquidation_heatmaps", "aggregated_OI", "CVD", "live_funding_across_venues"],
      "suggested_effect": "advisory_only",
      "facts_used": ["RE/USDT funding -0.002 = heavily negative shorts crowded / squeeze risk", "HEI/USDT OI +31-34% with price up (fresh positioning, confirmed)", "G/USDT OI +44.5% with price up (fresh positioning)", "MEGA/USDT OI +5.2% price down = fresh shorts pressing", "NEAR/USDT OI +7.4% price down = fresh shorts pressing", "most symbols: neutral funding ±5e-05, crowding normal"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest"],
      "data_missing": ["live_chart", "tradingview_confirmation"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Cycle 9 generated ZERO A/B tier new setups", "G/USDT rejected: >2 ATR from EMA20 = chase", "HEI pullback zone 0.167-0.174 vs current 0.178 (near resistance 0.190)", "NEAR short retest zone 1.818-1.842 (current 1.808 — just inside zone)", "ETH short conditional zone 1568-1580 (current 1562 — below zone, testing support)", "BTC swing short already at tp_hits (active signal, partials taken)"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["open_actionable", "entered_unresolved", "waiting_for_entry"],
      "data_missing": ["paper_monitor_cycle9_status (still running)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["9 crypto active signals all tp_hits", "BTC/NEAR/MEGA shorts: OPEN ACTIONABLE regime-aligned tp_hits", "HEI/HOT/ETH/AXS/FI/WLD: counter-trend ENTERED UNRESOLVED tp_hits (Asia bounce)", "Stocks: 50 signals WAITING (market closed)", "JPM B-tier triggered (prior cycle - likely tp_hits)", "Untracked legacy alerts = 0"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.88,
      "reason_codes": ["legal_risk", "headline_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ criminal+civil probe confirmed and expanded to Optum Rx, physician reimbursement (shares -16%) → mandatory AVOID per §I", "ADA: wallet exploit confirmed SecondFi private key flaw → AVOID longs", "6 counter-trend longs in overnight bearish regime = correlation cluster risk if BTC resumes decline", "BTC below $60K context + $1.48B liquidations", "Stocks swing paused: 48h audit -12R 0W/12L", "Weekend: AXS weekend_mode=Y"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.87,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto swing: 14W/17L PF 2.05 +18R WORKING", "Crypto intraday: 12W/28L PF 1.17 +5R marginal", "Crypto scalp: 0W/7L PF 0.00 -7R FAILING", "Long bias: 11W/9L PF 3.1 +19R outperforming", "Short bias: 15W/43L PF 0.9 -3R losing", "Multi-exchange confirmed PF 2.33 vs unconfirmed PF 0.81", "Stocks swing paused (-12R 0W/12L audit)", "Stocks A/B n=19 weak sample PF 1.11"]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["wait_for_trigger", "mixed", "risk_off"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Regime bearish but signal longs are outperforming (PF 3.1) while signal shorts losing (PF 0.9)", "Asia bounce validates counter-trend long TPs but not reversal", "No new A/B setups in cycle 9", "Catalyst mapping too weak (73.9% unmapped) to trust catalyst-based decisions", "Best entry quality: HEI pullback (RS leader), NEAR retest (active short)", "UNH forced AVOID; ADA forced AVOID"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.78,
    "preferred_side": "mixed",
    "best_long_candidate": {
      "symbol": "HEI/USDT",
      "trigger": "pullback to 0.167-0.174 with volume > 1x avg and BTC stable above $59K",
      "reason": "RS leader +57% vs BTC, OI +31% confirming fresh positioning, momentum_breakout basket primary, no verified catalyst but pure momentum is working in longs (PF 3.1)"
    },
    "best_short_candidate": {
      "symbol": "NEAR/USDT",
      "trigger": "failed bounce retest 1.82-1.84; 1h close below 1.80 with BTC continuation lower; SL above 1.869",
      "reason": "Active B-tier short, tp_hits, fresh shorts pressing (OI +7.4%), AI narrative basket (weak heat), regime-aligned, multi-exchange confirmed 87.9%"
    },
    "best_catalyst_candidate": {
      "symbol": "ETH/USDT",
      "trigger": "hold above 1532 support with BTC stable; pullback to 1532-1563 with volume",
      "reason": "SharpLink bought 5000 ETH ($7.85M) 6h ago (institutional buying); B-tier long active/tp_hits; Base outage resolved; concrete catalyst vs other names"
    },
    "avoid_candidate": {
      "symbol": "UNH",
      "reason": "DOJ criminal+civil probe confirmed + expanded; shares -16%; mandatory legal risk AVOID per §I regardless of score (81 intraday A-tier is irrelevant)"
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
|-------|---------|------------|--------------|-----------------|
| data_quality | **ok** | 0.88 | scheduler_fresh, packet_missing | advisory_only |
| market_regime | **ok** | 0.88 | risk_off, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | **caution** | 0.65 | mapping_weak, fresh_catalyst, catalyst_contradicted | advisory_only |
| derivatives_squeeze | **watch** | 0.58 | oi_supports, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.75 | entry_late, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | **ok** | 0.82 | open_actionable, entered_unresolved, waiting_for_entry | advisory_only |
| risk_manager | **caution** | 0.88 | legal_risk, headline_risk, correlation_cluster | advisory_only |
| playbook_performance | **caution** | 0.87 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | **ok** | 0.78 | wait_for_trigger, mixed, risk_off | advisory_only |

**Overall verdict:** CAUTION — risk-off confirmed, weak catalyst mapping, no new A/B setups, UNH forced AVOID. Asia bounce is partial / not reversal. Hold existing positions with active TP/SL. No new entries without Europe confirmation.

---

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-25_2330.md` (post-close 23:30 EEST).

| Item | Prior (23:30) | Now (04:39) | Change |
|------|--------------|-------------|--------|
| Active crypto signals | 8 B-tier | 9 B-tier | **HEI B-long intraday ADDED** (new cycle 9) |
| BTC/NEAR/MEGA shorts | OPEN ACTIONABLE | Still OPEN ACTIONABLE, tp_hits | Holding, no change |
| HOT/ETH/AXS/FIL/WLD longs | ENTERED UNRESOLVED | tp_hits (Asia bounce) | **Counter-trend longs hit TPs overnight** |
| BTC price | Below $60K intraday | Bounce off 2026 lows (ext. ~$62.7K June 24) | Asia relief bounce |
| Altcoin breadth | 22.7% above EMA20 | 26-32% | Slight improvement |
| G/USDT | In scalp watchlist | Score 100 scalp, still rejected (chase) | Consistent rejection |
| HEI/USDT | Not in prior review | +56% 24h, RS leader, momentum basket | **NEW — significant RS leader** |
| UNH legal risk | Flagged in prior | Confirmed DOJ probe expanded | Unchanged — mandatory AVOID |
| ADA exploit | Confirmed in prior | Still active | Unchanged — AVOID longs |
| XRP RLUSD Japan | Confirmed in prior | Still in XRP swing watchlist fresh | Carry-forward positive |
| Catalyst mapping | Not computed prior | 73.9% unmapped | **WEAK — flag in §5** |
| Stocks swing | Paused (audit) | Still paused (-12R 0W/12L) | Unchanged |
| Scalp playbook | Flagged losing | 0W/7L PF 0.00 | **Confirmed failing** |

**Thesis unchanged:** BTC in bearish downtrend, regime is risk-off. Counter-trend longs are speculative Asia bounces against trend. Swing shorts remain the regime-aligned plays.

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 482
- **Mapped (symbol assigned):** 126 (26.1%)
- **Unmapped (null/basket):** 356 (73.9%)
- **Narrative baskets:** 6

**⚠️ CATALYST MAPPING WEAK THIS RUN (73.9% unmapped) — use catalyst layer as context, not final decision.**

**Event type breakdown:** other_news=460 (95.4%), earnings_event=5, product_launch=3, partnership=3, regulatory_sector_headline=3, exploit_hack=2, platform_growth=1, airdrop=1, infrastructure_failure=1, rumour_only=1, low_liquidity_event=1, legal_risk=1

**Active narrative baskets:**
- **rwa_narrative** `<6h` FRESH — primary: ONDO/USDT, XLM/USDT — playbook: `related_beta_rotation`
- **momentum_breakout** `<1h` VERY FRESH — primary: HEI/USDT, G/USDT, ATM/USDT, ETHFI/USDT — playbook: `avoid_chase`
- **ai_narrative** `<24h` — primary: NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT — playbook: `related_beta_rotation`
- **perps_dex_narrative** `<24h` — primary: HYPE/USDT — playbook: `wait_pullback`
- **binance_ecosystem_teaser** `<24h` — primary: BNB/USDT — playbook: `related_beta_rotation`
- **delisting_thin_liquidity** `<24h` — playbook: `avoid_low_liquidity`

**Notable catalyst events:**
- `0.82` **ADA/USDT** [exploit_hack] Cardano wallet exploit: private key flaw (AMBCrypto) → AVOID
- `0.81` **ETH/USDT** [infrastructure_failure] Coinbase Base two-hour outage (CoinDesk) — resolved
- `0.75` **BTC/USDT** [regulatory_sector_headline] BTC below $60K + $1.48B liquidations (AMBCrypto)
- `0.73` **UNH** [legal_risk] DOJ probe, shares -16% (QuiverQuant)

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** `risk-off` — BTC + ETH both downtrend, altcoin breadth 26-32% above EMA20. BTC ATR at 97-99th percentile. ETF outflows 6 consecutive weeks ($5.94B). BTC touched new 2026 lows, Asia bounce underway (temporary relief).
- **Stocks mood:** `closed` — Regime: **chop** (VIX 18.89, 2/4 indices uptrend, breadth 50%). SMH/XLI/XLV strong; XLC/XLY/XLE weak. Stocks swing paused (audit). All stock signals WAITING.
- **Preferred side now:** `mixed` — Regime says shorts but signal history says longs outperform (PF 3.1 vs 0.9 shorts). Prefer: holding active shorts (BTC/NEAR/MEGA), monitoring counter-trend TP hits, no new aggressive entries.
- **Best long candidate:** HEI/USDT — RS leader +57% vs BTC, trigger: pullback 0.167-0.174 with volume
- **Best short candidate:** NEAR/USDT — active signal, fresh short pressure, trigger: failed bounce 1.82-1.84
- **Best catalyst-backed candidate:** ETH/USDT — SharpLink institutional buying + Base outage resolved
- **What to avoid:** G/USDT (chase >2 ATR), UNH (legal AVOID), ADA (exploit AVOID), scalp entries (PF 0.00)
- **What would change the view:** BTC close above $63K on high volume with ETF inflow reversal → regime flip; BTC break below $58K → increase short aggression

---

## 7. Candidate Deep Dives

### Candidate 1 — BTC/USDT (active B swing short, OPEN ACTIONABLE)

**Lifecycle:** OPEN ACTIONABLE — B-tier swing short, tp_hits. Entry ~$62K+ area.

**Thesis:** BTC confirmed downtrend, below $60K intraday, ETF outflows 6 weeks ($5.94B). Swing short playbook PF 2.05 / +18R. BTC is the cleanest regime-aligned short in the system.

**Has price reacted?** Yes — BTC broke below $60K on ETF outflow catalyst. Asia bounce (~$62.7K ext.) approaching prior support/resistance from below.

**Chase risk?** Low for holding; HIGH for new entry at this point.

**Actionable now?** HOLD existing position. Do not add. New entries require failed bounce from $62-63K retest or 1h close below $60K again.

**Aligned with market mood?** YES — regime-aligned short.

**Invalidation:** 1h close above $64K+.

**Counter-thesis:** June 23 ETF inflow +$39.2M potential inflection. If ETF flows turn positive, momentum shift could accelerate bounce.

---

### Candidate 2 — HEI/USDT (watchlist, best RS leader long)

**Lifecycle:** Active B-tier intraday long (tp_hits). Swing watchlist 57.3/100.

**Thesis:** HEI/USDT +56% 24h, RS vs BTC +57-59%. OI +31-34% with price up = fresh positioning. Volume 1.57x average. In `momentum_breakout` basket (primary).

**Chase risk?** HIGH at current price (0.178). Pullback zone: 0.167-0.174.

**No verified catalyst** — pure momentum play, higher risk.

**Actionable now?** WATCHLIST ONLY. Trigger: pullback to 0.167-0.174 with sustained volume >1x avg and BTC stability above $59K. SL: 1h close below 0.157.

---

### Candidate 3 — ETH/USDT (B swing long, ENTERED UNRESOLVED tp_hits)

**Lifecycle:** ENTERED UNRESOLVED — B-tier swing long, tp_hits. Entered in prior cycle.

**Catalyst:** SharpLink bought 5,000 ETH ($7.85M) ~6h ago (t.me/lookonchain). SharpLink holds 876,285 ETH ($1.4B total). Concrete institutional accumulation event. Coinbase Base outage resolved.

**Price context:** ETH ~$1,562. Support at 1,532.

**Actionable?** HOLD existing. No new entry — price near support.

**Invalidation:** 1h close below 1,532 → exit long.

**Catalyst mixed:** SharpLink buy = confirms long thesis. BTC downtrend + ETF outflows = contradicts.

---

### Candidate 4 — UNH (stocks A-tier score 81 → MANDATORY LEGAL RISK AVOID)

**LEGAL/HEADLINE RISK — AUTOMATIC AVOID**

UNH A-tier (81.26) stocks intraday / B-tier (75.72) stocks swing.

**DOJ Probe confirmed and expanded:** Criminal and civil DOJ investigations covering Optum Rx, physician reimbursement, Medicare Advantage billing. Criminal division leading. UNH acknowledged in SEC filing. Shares -16%.

**Sources:** pymnts.com · ainvest.com

**Final verdict: AVOID.** Score of 81 is irrelevant. All UNH signals: `needs_review`, NOT actionable.

---

### Candidate 5 — G/USDT (score 100 / rejected for chase, informational)

G/USDT score 100/100 scalp, 24h +35-37%, RS vs BTC +37-39%, volume 8.53x avg, OI +44.5%.

**Why not actionable:** >2 ATR from EMA20 (system rejected). No verified catalyst (momentum_breakout basket). In bearish regime, can evaporate when BTC resumes.

**Risk for shorts:** G/USDT OI +44.5% with price +35%+ — shorting here is extremely dangerous (squeeze risk). Do NOT short G/USDT.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Dir | Action | Tier | Trigger / Status |
|------|--------|------|-----|--------|------|-----------------|
| 1 | BTC/USDT | swing | short | HOLD — regime-aligned, TP hits, do not add | B (active) | Hold; failed retest $62-63K for add |
| 2 | NEAR/USDT | intraday | short | HOLD — active signal, TP hits | B (active) | Hold; retest 1.82-1.84 to add if clean |
| 3 | MEGA/USDT | swing | short | HOLD — active signal, TP hits | B (active) | Hold |
| 4 | ETH/USDT | swing | long | HOLD — entered, SharpLink catalyst, monitor 1532 support | B (active) | Exit if 1h close below 1532 |
| — | HEI/USDT | scalp/intraday | long | **WATCH** — best RS leader, pullback needed | watchlist | Trigger: 0.167-0.174 + volume + BTC stable |
| — | NEAR/USDT | intraday | short | **WATCH (new entry)** | watchlist | Failed bounce 1.82-1.84; SL above 1.869 |
| — | ETH/USDT | intraday | long | **WATCH-catalyst** | watchlist | 1532 hold + BTC stable; SL below 1532 |

---

## 9. Avoid / No Trade (this window only — never stop system)

- **G/USDT** — >2 ATR from EMA20, no verified catalyst, chase risk extreme.
- **UNH** — MANDATORY LEGAL AVOID. DOJ criminal + civil probe active.
- **ADA/USDT** — confirmed wallet exploit. Avoid longs.
- **No-catalyst intraday shorts** — Short bias PF 0.9. No new short entries without clear failed bounce structure.
- **Scalp entries** — Scalp mode 0W/7L PF 0.00. Skip scalp.
- **Stocks intraday** — market closed, all signals WAITING.

---

## 10. Main Risks

1. **BTC resumed decline below $60K** — Counter-trend longs (ETH/HOT/AXS/FI/WLD) face cascading stops.
2. **Catalyst mapping weak (73.9%)** — Important news may be in system but unattributed. Manual spot-checks recommended.
3. **UNH legal exposure** — DOJ probe expanding, shares -16%. Keep AVOID.
4. **ADA Cardano exploit** — Private key flaw, broader ecosystem confidence risk.
5. **Counter-trend long cluster** — 6 longs in bearish overnight regime. Correlation cluster if BTC drops hard.
6. **Scalp playbook edge missing** — 0W/7L, PF 0.00. Extra skepticism on any scalp A/B.
7. **Stocks swing audit pause** — -12R, 0W/12L. Swing capped to C/watchlist.
8. **SHORT BIAS NET NEGATIVE** — Crypto shorts PF 0.9, -3R despite bearish regime.

---

## 11. Action Plan — Next 4 Hours (04:39–08:39 EEST)

**Crypto:**
1. Do not open new positions. No A/B setups. Wait for Europe session.
2. BTC/NEAR/MEGA shorts: HOLD with existing TP/SL.
3. Counter-trend longs: Monitor vs invalidation. Exit if BTC shows renewed weakness.
4. HEI watchlist: Only if pullback to 0.167-0.174 AND volume confirms.
5. ADA: Strict AVOID.
6. G/USDT: Monitor only.

**Stocks (pre-market planning):**
7. UNH: Remove from active tracking. AVOID.
8. JPM: Re-evaluate at 09:30 ET open.
9. MSFT short: Monitor pre-market for gap direction.
10. AVGO/SMH/XLV sector: Plan intraday longs for US open.

**System:**
11. Check cycle 9 stocks invest report after 05:00 EEST.
12. Review counter-trend long invalidation levels before Europe open at ~07:00-07:30 EEST.

---

## 12. Final Verdict per Mode

| Mode | Asset class | Verdict | Rationale |
|------|-------------|---------|-----------|
| Scalp | Crypto | **WATCHLIST ONLY** | 0W/7L PF 0.00. No A/B scalp signals. |
| Intraday | Crypto | **HOLD/WATCH** | Hold NEAR/HEI (B active). No new entries until Europe open + confirmation. |
| Swing | Crypto | **HOLD** | BTC/NEAR/MEGA shorts OPEN ACTIONABLE. ETH long ENTERED UNRESOLVED. PF 2.05 — best mode. |
| Intraday | Stocks | **PLANNING ONLY** | Market closed. UNH mandatory AVOID. Re-evaluate 09:30 ET. |
| Swing | Stocks | **PAUSED** | 48h audit (-12R 0W/12L). All swing stocks capped to C/watchlist. |
| Invest | Stocks | **PENDING** | Cycle 9 invest report not yet complete. Check after 05:00 EEST. |

---

## 13. Sources

- Bitcoin ETF Outflows June 2026: $1.67B Weekly (bitcoinfoundation.org) — 6-week streak; June 23 +$39.2M potential inflection
- Bitcoin Falls as Record ETF Outflows and Strategy Sale Hit Sentiment (investing.com) — BTC sentiment context; June 24 ~$62.7K
- Bitcoin Price Recovery June 2026: Market Analysis (intellectia.ai) — Bounce off 2026 lows
- DOJ Expands Probe Into UnitedHealth's Prescription and Payment Practices (pymnts.com) — Criminal division expanding probe
- UnitedHealth Faces DOJ Expansion of Criminal Probe (ainvest.com) — DOJ criminal + civil probe scope
- SharpLink ETH purchase: t.me/lookonchain (internal news_items, single_source, chain-verifiable)
- ADA wallet exploit: AMBCrypto / internal catalyst_events (SecondFi private key flaw)
- Coinbase Base outage: CoinDesk (internal catalyst_events, resolved)
- Internal reports: scalp 04:02 · intraday 04:10 · swing 04:31 · stocks intraday 04:20 · stocks swing 04:37 (Cycle 9)

---

## 14. Fix Requests / TODO

### TODO-CATALYST-CLASSIFIER
- **issue:** 95.4% of catalyst events (460/482) classified as `other_news`. Catalyst classifier not extracting event type from most news items.
- **evidence:** `data/catalysts/2026-06-26/catalyst_cycle_01-10.md`
- **suggested manual fix:** Review event-type classifier in `src/`. Target: reduce `other_news` from 95% to <60%.
- **priority:** medium | **first observed:** 2026-06-26 04:39 EEST

### TODO-SCALP-PLAYBOOK-AUDIT
- **issue:** Crypto scalp playbook 0W/7L, PF 0.00, -7R over 14d. Edge has been negative in multiple review cycles.
- **evidence:** `src.cli signal-stats --asset-class crypto` → mode scalp: 0W/7L PF=0.00 totalR=-7.0
- **suggested manual fix:** Audit scalp entries/exits. Check TP1 distance vs captured MFE gap. Consider tightening TP1 or pausing until 20-signal re-audit.
- **priority:** high | **first observed:** 2026-06-26 04:39 EEST

### TODO-SHORT-BIAS-PERFORMANCE
- **issue:** Crypto short signals net-negative (15W/43L, PF 0.9, -3R) despite risk-off regime over 14d.
- **evidence:** `src.cli signal-stats --asset-class crypto` → direction=short: wins=15 losses=43 PF=0.929 totalR=-3.0
- **suggested manual fix:** Audit recent losing shorts. Check if entries are on initial breakdown vs retest, if stops too tight for elevated ATR. Consider requiring failed bounce retest before B-tier promotion.
- **priority:** medium | **first observed:** 2026-06-26 04:39 EEST

---

### TODO-INGEST-SOURCES-FORMAT (§Q — skipped step)
- **issue:** `scripts/ingest_enriched_review_sources.py` expects a flat JSON list but the sources artifact writes a structured object. Ingest was skipped this cycle.
- **result:** sources NOT ingested into `news_items` this cycle
- **suggested manual fix:** Update ingest script to accept structured object (extract `.sources` list). Or update skill to write flat list.
- **priority:** low | **first observed:** 2026-06-26 04:39 EEST

---

*Auto-generated by `opus-enriched-review-4h` skill · crypto_overnight slot · Advisory only — no auto-trade, no code edits, no signal registration*
