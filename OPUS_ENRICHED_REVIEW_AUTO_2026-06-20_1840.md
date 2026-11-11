# Opus Enriched Review — US Open Reaction Review (SAT/No Cash Open) — Auto Cycle 18:40 EEST

_Generated 2026-06-20 18:40 EEST (Saturday, weekend crypto-only mode). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

> **WEEKEND NOTE: Saturday 2026-06-20. No US cash open. This 18:30 "US open reaction" slot covers what changed since the 16:20 review — chiefly: EIGEN dropped from signals, 3 new signals triggered (BEL/AXS swing/ALICE swing), SOL upgraded to B-tier 76.**
>
> **REGIME: BTC downtrend ($63.6K), ETH downtrend (confirmed), breadth 45% EMA20. Shorts > catalyst-backed longs.**

_This is a history copy of OPUS_ENRICHED_REVIEW_LATEST.md as written at the 18:40 EEST slot._
_See OPUS_ENRICHED_REVIEW_LATEST.md for the live/current version._

---

## 1. Executive Summary

**Sat 2026-06-20, 18:40 EEST — US open reaction review (WEEKEND: no cash open) — advisory only / no auto-trade.**

- EIGEN scalp (67.6) + EIGEN swing (69.0) — the previous best long-watch — DROPPED from active signals since 16:20 (expired or price invalidated)
- 3 new signals triggered since 16:20: BEL swing, AXS swing, ALICE swing — all weekend Y, NONE with verified catalyst
- SOL upgraded from C-tier 64.9 → B-tier 76 swing WAITING; catalyst confirmed (Morgan Stanley ETF + $16.55M whale buy)
- Active signals grew 20 → 26 (Cycle 1 added 6 net new swing signals from the 16:30 report)
- Performance deteriorated: WR 9.84% → 9.47%, Total R -37.0 → -40.0 (−3R in 2.5h)
- Shorts remain best bucket: WR 28.6%, PF 1.77; longs WR 8.3%, PF 0.43
- BTC ~$63.6K (external confirmed), ETH downtrend; breadth 45% EMA20 — compressed, chop
- BTW/USDT: +107% 24h, extreme long crowding, MEXC-only, no catalyst — AVOID
- Head trader: CAUTION / WAIT-FOR-TRIGGER; prefer shorts and SOL catalyst-backed only

---

## 2. Data Used

