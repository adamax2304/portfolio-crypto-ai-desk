# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:39 EEST

**Slot:** crypto overnight / Asia review | **Time:** 2026-07-04 04:39 EEST
**Cycle:** 01 (03:54 start → 04:19 finish, 29/29 steps OK, 0 failures)
**Previous review:** 2026-07-03 23:24 EEST (post-close final daily review)
**Advisory only — no auto-trade.**

---

## 1. Executive Summary

This is the **crypto overnight / Asia review** slot (04:30 EEST) for Saturday July 4, 2026. Advisory only — no auto-trade. Stocks are CLOSED (US Independence Day weekend).

**Critical finding:** TLM/USDT is the system's #1 swing pick (72.4/100) but is under **Binance delisting monitoring** (flagged May 22, 2026). This is a HEADLINE RISK — do NOT enter TLM long. SYN/USDT is also on the same Binance Watch Label, which explains its -17.5% overnight decline.

Market regime is bullish trend (BTC uptrend, ETH uptrend, 82-85% alts above EMA20, F&G=22). However, weekend mode signals historically underperform (PF=0.9, WR=13.4% vs weekday PF=4.2). No A-tier signals exist. All active signals are B-tier longs with low confidence.

Strongest RS leaders (no delist/crowding issue): **ADA** is the cleanest active swing B with multi-exchange confirmation and no contradiction risk. **XRP** has a confirmed catalyst (Upbit volume > BTC on July 3) and is a C-tier catalyst watch. **ARPA** shows extreme OI (+184%) and elevated crowding — caution for new longs despite strong price action.

Preferred action: paper-watch ADA at pullback zone (0.1761–0.1787); catalyst-watch XRP at 1.129–1.133; do NOT chase TLM, HMSTR, or ARPA at current price.

---

## 2. Data Used

| Source | Age | Freshness |
|---|---|---|
| scheduler.log | 20 min | FRESH |
| cycle_01_03-54 summary | 20 min | FRESH (29/29 OK) |
| scalp report | 39 min | FRESH |
| intraday report | 34 min | FRESH |
| swing report | 23 min | FRESH |
| stocks intraday (07/03 23:07) | 5.5h | CARRY-FORWARD — market CLOSED Saturday |
| stocks swing (07/02 16:03) | ~36h | STALE — weekend |
| stocks invest (07/02 16:05) | ~36h | STALE — weekend |
| catalyst_events today | <2h (cycle) | FRESH (414–424 events, 4 baskets) |
| LLM packet | synced in cycle | FRESH |
| active-signals CLI | run now | 50 crypto B-tier active |
| signal-stats CLI | run now | week: PF=2.72, WR=19.9%, +51.68R |

External web research: available and used. Sources in §13.

**Stocks** excluded from final verdicts — US Independence Day weekend, no fresh data.

---

## 3. Scheduler / Data Freshness

- **Scheduler:** FRESH. Cycle 01 completed at 04:19 EEST (29/29 OK, 0 failed). Monitor PID active (90-min background window).
- **Paper monitor:** Open actionable=24, Waiting=7, Entered unresolved=43, Review/Shadow=179, No-entry/stale/moved-away=59, Closed=359W/21L/0flat, Needs review=0.
- **Untracked legacy alerts:** 0 (clean — previous cycle 22 now resolved/recalculated post-new-cycle).
- **Paper shadow:** ALL: A net −149.62R / B net +38.96R. Forward-valid: A −92.06R / B +55.39R. Shadow gate NOT_READY (4/6 lanes); no promotion.
- **Onchain:** config missing (no config/onchain.yaml) — interface ready but disabled.
- **Social attention:** MISSING. Reddit blocked (403 all three subreddits). Social context unavailable.
- **Bybit/OKX derivatives cross-check:** available for HMSTR, THE, ARPA, KITE, MANA in intraday report.

