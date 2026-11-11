# Opus Enriched Review — post-close final daily review — Auto Cycle 23:15 EEST

_Generated 2026-06-20 23:15 EEST (Saturday, weekend crypto-only mode). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

> **CATALYST MAPPING CRITICALLY LOW: ~21.6% (prior review baseline; new cycle did not raise materially). Use catalyst layer as CONTEXT ONLY, not final decision basis.**
>
> **REGIME: BTC range/chop ~$63,609. ETH transition_up ~$1,727. Breadth 48.7% EMA20. Shorts ONLY profitable direction (PF 1.77). Longs systemically losing (PF 0.54).**
>
> **KEY FLAG: SYN/USDT — B-tier swing TRIGGERED but AVOID from prior review (Bitget delisted June 18, no verified catalyst, pure speculation). MANUAL REVIEW REQUIRED.**
>
> **POST-CLOSE OUTCOME: +3R improvement during US session close (Total R –40 → –37). Multiple TP1 hits. Day net negative (longs drag) but US close modestly constructive.**

---

## 1. Executive Summary

**Sat 2026-06-20, 23:15 EEST — post-close final daily review — advisory only / no auto-trade.**

- Slot type: **post_close** (23:15 EEST). Stocks closed (weekend Saturday). Crypto-only live class.
- Scheduler fresh (cycle_02 finished 22:51 EEST, 24 min ago; steps ok=16, failed=0). Data quality: OK.
- BTC confirmed $63,609–$63,676 (external, range/chop). ETH transition_up ~$1,727. Weekend mode ACTIVE.
- **Catalyst mapping critically low** (prior review: 21.6%; current cycle same pattern — flag maintained; use as context only).
- US session close recap: BTC drifted in range/chop, no directional break. Net effect ~flat vs. late-session read.
- Performance: Week Total R –37R (PF 0.58, WR 10%). **Today's session improved from –40R (21:41) to –37R (+3R)** via TP1 hits across AXS scalp, MET intraday/swing, XLM swing short, SOL, and others.
- Active signals: **22** (all B-tier). OPEN ACTIONABLE: 4 (SAND scalp, BEL swing, AXS swing, SYN swing). WAITING for entry: 1 (NEAR short). TP1 REACHED / ENTERED UNRESOLVED: ~17.
- **SYN is TRIGGERED (swing B-tier) but previous review flagged AVOID. Manual review needed.**
- Overnight / Asia setup: NEAR short WAITING = cleanest candidate. SOL watch (TP1 hit, wait for pullback to $70.44–$70.73). Avoid: BICO, ALICE, SYN (extended/no-catalyst).
- Head trader verdict: **CAUTION / SHORTS PREFERRED.** Route catalyst-backed long SOL on retest. NEAR short on trigger. No new long for extended no-catalyst names.

---

## 2. Data Used

