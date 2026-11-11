# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

**Slot:** pre-US-open decision review | **Time:** 2026-07-06 16:20 EEST | **Day:** Monday
**Previous review:** 2026-07-06 11:39 EEST (Europe / pre-US context)
**Advisory only — no auto-trade. Scanning always continues.**

*(Latest copy at: OPUS_ENRICHED_REVIEW_LATEST.md)*

---

## 1. Executive Summary

**Slot:** pre-US-open decision review (16:20 EEST). US cash session opens at 16:30 EEST (~10 min from review time). **Stocks are NOT yet actionable — RTH confirmation required for all intraday entries. Do NOT chase pre-market moves.**

**Crypto regime:** BTC ~$62,886 in confirmed uptrend. ETH uptrend confirmed. Altcoin breadth 78.95% above EMA20 (improved from 73.7% this morning). ATR percentile 13% (low-volatility compression — watching for breakout or fade into the US open). F&G=24 (Extreme Fear) diverges from bullish tape — wall-of-worry supportive. ETH/BTC=0.028178 (ETH still lagging BTC relatively).

**Stocks pre-market signals:** Dow Jones Futures rising per internal news feed. QQQ range-bound (range 707–731 today). TSLA delivery beat → likely positive gap at open → **do not short TSLA pre-open; wait RTH confirmation/failed retest**. COIN Q2 revenue miss expected → potential gap down → **do not long COIN pre-open**. All stock intraday signals demoted to C (market_closed) — will re-evaluate at RTH open.

**Crypto candidates:** 45 active B-tier signals (all longs). No A-tier. Best candidates for pre-US watch: **ETH/USDT** (B swing, catalyst-backed: Vitalik "biggest rebuild" + $25.3M whale withdrawal), **XLM/USDT** (B intraday, news_supported flip this cycle, RWA narrative, WAITING = clean entry structure), **BEL/USDT** (caution — triggered RS leader but OI +50%, elevated crowding). **XLM** is the cleanest pre-open long-watch trigger. **EPIC/USDT** is cleanest short for crypto (-14.5% 24h, fresh short pressure, low squeeze risk).

**Legal risks:** UNH — AVOID (DOJ criminal + civil fraud probe, shares -16%). MSFT — MANUAL REVIEW (securities fraud lawsuit). SMCI — AVOID long (export-control violations lawsuit ongoing).

**Key event risk:** FOMC minutes July 8 (tomorrow). Reduce swing sizing today; option market call-heavy into $63K+.

**Advisory only. No auto-trade. Scanning continues in all moods.**

---

## 2. Data Used

| Source | Mtime / Freshness | Status |
|---|---|---|
| scheduler.log | 2026-07-06 14:48 EEST | **FRESH** (1h32m) |
| cycle_05_14-23_summary.md | 2026-07-06 14:48 EEST | **FRESH** (1h32m) |
| scalp report `2026-07-06_11-30` | generated 14:30 EEST | **FRESH** (~2h) |
| intraday report `2026-07-06_11-35` | generated 14:35 EEST | **FRESH** (~2h) |
| stocks intraday `2026-07-06_11-45` | generated 14:44 EEST | **FRESH** (~2h) |
| swing report `2026-07-06_02-01` | 2026-07-06 05:01 EEST | **STALE** (>14h — flagged, excluded from final swing verdict) |
| stocks swing `2026-07-02_13-03` | 2026-07-02 | **STALE** (4 days — excluded) |
| stocks invest | Not generated | **N/A** |
| catalyst_events.jsonl | cycle_5 + cycle_11-36 | **FRESH** (500 events, 2 baskets) |
| intelligence layer | 2026-07-06 11:42 UTC | **FRESH** (derivatives/squeeze phase) |
| active-signals CLI (crypto) | 16:20 EEST live | **LIVE** (45 signals) |
| active-signals CLI (stocks) | 16:20 EEST live | **LIVE** (20 C-tier) |
| signal-stats CLI × 2 | cycle_5 embedded | **LIVE** |
| detect_untracked_legacy | 16:20 EEST live | **8 untracked alerts** |
| LLM analysis packet | 2026-07-06T11:35 UTC | **FRESH** |
| External: BTC price | WebSearch 16:20 EEST | ~$62,886 confirmed, uptrend ✓ |
| External: ETH, TSLA | WebSearch unavailable (2nd attempt) | Internal data only — downgraded per protocol |
| External: QQQ range | WebSearch 16:20 EEST | Range 707.56–730.83, opened 725.58 |
| Paper monitor | cycle_5 step 30 | **FRESH** (Open=5, Waiting=3, Entered-unresolved=33) |
| Previous review | OPUS_ENRICHED_REVIEW_AUTO_2026-07-06_1139.md | Loaded for §4 comparison |

**External web research:** Partially available. ETH/TSLA search failed (tool error). External verification for ETH and TSLA candidates based on internal data only; candidates downgraded to CAUTION/WATCH per §G protocol.

---

