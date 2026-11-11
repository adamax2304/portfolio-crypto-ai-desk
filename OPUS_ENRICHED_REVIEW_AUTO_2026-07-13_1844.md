# Opus Enriched Review — US open reaction review — Auto Cycle 18:39 EEST

## 1. Executive Summary

**Slot: US open reaction review (nominal 18:30 EEST / ~11:30 ET, ~2h into the US cash session) — advisory only / no auto-trade.** This slot checks which pre-open ideas confirmed or failed, whether the tape is trustworthy or a gap trap, and how crypto is reacting to US flows.

**Scheduler healthy, all data fresh.** Active folder `2026-07-13_default_schedule`, `cycle_02` finished cleanly 17:42 EEST (started 16:57). Crypto scalp/intraday/swing (17:06–17:38 EEST) and stocks intraday (18:34 EEST, data as of 15:33 UTC) are all fresh this cycle — nothing carried forward except the known-deprecated stocks swing/invest reports (still 2026-07-02, ~11 days stale, excluded).

**No A-tier and no B-tier setups fired anywhere this cycle — crypto or stocks.** All four fresh reports (scalp, intraday, swing, stocks-intraday) independently returned "No A-tier setups found" / "No B-tier setups found." This is a genuine no-fresh-signal cycle, not a data gap — coverage, funnel counts, and news ingestion all look healthy in §3.

**Geopolitical escalation is the dominant macro driver and it got worse, not better, since the 16:28 review.** Verified via WebSearch/WebFetch: Iran struck US-allied bases in Kuwait, Bahrain, Jordan, Oman and Qatar overnight; Trump said the US will reinstate a blockade of Iranian shipping in the Strait of Hormuz. Brent crude is up ~2.8% to ~$78/bbl (WTI ~$73). US indices are choppy and directionally inconsistent intraday — one live-blog snapshot showed Dow/S&P/Nasdaq all modestly green (+0.29%/+0.42%/+0.29%), a separate snapshot the same morning showed Dow +0.1%/S&P -0.3%/Nasdaq -0.7% — this two-way chop is exactly what the desk's own stocks regime label captured: **regime flipped from `risk_on` (pre-open, stale Friday-scored) to `chop`** this cycle (VIX 16.24, breadth 50% above EMA20 / 100% above EMA50). BTC/ETH both opened the US session strong then faded — BTC ~$63,043 at 06:15 ET down to ~$62,555 by 09:30 ET; ETH ~$1,805 open down to ~$1,771 — consistent with the desk's crypto regime staying `transition_down`/`bearish, risk-off`.

**Crypto: still short-biased, one aging actionable-adjacent idea.** HYPE/USDT intraday short (B-tier, `perps_dex_narrative` basket primary) has been `waiting_for_entry` since 14:44 EEST — now ~4h without a fill, getting stale; re-check the zone live before treating as fresh. ZEC/USDT — the prior review's catalyst pick — has already progressed to TP in the paper book (see §4), a genuine win to note, not a live idea anymore.

**Stocks: gates are doing their job.** AAPL (raw A-tier, score 82) and 8 other raw B-tier names (META, TSLA, COIN, AMD, SMCI, UNH, MSTR, AMZN) were all correctly demoted B/A→C this cycle by the SI-1..5 actionability gates (`lunch_requires_strong_confirmation`, `liquidity_rvol_below_min`, `catalyst_none_and_not_exceptional_technical`, plus `rr_below_min_required` for AMD/AMZN and an active `legal_headline_risk: sec_doj` block for UNH). **UNH long is a hard AVOID** — verified active DOJ criminal investigation into Medicare billing, not a routine gate demotion. One existing position is still open and being monitored: **AAPL long (B-tier, opened a prior cycle)** — `OPEN_ACTIVE`, entry filled, TP/SL live.

**Catalyst mapping remains weak but flat**: 84.2% unmapped (2909/3454 events) vs 85.0% at 16:28 — marginal improvement, still well above the 50% "context only" threshold (§5, §14).

**Overall verdict: CAUTION, routed by side — not a blanket no-trade.** Crypto: short-biased, watch HYPE/USDT (stale waiting-for-entry, re-verify before trusting) and fresh RS-leader longs only with reduced size given the counter-tape risk. Stocks: chop regime + lunch-session gates correctly blocking new entries; monitor the open AAPL long; avoid UNH outright; do not chase JPM ahead of tomorrow's earnings. Scanning, tracking, and the paper book continue uninterrupted in every mood.