| Source | File / Tool | mtime EEST | Freshness |
|---|---|---|---|
| Scheduler log | `scheduler.log` | 22:51 | 24 min — FRESH |
| Latest cycle | `cycle_02_21-41_summary.md` | 22:51 | 24 min — FRESH |
| Scalp report | `2026-06-20_19-14_scalp_report.md` | 22:13 | 62 min — FRESH (<4h) |
| Intraday report | `2026-06-20_19-44_intraday_report.md` | 22:44 | 31 min — FRESH (<4h) |
| Swing report | `2026-06-20_13-30_swing_report.md` | 16:30 | 6h45m — CARRY-FORWARD (4–12h) |
| Stocks intraday | `2026-06-19_19-53_stocks_intraday_report.md` | yesterday | STALE (>24h — weekend expected) |
| Stocks swing | `2026-06-19_13-54_stocks_swing_report.md` | yesterday | STALE (>24h — weekend expected) |
| Catalyst events | `data/catalysts/2026-06-20/catalyst_events.jsonl` | 22:45 | 751 events; mapping critically low |
| Catalyst cycle | `catalyst_cycle_19-45.md` | 22:45 | 389 events in latest cycle |
| LLM packet | `data/processed/llm_analysis_packet.md` | 22:44 | Fresh (generated end of cycle_02) |
| Active signals | `active-signals --asset-class crypto` | 23:15 live | 22 signals |
| Signal stats | `signal-stats --asset-class crypto` | 23:15 live | 258 sample (B-tier dominant) |
| Untracked alerts | `detect_untracked_legacy_alerts --since 2026-06-20` | 23:15 | 0 untracked — clean |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_2141.md` | 22:00 | Previous slot (21:41 EEST) |
| External: BTC price | MetaMask / CoinDesk (WebSearch) | 2026-06-20 | $63,609–$63,676 confirmed |
| External: BTC macro | CryptoBriefing / Intellectia (WebFetch) | 2026-06 | $64K break + $1.1B liquidations |
| External: SYN | Invezz search snippet (June 18, 2026) | 2026-06-18 | No fundamental catalyst confirmed; URL 403 blocked |
| External: BICO | WebSearch | 2026-06-20 | No specific catalyst found |
| External: ALICE | WebSearch / MEXC prediction | 2026-06-20 | No confirmed pump catalyst |

**External web research**: Available. BTC/SYN/BICO/ALICE searched. All claims cited. No fabricated data.

**Blindspots**: Reddit 403 blocked (crowd sentiment missing), on-chain config absent (`config/onchain.yaml`), liquidation heatmaps not connected, Bybit OHLCV degraded (40 failures in swing), live KOL feeds not automated.

---

## 3. Scheduler / Data Freshness

- `scheduler.log` last write: **22:51 EEST** (24 min ago) — FRESH
- `cycle_02_21-41_summary.md` finished: **22:51 EEST** (24 min ago) — FRESH
- Cycle 02 steps: **ok=16, failed=0** — clean run
- Track-signals pre-pass: checked=404, **tp_hits=270**, stopped=0, expired=0 — anomaly flagged (see §14 TODO-TP-TRACKING)
- Weekend mode: **ACTIVE** (Saturday, A-tier margin penalty, chasing demotes to C, weak signals cap at B)
- Bybit OHLCV: degraded (swing report: 40 failed fetches) — derivatives confirmation weakened for swing
- Social sources: Reddit × 3 all failed (403/timeout) — crowd context missing
- Stocks: no reports generated today (expected for Saturday)
- LLM packet confirmed weekend mode active: A-tier penalty +5 pts, overextension multiplier 1.25×
- Untracked legacy alerts: **0** — pipeline healthy

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-06-20 23:15 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "catalyst_missing", "derivatives_sparse", "onchain_config_missing"],
      "data_missing": ["on-chain config (config/onchain.yaml)", "live social attention", "Bybit OHLCV partial", "liquidation heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_02 ok=16 failed=0 22:51", "Reddit 403 all 3 sources", "Bybit OHLCV 40 swing failures", "catalyst mapping ~21.6% per prior review baseline"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["chop", "mixed", "shorts_preferred"],
      "data_missing": ["live KOL/Telegram sentiment", "on-chain flows", "ETF flow data"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC trend range/chop $63,609", "ETH transition_up ~$1,727", "breadth 48.7% EMA20", "macro risk 31/100", "shorts PF 1.77 vs longs PF 0.54", "week Total R -37R"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.60,
      "reason_codes": ["stale_catalyst", "no_catalyst", "mapping_weak", "narrative_supported"],
      "data_missing": ["verified catalyst for BICO/ALICE/SYN", "SOL bitFlyer confirmation freshness (carry-forward)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["751 events today 4 baskets mapping ~21.6%", "no verified catalyst for BICO/ALICE/SYN (web search confirmed)", "ai_narrative basket active (NEAR/RENDER/TAO/FET)", "momentum_breakout: ALICE primary now", "Axelar $4.7M exploit basket"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "post_unwind_chop", "funding_extreme", "data_unavailable"],
      "data_missing": ["Bybit OI for several names", "liquidation cluster data", "on-chain flow"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALICE OI +124.87% funding -0.00249 long/short 2.298 crowding unknown", "BICO OI +13.6% funding -0.00220 crowding unknown", "SYN OI -17% short covering only", "NEAR price/OI down deleveraging", "SOL OI +1.6% funding neutral crowding normal"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["chase_risk", "entry_late", "clean_retest", "stale_before_entry"],
      "data_missing": ["live 1m/5m chart for intraday confirmation", "TradingView MCP not loaded"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALICE/BICO both >2ATR from EMA20 (rejected)", "SYN price 0.1543 above entry zone 0.1439-0.1504 (late entry)", "NEAR short WAITING zone clean failed bounce", "SOL TP1 reached retest zone $70.44-70.73", "AXS swing triggered at 1.1-1.14 (current ~1.151)"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "needs_review",
      "confidence": 0.80,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": ["paper monitor cycle_02 file (only cycle_01 data from prior review)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["22 active signals CLI 23:15", "4 OPEN actionable (SAND scalp BEL swing AXS swing SYN swing)", "1 WAITING (NEAR short)", "~17 TP1 REACHED / ENTERED UNRESOLVED", "SYN swing triggered vs AVOID flag - discrepancy needs manual review", "0 untracked alerts — pipeline healthy"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["repeated_losses", "correlation_cluster", "manual_review", "reduce_risk"],
      "data_missing": ["on-chain config for leverage/flow data"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Week longs PF 0.54 / -40R systemically losing", "shorts PF 1.77 only profitable direction", "weekend mode active wider wicks", "SYN triggered vs AVOID = manual review needed", "BICO/ALICE extended no entry", "Axelar exploit $4.7M cross-chain risk", "tp_hits=270 vs wins=25 tracking anomaly"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.70,
      "reason_codes": ["playbook_failing", "playbook_working", "missed_winner"],
      "data_missing": ["today-only outcome data (week aggregate only)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scalp n=115 triggered / 1 win / 13 losses", "intraday n=59 / 17 wins / 33 losses PF ~0.93", "swing n=82 / 7 wins / 40 losses PF 0.43", "shorts n=17 PF 1.77 only working bucket", "Today US close +3R improvement (Total R -40 to -37)", "multiple TP1 hits confirmed"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["shorts_preferred", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["All 8 agents: data_quality=caution, market_regime=chop, catalyst_narrative=caution, derivatives=caution, technical=caution, lifecycle=needs_review, risk_manager=caution, playbook=caution"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.75,
    "preferred_side": "shorts",
    "best_long_candidate": {
      "symbol": "SOL/USDT",
      "trigger": "pullback into $70.44-$70.73 + 15m acceptance; do NOT chase above zone",
      "reason": "bitFlyer listing June 24 (carry-forward catalyst); TP1 reached; cleanest catalyst-backed name; wait for retest"
    },
    "best_short_candidate": {
      "symbol": "NEAR/USDT",
      "trigger": "price enters WAITING zone (2.xxx per system) + 1h close below local structure",
      "reason": "B-tier swing short WAITING; clean deleveraging structure (price/OI down); best pure short in current lineup"
    },
    "best_catalyst_candidate": {
      "symbol": "SOL/USDT",
      "trigger": "retest of $70.44-$70.73 + 15m acceptance",
      "reason": "bitFlyer June 24 listing is the cleanest verified catalyst; TP1 confirmed playbook active"
    },
    "avoid_candidate": {
      "symbol": "SYN/USDT",
      "reason": "B-tier swing TRIGGERED but Bitget delisted June 18, no verified fundamental catalyst, pure momentum; requires manual session to resolve active signal discrepancy"
    },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, catalyst_missing, derivatives_sparse, onchain_config_missing | advisory_only |
| market_regime | caution | 0.80 | chop, mixed, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | stale_catalyst, no_catalyst (BICO/ALICE/SYN), mapping_weak, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.65 | squeeze_risk (ALICE/BICO), oi_contradicts (SYN), post_unwind_chop, funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.70 | chase_risk (ALICE/BICO), entry_late (SYN), clean_retest (NEAR), stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.80 | open_actionable (4), waiting_for_entry (1), needs_review (SYN vs AVOID) | advisory_only |
| risk_manager | caution | 0.75 | repeated_losses (longs), correlation_cluster, manual_review (SYN), reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing (scalp/swing longs), playbook_working (shorts), missed_winner (SOL) | advisory_only |
| head_trader | caution | 0.75 | shorts_preferred, wait_for_trigger, manual_review | advisory_only |

---

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_2141.md` (21:41 EEST, late-session risk review).

