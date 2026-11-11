# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (target 04:30 EEST; actual data-gathering window ~04:39-04:46 EEST, Δ+9-16min, within tolerance). **Advisory only — no auto-trade.** Stocks are closed at this hour — all stock signals are C-tier planning/watchlist only, not actionable until the RTH open (~16:30 EEST). Crypto is the live actionable class this slot. **Zero A-tier setups across all three crypto streams** (scalp/intraday/swing all show "No A-tier setups found"), and crypto scalp mode itself is disabled by kill-switch (config, not a bug) — data collection only. The desk is carrying a large open **long-only book**: 25 active B-tier crypto positions (all `triggered`/`waiting_for_entry`, all long, split across scalp/intraday/swing) — **no active short exposure anywhere in the book**. Market mood is genuinely **mixed/divergent**: BTC/ETH both uptrend, altcoin breadth 55-58% above EMA20 (bullish tape), while macro/geopolitical risk stays pinned at 93-100/100 for a sixth+ consecutive review (Iran/Strait-of-Hormuz, Houthi attacks, Ukraine drone strikes on Russian oil infrastructure) — a bullish tape sitting on a risk-off macro backdrop. **EPIC/USDT's OHLCV-gap-driven status desync is now unresolved for a fourth+ consecutive cycle** (18:48→21:46→23:15→04:39) — `signal_outcomes` still logging `candles=0` with an internal `final_outcome=expired` that never propagates to the master `triggered` status; needs a human session, not another review re-confirming it. **Good news this cycle**: the stale non-terminal signals backlog dropped sharply — 10 stocks / 0 crypto signals now sitting >7d past `expires_at`, down from 46 stocks / 16 crypto in the last review — and zero untracked legacy crypto alerts today (vs 13 at yesterday's close). The `binance_ecosystem_teaser` catalyst basket (BNB, zero-entry all of yesterday) has also dropped out of today's basket list entirely. Catalyst mapping: 43.0% unmapped today (285/500 mapped) — under the 50% "weak" threshold, healthy. Three baskets active: `perps_dex_narrative` (HYPE, `wait_pullback`), `rwa_narrative` (ONDO/XLM, `related_beta_rotation`), `momentum_breakout` (ZBT, `avoid_chase`, flagged overextended).

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-07_01-36_scalp_report.md` (generated 04:36:48 EEST, ~3min old, regime bullish trend/risk-on, **0 A-tier, 0 B-tier** — scalp mode kill-switched off across every candidate; best-scored ideas ZBT 76.0/BICO 71.9/ACE 68.0 all rejected on `crypto_scalp_disabled`), `data/reports/intraday/2026-08-06_22-46_intraday_report.md` (generated 01:46:14 EEST, ~2h53m old, regime bullish trend/risk-on, **0 A-tier, 6 B-tier**: ACE 67.1, CTSI 67.1, ADA 66.6, ZBT 66.1, BICO 66.1, HFT 66.1, all no-catalyst momentum/continuation, known failure mode "no-catalyst intraday in chop is net-negative — WR23%/PF0.70/-3R"), `data/reports/swing/2026-08-06_20-19_swing_report.md` (generated 23:19:11 EEST 08-06, **~5h20m old — carry-forward per freshness policy**, regime range/chop/neutral — notably diverges from the fresher scalp/intraday bullish-trend read; **0 A-tier, 0 B-tier**, 10 C-tier watchlist names topped by CTSI 60.0).
- Stocks: `data/reports/stocks/intraday/2026-08-06_23-15_stocks_intraday_report.md` (~5h27m old, market-closed planning-only banner; 0 A/B actionable — 9 raw A/B candidates demoted to C by the `market_closed_intraday_planning_only` gate, incl. MSFT raw-A 100.0 additionally hard-gated on standing `legal_risk: class_action,securities_fraud`, PLTR raw-A 98.33, XOM raw-A 92.28). Stocks swing/invest: last generated 2026-07-02, stale >1 month, excluded per standing deprecation policy (deprecated framework, per project history).
- `data/catalysts/2026-08-07/catalyst_events.jsonl` (freshly regenerated this cycle via the one allowed `catalyst-scan` CLI — today's folder did not exist yet; 500 events scanned, 285 mapped / 215 unmapped = **43.0% unmapped**, healthy, under the 50% weak-mapping threshold) and `narrative_baskets.jsonl` — 3 active baskets: `perps_dex_narrative` (HYPE primary, playbook `wait_pullback`, single_source, fresh<24h), `rwa_narrative` (ONDO/XLM primary, playbook `related_beta_rotation`, single_source, fresh<6h), `momentum_breakout` (ZBT primary, playbook `avoid_chase`, fresh<1h, `symbols_overextended: [ZBT/USDT]`).
- CLI: `active-signals --asset-class crypto` (50 rows) and direct DB query (25 active positions: `status IN triggered/waiting_for_entry`, all B-tier, **all long**, scores 65.3-78.1 — STO/USDT 78.1 highest); `active-signals --asset-class stocks` / direct DB query (40 rows, **all C-tier**, market-closed context; several legacy rows — AVGO/NVDA/GOOGL/LLY/SMH/SPY/AMZN/XLV/IWM/SMCI — carry `expires_at` from 2026-07-21 while still `status=triggered`, over 2 weeks stale, see §14); `signal-stats --asset-class crypto` (weekly tier B: n=125, PF≈2.9, avgR≈0.38, winrate 21.9%; one weak mode sub-cohort n=29 confidence=weak PF≈0.00 avgR negative — consistent with the disabled/weak scalp lane); `signal-stats --asset-class stocks` (weekly: n=245, only 99 triggered, 0 wins/6 losses, PF≈0.1x, totalR≈-5.0R — CLI flags tier=C winrate 0% and PF 0.17 below 0.8; C-tier only, never actionable, watchlist context); `detect_untracked_legacy_alerts --since 2026-08-07` (**0 untracked** — clean start to the day, down from 13 at yesterday's post-close).
- DB (read-only, `db/crypto_ai_desk.sqlite`): `proposed_signals`/`signal_outcomes` for `sig_f6259f2dfc6f2f63` (EPIC/USDT swing, `status=triggered`, last 5 `signal_outcomes` checks 01:43:06-01:44:06 UTC all `candles=0` / `final_outcome=expired` internally — unchanged pattern, 4th+ consecutive cycle); stale non-terminal backlog re-query (`expires_at` >7d past, still non-terminal): **10 stocks, 0 crypto** — down sharply from 46/16 at the last review; `news_items` scan for the last 5 hours (Pump.fun continuing to sell SOL for treasury, ~$807M cumulative; Ethereum leverage climbing to 0.65 with liquidation-cascade risk flagged; Japan FX intervention; Iran/Hormuz oil-supply headlines continuing — no fresh hack/listing/unlock beyond what the reports already carry).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_2315.md` (post-close final daily review, 23:15 EEST).
- **No external web research this cycle** — all flagged items (EPIC data-gap, MSFT legal gate, catalyst baskets) had sufficient fresh/consistent internal news, catalyst, and DB context; the missing-or-stale-internal trigger for external research (§G) was not met for any candidate this cycle.