## 2. Data Used

- Crypto scalp report: **fresh** — `2026-07-13_14-06_scalp_report.md` (generated 17:06 EEST; data as of 14:00 UTC). No A/B; regime bearish trend (risk-off), scalp remains kill-switch disabled.
- Crypto intraday report: **fresh** — `2026-07-13_14-12_intraday_report.md` (generated 17:12 EEST; data as of 14:00 UTC). No A/B this cycle; best C-tier watch is EVAA/USDT (score 60.0, resurfaced after dropping out at the 16:28 review).
- Crypto swing report: **fresh** — `2026-07-13_14-38_swing_report.md` (generated 17:38 EEST; data as of 14:30 UTC). No A/B; best C-tier watch is JTO/USDT (score 63.3, RS-leader + OI/volume confirmed).
- Stocks intraday: **fresh** — `2026-07-13_15-34_stocks_intraday_report.md` (generated ~18:34 EEST; data as of 15:33 UTC). Regime **chop** (VIX 16.24, breadth 50%/100%). AAPL raw A-tier (82) + 8 raw B-tier all demoted to C by SI-1..5 gates; 0 actionable A/B. Stocks swing/invest: still 2026-07-02, ~11 days stale, known-deprecated legacy mode, not evaluated.
- Catalysts: `data/catalysts/2026-07-13/catalyst_events.jsonl` (3454 cumulative events today) + `narrative_baskets.jsonl` (5 active baskets as of the 14:14 UTC cycle: `perps_dex_narrative`/HYPE, `rwa_narrative`/ONDO+XLM, `ai_narrative`/NEAR+RENDER+TAO+FET, `binance_ecosystem_teaser`/BNB, `delisting_thin_liquidity`/none). Mapped/unmapped computed directly from the JSONL (see §5).
- CLI: `active-signals --asset-class crypto` (27 rows, HYPE the only non-terminal fresh idea; rest tp1/tp2-hit or older swing/scalp), `active-signals --asset-class stocks` (50 rows, mostly historical tp/no-entry outcomes from Jul 3-11, plus AMZN/TSLA/XOM currently waiting), `signal-stats` crypto (week: n=202, PF 1.05, winrate 13.8%, totalR +3.0), `detect_untracked_legacy_alerts --since 2026-07-13` (**0 found**).
- Paper Monitor Status (`reports/PAPER_MONITOR_STATUS_LATEST.md`, 17:41 EEST): lifecycle counts in §3.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_1628.md` (16:28 EEST, ~2h11m ago) — primary comparison baseline for §4.
- External: 2 WebSearch queries (US stock market + Iran/Hormuz July 13 2026; BTC/ETH price today) + 1 WebFetch (Yahoo Finance live-blog, verified index levels/oil/earnings-week context) — sources in §13.

## 3. Scheduler / Data Freshness

- `scheduler.log` (`2026-07-13_default_schedule`): `cycle_02` started 16:57 EEST, finished cleanly 17:42 EEST — **fresh, not deferred** (~57min old at review time, well under the 3h defer threshold).
- Crypto scalp/intraday/swing: **fresh** this cycle (generated 17:06–17:38 EEST, data as of 14:00–14:30 UTC).
- Stocks intraday: **fresh** (generated ~18:34 EEST, data as of 15:33 UTC, ~6min old) — genuinely live RTH data, not pre-open.
- Stocks swing/invest: **stale** (2026-07-02, ~11 days) — known-deprecated legacy mode per prior audits, excluded from final verdict.
- Untracked legacy crypto alerts: **0** (confirmed this cycle).
- Known non-blocking noise (unchanged, self-documented in every report): Reddit social-attention sources unavailable; Bybit/OKX futures partial coverage; token-unlock/liquidation-heatmap/order-book/on-chain blindspots not automated.
- Paper Monitor Status (17:41 EEST): **Open actionable 1 (AAPL long, stocks/intraday/B) · Waiting for entry 4 (AMZN long stocks/intraday/A, TSLA short stocks/intraday/B, XOM long stocks/intraday/B, HYPE/USDT short crypto/intraday/B) · Review/Shadow 105 · Entered unresolved (expired-after-entry) 6 · No-entry/stale/moved-away 45 · Closed 392W / 24L / 0flat · Needs review 0**.
- HYPE/USDT has been `waiting_for_entry` since 14:44 EEST — now ~4h old; treat the entry zone as needing live re-verification before acting, per §J discipline.
- No legal/headline gate regressions found: UNH's DOJ block, JPM's earnings do-not-chase block, and the standing operator-review flags (BTC/ETH/HOOD/OP/ORCL/XRP) are all still correctly active in production (display/advisory, non-gating for routing) — consistent with the 16:28 review.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-13 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh"],
      "data_missing": ["stocks swing/invest (~11 days stale, known deprecated mode)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_02 started 16:57 EEST, finished cleanly 17:42 EEST", "crypto scalp/intraday/swing fresh (17:06-17:38 EEST); stocks intraday fresh (18:34 EEST, data 15:33 UTC)", "0 untracked legacy crypto alerts"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.55,
      "reason_codes": ["risk_off", "chop", "shorts_preferred", "mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC transition_down, ETH range, altcoin breadth 30-37.5% above EMA20 depending on mode, style 'short bias or no trade'", "stocks regime flipped from risk_on (pre-open, stale) to chop this cycle: VIX 16.24, breadth 50% above EMA20 / 100% above EMA50", "verified BTC $63,043->$62,555 and ETH $1,805->$1,771 fading from the US open per WebSearch (Yahoo Finance)", "verified US indices two-way chop intraday (one snapshot all-green +0.1-0.4%, another mixed Dow+0.1%/S&P-0.3%/Nasdaq-0.7%) driven by Iran/Hormuz headlines"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "narrative_supported", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl direct count: 3454 total, 545 mapped (15.8%), 2909 unmapped (84.2%) — essentially flat vs 16:28's 85.0%, still a persistent resolver gap", "5 active baskets as of 14:14 UTC cycle: perps_dex_narrative (HYPE primary, <6h), rwa_narrative (ONDO/XLM, <24h), ai_narrative (NEAR/RENDER/TAO/FET, <6h), binance_ecosystem_teaser (BNB, <1h), delisting_thin_liquidity (no primary, <6h)", "ZEC/USDT (16:28 review's catalyst pick) has already progressed to TP-hit in the paper book — Orchard-flaw/Top-10 catalyst thesis played out", "EVAA/USDT (best short-watch in earlier reviews, then dropped out) has resurfaced in this cycle's fresh intraday report at score 60.0"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["EVAA/USDT current OI/funding not shown in this cycle's derivatives table"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HYPE/USDT: prior cycle showed neutral external funding, no squeeze flag — thesis unchanged", "SXT/USDT: negative funding (-0.0022 to -0.0030 across scalp/intraday/swing reads), crowding elevated/unknown, explicitly capped 'short squeeze risk -> C' in the scalp report — do not chase the short", "VANRY/USDT: also explicitly capped 'thin_liquidity_short_squeeze_risk' in the scalp report's rejected list", "JTO/USDT: price up + OI up (+1.0% to +11.6% depending on report), funding near-zero, 'fresh positioning confirms trend, monitor crowding' — the cleanest derivatives read of the cycle's watchlist names"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["stale_before_entry", "chase_risk", "clean_retest", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HYPE/USDT: waiting_for_entry ~4h with no fill — needs live re-verification, not a fresh trigger", "JTO/USDT: conditional pullback zone 0.6459-0.6540 across scalp/swing reads, current price 0.6576-0.6580 just above the zone — a pullback-and-hold is required, not a chase of the current print", "SXT/USDT: conditional failed-bounce/retest zone 0.0079-0.0081 across all three crypto reports, current price sitting right in the zone — the cleanest technical level of the cycle, but squeeze-risk-capped", "DODO/XEC/DCR/KITE/ALLO all RS-leaders vs BTC (+10% to +46%) but capped B/C for being counter-tape longs in a bearish-regime tape or MEXC-only/kill-switch issues — do not chase these prints", "AAPL/META/TSLA/COIN/etc (stocks): technically scored but gated by lunch-session liquidity/confirmation rules — textbook 'wait for volume to return, don't chase the lunch lull' setup"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "no_entry", "closed_flat"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Paper monitor (17:41 EEST): Open actionable 1 (AAPL long stocks/intraday/B), Waiting for entry 4 (AMZN long-A, TSLA short-B, XOM long-B stocks; HYPE/USDT short-B crypto), Review/Shadow 105, Entered unresolved 6, No-entry/stale/moved-away 45, Closed 392W/24L/0flat, Needs review 0", "0 A/B setups fired fresh this cycle in any of the 4 fresh reports", "ZEC/USDT swing long already tp-hit in active-signals (crypto) — a completed win, not a live idea"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: active DOJ criminal probe into Medicare billing practices (TipRanks, Medical Economics, 2026-07-13) — production correctly demoted B->C via legal_headline_risk:sec_doj; treat as AVOID, not manual-review-optional", "JPM: earnings tomorrow (2026-07-14), swing-blocked + do-not-chase-warning already active in production, unchanged", "TSLA: Musk settled the SEC Twitter-disclosures securities-fraud suit today for a $1.5M fine (Union Leader) — a de-risking event, not a new overhang, though SPCX (SpaceX) separately hit a post-IPO low <$140 today, a Musk-adjacent headline risk worth noting for correlated names", "Geopolitical: verified Iran struck Kuwait/Bahrain/Jordan/Oman/Qatar overnight; Trump said the US will reinstate an Iranian-shipping blockade in the Strait of Hormuz; Brent +2.8% to ~$78 — a real, escalating headline-risk backdrop for the whole session, not resolved since the pre-open read"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week headline A/B: n=202, winrate 13.8%, PF 1.05, avgR 0.018, totalR +3.0 — broadly unchanged in character from the 16:28 read", "by mode: scalp worst (PF 0.32-0.33, kill-switch disabled for good reason), intraday roughly breakeven (PF 0.98-0.99), swing best (PF 1.4-1.5, +10R)", "weekend-mode signals continue to outperform weekday this week (PF ~3.2 vs ~0.6)", "stocks headline A/B weak sample (n=10, PF 1.02, +0.07R); stocks C-tier watchlist PF 0.78, winrate 14.7%, week totalR -8.5 — weak but not Telegram-actionable, unchanged pattern"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.55,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "shorts_preferred",
    "best_long_candidate":     { "symbol": "JTO/USDT (swing watch, counter-tape, reduce size)", "trigger": "pullback into 0.6459-0.6540 zone and hold, with OI/volume staying confirmed; invalidation on 1h close below 0.6360" },
    "best_short_candidate":    { "symbol": "SXT/USDT (failed-bounce/retest watch, squeeze-risk capped)", "trigger": "rejection inside 0.0079-0.0081 zone with hold below invalidation 0.0083; do not chase given elevated short-squeeze risk flag" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT (already waiting_for_entry, ~4h stale)", "trigger": "live re-verify the 65.376-65.681 failed-bounce zone before trusting the fill; perps_dex_narrative basket still fresh" },
    "avoid_candidate":         { "symbol": "UNH (active DOJ Medicare-fraud probe) + chasing any stock name during the lunch-liquidity lull", "reason": "UNH carries a verified, still-open DOJ criminal investigation (legal_headline_risk:sec_doj) — hard avoid, not manual-review-optional; stocks broadly are gated by SI-1..5 lunch/RVOL/catalyst rules with 0 actionable A/B this cycle" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh | advisory_only |
| market_regime | mixed | 0.55 | risk_off, chop, shorts_preferred, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.6 | mapping_weak, catalyst_confirmed, narrative_supported, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.5 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | stale_before_entry, chase_risk, clean_retest, overextended | advisory_only |
| execution_lifecycle | ok | 0.7 | open_actionable, waiting_for_entry, review_shadow, no_entry, closed_flat | advisory_only |
| risk_manager | caution | 0.6 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.55 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Comparison baseline: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_1628.md` (16:28 EEST, pre-US-open decision review).

