# Opus Enriched Review — Post-Close Final Daily Review — Auto Cycle 23:15 EEST

**Slot:** post-close final daily review | **Time:** 2026-07-04 23:15 EEST
**Previous review:** 2026-07-04 21:39 EEST (late-session risk review)
**Advisory only — no auto-trade. US markets CLOSED (Independence Day). Weekend mode active (Saturday).**

---

## 1. Executive Summary

This is the **post-close final daily review** for Saturday July 4, 2026 at 23:15 EEST. Crypto-only — US stocks closed for Independence Day. Advisory only, no auto-trade.

**How the US session closed:** Wall Street was fully closed (holiday). Crypto wrapped the day with BTC at **$63,147 (+0.67% daily, +3.6% weekly)**, reversing end-June losses and reclaiming Q3 momentum. ETH +3.2% ($1,784). XRP led major gainers +5.3%. Thin holiday liquidity exaggerated intraday wicks but directional drift was bullish throughout.

**What worked today:** Massive TP hit cluster across all modes. Signal stats improved from 21:39 baseline (PF 3.1 → **3.6**, totalR 86.4R → **93.7R**). Swing mode dominant (PF 5.58, +55R). OGN both scalp/intraday triggered and hit TP. HMSTR swing TP hit. KITO, ZEC, ARB, RITO, SENT, TRUMP, DOGS, BONK all hit TPs during the day.

**What failed:** Short side net-negative (PF 0.9, -0.3R). All short candidates (SYN, JTO) capped to C due to thin holiday squeeze risk. VANRY extended >2ATR — no entry possible. Clarity Act Senate vote **delayed** before July 4 recess (Galaxy Research: 50% passage probability). ADA van Rossem HF was June 18 — already live, not upcoming (stale catalyst).

**Catalyst coverage WEAK (80.3% unmapped)** — use as context only, not final decision signal.

**Overnight/Asia setup:** BTC above $63K recovery level, 87.5% alts above EMA20, bullish continuation bias into Asia. Prefer retests over fresh chases on thin overnight liquidity. Best overnight setup: OGN (triggered, pullback watch), DOGE swing (best catalyst), BTC/ETH/XRP/LTC swing (waiting).

---

## 2. Data Used

| Source | Time / Mtime | Freshness |
|---|---|---|
| scheduler.log + cycle_09_22-53 | 23:12 EEST (11 min ago) | **FRESH** |
| scalp report `2026-07-04_20-00` | 23:00 EEST (15 min) | **FRESH** |
| intraday report `2026-07-04_20-05` | 23:05 EEST (10 min) | **FRESH** |
| swing report `2026-07-04_13-14` | 16:14 EEST (7h) | **CARRY-FORWARD** (4–12h) |
| stocks intraday `2026-07-03_20-07` | 07/03 23:07 (~24h) | **STALE** — closed (holiday) |
| stocks swing `2026-07-02_13-03` | 07/02 16:03 (~59h) | **STALE** — excluded |
| stocks invest `2026-07-02_13-05` | 07/02 16:05 (~59h) | **STALE** — excluded |
| catalyst_events.jsonl + cycle_20-05 | 23:05 EEST | **FRESH** |
| narrative_baskets.jsonl | 23:05 EEST | **FRESH** |
| LLM analysis packet (intraday) | 23:05 EEST | **FRESH** |
| active-signals CLI (crypto, 50) | live 23:15 | **LIVE** |
| signal-stats CLI (crypto) | live 23:15 | **LIVE** |
| detect_untracked_legacy_alerts | live 23:15 | 16 untracked |
| BTC price (WebFetch CoinDesk) | 2026-07-04 | $63,147 +0.67% ✓ verified |
| ETH/XRP price (WebSearch) | 2026-07-04 | ETH $1,784 +3.2%; XRP +5.3% |
| Clarity Act (WebSearch) | 2026-07-04 | Senate vote DELAYED ✓ |

