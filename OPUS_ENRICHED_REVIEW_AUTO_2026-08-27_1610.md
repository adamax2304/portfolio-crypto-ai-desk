# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:10 EEST

## 1. Executive Summary
- Slot: **pre-US-open decision review** (target 09:00 America/New_York; actual fire ≈08:59–09:01 ET — within tolerance, no DST drift). Advisory only — no auto-trade, no code/strategy changes made.
- **Time-critical 09:00 ET hand-off completed**: `stocks-preus-candidates` found 24 eligible candidates; all 24 given a verdict (13 INSUFFICIENT_DATA, 6 CAUTION, 5 NEUTRAL — **zero SUPPORT**, deliberately: no SPY/QQQ premarket feed or RS-vs-sector data was verified in time, so no candidate met the strict SUPPORT bar). Ingest applied 12 fresh verdicts; 12 were preserved from an earlier deterministic baseline (`IGNORED_INSUFFICIENT_PRESERVED_BASELINE` — not overridden, not stale). `stocks-preus-review-health` reports **`PENDING_DEADLINE`** (reason: `structured_preus_review_not_yet_due`) — not `READY`/`NO_ELIGIBLE`, but not an error either; no promotion is claimed for the 12 preserved rows.
- **The dominant overnight catalyst is NVDA's blowout Q2 print** (verified via internal Telegram/Finnhub/MarketWatch sources): $96.2B revenue beat, $108B Q3 guide, "demand acceleration," stock +4–5% AH, Nasdaq futures +1.2% / S&P futures +0.6% pre-open, and price-target raises from JPMorgan/Mizuho/Melius/Goldman/Bernstein. This lifts the AI/semis complex specifically (SMH/XLK already leading 20d) — it is a **narrow sector tailwind**, not a broad risk-on signal (SPY/QQQ/IWM regime is still classified "transition," VIX 14.99, neutral bias).
- Crypto book is **100% long** (50/50 active B-tier signals, zero shorts, zero A-tier) inside a "bullish trend / risk-on" swing regime — but macro geopolitical risk is pinned at 100/100 (Hormuz naval-blockade rhetoric, Iran sanctions, CIA-Moscow warning). That is a genuine **mixed** regime: constructive price action against a real macro tail-risk overhang, with no short-side diversification if it reverses.
- Catalyst mapping is weak this run (78.2% unmapped, 437/2000 mapped) — consistent with the persistent, already-tracked pattern; treat the catalyst layer as context, not a decision driver.
- NVDA itself remains **avoid/manual-review**, not a clean long or short: it carries a standing legal-risk flag (Taiwan chip-smuggling indictment, tracked in prior reviews) plus a same-day "in talks to acquire Hugging Face — the platform an OpenAI agent previously hacked" headline. Compounding risk flags override the earnings beat for actionability purposes.

