# Opus Enriched Review — late-session risk review — Auto Cycle 21:39 EEST

## 1. Executive Summary

Slot: **late-session risk review** (18:39 UTC / 21:39 EEST, US cash session still open). Advisory only — no auto-trade, no code/scoring changes made. Scheduler is fresh (last cycle ended 21:08 EEST, ~31 min ago). Crypto: technical structure is bullish-trend/risk-on (BTC/ETH uptrend, 87.5% of alts above EMA50) but macro/geopolitical risk score is elevated at 98.4/100 (Iran/Strait of Hormuz tensions, new US sanctions) — a genuine tension between trend and macro tail-risk. **No A-tier crypto setups** this cycle; best B-tier ideas are PYTH/USDT, ONG/USDT, ZRO/USDT (all long, all still requiring pullback/entry discipline). Stocks: regime **transition/neutral**, VIX calm (15.54), but **zero A/B actionable stocks setups** — every A/B candidate was demoted to C by the rolling paper-R drawdown guard or by confirmed legal/headline risk (SMCI indictment, BLK class action). ZRO/USDT scalp signal is live and close to expiry (~1h04m) — worth a status check before end of window. The known untracked-alert tracking bug (ONG/PROM/POL/INJ) recurred again today (8 instances) — already an escalated TODO, not a new issue. Route decisions per mood; do not force trades.

## 2. Data Used

