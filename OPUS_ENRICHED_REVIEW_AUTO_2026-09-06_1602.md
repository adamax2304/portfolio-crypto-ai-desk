# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:02 EEST

## 1. Executive Summary

**Advisory only / no auto-trade.** Slot: **pre-US-open decision review**, target 08:50 ET, actual fire ~08:54 ET (Δ+4min, within tolerance). **Critical context this run: today (2026-09-06) is a Sunday — there is no US cash open today at all.** The pre-US-open framing (gap risk, RTH confirmation, first-15-min chase risk) does not apply; this run is pure planning/carry-forward for stocks until Monday's real pre-open. Crypto is the only live actionable class this window. Time-critical hand-off (`stocks-preus-candidates` → `stocks-preus-review-ingest`) ran first: **0 eligible candidates, health status NO_ELIGIBLE** — expected on a weekend, nothing to score, nothing ingested. Crypto regime: bullish trend / risk-on technicals (BTC/ETH uptrend, 93.3% breadth) layered under a real geopolitical macro overhang (Iran/Strait-of-Hormuz, Russia-Ukraine talks, macro risk 63.8/100). **0 A-tier signals** in either asset class over the last 48h. The Robinhood-Chain-adjacent narrative cluster (ARB/UNI/SUSHI/BNB) remains the dominant crypto story, but ARB has been **downgraded from actionable B-tier to C-tier watchlist** since the last review 4h ago. Weekend-mode cohort continues to be the single biggest known risk factor on today's book (historical PF 0.70, winrate ~11% for weekend-flagged signals). No pause/disable recommendation — scanning continues in all moods.

## 2. Data Used

- `data/reports/intraday/2026-09-06_11-45_intraday_report.md` (fresh, ~1h09m old at review time)
- `data/reports/swing/2026-09-06_02-54_swing_report.md` (10h old — **carry-forward**, 4–12h bracket)
- `data/reports/stocks/intraday/2026-09-04_19-53_stocks_intraday_report.md` (Friday close, market closed since — **stale/context-only**, expected on weekend)
- `data/reports/stocks/swing/` and `.../invest/` — last populated **2026-07-02** (deprecated per prior project decision to remove old stocks swing/invest paths; not treated as a freshness failure)
- `data/reports/scalp/` — last populated **2026-08-30** (7 days old; scalp appears currently disabled/deprioritized, not a fresh-data source this run)
- `data/catalysts/2026-09-06/catalyst_events.jsonl` (2,000 events read this cycle), `narrative_baskets.jsonl`
- `data/processed/llm_analysis_packet.md` (fresh, 14:47 EEST) / `llm_stocks_packet.md` (Sep 4 18:59, weekend carry-forward)
- `python -m src.cli active-signals --asset-class crypto` / `--asset-class stocks`
- `python -m src.cli signal-stats --asset-class crypto` / `--asset-class stocks`
- `python -m scripts.detect_untracked_legacy_alerts --since 2026-09-06`
- `news_items` / `proposed_signals` tables (read-only queries, internal-first per §G)
- `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` + `stocks-preus-review-health` output (hand-off)
- Previous review `OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_1139.md` (Europe/pre-US slot, ~4h20m earlier) for §4 comparison
- No external WebSearch/WebFetch run this cycle — internal records for the top candidates were fresh (<24h) and consistent with the prior review's already-ingested/verified sources; per §G this was sufficient and external research was not required this pass.

## 3. Scheduler / Data Freshness

