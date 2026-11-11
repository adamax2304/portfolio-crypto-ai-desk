# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (16:20 EEST / 13:20 UTC, ~10 min before the 09:30 ET cash open). Advisory only — no auto-trade, no scoring/strategy changes.

Crypto regime label is still "bullish trend / risk-on" on trend structure (BTC/ETH uptrend, 76-79% breadth above EMA20), but BTC/ETH/SOL are showing **price-down + OI-down (deleveraging)** right now and macro risk score is pinned at **100/100** on active Iran-US military escalation (oil at $89 Brent / $83 WTI, 9-10 consecutive nights of strikes) — a genuine, externally-confirmed risk-off headwind, not noise. No A-tier setups anywhere (crypto or stocks). Crypto B-tier book is mostly *already-running* positions (11 tp1_hit, 7 tp2_hit) rather than fresh entries; the only clean **waiting-for-entry** setup is AKE/USDT. A **live system bug recurred this cycle**: ERA/USDT and EPIC/USDT fired 4 raw Telegram watchlist alerts today with **no backing proposed_signal** (untracked, won't score) — same defect as the 2026-07-17 ALLO/BANK case, now a repeat offender (§14). Stocks: still **chop regime, VIX 17.6**, cash market closed pre-open with **zero current/compatible A/B intraday candidates**; the demoted near-A/B shortlist (UNH, XOM, JPM, AVGO, COIN) is the pre-open watchlist. **UNH stays AVOID** — externally re-confirmed live DOJ criminal+civil Medicare-billing investigation. A major overnight catalyst needing explicit gap-risk framing: **Iran's IRGC claims a cruise-missile strike destroyed AWS/Amazon data infrastructure in Bahrain** — reported by CNBC/Euronews/Jerusalem Post but **disputed by Bahrain** (says it intercepted the attack, denies commercial infrastructure was hit) and **unconfirmed by AWS/US officials**; treat as elevated, unresolved headline risk into the open, not a confirmed fact. GOOGL, TSLA, NOW report earnings today — do not chase. Catalyst mapping is weak again this run (81.1% unmapped).

## 2. Data Used

- Crypto reports: scalp (2026-07-22 11:42 EEST), intraday (11:48 EEST, freshness 11:45 UTC — fresh, ~2h35m old), swing (04:16 EEST / 01:15 UTC — **borderline stale, ~12h07m old**, used for narrative context only, not fresh entry timing).
- Stocks intraday report (2026-07-22 15:14 EEST / 12:14 UTC generation, data freshness 12:14 UTC) — market closed pre-open, planning-only.
- Stocks swing/invest reports: stale since 2026-07-02 (20 days) — excluded, per known deprecation of the old swing/invest pipeline ([[project_crypto_ai_desk_stocks_position_framework]]).
- `data/catalysts/2026-07-22/catalyst_events.jsonl` (2500 events today) and `narrative_baskets.jsonl` (6 baskets per report; 5 raw JSONL rows).
- `data/processed/llm_analysis_packet.md`, `llm_stocks_packet.md` (both ~14:48-15:16 EEST).
- CLI: `active-signals --asset-class crypto` (21 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-07-22` (**4 untracked** — ERA/USDT×3, EPIC/USDT×1).
- External web research: 3 WebSearch queries (Iran/Hormuz oil-market tape, BTC price/macro tape, Iran-Amazon-Bahrain claim verification, UNH DOJ status) + 1 WebFetch (Fortune BTC price page, verified opens). All resolved successfully — no "external web research unavailable" fallback needed.
- Previous review for diff: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-22_1139.md` (Europe/pre-US context slot, 11:39 EEST).

## 3. Scheduler / Data Freshness

- Scheduler folder: `data/scheduled_runs/2026-07-21_default_schedule/` (rolls over daily; current cycle is today's).
- `scheduler.log` mtime: 15:20 EEST (~1h03m old at time of this review — **fresh**, well under the 3h defer threshold).
- Latest cycle summary: `cycle_07_14-34_summary.md`, mtime 15:20 EEST — **fresh**.
- Monitors alive: `crypto_monitor` (log 16:30 EEST, live), `derivatives_monitor` (16:26 EEST, live), `stocks_monitor` (16:31 EEST, live even pre-open), `pending_monitor` (14:35 EEST), `mexc_canary_monitor` (14:35 EEST).
- No defer triggered.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-22 16:20 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_07 mtime 15:20 EEST, ~1h03m old", "crypto swing report ~12h07m old (borderline stale, flagged not used for entry timing)", "stocks swing/invest stale since 2026-07-02, known-deprecated pipeline"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "risk_off", "chop"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH labelled uptrend (76-79% breadth>EMA20) but BTC/ETH/SOL now show price-down+OI-down (deleveraging) in derivatives feed", "macro risk score 100/100, 7 risk-off hits vs 0 risk-on, Iran-war escalation + oil $89 Brent externally confirmed", "stocks regime=chop, neutral bias, VIX 17.63, 0/4 indices trending up"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 18.9% mapped / 81.1% unmapped today (2500 events)", "TRX/ERA/AKE B-tier ideas all explicitly 'no fresh verified catalyst detected' in evidence", "perps_dex_narrative (HYPE, fresh<1h) and ai_narrative (NEAR/RENDER/TAO/FET, fresh<24h) baskets still active"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "unwind", "data_unavailable"], "data_missing": ["OI history for MEXC-fallback symbols (n/a% OI change on most top movers)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH/SOL: price down + OI down = deleveraging/long liquidation, not a fresh short signal", "ERA/USDT and LA/USDT: negative funding + crowding=elevated across bybit/mexc/okx — crowded-short / squeeze-risk profile", "XRP/USDT: price up + OI down = short covering, weaker continuation quality"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRX/USDT B-tier idea generated at 11:48 UTC already shows tp1_hit by time of this review — entry window has passed", "BANK/USDT +27.5% 24h on only 0.45x volume — thin, extended, chase-risk", "AKE/USDT still genuinely waiting_for_entry at 0.001713-0.001761, current price ~0.0018 — live trigger zone"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["21 active crypto signals: 1 waiting_for_entry (AKE), 2 triggered, 11 tp1_hit, 7 tp2_hit — book is mostly already-running, not fresh", "4 untracked legacy alerts (ERA×3, EPIC×1) with no proposed_signal — needs_review, recurrence of known bug", "50 active stocks signals, all research/shadow-grade C-tier (plus a few B/A anecdotal), none current/compatible per today's report"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": ["confirmation status of Iran-Amazon Bahrain claim"],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: live, externally re-confirmed DOJ criminal+civil Medicare-billing investigation — legal_headline_risk gate stands", "GOOGL/TSLA/NOW earnings today, LMT tomorrow — do_not_chase_warning active", "AMZN: production risk_warning tag geopolitical_risk — Iran claims AWS Bahrain data-center strike; Bahrain disputes, AWS/US unconfirmed — unresolved headline risk into the open", "LLY: legal_risk tag — Novo Nordisk 'deceptive advertising' lawsuit against Eli Lilly"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week: intraday PF 2.06/+22.2R, swing PF 2.97/+23.6R (both actionable-primary), scalp PF 0.72/-3.1R (known-negative)", "crypto shorts n=8, 0 wins/6 losses, PF 0.125 — do not trigger fresh shorts on momentum alone", "stocks A/B headline (month) PF 0.356, totalR -14.17 — recent stocks A/B performance is poor; stocks C-tier PF 0.337 also negative"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["wait_for_trigger", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "AKE/USDT", "trigger": "1h close/hold inside 0.001713-0.001761 entry zone (price already ~0.0018, in-zone) with volume pickup; invalidation 1h close below 0.001654", "reason": "only genuinely fresh waiting_for_entry crypto B-tier setup this cycle; RS +10.2% vs BTC, but no catalyst backing (weak no-catalyst-intraday playbook, WR 23%/PF 0.70) — size accordingly" },
    "best_short_candidate":    { "symbol": "AVGO", "trigger": "wait for the stocks_intraday_7d_drawdown_guard to lift or for an operator manual-review sign-off, then confirm with a failed bounce after the open in the still-weak semis sector (SMH RS -13.2% vs SPY)", "reason": "cleanest technical short structure in the demoted stocks list (rr_to_tp1 3.19, structural TP), sector-aligned (short in a weak sector), but currently blocked by a rolling paper-R drawdown guard — not a chase" },
    "best_catalyst_candidate": { "symbol": "COIN", "trigger": "RTH confirmation + hold above pre-market/opening range; catalyst = Clarity Act Senate momentum + Coinbase-positive regulatory headlines (t.me/whale_alert_io, t.me/zerohedge, 2026-07-22)", "reason": "only stocks demoted-candidate with a same-day positive regulatory catalyst; currently capped purely by market_closed_intraday_planning_only, no legal/earnings flag" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "score 96 pre-gate but carries a live, externally re-confirmed DOJ criminal+civil Medicare-billing investigation — legal/headline risk overrides score; manual review required, never a clean long even after the open" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | mixed, risk_off, chop | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, unwind, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.70 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | wait_for_trigger, longs_preferred | advisory_only |

## 4. What Changed vs Previous Review

Previous review (11:39 EEST, Europe/pre-US context) named **OPN/USDT** best long (pullback zone 0.0655-0.0664), **HEMI/USDT** best short-watch, **ONDO/USDT** best catalyst-backed, **UNH** avoid, and reported **0 untracked legacy alerts** (clean).

- **OPN/USDT**: thesis played out — both the scalp/intraday (tp1_hit) and swing (triggered) OPN signals have progressed since 11:39; no longer a fresh entry.
- **HEMI/USDT**: dropped out of today's top-movers/strongest-weakest lists entirely — no longer trackable as a short-watch idea this cycle.
- **ONDO/USDT**: both active ONDO signals (scalp tp1_hit, intraday tp2_hit) have progressed further; rwa_narrative basket still lists ONDO as primary but freshness is now "unknown" (further staled from "6 days old" at 11:39) — demoted from catalyst-watch to "manage existing, don't chase."
- **Untracked alerts: NEW this cycle.** 11:39 review reported 0; this review found **4** (ERA×3 at 08:45/09:26/11:48 UTC, EPIC×1 at 12:35 UTC) — a live recurrence of the known watchlist-alert/signal-reuse defect. Escalated in §14.
- **UNH legal/headline risk**: unchanged, re-confirmed externally again this cycle (still AVOID).
- **AMZN geopolitical risk**: new this cycle — Iran-IRGC claims an AWS/Amazon Bahrain data-center strike surfaced as a production risk_warning tag; not present in the 11:39 review. Externally verified as a real, contested claim (see §13).
- Catalyst mapping: 18.9% mapped today vs 17.2% at 11:39 — marginal improvement, still far below the 50% usability bar (4th+ consecutive cycle flagged — see §14).

## 5. Catalyst Coverage

- Total catalyst events today: **2500** (`catalyst_events.jsonl`).
- Mapped (symbol present): **473** (18.9%). Unmapped: **2027** (81.1%).
- Narrative baskets: **6** per report (`perps_dex_narrative` primary HYPE, fresh<1h; `ai_narrative` primary NEAR/RENDER/TAO/FET, fresh<24h; `binance_ecosystem_teaser` primary BNB, fresh<24h; `delisting_thin_liquidity` primary XRP, fresh<24h; `rwa_narrative` primary ONDO/XLM, freshness unknown).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (>50% unmapped, persistent multi-day pattern — see TODO in §14.)
- Sample unmapped headlines (exchange operational notices, not trade-relevant): "Adjustment to Maximum Leverage for ONEUSDT Futures," "Delisting of SOLANGELESUSDT Perpetual Futures Pair."

## 6. Market Landscape

Crypto structural regime is still labelled "bullish trend / risk-on" (BTC/ETH uptrend, altcoin breadth 76.3%/78.9% above EMA20/50), but the derivatives feed shows BTC, ETH, and SOL **all price-down + OI-down** right now — genuine deleveraging, not just noise, coincident with a fresh externally-confirmed macro shock: Brent crude at **$89.22/bbl** and WTI at **$83.23/bbl** (2026-07-20 close) on the 9th-10th consecutive night of direct US-Iran military strikes, plus a Houthi maritime embargo declared against Saudi Arabia. BTC spot is ~$65,859 (07:15 EEST today), down from a one-month high, consistent with the report's own headline ("Bitcoin retreats from one-month high as oil tops $85"). Stocks regime is **chop, neutral bias**, VIX 17.63, breadth 75%/100% above EMA20/50, 0 of 4 major indices trending up (all "range"). Strongest stock sectors: energy (+8.2% 20d, RS +7.7% vs SPY), healthcare (+6.8%, RS +6.3%), financials (+4.5%, RS +4.0%). Weakest: semiconductors (-12.7%, RS -13.2%), technology (-5.9%, RS -6.4%), materials (-2.9%, RS -3.5%).

### Market Mood / Risk Routing
- Crypto mood: **mixed** (structurally risk-on/uptrend, but tactically risk-off — active deleveraging + geopolitical macro shock)
- Stocks mood: **chop / pre-market** (cash closed, VIX moderate at 17.6, indices rangebound)
- Dominant narrative: Iran-US military escalation / oil spike is the dominant cross-asset risk driver into the US open; secondary crypto narratives are RWA (ONDO/XLM, staling) and AI-beta (NEAR/RENDER/TAO/FET, fresh<24h)
- Preferred side now: **wait-for-trigger**, selective longs on RS-leaders only, no fresh momentum shorts
- Best long candidate: AKE/USDT (waiting_for_entry, see §8)
- Best short candidate: none clean crypto-side (shorts broken, PF 0.125 this week); AVGO stocks-side is the cleanest short structure but currently guard-blocked
- Best catalyst-backed candidate: COIN (stocks, Clarity Act momentum) — crypto catalyst-backed book (ONDO) has staled
- What to avoid: UNH (legal/DOJ), any fresh crypto short on momentum alone, chasing GOOGL/TSLA/NOW into today's earnings
- What would change the view: a de-escalation headline on Iran/Hormuz (oil retreating) would remove the dominant risk-off headwind; a stabilizing/confirmed (not just IRGC-claimed) resolution on the AWS Bahrain story would reduce tech/cloud headline risk; BTC/ETH OI turning back up alongside price would signal the deleveraging is done

## 7. Candidate Deep Dives

### 1. ERA/USDT (crypto, long, B-tier idea / system-integrity flag)
- Has price already reacted to the catalyst? No verified catalyst exists — move is pure momentum (24h +7.98%, 7d +35.76%).
- Chasing? Not yet — Entry Plan is a pullback zone 0.1016-0.1062 vs current 0.1082, i.e. just above the zone.
- Retest/pullback structure? Yes, defined pullback zone with RR 1.84 to TP1.
- Overextended (>2 ATR from EMA20)? Not flagged by the report; ATR 0.0101, current 0.1082 vs support 0.0848 — inside normal range.
- Would entry now be late? Borderline — price sits just above the pullback zone.
- Actionable now or after confirmation? **Not Telegram-actionable at all right now** — see below.
- **Critical finding:** `detect_untracked_legacy_alerts` shows ERA/USDT fired **3 separate raw watchlist alerts today** (08:45, 09:26, 11:48 UTC, scores 73.2/66.8/66.4) with **no backing `proposed_signal`** — confirmed by cross-checking `active-signals --asset-class crypto`, which has **zero** ERA/USDT rows. This is the same watchlist-alert/signal-reuse defect flagged 2026-07-17 on ALLO/BANK ([[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]), now recurring on a different symbol.
- Aligned with market mood? Momentum-only, no catalyst — weak fit for a risk-off-tilted tape.
- Chase-risk setup? Moderate — thin volume (0.36x).
- Catalyst confirmation/contradiction? None — "no fresh verified catalyst detected" per the report itself.
- **Verdict: AVOID treating as Telegram-actionable** (untracked — any resulting trade cannot be scored) until the bug is fixed; if manually tracked, only on a confirmed pullback hold with volume.

### 2. EPIC/USDT (crypto, long, multi-mode recurring mover / system-integrity flag)
- Has price reacted? Yes — vertical move, 24h +19.6% (intraday report) to +20.98% (swing report), 7d +41%.
- Chasing? Yes — this is a multi-cycle continuation of an already-extended move; swing entry zone was 0.5296-0.5382 at 01:16 EEST with price at 0.5420 (already through the top of the zone even then).
- Retest/pullback structure? Defined in the swing idea card, but the **borderline-stale swing report (~12h old)** makes current-price comparison unreliable — do not use its levels for a fresh entry without a re-check.
- Overextended? Very likely given the vertical multi-session move; treat as overextended until proven otherwise.
- Would entry now be late? Yes.
- **Critical finding:** the 12:35 UTC untracked alert (score 77.1) is the 4th untracked alert of the day and the 2nd symbol hit by the same bug as ERA above — EPIC also has **zero** rows in `active-signals --asset-class crypto` despite being a recurring "strongest symbol" across scalp/intraday/swing reports for multiple cycles running.
- Aligned with mood? No catalyst confirmed; pure momentum into a risk-off-tilted tape.
- Verdict: **AVOID fresh entries — chasing a stale, untracked, multi-session vertical move.** Same tracking defect as ERA; combine into the §14 TODO.

### 3. TRX/USDT (crypto, long, B-tier — cleanly tracked)
- Has price reacted? Modest, 24h +0.79%, 7d +0.58% — this is a low-volatility continuation idea, not a breakout chase.
- Chasing? No — Entry Plan pullback 0.3297-0.3299 vs report-time price 0.3300, essentially at the zone when generated (11:48 UTC).
- Retest/pullback structure? Yes, clean.
- Overextended? No.
- Current status: `active-signals` shows this signal **already at tp1_hit** by the time of this review (13:20 UTC) — the entry window has already passed; this is now an open, partially-resolved position, not a fresh watch.
- Catalyst confirmation? None — explicitly "no fresh verified catalyst detected"; playbook is the known-weak no-catalyst-intraday cohort (WR 23%/PF 0.70/-3R over 14d).
- Aligned with mood? Marginal — clean tracking is good, but weak playbook edge and no catalyst in a risk-off-tilted tape argue for small size only.
- Verdict: **Manage existing position (tp1 already hit); not a fresh entry.**

### 4. UNH (stocks, long, demoted near-A/B, score 96→C)
- Sector: healthcare — currently the #2 strongest sector (RS +6.3% vs SPY, +6.8% 20d).
- RR to TP1: 1.5 (atr_measured); RS vs SPY +6.8%, vs sector +0.5%; volume ratio 1.72x — technically one of the cleanest setups in the demoted list.
- Legal/headline risk: **externally re-confirmed today** — UnitedHealth is under an active DOJ criminal and civil investigation into Medicare Advantage billing practices (diagnosis-inflation allegations), also extending to Optum Rx and physician-reimbursement practices, per Healthcare Dive / CNBC / The Hill / Fierce Healthcare. No resolution found as of this review.
- Would entry be late/chasing? Irrelevant — legal risk overrides.
- **Verdict: AVOID / MANUAL REVIEW REQUIRED.** Score and technicals are clean, but the legal/headline gate must dominate per §I. This applies to both the intraday demoted candidate and the separate shadow-only `stocks_swing_growth_breakout` UNH pullback candidate (score 87.0) — same underlying legal risk, still shadow/non-actionable either way.

### 5. XOM (stocks, long, demoted near-A/B, score 95→C)
- Sector: energy — currently the **strongest** sector (RS +7.7% vs SPY, +8.2% 20d), and oil is spiking on the Iran/Hormuz escalation, which is directly sector-supportive for XOM specifically (though risk-off for broader equities).
- RR to TP1: 1.5 (atr_measured); RS vs SPY +9.0%; volume ratio 1.52x.
- Legal/headline/earnings risk: **none found** — no earnings today/tomorrow, no legal flags in the production risk-warning list.
- Only cap reason: `market_closed_intraday_planning_only` — purely a timing gate, not a quality issue.
- Is this candidate aligned with market mood? Yes — long in the strongest sector, with a live macro tailwind (oil spike) specific to energy.
- Actionable now or after confirmation? **After confirmation only** — needs 15-30 min of RTH price action to re-validate the entry zone before treating as live; do not chase pre-market.
- Chase-risk? Low, if RTH-confirmed at/near the stated zone; high if gapped well above it at the open.
- Verdict: **Best long-watch candidate for the post-open stocks book** — clean technicals, sector tailwind, no legal/earnings flags; require RTH confirmation.

## 8. Best Candidates Ranked

1. **AKE/USDT (long-watch, crypto)** — trigger: 1h close/hold inside 0.001713-0.001761, invalidation 0.001654. No catalyst backing; size small (weak no-catalyst-intraday cohort).
2. **XOM (long-watch, stocks)** — trigger: RTH confirmation of the 147.49-148.03 zone (report-time levels) holding above VWAP/opening range in the first 15-30 min; invalidation 146.94. Sector tailwind (energy) is live and macro-driven.
3. **COIN (catalyst-watch, stocks)** — trigger: RTH confirmation holding above pre-market highs; catalyst = Clarity Act Senate momentum (positive regulatory flow, same-day). Currently capped only by market-closed, no legal/earnings flag.
4. **AVGO (short-watch, stocks)** — trigger: failed bounce / rejection at resistance after the open, confirmed by continued SMH/semis relative weakness; currently blocked by the 7-day drawdown guard — treat as watch, not a live short, until the guard lifts or is manually reviewed.
5. **Avoid: UNH** (legal/DOJ risk, both intraday demoted and shadow-only swing candidates) and **fresh ERA/EPIC entries** (untracked, unscoreable — system bug, see §14).

Excess candidates not deep-dived (listed with reason): **BANK/USDT** (crypto, tracked B-tier, +27.5% 24h on thin 0.45x volume — chase-risk, no catalyst); **JPM** (stocks, financials strong sector, clean RR but only market-closed-capped — reasonable secondary long-watch behind XOM); **AAPL/GOOGL/TSLA/NOW** (stocks, earnings-today/tomorrow — explicitly avoid chasing per production risk warnings).

## 9. Avoid / No Trade

This is a decision-window call only — scanning, tracking, and monitors continue in all cases.

- **UNH** (stocks, all modes) — live DOJ criminal+civil investigation; legal/headline risk overrides a 96-score technical setup.
- **Fresh ERA/USDT and EPIC/USDT entries** (crypto) — both are currently firing raw Telegram alerts with no backing `proposed_signal`; any resulting manual trade would be untracked/unscoreable. Fix is a §14 TODO, not something to route around live.
- **Fresh momentum shorts, crypto, any symbol** — the short playbook is 0 wins / 6 losses (PF 0.125) over the past week; do not initiate new shorts on relative-weakness/momentum alone this window.
- **Chasing GOOGL, TSLA, NOW** into today's earnings, and **LMT** ahead of tomorrow's — per production `do_not_chase_warning` flags.
- **AMZN** — not a new trade call (no active AMZN candidate today), but note the unresolved Iran-AWS-Bahrain claim (§13) as a live headline-risk overhang if any AMZN/cloud-adjacent candidate appears before it is resolved one way or the other.

## 10. Main Risks

- **Iran-US military escalation / oil spike** is the dominant cross-asset risk factor into the US open: Brent $89, WTI $83, 9-10 consecutive nights of strikes, Houthi maritime embargo against Saudi Arabia declared this week. This is externally confirmed and is actively producing crypto deleveraging (BTC/ETH/SOL price-down + OI-down) and a "chop, VIX 17.6" stocks regime.
- **Contested overnight claim, unresolved:** Iran's IRGC states it destroyed Amazon/AWS's central data infrastructure in Bahrain via cruise-missile strike, also targeting US air-defense/radar sites in Muharraq and Riffa. Reported by CNBC, Euronews, Jerusalem Post, Middle East Eye, IBTimes, Gizmodo, Tom's Hardware — but **Bahrain says it intercepted the attack and does not confirm any commercial/Amazon infrastructure was hit**, and **neither AWS nor US officials have confirmed the claim**. Classify as single-source/state-media-originated and disputed — a real gap-risk factor for AMZN/cloud-adjacent names and general risk sentiment at the open, but not a confirmed fact. Re-check before the open and again at 18:30 (US-open-reaction slot).
- **Watchlist-alert/signal-reuse bug recurrence** (ERA/EPIC, 4 untracked alerts today) — same defect class as the 2026-07-17 ALLO/BANK case; a repeat, not a one-off (§14).
- **Crypto book is mostly already-running positions**, not fresh setups (11 tp1_hit, 7 tp2_hit out of 21 active signals) — limited fresh actionable surface this cycle regardless of mood.
- **Stocks A/B recent performance is weak**: month headline PF 0.356 (totalR -14.17), C-tier PF 0.337 — treat any fresh stocks A/B this week with extra skepticism even when technically clean.
- Crypto swing report is borderline-stale (~12h) — used for narrative context only, not for fresh entry levels (EPIC, ONDO already flagged above).

## 11. Action Plan — next 4 hours

1. Watch AKE/USDT for a confirmed hold inside its entry zone before treating as live; do not chase if it runs without a retest.
2. At/after 09:30 ET (16:30 EEST), require 15-30 min of RTH price action before treating XOM, JPM, or COIN as live — do not act on pre-market levels.
3. Re-check the Iran-AWS-Bahrain claim status (confirmed / retracted / still disputed) before or during the 18:30 EEST US-open-reaction review; this materially changes AMZN/cloud-sector headline risk.
4. Do not chase GOOGL, TSLA, NOW into today's earnings prints; wait for post-print confirmation if a setup re-appears.
5. Continue monitoring BTC/ETH OI — a turn back to price-up + OI-up would signal the current deleveraging phase is ending and would upgrade the crypto mood from mixed toward risk-on.
6. Manual review only: UNH (any mode, legal risk) and ERA/EPIC (untracked, system bug) — do not treat either as tradeable this window.

## 12. Final Verdict per Mode

- **Crypto scalp:** no action — known-negative playbook (PF 0.72/-3.1R, 14d), no fresh clean setups this cycle.
- **Crypto intraday:** wait-for-trigger — AKE/USDT is the only clean waiting_for_entry setup; TRX already progressed (manage, don't chase); ERA/EPIC untracked, avoid.
- **Crypto swing:** carry-forward only this cycle — source report borderline-stale (~12h); EPIC/ONDO swing ideas already progressed/chased, no fresh swing entry to propose.
- **Stocks intraday:** watch-only pre-open — zero current/compatible A/B; XOM/JPM/COIN are the post-open watchlist pending RTH confirmation; AVGO short pending guard review; UNH is avoid regardless of confirmation.
- **Stocks swing/invest (legacy):** deprecated, not reviewed.
- **Stocks swing growth-breakout (new, shadow):** 3 open shadow candidates (UNH, MS, AAPL) — research-only, no actionability; UNH candidate additionally carries the same legal-risk flag as the intraday demoted candidate.

## 13. Sources

- [Oil prices rise after Trump says Iran will pay for killing U.S. service members](https://www.cnbc.com/2026/07/20/oil-prices-today-brent-wti-crude-us-iran-centcom-hormuz.html) — CNBC, 2026-07-20. Verification: primary_source. Confirms Brent $89.22, WTI $83.23, active US-Iran military escalation.
- [Iran war update: five things to know after resumption of hostilities](https://www.cnbc.com/2026/07/21/iran-war-update-five-things-to-know-after-resumption-of-hostilities.html) — CNBC, 2026-07-21. Verification: primary_source. First report of the Amazon-Bahrain claim.
- [Iran's IRGC claims attack on Amazon's main data hub in Bahrain](https://www.euronews.com/2026/07/21/irans-irgc-claims-attack-on-amazons-main-data-hub-in-bahrain) — Euronews, 2026-07-21. Verification: single_source (state-media claim), disputed by Bahrain government, unconfirmed by AWS/US.
- [Iran targeted Amazon infrastructure in Bahrain, US military sites in Jordan, IRGC claims](https://www.jpost.com/middle-east/iran-news/article-903144) — Jerusalem Post, 2026-07-21. Verification: single_source, same contested claim.
- [Current price of Bitcoin for July 22, 2026](https://fortune.com/article/price-of-bitcoin-07-22-2026/) — Fortune, 2026-07-22. Verification: primary_source. BTC $65,858.69 at 06:15 ET, down $452.11 day-over-day.
- [UnitedHealth confirms it's under investigation by DOJ](https://www.healthcaredive.com/news/unitedhealth-under-investigation-department-of-justice-medicare/753913/) — Healthcare Dive. Verification: primary_source.
- [UnitedHealth facing DOJ investigation over Medicare billing](https://www.cnbc.com/2025/07/24/unitedhealthcare-doj-investigation-medicare-billing.html) — CNBC, 2025-07-24. Verification: primary_source. Confirms ongoing criminal+civil DOJ probe (Medicare Advantage billing, Optum Rx, physician reimbursement); no resolution reported.

## 14. Fix Requests / TODO

### TODO-untracked-alert-recurrence-era-epic
- **issue:** Watchlist-alert/signal-reuse defect recurred this cycle — ERA/USDT fired 3 raw Telegram watchlist alerts (08:45, 09:26, 11:48 UTC) and EPIC/USDT fired 1 (12:35 UTC), none with a backing `proposed_signal`. Same defect class as the confirmed 2026-07-17 ALLO/BANK case.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-22` → 4 untracked rows; cross-checked against `python -m src.cli active-signals --asset-class crypto` (21 rows, zero ERA/EPIC entries).
- **suggested manual fix:** Investigate why the alert path mints a Telegram watchlist alert without also minting/reusing a `proposed_signal`; check whether this is the same reuse-of-stale-signal_id bug already raised (see prior TODO-3, raised high 2026-07-17) or a distinct code path for symbols not currently in the DB.
- **priority:** high
- **first observed (this recurrence):** 2026-07-22 16:20 EEST

### TODO-catalyst-mapping-persistent-weak
- **issue:** Catalyst symbol-mapping coverage has been below the 50% usability bar for 4+ consecutive review cycles (17.2% at 11:39 EEST today, 18.9% now).
- **evidence:** `data/catalysts/2026-07-22/catalyst_events.jsonl` — 2500 total events, 473 mapped (18.9%), 2027 unmapped (81.1%); majority of unmapped items are exchange operational notices (leverage adjustments, delisting notices for obscure pairs) rather than trade-relevant news.
- **suggested manual fix:** Improve the symbol resolver in the catalyst layer to either better-classify operational-notice-only sources as a separate low-priority bucket (so the mapped% metric isn't diluted by noise), or expand ticker/alias resolution coverage.
- **priority:** medium
- **first observed:** carried forward from prior reviews (multi-day pattern)

### TODO-amzn-bahrain-claim-followup
- **issue:** Iran's IRGC claims a cruise-missile strike destroyed AWS/Amazon's central data infrastructure in Bahrain; Bahrain disputes the claim (says it intercepted the attack, denies commercial infrastructure was hit) and neither AWS nor US officials have confirmed it as of this review. This is a live, unresolved headline-risk item relevant to AMZN and broader cloud/tech sentiment at the US open.
- **evidence:** production risk-warning tag `AMZN [geopolitical_risk]: risk_warning — Iran says it attacked Amazon infrastructure in Bahrain (CNBC Markets)` in the 2026-07-22 11:48 intraday report §5c; externally cross-checked via CNBC/Euronews/Jerusalem Post (§13).
- **suggested manual fix:** No code fix needed — flagging for the next scheduled review (18:30 EEST US-open-reaction) to re-check whether the claim has been confirmed, retracted, or remains disputed, and to check for any actual AWS service-status impact.
- **priority:** medium
- **first observed:** 2026-07-22 16:20 EEST
