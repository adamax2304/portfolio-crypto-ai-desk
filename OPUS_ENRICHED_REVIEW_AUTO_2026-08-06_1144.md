# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:30 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context** (target 11:30 EEST, this run's data-gathering window ~11:39-11:44 EEST). **Advisory only — no auto-trade.** US cash market is not yet open (opens ~16:30 EEST); all stocks context below is pre-market planning/watchlist, not live. Zero A-tier anywhere, crypto or stocks, again this run — an unbroken streak. Crypto tape is constructive: BTC ~$64,500-64,800 (externally verified, uptrend), ETH ~$1,870-1,880 (transition_up per swing report, uptrend per fresher scalp/intraday), altcoin breadth 53-60% above EMA20, regime "bullish trend (risk-on)" / "selective longs; prefer pullbacks on relative strength" across all three crypto reports. Against that backdrop, macro/geopolitics risk score is **pinned at the 100/100 ceiling** for the second consecutive review (was 98.2/100 at 04:50 EEST, worse now) — Iran/Strait-of-Hormuz tension remains the dominant risk-off driver even as the tape stays green, a genuine mood/risk-score divergence worth flagging rather than resolving either way. The **HOME/USDT weakest-symbol-vs-active-long contradiction is now unresolved for roughly 19h41m** (first flagged ~15:58 EEST 2026-08-05, still present on both the freshest scalp and intraday weakest-symbols tables at 07:41-07:48 EEST today) — the longest-running data-consistency flag this desk has tracked. Good news: **EPIC/USDT's parallel contradiction (which resolved, then re-emerged at the 04:50 review) has resolved again** — off both fresh weakest-symbols tables this cycle. The **crypto scalp kill-switch registration bug flagged at 04:50 EEST (6 signals registered against an explicit "never registered" production guarantee) produced zero new instances this cycle** — a direct DB query confirms no scalp-mode signals have been created since 04:50 EEST; the underlying code path is still unfixed (root cause untouched) but the gap did not recur this cycle. Today's live event: **SpaceX's ~911.5M-share, ~$104B lockup unlock lands today (Aug 6)** — externally reconfirmed (stock already down >6% pre-unlock, -43% from IPO peak) — SPCXB/USDT (tokenized proxy) remains the desk's best catalyst-backed idea but is still capped to C for squeeze risk with no derivatives data and no defined bearish entry. The current top live idea per the freshest intraday report is **LONG DODO/USDT (B-tier, 68.6, waiting_for_entry)** — same no-catalyst momentum family the desk has run for three days, tagged in-house `avoid_chase` (momentum_breakout basket). Catalyst mapping **worsened** to **62.4% unmapped** (from 60.6% at 04:50 EEST, continuing a multi-cycle pattern now above 50% for at least four consecutive reviews). 0 untracked legacy alerts this cycle (clean).

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-06_07-41_scalp_report.md` (data freshness 07:30 UTC, generated 10:41 EEST — ~1h old, freshest source; **A/B empty this cycle** — scalp mode correctly showing zero fires, consistent with the kill-switch holding clean), `data/reports/intraday/2026-08-06_07-48_intraday_report.md` (generated 10:48 EEST — ~1h old, fresh; 1 B-tier long DODO/USDT, 1 B-tier long SYN/USDT), `data/reports/swing/2026-08-06_02-35_swing_report.md` (generated 05:35 EEST — ~6h old, **carry-forward band 4-12h**, flagged; 6 B-tier longs MIRA/KITE/TUT/BICO/SYN/HEI).
- Stocks: `data/reports/stocks/intraday/2026-08-06_08-12_stocks_intraday_report.md` (generated 11:12 EEST — ~32min old, freshest source this cycle; **market closed (after-hours/pre-market UTC overnight)** — all A/B demoted to C, `market_closed_intraday_planning_only`; 84 symbols ok, 0 fail).
- Stocks swing/invest: last generated 2026-07-02 — **stale >1 month, excluded** per standing policy (deprecated old framework).
- `data/catalysts/2026-08-06/catalyst_events.jsonl` (cumulative today, direct read: 752 mapped / 1248 unmapped of 2000 rows = 62.4% unmapped), `narrative_baskets.jsonl` and `catalyst_cycle_07-52.md` (freshest scan: 500 news_items scanned, 500 events, 2 baskets — `ai_narrative` NEAR/RENDER/TAO/FET/WLD/ASTER, `momentum_breakout` HEI/DODO/HFT/ZBT playbook `avoid_chase`).
- CLI: `active-signals --asset-class crypto` (42 rows: DODO/USDT intraday B waiting_for_entry, 6 swing B triggered/waiting from the overnight cluster, HOME/USDT x2 swing triggered, EPIC/USDT swing triggered, STO/USDT swing triggered 78.1 — steadiest, plus legacy tp-hit/expiry remnants), `active-signals --asset-class stocks` (50 rows, all C-tier or legacy expiry remnants, 0 A/B actionable), `signal-stats --asset-class crypto` (weekly: tier B n=124, PF 2.71, avgR 0.40, triggered winrate 24% — CLI's own observation flags this as low; weekend-mode signals underperform, winrate 11% n=10 — also CLI-flagged), `signal-stats --asset-class stocks` (weekly: tier C n=225, triggered winrate 2%, PF 0.79 — both below the CLI's own flag thresholds, unchanged known pattern), `detect_untracked_legacy_alerts --since 2026-08-06` (**0 untracked** — clean).
- DB (read-only queries): `proposed_signals` filtered `mode='scalp' AND created_at > '2026-08-06T04:50:00'` → **0 rows** (confirms the kill-switch registration bug produced no new instances since it was flagged); `news_items` filtered on DODO/SPCX symbol tags in the last 24h (DODO: 0 fresh catalyst rows — confirms "no fresh verified catalyst" is accurate, not a missed-catalyst false negative; SPCX: 2 rows, both the same Aug 5 earnings/unlock article already ingested last cycle).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_0450.md` (crypto overnight / Asia review, 04:50 EEST).
- **External web research invoked this cycle** (WebSearch x2, no WebFetch needed — search snippets were sufficient and directly answered both queries): BTC/ETH current level check; SpaceX (SPCX) unlock-day price-reaction check.

