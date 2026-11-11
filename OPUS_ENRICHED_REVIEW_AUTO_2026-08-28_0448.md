# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

**Slot: crypto overnight / Asia review (advisory only / no auto-trade).** Scheduler is fresh (`scheduler.log` 2h22m old); the last cycle-summary file is from the prior evening (~5h25m old) but since scheduler.log alone is under 3h, no defer is triggered. Today's catalyst folder (`data/catalysts/2026-08-28/`) was missing at run start and was regenerated via the allowed `catalyst-scan` CLI (500 events, 2 baskets). Crypto regime is a clean **bullish trend (risk-on)** tonight (BTC/ETH uptrend, 75–83% altcoin breadth) with **zero A-tier and zero fresh B-tier** this cycle — the active book is the same 100%-long RS-momentum cohort (TAO/SOL/RUNE/CHIP/etc., mostly `triggered`/`tp1_hit`/`waiting_for_entry`) carried from prior cycles. Scalp remains kill-switch-disabled (Asia dead-zone guard). All short-side candidates tonight (FIL, SNXXB, SNDKB, ONT) are explicitly capped to C for "fighting a bullish tape" + squeeze/thin-liquidity risk — there is no clean short, only a watch-and-wait one. Stocks are closed (overnight); prior signals are all historical/expired — planning-only context. The **ONG/USDT bias-tag contradiction is now unresolved for a 4th consecutive cycle** and has gotten worse (internal tag now -43.05%, up from -26% two cycles ago), while three independent external price sources tonight all show ONG **up** over 24h (+28% to +160%, mutually inconsistent with each other too) — this is escalated to the top integrity item. Scanning, tracking, and the scheduler continue regardless of tonight's verdict.

## 2. Data Used