- Crypto swing report `2026-08-25_17-52_swing_report.md` (fresh, ~1h47m old)
- Crypto intraday report `2026-08-25_15-22_intraday_report.md` (~6h17m old — carry-forward, treat as stale-ish for intraday timeframe)
- Crypto scalp report `2026-08-25_15-09_scalp_report.md` (not deep-read this cycle; scalp mode stats pulled via CLI instead)
- Stocks intraday report `2026-08-25_17-00_stocks_intraday_report.md` (~4h39m old — carry-forward, within report's own gate logic which already re-evaluated guards)
- Stocks swing / invest reports: last generated 2026-07-02 — **deprecated/disabled per project decision** (position-framework rework in progress), not treated as a freshness bug
- `data/catalysts/2026-08-25/catalyst_cycle_15-31.md` + `catalyst_events.jsonl` (last 500 events, this cycle)
- `active-signals --asset-class crypto` / `--asset-class stocks` (CLI, read-only)
- `signal-stats --asset-class crypto` / `--asset-class stocks` (CLI, read-only, week window)
- `detect_untracked_legacy_alerts --since 2026-08-25` (CLI, read-only)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-25_1841.md`
- **External web research skipped this cycle** — the one catalyst-backed candidate carried forward (AMD analyst upgrade) is backed by a fresh (<24h) internal catalyst record already surfaced in two consecutive cycles; no candidate this run depended critically on external verification.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-08-25 21:08 EEST (~31 min old) — **fresh**, cycle 2 (17:53 start) ended `CYCLE 2 END ok=90 failed=10 telegram=sent`.
- Latest `cycle_02_17-53_summary.md` mtime: 21:08 EEST — fresh.
- One non-fatal step failure this cycle: `refresh obsidian dashboard` timed out (10s→300s+ hang); cycle continued, telegram dashboard refresh (read-only) succeeded. Cosmetic, not a data-integrity issue.
- Monitors confirmed still running at end-of-cycle: crypto monitor (pid 13276, ~90min), pending monitor (pid 16224, ~180min), mexc-canary monitor (pid 12672, ~180min), crypto-invest-forward monitor (pid 18188, ~180min), fast-news monitor (pid 9600, ~180min), stocks monitor (pid 11172, ~180min).
- Paper monitor status (telegram) step ran and completed (45.9s) — no indication of a stuck/paused paper loop this cycle.
- Swing/intraday crypto reports: fresh / carry-forward as noted in §2. Stocks intraday report ~4h39m old but internally regenerated its own gate state (rolling drawdown guard), so its "no actionable setups" verdict is current logic, not stale data.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-08-25 21:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 21:08 EEST", "cycle_02_17-53_summary.md mtime 21:08", "intraday report 6h17m old", "stocks swing/invest deprecated since 2026-07-02"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["risk_on", "mixed", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: bullish trend risk-on, BTC/ETH uptrend, alt breadth 87.5% above EMA50", "macro/geopolitical risk score 98.4/100 risk-off headwind (Iran/Strait of Hormuz, new US sanctions)", "stocks: regime=transition, bias=neutral, VIX 15.54, breadth mixed (50% >EMA20 / 100% >EMA50)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping this cycle: 119/500 mapped (23.8%), unmapped 76.2% > 50% threshold", "2 active narrative baskets: perps_dex_narrative (HYPE), ai_narrative (NEAR/RENDER/TAO/FET)", "ZRO fresh LayerZero ATLAS catalyst paired with KelpDAO exploit risk event", "AMD analyst Strong-Buy upgrade catalyst carried forward from prior 2 cycles, still not scored A/B"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"], "data_missing": ["liquidation heatmaps", "order book depth/CVD — not connected per report blindspots"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZRO/ONG/ONT/PYTH: price up + OI up, fresh positioning, crowding normal", "PROM/FF: price up + OI down, short covering, weaker continuation quality", "HEMI: price down + OI down, deleveraging/long liquidation"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["entry_fresh", "chase_risk", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PYTH current 0.0526 vs entry zone 0.0519-0.0523 — near miss, small pullback needed", "ONG current 0.1001 vs entry zone 0.0951-0.0985 — extended, needs deeper pullback", "ZRO current 1.252 vs swing entry zone 1.214-1.240 — extended for the new swing idea; scalp version already triggered separately"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "open_actionable", "no_entry"], "data_missing": ["exact total beyond the 50-row CLI display cap"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals (latest 50 shown): ~10 waiting_for_entry, ~30 entered-unresolved (triggered, no TP/SL yet), ~10 open-actionable (tp1/tp2 hit, still running)", "ZRO scalp signal (triggered) expires 2026-08-25T19:43:08 UTC — ~1h04m from now", "stocks: 0 A/B actionable; today's fresh C-tier batch (NFLX/SMCI/HOOD/LRCX/PYPL/QCOM waiting, AMD/MCD/AMZN/MS entered-unresolved) is watchlist-only, not Telegram-pushed"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["SMCI demoted A→C: active legal/headline risk (indictment) — manual review required", "BLK demoted A→C: active legal/headline risk (class action) — manual review required", "NVDA/CRM/CRWD/AFRM/MRVL earnings within the week — do-not-chase warnings active", "macro geopolitical risk score 98.4/100 (Iran sanctions, Strait of Hormuz)", "HYPE: $1.2B token unlock looming — risk_warning"] },
    { "agent": "playbook_performance", "verdict": "bad", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp mode (week, n=114, reliable): PF=0.07, avgR=-0.076, totalR=-6.50 — reproducibly losing bucket", "crypto intraday mode (week, n=150, reliable): PF=2.36, avgR=0.49, totalR=48.81 — strongest bucket", "crypto swing mode (week, n=133, reliable): PF=1.79, avgR=0.18, totalR=20.50 — moderate", "stocks A-tier (week, n=10, weak confidence): PF=8.0, avgR=1.4, totalR=7.0 — too small a sample to lean on", "stocks C-tier (week, n=615): PF=0.43, totalR=-8.0 — expected, watchlist-only by design"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "longs",
    "best_long_candidate": { "symbol": "PYTH/USDT", "trigger": "1h close/hold inside 0.0519-0.0523 pullback zone; invalidation 0.0513", "reason": "Best-scored B-tier crypto swing idea (75.2/100), strongest playbook cohort (crypto_swing_narrative_rs_momentum, 14d WR 72%/PF 5.80), price only ~0.6% above entry zone — not yet extended" },
    "best_short_candidate": { "symbol": "none clean", "trigger": "crypto signal engine is long-only in this bull regime (0 short signals in the reliable weekly sample); stocks MCD/AMZN shorts are triggered but C-tier only — would need a B-tier confirmation or a clean breakdown below entry_low with volume to be actionable", "reason": "No side has a scored, actionable short setup this cycle" },
    "best_catalyst_candidate": { "symbol": "AMD", "trigger": "Strong-Buy analyst upgrade (Yahoo Finance Top Stories, 2026-08-25 catalyst cycle) — carried forward 3 cycles now without becoming an A/B stocks signal; watch for a scored setup or fade if it stays C-tier through tomorrow", "reason": "Only catalyst-backed idea with a repeat internal confirmation across cycles; currently C-tier/triggered, not actionable" },
    "avoid_candidate": { "symbol": "SMCI", "reason": "Demoted A→C on active legal/headline risk (indictment) — manual review required, never a clean actionable regardless of score (was 85.9)" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.70 | risk_on, mixed, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | entry_fresh, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | ok | 0.70 | waiting_for_entry, entered_unresolved, open_actionable, no_entry | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | bad | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (18:41 EEST)

- Previous best long (POL/USDT) has dropped out of the top B-tier list entirely — no longer in the active-signals set; likely closed/expired since 18:41.
- New top B-tier crypto ideas this cycle: PYTH/USDT (75.2), ONG/USDT (73.9), ZRO/USDT (72.4) — none of these were the headline idea last review.
- Best short candidate is unchanged: still **none clean**. Previously HEMI/TUT were noted as squeeze-prone extensions, not confirmed breakdowns — HEMI remains on the weakest-symbols list this cycle (price down + OI down, deleveraging), still not a confirmed short.
- AMD catalyst-watch is unchanged for the 3rd consecutive cycle: still not picked up as a scored A/B stocks signal, still C-tier only.
- Stocks: still 0 A/B actionable, same rolling-drawdown-guard demotion pattern as previous cycle, plus SMCI/BLK legal risk (new detail this cycle vs prior review, which didn't call these out explicitly).
- Macro geopolitical risk score (98.4/100) is a new explicit read this cycle — prior review's summary did not carry this specific number.

## 5. Catalyst Coverage

- Total catalyst events this cycle: **500**; mapped (non-null symbol): **119 (23.8%)**; unmapped: **381 (76.2%)**.
- Narrative baskets: **2** (perps_dex_narrative — primary HYPE/USDT; ai_narrative — primary NEAR/RENDER/TAO/FET).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped 76.2% > 50% threshold)
- Top 3 unmapped headlines (generic macro/PR noise, not trading-relevant):
  1. "German President Frank-Walter Steinmeier on immigrants…"
  2. "Carlos Hank Gonzalez Leads Banorte to Global Sustainability Recognition…"
  3. "United Community Names Dr. Jeff Beisler-Snell Head of International Banking…"

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **risk-on (technical)** with an elevated macro tail-risk overlay — BTC/ETH uptrend, 56.25% of alts above EMA20 / 87.5% above EMA50, but macro/geopolitical risk score 98.4/100 (Iran sanctions, Strait of Hormuz tension, US embassy staff returns). Treat as **bullish-but-headline-fragile**, not clean risk-on.
- Stocks mood: **transition / neutral** — VIX calm at 15.54, breadth mixed (50% above EMA20, 100% above EMA50), only SPY in a confirmed uptrend among the four major indices; energy (XLE) and technology (XLK) are the relative-strength leaders, utilities/industrials weakest.
- Dominant narrative: perps/DEX (HYPE-led) and AI-sector rotation (NEAR/RENDER/TAO/FET) — both flagged fresh (<6h) but single-source, watch for crowding rather than chase.
- Preferred side now: **longs, selective** — pullback entries only, no chasing extended movers.
- Best long candidate: **PYTH/USDT** (crypto) — pullback into 0.0519-0.0523.
- Best short candidate: **none clean** — crypto engine is effectively long-only this week (0 scored shorts in the reliable sample); stocks shorts (MCD, AMZN) are C-tier/triggered but not confirmed to B/A.
- What to avoid: **SMCI** (indictment, legal/headline risk) and **BLK** (class action) — both were A-scored but gated to C; also avoid chasing NVDA/CRM/CRWD/AFRM/MRVL into tomorrow's earnings prints.
- What would change the view: a confirmed B-tier short setup would open the short side; BTC losing local uptrend structure would flip the crypto regime and should prompt reducing long aggression per the system's own no-trade warnings; a rolling-drawdown-guard reset would reopen the stocks A/B pipeline.

## 7. Candidate Deep Dives

### PYTH/USDT — LONG (crypto swing, B-tier, score 75.2)
- Has price already reacted to the catalyst? No fresh verified catalyst for PYTH itself; move is RS/momentum-driven (24h +6.35%, 7d +36.59%, RS vs BTC +5.76%).
- Chasing? Not yet — current price 0.0526 is only ~0.6% above the top of the planned entry zone (0.0519-0.0523).
- Retest/pullback structure? Entry plan explicitly requires a pullback into the zone; no market-buy-if-extended per playbook rules.
- Overextended (>2 ATR from EMA20)? Not stated as overextended in the report; ATR 0.0011, current price close to the zone.
- Late if entered now? Only slightly — a small pullback confirms it; chasing the current price would violate the playbook's own condition-to-avoid.
- Mood alignment: yes — bullish trend regime, RS-leader long, matches the strongest historical cohort (crypto_swing_narrative_rs_momentum, 14d WR 72%/PF 5.80).
- Actionable now or after confirmation? After confirmation — wait for the 0.0519-0.0523 zone to hold on a pullback.
- Invalidation: 1h close beyond 0.0513.
- Chase-risk setup? Low, given proximity to entry.
- Catalyst confirmation/contradiction? None — "no fresh verified catalyst detected," which the playbook itself flags as a counter-thesis point (catalyst-backed is the cleanest sub-cohort, and this one isn't catalyst-backed).
- TradingView / manual chart check unavailable — using only local OHLCV/ATR/EMA fields from the report.

### ZRO/USDT — scalp signal live, near expiry (crypto, B-tier, triggered)
- Status: already **entered, unresolved** (triggered scalp signal), entry zone 1.2084-1.2344, invalidation 1.1767, expires 2026-08-25T19:43:08 UTC (~1h04m from now).
- Catalyst: fresh LayerZero ATLAS platform news, but paired with a risk event (LayerZero axing 14 low-activity chains after the KelpDAO exploit) — playbook flags "catalyst risk event is near the trading window," entry discipline required.
- Mode-level context: crypto **scalp mode is a reproducibly losing bucket this week** (PF 0.07, avgR -0.076, n=114 reliable) — this specific trade should not be read as representative of the desk's edge; treat as a late-session watch item to see if it resolves before window close, not a new-entry idea.
- Actionability: already entered — this is a monitor item, not a new-entry recommendation.

### AMD — catalyst-watch (stocks, C-tier, triggered, score 76.5)
- Has price already reacted to the catalyst? Catalyst is an analyst Strong-Buy upgrade (Yahoo Finance Top Stories) surfaced fresh in today's 15:31 catalyst cycle and carried forward from the two prior review cycles without the scoring engine promoting it past C-tier.
- Chasing? Signal shows status "triggered" (already entered per the scoring engine's internal tracking) but remains C-tier — **not Telegram-actionable**, watchlist/research only.
- What would make it actionable? A tier promotion to A/B in a future cycle, or a fresh technical confirmation independent of the stale analyst-upgrade catalyst.
- Legal/headline risk: none flagged for AMD this cycle.
- Mood alignment: consistent with technology sector's mixed-to-positive relative strength (XLK RS +2.89% vs SPY).

### SMCI — AVOID (stocks, was A-tier 85.9, demoted to C)
- Legal/headline risk: **active indictment** — tier demoted A→C, "manual review required," never a clean actionable regardless of score.
- Source: internal production risk-warning pipeline (SMCI legal/headline risk, already gating this signal before this review ran — no external claim added).
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED**, not a clean actionable under any circumstance this cycle.

### BLK — AVOID (stocks, was A-tier 80.83, demoted to C)
- Legal/headline risk: **active class-action** — tier demoted A→C, "manual review required."
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED**.

## 8. Best Candidates Ranked

1. **PYTH/USDT** (long, crypto, watch) — best long-watch, trigger: pullback hold in 0.0519-0.0523.
2. **ZRO/USDT** (long, crypto, already entered) — monitor to expiry (~19:43 UTC), do not add size; scalp-mode edge is currently negative on the week.
3. **AMD** (long, stocks, catalyst-watch) — trigger: tier promotion to A/B, or a fresh independent technical confirmation; currently C-tier only.
4. **Best short-watch: none clean.** Crypto engine has 0 scored shorts this week; stocks shorts (MCD, AMZN) are C-tier only — trigger for either to become actionable is a B-tier score with a confirmed breakdown below entry_low on volume.
5. **ONG/USDT** (long, crypto, watch-only) — score 73.9 but current price (0.1001) is already through the entry zone top (0.0951-0.0985); would need a deeper pullback than PYTH to avoid chasing. Also has an unrelated data-hygiene issue (see §14) — the *tracked* swing signal itself is fine, but duplicate untracked Telegram alerts were sent for this symbol today.

## 9. Avoid / No Trade (this decision window only)

- **SMCI** — active indictment, legal/headline risk, manual review required.
- **BLK** — active class action, legal/headline risk, manual review required.
- **NVDA, CRM, CRWD, AFRM, MRVL** — earnings within the week (NVDA/CRM/CRWD tomorrow 2026-08-26); do-not-chase warnings active, avoid new entries or holding through the print.
- Stocks intraday broadly: 0 A/B actionable this cycle — all candidates gated by the rolling paper-R drawdown guard (protective mechanism working as designed, not a system failure) or legal risk. This applies to **this decision window only**; scanning, tracking, and the guard's own rolling-window reset continue normally — this is not a command to pause the system.
- Crypto scalp mode broadly: PF 0.07 this week — exercise added caution on any *new* scalp entries specifically (ZRO's existing position is a monitor-to-resolution item, not a new entry).

## 10. Main Risks

- Macro/geopolitical risk score 98.4/100 (Iran sanctions, Strait of Hormuz tensions) sits underneath a bullish crypto technical picture — a headline escalation could invalidate correlated long setups quickly per the system's own no-trade warning ("if BTC loses local support, reduce long aggression immediately").
- HYPE/USDT: $1.2B token unlock looming — relevant given HYPE is the primary of the perps_dex_narrative basket.
- Catalyst mapping is weak this cycle (76.2% unmapped) — treat catalyst layer as context only, not a decision driver, for anything not individually verified.
- Crypto scalp mode is a confirmed losing bucket this week (PF 0.07) — the one live scalp position (ZRO) should be watched to resolution, not used as a template for new scalp entries.
- Known tracking-integrity bug (untracked Telegram alerts without a backing `proposed_signal`) recurred again today — 8 instances (POL x2, PROM x3, INJ x1, ONG x2) — does not affect PF/winrate stats materially (these never had a signal_id to begin with) but continues to under-count what actually got sent to the user.

## 11. Action Plan — next 4 hours

- Monitor ZRO/USDT scalp position to its 19:43 UTC expiry; no new scalp entries in the meantime given the mode's negative week-to-date edge.
- Watch PYTH/USDT for a pullback hold into 0.0519-0.0523; do not chase the current price.
- No new stocks entries expected while the rolling-drawdown guard is active on the long side; re-check next cycle (23:15 EEST post-close review) for a guard reset or a genuine A/B breakout.
- Keep AMD on catalyst-watch; if it's still C-tier by the post-close review, treat the analyst-upgrade catalyst as stale/priced-in for scoring purposes (still fine as macro color).
- No action needed on SMCI/BLK beyond continuing to exclude them from any manual override consideration.

## 12. Final Verdict per Mode

- **Crypto scalp:** CAUTION — one live position (ZRO) monitor-to-resolution; no new entries recommended given PF 0.07 week-to-date.
- **Crypto intraday:** WATCH — strongest mode this week (PF 2.36) but no fresh A-tier idea this cycle; reuse ONG/PYTH context if a fresh intraday report lands with a clean entry.
- **Crypto swing:** WATCH / WAIT-FOR-TRIGGER — PYTH is the cleanest idea, pullback-only.
- **Stocks intraday:** NO NEW ENTRIES this window — 0 A/B actionable, guard-gated; scanning/tracking continues normally.
- **Stocks swing/invest:** N/A — deprecated pending position-framework rework (not a freshness bug).

## 13. Sources

- Internal: [swing report 17:52](data/reports/swing/2026-08-25_17-52_swing_report.md), [intraday report 15:22](data/reports/intraday/2026-08-25_15-22_intraday_report.md), [stocks intraday report 17:00](data/reports/stocks/intraday/2026-08-25_17-00_stocks_intraday_report.md), [catalyst cycle 15:31](data/catalysts/2026-08-25/catalyst_cycle_15-31.md)
- AMD analyst upgrade catalyst: "AMD Stock Upgraded To Strong Buy" — Yahoo Finance Top Stories, surfaced in catalyst cycle 2026-08-25 15:31 (internal ingest, single_source, date as published in feed = 2026-08-25).
- ZRO catalyst: "LayerZero unveils ATLAS platform for builders, testnet coming soon" — CryptoBriefing (internal, via swing report §5); risk pair: "LayerZero to axe 14 low-activity chains after KelpDAO exploit" (internal, via swing report §5).
- SMCI legal risk / BLK legal risk: internal production risk-warning pipeline (stocks intraday report §7, §Production risk warnings) — no external source fetched this cycle (internal record already gates the signal; no candidate decision depended on further verification).
- No external WebSearch/WebFetch performed this cycle — all cited candidates were covered by fresh (<24h), internally consistent records per §G discipline.

## 14. Fix Requests / TODO

### TODO-untracked-alert-recurrence
- **issue:** Untracked Telegram alerts (watchlist_alerts without a matching proposed_signal within ±6h) recurred again today — 8 instances: POL/USDT (scalp 09:51, swing 12:29), PROM/USDT (swing 12:29, intraday 15:21, swing 17:52), INJ/USDT (swing 12:29), ONG/USDT (scalp 16:31, swing 17:52).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-25` output, 2026-08-25 21:xx EEST run.
- **suggested manual fix:** Already tracked as an escalated (high-priority, since 2026-07-17) known bug — watchlist re-fire reuses stale/closed signal_id instead of minting a new proposed_signal. This confirms it is still unresolved as of 2026-08-25; no new action needed beyond keeping the existing TODO-3 priority.
- **priority:** high (pre-existing, confirmed still open)
- **first observed:** 2026-07-17 (this run: reconfirmed 2026-08-25 21:39 EEST)

### TODO-scalp-mode-negative-edge
- **issue:** Crypto scalp mode has a reproducibly negative edge this week: PF=0.07, avgR=-0.076, totalR=-6.50 (n=114, reliable confidence) — worst-performing mode by a wide margin vs intraday (PF 2.36) and swing (PF 1.79).
- **evidence:** `python -m src.cli signal-stats --asset-class crypto`, "By mode" table, week window, run 2026-08-25 21:39 EEST.
- **suggested manual fix:** A human-driven session should review whether this is a short-term drawdown or a structural scalp-mode issue (entry/exit rules, TP ladder, or risk-management gap specific to scalp mode) — compare against the existing risk-management findings in the viable-core / paper-portfolio analysis before any parameter change.
- **priority:** medium
- **first observed:** 2026-08-25 21:39 EEST (this run — recommend a human session check whether this is new or a known/expected pattern for scalp mode specifically, distinct from the broader risk-mgmt gap already tracked)

---
_Advisory only. No auto-trade, no code/scoring changes made during this run._
