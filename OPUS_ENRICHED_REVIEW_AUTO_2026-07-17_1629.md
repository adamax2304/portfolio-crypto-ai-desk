# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:29 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (16:20 EEST assignment, dispatched ~16:24-16:29, ~1-6min before/around the US cash open at 16:30 EEST / 9:30 ET — treat as the final pre-open read, the first minutes may already be live by the time this is delivered). **Advisory only — no auto-trade, no code/scoring/routing changes.** Pipeline healthy: `scheduler.log` mtime 14:29 EEST, latest `cycle_05_13-53_summary.md` mtime 14:29 EEST (~1h55m old at review start) — both under the 3h defer threshold, **not deferred**. Crypto scalp/intraday fresh (generated 11:01/11:07 EEST content-time, file mtime 14:01/14:07 EEST, ~2h20-25m old). Stocks intraday fresh (11:23 EEST content-time, file mtime 14:23 EEST, ~2h old) and explicitly headered `MARKET CLOSED — planning/watchlist only` at generation time — it is the freshest available read for the open.

**Dominant story this cycle: an escalating US-Iran military conflict is the macro driver going into the open.** Macro risk score is **96/100** (up from 86/100 at the 11:30 review) — confirmed fresh as of ~13:56 EEST (33min before this review): US strikes expanding to Syria/Bahrain, Iranian IRGC strikes/claims on US bases in Oman and Qatar, missile strikes on a US command center in Syria, oil prices rising on Strait-of-Hormuz supply risk, bond markets bidding up safe-haven demand. This is risk-off for crypto (BTC/ETH `transition_down`/`range`, altcoin breadth only 21.4% above EMA20) but a **real, verified tailwind for the energy sector** (XLE mixed/strong, oil-linked names surging — PBF Energy +116% in 2026 cited). **Crypto**: no fresh A/B signals this cycle; TAO/USDT's swing short (yesterday's cleanest actionable idea) was **stopped out** (CLOSED LOSS) since the last review. ONDO/USDT (B, intraday, long) is TP1+TP2 hit but has been sitting **~5h past its hard `expires_at`** (2026-07-17T08:36:31 UTC) while still showing `tp2_hit` — a lifecycle/terminalization gap, flagged as TODO-10 (crypto-side instance of the already-open TODO-2). **Stocks**: pre-open, all ideas gate-demoted to C by the market-closed guard; the two strongest pre-gate-A ideas are **AVGO short** (score 89.62, semis-weakness thesis reinforced by yesterday's Marvell -8% AI-capex-slowdown selloff) and **XOM long** (score 89.44, now further reinforced by the fresh, verified oil-price catalyst from the Iran conflict) — both need RTH confirmation, not a pre-open chase. **MSFT** stays **AVOID/MANUAL REVIEW** on a recurring active securities-fraud lawsuit headline (2026-07-16T19:43 UTC, ~19h old, still fresh).

**Catalyst mapping is weak this run (82.0% unmapped, 2051/2500)** — unchanged in substance from the last two reviews (84%, 82.8%), use as directional context only, consistent with the known catalyst-linkage gap already logged in project memory. **System-integrity issues unchanged, still high-priority**: untracked legacy alerts still show the same 2 unresolved symbols (ALLO/USDT, BANK/USDT — TODO-3), and `mexc_canary_monitor` is still crash-looping on the same `database is locked` error on its kill-switch write path (TODO-8, live-execution safety component, not touched by this advisory review). Scanning, tracking, and all monitors continue unaffected — **no recommendation to pause anything.**

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-17_11-01_scalp_report.md` (mtime 14:01 EEST, ~2h28m old), `data/reports/intraday/2026-07-17_11-07_intraday_report.md` (mtime 14:07 EEST, ~2h22m old), `data/reports/swing/2026-07-17_01-03_swing_report.md` (mtime ~04:03 EEST content-time, >14h old — **stale**, excluded from primary regime read, mentioned only for continuity), `data/reports/stocks/intraday/2026-07-17_11-23_stocks_intraday_report.md` (mtime 14:23 EEST, ~2h old, generated pre-open, `MARKET CLOSED — planning/watchlist only` header).
- Catalyst: `data/catalysts/2026-07-17/catalyst_events.jsonl` (2500-row rolling buffer, 449 mapped / 2051 unmapped), `narrative_baskets.jsonl` (6 baskets), `data/catalysts/2026-07-17/catalyst_cycle_11-09.md` (latest cycle, mtime 14:09 EEST, already present, no re-scan needed).
- LLM packets: `data/processed/llm_analysis_packet.md` (~2h22m old), `data/processed/llm_stocks_packet.md` (~2h old).
- DB (direct SQL, `db/crypto_ai_desk.sqlite`): `proposed_signals` (TAO history — confirmed `stopped`; ONDO current row — confirmed `tp2_hit`, expiry ~5h in the past), `market_dashboard_snapshots` (latest row, 11:16 EEST), `news_items` (Iran/Gulf/oil freshness cross-check, MSFT legal-risk freshness cross-check, AVGO/XOM/AMD/GOOGL/SMCI/QQQ/AAPL headline sweep).
- CLI: `active-signals` ×2 (crypto: 1 row [ONDO]; stocks: 50 rows), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-17` (0 new today) and `--since 2026-07-16` (2 unresolved, unchanged).
- Scheduler: `data/scheduled_runs/2026-07-17_default_schedule/scheduler.log`, `cycle_05_13-53_summary.md`; `mexc_canary_monitor_1784285654.log` (latest, same traceback as prior reviews).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-17_1145.md` (11:45 EEST, Europe/pre-US slot) — used for TODO carry-forward (TODO-1..9), thesis tracking (TAO/ONDO/AVGO/XOM/MSFT), and integrity-issue history.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **14:29 EEST**, latest `cycle_05_13-53_summary.md` mtime **14:29 EEST** (~1h55m old at review start) — both under 3h, **not deferred**.
- Crypto scalp/intraday: fresh (~2h20-28m old, inside normal cycle cadence).
- Crypto swing: **stale** (>14h old per the freshness rule) — excluded from primary regime read this cycle; no fresher swing source exists so it is not cited for any new thesis.
- Stocks intraday: fresh (~2h old) but generated pre-open — `market_closed_intraday_planning_only` gate active on every idea; this is the correct/expected state for this slot (review fires ~10min before/around the open).
- Stocks swing/invest: last generated 2026-07-02 (15 days stale) — known-deprecated legacy framework by design, not a freshness fault; excluded.
- Catalyst directory present for today, 2500-row rolling buffer populated — no re-scan needed.
- Monitors: `mexc_canary_monitor` still **not healthy** — same `sqlite3.OperationalError: database is locked` on `ensure_tables()`/kill-switch write, confirmed in the latest same-day log (`mexc_canary_monitor_1784285654.log`). Live-execution component only; the paper-signal/scanning flow this review covers is unaffected. See TODO-8 (carried forward, unchanged).
- Dashboard snapshot (`market_dashboard_snapshots`, latest row 11:16 EEST): `crypto_market_mode=trend`, `crypto_fear_greed=27` (fear zone, unchanged), `stocks_market_mode=unknown`. No fresher snapshot since 11:16 EEST (~5h13m old) — treated as stale context only; report-level regime (`bearish trend (risk-off)`) remains authoritative. See TODO-9 (carried forward).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-17 16:29 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["swing report >14h stale, excluded from primary regime read", "dashboard snapshot ~5h13m old, treated as stale context"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle_05_13-53 both mtime 14:29 EEST, <3h", "scalp/intraday ~2h20-28m old", "stocks intraday ~2h old, pre-open by design", "stocks swing/invest 15d stale, deprecated legacy framework"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.8,
      "reason_codes": ["risk_off", "shorts_preferred", "danger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["macro risk score 96/100 (up from 86/100 at 11:30 review), driven by escalating US-Iran conflict, confirmed fresh headlines as of 13:56 EEST", "BTC transition_down, ETH range, altcoin breadth 21.4% above EMA20 (down from 25% at 11:30)", "crypto fear&greed=27 (fear zone)", "stocks: VIX 18.06 (flat vs 18.48 prior), regime label 'transition', SPY uptrend/QQQ downtrend split, energy sector real macro tailwind from oil spike"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["82.0% unmapped (2051/2500) catalyst events today — weak mapping run, same magnitude as prior two reviews (84%, 82.8%)", "ONDO: verified partnership catalyst (SBI Group, RWA tokenization), importance 0.69", "XOM: verified macro/sector catalyst (oil price rise, Iran-conflict supply risk), CNBC-sourced", "MSFT: recurring securities-fraud legal-risk headline, 2026-07-16T19:43 UTC, ~19h old, still fresh", "active baskets: rwa_narrative (ONDO/XLM), perps_dex (HYPE), ai_narrative (NEAR/RENDER/TAO/FET), binance_ecosystem (BNB/ASTER), momentum_breakout (KAITO)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "data_unavailable", "oi_contradicts"],
      "data_missing": ["stocks: no retail futures/OI data, only relative volume", "BTC/ETH-level funding/OI not separately surfaced, only altcoin-level"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOME/USDT: heavily negative funding across bybit/mexc/okx, elevated crowding, already -37.8% 24h — squeeze-prone if shorted late", "KAITO/BANK: external funding neutral across venues, crowding low — no squeeze signal either direction, momentum-only", "AIGENSYN/USDT: pipeline itself caps this short to C for 'thin_liquidity_short_squeeze_risk + late_short_after_exhaustion'"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["chase_risk", "entry_late", "stale_before_entry", "price_moved_away"],
      "data_missing": ["no live intraday tick / TradingView chart data — using local OHLCV/ATR/EMA fields only"],
      "suggested_effect": "advisory_only",
      "facts_used": ["AVGO short: entry zone 374.46-377.46, already reacted to yesterday's Marvell-driven semis selloff, ATR extension 1.77 (below the 2 ATR chase threshold but already extended)", "XOM long: fresh oil catalyst risks a gap-open at the cash open — chasing the gap is late; wait for a pullback/retest of the pre-open planning entry", "ONDO: TP1+TP2 already banked, racing TP3 vs a hard expiry that has already passed ~5h ago without terminalizing", "TAO short: closed via stop (loss), no longer active"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["entered_unresolved", "needs_review", "waiting_for_entry", "closed_flat"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: only ONDO remains (B, intraday, long) — TP1+TP2 hit, ~5h past hard expiry, still non-terminal — ENTERED UNRESOLVED / NEEDS REVIEW, not a missed entry (partial profit already locked)", "TAO/USDT swing short: confirmed CLOSED via stop in the DB (loss) since the 11:45 review", "stocks: 50 active-signals rows, all pre-open C-tier planning ideas WAITING for the 16:30 EEST open; majority are older tp1/tp2_hit rows past their mode horizon per TODO-2, not fresh", "0 new untracked legacy alerts today"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["headline_risk", "legal_risk", "correlation_cluster", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT: active securities-fraud legal/headline gate, recurring headline ~19h old, stays AVOID/MANUAL REVIEW", "correlation cluster: AVGO short + AMD short + QQQ short are all the same 'weak semis/tech' thesis — do not stack all three at full size, treat as one correlated bucket", "GOOGL earnings in 5 trading-ish days (unknown-confidence date) — reduce size / avoid new swing-length holds into it", "US-Iran conflict escalation (96/100 macro risk) is the dominant systemic risk driver into the open — reduce size / prefer defined-risk, RTH-confirmed entries only"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier week: n=122, reliable, PF 1.98, avgR 0.276, totalR +25.4 — real positive edge, low 25% winrate carried by asymmetric R", "crypto scalp remains a losing bucket: n=24, PF 0.30, avgR -0.18, totalR -3.5 — unchanged issue, TODO-6", "stocks headline A/B this week: n=14 (weak confidence), winrate 28.6%, PF 0.667, totalR -1.0; stocks C-tier watchlist also negative (PF 0.757, totalR -9.0) — consistent multi-review negative forward evidence for stocks intraday, still awaiting human sign-off per project memory"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents below"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "XOM", "trigger": "wait for the 16:30 EEST / 9:30 ET open, do NOT chase a gap-up on the oil catalyst — require the first 15-30min range to form and a clean pullback/retest hold above the pre-open planning entry (~142) before entering" },
    "best_short_candidate": { "symbol": "AVGO", "trigger": "wait for RTH confirmation of continued weakness below 374.46 after the open; do not enter on the pre-open planning zone alone — semis sector already reacted to Marvell's -8% selloff, confirm follow-through, not exhaustion-bounce" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "already active (B, intraday, long, TP1+TP2 hit) on a verified SBI Group/RWA partnership catalyst — no new entry needed; watch for TP3 (0.4017 area) or a lifecycle correction now that it is ~5h past hard expiry" },
    "avoid_candidate": { "symbol": "MSFT", "reason": "recurring active securities-fraud lawsuit headline (~19h old, still fresh) — stays AVOID/MANUAL REVIEW regardless of technical score" },
    "operator_action": "wait_for_trigger",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 9
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.80 | risk_off, shorts_preferred, danger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, data_unavailable, oi_contradicts | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, entry_late, stale_before_entry, price_moved_away | advisory_only |
| execution_lifecycle | caution | 0.65 | entered_unresolved, needs_review, waiting_for_entry, closed_flat | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, legal_risk, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Comparing to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-17_1145.md` (11:45 EEST):

- **New/removed**: TAO/USDT swing short (was the cleanest actionable idea at 11:45) is now **CLOSED via stop (loss)** — removed from active signals. No new crypto A/B signals appeared this cycle.
- **Macro escalation, not de-escalation**: macro risk score rose from 86/100 → **96/100**; the Iran-US conflict headlines got materially more severe (strikes expanding to Syria/Bahrain, direct claims on US bases in Oman and Qatar) rather than cooling off.
- **ONDO/USDT thesis unchanged but lifecycle-flagged**: at 11:45 it was noted as "racing its hard expiry" (expiry ~11:36 EEST); it is now confirmed **~5h past that expiry** while still `tp2_hit` — same idea, now an explicit data-integrity concern (TODO-10, new).
- **AVGO/XOM theses confirmed, strengthened**: both carry forward unchanged in direction and pre-gate-A score; XOM's catalyst got stronger (oil price action is now realized, not just a headline risk), AVGO's got a same-sector confirmation (Marvell -8% AI-capex-slowdown selloff spilling into AMD/Intel too).
- **MSFT avoid unchanged**: same legal/headline gate, still fresh (~19h old headline — a genuinely new instance of the recurring lawsuit story, not a stale repeat).
- **UNH contradiction**: not re-verified this cycle (no fresh UNH-specific news pulled); carried forward as unresolved context only, not re-confirmed.
- **Catalyst mapping**: 82.0% unmapped vs 82.8% at 11:45 — materially unchanged.
- **Integrity issues (TODO-3, TODO-8, TODO-9)**: all confirmed unchanged/still open this cycle via direct re-check.

## 5. Catalyst Coverage

- Total `catalyst_events` today (rolling buffer): **2500**
- Mapped (non-null symbol): **449**
- Unmapped (null symbol): **2051** (**82.0%**)
- `narrative_baskets`: **6** (rwa_narrative, perps_dex_narrative, delisting_thin_liquidity, binance_ecosystem_teaser, ai_narrative, momentum_breakout)

**Catalyst mapping weak this run — use the catalyst layer as context, not final decision.** Top 3 unmapped-style/basket-level headlines (no clean single-symbol map): "Messi's World Cup magic is moving more than just scoreboards, it's moving fan token markets" (delisting_thin_liquidity basket); "$386M in long positions liquidated in crypto market over past 24 hours" (perps_dex_narrative basket); ADMA/Photronics/Planet-Fitness/GPGI investor-deadline press-release spam (legal_risk basket, mostly noise, not desk-relevant). This matches the already-logged catalyst-linkage gap in project memory — no new root-cause finding this cycle, just confirmation the gap persists.

## 6. Market Landscape

Crypto: bearish trend / risk-off regime, BTC `transition_down`, ETH `range`, altcoin breadth 21.4% above EMA20 (weak), macro risk 96/100 dominated by the escalating US-Iran conflict. Fear & Greed 27 (fear zone). Strongest RS names today have **no verified catalyst** (KAITO +23.3%/RS+25.0% vs BTC, BANK +36.7%/RS+38.4% — both flagged "overextended"/counter-tape by the pipeline itself); weakest/short-biased names cluster around AIGENSYN, BONK, RE, HOME, TREE — all `weak_vs_market`, none catalyst-confirmed either.

Stocks: regime label "transition", bias neutral, VIX 18.06 (calm relative to the crypto-side macro read — equity vol has not yet repriced the Iran escalation as of the last data pull). Index split: SPY uptrend, QQQ downtrend, IWM range, DIA uptrend — narrow, not broad-based strength. Sector rotation: healthcare (XLV) and financials (XLF) strongest (RS vs SPY +5.7%/+4.4%), energy (XLE) mixed-but-positive (+2.9% RS, now with a live macro tailwind from the oil spike), semiconductors (SMH) and technology (XLK) weakest (RS vs SPY -7.7%/-4.8%).

### Market Mood / Risk Routing
- Crypto mood: **risk-off** (macro risk 96/100, weak breadth, no clean catalyst-backed longs)
- Stocks mood: **pre-market → transition/neutral, mixed on sector lines** (energy tailwind vs semis/tech headwind; broad index VIX has not yet caught up to the crypto-side macro read)
- Dominant narrative: **US-Iran conflict escalation** — risk-off for crypto/broad risk assets, a genuine sector-specific tailwind for energy names
- Preferred side now: **wait-for-trigger, sector-routed** (crypto: shorts-preferred if forced to pick a side; stocks: energy longs and semis/tech shorts, both RTH-confirmation-gated)
- Best long candidate: **XOM** — RTH confirmation required, do not chase the oil-driven gap
- Best short candidate: **AVGO** — RTH confirmation required, semis weakness already partly priced from yesterday's Marvell selloff
- Best catalyst-backed candidate: **ONDO/USDT** — already active, verified SBI Group/RWA partnership catalyst, TP1+TP2 banked
- What to avoid: **MSFT** (active legal/headline gate); avoid stacking AVGO+AMD+QQQ shorts as three separate full-size positions (correlation cluster, same thesis); avoid chasing KAITO/BANK crypto longs without a pullback + volume confirmation (counter-tape RS in a risk-off regime, no verified catalyst)
- What would change the view: **any Iran-US de-escalation headline (ceasefire, diplomatic breakthrough) would flip the crypto risk-off overlay quickly**; a VIX repricing higher at the open would confirm equities are catching up to the macro risk crypto is already pricing; a clean RTH close above/below the AVGO/XOM planning zones in the first 30min

## 7. Candidate Deep Dives

### AVGO (stocks, short) — best short candidate
- Pre-gate score 89.62 (A), demoted to C only by the `market_closed_intraday_planning_only` gate — a technically clean A-quality setup, not a rejected one.
- Entry zone 374.46-377.46, invalidation 380.47, TP1/2/3 365.45/359.45/350.44 (RR to TP1 1.5).
- Has price already reacted to the catalyst? Yes — Marvell's -8% AI-capex-slowdown selloff on 2026-07-16 already dragged Broadcom/AMD/Intel down together; this is a continuation setup, not a fresh break.
- Is the setup chasing? Borderline — ATR extension 1.77 (under the 2 ATR chase threshold) but already extended from the news reaction.
- Retest structure? The setup is "below prev day low" per the trade-idea agent — a breakdown-continuation read, not a clean pullback-to-resistance short.
- Actionable now or after confirmation? **After confirmation.** Wait for the open, confirm price stays below 377.46 / ideally below 374.46 in the first 15-30min rather than bouncing — a bounce would suggest yesterday's move already exhausted sellers.
- Mood alignment: aligned (semis sector RS -7.7% vs SPY, weakest sector on the desk).
- Legal/headline risk: none found (checked `news_items` last 48h — no fraud/investigation/delisting hits for AVGO).
- Correlation warning: AMD (short, score 82.46) and QQQ (short, score 82.06) are the same underlying thesis — treat all three as one correlated bucket, not three independent trades.

### XOM (stocks, long) — best long / catalyst-backed candidate
- Pre-gate score 89.44 (A), same `market_closed_intraday_planning_only` demotion to C.
- Has price already reacted to the catalyst? Partially — oil prices were already rising through the prior cycle on Strait-of-Hormuz supply-risk headlines; the risk into the open is a **gap-up**, meaning the easy move may already be priced by the cash open.
- Is the setup chasing? Will be, if entered directly on the gap. Not chasing if a pullback/retest of the planning entry holds.
- Retest structure: none confirmed yet (pre-open data only).
- Actionable now or after confirmation? **After confirmation** — wait for the first 15-30min range, prefer a retest-and-hold over chasing the open print.
- Mood alignment: strongly aligned — energy is the one sector with a verified, real (not just headline) macro tailwind today (oil price action, PBF Energy +116% cited as an extreme comp).
- Legal/headline risk: none found.
- Catalyst verification: oil-price-rise catalyst is CNBC-sourced (reputable), corroborated by multiple independent Iran-conflict headlines in the same 3h window — this clears the internal-first verification bar without needing external WebSearch.

### MSFT (stocks) — avoid / manual review
- Active securities-fraud shareholder-lawsuit headline recurring in `news_items` (PR Newswire (Stocks)): most recent instance 2026-07-16T19:43 UTC (~19h old at review time), a prior instance 2026-07-14T16:06 UTC — this is a recurring PR-Newswire investor-alert pattern (common for "shareholders who lost money" solicitation wires), not necessarily a new fraud finding, but per the routine's legal/headline-risk rule this must gate the symbol regardless of technical score.
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** — never a clean actionable while this flag is live, independent of any technical setup quality.

### ONDO/USDT (crypto, long) — catalyst-backed, needs review
- B-tier, intraday, long, TP1+TP2 hit. Entry zone was 0.365205-0.369701, invalidation 0.359709.
- Catalyst: verified partnership (ONDO Finance x SBI Group, yen-backed stablecoin tokenization of Japanese assets) — importance 0.69, single_source but consistent with a company-official announcement pattern (CryptoBriefing).
- Execution-lifecycle issue: `expires_at` was `2026-07-17T08:36:31 UTC`; as of this review (~13:29 UTC) that is **~4h53m past hard expiry** while the signal still shows `tp2_hit` (non-terminal). This is **not a missed entry** — TP1 and TP2 are already banked, real partial profit locked — but it should have terminalized (won/expired-with-partial-profit) rather than sit open. See TODO-10.
- Status for the operator: **ENTERED UNRESOLVED / NEEDS REVIEW.** No new entry to take here (position, if any, is already working); flag for a lifecycle-job check, not a trading decision.

### AIGENSYN/USDT (crypto, short) — best short-watch (no clean actionable crypto A/B)
- C-tier watchlist idea from the trade-idea agent, score 60.0 (capped from a raw 80.2 for `thin_liquidity_short_squeeze_risk` + `late_short_after_exhaustion`).
- 24h -16.85%, RS vs BTC -15.16%, volume 0.07x (below average — weak confirmation).
- No fresh verified catalyst (confirmed `catalysts: []` in the structured output).
- Watch trigger (from the pipeline's own conditional plan): failed-bounce/retest zone **0.0233-0.0235**, invalidation on a 1h close beyond **0.0238**, targets 0.0228 / 0.0223 / 0.0219.
- Chase risk: the pipeline itself flags this as a potentially late short into an already-exhausted move — do not enter on the breakdown itself, only on the defined retest failure.

## 8. Best Candidates Ranked

No clean Telegram-actionable A/B exists on either desk right at this instant (crypto: only a needs-review carry-forward position; stocks: everything gated by market-closed until 16:30 EEST). Per PART 9, the best watch-list per lane:

1. **Best long-watch: XOM** — wait for RTH confirmation, pullback/retest hold above the pre-open planning entry, do not chase the oil-driven gap.
2. **Best short-watch: AVGO** — wait for RTH confirmation of continued weakness below 374.46-377.46; avoid stacking with AMD/QQQ shorts (correlation cluster).
3. **Best catalyst-watch: ONDO/USDT** — already active/working (TP1+TP2 banked), watch TP3 (~0.4017) or a lifecycle correction given the expired-but-open status.
4. **Secondary short-watch (crypto): AIGENSYN/USDT** — failed-bounce/retest zone 0.0233-0.0235, invalidation above 0.0238.
5. **Secondary long-watch (crypto, caution): KAITO/USDT** — score 91.6, RS +25.0% vs BTC, but no verified catalyst and flagged counter-tape in a risk-off regime; only actionable after a pullback + volume-confirmation, not on the current chase.

## 9. Avoid / No Trade

This decision window only — never a system-stop signal, scanning/tracking continues in all cases.

- **MSFT** — active recurring legal/headline (securities-fraud lawsuit) gate. AVOID / MANUAL REVIEW REQUIRED.
- **HOME/USDT** — already -37.8% 24h, heavily negative funding + elevated crowding across bybit/mexc/okx, no fresh catalyst. Overextended, squeeze-prone if shorted late — avoid chasing the breakdown further.
- **BANK/USDT (chase)** — +36.7% 24h, RS +38.4% vs BTC, but explicitly tagged "overextended" by the pipeline and carries no verified catalyst; avoid entering at current levels, watch only for a clean pullback.
- **Stacking AVGO + AMD + QQQ shorts at full independent size** — same underlying "weak semis/tech" thesis; treat as one correlated risk bucket, not three.

## 10. Main Risks

- **Macro/geopolitical**: US-Iran conflict escalation (96/100 macro risk score, still intensifying as of the last confirmed headline ~33min before this review) is the dominant systemic risk into the US cash open — gap risk on both crypto and equity indices is elevated.
- **Data-freshness/gap risk**: this review's stocks data is pre-open by construction (the slot's whole purpose); the first 15-30min of RTH price action is unverified by this review and must be confirmed live before any of §7/§8's ideas are actioned.
- **Lifecycle/terminalization gap** (TODO-2, TODO-10): a meaningful and now cross-asset-class pattern of signals sitting non-terminal well past their `expires_at` — makes "active signals" counts less trustworthy at face value without cross-checking expiry.
- **Catalyst mapping weak** (82.0% unmapped): reduces confidence in any catalyst-driven read that isn't independently cross-checked (as done for ONDO and XOM this cycle).
- **Correlation risk**: the two cleanest stock ideas (AVGO short, AMD short, QQQ short) all share one sector-weakness thesis — a single "semis/tech relief bounce" scenario invalidates all three simultaneously.

## 11. Action Plan — next 4 hours

1. Do not enter AVGO/XOM (or any stocks A/B) pre-open or on the raw open print — wait for the first 15-30min RTH range and require retest/hold confirmation.
2. Watch ONDO/USDT for TP3 (~0.4017) or a stop/expiry resolution; flag to a human for lifecycle review given the ~5h-past-expiry non-terminal status (do not treat as a fresh entry either way).
3. Watch AIGENSYN/USDT only on a failed-bounce retest into 0.0233-0.0235 with confirmation; do not short the raw breakdown.
4. Treat KAITO/BANK as long-watch only pending a pullback + volume-expansion confirmation — do not chase current levels in a risk-off macro regime.
5. Re-check Iran-US conflict headlines before/at the next scheduled review (18:30 EEST, US open reaction slot) — any de-escalation materially changes the risk-routing view; continued escalation reinforces the current risk-off/energy-tailwind read.
6. No code, scoring, or scheduler changes this cycle — all findings routed to §14 TODOs for human action.

## 12. Final Verdict per Mode

- **Crypto scalp**: no trade — losing bucket this week (PF 0.30), not this-cycle-specific.
- **Crypto intraday**: wait-for-trigger — no fresh A/B; ONDO already working, needs-review not new-entry.
- **Crypto swing**: no fresh actionable; TAO closed at a loss; regime remains risk-off / shorts-preferred if a new setup appears.
- **Stocks intraday**: wait-for-trigger — market closed at data-generation time; require RTH confirmation on AVGO (short-watch) / XOM (long-watch) before any action.
- **Stocks swing/invest (legacy)**: deprecated, never actionable.
- **Stocks swing growth-breakout (new shadow framework)**: shadow-only research, 3 open candidates (UNH, MS, AAPL per the last shadow scan) — not actionable, not sized, no live/Telegram.

## 13. Sources

- [Iran says civilian infrastructure hit by latest U.S. strikes, expands attacks to Syria, Bahrain](internal news_items — CNBC Markets, 2026-07-17T10:49:50Z)
- [Oil prices rise as U.S.-Iran hostilities threaten supply through Strait of Hormuz](internal news_items — CNBC Markets, 2026-07-17T07:36:10Z)
- [Iran's Revolutionary Guards claim to target US Al Udeid Air Base in Qatar, rattling crypto and oil markets](internal news_items — CryptoBriefing, 2026-07-17T10:12:09Z)
- [PBF Energy shares surge 116% in 2026 amid US-Iran tensions, refining margin boost](internal news_items — CryptoBriefing, 2026-07-17T10:08:42Z)
- [ONDO Finance partners with SBI Group to tokenize Japanese assets using yen-backed stablecoin](internal catalyst_events — CryptoBriefing, importance 0.69)
- [Microsoft Corporation (MSFT) Shareholders Who Lost Money Have Opportunity to Lead Securities Fraud Lawsuit](internal news_items — PR Newswire (Stocks), 2026-07-16T19:43:00Z)
- [Marvell Drops 8% as AI Capex Slowdown Fears Weigh on Chips; Broadcom, AMD, and Intel Slide](internal news_items — Yahoo Finance Top Stories, 2026-07-16T16:12:07Z)
- Internal-only this cycle: no WebSearch/WebFetch was required — all cited claims cross-checked against `news_items`/`catalyst_events.jsonl` within the freshness window per §G discipline.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, unchanged)
- **issue:** Stocks intraday A/B guard combination continues to block ~100% of technically-qualified candidates via the market-closed gate (expected pre-open, but the underlying guard-calibration question from prior reviews is still open).
- **evidence:** current cycle: AVGO (89.62), XOM (89.44), AMD (82.46), GOOGL (82.06), QQQ (82.06), AAPL (80.93), SMCI (80.35) all pre-gate A, demoted to C purely by `market_closed_intraday_planning_only`.
- **suggested manual fix:** human sign-off on whether this is intentional design (it is, for pre-open data) or whether a distinct "planning A" vs "gated C" label would reduce confusion in downstream tooling.
- **priority:** low (re-confirmed as expected/by-design behavior for a pre-open slot, downgraded from medium).
- **first observed:** 2026-07-16 18:39 EEST review; re-confirmed 2026-07-17 16:29 EEST as expected-not-a-bug for this specific slot.

### TODO-2 (carried forward, unchanged — still high, see also TODO-10)
- **issue:** Many stocks signals show `expires_at` timestamps well in the past while still displaying non-terminal statuses (`tp1_hit`, `tp2_hit`, `triggered`).
- **evidence:** `active-signals --asset-class stocks` this cycle again shows numerous rows with `expires_at` days-to-weeks in the past (e.g. JPM expires 2026-07-11, COIN expires 2026-07-03, XLY expires 2026-07-10) still non-terminal.
- **suggested manual fix:** human check of the lifecycle/track-signals job for stocks (and now, per TODO-10, verify the crypto-side job too).
- **priority:** high (unchanged).
- **first observed:** 2026-07-16 16:20 EEST review.

### TODO-3 (carried forward, unchanged — still high)
- **issue:** `detect_untracked_legacy_alerts` still returns the same 2 unresolved results: ALLO/USDT (swing B, sent 2026-07-16T14:27:05 UTC) and BANK/USDT (intraday B, sent 2026-07-16T21:36:05 UTC). Zero new watchlist alerts fired since.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-16` (2 results, unchanged across 4+ consecutive reviews now).
- **suggested manual fix:** human check of the watchlist-alert re-fire path for symbols whose most recent same-mode `proposed_signal` has already closed. Note: project memory already tracks this as a confirmed bug pattern (untracked-alert signal-reuse) on ALLO/BANK, raised to high priority 2026-07-17 — this review's finding is consistent, not new.
- **priority:** high (unchanged, longest-running open item).
- **first observed:** 2026-07-16 18:39 EEST review.

### TODO-4 (carried forward, still not independently re-checked)
- **issue:** The `paper entry-mode classify` scheduler step failed (exit=1) in a 2026-07-16 cycle — not independently re-verified against today's cycles this run either.
- **evidence:** `data/scheduled_runs/2026-07-16_default_schedule/scheduler.log` (previous day, not re-read this cycle).
- **suggested manual fix:** human check whether this recurred in today's cycles.
- **priority:** low.
- **first observed:** 2026-07-16 21:39 EEST review.

### TODO-5 (resolved, informational — no action needed)
- **issue:** Dispatch-timing check.
- **evidence:** This cycle's review dispatched ~16:24-16:29 EEST against a 16:20 EEST target (~4-9min jitter) — within normal range.
- **suggested manual fix:** none; close unless a future slot fires >30min late.
- **priority:** low (informational, closed).
- **first observed:** 2026-07-17 02:45 EEST review; confirmed resolved again 2026-07-17 16:29 EEST.

### TODO-6 (carried forward, unchanged)
- **issue:** Crypto scalp mode remains a consistent losing bucket: n=24, PF 0.30, avgR -0.18, totalR -3.5 this week — unchanged from the 11:45 review.
- **evidence:** `signal-stats --asset-class crypto` this cycle, "By mode": `mode=scalp | n=24 | PF 0.300000 | avgR -0.184200 | totalR -3.5000`.
- **suggested manual fix:** human review of whether scalp should carry an explicit non-actionable label given the consistency of the negative edge.
- **priority:** medium.
- **first observed:** 2026-07-17 11:45 EEST review.

### TODO-7 (carried forward, unchanged)
- **issue:** Stocks earnings-date confidence still shows "(unknown)" for TSLA and GOOGL in today's stocks intraday report.
- **evidence:** `data/reports/stocks/intraday/2026-07-17_11-23_stocks_intraday_report.md` §3 — "TSLA: earnings in 5 trading-ish days (unknown)", "GOOGL: earnings in 5 trading-ish days (unknown)".
- **suggested manual fix:** human audit of the earnings-calendar source/ingestion for TSLA/GOOGL.
- **priority:** low-medium.
- **first observed:** 2026-07-17 11:45 EEST review.

### TODO-8 (carried forward, unchanged — still high)
- **issue:** `mexc_canary_monitor` continues crash-looping on `sqlite3.OperationalError: database is locked` inside `ensure_tables()` while writing the kill-switch control row.
- **evidence:** `mexc_canary_monitor_1784285654.log` (latest today) — same traceback at `src/live_execution/store.py:142`/`service.py:355`/`cli.py:1688` as every prior instance today.
- **suggested manual fix:** human investigation of lock contention on `db/crypto_ai_desk.sqlite` around `mexc_canary_control` writes (likely WAL-mode/timeout/concurrent-writer issue) — touches a kill-switch write path, treat with real urgency despite self-recovering via restart.
- **priority:** high (unchanged).
- **first observed:** 2026-07-17 11:45 EEST review.

### TODO-9 (carried forward, unchanged)
- **issue:** `market_dashboard_snapshots` (`crypto_market_mode=trend`, no bullish/bearish direction field visible in this cycle's read) continues to look decoupled from the fresh report-level regime classifier (`bearish trend (risk-off)`).
- **evidence:** latest snapshot row (11:16 EEST, ~5h13m old, no fresher row since) vs `data/reports/intraday/2026-07-17_11-07_intraday_report.md` line: "Market regime: bearish trend (risk-off)".
- **suggested manual fix:** human check of the dashboard-generation job's regime-classification input vs the report-level regime classifier.
- **priority:** medium.
- **first observed:** 2026-07-17 11:45 EEST review.

### TODO-10 (new)
- **issue:** ONDO/USDT (B, intraday, long, `sig_a914cdba49291324`) has an `expires_at` of `2026-07-17T08:36:31 UTC` — confirmed via direct DB check to be **~4h53m in the past** at review time — while still showing non-terminal status `tp2_hit`. This is a crypto-side instance of the exact same lifecycle/terminalization pattern already logged for stocks in TODO-2, suggesting the underlying job issue may not be stocks-specific.
- **evidence:** `active-signals --asset-class crypto` (1 row: ONDO, status `tp2_hit`, `expires_at` 2026-07-17T08:36:31); current review time ~13:29 UTC.
- **suggested manual fix:** human check whether the same lifecycle/track-signals job (or a shared terminalization path) handles both crypto and stocks, and whether it is failing/stalling for a subset of signals across both asset classes rather than stocks-only as previously scoped.
- **priority:** high.
- **first observed:** 2026-07-17 16:29 EEST review.
