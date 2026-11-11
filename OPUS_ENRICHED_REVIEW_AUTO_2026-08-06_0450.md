# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:50 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (target 04:30 EEST, this run's data-gathering window ~04:39-04:50 EEST). **Advisory only — no auto-trade.** Stocks are closed during this slot (Asia hours) — all stock context below is planning/watchlist carry-forward only, not live. Zero A-tier anywhere, crypto or stocks, again this run — an unbroken streak across every review tracked so far. Crypto stayed net constructive overnight on the same no-catalyst-momentum cluster the desk has been tracking for two days: **BICO/USDT swing hit TP1 (+1.0R, 00:00 EEST)** — resolving last review's "extra scrutiny, same-day-loss-on-this-symbol" flag with a clean win — and **SYN/USDT intraday extended TP1→TP2 (+1.0R→+2.0R, 23:45 EEST)**. Against that, **ZEC/USDT swing was STOPPED (-1.0R, 03:00 EEST)**, and **FIDA/USDT swing** (last review's cleanest "best long-watch") filled and is now an open ENTERED-and-triggered position with no TP yet. A **fresh wave of six B-tier scalp signals (SYN, MIRA, HEI, KITE, BICO, TUT) registered waiting_for_entry at 04:42-04:43 EEST** — but this is now a confirmed **data-integrity finding, not a tradeable observation**: `config/session_risk.yaml` documents crypto scalp as hard-disabled ("kill-switch... **never registered, never alerted**") since 2026-07-07, yet these six scalp signals were written to `proposed_signals` this cycle (verified `telegram_supported=0`, so the "never alerted" half held, but the "never registered" half did not) — new high-priority TODO (§14). Crypto regime: BTC ~$64,808 (+0.82% overnight, externally verified), uptrend, ETH transition_up, altcoin breadth 62-74% above EMA20 depending on report — healthy but off the prior evening's peak reading. Macro/geopolitics risk eased slightly to **98.2/100** (from 99.9/100 at the last review) — Iran/Strait-of-Hormuz tension is the persistent driver but external reporting shows the first real signs of de-escalation talk overnight. **EPIC/USDT's weakest-symbol-vs-active-long contradiction has RE-EMERGED** (resolved as of last night's review, back on both the freshest scalp and intraday weakest-symbols tables this morning) while **HOME/USDT's contradiction remains unresolved for a second consecutive session (~13h and counting)**. The best catalyst-backed idea tonight is materially stronger than last review: real-world **SpaceX (SPCX) closed -13.61% on Aug 5** and **over $100B in SPCX stock unlocks land today, Aug 6** (externally verified, WebFetch-confirmed, ingested into `news_items`) — SPCXB/USDT (tokenized proxy) still has no defined bearish entry (squeeze-risk capped, no derivatives data), so this remains watch-only. Stocks' post-close data-fetch failure flagged in the last review has **resolved** (84/84 symbols, 10/10 indices, 12/12 sector ETFs succeeded this cycle) — no action needed, closing that thread. 0 untracked legacy alerts this cycle (clean run on that front).

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-06_01-36_scalp_report.md` (data freshness 01:30 UTC, generated 04:36 EEST — ~14min old at review start, freshest source this cycle), `data/reports/intraday/2026-08-05_22-49_intraday_report.md` (generated 01:49 EEST — ~2h50m old, fresh), `data/reports/swing/2026-08-05_20-08_swing_report.md` (generated 23:08 EEST — ~5h30m old, **carry-forward band 4-12h**, flagged §3).
- Stocks: `data/reports/stocks/intraday/2026-08-05_23-12_stocks_intraday_report.md` (generated 02:12 EEST — ~2h27m old; **market closed this session** — planning/watchlist context only; data-fetch fully recovered this cycle, 84/84 symbols).
- Stocks swing/invest: last generated 2026-07-02 — **stale >1 month, excluded** per standing policy (deprecated old framework; see `project_crypto_ai_desk_stocks_position_framework.md`).
- `data/catalysts/2026-08-06/catalyst_events.jsonl` (500 rows, freshly generated this run via `catalyst-scan` since today's folder didn't exist yet — 197 mapped / 303 unmapped = 60.6% unmapped), `narrative_baskets.jsonl` (3 baskets: `ai_narrative`/NEAR·RENDER·TAO·FET, `perps_dex_narrative`/HYPE, `momentum_breakout`/DODO·TUT·ZBT, playbook `avoid_chase`).
- `data/processed/llm_analysis_packet.md` (crypto, generated 04:36 EEST, fresh) — regime, movers, macro, catalysts.
- CLI: `active-signals --asset-class crypto` (50 rows, re-run twice as new fires landed mid-review), `active-signals --asset-class stocks` (50 rows, all C-tier / legacy expiry remnants except 4 fresh planning-only watchlist names), `signal-stats --asset-class crypto` (weekly: tier B n=109, PF 2.41, avgR 0.38, triggered winrate 26% flagged low by the tool's own observation; by mode: intraday PF 3.06 best, swing PF 2.34, scalp PF 0.00 n=24 confirmed weak), `signal-stats --asset-class stocks` (weekly: intraday n=201, tier C triggered winrate 2%, PF 0.79 — both below the CLI's own flag thresholds, unchanged known pattern), `detect_untracked_legacy_alerts --since 2026-08-06` (**0 untracked** — clean).
- DB (read-only queries): `proposed_signals` + `signal_outcomes` joined for BICO/USDT, SYN/USDT, ZEC/USDT, FIDA/USDT, TAO/USDT, GIGGLE/USDT, KITE/USDT, HOME/USDT, EPIC/USDT, STO/USDT (reconstructed overnight closed-trade timeline, §4/§7); `proposed_signals` filtered on `mode='scalp' AND created_at > now-4h` (confirmed 6 new scalp registrations, `telegram_supported=0` on all — evidence for the §14 kill-switch finding); `config/session_risk.yaml` read (confirms the documented hard kill-switch and its "never registered, never alerted" language).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_2335.md` (post-close final daily review, 23:35 EEST).
- **External web research invoked this cycle** (WebSearch x2, WebFetch x2 attempted / x1 succeeded): BTC/ETH overnight-level check (Yahoo Finance search snippet — used for directional framing, BTC ~$64,808 +0.82%); SpaceX (SPCX) stock news (WebSearch found the story, then WebFetch on `finance.yahoo.com/markets/stocks/articles/stock-market-today-aug-5-212003303.html` **succeeded** and confirmed SPCX closed $108.27 / -13.61% on Aug 5, driven by AI capex concerns, with **over $100B in stock unlocks scheduled for Aug 6 2026** — this is dated, verified, and directly relevant to today's session; two other candidate URLs — `cnbc.com` and `247wallst.com` — returned HTTP 403 and were not used as primary sources, only as corroborating search-snippet color).

## 3. Scheduler / Data Freshness

- Cron target 04:30 EEST; this run's data-gathering window ~04:39-04:50 EEST — within tolerance.
- `scheduler.log` in `data/scheduled_runs/2026-08-05_default_schedule/` (the actively-running folder, despite its date-stamped name — it started 2026-08-05 and is still the live cycle folder past midnight) — mtime ~04:37 EEST, ~2min old at review start — fresh, not deferred. Latest `cycle_02_01-34_summary.md` mtime 02:27 EEST — ~2h12m old — within the 3h defer threshold, no defer triggered. A separate `2026-08-06_default_schedule/` folder exists with only a 2482-byte `scheduler.log` (mtime 00:03) — appears to be an aborted/duplicate midnight rollover, not the live folder; not itself a review blocker but worth a human glance if it recurs (not escalated to a formal TODO this cycle — single observation, low signal).
- Crypto scalp ~14min old (freshest source this cycle), intraday ~2h50m old (fresh), swing ~5h30m old (**carry-forward band, 4-12h** — weakest-symbols/regime figures from the swing report should be read as context, not as the single freshest truth; cross-checked against the fresher scalp/intraday reports throughout this review where they diverge).
- Stocks: 23:12 EEST (02:12 EEST local... report timestamped 2026-08-05_23-12, generated ~02:12 EEST) report shows **84/84 symbol, 10/10 index, 12/12 sector-ETF fetches succeeded** — the 0/84 total-failure flagged in the last review (23:35 EEST) has **resolved** on its own; treating that TODO as closed this cycle, no further action needed. Data itself remains a pre-close-into-close snapshot since the market has been closed since; correctly self-flagged and correctly gated `market_closed_intraday_planning_only` throughout.
- Data-quality anomalies this cycle: (1) catalyst mapping weak, 60.6% unmapped (303/500) — persistent pattern across at least the last 3 reviews (64.2% → 62.2% → 60.6%), slow improvement but still above the 50% weak-mapping threshold, escalated to a formal low-priority TODO this cycle (§14, new formal entry for a previously-narrative-only observation); (2) **crypto scalp kill-switch registration bug** — 6 new B-tier scalp signals registered `waiting_for_entry` this cycle despite `config/session_risk.yaml`'s documented hard kill-switch stating scalp signals are "never registered, never alerted" in production — confirmed via direct DB query, new high-priority TODO (§14); (3) EPIC/USDT weakest-symbol-vs-active-long contradiction re-emerged after resolving at last review; (4) HOME/USDT contradiction persists, now spanning a second session (~13h); (5) duplicate/aborted `2026-08-06_default_schedule/` scheduler folder (informational only, not escalated).
- **TradingView / manual chart check unavailable** — no chart MCP loaded this cycle; all price-structure statements are from local OHLCV/ATR/EMA fields in the reports plus the two external WebSearch/WebFetch checks cited above.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-06 04:50 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["no fresher swing report than 5h30m-old 20:08 EEST snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log fresh (~2min old), latest cycle_*_summary.md ~2h12m old, both within tolerance", "crypto swing report ~5h30m old (carry-forward band 4-12h), scalp/intraday fresh (<3h)", "stocks post-close data-fetch failure from last review has resolved (84/84 this cycle)", "duplicate/aborted 2026-08-06_default_schedule scheduler folder observed, informational only"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"],
      "data_missing": ["no live Asia-session tick beyond internal reports + WebSearch morning-level check"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC ~$64,808 +0.82% overnight (externally verified), uptrend; ETH transition_up", "altcoin breadth above EMA20: 62.22% (scalp, freshest), 73.81% (intraday), 71.43% (swing, carry-forward) -- directionally healthy but off the prior evening's 71-74% peak", "macro/geopolitics risk 98.2/100, eased slightly from 99.9/100 at last review; Iran/Hormuz theme persists but external search shows early de-escalation-talk color", "stocks closed (Asia hours) -- last verified close was mixed (S&P -0.17%, Nasdaq -0.83%, Dow +0.49% ATH); no fresher stocks regime data exists this slot"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["60.6% unmapped today (303/500), continuing a persistent weak-mapping pattern across the last several reviews (64.2% -> 62.2% -> 60.6%)", "3 narrative baskets unchanged in composition: ai_narrative (NEAR/RENDER/TAO/FET), perps_dex_narrative (HYPE), momentum_breakout (DODO/TUT/ZBT, playbook avoid_chase)", "TUT/USDT is simultaneously a momentum_breakout basket primary (avoid_chase playbook) AND one of tonight's 6 fresh no-catalyst scalp/intraday re-fires -- a direct in-house chase-flag on a symbol the funnel keeps re-firing", "SPCXB/USDT weak_rs_short tag externally re-confirmed and materially strengthened tonight: real SpaceX (SPCX) closed -13.61% Aug 5 with >$100B in stock unlocks landing today (Aug 6) -- the desk's best catalyst-confirmed idea, stronger evidence than last review's version of the same thesis"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["no fresh per-symbol funding/OI beyond what the scalp/intraday reports embed"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HFT/USDT (already tp1_hit on 2 legs): funding 0.00307, OI 24h +37.88%, 'extreme long crowding' -- standing flag carried from prior reviews, unresolved by any loss yet but still a caution for any fresh HFT entry", "SPCXB/USDT: 'no_derivatives_thin_short', squeeze-risk capped to C in every report tonight -- no actionable short exists despite the strong external catalyst", "BICO/SYN/TUT overnight legs: mostly short-covering / normal-crowding reads, nothing extreme beyond HFT"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "entry_fresh", "clean_retest", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BICO/USDT swing: filled cleanly inside its defined zone (from last review's caution flag) and hit TP1 +1.0R at 00:00 EEST -- resolves the same-day-same-symbol caution positively", "SYN/USDT intraday: extended from tp1 (+1.0R) to tp2 (+2.0R) between the last review and now, clean continuation", "ZEC/USDT swing: stopped -1.0R at 03:00 EEST -- a new loss on the same broad no-catalyst-momentum family", "6 fresh scalp fires (SYN/MIRA/HEI/KITE/BICO/TUT) registered 04:42-04:43 EEST are, per the kill-switch finding in this review, signals that should never have been registered at all -- treat their entry zones as informational only, not tradeable", "TUT/USDT specifically carries an in-house avoid_chase basket tag while being re-fired for the second time in ~12h (already closed one tp3 win earlier, now scalp+intraday waiting again)"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "closed_flat", "entered_unresolved"],
      "data_missing": ["CLI does not label lifecycle state directly -- classification is manual, from active-signals status + signal_outcomes joins"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto CLOSED since last review: BICO/USDT swing WIN (+1.0R, tp1, 00:00 EEST), SYN/USDT intraday extended to WIN (+2.0R, tp2, 23:45 EEST), ZEC/USDT swing LOSS (-1.0R, stopped, 03:00 EEST)", "Crypto OPEN actionable (triggered/tp-hit, non-expired) approx. 38 of 50 active rows: FIDA/USDT swing (newly filled, no TP yet -- ENTERED UNRESOLVED), STO/USDT swing (78.1, unchanged, steadiest), ZAMA/BABY/BIO swing (all filled overnight), HOME/USDT x2 swing (contradiction), EPIC/USDT swing (contradiction re-emerged), HFT/KITE/SYN intraday (tp1/tp2/triggered)", "Crypto WAITING for entry: ~11 of 50 rows -- ERA/USDT intraday (carried) plus the 6 disputed fresh scalp fires and the matching intraday-side fires (BICO/HEI/MIRA/TUT intraday) from 04:42-04:43 EEST", "Stocks: 0 OPEN, 4 WAITING (WMT/NOC/CRWD/V, C-tier, market-closed planning-only, expire 23:18 UTC today), all other 46 rows are past-expiry legacy remnants; 0 new A/B fired"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["manual_review", "legal_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOME/USDT: weakest-symbol-vs-active-long contradiction now unresolved for a second consecutive session (~13h and counting since first flagged ~15:58 EEST yesterday)", "EPIC/USDT: same class of contradiction RE-EMERGED this cycle after resolving at the last review -- worth tracking whether this is a recurring, not one-off, data-consistency issue", "Crypto scalp kill-switch registration bug -- 6 signals registered against an explicit 'never registered' production guarantee; not yet Telegram-alerted (telegram_supported=0 confirmed) but a genuine control-gap", "MSFT (raw A all session): active legal-headline risk (class_action, securities_fraud) confirmed again in the last live stocks snapshot", "0 untracked legacy alerts this cycle -- a clean read on the previously-confirmed watchlist-alert/signal-reuse bug pattern (ALLO/BANK/HEI), tempering but not resolving that standing concern"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly (tier B, n=109, reliable): PF 2.41, avgR 0.38, triggered winrate 26% -- the CLI's own observation flags this triggered-winrate as low despite a healthy PF (asymmetric win/loss sizing)", "crypto by mode weekly: intraday PF 3.06 (best), swing PF 2.34, scalp PF 0.00 (n=24, confirmed weak) -- consistent with the documented 2026-07-07 kill-switch rationale (scalp -4.4R/-$110, 19% win over 14d) that the §14 registration bug is now undermining operationally", "stocks weekly (n=201 intraday, reliable): tier C triggered winrate 2%, PF 0.79 -- unchanged known pattern, C-tier never actionable per standing policy", "overnight cluster net: BICO +1.0R, SYN +1.0R (incremental tp1->tp2), ZEC -1.0R = net +1.0R since last review on this specific family, smaller sample than yesterday's full-day +4.0R but directionally consistent"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH overnight tape constructive (+0.82% BTC), altcoin breadth healthy, macro risk easing slightly off the ceiling (98.2 vs 99.9) -- selective risk-on, not unambiguous", "overnight cluster net +1.0R since last review (1W closed, 1 extended-win, 1 loss) -- small positive data point, same family the desk has watched for two days", "SPCXB/USDT's catalyst case materially strengthened tonight with a verified, dated, still-live catalyst (>$100B unlock landing TODAY) -- best catalyst-backed idea this review has seen, still watch-only pending a defined entry", "the new scalp kill-switch registration finding is a genuine control-gap worth flagging clearly, even though it has not (yet) reached Telegram", "HOME/USDT and now EPIC/USDT both carry unresolved technical-consistency contradictions -- avoid fresh exposure on both pending a human check", "stocks: market closed, nothing actionable; MSFT legal-risk gate still live"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "MIRA/USDT", "trigger": "intraday/scalp B-tier waiting_for_entry (68.1/70.3), fill only inside 0.042653-0.043170, invalidation 0.042020 -- no negative history on this symbol tonight, cleanest of the fresh fires (unlike TUT, not tagged in an avoid_chase basket)" },
    "best_short_candidate":    { "symbol": "BANK/USDT", "trigger": "still the persistent weakest symbol on recent reports; desk's own gate rejects it for fighting the bullish tape; needs a confirmed failed-bounce/breakdown structure before actionable" },
    "best_catalyst_candidate": { "symbol": "SPCXB/USDT", "trigger": "weak_rs_short watchlist tag, externally re-confirmed and strengthened tonight -- real SpaceX (SPCX) closed -13.61% Aug 5 with >$100B in stock unlocks landing TODAY (Aug 6, externally verified); needs a confirmed bearish HTF structure + derivatives data + clear stop above swing high before actionable -- still capped for squeeze risk" },
    "avoid_candidate":         { "symbol": "HOME/USDT", "reason": "weakest-symbol-vs-active-long contradiction unresolved for a second consecutive session (~13h); 2 active triggered long swing positions against a persistent bias-short technical read -- do not add fresh exposure either direction until reconciled" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.6 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | risk_on, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.5 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, entry_fresh, clean_retest, entry_late | advisory_only |
| execution_lifecycle | ok | 0.6 | open_actionable, waiting_for_entry, closed_flat, entered_unresolved | advisory_only |
| risk_manager | caution | 0.6 | manual_review, legal_risk, reduce_risk | advisory_only |
| playbook_performance | ok | 0.6 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.6 | risk_on, longs_preferred, wait_for_trigger, manual_review | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_2335.md` (23:35 EEST, post-close final daily review):

- **Closed since 23:35 (crypto):** BICO/USDT swing **CLOSED WIN** (tp1_hit, +1.0R, 00:00 EEST — was "wait-for-entry, extra scrutiny" at 23:35); SYN/USDT intraday **extended WIN** (tp1→tp2, +1.0R→+2.0R, 23:45 EEST — was already tp1_hit at 23:35, this is incremental); ZEC/USDT swing **CLOSED LOSS** (-1.0R, stopped 03:00 EEST — new since 23:35, was not mentioned in the prior review). Net for the family since 23:35: **+1.0R** (1 clean win, 1 extended win, 1 loss).
- **New:** FIDA/USDT swing (last review's cleanest "best long-watch") **filled** — status is now `triggered`, an open ENTERED-UNRESOLVED position with no TP yet. Six new B-tier scalp signals (SYN, MIRA, HEI, KITE, BICO, TUT) registered `waiting_for_entry` at 04:42-04:43 EEST — flagged as a data-integrity issue, not a trading opportunity (§14). Matching intraday-side fires also landed for HEI/BICO/MIRA/TUT (waiting) and HFT (triggered).
- **Removed:** none of the prior cycle's core carried positions dropped.
- **Resolved:** the stocks post-close 0/84 data-fetch failure flagged at 23:35 EEST has **fully resolved** — this cycle's stocks report shows 84/84 symbol, 10/10 index, 12/12 sector-ETF fetches succeeded. No further action needed; closing that thread.
- **Contradiction re-emerged:** EPIC/USDT — resolved as of the 23:35 EEST review (no longer on the weakest-symbols table that night), but back on **both** the freshest scalp (01:36 gen) and intraday (01:49 gen) weakest-symbols tables this morning, while still carrying its 1 active triggered swing long (69.5). This is now the second time this specific contradiction has appeared and resolved and reappeared — worth tracking as a possible recurring pattern, not a one-off (§14).
- **Contradiction unresolved:** HOME/USDT — still both a weakest-symbol read (bias short, -11.15% per the freshest scalp packet) and 2 active triggered longs, now spanning a second consecutive session (~13h since first flagged).
- **New anomaly:** crypto scalp kill-switch registration bug (§14, new) — not present as a finding in the 23:35 review.
- **Confirmed clean:** 0 untracked legacy alerts this cycle (was 2 untracked HEI/USDT alerts at 23:35) — tempers, does not resolve, the standing watchlist-alert/signal-reuse bug thread.
- **Invalidated:** none.
- Macro/geopolitics risk **eased** 99.9/100 → **98.2/100** (still elevated, first easing since the 18:48 review yesterday reversed).
- Catalyst mapping **improved slightly** 62.2% → **60.6%** unmapped (continuing the slow multi-cycle trend, now formally tracked as a TODO given the persistence, §14).
- SPCXB/USDT's catalyst case **materially strengthened**: at 23:35 EEST this was "real SpaceX -13% today, needs confirmed bearish structure." Tonight the same thesis is reinforced with a second, more specific, dated catalyst — the >$100B stock-unlock event landing today (Aug 6) — externally verified and ingested into `news_items`.

## 5. Catalyst Coverage

- Total catalyst events today (fresh scan, this run): **500** scanned; mapped (non-null symbol): **197**; unmapped: **303** (**60.6%**) — improved slightly from 62.2% at 23:35 EEST, continuing a slow multi-cycle downward trend (64.2% → 62.2% → 60.6%) that remains above the 50% weak-mapping threshold for at least the third consecutive review.
- Narrative baskets: **3** — `ai_narrative` (playbook `related_beta_rotation`, primary NEAR/RENDER/TAO/FET, fresh <6h), `perps_dex_narrative` (playbook `wait_pullback`, primary HYPE, fresh <6h), `momentum_breakout` (playbook `avoid_chase`, primary DODO/TUT/ZBT, fresh <1h) — TUT/USDT's presence here directly overlaps with tonight's fresh scalp+intraday re-fire on the same symbol, a live in-house chase-flag.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** 60.6% unmapped, still above the 50% threshold; now formally escalated to a TODO given the persistence across several consecutive reviews (§14, new).
- Top unmapped headlines (sample): "Inside India newsletter: What's behind India's rush to sell shares in state-owned firms," "U.S. is ready to return to 'commitments,' Iran says, after Trump signals deal is near," "MercadoLibre outlines continued reinvestment as credit portfolio reaches $16.4B" — the same macro/earnings-wire mix flagged in prior cycles.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **selective risk-on** — BTC ~$64,808 (+0.82% overnight, externally verified), uptrend; ETH transition_up; altcoin breadth 62-74% above EMA20 depending on report (freshest scalp reading is the lower end, 62.22%, off the prior evening's 71-74% peak — worth watching whether this is genuine cooling or just the scalp funnel's narrower 45-symbol sample). Macro/geopolitics risk eased slightly to 98.2/100 (from 99.9/100) but remains elevated — Iran/Hormuz headlines still the dominant driver. Recommended style unchanged: "selective longs; prefer pullbacks on relative strength." Crypto scalp mode is explicitly disabled at the config level (documented kill-switch) — any fresh scalp fires seen tonight (§14) should not be treated as tradeable regardless of score.
- Stocks mood: **closed (Asia hours) — last verified state carries forward** — S&P -0.17%, Nasdaq -0.83%, Dow +0.49% (ATH), VIX 15.81, a tech-to-value rotation on the day the index hit a fresh high. No fresher stocks data exists this slot; treat all stocks context below as planning/watchlist only.
- Dominant narrative: crypto's no-catalyst-momentum cluster (HFT/BICO/SYN/TUT/HEI/KITE family) continues to be the desk's most active playbook, net positive again overnight (+1.0R) but now complicated by a real registration-control-gap on the scalp leg of that same family; SPCXB/USDT's real-world catalyst (SpaceX AI-capex sell-off + today's >$100B unlock) is the single strongest catalyst-confirmed thesis this desk has surfaced in several reviews, still stuck watch-only on execution-readiness grounds.
- Preferred side now: **longs (crypto, selective)** — net positive overnight on the tracked cluster; **watch-only (SPCXB short)** — strongest catalyst case, no defined entry yet; **wait (stocks)** — market closed, nothing actionable until RTH.
- Best long candidate: **MIRA/USDT** (fresh waiting_for_entry, intraday+scalp, no negative history tonight, not tagged in an avoid_chase basket unlike TUT) — see §7/§8.
- Best short candidate: **BANK/USDT** (persistent weakest symbol) — desk's own gate still rejects it for fighting the bullish tape; watch-only pending a confirmed failed-bounce structure.
- Best catalyst-backed candidate: **SPCXB/USDT** (weak_rs_short, externally re-confirmed and strengthened by today's >$100B SPCX unlock) — see §7.
- What to avoid: **HOME/USDT** fresh exposure either direction (unresolved contradiction, now a second session); **EPIC/USDT** treated with added caution given its contradiction just re-emerged; the **6 fresh scalp fires** (SYN/MIRA/HEI/KITE/BICO/TUT) should not be treated as tradeable ideas — they are evidence of a control-gap, not a signal, pending the §14 fix; **crypto scalp mode** generally, which is supposed to be fully disabled.
- What would change the view: macro/geopolitics risk continuing to ease off the elevated band; a human reconciling the HOME/USDT and EPIC/USDT contradictions; the scalp kill-switch registration gap being fixed; a defined bearish entry structure appearing for SPCXB/USDT once derivatives data becomes available; resolution (fill or expiry) of ERA/USDT's and the intraday-side fresh fires' defined zones; RTH reopening for a fresh stocks read.

## 7. Candidate Deep Dives

### Overnight no-catalyst-momentum cluster — net +1.0R since last review (1 clean win, 1 extended win, 1 loss), plus a control-gap finding
- **BICO/USDT swing** — CLOSED WIN, +1.0R (tp1), 00:00 EEST. Filled cleanly inside its defined zone (0.0259-0.0266) per last review's own entry plan, then hit target within roughly 3 hours — resolves the "extra scrutiny, same-day intraday loss on this symbol" caution flagged at 23:35 EEST with a clean positive outcome.
- **SYN/USDT intraday** — extended from tp1 (+1.0R, already closed-in-progress at 23:35) to **tp2 (+2.0R)** at 23:45 EEST — continuation of a position already flagged as a win last review, now a bigger win.
- **ZEC/USDT swing** — CLOSED LOSS, -1.0R, stopped 03:00 EEST. New since last review; same broad family, no fresh verified catalyst per its own evidence block — a pure technical-execution loss, consistent with the mixed (not clean) track record this specific momentum family has shown across the last two days.
- **FIDA/USDT swing** — filled since last review, now `triggered` (ENTERED UNRESOLVED — no TP/SL hit yet). Was last review's cleanest "best long-watch" with no same-day negative history; that thesis is unchanged, it has simply moved from waiting to live.
- **Six new B-tier scalp fires (SYN, MIRA, HEI, KITE, BICO, TUT)** registered `waiting_for_entry` at 04:42-04:43 EEST, plus matching intraday-side fires for HEI/BICO/MIRA/TUT (waiting) and HFT (triggered). **This is a data-integrity finding, not a trading signal**: `config/session_risk.yaml` documents `disabled_modes.crypto: [scalp]` with an explicit comment that this "demotes the listed modes to 'rejected' in PRODUCTION (never registered, never alerted)" — yet these six scalp signals exist in `proposed_signals` with defined entry/invalidation zones. Verified `telegram_supported=0` on all six, so the "never alerted" half of the guarantee held (no Telegram push observed, no untracked-alert anomaly either), but the "never registered" half did not. New high-priority TODO (§14) — treat all six scalp entry zones as informational only, not actionable, pending a human fix.
- Has price already reacted to a catalyst? No for all — every fire in this family explicitly carries "no fresh verified catalyst detected" in its own evidence block; pure momentum/RS thesis, same as every prior review.
- Is the setup chasing? Mixed, same pattern as the last two days: BICO and SYN won clean fills; ZEC lost. TUT/USDT specifically carries the funnel's own `avoid_chase` narrative-basket tag (`momentum_breakout`) while being re-fired for a second time in ~12h (it already closed a tp3 +3.0R win earlier yesterday) — worth extra scrutiny if this particular re-fire ever becomes tradeable again.
- Long/short/wait: **closed items need no action; FIDA/USDT hold (unresolved, watch invalidation); the six scalp fires should be treated as not-actionable pending the kill-switch fix.**
- Chase-risk / catalyst confirmation: none of the family carries catalyst backing; pure technical-execution outcomes, mixed but net positive since last review.

### EPIC/USDT (crypto — weakest-symbol vs active-long contradiction, RE-EMERGED)
- Resolved as of the 23:35 EEST review (no longer on that night's freshest weakest-symbols table). Back on **both** the freshest scalp (01:36 gen, expanded-universe leaders: bias short, score 68.2 — wait, cross-check: freshest scalp packet's "Lower-Cap / Expanded Universe Leaders" lists EPIC/USDT bias short, score 80.2, 24h -13.01%) and the freshest intraday (01:49 gen) weakest-symbols tables (bias short, 24h -10.12%), while still carrying its 1 active triggered swing long (69.5, weekend-mode).
- This is the second time in roughly 12h this specific symbol's contradiction has appeared, resolved, and reappeared — a pattern worth flagging distinctly from HOME/USDT's single unbroken instance, since a resolve-then-recur cycle may point to a different root cause (e.g., a rolling-window recalculation flipping the bias near a threshold) than HOME/USDT's flat, unbroken conflict.
- Would a fresh entry now be late (for a hypothetical short)? Yes — no defined short setup exists for EPIC/USDT in any report tonight; this is a flag, not a tradeable idea.
- What level would make a short actionable? Only after the desk's own scanner generates a confirmed failed-bounce/breakdown structure — none exists.
- Mood alignment: the bias-short read cuts against tonight's broader crypto risk-on tape, reinforcing this is an idiosyncratic/technical flag.
- Long/short/wait: **wait** — do not add fresh exposure in either direction; the existing long's invalidation (0.859329) is unchanged and untouched.
- Chase-risk: N/A. Catalyst confirmation/contradiction: none found; pure internal-consistency flag (§14, carried/recurring).

### HOME/USDT (crypto — weakest-symbol vs active-long contradiction, unresolved, now a second session)
- Still appears on the freshest scalp packet's expanded-universe leaders (bias short, score 68.2, 24h -11.15%, RS/BTC -11.52%) while carrying 2 active triggered long B-tier swing positions (68.5 and 67.3, one weekend-mode). Unresolved since first flagged ~15:58 EEST yesterday — now roughly 13h and counting, spanning two trading sessions.
- This remains a genuine internal-consistency question the review cannot resolve with read-only tools — it does not by itself mean either long is wrong (no invalidation has been hit on either), but the duration is now long enough, combined with EPIC/USDT's recurring version of the same pattern, to suggest a shared root cause worth a focused human check.
- Would a fresh entry now be late (for a hypothetical short)? Yes — no defined short setup exists for HOME/USDT in any report tonight; this is a flag, not a tradeable idea.
- What level would make a short actionable? Only after the desk's own scanner generates a confirmed failed-bounce/breakdown structure — none exists.
- Mood alignment: the bias-short read cuts against tonight's broader crypto risk-on tape, reinforcing this is idiosyncratic/technical, not market-wide.
- Long/short/wait: **wait** — do not add fresh exposure in either direction; monitor whether the existing longs' invalidations hold.
- Chase-risk: N/A. Catalyst confirmation/contradiction: none found; pure internal-consistency flag (§14, carried, now escalated given the duration + the EPIC/USDT parallel).

### SPCXB/USDT (crypto, weak_rs_short watchlist tag — best catalyst-backed candidate tonight, direction short, materially strengthened)
- Has price already reacted to a catalyst? Yes, and more so than last review — real-world SpaceX (SPCX) stock **closed at $108.27, down 13.61%, a new all-time closing low, on Aug 5**, driven by investor concern over >$18B in quarterly capital spending (AI capex alone $15.8B, up from $7.7B in Q1) despite beating revenue estimates ($7.81B, +92% YoY). Critically, **over $100 billion in SPCX stock unlocks are scheduled to land today, Aug 6, 2026** — a fresh, dated, still-live catalyst that was not part of last review's version of this thesis. SPCXB/USDT (tokenized-equity proxy) showed -8% to -8.8% 24h across last night's reports, directionally consistent with the real-world move; freshest per-symbol read not yet updated for today's unlock event specifically.
- Is the setup chasing? The desk's own funnel still tags SPCXB/USDT `weak_rs_short` (`crypto_failed_bounce_short` playbook) but caps it to C for "short squeeze risk" and "no_derivatives_thin_short" (no futures data available for this symbol) — unchanged from last review.
- Retest/pullback structure? No defined short entry exists yet in any report; the watchlist tag explicitly requires "confirm bearish HTF structure + derivatives data + clear stop above swing high" before actionable.
- Would entry now be late? Not assessable — no defined entry exists. Given today's unlock event is a same-day catalyst, any confirmed bearish structure that emerges during the day should be treated as fresh, not late.
- What level makes it actionable cleanly? A confirmed bearish HTF structure with a clear stop above the recent swing high, once derivatives (funding/OI) data becomes available for this symbol.
- Mood alignment: cuts against tonight's broader crypto risk-on tape — an idiosyncratic, catalyst-driven weakness in a single tokenized-equity proxy, not a market-wide signal.
- Long/short/wait: **watch-only** — no defined entry exists yet; this remains the desk's cleanest catalyst-confirmed idea, now backed by a stronger and more specific catalyst than at any prior review.
- Chase-risk: N/A (no entry defined). Catalyst confirmation: **strong and strengthening** — verified via WebFetch (Yahoo Finance), ingested into `news_items` this cycle (§13).

### STO/USDT (crypto swing long, triggered, B-tier, 78.1 — steadiest carried position)
- Highest-scoring active B-tier signal on the book tonight; unchanged status since last review (triggered, no TP hit yet, expires 2026-08-11).
- Has price already reacted to a catalyst? No — no fresh verified catalyst; pure RS/momentum thesis, same as when first flagged.
- Long/short/wait: **hold** — no new information this cycle, no action needed.
- Chase-risk: N/A (already filled, holding). Catalyst confirmation/contradiction: none.

*(Excess candidates not given a full deep dive, per the 5-candidate cap: ERA/USDT intraday — carried waiting_for_entry, no change; ZAMA/BABY/BIO/USDT swing — filled overnight in the same no-catalyst-momentum family as BICO/FIDA above, no new information beyond what §4 already covers; COTI/PUMP/AEVO/USDT swing — carried triggered/tp-hit positions, unchanged; the 4 stocks C-tier watchlist names (WMT/NOC/CRWD/V) — market-closed planning-only, not actionable, no legal-risk flags observed on any of the four this cycle.)*

## 8. Best Candidates Ranked

1. **STO/USDT (crypto swing long, triggered, B-tier, 78.1)** — steadiest open position, unchanged; hold.
2. **FIDA/USDT (crypto swing long, triggered, B-tier, 68.5)** — filled since last review, no TP yet; hold, watch invalidation 0.018671.
3. **MIRA/USDT (crypto intraday+scalp long, waiting_for_entry, B-tier, 68.1/70.3)** — best fresh long-watch; fill only inside 0.042653-0.043170, invalidation 0.042020; caveat: the scalp leg specifically falls under the §14 kill-switch finding — treat the intraday leg as the tradeable one, not the scalp leg.
4. **SPCXB/USDT (crypto, weak_rs_short watchlist, score ~78)** — best catalyst-backed watch tonight, materially strengthened by today's >$100B SPCX unlock; no defined entry yet, watch for a confirmed bearish structure.
5. **BICO/USDT / SYN/USDT (crypto, closed overnight)** — BICO swing CLOSED WIN +1.0R, SYN intraday extended to +2.0R; both resolved cleanly, no action needed, included here as the cluster's clean-outcome half against ZEC's loss.

**HOME/USDT** (unresolved contradiction, avoid fresh exposure, now a second session) and **EPIC/USDT** (contradiction re-emerged, treat with added caution) are tonight's explicit watch/avoid names — see §6/§9. No stocks name is actionable (market closed). The 6 fresh scalp fires (SYN/MIRA/HEI/KITE/BICO/TUT scalp legs) are explicitly **excluded** from this ranking — they are a control-gap finding, not candidates (§14).

## 9. Avoid / No Trade

*(This applies to this decision window / overnight-into-Asia only — scanning, tracking, and the scheduler continue unchanged.)*

- **HOME/USDT any fresh direction** — unresolved weakest-symbol-vs-active-long contradiction, now a second consecutive session; needs manual review before new exposure either way.
- **EPIC/USDT** — same class of contradiction re-emerged this cycle after resolving last night; treat with added caution pending a human check on whether this is a recurring or one-off pattern.
- **All 6 fresh crypto scalp fires (SYN/MIRA/HEI/KITE/BICO/TUT, scalp mode)** — registered against an explicit "never registered" production kill-switch guarantee; not Telegram-alerted, but should not be treated as tradeable ideas by any human reviewing the raw signal book either, pending the §14 fix.
- **All stocks C-tier watchlist names** (WMT, NOC, CRWD, V, MSFT, MSTR, JPM, NVDA, DIA, PLTR, XLV, QQQ, IWM) — market closed, planning-only; MSFT additionally carries a standing legal-risk gate (class_action, securities_fraud).
- **Crypto scalp mode generally** — weekly PF 0.00 (n=24), consistent with the documented rationale for disabling it entirely; the mode should not be trading at all right now (§14).
- **BANK/USDT** — persistent weakest symbol, but the desk's own gate rejects it for fighting the bullish tape; no defined short entry.
- **SPCXB/USDT as a live trade** — catalyst confirmation is real and strengthening, but no defined bearish entry structure or derivatives data exists yet; watch-only.

## 10. Main Risks

- **Crypto scalp kill-switch registration bug (new, high)** — a documented "never registered" production guarantee is being violated; while the softer "never alerted" half held this cycle (telegram_supported=0 confirmed on all 6), a control that only partially holds is a genuine risk that this could reach Telegram in a future cycle if the same gap extends further downstream. Needs a human fix before the next scalp-mode cycle.
- **HOME/USDT's contradiction has now spanned a second consecutive session (~13h)**, and **EPIC/USDT's version of the same pattern has now resolved-and-recurred once** — together these suggest a possible shared, recurring root cause in how the momentum-ranking table and the swing-signal book read OHLCV windows, rather than two unrelated one-off events (§14, carried + new instance).
- Macro/geopolitics risk remains elevated (98.2/100) despite easing slightly from the 99.9/100 ceiling — Iran/Hormuz headlines are the proximate driver; treat any easing as tentative.
- Catalyst mapping remains weak (60.6% unmapped), now a formally tracked TODO given the multi-cycle persistence — treat all catalyst-basket framing as directional color only.
- The overnight no-catalyst-momentum cluster's mixed outcome (2 wins, 1 loss since last review; a broader multi-day mixed record) means the standing chase-flag-recurrence hypothesis remains open — continue tracking, do not declare resolved in either direction.
- Stocks remain closed; nothing in the internal system has been live-tested since the verified mixed close yesterday — treat all stocks context as planning only until RTH.

## 11. Action Plan — next 4 hours

- Hold STO/USDT and FIDA/USDT swing positions into their invalidations/targets; no new sizing.
- Let ERA/USDT (intraday) and the legitimate intraday-side fresh fires (HEI/BICO/MIRA/TUT intraday, HFT intraday already triggered) either fill cleanly inside their defined zones or expire — do not force any of them.
- **Do not treat any of the 6 fresh scalp fires (SYN/MIRA/HEI/KITE/BICO/TUT) as tradeable** — flag for a human to investigate and fix the kill-switch registration gap before the next scalp-mode cycle runs (§14).
- Do not open any fresh HOME/USDT or EPIC/USDT position (long or short) until their respective weakest-symbol/active-long contradictions are manually reconciled; treat EPIC/USDT's resolve-then-recur pattern as a separate data point from HOME/USDT's continuous one when investigating root cause.
- Watch SPCXB/USDT for a confirmed bearish structure — today's live >$100B unlock event makes this the highest-priority catalyst watch on the book; watch BANK/USDT for a confirmed breakdown.
- Continue scanning/tracking/monitors unchanged through the Asia session into the European morning — this review recommends caution on specific entries and one control-gap fix only, never a pause of any kind.

## 12. Final Verdict per Mode

- **Crypto scalp:** should be fully disabled per the documented 2026-07-07 kill-switch (14d audit: -4.4R/-$110, 19% win, confirmed again this week's PF 0.00 n=24) — but 6 new B-tier signals registered this cycle despite that guarantee (§14, new). Treat scalp as **not tradeable** regardless of any score shown, and treat the registration itself as a bug to fix, not a feature to use.
- **Crypto intraday:** healthiest mode by weekly PF (3.06); overnight net +2.0R on SYN's tp1→tp2 extension; HFT/USDT still carries a standing "extreme long crowding" flag worth watching on any fresh entry.
- **Crypto swing:** the desk's steadiest bucket — BICO/USDT closed clean +1.0R overnight, FIDA/USDT filled and holding, ZEC/USDT stopped -1.0R (new loss); STO/USDT remains the steadiest unchanged carry; HOME/USDT and EPIC/USDT both flagged for unresolved/recurring technical contradictions.
- **Stocks intraday:** market closed all session (Asia hours); post-close data-fetch failure from last review has resolved (84/84); zero actionable A/B, nothing new to report until RTH.
- **Stocks swing/invest:** not evaluated — reports stale/deprecated since 2026-07-02, excluded per standing policy.

## 13. Sources

- Internal: `data/reports/scalp/2026-08-06_01-36_scalp_report.md`, `data/reports/intraday/2026-08-05_22-49_intraday_report.md`, `data/reports/swing/2026-08-05_20-08_swing_report.md`, `data/reports/stocks/intraday/2026-08-05_23-12_stocks_intraday_report.md`, `data/catalysts/2026-08-06/catalyst_events.jsonl`, `data/catalysts/2026-08-06/narrative_baskets.jsonl`, `config/session_risk.yaml`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `signal_outcomes` read-only joins), `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_2335.md`.
- External (WebSearch x2, WebFetch x2 attempted / x1 succeeded):
  - [Stock Market Today, Aug. 5: SpaceX Beats Revenue but Faces Capital Spending Pressure — Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/stock-market-today-aug-5-212003303.html) — WebFetch-verified: SpaceX (SPCX) closed $108.27, -13.61% on Aug 5 2026 (new all-time closing low), driven by concern over >$18B quarterly capex (AI capex $15.8B) despite beating revenue ($7.81B, +92% YoY); **>$100B in SPCX stock unlocks scheduled for Aug 6, 2026**. Ingested into `news_items` (asset_class=stocks) via `data/raw/enriched_review_sources/2026-08-06T0440_stocks.json`, 2 rows written.
  - [Bitcoin and ethereum prices today, Wednesday, August 5, 2026 — Yahoo Finance / search snippet](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-august-5-2026-crypto-prices-rise-as-investors-watch-hormuz-negotiations-and-jobs-report-closely-124640660.html) — used for directional framing only (BTC ~$64,808 +0.82%, ETH ~$1,878); not a live Asia-session tick.
  - `cnbc.com/2026/08/05/spacex-spcx-stock-today-earnings.html` and `247wallst.com/investing/2026/08/05/spacex-falls-10-on-soaring-ai-costs-as-other-space-stocks-hold-steady/` — both returned HTTP 403 on WebFetch; used only as corroborating search-snippet color, not as primary sources.
- No chart/TradingView source this cycle (unavailable, §3).

## 14. Fix Requests / TODO

### TODO-crypto-scalp-killswitch-registration-bug (priority: high, new)
- **issue:** `config/session_risk.yaml` documents a hard, permanent kill-switch (`disabled_modes.crypto: [scalp]`, in force since 2026-07-07) with the explicit comment: "Demotes the listed modes to 'rejected' in PRODUCTION (**never registered, never alerted**)." This cycle's fresh scalp report (`2026-08-06_01-36_scalp_report.md`) correctly rejects every single scalp idea with the reason `crypto_scalp_disabled (kill-switch: mode off, any hour/day)`. Yet a direct query of `proposed_signals` shows **6 B-tier scalp signals registered `waiting_for_entry` at 2026-08-06T01:42:47-01:42:48 UTC** (SYN, MIRA, HEI, KITE, BICO, TUT — signal_ids `sig_9281aa7c...`, `sig_3afc4588...`, `sig_c52c43ca...`, `sig_5e49f0d3...`, `sig_cffe3b83...`, `sig_73c24116...`), just minutes after the report's own generation timestamp rejected the same symbols for the same reason. The "never alerted" half of the guarantee held (`telegram_supported=0` confirmed on all 6, and `detect_untracked_legacy_alerts` shows 0 untracked alerts this cycle), but the "never registered" half clearly did not.
- **evidence:** `config/session_risk.yaml` lines 19-30 (`disabled_modes.enabled: true`, `crypto: [scalp]`); `data/reports/scalp/2026-08-06_01-36_scalp_report.md` §7b "Rejected / Not Ready" (SYN/MIRA/HEI/KITE/BICO/TUT/FIDA/HFT/VIC all rejected for `crypto_scalp_disabled (kill-switch: mode off, any hour/day)`); `db/crypto_ai_desk.sqlite` `proposed_signals` query filtered on `mode='scalp' AND created_at > now-4h` returning the 6 rows above with `telegram_supported=0`.
- **suggested manual fix:** a human-driven session should trace the signal-writer/registration pass to find why it does not honor the same `disabled_modes` gate the report-generation/scoring pass already respects — likely a snapshot-timing or a separate code path that reads the config differently (or not at all) at registration time. This is a distinct, more concrete instance of the general "funnel-scan and signal-writer may read different states" hypothesis already tracked under the chase-flag-recurrence TODO below, but specifically severe because it contradicts an explicit, documented production guarantee rather than a soft scoring preference.
- **priority:** high
- **first observed:** 2026-08-06 04:50 EEST (this cycle).

### TODO-home-usdt-contradiction-second-session-unresolved (priority: high, carried forward)
- **issue:** HOME/USDT has now shown the weakest-symbol-vs-active-long conflict for a second consecutive trading session (first flagged ~15:58 EEST 2026-08-05, still present ~04:40 EEST 2026-08-06 — roughly 13h and counting): bias-short on the weakest-symbols table (freshest scalp packet: score 68.2, -11.15% 24h) while carrying 2 active triggered long B-tier swing positions.
- **evidence:** `data/processed/llm_analysis_packet.md` "Lower-Cap / Expanded Universe Leaders" (HOME/USDT bias short, score 68.2, -11.15%); `db/crypto_ai_desk.sqlite` `proposed_signals` HOME/USDT swing rows (status=triggered, 2 active, scores 68.5 and 67.3); prior instances in every `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_*.md` review's §14.
- **suggested manual fix:** unchanged from prior cycles — check whether the "weakest symbols" momentum-score calculation and the long-signal scoring pipeline read the same OHLCV window/timeframe for HOME/USDT specifically. Now worth cross-referencing against EPIC/USDT's resolve-then-recur pattern (below) for a possible shared root cause.
- **priority:** high
- **first observed:** 2026-08-05 15:58 EEST; carried through every subsequent review; still open 2026-08-06 04:50 EEST (this cycle, now spanning a second session).

### TODO-epic-usdt-contradiction-reemerged (priority: medium, recurring instance)
- **issue:** EPIC/USDT showed the same weakest-symbol-vs-active-long contradiction pattern as HOME/USDT, first flagged in earlier reviews, then **resolved** as of the 23:35 EEST 2026-08-05 review (no longer on that night's weakest-symbols table). It has now **reappeared** on both the freshest scalp (01:36 EEST gen) and intraday (01:49 EEST gen) weakest-symbols tables, while still carrying its 1 active triggered swing long (69.5).
- **evidence:** `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_2335.md` §4 ("EPIC/USDT no longer appears on the freshest weakest-symbols table"); `data/reports/intraday/2026-08-05_22-49_intraday_report.md` "Weakest Symbols" (EPIC/USDT, -10.12%); `data/processed/llm_analysis_packet.md` "Top Movers" (EPIC/USDT bias short, score 80.2, -13.01%); `db/crypto_ai_desk.sqlite` `proposed_signals` EPIC/USDT swing row (status=triggered, score 69.5).
- **suggested manual fix:** a human-driven session should determine whether this resolve-then-recur pattern is driven by a rolling-window threshold effect (e.g., a 24h-return calculation crossing a bias-flip boundary) rather than a persistent data-consistency bug like HOME/USDT's — the two symbols may have different root causes despite looking similar on the surface.
- **priority:** medium
- **first observed (recurrence):** 2026-08-06 04:50 EEST (this cycle); underlying pattern first observed on this symbol in earlier 2026-08-05 reviews.

### TODO-catalyst-mapping-persistently-weak (priority: low, new formal entry for a recurring observation)
- **issue:** Catalyst-event symbol mapping has been below the 50% weak-mapping threshold for at least 3 consecutive reviews tracked so far: 64.2% unmapped (18:48 EEST 2026-08-05) → 62.2% (23:35 EEST 2026-08-05) → 60.6% (04:50 EEST 2026-08-06). The trend is slowly improving but has never crossed back above 50% mapped in this window.
- **evidence:** `data/catalysts/2026-08-06/catalyst_events.jsonl` this cycle (500 scanned, 197 mapped, 303 unmapped = 60.6%); prior reviews' §5 sections showing the multi-cycle trend.
- **suggested manual fix:** a human-driven session should review the symbol-resolver logic in the catalyst-mapping layer — likely candidates are macro/earnings-wire headlines (India state-owned-firm sales, MercadoLibre credit-portfolio updates, etc.) that have no natural crypto/stock ticker to map to and may need either better filtering (exclude from the mapped/unmapped denominator entirely) or a broader symbol-detection pass.
- **priority:** low
- **first observed (formal TODO):** 2026-08-06 04:50 EEST (this cycle); pattern present in narrative form across the last 3+ reviews.

### TODO-chase-flag-recurrence-ongoing (priority: medium, carried forward)
- **issue:** The standing chase-flag-recurrence hypothesis (funnel-scan and signal-writer may read different price snapshots, producing "reject for chasing, then fire live minutes later" fires) continues to accumulate mixed evidence. Overnight: BICO/USDT swing and SYN/USDT intraday both closed clean wins from the same family; ZEC/USDT swing closed a loss. This cycle also surfaced a more severe, distinct instance of the same underlying class of problem — the scalp kill-switch registration bug above — which may share root cause with this broader hypothesis.
- **evidence:** `db/crypto_ai_desk.sqlite` `signal_outcomes` for BICO/USDT swing (+1.0R, tp1, 00:00 EEST), SYN/USDT intraday (+1.0R→+2.0R, tp1→tp2), ZEC/USDT swing (-1.0R, stopped, 03:00 EEST) — all resolved since the last review.
- **suggested manual fix:** unchanged in substance — measure elapsed time between funnel-scan data-freshness and signal-writer `created_at` across the last 1-2 weeks and compare realized-R outcomes for short-gap vs long-gap cases; now also worth checking whether the same timing gap explains the scalp kill-switch bypass specifically.
- **priority:** medium
- **first observed:** 2026-08-04 (swing instance); escalated 2026-08-05; carried 2026-08-06 04:50 EEST (this cycle) with a new, more concrete related finding (scalp kill-switch bug, tracked separately above).