## 2. Data Used
- Reports (all same-day, all fresh): scalp N/A this cycle read directly, intraday (14:00 EEST), swing (15:46 EEST) — crypto; stocks intraday (14:55 EEST). Stocks swing/invest: latest file is 2026-07-02 — deprecated/removed framework (confirmed prior), correctly excluded, not "stale."
- `data/catalysts/2026-08-27/` — catalyst_events.jsonl (2000 rows), narrative_baskets.jsonl (4 baskets), catalyst_cycle_11-09.md (latest cycle file today).
- `data/processed/llm_analysis_packet.md` (16:02 EEST), `llm_stocks_packet.md` (14:57 EEST).
- CLI: `active-signals` ×2 (crypto n=50 shown, all B-tier long; stocks n=50 shown, historical tp1_hit/tp2_hit/triggered back to 2026-07-29), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-08-27` (**6 untracked** crypto alerts found).
- Pre-US overlay: `stocks-preus-candidates` (24 eligible / 54 excluded), `stocks-preus-review-ingest` (24/24 verdicts submitted, 12 applied fresh / 12 preserved baseline), `stocks-preus-review-health` (`PENDING_DEADLINE`).
- DB read queries: `news_items` freshness checks (last ~24–30h) for all 21 unique pre-open candidate symbols.
- External web research: **not exercised this run** — internal `news_items`/report data was sufficient to reach a verdict (mostly "no material catalyst, only generic listicle/opinion content") for every pre-open candidate within the 09:05 ET hand-off window; WebSearch/WebFetch were skipped deliberately to protect the deadline, per §G fallback rules (time-boxed, not "unavailable").

## 3. Scheduler / Data Freshness
- Pre-US schedule check: target 09:00 ET, actual fire ≈08:59–09:01 ET (Δ within ~1–2 min, well within tolerance — no DST-window mismatch; today is outside both 2026 DST-mismatch windows).
- `data/scheduled_runs/2026-08-27_default_schedule/scheduler.log` — mtime effectively now (actively being written). **Fresh.**
- No `cycle_*_summary.md` has been written yet in today's folder (only per-process logs so far: derivatives_monitor, fast_news_monitor, telegram_dashboard, scheduler.log). The most recent cycle summary on disk is `2026-08-26_default_schedule/cycle_06_10-02_summary.md` (>24h old). Per §D, defer requires **both** scheduler.log AND the cycle summary to be >3h stale — scheduler.log is fresh, so **no defer**. Flagged here as a minor data-quality gap (today's cycle-summary generation appears delayed/absent so far), not a blocker.
- Report freshness: swing 15:46 EEST (24 min old), intraday 14:00 EEST (2h10m), stocks intraday 14:55 EEST (1h15m) — all fresh (<4h). Stocks swing/invest: deprecated, excluded correctly.
- Pre-US overlay health: `PENDING_DEADLINE` / `structured_preus_review_not_yet_due` — 12/24 reviewed fresh this cycle, 12/24 preserved from an earlier deterministic baseline (not stale, already assessed). No promotion claimed for the preserved 12.
- Monitor/paper status: not separately queried (outside this run's read-only allowlist beyond the listed CLI commands).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-27 16:10 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["today's cycle_*_summary.md (not yet written)", "stocks_swing_invest_reports (deprecated, not a gap)"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log actively updating", "swing/intraday/stocks-intraday reports all <2.5h", "no cycle_06+ summary written yet today"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "risk_off", "longs_preferred", "wait_for_trigger"], "data_missing": ["live SPY/QQQ premarket tape", "live VIX print at hand-off time"],
      "suggested_effect": "advisory_only", "facts_used": ["crypto: BTC/ETH uptrend, 72.9% alts >EMA20, macro risk 100/100 (Hormuz/Iran)", "stocks: regime=transition, VIX 14.99, breadth 50%/100% (EMA20/EMA50), NVDA blowout Q2 lifting semis/AI narrowly"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "catalyst_contradicted", "no_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["78.2% catalyst events unmapped today (437/2000 mapped) — persistent, already-tracked pattern", "NVDA Q2 beat corroborated across Telegram marketfeed + Finnhub + MarketWatch", "META: EU Commission screen-time/parental-control pressure contradicts long thesis", "13/24 pre-open candidates had only generic listicle/opinion content, not real catalysts"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["stocks options/short-interest flow (not in allowed sources)"],
      "suggested_effect": "advisory_only", "facts_used": ["crypto RS leaders (CHIP/RUNE/S/MOVR) show price up + OI up, funding near-zero/slightly negative — fresh positioning, not yet extreme"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["stale_before_entry", "clean_retest", "chase_risk"], "data_missing": ["RTH opening-range data (market not yet open at hand-off time)", "TradingView/manual chart confirmation unavailable"],
      "suggested_effect": "advisory_only", "facts_used": ["crypto swing report defines explicit pullback zones for CHIP/RUNE/S/MOVR — do not chase 24h vertical movers", "stocks pre-open candidates are still market_closed_intraday_planning_only — cannot assess RTH entry freshness yet"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.6,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "needs_review", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto: 50 active B-tier (mix triggered/waiting_for_entry), 0 A-tier", "stocks: legacy tp1_hit/tp2_hit/triggered rows from as far back as 2026-07-29 still shown active (stale-resolution gap, tracked)", "pre-open overlay: 12 fresh verdicts applied, 12 preserved baseline, health=PENDING_DEADLINE", "6 untracked legacy crypto alerts today (known bug, no proposed_signal backing)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["headline_risk", "correlation_cluster", "legal_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto book is 100% long / 0 shorts — correlation/concentration risk if BTC reverses under macro risk-off headlines", "NVDA: standing legal-risk flag (Taiwan indictment) + fresh Hugging Face 'hacked platform' headline entanglement despite the earnings beat", "META: EU regulatory pressure headline against long thesis", "MRVL/AFRM report earnings today — do-not-chase"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto A/B headline: winrate 12.6% but PF 1.80, avgR +0.18, totalR +61.0 — low-winrate/high-R trend-following profile, consistent with prior reviews", "crypto weekend cohort underperforms (winrate 11%, n=137) — known flag", "stocks tier C (n=558, reliable): winrate 8%, PF 0.59 — weak, persistent", "stocks tier B (n=16, weak sample): winrate 11%, PF 4.0 — too small to trust"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "DELL", "trigger": "wait for RTH open + hold/retest above the pre-market reference zone (entry_trigger ~464.02) before treating as live; do not gap-chase", "reason": "raw pre-gate A (score 91.85), fresh same-day technical breakout note (Minervini trend template) + UBS price-target raise, reinforced by the NVDA-beat AI/semis sector tailwind" },
    "best_short_candidate":    { "symbol": "PYTH/USDT", "trigger": "manual watch only — confirm 1h close below the recent swing low with RS vs BTC staying negative and no bullish catalyst reversal", "reason": "weakest RS in today's swing report (-6.32% vs BTC, -5.03% 24h); price down + OI down = deleveraging, not squeeze-prone, unlike the thinner POL/GPS shorts capped to C" },
    "best_catalyst_candidate": { "symbol": "DELL", "trigger": "same as best-long — RTH confirmation required, no blind chase of the AH pop already priced into futures", "reason": "cleanest catalyst-plus-technical combination among all 24 pre-open candidates; NEUTRAL verdict this cycle only because SPY/QQQ premarket and RS-vs-sector data were not verified in time, not because the catalyst is weak" },
    "avoid_candidate":         { "symbol": "NVDA", "reason": "excluded by the pre-open hard gate (LEGAL_RISK) despite the blowout earnings — standing Taiwan chip-smuggling indictment plus a fresh 'in talks to acquire Hugging Face, the platform an OpenAI agent previously hacked' headline; manual review only, neither a clean long nor short" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---:|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | mixed, risk_off, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, catalyst_confirmed, catalyst_contradicted, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | stale_before_entry, clean_retest, chase_risk | advisory_only |
| execution_lifecycle | needs_review | 0.60 | waiting_for_entry, entered_unresolved, needs_review, no_entry | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, correlation_cluster, legal_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | ok | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review
Previous: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-27_1139.md` (Europe / pre-US context, 11:39 EEST).
- **New**: NVDA's Q2 earnings beat and the resulting AI/semis sector tailwind — not present in the 11:39 review (which only flagged NVDA's legal risk + Hugging Face rumor, pre-earnings). This is the single biggest change into the US open.
- **New**: the time-critical 09:00 ET pre-open stocks overlay (24 candidates scored, 12 fresh/12 preserved) — this mechanism did not exist as an input to the 11:39 review.
- **Confirmed unchanged**: NVDA and REGN both still carry standing legal/headline risk and remain manual-review-only, not clean actionable, in either direction.
- **Confirmed unchanged**: catalyst mapping still weak (78.2% today vs 79.2% at 11:39) — same persistent pattern, not a new regression.
- **Confirmed unchanged**: crypto swing book still 100% long, still bullish-trend/risk-on classification, still macro risk-off overhang (Hormuz/Iran) running alongside it.
- **Upgraded context, same names**: DELL, MSFT, TSM, HOOD were already on the 11:39 review's raw-candidate list (as ORCL/DELL/MSFT/... demoted-to-C planning names); DELL is now the standout of that group given the fresh analyst/technical catalyst plus the NVDA halo effect.
- **New this cycle**: 6 untracked legacy crypto alerts detected (EDEN, SOL×2, S, BICO, ONT) — same class of bug as `TODO-3` already tracked in project history (watchlist-alert/proposed_signal reuse), not a new root cause, but fresh evidence it is still live.