## 3. Scheduler / Data Freshness

- **scheduler.log** mtime 14:48 EEST — **NO DEFER** (1h32m, well within 3h threshold).
- **Cycle 5** (14:23–14:48 EEST): ok=32, failed=0. Weekday mode, stocks enabled, long-horizon swing/invest NOT run.
- Cycle 5 tracking (pre): checked=515, updated=0, tp_hits=361, stopped=0, expired=0. Revalidation: 7 stale=2, moved_away=1.
- Cycle 5 tracking (post): checked=539, updated=0, tp_hits=361. Revalidation: 29 signals, stale=24, moved_away=1.
- Intelligence layer: 127 derivative symbols; 156 timeline symbols; 2143 events; last event 11:37 UTC.
- Squeeze phase (cycle_5): phase_0_unknown=37, **phase_1_build_up=33**, phase_2_squeeze_expansion=7, phase_4_unwind=5, **phase_5_post_unwind_chop=45** (dominant — significant chop risk under bullish surface).
- Onchain: `interface_ready_config_missing` — no onchain data.
- Reddit: blocked 403 (all 3 sources) — social layer dark.
- Catalyst label refresh (cycle_5): 1008 scanned, **XLM flipped news_supported 0→1** (fresh this cycle).
- Paper shadow A/B: NOT_READY (4/6 criteria), forward-only: A=−197.54R, B=−35.06R (both negative, 11d window, 40% DATA_GAP_LATE excluded). Live locked. No auto-promote.

**Paper monitor (cycle 5, step 30 — 14:48 EEST):**

| Status | Count |
|---|---|
| OPEN ACTIONABLE | 5 |
| WAITING FOR ENTRY | 3 |
| ENTERED UNRESOLVED (filled, no TP/SL before window) | 33 |
| REVIEW / SHADOW | 145 |
| NO-ENTRY / STALE / MOVED AWAY | 87 |
| CLOSED (win/loss/flat) | 366W / 67L / 0flat |
| NEEDS REVIEW | 1 |

