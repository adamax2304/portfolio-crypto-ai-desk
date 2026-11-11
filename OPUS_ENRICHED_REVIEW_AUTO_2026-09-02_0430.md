# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

**Advisory only / no auto-trade.** Slot: **crypto overnight / Asia review** (04:30 EEST, US stocks closed — crypto is the only live actionable class this window). The geopolitical risk-off backdrop flagged in the 23:30 post-close review has **not de-escalated**: internal Telegram feed at 01:27-01:33 EEST shows fresh sirens/hostile-aircraft warnings in Kfar Yuval (Israel) and explicit IDF-Hezbollah escalation language, with Brent still +2% at a six-week high ($96.58). BTC/ETH regime is **transition_down / chop** (breadth 47.9% above EMA20, 60-62% above EMA50) — not a fresh panic leg, but not a clean risk-on tape either. The crypto swing book is still **~96% long-biased (48 open positions, all long except one legacy short)** against this backdrop; no new stops overnight beyond last night's ENA/TWT. One fresh, clean setup stands out: **FIL/USDT** (waiting_for_entry, created 00:55 EEST, top-scored strongest symbol with volume-backed breakout tags). **PROM/USDT recurs as a bias-tag contradiction** (tagged bias=short at -11.68% 24h while carrying two open long positions) — same tracked systemic bug, not new. Catalyst mapping is weak this run (73.8% unmapped) and **NEAR/USDT's "AI narrative" catalyst tag is a verified false positive** (symbol detector matched the common word "near" in unrelated macro headlines, not NEAR Protocol news). The scheduler's `refresh obsidian dashboard` step **failed** this cycle (exit=-1, ~60s) — the same step that hung 6h05m on 2026-08-31; now failing fast instead, but still not completing. No code/scoring changes made; TODOs only.

## 2. Data Used

