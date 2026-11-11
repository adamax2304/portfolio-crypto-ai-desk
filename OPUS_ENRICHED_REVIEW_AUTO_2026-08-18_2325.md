# Opus Enriched Review — post-close final daily review — Auto Cycle 23:25 EEST

## 1. Executive Summary
- **Slot: post-close final daily review.** Advisory only / no auto-trade — this review changes nothing in scoring, routing, or execution.
- US cash close (verified externally): S&P 500 7,691.76 (−0.69%), Nasdaq 26,289.71 (−1.33%), Dow 53,343.40 (−0.22%) — a **chip-led afternoon reversal** (SMH ≈ −5%, INTC/MU ≈ −6%, NVDA ≈ −2%) on rising yields (10y 4.70%, 30y ≈5.31%) and oil (Brent ≈$91). The desk's 22:58 EEST snapshot still labeled the regime **bullish** — the intraday reversal happened after that snapshot (see §11 TODO).
- Stocks A/B intraday: **0 actionable** all session — every A-tier candidate (AMGN, GILD, REGN, DXCM, XOM, COP, CMCSA, GE, INTU, BIIB, MA, ADBE, LLY, NFLX, CRM) was demoted to C by the rolling 7d drawdown guard (`stocks_intraday_7d_drawdown_guard`) or legal-risk gates (REGN, INTU). Guard is working as designed — it correctly kept the desk flat through a losing regime (A/B headline: winrate 13.8%, PF 0.125, totalR −3.5 this week).
- GE was the day's cleanest **realized** win: 3 A-tier intraday longs (99.7–100.0 score) all hit TP1 earlier today, before later-cycle GE signals got guard-demoted to C.
- Crypto: no A-tier active; 45 open B-tier swing/intraday/scalp positions, dominated by no-catalyst momentum longs (ACE, EDEN, GPS, BMT, HEMI). Swing mode remains the only crypto cohort with a real edge this week (PF 10.08, avgR +0.96); intraday and scalp are net-negative (PF 0.67 / 0.50) and short-direction is 0% winrate (n=6) — treat new crypto shorts with extra skepticism.
- Crypto macro: BTC ≈$64k, soft, Iran/Middle East stalemate cited as overhang; internal macro-risk score 100/100 risk-off-headwind from ETF outflow / exploit-hack headlines. Catalyst mapping is **weak this run (72.9% unmapped)** — treat the catalyst layer as context only.
- 3 untracked legacy crypto alerts recurring (HEMI×2, POL×1) — same known bug, still open, now flagged 5th+ consecutive cycle (§14 TODO-3, high priority).
- Overnight-into-Asia: no fresh crypto catalyst to lean on; carry-forward longs (EDEN, HEMI) unchanged; MMT/USDT stale short expires tomorrow 16:49 EEST unresolved.