- **Stocks regime flipped from `risk_on` (pre-open, Friday-stale scoring) to `chop` (this cycle, live RTH data)** — VIX essentially flat (16.27→16.24) but breadth above EMA20 collapsed from 100% to 50%. This confirms the 16:28 review's caution ("demand first 15-30min RTH confirmation") was warranted: the 8 A-tier stock longs scored pre-open (META, DIA, AVGO, NVDA, TSLA, QQQ, AMD, SPY) have **largely evaporated from this cycle's top-15 table** — only META (now B→C, score 78) survives from that list; AAPL is a new name at the top (raw A, score 82) that wasn't in the pre-open book at all.
- **ZEC/USDT — the 16:28 review's best catalyst-watch candidate — has already closed TP** in the paper book (see active-signals: `ZE.../swing/tp...`). A genuine win to log, not a live idea to re-pitch.
- **EVAA/USDT resurfaced.** It had dropped out of the top-40 universe at 16:28 (flagged as stale); it is back in this cycle's fresh intraday report as the #1 C-tier watch (score 60.0). Its unwind/failed-bounce thesis is re-verifiable again.
- **HYPE/USDT is unchanged but aging** — still `waiting_for_entry` since 14:44 EEST, now ~4h stale. Treat with more caution than at 16:28; re-verify the zone live rather than assuming it's still valid.
- **Catalyst mapping essentially flat**: 84.2% unmapped now vs 85.0% at 16:28 — the multi-cycle regression trend has stopped worsening but has not meaningfully improved (§14).
- **Geopolitical situation escalated, not de-escalated**: at 16:28 the read was "conflict has widened, not cooled"; verified external research now confirms a formal US blockade declaration on Iranian shipping in the Strait of Hormuz plus expanded Iranian strikes on five countries (Kuwait, Bahrain, Jordan, Oman, Qatar) — this is a step up in severity, not a plateau.
- **TSLA de-risked on one front**: the Musk/Twitter-disclosures SEC securities-fraud suit settled today for a $1.5M fine — a resolved overhang, though unrelated SpaceX (SPCX) weakness (post-IPO low) is a fresh Musk-adjacent headline to watch.
- No untracked legacy alerts in either review (0 → 0).

