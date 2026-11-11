# Opus Enriched Review — US open reaction review (weekend, no RTH) — Auto Cycle 18:39 EEST

## 1. Executive Summary

**18:30 EEST slot — US open reaction review.** Advisory only — no auto-trade, no code/scoring/strategy changes. **Critical framing: today is Saturday 2026-08-08.** There is no US cash session today or tomorrow (Sunday); the "first US-session reaction" framing does not apply literally — this run functions as a continuation/carry-forward pass over the weekend crypto tape, watching for confirmation/failure of ideas raised at 16:12 EEST, with stocks remaining planning-only until Monday RTH (2026-08-10).

**Crypto** stays **bullish trend / risk-on** at the technical level: BTC + ETH both uptrend (external check: BTC ~$65K, ETH ~$1,900-1,930, both firm off the weak July jobs report), altcoin breadth **57.5%/62.5%** above EMA20/50 — continuing the mild intraday cooling trend (66.7/74.4 at 11:45 → 60.0/67.5 at 16:12 → 57.5/62.5 now). The desk's own **macro risk score jumped back to 100.0/100** (from 86.9/100 at 16:12, driven by 6 fresh risk-off headline hits) — this **diverges** from a direct external check on the Strait of Hormuz thread specifically, which shows **de-escalation** signals in the 13:57-14:48 UTC window (Oman reporting "positive progress" in shipping talks, Iran informing the US it will allow maximum oil flow through Hormuz and will not impose transit fees, Pentagon working a safe-passage plan) — the headline-count risk score appears to be picking up breadth from other risk-off items (geopolitical intel warnings, exploit headlines), not a fresh Hormuz escalation specifically. **No A-tier signals** on either asset class (unchanged). The standing **ZBT/USDT open-long-vs-bias-short contradiction persists**, now joined by a **second symbol, NIL/USDT**, with the same pattern (open swing long vs. this cycle's own short-squeeze-capped short setup) — **ACE/USDT's version of the contradiction has resolved** (ACE is now the strongest aligned long in both scalp and intraday reports, no longer bias-short-tagged). **2 untracked legacy alerts today** (BICO/USDT, 12:01 and 14:46 UTC — a second recurrence since the 16:12 review, which only had 1). A **new observation this cycle**: the freshest scalp report (14:47 EEST) explicitly rejects ACE/USDT, TST/USDT, RE/USDT and others from scalp-mode actionability citing `crypto_scalp_disabled (kill-switch: mode off, any hour/day)`, yet `proposed_signals` shows **B-tier scalp-mode rows for the same three symbols reaching `triggered`/`waiting_for_entry` status 6 minutes later** — flagged as a data-integrity question in §14, not asserted as a confirmed bug. Catalyst mapping this run: **54.8% unmapped** (805/1,470 today's events) — **over the 50% "weak this run" threshold**, use catalyst layer as context only today.

No newer scheduler cycle has completed since the 16:12 review (`cycle_06_14-46` remains the latest finished cycle; `cycle_07` is mid-run as of this review, currently on a long-running `crypto quality overlay report` / `crypto swing versioned shadow sweep` step pair) — paper-monitor lifecycle counts below are therefore carried unchanged from `cycle_06` and will refresh next cycle.

## 2. Data Used

- `data/reports/scalp/2026-08-08_14-47_scalp_report.md` (gen 17:47 EEST) — fresh, <1h old
- `data/reports/intraday/2026-08-08_14-55_intraday_report.md` (gen 17:55 EEST) — fresh, <1h old, freshest this cycle
- `data/reports/swing/2026-08-08_04-00_swing_report.md` (gen 07:00 EEST) — ~11.6h old, carry-forward bucket (4-12h)
- `data/reports/stocks/intraday/2026-08-07_20-57_stocks_intraday_report.md` (gen Aug 7 23:57 EEST) — market closed Sat/Sun, planning-only
- `data/reports/stocks/swing/*`, `stocks/invest/*` — retired since 2026-07-02 ([[project_crypto_ai_desk_stocks_position_framework]]), excluded by design
- `data/catalysts/2026-08-08/catalyst_events.jsonl` (2,918 cumulative lines; 1,470 rows timestamped today), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_15-05.md` (latest cycle, 18:05 EEST)
- `data/processed/llm_analysis_packet.md` (17:56 EEST)
- `active-signals --asset-class crypto` (50 rows) / `--asset-class stocks` (50 rows)
- `signal-stats --asset-class crypto` and `--asset-class stocks`
- `detect_untracked_legacy_alerts --since 2026-08-08` → 2 untracked (BICO/USDT ×2)
- `data/scheduled_runs/2026-08-07_default_schedule/cycle_06_14-46_summary.md` (mtime 15:37 EEST, latest completed cycle) — 57/58 steps `[OK]`, 1 `[FAIL]`; `scheduler.log` (mtime 18:33 EEST) shows `cycle_07` actively running
- Direct read-only SQL on `db/crypto_ai_desk.sqlite` (`proposed_signals` for all open crypto A/B rows and all stocks A/B rows; `news_items` 24h lookups for ACE, RE, TST, SKYAI, DODO, NIL, HEI, BICO, STO, ZBT, TUT, BTC, ETH; direct read of `config/paper_entry_mode_policy.yaml` for the scalp kill-switch question)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-08_1612.md` (pre-US-open decision review, 16:12 EEST)
- 2 WebSearch queries (BTC/ETH price + macro backdrop; Strait of Hormuz / Coldcard hack latest) — both returned usable results, no WebFetch needed this cycle (search snippets were sufficient and directly corroborated/contrasted internal data)

