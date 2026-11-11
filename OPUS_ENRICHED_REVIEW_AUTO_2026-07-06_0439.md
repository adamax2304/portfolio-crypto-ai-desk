# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

**Slot:** crypto overnight / Asia review | **Time:** 2026-07-06 04:39 EEST | **Day:** Monday (first weekday after 4th July US holiday weekend)
**Previous review:** 2026-07-05 23:22 EEST (post-close final daily — Sunday weekend mode)
**Advisory only — no auto-trade. Scanning always continues.**

*(History copy — identical to OPUS_ENRICHED_REVIEW_LATEST.md at 04:39 EEST)*

---

## 1. Executive Summary

**Slot:** crypto overnight / Asia review (04:30 EEST). First weekday cycle after the US 4th July holiday weekend. Stocks CLOSED; US cash session reopens ~16:30 EEST today (Monday July 6).

**Overnight regime:** BTC/ETH both confirmed uptrend overnight. Altcoin breadth strong: 87% above EMA20, 85% above EMA50. ATR percentile low (10-11%) — compression phase. BTC ~$62,666 (external), approaching the $63K options strike that options market is call-heavy into. F&G=24 (Extreme Fear) — diverges from price action, a "wall of worry" supportive of continuation.

**New developments vs last review:** (1) Weekday mode activated — 35-step cycle 11 completed fully, all OK. (2) Untracked legacy alerts = 0 (was 23 Sunday — possible resolution or new cycle fresh start). (3) Entered-unresolved dropped from 43 → 22 (21 positions resolved overnight, net positive). (4) Vitalik "Lean Ethereum" roadmap confirmed externally (published July 4) — 3-4yr plan, not a near-term price catalyst; ETH/BTC = 0.028 (ETH underperforming). (5) TLM +44-48%/24h externally confirmed as **leveraged-contracts + tournament pump** — no organic catalyst; Binance delisting monitoring still active (no delist date set).

**No A-tier crypto signals.** Top B-tier swing: PUMP/USDT (75.6 — cleanest), TLM (72.4 — AVOID new entry), VANRY (72.4 — triggered on intraday/scalp, swing waiting).

**Stocks:** all 20 active signals are C-tier (not Telegram-actionable). AAPL has 1 shadow position framework candidate (reclaim_after_shakeout, score=77 — shadow only, planning context for Monday open).

**Key event risk:** FOMC minutes July 8 (Tuesday) — options market call-heavy → potential BTC breakout above $63K or event-driven reversal if hawkish surprise.

**Preferred side:** longs via RS-leader pullbacks (swing is strongest mode, PF=3.55). No clean short candidates. Scalp remains low-confidence (1W/7L historically). **Advisory only. No auto-trade.**

---

## 2. Data Used

| Source | Mtime / Freshness | Status |
|---|---|---|
| scheduler.log | 2026-07-06 04:33 EEST | **FRESH** (6 min) |
| cycle_11_03-58_summary.md | 2026-07-06 04:31 EEST | **FRESH** (7 min) |
| scalp report `2026-07-06_01-06` | 2026-07-06 04:06 EEST | **FRESH** (33 min) |
| intraday report `2026-07-06_01-12` | 2026-07-06 04:12 EEST | **FRESH** (27 min) |
| swing report `2026-07-06_01-27` | 2026-07-06 04:28 EEST | **FRESH** (11 min) |
| stocks intraday | not yet generated today | **CARRY-FORWARD** (market closed) |
| stocks swing / invest | deprecated/removed | N/A |
| catalyst_events.jsonl | 2026-07-06 04:12 EEST | **FRESH** |
| catalyst_cycle_01-12.md | 2026-07-06 04:12 EEST | **FRESH** |
| intelligence layer | 2026-07-06 01:18 UTC | **FRESH** |
| paper monitor status | cycle 11 (04:31) | **FRESH** |
| active-signals CLI × 2 | cycle 11 embedded | **LIVE** |
| signal-stats CLI × 2 | cycle 11 embedded | **LIVE** |
| detect_untracked_legacy | cycle 11 embedded | **CLEAN (0)** |
| External: BTC/market | WebSearch 04:39 | BTC ~$62,666 (July 5), F&G=24, uptrend holds |
| External: TLM Binance status | WebSearch 04:39 | Monitoring active, no delist date; pump = leveraged + tournament |
| External: ETH Vitalik roadmap | WebSearch 04:39 | "Lean Ethereum" July 4, 3-4yr plan, confirmed |

---

## 3. Scheduler / Data Freshness

- scheduler.log mtime 04:33 EEST — **NO DEFER** (well within 3h threshold).
- Cycle 11 result: ok=35 / failed=0 (04:31 EEST). Weekday mode with stocks and long-horizon swing enabled.
- Cycle 11 tracking: checked=583, updated=0, tp_hits=367, stopped=0, expired=0. Revalidation: 60 signals, stale=0, moved_away=0.
- Intelligence layer: 127 derivative symbols; 156 symbols in timeline; 2067 events; last event 01:11 UTC.
- Squeeze phase distribution: phase_0_unknown=42, phase_1_build_up=36, phase_2_expansion=3, phase_3_distribution=2, phase_4_unwind=3, **phase_5_post_unwind_chop=41** (significant chop pool).
- Onchain: `interface_ready_config_missing` (no config/onchain.yaml) — no onchain data.
- Reddit social: blocked 403 (all 3 sources) — social layer remains dark.

