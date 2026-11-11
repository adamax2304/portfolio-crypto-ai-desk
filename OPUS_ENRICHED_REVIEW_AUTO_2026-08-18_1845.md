# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

## 1. Executive Summary
**Slot: US open reaction review (18:30 EEST fixed slot). Advisory only — no auto-trade.** Crypto stays technically bullish (BTC/ETH uptrend, altcoin breadth 55%) but sits under a heavy macro risk-off overlay (Iran/Hormuz shipping attack, 30Y Treasury yield at a 19-year high) — no fresh A/B this cycle in scalp/intraday/swing; best idea remains the existing **EDEN/USDT swing long** watch. Stocks regime label is "bullish" (VIX 15.74, breadth 100%) but the desk's own A/B paper performance this week is poor (winrate 6.9%, PF 0.25, -1.5R) and the current cycle produced **zero actionable A/B** (18 raw A/B setups all demoted to C by lunch/liquidity/catalyst/legal gates). Four stocks positions from earlier cycles remain open: **GE long** (A-tier, thesis intact, chip/industrials divergence favors it), **AVGO / INTC short** (semis weakness vs. rising yields), and **META short** — but META still carries an unresolved legal-headline risk (29-state lawsuit reportedly reaching court today) that the production risk-warning block still does not surface, so META is downgraded to manual review here, not a clean short. Catalyst mapping remains weak (73.8% unmapped, unchanged from the last cycle). One system-integrity finding this cycle: 2 untracked HEMI/USDT legacy alerts (recurring, previously escalated) plus new evidence of duplicate proposed_signal minting on GE/META/AVGO/INTC — both routed to §14, no live changes made.

