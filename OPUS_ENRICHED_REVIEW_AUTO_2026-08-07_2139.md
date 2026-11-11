# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

## 1. Executive Summary

Late-session risk review (21:30 EEST slot). **Advisory only — no auto-trade, no code/scoring changes.** Scheduler is fresh (scheduler.log 21:30, monitors alive). Crypto flipped from range/chop mid-day to a bullish-trend/risk-on tape by evening (breadth 71–76% above EMA20/50), but macro/geopolitical risk score sits at 100/100 (Strait of Hormuz, Iran, Russia-sanctions escalation) — a headline-driven reversal is a live tail risk overnight. No fresh A/B crypto ideas fired this cycle (scalp/intraday both no-trade); 20 crypto B-tier swing/intraday positions remain open, none new. Stocks: 15 A-scored names all gate-demoted to C (liquidity/catalyst/sector confirmation), zero A/B actionable this cycle; one carried-forward ABNB B-tier position is still open with an unresolved earnings-date verification gap (TODO-1, still open). Catalyst mapping is weak this run (55.9% unmapped) — treat catalyst layer as context only. Two correlation clusters (ZBT/USDT ×2 longs on a token down -34.7% 24h; ADA/USDT ×3 longs) warrant operator attention, not new size.

## 2. Data Used

- `data/reports/scalp/2026-08-07_18-39_scalp_report.md` (generated 21:39 EEST, data freshness 18:30 UTC)
- `data/reports/intraday/2026-08-07_15-03_intraday_report.md` (generated 18:03 EEST, data freshness 14:45 UTC)
- `data/reports/swing/2026-08-07_16-15_swing_report.md` (generated 19:14 EEST, data freshness 16:00 UTC)
- `data/reports/stocks/intraday/2026-08-07_18-36_stocks_intraday_report.md` (data freshness 18:33 UTC)
- `data/catalysts/2026-08-07/catalyst_events.jsonl`, `narrative_baskets.jsonl`, latest cycle `catalyst_cycle_15-12.md`
- `active-signals --asset-class crypto` / `--asset-class stocks`, `signal-stats` (both classes), `detect_untracked_legacy_alerts --since 2026-08-07`
- Direct read-only SQL on `db/crypto_ai_desk.sqlite`: `proposed_signals`, `signal_outcomes` (lifecycle counts, correlation clustering)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_1839.md`
- 2 WebSearch queries (BTC Coldcard/ETF inflow corroboration; ZBT/USDT news check) — both used, results below

External web research **was** available this cycle (used for BTC and ZBT verification).

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-08-06_default_schedule/scheduler.log` — mtime **2026-08-07 21:30** (~9 min old) → **fresh**, review proceeds.
- `derivatives_monitor_1786127410.log` mtime 21:30, `fast_news_monitor` mtime 21:38 → monitor processes alive.
- Crypto scalp report: generated 21:39 EEST — as fresh as it gets.
- Crypto intraday report: generated 18:03 EEST, underlying data 14:45 UTC (~4h old) → **carry-forward**, flagged; regime read from this file (range/chop) is superseded by the fresher scalp/swing reads (bullish trend).
- Crypto swing report: generated 19:14 EEST, data 16:00 UTC (~2h40m old) → fresh enough for swing.
- Stocks intraday report: generated 18:36 EEST, data 18:33 UTC (~6 min old) → fresh.
- Stocks swing/invest reports: last generated 2026-07-02 → **retired/deprecated** (per prior system decision, replaced by a separate shadow-only `stocks_swing_growth_breakout` framework, not yet routing) — excluded from this review, not treated as a stale-data problem.
- **TODO-5 carried forward (see §14):** `data/scheduled_runs/2026-08-07_default_schedule/` still has zero `cycle_*_summary.md` files (scheduler.log only, mtime 03:21) — the scheduler is writing today's cycles into the `2026-08-06_default_schedule/` folder instead. Freshness check in this run used the folder that actually has fresh data; the dated-folder mechanism itself remains broken.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-08-07 21:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 21:30", "crypto intraday data 14:45 UTC (~4h old)", "stocks intraday data 18:33 UTC (~6 min old)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_on", "longs_preferred", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto breadth 71-76% above EMA20/50 (scalp/swing)", "macro risk score 100/100 risk-off (Strait of Hormuz, Russia sanctions)", "stocks VIX 14.91, breadth 100% above EMA20/50"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "no_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 1677/3000 (55.9%) unmapped today", "most open crypto B-tier swing longs flagged 'no fresh verified catalyst detected'"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["oi_contradicts", "funding_extreme", "data_unavailable"], "data_missing": ["OI history for MEXC-fallback-only symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/USDT: price up + OI down (short covering, weak continuation) repeated across scalp/intraday/swing", "BICO/USDT: negative funding across bybit/mexc/okx, crowding elevated"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "clean_retest", "overextended"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/TUT/SPCXB flagged >2 ATR from EMA20, do-not-chase (scalp §7b)", "BICO/EPIC/ALLO tagged momentum_breakout/avoid_chase basket (intraday §5b)", "open swing B-tier entries used disciplined pullback zones, not market chases"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 20 open_actionable (B triggered), 2 waiting_for_entry, 6 entered_unresolved (scalp expired w/ entry filled, 0R unresolved), 4 no-entry/stale/moved-away, 14 stopped + 2 partial-win today", "stocks: 1 open_actionable (ABNB, carried), 18 review/shadow (C triggered), 22 waiting (mostly C), 130 no-entry/stale across the day (research volume), 8 stopped"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["correlation_cluster", "legal_risk", "reduce_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZBT/USDT: 2 open swing longs on a token -34.67% 24h (correlation cluster, fighting the trend)", "ADA/USDT: 3 open positions (swing+intraday) + 1 fresh untracked alert today (concentration)", "REGN correctly demoted for active class-action/securities-fraud risk", "HON, RIOT, BONK, BTC correctly flagged by production risk-warning layer", "ABNB open B-tier position still carries the unresolved earnings-date verification gap from prior review (TODO-1)"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing/RS-momentum playbook 14d WR 72% / PF 5.80 (mode-level PF 6.82 in signal-stats)", "crypto scalp structurally losing, PF~0.14-0.16, kill-switch active", "stocks B-tier actionable n=9 anecdotal, 0W/3L this week, PF 0.000", "stocks C-tier research n=360, winrate 1.1%, PF 0.125 — poor but explicitly non-actionable"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "TUT/USDT", "trigger": "fill inside pullback zone 0.03270-0.03354 (waiting_for_entry, intraday); invalidation 1h close beyond 0.03166", "reason": "RS leader (+40.8% 24h vs BTC), disciplined pullback entry not yet triggered, RS-momentum playbook has best crypto-side edge this window" },
    "best_short_candidate":    { "symbol": "SYN/USDT", "trigger": "confirmed failed bounce / breakdown through 0.1094 zone; invalidation 1h close beyond 0.1147", "reason": "already an open swing short, -15.8% 24h, weak_rs_short source, needs the failed-bounce confirmation flagged in the prior review before adding conviction" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "confirmed RS leadership + rwa_narrative basket continuation without contradiction (basket fresh <24h)", "reason": "one of the few open names tied to an active narrative basket rather than pure momentum; catalyst mapping is weak overall so treat as context, not proof" },
    "avoid_candidate":         { "symbol": "ZBT/USDT", "reason": "2 open long swing signals on a token down -34.67% 24h with declining volume — correlation cluster fighting a clear downtrend; also flag REGN (active class-action/legal risk, correctly demoted this cycle)" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | risk_on, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.55 | oi_contradicts, funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, clean_retest, overextended | advisory_only |
| execution_lifecycle | ok | 0.85 | open_actionable, waiting_for_entry, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.70 | correlation_cluster, legal_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | ok | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (18:39 EEST)

- **New:** No new A/B crypto or stocks ideas fired this cycle. Crypto regime read upgraded from the 18:39 review's implicit "stale swing data" caveat — swing data is now fresh (16:00 UTC vs prior 15h44m-stale).
- **Removed:** BKNG (previously actionable, "manage toward TP1 218.43") no longer appears in this cycle's top candidates — likely closed/rolled off; not re-verified this cycle (not in the current active-signals crypto/stocks pull — flag for next cycle to confirm outcome).
- **Upgraded/downgraded:** None new this cycle for crypto. Stocks: same demotion pattern persists (liquidity_data_stale / catalyst_none / sector_confirmation gates knocking every A-scored name to C).
- **New catalysts:** No materially new catalyst since 18:39; same delisting_thin_liquidity (BONK/BTC), binance_ecosystem_teaser (BNB), rwa_narrative (ONDO/XLM), ai_narrative baskets persist.
- **Thesis changed:** UBER (flagged conditional in prior review, TODO-6 on catalyst-polarity scoring) no longer appears in current top candidates — status not re-verified this cycle.
- **Confirmed:** REGN legal/headline demotion (class action) — same as prior cycle, correctly caught again. ZBT correlation cluster — persists, now 2 open (was 3 in prior review, so one likely closed).
- **Invalidated:** None specific to report.

## 5. Catalyst Coverage

- Total catalyst events today: **3000** raw rows in `catalyst_events.jsonl` (report's deduped "unique events" count: 1887 as of the 18:12 catalyst cycle).
- Mapped (symbol present): **1323** (44.1%)
- Unmapped (no symbol): **1677** (55.9%)
- Narrative baskets active: **6** — delisting_thin_liquidity, binance_ecosystem_teaser, rwa_narrative, perps_dex_narrative, ai_narrative, momentum_breakout (intraday-only)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sample):
  1. "Pomerantz Law Firm Announces the Filing of a Class Action Against Microvast Holdings, Inc. and Certain Officers - MVST"
  2. "Pomerantz Law Firm Announces the Filing of a Class Action Against Insulet Corporation and Certain Officers - PODD"
  3. "INVESTOR ALERT: Pomerantz Law Firm Reminds Investors with Losses on their Investment in ZoomInfo Technologies Inc. — GTM"

## 6. Market Landscape

Crypto flipped intraday from range/chop (intraday report, 14:45 UTC snapshot) to a clean bullish trend/risk-on read by the scalp report (18:30 UTC snapshot): BTC and ETH both uptrend, altcoin breadth above EMA20 climbed from 50% → 71.4%, above EMA50 from 50% → 76.2%. Macro overlay stays hard risk-off (100/100) on Strait of Hormuz tanker attacks, EU/Russia sanctions escalation, and a soft July jobs report — a geopolitical headline could reverse the tape quickly overnight. Stocks: unambiguously risk-on (VIX 14.91, 100% index breadth above EMA20/50), but the stocks-intraday actionability gates (liquidity_data_stale, catalyst_none_and_not_exceptional_technical, sector_confirmation_weak) are demoting every A-scored name to C this cycle — the regime is bullish but the execution layer isn't finding anything clean enough to push live.

### Market Mood / Risk Routing
- Crypto mood: **risk-on** (trend) with a risk-off macro overlay — treat as **cautious risk-on**
- Stocks mood: **risk-on** (regime) but **not actionable** (0 A/B fired; all A-scored names gated to C)
- Dominant narrative: RS-leader/momentum continuation in low-cap alts (BICO/TST/ALLO/EPIC cluster); rwa_narrative (ONDO/XLM) and ai_narrative (NEAR/RENDER/TAO/FET) baskets secondary
- Preferred side now: **longs** on crypto, via confirmed pullback only — do not chase the momentum-breakout basket (BICO/EPIC/ALLO all tagged avoid_chase)
- Best long candidate: TUT/USDT — waiting for fill in 0.03270-0.03354
- Best short candidate: SYN/USDT — waiting for confirmed failed bounce below 0.1094
- Best catalyst-backed candidate: ONDO/USDT (rwa_narrative basket, fresh <24h)
- What to avoid: ZBT/USDT (correlation cluster fighting -34.67% 24h downtrend), REGN (active class-action risk), chasing ALLO/BICO/EPIC at current extended prices
- What would change the view: a BTC break of local support (turns "cautious risk-on" into outright risk-off given the macro overlay is already at max risk-off reading); a Strait of Hormuz de-escalation headline (removes the macro tail risk entirely)

## 7. Candidate Deep Dives

### TUT/USDT — long, WAITING for entry (best long-watch)
- Status: `waiting_for_entry`, intraday mode, tier B, entry zone 0.03269-0.03354, stop 0.03166, TP1 0.03579.
- Has price already reacted to the catalyst? No verified catalyst; this is pure RS/momentum (24h +41.5% per scalp scan, 7d strong).
- Chasing? No — order sits below current momentum, waiting for a pullback fill.
- Retest/pullback structure? Yes, that is the entry design.
- Overextended? Current price is above the entry band; the signal is explicitly not-yet-triggered for that reason.
- Would entry now be late? Yes at market; the whole point is to wait for the fill.
- Actionable now or after confirmation? After fill confirmation only.
- Aligned with market mood? Yes — RS-leader long in a risk-on crypto tape.
- Invalidation: 1h close beyond 0.03166.
- Chase risk: low (order is passive).
- Catalyst confirmation/contradiction: none found; treat as pure momentum, not catalyst-backed.

### SYN/USDT — short, open position (best short-watch / confirmation pending)
- Status: `triggered` (open), swing tier B, direction short, -15.8% 24h.
- Has price reacted? Yes, already breaking down; question is whether it's a clean breakdown or exhaustion.
- Chasing? The open position was entered on the initial breakdown; adding here without a failed-bounce confirmation would be chasing.
- Retest structure? Report's "failed bounce/retest zone" 0.1094-0.1118 is the confirmation level to watch.
- Overextended? Not by ATR, but short-squeeze risk was flagged (`thin_liquidity_short_squeeze_risk`) at the scalp-tier equivalent for this symbol.
- Aligned with mood? Only as a counter-trend idea inside an otherwise risk-on tape — treat as a tactical, not conviction, short.
- Invalidation: 1h close beyond 0.1147.
- Catalyst: none verified — technical short only.

### ONDO/USDT — long, part of rwa_narrative basket (catalyst-watch)
- Status: open per earlier basket association; not independently re-verified in this cycle's top-N tables (basket membership only).
- Catalyst confirmation: rwa_narrative basket flagged fresh <24h across two consecutive reports (intraday and scalp/swing) — moderately persistent, but catalyst mapping overall is only 44% this run, so treat with caution.
- Actionable now or after confirmation: after RS-leadership confirmation within the basket; not a standalone trigger.
- Legal/headline risk: none found.

### ZBT/USDT — avoid / manual review (correlation cluster)
- 2 open long swing signals on a symbol down -34.67% 24h (weakest-symbols list across scalp, intraday, and swing reports simultaneously).
- WebSearch corroboration: no fresh negative catalyst found (ZeroBase partnership/technical news is stale, from Feb/Apr 2026); the move reads as technical deleveraging, not headline-driven — but that does not make fighting the trend with 2 open longs safer.
- Recommendation: do not add size; flag existing 2 positions for manual review of stop discipline.

### REGN — avoid (confirmed legal risk, correctly gated)
- Tier raw A (score 94.2), demoted to C this cycle for active class-action/securities-fraud risk (Pomerantz Law Firm investor alert, PR Newswire, 2026-08-07).
- This is the production risk-warning layer working as intended — no action needed beyond confirming it stays gated.

## 8. Best Candidates Ranked

1. **TUT/USDT (long-watch)** — wait for fill 0.03270-0.03354, invalidation 0.03166.
2. **SYN/USDT (short-watch)** — wait for confirmed failed bounce below 0.1094, invalidation 0.1147.
3. **ONDO/USDT (catalyst-watch)** — wait for RS-leadership confirmation within rwa_narrative basket.
4. No clean new stocks idea this cycle — every A-scored name gated to C on liquidity/catalyst/sector-confirmation; re-check next cycle for gate clearance.

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and the scheduler continue uninterrupted regardless.
- **ZBT/USDT** — do not add to the existing 2-position long cluster against a -34.67% 24h trend.
- **REGN** — active class-action/legal risk; correctly gated to C, stays avoided until resolved.
- **Chasing ALLO/BICO/EPIC** at current extended prices — all three tagged `momentum_breakout`/`avoid_chase` this cycle; wait for the stated pullback zones instead.
- **New stocks entries generally** — 0 A/B actionable this cycle; every A-scored name demoted on liquidity/catalyst/sector gates.

## 10. Main Risks

- Macro/geopolitical risk score is pinned at 100/100 (Strait of Hormuz, Russia sanctions) even as crypto price trend is bullish — a headline reversal is the single biggest tail risk into the Asia session.
- ZBT/USDT correlation cluster (2 open longs against a clear downtrend) concentrates risk in the active book.
- ADA/USDT concentration: 3 open positions (swing+intraday) plus a fresh untracked watchlist alert today — same symbol appearing three ways increases correlated exposure without a corresponding size discount.
- Catalyst mapping at 55.9% unmapped this run reduces confidence in any catalyst-backed thesis, including the ONDO catalyst-watch pick above.
- ABNB's open B-tier position still carries the unresolved earnings-date verification gap from the 18:39 review (TODO-1) — unresolved for a third consecutive cycle.
- Crypto scalp mode remains structurally losing (PF ~0.14-0.16) — kill-switch is doing its job; no action needed but worth remembering when interpreting any scalp-tier "strong RS" name.

## 11. Action Plan — next 4 hours

- Do not add new size to ZBT/USDT; consider manual review of the existing 2 open longs given the persistent downtrend.
- Let TUT/USDT and SYN/USDT triggers play out passively — no market entries.
- Do not chase BICO/EPIC/ALLO at current extended prices; wait for confirmed pullback fills already defined in the swing report.
- No new stocks entries this cycle; re-check gate status (liquidity_data_stale, sector_confirmation) at the next scheduled slot (23:15 post-close final daily review).
- Re-verify ABNB's true last-earnings date against a reliable calendar source (TODO-1, now overdue for manual action).
- Re-check catalyst mapping % and untracked-alert count at 23:15 — if mapping stays >50% unmapped for multiple consecutive cycles, this becomes a resolver-quality TODO rather than a one-off.

## 12. Final Verdict per Mode

- **Crypto scalp:** no trade — mode disabled by kill-switch regardless; structurally losing bucket.
- **Crypto intraday:** no trade — no A/B fired; TUT/USDT is the one watch-worthy waiting order.
- **Crypto swing:** carry-forward the 20 open B-tier positions; no new entries recommended this cycle beyond the stated watch triggers; manage ZBT/ADA clusters with extra scrutiny.
- **Stocks intraday:** no trade — 0 A/B actionable; manage the one carried ABNB position pending the earnings-date verification; RIOT stays avoided (earnings today).
- **Stocks swing/invest:** retired/deprecated — not evaluated (see §3).

## 13. Sources

- [Bitcoin ETF Inflows Rise After Coldcard Hack: Bloomberg ETF Analyst](https://cointelegraph.com/news/bitcoin-etf-inflows-coldcard-hack-bloomberg-analyst) — Cointelegraph, 2026-08-06
- [Bitcoin ETFs Add Nearly $800 Million In The Wake Of Coldcard Exploit](https://bitcoinmagazine.com/news/bitcoin-etfs-800-million-coldcard) — Bitcoin Magazine
- [Bitcoin Faces Worst Month After Coldcard Exploit Drains $38M From 500 Wallets](https://www.techtimes.com/articles/322654/20260801/bitcoin-faces-worst-month-after-coldcard-exploit-drains-38m-500-wallets.htm) — Tech Times, 2026-08-01
- [ZEROBASE (ZBT) Price Prediction / news aggregation](https://coinmarketcap.com/cmc-ai/zerobase/latest-updates/) — CoinMarketCap, accessed 2026-08-07 (no fresh August-specific negative catalyst found)

## 14. Fix Requests / TODO

### TODO-1 (carry-forward, now 3rd consecutive cycle unresolved)
- **issue:** ABNB B-tier signal's "earnings: safe" gate has not been re-verified against a reliable earnings calendar since first flagged at 18:39 EEST; ABNB still carries an open B-tier position this cycle.
- **evidence:** `data/reports/stocks/intraday/2026-08-07_18-36_stocks_intraday_report.md` (ABNB present in active-signals stocks pull, tier B, triggered); original flag in `OPUS_ENRICHED_REVIEW_AUTO_2026-08-07_1839.md` TODO-1.
- **suggested manual fix:** verify ABNB's true last-earnings date against a reliable calendar source; confirm whether the internal earnings-calendar ingest is missing this name.
- **priority:** high
- **first observed:** 2026-08-07 18:39 EEST (recurrence confirmed 2026-08-07 21:39 EEST)

### TODO-3 (carry-forward, ongoing since 2026-07-17)
- **issue:** Untracked legacy alerts recurred again this cycle — `detect_untracked_legacy_alerts` reports 3 unmatched alerts today (ALLO/USDT ×2, ADA/USDT ×1), same root cause as the 2026-07-17 finding.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-08-07` → 3 untracked legacy crypto alert(s), all `NO (no proposed_signal)`.
- **suggested manual fix:** implement the fix already scoped in the prior finding — mint a new `proposed_signal` instead of reusing a stale/closed `signal_id` on watchlist re-fire.
- **priority:** high
- **first observed:** 2026-07-17 (recurrence confirmed 2026-08-07 21:39 EEST)

### TODO-5 (carry-forward)
- **issue:** `data/scheduled_runs/2026-08-07_default_schedule/` still contains zero `cycle_*_summary.md` files (only scheduler.log at 03:21); the scheduler is instead continuing to write today's cycles into the `2026-08-06_default_schedule/` folder.
- **evidence:** directory listing comparison, `2026-08-07_default_schedule/` (1 file, stale) vs `2026-08-06_default_schedule/` (scheduler.log mtime 21:30 today, i.e. actively receiving today's cycles).
- **suggested manual fix:** investigate the date-rollover logic in the scheduler script responsible for creating per-day `scheduled_runs` folders and writing `cycle_*_summary.md`.
- **priority:** medium
- **first observed:** 2026-08-07 18:39 EEST (recurrence confirmed 2026-08-07 21:39 EEST)
