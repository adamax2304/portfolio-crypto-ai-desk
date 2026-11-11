# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

_Generated 2026-06-19 ~18:39 EEST (Friday, Juneteenth — US stocks CLOSED all day; no US open today; next session Mon June 22; crypto live). Advisory only. No auto-trade. Scanner / collection / tracking continue in all moods. External web research **AVAILABLE** (WebSearch ×1; WebFetch ×1; limited by 8:30am ET data)._

> **⚠️ JUNETEENTH ALERT: US cash markets (NYSE, Nasdaq) are CLOSED today June 19, 2026.** This "US open reaction" slot fires normally per schedule, but there was NO US open today. Stock A/B signals remain Monday June 22 planning only. Crypto is the live actionable class.

> **KEY DEVELOPMENT THIS SLOT: AVAX/USDT intraday B short and XLM/USDT swing B short both TRIGGERED between 17:07 and 18:39 EEST.** Both are now ENTERED UNRESOLVED. Crypto swing report also freshly generated this cycle for the first time today.

---

## 1. Executive Summary

**Fri 2026-06-19 (Juneteenth), 18:39 EEST — "US open reaction review" — NO US OPEN; AVAX & XLM shorts entered; crypto risk-off deepening; BTC ~$62,498; no A-tier; advisory only.**

Since the 16:20 EEST pre-open review, two critical changes: (1) **AVAX/USDT intraday B short** (66.1/100, failed-bounce playbook, PF 2.00) is now **ENTERED UNRESOLVED** — price bounced into the 6.127–6.162 retest zone and triggered. (2) **XLM/USDT swing B short** (66.3/100, fresh swing report) is now **ENTERED UNRESOLVED** — price bounced into 0.2208–0.2226 zone and triggered. Both entered via clean retest on risk-off market structure. **Key risk: AVAX has OI +17.92% on price decline — significant short squeeze potential if BTC bounces from $62K.**

BTC remains at ~$62,498 (8:30am ET / 15:30 EEST external; post-FOMC selling, rates unchanged but hawkish dot plot, $102M ETF outflows June 18). ETH at ~$1,687.60. Both in confirmed downtrends internally. No A-tier across crypto or stocks. Crypto swing report is now fresh (was stale at 16:20). Stocks closed (Juneteenth); META B-tier short deferred to Monday.

**This slot is advisory only. No auto-trade. No changes to scoring, TP/SL, or execution logic.**

---

## 2. Data Used