## 5. Catalyst Coverage

- Total catalyst events today (cumulative, direct JSONL count): **3454**.
- Mapped (non-null symbol): **545 (15.8%)**.
- Unmapped (null symbol): **2909 (84.2%)**.
- Narrative baskets: **5** active (`perps_dex_narrative`/HYPE, `rwa_narrative`/ONDO+XLM, `ai_narrative`/NEAR+RENDER+TAO+FET, `binance_ecosystem_teaser`/BNB, `delisting_thin_liquidity`/none).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (84.2% > 50% threshold, essentially flat vs 85.0% at 16:28.)
- Top 3 unmapped headlines sampled this cycle:
  1. "French President Macron: It is today's wars that we have to win..." — political/geopolitical commentary, no tradeable ticker to resolve to.
  2. "InMode expects Q2 revenue above estimates" — this **should** resolve to a real single-stock ticker (INMD) and didn't; a concrete resolver-gap example (§14).
  3. "Best Railroad Stocks" — generic sector listicle, no single ticker; low-value noise the resolver correctly can't map, but inflates the denominator.

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **risk-off / bearish trend** — BTC `transition_down`, ETH `range`, altcoin breadth 30-37.5% above EMA20 depending on mode; verified BTC/ETH both faded from their US-open highs (BTC $63,043→$62,555, ETH $1,805→$1,771).
- Stocks mood: **chop** (VIX 16.24, bias neutral, breadth 50% above EMA20 / 100% above EMA50); verified US indices whipsawing intraday on Iran/Hormuz headlines rather than trending cleanly either direction.
- Dominant narrative: geopolitical escalation (Iran strikes on 5 countries + US blockade declaration on the Strait of Hormuz) driving oil higher (Brent +2.8% to ~$78) and keeping both crypto and equities choppy/risk-averse; secondary narrative is Hyperliquid/perps-DEX (HYPE) and RWA/tokenization (ONDO/XLM) in crypto.
- Preferred side now: **shorts-preferred in crypto (reduce size, demand confirmation)**; **wait-for-trigger in stocks** — the lunch-session gates are correctly blocking new entries until liquidity/confirmation returns.
- Best long candidate: JTO/USDT (swing watch, counter-tape — see §7/§8).
- Best short candidate: SXT/USDT (failed-bounce/retest watch, squeeze-risk capped — see §7/§8).
- Best catalyst-backed candidate: HYPE/USDT (already in the pipeline, stale — needs live re-verify).
- What to avoid: UNH (active DOJ probe); chasing any stock print during the lunch liquidity lull; chasing any of the RS-leader crypto longs (DODO/XEC/DCR/KITE/ALLO) at current extended prints.
- What would change the view: a clear de-escalation headline on Iran/Hormuz (would likely unwind the chop and let stocks trend), or BTC reclaiming and holding above its local range highs (would flip crypto's short bias).

## 7. Candidate Deep Dives

### 7.1 JTO/USDT — swing long watch (best long-watch)
- Score 63.3/100, confidence medium, playbook `crypto_swing_narrative_rs_momentum` (14d WR 72% / PF 5.80 / +24R — the desk's strongest mode).
- RS vs BTC +10.4%, volume 4.43x 20-period average, derivatives: price up + OI up (+1.0%), funding near-zero — genuinely fresh positioning, not stale.
- Has price already reacted to the catalyst? No verified fresh catalyst; this is a pure RS/momentum read.
- Is the setup chasing? Current price (0.6576-0.6580) sits just above the proposed 0.6459-0.6540 pullback zone — waiting for a pullback-and-hold, not chasing the current print.
- Retest/pullback structure? Yes — explicit conditional pullback zone defined.
- Overextended (>2 ATR from EMA20)? Not flagged as such in the report.
- Would entry now be late? Yes if bought at market; the zone requires a pullback first.
- Level that makes it actionable: hold above 0.6459-0.6540 zone on a retest, invalidation on 1h close below 0.6360.
- Aligned with current market mood? Only partially — it's a long in a bearish-tape regime ("counter-tape long — reduce size, demand confirmation" is explicitly flagged in the report).
- Long, short, or wait-for-trigger? Wait-for-trigger long.
- Actionable now or after confirmation? After confirmation (pullback + hold).
- What invalidates it? 1h close below 0.6360, or BTC breaking down further against the regime thesis.
- Chase-risk setup? Low chase risk at current levels given the defined pullback zone; would become chase risk if bought at market without the retest.
- Catalyst confirmation/contradiction? No catalyst either way — pure technical/derivatives read.

### 7.2 SXT/USDT — failed-bounce short watch (best short-watch)
- Score 58.9-60.0/100 depending on report, confidence low-medium, playbook `crypto_intraday_catalyst_or_momentum` / `crypto_failed_bounce_short` (no-catalyst cohort: 14d WR 23% / PF 0.70 / −3R — a known-weak playbook without confirmation).
- RS vs BTC -9.2% to -9.6%, volume 2.33-2.47x (real participation), derivatives: price down + OI down (deleveraging/long liquidation), funding notably negative (-0.0022 to -0.0030) — **short-squeeze risk explicitly capped in the scalp report** (`thin_liquidity_short_squeeze_risk`, `high_upper_wick_short_squeeze_risk`).
- Has price already reacted? Yes — already down 11-13% over 24h; this is a failed-bounce/retest thesis, not a fresh breakdown.
- Is the setup chasing? No — current price (0.0079-0.0080) sits inside the proposed 0.0079-0.0081 retest zone.
- Retest/pullback structure? Yes, explicit.
- Overextended? Not flagged beyond the general "no-catalyst chop is net-negative" playbook warning.
- Would entry now be late? No, price is in the zone, but negative funding argues for a tight stop given squeeze risk.
- Level that makes it actionable: rejection inside 0.0079-0.0081, hold below invalidation 0.0082-0.0083.
- Aligned with mood? Yes — shorts-preferred regime, weak-RS name.
- Long/short/wait-for-trigger? Short, but treat as squeeze-risk-capped — smaller size, tighter stop than usual.
- Actionable now or after confirmation? Needs confirmation of rejection at the zone, not a market short.
- What invalidates it? 1h close above 0.0082-0.0083, or BTC/ETH reclaiming local levels.
- Chase-risk? Low if entered on rejection; the squeeze-risk flag is the primary hazard, not chase risk.
- Catalyst? No fresh verified catalyst confirming or contradicting.

### 7.3 HYPE/USDT — intraday short, already waiting_for_entry (best catalyst-watch)
- B-tier, `perps_dex_narrative` basket primary, fresh <6h basket membership; external funding neutral, no squeeze flag at last read.
- Already in the pipeline since 14:44 EEST (~4h), status `waiting_for_entry` — has NOT yet filled.
- Has price reacted to the catalyst? Partially — the basket thesis (Hyperliquid/perps-DEX rotation) is intact but this specific signal has aged without a fill.
- Chase risk? None currently — it hasn't triggered.
- Retest structure? Yes, per the original 65.376-65.681 failed-bounce zone (16:28 review) — **needs live re-verification given the ~4h age**, not to be treated as still-fresh without a current price check.
- Actionable now or after confirmation? Only after live re-verification of the zone; do not assume the original level still holds after 4h.
- What invalidates it? Original invalidation 1h close beyond 66.053 (subject to re-check); if the basket rotates out or HYPE breaks the invalidation level, drop the idea.
- Catalyst confirmation? Basket still shows fresh (<6h) as of this cycle's narrative_baskets.jsonl — thesis technically alive but the specific trade age argues for caution over conviction.

### 7.4 UNH — stocks long, hard AVOID (legal/headline risk)
- Raw B-tier (score 66), demoted B→C for `legal_headline_risk: sec_doj`.
- Verified from two independent sources today (TipRanks, Medical Economics): active DOJ criminal investigation into Medicare billing/fraud practices.
- Per §I protocol: **this is not a manual-review-optional situation — final verdict is AVOID.** Any UNH long idea, however clean technically, is blocked until this legal overhang is resolved or the desk receives an update showing it's closed/immaterial.
- Separately, UNH earnings are in 3 trading days — an additional reason to stay out regardless of the legal risk.

### 7.5 AAPL — open existing long position (monitor only, not a new idea)
- **Already OPEN** in the paper book (B-tier, prior cycle entry) — entry filled, TP/SL live, per Paper Monitor Status.
- This cycle's fresh stocks-intraday report separately re-scored AAPL as raw A-tier (score 82) but demoted to C via `lunch_requires_strong_confirmation`, `liquidity_rvol_below_min`, `catalyst_none_and_not_exceptional_technical` — that re-score is **not** a new signal, just today's gate-correct read on a fresh scan; the live position is a separate, earlier trade already being monitored.
- News flow is mixed-to-negative for AAPL today: Apple suing OpenAI/ex-employees over alleged trade-secret theft (adds legal noise, not yet a block-level risk), offset by the SigScalr acquisition (routine, non-material). No action needed beyond continuing to monitor the existing position's TP/SL.

## 8. Best Candidates Ranked

1. **JTO/USDT — best long-watch.** Wait for pullback into 0.6459-0.6540 and hold; counter-tape, reduce size.
2. **SXT/USDT — best short-watch.** Wait for rejection inside 0.0079-0.0081; squeeze-risk capped, smaller size / tighter stop.
3. **HYPE/USDT — best catalyst-watch.** Already `waiting_for_entry`; re-verify the 65.376-65.681 zone live before trusting the ~4h-old level.
4. **AAPL — monitor only.** Existing open long (B-tier); no new action, just track TP/SL.

No A/B-tier setup cleared the desk threshold in either asset class this cycle — the above are watchlist-tier candidates with explicit triggers, per PART 9 (never a bare "no trade").

## 9. Avoid / No Trade

- **UNH long** — active DOJ criminal Medicare-fraud investigation; hard avoid this decision window (see §7.4). Re-check when the legal situation resolves.
- **New stock entries generally, this cycle** — 0 actionable A/B; SI-1..5 gates (lunch confirmation, RVOL floor, catalyst-quality floor) are correctly blocking AAPL/META/TSLA/COIN/AMD/SMCI/MSTR/AMZN. This is a decision-window call, not a scanner-stop — scanning and tracking continue.
- **Chasing crypto RS-leader longs at current extended prints** (DODO/XEC/DCR/KITE/ALLO) — all counter-tape against the bearish regime; several also carry `crypto_scalp_disabled` or MEXC-only-listing caps. Wait for a pullback into a defined zone, don't buy the extended print.
- **JPM** — earnings tomorrow (2026-07-14); do-not-chase-warning already active in production, unchanged.

## 10. Main Risks

- Geopolitical escalation (Iran/Strait of Hormuz) is verified worsening, not stabilizing — oil spiking, indices whipsawing. A headline-driven gap in either direction is plausible before the close.
- HYPE/USDT's waiting_for_entry signal is aging (~4h) — a stale zone traded without re-verification risks a bad fill.
- SXT/USDT short carries an explicit squeeze-risk flag (negative funding, elevated crowding per the scalp report) — a crowded-short unwind could produce a sharp adverse wick.
- Catalyst mapping at 84.2% unmapped means the news layer should be treated as context, not proof, for any candidate this cycle.
- UNH's DOJ investigation is a standing tail risk for any healthcare-adjacent basket exposure, not just UNH itself.

## 11. Action Plan — next 4 hours

- Re-verify HYPE/USDT's failed-bounce zone live before treating the waiting signal as tradeable; if the zone has moved meaningfully, treat the idea as stale and drop it.
- Watch JTO/USDT for a pullback into 0.6459-0.6540 with a hold; watch SXT/USDT for a rejection inside 0.0079-0.0081 — both are watch-only until confirmed.
- Continue monitoring the open AAPL long (B-tier) through its existing TP/SL; no new action needed.
- Do not open new UNH exposure regardless of technical score while the DOJ investigation is active.
- Re-check the Iran/Hormuz headline flow before the next cycle — a resolution or further escalation would meaningfully change both the crypto and stocks risk routing.
- Track whether the stocks regime stays `chop` or resolves directionally once lunch-session liquidity picks back up later in the US afternoon.

## 12. Final Verdict per Mode

- **Crypto scalp**: No trade. Kill-switch remains disabled; regime bearish/risk-off.
- **Crypto intraday**: No A/B. Watch EVAA/USDT (resurfaced, score 60) and HYPE/USDT (aging waiting-for-entry) only with live re-verification.
- **Crypto swing**: No A/B. Watch JTO/USDT (best long-watch, counter-tape) and SXT/USDT (best short-watch, squeeze-capped).
- **Stocks intraday**: No A/B — 0 actionable after SI-1..5 gates; chop regime. Monitor the existing open AAPL long only. UNH is a hard avoid.
- **Stocks swing/invest**: Not evaluated this cycle (data ~11 days stale, known-deprecated legacy mode).

## 13. Sources

- [Stock market today: Dow rises, S&P 500 and Nasdaq slip as US and Iran exchange fire, oil jumps](https://finance.yahoo.com/markets/live/stock-market-today-monday-july-13-dow-sp-nasdaq-113249278.html) — Yahoo Finance, 2026-07-13 (live-blog, index levels + earnings-week context, verified via WebFetch).
- [Live updates: Ceasefire disintegrates as Trump says US will reinstate blockade of Iranian ships in Strait of Hormuz](https://www.cnn.com/2026/07/13/world/live-news/iran-war-trump) — CNN, 2026-07-13.
- [US and Iran exchange strikes as Strait of Hormuz standoff escalates](https://www.cnbc.com/2026/07/13/us-iran-war-hormuz-oil-trump.html) — CNBC, 2026-07-13.
- [Oil prices jump as US and Iran trade attacks over Strait of Hormuz](https://www.aljazeera.com/economy/2026/7/13/oil-prices-jump-as-us-and-iran-trade-attacks-over-strait-of-hormuz) — Al Jazeera, 2026-07-13.
- [Bitcoin and ethereum prices today, Monday, July 13, 2026: Strong price openings backtracking this morning](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-july-13-2026-strong-price-openings-backtracking-this-morning-133042462.html) — Yahoo Finance, 2026-07-13.
- Internal: `data/reports/scalp/2026-07-13_14-06_scalp_report.md`, `data/reports/intraday/2026-07-13_14-12_intraday_report.md`, `data/reports/swing/2026-07-13_14-38_swing_report.md`, `data/reports/stocks/intraday/2026-07-13_15-34_stocks_intraday_report.md`, `data/catalysts/2026-07-13/catalyst_events.jsonl`, `data/catalysts/2026-07-13/narrative_baskets.jsonl`, `reports/PAPER_MONITOR_STATUS_LATEST.md`.

## 14. Fix Requests / TODO

### TODO-catalyst-resolver-gap
- **issue:** Catalyst symbol-mapping resolver remains at 84.2% unmapped (flat vs 85.0% at 16:28, part of a multi-cycle regression first flagged weeks ago).
- **evidence:** `data/catalysts/2026-07-13/catalyst_events.jsonl` direct count: 3454 total, 545 mapped, 2909 unmapped. Concrete example: "InMode expects Q2 revenue above estimates" (a clear single-ticker INMD headline) unmapped this cycle — see §5.
- **suggested manual fix:** Audit the symbol-resolver's ticker/company-name dictionary for gaps on real single-stock earnings/guidance headlines (not just the generic-listicle/geopolitical noise that's correctly left unmapped); consider a targeted regression test using headlines like the InMode example.
- **priority:** medium
- **first observed:** recurring, re-confirmed across the 2026-07-13 04:44/11:46/16:28/18:39 EEST cycles.

### TODO-hype-stale-waiting-signal
- **issue:** HYPE/USDT intraday short has sat in `waiting_for_entry` for ~4h (since 14:44 EEST) without a fill or an automatic staleness re-flag distinct from the general "waiting" bucket.
- **evidence:** `reports/PAPER_MONITOR_STATUS_LATEST.md` (17:41 EEST) still lists HYPE/USDT as plain `WAITING_FOR_ENTRY`, no age-based sub-status.
- **suggested manual fix:** Consider adding an age threshold (e.g. >3h) to the waiting_for_entry display so operators/reviews don't need to manually compute signal age from the alert timestamp each cycle.
- **priority:** low
- **first observed:** 2026-07-13 18:39 EEST.