## 3. Scheduler / Data Freshness

- Active scheduler folder: `data/scheduled_runs/2026-08-06_default_schedule/` — `scheduler.log` mtime 04:37 EEST (~2min old at check time), latest `cycle_02_01-28_summary.md` mtime 02:27 EEST (~2h12m old). Both well within the 3-hour defer threshold — **no defer triggered**.
- Crypto scalp ~3min old (freshest report of the day), intraday ~2h53m old — both fresh/current. Swing ~5h20m old — **carry-forward** per the 4-12h freshness band; its range/chop regime read is stale relative to the fresher bullish-trend scalp/intraday reports and should not be treated as the current regime.
- Stocks ~5h27m old, market-closed context — used for planning levels only, consistent with the report's own banner.
- Monitor/background processes confirmed live from the last completed cycle log: crypto watchlist monitor (5m cadence, pid 25528), crypto pending monitor (30s cadence, pid 21596), MEXC canary monitor (3s cadence, pid 7564) — all reported "already running," no restart needed. `track-signals (pre)` step from the last cycle: checked=216, tp_hits=135, stopped=0, expired=0 — consistent with a strongly bullish tracked book, no stop cascade.
- Data-quality anomalies this cycle: (1) **EPIC/USDT stop-breach/OHLCV-gap desync, still unresolved, 4th+ consecutive cycle** (§7/§14, carried from prior review); (2) **10 stale non-terminal stocks signals** (>7d past `expires_at`, still `triggered`/`waiting_for_entry`) — improved sharply from 46, but not fully cleared (§14); (3) swing report regime label (range/chop) now stale/contradicts the fresher bullish-trend scalp+intraday reads — a same-desk regime-label divergence worth watching into the next cycle, not yet a bug; (4) **resolved since last review**: 0 untracked legacy alerts (was 13), 0 crypto stale-backlog signals (was 16), `binance_ecosystem_teaser` basket (zero-entry all of yesterday) has dropped out of today's basket list.
- **TradingView / manual chart check unavailable** — no chart MCP loaded this cycle; all price-structure statements are from local OHLCV/ATR/EMA fields in the reports and DB.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-07 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["no fresh 1h OHLCV for EPIC/USDT (candles=0 on every recent tracker check, unchanged 4th+ cycle)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~2min old, latest cycle summary ~2h12m old — well within 3h defer threshold", "swing report ~5h20m old, carry-forward, regime label stale vs fresher scalp/intraday", "today's catalyst folder was missing and had to be regenerated via the one allowed catalyst-scan CLI", "EPIC/USDT signal_outcomes shows candles=0 on the last 5 consecutive checks, unchanged pattern from 3 prior reviews"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mixed", "longs_preferred", "risk_off"],
      "data_missing": ["no live intraday BTC/ETH tick beyond internal reports"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Scalp+intraday (freshest reports): BTC/ETH uptrend, altcoin breadth 55.6-58.1% above EMA20, 60-67% above EMA50 — genuinely bullish tape", "Swing (stale ~5h20m): range/chop/neutral — likely outdated, not the current regime", "Macro/geopolitics risk score pinned 93.4-100/100 for a 6th+ consecutive review — Iran/Hormuz, Houthi attack on Saudi Arabia, Ukraine drone strike on Russian refinery — a risk-off macro backdrop sitting under a bullish crypto tape, genuine divergence not a clean risk-on signal", "Active book is 100% long (25/25 positions), zero short exposure — consistent with the bullish tape but leaves the desk fully exposed if the macro risk converts into a spot selloff"] },
    { "agent": "catalyst_narrative", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["fresh_catalyst", "no_catalyst", "narrative_supported", "mapping_weak"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["43.0% unmapped today (215/500), healthy, under the 50% weak-mapping threshold", "3 active baskets: perps_dex_narrative (HYPE, wait_pullback, fresh<24h), rwa_narrative (ONDO/XLM, related_beta_rotation, fresh<6h), momentum_breakout (ZBT, avoid_chase, fresh<1h, symbols_overextended=[ZBT/USDT])", "All 6 current crypto B-tier setups (ACE/CTSI/ADA/ZBT/BICO/HFT) explicitly carry 'no fresh verified catalyst detected' and the known-failure-mode warning for no-catalyst intraday chop", "binance_ecosystem_teaser basket (BNB, zero-entry all of yesterday) has dropped out of today's basket list entirely — resolved, not carried forward as a TODO"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["funding_extreme", "squeeze_risk", "data_unavailable"],
      "data_missing": ["no OI% for several intraday MEXC-fallback symbols (ACE/CTSI/ZBT/BICO/HFT/HOME/MMT all show OI 24h n/a in the intraday report's derivatives table)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HFT/USDT: extreme positive funding vs long crowding flagged explicitly in the scalp report's rejected list ('extreme positive funding against long crowding')", "ACE/USDT: negative funding across external venues (bybit -0.0157, mexc -0.0146), crowding elevated/unknown — short-crowded funding under a long price move", "DODO/USDT and VIC/USDT (short candidates): both explicitly capped to C on short-squeeze risk (thin liquidity, high upper wick) — shorting either fights a bullish tape into a squeeze setup", "SKHYB/USDT: 8.83x unusual volume, short bias but capped to C on thin-liquidity squeeze risk"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "entry_fresh", "overextended", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZBT/USDT explicitly flagged symbols_overextended in the momentum_breakout basket and carries the avoid_chase playbook — do not chase the current print", "MMT/USDT (intraday, B-tier 67.4) and HOME/USDT (intraday, B-tier 67.3) both waiting_for_entry with defined pullback zones not yet filled — the cleanest genuine 'watch for trigger' setups this cycle", "HEI/USDT: weakest RS vs BTC across both scalp (-32.14%) and intraday (-22.38%) reports, consistently the desk's top short candidate by relative weakness, but needs the crypto_failed_bounce_short playbook's confirmation (bearish HTF structure + derivatives + clear stop above swing high) before it is actionable — not confirmed yet", "HYPE/USDT (perps_dex_narrative basket primary): playbook explicitly wait_pullback — not a chase entry as-is"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.65,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["25 active crypto B-tier positions, all OPEN actionable / holding (triggered or waiting_for_entry), all long, spanning scalp/intraday/swing modes — STO/USDT (78.1) highest-scored, carried since 2026-08-04", "EPIC/USDT swing (69.5): 4th+ consecutive cycle stuck status=triggered while internal signal_outcomes logs candles=0/final_outcome=expired that never propagates — genuinely NEEDS REVIEW, not a normal open position", "Stocks: 40 active C-tier rows, all planning-only (market closed); 10 of them are stale (>7d past expires_at, still triggered/waiting_for_entry) — NEEDS REVIEW as a data-hygiene item, not a live trading concern", "0 untracked legacy crypto alerts today — clean lifecycle tracking so far this cycle"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["manual_review", "reduce_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["100% of the active crypto book (25/25) is long with zero short hedge, against a macro risk score pinned 93-100/100 for 6+ consecutive reviews — a concentration/correlation risk if the geopolitical headline flow converts into a broad risk-off spot move", "EPIC/USDT: still triggered, still stuck on a confirmed OHLCV gap, 4th+ consecutive cycle unresolved — top standing data-integrity risk item", "MSFT (stocks) still hard-gated legal_risk (class_action, securities_fraud) — unchanged, consistent with prior reviews, correctly non-actionable regardless of its raw score", "10 stale non-terminal stocks signals >7d past expiry still sitting as triggered/waiting_for_entry — low live-risk since stocks are C-tier/non-actionable, but a data-hygiene item for §14"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly (tier B, n=125, reliable): PF≈2.9, avgR≈0.38, triggered winrate 21.9% — CLI flags winrate low despite positive PF, consistent pattern across recent reviews", "one crypto mode sub-cohort (n=29, confidence=weak) shows PF≈0.00/negative avgR — consistent with the scalp lane's known weak/disabled state (100% positive MFE but TP-horizon mismatch, PF 0.14 per the scalp report's own banner)", "stocks weekly (n=245, only 99 triggered): 0 wins/6 losses, PF≈0.1x, totalR≈-5.0R, tier=C only — CLI explicitly flags winrate 0% and PF 0.17 below 0.8; watchlist-only, no live-money impact but a standing weak-lane signal", "crypto B-tier swing/intraday no-catalyst playbook explicitly self-reports a known failure mode (WR23%/PF0.70/-3R over 14d) on every current B-tier idea — a structural edge weakness the desk already discloses, not a new finding"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.55,
      "reason_codes": ["longs_preferred", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["No A-tier anywhere; the desk's job this slot is holding the existing 25-position long book through the Asia session and watching for clean pullback fills, not chasing new no-catalyst B-tier momentum names", "MMT/USDT and HOME/USDT (both intraday, waiting_for_entry) are the cleanest genuine long-watch triggers — defined pullback zones, not yet filled", "HEI/USDT is the standout short-watch by relative weakness but needs failed-bounce confirmation before it is actionable — do not pre-empt the confirmation", "HYPE/USDT (perps_dex_narrative, wait_pullback) is the best catalyst-backed watch idea — a real narrative basket with a defined non-chase playbook, unlike the no-catalyst B-tier grind", "EPIC/USDT needs a human maintenance session for its data-gap desync, not another review cycle re-confirming the same finding — flagged again in §14", "Two genuine improvements to note: untracked alerts and the stale-signal backlog both dropped sharply since the last review — a data-hygiene win, not something to over-credit yet given only one cycle of confirmation"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.55,
    "preferred_side": "longs",
    "best_long_candidate": { "symbol": "MMT/USDT", "trigger": "fill into the defined pullback zone 0.171565-0.17422 (intraday B-tier 67.4, waiting_for_entry) with volume confirming on the retest; invalidation 1h close below 0.16832", "reason": "cleanest genuine not-yet-triggered long setup this cycle inside a bullish crypto tape; caveat — no-catalyst playbook, known 14d edge is weak (WR23%/PF0.70), size accordingly" },
    "best_short_candidate": { "symbol": "HEI/USDT", "trigger": "confirmed bearish HTF structure + derivatives data + a clear stop above the last swing high before entry — currently unconfirmed, do not pre-empt", "reason": "weakest relative strength vs BTC across both scalp (-32.1%) and intraday (-22.4%) reports, the desk's clearest short-bias name, but the crypto_failed_bounce_short playbook explicitly requires confirmation the setup does not yet have" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "perps_dex_narrative basket primary — wait for the basket's own wait_pullback confirmation rather than chasing the current print", "reason": "the only currently-active basket with a real multi-symbol narrative thesis and a defined non-chase playbook; fresher and better-sourced than the no-catalyst B-tier grind names" },
    "avoid_candidate": { "symbol": "DODO/USDT", "reason": "short-squeeze risk (thin liquidity, high upper wick) explicitly capped to C in the scalp report; shorting into a bullish tape here risks a squeeze, not an edge" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.65 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.55 | mixed, longs_preferred, risk_off | advisory_only |
| catalyst_narrative | ok | 0.60 | fresh_catalyst, no_catalyst, narrative_supported, mapping_weak | advisory_only |
| derivatives_squeeze | caution | 0.50 | funding_extreme, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, entry_fresh, overextended, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.65 | open_actionable, waiting_for_entry, needs_review, no_entry | advisory_only |
| risk_manager | caution | 0.60 | manual_review, reduce_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.55 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.55 | longs_preferred, wait_for_trigger, manual_review | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_2315.md` (post-close, 23:15 EEST):

- **New day, clean start**: untracked legacy crypto alerts reset to **0** (was 13, a 4th-consecutive-review escalation yesterday) — the day's new-alert count resets at day boundary, not evidence of a fix, but a clean start.
- **Improved**: stale non-terminal signal backlog dropped to **10 stocks / 0 crypto**, down from **46 stocks / 16 crypto** — a sharp, real improvement (not a day-boundary reset, this metric is a rolling >7d-past-expiry count).
- **Unchanged**: EPIC/USDT's OHLCV-gap desync — still `status=triggered`, still `candles=0` on every check, now a 4th+ consecutive cycle (18:48→21:46→23:15→04:39). Still needs a human session (§14).
- **Unchanged**: MSFT still hard-gated `legal_risk: class_action,securities_fraud` (raw score 100.0 this cycle) — correctly non-actionable, consistent across every recent review.
- **Changed**: catalyst baskets rotated — `binance_ecosystem_teaser` (BNB, zero-entry all of yesterday) has dropped out entirely; today's set is `perps_dex_narrative` (HYPE), `rwa_narrative` (ONDO/XLM, new), `momentum_breakout` (ZBT, was ACE at post-close — rotated again).
- **New this cycle**: swing report is now the stale stream (~5h20m old, carry-forward) with a regime label (range/chop) that visibly lags the fresher scalp/intraday bullish-trend read — worth confirming at the next Europe-slot review once a fresher swing report lands.
- Crypto book composition: STO/PUMP/CTSI-swing all remained `triggered`/open overnight as expected; the book has grown to 25 positions (from the prior review's smaller carried set) as several new intraday/swing longs (ADA, ZBT, MIRA, KITE, TUT, HOME, AEVO, FIDA, COTI, BABY, ZAMA, MMT, SYN, BIO, PUMP) triggered or were proposed overnight — still 100% long, no shorts added.

## 5. Catalyst Coverage

- Total `catalyst_events` today (freshly generated this cycle): **500**
- Mapped (non-null symbol): **285** (57.0%)
- Unmapped (null symbol): **215** (43.0%)
- `narrative_baskets`: **3** — `perps_dex_narrative` (HYPE primary, wait_pullback), `rwa_narrative` (ONDO/XLM primary, related_beta_rotation), `momentum_breakout` (ZBT primary, avoid_chase, overextended)
- 43.0% unmapped is **under** the 50% weak-mapping threshold — catalyst layer is usable as a decision input this cycle, not context-only. Sample unmapped headlines (mostly securities-fraud class-action boilerplate that legitimately has no single primary symbol, plus general macro): "Pomerantz Law Firm Announces the Filing of a Class Action Against Microvast Holdings, Inc...", "INVESTOR ALERT: Pomerantz Law Firm Reminds Investors... ZoomInfo Technologies...", "Stock Market Today, Aug. 6: SoundHound AI Surges 10% on Record Q2 Revenue...".

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed** — bullish price tape (BTC/ETH uptrend, 55-58% breadth above EMA20) sitting under a pinned risk-off macro backdrop (93-100/100 for 6+ consecutive reviews: Iran/Strait-of-Hormuz tension, Houthi attack on Saudi Arabia, Ukraine drone strike on a major Russian refinery). Treat as risk-on for entries but stay alert to a fast reversal if a macro headline lands.
- Stocks mood: **closed** — US cash session shut; all levels are pre-open planning context only, not actionable until ~16:30 EEST.
- Dominant narrative: no single dominant theme — three parallel baskets (perps/DEX, RWA/tokenization, pure momentum) plus a broad no-catalyst momentum grind across the B-tier book (ACE/CTSI/ADA/ZBT/BICO/HFT all self-flag "no fresh verified catalyst").
- Preferred side now: **longs**, selectively — the book is already 100% long with 25 open positions; new entries should be pullback fills only (MMT, HOME), not chases of the already-extended names (ZBT flagged overextended).
- Best long candidate: **MMT/USDT** — waiting_for_entry, pullback zone 0.171565-0.17422, not yet filled.
- Best short candidate: **none confirmed — trigger: HEI/USDT on a confirmed failed bounce** (bearish HTF structure + derivatives + stop above swing high; weakest RS in the tape but unconfirmed).
- Best catalyst-backed candidate: **HYPE/USDT** (perps_dex_narrative basket, wait_pullback).
- What to avoid: **DODO/USDT** and **VIC/USDT** shorts (both squeeze-risk-capped, fighting a bullish tape); chasing ZBT/USDT at the current extended print.
- What would change the view: a fresh macro risk-off headline converting into an actual BTC breakdown (would flip preferred side toward defensive/short); a swing-report refresh confirming bullish-trend regime (would strengthen the long bias); EPIC/USDT's OHLCV gap resolving (would clear the standing needs-review flag).

## 7. Candidate Deep Dives

### 7.1 MMT/USDT — LONG-WATCH

- Status: `waiting_for_entry` (intraday, B-tier 67.4, created 2026-08-07T00:41 UTC)
- Has price reacted to a catalyst? No — no fresh verified catalyst; pure momentum/RS setup (24h +9.6%, RS vs BTC +10%).
- Chasing? No — still waiting for the pullback zone (0.171565-0.17422); current tape has not filled it yet.
- Retest/pullback structure? Yes — that is the entire entry plan; watch for a clean retest with volume, not a market chase.
- Overextended (>2 ATR from EMA20)? Not flagged in the report.
- Would entry now be late? No — it hasn't triggered.
- Actionability level: watch only, no market entry until the zone is tagged with volume confirmation.
- Mood alignment: aligned — bullish crypto tape, selective-long routing.
- Long/short/wait: wait-for-trigger long.
- Invalidates if: 1h close beyond 0.16832, or if BTC breaks its local support (regime thesis).
- Chase risk: low, given the plan explicitly requires the pullback.
- Catalyst confirmation/contradiction: none either way — pure technical/momentum thesis, carries the desk's own disclosed known-failure-mode (no-catalyst intraday chop WR23%/PF0.70) — size small.

### 7.2 HEI/USDT — SHORT-WATCH (unconfirmed)

- Status: not an open signal — appears only in the "weakest symbols" / expansion-watchlist sections (`crypto_failed_bounce_short` playbook), consistently the desk's weakest RS name across both scalp (-32.14% vs BTC) and intraday (-22.38% vs BTC) reports.
- Has price reacted to a catalyst? No catalyst identified for HEI in either report — pure relative-weakness/technical read.
- Chasing? A short here without confirmation would be chasing weakness into a bullish tape — explicitly the playbook's own caution.
- Retest/pullback structure? Not yet established; the playbook requires a **failed bounce**, which has not been confirmed.
- Overextended? Not explicitly flagged, but the setup fights the broader bullish regime by construction.
- Would entry now be late/early? Too early — pre-confirmation.
- Actionability: **not actionable** — watch only, pending the exact promotion criteria the report itself states: "Confirm bearish HTF structure + derivatives data + clear stop above swing high; squeeze guard."
- Mood alignment: contrarian to the broader tape — only trade on strong individual confirmation, not as a market-mood-aligned idea.
- Long/short/wait: wait-for-trigger short.
- Invalidates if: HEI reclaims relative strength or the bounce holds instead of failing.
- Chase risk: high if entered without confirmation.
- Catalyst: none — technical-only thesis.

### 7.3 HYPE/USDT — CATALYST-WATCH

- Status: not an open `proposed_signal` — surfaces via the `perps_dex_narrative` basket (primary symbol), playbook `wait_pullback`, source single_source, fresh<24h.
- Has price reacted? Basket data does not show `symbols_moved` yet for HYPE specifically this cycle.
- Chasing? No — the basket's own suggested playbook is explicitly `wait_pullback`, not a market chase.
- Retest/pullback structure? That is the entry condition by design; no fill signal yet.
- Overextended? Not flagged for HYPE in `symbols_overextended` (only ZBT is flagged there).
- Actionability: watchlist/context only — no scored `proposed_signal` exists for HYPE this cycle, this is catalyst-basket surfacing, not a desk-scored trade idea.
- Mood alignment: aligned with a risk-on/selective-longs stance if/when it triggers.
- Long/short/wait: wait-for-trigger long (per basket playbook).
- Invalidates if: the basket loses freshness or HYPE breaks its structure decisively before a pullback forms.
- Catalyst confirmation: basket-level narrative confirmation (perps/DEX theme), not a single hard news item — treat as a soft catalyst.

### 7.4 EPIC/USDT — NEEDS REVIEW (data-integrity, not a trade idea)

- Status: `sig_f6259f2dfc6f2f63`, swing, score 69.5, `status=triggered`, entry 0.88456964-0.90522143, invalidation 0.85932857, created 2026-08-01, expires 2026-08-08.
- The last 5 `signal_outcomes` checks (01:43:06-01:44:06 UTC this cycle) all show `candles=0` on `binance/1h` with an internal `final_outcome=expired` in the notes that never propagates to the master `status` field — the position display-shows `triggered`/open but the underlying data feed for it has been dark for 4+ consecutive review cycles (18:48→21:46→23:15→04:39, spanning 2026-08-06 through 2026-08-07).
- This is **not** a trade recommendation of any kind — it is a standing data-integrity issue that keeps re-surfacing because the underlying pipeline bug has not been fixed (per the permission contract, this run cannot fix it — see §14).
- Actionability: N/A — flag for manual review, do not treat the displayed `triggered` status as trustworthy for this specific signal.

### 7.5 DODO/USDT — AVOID

- Status: not an open signal; appears in scalp report's rejected list, score 32.4 (short), explicitly capped to C on "short squeeze risk → capped to C: thin_liquidity_short_squeeze_risk, high_upper_wick_short_squeeze_risk (+exhaustion)".
- Has price reacted? Yes — 24h -25.64% to -26.60% across reports, already a large weak move.
- Chasing? A fresh short here would be chasing an already-large down move into thin liquidity — squeeze risk explicitly flagged by the desk's own gate.
- Retest/pullback structure? Not established for a clean short entry.
- Overextended? Yes, to the downside — high upper wick pattern flagged.
- Actionability: **avoid** — the desk's own risk gate already rejected this, no override warranted.
- Mood alignment: a short here also fights the broader bullish crypto tape — double-count of chase + squeeze risk.
- Invalidates the avoid-thesis if: liquidity improves and a clean failed-bounce structure forms with derivatives confirmation — not present now.

## 8. Best Candidates Ranked

1. **MMT/USDT** — best long-watch, wait for pullback fill 0.171565-0.17422.
2. **HYPE/USDT** — best catalyst-watch, wait for `wait_pullback` basket confirmation.
3. **HEI/USDT** — best short-watch, wait for confirmed failed bounce before any entry.
4. Hold: the existing 25-position long crypto book (STO/PUMP/CTSI/ADA/ZBT/MIRA/KITE/TUT/HOME/AEVO/FIDA/COTI/BABY/ZAMA/SYN/BIO and others) — no new action needed, monitor invalidations.
5. **EPIC/USDT** — needs review, not a trade candidate this cycle (data integrity).

No candidate this cycle clears the bar for an outright fresh actionable A/B call — the desk's job into the rest of the Asia session is holding the existing book and watching the three named triggers above, not forcing a new entry.

## 9. Avoid / No Trade

This applies to the current decision window only — scanning, tracking, and the scheduler continue unaffected.

- **DODO/USDT / VIC/USDT shorts** — squeeze risk, fighting a bullish tape.
- **ZBT/USDT fresh long entries at current print** — flagged overextended by its own catalyst basket (`avoid_chase`); the existing swing position (already `triggered`) is a hold, not a new-entry recommendation.
- **All stocks** — market closed, planning-only, not actionable until RTH.
- **MSFT (stocks)** — permanently legal-gated regardless of score; do not treat as promotable even after the open.
- **EPIC/USDT** — do not treat the displayed `triggered` status as a fresh trade signal given the confirmed data gap; existing holders should be aware the position's live-price tracking is unreliable right now.

## 10. Main Risks

- **Macro/crypto divergence**: risk-off geopolitical headline flow (93-100/100 for 6+ reviews) sitting under a fully bullish, 100%-long crypto book with zero short hedge — a real tail risk if any single headline (e.g., an actual Strait-of-Hormuz disruption event) converts into a fast de-risking move.
- **EPIC/USDT data-integrity**: 4th+ consecutive cycle with an unresolved OHLCV gap; the position's true state is unknown to the automated tracker.
- **No-catalyst B-tier concentration**: every current intraday B-tier idea (ACE/CTSI/ADA/ZBT/BICO/HFT) self-discloses the same weak no-catalyst-chop failure mode (WR23%/PF0.70/-3R) — the book's newest additions carry a known-weak edge, not a fresh strong one.
- **Stocks C-tier weak lane**: weekly PF≈0.1x / totalR≈-5.0R with 0 wins across 245 samples — watchlist-only, no live impact, but a standing pattern worth remembering when stocks reopen.
- **Stale-signal residue**: 10 stocks signals still >7d past expiry and non-terminal — down from 46, real progress, but not yet zero.

## 11. Action Plan — next 4 hours

- Hold the existing 25-position long crypto book; no new market entries.
- Watch MMT/USDT (0.171565-0.17422) and HOME/USDT intraday (0.00918361-0.00940957) pullback zones for clean fills with volume confirmation.
- Watch HYPE/USDT for a `wait_pullback` confirmation per the perps_dex_narrative basket.
- Watch HEI/USDT for a confirmed failed-bounce short setup; do not pre-empt.
- Do not add fresh exposure to ZBT/USDT at the current extended print.
- Monitor macro headline flow (Iran/Hormuz, Houthi, Ukraine) for any escalation that would flip the routing from selective-longs toward defensive.
- Carry EPIC/USDT and the 10 stale stocks signals forward as standing needs-review items into the 11:30 EEST Europe/pre-US context review; re-check whether a fresher swing report has landed by then to resolve the regime-label divergence noted in §3/§4.

## 12. Final Verdict per Mode

- **Crypto scalp**: kill-switched off (config, not a bug) — no trade, data collection only. Known weak edge (100% positive MFE but PF 0.14, TP-horizon mismatch) confirms the disable is appropriate.
- **Crypto intraday**: no A-tier; 6 no-catalyst B-tier ideas already largely triggered/held — watch-only for the 2 not-yet-filled (MMT, HOME), do not chase the rest.
- **Crypto swing**: report stale (~5h20m, carry-forward); no A-tier, 10 C-tier watchlist names; the desk's historically strongest bucket, currently holding a large triggered book — hold, no new action pending a fresher report.
- **Stocks intraday/swing/invest**: market closed — planning/watchlist only, all levels are pre-open context; re-evaluate at/after the 09:30 ET (~16:30 EEST) open.

## 13. Sources

All external context this cycle came from internal system data — no WebSearch/WebFetch was needed (§G threshold not met for any candidate). Internal sources cited above:

- `data/reports/scalp/2026-08-07_01-36_scalp_report.md`
- `data/reports/intraday/2026-08-06_22-46_intraday_report.md`
- `data/reports/swing/2026-08-06_20-19_swing_report.md`
- `data/reports/stocks/intraday/2026-08-06_23-15_stocks_intraday_report.md`
- `data/catalysts/2026-08-07/catalyst_events.jsonl`, `data/catalysts/2026-08-07/narrative_baskets.jsonl`
- `db/crypto_ai_desk.sqlite` — `proposed_signals`, `signal_outcomes`, `news_items` (read-only queries)
- `data/scheduled_runs/2026-08-06_default_schedule/scheduler.log`, `cycle_02_01-28_summary.md`
- `OPUS_ENRICHED_REVIEW_AUTO_2026-08-06_2315.md` (previous review, for §4 comparison)

## 14. Fix Requests / TODO

### TODO-epic-usdt-ohlcv-gap-confirmed (priority: high, unresolved — 4th+ consecutive cycle)
- **issue:** EPIC/USDT swing signal `sig_f6259f2dfc6f2f63` remains `status=triggered` while `signal_outcomes` logs `candles=0` on `binance/1h` for every check across 4+ consecutive review cycles (18:48, 21:46, 23:15 on 08-06, and 04:39 on 08-07), with an internal `final_outcome=expired` that never propagates to the master status.
- **evidence:** `SELECT * FROM signal_outcomes WHERE signal_id='sig_f6259f2dfc6f2f63' ORDER BY checked_at DESC LIMIT 5` — all rows `entry_triggered=1`, `notes` containing `candles=0` and `final_outcome=expired` embedded in the notes text, most recent checks 2026-08-07T01:43:06Z-01:44:06Z.
- **suggested manual fix:** investigate the OHLCV fetch path for EPIC/USDT on the `binance/1h` source for this specific signal_id; determine why the fetch returns 0 candles repeatedly and why the internal `final_outcome=expired` computed by the tracker does not propagate to `proposed_signals.status`. Likely a delisting/symbol-rename/thin-liquidity edge case on binance for EPIC/USDT worth checking directly.
- **priority:** high
- **first observed:** 2026-08-06 18:48 EEST (this is at least the 4th consecutive review flagging it)

### TODO-stale-nonterminal-stocks-signals (priority: medium, improved but not resolved)
- **issue:** 10 stocks `proposed_signals` remain `status IN (triggered, waiting_for_entry)` with `expires_at` more than 7 days in the past (several from 2026-07-20/21, e.g. AVGO, NVDA, GOOGL, LLY, SMH, SPY, AMZN, XLV, IWM, SMCI) — down sharply from 46 at the last review, but not yet zero.
- **evidence:** `SELECT asset_class, COUNT(*) FROM proposed_signals WHERE status IN ('open','waiting_for_entry','triggered') AND datetime(expires_at) < datetime('now','-7 days') GROUP BY asset_class` → `('stocks', 10)`, `('crypto', 0)`.
- **suggested manual fix:** run/verify the signal-lifecycle expiry sweep for stocks specifically — something is not transitioning these rows to a terminal state (`expired`/`no_entry`/etc.) even long after `expires_at` has passed. Confirm whether this is the same root cause as the EPIC/USDT desync (a broader status-propagation bug) or a separate stocks-specific gap.
- **priority:** medium
- **first observed:** 2026-08-06 (carried forward from prior review's 46-row count; recheck confirms real improvement, not resolution)

### TODO-swing-report-regime-label-lag (priority: low, new this cycle, observation only)
- **issue:** The freshest swing report (23:19 EEST 08-06, ~5h20m old at this review) labels the regime `range/chop (neutral)`, while both the fresher scalp (04:36 EEST) and intraday (01:46 EEST) reports label it `bullish trend (risk-on)` with 55-58% breadth above EMA20. This is very likely just the swing report being older (regime shifted since it ran), not a bug — but worth confirming once a fresher swing report lands, since a stale regime label could mislead the swing-mode desk notes if this widens.
- **evidence:** `data/reports/swing/2026-08-06_20-19_swing_report.md` line 32 (`Recommended trading style: mean reversion or wait for clean breakouts`, regime `range/chop`) vs `data/reports/scalp/2026-08-07_01-36_scalp_report.md` / `data/reports/intraday/2026-08-06_22-46_intraday_report.md` (both `bullish trend (risk-on)`).
- **suggested manual fix:** none required if this resolves naturally on the next swing report generation (next scheduled cycle); only escalate if the swing report's regime label continues to diverge from scalp/intraday for 2+ more consecutive reports.
- **priority:** low
- **first observed:** 2026-08-07 04:39 EEST