| Item | Previous (21:41) | Now (23:15) | Change |
|---|---|---|---|
| Scheduler | cycle_01 19:41 (2h old) | cycle_02 22:51 (24 min) | UPGRADED — fresh cycle |
| Scalp report | 16:24 (5h old) | 22:13 (62 min) | UPGRADED — fresh |
| Intraday report | 16:39 (5h old) | 22:44 (31 min) | UPGRADED — fresh |
| BTC price | ~$63,676 | $63,609–$63,676 | UNCHANGED — range/chop confirmed |
| ETH regime | uptrend | transition_up | ESSENTIALLY UNCHANGED |
| Active signals | 23 | 22 | –1 signal (one closed/expired) |
| Total R | –40R | –37R | +3R IMPROVEMENT via TP1 hits |
| Wins | 24 | 25 | +1 confirmed win |
| momentum_breakout primary | BEL/USDT | ALICE/USDT | ROTATED — ALICE took over |
| SYN thesis | AVOID flagged | Still TRIGGERED, still no catalyst | CONCERN PERSISTS |
| SOL status | B-tier WAITING ($71.43 > zone) | TP1 REACHED | UPGRADED |
| NEAR short | WAITING | Still WAITING | UNCHANGED — best overnight |
| Catalyst mapping | 21.6% CRITICALLY LOW | Same pattern | UNCHANGED |
| Untracked alerts | 0 | 0 | CONFIRMED clean |

