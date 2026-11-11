# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:45 EEST

## 1. Executive Summary

**11:30 EEST slot — Europe / pre-US context.** Advisory only — no auto-trade, no code/scoring changes. Today is Saturday (2026-08-08) — **US stocks are closed**; all stock signals below are planning/watchlist context only, not actionable until Monday RTH. Crypto stays **bullish-trend / risk-on** on the desk's own regime read (BTC + ETH uptrend, breadth 66.7%/74.4% above EMA20/EMA50) and external sources confirm BTC holding ~$65k / ETH ~$1,900-1,930 on a dovish jobs-report tailwind — but the macro overlay is still pinned **100/100 risk-off** (Coldcard hardware-wallet exploit now confirmed >$130M across 5,200+ addresses, plus ongoing Ukraine/Hormuz geopolitical wires). Net call: **cautious risk-on**, technical + external price action outweighs the headline risk this cycle. **No A-tier signals** on either asset class. The **ZBT/ACE open-long-vs-bias-short contradiction** flagged in the 04:39 overnight review **persists** (STG/SYN have dropped off the weakest-symbols list, but ZBT and ACE are still open long swings tagged bias=short with negative 24h returns) — escalated to a standing TODO. Untracked-legacy-alert count is **0**. Catalyst mapping is **48.7% unmapped** (730/1500 today, cumulative across 3 cycles) — borderline under the 50% "weak" threshold for a second consecutive review, usable as context only.

## 2. Data Used

