# Opus Enriched Review — post-close final daily review — Auto Cycle 23:24 EEST

## 1. Executive Summary

Post-close final daily review. **Advisory only / no auto-trade.** Crypto stays in
range/chop with both BTC and ETH in downtrend and macro risk pinned at 100/100
risk-off headwind — no A/B setups cleared the bar in scalp, intraday, or swing
this cycle. Stocks closed with extreme earnings-season dispersion (AMZN +15%,
best day since 2012, vs AAPL down hard on weak guidance) but zero clean A/B
actionable setups after legal/headline and actionability gates. The single
biggest finding this cycle is a **legal-risk false positive**: a genuine A-tier,
post-earnings AMZN long (score 86.2) was demoted to C/non-actionable by a
`going_concern` flag sourced from a headline about an *Amazon cloud rival's*
Chapter 11 filing, not Amazon itself (§7, TODO-6). Separately, the
`track-signals` pipeline has now failed **6 consecutive times** today, and a
direct DB check shows **16/21 crypto** and **167/175 stocks** "active" proposed
signals are past their own `expires_at` and stuck unresolved — this is a
system-wide tracker outage, not a market observation (§3, TODO-1). Scanning,
tracking, and monitors all continue regardless of mood.

## 2. Data Used

- Reports: scalp (mtime 22:21), intraday (22:29), swing (20:06) — crypto;
  stocks intraday (23:00). Stocks swing/invest last generated 2026-07-02 —
  expected: deprecated in favor of the shadow-only stocks position framework,
  not a freshness fault.
- LLM packets: `llm_analysis_packet.md` (22:29), `llm_stocks_packet.md` (22:55).
- Catalysts: `data/catalysts/2026-07-31/` — 7 cycles today, latest `catalyst_cycle_19-33.md`
  (mtime 22:33), `catalyst_events.jsonl` (3,500 events today), `narrative_baskets.jsonl` (1 basket).
- CLI: `active-signals` ×2 (crypto 21 rows, stocks 175 rows), `signal-stats` ×2,
  `detect_untracked_legacy_alerts --since 2026-07-31` (clean, 0 findings).
- DB (`db/crypto_ai_desk.sqlite`, read-only queries): `news_items`, `proposed_signals`
  expiry/status cross-checks for the tracker-backlog finding.
- Scheduler log `data/scheduled_runs/2026-07-31_default_schedule/scheduler.log`.
- External web research: **not performed this cycle** — internal `news_items`
  (90-day window) fully explained the AMZN legal-risk finding and the HYPE
  narrative basket was already sourced internally; no WebSearch/WebFetch needed.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 23:02 EEST, latest `cycle_03_22-12_summary.md` mtime
  23:02 EEST — both well under the 3h defer threshold. **Not deferred.**
- Monitors alive at end-of-cycle: crypto (pid 25568, ~90min), derivatives
  (pid 28652), fast-news (pid 25616), stocks (pid 23140), mexc-canary (pid 2212)
  — all reporting "still running," no restarts needed.
- News source health monitor + entity resolver health monitor: both exit=0.
- Paper monitor status (telegram): exit=0.
- **`track-signals` pipeline: FAILING.** Exit=1 on all 6 invocations today
  (14:55, 16:38, 18:41, 20:09, 22:13, 23:00 EEST) — up from 4 consecutive
  failures at the 21:39 review. See TODO-1.