**New this cycle**: cycle_02 ok=16 clean; ALICE promoted to momentum_breakout primary; ~17 TP1 signals detected; tp_hits=270 tracking anomaly newly observed.

**Confirmed from prior**: SYN AVOID (no catalyst externally); shorts PF 1.77 only profitable direction; catalyst mapping poor.

**Invalidated**: BTC/ETH swing regime (downtrend in 13:30 swing) superseded by fresh intraday (range/chop + transition_up ETH).

---

## 5. Catalyst Coverage

- **Events today**: 751 (catalyst_events.jsonl updated 22:45 EEST)
- **Latest cycle (19-45)**: 389 events scanned; 3 baskets
- **Mapping**: ~21.6% from prior review baseline. Current cycle distribution consistent — majority events are `(basket)` / null symbol. **Unmapped > 50%: YES.**
- **⚠️ catalyst mapping critically low — use catalyst layer as context only, not final decision basis.**
- **Active baskets (4)**:
  - `delisting_thin_liquidity` — avoid low-liquidity plays (fan tokens, World Cup prediction markets)
  - `rwa_narrative` — related beta rotation; primary: ONDO/USDT, XLM/USDT
  - `ai_narrative` — related beta rotation; primary: NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT
  - `momentum_breakout` — wait for pullback; primary: ALICE/USDT (+47% 24h, vol 1.70x); no confirmed catalyst
- **Top 3 unmapped headlines (context only)**:
  1. World Cup 2026 prediction markets dwarfing fan token trading (Netherlands vs Sweden)
  2. How Premier League transfer drama is moving crypto fan token markets
  3. ICE Compass for trade analytics unveiled (sector product launch)
- **Legal/regulatory**:
  - SMCI indictment (SEC EDGAR FY2026 8-K) — stocks only; AVOID
  - UNH DOJ probe — stocks only; AVOID
  - Sporting goods chain Chapter 11 — retail basket; not crypto-direct
- **Crypto-specific hack**: Axelar Secret Network bridge — $4.7M stolen. Mapped as `(basket)`. Potential cross-chain sentiment dampener; no specific crypto symbol directly affected in current candidates.
- **Regulatory positive**: WhiteBIT EU MiCA license (Austria). CLARITY Act debate (mixed).

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood**: chop / range — BTC $63,609 range/chop; ETH transition_up ~$1,727; breadth 48.7% EMA20 (neutral)
- **Stocks mood**: closed (weekend Saturday) — carry-forward only
- **Dominant narrative**: Range consolidation post-$64K liquidation event. AI basket active (NEAR/TAO/RENDER/FET). Gaming/metaverse names (AXS/ALICE/SAND/BEL) momentum-only with no verified catalyst. SOL tokenized-equity + bitFlyer listing narrative = most credible catalyst today.
- **Preferred side now**: **shorts + catalyst-backed longs only.** No new naked long on extended no-catalyst names.
- **Best long candidate**: SOL/USDT — trigger: pullback to $70.44–$70.73 + 15m acceptance. Do NOT chase.
- **Best short candidate**: NEAR/USDT — trigger: WAITING entry zone (2.xxx) + 1h close below structure.
- **Best catalyst-backed candidate**: SOL/USDT (bitFlyer June 24). AI basket names (NEAR/TAO/FET) if pullback available.
- **What to avoid**: SYN (MANUAL REVIEW), BICO (>2ATR no catalyst), ALICE (>2ATR momentum-only), BEL/AXS (triggered, monitor invalidation closely).
- **What would change the view**: BTC break above $66–67K with volume = breadth expansion, longs viable. BTC break below $61K = risk-off, shorts accelerate. ETH loses uptrend = reduce all long exposure.