| Source | File/Tool | mtime (EEST) | Freshness |
|---|---|---|---|
| Scheduler log | `scheduler.log` | 18:32 | 8 min — fresh |
| Latest cycle | `cycle_01_15-47_summary.md` | 16:31 | 2h9m — fresh (<3h) |
| Scalp report | `2026-06-20_13-01_scalp_report.md` | 16:01 | 2h39m — fresh (<4h) |
| Intraday report | `2026-06-20_13-13_intraday_report.md` | 16:13 | 2h27m — fresh (<4h) |
| Swing report | `2026-06-20_13-30_swing_report.md` | 16:30 | 2h10m — fresh (<4h) |
| Stocks reports | N/A | — | Weekend (not generated) |
| Catalyst events | `2026-06-20/catalyst_events.jsonl` | via reports | 568–598 events, 5 baskets |
| LLM packet | `llm_analysis_packet.md` | via cycle | Refreshed at 16:30 cycle end |
| Active signals CLI | `active-signals --asset-class crypto` | 18:40 live | 26 active signals |
| Signal stats CLI | `signal-stats --asset-class crypto` | 18:40 live | 257 sample |
| Untracked alerts | `detect_untracked_legacy_alerts` | 18:40 live | 0 untracked |
| Paper monitor | `PAPER_MONITOR_STATUS_LATEST.md` | 16:31 cycle | From step 16 of cycle |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_1620.md` | 16:35 est | Previous slot |
| External: BTC price | MetaMask/CoinDesk | 2026-06-20 | $63,609 confirmed |
| External: BEL catalyst | WEEX/Binance | 2026-06-20 | No catalyst found |
| External: EIGEN | MetaMask | 2026-06-12 | $0.18 (Jun 12); ~$0.26 Jun 20 |

**External web research**: available and performed. No uncited claims.

**Blindspots**: Reddit 403 blocked (crowd sentiment missing), on-chain config missing, liquidation heatmaps not connected, live KOL feeds not automated.

---

## 3. Scheduler / Data Freshness

- `scheduler.log` last write: **18:32 EEST** (8 min ago) — FRESH
- `cycle_01_15-47_summary.md` last write: **16:31 EEST** (2h9m ago) — FRESH (< 3h threshold)
- Cycle 1 steps: **ok=18 failed=0** (clean run, no failures)
- Monitor window: 90 min (background pid=12932)
- Paper monitor status (from cycle step 16, 16:31): Open actionable=1 · WAITING=2 · ENTERED UNRESOLVED=25 · REVIEW/SHADOW=129 · NO-ENTRY/stale/moved-away=30 · Needs review=0 · Closed today: 271W/13L/0flat
- Current active signals (CLI 18:40): **26** (up from 20 at 16:01)
- Untracked legacy alerts: **0** (pipeline healthy)
- Bybit OHLCV in swing report: 0 rows / 40 failed (degraded, as flagged in previous review — TODO carries forward)

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-06-20 18:40 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "social_attention_missing", "reddit_blocked"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log mtime 18:32 EEST (8 min ago)",
        "cycle_01 finished 16:31 EEST (2h9m ago) — below 3h threshold",
        "scalp 16:01 / intraday 16:13 / swing 16:30 — all < 3h",
        "Reddit 403 blocked (3 sources) — social attention missing",
        "onchain.yaml config missing — no on-chain data",
        "BEL/BICO/BTW: no verified external catalyst found"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["risk_off", "chop", "wait_for_trigger"],
      "data_missing": ["live_x_twitter_sentiment", "liquidation_heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: downtrend (~$63,609 external confirmed)",
        "ETH trend: downtrend (flipped 16:30 swing from transition_up)",
        "Altcoin breadth EMA20: 45% (declining: 59% at 16:01 → 49% → 45%)",
        "Altcoin breadth EMA50: 55% (neutral zone)",
        "ATR percentile: 16-17th — low volatility, compressed range",
        "Squeeze phase: 23/74 symbols in post-unwind-chop (dominant)",
        "Weekend mode: Saturday — stocks closed, crypto only"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["fresh_catalyst", "no_catalyst", "mapping_weak"],
      "data_missing": ["bel_catalyst_unknown", "bico_catalyst_unverified", "btw_catalyst_unverified"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SOL: confirmed Morgan Stanley spot ETF (cheapest 0.14% fee) + whale $16.55M buy",
        "ETH: Tom Lee rejects funding crisis narrative — single_source, positive sentiment only",
        "BEL +51-59% 24h: NO verified catalyst internally or externally",
        "BICO +71-75% 24h: NO verified catalyst; OI+106%; thin volume 0.16x",
        "BTW +97-107% 24h: extreme long crowding, no catalyst, MEXC primary listing",
        "Axelar $4.7M bridge hack: basket-level risk, unnamed symbol exposure",
        "CLARITY Act: mixed signals — called 'commitment' and 'illicit-finance-friendly'",
        "catalyst_events today: 568-598 events; 5 baskets; momentum_breakout basket active for BTW/BICO/EIGEN"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["liquidation_heatmap_missing", "order_book_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ALICE: OI+111-121%, funding -0.00689 to -0.01252 (most negative of watchlist = crowded longs, long squeeze risk)",
        "BTW: funding +0.00334 across venues (extreme long crowding) — avoid new longs",
        "BICO: OI+106-108%, funding -0.00134 (crowded, OI doubling)",
        "AXS: OI+44-46%, funding -0.00064 to -0.00134 (elevated negative)",
        "BEL: funding -0.00029 to -0.00058 (moderate negative, crowded longs)",
        "SYN: OI-15-18% (short covering = weaker continuation quality)",
        "SOL: OI +0.11-0.26% (benign, no crowding concern)",
        "Squeeze phase distribution: 23 post-unwind-chop / 13 build-up / 3 unwind / 2 squeeze-expansion"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["entry_late", "chase_risk", "price_moved_away", "overextended"],
      "data_missing": ["tradingview_chart_unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "EIGEN: price 0.261 at 16:01 vs zone 0.252-0.258 — above zone, DROPPED from signals by 18:40 (expired or invalidated)",
        "SYN: current 0.1533 vs zone 0.1439-0.1504 — above zone (chase risk)",
        "SOL: current ~71.54 vs zone 71.15-71.44 — slightly above zone, wait for pullback",
        "BICO: current ~0.0412 vs zone 0.0392-0.0413 — AT ZONE but no catalyst",
        "BEL: triggered at zone ~0.0392; no catalyst confirmed",
        "AXS swing: triggered at zone ~1.098-1.125; OI elevated, funding negative",
        "ALICE swing: triggered at zone 0.1296-0.1340; OI+111% long squeeze risk",
        "BTW: +107% 24h, estimated well above pullback levels — extreme extension",
        "TradingView / manual chart check unavailable"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Paper monitor (16:31): OPEN actionable=1 · WAITING for entry=2 · ENTERED UNRESOLVED=25 · REVIEW/SHADOW=129 · NO-ENTRY/stale/moved-away=30 · NEEDS REVIEW=0",
        "Closed today: 271 WINS / 13 LOSSES / 0 FLAT",
        "Expired split: 25 entered-unresolved (entry filled, no TP/SL before window) · 30 no-entry/stale/moved-away",
        "Active signals now (CLI 18:40): 26 (up from 20 at 16:01 — 6 new Cycle 1 signals)",
        "New triggered since 16:20: BEL swing (TRIGGERED), AXS swing (TRIGGERED), ALICE swing (TRIGGERED)",
        "DROPPED since 16:20: EIGEN scalp (67) + EIGEN swing (69) — absent from 26 active",
        "SOL: new B-tier 76 swing signal WAITING (was C-tier 64.9)",
        "Untracked legacy alerts: 0 (PART 1 pipeline healthy)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.80,
      "reason_codes": ["repeated_losses", "correlation_cluster", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Weekend mode: WR 9.4% (3W/14L), PF 0.42 — significantly below non-weekend",
        "Performance deteriorated -3R in 2.5h (16:01 to 18:40: -37R → -40R)",
        "WR dropped 9.84% → 9.47% over same 2.5h window",
        "B-tier overall: PF 0.529 (below 0.8 threshold — observations flagged in signal-stats)",
        "3 triggered signals (BEL/AXS swing/ALICE swing) — all no verified catalyst, all weekend Y",
        "Correlation cluster: BEL+BICO+AXS+ALICE all altcoin longs on BTC+ETH downtrend weekend",
        "BTW: extreme long crowding (funding +0.00334) — high risk to add new long",
        "ALICE: OI+111%, funding -0.0124 — long squeeze candidate, do not add"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Swing RS-leader (14d): WR 72%, PF 5.80, +24R — strongest playbook (none present in current cycle)",
        "Shorts (14d): WR 28.6%, PF 1.77, +3R — only clean positive bucket",
        "Intraday no-catalyst (14d): WR 0.9%, PF 0.05 — severely underperforming",
        "Scalp (14d): WR 8.4%, PF ~0.4 — underperforming",
        "B-tier overall: WR 9.47%, PF 0.529, -40R total (signal-stats observations flagged)",
        "Weekend signals: WR 9.4% (3W/14L); underperformance confirmed",
        "Longs (14d): WR 8.3%, PF 0.43 — negative",
        "No A-tier setups across all modes (scalp/intraday/swing) this cycle"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["wait_for_trigger", "catalyst_backed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Synthesized all eight agents above",
        "EIGEN (previous best long) is GONE — no A-tier replacement in current cycle",
        "Only confirmed catalyst-backed candidate: SOL (Morgan Stanley ETF + whale buy)",
        "Shorts outperform significantly: WR 28.6%, PF 1.77 vs longs 8.3%, PF 0.43",
        "BTC+ETH downtrend + breadth 45% + weekend = maintain defensive posture",
        "3 no-catalyst triggered signals (BEL/AXS/ALICE): already in database, monitor but do not add"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.78,
    "preferred_side": "catalyst_backed",
    "best_long_candidate": {
      "symbol": "SOL/USDT",
      "trigger": "Pullback to 71.15–71.44; 1h close acceptance inside zone; invalidation 1h close <70.80",
      "reason": "Only confirmed dual catalyst (Morgan Stanley ETF 0.14% fee + $16.55M whale buy). B-tier 76 swing WAITING. OI benign. Slightly above zone at ~71.54 — wait for pullback."
    },
    "best_short_candidate": {
      "symbol": "HEI/USDT",
      "trigger": "Failed bounce / retest to 0.1055–0.1081; stop above 0.1109; current price ~0.1038",
      "reason": "-16.7 to -25.4% 24h, weakest RS on watchlist, OI deleveraging -36.9%, thin crowding, BTC+ETH downtrend supports short bias. Wait for bounce — do not chase current price."
    },
    "best_catalyst_candidate": {
      "symbol": "SOL/USDT",
      "trigger": "Pullback to 71.15–71.44; Morgan Stanley ETF catalyst confirmed; whale $16.55M buy confirmed",
      "reason": "Dual catalyst, clearest internal + external alignment this session. B-tier 76 score. Catalyst-backed sub-cohort has best historical edge in swing mode."
    },
    "avoid_candidate": {
      "symbol": "BTW/USDT",
      "reason": "MEXC-only listing, extreme long crowding (funding +0.00334), +97-107% 24h, no verified catalyst, B-tier 66 swing WAITING — do not add long exposure under any circumstances this window"
    },
    "operator_action": "wait_for_trigger",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | **ok** | 0.85 | scheduler_fresh, report_stale (social/onchain missing) | advisory_only |
| market_regime | **caution** | 0.78 | risk_off, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | **caution** | 0.68 | fresh_catalyst (SOL only), no_catalyst (BEL/BICO/BTW), mapping_weak | advisory_only |
| derivatives_squeeze | **caution** | 0.72 | squeeze_risk (ALICE/BICO), oi_supports (AXS), funding_extreme (BTW) | advisory_only |
| technical_entry | **caution** | 0.65 | entry_late (EIGEN gone), chase_risk (SYN/SOL), price_moved_away | advisory_only |
| execution_lifecycle | **ok** | 0.85 | waiting_for_entry, entered_unresolved (25), review_shadow (129) | advisory_only |
| risk_manager | **caution** | 0.80 | repeated_losses (−3R in 2.5h), correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | **caution** | 0.82 | playbook_working (shorts, swing RS-leader), playbook_failing (intraday, longs overall) | advisory_only |
| head_trader | **caution** | 0.78 | wait_for_trigger, catalyst_backed (SOL only clean idea) | advisory_only |

**Overall verdict: CAUTION / WAIT-FOR-TRIGGER**

---

## 4. What Changed vs Previous Review (16:20)

| Item | 16:20 State | 18:40 State | Significance |
|---|---|---|---|
| EIGEN B swing (69) | WAITING — best long candidate | **DROPPED** from active signals | Thesis invalidated / expired — do not re-enter |
| EIGEN B scalp (67) | WAITING | **DROPPED** from active signals | Same as above |
| SOL signal | C-tier 64.9, catalyst-watch | **B-tier 76 swing WAITING** | Upgraded; catalyst still valid |
| BEL/USDT | Not in active signals | **B swing TRIGGERED** (weekend Y) | No catalyst — entered-unresolved risk |
| AXS/USDT | B scalp TP tracking | **B swing TRIGGERED** (weekend Y) | New swing triggered; OI elevated |
| ALICE/USDT | B swing WAITING | **B swing TRIGGERED** (weekend Y) | OI+111%, long squeeze risk |
| BICO/USDT | C-tier AVOID | B swing WAITING (weekend Y) | Still no catalyst; risk unchanged |
| BTW/USDT | Not mentioned | B swing WAITING (weekend Y) | New signal; extreme crowding; AVOID |
| SYN/USDT | B swing WAITING (extended) | B swing WAITING (extended) | Unchanged; still above entry zone |
| NEAR short | Not in active signals | B swing short WAITING (weekend Y) | New directional short signal |
| Active signals | 20 | **26** | +6 net new from Cycle 1 swing report |
| Total R | -37.0 | **-40.0** | −3R deterioration in 2.5h |
| WR | 9.84% | **9.47%** | Declining trend |
| ETH regime | downtrend (from 16:30) | downtrend (confirmed) | No change — maintained bearish |
| Previous best long | EIGEN 0.252-0.258 zone | **None — EIGEN gone** | Regime requires catalyst-backed SOL only |

**New catalysts since 16:20**: None material. SOL catalyst (Morgan Stanley ETF + whale) remains the dominant and only confirmed catalyst. BICO Dream Bowl listing speculation (Jun 23) remains externally unverified.

**Thesis changes**:
- EIGEN thesis: INVALIDATED (signal dropped). The pullback never came, or the invalidation level was breached.
- SOL thesis: UPGRADED (B-tier 76, was C-tier). Still requires pullback to 71.15-71.44.
- HEI short thesis: UNCHANGED (still best short candidate at 0.1055-0.1081 retest).
- Defensive posture: CONFIRMED (BTC+ETH downtrend, breadth 45%, -3R since 16:01).

---

## 5. Catalyst Coverage

- **Today's catalyst events**: 568-598 (growing through the day as new scans ran)
- **Active narrative baskets** (5):
  - `delisting_thin_liquidity` (fresh <1-6h) — primary: none (unnamed)
  - `rwa_narrative` (fresh <24h) — primary: ONDO/USDT, XLM/USDT
  - `binance_ecosystem_teaser` (fresh <24h) — primary: BNB/USDT
  - `ai_narrative` (fresh unknown) — primary: NEAR/USDT, RENDER/USDT, TAO/USDT, FET/USDT
  - `momentum_breakout` (fresh <1h) — primary: BTW/USDT, BICO/USDT, EIGEN/USDT; also ALICE in scalp run
- **Catalyst-confirmed symbols this cycle**: SOL (dual), ETH (narrative only), BTC (macro)
- **Unverified movers**: BEL (+51-59%, no catalyst), BICO (+71-75%, no catalyst), BTW (+97-107%, no catalyst)
- **Notable risk events**:
  - SMCI: export-control indictment (stocks, pre-existing, carry-forward)
  - UNH: DOJ fraud probe (stocks only — not relevant weekend crypto)
  - Axelar bridge hack: $4.7M — IBC/Secret Network affected; basket-level (no named crypto symbol in active signals)

**Catalyst mapping quality**: Dominant event type is `other_news` per previous TODO (catalyst mapping below 50% for symbol resolution — carry-forward). Use catalyst layer as context, not final decision trigger. SOL is the exception with direct named catalyst.

---

## 6. Market Landscape

### Market Mood / Risk Routing

_Driven by the Agent Council `market_regime` + `risk_manager` agents above._

- **Crypto mood**: chop / mixed risk-off (BTC downtrend, ETH downtrend, breadth 45% EMA20 and falling)
- **Stocks mood**: closed (weekend — Saturday)
- **Dominant narrative**: EIGEN dropped; no new RS-leader longs. Short-covering moves in SYN/ALICE/AXS; catalyst rotation around SOL. Crypto staying in compressed range with BTC ~$63.6K.
- **Preferred side now**: catalyst-backed longs (SOL only, pullback required) | failed-bounce shorts (HEI, XLM)
- **Best long candidate**: SOL/USDT — pullback to 71.15–71.44; Morgan Stanley ETF + $16.55M whale confirmed
- **Best short candidate**: HEI/USDT — failed bounce retest 0.1055–0.1081; current 0.1038 (below zone, wait for bounce)
- **Best catalyst-backed candidate**: SOL/USDT (same as best long; confirmed dual catalyst)
- **What to avoid**: BTW/USDT (extreme crowding, MEXC-only, +107% no catalyst); BEL (triggered but unverified catalyst); new altcoin longs in BTC+ETH downtrend without catalyst
- **What would change the view**:
  - Long side: BTC reclaims the 64.5K+ level with 1h close; ETH reverts to transition_up; breadth rises above 55% EMA20 → upgrade to mixed/neutral, permit RS-leader longs
  - Short side: BTC breaks below 62K → accelerate short bias, add failed-retest shorts
  - Catalyst: verified BICO or BEL announcement → re-evaluate those signals
  - Volume: if ALICE/AXS/BEL triggered positions show strong acceptance, the tail could extend — track in next cycle

**Risk-routing summary**: Weekend + BTC+ETH downtrend + 45% breadth + no A-tier = **route to SOL catalyst-backed (pullback only) and HEI short (bounce entry only). No new altcoin long adds without confirmed catalyst. The deteriorating performance (-3R since 16:01) reinforces the conservative routing.**

---

## 7. Candidate Deep Dives (5)

---

### 7.1 SOL/USDT — BEST CATALYST-BACKED LONG-WATCH

**Signal**: B-tier swing 76 score, WAITING for entry, weekend Y
**Internal entry zone**: 71.15–71.44 | **TP1**: 72.21 | **Invalidation**: 1h close <70.80
**Current price (16:01 scalp)**: ~71.56 | **ATR**: 0.647

**Catalyst check (internal)**: `catalyst_events.jsonl` has two confirmed items:
- Whale DAWHnv: $16.55M USDC → 234,898 SOL at avg $70.5 (Lookonchain, 7h before cycle)
- Morgan Stanley spot SOL ETF filing: "Cheapest Spot SOL ETF ever!" at 0.14% fee (AMBCrypto)

**Chase/entry assessment**:
- Price ~71.56 is slightly ABOVE the zone (71.15–71.44) — do NOT buy market
- The whale bought at $70.5 → provides support near 70.5 level
- Invalidation 70.80 is tight (70.5–70.80 is a narrow support band)
- OI change only +0.11% (benign), funding -6.6e-05 (neutral-negative = not crowded longs)
- Pullback to 71.15–71.44 would be a ~0.5-1.0% move from current — reasonable
- A 1h close acceptance IN the zone is the trigger

**Market mood alignment**: SOL is the strongest catalyst-backed candidate. ETF narrative is real, whale buy adds floor support. However, BTC downtrend means SOL correlation risk remains. This is the EXCEPTION to the no-long rule: catalyst + benign derivatives + B-tier 76.

**What would invalidate**: 1h close below 70.80. If BTC breaks 62K, recheck entirely.

**Verdict**: WATCHLIST — WAITING for pullback to 71.15–71.44. **Do not chase 71.56. Pullback + 1h zone acceptance required.**

---

### 7.2 EIGEN/USDT — DROPPED FROM ACTIVE SIGNALS (WAS BEST LONG)

**Previous signal**: B swing (69.0) WAITING + B scalp (67.6) WAITING
**Previous entry zone**: swing 0.2519–0.2583; scalp 0.2516–0.2581
**Previous price (16:01)**: 0.2610 (above entry zone)
**Current status (18:40 CLI)**: **ABSENT from active signals** — signal dropped

**Analysis**:
- At 16:01 price was 0.2610, ABOVE the entry zone of 0.252–0.258 → signal was in "waiting" with price above zone
- Three possible outcomes since 16:20: (a) signal expired (time window closed), (b) price continued up and signal was marked as stale/moved-away (no-entry), (c) price dropped through invalidation 0.2437
- No external catalyst confirmed for EIGEN — the 24h +13-18% move was purely technical RS
- External: EIGEN at ~$0.18 on Jun 12 → ~$0.261 on Jun 20 = +45% in 8 days; this is a significant extension
- Given the low-volatility, range/chop regime and EIGEN's absence from new Cycle 1 signals, most likely explanation: signal EXPIRED or STALE (price never touched entry zone; moved away)
- Track via `data/reports/intraday/` or `data/reports/scalp/` next cycle if EIGEN reappears

**Action**: Do NOT re-enter EIGEN without a fresh signal from the next cycle. The previous entry zones (0.252–0.258) are reference-only; any new entry requires fresh scoring. If EIGEN pulls back to those levels AND a new B-tier signal is generated in Cycle 2, then reassess.

**Verdict**: CLOSED / NO-ENTRY — signal expired or stale. Not actionable without fresh signal from next cycle.

---

### 7.3 BEL/USDT — TRIGGERED BUT NO VERIFIED CATALYST

**Signal**: B swing 65 score, TRIGGERED (weekend Y)
**Entry zone (from cycle)**: implied from swing report (BICO/BEL area ~0.039-0.041)
**Derivatives**: funding -0.00029 to -0.00058 (moderate negative = some short crowding), OI +38-41%
**24h return**: +51.04% (scalp) / +59.84% (swing)
**RS vs BTC**: +49.84%

**Catalyst check**: 
- Internal `news_items` / `catalyst_events`: NO BEL-specific catalyst in any report
- External WebSearch: No specific June 2026 pump catalyst found for Bella Protocol
- Price $0.08-$0.095 on external sources (pre-move); +51-59% puts it at approximately $0.13 range (consistent with reports)

**Assessment**:
- +51-59% move with 1.48x volume (scalp) or 0.61x volume (swing) — volume DECLINING relative to move size
- OI +38-41%: positioning building but not extreme
- Funding slightly negative: shorts adding (contrarian signal = further upside possible but crowding)
- No verified catalyst: this is a momentum/RS trade without fundamental backing
- Signal triggered means price entered the zone — status is now ENTERED UNRESOLVED (no TP/SL hit yet)
- Historical context: "no_catalyst" intraday/scalp is net-negative; swing RS without catalyst is weakest swing sub-cohort
- Reward/risk at current prices: UNKNOWN (chart unavailable), but extended moves without catalyst frequently mean-revert

**Action**: Do NOT add new BEL exposure. The signal is in the database and being tracked. Treat as ENTERED UNRESOLVED. If BTC/ETH accelerates downward, BEL is high-beta exposure to shed.

**Verdict**: ENTERED UNRESOLVED — no catalyst, momentum-only. Monitor only. **Do not add.**

---

### 7.4 AXS/USDT — SWING TRIGGERED (OI ELEVATED)

**Signal**: B swing 65 score, TRIGGERED (weekend Y); also B scalp TP tracking (separate)
**Entry zone (swing from swing report)**: 1.098–1.125 | **TP1**: 1.196 | **Invalidation**: 1.066
**Current price (16:13 intraday)**: 1.138
**Derivatives**: funding -0.00064 to -0.00134 (elevated negative), OI +44-46%

**Catalyst check**: NO verified catalyst in internal or external data. 24h +19-21%, RS vs BTC +19%.

**Assessment**:
- Price 1.138 vs zone 1.098–1.125 → AT/ABOVE zone — signal triggered when price touched zone
- OI +44-46%: meaningful positioning; combined with negative funding = crowded longs
- Gaming sector — no basket activation for gaming (heat 9.2/100, status quiet)
- AXS scalp (also in active signals in TP tracking mode) = dual exposure on this name
- Both scalp TP-tracking AND swing triggered: total exposure doubles if both in paper model
- Without catalyst, the continuation from 1.138 after triggering at ~1.098–1.125 is momentum-dependent
- Invalidation 1.066: current price 1.138 provides 72-point buffer (~6.4%) — adequate margin

**Action**: Signal is tracked. Do NOT add new AXS exposure (dual scalp+swing already in). Monitor for TP1 (1.196) or invalidation breach. If BTC drops, AXS correlation risk is high.

**Verdict**: ENTERED UNRESOLVED — triggered at zone but no catalyst. Monitor both scalp TP and swing. **Do not add.**

---

### 7.5 HEI/USDT — BEST SHORT CANDIDATE

**Signal**: C-tier watchlist 58.3 (scalp), not in active B-tier signals yet
**From 16:20 review**: watching for short entry at 0.1055–0.1081
**Entry zone (short)**: 0.1055–0.1081 | **TP1**: 0.0979 | **Invalidation**: 1h close >0.1109
**Current price (16:01 scalp)**: 0.1038 | **ATR**: 0.0059

**Catalyst check**: NO catalyst noted in any report for HEI.

**Assessment**:
- HEI -16.7 to -25.4% in 24h — consistent weakness across all three report timestamps
- OI deleveraging -36.91% = long liquidation or closing (NOT squeeze-prone short)
- Funding -5.9e-05 (near-zero negative) = not crowded shorts, room to run
- Price 0.1038 is BELOW the short entry zone (0.1055–0.1081) — do NOT enter at current price
- A dead-cat bounce / failed retest back to 0.1055–0.1081 is the entry trigger
- Support: 0.1003; resistance: 0.1350
- If price bounces into zone AND rejects: short with stop 0.1109, target 0.0979-0.0920
- This is the ONLY clean risk-managed short setup on the watchlist

**Market mood alignment**: Short side preferred in current BTC+ETH downtrend. HEI shows relative weakness (RS -26.58% vs BTC) with deleveraging OI = natural short candidate in risk-off crypto regime. Shorts are best performing bucket historically (WR 28.6%, PF 1.77).

**Verdict**: SHORT-WATCH — WAITING for bounce to 0.1055–0.1081. **Current price 0.1038 is too low — wait for bounce first.**

---

## 8. Best Candidates Ranked

No clean immediate entries exist this window. All candidates require trigger events:

| Rank | Symbol | Side | Status | Entry Trigger | Priority |
|---|---|---|---|---|---|
| 1 | SOL/USDT | Long | WAITING | Pullback 71.15–71.44 + 1h close acceptance | Catalyst-backed (highest conviction) |
| 2 | HEI/USDT | Short | Watch | Bounce to 0.1055–0.1081 + rejection | Best short; regime-aligned |
| 3 | NEAR short | Short | WAITING | Confirm entry zone from next cycle report | New short signal, B-tier 65 |
| 4 | XLM/USDT | Short | TP tracking | Already in TP tracking (B swing short) | Tracking, not new entry |
| 5 | AXS/USDT | — | ENTERED UNRESOLVED | Already triggered — monitor TP1 1.196 | Do not add |

**Best long-watch**: SOL/USDT — trigger: pullback to 71.15–71.44, catalyst confirmed
**Best short-watch**: HEI/USDT — trigger: bounce to 0.1055–0.1081, then rejection
**Best catalyst-watch**: SOL/USDT — same as long-watch (dual catalyst: ETF + whale)

---

## 9. Avoid / No Trade (This Decision Window Only)

The following should be avoided in the current 2026-06-20 18:40-22:30 EEST window. This is NOT a command to stop the scanner or disable tracking.

| Symbol | Reason | If Reconsidered |
|---|---|---|
| BTW/USDT | MEXC-only, +107% no catalyst, extreme long crowding (funding +0.00334) | Only if verified catalyst AND price resets to pullback zone post-funding normalization |
| BICO/USDT | +71-75% no verified catalyst, OI+106%, thin volume 0.16x | Only if Dream Bowl listing (Jun 23) is officially confirmed with direct announcement |
| BEL/USDT | Triggered but no catalyst; do not add to existing entered-unresolved exposure | Only if verified news/event materializes |
| ALICE/USDT | OI+111%, funding -0.0124 (highest negative = crowded longs, long squeeze risk) | Only if OI normalizes below 60% and ETH regime recovers |
| SYN/USDT | 7d +382%, price above entry zone at 0.1533, short-covering OI | Only on pullback to 0.1439-0.1504 with BTC recovery |
| EIGEN/USDT | Dropped from signals | Fresh signal required from Cycle 2 |
| New uncatalyzed altcoin longs | BTC+ETH downtrend + weekend underperformance | Wait for BTC reclaim of 64.5K+ and breadth above 55% |

Scanner always continues. No-trade applies to new manual entry decisions only.

---

## 10. Main Risks

1. **BTC breakdown below $62K**: Would accelerate bearish regime; all correlated altcoin longs (SOL, AXS, ALICE, SYN) become higher-risk. Short bias amplified.
2. **ALICE/BICO long squeeze**: OI+111% (ALICE) and OI+106% (BICO) with negative funding = potential rapid long unwind if price reverses. Signals would move to CLOSED LOSS quickly.
3. **Weekend liquidity gap**: Thin markets + no stocks = crypto-only volatility on small catalysts. BTW already showing this dynamic (+107% on limited volume).
4. **ETH regime deterioration**: ETH confirmed downtrend as of 16:30 swing. If ETH breadth continues falling below 40% EMA20, upgrade to risk-off and prefer clean shorts over any longs.
5. **BEL no-catalyst unwind**: BEL +51-59% without verified catalyst — if the unknown driver reverses, BEL will drop sharply. Current signal is entered-unresolved.
6. **Axelar hack contagion**: $4.7M bridge exploit — IBC-linked assets may see risk-off pressure. Not directly affecting current watchlist but watch for Cosmos ecosystem spill-over.
7. **Performance tail risk**: -40R total, WR 9.47%, PF 0.529 — system is in a losing streak. No A-tier setups this cycle. Discretionary reduction of position size is appropriate.
8. **Reddit/social blindspot**: Reddit 403 blocked across all 3 sources — crowd sentiment context is absent. KOL watchlist still has placeholder account. No social amplification detection.

---

## 11. Action Plan — Next 4 Hours (18:40–22:40 EEST)

| Priority | Action | Trigger |
|---|---|---|
| 1 | **SOL watch**: Check if SOL pulls back to 71.15–71.44 | Price action — do not chase above 71.80 |
| 2 | **HEI short**: Watch for bounce to 0.1055–0.1081 | Price bounces from 0.1038 low |
| 3 | **Monitor BEL/AXS/ALICE**: Already triggered — check for TP1 hits or invalidation breaches | TP1 or invalidation levels from signal DB |
| 4 | **ETH regime check**: Did ETH recover transition_up? | Next Cycle 2 swing report (~20:47 EEST if scheduler runs) |
| 5 | **BICO/BTW**: Only re-evaluate if verified news emerges | Official exchange announcement with direct URL |
| 6 | **SYN**: If price returns to 0.1439–0.1504 AND BTC is stable | Pullback to zone only |
| 7 | **NEAR short**: Confirm entry zone from Cycle 2 report | Next scheduled cycle report |
| 8 | **Scanner: ALWAYS ON** | Never pause, never disable |

---

## 12. Final Verdict per Mode

| Mode | Verdict | Active Signals | Conditions |
|---|---|---|---|
| **Scalp** | WATCHLIST-ONLY | B scalp: AXS TP tracking, EIGEN DROPPED | No new scalp entries without fresh A/B signal this window |
| **Intraday** | AVOID-NEW | MET/MEGA in TP tracking | Intraday no-catalyst WR 0.9% — worst bucket; await catalyst |
| **Swing (longs)** | WAIT-FOR-TRIGGER | SOL (76 WAITING), SYN (65, above zone), BICO/BEL/AXS triggered | Only SOL with catalyst is actionable — pullback required |
| **Swing (shorts)** | WATCH-FOR-ENTRY | XLM/MEGA/NEAR in tracking or waiting | HEI best new entry — wait for bounce |
| **Weekend mode** | CAUTION | All 26 signals weekend Y | WR 9.4%, PF 0.42 — use tighter size if in paper mode |
| **Stocks** | CLOSED | N/A (Saturday) | No action until Monday open |

---

## 13. Sources

Internal sources (no URL needed):
- `data/reports/scalp/2026-06-20_13-01_scalp_report.md` (16:01 EEST)
- `data/reports/intraday/2026-06-20_13-13_intraday_report.md` (16:13 EEST)
- `data/reports/swing/2026-06-20_13-30_swing_report.md` (16:30 EEST)
- `data/scheduled_runs/2026-06-20_default_schedule/cycle_01_15-47_summary.md` (16:31 EEST)
- `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_1620.md` (previous review, 16:20 EEST)
- CLI: `active-signals --asset-class crypto` (18:40 EEST live)
- CLI: `signal-stats --asset-class crypto` (18:40 EEST live)
- CLI: `detect_untracked_legacy_alerts --since 2026-06-20` (18:40 EEST live)

External sources:
- [Bitcoin Price Today ~$63,609](https://metamask.io/price/bitcoin) — MetaMask / CoinDesk, 2026-06-20
- [Bella Protocol price (no catalyst found)](https://www.weex.com/tokens/bella-protocol) — WEEX, 2026-06-20
- [EigenLayer price ~$0.18 (Jun 12 ref)](https://metamask.io/price/eigenlayer) — MetaMask, 2026-06-12

---

## 14. Fix Requests / TODO

### TODO-bybit-ohlcv-failure (CARRY-FORWARD)
- **issue**: Bybit returned 0 OHLCV rows in 16:30 swing (40 symbols failed). Swing report has degraded derivatives data for Bybit-primary symbols.
- **evidence**: `cycle_01_15-47_summary.md` step 8 — bybit universe=423, ohlcv_fetched=0, failed=40
- **suggested manual fix**: Investigate Bybit API rate limit or auth token expiry. Check `last_update.json` for Bybit. Manual session to re-authenticate or adjust retry logic.
- **priority**: HIGH
- **first observed**: 2026-06-20 ~16:30 EEST (previous review)

### TODO-catalyst-mapping-quality (CARRY-FORWARD)
- **issue**: Dominant event type is `other_news` — symbol-to-catalyst mapping is weak. BEL, BICO, BTW moved 50-107% but no catalyst was assigned internally.
- **evidence**: Internal reports show "no fresh verified catalyst detected" for all three movers; previous review noted ~94% other_news classification.
- **suggested manual fix**: Review entity extraction logic in catalyst layer; add BEL, BICO, BTW to symbol resolver list if not present; re-evaluate JSONL structure for non-standard tickers.
- **priority**: MEDIUM
- **first observed**: 2026-06-20 16:20 EEST

### TODO-social-reddit-403 (CARRY-FORWARD)
- **issue**: Reddit CryptoCurrency, Reddit Bitcoin, Reddit Ethereum all returning 403 Blocked on every cycle run (multiple consecutive failures).
- **evidence**: `cycle_01_15-47_summary.md` — 6 Reddit 403 warnings across scalp/intraday/swing steps (steps 2, 3, 8).
- **suggested manual fix**: Investigate Reddit API authentication — possibly requires OAuth user token. Consider switching to Pushshift or Reddit API v2 with proper credentials. Or remove Reddit from social sources until fixed.
- **priority**: MEDIUM
- **first observed**: Persistent across multiple days

### TODO-weekend-signal-underperformance-audit
- **issue**: Weekend signals now showing WR 9.4% (3W/14L), PF 0.42 — signal-stats observations flag this. Weekend Y signals are being generated in the same scoring pipeline as non-weekend, but performance is significantly lower.
- **evidence**: `signal-stats --asset-class crypto`: `weekend=Y: WR 15%, n=31` (older entry), now showing 3W/14L=17.6% but PF 0.42. The WR is marginally above non-weekend but PF is dramatically worse, suggesting weekend winners are smaller R.
- **suggested manual fix**: Manual session to audit weekend signal outcomes in detail. Consider a weekend-specific score penalty or minimum score threshold increase (e.g., require score ≥75 on weekends vs ≥65 weekdays). Or investigate whether weekend signals need longer time-horizon TP settings.
- **priority**: MEDIUM
- **first observed**: 2026-06-20 18:40 EEST (signal-stats observations)
