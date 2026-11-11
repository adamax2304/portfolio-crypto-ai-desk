# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

_Generated 2026-06-21 04:39 EEST (Sunday, weekend crypto-only mode). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods._

> **CATALYST UPGRADE: AXS/USDT now has a CONFIRMED catalyst (Terrariums V1 land-staking launch + bAXS first distribution live). Internal reports showed "no catalyst" — external research confirmed it. Upgraded to catalyst-backed candidate.**
>
> **REGIME IMPROVED: BTC transition_up (~$63,935), ETH uptrend. Improvement from prior session's range/chop. Not yet a clean breakout — regime report still says "range/chop (neutral)".**
>
> **SQUEEZE CLUSTER: ALICE +54%, BICO +52%, BTW +72% — extreme funding levels, no verified catalyst. Short-squeeze or momentum blow-off. AVOID new longs on these names.**
>
> **BICO WARNING: Team wallets unstaked 90M BICO and deposited to Gate.io near price tops (insider selling signal). AVOID.**
>
> **SIGNALS: 29 active (up from 22). OPEN/TRIGGERED: ~5. WAITING: ~5. TP1 REACHED / ENTERED UNRESOLVED: ~19. NEAR short = WAITING. Untracked alerts: 0 (clean).**

---

## 1. Executive Summary

**Sun 2026-06-21, 04:39 EEST — crypto overnight / Asia review — advisory only / no auto-trade.**

- Slot type: **crypto_overnight** (04:30 EEST). Stocks closed (Sunday weekend). Crypto-only live class.
- Scheduler fresh: scheduler.log 04:37 EEST (2 min ago). Cycle 4 ACTIVE — scalp completed, intraday timed out, catalyst scan just started.
- BTC: transition_up ~$63,935 (range $63,000–$64,145). ETH: uptrend ~$1,727+. Weekend mode ACTIVE.
- **Regime improved overnight**: BTC was range/chop in prior review ($63,609), now transition_up ($63,935). ETH improved from transition_up to uptrend. Not a clean breakout yet.
- **AXS catalyst confirmed** (external research): Terrariums V1 land-staking (June 17 launch), bAXS first distribution live. Futures volume +900%, OI +95%. System missed this — scored "no catalyst" internally.
- **Active signals**: 29 (up from 22). OPEN/TRIGGERED: ~5 (ETH intraday, BEL intraday/swing, SAND intraday, ALICE intraday). WAITING: ~5 (AXS scalp, SAND scalp, BTC intraday, NEAR short, W/? intraday). TP1 REACHED / ENTERED UNRESOLVED: ~19.
- **BICO insider dump**: team wallets 90M BICO → Gate.io near tops. AVOID.
- **Untracked legacy alerts**: 0 (pipeline healthy).
- **signal-stats**: failed exit 255 — stats unavailable this cycle, carry-forward from prior review (longs PF 0.54, shorts PF 1.77, week Total R –37).
- **Preferred action**: wait for AXS pullback to $1.186–$1.206 (catalyst-backed). Monitor NEAR short (WAITING). Avoid BICO/ALICE/BTW.

---

## 2. Data Used

