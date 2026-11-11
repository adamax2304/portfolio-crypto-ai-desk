# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:30 EEST

## 1. Executive Summary
- **Slot: crypto overnight / Asia review** (04:30 EEST target; data as of ~04:45 EEST / 01:45 UTC). **Advisory only / no auto-trade.**
- **Geopolitical escalation is materially worse than the 23:34 EEST post-close review reported.** Since that review: the IRGC claims direct ballistic-missile strikes on **two US Navy destroyers** (USS Delbert D. Black, USS John Paul Jones) "causing significant damage" (Iranian state media, unconfirmed by US side in internal feed); Iran fired **20 ballistic missiles at a US base in Jordan** (Muwaffaq Salti/Al-Azraq), Jordan intercepted 18, 2 landed in unpopulated areas, no casualties; US Central Command says it destroyed **five Iranian crude oil carriers**; Iran claims it **captured a US submarine drone in the Strait of Hormuz**. A later Telegram post (01:14 UTC) flagged a *separate* renewed-attack-on-Jordan rumor as false — treat any single-source Jordan-attack headline after that point with extra caution.
- **Market reaction:** Brent crude ~$99.37/bbl (+1.5%), WTI ~$94.47 (approaching the "$100 oil" headline threshold multiple outlets are now running); gold actually **fell** ~1% to $4,357.88 (rate-path concerns outweighing safe-haven bid); 10y yields holding ~4.79%; yen firmer. Notably, **Asia-Pac equities opened mostly higher, "shrugging off" the weak Wall St lead**, with South Korean chip names specifically cited as strong — a genuine mixed/non-uniform risk reaction, not a clean risk-off cascade.
- **Crypto itself: still thin and directionally quiet.** BTC last read $79,280 (-0.67%), ETH $2,484 (-0.41%) as of the 01:57 EEST swing report (fresh, ~2h48m old) — no fresher price confirmation found in news_items. Two new B-tier swing longs appeared since the last review (PROM/USDT 01:29 UTC, FORM/USDT 01:03 UTC, both `waiting_for_entry`, both pure-momentum/no-catalyst). No A-tier crypto or stocks signals are currently live. The **Asia dead-zone guard (00:00-06:00 UTC) is active right now** — config demotes crypto scalp/intraday actionability at this hour, consistent with the C-tier-only trade-idea sections in tonight's reports.
- Catalyst mapping is weak again (58.4% unmapped today, 208/500 mapped) — context only. Scheduler is fresh (cycle 2/12 running, last cycle finished ok=94/failed=12 — notably better than last night's 29-fail cascade); all six background monitors report healthy. One confirmed fix from last night's TODO: **crypto scalp is deliberately disabled** ("negative forward edge; research data retained" — explicit log line), not a silent regression as previously suspected — see §14.

## 2. Data Used
- `data/reports/swing/2026-09-08_22-58_swing_report.md` (generated 2026-09-09 01:57:50 EEST) — **fresh** (~2h48m old at read time): BTC transition_down, ETH uptrend, altcoin breadth 75.0%/87.5%, macro risk 100/100 risk-off headwind, no A/B trade ideas (C-tier watchlist only: PROM, SAHARA).
- `data/reports/intraday/2026-09-08_20-48_intraday_report.md` (generated 2026-09-08 23:47:37 EEST) — **carry-forward** (~5h old): BTC transition_down, ETH range, macro risk 99.9/100, no A/B trade ideas (C-tier watchlist only: DOGS, INJ, PENGU, FORM, XPL).
- `data/catalysts/2026-09-09/catalyst_events.jsonl`, `narrative_baskets.jsonl` — regenerated this run via the allowed `catalyst-scan --no-print` CLI (today's folder was missing): 500 events, 208 mapped/292 unmapped (58.4% unmapped), 2 baskets (`perps_dex_narrative` — HYPE primary; `momentum_breakout` — UNI/DOT catalyst-backed, AUCTION/DOGS no-catalyst).
- `proposed_signals` / `news_items` (SQLite `db/crypto_ai_desk.sqlite`) — direct queries for: crypto/stocks A/B 24h lifecycle counts, signals created in the last 3h, DOT/UNI/HYPE signal history, the full Iran/Jordan/Navy-destroyer/oil news timeline from 20:20 UTC (last review's cutoff) through 01:29 UTC.
- CLI: `active-signals --asset-class crypto` (50 rows, all B-tier swing long), `active-signals --asset-class stocks` (50 rows, only BAC C-tier `waiting_for_entry` and REGN B-tier swing `waiting_for_entry` are still live/unresolved; rest are resolved from prior sessions), `signal-stats --asset-class crypto` (completed this run, ~4-5min — see §14 for the still-open slow-step history), `detect_untracked_legacy_alerts --since 2026-09-09` (clean — no untracked alerts).
- `data/scheduled_runs/2026-09-08_default_schedule/scheduler.log` — live production log, tail read at ~04:45 EEST: cycle 1 ended `ok=94 failed=12` at 02:29:45 EEST; cycle 2/12 started 04:29:46 EEST and is currently running (intraday report generating); all six monitors (crypto, pending, mexc-canary, crypto-invest-forward, derivatives, fast-news) report healthy/reused.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_2330.md` (23:15 EEST, post-close slot) — used for §4 comparison.
- **External web research: not invoked this cycle.** The Iran/Jordan/Navy-destroyer story is exceptionally well-covered internally (CNBC Markets, Reuters via Finnhub, WSJ/CNBC via t.me/marketfeed and t.me/FinancialJuice, Jordanian Army statement via t.me/Middle_East_Spectator and t.me/ClashReport, IRGC statements via the same) — multiple independent, dated, mutually-consistent sources. Internal-first discipline satisfied; no candidate this cycle depends on external verification beyond what is already internally sourced.

## 3. Scheduler / Data Freshness
- **Not deferred**: `scheduler.log` mtime 04:31 EEST (<15min old at read time), well inside the 3-hour defer threshold.
- **Cycle 1 completed**: `ok=94 failed=12` at 02:29:45 EEST — a real improvement over the prior cycle's 29/105 fail count, though `refresh obsidian dashboard` timed out again (recurring, see §14) immediately before cycle-end.
- **Cycle 2/12 in progress**: started 04:29:46 EEST (weekday, crypto+stocks, long_horizon window 1); catalyst-label-refresh, stablecoin/cross-exchange risk context, options context (IV/RV+GEX), token-unlock context, and track-signals(pre) all completed 04:29-04:31 EEST; crypto intraday report generation was the in-flight step at read time.
- **Crypto scalp — confirmed deliberately disabled**, not a silent regression: `2026-09-09 04:31:44,233 [INFO] NOTE: crypto scalp report — disabled: negative forward edge; research data retained.` This resolves the recurring TODO-crypto-scalp-mode-inactive from the last three reviews — see §14 (closed, not reopened).
- Crypto swing report: **fresh** (~2h48m old, generated 01:57:50 EEST).
- Crypto intraday report: carry-forward (~5h old at read time; a fresher one was mid-generation in cycle 2 but not yet written when this review was compiled).
- Stocks intraday report (file): not re-checked this cycle — RTH is closed until the pre-US-open slot; live-DB lifecycle reads (`active-signals --asset-class stocks`) used instead, current as of read time.
- Stocks swing/invest: deprecated (shadow-only position framework in effect) — not evaluated, per standing project history.
- Catalyst data: regenerated fresh this run via the allowed CLI (today's folder had been missing) — 500 events / 2 baskets, 58.4% unmapped.
- All six background monitors (crypto, pending, mexc-canary, crypto-invest-forward, derivatives, fast-news) plus telegram-dashboard report **healthy/reused** — no restart or degraded-monitor signal.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-09-09 04:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"],
      "data_missing": ["catalyst folder for today was missing and had to be regenerated via the allowed CLI mid-review", "no crypto intraday report newer than 23:47 EEST yet (regen in-flight in cycle 2 at read time)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log <15min old, not deferred", "cycle 1 ok=94/failed=12 (improved vs prior night's 29 fails)", "cycle 2/12 running, all 6 monitors healthy/reused", "crypto scalp confirmed deliberately disabled via explicit log line — resolves a 3-review-old open TODO"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["mixed", "risk_off", "chop"],
      "data_missing": ["no BTC/ETH price print fresher than the 01:57 EEST swing report"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Iran claims ballistic-missile strikes on 2 US Navy destroyers + captured a US submarine drone in the Strait of Hormuz; 20 missiles fired at a US base in Jordan (18 intercepted, no casualties)", "US Centcom destroyed 5 Iranian crude carriers; Brent ~$99.37 (+1.5%), WTI ~$94.47", "gold fell ~1% despite the escalation (rate-path narrative dominating safe-haven bid)", "Asia-Pac equities opened mostly higher, chip names strong — NOT a uniform risk-off cascade", "BTC $79,280 (-0.67%), ETH $2,484 (-0.41%), transition_down/uptrend split, macro risk 100/100 risk-off headwind (swing report)", "Asia dead-zone guard (00:00-06:00 UTC) active right now — config-level demotion of crypto scalp/intraday actionability"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "narrative_supported", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["58.4% of today's 500 catalyst_events unmapped (208 mapped) — regenerated fresh this run", "2 active baskets: perps_dex_narrative (HYPE primary, no live A/B signal riding it), momentum_breakout (UNI/DOT explicitly catalyst-backed per the basket's own summary, not a chase; AUCTION/DOGS unconfirmed)", "both UNI/USDT and DOT/USDT already have live B-tier swing signals in `triggered` (entered-unresolved) status, aging 3 days and 2 days respectively"] },
    { "agent": "derivatives_squeeze", "verdict": "manual_review", "confidence": 0.35,
      "reason_codes": ["data_unavailable"],
      "data_missing": ["no fresh funding/OI/crowding re-check performed this cycle beyond what the 01:57 EEST swing report carries"],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing report derivatives table (01:57 EEST): PROM/USDT price up + OI up (fresh positioning, crowding normal); no fresher cross-exchange funding re-check run this cycle"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_fresh", "chase_risk", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM/USDT B-tier swing created 01:29 UTC (~16min old at read time), waiting_for_entry, zone 5.7849-5.8514, current price 5.943 (per swing report desk notes) — ~0.5-0.9 ATR above the zone, a genuine pullback watch not a chase", "FORM/USDT B-tier swing created 01:03 UTC (~42min old), waiting_for_entry, zone 0.29611-0.30386", "BNB/USDT B-tier swing waiting_for_entry since 2026-09-06T02:54 UTC — now ~3 days aging, unchanged zone, bordering on stale-before-entry (carried-forward finding, unchanged from the 23:34 review)"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.65,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "no_entry", "needs_review"],
      "data_missing": ["the 7 stocks 'expired' rows from the prior 24h window still lack a queryable fill-event field to split entered-unresolved vs no-entry — same open TODO as last night, unresolved"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B last 24h (n=13): 6 triggered/entered-unresolved, 2 waiting_for_entry, 4 no-entry/stale/moved-away, 1 closed loss (stopped)", "stocks A/B last 24h (n=52, market closed): 14 closed-win (touch-based tp-hit), 7 needs-review (expired, ambiguous), 30 no-entry, 1 waiting_for_entry (REGN)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.85,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["direct, claimed kinetic exchange between Iran and the US (destroyer strikes, Jordan missile barrage, captured submarine drone, destroyed oil carriers) is a live, still-developing story with real Strait-of-Hormuz tail risk", "a false-alarm correction already circulated once (01:14 UTC 'renewed attack on Jordan is false') — single-source headlines from this point need extra scrutiny before being treated as new escalation", "Asia dead-zone guard is independently already suppressing crypto scalp/intraday actionability at this hour regardless of the geopolitical overlay"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["low_sample", "playbook_working"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier lifetime (signal-stats, n=233, reliable): PF 2.52, avgR 0.33, totalR +50.3, but triggered winrate only 19% — system's own low-confidence observation, unchanged finding", "weekend-mode signals specifically underperform (winrate 10%, n=105) per the same stats run — not directly relevant tonight (weekday) but worth carrying forward", "swing mode PF 3.97 vs intraday PF 2.13 — swing remains the stronger sub-cohort, consistent with tonight's swing-only C-tier/B-tier candidate set"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "PROM/USDT", "trigger": "confirmed fill in the 5.7849-5.8514 pullback zone with volume holding above the 20-period average; invalidate below 5.7037", "reason": "freshest B-tier swing long (~16min old), RS-leader (score 88.0 in the swing report's Strongest Symbols), price currently ~0.5-0.9 ATR above the zone so a real pullback watch rather than a chase — but no catalyst backing, pure momentum" },
    "best_short_candidate":    { "symbol": "none", "trigger": "no crypto short setups exist in tonight's reports (100% long bias across all 50 active B-tier signals); would need a confirmed BTC breakdown through the transition_down structure, or the oil-driven equity risk-off tape to visibly bleed into BTC/ETH majors, before a clean short thesis exists", "reason": "the desk's own long/short=3-sample stock shows shorts performing poorly lifetime (PF 0.25, avgR -0.50) — low-confidence side regardless" },
    "best_catalyst_candidate": { "symbol": "DOT/USDT", "trigger": "already entered/triggered (2026-09-07T05:03 UTC, ~2 days aging) — re-confirm the momentum_breakout basket is still active and DOT has not broken its invalidation before treating the open position as still thesis-valid", "reason": "explicitly flagged catalyst-backed (not a no-catalyst chase) by the momentum_breakout basket's own catalyst_summary; UNI/USDT rides the same basket but is more aged (~3 days) and could be named as a secondary" },
    "avoid_candidate":         { "symbol": "BNB/USDT", "reason": "waiting_for_entry since 2026-09-06T02:54 UTC (~3 days), unchanged zone, catalyst (binance_ecosystem_teaser) itself unrefreshed for multiple review cycles now — bordering on stale-before-entry, carried forward unchanged from the 23:34 review's own caution" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.75 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | caution | 0.80 | mixed, risk_off, chop | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, narrative_supported, catalyst_confirmed | advisory_only |
| derivatives_squeeze | manual_review | 0.35 | data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_fresh, chase_risk, stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.65 | waiting_for_entry, entered_unresolved, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.85 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | low_sample, playbook_working | advisory_only |
| head_trader | caution (overall) | 0.55 | synthesis — see JSON | advisory_only |

## 4. What Changed vs Previous Review
Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_2330.md` (23:15/23:34 EEST, post-close slot):
- **Escalation confirmed to a materially higher severity level.** The 23:34 review's framing ("Iranian retaliation attempt against US Navy ships, no hits, per WSJ") is now superseded: IRGC state media claims direct ballistic-missile strikes on **two named US Navy destroyers** with "significant damage" (unconfirmed independently in the internal feed), plus a **20-missile barrage on a US base in Jordan** (18 intercepted by Jordanian air defense, 2 landed in open areas, no casualties), plus a claimed **captured US submarine drone in the Strait of Hormuz**. US Centcom's countermeasure — destroying five Iranian crude carriers — is also new since 23:34.
- **A false-alarm correction has already appeared** (01:14 UTC: "reports of a renewed attack targeting Jordan are false") — the story is not only escalating linearly; single-source claims after this point need extra scrutiny.
- **Market reaction diverged from a clean risk-off script:** oil continued higher (Brent nearing $100, up from $97.92 at the 23:34 review) and gold **fell** rather than rallying, while Asia-Pac equities opened **higher**, not lower — this is a more mixed/idiosyncratic reaction than the textbook "oil up, stocks down" print the 23:34 review closed on.
- **Crypto pipeline produced two new B-tier swing longs** since 23:34 (PROM/USDT 01:29 UTC, FORM/USDT 01:03 UTC) — both pure-momentum, no-catalyst, `waiting_for_entry`. The 23:34 review's live crypto ideas (XPL/USDT swing, BNB/USDT swing) are both still `waiting_for_entry`/`triggered` per tonight's active-signals pull — no resolution either way overnight.
- **TODO-crypto-scalp-mode-inactive is now resolved as an explicit, deliberate config decision** ("negative forward edge; research data retained"), not a silent regression as the last three reviews suspected — closing that recurring finding (see §14).
- **Scheduler health improved**: cycle 1 finished `ok=94/failed=12`, well below the prior cycle's 29/105-step timeout cascade — though `refresh obsidian dashboard` still timed out, keeping that specific recurring TODO open.
- Catalyst mapping ratio shifted (58.4% unmapped tonight vs 73.7% last night) — today's file is a fresh regeneration (yesterday's folder had rolled over), so this is a new-day baseline, not a trend signal yet.

## 5. Catalyst Coverage
- Catalyst events file (regenerated this run via the allowed CLI): **500 total rows, 208 mapped to a symbol, 292 unmapped (58.4% unmapped)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- 2 active narrative baskets: `perps_dex_narrative` (HYPE/USDT primary; DYDX/GMX/ASTER related — no live A/B signal currently riding this basket), `momentum_breakout` (UNI/USDT + DOT/USDT explicitly flagged catalyst-backed by the basket's own summary — "treat as catalyst-backed, watch pullback / do NOT chase"; AUCTION/USDT + DOGS/USDT unconfirmed/no-catalyst within the same cluster).
- Top 3 unmapped illustrative headlines: "South Korean stocks open higher, led by chip gains amid Middle East tensions" (importance 0.44), "Defense Minister Ahn Gyu-back will travel to Croatia on Wednesday..." (importance 0.44), "Gold slips; traders eye inflation data - WSJ" (importance 0.44) — all macro/regional noise, none symbol-specific to a tradeable crypto/stock ticker.
- As with the last several reviews: the dominant story tonight (the Iran/Jordan/Navy escalation) lives in the macro/regime layer, not the per-symbol catalyst-mapping layer — its absence from the "mapped" count is expected, not a mapping failure.

## 6. Market Landscape

Overnight brought a real escalation in the Iran-US confrontation that the 23:34 EEST review closed out as "still developing": IRGC state media now claims direct ballistic-missile strikes on two US Navy destroyers (USS Delbert D. Black, USS John Paul Jones) causing "significant damage" — a claim not yet independently corroborated in the internal feed — alongside a 20-missile barrage on a US base in Jordan (Jordanian air defense intercepted 18 of 20, no casualties reported) and an Iranian claim of capturing a US submarine drone in the Strait of Hormuz. US Central Command's response, destroying five Iranian crude oil carriers, is the other side of the exchange. Yet the market reaction has not been a clean, uniform risk-off cascade: oil continued grinding higher (Brent ~$99.37, WTI ~$94.47, both outlets now running "$100 oil" headlines), but gold actually fell about 1% on rate-path concerns, and — most notably — Asia-Pacific equities opened mostly higher on the news, explicitly "shrugging off" the weak Wall Street lead, with South Korean chip names singled out as a pocket of strength. A single-source correction already circulated (01:14 UTC, "reports of a renewed attack targeting Jordan are false"), a reminder that headline velocity is outrunning verification right now. Crypto itself remains the quiet corner of this story: BTC last read $79,280 (-0.67%) and ETH $2,484 (-0.41%) as of the freshest (01:57 EEST) swing report, still sitting in a transition_down/uptrend split with macro risk scored 100/100 risk-off — yet altcoin breadth stayed elevated (75.0% above EMA20, 87.5% above EMA50), the same "regime hasn't caught up to the macro shock yet" tension flagged in the last review. Two new pure-momentum B-tier swing longs (PROM/USDT, FORM/USDT) appeared in the small hours, both still unfilled, both with no catalyst backing found in news_items. Structurally, the Asia dead-zone guard (00:00-06:00 UTC) is independently suppressing crypto scalp/intraday actionability at this exact hour regardless of the geopolitical overlay — both the swing and intraday reports show zero A-tier and zero B-tier "actionable now" trade ideas, watchlist/C-tier only.

### Market Mood / Risk Routing
- Crypto mood: **mixed — risk-off macro overlay (BTC transition_down, macro risk 100/100) against still-elevated altcoin breadth (75.0%/87.5%); Asia dead-zone guard (00-06 UTC) independently caps actionability right now**
- Stocks mood: **closed (RTH resumes later today)** — pre-close context only; the one live watch-only idea (REGN swing long) is unchanged and inside its multi-week window
- Dominant narrative: escalating, still-developing Iran-US military exchange (claimed destroyer strikes, Jordan missile barrage, captured submarine drone, destroyed oil carriers) with a genuinely mixed market reaction (oil up, gold down, Asia equities up); secondary: momentum_breakout catalyst basket (UNI/DOT, explicitly catalyst-backed, do-not-chase)
- Preferred side now: **catalyst-backed watch over fresh momentum chases — the dominant story is still an unresolved, partially-unverified escalation; crypto has two fresh pure-momentum long-watches (PROM, FORM) and two catalyst-backed long-watches already entered (DOT, UNI)**
- Best long candidate: **PROM/USDT** (freshest B-tier swing, ~16min old, RS-leader momentum, waiting_for_entry, no catalyst — confirm pullback fill before treating as live)
- Best short candidate: **none live** — 100% of tonight's 50 active crypto B-tier signals are long; would need a confirmed BTC breakdown or the oil-shock tape visibly bleeding into BTC/ETH majors before a clean short thesis exists
- Best catalyst-backed candidate: **DOT/USDT** (momentum_breakout basket, B-tier swing, already `triggered`/entered ~2 days ago — re-verify invalidation hasn't been threatened)
- What to avoid: fresh positioning directly off unverified single-source Iran/Jordan headlines (one correction already circulated at 01:14 UTC); chasing PROM/FORM above their planned pullback zones; treating BNB/USDT's ~3-day-aging unfilled zone as a fresh idea
- What would change the view: confirmation (or denial) of the claimed destroyer strikes from a second independent source; any further Gulf-shipping incident; a fresher catalyst-cycle file with the mapping ratio improving; BTC/ETH price action once the Asia dead-zone window closes at 06:00 UTC (09:00 EEST)

## 7. Candidate Deep Dives

### PROM/USDT (crypto swing, B-tier 65.7 — freshest long-watch)
- Created 2026-09-09T01:29:07 UTC (~16min old at read time), `waiting_for_entry`, zone 5.7849-5.8514, invalidation 5.7037.
- Has price already reacted? Yes — 24h +7.08%, 7d +24.46%, RS vs BTC +7.62% (swing report Strongest Symbols, score 88.0); current price 5.943 per the report's Desk Notes, meaning price sits ~0.5-0.9 ATR (ATR 0.183) above the planned entry zone — a genuine pullback watch, not an already-filled chase.
- Is there a retest/pullback structure? The report's own C-tier writeup (Trade Idea #1) frames this explicitly as "watch only... conditional pullback zone," consistent with tonight's B-tier proposed_signal using the same zone.
- Catalyst confirmation? None — "no fresh verified catalyst detected" (swing report). Pure RS-leader momentum.
- Aligned with mood? Loosely — crypto mood is mixed/risk-off-tilted overall; a no-catalyst long into that backdrop, plus the Asia dead-zone actionability cap, argues for patience over urgency.
- Would entry now be late? No — still above the zone, unfilled.
- Actionable now or after confirmation? After a confirmed fill inside 5.7849-5.8514 with volume holding.
- Invalidation: 5.7037 (1h close beyond, per the swing report's watchlist framing).

### FORM/USDT (crypto swing, B-tier 68.1 — second fresh long-watch)
- Created 2026-09-09T01:03:02 UTC (~42min old), `waiting_for_entry`, zone 0.29611-0.30386, invalidation 0.28663.
- Has price already reacted? Yes — 24h +21.51% (swing report), +16.43% in the slightly earlier intraday report read — a fast mover; scored 91.5 in the swing report's Strongest Symbols list.
- Catalyst confirmation? None found for FORM specifically in news_items or the two active baskets.
- Chase risk: given the size of the 24h move (+21.51%), this is the higher chase-risk name of tonight's two fresh longs — the entry zone itself is the discipline mechanism; do not enter above it.
- Actionable now or after confirmation? After a confirmed fill inside the zone only.
- Invalidation: 0.28663.

### DOT/USDT (crypto swing, B-tier — catalyst-backed, already entered)
- Signal created 2026-09-07T05:03:21 UTC (~2 days aging), status `triggered` (entered, unresolved — not yet at TP/SL).
- Catalyst backing: explicitly named in tonight's `momentum_breakout` basket as catalyst-backed ("treat as catalyst-backed, watch pullback / do NOT chase; NOT a no-catalyst momentum chase") — one of only two symbols (with UNI) given that explicit confirmation in the basket's own summary.
- Aligned with mood? The catalyst-backed framing is a genuine edge over tonight's two pure-momentum names, but the position is already 2 days old — this is a hold/monitor situation, not a fresh entry decision.
- What would invalidate: re-verify the original invalidation level against current price before the next review; no invalidation breach found in tonight's active-signals pull (still `triggered`, not `stopped`).

### UNI/USDT (crypto swing, B-tier — same catalyst basket, more aged)
- Signal created 2026-09-06T02:54:10 UTC (~3 days aging), status `triggered` (entered, unresolved).
- Same `momentum_breakout` catalyst-backed confirmation as DOT/USDT, but materially more aged — carried forward as a secondary catalyst-backed hold, not a fresh idea.
- No invalidation breach found in tonight's pull.

### BNB/USDT (crypto swing, B-tier 73.8 — avoid/stale-watch carryover)
- `waiting_for_entry` since 2026-09-06T02:54:10 UTC (~3 days aging), unchanged zone 759.24-761.96, invalidation 755.92 — identical figures to the 23:34 review, meaning it has neither filled nor been invalidated in the last ~5 hours.
- Catalyst backing (`binance_ecosystem_teaser` basket) is itself unrefreshed across multiple review cycles now (first flagged stale at 21:55 EEST last night).
- Verdict: bordering on stale-before-entry. Not urgent to act on; flagged as this cycle's avoid/no-fresh-action candidate rather than a live idea.

## 8. Best Candidates Ranked
1. **DOT/USDT catalyst-watch** (crypto, already entered/`triggered`, momentum_breakout-confirmed catalyst-backed, ~2 days aging) — the strongest-backed idea standing; re-verify invalidation before next review.
2. **PROM/USDT long-watch** (crypto, freshest, ~16min old, pure momentum, no catalyst) — confirm pullback fill inside 5.7849-5.8514 before treating as live.
3. **FORM/USDT long-watch** (crypto, ~42min old, pure momentum, no catalyst, higher chase-risk given the size of its 24h move) — confirm fill inside 0.29611-0.30386 only, do not chase above.
4. **UNI/USDT catalyst-watch** (crypto, already entered, same basket as DOT but ~3 days aged) — secondary catalyst-backed hold.
5. Short-watch (no symbol yet): would require a confirmed BTC breakdown through the transition_down structure, or clear bleed-through from the oil-shock equity tape into BTC/ETH majors — neither condition is met tonight.

## 9. Avoid / No Trade
*(This decision window only — scanning, tracking, and monitoring continue regardless.)*
- **Fresh positioning directly off single-source Iran/Jordan headlines** — a false-alarm correction already circulated once tonight (01:14 UTC); the underlying story (claimed destroyer strikes, submarine-drone capture) remains partially unverified in the internal feed even where multiple wires agree on the broad shape of events.
- **Chasing PROM/USDT or FORM/USDT above their planned entry zones** — both are unfilled pullback watches, not confirmed entries; FORM in particular carries real chase-risk given its outsized 24h move.
- **BNB/USDT** should not be treated as a fresh idea — unchanged zone for ~3 days, catalyst itself stale across multiple review cycles.
- General: crypto scalp/intraday actionability is independently capped by the Asia dead-zone guard (00:00-06:00 UTC) until 09:00 EEST — no fresh intraday chase should be initiated regardless of setup quality until that window closes. Continue avoiding no-catalyst C-tier momentum names given the desk's own documented weak triggered-winrate (B-tier ~19% triggered winrate lifetime, per tonight's signal-stats run).

## 10. Main Risks
- **Geopolitical, escalating and partially unverified:** claimed direct Iran-US military exchange (destroyer strikes, Jordan missile barrage, captured submarine drone, destroyed Iranian oil carriers) with a genuinely mixed market reaction (oil up, gold down, Asia equities up) rather than a clean risk-off cascade — the single biggest swing factor into the rest of the Asia session and the European open.
- **Headline-verification risk:** a false-alarm correction already circulated once tonight; single-source Telegram/state-media claims from this point should not be treated as confirmed without a second independent source.
- **Scheduler/data-pipeline health — improved but not resolved:** cycle 1 finished with only 12 failed steps (down from 29 last night), but `refresh obsidian dashboard` timed out again — the recurring pattern from 2026-08-31 onward is not yet fully resolved (see §14).
- **Execution-lifecycle ambiguity — unresolved, carried forward:** the 7 stocks A/B `expired` rows from the prior 24h window still lack a queryable fill-event field to split entered-unresolved from no-entry (same open TODO as the 23:34 review).
- Catalyst mapping remains weak (58.4% unmapped tonight) — useful for context, not for symbol-specific final decisions.
- Crypto signal-generation remains directionally one-sided: 100% of tonight's 50 active B-tier signals are long — no short setups exist to diversify against a further risk-off leg if the geopolitical story worsens.

## 11. Action Plan — next 4 hours
- Watch for a second independent source confirming or denying the claimed US Navy destroyer strikes and the submarine-drone capture claim before treating either as settled fact.
- Re-verify PROM/USDT and FORM/USDT fills at the next review (11:30 EEST slot); if still unfilled and the zones haven't moved, note aging but do not chase.
- Re-confirm DOT/USDT and UNI/USDT haven't breached invalidation — both are open/unresolved catalyst-backed positions riding the momentum_breakout basket.
- No fresh stocks action needed — RTH remains closed; use the pre-US-open review (16:20 EEST) to reassess gap risk from the overnight oil/geopolitical developments once pre-market data exists.
- Do not initiate fresh crypto intraday/scalp entries until the Asia dead-zone window closes at 09:00 EEST, regardless of setup quality.
- Monitor whether the two new B-tier longs (PROM, FORM) represent a genuine pipeline pickup in volume or a one-off pair — compare against the next 1-2 cycles.

## 12. Final Verdict per Mode
- **Crypto scalp:** deliberately disabled (`negative forward edge; research data retained`) — confirmed this cycle via an explicit scheduler log line, not a regression. No verdict applicable; TODO closed (see §14).
- **Crypto intraday/swing:** two new pure-momentum B-tier swing longs (PROM, FORM) since the last review, both watch-only pending fill; two catalyst-backed swing longs (DOT, UNI) already entered/unresolved, riding the confirmed momentum_breakout basket; one aging catalyst-backed long (BNB) bordering on stale. Asia dead-zone guard independently caps fresh actionability until 09:00 EEST. Treat as low-urgency, watch-and-confirm.
- **Stocks intraday:** RTH closed; only REGN swing long remains a standing watch-only idea (unchanged, inside its multi-week window); nothing fresh to act on until the pre-market/RTH reopens.
- **Stocks swing / invest:** deprecated (shadow-only position framework in effect) — not evaluated, consistent with prior reviews.

## 13. Sources
- Internal: [proposed_signals / news_items SQLite queries — this session, 2026-09-09 04:30-04:45 EEST]
- [data/reports/swing/2026-09-08_22-58_swing_report.md] (generated 2026-09-09 01:57:50 EEST)
- [data/reports/intraday/2026-09-08_20-48_intraday_report.md] (generated 2026-09-08 23:47:37 EEST)
- [data/catalysts/2026-09-09/catalyst_events.jsonl], [narrative_baskets.jsonl] (regenerated this run via `catalyst-scan --no-print`)
- [data/scheduled_runs/2026-09-08_default_schedule/scheduler.log] (live production log, read ~04:45 EEST)
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_2330.md] (prior review, 23:15/23:34 EEST, used for §4 comparison)
- news_items (internal, t.me/ClashReport): "IRGC: We struck the U.S. destroyers USS Delbert D. Black (DDG-119) and USS John Paul Jones (DDG-53) with ballistic missiles, causing significant damage," published 2026-09-08T23:19:07Z
- news_items (internal, t.me/marketfeed / Jordanian Army via t.me/Middle_East_Spectator): "Jordan: 20 ballistic missiles fired from Iran toward its territory... air defences intercepted and destroyed 18 of the 20 and two fell in areas away from population centres, no casualties reported," published 2026-09-08T23:37-23:51Z
- news_items (internal, Finnhub market-news / Reuters): "US military says it destroyed five Iranian oil carriers after attempted missile attacks," published 2026-09-09T00:56:01Z (CNBC Markets variant) / 23:05:45Z (Finnhub/Reuters variant)
- news_items (internal, Finnhub market-news / Reuters): "Iran says it captured US submarine drone in Strait of Hormuz," published 2026-09-08T22:33:55Z
- news_items (internal, t.me/Middle_East_Spectator): "Reports of a renewed attack targeting Jordan are false," published 2026-09-09T01:14:27Z
- news_items (internal, CNBC Markets): "Brent crude nears $100 a barrel as U.S.-Iran tit-for-tat strikes stoke supply worries," published 2026-09-09T00:33:31Z
- news_items (internal, t.me/marketfeed): "Oil was the main market concern, with Brent rising 1.5% to $99.37 a barrel and WTI reaching $94.47... Asia-Pac stocks begin mostly higher with the region shrugging off the weak lead from Wall St," published 2026-09-09T00:11-00:16Z
- news_items (internal, t.me/marketfeed): "Gold fell 1% to $4,357.88 an ounce as rising Middle East tensions pushed oil prices higher... 10-year Treasury yields held near 4.79%," published 2026-09-08T23:33:04Z
- No external web sources cited this cycle (internal-first discipline satisfied; all citations above are dated, sourced, already-ingested internal `news_items` rows).

## 14. Fix Requests / TODO

### TODO-crypto-scalp-mode-inactive (RESOLVED — closing recurring TODO)
- **issue (resolved):** The last three reviews (2026-09-08 18:39, 21:55, 23:34 EEST) flagged `data/reports/scalp/` producing no new report since 2026-08-30 as an unconfirmed possible silent regression.
- **evidence:** `data/scheduled_runs/2026-09-08_default_schedule/scheduler.log`, line at 2026-09-09 04:31:44,233: `[INFO] NOTE: crypto scalp report — disabled: negative forward edge; research data retained.`
- **resolution:** This is a deliberate, logged config decision (negative forward edge found in research), not a regression. No further action needed — closing this recurring TODO. If a human wants scalp mode reconsidered later, that would be a new, separate decision, not a bug fix.
- **priority:** n/a (resolved)
- **first observed:** 2026-08-30/31 (recurring across 3+ reviews); **resolved:** 2026-09-09 04:45 EEST.

### TODO-scheduler-timeout-obsidian-dashboard (recurring, narrowed)
- **issue:** `refresh obsidian dashboard` timed out again this cycle (`[ERROR] CMD TIMEOUT: refresh obsidian dashboard` at 02:29:34 EEST), consistent with the broader step-timeout-cascade pattern flagged across multiple prior reviews and the 2026-08-31 ~6h05m hang incident in project memory. Notably, cycle 1's overall fail count (12/106) was much lower than the prior cycle's 29/105 — the cascade may be narrowing toward this specific step rather than being systemic tonight.
- **evidence:** `data/scheduled_runs/2026-09-08_default_schedule/scheduler.log`, lines 2026-09-09 02:29:34,695-697.
- **suggested manual fix:** Given the fail count dropped sharply cycle-over-cycle, a human-driven session should check whether `refresh obsidian dashboard` specifically has a distinct root cause (e.g., a file lock, an external dependency, or an Obsidian-vault-side issue) separate from the broader multi-step cascade seen on prior nights, rather than assuming they share one fix.
- **priority:** medium (downgraded from high — the broader cascade appears to be narrowing)
- **first observed (this recurrence):** 2026-09-09 04:45 EEST (recurring: 2026-08-31 ~6h05m hang; 2026-09-08 21:55 and 23:34 EEST reviews).

### TODO-expired-status-entered-vs-no-entry-ambiguity (recurring, unresolved)
- **issue:** Stocks A/B signals resolving to status `expired` still cannot be split into entered-unresolved vs no-entry from the exported `proposed_signals` schema — same gap as the 23:34 EEST review (7 affected rows: COIN, UBER, SHOP, V, BIIB, PYPL, ARM).
- **evidence:** unchanged from the prior review's finding; no new query performed this cycle since it's the same 24h-old batch, carried forward unresolved.
- **suggested manual fix:** unchanged — a human-driven session should check whether `signal_outcomes` (or an equivalent fill-event table) can be joined to distinguish entered-unresolved from no-entry, and consider exposing the split directly in the status vocabulary (e.g. `expired_entered` vs `expired_no_entry`).
- **priority:** medium
- **first observed:** 2026-09-08 23:34 EEST (recurring, unresolved this cycle).

### TODO-crypto-catalyst-mapping-fluctuating (recurring, informational)
- **issue:** Catalyst mapping ratio moved from 73.7% unmapped (last night's file) to 58.4% unmapped (tonight's freshly regenerated file) — still above the 50% "weak" threshold, but a meaningfully different ratio day-over-day on what should be a similar event mix. Worth confirming whether this variance is normal day-to-day noise or reflects a symbol-resolver behavior change.
- **evidence:** `data/catalysts/2026-09-08/catalyst_events.jsonl` (657/2500 mapped, 26.3% mapped) vs `data/catalysts/2026-09-09/catalyst_events.jsonl` (208/500 mapped, 41.6% mapped) — different total row counts too (2500 vs 500), which may itself explain part of the swing (smaller sample, different event mix) rather than a resolver change.
- **suggested manual fix:** A human-driven session should check whether the total-event-count difference (2500 vs 500) reflects a genuine data-volume difference between days or a partial/early read of today's still-accumulating file, before concluding anything about the resolver itself.
- **priority:** low
- **first observed:** 2026-09-09 04:45 EEST.
