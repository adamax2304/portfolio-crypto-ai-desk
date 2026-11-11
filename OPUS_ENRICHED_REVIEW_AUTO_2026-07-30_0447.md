# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (04:30 EEST — overnight crypto action, Asia session; stocks market closed, planning/watchlist context only). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** External web research was available and used this run. The book carried three crypto positions into the Asia window: **BANK/USDT** (swing short, OPEN, dormant ~14h, price -8.6% 24h — favorable drift, thesis intact) and **ACH/USDT** (swing long, OPEN — NOT closed despite the CLI displaying `tp2_hit`; the realistic paper-execution model shows this is still `lifecycle_state=OPEN` with a profit-lock armed at +0.5R, price now +21.5% 24h and explicitly flagged "more than 2 ATR from EMA20 — do not chase" in the freshest scan). A **new fill** appeared this cycle: **DEXE/USDT** scalp short, triggered 00:45 UTC via the `watchlist-monitor` fast-scan path — but the same symbol was explicitly demoted to C-tier 8 minutes earlier in the 00:37 UTC scalp batch report for `crypto_scalp_disabled (kill-switch: mode off, any hour/day)`. This is a **live gating-bypass**: the mode-level scalp kill-switch is enforced in the batch scan but not in the watchlist-monitor promotion path, letting a real paper position open in a mode the desk explicitly disabled for being net-negative (§14 TODO, high priority). External verification confirms DEXE itself is a genuinely late short: the token crashed ~85-90% from its July 13 ATH (~$48.89) to ~$2.73 today after a $6M project-wallet-to-Binance transfer, i.e. shorting here risks chasing an already-exhausted breakdown (matches the internal report's own `late_short_after_exhaustion` tag). **KAITO/USDT** (the prior review's best long-watch, waiting for a pullback into 1.3036-1.3202) resolved `entry_moved_away` overnight — price never pulled back, extension continued. Macro backdrop: internal macro-risk scoring reads 98.4-100/100 (very high risk-off) across scalp/swing scans; BTC ~$63.8-64K / ETH ~$1.9K roughly flat externally; the Iran/Iraq/Jordan conflict remains a live overnight tail risk with no confirmed further escalation since the last review. Catalyst mapping is weak this run (60.6% unmapped). A fresh catalyst contradiction: the `perps_dex_narrative` basket (HYPE) carries a bullish Grayscale framing, but a same-hour Telegram/on-chain read shows Multicoin Capital and Bitwise depositing large HYPE amounts into Coinbase Prime (institutional selling) — treat HYPE as **contradicted, not actionable either direction**. Scanning, tracking, and monitors continue into the Europe session in every mood; this review recommends caution and position management, never a stop.

## 2. Data Used

| File / Source | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-30_00-37_scalp_report.md` | 03:37 EEST | ~1h10m |
| `data/reports/intraday/2026-07-30_00-44_intraday_report.md` | 03:44 EEST | ~1h03m |
| `data/reports/swing/2026-07-30_01-36_swing_report.md` | 04:36 EEST | ~11m — very fresh |
| `data/reports/stocks/intraday/2026-07-30_01-12_stocks_intraday_report.md` | 04:12 EEST | ~35m (market closed — planning only) |
| `data/reports/stocks/swing/…` / `invest/…` (2026-07-02) | deprecated/removed playbooks — see [[project_crypto_ai_desk_stocks_position_framework]], not a freshness failure |
| `data/catalysts/2026-07-30/catalyst_events.jsonl` (500 rows) + `narrative_baskets.jsonl` (2) | ~03:49 EEST | ~58m |
| `reports/PAPER_MONITOR_STATUS_LATEST.md` | 04:24 EEST | ~23m, but **predates** ACH's touch of TP2 and the DEXE fill — cross-checked directly against live `proposed_signals` / `paper_execution_outcomes` |
| `python -m src.cli active-signals --asset-class crypto` / `stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` / `stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-30` | live query | now — none found |
| `db/crypto_ai_desk.sqlite` `proposed_signals` / `paper_execution_outcomes` / `watchlist_alerts` / `news_items` (direct query) | live query | now |
| `data/scheduled_runs/2026-07-30_default_schedule/scheduler.log` | 03:16 EEST | ~1h31m |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-29_2315.md` | 23:31 EEST | for §4 diff |
| WebSearch: BTC/ETH price today, DeXe (DEXE) crypto news July 2026, Iran/Iraq/Jordan war update | live | now |
| WebFetch: CoinGecko DEXE page (verified current price/24h change) | live | now |

**External web research was available and used this run.**

## 3. Scheduler / Data Freshness