### US Session Close Assessment (post-close slot focus)

BTC closed Saturday's effective US session at ~$63,600. No directional break achieved. Session characterized by:
- **What worked today**: TP1 hits on AXS scalp, MET intraday (both L and S variants), MET swing short, XLM swing short, SOL, WLD, and ~10 others → +3R net since 21:41 review
- **What didn't work**: Long attrition continuing (longs PF 0.54); SYN triggered despite AVOID recommendation; scalp mode severely underperforming (1 win / 108 triggered)
- **Shorts**: XLM swing short hit TP1; MET swing short hit TP1 — short playbook confirmed working
- **Net daily view**: Today was modestly constructive for active positions (TP hits) but the week remains deeply negative (–37R). The improvement is directionally right but insufficient to change the regime verdict.

---

## 7. Candidate Deep Dives

### Candidate 1: SYN/USDT — B-tier swing TRIGGERED vs AVOID contradiction

**Status**: OPEN ACTIONABLE (triggered, swing long). **⚠️ NEEDS MANUAL REVIEW.**
**Score**: 65.6/100 (swing, from 16:30 report). **Tier**: B. **Direction**: long. **Weekend flag**: Y.
**Current price**: ~$0.1543. Entry zone (swing): $0.1439–$0.1504. **Price is ABOVE entry zone** → entry triggered at market.
**Invalidation**: 1h close < $0.1359. **TP1**: $0.1678. **TP2**: $0.1822. **TP3**: $0.1967.

**External research**: Invezz (2026-06-18) describes SYN up ~108%/24h and ~327%/7d as of June 18. No specific fundamental catalyst named in search snippet. URL returned 403 on WebFetch — cannot verify deeper content. Prior review confirmed via multiple sources: Bitget **delisted SYN June 18** (bearish). OI declining (–17% 24h) = short covering only, not fresh long positioning.

**Has price reacted to catalyst?** N/A — no verified catalyst exists.
**Is setup chasing?** YES — price is above entry zone; entry was market-order triggered.
**Retest structure?** NO — entered on breakout, not retest.
**Overextended?** 7d +382% (scalp), OI declining → extended and deteriorating structure.
**Mood alignment?** AGAINST — chop regime, no catalyst, declining OI, late entry.
**Verdict**: **MANUAL REVIEW REQUIRED / AVOID for new entry.** Existing triggered signal must be assessed in a manual session — either accept the existing TP/SL framework and hold, or manually flag for close. Do NOT add, do NOT chase. No auto-trade action this session.

---

### Candidate 2: NEAR/USDT — best short, WAITING for entry

**Status**: WAITING for entry (B-tier swing short). **Weekend flag**: Y.
**Entry zone**: system-defined WAITING zone (failed bounce/retest structure per swing report, price around 2.xxx area).
**Direction**: short. **Invalidation**: 1h close above swing high.

**Internal news check**: NEAR is in `ai_narrative` basket (primary). AI narrative is active but price is in downtrend — AI basket attention has not translated to NEAR price leadership. From scalp rejected list: NEAR had squeeze risk in short-scalp context, but swing short has cleaner structure.

**Derivative check**: Active signals show NEAR B swing short is WAITING — this is the cleaner, structural variant. Intraday/scalp NEAR rejected due to squeeze risk; swing short is the actionable route.

**Chase check**: WAITING = NOT chasing. Entry triggers only if price comes back to zone.

**Mood alignment**: YES — NEAR short aligns with preferred side (shorts in chop/range).

**Overnight/Asia watch**: NEAR short is the **cleanest overnight candidate** entering Asia. AI narrative may try to push NEAR, which would bring price to the retest zone naturally.

**Verdict**: **WAIT FOR ENTRY. Best overnight short.** If price enters zone overnight with 1h confirmation: actionable. Risk: AI narrative asserting → keep invalidation tight above swing high.

---

### Candidate 3: SOL/USDT — catalyst-backed, TP1 hit

**Status**: ENTERED UNRESOLVED (TP1 reached, tracking TP2). B-tier swing long.
**TP1**: $71.51 (swing report). **TP2**: $72.17. **TP3**: $72.82.
**Current price**: ~$70.86 (intraday report, ~30min old) — has likely touched TP1 territory.

**Catalyst (carry-forward)**: bitFlyer (Japan) listing June 24. Confirmed in prior review via external search. SOL also part of tokenized equity narrative. Whale buy $16.55M at $70.5 (~15h stale from swing report, but bitFlyer listing is the durable catalyst).

