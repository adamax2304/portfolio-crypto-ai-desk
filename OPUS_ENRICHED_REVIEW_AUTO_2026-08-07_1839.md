# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

## 1. Executive Summary

**Slot: US open reaction review (18:30 EEST slot, run at 18:39 EEST). Advisory only — no auto-trade, no code/scoring changes made.**

- Crypto: no fresh A/B signals fired this cycle (intraday 15:03, scalp 14:52 both empty of A/B). Regime is range/chop with an uptrend bias; 50 prior B-tier signals remain open across scalp/intraday/swing horizons. Route: wait-for-trigger.
- Stocks: bullish regime (VIX 14.96, 100% index/breadth uptrend). 4 B-tier actionable longs fired this cycle — **BKNG is clean** (post-earnings beat, analyst upgrades, RS leader). **META and ABNB both carry real, verified legal/headline risk the system's own risk-warning layer did not surface** — treat both as manual-review, not clean actionable, despite high scores. UBER is post-guidance-miss chase risk.
- 2 untracked legacy alerts recurred today (ALLO, ADA) — same known bug as prior cycles (TODO-3, still open).
- Catalyst mapping is weak this cycle (~56% of today's events unmapped to a symbol) — use catalyst layer as context, not final decision.
- Scanner, monitors, and scheduler continue running in all cases; this review recommends caution on specific names, never system pause.

## 2. Data Used

- Crypto: `2026-08-07_15-03_intraday_report.md`, `2026-08-07_14-52_scalp_report.md`, `2026-08-07_02-55_swing_report.md` (stale, see §3)
- Stocks: `2026-08-07_15-33_stocks_intraday_report.md`
- Catalysts: `data/catalysts/2026-08-07/catalyst_events.jsonl` (3,000 raw rows this file), `narrative_baskets.jsonl`, `catalyst_cycle_15-12.md`
- CLI: `active-signals` (crypto, stocks), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-07`
- External: 4 WebSearch queries (ABNB, BKNG, META, UBER), see §13
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_1612.md` (pre-US-open slot, 18:27 prior)

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-08-07_default_schedule/scheduler.log` mtime: **03:21 EEST** (>15h old) and **no `cycle_*_summary.md` files exist in that folder at all today.** Taken literally, §D's rule would defer this review.
- **Deferred anyway? No.** Actual report artifacts are fresh: scalp 17:52, intraday 18:03, stocks intraday 18:33, catalysts 18:12 — all within the last hour, proving the scheduler is alive and cycling normally (5 stocks-intraday cycles alone since 14:41). The `scheduled_runs/*/cycle_*_summary.md` freshness-check plumbing this skill relies on appears broken/not populated for 2026-08-07 even though the underlying pipeline is healthy. See TODO-6.
- Crypto swing report (`2026-08-07_02-55_swing_report.md`): generated 02:55, now 18:39 → **15h44m old, STALE (>14h threshold)**. Used only as background/carry-forward context in §6, excluded from active verdicts.
- Crypto intraday/scalp: <1h fresh.
- Stocks intraday: <10min fresh (data freshness stamp 15:29 UTC / 18:29 EEST).
- Stocks swing/invest: last report July 2 — stale by over a month, not used.
- Monitor/paper status: not independently queried this cycle (outside the §A allowed CLI list); scheduler cadence (5 stocks-intraday + 1 catalyst cycle in the last 4h) is used as the live-system proxy instead.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-07 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["data/scheduled_runs/2026-08-07_default_schedule/cycle_*_summary.md missing all day despite live reports"],
      "suggested_effect": "advisory_only",
      "facts_used": ["report mtimes 17:52-18:33 EEST", "swing report mtime 02:55 EEST (15h44m old)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["chop", "risk_on", "mixed", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: range/chop, BTC/ETH uptrend, breadth 50%, macro risk 100/100 risk-off headwind", "stocks: bullish, VIX 14.96, breadth 100%, 4/4 indices uptrend"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["~56% of today's catalyst_events.jsonl rows unmapped to a symbol", "BKNG: Trade Desk partnership + analyst upgrade wave is a real, fresh, corroborated catalyst"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["OI 24h % unavailable for most MEXC-fallback symbols (n/a)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BICO/TST/ESP negative funding across bybit/mexc/okx, crowding=elevated", "ALLO: price up + OI down = short covering, weaker continuation"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chase_risk", "entry_late", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp 7b: SPCXB/TST/CRCLB rejected as >2 ATR from EMA20, do-not-chase", "ABNB re-triggered across multiple cycles today (173-176 zone) = late entries piling up"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["100 active signals (crypto 50 + stocks 50): 21 waiting, 45 entered-unresolved, 34 open with partial TP hit, 2 untracked legacy alerts needing review"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["legal_risk", "correlation_cluster", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["META: $942M NM liability + $1.4T trial risk this month, not in production risk-warning list", "ABNB: verified Chicago Shared Housing Ordinance + shareholder-proposal lawsuits, not in production risk-warning list", "ZBT/USDT: 3 separate open swing signals on a symbol down -34.9% 24h = correlation cluster"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_failing", "low_sample", "playbook_working"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp: PF 0.125, 0W/5L (14d) — structurally losing", "crypto swing subset: PF 6.83, +23.3R (14d) — working", "stocks B-tier: n=10 weak sample, 0% winrate", "stocks C-tier: PF 0.14, winrate 1% (n=343, reliable) — by design watchlist-only"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "BKNG", "trigger": "already entered 213.53-214.76 (triggered), hold above stop 212.30, manage toward TP1 218.43", "reason": "RS leader (+17.9% vs SPY 20d), clean beat-and-raise Q2 (Aug 4), RBC Buy + Citi PT to $236 (Aug 7), no legal/earnings flags, bullish regime aligned" },
    "best_short_candidate":    { "symbol": "SYN/USDT", "trigger": "confirmed failed bounce/retest of 0.1094-0.1118 with rejection candle, invalidate above 0.1147 (no formal signal yet, watch only)", "reason": "downtrend, -15.8% 24h, weakest-symbols list two cycles running, but no catalyst or derivatives confirmation yet" },
    "best_catalyst_candidate": { "symbol": "BKNG", "trigger": "already actionable — Trade Desk ad-data partnership + broad analyst upgrade wave", "reason": "only candidate this cycle with a real, multi-source, dated catalyst that is not stale and not contradicted" },
    "avoid_candidate":         { "symbol": "META", "reason": "B-tier long signal (score 68.8) sits directly under active litigation: $567M New Mexico order (total ~$942M liability, Aug 6) plus a $1.4T penalty trial threat this month (CA/CO/KY/NJ, Oakland) and ongoing FTC antitrust — none of this is in the production risk-warning list that correctly caught AMZN/HON/RIOT/BTC" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 8
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.75 | chop, risk_on, mixed, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, entry_late, price_moved_away | advisory_only |
| execution_lifecycle | ok | 0.80 | waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.70 | legal_risk, correlation_cluster, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, low_sample, playbook_working | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_1612.md` (pre-US-open slot, ~18:27 ago).

- **New this cycle:** BKNG, ABNB (re-triggered), UBER, META all newly fired as B-tier stocks-intraday candidates post-US-open — the 16:12 review's best candidates were crypto-only (XAI/USDT long, HEI/USDT short-watch, CSCO catalyst-watch) since stocks hadn't opened yet.
- **Removed / no longer best:** XAI/USDT no longer appears in this cycle's crypto reports at all (neither intraday nor scalp) — likely expired or rotated out of the top-strength list; not confirmed as closed.
- **Thesis carried forward:** HEI/USDT — still unconfirmed as a clean short in both reviews; still the weakest-RS name in this review's scalp desk notes context.
- **New risk finding this cycle:** META and ABNB legal/headline risk (not flagged in the 16:12 review, which only saw an EARNINGS_BLACKOUT gate list for a different symbol set — META was not on that list either, so this is a fresh finding from this cycle's external research, not a contradiction of the prior review).
- **Catalyst coverage:** 46.2% mapped at 16:12 → ~44% mapped (56% unmapped) now — roughly flat, still weak.

## 5. Catalyst Coverage

- Total `catalyst_events.jsonl` rows sampled today: 3,000. Mapped (non-null symbol): 1,323 (44.1%). Unmapped: 1,677 (55.9%).
- Report-stated unique events today: 1,387; narrative baskets: 5 (rwa_narrative, binance_ecosystem_teaser, ai_narrative, delisting_thin_liquidity, momentum_breakout).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top unmapped headlines (sample):
  1. "Pomerantz Law Firm Announces the Filing of a Class Action Against Microvast Holdings, Inc. and Certain Officers - MVST"
  2. "Pomerantz Law Firm Announces the Filing of a Class Action Against Insulet Corporation and Certain Officers - PODD"
  3. "INVESTOR ALERT: Pomerantz Law Firm... ZoomInfo Technologies Inc..."

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **chop** (report label: "range/chop, neutral") with an uptrend bias — BTC uptrend, ETH uptrend, but altcoin breadth only 50% above EMA20/50, and macro/geopolitics score is 100/100 risk-off headwind (Strait of Hormuz oil-deal watch, EU/Russia sanctions escalation).
- Stocks mood: **risk-on / bullish** — VIX 14.96, 4/4 major indices in uptrend, 100% breadth above EMA20/50. Strongest sectors: energy, materials, financials. Weakest: semiconductors, utilities, communications.
- Dominant narrative: crypto — momentum_breakout basket (BICO/EPIC/ALLO, tagged avoid_chase) and rwa_narrative (ONDO/XLM); stocks — post-earnings drift + Q2-season analyst repositioning (BKNG upgrades, UBER downgrades).
- Preferred side now: **stocks longs selectively (RS leaders only, earnings/legal-clean)**; **crypto wait-for-trigger** (no A/B fired this cycle).
- Best long candidate: **BKNG** (see §8).
- Best short candidate: **none confirmed** — best short-watch is SYN/USDT (crypto, see §8).
- Best catalyst-backed candidate: **BKNG** (Trade Desk partnership + analyst upgrade wave).
- What to avoid: **META** (active litigation, see §7) and, secondarily, **ABNB** (unresolved legal exposure) and **UBER** (post-guidance-miss chase risk).
- What would change the view: a confirmed BTC/ETH breakout above range with rising breadth (>65% above EMA20) would flip crypto to risk-on; a VIX spike above ~18-20 or a broad SPY breakdown would flip stocks to risk-off.

## 7. Candidate Deep Dives

### 1. BKNG — B-tier long, stocks intraday — ENTERED UNRESOLVED

- Entry zone 213.53-214.76 (triggered), stop 212.30, TP1 218.43 (RR 1.50), TP2 220.88, TP3 224.56.
- Has price already reacted to the catalyst? Yes — Q2 beat reported Aug 4, stock already trending up into Aug 7; this is post-earnings-drift continuation, not a fresh surprise.
- Chasing? Moderate — entry is above prior-day high, but RS is genuinely leading (+17.9% vs SPY 20d, +17.7% vs sector).
- Retest/pullback structure? No formal retest; momentum entry.
- Overextended (>2 ATR from EMA20)? Not flagged by the system; volume is only 0.74x (unremarkable), reducing blow-off-top risk.
- Actionable now or after confirmation? Actionable now — already triggered.
- Aligned with market mood? Yes — bullish regime, RS-leader long is the preferred routing.
- Long/short/wait? Long.
- Invalidation: close beyond 212.30.
- Chase risk: low-moderate.
- Catalyst confirmation: **confirmed** — RBC Capital Buy rating and Citi PT raise to $236 both dated Aug 7 (today), plus a new Trade Desk ad-data partnership. [Sources: StockTitan, Yahoo Finance — see §13]
- Legal/headline check: no legal flags found in external search or internal risk-warning list. **Clean.**

### 2. META — B-tier long, stocks intraday — MANUAL REVIEW REQUIRED (not a clean actionable)

- Internal signal: score 68.79, entry 593.45-596.05, stop 590.85, TP1 603.84. Internal system tags "earnings: safe" and applies no legal-risk cap.
- **Verified legal/headline risk (external, multi-source):** a New Mexico judge ordered Meta to pay $567M for youth mental-health programs (Aug 6), on top of an earlier $375M penalty — total ~$942M liability in that case alone. Separately, four states (CA/CO/KY/NJ) are seeking ~$1.4T in penalties with a trial expected in Oakland **this month** (August 2026); Meta also faces an active FTC antitrust case. [Sources: Yahoo Finance, Benzinga, 24/7 Wall St. — see §13]
- Price cross-check: external source quotes META at $598.22 (Friday close), consistent with the internal entry zone (593-596) — confirms the external data is current, not stale.
- This is exactly the class of risk §I (legal/headline check) exists to catch, and it was **not caught** by the internal production risk-warning list (which correctly flagged AMZN, BA, BTC, GOOGL, HON, INTC, RIOT this same cycle but omitted META). See TODO-2.
- Verdict: **MANUAL REVIEW REQUIRED / AVOID as a clean long** regardless of the technical score. If traded at all, this is a headline-risk-aware position, not a vanilla momentum long.

### 3. ABNB — B-tier long (×2 signals across cycles), stocks intraday — MANUAL REVIEW REQUIRED

- Two open signals this cycle: sig_c1f683051cad546b (B, 174.16-175.67) from an earlier cycle and a fresh Idea #1 this cycle (173.24-174.78, score 100.0) — the RS-leader long has now triggered across multiple consecutive cycles, which is itself a late-entry / chase-risk signal (§technical_entry).
- **Verified legal exposure:** City of Chicago filed suit June 23, 2026 alleging ~200 unregistered short-term rentals under the Shared Housing Ordinance; separately a shareholder-proposal exclusion lawsuit forced Airbnb to add two proposals to its 2026 annual meeting agenda. Both corroborated by an SEC 8-K primary source and independent trade press. [Sources: SEC EDGAR, StockTitan, Investing.com — see §13] Neither appears in the internal production risk-warning list.
- **Unverified/uncertain claim (flagged, not asserted as fact):** one search result described an Aug 6 earnings report for ABNB, but the price it quoted ($141.88) conflicts sharply with the internal system's live entry zone (~$174) and with META's externally-confirmed price consistency test above — this is most likely a stale/cached index result, not current data. Recommend the operator manually confirm ABNB's true earnings-calendar status rather than trusting this claim; the internal report currently shows no ABNB earnings flag at all (see TODO-1), so either way the earnings-proximity gate needs a human check on this name.
- Verdict: **MANUAL REVIEW REQUIRED** — real litigation risk is confirmed even though the earnings-timing claim is not.

### 4. UBER — B-tier long, stocks intraday — CAUTION, wait for confirmation

- Entry zone 74.52-75.07, stop 73.98, TP1 76.69. Internal report already flags "RS=laggard" and a counter-thesis ("relative strength is not in the leader bucket").
- Q2 2026 reported Aug 5: revenue +12% YoY, EPS beat, but **Q3 guidance missed expectations** — stock fell ~5% on the print. Barclays cut PT to $106 (from $107), Wells Fargo cut to $89 (from $100). Separately, Uber is reportedly in advanced talks to acquire Delivery Hero at a premium, and shares fell further (~2.5%) on that news. [Sources: CNBC, StocksToTrade — see §13]
- This is a stock fighting negative sentiment (guidance miss + analyst downgrades + M&A-rumor uncertainty) despite a technical "above prev day high" trigger. Score (77.94) and RR are fine on paper, but the fundamental backdrop argues against chasing.
- Verdict: **caution — require RTH confirmation (hold above prior-day high into the close) before treating as clean; do not add on further extension.**

### 5. Crypto watch-only — BICO/USDT (long-watch) & SYN/USDT (short-watch)

- No A/B crypto signals fired this cycle. BICO/USDT is the top C-tier watchlist idea (score 63.9, momentum_breakout basket, funding negative/crowded across bybit/mexc/okx) — not active until price pulls back into 0.0472-0.0496 with volume confirmation; currently trading 0.0508, up 37.9% 24h — chasing this now would be buying an extended, crowded-short move.
- SYN/USDT is the cleanest short-side idea on the "weakest symbols" list (-15.8% 24h, downtrend) but has no derivatives or catalyst confirmation yet — watch only, per §8.

## 8. Best Candidates Ranked

1. **BKNG** (long, actionable, entered) — clean RS leader, catalyst-confirmed, no legal flags.
2. **BICO/USDT** (long-watch, crypto) — wait for pullback fill 0.0472-0.0496, invalidate 1h close <0.0441.
3. **SYN/USDT** (short-watch, crypto) — wait for confirmed failed bounce at 0.1094-0.1118, invalidate 1h close >0.1147.
4. **UBER** (long, conditional) — wait for RTH confirmation above prior-day high before treating as clean.
5. META and ABNB are excluded from this ranking — see §9.

## 9. Avoid / No Trade

*(This decision window only — never a command to stop the system, scanner, or data collection.)*

- **META** — active $1.4T litigation trial risk this month + $942M confirmed liability, not reflected in internal risk warnings. Avoid as a clean long; manual review only.
- **ABNB** — real, dated legal exposure (Chicago ordinance suit, shareholder suit) plus an unresolved earnings-calendar question. Manual review only.
- **ZBT/USDT** — three separate open swing signals on a token down -34.9% 24h with declining volume (deleveraging/long-liquidation pattern) — correlation-cluster risk, avoid adding more exposure to this name.
- Crypto scalp mode generally — structurally losing bucket this window (PF 0.125, 0W/5L in 14d); treat any scalp idea with low confidence per the report's own header note.

## 10. Main Risks

- Two verified legal/headline risks (META, ABNB) slipped past the production risk-warning layer this cycle — see TODO-1/TODO-2. If this generalizes, other "clean" B-tier stock signals may be carrying undetected legal exposure.
- Catalyst mapping at ~56% unmapped reduces confidence in any catalyst-backed thesis this cycle.
- Crypto macro risk score is 100/100 risk-off (Strait of Hormuz watch, Russia sanctions escalation) even though price trend is up — a headline-driven reversal is a live tail risk into the evening.
- Untracked legacy alert bug (ALLO, ADA) recurred again today — same root cause as the 2026-07-17 finding, still open (TODO-3).
- ZBT/USDT correlation cluster (3 open swing signals, same losing name) concentrates risk in the active book.

## 11. Action Plan — next 4 hours

- Manage BKNG toward TP1 (218.43); no new entry needed, already triggered.
- Do not chase BICO/EPIC/ALLO momentum-basket names without a confirmed pullback fill.
- Watch SYN/USDT for a confirmed failed bounce before treating as a short candidate.
- Do not add new size to META or ABNB without an operator manually reviewing the legal exposure above.
- Require UBER to hold above its prior-day high into the close before treating the current signal as clean.
- Re-check catalyst mapping and untracked-alert counts at the next scheduled slot (21:30 late-session risk review).

## 12. Final Verdict per Mode

- **Crypto scalp:** no trade — mode disabled by kill-switch this cycle regardless; structurally losing bucket (PF 0.125).
- **Crypto intraday:** no trade — no A/B fired; watch BICO/SYN per §8.
- **Crypto swing:** stale data (15h44m) — treat existing open positions as carry-forward only, no new read this cycle.
- **Stocks intraday:** selective — BKNG actionable/clean; UBER conditional (wait for RTH confirmation); META and ABNB manual-review-only despite high scores.
- **Stocks swing/invest:** stale (>1 month) — not evaluated.

## 13. Sources

- [Airbnb, Inc. - Form 8-K - FY2026](https://www.sec.gov/Archives/edgar/data/0001559720/000119312526337928/d70413d8k.htm) — SEC EDGAR, primary source
- [Airbnb Faces Lawsuit Over Excluded Shareholder Proposals Before Annual Meeting](https://www.stocktitan.net/news/ABNB/airbnb-provides-copies-of-stockholder-complaint-and-alleged-98zch4y8qn1c.html) — StockTitan
- [Airbnb faces lawsuit over proxy statement exclusions](https://www.investing.com/news/company-news/airbnb-faces-lawsuit-over-proxy-statement-exclusions-93CH-4079063) — Investing.com
- [Booking Holdings to Webcast Second Quarter 2026 Financial Results](https://www.stocktitan.net/news/BKNG/booking-holdings-to-webcast-second-quarter-2026-financial-results-on-0pguei3orfl1.html) — StockTitan, 2026-08-04
- [Booking Holdings (BKNG) Stock Falls Amid Market Uptick](https://finance.yahoo.com/markets/stocks/articles/booking-holdings-bkng-stock-falls-220003714.html) — Yahoo Finance
- [Meta's Legal War Just Escalated to $1.4 Trillion](https://finance.yahoo.com/markets/stocks/articles/meta-legal-war-just-escalated-201733224.html) — Yahoo Finance / 24/7 Wall St., 2026-07-07
- [Meta Stock in Focus -- Judge Orders $567 Million Child Safety Payment](https://finance.yahoo.com/markets/stocks/articles/meta-stock-focus-judge-orders-122626372.html) — Yahoo Finance, 2026-08-06
- [Meta's $1.4 Trillion Penalty Scare Is Almost As Big As Meta Itself](https://www.benzinga.com/markets/large-cap/26/07/60309780/metas-1-4-trillion-penalty-scare-is-almost-as-big-as-meta-itself) — Benzinga, 2026-07-01
- [Uber stock sinks 5% after weak guidance despite revenue growth](https://www.cnbc.com/2026/08/05/uber-stock-q2-2026-earnings.html) — CNBC, 2026-08-05
- [UBER Stock Under Pressure As Legal, Deal, And Regulatory Risks Pile Up](https://stockstotrade.com/news/uber-technologies-inc-uber-news-2026_08_05-2/) — StocksToTrade, 2026-08-05

## 14. Fix Requests / TODO

### TODO-1
- **issue:** ABNB B-tier signals show "earnings: safe (no event in the near window)" in the stocks-intraday report, but ABNB is a Q2-season name that may have reported earnings in the last 1-2 days (external search flagged this, though price data in that source was inconsistent/possibly stale). The same report's own §7 C-tier watchlist already demotes DIS for an analogous `stale_post_earnings_setup` gate — that gate did not fire for ABNB.
- **evidence:** `data/reports/stocks/intraday/2026-08-07_15-33_stocks_intraday_report.md` line ~465 ("earnings: safe") vs line 648 (DIS demoted for `stale_post_earnings_setup`); external search result citing an Aug 6 ABNB earnings report (price data unreliable in that source).
- **suggested manual fix:** a human session should verify ABNB's true last-earnings date against a reliable calendar source and confirm whether the internal earnings-calendar ingest is missing this name (same class of gap previously seen with DIS/RIOT-style detection working for some names but not others).
- **priority:** high
- **first observed:** 2026-08-07 18:39 EEST

### TODO-2
- **issue:** META carries active, material litigation (a $567M New Mexico order on top of an earlier $375M penalty = ~$942M total liability, plus a pending $1.4T multi-state penalty trial expected this month) that is not present in the production risk-warning list, even though that same list correctly caught AMZN, BA, BTC, GOOGL, HON, INTC, and RIOT this cycle.
- **evidence:** `data/reports/stocks/intraday/2026-08-07_15-33_stocks_intraday_report.md` §"Production risk warnings" (META absent) vs external sources in §13 (Yahoo Finance, Benzinga, 24/7 Wall St., all corroborating, price cross-checked against internal entry zone).
- **suggested manual fix:** review why the legal-risk news-classification pipeline (src/news/) missed META's ongoing litigation coverage — check symbol-detection/entity-resolution for "Meta"/"META" against these specific stories, and whether the $1.4T-trial coverage is being ingested at all.
- **priority:** high
- **first observed:** 2026-08-07 18:39 EEST

### TODO-3
- **issue:** Untracked legacy alerts recurred again today (ALLO/USDT 12:05 UTC, ADA/USDT 12:37 UTC) — watchlist_alerts fired to Telegram with no matching `proposed_signal` within 6h, so neither will contribute to PF/winrate tracking. This is the same bug already raised to high priority on 2026-07-17 (see memory `project_crypto_ai_desk_watchlist_alert_signal_reuse_bug`), still unresolved.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-07` → 2 untracked legacy crypto alert(s).
- **suggested manual fix:** implement the fix already scoped in the prior finding — mint a new `proposed_signal` instead of reusing a stale/closed `signal_id` on watchlist re-fire.
- **priority:** high
- **first observed:** 2026-07-17 (recurrence confirmed 2026-08-07 18:39 EEST)

### TODO-4
- **issue:** Crypto scalp mode is structurally losing this window: sample=37 (14d), 0 wins / 5 losses on triggered A/B, PF 0.125, avgR -0.117. The report's own header already acknowledges this (kill-switch active, "re-audit at 20 closed A/B scalp signals").
- **evidence:** `signal-stats --asset-class crypto` → `mode=scalp | n=37 | trig=36 | wins=0 | losses=5 | PF 0.125000 | avgR -0.116700`.
- **suggested manual fix:** continue collecting data toward the 20-closed-signal re-audit threshold already planned; no action needed before then.
- **priority:** medium
- **first observed:** 2026-08-07 18:39 EEST (confirms pre-existing known issue)

### TODO-5
- **issue:** `data/scheduled_runs/2026-08-07_default_schedule/` contains only `scheduler.log` (mtime 03:21) and zero `cycle_*_summary.md` files for the entire day, even though the actual report pipeline is clearly healthy (5+ fresh report cycles observed). This breaks the freshness-check mechanism this review skill (§D) depends on to decide whether to defer.
- **evidence:** directory listing of `data/scheduled_runs/2026-08-07_default_schedule/` (1 file only) vs fresh mtimes on `data/reports/**` (within the last hour).
- **suggested manual fix:** investigate why `cycle_*_summary.md` generation stopped writing into the dated `scheduled_runs` folder for 2026-08-07 — check the scheduler script that's supposed to write per-cycle summaries there.
- **priority:** medium
- **first observed:** 2026-08-07 18:39 EEST

### TODO-6
- **issue:** UBER's B-tier signal received full `news_catalyst` score credit (11.00, same as ABNB/BKNG) despite the 8 news items in its lookback window skewing negative (post-earnings guidance miss, two analyst price-target cuts). The scoring does not appear to differentiate catalyst sentiment polarity.
- **evidence:** `data/reports/stocks/intraday/2026-08-07_15-33_stocks_intraday_report.md` UBER Idea #3 score breakdown (`news_catalyst: 11.00`) vs external corroboration of negative UBER coverage (CNBC, StocksToTrade, §13).
- **suggested manual fix:** consider whether `news_catalyst` scoring should weight sentiment/direction, not just count of news items, for the stocks-intraday playbook.
- **priority:** low
- **first observed:** 2026-08-07 18:39 EEST

### TODO-7
- **issue:** Crypto weekend-mode signals continue to underperform (PF 0.5, winrate 11%, n=10, weak confidence) per this cycle's `signal-stats` observations. Distinct from the existing Asia dead-zone guard (which addresses session hours, not weekend specifically).
- **evidence:** `signal-stats --asset-class crypto` observations: "(weak, n=10) weekend=Y: weekend signals underperform (winrate 11%, n=10)."
- **suggested manual fix:** monitor sample growth; if it persists past n=20+, consider a weekend-specific demotion similar to the existing Asia dead-zone guard.
- **priority:** low
- **first observed:** 2026-08-07 18:39 EEST

### TODO-8
- **issue:** `active-signals` CLI returns entries with `expires_at` dates 2+ weeks in the past (e.g. several `tp1_hit`/`tp2_hit`/`triggered` rows expiring 2026-07-21/22) still listed as part of the "active" signal set (50/50 crypto and stocks rows respectively). This makes lifecycle bookkeeping harder to reason about and may be inflating "active" counts in dashboards/telegram summaries.
- **evidence:** `active-signals --asset-class crypto` and `--asset-class stocks` output, rows with `expires_at` in 2026-07-17 through 2026-07-22 range, current date 2026-08-07.
- **suggested manual fix:** review whether `active-signals` should filter out rows with `expires_at` far in the past, or whether these need explicit closing/reconciliation.
- **priority:** low
- **first observed:** 2026-08-07 18:39 EEST
