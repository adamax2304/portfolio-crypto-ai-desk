# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

## 1. Executive Summary

Overnight/Asia slot (04:30 EEST). **Advisory only — no auto-trade, no code/scoring changes.** Stocks are closed (Saturday) — treat all stock signals as planning/watchlist only. Crypto tape stayed bullish-trend/risk-on overnight (BTC + ETH uptrend, breadth 70.7%/75.6% above EMA20/EMA50), but the macro overlay is pinned at 100/100 risk-off (an active, ongoing **Coldcard hardware-wallet exploit** — verified via WebSearch: ~1,816 BTC / ~$116M drained from 5,200+ addresses since 2026-07-30 — plus fresh US sanctions on Iranian crypto exchanges). Net call: **cautious risk-on**, not risk-off — external sources confirm BTC has stayed firm/resilient through the hack headlines. No A-tier signals on either asset class (weekend-mode caps intraday/scalp at B). The desk's own stats confirm **swing is the working crypto edge this week** (PF 5.46, 13W/9L) while **scalp is structurally losing again** (0W/4L closed, avgR −0.086, n=36) — consistent with the standing scalp kill-switch candidate. A real contradiction surfaced this run: three currently-open swing **longs (ZBT, STG, SYN)** are tagged **bias=short** with negative 24h returns (−42.8%, −11.7%, −10.0%) in the freshest intraday scan — flagged for manual review, not new size. Untracked-legacy-alert count is **0** today (prior-cycle TODO-3 not recurring this run). Catalyst mapping 53.4% (just under the 50%-unmapped "weak" threshold) — usable as context.

## 2. Data Used