## 5. Catalyst Coverage
- Total catalyst events today: **2000**; mapped: **437** (21.8%); unmapped: **1563** (78.2%); narrative baskets: **4** (`binance_ecosystem_teaser`, `perps_dex_narrative`, `ai_narrative`, `momentum_breakout`).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top unmapped headlines are BOJ commentary (macro/central-bank, arguably acceptable to be unmapped by design — same open question as the prior review).

### Pre-US Stocks Review Overlay
- candidates reviewed: 24 (SUPPORT 0 / NEUTRAL 5 / CAUTION 6 / BLOCK 0 / INSUFFICIENT_DATA 13)
- session-cap-only C's now eligible for pre-open Paper lane: 15 (all `promotable=true` in the candidate list: ISRG, DXCM, TSLA, COST×2, SBUX, TSM, GILD, NFLX, BKNG, HOOD, DELL, MSFT — tier/adjustment enforcement is entirely code-side; no SUPPORT was granted so no score lift was applied to any of them)
- excluded by hard gate: 54 (44 `NO_ENTITY_RESOLVED_CATALYST`, 10 `LEGAL_RISK` incl. NVDA×2/UNH/MAR×2/INTU/REGN/BLK, 5 `EARNINGS_BLACKOUT` incl. AAPL×2/GOOGL/NOW/LLY/BIIB)
- Verdict reasoning in one line: 13/24 candidates had no material, entity-specific catalyst beyond generic "Best Stocks" listicles or Motley Fool opinion pieces; 6/24 had a genuine fresh item that **contradicted** the signal's direction (META long vs. EU regulatory pressure; HD/COST/BKNG shorts vs. bullish-leaning commentary); 5/24 (SBUX, TSM, GILD, HOOD, DELL) had a mildly supportive fresh item but lacked verified SPY/QQQ/RS-vs-sector confirmation within the hand-off window, so were capped at NEUTRAL rather than SUPPORT.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed** (bullish trend/risk-on price action; risk-off macro overhang from Hormuz/Iran headlines; 100% long book with no short diversification)
- Stocks mood: **mixed / pre-market** (broad index regime = transition/neutral, VIX 14.99; but **narrow risk-on** in AI/semis specifically off the NVDA beat)
- Dominant narrative: NVDA Q2 beat → AI/semis capex tailwind (DELL, TSM, MSFT, AMD, MU all named in overnight coverage); crypto RS-leader momentum (CHIP/RUNE/S/MOVR/BICO) inside a broader bullish-trend regime
- Preferred side now: **catalyst-backed longs** in the AI/semis complex (RTH-confirmed, not gap-chased) for stocks; **RS-leader longs with defined pullback zones** for crypto; no clean short setup confirmed on either side this cycle
- Best long candidate: DELL (stocks, needs RTH confirmation) / CHIP-RUNE-S-MOVR cohort (crypto, needs pullback fill, not market-buy)
- Best short candidate: none clean on stocks (all short-tier candidates carried CAUTION-level contradicting news); PYTH/USDT on crypto (watch-only, needs 1h close confirmation)
- Best catalyst-backed candidate: DELL
- What to avoid: NVDA (legal_risk + hack-headline entanglement, manual review only); META long (EU regulatory pressure against thesis); MRVL/AFRM intraday (earnings today, do-not-chase); any blind pre-market gap-chase into the NVDA halo before RTH confirms it isn't already priced in
- What would change the view: RTH opening range on DELL/TSM/MSFT holding above pre-market reference (confirms the AI tailwind is durable, not a fade); BTC/ETH structure holding above swing-report support if a Hormuz/Iran headline escalates; a resolution (positive or negative) on the NVDA legal-risk items