**Squeeze phase distribution (115 symbols):** phase_5_post_unwind_chop=33, phase_1_build_up=26, phase_0_unknown=48, phase_2_squeeze_expansion=4, phase_4_unwind=3, phase_3_distribution=1.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-04 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["social_attention", "onchain_config", "reddit_feeds"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.72,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"],
      "data_missing": ["etf_flows_today", "dxy_live"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["fresh_catalyst", "catalyst_contradicted", "mapping_weak"],
      "data_missing": ["tlm_delist_mapping", "syn_delist_mapping"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "funding_extreme"],
      "data_missing": ["liquidation_heatmaps"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["chase_risk", "overextended", "stale_before_entry"],
      "data_missing": ["tradingview_chart"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.78,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved"],
      "data_missing": [],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["headline_risk", "manual_review", "correlation_cluster"],
      "data_missing": ["daily_pnl_live"],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only"
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.73,
      "reason_codes": ["wait_for_trigger", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only"
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.73,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "ADA/USDT",
      "trigger": "pullback into 0.1761-0.1787 zone on 15m-1h structure",
      "reason": "cleanest B-tier swing long: no delist risk, multi-exchange confirmed, OI fresh"
    },
    "best_short_candidate": {
      "symbol": "SYN/USDT",
      "trigger": "failed bounce above ~0.60 on 4h close; NOT a fresh short here",
      "reason": "Binance Watch Label active, but currently extended short with squeeze risk"
    },
    "best_catalyst_candidate": {
      "symbol": "XRP/USDT",
      "trigger": "pullback into 1.129-1.133 zone with Upbit volume sustaining",
      "reason": "Upbit volume > BTC confirmed July 3, Korean market driver"
    },
    "avoid_candidate": {
      "symbol": "TLM/USDT",
      "reason": "Binance delisting monitoring active — pump likely delisting-driven"
    },
    "operator_action": "watch",
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh, report_stale (stocks stale weekend) | advisory_only |
| market_regime | ok | 0.72 | risk_on, longs_preferred, mixed (F&G fear divergence) | advisory_only |
| catalyst_narrative | caution | 0.65 | fresh_catalyst (XRP), catalyst_contradicted (TLM delist), mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.70 | squeeze_risk (ARPA/ZKP), oi_contradicts, funding_extreme (ZKP -0.00565) | advisory_only |
| technical_entry | caution | 0.68 | chase_risk (TLM/HMSTR), overextended, stale_before_entry (ARPA) | advisory_only |
| execution_lifecycle | ok | 0.78 | open_actionable=24, waiting=7, entered_unresolved=43 | advisory_only |
| risk_manager | caution | 0.75 | headline_risk (TLM/SYN delist), manual_review, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.72 | playbook_working (swing 14d WR 72%), playbook_failing (weekend PF=0.9) | advisory_only |
| head_trader | caution | 0.73 | wait_for_trigger (ADA/XRP pullback), longs_preferred (not TLM) | advisory_only |

---

## 4. What Changed vs Previous Review (2026-07-03 23:24)

| Change | Detail |
|---|---|
| New cycle generated | 50 active signals (was 20 in 23:24 review) |
| TLM/swing now #1 pick | 72.4/100 — new this cycle; HEADLINE RISK discovered via external research |
| ARPA 3xTP (prev) then new ARPA signals | Previous: ARPA 3xTP hit, moved away. This cycle: new ARPA swing/intraday/scalp signals generated |
| ZKP swing TP hit (prev) then C-tier | ZKP now C-tier watchlist only (64.9/100) |
| NEAR news_supported flip | AI narrative basket fresh — confirmed in cycle 06 label refresh |
| Untracked alerts | 22 in previous review — 0 now (recalculated after new full cycle) |
| Paper actionable +10 | 14 — 24 open actionable |

---

## 5. Catalyst Coverage

- **Today's events:** 411–424 (scalp/swing timing difference)
- **Baskets:** 4 (delisting_thin_liquidity, perps_dex_narrative, ai_narrative, momentum_breakout)
- **Integrity report:** 29 mapped / 5 unmapped (AAVE, AVAX, BNB, GOOGL, OP). Below 50% threshold — no flag.
- **Critical gap:** TLM Binance Watch Label NOT in catalyst_events.jsonl for TLM. SYN Watch Label also missing.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-on (bullish trend) with structural caution (F&G=22 Fear divergence)
- **Stocks mood:** CLOSED — US Independence Day Saturday weekend. Next open Monday July 6, 09:30 ET.
- **Dominant narrative:** Binance delisting-monitoring headline (TLM/SYN); crypto derivatives squeeze (ARPA/ZKP); XRP Korean market volume leadership; weekend alt continuation
- **Preferred side now:** longs on pullback at RS leaders (NOT extended) — wait for confirmation
- **Best long candidate:** ADA/USDT — pullback into 0.1761–0.1787, no delist risk, multi-exchange confirmed
- **Best short candidate:** SYN/USDT — failed bounce above ~0.60 on 4h (NOT now — squeeze risk)
- **Best catalyst-backed candidate:** XRP/USDT — Upbit volume > BTC confirmed July 3; pullback 1.129–1.133
- **What to avoid:** TLM (delisting), HMSTR (extended >2 ATR), ARPA above zone (OI extreme), ZKP (extreme funding)

---

## 7. Candidate Deep Dives

### Candidate 1 — TLM/USDT (LONG B-tier swing, 72.4/100)

**HEADLINE RISK — DO NOT ENTER LONG**

- System: B-tier swing, score 72.4, actionable, entry 0.0021-0.0023, current 0.0023, ATR 0.0003. 24h +48%, 7d +159%.
- External catalyst — CRITICAL: Binance Watch Label (delisting monitoring) active since May 22, 2026. Pump profile: +48% 24h / +584% volume / $209M = classic pre-delist pump pattern.
- Internal: "no fresh verified catalyst detected" per all three reports. Catalyst layer did not flag TLM delist.
- Chase risk: YES. 7x in 7 days is extreme.
- **Final verdict: AVOID.** Do not enter long at any level. Monitor only.

---

### Candidate 2 — ARPA/USDT (B-tier swing/intraday/scalp)

**CAUTION / MANUAL REVIEW**

- System: B-tier across all modes. Swing 68.5, scalp 68.0, intraday 67.4. Entry 0.0096-0.0100. Current 0.0101-0.0102.
- OI +183-184%, funding -0.00112 (negative). Cross-check: elevated crowding across bybit/mexc. Squeeze dynamics in play.
- External: ARPA Chain launch expectations (anticipation, no hard date). Not a hard catalyst.
- Previous cycle: 3xTP hit — new signals are at higher levels.
- **Final verdict: CAUTION.** Only at entry zone (0.0096-0.0100). Do NOT enter above. Watch OI for stabilization.

---

### Candidate 3 — HMSTR/USDT (C-tier watchlist)

**AVOID — extended >2 ATR**

- System explicitly rejected: >2 ATR from EMA20. C-tier watchlist. 24h +46%.
- No confirmed catalyst for July 4 spike.
- **Verdict: AVOID.**

---

### Candidate 4 — SYN/USDT (Short candidate analysis)

**MANUAL REVIEW — Binance Watch Label + squeeze risk**

- System rejected: "fights bullish tape; price >2 ATR from EMA20."
- Binance Watch Label (May 22, 2026) explains -17.5% drop. Long/short 0.44 = shorts crowded.
- Short trigger: failed bounce above 0.58-0.60 on 4h (NOT now — too extended, squeeze risk).
- **Verdict: MANUAL REVIEW.** Not actionable. Watch for failed-bounce setup.

---

### Candidate 5 — XRP/USDT (C-tier catalyst watch)

**WATCH — Upbit volume confirmed**

- System: C-tier swing (64.8/100). Entry 1.129-1.133. TP1 1.146, TP2 1.157. Current 1.136.
- Catalyst CONFIRMED: Upbit volume > BTC on July 3, 2026. Korean market driver.
- **Verdict: WATCH.** Pullback to 1.129-1.133 entry zone. Invalidation 1.123.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Entry zone | Trigger | Notes |
|---|---|---|---|---|---|
| 1 (long-watch) | ADA/USDT | swing | 0.1761-0.1787 | Pullback + BTC holding | No delist, multi-exchange confirmed |
| 2 (catalyst-watch) | XRP/USDT | C-tier watch | 1.129-1.133 | Pullback; Upbit volume sustaining | Catalyst confirmed July 3 |
| 3 (secondary) | TIA/USDT | swing | 0.3905-0.3935 | Pullback + BTC holding | Clean, no headline risk |
| AVOID | TLM/USDT | — | — | — | Binance Watch Label active |
| SHORT-WATCH | SYN/USDT | — | — | Failed bounce >0.58-0.60 on 4h | Not actionable now |
| CAUTION | ARPA/USDT | all modes | 0.0096-0.0100 | Only at zone if OI normalizes | OI 184%, chase above zone |

---

## 9. Avoid / No Trade (This Decision Window)

- **TLM** — Binance delisting monitoring active
- **HMSTR** — >2 ATR extended, C-tier only
- **ARPA new longs above 0.0100** — OI 184% squeeze risk
- **ZKP new longs** — extreme funding (-0.00565)
- **All shorts in bullish tape** — wait for specific trigger
- **Scalp mode generally** — PF 0.14 over 14d (low_confidence)
- **Weekend mode signals** — PF=0.9, WR=13.4% historically

---

## 10. Main Risks

1. TLM pump/dump risk: classic pre-delist pump pattern on Binance Watch Label token
2. ARPA post-squeeze unwind: OI 184% spike — forced buying dries up when shorts finish covering
3. Weekend mode underperformance: net-negative PF (0.9) historically
4. No A-tier signal: all B-tier with low_confidence overlays
5. Social attention blind spot: Reddit blocked, no Telegram/X feeds
6. Catalyst layer gap: TLM and SYN delist risks not in internal data
7. Correlation cluster: most active alts (ADA, TIA, SENT, etc.) correlated; BTC breakdown = all-hit

---

## 11. Action Plan — Next 4 Hours (04:39–08:39 EEST)

1. Monitor ADA/USDT at 0.1761-0.1787 — cleanest pullback long candidate
2. Monitor XRP/USDT at 1.129-1.133 — catalyst-backed watch
3. Do not enter TLM at any price — Binance Watch Label active
4. Watch ARPA OI trend — entry only at zone (0.0096-0.0100), not above
5. Check SYN for bounce toward 0.58-0.60 — monitor for failed-bounce short setup
6. Next scheduled cycle: ~05:54 EEST

---

## 12. Final Verdict per Mode

| Mode | Verdict | Best candidate | Notes |
|---|---|---|---|
| Crypto scalp | LOW CONFIDENCE | ADA/USDT (73.4) | PF 0.14 / 14d; low_confidence overlay |
| Crypto intraday | WATCH ONLY | ADA/USDT (70.2) | Wait for zone pullback |
| Crypto swing | CAUTION | ADA/USDT (65.3) | TLM #1 score but AVOID |
| Stocks intraday | N/A — CLOSED | — | US Independence Day weekend |
| Stocks swing | N/A — STALE | — | 36h stale, holiday weekend |
| Stocks invest | N/A — STALE | — | 36h stale, holiday weekend |

**Overall session verdict:** CAUTION. Bullish regime but TLM delist risk, weekend underperformance, no A-tier. Watch ADA/XRP at pullback zones. Advisory only — no auto-trade.

---

## 13. Sources

| # | Source | Finding | URL | Date | Verification |
|---|---|---|---|---|---|
| 1 | BeInCrypto/Yahoo | XRP volume tops Bitcoin on Upbit | https://finance.yahoo.com/markets/crypto/articles/xrp-trading-volume-tops-bitcoin-203235623.html | 2026-07-03 | single_source |
| 2 | CoinPaper | XRP Upbit volume overtakes Bitcoin | https://coinpaper.com/32672/xrp-clears-major-hurdle-eyes-130-as-upbit-volume-overtakes-bitcoin | 2026-07-03 | single_source |
| 3 | CryptoNews | Binance Watch Label: TLM+SYN among 11 altcoins | https://cryptonews.net/news/market/32903896/ | 2026-05-22 | single_source |
| 4 | 8V Crypto Academy | TLM delisting announcement | https://8v.com/info/platform/announcements/announcement-of-delisting-tlm-alien-worlds/ | 2026 | single_source |
| 5 | CoinMarketCap (AI) | TLM: +107% 7d, delist monitoring, +584% volume | https://coinmarketcap.com/cmc-ai/alien-worlds/latest-updates/ | 2026-07-04 | single_source |
| 6 | CoinMarketCap (AI) | ARPA: +68% 24h, ARPA Chain launch expectations | https://coinmarketcap.com/cmc-ai/arpa-chain/latest-updates/ | 2026-07-04 | single_source |
| 7 | CoinMarketCap (AI) | HMSTR: +28.7% 24h, no confirmed catalyst | https://coinmarketcap.com/cmc-ai/hamster-kombat/latest-updates/ | 2026-07-04 | single_source |
| 8 | Internal | Cycle 01 summary, paper monitor, signal stats | local files | 2026-07-04 04:19 EEST | primary_source |

---

## 14. Fix Requests / TODO

### TODO-tlm-delist-not-mapped [HIGH]
TLM Binance Watch Label (May 22, 2026) NOT in catalyst_events.jsonl for TLM. The "delisting_thin_liquidity" basket maps BTC/XRP (unrelated story), not TLM. Operator had no internal warning about TLM's delist risk despite #1 swing score. Suggested fix: add Binance Watch Label monitoring to catalyst ingest pipeline; tag all affected symbols with `exchange_delisting` / `risk_level=high`. First observed: 2026-07-04 04:39 EEST.

### TODO-syn-delist-not-mapped [HIGH]
SYN on same Binance Watch Label (May 22, 2026). The -17.5% overnight drop is explained by this, but internal reports only show "rejected short / fights bullish tape" with no delist flag. Same fix as TLM above. First observed: 2026-07-04 04:39 EEST.

### TODO-weekend-scalp-systematic-review [MEDIUM]
Weekend mode: PF=0.9, WR=13.4% (net negative). Scalp mode: PF=0.14 over 14d (low_confidence). Both continue generating B-tier Telegram-actionable signals on weekends. Consider auto-downgrade to C-tier for weekend+scalp combo until PF recovers. Requires operator sign-off. First observed: 2026-07-04 04:39 EEST.