- Scheduler log last write 03:16 EEST (~1h31m) — well within the 3h defer threshold; **not deferred**. Latest cycle summary `cycle_04_00-41_summary.md` (folder `2026-07-29_default_schedule`, mtime 01:27 EEST) is the most recent full-cycle record; no `cycle_*_summary.md` yet exists in today's `2026-07-30_default_schedule` folder (only `scheduler.log`), consistent with the scheduler being mid-cycle.
- Crypto scalp/intraday reports fresh (~1h03-10m). Crypto swing report is exceptionally fresh (~11m, generated essentially at review time).
- Stocks-intraday report fresh (~35m) but market is **closed** overnight — all today's stocks signals are C-tier `waiting_for_entry` / `missed_no_entry`, planning-only.
- Catalyst JSONL/baskets last wrote ~03:49 EEST (~58m) — usable, not stale.
- `detect_untracked_legacy_alerts --since 2026-07-30`: **None** — every legacy crypto alert has a backing proposed_signal. [[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]] (the reverse-direction bug: alert without a signal) not triggered this cycle — but see §14 for a **related, different** integrity issue found this cycle (signal created via a gating-bypass, not a missing-backing issue).
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (04:24 EEST) shows OPEN_ACTIVE=2 (BANK, ACH) and WAITING_FOR_ENTRY=0 — this **predates** two live developments confirmed by direct DB query just now: (1) ACH touched TP2 (`touch_r=2.5`, `highest_tp_touched=2`) but remains `lifecycle_state=OPEN` under the realistic `early_mfe_protection_v1` model (lock armed at +0.5R) — **not** a closed win; (2) a new DEXE/USDT scalp short (`sig_6bd41cf0585d5c9c`) triggered at 00:45 UTC, still open, expires 02:45 UTC (~1h from now at review time). Both cross-checked directly via `proposed_signals` + `paper_execution_outcomes`, not the stale snapshot.
- **XOM lifecycle anomaly persists, 5th+ consecutive cycle**: `reports/PAPER_MONITOR_STATUS_LATEST.md` line 165 still shows `XOM long (stocks/intraday/B) — STATUS NEEDS REVIEW — inconsistent lifecycle fields · unmapped status 'tp2_hit'`, unchanged since ≥2026-07-29 15:59 EEST (see §14).
- Crypto DB direct query (signals created since 20:00 UTC 07-29): DEXE/USDT (scalp short, **triggered**, via watchlist-monitor bypass — see §14), ACH/USDT (scalp long, `expired` — a second, separate ACH idea that never filled), plus the already-open ACH/USDT swing long and BANK/USDT swing short from the prior cycle. KAITO/USDT swing long (previously WAITING) resolved `entry_moved_away`. The older DEXE/USDT intraday short (waiting since 16:00 UTC) resolved `stale_before_entry`.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-30 04:47 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["PAPER_MONITOR_STATUS_LATEST.md (04:24 EEST) predates ACH's TP2 touch and the DEXE fill; cross-checked directly against proposed_signals/paper_execution_outcomes"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 03:16 EEST (~1h31m)", "swing report ~11m fresh, scalp/intraday ~1h03-10m fresh", "stocks-intraday ~35m fresh but market closed", "catalyst JSONL ~58m fresh (500 rows, 2 baskets)", "detect_untracked_legacy_alerts: none"] },
    { "agent": "market_regime", "verdict": "risk_off", "confidence": 0.82,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"],
      "data_missing": ["no fresh overnight stocks pre-market read (market closed)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Internal regime label: bearish trend (risk-off) across scalp/intraday/swing", "BTC downtrend, ETH uptrend (split regime), 22.5% of tracked symbols above EMA20 (weak breadth), BTC ATR percentile 89 (elevated)", "Macro/geopolitics internal risk score 98.4-100/100 from 8 risk-off hits vs 0-1 risk-on hits", "External spot check: BTC ~$63.8-64K, ETH ~$1.9K, roughly flat/range-bound per July 30 outlook (63k-66k range expected)", "Iran/Iraq/Jordan war ongoing (Jordan intercepted 5 missiles, US-Saudi strikes killed 20+ PMF in Iraq) — no confirmed further escalation overnight beyond what the 23:15 EEST review already captured"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "catalyst_contradicted"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl (500 rows, ~03:49 EEST): 197 mapped (39.4%), 303 unmapped (60.6%) — weak-mapping threshold breached", "2 active narrative baskets: perps_dex_narrative (HYPE, primary, source single_source, playbook wait_pullback) and momentum_breakout (COTI/ACH/RE, explicitly 'top gainers WITHOUT confirmed news catalyst', playbook avoid_chase, COTI flagged overextended)", "Fresh (<1h) news_items row for HYPE: Multicoin Capital + Bitwise depositing large HYPE amounts into Coinbase Prime (t.me/lookonchain, CryptoBriefing) — institutional-selling signal that CONTRADICTS the basket's bullish Grayscale framing", "No fresh (<24h) news_items row for DEXE, ACH, or BANK beyond the momentum-basket auto-tag — all three remain no-catalyst technical/momentum setups"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["no fresher-than-04:36-EEST funding/OI read for BANK/ACH", "DEXE derivatives snapshot is from the 00:45 UTC fill, ~1h old"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACH/USDT (04:36 EEST swing scan): funding -0.00148, OI +45.0% 24h, long/short 1.354, crowding unknown — 'price up + OI up: fresh positioning confirms trend' but crowding unresolved on a name already 2+ ATR extended", "DEXE/USDT (00:45 UTC fill): funding -0.00048, OI -1.75%, 'price down + OI down: deleveraging or long liquidation', squeeze_potential explicitly 'normal' (not elevated) per the desk's own model", "BANK/USDT: no fresher derivatives read this cycle than the dormant 19:26 EEST scan carried in the prior review (funding -0.00167, OI +16.71%) — still unresolved, still dormant"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["overextended", "chase_risk", "entry_late", "entry_fresh"],
      "data_missing": ["TradingView / manual chart check unavailable this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACH/USDT: 24h return now +21.54% (up from +17.9% at the 23:15 EEST review), the FRESHEST swing scan (04:36 EEST) explicitly gate-rejects a fresh long here: 'Price is more than 2 ATR from EMA20; do not chase' — position is already open and managed, not a new entry, but any add would repeat the exact overextension already twice-flagged", "DEXE/USDT: entered 2.71048-2.75433 (00:45 UTC); external verification (CoinGecko, live) shows current price ~$2.73, -5.3% 24h — sitting mid-zone, no clear directional resolution yet; token is down ~85-90% from its July 13 ATH ($48.89) after a $6M wallet-to-Binance transfer — shorting here is itself late/chase-risk against an already-exhausted move (matches the internal 'late_short_after_exhaustion' tag and counter-thesis)", "BANK/USDT: 24h -8.6%, RS vs BTC -8.89% — directionally favorable drift for the open short, but touch_r still 0.0 (no realized MFE since entry) per paper_execution_outcomes; dormant, not chasing"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.75,
      "reason_codes": ["open_actionable", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["OPEN actionable = 3 (live DB, corrects the stale 04:24 EEST monitor snapshot's count of 2): BANK/USDT (swing short, entered 14:50 UTC 07-29, dormant, touch_r=0.0), ACH/USDT (swing long, entered 18:47 UTC 07-29, touch_r=2.5/highest_tp_touched=2 but lifecycle_state=OPEN with lock armed at +0.5R — NOT a closed win), DEXE/USDT (scalp short, entered 00:45 UTC 07-30, touch_r=0.0, expires 02:45 UTC — an entered-unresolved-soon position, watch the window)", "NO-ENTRY / MOVED-AWAY this cycle: KAITO/USDT swing long (`entry_moved_away` — the prior review's best long-watch never got its pullback), DEXE/USDT intraday short from 16:00 UTC (`stale_before_entry`), ACH/USDT scalp long from 22:42 UTC (`expired`, price never touched)", "NEEDS REVIEW = 1 (XOM, stocks/intraday/B, unmapped `tp2_hit` status) — 5th+ consecutive cycle unresolved, see §14", "detect_untracked_legacy_alerts: none — no reverse-direction (alert-without-signal) integrity failure this cycle"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Iran/Iraq/Jordan war remains a live, unresolved overnight tail risk (missiles intercepted over Jordan, 20+ PMF killed in US-Saudi strikes on Iraq) — no de-escalation confirmed", "Internal macro-risk scoring at 98.4-100/100 this cycle — among the highest reads seen across recent cycles", "DEXE/USDT open position was created via a kill-switch bypass (crypto_scalp_disabled did not block the watchlist-monitor promotion path) — real paper capital is now exposed in a mode the desk explicitly disabled for being net-negative; recommend manual review of this specific position, not a blanket panic", "ACH/USDT open long is 2+ ATR extended per the freshest scan; the profit-lock at +0.5R limits downside but the position should not be added to", "Crypto shorts (all modes, this week) show PF 0.5/n=12 — a weak sample, worth noting even though the regime otherwise favors shorts"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample", "fresh_expired_problem"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto B-tier headline (week, live query): PF 2.6647, 23W/25L, +28.3R over 83 triggered — net positive but triggered win-rate only 27.7% (system's own observation, manual review required)", "By mode: scalp PF 0.20/avgR -0.25/n=20 (weak, net-negative, this is the exact mode DEXE's new position sits in) vs swing PF 3.90/n=33 and intraday PF 3.40/n=33 (both stronger)", "By direction: short PF 0.50/n=12 (weak) vs long PF 2.95/n=74 (stronger) — shorts underperform this week despite the risk-off regime nominally favoring them", "Stocks headline actionable: sample=2, anecdotal, PF 0.0, totalR -1.0 (just the NVDA loss) — too small to read; stocks C-tier watchlist PF 0.20, 5W/12L, net negative, consistent with prior cycles, research-only per [[project_crypto_ai_desk_stocks_intraday_hardening]]"] },
    { "agent": "head_trader", "verdict": "caution",
      "reason_codes": ["route_not_block"],
      "confidence": 0.63,
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Three open crypto positions overnight (BANK short dormant, ACH long extended-but-locked, DEXE short newly-filled-via-bypass) — a manage-and-watch cycle, not a no-trade cycle, and not a fresh-entry cycle either", "The DEXE fill is a genuine gating-bypass integrity issue that deserves manual review of that specific position, separate from the broader risk-off regime read", "KAITO's pullback never came (entry_moved_away) — the best long-watch from the last two reviews is now closed out with no fill; no replacement long-watch has emerged yet", "HYPE is catalyst-contradicted (bullish narrative basket vs bearish whale-flow news) — not actionable in either direction until the contradiction resolves", "Stocks market is closed; nothing actionable until European pre-market color and the eventual US pre-market"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.63,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "ACH/USDT", "trigger": "already open (~18:47 UTC 07-29) — manage existing position only, do not add; profit-lock armed at +0.5R; would need a pullback toward EMA20 before any fresh add could be considered", "reason": "the only open long; 2+ ATR extended per the freshest scan, no-catalyst momentum name — reduce-conviction management, not a fresh idea" },
    "best_short_candidate":    { "symbol": "BANK/USDT", "trigger": "already open (~14:50 UTC 07-29) — manage existing position only, do not add; respect stop 0.19683", "reason": "cleanest open short into the Asia session; price drifting favorably (-8.6% 24h) though touch_r still 0.0; squeeze risk flagged historically but dormant" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "contradiction must resolve first — either a confirmed on-chain reversal (whales stop depositing to exchanges) for the bullish case, or a confirmed breakdown below the recent range for the bearish case; not actionable either direction now", "reason": "closest active catalyst basket (perps_dex_narrative), but a same-hour news_items row (Multicoin/Bitwise depositing to Coinbase Prime) directly contradicts the basket's bullish Grayscale framing" },
    "avoid_candidate":         { "symbol": "DEXE/USDT (as a template for new entries) and KAITO/USDT (re-chase)", "reason": "DEXE's open position resulted from a kill-switch bypass and is itself a late short into an already -85-90%-from-ATH token — manage the existing fill to its 02:45 UTC expiry, do not treat it as a repeatable setup; KAITO's entry zone was never reached and chasing the continued extension repeats the exact overextension flagged in the last two reviews" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | risk_off | 0.82 | risk_off, shorts_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.62 | overextended, chase_risk, entry_late, entry_fresh | advisory_only |
| execution_lifecycle | needs_review | 0.75 | open_actionable, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.68 | headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample, fresh_expired_problem | advisory_only |
| head_trader | caution | 0.63 | route_not_block | advisory_only |

## 4. What Changed vs Previous Review (23:15 EEST, post-close final daily review)

- **ACH/USDT touched TP2 but is NOT closed**: 24h return extended from +17.9% to **+21.54%**; the CLI's touch-based status shows `tp2_hit`, but the realistic `early_mfe_protection_v1` paper-execution model shows `lifecycle_state=OPEN`, protection/lock armed at +0.5R, `paper_execution_r=None` (unresolved). This is exactly the touch-vs-realistic distinction flagged in [[project_crypto_ai_desk_touch_based_pnl]] — do not report this as a win yet.
- **NEW fill: DEXE/USDT scalp short triggered** (00:45 UTC) via the `watchlist-monitor` promotion path — **8 minutes after** the 00:37 UTC scalp batch report explicitly demoted the same symbol to C-tier for `crypto_scalp_disabled`. A genuine gating-bypass, not present in the 23:15 EEST review (§14, new TODO).
- **KAITO/USDT resolved `entry_moved_away`**: the prior two reviews' best long-watch (waiting for a pullback into 1.3036-1.3202) never got its pullback; the order aged out. No replacement long-watch has emerged.
- **Old DEXE/USDT intraday short (16:00 UTC) resolved `stale_before_entry`** — a separate, unrelated signal from the one that filled above.
- **A second ACH/USDT idea (scalp long, 22:42 UTC) resolved `expired`** — never touched, unrelated to the open swing long.
- **Catalyst mapping**: 60.6% unmapped (197/500) this cycle vs 66.0% at 23:15 EEST (different day's catalyst folder) — still weak, roughly the same order of magnitude.
- **BANK/USDT unchanged in substance**: still open, still dormant by touch_r (0.0), but 24h return now -8.6% (favorable drift for the short) vs "flat ~0.17" at 23:15 EEST.
- **Macro risk-off internal scoring intensified**: 98.4-100/100 across today's scans vs the external VIX-driven read carried at 23:15 EEST — consistent direction, higher internal confidence.
- **Stocks**: still closed; no new stocks A/B; all fresh stocks C-tier signals from the 01:11 UTC scan are `waiting_for_entry` or `missed_no_entry` (pre-market/planning only).

## 5. Catalyst Coverage

- Total catalyst events (~03:49 EEST snapshot): **500**
- Mapped (non-null symbol): **197** (39.4%)
- Unmapped (null symbol): **303** (60.6%)
- Narrative baskets: **2** — perps_dex_narrative (HYPE/USDT, primary; related DYDX/GMX/ASTER), momentum_breakout (COTI/ACH/RE, explicitly "no confirmed news catalyst")
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped headlines (illustrative, macro/exchange-flow noise rather than symbol-specific):
  1. "California Water Service Group Reports Strong Second Quarter 2026 Financial Results" (unrelated equity, likely misfiled into the crypto catalyst stream)
  2. "250,000,000 $USDC (250,275,000 USD) minted at USDC Treasury" (routine stablecoin mint, no symbol tag)
  3. "Grayscale parent Digital Currency Group wrote to Senate leaders urging a CLARITY Act floor vote before the August recess"

## 6. Market Landscape

- **Crypto**: internal regime labels bearish trend/risk-off across scalp/intraday/swing; BTC downtrend, ETH uptrend (split), breadth weak (22.5% of tracked symbols above EMA20), BTC ATR percentile 89 (elevated). External spot check: BTC ~$63.8-64K, ETH ~$1.9K — roughly flat, July 30 outlook calls for a $63K-$66K range as markets digest the Fed. No confirmed reversal of the internal downtrend label.
- **Stocks**: market **closed** overnight (Asia session). Carrying forward yesterday's close as context only: Dow -2.19%, S&P -1.52%, Nasdaq -1.74% (correction territory), VIX +13.1% to 20.61 — a genuine risk-off close, not yet re-tested this cycle.
- **Dominant driver — into the Asia/Europe session**: the still-live, unresolved Iran/Iraq/Jordan conflict (Jordan intercepted 5 missiles; US-Saudi strikes killed 20+ PMF fighters in Iraq) remains the single largest overnight gap-risk factor for BTC/ETH; internal macro-risk scoring (98.4-100/100) is now at some of the highest levels seen in recent cycles.

### Market Mood / Risk Routing
- Crypto mood: **risk-off (bearish trend, elevated ATR, very high internal macro-risk score)** — external BTC/ETH roughly flat, no confirmed reversal.
- Stocks mood: **closed** — carrying forward yesterday's risk-off close (VIX +13.1%, Nasdaq correction); nothing fresh until European hours bring pre-market color.
- Dominant narrative: the Iran war remains the top macro overhang; on the symbol level, a no-catalyst momentum cluster (COTI/ACH/RE, all up double digits with no confirmed news) is running counter to the bearish tape, and the perps-DEX/HYPE narrative is internally contradicted by fresh institutional-selling on-chain flow.
- Preferred side now: **manage existing shorts and longs; no fresh directional conviction** — the regime nominally favors shorts, but crypto shorts have a weak sample this week (PF 0.5, n=12) and the one fresh short (DEXE) carries its own gating-bypass and chase-risk problems.
- Best long candidate: ACH/USDT — already open; manage only, do not add, respect the +0.5R lock; 2+ ATR extended, do not chase further.
- Best short candidate: BANK/USDT — already open; manage only, do not add, respect stop 0.19683.
- Best catalyst-backed candidate: HYPE/USDT — contradicted (bullish basket vs bearish whale-flow news); watch, not tradeable either direction yet.
- What to avoid: chasing ACH at the current extension; treating DEXE's bypass-created fill as a repeatable setup; re-chasing KAITO now that its pullback never arrived; any fresh crypto scalp ideas via any path until the kill-switch bypass is closed (§14).
- What would change the view: further Iran/Iraq/Jordan escalation or de-escalation; BTC reclaiming/losing local structure into the Europe open; a resolution (either direction) of the HYPE whale-flow-vs-narrative contradiction; European pre-market color feeding into the 11:30 EEST review.

## 7. Candidate Deep Dives

### 1. DEXE/USDT — crypto scalp short, ENTERED / OPEN (new fill, gating-bypass concern)
- Status: `triggered` at 00:45:09 UTC (~1h ago at review time); entry zone 2.71049-2.75433, invalidation 2.80791, TP1 2.59357, TP2 2.49614; expires 02:45:09 UTC (~1h from review time — watch the window).
- **Gating anomaly**: created via `report_id='watchlist-monitor-20260730-004509'`, `previous_tier='rejected'` → `new_tier='B'`. The 00:37 UTC scalp batch report explicitly scored this same symbol 68.2 (short) and demoted it to C for `crypto_scalp_disabled (kill-switch: mode off, any hour/day)`. The watchlist-monitor's independent 45s-cadence rescoring path does not appear to enforce the same mode-level kill-switch (§14).
- Has price already reacted? Yes, severely — external verification (CoinGecko, live fetch): current price ~$2.73, -5.3% 24h; the token crashed ~85-90% from its July 13 ATH (~$48.89) after a $6M project-wallet-to-Binance transfer, then had a brief ~90% bounce ~5 days ago before correcting again. Entering a fresh short here is a genuine late-short-into-exhaustion risk, not a fresh breakdown.
- Chasing? The internal report itself tags this `late_short_after_exhaustion` and its own counter-thesis states: "The short fails if DEXE/USDT is a late breakdown into exhausted sellers and BTC/ETH reclaim local levels."
- Retest/pullback structure? N/A — already filled; touch_r=0.0, stop_current_r=-1.0 (no MFE yet), protection not yet armed.
- Overextended? Directionally, the underlying 30-day move (-85-90% from ATH) is the extended leg, not the entry itself.
- Catalyst confirmation/contradiction: none — no fresh verified catalyst for DEXE in the last 24h beyond the generic momentum tag.
- Mood alignment: directionally consistent with the risk-off/short-biased regime label, but the desk's own squeeze model reads `squeeze_potential: normal` (not elevated) — the risk here is thesis-quality (late/exhausted), not an acute squeeze.
- **Verdict: OPEN, manage to the 02:45 UTC expiry only — do not treat as a template for new scalp shorts; flag for manual review given the gating-bypass origin (§14).**

### 2. ACH/USDT — crypto swing long, ENTERED / OPEN (touched TP2, still open under realistic model)
- Status: `triggered` at 18:47:36 UTC 07-29 (~10h ago); entry 0.00451-0.00461, invalidation 0.00438, TP1 0.00496, TP2 0.00520. CLI/status field shows `tp2_hit`, but `paper_execution_outcomes` shows `lifecycle_state=OPEN`, `touch_r=2.5`, `paper_execution_r=None`, `lock_armed=1` at `lock_level_r=0.5` — **the realistic model has NOT closed this trade; it has moved the stop up to lock a minimum +0.5R.**
- Has price already reacted? Yes, further than at the last review — 24h return now +21.54% (was +17.9% at 23:15 EEST), RS vs BTC +21.25%.
- Chasing? Already entered — management only. The freshest swing scan (04:36 EEST) explicitly gate-rejects a fresh long here: "Price is more than 2 ATR from EMA20; do not chase," "counter-tape long — reduce size."
- Catalyst confirmation/contradiction: none — ACH sits in the `momentum_breakout` basket, explicitly tagged "top gainers WITHOUT confirmed news catalyst," playbook `avoid_chase`. Derivatives: funding -0.00148, OI +45.0% 24h — fresh positioning confirms the move but crowding is "unknown."
- Mood alignment: partial — an RS-leader long against a bearish tape, no catalyst backing, now doubly-extended since the last review.
- **Verdict: OPEN — manage existing exposure only, do not add; the +0.5R lock protects against giveback; do not report as a closed win until `paper_execution_outcome` actually resolves.**

### 3. BANK/USDT — crypto swing short, ENTERED / OPEN (unchanged thesis, favorable drift)
- Status: `triggered` at 14:50:46 UTC 07-29 (~14h ago); entry 0.17447-0.18453, invalidation 0.19683, TP1 0.14094, TP2 0.11858.
- Has price already reacted? Directionally yes — 24h return now -8.6%, RS vs BTC -8.89% (favorable for the short), but `paper_execution_outcomes` still shows `touch_r=0.0` and no lock armed — treat as dormant/early-stage, not yet meaningfully in profit by the realistic model.
- Chasing? N/A — already in the trade; management only.
- Catalyst confirmation/contradiction: none — no fresh news_items row in 24h.
- Mood alignment: fits the risk-off/short-biased regime; cleanest open position this cycle.
- **Verdict: OPEN — manage existing exposure, do not add; respect the 0.19683 stop.**

### 4. HYPE/USDT — crypto catalyst-watch, contradicted, not actionable
- No open or waiting proposed_signal for HYPE this cycle — pure catalyst-watch.
- Catalyst basket (`perps_dex_narrative`, single_source, <1h freshness): bullish framing — "Grayscale says HYPE still looks cheap... projecting ~$1B in earnings for 2027," a Japan-listed company buying HYPE.
- **Contradiction**: a same-hour (00:37-00:44 UTC) news_items row from t.me/lookonchain + CryptoBriefing reports Multicoin Capital depositing another 137,100 HYPE (~$7.51M) and Bitwise depositing 22,463 HYPE (~$1.23M) into Coinbase Prime — a classic institutional-selling-pressure signal that directly contradicts the bullish narrative-basket framing.
- Would entry now be late/risky in either direction? Yes — the two data points actively disagree; entering long fights the fresh whale-flow signal, entering short fights the fresh catalyst-basket framing.
- **Verdict: WATCH ONLY — do not take either side until the contradiction resolves (either the whale outflows stop, or price confirms a breakdown consistent with the selling pressure).**

## 8. Best Candidates Ranked

1. **Manage existing (crypto): BANK/USDT** — open short, price drifting favorably (-8.6% 24h) but still touch_r=0.0/dormant by the realistic model; do not add, respect stop 0.19683.
2. **Manage existing (crypto): ACH/USDT** — open long, touched TP2 but still OPEN under the realistic model (+0.5R lock armed); do not add; 2+ ATR extended, do not chase further.
3. **Manage existing (crypto), flag for manual review: DEXE/USDT** — open short via a kill-switch-bypass fill; manage to its 02:45 UTC expiry; do not treat as a repeatable scalp setup (§14).
4. **Catalyst-watch (crypto): HYPE/USDT** — contradicted signal; watch for resolution, not actionable either direction.
5. **Best long-watch, none currently waiting**: KAITO/USDT's pullback never arrived (`entry_moved_away`); no replacement long-watch has emerged this cycle — the next fresh idea will need to clear the desk's own "do not chase" gates from scratch.
6. **Stocks: none actionable overnight** — market closed; all fresh C-tier ideas are `waiting_for_entry`/`missed_no_entry`, watch for the European/pre-US-open reviews.

## 9. Avoid / No Trade

This is a **decision-window-only** call, not a system-wide stop — scanning, tracking, and monitors continue regardless.

- **Adding to BANK/USDT or ACH/USDT** — both are open, managed positions; manage-don't-add cycle for both.
- **Chasing ACH/USDT at the current extension** — every fresh scan independently rejects a new long here.
- **Treating DEXE/USDT's fill as a repeatable scalp setup** — it exists because of a gating bypass, and the underlying short is itself a late-into-exhaustion thesis against an already -85-90%-from-ATH token.
- **Re-chasing KAITO/USDT** — its defined pullback zone was never reached; the extension has continued unconfirmed.
- **Taking a fresh position (either direction) in HYPE/USDT** — the catalyst basket and the fresh whale-flow news directly contradict each other.
- **Any fresh crypto scalp ideas via any path** — the mode is net-negative this week (PF 0.20) and now has a confirmed side-channel that bypasses its own kill-switch; treat scalp as fully paused for new ideas until §14 is resolved.
- **Any fresh stocks positioning overnight** — the market is closed; nothing is actionable until European/US hours.
- Nothing here is a command to pause the scanner, monitors, or data collection — all continue into the Europe session.

## 10. Main Risks

- **Crypto scalp kill-switch bypass (DEXE/USDT)** — the mode-level `crypto_scalp_disabled` gate is enforced in the batch scalp scan but not in the `watchlist-monitor` promotion path; a real paper position opened in a mode the desk explicitly disabled for being net-negative (PF 0.20 this week). This is a live-cost integrity issue, not just a display anomaly (§14, high priority).
- **Widening/unresolved Iran/Iraq/Jordan war** — still a live, escalating tail risk heading into the Europe session; the single largest overnight gap-risk factor for BTC/ETH.
- **ACH/USDT touch-based status could mislead** — the CLI/status field shows `tp2_hit`; anyone reading only that field (not the realistic paper-execution model) would incorrectly treat this as a closed win. Correct framing: OPEN, +0.5R locked, unresolved.
- **DEXE/USDT is a late short into an already-exhausted collapse** (-85-90% from ATH) — genuine chase-the-breakdown risk if BTC/ETH stabilize or a relief bounce occurs.
- **HYPE/USDT catalyst contradiction** — bullish narrative basket vs bearish institutional on-chain flow; treat as noise until resolved, not as a tradeable edge.
- **Crypto shorts underperforming this week** (PF 0.5, n=12) despite the regime nominally favoring them — a small sample, but worth tracking before leaning harder into short-side conviction.
- **XOM lifecycle inconsistency** (unmapped `tp2_hit` status) persists for a 5th+ consecutive review cycle — low blast radius but overdue for a manual audit (§14).
- **Very high internal macro-risk score** (98.4-100/100) — among the highest reads seen in recent cycles; size and conviction should stay reduced into the Europe session.

## 11. Action Plan — next 4 hours (overnight into Europe)

1. **Manage the open BANK/USDT short** — do not add; price drifting favorably (-8.6% 24h) but still dormant by the realistic model; respect the 0.19683 stop.
2. **Manage the open ACH/USDT long** — do not add; it is still OPEN (not closed) with a +0.5R lock armed despite the touch-based `tp2_hit` status; do not chase further extension.
3. **Manage the open DEXE/USDT short to its 02:45 UTC expiry** — do not extend or repeat this setup; flag the fill itself for manual review given the gating-bypass origin.
4. **Escalate the crypto-scalp kill-switch bypass (§14)** — the mode-level disable is not being honored by the watchlist-monitor promotion path; this needs a human-driven fix, not just a display note.
5. **Watch HYPE/USDT for the whale-flow-vs-narrative contradiction to resolve** — not actionable either direction until it does.
6. **Monitor the Iran/Iraq/Jordan conflict** into the Europe session for further escalation or de-escalation.
7. **Flag the XOM unmapped `tp2_hit` anomaly** for a manual lifecycle audit (5th+ consecutive cycle, see §14).
8. Continue all scanning/monitoring — no pause recommended in any mood.

## 12. Final Verdict per Mode

- **Crypto scalp**: KILL-SWITCHED / data-collection only per config, BUT a confirmed gating bypass let one live position (DEXE/USDT) through this cycle — treat scalp as fully paused for new ideas pending a manual fix (§14); net-negative bucket (PF 0.20 this week) unchanged.
- **Crypto intraday**: NO-ENTRY this cycle (the only intraday idea, DEXE, resolved `stale_before_entry`) — WATCHLIST ONLY.
- **Crypto swing**: ENTERED/OPEN on BANK/USDT (manage, don't add) and ACH/USDT (manage, don't add — touched TP2 but still open under the realistic model); KAITO/USDT's waiting order resolved `entry_moved_away` — no replacement long-watch yet.
- **Stocks intraday**: MARKET CLOSED overnight — all fresh C-tier ideas from the 01:11 UTC scan are `waiting_for_entry`/`missed_no_entry`; nothing actionable until European/US hours.
- **Stocks swing/invest**: deprecated/removed, not evaluated (new `stocks_swing_growth_breakout` remains shadow-only research, not actionable).

## 13. Sources

- [DEXE Price Analysis: Why DEXE Crashed Over 90% in One Month Amid FUD-Driven Selling](https://www.kucoin.com/blog/dexe-price-analysis-why-dexe-crashed-over-90-percent-in-one-month) — KuCoin, verified crash magnitude/cause (FUD-driven selling, thin liquidity, no confirmed exploit)
- [DeXe (DEXE) Price: DEXE/USD Live Price Chart, Market Cap & News Today](https://www.coingecko.com/en/coins/dexe) — CoinGecko, verified via WebFetch: current price ~$2.73, -5.3% 24h, $6M project-wallet-to-Binance transfer preceding the 85% crash
- [Crypto Price Prediction for July 30: Will Bitcoin, Ethereum and XRP Extend Their Recovery After the Fed?](https://sundayguardianlive.com/business/crypto-price-prediction-for-july-30-will-bitcoin-ethereum-and-xrp-extend-their-recovery-after-the-fed-check-btc-eth-and-xrp-forecast-key-level-and-market-outlook-248979/) — BTC/ETH July 30 range outlook ($63K-$66K)
- [Bitcoin and ethereum prices today, Wednesday, July 29, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-july-29-2026-crypto-investors-watching-the-fed-decision-closely-131641825.html) — Yahoo Finance, BTC ~$63.8K, ETH ~$1.9K spot cross-check
- [Jordan intercepts Iranian missiles as US and Saudi Arabia launch strikes against militias in Iraq](https://www.washingtonpost.com/world/2026/07/29/iran-war-us-hormuz-strait-july-29-2026/2ae527d4-8b0c-11f1-8912-d71e69d679d7_story.html) — Washington Post, conflict-status confirmation, no de-escalation
- Internal: `data/reports/scalp/2026-07-30_00-37_scalp_report.md`, `intraday/2026-07-30_00-44_intraday_report.md`, `swing/2026-07-30_01-36_swing_report.md`, `stocks/intraday/2026-07-30_01-12_stocks_intraday_report.md` — regime, scores, gate reasons, funding, DEXE kill-switch demotion evidence
- Internal: `data/catalysts/2026-07-30/catalyst_events.jsonl`, `narrative_baskets.jsonl` — catalyst coverage math, baskets, HYPE contradiction source
- Internal: `reports/PAPER_MONITOR_STATUS_LATEST.md` — lifecycle counts (cross-checked against live DB for staleness), XOM anomaly
- Internal: `db/crypto_ai_desk.sqlite` `proposed_signals` / `paper_execution_outcomes` / `watchlist_alerts` (direct SQL, live, this run) — DEXE gating-bypass evidence, ACH touch-vs-realistic distinction
- Internal: `active-signals`/`signal-stats` CLI (live, this run)

## 14. Fix Requests / TODO

### TODO-crypto-scalp-killswitch-bypass-watchlist-monitor (NEW, high priority)
- **issue:** The mode-level kill-switch `crypto_scalp_disabled (kill-switch: mode off, any hour/day)` is enforced in the batch scalp-scan report (which correctly demoted DEXE/USDT to C-tier at 00:37 UTC) but is **not** enforced in the `watchlist-monitor` fast-rescan promotion path. Eight minutes later (00:45:09 UTC), the same symbol was promoted from `previous_tier='rejected'` directly to `new_tier='B'` and created a live, triggered `proposed_signal` (`sig_6bd41cf0585d5c9c`, scalp mode) — a real paper position now sits open in a mode the desk explicitly disabled for being the worst-performing bucket this week (signal-stats: scalp PF 0.20, avgR -0.25, n=20, weak confidence).
- **evidence:** `db/crypto_ai_desk.sqlite` `watchlist_alerts` id=1987 (`previous_tier='rejected'`, `new_tier='B'`, `sent_at='2026-07-30T00:45:10+00:00'`, linked `signal_id='sig_6bd41cf0585d5c9c'`); `proposed_signals.report_id='watchlist-monitor-20260730-004509'` for the same signal; contrast with `data/reports/scalp/2026-07-30_00-37_scalp_report.md` line 168, which shows DEXE/USDT scored 68.2 (short) but explicitly gated to C for `crypto_scalp_disabled` 8 minutes earlier.
- **suggested manual fix:** locate the watchlist-monitor's promotion/scoring code path (separate from the batch scalp-scan gating logic) and confirm whether it checks the same mode-disable config flags before writing a new `proposed_signal`/`watchlist_alerts` row; add the missing check if absent, or determine if this was an intentional design gap (e.g., watchlist-monitor is meant to bypass mode kill-switches for research purposes) and if so, ensure it cannot reach `triggered`/paper-execution status while the mode is disabled.
- **priority:** high (real paper capital exposed in a mode explicitly disabled for being net-negative; a live-cost integrity issue, not display-only).
- **first observed:** 2026-07-30 04:47 EEST (this review).

### TODO-ach-touch-vs-realistic-status-display (NEW, medium priority)
- **issue:** `active-signals`/`proposed_signals.status` displays `tp2_hit` for ACH/USDT (`sig_c82d648fe9180aca`), which reads as a closed win at a glance, but the realistic `paper_execution_outcomes` row shows `lifecycle_state='OPEN'`, `paper_execution_r=None`, `paper_execution_outcome='open'` — the position is genuinely still open with a +0.5R lock, not resolved. This is the exact touch-vs-realistic distinction flagged in [[project_crypto_ai_desk_touch_based_pnl]], now observed live in the CLI/status surface an operator would check first.
- **evidence:** `db/crypto_ai_desk.sqlite` `proposed_signals` row `sig_c82d648fe9180aca` (`status='tp2_hit'`) vs `paper_execution_outcomes` row for the same `signal_id` (`lifecycle_state='OPEN'`, `touch_r=2.5`, `paper_execution_r=None`, `lock_armed=1`, `lock_level_r=0.5`).
- **suggested manual fix:** consider whether `active-signals`/`signal-stats` CLI output (or the paper-monitor display layer) should surface the realistic `lifecycle_state` alongside or instead of the touch-based `status` field for open positions under the `early_mfe_protection_v1` model, to avoid an operator misreading `tp2_hit` as "closed win" at a glance.
- **priority:** medium (no live-cost impact yet, but a real risk of operator misreading a genuinely-open position as closed).
- **first observed:** 2026-07-30 04:47 EEST (this review).

### TODO-xom-unmapped-tp2-hit-status-recurring (carried forward, unresolved, 5th+ cycle)
- **issue:** An XOM stocks/intraday/B-tier row continues to display `STATUS NEEDS REVIEW — inconsistent lifecycle fields · unmapped status 'tp2_hit'` in the paper-monitor status output. Flagged in the 15:59, 18:39, 21:46, and 23:15 EEST (07-29) reviews — now a 5th+ consecutive cycle without resolution.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` line 165: `XOM long (stocks/intraday/B) — STATUS NEEDS REVIEW — inconsistent lifecycle fields · unmapped status 'tp2_hit'`.
- **suggested manual fix:** locate the lifecycle-status mapping table for stocks/intraday and add/confirm a mapping for `tp2_hit`, or determine whether this specific row's `tp2_hit` value is itself a data-entry error that should be corrected/backfilled to a mapped status.
- **priority:** medium (low blast radius — single row, display-only — but recurring across 5+ cycles warrants closing it out).
- **first observed:** carried forward from at least 2026-07-29 15:59 EEST; still present at 2026-07-30 04:47 EEST.
