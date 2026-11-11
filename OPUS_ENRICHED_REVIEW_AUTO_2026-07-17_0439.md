# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (04:30 EEST). **Advisory only — no auto-trade, no code/scoring/routing changes.** Data pipeline healthy: `scheduler.log` ~32min old, latest cycle summary (`cycle_01_03-12_summary.md`, finished 04:07 EEST) ~32min old — **not deferred**. Crypto scalp/intraday/swing reports all fresh (~1h18m–1h23m old, generated 03:21–04:03 EEST). Stocks intraday fresh (~1h58m, after-hours planning-only) — **US cash session closed**, treat all stock signals as planning/watchlist context only.

**Crypto: only one live position** — ONDO/USDT intraday (B, long, `tp2_hit`, unchanged since the 02:45 review) managing toward tp3. **No new crypto signals fired this cycle** — every fresh idea in both the intraday and swing reports (KAITO, ALLO, BANK, ZEC, DOT, MANTRA, TREE, LUMIA) is **watchlist-only**, and **100% long-biased again** — the scanner surfaced zero short setups tonight. BANK/USDT's score continued to fade (65→52) with still no verified catalyst. **System-integrity issue unchanged, not escalated**: `detect_untracked_legacy_alerts` still shows exactly **2** unresolved (ALLO/USDT, now 14+ hours / 6+ review cycles; BANK/USDT, ~7h) — no third symbol joined this cycle, and no fresh watchlist alert fired at all since 21:36 UTC yesterday. TODO-3 stays **high**, unchanged.