| Source | File / Tool | mtime EEST | Freshness |
|---|---|---|---|
| Scheduler log | `scheduler.log` | 04:37 | 2 min — FRESH |
| Latest cycle summary | `cycle_03_00-51_summary.md` | 01:25 | 3h14m — acceptable (scheduler.log is fresh) |
| Scalp report | `2026-06-21_00-50_scalp_report.md` | 03:50 | ~49 min — FRESH |
| Intraday report | `2026-06-21_01-32_intraday_report.md` | 04:32 | ~7 min — FRESH (timed out at 04:37 mid-cycle) |
| Swing report | `2026-06-20_13-30_swing_report.md` | 16:30 Jun 20 | ~12h — BORDERLINE STALE |
| Stocks reports | not generated | — | STALE (expected Sunday) |
| Catalyst events (Jun 20) | `data/catalysts/2026-06-20/catalyst_events.jsonl` | 01:23 | 399 events, carry-forward |
| Catalyst cycle | `catalyst_cycle_22-23.md` | 01:23 | 3h16m — acceptable |
| Jun 21 catalyst data | not yet generated | — | MISSING (scan started 04:37) |
| LLM packet | `data/processed/llm_analysis_packet.md` | 03:50 | weekend mode confirmed |
| Active-signals CLI | returned 04:39 | live | 29 signals — confirmed |
| Signal-stats CLI | FAILED exit 255 | — | MISSING — carry prior review |
| Detect untracked | returned 04:39 | live | 0 untracked — pipeline healthy |
| Prior review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_2315.md` | 23:15 Jun 20 | Previous slot |
| External: BTC price | WebSearch | 2026-06-21 | $63,935 confirmed |
| External: AXS catalyst | WebSearch + WebFetch EdaFace | 2026-06-20 | Terrariums V1 + bAXS confirmed |
| External: BICO/ALICE | WebSearch CoinMarketCap | 2026-06-21 | BICO insider dump flag; ALICE no catalyst |

**External web research**: Available and used. BTC price, AXS catalyst, BICO/ALICE searched and cited.

**Blindspots**: June 21 catalyst scan not yet available; signal-stats failed; Reddit 403 (crowd sentiment missing); on-chain config absent; cycle_4 intraday timed out; Bybit OI partial (intraday uses fallback_via_mexc).

---

## 3. Scheduler / Data Freshness

- `scheduler.log` last write: **04:37 EEST** (2 min ago) — **FRESH**
- `cycle_03_00-51_summary.md` finished: **01:25 EEST** (3h14m ago) — within rule → **NOT DEFERRED**
- **Cycle 4 status** (started 03:25 EEST, weekend, crypto-only):
  - track-signals (pre): completed 03:27 (69s)
  - crypto scalp report: completed 03:52 (**1511s = 25 min** — very slow)
  - crypto intraday report: **TIMED OUT** 04:37:13 (45 min — pipeline anomaly, TODO §14)
  - catalyst scan: **just started** 04:37 — June 21 data pending
- Weekend mode: **ACTIVE** (Sunday; A-tier score penalty +7, chasing demotes to C, MEXC-only cap at C)
- Untracked legacy alerts: **0** — pipeline healthy
- Social sources: Reddit all 403 (expected, recurring)

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-06-21 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["scheduler_fresh", "catalyst_missing", "derivatives_sparse", "packet_missing"],
      "data_missing": [
        "June 21 catalyst scan (just started — output pending)",
        "signal-stats CLI failed exit 255",
        "cycle_4 intraday timed out (45 min) — partial report only",
        "on-chain config (config/onchain.yaml)",
        "Reddit sentiment (403 blocked)",
        "Bybit OI for intraday names (fallback_via_mexc)"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log 04:37 EEST (2 min) — FRESH",
        "cycle_03 summary 01:25 (3h14m) — acceptable",
        "scalp report 03:50 FRESH; intraday 04:32 FRESH but timed out at 04:37",
        "swing report 12h ago — borderline stale",
        "catalyst events: June 20 cycle_22-23 (399 events, 01:23)",
        "active-signals returned: 29 signals",
        "detect_untracked: 0 — healthy"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["mixed", "chop", "longs_preferred", "wait_for_trigger"],
      "data_missing": [
        "live KOL/Telegram sentiment",
        "on-chain flow data",
        "ETF fund flows",
        "liquidation heatmap"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: transition_up ~$63,935 (range $63K–$64.1K)",
        "ETH trend: uptrend ~$1,727+",
        "Altcoin breadth EMA20: 46.15% (below 50% — not broad)",
        "ATR percentile: 9.0 (low volatility)",
        "Report regime: range/chop (neutral)",
        "Macro risk 27/100 — risk-on tailwind",
        "BTC shrugged off Japan rate hike"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["fresh_catalyst", "no_catalyst", "mapping_weak", "narrative_supported", "catalyst_confirmed"],
      "data_missing": [
        "June 21 catalyst scan not yet run",
        "ALICE: no catalyst confirmed (external search negative)",
        "BTW: no catalyst confirmed"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "AXS: Terrariums V1 launch (June 17) + bAXS first distribution live — CONFIRMED (EdaFace/Phemex)",
        "AXS futures volume +900%, OI +95%",
        "BICO: team 90M → Gate.io = insider dump signal (CoinMarketCap CMC-AI)",
        "ALICE: no catalyst found (external search negative)",
        "ai_narrative basket: NEAR/RENDER/TAO/FET active",
        "perps_dex basket: HYPE/DYDX/GMX primary",
        "momentum_breakout: MET primary (pure momentum, no catalyst)",
        "June 20 cycle_22-23: 399 events, <20% mapped — catalyst layer is context only"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme", "data_unavailable"],
      "data_missing": [
        "Bybit OI for intraday names (fallback_via_mexc; OI 24h = n/a)",
        "liquidation cluster heatmap",
        "on-chain flow"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "AXS: funding -0.000372 to -0.00142 (cross-venue negative) = shorts paying longs; OI +41.92%; crowding elevated",
        "ALICE: funding -0.003128 to -0.00954 (extreme negative) = massive short squeeze; OI +89.76%",
        "BTW: funding +0.002675 to +0.00377 (strong positive) = crowded long; extreme long crowding label",
        "BICO: funding -7.7e-05 — neutral; OI +17.51%; crowding moderate",
        "SAND: funding -0.000262 — slightly negative; OI +36.28%",
        "MET: funding +9e-06 — neutral; OI n/a (mexc fallback)"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["chase_risk", "clean_retest", "overextended", "price_moved_away"],
      "data_missing": [
        "TradingView chart MCP not loaded",
        "Live price updates (reports based on 00:45 UTC data freshness)"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "AXS: price $1.215, resistance $1.236, pullback zone $1.186–$1.206 — do NOT chase",
        "ALICE: +54.5%, no clean entry — squeeze exhaustion risk",
        "BICO: +52.9%, insider dump risk — no entry",
        "BTW: +72.4%, extreme long crowding — no entry",
        "SAND: $0.0610, resistance $0.0639, pullback $0.0596–$0.0606",
        "NEAR: WAITING for system short entry zone"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [
        "signal-stats failed — exact R / WR counts unavailable this cycle",
        "paper monitor cycle output not read this slot"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "active-signals CLI: 29 signals (up from 22 in prior review)",
        "WAITING for entry: AXS scalp, SAND scalp, BTC intraday, NEAR short, W/? intraday (~5 signals)",
        "OPEN/TRIGGERED: ETH intraday, BEL intraday, SAND intraday, ALICE intraday, BEL swing (~5 signals)",
        "TP1 REACHED / ENTERED UNRESOLVED: ~19 signals",
        "Untracked legacy alerts: 0 — pipeline healthy",
        "SYN swing: AVOID flag from prior review — not visible in current table (may have been resolved or expired)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["repeated_losses", "correlation_cluster", "reduce_risk", "headline_risk"],
      "data_missing": ["on-chain config", "live KOL feeds"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Prior review week stats: Total R -37, longs PF 0.54 (losing), shorts PF 1.77",
        "Weekend mode: thinner liquidity, wider spreads",
        "BICO: team dump 90M to Gate.io — headline risk",
        "ALICE: pure short squeeze +54% — gap reversal risk",
        "ALICE intraday TRIGGERED = open position in squeeze — elevated risk",
        "AXS at resistance $1.236 — do NOT add above zone",
        "Cycle_4 intraday timeout — pipeline anomaly",
        "Axelar $4.67M bridge exploit (June 20) — cross-chain background risk"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [
        "signal-stats failed exit 255 — current stats unavailable",
        "Using carry-forward from prior review"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Carry-forward: scalp 1W/13L (PF 0.14) — failing",
        "Carry-forward: intraday WR 23% (PF 0.70, -3R no-catalyst bucket)",
        "Carry-forward: swing 7W/40L (PF 0.43)",
        "Carry-forward: shorts PF 1.77 — only working bucket",
        "Scalp known TP mismatch: 100% MFE positive, avg MFE 0.54R vs TP1 1.86R",
        "US close Jun 20: +3R improvement (Total R -40 → -37)"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.73,
      "reason_codes": ["wait_for_trigger", "catalyst_confirmed", "shorts_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "All 8 agents: caution across the board",
        "AXS catalyst confirmed externally — upgrades from no-catalyst to catalyst-backed",
        "BICO insider dump = hard avoid",
        "ALICE squeeze open position = monitor carefully",
        "ALICE/BTW no-catalyst = avoid new longs",
        "Short bucket only profitable direction week-to-date (PF 1.77)",
        "BTC transition_up = improvement but not confirmed breakout"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.73,
    "preferred_side": "catalyst_backed",
    "best_long_candidate": {
      "symbol": "AXS/USDT",
      "trigger": "pullback into $1.186–$1.206 + 15m acceptance; do NOT buy above $1.215 near resistance $1.236",
      "reason": "Terrariums V1 land-staking (June 17) + bAXS first distribution live = confirmed catalyst. Futures volume +900%, OI +95%. Negative funding (shorts paying) = squeeze support. Wait for pullback."
    },
    "best_short_candidate": {
      "symbol": "NEAR/USDT",
      "trigger": "WAITING zone hit per system (B-tier swing short active); or JTO on 1h structural breakdown",
      "reason": "NEAR: B-tier swing short WAITING, deleveraging structure (price/OI down), AI sector crowded. JTO: -9.34% 24h, RS -10.54% vs BTC = second weakest behind HOME."
    },
    "best_catalyst_candidate": {
      "symbol": "AXS/USDT",
      "trigger": "pullback to $1.186–$1.206 zone, 15m close accepted",
      "reason": "Only confirmed fresh crypto catalyst in current scan. SOL (bitFlyer June 24) is carry-forward second choice on pullback $70.44–$70.73."
    },
    "avoid_candidate": {
      "symbol": "BICO/USDT",
      "reason": "Team wallets unstaked 90M BICO and deposited to Gate.io near price tops (insider selling). +52.9% move is likely a distribution event. Do not long under any conditions this window."
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.72 | scheduler_fresh, catalyst_missing, derivatives_sparse, packet_missing | advisory_only |
| market_regime | caution | 0.72 | mixed, chop, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.68 | fresh_catalyst, no_catalyst, mapping_weak, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.68 | squeeze_risk, oi_supports, funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.68 | chase_risk, clean_retest, overextended, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.72 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.75 | repeated_losses, correlation_cluster, reduce_risk, headline_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.73 | wait_for_trigger, catalyst_confirmed, shorts_preferred | advisory_only |

---

## 4. What Changed vs Previous Review

Previous: `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_2315.md` (23:15 EEST)

| Change | Previous (23:15 Jun 20) | Now (04:39 Jun 21) |
|---|---|---|
| BTC regime | range/chop ~$63,609 | transition_up ~$63,935 (+$326) |
| ETH regime | transition_up ~$1,727 | uptrend ~$1,727+ |
| AXS catalyst | "no catalyst" (internal) | **CONFIRMED** Terrariums V1 + bAXS |
| BICO | momentum mover, no flag | **Team dump 90M → Gate.io** — AVOID |
| ALICE | not top candidate | +54.5% short squeeze, **TRIGGERED intraday B-tier** |
| BTW | +97% swing (stale) | +72.4% 24h, extreme long crowding |
| Active signals | 22 | **29** (7 new, mostly TP1-reached) |
| OPEN/TRIGGERED | 4 (SAND scalp, BEL swing, AXS swing, SYN swing) | ~5 (ETH intraday, BEL intraday/swing, SAND intraday, ALICE intraday) |
| WAITING | 1 (NEAR short) | ~5 (AXS scalp, SAND scalp, BTC intraday, NEAR short, W/?) |
| SYN | TRIGGERED vs AVOID flag | Not visible in active table — may be resolved/expired |
| Intraday pipeline | Clean | Cycle 4 TIMEOUT (45 min) |
| Catalyst scan | cycle_22-23 (01:23 EEST) | Same (June 21 scan just started) |
| Untracked alerts | 0 | **0** (confirmed this run) |

**New this cycle**: AXS external catalyst confirmation, BICO insider dump warning, ALICE squeeze identification with open triggered intraday signal.

---

## 5. Catalyst Coverage

**June 20 cycle_22-23 (latest — 01:23 EEST, 3h16m ago):**
- Total catalyst events: **399**
- By type: other_news 382, partnership 5, product_launch 3, legal_risk 3, exploit_hack 2, analyst_action 1, insider_activity 1
- Narrative baskets: **4** (perps_dex_narrative, delisting_thin_liquidity, ai_narrative, momentum_breakout)
- Estimated mapped to specific crypto symbols: **<20%** (382/399 = 95.7% classified as other_news; top catalysts mostly "basket" unmapped)

> **⚠ CATALYST MAPPING CRITICALLY LOW — estimated <20% of events mapped to specific crypto symbols. Use catalyst layer as CONTEXT ONLY, not final decision basis.**
>
> Top 3 unmapped basket headlines:
> 1. "JaredFromSubway MEV bot exploited for $15M+" (exploit_hack)
> 2. "Popular sporting goods chain files Chapter 11 bankruptcy" (legal_risk)
> 3. "OpenAI partners with Open Network Lab" (partnership)

**June 21 catalyst scan**: Not yet run (started 04:37). Data will be available after next cycle completion.

**Notable mapped events (verified)**:
- **SMCI** [legal_risk, 0.77]: export-control indictment — AVOID
- **UNH** [legal_risk, 0.73]: DOJ probe, -16% — weekend/stocks, carry context only
- **HYPE + perps DEX** [perps_dex_narrative]: HYPE/DYDX/GMX/ASTER narrative active
- **AI narrative**: NEAR/RENDER/TAO/FET primary; WLD/ASTER related
- **Axelar bridge** [exploit_hack, 0.75]: $4.67M Secret Network breach — cross-chain background risk

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood**: mixed → transitioning (BTC transition_up, ETH uptrend; report regime "range/chop"; not confirmed breakout)
- **Stocks mood**: closed (Sunday)
- **Dominant narrative**: GameFi revival (AXS Terrariums V1), AI rotation (NEAR/TAO/FET), perps DEX (HYPE)
- **Preferred side now**: catalyst-backed longs on pullback + shorts on RS laggards
- **Best long candidate**: AXS/USDT — pullback to $1.186–$1.206, 15m acceptance; do NOT buy at $1.215 near resistance $1.236
- **Best short candidate**: NEAR/USDT — WAITING zone hit per system; JTO/USDT on 1h structural breakdown
- **Best catalyst-backed candidate**: AXS/USDT (Terrariums V1 + bAXS); SOL/USDT carry-forward (bitFlyer June 24 listing, retest $70.44–$70.73)
- **What to avoid**: BICO (insider dump), ALICE (squeeze exhaustion + open triggered), BTW (extreme long crowding), SYN (delisted + no catalyst)
- **What would change the view**: BTC sustained break above $64,500 with volume → upgrade to risk-on; BTC break below $63,000 → revert to shorts-preferred

**Risk routing**: Not a broad "no trade" window. Route by catalyst and side. Catalyst-backed long (AXS pullback) and RS short (NEAR/JTO) are the two actionable paths. No-catalyst momentum longs = negative expectancy in range/chop (WR 23%, PF 0.70 per 14d no-news cut).

---

## 7. Candidate Deep Dives

### Candidate 1 — AXS/USDT (Best Catalyst-Backed Long Watch)

**Lifecycle status**: WAITING for entry (AXS scalp B-tier), WAITING (AXS swing, TP1 reached per signals row 12 → actually shows tp_hit status). Two signals: scalp WAITING + swing TP1-reached/entered-unresolved.

**Score**: Scalp 68.3 (B, low confidence); Intraday 63.0 (C, watchlist). Weekend mode applied.

**Catalyst**: CONFIRMED. Terrariums V1 land-staking (June 17 2026), replacing Homeland. bAXS first distribution live. Futures volume +900%, OI +95% (EdaFace June 20 2026, WebFetch verified). This upgrades AXS from "no catalyst" to catalyst-backed — the internal system missed this.

**Has price reacted?** Yes — +22.7% 24h (+25.26% 7d). Move is catalyst + short-squeeze hybrid. Negative funding (-0.000372 to -0.00142 cross-venue) = shorts paying longs = squeeze component. Real catalyst exists but squeeze adds fragility.

**Is setup chasing?** Current $1.215 near resistance $1.236. System explicitly says "No market buy if extended." Entry zone: pullback to $1.186–$1.206. Not a chase if pullback occurs.

**Overextended?** Near resistance $1.236. ATR $0.0443. Support at $1.104. Not yet >2ATR stretch but at a key level.

**Entry NOW late?** YES — do not enter at $1.215. Wait for pullback to $1.186–$1.206 with 15m acceptance.

**Catalyst confirmation**: CONFIRMED externally. Internal system gap flagged in §14 TODO.

**Weekend risk**: Weekend mode — demand cleaner structure, prefer ATR-based stop, max scalp hold 2h, no chasing after impulse candles.

**Invalidation**: 1h close below $1.162.

**Targets**: TP1 $1.259, TP2 $1.304, TP3 $1.348.

**Verdict**: WAITING for pullback trigger. Catalyst-backed. Best long candidate this window.

---

### Candidate 2 — NEAR/USDT (Short WAITING — B-tier Swing)

**Lifecycle status**: WAITING for entry (B-tier swing short, row 10 in active-signals table, entry zone ~2.xxx).

**Catalyst**: AI narrative basket active (NEAR primary in ai_narrative). This is the dominant narrative but also means crowded — many participants aware of the same sector. No positive catalyst for NEAR specifically.

**Derivatives**: From prior review: price/OI down (deleveraging structure). Current active-signals confirms WAITING zone ~2.xxx still active.

**Aligned with market mood?** YES — BTC transitioning up but NEAR shows RS weakness vs BTC historically. AI narrative crowding can reverse on any broad sentiment shift.

**Is setup chasing?** No — WAITING means price hasn't yet reached the short entry zone. Patient entry.

**What makes it actionable?** System WAITING zone hit (per signal levels). Do not manually force entry.

**Invalidation**: Per system levels (unknown without full CLI output, but system-managed).

**Verdict**: WAITING for system trigger. Do not force. Best structured short candidate.

---

### Candidate 3 — ALICE/USDT (Open — CAUTION / Monitor Closely)

**Lifecycle status**: TRIGGERED / OPEN (B-tier intraday long, row 8 in active-signals table, entry ~0.0xxx).

**This is a RISK FLAG**: ALICE has an open triggered intraday long with extreme short-squeeze dynamics.

**Evidence**: +54.51% 24h, +53.31% RS vs BTC. Volume 1.12x. OI +89.76% (scalp) — massive OI spike. Funding -0.003128 to -0.00954 (extreme negative) = shorts paying heavily = active short squeeze.

**Catalyst**: No catalyst found (external WebSearch returned no news). Pure squeeze on no-catalyst name = volatile both ways.

**Risk**: Squeeze exhaustion can unwind rapidly, especially on weekend thin liquidity. The open ALICE intraday long is exposed to sudden reversal if funding normalizes or buyers exhaust.

**Should new position be opened?** NO. ALICE is an OPEN EXISTING signal, not a new opportunity. Monitor for TP or stop trigger. Do not add or double.

**Verdict**: EXISTING OPEN position — monitor for TP1 or stop. Do NOT initiate new longs. Elevated reversal risk.

---

### Candidate 4 — BICO/USDT (AVOID — Insider Selling)

**Lifecycle status**: Not in active-signals table. Pure momentum mover, no system signal.

**Insider selling alert**: Team-associated wallets unstaked **90 million BICO** and deposited to Gate.io near local price tops (CoinMarketCap CMC-AI, June 2026). Classic distribution pattern.

**Price**: +52.9% 24h. OI +17.51%. Funding -7.7e-05 (near neutral). In prior swing report "momentum_breakout" basket.

**Catalyst assessment**: ERC-8211 Ethereum Foundation standard (April 2026 — old, price-discovery already happened). Dream Bowl I listing June 23 (speculative; not confirmed boost). No fresh verified catalyst.

**Verdict**: **HARD AVOID**. Team is distributing at elevated prices. Do not long. Potential short setup after momentum exhaustion, but not now.

---

### Candidate 5 — JTO/USDT (Short Manual Watchlist)

**Lifecycle status**: Not in active-signals. Detected as RS laggard from momentum table.

**Evidence**: 24h -9.34%, RS vs BTC -10.54% (second weakest after HOME). No positive catalyst. No news mapped in catalyst cycle.

**Not a system signal**: Manual watchlist observation only. No B-tier signal generated.

**Actionable?** Only with manual setup verification (chart, entry, invalidation, SL levels). Cannot trade without a clean setup.

**Verdict**: SHORT-WATCH only. Best RS-weakness candidate without system signal. Needs manual session with TradingView to define entry and SL.

---

## 8. Best Candidates Ranked

No A-tier. Weekend mode + range/chop = trigger-based approach only.

| Rank | Symbol | Side | Tier | Lifecycle | Exact Trigger |
|---|---|---|---|---|---|
| 1 | AXS/USDT | Long (catalyst-backed) | B scalp | WAITING for entry | Pullback to $1.186–$1.206 + 15m acceptance |
| 2 | NEAR/USDT | Short | B swing | WAITING for entry | System WAITING zone (~2.xxx) hit per signal |
| 3 | JTO/USDT | Short | Manual watchlist | Not in system | 1h structural breakdown below support (chart needed) |
| 4 | SOL/USDT | Long (catalyst carry-fwd) | B swing | TP1 reached | Retest $70.44–$70.73 (bitFlyer June 24 listing) |
| Monitor | ALICE/USDT | — | B intraday | OPEN TRIGGERED | Watch for TP1 or stop — do NOT add |
| AVOID | BICO/USDT | — | — | Not in system | Insider dump — no entry under any conditions |
| AVOID | BTW/USDT | — | — | Not in system | Extreme long crowding |

---

## 9. Avoid / No Trade

**This decision window only. Scanner and tracking continue in all moods.**

- **BICO/USDT**: Insider dump (90M to Gate.io near tops). Hard avoid for longs.
- **BTW/USDT**: +72.4%, extreme long crowding (funding +0.00265–+0.00377). Avoid both sides.
- **ALICE/USDT (new entries)**: Pure squeeze, no catalyst, open position already exists. Do NOT open new positions. Monitor existing.
- **SYN/USDT**: Bitget delisted June 18. No catalyst. Not visible in current active-signals (may be expired).
- **No-catalyst momentum longs in chop**: Playbook WR 23%, PF 0.70, -3R over 14d (intraday no-news bucket). Negative expectancy clearly documented.

---

## 10. Main Risks

1. **ALICE intraday OPEN in squeeze**: Existing triggered long in +54.5% squeeze move. Weekend thin liquidity = rapid reversal risk if squeeze exhausts. Monitor closely for TP1 or stop trigger.
2. **Intraday report timeout (cycle 4, 45 min)**: Signal generation may be incomplete. Some new intraday candidates from cycle 4 may be missing.
3. **Catalyst mapping critically low (<20%)**: High probability of missing important overnight developments for less-covered tokens.
4. **signal-stats CLI failed (exit 255)**: Cannot confirm current win rate / total R this cycle. Carry-forward stats may be stale by 2+ hours.
5. **BICO insider dump**: If additional team wallet moves occur, weekend liquidity will amplify the drop.
6. **AXS near resistance**: Even with catalyst, $1.215 near $1.236 resistance. Failed break = fast pullback to $1.162 (invalidation).
7. **Axelar bridge exploit (June 20)**: $4.67M Secret Network breach. No crypto-wide contagion confirmed but background risk for cross-chain names.
8. **BTC low ATR (percentile 9.0)**: Low volatility can precede a directional move. Either expansion up (confirms transition_up) or down trap.

---

## 11. Action Plan — Next 4 Hours

| Time (EEST) | Action |
|---|---|
| 04:45 | Check catalyst scan output when June 21 `data/catalysts/2026-06-21/` folder appears |
| 04:45 | Check if signal-stats recovers (retry when next scheduler cycle runs) |
| 05:00 | AXS: if pullback to $1.186–$1.206, watch for 15m acceptance — scalp entry trigger |
| 05:00 | NEAR: monitor if WAITING zone hit per system (no forced action) |
| All window | ALICE open signal: monitor for TP1 ($0.0xxx per system) or stop trigger — do NOT add |
| All window | AVOID BICO, BTW, SYN regardless of price action |
| All window | No new no-catalyst momentum longs |
| 06:00+ | Europe pre-market builds. BTC above $64,145 (overnight high) = upgrade signal; below $63,000 = downgrade |
| 07:30 | Next scheduled cycle expected (~2h from cycle 4 start at 05:30?). Check new signals |

---

## 12. Final Verdict per Mode

| Mode | Verdict | Active? | Notes |
|---|---|---|---|
| **Scalp** | WATCH/WAIT | Yes (24/7) | AXS pullback $1.186–$1.206 = only clean catalyst-backed trigger. Known TP mismatch issue — consider partial at early MFE. Weekend max hold 2h. |
| **Intraday** | WATCH/WAIT | Yes (24/7) | AXS C-tier watchlist. ALICE B-tier TRIGGERED already. BTC intraday WAITING. No new C-tier long in chop without catalyst. |
| **Swing** | CARRY-FORWARD | Yes (24/7) | AXS swing TP1 reached (ENTERED UNRESOLVED per lifecycle). NEAR short WAITING. BEL swing TRIGGERED. SOL swing TP1 reached. All statuses from CLI carry-forward. |
| **Stocks** | CLOSED | No | Sunday. No reports. Next: Monday pre-market context needed. |

**Overall**: **CAUTION / WATCH FOR TRIGGER.** Regime improving but not clean breakout. Best catalyst-backed setup is AXS on pullback. Best short is NEAR on trigger. Avoid squeeze cluster. Scanner continues. No recommendation to pause or stop any system component.

---

## 13. Sources

| # | Title | Source | Date | URL |
|---|---|---|---|---|
| 1 | "Why Is Axie Infinity Price Up Today?" — Terrariums V1 catalyst confirmed | EdaFace Newsfeed | 2026-06-20 | [EdaFace](https://news.edaface.com/2026/06/20/why-is-axie-infinity-price-up-today/) |
| 2 | "Axie Infinity Price Today and Why AXS Moved on the Terrariums V1 Launch" | Phemex | 2026-06 | [Phemex](https://phemex.com/blogs/axie-infinity-price-axs-terrain-v1-launch) |
| 3 | "Axie Infinity Price Prediction 2026: GameFi's $380M Volume Surge" | Bitget News | 2026-06 | [Bitget](https://www.bitget.com/news/detail/12560605161832) |
| 4 | "Latest Biconomy (BICO) Price Analysis" — team dump 90M to Gate.io | CoinMarketCap CMC-AI | 2026-06 | [CoinMarketCap](https://coinmarketcap.com/cmc-ai/biconomy/price-analysis/) |
| 5 | BTC price $63,935, range $63K–$64.1K | CoinDesk (WebSearch) | 2026-06-21 | [CoinDesk](https://www.coindesk.com/price/bitcoin) |
| 6 | Scalp report | `data/reports/scalp/2026-06-21_00-50_scalp_report.md` | 03:50 EEST | local |
| 7 | Intraday report | `data/reports/intraday/2026-06-21_01-32_intraday_report.md` | 04:30 EEST | local |
| 8 | Swing report (borderline stale) | `data/reports/swing/2026-06-20_13-30_swing_report.md` | 16:30 EEST Jun 20 | local |
| 9 | Catalyst cycle 22-23 | `data/catalysts/2026-06-20/catalyst_cycle_22-23.md` | 01:23 EEST | local |
| 10 | Prior review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-20_2315.md` | 23:15 Jun 20 | local |