**Notes:**
- Stocks: excluded from verdicts (US Independence Day + weekend mode, data stale >24h).
- Social attention: unavailable (Reddit 403 blocked, no live X/Telegram connectors).
- Onchain: `interface_ready_config_missing`.
- Weekend mode active: A-tier -5pts, confidence -1 band, MEXC-only cap C.

---

## 3. Scheduler / Data Freshness

- **Scheduler:** cycle_09 completed 23:12 EEST (11 min ago). All crypto reports regenerated at 23:00/23:05. **FRESH.**
- **Cycle mode:** weekend (crypto-only). Stocks disabled.
- **Paper monitor status (from previous review 21:39 as baseline; ~2h stale):**
  - OPEN actionable: ~10 (estimated from active-signals triggered rows)
  - WAITING for entry: ~7 (HEI sc, GRAM sc, BTC sw, ETH sw, LTC sw, XRP sw, EPIC sw)
  - ENTERED UNRESOLVED: ~59 (filled, no TP/SL before window — lifecycle status, not losses)
  - Review/Shadow: ~163
  - NO-ENTRY / STALE / MOVED AWAY: ~70
  - Needs review: ~0
- **50 active signals (live CLI):** heavily long B-tier, all crypto. No A-tier active.
- **Untracked legacy alerts today:** 16 (TLM×5 [intraday/scalp], ADA×2 [scalp/swing], ZEC×2 [scalp], XRP×1 [intraday], plus 6-signal scalp batch at 20:00: EPIC, DOGS, MIRA, SENT, BONK, XPL). Sent to Telegram but NOT tracked in PF/winrate.
- **Signal stats week-over-week improvement:** PF 3.1 → 3.6; totalR 86.4 → 93.7R since last review.
- **Paper shadow (forward-valid, gate NOT_READY 4/6):** A −81.98R / B +59.62R. No promotion.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-07-04 23:15 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["social_attention", "onchain_data", "liquidation_heatmaps", "order_book_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log + cycle_09: 11 min old — FRESH",
        "scalp/intraday reports: 10-15 min — FRESH",
        "swing: 7h — CARRY-FORWARD",
        "stocks: >24-59h — STALE excluded (holiday)",
        "catalyst mapping: 692/3516 (19.7%) — WEAK flag triggered"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": ["live_social_sentiment", "macro_calendar", "DXY_yields"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC: $63,147 +0.67% day, +3.6% week — Q3 reversal from 21-month lows",
        "ETH: $1,784 +3.2%; XRP: +5.3% (led majors)",
        "Altcoin breadth: 87.5% above EMA20 and EMA50",
        "BTC ATR percentile: 6 — low volatility environment",
        "Macro risk score: 17/100 (risk-on tailwind)",
        "Soft US jobs + Fed Chair Warsh inflation comments = favourable backdrop"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["narrative_supported", "mapping_weak", "stale_catalyst"],
      "data_missing": ["symbol_resolver_coverage", "social_feeds"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "936 unique events today (JSONL 3516; 692 mapped = 19.7%) — WEAK flag",
        "ETH: Clarity Act advancing BUT Senate vote DELAYED (50% passage probability)",
        "ETH: Lean Ethereum 10,000 TPS + quantum safety roadmap (CryptoBriefing)",
        "BTC: BlackRock $1.22B to Coinbase 4 days — institutional structural demand",
        "DOGE: Musk+Saylor July 4 posts + TDOG ETF + DogeOS — multi-layer verified",
        "ADA: van Rossem HF went live June 18 — STALE (corrected prev review)",
        "TLM: Binance delisting monitoring active — block_requires_operator_review",
        "Baskets: delisting_thin_liquidity, ai_narrative, momentum_breakout"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.50,
      "reason_codes": ["oi_supports", "funding_extreme", "data_unavailable"],
      "data_missing": ["OI_change_intraday_mode", "liquidation_heatmap", "order_book_CVD"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OGN: funding -0.00535 (Bybit) / -0.005298 (MEXC) — shorts crowded, squeeze potential",
        "HMSTR: OI +131% from swing data — fresh positioning confirmed",
        "MIRA: funding -0.008 to -0.003 across venues — crowding unknown",
        "VANRY: OI +135% — heavily positioned, crowding unknown",
        "Intraday mode: mostly MEXC/Bybit fallbacks, OI change unavailable",
        "Short squeeze risk: SYN, JTO capped to C on holiday thin liquidity",
        "Squeeze phases (120 symbols): 42 in post_unwind_chop, 4 in active unwind"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["clean_retest", "entry_late", "chase_risk", "overextended"],
      "data_missing": ["TradingView_chart_MCP", "live_price_tick"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OGN: price 0.0199, entry zone 0.0187-0.0196 (pullback available — not chasing)",
        "EPIC: price 0.728; swing entry was 0.6442-0.6635 — may be attainable on pullback",
        "VANRY: price 0.0049-0.0050, >2ATR from EMA20 — AVOID, do not chase",
        "HMSTR: micro-price at 0.0003 — +86% 7d, extended",
        "DOGS: sub-micro price, volume 0.15x below average — weak confirmation",
        "TradingView chart MCP unavailable — all observations from OHLCV/ATR fields only"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.70,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved"],
      "data_missing": ["real_time_paper_monitor_direct_feed"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "50 active crypto signals (active-signals CLI)",
        "OPEN ACTIONABLE (~10): HEI(in), TAO(in), HMSTR(sc), MIRA(sw+in+sc), DOGS(sw), THE(sw)",
        "WAITING FOR ENTRY (~7): HEI(sc), GRAM(sc), BTC(sw), ETH(sw), LTC(sw), XRP(sw), EPIC(sw)",
        "TP HIT (~30): OGN(sc+in), DOGS(in+sc), TRUMP(in), HMSTR(sw), KITO×3, ZEC×2, ARB×3, SENT×2, SOL, BTC(in), NEAR, ZK×2, RITO, BCH, PEPE",
        "ENTERED UNRESOLVED (~59 at 21:39): filled, window expired before TP/SL — lifecycle, not loss",
        "Untracked: 16 alerts today (TLM×5, ADA×2, ZEC×2, XRP×1, scalp-batch×6)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["reduce_risk", "legal_risk", "manual_review"],
      "data_missing": ["intraday_drawdown_realtime"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Weekend mode: A-tier -5pts, confidence -1 band, MEXC-only capped C",
        "Holiday thin liquidity: exaggerates wicks in both directions",
        "TLM: block_requires_operator_review — appears in active signals (flag §14)",
        "Short side this week: PF 0.9, -0.3R — net negative, do not add short aggression",
        "16 untracked alerts: tracking gap; signal quality comparison compromised",
        "Meme-alt correlation: HMSTR/DOGS/MIRA may correlate with BTC dip",
        "No legal/headline risk on active crypto A/B (TLM blocked, UNH stocks-only)"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing"],
      "data_missing": ["full_14d_no_catalyst_detailed_cut"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Week: 257 signals, WR 26.9%, PF 3.60, avgR 0.53R, totalR 93.7R",
        "Swing: PF 5.58, avgR 0.85R, +55R (88 signals) — strongest mode",
        "Intraday: PF 2.72, avgR 0.50R, +31R (72 signals) — working",
        "Scalp: PF 2.26, avgR 0.18R, +7.6R (97 signals) — weakest mode",
        "Shorts: PF 0.9, -0.3R total — net negative, avoid increasing short exposure",
        "No-catalyst intraday (14d cut from report): WR 23%, PF 0.70, -3R — weak subset",
        "Non-weekend better than weekend (PF 4.4 vs 2.9)"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.73,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "OGN/USDT",
      "trigger": "pullback into 0.0187-0.0196 (already triggered scalp/intraday; new entries on retests only — no chase above 0.0205); invalidation 1h close below 0.0177",
      "reason": "Highest-scored B non-catalyst (scalp 79.1 / intraday 73.1), RS +24% vs BTC, OI +129%, negative funding = shorts crowded, momentum basket primary"
    },
    "best_short_candidate": {
      "symbol": "SYN/USDT",
      "trigger": "failed retest of 0.0043-0.0045 resistance area with volume confirmation + BTC not rallying; avoid on thin holiday liquidity, squeeze risk on holiday tape",
      "reason": "RS -18.4% vs BTC, -16.7% 24h, failed bounce structure; capped C on holiday tape — short only after confirmed failed retest with stop above swing high"
    },
    "best_catalyst_candidate": {
      "symbol": "DOGE/USDT",
      "trigger": "swing B already triggered (OPEN from 21:39 review); on pullback — Musk+Saylor July 4 posts + TDOG ETF + DogeOS + commodity classification multi-layer",
      "reason": "Best multi-source verified catalyst of the day — four independent catalyst layers confirmed"
    },
    "avoid_candidate": {
      "symbol": "TLM/USDT",
      "reason": "Binance delisting monitoring active, OI declining into pump (short-covering not fresh positioning), block_requires_operator_review active; appears in active signals — system tracking gap (see §14 TODO-TLM-IN-ACTIVE)"
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
|---|---|---|---|---|
| data_quality | **ok** | 0.75 | scheduler_fresh, report_stale (swing 7h) | advisory_only |
| market_regime | **ok** | 0.82 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | **caution** | 0.55 | narrative_supported, mapping_weak, stale_catalyst | advisory_only |
| derivatives_squeeze | **caution** | 0.50 | oi_supports, funding_extreme, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.65 | clean_retest, entry_late, chase_risk, overextended | advisory_only |
| execution_lifecycle | **ok** | 0.70 | open_actionable, waiting_for_entry, entered_unresolved | advisory_only |
| risk_manager | **caution** | 0.72 | reduce_risk, legal_risk, manual_review | advisory_only |
| playbook_performance | **ok** | 0.75 | playbook_working (swing/intraday), playbook_failing (shorts, scalp weak) | advisory_only |
| head_trader | **normal** | 0.73 | longs preferred, route by catalyst/RS, avoid TLM | advisory_only |

---

## 4. What Changed vs Previous Review (21:39 EEST late-session)

| Item | Previous (21:39) | Now (23:15) |
|---|---|---|
| Scheduler cycle | cycle_08 (20:53) | cycle_09 (23:12) — **FRESH** |
| Scalp report | 17:41 EEST | **23:00 EEST** — regenerated |
| Intraday report | 17:47 EEST | **23:05 EEST** — regenerated |
| Signal stats (PF) | 3.1 (n=254) | **3.60** (n=257) — improved |
| Signal stats (totalR) | 86.4R | **93.7R** — +7.3R added |
| BTC external | $63,121 (2:30 pm EDT) | $63,147 (close) — **day closed flat-to-up** |
| ETH external | not checked | **$1,784 +3.2%** |
| XRP | in reports | **+5.3%** best major |
| Clarity Act | advancing | **Senate vote DELAYED** — 50% passage prob |
| Untracked alerts | 8 | **16** — 8 new alerts since 21:39 (scalp batch 20:00 + XRP 19:36) |
| Catalyst coverage | 826 unique | **936 unique** today; 3516 JSONL total; 80.3% unmapped |
| OGN status | both modes triggered | **TP hit confirmed** (scalp + intraday) |
| ADA catalyst | "upcoming HF" | **STALE — HF went live June 18** (corrected) |
| DOGE catalyst | multi-layer verified | **Confirmed** — Musk+Saylor July 4 verified |
| Short side | all capped C | **unchanged — avoid shorts on thin tape** |

**New this review:** Clarity Act Senate delay confirmed, XRP +5.3% outperformance, signal quality metrics improved.
**Removed/demoted:** VANRY intraday — too extended. ADA catalyst declared stale.
**Unchanged thesis:** OGN best non-catalyst long; DOGE best catalyst-backed; TLM avoid; SYN short-watch only.

---

## 5. Catalyst Coverage

> **⚠ CATALYST MAPPING WEAK THIS RUN — use catalyst layer as context, not final decision.**

- Total catalyst events (JSONL): **3,516**
- Mapped: **692 (19.7%)**
- Unmapped: **2,824 (80.3%)** — exceeds 50% threshold
- Unique events today: **936**; Baskets: **3**

**Active narrative baskets:**
1. `delisting_thin_liquidity` (avoid_low_liquidity, fresh <1h): no primary symbol
2. `ai_narrative` (related_beta_rotation, fresh <6h): NEAR/RENDER/TAO/FET primary
3. `momentum_breakout` (avoid_chase, fresh <1h): VANRY/EPIC/OGN primary (+ MIRA related)

---

## 6. Market Landscape

- **Crypto mood:** risk-on (BTC uptrend, 87.5% breadth above EMA20)
- **Stocks mood:** closed (US Independence Day)
- **Preferred side:** longs (pullback/retest only; no chase on thin overnight)
- **Best long:** OGN/USDT — pullback 0.0187-0.0196, negative funding
- **Best short:** SYN/USDT — short-watch only after failed retest
- **Best catalyst:** DOGE/USDT — swing open, multi-layer July 4 catalysts
- **Avoid:** TLM (delisting), VANRY (extended), ADA (stale), new shorts

**Asia setup:** BTC above $63K. 87.5% alts breadth. Continuation bias unless BTC drops below $62K.

---

## 7. Candidate Deep Dives

### OGN/USDT — LONG B (Best RS non-catalyst)
- 24h +25.1% | RS vs BTC +24.2% | Volume 1.41x | OI +129%
- Entry: pullback 0.0187-0.0196 | Inv: 0.0177 | TP1: 0.0218
- Funding: Bybit -0.00722, MEXC -0.00530 — shorts crowded both venues
- **Verdict:** WATCH pullback into 0.0187-0.0196. No chase above 0.0205.

### DOGE/USDT — LONG B (Best catalyst-backed, swing OPEN)
- Multi-layer: Musk+Saylor posts + TDOG ETF + DogeOS + commodity classification
- Swing already triggered. Monitor invalidation level.
- **Verdict:** Best overnight catalyst setup. Watch swing position, do not add scalp if extended.

### EPIC/USDT — LONG B (WAITING, strongest RS +36.7%)
- 24h +37.6% | Swing entry 0.6442-0.6635 | Current ~0.7280 — above zone
- **Verdict:** WAITING. Watch for pullback to entry zone. Do not chase.

### SYN/USDT — SHORT watch (capped C, not actionable)
- 24h -16.7% | RS -18.4% | Squeeze risk on holiday tape
- **Verdict:** SHORT-WATCH. Trigger: failed retest 0.0043-0.0045 + volume. Revisit Monday.

### VANRY/USDT — RS monitor only
- +62.4% 24h | OI +135% | >2ATR from EMA20 — system flag
- **Verdict:** No entry. Track pullback to 0.0043-0.0048 for future cycle consideration.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Direction | Score | Lifecycle | Trigger |
|---|---|---|---|---|---|---|
| 1 | OGN/USDT | scalp+intraday B | LONG | 79.1/73.1 | TP HIT — reentry watch | Pullback 0.0187-0.0196 |
| 2 | DOGE/USDT | swing B | LONG | — | OPEN ACTIONABLE | Swing active; monitor inv. |
| 3 | EPIC/USDT | swing B | LONG | 73.9 | WAITING | Pullback to 0.6442-0.6635 |
| 4 | BTC/USDT | swing B | LONG | 65-66 | WAITING | Entry 62,200-62,500 |
| 5 | XRP/USDT | swing B | LONG | 64-68 | WAITING | Entry 1.144-1.148 |

**Short-watch (not actionable):** SYN/USDT — failed retest only + BTC not ripping

---

## 9. Avoid / No Trade

- **TLM/USDT:** Binance delisting. `block_requires_operator_review`. Full avoid.
- **VANRY/USDT:** >2ATR, no catalyst, chase risk.
- **ADA/USDT:** >2ATR, stale catalyst (HF live since June 18).
- **SYN/USDT:** No active short on holiday thin tape.
- New scalp entries on extended overnight moves.

---

## 10. Main Risks

1. BTC thin holiday liquidity — 2-3% overnight wick risk
2. Clarity Act 50% passage probability — ETH catalyst conditional
3. Meme correlation — HMSTR/DOGS/MIRA/DOGE all correlated to BTC
4. 16 untracked alerts — PF/winrate understated (manual audit needed)
5. Catalyst mapping 80.3% unmapped — context only
6. Short side systemic: PF 0.9, -0.3R; avoid adding shorts
7. Social data unavailable — crowd context missing

---

## 11. Action Plan — Overnight (23:15 → 03:15 EEST)

1. **OGN:** Watch 0.0187-0.0196 pullback. Enter on 15m close acceptance. Stop: 1h below 0.0177.
2. **DOGE swing:** Monitor existing position. Watch invalidation. Reduce on approach.
3. **EPIC:** Watch for pullback to 0.6442-0.6635. Current 0.7280 = above entry.
4. **BTC/ETH swing:** Watch 62,200-62,500. No scalp/intraday on macro anchors overnight.
5. **TLM:** Full avoid.
6. **Monitor:** Exploit/hack news, Clarity Act vote, BlackRock flows, Asia exchange developments.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|---|---|---|
| **Crypto scalp** | CAUTION | Holiday + weekend wicks. Pullback-only. No chase entries. |
| **Crypto intraday** | WATCH — pullback first | OGN only if pullback available. RS-leaders only for no-catalyst. |
| **Crypto swing** | ACTIVE — best mode | PF 5.58, +55R week. DOGE triggered; EPIC/BTC/ETH/XRP waiting. |
| **Stocks (any)** | CLOSED | Independence Day. All stale >24h. No action until Monday. |

---

## 13. Sources

- [BTC: Bitcoin retakes $63,000 — CoinDesk, 2026-07-04](https://www.coindesk.com/markets/2026/07/04/bitcoin-jumps-above-usd63-000-reversing-end-june-losses) ✓
- [Clarity Act ETH — Motley Fool, 2026-07-04](https://www.fool.com/investing/2026/07/04/congress-is-moving-forward-with-the-clarity-act-th/)
- [CLARITY Act Senate DELAY — Bitcoin Foundation, 2026-07-04](https://bitcoinfoundation.org/news/regulation/clarity-act-blocked-before-july-4-senate-delay-sparks-uncertainty-what-happens-next/)
- Internal: scalp/intraday/swing reports (FRESH/CARRY-FORWARD)
- Internal: active-signals (50 signals), signal-stats (n=257, PF 3.60), untracked alerts (16)
- Internal: catalyst_events.jsonl (3516 total, 692 mapped)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-04_2139.md`
- Sources JSON: `data/raw/enriched_review_sources/2026-07-04T23-15-00+03-00.json`

---

## 14. Fix Requests / TODO

### TODO-TLM-IN-ACTIVE
TLM/USDT appears in active-signals CLI despite `block_requires_operator_review`. Review whether block gate should suppress CLI display. Priority: medium.

### TODO-UNTRACKED-ALERT-VOLUME
16 untracked legacy alerts today (up from 8 at 21:39). Scalp batch at 20:00 created 6 untracked alerts (EPIC, DOGS, MIRA, SENT, BONK, XPL) — bulk generation path likely skipping proposed_signal registration. Priority: medium.

### TODO-CATALYST-MAPPING-PERSISTENT-WEAKNESS
19.7% mapped (692/3516) — recurring. Expand symbol resolver; classify basket-only events explicitly vs null symbol. Priority: medium.