Crypto Fear & Greed ticked from 25→**27** (still fear-zone, borderline extreme-fear, not a real regime change). Dashboard still labels crypto `trend`/`bullish` while both fresh reports read **BTC/ETH trend = range** — the same internal label inconsistency flagged last cycle. Swing-report altcoin breadth **dropped to 26.8%** above EMA20 (from ~47.5% two cycles ago) — genuinely weaker breadth, worth watching into Europe. Catalyst mapping is **weak this run (84% unmapped, 80/500)** — treat catalyst layer as context only. **Stocks**: AVGO (short) and XOM (long) remain the cleanest A-pretier planning ideas for the 09:30 ET open, now with concrete levels published (`active-signals` CLI); **MSFT still carries an unresolved securities-fraud legal/headline gate** and stays AVOID/MANUAL REVIEW. Scanning, tracking, and all monitors continue unaffected — **no recommendation to pause anything.**

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-17_00-21_scalp_report.md` (generated 03:21 EEST, ~1h23m old), `data/reports/intraday/2026-07-17_00-27_intraday_report.md` (generated 03:27 EEST, ~1h17m old, regime range/chop), `data/reports/swing/2026-07-17_01-03_swing_report.md` (generated 04:03 EEST, ~41min old, regime transition/mixed), `data/reports/stocks/intraday/2026-07-17_00-47_stocks_intraday_report.md` (generated ~04:46 UTC / ~1h58m old, after-hours planning-only). Stocks swing/invest last generated 2026-07-02 — deprecated legacy framework, excluded (>14h stale by design).
- Catalyst: `data/catalysts/2026-07-17/catalyst_events.jsonl` (500 rows, today's UTC day), `narrative_baskets.jsonl` (6 baskets), `data/catalysts/2026-07-17/catalyst_cycle_00-31.md` (latest cycle, already present, no re-scan needed).
- LLM packets: `data/processed/llm_analysis_packet.md` (~41min old), `data/processed/llm_stocks_packet.md` (~56min old).
- DB (direct SQL, `db/crypto_ai_desk.sqlite`): `proposed_signals`, `watchlist_alerts`, `market_dashboard_snapshots`.
- CLI: `active-signals` ×2, `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-16` (apples-to-apples with prior review) and `--since 2026-07-17` (fresh-today check).
- Scheduler: `data/scheduled_runs/2026-07-17_default_schedule/scheduler.log`, `cycle_01_03-12_summary.md`.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-17_0245.md` (post-close, dispatched late at 02:45 EEST) — used for TODO carry-forward, thesis tracking (ONDO/BANK/ALLO/MSFT), and integrity-issue history.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **04:07:49 EEST**, latest `cycle_01_03-12_summary.md` mtime **04:07:47 EEST** — both ~32min old at review start (04:39). **Not deferred.**
- Crypto scalp/intraday: fresh (~1h17-23m, content-generated timestamps 03:21/03:27 EEST — note report filenames use a UTC-labeled naming convention offset ~3h earlier than the EEST content timestamp; used the in-file `Generated at` field, not the filename, for freshness).
- Crypto swing: fresh (~41min, generated 04:03 EEST) — well inside the fresh band.
- Stocks intraday: ~1h58m old, generated after-hours — US cash session is closed; every name is `market_closed_intraday_planning_only` (A/B pre-tier demoted to C, planning levels only). Expected at this hour, not a fault.
- Stocks swing/invest: last generated 2026-07-02 (15 days stale) — known, intentionally-deprecated legacy framework; not a freshness fault.
- Catalyst directory present for today (`2026-07-17`), 500 rows already scanned this cycle — no re-scan needed.
- Monitors: not independently re-verified this cycle (no monitor-status command in the allowed CLI list); no anomaly in the scheduler summary read (76/76 steps ok=76 failed=0).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-17 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["monitor process status not re-checked this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle summary both ~32min old, cycle finished 04:07 EEST with 76/76 steps ok", "crypto scalp ~1h23m, intraday ~1h17m, swing ~41min — all fresh", "stocks intraday ~1h58m fresh but after-hours planning-only", "stocks swing/invest deprecated, 15d stale by design"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["dashboard crypto_market_mode=trend, but both intraday (BTC/ETH trend=range) and swing (BTC/ETH trend=range, regime label 'transition/mixed') reports independently read range — same label inconsistency as last cycle, treat the report-level read as primary", "altcoin breadth above EMA20 dropped to 26.8% (swing) / 43.9% (intraday) — weaker breadth than the ~47.5% seen two cycles ago, genuinely softer tape", "Fear & Greed 27 (fear, borderline extreme-fear), up marginally from 25 — not a meaningful regime shift", "stocks_market_mode=unknown (overnight/closed), VIX 16.73 low-normal from the last-loaded report"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["500 catalyst events today, 80 mapped (16.0%), 420 unmapped (84.0%) — weak mapping, worse than the 20.5% cumulative baseline seen at 02:45 (different, smaller today-only sample; largely whale-mint/generic-newswire noise)", "6 narrative baskets: perps_dex (HYPE primary), rwa_narrative (ONDO+XLM primary, <24h fresh), binance_ecosystem_teaser (BNB primary), ai_narrative (NEAR/RENDER/TAO/FET), delisting_thin_liquidity, momentum_breakout (KAITO primary, <1h fresh, explicitly no confirmed news)", "BANK/USDT again explicitly 'no fresh verified catalyst detected' in both intraday and swing reports this cycle", "ONDO/XLM RWA basket remains the only basket with a live, catalyst-confirmed position (ONDO intraday, tp2_hit)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "ok",
      "confidence": 0.4,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["OI for most non-BTC/ETH symbols", "funding/OI history beyond this cycle's snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["KAITO/USDT: price up + OI up 1.46%, funding 5e-05 (low) — fresh positioning, not a squeeze", "ALLO/USDT: price up + OI down 2.16% — short covering, weaker continuation quality (a caution flag, not a squeeze signal)", "BANK/USDT: funding 5e-05 neutral, external cross-check shows low crowding"]
    },
    {
      "agent": "technical_entry",
      "verdict": "ok",
      "confidence": 0.55,
      "reason_codes": ["clean_retest", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONDO/USDT intraday tp2_hit — managing toward tp3, not a fresh entry, no chase risk for the existing position", "KAITO/USDT: current price 0.8587 sits just above its conditional swing pullback zone (0.8390-0.8526) — a genuine pullback-to-zone would be a clean, non-chased retest trigger, not a chase", "BANK/USDT: score continued to fade (65.0 at 21:36 UTC -> 51.9 this cycle) — the setup is getting weaker, not fresher; conditional zone 0.0600-0.0610 remains below-threshold watch-only", "AVGO/XOM: concrete planning levels now published via active-signals (AVGO short 374.46-377.46 inval 380.4652; XOM long 145.46-145.97 inval 144.9546), both require RTH confirmation before any fill — not chaseable pre-market"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: exactly 1 OPEN actionable position (ONDO/USDT intraday, tp2_hit, running toward tp3); zero new triggers, zero waiting, zero entered-unresolved this cycle — a quiet overnight window", "stocks: 20 WAITING for entry (all C-tier planning, expire 2026-07-18T00:46:39 — tomorrow's session), plus a backlog of REVIEW/SHADOW (triggered/tp1/tp2 running) and CLOSED WIN/LOSS names carried from the prior 1-2 sessions, none of it live-actionable tonight since the cash session is closed"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["legal_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT: securities-fraud shareholder-rights PR-Newswire solicitation still present in tonight's report, unchanged from 02:45 — tier demoted B(74)->C, AVOID/MANUAL REVIEW", "Same law-firm-solicitation pattern (Pomerantz etc.) appears against Planet Fitness, GPGI, Nano-X, BitGo, AeroVironment in tonight's catalyst top-10 — none of those symbols are on the active-signals list, so no new gate needed, but the pattern itself is generic recurring PR-Newswire noise, not confirmed fraud findings", "stocks_intraday_7d_drawdown_guard forward evidence (Model F, 14d/30d paper_execution_r all=-3.0R/PF0.40/n=10; would-have-been-A/B 14d net -42.5R/PF0.27) is unchanged from the 02:45 read — same numbers, continues to support the guard"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "bad",
      "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B(B-tier) weekly: n=156 (was 160 at 02:45 — window rolled slightly), winrate 22.2%, PF 1.7857, avgR 0.2292, totalR +27.50 — still profitable via R:R asymmetry", "crypto scalp mode still losing: n=34 (31 triggered), 0 wins/7 losses, PF 0.40, totalR -3.0 — unchanged real losing bucket", "crypto short direction still losing (n=6, PF 0.25, anecdotal, avgR -0.375) — but this is a sample-size artifact of near-zero shorts being generated at all, not evidence shorts should be avoided structurally", "stocks A/B weekly: n=14 (weak confidence), winrate 28.6%, PF 0.6667, avgR -0.125, totalR -1.0 — unchanged losing; C-tier n=207, PF 0.7568, totalR -9.0; semiconductors/technology sectors still worst (PF 0.10-0.20)"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "KAITO/USDT", "trigger": "swing pullback fill into 0.8390-0.8526 (current price 0.8587, just above zone), invalidation 1h close below 0.8223", "reason": "cleanest RS-leader in both intraday and swing scans two cycles running (RS +14.15% vs BTC), fresh OI confirms the trend (not just price), medium confidence — but explicitly no verified catalyst, size accordingly" },
    "best_short_candidate":    { "symbol": "none — crypto scanner surfaced zero shorts again tonight; AVGO (stocks, planning-only)", "trigger": "AVGO: RTH confirmation at 09:30 ET against the published 374.46-377.46 zone, invalidation 380.4652; crypto has no clean short structure this cycle (HOME/USDT -39.46% 24h is the weakest symbol but below the scanner's actionable threshold — do not fabricate a level)", "reason": "AI-capex-slowdown sector headline + semiconductors -7.69% RS vs SPY remains the cleanest short-side alignment on the board; crypto stayed 100% long-biased for a second consecutive cycle, worth flagging as a standing scanner characteristic, not a bug" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "already open (intraday, B-tier, tp2_hit) — manage toward tp3; do not chase above current levels", "reason": "only symbol tonight with both a confirmed catalyst (RWA/tokenization basket, SBI deal) and a live, in-profit position; its swing sibling already stopped -1R on 2026-07-16, a reminder that catalyst-confirmed is not risk-free" },
    "avoid_candidate":         { "symbol": "BANK/USDT", "reason": "score faded 65.0->51.9 this cycle with still no verified catalyst, negative-expectancy no-catalyst-momentum playbook bucket, and the ongoing source of the unresolved untracked-alert integrity issue (TODO-3) — do not chase even if price prints the conditional zone" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.50 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.40 | oi_supports, data_unavailable | advisory_only |
| technical_entry | ok | 0.55 | clean_retest, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry, review_shadow, no_entry | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | bad | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (02:45 EEST)

- **Unchanged**: ONDO/USDT intraday remains the only live crypto position — still `tp2_hit`, still managing toward tp3, no status change since 02:45.
- **Faded, not escalated**: BANK/USDT's score dropped from 65.0 (the 21:36 UTC watchlist alert) to 51.9 this cycle — momentum is cooling, still explicitly no catalyst. It did **not** produce a new fresh watchlist alert or signal this cycle, so the untracked-alert count stayed at 2 (no third symbol).
- **Unchanged**: `detect_untracked_legacy_alerts` still returns exactly ALLO/USDT (now 14+ hours, 6th+ consecutive review cycle) and BANK/USDT (unresolved since 21:36 UTC, ~7h) — confirmed via both `--since 2026-07-16` (2 results, same as 02:45) and `--since 2026-07-17` (0 new results today). TODO-3 stays **high**, no new evidence either way this cycle.
- **New this cycle**: KAITO/USDT has now printed as the top-scored RS-leader in *both* the intraday (score 91.6) and swing (score 93.1) reports for a second consecutive cycle, with concrete conditional levels — promoted to best long-watch candidate this review (was not deep-dived at 02:45).
- **Weaker breadth**: swing-report altcoin breadth above EMA20 fell to 26.8% (from a higher reading in earlier cycles) — a genuine softening signal worth tracking into the Europe slot, not previously flagged this explicitly.
- **Unchanged**: Catalyst mapping stays weak (16.0% mapped today vs. 20.5% cumulative at 02:45 — different denominators, both weak). Fear & Greed nudged 25→27 (immaterial). MSFT's legal/headline gate is unchanged, same underlying PR Newswire item from 2026-07-16.
- **Unchanged**: AVGO/XOM remain the two cleanest stocks planning ideas; their levels are now directly readable from `active-signals` (they were not re-confirmed with exact numbers at 02:45 — this review adds them for the first time from a verified internal source, not fabricated).
- **No update available**: TODO-1 (drawdown-guard calibration) — same underlying 14d/30d numbers as 02:45 (report content did not refresh between cycles); TODO-2 and TODO-4 not independently re-checked this cycle (see §14).

## 5. Catalyst Coverage

- Catalyst events today (`2026-07-17`, UTC day so far): **500** scanned, **80 mapped (16.0%)**, **420 unmapped (84.0%)**. Narrative baskets: **6**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sample): "250,000,000 $USDC (~$250M) minted at USDC Treasury" (whale-mint noise, not symbol-actionable); "MoonPay has acquired Glide, a cross-chain deposit infrastructure startup"; "Ledger has launched Agent Stack, letting AI agents prep crypto transactions."
- Mapped/basket-confirmed narratives in play: **RWA/tokenization** (ONDO/USDT + XLM/USDT primary, <24h fresh — the only basket with a live, in-profit position tonight); **perps-DEX** (HYPE/USDT primary, DYDX/GMX/ASTER related); **Binance ecosystem teaser** (BNB/USDT primary, ASTER related); **AI sector rotation** (NEAR/RENDER/TAO/FET primary); **delisting/thin-liquidity capitulation** (avoid-low-liquidity playbook, <6h fresh); **momentum-breakout** (KAITO/USDT primary, <1h fresh, explicitly "without confirmed news catalyst" — pure momentum cluster, consistent with the technical read above).
- Also noted (not mapped to an active signal): Humanity Protocol (H) -15% on a $36M exploit/hack headline (AMBCrypto) — no active or watchlist position in this symbol, context only.

## 6. Market Landscape

### Crypto
- Regime: dashboard label **bullish trend**, but both the fresh intraday report (BTC/ETH trend = **range**) and the fresher swing report (regime = **transition/mixed**, BTC/ETH trend = **range**) independently disagree with the dashboard tag — same inconsistency flagged last cycle, treat the report-level read (range/chop-leaning, neutral-to-softening) as primary. Altcoin breadth above EMA20: **43.9%** (intraday) / **26.8%** (swing) — the swing reading is a meaningfully weaker breadth print than recent cycles. Volatility normal (ATR percentile 31-32).
- Fear & Greed: **27** (fear, borderline extreme-fear), up marginally from 25 at 02:45/21:39 — not a material shift, still a sentiment headwind, not a tailwind.
- Strongest (swing): KAITO/USDT (score 93.1, +13.1% 24h), BANK/USDT (score 91.6, +18.9% 24h, no catalyst, fading), SOXLB/USDT (score 80.2, -13.3% 24h — a short-biased strong-score name, not deep-dived, no signal minted), ALLO/USDT (score 77.4, +2.5% 24h, still the source of the oldest untracked-alert). Weakest (intraday): HOME/USDT (-39.5% 24h), SNDKB/USDT (-13.1% 24h) — no active signals either direction, no fresh news confirming the weakness thesis, below the scanner's actionable threshold.

### Stocks
- Regime: **transition** (report label), risk-on **False**, VIX **16.73** (low-normal), breadth 75%/75% above EMA20/50 (healthy breadth despite the transition label). SPY uptrend (+0.05% 20d), DIA uptrend (+0.65% 20d), QQQ **downtrend** (-3.28% 20d), IWM range.
- Strongest sectors: healthcare (XLV, RS +5.74% vs SPY 20d), financials (XLF, +4.36%), energy (XLE, +2.95%) — unchanged from 02:45. Weakest: semiconductors (SMH, -7.69%), technology (XLK, -4.84%), materials (XLB, -3.52%) — unchanged.
- Market status: **closed (overnight/after-hours)** — every intraday A/B idea is demoted to C, planning-only until the 09:30 ET open (many hours away from this 04:30 EEST slot).
- Legal/headline gate active: **MSFT** (unchanged securities-fraud PR-Newswire solicitation, 2026-07-16); same generic law-firm-solicitation pattern also appears against Planet Fitness, GPGI, Nano-X, BitGo, AeroVironment in tonight's catalyst feed — none are on the active-signals list, no new gate required.

### Market Mood / Risk Routing

- Crypto mood: **mixed, softening slightly** (report-level range/transition regime disagrees with the dashboard's "bullish trend" tag; altcoin breadth weaker than earlier cycles; fear-zone sentiment persists; scanner remains 100% long-biased with zero shorts surfaced two cycles running)
- Stocks mood: **closed / transition** (US cash session closed; regime label transition with healthy breadth; sector rotation still firmly into healthcare/financials/energy and out of semis/technology)
- Dominant narrative: RWA/tokenization (ONDO/XLM) in crypto, the only basket with a live in-profit position; AI-capex-slowdown fear (semis/tech weak) vs. oil-rally/energy strength in stocks
- Preferred side now: **catalyst-backed only, cautious** (crypto — manage the existing ONDO position, do not chase no-catalyst momentum) / **wait-for-RTH-confirmation** (stocks — nothing fills before 09:30 ET, many hours out)
- Best long candidate: **KAITO/USDT** (crypto, swing, watch-only — trigger: pullback fill into 0.8390-0.8526, invalidation below 0.8223); **XOM** (stocks, planning-only, A-pretier — trigger: RTH confirmation, published zone 145.46-145.97)
- Best short candidate: **none clean in crypto** (scanner surfaced zero shorts again; HOME/USDT is the weakest symbol but below actionable threshold, no level to publish); **AVGO** (stocks, planning-only, A-pretier — trigger: RTH confirmation, published zone 374.46-377.46)
- Best catalyst-backed candidate: **ONDO/USDT** (intraday, open, tp2_hit — manage toward tp3; RWA basket)
- What to avoid: **BANK/USDT as a chase** (fading score, no catalyst, negative-expectancy playbook bucket, ongoing source of the untracked-alert integrity issue); **MSFT** (active legal/headline gate, stocks)
- What would change the view: a fresh, verified `news_items` hit on BANK/USDT or HOME/USDT; resolution of the MSFT securities-fraud matter; a third symbol joining `detect_untracked_legacy_alerts` (would confirm TODO-3 is accelerating, not just persisting); RTH price action on AVGO/XOM at the 09:30 ET open; altcoin breadth recovering back above ~40% (currently 26.8% swing-read)

## 7. Candidate Deep Dives

### 1. ONDO/USDT — long, catalyst-backed, crypto (B, intraday, open tp2_hit)
- Intraday leg (`sig_a914cdba49291324`): entry 0.36521-0.36970, invalidation 0.35971, currently **tp2_hit**, open toward tp3, expires 2026-07-17T08:36:31 UTC. Unchanged status since the 02:45 review.
- Sibling swing leg (`sig_b5561a1b247ead39`, entry 0.37805-0.38210): remains **stopped, -1.0R** (since 2026-07-16) — the catalyst (SBI tokenization deal, MEXC tokenized-stock listing) was real and verified, but price still reversed through the swing stop. Confirms the finding from the last two reviews: catalyst confirmation reduces but does not eliminate downside risk.
- Has price already reacted to the catalyst? Yes, substantially (+17% 24h at the time the intraday position was opened); the swing stop-out suggests the move was largely priced in by the time that sibling entry filled.
- Chasing? No for the existing intraday position (already deep in profit, tp2_hit, expiring within ~4h of this review); yes for any fresh entry now, given the swing sibling's prior failure and the RWA narrative basket showing no new confirming headline tonight.
- Aligned with market mood? Marginally — the only catalyst-confirmed name with a live position in an otherwise mixed/softening-breadth crypto tape.
- Actionable level: manage the existing intraday position toward tp3; do not add on catalyst-only conviction without a fresh technical trigger. Position also expires at 08:36 UTC (~4h from this review) — worth a status check at the 11:30 EEST Europe slot.
- Invalidation: 0.35971 (intraday stop, unchanged).

### 2. KAITO/USDT — long-watch, crypto, no catalyst, RS-leader (swing, watchlist score 63.1 / intraday score 91.6)
- Swing conditional zone: pullback entry 0.8390-0.8526, invalidation 1h close below 0.8223, targets 0.8890/0.9193/0.9496. Current price 0.8587 (just above the pullback zone) — a genuine pullback fill would be a clean retest, not a chase.
- Catalyst: **no fresh verified catalyst detected** — pure RS/momentum play, tagged in tonight's `momentum_breakout` narrative basket explicitly as "without confirmed news catalyst" (fresh <1h).
- Has price already reacted? Partially — +13.06% 24h, +29.24% 7d; RS vs BTC +14.15%, still the top-scored name across both intraday (91.6) and swing (93.1) scans for a second consecutive cycle, suggesting the RS leadership is persistent, not a one-cycle spike.
- Would a fresh entry be late? Current price sits above the conditional entry zone (chasing if entered at market); a pullback into 0.8390-0.8526 with volume confirmation would not be late.
- Aligned with market mood? Cautiously — it's the cleanest technical structure on the board tonight, but the desk's own playbook note (no-catalyst intraday/swing momentum in chop/transition regimes) argues for smaller size and RS-leader confirmation over conviction sizing.
- Chase risk: moderate if entered above the zone; low if entered on a confirmed pullback.
- Would invalidate: 1h close below 0.8223; BTC breaking down against the regime thesis; the RS-leader status fading on the next report cycle (as BANK/USDT's did overnight).

### 3. BANK/USDT — avoid/chase-risk, crypto, no catalyst + unresolved integrity flag (swing no-entry/moved-away / intraday watchlist, fading)
- Swing leg (`sig_ff3e8319e73a112d`): entry 0.05614-0.05736, invalidation 0.05464 — **status update this cycle: resolved to `entry_moved_away` (NO-ENTRY / MOVED AWAY)**, not still `waiting_for_entry` as characterized in the last two reviews (verified directly via SQL, not visible in the `active-signals` table since closed signals drop off that view). Price moved up and away from the stale zone without a fill — this closes the 14+ hour open question, but confirms the zone was too stale to ever trigger, not a new development to act on.
- Intraday score continued to fade this cycle: 91.6 as a "strongest symbol" mention, but the actual trade-idea score dropped to **51.9** (from 65.0 at the 21:36 UTC watchlist alert, and from 66.1 at the prior review's read) — momentum is visibly cooling even as the raw 24h return (18.7%→18.9%→18.7%) stays roughly flat.
- Catalyst: still explicitly **"no fresh verified catalyst detected"** in both the intraday and swing reports tonight, plus the desk's own playbook note: "No-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation" (14d cut: WR 23% / PF 0.70 / -3R).
- **System-integrity flag unchanged**: `detect_untracked_legacy_alerts` still lists BANK/USDT (alert id 1638, 21:36:05 UTC, unresolved ~7h) alongside ALLO/USDT (14+ hours) — no third symbol joined this cycle and no fresh alert fired for either symbol since. See TODO-3 (unchanged, high).
- Actionable level: swing fill at 0.05614-0.05736 (increasingly stale, deep pullback zone); intraday conditional zone 0.0600-0.0610 (below-threshold, score continuing to fade rather than firm up).
- Would invalidate the long-watch thesis (if ever activated): a 1h close below 0.05464 (swing) / 0.0587 (intraday reference); confirmed absence of any real news catalyst continuing to hold.
- Chase risk: **elevated and worsening** — fading score plus the ongoing unresolved integrity issue argue for treating this purely as a research/monitoring name, not a trade candidate.

### 4. AVGO — short-watch, stocks, planning-only (A pre-gate 89.62, demoted to C for market-closed)
- Concrete levels now confirmed via `active-signals`: entry 374.46-377.46, invalidation 380.4652, expires 2026-07-18T00:46:39 UTC (tomorrow's session) — status `waiting_for_entry`. These were "not published" as of the 02:45 review; this review verifies them directly from the tracked signal record, not fabricated.
- Catalyst/narrative: unchanged same-day sector headline — "Marvell Drops 8% as AI Capex Slowdown Fears Weigh on Chips; Broadcom, AMD, and Intel Slide" (Yahoo Finance Top Stories, 2026-07-16); semiconductors remain today's weakest sector (RS -7.69% vs SPY 20d).
- Has price already reacted? Not independently re-verified this cycle (no fresh intraday tick data read); treat the headline as still-relevant context, not a confirmed price move.
- Aligned with market mood? Yes — cleanest short-side sector alignment on the board, unchanged from 02:45.
- Actionable level: not actionable now (market closed, ~5h from the 09:30 ET open); would need RTH confirmation before any fill against the published zone.
- Would invalidate: a positive AI-capex surprise or a broad semis bounce at the open.

### 5. XOM — long-watch, stocks, planning-only (A pre-gate 89.44, demoted to C for market-closed)
- Concrete levels now confirmed via `active-signals`: entry 145.46-145.97, invalidation 144.9546, expires 2026-07-18T00:46:39 UTC — status `waiting_for_entry`. Same verification note as AVGO above.
- Catalyst/narrative: unchanged — "Oil Pushes Above $85 as US Reserve Buffer Depletes: Will Crude Hit $100?" (BeInCrypto, 2026-07-15); energy remains one of today's strongest sectors (RS +2.95% vs SPY 20d).
- Aligned with market mood? Yes — energy strength remains one of the cleanest sector trends, contrasting with weak tech/semis.
- Actionable level: not actionable now (market closed); RTH confirmation required against the published zone.
- Would invalidate: an oil-price reversal below $85 or an energy-sector rotation reversal at the open.

**Excess candidates not deep-dived**: ALLO/USDT (swing watchlist score 58.7, no catalyst, also the oldest unresolved untracked-alert — covered in §4/§9 as an integrity issue, not a fresh trade idea); ZEC/DOT/MANTRA/TREE/LUMIA (all swing watchlist-only, scores 50-58, no catalyst, RS-momentum playbook, lower conviction than KAITO); MSFT (stocks avoid, unchanged from 02:45, not re-deep-dived since nothing changed); SOXLB/USDT (swing "strongest symbols" list, score 80.2, short-biased 24h -13.3%, but no trade idea/signal generated this cycle — context only).

## 8. Best Candidates Ranked

1. **ONDO/USDT long** (crypto, B, intraday, open tp2_hit) — catalyst-backed, actionable now (manage existing position toward tp3, expires ~08:36 UTC). Trigger: N/A, already filled.
2. **KAITO/USDT long-watch** (crypto, swing, RS-leader, no catalyst) — cleanest technical structure on the board, two cycles running as top scorer. Trigger: pullback fill into 0.8390-0.8526, invalidation below 0.8223.
3. **XOM long-watch** (stocks, A-pretier, planning-only) — energy-sector strength + oil-rally catalyst, levels now confirmed. Trigger: RTH confirmation at 09:30 ET against 145.46-145.97.
4. **AVGO short-watch** (stocks, A-pretier, planning-only) — semis-sector weakness + AI-capex-slowdown headline, levels now confirmed. Trigger: RTH confirmation at 09:30 ET against 374.46-377.46.
5. **BANK/USDT avoid/chase-risk** (crypto, fading score, no catalyst, unresolved integrity flag) — do not treat as clean; monitor only.

## 9. Avoid / No Trade (this decision window only)

- **BANK/USDT as a chase** — score faded 65.0→51.9 this cycle, explicitly no confirmed catalyst, negative-expectancy playbook bucket (14d no-news cut: WR 23% / PF 0.70 / -3R), and implicated in an unresolved system-integrity issue (TODO-3, ~7h unresolved).
- **MSFT** — AVOID / MANUAL REVIEW. Active securities-fraud shareholder-rights solicitation (PR Newswire, 2026-07-16, unchanged). Applies to this decision window only — scanning and tracking continue.
- **New crypto scalp entries generally** — weekly scalp-mode stats show 0 wins / 7 losses, PF 0.40, totalR -3.0 over the sample read; not a fault to fix here, just a caution for this window.
- **Crypto shorts generally** — the scanner produced zero short setups again tonight (second consecutive cycle); this is a scanner/regime characteristic to note, not a directive to force shorts that aren't there.
- Scanning, candidate generation, tracking, and outcome recording continue unaffected across all of the above — this is a per-symbol/per-window caution, never a system-wide stop.

## 10. Main Risks

- Altcoin breadth (swing-report read) dropped to 26.8% above EMA20 — a genuinely softer print than the ~47.5% seen in earlier cycles; if this continues into the Europe slot, the "range/chop" read strengthens further and RS-leader longs like KAITO become more chase-prone.
- Crypto Fear & Greed remains fear-zone (27), still diverging from the dashboard's "bullish trend" label — a fragile-sentiment backdrop into the Asia→Europe transition.
- BANK/USDT and ALLO/USDT's watchlist-alert integrity issue remains unresolved across 6+ review cycles for ALLO/USDT specifically — if a third symbol joins, that would confirm the root cause is actively recurring rather than a one-time double failure; worth explicit attention at the next review.
- `stocks_intraday_7d_drawdown_guard` continues to suppress 100% of A/B stock names; forward evidence (14d/30d paper_execution_r -3.0R, would-have-been-A/B -42.5R) is unchanged from 02:45 and keeps supporting the guard, but TODO-1 (human calibration confirmation) remains formally open.
- Catalyst-confirmed does not equal guaranteed win — ONDO/USDT's swing loss despite real, verified news (from the prior review) remains a live reminder heading into any fresh RWA-basket entries.

## 11. Action Plan — next 4 hours (into the 11:30 EEST Europe / pre-US slot)

- Manage the open ONDO/USDT intraday position (tp2_hit) toward tp3; it expires ~08:36 UTC (~4h from this review) — check resolution status at the next review.
- Watch KAITO/USDT for a pullback fill into 0.8390-0.8526 with volume confirmation; do not chase above the zone. Re-check whether it holds its RS-leader status for a third consecutive cycle.
- Do not chase BANK/USDT above the stated zones — score is fading, not firming; if it fires a fresh watchlist alert, verify immediately whether a matching `proposed_signal` was minted (TODO-3 relevance).
- Hold AVGO/XOM levels as the pre-open watchlist for the 16:20 EEST pre-US-open decision review; do not treat tonight's planning-only levels as final until re-confirmed against a fresher report closer to the open.
- Next scheduled review (11:30 EEST, Europe/pre-US context) should reconcile: whether ONDO/USDT intraday resolved to tp3 or reversed, whether altcoin breadth recovered or fell further, whether a third symbol joined `detect_untracked_legacy_alerts`, and whether BANK/USDT's score continued to fade or found fresh confirmation.

## 12. Final Verdict per Mode

- **Crypto scalp**: **avoid new entries** — weekly sample shows 0 wins/7 losses, PF 0.40, totalR -3.0; no scalp signal fired this cycle.
- **Crypto intraday**: **watch/manage** — ONDO/USDT open (tp2_hit, catalyst-backed, expires ~08:36 UTC); no new intraday trigger of note.
- **Crypto swing**: **catalyst-backed only, cautious; watch KAITO/USDT as the cleanest non-catalyst RS structure** — BANK/USDT and ALLO/USDT remain no-catalyst chase-risk watches, not clean actionables; breadth softening argues for smaller size on any fresh entries.
- **Stocks intraday**: **watch_only / planning_only** — market closed, zero A/B all session (guard + closed-session demotion); AVGO/XOM are the cleanest planning ideas for the 09:30 ET open, now with confirmed levels.
- **Stocks swing/invest**: dormant (deprecated legacy framework) — no verdict needed.

## 13. Sources

- Internal: `data/reports/scalp/2026-07-17_00-21_scalp_report.md`, `data/reports/intraday/2026-07-17_00-27_intraday_report.md`, `data/reports/swing/2026-07-17_01-03_swing_report.md`, `data/reports/stocks/intraday/2026-07-17_00-47_stocks_intraday_report.md`, `data/catalysts/2026-07-17/catalyst_events.jsonl`, `data/catalysts/2026-07-17/narrative_baskets.jsonl`, `data/catalysts/2026-07-17/catalyst_cycle_00-31.md`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `watchlist_alerts`, `market_dashboard_snapshots`), `data/scheduled_runs/2026-07-17_default_schedule/scheduler.log`.
- Reused from prior review (02:45 EEST, internal source, <24h old, uncontradicted by fresher `news_items` this cycle): "Microsoft Corporation (MSFT) Shareholders Who Lost Money Have Opportunity to Lead Securities Fraud Lawsuit" — PR Newswire (Stocks), 2026-07-16; "Marvell Drops 8% as AI Capex Slowdown Fears Weigh on Chips; Broadcom, AMD, and Intel Slide" — Yahoo Finance Top Stories, 2026-07-16; "Oil Pushes Above $85 as US Reserve Buffer Depletes: Will Crude Hit $100?" — BeInCrypto, 2026-07-15.
- Internal (this cycle, from `data/catalysts/2026-07-17/catalyst_cycle_00-31.md`): "Ondo Finance has partnered with Japan's SBI Group to tokenize Japanese assets and enable settlement using the JPYSC stablecoin" (narrative basket source, single_source, <24h); "Humanity Protocol (H) falls 15% as $36M hack returns to focus" — AMBCrypto (single_source).

**External web research note**: Internal `news_items` / report data was fresh, present, and consistent for all deep-dive candidates this cycle (ONDO, KAITO, BANK, AVGO, XOM) — no fresh WebSearch/WebFetch calls were needed per source-discipline rules (§G). No web tools were invoked this run.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, unchanged)
- **issue:** The stocks-intraday `stocks_intraday_7d_drawdown_guard` / `stocks_intraday_long_guard` combination continues to block 100% of A/B-scored candidates (compounded tonight by the market-closed demotion). Forward evidence this cycle (Model F paper_execution_r, 14d/30d all=-3.0R/PF0.40/n=10; would-have-been-A/B 14d net -42.5R/PF0.27) is unchanged from the last two reviews and continues to support the guard as reasonably calibrated, not over-tight — but this still needs an explicit human sign-off, not an automated conclusion.
- **evidence:** `data/reports/stocks/intraday/2026-07-17_00-47_stocks_intraday_report.md` §9 (Intraday A/B Quality — recent paper performance).
- **suggested manual fix:** Have a human formally confirm/close this TODO given the now-multi-cycle consistent negative forward evidence, or explicitly flag if a different calibration is intended.
- **priority:** medium
- **first observed:** 2026-07-16 18:39 EEST review (still open)

### TODO-2 (carried forward, not independently re-checked this cycle)
- **issue:** Several stocks B-tier signals in `active-signals` show `expires_at` timestamps in the past while still displaying non-terminal statuses (`tp1_hit`, `tp2_hit`, `triggered`) rather than a closed/expired terminal state.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` — e.g. XOM's older B-tier signal (expires 2026-07-14, in the past, tp2_hit), JPM (C, tp1_hit, expires 2026-07-11, 6 days in the past) — both still visible in tonight's `active-signals` output.
- **suggested manual fix:** have a human check whether the lifecycle/track-signals job is correctly terminalizing stocks signals past their `expires_at`.
- **priority:** medium
- **first observed:** 2026-07-16 16:20 EEST review (still open)

### TODO-3 (carried forward, unchanged this cycle — still high)
- **issue:** `detect_untracked_legacy_alerts` still returns exactly **2** unresolved results: ALLO/USDT (swing B, 65.4, sent 2026-07-16T14:27:05 UTC — now unresolved for **6th+ consecutive review cycle**, 14+ hours) and BANK/USDT (intraday B, 65.0, sent 2026-07-16T21:36:05 UTC — ~7h unresolved). No new watchlist alert fired for either symbol, or any other symbol, since 21:36 UTC yesterday (verified via direct SQL on `watchlist_alerts`, most recent row still id 1638).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-16` (2 results, unchanged) and `--since 2026-07-17` (0 new results today); direct SQL confirms no `watchlist_alerts` row newer than 2026-07-16T21:36:05 UTC.
- **suggested manual fix:** have a human check the watchlist-alert re-fire path for symbols whose most recent same-mode `proposed_signal` has already closed — unchanged recommendation from the 02:45 review; the issue is stable, not worsening, this cycle, which may make it easier to reproduce/debug on the two known symbols before it recurs on others.
- **priority:** high (unchanged — 2 symbols, ALLO/USDT now 14+ hours unresolved across 6+ review cycles)
- **first observed:** 2026-07-16 18:39 EEST review (ALLO/USDT); BANK/USDT observed 2026-07-17 02:45 EEST; unchanged 2026-07-17 04:39 EEST

### TODO-4 (carried forward, status unconfirmed this cycle)
- **issue:** The `paper entry-mode classify` scheduler step failed (exit=1) in cycle 6 (19:49 EEST, 2026-07-16) — a non-fatal failure that let the cycle continue. Not independently re-checked this cycle (tonight's cycle summary read, `cycle_01_03-12_summary.md`, showed 76/76 steps ok=76 failed=0 for the current cycle, but did not re-verify the specific prior-day step).
- **evidence:** `data/scheduled_runs/2026-07-16_default_schedule/scheduler.log` (previous day's folder, not re-read this cycle).
- **suggested manual fix:** have a human check whether this recurred in later cycles or was transient (first occurrence noted at 21:39 EEST 2026-07-16; tonight's cycle summary shows a clean 76/76, a mild positive signal that it may have been transient, but not confirmed against the specific step).
- **priority:** low
- **first observed:** 2026-07-16 21:39 EEST review

### TODO-5 (resolved this cycle — informational only)
- **issue:** The prior (02:45 EEST) post-close review fired ~3.5h late against its 23:15 EEST slot assignment. This cycle's 04:30-slot task fired on time (dispatched ~04:39 EEST against a 04:30 assignment, ~9min jitter — well within normal tolerance), suggesting the late-dispatch issue was transient rather than a persistent scheduling regression.
- **evidence:** This run's system clock read 2026-07-17 04:39-04:44 EEST against a 04:30 EEST slot assignment (~9min jitter, normal).
- **suggested manual fix:** no action needed this cycle; if the `opus-enriched-review-postclose` 23:15 slot fires late again on a future night, escalate back to high/medium — for now, treat as a one-off.
- **priority:** low (downgraded from the prior open item — on-time dispatch this cycle)
- **first observed:** 2026-07-17 02:45 EEST review; re-observed/downgraded 2026-07-17 04:39 EEST (on-time this cycle)
