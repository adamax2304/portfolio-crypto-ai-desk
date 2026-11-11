# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:15 EEST

## 1. Executive Summary

**Slot: pre-US-open decision review (advisory only / no auto-trade).** Pre-US schedule check: target 09:00 ET, actual fire/start ~09:03-09:04 ET (Δ+3-4min, within tolerance), but the time-critical hand-off itself completed late relative to its own internal deadline — **`stocks-preus-review-health` reports `REVIEW_LATE`** (3/29 candidates recorded, 26 missing) — see §3 and §14 TODO-preus-late. Scheduler is fresh (new cycle 1/12 started 15:58 EEST, still running; `scheduler.log` <20 min old). Crypto: zero A-tier, zero fresh B-tier scalp/intraday setups this cycle; the one fresh actionable crypto idea is **HEI/USDT** (swing long, score 70.0, RS-leader + narrative-basket confirmed) — already extended, fill-only on pullback 0.1590-0.1620. Crypto book remains **100% long** (signal-stats: n=437, direction=long only) — no audited short exists. Stocks: market not yet open; **SNOW** (base_score 97.6, raw A) is the highest-scored stocks candidate but has **no fresh internal catalyst confirmation** (INSUFFICIENT_DATA on pre-US review) — treat as catalyst-watch, not a clean actionable at the open. **VRT long was BLOCKed** by this run's pre-US overlay for a fresh (2026-08-27T22:11 UTC) Pomerantz law-firm investor-investigation headline the code's hard gate had not caught — do not treat VRT as a clean long into the open. **PYPL short** has a genuinely fresh, material, entity-resolved catalyst (takeover-bid collapse, stock sinking) but was left NEUTRAL pending independent RS-vs-sector confirmation I could not complete in the time available. **ONG/USDT's bias-tag contradiction remains unresolved** (open swing long `sig_8d3a8fd71bf0bf75`, triggered 2026-08-26, still tagged bias=short −8.18% 24h this cycle) — continuing the escalated HIGH-priority TODO. Catalyst mapping is weak this run (74.3% unmapped). Scanning, tracking, and the scheduler continue regardless of this window's verdict.

## 2. Data Used