- Direct consequence, verified by DB query just now: of 21 "active" crypto
  `proposed_signals`, **16 have `expires_at` already in the past** and are
  stuck unresolved; of 175 "active" stocks `proposed_signals`, **167** are
  past `expires_at` and stuck. Only 5 crypto and ~8 stocks signals are inside
  a still-valid window. Treat the count of "active signals" the CLI reports
  as **not representative of genuinely live risk** this cycle — see §3A
  `execution_lifecycle` and the Telegram Status block for the corrected split.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-07-31 23:24 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["scheduler_fresh"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 23:02, cycle summary 23:02, both fresh",
        "track-signals exit=1 x6 today (14:55-23:00)",
        "16/21 crypto and 167/175 stocks active signals past expires_at, unresolved"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["chop", "risk_off", "mixed"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC trend downtrend, ETH trend downtrend (intraday+swing reports)",
        "macro risk 100/100 risk-off headwind, 8 risk-off hits",
        "stocks: AMZN +15% vs AAPL sharp drop same session — earnings dispersion, not directional trend"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 3500 today, 1342 mapped / 2158 unmapped (61.7% unmapped)",
        "perps_dex_narrative basket: HYPE primary, DYDX/GMX/ASTER related, fresh <6h, single_source",
        "BTC exploit_hack Coldcard $38-40M self-custody exploit, importance 0.86"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["full OI history for thin alts"],
      "suggested_effect": "advisory_only",
      "facts_used": ["MMT/ZAMA/RE/EUL/BCH all capped C for thin_liquidity_short_squeeze_risk or high_upper_wick_short_squeeze_risk",
        "CFX/ERA flagged funding negative, shorts may be crowded"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["stale_before_entry", "entry_late", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["No A/B setups in scalp/intraday/swing reports (score < active threshold, mixed regime)",
        "AMZN already +15% intraday — chasing now would be late even absent the legal-risk block",
        "ROBO/PUMP/FIL still waiting_for_entry since earlier today, unfilled"] },
    { "agent": "execution_lifecycle", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/USDT (swing) triggered, expires 2026-08-07, genuinely open",
        "ACH/USDT (swing) tp2_hit, expires 2026-08-05, still open running to tp3",
        "16 crypto + 167 stocks signals past expires_at, unresolved — needs_review, not clean no-entry"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["headline_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["AMZN tier-demotion traced to a false-positive legal-risk match (TODO-6)",
        "no untracked-alert anomalies today (detector clean)",
        "no genuine legal/headline risk found on WMT/CAT/NOC in the window checked"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B week: sample=102, winrate 26.6%, PF 2.41, totalR +33.9R",
        "crypto by-mode: intraday PF 5.24/+29.7R, swing PF 1.84/+9.2R, scalp PF 0.17/-5.0R but scalp is kill-switch disabled (mitigated)",
        "stocks A/B week: sample=6, anecdotal, PF 0/-1.0R — too small to conclude",
        "stocks C-tier: winrate 6%, PF 0.18 — known/expected, C-tier stocks is watchlist-only per prior hardening"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.6,
      "reason_codes": [], "data_missing": [], "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "ROBO/USDT", "trigger": "limit fill 0.01402-0.01432, invalidation 0.01365", "reason": "Carried B-tier swing long, unchanged since 21:39 review, still not filled — no new confirmation, no new invalidation." },
    "best_short_candidate":    { "symbol": "WMT", "trigger": "confirmed break + hold below 111.09 with volume; C-tier only, do not treat as clean until confirmed", "reason": "Highest-score (78.5) fresh post-close C-tier short; stocks C-tier bucket has a 6% winrate/0.18 PF this week — watch only, not actionable." },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "pullback into perps-DEX narrative structure per wait_pullback playbook; confirm via DYDX/GMX/ASTER relative strength", "reason": "Only fresh (<6h) narrative-basket primary this cycle; single_source, needs corroboration." },
    "avoid_candidate":         { "symbol": "MMT/USDT", "reason": "Already down -26.4% 24h with high_upper_wick_short_squeeze_risk + exhaustion flags — chasing the short here risks a squeeze; also thin liquidity." },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 6
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.55 | scheduler_fresh (but track-signals failing) | advisory_only |
| market_regime | caution | 0.70 | chop, risk_off, mixed | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | stale_before_entry, entry_late, price_moved_away | advisory_only |
| execution_lifecycle | manual_review | 0.60 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.55 | headline_risk, manual_review | advisory_only |
| playbook_performance | ok | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | ok | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-31_2139.md` (21:39 EEST, late-session
risk review).

- **ROBO/USDT** — unchanged. Still the best long-watch, still `waiting_for_entry`
  at the same 0.01402-0.01432 zone. Thesis not invalidated, not confirmed either.
- **MSTR** — the 21:39 review's TODO-2 (conflicting active long+short across a
  confirmed earnings-miss catalyst) is now **resolved organically**: the long
  (`sig_1a5a9a318e38d9a3`) closed `missed_no_entry` and the short
  (`sig_89237c493b51f325`) closed `expired`. No longer an active contradiction
  — dropping it from the TODO list.
- **track-signals failures** — escalated from 4 to 6 consecutive today.
- **Catalyst mapping** — 61.7% unmapped this cycle vs 63.7-63.8% the last three
  cycles. Marginal improvement, still well over the 50% "weak" threshold —
  chronic, not resolved.
- **New this cycle**: the AMZN legal-risk false-positive (TODO-6) — not
  previously flagged; AMZN's earnings/price action itself is new to today.
- **New this cycle**: WMT / CAT / NOC C-tier stocks shorts, freshly
  `waiting_for_entry` (expire ~22:41 EEST) — none were listed in the 21:39
  review.

## 5. Catalyst Coverage

- Total catalyst events today: **3,500**. Mapped (non-null symbol): **1,342**
  (38.3%). Unmapped: **2,158 (61.7%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final
  decision.**
- Narrative baskets: **1** (`perps_dex_narrative`, primary HYPE/USDT, related
  DYDX/GMX/ASTER, playbook `wait_pullback`, single_source, fresh <6h).
- Top 3 unmapped headlines (macro/whale-flow, not symbol-specific — expected
  category of unmapped, not a resolver bug by itself):
  1. "250,000,000 $USDC minted at USDC Treasury" (×2, 2026-07-30)
  2. "Institutions accounted for a record 72% of spot OTC flow in H1 2026... per Wintermute" (2026-07-30)
  3. "South Korean crypto trading jumped 82% as the KOSPI plunged... per Seoul Economic Daily" (2026-07-30)

## 6. Market Landscape

Crypto stayed in range/chop with both majors trending down and a heavy macro
risk-off backdrop; nothing in scalp, intraday, or swing cleared the A/B bar
this cycle. The only mild positive dispersion was thin, low-volume names
(GIGGLE, COTI, EPIC, PUMP — all 0.2-0.4x volume), none of which supported a
clean breakout. Stocks closed on an extreme earnings-driven dispersion day
(AMZN's best single day since 2012 on AWS re-acceleration and a $600M tariff
refund story, against a hard AAPL drop on weak guidance) — this is idiosyncratic
single-name dispersion, not a directional index signal.

### Market Mood / Risk Routing

- Crypto mood: **chop / risk-off leaning** (BTC + ETH downtrend, macro risk 100/100)
- Stocks mood: **mixed / earnings-dispersion** (closed; AMZN +15% vs AAPL sharp drop, same session)
- Dominant narrative: perps-DEX (HYPE/DYDX/GMX/ASTER) in crypto; Mag7 earnings reset in stocks
- Preferred side now: **wait-for-trigger**, tilted toward catalyst-confirmed setups only
- Best long candidate: ROBO/USDT — trigger: limit fill 0.01402-0.01432
- Best short candidate: none clean — best short-watch: WMT — trigger: confirmed break below 111.09 with volume (C-tier only, unconfirmed)
- Best catalyst-backed candidate: HYPE/USDT — perps-DEX narrative pullback, needs RS corroboration from DYDX/GMX/ASTER
- What to avoid: MMT/USDT short (already -26.4% 24h, squeeze-risk-capped — do not chase)
- What would change the view: a clean BTC reclaim of local resistance (crypto), or RTH confirmation + resolved legal-risk tag on AMZN (stocks)

## 7. Candidate Deep Dives

### 1. AMZN (stocks, long) — contradiction risk / legal-risk false positive
- Score 86.2, would be A-tier, demoted to C ("watchlist / not actionable") by
  `legal_headline_risk: going_concern`.
- Root cause traced via internal `news_items` (90-day lookback used by the
  persistent legal-flag loader): the only AMZN-tagged hit matching the
  `going_concern`/bankruptcy regex is **"Cheaper Amazon cloud rival files for
  Chapter 11 bankruptcy"** (Finnhub company-news, 2026-07-27). This story is
  about an *AWS competitor* going bankrupt, not Amazon — the symbol resolver
  attached AMZN because the headline text contains "Amazon."
- Has price already reacted to the catalyst? Yes — AMZN is already +15% on
  today's earnings (AWS accel, tariff refund), so even absent the false
  legal-risk block, entering now would be **late/chasing** without a pullback.
- Is this a chase-risk setup? Yes, on the price side; the legal-risk block is
  unrelated to chase risk and is simply wrong.
- Actionable now or after confirmation? Neither — treat as **manual review
  required** until (a) the legal-risk tag is corrected (see TODO-6) and
  (b) a pullback/retest structure forms.
- Legal/headline risk: **false positive**, see TODO-6. No genuine legal risk
  found on AMZN in the 24-48h window.
- Verdict: **MANUAL REVIEW REQUIRED** (data-integrity block, not a real risk finding).

### 2. ROBO/USDT (crypto, swing, long) — carried long-watch
- Score 69.0, `waiting_for_entry`, entry 0.01402-0.01432, invalidation
  0.01365, created 13:34 UTC today. Unchanged since the 21:39 review.
- No fresh catalyst found for ROBO specifically this cycle; thesis is
  technical/RS-based, not catalyst-backed.
- Not overextended, not yet triggered — still a clean wait-for-fill idea, no
  new confirmation or invalidation since last review.
- Verdict: **WAITING for entry** — long-watch, trigger unchanged.

### 3. COTI/USDT (crypto, swing, long) — only genuinely open crypto long
- Score 65.9, status **triggered** (entry filled), entry zone
  0.01611-0.01673, invalidation 0.01536, targets 0.01878/0.02015/0.02193,
  expires 2026-08-07 — well inside its window.
- No dedicated fresh catalyst for COTI itself in this cycle's catalyst layer
  (catalyst_news score component was low, 6.8/20, in the adjacent watchlist
  scoring); running on technical/momentum thesis.
- Is the move overextended? 24h move (+18.9% in the 19:29 snapshot) is
  material but the entry already triggered earlier — this is a live open
  position, not a fresh entry decision.
- Verdict: **OPEN actionable** (entered, running toward TP1/TP2/TP3). No
  action needed; monitor invalidation at 0.01536.

### 4. HYPE/USDT (crypto, catalyst-backed, C-tier / narrative primary)
- Not an active `proposed_signal` — surfaced via the `perps_dex_narrative`
  basket (primary HYPE, related DYDX/GMX/ASTER), playbook `wait_pullback`,
  fresh <6h, source **single_source** (needs corroboration before treating
  as more than a watch idea).
- Has price already reacted? Partially — sample headline referenced a $57M
  HYPE whale move to exchanges, framed as bearish-leaning ("is $52 next?").
- Actionable now or after confirmation? After confirmation only — the
  playbook itself says wait for pullback, and single-source news should not
  be treated as verified.
- Verdict: **catalyst-watch** — wait for pullback + RS corroboration from
  DYDX/GMX/ASTER before treating as tradeable.

### 5. Crypto + stocks signal backlog (system integrity) — see TODO-1
- 16/21 crypto and 167/175 stocks "active" `proposed_signals` are past their
  own `expires_at` and unresolved, coincident with `track-signals` failing
  6/6 times today. This is not a market call — it is a tracker outage
  distorting the apparent size of the "active" book. See §3, TODO-1.
- Verdict: **NEEDS REVIEW** (data/tracking integrity, not a trade decision).

## 8. Best Candidates Ranked

1. **ROBO/USDT** (long-watch) — trigger: limit fill 0.01402-0.01432, invalidation 0.01365.
2. **HYPE/USDT** (catalyst-watch) — trigger: pullback + RS confirmation vs DYDX/GMX/ASTER.
3. **WMT** (short-watch, C-tier only) — trigger: confirmed break + hold below 111.09 with volume; do not treat as clean without confirmation given the C-tier bucket's 6% winrate this week.
4. **AMZN** (manual-review-only) — not actionable until the legal-risk tag is corrected AND a pullback forms; do not chase the existing +15% move.

## 9. Avoid / No Trade

This decision window only — never a command to stop the system.

- **MMT/USDT short** — already -26.4% 24h, `high_upper_wick_short_squeeze_risk`
  + exhaustion flags, thin liquidity. Chasing this short risks a squeeze.
- **RE/USDT, ZAMA/USDT, EUL/USDT, BCH/USDT shorts** — all capped to C for
  `thin_liquidity_short_squeeze_risk`; same logic, avoid chasing.
- **AMZN long at current price** — already +15% today; even setting aside the
  false legal-risk block, chasing here is late. Wait for a pullback/retest.
- Crypto scalp mode broadly — kill-switch disabled system-wide (mode off, any
  hour/day); no scalp ideas are actionable regardless of score.

## 10. Main Risks

- **Tracker outage (TODO-1)**: `track-signals` has failed 6/6 times today.
  Until fixed, "active signals" counts across both asset classes overstate
  genuinely live risk — 16 crypto + 167 stocks signals are stuck past expiry.
- **Legal-risk false positives (TODO-6)**: at least one A-tier stocks long
  (AMZN) was wrongly suppressed today by a mismapped competitor-bankruptcy
  headline. Unknown how many other symbols carry similar stale/mismapped
  90-day legal flags — worth a broader audit.
- **Catalyst mapping weak** (61.7% unmapped) — treat the catalyst layer as
  context, not a final decision input, this cycle.
- **Macro risk-off headwind (100/100)** for crypto — reduces conviction on
  any long chase; BTC self-custody exploit headline (Coldcard) adds sentiment
  drag independent of price.
- **Thin/low-volume RS leaders** (GIGGLE, COTI, EPIC, PUMP all <0.5x volume) —
  relative strength without volume confirmation is fragile.

## 11. Action Plan — next 4 hours

1. Monitor COTI/USDT (open, targets 0.01878/0.02015/0.02193, invalidation 0.01536) — no action needed, just track.
2. Watch ROBO/USDT for a fill at 0.01402-0.01432; do not chase above entry_high.
3. Track HYPE/USDT for a pullback into the perps-DEX narrative zone; confirm via DYDX/GMX/ASTER RS before treating as tradeable.
4. Do not chase AMZN's existing +15% move; wait for a pullback AND for the legal-risk tag to be manually corrected (TODO-6) before re-considering it actionable.
5. Treat WMT/CAT/NOC C-tier shorts as watch-only pending confirmation — this bucket has a 6% winrate this week.
6. No action on the crypto/stocks signal backlog from this run — it is a TODO for a human session (TODO-1), not something this review can fix.
7. Into the Asia session: BTC/ETH downtrend + risk-off headwind argues for continued caution on fresh longs; no clean short setups either given squeeze-risk caps on the weakest names — expect continued chop unless BTC breaks local support/resistance.

## 12. Final Verdict per Mode

- **Crypto scalp**: kill-switch disabled system-wide — no verdict needed, mode is off.
- **Crypto intraday**: no A/B setups; wait-for-trigger. Strongest historical performer this week (PF 5.24, +29.7R) but nothing fresh to act on right now.
- **Crypto swing**: no new A/B setups; ROBO waiting, COTI open and running, ACH (tp2_hit) still open toward tp3. Manage existing positions, don't force new entries.
- **Stocks intraday**: no A/B actionable setups; AMZN manual-review-only (false legal-risk block + already extended); WMT/CAT/NOC C-tier watch-only.
- **Stocks swing/invest**: dormant since 2026-07-02 by design (deprecated pending the shadow-only position framework) — planning-only, no fresh output expected.

## 13. Sources

- Internal: [data/reports/scalp/2026-07-31_19-21_scalp_report.md], [data/reports/intraday/2026-07-31_19-29_intraday_report.md], [data/reports/swing/2026-07-31_17-06_swing_report.md], [data/reports/stocks/intraday/2026-07-31_20-00_stocks_intraday_report.md], [data/catalysts/2026-07-31/catalyst_cycle_19-33.md], `news_items` (Finnhub company-news, "Cheaper Amazon cloud rival files for Chapter 11 bankruptcy," 2026-07-27), `proposed_signals` (DB query, 2026-07-31 23:2x EEST), `data/scheduled_runs/2026-07-31_default_schedule/scheduler.log`.
- No external web sources cited this cycle — internal data was sufficient (see §2).

## 14. Fix Requests / TODO

### TODO-1: `track-signals` pipeline failure — escalated, now with quantified impact
- **issue:** `track-signals` (pre/post variants) has exited with code 1 on
  **6 consecutive** scheduled invocations today: 14:55, 16:38, 18:41, 20:09,
  22:13, 23:00 EEST. Up from 4 at the 21:39 review. Direct, quantified
  consequence verified this cycle: **16/21 crypto** and **167/175 stocks**
  "active" `proposed_signals` are already past their own `expires_at` and
  stuck unresolved — the tracker that should be resolving them to a terminal
  status (stopped/expired/tp3_hit) has not run successfully all day.
- **evidence:** `data/scheduled_runs/2026-07-31_default_schedule/scheduler.log`
  lines with `track-signals.*exit=1` at the six timestamps above. DB query:
  `SELECT count(*) FROM proposed_signals WHERE asset_class='crypto' AND status
  IN ('generated','waiting_for_entry','triggered','tp1_hit','tp2_hit') AND
  datetime(expires_at) < datetime('now')` → 16 (of 21 total); same query with
  `asset_class='stocks'` → 167 (of 175 total).
- **suggested manual fix:** A human session should run `track-signals`
  directly with verbose/debug output captured, identify the exception, and
  fix it. This is now a 6th consecutive failure across two review cycles —
  treat as urgent; the growing unresolved backlog is actively corrupting the
  "active signals" view for every downstream consumer (this review included).
- **priority:** high
- **first observed:** 2026-07-31 14:55 EEST (this run's evidence); originally
  flagged as a 3rd failure in `OPUS_ENRICHED_REVIEW_AUTO_2026-07-31_1847.md`
  TODO-2, escalated to 4th in the 21:39 review, now 6th.

### TODO-3: Stocks backlog re-measured — larger than previously reported
- **issue:** The 21:39 review's TODO-3 measured 153 stocks signals open
  >14 days. A stricter, more direct measure (past-`expires_at`, any age)
  gives **167 of 175** total "active" stocks `proposed_signals` — i.e. 95%
  of the stocks "active" book is actually stuck past its own expiry window,
  not just an old-signal tail. Directly tied to TODO-1.
- **evidence:** DB query above; also `python -m src.cli active-signals
  --asset-class stocks` this cycle shows expires_at values from 2026-07-09
  through 2026-08-01, the great majority already in the past relative to
  today (2026-07-31).
- **suggested manual fix:** Fix TODO-1 first; once `track-signals` runs
  cleanly again, re-measure this backlog to see how much resolves on its own
  vs. how much needs a manual backfill/cleanup pass.
- **priority:** high
- **first observed:** 2026-07-31 21:39 EEST (as 153/14-day); re-measured and
  escalated 2026-07-31 23:24 EEST (167/175 past-expiry).

### TODO-4: Catalyst mapping still weak (chronic)
- **issue:** Unmapped catalyst events sit at 61.7% this cycle vs 63.7-63.8%
  across the prior three cycles today — marginal improvement, still well
  over the 50% "weak" threshold for several consecutive cycles.
- **evidence:** `data/catalysts/2026-07-31/catalyst_events.jsonl` — 3,500
  cumulative events today, 2,158 unmapped (61.7%).
- **suggested manual fix:** Improve the symbol resolver in the catalyst
  layer per the existing tracked initiative in
  [[project_crypto_ai_desk_news_layer_hardening]] (prior symbol-audit found
  only 17% match rate).
- **priority:** medium
- **first observed:** 2026-07-31 21:39 EEST (chronic, pre-existing).

### TODO-5: "GE" ticker news-symbol ambiguity (carried, not re-verified this cycle)
- **issue:** Carried unchanged from the 21:39 review — GE-tagged news rows
  were actually about Portland General Electric (POR), not General Electric.
  Not re-checked this cycle; still a latent risk for any GE-tagged signal.
- **evidence:** See `OPUS_ENRICHED_REVIEW_AUTO_2026-07-31_2139.md` TODO-5.
- **suggested manual fix:** Disambiguate ticker "GE" in the news symbol
  detector; part of [[project_crypto_ai_desk_news_layer_hardening]].
- **priority:** low
- **first observed:** 2026-07-31 21:39 EEST.

### TODO-6: AMZN "going_concern" legal-risk false positive (new)
- **issue:** A genuine A-tier (score 86.2) post-earnings AMZN long was
  demoted to C/non-actionable today by `legal_headline_risk: going_concern`.
  Root cause: the only AMZN-tagged news row matching the going-concern/
  bankruptcy regex over a 90-day lookback is "Cheaper Amazon cloud rival
  files for Chapter 11 bankruptcy" (Finnhub, 2026-07-27) — a story about a
  competitor, not Amazon. The symbol resolver appears to attach AMZN to any
  headline containing the word "Amazon," including ones where Amazon is only
  a point of comparison.
- **evidence:** SQL: `SELECT title, source, published_at FROM news_items
  WHERE detected_symbols_json LIKE '%AMZN%' AND (LOWER(title) LIKE '%going
  concern%' OR LOWER(title) LIKE '%bankrupt%' OR LOWER(title) LIKE '%chapter
  11%') AND datetime(published_at) > datetime('now','-90 days')` → exactly 1
  row, the "cloud rival" headline above. No other AMZN news in the last 48h
  supports any legal/going-concern risk (AMZN's own news is uniformly
  earnings-positive: AWS growth, tariff refunds, analyst upgrades).
- **suggested manual fix:** Tighten the `going_concern`/bankruptcy pattern
  match (or the symbol-attachment step feeding `load_active_legal_news` in
  `src/stocks/legal_risk.py`) to require the flagged company to be the
  subject of the bankruptcy/going-concern language, not merely mentioned as a
  competitor/comparison. Consider a broader audit of the 90-day persistent
  legal-flag window for similar "competitor mentioned in headline" false
  positives on other symbols.
- **priority:** high
- **first observed:** 2026-07-31 23:24 EEST.