- `data/reports/scalp/2026-08-27_22-44_scalp_report.md` (generated 01:44 EEST, ~3.0h old — fresh)
- `data/reports/intraday/2026-08-27_23-14_intraday_report.md` (generated 02:14 EEST, ~2.6h old — fresh)
- `data/reports/swing/2026-08-27_12-46_swing_report.md` (generated 15:46 EEST, ~13.0h old — **borderline stale**, carried forward, no fresher source exists)
- `data/reports/stocks/intraday/2026-08-27_18-31_stocks_intraday_report.md` (generated 21:31 EEST, ~7.3h old — market closed overnight, planning-only)
- `data/reports/stocks/swing/2026-07-02_...` / `stocks/invest/2026-07-02_...` — ~8 weeks stale, excluded (known-deprecated pipeline, not re-raised)
- `data/catalysts/2026-08-28/catalyst_events.jsonl` (500 events, regenerated this cycle via `catalyst-scan`), `narrative_baskets.jsonl` (2 baskets)
- `active-signals --asset-class crypto` (50 rows), `active-signals --asset-class stocks` (50 rows, all historical/closed)
- `signal-stats --asset-class crypto` (444 A/B sample, reliable), `signal-stats --asset-class stocks` (9 A/B anecdotal, 656 C-tier reliable)
- `detect_untracked_legacy_alerts --since 2026-08-28` (0 hits)
- `proposed_signals` direct query (ONG/USDT, 10 rows) and `news_items` direct query (ONG/USDT, 48h — 0 matches)
- 1 WebSearch (ONG/USDT price cross-check, 3 distinct exchange/aggregator sources, mutually conflicting) — external web research available this cycle.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_2338.md`

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-08-28 02:26:16 EEST — **fresh** (<3h old at review time 04:48).
- Latest cycle-summary file on disk: `cycle_02_18-25_summary.md` (prior day, mtime 2026-08-27 23:23:20 EEST) — **stale** (~5.4h old) considered alone, but the rule requires **both** to be stale to defer; scheduler.log is fresh, so **no defer**.
- Report-level freshness: scalp ~3.0h (fresh), intraday ~2.6h (fresh), swing ~13.0h (**borderline stale**, 12–14h band, flagged and used as the only swing source available), stocks-intraday ~7.3h (stale by the report's own clock, but stocks are closed overnight so this is expected carry-forward/planning context, not a gap).
- `data/catalysts/2026-08-28/` did not exist at run start; regenerated via the one allowed `catalyst-scan --no-print` CLI call (events=500, baskets=2, rejected_test=0, rejected_missing=0).
- No monitor/paper-portfolio status file was read this cycle (out of the allowed read set); not blocking.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-28 04:48 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"],
      "data_missing": ["today's catalyst folder was missing at run start (regenerated this cycle)", "swing report is a 13.0h carry-forward, borderline stale", "stocks swing/invest last generated 2026-07-02, ~8wk stale, excluded"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 02:26:16 EEST", "catalyst-scan re-run produced 500 events / 2 baskets", "swing report generated 15:46 EEST prior day"] },
    { "agent": "market_regime", "verdict": "ok", "confidence": 0.72,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scalp+intraday both label 'bullish trend (risk-on)' consistently tonight (no flip)", "BTC/ETH uptrend, altcoin breadth 75.0% above EMA20 / 83.3% above EMA50", "macro/geopolitical risk score 100/100 (Iran/Strait of Hormuz, Russia-Ukraine, Israel-Syria headlines) sitting under the bullish tape"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "narrative_supported"],
      "data_missing": ["ai_narrative basket's sample headlines are Israel-Syria conflict items, unrelated to AI/crypto — likely a keyword-collision/basket-building issue, see TODO"],
      "suggested_effect": "advisory_only",
      "facts_used": ["500 catalyst_events today (freshly regenerated), 115 mapped (23.0%), 385 unmapped (77.0%) — sampled unmapped headlines are macro/political (Japan forex, US postal rule, Philippine peso), consistent with prior nights' pattern", "2 narrative baskets today: perps_dex_narrative (primary HYPE/USDT, single_source whale-transfer headline only) and ai_narrative (primary NEAR/RENDER/TAO/FET, single_source, mismatched sample headlines)", "SOL/USDT carries an internally verified single-name catalyst (DeFi Development 'State of Solana' platform launch)"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.55,
      "reason_codes": ["oi_supports", "squeeze_risk", "data_unavailable"],
      "data_missing": ["MSTRB/USDT and several expansion-watchlist shorts lack derivatives confirmation"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ENA/SOL/TAO all show price-up+OI-up fresh positioning, crowding normal, funding not extreme", "FIL/ONT/ONG short candidates all explicitly flagged thin_liquidity_short_squeeze_risk / squeeze_risk_upper_wick in the expansion table"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["chase_risk", "clean_retest", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BMT/TRUMP-class movers explicitly rejected on the scalp/fast timeframe for being >2 ATR from EMA20", "SOL/TAO B-tier intraday ideas are defined pullback-only zones below current price, not market-buy plans", "all short-side candidates (FIL/SNXXB/SNDKB) are capped to C for fighting the bullish-trend regime — not a clean entry in either direction for shorts tonight"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 50 rows returned, mix of triggered/tp1_hit (managed, OPEN actionable) and waiting_for_entry (BMT, ENA, BEAMX, RE) — zero fresh B-tier this cycle", "stocks active-signals: 50 rows, all historical tp1_hit/tp2_hit/triggered with expires_at in the past — 0 live open, market closed overnight", "detect_untracked_legacy_alerts --since 2026-08-28: 0 hits — TODO-3 pattern not firing so far today"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["correlation_cluster", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto book 100% long, 0 shorts triggered (signal-stats direction table: direction=long n=444/444)", "correlated crypto_swing_narrative_rs_momentum cohort (TAO/RUNE/S/GIGGLE/etc.) shares one BTC-dump failure mode", "macro/geopolitical risk score 100/100 tonight (Iran/Strait of Hormuz, Israel-Syria, Russia-Ukraine wheat)", "ONG/USDT bias-tag contradiction now 4th consecutive cycle and worsening (-26% -> -43% internal vs. +28%/+160% external reads)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.72,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto mode=intraday PF 1.90 (best), mode=swing PF 1.78 (both working), mode=scalp PF 0.05 (kill-switch disabled, matches)", "crypto headline A/B: winrate 12.2% but PF 1.62 / avgR 0.144 (positive expectancy via R:R, low win-rate strategy)", "stocks C-tier: winrate 6%, PF 0.41 — correctly gated non-actionable; stocks A/B n=9 too small to trust (anecdotal)"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.63,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "TAO/USDT", "trigger": "already triggered/waiting across intraday+swing; manage existing entries, fresh adds only on a further pullback toward the stated invalidation zone, no chase at current print", "reason": "top RS-momentum score (89/100), price-up+OI-up derivatives confirmation, but no fresh verified catalyst — pure momentum long, part of the correlated cohort" },
    "best_short_candidate":    { "symbol": "SNXXB/USDT", "trigger": "confirm bearish HTF structure + derivatives data + a regime shift (BTC/ETH losing uptrend) before promotion out of C", "reason": "highest-scored short-side candidate tonight (80/100, RS -11.9% vs BTC) but explicitly capped to C for fighting the bullish-trend regime and thin-liquidity squeeze risk — not actionable, genuinely no clean short tonight" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "pullback fill into 108.10-108.89, invalidation 1h close beyond 107.14", "reason": "internally verified single-name catalyst (DeFi Development 'State of Solana' platform launch), canonical_news_event, defined pullback-only entry" },
    "avoid_candidate":         { "symbol": "ONG/USDT", "reason": "bias-tag contradiction now unresolved for a 4th consecutive review cycle and worsening (internal desk snapshot now -43.05% vs. three external sources all showing +28% to +160%, themselves mutually inconsistent) — needs a human with a live quote before any action either direction on the open triggered long (sig_8d3a8fd71bf0bf75, invalidation 0.09240)" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | ok | 0.72 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.55 | oi_supports, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.62 | chase_risk, clean_retest, entry_late | advisory_only |
| execution_lifecycle | ok | 0.75 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.68 | correlation_cluster, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.72 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | ok | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_2338.md` (23:38 EEST, post-close final daily review).