- Stocks pre-US candidates: `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (29 eligible / 57 excluded, generated 13:04:19 UTC)
- Pre-US review ingest: `data/raw/enriched_review_sources/preus_review_2026-08-28T1305Z.json` (29 verdicts submitted; 3 recorded OK/late, 26 IGNORED_LATE — see §3)
- Crypto scalp report: `data/reports/scalp/2026-08-28_11-40_scalp_report.md` (fresh, ~1h35m old)
- Crypto intraday report: `data/reports/intraday/2026-08-28_11-51_intraday_report.md` (fresh, ~1h24m old)
- Crypto swing report: `data/reports/swing/2026-08-28_07-59_swing_report.md` (carry-forward, ~5h16m old)
- Stocks intraday report: `data/reports/stocks/intraday/2026-08-28_06-42_stocks_intraday_report.md` (carry-forward, ~6h33m old, pre-market/market-closed at generation time)
- Stocks swing/invest reports: both dated 2026-07-02 (~57 days stale, deprecated pipeline — excluded, not re-raised)
- `data/catalysts/2026-08-28/catalyst_events.jsonl` (1500 events), `narrative_baskets.jsonl` (5 baskets)
- Direct read-only SQL against `news_items` (24h window, per-symbol) for all 29 pre-US eligible tickers, and against `proposed_signals` for ONG/USDT history
- CLI: `active-signals --asset-class crypto` (50 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-28`
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_1224.md`
- **External web research unavailable this run** (WebSearch/WebFetch not used — internal-first data was sufficient/consistent for every candidate reviewed within the time budget; RS-vs-sector confirmation for PYPL specifically could not be completed and is called out as a gap, not guessed).
- **TradingView / manual chart check unavailable** — all technical reads taken directly from report-stated OHLCV/ATR/EMA fields.

## 3. Scheduler / Data Freshness

- Pre-US schedule check: target 09:00 ET, actual fire ~09:03-09:04 ET (Δ+3-4min, within tolerance).
- **Pre-US hand-off timing:** candidates generated 13:04:19 UTC; my verdict JSON was ingested ~13:07-13:08 UTC (2-3 min after the pipeline's own internal review-deadline). `stocks-preus-review-health` → **`REVIEW_LATE`** (`reason: structured_preus_review_recorded_after_deadline`), reviewed_count=3, missing_count=26. Only VRT (BLOCK) and AVGO/SNOW were recorded (SNOW as INSUFFICIENT_DATA, late); the other 26 verdicts were `IGNORED_LATE_PRESERVED_TIMELY_REVIEW` against a preserved prior review timestamped 12:55:32 UTC. **No promotion should be assumed for the 26 missing candidates from this run's overlay** — see §14 TODO-preus-late.
- `scheduler.log`: 2026-08-28 15:59:44 EEST (~16 min old) — **fresh**, cycle 1/12 actively running (crypto scalp report step in progress at last log line read).
- No `cycle_*_summary.md` exists yet for today's newest cycle (still in progress); the most recent one is `2026-08-27_default_schedule/cycle_04_07-14_summary.md` (08:17 UTC, prior day) — not used as a freshness gate since `scheduler.log` itself is fresh and the defer rule requires BOTH stale.
- Crypto scalp: 11:40 UTC (~1h35m old) — **fresh**.
- Crypto intraday: 11:51 UTC (~1h24m old) — **fresh**.
- Crypto swing: 07:59 UTC (~5h16m old) — **carry-forward** (4-12h band); HEI/USDT idea below is carried from this report.
- Stocks intraday: 06:42 UTC (~6h33m old) — **carry-forward**; generated pre-market, before today's pre-US candidate refresh — used for regime/context only, not for fresh actionability claims.
- Stocks swing/invest: 2026-07-02 — **stale** (deprecated pipeline per prior audits, cross-referenced only, not re-raised as new).
- No monitor/paper-status file was read this run (not in the allowed CLI/read list); no claim made about it.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-28 16:15 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["26 of 29 pre-US candidates never received a timely structured verdict this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 15:59:44 EEST fresh, cycle 1/12 running", "scalp/intraday fresh (~1.5h)", "swing carry-forward (~5.3h)", "stocks intraday carry-forward (~6.5h, pre-market)", "stocks-preus-review-health=REVIEW_LATE, reviewed=3/29"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "longs_preferred", "chop"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: range/chop (neutral), BTC/ETH uptrend, breadth 43.8%/68.8% (scalp/intraday) vs 52.1%/79.2% (swing carry-forward)", "macro risk 100/100 risk-off overlay (Iran, Russia/Ukraine, oil)", "stocks: pre-open, no RTH confirmation yet"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["1500 catalyst_events, 385 mapped (25.7%), 1115 unmapped (74.3%)", "PYPL: fresh entity-resolved bearish catalyst (takeover bid collapse) confirms short thesis", "VRT: fresh Pomerantz investor-investigation headline contradicts long thesis (not caught by hard gate)", "GILD FDA approval + ANET price-target hike are genuine but RS-unconfirmed positives"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["most stocks candidates: no options/derivatives read this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HEI/USDT: price up + OI up, crowding normal", "MSTRB/USDT and several C-tier crypto names: futures data unavailable"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "entry_late", "stale_before_entry"], "data_missing": ["premarket RVOL/gap data for all 29 stocks candidates — not read this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HEI/USDT +19.9% 24h, pullback zone 0.1590-0.1620", "SNOW score 97.56 raw A but no fresh catalyst found internally", "all 29 stocks pre-US candidates still capped market_closed_intraday_planning_only pending RTH confirmation"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.65,
      "reason_codes": ["waiting_for_entry", "review_shadow", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 0 A-tier, 0 fresh B-tier scalp/intraday; 1 untracked legacy alert (MOVR/USDT) detected", "stocks: 0 A/B actionable intraday this cycle; SNOW/others demoted to C by market_closed_intraday_planning_only cap", "ONG/USDT swing long sig_8d3a8fd71bf0bf75 still triggered/unresolved since 2026-08-26"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["VRT: fresh investor-investigation headline → BLOCK this cycle", "ONG/USDT bias-tag contradiction unresolved, escalated HIGH per prior review", "1 untracked legacy crypto alert (MOVR/USDT) — known recurring TODO-3 pattern"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp: PF 0.10, avgR -0.083, totalR -9.0R (weekly) — losing bucket, active for data collection only", "crypto swing: PF 1.61 weekly — RS-momentum playbook working", "stocks C-tier: PF 0.36, totalR -7.0 weekly — watchlist quality, not actionable"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["wait_for_trigger", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["no clean A-tier actionable in either asset class this window", "HEI/USDT fill-only is the best crypto idea", "SNOW is the best catalyst-watch into the open but unconfirmed", "PYPL is the best short-watch but RS-unconfirmed", "VRT and ONG/USDT are the two active avoid/manual-review items"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "HEI/USDT", "trigger": "fill only on pullback into 0.1590-0.1620; no market buy at current 0.161x extension", "reason": "RS-leader + narrative-basket confirmed, best crypto score this cycle (70.0), but already +19.9% 24h" },
    "best_short_candidate":    { "symbol": "PYPL", "trigger": "wait for RTH confirmation of continued weakness below the pre-open reaction low + RS-vs-sector (XLF/financials) confirmation before treating as actionable", "reason": "fresh, entity-resolved, material bearish catalyst (takeover bid collapse) directly matching the short thesis; RS-vs-sector not independently confirmed this run" },
    "best_catalyst_candidate": { "symbol": "SNOW", "trigger": "clean reclaim of pre-market structure with RTH volume confirmation after the open; do not treat pre-market strength alone as confirmation", "reason": "highest raw score (97.6, A) of all pre-US candidates, capped only by market_closed_intraday_planning_only — but pre-US review found no fresh internal catalyst to confirm the thesis (INSUFFICIENT_DATA)" },
    "avoid_candidate":         { "symbol": "VRT", "reason": "fresh Pomerantz law-firm investor-investigation headline (2026-08-27T22:11 UTC) not caught by the code's hard gate — BLOCKed this cycle via the pre-US overlay" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.60 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | mixed, longs_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, entry_late, stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.65 | waiting_for_entry, review_shadow, no_entry | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | wait_for_trigger, manual_review | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_1224.md` (Europe / pre-US context, 11:30 EEST slot).