- `data/reports/scalp/2026-08-08_06-16_scalp_report.md` (gen 09:16 EEST) — ~2.5h old
- `data/reports/intraday/2026-08-08_06-24_intraday_report.md` (gen 09:24 EEST) — ~2.4h old, freshest report this cycle
- `data/reports/swing/2026-08-08_04-00_swing_report.md` (gen 07:00 EEST) — ~4.75h old, carry-forward bucket, flagged
- `data/reports/stocks/intraday/2026-08-07_20-57_stocks_intraday_report.md` (gen Aug 7 23:57 EEST) — market closed Saturday, planning-only
- `data/reports/stocks/swing/*`, `stocks/invest/*` — last generated 2026-07-02, retired/deprecated ([[project_crypto_ai_desk_stocks_position_framework]]), excluded
- `data/catalysts/2026-08-08/catalyst_events.jsonl` (1500 events cumulative), `narrative_baskets.jsonl` (6 baskets), `catalyst_cycle_06-31.md` (latest cycle, 09:31 EEST)
- `data/processed/llm_analysis_packet.md` (09:25 EEST), `data/processed/llm_stocks_packet.md` (00:02 EEST, weekend-stale — stocks planning-only anyway)
- `active-signals --asset-class crypto` (50 rows, all future expires_at) / `--asset-class stocks` (50 rows, mostly stale historical — see §14 TODO)
- `signal-stats --asset-class crypto` and `--asset-class stocks`
- `detect_untracked_legacy_alerts --since 2026-08-08` → 0 untracked
- `data/scheduled_runs/2026-08-07_default_schedule/cycle_04_09-07_summary.md` (mtime 09:54 EEST) — 42/42 steps `[OK]`, market intelligence health, latency SLA
- Direct read-only SQL on `db/crypto_ai_desk.sqlite` (`news_items`, 24h symbol lookups for ACE/BICO/EPIC/ZBT/STG/SYN)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-08_0439.md` (crypto overnight / Asia, 04:39 EEST)
- 2 WebSearch queries (BTC/ETH price + macro context; Coldcard exploit follow-up) — both used, no WebFetch needed (search snippets were sufficiently sourced and dated)

External web research **was** available this cycle.

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-08-07_default_schedule/scheduler.log` — mtime **Aug 8 09:54 EEST** (~1h50m old at review start) → **fresh**, well under the 3h defer threshold.
- Latest cycle summary `cycle_04_09-07_summary.md` (mtime 09:54 EEST) — all 42 steps `[OK]`, exit=0. No step failures.
- Crypto scalp report: 09:16 EEST → fresh (~2.5h old).
- Crypto intraday report: 09:24 EEST → fresh, freshest this cycle.
- Crypto swing report: 07:00 EEST, ~4.75h old → carry-forward bucket (4-12h); regime read cross-checked against fresher scalp/intraday — consistent (bullish trend, uptrend BTC/ETH both times).
- Stocks intraday report: Aug 7 23:57 EEST, ~12h old → stale relative to now but market is closed (Saturday) — used as planning/watchlist context only, not a data-quality failure.
- Stocks swing/invest: retired since 2026-07-02 — excluded by design, not a freshness problem.
- Market intelligence health (06:47 UTC run): `status: ok`, 0 issues; cross-exchange quotes, Deribit DVOL, SEC Form4 all `ok`.
- Latency: crypto acceptance = **SLA_BREACH** (detect p90 5137.5s > 180s threshold), stocks intraday acceptance = **SLA_BREACH** (fast-source share 12% < 80%, provider yfinance, BLOCKED_NOT_LIVE_GRADE) — both standing issues under [[project_crypto_ai_desk_latency_layer]], not new this cycle.
- Paper portfolio ledger refresh: `[OK]`, 3336 scanned/written, 2910 resolved, 0 errors; 796 deduped actionable paper trades this run.
- Monitors: crypto watchlist monitor, crypto pending monitor, MEXC canary monitor, derivatives monitor, fast Finnhub news monitor, telegram dashboard callbacks all `[OK]` / continuous-background this cycle.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-08 11:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~1h50m old, cycle_04 all 42 steps OK", "swing report ~4.75h old (carry-forward, cross-checked consistent)", "market intelligence health status=ok, 0 issues", "paper portfolio ledger refresh OK, 0 errors"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC+ETH uptrend, breadth 66.7%/74.4% above EMA20/50", "macro risk score 100/100 risk-off overlay (Coldcard exploit >$130M confirmed, Ukraine/Hormuz geopolitical wires)", "WebSearch confirms BTC ~$65k / ETH ~$1,900-1,930, firm on dovish jobs-report tailwind", "stocks closed (Saturday) — no US-session risk signal yet"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 51.3% mapped / 48.7% unmapped (770/1500 today, cumulative) — borderline under 50% weak threshold for 2nd consecutive review", "6 active narrative baskets: perps_dex, delisting_thin_liquidity (BONK), binance_ecosystem_teaser (BNB/ASTER), ai_narrative, rwa_narrative (ONDO/XLM), momentum_breakout (MMT, fresh <1h)", "ACE/BICO/EPIC/ZBT/SYN: 0 fresh (24h) news_items rows each — pure technical/momentum, no catalyst"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["oi_contradicts", "data_unavailable", "squeeze_risk"], "data_missing": ["OI 24h% n/a for most active symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BICO/USDT negative funding across bybit/okx/mexc despite long-biased report placement", "ALLO/USDT price up + OI down = short covering, weaker continuation quality", "no fresh derivatives data for ZBT/ACE this cycle"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "overextended"], "data_missing": ["TradingView / manual chart check unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BICO/EPIC/TUT/TST/MMT 24h moves of 26-48% already triggered — chase risk on fresh entries", "BICO highest swing score (79.5) among active B-tier, no bias-short conflict", "ACE (score 79.3/68.5) and STO (78.1) are the next-highest scoring but both carry-forward, ACE flagged for contradiction"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 50 rows, all future expires_at, 0 A-tier, all B-tier; ~34 triggered, 3 waiting_for_entry, ~13 tp1/tp2_hit (partial wins in progress)", "stocks active-signals: 50 rows, only 8 with today's expiry (C-tier, market closed), remainder carry stale historical expires_at back to 2026-07-03 — flagged as data-quality TODO", "detect_untracked_legacy_alerts: 0 today"] },
    { "agent": "risk_manager", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": ["correlation_cluster", "reduce_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZBT/USDT (2 open swing longs) and ACE/USDT (2 open swing longs) both tagged bias=short with negative 24h (-23.67%, -19.02%) in the freshest intraday scan — persistent contradiction cluster from the 04:39 review, now a 2-symbol recurring pattern (STG/SYN dropped off the weak-list this cycle)", "crypto scalp mode still structurally losing (PF 0.17, 1W/4L, avgR -0.083, n=40, standing kill-switch candidate)", "weekend-mode signals underperform (PF 0.65, winrate 12%, n=38, system observation)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing mode: PF 4.72, 13W/11L, avgR +0.38 (n=63) — working edge this week", "crypto intraday mode: PF 1.42, 14W/35L, avgR +0.19 (n=76) — moderate, winrate 16% system-flagged 'low'", "crypto scalp mode: PF 0.17, 1W/4L, avgR -0.083 (n=40) — structurally losing, standing kill-switch candidate", "stocks all-tier: n=448, PF 0.17, avgR -0.23, totalR -10 — known issue, C-tier never actionable per [[project_crypto_ai_desk_stocks_intraday_hardening]]"] },
    { "agent": "head_trader", "verdict": "ok",
      "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents below"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "BICO/USDT", "trigger": "already triggered across scalp/intraday/swing (highest active swing score 79.5); wait for pullback into 0.0587-0.0610 (intraday) / 0.0549-0.0572 (swing) zone with volume confirmation, do not chase the +47.7%/24h move" },
    "best_short_candidate":    { "symbol": "XRP/USDT", "trigger": "already-open swing short (tp1_hit, entry 1.0598-1.0610, invalidation 1.0626, expires 2026-08-08T18:02 UTC) — manage existing only; no fresh short setup scored this cycle, would need a confirmed breakdown/failed-bounce with volume" },
    "best_catalyst_candidate": { "symbol": "MMT/USDT", "trigger": "momentum_breakout basket (fresh <1h, +40.0% 24h, vol 1.3x) — no verified news catalyst, pure momentum cluster; wait for breakout retest before treating as actionable" },
    "avoid_candidate":         { "symbol": "ZBT/USDT, ACE/USDT (open swing longs)", "reason": "both tagged bias=short + negative 24h (-23.67%, -19.02%) in the freshest scan while desk holds open longs — persistent contradiction cluster, manual review before adding any risk" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | risk_on, longs_preferred, mixed | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | oi_contradicts, data_unavailable, squeeze_risk | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, overextended | advisory_only |
| execution_lifecycle | needs_review | 0.75 | open_actionable, waiting_for_entry, review_shadow | advisory_only |
| risk_manager | manual_review | 0.60 | correlation_cluster, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-08_0439.md` (crypto overnight / Asia, 04:39 EEST):

- **ZBT/ACE contradiction persists, STG/SYN improved.** The 04:39 review flagged a 3-symbol cluster (ZBT, STG, SYN) as open long swings tagged bias=short with negative 24h. This cycle's freshest intraday scan (09:24 EEST) no longer lists STG or SYN in the weakest-symbols section (may have stabilized — not confirmed, just absent from the extreme-movers list). **ZBT and ACE still persist**: ZBT improved from -42.8% to -23.67% 24h (still bias=short tag, still 2 open longs); **ACE is a new addition to the weak-list this cycle** (-19.02% 24h, also 2 open longs) — the cluster has rotated rather than resolved. Escalated to a standing TODO (§14).
- **Untracked legacy alerts: still 0.** Consistent with the last review; the prior TODO-3 recurrence (stale-signal reuse on watchlist re-fire) has not resurfaced in this or the prior cycle.
- **Coldcard exploit externally confirmed to have grown to >$130M** (from ~$116M at 04:39) across 5,200+ addresses per Forbes/TechCrunch/CBC reporting — but BTC price has stayed resilient (~$65k) per Yahoo Finance's Aug 7 update citing the weak July jobs report as a dovish Fed tailwind. Thesis not invalidated; risk overlay stays elevated.
- **Catalyst mapping**: 46.6% unmapped at 04:39 (233/500, single-cycle) vs **48.7% unmapped now** (730/1500, cumulative across 3 cycles today) — direction is flat/slightly worse, still under the 50% auto-trigger but worth watching for a third consecutive borderline reading.
- **Swing remains the working crypto edge** (PF 4.72 this window vs PF 5.46 at 04:39) — still the primary actionable lane; **scalp remains structurally losing** (PF 0.17, unchanged direction).
- **No new A-tier signals** on either asset class in either review.

## 5. Catalyst Coverage

- Total catalyst events today (cumulative, 3 cycles): **1500**
- Mapped (non-null symbol): **770** (51.3%)
- Unmapped: **730** (48.7%)
- Narrative baskets: **6** (perps_dex_narrative, delisting_thin_liquidity, binance_ecosystem_teaser, ai_narrative, rwa_narrative, momentum_breakout)
- Latest single cycle (`catalyst_cycle_06-31.md`, 500 events) by type: other_news 462, legal_risk 12, earnings_event 9, exploit_hack 5, partnership 5, regulatory_sector_headline 4, exchange_delisting 1, product_launch 1, platform_growth 1.
- 48.7% unmapped is **just under** the 50% "weak this run" threshold for a second consecutive review — usable as context, not a primary decision driver. Top unmapped headline samples:
  1. Tradfin geopolitical wire (Ukraine tanker attacks / Black Sea Kazakhstan oil terminal, no symbol resolver hit)
  2. "PNR Investors Have Opportunity to Lead Pentair plc Securities Fraud Lawsuit" (law-firm investor-alert prose-ticker format — same miss pattern flagged in the 04:39 review)
  3. "Ant Group's Ling 3.0 Flash packs 124B parameters..." (AI model news, no crypto/stock symbol expected)
  4. "Russia shuts down 9 crypto exchanges in major Moscow crackdown" (regulatory, no single symbol)
  5. "Why Redwire Stock Keeps Gaining" (stock ticker embedded in prose, resolver miss)

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **cautious risk-on** — BTC/ETH uptrend, breadth 66.7%/74.4% above EMA20/50, external sources confirm BTC ~$65k / ETH ~$1,900-1,930 holding through the Coldcard exploit headlines on a dovish jobs-report tailwind. Macro risk overlay stays pinned 100/100 risk-off; technical + external price action wins the tiebreak.
- Stocks mood: **closed (Saturday)** — all stock signals are planning/watchlist context only until Monday RTH; no fresh US pre-market data this cycle.
- Dominant narrative: RWA/tokenization (ONDO/XLM, multi-week thesis) remains the most durable basket; binance_ecosystem_teaser (BNB/ASTER, fresh <6h) and momentum_breakout (MMT, fresh <1h, pure momentum no catalyst) are the freshest.
- Preferred side now: **longs, selective** — prefer pullback/retest entries on RS-leaders; avoid chasing the 26-48% 24h movers already triggered (BICO/EPIC/TUT/TST/MMT).
- Best long candidate: **BICO/USDT** (highest active swing score 79.5, no bias-short conflict, appears across scalp/intraday/swing) — wait for pullback, not a chase.
- Best short candidate: **XRP/USDT** — the only currently-open short in the book (tp1_hit, invalidation 1.0626, expires today 18:02 UTC); manage existing, no fresh short setup scored this cycle.
- Best catalyst-backed candidate: **MMT/USDT** on the momentum_breakout basket (fresh <1h) — no verified news catalyst behind it, pure momentum; watch for retest confirmation.
- What to avoid: adding size to **ZBT/USDT and ACE/USDT** open longs while they carry a fresh bias=short + negative-24h tag; chasing any of the 26-48% 24h movers already triggered without a retest.
- What would change the view: a confirmed BTC breakdown below its current uptrend structure, a material escalation in Coldcard-exploit-driven exchange-level contagion (beyond self-custody), or ZBT/ACE breaking their swing invalidation levels (would convert the "contradiction" into a clean stop-out and resolve the ambiguity).

## 7. Candidate Deep Dives

### 1. ZBT/USDT — open swing longs vs. fresh short-bias tag (contradiction risk, manual review)
- Status: 2 open swing longs, both `triggered` (`sig_0be20040e229aec5` entry 0.1407-0.1491/inval 0.1253/exp 2026-08-14; `sig_66ffd2ccca900b8f` entry 0.1573-0.1626/inval 0.1510/exp 2026-08-13), plus 1 older scalp `tp1_hit`.
- Has price already reacted to a catalyst? No — 0 fresh (24h) `news_items` rows for ZBT. Pure technical divergence, not news-driven.
- Is the setup chasing? N/A — no new entry proposed, this is a hold-review.
- Aligned with market mood? No — mood is cautious risk-on/longs-preferred, but ZBT is now tagged bias=short with -23.67% 24h (improved from -42.8% at 04:39 but still negative and still tagged).
- Actionable now or wait? Do not add size. Watch for a break of the swing invalidation (0.1253 / 0.1510) which would resolve the contradiction into a clean stop-out, or a reversal back to bias=long which would validate holding.
- What invalidates: a confirmed close below 0.1253 (first entry's invalidation) triggers a stop; a reversal to bias=long with fresh volume would validate the existing longs.
- Chase risk: none (hold-only).
- Catalyst confirmation/contradiction: no catalyst either way — pure technical.

### 2. ACE/USDT — open swing longs vs. fresh short-bias tag (contradiction risk, manual review)
- Status: 2 open swing longs (`sig_9d70822c7254b39f` score 79.3, entry 0.1204-0.1284/inval 0.1106/exp 2026-08-14; `sig_cdf7e02cf2a4274c` score 68.5, entry 0.0977-0.1017/inval 0.0928/exp 2026-08-13).
- Has price already reacted to a catalyst? No — 0 fresh (24h) `news_items` rows for ACE.
- Is the setup chasing? N/A — hold-review, not a new entry.
- Aligned with market mood? No — ACE is newly tagged bias=short this cycle (-19.02% 24h, RS vs BTC -20.07%), a new addition to the contradiction cluster (was not flagged at 04:39).
- Actionable now or wait? Do not add size; treat as a manual-review hold. The intraday report's own deep-setup table shows ACE scored both `long` (catalyst_backed / momentum_7d_leader, score 68) and `short` (weak_rs_short, score 68) simultaneously — the signal itself is internally conflicted this cycle, not just vs. the open position.
- What invalidates: a confirmed close below 0.1106 (first entry's invalidation) or 0.0928 (second) triggers a stop.
- Chase risk: none (hold-only).
- Catalyst confirmation/contradiction: no catalyst either way — pure technical, and the technical read itself is split long/short in the same report.

### 3. BICO/USDT — best long candidate (momentum leader, no catalyst)
- Status: highest-scoring active B-tier signal today (swing score 79.5, `sig_fe17a18b8658e57a`, triggered, entry 0.0549-0.0572/inval 0.0520/exp 2026-08-14); also present in intraday (score 66.1) and scalp (score 68.0, tp1_hit) — consistent long bias across all three modes.
- Has price already reacted? Yes — +47.7% 24h / +420.67% 7d already realized; this is a continuation/pullback thesis, not a fresh breakout call.
- Is the setup chasing? Yes, if entered at current price (0.0620) rather than the planned pullback zone (0.0587-0.0610 intraday / 0.0549-0.0572 swing).
- Retest/pullback structure? The playbook explicitly calls for a pullback entry, not a market buy.
- Overextended? Current price 0.0620 vs support 0.0406 — well extended from recent base; RR to TP1 quoted at 1.84R only if entered in the pullback zone.
- Aligned with market mood? Yes — RS-leader long in a bullish-trend/risk-on tape, no bias-short conflict anywhere in today's reports.
- Actionable now or after confirmation? Wait for the pullback zone; do not chase the extended move.
- What invalidates: 1h close beyond 0.0560 (intraday) / 0.0520 (swing).
- Chase risk: **high** at current price — this is the core caution flagged by `technical_entry`.
- Catalyst confirmation/contradiction: no catalyst detected — pure momentum/RS thesis, consistent with the desk's own "no-catalyst intraday in chop is net-negative" playbook warning (applies less to swing mode, which is this week's working edge).

### 4. XRP/USDT — only open short in the book (manage existing)
- Status: 1 open swing short, `tp1_hit` (`sig_c1e2871dd5fcaf1a`, entry 1.0598-1.0610, invalidation 1.0626, expires **2026-08-08T18:02 UTC — today**, weekend-mode flagged).
- Has price already reacted? Partially — TP1 already hit, position is a partial win in progress.
- Is the setup chasing? N/A — no new entry, existing position.
- Retest/pullback structure? N/A for management; monitor whether price retests the 1.0598-1.0626 zone from below, which would be the key level to watch into the 18:02 UTC expiry.
- Aligned with market mood? Mixed — mood is longs-preferred overall, but this is the only short in the book and stats show short-direction sample is anecdotal (n=2, 0W/1L) — not enough data to draw a directional conclusion either way.
- Actionable now or wait? Manage existing only; this expires later today (before the 21:30 late-session slot) — flag for the next review to confirm resolution (win/loss/no further TP) rather than treating it as still "fresh."
- What invalidates: a confirmed break back above 1.0626.
- Chase risk: N/A (no new entry).
- Catalyst confirmation/contradiction: no XRP-specific catalyst found in the last 24h.

### 5. MMT/USDT — best catalyst-adjacent candidate (pure momentum, no verified news)
- Status: `momentum_breakout` narrative basket primary (fresh <1h per catalyst scan); active B-tier swing signal `sig_d2212817157a189f` (`waiting_for_entry`, score 65.3, entry 0.1960-0.1993/inval 0.1920/exp 2026-08-15); also appears in swing watchlist (score 54.9) and intraday strongest-symbols list (+40.05% 24h, RS vs BTC +39.0%, volume 1.3x — the only strongest-symbol with volume confirmation above 1x).
- Has price already reacted? Yes — the +40% move is already realized; the basket label itself says "top gainers without confirmed news catalyst — pure momentum cluster," i.e. this is not a real catalyst, just the closest thing to one this cycle.
- Is the setup chasing? Moderate — volume ratio 1.3x is the strongest confirmation of any active B-tier idea today, better than BICO/EPIC/TST's sub-0.3x ratios.
- Retest/pullback structure? Signal is `waiting_for_entry` at 0.1960-0.1993, below current levels — a genuine pullback-wait, not a chase-now setup.
- Overextended? Not verified via chart (TradingView unavailable) — rely on the waiting_for_entry zone as the discipline mechanism.
- Aligned with market mood? Yes — RS-leader long with the best volume confirmation in today's report set.
- Actionable now or after confirmation? Wait for price to reach the 0.1960-0.1993 entry zone; do not chase the current extended level.
- What invalidates: 1h close beyond 0.1920.
- Chase risk: moderate (mitigated by the waiting_for_entry structure).
- Catalyst confirmation/contradiction: no verified catalyst — label explicitly says "no confirmed news catalyst," included here only because it is the best-volume-confirmed momentum idea and the basket layer flagged it, not because it has real news backing.

## 8. Best Candidates Ranked

1. **BICO/USDT (long-watch)** — wait for pullback into 0.0587-0.0610 (intraday) / 0.0549-0.0572 (swing); highest active score (79.5), no bias-short conflict.
2. **MMT/USDT (catalyst/momentum-watch)** — wait for pullback into 0.1960-0.1993; best volume confirmation (1.3x) of any active idea, though explicitly no verified catalyst.
3. **XRP/USDT (short — manage existing)** — only open short in the book, tp1_hit, watch the 18:02 UTC expiry and the 1.0598-1.0626 retest zone.
4. **ZBT/USDT & ACE/USDT (manual review, avoid new size)** — contradiction cluster, do not add risk until resolved by a stop-out or a reversal to bias=long.
5. Excess B-tier ideas not deep-dived (score below the above and lower priority): TST/USDT (66.2, no-catalyst momentum, same known-failure-mode playbook as BICO/EPIC), EPIC/USDT (69.5-74.0 across modes, same pullback-only caution), HEI/USDT (65.2-69.9, same caution) — all long-only, no-catalyst, chase-risk-flagged; none scored high enough or carried enough differentiation to displace the five above.

## 9. Avoid / No Trade

This applies to the **current decision window only** — scanning, tracking, and monitoring continue uninterrupted regardless.

- **Do not add size to ZBT/USDT or ACE/USDT** open longs while they carry a fresh bias=short + negative-24h tag (contradiction cluster, §7.1-7.2).
- **Do not chase** BICO/EPIC/TUT/TST/MMT at current extended prices (26-48% 24h already realized) — wait for the stated pullback zones.
- **Do not treat any stock signal as actionable today** — market closed (Saturday); all 50 rows in `active-signals --asset-class stocks` are planning/watchlist context, and most carry stale historical expires_at (see §14 TODO).
- **Do not add new scalp-mode risk** — structurally losing this week (PF 0.17, 1W/4L, avgR -0.083); standing kill-switch candidate.

## 10. Main Risks

- **Macro/headline risk (100/100)**: Coldcard exploit now >$130M confirmed across 5,200+ addresses (externally verified); self-custody-specific so far, no confirmed exchange-level contagion, but a material escalation would flip the market-mood call.
- **Contradiction-cluster risk**: ZBT/ACE open longs vs. bias=short tags — if this converts into a genuine reversal rather than resolving via stop-out, it represents unrecognized directional risk on live positions.
- **Chase risk**: every currently-scored B-tier long (BICO, EPIC, TUT, TST, MMT) is already 26-48% into its move; entries above the stated pullback zones carry materially worse RR than reported.
- **Data-integrity risk**: `active-signals --asset-class stocks` mixes genuinely current rows with month-old expired records under the same "active" status — see §14 TODO; do not read stocks lifecycle status at face value without checking expires_at.
- **Standing latency risk**: crypto and stocks intraday both SLA_BREACH — general live promotion stays blocked (known, not new).

## 11. Action Plan — next 4 hours

- Watch BICO/USDT and MMT/USDT for pullback entries into their stated zones; do not chase.
- Watch ZBT/USDT (0.1253 / 0.1510) and ACE/USDT (0.1106 / 0.0928) invalidation levels — a break would resolve the contradiction into a clean stop-out; a bias flip back to long would validate the holds.
- Watch XRP/USDT into its 18:02 UTC expiry — confirm resolution (further TP, flat, or stop) by the next (18:30 US open reaction) review.
- No stock action expected before Monday RTH; use the remaining pre-US window to note any pre-market headlines for Monday's pre-US-open decision review.
- Continue monitoring the Coldcard exploit thread for any exchange-level contagion signal that would change the risk-off overlay from "self-custody-only" to "market-wide."

## 12. Final Verdict per Mode

- **Crypto scalp**: caution / near-avoid — structurally losing this week (PF 0.17), weekend-mode also underperforming; no new scalp risk recommended.
- **Crypto intraday**: caution — moderate edge (PF 1.42) but all active ideas are no-catalyst chase-risk longs already 26-48% extended; wait for pullback confirmation.
- **Crypto swing**: watch/selective-long — this week's working edge (PF 4.72); BICO/MMT are the cleanest pullback-watch candidates; ZBT/ACE need manual review before any further action.
- **Stocks (all modes)**: closed / planning-only — market shut for the weekend; C-tier signals are watchlist/research only per [[project_crypto_ai_desk_stocks_intraday_hardening]], not actionable regardless of day.

## 13. Sources

- [Bitcoin and ethereum prices today, Friday, August 7, 2026](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-august-7-2026-crypto-prices-moving-higher-following-july-jobs-report-131451960.html) — Yahoo Finance, 2026-08-07
- [Coldcard Bitcoin Exploit Balloons to $88 Million as Attackers Keep Draining Wallets](https://finance.yahoo.com/markets/crypto/articles/coldcard-bitcoin-exploit-balloons-88-171851804.html) — Yahoo Finance, 2026-08-04
- [Coldcard Hack: $116 Million Bitcoin Stolen Via Firmware Flaw](https://www.forbes.com/sites/boazsobrado/2026/08/04/i-did-everything-right-ai-warning-after-116-million-bitcoin-hack/) — Forbes, 2026-08-04
- [Hackers steal over $130M by exploiting bug in offline hardware wallets](https://techcrunch.com/2026/08/04/hackers-steal-over-130-million-by-exploiting-bug-in-offline-hardware-wallets/) — TechCrunch, 2026-08-04
- [What we know about ongoing Coldcard hack](https://www.cbc.ca/news/world/bitcoin-coinkite-security-hack-9.7295582) — CBC News, dated in-article
- Internal: `data/reports/scalp/2026-08-08_06-16_scalp_report.md`, `data/reports/intraday/2026-08-08_06-24_intraday_report.md`, `data/reports/swing/2026-08-08_04-00_swing_report.md`, `data/catalysts/2026-08-08/catalyst_cycle_06-31.md`

## 14. Fix Requests / TODO

### TODO-zbt-ace-contradiction
- **issue:** Open long swing signals on ZBT/USDT (×2) and ACE/USDT (×2) are simultaneously tagged `bias=short` with negative 24h returns in the freshest intraday scans, for a 2nd consecutive review cycle — the cluster composition rotated (STG/SYN dropped off, ACE newly added) rather than resolving.
- **evidence:** `active-signals --asset-class crypto` rows `sig_0be20040e229aec5`, `sig_66ffd2ccca900b8f` (ZBT), `sig_9d70822c7254b39f`, `sig_cdf7e02cf2a4274c` (ACE); `data/reports/intraday/2026-08-08_06-24_intraday_report.md` §2 "Weakest Symbols" and §6 deep-setup table (ACE scored both long and short simultaneously in the same report).
- **suggested manual fix:** Investigate whether the bias-tagging logic and the open-signal-hold logic are reading from different lookback windows, causing a fresh bearish tag to coexist with an untouched bullish position; consider whether a bias-flip should trigger an automatic manual-review flag on open positions.
- **priority:** medium (escalate to high if a 3rd consecutive cycle recurs with the same or an expanding symbol set).
- **first observed:** 2026-08-08 04:39 EEST (as a 3-symbol cluster: ZBT/STG/SYN); this run confirms persistence with a rotated composition.

### TODO-stocks-active-signals-stale-expiry
- **issue:** `active-signals --asset-class stocks` returns rows with `expires_at` as old as 2026-07-03 alongside genuinely current rows (only 8 of 50 rows have today's expiry), making the command's "active" framing misleading for operator review.
- **evidence:** CLI output this run — e.g. `sig_2c5873419dacc630` (COIN, expires 2026-07-03T22:37:08) and `sig_4a4a37d95e64761f` (JPM invest, expires 2026-07-31T03:11:54) both listed alongside `sig_1e8478376601bc25` (CRWD, expires 2026-08-08T15:41:58).
- **suggested manual fix:** Add an `expires_at >= now` filter to `active-signals` by default (or add an explicit `--include-expired` flag for historical review use cases).
- **priority:** low/medium.
- **first observed:** 2026-08-08 11:45 EEST (this run).

### TODO-catalyst-mapping-borderline
- **issue:** Catalyst symbol-mapping unmapped share has sat just under the 50% "weak" auto-trigger threshold for 2 consecutive reviews (46.6% at 04:39, 48.7% now).
- **evidence:** `data/catalysts/2026-08-08/catalyst_events.jsonl` (1500 events, 730 unmapped); recurring miss patterns: law-firm investor-alert prose tickers ("PNR Investors...", "Futu Shareholder Alert...") and geopolitical/tradfin wires with no single-symbol hit.
- **suggested manual fix:** Review the symbol resolver for the investor-alert-prose pattern specifically (a common recurring headline template from PR Newswire) as a targeted, low-effort mapping win.
- **priority:** low.
- **first observed:** 2026-08-07 (recurring; explicitly noted 2026-08-08 04:39 and 11:45).

### TODO-scalp-kill-switch
- **issue:** Crypto scalp mode remains structurally negative this week (PF 0.17, 1W/4L, avgR -0.083, n=40) — standing candidate for a pause/kill-switch discussion, unchanged across recent reviews.
- **evidence:** `signal-stats --asset-class crypto` this run, "By mode" table, `mode=scalp`.
- **suggested manual fix:** Human-driven review of whether scalp mode should be paused pending a strategy fix, consistent with prior reviews' standing note.
- **priority:** medium.
- **first observed:** prior to 2026-08-07 (recurring; re-confirmed this run).
