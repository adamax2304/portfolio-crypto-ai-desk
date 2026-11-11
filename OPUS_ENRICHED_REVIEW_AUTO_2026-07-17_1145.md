# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:45 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context** (11:30 EEST assignment, dispatched ~11:39-11:45). **Advisory only — no auto-trade, no code/scoring/routing changes.** Pipeline healthy: `scheduler.log` mtime 11:39 EEST (fresh), latest `cycle_03_08-43_summary.md` mtime 09:18 EEST (~2h27m old) — both under the 3h defer threshold, **not deferred**. Crypto scalp/intraday fresh (~3h, generated 08:26/08:32 EEST); crypto swing is carry-forward (generated 01:03 EEST, ~10h36m old, within the 4-12h carry-forward band, market regime read range/chop at that time vs current bearish trend — used with a freshness flag, not as primary regime source). Stocks intraday fresh (06:13 EEST, ~5.5h old) but **pre-market** — US cash session opens ~16:30 EEST (9:30 ET), so every stocks idea is planning/watchlist context only, not yet RTH-confirmed. Stocks swing/invest last generated 2026-07-02 (15 days stale) — known-deprecated legacy framework, excluded.

**Crypto mood is bearish/risk-off**: BTC/ETH both `transition_down`, altcoin breadth only 25% above EMA20, macro risk score 86/100 driven almost entirely by escalating **Iran-US Gulf tensions** (US airstrikes near Qeshm, Iranian Revolutionary Guard strikes on a US radar in Oman, Strait of Hormuz supply-risk headlines) — this is the dominant macro overhang into the US session. **Two live crypto positions, no new signals this cycle**: TAO/USDT (B, swing, short, `triggered` at 05:36 EEST, aligned with the bearish regime, no fresh catalyst) and ONDO/USDT (B, intraday, long, `tp2_hit`) — ONDO's `expires_at` is **2026-07-17T08:36:31 UTC = 11:36:31 EEST, i.e. essentially right now** at review time; it has already banked TP1+TP2 and is racing its hard expiry toward TP3 — watch for it to convert to entered-unresolved in the next monitor tick if TP3/stop isn't hit first (not a missed entry — partial profit already locked). No A/B setups anywhere in scalp/intraday/swing; only watchlist C-tier ideas, still dominated by two counter-tape RS-leader longs (BANK/USDT, KAITO/USDT, both no verified catalyst, "reduce size" warnings) and several no-catalyst short-biased names (TAO, SUI, GRAM, WLD, AIGENSYN watchlist entries — TAO's watchlist entry is separate from and consistent with the already-triggered swing short).

**Stocks pre-market**: chip-sector weakness headline overshadowing an otherwise strong earnings season; VIX 18.48 (up from ~16.7 two cycles ago), QQQ trend down, SPY flat — softer tape into the open. No actionable stocks intraday (0 A/B live; 18 A/B candidates demoted to C purely by the market-closed gate). The two strongest pre-tier planning ideas carry forward unchanged from the overnight review: **AVGO short** (score 90, was A) and **XOM long** (score 89, was A) — both need RTH confirmation before acting. **MSFT** (was B) stays gated **AVOID/MANUAL REVIEW** on an active securities-fraud legal/headline flag. UNH shows a genuine internal contradiction (DOJ antitrust-probe-expansion headline same day as an earnings-beat/rally headline) — treat as manual-review context, not a clean read.

**Catalyst mapping is weak this run (82.8% unmapped, 345/2000)** — unchanged in substance from the last review (was 84%), use the catalyst layer as directional context only, not a gating input. **System-integrity issue unchanged, still high-priority**: `detect_untracked_legacy_alerts` still shows the same 2 unresolved symbols (ALLO/USDT ~21h, BANK/USDT ~14h) with zero new watchlist alerts fired since 2026-07-16T21:36 UTC — TODO-3 carries forward unchanged. **New this cycle**: `mexc_canary_monitor` is repeatedly crash-looping on `OperationalError: database is locked` while writing its kill-switch state (4 separate log files today, restarting roughly every ~2.5h) — flagged as a new high-priority TODO; this is a live-execution safety-mechanism component, not something this advisory review can or should touch. Scanning, tracking, and all monitors continue unaffected — **no recommendation to pause anything.**

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-17_08-26_scalp_report.md` (generated 11:26 EEST, ~13min old at write time), `data/reports/intraday/2026-07-17_08-32_intraday_report.md` (generated 11:32 EEST, ~7min old), `data/reports/swing/2026-07-17_01-03_swing_report.md` (generated ~04:03 EEST content-time / carry-forward, ~10h36m old — regime range/chop, flagged), `data/reports/stocks/intraday/2026-07-17_06-13_stocks_intraday_report.md` (~5.5h old, pre-market planning-only). Stocks swing/invest last generated 2026-07-02 — deprecated legacy framework, excluded (>14h stale by design).
- Catalyst: `data/catalysts/2026-07-17/catalyst_events.jsonl` (2000-row rolling buffer, 345 mapped / 1655 unmapped), `narrative_baskets.jsonl` (5 baskets), `data/catalysts/2026-07-17/catalyst_cycle_08-34.md` (latest cycle, already present, no re-scan needed).
- LLM packets: `data/processed/llm_analysis_packet.md` (~13min old), `data/processed/llm_stocks_packet.md` (~2h31m old).
- DB (direct SQL, `db/crypto_ai_desk.sqlite`): `proposed_signals` (full TAO/ONDO rows), `market_dashboard_snapshots` (latest row), `news_items` (UNH DOJ/earnings cross-check).
- CLI: `active-signals` ×2 (crypto: 2 rows; stocks: 50 rows), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-17` (0 new today) and `--since 2026-07-16` (2 unresolved, unchanged).
- Scheduler: `data/scheduled_runs/2026-07-17_default_schedule/scheduler.log`, `cycle_03_08-43_summary.md`; monitor logs (`pending_monitor_manual_restart.log`, `mexc_canary_monitor_*.log` ×4).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-17_0439.md` (04:39 EEST, crypto overnight/Asia slot) — used for TODO carry-forward (TODO-1..5), thesis tracking (ONDO/TAO/BANK/AVGO/XOM/MSFT), and integrity-issue history.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **11:39 EEST**, latest `cycle_03_08-43_summary.md` mtime **09:18 EEST** (~2h27m old at review start) — both under 3h, **not deferred**.
- Crypto scalp/intraday: fresh (generated 11:26/11:32 EEST, minutes old).
- Crypto swing: **carry-forward** (generated ~04:03 EEST, ~10h36m old — inside the 4-12h carry-forward band, used with an explicit staleness flag; regime read at generation time was range/chop, materially different from the current bearish/transition_down read, so swing watchlist ideas below are treated as lower-confidence context, not primary).
- Stocks intraday: fresh (06:13 EEST, ~5.5h old) but generated pre-market; all ideas are `market_closed_intraday_planning_only` until the 16:30 EEST / 9:30 ET open.
- Stocks swing/invest: last generated 2026-07-02 (15 days stale) — known-deprecated legacy framework by design, not a freshness fault.
- Catalyst directory present for today, 2000-row rolling buffer already populated — no re-scan needed.
- Monitors: `pending_monitor_manual_restart.log` shows healthy recent ticks (tick 994, crypto-only, refresh succeeded 2/2, no errors). `mexc_canary_monitor` is **not healthy** — repeated `OperationalError: database is locked` crash on `ensure_tables`/kill-switch write, 4 restart cycles today (03:30, 06:24, 08:59, 11:33). See TODO-8 (§14). This is a live-execution component; scanning/tracking/paper-signal flow (the actual subject of this review) is unaffected.
- Dashboard snapshot (`market_dashboard_snapshots`, latest row 08:41 EEST): `crypto_market_mode=trend`, `crypto_regime=bullish trend`, `crypto_fear_greed=27` (fear zone), `stocks_market_mode=unknown`, `stocks_regime=transition`, `spy_trend=flat`, `qqq_trend=down`, `vix=18.48`. **Note**: the dashboard's `crypto_regime=bullish trend` label continues to disagree with both fresh report-level reads (`bearish trend (risk-off)`, BTC/ETH `transition_down`) — same inconsistency flagged in the prior 04:39 review, still unresolved. Report-level regime is treated as authoritative here (see TODO-9).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-17 11:45 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["swing report is carry-forward (~10h36m), used with a staleness flag"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 11:39 EEST + cycle_03_08-43 09:18 EEST, both <3h", "scalp/intraday fresh (~7-13min)", "swing 10h36m old, regime read at generation (range/chop) differs from current (bearish)", "stocks intraday 5.5h old, pre-market by design", "stocks swing/invest 15d stale, deprecated legacy framework"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH trend=transition_down in both fresh crypto reports", "altcoin breadth 25.0% above EMA20 (weak breadth)", "macro risk 86/100, driven by Iran-US Gulf conflict escalation headlines", "crypto fear&greed=27 (fear zone)", "stocks: VIX 18.48 (rising), QQQ trend down, SPY flat, chip-sector-weakness headline; US cash still pre-market"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "stale_catalyst", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["82.8% unmapped (1655/2000) catalyst events today — weak mapping run, same magnitude as the prior review (84%)", "active baskets: perps_dex (HYPE), ai_narrative (NEAR/RENDER/TAO/FET), binance_ecosystem (BNB/ASTER), momentum_breakout (LUMIA)", "TAO short aligns with the AI-narrative basket but has no symbol-specific fresh catalyst — pure technical/regime thesis", "UNH: DOJ antitrust-probe-expansion headline (2026-07-16) same-day as an earnings-beat/rally headline — internal contradiction, not resolved"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.45,
      "reason_codes": ["oi_supports", "data_unavailable", "squeeze_risk"],
      "data_missing": ["BTC/ETH-level funding/OI not separately surfaced in today's reports, only altcoin-level"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TAO: price down + OI up (fresh shorts pressing, possible squeeze if price reclaims), funding -7.85e-05, crowding normal", "ONDO (at entry): price up + OI up, funding 3.6e-05, crowding normal", "HOME/USDT: heavily negative funding across bybit/mexc/okx, elevated crowding — overextended breakdown, squeeze-prone if shorted late"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["entry_fresh", "chase_risk", "price_moved_away", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TAO short: entry zone 191.04-192.02, triggered at 05:36 EEST, current context still valid per 11:32 report watchlist re-scan of TAO at 189.50 (below entry, already working toward TP1 188.42)", "ONDO long: TP1+TP2 already hit, current price context 0.37-ish per earlier setup, TP3 0.4017 still open, hard expiry essentially now (11:36 EEST)", "BANK/KAITO watchlist longs are up 14-20% over 24h already — chasing risk if entered now, no pullback confirmation yet", "AVGO/XOM stocks ideas are pre-market only, no RTH price action yet to confirm or invalidate"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["open_actionable", "entered_unresolved", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: TAO (OPEN actionable, triggered, working toward TP1-3), ONDO (ENTERED, TP1+TP2 hit, NEEDS REVIEW — at/past hard expiry boundary as of this review)", "stocks active-signals: 50 rows, the great majority are older tp1_hit/tp2_hit/triggered entries well past their mode-appropriate horizon (see TODO-2, carried forward) rather than fresh actionable ideas", "no untracked legacy alerts fired today (0 new since 2026-07-17T00:00)"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT: active securities-fraud legal/headline gate, correctly demoted B->C by the pipeline, stays AVOID/MANUAL REVIEW", "UNH: DOJ antitrust probe vs earnings-beat headline contradiction, C-tier only (not A/B) but worth manual-review context if it resurfaces at A/B", "Iran-US Gulf conflict is the dominant macro risk driver (86/100 macro risk score) — reduce size / prefer defined-risk setups across the board", "BANK/KAITO longs are explicitly flagged by the pipeline itself as counter-tape RS-leaders — reduce size if ever promoted to actionable"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto B-tier week: n=130, reliable, PF 1.85, avgR 0.256, totalR +25.6 — real positive edge despite a low 24% winrate (asymmetric R management carrying it)", "crypto scalp mode is a losing bucket this week: n=24, PF 0.30, avgR -0.18, totalR -3.5 (weak confidence) — TODO-6", "stocks headline A/B this week: n=14 (weak confidence), winrate 28.6%, PF 0.667, totalR -1.0; stocks C-tier watchlist also negative (PF 0.757, totalR -9.0) — consistent with TODO-1's forward-negative evidence for stocks intraday, still needing human sign-off"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents below"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "shorts",
    "best_long_candidate": { "symbol": "XOM", "trigger": "RTH confirmation of the pre-market long setup after the 16:30 EEST / 9:30 ET open — do not chase pre-market strength; wait for the first 15-30min range and a clean hold above the pre-market planning entry" },
    "best_short_candidate": { "symbol": "TAO/USDT", "trigger": "already active (B, swing, triggered 05:36 EEST) — working the existing plan toward TP1 188.42 / TP2 186.24 / TP3 184.06, stop 193.21; no new entry needed, this is the cleanest actionable idea on the desk right now" },
    "best_catalyst_candidate": { "symbol": "none clean", "reason": "catalyst mapping is weak this run (82.8% unmapped); BONK carries the highest-importance verified catalyst (exploit-fallout, importance 0.82) but is only an operator-review risk flag, not a scored A/B setup — treat as catalyst-watch only, not actionable" },
    "avoid_candidate": { "symbol": "MSFT", "reason": "active securities-fraud legal/headline gate, correctly demoted by the pipeline; stays AVOID/MANUAL REVIEW. HOME/USDT is a secondary avoid — already -39.4% in 24h with elevated funding/crowding, overextended, chase-risk on any further short entry" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 9
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.75 | risk_off, shorts_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, stale_catalyst, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | oi_supports, data_unavailable, squeeze_risk | advisory_only |
| technical_entry | caution | 0.60 | entry_fresh, chase_risk, price_moved_away, stale_before_entry | advisory_only |
| execution_lifecycle | caution | 0.70 | open_actionable, entered_unresolved, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, legal_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-17_0439.md` (04:39 EEST, crypto overnight/Asia slot):

- **New**: TAO/USDT B-tier swing short **triggered** at 05:36 EEST — did not exist as an active signal in the 04:39 review (TAO was watchlist-only at that point). This is now the desk's cleanest actionable idea.
- **Unchanged**: ONDO/USDT intraday long remains `tp2_hit`, now at/past its hard expiry (11:36 EEST) — same position, now at a lifecycle inflection point.
- **Regime flip**: crypto regime went from `range` (both reports, 04:39 review) to `bearish trend (risk-off) / transition_down` (current fresh reports) — a real shift, not noise; altcoin breadth also fell further.
- **Confirmed, not new**: MSFT securities-fraud gate still active; AVGO/XOM remain the top two stocks pre-tier ideas, scores essentially unchanged (90/89 now vs similar before).
- **Confirmed, not new**: TODO-3 (ALLO/BANK untracked legacy alerts) unchanged — still exactly 2 unresolved, no new alert fired since 2026-07-16T21:36 UTC (now ~14-21h stale).
- **Confirmed, not new**: catalyst mapping still weak (82.8% vs 84% previously — essentially flat, no improvement).
- **New this cycle**: `mexc_canary_monitor` crash-loop discovered (not observed/checked in the 04:39 review) — TODO-8.
- BANK/USDT's watchlist score continues to fade slightly cycle over cycle (65→52→51.7) with still no verified catalyst — thesis unchanged (counter-tape RS-leader, not actionable).

## 5. Catalyst Coverage

- Today's rolling buffer: **2000 events**, **345 mapped (17.2%)**, **1655 unmapped (82.8%)**. **Catalyst mapping weak this run — use the catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (symbol resolver missed these): "250,000,000 $USDC minted at USDC Treasury Details" (×2, likely a stablecoin-mint alert with no ticker match), "MoonPay has acquired Glide, a cross-chain deposit infrastructure startup" (6th acquisition of 2026 — no ticker to map to).
- 5 active narrative baskets: `perps_dex_narrative` (HYPE, DYDX, GMX, ASTER; wait_pullback), `ai_narrative` (NEAR, RENDER, TAO, FET; related_beta_rotation) — TAO's active short sits inside this basket, `binance_ecosystem_teaser` (BNB, ASTER), `delisting_thin_liquidity` (no primary), `momentum_breakout` (LUMIA).
- Highest-importance verified catalyst today: BONK/USDT exploit-fallout piece (importance 0.82, single-source) — already surfaced as an operator-review risk warning, not a scored setup.
- Stocks legal-risk cluster remains heavy: MSFT (securities fraud, active gate), plus PLAB/AVAV/BTGO/NNOX/ADMA/Planet Fitness/GPGI investor-deadline notices (routine law-firm PR, low actionability, not gating anything today).

## 6. Market Landscape

Crypto: BTC/ETH both `transition_down`, altcoin breadth thin (25% > EMA20, 31.8% > EMA50). Macro backdrop dominated by the Iran-US Gulf conflict (US airstrikes near Qeshm, IRGC strike on a US radar in Oman, Strait of Hormuz tanker/blockade headlines, oil prices rising) — macro risk score 86/100, clearly risk-off for crypto beta. Fear & Greed 27 (fear zone). Two RS-leaders (BANK +14.4%/24h, KAITO +19.9%/24h) are swimming against this tape — the pipeline itself flags both as "counter-tape long, reduce size," consistent with the risk-off read. HOME/USDT is the most overextended name on the desk (-39.4%/24h, elevated negative funding/crowding across bybit/mexc/okx) — a chase-risk avoid rather than a fresh short.

Stocks: pre-market (US cash opens ~16:30 EEST). VIX 18.48 (rising from ~16.7 two cycles ago), QQQ trend down, SPY flat — "chip sector weakness overshadowing strong earnings season" is the dominant pre-market headline. UNH shows a genuine contradiction worth carrying into the open: an earnings-beat/rally headline (2026-07-16) sits alongside a DOJ antitrust-probe-expansion headline (Claritev review) the same day — resolve via price action at the open, not via either headline alone.

### Market Mood / Risk Routing

- Crypto mood: **risk-off**
- Stocks mood: **pre-market / mixed** (VIX rising, QQQ weak, SPY flat, chip-sector headline risk)
- Dominant narrative: Iran-US Gulf conflict escalation (macro risk-off driver); secondary: AI-sector rotation basket (mixed/fading), perps-DEX narrative (HYPE-led, fresh <1h)
- Preferred side now: **shorts** (crypto) / **wait-for-RTH-confirmation** (stocks)
- Best long candidate: none clean in crypto (BANK/KAITO are counter-tape watchlist-only); **XOM** for stocks, pending RTH confirmation
- Best short candidate: **TAO/USDT** (already active, B-tier swing, aligned with regime) in crypto; **AVGO** for stocks, pending RTH confirmation
- Best catalyst-backed candidate: none clean — catalyst mapping is weak this run; BONK is the highest-importance verified item but is a risk-flag, not a setup
- What to avoid: **MSFT** (active legal gate), **HOME/USDT** (overextended chase risk), fresh no-catalyst altcoin breakouts in general (14d no-news cut on intraday momentum reads WR 23% / PF 0.70 / -3R per the report's own playbook note)
- What would change the view: a de-escalation headline out of the Gulf (oil reversing, no further strikes) would ease the crypto risk-off read; a clean RTH open above/below the AVGO/XOM pre-market levels with volume would confirm those two stocks ideas either way

## 7. Candidate Deep Dives

### 1. TAO/USDT — B, swing, short, ACTIVE (triggered 05:36 EEST)

- Entry zone 191.036-192.016 (already filled), stop/invalidation 193.214, TP1 188.421 (1.2R) / TP2 186.243 (2.2R) / TP3 184.064 (3.2R). Expires 2026-07-24T02:36 UTC (168h swing window).
- Has price already reacted to a catalyst? No — this is a pure technical/regime thesis (breakdown/retest, momentum score 68.3, weak_vs_market tag); no fresh verified catalyst for TAO specifically.
- Chasing? No — entry was the failed-bounce/retest zone, already filled cleanly per plan.
- Retest/pullback structure? Yes — this is exactly the retest entry the playbook called for.
- Overextended? No signal of it; TAO's watchlist re-scan at 11:32 EEST (separate C-tier idea, same symbol, different report) shows price at 189.50, already through TP1's neighborhood zone, consistent with the short working.
- Aligned with market mood? Yes — bearish/risk-off regime, derivatives context (price down + OI up = fresh shorts pressing) supports continuation but also raises squeeze risk if BTC/ETH reclaim local levels.
- Actionable now? Already filled — manage the existing position, no new entry needed.
- Invalidates on: 1h close beyond 193.21, or BTC/ETH reclaiming local structure against the bearish thesis.
- Chase risk: no (already in). Catalyst confirmation: none, pure technical — treat as medium-confidence per the desk's own "medium" confidence label.

### 2. ONDO/USDT — B, intraday, long, ACTIVE (tp2_hit, at hard expiry)

- Entry 0.3652-0.3697 (filled), stop 0.3597, TP1 0.3817 (hit) / TP2 0.3917 (hit) / TP3 0.4017 (open). **Expires 2026-07-17T08:36:31 UTC = 11:36:31 EEST — essentially now** at review time.
- Lifecycle status: **ENTERED, TP1+TP2 hit, NEEDS REVIEW at expiry boundary.** This is not a missed entry and not a flat close — partial profit is already locked at minimum +2.2R equivalent; if TP3/stop is not resolved before the hard expiry, expect it to convert to entered-unresolved (0R *display* on the unresolved tail only — the TP1/TP2 legs already banked their R, per the desk's mandatory lifecycle vocabulary).
- Setup was a continuation/pullback long in a then-range/chop regime (created 2026-07-16), RS vs BTC +17.1% at entry, momentum score 90.6 — strong at entry, no fresh catalyst then or now.
- Actionable now? No new entry — position management only; next monitor tick should show its terminal state.

### 3. AVGO — stocks, short, was A (score 90), demoted C by market-closed gate

- Pre-market planning idea only; no RTH price action yet.
- Has price reacted to a catalyst? No specific AVGO catalyst found today beyond routine bullish commentary pieces ("1 Critical Reason to Buy Broadcom Stock on the Dip") — thesis is technical/quant-scored, not catalyst-driven, and the news tone (bullish commentary) mildly cuts against a short bias, worth weighing at the open.
- Actionable now? No — wait for the 16:30 EEST / 9:30 ET open and the first 15-30min range before treating as live; do not chase pre-market gaps.
- Aligned with mood? Consistent with the softer/chip-sector-weakness stocks tape.
- Chase risk: high if entered on a pre-market extrapolation without RTH confirmation.

### 4. XOM — stocks, long, was A (score 89), demoted C by market-closed gate

- Pre-market planning idea only; no RTH price action yet.
- Catalyst support: "ExxonMobil Is Poised for a Major Transformation by 2040" (Motley Fool, mildly supportive, long-horizon framing, not a near-term catalyst) — weak catalyst support, primarily technical.
- Actionable now? No — same RTH-confirmation requirement as AVGO.
- Aligned with mood? Energy has been a relative-strength pocket historically during Gulf-tension macro risk-off episodes (oil bid) — plausibly aligned, but not confirmed by today's data alone.

### 5. MSFT — stocks, long, was B (score 74), demoted C by active legal/headline gate — AVOID / MANUAL REVIEW

- Active securities-fraud shareholder-lawsuit headline (PR Newswire, routine law-firm investor-deadline notice, but the pipeline's `legal_headline_risk: securities_fraud` gate is correctly live on this name).
- Would otherwise have scored B-tier long on technicals — this is exactly the contradiction-risk category (tier ties broken by legal risk, not technical quality).
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED** — do not treat as actionable regardless of technical score until a human clears the legal flag.

## 8. Best Candidates Ranked

1. **TAO/USDT short** (crypto, B, swing) — already active, cleanest idea on the desk, aligned with regime, working the plan.
2. **XOM long-watch** (stocks) — best pre-tier stocks long idea, needs RTH confirmation at ~16:30 EEST.
3. **AVGO short-watch** (stocks) — best pre-tier stocks short idea, needs RTH confirmation at ~16:30 EEST.
4. **BANK/KAITO long-watch** (crypto, C-tier, counter-tape) — only if a pullback zone (BANK 0.0620-0.0630, KAITO 0.8617-0.8747) is defended with volume; reduce size given counter-tape context; do not chase the existing +14-20%/24h move.
5. **BONK catalyst-watch** (crypto) — exploit-fallout narrative (importance 0.82), watch for confirmed follow-through decline with volume before treating as short-actionable; currently only an operator-review risk flag.

## 9. Avoid / No Trade

This applies to the current decision window only — scanning, tracking, and all monitors continue unaffected.

- **MSFT** — active securities-fraud legal/headline gate; AVOID/MANUAL REVIEW until cleared.
- **HOME/USDT** — already -39.4%/24h, elevated negative funding and crowding, overextended; chase risk on any further short entry without a bounce/retest first.
- **Fresh no-catalyst altcoin momentum entries generally** — the desk's own playbook note flags this bucket net-negative over the trailing 14d (WR 23% / PF 0.70 / -3R); TAO/SUI/GRAM/WLD/AIGENSYN watchlist ideas are all in this bucket and stay watchlist-only, not actionable, without an RS-leader or breakout confirmation.
- **All pre-market stocks levels (AVGO, XOM, and the rest of the demoted-A/B list)** — not a no-trade verdict on the ideas themselves, just not yet actionable pending RTH confirmation.

## 10. Main Risks

- Iran-US Gulf conflict escalation is the dominant, fast-moving macro risk — any further strikes/de-escalation headline can move BTC/ETH and oil-linked stocks names (XOM) quickly; re-check before the US open.
- ONDO's hard-expiry timing (right at review time) means its final resolution won't be visible until the next monitor tick — needs-review status, not a data error.
- Catalyst mapping weak (82.8% unmapped) — do not over-weight the catalyst layer for any decision this cycle.
- mexc_canary_monitor crash-looping on a locked DB while writing kill-switch state — a live-execution safety-mechanism reliability concern (TODO-8), outside this review's read-only scope to fix.
- Stocks intraday A/B guard continues to block 100% of technically-qualified candidates market-closed pre-open (expected at this hour) — the deeper question of whether the guard is correctly calibrated (TODO-1) still needs human sign-off.

## 11. Action Plan — next 4 hours

- Manage TAO short toward TP1/TP2/TP3 per the existing plan; no new entry needed.
- Watch ONDO's next monitor tick for terminal resolution (TP3, stop, or unresolved-expiry) — no action needed, just confirm it settles cleanly.
- Into the 16:20 EEST pre-US-open review: re-check AVGO/XOM pre-market reaction, confirm MSFT's legal gate is still live, re-verify UNH's DOJ-vs-earnings contradiction hasn't resolved either direction.
- Re-run `detect_untracked_legacy_alerts` next cycle — flag to a human if ALLO/BANK cross 24h unresolved (TODO-3, already high priority).
- No action on BANK/KAITO longs unless a defended pullback with volume confirmation appears — do not chase the existing move.

## 12. Final Verdict per Mode

- **Crypto scalp**: no A/B setups; mode itself is a losing bucket this week (PF 0.30) — no action, data-collection only.
- **Crypto intraday**: no A/B setups; ONDO position resolving at expiry — monitor only.
- **Crypto swing**: TAO short active and working the plan — manage existing position, no new entries (swing report itself is carry-forward/stale, do not source new swing ideas from it this cycle).
- **Stocks intraday**: no actionable setups pre-market; AVGO/XOM are the watch-list for RTH confirmation at the open.
- **Stocks swing/invest**: deprecated legacy framework, no read this cycle.

## 13. Sources

- Internal only this cycle — no external WebSearch/WebFetch was required; internal `news_items`/catalyst records for UNH (DOJ probe vs earnings) and TAO/BANK/AVGO/XOM/MSFT were fresh (<24h) and internally consistent enough to avoid external verification, per the internal-first rule.
- [UnitedHealth Group (UNH) Faces Wider DOJ Antitrust Probe As Claritev Review Expands](https://finance.yahoo.com) — Yahoo Finance, 2026-07-16 (internal `news_items` record; URL not independently re-fetched this cycle).
- [UnitedHealth now has an improved outlook for the year. Its stock is rallying.](https://www.marketwatch.com) — MarketWatch, 2026-07-16 (internal `news_items` record).
- Macro headlines (Iran-US Gulf conflict, Strait of Hormuz) — sourced from today's intraday/scalp report §4, original feed attribution not individually re-verified this cycle (internal aggregation only).

## 14. Fix Requests / TODO

### TODO-1 (carried forward, unchanged)
- **issue:** Stocks intraday A/B guard combination continues to block ~100% of technically-qualified candidates (18 demoted A/B->C this cycle, purely by market-closed gate pre-open — expected at this hour, but the underlying guard calibration question from prior reviews is still open).
- **evidence:** `data/reports/stocks/intraday/2026-07-17_06-13_stocks_intraday_report.md` — "Demoted A/B→C by gates: 18 (RR / rolling guard / legal / earnings / market-closed / ATR-only TP1)".
- **suggested manual fix:** human sign-off on whether the guard calibration is intentional (multi-cycle consistent negative forward evidence already noted in prior reviews) or needs adjustment.
- **priority:** medium
- **first observed:** 2026-07-16 18:39 EEST review (still open, 3rd+ consecutive review cycle).

### TODO-2 (carried forward, confirmed still present — evidence significantly stronger, priority raised to high)
- **issue:** Many stocks signals show `expires_at` timestamps well in the past while still displaying non-terminal statuses (`tp1_hit`, `tp2_hit`, `triggered`) instead of a closed/expired terminal state. A direct DB check this cycle (beyond just the 50-row `active-signals` CLI window) found this is systemic, not a handful of edge cases: of 231 stocks signals currently sitting in a non-terminal status (`tp1_hit`=111, `triggered`=79, `tp2_hit`=41), **129 (56%)** already have an `expires_at` in the past — some by nearly 7 weeks (e.g. a DIA `tp1_hit` C-tier signal expired 2026-05-30, an SMH `tp1_hit` B-tier signal expired 2026-06-05).
- **evidence:** `python -m src.cli active-signals --asset-class stocks` today (12+ visible examples: JPM expires 2026-07-11, COIN expires 2026-07-03, XLY expires 2026-07-10, etc.); direct SQL against `db/crypto_ai_desk.sqlite` `proposed_signals` table this cycle: `SELECT status, COUNT(*) FROM proposed_signals WHERE asset_class='stocks' GROUP BY status` and an `expires_at`-vs-now comparison on the 3 non-terminal statuses, confirming 129/231 past expiry.
- **suggested manual fix:** human check of the lifecycle/track-signals job for stocks — this looks like a systemic terminalization failure (job not running, or silently failing, for a meaningful fraction of stocks signals) rather than isolated stragglers; worth checking whether the equivalent crypto-side job is healthy for comparison.
- **priority:** high (raised from medium given the DB-wide scope confirmed this cycle).
- **first observed:** 2026-07-16 16:20 EEST review (scope significantly re-scoped/escalated 2026-07-17 11:45 EEST).

### TODO-3 (carried forward, unchanged — still high)
- **issue:** `detect_untracked_legacy_alerts` still returns exactly 2 unresolved results: ALLO/USDT (swing B, 65.4, sent 2026-07-16T14:27:05 UTC — now ~21h unresolved) and BANK/USDT (intraday B, 65.0, sent 2026-07-16T21:36:05 UTC — now ~14h unresolved). Zero new watchlist alerts fired for any symbol since 2026-07-16T21:36:05 UTC (confirmed via `--since 2026-07-17` returning 0 results).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-16` (2 results, unchanged across at least 3 consecutive reviews) and `--since 2026-07-17` (0 new).
- **suggested manual fix:** human check of the watchlist-alert re-fire path for symbols whose most recent same-mode `proposed_signal` has already closed — unchanged recommendation from prior reviews.
- **priority:** high (unchanged, now the longest-running open item).
- **first observed:** 2026-07-16 18:39 EEST review (ALLO/USDT); BANK/USDT 2026-07-17 02:45 EEST; unchanged through 04:39 and 11:45 EEST.

### TODO-4 (carried forward, still not independently re-checked)
- **issue:** The `paper entry-mode classify` scheduler step failed (exit=1) in a 2026-07-16 cycle — non-fatal, cycle continued. Not independently re-verified this cycle either (today's `cycle_03_08-43_summary.md` was read for freshness only, not step-by-step).
- **evidence:** `data/scheduled_runs/2026-07-16_default_schedule/scheduler.log` (previous day, not re-read this cycle).
- **suggested manual fix:** human check whether this recurred in any of today's 3 cycles so far, or was a one-off.
- **priority:** low
- **first observed:** 2026-07-16 21:39 EEST review.

### TODO-5 (resolved, informational — no action needed)
- **issue:** A prior post-close review fired ~3.5h late; the 04:39 EEST slot fired on-time (~9min jitter). Today's 11:30-slot review also fired within normal jitter (~9-15min). Dispatch timing looks stable across the last 3 slots.
- **evidence:** on-time dispatch this cycle and last cycle.
- **suggested manual fix:** none; close this item unless a future slot fires >30min late.
- **priority:** low (informational).
- **first observed:** 2026-07-17 02:45 EEST review; confirmed resolved 2026-07-17 04:39 and 11:45 EEST.

### TODO-6 (new)
- **issue:** Crypto scalp mode is a consistent losing bucket this week: n=24, PF 0.30, avgR -0.18, totalR -3.5 (weak confidence), while the scalp report itself already carries a header noting "TP1/2h horizon mismatch caps capture (1W/7L over 14d, PF 0.14)" — the mismatch is known but scalp remains fully live for data collection, contributing negative R weekly.
- **evidence:** `signal-stats --asset-class crypto` this cycle, "By mode" table: `mode=scalp | n=24 | PF 0.300000 | avgR -0.184200 | totalR -3.5000`; scalp report header self-disclosure.
- **suggested manual fix:** human review of whether scalp's data-collection-only status should be reinforced more strongly (e.g. explicit non-actionable labeling) given the consistency of the negative edge, or whether the horizon mismatch fix is scheduled.
- **priority:** medium.
- **first observed:** 2026-07-17 11:45 EEST review.

### TODO-7 (new)
- **issue:** Stocks earnings-date confidence shows "(unknown)" for at least TSLA and GOOGL ("earnings in 5 trading-ish days (unknown)") in today's stocks intraday report — an earnings-calendar data-quality gap that could affect the earnings-proximity gate's reliability.
- **evidence:** `data/reports/stocks/intraday/2026-07-17_06-13_stocks_intraday_report.md` §3, lines 48-49.
- **suggested manual fix:** human audit of the earnings-calendar source/ingestion for TSLA/GOOGL and any other symbols showing `(unknown)` confidence.
- **priority:** low-medium.
- **first observed:** 2026-07-17 11:45 EEST review.

### TODO-8 (new — high priority)
- **issue:** `mexc_canary_monitor` (live-execution kill-switch/canary process) is crash-looping on `sqlite3.OperationalError: database is locked` inside `ensure_tables()` while trying to write `INSERT OR IGNORE INTO mexc_canary_control(control_key='kill_switch', control_value='CLEAR', ...)`. 4 separate log files today (03:30, 06:24, 08:59, 11:33 EEST), each ending in the same traceback — consistent with the process crashing and being auto-restarted roughly every ~2.5h rather than running continuously.
- **evidence:** `data/scheduled_runs/2026-07-17_default_schedule/mexc_canary_monitor_1784276394.log` (and the 3 earlier same-day logs) — traceback at `src/live_execution/store.py:142` in `ensure_tables`, `src/live_execution/service.py:355` in `worker_once`, `src/cli.py:1688` in `mexc_canary_monitor`.
- **suggested manual fix:** human investigation of the lock contention on `db/crypto_ai_desk.sqlite` around `mexc_canary_control` writes (likely a concurrent-writer/WAL-mode/timeout issue) — this touches a kill-switch write path, so treat with real urgency even though it is currently self-recovering via restart.
- **priority:** high.
- **first observed:** 2026-07-17 11:45 EEST review.

### TODO-9 (new)
- **issue:** `market_dashboard_snapshots` continues to label `crypto_market_mode=trend` / `crypto_regime=bullish trend` while both fresh crypto reports (scalp, intraday) independently read `bearish trend (risk-off)` with BTC/ETH `transition_down` — the same dashboard/report label inconsistency noted (but not formally logged as a TODO) in the 04:39 EEST review, still present now with the two labels even further apart (bullish vs bearish, not just a mild mismatch).
- **evidence:** `market_dashboard_snapshots` latest row (08:41 EEST): `crypto_market_mode=trend`, `crypto_regime=bullish trend`. `data/reports/intraday/2026-07-17_08-32_intraday_report.md` line 7: "Market regime: bearish trend (risk-off)".
- **suggested manual fix:** human check of the dashboard-generation job's regime-classification input vs the report-level regime classifier — they appear to be two independent classifiers that have now diverged to opposite labels.
- **priority:** medium.
- **first observed:** 2026-07-17 11:45 EEST review (label divergence first informally noted 04:39 EEST, now formally logged).
