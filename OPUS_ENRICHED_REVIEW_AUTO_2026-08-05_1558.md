# Opus Enriched Review — pre-US-open decision review — Auto Cycle 15:58 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (target 08:55 America/New_York / 15:55 EEST, fired ~15:58 EEST / ~08:58 ET). **Advisory only — no auto-trade.** US cash session has not yet opened (09:30 ET / 16:30 EEST) — every stocks row remains planning/watchlist context. Crypto regime **improved to bullish trend (risk-on)** this cycle (from "transition/mixed" at 11:39) — BTC uptrend, ETH transition_up, altcoin breadth 66.67% above EMA20/50. Zero A-tier anywhere, crypto or stocks. Five crypto B-tier signals fired/progressed in the last ~3h (TUT/USDT intraday brand-new at 16:03 EEST, FIDA/USDT and SYN/USDT intraday waiting_for_entry at 15:49 EEST, BICO/USDT scalp triggered at 15:34 EEST, PUMP/USDT intraday triggered at 12:58 EEST) — all in the desk's self-labeled worst sub-playbook (no-catalyst intraday momentum, 14d WR 23%/PF 0.70/−3R). **FIDA/USDT shows the same chase-flag/live-signal tension previously flagged for BICO/USDT (TODO-bico-chase-flag-recurrence)**: the 15:37 EEST intraday report's own funnel rejects FIDA at score 47.8 ("more than 2 ATR from EMA20, do not chase"), while a fresh B-tier signal (score 72.7, defined pullback entry, not yet filled) fired 12 minutes later — a third occurrence of this pattern, now on a second symbol, strengthening the case that this is systemic rather than symbol-specific (§14). **This run's new pre-US stocks overlay surfaced two hard-gate misses**: BAC (pre_gate_tier A, base_score 91.0) carries active Epstein-banking-scrutiny and OCC AML-penalty headline risk not caught by the code's exclusion list; SMCI (pre_gate_tier A, base_score **100.0** — itself a suspicious round number worth a scoring-anomaly TODO) carries an active DOJ investigation, auditor turnover, and heavy debt/cash-burn profile. Both are scored **BLOCK** in this review's manual verdict; the automated ingest that would persist these verdicts to the DB **failed twice with "database is locked"** (§3/§14) — the BLOCK is advisory-only in this file, not yet enforced in the pipeline. A separate internal contradiction: **HOME/USDT** appears simultaneously as one of today's weakest symbols (bias short, 24h −14.27%, RS vs BTC −15.07%) and carries three active **long** B-tier positions. Macro/geopolitics risk remains pinned at 100/100 risk-off. Catalyst→symbol mapping degraded further to **64.2% unmapped** (vs 60.8% at 11:39, 59.8% at 04:39) — a worsening trend, still over the 50% weak-mapping threshold. Premarket context (external): S&P futures +0.4%, Nasdaq 100 +0.4%, VIX ~17.9 (up from 16.50 at 11:39), Michael Burry 1987-crash-warning headlines circulating alongside yesterday's S&P close at a fresh ATH — a genuine bull/bear tension into the open. LLY and UBER report earnings today — do not chase either print. STO/USDT remains the cleanest open long, unchanged.

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-05_12-31_scalp_report.md` (~1h27m old at write time, fresh), `data/reports/intraday/2026-08-05_12-37_intraday_report.md` (~1h21m old, fresh, most current read this cycle), `data/reports/swing/2026-08-05_01-48_swing_report.md` (~14h10m old — **stale, borderline; used only for continuity context, excluded from fresh verdict**).
- Stocks: `data/reports/stocks/intraday/2026-08-05_10-06_stocks_intraday_report.md` (~5h52m old at write time, market was closed at generation — planning/watchlist only; superseded for this slot by the dedicated pre-US overlay below).
- `data/catalysts/2026-08-05/catalyst_events.jsonl` (2,500 rows scanned, 1,605 null-symbol), `narrative_baskets.jsonl` (4 baskets), `catalyst_cycle_12-42.md`.
- LLM packets: `data/processed/llm_analysis_packet.md` (~15:38 EEST), `data/processed/llm_stocks_packet.md` (~13:08 EEST, referenced for context only).
- CLI: `active-signals --asset-class crypto` (36 rows), `active-signals --asset-class stocks` (50 rows, all legacy/past-expiry), `signal-stats --asset-class crypto` (weekly), `signal-stats --asset-class stocks` (weekly), `detect_untracked_legacy_alerts --since 2026-08-05` (0 untracked).
- **Pre-US stocks overlay** (this slot only): `stocks-preus-candidates` → `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` (9 eligible, 31 excluded by hard gate); manual verdicts built and saved to `data/raw/enriched_review_sources/preus_review_2026-08-05T13-05.json`; `stocks-preus-review-ingest` attempted twice, **both failed** (`OperationalError: database is locked`) — verdicts below are advisory-only in this document, not yet persisted.
- DB (read-only queries): `proposed_signals` (created_at filter, last 3h — 5 fresh crypto rows), `news_items` (24h symbol-match check for AMAT/BAC/NFLX/IWM/DIA/SPY/MSTR/SMH/SMCI), `catalyst_events.jsonl` title-match for the same 9 symbols.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1139.md` (Europe / pre-US context, 11:39 EEST).
- **External web research invoked this cycle** (WebSearch ×4, no WebFetch — see §13): premarket S&P/VIX context, MSTR "Trump accounts" headline verification (unconfirmed by mainstream press — social/Telegram-only), SMCI current fundamentals/legal status, BAC current fundamentals/legal status. Used because the pre-US overlay's two highest raw-score candidates (BAC, SMCI) needed legal/headline verification beyond what the internal hard gate checks, per the overlay's explicit instruction to always call out legal/DOJ/going-concern risk.

## 3. Scheduler / Data Freshness

