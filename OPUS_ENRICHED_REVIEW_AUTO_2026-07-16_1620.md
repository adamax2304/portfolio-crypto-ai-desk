# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (~10 min before the 16:30 EEST / 09:30 ET US cash open), run at **16:20-16:32 EEST, 2026-07-16**. **Advisory only — no auto-trade, no code/scoring/routing changes.** Data pipeline is fully healthy this cycle: cycle 4 (14:11-14:43 EEST) completed **59/59 steps, 0 failures** — the stocks-intraday timeout that broke the previous (13:26 EEST) review has **resolved**; fresh stocks data is ~1h50m old, fresh crypto scalp/intraday ~2h old. **No A-tier signal exists in either asset class right now** — crypto scalp mode is globally kill-switched off (structurally negative playbook, unchanged), crypto intraday produced **zero A/B** this cycle (only 4 C-tier watchlist names: ORDI, KITE, ONDO, ALLO), and stocks intraday produced a strong A-tier *score* set (AAPL 91.0, JPM 89.5, AMZN 85.3, META 84.8, XLE 84.3, GOOGL 84.0, XOM 83.4) that the desk correctly demoted to C via `market_closed_intraday_planning_only` — the market was still closed when the report ran (14:37 EEST) and **opens in minutes from this review's timestamp**; these are the pre-open watchlist, not yet actionable. **Fresh, externally-confirmed geopolitical escalation continues**: US reinstated its Iran blockade and disabled the tanker *Belma*; Iran struck Bahrain and Kuwait with drones/missiles (intercepted) — a genuine widening, not headline recurrence. Crypto has so far absorbed this without a breakdown (BTC ~-0.3%, ETH +2%, external confirmation). **UNH reported Q2 earnings before this review** — beat on revenue/EPS and raised FY26 guidance, +6% premarket — but the DOJ Medicare-billing probe remains unresolved, so per the legal-risk rule this stays **AVOID / MANUAL REVIEW**, not a clean actionable long, despite the green tape. **NFLX reports after today's close** (not yet reported) — still a do-not-chase name pre-print. Nasdaq futures are soft (~-1%) on continued TSMC-capex-driven semiconductor weakness, S&P/Dow closer to flat-to-mixed. Catalyst mapping is weak this run (19.6% mapped / 80.4% unmapped, direct count — context only, largely whale-transfer/mint noise). Untracked legacy crypto alerts: **0** (clean). All 4 monitors healthy.

## 2. Data Used

