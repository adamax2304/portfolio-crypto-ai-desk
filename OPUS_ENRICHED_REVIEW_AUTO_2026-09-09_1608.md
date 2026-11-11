# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:08 EEST

## 1. Executive Summary

**Advisory only — no auto-trade, no scoring/threshold/strategy changes.** Slot: **pre-US-open decision review** (target 08:50 America/New_York; actual fire ~08:54 ET, Δ+4min — within tolerance). The time-critical structured hand-off (`stocks-preus-candidates` → 37 verdicts → `stocks-preus-review-ingest` → `stocks-preus-review-health`) completed at **09:02 ET**, inside the 09:12 ET cutoff. Health check reports **PENDING_DEADLINE** (39/39 reviewed, 0 missing) — not yet READY/NO_ELIGIBLE because the 09:15 ET structured decision window has not yet been reached; this is expected, not an error. Crypto book remains **100% long** (50/50 active B-tier signals) against a still-live Iran/Israel geopolitical escalation and Brent crude above $100/bbl (risk-off macro overlay, 100/100) that has not yet broken the BTC/ETH technical uptrend — the same technical-vs-macro contradiction flagged in the 11:45 EEST review persists unresolved. Stocks regime is "transition/neutral," VIX 16.40 (calm), energy (XLE) the standout strong sector on the oil spike, semis showing modest positive RS vs SPY. A confirmed, concrete catalyst-mapping bug was found this cycle (UBER mis-tagged with a Rivian R2 headline) — see §14. Scheduler shows a broad DB-contention/timeout pattern today (9 failed steps in the latest cycle, plus this review's own `signal-stats --asset-class stocks` call timing out twice) — flagged, not fixed.

## 2. Data Used

- `data/reports/intraday/2026-09-09_11-05_intraday_report.md` (crypto intraday, generated 2026-09-09 14:04:55 EEST)
- `data/reports/swing/2026-09-09_04-12_swing_report.md` (crypto swing, generated ~07:11 EEST — borderline carry-forward, ~12h old)
- `data/reports/stocks/intraday/2026-09-09_12-23_stocks_intraday_report.md` (stocks intraday, data freshness 12:08 UTC / ~15:08 EEST)
- `data/processed/llm_analysis_packet.md` (generated 14:08 EEST), `data/processed/llm_stocks_packet.md` (generated 15:31 EEST)
- `data/catalysts/2026-09-09/catalyst_events.jsonl` (2000 rows scanned this cycle), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_11-14.md`
- Internal CLI: `active-signals` ×2 (crypto 50/50, stocks 50/50), `signal-stats --asset-class crypto` (completed on retry after an initial timeout), `signal-stats --asset-class stocks` (**timed out twice, unavailable this cycle**), `detect_untracked_legacy_alerts --since 2026-09-09` (0 untracked)
- `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` + this cycle's `data/raw/enriched_review_sources/preus_review_2026-09-09T12-58-36Z.json` (37 hand-off verdicts) + `stocks-preus-review-ingest` / `stocks-preus-review-health` output
- Direct `news_items` SQLite queries (internal-first, this session, ~12:54–13:00 UTC) for 36 pre-US candidate symbols + ZEC/Zcash follow-up
- `data/scheduled_runs/2026-09-08_default_schedule/scheduler.log` + `cycle_03_09-47_summary.md` (today's cycle, finished 11:42 EEST)
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-09_1145.md` (11:45 EEST, "Europe/pre-US context" slot) — used for §4
- No external WebSearch/WebFetch used this cycle — internal `news_items` coverage was recent, consistent, and sufficient for every candidate reviewed (internal-first discipline satisfied).

## 3. Scheduler / Data Freshness

- Pre-US schedule check: target 08:50 ET, actual fire ~08:54 ET (Δ+4min, within tolerance).
- `scheduler.log` mtime: 15:52 EEST (~10 min before this review started) — **fresh**.
- Latest `cycle_03_09-47_summary.md`: cycle started 09:47 EEST, finished 11:42 EEST (~4h20min before this review) — under the 3h defer threshold together with the fresh log, so **no defer**.
- **Cycle 3 today: ok=74, failed=9.** Eight of the nine failures are `(timeout)` at almost exactly 300s: `paper execution accounting refresh`, `paper structural TP refresh`, `paper entry-mode classify`, `paper stock direction (multi-factor)`, `entry latency audit (root cause)`, `paper-shadow A/B execution`, `paper portfolio ledger refresh`, `intelligence layer update`; the ninth, `refresh obsidian dashboard`, failed at 60s — this is the same step flagged as a 6h05m hang on 2026-08-31 per project history, now recurring as a fast (60s) failure instead, still unresolved. This review independently reproduced the pattern live: `python -m src.cli signal-stats --asset-class stocks` timed out twice (45s and 60s bounded attempts) during this run; `signal-stats --asset-class crypto` also timed out on first attempt but completed on a background retry (~3 min). At review time, `tasklist` showed 17+ concurrent `python.exe` processes, one holding ~3.7GB RSS — consistent with DB-lock/contention as the likely mechanism, not individually diagnosed further (out of scope — advisory only).
- Crypto intraday report: 11:05 EEST-tagged, `Data freshness: 2026-09-09 11:00:00+00:00` — **fresh** (<4h).
- Crypto swing report: 04:12 EEST-tagged (~11h56min old) — **borderline carry-forward** (4–12h bucket, near the upper edge); used with that caveat.
- Stocks intraday report: `Data freshness: 2026-09-09 12:08 UTC` (~15:08 EEST, ~1h old) — **fresh**; market session explicitly "after-hours (UTC overnight)" / MARKET CLOSED banner, consistent with pre-open.
- LLM packets: crypto 14:08 EEST (~2h old, fresh), stocks 15:31 EEST (~37min old, fresh).
- Stocks swing/invest reports: latest on disk from 2026-07-02 — **not a freshness issue**; per project history this position framework is deprecated/shadow-only and intentionally not refreshed.
- **Pre-US hand-off status:** `stocks-preus-review-health` reports `PENDING_DEADLINE`, eligible=39, reviewed=39, missing=0 — the small eligible-count drift from 37 (at candidate-generation time) to 39 (at health-check time, ~7 min later) reflects candidates generated/updated between the two calls; both handled by the code's own gate re-check, not by this review.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-09-09 16:08 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["signal-stats --asset-class stocks (timed out twice this run)", "fresh paper-execution/paper-shadow refresh (8 timeouts in latest cycle)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 15:52 EEST", "cycle_03 ok=74 failed=9, 8 timeouts at ~300s + obsidian dashboard fail at 60s", "17+ concurrent python.exe processes at review time"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 81-94% breadth vs macro geopolitical risk 100/100 risk-off — unresolved contradiction, persisting from 11:45 EEST review", "stocks: regime=transition/neutral, VIX 16.40, energy +8.54% RS vs SPY (oil-driven), consumer_discretionary -3.83% RS weakest"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.45,
      "reason_codes": ["mapping_weak", "catalyst_contradicted", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 2000 scanned, 1271 unmapped (63.5%) — exceeds 50% weak-mapping threshold", "confirmed mismap: 'UBER/USDT' catalyst entry is actually a Rivian R2 headline (importance 0.72)", "ZEC: institutional ETF-inflow thesis (Grayscale $500M) now countered by a fresh same-morning 'obvious pump and dump' quote (JAN3 CEO, 11:10 UTC)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.3,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["fresh funding/OI/liquidation query this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZEC 72% short-interest positioning (AMBCrypto, carried from prior review, not re-verified this cycle)"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["stale_before_entry", "entry_fresh", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active signals: 39/50 open (triggered/tp-hit), 11/50 waiting_for_entry", "BNB/USDT swing waiting_for_entry unchanged zone 759.24-761.96 for ~3.6+ days, catalyst basket unrefreshed", "ZEC/USDT swing waiting_for_entry, zone moved to 1198.18-1208.58 (from 1191-1199 at 11:45 review) — still unfilled"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry"],
      "data_missing": ["exact stocks entered-unresolved/no-entry split this cycle (paper-shadow/paper-execution refresh both timed out in cycle_03; not independently re-queried given the review time budget)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto armed watch (50): open_actionable=39 (33 triggered + 3 tp1_hit + 3 tp2_hit), waiting_for_entry=11", "stocks armed watch (50): open_actionable=49 (37 tp1_hit + 12 tp2_hit), waiting_for_entry=1", "untracked-legacy-alert detector: 0 (clean)"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Brent >$100/bbl on US-Iran escalation (multi-source, persisting from 04:45/11:45 reviews)", "BTC/USDT news_items row: 'US Treasury targeting Iran sanctions evasion through Bitcoin and USDT' tagged block_requires_operator_review — broad crypto regulatory headline risk, not tied to one active signal", "crypto book 100% long, zero shorts across all 50 active signals — no hedge available against a further risk-off leg"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["playbook_working", "low_sample"],
      "data_missing": ["stocks signal-stats this cycle (CLI timeout)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B headline: n=248, triggered=233, winrate 18.0%, PF 2.39, totalR +47.2 — positive expectancy despite low winrate (asymmetric R)", "observation: tier=B triggered winrate 18% flagged low by the CLI itself", "observation: weekend signals underperform (winrate 11%, n=105)"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.5,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "ANET (stocks, watch)", "trigger": "confirmed RTH open above pre-open level with volume; sector RS +1.75% tech / networking-AI catalyst fresh", "reason": "Fresh, entity-resolved $12.6B AI/campus/cloud networking growth catalyst (05:02 UTC), SUPPORT verdict in the pre-US overlay (clamped to 0 by the code pending live RS confirmation)" },
    "best_short_candidate":    { "symbol": "none clean in crypto (100% long book)", "trigger": "a confirmed break of the BTC/ETH uptrend structure would be the first crypto short-side opening", "reason": "In stocks: PLTR (short, base 77.1) was BLOCKed this cycle on fresh contradicting bullish narrative (+50% August rally framing) — avoid, not a short-watch" },
    "best_catalyst_candidate": { "symbol": "ABNB (stocks, short-watch)", "trigger": "RTH confirmation of weakness after the EU Commission's proposed Airbnb housing-crunch restrictions (fresh, 10:37 UTC)", "reason": "Fresh, entity-resolved, directionally-aligned regulatory headwind; SUPPORT verdict in the overlay" },
    "avoid_candidate":         { "symbol": "PLTR (stocks, short)", "reason": "BLOCKed this cycle — multiple fresh same-morning bullish articles (high-growth leadership screen, +50% August rally, bull-vs-Tesla framing) directly contradict the short setup" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.55 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.55 | mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.45 | mapping_weak, catalyst_contradicted, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.30 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | stale_before_entry, entry_fresh, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.60 | open_actionable, waiting_for_entry, no_entry | advisory_only |
| risk_manager | caution | 0.50 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.50 | — (see JSON) | advisory_only |

## 4. What Changed vs Previous Review (11:45 EEST)

- **Pre-US structured hand-off is new this cycle** (11:45 was a plain "Europe/pre-US context" slot, no hand-off): 37 candidates reviewed → 10 SUPPORT / 7 CAUTION / 1 BLOCK / 11 NEUTRAL / 8 INSUFFICIENT_DATA, all clamped to adjustment=0 by the code because `relative_strength_confirmed` was honestly reported `false` for every candidate (no live premarket RS-vs-sector feed was queried against the hand-off's tight 09:12 ET deadline) — this is the code's backstop working exactly as documented, not a bug.
- **ZEC/USDT long-watch**: still not filled — zone moved from 1191.25–1199.27 (11:45 review) to 1198.18–1208.58 now, invalidation 1185.47. Thesis gained a fresh **counter-narrative**: a same-morning "obvious pump and dump" quote (JAN3 CEO Samson Mow, 11:10 UTC) alongside continued institutional framing (Grayscale covered-call yield story, 12:20 UTC) — treat as **more contested**, not a clean confirmed long anymore.
- **DOT/UNI catalyst-backed swing positions**: still `triggered` (entered/unresolved), unchanged. DOT is **no longer listed** in the `momentum_breakout` basket this cycle (basket now: IOST/UNI/ATOM primary + AUCTION related) — UNI remains the only one explicitly catalyst-confirmed in the current basket text.
- **BNB/USDT**: still the stale avoid-carryover, unchanged zone, now ~3.6+ days aging (was ~3.4 days at 11:45).
- **Crypto book remains 100% long** (50/50) — unchanged all week, now confirmed again this cycle.
- **New this cycle**: a concrete, reproducible catalyst-mapping bug found (UBER/Rivian mismatch, see §14) — sharper evidence than the general 63.5%-unmapped statistic already known.
- **Stocks**: 37 pre-US candidates processed via the new hand-off (see §5); demoted-A/B list largely consistent with 11:45's list (LRCX, CLSK, TSM, AMD, QCOM, XLE longs; SBUX/ABNB/GILD/BKNG/MAR/SHOP shorts) with PLTR now also surfaced (and BLOCKed) via the wider 37-candidate pre-US scan that the plain 11:45 review didn't run.

## 5. Catalyst Coverage

- `catalyst_events.jsonl`: **2000 scanned, 729 mapped, 1271 unmapped (63.5%)**. **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top unmapped headlines: "South Korean stocks open higher, led by chip gains amid Middle East tensions"; "Defense minister... travel to Croatia"; "Gold slips; traders eye inflation data"; "Archer Aviation has lost over half its value..."; "Brent crude nears $100 a barrel as U.S.-Iran tit-for-tat strikes stoke supply worries."
- `narrative_baskets.jsonl`: **5 baskets** — rwa_narrative (ONDO, XLM), perps_dex_narrative (HYPE + DYDX/GMX/ASTER), ai_narrative (NEAR/RENDER/TAO/FET + WLD/ASTER), binance_ecosystem_teaser (BNB + ASTER), momentum_breakout (IOST/UNI/ATOM + AUCTION, UNI catalyst-confirmed).
- **Confirmed mapping-quality bug**: catalyst event tagged `UBER/USDT` [earnings_event] is actually a **Rivian R2** headline ("Rivian R2 Demand Tops Expectations as Autonomy and Robotaxi Plans Advance") — wrong entity entirely, importance 0.72. Also note stock tickers (XOM, UBER, COIN) appearing with a `/USDT` crypto-pair suffix in the top-catalysts list — a formatting/entity-class mixing artifact, not just a symbol mismatch. See §14.

### Pre-US Stocks Review Overlay
- candidates reviewed: 37 (SUPPORT 10 / NEUTRAL 11 / CAUTION 7 / BLOCK 1 / INSUFFICIENT_DATA 8)
- session-cap-only C's now eligible for pre-open Paper lane: 37 (all capped only by `market_closed_intraday_planning_only`, no substantive hard-gate reason)
- excluded by hard gate: 53 — 33× NO_ENTITY_RESOLVED_CATALYST, 12× LEGAL_RISK (incl. AMZN, UNH ×2, ORCL, WMT, TSLA, COST, REGN, INTU, BLK), 8× EARNINGS_BLACKOUT (incl. AVGO, APP, DELL, LLY, MSFT, CRM, NOW, VRT, BX)
- All 10 SUPPORT and the 1 BLOCK verdict were confirmed by the ingest code's own re-check (SUPPORTs clamped to adjustment=0 since `relative_strength_confirmed` was honestly reported false; BLOCK on PLTR applied a 3h TTL veto, `block_expires_at` 17:01:25 UTC).

## 6. Market Landscape

The Iran/Israel geopolitical picture and the Brent-above-$100 move that drove the 04:45 and 11:45 EEST reviews remain the dominant macro fact this cycle — no de-escalation or correction found in internal sources through this review's cutoff. What's new is on the equity side: the stocks intraday report's sector-rotation module now gives concrete relative-strength numbers that weren't queried at the 11:45 review — energy (XLE) is the standout strong sector (+8.54% RS vs SPY, +7.63% 20d, directly the oil trade), technology and semiconductors show smaller positive RS (+1.75% / +1.67%), while consumer discretionary (-3.83% RS) and industrials (-4.60% RS) are the weakest. This gives real substance to the "chip rally keeps Nasdaq from snapping" narrative repeated across this morning's news_items for MRVL/AMD/INTC/TSM/KLAC — a genuine, multiply-sourced sector story, not a single-headline read. On the crypto side, the technical-vs-macro contradiction flagged at 11:45 (BTC/ETH in confirmed uptrend, 81-94% breadth, vs. the same intraday report's own macro module scoring geopolitical risk 100/100 risk-off) persists unresolved this cycle — price action is still siding with the technical read. A second contradiction was found live this run in the catalyst layer itself: a `UBER/USDT`-tagged catalyst event is actually a Rivian headline, and the mapping layer is running 63.5% unmapped overall — catalyst context should be read as directional color, not confirmed fact, this cycle. ZEC/USDT's institutional-inflow long thesis picked up a fresh same-morning contrarian voice ("obvious pump and dump," JAN3 CEO) — the setup is now genuinely two-sided rather than a clean confirmed catalyst. The pre-US structured hand-off (§5 overlay) reviewed 37 session-cap-only C-tier candidates and found the market's dominant morning narrative (oil/Iran risk-off macro vs. a resilient, RS-positive semis basket) cutting across individual names too: multiple would-be shorts (XOM, DIS, VRTX, AMGN, COIN, PLTR) were downgraded to CAUTION or BLOCK on fresh contradicting bullish catalysts, while the semis basket (ANET, MRVL, INTC, AMD, TSM, KLAC) and the two broad-index shorts (SPY, DIA) carried the cleanest, most internally-consistent catalyst support — though none converted to a live SUPPORT adjustment this cycle because relative-strength-vs-sector wasn't independently re-verified inside the hand-off's tight window.

### Market Mood / Risk Routing
- Crypto mood: **mixed/divergent** — technical regime uptrend/risk-on (BTC/ETH both trending, 81-94% breadth) vs. macro overlay 100/100 risk-off inside the same report; unresolved for a second consecutive review.
- Stocks mood: **pre-market / transition-neutral** — VIX 16.40 (calm), energy strong on oil, semis mixed-positive RS, consumer discretionary and industrials weakest; no panic signature.
- Dominant narrative: still-live Iran/Israel escalation + Brent >$100/bbl, cutting across both books; secondary: the semis "chip rally" RS story now has concrete sector-rotation numbers behind it.
- Preferred side now: **catalyst-backed over fresh no-catalyst momentum chases** in crypto (ZEC is contested, not clean); in stocks, **sector-aligned longs (semis) and macro-aligned index shorts (SPY/DIA) over single-name shorts that fresh news is actively contradicting (XOM, DIS, VRTX, AMGN, COIN, PLTR)**.
- Best long candidate: **ANET** (stocks, watch — fresh AI/networking catalyst, positive tech/semis sector RS; requires RTH confirmation) / crypto: no clean fresh long this cycle — ZEC is now contested, ATOM/FF/SAHARA ride the documented-negative no-catalyst playbook.
- Best short candidate: **none clean in crypto** (100% long book, unchanged all week); in stocks, **SPY/DIA** (index-level, macro risk-off aligned) over any single name — every single-name short candidate reviewed in the pre-US overlay carried at least one fresh contradicting bullish catalyst.
- Best catalyst-backed candidate: **ABNB** (stocks, short-watch — fresh EU regulatory headwind, entity-resolved, directionally aligned) / crypto: ZEC remains the most-cited but is now two-sided.
- What to avoid: **PLTR short** (BLOCKed — fresh, multiply-sourced bullish narrative directly contradicts); chasing ATOM/FF/SAHARA above zone (documented-negative no-catalyst playbook); treating BNB/USDT (~3.6+ days stale) as fresh; single-name stock shorts with a same-morning bullish contradiction (XOM, DIS, VRTX, AMGN, COIN); anything reliant on the mismapped UBER/USDT catalyst row.
- What would change the view: a second-source confirmation or correction on the Iran/Israel fronts; BTC/ETH losing uptrend structure (would resolve the technical-vs-macro contradiction toward risk-off); RTH open price action confirming or failing the semis-RS / energy-strength thesis; a live premarket RS-vs-sector re-check on any of the 10 pre-US SUPPORT names once the code's clamp condition can be satisfied.

## 7. Candidate Deep Dives

### ANET (stocks, pre-US overlay SUPPORT, base_score 72.5, watch)
- Catalyst: "Arista Networks Targets $12.6B as AI, Campus and Cloud Networking Growth Accelerates" (Finnhub, 05:02 UTC) — fresh, entity-resolved, directly aligned with the long direction.
- Sector backdrop: technology RS +1.75% vs SPY, semiconductors +1.67% — modest but real tailwind, not overextended.
- Has price already reacted? Report-level premarket move not independently re-verified this cycle (RS-vs-sector clamp applied by the ingest code, adjustment=0).
- Actionable now or after confirmation? After RTH open confirms the pre-open level holds with volume — this is a watch, not a pre-open entry (market closed, cap-only C-tier).
- Would invalidate: a broad tech/semis reversal at the open, or a fresh contradicting ANET-specific headline.

### ABNB (stocks, pre-US overlay SUPPORT, base_score 89.0, short-watch)
- Catalyst: "Airbnb Set To Face More Restrictions As European Commission Proposes New Rules To Tackle Housing Crunch" (t.me/marketfeed, 10:37 UTC) — fresh, entity-resolved regulatory headwind, aligned with short.
- Not a hard legal-risk block (no indictment/SEC/DOJ/class-action/delisting trigger) — stays an overlay SUPPORT, not an AVOID.
- Actionable now or after confirmation? After RTH confirms weakness; do not pre-position on the headline alone pre-open.
- Would invalidate: a same-day denial/clarification from Airbnb or the EU Commission, or a strong open against the short.

### PLTR (stocks, pre-US overlay BLOCK, base_score 77.1, avoid this window)
- Contradicting catalysts found same-morning: "Palantir Technologies Displays High-Growth Leadership and Momentum on CAN SLIM Screen," "Why Palantir Rallied Over 50% in August," "Palantir vs. Tesla: Which AI Stock Should You Buy?" — three independent bullish framings, no bearish counter-evidence found.
- Verdict: BLOCK applied — 3h TTL veto (`block_expires_at` 2026-09-09T17:01:25 UTC) on the short signal only; underlying signal/scoring untouched.
- Actionable now or after confirmation? Not this window. Re-check after the veto expires or at the next review slot.

### ZEC/USDT (crypto swing B-tier 68.2 — contested long-watch, carried forward)
- `waiting_for_entry`, zone now 1198.18–1208.58 (moved up from 1191–1199 at 11:45), invalidation 1185.47.
- Catalyst confirmation, updated: institutional ETF-inflow thesis (Grayscale $500M, 72% short-interest) still stands, but a fresh same-morning contrarian quote ("an obvious pump and dump," JAN3 CEO Samson Mow, t.me/CoinMarketCapAnnouncements, 11:10 UTC) plus a high-implied-yield covered-call story (Grayscale, 12:20 UTC, reflecting elevated volatility) make this a genuinely two-sided setup now, not a clean confirmed catalyst.
- Actionable now or after confirmation? After a confirmed fill inside the (moved) zone with volume — patience is more warranted this cycle than at 11:45, given the fresh contrarian voice.
- Invalidation: 1185.47.

### BNB/USDT (crypto swing B-tier 73.8 — stale avoid, third+ consecutive review)
- `waiting_for_entry`, unchanged zone 759.24–761.96, invalidation 755.92, now ~3.6+ days aging with the `binance_ecosystem_teaser` basket catalyst still unrefreshed.
- Verdict unchanged: stale-before-entry, not urgent, flagged again as this cycle's crypto avoid/no-fresh-action carryover.

### DOT/USDT + UNI/USDT (crypto swing, catalyst-backed, already entered/unresolved)
- Both remain `triggered` per this cycle's active-signals pull, unchanged status from 11:45. UNI remains explicitly named as catalyst-confirmed in the current `momentum_breakout` basket text; DOT has dropped out of the current basket's primary/related list (basket membership churns cycle to cycle — not itself a red flag, just noted).
- Actionable now or after confirmation? Hold/monitor only — re-verify invalidation hasn't been breached at the next review.

## 8. Best Candidates Ranked

1. **ANET long-watch** (stocks) — fresh AI/networking catalyst + positive semis/tech sector RS; requires RTH open confirmation, not actionable pre-open.
2. **ABNB short-watch** (stocks) — fresh EU regulatory headwind, entity-resolved; requires RTH confirmation.
3. **SPY / DIA short-watch** (stocks, index-level) — cleanest macro-aligned short exposure (oil/Iran risk-off) vs. single names that fresh news keeps contradicting; requires RTH confirmation, not a pre-open entry.
4. **ZEC/USDT catalyst-watch (contested)** (crypto) — institutional-inflow thesis intact but now genuinely two-sided; confirm fill inside 1198.18–1208.58 before treating as live, and weigh the fresh "pump and dump" counter-narrative.
5. **DOT/UNI catalyst-watch** (crypto, already entered/unresolved) — hold/monitor, re-verify invalidation.
- Avoid this window: **PLTR short** (BLOCKed); **BNB/USDT** (stale ~3.6+ days); **ATOM/FF/SAHARA** (documented-negative no-catalyst playbook); single-name stock shorts contradicted by fresh bullish catalysts (XOM, DIS, VRTX, AMGN, COIN).

## 9. Avoid / No Trade

*(This decision window only — scanning, tracking, and monitoring continue regardless.)*
- **PLTR short** — BLOCKed this cycle (3h TTL veto) on multiply-sourced fresh bullish contradiction.
- **XOM, DIS, VRTX, AMGN, COIN shorts** — each carries at least one fresh, same-morning catalyst that contradicts the short direction (oil-price tailwind for XOM; analyst rating upgrade for DIS; Goldman conviction-list add for VRTX; positive clinical trial data for AMGN; bullish partnership news for COIN). CAUTION verdicts, not clean shorts.
- **ATOM/USDT, FF/USDT, SAHARA/USDT** above their planned entry zones — no-catalyst playbook with a documented negative 14-day edge (WR 23%/PF 0.70/−3R per prior review).
- **BNB/USDT** — not a fresh idea, unchanged zone ~3.6+ days, catalyst unrefreshed.
- Any decision reliant on the mismapped `UBER/USDT` catalyst row (actually a Rivian headline) — treat catalyst layer as context only this cycle (63.5% unmapped).
- General: RTH still closed at review time — all 37 pre-US-reviewed stock candidates remain planning/watchlist only until the 09:30 ET open confirms levels.

## 10. Main Risks

- **Geopolitical, still live and unresolved for a third consecutive review:** Iran/Israel fronts, Brent >$100/bbl — the single biggest swing factor into the US open.
- **Technical-vs-macro contradiction in crypto, unresolved for a second consecutive review:** BTC/ETH uptrend vs. 100/100 macro risk-off score inside the same report.
- **Scheduler/data-pipeline health, worsening pattern:** 9 failures in today's cycle (8 timeouts at ~300s across paper-execution/paper-TP/entry-mode/stock-direction/entry-latency/paper-shadow/portfolio-ledger/intelligence-layer refreshes, plus obsidian dashboard failing fast at 60s instead of its prior 6h05m hang) — this review independently reproduced the pattern live via a hung `signal-stats --asset-class stocks` call and 17+ concurrent python.exe processes at review time. This looks systemic (DB contention), not isolated to one script.
- **Concrete catalyst mis-mapping confirmed this cycle:** `UBER/USDT` catalyst row is actually a Rivian headline — a specific, reproducible instance beyond the general 63.5%-unmapped statistic.
- **ZEC's long thesis is now genuinely contested**, not clean — a fresh contrarian "pump and dump" quote appeared same-morning alongside the institutional-inflow story.
- **Crypto book remains 100% one-sided long** (50/50 active signals), unchanged all week — no hedge available if either geopolitical front worsens or the technical uptrend breaks. This continues to line up with the still-open `bias_tag_contradiction` project issue (symbols tagged bias=short with negative 24h performance appearing in the "Weakest Symbols" list while simultaneously held as active long positions — AERO/USDT -8.23%, TUT/USDT -7.24%, and HEMI/USDT -16.13% all reproduced this pattern in this cycle's intraday report) — flagged again, not fixed.
- **Regulatory headline risk on crypto broadly:** a `news_items` row ("US Treasury targeting Iran sanctions evasion through Bitcoin and USDT," tagged `block_requires_operator_review`) is a fresh general crypto-regulatory headline, not tied to one active signal but worth awareness given the fully-long book.
- **Stocks headline stats unavailable this cycle** — `signal-stats --asset-class stocks` timed out twice; the previously-documented suspicious 0-loss/PF=inf pattern (n=157) from the 11:45 review could not be re-checked.

## 11. Action Plan — next 4 hours

- Watch for RTH open (09:30 ET) confirmation on ANET (long) and ABNB (short) before treating either as live; use SPY/DIA for macro-aligned index short exposure if the open confirms risk-off continuation.
- Do not act on PLTR short until its 3h BLOCK veto expires (17:01:25 UTC) and only after re-checking for fresh contradicting news at that time.
- Re-confirm ZEC/USDT's fill inside 1198.18–1208.58 at the next review (18:30 EEST US-open-reaction slot); weigh the fresh "pump and dump" counter-narrative before treating any fill as high-confidence.
- Re-confirm DOT/USDT and UNI/USDT haven't breached invalidation.
- Do not chase ATOM/FF/SAHARA above zone.
- Treat catalyst-layer output as directional color only this cycle (63.5% unmapped, one confirmed mismap) — do not cite `UBER/USDT` catalyst row as evidence for anything.
- At the next review, re-attempt `signal-stats --asset-class stocks` and re-check scheduler timeout pattern; if the 8-step timeout pattern repeats a second consecutive cycle, escalate priority on the corresponding §14 TODO.

## 12. Final Verdict per Mode

- **Crypto scalp:** deliberately disabled (unchanged, no verdict applicable).
- **Crypto intraday/swing:** no clean fresh long or short this cycle; ZEC is a contested catalyst-watch (confirm fill, weigh contrarian voice), DOT/UNI are hold/monitor catalyst-backed positions already entered, BNB is a stale avoid, ATOM/FF/SAHARA are do-not-chase no-catalyst momentum. Book remains 100% long — treat as a data point, not an instruction to add shorts.
- **Stocks intraday:** RTH closed; 37 pre-US candidates processed via the structured hand-off — 10 SUPPORT-graded watches (ANET, ABNB, SPY, DIA, MRVL, INTC, AMD, TSM, KLAC, META), 1 BLOCK (PLTR, avoid this window), 7 CAUTION (single-name shorts contradicted by fresh bullish news), 11 NEUTRAL, 8 INSUFFICIENT_DATA. All require RTH confirmation before any is actionable.
- **Stocks swing / invest:** deprecated (shadow-only position framework in effect) — not evaluated, consistent with prior reviews.

## 13. Sources

- Internal: proposed_signals / news_items SQLite queries — this session, 2026-09-09 12:50–13:05 UTC
- [data/reports/intraday/2026-09-09_11-05_intraday_report.md] (generated 2026-09-09 14:04:55 EEST)
- [data/reports/swing/2026-09-09_04-12_swing_report.md] (generated ~07:11 EEST, borderline carry-forward)
- [data/reports/stocks/intraday/2026-09-09_12-23_stocks_intraday_report.md] (data freshness 12:08 UTC)
- [data/catalysts/2026-09-09/catalyst_events.jsonl], [narrative_baskets.jsonl], [catalyst_cycle_11-14.md]
- [reports/STOCKS_PREUS_REVIEW_CANDIDATES.md] (generated 2026-09-09T12:54:49 UTC, this cycle)
- [data/raw/enriched_review_sources/preus_review_2026-09-09T12-58-36Z.json] (this cycle's 37 hand-off verdicts)
- [data/scheduled_runs/2026-09-08_default_schedule/scheduler.log], [cycle_03_09-47_summary.md] (live production log, read ~16:00 EEST)
- [OPUS_ENRICHED_REVIEW_AUTO_2026-09-09_1145.md] (prior review, used for §4 comparison)
- news_items (internal, Finnhub company-news): "Strategy Launches $250 Bitcoin Air Jordans but Won't Let You Pay in BTC," published 2026-09-09T09:42:01Z — market color only, not cited as a trading catalyst.
- news_items (internal, Finnhub company-news): "Arista Networks Targets $12.6B as AI, Campus and Cloud Networking Growth Accelerates," published 2026-09-09T05:02:02Z
- news_items (internal, t.me/marketfeed): "Airbnb Set To Face More Restrictions As European Commission Proposes New Rules To Tackle Housing Crunch," published 2026-09-09T10:37:33Z
- news_items (internal, Finnhub company-news x3): "Palantir Technologies Displays High-Growth Leadership...," "Why Palantir Rallied Over 50% in August," "Palantir vs. Tesla: Which AI Stock Should You Buy?" — published 2026-09-09T09:40:00Z–11:12:40Z
- news_items (internal, t.me/CoinMarketCapAnnouncements): "JAN3 CEO Samson Mow called Zcash 'an obvious pump and dump'," published 2026-09-09T11:10:10Z
- news_items (internal, CoinDesk): "Bitcoin recovers toward $79,000 as Zcash records a $500 million ETF haul," published 2026-09-09T04:35:55Z
- news_items (internal, AMBCrypto): "Zcash shorts hit 72% as ZEC price holds above $1,100," published 2026-09-09T03:00:37Z
- news_items (internal, BeInCrypto): "US Treasury's Office Targeting Iran's Sanctions Evasion Through Bitcoin and USDT" — dated within the macro/geopolitics module of the 11:05 intraday report.
- catalyst_events.jsonl row (internal, Finnhub company-news): "Rivian R2 Demand Tops Expectations as Autonomy and Robotaxi Plans Advance" — mis-tagged as `UBER/USDT` [earnings_event], importance 0.72; cited as evidence of the §14 mapping-quality bug, not as a trading catalyst.
- No external web sources cited this cycle (internal-first discipline satisfied for all 37 hand-off candidates and all base-routine candidates; internal `news_items` coverage was recent and sufficient).

## 14. Fix Requests / TODO

### TODO-scheduler-db-contention
- **issue:** 8 of 9 step failures in today's cycle_03 (09:47–11:42 EEST) are `(timeout)` at almost exactly 300s (paper-execution/paper-TP/entry-mode/stock-direction/entry-latency/paper-shadow/portfolio-ledger/intelligence-layer refreshes), plus `refresh obsidian dashboard` failing fast at 60s (previously a 6h05m hang on 2026-08-31 per project history). This review independently reproduced the pattern live: `signal-stats --asset-class stocks` timed out twice (45s and 60s bounded attempts), and `tasklist` showed 17+ concurrent python.exe processes at review time, one holding ~3.7GB RSS.
- **evidence:** `data/scheduled_runs/2026-09-08_default_schedule/cycle_03_09-47_summary.md` steps 25/26/28/29/30/31/38/40/82; this review's own bounded `signal-stats --asset-class stocks` attempts (both exit=124).
- **suggested manual fix:** investigate DB lock/contention (likely SQLite write-lock contention given the process count and long-running memory-heavy process) as the common root cause across the paper-* refreshes, the obsidian dashboard step, and signal-stats; consider whether the ~3.7GB process is a runaway/stuck job.
- **priority:** high
- **first observed:** 2026-09-09 16:08 EEST (this review); related prior incident 2026-08-31 (obsidian dashboard 6h05m hang, per project history).

### TODO-catalyst-uber-rivian-mismap
- **issue:** A catalyst_events.jsonl row tagged `UBER/USDT` [earnings_event] importance 0.72 is actually a Rivian headline ("Rivian R2 Demand Tops Expectations as Autonomy and Robotaxi Plans Advance") — wrong entity entirely. Stock tickers (XOM, UBER, COIN) also appear with a `/USDT` crypto-pair suffix in the top-catalysts list, suggesting an asset-class mixing artifact in the symbol resolver, not just a one-off mismatch.
- **evidence:** `data/catalysts/2026-09-09/catalyst_cycle_11-14.md`, "Top catalysts by importance" section, `0.72 **UBER/USDT** [earnings_event] Rivian R2 Demand Tops Expectations...`.
- **suggested manual fix:** audit the symbol resolver for stock-vs-crypto entity confusion (RIVN vs UBER, or a ticker-adjacency bug) and for the `/USDT` suffix being applied to non-crypto tickers.
- **priority:** medium
- **first observed:** 2026-09-09 16:08 EEST.

### TODO-bias-tag-contradiction-recurrence
- **issue:** Symbols tagged `bias short` with negative 24h performance in the intraday report's "Weakest Symbols" list, while simultaneously held as active long positions in the same-day armed-watch table — AERO/USDT (bias short, -8.23%, but an active swing long, `sig_d482be05fc0a7d16`), TUT/USDT (bias short, -7.24%, active swing long tp1_hit, `sig_63abd1a2060b9ac2`), HEMI/USDT (bias short, -16.13%, active swing long waiting_for_entry, `sig_382f4a56792643ef`). This is the same systemic issue already tracked in project history (symbol-agnostic, recurring since 2026-08-08) — confirmed still unfixed with three fresh instances this cycle.
- **evidence:** `data/reports/intraday/2026-09-09_11-05_intraday_report.md` §2 "Weakest Symbols"; `active_crypto_wide.txt` (this review's CLI pull) rows for AERO/USDT, TUT/USDT, HEMI/USDT.
- **suggested manual fix:** per prior project note — reconcile the bias-tagging logic against the actual open-position direction table; this is a labeling/display bug, not a scoring bug (the actual positions are long, correctly).
- **priority:** high (carried forward, still unresolved)
- **first observed (this instance):** 2026-09-09 16:08 EEST; original issue first observed 2026-08-08 per project history.

### TODO-stocks-signal-stats-unavailable
- **issue:** `python -m src.cli signal-stats --asset-class stocks` did not complete within 45s or 60s bounded attempts during this review (two separate tries), while the crypto equivalent completed on a background retry (~3 min). Stocks headline performance stats (including the previously-flagged suspicious 0-loss/PF=inf pattern, n=157, from the 11:45 review) could not be re-checked this cycle.
- **evidence:** this review's two bounded `timeout 45/60 python -m src.cli signal-stats --asset-class stocks` calls, both exit=124.
- **suggested manual fix:** profile the stocks signal-stats query specifically (likely related to TODO-scheduler-db-contention above, but stocks appears more consistently affected than crypto in this run) — may indicate a stocks-specific slow query or a larger stocks proposed_signals table needing an index.
- **priority:** medium
- **first observed:** 2026-09-09 16:08 EEST.
