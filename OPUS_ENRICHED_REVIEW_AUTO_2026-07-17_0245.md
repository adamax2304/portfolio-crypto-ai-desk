# Opus Enriched Review — post-close final daily review — Auto Cycle 02:45 EEST

## 1. Executive Summary

Slot: **post-close final daily review** (assigned 23:15 EEST; this run actually dispatched/executed at **02:45 EEST, 2026-07-17** — a ~3.5h delayed fire of the post-close sibling task, not ordinary dispatch jitter; see TODO-5). **Advisory only — no auto-trade, no code/scoring/routing changes.** Data pipeline healthy: scheduler.log 13min old, latest cycle summary ~1h49m old (not deferred). Crypto scalp/intraday fresh (~2h), crypto swing carry-forward (~9h11m, still in-band), stocks intraday very fresh (~1h49m, **after-hours planning-only** — US cash session is closed). **Daily wrap: crypto stayed 100% long-biased, zero A-tier, zero shorts fired** (19 signals) — **4 wins** (VIRTUAL/USDT×2, OPN/USDT×2, all tp3_hit), **11 stopped**, 1 entered-unresolved (VIRTUAL/USDT scalp, 0R display), 1 no-entry (BANK/USDT intraday, price moved away). **Catalyst confirmation was not a guarantee today**: the RWA-basket ONDO/USDT swing long (catalyst-confirmed via SBI tokenization + MEXC listing) **stopped at −1.0R**, while its basket-mate XLM/USDT swing long captured tp1+tp2 before a trailing stop for **+2.0R** — net positive for the basket thesis but a reminder that a fresh catalyst still needs technical confirmation. A separate ONDO/USDT **intraday** long (unrelated entry, opened 04:56 UTC) remains **open, tp2_hit, running toward tp3**. **Stocks stayed 100% C-tier all session** (38 signals, zero A/B) — market-closed planning demotion (all sessions) plus the pre-existing `stocks_intraday_7d_drawdown_guard`; forward paper evidence (Model F, 14d/30d) continues to show the demoted cohort net **−3.0R, PF 0.40**, and the would-have-been-A/B diagnostic shows **−42.5R / PF 0.27** over 14d — this keeps supporting the guard as correctly calibrated, not over-tight (TODO-1 stays open pending a human sign-off either way). **MSFT carries an active legal/headline gate** (securities-fraud shareholder-rights solicitation, PR Newswire) — AVOID/MANUAL REVIEW. **Two A-tier-scored stocks ideas (AVGO short, XOM long) are planning-only for tomorrow's 09:30 ET open** — chip-sector AI-capex-slowdown fear vs. an oil rally above $85, respectively. Crypto Fear & Greed is **still 25 (extreme fear)**, unchanged since 21:39 EEST, continuing to diverge from the dashboard's "bullish trend" crypto-regime label (report-level BTC trend itself reads **range**, not trend — an internal label inconsistency worth noting, not a fault). **System-integrity issue escalated**: `detect_untracked_legacy_alerts` now shows **2** unresolved (ALLO/USDT, unresolved 5th+ consecutive review cycle since 14:27 UTC; **BANK/USDT newly joined at 21:36 UTC**, confirming the root cause is systemic across symbols, not ALLO-specific — TODO-3 raised to **high**). Scanning, tracking, and all monitors continue unaffected — **no recommendation to pause anything.**

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-16_21-30_scalp_report.md` (~2h08m old), `data/reports/intraday/2026-07-16_21-36_intraday_report.md` (~2h02m old, regime range/chop), `data/reports/swing/2026-07-16_14-27_swing_report.md` (~9h11m old, carry-forward band), `data/reports/stocks/intraday/2026-07-16_21-49_stocks_intraday_report.md` (~1h49m old, after-hours planning-only). Stocks swing/invest last generated 2026-07-02 — deprecated legacy framework, excluded (>14h stale by design).
- Catalyst: `data/catalysts/2026-07-16/catalyst_events.jsonl` (5000 rows cumulative today), `narrative_baskets.jsonl` (5 baskets), `data/catalysts/2026-07-16/catalyst_cycle_23-39.md` (latest cycle, 500 scanned). Catalyst folder for the UTC calendar day (`2026-07-16`) was already present; ran the one allowed `catalyst-scan` CLI to refresh the latest cycle file (cheap, read-only per §A.4).
- LLM packets: `data/processed/llm_analysis_packet.md` (~2h09m old), `data/processed/llm_stocks_packet.md` (~1h55m old).
- DB (direct SQL, `db/crypto_ai_desk.sqlite`): `proposed_signals`, `signal_outcomes`, `watchlist_alerts`, `news_items`, `market_dashboard_snapshots`.
- CLI: `active-signals` ×2, `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-16`.
- Scheduler: `data/scheduled_runs/2026-07-17_default_schedule/scheduler.log`, `cycle_01_00-22_summary.md`.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-16_2139.md` (late-session risk review, 21:39 EEST) — used for TODO carry-forward, thesis tracking (ONDO/BANK/UNH), and integrity-issue history (ALLO).

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **02:25 EEST**, latest `cycle_01_00-22_summary.md` mtime **00:56 EEST** — both well under the 3h defer threshold at review start (02:45). **Not deferred.**
- Crypto scalp/intraday: fresh (~2h). Crypto swing: ~9h11m old — **carry-forward band** (4–12h), used with that caveat.
- Stocks intraday: ~1h49m old, generated **after-hours** — US cash session is closed; every name is `market_closed_intraday_planning_only` (A/B demoted to C, planning levels only). This is expected behavior at this hour, not a fault.
- Stocks swing/invest: last generated 2026-07-02 (15 days stale) — known, intentionally-deprecated legacy framework superseded by the shadow-only position-candidates framework; not a freshness fault.
- Catalyst directory present for the UTC trading day; ran `catalyst-scan --no-print` once (missing latest-cycle file), which is why the folder shows as `2026-07-16` even though the local EEST wall clock has rolled into 07-17 — the app's "today" boundary is UTC-based, and UTC is still 2026-07-16 at 02:45 EEST.
- Monitors: not independently re-verified this cycle (read-only CLI list in §A.4 does not include a monitor-status command); no anomaly reported in the scheduler summary read.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-07-17 02:45 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["monitor process status not re-checked this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 02:25 EEST (13min old), cycle summary 00:56 EEST (~1h49m old)", "crypto scalp/intraday ~2h old, crypto swing ~9h11m carry-forward", "stocks intraday ~1h49m fresh but after-hours planning-only", "stocks swing/invest deprecated, 15d stale by design", "this run itself fired ~3.5h late vs its 23:15 EEST slot assignment"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["mixed", "chop", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["dashboard crypto_market_mode=trend / crypto_regime=bullish trend, but the intraday report's own BTC trend=range (label inconsistency)", "ETH trend uptrend, altcoin breadth 47.5%/47.5% (neutral)", "Fear & Greed still 25 (extreme fear), unchanged since 21:39 EEST — persistent divergence vs the bullish-trend label", "stocks_market_mode=chop, stocks_regime=chop, VIX 16.73 (low-normal), SPY flat, QQQ downtrend, market closed"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "catalyst_confirmed", "narrative_supported", "catalyst_contradicted"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["5000 catalyst events today, 1025 mapped (20.5%), 3975 unmapped (79.5%) — weak mapping", "RWA basket (ONDO+XLM) catalyst-confirmed via SBI/MEXC/Tradable-Stellar news, but today's realized outcome was mixed: ONDO swing stopped -1.0R, XLM swing +2.0R", "BANK/USDT explicitly 'no fresh verified catalyst detected' in both the 14:27 swing and 21:36 intraday setups, plus a known negative-expectancy playbook note (14d no-news cut: WR 23% / PF 0.70 / -3R)", "MSFT active legal_risk flag: securities-fraud shareholder-rights PR Newswire solicitation"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "ok",
      "confidence": 0.45,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["OI for most non-BTC/ETH symbols", "OI/funding for AVGO/XOM (equities, not applicable)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT: price up + OI up 38.08%, funding 5e-05 (low, not extreme), crowding normal — fresh positioning, not a squeeze"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["price_moved_away", "chase_risk", "entry_late", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT swing entry zone (0.05614-0.05736, set 14:27 UTC) now sits below the fresh intraday pullback zone (0.0597-0.0609, 21:36 UTC) — price has moved up and away; swing fill, if it happens, would be into a deeper, staler zone", "ONDO/USDT intraday tp2_hit — managing toward tp3, not a fresh entry, no chase risk for the existing position", "AVGO/XOM are A-pretier planning-only ideas — genuinely fresh entries would require 09:30 ET RTH confirmation, not a market-closed fill"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "entered_unresolved", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto today (19 signals, all long): CLOSED WIN(tp3_hit)=4, CLOSED LOSS(stopped)=11, ENTERED UNRESOLVED (0R display)=1 (VIRTUAL/USDT scalp), NO-ENTRY/MOVED AWAY=1 (BANK/USDT intraday), WAITING for entry=1 (BANK/USDT swing), OPEN actionable (tp2_hit running)=1 (ONDO/USDT intraday)", "stocks today (38 signals, all C-tier/shadow): CLOSED LOSS(stopped)=17, NO-ENTRY/STALE=8, REVIEW/SHADOW (triggered/tp1/tp2 running)=11, WAITING for entry=1, NEEDS REVIEW(ambiguous)=1"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT: active securities-fraud shareholder-rights class-action solicitation (PR Newswire) — tier demoted B(74)->C, AVOID/MANUAL REVIEW", "UNH/NFLX both earnings-blocked today (block_requires_operator_review, do_not_chase_warning)", "stocks_intraday_7d_drawdown_guard forward evidence continues to support suppression: 14d/30d paper_execution_r all=-3.0R/PF0.40 (n=10), would-have-been-A/B(14d, incl. demoted) net -42.5R/PF0.27"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "bad",
      "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B(B-tier) weekly: n=160, winrate 21.8%, PF 1.7361, avgR 0.2172, totalR +26.50 — profitable overall via R:R asymmetry", "crypto scalp mode losing: n=36 (33 triggered), 0 wins/7 losses, PF 0.40, totalR -3.0 — a real losing bucket", "crypto short direction losing (n=6, PF 0.25, anecdotal sample)", "stocks A/B weekly: n=14 (weak confidence), winrate 28.6%, PF 0.6667, avgR -0.125, totalR -1.0 — losing; C-tier n=210, PF 0.77, totalR -9.0; semiconductors/technology/crypto_equity sectors particularly bad (PF 0.10-0.17)", "BANK/USDT's own momentum-no-catalyst playbook bucket: 14d WR 23% / PF 0.70 / -3R — negative expectancy"]
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
    "best_long_candidate":     { "symbol": "XOM", "trigger": "planning-only, A-pretier score 89 — wait for 09:30 ET RTH confirmation before any fill; oil >$85 rally thesis", "reason": "energy is today's strongest sector (RS +2.95-3.00% vs SPY 20d), oil breakout narrative fresh, but no live level published in this excerpt — do not fabricate entry/stop until the fresh report prints them" },
    "best_short_candidate":    { "symbol": "AVGO", "trigger": "planning-only, A-pretier score 90 — wait for 09:30 ET RTH confirmation; AI-capex-slowdown fear (Marvell -8%, Broadcom/AMD/Intel sliding) thesis", "reason": "semiconductors are today's weakest sector (RS -7.69% vs SPY 20d), fresh negative sector headline same-day" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "already open (intraday, B-tier, tp2_hit) — manage toward tp3 0.0700 area; do not chase above current levels", "reason": "RWA/tokenization basket, catalyst-confirmed (SBI deal + MEXC listing), sibling swing signal stopped -1R today but basket-mate XLM/USDT captured +2R — net-positive basket thesis despite one losing leg" },
    "avoid_candidate":         { "symbol": "MSFT", "reason": "active securities-fraud shareholder-rights class-action solicitation (PR Newswire, 2026-07-16) — tier demoted B->C, AVOID/MANUAL REVIEW; do not treat any MSFT setup as clean until resolved" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.55 | mixed, chop, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, catalyst_confirmed, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | ok | 0.45 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | price_moved_away, chase_risk, entry_late, stale_before_entry | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry, review_shadow, entered_unresolved, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | bad | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (21:39 EEST)

- **Resolved since 21:39**: ONDO/USDT **swing** long (was "best long candidate," triggered, catalyst-confirmed) → **stopped, −1.0R**. XLM/USDT **swing** long (was "best catalyst candidate," tp2_hit, running) → **stopped after tp1+tp2, +2.0R** (trailing-stop-style exit, net win). Both were flagged catalyst-confirmed at 21:39; today's realized outcome for the basket is net **+1.0R** across the two legs, but the individual-symbol result is mixed, not a clean sweep.
- **Still running**: ONDO/USDT **intraday** (separate signal, unrelated entry, opened 04:56 UTC) — unchanged status, tp2_hit, still open toward tp3.
- **Unchanged / still waiting**: BANK/USDT swing (created 14:27 UTC) — still `waiting_for_entry` at the same zone (0.05614-0.05736) 12+ hours later; price has since moved up (fresh 21:36 UTC intraday pullback zone is now 0.0597-0.0609), so the swing zone is increasingly stale relative to current price action.
- **Escalated**: `detect_untracked_legacy_alerts` — ALLO/USDT is now unresolved for a **5th+ consecutive review cycle** (18:39 → 21:39 → this run, same 14:27 UTC alert, same root-cause signal_id reuse). **New**: BANK/USDT joined the untracked list at 21:36 UTC (a fresh intraday watchlist alert fired with no matching `proposed_signal` — verified directly: the only intraday BANK/USDT signal was `entry_moved_away` and already closed before 21:36). This is the same failure pattern on a second symbol, confirming it is systemic in the watchlist-alert re-fire path, not ALLO-specific. TODO-3 priority raised **medium → high**.
- **Unchanged**: Catalyst mapping stays weak (19.6% at 21:39 → 20.5% now, materially unchanged, cumulative-day denominator). Crypto Fear & Greed unchanged at 25 (extreme fear). Stocks stayed 100% C-tier all session (drawdown guard + now also market-closed demotion).
- **New context**: MSFT's securities-fraud legal flag (present in the catalyst top-10 already at 21:39 implicitly via the catalyst scan) is now explicitly confirmed gating MSFT B(74)->C in the fresh stocks report.
- **New issue**: This run itself is a ~3h20-30m late dispatch of the 23:15 EEST post-close slot (see TODO-5) — noted for completeness, does not affect the review's data validity since freshness checks independently passed.

## 5. Catalyst Coverage

- Catalyst events today (cumulative, UTC day 2026-07-16): **5000** scanned, **1025 mapped (20.5%)**, **3975 unmapped (79.5%)**. Narrative baskets: **5**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (Consistent with the known ~17-20% baseline from prior news-layer hardening work — not a new regression.)
- Top 3 (most recent) unmapped headlines: "Keyrock acquires BlockFills trading assets to expand institutional crypto business"; "The Clarity Act is the most important consumer protection effort in years"; "Crypto for Advisors: Strengthening defenses against AI fraud".
- Mapped/basket-confirmed narratives in play: RWA/tokenization (ONDO/USDT + XLM/USDT, primary, mixed realized result today +1R net); perps-DEX (HYPE/USDT primary, DYDX/GMX/ASTER related); Binance ecosystem teaser (BNB/USDT primary, ASTER related); delisting/thin-liquidity capitulation (BTC/USDT primary — avoid-low-liquidity playbook, unrelated to BTC's own price action); momentum-breakout basket (BANK/USDT primary, explicitly labeled "without confirmed catalyst").

## 6. Market Landscape

### Crypto
- Regime: dashboard label **bullish trend**, but the intraday/scalp reports' own read is **BTC trend = range**, ETH trend = **uptrend** — an internal inconsistency, treat the report-level read (range/chop, neutral) as primary since it's the more granular source. Altcoin breadth above EMA20 **47.5%**, above EMA50 **47.5%** (neutral/mixed, narrow leadership). Volatility normal (ATR percentile 32).
- Fear & Greed: **25 (extreme fear)**, unchanged since 21:39 EEST — still diverging from any "bullish" framing; treat as a sentiment headwind.
- Strongest: BANK/USDT (score 93.4, +17.6% 24h, no catalyst), KAITO/USDT (score 91.0, +9.5% 24h), MANTRA/USDT (score 87.8, +11.8% 24h, no catalyst), VIRTUAL/USDT (score 84.1, +5.5% 24h — today's 2× tp3_hit winner). Weakest: HOME/USDT (-22.5% 24h), DODO/USDT (-21.9% 24h), SNDKB/USDT (-11.8% 24h) — no active signals either direction, no fresh news confirming the weakness thesis.

### Stocks
- Regime: **chop** (both dashboard mode and report label agree), risk-on **False**, VIX **16.73** (low-normal), breadth 75%/75% above EMA20/50 (healthy breadth despite chop label). SPY flat/uptrend (+0.05% 20d), DIA uptrend (+0.65% 20d), QQQ **downtrend** (-3.28% 20d), IWM range.
- Strongest sectors: healthcare (XLV, RS +5.74% vs SPY 20d), financials (XLF, +4.36%), energy (XLE, +2.95%). Weakest: semiconductors (SMH, -7.69%), technology (XLK, -4.84%), materials (XLB, -3.52%).
- Market status: **closed (after-hours)** — every intraday A/B idea is demoted to C, planning-only until the 09:30 ET open. Earnings today: NFLX, UNH (both swing-blocked).
- Legal/headline gate active: **MSFT** (securities-fraud PR-Newswire shareholder-rights solicitation).

### Market Mood / Risk Routing

- Crypto mood: **mixed** (internal regime-label inconsistency, neutral altcoin breadth, extreme-fear sentiment divergence, and today's mixed catalyst-confirmed outcome — not a clean risk-on read despite the "bullish trend" dashboard tag)
- Stocks mood: **closed / chop** (US cash session closed; regime label chop with healthy breadth; sector rotation firmly into healthcare/financials/energy and out of semis/technology)
- Dominant narrative: RWA/tokenization (ONDO/XLM, mixed realized result) in crypto; AI-capex-slowdown fear (semis/tech weak) vs. oil-rally strength (energy) in stocks
- Preferred side now: **catalyst-backed only, cautious** (crypto) / **wait-for-RTH-confirmation** (stocks — nothing fills before 09:30 ET)
- Best long candidate: **XOM** (stocks, planning-only, A-pretier — trigger: RTH confirmation at the 09:30 ET open); crypto has no fresh actionable long beyond managing the existing ONDO/USDT intraday position
- Best short candidate: **AVGO** (stocks, planning-only, A-pretier — trigger: RTH confirmation); crypto has zero active shorts (100% long-biased all day)
- Best catalyst-backed candidate: **ONDO/USDT** (intraday, open, tp2_hit — manage toward tp3; RWA basket)
- What to avoid: **MSFT** (active legal/headline gate); **BANK/USDT as a chase** (explicitly no-catalyst, negative-expectancy playbook bucket, and now also the source of a new untracked-alert integrity issue)
- What would change the view: a fresh, verified `news_items` hit on BANK/USDT; resolution (positive or negative) of the MSFT securities-fraud matter; RTH price action on AVGO/XOM confirming or invalidating the planning levels; a human decision on TODO-1 (drawdown-guard calibration) and TODO-3 (untracked-alert root cause, now affecting 2 symbols)

## 7. Candidate Deep Dives

### 1. MSFT — avoid, stocks, legal/headline risk (B pre-gate, demoted to C)
- Score 74 pre-gate. Demoted B→C for **active legal/headline risk (securities_fraud)** — "Microsoft Corporation (MSFT) Shareholders Who Lost Money Have Opportunity to Lead Securities Fraud Lawsuit" (PR Newswire (Stocks), 2026-07-16) — plus market-closed planning-only.
- Has price already reacted? Not verified in this excerpt — no price-impact data cross-checked; treat as headline-only for now.
- Is this a chase-risk setup? N/A — not actionable, correctly gated.
- Catalyst confirmation or contradiction? This class of PR-Newswire "shareholder rights" release is typically a law-firm investor solicitation rather than a confirmed adjudicated fraud finding — still correctly treated as a gating headline-risk event per protocol; not itself proof of wrongdoing.
- Actionable level: none — verdict is **AVOID / MANUAL REVIEW**, not a level-based trade idea.
- What would invalidate the avoid: the gate would need a human to review the underlying legal matter and confirm it is stale/non-material before any A/B MSFT idea should be treated as clean.

### 2. ONDO/USDT — long, catalyst-backed, crypto (B, intraday, open tp2_hit)
- Intraday leg (sig_a914cdba49291324): entry 0.36520-0.36970, invalidation 0.35971, currently **tp2_hit**, open toward tp3 (~0.41-area extrapolated from the swing sibling's target ladder; exact intraday tp3 not re-confirmed this cycle — do not assume the swing tp3 applies to a different signal_id).
- Sibling swing leg (sig_b5561a1b247ead39, entry 0.37805-0.38210): **stopped, -1.0R** since the 21:39 review — the catalyst (SBI tokenization deal, MEXC tokenized-stock listing) was real and verified, but price still reversed through the swing stop. Catalyst confirmation reduced but did not eliminate downside risk.
- Has price already reacted to the catalyst? Yes, substantially (+17% 24h at the time of the 21:39 review); the swing stop-out suggests the move was largely priced by the time that entry filled.
- Chasing? No for the existing intraday position (already deep in profit, tp2_hit); yes for any fresh entry now, given the swing sibling's failure.
- Is it aligned with market mood? Marginally — one of the few catalyst-confirmed names in an otherwise mixed/chop crypto tape, but today's realized result (net +1R across ONDO -1R / XLM +2R) argues for smaller size on repeat catalyst plays, not blind confidence.
- Actionable level: manage the existing intraday position; do not add on new catalyst-only conviction without a fresh technical trigger.
- Invalidation: 0.35971 (intraday stop).
- Catalyst confirmation: confirmed (SBI + MEXC), but proven insufficient on its own for the swing leg today.

### 3. BANK/USDT — long-watch, crypto, no catalyst + integrity flag (B, swing waiting / intraday no-signal)
- Swing leg (sig_ff3e8319e73a112d): entry 0.05614-0.05736, invalidation 0.05464, still `waiting_for_entry` 12+ hours after creation (14:27 UTC).
- A fresh **intraday** setup was generated at 21:36 UTC (score 66.1, pullback entry 0.0597-0.0609, invalidation 0.0581, targets 0.0643/0.0671/0.0700) but **no proposed_signal was minted for it** — a watchlist alert (id 1638) fired with no matching signal, the same failure mode as the long-unresolved ALLO/USDT case. See TODO-3.
- Catalyst: explicitly **"no fresh verified catalyst detected"** in the report's own evidence section, both today and at 21:39. The desk's own playbook note for this bucket: "No-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation" (14d cut: WR 23% / PF 0.70 / -3R).
- Has price already reacted? Yes, +17.6% 24h, +73.7% 7d — most of the momentum has already happened.
- Chasing? Elevated — pure momentum/RS play, no fundamental backstop, and price has moved up away from the older swing entry zone.
- Actionable level: swing fill at 0.05614-0.05736 (increasingly stale, deep pullback); intraday pullback fill at 0.0597-0.0609 (fresher, but the corresponding signal was never minted — treat as report-level context only, not a trackable trade).
- Would invalidate the long-watch thesis: a 1h close below 0.05464 (swing) / 0.0581 (intraday reference); confirmed absence of any real news catalyst continuing.
- Chase risk: **elevated** — desk's own no-catalyst, negative-expectancy classification.

### 4. AVGO — short-watch, stocks, planning-only (A pre-gate, demoted to C for market-closed)
- Score 90 pre-gate, short direction. Demoted A→C solely for `market_closed_intraday_planning_only` — not a quality or risk-based demotion.
- Catalyst/narrative: same-day sector headline — "Marvell Drops 8% as AI Capex Slowdown Fears Weigh on Chips; Broadcom, AMD, and Intel Slide" (Yahoo Finance Top Stories, 2026-07-16); semiconductors are today's weakest sector (RS -7.69% vs SPY 20d).
- No specific entry/stop/TP levels were published in the watchlist excerpt read this cycle — **do not fabricate**; the fresh 09:30 ET report will need to be re-checked before this becomes a live actionable idea.
- Aligned with market mood? Yes — cleanest short-side sector alignment on the board tonight.
- Actionable level: not actionable now (market closed); would need RTH confirmation and a fresh level print at the next report cycle.
- Would invalidate: a positive AI-capex surprise or a broad semis bounce at the open.

### 5. XOM — long-watch, stocks, planning-only (A pre-gate, demoted to C for market-closed)
- Score 89 pre-gate, long direction. Demoted A→C solely for `market_closed_intraday_planning_only`.
- Catalyst/narrative: "Oil Pushes Above $85 as US Reserve Buffer Depletes: Will Crude Hit $100?" (BeInCrypto, 2026-07-15); energy is one of today's strongest sectors (RS +2.95% vs SPY 20d).
- No specific entry/stop/TP levels were published in the watchlist excerpt read this cycle — do not fabricate; re-check at the next fresh report.
- Aligned with market mood? Yes — energy strength is one of the cleanest sector trends today, contrasting with weak tech/semis.
- Actionable level: not actionable now (market closed); RTH confirmation required.
- Would invalidate: an oil-price reversal below $85 or an energy-sector rotation reversal at the open.

**Excess candidates not deep-dived**: XLM/USDT (already closed, +2.0R win, RWA basket — covered in §4 as color, not a live idea); COIN/SPY/DIA stocks C-tier shorts (still `waiting_for_entry`/`triggered`, carried from earlier in the session, shadow-tracked only); MSTR/SMH/XLK/XLV/PLTR C-tier watchlist names (planning-only, market-closed demotion, same as AVGO/XOM but lower pre-gate scores).

## 8. Best Candidates Ranked

1. **ONDO/USDT long** (crypto, B, intraday, open tp2_hit) — catalyst-backed, actionable now (manage existing position toward tp3). Trigger: N/A, already filled.
2. **XOM long-watch** (stocks, A-pretier, planning-only) — energy-sector strength + oil-rally catalyst. Trigger: RTH confirmation at 09:30 ET, fresh level print required.
3. **AVGO short-watch** (stocks, A-pretier, planning-only) — semis-sector weakness + AI-capex-slowdown headline. Trigger: RTH confirmation at 09:30 ET, fresh level print required.
4. **BANK/USDT long-watch** (crypto, B, waiting/no-signal) — momentum-only, explicitly no catalyst, negative-expectancy playbook bucket; treat as lower-confidence chase risk. Trigger: swing fill 0.05614-0.05736 or intraday pullback 0.0597-0.0609, both requiring a fresh catalyst check before entry.
5. **MSFT avoid** (stocks, legal/headline gate) — do not treat as clean until the securities-fraud matter is reviewed.

## 9. Avoid / No Trade (this decision window only)

- **MSFT** — AVOID / MANUAL REVIEW. Active securities-fraud shareholder-rights solicitation (PR Newswire, 2026-07-16). This applies to this decision window only — scanning and tracking continue.
- **BANK/USDT as a chase** — explicitly no confirmed catalyst per the report's own evidence section and playbook classification (14d no-news cut: WR 23% / PF 0.70 / -3R); also implicated in an unresolved system-integrity issue (TODO-3).
- **New crypto scalp entries generally** — weekly scalp-mode stats show 0 wins / 7 losses, PF 0.40, totalR -3.0 over the sample read; not a fault to fix here, just a caution for this window.
- Scanning, candidate generation, tracking, and outcome recording continue unaffected across all of the above — this is a per-symbol/per-window caution, never a system-wide stop.

## 10. Main Risks

- Crypto Fear & Greed stuck at 25 (extreme fear) for at least two consecutive review cycles, still diverging from any bullish framing — a fragile-sentiment backdrop into the Asia session.
- BANK/USDT's watchlist-alert integrity issue is now confirmed on a **second symbol** (ALLO/USDT + BANK/USDT) — if the root cause (signal_id reuse on re-fired watchlist alerts) is truly systemic, more symbols could silently accumulate untracked Telegram alerts that never contribute to PF/winrate tracking.
- `stocks_intraday_7d_drawdown_guard` continues to suppress 100% of A/B stock names; forward evidence (14d/30d paper_execution_r -3.0R, would-have-been-A/B -42.5R) keeps supporting the guard, but TODO-1 (human calibration confirmation) remains formally open.
- Catalyst-confirmed does not equal guaranteed win — today's ONDO/USDT swing loss despite real, verified news is a concrete reminder for tomorrow's routing.
- This run's own ~3.5h dispatch delay (TODO-5) means the true "post-close" wrap is reviewing data that is itself already ~5-6h old relative to the actual US close; treat the "overnight-into-Asia" framing below as current as of 02:45 EEST, not as of the close itself.

## 11. Action Plan — next 4 hours (into the 04:30 EEST overnight/Asia slot)

- Manage the open ONDO/USDT intraday position (tp2_hit) toward tp3; no new action needed.
- Do not chase BANK/USDT above the stated zones without a fresh, verified catalyst check; if either the swing or intraday level fills, size it as a lower-confidence, no-catalyst position.
- Watch for AVGO/XOM level prints in the next fresh stocks report ahead of the 09:30 ET open; do not treat tonight's planning-only scores as tradeable levels until re-confirmed.
- No stocks A/B expected to fire before the US open (market closed) and likely remains guard-suppressed after the open per TODO-1's unresolved status.
- Next scheduled review (04:30 EEST, crypto overnight/Asia) should reconcile: whether BANK/USDT's untracked intraday alert recurs a third time (escalation signal for TODO-3), whether Fear & Greed moves off 25, and whether ONDO/USDT intraday resolves to tp3 or reverses.

## 12. Final Verdict per Mode

- **Crypto scalp**: **avoid new entries** — weekly sample shows 0 wins/7 losses, PF 0.40, totalR -3.0; one signal today entered-unresolved (VIRTUAL/USDT, 0R display).
- **Crypto intraday**: **watch/manage** — ONDO/USDT open (tp2_hit, catalyst-backed); no new intraday trigger of note.
- **Crypto swing**: **catalyst-backed only, cautious** — today's realized results were mixed (ONDO -1R, XLM +2R); BANK/USDT remains a no-catalyst chase-risk watch, not a clean actionable.
- **Stocks intraday**: **watch_only / planning_only** — market closed, zero A/B all session (guard + closed-session demotion); AVGO/XOM are the cleanest planning ideas for tomorrow's RTH open, pending fresh levels.
- **Stocks swing/invest**: dormant (deprecated legacy framework) — no verdict needed.

## 13. Sources

- Internal: `data/reports/scalp/2026-07-16_21-30_scalp_report.md`, `data/reports/intraday/2026-07-16_21-36_intraday_report.md`, `data/reports/swing/2026-07-16_14-27_swing_report.md`, `data/reports/stocks/intraday/2026-07-16_21-49_stocks_intraday_report.md`, `data/catalysts/2026-07-16/catalyst_events.jsonl`, `data/catalysts/2026-07-16/narrative_baskets.jsonl`, `data/catalysts/2026-07-16/catalyst_cycle_23-39.md`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `signal_outcomes`, `watchlist_alerts`, `news_items`, `market_dashboard_snapshots`), `data/scheduled_runs/2026-07-17_default_schedule/scheduler.log`.
- Reused from prior review (21:39 EEST, internal source, <24h old, uncontradicted by fresher `news_items` this cycle): [Ondo Hits 1-Month High: Here Is What's Driving The 17% Surge — BeInCrypto](https://beincrypto.com/) (2026-07-16, 11:41 UTC); [SBI extends onchain finance push with Ondo deal to tokenize Japanese stocks — The Block](https://www.theblock.co/) (2026-07-16, 10:59 EDT); [MEXC to Launch Ondo Tokenized Stock Trading Pairs on Spot Markets — t.me/MEXC_OfficialAnnouncements](https://t.me/MEXC_OfficialAnnouncements) (2026-07-16, 08:31 UTC).
- Internal (this cycle, from `data/reports/stocks/intraday/2026-07-16_21-49_stocks_intraday_report.md` §4): "Microsoft Corporation (MSFT) Shareholders Who Lost Money Have Opportunity to Lead Securities Fraud Lawsuit" — PR Newswire (Stocks), 2026-07-16; "Marvell Drops 8% as AI Capex Slowdown Fears Weigh on Chips; Broadcom, AMD, and Intel Slide" — Yahoo Finance Top Stories, 2026-07-16; "Oil Pushes Above $85 as US Reserve Buffer Depletes: Will Crude Hit $100?" — BeInCrypto, 2026-07-15.

**External web research note**: Internal `news_items` / report data was fresh, present, and consistent for all deep-dive candidates this cycle (MSFT, ONDO, BANK, AVGO, XOM) — no fresh WebSearch/WebFetch calls were needed per source-discipline rules (§G). No web tools were invoked this run.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, unchanged)
- **issue:** The stocks-intraday `stocks_intraday_7d_drawdown_guard` / `stocks_intraday_long_guard` combination continues to block 100% of A/B-scored candidates (compounded tonight by the market-closed demotion). Fresh forward evidence this cycle (Model F paper_execution_r, 14d/30d all=-3.0R/PF0.40; would-have-been-A/B 14d net -42.5R/PF0.27) continues to support the guard as reasonably calibrated, not over-tight — but this still needs an explicit human sign-off, not an automated conclusion.
- **evidence:** `data/reports/stocks/intraday/2026-07-16_21-49_stocks_intraday_report.md` §9 (Intraday A/B Quality — recent paper performance).
- **suggested manual fix:** Have a human formally confirm/close this TODO given the now-multi-cycle consistent negative forward evidence, or explicitly flag if a different calibration is intended.
- **priority:** medium
- **first observed:** 2026-07-16 18:39 EEST review (still open)

### TODO-2 (carried forward, unchanged)
- **issue:** Several stocks B-tier signals in `active-signals` show `expires_at` timestamps in the past while still displaying non-terminal statuses (`tp1_hit`, `tp2_hit`, `triggered`) rather than a closed/expired terminal state.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` — e.g. XOM (B, tp2_hit, expires_at 2026-07-14, 3 days in the past), JPM (C, tp1_hit, expires_at 2026-07-11, 6 days in the past).
- **suggested manual fix:** have a human check whether the lifecycle/track-signals job is correctly terminalizing stocks signals past their `expires_at`.
- **priority:** medium
- **first observed:** 2026-07-16 16:20 EEST review (still open)

### TODO-3 (carried forward, escalated: medium → high)
- **issue:** `detect_untracked_legacy_alerts` now returns **2** unresolved results: ALLO/USDT (swing B, 65.4, sent 2026-07-16T14:27:05 UTC — unresolved for a **5th+ consecutive review cycle**, 12+ hours) and **newly**, BANK/USDT (intraday B, 65.0, sent 2026-07-16T21:36:05 UTC). Direct SQL confirms BANK/USDT's only intraday `proposed_signal` (`sig_1a5f0246e9a3d148`, created 14:26:18 UTC) was already `entry_moved_away`/closed before the 21:36 alert fired — no fresh `proposed_signal` was minted for the new intraday setup, the same pattern as ALLO/USDT's stale signal_id reuse.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-16`; direct SQL on `watchlist_alerts` (id 1638, BANK/USDT, 21:36:05 UTC) vs `proposed_signals` (no matching intraday BANK/USDT signal created near that time).
- **suggested manual fix:** have a human check the watchlist-alert re-fire path for symbols whose most recent same-mode `proposed_signal` has already closed — the re-fire appears to either reuse a stale signal_id or fail to mint a new one, and this now reproduces on a second, unrelated symbol, confirming it is systemic rather than symbol-specific.
- **priority:** high (raised from medium — now confirmed on 2 symbols, and ALLO/USDT has gone unresolved for 12+ hours across 5+ review cycles)
- **first observed:** 2026-07-16 18:39 EEST review (ALLO/USDT); BANK/USDT newly observed 2026-07-17 02:45 EEST

### TODO-4 (carried forward from 21:39, status unconfirmed this cycle)
- **issue:** The `paper entry-mode classify` scheduler step failed (exit=1) in cycle 6 (19:49 EEST, 2026-07-16) — a non-fatal failure that let the cycle continue. Not independently re-checked this cycle (cycle summary read was for cycle 1 of the new UTC day, 00:22-00:56 EEST, not cycle 6).
- **evidence:** `data/scheduled_runs/2026-07-16_default_schedule/scheduler.log` (previous day's folder).
- **suggested manual fix:** have a human check whether this recurred in later cycles or was transient (first occurrence noted at 21:39 EEST).
- **priority:** low
- **first observed:** 2026-07-16 21:39 EEST review

### TODO-5 (new)
- **issue:** This scheduled post-close run fired at **02:45 EEST (2026-07-17)** against its assigned **23:15 EEST** slot — a delay of roughly 3.5 hours, well beyond the "a few minutes of dispatch jitter" tolerance described in the routine's SLOT AWARENESS section. The freshness checks (§D) still passed independently, so the review content itself is not stale, but the slot-timing assumption ("run shortly after the market scheduler completes a cycle, close to the named local time") did not hold this cycle.
- **evidence:** System clock at execution time read 2026-07-17 02:38-02:45 EEST; the task was dispatched under the `opus-enriched-review-postclose` name for the 23:15 EEST slot.
- **suggested manual fix:** have a human check the `opus-enriched-review-postclose` scheduled-task trigger/queue for why it fired ~3.5h late (e.g. a missed trigger window, a backlog, or a host/agent availability gap) — this is an infrastructure/scheduling issue outside this routine's own read-only scope.
- **priority:** low
- **first observed:** 2026-07-17 02:45 EEST (this run)
