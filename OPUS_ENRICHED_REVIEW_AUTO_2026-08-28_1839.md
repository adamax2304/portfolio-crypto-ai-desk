# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

## 1. Executive Summary

**Slot: US open reaction review (advisory only / no auto-trade).** Scheduler is fresh (`scheduler.log` 18:35 EEST, ~4 min old) — no defer. Crypto regime: **range/chop, neutral**, but macro/geopolitical risk stays pinned at 100/100 (Iran sanctions pushback, Strait of Hormuz, Russia missile drills) — a persistent risk-off overlay on an otherwise constructive tape. Zero A-tier crypto signals; the book is structurally **100% long** (signal-stats: n=435, direction=long only, PF 1.37, but triggered winrate only 11.5% — touch-based capture, not a clean win rate). **TRUMP/USDT is today's cleanest long** — RS leader (score 89.2, 24h +8.0%, RS/BTC +9.1%), OI +27.9% confirms fresh positioning, funding not extreme, already has a waiting B-tier swing signal (77.7) and a tp1_hit intraday signal (76.4). **Two open positions carry unresolved bias-tag / price contradictions that need operator eyes now:** (1) **TUT/USDT** — an open *triggered* swing **long** (`sig_c7ce9835f38c40a8`, entry 0.0516-0.0525, invalidation 0.050579) sits against a symbol that has printed **-28% to -29.6% 24h across three consecutive report cycles** (07:59→13:11→15:23 UTC) with an explicit short-squeeze-risk tag — price is almost certainly through invalidation already; this is a **new finding this cycle**, not previously flagged. (2) **ONG/USDT** — the escalated (2026-08-08) bias-tag contradiction continues and is **worsening** (open triggered long `sig_8d3a8fd71bf0bf75`, current tag bias=short, 24h now -13.58% vs -8.18% two cycles ago). Stocks: regime **risk_on**, bias long, VIX 14.4, breadth 100% above EMA50, tech strongest sector — but the **rolling paper-R drawdown guard has demoted every fresh stocks-intraday A/B candidate to C this window** (14d net -5.7R PF 0.39, 7d net -0.2R PF 0.49) — MU (93.4), BX (82.0), V (78.0), NFLX (94.2) all score high but are **not Telegram-actionable**, working as designed, not a bug. **4 untracked legacy crypto alerts today** (MOVR, HEMI×2, CHIP) continue the known watchlist-alert/signal-reuse bug (TODO-3, escalated HIGH 2026-07-17); two of the four (HEMI, CHIP) overlap with today's no-catalyst momentum-breakout basket. Catalyst mapping is weak this run (73.8% unmapped, and the underlying `catalyst_events.jsonl` window is stale — see §5/§14). Scanning, tracking, and the scheduler continue regardless of this window's verdict.

## 2. Data Used

