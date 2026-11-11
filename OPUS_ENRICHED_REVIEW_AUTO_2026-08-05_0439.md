# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (04:30 EEST target, fired ~04:39). **Advisory only — no auto-trade.** Stocks are closed at this hour — every stocks row is C-tier planning/watchlist context only, never actionable per standing framework. Crypto: zero A-tier signals, 34 active B-tier rows, only **one** genuinely new signal this cycle (EPIC/USDT intraday, waiting_for_entry, created 02:16 EEST). Market regime stayed **transition/mixed**: BTC transition_up, but ETH flipped from range (22:54 report) to **downtrend** (04:03 report) and altcoin breadth softened 75%→69% above EMA20 — a mild cooling into the Asia session, not a reversal. Crypto macro/geopolitics overlay remains pinned near-max risk-off (**99.6/100**, driven by ongoing Strait-of-Hormuz headlines, not the now-de-escalating Coldcard hack) against still-constructive price structure — the same unresolved macro-vs-price divergence flagged in every review this week. The standout finding this cycle: **BICO/USDT carries three contradictory scores in the same report cycle** — a live triggered B-tier signal at 69.7, a "do not chase / >2 ATR from EMA20" watchlist read at 35.5, and a "catalyst_backed" narrative-basket tag at 84 even though its own thesis explicitly states "No fresh catalyst is verified" — routed to **avoid/manual-review**, not a clean long. Best clean long this cycle is **STO/USDT** (RS-leader, volume-confirmed, no chase flag, both intraday+swing triggered). No clean short fired. Catalyst→symbol mapping improved to **59.8% unmapped** (down from 63.5% flat all of yesterday) — still over the 50% weak-mapping threshold but the best reading since 04:45 yesterday. No untracked legacy alerts. TUT/USDT remains the desk's one continuously-open crypto position, carried through the Asia session unchanged.

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-05_00-57_scalp_report.md` (~42min old, fresh), `data/reports/intraday/2026-08-05_01-03_intraday_report.md` (~36min old, fresh, most current read this cycle), `data/reports/swing/2026-08-04_19-54_swing_report.md` (~5h45m old — **carry-forward**, no fresher swing report generated yet this cycle)
- Stocks: `data/reports/stocks/intraday/2026-08-05_01-23_stocks_intraday_report.md` (~16min old, fresh, but market closed — planning/watchlist only). Stocks swing/invest last generated 2026-07-01/02 — >1 month stale, excluded per standing deprecation.
- `data/catalysts/2026-08-05/catalyst_events.jsonl` (500 rows scanned, 299 null-symbol), `narrative_baskets.jsonl` (4 baskets), `catalyst_cycle_01-08.md`
- LLM packets: `data/processed/llm_analysis_packet.md` (~36min old), `data/processed/llm_stocks_packet.md` (~13min old)
- CLI: `active-signals --asset-class crypto` (34 rows), `active-signals --asset-class stocks` (50 rows, all C-tier), `signal-stats --asset-class crypto` (weekly), `signal-stats --asset-class stocks` (weekly), `detect_untracked_legacy_alerts --since 2026-08-05` (0 untracked)
- DB (read-only queries): `proposed_signals` (created_at filter, thesis/counter_thesis text), `news_items` (recent 5h, importance ≥0.6, telegram-source counts)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_2323.md` (post-close final daily review, 23:23 EEST)
- **External web research not invoked this cycle** — internal catalyst/news layer was fresh (<1-6h) and internally consistent for every candidate evaluated; no candidate's verdict depended on external verification. (Not the same as "unavailable" — it simply wasn't needed per §G's internal-first rule.)

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime ~04:35 EEST (~4min old) — fresh, not deferred. Latest `cycle_02_01-02_summary.md` mtime ~01:49 EEST (~2h50m old) — fresh (<3h), not deferred.
- Crypto scalp ~42min old, intraday ~36min old — both fresh. Crypto swing ~5h45m old — carry-forward (4-12h band); used with that caveat, no fresher swing scan available.
- Stocks intraday ~16min old — fresh, but market closed (planning/watchlist only per slot awareness). Stocks swing/invest stale >1 month — excluded, known-deprecated.
- No monitor/paper-status file read this cycle (outside allowed read list) — data_missing.
- No data-quality anomalies beyond: (1) the persistent catalyst-mapping weakness (§5), now improving; (2) the BICO/USDT 3-way score contradiction (§7); (3) the carried-forward legacy tp-hit/expiry lifecycle ambiguity (§14, unresolved since 2026-08-04).
- **TradingView / manual chart check unavailable** — no chart MCP loaded this cycle; all price-structure statements in §7 (ATR, EMA20 distance, chase-risk) are taken directly from the local OHLCV/ATR/EMA fields already computed inside the intraday/swing reports, not from any live chart inspection.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-05 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["monitor/paper-status file not read (outside allowed read list)", "no daily-only signal-stats breakdown from allowed CLI"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~4min old", "cycle_02 summary ~2h50m old, both fresh", "crypto scalp ~42min, intraday ~36min old, fresh", "crypto swing ~5h45m old, carry-forward, no fresher scan yet", "stocks intraday ~16min old but market closed"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "risk_off", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC transition_up in both swing (22:54) and intraday (04:03) reads", "ETH flipped range -> downtrend between the two reads", "altcoin breadth above EMA20 softened 75.0% -> 69.05%, above EMA50 70.0% -> 66.67%", "macro/geopolitics risk score 99.6/100, risk-off headwind, driven by Strait-of-Hormuz headlines (not Coldcard this cycle)", "both reports independently recommend 'selective only; demand clean invalidation'"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["59.8% unmapped today (299/500) -- improved vs yesterday's flat 63.5%, best reading since 04:45 yesterday (53.2%)", "4 narrative baskets: ai_narrative (NEAR/RENDER/TAO/FET, <1h), perps_dex_narrative (HYPE/DYDX/GMX/ASTER, <1h, HYPE also carries a fresh $1.28B token-unlock overhang), rwa_narrative (ONDO/XLM, <6h), momentum_breakout (BICO/HOME/SNXXB/KORUB, <1h, explicitly 'without confirmed news catalyst')", "BICO/USDT tagged catalyst_backed at score 84 in one report table despite its own signal thesis stating no fresh catalyst is verified -- direct internal contradiction"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["data_unavailable", "squeeze_risk"],
      "data_missing": ["no per-symbol funding/OI table read this cycle (derivatives_monitor log is JSON telemetry, not a per-symbol funding/OI snapshot in the allowed read set)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["derivatives_monitor cycle log confirms feeds running (binance/bybit/hyperliquid/okx/mexc all reporting rows) but no symbol-level funding/OI figures were pulled into this review", "prior review flagged HFT/USDT extreme long crowding and GIGGLE/ERA/AKE short-squeeze risk -- not re-verified this cycle, carried forward as unconfirmed"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "clean_retest", "stale_before_entry", "entry_fresh"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["STO/USDT: momentum 90-92.5/100, RS + volume_expansion tags, no chase-risk flag in either intraday or swing read -- cleanest entry in the batch", "BICO/USDT: explicit '>2 ATR from EMA20, do not chase' flag in the same report that also lists it triggered at 69.7 -- contradictory", "HOME/USDT: 'volume is below average; breakout confirmation is weak' flagged directly in its own counter-thesis", "EPIC/USDT: newest signal this cycle (02:16 EEST, waiting_for_entry) but overlaps 2 older triggered swing rows for the same symbol -- lifecycle ambiguity, not a clean fresh fill"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": ["CLI does not label lifecycle state directly -- classification below is manual, from status + expires_at"],
      "suggested_effect": "advisory_only",
      "facts_used": ["~17/34 crypto rows OPEN actionable (triggered or tp1/tp2_hit with expires_at still in the future)", "1/34 WAITING for entry (EPIC/USDT intraday)", "~15/34 ENTERED UNRESOLVED (tp1_hit/tp2_hit but expires_at already in the past -- entry was filled and partially profitable, but no final TP/SL close recorded before the window lapsed; same carried-forward ambiguity as every review this week, see §14)", "BICO/USDT flagged NEEDS REVIEW for the 3-way score contradiction", "stocks: all 50 rows C-tier, market-closed, planning/watchlist only, not lifecycle-tracked this cycle"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["no daily paper PnL figure read this cycle (not in allowed CLI list)", "PLTR/MSFT legal-flag status not re-verified this cycle (carried from memory/prior review, not confirmed fresh)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Coldcard hack narrative continues but de-escalating (importance 0.79-0.84 in today's top catalysts vs dominating yesterday's list); Michael Saylor/Strategy wallet moved out 1,030 BTC (~$66.14M) ~2h ago per Lookonchain -- adds a fresh, unconfirmed 'is Saylor selling' sentiment overhang, no desk position affected directly", "legal/regulatory risk catalysts today (BABA, Primoris, GPGI/CMPO, FUTU, PLNT, PNR, PROCEPT) are all lawsuit-mill PR Newswire noise and do not overlap any symbol in this cycle's active-signals list", "BICO/USDT contradiction routed to manual_review rather than a clean actionable, per risk discipline"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly (all-tier, n=78): PF 1.7765, avgR +0.2164, totalR +13.2, triggered winrate 21% (CLI's own observation: 'low, review entries')", "by mode: intraday PF 3.34/avgR +0.86 (strong), swing PF 0.90/avgR -0.024 (near-breakeven at the weekly aggregate level -- notably weaker than the self-reported crypto_swing_narrative_rs_momentum playbook's 14d WR72%/PF5.80, a real divergence between the specific playbook and the mode-wide aggregate), scalp PF 0.167/avgR -0.19 (weak, self-framed as data-collection-only)", "weekend=Y signals underperform (PF 0.50, n=10, CLI's own observation) -- not active today (Wednesday)", "stocks weekly (n=230, reliable): PF 0.59, avgR -0.12, totalR -4.5; tier=C triggered winrate 5%, PF 0.65 below 0.8 (CLI's own observation) -- confirms C-tier-never-actionable framework is correctly excluding this bucket"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.55,
      "reason_codes": ["mixed", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["no A-tier anywhere; the only genuinely fresh crypto idea (EPIC/USDT) is entry-ambiguous due to overlapping older rows; the highest-quality clean read (STO/USDT) is a carried triggered position, not a brand-new fill; BICO/USDT's internal contradiction is this cycle's single most important finding and is routed to avoid, not chased despite its 69.7 score; stocks are closed and 100% non-actionable by design"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.55,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "STO/USDT", "trigger": "already triggered (swing 0.04054-0.04162, intraday 0.04084-0.04192); invalidation 0.0392/0.0395 unbroken; add-on only on a clean retest, not a fresh chase" },
    "best_short_candidate":    { "symbol": "none clean this cycle", "trigger": "GIGGLE/USDT watch: confirmed bearish HTF structure + stop above swing high once thin-liquidity/squeeze risk clears (unconfirmed this cycle, carried from prior read)" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "rwa_narrative basket primary, fresh <6h, multi-week institutional thesis (DTCC/Stellar tokenization) -- watch for a fresh B/A-tier signal with news_supported=1 before treating as actionable; no live signal fired this cycle" },
    "avoid_candidate":         { "symbol": "BICO/USDT", "reason": "same symbol, same cycle: triggered B-tier at 69.7, watchlist funnel score 35.5 with an explicit 'do not chase, >2 ATR from EMA20' flag, and a separate 'catalyst_backed' tag at 84 that contradicts its own thesis text ('No fresh catalyst is verified'). Manual review required before treating the triggered signal as clean." },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.8 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.6 | mixed, chop, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.6 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | data_unavailable, squeeze_risk | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, clean_retest, stale_before_entry, entry_fresh | advisory_only |
| execution_lifecycle | caution | 0.55 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.55 | headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.6 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.55 | mixed, wait_for_trigger, manual_review | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_2323.md` (23:23 EEST, post-close final daily review):

- **New:** EPIC/USDT intraday long re-fired as a fresh B-tier waiting_for_entry row (score 68.0, created 02:16 EEST) — distinct signal_id from the swing-mode EPIC/USDT rows already open; STO/USDT emerged as this session's cleanest, highest-scoring long (78.1 swing / 74.2 intraday), not called out by name in the prior review.
- **Removed:** none of yesterday's watchlist names (HOME/USDT, COTI/USDT, BICO/USDT) dropped off — all three persist, still sub-threshold or contradictory.
- **Upgraded/downgraded:** stocks flipped back to C-tier-across-the-board as expected overnight (market fully closed, no fresh open/close-gate transition to report); crypto ETH trend downgraded range → downtrend between the 22:54 and 04:03 reports; altcoin breadth softened ~6 points.
- **New catalysts:** Michael Saylor/Strategy BTC wallet outflow (~$66M, 2h old, unconfirmed "dumping" framing); Intesa Sanpaolo cutting IBIT exposure 94% while adding ETH exposure (institutional rotation signal, single-source).
- **Thesis changed:** BICO/USDT's status is now materially more uncertain than it appeared in the 23:23 review's brief mention — the 3-way score contradiction (35.5 / 69.7 / 84) was not previously surfaced by name.
- **Confirmed:** TUT/USDT thesis unchanged, still open; no untracked legacy alerts (bug dormant, root cause still unfixed, TODO carried); Coldcard hack narrative continues de-escalating (importance dropped out of the very top of today's catalyst list, though still present).
- **Invalidated:** none.
- Catalyst mapping **improved**: 63.5% (flat all of yesterday) → **59.8%** unmapped today — the best reading since 04:45 yesterday (53.2%), worth confirming it holds through the next cycle before declaring a genuine trend reversal.

## 5. Catalyst Coverage

- Total catalyst events today: **500**; mapped (non-null symbol): **201**; unmapped: **299** (**59.8%**).
- Narrative baskets: **4** — `ai_narrative` (NEAR/RENDER/TAO/FET primary, <1h fresh), `perps_dex_narrative` (HYPE primary, <1h fresh, HYPE also carries a $1.28B token-unlock overhang this month), `rwa_narrative` (ONDO/XLM primary, <6h fresh), `momentum_breakout` (BICO/SNXXB/KORUB/HOME primary, <1h fresh, explicitly "without confirmed news catalyst" per its own summary).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Unmapped is 59.8%, over the 50% threshold, though improved from yesterday's flat 63.5%.
- Top unmapped headlines this cycle: "Agthia meldet eine verbesserte Finanzlage..." (foreign-language corporate PR), a large-figure USDC-mint alert with no symbol tag, a ByBit BACUSDT listing announcement (should plausibly map but does not), a South African crypto-offshoring regulatory proposal, a Western Union USDPT-Visa-card launch announcement — a mix of foreign-language PR, generic macro/regulatory chatter, and exchange-listing announcements that should be mappable but aren't, consistent with the pattern flagged all week (§14).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed** — BTC transition_up holds, but ETH flipped range→downtrend and altcoin breadth softened (75%→69% above EMA20) between the last two scans; macro/geopolitics overlay pinned near-max risk-off (99.6/100, Strait-of-Hormuz headlines) against still-constructive underlying structure. Recommended style in both reports: "selective only; demand clean invalidation."
- Stocks mood: **closed** — planning/watchlist only until the 09:30 ET open; all 50 active rows are C-tier by design at this hour.
- Dominant narrative: Strait-of-Hormuz geopolitical risk-off overlay (unresolved, drives the 99.6/100 macro score) vs. the now-de-escalating Coldcard hardware-wallet hack; Saylor/Strategy BTC outflow adds a fresh but unconfirmed sentiment wrinkle.
- Preferred side now: **longs, selectively** — clean RS/volume names only (STO/USDT), not chase-flagged names (BICO/USDT) or weak-volume names (HOME/USDT).
- Best long candidate: **STO/USDT** — see §7.
- Best short candidate: none clean — GIGGLE/USDT remains the weakest-RS name (-12.81% vs BTC in the last swing read) but its squeeze-risk cap was not re-verified this cycle; treat as watch-only until a fresh bearish HTF confirmation appears.
- Best catalyst-backed candidate: **ONDO/USDT** (rwa_narrative primary, fresh <6h) — no live signal fired yet, watch for one with `news_supported=1`.
- What to avoid: **BICO/USDT** (3-way internal score contradiction, explicit chase-risk flag — see §7); new crypto scalp entries generally (PF 0.167 this week); adding fresh exposure to HFT/USDT without re-verifying its crowding status (unconfirmed this cycle).
- What would change the view: ETH regime flipping back to range/uptrend on the next scan; altcoin breadth re-expanding past 70%; the Strait-of-Hormuz overlay de-escalating in the macro score; BICO/USDT's three scoring paths converging (or the desk publishing a corrected single score).

## 7. Candidate Deep Dives

### BICO/USDT (crypto swing long, B-tier triggered — NEEDS REVIEW / AVOID for now)
- Has price already reacted to the catalyst? No verified catalyst exists — the `momentum_breakout` basket explicitly labels BICO "without confirmed news catalyst," yet a separate report table tags it `catalyst_backed` (score 84) — a direct internal contradiction.
- Is the setup chasing? The same report that lists it triggered at 69.7 also flags it at 35.5 with "Price is more than 2 ATR from EMA20; do not chase" and "Entry quality is weak because the move is extended."
- Retest/pullback structure? Not evidenced — the report explicitly frames it as extended, not pulled back.
- Overextended (>2 ATR from EMA20)? Yes, per the report's own watchlist-funnel read.
- Would entry now be late? Yes, by the report's own words.
- What level makes it actionable? A confirmed pullback into a defensible zone with the score contradiction resolved (i.e., the desk should not present a symbol as both "triggered, tradeable" and "do not chase" in the same cycle) — this is a data-quality gate, not a price gate.
- Mood alignment: nominally aligned with the market's constructive breadth, but the entry-quality contradiction overrides that.
- Long/short/wait: wait — manual review, not a clean long.
- Actionable now or confirmation-only? No — confirmation-only, and the confirmation needed is on the data pipeline, not just price.
- Invalidates avoid call: the desk re-scoring BICO/USDT to a single consistent read across all tables/sections.
- Chase-risk: high, explicitly flagged.
- Catalyst confirmation/contradiction: contradicted (tagged catalyst_backed while its own thesis says no catalyst verified).

### STO/USDT (crypto swing + intraday long, B-tier triggered, actionable — best long this cycle)
- Has price already reacted to the catalyst? No catalyst cited — pure RS/momentum thesis (24h +13.93%, RS vs BTC +13.22%, volume 1.73x 20-period average — a genuine, if modest, volume confirmation).
- Is the setup chasing? No chase-risk flag in either the intraday or swing read, unlike BICO/HOME in the same reports.
- Retest/pullback structure? Entry zones (0.04054-0.04162 swing, 0.04084-0.04192 intraday) are already triggered — this is a continuation/pullback thesis already in progress, not a fresh chase.
- Overextended? Not flagged in either report.
- Would entry now be late? Existing exposure is already open (triggered); a fresh add should wait for a clean retest, not a market fill.
- What level makes it actionable (for an add-on)? Hold above invalidation (0.0392 swing / 0.0395 intraday); a retest of the entry zone would be the cleanest add point.
- Mood alignment: consistent with the constructive-but-softening breadth read; momentum score 90-92.5/100 with `relative_strength` + `volume_expansion` tags on the swing read.
- Long/short/wait: long, continuation.
- Actionable now or confirmation-only? Already triggered/open; treat as hold/monitor, add only on retest.
- Invalidates: close below 0.0392 (swing) / 0.0395 (intraday), or BTC breaking the transition_up structure.
- Chase-risk: low.
- Catalyst confirmation/contradiction: none either way — clean technical/RS thesis only, no contradiction like BICO.

### EPIC/USDT (crypto intraday long, B-tier waiting_for_entry, fresh this cycle — needs lifecycle care)
- Has price already reacted? No catalyst cited (news_supported=0); "Relative strength is not backed by strong current volume" and "Volume is below average; breakout confirmation is weak" are both flagged directly in its own counter-thesis.
- Is the setup chasing? Not per the report, but the volume-confirmation gap is a real weakness relative to STO/USDT's cleaner read.
- Retest/pullback structure? Entry plan is 0.9811-1.0009, a defined pullback zone.
- Overextended? Not flagged.
- Would entry now be late? No — status is waiting_for_entry, price has not yet filled.
- What level makes it actionable? A fill inside 0.9811-1.0009 holding above invalidation 0.9568.
- Mood alignment: consistent with the still-transition_up BTC structure, tempered by the weak-volume flag.
- Long/short/wait: long, wait-for-entry.
- Actionable now or confirmation-only? Wait-for-entry by design; separately, this symbol already carries two older triggered swing rows (one weekend-flagged, expiring 08-08) — treat this intraday row as a distinct, smaller idea, not a size-up on existing exposure, until the lifecycle labeling TODO (§14) is resolved.
- Invalidates: 1h close beyond 0.9568.
- Chase-risk: low (still waiting).
- Catalyst confirmation/contradiction: none — pure technical thesis, no contradiction.

### HOME/USDT (crypto swing + intraday, B-tier, mixed status — watch only, not actionable)
- Has price already reacted? No — `momentum_breakout` basket lists it as a pure momentum mover (+22.7% one cycle) "without confirmed news catalyst."
- Is the setup chasing? Ambiguous — one active row shows tp1_hit (intraday, still within its window) while several swing rows show triggered; the underlying thesis for the swing row explicitly warns "Relative strength is not backed by strong current volume" and "Volume is below average; breakout confirmation is weak."
- Retest/pullback structure? Not clearly confirmed given the flagged weak-volume read.
- Overextended? Not directly flagged, but the volume gap raises the same quality concern as BICO/USDT, just without the outright contradiction.
- Would entry now be late? For a fresh entry, yes — treat as watch-only until volume confirms.
- What level makes it actionable? A breakout re-confirmed by volume ≥1x 20-period average, not the current 0.18x-0.34x reads seen across today's cycles.
- Mood alignment: nominally long-side but the confirmation gap keeps it below a clean actionable bar.
- Long/short/wait: wait-for-confirmation.
- Actionable now or confirmation-only? Confirmation-only.
- Invalidates: continued sub-average volume through the next 1-2 cycles.
- Chase-risk: moderate (extended move, weak volume backing).
- Catalyst confirmation/contradiction: none — consistent with its own "no catalyst" framing, unlike BICO.

### ONDO/USDT (crypto, no live signal — catalyst-watch only)
- Has price already reacted? The `rwa_narrative` basket (ONDO primary, with XLM) is framed as a "multi-week institutional thesis" (DTCC/Stellar tokenization coverage), fresh <6h, not a same-day pop.
- Is the setup chasing? N/A — no active signal exists; this is a pre-signal catalyst watch.
- Retest/pullback structure? N/A yet.
- What level/condition makes it actionable? A fresh B/A-tier `proposed_signal` for ONDO/USDT with `news_supported=1`, tying the RWA institutional narrative directly to a scored technical setup — none exists as of this cycle (the two ONDO rows in active-signals are both weeks-old, expired tp-hit rows from the scalp/intraday modes, not swing).
- Mood alignment: RWA/tokenization is a multi-week thesis, largely orthogonal to the current risk-off macro overlay — a reasonable catalyst-watch even in a cautious tape.
- Long/short/wait: wait-for-signal.
- Actionable now or confirmation-only? Confirmation-only — this is explicitly a watch, not a position.
- Invalidates the watch: the rwa_narrative basket dropping out of the next catalyst cycle, or no scored ONDO signal appearing within the next 1-2 cycles.
- Chase-risk: N/A (no signal yet).
- Catalyst confirmation/contradiction: confirmed narrative, no live signal to contradict it.

## 8. Best Candidates Ranked

1. **STO/USDT (crypto swing+intraday long, triggered, B-tier)** — best long-watch; hold, add only on a clean retest above invalidation (0.0392/0.0395).
2. **TUT/USDT (crypto swing long, OPEN, carried forward)** — hold/monitor into invalidation/TP, unchanged thesis.
3. **ONDO/USDT (crypto, catalyst-watch, no live signal)** — watch for a fresh B/A-tier signal with news_supported=1 tying the rwa_narrative basket to a scored setup.
4. **EPIC/USDT (crypto intraday long, waiting_for_entry, fresh this cycle)** — enter only on a fill inside 0.9811-1.0009, invalidation 0.9568; treat as distinct from the older swing-mode EPIC rows, not a size-up.
5. **BICO/USDT (crypto swing, AVOID / needs review)** — do not treat the 69.7 triggered score as clean; the same cycle flags it "do not chase" and contradicts its own no-catalyst thesis with a catalyst_backed tag.

HOME/USDT and GIGGLE/USDT remain the best watch-only names outside the top 5 (HOME on a volume-confirmation trigger, GIGGLE on a squeeze-risk-clearing trigger for a short).

## 9. Avoid / No Trade

*(This applies to this decision window / overnight-into-Asia only — scanning, tracking, and the scheduler continue unchanged.)*

- **BICO/USDT** — internal 3-way score contradiction (35.5 / 69.7 / 84) plus an explicit "do not chase, >2 ATR from EMA20" flag in the same cycle; manual review required before treating as a clean long.
- **Crypto scalp mode generally** — PF 0.167, avgR -0.19 this week; self-framed as data-collection-only.
- **HOME/USDT (fresh entries)** — weak-volume breakout confirmation flagged directly in its own thesis; watch, don't enter.
- **HFT/USDT (fresh long entries)** — prior review flagged extreme long crowding; not re-verified this cycle, so treated as still-cautionary pending confirmation.
- **New stocks positions of any kind** — market closed; all 50 active rows are C-tier by design, re-evaluate fresh at the 09:30 ET open.
- **New crypto shorts generally** — no clean bearish HTF structure identified this cycle; GIGGLE/USDT is the best watch but unconfirmed.

## 10. Main Risks

- Strait-of-Hormuz geopolitical overlay keeps the crypto macro/geopolitics risk score pinned at 99.6/100 (risk-off) even as underlying BTC/altcoin price structure stays transition/constructive — the same unresolved macro-vs-price divergence as every review this week; the situation itself (per today's own headline feed) shows early signs of de-escalation ("CENTCOM says the strait is still free and open," "oil dives on hopes of a deal") but that has not yet moved the internal 99.6/100 score.
- BICO/USDT's 3-way score contradiction is a genuine data-quality risk — if it recurs on other symbols, any "triggered" B-tier signal could be masking an unflagged chase-risk condition elsewhere in the batch that this review did not catch (only BICO was cross-checked against its watchlist-funnel read this cycle).
- ETH regime softened (range→downtrend) and altcoin breadth cooled (75%→69%) between the last two scans — worth confirming on the next cycle whether this is Asia-session noise or the start of a real rotation.
- Catalyst→symbol mapping remains over 50% unmapped (59.8%) despite the improvement — treat all catalyst-basket framing as directional color, not confirmation.
- Carried-forward legacy lifecycle ambiguity: ~15/34 crypto active-signal rows are tp1_hit/tp2_hit with `expires_at` already in the past — entered-unresolved, not cleanly closed, same unresolved TODO as every review this week (§14).
- Saylor/Strategy BTC wallet outflow (~$66M, unconfirmed framing) — worth watching for confirmation or denial in the next few cycles; no desk position is directly exposed.

## 11. Action Plan — next 4 hours

- Hold TUT/USDT and STO/USDT into their respective invalidations; add to STO/USDT only on a clean retest, not a market chase.
- Enter EPIC/USDT (intraday row) only on a fill inside 0.9811-1.0009 with 0.9568 unbroken; do not conflate with the older swing-mode EPIC/USDT rows.
- Do not act on BICO/USDT's triggered signal until the score contradiction is resolved or manually reviewed; flag internally for a human pass (see §14).
- Watch ONDO/USDT for a fresh scored signal tying the rwa_narrative basket to an actionable setup; watch GIGGLE/USDT for a confirmed bearish structure before considering any short.
- Re-check ETH regime and altcoin breadth on the next cycle to confirm whether the range→downtrend flip is noise or a genuine rotation.
- Do not initiate any stocks position before the 09:30 ET open — all current C-tier stocks names are re-evaluate-fresh-at-open by design.
- Continue scanning/tracking/monitors unchanged through the Asia session — this review recommends caution on new entries only, never a pause of any kind.

## 12. Final Verdict per Mode

- **Crypto scalp:** no trade — data-collection only, PF 0.167 this week.
- **Crypto intraday:** selective watch only — EPIC/USDT on a clean fill; avoid HOME/USDT and BICO/USDT-adjacent chase setups.
- **Crypto swing:** the desk's steadiest bucket — hold TUT/USDT and STO/USDT; BICO/USDT is explicitly NOT clean despite its triggered status, needs manual review.
- **Stocks intraday:** no trade — market closed, all rows mechanically C-tier by design; re-evaluate fresh at tomorrow's open.
- **Stocks swing/invest:** not evaluated — reports stale/deprecated since 2026-07-01/02, excluded per standing policy.

## 13. Sources

- Internal: `data/reports/scalp/2026-08-05_00-57_scalp_report.md`, `data/reports/intraday/2026-08-05_01-03_intraday_report.md`, `data/reports/swing/2026-08-04_19-54_swing_report.md`, `data/reports/stocks/intraday/2026-08-05_01-23_stocks_intraday_report.md`, `data/catalysts/2026-08-05/catalyst_events.jsonl`, `data/catalysts/2026-08-05/narrative_baskets.jsonl`, `data/catalysts/2026-08-05/catalyst_cycle_01-08.md`, `data/processed/llm_analysis_packet.md`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items` read-only queries), `OPUS_ENRICHED_REVIEW_AUTO_2026-08-04_2323.md`.
- No external sources this cycle (see §2 — internal data was sufficient and consistent for every candidate; no WebSearch/WebFetch run).

## 14. Fix Requests / TODO

### TODO-bico-triple-score-contradiction (priority: high, new this cycle)
- **issue:** BICO/USDT carries three different, mutually contradictory scores in the same report/cycle: a live `proposed_signals` row triggered at score 69.7 (swing, B-tier), a watchlist-funnel read in the same swing report at score 35.5 with an explicit "do not chase, >2 ATR from EMA20, breakout failure risk elevated" flag, and a separate narrative-basket cross-reference table tagging it `catalyst_backed` at score 84 — while the signal's own `thesis`/`counter_thesis` text explicitly states "No fresh catalyst is verified for this symbol" (twice).
- **evidence:** `data/reports/swing/2026-08-04_19-54_swing_report.md` (both the "Where Money Is Flowing" funnel section and the narrative-basket cross-reference table), `db/crypto_ai_desk.sqlite` `proposed_signals` row `sig_344704af4d161ecc`.
- **suggested manual fix:** a human-driven session should trace which scoring pass (deep-analysis funnel vs. narrative-basket tagger vs. the final `proposed_signals` writer) is authoritative, and why three different subsystems disagree by up to 48 points on the same symbol in the same report generation.
- **priority:** high
- **first observed:** 2026-08-05 04:39 EEST.

### TODO-catalyst-mapping-persistently-weak (priority: low, recurring, now improving)
- **issue:** Catalyst→symbol mapping has been over the 50% unmapped threshold for at least seven consecutive reviews: 53.2% → 57.2% → 60.2% → 62.9% → 63.5% → 63.5% (flat) → **59.8%** (this run, improved).
- **evidence:** `data/catalysts/2026-08-05/catalyst_events.jsonl` (500 rows today, 299 null-symbol).
- **suggested manual fix:** unchanged — revisit the symbol resolver in the catalyst layer; confirm over the next 1-2 cycles whether today's improvement holds or was noise.
- **priority:** low
- **first observed:** 2026-08-04 04:45 EEST (carried forward, improving).

### TODO-legacy-open-position-volume (priority: medium, carried forward, unresolved)
- **issue:** `active-signals` continues to return rows (~15/34 crypto this cycle) with tp1_hit/tp2_hit status alongside `expires_at` dates well in the past — unclear whether this is correct "not yet finally closed" behavior by design or a stuck closure job.
- **evidence:** this cycle's `active-signals --asset-class crypto` (34 rows); same pattern every review this week.
- **suggested manual fix:** unchanged — a human-driven session should confirm intended lifecycle semantics and add clearer status labeling.
- **priority:** medium
- **first observed:** 2026-08-04 11:39 EEST (carried forward, still unresolved).

### TODO-untracked-alert-bug-not-refired-but-unfixed (priority: high, recurring root cause, dormant this cycle)
- **issue:** The watchlist-alert signal-reuse bug (re-fire reuses a stale/closed `signal_id` instead of minting a fresh `proposed_signal`) produced no untracked alerts today (0 this run) — but the underlying root cause remains unfixed.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-05` returned 0 this run; prior confirmed instances on ALLO/USDT, BANK/USDT (2026-07-17) and TUT/USDT (2026-08-04 16:11).
- **suggested manual fix:** unchanged (TODO-3, raised to high priority 2026-07-17) — fix the watchlist-alert path so a re-fire mints a fresh `proposed_signal`.
- **priority:** high
- **first observed root cause:** 2026-07-17; **last confirmed instance:** 2026-08-04 16:11 EEST; **this cycle:** dormant, not fixed.

_All items above are TODOs for a separate human-driven review session — no code, scoring, or configuration was changed in producing this report._