External web research **was** available this cycle (full — 2/2 WebSearch queries returned usable, datable results).

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-08-07_default_schedule/scheduler.log` — mtime **Aug 8 18:33 EEST** (~6min old at review start) → **fresh**, well under the 3h defer threshold; log tail shows `cycle_07` actively mid-run (long steps: `crypto quality overlay report` 513.9s, `crypto swing versioned shadow sweep` still running at review time).
- Latest **completed** cycle summary `cycle_06_14-46_summary.md` (mtime 15:37 EEST, ~3h02min old) — **57 OK / 1 FAIL**, same file already read for the 16:12 review; no new completed cycle since then, so cycle-level counts (paper monitor status, scheduler failures) are unchanged carry-forwards, not fresh data points.
- The one failure carried from `cycle_06`: `paper execution accounting refresh` (exit=-1, 306.7s, hit the 300s timeout) — 2nd consecutive cycle at the time it was logged; cannot confirm a 3rd occurrence until `cycle_07` finishes.
- Crypto scalp report: 17:47 EEST → fresh (~1h old at write time, <1h at review start).
- Crypto intraday report: 17:55 EEST → fresh, freshest this cycle.
- Crypto swing report: 07:00 EEST, ~11.6h old → carry-forward bucket (4-12h); regime read (bullish trend, BTC/ETH uptrend) still consistent with fresher scalp/intraday.
- Stocks intraday report: Aug 7 23:57 EEST → stale relative to now but market is closed (weekend) — planning/watchlist context only, not a data-quality failure.
- Stocks swing/invest: retired since 2026-07-02 — excluded by design.
- Paper monitor status (from `cycle_06`, step 55, Telegram, carried forward — not re-measured this cycle): Open actionable **34**, Waiting for entry **2**, Entered unresolved **16**, Review/Shadow **29**, No-entry/stale/moved-away **243**, Needs review **5**.
- Untracked legacy crypto alerts: **2** today (BICO/USDT intraday 12:01:41 UTC, BICO/USDT scalp 14:46:08 UTC) — both without a matching `proposed_signal` within 6h.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-08 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["cycle_07 not yet complete, no fresh paper-monitor counts this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~6min old, actively running cycle_07 (long-running crypto quality overlay + shadow sweep steps)", "latest completed cycle (cycle_06) unchanged since 16:12 review, 57/58 OK, 1 FAIL", "swing report ~11.6h old (carry-forward, cross-checked consistent)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"], "data_missing": ["stocks weekend market data (structurally unavailable)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC+ETH uptrend, breadth 57.5%/62.5% above EMA20/50, continuing mild intraday cooling (66.7/74.4 -> 60.0/67.5 -> 57.5/62.5 across today's reviews)", "macro risk score back to 100.0/100 (6 risk-off hits) vs 86.9/100 at 16:12", "WebSearch confirms BTC ~$65k / ETH ~$1,900-1,930 holding, reacting positively to weak July jobs report (dovish Fed read)", "stocks: no session today or tomorrow"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping today: 45.2% mapped / 54.8% unmapped (665/1470) -- over the 50% weak-mapping threshold", "5 active narrative baskets: binance_ecosystem_teaser (BNB/ASTER), rwa_narrative (ONDO/XLM, fresh<6h), perps_dex_narrative (HYPE+DYDX/GMX/ASTER), delisting_thin_liquidity (BONK), momentum_breakout (TUT/RE/DODO/SYN/ACE, fresh<1h, explicitly labeled 'no confirmed news catalyst', playbook avoid_chase)", "direct news_items 24h check for ACE/RE/TST/SKYAI/DODO/NIL/HEI/BICO/STO/ZBT/TUT: zero hits for all -- pure technical/momentum cluster, confirmed not just inferred", "external WebSearch on Hormuz thread shows de-escalation (Oman/Iran talks positive) contrasting with the desk's own elevated risk-off headline count"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "data_unavailable"], "data_missing": ["OI 24h% n/a for several active symbols this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZBT/USDT, NIL/USDT, HFT/USDT, BTW/USDT all explicitly capped from short to C-tier this cycle by the report's own logic: 'short squeeze risk -> capped to C: thin_liquidity_short_squeeze_risk'", "ACE/USDT: price up + OI down = short covering, weaker continuation quality; funding -0.000625, OI 24h -9.94%", "TST/USDT: price up + OI down, funding -0.000129, OI 24h -3.93%", "TUT/USDT: OI 24h +72.92% on an already +92%/24h move -- fresh leveraged positioning piling into an extreme extension", "DODO/USDT: negative funding across mexc (-0.00196), crowding elevated"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest"], "data_missing": ["TradingView / manual chart check unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["DODO/USDT intraday signal (score 68.0) already tp1_hit -- confirmed the pullback-entry thesis carried from the 16:12 review, manage remainder", "RE/USDT is fresh (waiting_for_entry, created 14:53-14:55 UTC, ~44min old at review time) but the scalp report itself flags 'Weekend Mode: large 24h move detected -- demand retest acceptance before entry', +13-14%/24h already realized", "TUT/USDT +92.4%/24h, >2 ATR from EMA20 per the report's own scalp rejection note -- explicit do-not-chase flag", "BICO/USDT remains a chase-risk repeat name, tagged 'Weekend Mode: large 24h move' in the rejected list"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry"], "data_missing": ["cycle_07 not complete -- lifecycle counts are a carry-forward from cycle_06"],
      "suggested_effect": "advisory_only",
      "facts_used": ["paper monitor status (carried from cycle_06): open actionable 34, waiting for entry 2, entered unresolved 16, review/shadow 29, no-entry/stale/moved-away 243, needs review 5", "crypto active A/B open book: 0 A-tier, 63 B-tier rows across triggered/tp1_hit/tp2_hit/waiting_for_entry", "XRP/USDT swing short still tp1_hit, unresolved, expires 2026-08-08T18:02 UTC (~2h20min from this review -- will resolve before the 21:30 late-session review)", "detect_untracked_legacy_alerts: 2 today (BICO/USDT x2) vs 1 at 16:12 -- new recurrence"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": ["correlation_cluster", "reduce_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZBT/USDT (2 open swing longs) tagged bias=short with -10.6% 24h in this cycle's own intraday deep-dive (capped to C for short-squeeze risk) -- persists across at least 4 consecutive reviews today", "NIL/USDT (1 open swing long, score 66.2) NEW this cycle -- same pattern: bias short, -8.36% 24h, this cycle's own report caps its short setup to C for squeeze risk, yet an open long from 04:00 UTC remains live", "ACE/USDT contradiction RESOLVED this cycle -- ACE is now the strongest aligned long (score 100, +10.4%/24h), no longer bias-short-tagged", "crypto scalp mode structurally losing (PF ~0.16-0.17 in recent windows per signal-stats mode breakdown), and today's freshest scalp report shows scalp-mode kill-switch active for essentially every candidate", "2 untracked legacy alerts (BICO/USDT) -- signal-reuse integrity risk, standing TODO, now escalating within the day (1 -> 2)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto headline A/B stats: sample=189, triggered=184, winrate 15.76%, PF 1.95, avgR +0.217, totalR +31.4 -- reliable confidence", "by-mode breakdown (labels truncated in CLI table but consistent with prior reviews' mapping): one mode PF ~5.35 (n=63, working edge = swing), one mode PF ~1.32 (n=81, moderate = intraday), one mode PF ~0.17 (n=45, structurally losing = scalp)", "system's own observations: 'tier=B triggered winrate 16% is low' and 'weekend=Y: weekend signals underperform (winrate 11%, n=48)'", "stocks: all-tier n=448, PF 0.17, avgR -0.23 -- known standing issue, no live A/B stocks currently open (all resolved expired/missed/stopped)"] },
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
    "best_long_candidate":     { "symbol": "DODO/USDT", "trigger": "already open (tp1_hit, entry 0.02088-0.02228, stop 0.02089), manage remainder toward tp2 0.02535/tp3 0.02674 -- confirms the pullback-entry thesis carried from the 16:12 review; for a fresh non-open idea, RE/USDT (waiting_for_entry, entry 0.4134-0.4514) needs a retest/acceptance per the report's own weekend-mode flag before it is a clean chase-free entry" },
    "best_short_candidate":    { "symbol": "XRP/USDT", "trigger": "already-open swing short (tp1_hit, entry 1.0598-1.0610, invalidation 1.0626, expires 2026-08-08T18:02 UTC, ~2h20min from this review) -- manage existing only; no fresh short setup scored this cycle, all short candidates (ZBT/NIL/HFT/BTW) are capped to C for short-squeeze risk against the bullish tape" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT or XLM/USDT (rwa_narrative basket, freshest genuine catalyst basket <6h)", "trigger": "no live A/B signal currently open on either -- basket-level only; would need a fresh proposed_signal referencing the RWA/tokenization narrative with a technical entry structure before it is actionable" },
    "avoid_candidate":         { "symbol": "ZBT/USDT, NIL/USDT (open swing longs); TUT/USDT (fresh chase)", "reason": "ZBT/NIL: open longs contradicted by this cycle's own bias=short + short-squeeze-capped tagging -- do not add size until stop-out or bias flip. TUT/USDT: +92.4%/24h, >2 ATR from EMA20, OI +72.9% (fresh leverage piling into an extreme extension) -- textbook chase risk, explicitly flagged by the report's own rejection logic" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | risk_on, longs_preferred, mixed | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, oi_contradicts, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.70 | open_actionable, waiting_for_entry, entered_unresolved, no_entry | advisory_only |
| risk_manager | manual_review | 0.60 | correlation_cluster, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-08_1612.md` (pre-US-open decision review, 16:12 EEST):