- Reports: `2026-07-16_11-19_scalp_report.md` (crypto scalp, ~2h05m old, mode kill-switched off); `2026-07-16_11-26_intraday_report.md` (crypto intraday, ~1h58m old, regime range/chop); `2026-07-16_02-27_swing_report.md` (crypto swing, ~10h57m old, carry-forward band, regime bullish trend at the time it ran — cooler now per fresher scalp/intraday reads); `2026-07-16_11-37_stocks_intraday_report.md` (stocks, ~1h47m old, generated pre-open, market-closed caps active — about to lift at the open).
- Stocks swing/invest: last file `2026-07-02_13-03` / `2026-07-02_13-05` — **14 days old, STALE, excluded**. Per project memory these old `stocks_swing_watchlist_rs_rotation` / `stocks_invest_watchlist_30d_thesis` playbooks are DEPRECATED/REMOVED (poor forward performance); the replacement `stocks_swing_growth_breakout` framework is shadow-only research (1 open candidate, AAPL reclaim_after_shakeout 77.0) and out of scope for actionability in this slot.
- LLM packets: `data/processed/llm_analysis_packet.md` (crypto, ~1h58m fresh); `data/processed/llm_stocks_packet.md` (stocks, ~1h47m fresh).
- Catalyst / narrative: `data/catalysts/2026-07-16/catalyst_events.jsonl` (direct count: 392/2,000 mapped = 19.6%; report's dedup count: 717 unique events, 5 baskets) and `narrative_baskets.jsonl` for `2026-07-16`.
- CLI: `active-signals` (crypto ×8, stocks ×50 total / ×18 B-tier with full detail pulled), `signal-stats` (crypto: A/B headline PF 1.48 n=168 reliable; stocks: A/B headline PF 0.40 n=17 weak, C-tier PF 0.59 n=215), `detect_untracked_legacy_alerts --since 2026-07-16` (0 results — clean).
- Trade-idea agent outputs: `20260716_112609_trade_idea_agent.json` (crypto, 15 ideas: 4 watchlist-C, 11 rejected, zero A/B); `20260716_113658_stocks_stock_trade_idea.json` + `20260716_113657_stocks_stock_scoring.json` (stocks, full A-tier-score/C-tier-actionable list).
- `data/scheduled_runs/2026-07-16_default_schedule/cycle_04_14-11_summary.md` — 59/59 ok, paper monitor status (#57), scheduler.log mtime 15:30 EEST.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-16_1326.md` (mislabeled "post-close", actually dispatched at 13:26 EEST pre-open) — used for §4 comparison.
- **External web research performed** (needed to verify whether today's UNH/NFLX earnings had landed, whether the Iran/Bahrain escalation continued or cooled since 13:26 EEST, and to check severity of an AAPL political-pressure headline before treating it as a legal-risk block):
  - WebSearch: "US stock market futures pre-market July 16 2026 S&P Nasdaq Dow NFLX UNH earnings" — confirmed UNH beat (rev $112.0B vs $110.8B est, adj EPS $6.38 vs $4.85 est, FY26 guidance raised to $19.50-$20.00, stock +6% premarket); confirmed NFLX reports **after today's close**, not yet reported; confirmed Nasdaq 100 futures ~-1%, S&P mixed/slightly soft, Dow ~flat on continued chip-sector weakness after TSMC's capex-heavy guidance.
  - WebSearch: "Iran Hormuz Bahrain Kuwait tanker Belma military escalation July 16 2026" — confirmed the blockade reinstatement and tanker *Belma* disabling near Kharg Island are real and current; confirmed Iran's retaliatory strikes on Bahrain/Kuwait (intercepted, no reported casualties on the US/allied side) are a genuine widening beyond the naval standoff, still active as of this review.
  - WebSearch: "Bitcoin Ethereum price reaction July 16 2026 Iran escalation safe haven risk-off" — confirmed BTC ~-0.34% to ~$64.7k, ETH +2.07%, both largely absorbing the escalation without a clean breakdown; a further-escalation scenario is flagged by outside analysts as a downside risk toward BTC $62.5k.
  - WebSearch: "Senator Cotton Apple blacklisted Chinese chips warning July 2026" — confirmed this is an ongoing political-pressure story (Apple lobbying to buy memory chips from Pentagon-blacklisted CXMT/YMTC amid a memory shortage; Cotton and other senators objecting) dating to late June/early July — **not** an indictment, SEC/DOJ investigation, or class action against AAPL; classified as background regulatory-risk noise, not a hard legal-risk block.
  - No WebFetch needed this cycle — all four WebSearch syntheses were directly usable with named, dated sources; no single result needed deeper verification via page fetch.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 15:30 EEST (~1h escaped since; ~54min old at review start), `cycle_04_14-11_summary.md` mtime 14:43 EEST (~1h49m old at review start) — both well under the 3h defer threshold. **Not deferred.**
- Cycle 4: **ok=59, failed=0** — full clean run (14:11-14:43 EEST), including crypto scalp, crypto intraday, stocks intraday, all CLI diagnostics, paper monitor, and obsidian refresh. This resolves the stocks-intraday-timeout problem flagged in the 13:26 EEST review (3 consecutive timeouts then; 0 timeouts this cycle).
- Crypto scalp (~2h05m old, mode kill-switched, structurally negative playbook — data-collection only) / intraday (~1h58m old, regime range/chop, macro risk 100/100) fresh this cycle; crypto swing (~10h57m old, 02:27 EEST) is carry-forward band (4-12h) — used but flagged: its `bullish trend (risk-on)` read is now the cooler `range/chop` per the fresher scalp/intraday reports.
- Stocks intraday (~1h47m old, 14:37 EEST) fresh this cycle but generated **while the market was still closed** — every A-tier-score candidate carries a `market_closed_intraday_planning_only` cap to C; this cap should lift automatically once RTH data flows in after the 16:30 EEST open, but that has not happened as of this review (dispatched ~10 min before the open by design).
- Monitors: all 4 (crypto, pending, stocks, derivatives) healthy, restarted at cycle start per the log.
- Paper Monitor Status (cycle 4, #57, telegram): **Open actionable: 0 · Waiting for entry: 0 · Entered unresolved: 0 · Review/Shadow: 25 · No-entry/stale/moved-away: 18 · Closed today: 204W / 24L / 122flat · Needs review: 0.**
- Untracked legacy crypto alerts: **0** (clean, consistent with the last review — the recurring TODO from mid-July appears durably resolved).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-16 16:32 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["RTH-confirmed stocks price action (market not yet open at review dispatch)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_04 59/59 ok, 0 failed, finished 14:43 EEST", "crypto scalp/intraday <2h05m old, stocks intraday ~1h47m old", "crypto swing ~10h57m old, carry-forward band, used with regime-drift flag", "stocks swing/invest 14 days old, stale/deprecated, excluded"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "chop", "wait_for_trigger", "risk_off"], "data_missing": ["post-open stocks regime read"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC range, ETH uptrend, breadth 57.4%/59.6% above EMA20/50, macro risk 100/100 on genuine fresh Iran/Bahrain/Kuwait escalation", "external: BTC -0.34%, ETH +2.07%, absorbing the escalation without a clean breakdown", "stocks: regime label chop, bias neutral, VIX 16.09 (not elevated), breadth 75%/100% above EMA20/50", "Nasdaq futures ~-1% pre-open on continued TSMC-capex-driven chip weakness; S&P/Dow closer to flat"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "narrative_supported", "catalyst_contradicted"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl today: 392/2,000 mapped (19.6% direct count), 717 unique events / 5 baskets per report dedup", "top unmapped headlines are whale-transfer/USDC-mint alerts and generic macro, not tradeable per-symbol signal", "active baskets: rwa_narrative (ONDO/XLM), perps_dex_narrative (HYPE), binance_ecosystem_teaser (BNB), delisting_thin_liquidity, momentum_breakout (ONDO)", "UNH: strong earnings-beat catalyst directly contradicted by an unresolved DOJ legal-risk flag — classic contradiction case"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.55,
      "reason_codes": ["oi_supports", "squeeze_risk", "data_unavailable"], "data_missing": ["derivatives for several MEXC-only weak_vs_market names"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONDO/VIRTUAL: price up + OI up, fresh positioning confirms trend, crowding normal", "ALLO/ETH: price up + OI down, short covering, weaker continuation quality", "MUB/SKHYB explicitly flagged thin_liquidity_short_squeeze_risk in the scalp report — not clean shorts"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chase_risk", "entry_late", "stale_before_entry", "waiting_for_entry"], "data_missing": ["post-open confirmation for every stocks candidate"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT: momentum score 93.6 but scalp report explicitly flags 'more than 2 ATR from EMA20 — do not chase', converted to watchlist-only", "AAPL/JPM/AMZN/META/XLE/GOOGL/XOM: all pre-gate A-tier score, all capped to C purely on market_closed_intraday_planning_only — needs RTH confirmation, not a data-quality problem", "AMD: A→C on catalyst_none_and_not_exceptional_technical + first_15m_requires_orb_or_opening_drive — genuinely needs the opening range before it's tradeable"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["waiting_for_entry", "no_entry", "review_shadow", "closed_flat"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Paper Monitor: open_actionable=0, waiting_for_entry=0, entered_unresolved=0, review_shadow=25, no_entry/stale/moved_away=18, needs_review=0, closed_today=204W/24L/122flat", "crypto: 8 active B-tier signals, several already tp1_hit/tp2_hit (ONDO, ALLO, VIRTUAL x2, XLM)", "stocks: several B-tier signals from 2026-06-05 through 2026-07-08 carry expires_at timestamps already in the past while still shown tp1_hit/tp2_hit/triggered — lifecycle-closing hygiene question, see TODO"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ Medicare-billing/Optum Rx probe unresolved (last confirmed 2026-07-14) STACKED with a genuine positive earnings surprise today (+6% premarket) — contradiction, legal risk wins per policy, AVOID/MANUAL REVIEW for fresh exposure", "NFLX: earnings after today's close, do_not_chase_warning active pre-print, no open signal", "IBM: low-materiality shareholder-solicitation notice (Levi & Korsinsky boilerplate), not confirmed material, background only", "AAPL: Cotton/CXMT political-pressure story is background regulatory noise, not an indictment/SEC/DOJ/class-action — does not rise to a hard legal-risk block", "geopolitical: Iran/Bahrain/Kuwait escalation externally confirmed as continuing and real, macro risk 100/100 justified"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly headline: PF 1.48, n=168 reliable, winrate 21.2%", "crypto scalp mode PF 0.25 (mode=1st row, n=40) structurally negative, kill-switched — consistent, unchanged", "stocks weekly headline A/B: PF 0.40, n=17 weak-confidence, winrate 23.5% — do not over-trust a fresh stocks A/B this week even once RTH confirms", "stocks C-tier: PF 0.59, n=215 reliable — watchlist tier remains a drag, informational only"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of the eight agents above; the desk is data-healthy and the mood is not a hard no-trade, but literally nothing is RTH-confirmed yet at 16:32 EEST (open is 16:30 EEST) — the honest read is watch-and-confirm-at-open, not a stocks entry signal this exact minute; crypto has clean C-tier watchlist names but no A/B"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "AAPL", "trigger": "pre-gate A-tier score 91.0 (RS leader +10.5% vs SPY / +15.8% vs sector, 8 catalysts, long zone 326.17-327.57, invalidation 324.77) capped to C only by market_closed_intraday_planning_only — re-confirm on the first 15-30min of RTH before treating as live; do not chase if already >2 ATR extended at the open" },
    "best_short_candidate":    { "symbol": "AMD", "trigger": "A→C on catalyst_none + first_15m_requires_orb_or_opening_drive, aligned with the overnight Asia/TSMC-capex semiconductor weakness (external confirmation) — wait for the opening 15-30min range and a clean retest, do not chase the overnight gap" },
    "best_catalyst_candidate": { "symbol": "UNH", "trigger": "genuine primary-source beat-and-raise catalyst (rev/EPS beat, guidance raised, +6% premarket) but BLOCKED by an unresolved DOJ Medicare-billing probe — manual review required, not a clean actionable long despite the green tape" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "DOJ probe unresolved stacked with a large earnings-day gap — do-not-chase regardless of the fundamentally strong print" },
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
| market_regime | caution | 0.65 | mixed, chop, wait_for_trigger, risk_off | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, catalyst_confirmed, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | ok | 0.55 | oi_supports, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, entry_late, stale_before_entry, waiting_for_entry | advisory_only |
| execution_lifecycle | ok | 0.80 | waiting_for_entry, no_entry, review_shadow, closed_flat | advisory_only |
| risk_manager | caution | 0.70 | legal_risk, headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (2026-07-16 13:26 EEST, mislabeled "post-close")

- **Stocks pipeline fully recovered**: 3 consecutive timeouts (05:03/08:50/12:07 UTC) → cycle 4 completed 59/59 with 0 failures and a fresh stocks-intraday report (14:37 EEST). This was the previous review's #1 risk; it is resolved.
- **This run's slot label matches its dispatch time** — no repeat of the previous "post-close label at a pre-open dispatch time" mismatch; this run is genuinely the 16:20 pre-US-open slot.
- **Review-schedule gap confirmed, not yet explained**: only one review exists for today before this one (13:26 EEST) — the 04:30 and 11:30 EEST slots produced no `OPUS_ENRICHED_REVIEW_AUTO_2026-07-16*.md` file. Carried forward as a TODO; cannot be diagnosed from inside this run (scheduler internals are out of scope).
- **UNH earnings landed since the last review**: beat on revenue/EPS, raised FY26 guidance, +6% premarket — new information not available at 13:26 EEST. Does **not** change the AVOID verdict (DOJ probe still unresolved) but the reasoning is now sharper: a contradiction case (bullish print vs. unresolved legal risk), not a plain do-not-chase-earnings case.
- **NFLX not yet reported** (after today's close) — unchanged from 13:26 EEST, still do-not-chase pre-print.
- **Crypto regime**: still range/chop (fresher intraday read confirms the 13:26 EEST "cooling from risk-on" call); macro risk still pinned at 100/100 on the same, still-active Iran/Bahrain/Kuwait escalation — externally confirmed to still be live, not resolved or further escalated dramatically since 13:26 EEST.
- **Catalyst mapping**: 19.6% mapped this run (direct count) vs. 17.3% at 13:26 EEST — persistently weak, consistent pattern, not new.
- **AAPL/JPM/AMZN/META/XLE/GOOGL/XOM all carry fresh A-tier-score classifications** from the 14:37 EEST stocks report (vs. the 13:26 EEST review, which had zero fresh stocks classification at all due to the outage) — this is new, actionable-pending-RTH information this cycle.
- **Untracked legacy crypto alerts**: still 0, confirming the fix holds.

## 5. Catalyst Coverage

- Total catalyst_events rows today (direct JSONL count): **2,000** — mapped (non-null symbol): **392** (19.6%), unmapped: **1,608** (80.4%). Report's own dedup figure: **717 unique events**, **5** active narrative baskets.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headline types (sampled): (1) large whale wallet-transfer/mint alerts (e.g., "$117.6M USDT transferred from Bitfinex to Tether Treasury", "$250M USDC minted at USDC Treasury") — routine flow noise, not symbol-specific tradeable signal; (2) generic macro/geopolitical headlines without a clean ticker match (e.g., Strait of Hormuz, CLARITY Act commentary); (3) new-pair-listing alert lists spanning many tickers at once (Binance Spot tokenized-equity pairs) that the resolver doesn't attribute to a single symbol.
- Active narrative baskets: **rwa_narrative** (ONDO/USDT, XLM/USDT, playbook `related_beta_rotation`, fresh <6h); **perps_dex_narrative** (HYPE/USDT, playbook `wait_pullback`, fresh <1h); **binance_ecosystem_teaser** (BNB/USDT, playbook `related_beta_rotation`, fresh <24h); **delisting_thin_liquidity** (no primary, playbook `avoid_low_liquidity`); **momentum_breakout** (ONDO/USDT, playbook `wait_pullback`, fresh <1h).
- Notable mapped events: ETH exploit cluster this week (Ostium $18-23.75M oracle-manipulation hack laundered via Tornado Cash, Prism relaunch after an exploit, Summer.fi $6M vault exploit wind-down) — a real, elevated DeFi-hack backdrop touching ETH-adjacent narratives, not a fundamental ETH sell signal but worth a caution flag on DeFi-correlated ETH exposure.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed, absorbing elevated but not new geopolitical risk** — BTC range/chop (~-0.3% today, external), ETH uptrend (+2.1%, external, outperforming on Japan-regulatory/staking-institutional narratives), altcoin breadth 57.4%/59.6% above EMA20/50 (modest positive tilt, not strong risk-on), macro risk 100/100 on the still-active US-Iran/Bahrain/Kuwait escalation (externally confirmed as genuinely ongoing, not recurring-headline inflation). No A-tier anywhere; crypto scalp mode is globally off.
- Stocks mood: **chop, neutral bias, pre-open** — regime label chop, VIX 16.09 (not elevated — no fear-driven risk-off), breadth 75%/100% above EMA20/50 (healthier than the chop label alone suggests), Nasdaq futures ~-1% (chip-sector drag from TSMC's capex-heavy guidance), S&P/Dow closer to flat. Financials/healthcare/energy are the strongest sectors (20d RS); semis/tech/materials the weakest — directly consistent with the AMD/semis short-watch thesis.
- Dominant narrative: crypto — RWA (ONDO/XLM) and perps-DEX (HYPE) baskets are the freshest live narratives; stocks — the semiconductor unwind continuing from TSMC's earnings-day guidance (capex up, margin-worry framing) is the story walking into the open, alongside UNH's beat-vs-legal-risk contradiction.
- Preferred side now: **wait-for-trigger into the open, asset-class-specific** — stocks because literally every A-tier-score name is still capped on `market_closed_intraday_planning_only` at review time (open is essentially concurrent with this review); crypto because there is no A/B to act on, only C-tier watchlist.
- Best long candidate: AAPL (stocks, pre-gate A-tier 91.0, RS leader, capped only by the market-closed gate — needs first-15-30min RTH confirmation).
- Best short candidate: AMD (stocks, A→C on catalyst/ORB caps, aligned with confirmed overnight semiconductor weakness — needs opening-range confirmation, not a chase of the overnight gap).
- Best catalyst-backed candidate: UNH (stocks) — genuine beat-and-raise, but legal risk overrides: **not actionable**, manual review only.
- What to avoid: UNH (DOJ probe + earnings-gap chase risk, despite the beat); NFLX (reports after close, do-not-chase pre-print); BANK/USDT (crypto, momentum score 93.6 but explicitly >2 ATR from EMA20 in the scalp report — do not chase); any crypto short on MUB/SKHYB (thin-liquidity, short-squeeze-risk capped).
- What would change the view: RTH price action and volume in the first 15-30 minutes after the 16:30 EEST / 09:30 ET open (the single biggest unknown right now); further Iran/Bahrain/Kuwait escalation or a de-escalation signal; NFLX's after-close print; a pullback/retest forming on ONDO/USDT (currently extended, momentum score 90.8, RS +16.5% vs BTC) that would make the RWA-basket long thesis actionable rather than a chase.

## 7. Candidate Deep Dives

### 1. AAPL — stocks, long, best long-watch (pre-gate A-tier, market-closed capped)
- Score 90.98 (pre-gate tier A, final tier **C** via `market_closed_intraday_planning_only`), long zone 326.17-327.57, invalidation 324.77, TP1/2/3 331.77/334.57/338.77 (RR to TP1 1.5, ATR-measured).
- Has price already reacted to the catalyst? Partially — 8 news catalysts in the lookback window (Broadcom-supplier commentary from Tim Cook, Motley Fool "$5T market cap" prediction pieces); mostly opinion/secondary-source, not a single hard primary catalyst — this is primarily an RS/technical setup (RS vs SPY +10.5%, vs sector +15.8%, classification "leader") with catalyst support, not a catalyst-led trade.
- Chasing? Cannot fully assess pre-open; ATR extension at classification time was 2.3x (already at the edge of the "clean entry" band) — watch for the opening print relative to the 326.17-327.57 zone; if price gaps well above 327.57 at the open, this becomes a chase and should wait for a retest.
- Retest/pullback structure? Unknown until RTH prints; treat the printed zone as a reference level, not a live order.
- Overextended (>2 ATR from EMA20)? Borderline (2.3x ATR extension at classification) — flag, do not oversize.
- Would entry now be late? Not applicable pre-open; the question is whether the opening print respects or blows through the zone.
- Legal/headline check: **Cotton/CXMT chip-sourcing political pressure** confirmed as a real, ongoing story (Apple lobbying to buy memory from blacklisted Chinese chipmakers amid a memory shortage) — background regulatory-risk noise, not an indictment/SEC/DOJ probe/class action; does **not** meet the §I bar for a hard AVOID, but worth watching if it escalates toward actual Commerce Department entity-list action.
- Mood alignment: technology sector is mixed/weak in the 20d RS read (XLK -5.3% vs SPY) — AAPL's own RS is a leader *within* a weak sector, a genuine idiosyncratic-strength case rather than sector-driven momentum; worth noting the sector itself isn't confirming.
- Is this a chase-risk setup? Borderline, per the ATR-extension flag above.
- **Verdict: WATCH — re-confirm on the first 15-30min of RTH before treating as live. If the open respects the printed zone (326.17-327.57) without a gap-and-run, this is the cleanest long-watch on the desk right now; if it gaps away, wait for a retest rather than chasing.**

### 2. AMD — stocks, short, best short-watch (A→C on ORB/catalyst caps, sector-aligned)
- Score 90 (pre-gate A), final tier **C** via `market_context_unknown_or_stale`, `first_15m_requires_orb_or_opening_drive`, `liquidity_rvol_below_min`, `catalyst_none_and_not_exceptional_technical` — this is the stocks-intraday actionability gate correctly demanding the opening range before treating a semis-sector short as live.
- Has price already reacted? Directionally, yes at the sector level — confirmed overnight Asia semiconductor selloff (Nikkei -3.6% per the internal report; external search confirms TSMC's capex-heavy 2026 guidance, not a demand miss, is driving the "AI-valuation-worry" framing) and Nasdaq futures ~-1% pre-open on the same theme.
- Chasing? Would be, if entered on the overnight gap alone — the caps correctly require the opening 15-30min range (ORB) before confirming direction.
- Retest/pullback structure? Not yet formed — needs RTH data.
- Legal/headline/catalyst check: no AMD-specific negative catalyst; this is pure sector/macro weakness (TSMC guidance read-through), not company news.
- Mood alignment: strongly aligned — semiconductors are the weakest 20d-RS sector (SMH -8.7% vs SPY) in the current stocks regime read, and the overnight Asia action reinforces it.
- **Verdict: SHORT-WATCH. Directionally well-supported by sector weakness and confirmed overnight Asia action, but the specific entry needs the opening-range confirmation the system's own gate is requiring — do not chase the overnight gap.**

### 3. UNH — stocks, contradiction case (beat-and-raise vs. unresolved DOJ probe)
- No open UNH signal in the actionable B-tier table; a C-tier long (80.0, tp1_hit) and C-tier short (73.6, waiting) both exist as legacy/non-actionable-tier carryovers, not live decision points.
- Has price already reacted to the catalyst? Yes, strongly — Q2 revenue $112.0B vs $110.8B est, adjusted EPS $6.38 vs $4.85 est, FY26 guidance raised to $19.50-$20.00, stock +6% premarket (external, confirmed).
- Legal/headline check: **confirmed** — DOJ Medicare-billing/Optum Rx probe remains unresolved (last confirmed 2026-07-14, stock fell 4.7% on that confirmation). Per §I, a confirmed legal/DOJ risk makes the final verdict AVOID/MANUAL REVIEW regardless of a subsequently strong earnings print — the two facts do not cancel out, they stack as a contradiction the operator should look at directly.
- Chasing? A fresh long here at the open would be chasing a large earnings gap into an unresolved legal overhang simultaneously — doubly risky, not a clean setup either direction.
- Mood alignment: irrelevant to the verdict — this is a hard avoid-for-fresh-entry regardless of the broader stocks mood, given the stacked catalyst-vs-legal-risk contradiction.
- **Verdict: AVOID / MANUAL REVIEW REQUIRED for any fresh exposure. Genuinely the best catalyst print on the desk today, but the unresolved DOJ probe means this is not a clean actionable — flag for a human look at open, do not auto-chase the gap.**

### 4. ONDO/USDT — crypto, long, best catalyst-backed watch (dual-basket, extended)
- C-tier watchlist score 56.2 (trade-idea agent) / momentum score 90.8 (top-movers ranking) — the gap between these two numbers is expected: the momentum/RS ranking is a raw funnel metric, the trade-idea score is the final scored output after full agent analysis; ONDO did not clear the bar for a scored B/A idea despite strong raw momentum.
- Active signal: existing B-tier intraday long, **tp1_hit**, still open (expires 2026-07-17T08:36:31).
- Dual narrative-basket primary: `rwa_narrative` (with XLM) and `momentum_breakout`, both fresh <6h/<1h — the cleanest catalyst-linked crypto name on the desk today.
- Has price already reacted? Yes — 24h +15.75%, RS vs BTC +16.5%, already extended.
- Chasing? A fresh entry now would be chasing; no explicit ">2 ATR" flag was printed for ONDO the way BANK/MUB were, but the extension is real (top-3 mover, volume only 0.22x — extension without volume confirmation is a caution sign, not confirmation).
- Retest/pullback structure? Not established; would need a genuine pullback into a lower zone for a fresh entry to be clean.
- Legal/headline/catalyst check: none negative found for ONDO specifically.
- **Verdict: WATCH for a pullback, not a fresh chase. The existing B-tier position (tp1_hit) is running correctly; do not add fresh exposure at the current extension — wait for a retest into the RWA-basket support zone.**

### 5. BANK/USDT — crypto, avoid/chase-risk flag (top raw mover, explicitly flagged)
- Momentum/RS score 93.6 (highest on the desk today, 24h +40.5%, RS vs BTC +41.2%), but the scalp report explicitly rejects it: **"Price is more than 2 ATR from EMA20 — do not chase,"** converted to watchlist-only pending a pullback. It also did not clear into the intraday trade-idea agent's deep-analysis set.
- Has price already reacted? Yes, dramatically — this is the definition of an already-completed move, not a setup.
- Chasing? Explicitly, yes — this is a textbook chase-risk flag from the system's own gate, not an editorial judgment call.
- Legal/headline/catalyst check: no fresh BANK-specific catalyst found to justify the move; unexplained/momentum-only.
- **Verdict: AVOID a fresh long at current levels. Watch only for a genuine pullback to EMA20 with volume confirmation before reconsidering — do not treat today's move as a live entry signal.**

## 8. Best Candidates Ranked

1. **AAPL — best long-watch (stocks)** — pre-gate A-tier (91.0), RS leader, capped only by the market-closed gate; needs the first 15-30min RTH confirmation before treating as live.
2. **AMD — best short-watch (stocks)** — sector-aligned with confirmed overnight semiconductor weakness; needs the opening-range confirmation the system's own gate is requiring.
3. **UNH — best catalyst print, but AVOID/MANUAL REVIEW (stocks)** — genuine beat-and-raise blocked by an unresolved DOJ probe; flag for human review, do not auto-chase.
4. **ONDO/USDT — best crypto catalyst-watch (dual basket)** — already extended; watch for a pullback, do not chase the existing move.
5. **BANK/USDT — avoid, explicit chase-risk flag (crypto)** — today's biggest mover, but the system's own gate already rejected it as an entry; informational only.

No fresh, RTH-confirmed *new* entry exists in either asset class at 16:32 EEST — the US cash market opens essentially concurrently with this review. This is a **watch-and-confirm-at-open window**, not a system pause. Scanning, tracking, and monitors continue unchanged.

## 9. Avoid / No Trade (this decision window only)

- UNH — DOJ probe unresolved (confirmed 2026-07-14) stacked with a large earnings-day gap (+6% premarket) — do-not-chase regardless of the fundamentally strong print.
- NFLX — reports after today's close, do-not-chase pre-print, no open signal.
- BANK/USDT — explicit ">2 ATR from EMA20, do not chase" flag from the scalp report; today's biggest raw mover but a completed move, not a setup.
- MUB/USDT, SKHYB/USDT — thin-liquidity/short-squeeze-risk capped in the scalp report; not clean shorts despite weak_vs_market tags.
- Any fresh AAPL/AMD/JPM/AMZN/META/XLE/GOOGL/XOM entry treating the pre-open A-tier score as a live trigger before the RTH open actually confirms it — the `market_closed_intraday_planning_only` and ORB gates exist specifically to prevent this.
- This is a no-new-entries read for the listed names/situations only; the scanner, monitors, and scheduler continue running unchanged in both asset classes.

## 10. Main Risks

- **The US cash open (16:30 EEST) is essentially concurrent with this review** — nothing in the stocks candidate list is RTH-confirmed yet; treat every stocks number here as a pre-open plan, not a live trigger, until the opening range prints.
- **Genuinely active, externally-confirmed geopolitical escalation** (US blockade reinstatement, tanker *Belma* disabled, Iran strikes on Bahrain/Kuwait) continues; crypto has absorbed it so far (BTC -0.3%, ETH +2%) but a further escalation could still shift the mood materially — worth monitoring through the US session.
- **Semiconductor weakness continuing from TSMC's capex-heavy guidance** — a live headwind for AMD/NVDA/AVGO-class longs heading into the open; supports the AMD short-watch thesis but also caps enthusiasm for any semis long.
- **UNH's beat-vs-legal-risk contradiction** is the single most interesting single-name situation today and needs an actual human look at the open — the system correctly keeps it non-actionable, but a human may want to size the legal-risk probability explicitly.
- Catalyst mapping running at 80.4% unmapped today (direct count) — treat the catalyst layer as context only; this is a recurring pattern (17.3-19.6% mapped across the last two reviews), not a one-off.
- Crypto scalp mode remains kill-switched off — no scalp ideas today or expected, unchanged.
- Stocks weekly A/B headline PF is 0.40 on a weak-confidence n=17 sample — do not over-trust a fresh stocks A/B once RTH confirms it this week; size cautiously.
- **Data-lifecycle observation**: several stocks B-tier signals in the active-signals table carry `expires_at` timestamps from 2026-06-05 through 2026-07-08 (weeks in the past) while still showing `tp1_hit`/`tp2_hit`/`triggered` status rather than a closed/expired terminal state — see TODO-2 below.
- **Review-schedule gap**: only one prior review exists for today (13:26 EEST); the 04:30 and 11:30 EEST slots produced no output file — see TODO-3 below.

## 11. Action Plan — next 4 hours

- **Priority 1**: watch the first 15-30 minutes of RTH price action on AAPL (long-watch, zone 326.17-327.57) and AMD (short-watch, needs opening-range formation) — do not treat either as live until that confirmation exists.
- Flag UNH for an explicit human/manual review given the beat-vs-DOJ-probe contradiction — no automatic action either direction.
- No new NFLX exposure ahead of tonight's after-close print.
- Watch ONDO/USDT for a genuine pullback/retest into the RWA-basket support zone rather than chasing the current extension; same caution on BANK/USDT for a pullback to EMA20.
- Continue tracking crypto's B-tier signals already in flight (ONDO, ALLO, VIRTUAL ×2, XLM, SKL, VIRTUAL-scalp) — several already tp1/tp2_hit, manage per existing invalidation levels, no fresh entries needed.
- Monitor the Bahrain/Iran/tanker situation for further escalation or de-escalation through the US session — still the dominant tail-risk driver of today's elevated crypto macro-risk score.
- Continue scanning/tracking as normal in both asset classes — no system changes; both pipelines are healthy.

## 12. Final Verdict per Mode

- Crypto scalp: kill-switched off (mode disabled, structurally negative PF 0.25 playbook) — no ideas expected, unchanged.
- Crypto intraday: zero A/B this cycle; ONDO/USDT (C-tier, dual-basket catalyst-backed) is the cleanest watch name but already extended — wait for a pullback, do not chase.
- Crypto swing: last fresh cycle 05:27 EEST (~11h old, carry-forward); existing B-tier longs (ALLO, XLM, VIRTUAL — several tp1/tp2_hit) remain the desk's best still-open crypto exposure; the swing report's HOME/USDT B-tier idea should be treated as **stale/already-resolved** (no active HOME signal exists on the desk right now, consistent with it having stopped out earlier today per the prior review) — do not treat it as a fresh idea from this carry-forward report.
- Stocks intraday: **fresh classification exists (14:37 EEST) but is pre-open-capped** — AAPL (long-watch) and AMD (short-watch) are the two names to re-confirm at the open; UNH is a flagged contradiction, not actionable; no other name in the A-tier-score list clears both the technical and catalyst bars cleanly enough to lead the list.
- Stocks swing/invest (legacy): deprecated, not used this run. `stocks_swing_growth_breakout` (new framework): shadow-only research (1 open candidate, AAPL reclaim_after_shakeout 77.0), out of scope for actionability in this slot.

## 13. Sources

- [U.S. fires a new wave of strikes on Iran and hits a tanker trying to skirt its blockade — NPR](https://www.npr.org/2026/07/15/nx-s1-5894582/us-iran-updates) (2026-07-15)
- [Iran Strikes US Allies' Bases In Bahrain, Kuwait As Jordan Downs Missiles Amid Hormuz Blockade — HNGN](https://www.hngn.com/articles/272062/20260715/us-iran-truce-collapses-naval-blockade-resumes-iranian-missiles-kill-one-near-hormuz-strait.htm) (2026-07-15)
- [Bitcoin and ethereum prices today, Thursday, July 16, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-july-16-2026-prices-rise-ethereum-becomes-increasingly-compelling-124218108.html) (2026-07-16)
- [Bitcoin, Ethereum, XRP, Dogecoin Consolidate as US-Iran Tensions Escalate — Benzinga](https://www.benzinga.com/crypto/cryptocurrency/26/07/60406116/bitcoin-ethereum-xrp-and-dogecoin-consolidate-as-us-iran-tensions-escalate) (2026-07-16)
- [Stock market today: Dow, S&P 500, Nasdaq futures mixed as chip stocks slide after TSMC earnings — Yahoo Finance](https://finance.yahoo.com/markets/live/stock-market-today-thursday-july-16-dow-sp-500-nasdaq-103116735.html) (2026-07-16)
- [Stock Market Today (July 16, 2026): S&P 500 futures slip as tech stocks lose momentum — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-july-16-2026) (2026-07-16)
- [Asian Stocks Fall as Chip Selloff Overshadows TSMC Earnings — Modern Diplomacy](https://moderndiplomacy.eu/2026/07/16/asian-stocks-fall-as-chip-selloff-overshadows-tsmc-earnings/) (2026-07-16)
- [Cotton Warns Apple Not To Do Business With Dangerous Chinese Chipmaker — Sen. Tom Cotton press release](https://www.cotton.senate.gov/news/press-releases/cotton-warns-apple-not-to-do-business-with-dangerous-chinese-chipmaker) (2026-07-16)
- [Senator Cotton criticizes Apple for potential use of blacklisted China chips — CryptoBriefing](https://cryptobriefing.com/senator-cotton-apple-blacklisted-china-chips/) (2026-07-16)
- Internal: `data/reports/scalp/2026-07-16_11-19_scalp_report.md`, `data/reports/intraday/2026-07-16_11-26_intraday_report.md`, `data/reports/swing/2026-07-16_02-27_swing_report.md`, `data/reports/stocks/intraday/2026-07-16_11-37_stocks_intraday_report.md`, `data/catalysts/2026-07-16/*`, `data/processed/agent_outputs/20260716_112609_trade_idea_agent.json`, `20260716_113658_stocks_stock_trade_idea.json`, `20260716_113657_stocks_stock_scoring.json`.

## 14. Fix Requests / TODO

### TODO-1
- **issue:** Catalyst symbol-mapping coverage remains persistently weak (17.3% at 13:26 EEST → 19.6% this run, direct count), dominated by whale-transfer/mint alerts and multi-ticker listing lists the resolver can't attribute to one symbol.
- **evidence:** `data/catalysts/2026-07-16/catalyst_events.jsonl` — 392/2,000 mapped this run; sampled unmapped headlines are whale-flow noise, not missed tradeable catalysts.
- **suggested manual fix:** Consider either (a) filtering out whale-transfer/mint-alert event types from the mapped/unmapped denominator so the coverage metric reflects genuinely attributable news, or (b) extending the symbol resolver to handle multi-ticker listing-announcement formats (e.g., the Binance tokenized-equity pairs list). Low urgency — the catalyst layer is already correctly treated as context-only per the existing §H rule.
- **priority:** low
- **first observed:** 2026-07-15 (recurring across multiple reviews)

### TODO-2
- **issue:** Several stocks B-tier signals in `active-signals` show `expires_at` timestamps weeks in the past (2026-06-05 through 2026-07-08) while still displaying non-terminal statuses (`tp1_hit`, `tp2_hit`, `triggered`) rather than a closed/expired terminal state.
- **evidence:** `python -m src.cli active-signals --asset-class stocks --tier B` — e.g. `sig_1bc6d2076b02bd2b` SMH expires 2026-06-05T10:59:41 still `tp1_hit`; `sig_f1425a12d5b3e1cd` SMCI expires 2026-06-07T22:16:06 still `tp1_hit`; `sig_20c7c47312a9c1ee` UNH expires 2026-06-11T14:55:38 still `tp1_hit`.
- **suggested manual fix:** Have a human check whether the lifecycle/track-signals job is correctly terminalizing stocks B-tier signals past their `expires_at`, or whether these are intentionally left open pending a manual TP3/close decision. If unintentional, this inflates the "active signals" count in every future review and could confuse candidate-priority scoring (§F item 4, "waiting_for_entry within 1 ATR").
- **priority:** medium
- **first observed:** 2026-07-16 16:20 EEST review (not flagged in prior reviews, may be longer-standing)

### TODO-3
- **issue:** The 04:30 and 11:30 EEST scheduled-review slots for 2026-07-16 produced no output file — only the (mislabeled) 13:26 EEST review and this 16:20 EEST review exist for today.
- **evidence:** `ls OPUS_ENRICHED_REVIEW_AUTO_2026-07-16*.md` → only `_1326.md` exists before this run.
- **suggested manual fix:** Check the `opus-enriched-review-4h` / sibling scheduled-task dispatcher logs for 2026-07-16 04:30 and 11:30 EEST to see whether the task failed to fire, was skipped, or fired with an output-write failure. Out of scope for this run to diagnose (scheduler ops are forbidden under §B).
- **priority:** medium
- **first observed:** 2026-07-15 21:39 EEST review cycle (recurring)

### TODO-4
- **issue:** ONDO/USDT's momentum/RS ranking score (90.8, top-movers table) diverges sharply from its final trade-idea-agent score (56.2, C-tier watchlist) — expected by design (different scoring layers) but worth a documentation note so future reviews don't read the top-movers score as the tradeable score.
- **evidence:** `data/processed/llm_analysis_packet.md` top-movers list vs. `data/processed/agent_outputs/20260716_112609_trade_idea_agent.json` ideas list.
- **suggested manual fix:** No code change needed; consider adding a one-line clarifying note in the LLM packet's top-movers section (e.g., "raw momentum score, not the final trade-idea score") to reduce the chance of a future review or operator conflating the two.
- **priority:** low
- **first observed:** 2026-07-16 16:20 EEST review