**TP1 reached**: Per active signals CLI, SOL shows "tp" status — TP1 has been touched. Paper trade partially resolved.

**Do NOT chase**: Entry zone was $70.44–$70.73. With TP1 hit, ideal retest would be a pullback to that zone before Asia session. If Asia opens with BTC stable, SOL may consolidate near $70.5–$71 before bitFlyer listing date.

**Derivative check**: SOL OI +1.6%, funding –0.0000648, crowding normal — clean positioning, not crowded.

**Verdict**: **ENTERED UNRESOLVED (TP1 hit). Watch TP2 ($72.17) or retest. Do NOT chase above $71.5. Best catalyst-backed name overnight.**

---

### Candidate 4: BICO/USDT — extreme move, no catalyst, integrity check

**Status**: WATCHLIST ONLY / REJECTED (>2ATR from EMA20).
**24h return**: +79–80%. **7d return**: +119%. **Score**: 36–60/100 (too extended).

**Catalyst search**: WebSearch returned only price prediction content — no verified fundamental catalyst for BICO in June 2026. System placed BICO in `momentum_breakout` basket in earlier swing cycles. No announcement confirmed.

**Derivative check**: OI up +13–18%, funding –0.002+ (very negative = expensive for longs), crowding unknown. Negative funding signals longs are paying shorts — unsustainable if momentum fades.

**Chase check**: >2ATR from EMA20 — correctly rejected. Pullback zone from swing: $0.0382–$0.0403.

**Axelar connection**: Biconomy (BICO) = ERC-4337 / account abstraction. Axelar = cross-chain bridge. Different protocol, not directly affected by Axelar exploit.

**Verdict**: **AVOID / NO NEW ENTRY.** Pullback to $0.038–$0.040 zone with verified catalyst would be the entry condition. Currently: no catalyst, extended, funding extreme negative. Do not chase.

---

### Candidate 5: ALICE/USDT — momentum_breakout primary, no catalyst

**Status**: WATCHLIST ONLY / REJECTED (>2ATR from EMA20). momentum_breakout basket primary.
**24h return**: +47% (intraday report). **Score**: 42–95/100 by mode (rejected due to extension in live modes).

**Catalyst search**: MEXC price prediction ($0.13348 for June 20) consistent with current ~$0.1361 — price in predicted range but that's coincidence, not catalyst. No specific pump catalyst identified in any source.

**Crowd attention**: attention 10/100, momentum 95/100, crowding 60/100 — high momentum, very low organic attention (no crowd driving this). Stage unknown.

**Derivative check**: ALICE OI +124.87%, funding –0.00249, long/short 2.298 — **ELEVATED SQUEEZE RISK**. If momentum fades, violent reversal possible. Crowding "unknown" (insufficient data) adds risk.

**Chase check**: >2ATR from EMA20 — rejected. Pullback zone (intraday): $0.1292–$0.1340.

**Verdict**: **WATCHLIST ONLY.** Entry only if: (1) verified catalyst emerges, (2) price pulls back to $0.129–$0.134 zone, (3) 15m acceptance, (4) squeeze risk cleared. Currently: no catalyst, extended, elevated crowding risk. Do NOT enter.

---

## 8. Best Candidates Ranked

No A/B candidates are clean for new entries right now. Routing by trigger:

| Rank | Symbol | Direction | Setup | Trigger | Lifecycle Status |
|---|---|---|---|---|---|
| 1 | **NEAR/USDT** | Short | B-tier swing | Enter WAITING zone (2.xxx) + 1h confirmation | WAITING FOR ENTRY |
| 2 | **SOL/USDT** | Long (catalyst) | B-tier swing | Pullback to $70.44–$70.73 + 15m acceptance | ENTERED UNRESOLVED (TP1 hit) |
| 3 | **BICO/USDT** | Long (catalyst-required) | Watchlist | Pullback to $0.038–$0.040 + verified catalyst | WATCH ONLY |
| 4 | **ALICE/USDT** | Long (catalyst-required) | Watchlist | Pullback to $0.129–$0.134 + verified catalyst + squeeze cleared | WATCH ONLY |
| 5 | **JTO/USDT** | Short (watchlist) | Watchlist (squeeze-risk capped) | Failed bounce + squeeze risk cleared + thin liquidity warning passed | WATCH ONLY |