- Pre-US schedule check: target 08:50 ET, actual fire 08:54 ET (Δ+4min, within tolerance). DST note: today is outside both 2026 mismatch windows (2026-03-08→03-29, 2026-10-25→11-01); the standard 7h Nicosia-vs-NY offset holds (verified: NY 08:54 EDT = 15:54 EEST at fire time).
- Time-critical hand-off: `stocks-preus-candidates` → `eligible=0, excluded=0`; `stocks-preus-review-health` → `status=NO_ELIGIBLE`. No ingest needed (nothing eligible to score). Completed well before the 09:12 ET deadline.
- Scheduler folder: `data/scheduled_runs/2026-09-05_default_schedule/` — `scheduler.log` mtime ~16:00 EEST (current), latest `cycle_05_11-23_summary.md` at 12:35 EEST, cycle 06 in progress. **Both well within the 3h freshness gate — no defer.**
- Intraday crypto report: fresh (~1h old). Swing crypto report: 10h old → **carry-forward** (4–12h bracket, used with flag per rule).
- Stocks intraday: last Friday close (market closed all weekend) — context-only, expected. Stocks swing/invest: long-stale (early July) — known-deprecated paths per prior project decision, not a fresh signal source.
- Scalp: 7 days stale — appears currently disabled/deprioritized; excluded from this review's actionable set.
- **Recurring scheduler issue, escalating:** `refresh obsidian dashboard` has now timed out on **6/6** observed cycles today (23:12, 02:09, 06:01, 09:23, 12:35, 16:00 EEST) — up from 3/3 at the last review. See §14.
- **Continuing pattern:** paper-execution/paper-portfolio scheduler steps (accounting refresh, structural TP/stop, paper-shadow A/B, portfolio ledger, entry-mode classify, intelligence layer update) continue to time out repeatedly in the same log window (44 total `CMD TIMEOUT` lines in today's log vs. 30 observed at the last review's cutoff). See §14.
- No monitor/paper-portfolio status file was read beyond the scheduler log; paper P&L visibility should be treated as potentially lagging given the timeout pattern above.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-09-06 16:02 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.72,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks intraday fresh RTH data (market closed, weekend)", "paper portfolio status file not directly read"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime ~16:00 EEST", "cycle_05_11-23_summary.md at 12:35", "swing report 10h old", "stocks reports weekend-stale"] },
    { "agent": "market_regime", "verdict": "ok", "confidence": 0.68,
      "reason_codes": ["risk_on", "mixed", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH uptrend, breadth 93.3%/91.1% above EMA20/50", "macro risk score 63.8/100 (Iran/Hormuz, Russia-Ukraine)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.60,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": ["SUSHI's externally-verified catalyst rows carry no published_at timestamp in news_items"],
      "suggested_effect": "advisory_only",
      "facts_used": ["68.7% catalyst_events unmapped today (2000 read)", "ARB/UNI internal news_items <24h confirm Robinhood Chain cluster", "SUSHI catalyst previously WebFetch-verified (buyback effective 2026-09-07)"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.52,
      "reason_codes": ["oi_supports", "squeeze_risk", "data_unavailable"],
      "data_missing": ["OI 24h reported n/a for several top candidates via fallback_via_mexc"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HEMI: negative funding across Bybit/MEXC, crowding elevated on external cross-check", "ARB/UNI/SUSHI derivatives fallback via MEXC, OI change n/a in this cycle's report"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_fresh", "chase_risk", "clean_retest"],
      "data_missing": ["today's exact live price-vs-zone distance not independently re-verified beyond the report text"],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNI/SUSHI pullback zones stated in report, ~0.2 ATR discipline per playbook", "TAO 4.31x volume breakout with no strong catalyst behind it — chase risk if bought at market"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["waiting_for_entry", "open_actionable", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto (48h): 21 triggered, 6 waiting_for_entry, 4 tp2_hit, 1 tp1_hit, 0 A-tier", "stocks (48h): 2 tp2_hit, 1 tp1_hit (Friday), 2 C-tier tp1_hit, 0 A-tier", "9 untracked legacy crypto alerts today — no backing proposed_signal, needs_review", "GE stocks A-tier position from 2026-08-18 (tp1_hit) still surfacing in the active tracker — stale-position hygiene flag"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.70,
      "reason_codes": ["correlation_cluster", "reduce_risk", "legal_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ARB/UNI/SUSHI/BNB all inside the same Robinhood-Chain-adjacent narrative", "weekend-mode cohort PF 0.70 / ~11% triggered winrate historically", "XRP flagged block_requires_operator_review (wallet-breach headline) in production risk warnings"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto tier=B: triggered winrate 18% (n=204, reliable)", "mode=swing PF 2.525/avgR 0.19 vs mode=intraday PF 1.82/avgR 0.29 (n=113)", "no-catalyst intraday momentum sub-cohort 14d WR 23%/PF 0.70 (per report's own playbook note)"] },
    { "agent": "head_trader", "verdict": "manual_review",
      "confidence": 0.60,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "UNI/USDT", "trigger": "pullback fill into stated intraday/swing zone; do not chase above current price", "reason": "internal news_items confirm Robinhood-Chain burns + Arthur Hayes OTC buy within 24h; B-tier actionable both intraday and swing" },
    "best_short_candidate":    { "symbol": "HEMI/USDT", "trigger": "confirmed 1h close below recent swing low + failed bounce into EMA20", "reason": "bias=short both scans (-16.1%/24h), but audit-capped against bullish regime and funding/crowding elevated (squeeze-prone) — manual-only, not armed" },
    "best_catalyst_candidate": { "symbol": "SUSHI/USDT", "trigger": "pullback fill; avoid market chase given the 24h move already booked", "reason": "governance-approved weekly buyback effective 2026-09-07 + Launch V2 on Robinhood Chain (previously WebFetch-verified, carried forward — no re-verification needed this cycle)" },
    "avoid_candidate":         { "symbol": "COTI/USDT", "reason": "today's top-scoring B-tier idea (67.1) but explicitly 'no fresh verified catalyst detected', running under the known-losing crypto_intraday_catalyst_or_momentum no-catalyst sub-cohort (14d WR 23%/PF 0.70)" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.72 | scheduler_fresh, report_stale | advisory_only |
| market_regime | ok | 0.68 | risk_on, mixed, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, fresh_catalyst, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.52 | oi_supports, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_fresh, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | caution | 0.68 | waiting_for_entry, open_actionable, needs_review | advisory_only |
| risk_manager | caution | 0.70 | correlation_cluster, reduce_risk, legal_risk | advisory_only |
| playbook_performance | caution | 0.62 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution (synthesis) | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-06_1139.md` (Europe/pre-US-context slot), ~4h20m earlier.

- **Downgraded:** **ARB/USDT** moved from the previous review's **best long candidate (B-tier, actionable, score 69.4)** to **C-tier watchlist-only this cycle (score 64.2)**. The Robinhood-Chain catalyst is still present in internal `news_items` (fresh <24h), but the gated trade score fell below the active-trade threshold — treat as watch-only, not a live long, until it re-clears.
- **New:** **TAO/USDT** entered the B-tier intraday list (score 66.6, 4.31x volume, breakout tag) but carries no genuine catalyst — internal `news_items` returns only a generic "price prediction" piece and a stale (Sep 2) token-unlock warning. Treat as a technical breakout play only, chase-risk if bought at market.
- **Persistent:** UNI/USDT and SUSHI/USDT remain B-tier, catalyst-backed, actionable (both intraday and, per the 10h-old carry-forward swing report, swing). BNB/USDT remains inside the `binance_ecosystem_teaser` basket as the flagged primary but is now showing only C-tier/shadow status with low volume ratio (0.4x) — consistent with the prior review's "sell-the-news risk" caution, no upgrade.
- **Persistent/worse:** Catalyst mapping weak-this-run pattern continues: **68.7% unmapped** today (vs 66.3% at the last review, 63.8% at 04:39) — a third consecutive cycle of worsening mapping.
- **Persistent/worse:** `refresh obsidian dashboard` timeout now confirmed on **6/6** observed cycles (was 3/3 at last review) — full escalation, see §14.
- **Unchanged:** 0 A-tier crypto or stocks setups (48h check); HEMI/USDT remains the cleanest audit-capped short-watch idea; weekend-mode cohort remains the dominant risk factor for anyone acting on today's B-tier book; stocks remain closed with 0 eligible pre-US-review candidates (expected on a Sunday).
- **New this cycle (hand-off specific):** the stocks pre-US structured hand-off ran cleanly — `stocks-preus-candidates` returned 0 eligible / 0 excluded, `stocks-preus-review-health` returned `NO_ELIGIBLE`. This is expected (no premarket activity on a Sunday) and is not itself an anomaly, but it means today's pre-US-open decision review has **no stocks decision content** — a genuine first for this slot type on a weekend.

## 5. Catalyst Coverage

- Total `catalyst_events` today (this read): **2,000**
- Mapped (non-null symbol): **627 (31.3%)**
- Unmapped (null symbol): **1,373 (68.7%)**
- `narrative_baskets` today: **6** (perps_dex_narrative, ai_narrative, binance_ecosystem_teaser, delisting_thin_liquidity, rwa_narrative — same set as the last review, no new basket this cycle)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (68.7% unmapped, worse than 66.3% at 11:39 and 63.8% at 04:39 — third consecutive worsening reading, see TODO in §14 note)
- Top 3 unmapped headlines (sample): Kremlin/Kushner-Witkoff Ukraine-talks wire updates, a White House Russia-Ukraine statement, a CZ/YZi Labs investment commentary piece — these are macro/geopolitical wire items and a crowd-commentary piece, not obviously symbol-attributable; consistent with the prior review's note that some of this unmapped share is expected noise rather than a pure resolver bug.

### Pre-US Stocks Review Overlay
- candidates reviewed: 0 (SUPPORT 0 / NEUTRAL 0 / CAUTION 0 / BLOCK 0 / INSUFFICIENT_DATA 0)
- session-cap-only C's now eligible for pre-open Paper lane: 0
- excluded by hard gate: 0 (none — the code returned zero eligible and zero excluded candidates; no premarket stock activity to review on a Sunday)

## 6. Market Landscape

BTC and ETH are both in confirmed uptrends with 93.3%/91.1% of tracked altcoins above EMA20/EMA50 respectively — a genuinely broad, technically risk-on tape. Layered on top of that is a real geopolitical macro overhang: Iran/Strait-of-Hormuz-adjacent headlines and ongoing Russia-Ukraine talks (Witkoff/Kushner in Kyiv, via Moscow) are driving the macro risk score to 63.8/100. This is not crypto-specific yet, but it is a standing tail-risk, and it is compounded today by genuinely thin weekend liquidity. The dominant crypto-native narrative remains the **Robinhood Chain / tokenized-stocks DEX cluster** (ARB as host L2 — now demoted to watchlist; UNI via fee burns and a disclosed OTC buy; SUSHI via Launch V2 + a weekly Strategic Reserve buyback effective tomorrow; BNB as an early, still-unconfirmed rotation candidate). Because today is Sunday, stocks contribute zero decision content to this slot — the "pre-US-open" framing this review is nominally built for does not have a live open to prepare for; the next genuine pre-US-open review is Monday.

### Market Mood / Risk Routing

- Crypto mood: **risk-on (technical), with a geopolitical macro overhang** — mixed-but-actionable, not danger/chop.
- Stocks mood: **closed (Sunday, no cash open today)** — pure planning/carry-forward, zero fresh RTH or premarket data.
- Dominant narrative: Robinhood Chain / tokenized-stocks DEX rotation (UNI, SUSHI catalyst-confirmed; ARB now watchlist-only; BNB unconfirmed/low-volume).
- Preferred side now: **longs, selective — RS-leader + catalyst-backed only (UNI, SUSHI); avoid the no-catalyst intraday momentum sub-cohort** (14d WR 23%/PF 0.70) that COTI, TAO, ADA, STRK, ENA, CAKE currently sit in.
- Best long candidate: **UNI/USDT** (actionable, B-tier both intraday and swing, catalyst-confirmed internally <24h).
- Best short candidate: **HEMI/USDT** (watch only — audit-capped against the bullish regime, funding/crowding elevated = squeeze-prone if chased).
- Best catalyst-backed candidate: **SUSHI/USDT** (buyback effective 2026-09-07, Launch V2 live; catalyst previously externally verified and carried forward).
- What to avoid: **COTI/USDT** (top-scoring but explicitly no-catalyst, known-losing sub-cohort) and any *new* no-catalyst intraday long (TAO, ADA, STRK, ENA, CAKE); **BNB/USDT** as new exposure (still low-volume/unconfirmed rotation, C-tier/shadow only this cycle).
- What would change the view: ARB re-clearing the active-trade score threshold on a fresh catalyst re-check; a confirmed 1h close below HEMI's recent swing low with a failed EMA20 bounce (arms the short manually); de-escalation or escalation out of the Iran/Strait-of-Hormuz or Russia-Ukraine threads; BTC losing uptrend structure (would flip the "selective longs" style off); Monday's actual pre-US-open data replacing this weekend's placeholder read.

## 7. Candidate Deep Dives

**TradingView / manual chart check unavailable this cycle** — all price/ATR/EMA/support-resistance figures below are taken directly from the local report's own OHLCV fields, no external chart tool was consulted.

### 1. UNI/USDT — LONG, B-tier intraday (score 66.1) / B-tier swing (10h carry-forward), actionable

- **Catalyst confirmation:** Internal `news_items` (last 24h): AMBCrypto (2026-09-06T03:00Z) "Uniswap's Robinhood Chain boom fuels $1M in daily UNI burns"; CryptoBriefing (2026-09-06T00:47Z) "Arthur Hayes buys 244,406 UNI for $1.73M in a quiet OTC deal." Both still within the 24h window at review time — genuinely fresh, not carried-forward stale claims.
- **Price reaction / chase check:** The scan-time per-symbol catalyst check in today's intraday report says "no fresh verified catalyst detected" for UNI — this is the known scan-time news-linkage gap (the mechanical per-cycle check under-fires vs. a manual `news_items` query); the manual check above overrides it per §G source discipline.
- **Structure:** Uptrend, setup quality 71.9/100, RR to TP1 1.84R (intraday). Entry plan: pullback into 6.928-6.995 (intraday); invalidation 1h close beyond 6.847.
- **Actionable now or after confirmation?** Actionable now on a disciplined pullback fill; do not chase above the zone.
- **Chase-risk verdict:** Low-moderate — the OTC buy and burns note are both same-day, but burns are a recurring structural flow rather than a one-off headline, so some of the reaction may already be priced.
- **Legal/headline risk:** None found for UNI specifically.

### 2. SUSHI/USDT — LONG / catalyst-backed, B-tier intraday (score 66.1), actionable

- **Catalyst confirmation:** Internal `news_items` has **zero fresh (<24h) rows** for SUSHI, consistent with the report's own "no fresh verified catalyst detected" note. However, two externally-verified rows from the prior review's ingest are present in `news_items` (CoinMarketCap: Launch V2 on Robinhood Chain + weekly Strategic Reserve buyback effective **2026-09-07**; Yahoo Finance/CoinGecko aggregation: +33.5%/24h, OKX Singapore trade-only listing). These carry no `published_at` timestamp (a data-quality gap in the ingest, not treated as invalidating), but the underlying event (tomorrow's buyback) is still forward-looking and has not yet resolved — the catalyst remains live. Per §G ("internal records present, recent, and consistent — reuse them"), no fresh external research was required this cycle.
- **Structure:** Uptrend, setup quality per intraday report; entry plan pullback into 0.2363-0.2407; invalidation 1h close beyond 0.2309.
- **Actionable now or after confirmation?** Actionable now on the pullback plan; avoid chasing above the zone given the 24h move already largely booked.
- **Chase-risk verdict:** Moderate — real, dated catalyst (tomorrow's buyback), but a third of the recent move may already reflect anticipation.
- **Legal/headline risk:** None found.

### 3. ARB/USDT — DOWNGRADED to C-tier / watchlist-only (score 64.2, was B-tier 69.4 four hours ago)

- **Catalyst confirmation:** Internal `news_items` still shows fresh (<24h) Robinhood Chain coverage: CryptoBriefing (2026-09-06T11:28Z, OI/momentum), t.me/wublockchainenglish (2026-09-06T04:20Z, Offchain Labs/Solana fee-model debate), The Motley Fool (2026-09-05 21:00 EDT, "soared 45%... is ARB a buy?"). The catalyst is not gone — the gated composite score simply fell below the active-trade threshold this cycle.
- **Price reaction / chase check:** 24h move is still large (+47.5%), 7d +121.6% — the weekly move remains substantially priced in; the score drop is consistent with the setup getting more extended/lower-quality on a risk-adjusted basis rather than the catalyst weakening.
- **Actionable now or after confirmation?** Watchlist only. Conditional pullback zone 0.1880-0.1927; needs the gated score to re-clear the active threshold before treating as live again.
- **What would invalidate/reactivate:** A pullback into the conditional zone with the score re-clearing threshold would reactivate; a 1h close beyond 0.1823 invalidates the underlying thesis if activated.
- **Legal/headline risk:** None found.

### 4. TAO/USDT — technical breakout, no catalyst backing, chase-risk if bought at market

- **Catalyst confirmation:** Internal `news_items` (any window) returns only a generic "TAO Price Prediction: 2025, 2026, 2030" content piece (2026-09-05T14:12Z, not a real catalyst) and a stale (2026-09-02) token-unlock warning ($1.535B tokens unlocking across the market, not TAO-specific). **No genuine fresh catalyst found.**
- **Price reaction / chase check:** 4.31x 20-period volume, tagged breakout, but only +0.5%/24h and +1.13%/7d — the volume expansion has not yet translated into a large price move, which cuts both ways (could be early accumulation, or could be a low-conviction spike).
- **Actionable now or after confirmation?** B-tier score (66.6) makes it technically "actionable" per the report, but per playbook rules ("no-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation") this should wait for a confirmed breakout close, not be chased on volume alone.
- **Chase-risk verdict:** Moderate-high without a catalyst; treat as watch-and-confirm, not an immediate market entry.
- **Legal/headline risk:** None found.

### 5. HEMI/USDT — Best short-watch, manual only, not armed

- **Setup:** -16.1%/24h intraday, bias=short, weakest symbol on today's scan alongside GIGGLE, TUT, PUMP.
- **Derivatives:** Negative funding, "crowding elevated" flagged on external cross-check in the prior review's deep dive (same underlying condition persists — a fresh short chase here is more squeeze-prone than a fresh short).
- **Catalyst:** None found in `news_items` for HEMI — a pure technical breakdown, not catalyst-driven.
- **Actionable now or only after confirmation?** Manual/watch only; the desk's own audit caps this against the bullish-trend regime, so it will not arm automatically.
- **What would invalidate the idea:** A reclaim of EMA20 with volume, or funding flipping toward short-covering.
- **Legal/headline risk:** None found.

## 8. Best Candidates Ranked

1. **UNI/USDT** — best long, actionable now (intraday + swing), catalyst-confirmed internally <24h.
2. **SUSHI/USDT** — best catalyst-backed, actionable now, catalyst carried forward from prior verified ingest (buyback effective tomorrow).
3. **ARB/USDT** — best long-watch, catalyst still present but gated score fell to C-tier; re-check after next cycle for threshold re-clear.
4. **HEMI/USDT** — best short-watch, manual-only, audit-capped; trigger = confirmed breakdown + failed EMA20 bounce.
5. **TAO/USDT** — best "watch-only technical" idea; trigger = confirmed breakout close on volume, not a market chase.

## 9. Avoid / No Trade

This applies to the **current decision window only** — scanning, tracking, and the scheduler continue regardless.

- **COTI/USDT and other new no-catalyst intraday longs (ADA, STRK, ENA, CAKE, FIL):** all explicitly "no fresh verified catalyst detected" and running under the known-losing `crypto_intraday_catalyst_or_momentum` no-catalyst sub-cohort (14d WR 23%/PF 0.70/−3R).
- **BNB/USDT as new exposure** — still C-tier/shadow, low volume ratio (0.4x), unconfirmed "sell-the-news"-risk rotation per the desk's own narrative note; no upgrade since the last review.
- **Any HEMI short at market** — the system audit-caps this against the current regime; only a confirmed technical trigger (see §7.5) should be considered, and only manually.
- **Stocks (all modes):** no trade of any kind — market is closed, zero pre-US-review candidates today.

## 10. Main Risks

1. **Weekend-mode edge is historically poor** (PF 0.70, ~11% triggered winrate historically for weekend-flagged signals) and essentially all of today's freshest B-tier signals are weekend-flagged — the single biggest risk factor for anyone acting on today's book.
2. **Geopolitical macro overhang** (Iran/Strait-of-Hormuz, Russia-Ukraine talks) scoring 63.8/100 — not crypto-specific yet but could compress risk appetite quickly over thin weekend liquidity.
3. **Correlated exposure** — UNI, SUSHI, (and to a lesser extent now-demoted ARB and unconfirmed BNB) all sit inside the same Robinhood-Chain-adjacent narrative cluster; a reversal in that specific story would hit several of today's ideas at once.
4. **Catalyst mapping is weak and worsening for a third straight cycle** (68.7% unmapped, up from 66.3% and 63.8%) — treat the catalyst layer as directional context only this run.
5. **Scheduler reliability degrading:** `refresh obsidian dashboard` now fails on 100% of observed cycles (6/6), and a widening set of paper-execution/paper-portfolio steps continue to time out — paper P&L visibility used elsewhere may be lagging (see §14).
6. **No live stocks decision content this slot** — this pre-US-open review has nothing to say about the actual next US cash open (which is Monday, not today); do not extrapolate today's "0 eligible" result as a signal about Monday's setup quality.

## 11. Action Plan — next 4 hours

- Watch UNI/USDT and SUSHI/USDT for pullback fills into their stated zones; do not chase above current price on either.
- Watch ARB/USDT for the gated score to re-clear the active-trade threshold before treating it as a live long again; the catalyst itself remains intact.
- Do not add new COTI, TAO, ADA, STRK, ENA, CAKE, or BNB exposure this window under the no-catalyst / unconfirmed-rotation caution above.
- Monitor HEMI/USDT for a confirmed breakdown + failed EMA20 bounce as a manual short trigger; do not chase the existing move.
- Watch the Iran/Strait-of-Hormuz and Russia-Ukraine headline threads for escalation/de-escalation.
- No stocks action possible or expected until Monday's actual pre-US-open window; today's 0-eligible result is a weekend artifact, not a Monday forecast.

## 12. Final Verdict per Mode

- **Crypto intraday:** Selective longs only, catalyst-backed preferred (UNI, SUSHI). No-catalyst momentum longs (COTI/TAO/ADA/STRK/ENA/CAKE) are watchlist/no-trade this cycle given the known-losing sub-cohort stats. ARB downgraded to watch pending score re-clear.
- **Crypto swing:** Actionable on the same UNI/SUSHI catalyst-backed names per the 10h carry-forward swing report; treat as carry-forward context, re-verify next fresh swing cycle.
- **Crypto scalp:** Disabled/deprioritized (last report 7 days old), unchanged.
- **Stocks (all modes):** Closed — Sunday, zero pre-US-review-eligible candidates, zero fresh RTH data. Nothing actionable; next genuine decision point is Monday's actual pre-US-open window.
- **System-wide:** Scanning, tracking, and monitors continue as normal — no pause/disable recommendation.

## 13. Sources

- Internal `news_items` (AMBCrypto, 2026-09-06T03:00Z): "Uniswap's Robinhood Chain boom fuels $1M in daily UNI burns."
- Internal `news_items` (CryptoBriefing, 2026-09-06T00:47Z): "Arthur Hayes buys 244,406 UNI for $1.73M in quiet OTC deal."
- Internal `news_items` (CryptoBriefing, 2026-09-06T11:28Z): "Altcoin open interest rises as ZEC, BNB, ARB, XRP, and SOL gain momentum."
- Internal `news_items` (t.me/wublockchainenglish, 2026-09-06T04:20Z): "Offchain Labs and Solana Co-Founders Debate Robinhood Chain Fee Model."
- Internal `news_items` (The Motley Fool Investing, 2026-09-05 21:00 EDT): "This Little-Known Altcoin Powering Robinhood's New Blockchain Just Soared By 45%. Is ARB a Buy, Sell, or Hold?"
- Internal `news_items` (previously ingested, CoinMarketCap): "SushiSwap (SUSHI) Latest Updates — Launch V2 on Robinhood Chain, weekly Strategic Reserve buybacks" (published_at not recorded — carried forward from prior review's WebFetch verification, event effective 2026-09-07, not yet resolved).
- Internal `news_items` (Benzinga Movers, 2026-09-05T14:12Z): "Bittensor (TAO) Price Prediction: 2025, 2026, 2030" — generic content, cited to show the *absence* of a genuine TAO catalyst.
- `data/catalysts/2026-09-06/catalyst_events.jsonl`, `narrative_baskets.jsonl` — 2,000 events read this cycle, 6 active baskets.
- `data/scheduled_runs/2026-09-05_default_schedule/scheduler.log` — timeout evidence for §14.

## 14. Fix Requests / TODO

### TODO-obsidian-dashboard-timeout-full-escalation (continuing, priority raised)
- **issue:** `refresh obsidian dashboard` has now timed out on **every single observed cycle today (6/6)**: 23:12, 02:09, 06:01, 09:23, 12:35, 16:00 EEST — a full escalation from 3/3 observed at the last review (11:39 EEST) and the first-flagged pattern on 2026-08-31.
- **evidence:** `data/scheduled_runs/2026-09-05_default_schedule/scheduler.log` — `[ERROR] CMD TIMEOUT: refresh obsidian dashboard` at all six timestamps above, each followed by `non-fatal step failed ... cycle continues`.
- **suggested manual fix:** unchanged from prior reviews — profile the step directly (likely vault size or a slow file-write), raise its timeout or move it to an async/best-effort step. Given 100% failure rate is now sustained across a full day, this should be prioritized ahead of the paper-execution timeout pattern below.
- **priority:** high
- **first observed (this escalation):** 2026-08-31; confirmed at 100% failure rate as of 2026-09-06 16:02 EEST.

### TODO-paper-execution-step-timeout-pattern (continuing)
- **issue:** Paper-execution/paper-portfolio scheduler steps continue to time out repeatedly in the same log window flagged at the last review: `paper execution accounting refresh`, `paper-shadow A/B execution`, `paper structural TP refresh`, `paper structural stop plan`, `paper portfolio ledger refresh`, `intelligence layer update`, `paper entry-mode classify`, `market intelligence health (alert-only)`, plus others.
- **evidence:** `data/scheduled_runs/2026-09-05_default_schedule/scheduler.log` — 44 total `CMD TIMEOUT` lines observed in today's log (up from 30 at the last review's cutoff ~4h20m earlier), spanning the full day including entries as recent as 15:46 EEST.
- **suggested manual fix:** unchanged from prior review — check whether cycle duration is trending longer (trailing diagnostic/paper-accounting steps consistently missing their budget); if so, widen timeouts for paper-accounting/portfolio steps specifically, since stale paper P&L visibility undermines promotion-readiness and shadow-lane read-models that depend on it.
- **priority:** medium (escalate to high if paper P&L/portfolio figures used elsewhere are confirmed stale as a result)
- **first observed:** 2026-09-06 11:39 EEST; continuing as of 2026-09-06 16:02 EEST.

### TODO-stale-active-tracker-position (new, low)
- **issue:** `python -m src.cli active-signals --asset-class stocks --tier A` surfaces a GE stocks A-tier position (`sig_bc88416f6f2890b0` and related rows) created 2026-08-18, already `tp1_hit`/`stopped`/`tp1_hit` weeks ago, still appearing in the "active signals" view. This is a tracker-hygiene question, not a scoring or execution issue — it does not affect any live decision, but it does add noise to the active-signals view used by this and future reviews.
- **evidence:** `db/crypto_ai_desk.sqlite` `proposed_signals` table, `symbol='GE' AND tier='A'`, `created_at` 2026-08-17/18, `status` in (`tp1_hit`, `stopped`).
- **suggested manual fix:** review whether `active-signals` should filter out positions with a terminal-ish status (`tp1_hit` without a subsequent close) past some age threshold, or whether this reflects a genuinely unresolved position that should be surfaced differently (e.g., "entered-unresolved, 19 days open").
- **priority:** low
- **first observed:** 2026-09-06 16:02 EEST.

_Recurring note (not a new TODO, already tracked): `detect_untracked_legacy_alerts` again found 9 untracked legacy crypto alerts today (SUSHI, FIL, COTI, UNI, ADA, STRK, ENA, CHIP — all intraday B-tier, sent 2026-09-06 09:08–11:52 UTC) with no backing `proposed_signal`. This is the same watchlist-alert/signal-reuse pattern already raised as a high-priority item on 2026-07-17 (confirmed previously on ALLO/USDT and BANK/USDT) — recorded here only to confirm continued recurrence, not raised as a fresh finding._

_Catalyst mapping weak-this-run (68.7% unmapped, worsening for a third straight cycle) and weekend-mode cohort underperformance are already covered by existing/standing project context (recurring pattern, not a new regression) and are not raised as fresh TODOs this run._