- Crypto scalp report: `data/reports/scalp/2026-08-28_13-11_scalp_report.md` (~5h29m old — carry-forward)
- Crypto intraday report: `data/reports/intraday/2026-08-28_13-47_intraday_report.md` (~4h52m old — carry-forward)
- Crypto swing report: `data/reports/swing/2026-08-28_15-23_swing_report.md` (~16m old — **fresh**)
- Stocks intraday report: `data/reports/stocks/intraday/2026-08-28_14-43_stocks_intraday_report.md` (~56m old — **fresh**)
- Stocks swing/invest reports: both dated 2026-07-02 (~57d stale, deprecated pipeline, excluded)
- `data/processed/llm_analysis_packet.md` (18:26, fresh), `data/processed/llm_stocks_packet.md` (17:47, fresh)
- `data/catalysts/2026-08-28/catalyst_cycle_13-59.md` (latest cycle summary, 500 scanned), `catalyst_events.jsonl` (2000 rows but stale window — see §5), `narrative_baskets.jsonl` (5 baskets)
- `reports/CONTEXT_FILTERS_STATUS.md` (14:36 UTC, fresh) — paper-routing filter/health status
- CLI: `active-signals --asset-class crypto` (50 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-28`
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_1615.md`
- **External web research not used this run** — internal reports/catalyst layer/signal-stats were sufficient and internally consistent for every candidate reviewed within the time budget; nothing here depended on an unverified external claim.
- **TradingView / manual chart check unavailable** — all technical reads taken directly from report-stated OHLCV/ATR/EMA/RS fields.

## 3. Scheduler / Data Freshness

- `scheduler.log`: 2026-08-28 18:35 EEST (~4 min old) — **fresh**.
- No `cycle_*_summary.md` exists yet for today's active cycle folder (`2026-08-28_default_schedule` has no `cycle_*_summary.md` files at all this run — only per-process logs); most recent one anywhere is `2026-08-27_default_schedule/cycle_04_07-14_summary.md` (mtime 2026-08-28 11:17, ~7h22m old). Not used as the defer gate — `scheduler.log` freshness alone clears the rule (only defers when BOTH are >3h stale). Flagged as a data-quality gap (see §14 TODO-cycle-summary-gap).
- Crypto swing: 15:23 UTC — **fresh** (~16m old).
- Crypto intraday: 13:47 UTC — **carry-forward** (~4h52m, inside 4-12h band).
- Crypto scalp: 13:11 UTC — **carry-forward** (~5h29m).
- Stocks intraday: 14:43 UTC — **fresh** (~56m old).
- Stocks swing/invest: 2026-07-02 — **stale**, deprecated pipeline, excluded per prior audits.
- `reports/CONTEXT_FILTERS_STATUS.md` (14:36 UTC): paper routing config `context_filters_v1` **LOCKED**; stablecoin depeg NORMAL; cross-exchange consistency OK (BTC/ETH FULL_SIZE); all context-source health checks `ok`/`ok_provisional` except `stocks_options_import` (`disabled_no_current_file`, non-blocking — options data replaced by the yfinance proxy). No reduce-only / paper-blocking condition active.
- No monitor-process-uptime file was read this run (not in the allowed CLI/read list); no claim made about it beyond the context-filters snapshot above.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-28 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"],
      "data_missing": ["today's cycle_*_summary.md missing", "catalyst_events.jsonl window stale (01:37-09:24 UTC only despite 16:59 mtime)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 18:35", "catalyst_events.jsonl first/last timestamps", "no cycle_*_summary.md in today's folder"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["mixed", "chop", "risk_on", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime range/chop neutral, macro risk 100/100", "stocks regime risk_on, VIX 14.40, breadth 100% >EMA50"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["stale_catalyst", "mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": ["fresh (post-09:24 UTC) catalyst events not captured in catalyst_events.jsonl"],
      "suggested_effect": "advisory_only",
      "facts_used": ["73.8% unmapped in catalyst_events.jsonl", "momentum_breakout basket (HEMI/CHIP/MANTRA) explicitly no-catalyst", "SOL fresh clean catalyst, ZRO catalyst contradicted by price action"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["oi_supports", "funding_extreme"],
      "data_missing": ["no external derivatives cross-check this run (n/a in packet)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/USDT price up + OI up +27.86%, funding 5e-05 (not extreme)", "MANTRA OI +50.53% crowding unknown"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["entry_fresh", "overextended", "chase_risk", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["DEXE/USDT +13% vol 2.59x overextended", "TUT/USDT >2 ATR from EMA20, do-not-chase flag, short-squeeze-risk cap"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review", "review_shadow"],
      "data_missing": ["exhaustive book count beyond the 50-row CLI sample per asset class"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto 50-row sample: 6 waiting, ~34 open/triggered, 10 tp1/tp2-hit running", "stocks 50-row sample: 3 waiting, 7 open/triggered, ~35 legacy tp1/tp2-hit carryover from Aug13-26 window", "0 current/compatible stocks A/B per guard"] },
    { "agent": "risk_manager", "verdict": "bad", "confidence": 0.8,
      "reason_codes": ["manual_review", "correlation_cluster", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT open long vs -28..-29.6% 24h collapse across 3 cycles, invalidation only 2% below entry", "ONG/USDT bias-tag contradiction worsening (-13.58% vs -8.18%)", "crypto book 100% long, 0 audited shorts"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "low_sample", "playbook_working"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp weekly PF 0.10, avgR -0.0865, totalR -9.0", "crypto swing/intraday PF 1.49-1.63, positive", "stocks A/B month sample=142 PF 0.83 (losing), C-tier PF 0.44-0.46 (expected, never actionable)", "stocks A/B week sample=9 anecdotal, do not cite as proof"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.7,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "manual_review",
    "confidence": 0.7,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "TRUMP/USDT", "trigger": "already has waiting B-tier swing entry 2.7908-2.8422 (invalidation 2.7280); RS-leader, OI-confirmed, funding not extreme" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "not an audited short setup, only a bias/failed-bounce tag (score 74, watchlist) — confirm bearish HTF structure break + volume before promoting; note the open LONG contradiction takes priority over any new short entry" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "already triggered swing long (entry ~96.0-96.6); fresh clean catalyst (State-of-Solana platform launch, no contradicting risk tags), ETF-inflow tailwind noted with a historical 20%-pullback caveat" },
    "avoid_candidate":         { "symbol": "TUT/USDT", "reason": "open long contradicts a 3-cycle -28..-29.6% collapse with an explicit squeeze-risk cap; needs operator resolution, not a new position either direction" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | caution | 0.75 | mixed, chop, risk_on, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | stale_catalyst, mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.60 | oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.65 | entry_fresh, overextended, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | caution | 0.70 | open_actionable, waiting_for_entry, needs_review, review_shadow | advisory_only |
| risk_manager | bad | 0.80 | manual_review, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, low_sample, playbook_working | advisory_only |
| head_trader | caution | 0.70 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_1615.md`:
- **New:** TUT/USDT open-long-vs-collapse contradiction (this review's top risk finding — not previously raised in any prior cycle for this specific open position).
- **Confirmed/worsened:** ONG/USDT bias-tag contradiction — now -13.58% 24h (was -8.18% at 16:15, -8.18% before that too across 3+ reviews) — same open long, same unresolved state, escalation stands.
- **New this cycle:** TRUMP/USDT swept up to the #4 RS-leader slot (score 89.2, was not the top idea at 16:15 where HEI/USDT led); HEMI/USDT hit tp2 since the last review (momentum-breakout, no-catalyst basket — a working example of the no-catalyst momentum cohort).
- **Resolved/dropped:** HEI/USDT (16:15's top long idea) no longer appears in the fresh swing report's top-movers list this cycle — carried-forward idea has rolled off; no new status confirmed either way.
- **Resolved:** PYPL / SNOW / VRT (16:15's stocks pre-US candidates) are not in today's fresh stocks-intraday active list — US market is open now and today's fresh cohort is MU/BX/V/NFLX/MRVL/AMD/LMT/RIOT/CLSK/KLAC instead; all guard-demoted to C, none actionable.
- **Unchanged:** crypto book still 100% long; crypto scalp still net-negative (PF 0.10); catalyst mapping still weak (73.8% vs 74.3% prior); untracked-alert bug still firing (4 today vs 1 at 16:15 — MOVR carried over, HEMI×2 and CHIP new).

## 5. Catalyst Coverage

- `catalyst_events.jsonl` (2026-08-28): **2000 total, 523 mapped (26.2%), 1477 unmapped (73.8%)**. **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines: "JAPAN SHOULD NOT RAID ITS FOREX RESERVES..." (macro/FX), "JUDGE BLOCKS KEY PARTS OF TRUMP-BACKED RULE THAT WOULD RESTRICT MAIL-IN VOTING..." (US politics), "PHILIPPINE PESO FALLS AS MUCH AS 0.6%..." (macro/FX) — all macro/political noise, not symbol-mapping regressions.
- **Data-quality caveat:** the events in this file only span **2026-08-28T01:37–09:24 UTC** despite the file's 16:59 UTC mtime — the mapping % above reflects a ~9h-stale window, not the current cycle. The newer `catalyst_cycle_13-59.md` cycle summary (500 events scanned, generated 13:59 EEST) is fresher and was used for narrative-basket / top-catalyst content in §6 instead — see §14 TODO-catalyst-window-gap.
- `narrative_baskets.jsonl`: 5 baskets (delisting_thin_liquidity/BTC, rwa_narrative/ONDO+XLM, perps_dex_narrative/HYPE, binance_ecosystem_teaser/BNB, momentum_breakout/HEMI+CHIP+MANTRA — explicitly no confirmed news catalyst).

## 6. Market Landscape

**Crypto** (swing report, 15:23 UTC): regime **range/chop, neutral risk mode**, confidence 100/100, style "mean reversion or wait for clean breakouts." Breadth: 54.2% above EMA20, 77.1% above EMA50, only 38.3% outperforming BTC. Macro/geopolitical risk stuck at 100/100 (Iran sanctions, Strait of Hormuz, Russia missile-drill headlines) — a real risk-off headwind despite range-bound price action. Top RS leaders: DEXE (95.3, overextended, chase risk), HEMI (91.6, +58.6% 24h, already tp2_hit), EDEN (91.6), **TRUMP (89.2, clean)**, MANTRA (83.9), PROM (83.5). Weakest/short-tag list: ONG (-13.58%, contradicts an open long), ZRO (-8.39%, contradicts a fresh bullish catalyst), **TUT (-29.5%, contradicts an open long)**, BCH/MOVR/JTO/PYTH also weak_vs_market.

**Stocks** (intraday report, 14:43 UTC, US session open): regime **risk_on**, bias long, VIX 14.40 (low/calm), breadth 100% above EMA50, SPY/QQQ/DIA all uptrend, IWM range. Strongest sector: technology (RS +3.78% vs SPY 20d). Weakest: utilities, industrials, real estate. The stocks-intraday rolling paper-R drawdown guard is active and has demoted **every** fresh A/B candidate to C this window (14d net -5.7R PF 0.39, 7d net -0.2R PF 0.49) — this is the guard working as designed against a real losing streak, not a data problem.

### Market Mood / Risk Routing

- Crypto mood: **mixed / chop** (range-bound structure, macro risk-off overlay, but individual RS-leader longs still working — HEMI already tp2_hit)
- Stocks mood: **risk-on** (VIX low, breadth strong, tech leading) but **guard-suppressed** at the signal-actionability layer
- Dominant narrative: momentum-breakout / RS-rotation on the crypto side (HEMI/CHIP/MANTRA, no confirmed catalyst); tech-sector strength + AI-adjacent names on the stocks side; RWA (ONDO/XLM) and perps-DEX (HYPE) baskets simmering but not yet actionable
- Preferred side now: **mixed** — crypto: selective RS-leader longs only (TRUMP/USDT); stocks: watch-only, wait for the guard to clear or an operator override
- Best long candidate: TRUMP/USDT (crypto, RS-leader, waiting-entry B-tier already live)
- Best short candidate: none clean — TUT/USDT is the best short-watch bias tag, but is subordinate to resolving the open long contradiction on the same symbol first
- Best catalyst-backed candidate: SOL/USDT (fresh, clean, already-open swing long; no contradicting risk tags)
- What to avoid: new entries on **TUT/USDT** in either direction until the open-long contradiction is resolved; chasing DEXE/USDT or HEMI/USDT at current extension; new crypto scalp entries (weekly PF 0.10); any stocks-intraday C-tier signal as if it were actionable (MU/BX/V/NFLX all guard-capped)
- What would change the view: operator resolution of TUT/USDT and ONG/USDT open-position contradictions; a fresh (post-09:24 UTC) catalyst-events refresh; the stocks-intraday 7d/14d cohort turning positive again to lift the guard

## 7. Candidate Deep Dives

### 1. TUT/USDT (crypto, **open long contradiction — priority risk**, swing, B-tier score 69.2)
- Signal: `sig_c7ce9835f38c40a8`, status **triggered** (ENTERED, unresolved final outcome), entry 0.051638-0.052505, invalidation 0.050579, expires 2026-09-03.
- Has price already reacted? Yes — violently, against the position: -28.60% (13:11 UTC), -29.58% (13:47 UTC), -29.50% (15:23 UTC) 24h, three consecutive cycles, RS vs BTC -28 to -29%.
- Is the setup chasing? N/A for the open long — the concern is the position itself, not a new entry.
- Retest/pullback structure? None stated; reports explicitly flag "more than 2 ATR from EMA20; do not chase" and a **short-squeeze-risk cap** (`high_upper_wick_short_squeeze_risk`) on the short side.
- Overextended? Yes, >2 ATR from EMA20 per all three reports.
- Would a new entry now be late? Irrelevant — no new entry recommended either direction.
- What level makes it actionable (short side)? Confirmed bearish HTF structure break + volume, per the swing report's own watchlist note; not yet an audited/scored short setup.
- Aligned with market mood? The open long is **not** aligned with current price action at all.
- Long, short, or wait-for-trigger? **Manual review required** — the open long's invalidation (0.050579, only ~2% below entry_low) was almost certainly breached days ago given the magnitude of the move; status still shows "triggered" rather than a closed/stopped outcome.
- What would invalidate it? Already should be invalidated per stated levels — this is a monitor/outcome-recording question, not a new-information question.
- Chase-risk setup? N/A (open position).
- Catalyst confirmation or contradiction? No specific TUT/USDT catalyst found; this is a pure price/RS collapse, unexplained by any single headline in this window.

### 2. ONG/USDT (crypto, open swing long, escalated manual-review carryover)
- Signal: `sig_8d3a8fd71bf0bf75`, triggered 2026-08-26, invalidation 0.09240 — still ENTERED UNRESOLVED.
- Current fresh swing report (15:23 UTC) still tags ONG/USDT **bias=short, 24h -13.58%, RS vs BTC -12.48%** — worse than the -8.18% seen at the 16:15 review, continuing the same internal contradiction flagged across 3+ prior reviews (escalated HIGH 2026-08-08).
- Not re-verified externally this cycle (no new information beyond the worsening bias/price tag) — carried forward as an open, still-unresolved, now-worsening manual-review item.

### 3. TRUMP/USDT (crypto, long, swing/intraday, best clean long this cycle)
- Score 89.2 (RS-leader list), 24h +8.02%, RS vs BTC +9.12%, vol 0.63x. Derivatives: price up + OI up (+27.86%), funding 5e-05 (not extreme) — "fresh positioning confirms trend, monitor crowding," crowding normal.
- Has price already reacted to a catalyst? No single catalyst found; this is RS/momentum + weekly top-gainer status (#4, +63.59% weekly per Telegram digest).
- Is the setup chasing? Moderate — 24h move is material (+8%) but not as extreme as DEXE/HEMI; not flagged overextended in the RS-leader tags.
- Retest/pullback structure? The already-open B-tier swing signal (score 77.7, waiting_for_entry, entry 2.7908-2.8422, invalidation 2.7280) is itself the structured pullback/entry zone.
- Would entry now be late? Not clearly — signal remains in `waiting_for_entry`, not yet filled.
- Aligned with market mood? Yes — RS-leader long in a range/chop regime with OI-confirmed positioning is the playbook's preferred cohort for this regime.
- Long, short, or wait-for-trigger? Long, wait-for-fill in the stated entry zone.
- What would invalidate it? A 1h/4h close through 2.7280, or BTC/ETH breaking the current range to the downside.
- Chase-risk setup? Low at current entry-zone pricing.
- Catalyst confirmation or contradiction? No explicit catalyst; RS/derivatives-confirmed momentum only.

### 4. HEMI/USDT (crypto, swing, already tp2_hit — no-catalyst momentum working)
- Score 91.6 in RS-leader list, 24h +58.59%, RS vs BTC +59.69%, tagged relative_strength/breakout/overextended. Derivatives: price up + OI up (+6.33%), funding 5e-05, crowding normal.
- The `momentum_breakout` narrative basket explicitly states this cluster (HEMI, CHIP, MANTRA) has **no confirmed news catalyst** — pure momentum/volume-driven.
- The open swing signal (`sig_7ecc92d0f4a272bb`, score 72.9) already hit **tp2** — a concrete example of the no-catalyst momentum cohort paying off this cycle.
- Also the subject of **2 of today's 4 untracked legacy alerts** (intraday 73.1 @14:39 UTC, swing 72.9 @15:28 UTC) — these newer alerts fired without a matching `proposed_signal` and will not contribute to PF/winrate tracking (see §9/§14).
- Would a new entry now be late/chasing? Yes — +58.6% 24h, overextended tag present; no fresh entry recommended, this is a "watch the existing win, don't chase more" situation.

### 5. MU (stocks, long, intraday, best-scoring but guard-capped)
- Raw score 93.4, status `waiting_for_entry`, entry 936.4727-943.4700, invalidation 929.4755, tier **C** (guard-capped from what would otherwise likely be A/B).
- Sector technology — today's strongest sector (RS +3.78% vs SPY 20d) — sector alignment is genuinely favorable.
- Is the setup chasing? Cannot fully assess without a fresh RVOL/premarket read beyond the report; not flagged overextended in the packet excerpt reviewed.
- Actionable now or after confirmation? **Not actionable** regardless of price action — the stocks-intraday rolling paper-R drawdown guard (14d net -5.7R PF 0.39) demotes every fresh A/B to C this window; per standing hardening, C-tier is never Telegram-actionable.
- What would make it actionable? Either the guard's 7d/14d cohort recovering to a positive read, or an explicit operator override — not a price-level trigger.
- Legal/headline risk? None found in the stocks packet's ticker-specific news or fresh-SEC/legal (48h) sections for MU.
- Catalyst confirmation or contradiction? None specific to MU this cycle — pure sector-strength/technical score.

## 8. Best Candidates Ranked

1. **TUT/USDT** (manual review, urgent) — open long contradicting a 3-cycle -28..-29.6% collapse; resolve before any new action on this symbol.
2. **ONG/USDT** (manual review, escalated) — open long, bias-tag contradiction worsening (-13.58% vs -8.18%); existing invalidation 0.09240 stands.
3. **TRUMP/USDT** (long-watch) — cleanest fresh long this cycle; wait for fill in 2.7908-2.8422, invalidation 2.7280.
4. **SOL/USDT** (catalyst-watch, already open) — fresh clean catalyst, no contradicting tags; existing swing long stands.
5. **MU** (stocks, watch-only) — highest raw stocks score this cycle (93.4) but guard-capped to C; not actionable until the cohort clears or an operator overrides.

## 9. Avoid / No Trade (this decision window only)

- **TUT/USDT — new entries either direction.** The open long needs operator resolution first; do not add a short on top of an unresolved long in the same symbol.
- **Chasing DEXE/USDT or HEMI/USDT at market** — both overextended (+13%/+58.6% 24h respectively).
- **New crypto scalp entries** — weekly PF 0.10, net-negative bucket; scanner continues, no new entries this window.
- **Any stocks-intraday C-tier signal treated as actionable** — MU/BX/V/NFLX/MRVL/AMD/LMT/RIOT/CLSK/KLAC are all guard-capped C this cycle; none are Telegram-actionable regardless of raw score.
- **ONG/USDT** — no new long or short action pending operator resolution of the bias-tag contradiction.
- This is a decision-window verdict only — scanning, candidate generation, tracking, and the scheduler continue in all cases; nothing here recommends pausing any part of the system.

## 10. Main Risks

- **TUT/USDT open long vs. a -28..-29.6% 24h collapse (new finding this cycle)** — the position's stated invalidation is only ~2% below entry, so price is almost certainly through it already while the signal still reads "triggered"; needs an operator/monitor check on why the outcome hasn't resolved.
- **ONG/USDT bias-tag contradiction, still unresolved and worsening** — open triggered swing long tagged bias=short, now -13.58% (was -8.18%), escalated HIGH since 2026-08-08.
- **Crypto book remains 100% long, 0 audited shorts** — expected given no scored short candidate exists, but a real concentration risk if BTC/ETH break the current range down.
- **Crypto scalp underperformance continues** — weekly PF 0.10, avgR -0.0865, totalR -9.0R.
- **Catalyst mapping weak (73.8% unmapped) AND the underlying events file appears stale/capped** (spans only 01:37-09:24 UTC despite a 16:59 mtime) — treat the catalyst layer as context only this run; see §14.
- **4 untracked legacy crypto alerts this cycle** (MOVR, HEMI×2, CHIP) — consistent with the known recurring watchlist-alert/signal-reuse bug (TODO-3, escalated HIGH 2026-07-17); 2 of the 4 overlap with today's working no-catalyst momentum basket.
- **No `cycle_*_summary.md` for today's active scheduler folder** — freshness gate still passed via `scheduler.log`, but the summary artifact itself appears to not be generating this cycle; see §14.

## 11. Action Plan — next 4 hours

- Flag TUT/USDT for immediate operator review: confirm whether the open long has already been stopped out and simply not recorded, or whether the monitor is genuinely still holding a position deep through invalidation.
- Continue tracking ONG/USDT's bias-tag contradiction; no new action on the existing invalidation (0.09240).
- Watch TRUMP/USDT for a fill in 2.7908-2.8422; do not chase above the zone.
- Hold SOL/USDT's existing swing long; no new action needed, catalyst remains clean.
- Do not treat any stocks-intraday C-tier candidate (MU, BX, V, NFLX, MRVL, AMD, LMT, RIOT, CLSK, KLAC) as actionable this window; re-check the 7d/14d guard cohort at the next cycle (21:30 late-session risk review).
- No new crypto scalp entries this window (weekly PF 0.10).
- Re-check the untracked-alert count and catalyst-events.jsonl freshness at the next cycle.

## 12. Final Verdict per Mode

- **Crypto scalp:** carry-forward (~5.5h); weekly PF 0.10 (losing bucket) — scanner continues, no new entries this window.
- **Crypto intraday:** carry-forward (~4.9h); TRUMP/USDT tp1_hit is the standout; no new A/B setups flagged this cycle beyond the existing book.
- **Crypto swing:** fresh (~16m); TRUMP/USDT is the one fresh clean actionable idea (wait-for-fill); TUT/USDT and ONG/USDT need manual review, not new action.
- **Stocks intraday:** fresh (~56m), US session open, risk-on regime, but 0 A/B actionable — every fresh candidate guard-capped to C (MU, BX, V, NFLX, MRVL, AMD, LMT, RIOT, CLSK, KLAC); working as designed.
- **Stocks swing:** stale (2026-07-02) — excluded, deprecated pipeline.
- **Stocks invest:** stale (2026-07-02) — excluded, deprecated pipeline.

## 13. Sources

- Internal: `data/reports/swing/2026-08-28_15-23_swing_report.md`, `data/reports/intraday/2026-08-28_13-47_intraday_report.md`, `data/reports/scalp/2026-08-28_13-11_scalp_report.md`, `data/reports/stocks/intraday/2026-08-28_14-43_stocks_intraday_report.md`, `data/processed/llm_analysis_packet.md`, `data/processed/llm_stocks_packet.md`, `data/catalysts/2026-08-28/catalyst_cycle_13-59.md`, `data/catalysts/2026-08-28/catalyst_events.jsonl`, `data/catalysts/2026-08-28/narrative_baskets.jsonl`, `reports/CONTEXT_FILTERS_STATUS.md`.
- CLI: `active-signals --asset-class crypto`, `active-signals --asset-class stocks`, `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-28`.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-28_1615.md`.
- No external WebSearch/WebFetch performed this run (date unavailable for none of the above — all internal timestamps present and consistent).

## 14. Fix Requests / TODO

### TODO-tut-invalidation-unresolved
- **issue:** Open swing long `sig_c7ce9835f38c40a8` (TUT/USDT, entry 0.051638-0.052505, invalidation 0.050579) still shows status `triggered` despite the symbol printing -28.60% (13:11 UTC), -29.58% (13:47 UTC), -29.50% (15:23 UTC) 24h across three consecutive report cycles — invalidation is only ~2% below entry, so price is almost certainly through it already.
- **evidence:** `active-signals --asset-class crypto` row `sig_c7ce9835f38c40a8`; `data/reports/swing/2026-08-28_15-23_swing_report.md:48` ("TUT/USDT: bias short, 24h -29.50%"); same pattern at `data/reports/intraday/2026-08-28_13-47_intraday_report.md:48` (-29.58%) and `data/reports/scalp/2026-08-28_13-11_scalp_report.md:50` (-28.60%).
- **suggested manual fix:** a human-driven session should query the exact current TUT/USDT price and the position monitor's state directly, confirm whether the stop was actually hit and simply not yet recorded as a `signal_outcome`, and if so investigate why the monitor didn't close/record it.
- **priority:** high
- **first observed:** 2026-08-28 18:39 EEST

### TODO-catalyst-window-gap
- **issue:** `data/catalysts/2026-08-28/catalyst_events.jsonl` (mtime 16:59 UTC) only contains events timestamped 2026-08-28T01:37-09:24 UTC — a ~9h gap between the file's last event and its last write, despite the pipeline running multiple fresher cycles (`catalyst_cycle_13-59.md` exists and is fresher). The file appears to be a rolling/capped buffer (exactly 2000 lines) that has fallen behind.
- **evidence:** direct read of first/last `published_at` values across all 2000 lines in `catalyst_events.jsonl` vs. file mtime; `catalyst_cycle_13-59.md` (fresher, 500 events scanned, generated 13:59 EEST) used instead for narrative content in this review.
- **suggested manual fix:** a human-driven session should check whether `catalyst_events.jsonl`'s buffer size/rotation logic is capping it below the actual daily event volume, and whether the mapped/unmapped % reported to Opus reviews should instead be computed from the latest `catalyst_cycle_*.md` cycle summary rather than the full-day jsonl.
- **priority:** medium
- **first observed:** 2026-08-28 18:39 EEST

### TODO-cycle-summary-missing
- **issue:** No `cycle_*_summary.md` file exists in today's `data/scheduled_runs/2026-08-28_default_schedule/` folder at all this run, despite the scheduler having been running since early morning (per-process logs like `derivatives_monitor_*.log`, `fast_news_monitor_*.log` are present and fresh, but no cycle summary artifact).
- **evidence:** `ls data/scheduled_runs/2026-08-28_default_schedule/` — only `.log` files present, no `cycle_*_summary.md`; most recent summary anywhere is in yesterday's folder (`2026-08-27_default_schedule/cycle_04_07-14_summary.md`, mtime 2026-08-28 11:17).
- **suggested manual fix:** a human-driven session should check whether the cycle-summary-generation step is still wired into today's scheduler run or was silently dropped/broken this cycle.
- **priority:** low
- **first observed:** 2026-08-28 18:39 EEST

### TODO-untracked-alerts-recurring (carryover, still open)
- **issue:** 4 untracked legacy crypto alerts today (MOVR/USDT 12:03, HEMI/USDT 14:39 + 15:28, CHIP/USDT 15:28) — same recurring watchlist-alert/signal-reuse bug escalated to HIGH priority 2026-07-17 (project memory: `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug`). Not a new issue, but still unresolved and firing today.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-28` output.
- **suggested manual fix:** see prior TODO-3 — investigate why these alerts reuse a stale/closed `signal_id` instead of minting a new `proposed_signal`.
- **priority:** high
- **first observed:** 2026-07-17 (recurring; observed again 2026-08-28 18:39 EEST)