- **Best long-watch**: SOL/USDT — trigger: retest $70.44–$70.73 + bitFlyer June 24 catalyst live
- **Best short-watch**: NEAR/USDT — trigger: enter WAITING zone 2.xxx + 1h close below structure
- **Best catalyst-watch**: SOL/USDT (bitFlyer June 24 listing)
- **Avoid for new entry**: SYN (triggered but AVOID — manual review), BICO (extended), ALICE (extended + squeeze risk)

---

## 9. Avoid / No Trade (this decision window only)

- **SYN/USDT**: DO NOT add or chase. Active signal exists but contradicts AVOID recommendation. Requires manual session to resolve.
- **BICO/USDT**: Extended >2ATR, no catalyst. Don't chase. Pullback zone only if catalyst emerges.
- **ALICE/USDT**: Extended >2ATR, no verified catalyst, crowding elevated, OI squeeze risk.
- **BEL/USDT**: Active swing long (triggered) but no catalyst; momentum-only; late entry risk. Monitor invalidation ($0.1425).
- **AXS/USDT**: Active swing long (triggered). No catalyst. Monitor invalidation.
- **Intraday no-catalyst longs in chop**: 14d no-news cut: WR 23% / PF 0.70 / –3R — not viable without catalyst + RS.

**Scanning continues in all moods. This is a decision-window filter only.**

---

## 10. Main Risks

1. **BTC breaks below $61K**: Risk-off accelerates. All long exposure reduces. Shorts on weak alts accelerate.
2. **SYN/USDT active signal vs AVOID conflict**: System has a triggered B-tier position in a name flagged for avoidance externally. Not resolved until manual session.
3. **TP1-hit vs confirmed-win gap**: track-signals shows tp_hits=270 but only 25 confirmed wins — tracking system may not be converting TP1 touches to outcome records reliably.
4. **Catalyst mapping < 25%**: Cannot rely on catalyst layer for conviction. Each candidate requires external research before acting.
5. **Weekend liquidity**: Thinner orderbooks, wider wicks. Weekend mode applies A-tier margin penalty. New entries: wider stops, smaller size.
6. **Axelar exploit ($4.7M)**: Cross-chain perception negative. Any cross-chain / bridge token could see sentiment spillover.
7. **Bybit OHLCV degradation**: 40 failures in swing. Derivatives confirmation weakened.
8. **BICO/ALICE squeeze risk**: ALICE OI +124%, funding extreme negative — if momentum fades, violent reversal possible.

---

## 11. Action Plan — Next 4 Hours (23:15 → 03:15 EEST, entering Asia session)

- **NEAR short**: Monitor entry zone (2.xxx). If price pulls back to zone with 1h confirmation overnight → system should capture the WAITING signal. Best overnight trade.
- **SOL**: Watch for pullback to $70.44–$70.73. If price pulls back from TP1 territory to that zone AND 15m acceptance → potential add/re-entry trigger for bitFlyer catalyst (June 24 still approaching).
- **Active longs (BEL, AXS, SAND)**: Monitor invalidation levels. If BTC drops below $62K: tighten monitoring, prepare to accept stops.
- **SYN**: Do NOT act. Flag for manual session. The active triggered signal should be reviewed — not force-closed this automated session.
- **Asia open watch**: Asia opens ~01:00–02:00 EEST (Tokyo 07:00–08:00). Watch for BTC direction shift. AI narrative (TAO/NEAR/FET) may react to Asian trading sentiment.
- **Catalyst watch overnight**: BICO, ALICE — if any announcement emerges, pull to watchlist review. Otherwise: wait.
- **Scanning**: All scanners, collectors, and monitors continue running. Do NOT disable or pause any component.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Confidence | Notes |
|---|---|---|---|
| **Scalp** | NO NEW ENTRY — watch only | Low | PF 0.08 week, 1 win / 108 triggered. Horizon mismatch. SAND scalp active but low confidence. |
| **Intraday** | CAUTION — catalyst-backed only | Medium | PF 0.93 week near break-even. 14d no-news intraday in chop: –3R. Weekend: prefer retests, not breakout chase. |
| **Swing** | CAUTION — shorts preferred; catalyst-backed only | Medium | PF 0.43 week for longs (failing). Shorts PF 1.77 (working). NEAR short = best swing idea. SOL tracking TP2. |
| **Stocks** | N/A (weekend) | — | No reports. SMCI/UNH legal risk carried forward. |
| **Overall** | CAUTION / SHORTS PREFERRED | 0.75 | Route: shorts (NEAR), catalyst-backed (SOL), avoid extended momentum (SYN/BICO/ALICE). Manual review for SYN conflict. |