- **New this cycle:** the full pre-US-open stocks review overlay ran for the first time today (29 eligible candidates from `stocks-preus-candidates`), surfacing **VRT BLOCK** (fresh legal-investigation headline) and **PYPL** as a strong-but-unconfirmed short catalyst — neither was flagged in the 11:30 review.
- **Confirmed / unchanged:** ONG/USDT bias-tag contradiction remains unresolved (still triggered/open, still tagged bias=short) — now spanning into this cycle as well. Crypto book remains 100% long. SNOW remains the top-scored stocks candidate, still capped by `market_closed_intraday_planning_only`, now further confirmed as lacking a fresh internal catalyst (was assumed catalyst-clean at 11:30, now explicitly checked and found INSUFFICIENT_DATA).
- **Thesis changed:** HEI/USDT (crypto swing long) carries forward unchanged from the 11:30 review (same score 70.0, same fill zone) — no new information this cycle since the swing report itself has not refreshed (carry-forward).
- **New integrity issue this cycle:** the pre-US structured review itself ran late against its internal deadline (`REVIEW_LATE`, 3/29 recorded) — a new, distinct issue from the ONG/legal ones already tracked (see §14 TODO-preus-late).
- **Invalidated:** nothing from the 11:30 review was invalidated; CRM/CRWD earnings-calendar concern from that review is unchanged (not re-verified this cycle, still excluded from candidates by `EARNINGS_BLACKOUT`).