**Paper monitor (cycle 11, as of 04:31 EEST):**

| Status | Count |
|---|---|
| OPEN ACTIONABLE | 6 |
| WAITING FOR ENTRY | 12 |
| ENTERED UNRESOLVED (filled, no TP/SL before window) | 22 |
| REVIEW / SHADOW | 198 |
| NO-ENTRY / STALE / MOVED AWAY | 32 |
| CLOSED (win/loss/flat) | 372W / 36L / 0flat |
| NEEDS REVIEW | 0 |

- Entered-unresolved (22): entries were filled overnight; no TP or stop triggered before window expiry — **NOT missed entries**.
- No-entry / moved-away (32): price never reached trigger or moved away before entry — N/A lifecycle.
- Paper shadow A/B: A net −164.57R / B net +27.72R (Δ192.29R all-time). FORWARD-only (no backfill look-ahead): A −124.30R / B +31.42R. Promotion gate: **NOT_READY** (forward duration <14 days, data_gap_late elevated for stocks intraday).
- Paper portfolio (active: bybit_non_vip_usdt_perp): $7,379 net (+47.58%) vs $5,000 start. Conservative-taker: $7,077 (+41.53%). Zero-fees: $10,740 (+114.8%). Fee drag: ~$2,000 (fees eat 307 BE trades, converting them to losses).

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-06 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.90,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "reddit_social_blocked"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 04:33 (6 min)", "cycle 11 ok=35 failed=0", "all reports <33 min old", "untracked=0", "intelligence 01:18 UTC"]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC uptrend", "ETH uptrend", "breadth EMA20 87%", "breadth EMA50 85%", "ATR pct 10-11% (compression)", "F&G=24 (Extreme Fear vs bullish price)", "VIX=16.15", "SPY up / QQQ down", "ETH/BTC=0.028 (ETH underperforming)"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["fresh_catalyst", "catalyst_contradicted", "narrative_supported", "stale_catalyst"],
      "data_missing": ["derivatives_sparse"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ETH Vitalik Lean Ethereum July 4 (3-4yr, not near-term)", "BTC macro delayed-hike narrative", "FOMC minutes July 8 event risk", "TLM pump = leveraged contracts + tournament (no organic catalyst)", "ETH/SOL/APT exploit advisory", "ai_narrative basket (NEAR/RENDER/TAO/FET)", "rwa_narrative basket (ONDO/XLM)", "12 high-importance symbols not mapped in catalyst_events (AMZN/ARB/AXP/BAC/BNB/HYPE/MKR/MS/SMH/SPY)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.58,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["derivatives_sparse"],
      "suggested_effect": "advisory_only",
      "facts_used": ["VANRY OI +50.52% + negative funding (Bybit -0.000424, MEXC -0.000444) — potential short-squeeze fuel or crowded-long risk", "TLM OI +34% normal crowding funding neutral", "GIGGLE OI +26% L/S=1.735", "41 symbols in phase_5_post_unwind_chop", "36 in phase_1_build_up", "3 in phase_2_squeeze_expansion", "OI numeric history sparse per intelligence note"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["entry_late", "chase_risk", "overextended", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TLM +284%/7d +44%/24h — extreme extension, chase risk high", "PUMP at/near resistance 0.0017, needs pullback to 0.0016", "VANRY +82%/7d triggered intraday/scalp, swing waiting for deeper pullback 0.0052-0.0054", "ATR percentile 10-11% — very low volatility compression", "no chart MCP available — technical read from OHLCV fields only", "scalp mode: 1W/7L historically (low confidence)"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["OPEN ACTIONABLE=6", "WAITING=12", "ENTERED UNRESOLVED=22 (filled, no TP/SL, NOT missed entries)", "REVIEW/SHADOW=198", "NO-ENTRY/STALE/MOVED-AWAY=32", "NEEDS REVIEW=0", "Entered-unresolved dropped 43→22 overnight (21 resolved)", "untracked=0 (clean vs 23 Sunday)", "cycle 11 tracking: expired=0 ambiguous=0"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.74,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TLM Binance delisting monitoring since May 22 (monitoring active, no date set)", "ETH exploit advisory (UXLINK hacker 14,336 ETH transfers)", "SOL exploit advisory (Step Finance $21M laundered via Tornado Cash)", "APT exploit advisory (critical vulnerability patched)", "FOMC minutes July 8 = event risk (call-heavy options → upside OR hawkish surprise = risk-off)", "all-long positioning (0 shorts in active signals)", "short playbook −2.5R historically this week", "crypto paper (with fees): both A and B net-negative on crypto alone; stocks drives B advantage", "fee-sensitive edge: 307 BE trades become losses with fees"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "ok",
      "confidence": 0.80,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto swing: PF=3.55, WR=72% (14d) — strongest mode", "Crypto intraday no-catalyst: WR=23%, PF=0.70, −3R (structurally negative)", "Scalp: 1W/7L historically — low confidence", "Crypto A/B overall: PF=2.627, WR=21.9%, +81.35R sample=336", "Stocks A/B: PF=0.333, WR=3.1%, −3.33R sample=32 (net negative)", "Stocks C-tier: PF=0.47, −13.67R (not Telegram-actionable)", "Weekend signals: WR=24% (underperform)", "B-tier WR 22% system observation"]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.76,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesised all 8 agents", "risk-on regime with compression", "PUMP cleanest entry (pullback needed)", "TLM contradicted by delisting + leveraged pump", "ETH catalyst multi-year not immediate", "VANRY OI expansion warrants caution on crowding but potential squeeze", "FOMC July 8 = manage event risk", "stocks closed until 16:30 EEST"]
    }
  ],
  "head_trader": {
    "overall_verdict": "normal",
    "confidence": 0.76,
    "preferred_side": "longs",
    "best_long_candidate": {
      "symbol": "PUMP/USDT",
      "trigger": "pullback into 0.0016 zone confirmed by BTC holding above current structure and volume pickup",
      "reason": "Highest swing B score (75.6), RS leader, 1.17x volume, not over-extended (7d +16%), normal derivatives crowding, cleanest entry setup of active signals"
    },
    "best_short_candidate": {
      "symbol": "none — trigger: BTC 1h close below $61,000 (invalidates uptrend) + EPIC/USDT failed retest of 24h breakdown zone",
      "trigger": "BTC structural break below $61K or TLM fails retest of recent highs after any Binance delisting announcement",
      "reason": "No clean short in current risk-on; macro is anti-short (delayed hike narrative + call-heavy options); wait for structural breakdown"
    },
    "best_catalyst_candidate": {
      "symbol": "ETH/USDT",
      "trigger": "Pullback to $1,720-1,750 zone holding above swing support; ETH/BTC ratio stabilizing above 0.027; no new exploit news in 24h",
      "reason": "Vitalik Lean Ethereum roadmap (July 4, confirmed externally) is a genuine multi-year bullish catalyst; ETH/BTC at multi-month low = mean-reversion potential; requires confirmation of support hold"
    },
    "avoid_candidate": {
      "symbol": "TLM/USDT",
      "reason": "Binance delisting monitoring active since May 22 (no delist date but under review); externally confirmed as leveraged-contracts + tournament pump (no organic catalyst); +284%/7d extreme extension; chase risk maximum; any Binance delist announcement = catastrophic downside"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | **ok** | 0.90 | scheduler_fresh, report_stale | advisory_only |
| market_regime | **ok** | 0.82 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | **caution** | 0.70 | fresh_catalyst, catalyst_contradicted, narrative_supported | advisory_only |
| derivatives_squeeze | **caution** | 0.58 | oi_supports, data_unavailable | advisory_only |
| technical_entry | **caution** | 0.68 | entry_late, chase_risk, overextended, clean_retest | advisory_only |
| execution_lifecycle | **ok** | 0.82 | open_actionable, waiting_for_entry, entered_unresolved | advisory_only |
| risk_manager | **caution** | 0.74 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | **ok** | 0.80 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | **ok** | 0.76 | risk_on, longs_preferred, wait_for_trigger | advisory_only |

**Council summary:** 4 ok / 4 caution / 0 bad. Caveats concentrated in catalyst contradiction (TLM), derivative data sparsity (OI numeric history), entry extension risk, and legal/exploit advisory flags. Regime and lifecycle are clean.

---

## 4. What Changed vs Previous Review

**Previous review:** 2026-07-05 23:22 EEST (post-close final daily, Sunday, weekend mode)

| Item | Previous (23:22) | Now (04:39) | Change |
|---|---|---|---|
| Mode | Weekend/crypto-only | Weekday, crypto+stocks | Upgraded |
| Untracked alerts | 23 (PART-1 regression) | **0** (clean) | Resolved / fresh-cycle |
| Entered unresolved | 43 | **22** | −21 positions resolved overnight |
| Active crypto signals | ~40+ (50 reported) | 20 top (full set ~40) | Same pool, new cycle priority |
| Stocks signals | All C-tier (carry) | All C-tier (fresh cycle) | No new A/B |
| AAPL shadow | Not reported | score=77 reclaim_after_shakeout | New shadow candidate |
| TLM delisting | Monitoring (monitoring) | Confirmed externally: no date set, pump = leveraged | Contradiction confirmed |
| ETH catalyst | Vitalik roadmap mentioned | Confirmed externally: Lean Ethereum July 4, 3-4yr | Confirmed, not near-term |
| BCH thesis | Swing entered ~234, TP1 hit | Not in top 20 active | TP hit, carry |
| Short playbook | −2.5R noted | Still 0 shorts active | No change |
| FOMC minutes | July 8 flagged | July 8 = event risk, 2 days | Same, closer |

**New:** AIGENSYN consistent in top RS for 2nd consecutive cycle. GIGGLE added to swing signals. ULTIMA/USDT appears in intraday.
**Removed from top 20:** BCH (TP hit — no longer in priority queue), WLFI, EIGEN, HOT (TP hit, still tracking but moved down priority).
**Confirmed:** Bullish bias held overnight with no structural break. Swing long playbook continues as the dominant mode.

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 422
- **Narrative baskets:** 3
  - `delisting_thin_liquidity` (avoid_low_liquidity) — primary: none; watch
  - `rwa_narrative` (related_beta_rotation, <6h) — primary: **ONDO/USDT, XLM/USDT**
  - `ai_narrative` (related_beta_rotation, <24h) — primary: **NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT**; related: WLD/USDT, ASTER/USDT
- **Catalyst integrity:** 12 high-importance symbol-tagged catalysts NOT mapped into catalyst_events: AMZN, ARB, AXP, BAC, BNB, HYPE, MKR, MS, SMH, SPY
- **Unmapped fraction estimate:** <10% of total 422 events → no "weak this run" override applies. Mapping is adequate.

**Notable events:**
- **ETH/USDT:** Vitalik "Lean Ethereum" roadmap (July 4) — quantum resistance + STARKs + simplified consensus; 3-4yr timeline. *(source: cryptotimes.io, beincrypto.com — confirmed)*
- **UNH/USDT:** DOJ fraud probe confirmed, shares −16% (QuiverQuant) → LEGAL RISK. Stock is C-tier only; any actionability blocked.
- **APT/USDT:** Aptos critical vulnerability fix (exploit_hack advisory — operator review).
- **ETH/USDT:** UXLINK hacker 14,336 ETH transfers (exploit_hack advisory — operator review).
- **SOL/USDT:** Step Finance exploiter sold $21M SOL via Tornado Cash (exploit_hack advisory — operator review).
- **Legal basket (stocks):** HUBG, ZTS, CHX, LCID, CVLT securities fraud lawsuits (baskets, not symbol-mapped).
- **Rumours (low confidence):** XLM (Haaland speculation); SOL (Mbappé meme token speculation).

**Top by importance:** UNH DOJ probe (0.73), HUBG/ZTS/CHX legal (0.71-0.75), ETH Lean Ethereum roadmap (0.61).

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** `risk-on` — BTC/ETH uptrend; 87% EMA20 breadth; BTC ~$62,666 (external); ATR compression at 10-11th pct; F&G=24 (Extreme Fear vs bullish price = wall of worry).
- **Stocks mood:** `closed` — US market reopens ~16:30 EEST today (Monday July 6). Pre-market context only. VIX=16.15 (low fear for equities). SPY=up, QQQ=down (tech under pressure — AI chip selloff cited externally). AAPL shadow candidate (score=77, planning only).
- **Dominant narrative:** "Delayed Fed rate hikes + gold/BTC macro correlation" — BTC rising in line with gold/silver as markets price delayed hikes. FOMC minutes July 8 = key inflection in 2 days. Ethereum "Lean Ethereum" multi-year roadmap (structural bullish, not a near-term catalyst). AI narrative basket (TAO/RENDER/FET/NEAR) in related-beta rotation.
- **Preferred side now:** `longs` — swing pullbacks on RS leaders. Scalp low-confidence. No clean short.
- **Best long candidate:** PUMP/USDT — pullback to 0.0016, BTC structure stable, volume confirmation
- **Best short candidate:** none now — trigger: BTC 1h close below $61,000 OR TLM fails retest post-Binance-delist-announcement
- **Best catalyst-backed candidate:** ETH/USDT — "Lean Ethereum" July 4 (confirmed), pullback to $1,720-1,750 zone, ETH/BTC stabilization above 0.027
- **What to avoid:** TLM (delisting monitoring + leveraged pump + +284%/7d); scalp (1W/7L); new shorts in risk-on regime; US stocks before RTH (C-tier only)
- **What would change the view:** BTC closes below $61K on 1h (uptrend invalidation) OR FOMC minutes July 8 more hawkish than expected (rate hike back on table) OR Binance formal TLM delist announcement (delist date set)

---

## 7. Candidate Deep Dives

### Candidate 1 — TLM/USDT (CONTRADICTION — AVOID NEW ENTRY)

**Signal:** B-tier, swing (score 72.4) + intraday (66.1) + scalp (71.4). Direction: long. Status: WAITING FOR ENTRY (swing), TRIGGERED (intraday/scalp).

**Setup:** Entry pullback 0.0032-0.0034. Current price: ~0.0034 (swing report). Support: 0.0023. Resistance: 0.0038. ATR: 0.0003. TP1: 0.0037, TP2: 0.0040, TP3: 0.0043.

**Catalyst check (internal):** No fresh verified catalyst in catalyst_events for TLM.

**External research:** Externally confirmed via [interactivecrypto.com](https://www.interactivecrypto.com/tlm-rockets-55-on-leveraged-contracts-and-alien-worlds-tournament-amid-broader-crypto-rally-jul) — the 55% pump is driven by **leveraged contracts + Alien Worlds Tournament**, NOT by a fundamental catalyst. No organic demand driver verified.

**Binance delisting monitoring:** Monitoring since May 22, 2026. No final delist date announced. Remains under review. Any Binance announcement = catastrophic downside risk.

**Chase/extension check:**
- 24h: +44-48%
- 7d: +284%
- Volume: 0.26x (below average on the swing) → pump on thin volume + leveraged OI
- OI change: +34.03%. Funding: near-zero (5e-05) → longs not paying a squeeze premium yet, but OI expansion is significant
- Is this chasing? **YES — extreme extension.** Entry zone 0.0032-0.0034 is only 12-15% below the 7d top. A delisting event would return TLM to pre-pump levels (sub-0.001).

**Mood alignment:** BTC risk-on favors longs, but this specific token carries binary Binance risk that is completely independent of macro regime. **Not mood-aligned for new entry.**

**LEGAL/HEADLINE RISK:** Binance delisting monitoring is an active headline risk. No legal charges, but platform risk is equivalent in effect.

**Verdict: AVOID new entry. Final verdict: AVOID.** Existing triggered intraday/scalp signals may be monitored for TP hits (they entered before this review), but no new positions should be added. The leveraged pump without organic catalyst on a delisting-monitored token is a textbook avoid scenario.

---

### Candidate 2 — PUMP/USDT (BEST LONG-WATCH)

**Signal:** B-tier, swing (score 75.6) + intraday (72.0). Direction: long. Status: WAITING FOR ENTRY (swing), TP_HIT (intraday — already at first target).

**Setup (swing):** Entry pullback 0.0016. Current price: ~0.0017. Support: 0.0015. Resistance: 0.0017. ATR: ~0.0001-0.0002 (display rounds to 0.0000 at this precision). TP1: 0.0017 (at resistance), TP2: 0.0017, TP3: 0.0018. Invalidation: 1h close beyond 0.0016.

**Important nuance:** Price is currently AT the resistance level (0.0017) which is also TP1. This means: the intraday signal already HIT TP1 (confirmed by tp_hit status), and the swing signal is WAITING for a pullback back INTO the 0.0016 entry zone. This is NOT a breakout chase — it's a retest-pullback structure.

**Derivatives:** Price up + OI up (+3.75%) → fresh positioning, normal crowding. Funding 5e-05 (near-zero, neutral). Long/short 1.183 (slightly long-heavy but not extreme). OKX cross-check: funding 3.24e-05 (neutral). **No squeeze risk, clean derivatives.**

**Catalyst check:** No fresh verified catalyst. This is a pure momentum/RS play.

**RS credentials:** 24h +7-8%, RS vs BTC +5.9-6%. 7d +15.9%. **Not over-extended** compared to TLM/VANRY. Volume 1.17x (above average) — the only signal with volume above 1x in the top set.

**Chase check:**
- Is price already reacted to catalyst? No catalyst (not applicable).
- Is setup chasing? **NO — waiting for pullback from resistance to support zone.**
- Retest/pullback structure? YES — price at resistance (0.0017), entry zone below at 0.0016 = retest of support.
- Overextended (>2 ATR from EMA20)? Cannot confirm without EMA20 value; 7d +16% is not extreme.
- Entry NOW late? **Not applicable** — signal is WAITING, not triggered.
- Actionable now or after confirmation? **After pullback to 0.0016 confirmed with BTC structure intact.**
- Invalidation: 1h close below 0.0016.

**Mood alignment:** Risk-on macro → longs preferred. PUMP is RS-leader with volume confirmation. **Aligned.**

**Verdict: BEST LONG-WATCH.** Cleanest setup in the current pool. Wait for pullback to 0.0016 entry zone. Do not buy the 0.0017 resistance without a confirmed pullback-and-hold. If pullback occurs with BTC stable, this is the highest-priority swing candidate.

---

### Candidate 3 — ETH/USDT (CATALYST-BACKED — WAIT FOR CONFIRMATION)

**Signal:** B-tier, swing (score 65.3). Direction: long. Status: WAITING FOR ENTRY.

**Setup (swing):** Entry zone not extracted from report (not in top-3 swing — needs full report read), but externally ETH at ~$1,771 (July 5). From the scalp/intraday reports, ETH shows uptrend. ETH/BTC = 0.028 (very low — underperforming vs BTC significantly).

**Catalyst:** Vitalik "Lean Ethereum" roadmap published July 4. External verification confirms: ["Lean Ethereum" plans STARKs, quantum resistance, simpler consensus over 3-4 years](https://www.cryptotimes.io/2026/07/05/vitalik-buterin-unveils-lean-ethereum-roadmap-for-next-era/). Significance: this is Ethereum's "third major iteration" — genuinely significant protocol plan. BUT: **3-4 year timeline = not a short-term pump catalyst.** Similar roadmap announcements (e.g., ETH 2.0) historically produced sell-the-news reactions after initial pops.

**Risk warnings (advisory):** ETH has exploit_hack advisory (UXLINK hacker 14,336 ETH transfers). This is advisory-only, does not gate routing, but adds headline uncertainty.

**ETH/BTC at 0.028:** Near multi-month lows. Two interpretations: (1) ETH structurally weak → avoid; (2) ETH/BTC mean-reversion trade opportunity → long ETH when BTC shows relative exhaustion.

**Derivatives:** Bybit cross-check not available for ETH in the top candidate list from the report (ETH not in top 8 strongest symbols in derivatives section). ETH funding shows exploit warning context.

**Chase check:**
- Catalyst already reacted to? Partially — ETH moved up on initial roadmap announcement (July 4-5). Internal data shows ETH up slightly (intraday from the report), but significantly below BTC performance.
- Overextended? No — ETH underperforming BTC (ETH/BTC 0.028) means room for catch-up.
- Actionable now? **WAIT** — need ETH to stabilize above support zone (~$1,720-1,750), UXLINK exploit news to not escalate, ETH/BTC to show stabilization.
- What would invalidate? ETH/BTC breaks below 0.027, or new major ETH exploit surfaces, or broader market sells off on FOMC July 8.

**Mood alignment:** Risk-on regime supports longs; ETH catalyst is structural bullish; ETH/BTC underperformance is a risk but also creates catch-up potential. **Partially aligned — requires more confirmation.**

**Verdict: CATALYST-WATCH (planning context).** Score 65.3 is below the "clean A/B actionable" threshold for aggressive entry. Monitor for ETH/BTC stabilization above 0.027. The catalyst is real but multi-year. Asia hours with thin liquidity → no chase. Window for entry: US open or confirmed Asia follow-through.

---

### Candidate 4 — VANRY/USDT (TRIGGERED — HIGH OI WATCH)

**Signal:** B-tier, swing (score 72.4) + intraday (66.4, triggered) + scalp (71.4, triggered). Direction: long. Status: WAITING (swing), TRIGGERED (intraday/scalp) — price has entered intraday/scalp entry zones.

**Setup (swing):** Entry pullback 0.0052-0.0054. TP1: 0.0059, TP2: 0.0063, TP3: 0.0067. Invalidation: 1h close beyond 0.0050. Support: ~0.0050.

**RS credentials:** 24h +26-30%, 7d +83%, RS vs BTC +25-28%. Volume 0.17x (below average on swing — thin).

**Derivatives — KEY WATCHPOINT:**
- OI change: **+50.52%** (highest of all active signals — very significant OI expansion)
- Funding (Bybit): −0.00042, Funding (MEXC): −0.000444 → **Negative funding across both venues**
- Negative funding = shorts paying longs (short-overcrowded OR heavy hedging pressure)
- Crowding: system rates "normal" — but the combination of OI +50% + negative funding is not typical "normal"

**Interpretation:** Large OI expansion with negative funding could mean: (a) short sellers aggressively shorted the 30% 24h move, setting up a potential short-squeeze if price continues up; OR (b) longs opened but used hedges (funding went negative due to venue dynamics). Either way, the elevated OI + negative funding warrants more monitoring.

**Chase check:**
- 7d +83% — extended but not TLM-extreme
- 24h +27-30% — significant single-day move
- Entry zone (swing): 0.0052-0.0054 = pullback of ~7-10% from 24h high implied by OI data
- Intraday/scalp already triggered → these are ENTERED or entering; swing requires deeper pullback

**Risk flags:** Volume thin (0.17x). No catalyst. High OI expansion raises risk of sharp reversal if crowd unwinds. Funding negative → monitoring position.

**Mood alignment:** Risk-on supports longs. VANRY has RS. But thin volume + extreme OI expansion without catalyst is a caution flag. **Conditional alignment.**

**Verdict: WATCH / MONITOR (not new entry now).** Intraday/scalp already triggered — those are running. For swing: wait for pullback to 0.0052-0.0054 with volume stabilization and OI settling (not continuing to expand rapidly). If OI expansion stops and funding normalizes slightly, the swing entry becomes cleaner.

---

### Candidate 5 — AIGENSYN/USDT (WATCHLIST — THIN/MEXC CONCERN)

**Signal:** B-tier, swing (68.4) + intraday (66.3) + scalp (67.4). Direction: long. Status: WAITING (all three modes).

**Setup:** Intraday entry: pullback 0.0290-0.0293. Current price: ~0.0294 (intraday report, 04:12). Support: 0.0277. Resistance: 0.0382. ATR: 0.0007. TP1: 0.0301. RS vs BTC: +7.4-8.4%.

**Consistency:** AIGENSYN has appeared in RS top-5 across scalp, intraday, and swing reports this cycle and the prior cycle. Consistent RS leadership.

**Concerns:** (1) Volume: 0.01-0.1x across modes — **very thin liquidity**. (2) MEXC-only listing (skipped on Bybit: "AIGENSYN/USDT skipped on bybit: not listed") → cap at 70 (65 for weak structure) per system rules. (3) Funding negative (Bybit: −0.00411, MEXC: −0.001878) and crowding "unknown" (insufficient OI data from cross-venue). (4) No catalyst verified. (5) Name suggests an AI narrative play but not in the ai_narrative basket.

**Mood alignment:** RS leader in risk-on environment. But thin liquidity makes it unsuitable for any significant size. **Watchlist only.**

**Verdict: WATCHLIST / RESEARCH only.** Suitable for small paper observation. Not a priority for capital allocation given thin liquidity and MEXC-only exposure.

---

## 8. Best Candidates Ranked

**Note on "no-trade" rule:** Per PART 9, there is no blanket no-trade verdict. The regime is risk-on; we route, not stop.

| Rank | Symbol | Mode | Score | Why | Status |
|---|---|---|---|---|---|
| 1 | **PUMP/USDT** | swing | 75.6 | Best RR, RS, volume (1.17x), not extended, clean pullback structure | WAIT for 0.0016 pullback |
| 2 | **ETH/USDT** | swing | 65.3 | Real catalyst (Lean Ethereum, July 4), ETH/BTC mean-reversion potential | WAIT for $1,720-1,750 confirmation |
| 3 | **VANRY/USDT** | swing | 72.4 | Strong RS, OI expansion (needs monitoring), swing still waiting | WATCH OI dynamics |
| 4 | **AIGENSYN/USDT** | swing | 68.4 | Consistent RS but thin/MEXC-only | WATCHLIST |
| 5 | **TLM/USDT** | swing | 72.4 | Score high but contradicted by delisting risk + leveraged pump | **AVOID new entry** |

**Best long-watch:** PUMP/USDT — trigger: pullback to 0.0016 with BTC structure intact and volume on pullback not accelerating downward.
**Best short-watch:** No clean short. Trigger: BTC 1h close below $61,000 OR TLM fails retest post any Binance delist announcement.
**Best catalyst-watch:** ETH/USDT — trigger: ETH/BTC holds above 0.027; pullback to $1,720-1,750 (estimated swing entry zone) absorbed; no new exploit headlines in 24h.

---

## 9. Avoid / No Trade (this decision window only)

**This window only — not a system stop. Scanning continues.**

- **TLM/USDT new entries** — Binance delisting monitoring + externally confirmed leveraged pump + extreme extension (+284%/7d). Existing triggered intraday/scalp may run to TP; no new positions.
- **Scalp mode** — 1W/7L historically (14d data). Low-confidence. Data collection mode only.
- **Intraday (no-catalyst)** — WR=23%, PF=0.70, −3R on no-news cut. Only actionable with RS-leader + breakout confirmation.
- **US stocks** — all C-tier, market closed until 16:30 EEST. Not Telegram-actionable; planning/watchlist context only.
- **SOL/ETH/APT new entries without exploit check** — operator review advisory active for all three. Always check for new exploit headlines before entry.
- **Any chase entry** — Low ATR compression environment; wait for pullback structure.

---

## 10. Main Risks

1. **FOMC minutes July 8** — Call-heavy options positioning around $63K BTC. If minutes are more hawkish than expected, the delayed-hike narrative breaks → risk-off rotation → BTC potential dump to $58-60K zone. **Check this before any new positions Tuesday.**
2. **TLM Binance delist announcement** — No date set, but active monitoring. Any formal announcement = immediate sharp downside (−50-80%). TLM intraday/scalp already triggered signals are exposed.
3. **ETH exploit escalation** — UXLINK hacker 14,336 ETH in motion. If funds hit major exchanges or cause market disruption → ETH-specific selloff risk.
4. **Low ATR / Compression environment** — 10-11th percentile. Scalp mode structurally ineffective. Breakout moves tend to be fast and revert. Do not chase any initial spike without retest confirmation.
5. **Thin liquidity — Asia overnight** — Low volume environment (0.01-0.17x volume ratios on most candidates except PUMP). Price can gap; spread risk elevated. Prefer limit orders at defined zones.
6. **Stocks C-tier performance** — A/B stocks: PF=0.33, WR=3.1%. If any C-tier stock signal looks interesting at US open, remember: these are research/watchlist only, not Telegram-actionable.
7. **Fee-sensitive edge** — 307 paper BE trades become losses with standard Bybit fees. The edge exists but is narrow. Over-trading or scalping compounds fee drag.
8. **All-long positioning** — No shorts active in the system. If regime flips suddenly (flash crash, major exploit), no hedge protection from the signal set.

---

## 11. Action Plan — Next 4 Hours (04:39 → 08:39 EEST)

1. **PUMP/USDT swing:** Monitor for pullback to 0.0016 zone. Do NOT chase 0.0017. If pullback occurs with BTC stable and no new headline, this is the cleanest entry in the current set. Check volume on pullback (should slow, not accelerate = support hold).
2. **TLM/USDT:** Do NOT add new positions. Monitor existing triggered intraday/scalp for TP hits. Watch for any Binance announcement on delisting status.
3. **ETH/USDT:** Monitor ETH/BTC ratio above 0.027. Note: Asia hours are thin for ETH — wait for London/EU session confirmation. If ETH pulls back to $1,720-1,750 and holds, reassess swing entry.
4. **VANRY/USDT:** Existing triggered intraday/scalp running. For swing: wait for deeper pullback to 0.0052-0.0054 zone with OI expansion rate normalizing. Watch funding to see if it stays negative (short-squeeze fuel) or normalizes (crowding unwinding).
5. **FOMC prep:** Before July 8 (Tuesday, 2 days). Be aware that call-heavy options positioning around $63K creates gamma risk on both sides. Reduce new position size if entering near $63K; a squeeze above $63K is possible but not guaranteed.
6. **US open readiness:** At 16:30 EEST, stocks market opens. All current stocks signals are C-tier (not actionable). Only re-evaluate if fresh stocks A/B signals emerge from weekday intraday scan at that time.
7. **Monitor:** Exploit news for ETH/SOL/APT. Any new headline changes the advisory status.

---

## 12. Final Verdict per Mode

| Mode | Asset | Verdict | Notes |
|---|---|---|---|
| Swing (crypto) | PUMP/USDT | WATCH — wait for 0.0016 pullback | Strongest setup; swing PF=3.55 |
| Swing (crypto) | VANRY/USDT | WATCH — triggered intraday; swing deeper pullback | OI expansion monitoring |
| Swing (crypto) | ETH/USDT | CATALYST-WATCH — planning context | Lean Ethereum confirmed; wait for support hold |
| Swing (crypto) | TLM/USDT | AVOID new entry | Delisting monitoring + leveraged pump |
| Intraday (crypto) | No-catalyst | NO-ENTRY (current window) | WR=23%, PF=0.70 on no-news cut |
| Intraday (crypto) | Catalyst-backed | MANUAL REVIEW REQUIRED | ETH/SOL/APT advisory; check per entry |
| Scalp (crypto) | — | DATA COLLECTION ONLY | 1W/7L historically; low confidence |
| Intraday (stocks) | All C-tier | PLANNING/WATCHLIST only | Market closed; US opens 16:30 EEST |
| Intraday (stocks) | UNH | AVOID — LEGAL/HEADLINE RISK | DOJ fraud probe confirmed (−16%) |
| Shadow (stocks) | AAPL | SHADOW ONLY — planning | reclaim_after_shakeout score=77; not paper-actionable |

---

## 13. Sources

External sources cited in this review (WebSearch, verified):

- [TLM Rockets 55% on Leveraged Contracts and Alien Worlds Tournament Amid Broader Crypto Rally](https://www.interactivecrypto.com/tlm-rockets-55-on-leveraged-contracts-and-alien-worlds-tournament-amid-broader-crypto-rally-jul) — interactivecrypto.com, July 2026
- [Vitalik Buterin Unveils Lean Ethereum Roadmap for Next Era](https://www.cryptotimes.io/2026/07/05/vitalik-buterin-unveils-lean-ethereum-roadmap-for-next-era/) — cryptotimes.io, 2026-07-05
- [Vitalik's Lean Ethereum Roadmap Draws Pushback on Its Timeline](https://beincrypto.com/vitalik-lean-ethereum-roadmap-starks-quantum/) — beincrypto.com, July 2026
- [BTC price news: Bitcoin zooms above $61,000 as inflation fears soften](https://www.coindesk.com/markets/2026/07/02/bitcoin-zooms-above-usd61-000-as-inflation-fears-soften) — CoinDesk, 2026-07-02
- [Latest Alien Worlds News — TLM Binance monitoring status](https://coinmarketcap.com/cmc-ai/alien-worlds/latest-updates/) — CoinMarketCap, July 2026

Internal sources (not cited externally):
- `data/reports/scalp/2026-07-06_01-06_scalp_report.md` (04:06 EEST)
- `data/reports/intraday/2026-07-06_01-12_intraday_report.md` (04:12 EEST)
- `data/reports/swing/2026-07-06_01-27_swing_report.md` (04:28 EEST)
- `data/catalysts/2026-07-06/catalyst_cycle_01-12.md` (04:12 EEST)
- `data/scheduled_runs/2026-07-05_default_schedule/cycle_11_03-58_summary.md` (04:31 EEST)

---

## 14. Fix Requests / TODO

### TODO-untracked-regression-resolution
- **issue:** Untracked legacy alerts were 23 on Sunday July 5 (persistent PART-1 regression flagged in previous reviews); cycle 11 shows 0 untracked. Cannot confirm whether this is a genuine fix or just a cycle-boundary artifact (fresh weekday cycle starting from scratch). Needs monitoring across next 2-3 cycles to confirm resolution.
- **evidence:** Previous review (23:22) logged 23 untracked (ETHFI/ADA/BCH/VANRY/HOT/AIGENSYN/SENT/CAP, 08:27–20:13 UTC). Cycle 11 detector: "None. Every legacy crypto alert has a backing proposed_signal."
- **suggested manual fix:** Run `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-05` in next session to check if Sunday's 23 alerts are genuinely resolved or newly orphaned. Investigate if the detector resets on weekday-mode transition.
- **priority:** medium
- **first observed:** 2026-07-05 23:22 EEST (regression); apparent resolution 2026-07-06 04:39 EEST

### TODO-catalyst-mapping-12-high-importance
- **issue:** 12 high-importance symbol-tagged catalysts not mapped into catalyst_events in cycle 11: AMZN, ARB, AXP, BAC, BNB, HYPE, MKR, MS, SMH, SPY. This is a recurring gap — BNB and MKR are crypto-native and likely have on-chain relevance that the catalyst layer misses.
- **evidence:** cycle_11_03-58_summary.md step 5 catalyst integrity scan: "WARNING: 12 high-importance symbol-tagged catalysts not mapped into catalyst_events: AMZN, ARB, AXP, BAC, BNB, HYPE, MKR, MS, SMH, SPY"
- **suggested manual fix:** Audit symbol resolver in catalyst layer for BNB, HYPE, MKR — these are crypto native and should map directly. Stocks (AMZN, AXP, BAC, MS, SMH, SPY) may be intentionally excluded from catalyst_events if crypto-pair not present; confirm whether that exclusion is intentional design.
- **priority:** low
- **first observed:** 2026-07-06 04:39 EEST