---

## 13. Sources

| # | Title | Source | Date | URL | Verification |
|---|---|---|---|---|---|
| 1 | Bitcoin Price is $63,609 today | MetaMask | 2026-06-20 | metamask.io/price/bitcoin | primary_source |
| 2 | Bitcoin (BTC) price today live | CoinDesk | 2026-06-20 | coindesk.com/price/bitcoin | primary_source / $63,675.74 |
| 3 | Bitcoin falls below $64,000, triggers $1.1B in liquidations | CryptoBriefing | 2026-06 | cryptobriefing.com | single_source |
| 4 | Bitcoin Price Crash June 2026 | Intellectia AI | 2026-06 | intellectia.ai | single_source |
| 5 | Why is Synapse (SYN) price skyrocketing? | Invezz | 2026-06-18 | invezz.com | single_source — 403 blocked; no catalyst named |
| 6 | My Neighbor Alice price prediction | MEXC | 2026-06-20 | mexc.com | single_source / context only |
| 7 | Internal reports (scalp/intraday/swing) | crypto-ai-desk | 2026-06-20 | data/reports/ | primary_source |
| 8 | Internal catalyst_cycle_19-45.md | crypto-ai-desk | 2026-06-20 | data/catalysts/2026-06-20/ | primary_source |
| 9 | Internal active-signals + signal-stats CLI | crypto-ai-desk | 2026-06-20 23:15 | CLI stdout | primary_source |
| 10 | Internal cycle_02_21-41_summary.md | crypto-ai-desk | 2026-06-20 22:51 | data/scheduled_runs/ | primary_source |
| 11 | bitFlyer SOL listing June 24 (carry-forward) | Prior review §7 | 2026-06-20 | OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_2141.md | single_source (carry-forward) |

---

## 14. Fix Requests / TODO

### TODO-SYN-AVOID-CONFLICT
- **issue:** SYN/USDT B-tier swing signal TRIGGERED while this review (and prior review 21:41) recommends AVOID. Bitget delisted June 18 + no verified catalyst + OI declining = no valid long thesis, but system generated and triggered the signal.
- **evidence:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_2141.md` §7 SYN AVOID flag; active-signals CLI 23:15 SYN B swing status=triggered
- **suggested manual fix:** In a manual session, review the SYN swing signal. Check whether to manually close/invalidate it. Consider mechanism to flag signals where external research contradicts system thesis before they trigger.
- **priority:** high
- **first observed:** 2026-06-20 21:41 EEST; confirmed 23:15

### TODO-TP-TRACKING-ANOMALY
- **issue:** cycle_02 track-signals pre-pass: tp_hits=270 vs only 25 confirmed wins (signal-stats). The gap suggests TP1 "touches" are not being reliably converted to confirmed win outcomes.
- **evidence:** `cycle_02_21-41_summary.md` step 1: `tp_hits=270, stopped=0, expired=0`; signal-stats CLI: `wins=25, triggered=249`
- **suggested manual fix:** Audit tracking pass logic — clarify whether `tp_hits` counts "price currently at/past TP1 level" vs "confirmed partial close." Check `signal_outcomes` table.
- **priority:** high
- **first observed:** 2026-06-20 23:15 EEST

### TODO-BYBIT-OHLCV-DEGRADED
- **issue:** Bybit OHLCV fetches failing (40 failures in swing report). Degrades derivatives confirmation for swing candidates.
- **evidence:** `data/reports/swing/2026-06-20_13-30_swing_report.md` §0: `bybit: role=derivatives, ohlcv_fetched=0, failed=40`
- **suggested manual fix:** Audit Bybit API connection/config. Add retry logic or OKX fallback.
- **priority:** medium
- **first observed:** Prior reviews; confirmed 2026-06-20 23:15 EEST

### TODO-CATALYST-MAPPING-LOW
- **issue:** Catalyst mapping has been critically low (~21.6%) throughout 2026-06-20. Symbol resolver not mapping most news events to tracked symbols.
- **evidence:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_2141.md` §5: "21.6% mapped (536/2479)"
- **suggested manual fix:** Audit symbol resolver in catalyst layer. Expand ticker matching (aliases, partial match, case normalization).
- **priority:** medium
- **first observed:** Multiple prior reviews; flagged again 2026-06-20 23:15 EEST
