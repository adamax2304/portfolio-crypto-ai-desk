# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:39 EEST

**Slot:** Europe / pre-US context | **Time:** 2026-07-06 11:39 EEST | **Day:** Monday — first full US trading day post July 4th holiday
**Previous review:** 2026-07-06 04:39 EEST (crypto overnight / Asia review)
**Advisory only — no auto-trade. Scanning always continues.**

*(Latest copy at: OPUS_ENRICHED_REVIEW_LATEST.md)*

---

## 1. Executive Summary

**Slot:** Europe / pre-US context (11:30 EEST). US cash session opens at 16:30 EEST (10:30 ET = pre-market only until then). Stocks are planning/watchlist ONLY. Crypto is fully live and actionable.

**Crypto regime:** BTC and ETH both confirmed uptrend. BTC holding ~$62,500–63,000 (external verification: ~$62,538–63,061, +$788/24h, +3.71%/7d). Altcoin breadth 73.7% above EMA20 — solid but down from 82.5% at the overnight swing cycle, indicating mild rotation / breadth compression since 05:00 EEST. ATR percentile 10% (compression phase — low intraday volatility). F&G=24 (Extreme Fear) diverges positively from price action (wall of worry = continuation supportive). Dollar near two-week lows → macro risk-on for BTC/ETH. ETH/BTC=0.028127 (ETH still underperforming BTC on a relative basis).

**Key wins this cycle:** TRB/USDT B-tier intraday TP1 hit during cycle 3 (09:30–09:57 EEST). ETH B-tier scalp TP1 hit. Both signals entered and resolved at first target — system working.

**No A-tier crypto.** Top B-tier (all no-catalyst — see caution note): LAB/USDT (intraday B, MEXC-only), TLM/USDT (multiple modes, AVOID new entry), ANSEM/USDT (intraday B, MEXC-only), TRB/USDT (TP1 HIT — do not enter new), XPL/USDT (intraday B triggered — cleanest entry). BTC swing B triggered (macro-supported). ETH swing B triggered.

**Stocks:** All 20 active signals are C-tier (not actionable). Market closed. **UNH: active DOJ fraud probe (criminal + civil, Medicare fraud) — shares -16% — LEGAL RISK → AVOID any long.** MSFT securities fraud lawsuit advisory. Stocks A/B paper performance -3.3R/PF0.33 (7d) — global paper guard blocking both directions.

**Key event risk:** FOMC minutes July 8 (tomorrow, Tuesday). Options market call-heavy into that event → potential breakout above $63K or event-driven reversal if hawkish surprise. Position sizing caution advised for swing entries today.

**Preferred side:** Longs (crypto) via RS-leader pullbacks. Crypto swing remains the strongest mode (PF5.80, 72% WR per system notes). No clean short candidates — all bullish tape, all shorts capped by squeeze risk system flags. **Advisory only. No auto-trade.**

---

## 2. Data Used

| Source | Mtime / Freshness | Status |
|---|---|---|
| scheduler.log | 2026-07-06 09:57 EEST | **FRESH** (1h42m) |
| cycle_03_09-30_summary.md | 2026-07-06 09:57 EEST | **FRESH** (1h42m) |
| scalp report `2026-07-06_06-38` | 2026-07-06 09:38 EEST | **FRESH** (<2h) |
| intraday report `2026-07-06_06-45` | 2026-07-06 09:45 EEST | **FRESH** (<2h) |
| stocks intraday `2026-07-06_06-54` | 2026-07-06 09:54 EEST | **FRESH** (<2h) |
| swing report `2026-07-06_02-01` | 2026-07-06 05:01 EEST | **CARRY-FORWARD** (6h38m; 4–12h window) |
| stocks swing / invest | Not generated today (cycle 3: long-horizon=False) | **N/A** |
| catalyst_events.jsonl | 2026-07-06 (same cycle) | **FRESH** (491 events, 3 baskets) |
| intelligence layer | 2026-07-06 06:51 UTC | **FRESH** |
| paper monitor status | cycle 3 (09:55 EEST) | **FRESH** |
| active-signals CLI × 2 | cycle 3 embedded | **LIVE** |
| signal-stats CLI × 2 | cycle 3 embedded | **LIVE** |
| detect_untracked_legacy | cycle 3 embedded | **CLEAN (0)** |
| crypto monitors | 11:25 EEST (background) | **ACTIVE** (90 min window) |
| External: BTC price | WebSearch 11:39 | ~$62,538–63,061, uptrend ✓ |
| External: TLM status | WebSearch 11:39 | Price ambiguous across sources; leveraged-pump narrative confirmed from 04:39 |
| External: UNH DOJ | WebSearch 11:39 | Criminal + civil probe confirmed ongoing; Medicare fraud; shares -16% |