## 5. Catalyst Coverage

- Total `catalyst_events` today: **1500**
- Mapped (non-null symbol): **385** (25.7%)
- Unmapped (null symbol): **1115** (74.3%)
- `narrative_baskets`: **5**
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top 3 unmapped headlines:
  1. "JAPAN SHOULD NOT RAID ITS FOREX RESERVES FOR TAKAICHI'S FOOD TAX CUT..." (t.me/marketfeed)
  2. "JUDGE BLOCKS KEY PARTS OF TRUMP-BACKED RULE THAT WOULD RESTRICT MAIL-IN VOTING..." (t.me/marketfeed)
  3. "JUDGE BLOCKS U.S. POSTAL SERVICE FROM ENFORCING MAJOR TRUMP-BACKED RULE..." (t.me/marketfeed)
  (mostly macro/political noise, not a symbol-mapping regression)

### Pre-US Stocks Review Overlay

- candidates reviewed (verdicts submitted): 29 (NEUTRAL 24 / CAUTION 3 / BLOCK 1 / INSUFFICIENT_DATA 1)
- **actually recorded before the internal deadline (per `stocks-preus-review-health`): 3** — VRT (BLOCK, enforced), AVGO (late-recorded, adjustment clamped to 0), SNOW (INSUFFICIENT_DATA, late-recorded) — the other 26 verdicts were `IGNORED_LATE_PRESERVED_TIMELY_REVIEW` and did **not** change any score/tier this run.
- session-cap-only C's now eligible for pre-open Paper lane: **0** confirmed via this run's overlay (VRT was BLOCKed, not promoted; SNOW/AVGO late and not promotable as INSUFFICIENT_DATA/NEUTRAL)
- excluded by hard gate: 57 total — 33 `NO_ENTITY_RESOLVED_CATALYST`, 15 `EARNINGS_BLACKOUT`, 6 `LEGAL_RISK` (INTU, UNH, BLK, BAC, REGN, NVDA, SMCI — 7 actually, see candidates file) — full list in `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`

## 6. Market Landscape

Crypto regime (fresh scalp/intraday reads, 11:40-11:51 UTC): **range/chop (neutral)**, BTC/ETH both in an uptrend, altcoin breadth 43.75%/68.75% (above EMA20/EMA50) — softer breadth reading than the carry-forward swing report (52.1%/79.2%), consistent with intraday cooling. Macro/geopolitical risk 100/100 (Iran sanctions pushback, Russia/Ukraine escalation, oil-price divisions) — a persistent risk-off overlay on an otherwise constructive tape. Stocks: pre-open, no RTH data yet; VIX/regime context carried from the 06:42 UTC pre-market report (transition/neutral bias).

### Market Mood / Risk Routing

- Crypto mood: **mixed / chop** (uptrend structure, but breadth cooling and 0 fresh A/B setups this cycle)
- Stocks mood: **pre-market / closed** (no RTH confirmation yet; regime carried forward as transition/neutral)
- Dominant narrative: AI / RS-rotation baskets (ai_narrative, momentum_breakout) — crypto side; PayPal takeover-bid collapse and Vertiv legal-investigation headline are the two live single-name stock catalysts this cycle
- Preferred side now: **wait-for-trigger** (crypto: fill-only on pullback; stocks: wait for RTH confirmation)
- Best long candidate: HEI/USDT — fill only, 0.1590-0.1620
- Best short candidate: none clean yet — PYPL is the best short-watch, trigger: RTH confirmation of continued weakness + RS-vs-sector check
- Best catalyst-backed candidate: SNOW — catalyst-watch only, trigger: RTH volume-confirmed reclaim of pre-market structure
- What to avoid: VRT (fresh legal-investigation headline, BLOCKed), chasing HEI/USDT above the fill zone, any new crypto scalp entries (PF 0.10 this week), ONG/USDT (bias-tag contradiction unresolved, manual review pending)
- What would change the view: a fresher crypto swing report confirming HEI/USDT's RS leadership is intact into the pullback zone; RTH open confirming or rejecting SNOW's pre-market strength with volume; independent RS-vs-sector data on PYPL vs XLF