## 2. Data Used
- Reports: `data/reports/scalp/2026-08-18_13-28_scalp_report.md`, `data/reports/intraday/2026-08-18_13-35_intraday_report.md`, `data/reports/swing/2026-08-18_14-39_swing_report.md`, `data/reports/stocks/intraday/2026-08-18_15-32_stocks_intraday_report.md`
- Stocks swing/invest reports are the deprecated single-shot artifacts from 2026-07-02 (position-framework rebuild in progress per project history) — excluded from this review, not treated as "stale."
- `data/catalysts/2026-08-18/catalyst_events.jsonl` (2444 rows), `narrative_baskets.jsonl` (2 baskets), `catalyst_cycle_13-40.md`
- `data/processed/llm_analysis_packet.md` (17:40), `data/processed/llm_stocks_packet.md` (17:05)
- CLI: `active-signals` (crypto n=47, stocks n=50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-18`
- Direct read query on `news_items` (META legal-headline verification) and `db/crypto_ai_desk.sqlite` proposed_signals for duplicate-signal check — read-only, per §A.1
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_1709.md` (§4 comparison)
- External web research: not invoked this cycle — internal `news_items` + catalyst records were fresh, consistent, and sufficient for every candidate touched (§G discipline); no WebSearch/WebFetch calls made.

## 3. Scheduler / Data Freshness
- `scheduler.log`: mtime 17:48 (57 min old) — cycle 1 ended 17:48:56, ok=98 failed=1, telegram=sent. **Fresh.**
- `cycle_01_16-20_summary.md`: mtime 17:48 — fresh.
- Background monitors alive: derivatives_monitor and fast_news_monitor logs updated 18:43 (2 min old); pending/crypto/invest-forward/stocks monitors reported "still running" at end-of-cycle (lifetimes 90–180 min).
- Report freshness: stocks intraday 7 min old (fresh, right at open-reaction window); crypto swing ~1h06m old (fresh); crypto intraday ~2h10m, scalp ~2h17m (fresh, <4h band).
- Catalyst folder present for today (7 cycle files, latest 16:40).
- No deferral triggered (both freshness checks well under the 3h rule).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-18 18:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["live orderbook/derivatives for stocks"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 57min", "stocks intraday report 7min old", "stocks swing/invest deprecated since 2026-07-02"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "risk_off", "longs_preferred", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, macro risk score 100/100 (Iran/Hormuz, 30Y yield 19yr high)", "stocks: bullish label VIX 15.74 breadth 100% but semis (AVGO/INTC/TSM) diverging weak vs industrials (GE)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["73.8% unmapped catalyst events (1804/2444)", "2 active narrative baskets: perps_dex_narrative (HYPE), momentum_breakout (ACE)", "META 29-state lawsuit confirmed via 2 internal news_items (Motley Fool 08-17, CNBC 08-17)"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.45,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["stocks options/OI", "crypto liquidation heatmap"],
      "suggested_effect": "advisory_only",
      "facts_used": ["EDEN/GPS/BMT/RED/ACE all price-up + OI-up (fresh positioning, no extreme funding)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "clean_retest", "stale_before_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["stocks open positions (GE/AVGO/META/INTC) entered ~14:0x UTC, now 1.5h+ into the move at lunch-gate window", "crypto swing longs plan pullback entries, not chases"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 18 triggered, 2 waiting_for_entry, 19 tp1_hit, 8 tp2_hit (n=47)", "stocks: 19 triggered, 9 waiting_for_entry, 19 tp1_hit, 3 tp2_hit (n=50)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["META unresolved legal headline not in production risk-warning block (TODO-1, carried forward)", "stocks A/B this week: winrate 6.9%, PF 0.25, -1.5R — daily_loss_pressure", "HD/PANW earnings-today block_requires_operator_review"] },
    { "agent": "playbook_performance", "verdict": "bad", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing PF 7.96 avgR +0.92 (n=44, working)", "crypto intraday PF 0.69 avgR -0.22 / scalp PF 0.50 (both failing)", "stocks A/B headline PF 0.25 winrate 6.9% (n=44, failing)", "crypto shorts 0W/3L PF 0.0 this week (n=7, anecdotal but consistently bad)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "EDEN/USDT", "trigger": "pullback fill into 0.0500-0.0516, 1h close beyond 0.0460 invalidates", "reason": "RS-leader (score 73.2), swing playbook 14d WR72%/PF5.80, no chase — OI+price confirm" },
    "best_short_candidate":    { "symbol": "AVGO", "trigger": "already filled 379.36-381.60 (open); no fresh short qualifies this cycle — new semis shorts need sector-confirmation + RVOL to clear lunch gate", "reason": "semis (AVGO/INTC/TSM) diverging weak vs rising yields, sector-confirmed at entry" },
    "best_catalyst_candidate": { "symbol": "XRP/USDT", "trigger": "RS turning positive vs BTC + a scoreable 15m-1h technical structure forming around the Jeonbuk Bank partnership catalyst", "reason": "verified fresh catalyst, no technical setup yet — watch only" },
    "avoid_candidate":         { "symbol": "META", "reason": "active unresolved legal headline (29-state suit in court today, CNBC 'astronomical consequences') not yet reflected in the production risk-warning block — treat existing short as manual review, do not add" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | mixed, risk_off, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.45 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_late, clean_retest, stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.70 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | bad | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review
(vs `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_1709.md`, 17:09 EEST)
- **New:** none — no fresh A/B minted in either asset class since 17:09; the 15:32 stocks-intraday cycle produced 0 actionable A/B (18 raw A/B all gate-demoted).
- **Removed/expired:** none observed; GE/AVGO/META/DIA positions from the prior cycle remain open (DIA short at B67 tp1_hit — progressed, no longer freshly "triggered").
- **Upgraded/downgraded:** no tier changes on open positions.
- **Confirmed:** GE long and AVGO short theses unchanged — still the desk's best stocks ideas. META legal-risk concern (TODO-1) **still unresolved** — production risk block still shows only BTC/DXCM/HD/PANW.
- **Catalyst coverage:** flat at 73.8% unmapped (was 73.8% at 17:09 too — same underlying `catalyst_events.jsonl` file, no new ingest between cycles).
- **System integrity:** untracked legacy alerts dropped from 4 (17:09, HEMI×2/EDEN/GPS) to 2 (18:45, HEMI×2 only) — EDEN/GPS rows aged out of the ±6h detector window, not resolved. New finding this cycle: duplicate proposed_signal minting on GE/META/AVGO/INTC (see §14 TODO-4), not previously flagged.
- **Thesis change:** none. XRP/USDT catalyst-watch idea carries forward unchanged (still no technical structure).

## 5. Catalyst Coverage
- Total catalyst_events today: **2444** | mapped (non-null symbol): **640** | unmapped: **1804 (73.8%)**
- Narrative baskets: **2** (`perps_dex_narrative` primary HYPE/USDT fresh<6h; `momentum_breakout` primary ACE/USDT fresh<1h)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sample): "Enginprime Medical Closes $12M Series A Financing"; "Greenberg Traurig's Marissa A. Neufeld Appointed to Miami Homes For All Board of Directors"; "Aastro Roofing Company Named Deerfield Beach's Roofer of the Year" — small-cap PR-newswire noise, consistent with TODO-2's earlier diagnosis.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed** (technical uptrend BTC/ETH + 55% altcoin breadth above EMA20, vs. macro risk-off 100/100 from Iran/Hormuz shipping attack + naval blockade + 30Y yield at a 19-year high)
- Stocks mood: **mixed** (regime label "bullish", VIX 15.74, breadth 100%, but semis/AI names selling into rising yields while industrials/GE hold up; this week's real A/B paper performance is poor — PF 0.25)
- Dominant narrative: crypto — perps/DEX and momentum-breakout baskets (HYPE, ACE) fresh but thin (single_source only); stocks — AI capex/financing debate (Broadcom $370B financing, Microsoft AI-spend valuation compression) and rising-yields rotation out of chips
- Preferred side now: **longs** (crypto RS-leader swing pullbacks only); stocks — hold existing GE long / AVGO-INTC shorts, do **not** chase new stocks A/B this cycle (gated to zero, and week's stats say caution is warranted anyway)
- Best long candidate: EDEN/USDT (swing, pullback 0.0500-0.0516)
- Best short candidate: none fresh — AVGO/INTC shorts already open from earlier cycle; crypto shorts have a 0W/3L week, avoid fresh crypto shorts
- Best catalyst-backed candidate: XRP/USDT (Jeonbuk Bank partnership) — watch only, no technical trigger yet
- What to avoid: META short (unresolved legal headline, manual review); any new crypto scalp/intraday (PF <1 this week); any new stocks A/B during the 15:30-16:30 UTC lunch window (structurally gated)
- What would change the view: a clean 1h close by BTC below its recent swing low (would flip crypto short-side interest on); META's court outcome becoming known/priced or the production risk block picking it up (would resolve the manual-review flag one way or the other); stocks A/B sample growing past 50 with improved PF (would re-open confidence in chasing new stocks setups)

## 7. Candidate Deep Dives

### 1. EDEN/USDT — LONG (crypto, B-tier swing, score 73.2, status waiting_for_entry)
- Has price already reacted? No — current price 0.0523 sits above the 0.0500-0.0516 planned pullback zone; setup is waiting for a retrace, not chasing.
- Chasing risk? Low if entry discipline (pullback only) is respected; the report explicitly says "no market buy if extended."
- Retest/pullback structure? Yes — that's the entire entry plan.
- Overextended (>2 ATR from EMA20)? Not flagged; ATR 0.0036 vs current 0.0523, support 0.0465.
- Would entry now (at market) be late? Yes, for a market order; the plan already accounts for this by requiring the pullback.
- Level that makes it actionable: fill inside 0.0500-0.0516.
- Aligned with market mood? Yes — RS-leader long inside a technical uptrend, consistent with "selective longs, prefer pullbacks" regime guidance; the macro risk-off overlay argues for smaller size / tighter invalidation discipline, not skipping the idea.
- Long/short/wait-for-trigger? Long, wait-for-trigger (pullback).
- Actionable now or after confirmation? After the pullback fills — not actionable at current market price.
- Invalidation: 1h close beyond 0.0460.
- Catalyst confirmation/contradiction? No fresh verified catalyst — thesis rests purely on RS + narrative-basket momentum (`momentum_breakout`-adjacent), not a hard news catalyst. TradingView/manual chart check unavailable — using only the local OHLCV/ATR/EMA fields from the report.

### 2. GE — LONG (stocks, A-tier intraday, score 100, status triggered ×2 open)
- Has price already reacted? Yes — position already filled 369.4462-370.7100 in an earlier cycle; a prior GE instance already banked TP1 today.
- Chasing risk? For a *new* entry now, yes — this cycle's report demotes GE A→C on `sector_confirmation_conflict` + `lunch_requires_strong_confirmation` + no fresh catalyst. Existing open fills are not chasing; a fresh add here would be.
- Retest/pullback structure? Not currently offered — the live positions are riding the existing fill.
- Overextended? Not flagged in the report.
- Would entry now be late? For fresh size, yes (lunch-gate window, no new catalyst).
- Level that makes a fresh add actionable: RTH confirmation clearing the lunch gate, or a clean pullback retest of the 368.18 invalidation zone with sector confirmation restored.
- Aligned with market mood? Yes — industrials holding up while chips sell off is exactly the kind of RS-leadership the "bullish but narrow" tape rewards.
- Long/short/wait-for-trigger? Long, hold existing / wait-for-trigger on adds.
- Actionable now? Existing fills: yes (open, managed). New size: no, wait for gate to clear.
- Invalidation: 368.1823.
- Catalyst confirmation/contradiction? A `risk_warning`-level geopolitical item exists (GEK800 engine USAF award) — advisory only, not disqualifying. No hard positive catalyst backing the long; it is RS/technical driven.

### 3. AVGO — SHORT (stocks, B-tier intraday, score 66.7, status triggered ×2 open — duplicate, see §14 TODO-4)
- Has price already reacted? Yes — filled 379.36-381.60 during the early-session chip selloff (NVDA/MU/SNDK tumbling on rising yields per §4 News).
- Chasing risk? For the existing fill, no (entered near the move's start). For a fresh add now, moderate — the move is 1.5h+ old.
- Retest/pullback structure? Current report demotes new AVGO shorts to C on `lunch_requires_strong_confirmation` — no clean fresh retest offered this cycle.
- Overextended? Not explicitly flagged; treat with caution given elapsed time.
- Would entry now be late? For new size, likely yes.
- Level that makes a fresh add actionable: sector-confirmed continuation clearing the lunch gate + RVOL support.
- Aligned with market mood? Yes — sector-confirmed semis weakness vs. yields is the cleanest short thesis on the desk right now.
- Long/short/wait-for-trigger? Short, hold existing / wait-for-trigger on adds.
- Invalidation: 383.8415.
- Catalyst confirmation/contradiction? No direct AVGO catalyst; thesis is sector/macro (rates) driven, consistent with the broader chip-selloff headlines.

### 4. META — SHORT, downgraded to AVOID/MANUAL REVIEW (stocks, B-tier, score 71.8, status triggered ×3 — duplicate, see §14 TODO-4)
- Has price already reacted? Position filled 549.15-551.78 during the early session; one earlier META short instance already hit TP2 today.
- **LEGAL/HEADLINE RISK:** confirmed via 2 internal sources — "Meta Faces 29 States in Court Tuesday. The Case Could Be Big Tech's Big Tobacco Moment." (The Motley Fool Investing, 2026-08-17 18:55 EDT) and "Meta faces 'astronomical' consequences as legal fight reaches critical moment in California" (CNBC Markets, 2026-08-17 16:06 UTC). "Tuesday" = today, 2026-08-18. This is the same unresolved item flagged as TODO-1 in the 17:09 review; still not in the production risk-warning block (which lists only BTC/DXCM/HD/PANW).
- Per §I discipline: verified legal/headline risk on a stocks A/B candidate forces the verdict to AVOID or MANUAL REVIEW — never a clean actionable, regardless of the short thesis otherwise lining up with sector weakness.
- Aligned with market mood? Directionally yes (tech/AI valuation compression), but the legal overhang makes the risk/reward asymmetric and headline-gap-prone (court outcomes can gap the stock either direction intraday).
- Actionable now? No — existing open exposure should be treated as manual review, not added to.
- Catalyst confirmation/contradiction? Confirms elevated risk, does not confirm the short's technical thesis one way or the other — a court development could just as easily cause a violent short squeeze on relief as extend the down move.

### 5. XRP/USDT — CATALYST-WATCH (crypto, no active score/tier)
- Has price already reacted? Not materially — no technical setup has formed yet per the swing report ("fresh attention/catalyst detected... risks []").
- Catalyst: Ripple partners with South Korea's Jeonbuk Bank for cross-border payments (The Block) — real, no contradicting risk flags.
- Chasing risk? N/A — nothing to chase yet.
- What would make it actionable: RS turning positive vs. BTC + a scoreable technical structure forming on 15m-1h (same trigger as the prior review — still unmet).
- Aligned with market mood? Directionally consistent with "catalyst-backed longs" being one of the desk's preferred idea types in a mixed/risk-off-tinged crypto tape.
- Long/short/wait-for-trigger? Wait-for-trigger.

## 8. Best Candidates Ranked
1. **GE long** (stocks, A-tier, open) — best overall: RS-leadership vs. weak chips, catalyst-neutral but technically clean; existing fills managed, fresh adds wait for the lunch gate to clear.
2. **AVGO short** (stocks, B-tier, open) — best clean short: sector-confirmed semis weakness vs. rising yields, no legal cloud.
3. **EDEN/USDT long-watch** (crypto, B-tier swing) — best fresh crypto idea: RS-leader, pullback-only entry at 0.0500-0.0516, invalidation 0.0460.
4. **XRP/USDT catalyst-watch** (crypto) — real catalyst, no technical trigger yet; re-check each cycle for RS-vs-BTC turning positive.
5. **META** — explicitly demoted out of actionable ranking; manual-review-only pending resolution of the legal headline or the production risk block picking it up.

## 9. Avoid / No Trade
_This decision window only — scanning, tracking, and the scheduler continue regardless._
- **META** (stocks short) — unresolved legal headline (29-state suit in court today), manual review required, do not add.
- **New crypto scalp/intraday entries** — this week's PF is 0.69 (intraday) and 0.50 (scalp) with negative avgR; no fresh A/B minted anyway this cycle.
- **New stocks A/B during 15:30-16:30 UTC lunch window** — structurally gated (`lunch_requires_strong_confirmation` hit 18 times this cycle); wait for post-lunch confirmation.
- **HD, PANW** — earnings today, `block_requires_operator_review` + `do_not_chase_warning` already active in production.
- **INTU, REGN** — active class-action legal risk, already correctly demoted A→C by the system; do not manually override.

## 10. Main Risks
- Crypto macro overlay: Iran/Hormuz shipping attack + naval blockade + 30Y yields at a 19-year high — a genuine risk-off shock could invalidate correlated crypto swing longs quickly; size and invalidation discipline matter more than usual.
- Stocks A/B quality risk: this week's actionable-tier paper performance (winrate 6.9%, PF 0.25, -1.5R, n=44) is weak enough that even A-tier scores (GE, INTU, REGN, etc.) should be treated skeptically until the sample improves or the entry-quality gates (already firing hard this cycle — 18/18 raw A/B demoted) show a cleaner pass-through.
- META headline-gap risk: a short position sitting through an active, unresolved 29-state legal proceeding carries two-sided gap risk that a technical stop cannot fully protect against.
- Catalyst-mapping blind spot: 73.8% of today's catalyst events are unmapped to a symbol — treat any catalyst-driven thesis (including XRP/USDT above) as advisory, not proof.
- Duplicate-signal data-quality risk: GE/META/AVGO/INTC each show 2-3 near-identical proposed_signals minted minutes apart this cycle (see TODO-4) — this inflates the apparent sample size in `signal-stats` without adding real diversity; the headline winrate/PF numbers above should be read with that caveat in mind, though the direction of the numbers (stocks A/B weak, crypto swing strong) is unlikely to flip once cleaned up.

## 11. Action Plan — next 4 hours
- Hold existing GE long, AVGO short, INTC short positions as managed; do not add fresh size until the post-lunch gate clears with sector confirmation.
- Treat META short as manual-review-only: no adds, consider whether existing exposure should be reduced given the unresolved court-case gap risk (operator decision, not automated).
- Watch EDEN/USDT for a pullback fill into 0.0500-0.0516; do not chase at current 0.0523+.
- Watch XRP/USDT for RS-vs-BTC turning positive + a scoreable 15m-1h structure before it becomes a real candidate.
- No new crypto scalp/intraday or fresh stocks A/B chasing this window — scanning and tracking continue as normal in the background.
- Re-check HD/PANW post-earnings reaction next cycle once the operator-review block clears.

## 12. Final Verdict per Mode
- **Crypto scalp:** NO TRADE — no active idea clears the desk threshold this cycle; week's PF 0.50, avoid fresh entries.
- **Crypto intraday:** NO TRADE — no A/B setups found; week's PF 0.69, avgR -0.22, avoid fresh entries.
- **Crypto swing:** WATCHLIST / WAIT-FOR-TRIGGER — EDEN/USDT (and BMT/GPS as secondary RS-leaders) pending pullback fills; week's PF 7.96 supports staying engaged with discipline.
- **Stocks intraday:** MANUAL REVIEW / HOLD-EXISTING-ONLY — 0 fresh actionable A/B this cycle (18 gate-demoted); existing GE/AVGO/INTC positions managed; META flagged manual review; do not chase new setups given this week's weak A/B stats (PF 0.25).
- **Stocks swing/invest:** N/A this cycle — reports deprecated pending position-framework rebuild (per project history); no verdict issued.

## 13. Sources
- [Meta Faces 29 States in Court Tuesday](internal news_items — The Motley Fool Investing, 2026-08-17 18:55 EDT) — internal record, verification_status: primary_source (major outlet, dated)
- [Meta faces 'astronomical' consequences as legal fight reaches critical moment in California](internal news_items — CNBC Markets, 2026-08-17 16:06 UTC) — internal record, verification_status: primary_source
- [Ripple partners with South Korea's Jeonbuk Bank for cross-border payments](internal — The Block, via swing report §5) — verification_status: single_source
- `data/catalysts/2026-08-18/catalyst_events.jsonl`, `narrative_baskets.jsonl` — internal, generated 2026-08-18 16:40
- `data/reports/stocks/intraday/2026-08-18_15-32_stocks_intraday_report.md` — internal, generated 2026-08-18 15:32 UTC
- `data/reports/swing/2026-08-18_14-39_swing_report.md` — internal, generated 2026-08-18 14:39 UTC
- `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_1709.md` — internal, prior review, 2026-08-18 17:09 EEST

## 14. Fix Requests / TODO

### TODO-1: META legal-headline gap not yet in production risk-warning block (recurring, unresolved)
- **issue:** META has an active 29-state lawsuit reportedly reaching a critical court moment today (2026-08-18), per 2 internal news_items rows, but the production "Operator-review warning" block still lists only BTC, DXCM, HD, PANW.
- **evidence:** `db/crypto_ai_desk.sqlite` news_items query, 2 rows: "Meta Faces 29 States in Court Tuesday..." (Motley Fool, 2026-08-17) and "Meta faces 'astronomical' consequences..." (CNBC, 2026-08-17); `data/reports/stocks/intraday/2026-08-18_15-32_stocks_intraday_report.md` §"Production risk warnings" still omits META.
- **suggested manual fix:** review the legal_risk/class_action detector's symbol-matching — a "X states sue Y in court [today]" + "astronomical consequences" headline pair should trigger `block_requires_operator_review` the same way HD/PANW earnings-day warnings do.
- **priority:** high
- **first observed:** 2026-08-18 17:09 EEST (still open at 18:45 EEST — second consecutive cycle unresolved)

### TODO-2: Catalyst mapping stuck below 50% (flat, not improving)
- **issue:** catalyst symbol-mapping coverage is 73.8% unmapped, unchanged from the 17:09 EEST review (same underlying file, no new ingest cycle between reviews).
- **evidence:** `data/catalysts/2026-08-18/catalyst_events.jsonl`: 2444 total, 640 mapped, 1804 unmapped. Sample unmapped headlines are small-cap PR-newswire noise (financings, board appointments, local business awards).
- **suggested manual fix:** as previously noted — filter obvious non-market PR-newswire noise (financings/appointments/local awards) out of the unmapped denominator, or improve the symbol resolver; this is a display-only diagnostic so no scoring risk in fixing it.
- **priority:** medium
- **first observed:** 2026-08-18 11:39 EEST (recurring — 3rd consecutive cycle at ~70-74% unmapped)

### TODO-3: Untracked legacy crypto alerts recurring (2 today, down from 4 last cycle)
- **issue:** `detect_untracked_legacy_alerts` found 2 watchlist_alerts sent to Telegram today (HEMI/USDT ×2, 08:52 and 12:02 UTC) with no matching `proposed_signal` within ±6h.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-18` — 2 rows, both `trackable=NO`.
- **suggested manual fix:** known, previously-confirmed issue (watchlist re-fire reuses a stale/closed signal_id instead of minting a new proposed_signal) — per project history, confirmed on ALLO/USDT and BANK/USDT previously, now HEMI/USDT. Escalate given repeated recurrence across many review cycles.
- **priority:** high
- **first observed:** recurring, multiple prior cycles (see project memory `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug.md`)

### TODO-4 (NEW): Duplicate proposed_signal minting within minutes for the same symbol/direction/entry
- **issue:** GE, META, AVGO, and INTC each show 2-3 `proposed_signals` rows with identical entry_low/entry_high/invalidation, minted within a 2-6 minute window this cycle (GE ×2 at 14:07:06/14:09:01; META ×3 at 14:03:23/14:07:06/14:09:01; AVGO ×2 at 14:07:06/14:09:01; INTC ×2 both at 14:28:07). This inflates the effective sample size counted by `signal-stats` without representing genuinely distinct trade opportunities.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` output this cycle — e.g. `sig_bc88416f...` and `sig_e9b2f0ea...` both GE long 369.4462/370.7100/368.1823; `sig_25f4e643...`, `sig_0feae0a6...`, `sig_21dd14ef...` all META short 549.1520/551.7846/554.4173.
- **suggested manual fix:** audit the stocks-intraday signal-generation loop for idempotency — likely the same underlying setup is being re-scored and re-proposed on consecutive scheduler sub-cycles within the same entry window instead of recognizing an already-open identical proposal for the symbol/direction/entry-zone combination.
- **priority:** medium
- **first observed:** 2026-08-18 18:45 EEST
