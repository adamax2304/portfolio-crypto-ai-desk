# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:03 EEST

## 1. Executive Summary

**Slot: pre-US-open decision review. Advisory only — no auto-trade, no code/scoring changes.**
Pre-US hand-off completed on time (target 08:50 ET, actual fire 08:53 ET, Δ+3min). All 34 eligible stocks pre-open candidates reviewed; none qualified for a genuine SUPPORT promotion — internal catalyst records (`signal_catalyst_labels`) and external verification both show the headline "catalysts" behind this cycle's highest-scoring names (NFLX, SMCI) are ~2.5–3 months stale, already priced in. Macro geopolitical risk remains extreme (91.3/100, Iran-war uncertainty persisting) but stocks-side VIX is calm (16.28) and futures are flat — a real cross-asset divergence carried forward from the 11:30 cycle. Catalyst mapping is still weak (73.5% unmapped). Route the decision — every stock A/B needs RTH confirmation before entry; do not chase the pre-market print.

## 2. Data Used

- Pre-US-open candidate overlay: `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (generated 12:53:40 UTC) — 33 eligible + 1 more surfaced by the health check (34 total reviewed), 51 excluded (mostly `NO_ENTITY_RESOLVED_CATALYST`, some `LEGAL_RISK`/`EARNINGS_BLACKOUT`)
- Intraday crypto report: `data/reports/intraday/2026-09-08_11-29_intraday_report.md` (generated 14:28:43 EEST) — fresh (~1h34m)
- Swing crypto report: `data/reports/swing/2026-09-08_02-45_swing_report.md` (generated 05:45 EEST) — ~10h old, **carry-forward** (4–12h bucket)
- Stocks intraday report: `data/reports/stocks/intraday/2026-09-08_12-18_stocks_intraday_report.md` (generated 15:18 EEST) — fresh (~44min)
- Stocks swing/invest reports: last real content 2026-07-02 — deprecated/stale per prior audits, zero-weighted
- Scalp report: `data/reports/scalp/2026-08-30_13-18_scalp_report.md` — **9 days stale**, excluded, noted for §14
- Catalyst layer: `data/catalysts/2026-09-08/catalyst_events.jsonl` (2000 rows), `narrative_baskets.jsonl` (6 baskets), `catalyst_cycle_11-35.md` (latest)
- LLM packets: `data/processed/llm_analysis_packet.md` (11:31 EEST), `data/processed/llm_stocks_packet.md` (12:21 EEST) — both fresh, not deep-read this cycle (report files carried the needed detail)
- CLI: `active-signals` ×2, `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-09-08` (clean)
- Direct DB reads: `signal_catalyst_labels`, `news_items` (per-candidate freshness check), `proposed_signals` (lifecycle counts, GE duplicate check)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1139.md` (11:30 Europe/pre-US context cycle)
- **External web research performed** (internal catalyst records for the top pre-US candidates were present but low-quality/stale — see §G discipline):
  - [S&P 500 VIX Futures — Investing.com](https://www.investing.com/indices/us-spx-vix-futures)
  - [Micron Technology (MU) — CNBC quote](https://www.cnbc.com/quotes/MU)
  - [Supermicro Delivers NVIDIA Vera Rubin NVL4 Blueprint — HPCwire](https://www.hpcwire.com/off-the-wire/supermicro-delivers-nvidia-vera-rubin-nvl4-end-to-end-dcbbs-blueprint-with-native-fp64-performance-for-converged-hpc-and-ai-infrastructure/)
  - [Fox Corporation to Acquire Roku, Inc. — Fox Corporation press release](https://www.foxcorporation.com/news/corp-press-releases/2026/fox-corporation-to-acquire-roku-inc/)
  - [Netflix (NFLX) — Investing.com quote/history](https://www.investing.com/equities/netflix,-inc.-historical-data)
  - [Morgan Stanley (MS) stock holds steady — ad-hoc-news.de](https://www.ad-hoc-news.de/boerse/news/corporate-news/morgan-stanley-stock-holds-steady-as-investors-look-to-recent-earnings-and/70059082)

## 3. Scheduler / Data Freshness

- **Pre-US schedule check: target 08:50 ET, actual fire 08:53 ET (Δ+3min, within tolerance).**
- `scheduler.log`: mtime 12:42:53 UTC (15:42:53 EEST) — fresh (~20min old at time of this check). **Not deferred.**
- Latest cycle summary `cycle_05_14-13_summary.md`: mtime 12:42:51 UTC — same freshness, ~20min old.
- Intraday crypto report: ~1h34m old — fresh.
- Swing crypto report: ~10h17m old — carry-forward, flagged; BTC regime read (`transition_down`, intraday) supersedes any stale swing-report regime read.
- Stocks intraday report: ~44min old — fresh.
- Stocks swing/invest: 2+ months stale — deprecated, zero-weighted (consistent with prior audits).
- Scalp report: 9 days stale (2026-08-30) — excluded from this review; flagged in §14 as it is unusually stale relative to every other report class.
- Catalyst scan: current, no re-scan needed (`data/catalysts/2026-09-08/` present, last cycle file `catalyst_cycle_11-35.md`).
- **Pre-US-open overlay health:** `stocks-preus-review-health` → `PENDING_DEADLINE` / `structured_preus_review_not_yet_due`, eligible=34, reviewed=34, missing=0. This is expected/benign at 08:53 ET (deterministic decision window is 09:15 ET) — not a `REVIEW_MISSING`/`PARTIAL_REVIEW_MISSING` failure state. See §14 for a documentation note.
- My own 33-candidate INSUFFICIENT_DATA batch (ingested at 12:55 UTC) was correctly **ignored** by `stocks-preus-review-ingest` in favor of a `timely_deterministic_baseline_remains_authoritative` preserved review from 12:45:45 UTC (8 min earlier, same session) — the safety mechanism worked as designed; no double-write, no harm.
- `detect_untracked_legacy_alerts --since 2026-09-08`: clean, no untracked crypto alerts.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-09-08 16:03 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks swing/invest fresh data (deprecated since July)", "scalp report fresh data (9 days stale)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~20min old", "cycle_05 summary ~20min old", "swing crypto report ~10h17m old (carry-forward)", "stocks intraday ~44min old", "scalp report 9 days stale"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["mixed", "risk_off", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC transition_down, ETH range, altcoin breadth 75.0%/85.4% above EMA20/50", "macro/geopolitics risk 91.3/100, Iran-war uncertainty persists (Finnhub-corroborated), carried forward from 11:30's 92.5-94.6", "stocks futures flat: ES +0.03%, NQ +0.01% (Investing.com/Barchart)", "VIX 16.28 (calm-moderate) — notable divergence vs crypto-side macro-risk read", "today's crypto B-tier signals are 100% long direction, zero shorts triggered"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.48,
      "reason_codes": ["mapping_weak", "stale_catalyst", "no_catalyst", "catalyst_confirmed"],
      "data_missing": ["ABNB-specific news beyond generic listicle coverage"],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 2000 rows, 530 mapped (26.5%), 1470 unmapped (73.5%)", "signal_catalyst_labels: 32/33 pre-US candidates show catalyst_freshness='none'; NVDA (not in top-5) shows 22.4h-stale", "NFLX 'Roku loss to Fox' narrative verified stale: Fox-Roku deal announced 2026-06-15, ~3 months old", "SMCI 'Vera Rubin/ISC' catalyst verified stale: announced 2026-06-22, ~2.5 months old", "MS: potential lead-underwriter role on Anthropic IPO — plausible positive catalyst but exact publish date not confirmed", "MU: no catalyst found, pure momentum/technical (+256% YTD)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["oi_contradicts", "squeeze_risk", "data_unavailable"],
      "data_missing": ["stocks options/short-interest flow for MU/NFLX/SMCI/ABNB/MS (not checked this cycle)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ARB/USDT: price up + OI down 5.19% = short covering, weaker continuation quality (flipped from 11:30's OI-up read)", "SOPH/USDT: funding -0.02 (bybit/mexc), -0.01 (okx), crowding elevated", "INJ/DOT/WLD: price up + OI up, funding neutral, crowding normal"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "entry_late", "stale_before_entry", "overextended"],
      "data_missing": ["TradingView/manual chart check unavailable — no ATR/EMA20 extension verified beyond report fields"],
      "suggested_effect": "advisory_only",
      "facts_used": ["MU entry 1014.95/stop 998.65 (~1.6% stop distance) near 2026 highs after a +256% YTD run — high chase risk if bought at market", "NFLX entry 78.24/stop 79.06 (~1.05% stop distance) near 52-week low ($65.08-126.70 range) — tight stop, squeeze risk on any bounce", "all 5 top candidates show status stale_before_entry/missed_no_entry pre-open, but expires_at is 2026-09-09 01:48-05:50 UTC — still valid through today's RTH open, not genuinely expired"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.72,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "review_shadow"],
      "data_missing": ["explicit entered-unresolved vs no-entry split for 'expired' rows (none present this 36h window)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B last 36h: triggered(open actionable)=9, waiting_for_entry=2, entry_moved_away+stale_before_entry+missed_no_entry(no-entry/stale)=12, stopped(closed loss)=4, tp1/2/3_hit(closed win)=4", "stocks A/B last 36h: 0 rows — all demoted to C by market_closed_intraday_planning_only, consistent with pre-open gating, not a data gap", "pre-US overlay: 34/34 candidates reviewed (review_shadow), 0 promoted to a live A/B by this cycle's verdicts"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ORCL: legal_headline_risk (securities_fraud) + earnings tomorrow 2026-09-09 + do_not_chase_warning + market_closed — quadruple-gated, A-tier raw score 88 demoted to C", "TSLA: class_action legal flag, A->C", "AMZN: block_requires_operator_review, Miami 250-flight air-network fatal-crash investigation", "XOM (in the eligible-short list, not a top-5 pick): geopolitical_risk tag — 'war premium' framing directly conflicts with its own short thesis given oil at multi-week highs on the Iran conflict", "BTC: Coldcard-attacker fund movement via THORChain/CoinJoin, exploit_hack flag", "macro risk 91.3/100, externally corroborated (Iran war uncertainty, Finnhub)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto by-direction (n=799 reliable): long-direction bucket 12W/0L, PF inf, +21.1R; short-direction bucket 3W/4L, PF 1.8, +3.5R — longs materially outperforming shorts recently, consistent with today's 100%-long crypto signal mix", "crypto tier C triggered winrate 4% (n=642), tier B 5% (n=151) — both flagged low by the CLI's own observations despite positive aggregate PF (few large winners carrying many small losers)", "stocks tier B triggered winrate 19% low (n=233 reliable); weekend=Y signals underperform (winrate 11%, n=105) vs weekend=N"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.62,
    "preferred_side": "mixed",
    "best_long_candidate": { "symbol": "MU", "trigger": "RTH hold above the pre-market/entry level (1014.95) with confirming volume in the first 15-30min — do not buy the gap or the pre-market print blind; stop 998.65", "reason": "Strongest technical momentum of the pre-US list (+256% YTD, near highs), score 88.3 (highest of all 34 reviewed), but no fresh catalyst — this is a pure trend-continuation/chase-risk setup that needs RTH confirmation, not a catalyst play." },
    "best_short_candidate": { "symbol": "NFLX", "trigger": "RTH failed-bounce/breakdown confirmation near 78.24 — do not short the pre-market low blind given the tight ~1.05% stop and elevated squeeze risk on any broad-market bounce; stop 79.06", "reason": "Genuine, externally-verified fundamental weakness (down 17% YTD, near 52-week low, 'slowing growth and executive changes'), but the specific 'lost Roku to Fox' catalyst cited by generic media coverage is ~3 months stale and already priced in — treat as a sustained-weakness technical short, not an event-driven one." },
    "best_catalyst_candidate": { "symbol": "MS", "trigger": "RTH hold above 217.72 with financials-sector relative strength confirmation; stop 216.04", "reason": "Only pre-US candidate with a plausible fresh positive driver — potential lead-underwriter role on the Anthropic IPO plus sector-positive framing ('Top Financial Stocks for the Week', published today) — but the IPO-role headline's exact publish date could not be confirmed, so treat as supportive context, not a proven same-day catalyst. No legal/earnings risk found." },
    "avoid_candidate": { "symbol": "ORCL", "reason": "Quadruple-gated: A-tier raw score 88 but demoted to C for active legal/headline risk (securities_fraud) AND earnings tomorrow (2026-09-09, explicit do-not-chase warning) AND market-closed. Not actionable under any read this window." },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.68 | mixed, risk_off, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.48 | mapping_weak, stale_catalyst, no_catalyst, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.45 | oi_contradicts, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, entry_late, stale_before_entry, overextended | advisory_only |
| execution_lifecycle | needs_review | 0.72 | open_actionable, waiting_for_entry, no_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.68 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.62 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.62 | — | advisory_only |

## 4. What Changed vs Previous Review (11:30 Europe/pre-US context cycle)

- **Macro risk eased very slightly but remains extreme**: 92.5–94.6/100 → **91.3/100**. Still an active, externally-confirmed Iran-war-uncertainty risk-off headwind, not resolved.
- **BTC regime unchanged**: `transition_down` persists (intraday read). Altcoin breadth firmed slightly: 70.8–83.3% → **75.0%/85.4%** above EMA20/50.
- **ARB/USDT derivatives flipped**: 11:30 read was "OI up = fresh shorts pressing" (squeeze setup); this cycle shows **OI down 5.19% = short covering** — the fresh-short thesis from 11:30 did not confirm; treat ARB as lower-conviction now.
- **PENDLE/USDT long-watch (11:30 pick) has since triggered** (`sig_0031fe559ba3b3ad`, status `triggered`, entry 2.2054) — the pullback-fill plan played out; now an open-actionable position, not a fresh idea this cycle.
- **Catalyst mapping**: 74.5% → **73.5% unmapped** — essentially flat, still weak, still flagged (see carried-forward TODO in §14).
- **Stocks pre-US-open overlay ran for the first time this session** (this slot's dedicated hand-off): 34 candidates reviewed, 0 promoted — the 11:30 review only had the raw pre-gate list, not a reviewed one.
- **New external verification this cycle**: NFLX's and SMCI's headline catalysts (Roku/Fox loss, Vera Rubin/ISC blueprint) were both confirmed stale (~3 months, ~2.5 months respectively) — the 11:30 review did not have stocks-specific external verification since the market was further from open.
- **ORCL, TSLA, AMZN legal/headline flags**: unchanged, still active, still correctly gating those names.

## 5. Catalyst Coverage

- Total catalyst rows scanned today: **2000**.
- Symbol-mapped: **530 (26.5%)**. Unmapped: **1470 (73.5%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (Essentially flat vs 74.5% unmapped at 11:30; still part of the multi-cycle degradation trend — see §14.)
- Top unmapped headlines (macro/market-wide, no clean ticker): "Investigators recover black boxes from cargo plane crash in Miami" (Reuters); Japanese government bond yield moves (30Y -4.0bps to 3.980%, 5Y -2.0bps to 2.230%) — consistent with the 11:30 cycle's unmapped mix (macro/bond noise, not a pure resolver failure).
- Active narrative baskets: 6 (not individually re-verified this cycle — carried from the catalyst layer; L2/ARB remains the most active per the intraday report's narrative heatmap, heat 60.5/100, status rising).

### Pre-US Stocks Review Overlay
- candidates reviewed: 34 (0 SUPPORT / 0 NEUTRAL / 0 CAUTION / 0 BLOCK / 34 INSUFFICIENT_DATA-attempted, all superseded by a `timely_deterministic_baseline_remains_authoritative` preserved review from 12:45:45 UTC — see §3)
- session-cap-only C's now eligible for pre-open Paper lane: 0 promoted this cycle (baseline preservation kept whatever the 12:45 cycle assigned; my own review found no candidate with a genuinely fresh, entity-resolved catalyst)
- excluded by hard gate: 51 — 41 `NO_ENTITY_RESOLVED_CATALYST`, 8 `LEGAL_RISK` (UNH, INTU, BLK, HOOD, COST, TSLA, ORCL, plus one more), 3 `EARNINGS_BLACKOUT` (LLY, DELL, TSM) — list in `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`.

## 6. Market Landscape

### Market Mood / Risk Routing
- **Crypto mood:** mixed — risk-off macro overlay (91.3/100, Iran war persists) sitting on top of a still-constructive breadth internals (75.0%/85.4% above EMA20/50) and a 100%-long, 0%-short live B-tier signal mix today. A genuine two-speed tape, not a clean risk-off wipeout.
- **Stocks mood:** pre-market / calm-mixed. VIX 16.28, ES +0.03%, NQ +0.01% — no gap-risk signal from futures. 34 pre-US candidates split roughly evenly long(16)/short(17); no directional futures bias to route by, so per-name confirmation matters more than index-level mood today.
- **Dominant narrative:** crypto — L2/ARB (heat 60.5/100, rising); stocks — AI-infra/semis momentum (MU/SMCI/SMH all appear in today's long list) alongside a financials-sector positive tilt (MS, Anthropic-IPO-adjacent).
- **Preferred side now:** mixed / wait-for-RTH-confirmation on stocks; selective longs on crypto (matches the desk's own recent long-vs-short performance split).
- **Best long candidate:** MU — trigger: RTH hold above 1014.95 with volume; do not chase the gap.
- **Best short candidate:** NFLX — trigger: RTH failed-bounce/breakdown confirmation near 78.24; tight stop, squeeze risk.
- **Best catalyst-backed candidate:** MS — trigger: RTH hold above 217.72 with sector RS; Anthropic-IPO-role catalyst plausible but date-unconfirmed.
- **What to avoid:** ORCL (legal + earnings + market-closed triple/quadruple gate); XOM short (eligible-list short whose own "war premium" framing argues against the short thesis given the Iran-driven oil rally); no-catalyst crypto chases in chop.
- **What would change the view:** an Iran/Israel de-escalation headline (macro risk score drop), a confirmed RTH breakout/breakdown on any of the top-5 stocks with volume, or VIX moving to confirm (rather than diverge from) the crypto-side macro-risk read.

## 7. Candidate Deep Dives

### MU (long-watch, stocks — pre_gate tier A, current tier C/market-closed)
- Has price already reacted to a catalyst? No fresh catalyst found (internal `signal_catalyst_labels`: none; external search found no MU-specific news driver) — this is a pure multi-month momentum/technical trend (+256% YTD, trading near 2026 highs $962–1018).
- Chasing? Yes if bought at market pre-open — buying near all-time-high territory after a huge run is inherently chase-risk; needs RTH confirmation, not a blind entry.
- Retest/pullback structure? Not established in available data (chart tool unavailable).
- Overextended (>2 ATR from EMA20)? **TradingView/manual chart check unavailable** — cannot confirm; stop distance (entry 1014.95, stop 998.65, ~1.6%) suggests a specific technical level was used, not an arbitrary chase level.
- Would entry now be late? Yes at the pre-market print; wait for RTH + volume confirmation.
- Mood alignment: consistent with a broader AI-infra/semis momentum theme this cycle (SMCI and SMH also on today's long list) — flag as a correlation cluster, not three independent ideas.
- Long/short: long. Actionable only after RTH confirmation.
- Invalidation: 998.65.
- Chase risk: **high** — explicitly flag.
- Catalyst confirmation/contradiction: none; momentum-technical only.

### NFLX (short-watch, stocks — pre_gate tier A, current tier C/market-closed)
- Has price already reacted? Yes — down 17% YTD, trading near the low end of its 52-week range ($65.08–126.70), "slowing growth and executive changes" per market commentary (Investing.com, as of 2026-09-07 close).
- Chasing? A fresh short at the exact low print carries squeeze risk; the specific "lost Roku to Fox" narrative cited by generic financial-media coverage is verified **stale** (Fox-Roku deal announced 2026-06-15, ~3 months old, already priced in) — do not treat it as a fresh trigger.
- Retest structure? Not specified internally; recommend a failed-bounce/rejection confirmation near 78.24 rather than shorting the print.
- Overextended? Chart unavailable; price already sits near a 52-week low, which itself implies downside extension and elevated bounce/squeeze risk.
- Entry now: late at the pre-market level; RTH confirmation required.
- Mood alignment: consistent with a sustained-weakness fundamental narrative, not an event-driven one.
- Invalidation: 79.06 (tight, ~1.05% — flag as a tight-stop chase-risk setup).
- Catalyst confirmation/contradiction: no fresh catalyst; the cited driver is stale.

### MS (catalyst-watch / long, stocks — pre_gate tier A, current tier C/market-closed)
- Has price already reacted? Modestly — trading steady ($217.75 as of 2026-09-07), positively framed in today's "Top Financial Stocks for the Week" (Benzinga Movers, published 2026-09-08).
- Chasing? Low — "holds steady" language argues against an extended/chase setup relative to MU/SMCI.
- Retest structure? Not established; chart unavailable.
- Entry now: wait for RTH confirmation regardless (per slot rule).
- Mood alignment: financials sector positively framed today; potential lead-underwriter role on the Anthropic IPO is a plausible catalyst, but its exact publish date could not be confirmed this cycle — treat as supportive context, not a proven same-day trigger.
- Long/short: long. Actionable after RTH + sector-RS confirmation.
- Invalidation: 216.04.
- Legal/headline risk: **none found** — clean.

### SMCI (long-watch, stocks — pre_gate tier A, current tier C/market-closed)
- Has price already reacted? Yes, to a catalyst that is now **stale**: the NVIDIA Vera Rubin/ISC 2026 blueprint announcement was 2026-06-22, ~2.5 months old, fully priced into the prior surge.
- Chasing? Yes if bought blind — SMCI is a historically volatile, headline-sensitive name; today's setup is pure momentum continuation on old news.
- Mood alignment: part of the same AI-infra/semis cluster as MU/SMH — correlation risk if that theme reverses at the open.
- Entry now: late without RTH confirmation.
- Invalidation: 38.79.
- Legal/headline risk: none found in today's stocks-intraday legal-risk scan (clean this cycle).
- Catalyst confirmation/contradiction: stale catalyst only.

### ABNB (short-watch, stocks — pre_gate tier A, current tier C/market-closed)
- Has price already reacted? Unknown — external search returned no ABNB-specific news beyond generic listicle coverage ("Airbnb vs. Shopify", whale-alert roundups); no legal/SEC issue found (only routine Form 4 insider filings).
- Chasing? Cannot assess without a clearer internal or external driver.
- Entry now: wait RTH confirmation; treat as the **lowest-conviction** of the five given the absence of any visible catalyst or narrative explaining the score.
- Invalidation: 183.50.
- Catalyst confirmation/contradiction: **none found either way** — flag for manual review rather than a confident short thesis; the score (81.0, highest pre_gate tier A alongside MS) is not obviously explained by anything found this cycle.

## 8. Best Candidates Ranked

1. **MU (long-watch)** — strongest momentum, highest score (88.3) of all 34 reviewed; trigger: RTH hold above 1014.95 with volume. High chase risk — do not buy the gap.
2. **NFLX (short-watch)** — genuine sustained fundamental weakness, but cited catalyst is stale; trigger: RTH failed-bounce/breakdown near 78.24. Tight stop — squeeze risk.
3. **MS (catalyst-watch)** — only plausible fresh positive driver (Anthropic IPO role, unconfirmed date) + sector tailwind; trigger: RTH hold above 217.72 with financials RS.
4. **SMCI (long-watch)** — same AI-infra momentum cluster as MU; stale catalyst; trigger: RTH confirmation above 39.59, treat as correlated with MU, not independent.
5. **ABNB (short-watch, low-conviction)** — no catalyst or narrative found to explain the score; manual review recommended before treating as actionable even after RTH confirmation.

Crypto context (not double-counted against the ≤5 stocks slate): PENDLE/USDT's 11:30 long-watch has already triggered and is open-actionable; ARB/USDT's catalyst-watch thesis weakened (OI flipped to short-covering) — downgrade conviction versus the 11:30 read.

## 9. Avoid / No Trade

*(This decision window only — scanning, tracking, and the scheduler continue regardless.)*

- **ORCL** — securities_fraud legal flag + earnings tomorrow (2026-09-09) + market-closed. Quadruple-gated.
- **TSLA** — class_action legal flag, demoted A→C; avoid until resolved.
- **XOM (short, eligible-list)** — its own geopolitical_risk tag ("war premium") argues against the short thesis while Iran-driven oil strength persists; do not treat as a clean directional idea this window.
- **No-catalyst crypto chases in chop** — consistent with the desk's own documented net-negative no-catalyst intraday playbook.

## 10. Main Risks

- **Geopolitical escalation remains live** (Iran-war uncertainty, macro risk 91.3/100, externally corroborated) — the single largest tail risk into the US open.
- **Cross-asset divergence persists**: VIX calm (16.28) vs crypto-side macro-risk 91.3/100 — either equities have not priced the escalation, or crypto's macro-risk scoring overweights geopolitical headlines relative to realized volatility. Carried forward from 11:30, unresolved.
- **Both pre-US-open "catalyst" stories that showed up in generic media search (NFLX/Roku-Fox, SMCI/Vera Rubin) are stale by ~2.5–3 months** — a reminder that headline-level web search alone, without a publish-date check, would have mis-labeled these as fresh; this review verified dates before using either.
- **AI-infra/semis correlation cluster**: MU, SMCI, and SMH all sit on today's long list — a reversal in that theme at the open would hit all three together, not independently.
- **Catalyst mapping still weak** (73.5% unmapped) — treat the catalyst layer as context only, not as a scoring input to trust blindly.
- **Scalp report is 9 days stale** — if scalp mode is still intended to be live, this is a data-freshness gap; see §14.

## 11. Action Plan — Next 4 Hours

- At/after 09:30 ET (RTH open): require confirmation (hold above trigger + volume) before treating MU, SMCI, or MS as actionable longs — do not chase the pre-market print on any of them.
- At/after 09:30 ET: require a failed-bounce/breakdown confirmation before shorting NFLX; respect the tight 79.06 stop.
- Treat ABNB as manual-review-only pending a clearer driver; do not size it like MU/NFLX.
- Monitor the Iran/Israel headline flow through the open — the single most likely trigger to move both the macro-risk score and the VIX/crypto-risk divergence.
- Crypto: PENDLE/USDT is already open-actionable (triggered) — manage per existing stop; ARB/USDT's catalyst-watch conviction is now lower (OI flipped to short-covering) — do not add size on the old 11:30 thesis without re-confirming.
- No action needed on the scanner/scheduler/monitors — all continue unchanged.

## 12. Final Verdict per Mode

- **Stocks intraday (pre-US-open focus):** 34 candidates reviewed, all correctly capped at C by the market-closed gate; 5 stand out on score (MU, NFLX, SMCI, ABNB, MS) but **none** carry a genuinely fresh catalyst — route all five through mandatory RTH confirmation, not pre-market entry.
- **Stocks swing/invest:** Deprecated/stale — zero-weight this window.
- **Crypto intraday:** No fresh A/B this cycle beyond the carried-forward PENDLE trigger; C-tier watchlist only, no-catalyst names remain in the desk's documented bad playbook.
- **Crypto swing:** PENDLE/USDT open-actionable (triggered from 11:30's pullback plan); ARB/USDT downgraded from catalyst-watch to lower-conviction watch.
- **System-wide:** Scanning, tracking, and the scheduler continue uninterrupted — this is a decision-window caution, not a stop instruction.

## 13. Sources

- Internal: [reports/STOCKS_PREUS_REVIEW_CANDIDATES.md](reports/STOCKS_PREUS_REVIEW_CANDIDATES.md)
- Internal: [data/reports/intraday/2026-09-08_11-29_intraday_report.md](data/reports/intraday/2026-09-08_11-29_intraday_report.md)
- Internal: [data/reports/swing/2026-09-08_02-45_swing_report.md](data/reports/swing/2026-09-08_02-45_swing_report.md)
- Internal: [data/reports/stocks/intraday/2026-09-08_12-18_stocks_intraday_report.md](data/reports/stocks/intraday/2026-09-08_12-18_stocks_intraday_report.md)
- Internal: `signal_catalyst_labels`, `news_items`, `proposed_signals` (queried this cycle)
- External: [S&P 500 VIX Futures — Investing.com, accessed 2026-09-08](https://www.investing.com/indices/us-spx-vix-futures)
- External: [Micron Technology (MU) — CNBC quote, accessed 2026-09-08](https://www.cnbc.com/quotes/MU)
- External: [Supermicro Delivers NVIDIA Vera Rubin NVL4 Blueprint — HPCwire, 2026-06-22](https://www.hpcwire.com/off-the-wire/supermicro-delivers-nvidia-vera-rubin-nvl4-end-to-end-dcbbs-blueprint-with-native-fp64-performance-for-converged-hpc-and-ai-infrastructure/)
- External: [Fox Corporation to Acquire Roku, Inc. — Fox Corporation press release, 2026-06-15](https://www.foxcorporation.com/news/corp-press-releases/2026/fox-corporation-to-acquire-roku-inc/)
- External: [Netflix (NFLX) historical data — Investing.com, accessed 2026-09-08 (price as of 2026-09-07 close)](https://www.investing.com/equities/netflix,-inc.-historical-data)
- External: [Morgan Stanley stock holds steady — ad-hoc-news.de, accessed 2026-09-08](https://www.ad-hoc-news.de/boerse/news/corporate-news/morgan-stanley-stock-holds-steady-as-investors-look-to-recent-earnings-and/70059082)
- Previous review: [OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1139.md](OPUS_ENRICHED_REVIEW_AUTO_2026-09-08_1139.md)

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-trend (carried forward, updated)
- **issue:** Catalyst symbol-mapping rate remains weak across three consecutive cycles today: 68.2% unmapped (04:30) → 74.5% (11:30) → 73.5% (this cycle, 16:03). Essentially plateaued at a bad level rather than continuing to worsen.
- **evidence:** `data/catalysts/2026-09-08/catalyst_events.jsonl` this cycle: 2000 rows, 530 mapped (26.5%), 1470 unmapped (73.5%). Top unmapped headlines remain macro/bond/political items with no natural single-ticker mapping (Miami crash investigation, JGB yield moves), consistent with the 11:30 cycle's sample.
- **suggested manual fix:** unchanged from 11:30 — sample ~30 unmapped rows to classify genuinely-unmappable macro noise vs resolvable symbol misses.
- **priority:** medium
- **first observed:** 2026-09-08 04:30 EEST; still open at 16:03 EEST.

### TODO-stale-catalysts-in-generic-search
- **issue:** Generic web-search summarization surfaced two ~2.5–3-month-old news stories (NFLX/Roku-Fox loss, SMCI/Vera Rubin blueprint) framed in a way that reads as current/fresh unless the publish date is explicitly checked. This review caught it by fetching dates before use, but it is a systemic risk for any future review that trusts a search summary's framing without a date check.
- **evidence:** Fox-Roku deal press release dated 2026-06-15; SMCI HPCwire announcement dated 2026-06-22; both surfaced in a same-day 2026-09-08 web search as if potentially current.
- **suggested manual fix:** none needed for the routine itself (the existing §G discipline already requires a publish-date check) — flagging as a reminder/example for future reviews and for anyone auditing this cycle's sourcing.
- **priority:** low
- **first observed:** 2026-09-08 16:03 EEST.

### TODO-abnb-thin-thesis
- **issue:** ABNB scored 81.0 (pre_gate tier A, tied for second-highest of the 34 pre-US candidates) but no catalyst, narrative, or legal/headline driver was found internally or externally to explain the score — it may be a pure technical/momentum score with no qualitative story behind it, which is fine, but worth a human sanity-check on whether the technical inputs driving that score are sound.
- **evidence:** `signal_catalyst_labels` for `sig_59168732e6209969`: catalyst_freshness='none'. WebSearch for "Airbnb ABNB stock news September 2026 legal SEC" returned only routine Form 4 insider filings and generic listicle coverage.
- **suggested manual fix:** a human-driven session should pull the raw technical/scoring inputs for this specific ABNB signal and confirm the score is driven by a real technical setup (RS, volume, structure) rather than a data artifact.
- **priority:** low
- **first observed:** 2026-09-08 16:03 EEST.

### TODO-scalp-report-stale
- **issue:** The latest scalp report on disk is 9 days old (`2026-08-30_13-18_scalp_report.md`), in contrast to every other report class (intraday, stocks intraday, catalyst) refreshing within the last ~2h this cycle.
- **evidence:** `data/reports/scalp/` — no file newer than 2026-08-30 13:18 UTC as of this review (2026-09-08 16:03 EEST).
- **suggested manual fix:** a human-driven session should confirm whether scalp mode is intentionally paused/deprecated (similar to stocks swing/invest) or whether this is an unnoticed pipeline regression; if intentional, update the report-freshness expectations in this routine's §E to stop treating scalp as an expected-fresh source.
- **priority:** medium
- **first observed:** 2026-09-08 16:03 EEST.