| Report | File | mtime EEST | Age at review | Status |
|--------|------|------------|---------------|--------|
| Crypto scalp | `2026-06-19_12-54_scalp_report.md` | Jun 19 15:54 | ~2h45m | **FRESH** (<4h) |
| Crypto intraday | `2026-06-19_13-06_intraday_report.md` | Jun 19 16:06 | ~2h33m | **FRESH** (<4h) |
| Crypto swing | `2026-06-19_13-40_swing_report.md` | Jun 19 16:41 | ~1h58m | **FRESH** (<4h) ← NEW vs 16:20 review |
| Stocks intraday | `2026-06-19_15-32_stocks_intraday_report.md` | Jun 19 18:32 | ~7 min | **FRESH** (<4h) |
| Stocks swing | `2026-06-19_13-54_stocks_swing_report.md` | Jun 19 16:54 | ~1h45m | **FRESH** (<4h) — watchlist-only mode |
| Stocks invest | `2026-06-19_14-04_stocks_invest_report.md` | Jun 19 17:04 | ~1h35m | **FRESH** (<4h) — watchlist-only mode |
| LLM packet (crypto) | `data/processed/llm_analysis_packet.md` | Jun 19 16:41 | ~1h58m | **FRESH** |
| Active signals (CLI) | `python -m src.cli active-signals` | Jun 19 18:39 | 0 min | **LIVE** |
| External prices | Yahoo Finance article (Jun 19 2026) | 8:30am ET / 15:30 EEST | ~3h | **dated** — best available |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-06-19_1620.md` | Jun 19 16:20 | ~2h19m | pre-US-open slot |

**External web research:** BTC $62,498 / ETH $1,687 confirmed from Yahoo Finance June 19 2026 article. Post-FOMC selling context confirmed. No fresher intraday price available. TradingView/manual chart: **unavailable** — all technical observations use OHLCV/ATR/EMA from reports only.

**Social attention:** Reddit 403 blocked (recurring). 0 symbol-level hits. No X/Telegram/Discord live feeds.

---

## 3. Scheduler / Data Freshness

| Check | Value | Status |
|-------|-------|--------|
| Latest run folder | `2026-06-19_default_schedule/` | ✓ |
| `scheduler.log` mtime | Jun 19 17:07 EEST (1h32m ago) | **FRESH** (<3h) |
| Latest `cycle_*_summary.md` | `cycle_01_15-37_summary.md` — Jun 19 17:07 EEST | **FRESH** (<3h) |
| Defer rule | Both <3h → **DO NOT DEFER** | ✓ |
| Monitors running | `crypto_monitor` at 18:39 (0 min ago), `stocks_monitor` at 18:22 (17 min ago) | **ACTIVE** |
| Paper monitor | Open=6, Waiting=1, Entered_unresolved=14, Review/Shadow=141, No-entry=39, Closed=269W/33L | **OK** |
| Crypto swing freshness | FRESH (~2h) — previously stale (48h) at 16:20 review | RESOLVED |
| Reddit social | 403 block (recurring) | WARNING |
| Bybit init | WARNING on swing step (api.bybit.com/v5/market/instruments-info — spot instruments-info failed) | WARNING |
| Onchain | `interface_ready_config_missing` — no `config/onchain.yaml` | CONFIG_MISSING |
| Derivatives | Partial — MEXC fallback for SYN, HEI (MEXC), HOME, CHIP, XLM, OPG, EIGEN, XPL | PARTIAL |

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-06-19 18:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "derivatives_sparse", "onchain_config_missing"],
      "data_missing": ["onchain whale flows", "live X/Telegram/Discord feeds", "liquidation heatmaps", "ETF flows real-time"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "scheduler.log 1h32m old (<3h)",
        "cycle_01_15-37_summary.md 1h32m old",
        "all reports fresh: scalp 2h45m, intraday 2h33m, swing 1h58m, stocks-intraday 7min",
        "crypto_monitor log 0min old, stocks_monitor 17min old",
        "Bybit spot instruments-info WARNING in swing step",
        "MEXC derivatives fallback for multiple symbols",
        "Reddit 403 blocked (recurring)",
        "onchain.yaml config missing"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "ok",
      "confidence": 0.9,
      "reason_codes": ["risk_off", "shorts_preferred", "danger"],
      "data_missing": ["live BTC intraday price beyond 8:30am ET", "ETF flow today"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC trend: downtrend (internal + external ~$62,498)",
        "ETH trend: downtrend (internal + external ~$1,687)",
        "Altcoin breadth above EMA20: 22.73% (scalp/intraday) / 29.55% (swing) — very weak",
        "Post-FOMC hawkish signals (Jun 17), rates unchanged but dot plot hawkish",
        "$102M BTC+ETH spot ETF net outflows June 18",
        "BTC 1-month -18.3%, 1-year -40% (Yahoo Finance)",
        "Stocks closed (Juneteenth) — not a regime signal"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["no_catalyst", "mapping_weak", "narrative_supported", "catalyst_contradicted"],
      "data_missing": ["307/320 catalyst events typed as other_news — specific catalyst missing for AVAX, XLM, TAO short candidates"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "680-777 catalyst events today; 5 narrative baskets",
        "Mapping: 307/320 = 96% other_news in latest cycle — mapping weak",
        "momentum_breakout basket (HEI/ATM/SYN): playbook=avoid_chase",
        "ETH negative: $102M ETF outflows Jun 18, UXLink exploit $8.1M, leadership 2nd co-director departure",
        "XRP negative: Israeli attacks on Iran deal, 5% plunge",
        "BNB single_source: EASY Residency S4 — sell-the-news risk",
        "UNH legal_risk: DOJ probe importance 0.73 (confirmed)",
        "SMCI legal_risk: export-control indictment importance 0.77 (confirmed)",
        "CLARITY Act + CFTC Mashinsky ban + stablecoin ID requirements (regulatory basket)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "data_unavailable", "post_unwind_chop"],
      "data_missing": ["ATM futures data unavailable", "OI numeric history sparse", "liquidation clustering unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "AVAX: price down + OI +17.92% — fresh shorts pressing; high squeeze risk on BTC bounce",
        "XLM: price down + OI +0.37%; funding -0.000140 — fresh shorts, mild squeeze risk",
        "HOME: elevated crowding (OKX funding -0.0022); OI 24h -5.07% — crowded shorts deleveraging",
        "CHZ: crowding unknown; funding -0.000637 (MEXC) — crowded short proxy",
        "SYN: funding -0.000461 (MEXC); negative across venues — shorts crowded on RS leader",
        "HEI: price up + OI +10.76-18.67% — fresh positioning confirms trend, healthy",
        "EDEN: price up + OI down — short covering, weaker continuation",
        "squeeze_phase distribution: phase_2_squeeze_expansion = 4 symbols (unknown which)",
        "ATM/USDT: no futures data available"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "ok",
      "confidence": 0.75,
      "reason_codes": ["clean_retest", "entry_fresh", "waiting_for_entry"],
      "data_missing": ["TradingView chart unavailable — using OHLCV/ATR/EMA from report only", "no live 15m candle confirmation"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "AVAX: triggered (status tr...) — bounced into 6.127-6.162 zone; entry_fresh; ATR 0.0765",
        "XLM: triggered (status tr...) — bounced into 0.2208-0.2226 zone; entry_fresh; ATR 0.0042",
        "TAO swing short: WAITING for entry at ~22.x entry zone — price ~27 currently; far trigger",
        "HEI: +47-51% RS, OI confirms, entry zone 0.1192-0.1237 — DO NOT CHASE current ~0.1257",
        "NEAR scalp: entry zone 2.103-2.122, current 2.095-2.134; may have moved through zone",
        "MEGA/XLM/SUI rejected in reports as >2 ATR from EMA20 (extended)"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["entered_unresolved", "waiting_for_entry", "open_actionable"],
      "data_missing": ["exact AVAX/XLM fill prices not visible in truncated CLI output"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "AVAX intraday B short: ENTERED UNRESOLVED (was WAITING at 17:07, now triggered at 18:39)",
        "XLM swing B short: ENTERED UNRESOLVED (was WAITING at 17:07, now triggered at 18:39)",
        "XPL scalp B short: TP1 HIT (positive, confirmed in cycle summary and CLI)",
        "TAO swing B short: WAITING for entry (~22.x, ~19% below current price)",
        "Paper monitor: 6 open actionable, 1 waiting, 14 entered-unresolved, 141 review/shadow, 39 no-entry/stale/moved-away",
        "Closed today: 269W / 33L / 0flat (excellent session close stats)",
        "Untracked legacy alerts: 0 (clean)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["correlation_cluster", "reduce_risk", "headline_risk", "manual_review"],
      "data_missing": ["daily P&L not directly visible", "position sizing not confirmed"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "AVAX OI +17.92% into price decline = squeeze risk if BTC bounces from $62K",
        "XLM + AVAX + potential TAO = correlated short cluster (all BTC-linked)",
        "Crypto B-tier WR 8.7%, PF 0.494, -40R over week — repeated playbook losses on longs",
        "Short playbook subset: WR 40%, PF 2.00, +9R (14d) — better sub-cohort",
        "Weekend approaching: swing shorts (XLM) carry gap risk over Sat/Sun",
        "UNH: DOJ probe AVOID (stocks legal risk)",
        "SMCI: export-control indictment AVOID (confirmed)",
        "No daily loss pressure identified in paper monitor",
        "Crypto scalp WR 12% PF 0.14 = low confidence, 0.5x sizing weight"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["playbook_working", "playbook_failing", "missed_winner", "low_sample"],
      "data_missing": ["short-playbook sample n=10 (week) — small", "scalp sample 14d n=8 closed"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "crypto_failed_bounce_short: 14d WR 40%, PF 2.00, +9R — actionable; AVAX/XLM on this playbook",
        "crypto_swing_narrative_rs_momentum: 14d WR 72%, PF 5.80, +24R — best playbook; RS longs (HEI/SYN/ATM/EDEN) showing TP1 hits",
        "crypto_intraday_catalyst_or_momentum (no catalyst): WR 23%, PF 0.70, -3R — weak; most C-tier intraday on this",
        "crypto_scalp_momentum_continuation: WR 12%, PF 0.14, -6R — low confidence; 0.5x sizing weight",
        "stocks_intraday_rth_momentum (B-tier): 14d WR 55%, PF 2.03, +80R — primary playbook, but market closed today",
        "stocks_swing + invest: paused/watchlist-only (0x weight)",
        "B-tier overall week: WR 8.7%, PF 0.494, -40R driven by intraday long sub-cohort losses"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["risk_off", "shorts_preferred", "correlation_cluster", "squeeze_risk"],
      "data_missing": ["live BTC intraday chart beyond 8:30am ET"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "AVAX/XLM shorts entered on clean retest — monitor for TP1 execution",
        "Risk-off regime confirmed by all internal + external signals",
        "Squeeze risk on AVAX is the primary risk for this window",
        "HEI RS leadership is the best long setup but counter-tape — needs pullback",
        "UNH Monday planning: DOJ probe confirmed AVOID for directional trade",
        "No A-tier across all asset classes"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.78,
    "preferred_side": "shorts",
    "best_long_candidate": {
      "symbol": "HEI/USDT",
      "trigger": "pullback to 0.1192–0.1237 zone with volume holding; do NOT chase at current ~0.1257",
      "reason": "Top RS leader +47-51% vs BTC; OI confirms trend (fresh positioning); momentum_breakout basket member; counter-tape so reduce size and require confirmation"
    },
    "best_short_candidate": {
      "symbol": "AVAX/USDT (entered) + TAO/USDT (waiting)",
      "trigger": "AVAX entered at 6.127-6.162 retest (monitor TP1 6.035); TAO trigger at ~22.x entry zone if price drops from ~27",
      "reason": "AVAX B-tier failed-bounce short on clean retest, playbook PF 2.00; TAO swing short WAITING — far trigger, lower urgency"
    },
    "best_catalyst_candidate": {
      "symbol": "UNH",
      "trigger": "Monday Jun 22 open: short if SPY weak at open AND UNH fails first 15-min bounce below prior low; confirm entry is not extended",
      "reason": "DOJ probe importance 0.73 confirmed; shares -16% on news; stocks playbook PF 9.00 on shorts subset; MARKET CLOSED TODAY"
    },
    "avoid_candidate": {
      "symbol": "CHZ/HOME (crowded shorts) + BNB (sell-the-news risk) + HEI/ATM/SYN chase longs",
      "reason": "CHZ/HOME: extreme negative funding, crowded short = squeeze risk; BNB catalyst single-source; HEI/ATM/SYN momentum_breakout basket = avoid_chase playbook; no catalyst confirmation for any RS leader"
    },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|-------|---------|------------|--------------|-----------------|
| data_quality | **ok** | 0.85 | `scheduler_fresh`, `derivatives_sparse`, `onchain_config_missing` | advisory_only |
| market_regime | **ok** | 0.90 | `risk_off`, `shorts_preferred`, `danger` | advisory_only |
| catalyst_narrative | **caution** | 0.65 | `no_catalyst`, `mapping_weak`, `narrative_supported`, `catalyst_contradicted` | advisory_only |
| derivatives_squeeze | **caution** | 0.65 | `squeeze_risk`, `oi_contradicts`, `data_unavailable`, `post_unwind_chop` | advisory_only |
| technical_entry | **ok** | 0.75 | `clean_retest`, `entry_fresh`, `waiting_for_entry` | advisory_only |
| execution_lifecycle | **ok** | 0.85 | `entered_unresolved`, `waiting_for_entry`, `open_actionable` | advisory_only |
| risk_manager | **caution** | 0.70 | `correlation_cluster`, `reduce_risk`, `headline_risk`, `manual_review` | advisory_only |
| playbook_performance | **caution** | 0.75 | `playbook_working`, `playbook_failing`, `missed_winner`, `low_sample` | advisory_only |
| head_trader | **caution** | 0.78 | `risk_off`, `shorts_preferred`, `correlation_cluster`, `squeeze_risk` | advisory_only |

---

## 4. What Changed vs Previous Review

**Prior review:** `OPUS_ENRICHED_REVIEW_AUTO_2026-06-19_1620.md` (16:20 EEST, pre-US-open slot)

| Item | 16:20 EEST (pre-US-open) | 18:39 EEST (US open reaction) |
|------|--------------------------|-------------------------------|
| AVAX/USDT status | WAITING for entry (retest 6.127–6.162) | **ENTERED UNRESOLVED** ← key change |
| XLM/USDT status | Not in 16:20 review (swing stale at 16:20) | **ENTERED UNRESOLVED** (swing now fresh) ← key change |
| TAO swing short | Not present | **WAITING** ~22.x entry zone (new signal) |
| Crypto swing report | STALE (Jun 17, ~48h) | **FRESH** (Jun 19 16:41 EEST, ~2h) ← major improvement |
| Active crypto signals | 17 | **18** (+1 net) |
| Stocks intraday report | Jun 19 13:21 EEST | **Jun 19 18:32 EEST** (7 min old, very fresh) |
| Stocks swing/invest | STALE (Jun 17) | **FRESH** (Jun 19, <2h) |
| BTC external price | ~$62,498 (8:30am ET) | ~$62,498 (same source — best available) |
| META stocks B-tier | 70.29, Monday planning | Monday planning (unchanged — market closed) |
| UNH AVOID | DOJ probe confirmed | DOJ probe unchanged — AVOID Monday |
| SMCI AVOID | Indictment confirmed | Unchanged |
| XPL scalp B | TP1 hit confirmed | TP1 hit confirmed (closed) |
| Paper monitor | Not available from 16:20 | 6 open, 14 entered-unresolved, 269W/33L closed |

**New since 16:20 EEST:**
- Crypto swing report regenerated — fresh setup universe confirmed.
- XLM swing B short appeared and immediately triggered.
- TAO swing B short new in active signals (WAITING, distant trigger).
- All stocks reports now fresh (were stale at 16:20).
- Stocks regime: market closed confirmed via fresh stocks report (NaN returns = Juneteenth).

**Confirmed / unchanged:**
- Risk-off crypto. BTC below $63K. No A-tier.
- HEI/EDEN RS leadership persisting but decaying slightly (+51%→+47% from 16:20 intraday data).
- UNH and SMCI AVOID flags confirmed.
- META B-tier short deferred to Monday.

---

## 5. Catalyst Coverage

- **Total catalyst events today:** 680–777 (range across scalp→swing reports); **baskets: 5**
- **Latest cycle scan:** 320 `news_items` rows; typed events: legal_risk=3, analyst_action=3, roadmap_event=2, partnership=2, mainnet_launch=1, regulatory_sector_headline=1, low_liquidity_event=1 = **13 typed events**; other_news = 307

> ⚠️ **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** 96% of events (307/320) classified as "other_news" without specific catalyst type resolution. Symbol-specific verified events (UNH, SMCI, ETH, BNB, XRP) are available in news_items but the broader event landscape is unmapped. This has been recurring across multiple runs.

**Active narrative baskets:**

| Basket | Playbook | Freshness | Primary | Implication |
|--------|----------|-----------|---------|-------------|
| momentum_breakout | **avoid_chase** | <1h | HEI/USDT, ATM/USDT, SYN/USDT (swing: + EDEN) | DO NOT CHASE — pure price action, zero catalyst |
| ai_narrative | related_beta_rotation | unknown | NEAR, RENDER, TAO, FET | Mixed heat 44/100; context only |
| perps_dex_narrative | wait_pullback | <24h | HYPE/USDT | Wait for pullback |
| binance_ecosystem_teaser | related_beta_rotation | <6-24h | BNB/USDT | Single-source, sell-the-news risk |
| delisting_thin_liquidity | avoid_low_liquidity | <24h | — | Avoid thin/low-float |

**Notable catalyst events (legal/regulatory priority):**
- **UNH** [legal_risk, importance 0.73]: DOJ probe (Medicare fraud + Optum Rx antitrust) — shares -16%. Stocks CLOSED today; Monday trigger for short setup if confirmed at open.
- **SMCI** [legal_risk, importance 0.77]: Export-control violation conspiracy indictment (3 individuals, SEC EDGAR Form 8-K). AVOID.
- **ETH** [exploit_hack]: UXLink exploit ($8.1M ETH → Tornado Cash); DAO relaunches as $130M security fund — net bearish for ETH confidence.
- **ETH** [leadership]: Second co-director departure from Ethereum Foundation.
- **Regulatory basket**: CLARITY Act (crypto market structure bill); CFTC Mashinsky permanent trading ban; US stablecoin user-ID requirements.

**Top 3 unmapped headline events (other_news):** Goldman Sachs gold outlook cut; UAE social media age laws; Base Beryl upgrade targeting June 25.

---

## 6. Market Landscape

### Market Mood / Risk Routing

- **Crypto mood:** risk-off (BTC downtrend, ETH downtrend, breadth 22-29%, post-FOMC pressure, $102M ETF outflows)
- **Stocks mood:** CLOSED (Juneteenth — full day holiday; NaN returns in all stock reports confirm closure; next session Mon June 22)
- **Dominant narrative:** Post-FOMC hawkish continuation; dollar strength; no oil-shock resolution lifting crypto; ETF outflows; ETH leadership instability
- **Preferred side now:** shorts (crypto) — failed-bounce pattern on weak alts; AVAX/XLM already entered
- **Best long candidate:** HEI/USDT — RS leader +47-51% vs BTC; OI confirms trend — pullback to 0.1192–0.1237 only; no chase
- **Best short candidate:** AVAX/USDT (ENTERED UNRESOLVED, monitor TP1); TAO/USDT (WAITING, trigger ~22.x)
- **Best catalyst-backed candidate:** UNH (DOJ probe, Monday June 22 only — stocks closed today)
- **What to avoid:** CHZ/HOME (crowded shorts with negative funding — squeeze risk); BNB long (single-source catalyst); any RS leader chase (HEI/ATM/SYN above entry zones)
- **What would change the view:** BTC reclaiming $64K on volume would signal short-term reversal and require re-evaluation of AVAX/XLM short entries

---

## 7. Candidate Deep Dives

### Candidate 1 — AVAX/USDT — B-tier intraday short — ENTERED UNRESOLVED

**Signal summary:** Score 66.1/100, playbook `crypto_failed_bounce_short` (14d WR 40%, PF 2.00, +9R), status actionable, entered between 17:07 and 18:39 EEST.

**Entry context:**
- Entry zone: 6.127–6.162 (failed-bounce/retest zone). Price at 16:06 report was 6.112 (just below). Status changed from WAITING to TRIGGERED between 17:07 and 18:39. Entry is consistent with a bounce into retest.
- Current price at last report: 6.112. ATR: 0.0765. Support: 5.968. Resistance: 6.386.
- TP1: 6.035 (~1.2 ATR below entry midpoint). TP2: 5.959. TP3: 5.883.
- Invalidation: 1h close beyond 6.204 (~0.5 ATR above entry midpoint).

**Squeeze risk (PRIMARY CONCERN):**
- AVAX: price down + OI +17.92% = **fresh shorts pressing**. This means many shorts entered at/before our entry zone. If BTC bounces from ~$62K, a short squeeze could run AVAX back toward 6.204 invalidation quickly.
- Bybit cross-check: crowding = normal. Funding -0.00016266 (slightly negative).
- Multi-exchange confirmation: binance + MEXC, anchor=binance, confirmation 83%.

**Price reaction check:** Yes, price already reacted to the risk-off regime. Entry is NOT chasing — it's a retest after a breakdown. The breakdown from ~$7 range to $6.1 happened; retest into entry zone is the clean pattern.

**Chase risk:** LOW — entry triggered on bounce into zone, not at the low.

**Alignment with mood:** Fully aligned. Risk-off regime, weak RS vs BTC (-6.4%), no catalyst backing shorts.

**Actionability:** ENTERED. Monitor TP1 (6.035). Watch BTC for squeeze trigger. Stop at 1h close beyond 6.204.

**Verdict:** ENTERED UNRESOLVED — watch, do not add. Primary risk = BTC bounce squeezes AVAX shorts.

---

### Candidate 2 — XLM/USDT — B-tier swing short — ENTERED UNRESOLVED

**Signal summary:** Score 66.3/100, playbook `crypto_failed_bounce_short` (swing variant, same playbook, 7d horizon), status actionable, entered between 17:07 and 18:39 EEST. This is a NEW addition vs 16:20 review (swing was stale then).

**Entry context:**
- Entry zone: 0.2208–0.2226 (failed-bounce/retest zone). Price at 16:41 report was 0.2190 (below zone). Triggered on bounce.
- Current price at last report: 0.2190. ATR: 0.0042. Support: 0.2163. Resistance: 0.2443.
- TP1: 0.2160. TP2: 0.2119. TP3: 0.2079.
- Invalidation: 1h close beyond 0.2248 (~0.5 ATR above entry midpoint).

**Derivatives context:**
- XLM: price down + OI +0.37% = fresh shorts, very mild OI increase. Less squeeze risk than AVAX.
- Funding: -0.000140 (bybit) / -0.000117 (MEXC) = slightly negative but not extreme.
- Long/short: 1.235 (more longs than shorts). OI change small. Squeeze risk: moderate but lower than AVAX.
- Multi-exchange confirmation: binance + MEXC, confirmation 88.4%, anchor=binance.

**Catalyst note:** XRP and DOT are cited for "June sentiment crash" analogy. XLM is correlated as Stellar (XRP competitor), so if XRP sentiment deteriorates further (Trump-Iran deal tensions), XLM could accelerate lower.

**7d return context:** 7d +13.53% but 24h -10.61% = recent weakness after a 7d run. This is the classic failed-bounce setup: 7d pump followed by retest of the breakdown.

**Squeeze risk:** Moderate. OI only +0.37%. Lower risk than AVAX.

**Swing horizon:** Multi-day. Weekend gap risk. If XLM moves against the short over the weekend (e.g. BTC bounces Sunday), the stop could trigger at 0.2248 without being able to act quickly.

**Verdict:** ENTERED UNRESOLVED — swing short, watch TP1 (0.2160). Weekend gap risk acknowledged. Squeeze risk lower than AVAX.

---

### Candidate 3 — HEI/USDT — RS leader long watchlist — COUNTER-TAPE, DO NOT CHASE

**Signal summary:** C-tier watchlist (counter-tape long against bearish regime). Score 59.3/100. Momentum_breakout basket (playbook: `avoid_chase`). No verified catalyst.

**RS leadership:** +43-52% vs BTC (24h). This is exceptional relative strength in a risk-off market. HEI is the single strongest symbol by RS margin.

**Price context:** 24h +47-51% (intraday→swing range). Current ~0.1257 (swing report). Support: 0.0842. Resistance: 0.1458.
- Entry zone (conditional pullback): 0.1192–0.1237. Current price IS above entry zone.
- OI: +10.76–18.67% while price up = fresh positioning confirming the trend (healthy, not a short squeeze).
- Funding: neutral (+5e-5 bybit).

**DO NOT CHASE:** Current price (0.1257) is above the conditional pullback zone (0.1192–0.1237). The momentum_breakout basket explicitly assigns `avoid_chase` playbook. No catalyst confirmed. Counter-tape long against bearish BTC regime = reduce size.

**What would make it actionable:** Pullback to 0.1192–0.1237 on controlled volume + no new bearish catalyst + BTC stabilizing at/above $62K support.

**Verdict:** WATCH ONLY. Trigger: pullback to 0.1192–0.1237. Do not enter above entry zone.

---

### Candidate 4 — TAO/USDT — B-tier swing short — WAITING for entry

**Signal summary:** Score ~65, swing short, status WAITING. Entry around ~22.x zone.

**Context:** TAO is in the AI narrative basket (mixed heat 36-44/100). Price currently ~27 based on the active long signal at 27.x entry. The short signal is waiting for a drop to ~22 — approximately 19% below current price.

**This is a distant trigger.** No imminent action. Monitor if BTC resumes downtrend and AI narrative basket fades.

**Verdict:** WAITING. Not actionable this window. Monitor.

---

### Candidate 5 — UNH (UnitedHealth) — Stocks Monday planning — AVOID for directional trade

**Legal risk:** DOJ probe confirmed (Medicare fraud + Optum Rx antitrust investigation). Shares -16% on news (QuiverQuant, June 2026). This is an active investigation, not resolved.

**Stocks status:** CLOSED today (Juneteenth). The 16:20 review identified META B-tier short (70.29) as the Monday candidate. UNH carries legal/headline risk that makes it a **MANUAL REVIEW REQUIRED** rather than actionable: if the DOJ probe expands or new charges surface over the weekend, Monday open could gap significantly.

**For Monday (June 22 RTH open):**
- META B-tier short: if SPY is weak at open AND META fails first 15-min bounce → actionable
- UNH: AVOID as a directional trade (legal risk). Monitor for further DOJ developments over weekend.
- SMCI: AVOID (export-control indictment).

**Verdict:** UNH = AVOID. META = Monday watchlist (not actionable today). SMCI = AVOID.

**Excess candidates (>5):**
- NEAR/USDT scalp short (B, 65.7): low-confidence scalp playbook (PF 0.14); watchlist-only unless confidence improves.
- XPL/USDT: TP1 CLOSED — no further action.
- BNB: single-source catalyst, sell-the-news risk, C-tier watchlist only.

---

## 8. Best Candidates Ranked

**No clean A-tier candidates. Best B-tier entries already taken:**

| Rank | Symbol | Direction | Playbook | Status | Trigger/Action |
|------|--------|-----------|----------|--------|----------------|
| 1 | AVAX/USDT | SHORT | `crypto_failed_bounce_short` | **ENTERED UNRESOLVED** | Monitor TP1 6.035; stop 6.204 |
| 2 | XLM/USDT | SHORT | `crypto_failed_bounce_short` (swing) | **ENTERED UNRESOLVED** | Monitor TP1 0.2160; stop 0.2248 |
| 3 | HEI/USDT | LONG (counter-tape) | `crypto_swing_narrative_rs_momentum` | **WATCH ONLY** | Pullback to 0.1192–0.1237 required |
| 4 | TAO/USDT | SHORT | `crypto_failed_bounce_short` (swing) | **WAITING** | Far trigger ~22.x; monitor |
| 5 | UNH | SHORT | `stocks_intraday_rth_momentum` | **Monday planning only** | Confirm at RTH open June 22 |

**Best long-watch:** HEI/USDT — trigger: pullback to 0.1192–0.1237 with controlled volume, BTC holding above $62K.
**Best short-watch:** TAO/USDT swing short — trigger: TAO drops to ~22.x entry zone (distant, monitor).
**Best catalyst-watch:** UNH — trigger: Monday June 22 RTH open, DOJ probe + SPY weak + first-15min structure confirms short.

---

## 9. Avoid / No Trade

*This decision window only — does not reflect a system-level command. Scanning continues in all moods.*

- **CHZ/USDT**: Crowded short (funding -0.000637 MEXC; crowding unknown). Avoid new short — squeeze risk if BTC bounces.
- **HOME/USDT**: Elevated crowding at OKX (funding -0.0022); short crowding at MEXC too. Avoid new short.
- **BNB/USDT long**: Single-source catalyst (EASY Residency teaser). Sell-the-news risk. Avoid.
- **HEI/ATM/SYN/EDEN chase longs**: Above entry zones; `avoid_chase` playbook from momentum_breakout basket. Do not enter above pullback zone.
- **UNH**: Legal/headline risk — AVOID directional trade until DOJ probe status clarifies.
- **SMCI**: Active indictment — AVOID.
- **NEAR scalp short**: Low-confidence scalp playbook (WR 12%, PF 0.14); not worth the risk in this window.
- **TRX long**: Overextended (>2 ATR from EMA20) — rejected in reports.

---

## 10. Main Risks

1. **AVAX squeeze risk** (HIGH): OI +17.92% on price decline. If BTC bounces from $62K intraday, AVAX shorts could squeeze to 6.204 invalidation rapidly. Monitor BTC closely.
2. **Correlated short cluster** (MEDIUM): AVAX + XLM + potential TAO = 3 correlated crypto shorts. All stop simultaneously if BTC regime reverses.
3. **Weekend gap risk** (MEDIUM): XLM swing short carries weekend gap risk. BTC could move 3-5% over Sat/Sun without ability to react quickly.
4. **Catalyst mapping weakness** (MEDIUM): 96% events untyped — could be missing a narrative catalyst that invalidates short thesis (e.g. macro positive surprise weekend).
5. **Derivatives data sparse** (LOW): MEXC fallback for multiple symbols; OI numeric history thin. Squeeze phase mapping for 4 symbols in phase_2 not identified by symbol.
6. **Enriched review source ingest**: Script `ingest_enriched_review_sources` will be attempted below; on failure logged here, review continues.

---

## 11. Action Plan — Next 4 Hours

| Time window | Action | Priority |
|-------------|--------|----------|
| Now | Monitor AVAX/USDT — TP1 at 6.035, stop at 6.204 | HIGH |
| Now | Monitor XLM/USDT — TP1 at 0.2160, stop at 0.2248 | HIGH |
| Now | Watch BTC $62K support — if BTC bounces sharply, AVAX squeeze risk activates | HIGH |
| ~20:00-21:00 EEST | Late-session risk review slot (21:30) will handle next evaluation | SCHEDULED |
| Saturday pre-open | No new US stock entries possible (market closed weekend) | N/A |
| Monday June 22 | Re-evaluate META B-tier short at RTH 9:30am ET | PLANNED |
| Monday June 22 | UNH — check DOJ status; if probe expands, confirm AVOID | PLANNED |
| Ongoing | TAO swing short: monitor for drop to ~22.x entry zone | LOW |

**Do NOT:** Chase HEI/ATM/SYN above entry zones. Add to AVAX/XLM shorts without analysis. Enter any stock position today (market closed). Disable scanner or stop monitoring.

---

## 12. Final Verdict per Mode

| Mode | Status | Verdict |
|------|--------|---------|
| Crypto scalp | Low confidence (WR 12%, PF 0.14) | Watchlist only; no new scalp entries tonight |
| Crypto intraday | AVAX entered | Monitor entered AVAX short; no new entries without clean setup |
| Crypto swing | XLM entered; TAO waiting | Monitor XLM short; TAO watching; HEI long only on pullback |
| Stocks intraday | CLOSED (Juneteenth) | Monday June 22 only |
| Stocks swing | Watchlist-only (paused) | Monday planning only |
| Stocks invest | Watchlist-only (paused) | Monday planning only |

---

## 13. Sources

External sources used in this review:

1. [Bitcoin and Ethereum prices today, Friday, June 19, 2026: Prices keep falling post-Fed decision](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-june-19-2026-prices-keep-falling-post-fed-decision-123239380.html) — Yahoo Finance, June 19 2026. BTC $62,882→$62,498 at 8:30am ET; ETH $1,709→$1,687; post-FOMC context. **confirms / used for regime and price context**. Verification: primary_source.

Internal sources (all derived from project data; not external citations):
- `data/reports/scalp/2026-06-19_12-54_scalp_report.md`
- `data/reports/intraday/2026-06-19_13-06_intraday_report.md`
- `data/reports/swing/2026-06-19_13-40_swing_report.md`
- `data/reports/stocks/intraday/2026-06-19_15-32_stocks_intraday_report.md`
- `data/reports/stocks/swing/2026-06-19_13-54_stocks_swing_report.md`
- `data/scheduled_runs/2026-06-19_default_schedule/cycle_01_15-37_summary.md`
- `data/catalysts/2026-06-19/catalyst_events.jsonl` (via report §5b)
- `data/processed/llm_analysis_packet.md`
- `OPUS_ENRICHED_REVIEW_AUTO_2026-06-19_1620.md` (previous review)

---

## 14. Fix Requests / TODO

### TODO-CATALYST-MAPPING-PERSISTENT
- **issue:** Catalyst event mapping remains weak (96% "other_news") across multiple consecutive runs. 307/320 events untyped in the latest cycle scan.
- **evidence:** `data/scheduled_runs/2026-06-19_default_schedule/cycle_01_15-37_summary.md` step 4: "Catalyst scan ok — events=320, baskets=5" but report §5b shows 307/320 other_news.
- **suggested manual fix:** Audit symbol resolver and event classifier in catalyst layer. Improve keyword→event_type mapping for common headline patterns (earnings, upgrades, regulatory). Consider LLM-assisted classification for the "other_news" bucket.
- **priority:** medium
- **first observed:** 2026-06-19 18:39 EEST (recurring across prior reviews)

### TODO-AVAX-SQUEEZE-MONITOR
- **issue:** AVAX entered with OI +17.92% on price decline — squeeze risk is high. No automated squeeze phase alerting specific to entered positions.
- **evidence:** Intraday report §3: "AVAX: price down + OI up: fresh shorts pressing, possible squeeze if price reclaims". Active signals show status=triggered. Phase distribution shows phase_2_squeeze_expansion = 4 symbols but symbol names not identified.
- **suggested manual fix:** Add squeeze-phase symbol identification to the intelligence layer output so the review can check whether a newly entered short is in phase_2. Consider alerting when entered position's OI change exceeds +10% on price decline.
- **priority:** medium
- **first observed:** 2026-06-19 18:39 EEST