## 3. Scheduler / Data Freshness

- Cron target 11:30 EEST; this run's data-gathering window ~11:39-11:44 EEST — within tolerance.
- `scheduler.log` in `data/scheduled_runs/2026-08-05_default_schedule/` (still the live cycle folder, date-stamped from when it started but continuously active past midnight) — mtime 11:24 EEST, ~15-20min old at review start — fresh, not deferred. Latest `cycle_05_10-33_summary.md` mtime 11:24 EEST — ~15-20min old — well within the 3h defer threshold.
- Crypto scalp ~1h old (freshest, and correctly empty), intraday ~1h old (fresh), swing ~6h old (**carry-forward band, 4-12h** — cross-checked against fresher scalp/intraday where they diverge; ETH trend read is the one material divergence, "transition_up" in the 6h-old swing report vs "uptrend" in the two fresher reports).
- Stocks: 08:12 EEST-generated report (11:12 EEST) — 84/84 symbols, 10/10 indices, 12/12 sector ETFs succeeded, no data-fetch issues.
- Data-quality anomalies this cycle: (1) catalyst mapping weak and **worsening**, 62.4% unmapped vs 60.6% at 04:50 EEST — now above the 50% weak-mapping threshold for at least four consecutive reviews, TODO carried and escalated; (2) crypto scalp kill-switch registration bug — **0 new instances since 04:50 EEST** (verified by direct query), root cause still unfixed but no fresh evidence of recurrence this cycle — downgrading urgency language, not priority, pending a human fix; (3) HOME/USDT weakest-symbol-vs-active-long contradiction — unresolved, now ~19h41m and counting, the longest-running instance tracked; (4) EPIC/USDT's parallel contradiction has **resolved again** (off both fresh weakest-symbols tables this cycle) — third state-flip in ~24h (present→resolved→present→resolved), reinforcing the resolve-then-recur hypothesis is real and worth a focused human check on shared root cause with HOME/USDT.
- **TradingView / manual chart check unavailable** — no chart MCP loaded this cycle; all price-structure statements are from local OHLCV/ATR/EMA fields in the reports plus the two external WebSearch checks cited above.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-06 11:44 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["no fresher swing report than ~6h-old 05:35 EEST snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log and latest cycle summary both ~15-20min old, well within tolerance", "crypto swing report ~6h old (carry-forward band), scalp/intraday ~1h old (fresh)", "stocks report 84/84 symbols ok, no fetch issues", "0 untracked legacy alerts this cycle"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": ["no live intraday BTC/ETH tick beyond internal reports + WebSearch morning-level check"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC ~$64,500-64,800 (externally verified), uptrend; ETH ~$1,870-1,880, uptrend (fresher reports) / transition_up (6h-old swing report)", "altcoin breadth 53.49-55.56% above EMA20 (swing, stale) vs 60.47% (scalp/intraday, fresh) -- directionally healthy, moderating slightly intraday", "macro/geopolitics risk PINNED AT 100/100 ceiling, worse than 98.2/100 at last review -- Iran/Hormuz still the dominant driver, a genuine mood-vs-risk-score divergence against the green tape", "US cash market not yet open (~16:30 EEST); last verified stocks state is Wednesday's close, bullish regime, VIX 15.85"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["62.4% unmapped today (1248/2000 in the cumulative catalyst_events.jsonl), worse than 60.6% at 04:50 EEST -- now a persistent 4+ cycle pattern above the 50% threshold", "freshest scan cycle (07:52 EEST) narrowed to 2 active baskets: ai_narrative (NEAR/RENDER/TAO/FET/WLD/ASTER) and momentum_breakout (HEI/DODO/HFT/ZBT, playbook avoid_chase)", "DODO/USDT -- today's top live idea -- carries zero fresh catalyst rows in a direct 24h news_items query, confirming the report's own 'no fresh verified catalyst detected' is accurate, not a missed-catalyst gap", "SPCXB/USDT's catalyst case is now live-event-day: the >$100B SpaceX unlock is happening TODAY (Aug 6), externally reconfirmed"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["no fresh per-symbol funding/OI beyond what the scalp/intraday reports embed"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HFT/USDT: funding 0.0036, 'extreme long crowding' -- standing flag, carried across multiple reviews without a loss yet", "DODO/USDT: negative funding across external venues (mexc -0.0006), 'crowding moderate' -- no red flag but no strong confirmation either", "SPCXB/USDT: 'no_derivatives_thin_short', squeeze-risk capped to C in every report -- unchanged, no actionable short despite today's live catalyst event"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "entry_fresh", "clean_retest", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["DODO/USDT intraday: current price 0.0284 sits above the defined pullback entry zone 0.026058-0.027714 -- a genuine pullback-wait, not a chase; if price fills inside the zone before invalidation (0.024035) the entry is clean by the report's own logic", "DODO/USDT carries the funnel's own avoid_chase basket tag (momentum_breakout) -- extra scrutiny warranted despite the clean zone logic", "SYN/USDT intraday (65.4, triggered) and the 6-name overnight swing cluster (MIRA/KITE/TUT/BICO/SYN/HEI) are unchanged holds from the last review, no new fills or stops since 04:50 EEST", "0 new scalp-mode registrations since 04:50 EEST -- the kill-switch gap did not recur this cycle"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry"],
      "data_missing": ["CLI does not label lifecycle state directly -- classification is manual, from active-signals status + signal_outcomes joins"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto CLOSED since last review: none newly closed -- no fresh TP/stop hits observed between 04:50 and 11:44 EEST on the tracked cluster", "Crypto OPEN actionable / ENTERED UNRESOLVED: STO/USDT swing (78.1, triggered, steadiest, unchanged), FIDA/USDT swing (68.5, triggered, still no TP), HOME/USDT x2 swing (triggered, contradiction unresolved), EPIC/USDT swing (triggered, contradiction resolved again), 6-name overnight cluster (mostly triggered/waiting, unchanged)", "Crypto WAITING for entry: DODO/USDT intraday (fresh this cycle, 68.6), HEI/USDT swing (67.4, waiting)", "Stocks: 0 OPEN, all 50 rows C-tier or legacy expiry remnants; 0 new A/B fired; market not yet open"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["manual_review", "legal_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOME/USDT: weakest-symbol-vs-active-long contradiction now unresolved for ~19h41m, the longest-running instance of this pattern tracked so far -- escalating urgency language in this review", "EPIC/USDT: resolved again this cycle -- third state-flip in ~24h, reinforcing a resolve-then-recur pattern distinct from HOME/USDT's continuous one", "Macro/geopolitics risk pinned at 100/100 -- a mood-vs-risk-score divergence against an otherwise green crypto tape, worth treating as a standing caution rather than a directional call", "MSFT (stocks, raw A, demoted to C for market-closed + legal risk): active legal-headline risk (class_action, securities_fraud) confirmed again, unchanged", "0 untracked legacy alerts this cycle -- clean read on the previously-confirmed watchlist-alert/signal-reuse bug pattern"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly (tier B, n=124, reliable): PF 2.71, avgR 0.40, triggered winrate 24% -- CLI's own observation flags this as low despite healthy PF; weekend-mode signals separately flagged as underperforming (winrate 11%, n=10)", "stocks weekly (tier C, n=225, reliable): triggered winrate 2%, PF 0.79 -- both below the CLI's own flag thresholds, unchanged known pattern, C-tier never actionable", "no new closed trades since the last review to update the overnight-cluster running tally (was net +1.0R at 04:50 EEST)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH tape constructive, breadth healthy, but macro/geopolitics risk pinned at the 100/100 ceiling -- a genuine divergence, not a clean risk-on read; treat as selective, not unambiguous", "DODO/USDT is the cleanest fresh long-watch this cycle (defined pullback zone, no same-day negative history) but carries an in-house avoid_chase tag -- confirm the pullback fills cleanly before treating as high-conviction", "SPCXB/USDT's catalyst is now live (unlock happening today) but still has no defined bearish entry or derivatives data -- remains watch-only", "HOME/USDT's contradiction has now run long enough (~19h41m) to warrant explicit avoid-fresh-exposure language; EPIC/USDT's resolve-then-recur pattern is a second, related data point", "stocks: market not yet open, nothing actionable; MSFT legal-risk gate still live for the pre-US watchlist"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "DODO/USDT", "trigger": "intraday B-tier (68.6) waiting_for_entry, fill only inside 0.026058-0.027714, invalidation 0.024035 -- cleanest fresh long-watch this cycle, but carries an in-house avoid_chase (momentum_breakout) tag; confirm pullback fills cleanly, do not chase the current 0.0284 level" },
    "best_short_candidate":    { "symbol": "HOME/USDT", "trigger": "persistent weakest-symbol read (bias short, -8.38% 24h) now unresolved ~19h41m against 2 active triggered longs -- NOT a tradeable short (no defined breakdown structure exists), listed here as the desk's clearest short-side technical read pending reconciliation" },
    "best_catalyst_candidate": { "symbol": "SPCXB/USDT", "trigger": "weak_rs_short watchlist tag; real SpaceX (SPCX) ~911.5M-share / ~$104B unlock lands TODAY (Aug 6, externally reconfirmed, stock already -43% from IPO peak) -- needs a confirmed bearish HTF structure + derivatives data + clear stop above swing high before actionable; still capped for squeeze risk" },
    "avoid_candidate":         { "symbol": "HOME/USDT", "reason": "weakest-symbol-vs-active-long contradiction unresolved for ~19h41m, the longest-running instance tracked; 2 active triggered long swing positions against a persistent bias-short technical read -- do not add fresh exposure either direction until reconciled" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.65 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.6 | risk_on, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.5 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, entry_fresh, clean_retest, entry_late | advisory_only |
| execution_lifecycle | ok | 0.6 | open_actionable, waiting_for_entry, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.6 | manual_review, legal_risk, reduce_risk | advisory_only |
| playbook_performance | ok | 0.6 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.6 | risk_on, longs_preferred, wait_for_trigger, manual_review | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_0450.md` (04:50 EEST, crypto overnight / Asia review):

- **Closed since 04:50:** none observed — no fresh TP/stop hits on the tracked cluster between 04:50 and 11:44 EEST; STO/USDT, FIDA/USDT, the 6-name overnight cluster, HOME/USDT and EPIC/USDT positions are all unchanged holds.
- **New:** DODO/USDT intraday B-tier (68.6) registered `waiting_for_entry` this cycle — today's cleanest fresh long-watch, though it carries the in-house `avoid_chase` tag.
- **Resolved:** the 6 scalp signals flagged at 04:50 EEST as a kill-switch registration bug have produced **0 new instances** — direct DB query confirms no scalp-mode signal has been created since 04:50 EEST. The underlying code path is still unfixed (this is not a fix, just an absence of new evidence), so the TODO stays open but its urgency language is downgraded this cycle.
- **Resolved again:** EPIC/USDT's weakest-symbol-vs-active-long contradiction — present at 04:50 EEST, now off both fresh weakest-symbols tables (07:41/07:48 EEST reports). This is the third state-flip in roughly 24h (present → resolved → present → resolved), which strengthens rather than weakens the case that this is a recurring pattern worth a focused human check, not noise.
- **Unresolved, escalated:** HOME/USDT's contradiction — still present, now spanning ~19h41m since first flagged, the longest-running instance of this class of finding tracked by this review series.
- **Worsened:** catalyst mapping 60.6% → **62.4%** unmapped (cumulative-file read), continuing the multi-cycle pattern, now above 50% for at least 4 consecutive reviews.
- **Worsened:** macro/geopolitics risk 98.2/100 → **100/100** (back at the ceiling) despite the crypto tape staying green — a genuine mood/risk-score divergence, not necessarily bearish but worth tracking as elevated tail risk.
- **New context:** SPCXB/USDT's underlying catalyst (SpaceX ~$104B unlock) has moved from "landing today" (as framed at 04:50 EEST) to actually happening today — externally reconfirmed via a fresh WebSearch (911.5M shares, stock already down >6% pre-unlock, -43% from IPO peak). No change to actionability — still capped, no defined entry.
- **Invalidated:** none.

## 5. Catalyst Coverage

- Cumulative today (`catalyst_events.jsonl`, direct read): mapped **752**, unmapped **1248**, total **2000** rows → **62.4% unmapped**, worse than 60.6% at 04:50 EEST.
- Freshest single scan (`catalyst_cycle_07-52.md`, 07:52 EEST): 500 `news_items` scanned, 500 events, 2 active narrative baskets — `ai_narrative` (NEAR/RENDER/TAO/FET, related WLD/ASTER, playbook `related_beta_rotation`) and `momentum_breakout` (HEI/DODO/HFT primary, related ZBT, playbook `avoid_chase`, fresh <1h).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** 62.4% unmapped, worsening, now above the 50% threshold for at least 4 consecutive reviews.
- Top unmapped headlines (sample): "Inside India newsletter: What's behind India's rush to sell shares in state-owned firms," "U.S. is ready to return to 'commitments,' Iran says, after Trump signals deal is near," "MercadoLibre outlines continued reinvestment as credit portfolio reaches $16.4B," "Teknova targets less than $8M 2026 free cash outflow as it lifts revenue guide to $45M-$47M," "Talen outlines higher 2026 guidance to $2.025B-$2.225B adjusted EBITDA" — mostly macro/earnings-wire items without a clean single-symbol tag, consistent with prior cycles' pattern.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **selective risk-on, with an elevated-risk caveat** — BTC ~$64,500-64,800 (externally verified), uptrend; ETH ~$1,870-1,880, uptrend (fresh reports) / transition_up (6h-old swing report); altcoin breadth 53-60% above EMA20 depending on report freshness. Regime label unchanged: "bullish trend (risk-on)," recommended style "selective longs; prefer pullbacks on relative strength." Against this, macro/geopolitics risk is **pinned at 100/100** — worse than 98.2/100 at the last review — Iran/Strait-of-Hormuz tension remains the dominant driver even as price stays constructive. Treat this as a standing background caution, not a reason to flip bearish.
- Stocks mood: **pre-market / not yet open** — US cash session opens ~16:30 EEST (09:30 ET); last verified state is Wednesday's bullish close (VIX 15.85, breadth 100% above EMA20/50, all 4 major indices uptrend). All stocks context below is planning/watchlist only, building the US-session view ahead of the open — not confirmed actionable until RTH.
- Dominant narrative: the no-catalyst-momentum cluster (DODO/SYN/HEI/KITE/TUT/BICO/HFT family) remains the desk's most active playbook, unchanged since 04:50 EEST with a new fresh fire on DODO/USDT intraday; SPCXB/USDT's catalyst is now a live-event-day story (the >$104B unlock is happening today) but remains execution-blocked on entry-structure and derivatives-data grounds.
- Preferred side now: **longs (crypto, selective)** — tape constructive but elevated macro risk argues for measured sizing; **watch-only (SPCXB short)** — strongest catalyst case, still no defined entry; **wait (stocks)** — market not yet open, build the watchlist, do not treat pre-market/planning levels as actionable.
- Best long candidate: **DODO/USDT** (intraday B-tier, fresh waiting_for_entry, clean pullback zone, but carries an avoid_chase tag) — see §7/§8.
- Best short candidate: **HOME/USDT is the clearest technical read but is explicitly NOT tradeable** — no defined breakdown structure exists; treat this as a data-consistency flag, not a short idea, until reconciled. Absent that, no clean short exists this cycle.
- Best catalyst-backed candidate: **SPCXB/USDT** (weak_rs_short, live-event-day SpaceX unlock) — see §7.
- What to avoid: **HOME/USDT** fresh exposure either direction (unresolved ~19h41m); the crypto scalp mode generally (root cause of the registration bug still unfixed, even though no new instances appeared this cycle); chasing DODO/USDT above its defined pullback zone.
- What would change the view: macro/geopolitics risk easing off the 100/100 ceiling; a human reconciling HOME/USDT's contradiction (and ideally explaining EPIC/USDT's resolve-then-recur pattern as a related root cause); a confirmed bearish HTF structure appearing for SPCXB/USDT once derivatives data becomes available; the US cash open providing a fresh, live stocks read.

## 7. Candidate Deep Dives

### DODO/USDT (crypto intraday, B-tier long, 68.6, waiting_for_entry — today's cleanest fresh long-watch)
- Has price already reacted to the catalyst? No fresh verified catalyst exists (confirmed by direct 24h `news_items` query — 0 rows) — this is a pure momentum/RS thesis, same family the desk has run for three days.
- Is the setup chasing? Current price 0.0284 sits **above** the defined pullback entry zone (0.026058-0.027714) — this is a wait-for-pullback setup, not a chase, by the report's own logic. However, DODO/USDT is also a `momentum_breakout` narrative-basket primary with playbook `avoid_chase` — the funnel itself flags this family as one that has already moved a lot (54-59% 24h across reports) without confirmed news.
- Retest/pullback structure? Yes, explicitly defined: entry 0.026058-0.027714, invalidation (1h close beyond) 0.024035, TP1/TP2/TP3 0.0321/0.0358/0.0395.
- Would entry now be late? Only if bought at the current 0.0284 level without waiting for the pullback — the report explicitly warns "no market buy if extended."
- Is this aligned with market mood? Yes — bullish-trend regime, selective-longs style, RS vs BTC +53.9-54.0% across reports.
- Long/short/wait: **wait for the pullback fill inside the defined zone; do not chase above 0.0284.**
- Chase-risk: elevated by the basket tag despite the technically clean zone logic — treat as medium confidence per the report's own label, not high.
- Catalyst confirmation/contradiction: none found; pure technical setup, consistent across every report tonight and this morning.

### HOME/USDT (crypto — weakest-symbol vs active-long contradiction, unresolved, ~19h41m and counting)
- Still on the freshest scalp (07:41 EEST) and intraday (07:48 EEST) weakest-symbols tables: bias short, 24h -8.38%, RS vs BTC -9.34% to -9.47%, while carrying 2 active triggered long B-tier swing positions (68.5 and 67.3, one weekend-mode) with invalidations at 0.008703 and 0.005879 respectively, both untouched.
- This is now the longest-running instance of this specific class of finding tracked across this review series (first flagged ~15:58 EEST 2026-08-05).
- Would a fresh entry now be late (for a hypothetical short)? Yes — no defined short setup exists for HOME/USDT in any report; this remains a flag, not a tradeable idea.
- What level would make a short actionable? Only after the desk's own scanner generates a confirmed failed-bounce/breakdown structure — none exists currently.
- Mood alignment: the bias-short read cuts against the broader crypto risk-on tape — idiosyncratic/technical, not market-wide.
- Long/short/wait: **wait** — do not add fresh exposure in either direction; monitor whether either existing long's invalidation is hit.
- Chase-risk: N/A. Catalyst confirmation/contradiction: none found; pure internal-consistency flag, now the highest-priority carried TODO (§14).

### SPCXB/USDT (crypto, weak_rs_short watchlist tag — best catalyst-backed candidate, live-event-day)
- Has price already reacted to the catalyst? Yes, and the event is now live: real-world SpaceX (SPCX) stock has already fallen >6% pre-unlock on top of its prior -13.61% Aug 5 close, now roughly **-43% from its IPO-era peak**; the ~911.5M-share (~$104B) lockup unlock is landing **today, Aug 6** (externally reconfirmed via fresh WebSearch — not just the Aug 5 pre-announcement framing carried from the last review).
- Is the setup chasing? The desk's own funnel still tags SPCXB/USDT `weak_rs_short` (`crypto_failed_bounce_short` playbook) but caps it to C for "short squeeze risk" and "no_derivatives_thin_short" — unchanged since the last review.
- Retest/pullback structure? No defined short entry exists yet in any report; the watchlist tag explicitly requires "confirm bearish HTF structure + derivatives data + clear stop above swing high" before actionable.
- Would entry now be late? Not assessable — no defined entry exists. Because the unlock is a same-day, still-unfolding event, any confirmed bearish structure that emerges during the session should be treated as fresh, not late.
- What level makes it actionable cleanly? A confirmed bearish HTF structure with a clear stop above the recent swing high, once derivatives (funding/OI) data becomes available for this symbol.
- Mood alignment: cuts against the broader crypto risk-on tape — an idiosyncratic, catalyst-driven weakness in a single tokenized-equity proxy, not a market-wide signal.
- Long/short/wait: **watch-only** — no defined entry exists; remains the desk's cleanest catalyst-confirmed idea, now on the actual event day.
- Chase-risk: N/A (no entry defined). Catalyst confirmation: **strong, live, externally reconfirmed this cycle** (§13).

### STO/USDT (crypto swing long, triggered, B-tier, 78.1 — steadiest carried position)
- Highest-scoring active B-tier signal on the book; unchanged status since the last review (triggered, no TP hit yet, expires 2026-08-11).
- Has price already reacted to a catalyst? No — no fresh verified catalyst; pure RS/momentum thesis, unchanged.
- Long/short/wait: **hold** — no new information this cycle, no action needed.
- Chase-risk: N/A (already filled, holding). Catalyst confirmation/contradiction: none.

*(Excess candidates not given a full deep dive, per the 5-candidate cap: EPIC/USDT — contradiction resolved again this cycle, see §4, no longer needs a full dive but flagged as a recurring-pattern data point; FIDA/USDT swing — still triggered/unresolved, no new information beyond §4; the 6-name overnight cluster (MIRA/KITE/TUT/BICO/SYN/HEI swing) — unchanged holds, no fresh fills or stops; SYN/USDT intraday (65.4, triggered) — same family as DODO, unchanged; all stocks C-tier names (MSTR/MSFT/JPM/NVDA/DIA/XLF/NFLX/PLTR/XLV/QQQ/XLY/IWM/LLY/AVGO/XOM) — market not yet open, planning-only, MSFT carries the standing legal-risk gate, no new information.)*

## 8. Best Candidates Ranked

1. **STO/USDT (crypto swing long, triggered, B-tier, 78.1)** — steadiest open position, unchanged; hold.
2. **FIDA/USDT (crypto swing long, triggered, B-tier, 68.5)** — filled, no TP yet; hold, watch invalidation 0.018671.
3. **DODO/USDT (crypto intraday long, waiting_for_entry, B-tier, 68.6)** — best fresh long-watch this cycle; fill only inside 0.026058-0.027714, invalidation 0.024035; caveat: carries the in-house avoid_chase basket tag.
4. **SPCXB/USDT (crypto, weak_rs_short watchlist, capped C)** — best catalyst-backed watch, now on the live unlock event day; no defined entry yet, watch for a confirmed bearish structure.
5. **The 6-name overnight swing cluster (MIRA/KITE/TUT/BICO/SYN/HEI)** — unchanged holds since 04:50 EEST, no new fills or stops; included as the steady core of the book, not a fresh idea.

**HOME/USDT** (unresolved contradiction, ~19h41m, avoid fresh exposure either direction) is this cycle's explicit avoid name — see §6/§9. **EPIC/USDT** has resolved again but remains on watch given its resolve-then-recur history. No stocks name is actionable (market not yet open); the pre-US watchlist to carry into the 16:20 pre-open slot is MSTR/MSFT/JPM/NVDA (highest-scoring raw-A names, all demoted to C purely for market-closed reasons except MSFT which also carries the legal-risk gate).

## 9. Avoid / No Trade

*(This applies to this decision window only — scanning, tracking, and the scheduler continue unchanged.)*

- **HOME/USDT any fresh direction** — unresolved weakest-symbol-vs-active-long contradiction, now ~19h41m, the longest-running instance tracked; needs manual review before new exposure either way.
- **Chasing DODO/USDT above its defined pullback zone (0.026058-0.027714)** — the setup is only clean inside the zone; current price 0.0284 is above it.
- **Crypto scalp mode generally** — weekly PF pattern historically weak (consistent with the documented 2026-07-07 kill-switch rationale); the mode should not be trading at all right now, and while 0 new registration-bug instances appeared this cycle, the underlying code gap is still unfixed (§14).
- **All stocks C-tier watchlist names** (MSTR, MSFT, JPM, NVDA, DIA, XLF, NFLX, PLTR, XLV, QQQ, XLY, IWM, LLY, AVGO, XOM) — market not yet open, planning-only; MSFT additionally carries a standing legal-risk gate (class_action, securities_fraud).
- **SPCXB/USDT as a live trade** — catalyst confirmation is real and the unlock is happening today, but no defined bearish entry structure or derivatives data exists yet; watch-only.

## 10. Main Risks

- **HOME/USDT's contradiction has now run ~19h41m**, the longest-running instance of this pattern tracked by this review series; combined with **EPIC/USDT's third state-flip in ~24h**, this reinforces rather than resolves the hypothesis of a shared, recurring root cause in how the momentum-ranking table and the swing-signal book read OHLCV windows (§14, carried).
- Macro/geopolitics risk is **pinned at the 100/100 ceiling**, worse than the prior review's 98.2/100, despite a green crypto tape — a genuine mood/risk-score divergence that argues for measured sizing on any fresh crypto exposure, not a directional call in either direction.
- Catalyst mapping remains weak and **worsened** this cycle (62.4% unmapped vs 60.6%) — now above the 50% weak-mapping threshold for at least 4 consecutive reviews; treat all catalyst-basket framing as directional color only.
- The crypto scalp kill-switch registration bug's root cause is **still unfixed** even though 0 new instances appeared this cycle — a control that only partially holds under a "never registered, never alerted" guarantee remains a genuine risk until a human traces and closes the gap.
- DODO/USDT and the broader no-catalyst-momentum cluster carry an in-house `avoid_chase` tag while remaining the desk's most actively re-fired family across multiple sessions — track whether this specific chase-flag-recurrence pattern resolves cleanly or repeats the mixed (win/loss) record seen over the last two days.
- Stocks remain pre-market; nothing has been live-tested since Wednesday's verified close — treat all stocks context as planning only until the ~16:30 EEST RTH open.

## 11. Action Plan — next 4 hours

- Hold STO/USDT and FIDA/USDT swing positions into their invalidations/targets; no new sizing.
- Let DODO/USDT intraday fill cleanly inside its defined pullback zone (0.026058-0.027714) or expire — do not chase the current 0.0284 level.
- Let the 6-name overnight swing cluster and SYN/USDT intraday continue to resolve naturally (fill, TP, or invalidation) — no action needed.
- Do not open any fresh HOME/USDT position (long or short) until its contradiction is manually reconciled; treat EPIC/USDT's resolve-then-recur pattern as a related but distinct data point worth cross-referencing when investigating root cause.
- Watch SPCXB/USDT for a confirmed bearish structure through the SpaceX unlock event today; watch for the US cash open (~16:30 EEST) to refresh the stocks picture ahead of the 16:20 pre-US-open decision review.
- Continue scanning/tracking/monitors unchanged through the European morning into the US pre-open — this review recommends caution on specific entries and one carried control-gap tracking item only, never a pause of any kind.

## 12. Final Verdict per Mode

- **Crypto scalp:** should be fully disabled per the documented 2026-07-07 kill-switch; correctly showing zero fires in the freshest report this cycle, and the registration-bug gap produced 0 new instances since 04:50 EEST — a clean cycle on evidence, but the underlying code path is still unfixed. Treat scalp as **not tradeable** regardless of any score shown.
- **Crypto intraday:** DODO/USDT (68.6) and SYN/USDT (65.4) are the live B-tier ideas; DODO is the cleaner fresh setup pending its pullback fill; both carry no-catalyst / avoid_chase caveats.
- **Crypto swing:** the desk's steadiest bucket — STO/USDT (78.1) and FIDA/USDT (68.5) hold unchanged; the 6-name overnight cluster (MIRA/KITE/TUT/BICO/SYN/HEI) unchanged; HOME/USDT flagged avoid (unresolved contradiction, ~19h41m); EPIC/USDT resolved again but watch for recurrence.
- **Stocks intraday:** market not yet open (pre-market/after-hours UTC-overnight session); zero actionable A/B; MSTR/MSFT/JPM/NVDA are the highest-scoring pre-US watchlist names to carry into the 16:20 pre-open review, MSFT with a standing legal-risk gate.
- **Stocks swing/invest:** not evaluated — reports stale/deprecated since 2026-07-02, excluded per standing policy.

## 13. Sources

- Internal: `data/reports/scalp/2026-08-06_07-41_scalp_report.md`, `data/reports/intraday/2026-08-06_07-48_intraday_report.md`, `data/reports/swing/2026-08-06_02-35_swing_report.md`, `data/reports/stocks/intraday/2026-08-06_08-12_stocks_intraday_report.md`, `data/catalysts/2026-08-06/catalyst_events.jsonl`, `data/catalysts/2026-08-06/narrative_baskets.jsonl`, `data/catalysts/2026-08-06/catalyst_cycle_07-52.md`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items` read-only queries), `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_0450.md`.
- External (WebSearch x2, no WebFetch needed this cycle):
  - [Bitcoin and ethereum prices today, Wednesday, August 5, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-august-5-2026-crypto-prices-rise-as-investors-watch-hormuz-negotiations-and-jobs-report-closely-124640660.html) — BTC opened $64,052.56, moved to $64,486.72; ETH opened $1,868.36, moved to $1,880.89 (Aug 5 data, most recent available at query time). Used for directional framing only.
  - [Nearly 1 Billion SpaceX Shares Unlock On Aug. 6 — The Motley Fool](https://www.fool.com/investing/2026/08/05/spacex-s-911-5-share-unlock-hits-tomorrow-here-s-what-investors-need-to-know/) and [Over $100 billion worth of SpaceX shares unlock tomorrow — Finbold](https://finbold.com/over-100-billion-worth-of-spacex-shares-unlock-tomorrow/) — 911.5M shares (~$104B at ~$114.39/share) unlock today Aug 6; SPCX already down >6% pre-unlock atop the Aug 5 -13.61% close, ~-43% from IPO-era peak. Not re-ingested into `news_items` this cycle — same underlying event already ingested at the 04:50 EEST review (`data/raw/enriched_review_sources/2026-08-06T0440_stocks.json`), confirmed via direct `news_items` query (2 rows, same article).
- No chart/TradingView source this cycle (unavailable, §3).

## 14. Fix Requests / TODO

### TODO-home-usdt-contradiction-second-session-unresolved (priority: high, carried forward, escalated)
- **issue:** HOME/USDT has now shown the weakest-symbol-vs-active-long conflict continuously for **~19h41m** (first flagged ~15:58 EEST 2026-08-05, still present at 07:41-07:48 EEST 2026-08-06): bias-short on the weakest-symbols table (freshest scalp/intraday: score ~68-80, -8.38% 24h) while carrying 2 active triggered long B-tier swing positions (68.5 and 67.3).
- **evidence:** `data/reports/scalp/2026-08-06_07-41_scalp_report.md` and `data/reports/intraday/2026-08-06_07-48_intraday_report.md` "Weakest Symbols" tables (HOME/USDT bias short); `db/crypto_ai_desk.sqlite` `proposed_signals` HOME/USDT swing rows (status=triggered, 2 active, scores 68.5 and 67.3); present in every `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_*.md` and `_2026-08-06_0450.md` review's §14.
- **suggested manual fix:** unchanged from prior cycles — check whether the "weakest symbols" momentum-score calculation and the long-signal scoring pipeline read the same OHLCV window/timeframe for HOME/USDT specifically. Now worth cross-referencing against EPIC/USDT's resolve-then-recur pattern (below) for a possible shared root cause, given EPIC/USDT has now flipped state three times in ~24h while HOME/USDT has stayed continuously in conflict — the difference in behavior between the two symbols may itself be diagnostic.
- **priority:** high
- **first observed:** 2026-08-05 15:58 EEST; carried through every subsequent review; still open 2026-08-06 11:44 EEST (this cycle, now ~19h41m).

### TODO-epic-usdt-contradiction-recurring (priority: medium, recurring instance, updated)
- **issue:** EPIC/USDT's weakest-symbol-vs-active-long contradiction has now flipped state three times in roughly 24h: present (23:35 EEST review or earlier) → resolved (23:35 EEST) → re-emerged (04:50 EEST) → resolved again (this cycle, 11:44 EEST, off both fresh weakest-symbols tables). It still carries 1 active triggered swing long (69.5, weekend-mode).
- **evidence:** `data/reports/scalp/2026-08-06_07-41_scalp_report.md` and `data/reports/intraday/2026-08-06_07-48_intraday_report.md` — EPIC/USDT absent from both fresh "Weakest Symbols" tables this cycle (contrast with `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_0450.md` §7 where it was present); `db/crypto_ai_desk.sqlite` `proposed_signals` EPIC/USDT swing row (status=triggered, score 69.5).
- **suggested manual fix:** a human-driven session should compare EPIC/USDT's and HOME/USDT's OHLCV-window handling side by side — EPIC/USDT's oscillating pattern (vs. HOME/USDT's continuous one) may indicate a threshold-boundary effect (e.g., a rolling-window recalculation flipping the bias near a cutoff) rather than a flat data-source mismatch, which would point to a different, narrower fix than whatever is affecting HOME/USDT.
- **priority:** medium
- **first observed:** 2026-08-05 (exact time not captured pre-23:35 review); resolve-then-recur pattern first noted 2026-08-06 04:50 EEST; third flip observed this cycle 2026-08-06 11:44 EEST.

### TODO-catalyst-mapping-weak-worsening (priority: low, carried forward, worsened)
- **issue:** Catalyst-to-symbol mapping coverage has worsened this cycle: 62.4% unmapped (1248/2000 cumulative rows) vs 60.6% at the 04:50 EEST review, continuing a pattern that has now been above the 50% weak-mapping threshold for at least 4 consecutive reviews (64.2% → 62.2% → 60.6% → 62.4%).
- **evidence:** direct read of `data/catalysts/2026-08-06/catalyst_events.jsonl` (752 mapped / 1248 unmapped of 2000 rows); `data/catalysts/2026-08-06/catalyst_cycle_07-52.md` (freshest single scan, by-type breakdown shows `other_news: 472` of 500, i.e. the large majority of the freshest scan's events land in the generic/unmapped-style bucket).
- **suggested manual fix:** a human-driven session should review the symbol-resolver logic in the catalyst layer (likely `src/news/` or the catalyst-scan agent) to understand why macro/earnings-wire headlines without an explicit ticker mention are not being mapped to any relevant basket or symbol, and whether a broader fuzzy-match or sector-level fallback would reduce the unmapped rate without introducing false positives.
- **priority:** low
- **first observed:** tracked informally across several reviews; first formally escalated to a TODO at 2026-08-06 04:50 EEST; worsened this cycle 2026-08-06 11:44 EEST.

_Note: the crypto scalp kill-switch registration bug (TODO-crypto-scalp-killswitch-registration-bug, first raised 04:50 EEST) produced **0 new instances** this cycle (verified via direct DB query on `mode='scalp' AND created_at > '2026-08-06T04:50:00'`). Not closing this TODO — the underlying code path that allowed the 6 signals to register is still unfixed and unverified as fixed — but downgrading it out of the active §14 list this cycle since there is no fresh evidence to report beyond "still absent." Re-open with full detail immediately if any new scalp-mode `proposed_signals` row appears in a future cycle._