**External web research:** Available. See §13 for sources.

---

## 3. Scheduler / Data Freshness

- **scheduler.log** mtime 09:57 EEST — **NO DEFER** (1h42m, well within 3h threshold).
- **Cycle 3** (09:30–09:57 EEST): ok=32, failed=0. Weekday mode, stocks enabled, long-horizon swing/invest not run today.
- Cycle 3 tracking (pre): checked=547, updated=0, tp_hits=367, stopped=0, expired=0. Revalidation: 27 signals, stale=25, moved_away=0.
- Cycle 3 tracking (post): checked=553, updated=1, tp_hits=367, stopped=1, expired=0.
- Intelligence layer: 127 derivative symbols; 156 symbols in timeline; 2135 events; last event 06:47 UTC.
- Squeeze phase distribution: phase_0_unknown=40, phase_1_build_up=34, phase_2_expansion=4, phase_4_unwind=3, **phase_5_post_unwind_chop=46** (largest block — significant chop risk under the bullish surface).
- Onchain: `interface_ready_config_missing` (no config/onchain.yaml) — no onchain data.
- Reddit social: blocked 403 (all 3 sources) — social layer dark.
- Reuters Business: failed (RSS).
- Catalyst integrity scan: 10 high-importance symbols not mapped to catalyst_events: AMZN, ARB, AXP, BAC, BNB, HYPE, MKR, MS, SMH, SPY.
- Monitors: crypto_monitor_1783320902 and stocks_monitor_1783320902 both active as of 11:25 EEST.

**Paper monitor (cycle 3, as of 09:55 EEST):**

| Status | Count |
|---|---|
| OPEN ACTIONABLE | 9 |
| WAITING FOR ENTRY | 4 |
| ENTERED UNRESOLVED (filled, no TP/SL before window) | 31 |
| REVIEW / SHADOW | 149 |
| NO-ENTRY / STALE / MOVED AWAY | 82 |
| CLOSED (win/loss/flat) | 372W / 55L / 0flat |
| NEEDS REVIEW | 0 |

