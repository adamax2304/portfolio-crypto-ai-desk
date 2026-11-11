# Opus Enriched Review — US open reaction review — Auto Cycle 18:38 EEST

## 1. Executive Summary

Slot: **US open reaction review** (target 18:30 EEST / ~11:30 ET, actual data pull 18:38-18:48 EEST — within tolerance). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** External web research was available and used this run. Every internal scan this cycle (crypto scalp, crypto intraday, crypto swing, stocks intraday) returned **zero A/B-tier actionable ideas** — this is a genuinely quiet decision window, not a system failure: scalp remains kill-switched desk-wide, and every stocks candidate that scored A/B on raw technicals was gated to C by SI-1..5 (lunch-session confirmation, RVOL, sector confirmation, or legal/earnings flags). The US session is live and diverging hard: **S&P +0.88%, Nasdaq +1.6%, Dow +0.53% on a Microsoft +15% cloud-earnings surge**, while **Russell 2000/IWM -1.61%** — a genuine large-cap-vs-small-cap split that the internal "risk_off, breadth 0%" read (a 5d/20d trend metric) does not contradict but does not fully capture either (today's print is a single-day large-cap-driven bounce inside a still-down medium-term trend). The single most decision-relevant catch this cycle: the freshly-refreshed `binance_ecosystem_teaser` catalyst basket (primary BNB/USDT) is built on a headline that is **not actually a bullish Binance-ecosystem catalyst** — it is a governance/delisting crisis at "BNB Plus" (ticker BNBX), a small Nasdaq-delisted BNB-treasury shell company that just lost its crypto asset manager with no successor named (published today, verified via CryptoSlate + WebFetch). Direct BNB holdings disclosed are small (2,186 BNB as of Q1), so this is not a major forced-seller overhang, but the basket's "bullish rotation" framing is mislabeled — BNB is demoted from catalyst-watch to caution this cycle. **AAPL, AMZN, COIN, MA, and MSTR all report earnings today after the close** — do not chase any of the five into the print; existing C-tier watchlist entries on AAPL/GOOGL are research-only, not actionable. Catalyst mapping remains weak (70.8% unmapped, re-counted live post-refresh). Crypto stays selective: BTC ~$64.5-64.8K, ETH ~$1,908-1,923, both modestly higher on the Fed's steady-rate hold; EPIC/USDT and GIGGLE/USDT are the cleanest pure-momentum longs (no catalyst backing, chase risk at current extension); BANK/USDT (Lorenzo Protocol) is -55% today alone and -78% from its mid-July ATH — a crash-continuation/unwind pattern, not a fresh short entry, and squeeze-risk elevated per external funding. Scanning, tracking, and monitors continue in every mood; this review recommends selective caution and confirmation, never a stop.

## 2. Data Used

| File / Source | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-30_15-26_scalp_report.md` | 18:26:00 EEST | ~22min — fresh |
| `data/reports/intraday/2026-07-30_15-35_intraday_report.md` | 18:35:37 EEST | ~13min — fresh |
| `data/reports/swing/2026-07-30_13-04_swing_report.md` | 16:04:37 EEST | ~2h44m — fresh (<4h bucket) |
| `data/reports/stocks/intraday/2026-07-30_15-38_stocks_intraday_report.md` | 18:38:09 EEST | ~10min — fresh, generated just after RTH reaction |
| `data/reports/stocks/swing/…` / `invest/…` (2026-07-02) | deprecated/removed playbooks — see [[project_crypto_ai_desk_stocks_position_framework]], not a freshness failure |
| `data/catalysts/2026-07-30/catalyst_events.jsonl` (3000 rows, re-counted live post-refresh) + `narrative_baskets.jsonl` | 18:45:01 EEST | ~3min — fresh, refreshed mid-review |
| `data/processed/llm_analysis_packet.md` (crypto) | 18:35:37 EEST | ~13min — fresh |
| `data/processed/llm_stocks_packet.md` | 15:33:17 EEST | ~3h15m — stale relative to the 18:38 stocks report; read the fresher raw report directly instead (see TODO-8) |
| `reports/PAPER_MONITOR_STATUS_LATEST.md` | 16:11 EEST | ~2h37m — used with a freshness caveat, cross-checked against live `active-signals` |
| `python -m src.cli active-signals --asset-class crypto` / `stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` / `stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-30` | live query | now — none found |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-30_1606.md` (pre-US-open slot) | 16:13 EEST | for §4 diff |
| WebSearch: US stock market today (Fed/MSFT/META earnings), BTC/ETH price today, BANK/Lorenzo Protocol token, BNB treasury company Nasdaq | live | now |
| WebFetch: CryptoSlate BNB Plus treasury article (verify + extract forced-selling risk detail) | live | now |

**External web research was available and used this run.**

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-07-30_default_schedule/scheduler.log` mtime 18:38:33 EEST (fresh, cycle 2/12 actively running at data-pull time). Latest `cycle_01_14-53_summary.md` mtime 16:14 EEST (~2h34m old at pull time) — not deferred; scheduler.log alone was fresh, and cycle 2 completed its crypto/stocks report steps live during this review.
- Crypto scalp/intraday reports fresh (~13-22min). Crypto swing report ~2h44m old — inside the fresh (<4h) bucket, no carry-forward flag needed this cycle.
- Stocks-intraday report regenerated at 18:38 EEST, ~10min old — captures the live RTH reaction to the Fed hold + MSFT/META earnings.
- Catalyst JSONL refreshed mid-review (18:45 EEST): **3000** unique events today, **876 mapped (29.2%)**, **2124 unmapped (70.8%)** — weak-mapping threshold breached again (see §5, TODO-5 recurring, worse than the 16:06 review's 71.6%→ now 70.8%, essentially flat).
- `detect_untracked_legacy_alerts --since 2026-07-30`: **None** — every legacy crypto alert has a backing proposed_signal.
- `reports/PAPER_MONITOR_STATUS_LATEST.md` (16:11 EEST, ~2h37m old): REVIEW_ONLY_SHADOW=36, ENTERED_UNRESOLVED_EXPIRED=2, NO_ENTRY_EXPIRED=53, CLOSED_WIN=147, CLOSED_LOSS=13, CLOSED_FLAT=13, UNKNOWN_INCONSISTENT=5, OPEN_ACTIVE=0, WAITING_FOR_ENTRY=0. Cross-checked against live `active-signals`: crypto shows 18 non-terminal signals, all `tp1_hit`/`tp2_hit` (TP touched, still tracking remainder of ladder or stop — consistent with OPEN_ACTIVE reading as 0 under this system's stricter "not yet TP-touched" definition); stocks shows 50 non-terminal signals including 2 genuinely fresh C-tier watchlist entries (GOOGL, XLY, both `waiting_for_entry`, expiring 2026-07-31).
- **Recurring lifecycle anomaly, unchanged**: UNKNOWN_INCONSISTENT bucket (5 items, same pattern as the 11:45/16:06 EEST reviews) — not independently re-verified line-by-line this cycle since `PAPER_MONITOR_STATUS_LATEST.md` is 2h37m stale; treated as still-open per TODO-3/TODO-4 below rather than re-litigated.
- Zero A/B-tier ideas this cycle across scalp, intraday, and stocks-intraday trade-idea agent outputs (verified directly from `data/processed/agent_outputs/20260730_153411_*` [scalp], `20260730_153530_*` [intraday], and the stocks report §6 "No A/B-tier actionable setups in this run").

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-30 18:48 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.83,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["llm_stocks_packet.md is ~3h stale relative to the fresher raw stocks-intraday report (read directly instead)", "PAPER_MONITOR_STATUS_LATEST.md is ~2h37m old, used with caveat"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 18:38 EEST fresh, cycle 2/12 running live", "crypto scalp/intraday ~13-22min fresh", "crypto swing ~2h44m, inside fresh bucket", "stocks-intraday regenerated 18:38 EEST capturing live RTH reaction", "catalyst JSONL refreshed live mid-review: 3000 rows, 876 mapped/2124 unmapped", "detect_untracked_legacy_alerts: none"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.65,
      "reason_codes": ["mixed", "longs_preferred", "shorts_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["External: S&P +0.88%, Nasdaq +1.6%, Dow +0.53% on MSFT +15% cloud-earnings surge; Russell 2000/IWM -1.61% — genuine large-cap-vs-small-cap divergence", "Internal stocks regime label: risk_off/short bias, breadth 0% above EMA20 (a 5d/20d trend read, not contradicted by today's single-day large-cap bounce)", "Internal crypto regime: range/chop, neutral, BTC transition_up, ETH uptrend, altcoin breadth 41.9% above EMA20", "External: BTC ~$64.5-64.8K, ETH ~$1,908-1,923, both modestly higher post-Fed-hold"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "catalyst_contradicted", "mapping_weak"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 3000 rows, 876 mapped (29.2%), 2124 unmapped (70.8%) — weak-mapping threshold breached", "binance_ecosystem_teaser basket (primary BNB/USDT) is built on a mislabeled headline: BNB Plus (BNBX) is a small Nasdaq-delisted BNB-treasury shell company in a governance crisis, not a bullish Binance-ecosystem event; verified via CryptoSlate + WebFetch, published 2026-07-30", "momentum_breakout basket (EPIC/USDT, GIGGLE/USDT) explicitly flagged as 'top gainers without confirmed news catalyst — pure momentum cluster'", "delisting_thin_liquidity basket present, no specific symbols, generic avoid-chase note"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["OI change unavailable ('n/a') for most symbols this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK/USDT: external funding negative across venues (bybit -0.0075, mexc -0.0022), crowding 'elevated' — squeeze-risk caveat against a fresh short after an already -55% day / -78% from mid-July ATH", "ESP/USDT and EUL/USDT: negative funding across external venues, crowding 'elevated'", "EPIC/USDT, GIGGLE/USDT, ZAMA/USDT: funding neutral, crowding 'low' — cleaner if a long/short thesis develops"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "entry_late", "stale_before_entry"],
      "data_missing": ["TradingView / manual chart check unavailable this run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["EPIC/USDT +19.4% 24h, +35.1% 7d, tagged overextended in prior scans, RS vs BTC +18.25% — trade-idea agent's own conditional entry plan is a pullback zone (0.8314-0.8596), current price 0.8722 is already through it", "ADA/USDT +7.3% 24h, tagged breakout+overextended, 3.63x volume — chase risk at current levels despite a real catalyst (Cardano data-monetization partnership news)", "BANK/USDT -55% 24h alone, -78% from ATH — a short here chases an already-extreme move, not a fresh setup", "Stocks: every raw-A/B candidate this cycle was demoted specifically by `lunch_requires_strong_confirmation` (8x) — 11:30am-1:30pm ET lunch-chop gate is active at this exact slot time (11:38 ET)"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.78,
      "reason_codes": ["review_shadow", "no_entry", "needs_review", "waiting_for_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto: 18 non-terminal signals live, all TP1/TP2-touched (tracking remaining ladder or stop; none flagged as a fresh open-actionable entry this cycle)", "Stocks: 50 non-terminal signals live; 2 genuinely fresh C-tier watchlist entries (GOOGL, XLY) waiting for entry, expiring 2026-07-31 — research-grade only, not actionable", "PAPER_MONITOR_STATUS_LATEST.md (2h37m stale, cross-checked): REVIEW_ONLY_SHADOW=36, ENTERED_UNRESOLVED_EXPIRED=2, NO_ENTRY_EXPIRED=53, CLOSED_WIN=147/LOSS=13/FLAT=13, UNKNOWN_INCONSISTENT=5 (recurring, not re-verified line-by-line this cycle)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.72,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review"],
      "data_missing": ["cannot re-confirm the PLTR sec_doj / META indictment flags beyond the 11:45/16:06 review's research pass"],
      "suggested_effect": "advisory_only",
      "facts_used": ["AAPL, AMZN, COIN, MA, MSTR report earnings today (2026-07-30) after the close — do_not_chase_warning + block_requires_operator_review active on all five", "XOM reports Q2 earnings tomorrow (2026-07-31) — same warning class", "META already reported this morning: stock fell ~10% on a disappointing revenue forecast despite MSFT's +15% surge on the same earnings cycle — confirms the earnings-volatility theme is live, not hypothetical", "PLTR still shows legal_headline_risk 'sec_doj' (C-tier, unresolved TODO-1); META still shows legal_headline_risk 'indictment' (C-tier, unresolved TODO-2) — both unchanged since 11:45 EEST", "BNB Plus (BNBX) governance-crisis headline mapped under BNB/USDT — small disclosed direct holdings (2,186 BNB), so overhang risk is minor but the catalyst label itself is misleading (see §5)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto B-tier weekly headline: n=75, winrate 27.8%, PF 2.12, avgR +0.358, totalR +17.9 — healthy despite low winrate; crypto scalp mode PF 0.25/-3.0R (correctly kill-switched)", "Crypto shorts weak this week: n=14, PF 0.33, totalR -2.0 — short_playbook overlay underperforming its usual 'cleaner than longs' pattern in the trailing week", "Stocks A/B headline: n=2 anecdotal, PF 0.0, totalR -1.0 — not enough sample to trust either way", "Stocks C-tier watchlist: n=182-183, winrate ~5.7-5.8%, PF ~0.09-0.10, totalR -9 to -11 — badly losing, consistent with C-tier being correctly non-actionable by design", "Stocks intraday 14d post-trade diagnostics: forward_postfreeze n=252, ΣR=-55.20 — the only evidence-class bucket usable as proof, and it is negative; top avoidable loss bucket is 'no_gate_context' (-410R over 736, mostly backfill_pretrained, hypothesis-only, not proof)"] },
    { "agent": "head_trader", "verdict": "advisory_only",
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of the eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "EPIC/USDT", "trigger": "pullback into 0.8314-0.8596 zone with volume holding (current price 0.8722 is already through the conditional entry zone — do not chase at current extension); invalidation 0.7969", "reason": "strongest RS mover in the intraday scan (score 93, RS vs BTC +18.25%), but no catalyst backing and the trade-idea agent's own thesis is watchlist-only pending a cleaner entry" },
    "best_short_candidate":    { "symbol": "IWM", "trigger": "wait for a clean break/retest of today's low with volume once the lunch-chop gate (11:30am-1:30pm ET) clears — do not chase the already-realized -1.61% divergence from SPY/QQQ", "reason": "the cleanest real short-side confirmation this cycle: Russell 2000 diverging hard from the MSFT-driven large-cap rally, though internally demoted to C on rr_below_min_required (rr_to_tp1=0.87)" },
    "best_catalyst_candidate": { "symbol": "none clean — BNB/USDT basket demoted to caution", "trigger": "would need a genuine Binance-protocol-level (not BNB-treasury-shell) catalyst plus a non-extended entry; current basket thesis is mislabeled (see §5) and BNB is not among today's top movers", "reason": "the only fresh narrative basket this cycle turned out to be a governance-crisis headline about a small, unrelated Nasdaq-delisted treasury company, not a bullish BNB-ecosystem event" },
    "avoid_candidate":         { "symbol": "BANK/USDT (Lorenzo Protocol) short", "reason": "already -55% today alone and -78% from its mid-July ATH; chasing a short here fights an extreme, likely-exhausted move, and external funding/crowding data flags elevated squeeze risk on the short side" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 8
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.83 | scheduler_fresh, report_stale | advisory_only |
| market_regime | mixed | 0.65 | mixed, longs_preferred, shorts_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, entry_late, stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.78 | review_shadow, no_entry, needs_review, waiting_for_entry | advisory_only |
| risk_manager | caution | 0.72 | headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.68 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | watch_only | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review (16:06 EEST, pre-US-open)

- **US session opened and moved decisively**: S&P/Nasdaq/Dow up hard on MSFT's +15% cloud-earnings surge; Russell 2000/IWM down -1.61% — the large-cap/small-cap split the 16:06 review could not see (cash session was closed).
- **NFLX long-watch (16:06 pick) failed to develop**: NFLX is now `no_trade` / `no_directional_setup` in the fresh 18:38 stocks report — not among today's actionable-adjacent candidates at all. Dropped from this cycle's watch list.
- **JPM short-watch (16:06 pick) persists but is unconfirmed**: still C-tier, still gated (`sector_confirmation_weak_or_unknown`, `lunch_requires_strong_confirmation`, `liquidity_rvol_below_min`) — no RTH confirmation yet; demoted in this review's ranking in favor of IWM, which now has a real, externally-verified divergence behind it.
- **AMD short-TTL BLOCK (16:06, expired ~20:06 EEST) is no longer relevant** — AMD does not appear as a raw A/B candidate in the fresh 18:38 stocks report at all (`AMD (no_trade): 32.95 — no_directional_setup`); the contradiction that triggered the block appears to have resolved into a flat/no-setup read rather than a live short.
- **New finding this cycle**: the `binance_ecosystem_teaser` catalyst basket refreshed with a new, different headline (BNB Plus/BNBX governance crisis) that is mislabeled as a bullish Binance-ecosystem catalyst — not caught or discussed in the 16:06 review, which only saw the earlier version of this basket (Binance Alpha listing chatter).
- **Catalyst mapping**: 71.6% unmapped at 16:06 → 70.8% now (live re-count post-refresh) — essentially flat, still breaching the 50% threshold (TODO-5 recurring).
- **TODO-1 (PLTR sec_doj) and TODO-2 (META indictment)**: still open, unchanged, re-confirmed present in the fresh 18:38 stocks report.
- **Earnings thesis confirmed live**: META already reported and fell ~10% on a weak revenue forecast this morning, while MSTR/AAPL/AMZN/COIN/MA remain pending after tonight's close — the earnings-volatility risk flagged at 16:06 is now playing out in real time, reinforcing the do-not-chase stance into tonight's prints.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **3000** (live re-count, post mid-review refresh at 18:45 EEST). Mapped (non-null symbol): **876 (29.2%)**. Unmapped: **2124 (70.8%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets today (refreshed 18:45 EEST):
  - **binance_ecosystem_teaser** (playbook `related_beta_rotation`, source single_source, freshness label `<6h`) primary: BNB/USDT, related ASTER/USDT — **mislabeled this cycle**: the underlying headline is about BNB Plus (BNBX), a small Nasdaq-delisted BNB-treasury shell company that just lost its crypto asset manager with no successor named (published today; verified via CryptoSlate + WebFetch). Disclosed direct holdings are small (2,186 BNB as of Q1), so forced-selling overhang is minor, but this is not a bullish "Binance ecosystem" event as the basket name implies — treat as **caution/noise**, not a catalyst-backed long.
  - **momentum_breakout** (playbook `wait_pullback`, freshness `<1h`) — EPIC/USDT +19.4% (vol 1.28x), GIGGLE/USDT +17.3% (vol 1.56x) — explicitly flagged internally as "top gainers **without** confirmed news catalyst — pure momentum cluster."
  - **delisting_thin_liquidity** (playbook `avoid_low_liquidity`, freshness `<6h`) — no specific symbols, generic "avoid chasing low-float dumps" note.
- Top unmapped-illustrative items (not tradable as-is): generic macro/geopolitical wire copy (Iran/Hormuz de-escalation follow-ups), shareholder-fraud-lawsuit boilerplate (PR Newswire), and crypto Telegram promo/AMA posts with no resolvable ticker.

## 6. Market Landscape

The picture this cycle is a real, externally-confirmed divergence rather than a clean risk-on or risk-off tape: US large-caps are ripping on a single mega-cap earnings beat (MSFT +15%) while small-caps (Russell 2000/IWM) sell off -1.61% — a narrow, concentration-driven rally, not broad risk appetite. The internal stocks regime label (`risk_off`, breadth 0% above EMA20) is a 5d/20d trend read and is not contradicted by today's single-day bounce, but it also does not fully capture the live large-cap/small-cap split — read it as "medium-term downtrend, today's print is a large-cap-concentrated relief bounce, not a regime change." Crypto stays selective and modestly firmer post-Fed-hold (BTC ~$64.5-64.8K, ETH ~$1,908-1,923), with no A/B setups internally this cycle — the strongest movers (EPIC/USDT, GIGGLE/USDT, ADA/USDT) are pure momentum, already extended, and explicitly tagged as chase-risk by the desk's own scoring. The one narrative basket that looked catalyst-backed (BNB/USDT via `binance_ecosystem_teaser`) turned out to be built on a mislabeled governance-crisis headline about an unrelated small-cap treasury shell company, not a genuine Binance-ecosystem catalyst. Tonight's close brings AAPL, AMZN, COIN, and MA earnings (MSTR already reported today per the 16:06 review's earnings-today list) — META's ~10% post-earnings drop this morning is a live reminder that the earnings-volatility risk is real, not theoretical.

### Market Mood / Risk Routing
- Crypto mood: **mixed / selective** (BTC transition_up, ETH uptrend, altcoin breadth 41.9% above EMA20; no A/B setups; strongest movers are unconfirmed momentum, not catalyst-backed)
- Stocks mood: **mixed / narrow** (large-cap indices up hard on a single mega-cap earnings beat, small-caps diverging down; internal medium-term regime still risk_off/short-biased; zero A/B actionable this cycle, mostly gated by lunch-session and liquidity confirmation requirements)
- Dominant narrative: MSFT's blowout cloud print is carrying the large-cap tape; small-caps are not participating; four more mega-cap earnings (AAPL, AMZN, COIN, MA) land after tonight's close on top of META's ~10% drop this morning — earnings-driven single-stock volatility is the dominant force right now, not a broad macro regime shift
- Preferred side now: **wait-for-trigger / RTH-confirmation** — no side is clean; crypto has no open new entries this cycle, stocks are gated by the lunch-session confirmation window (11:30am-1:30pm ET, active right now at 11:38 ET)
- Best long candidate: EPIC/USDT watch — needs a pullback into 0.8314-0.8596, not a chase at the current 0.8722 extension
- Best short candidate: IWM watch — needs a clean break/retest of today's low with volume once the lunch-chop gate clears; do not chase the already-realized -1.61% divergence
- Best catalyst-backed candidate: none clean this cycle — the one fresh basket (BNB/USDT) is mislabeled/noise, not a genuine bullish catalyst
- What to avoid: BANK/USDT short (already -55% today / -78% from ATH, squeeze-risk elevated); chasing AAPL/AMZN/COIN/MA into tonight's earnings; treating the BNB/USDT basket as a clean catalyst long
- What would change the view: a clean RTH retest confirming IWM short or EPIC pullback-long; small-caps joining the large-cap rally (would flip the "narrow" read to genuine risk-on); tonight's AAPL/AMZN/COIN/MA earnings reactions, which will set tomorrow's (04:30 EEST) crypto-overnight and Asia-session tone

## 7. Candidate Deep Dives

### 1. EPIC/USDT — crypto intraday/scalp, C-tier watchlist (score 62.7 intraday / 64.2 scalp), long — best long-watch
- Internal setup: long, watchlist only, conditional pullback entry 0.8314-0.8596, invalidation below 0.7969, RR to TP1 1.84.
- Has price already reacted to the catalyst? There is no catalyst — this is a pure momentum/RS move (+19.4% 24h, +35.1% 7d, RS vs BTC +18.25%); the `momentum_breakout` basket explicitly confirms "no confirmed news catalyst."
- Is the setup chasing? Yes at the current 0.8722 price — already through the conditional entry zone.
- Retest/pullback structure? The desk's own plan requires one; not present yet.
- Overextended? RS/momentum tags plus the >2ATR-from-EMA20 avoid-condition in the raw agent output both flag this.
- Would entry now be late? Yes.
- Aligned with market mood? Directionally yes (crypto mildly firmer post-Fed), but nothing catalyst-specific supports it.
- Actionable now or after confirmation? After confirmation only — needs the pullback zone to hold with volume.
- Invalidation: 1h close below 0.7969.
- Chase-risk setup? Yes, explicitly.
- Catalyst confirmation/contradiction? Neither — no catalyst either way, pure technical.

### 2. IWM — stocks intraday, C-tier (raw B, score 68.88), short — best short-watch
- Internal setup: short, demoted B→C on `rr_below_min_required` (rr_to_tp1=0.87 < 1.50) — no clean structural 1.5R target this cycle.
- External verification: Russell 2000 -1.61% today, diverging sharply from SPY (+0.88%) and Nasdaq (+1.6%) — a real, externally-confirmed small-cap-vs-large-cap split, not a stale internal read.
- Has price already reacted? Yes, the divergence is already visible; entering right now (mid-lunch-session, 11:38 ET) risks chasing the already-realized move.
- Chasing? Moderate risk — the move is real but the internal RR gate correctly flags no clean structural target yet.
- Retest/pullback structure? Not yet confirmed; wait for the post-lunch session (after ~13:30 ET / ~20:30 EEST) when the `lunch_requires_strong_confirmation` gate would naturally clear.
- Aligned with mood? Yes — this is the cleanest expression of "narrow, large-cap-only rally" this cycle.
- Actionable now or pending confirmation? Pending — wait for a break/retest of today's low with volume after lunch-session chop clears.
- Catalyst confirmation/contradiction? No stock-specific catalyst; purely index-relative-strength divergence.

### 3. BNB/USDT — crypto, catalyst basket primary, demoted to caution
- Internal setup: `binance_ecosystem_teaser` basket, freshness label `<6h`, primary BNB/USDT, related ASTER/USDT, playbook `related_beta_rotation`.
- External verification: the underlying headline ("BNB treasury company dumps its crypto manager after Nasdaq suspends its stock") is about **BNB Plus (BNBX)**, a small company that ran a corporate BNB-treasury strategy, was suspended from Nasdaq on 2026-07-14 after a failed treasury bet, and just terminated its crypto-asset-manager relationship with no successor named (CIO departed 7/23, Chairman resigns 7/31). Disclosed direct BNB holdings are small (2,186 BNB as of Q1) — meaningful forced-selling overhang is unlikely at that size, but this is a corporate-governance story about a distressed shell company, not a Binance-protocol catalyst.
- Has price already reacted? BNB/USDT does not appear among today's strongest or weakest movers in the fresh intraday report — no visible reaction either way.
- Chasing? N/A — no clean setup either direction.
- Catalyst confirmation/contradiction? **Mislabeled** — the basket name implies a bullish rotation catalyst; the actual news is neutral-to-mildly-negative governance noise about an unrelated small-cap vehicle.
- Actionable now or pending confirmation? Neither — demote from catalyst-watch to caution/skip pending a genuine BNB-protocol-level catalyst.

### 4. BANK/USDT (Lorenzo Protocol) — crypto, C-tier top mover (score 82.2), short bias — avoid, not a fresh short
- Internal setup: short bias, score 82.2, tags `weak_vs_market`, `breakdown`, `overextended`, -55.0% 24h move, RS vs BTC -56.1%.
- External verification: Lorenzo Protocol (BANK) pumped from ~$0.03 to an ATH of $0.5294 in mid-July 2026 on a BTCFi/rotation narrative (WLFI wallet purchase publicity included); it is now trading **-78% below that ATH**, and today's -55% is part of that ongoing unwind, not a fresh, isolated breakdown.
- Has price already reacted? Yes, extremely — this is the tail end (or middle) of a violent pump-and-dump unwind.
- Chasing? A fresh short here chases an already-extreme move.
- Retest/pullback structure? None visible; this is capitulation-style price action.
- Overextended? Yes, to the downside — the opposite chase risk from a long-side overextension.
- Aligned with mood? Directionally (weak_vs_market), but the move is already realized, not developing.
- Actionable now or pending confirmation? Neither — avoid until either a clean lower-high short-retest forms or price stabilizes enough to define real risk.
- Squeeze risk: external funding is negative and crowding is flagged "elevated" — a real risk that a short entered here gets caught in a relief-bounce squeeze.
- Catalyst confirmation/contradiction? No fresh catalyst tied to today's specific move found in the internal news feed; treat as pure technical unwind continuation.

### 5. Mega-cap earnings cluster (AAPL, AMZN, COIN, MA) — stocks, earnings today after the close — avoid chasing
- Internal setup: all four (plus MSTR) carry `do_not_chase_warning` + `block_requires_operator_review` for earnings today (2026-07-30); AAPL and GOOGL also carry separate C-tier watchlist entries (short bias, not actionable) unrelated to the earnings flag itself.
- External verification: META already reported this morning and fell ~10% on a disappointing revenue forecast, even as MSFT (same reporting cycle) surged +15% on strong cloud growth — confirms this is a genuinely earnings-driven, single-stock-dispersion tape, not a uniform macro move.
- Has price already reacted? Only for META/MSFT so far (already reported); AAPL/AMZN/COIN/MA/MSTR reactions are still pending tonight's prints.
- Chasing? Any directional bet on these four ahead of tonight's numbers is a pure earnings gamble, not a technical setup.
- Actionable now or pending confirmation? Pending — do not position ahead of the print; re-evaluate at the 21:30 EEST late-session review or the 23:15 EEST post-close review once reactions are known.
- Catalyst confirmation/contradiction? N/A — this is a scheduled event risk, not a contradicted thesis.

## 8. Best Candidates Ranked

1. **IWM short-watch** — best short-watch, real externally-confirmed small-cap/large-cap divergence, wait for post-lunch break/retest with volume.
2. **EPIC/USDT long-watch** — best long-watch, strongest RS in crypto but needs the 0.8314-0.8596 pullback, not a chase at 0.8722.
3. **BNB/USDT** — demoted from catalyst-watch to caution; basket is mislabeled, no genuine bullish catalyst behind it this cycle.
4. **BANK/USDT** — avoid; already-extreme -55%/-78%-from-ATH unwind, squeeze risk on a fresh short.
5. **AAPL/AMZN/COIN/MA earnings cluster** — avoid positioning ahead of tonight's prints; re-check post-close.

## 9. Avoid / No Trade (this decision window only)

- **BANK/USDT short**: already -55% today / -78% from ATH — chasing an extreme unwind, squeeze-risk elevated on external funding/crowding data.
- **AAPL, AMZN, COIN, MA, MSTR**: earnings today — `do_not_chase_warning` + `block_requires_operator_review` active on all five; MSTR earnings already released today per the internal earnings calendar, AAPL/AMZN/COIN/MA report after tonight's close.
- **BNB/USDT (binance_ecosystem_teaser basket)**: mislabeled catalyst — the underlying headline is a small-cap treasury-shell governance crisis, not a bullish Binance-ecosystem event; do not treat as catalyst-backed.
- **META, PLTR**: still carrying unresolved internal legal-risk flags (TODO-1/TODO-2, unchanged since 11:45 EEST) — treat as manual-review, not confirmed avoid, but also not a clean actionable.
- **Crypto scalp mode**: correctly disabled desk-wide (kill-switch), not a per-symbol avoid.
- This is a decision-window call only — scanning, tracking, and monitors continue in every mood; nothing here is a stop-the-system instruction.

## 10. Main Risks

- **Concentration risk in today's rally**: the S&P/Nasdaq gain is driven almost entirely by MSFT's single-name +15% move; Russell 2000 diverging -1.61% is a real signal that breadth is narrow, not broad risk-on — a reversal in MSFT sentiment or a broad-market catch-down to small-cap weakness is a live risk into the close.
- **Concentrated earnings-event risk tonight**: AAPL, AMZN, COIN, and MA all report after the close on the same day META already dropped ~10% on its print — expect elevated overnight/tomorrow-morning volatility; the 21:30 and 23:15 EEST reviews should specifically re-assess these four.
- **Catalyst-mapping/labeling risk**: the one fresh narrative basket this cycle (`binance_ecosystem_teaser`) was mislabeled — a reminder that basket names/playbook tags should be treated as a starting hypothesis to verify externally, not a ready-made thesis (see TODO-9).
- Squeeze risk on any short chasing BANK/USDT, ESP/USDT, or EUL/USDT given elevated external crowding/negative funding on all three.
- Data-quality risk: the recurring `UNKNOWN_INCONSISTENT` lifecycle-mapping bug (5 items) persists across at least 4 consecutive reviews now (TODO-3/TODO-4) — not independently re-verified this cycle due to `PAPER_MONITOR_STATUS_LATEST.md` staleness; always cross-check against live `active-signals` directly.
- Legal-flag reliability risk: META and PLTR legal_headline_risk flags remain unresolved/unverified since the 11:45 EEST review (TODO-1/TODO-2).
- Catalyst mapping is stuck at ~70-72% unmapped across at least 3 consecutive reviews (TODO-5) — the catalyst layer should be read as context, not a decision input, until this improves.
- Source-ingest note: the first `ingest_enriched_review_sources --asset-class crypto` attempt this cycle hit `sqlite3.OperationalError: database is locked` (scheduler cycle 2 writing concurrently); an immediate retry succeeded (5/6 rows written, idempotent UPSERT). No data loss, logged here per §M failure-handling.

## 11. Action Plan — next 4 hours

- No new crypto or stocks entries this cycle — zero A/B ideas across scalp, intraday, swing, and stocks-intraday.
- Watch IWM for a clean break/retest of today's low with volume once the post-lunch session (after ~13:30 ET) clears the `lunch_requires_strong_confirmation` gate; do not chase the already-realized move.
- Watch EPIC/USDT for a non-extended pullback into 0.8314-0.8596 before considering a long; do not chase at the current 0.8722 level.
- Do not treat BNB/USDT as catalyst-backed this cycle; the basket thesis is mislabeled.
- Do not short BANK/USDT, ESP/USDT, or EUL/USDT fresh here — all three carry elevated external crowding/squeeze-risk flags on top of already-extreme moves.
- Do not position in AAPL, AMZN, COIN, or MA ahead of tonight's earnings prints; re-assess at the 21:30 EEST late-session review and the 23:15 EEST post-close review once reactions are known.
- Continue managing existing crypto TP1/TP2-touched positions per their own ladders/stops; no new management action indicated by this review.

## 12. Final Verdict per Mode

- **Crypto scalp**: disabled (kill-switch), no change.
- **Crypto intraday**: 0 A/B ideas this cycle; 18 non-terminal signals from prior cycles tracking their own TP/stop ladders, no new entries indicated.
- **Crypto swing**: 0 A/B ideas this cycle (report ~2h44m old, inside fresh bucket); C-tier watchlist only.
- **Stocks intraday**: 0 A/B actionable this cycle — regime risk_off/short-biased on the medium-term trend, but today's session itself is a narrow large-cap rally; every raw A/B candidate gated by lunch-session/liquidity/legal/earnings rules. Wait for post-lunch RTH confirmation.
- **Stocks swing/invest**: deprecated/removed frameworks, no active signals this run (see [[project_crypto_ai_desk_stocks_position_framework]]).

## 13. Sources

- [Stock Market Today (July 30, 2026): S&P 500 rises as Microsoft surges, Fed holds rates steady (TheStreet)](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-july-30-2026)
- [Stock market today: Dow, S&P 500, Nasdaq rebound after Fed decision, as Microsoft leads tech gains (Yahoo Finance)](https://finance.yahoo.com/markets/live/stock-market-today-thursday-july-30-dow-sp-500-nasdaq-082255995.html)
- [Stock Market Live July 30, 2026: S&P 500 (SPY) Pivoting from Fed-Induced Drop (24/7 Wall St.)](https://247wallst.com/investing/2026/07/30/stock-market-live-july-30-2026-sp-500-spy-pivoting-from-fed-induced-drop/)
- [Bitcoin and ethereum prices today, Thursday, July 30, 2026: Prices rise after Fed leaves rates unchanged (Yahoo Finance)](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-thursday-july-30-2026-prices-rise-after-fed-leaves-rates-unchanged-132340233.html)
- [Lorenzo Protocol (BANK) Rallies on BTCfi and Yield Trends (tapbit.com)](https://www.tapbit.com/en/learn/article/lorenzo-protocol-bank-token-price-rally-july-2026-20260721)
- [Why is Lorenzo Protocol (BANK) up 46.78% Today, July 23, 2026? (BingX)](https://bingx.com/en/news/post/why-is-lorenzo-protocol-bank-up-today-july-btcfi-rotation-meets-a-high-turnover-breakout)
- [BNB treasury company dumps its crypto manager after Nasdaq suspends its stock, leaving no one in charge of its treasury (CryptoSlate, 2026-07-30)](https://cryptoslate.com/bnb-treasury-company-dumps-its-crypto-manager-after-nasdaq-suspends-its-stock-leaving-no-one-in-charge-of-its-treasury/)
- [BNB Plus suspended by Nasdaq after failed BNB treasury bet (Protos)](https://protos.com/bnb-plus-suspended-by-nasdaq-after-failed-bnb-treasury-bet/)
- [BNB treasury company plunges 77% after Nasdaq delisting notice (Cointelegraph)](https://cointelegraph.com/news/bnb-treasury-firm-falls-77-percent-after-nasdaq-delisting)
- Internal: `data/reports/stocks/intraday/2026-07-30_15-38_stocks_intraday_report.md` (generated 18:38 EEST, post-RTH-open).
- Internal: `data/catalysts/2026-07-30/narrative_baskets.jsonl` (refreshed 18:45 EEST).
- Internal: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-30_1606.md` (prior review, pre-US-open slot) — used for §4 diff.

## 14. Fix Requests / TODO

### TODO-1: PLTR `legal_headline_risk: sec_doj` flag looks like a false positive from law-firm solicitation boilerplate
- **issue:** Still open, unresolved since the 11:45 EEST review. PLTR remains demoted A→C citing "active legal/headline risk (sec_doj)" this cycle too (`data/reports/stocks/intraday/2026-07-30_15-38_stocks_intraday_report.md` §7).
- **evidence:** Prior WebSearch (11:45/16:06 EEST reviews) found only ~9-month-old (Oct 2025) shareholder-solicitation boilerplate; not re-verified this cycle (no new evidence either way).
- **suggested manual fix:** Audit the `legal_headline_risk`/`sec_doj` classifier's source data for PLTR; consider down-weighting generic shareholder-solicitation press-release boilerplate.
- **priority:** high
- **first observed:** 2026-07-30 11:45 EEST; still open 2026-07-30 18:38 EEST.

### TODO-2: META `legal_headline_risk` mislabeled as "indictment"
- **issue:** Still open, unresolved. META remains demoted B→C citing "active legal/headline risk (indictment)" this cycle too. Prior review confirmed the actual exposure is civil litigation (child-safety verdicts/trial), not a criminal indictment.
- **evidence:** Prior WebSearch (11:45 EEST review); not re-verified this cycle.
- **suggested manual fix:** Correct the legal-risk taxonomy/label for META from "indictment" to "civil_litigation" or similar.
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST; still open 2026-07-30 18:38 EEST.

### TODO-3: Recurring `UNKNOWN_INCONSISTENT` lifecycle mapping — unmapped status `'tp2_hit'`
- **issue:** AAPL, GOOGL, XOM (stocks/intraday/B) shown as "unmapped status 'tp2_hit'" in `PAPER_MONITOR_STATUS_LATEST.md` as of the 16:06 EEST review; not independently re-verified this cycle since that file is 2h37m stale and a line-by-line refresh was out of scope. Persistent across at least 3-4 consecutive review cycles (04:47, 11:45, 16:06, and presumed 18:38).
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` (16:11 EEST), UNKNOWN_INCONSISTENT=5 unchanged from prior cycle's count.
- **suggested manual fix:** Fix the lifecycle-state mapping for legacy-touch signals with raw status `tp2_hit` in the stocks/intraday/B path so it resolves to a proper CLOSED_WIN/OPEN state.
- **priority:** high
- **first observed:** 2026-07-29; reappeared every reviewed cycle since, including 2026-07-30 18:38 EEST (via unchanged bucket count).

### TODO-4: Separate lifecycle inconsistency — "labelled loss but final_r>0"
- **issue:** MSTR and PLTR (stocks/intraday/C) shown with "labelled loss but final_r>0 — inconsistent" as of the 16:06 EEST review; same caveat as TODO-3 (not independently re-verified this cycle, bucket count unchanged).
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` (16:11 EEST).
- **suggested manual fix:** Audit the loss-labelling logic for legacy-touch signals where `final_r` is computed as positive but the status field still says "loss".
- **priority:** medium
- **first observed:** 2026-07-30 11:45 EEST; still open.

### TODO-5: Catalyst mapping weak again this run (70.8% unmapped, effectively flat vs last cycle's 71.6%)
- **issue:** 2124 of 3000 catalyst events today have no resolved symbol — above the 50% weak-mapping threshold, not improving across at least 3 consecutive reviews (67.3% → 71.6% → 70.8%).
- **evidence:** live count of `data/catalysts/2026-07-30/catalyst_events.jsonl` this run (post-18:45 EEST refresh): 876 mapped / 2124 unmapped.
- **suggested manual fix:** Continue widening/improving the symbol resolver in the catalyst layer per [[project_crypto_ai_desk_catalyst_linkage]].
- **priority:** low (known, deferred, not worsening materially, but not improving either)
- **first observed:** recurring; re-confirmed 2026-07-30 18:38 EEST.

### TODO-9: Narrative-basket auto-labeling can mismatch its own summary text — needs a sanity check
- **issue:** The `binance_ecosystem_teaser` basket (playbook `related_beta_rotation`, implying a bullish rotation thesis) was built this cycle from a headline about "BNB treasury company dumps its crypto manager after Nasdaq suspends its stock" — a governance/delisting crisis at a small, unrelated shell company (BNB Plus/BNBX), not a bullish Binance-protocol catalyst. The basket's own `catalyst_summary` field even includes the negative headline verbatim, but the `suggested_playbook` and basket name still frame it as a bullish rotation setup.
- **evidence:** `data/catalysts/2026-07-30/narrative_baskets.jsonl` (18:45 EEST refresh), `binance_ecosystem_teaser` entry; external verification via CryptoSlate/Protos/Cointelegraph (see §13) confirms the headline is about BNB Plus (BNBX), not BNB-the-protocol.
- **suggested manual fix:** Consider a lightweight sentiment/polarity check on the headline(s) feeding a narrative basket before the basket inherits a directional `suggested_playbook` (e.g., `related_beta_rotation` implies bullish) — a governance-crisis or delisting headline about an entity merely named "BNB ___" should not silently carry a bullish rotation label just because the primary symbol string matches.
- **priority:** medium
- **first observed:** 2026-07-30 18:38 EEST.

### TODO-8 (carried forward, renumbered from 16:06's TODO-7 discussion, new symbol): `llm_stocks_packet.md` regeneration cadence lags the underlying stocks-intraday report
- **issue:** This cycle's `data/processed/llm_stocks_packet.md` mtime (15:33:17 EEST) is ~3h05m older than the freshly-regenerated `data/reports/stocks/intraday/2026-07-30_15-38_stocks_intraday_report.md` (18:38:09 EEST) it is supposed to summarize. This review read the raw report directly to avoid using stale packet content, but a future automated consumer that only reads the packet would get a stale RTH picture.
- **evidence:** file mtimes above, both captured this review cycle.
- **suggested manual fix:** Confirm whether `prepare-analysis --mode stocks_intraday` (or equivalent) is wired into every scheduler cycle that regenerates the stocks-intraday report, or only some of them; align the cadence if not.
- **priority:** low
- **first observed:** 2026-07-30 18:38 EEST.