- `data/reports/scalp/2026-08-08_00-03_scalp_report.md` (Aug 8 03:03 EEST) — fresh (~1.6h old)
- `data/reports/intraday/2026-08-08_00-15_intraday_report.md` (Aug 8 03:15 EEST) — fresh (~1.4h old), freshest report this cycle
- `data/reports/swing/2026-08-07_21-42_swing_report.md` (Aug 8 00:42 EEST) — ~4h carry-forward, flagged
- `data/reports/stocks/intraday/2026-08-07_20-57_stocks_intraday_report.md` (Aug 7 23:57 EEST) — market closed weekend, planning-only
- `data/reports/stocks/swing/*`, `stocks/invest/*` — last generated 2026-07-02, retired/deprecated, excluded
- `data/catalysts/2026-08-08/catalyst_events.jsonl`, `narrative_baskets.jsonl`, `catalyst_cycle_00-27.md` (Aug 8 03:27 EEST)
- `data/processed/llm_analysis_packet.md` (03:22 EEST), `data/processed/llm_stocks_packet.md` (00:02 EEST, weekend-stale — stocks planning-only anyway)
- `active-signals --asset-class crypto` (50 rows) / `--asset-class stocks` (50 rows, all C-tier waiting_for_entry)
- `signal-stats --asset-class crypto` and `--asset-class stocks`
- `detect_untracked_legacy_alerts --since 2026-08-08` → 0 untracked
- `data/scheduled_runs/2026-08-07_default_schedule/cycle_02_02-52_summary.md` (mtime 03:55 EEST) — market intelligence health, latency SLA, news source health, paper operational audit sections
- Direct read-only SQL on `db/crypto_ai_desk.sqlite`: `news_items` (24h symbol lookups for ACE/XRP/ZBT/STO), `catalyst_events.jsonl` mapping stats
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_2325.md` (post-close, 23:25 EEST)
- 2 WebSearch queries (Coldcard exploit verification; BTC/ETH price snapshot) — both used, no WebFetch needed (search results were sufficiently sourced and dated)

External web research **was** available this cycle.

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-08-07_default_schedule/scheduler.log` — mtime **Aug 8 03:55 EEST** (~44 min old at review start) → **fresh**, review proceeds (well under the 3h defer threshold on both scheduler.log and latest cycle summary).
- Latest cycle summary `cycle_02_02-52_summary.md` (mtime 03:55 EEST) — all 48 steps `[OK]`, exit=0. No step failures this cycle.
- Crypto scalp report: 03:03 EEST → fresh.
- Crypto intraday report: 03:15 EEST → fresh, freshest this cycle.
- Crypto swing report: 00:42 EEST, ~4h old → carry-forward bucket (4–12h); regime read cross-checked against fresher scalp/intraday reports — consistent (bullish trend, uptrend BTC/ETH both times).
- Stocks intraday report: Aug 7 23:57 EEST → stale relative to now but market is closed (Saturday) — used as planning/watchlist context only, not treated as a data-quality failure.
- Stocks swing/invest: retired since 2026-07-02 — excluded, not a freshness problem (deliberate deprecation, see [[project_crypto_ai_desk_stocks_position_framework]]).
- Market intelligence health monitor (00:44 EEST run): `status: ok`, 0 issues, all context sources (cross-exchange quotes, Deribit DVOL, SEC Form4, stablecoin pegs) reporting `ok`.
- News source health: OK 42 · DEGRADED 0 · ERROR 3 · STALE 0 · DEAD 0 (alerts_sent 1). News entity resolver: 100% resolved, 0 unresolved symbol-tagged rows.
- News quality gold/replay gate: **READY=False** (gold 31/31, but `primary_source_error_dead=2`, `mapping_gap=1`) — not a blocker for this review, but a standing data-quality note.
- Latency: crypto acceptance = **SLA_BREACH**, stocks intraday acceptance = **SLA_BREACH** (both already tracked under [[project_crypto_ai_desk_latency_layer]] — general live promotion stays blocked; not new this cycle).
- Monitors: crypto watchlist monitor, crypto pending monitor, MEXC canary monitor, derivatives monitor, fast Finnhub news monitor, telegram dashboard callbacks all reported `[OK]` / continuous-background this cycle.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-08 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 44min old, cycle_02 all 48 steps OK", "swing report ~4h old (carry-forward bucket, cross-checked consistent)", "market intelligence health status=ok, 0 issues", "news quality gate READY=False (primary_source_error_dead=2) — standing, not new"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC+ETH uptrend, breadth 70.7%/75.6% above EMA20/50", "macro risk score 100/100 risk-off overlay (Coldcard exploit ~$116M, Iran sanctions)", "WebSearch confirms BTC firmed through the hack headlines (soft jobs report, Hormuz de-escalation tailwind)", "weekend mode active — thinner liquidity, A-tier margin penalty, chase-entry downgrade"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "no_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 53.4% (267/500), just under the 50%-unmapped weak threshold", "3 active narrative baskets: rwa_narrative (ONDO/XLM), binance_ecosystem_teaser (BNB/ASTER), perps_dex_narrative (HYPE/DYDX/GMX/ASTER)", "ACE/USDT, ZBT/USDT, STO/USDT — 0 fresh (24h) news_items rows each, pure technical/momentum setups"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable", "oi_contradicts"], "data_missing": ["OI 24h% for most active symbols shows n/a"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BICO/USDT negative funding across bybit/okx/mexc, crowding=elevated on cross-check despite being long-biased in reports", "ZBT/USDT price down + OI down = deleveraging/long-liquidation signature", "HEI/USDT price up + OI down = short covering, weaker continuation quality"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "clean_retest", "overextended"], "data_missing": ["TradingView / manual chart check unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BICO/EPIC/TUT/TST 24h moves of 20-61% already triggered — chase risk on fresh entries", "weekend-mode intraday requires retest after impulse and RR>=1.2 to TP1", "ACE/USDT (score 79.3) and STO/USDT (78.1) are the highest-scoring active B-tier swings, both triggered days ago, no fresh entry available"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 50 rows, 0 A-tier, all B-tier; ~34 triggered/open, ~4 waiting_for_entry, ~7 tp1/tp2_hit (partial), rest scalp entered-unresolved or expired-window", "stocks active-signals: 50 rows, all C-tier waiting_for_entry, market closed", "detect_untracked_legacy_alerts: 0 today (prior-cycle TODO-3 not recurring)"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": ["correlation_cluster", "reduce_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["3 open swing LONGS (ZBT, STG, SYN) tagged bias=short with negative 24h (-42.8%/-11.7%/-10.0%) in freshest intraday scan — contradiction cluster, recurring theme from prior review's ZBT flag", "crypto intraday long 7d: PF 0.856, WEAK_PROFIT_FACTOR warning, PNL_CONCENTRATED_TOP3=0.889", "weekend signals underperform: winrate 5%, n=25 (system observation)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing mode: PF 5.46, 13W/9L, avgR +0.42 (n=56) — working edge", "crypto intraday mode: PF 1.68, 12W/27L, avgR +0.24 (n=74) — moderate, winrate 15% flagged 'low' by system observation", "crypto scalp mode: PF 0.17, 0W/4L, avgR -0.086 (n=36) — structurally losing, standing kill-switch candidate", "stocks intraday: 209 triggered, 2W/12L, PF 0.17, avgR -0.23 — known issue, C-tier never actionable per [[project_crypto_ai_desk_stocks_intraday_hardening]]"] },
    { "agent": "head_trader", "verdict": "ok",
      "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents below"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "ACE/USDT", "trigger": "already triggered (swing, score 79.3); re-add on a clean pullback to 0.0977-0.1284 zone with volume confirmation, not on a fresh chase" },
    "best_short_candidate":    { "symbol": "ZBT/USDT", "trigger": "no fresh short signal live; watch for a confirmed breakdown/retest below 0.1253 (existing swing invalidation) before considering a tactical short — do not add size to the open longs" },
    "best_catalyst_candidate": { "symbol": "BNB/USDT or ASTER/USDT", "trigger": "binance_ecosystem_teaser basket (fresh <6h); wait for a clean breakout/retest on either name before treating as actionable, no live signal yet" },
    "avoid_candidate":         { "symbol": "ZBT/USDT, STG/USDT, SYN/USDT (open longs)", "reason": "bias=short + negative 24h in freshest scan while desk holds open long swings — contradiction, manual review before adding risk" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | risk_on, longs_preferred, mixed | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, catalyst_confirmed, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable, oi_contradicts | advisory_only |
| technical_entry | caution | 0.55 | entry_late, clean_retest, overextended | advisory_only |
| execution_lifecycle | needs_review | 0.75 | open_actionable, waiting_for_entry, entered_unresolved | advisory_only |
| risk_manager | manual_review | 0.60 | correlation_cluster, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_2325.md` (post-close, 23:25 EEST):

- **Untracked legacy alerts: 6 → 0.** Prior review flagged TODO-3 recurrence (ALLO ×3, ADA, BICO, ACE) at a worsening trend. This cycle's `detect_untracked_legacy_alerts --since 2026-08-08` returns **0**. Improvement, but the root cause (stale-signal-reuse on watchlist re-fire) was not code-fixed — this is likely quiet overnight volume, not a resolution. Keep watching next cycle.
- **TODO-5 (missing cycle_*_summary.md) appears resolved.** `2026-08-07_default_schedule/` now has 2 summary files (`cycle_01_22-56`, `cycle_02_02-52`), unlike the gap flagged at 23:25 EEST. Downgrading this TODO to resolved/monitor.
- **ZBT/USDT contradiction persists and has grown.** Prior review flagged ZBT as tagged short-bias/-34.2% 24h while desk held 2 open swing longs. This run: ZBT is now -42.8% 24h and **two more symbols (STG, SYN) show the same pattern** (open long, bias=short tag, negative 24h). This is now a 3-symbol correlation cluster, not an isolated case — escalating from a single-symbol note to a TODO (see §14).
- **New macro catalyst since last review:** the Coldcard hardware-wallet exploit (verified externally) has grown from prior-review's passing "risk events" mention to the top-importance catalyst line (`0.84` BTC/USDT exploit_hack) this cycle — but external sources confirm BTC price has stayed resilient (jobs report tailwind, Hormuz de-escalation), consistent with the desk's own bullish-trend regime read. Thesis not invalidated, risk overlay stays elevated.
- **Scalp mode still structurally losing** (0W/4L, avgR -0.086, n=36) — same standing issue, no new evidence either direction.
- **Swing remains the working edge** (PF 5.46 this window vs PF 6.83/5.80 in recent prior windows) — consistent, still the primary actionable crypto lane.

## 5. Catalyst Coverage

- Total catalyst events today: **500**
- Mapped (non-null symbol): **267** (53.4%)
- Unmapped: **233** (46.6%)
- Narrative baskets: **3** (rwa_narrative, binance_ecosystem_teaser, perps_dex_narrative)
- By type: other_news 457, earnings_event 13, partnership 11, regulatory_sector_headline 5, exploit_hack 5, analyst_action 5, legal_risk 3, platform_growth 1.
- 46.6% unmapped is **just under** the 50% "weak this run" threshold — usable as context, but treat with caution, not as a primary decision driver. Top unmapped headlines (sample):
  1. Tradfin geopolitical wire (Ukraine/Black Sea oil terminal, no symbol resolver hit)
  2. "PNR Investors Have Opportunity to Lead Pentair plc Securities Fraud Lawsuit" (law-firm investor-alert format, trailing-ticker pattern — same class of miss as prior-review TODO-6)
  3. "Ant Group's Ling 3.0 Flash" (AI model news, no crypto/stock symbol mapping expected)
  4. "Russia shuts down 9 crypto exchanges in major Moscow crackdown" (regulatory, no single symbol)
  5. "Why Redwire Stock Keeps Gaining" (stock ticker embedded in prose, resolver miss)

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **cautious risk-on** — BTC/ETH uptrend, breadth 70.7%/75.6% above EMA20/50, but macro risk overlay pinned 100/100 (Coldcard exploit + Iran sanctions). Technical regime and headline risk disagree; technical + external price action (BTC holding ~$65k through the hack news) wins the tiebreak.
- Stocks mood: **closed (weekend)** — all 50 active stock signals are C-tier `waiting_for_entry`; planning/watchlist context only until Monday RTH.
- Dominant narrative: RWA/tokenization (ONDO/XLM, multi-week thesis) and a fresh Binance-ecosystem teaser (BNB/ASTER, <6h) are the two live baskets with primary/related tickers; perps-DEX narrative (HYPE/DYDX/GMX/ASTER) flagged `wait_pullback`.
- Preferred side now: **longs, selective** — prefer pullback/retest entries on RS-leaders per weekend-mode rules; avoid chasing the 20-61% 24h movers already triggered (BICO/EPIC/TUT/TST).
- Best long candidate: **ACE/USDT** (score 79.3, highest-scoring active B-tier swing, already triggered — watch for a pullback re-entry, not a chase).
- Best short candidate: **none clean right now** — ZBT/USDT is the closest on data (bias=short, -42.8% 24h) but the desk already holds open longs on it; a fresh short would need a confirmed breakdown below its own swing invalidation (0.1253) with volume, not just the current tag.
- Best catalyst-backed candidate: **BNB/USDT or ASTER/USDT** on the binance_ecosystem_teaser basket (fresh <6h) — no live actionable signal yet, watch for breakout/retest.
- What to avoid: adding size to **ZBT/STG/SYN** open longs while they carry a fresh bias=short + negative-24h tag; chasing any of the 20-61% 24h movers already triggered without a retest.
- What would change the view: a confirmed BTC breakdown below its current uptrend structure, a material escalation in Coldcard-exploit-driven exchange-level contagion (beyond self-custody), or ZBT/STG/SYN breaking their swing invalidation levels (would convert the "contradiction" into a clean stop-out).

## 7. Candidate Deep Dives

### 1. ZBT/USDT — open swing longs vs. fresh short-bias tag (contradiction risk, manual review)
- Status: 2 open swing longs (`sig_0be20040e229aec5` entry 0.1407-0.1491/inval 0.1253/exp 2026-08-14; `sig_66ffd2ccca900b8f` entry 0.1573-0.1626/inval 0.1510/exp 2026-08-13), triggered. Plus 1 scalp `tp1_hit` (already partial-won, older).
- Has price already reacted to the catalyst? No specific ZBT catalyst found (0 fresh news_items in 24h) — this is a pure technical divergence, not news-driven.
- Is the setup chasing? N/A — no new entry being proposed here, this is a hold-review.
- Retest/pullback structure? Unknown — TradingView/manual chart check unavailable, using only local OHLCV/derivatives fields.
- Overextended? Derivatives note: "price down + OI down: deleveraging or long liquidation" (funding -0.00053, OI 24h -24.94%, long/short 0.751) — consistent with continued long unwind, not a base being built.
- Would entry now be late? Not evaluating new entry — this is a manage-existing-risk item.
- Actionable now or after confirmation? The two open longs stay open per system rules (no auto-trade); flagging for **human review of whether these should be manually reassessed**, not for any automated action.
- Aligned with market mood? No — contradicts the "prefer RS-leader longs" mood guidance; ZBT is currently the weakest tagged name in the active book.
- Chase-risk? N/A (existing position, not new).
- Catalyst confirmation or contradiction? No catalyst; the -42.8% 24h / bias=short technical tag directly contradicts the long thesis these positions were opened under.
- **Verdict: manual review required.** Do not add size. Watch invalidation levels (0.1253 / 0.1510).

### 2. STG/USDT + SYN/USDT — same contradiction pattern, smaller magnitude
- STG/USDT: 1 open swing long (`sig_810809c2b4987589`, score 69.1, entry 0.1398-0.1441, inval 0.1363, exp 2026-08-14), tagged bias=short/-11.70% 24h in the freshest intraday scan.
- SYN/USDT: 1 open swing long (score 66.0, entry 0.1250-0.1289, inval 0.1201, exp 2026-08-13) + 1 intraday `tp2_hit` (already won), tagged bias=short/-10.01% 24h.
- Same read as ZBT: no fresh catalyst for either symbol (0 news_items rows, 24h), pure technical divergence between the open-long thesis and the freshest regime tag.
- Magnitude is smaller than ZBT (-10 to -12% vs -42.8%) — lower urgency, but the pattern repeating across 3 names in one scan is itself the finding (correlation cluster, not 3 independent noise events).
- **Verdict: watch, not yet at invalidation.** Group with ZBT for a single manual review pass rather than treating as 3 separate items.

### 3. ACE/USDT — best long candidate (already triggered, watch for pullback re-entry)
- Active: 3 signals — swing `triggered` score 79.3 (entry 0.1204-0.1284, inval 0.1106, exp 2026-08-13), swing `triggered` score 68.5 (entry 0.0977-0.1017, inval 0.0928, exp 2026-08-13), intraday `tp2_hit` (already won, score 68.3).
- No fresh catalyst (0 news_items in 24h) — pure RS/momentum setup, playbook `crypto_swing_narrative_rs_momentum` (the desk's strongest playbook this window, PF 5.46-5.80 range recently).
- Has price already reacted? Yes — both open entries are below current highs implied by the score; a fresh chase at current levels would be late.
- Retest structure? Not verifiable without chart access — flagging chart-check unavailable.
- Actionable now or after confirmation? The two existing swings stay open per normal rules; a **new** add would need a pullback into the 0.098-0.128 zone with volume, not a market chase.
- Aligned with mood? Yes — RS-leader long in a risk-on-leaning tape, no headline risk on this name specifically.
- Invalidates if: 1h close beyond the swing invalidation levels (0.0928 / 0.1106).

### 4. STO/USDT — second-highest active B-tier swing score
- Active: 1 open swing long, score 78.1, entry 0.0405-0.0416, inval 0.0392, exp 2026-08-11.
- No fresh catalyst found for STO in 24h news_items.
- Score is close to the A-tier threshold (80) but weekend-mode's A-tier margin penalty (-5.0) means this would not clear A-tier even at a slightly higher raw score right now — consistent with system design, not an anomaly.
- No contradiction signal found (not in the "Weakest Symbols" list) — held position is currently clean.
- **Verdict: hold, no action needed.** No new entry signal live.

### 5. XRP/USDT — only live short in the active book
- Active: 1 swing short, score 67.4, status `tp1_hit` (already partial-won), entry 1.0598-1.0610, inval 1.0626, exp 2026-08-08 (expires today).
- News context: 3 fresh (24h) items, all regulatory-flavored ("XRP at a Crossroads as Senate Punts on Clarity Act") — mildly consistent with continued short-side overhang (regulatory delay = uncertainty, not a bullish catalyst), but not a decisive confirmation either way.
- Already tp1_hit and expiring today — this is a **closing-out** watch item, not a fresh short idea. No action needed beyond normal tracking.

## 8. Best Candidates Ranked

1. **ACE/USDT (long-watch)** — highest-scoring active B-tier swing (79.3), RS-leader, working playbook. Trigger for a fresh add: pullback into 0.098-0.128 with volume confirmation, not a chase at current levels.
2. **STO/USDT (long-watch, hold)** — clean second-highest B-tier (78.1), no contradiction flags, no new entry live.
3. **BNB/ASTER (catalyst-watch)** — binance_ecosystem_teaser basket, fresh <6h. Trigger: confirmed breakout/retest on either name before treating as actionable.
4. **ZBT/USDT (short-watch, conditional)** — no live short signal; would need a confirmed breakdown below 0.1253 with volume before this becomes an actionable short idea. Currently more of a "review the open longs" item than a short opportunity.
5. **XRP/USDT (closing watch)** — tp1_hit swing short expiring today, regulatory overhang context only, no fresh action needed.

## 9. Avoid / No Trade

- **This decision window only** — never a system-wide stop. Scanning, tracking, and candidate generation continue unchanged.
- Avoid adding size to **ZBT/STG/SYN** open longs given the fresh bias=short + negative-24h contradiction (see §7.1-7.2).
- Avoid chasing the 20-61% 24h movers already triggered this cycle (BICO, EPIC, TUT, TST, MMT, ALLO, HEI) without a retest — weekend-mode rules explicitly require retest confirmation after an impulse move.
- Avoid treating any stocks signal as actionable before Monday RTH — market is closed, all 50 active stock signals are C-tier planning-only.
- Avoid over-weighting the 46.6%-unmapped catalyst layer as a primary decision input this cycle.

## 10. Main Risks

- **Coldcard exploit contagion risk** — currently framed as a self-custody/hardware-wallet issue (~$116M, 5,200+ addresses), not an exchange-level or systemic event. Watch for escalation (e.g., exchange-level freezes, broader FUD cascade) that could flip the "cautious risk-on" read to genuine risk-off.
- **ZBT/STG/SYN correlation cluster** — 3 open longs now tagged bias=short with negative 24h in the same scan; if this reflects a genuine regime shift in these names (vs. noise), the desk is carrying stale directional risk on ~3 open swing positions.
- **Weekend liquidity** — Weekend Mode active, wider wicks expected, tight stops can be hit on noise; system already applies the standard overlay (A-tier margin penalty, chase-entry downgrade, retest requirement).
- **Latency SLA breach (crypto + stocks intraday)** — standing issue, general live promotion stays blocked; not new this cycle but still open.
- **Scalp mode** — 0W/4L this window, avgR -0.086; continues to look like the standing kill-switch candidate flagged in prior reviews.

## 11. Action Plan — next 4 hours

1. Manual review of ZBT/STG/SYN open longs against their invalidation levels (0.1253/0.1510 ZBT, 0.1363 STG, 0.1201 SYN) — no automated action, human judgment call on whether the bias=short tag changes the risk picture.
2. Watch ACE/USDT and STO/USDT for a clean pullback/retest before considering any fresh add — do not chase current levels.
3. Watch BNB/USDT and ASTER/USDT for a breakout/retest on the binance_ecosystem_teaser basket.
4. Monitor Coldcard-exploit headlines for any exchange-level escalation that would change the "cautious risk-on" read.
5. No stocks action until Monday RTH — all 50 active stock signals stay planning-only.

## 12. Final Verdict per Mode

- **Crypto scalp:** avoid new adds — structurally losing this window (0W/4L, PF 0.17). Standing kill-switch candidate, not a new call.
- **Crypto intraday:** selective — moderate edge (PF 1.68) but weekend-mode chase-risk is high on names that already moved 20-61% in 24h; require retest.
- **Crypto swing:** primary actionable lane (PF 5.46) — best long-watch is ACE/USDT on a pullback; manage the ZBT/STG/SYN contradiction cluster before adding new swing risk.
- **Stocks (all modes):** planning/watchlist only — market closed until Monday RTH.

## 13. Sources

- [The Largest Hardware Wallet Exploit of 2026: Inside the USD 116 Million Coldcard Hack](https://www.trmlabs.com/resources/blog/the-largest-hardware-wallet-exploit-of-2026-inside-the-usd-116-million-coldcard-hack) — TRM Labs, accessed 2026-08-08
- [BTC news: Coldcard urges users to move bitcoin as active wallet exploit continues](https://www.coindesk.com/tech/2026/08/04/coldcard-urges-users-to-move-bitcoin-as-active-wallet-exploit-continues) — CoinDesk, 2026-08-04
- [Hackers steal over $130M by exploiting bug in offline hardware wallets](https://techcrunch.com/2026/08/04/hackers-steal-over-130-million-by-exploiting-bug-in-offline-hardware-wallets/) — TechCrunch, 2026-08-04
- [Bitcoin and ethereum prices today, Friday, August 7, 2026: Crypto prices moving higher following July jobs report](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-august-7-2026-crypto-prices-moving-higher-following-july-jobs-report-131451960.html) — Yahoo Finance, 2026-08-07
- Internal: `data/catalysts/2026-08-08/catalyst_cycle_00-27.md` — BTCPay/Coldcard exploit_hack catalyst entries (importance 0.81-0.84)
- Internal: `data/scheduled_runs/2026-08-07_default_schedule/cycle_02_02-52_summary.md` — market intelligence health, latency SLA, paper operational audit

## 14. Fix Requests / TODO

### TODO-3 (carry-forward, updated — improved this cycle, root cause still open)
- **issue:** Untracked legacy alerts (stale/closed `signal_id` reused on watchlist re-fire instead of minting a new `proposed_signal`) — count was 6 at the 23:25 EEST review, is **0** this cycle.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-08` → "None. Every legacy crypto alert has a backing proposed_signal."
- **suggested manual fix:** root cause (per [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]) is unaddressed in code — this looks like a quiet-overnight-volume effect, not a fix. Keep tracking across the next few cycles before downgrading priority.
- **priority:** high (unchanged — recurrence risk remains)
- **first observed:** 2026-07-17 (0 recurrence confirmed 2026-08-08 04:39 EEST)

### TODO-5 (carry-forward — appears resolved)
- **issue:** `2026-08-07_default_schedule/` was missing `cycle_*_summary.md` files as of the 23:25 EEST review.
- **evidence:** folder now contains `cycle_01_22-56_summary.md` and `cycle_02_02-52_summary.md`, both populated and referenced in this review.
- **suggested manual fix:** none needed — appears self-resolved. Recommend closing this TODO if it doesn't recur for one more full day cycle.
- **priority:** low (downgraded from medium)
- **first observed:** 2026-08-07 18:39 EEST; resolved-pending-confirmation 2026-08-08 04:39 EEST

### TODO-6 (carry-forward)
- **issue:** Catalyst symbol resolver still misses trailing-ticker / prose-embedded-ticker headline formats (law-firm investor-alert wires, "Why X Stock Keeps Gaining" style headlines).
- **evidence:** `data/catalysts/2026-08-08/catalyst_events.jsonl` — 233/500 (46.6%) unmapped this cycle; sample unmapped titles in §5 include the same "PNR Investors... Securities Fraud Lawsuit" pattern and a new "Why Redwire Stock Keeps Gaining" prose-ticker case.
- **suggested manual fix:** unchanged from prior finding — add a resolver pattern for trailing-ticker law-firm wire titles and prose-embedded-ticker stock headlines; re-run mapping stats after the fix.
- **priority:** low
- **first observed:** 2026-08-07 23:25 EEST

### TODO-7 (new)
- **issue:** 3 currently-open crypto swing longs (ZBT/USDT, STG/USDT, SYN/USDT) are simultaneously tagged `bias=short` with negative 24h returns (-42.8%, -11.7%, -10.0%) in the freshest intraday regime scan. This is a correlation cluster, not an isolated case — ZBT alone was flagged in the prior review, but the pattern has now spread to 2 more names in one scan.
- **evidence:** `data/reports/intraday/2026-08-08_00-15_intraday_report.md` §2 "Weakest Symbols" lists ZBT/STG/SYN as `bias short`; cross-referenced against `active-signals --asset-class crypto` showing all 3 as open `triggered` swing longs (`sig_0be20040e229aec5`, `sig_810809c2b4987589`, `sig_e349c3ae6bb7da8d` / related IDs).
- **suggested manual fix:** investigate whether the regime/bias-tagging logic and the open-position tracker are reading from consistent data, or whether this reflects a genuine late-stage reversal on these 3 names that the position-management layer doesn't act on (by design, since the desk is read-model/advisory for existing positions). A human session should decide whether these need manual intervention.
- **priority:** medium
- **first observed:** 2026-08-08 04:39 EEST (ZBT precursor first flagged 2026-08-07 23:25 EEST)