---

## 14. Fix Requests / TODO

### TODO-INTRADAY-TIMEOUT
- **issue:** Cycle 4 crypto intraday report timed out after 45 minutes (03:52–04:37). Scalp took 25 min. Intraday consistently slower and now failing.
- **evidence:** `scheduler.log`: `2026-06-21 04:37:13,857 [ERROR] CMD TIMEOUT: crypto intraday report`
- **suggested manual fix:** Investigate intraday pipeline for stuck steps (LLM call hanging? agent count exceeded?); check if intraday universe size grew vs scalp; consider per-agent timeout guard or parallel execution.
- **priority:** high
- **first observed:** 2026-06-21 04:37 EEST

### TODO-SIGNAL-STATS-EXIT255
- **issue:** `python -m src.cli signal-stats --asset-class crypto` failed with exit code 255. Stats unavailable this review.
- **evidence:** Background task brxva8tmb: exit code 255.
- **suggested manual fix:** Run signal-stats interactively to see error message. Check if DB lock conflict with active cycle (cycle 4 may have held a write lock during stats query).
- **priority:** high
- **first observed:** 2026-06-21 04:39 EEST

### TODO-CATALYST-NEWS-GAP-AXS
- **issue:** AXS scored "no fresh verified catalyst" in both scalp and intraday reports despite Terrariums V1 (June 17) being a major confirmed real catalyst. Internal news mapping missed it.
- **evidence:** Scalp report: `catalyst_news: 5.4` / "no fresh verified catalyst detected" for AXS. External: EdaFace (June 20), Phemex, Bitget all confirm Terrariums V1 as primary driver. Futures volume +900%.
- **suggested manual fix:** Check if Terrariums V1 news ingested in `news_items` with AXS in `detected_symbols_json`. If absent, review news source coverage for GameFi/Axie. Consider adding The Block or Decrypt as sources.
- **priority:** high
- **first observed:** 2026-06-21 04:39 EEST