- **Pre-US schedule check: target 08:55 ET, actual fire ~08:58 ET (Δ+3min, within tolerance).** Nicosia-local cron 15:55 fired ~15:58 EEST; both zones observing summer DST (EDT/EEST) as of 2026-08-05, well outside the documented mismatch windows (2026-03-08→03-29, 2026-10-25→11-01) — no DST drift this run.
- `scheduler.log` mtime ~15:57 EEST (~1 min old at read time) — fresh, not deferred. Latest `cycle_06_12-29_summary.md` mtime ~16:22 EEST — fresh (<3h), not deferred.
- Crypto scalp ~1h27m old, intraday ~1h21m old — both fresh. Crypto swing ~14h10m old — **stale (>14h band)**, excluded from the fresh verdict per the freshness rule, used only for background continuity.
- Stocks intraday report ~5h52m old, market closed at generation time — superseded for this slot by the dedicated `stocks-preus-candidates` overlay (generated 13:01 UTC / 16:01 EEST, ~fresh).
- **`stocks-preus-review-ingest` failed twice** with `OperationalError: database is locked` (full traceback in the raw source JSON's sibling log) — the BLOCK/CAUTION verdicts assigned to BAC, SMCI, DIA, SPY, MSTR below are recorded in this review and in the source JSON file, but were **not** written to `stocks_preus_review` / `stocks_preus_review_blocks` tables. The deterministic pipeline will still show these 9 candidates at their original hard-gate tier (C, planning-only pre-open) until a human re-runs the ingest once the lock clears (§14).
- No monitor/paper-status file read this cycle (outside allowed read list) — data_missing.
- Data-quality anomalies this cycle: (1) catalyst-mapping weakness worsening (§5); (2) FIDA/USDT chase-flag/live-signal tension — third occurrence of the pattern first flagged on BICO/USDT (§14, now escalated to a second symbol); (3) SMCI base_score=100.0 — a suspicious round-number score worth a data-quality check (§14); (4) HOME/USDT internal long-vs-weakest-symbol contradiction (§7); (5) the ingest failure above.
- **TradingView / manual chart check unavailable** — no chart MCP loaded this cycle; all price-structure statements are from local OHLCV/ATR/EMA fields already computed inside the reports, plus external WebSearch for premarket/VIX context only (no chart reads).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-05 15:58 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["monitor/paper-status file not read (outside allowed read list)", "stocks-preus-review-ingest failed twice — DB lock — verdicts not persisted"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~1min old, cycle_06 summary <3h old, both fresh", "crypto scalp ~1h27m, intraday ~1h21m old, fresh", "crypto swing ~14h10m old, stale (>14h band), excluded from fresh verdict", "stocks-preus-candidates generated 16:01 EEST, fresh", "stocks-preus-review-ingest OperationalError: database is locked, two attempts, both failed"] },
    { "agent": "market_regime", "verdict": "ok", "confidence": 0.6,
      "reason_codes": ["risk_on", "mixed", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime upgraded to bullish trend (risk-on) this cycle, from transition/mixed at 11:39", "BTC uptrend, ETH transition_up, altcoin breadth 66.67% above EMA20/50 (down slightly from 70.0% at 11:39 but still >65%)", "macro/geopolitics risk pinned 100/100 risk-off, unresolved divergence vs headline tone flagged every cycle this week", "external: S&P futures +0.4%, Nasdaq 100 +0.4%, VIX ~17.9 (up from 16.50 at 11:39), Michael Burry 1987-crash-warning headlines circulating same day as yesterday's fresh S&P ATH close — genuine bull/bear tension into the US open"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "stale_catalyst", "catalyst_contradicted", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["64.2% unmapped today (1605/2500) vs 60.8% at 11:39, 59.8% at 04:39 — worsening trend, still over the 50% weak-mapping threshold", "4 narrative baskets (down from 5): delisting_thin_liquidity (new), binance_ecosystem_teaser (BNB/ASTER), rwa_narrative (ONDO/XLM), momentum_breakout (HEI/FIDA/PUMP)", "MSTR 'Strategy joins Invest America / $250 Trump-accounts pledge' headline is single-source Telegram (t.me/marketfeed, WatcherGuru, WalterBloomberg) — could not be corroborated via WebSearch against mainstream financial press; classified social_only/unverifiable, contradicted by the same-day 'MSTR August slump' framing and a separate BTC-outflow-from-Strategy-wallets headline", "confirmed via direct news_items + catalyst_events title-match query: no material entity-resolved catalyst found for AMAT, NFLX, IWM, DIA, SPY, SMH beyond generic macro/sector noise"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["no fresh per-symbol funding/OI read beyond what the 15:37 EEST intraday report embeds"],
      "suggested_effect": "advisory_only",
      "facts_used": ["carried from 11:39: Hyperliquid whale 40x short on 1,600 BTC (~$102.6M notional), liquidation ~$64,889 — BTC last read 64,417.68 (12:37 EEST intraday snapshot), ~$470 / ~0.7% below the liquidation trigger — squeeze risk still live into the US open", "TUT/USDT: price up + OI up (fresh positioning confirms trend) on both the new intraday signal and the carried swing tp2_hit position", "FIDA/USDT: negative funding across external venues, crowding elevated per derivatives cross-check — a genuine headwind on the fresh waiting_for_entry signal"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "clean_retest", "entry_fresh", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["FIDA/USDT: 15:37 EEST report's own funnel rejects it (score 47.8, '>2 ATR from EMA20, do not chase'), yet a fresh B-tier proposed_signal (72.7, defined pullback entry 0.02100-0.02162, NOT yet filled) fired 12 minutes after that report's data-freshness cutoff — third occurrence of the BICO-pattern chase-flag/live-signal tension (§14), now on a second symbol", "BICO/USDT: prior cycle's waiting_for_entry intraday signal has since filled (now triggered, 66.1); a separate BICO/USDT scalp signal (68.7) also triggered fresh this cycle at 15:34 EEST — desk notes price 0.0240 sits just above the original 0.0228-0.0236 pullback zone, borderline extended", "STO/USDT: still no chase-risk flag, cleanest open long, unchanged since 04:39/11:39", "TUT/USDT, SYN/USDT: both fresh waiting_for_entry with defined pullback zones, not market chases"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry"],
      "data_missing": ["CLI does not label lifecycle state directly — classification below is manual, from status + expires_at"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto (36 active rows): ~15 OPEN actionable (triggered/tp-hit with expires_at still future, incl. HEI/USDT intraday now tp2_hit, TUT/USDT swing tp2_hit, STO/USDT still triggered, BICO/USDT scalp+intraday both triggered), 3 WAITING for entry (FIDA/USDT, SYN/USDT, TUT/USDT intraday — all fresh this cycle, all defined pullback zones), ~18 ENTERED UNRESOLVED (tp-hit but expires_at already past — same carried-forward ambiguity flagged every review this week)", "Stocks legacy active-signals (50 rows): 0 OPEN, 0 WAITING — every row's expires_at already past (latest 2026-08-04T13:54:39), all ENTERED UNRESOLVED/CLOSED", "Stocks pre-US overlay (9 candidates, separate from the legacy table): all in PREOPEN_PLAN state — planning only, not yet live signals; 2 (BAC, SMCI) recommended BLOCK by this review, pending DB ingest retry"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BAC (pre_gate_tier A, base_score 91.0): Senate report alleges Deutsche Bank and BofA 'enabled' Epstein's banking network (corroborates the internal t.me/ClashReport hit re: 60 Minutes shelving an Epstein-banking investigation); OCC anti-money-laundering deficiency penalty risk cited externally — neither caught by the code's LEGAL_RISK exclusion list (which only flagged COIN, MSFT, PLTR this run)", "SMCI (pre_gate_tier A, base_score 100.0): active DOJ investigation, auditor turnover, debt >$8.7B, heavy operating cash use, stock down 52% YTD, earnings 2026-08-11 (6 days out) — also not caught by the hard gate", "LLY and UBER report earnings today (confirmed in the 15:37 EEST intraday report's production risk-warnings block) — do_not_chase_warning both", "PLTR, MSFT, GOOGL, META, AMZN, BNB, BTC all carry active operator-review warnings per the same block (legal/geopolitical/exploit-hack flags)", "HOME/USDT: internal contradiction — appears in today's weakest-symbols list (bias short, 24h -14.27%, RS vs BTC -15.07%) while the desk carries three separate active long B-tier positions in the same symbol"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly: tier=B triggered winrate 26% (CLI's own flag); mode=scalp is the worst bucket (n=16, PF 0.17, avgR -0.18) vs mode=intraday (PF 3.39, avgR 0.83) and mode=swing (PF 2.20, avgR 0.27) — scalp remains a confirmed drag, consistent with the report's own 'low confidence, data collection only' framing", "stocks weekly: tier=C triggered winrate 4%, PF 0.65 below 0.8 (CLI's own flag, n=223, reliable confidence); direction=short is a materially worse bucket than direction=long at reliable/stronger sample size (short: PF 0.14, avgR -0.40, n=82, 1W/10L vs long: PF 1.38, avgR +0.07, n=148, 3W/3L) — a large, high-confidence losing bucket worth a dedicated TODO", "this cycle's fresh crypto fires (TUT, FIDA, SYN, BICO×2, PUMP) sit in the same self-labeled worst sub-playbook as HEI/BICO did at 11:39 ('no-catalyst intraday momentum', 14d WR 23%/PF 0.70/-3R) — but the carried TUT/USDT swing position (different playbook: crypto_swing_narrative_rs_momentum, 14d WR 72%/PF 5.80) continues performing well (tp2_hit)"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.55,
      "reason_codes": ["mixed", "longs_preferred", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime upgraded to risk-on this cycle but the two highest-conviction pre-US stocks candidates (BAC, SMCI, both pre_gate_tier A) both carry hard-gate-missed legal/going-concern risk — routing calls for caution on the stocks side even as crypto brightens", "FIDA/USDT chase-flag/live-signal tension is now a 3rd-occurrence, 2nd-symbol pattern — strong enough to warrant a systemic pipeline-timing review, not just a per-symbol caution flag", "STO/USDT remains the cleanest, unchanged long; HOME/USDT's long-vs-weakest-symbol contradiction needs a manual look before any fresh HOME/USDT sizing", "ingest failure means BAC/SMCI BLOCK verdicts exist only in this document until a human clears the DB lock and re-runs the ingest"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "STO/USDT", "trigger": "already triggered (swing 0.04054-0.04162), invalidation 0.0392 unbroken; add-on only on a clean retest, not a fresh chase" },
    "best_short_candidate":    { "symbol": "HOME/USDT", "trigger": "watch-only, contradiction flag: today's weakest-symbols list shows bias short (24h -14.27%, RS -15.07%) — do NOT open a fresh short while the desk still holds 3 active long B-tier positions in the same symbol; a genuine short only becomes clean if/when those longs are closed or invalidated" },
    "best_catalyst_candidate": { "symbol": "TUT/USDT", "trigger": "fresh intraday waiting_for_entry (65.7, defined pullback 0.02510-0.02559, invalidation 0.02449) layered on top of the already-open, well-performing swing position (tp2_hit) in the same symbol — cleanest RS/narrative-adjacent setup this cycle, fill only inside the defined zone" },
    "avoid_candidate":         { "symbol": "SMCI", "reason": "pre-US overlay BLOCK: active DOJ investigation, auditor turnover, heavy debt/cash-burn, base_score=100.0 anomaly; do not treat as A-tier even though the raw pre_gate_tier says A" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.7 | scheduler_fresh, report_stale | advisory_only |
| market_regime | ok | 0.6 | risk_on, mixed, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.5 | mapping_weak, stale_catalyst, catalyst_contradicted, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, clean_retest, entry_fresh, stale_before_entry | advisory_only |
| execution_lifecycle | caution | 0.55 | open_actionable, waiting_for_entry, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.6 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.6 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | 0.55 | mixed, longs_preferred, manual_review | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1139.md` (11:39 EEST, Europe / pre-US context):

- **New:** TUT/USDT intraday long fired waiting_for_entry (65.7, 16:03 EEST — brand new, ~5 min before this review started); FIDA/USDT and SYN/USDT intraday longs both fired waiting_for_entry (72.7 / 65.2, 15:49 EEST); BICO/USDT scalp long fired triggered (68.7, 15:34 EEST); PUMP/USDT intraday long triggered (70.2, 12:58 EEST, carried into this cycle). All five sit in the desk's self-labeled worst sub-playbook (no-catalyst intraday momentum). **First run of the pre-US stocks overlay** (new for this slot): 9 eligible candidates surfaced, 2 (BAC, SMCI) flagged BLOCK on legal/going-concern grounds not caught by the hard gate.
- **Removed:** none of the prior cycle's core watchlist names dropped.
- **Upgraded/downgraded:** crypto market regime upgraded transition/mixed → **bullish trend (risk-on)**. HEI/USDT intraday advanced triggered → **tp2_hit** (a win, despite the chase-risk flag noted at 11:39 — worth remembering when weighing the FIDA/USDT tension below: not every chase-flagged fill loses). BICO/USDT's 11:39 waiting_for_entry intraday signal (65.1) has since filled (now triggered, 66.1); a second, separate BICO/USDT scalp signal also triggered fresh this cycle. TUT/USDT swing unchanged at tp2_hit, runner still live.
- **New catalysts:** MSTR "Strategy joins Invest America / $250 Trump-accounts pledge" (single-source Telegram, could not corroborate via WebSearch — treated as unverified/social_only, see §5). Hyperliquid whale 40x BTC short (carried from 11:39) — BTC now trading ~$470 below the ~$64,889 liquidation level, squeeze risk closer than before.
- **Thesis changed:** none of the core carried positions (STO/USDT swing, TUT/USDT swing) had their thesis invalidated.
- **Confirmed:** no untracked legacy alerts (0, per detector). The FIDA/USDT chase-flag/live-signal tension **confirms** the pattern first raised as TODO-bico-chase-flag-recurrence — now a 3rd occurrence, 2nd symbol, escalating from "watch" to "likely systemic" (§14).
- **Invalidated:** none.
- Catalyst mapping **worsened further**: 59.8% (04:39) → 60.8% (11:39) → **64.2%** (this cycle) unmapped — a consistent multi-cycle degradation, not noise.

## 5. Catalyst Coverage

- Total catalyst events today: **2,500**; mapped (non-null symbol or related_symbols): **895**; unmapped: **1,605** (**64.2%**).
- Narrative baskets: **4** (down from 5 at 11:39) — new: `delisting_thin_liquidity` (avoid chasing low-float delisting dumps). Continuing: `binance_ecosystem_teaser` (BNB/ASTER, sell-the-news risk), `rwa_narrative` (ONDO/XLM), `momentum_breakout` (HEI/FIDA/PUMP primary — FIDA's presence here is consistent with its chase-flag/live-signal tension above).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Unmapped is 64.2%, the worst reading of the day and rising each cycle.
- Top unmapped headlines this cycle: an Agthia (UAE F&B) earnings release in German (PR Newswire), a $250M USDC mint (whale-alert), a Bybit BACUSDT perpetual listing notice, South African crypto-remittance draft rules, a Western Union stablecoin card launch, a Cloudflare programmable-stablecoin-wallet announcement — the same macro-data / exchange-listing / small-cap-PR mix flagged every cycle this week (§14).

### Pre-US Stocks Review Overlay
- candidates reviewed: 9 (SUPPORT 0 / NEUTRAL 4 / CAUTION 3 / BLOCK 2 / INSUFFICIENT_DATA 0)
- session-cap-only C's now eligible for pre-open Paper lane: 0 (no SUPPORT verdicts issued — none of the 9 met the full bar of entity-resolved + fresh catalyst + fresh market context + no hard cap + genuine RS confirmation; ETFs lack single-entity catalysts by nature, and the two highest-scored single names (BAC, SMCI) both carry real legal/going-concern risk)
- excluded by hard gate: 31 — 15× EARNINGS_BLACKOUT (CAT, META, AAPL, TSLA, GOOGL, AMD, JPM, NVDA, AMZN, AVGO), 3× LEGAL_RISK (COIN, MSFT, PLTR), 13× NO_ENTITY_RESOLVED_CATALYST (COST, GE, CRM, ORCL, NOW, GS, ADBE, LMT, PANW, XLE, XLY, XLF, QQQ, XLK, V, WMT, CRWD)
- **Ingest failure:** both BAC and SMCI BLOCK verdicts (and the 3 CAUTION / 4 NEUTRAL verdicts on the remaining 7) are recorded in `data/raw/enriched_review_sources/preus_review_2026-08-05T13-05.json` and in this review only — `stocks-preus-review-ingest` failed twice with `database is locked`, so the deterministic pipeline still shows all 9 at their original hard-gate tier (§14 TODO).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **risk-on** — BTC uptrend, ETH transition_up, altcoin breadth 66.67% above EMA20/50 (a slight cooling from 70.0% at 11:39, still comfortably risk-on). Macro/geopolitics overlay still pinned at 100/100 risk-off, an unresolved score-vs-headline divergence carried from every prior cycle this week. Recommended style: "selective longs; prefer pullbacks on relative strength."
- Stocks mood: **pre-market, mixed** — external: S&P futures +0.4%, Nasdaq 100 +0.4%, VIX ~17.9 (up from 16.50 three hours ago — a mild risk-off tick), NVDA advancing premarket on a partner's strong AI-infra sales print (constructive for the SMH-tracked semis complex specifically). Counter-current: Michael Burry's 1987-crash-warning commentary is circulating the same day as yesterday's fresh S&P ATH close, and oil/Iran-tanker headlines add a geopolitical layer — genuine tension, not a clean risk-on read. Zero A/B stocks rows are actionable pre-open by design; the 9-name pre-US overlay produced 0 SUPPORT, 2 BLOCK.
- Dominant narrative: crypto risk-on broadening (altcoin breadth) vs. a stocks tape torn between fresh-ATH momentum and a viral crash-warning headline; two of the desk's highest-scored pre-US stocks names (BAC, SMCI) carry real legal/going-concern risk the automated gate did not catch.
- Preferred side now: **longs (crypto)** / **wait-for-RTH-confirmation (stocks)** — crypto's regime upgrade supports selective long adds on RS names; stocks needs the 16:30 EEST open before any pre-market level is trusted, and BAC/SMCI specifically should stay capped regardless of what the open does.
- Best long candidate: **STO/USDT** (carried, unchanged, clean) — see §7/§8.
- Best short candidate: **none clean** — HOME/USDT is the standout weak-symbol candidate but is disqualified from a fresh short by the desk's own conflicting long exposure in the same name; treat as **watch-only** until that conflict resolves.
- Best catalyst-backed candidate: **TUT/USDT** (fresh intraday waiting_for_entry layered on an already-winning swing position) — see §7.
- What to avoid: **SMCI and BAC** for any pre-open A/B consideration (legal/going-concern risk, this review's BLOCK); **FIDA/USDT** fresh sizing until the chase-flag/live-signal tension resolves one way or the other; **crypto scalp mode** generally (confirmed weak bucket, PF 0.17); **stocks short-direction ideas generally** (confirmed weak bucket at reliable sample size, PF 0.14, §14 TODO); new stocks positions of any kind before 16:30 EEST; LLY/UBER earnings prints.
- What would change the view: the `stocks-preus-review-ingest` DB lock clearing so BAC/SMCI BLOCK actually persists; RTH confirmation at/after 16:30 EEST of which pre-market stocks levels hold; BTC approaching the ~$64,889 Hyperliquid liquidation level; the macro/geopolitics score finally moving off 100/100; resolution (fill or expiry, without chase) of FIDA/SYN/TUT's defined pullback zones.

## 7. Candidate Deep Dives

### SMCI (stocks pre-US overlay, pre_gate_tier A→C by market-closed cap, base_score 100.0 — this review: BLOCK)
- Has price already reacted to a catalyst? No fresh entity-specific catalyst found internally or externally beyond a routine "is SMCI fully valued" piece (2026-08-05).
- Is the setup chasing? Not assessable pre-open; irrelevant given the BLOCK below.
- Legal/headline/going-concern check (external, WebSearch): active **DOJ investigation**, **auditor turnover**, debt **>$8.7B**, heavy operating cash use funding a $39B AI-server backlog via a $7B equity/equity-linked raise plus a $75M mandatory-convertible-preferred issue, stock down **52% YTD**, next earnings **2026-08-11** (6 days out). None of this was caught by the code's hard gate (SMCI was not on the EARNINGS_BLACKOUT or LEGAL_RISK exclusion lists this run).
- base_score **100.0** is itself unusual — a perfect round-number score is worth a data-quality check independent of the legal finding (§14).
- Verdict: **BLOCK**. reason_codes: going_concern_risk_doj_investigation, auditor_turnover, heavy_debt_and_cash_burn, hard_gate_missed_legal_risk, score_100_anomaly_suspect.
- What would invalidate the BLOCK: DOJ investigation formally closed/resolved with no findings, audited financials filed cleanly, debt materially reduced — none of which is plausible inside a single decision window.
- Chase-risk: N/A (blocked). Catalyst confirmation/contradiction: no fresh catalyst; going-concern risk is the dominant fact.

### BAC (stocks pre-US overlay, pre_gate_tier A→C by market-closed cap, base_score 91.0 — this review: BLOCK)
- Has price already reacted? Premarket down ~0.75% per external quote (context, not a live desk read).
- Legal/headline check (external, WebSearch + internal news_items cross-confirmation): a Senate report alleges Deutsche Bank and Bank of America "enabled" Jeffrey Epstein's banking network; internal `news_items` independently carries a related t.me/ClashReport hit ("CBS's 60 Minutes reportedly shelved an investigation into Jeffrey Epstein's banking network"), corroborating the theme from a second source. Separately, BAC faces potential OCC penalties for anti-money-laundering deficiencies. Neither was caught by the hard gate's LEGAL_RISK list this run.
- Positives on file (context only, does not offset the legal flag): price target raised to $70 (UBS, 2026-08-03); dividend $0.32 declared.
- Verdict: **BLOCK**. reason_codes: legal_headline_risk_epstein_banking_scrutiny, regulatory_risk_occ_aml_penalty, hard_gate_missed_legal_risk.
- What would invalidate the BLOCK: the Senate-report allegation formally cleared or shown to not implicate BAC specifically, OCC matter resolved/settled with no material penalty.
- Chase-risk: N/A (blocked). Catalyst confirmation/contradiction: fresh legal-headline risk contradicts the raw A-tier technical score.

### FIDA/USDT (crypto intraday long, B-tier waiting_for_entry, 72.7, fresh — chase-flag/live-signal tension, 3rd occurrence)
- Has price already reacted to a catalyst? No — confirmed via `news_items`/`catalyst_events` title search (0 material entity-specific hits <24h); it is a pure momentum name (momentum_breakout basket primary, +33.9% 24h).
- Is the setup chasing? The 15:37 EEST intraday report's own funnel **rejects** FIDA/USDT at score 47.8 ("Price is more than 2 ATR from EMA20; do not chase"; entry quality weak; no catalyst) — yet a fresh B-tier `proposed_signal` (72.7) fired 12 minutes after that report's data-freshness cutoff (12:30 UTC report vs 12:49 UTC signal). This is the **third** occurrence of the exact pattern first raised on BICO/USDT (TODO-bico-chase-flag-recurrence, 04:39 swing + 11:39 intraday) — now on a **second symbol**, which shifts the read from "maybe this one symbol is just volatile" toward "possibly a systemic timing gap between the funnel-scoring pass and the signal-writer pass" (§14, priority raised).
- Retest/pullback structure? Yes — unlike HEI/USDT's continuation entry at 11:39, this is a defined pullback zone (0.02100-0.02162), not a market chase; status is waiting_for_entry, not yet filled.
- Overextended? Yes per the funnel read minutes earlier; derivatives cross-check also shows negative funding + elevated crowding on FIDA specifically — an added headwind.
- Would entry now be late? Not yet — waiting for the defined zone to fill.
- What level makes it actionable cleanly? A fill inside 0.02100-0.02162 holding above invalidation 0.02024, ideally with the funnel's own chase-flag no longer active on the next report cycle.
- Mood alignment: nominally consistent with crypto's risk-on upgrade this cycle, tempered by the same-symbol-class caution already earned by BICO/HEI.
- Long/short/wait: wait-for-entry; treat as manual-review-adjacent given the recurring pattern, same framing the previous review gave BICO/USDT.
- Chase-risk: high per current funnel read. Catalyst confirmation/contradiction: none — clean no-catalyst momentum thesis, consistent with its own framing.

### HOME/USDT (crypto — internal contradiction: weakest-symbol bias-short vs 3 active long B-tier positions)
- The 15:37 EEST intraday report's "Weakest Symbols" table lists HOME/USDT with **bias short**, 24h **-14.27%**, RS vs BTC **-15.07%** — one of the five weakest names on the desk's own board this cycle.
- Simultaneously, `active-signals` shows **three** separate active long B-tier HOME/USDT positions: a swing long (68.5, triggered, invalidation 0.008703), an intraday long (65.3, tp1_hit, invalidation 0.008321, expires later today), and a second swing long (67.3, weekend-mode, triggered, invalidation 0.005879). One position (tp1_hit) is already showing partial profit; the other two are live/triggered with invalidations below current-cycle weakness.
- This is a genuine internal contradiction, not a data-freshness artifact alone — the weakest-symbols read and the active long book come from the same report/DB generation window. It does not by itself mean the longs are wrong (tp1_hit shows one already worked), but it means fresh HOME/USDT exposure in either direction needs a manual look before acting.
- Would entry now be late (for a hypothetical fresh short)? Yes — no defined short setup exists in the reports; this is a flag, not a tradeable idea.
- What level would make a short actionable? Only after a confirmed failed-bounce/breakdown structure is generated by the desk's own scanner — none exists yet.
- Mood alignment: the bias-short read cuts against this cycle's broader risk-on upgrade, which itself is a reason to treat it as a name-specific idiosyncratic move rather than a market-wide signal.
- Long/short/wait: **wait** — do not add fresh exposure either direction; monitor whether the existing longs' invalidations (0.005879 / 0.008321 / 0.008703) hold.
- Chase-risk: N/A (no fresh entry recommended). Catalyst confirmation/contradiction: none found; this is a pure technical/internal-consistency flag (§14).

### STO/USDT (crypto swing long, B-tier triggered, carried — best long this cycle, unchanged)
- Has price already reacted to a catalyst? No catalyst cited — pure RS/momentum thesis, unchanged since 04:39/11:39.
- Is the setup chasing? No chase-risk flag in any report this week for this symbol.
- Retest/pullback structure? Already triggered (0.04054-0.04162) — hold/continuation thesis, not a fresh chase.
- Overextended? Not flagged. STO/USDT continues to not appear among today's "strongest symbols" table — a relative-momentum cooling worth watching, not yet an invalidation.
- Would a fresh entry now be late? For new exposure, prefer a retest over a market fill; existing exposure should simply hold.
- What level makes an add-on actionable? Hold above invalidation 0.0392; a retest of the entry zone is the cleanest add point.
- Mood alignment: consistent with this cycle's risk-on regime upgrade.
- Long/short/wait: long, hold/monitor; add only on retest.
- Chase-risk: low. Catalyst confirmation/contradiction: none either way — clean technical/RS thesis, no contradiction.

*(Excess candidates not given a full deep dive, per the 5-candidate cap: TUT/USDT — fresh intraday waiting_for_entry layered on an already-winning carried swing position, cleanest of the remaining fresh fires, covered in §6/§8 as best catalyst-backed candidate; BICO/USDT — two fresh fills this cycle (scalp 68.7 triggered, intraday 66.1 now triggered from 11:39's waiting_for_entry), continuation of a name already covered in depth at 11:39, current price sits just above its original pullback zone (borderline extended); SYN/USDT and PUMP/USDT — fresh/carried waiting_for_entry and triggered respectively, same no-catalyst-momentum playbook as FIDA/USDT above, lower priority than the contradiction/legal-risk findings; MSTR, AMAT, NFLX, IWM, DIA, SPY, SMH — remaining pre-US overlay names, verdicts (CAUTION/NEUTRAL) recorded in §5 and the source JSON, none met the SUPPORT bar, none carried a BLOCK-level finding.)*

## 8. Best Candidates Ranked

1. **STO/USDT (crypto swing long, triggered, B-tier, carried)** — best long-watch; hold, add only on a clean retest above invalidation 0.0392.
2. **TUT/USDT (crypto intraday long, waiting_for_entry, B-tier, fresh this cycle, layered on a winning swing position)** — best catalyst-backed candidate; enter only on a fill inside 0.02510-0.02559, invalidation 0.02449.
3. **TUT/USDT swing (tp2_hit, carried)** — hold the runner into TP3 (0.0264) or invalidation (0.0222).
4. **FIDA/USDT (crypto intraday, waiting_for_entry, B-tier, fresh this cycle)** — enter only on a fill inside 0.02100-0.02162 above invalidation 0.02024; route to manual review given the recurring chase-flag/live-signal tension (§7/§14) before treating as clean.
5. **SMCI / BAC (stocks pre-US overlay, pre_gate_tier A, this review: BLOCK)** — do not treat as A-tier candidates for the post-open watchlist despite the raw score; legal/going-concern risk documented in §7.

HOME/USDT (best short-watch, disqualified pending resolution of the long/short contradiction — §7) and SYN/USDT (fresh waiting_for_entry, same playbook as FIDA/USDT, lower priority) remain the best watch-only names outside the top 5.

## 9. Avoid / No Trade

*(This applies to this decision window / pre-US-open only — scanning, tracking, and the scheduler continue unchanged.)*

- **SMCI, BAC (pre-US overlay)** — legal/going-concern risk (§7), this review's BLOCK; not actionable regardless of raw score even after RTH confirmation, pending human legal review.
- **FIDA/USDT fresh sizing** — third occurrence of the chase-flag/live-signal tension; let the defined pullback zone fill cleanly or expire, do not force it.
- **HOME/USDT any fresh direction** — internal contradiction between weakest-symbol bias-short read and 3 active long positions; needs manual review before new exposure either way.
- **Crypto scalp mode generally** — confirmed weak bucket this week (PF 0.17, 1W/7L over 14d).
- **Stocks short-direction ideas generally** — confirmed weak bucket at reliable sample size (PF 0.14, n=82, §14 TODO).
- **New stocks positions of any kind before 16:30 EEST** — market closed; the legacy active-signals table is 100% past-expiry, and the pre-US overlay is planning-only by design.
- **LLY, UBER** — earnings today; do not chase into either print.
- **PLTR, MSFT, GOOGL, META, AMZN** — active legal/geopolitical operator-review warnings per the production risk block.

## 10. Main Risks

- **Two of the highest-scored pre-US stocks candidates (BAC, SMCI) both carry real legal/going-concern risk the automated hard gate did not catch** — a reminder that pre_gate_tier A/high base_score alone is not sufficient for actionability even before the market-closed cap is considered.
- **`stocks-preus-review-ingest` failed twice with a DB lock** — this review's BLOCK verdicts on BAC/SMCI are not yet enforced in the deterministic pipeline; if a human doesn't re-run the ingest, tomorrow's pre-US scan could re-surface both as apparently-clean A-tier candidates.
- **The chase-flag/live-signal tension has now recurred a third time, on a second symbol (FIDA/USDT after BICO/USDT)** — increasingly looks like a systemic timing gap between the funnel-scoring pass and the signal-writer pass rather than a one-off; worth a focused human pipeline-timing check (§14).
- **HOME/USDT's internal contradiction** (weakest-symbol bias-short vs 3 active longs) is a genuine data-consistency question, not yet resolved either way.
- Macro/geopolitics risk score remains pinned at 100/100 risk-off for the fourth consecutive review despite a genuinely mixed headline tape (Strait-of-Hormuz de-escalation language earlier in the week, oil/Iran-tanker risk resurfacing today) — the score-vs-headline divergence is unresolved.
- Catalyst→symbol mapping has degraded for three consecutive cycles (59.8% → 60.8% → 64.2% unmapped) — treat all catalyst-basket framing as directional color only.
- A fresh Hyperliquid whale 40x short on 1,600 BTC has a liquidation level (~$64,889) now only ~$470/~0.7% above BTC's last read (64,417.68) — a squeeze risk that has moved closer, not further, since 11:39.
- External VIX ticked up from 16.50 to ~17.9 alongside a viral Michael Burry 1987-crash-warning headline the same day as a fresh S&P ATH close — genuine bull/bear tension into the US open; treat all pre-market stocks levels as provisional until RTH confirms them.

## 11. Action Plan — next 4 hours

- Hold STO/USDT and TUT/USDT's swing runner into their respective invalidations/targets; add to STO/USDT only on a clean retest.
- Let TUT/USDT's fresh intraday order, FIDA/USDT's, and SYN/USDT's waiting_for_entry orders either fill cleanly inside their defined zones or expire — do not manually force any of them, and treat FIDA/USDT specifically as manual-review-adjacent given the recurring chase-flag pattern.
- Do not open any fresh HOME/USDT position (long or short) until the weakest-symbol/active-longs contradiction is manually reconciled.
- Re-run `stocks-preus-review-ingest` once the SQLite lock clears, so the SMCI/BAC BLOCK verdicts actually persist to the pipeline before tomorrow's pre-US cycle.
- Build the post-16:30-EEST stocks watchlist from the pre-US overlay's remaining 7 non-BLOCK names (highest-quality: MSTR, SMH, SPY, DIA — all CAUTION-flagged for macro-narrative-contradiction reasons, require RTH confirmation before any consideration); keep BAC and SMCI off the list regardless of what the open does.
- Avoid chasing LLY/UBER into today's earnings prints; watch BTC price action relative to the ~$64,889 Hyperliquid short-liquidation level into the US open.
- Continue scanning/tracking/monitors unchanged through the pre-US window — this review recommends caution on specific new entries only, never a pause of any kind.

## 12. Final Verdict per Mode

- **Crypto scalp:** no trade — confirmed weak bucket, data-collection only; two scalp signals fired this cycle (BICO/USDT triggered) but the mode-level PF (0.17) argues against fresh sizing regardless of the individual signal.
- **Crypto intraday:** caution — TUT/USDT and FIDA/USDT wait-for-entry (FIDA manual-review-adjacent), HEI/USDT hold-only (already tp2_hit), no fresh market chases.
- **Crypto swing:** the desk's steadiest bucket — hold STO/USDT and TUT/USDT's runner; no fresh swing ideas fired this cycle.
- **Stocks intraday:** no trade — market closed until 16:30 EEST; pre-US overlay produced 0 SUPPORT / 2 BLOCK out of 9 eligible candidates; build the watchlist from the 7 non-BLOCK names but require fresh RTH-confirmed levels before treating any as actionable.
- **Stocks swing/invest:** not evaluated — reports stale/deprecated since 2026-07-02, excluded per standing policy.

## 13. Sources

- Internal: `data/reports/scalp/2026-08-05_12-31_scalp_report.md`, `data/reports/intraday/2026-08-05_12-37_intraday_report.md`, `data/reports/swing/2026-08-05_01-48_swing_report.md` (stale, context only), `data/reports/stocks/intraday/2026-08-05_10-06_stocks_intraday_report.md`, `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`, `data/catalysts/2026-08-05/catalyst_events.jsonl`, `data/catalysts/2026-08-05/narrative_baskets.jsonl`, `data/catalysts/2026-08-05/catalyst_cycle_12-42.md`, `data/processed/llm_analysis_packet.md`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items` read-only queries), `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1139.md`.
- External (WebSearch, no WebFetch this cycle):
  - [Stock Market Today (Aug. 5, 2026): S&P futures gain ahead of Disney, Shopify earnings — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-5-2026) — premarket S&P/Nasdaq futures context.
  - [S&P 500 VIX Futures - Investing.com](https://www.investing.com/indices/us-spx-vix-futures) — VIX ~17.9 read.
  - [Michael Dell Reaffirms $250 Trump Accounts Pledge to 25M Children — Yahoo Finance](https://finance.yahoo.com/economy/articles/michael-dell-reaffirms-250-trump-233109477.html) — used to confirm the "$250 Trump Accounts" program is real but tied to Michael Dell, NOT independently corroborating the MSTR/Saylor-specific Telegram headline (treated as unverified for MSTR).
  - [Super Micro Computer (SMCI) Stock Price & Overview — stockanalysis.com](https://stockanalysis.com/stocks/smci/) and related search aggregate — DOJ investigation, auditor turnover, debt, 52% YTD decline, Aug 11 earnings date.
  - [Bank of America (BAC) — Stock Premarket — stockmarketwatch.com](https://stockmarketwatch.com/stock/BAC/premarket) and related search aggregate — Epstein-banking Senate report, OCC AML penalty risk, premarket quote.
- No chart/TradingView source this cycle (unavailable, §3).

## 14. Fix Requests / TODO

### TODO-preus-ingest-db-locked (priority: high, new)
- **issue:** `python -m src.cli stocks-preus-review-ingest --json data/raw/enriched_review_sources/preus_review_2026-08-05T13-05.json` failed twice with `sqlite3.OperationalError: database is locked`, first on the INSERT into `stocks_preus_review_blocks` (BAC's BLOCK), second on the INSERT into `stocks_preus_review` (base table). The pre-US overlay's BLOCK verdicts on BAC and SMCI (and the 3 CAUTION / 4 NEUTRAL verdicts on the other 7 candidates) exist only in this review file and the source JSON — they were never persisted to the DB.
- **evidence:** command output captured in this run's background-task log; source JSON at `data/raw/enriched_review_sources/preus_review_2026-08-05T13-05.json`.
- **suggested manual fix:** a human-driven session should identify what holds the write lock on `db/crypto_ai_desk.sqlite` during the pre-US window (likely a long-running scheduler/monitor transaction — `derivatives_monitor` and `fast_news_monitor` were both actively writing large log files at review time) and either serialize pre-US-overlay ingest writes behind a retry-with-backoff, or move `stocks_preus_review`/`stocks_preus_review_blocks` writes to a WAL-friendlier access pattern. Then manually re-run the ingest command above once the lock clears.
- **priority:** high
- **first observed:** 2026-08-05 16:05 EEST (this cycle, first run of this overlay).

### TODO-chase-flag-recurrence-escalation (priority: high, escalated — 3rd occurrence, 2nd symbol)
- **issue:** the "funnel-scoring pass rejects a symbol for being >2 ATR from EMA20 / do not chase, while a live `proposed_signal` fires for the identical symbol minutes later" pattern has now recurred a third time: BICO/USDT swing (flagged 04:39, since resolved tp3_hit win), BICO/USDT intraday (flagged 11:39, since filled/triggered), and now **FIDA/USDT intraday** (this cycle — report score 47.8 "do not chase" at 12:30 UTC data-freshness, live signal 72.7 fired 12:49 UTC, still waiting_for_entry). Two different symbols showing the identical timing pattern raises the likelihood this is systemic (a gap between the funnel-scan pass and the signal-writer pass) rather than one volatile symbol.
- **evidence:** `data/reports/intraday/2026-08-05_12-37_intraday_report.md` §7b (FIDA/USDT score 47.8, "Price is more than 2 ATR from EMA20; do not chase"); `db/crypto_ai_desk.sqlite` `proposed_signals` row `sig_e3c13a408833b09e` (score 72.7, created 2026-08-05T12:49:35 UTC); prior instances referenced in `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1139.md` §14 (TODO-bico-chase-flag-recurrence) and `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_0439.md` §14.
- **suggested manual fix:** a human-driven session should measure the actual elapsed time between the funnel-scan data-freshness timestamp and the signal-writer's `created_at` across the last 1-2 weeks of signals, checking whether symbols with large intraday ATR are disproportionately represented in this "flagged then fired" set — if so, the funnel-scan and signal-writer likely need to share a single price snapshot rather than running against two different reads.
- **priority:** high
- **first observed:** 2026-08-04 (swing instance); escalated 2026-08-05 15:58 EEST (this cycle, 2nd symbol confirmed).

### TODO-home-usdt-contradiction (priority: medium, new)
- **issue:** HOME/USDT appears in the 15:37 EEST intraday report's "Weakest Symbols" table (bias short, 24h -14.27%, RS vs BTC -15.07%) in the same report-generation window where `active-signals` shows three separate active **long** B-tier HOME/USDT positions (one already tp1_hit, two triggered). This is an internal consistency question the review cannot resolve with read-only tools.
- **evidence:** `data/reports/intraday/2026-08-05_12-37_intraday_report.md` §2 "Weakest Symbols"; `active-signals --asset-class crypto` output, HOME/USDT rows (signal_ids visible via `db/crypto_ai_desk.sqlite` `proposed_signals`).
- **suggested manual fix:** a human-driven session should check whether the "weakest symbols" momentum-score calculation and the long-signal scoring pipeline are reading from the same OHLCV window, and whether HOME/USDT's recent price action has genuinely reversed against the still-open longs (in which case the invalidations, not the momentum table, are the operative risk control) or whether one of the two pipelines is stale.
- **priority:** medium
- **first observed:** 2026-08-05 15:58 EEST.

### TODO-smci-score-100-anomaly (priority: medium, new)
- **issue:** SMCI's pre-US overlay `base_score` is exactly **100.0** — a perfect round-number score is unusual for a continuous scoring function and worth checking independent of the legal-risk finding in §7 (which alone is sufficient to block the candidate either way).
- **evidence:** `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`, SMCI row: `base_score=100.0`.
- **suggested manual fix:** a human-driven session should trace SMCI's score computation for this cycle and confirm whether 100.0 is a genuine (if extreme) output or a clamping/default-value bug.
- **priority:** medium
- **first observed:** 2026-08-05 15:58 EEST.

### TODO-stocks-short-direction-losing-bucket (priority: medium, carried forward as a fresh reliable-sample confirmation)
- **issue:** `signal-stats --asset-class stocks` weekly, `direction=short`, confidence=stronger, n=82: PF **0.14**, avgR **-0.40**, 1W/10L (triggered=40). This is now a large-enough, high-confidence-enough sample to treat as a structural weak bucket, not noise — materially worse than `direction=long` (PF 1.38, avgR +0.07, n=148) in the same weekly window.
- **evidence:** `signal-stats --asset-class stocks` CLI output, "By direction" table, this cycle.
- **suggested manual fix:** a human-driven session should review whether stocks short-side entries need a stricter setup-quality or RS-confirmation gate, or whether the bucket should be demoted to watchlist-only pending further data, mirroring how crypto scalp mode was demoted.
- **priority:** medium
- **first observed:** carried/confirmed 2026-08-05 15:58 EEST (first flagged generically in earlier cycles; this is the first review to quantify it directly via signal-stats).