## 7. Candidate Deep Dives

### HEI/USDT (crypto, long, swing, B-tier score 70.0)
- Has price already reacted to the catalyst? No fresh verified catalyst — this is a pure RS-momentum/narrative-basket setup (score breakdown: technical_setup 16.9, momentum 9.6, narrative 5.5).
- Is the setup chasing? Yes at current price (+19.9% 24h, near the top of its own stated pullback zone 0.1590-0.1620).
- Retest/pullback structure? Yes — the playbook explicitly requires a pullback fill, not a market entry.
- Overextended (>2 ATR from EMA20)? Not explicitly flagged, but the 24h move is large; treat with chase-risk discipline.
- Would entry now be late? At market, yes. On a pullback fill, no.
- What level makes it actionable? Pullback into 0.1590-0.1620, invalidation on a 1h close beyond 0.1554.
- Aligned with market mood? Yes — RS-leader long in an uptrend-but-chop regime is the playbook's preferred cohort (14d WR 72% / PF 5.80 historically).
- Long, short, or wait-for-trigger? Long, fill-only (wait-for-trigger on the pullback).
- Actionable now or after confirmation? After a pullback fill only.
- What would invalidate it? 1h close beyond 0.1554, or BTC/ETH losing the current uptrend structure.
- Chase-risk setup? Yes at market price.
- Catalyst confirmation or contradiction? No catalyst either way — pure technical/RS setup.

### SNOW (stocks, long, intraday, raw A-tier 97.6 → C by session cap)
- Has price already reacted to the catalyst? No catalyst found — internal `news_items` search (24h window) returned zero rows for SNOW.
- Is the setup chasing? Cannot assess pre-open; no premarket/RVOL data read this run.
- Retest/pullback structure? Unknown pre-open.
- Overextended? Unknown pre-open.
- Would entry now be late? Market is closed — not applicable; the question is whether RTH confirms.
- What level makes it actionable? RTH volume-confirmed reclaim of the pre-market structure per the code's own SI-1..5 intraday gates (currently 0 A/B actionable this cycle for all stocks).
- Aligned with market mood? Unclear — no RTH data yet.
- Long, short, or wait-for-trigger? Wait-for-trigger.
- Actionable now or after confirmation? After RTH confirmation only.
- What would invalidate it? A gap-and-fade open with no volume follow-through, or a fresh negative catalyst before/at the open.
- Chase-risk setup? Cannot assess pre-open.
- Catalyst confirmation or contradiction? **Neither found** — genuinely missing data (INSUFFICIENT_DATA verdict), not treated as a positive signal.

### PYPL (stocks, short, intraday, C-tier raw score 62.1)
- Has price already reacted to the catalyst? Yes — internal news explicitly states "PayPal's stock sinks as suitors reportedly walk away from their takeover bid" (published 2026-08-28T11:10 UTC) and a related Seeking Alpha piece on PayPal-linked ETFs falling.
- Is the setup chasing? Possibly — the reaction may already be partly priced in pre-open; RTH confirmation needed.
- Retest/pullback structure? Unknown — no premarket level data read this run.
- Overextended? Unknown.
- Would entry now be late? Cannot say without RTH data.
- What level makes it actionable? RTH confirmation of continued weakness below the pre-open reaction low, plus RS-vs-financials/payments-sector confirmation (not independently verified this run).
- Aligned with market mood? Directionally yes (bearish, entity-specific, not macro-driven).
- Long, short, or wait-for-trigger? Short, wait-for-trigger (RTH + RS confirmation).
- Actionable now or after confirmation? After confirmation only — left NEUTRAL in the pre-US overlay because RS-vs-sector could not be independently verified in the time available, not because the catalyst is weak.
- What would invalidate it? A reversal/rescue-bid headline, or RTH price reclaiming pre-open levels.
- Chase-risk setup? Possible — flagged as a risk in the trigger condition.
- Catalyst confirmation or contradiction? **Confirmed** — fresh, entity-resolved, material, directly matches the short thesis.