- **Unchanged:** No fresh A/B in crypto or stocks this cycle (same as 21:48/23:15). Crypto book still 100% long, 0 shorts. Correlated RS-momentum swing cohort (TAO/RUNE/S/CHIP/GIGGLE/etc.) still open, unchanged thesis.
- **Worse:** The **ONG/USDT bias-tag contradiction is now a 4th consecutive cycle unresolved** — the internal desk snapshot moved from -26.09% (23:15 review) to **-43.05%** (this cycle), while three independent external sources tonight all report ONG **up** 24h (CoinGecko +160% at $0.2479, CoinMarketCap $0.1148, Crypto.com +28% at $0.0960) — themselves mutually inconsistent, but uniformly contradicting the internal short-bias direction. Escalated from "high" to the top integrity item this cycle.
- **Resolved/improved:** `detect_untracked_legacy_alerts --since 2026-08-28` returned **0 hits** tonight, versus 7 hits the prior day (EDEN, SOL×3, S, BICO, ONT) — TODO-3 is not firing so far today. Not closing the TODO (one quiet day isn't proof of a fix) but noting the improvement.
- **New this cycle:** GOOGLB/USDT (the prior review's best short-watch) does not appear anywhere in tonight's scalp/intraday/swing reports — it was carried from stale context and is dropped. Tonight's short-side field (FIL/SNXXB/SNDKB) is fresher but every single one is explicitly capped to C for "fighting a bullish tape" plus squeeze/thin-liquidity risk — a more structurally honest "no clean short" than a stale carry-forward name.
- **New TODO:** The `ai_narrative` narrative basket's `catalyst_summary` sample headlines are Israel-Syria conflict items — unrelated to AI/crypto narrative. Likely a keyword-collision or basket-building bug (see §14).

## 5. Catalyst Coverage

- Total `catalyst_events` today (freshly regenerated this cycle): **500**. Mapped (non-null symbol): **115 (23.0%)**. Unmapped: **385 (77.0%)**.
- `narrative_baskets` today: **2** (perps_dex_narrative — primary HYPE/USDT; ai_narrative — primary NEAR/RENDER/TAO/FET).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sampled): "Japan should not raid its forex reserves for Takaichi's food tax cut" (macro/political); "Judge blocks key parts of Trump-backed rule restricting mail-in voting" (US politics, duplicated across sources); "Philippine peso falls to record low against USD" (macro FX) — legitimate macro-context items that don't map to a single symbol by design, consistent with the pattern flagged in prior reviews; not treated as a new pipeline regression.
- **Data-quality flag:** the `ai_narrative` basket's sample headlines (Israel-Syria conflict reporting) do not match its stated AI/crypto narrative — see TODO-ai-narrative-mismatch in §14.

## 6. Market Landscape

Crypto: BTC/ETH both in a clean uptrend tonight with no regime-label flip between scalp and intraday (both read "bullish trend (risk-on)" consistently, unlike the inconsistency flagged in the prior night's TODO). Altcoin breadth is strong (75.0% above EMA20, 83.3% above EMA50). Underneath the constructive tape, macro/geopolitical risk sits at 100/100 — Iran/Strait-of-Hormuz tension, Russia-Ukraine wheat-export disruption, and Israel-Syria strike headlines are all live risk-off inputs a pure price read would miss. The desk's own scalp mode is kill-switch-disabled for the Asia dead-zone window (00:00–06:00 UTC), consistent with the documented guard; intraday and swing remain live. Every short-side candidate tonight is explicitly capped to C for fighting the bullish regime plus thin-liquidity/squeeze risk (FIL, SNXXB, SNDKB, ONT) — this is a real, structurally-honest "no clean short" rather than a forced no-trade call.

Stocks: market closed overnight (US session). All 50 rows in `active-signals --asset-class stocks` are historical (`tp1_hit`/`tp2_hit`/`triggered` with `expires_at` in the past) — nothing live to manage or chase pre-market. Stocks swing/invest reports remain ~8 weeks stale (2026-07-02) and are excluded, cross-referenced not re-raised (known-deprecated pipeline per project memory). Weekly stocks signal-stats: C-tier (the bulk of raw candidates) shows winrate 6% / PF 0.41 — the actionability gates correctly keeping these out of A/B; financials remains the strongest sector by realized edge (PF 2.67) versus the broader mixed/negative sector picture.

### Market Mood / Risk Routing
- Crypto mood: **risk-on (price/technical), risk-off macro overlay** — routed as mixed-but-longs-preferred
- Stocks mood: **closed** (overnight; last session data is historical context only)
- Dominant narrative: crypto RS-momentum swing cohort (TAO/RUNE/S/CHIP/GIGGLE/etc.); AI narrative basket (NEAR/RENDER/TAO/FET, but evidence quality weak — see §5); perps_dex narrative (HYPE, single whale-transfer headline only)
- Preferred side now: **longs (pullback-only, manage existing)** / stocks **wait-for-trigger (session closed)**
- Best long candidate: TAO/USDT — manage existing triggered/waiting entries, no chase at current print
- Best short candidate: none clean — best short-watch is SNXXB/USDT, trigger: confirm bearish HTF structure + derivatives + a regime shift before promotion out of C
- Best catalyst-backed candidate: SOL/USDT — pullback fill into 108.10-108.89, invalidation 107.14
- What to avoid: ONG/USDT (bias-tag contradiction, 4th consecutive cycle, needs operator review); fresh entries on BMT/TRUMP-class movers at current extended scalp-timeframe prices; any short at market tonight (all capped to C, fighting the regime)
- What would change the view: BTC losing local support (invalidates the long-only correlated swing cohort per the playbook's own known-failure-mode); a resolved/verified ONG live-price check; a short candidate clearing the "fighting the regime" cap with an actual BTC/ETH trend break; catalyst mapping recovering toward symbol-specific coverage

## 7. Candidate Deep Dives

### 1. ONG/USDT — NEEDS REVIEW / AVOID (top priority, escalated)
- Open swing long `sig_8d3a8fd71bf0bf75`, triggered 2026-08-26T02:59:24, entry 0.09561-0.09824, invalidation 0.09240, score 73.9 — still status=`triggered` per direct `proposed_signals` query, i.e. still open tonight.
- Current desk snapshot (intraday report, 02:14 EEST) tags ONG/USDT as the single **weakest** symbol tonight: bias=short, 24h **-43.05%**, RS vs BTC -45.03% — worse than the -26.09% cited two cycles ago.
- `news_items` check: **0 matches** for ONG/USDT in the last 48h — no internal catalyst explains a move in either direction.
- External WebSearch (this cycle) returned three distinct reads, all showing ONG **up**, not down, and mutually inconsistent with each other: CoinGecko $0.2479 (+160% 24h), CoinMarketCap $0.1148 (no % given), Crypto.com $0.0960 (+28.03% 24h). The Crypto.com print ($0.0960) sits essentially at the open long's invalidation level (0.09240) — if that read is accurate, the position may still be technically valid, not stopped; if the internal -43% read is accurate, it should already be well past invalidation. **These cannot both be true.** Classified `single_source` each, treated as directionally suggestive (all three disagree with the internal short-bias tag) but individually unverifiable for an exact price.
- Has price already reacted to a catalyst? No catalyst exists internally or externally to react to — this looks like a data/tagging problem, not a news-driven move.
- Is this candidate aligned with market mood? N/A — this is a data-integrity item, not a trade thesis.
- Actionable now or after confirmation? Neither direction is actionable until a human confirms the live price against 0.09240.
- What would invalidate/resolve this: a single trusted live quote (exchange order book, not aggregator scrape) settling whether ONG is up or down over the last 24h.
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** — do not add to the open long, do not open a fresh short, until an operator confirms current live price against 0.09240.

### 2. TAO/USDT — LONG (best long candidate, manage-only)
- Score 89.0/100 momentum (intraday), 67.5-69.1 across active swing/intraday B-tier signals; already `triggered`/`waiting_for_entry` across both timeframes — not a fresh idea tonight, a managed position.
- Has price already reacted? Yes — 24h +9.22%, 7d +18.39%, RS vs BTC +7.23%.
- Chasing? At the current print, yes for a fresh add; the existing triggered signals were entered earlier in the move.
- Retest/pullback structure? The intraday B-tier plan is pullback-only, not a market-buy.
- Catalyst: **no fresh verified catalyst detected** (explicitly noted in the intraday report) — this is a pure RS-momentum long, and it sits inside the `ai_narrative` basket only via a source-quality-weak, mismatched-evidence classification (see §5 data-quality flag) — do not treat the basket membership as catalyst confirmation.
- Mood alignment: aligned with the risk-on price leg; part of the correlated RS-momentum cohort, so exposed to the playbook's own documented BTC-dump failure mode.
- Chase-risk setup: yes on fresh adds at current price; no for managing the existing triggered positions to their stated invalidation.
- Actionable level for a fresh add: pullback into the stated intraday entry zone only; manage existing entries per their own invalidation levels.

### 3. SOL/USDT — LONG, catalyst-backed (best catalyst candidate)
- Score 70.5/100 (intraday), also actively `triggered` in the swing book. Fresh catalyst: "SOL treasury firm DeFi Development launches real-time 'State of Solana' intelligence platform" (The Block), canonical_news_event, importance 0.75.
- Price reaction: 24h +9.57%, 7d +25.22% — already moved; not chasing further at the current 109.24 print if the pullback zone fills.
- Retest structure: yes — pullback zone 108.10-108.89, invalidation 1h close beyond 107.14.
- Overextended: RR to TP1 stated at 1.84R, not flagged >2 ATR from EMA20 in this report.
- Catalyst confirmation: internally verified, single named source (The Block) — treat as confirmed but not overwhelming (importance 0.75, moderate).
- Counter-thesis (from report): the long fails if this is just a beta bounce inside a bullish-trend market and buyers do not defend the pullback zone; the move may be late relative to EMA20/ATR.
- Actionable level: 108.10-108.89 fill, invalidation 107.14.

### 4. SNXXB/USDT — SHORT-WATCH (best short candidate, not actionable)
- Discovery-expansion candidate, `crypto_failed_bounce_short` playbook, score 80/100 (highest short score tonight), RS vs BTC -11.9%, volume 0.2x (thin).
- Explicitly capped in the audit: "short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, no_derivatives_thin_short" and "crypto intraday short against bullish-trend regime (audit cap) — Short setup fights a bullish tape."
- Status: shadow/C-tier, in-top in the expansion table but not promoted.
- Trigger to promote: confirm bearish HTF structure + derivatives data + a genuine regime shift (BTC/ETH losing the current uptrend) — none of these conditions are met tonight.
- Not actionable — surfaced as the cleanest available short-side idea in an otherwise 100%-long book, with its real structural caveats stated plainly rather than presented as a clean setup.
- Runner-up: FIL/USDT (unusual_volume, 3.8x, weak_vs_market, score 70) carries the identical "fights a bullish tape" + squeeze-risk caps; SNDKB/USDT (score 73, RS -7.2%) likewise capped.

### 5. HYPE/USDT — CATALYST-WATCH, not yet scored
- Primary symbol of tonight's `perps_dex_narrative` basket, but the basket's only evidence is a single_source Telegram repost of two large whale-transfer alerts (~$37M each, FalconX-related) — no price/RS/volume data, and HYPE does not appear anywhere in the scored top-N candidate funnel or expansion watchlist tonight.
- Suggested playbook: `wait_pullback`, but there is no defined entry, invalidation, or target — this is a raw catalyst tag, not a trade idea.
- Not actionable — watch for HYPE to actually surface in the scored candidate funnel with a defined technical setup before treating this as more than a headline note.

## 8. Best Candidates Ranked

1. **ONG/USDT** — NEEDS REVIEW (top priority — bias-tag contradiction, 4th consecutive cycle, worsening).
2. **TAO/USDT** (long, manage-only) — top RS-momentum score, already open across timeframes, no chase at current price.
3. **SOL/USDT** (catalyst-watch, long) — verified single-name catalyst, pullback fill into 108.10-108.89.
4. **SNXXB/USDT** (short-watch, not actionable) — best available short in a 100%-long book, requires regime shift to promote.
5. **HYPE/USDT** (catalyst-watch, not yet scored) — perps_dex narrative primary, needs a real technical setup before it's more than a headline.

## 9. Avoid / No Trade (this decision window only)

- **ONG/USDT** — any new long or short action pending operator review of the bias contradiction and current live price vs. 0.09240 invalidation.
- **Fresh shorts at market tonight** — FIL/SNXXB/SNDKB/ONT are all explicitly audit-capped for fighting the bullish-trend regime plus squeeze/thin-liquidity risk; wait for a genuine regime shift before promoting any of them.
- **BMT/TRUMP-class movers** — rejected on the scalp/fast timeframe for being >2 ATR from EMA20; chase risk on fresh entries.
- **Crypto scalp mode** — kill-switch-disabled for the Asia dead-zone window; no new scalp entries regardless of setup quality until the guard lifts.
- Stocks broadly — market closed overnight; nothing to chase pre-market off tonight's (already historical) data.
- This is a decision-window verdict only — scanning, candidate generation, tracking, and the scheduler continue in all cases; nothing here recommends pausing any part of the system.

## 10. Main Risks

- **ONG/USDT bias-tag contradiction, unresolved and worsening across a 4th consecutive cycle** — now compounded by three mutually-inconsistent external price reads, all disagreeing with the internal short-bias tag's direction. The single most concrete integrity risk tonight.
- **Crypto book is 100% long, 0 shorts triggered** (signal-stats: direction=long n=444/444) — no short-side capacity is currently being exercised; every short candidate tonight is capped for fighting the regime, so this imbalance is structurally expected right now, not a bug, but still a real concentration risk if the regime reverses.
- **Correlated swing cohort risk** — TAO/RUNE/S/CHIP/GIGGLE/etc. all share the `crypto_swing_narrative_rs_momentum` playbook; its own documented failure mode is a BTC dump invalidating the whole basket at once.
- **Macro risk-off headwind (100/100) under a bullish crypto tape** — Iran/Strait-of-Hormuz tension, Russia-Ukraine wheat-export disruption, Israel-Syria strike headlines sitting underneath BTC/ETH uptrend and strong altcoin breadth.
- **Catalyst mapping weak (77.0% unmapped)** — mostly legitimate macro noise tonight, not a symbol-mapping regression, but the catalyst layer should not carry single-name decisions.
- **`ai_narrative` basket evidence mismatch** — the basket's cited sample headlines (Israel-Syria conflict news) do not relate to its AI/crypto narrative label; treat any basket-based catalyst claim for NEAR/RENDER/TAO/FET with reduced confidence until traced (see §14).
- **Stocks swing/invest pipeline** still has zero fresh reports since 2026-07-02 (~8 weeks) — persists unchanged, cross-referenced not re-raised as a new item.

## 11. Action Plan — next 4 hours (Asia session into Europe open)

- Flag ONG/USDT for operator review before Europe/US session start — a human with a live order-book quote should settle the -43% vs. +28%/+160% conflict and confirm the open triggered long's status against 0.09240.
- Manage the existing triggered/waiting swing-intraday cohort (TAO, SOL, RUNE, S, CHIP, GIGGLE, etc.) against their stated invalidations only; no new correlated adds given the playbook's own BTC-dump failure mode and tonight's elevated (100/100) macro risk score.
- Watch SOL/USDT for a fill into 108.10-108.89; catalyst confirmed but moderate importance, size accordingly.
- Track SNXXB/USDT (and FIL/SNDKB as runners-up) for a possible short promotion only if BTC/ETH actually break the current uptrend structure — do not force a short into today's regime.
- Watch for HYPE/USDT to surface in the scored candidate funnel with an actual technical setup before treating the perps_dex basket as more than a headline.
- Do not re-enable scalp manually — it is correctly kill-switch-disabled for the Asia dead-zone window; let the guard lift on schedule.
- Re-check the ONG resolution and the ai_narrative basket-evidence question at the next cycle (11:30 Europe / pre-US context review).

## 12. Final Verdict per Mode

- **Crypto scalp:** kill-switch-disabled (Asia dead-zone guard); weekly PF 0.05 (consistent with the guard being warranted) — scanner continues, no new entries regardless.
- **Crypto intraday:** no fresh A/B this cycle; strongest weekly performer by mode-level stats (PF 1.90) — manage existing triggered/waiting orders only, no chase.
- **Crypto swing:** RS-momentum cohort (PF 1.78 weekly) open and running; no fresh entries — pullback-only discipline, chase risk flagged for anything bought at market.
- **Stocks intraday:** market closed overnight; nothing pending from tonight's historical data into the next session.
- **Stocks swing:** stale (2026-07-02) — excluded, cross-referenced not re-raised.
- **Stocks invest:** stale (2026-07-02) — excluded, cross-referenced not re-raised.

## 13. Sources

- Internal: [scalp report](data/reports/scalp/2026-08-27_22-44_scalp_report.md), [intraday report](data/reports/intraday/2026-08-27_23-14_intraday_report.md), [swing report](data/reports/swing/2026-08-27_12-46_swing_report.md), [stocks intraday report](data/reports/stocks/intraday/2026-08-27_18-31_stocks_intraday_report.md)
- Internal: `data/catalysts/2026-08-28/catalyst_events.jsonl` (regenerated this cycle), `narrative_baskets.jsonl`, `catalyst_cycle_01-41.md`
- Internal: `active-signals`/`signal-stats` CLI output (2026-08-28 04:4x EEST), `detect_untracked_legacy_alerts --since 2026-08-28`
- Internal: `db/crypto_ai_desk.sqlite` direct queries — `proposed_signals` (ONG/USDT history, 10 rows), `news_items` (ONG/USDT, 48h window, 0 matches)
- External: [Ontology Gas (ONG) Price Today | CoinGecko](https://www.coingecko.com/en/coins/ontology-gas) — $0.2479, +160% 24h claimed; conflicts with other sources, see §7.1
- External: [Ontology Gas price today | CoinMarketCap](https://coinmarketcap.com/currencies/ontology-gas/) — $0.1148; conflicts with other sources, see §7.1
- External: [Ontology Gas (ONG) Price Today | Crypto.com](https://crypto.com/en/price/ontology-gas) — $0.0960, +28.03% 24h claimed; conflicts with other sources, see §7.1
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_2338.md`

## 14. Fix Requests / TODO

### TODO-ong-bias-contradiction (escalated further — 4th consecutive cycle, worsening)
- **issue:** ONG/USDT carries an open swing long (`sig_8d3a8fd71bf0bf75`, triggered 08-26, invalidation 0.09240) while the current desk snapshot tags ONG bias=short with 24h -43.05% — worse than the -26.09% cited two cycles ago. Three external sources tonight all show ONG up 24h (+28% to +160%), not down, and disagree with each other too.
- **evidence:** `proposed_signals` query (§7.1); intraday report §2 "Weakest Symbols" list; WebSearch cross-check (§13); matches recurring pattern in project memory (ZBT/ACE 2026-08-08; this symbol first flagged 2026-08-27 18:39).
- **suggested manual fix:** a human session with a live order-book price feed (not an aggregator scrape) should check ONG/USDT's actual current price against 0.09240 and either confirm the long is still valid or force-close/flag it. Separately, trace why the desk's own bias-tagging keeps drifting further from external reality on this symbol across four cycles instead of converging — this may indicate a stale or wrong price-source feed specifically for ONG, not just a one-off classification glitch.
- **priority:** high (escalate to critical if unresolved by the next cycle)
- **first observed (this symbol):** 2026-08-27 18:39 EEST; reconfirmed and worsened 2026-08-28 04:48 EEST (4th consecutive cycle).

### TODO-ai-narrative-basket-mismatch (new)
- **issue:** The `ai_narrative` narrative basket (primary NEAR/RENDER/TAO/FET, `related_beta_rotation` playbook) cites sample headlines about Israeli military strikes near Damascus, Syria — content with no relation to AI/crypto narrative. This looks like a keyword-collision or source-selection bug in the basket-building step.
- **evidence:** `data/catalysts/2026-08-28/narrative_baskets.jsonl`, `ai_narrative` record's `catalyst_summary` field.
- **suggested manual fix:** a human session should trace the narrative-basket builder's headline-selection logic for `ai_narrative` and check whether it's pulling from a shared/mismatched event pool rather than AI-tagged events specifically.
- **priority:** medium
- **first observed:** 2026-08-28 04:48 EEST

### TODO-untracked-alerts-quiet-day (monitor, not closed)
- **issue:** `detect_untracked_legacy_alerts --since 2026-08-28` returned 0 hits tonight, versus 7 hits the prior day (EDEN, SOL×3, S, BICO, ONT). This is an improvement but not proof the underlying TODO-3 (watchlist-alert/signal-reuse) bug is fixed — could simply be a quiet alert day.
- **evidence:** detector output this cycle vs. prior cycle's 7-hit count (see prior review §14).
- **suggested manual fix:** none yet — keep tracking daily hit counts; only downgrade/close TODO-3 in project memory after multiple consecutive quiet days across varied market conditions.
- **priority:** low (informational)
- **first observed:** 2026-08-28 04:48 EEST

### TODO-nvda-legal-tag-false-positive (carried forward, unresolved)
- **issue:** NVDA (stocks intraday) was demoted A→C in the prior cycle citing "active legal/headline risk (indictment)," but the underlying news item is a bullish M&A story (Nvidia agreeing to buy Hugging Face) with only a tangential "previously hacked" mention about Hugging Face itself. Not re-verified this cycle (stocks market closed, no fresh stocks-intraday report to check against).
- **evidence:** see prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_2338.md` §7.5 and §14.
- **suggested manual fix:** unchanged — a human session should check the legal-risk classifier's keyword/tag mapping for exploit_hack-tagged items referencing a third company.
- **priority:** medium
- **first observed:** 2026-08-27 23:38 EEST; carried forward, not re-verified this cycle.
