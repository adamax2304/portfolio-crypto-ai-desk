# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:40 EEST

_Generated 2026-06-24 04:40 EEST (Wednesday). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

---

## 1. Executive Summary

**Wed 2026-06-24, 04:40 EEST — crypto overnight / Asia review — advisory only / no auto-trade.**

- **SLOT: crypto overnight / Asia review.** US closed; Europe pre-open. Asia session is live driver.
- **⚠️ CATALYST MAPPING VERY WEAK — 17.4% mapped (174/1000 events). Use catalyst layer as context only, NOT as decision basis this run.**
- **Crypto: RISK-OFF confirmed.** BTC and ETH both in confirmed downtrend. Altcoin breadth 20.93% above EMA20 — extremely weak. Short bias or no trade; no weak altcoin longs.
- **Stocks: closed overnight / planning only.** All active stocks signals C-tier, WAITING FOR ENTRY. No actionable stocks until RTH open.
- **Contradiction flag — WLD:** swing short B (70.4, new today's cycle) active while historical swing long B (75, tp1) and intraday long B (71, tp1) are also tracked. Long signals appear to be from prior regime and have hit TP1; short is current-regime aligned. Lifecycle review needed.
- **Whale buying pressure ETH:** a16z withdrew $42.6M ETH from Binance + Bitmine bought $58.65M ETH (~$101M combined, t.me/lookonchain). Contradicts bearish ETH posture but does not reverse the regime.
- **Best short-watch:** WLD/USDT — failed bounce/retest 0.5417-0.5473. Price may be below entry zone now (0.5392); wait for retest before entry.
- **Best long-watch:** SOL/USDT — Korean bank stablecoin adoption catalyst, swing long B tp1 hit. Holds only if BTC stabilizes above ~$61.5K.
- **Avoid:** HEI/USDT (+67%, extreme chase); G/USDT (+12%, avoid_chase basket).

---

## 2. Data Used

| Source | File / Path | mtime EEST | Freshness |
|---|---|---|---|
| scheduler.log | `data/scheduled_runs/2026-06-24_default_schedule/scheduler.log` | 04:09 | **FRESH** (31 min) |
| Latest cycle | `cycle_01_03-21_summary.md` | 04:09 | **FRESH** (31 min) |
| Crypto scalp | `2026-06-24_00-32_scalp_report.md` | 03:32 | **FRESH** (1h8m) |
| Crypto intraday | `2026-06-24_00-40_intraday_report.md` | 03:40 | **FRESH** (1h) |
| Crypto swing | `2026-06-24_00-58_swing_report.md` | 03:58 | **FRESH** (42m) |
| Stocks intraday | `2026-06-24_00-48_stocks_intraday_report.md` | ~03:48 | **FRESH** (52m) |
| Stocks swing | `2026-06-24_01-03_stocks_swing_report.md` | ~04:03 | **FRESH** (37m) |
| Stocks invest | `2026-06-24_01-07_stocks_invest_report.md` | ~04:07 | **FRESH** (33m) |
| LLM crypto packet | `data/processed/llm_analysis_packet.md` | 00:58 UTC | **FRESH** |
| Catalyst events | `data/catalysts/2026-06-24/catalyst_events.jsonl` | cycle 1 | **FRESH** |
| Narrative baskets | `data/catalysts/2026-06-24/narrative_baskets.jsonl` | cycle 1 | **FRESH** |
| Active-signals CLI | crypto (24) + stocks (20) | 04:40 | **LIVE** |
| Untracked alerts | `detect_untracked_legacy_alerts` | 04:40 | **LIVE — 0 untracked** |
| Prior review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-23_2315.md` | 23:50 | 4h50m ago |
| Signal stats CLI | crypto + stocks | from cycle summary | **cycle data** |

**External web research: not performed this cycle.** All key candidate data available internally (news_items, catalyst_events, report data). Claims without external verification are noted as single_source per internal records.

**Blindspots:** Reddit social blocked (403) all cycle. TradingView chart MCP unavailable. Onchain config missing. Liquidation heatmaps not connected. BTC/ETH live price unknown — last OHLCV at 00:30 UTC; prior review had BTC ~$62.2K.

---

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: **04:09 EEST** (31 min ago) — within 3h threshold ✓
- Latest cycle `cycle_01_03-21_summary.md` mtime: **04:09 EEST** (31 min ago) — within 3h threshold ✓
- **NOT DEFERRED** — both freshness checks pass.
- Cycle 1 (03:21–04:09 EEST): **ok=27, failed=0** — clean run, all steps nominal.
- Paper monitor status: Open actionable=5, Waiting=1, Entered unresolved=15, Review/Shadow=187, No-entry/stale=24. Closed today: 281W / 24L / 0flat.
- Monitor background pids confirmed: crypto_monitor_1782263293, stocks_monitor_1782263293 (started 04:08).
- Catalyst label refresh: 706 labels written, 1 news flip (WLD: news_supported 0→1).
- Integrity check: 17 high-importance symbols not mapped into catalyst_events (ALGO, AMZN, BCH, BNB, COIN, DOGE, DOT, FIL, GOOGL, HBAR and 7 more).

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-06-24 04:40 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "derivatives_sparse", "onchain_config_missing"],
      "data_missing": ["reddit_social_blocked", "onchain_data_config_missing", "btc_eth_live_price", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log 04:09 EEST — FRESH (31 min)",
        "cycle_01 finished 04:09 EEST — FRESH, ok=27/27",
        "All crypto/stocks reports fresh <2h",
        "Catalyst events 1000 rows present in JSONL",
        "Derivatives: fallback_via_mexc for most symbols, OI missing for several",
        "Onchain: interface_ready_config_missing (no config/onchain.yaml)",
        "Reddit: 403 blocked all cycle"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.87,
      "reason_codes": ["risk_off", "shorts_preferred"],
      "data_missing": ["btc_eth_live_price", "social_sentiment"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: downtrend (all three reports)",
        "ETH trend: downtrend (all three reports)",
        "Altcoin breadth above EMA20: 20.93% (scalp/intraday) — extremely weak",
        "All reports: recommended trading style = short bias or no trade",
        "Stocks: chop, VIX 19.49, breadth 50% above EMA20, neutral bias",
        "SPY range 5d=-2.82%, QQQ range 5d=-4.08% — tech in drawdown",
        "Prior review: BTC ~$62.2K, ETH ~$1,720",
        "Squeeze phases: 31 post-unwind chop dominant"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.45,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_contradicted"],
      "data_missing": ["symbol_resolver_weak", "reddit_blocked", "high_importance_unmapped_17"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Catalyst events file: 1000 rows, 174 mapped (17.4%) — VERY WEAK",
        "826/1000 events have empty symbol field",
        "Integrity check: 17 high-importance symbol-tagged catalysts not mapping",
        "Key mapped catalysts: ETH whale buying (a16z $42.6M + Bitmine $58.65M, t.me/lookonchain), SOL Korean bank stablecoin, ADA SecondFi hack $2.4M, ETH L2 bridge failure",
        "WLD: news_supported flipped 0->1 in label refresh (direction unclear, mapping weak)",
        "BTC: $10.6B options expiry + below $63K + ETF outflows (The Block)",
        "Clarity Act: Senate negotiations uncertain, multiple opposition groups",
        "Narrative baskets: delisting_thin_liquidity, ai_narrative, perps_dex_narrative, momentum_breakout"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["post_unwind_chop", "squeeze_risk", "oi_contradicts", "data_unavailable"],
      "data_missing": ["oi_data_incomplete_mexc_fallback", "liquidation_flows", "funding_history"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Squeeze phase dist: 31 post-unwind chop, 7 build-up, 2 squeeze expansion, 6 unwind, 41 unknown (87 symbols)",
        "HEI: OI +62.86%, price up + OI up = fresh positioning — squeeze expansion candidate",
        "G/USDT: OI +130.46%, price up + OI up = crowding risk (unknown crowding label)",
        "WLD: price down + OI up = fresh shorts pressing, squeeze risk if BTC reclaims",
        "ID/USDT: OI -30.2%, price down + OI down = deleveraging/long liquidation",
        "Most OI data via fallback_via_mexc — incomplete"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["price_moved_away", "overextended", "clean_retest", "entry_fresh"],
      "data_missing": ["chart_mcp_unavailable", "live_price_unknown"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "WLD swing short entry zone 0.5417-0.5473; last price in report 0.5392 — price BELOW entry (moved away or at low)",
        "BTC swing short tp1 hit — entered, in partial profit territory",
        "ETH swing long tp1 hit — entered",
        "SOL swing long tp1 hit — entered",
        "HEI: +67% 24h — massively overextended; tagged overextended in intraday; momentum_breakout basket = avoid_chase",
        "G/USDT: +12% 24h, momentum_breakout basket; entry would be late",
        "WLD short: entry valid IF price retests 0.5417-0.5473 zone",
        "ATR BTC: 46th percentile — normal volatility"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["open_actionable", "entered_unresolved", "review_shadow", "needs_review"],
      "data_missing": ["individual_signal_ids_truncated_in_cli"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Paper monitor: OPEN ACTIONABLE=5, WAITING FOR ENTRY=1, ENTERED UNRESOLVED=15, REVIEW/SHADOW=187, NO-ENTRY/STALE=24",
        "Closed today (paper): 281W / 24L / 0flat",
        "Untracked legacy alerts today: 0 (clean)",
        "WLD: 3 short signals (swing, scalp, intraday) + 2 long signals (intraday, swing) simultaneously active — long signals at tp1 from prior regime",
        "Prior 2 ETH B swing short untracked alerts (2026-06-23) — not carried into today",
        "Stocks: 20 signals all C-tier, all WAITING FOR ENTRY (market closed)",
        "Cycle 1: ok=27/27 — clean run"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["repeated_losses", "correlation_cluster", "headline_risk"],
      "data_missing": ["daily_pnl_exact", "drawdown_limit_status"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto intraday: WR 2%, PF 0.12, totalR=-7R this week — net-negative bucket",
        "Crypto swing: PF 0.65, totalR=-12R this week — losing",
        "Crypto scalp: PF 1.61, totalR=+11R — positive (keep running)",
        "Stocks A/B headline: 0W/6L, PF=0.0, totalR=-6R (weak sample n=15)",
        "15 entered-unresolved signals — correlation cluster; BTC gap-down = multiple concurrent stops",
        "ADA: SecondFi wallet hack $2.4M — active headline risk",
        "ETH: L2 bridge failure headline — infrastructure risk narrative",
        "Clarity Act: regulatory uncertainty for crypto sector",
        "Stocks swing cap persists: -12R, 0W/12L audit"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": ["playbook_breakdown_by_name_truncated_in_cli"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Mode scalp n=38, PF=1.61, totalR=+11R — WORKING",
        "Mode intraday n=65, PF=0.12, totalR=-7R — FAILING",
        "Mode swing n=58, PF=0.65, totalR=-12R — FAILING",
        "Setup 1 (likely RS-momentum): n=36, PF=1.35, totalR=+3R — working",
        "Setup 2: n=9, PF=0.0, totalR=-5R — 0 wins — failing badly",
        "Setup 3 (likely failed bounce): n=116, PF=0.83, totalR=-6R — negative",
        "Stocks B-tier: n=15 weak sample, 0W/6L — failing but insufficient data",
        "crypto_swing_narrative_rs_momentum: 14d WR 72% / PF 5.80 / +24R per report (best playbook)",
        "Scalp remains data-collection mode; re-audit at 20 closed A/B scalp signals"
      ]
    },
    {
      "agent": "head_trader",
      "overall_verdict": "caution",
      "confidence": 0.68,
      "preferred_side": "shorts",
      "best_long_candidate": {
        "symbol": "SOL/USDT",
        "trigger": "BTC holds above ~$61.5K at Asia open + SOL shows relative strength vs BTC; swing long B tp1 already entered — monitor/trail",
        "reason": "Korean bank stablecoin adoption catalyst (fresh, CryptoSlate); RS vs BTC +10-11%; swing long B tp1 hit; cleanest catalyst-backed long in risk-off environment"
      },
      "best_short_candidate": {
        "symbol": "WLD/USDT",
        "trigger": "Failed bounce/retest into 0.5417-0.5473 with rejection candle + volume confirmation; do NOT short below current 0.5392",
        "reason": "Swing short B 70.4 (today's cycle); bearish vs BTC -12%; OI building on short side; regime-aligned; no verified catalyst; wait for retest"
      },
      "best_catalyst_candidate": {
        "symbol": "ETH/USDT",
        "trigger": "Sustained hold above 1,750 OR L2 bridge resolution confirmed via primary source + price reclaims EMA20",
        "reason": "$101M whale accumulation (a16z $42.6M + Bitmine $58.65M) creates genuine counter-pressure; MANUAL REVIEW REQUIRED — NOT actionable now given L2 bridge failure and $170M longs liquidated"
      },
      "avoid_candidate": {
        "symbol": "HEI/USDT",
        "reason": "+67% 24h move; momentum_breakout basket (playbook: avoid_chase); OI +63% — entry now is pure chase into extended move without retest"
      },
      "operator_action": "watch",
      "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
      "todo_count": 3
    }
  ]
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh, derivatives_sparse, onchain_config_missing | advisory_only |
| market_regime | caution | 0.87 | risk_off, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.45 | mapping_weak, fresh_catalyst, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.55 | post_unwind_chop, squeeze_risk, oi_contradicts, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | price_moved_away, overextended, clean_retest, entry_fresh | advisory_only |
| execution_lifecycle | ok | 0.75 | open_actionable, entered_unresolved, review_shadow, needs_review | advisory_only |
| risk_manager | caution | 0.72 | repeated_losses, correlation_cluster, headline_risk | advisory_only |
| playbook_performance | caution | 0.68 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | — (synthesiser) | 0.68 | overall_verdict=caution, preferred_side=shorts | advisory_only |

---

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-23_2315.md` (23:24 EEST, 5h16m ago).

| Change | Detail |
|---|---|
| **Cycle completed** | Cycle 1 of 2026-06-24 ran (03:21–04:09 EEST), ok=27/27 vs cycle 7 prior had ok=21/failed=1 |
| **New signals** | WLD swing short B (70.4) generated in today's swing report; total 24 active vs 20 prior |
| **HEI pump** | HEI/USDT +67% 24h; momentum_breakout basket activated (avoid_chase playbook) |
| **G/USDT** | +12-14% today; OI +130% — crowding risk elevated |
| **WLD catalyst flip** | news_supported 0→1 (catalyst label refresh) — direction unclear, mapping weak |
| **SOL catalyst** | South Korean bank (15M users) stablecoin adoption confirmed in cycle 1 |
| **ETH whale buying** | a16z $42.6M + Bitmine $58.65M ETH buys confirmed in news_items (t.me/lookonchain) |
| **Untracked alerts** | 0 today (vs 2 ETH swing short untracked in prior review — resolved/clear) |
| **Stocks swing cap** | Watchlist-only cap persists from audit: -12R, 0W/12L |
| **BTC options expiry** | $10.6B BTC options expiry today — quarter-end event |
| **NEAR lifecycle** | NEAR intraday short B (tp1) + swing long B (tp1) both active — same lifecycle pattern as WLD |

---

## 5. Catalyst Coverage

**⚠️ CATALYST MAPPING VERY WEAK THIS RUN (17.4% mapped) — use catalyst layer as context, not final decision.**

- Total catalyst events in file today: **1,000**
- Mapped (non-empty symbol): **174 (17.4%)**
- Unmapped (empty symbol): **826 (82.6%)** — far above 50% threshold
- Narrative baskets: **4** (delisting_thin_liquidity, ai_narrative, perps_dex_narrative, momentum_breakout)
- Integrity warning: **17 high-importance symbol-tagged catalysts not mapped** into catalyst_events (ALGO, AMZN, BCH, BNB, COIN, DOGE, DOT, FIL, GOOGL, HBAR + 7 more)

**Top 3 unmapped headlines (from file head):**
1. "Matt Freese reflects on World Cup debut and eyes Türkiye rematch" — sports news misrouted to crypto catalyst file
2. "OpenAI faces scrutiny over Sam Altman's investment ties" — tech/CryptoBriefing, no symbol mapped
3. "Gold extends decline as tech-led selloff prompts investor liquidation" — macro, no symbol mapped

**Key MAPPED catalysts:**
- **ETH:** L2 bridge failure (CryptoSlate); $170M longs liquidated (Cointelegraph); whale buying a16z +$42.6M + Bitmine +$58.65M (t.me/lookonchain)
- **BTC:** $10.6B options expiry, below $63K, ETF outflows (The Block); quantum-resistance concern (Decrypt)
- **SOL:** South Korean digital bank (15M users) stablecoin adoption (CryptoSlate)
- **ADA:** SecondFi wallet vulnerability, $2.4M drained (CryptoBriefing) — headline risk
- **ENA:** "13% rally wiped out" (AMBCrypto) — bearish narrative for this signal
- **WLD:** news_supported flipped 0→1 (internal catalyst label refresh); actual article not identified

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood: risk-off** — BTC downtrend, ETH downtrend, altcoin breadth 20.93% above EMA20 (extremely weak). $170M ETH longs liquidated overnight. BTC below $63K with ETF outflows and $10.6B options expiry today.
- **Stocks mood: closed / planning** — US market closed until 09:30 ET (16:30 EEST). All signals C-tier WAITING FOR ENTRY. Chop regime: VIX 19.49, SPY range, QQQ range. Strong sectors: semiconductors (+7.93% 20d), financials (+3.74%), industrials (+3.71%). Weak: energy (-8.46%), communications (-7.09%).
- **Dominant narrative:** Bearish crypto liquidation cascade; regulatory uncertainty (Clarity Act Senate delays); ETH whale accumulation as counter-narrative; AI narrative basket active but weak (heat 28-30/100); BTC options expiry creating vol uncertainty today.
- **Preferred side now:** Shorts (WLD retest, ENA continuation) with extreme caution on new longs until BTC/ETH stabilize. No new crypto intraday (PF 0.12 this week).
- **Best long candidate:** SOL/USDT — Korean bank catalyst, swing long B tp1 entered, best catalyst-backed long this window.
- **Best short candidate:** WLD/USDT — failed bounce/retest setup, swing short B new, regime-aligned. Wait for retest to 0.5417-0.5473.
- **Best catalyst-backed candidate:** ETH/USDT — $101M whale buying creates support; MANUAL REVIEW. Trigger: hold above 1,750 + L2 bridge issue confirmed contained.
- **What to avoid:** HEI (+67%, extreme chase); G/USDT (+12%, avoid_chase); no new crypto intraday (net-negative playbook); no new stocks B positions.
- **What would change the view:** BTC reclaims above $63.5K + altcoin breadth recovers above 35% → longs more viable; BTC loses $61K → deepen short bias, increase WLD/ENA squeeze monitoring.

---

## 7. Candidate Deep Dives

### Candidate 1: WLD/USDT — Swing Short B (70.4) — WAITING FOR ENTRY

**Status:** WAITING FOR ENTRY (price below entry zone; wait for retest up)

- Mode: swing short; Entry zone: 0.5417–0.5473; Invalidation: 1h close above 0.5541
- TP1: 0.5268 | TP2: 0.5143 | TP3: 0.5019
- Last price (OHLCV ~00:30 UTC): ~0.5392 — BELOW entry zone → price moved away or at local low
- ATR: 0.0124 | Support: 0.5337 | Resistance: 0.6129
- 24h return: -13.25% to -14.06%; 7d return: -20.88% to -21.8%; RS vs BTC: -11.1% to -12.2%
- Derivatives: price down + OI up = fresh shorts pressing; funding -0.00012; crowding normal

**Contradiction flag:** WLD has swing short B (70.4, new) AND swing long B (75, tp1) AND intraday long B (71, tp1) simultaneously active. Long signals are from prior regime that hit TP1 before today's -14% move — NOT a current competing thesis. But lifecycle should close/resolve these longs.

**news_supported flip:** Catalyst label refresh shows WLD news_supported 0→1 but actual article unidentified (82.6% unmapped). Cannot confirm direction. Treat as unknown catalyst risk — do NOT use as confirming signal.

**Price reaction / chase check:** Price already -14% today. Entry requires RETEST UPWARD to 0.5417-0.5473 first — NOT a chase. Entry is valid only on retest + rejection candle. Do not short below 0.5392.

**Verdict:** WAITING FOR ENTRY. Best short-watch this window. Valid only on retest.

---

### Candidate 2: ETH/USDT — Swing Long B (66 score, tp1) — MANUAL REVIEW REQUIRED

**Status:** ENTERED UNRESOLVED (tp1 hit; contradicted by macro + headline risk)

**Two competing forces:**
- **BEARISH:** ETH downtrend confirmed; $170M longs liquidated overnight; L2 bridge failure headline (CryptoSlate: "pull funds... exposes rollup exit risk"); altcoin breadth 20.93% above EMA20
- **BULLISH counter:** a16z withdrew 25,560 ETH ($42.6M) from Binance + Bitmine bought 35,138 ETH ($58.65M) = $101M+ institutional accumulation (t.me/lookonchain, within last 9h). Classic smart-money absorption of liquidation event.

**Evidence:**
- ETH 24h: -7.90% to -8.32%; RS vs BTC: -5.95% to -6.24% — underperforming
- Playbook was crypto_swing_narrative_rs_momentum (best 14d playbook) but L2 failure narrative is headwind
- L2 bridge failure: potential infrastructure narrative risk if contagion builds

**Chase check:** Existing swing long at tp1 — position entered before. Do not add new exposure now. Trigger for new long: ETH holds above 1,750 sustainably + L2 bridge failure confirmed contained.

**Verdict:** MANUAL REVIEW REQUIRED. Existing tp1 position — manage/trail. No new long entry. $101M whale buying is real but insufficient counter to current regime alone.

---

### Candidate 3: BTC/USDT — Swing Short B (65 score, tp1) — MONITOR

**Status:** ENTERED UNRESOLVED / tp1 hit

- BTC trend: DOWNTREND (all reports)
- Last known price: ~$62.2K (from prior review); below $63K resistance
- $10.6B options expiry today (quarter-end) — gamma hedging uncertainty; could spike either direction post-expiry
- ETF outflows confirmed (The Block)
- ETH whale buying may signal broader institutional appetite beginning — watch as a leading indicator
- ATR: 46th percentile — normal volatility

**Verdict:** ENTERED UNRESOLVED, tp1 reached. Trail stop to breakeven. Watch $63.5K as invalidation proxy. Options expiry may cause volatility spike at US open (16:00+ EEST) — be aware.

---

### Candidate 4: SOL/USDT — Swing Long B (68 score, tp1) — MONITOR EXISTING

**Status:** ENTERED UNRESOLVED / tp1 hit (~73X USDT)

- Catalyst: "South Korean digital bank with 15M users turns to Solana stablecoins for overseas transfers" — CryptoSlate, collected this cycle, single_source
- 24h: RS positive vs BTC (+10-11% RS) — RS leader in risk-off environment
- Playbook: crypto_swing_narrative_rs_momentum — best 14d playbook (WR 72%, PF 5.80, +24R)
- Catalyst-backed + RS leader = cleanest long profile in current market

**Chase check:** Existing position at tp1 — monitor and trail. No new entry at tp1 level; wait for pullback to support 72.X-73.X if adding. Invalidation: BTC loses $61K.

**Verdict:** ENTERED UNRESOLVED, tp1 hit. Best catalyst-backed active position. Trail stop, no new chase at current levels.

---

### Candidate 5: HEI/USDT — AVOID COMPLETELY

**Status:** Not in active trade signals. Momentum_breakout basket watch only.

- 24h return: +64-69% (extreme across all reports)
- RS vs BTC: +66-71% — anomalous outlier, no verified fundamental catalyst
- Derivatives: OI +62.86%, price up + OI up = fresh positioning, funding -0.00199 (negative = longs paying, shorts crowding)
- Momentum basket: momentum_breakout, playbook = avoid_chase (fresh <1h)

**Why AVOID:** +67% with negative funding = thin market/possible manipulation; any entry is pure chase; momentum_breakout basket explicitly uses avoid_chase playbook; OI surge without verified catalyst = crowding risk.

**Verdict:** AVOID COMPLETELY this window. No entry until major pullback (-30%+) + OI reset + verified catalyst.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Side | Status | Verdict | Trigger |
|---|---|---|---|---|---|
| 1 | WLD/USDT | Short | WAITING FOR ENTRY | Wait for retest | Retest 0.5417-0.5473 + rejection |
| 2 | SOL/USDT | Long | ENTERED (tp1 hit) | Monitor/trail | BTC stable above $61.5K |
| 3 | BTC/USDT | Short | ENTERED (tp1 hit) | Monitor/trail | Stay below $63K; trail to BE |
| 4 | ETH/USDT | Long | ENTERED (tp1 hit) | Manual review | Hold above 1,750 + L2 contained |
| 5 | ENA/USDT | Short | ENTERED (trending) | Monitor | Trending; watch squeeze risk |

**Best long-watch (not yet entered):** SOL/USDT pullback to 72.X-73.X support zone. Trigger: clean base formation + BTC holds $61.5K + Korean bank catalyst confirmed via second source.

**Best short-watch:** WLD/USDT — retest to 0.5417-0.5473 with rejection candle. Current price below zone; do not rush. This is the regime-aligned entry for the Asia session.

**Best catalyst-watch:** ETH/USDT — $101M institutional accumulation is the cleanest pending catalyst. Monitor t.me/lookonchain for follow-on buys or L2 bridge resolution.

---

## 9. Avoid / No Trade

This decision window only (04:40–08:40 EEST). System continues scanning in all moods.

- **HEI/USDT:** +67% — hard avoid (momentum_breakout basket = avoid_chase)
- **G/USDT:** +12% today, OI +130%, momentum_breakout basket — avoid_chase; entry late
- **ID/USDT:** -15%, OI -30% (deleveraging) — do not long into liquidation flush
- **ADA/USDT:** SecondFi wallet hack active headline risk — avoid until contained
- **No new crypto INTRADAY:** PF=0.12, WR=2%, -7R this week — do not add new intraday signals
- **No new stocks B positions:** stocks swing watchlist-only; intraday all C-tier; market closed

---

## 10. Main Risks

1. **BTC options expiry today ($10.6B, quarter-end):** Volatility spike risk at US open (16:00+ EEST). Gamma hedging could cause squeeze or extension; existing shorts could face sudden pop.
2. **ETH L2 bridge failure escalation:** If CryptoSlate headline expands into broader ETH security narrative, swing long B positions are at risk. Monitor follow-up headlines.
3. **WLD squeeze risk:** OI building on short side = squeeze possible if BTC/ETH recover. Invalidation at 0.5541 (1h close). Do not size up before confirmation.
4. **15 entered-unresolved / correlation cluster:** BTC gap-down could simultaneously stop out multiple positions. Effective drawdown could exceed individual position sizing.
5. **Catalyst mapping failure (17.4%):** 17 high-importance symbols confirmed not mapping (integrity scan). Missed catalysts could blindside active positions in ALGO, BNB, COIN, GOOGL, etc.
6. **HEI manipulation dump risk:** Negative funding + +67% pump = potential sharp reversal coming. No active HEI position, but sentiment bleed possible.
7. **Clarity Act regulatory uncertainty:** Any negative Senate vote = sector-wide crypto selloff risk.

---

## 11. Action Plan — Next 4 Hours (04:40–08:40 EEST)

1. **WLD/USDT:** Watch for bounce/retest to 0.5417-0.5473. If price returns with rejection candle + declining volume → swing short B entry valid. Do not enter below 0.5417.
2. **SOL/USDT:** Trail existing swing long B. BTC above $61.5K = hold. BTC loses $61K = exit or tighten aggressively.
3. **ETH/USDT:** Existing tp1 position — monitor only. Read any ETH L2 bridge follow-up headlines if they appear.
4. **BTC/USDT:** Trail existing swing short B. Move stop to breakeven. Options expiry watch at US open.
5. **ENA/USDT:** Existing shorts (swing + intraday, trending). Funding elevated negative. Watch for squeeze indicator (price reclaims key level).
6. **No new entries:** HEI, G, ID, DASH, ADA, any new intraday, any new stocks.
7. **Next review:** 11:30 EEST (Europe / pre-US context) — re-evaluate all active B-tier signals with fresh cycle data.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Reasoning |
|---|---|---|
| **crypto scalp** | CAUTION / data-collection | PF 1.61 (+11R) but low sample (n=38). WLD scalp short at tp1 — monitor. Re-audit at 20 A/B scalp signals. |
| **crypto intraday** | AVOID NEW ENTRIES | PF 0.12 (-7R this week). Existing NEAR/WLD intraday shorts at tp1 — monitor only; zero new intraday. |
| **crypto swing** | SELECTIVE — MANAGE EXISTING | PF 0.65 (-12R). WLD swing short new/valid (wait retest). SOL/ETH/BTC/ENA existing — trail and manage. |
| **stocks intraday** | PLANNING ONLY | Market closed. C-tier WAITING FOR ENTRY. UNH B-tier (74.73) — track at RTH open. |
| **stocks swing** | WATCHLIST ONLY | 48h audit cap continues: -12R, 0W/12L. JPM B (65.32) and LLY B (65.31) noted for research. |
| **stocks invest** | WATCHLIST / RESEARCH | LLY, JPM, AMD long setups noted. Not tradeable until swing audit cap lifted. |

---

## 13. Sources

All sources internal this cycle (external web research not performed — all key data available in news_items and catalyst_events):

1. SecondFi wallet vulnerability draining $2.4M ADA — CryptoBriefing, 2026-06-24, single_source (internal)
2. ETH L2 bridge failure / rollup exit risk — CryptoSlate, 2026-06-24, single_source (internal)
3. $170M ETH longs liquidated — Cointelegraph, 2026-06-24, single_source (internal)
4. a16z bought 25,560 ETH ($42.6M) from Binance — t.me/lookonchain, 2026-06-24, single_source/social (internal news_items)
5. Bitmine bought 35,138 ETH ($58.65M) from BitGo + Kraken — t.me/lookonchain, 2026-06-24, single_source/social (internal news_items)
6. South Korean digital bank (15M users) Solana stablecoins — CryptoSlate, 2026-06-24, single_source (internal)
7. BTC $10.6B options expiry, below $63K, ETF outflows — The Block, 2026-06-24, single_source (internal)
8. Clarity Act Senate uncertainty — CoinDesk + CryptoBriefing + Decrypt, 2026-06-24, multi-source (internal)
9. ENA rally wiped out — AMBCrypto, 2026-06-24, single_source (internal)
10. BTC quantum-resistance concern — Decrypt, 2026-06-24, single_source (internal)
11. Cycle 1 summary — `data/scheduled_runs/2026-06-24_default_schedule/cycle_01_03-21_summary.md`, 2026-06-24 04:09 EEST
12. Prior review — `OPUS_ENRICHED_REVIEW_AUTO_2026-06-23_2315.md`, 2026-06-23 23:24 EEST

All verification statuses: single_source (unless noted multi-source). No fabricated chart observations. No uncited statistics. External web research unavailable this slot — flagged in §1 and §2.

---

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-chronic
- **issue:** Catalyst mapping ratio chronically very low — this run 17.4% (174/1000). Integrity scan confirms 17 high-importance symbol-tagged articles not mapping into catalyst_events. Sports/general news (World Cup match reports) being ingested as crypto catalyst events.
- **evidence:** `data/catalysts/2026-06-24/catalyst_events.jsonl` — 826/1000 empty symbol; cycle_01 step 5 integrity scan warning: "17 high-importance symbol-tagged catalysts not mapped"
- **suggested manual fix:** Audit catalyst symbol resolver (`src/` catalyst layer) to improve named-entity extraction for crypto symbols; add filter to exclude non-crypto sports/macro articles from crypto catalyst JSONL; investigate why 17 high-importance internally-tagged items are not resolving
- **priority:** high
- **first observed:** recurring across multiple runs; confirmed 2026-06-24 04:40 EEST

### TODO-wld-lifecycle-contradiction
- **issue:** WLD simultaneously shows swing short B (70.4, new, trending) AND swing long B (75, tp1) AND intraday long B (71, tp1) as active signals. Long signals from prior regime that hit TP1 remain open alongside new opposing-direction signal. Same pattern observed for NEAR (intraday short + swing long both at tp1).
- **evidence:** `python -m src.cli active-signals --asset-class crypto` output 2026-06-24 04:40 — WLD appears 5 times with conflicting directions/modes; NEAR appears twice with conflicting directions
- **suggested manual fix:** Investigate signal lifecycle: if a signal hits tp1 and a new opposing-direction signal is generated, the old signal should either close or be moved to explicit ENTERED UNRESOLVED status. Consider adding "conflicting direction" lifecycle flag in the signal generator.
- **priority:** medium
- **first observed:** 2026-06-24 04:40 EEST

### TODO-ingest-script-schema-mismatch
- **issue:** `python -m scripts.ingest_enriched_review_sources` failed with schema error when passed the sources JSON built this run. Script's `_load_input` function rejected the JSON structure.
- **evidence:** Exit code 1; `scripts/ingest_enriched_review_sources.py:95 _load_input` raised error on `data/raw/enriched_review_sources/2026-06-24T04-40-00.json`
- **suggested manual fix:** Check the expected JSON schema in `scripts/ingest_enriched_review_sources.py` (around line 95) and align the review-sources JSON template accordingly. The sources JSON file has been written to `data/raw/enriched_review_sources/` for manual inspection.
- **priority:** low (ingest is optional enrichment, review was completed)
- **first observed:** 2026-06-24 04:40 EEST

### TODO-derivatives-oi-incomplete
- **issue:** Most OI data falling back to mexc (fallback_via_mexc) with `OI 24h n/a%` for majority of symbols. Bybit OI endpoint appears not returning OI data for non-primary Bybit symbols in intraday/scalp mode.
- **evidence:** Intraday report derivatives section shows `fallback_via_mexc` for G, SYN, DASH, OPG, VIC, RE, HEI, ID — all with `OI 24h n/a%`. Only symbols with Bybit perps have actual OI 24h data (e.g., BTC, ETH in swing report).
- **suggested manual fix:** Check `src/` derivatives fetch code for Bybit OI endpoint; investigate whether the fallback trigger is too aggressive; review if mexc fallback should also attempt to pull OI (currently returning n/a).
- **priority:** medium
- **first observed:** 2026-06-24 04:40 EEST (likely persistent across runs)