## 7. Candidate Deep Dives

### 7.1 DELL (long, pre-gate A / current C — planning only pre-open)
- Catalyst: fresh same-day Finnhub items — "Clears Minervini Trend Template with High Growth Momentum" and "Dell Stock Climbs After UBS Raises Target" (analyst PT raise). Reinforced by the broader NVDA-beat AI/semis tailwind (DELL is a named AI-server beneficiary in overnight coverage).
- Has price already reacted? Not observable — market not yet open at hand-off time; AH/pre-market reaction unverified (no live premarket feed used this cycle).
- Chasing? Cannot assess yet — needs RTH open. Retest/pullback structure: entry_trigger 464.02 / stop 456.99 from the code's pre-gate levels; treat that as the reference zone, not a blind buy.
- Overextended vs EMA20? Unknown — TradingView/manual chart check unavailable this cycle; only the code's own levels are used, no fabricated chart read.
- Aligned with mood? Yes — narrow AI/semis risk-on is the dominant overnight theme.
- Actionable now or after confirmation? **After confirmation only** — RTH open + hold above/retest of the reference zone.
- Invalidation: 1h/session close back below the stop level, or a broad-market fade that shows the NVDA halo was already priced in.
- Chase risk: real — the AH pop is a known, already-discussed catalyst; do not buy the gap blind.
- Catalyst confirmation/contradiction: confirmed by two independent internal sources (Finnhub items) plus sector-level corroboration (NVDA beat, SMH/XLK 20d strength); no contradicting news found.