### VRT (stocks, long, intraday, raw A-tier 80.5 → C by session cap, BLOCKed this cycle)
- Has price already reacted to the catalyst? Unknown pre-open, but the catalyst itself (a Pomerantz Law Firm investor-investigation notice, published 2026-08-27T22:11 UTC) is a headline-risk event, not a price-reaction confirmation.
- Is the setup chasing? Not assessed — irrelevant given the BLOCK.
- What level makes it actionable? None this cycle — BLOCKed via a short-TTL veto (expires 2026-08-28T17:07 UTC per the ingest command's own clamp).
- Aligned with market mood? N/A.
- Long, short, or wait-for-trigger? Avoid.
- Actionable now or after confirmation? No — legal/headline risk overrides the raw score regardless of technical setup.
- What would invalidate the BLOCK? Passage of the TTL window without further adverse developments, or explicit operator review clearing the concern.
- Catalyst confirmation or contradiction? **Contradicts** the long thesis — a fresh legal-risk headline the code's hard gate had not seen at candidate-selection time.

### ONG/USDT (crypto, open swing long, manual-review carryover)
- Status: `sig_8d3a8fd71bf0bf75`, triggered 2026-08-26, invalidation 0.09240 — still ENTERED UNRESOLVED.
- Current swing report (07:59 UTC carry-forward) still tags ONG/USDT bias=short, 24h -8.18%, RS vs BTC -8.87% — the same internal contradiction flagged in the prior 3+ reviews (escalated to HIGH priority 2026-08-08 per project history).
- Not re-verified externally this cycle (no WebSearch budget available given the pre-US hand-off time cost) — carried forward as an open, still-unresolved manual-review item, not re-escalated with new external data.

## 8. Best Candidates Ranked

1. **PYPL** (short-watch) — best catalyst-confirmed short-side idea this cycle; trigger: RTH confirmation of continued weakness + RS-vs-sector (XLF/payments) confirmation.
2. **HEI/USDT** (long, fill-only) — best crypto score this cycle (70.0), but already extended; trigger: pullback fill 0.1590-0.1620.
3. **SNOW** (catalyst-watch) — highest raw score of all pre-US candidates (97.6) but no internal catalyst found; trigger: RTH volume-confirmed reclaim of pre-market structure.
4. **VRT** (avoid) — fresh legal-investigation headline, BLOCKed this cycle; do not treat as a clean long regardless of its 80.5 raw score.
5. **ONG/USDT** (manual review, not a new entry candidate) — open unresolved long with a persistent bias-tag contradiction; no new action, existing invalidation (0.09240) stands.

## 9. Avoid / No Trade (this decision window only)

- **VRT** — BLOCKed this cycle for fresh legal/headline risk; do not treat as a clean long into the open regardless of its raw A-tier score.
- **Chasing HEI/USDT at market** — +19.9% 24h; fill-only discipline applies.
- **New crypto scalp entries** — weekly PF 0.10 (per signal-stats), net-negative bucket; scanner continues for data collection, no new entries recommended this window.
- **Any of the 26 stocks pre-US candidates whose verdict was `IGNORED_LATE_PRESERVED_TIMELY_REVIEW`** — treat their tier/score exactly as the code's own preserved prior review left them; do not assume this cycle's overlay promoted or blocked any of them.
- **ONG/USDT** — no new long or short action pending operator resolution of the bias-tag contradiction.
- This is a decision-window verdict only — scanning, candidate generation, tracking, and the scheduler continue in all cases; nothing here recommends pausing any part of the system.

## 10. Main Risks

- **Pre-US structured review ran late (`REVIEW_LATE`)** — only 3/29 candidates got a timely recorded verdict this cycle; the remaining 26 fell back to a preserved prior review rather than this cycle's fresh read. See §14 TODO-preus-late.
- **ONG/USDT bias-tag contradiction, still unresolved** — open triggered swing long tagged bias=short for multiple consecutive cycles now (escalated HIGH since 2026-08-08).
- **Crypto book remains 100% long, 0 shorts triggered** — structurally expected (no audited short candidate exists), but a real concentration risk if BTC breaks its current uptrend.
- **Crypto scalp underperformance continues** — weekly PF 0.10, avgR -0.083, totalR -9.0R.
- **Catalyst mapping weak (74.3% unmapped)** — mostly macro/political noise, not a symbol-mapping regression, but the catalyst layer should not carry single-name decisions this run.
- **1 untracked legacy crypto alert this cycle** (MOVR/USDT, sent 12:03 UTC, no matching `proposed_signal` within 6h) — consistent with the known recurring watchlist-alert/signal-reuse bug (prior TODO-3, escalated HIGH 2026-07-17).
- **RS-vs-sector confirmation gap on PYPL** — the strongest single-name catalyst this cycle could not be fully verified against sector context in the time available; treat as a genuine data gap, not a negative signal.

## 11. Action Plan — next 4 hours (into and through the US open)

- Watch PYPL for RTH confirmation of the takeover-collapse reaction; do not short pre-open or without RS-vs-XLF/payments-sector confirmation.
- Watch HEI/USDT for a pullback fill into 0.1590-0.1620; do not chase at the current extension.
- Watch SNOW for a clean, volume-confirmed reclaim of pre-market structure after the open; do not treat pre-market strength alone as confirmation, and do not assume the raw 97.6 score is actionable without that confirmation.
- Do not treat VRT as a clean long candidate this cycle regardless of its 80.5 raw score; revisit only after the BLOCK's TTL (2026-08-28T17:07 UTC) and any operator review.
- No new crypto scalp entries this window (weekly PF 0.10).
- Flag ONG/USDT for operator review of the bias-tag vs. live-price contradiction on the open swing long (invalidation 0.09240).
- Re-run (or have a human re-run promptly) the pre-US candidate ingest earlier in the window next time, to avoid another `REVIEW_LATE` result — see §14 TODO-preus-late.
- Re-check catalyst mapping %, ONG resolution, and the untracked-alert count at the next cycle (18:30 US open reaction review).

## 12. Final Verdict per Mode

- **Crypto scalp:** fresh data (~1.6h); weekly PF 0.10 (losing bucket) — scanner continues, no new entries this window.
- **Crypto intraday:** fresh data (~1.4h); 0 A/B setups this cycle — no action.
- **Crypto swing:** carry-forward (~5.3h); HEI/USDT is the one fresh actionable idea, fill-only.
- **Stocks intraday:** pre-open, 0 A/B actionable; SNOW is the cleanest catalyst-watch (unconfirmed), PYPL the cleanest short-watch (unconfirmed), VRT is BLOCKed.
- **Stocks swing:** stale (2026-07-02) — excluded, cross-referenced not re-raised.
- **Stocks invest:** stale (2026-07-02) — excluded, cross-referenced not re-raised.

## 13. Sources

- Internal `news_items` (read-only SQL, 24h window, per-symbol): PYPL takeover-bid-collapse coverage (MarketWatch Top Stories, Seeking Alpha Market Currents — both dated 2026-08-28), VRT Pomerantz investor-investigation notice (PR Newswire (Stocks), dated 2026-08-27T22:11 UTC), GILD Gilead HIV-pill FDA approval (Seeking Alpha Market Currents / CNBC Markets, dated 2026-08-27/28), ANET price-target increase (Finnhub company-news, dated 2026-08-28T06:08 UTC), CRCL price-target decrease (Finnhub company-news, dated 2026-08-28T10:30 UTC), TSM Moody's outlook raise (t.me/marketfeed / CryptoBriefing, dated 2026-08-28).
- Internal: `data/reports/scalp/2026-08-28_11-40_scalp_report.md`, `data/reports/intraday/2026-08-28_11-51_intraday_report.md`, `data/reports/swing/2026-08-28_07-59_swing_report.md`, `data/reports/stocks/intraday/2026-08-28_06-42_stocks_intraday_report.md`, `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`, `data/catalysts/2026-08-28/*`, `proposed_signals` / `news_items` (read-only SQL), `signal-stats` / `active-signals` CLI outputs, `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_1224.md`.
- No external WebSearch/WebFetch performed this run (date unavailable for none of the above — all internal timestamps present).

## 14. Fix Requests / TODO

### TODO-preus-late
- **issue:** The pre-US-open structured stocks review overlay ran late against its own internal deadline. Candidates were generated at 13:04:19 UTC; the verdict JSON was ingested ~13:07-13:08 UTC (2-3 min after the pipeline's deadline). `stocks-preus-review-health` returned `REVIEW_LATE` (`structured_preus_review_recorded_after_deadline`), with only 3/29 candidates recorded (26 fell back to a preserved prior review from 12:55:32 UTC).
- **evidence:** `python -m src.cli stocks-preus-review-health` output this run: `{"status": "REVIEW_LATE", "reviewed_count": 3, "missing_count": 26, ...}`.
- **suggested manual fix:** Either widen the internal review-submission deadline window relative to candidate-generation time, or have the hand-off step generate candidates earlier in the 09:00 ET cycle so a full 29-candidate structured review can complete before the deadline. A human should confirm whether the 12:55:32 UTC preserved review was itself a prior valid run for today or a stale artifact.
- **priority:** high
- **first observed:** 2026-08-28 13:08 EEST-equivalent (13:08 UTC)

### TODO-ong-bias-contradiction (recurring, already escalated)
- **issue:** ONG/USDT open swing long (`sig_8d3a8fd71bf0bf75`, triggered 2026-08-26, invalidation 0.09240) remains tagged bias=short (-8.18% 24h) in today's swing report — the same internal direction/bias-tag contradiction flagged and escalated to HIGH priority on 2026-08-08, still unresolved this cycle.
- **evidence:** `data/reports/swing/2026-08-28_07-59_swing_report.md` line 51 ("ONG/USDT: bias short, 24h -8.18%..."); `proposed_signals` row `sig_8d3a8fd71bf0bf75` status=triggered.
- **suggested manual fix:** Human review of the bias-tag computation vs. the open long's actual direction/invalidation; confirm whether the position should be closed given the sustained short bias tag.
- **priority:** high
- **first observed:** 2026-08-08 (recurring; not newly raised this run)

### TODO-untracked-alert-movr (recurring, already escalated)
- **issue:** 1 untracked legacy crypto alert this cycle — MOVR/USDT, B-tier intraday long, sent to Telegram 2026-08-28T12:03:32 UTC with no matching `proposed_signal` within 6h, so it will not contribute to PF/winrate/avgR tracking.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-28` output: 1 untracked alert (MOVR/USDT).
- **suggested manual fix:** Same root cause already tracked under the watchlist-alert/signal-reuse bug (escalated HIGH 2026-07-17) — a human session should confirm whether the fix for that bug has shipped; this is a fresh recurrence, not a new class of issue.
- **priority:** high
- **first observed:** 2026-07-17 (recurring; fresh instance this run)

### TODO-catalyst-mapping-weak (recurring)
- **issue:** Catalyst symbol-mapping coverage is 74.3% unmapped this run (385/1500 mapped), consistent with prior cycles' weak-mapping flags. Mostly macro/political noise, not obviously a regression, but persistent across many consecutive cycles.
- **evidence:** `data/catalysts/2026-08-28/catalyst_events.jsonl` — 1500 total events, 385 with non-empty `symbol`.
- **suggested manual fix:** Improve the symbol resolver in the catalyst layer for high-volume low-signal sources (e.g. `t.me/marketfeed`) if this pattern continues to dominate the unmapped bucket across many cycles.
- **priority:** medium
- **first observed:** recurring (not newly raised this run)