**Untracked legacy alerts (live, 16:20 EEST): 8 total** — CAKE/USDT (scalp, ×2), TLM/USDT (scalp/intraday, ×3), VANRY/USDT (intraday, ×1), TRB/USDT (scalp, ×1), PUMP/USDT (scalp, ×1). All sent to Telegram without proposed_signal — contribute nothing to PF/winrate.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-06 16:20 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["swing_report_stale_14h", "stocks_swing_stale_4d", "onchain_config_missing", "reddit_blocked"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log mtime 14:48 EEST (1h32m old)",
        "cycle_05 ok=32 failed=0",
        "scalp/intraday/stocks-intraday fresh (~2h)",
        "swing report 2026-07-06_02-01 is >14h (stale threshold)",
        "catalyst 500 events cycle_5, 2 baskets"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"],
      "data_missing": ["real_time_eth_price", "onchain_flows"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC ~$62,886 uptrend confirmed (external WebSearch)",
        "ETH uptrend (internal data)",
        "altcoin breadth 78.95% EMA20 (improved from 73.7% morning)",
        "ATR percentile 13% (low vol compression)",
        "F&G=24 (Extreme Fear) = wall of worry supportive",
        "VIX=16.33 (low)",
        "SPY uptrend +1.43% 5d; QQQ range -0.53% 5d",
        "ETH/BTC 0.028178 (ETH lagging BTC)",
        "dashboard: crypto_mode=trend, stocks_mode=risk_on",
        "Dow Jones Futures Rising (internal news)"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["fresh_catalyst", "narrative_supported", "mapping_weak"],
      "data_missing": ["verified_eth_catalyst_depth", "xlm_specific_catalyst_article"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "XLM news_supported flipped 0→1 cycle_5 (fresh)",
        "XRP: full MiCA CASP authorization 30 EEA countries (The Block)",
        "ETH: Vitalik biggest rebuild since Merge + $25.3M whale withdrawal (lookonchain)",
        "TSLA: Q2 delivery beat (JPMorgan $475, Baird $522)",
        "COIN: Q2 revenue miss expected (Baird, 8% below)",
        "Summer Finance hack $6M DAI (multi-source)",
        "500 events, 2 baskets; majority single_source verification"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "funding_extreme"],
      "data_missing": ["full_oi_numeric_history", "onchain_liquidation_map"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BEL: OI +50% 24h, funding -0.01 (crowding elevated)",
        "LAB: funding -0.005 to -0.012 across venues (crowding elevated)",
        "TLM: negative funding cross-venue (crowding moderate)",
        "PYTH: OI -0.78% (short covering, weaker quality)",
        "phase_5_post_unwind_chop=45 (dominant); phase_2_squeeze_expansion=7",
        "5 symbols in active unwind phase"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["chase_risk", "overextended", "clean_retest"],
      "data_missing": ["live_chart_tradingview", "real_time_l2_orderbook"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BEL: +24.6% 24h, triggered, no catalyst — significantly extended",
        "LAB: current 18.174, entry zone 17.6-18.0 (borderline extended from entry top)",
        "TLM: leveraged-pump narrative + 8 untracked Telegram alerts",
        "XLM: status=WAITING (not triggered yet) = cleanest entry structure",
        "ATR percentile 13% = compression; pullback entries preferred",
        "TradingView / manual chart check unavailable"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "OPEN ACTIONABLE: 5",
        "WAITING FOR ENTRY: 3 (including XLM intraday)",
        "ENTERED UNRESOLVED: 33 (entries filled, no TP/SL before window — NOT missed entries)",
        "REVIEW/SHADOW: 145",
        "NO-ENTRY/STALE/MOVED AWAY: 87",
        "CLOSED: 366W / 67L / 0flat",
        "NEEDS REVIEW: 1",
        "Stocks: all 20 active signals C-tier (market_closed demotion)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["legal_risk", "headline_risk", "correlation_cluster", "reduce_risk"],
      "data_missing": ["daily_drawdown_figure", "portfolio_exposure_sum"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "UNH: DOJ criminal + civil Medicare fraud probe (-16%) → AVOID long",
        "MSFT: securities fraud lawsuit → MANUAL REVIEW",
        "SMCI: export-control violations lawsuit → AVOID long",
        "45 active crypto signals all longs → correlation cluster risk",
        "FOMC minutes July 8 (tomorrow) → event risk swing entries",
        "APT token unlock next week (operator flag)",
        "ETH: UXLINK hacker 14K ETH, Step Finance exploiter (advisory flags)",
        "Paper shadow forward: A=−197.54R, B=−35.06R (both negative, not evidence)"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": ["forward_shadow_post_gate"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto_swing_narrative_rs_momentum: WR 72% PF 5.80 +24R (n=18) — PRIMARY",
        "crypto_intraday_catalyst_or_momentum (catalyst): WR 50% PF 2.75 +7R",
        "crypto_intraday_catalyst_or_momentum (no catalyst): WR 23% PF 0.70 −3R",
        "crypto_failed_bounce_short: WR 40% PF 2.00 +9R",
        "crypto_scalp: WR 12% PF 0.14 −6R — LOW CONFIDENCE",
        "stocks_intraday_rth_momentum (shorts): PF 9.00",
        "stocks A/B: PF 0.33 avgR −0.133 (7d, losing)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["wait_for_trigger", "longs_preferred", "legal_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto risk-on trend; breadth 78.95%; ATR compression",
        "US cash opens in ~10 min: stocks not RTH-confirmed yet",
        "Best long: XLM (WAITING, news_supported=1, clean entry) or ETH (catalyst swing)",
        "Best short: EPIC (−14.5%, fresh shorts, low squeeze risk)",
        "Best catalyst: ETH (dual catalyst) or XRP (MiCA, no active signal)",
        "Avoid: TLM (8 untracked, pump narrative), UNH (DOJ)",
        "FOMC tomorrow → reduce swing sizing",
        "Scalp LOW CONFIDENCE → 0.5× if used"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.75,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "XLM/USDT",
      "trigger": "Price enters WAITING zone; news_supported=1 confirmed; BTC ≥ $62,500",
      "reason": "news_supported flipped 0→1 this cycle; RWA narrative basket; WAITING = no-chase entry; intraday B-tier"
    },
    "best_short_candidate": {
      "symbol": "EPIC/USDT",
      "trigger": "Failed bounce below day's high; BTC neutral/stable; funding/OI no squeeze setup",
      "reason": "−14.5% 24h; fresh short OI build; funding −0.00044 (not squeezed); crowding low"
    },
    "best_catalyst_candidate": {
      "symbol": "ETH/USDT",
      "trigger": "B-tier swing holds above invalidation at RTH open; ETH/BTC ratio stable or improving",
      "reason": "Dual catalyst: Vitalik biggest rebuild narrative + $25.3M whale withdrawal; swing playbook PF 5.80"
    },
    "avoid_candidate": {
      "symbol": "TLM/USDT",
      "reason": "8 untracked Telegram alerts (0 proposed_signals); leveraged-pump narrative confirmed; invisible to PF tracking"
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
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | ok | 0.82 | risk_on, longs_preferred, mixed | advisory_only |
| catalyst_narrative | caution | 0.65 | fresh_catalyst, narrative_supported, mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.70 | squeeze_risk, oi_contradicts, funding_extreme | advisory_only |
| technical_entry | caution | 0.72 | chase_risk, overextended, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.85 | open_actionable, waiting_for_entry, entered_unresolved | advisory_only |
| risk_manager | caution | 0.78 | legal_risk, headline_risk, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | ok | 0.75 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.75 | wait_for_trigger, longs_preferred, legal_risk | advisory_only |

---

## 4. What Changed vs Previous Review

Previous review: 2026-07-06 11:39 EEST (Europe / pre-US context)

| Change | Detail |
|---|---|
| **Breadth improved** | 73.7% → 78.95% EMA20 (altcoin bid strengthening) |
| **Cycle 5 completed** | 14:23–14:48 EEST; ok=32, failed=0 |
| **XLM news_supported flip** | NEW: XLM flipped 0→1 in cycle_5 catalyst label refresh |
| **Active signals: 20→45** | Many watchlist=Y TP-hit signals added to live list |
| **Untracked alerts: 7→8** | PUMP/USDT added at 12:13 UTC |
| **Entered-unresolved: 31→33** | 2 more fills during cycles 4/5 |
| **TSLA catalyst confirmed** | Baird + JPMorgan both commented on delivery beat (new detail) |
| **COIN miss confirmed** | Baird Q2 revenue miss 8% below estimate (new detail) |
| **BEL crowding elevated** | OI +50% 24h now visible (crowding upgraded to elevated) |
| **Paper shadow NOT_READY** | Confirmed 4/6 criteria; forward both negative (A=−197.54R, B=−35.06R) |
| **Swing report stale** | 02:01 EEST report now >14h → crosses stale threshold, excluded |
| **No new A-tier crypto** | Unchanged from morning |
| **UNH/MSFT/SMCI legal** | Unchanged — all still active legal risk |
| **TLM still AVOID** | Worsened: 7→8 untracked alerts |

---

## 5. Catalyst Coverage

- **Total catalyst_events today:** 500 (cycle_5: events=500, baskets=2, scanned=500, rejected=0)
- **Mapped (non-null symbol):** Estimated ~55–60% (455 other_news are mix of mapped/unmapped; specific legal/regulatory events are mapped)
- **Unmapped (null symbol):** Estimated ~40–45%
- **Narrative baskets:** 2 active
  - `delisting_thin_liquidity` → primary: XRP/USDT — ⚠ see §7 Candidate 5 for contradiction analysis
  - `momentum_breakout` → primary: LAB/USDT, PYTH/USDT (no confirmed catalyst, pure momentum)
- **XLM catalyst flip:** news_supported 0→1 in cycle_5 refresh (underlying article not surfaced — see §14 TODO)

**Unmapped ~40–45%: borderline weak. Use catalyst layer as context, not final decision this run.**

**Top mapped catalysts:**

| Symbol | Type | Summary | Source |
|---|---|---|---|
| XRP/USDT | regulatory_sector_headline | Full MiCA CASP authorization, 30 EEA countries | The Block (single_source) |
| TSLA/USDT | earnings_event | Q2 delivery beat; Baird Outperform $522, JPMorgan Neutral $475 | t.me/WalterBloomberg (single_source) |
| COIN/USDT | earnings_event | Q2 revenue miss expected, 8% below estimate (Baird) | t.me/WalterBloomberg (single_source) |
| ETH/USDT | operator_review_flag | UXLINK hacker 14K ETH transfers; Step Finance laundering | AMBCrypto / CryptoBriefing (single_source) |
| MSFT/USDT | legal_risk | Securities fraud class action opportunity | PR Newswire (single_source) |
| UNH/USDT | legal_risk | DOJ fraud probe criminal + civil; shares −16% | QuiverQuant (single_source) |
| (basket) | exploit_hack | Summer Finance $6M DAI hack | The Block / CryptoBriefing / t.me/lookonchain (multi-source) |

---

## 6. Market Landscape

### Index Overview

| Asset | Trend | 5d | Notes |
|---|---|---|---|
| BTC | uptrend | — | ~$62,886 external confirmed; ATR 13th pct (compression) |
| ETH | uptrend | — | ETH/BTC 0.028178 (ETH lagging); Vitalik catalyst |
| SPY | uptrend | +1.43% | 20d −1.25% (US mkt only recovered recently) |
| QQQ | range | −0.53% | 20d −4.25%; range 707–731 today; tech sector weak |
| IWM | uptrend | −0.44% | 20d +3.44% (small caps showing strength) |
| DIA | uptrend | +1.66% | 20d +3.86%; Dow strongest index; futures rising |
| VIX | — | — | 16.33 (low; supportive risk-on) |

### Market Mood / Risk Routing

- **Crypto mood:** risk-on / trend. BTC uptrend confirmed (~$62,886, approaching $63K). ETH uptrend. Breadth 78.95% (improved). ATR 13th percentile = compression. F&G=24 (Extreme Fear) = wall-of-worry continuation supportive. 45 post-unwind-chop symbols = chop under the surface.
- **Stocks mood:** risk-on pre-market (VIX 16.33, SPY/DIA/IWM uptrend). QQQ range-bound (tech mixed). Financials/Healthcare/Industrials RS leaders. Semis/Tech weak. Dow futures rising. US cash opens in ~10 min from review time — NOT yet actionable.
- **Dominant narrative:** Altcoin RS momentum (TLM, BEL, VANRY, PYTH, LAB all long-biased) + regulatory tailwinds (MiCA/XRP). DeFi exploit concern. Stocks: delivery beat (TSLA), revenue miss warning (COIN), legal cluster (UNH/MSFT/SMCI).
- **Preferred side now:** Longs (crypto swing + catalyst-backed intraday). Wait-for-trigger (stocks — RTH required). Crypto shorts are squeeze-prone given post_unwind_chop dominant.
- **Best long candidate:** XLM/USDT — news_supported=1 (fresh), RWA basket, B-tier intraday WAITING (cleanest entry structure). Trigger: price enters WAITING entry zone; BTC ≥ $62,500.
- **Best short candidate:** EPIC/USDT — fresh −14.5% 24h, fresh short OI build, low crowding/squeeze risk. Trigger: failed bounce below day's high.
- **Best catalyst-backed candidate:** ETH/USDT — dual catalyst (Vitalik rebuild + whale withdrawal), B-tier swing triggered, swing playbook PF 5.80.
- **What to avoid:** TLM (pump narrative, 8 untracked), UNH (DOJ), BEL (crowding elevated, no catalyst).
- **What would change the view:** BTC break below $62,000 (invalidates all crypto longs); VIX spike above 20 (invalidates stocks risk-on); FOMC minutes hawkish surprise tomorrow.

---

## 7. Candidate Deep Dives

### Candidate 1: ETH/USDT — B-tier swing (triggered, catalyst-backed)

**Signal:** B-tier swing long, status=triggered. Score ~65–67 range.  
**Playbook:** `crypto_swing_narrative_rs_momentum` (WR 72%, PF 5.80, +24R 14d — primary actionable).

**Internal catalyst check (§G):**
- news_items (<24h): ETH confirmed — Vitalik "biggest rebuild since Merge" (CoinDesk) + whale withdrawal 14,267 ETH / $25.3M from Binance (t.me/lookonchain)
- Operator-review warning active: UXLINK hacker 14K ETH transfers, Step Finance exploiter. Advisory, does not gate routing.
- catalyst_events.jsonl: ETH listed with both catalysts (fresh attention/catalyst detected)

**External:** ETH web search unavailable this run → internal data only. Verification: single_source per catalyst.

**Price/chase/mood check:**
- Reacted? Partially — ETH in uptrend but lagging BTC (ETH/BTC 0.028178). Room to run if narrative catches.
- Chasing? Signal triggered — within entry window; not a market-buy chase
- Overextended? ATR 13th pct (low vol) — not overextended in absolute terms
- Entry fresh? Signal triggered in prior cycle; borderline; check price vs invalidation before entering
- RTH relevance? YES — US open flows may drive ETH/BTC ratio normalization. Watch for ETH/BTC to hold or improve.
- Invalidation: 1h close below signal's invalidation level
- Mood-aligned: YES (risk-on crypto, swing playbook preferred)
- Chase risk: LOW (triggered signal, not a momentum chase into top)

**FOMC caution:** Reduce size 25–50% vs standard due to FOMC minutes tomorrow.

**Verdict:** LONG-WATCH — best catalyst-backed swing today. Enter only if price still within entry zone per signal and BTC holds $62,500. Advisory only.

---

### Candidate 2: XLM/USDT — B-tier intraday (news_supported flip, WAITING)

**Signal:** B-tier intraday long, status=WAITING (not yet triggered). Clean entry — no chase.  
**Playbook:** `crypto_intraday_catalyst_or_momentum` with catalyst (WR 50%, PF 2.75, +7R).

**Internal catalyst check (§G):**
- XLM flipped news_supported 0→1 in cycle_5 catalyst label refresh (new this cycle)
- Active narrative baskets: rwa_narrative (playbook: related_beta_rotation); primary: ONDO/USDT, XLM/USDT
- XLM/Stellar ecosystem benefits indirectly from MiCA/XRP regulatory tailwinds
- Specific article driving the news_supported flip: not surfaced in catalyst_events (see §14 TODO)

**External:** WebSearch unavailable for XLM this run — internal only. Single_source confidence.

**Price/chase/mood check:**
- Reacted? NO — status=WAITING means price has NOT entered entry zone
- Chasing? NO — cleanest possible entry structure for this session
- Overextended? Unknown (chart unavailable); regime risk-on
- Entry fresh? FRESH — trigger not yet fired
- Trigger: price enters WAITING entry zone; BTC ≥ $62,500; news_supported holds
- Invalidation: Signal expires before price enters zone; BTC breaks $62,000
- Mood-aligned: YES — catalyst-backed intraday, risk-on regime, US open flows arriving

**Verdict:** BEST LONG-WATCH this window. Cleanest entry structure available. Monitor entry zone trigger at/after 16:30 EEST open. News_supported=1 activates the catalyst lane (PF 2.75 vs no-catalyst PF 0.70).

---

### Candidate 3: BEL/USDT — B-tier intraday (contradiction: RS leader vs crowding risk)

**Signal:** B-tier intraday long, status=triggered.  
**Playbook:** `crypto_intraday_catalyst_or_momentum` — NO CATALYST lane (WR 23%, PF 0.70, −3R).

**Internal catalyst check (§G):**
- No catalyst in news_items for BEL within 24h
- No entry in catalyst_events for BEL
- BEL is in momentum_breakout basket (no catalyst, pure momentum): "Top gainers without confirmed news catalyst"

**Derivatives check:**
- OI: +50% 24h (Bybit cross-check confirmed)
- Funding: −0.00995 Bybit, −0.009864 MEXC (elevated negative; crowding elevated)
- Long/short: 0.887 (slight short-skew)

**Price/chase/mood check:**
- Reacted? YES massively — +24.6% 24h already moved
- Chasing? YES — entered B-tier after +24.6% move with no catalyst
- Overextended? LIKELY (24.6% in 24h; no-catalyst)
- Playbook alignment: POOR — no-catalyst lane is the losing lane (PF 0.70)
- Chase risk: HIGH

**Verdict:** AVOID NEW ENTRY. Despite RS strength, BEL is: (1) no-catalyst intraday = losing lane, (2) OI +50% = crowding elevated, (3) +24.6% already = overextended. Any reversal could unwind fast. The playbook explicitly says "avoid no-catalyst intraday in chop." Not the setup to take at the US open.

---

### Candidate 4: TSLA — B-tier short (pre-demotion; RTH gate required)

**Signal:** Raw B-tier short (score 71.42). Demoted to C for market_closed_intraday_planning_only.  
**Playbook:** `stocks_intraday_rth_momentum` shorts (PF 9.00 historically in 14d).

**Legal/headline check (§I):** No active legal risk for TSLA. Q2 deliveries were the event. No earnings before Q2 results. CLEAR of legal/regulatory risk.

**Catalyst check:** Delivery beat is a POSITIVE fundamental catalyst for TSLA stock. This contradicts the short thesis pre-open. JPMorgan kept Neutral $475, Baird Outperform $522 — both buying the beat. **Pre-open: TSLA is likely to gap up or be bid.**

**Pre-market/gap risk:**
- Do NOT short into delivery-beat gap-up. This is a textbook short-squeeze setup pre-open.
- Short only becomes valid if: (1) RTH open, (2) gap-up fails to sustain above key resistance, (3) rejection with volume, (4) break below gap-open level in first 15–30 min

**RTH confirmation trigger:** Gap up → fails to hold above pre-market high → sells back below the gap-open level on above-average volume within 15–30 min of RTH.

**Verdict:** SHORT-WATCH — stocks only, RTH gate mandatory. Do not initiate before 16:30 EEST open. Do not short into the initial gap-up. Wait for a failed retest pattern. If the stock simply opens and continues, pass on the short for today.

---

### Candidate 5: XRP/USDT — catalyst contradiction analysis

**Signal:** No active A/B-tier XRP signal in current active-signals table. C-tier planning only (XRP in delisting basket).

**Catalyst contradiction:**
- POSITIVE: Ripple received full MiCA CASP authorization across 30 EEA countries (The Block, single_source) + Luxembourg preliminary license upgraded to full (CoinDesk, single_source) = MAJOR regulatory milestone for XRP institutional access
- CONTRADICTING: XRP is the PRIMARY symbol in `delisting_thin_liquidity` basket (playbook: avoid_low_liquidity)
- Basket summary: "Spain knocks out Portugal... Azul to List on NYSE" — basket appears to be assembled from multiple articles; XRP mapping to this basket may be artifact of article-level text matching rather than an actual XRP delisting event

**Assessment:** MiCA authorization is the more material, verified signal. The delisting basket association appears to be a mapping artifact. However, no A/B-tier XRP signal exists currently — XRP is not in the active-signals table as a crypto signal.

**Legal/headline check (§I):** Ripple's SEC case is historically resolved (XRP sold as non-security in secondary markets). No new legal risk detected.

**Verdict:** CATALYST-WATCH — XRP has real positive catalyst (MiCA) but no active signal. Monitor for B-tier generation in the next cycle (18:30 EEST slot). Do not act on catalyst without a backing signal. The delisting basket association should be flagged for review (is mapping artifact?) per §14.

---

## 8. Best Candidates Ranked

| Rank | Symbol | Class | Side | Verdict | Trigger | Confidence |
|---|---|---|---|---|---|---|
| 1 | **XLM/USDT** | Crypto intraday B | Long-watch | WAITING → cleanest entry | Enter WAITING zone; BTC ≥ $62,500 | medium |
| 2 | **ETH/USDT** | Crypto swing B | Long-watch | Triggered, catalyst-backed | Hold above invalidation; RTH crypto risk-on | medium |
| 3 | **EPIC/USDT** | Crypto intraday | Short-watch | Low squeeze risk | Failed bounce below day's high | medium-low |
| 4 | **TSLA** | Stocks intraday | Short-watch | RTH gate required | Gap up fails → breaks below gap-open on vol | medium |
| 5 | **XRP/USDT** | Crypto catalyst | Catalyst-watch | No active signal yet | B-tier generated in next cycle post-MiCA | low |

**If no signal triggers this window:**
- **Best long-watch trigger:** XLM enters WAITING entry zone — exact trigger from signal
- **Best short-watch trigger:** EPIC failed bounce below today's high after any relief bounce
- **Best catalyst-watch trigger:** XRP B-tier A/B signal generated in next cycle on MiCA continuation

---

## 9. Avoid / No Trade

This decision window only — scanning continues:

| Symbol | Reason |
|---|---|
| **TLM/USDT** | Leveraged-pump narrative; 8 untracked alerts today (0 proposed_signals); invisible to PF/winrate |
| **UNH** | DOJ criminal + civil Medicare fraud probe; shares −16%; LEGAL RISK — AVOID any long |
| **MSFT** | Securities fraud lawsuit; MANUAL REVIEW REQUIRED — not a clean long or short |
| **SMCI** | Export-control violations lawsuit; AVOID long; short needs legal escalation confirm |
| **BEL/USDT** | Chase risk: OI +50% crowding elevated, no catalyst, +24.6% already moved, PF 0.70 no-catalyst lane |
| **LAB/USDT** | MEXC-only cap (70); borderline extended (price 18.17, entry top 18.0); no catalyst; no-catalyst lane |
| **COIN** | Q2 revenue miss expected — likely gap down; do NOT long into gap; wait RTH confirm |
| **Any crypto scalp** | Playbook LOW CONFIDENCE (WR 12%, PF 0.14, −6R); 0.5× sizing only if forced; TLM/BEL scalps explicitly avoid |

---

## 10. Main Risks

1. **FOMC minutes July 8 (tomorrow):** Potential hawkish surprise → swing reversal risk. Options call-heavy into $63K — could be a vol event either direction. Reduce all new swing position sizing 25–50% today.

2. **BTC $63K compression:** ATR 13th percentile = extremely low vol. Compression resolves in one direction. If US open flows don't push BTC above $63K, could see a fade/consolidation that takes down all 45 active long signals.

3. **Crowding in RS leaders:** BEL OI +50%, LAB elevated funding. 45 active signals all longs = severe correlation cluster. A BTC fade = synchronized drawdown across all positions.

4. **DeFi exploit contagion:** Summer Finance $6M DAI hack + UXLINK hacker + Step Finance exploiter all active today. Low systemic risk for BTC/ETH but adds to negative DeFi sentiment.

5. **Stocks legal cluster:** UNH (−16%), MSFT (fraud), SMCI (export violation) — three concurrent legal risks. Any new A/B stock signals should be checked against this pattern.

6. **TLM tracking gap:** 8 alerts sent to Telegram with 0 proposed_signals. System is sending actionable-style alerts for TLM that contribute nothing to performance tracking — this creates an unquantified exposure in the PF stats.

7. **Paper shadow forward both negative:** A=−197.54R, B=−35.06R. NOT proof of either direction. Do not promote. Do not assume the system is winning or losing based on these figures alone.

---

## 11. Action Plan — next 4 hours

**16:20–16:30 EEST (final pre-open — now):**
- Monitor XLM/USDT: if price approaches WAITING entry zone, prepare (check BTC ≥$62,500, news_supported still=1, entry zone active)
- Do not initiate any stock intraday entries before 16:30 EEST
- Note BTC price action: is it approaching $63K or fading?

**16:30–17:00 EEST (RTH open — first 15-30 min):**
- **TSLA:** Watch gap-open direction. If gap-up fails (breaks back below gap-open level on volume within 15 min) → short becomes valid. If it holds or extends → pass the short today.
- **DIA/XLF:** If opens strong and holds (Dow futures positive, financials sector RS leader) → cleanest stocks long candidate. Wait full 15 min before any entry.
- **ETH:** Watch ETH/BTC ratio. If ratio holds 0.028 or improves → ETH swing signal remains active. If ratio breaks lower → ETH swing caution.
- **XLM:** If WAITING zone still not hit → continue watching. If triggered → intraday catalyst-backed setup is live.

**17:00–20:00 EEST (settling / directional confirmation):**
- If BTC breaks $63K with volume → altcoin breadth should improve further → XLM/TRB continuation setups more reliable.
- If BTC rejects $63K → tighten crypto exposure, prioritize cash / EPIC short.
- Do not add new swing positions today; carry existing triggered signals only. FOMC tomorrow.

**20:30 EEST — US open reaction review (next auto slot):**
- Cycle 6 (18:30 EEST) will provide fresh reports with RTH prices. Re-evaluate all stocks candidates then with confirmed RTH direction.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Notes |
|---|---|---|
| **Crypto swing** | ✅ PROCEED (caution sizing) | ETH B-tier triggered, catalyst-backed. PF 5.80 playbook. Reduce size 25–50% for FOMC tomorrow. |
| **Crypto intraday (catalyst)** | ✅ PROCEED — XLM only | XLM news_supported=1, WAITING (clean). PF 2.75 catalyst lane. |
| **Crypto intraday (no catalyst)** | ⚠️ AVOID this window | PF 0.70, WR 23%. BEL/LAB are no-catalyst momentum → skip. |
| **Crypto scalp** | ⚠️ LOW CONFIDENCE | PF 0.14, WR 12%. Research grade. 0.5× sizing only. Avoid TLM/BEL scalps. |
| **Crypto short** | 👀 WATCH-ONLY (EPIC trigger) | EPIC failed-bounce setup only. Most longs are chop-zone / squeeze-prone. |
| **Stocks intraday** | 🔴 NOT ACTIONABLE pre-open | Demoted C. Re-evaluate post 16:30 EEST RTH with 15-min confirmation. |
| **Stocks intraday (post-RTH)** | 👀 WATCH — TSLA short / DIA long | TSLA: failed-gap trigger. DIA/XLF: 15-min confirm. Legal checks mandatory for all. |
| **Stocks swing** | 🔴 STALE DATA | Last report 4 days old → excluded. Research only. |
| **Stocks scalp** | 🔴 NOT IMPLEMENTED | System: "stocks scalp unavailable in this CLI" |

---

## 13. Sources

External:
- [Current price of Bitcoin July 6 2026 | Fortune](https://fortune.com/article/price-of-bitcoin-07-06-2026/) — BTC ~$62,886 (July 6, 2026); date: 2026-07-06; verification: primary_source
- [Invesco QQQ Stock Price | Investing.com](https://www.investing.com/etfs/powershares-qqqq) — QQQ range 707.56–730.83, opened 725.58; date: 2026-07-06; verification: primary_source

Internal (no external URL, read-only project files):
- `data/scheduled_runs/2026-07-06_default_schedule/cycle_05_14-23_summary.md`
- `data/reports/intraday/2026-07-06_11-35_intraday_report.md`
- `data/reports/scalp/2026-07-06_11-30_scalp_report.md`
- `data/reports/stocks/intraday/2026-07-06_11-45_stocks_intraday_report.md`
- `data/catalysts/2026-07-06/catalyst_cycle_11-36.md`
- `data/processed/llm_analysis_packet.md`
- `OPUS_ENRICHED_REVIEW_AUTO_2026-07-06_1139.md`
- `python -m src.cli active-signals --asset-class crypto` (live, 16:20 EEST — 45 signals)
- `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-06` (8 untracked alerts)

**ETH and TSLA external web search unavailable (tool error on 2nd query attempt).** Declared at top of §1 and §2 per §N source-discipline checklist. ETH/TSLA candidates derived from internal data only.

---

## 14. Fix Requests / TODO

### TODO-TLM-untracked-alerts
- **issue:** TLM/USDT generates repeated Telegram alerts (3+ per day, multiple modes) with no corresponding proposed_signal — alerts are invisible to PF/winrate tracking
- **evidence:** `detect_untracked_legacy_alerts 2026-07-06`: TLM appears at 09:05, 09:56, 11:30 UTC (scalp + intraday modes); 0 proposed_signals with matching IDs
- **suggested manual fix:** Investigate the B-tier signal persistence path for TLM (possible: MEXC-only cap causes demotion after watchlist_alert write but before proposed_signal write). Audit `src/signals/` or `src/pipeline/` for demotion logic ordering. Consider whether the alert-write gate should be atomic with proposed_signal creation.
- **priority:** medium
- **first observed:** 2026-07-06 16:20 EEST

### TODO-swing-report-mid-day-gap
- **issue:** Swing report last updated at 02:01 EEST (>14h at review time). No mid-day swing refresh in cycles 4 or 5. Pre-US-open slot has stale swing data.
- **evidence:** `data/reports/swing/` — latest `2026-07-06_02-01_swing_report.md`; cycle_5 step log: `Daily long-horizon swing/invest included: False`; the scheduler appears to skip swing during the US-session intraday cycles
- **suggested manual fix:** Check `config/scheduler.yaml` (or equivalent) for swing report frequency. Consider whether the 14:23 EEST weekday cycle should include at least one swing refresh to keep pre-US-open reviews valid.
- **priority:** medium
- **first observed:** 2026-07-06 16:20 EEST

### TODO-xlm-catalyst-flip-article-tracing
- **issue:** XLM flipped news_supported 0→1 in cycle_5 catalyst label refresh, but the specific news_item driving this flip is not surfaced in catalyst_events.jsonl or the intraday report's catalyst section. The flip exists but the underlying article is opaque.
- **evidence:** cycle_5 step 6: `news_supported 0->1: XLM`; XLM not listed in intraday report §5 catalyst/events block; not found in catalyst_cycle_11-36.md top events
- **suggested manual fix:** Add debug output to the catalyst label refresh step logging which specific news_item row(s) caused each news_supported flip (symbol, source, headline, published_at). This would allow the enriched-review process to validate catalyst depth for WAITING signals.
- **priority:** low
- **first observed:** 2026-07-06 16:20 EEST