### 7.2 NVDA (avoid / manual review — excluded from pre-open eligible list by hard gate)
- Catalyst: genuinely major — $96.2B Q2 revenue beat, $108B Q3 guide, stock +4–5% AH, multiple bank PT raises (JPM $320, Mizuho $315, Melius $420, Goldman $300, Bernstein $400).
- But: carries a standing `LEGAL_RISK` gate hit (excluded twice in today's candidate list, sig_e72a3f53f2705267 and sig_ee384c7fa30be2ad) tied to the Taiwan chip-smuggling indictment tracked in prior reviews, **plus** a same-day headline that Nvidia is "in talks to acquire Hugging Face — the platform an OpenAI agent previously hacked" (t.me/WatcherGuru, t.me/marketfeed).
- Verdict: **avoid / manual review required** in both directions. The earnings beat does not clear the legal/headline risk; a long chases a name under active indictment scrutiny, a short fights a blowout print. Not a clean trade either way this cycle.

### 7.3 META (long, pre-gate C — CAUTION this cycle)
- Catalyst: "EU Commission spokesperson says META must improve screen time management and parental control" + "EU Commission held talks with $META since US settlement" (t.me/marketfeed, both today).
- This is a genuine regulatory-pressure headline working **against** a long thesis — potential future restrictions/fines, not supportive.
- Verdict: CAUTION (-4 adjustment applied), score 56.57→52.57, tier remains C. Not actionable as a clean long until the regulatory overhang clarifies.

### 7.4 CHIP/USDT (long, crypto swing B-tier, score 72.4)
- Thesis: continuation/pullback inside a bullish-trend regime; momentum 91.6/100, RS vs BTC +10.2%, 24h +11.5%.
- Has price reacted already? Yes — vertical 24h move; entry plan explicitly calls for a pullback into 0.0362–0.0368, not a market buy at current price (0.0371, already near the top of that zone).
- Overextended? Volume is below average (0.3x) despite the move — weak breakout confirmation, a real counter-thesis point per the report itself.
- Catalyst: none verified — this is a pure RS/momentum setup, no fresh catalyst attached.
- Actionable now or after confirmation? Only on the defined pullback; do not chase the current print.
- Invalidation: 1h close below 0.0355.

### 7.5 PYTH/USDT (short-watch, crypto)
- Weakest RS in today's swing report: -6.32% vs BTC, -5.03% 24h.
- Price down + OI down = deleveraging pattern, not a squeeze-prone short (unlike the thinner POL/GPS names the system already caps to C for squeeze risk).
- Not system-leveled this cycle (no active short signal) — this is a manual watch-only idea.
- Trigger: confirm 1h close below the recent swing low with RS staying negative and no bullish catalyst reversal (e.g. no fresh RWA-narrative pickup, which the swing report shows *is* active elsewhere — RWA basket is "mixed," not clearly bearish, so this needs fresh confirmation, not an assumption).

## 8. Best Candidates Ranked
1. **DELL** (long, catalyst-backed) — best overall idea this cycle; wait for RTH confirmation.
2. **CHIP/RUNE/S/MOVR/USDT cohort** (long, crypto RS-momentum) — actionable only on defined pullback zones, not market price.
3. **TSM / MSFT / HOOD / SBUX / GILD** (long-watch, stocks) — NEUTRAL verdict; mildly supportive catalysts but unconfirmed against market context; re-check after RTH open.
4. **PYTH/USDT** (short-watch, crypto) — needs 1h close confirmation below swing low.
5. No clean catalyst-backed short exists on stocks this cycle — closest candidates (HD, COST, BKNG shorts) all carry a contradicting bullish-leaning headline; treat as short-watch only if RTH price action fails to follow that bullish tilt.

## 9. Avoid / No Trade (this decision window only)
- **NVDA** — legal_risk + hack-headline entanglement overrides the earnings beat; manual review only.
- **META long** — EU regulatory pressure headline contradicts the thesis.
- **MRVL, AFRM** — earnings today; do-not-chase into the print (swing-blocked by earnings per the stocks intraday report).
- **Any blind gap-chase** on AI/semis names before RTH confirms the NVDA halo isn't already fully priced into futures.
- This is a decision-window verdict only — scanning, candidate generation, and tracking continue in all cases; nothing here recommends pausing the scanner or scheduler.

## 10. Main Risks
- Macro geopolitical risk score is pinned at 100/100 (Hormuz naval-blockade rhetoric, Iran sanctions, CIA-Moscow warning) while crypto price action is bullish and the book is 100% long — a reversal risk with zero short-side offset.
- NVDA's dual-edged setup (blowout earnings vs. active legal/headline risk) could whipsalt sentiment either way at the open; do not treat the AH pop as risk-free confirmation for AI-adjacent longs.
- Catalyst mapping remains weak (78.2% unmapped) — do not over-weight the catalyst layer for any single-name decision today.
- 6 untracked legacy crypto alerts today — these will not contribute to PF/winrate tracking; a recurrence of the known watchlist-alert/signal-reuse bug (see §14).
- Stale, unresolved historical signals (some from 2026-07-29) still appear "active" in `active-signals` for stocks — inflates the apparent open-signal count; carried forward from the prior review, still unresolved.

## 11. Action Plan — next 4 hours
- Watch RTH open (09:30 ET) for DELL/TSM/MSFT/HOOD: require a hold or retest above the pre-market reference zone before treating any as live; do not chase the first print.
- Watch crypto RS leaders (CHIP/RUNE/S/MOVR/BICO) for a pullback fill into their defined entry zones; do not buy the current vertical extension.
- Watch PYTH/USDT for a 1h close below its swing low as the cleanest short-watch trigger available this cycle.
- Re-check NVDA/META/REGN legal-and-headline-risk status at the next cycle before considering either a clean long or short.
- Flag the still-missing today's cycle-summary file and the 6 untracked alerts to the operator (see §14) — no code action taken.

## 12. Final Verdict per Mode
- **Crypto scalp**: no fresh input this cycle (not separately re-pulled); prior state — disabled by kill-switch, net-negative historically (PF ~0.1).
- **Crypto intraday**: watch-only; no A-tier, B-tier waiting-for-entry names present, none reviewed as high-conviction this cycle.
- **Crypto swing**: watch / selective-longs-on-pullback; RS-leader cohort (CHIP/RUNE/S/MOVR/BICO) is the cleanest lane, entries only on defined pullback zones, not market price. Winrate is low (12.6%) but avgR/PF are net-positive (0.18 / 1.80) — trend-following profile, consistent with prior cycles.
- **Stocks intraday**: wait-for-RTH-confirmation across the board; zero A/B actionable pre-open by design (market-closed gate); DELL is the standout watch name once the session opens.
- **Stocks swing/invest**: framework deprecated/removed — no verdict rendered (unchanged from prior reviews).

## 13. Sources
- Internal: [data/reports/swing/2026-08-27_12-46_swing_report.md](data/reports/swing/2026-08-27_12-46_swing_report.md), [data/reports/intraday/2026-08-27_11-00_intraday_report.md](data/reports/intraday/2026-08-27_11-00_intraday_report.md), [data/reports/stocks/intraday/2026-08-27_11-55_stocks_intraday_report.md](data/reports/stocks/intraday/2026-08-27_11-55_stocks_intraday_report.md), [reports/STOCKS_PREUS_REVIEW_CANDIDATES.md](reports/STOCKS_PREUS_REVIEW_CANDIDATES.md), `data/catalysts/2026-08-27/catalyst_events.jsonl`, `db/crypto_ai_desk.sqlite` (`news_items` table, direct read queries).
- NVDA Q2 beat: t.me/marketfeed "🌆 Market News Digest [Aug 26, 2026 EST]" (2026-08-26, internal DB), MarketWatch Top Stories "Nvidia stock is climbing after another set of blockbuster results" (2026-08-27, internal DB), t.me/marketfeed price-target digest (2026-08-27, internal DB) — all primary/aggregator sources already ingested, cross-corroborated across 3 independent internal feeds; no external WebFetch needed.
- META EU regulatory headline: t.me/marketfeed, two items, 2026-08-27T10:15–10:25 UTC (internal DB).
- Home Depot own-PR: PR Newswire (Stocks), "The Home Depot Expands Magic Apron..." 2026-08-27T12:00 UTC (internal DB).

## 14. Fix Requests / TODO

### TODO-untracked-legacy-alerts-recurring
- **issue:** `detect_untracked_legacy_alerts` found 6 crypto Telegram alerts today (EDEN/USDT, SOL/USDT ×2, S/USDT, BICO/USDT, ONT/USDT) with no matching `proposed_signal` within 6h — same class of bug already tracked in project history as the watchlist-alert/signal-reuse issue (TODO-3, raised to high priority 2026-07-17).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-27` output, 6 rows, all `trackable=NO (no proposed_signal)`.
- **suggested manual fix:** confirm whether this is the same reuse-of-stale-signal-id root cause already logged, or a distinct new gap; these alerts will not contribute to PF/winrate tracking.
- **priority:** high (matches an already-escalated open issue; fresh evidence it is still live).
- **first observed (this thread):** 2026-08-27 16:10 EEST — consistent with the 2026-07-17 escalation.

### TODO-catalyst-mapping-weak (persistent, unchanged)
- **issue:** catalyst→symbol mapping is 78.2% unmapped today (437/2000 mapped), essentially unchanged from the 79.2% observed at 11:39 EEST this same day.
- **evidence:** direct count from `data/catalysts/2026-08-27/catalyst_events.jsonl`.
- **suggested manual fix:** unchanged from prior review — confirm whether macro/central-bank headlines (BOJ commentary dominates the unmapped tail again) should be excluded from the 50% threshold as an acceptable-by-design category before treating this as a true regression.
- **priority:** low (known, persistent, not new).
- **first observed (this thread):** 2026-08-27 16:10 EEST — consistent with prior reviews.

### TODO-stale-open-signals-not-expiring (persistent, unchanged)
- **issue:** stocks `active-signals` still shows historical `triggered`/`tp1_hit`/`tp2_hit` rows with `expires_at` weeks in the past (e.g. `sig_57bd3d1e35d6952f` BX and `sig_838e06bbde9dc1c2` COP, both `expires_at` 2026-08-08, still listed as active on 2026-08-27) — same gap flagged in the 11:39 EEST review, still present.
- **evidence:** `active-signals --asset-class stocks` output this cycle.
- **suggested manual fix:** unchanged — a human-driven session should check whether the paper-execution/outcome resolver is correctly closing out partially-booked (tp1_hit/tp2_hit) signals that have gone stale past `expires_at`.
- **priority:** medium.
- **first observed (this thread):** 2026-08-27 16:10 EEST — consistent with the 11:39 EEST review.
