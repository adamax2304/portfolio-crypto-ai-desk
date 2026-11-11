# Opus Enriched Review — late-session risk review — Auto Cycle 21:45 EEST

## 1. Executive Summary

Slot: **late-session risk review** (target 21:30 EEST / ~14:30 ET, actual data pull 21:39-21:45 EEST — within tolerance, ~75-80min left in the US cash session before the 23:00 EEST close). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** External web research was available and used this run. The US large-cap rally (S&P +0.88%, Nasdaq +1.6%, Dow +0.53% on MSFT's +15% cloud-earnings surge) vs. Russell 2000/IWM -1.61% divergence flagged at 18:38 EEST is confirmed still intact into the late session (external re-check, no fresher intraday print found beyond the same day-level figures). Crypto stays selective: BTC/ETH modestly firm post-Fed-hold, no A/B-tier setups fired this cycle across scalp (kill-switched), intraday, or swing. **BANK/USDT (Lorenzo Protocol) continues deteriorating** — external verification confirms a -56.3% 7d decline consistent with the internal read, and the internal score worsened from -55.0%/24h at 18:35 to -58.45%/24h at 19:50 — still an ongoing capitulation/unwind, not a fresh short entry; OI +80.6% with negative funding flags real squeeze risk on any short chased here. **ONDO/USDT** remains the cleanest long-watch: price (0.4127) sits just ~0.4% above its 0.4078-0.4112 pullback entry zone, backed by a canonical catalyst (importance 0.95) and a "hot" RWA narrative basket — closest thing to an actionable long this cycle, still gated at waiting_for_entry. A genuine data-freshness gap surfaced this cycle: `PAPER_MONITOR_STATUS_LATEST.md` (19:54 EEST, ~1h50m stale) shows an **EPIC/USDT (crypto/intraday/B) OPEN position — entry filled, monitoring TP/SL**, but the live `active-signals` query (run now, 21:39 EEST) shows **no EPIC/USDT row at all** in either mode — most likely both EPIC signals (intraday-open and swing-waiting) resolved in the intervening ~1h50m, but this cannot be confirmed without fabricating an outcome, so it is logged as a data-lag note (TODO-11), not asserted either way. Tonight's mega-cap earnings cluster (AAPL, AMZN, COIN, MSTR — all reporting after the 23:00 EEST close) remains the dominant event risk for the next 4 hours; do not chase any of the four into the print. PLTR (sec_doj) and META (indictment) legal-flag false-positive TODOs (TODO-1/TODO-2) remain open and unchanged for a third consecutive cycle. Catalyst mapping stays weak (70.8% unmapped). Scanning, tracking, and monitors continue in every mood; this review recommends selective caution into the close, never a stop.

## 2. Data Used

| File / Source | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-30_15-26_scalp_report.md` | 18:26:00 EEST | ~3h19m — fresh (scalp regen cadence is coarser; no fresher file exists this cycle) |
| `data/reports/intraday/2026-07-30_15-35_intraday_report.md` | 18:35:37 EEST | ~3h10m — carry-forward within tolerance, no fresher intraday report generated this cycle |
| `data/reports/swing/2026-07-30_16-50_swing_report.md` | 19:50:xx EEST | ~1h55m — fresh, freshest crypto source this cycle |
| `data/reports/stocks/intraday/2026-07-30_18-35_stocks_intraday_report.md` | 21:35:xx EEST | ~10min — fresh, essentially live RTH snapshot |
| `data/reports/stocks/swing/…` / `invest/…` (2026-07-02) | stale (>14h, in fact ~4 weeks) | deprecated/removed playbooks, see [[project_crypto_ai_desk_stocks_position_framework]] — excluded from final verdict, not a freshness failure |
| `data/catalysts/2026-07-30/catalyst_events.jsonl` (3000 rows) + `narrative_baskets.jsonl` (3 baskets) | 18:45:01 EEST | ~1h — fresh, unchanged since last cycle's refresh |
| `data/processed/llm_analysis_packet.md` (crypto) | 19:51 EEST | ~1h54m — fresh |
| `data/processed/llm_stocks_packet.md` | 19:10 EEST | ~2h35m — stale relative to the 21:35 stocks report; read the fresher raw report directly instead (TODO-8, recurring) |
| `reports/PAPER_MONITOR_STATUS_LATEST.md` | 19:54 EEST | ~1h50m — used with a freshness caveat, cross-checked against live `active-signals` (see §1 EPIC discrepancy, TODO-11) |
| `python -m src.cli active-signals --asset-class crypto` / `stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` / `stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-30` | live query | now — none found |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-30_1838.md` (US open reaction slot) | 18:55 EEST | for §4 diff |
| WebSearch: US stock market today close-of-day figures, Lorenzo Protocol BANK crash, BTC/ETH price today | live | now |

**External web research was available and used this run.**

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-07-30_default_schedule/scheduler.log` mtime 19:57 EEST (fresh, ~1h48m old at pull time). Latest `cycle_02_18-14_summary.md` mtime 19:57 EEST (~1h48m old) — well within the 3h non-deferral window.
- Crypto scalp/intraday reports are carry-forward from the 18:26/18:35 cycle (no fresher regeneration yet this cycle) — both still inside the <4h fresh bucket, no material regime change found via the fresher swing report or live signal-stats.
- Crypto swing report (19:50 EEST, ~1h55m old) is the freshest crypto source and shows BANK/USDT deteriorating further (-55.0%→-58.45% 24h) versus the 18:35 intraday snapshot.
- Stocks-intraday report regenerated at 21:35 EEST (~10min old) — captures the live late-session tape.
- Catalyst JSONL unchanged since the 18:45 EEST refresh: **3000** unique events today, **876 mapped (29.2%)**, **2124 unmapped (70.8%)** — weak-mapping threshold breached again (TODO-5, recurring, flat vs the 18:38 review).
- `detect_untracked_legacy_alerts --since 2026-07-30`: **None** — every legacy crypto alert has a backing proposed_signal.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (19:54 EEST, ~1h50m old): OPEN_ACTIVE=1, WAITING_FOR_ENTRY=5, REVIEW_ONLY_SHADOW=36, ENTERED_UNRESOLVED_EXPIRED=2, NO_ENTRY_EXPIRED=58, CLOSED_WIN=148, CLOSED_LOSS=15, CLOSED_FLAT=13, UNKNOWN_INCONSISTENT=5.
  - OPEN_ACTIVE=1 = **EPIC/USDT long (crypto/intraday/B)** — "entry filled, monitoring TP/SL." WAITING_FOR_ENTRY=5 = the 5 crypto/swing/B longs (ONDO, ESP, EPIC, ADA, AERO).
  - **Cross-check against live `active-signals --asset-class crypto` (run now, 21:39 EEST): no EPIC/USDT row at all**, in either intraday or swing mode. The 22 live crypto signals are: ONDO/ESP/ADA/AERO (swing, `waiting_for_entry`, expire 2026-08-06) plus 18 `tp1_hit`/`tp2_hit` legacy-touch rows (DEXE, ACH, ZEC, ONDO, OPN, FIL, ONDO, KITE, ZAMA×3, ADA, VIRTUAL, PENGU, PUMP, KAITO, ALLO, NEAR), several carrying `expires_at` dates already weeks in the past (stale-expiry display artifact, recurring, not a new issue this cycle).
  - Most likely explanation: both EPIC/USDT signals resolved (closed win/loss/flat) sometime in the ~1h50m between the 19:54 monitor snapshot and this 21:39 query — a normal lifecycle progression for a short-duration intraday signal. This cannot be confirmed without re-running the monitor-status generator, which is outside this run's allowed CLI list, so **no outcome is asserted** (see TODO-11).
  - Recurring UNKNOWN_INCONSISTENT bucket (5 items: MSTR/PLTR long+short labelled-loss-but-final_r>0, same pattern as at least 4 prior reviews) — not independently re-verified line-by-line this cycle (TODO-3/TODO-4, unchanged).
- Zero A/B-tier ideas this cycle across scalp, intraday, swing, and stocks-intraday — confirmed directly from `data/reports/**` §5/§6 "No A/B-tier actionable setups in this run" / "actionable" B-tier swing ideas exist (ONDO/ESP/EPIC/ADA/AERO) but all remain `waiting_for_entry`, none newly triggered this cycle.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-30 21:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.78,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["llm_stocks_packet.md ~2h35m stale vs the fresher 21:35 stocks report (read directly instead)", "PAPER_MONITOR_STATUS_LATEST.md ~1h50m old, used with caveat, EPIC/USDT discrepancy vs live active-signals not resolvable this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 19:57 EEST fresh (~1h48m old)", "crypto scalp/intraday carry-forward from 18:26/18:35 (inside fresh bucket)", "crypto swing 19:50 EEST freshest crypto source", "stocks-intraday regenerated 21:35 EEST, ~10min old", "catalyst JSONL unchanged since 18:45 EEST refresh: 3000 rows, 876 mapped/2124 unmapped", "detect_untracked_legacy_alerts: none"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.65,
      "reason_codes": ["mixed", "longs_preferred", "chop"],
      "data_missing": ["no intraday-granularity late-session print found beyond the same day-level external figures used at 18:38"],
      "suggested_effect": "advisory_only",
      "facts_used": ["External: S&P +0.88%, Nasdaq +1.6%, Dow +0.53% (MSFT +15%), Russell 2000/IWM -1.61% — divergence confirmed still standing into late session", "Internal crypto swing regime: bullish trend / transition_up (BTC), uptrend (ETH), altcoin breadth 62.8% above EMA20, 'selective longs; prefer pullbacks on RS'", "Internal crypto intraday regime (carry-forward): range/chop (neutral), altcoin breadth 41.9% above EMA20", "Internal stocks regime: risk_off/short bias, breadth 25% above EMA20, VIX 17.95", "Macro/geopolitics risk score 100/100 per swing report (7 risk-off hits) — a headline-risk flag, not necessarily reflected in today's actual price action"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 3000 rows, 876 mapped (29.2%), 2124 unmapped (70.8%) — weak-mapping threshold breached, unchanged since 18:45 EEST refresh", "binance_ecosystem_teaser basket (BNB/USDT, ASTER/USDT) still mislabeled per the 18:38 review's verified finding (BNB Plus/BNBX governance crisis, not a bullish Binance-protocol event) — carried forward, basket not regenerated since", "momentum_breakout basket (EPIC/USDT, GIGGLE/USDT) explicitly 'no confirmed news catalyst'", "ONDO/USDT carries a genuine canonical catalyst, importance 0.95, plus a 'hot' RWA narrative basket (heat 74.4/100)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "unwind", "data_unavailable"],
      "data_missing": ["OI change unavailable ('n/a') for several symbols this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT: OI +80.59% 24h (fresh shorts pressing) with external funding still negative (bybit -0.0075, mexc -0.0022) and crowding 'elevated' — real squeeze risk if price reclaims, against an already -58.45% day", "ONDO/USDT: price up + OI up (+10.1%), funding near-zero, crowding normal — fresh positioning confirms the trend, no crowding red flag", "EPIC/USDT (swing): price up + OI down (-3.83%) — short covering, weaker continuation quality, a caution flag on the long thesis independent of the entry-zone question"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["entry_late", "clean_retest", "chase_risk", "price_moved_away"],
      "data_missing": ["TradingView / manual chart check unavailable this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONDO/USDT: current price 0.4127 vs entry zone 0.4078-0.4112 — only ~0.4% above, the tightest 'near actionable' gap of any candidate this cycle, RR to TP1 1.84", "EPIC/USDT (swing): current price 0.8782 vs entry zone 0.8372-0.8656 — still meaningfully extended (~1.4-4.9% above zone), same chase-risk read as the 18:38 review, unresolved", "BANK/USDT: -58.45% 24h, tags weak_vs_market/breakdown/overextended — a short here chases an already-extreme, still-deepening move", "Stocks: every raw A/B candidate this cycle demoted by a mix of market_context_conflict, sector_confirmation_weak/conflict, liquidity_rvol_below_min, legal/headline flags, or rr_below_min_required — NVDA short is the cleanest technical gate (rr_to_tp1=1.29 vs 1.50 required, no context conflict)"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.68,
      "reason_codes": ["waiting_for_entry", "needs_review", "no_entry", "review_shadow"],
      "data_missing": ["EPIC/USDT (crypto/intraday/B) open-position outcome cannot be confirmed this cycle — see TODO-11"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto: 4 confirmed live waiting_for_entry swing/B longs (ONDO, ESP, ADA, AERO), 18 tp1_hit/tp2_hit legacy-touch rows tracking remaining ladder/stop, several with already-passed expires_at (display artifact)", "Stocks: 50 non-terminal legacy rows; today's fresh C-tier entries (JPM, XLF, UNH, MSTR waiting; AAPL, NFLX triggered/waiting) all C-tier, never actionable by design", "PAPER_MONITOR_STATUS_LATEST.md (1h50m stale): OPEN_ACTIVE=1 (EPIC/USDT intraday), WAITING=5, UNKNOWN_INCONSISTENT=5 (recurring) — EPIC/USDT absent from the live active-signals re-query, logged as a data-lag note, not an asserted outcome"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.72,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["cannot re-confirm PLTR sec_doj / META indictment flags beyond the 11:45/16:06/18:38 reviews' research passes this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["AAPL, AMZN, COIN, MSTR report earnings tonight after the 23:00 EEST close — do_not_chase_warning + block_requires_operator_review active on all four (plus MA per the production-risk-warnings block)", "XOM reports tomorrow (2026-07-31) — same warning class", "PLTR still carries legal_headline_risk 'sec_doj' (C-tier, unresolved TODO-1); META still carries 'indictment' (C-tier, unresolved TODO-2); GOOGL now also carries 'class_action' this cycle (new gate reason, not yet independently verified as false-positive or genuine — logged for a future cycle to check)", "BANK/USDT: no fresh catalyst tied to today's continued decline found in the internal feed — treat as pure technical unwind continuation, not a headline-driven event risk"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto B-tier weekly headline: n=81, winrate 27.0%, PF 1.88, avgR +0.306, totalR +15.9 — healthy on R despite low winrate; intraday mode strongest (PF 3.40, avgR +0.92, n=29), swing solid (PF 1.77, avgR +0.27, n=35), scalp still losing (PF 0.25, avgR -0.23, n=17, correctly kill-switched)", "Crypto shorts weak this week: n=14, PF 0.33, totalR -2.0 vs longs n=67, PF 2.19, totalR +17.9 — favor longs over shorts in the current window, consistent with routing BANK/USDT away from a fresh short", "Stocks A/B headline: n=2 anecdotal, PF 0.0, totalR -1.0 — not enough sample either way", "Stocks C-tier watchlist: n=185, winrate 5.9%, PF 0.11, totalR -8.0 — badly losing, consistent with C-tier being correctly non-actionable by design"] },
    { "agent": "head_trader", "verdict": "advisory_only",
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of the eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.62,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "ONDO/USDT", "trigger": "pullback fill into 0.4078-0.4112 (currently 0.4127, only ~0.4% above zone); invalidation 1h close beyond 0.4037", "reason": "closest-to-actionable setup this cycle: canonical catalyst (importance 0.95), 'hot' RWA narrative basket, fresh OI confirming the trend, RR to TP1 1.84 — crypto's clearest expression of the week's long-favoring playbook stats" },
    "best_short_candidate":    { "symbol": "NVDA", "trigger": "wait for RR to TP1 to clear 1.50 (currently 1.29) — either a slightly better short entry or a widened TP1 target; no market_context/sector conflict unlike XLV/LLY", "reason": "the only stocks short this cycle gated purely on RR math rather than a context or legal conflict, making it the cleanest technical short-watch, though still not actionable without a better level" },
    "best_catalyst_candidate": { "symbol": "none clean — BNB/USDT basket remains mislabeled", "trigger": "would need a genuine Binance-protocol-level catalyst (not the BNB Plus/BNBX treasury-shell governance story) plus a non-extended entry", "reason": "unchanged from the 18:38 review; basket not regenerated since 18:45 EEST" },
    "avoid_candidate":         { "symbol": "BANK/USDT (Lorenzo Protocol) — either side", "reason": "an already -58.45% day (worse than the -55.0% seen at 18:35) with OI +80.6% and elevated external crowding/negative funding — chasing a short here risks a squeeze on a still-deepening capitulation, and there is no basing/reversal structure yet for a long" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 6
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.78 | scheduler_fresh, report_stale | advisory_only |
| market_regime | mixed | 0.65 | mixed, longs_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, unwind, data_unavailable | advisory_only |
| technical_entry | caution | 0.62 | entry_late, clean_retest, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.68 | waiting_for_entry, needs_review, no_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.72 | headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.68 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | watch_only | 0.62 | — | advisory_only |

## 4. What Changed vs Previous Review (18:38 EEST, US open reaction)

- **IWM short-watch (18:38 pick) evaporated**: the fresh 21:35 stocks report no longer even lists IWM among Top Candidates — it now sits in Rejected/Not Ready as `no_trade / no_directional_setup` (score 41.39). Dropped from this cycle's watch list; replaced by NVDA (rr_below_min_required, cleanest remaining technical short-gate).
- **BANK/USDT deteriorated further**: -55.0% 24h at 18:35 → -58.45% at 19:50 — the capitulation/unwind flagged at 18:38 as "avoid, already extreme" is still going, confirming that call rather than reversing it.
- **EPIC/USDT status changed materially but ambiguously**: at 18:38 EEST EPIC was watchlist-only (chase risk, price through the pullback zone). By 19:54 EEST the paper-monitor snapshot showed an EPIC/USDT intraday-mode position OPEN (entry filled). By 21:39 EEST (this review's live query) neither the intraday nor swing EPIC signal appears in `active-signals` at all — logged as a data-lag/reconciliation note (TODO-11), not an asserted win/loss.
- **ONDO/USDT priced closer to its pullback zone**: price 0.4127 vs entry zone 0.4078-0.4112 — a tight ~0.4% gap, the closest-to-actionable long this cycle; still `waiting_for_entry`, unchanged tier/thesis from earlier cycles.
- **GOOGL now also carries a `class_action` legal-headline-risk gate** in the 21:35 stocks report — not seen as a distinct TODO in the 18:38 review; not yet independently verified as a false positive (unlike PLTR/META) — flagged for the next cycle's research pass rather than asserted either way this cycle.
- **TODO-1 (PLTR sec_doj) and TODO-2 (META indictment)**: still open, unchanged, re-confirmed present in the fresh 21:35 stocks report for a third consecutive cycle.
- **Catalyst mapping**: 70.8% unmapped, identical to 18:38 (catalyst JSONL not regenerated since 18:45 EEST) — TODO-5 recurring, not worsening but not improving.
- **Earnings cluster unchanged**: AAPL, AMZN, COIN, MSTR still pending after tonight's 23:00 EEST close (MA carries the same warning class per the production-risk-warnings block); META's ~10% post-earnings drop this morning remains the live proof-point that this is a genuinely dispersive, earnings-driven tape.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **3000** (unchanged since the 18:45 EEST refresh — no newer catalyst-scan cycle ran between reviews). Mapped (non-null symbol): **876 (29.2%)**. Unmapped: **2124 (70.8%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets today (unchanged since 18:45 EEST):
  - **binance_ecosystem_teaser** (primary BNB/USDT, related ASTER/USDT) — still mislabeled per the 18:38 review's verified finding (BNB Plus/BNBX governance crisis at a small Nasdaq-delisted treasury shell, not a bullish Binance-protocol event). Treat as caution/noise, not a catalyst-backed long.
  - **momentum_breakout** (EPIC/USDT, GIGGLE/USDT) — explicitly "top gainers without confirmed news catalyst — pure momentum cluster."
  - **delisting_thin_liquidity** — no specific symbols, generic "avoid chasing low-float dumps" note.
- Top unmapped-illustrative items (from a fresh scan of the raw JSONL): earnings-report boilerplate (e.g. California Water Service Group Q2 results), crypto Telegram/AMA promo posts (emoji-heavy, no resolvable ticker), and macro/policy wire copy (CLARITY Act Senate letter, Fed Chair rate-hold remarks) — none tradable as-is.

## 6. Market Landscape

The late-session picture is a continuation of the 18:38 review's narrow, earnings-driven divergence: US large-caps remain up hard on MSFT's single-name +15% cloud-earnings beat while the Russell 2000/IWM stays down -1.61%, and internal stocks scoring still reads risk_off/short-biased on the medium-term trend (breadth 25% above EMA20, VIX 17.95) even as the day's headline indices are green. No fresher intraday-granularity print was found beyond the same day-level figures used earlier, so this divergence is carried forward rather than independently re-verified tick-by-tick. Crypto is modestly more constructive at the swing horizon than the intraday one: the swing report reads a genuine bullish-trend regime (BTC transition_up, ETH uptrend, altcoin breadth 62.8% above EMA20, "selective longs; prefer pullbacks on RS"), while the carried-forward intraday report still reads range/chop — read this as "the crypto tape firmed somewhat over the last ~2h without a fresh intraday scan confirming it directly." The single most decision-relevant symbol-level fact this cycle is BANK/USDT's continued unwind (-55.0%→-58.45% 24h between the 18:35 and 19:50 reports) with OI up +80.6% and negative external funding — a live squeeze-risk warning against chasing a short into an already-extreme move. ONDO/USDT is the cleanest long-side setup, sitting just ~0.4% above its pullback entry zone with a genuine catalyst and a hot RWA narrative behind it. Tonight's AAPL/AMZN/COIN/MSTR earnings cluster (after the 23:00 EEST close) remains the dominant event risk for the next 4 hours, following META's ~10% drop this morning on the same reporting cycle.

### Market Mood / Risk Routing
- Crypto mood: **mixed / selective, mildly firmer at swing horizon** (BTC transition_up, ETH uptrend at swing; range/chop at carried-forward intraday; no fresh A/B setups this cycle)
- Stocks mood: **mixed / narrow** (large-cap indices still up on MSFT's single-name beat, small-caps still diverging down; internal medium-term regime risk_off/short-biased; zero A/B actionable this cycle)
- Dominant narrative: the same MSFT-driven large-cap/small-cap split from the US-open review persists into the late session; tonight's AAPL/AMZN/COIN/MSTR earnings after the close is the next catalyst that will move the tape
- Preferred side now: **longs, selectively, wait-for-fill on the pullback zone** — crypto favors longs this week on the playbook stats (short PF 0.33 vs long PF 2.19); stocks remain wait-for-trigger/RTH-confirmation with no clean side
- Best long candidate: ONDO/USDT — fill into 0.4078-0.4112 (currently 0.4127, ~0.4% above), invalidation 0.4037
- Best short candidate: NVDA — wait for RR to TP1 to clear 1.50 (currently 1.29); cleanest technical-only gate among stocks shorts (no context/legal conflict)
- Best catalyst-backed candidate: none clean — BNB/USDT basket remains mislabeled, unchanged since 18:45 EEST
- What to avoid: BANK/USDT (either side, still-deepening capitulation with squeeze risk); chasing AAPL/AMZN/COIN/MSTR ahead of tonight's prints; treating BNB/USDT as a clean catalyst long
- What would change the view: ONDO/USDT filling and holding the pullback zone; NVDA's RR clearing 1.50 on a cleaner entry; tonight's earnings reactions, which set the tone for the 23:15 EEST post-close review and tomorrow's 04:30 EEST Asia-session read

## 7. Candidate Deep Dives

### 1. ONDO/USDT — crypto swing, B-tier, long — best long-watch
- Internal setup: `waiting_for_entry`, entry 0.4078-0.4112, invalidation 1h close beyond 0.4037, TP1 0.4202/TP2 0.4278/TP3 0.4353, RR to TP1 1.84.
- Has price already reacted to the catalyst? Partially — 24h +4.83%, 7d +1.85%, RS vs BTC +3.28% — a moderate move, not a vertical spike.
- Is the setup chasing? No — current price 0.4127 is only ~0.4% above the top of the entry zone, the tightest gap of any candidate this cycle.
- Retest/pullback structure? The desk's plan requires a pullback into 0.4078-0.4112; not yet filled but close.
- Overextended? No — setup quality 65.9/100, no overextension tag.
- Would entry now be late? Borderline-no; a small further dip would fill the zone cleanly.
- Aligned with market mood? Yes — crypto swing regime is genuinely bullish-trend this cycle, and longs are outperforming shorts on the week's playbook stats.
- Actionable now or after confirmation? After the pullback fills — not actionable yet by policy (waiting_for_entry).
- Invalidation: 1h close beyond 0.4037.
- Chase-risk setup? No.
- Catalyst confirmation/contradiction? Confirmed — canonical_news_event, importance 0.95, plus RWA narrative basket "hot" (heat 74.4/100).

### 2. BANK/USDT (Lorenzo Protocol) — crypto, C-tier top mover, short bias — avoid, either side
- Internal setup: short bias, score rising 82.2→85.2 across the two most recent reports as the move deepens; tags `weak_vs_market`, `breakdown`, `overextended`; 24h move -55.0% (18:35) → -58.45% (19:50).
- External verification: confirmed -56.3% over the trailing 7d via WebSearch — consistent with an ongoing capitulation following the mid-July BTCFi/Aster-wallet-driven pump to an ATH near $0.295-0.53.
- Has price already reacted? Yes, extremely, and still actively reacting — this is not a one-day event, it is a multi-day unwind that deepened again this cycle.
- Chasing? A fresh short here chases an already-extreme, still-moving target.
- Retest/pullback structure? None visible; capitulation-style price action continues.
- Overextended? Yes, to the downside.
- Aligned with mood? Directionally (weak_vs_market), but not a clean entry — the move is realized and ongoing, not a fresh setup.
- Actionable now or pending confirmation? Neither — avoid until a basing/reversal structure forms.
- Squeeze risk: OI +80.59% 24h (fresh shorts pressing) with external funding still negative and crowding "elevated" — a real risk that a short entered here gets caught in a violent relief-bounce squeeze if shorts get crowded further.
- Catalyst confirmation/contradiction? No fresh catalyst found tied to today's specific continued decline — treat as pure technical unwind continuation.

### 3. BNB/USDT — crypto, catalyst basket primary, still demoted to caution
- Internal setup: `binance_ecosystem_teaser` basket, primary BNB/USDT, related ASTER/USDT — unchanged since the 18:38 review's external verification (BNB Plus/BNBX governance crisis at a small, unrelated Nasdaq-delisted treasury shell, not a bullish Binance-protocol event).
- Has price already reacted? BNB/USDT does not appear among today's strongest or weakest movers in either the 18:35 intraday or 19:50 swing report — no visible reaction either way, consistent with the mislabeling finding (the market is not treating this as a real BNB catalyst).
- Actionable now or pending confirmation? Neither — demoted from catalyst-watch to caution/skip, carried forward unchanged (see TODO-9).

### 4. EPIC/USDT — crypto, dual-mode lifecycle discrepancy — needs review, not a fresh entry either way
- Swing mode: `waiting_for_entry`, entry 0.8372-0.8656, current price 0.8782 (19:50 EEST) — still ~1.5-4.9% above the zone, unchanged chase-risk read from the 18:38 review.
- Intraday mode: the 19:54 EEST `PAPER_MONITOR_STATUS_LATEST.md` snapshot showed this signal as OPEN ("entry filled, monitoring TP/SL"), but the live `active-signals --asset-class crypto` query at 21:39 EEST shows no EPIC/USDT row in any mode.
- Most likely explanation: the intraday-mode position (and possibly the swing one) resolved — closed win, loss, or flat — in the ~1h45-50m gap between the two reads. This is a normal lifecycle outcome for a short-duration intraday signal, not inherently a bug.
- No outcome is asserted here per the source-discipline rule — never fabricate a result. Flagged as TODO-11 for a human session to check the actual closed-trade record (`signal_outcomes` table) if the true R matters for tonight's book.
- Actionable now or pending confirmation? Not for a new entry either way — the swing leg is still extended/chase-risk, and the intraday leg's status cannot be confirmed live this cycle.

### 5. Mega-cap earnings cluster (AAPL, AMZN, COIN, MSTR) — stocks, earnings after tonight's close — avoid chasing into the print
- Internal setup: all four (plus MA, per the production-risk-warnings block) carry `do_not_chase_warning` + `block_requires_operator_review` for earnings today (2026-07-30, reporting after the close).
- External verification: META already reported this morning and fell ~10% on a disappointing revenue forecast on the same broad reporting cycle that saw MSFT surge +15% — the dispersion thesis flagged at 18:38 remains the operative read into tonight's prints.
- Has price already reacted? Only for META/MSFT so far; AAPL/AMZN/COIN/MSTR reactions are still pending as of this review (23:00 EEST close is ~75-80min away).
- Chasing? Any directional position on these four ahead of tonight's numbers is a pure earnings gamble.
- Actionable now or pending confirmation? Pending — do not position ahead of the print; re-evaluate specifically at the 23:15 EEST post-close review once reactions are known.
- Catalyst confirmation/contradiction? N/A — scheduled event risk, not a contradicted thesis.
- Related: PLTR (sec_doj, TODO-1) and META (indictment, TODO-2) legal-headline-risk flags remain open and unverified for a third consecutive cycle; GOOGL now also shows a `class_action` gate this cycle, not yet independently checked.

## 8. Best Candidates Ranked

1. **ONDO/USDT long-watch** — best long-watch, tightest gap to entry (~0.4%) of any candidate this cycle, catalyst + hot narrative confirmed.
2. **NVDA short-watch** — best short-watch, cleanest technical-only gate (RR 1.29 vs 1.50 required) among stocks shorts.
3. **EPIC/USDT** — needs-review; swing leg still extended/chase-risk, intraday leg's live status unresolved this cycle (TODO-11).
4. **BANK/USDT** — avoid either side; still-deepening capitulation, squeeze risk on a fresh short.
5. **AAPL/AMZN/COIN/MSTR earnings cluster** — avoid positioning ahead of tonight's prints; re-check at 23:15 EEST post-close.

## 9. Avoid / No Trade (this decision window only)

- **BANK/USDT, either side**: still-deepening capitulation (-58.45% 24h), OI +80.6% with negative funding/elevated crowding — squeeze risk on a short, no basing structure for a long.
- **AAPL, AMZN, COIN, MSTR, MA**: earnings after tonight's close — `do_not_chase_warning` + `block_requires_operator_review` active on all five.
- **BNB/USDT (binance_ecosystem_teaser basket)**: still mislabeled — do not treat as catalyst-backed.
- **PLTR, META, GOOGL**: carrying legal-headline-risk flags (sec_doj / indictment / class_action) — treat PLTR/META as manual-review per the standing TODO-1/TODO-2 false-positive suspicion; GOOGL's class_action flag is new this cycle and not yet independently checked, so treat as manual-review by default rather than a confirmed avoid.
- **EPIC/USDT (either mode)**: no new entry — swing leg extended/chase-risk, intraday leg's status unresolved (TODO-11).
- **Crypto scalp mode**: correctly disabled desk-wide (kill-switch), not a per-symbol avoid.
- This is a decision-window call only — scanning, tracking, and monitors continue in every mood; nothing here is a stop-the-system instruction.

## 10. Main Risks

- **Concentrated earnings-event risk tonight**: AAPL, AMZN, COIN, and MSTR all report after the 23:00 EEST close on the same broad cycle that already saw META drop ~10% this morning — expect elevated overnight/tomorrow-morning volatility; the 23:15 EEST post-close review should specifically re-assess these four.
- **BANK/USDT squeeze risk**: OI +80.6% with negative external funding and elevated crowding on an already -58.45% day — a short chased here risks a violent relief-bounce squeeze.
- **Data-lag risk (new this cycle, TODO-11)**: EPIC/USDT's dual-mode signal status could not be reconciled between the 19:54 EEST paper-monitor snapshot (OPEN) and the 21:39 EEST live active-signals query (absent) — flagged rather than guessed.
- **Recurring `UNKNOWN_INCONSISTENT` lifecycle-mapping bug (5 items)** persists across at least 5 consecutive reviews now (TODO-3/TODO-4) — not independently re-verified this cycle due to `PAPER_MONITOR_STATUS_LATEST.md` staleness.
- **Legal-flag reliability risk**: PLTR and META legal_headline_risk flags remain unresolved/unverified for a third consecutive cycle (TODO-1/TODO-2); GOOGL's new `class_action` flag this cycle is unverified either way.
- **Catalyst mapping stuck at ~70-72% unmapped** across at least 4 consecutive reviews (TODO-5) — read the catalyst layer as context, not a decision input, until this improves.
- **Concentration risk in the ongoing large-cap rally**: still driven almost entirely by MSFT's single-name move; a reversal in MSFT sentiment or a broad catch-down to small-cap weakness into the close is a live risk.

## 11. Action Plan — next 4 hours

- No new crypto or stocks entries this cycle — zero A/B ideas across scalp, intraday, swing, and stocks-intraday.
- Watch ONDO/USDT for a fill into 0.4078-0.4112; do not chase above the zone; invalidation 1h close beyond 0.4037.
- Watch NVDA for RR to TP1 to clear 1.50 before treating it as a clean short-watch.
- Do not short (or long) BANK/USDT fresh here — still-deepening capitulation with squeeze risk.
- Do not position in AAPL, AMZN, COIN, or MSTR ahead of tonight's close; re-assess specifically at the 23:15 EEST post-close review.
- Do not treat BNB/USDT as catalyst-backed; the basket thesis remains mislabeled.
- Continue managing existing crypto tp1_hit/tp2_hit positions per their own ladders/stops; no new management action indicated by this review.
- A human session should check the `signal_outcomes` table for EPIC/USDT's actual closed-trade result if tonight's book needs to reconcile against the paper-monitor snapshot (TODO-11).

## 12. Final Verdict per Mode

- **Crypto scalp**: disabled (kill-switch), no change.
- **Crypto intraday**: 0 A/B ideas this cycle (report carried forward from 18:35); EPIC/USDT's intraday-mode status unresolved this cycle (TODO-11).
- **Crypto swing**: 0 newly-triggered A/B ideas; 4 confirmed live waiting_for_entry longs (ONDO, ESP, ADA, AERO) — ONDO closest to filling.
- **Stocks intraday**: 0 A/B actionable this cycle — regime risk_off/short-biased on the medium-term trend inside a narrow large-cap rally; every raw A/B candidate gated by context/liquidity/legal/RR rules. NVDA is the cleanest remaining short-watch pending a better RR.
- **Stocks swing/invest**: deprecated/removed frameworks, no active signals this run (see [[project_crypto_ai_desk_stocks_position_framework]]).

## 13. Sources

- [Stock market today: Dow, S&P 500, Nasdaq rebound after Fed decision, as Microsoft leads tech gains, bond yields rise (Yahoo Finance)](https://finance.yahoo.com/markets/live/stock-market-today-thursday-july-30-dow-sp-500-nasdaq-treasury-yields-microsoft-082255995.html)
- [Stock Market Today (July 30, 2026): Dow rises as Microsoft surges, Fed holds rates steady (TheStreet)](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-july-30-2026)
- [Bitcoin and ethereum prices today, Thursday, July 30, 2026: Prices rise after Fed leaves rates unchanged (Yahoo Finance)](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-july-30-2026-prices-rise-after-fed-leaves-rates-unchanged-132340233.html)
- [Lorenzo Protocol (BANK) Rallies on BTCfi and Yield Trends (Tapbit)](https://www.tapbit.com/en/learn/article/lorenzo-protocol-bank-token-price-rally-july-2026-20260721)
- [Lorenzo Protocol's BANK Token Rockets 517% After a Mysterious Wallet Move (Startup Fortune)](https://startupfortune.com/lorenzo-protocols-bank-token-rockets-517-after-a-mysterious-wallet-move/)
- Internal: `data/reports/swing/2026-07-30_16-50_swing_report.md` (freshest crypto source, 19:50 EEST).
- Internal: `data/reports/stocks/intraday/2026-07-30_18-35_stocks_intraday_report.md` (generated 21:35 EEST).
- Internal: `reports/PAPER_MONITOR_STATUS_LATEST.md` (19:54 EEST) cross-checked against live `active-signals`.
- Internal: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-30_1838.md` (prior review, US open reaction slot) — used for §4 diff.

## 14. Fix Requests / TODO

### TODO-1: PLTR `legal_headline_risk: sec_doj` flag looks like a false positive from law-firm solicitation boilerplate
- **issue:** Still open, unresolved for a third consecutive review. PLTR remains demoted A→C citing "active legal/headline risk (sec_doj)" this cycle too (`data/reports/stocks/intraday/2026-07-30_18-35_stocks_intraday_report.md` §7).
- **evidence:** Prior WebSearch (11:45/16:06/18:38 EEST reviews) found only ~9-month-old (Oct 2025) shareholder-solicitation boilerplate; not re-verified this cycle (no new evidence either way).
- **suggested manual fix:** Audit the `legal_headline_risk`/`sec_doj` classifier's source data for PLTR; consider down-weighting generic shareholder-solicitation press-release boilerplate.
- **priority:** high
- **first observed:** 2026-07-30 11:45 EEST; still open 2026-07-30 21:45 EEST.

### TODO-2: META `legal_headline_risk` mislabeled as "indictment"
- **issue:** Still open, unresolved. META remains demoted B→C citing "active legal/headline risk (indictment)" this cycle too. Prior review confirmed the actual exposure is civil litigation (child-safety verdicts/trial), not a criminal indictment.
- **evidence:** Prior WebSearch (11:45 EEST review); not re-verified this cycle.
- **suggested manual fix:** Correct the legal-risk taxonomy/label for META from "indictment" to "civil_litigation" or similar.
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST; still open 2026-07-30 21:45 EEST.

### TODO-3: Recurring `UNKNOWN_INCONSISTENT` lifecycle mapping — unmapped status `'tp2_hit'`
- **issue:** AAPL, GOOGL, XOM (stocks/intraday/B) pattern, persistent across at least 5 consecutive review cycles now (04:47, 11:45, 16:06, 18:38, 21:45); not independently re-verified this cycle since `PAPER_MONITOR_STATUS_LATEST.md` is ~1h50m stale.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` (19:54 EEST), UNKNOWN_INCONSISTENT=5, count unchanged from prior cycles.
- **suggested manual fix:** Fix the lifecycle-state mapping for legacy-touch signals with raw status `tp2_hit` in the stocks/intraday/B path so it resolves to a proper CLOSED_WIN/OPEN state.
- **priority:** high
- **first observed:** 2026-07-29; reappeared every reviewed cycle since, including 2026-07-30 21:45 EEST.

### TODO-4: Separate lifecycle inconsistency — "labelled loss but final_r>0"
- **issue:** MSTR and PLTR (stocks/intraday/C) shown with "labelled loss but final_r>0 — inconsistent"; same caveat as TODO-3 (not independently re-verified this cycle, bucket count unchanged).
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` (19:54 EEST).
- **suggested manual fix:** Audit the loss-labelling logic for legacy-touch signals where `final_r` is computed as positive but the status field still says "loss".
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST; still open.

### TODO-5: Catalyst mapping weak again this run (70.8% unmapped, unchanged since the 18:45 EEST refresh)
- **issue:** 2124 of 3000 catalyst events today have no resolved symbol — above the 50% weak-mapping threshold, not improving across at least 4 consecutive reviews (67.3% → 71.6% → 70.8% → 70.8%).
- **evidence:** live count of `data/catalysts/2026-07-30/catalyst_events.jsonl` this run: 876 mapped / 2124 unmapped.
- **suggested manual fix:** Continue widening/improving the symbol resolver in the catalyst layer per [[project_crypto_ai_desk_catalyst_linkage]].
- **priority:** low (known, deferred, not worsening materially, but not improving either)
- **first observed:** recurring; re-confirmed 2026-07-30 21:45 EEST.

### TODO-11: EPIC/USDT (crypto/intraday/B) lifecycle status cannot be reconciled between the 19:54 EEST paper-monitor snapshot and the live 21:39 EEST active-signals query
- **issue:** `PAPER_MONITOR_STATUS_LATEST.md` (19:54 EEST) shows EPIC/USDT long (crypto/intraday/B) as OPEN ("entry filled, monitoring TP/SL"), and a separate EPIC/USDT long (crypto/swing/B) as WAITING. The live `active-signals --asset-class crypto` query run at 21:39 EEST for this review shows no EPIC/USDT row in either mode among the 22 live signals returned. The most likely explanation is that both resolved (closed win/loss/flat) in the intervening ~1h45-50m, which would be normal lifecycle progression, but this review's source-discipline rule (never fabricate an outcome) means no result is asserted.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` (19:54 EEST) item rows for EPIC/USDT vs. live `python -m src.cli active-signals --asset-class crypto` output captured 2026-07-30 21:39 EEST (22 rows, no EPIC/USDT).
- **suggested manual fix:** A human session (or the next monitor-status regeneration) should check the `signal_outcomes` table directly for EPIC/USDT's actual closed-trade record from this window, to confirm whether this is simply monitor-status staleness or a genuine gap in signal tracking.
- **priority:** medium
- **first observed:** 2026-07-30 21:45 EEST.

### TODO-8 (carried forward): `llm_stocks_packet.md` regeneration cadence lags the underlying stocks-intraday report
- **issue:** This cycle's `data/processed/llm_stocks_packet.md` mtime (19:10 EEST) is ~2h25m older than the freshly-regenerated `data/reports/stocks/intraday/2026-07-30_18-35_stocks_intraday_report.md` (21:35 EEST) it is supposed to summarize. This review read the raw report directly to avoid stale packet content.
- **evidence:** file mtimes above, both captured this review cycle.
- **suggested manual fix:** Confirm whether `prepare-analysis --mode stocks_intraday` (or equivalent) is wired into every scheduler cycle that regenerates the stocks-intraday report, or only some of them; align the cadence if not.
- **priority:** low
- **first observed:** 2026-07-30 18:38 EEST; still open 2026-07-30 21:45 EEST.