- Reports: intraday (2026-09-01_22-54, ~5h45m old), swing (2026-09-01_17-02, ~11h37m old, carry-forward), scalp (2026-08-30_13-18, **stale, >3 days** — scalp mode is intentionally disabled per prior review, historical stats only).
- Stocks intraday report (2026-09-01_23-33) — market closed, planning/watchlist context only.
- `active-signals --asset-class crypto` (50 rows, limit-capped) and `--asset-class stocks`.
- `signal-stats --asset-class crypto` and `--asset-class stocks`.
- `detect_untracked_legacy_alerts --since 2026-09-02` — clean, 0 anomalies.
- `catalyst-scan` run this cycle (today's folder was missing) — 500 events, 4 baskets.
- `db/crypto_ai_desk.sqlite`: `news_items` (symbol-targeted freshness checks), `proposed_signals` (status/lifecycle counts).
- Latest cycle summary: `data/scheduled_runs/2026-09-01_default_schedule/cycle_02_01-44_summary.md`.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-01_2330.md`.
- **External web research unavailable this run** (not invoked — internal Telegram feed already carried fresh, consistent (<4h) confirmation of the geopolitical driver, so external search was not required per the internal-first discipline; no candidate's verdict here depends on external-only verification).

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-09-02 02:45 EEST (~1h55m before this run) → **fresh**, no defer.
- Latest cycle: `cycle_02_01-44_summary.md`, started 01:44:43, finished 02:44:59 EEST. Steps: **ok=79, failed=1**.
- Failed step: **`refresh obsidian dashboard` (exit=-1, ~60s timeout)** — see §14 TODO-1; same step hung 6h05m on 2026-08-31.
- Monitors (watchlist, pending, MEXC canary, derivatives, fast Finnhub, stocks): all `[OK]`.
- Paper execution refreshed cleanly: scanned=4128, written=4128, resolved=3499, errors=0.
- Telegram outbox: due=0, sent=0, failed=0, dead=0 — no backlog.
- Minor: Reddit social sources (CryptoCurrency/Bitcoin/Ethereum) returning 403 Blocked — non-critical, does not block scoring.
- Swing report is ~11h37m old (4-12h band) → used as **carry-forward**, flagged.
- Scalp report >3 days old — scalp mode disabled per prior review; excluded from actionable verdicts, historical stats only.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-09-02 04:30 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["derivatives/OI/funding fields not in reports"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 1h55m", "obsidian dashboard step failed exit=-1", "scalp report >3d stale", "catalyst folder generated on-demand this run"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chop", "mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC trend transition_down", "ETH trend transition_down/range", "breadth 47.9% above EMA20, 60-62% above EMA50", "regime label range/chop (neutral)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "catalyst_contradicted", "narrative_supported"],
      "data_missing": ["symbol-level source for AUCTION/UNI momentum_breakout basket"],
      "suggested_effect": "advisory_only",
      "facts_used": ["500 events, 369 unmapped (73.8%)", "NEAR/USDT news_items match is generic macro text, not NEAR Protocol", "momentum_breakout basket has no matching catalyst_events rows for AUCTION or UNI"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.3,
      "reason_codes": ["data_unavailable"],
      "data_missing": ["funding rate", "open interest", "liquidation/crowding data"],
      "suggested_effect": "advisory_only",
      "facts_used": ["reports do not surface funding/OI fields this cycle"] },
    { "agent": "technical_entry", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["entry_fresh", "entry_late", "price_moved_away"],
      "data_missing": ["live tick price for ZK/USDT vs its 2-day-old entry band"],
      "suggested_effect": "advisory_only",
      "facts_used": ["FIL/USDT waiting_for_entry created 00:55 EEST, top strongest-symbol score 86.7, volume 2.77x with breakout tag", "AUCTION/TAO/NEAR entries already filled, chase risk if adding now", "PROM/USDT tagged weak_vs_market/short bias while long positions still open"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.8,
      "reason_codes": ["open_actionable", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["2 waiting_for_entry (FIL, ZK)", "48 triggered/tp1/tp2 open positions", "0 untracked legacy alerts"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["correlation_cluster", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["48 open positions, ~96% single-direction (long)", "geopolitical risk-off driver still live per internal feed 01:27-01:33 EEST", "PROM/USDT bias-tag contradiction recurrence"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["playbook_working", "low_sample"],
      "data_missing": ["fresh scalp-mode data (report >3d stale, mode disabled)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing PF 2.02 (n=66)", "intraday PF 1.53 (n=67)", "tier B triggered winrate 12% flagged low by system observation"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chop", "correlation_cluster", "mapping_weak"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate": { "symbol": "FIL/USDT", "trigger": "fill on close inside 0.75966-0.77007 with volume confirmation; invalidation 0.74693", "reason": "freshest signal (created 00:55 EEST), top-scored strongest symbol both reports, 2.77x volume with breakout+relative_strength tags" },
    "best_short_candidate": { "symbol": "PROM/USDT", "trigger": "confirmed breakdown + retest failure below the open longs' invalidation levels (~6.27 and ~4.17), not a chase of the current -11.68% print", "reason": "weakest symbol in tonight's intraday report, bias=short tag directly contradicts two still-open long positions on the same symbol" },
    "best_catalyst_candidate": { "symbol": "AUCTION/USDT", "trigger": "hold above the momentum_breakout basket's structure; re-verify catalyst layer next cycle before treating as news-backed", "reason": "primary symbol in a <1h fresh basket AND already a triggered swing long — best technical/basket alignment available, but the basket itself has no matching catalyst_events row (price-momentum-derived, not a verified news catalyst)" },
    "avoid_candidate": { "symbol": "NEAR/USDT", "reason": "AI-narrative catalyst tag is a verified false positive (symbol detector matched the word 'near' inside unrelated macro headlines) — the open long position should be tracked as technical-only, with no catalyst edge" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.60 | chop, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, catalyst_contradicted, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.30 | data_unavailable | advisory_only |
| technical_entry | ok | 0.65 | entry_fresh, entry_late, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.80 | open_actionable, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.70 | correlation_cluster, reduce_risk, manual_review | advisory_only |
| playbook_performance | ok | 0.60 | playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.60 | chop, correlation_cluster, mapping_weak | advisory_only |

## 4. What Changed vs Previous Review

vs `OPUS_ENRICHED_REVIEW_AUTO_2026-09-01_2330.md` (post-close, 23:30 EEST):

- **New:** FIL/USDT waiting_for_entry signal (created 00:55 EEST) — not present at 23:30.
- **Open book:** 48 open positions now vs 49 at 23:30 — one position resolved overnight (net -1), no new stops reported since ENA/TWT.
- **Geopolitics:** confirmed still escalating, not de-escalating — fresh sirens/Hezbollah headlines 01:27-01:33 EEST, Brent holding the six-week high.
- **Scheduler:** the gap flagged 2026-08-31/22:05 had not recurred as of 23:30; **this cycle a new, different failure appeared** — `refresh obsidian dashboard` step failed fast (exit=-1) rather than hanging. Same step, different failure mode — still unresolved.
- **Catalyst mapping:** 73.8% unmapped tonight vs 75.6% at 23:30 — materially unchanged, still weak.
- **Thesis status:** PROM/USDT bias contradiction persists (present at 23:30 context too); NEAR/USDT false-positive catalyst tag is a **newly verified** finding this run (not called out at 23:30).
- Stocks: no new stocks data this window (market closed); SHOP/XOM context from 23:30 carries forward unchanged, not re-verified this cycle (out of scope for the overnight crypto slot).

## 5. Catalyst Coverage

- Total catalyst_events today: **500**. Mapped (symbol present): **131 (26.2%)**. Unmapped: **369 (73.8%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (macro/rates, no symbol resolution attempted): BOJ's Takata on inflation risk alertness; BOJ's Takata on policy-exit evaluation; BOJ's Takata on neutral-rate positioning ahead of inflationary pressure.
- Narrative baskets: 4 — `ai_narrative` (NEAR/RENDER/TAO/FET, <1h, single_source — **NEAR match is a false positive**, see §7), `rwa_narrative` (ONDO/XLM, <6h, single_source), `perps_dex_narrative` (HYPE, <6h, single_source, wait_pullback), `momentum_breakout` (UNI/AUCTION, <1h, single_source, wait_pullback — no backing catalyst_events row for either symbol, i.e. price-momentum-derived label, not a news catalyst).

## 6. Market Landscape

BTC/ETH: transition_down / transition_down (intraday) and transition_down / range (swing carry-forward). Altcoin breadth: 47.9% above EMA20 (below half — near-term weak breadth), 60-62% above EMA50 (still constructive medium-term). System-labeled regime: **range/chop (neutral)**, recommended style "mean reversion or wait for clean breakouts." Strongest symbols (both reports): UNI, CHIP, SC, ONG, CRV, FIL — with FIL and CHIP carrying real volume confirmation (2.6-2.8x). Weakest: PROM, HEMI, GRAM, MORPHO, ZEN — all tagged bias=short. Geopolitical backdrop (Israel-Hezbollah escalation, Brent +2% at 6-week high) is a live risk-off pressure on broader risk assets, not yet reflected as a fresh crypto leg-down since the 19:19 UTC stop-outs.

### Market Mood / Risk Routing

- Crypto mood: **chop / mixed**, leaning cautious given the still-live geopolitical driver.
- Stocks mood: **closed** (04:30 slot) — carry-forward context only from the 23:30 review.
- Dominant narrative: AI (NEAR/RENDER/TAO/FET basket, but NEAR's news backing is a false positive — treat as technical-only); momentum_breakout (UNI/AUCTION, technical not news-backed).
- Preferred side now: **mixed / wait-for-trigger**, selective longs only on fresh clean setups (FIL), short-watch only after confirmed breakdown (PROM).
- Best long candidate: **FIL/USDT** — see §7.
- Best short candidate: **PROM/USDT** — see §7 (watch-for-breakdown, not a chase of the current print).
- Best catalyst-backed candidate: **AUCTION/USDT** — technical/basket alignment, catalyst label unverified.
- What to avoid: adding fresh long exposure on top of the existing 48-position, ~96%-long book while the geopolitical risk-off driver is still live; chasing NEAR/USDT on its (false) catalyst tag.
- What would change the view: a confirmed de-escalation headline (Iran/Israel/Hezbollah) or Brent giving back the +2% move would ease the risk-off pressure; a clean breadth recovery above 55-60% on EMA20 would flip the regime read toward risk-on.

## 7. Candidate Deep Dives

### FIL/USDT — long, B-tier swing, waiting_for_entry
- Entry band 0.75966-0.77007, invalidation 0.74693, created 00:55 EEST (~3h44m ago, fresh).
- Top-scored "strongest symbol" in both the 22:54 intraday (score 86.7) and 17:02 swing (score 90.3) reports; swing report also tags it 2.77x unusual volume with `relative_strength, volume_expansion, breakout` (also `overextended` — worth respecting, not chasing beyond the stated entry band).
- Has price already reacted? Yes, 24h +11.96%, RS vs BTC +13.69% — the move is underway, entry band anchors it to a defined pullback zone rather than the highs.
- Chase risk: moderate — `overextended` tag present; only actionable inside the stated entry band, not above it.
- Retest/pullback structure: yes, this is an entry-band (not breakout-chase) signal.
- Catalyst support: none found in news_items for FIL/USDT — pure technical/momentum setup.
- Mood alignment: acceptable as a single, clean, unchased long even in a mixed/chop tape; does not resolve the book's directional concentration issue.
- Invalidation: close below 0.74693.
- Actionable now, subject to price reaching the entry band; TradingView/manual chart check unavailable, judged from local OHLCV/score fields only.

### PROM/USDT — bias contradiction, B-tier swing, 2 open long positions
- Two open longs: entry 6.5825-6.8355 (invalidation 6.2733, expires 2026-09-06) and entry 4.2849-4.3805 (invalidation 4.1681, expires 2026-09-03).
- Tonight's 22:54 intraday report tags PROM/USDT **bias=short**, 24h **-11.68%**, RS vs BTC -9.94% — directly contradicting the still-open long theses.
- This is the same systemic bias-tag contradiction tracked since 2026-08-08 (ZBT/ACE) through 2026-08-31 (ONG/PROM/PUMP/BICO); PROM/USDT itself already appeared in that cluster. **Recurrence, not a new bug** — see §14 TODO-3.
- Has price already reacted? Yes, materially against the long theses (-11.68% 24h).
- Actionable short only after a **confirmed breakdown and failed retest** below the existing longs' invalidation levels (6.27 / 4.17) — chasing the current print is not recommended.
- Legal/headline risk: none found.
- Verdict: **manual review required** for the two open long positions given the direct bias contradiction; not a clean short entry yet either.

### AUCTION/USDT — catalyst-watch, B-tier swing, triggered
- Entry 3.6018-3.6712, invalidation 3.5170, triggered, expires 2026-09-06 14:37.
- Primary symbol in the `momentum_breakout` basket (freshness <1h, source_quality single_source) alongside UNI/USDT.
- Verification: no `catalyst_events.jsonl` row maps to AUCTION/USDT or UNI/USDT specifically, and no `news_items` row matches AUCTION/USDT in the last 24h — the basket's "catalyst_summary" text is built from generic macro headlines (Brent, Nvidia/Hugging Face, gold), not an AUCTION-specific event. Treat as **price-momentum alignment, not a verified news catalyst**.
- Has price already reacted? Position is already triggered — entry has passed; this is a hold/monitor item, not a fresh entry.
- Mood alignment: acceptable as an existing long to continue holding; do not treat the basket label as additional conviction beyond the original technical score.

### TAO/USDT — catalyst-watch (weak), B-tier swing, triggered
- Entry 236.3207-238.0371, invalidation 234.2229, triggered, expires 2026-09-03.
- Primary symbol in `ai_narrative` basket (<1h) alongside NEAR/RENDER/FET.
- Only matching news_items row: a Benzinga Movers "Bittensor (TAO) Price Prediction: 2025, 2026, 2030" piece from 14:13 EEST the prior day — a content-mill/evergreen article, not an event catalyst. `verification_status`: single_source, effectively unverifiable as a trading catalyst.
- Existing open long, hold/monitor only; no incremental catalyst conviction.

### NEAR/USDT — avoid (catalyst false positive), B-tier swing, triggered
- Entry 1.9430-1.9610, invalidation 1.9210, triggered, expires 2026-09-08.
- Listed as a primary symbol in the fresh (<1h) `ai_narrative` basket, which would normally support the open long thesis.
- **Verification failed:** the only news_items rows matching "NEAR/USDT" in the last 24h are t.me/marketfeed macro headlines ("...REACHING $96.58... HOVERING **NEAR** A SIX-WEEK HIGH", "NVIDIA IS SAID TO **NEAR** $14B DEAL...", "GOLD HOLDS **NEAR** $4,330...") — the symbol detector matched the common English word "near," not NEAR Protocol. No genuine NEAR-specific news found.
- Verdict: treat the open long as **technical-only**; the catalyst tag should not add conviction. Flagged to §14 as a mapping-quality issue (not a new bug class — consistent with the known ~17% symbol-match rate documented previously).

## 8. Best Candidates Ranked

1. **FIL/USDT (long-watch, B-tier)** — cleanest fresh setup this window; enter only inside the stated band, invalidation 0.74693.
2. **PROM/USDT (short-watch / manual review, B-tier)** — best short-side idea, but only after confirmed breakdown; the two open longs need manual review given the bias contradiction.
3. **AUCTION/USDT (catalyst-watch, held long, B-tier)** — best technical+basket alignment among open positions; hold, don't add on the catalyst label alone.
4. **TAO/USDT (catalyst-watch, weak, held long, B-tier)** — hold/monitor; catalyst backing is unverifiable (content-mill source only).
5. **NEAR/USDT (avoid new conviction, held long, B-tier)** — hold as technical-only; do not treat as catalyst-confirmed.

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and the scheduler continue regardless.

- **New crypto swing/intraday longs beyond FIL/USDT** — the book is already ~96% long (48 of ~50 tracked positions) against a still-live geopolitical risk-off driver; adding further undifferentiated long exposure is not recommended this window.
- **Chasing PROM/USDT short at the current print** — the move is already -11.68% on the day; wait for a confirmed breakdown/retest failure instead.
- **Treating NEAR/USDT or AUCTION/USDT/TAO/USDT catalyst tags as trade justification** — all three have unverified or false-positive catalyst backing this run; technical score only.
- **Scalp mode** — remains intentionally disabled per prior review; no action needed, not evaluated this run (report >3 days stale).
- Stocks — market closed; SHOP/XOM/INTU context from the 23:30 review carries forward unchanged and is not re-verified this cycle.

## 10. Main Risks

- **Directional concentration:** ~96% of the open book is long against a mixed/chop, geopolitically-pressured tape — a single BTC/ETH leg-down would hit correlated stops across the cluster (as already happened once tonight with ENA/TWT).
- **Bias-tag contradiction (PROM/USDT):** recurring, unresolved systemic issue creating a direct thesis conflict on open positions — see TODO-3.
- **Catalyst layer reliability:** 73.8% unmapped plus a confirmed false-positive symbol match (NEAR) reduces confidence in using catalyst tags as a decision input this run.
- **Scheduler step instability:** `refresh obsidian dashboard` failed this cycle after having hung for 6h05m previously — a currently non-blocking but recurring weak point.
- **Geopolitical escalation:** live Israel-Hezbollah tension and Brent at a 6-week high remain an active risk-off pressure into the Europe session.

## 11. Action Plan — next 4 hours

1. Monitor the existing 48-position book for stops/TPs; no proactive rebalancing (advisory only, no execution authority here).
2. Watch FIL/USDT for entry-band fill; do not chase above 0.77007.
3. Watch PROM/USDT for a confirmed breakdown/retest failure below 6.27 / 4.17 before treating it as short-actionable; flag both open longs for manual review given the bias contradiction.
4. Re-check the geopolitical headline flow before the 11:30 EU/pre-US review — a de-escalation or fresh escalation print will materially change the mood read.
5. No action needed on the `refresh obsidian dashboard` failure this run (see TODO-1) — human review only.

## 12. Final Verdict per Mode

- **Crypto swing:** no new entries beyond FIL/USDT (fresh, clean); passive hold on the existing long-heavy book; PROM/USDT longs flagged for manual review.
- **Crypto intraday:** wait_for_trigger — no fresh intraday-specific candidates surfaced this window.
- **Crypto scalp:** confirmed intentionally disabled — no action, not evaluated (report stale).
- **Stocks (all modes):** market closed; no action this slot — carry forward 23:30 context only.

## 13. Sources

- Internal: [scheduler cycle summary](data/scheduled_runs/2026-09-01_default_schedule/cycle_02_01-44_summary.md) (2026-09-02, run 01:44-02:45 EEST).
- Internal: t.me/marketfeed, 2026-09-02T01:32:59Z — Brent futures +2%, six-week high, $96.58/bbl.
- Internal: t.me/marketfeed, 2026-09-02T01:30:13Z — sirens/hostile-aircraft warning, Kfar Yuval, Israeli military.
- Internal: t.me/Middle_East_Spectator, 2026-09-02T01:26-01:27Z — IDF statement on Hezbollah projectile response.
- Internal: news_items table — NEAR/USDT, TAO/USDT, UNI/USDT symbol-match verification queries (this run).
- Internal: `data/catalysts/2026-09-02/catalyst_events.jsonl` and `narrative_baskets.jsonl` (generated this run via `catalyst-scan`).
- Prior review: [OPUS_ENRICHED_REVIEW_AUTO_2026-09-01_2330.md](OPUS_ENRICHED_REVIEW_AUTO_2026-09-01_2330.md).
- **External web research unavailable this run** (not invoked — internal sources were sufficiently fresh and consistent; see §2).

## 14. Fix Requests / TODO

### TODO-1: obsidian dashboard refresh step failing
- **issue:** `refresh obsidian dashboard` scheduler step failed (exit=-1, ~60s) in the 01:44-02:45 EEST cycle.
- **evidence:** `data/scheduled_runs/2026-09-01_default_schedule/cycle_02_01-44_summary.md`, line `### 79. [FAIL] refresh obsidian dashboard (exit=-1, 60.0s, attempts=1)`.
- **suggested manual fix:** investigate the obsidian dashboard refresh script for a stuck/timeout condition; this is the same step that hung 6h05m on 2026-08-31 (see prior TODO). Consider adding a hard per-step timeout with skip-and-continue if one isn't already in place, since this step has now failed twice in two different modes (long hang, then fast failure).
- **priority:** high
- **first observed (this failure mode):** 2026-09-02 02:45 EEST (prior hang: 2026-08-31 11:20-17:26 EEST).

### TODO-2: catalyst symbol-resolver false positive on common-word tickers
- **issue:** NEAR/USDT was matched into the `ai_narrative` catalyst basket via news_items rows that only contain the common English word "near" (e.g. "...six-week high", "NVIDIA IS SAID TO NEAR $14B DEAL...") — not NEAR Protocol-specific news. Catalyst mapping overall is also weak this run (73.8% unmapped, 369/500 events).
- **evidence:** `db/crypto_ai_desk.sqlite` `news_items` query for `detected_symbols_json LIKE '%NEAR/USDT%'` in the last 24h (this run); `data/catalysts/2026-09-02/catalyst_events.jsonl` mapped/unmapped counts.
- **suggested manual fix:** add a negative-keyword/word-boundary guard in the symbol resolver for tickers that collide with common English words (NEAR, ONE, CAKE, etc.); this is consistent with the ~17% symbol-match-quality figure already tracked in the news-layer hardening work.
- **priority:** medium
- **first observed:** 2026-09-02 04:30 EEST (this specific NEAR/USDT false positive); underlying mapping-weakness pattern tracked previously.

### TODO-3: bias-tag contradiction recurrence (PROM/USDT)
- **issue:** PROM/USDT tagged `bias=short` with 24h -11.68% in tonight's 22:54 intraday report while still carrying two open **long** swing positions (entries 6.5825-6.8355 and 4.2849-4.3805, both unresolved).
- **evidence:** `data/reports/intraday/2026-09-01_22-54_intraday_report.md` "Weakest Symbols" section; `active-signals --asset-class crypto` output (this run) showing both PROM/USDT long entries still `triggered`.
- **suggested manual fix:** this is a recurrence of the already-tracked systemic bias-tag contradiction bug (first observed 2026-08-08 on ZBT/ACE, recurred through 2026-08-31 on ONG/PROM/PUMP/BICO — PROM/USDT itself already in that cluster). Still unresolved; a human-driven session should investigate why the bias/direction tag can diverge from an open position's actual direction.
- **priority:** high
- **first observed (overall issue):** 2026-08-08; **this recurrence:** 2026-09-02 04:30 EEST.

### TODO-4: telegram-test notifier chokes on unescaped underscores
- **issue:** `python -m src.cli telegram-test -m "..."` returns `400 Client Error: Bad Request` whenever the message contains an odd number of literal underscores (e.g. the filename `OPUS_ENRICHED_REVIEW_LATEST.md`) — Telegram's default Markdown parse mode treats `_` as an italics delimiter, and an unmatched one breaks entity parsing for the whole message. Confirmed by bisection this run: escaping to `OPUS\_ENRICHED\_REVIEW\_LATEST.md` sends successfully.
- **evidence:** this run's telegram-test bisection (5 failed sends narrowed to the bare filename string; escaped variant succeeded).
- **suggested manual fix:** either switch the shared notifier to `parse_mode=None`/plain text for auto-generated messages that may contain arbitrary filenames/tickers, or have the enriched-review skill escape `_`, `*`, `` ` ``, `[`, `]` before composing the Telegram body. Low risk today (this run recovered via escaping) but will silently fail future auto-review sends if a message happens to contain an odd count of any Markdown special character.
- **priority:** medium
- **first observed:** 2026-09-02 04:30 EEST.