- **Entered-unresolved (31):** entries were filled; no TP or stop triggered before window expiry — NOT missed entries.
- **No-entry/moved-away (82):** price never reached trigger or moved away before entry — N/A lifecycle.
- **Paper portfolio (bybit_non_vip_usdt_perp active):** $7,009.66 net (+40.19%) vs $5,000 start. Conservative-taker: $6,707.63 (+34.15%). Zero-fees upper bound: $10,308 (+106%).
- **Paper shadow A/B (FORWARD only — no backfill look-ahead):** window=11d. A: -88.24R (-$2,206). B: -26.76R (-$669). Delta: B better by +61.48R/$1,537. Promotion gate: **NOT_READY** (4/6: forward duration <14d; DATA_GAP_LATE at 40% of forward). Both A and B are negative in the forward window; B loses less. Do not promote.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-06 11:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.87,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "reddit_social_blocked", "reuters_business_failed", "sec_edgar_dead"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log 09:57 EEST (1h42m)",
        "cycle_03 ok=32 failed=0",
        "scalp/intraday/stocks-intraday all <2h",
        "swing report carry-forward 6h38m",
        "untracked alerts=0",
        "intelligence layer 06:51 UTC",
        "8 dead/disabled sources (SEC EDGAR, Business Wire, Binance Announcements, t.me/coin_listing)"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": ["live_social_attention", "etf_flows", "onchain_whale_flows", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC uptrend, ETH uptrend",
        "73.7% alts above EMA20 (down from 82.5% overnight — mild breadth compression)",
        "BTC ATR pct 10% (compression)",
        "F&G=24 (extreme fear / wall of worry)",
        "Dollar near 2-week lows — macro risk-on",
        "Stocks VIX 16.15, risk_on, 3/4 indices uptrend",
        "ETH/BTC=0.028127 (ETH underperforming relative)",
        "BTC steady above $63K (CoinDesk)"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.62,
      "reason_codes": ["no_catalyst", "narrative_supported", "stale_catalyst"],
      "data_missing": ["fresh_catalyst_for_top_B_crypto", "kol_social_feeds"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "491 catalyst events today; baskets: delisting_thin_liquidity / rwa_narrative / ai_narrative",
        "Zero fresh verified catalyst for TLM, TRB, XPL, LAB, ANSEM (all no-news B-tier)",
        "BTC/ETH: macro narrative confirmed (dollar weakness + FOMC minutes July 8)",
        "UNH: confirmed DOJ probe (legal risk, criminal + civil, Medicare fraud)",
        "No-catalyst intraday crypto: WR23% / PF0.70 / -3R per 14d system warning",
        "10 high-importance symbols unmapped in catalyst_events (integrity scan)",
        "FOMC minutes July 8 = near-term catalyst for BTC/ETH"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["post_unwind_chop", "squeeze_risk", "data_unavailable"],
      "data_missing": ["oi_history_sparse", "liquidation_heatmaps", "order_book_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "46 symbols in phase_5_post_unwind_chop (intelligence layer)",
        "VANRY: funding -0.002 cross-venues (Bybit+MEXC) — crowding elevated",
        "LAB: funding -0.001 to -0.005 cross-venues (Bybit+OKX+MEXC) — crowding elevated",
        "EPIC: OI +53.25%/24h, funding -0.000525, fresh shorts pressing — SQUEEZE RISK",
        "All short setups capped C via thin_liquidity_short_squeeze_risk flags",
        "TRB: funding 4.5e-05 neutral, OI +27.4% (fresh long positioning, healthy)",
        "XPL: funding neutral, OI -0.35% (short covering, weaker continuation)",
        "TLM: funding -7.3e-05 (MEXC fallback, OI n/a)"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["chase_risk", "clean_retest", "entry_late"],
      "data_missing": ["tradingview_chart_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "TRB: TP1 17.760 ALREADY HIT — entering now is chasing past TP1. LATE.",
        "XPL: price 0.1094 vs entry 0.1078-0.1089 — minor extension, volume 1.91x; pullback needed",
        "TLM: price 0.0033 vs entry zone 0.0031-0.0032 — 7d +266% parabolic, AVOID new entry",
        "BTC: ~$62,500-63,000 approaching $63K resistance (options call-heavy into FOMC July 8)",
        "All B-tier RR to TP1 ~1.84R; scalp known failure: mean reverts before TP1",
        "ATR percentile 10% = low intraday range (compressed entry conditions)"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["open_actionable", "entered_unresolved", "waiting_for_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE: 9 (all crypto)",
        "WAITING FOR ENTRY: 4",
        "ENTERED UNRESOLVED: 31 (not missed — filled, no TP/SL before window)",
        "REVIEW/SHADOW: 149",
        "NO-ENTRY/STALE/MOVED-AWAY: 82 (+50 vs 04:39 cycle)",
        "CLOSED WIN: 372 / LOSS: 55 / FLAT: 0",
        "NEEDS REVIEW: 0",
        "Stocks: all 20 active signals C-tier (market closed — not actionable)",
        "TRB intraday B: TP1 HIT (ENTERED-RESOLVING, not new entry)",
        "ETH scalp B: TP1 HIT (ENTERED-RESOLVING)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "UNH: active DOJ criminal+civil probe (Medicare fraud) + shares -16% → LEGAL RISK → AVOID",
        "MSFT: securities fraud lawsuit (advisory only, operator-review flag active)",
        "ETH: UXLINK hacker 14,336 ETH transfer advisory (operator-review, display-only)",
        "SOL: Step Finance exploiter $21M SOL→ETH via Tornado (operator-review, display-only)",
        "APT: critical vulnerability (operator-review, display-only)",
        "TLM: leveraged contracts + tournament pump (no organic catalyst) — AVOID per prior review",
        "FOMC minutes July 8 — event risk (hawkish surprise → reversal)",
        "Russia/Ukraine attack ahead of NATO summit — geopolitical risk-off signal (minor)",
        "Stocks A/B paper 7d: -3.3R/PF0.33 → global paper guard blocks both directions",
        "46 post_unwind_chop symbols — potential surprise reversals under bullish surface",
        "Peter Brandt considering selling BTC for gold (negative sentiment signal, minor)"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto swing: best mode (72% WR, PF5.80 per prior review; 14d WR 72% / PF5.80 / +24R)",
        "Crypto intraday: week PF3.0 / +41.7R (n=129 — strong bucket)",
        "Crypto scalp: PF0.9 / -0.7R (n=135 — barely flat; low confidence overlay active)",
        "No-catalyst crypto intraday: WR23%/PF0.70/-3R per 14d (system playbook warning)",
        "Stocks A/B intraday: WR3.1%/PF0.333/-3.33R week — FAILING",
        "Stocks no-news long 30d: -5.7R/n93/WR23% — worst bucket",
        "Stocks news-supported 30d: +0.8R/n20/WR20% — only positive stocks bucket",
        "Stocks B-tier PF0.42 (below 0.8 threshold — system observation flagged)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "normal",
      "confidence": 0.68,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto: bullish regime, RS-leader pullbacks preferred, swing mode strongest",
        "No A-tier — all B no-catalyst (historically net-negative without catalyst; prefer RS-leader confirmation)",
        "BTC/ETH macro catalyst confirmed (dollar weakness + FOMC July 8)",
        "Stocks: closed, global paper guard blocking, AVOID new A/B stocks today",
        "TRB/ETH TP1 hits = system producing wins in current regime",
        "FOMC July 8 = size caution on new swing entries today"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.68,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "BTC/USDT",
      "trigger": "pullback to $62,000-62,400 entry zone OR 1h close above $63,200 with volume expansion",
      "reason": "Cleanest macro catalyst (dollar weakness + FOMC July 8 call-heavy options); B-tier swing triggered; most liquid; holds uptrend structure; no squeeze concerns"
    },
    "best_short_candidate": {
      "symbol": "EPIC/USDT",
      "trigger": "failed bounce + bearish 1h candle + derivatives confirmation; NOT actionable without derivatives read",
      "reason": "RS -40% vs BTC, OI +53%, fresh shorts pressing; system capped C — manual review required"
    },
    "best_catalyst_candidate": {
      "symbol": "ETH/USDT",
      "trigger": "hold above $2,350 support on pullback + US-session direction confirmation OR breakout above $2,450 with volume",
      "reason": "Dollar weakness + FOMC July 8 event + scalp TP1 hit this cycle (momentum confirmed)"
    },
    "avoid_candidate": {
      "symbol": "TLM/USDT",
      "reason": "Leveraged contracts + tournament pump; 7d +266% parabolic; Binance delisting monitoring active; prior review AVOID judgment stands"
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
|---|---|---|---|---|
| data_quality | **ok** | 0.87 | scheduler_fresh, report_stale | advisory_only |
| market_regime | **ok** | 0.82 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | **caution** | 0.62 | no_catalyst, narrative_supported, stale_catalyst | advisory_only |
| derivatives_squeeze | **caution** | 0.55 | post_unwind_chop, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.65 | chase_risk, clean_retest, entry_late | advisory_only |
| execution_lifecycle | **ok** | 0.80 | open_actionable, entered_unresolved, waiting_for_entry | advisory_only |
| risk_manager | **caution** | 0.72 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | **ok** | 0.75 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | **normal** | 0.68 | risk_on, longs_preferred, wait_for_trigger | advisory_only |

---

## 4. What Changed vs Previous Review (04:39 EEST today)

| Item | 04:39 Review | 11:39 Review | Change |
|---|---|---|---|
| TRB/USDT | B intraday WAITING for entry | TP1 HIT — ENTERED RESOLVING | **Win this cycle** |
| ETH/USDT scalp | B scalp WAITING | TP1 HIT — ENTERED RESOLVING | **Win this cycle** |
| XPL/USDT | Not a named top candidate | B intraday TRIGGERED (new) | **New triggered candidate** |
| PUMP/USDT | B swing 75.6 (cleanest) | C intraday only 62.8 | **Downgraded** — swing 05:01 cycle showed no B-tier |
| VANRY/USDT | RS leader in swing report | C-tier all modes, risk penalty -14.9, elevated funding | **Risk flag added** |
| BTC/USDT | B swing triggered | B swing still triggered (confirmed) | Unchanged — macro narrative strengthened |
| ETH/USDT swing | Triggered | Still triggered | Unchanged |
| Stocks intraday | Not yet generated | Fresh run — all C (market closed) | First stocks run today |
| UNH | Not in prior review | LEGAL RISK confirmed (DOJ probe + shares -16%) | **New legal risk candidate** |
| OPEN ACTIONABLE | 6 | 9 | +3 new entries |
| ENTERED UNRESOLVED | 22 | 31 | +9 new entries filled |
| NO-ENTRY/STALE | 32 | 82 | +50 expired no-entry |
| FOMC July 8 | Mentioned | Confirmed imminent (tomorrow) | Event risk approaching |
| TLM AVOID | AVOID (leveraged pump) | AVOID still (confirmed) | No change |

---

## 5. Catalyst Coverage

- **Total events today:** 491 (cycle 3 scan, up from 441 at the overnight 01:12 cycle)
- **Active narrative baskets:** 3
  - `delisting_thin_liquidity` — playbook: avoid_low_liquidity (fresh <6h)
  - `rwa_narrative` — playbook: related_beta_rotation (fresh <24h) — primary: ONDO/USDT, XLM/USDT
  - `ai_narrative` — playbook: related_beta_rotation — primary: NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT

**Catalyst mapping: NOT WEAK this run.** 10 unmapped high-importance symbols: AMZN, ARB, AXP, BAC, BNB, HYPE, MKR, MS, SMH, SPY. Unmapped fraction <5% of 491 events — non-critical for this slot's crypto decisions.

**Notable catalyst events:**
- **UNH**: DOJ Probe confirmed — shares dive 16% (criminal + civil Medicare fraud investigation)
- **APT**: Critical vulnerability exploit advisory
- **ETH**: UXLINK hacker 14,336 ETH transfer (display-only operator review)
- **SOL**: Step Finance exploiter $21M SOL→ETH via Tornado Cash (display-only)
- **MSFT**: Securities fraud lawsuit advisory

---

## 6. Market Landscape

- **Crypto mood:** risk-on — BTC+ETH uptrend, breadth 73.7% EMA20, dollar weakness, BTC ~$62,500–63,000. ATR compressed = quiet but directional.
- **Stocks mood:** pre-market / closed — US cash session opens 16:30 EEST. VIX 16.15. Healthcare+financials+industrials strong; energy+tech+semis weak. All intraday signals demoted C.
- **Dominant narrative:** Dollar weakness → macro risk-on → BTC/ETH lift. FOMC minutes July 8 (tomorrow) = call-heavy options → breakout above $63K or hawkish reversal.
- **Preferred side:** Longs (crypto, RS-leader pullbacks) — swing mode (PF5.80) and intraday (PF3.0).
- **Best long:** BTC/USDT — macro catalyst, B-tier swing triggered, $63K approaching
- **Best short:** EPIC/USDT — RS -40%, OI+53% — MANUAL REVIEW REQUIRED; system capped C
- **Best catalyst:** ETH/USDT — dollar weakness + FOMC July 8 narrative
- **Avoid:** TLM/USDT new entry, UNH, stocks A/B, chasing TRB past TP1
- **What changes view:** BTC 1h close below $61,500 → reduce longs; FOMC hawkish surprise → risk-off; BTC break above $63,500 with volume → upgrade conviction

---

## 7. Candidate Deep Dives

### Candidate 1 — BTC/USDT — LONG — B-tier Swing (TRIGGERED / WAITING)

**Status:** B-tier swing TRIGGERED. WAITING FOR ENTRY pullback.

**Thesis:** Dollar near 2-week lows = macro tailwind. BTC confirmed uptrend, approaching $63K resistance with options market call-heavy into FOMC minutes July 8. B-tier swing signal triggered; clean macro-catalyst backing separates this from the no-catalyst B-tier crypto field.

- Active-signals: B swing triggered, entry ~$63K zone, invalidation ~$62K zone
- BTC trend: uptrend (daily + hourly confirmed); ATR percentile 10% (compression)
- External: BTC ~$62,538–63,061 (+$788/24h, +3.71%/7d)
- F&G=24 (Extreme Fear = wall of worry, continuation supportive)
- **Actionable level:** Pullback to $62,000–62,400 (swing). OR 1h close above $63,200 with volume (breakout).
- **Invalidation:** ~$62,000 (1h close below). Chase risk: LOW on pullback, HIGH market-buying $63K.

**VERDICT:** WAITING FOR ENTRY (swing). Best macro-supported long-watch.

---

### Candidate 2 — XPL/USDT — LONG — B-tier Intraday (TRIGGERED)

**Status:** B-tier intraday TRIGGERED. OPEN ACTIONABLE.

- Score: 66.0/100 intraday; 68.0/100 scalp
- Entry zone: 0.1078–0.1089; Current price: 0.1094 (09:38) — minor extension
- TP1: 0.1117; TP2: 0.1141; TP3: 0.1164; Invalidation: 1h close below 0.1065
- ATR: 0.0024; RR to TP1: 1.84R; Volume: 1.91x average (differentiator)
- OI: -0.35% (short covering — weaker continuation); Funding: neutral
- Playbook: no-catalyst (system warning: WR23%/PF0.70/-3R per 14d no-news cut)
- **Actionable level:** Pullback to 0.1078–0.1089. Do not market-buy above 0.1095.
- **Invalidation:** 1h close below 0.1065.

**VERDICT:** WAITING FOR ENTRY on pullback (0.1078–0.1089). Cleanest entry structure in current B-tier crypto intraday field.

---

### Candidate 3 — TRB/USDT — LIFECYCLE NOTE (TP1 HIT — DO NOT ENTER)

**Status:** B-tier intraday — TP1 HIT. ENTERED RESOLVING.

TP1 17.760 hit within cycle 3. Entry zone was 16.726–17.096.

- Current holders: monitor TP2 (18.903) vs BE stop.
- **Do NOT enter a new TRB position** — entering now is chasing past TP1.

**VERDICT:** ENTERED RESOLVING. No new entry.

---

### Candidate 4 — ETH/USDT — LONG — B-tier Scalp (TP1 HIT) + B-tier Swing (TRIGGERED)

**Status:** Scalp B-tier TP1 HIT (ENTERED RESOLVING). Swing B-tier TRIGGERED (WAITING FOR ENTRY).

- Scalp TP1 confirmed in active-signals
- Swing B-tier triggered; pullback entry needed
- ETH/BTC = 0.028127 (underperforming relative, but macro helps)
- UXLINK operator-review advisory: DISPLAY-ONLY
- **Actionable level (swing):** Pullback to demand zone post-US-open confirmation; size conservatively for FOMC.

**VERDICT:** Scalp ENTERED RESOLVING. Swing WAITING FOR ENTRY on pullback.

---

### Candidate 5 — UNH (Stocks) — LEGAL RISK AVOID

**Status:** A→C. LEGAL RISK → AVOID / MANUAL REVIEW REQUIRED.

- DOJ criminal + civil investigation confirmed (Medicare Advantage billing fraud).
- Shares -16%. System flag: `legal_headline_risk: sec_doj`.
- **As long:** AVOID while probe open.
- **As short:** Not actionable today (market closed + paper guard blocking).

**VERDICT:** AVOID ANY LONG. Short: not actionable today.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Mode | Direction | Tier | Status | Entry trigger | Key risk |
|---|---|---|---|---|---|---|---|
| 1 | BTC/USDT | Swing | Long | B | WAITING — macro-supported | Pullback $62,000–62,400 | FOMC July 8 event risk |
| 2 | ETH/USDT | Swing | Long | B | WAITING — catalyst-backed | Pullback post-US-open | FOMC; UXLINK advisory (display only) |
| 3 | XPL/USDT | Intraday | Long | B | TRIGGERED — volume confirmed | Pullback 0.1078–0.1089 | No catalyst (net-negative warning) |
| 4 | TRB/USDT | Intraday | Long | B | TP1 HIT (ENTERED RESOLVING) | No new entry — monitor TP2 18.903 | Chase risk if entering |
| 5 | TLM/USDT | All modes | Long | B | TRIGGERED — **AVOID new entry** | N/A — leveraged pump | No organic catalyst + parabolic |

**Best long-watch:** BTC/USDT — pullback to $62,000–62,400.
**Best short-watch:** EPIC/USDT — manual review required (system capped C).
**Best catalyst-watch:** ETH/USDT — FOMC July 8 breakout trigger above $2,450 with volume.

---

## 9. Avoid / No Trade (This Decision Window)

- **TLM/USDT:** AVOID new entry. Leveraged pump + tournament. No organic catalyst. Parabolic 7d+266%. Binance delisting monitoring active.
- **ANSEM/USDT, LAB/USDT:** MEXC-only (conf 38%). Require anchor/Bybit confirmation.
- **VANRY/USDT:** C-tier. Elevated funding -0.002. Risk penalty -14.9. Watch only.
- **All stocks intraday A/B:** Market closed; global paper guard blocking. Re-evaluate after 16:30 EEST.
- **UNH:** AVOID any long. Short: not actionable today.
- **Shorts (crypto):** All short setups capped C. EPIC: manual review required.
- **Chasing TRB:** TP1 already hit. No new entries.

---

## 10. Main Risks

1. **FOMC minutes July 8 (tomorrow):** Hawkish surprise triggers reversal. Reduce swing position sizes today.
2. **Stocks A/B paper failing:** 7d -3.3R/PF0.33. Global paper guard blocking. Do not override.
3. **Post-holiday US open volatility:** First US trading day after 4th July weekend. Gap risk + correlated crypto volatility at 16:30 EEST.
4. **46 symbols in post-unwind-chop phase:** Mixed continuation quality under bullish surface.
5. **Geopolitical (Russia/Ukraine NATO summit):** Minor risk-off signal.
6. **Reddit/social blocked:** Crowd context dark.
7. **Dead sources:** SEC EDGAR, Business Wire, Binance Announcements, t.me/coin_listing — reduced legal/delist detection coverage.

---

## 11. Action Plan — Next 4 Hours (11:39–15:39 EEST)

1. **BTC watch:** $63K resistance. Pullback to $62,000–62,400 = swing trigger. US open 16:30 EEST = next major test.
2. **XPL watch:** Pullback to 0.1078–0.1089. Do not market-buy above 0.1095.
3. **ETH watch:** Swing entry on pullback post US-open; size conservatively ahead of FOMC.
4. **TRB (existing):** Monitor TP2 (18.903) vs BE stop. Do not add.
5. **US market pre-open planning (16:30 EEST):** XLF (94.68), LLY (92.24), XLV (91.32), DIA (88.02) as candidates. UNH: AVOID long. Stocks guard blocking — do not force A/B.
6. **Do not enter TLM** at any current level.
7. **FOMC sizing:** New swing entries: size conservatively ahead of tomorrow's event.

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Note |
|---|---|---|---|
| Crypto scalp | Crypto | **LOW CONFIDENCE** | Known TP1/2h mismatch. XPL only (volume confirmed). Low conviction. |
| Crypto intraday | Crypto | **ACTIONABLE (cautious)** | XPL TRIGGERED (pullback needed). LAB/ANSEM MEXC-only. No-catalyst warning applies. TRB: do not enter (TP1 hit). |
| Crypto swing | Crypto | **WATCHLIST / WAIT FOR TRIGGER** | BTC + ETH B-tier swing triggered (macro-supported). PUMP downgraded. Best mode (PF5.80). Enter on pullback only. |
| Stocks intraday | Stocks | **PLANNING ONLY** | Market closed until 16:30 EEST. All A/B demoted C. Global guard blocking. Re-evaluate at RTH open. |
| Stocks swing / invest | Stocks | **SHADOW FRAMEWORK ONLY** | Not in proposed_signals. Not actionable. |

---

## 13. Sources

- [Bitcoin price today, BTC to USD live price, marketcap and chart](https://www.coindesk.com/price/bitcoin) — CoinDesk, 2026-07-06
- [Dollar nears two-week lows as rate-hike bets recede, sending Bitcoin and Ether sharply higher](https://cryptobriefing.com) — CryptoBriefing, 2026-07-06
- [UnitedHealth under criminal probe for possible Medicare fraud](https://finance.yahoo.com/news/unitedhealth-under-criminal-probe-possible-231729520.html) — Yahoo Finance, ongoing
- [UnitedHealth confirms it's under investigation by DOJ](https://www.healthcaredive.com/news/unitedhealth-under-investigation-department-of-justice-medicare/753913/) — Healthcare Dive, 2025
- [Alien Worlds (TLM) live price on Binance](https://www.binance.com/en/price/alien-worlds) — Binance, 2026-07-06
- Internal: `data/reports/scalp/2026-07-06_06-38_scalp_report.md`
- Internal: `data/reports/intraday/2026-07-06_06-45_intraday_report.md`
- Internal: `data/reports/stocks/intraday/2026-07-06_06-54_stocks_intraday_report.md`
- Internal: `data/reports/swing/2026-07-06_02-01_swing_report.md`
- Internal: `data/scheduled_runs/2026-07-06_default_schedule/cycle_03_09-30_summary.md`
- Internal: `data/catalysts/2026-07-06/catalyst_events.jsonl`

---

## 14. Fix Requests / TODO

### TODO-DEAD-SOURCES
- **issue:** 8 configured news/data sources are DEAD (enabled but not writing) including SEC EDGAR, Business Wire (Stocks), Binance Announcements, and t.me/coin_listing
- **evidence:** `data/reports/stocks/intraday/2026-07-06_06-54_stocks_intraday_report.md` §News/catalyst advisory
- **suggested manual fix:** Audit all 8 dead sources. Re-enable or replace SEC EDGAR (legal risk detection). Check Binance Announcements alternative. Remove permanently gone sources.
- **priority:** high

### TODO-STOCKS-AB-PAPER-FAILING
- **issue:** Stocks A/B paper 7d: -3.3R/PF0.33/n25; B-tier PF0.42 below 0.8 threshold; no-news long 30d: -5.7R/n93; global guard blocking both directions
- **evidence:** `data/reports/stocks/intraday/2026-07-06_06-54_stocks_intraday_report.md` §9 paper performance
- **suggested manual fix:** Review stocks intraday scoring thresholds. Consider hard "requires news_supported" gate for stocks B-tier longs. Manual sign-off needed.
- **priority:** high

### TODO-CATALYST-UNMAPPED-SYMBOLS
- **issue:** 10 high-importance symbols not mapped to catalyst_events: AMZN, ARB, AXP, BAC, BNB, HYPE, MKR, MS, SMH, SPY
- **evidence:** `data/scheduled_runs/2026-07-06_default_schedule/cycle_03_09-30_summary.md` step 5 catalyst integrity scan
- **suggested manual fix:** Investigate symbol resolver in catalyst layer for these tickers. Check `src/catalysts/` symbol resolution logic.
- **priority:** medium