## 2. Data Used
- Crypto reports: scalp `2026-08-18_17-11`, intraday `2026-08-18_17-28`, swing `2026-08-18_19-07` (latest cycle: 0 new A/B).
- Stocks: intraday `2026-08-18_19-58` (fresh, ~30 min old at run time). Stocks swing/invest reports are stale from 2026-07-02 (deprecated framework per project history — excluded from verdicts, planning-only if ever referenced).
- `data/catalysts/2026-08-18/` (catalyst_events.jsonl 2,944 rows, narrative_baskets.jsonl 2 rows, catalyst_cycle_17-37.md).
- `data/processed/llm_analysis_packet.md`, `llm_stocks_packet.md` (present, not deep-read line-by-line this cycle; superseded by fresher report sections above).
- CLI: `active-signals` (crypto=45, stocks=50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-18` (3 hits).
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_2139.md` (18:45→21:39 cycle) for §4 comparison.
- External (web unavailable was NOT the case — WebSearch/WebFetch worked): 2 WebSearch queries (US close, BTC/ETH price) + 1 WebFetch verification (Yahoo Finance market-close article, 403 on TheStreet — fell back to the working source). Sources ingested into `news_items` via the allowed CLI (crypto: 0 new rows, already present; stocks: 1 new row).

## 3. Scheduler / Data Freshness
- Latest scheduled-run folder: `data/scheduled_runs/2026-08-18_default_schedule/`.
- `scheduler.log` mtime ≈22:23 EEST (≈1h old at run time) — **fresh**, no defer needed.
- Latest `cycle_02_19-48_summary.md` mtime ≈22:23 EEST — fresh.
- Swing report (19:07 cycle / ~22:07 EEST): **fresh** (<4h).
- Stocks intraday report (19:58 UTC / ~22:58 EEST): **fresh** (<1h).
- Stocks swing/invest: **stale** (>14h, actually ~7 weeks old — deprecated per project history, excluded from verdicts).
- Monitor/paper status: not independently queried this cycle beyond the CLI outputs above (read-only tool budget kept to §A.4 allowlist).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-08-18 23:25 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["stocks_swing_invest_fresh_data"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime ~22:23 EEST", "stocks intraday report mtime ~22:58 EEST", "stocks swing/invest reports last generated 2026-07-02 (deprecated)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["mixed", "risk_off", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["S&P -0.69%, Nasdaq -1.33% at close (chip-led selloff)", "internal 22:58 EEST snapshot still read 'bullish', breadth 100% — stale by close", "BTC ~$64k soft, Iran/Middle East overhang", "internal macro risk score 100/100 risk-off headwind"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "stale_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 2944 total, 798 mapped, 2146 unmapped = 72.9% unmapped", "ACE/USDT momentum_breakout basket has no verified news catalyst", "perps_dex_narrative basket (HYPE primary) fresh <6h"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["funding_extreme", "data_unavailable"], "data_missing": ["OI_24h_for_most_symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE/USDT persistently negative funding despite +29% 24h move (elevated crowding)", "PORTAL/USDT price down + OI down = deleveraging/long liquidation", "EDEN/USDT OI +30% with price up = fresh trend positioning"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "clean_retest", "entry_late"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE/USDT +29-33% 24h, no-catalyst momentum cluster, chase risk flagged in its own playbook note", "EDEN/USDT RR to TP1 only 1.06R, thin", "MU/USDT semis short waiting_for_entry, thesis now confirmed by today's -6% Micron move"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 45 active B-tier signals, mostly triggered/tp_hit, 0 A-tier", "stocks: 0 A/B actionable this cycle, all demoted to C", "MMT/USDT triggered 6+ days unresolved, expires 2026-08-19T16:49 UTC tomorrow", "3 untracked legacy alerts (HEMI x2, POL x1), trackable=NO"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["daily_loss_pressure", "repeated_losses", "legal_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["stocks A/B headline this week: winrate 13.8%, PF 0.125, totalR -3.5", "REGN/INTU demoted to C on active legal/headline risk (class_action/securities_fraud)", "crypto direction=short bucket: 0% winrate, n=6, avgR -0.50 — do not lean on new crypto shorts", "stocks_intraday_7d_drawdown_guard is correctly blocking new A/B given the losing book"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing: PF 10.08, avgR +0.96, n=42 — working", "crypto intraday: PF 0.67, avgR -0.23, n=27 — failing", "crypto scalp: PF 0.50, avgR -0.05, n=13 — failing", "stocks tier=C watchlist: PF 0.57, winrate 8% — directionally decent this cycle on semis shorts (SMH/INTC/TSM/MU) but not actionable, no P&L captured"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of agents 1-8"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "EDEN/USDT", "trigger": "already filled 0.0500-0.0516 (open, RS-leader swing, playbook 14d WR72%/PF5.80); hold to TP1 0.0559 / invalidate on 1h close < 0.0460", "reason": "cleanest open crypto long — RS +7.5% vs BTC, OI +30% confirming fresh positioning, no fresh catalyst but momentum + swing-mode edge (PF10.08) backs it" },
    "best_short_candidate":    { "symbol": "MU", "trigger": "stocks C-tier, waiting_for_entry 927.66-936.93, invalidation 946.19 — semis-weakness thesis now confirmed by today's actual ~-6% Micron close; needs RTH confirmation tomorrow and a tier upgrade (currently NOT actionable, C-tier/gated) before it can be traded", "reason": "SMH was already flagged weakest sector pre-close; today's chip-led selloff (SMH -5%, INTC/MU -6%) validates the direction, but this signal is watchlist-only, not actionable" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "perps_dex_narrative basket primary, fresh <6h, playbook wait_pullback — needs a pullback confirmation before entry, not a chase", "reason": "only narrative basket with a real news trail (Hyperliquid/SEC pre-IPO perps headline) vs ACE/USDT's momentum_breakout basket which has zero verified catalyst" },
    "avoid_candidate":         { "symbol": "MMT/USDT", "reason": "B-tier swing short stuck 'triggered' 6+ days (opened 2026-08-12), no TP/stop hit, expires 2026-08-19T16:49 UTC tomorrow — stale, do not treat as a live idea without manual re-validation" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.75 | mixed, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, stale_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.40 | funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, clean_retest, entry_late | advisory_only |
| execution_lifecycle | caution | 0.70 | open_actionable, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | daily_loss_pressure, repeated_losses, legal_risk, manual_review | advisory_only |
| playbook_performance | ok | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (18:45→21:39 cycle)
- **Best long:** unchanged — EDEN/USDT still the pick, still open, thesis intact (no new price update this cycle; no fresher swing cycle re-listed it since it's already triggered).
- **Best short:** changed — prior review's AVGO short is not present in this cycle's active-signals output (stocks swing/invest is deprecated/stale, so it's carry-forward-only context, not re-verifiable via the current CLI). Replaced with MU/USDT (stocks C-tier semis short), now backed by today's realized close.
- **Best catalyst:** changed — prior pick ACE/USDT is downgraded this cycle (its momentum_breakout basket confirmed to have zero verified catalyst); replaced with HYPE/USDT (perps_dex_narrative, has an actual news trail).
- **Avoid:** unchanged — MMT/USDT, now one cycle closer to its tomorrow-16:49-UTC expiry, still unresolved.
- **New catalysts:** none material since 21:39 beyond the confirmed US chip-selloff close (external) and Iran/Middle-East BTC overhang (external).
- **Confirmed:** GE's earlier-session A-tier intraday longs all resolved tp1_hit (was already flagged as the day's cleanest stocks setup in the 21:39 review's underlying data; now fully realized/closed for the day).
- **Invalidated:** none of tonight's open positions hit invalidation levels since the last review, per the active-signals snapshot.

## 5. Catalyst Coverage
- Total catalyst_events today: **2,944**. Mapped (non-null symbol): **798**. Unmapped: **2,146** → **72.9% unmapped**.
- Narrative baskets: **2** (perps_dex_narrative primary HYPE/USDT; momentum_breakout primary ACE/USDT).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (noise pattern, unchanged from prior cycles): "Enginprime Medical Closes $12M Series A Financing"; "Greenberg Traurig's Marissa A. Neufeld Appointed to Miami Homes For All Board of Directors"; "Aastro Roofing Company Named Deerfield Beach's Roofer of the Year" — small-cap/local PR-newswire noise, not market-moving.
- This is the 5th+ consecutive cycle today flat at ~70-74% unmapped (see §14 TODO-2).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **mixed / risk-off leaning** — BTC ~$64k soft on Iran/Middle East overhang; internal macro risk score 100/100 risk-off-headwind (ETF outflows, exploit/hack headlines); but BTC/ETH trend labels in the swing report still read uptrend and altcoin breadth is ~48-52% (neutral, not broken).
- Stocks mood: **closed** (post-close). Session itself closed **risk-off in the final hours** — chip-led selloff (S&P -0.69%, Nasdaq -1.33%) despite an earlier-session bullish/high-breadth tape; VIX still low (15.68) so this reads as a sector rotation shock, not a broad risk-off panic.
- Dominant narrative: chip-sector weakness (SMH/INTC/MU/NVDA) into rising yields + oil, vs. crypto's momentum-cluster (ACE) and perps-DEX narrative (HYPE) with essentially no macro catalyst tailwind.
- Preferred side now: **mixed / wait-for-trigger** — crypto: lean longs only in swing mode with RS+catalyst backing (swing is the only edge-positive cohort this week); stocks: no live session until tomorrow's open, but semis-short thesis is now technically confirmed for tomorrow's RTH watch.
- Best long candidate: **EDEN/USDT** (open, hold — see §3A).
- Best short candidate: **MU** (stocks, watchlist-only, needs RTH confirmation and a tier upgrade before actionable — see §3A).
- Best catalyst-backed candidate: **HYPE/USDT** (perps_dex_narrative, wait for pullback — see §3A).
- What to avoid: **MMT/USDT** (stale 6+ day short); new crypto shorts generally (0% winrate this week, n=6); chasing ACE/USDT at +29-33% 24h with no verified catalyst; any stocks A-tier name still sitting in the §7 C-tier watchlist list — all correctly gated by the 7d drawdown guard, do not override.
- What would change the view: a confirmed pullback/retest on EDEN or HYPE before adding size; RTH confirmation of chip weakness tomorrow before treating MU as tradeable; the stocks_intraday_7d_drawdown_guard rolling off its 7d/14d lookback with a cleaner forward sample before A/B reopens.

## 7. Candidate Deep Dives

### 7.1 EDEN/USDT (crypto swing, B-tier, score 73.2, OPEN actionable)
- Filled zone 0.0500-0.0516 (per 14:39 cycle report); invalidation 1h close < 0.0460; TP1 0.0559 / TP2 0.0595 / TP3 0.0631 (RR to TP1 only ~1.06R — thin, size accordingly).
- RS vs BTC +7.5%, OI +30% with price up (fresh positioning, not a stale extension), funding negative (shorts crowded, mild tailwind for continuation).
- No fresh verified catalyst — pure RS/momentum thesis, playbook `crypto_swing_narrative_rs_momentum` (14d WR 72% / PF 5.80, the desk's strongest crypto cohort).
- Has price already reacted? Yes, entry already filled — this is a hold/monitor, not a fresh entry decision.
- Chase risk: low at current levels (entry already inside plan, not chasing the extension).
- Would invalidate: 1h close below 0.0460, or BTC breaking down against the swing-longs thesis broadly.
- Aligned with market mood: yes, provided BTC holds — crypto mood is mixed-not-broken, and swing is the edge-positive mode.

### 7.2 GE (stocks, was A-tier 94-100, demoted to C, CLOSED WIN today / no longer actionable)
- 3 intraday A-tier longs today (99.7, 100.0, 100.0 score) all **CLOSED WIN — TP1 hit** between 14:07-14:16 UTC.
- Later-cycle GE candidates (score 94) were then demoted A→C by `stocks_intraday_7d_drawdown_guard` + `stocks_intraday_long_guard` — the guard correctly stopped chasing more GE size after the cohort's rolling 7d/14d/30d numbers stayed net-negative overall, even though GE itself worked today.
- Production risk warning present: `GE [geopolitical_risk]: risk_warning` — actually a **defense-contract win** (Kratos/GE Aerospace GEK800 engine, USAF EMD contract) mis-tagged as geopolitical_risk rather than a bullish catalyst; likely a classifier miscategorization, not a real risk (see §14 TODO-6).
- Lifecycle status: CLOSED WIN, no live exposure into the overnight/tomorrow session.

### 7.3 MU (stocks, C-tier watchlist, score 60.2, short, WAITING for entry — NOT actionable)
- Entry 927.66-936.93, invalidation 946.19, direction short, semis thesis.
- Has price already reacted to the catalyst? Partially — today's close confirmed the semis-weakness direction externally (Micron ≈ -6% into the close per verified market-close reporting), but this specific signal is still only watchlist/C-tier, not Telegram-actionable, and needs RTH confirmation tomorrow before it can be treated as live.
- Chase risk: low if confirmed at/above the stated entry zone tomorrow; high if chasing further downside gap without a retest.
- Not aligned to trade tonight (market closed); aligned to watch into tomorrow's RTH open.

### 7.4 MMT/USDT (crypto swing, B-tier, score 65.6, short, TRIGGERED/STALE — avoid)
- Triggered since 2026-08-12, still unresolved after 6+ days, expires 2026-08-19T16:49 UTC (tomorrow).
- Not re-evaluated in any of tonight's scalp/intraday/swing reports.
- Direction=short crypto bucket is 0% winrate (n=6) this week — no reason to treat this as a fresh idea even if it were still fresh.
- Recommended handling: let it expire naturally per the monitor; do not manually re-enter or extend.

### 7.5 System integrity — 3 untracked legacy crypto alerts (HEMI×2, POL×1)
- `detect_untracked_legacy_alerts --since 2026-08-18`: HEMI/USDT (08:52, 12:02 UTC), POL/USDT (17:28:45 UTC) — all `trackable=NO`, no matching `proposed_signal` within ±6h.
- Same 3 rows as the 21:39 review (no new occurrences since, but none resolved either) — recurring known bug (watchlist re-fire reusing a stale/closed signal_id instead of minting a new `proposed_signal`; see project memory on the ALLO/BANK/HEMI/POL pattern).
- Effect: these 3 alerts were pushed to Telegram but will not contribute to PF/winrate/avgR tracking — an under-count of today's real alert volume, not a live-risk issue.

## 8. Best Candidates Ranked
1. **EDEN/USDT** — long, OPEN actionable, hold to TP1 0.0559 / invalidate < 0.0460.
2. **HYPE/USDT** — catalyst-watch, perps_dex_narrative, wait for pullback confirmation before entry.
3. **MU** — short-watch, needs RTH confirmation tomorrow + tier upgrade before actionable; direction now backed by today's realized chip selloff.
4. **GE** — closed win today, no live entry; watch for a cleaner re-set once the drawdown guard's forward window improves.
(If none of the above satisfy: no clean fresh entry exists tonight — crypto is post-close-adjacent (24/7 but thin liquidity into Asia), stocks are closed. Best posture is watch/hold, not chase.)

## 9. Avoid / No Trade (this decision window only)
- **MMT/USDT** — stale 6-day short, let expire, do not extend.
- **New crypto shorts generally** — 0% winrate this week (n=6); only take with exceptional confirmation.
- **Chasing ACE/USDT** at +29-33% 24h — no verified catalyst, funding persistently negative (crowded), known chase-risk failure mode flagged in its own playbook.
- **Any stocks A-tier name still gated to C** (AMGN, GILD, REGN, DXCM, XOM, COP, CMCSA, GE, INTU, BIIB, MA, ADBE, LLY, NFLX, CRM) — correctly held back by the rolling drawdown guard; do not override manually.
- This is a decision-window call only. Scanning, tracking, and data collection continue uninterrupted in all cases — nothing here is a command to pause the system.

## 10. Main Risks
- **Regime-label lag:** the 22:58 EEST stocks snapshot read "bullish" with 100% breadth; the actual close 1-2h later reversed on a chip-sector selloff. The label wasn't wrong at the time it was generated, but a review consuming only that snapshot without the external close check would have missed the reversal (see §14 TODO-6... actually TODO-7 below).
- **Stocks A/B book is in a real drawdown:** week-level winrate 13.8%, PF 0.125, totalR -3.5 — the guard is doing its job, but this is not a "we're being overly cautious" situation; it's a genuinely weak recent sample.
- **Crypto intraday/scalp modes net-negative this week** (PF 0.67 / 0.50) — only swing has a real edge; avoid over-weighting intraday/scalp signals in the 45-position open book.
- **Catalyst layer unreliable this run** (72.9% unmapped) — do not lean on catalyst tags for conviction tonight.
- **MMT/USDT and the 3 untracked alerts** are low-materiality but recurring data-integrity gaps that compound review-to-review if not fixed upstream.

## 11. Action Plan — next 4 hours
1. Hold EDEN/USDT to plan (TP1 0.0559 / invalidate < 0.0460); no new size.
2. Watch HYPE/USDT for a pullback entry into the Asia session; do not chase the current level.
3. Do not add new crypto shorts overnight without exceptional confirmation (0% WR week-to-date).
4. Let MMT/USDT run to its natural 16:49 UTC tomorrow expiry; no manual intervention.
5. Pre-market tomorrow: re-check MU and the broader semis-short thesis against RTH price action before treating any semis short as actionable.
6. No scanner/monitor/scheduler changes — everything continues running as-is.

## 12. Final Verdict per Mode
- **Crypto swing:** watch/hold — only edge-positive cohort this week (PF 10.08); hold EDEN, watch HYPE for pullback.
- **Crypto intraday:** caution — net-negative this week (PF 0.67); no new entries recommended without RS-leader + catalyst confirmation.
- **Crypto scalp:** caution — net-negative this week (PF 0.50, n=13); low-conviction mode right now.
- **Stocks intraday:** no action — 0 actionable A/B, guard correctly flat; watch MU/semis-short thesis into tomorrow's RTH.
- **Stocks swing/invest:** not evaluated — deprecated/stale data source, planning-context only if ever revisited.

## 13. Sources
- [Stock market today: Dow, S&P 500, Nasdaq fall as chip stocks sell off, bond yields rattle markets](https://finance.yahoo.com/markets/live/stock-market-today-tuesday-august-18-dow-sp-500-nasdaq-080822735.html) — Yahoo Finance, 2026-08-18 (verified via WebFetch; closing levels S&P 7,691.76 −0.69%, Nasdaq 26,289.71 −1.33%, Dow 53,343.40 −0.22%; semis −5%, INTC/MU ≈−6%, NVDA ≈−2%, 10y yield 4.70%, Brent ≈$91).
- [Bitcoin and ethereum prices today, Tuesday, August 18, 2026: Crypto prices mixed as Iran stalemate continues](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-august-18-2026-crypto-prices-mixed-as-iran-stalemate-continues-155702632.html) — Yahoo Finance, 2026-08-18 (BTC ~$64k, soft; Iran/Middle East overhang cited).
- Internal: `data/reports/swing/2026-08-18_19-07_swing_report.md`, `data/reports/intraday/2026-08-18_17-28_intraday_report.md`, `data/reports/scalp/2026-08-18_17-11_scalp_report.md`, `data/reports/stocks/intraday/2026-08-18_19-58_stocks_intraday_report.md`, `data/catalysts/2026-08-18/catalyst_cycle_17-37.md`, `data/catalysts/2026-08-18/catalyst_events.jsonl`, `data/catalysts/2026-08-18/narrative_baskets.jsonl`.
- Internal CLI: `active-signals` (crypto/stocks), `signal-stats` (crypto/stocks), `detect_untracked_legacy_alerts --since 2026-08-18`.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_2139.md`.

## 14. Fix Requests / TODO

### TODO-2 (carried forward, unchanged): Catalyst mapping stuck below 50%
- **issue:** catalyst symbol-mapping coverage is 72.9% unmapped (2146/2944), essentially flat vs. every cycle today (72.9-74%).
- **evidence:** `data/catalysts/2026-08-18/catalyst_events.jsonl` recount this cycle: 2944 total, 798 mapped, 2146 unmapped.
- **suggested manual fix:** filter obvious non-market PR-newswire noise (small-cap financings, board appointments, local business awards) out of the unmapped denominator, or improve the symbol resolver. Display-only diagnostic, no scoring risk in fixing it.
- **priority:** medium
- **first observed:** 2026-08-18 11:39 EEST (recurring — 5th+ consecutive cycle today at ~70-74% unmapped).

### TODO-3 (carried forward, unresolved): Untracked legacy crypto alerts recurring
- **issue:** `detect_untracked_legacy_alerts` still shows the same 3 rows from earlier today (HEMI/USDT ×2 at 08:52/12:02 UTC, POL/USDT ×1 at 17:28:45 UTC), `trackable=NO`. No new occurrences since 21:39 EEST, but also none resolved.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-18` — 3 rows.
- **suggested manual fix:** known bug (watchlist re-fire reuses a stale/closed signal_id instead of minting a new `proposed_signal`) — confirmed previously on ALLO/USDT, BANK/USDT, HEMI/USDT, now also POL/USDT. Escalate given continued recurrence across many review cycles.
- **priority:** high
- **first observed:** recurring, multiple prior cycles (see project memory `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug.md`).

### TODO-5 (carried forward, unresolved): MMT/USDT stale `triggered` signal
- **issue:** MMT/USDT B-tier swing short (`sig_6f5d3799c4e660c1`) has held `status='triggered'` since 2026-08-12T16:49:12 UTC — now 6+ days — without hitting TP or stop. Expires 2026-08-19T16:49 UTC (tomorrow afternoon).
- **evidence:** active-signals CLI, same signal_id, same entry/invalidation as the 21:39 review.
- **suggested manual fix:** audit whether the pending-monitor / outcome-resolution job is correctly polling old `triggered` swing signals for TP/stop hits, or whether this row is stuck due to a monitor gap; check for other similarly-aged `triggered` rows across symbols, not just MMT/USDT.
- **priority:** medium
- **first observed:** 2026-08-18 21:39 EEST.

### TODO-6 (NEW): GE geopolitical_risk tag likely mis-classifies a bullish defense-contract win
- **issue:** the production risk-warning block flags `GE [geopolitical_risk]: risk_warning — Kratos Defense & Security Solutions And GE Aerospace Announce That The GEK800 Engine Has Been Awarded A U.S. Air Force Contract`. This is a positive contract-award headline (defense_contract), not a geopolitical risk to GE — it reads like a classifier keyword-match (military/Air Force terms) mis-tagging a bullish catalyst as a risk warning.
- **evidence:** `data/reports/swing/2026-08-18_19-07_swing_report.md` §5c and `data/reports/stocks/intraday/2026-08-18_19-58_stocks_intraday_report.md` "Production risk warnings" section; cross-checked against `data/raw/enriched_review_sources/2026-08-18T08-39-00Z_stocks.json` which already correctly tags the same headline cluster as `defense_contract`/`primary_source`.
- **suggested manual fix:** review the geopolitical_risk classifier's keyword set for false-positives on defense-contract-award language (Air Force, military designation, EMD contract) vs. genuine geopolitical risk (sanctions, war, export controls).
- **priority:** low (display/advisory only, does not gate routing or execution)
- **first observed:** 2026-08-18 23:25 EEST.

### TODO-7 (NEW): Stocks regime label can go stale intraday near the close
- **issue:** the 19:58 UTC (22:58 EEST) stocks intraday report snapshot read regime "bullish" with 100% breadth above EMA20/50 and VIX 15.68. The actual 20:00 EST close (23:00 EEST), roughly 2 hours later, reversed on a chip-sector selloff (S&P -0.69%, Nasdaq -1.33%, SMH ≈-5%). The label was accurate when generated (mid-afternoon still bullish) but nothing in the pipeline re-flags a same-day regime reversal between the last intraday cycle and the close.
- **evidence:** internal report timestamp 19:58 UTC vs. externally verified close reporting (Yahoo Finance) showing the reversal happened after that snapshot.
- **suggested manual fix:** consider a lightweight last-30-minutes-of-session regime re-check (or at minimum, a "stale near close" flag) so a post-close review consuming only the last intraday cycle doesn't inherit a now-superseded bullish label without cross-checking an external close source, as this review had to do manually.
- **priority:** low (this review already caught and corrected it via external verification; not a live-trading impact since stocks were flat A/B all session anyway)
- **first observed:** 2026-08-18 23:25 EEST.