- **Macro risk score reversed higher**: 86.9/100 → **100.0/100** (6 fresh risk-off hits, 0 risk-on, 3 calendar/watch). A direct external check specifically on the Strait of Hormuz thread (the previous review's cited driver) shows **de-escalation**, not escalation, in the 13:57-14:48 UTC window — the score's move looks driven by breadth of risk-off headlines generally, not a fresh Hormuz shock. Worth treating the 100/100 reading with more skepticism than face value this cycle.
- **Altcoin breadth continued cooling**: 60.0%/67.5% → **57.5%/62.5%** (EMA20/50) — still bullish-trend, incrementally less broad for the third straight review today.
- **ACE/USDT contradiction resolved**: ACE is no longer in the weakest-symbols/bias-short list; it is now the single strongest symbol in both the scalp and intraday reports (score 100.0, +10.4%/24h), fully aligned with its open long positions.
- **NIL/USDT contradiction newly confirmed**: 1 open swing long (score 66.2, created 08:00 UTC) against this cycle's own short-squeeze-capped short setup for NIL (bias short, -8.36%/24h) — a new symbol joining the standing ZBT/USDT pattern, not previously flagged at this severity.
- **Untracked legacy alerts: 1 → 2** (BICO/USDT 12:01 UTC carried, plus a **new** BICO/USDT scalp alert at 14:46 UTC) — the TODO-3 pattern recurred a second time today.
- **New observation**: freshest scalp report (17:47 EEST) rejects ACE/TST/RE from scalp actionability via `crypto_scalp_disabled` kill-switch language, yet `proposed_signals` recorded B-tier scalp rows for the same three symbols reaching `triggered`/`waiting_for_entry` 6 minutes later (14:53-14:55 UTC) — flagged in §14 for human verification (may be an intentional shadow/counterfactual tracking lane per `config/paper_entry_mode_policy.yaml`'s `disabled_shadow` block, or a genuine kill-switch gap; not confirmed either way from available data).
- **DODO/USDT progressed**: the 16:12 review's best-long-candidate pick (`waiting_for_entry`, pullback zone 0.0217-0.0223) has since triggered and hit TP1 — confirms the thesis; now managing the remainder toward TP2/TP3.
- **Catalyst mapping**: 47.8% unmapped (cumulative, 5-cycle basis at 16:12) vs **54.8% unmapped** (today-only, 6-cycle basis measured directly this run) — methodology differs slightly (today-only vs. cumulative) but both reviews stayed near or over the 50% threshold; this run crosses it and triggers the "weak this run" flag.
- **No newer completed scheduler cycle**: `cycle_06` remains the latest finished cycle (unchanged from 16:12); `cycle_07` is mid-run — paper-monitor lifecycle counts and the `paper execution accounting refresh` failure status are carried forward, not re-measured.
- **XRP/USDT short still unresolved** (tp1_hit, same as 16:12) — now within ~2h20min of its 18:02 UTC expiry; will resolve before the 21:30 late-session-risk review, not this one.
- **No new A-tier signals** on either asset class.

## 5. Catalyst Coverage

- Total catalyst events measured today (timestamp-filtered to 2026-08-08, across all cycles through `cycle_15-05`): **1,470**
- Mapped (non-null symbol): **665** (45.2%)
- Unmapped: **805** (54.8%) — **over the 50% threshold this run**
- Narrative baskets: **5** (binance_ecosystem_teaser, rwa_narrative, perps_dex_narrative, delisting_thin_liquidity, momentum_breakout)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top unmapped headline samples:
  1. "Tradfin: *US SAYS UKRAINE TO AVOID TARGETING TANKERS, BLACK SEA OIL SITE..." (geopolitical wire, no symbol resolver hit)
  2. "PNR Investors Have Opportunity to Lead Pentair plc Securities Fraud Lawsuit" (recurring law-firm investor-alert prose-ticker miss pattern, flagged in prior reviews)
  3. "Ant Group's Ling 3.0 Flash packs 124B parameters into a model built for speed, not size" (AI model news, no crypto/stock symbol expected)
  4. "Russia shuts down 9 crypto exchanges in major Moscow crackdown" (regulatory, no single symbol)
  5. "Japan's FSA has asked crypto exchanges to impose withdrawal delays..." (regulatory, sector-wide, no single symbol)
- Latest single cycle (`catalyst_cycle_15-05.md`, 500 events): other_news 472, exploit_hack 7, partnership 5, regulatory_sector_headline 4, insider_activity 3, product_launch 3, earnings_event 3, platform_growth 1, legal_risk 1, exchange_delisting 1.
- Top catalysts by importance this cycle: BTC/USDT exploit_hack (0.86, "$1.5 billion hack... irreversible"), BTC/USDT exploit_hack ×2 (0.81, Lightning-node drains), COIN regulatory (0.80, CLARITY Act 60-vote Senate showdown in September), basket exploit_hack (0.73, Coldcard $111M), basket legal_risk (0.73, Photronics securities suit).

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **cautious risk-on** — BTC/ETH uptrend, breadth 57.5%/62.5% above EMA20/50 (continued mild cooling through the day), macro risk-off headline overlay at 100/100 but the specific Hormuz driver cited by the prior review is externally de-escalating, not escalating; price action (BTC ~$65K, ETH ~$1,900-1,930 per external check) continues to shrug off headline pressure.
- Stocks mood: **closed (weekend)** — no session today or tomorrow; all stock signals are Monday-planning context only; no A/B stocks signal is currently open (all recent stocks A/B rows resolved expired/missed_no_entry/stopped).
- Dominant narrative: RWA/tokenization (ONDO/XLM) remains the most durable multi-week basket; momentum_breakout (TUT/RE/DODO/SYN/ACE, fresh <1h, explicitly "no confirmed news catalyst") is the freshest and most extreme (TUT +92.4%/24h).
- Preferred side now: **longs, selective, no fresh chases** — manage the existing DODO/USDT long toward TP2/TP3; RE/USDT needs a retest before entry; do not chase TUT/BICO/TST/SYN/MMT at current extended levels.
- Best long candidate: **DODO/USDT** (open, tp1_hit, manage toward tp2 0.02535/tp3 0.02674).
- Best short candidate: **XRP/USDT** (open, tp1_hit, invalidation 1.0626, resolves within ~2h20min).
- Best catalyst-backed candidate: **ONDO/USDT or XLM/USDT** (rwa_narrative basket, freshest genuine catalyst grouping) — basket-level only, no live signal yet.
- What to avoid: adding size to **ZBT/USDT and NIL/USDT** open longs (bias contradiction, both capped to C on the short side by this cycle's own report for squeeze risk); chasing **TUT/USDT** (+92.4%/24h, OI +72.9%, textbook overextension) or any of TST/SYN/BICO/MMT/RE at current extended levels; treating any stock signal as actionable before Monday RTH; adding new scalp-mode risk (structurally losing, kill-switch active for essentially every candidate this cycle).
- What would change the view: a confirmed BTC breakdown below its current uptrend structure, a material Hormuz escalation reversing today's de-escalation signals, ZBT/NIL breaking their swing invalidation levels (resolving the contradiction via stop-out), or a bias flip back to long for either.

## 7. Candidate Deep Dives

### 1. ZBT/USDT & NIL/USDT — open swing longs vs. this cycle's own short-squeeze-capped short tags (contradiction risk, manual review)
- Status: ZBT/USDT — 2 open swing longs, `triggered` (`sig_66ffd2ccca900b8f` score 72.4, entry 0.1573-0.1626/inval 0.1510/exp 2026-08-13; `sig_0be20040e229aec5` score 69.9, entry 0.1407-0.1491/inval 0.1253/exp 2026-08-14). NIL/USDT — 1 open swing long, `triggered` (`sig_1a18d3fdc3986371` score 66.2, entry 0.03425-0.03934/inval unspecified stop 0.03424/exp 2026-08-15, created 2026-08-08T04:00:03 UTC).
- Has price already reacted to a catalyst? No — 0 fresh (24h) `news_items` rows for either symbol (directly re-verified this run). Pure technical divergence.
- Aligned with market mood? No — mood is cautious risk-on/longs-preferred, but both are tagged bias=short with negative 24h (ZBT -10.6%, NIL -8.36%) in this cycle's freshest intraday report, and the report's own deep-analysis engine caps their short setups to C-tier specifically because shorting them fights a bullish tape and carries squeeze risk — i.e., the system itself is internally conflicted: long-book says hold, short-analysis says squeeze-risk-if-shorted, neither resolves the open longs.
- Actionable now or wait? Do not add size to either. Watch for a break of the swing invalidation levels (ZBT 0.1253/0.1510; NIL near 0.03424), which would resolve the contradiction into a clean stop-out, or a bias flip back to long.
- What invalidates: ZBT — confirmed close below 0.1253 (first entry). NIL — confirmed close below ~0.0342.
- Catalyst confirmation/contradiction: no catalyst either way for either symbol — pure technical.

### 2. ACE/USDT — resolved contradiction, now top mover, but with an unresolved kill-switch/DB question
- Status: strongest symbol in both fresh reports (score 100.0, +10.4%/24h, RS+10.1%, volume 3.97x). Open positions: B-tier intraday `waiting_for_entry` (score 75.0, created 14:55:05 UTC) and 2 older B-tier swing `triggered` positions (scores 79.3 and 68.5, from 08-06/08-07).
- **Data-integrity flag**: the 17:47 EEST scalp report explicitly places ACE/USDT in "Rejected / Not Ready" citing `crypto_scalp_disabled (kill-switch: mode off, any hour/day)` plus "No fresh verified catalyst detected" — yet `proposed_signals` shows a B-tier **scalp**-mode row for ACE (`sig_496015826e4cf605`, score 78.0, status `triggered`) created 14:53:46 UTC, 6 minutes after the report file was written. Same pattern for TST/USDT (`sig_03514dedd89a28bc`) and RE/USDT (`sig_acb5a61b1bdab109`). `config/paper_entry_mode_policy.yaml` shows a `disabled_shadow` block for `crypto`/`scalp` with reason `crypto_scalp_disabled_by_policy`, which by its own comment governs the **shadow/new-logic measurement lane**, not necessarily the production-paper lane — it is not clear from available read-only data whether these `triggered` scalp rows are (a) intentional shadow-lane tracking rows that don't count toward live paper P&L, or (b) a genuine gap where kill-switched scalp candidates still reach `triggered` status in the same table used for signal-stats. See §14.
- Has price already reacted to a catalyst? No — 0 fresh (24h) `news_items` rows for ACE. Pure momentum/RS.
- Aligned with market mood? Yes, directionally (RS-leader long in a bullish tape) — but the momentum_breakout narrative basket explicitly tags ACE (along with TUT/RE/DODO/SYN) as "top gainers without confirmed news catalyst — pure momentum cluster" with playbook `avoid_chase`.
- Actionable now or after confirmation? The live intraday `waiting_for_entry` position (entry 0.1246, stop 0.1165) requires its own entry trigger — not a market chase. Do not add fresh scalp-mode exposure regardless of resolution of the §14 question above.
- What invalidates: 1h close beyond the intraday stop (0.1165) or swing invalidations (0.1106 / 0.0928 on the older positions).
- Catalyst confirmation/contradiction: none — pure technical/RS thesis, explicitly flagged avoid-chase by the desk's own narrative layer.

### 3. DODO/USDT — best long candidate, confirmed progressing (carried from 16:12 review)
- Status: B-tier intraday, `tp1_hit` (`sig_daaddc397aaac7b8`, score 68.0, entry 0.02088-0.02228, stop 0.02089, tp1 0.02395/tp2 0.02535/tp3 0.02674, created 2026-08-08T12:01:39 UTC).
- Has price already reacted? Yes — +9.1%/24h, TP1 already realized; this is the same idea flagged as the cleanest non-extended setup at 16:12, now confirmed working.
- Is the setup chasing? No — already in position; managing an existing partial win, not a fresh entry decision.
- Aligned with market mood? Yes — RS-leader long in a bullish tape, though still part of the "no confirmed catalyst" momentum_breakout basket (pure technical/RS thesis).
- Actionable now or after confirmation? Manage existing toward TP2 (0.02535) / TP3 (0.02674); no fresh action needed.
- What invalidates: a stop-out at 0.02089 on the remaining position.
- Catalyst confirmation/contradiction: none — technical/RS thesis only, consistent with the 16:12 framing.
- Derivatives: negative funding across mexc (-0.00196), crowding elevated — mild caution, not disqualifying, unchanged from 16:12.

### 4. TUT/USDT — clearest chase-risk / avoid example this cycle
- Status: no fresh signal this cycle; multiple older B-tier scalp (tp1_hit) and swing (`triggered`) positions from 08-04 through 08-07 remain open, but the symbol itself is now +92.4%/24h — an extreme extension.
- Has price already reacted to a catalyst? No fresh (24h) `news_items` hit; the momentum_breakout basket explicitly lists TUT as part of the "no confirmed news catalyst" pure-momentum cluster with playbook `avoid_chase`.
- Is the setup chasing? Yes, unambiguously — the scalp report's own rejection note reads "Price is more than 2 ATR from EMA20; do not chase" and "Entry quality is weak because the move is extended."
- Retest/pullback structure? None offered this cycle — this is a hold-existing-only situation for the open positions, not a fresh-entry idea.
- Overextended? Yes — OI 24h +72.92% on top of the +92.4% price move indicates fresh leveraged positioning piling into an already extreme move, raising both chase risk and squeeze/unwind risk for any new entrant.
- Aligned with market mood? Directionally (long, bullish tape) but the extension itself is the risk, not the direction.
- Actionable now or after confirmation? Not actionable as a fresh entry under any confirmation this cycle; manage existing positions only, tighten mental stops given the extension.
- What invalidates: a sharp reversal / failed-breakout candle would be the first sign of unwind risk given the OI buildup.
- Catalyst confirmation/contradiction: none — pure technical extension.

### 5. XRP/USDT — only open short in the book, near resolution
- Status: 1 open swing short, `tp1_hit` (`sig_c1e2871dd5fcaf1a`, entry 1.0598-1.0610, invalidation 1.0626, expires **2026-08-08T18:02 UTC** — ~2h20min from this review).
- Has price already reacted? Partially — TP1 already hit, partial win in progress, same status as the 16:12 review.
- Actionable now or wait? Manage existing only; will resolve before the 21:30 late-session-risk review (the next slot), not this one — the 16:12 review's expectation that it would resolve by 18:30 was off by roughly the residual time-to-expiry, since expiry is 18:02 UTC = 21:02 EEST, not 18:02 EEST (a EEST/UTC labeling slip in the prior review's arithmetic, corrected here).
- What invalidates: a confirmed break back above 1.0626.
- Catalyst confirmation/contradiction: no XRP-specific catalyst found in the last 24h.

## 8. Best Candidates Ranked

1. **DODO/USDT (long — manage existing)** — tp1_hit, managing toward tp2/tp3; cleanest confirmed idea carried from the prior review.
2. **XRP/USDT (short — manage existing)** — only open short in the book, tp1_hit, resolves ~21:02 EEST (before the 21:30 review).
3. **RE/USDT (long-watch, needs retest)** — waiting_for_entry (entry 0.4134-0.4514), but the report's own weekend-mode flag demands a retest/acceptance before this is a chase-free entry; not yet actionable at market.
4. **ONDO/USDT / XLM/USDT (catalyst-watch, basket-level only)** — freshest genuine catalyst grouping (rwa_narrative, <6h), no live signal yet.
5. **ZBT/USDT & NIL/USDT (manual review, avoid new size)** — open-long-vs-bias-short contradiction, NIL newly confirmed this cycle alongside the standing ZBT pattern.
6. Not deep-dived, chase-risk-flagged, no displacement of the above: TST/USDT (+8.2%/24h, long/short ratio heavily skewed per scalp rejection notes), SYN/USDT, BICO/USDT (repeat chase-risk name), MMT/USDT, SKYAI/USDT (MEXC-only, no derivatives confirmation).

## 9. Avoid / No Trade

This applies to the **current decision window only** — scanning, tracking, and monitoring continue uninterrupted regardless.

- **Do not add size to ZBT/USDT or NIL/USDT** open longs while the bias=short + short-squeeze-capped contradiction persists (§7.1).
- **Do not chase TUT/USDT** at its current +92.4%/24h extension, or TST/SYN/BICO/MMT at their current extended levels — wait for stated pullback/retest zones, or skip.
- **Do not treat any stock signal as actionable this weekend** — market closed until Monday RTH; no A/B stocks signal is currently open regardless.
- **Do not add new crypto scalp-mode risk** — structurally losing (PF ~0.16-0.17 in recent windows), kill-switch active for essentially every candidate in the freshest scalp report, and the §14 kill-switch/DB question raises further doubt about what scalp-mode signals in the tracker actually represent right now.
- **RE/USDT is not a clean entry at market** — the report's own weekend-mode logic requires a retest/acceptance first.

## 10. Main Risks

- **Macro-risk-score / substantive-news divergence**: the desk's own risk-off score jumped back to 100/100, but a direct external check on the specifically-cited Hormuz driver shows de-escalation this cycle — worth treating the headline-count score as a breadth signal, not a precision signal, until reconciled.
- **Contradiction-cluster risk, expanding**: ZBT/USDT (standing) plus now NIL/USDT (new) open longs vs. bias=short + short-squeeze-capped tags — the pattern is not resolving, and a second symbol joining suggests it may be a systematic tagging-window issue rather than isolated to one symbol (see standing TODO).
- **Chase risk**: TUT (+92.4%/24h, OI +72.9%) is the most extreme example; RE/TST/SYN/BICO/MMT all sit in the same no-catalyst momentum cluster at varying degrees of extension.
- **Data-integrity risk, escalating**: untracked legacy alerts went from 1 (16:12) to 2 (this review) for BICO/USDT specifically; the new scalp-mode kill-switch-vs-`proposed_signals` question (§7.2, §14) adds a second, distinct integrity concern this cycle.
- **Scheduler regression risk (unconfirmed this cycle)**: `paper execution accounting refresh` failed for its most-recently-observed 2 consecutive cycles as of `cycle_06`; `cycle_07` has not finished, so a 3rd occurrence cannot be confirmed or ruled out yet.
- **Standing latency risk**: crypto and stocks intraday both remained SLA_BREACH as of the last full cycle read (unchanged, not re-measured this cycle).
- **Weekend data-gap risk**: stocks remain fully planning-only; nothing found here should be assumed to still hold without a fresh Monday-morning check.

## 11. Action Plan — next 4 hours

- Manage DODO/USDT toward TP2 (0.02535) / TP3 (0.02674); no fresh action needed.
- Watch XRP/USDT into its 18:02 UTC (21:02 EEST) expiry — confirm win/loss/no-further-TP outcome at or before the 21:30 late-session-risk review.
- Watch ZBT/USDT (0.1253 / 0.1510) and NIL/USDT (~0.0342) invalidation levels — a break resolves the contradiction into a clean stop-out; a bias flip back to long would validate the holds. Treat NIL as a newly-confirmed instance of the same standing pattern, not a one-off.
- Do not chase RE/USDT at market; wait for the retest/acceptance the report itself demands.
- Continue monitoring the Hormuz thread for confirmation of the de-escalation signal found this cycle (Oman/Iran talks, no transit fees) versus the desk's own elevated risk-off score — reconcile at the next review.
- No stock action possible before Monday RTH.
- Flag the scalp-mode kill-switch/`proposed_signals` question (§7.2) to a human session for direct code/config verification — this review cannot resolve it from read-only data alone.

## 12. Final Verdict per Mode

- **Crypto scalp**: caution / near-avoid — structurally losing (PF ~0.16-0.17), kill-switch active for essentially every candidate this cycle, and an unresolved data-integrity question about what "triggered" scalp signals in the tracker actually represent right now.
- **Crypto intraday**: caution — moderate edge; DODO/USDT is the confirmed clean exception this cycle (tp1_hit, managing existing), RE/USDT needs a retest before it qualifies.
- **Crypto swing**: watch/selective — still historically the working edge (PF ~5.35 in recent windows); ZBT/NIL need manual review before any further action, ACE's prior contradiction has resolved.
- **Stocks (all modes)**: closed / planning-only through the weekend — no A/B signal currently open; next real data point is Monday premarket/RTH.

## 13. Sources

- [Bitcoin and ethereum prices today, Friday, August 7, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-august-7-2026-crypto-prices-moving-higher-following-july-jobs-report-131451960.html) — Yahoo Finance, 2026-08-07
- [The Largest Hardware Wallet Exploit of 2026: Inside the USD 116 Million Coldcard Hack](https://www.trmlabs.com/resources/blog/the-largest-hardware-wallet-exploit-of-2026-inside-the-usd-116-million-coldcard-hack) — TRM Labs
- [Damage From Coldcard Hack Reaches $130 Million](https://finance.yahoo.com/markets/crypto/articles/damage-coldcard-hack-reaches-130-142500652.html) — Yahoo Finance
- [Coldcard Bitcoin Wallets Compromised as Hackers Exploit Software Flaw](https://www.bloomberg.com/news/articles/2026-08-03/hackers-target-bitcoin-s-safest-hiding-place-in-ongoing-attack) — Bloomberg
- Internal: `data/reports/scalp/2026-08-08_14-47_scalp_report.md`, `data/reports/intraday/2026-08-08_14-55_intraday_report.md`, `data/reports/swing/2026-08-08_04-00_swing_report.md`, `data/catalysts/2026-08-08/catalyst_cycle_15-05.md`
- Internal (Hormuz de-escalation, sourced from `catalyst_events.jsonl` today, 13:57-14:48 UTC, wire-service headlines via internal feed): Oman state news agency (positive-progress + condemnation-of-attacks statements), France/Pentagon safe-passage statements, Iran-to-US oil-flow/no-transit-fee statements relayed via Fox News/Alarabiya feeds — treated as `single_source`/wire-relay, not independently cross-verified this run.

## 14. Fix Requests / TODO

### TODO-scalp-killswitch-vs-proposed-signals
- **issue:** The freshest scalp report (2026-08-08 17:47 EEST / 14:47 UTC) explicitly rejects ACE/USDT, TST/USDT, RE/USDT (and others) from scalp actionability citing `crypto_scalp_disabled (kill-switch: mode off, any hour/day)`. Yet `proposed_signals` contains B-tier **scalp**-mode rows for the same three symbols reaching `triggered` (ACE, TST) / `waiting_for_entry` (RE) status at 14:53:46-47 UTC — 6 minutes after the report file was written, same cycle.
- **evidence:** `data/reports/scalp/2026-08-08_14-47_scalp_report.md` §7b ("Rejected / Not Ready"); direct SQL: `sig_496015826e4cf605` (ACE, scalp, triggered), `sig_03514dedd89a28bc` (TST, scalp, triggered), `sig_acb5a61b1bdab109` (RE, scalp, waiting_for_entry), all `created_at` 2026-08-08T14:53:46-47Z; `config/paper_entry_mode_policy.yaml` shows a `disabled_shadow` block (not necessarily production-lane) for `crypto`/`scalp` with reason `crypto_scalp_disabled_by_policy`.
- **suggested manual fix:** Verify directly in code whether these `triggered`/`waiting_for_entry` scalp rows are (a) an intentional shadow/counterfactual tracking lane that does not feed live paper P&L or Telegram alerts (in which case this is expected behavior and the report's rejection message could be reworded to reduce confusion), or (b) a genuine gap where the scalp kill-switch is applied at the report/Telegram-alert layer but not at the `proposed_signals` creation layer, which would mean scalp-mode signal-stats (PF ~0.16-0.17) may include kill-switched-mode trades that were never meant to be tracked as live/actionable.
- **priority:** high (data-integrity question affecting how scalp-mode performance numbers should be interpreted).
- **first observed:** 2026-08-08 18:39 EEST (this run).

### TODO-nil-zbt-contradiction-expanding
- **issue:** The standing ZBT/USDT open-long-vs-bias-short contradiction ([[project_crypto_ai_desk_bias_tag_contradiction]], previously tracked with ACE/USDT) has gained a new symbol this cycle: NIL/USDT (1 open swing long, score 66.2, vs. this cycle's own short-squeeze-capped short tag, -8.36% 24h). ACE/USDT's version of the contradiction has resolved (ACE realigned to a genuine long leader). Composition is shifting rather than shrinking.
- **evidence:** `data/reports/intraday/2026-08-08_14-55_intraday_report.md` §2 "Weakest Symbols" (ZBT -10.58%, NIL -8.36%) and its deep-analysis section (ZBT/NIL both "short squeeze risk -> capped to C"); direct `proposed_signals` SQL confirming both symbols' open long positions.
- **suggested manual fix:** per the existing TODO — investigate whether the bias-tagging logic and the open-signal-hold logic read from different lookback windows; the pattern recurring with a rotating-but-persistent symbol set (3-symbol -> 2-symbol -> now expanding again) suggests a systematic timing/window mismatch rather than isolated bad luck per symbol.
- **priority:** high (already escalated per standing memory; this is a fresh expansion, not just a persistence data point).
- **first observed (this specific NIL instance):** 2026-08-08 18:39 EEST (this run); standing pattern first observed 2026-08-08 04:39 EEST.

### TODO-untracked-alert-recurrence-2nd-today
- **issue:** `detect_untracked_legacy_alerts` found 2 untracked alerts today (BICO/USDT intraday 12:01:41 UTC, BICO/USDT scalp 14:46:08 UTC) — both without a matching `proposed_signal` within 6h. This is the second BICO/USDT instance today (the 16:12 review only had the first).
- **evidence:** `scripts.detect_untracked_legacy_alerts --since 2026-08-08` output this run.
- **suggested manual fix:** per the existing standing TODO ([[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]) — investigate whether the watchlist re-fire path is reusing a stale/closed signal_id instead of minting a new `proposed_signal`, specifically for BICO/USDT which has now recurred at least 3 times across recent sessions.
- **priority:** high (already raised to high 2026-07-17 per memory; recurring within the same day now).
- **first observed:** 2026-07-17 (standing); today's recurrences 2026-08-08 12:01 and 14:46 UTC.

### TODO-paper-execution-accounting-refresh-timeout-unconfirmed
- **issue:** `paper execution accounting refresh` failed for 2 consecutive cycles as of the last completed cycle (`cycle_06_14-46`, 306.7s, hit the 300s timeout). `cycle_07` has not finished at review time, so whether this is now a 3rd consecutive failure cannot be confirmed this run.
- **evidence:** `data/scheduled_runs/2026-08-07_default_schedule/cycle_06_14-46_summary.md` §24 (carried from the 16:12 review, not re-measured).
- **suggested manual fix:** unchanged from the 16:12 review — investigate whether the underlying dataset this step scans has grown to the point of needing an index or batching change; check `cycle_07`'s summary once it completes to confirm or rule out a 3rd occurrence.
- **priority:** medium (escalate to high if `cycle_07` confirms a 3rd consecutive failure).
- **first observed:** 2026-08-08 (11:54 cycle); status at this review unconfirmed pending `cycle_07` completion.