### TODO-BICO-INSIDER-FLAG
- **issue:** BICO +52.9% appeared in momentum candidates. Team wallets (90M → Gate.io near tops) = insider distribution not captured in internal scoring.
- **evidence:** CoinMarketCap CMC-AI (WebSearch June 2026): "team-associated wallets unstaked 90 million BICO and deposited to Gate.io near local price tops."
- **suggested manual fix:** Check if `insider_activity` catalyst type (present in June 20 cycle_22-23) captured any BICO entry. If not, consider whether on-chain alert feed (Lookonchain) coverage of BICO is sufficient.
- **priority:** medium
- **first observed:** 2026-06-21 04:39 EEST

### TODO-ALICE-OPEN-SQUEEZE-RISK
- **issue:** ALICE intraday B-tier long shows as TRIGGERED/OPEN in active-signals despite +54.5% squeeze move with no verified catalyst. Open position in a pure-squeeze name on weekend thin liquidity = elevated risk.
- **evidence:** active-signals CLI row 8: "AL... B intraday long triggered 0.xxx" with ALICE at +54.5% and funding -0.003 to -0.009.
- **suggested manual fix:** Manual review session: check ALICE current price vs TP1, current funding, whether squeeze is exhausting. Consider early close if price >2ATR from EMA20 and funding normalizes. Add squeeze detection check to position-open criteria.
- **priority:** high
- **first observed:** 2026-06-21 04:39 EEST
