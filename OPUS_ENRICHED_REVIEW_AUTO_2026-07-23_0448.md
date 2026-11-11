# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:30 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (04:30 EEST, 2026-07-23). **Advisory only — no auto-trade, no scoring/strategy changes.**

Crypto technicals are constructive (BTC + ETH both uptrend, 74% of tracked symbols above EMA20) but a **major geopolitical macro overlay** (Iran–US missile-strike escalation headlines, macro risk score 100/100) is a genuine risk-off counterweight — treat as **mixed**, not clean risk-on. No new A/B setups fired this cycle in scalp or intraday; the book holds 21 crypto B-tier signals (all long except one short), most already partially booked (tp1/tp2_hit). Stocks are closed (pre-Europe); all stock candidates are demoted to planning-only. Catalyst mapping is weak this run (78% unmapped) — use catalyst layer as context only. UNH's DOJ Medicare-billing investigation remains open (last confirmed 2026-07-16/17, no update since) and stays an avoid/manual-review name. Scanning, tracking, and monitors continue regardless of this review's caution stance.

## 2. Data Used

- Crypto reports: `2026-07-23_01-20_scalp_report.md`, `2026-07-23_01-28_intraday_report.md` (both fresh, <30min old)
- Swing report: `2026-07-22_01-16_swing_report.md` (**stale**, ~27h old — no fresher source, carried forward with caution flag)
- Stocks intraday: `2026-07-22_22-47_stocks_intraday_report.md` (fresh, ~6h old, generated pre-close)
- Stocks swing/invest: last available `2026-07-02_13-0x` reports (**~21 days stale** — see §14 TODO)
- Catalyst layer: `data/catalysts/2026-07-23/catalyst_events.jsonl` (500 events), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_01-38.md`
- LLM packets: `llm_analysis_packet.md` (crypto, fresh), `llm_stocks_packet.md` (stocks)
- CLI: `active-signals` (crypto ×21, stocks ×50), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts` (clean — no untracked alerts)
- Direct read-only SQL against `db/crypto_ai_desk.sqlite` (`news_items`, `watchlist_alerts` schema) for UNH DOJ-investigation freshness verification and signal expiry classification

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime: 2026-07-23 04:38 (fresh, <1min old at read time)
- Latest cycle summary: `cycle_02_00-55_summary.md` (~2.6h old) — well within the 3h defer threshold, review proceeds
- `derivatives_monitor`, `pending_monitor`, `mexc_canary_monitor` logs all updating within the last few minutes — monitors alive
- Crypto scalp/intraday reports fresh (<30min)
- Swing report stale (>14h threshold) — excluded from active long/short recommendations, used only as background context
- Stocks swing/invest reports ~21 days stale — **not used** for any candidate this run (see §14)
- Catalyst scan for today already present (`catalyst_cycle_01-38.md`, generated 04:38) — no need to re-run the CLI

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-23 04:48 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "data_missing": ["stocks swing/invest reports ~21d stale", "OI data unavailable for most crypto symbols (n/a via mexc fallback)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 04:38", "swing report mtime 2026-07-22 04:16 (~27h)", "stocks swing/invest last dated 2026-07-02"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["risk_on", "danger", "mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH both uptrend, 73.7% breadth above EMA20", "macro risk 100/100 from Iran-US missile-strike escalation headlines", "stocks regime = chop, neutral, VIX 16.64"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": ["accurate symbol resolution for funding-rate/listing notices"],
      "suggested_effect": "advisory_only",
      "facts_used": ["500 catalyst events, 110 mapped (22%) / 390 unmapped (78%)", "ai_narrative basket's sample headline is an Iran-strike geopolitical item, not AI-sector news — narrative clustering mismatch"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["data_unavailable", "squeeze_risk"],
      "data_missing": ["OI 24h data (n/a for all fallback_via_mexc symbols)", "long/short ratio"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ERA/USDT funding -0.00316 (bybit -0.0026, mexc -0.00316), crowding elevated", "DODO/USDT funding -0.000646, crowding moderate", "all other tracked symbols funding neutral/low crowding"] },
    { "agent": "technical_entry", "verdict": "watch", "confidence": 0.5,
      "reason_codes": ["stale_before_entry", "price_moved_away", "clean_retest"],
      "data_missing": ["structured entry/ATR levels for WLFI/USDT and DEXE/USDT (not written up as formal Trade Ideas this cycle)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["AKE/EPIC/DODO watchlist ideas all conditional pullback zones, none triggered", "WLFI/USDT -7.87% 24h with 2.53x volume expansion but no published entry structure this cycle"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.6,
      "reason_codes": ["open_actionable", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 5/21 active signals within tracking window (open_actionable), 16/21 past expires_at while still tp1/tp2_hit (entered_unresolved)", "stocks: ~16/50 within window (mostly invest-mode), ~34/50 past expires_at (entered_unresolved)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "correlation_cluster", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ Medicare-billing investigation confirmed 2026-07-16, no update since", "MSFT: active securities_fraud legal flag, tier demoted B→C", "GOOGL + TSLA + LMT: earnings today, do-not-chase warning", "ARB/ETH/ADA/BNB: correlated exploit_hack cluster (Arbitrum bridge, Wanchain Cardano-BNB bridge, AFX Trade) same 24h window", "macro: Iran-US military escalation headlines, risk 100/100"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp mode: PF 0.72, avgR -0.09, 2W/14L, totalR -3.10 (week, n=44) — reproducibly losing", "crypto swing mode: PF 2.97, avgR +0.56, totalR +23.61 (n=50) — best-performing bucket", "crypto short direction: PF 0.125, 0W/6L (n=8, anecdotal) — small sample but consistently bad", "weekend_mode signals underperform, winrate 32% (n=32) — CLI-flagged observation", "stocks: headline A/B sample=0 this week; C-tier watchlist PF 0.958, avgR -0.0094 — flat/slightly negative"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.55,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "AKE/USDT", "trigger": "1h close and hold inside/above 0.0017-0.0018 pullback zone on confirming volume; invalidate on 1h close below 0.0017", "reason": "highest-scored (67.5) crypto watchlist idea in bullish-trend regime, but known failure mode is no-catalyst intraday momentum in chop (14d: WR 23%/PF 0.70/-3R) — needs RS-leader or breakout confirmation before treating as live" },
    "best_short_candidate": { "symbol": "WLFI/USDT", "trigger": "wait for a failed bounce / breakdown continuation with volume confirmation — exact entry/ATR structure not published this cycle, re-check next report", "reason": "score 76.5, -7.87% 24h, RS -7.11% vs BTC, 2.53x volume expansion, tagged weak_vs_market + overextended; funding neutral/crowding low across bybit/mexc/okx so not obviously squeeze-prone" },
    "best_catalyst_candidate": { "symbol": "none", "trigger": "wait for a catalyst event with verification_status=primary_source AND same-symbol RS/technical confirmation — catalyst mapping is only 22% this cycle and the two live narrative baskets (perps_dex, ai_narrative) are either bearish (HYPE) or built on a mismatched headline", "reason": "no clean catalyst-backed setup survives verification this window" },
    "avoid_candidate": { "symbol": "UNH", "reason": "live DOJ criminal+civil Medicare-billing investigation (confirmed 2026-07-16, reiterated 2026-07-17, no update since) overrides technical score; manual review required" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.60 | scheduler_fresh, report_stale, derivatives_sparse | advisory_only |
| market_regime | caution | 0.55 | risk_on, danger, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.40 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, squeeze_risk | advisory_only |
| technical_entry | watch | 0.50 | stale_before_entry, price_moved_away, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.60 | open_actionable, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

(vs `OPUS_ENRICHED_REVIEW_AUTO_2026-07-22_2332.md`, 23:32 EEST cycle)

- **Confirmed:** RE/USDT — previous review's best-long-watch (waiting_for_entry) has since **triggered** (now an open B-tier intraday long, entry 0.4754-0.4857, invalidation 0.4628, expires 19:03 today). Thesis played out as flagged.
- **Faded:** RIF/USDT — previous review's best-short-watch (persistent -27% laggard, squeeze-risk-unresolved) **no longer appears** in either today's scalp or intraday weakest-symbols list. Treat the short thesis as stale/resolved; do not carry it forward.
- **Unchanged:** UNH avoid/manual-review stance — DOJ investigation still open, no fresh contradicting or confirming news since 2026-07-16/17. This is now flagged across 6+ consecutive cycles; treat as a standing position, not a new alert.
- **New this cycle:** Iran-US military escalation headlines (missile strikes, "Trump ratchets up war rhetoric") pushed macro risk to 100/100 — this is a fresh macro overlay, consistent in intensity with the prior review's framing (Strait of Hormuz conflict), but now carrying additional Amazon-data-center-strike and Fed-rate-hike-risk headlines not present before.
- **New:** A cluster of same-day exploit_hack reports (Arbitrum bridge $24M, AFX Trade $24.15M via Ethereum, Wanchain Cardano-BNB bridge $9M NIGHT) — correlated cross-chain bridge-exploit risk touching ARB, ETH, ADA, BNB simultaneously.
- **Improved:** The previously escalating untracked-alert defect (9 raw Telegram alerts with no backing proposed_signal as of the last review) shows **0** today per `detect_untracked_legacy_alerts` — but see §14 carried-forward note, this detector checks a different failure mode than the signal-reuse bug tracked in project memory, so do not treat this as confirmation that bug is fixed.

## 5. Catalyst Coverage

- Total catalyst events today: **500**
- Mapped (non-null symbol): **110 (22.0%)**
- Unmapped: **390 (78.0%)**
- Narrative baskets: **3** (perps_dex_narrative, ai_narrative, momentum_breakout)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped headlines (symbol clearly present in title but not resolved):
1. "First in Market: MEXC to List WOODUSDT Futures in Innovation Zone..." (#New_Listings)
2. "Adjustment to RIFUSDT Funding Rate Settlement Frequency..." (#Trading_Updates)
3. "Adjustment to BNCUSDT Funding Rate Settlement Frequency..." (#Trading_Updates)

These three look like a resolver regression, not routine noise — the ticker is spelled out literally in the headline (WOODUSDT, RIFUSDT, BNCUSDT) yet the symbol field is null. See §14 TODO-1.

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed** (technically risk-on — BTC + ETH uptrend, 73.7% breadth above EMA20 — but macro/geopolitical risk score 100/100 from Iran-US escalation headlines is a genuine risk-off counterweight)
- Stocks mood: **closed** (pre-Europe slot; underlying regime label is chop/neutral, VIX 16.64, mixed breadth — planning context only)
- Dominant narrative: momentum_breakout cluster (DODO/ZAMA/AKE, no confirmed catalyst) and a bearish perps-DEX narrative (HYPE down after Multicoin unstake + ETF outflows)
- Preferred side now: **wait-for-trigger, selective longs on RS-leader confirmation** (per regime), shorts only on confirmed breakdown with volume
- Best long candidate: AKE/USDT — conditional pullback 0.0017-0.0018, needs breakout/RS confirmation (see §8)
- Best short candidate: WLFI/USDT — needs a defined entry structure next cycle (see §8)
- Best catalyst-backed candidate: none clean this window (catalyst mapping only 22%)
- What to avoid: UNH (open DOJ investigation), fresh entries into ARB/ETH/ADA/BNB while the cross-chain bridge-exploit cluster is unresolved, chasing GOOGL/TSLA/LMT into today's earnings prints
- What would change the view: a de-escalation headline on the Iran-US situation would remove the macro risk-off overlay; a primary-source catalyst confirming one of the current watchlist longs would upgrade it toward B-tier

## 7. Candidate Deep Dives

### 1. AKE/USDT (long, watchlist, score 67.5)
- Has price already reacted to a catalyst? No — no fresh verified catalyst; this is the momentum_breakout basket (pure price/volume cluster, no news).
- Chasing? Not yet — still inside the conditional pullback zone (current price 0.0018, zone 0.0017-0.0018).
- Retest/pullback structure? Yes, that's the entire thesis — waiting for acceptance inside the zone.
- Overextended (>2 ATR from EMA20)? Not flagged in report; ATR ≈ 0.0001, current price sits at zone top.
- Would entry now be late? No, but score is below the active-trade threshold — this is watchlist, not live.
- Actionable level: 1h close and hold inside 0.0017-0.0018 with volume confirmation.
- Market-mood alignment: consistent with "selective longs, prefer pullbacks on RS" recommended style.
- Long/short/wait: wait-for-trigger long.
- Invalidation: 1h close below 0.0017.
- Chase risk: low right now (still in zone), would become high if price runs before confirmation arrives.
- Catalyst confirmation/contradiction: none either way — pure technical/momentum play, explicitly the playbook's known weak spot (WR 23%/PF 0.70/-3R over 14d for no-catalyst intraday momentum in chop).
- TradingView/manual chart check unavailable — reading only from the report's local OHLCV/ATR/EMA fields, chart PNG not visually inspected.

### 2. WLFI/USDT (short, informal watch, score 76.5)
- Has price already reacted? Yes — already -7.87% 24h, RS -7.11% vs BTC.
- Chasing? Potentially — the move has already happened; a fresh short here without a retest is late.
- Retest/pullback structure? Not published this cycle (no formal Trade Idea write-up despite scoring 76.5).
- Overextended? Tagged `overextended` + `volume_expansion` in the report's own symbol tags.
- Would entry now be late? Likely yes without a bounce-and-fail confirmation first.
- Actionable level: undefined this cycle — flagged as a data gap rather than fabricating a number.
- Market-mood alignment: consistent with "shorts only on confirmed breakdown."
- Chase risk: high if entered now, low if waiting for a failed bounce.
- Catalyst confirmation/contradiction: none found — no catalyst_events entry for WLFI today, this is a clean technical short candidate, not catalyst-driven.
- Derivatives: funding neutral, crowding low across bybit/mexc/okx — no squeeze risk currently visible.

### 3. RE/USDT (long, already OPEN — status update, not a new idea)
- Confirmed trigger from the prior cycle's long-watch call; now an active B-tier intraday long (entry 0.4754-0.4857, invalidation 0.4628, score 65.1, expires 19:03 today).
- No action needed — tracking only. Do not treat as a fresh entry opportunity; it's already filled.

### 4. UNH (stocks, avoid/manual review — carried forward)
- Legal/headline risk verified via direct news_items query: DOJ investigation into Medicare billing confirmed 2026-07-16 ("UnitedHealth Group under DOJ investigation over Medicare billing practices" — Medical Economics), reiterated 2026-07-17 ("UnitedHealth stock sinks 4.7% after company confirms DOJ investigation" — Yahoo Finance). No update in the last 48h (most recent UNH item is a bullish BofA price-target note, unrelated to the legal matter).
- Verdict stays AVOID / MANUAL REVIEW REQUIRED regardless of technical score — this is a standing, unresolved federal investigation, not stale/contradicted news.

### 5. ARB/USDT and correlated exploit-hack cluster (risk note, not a trade idea)
- Multiple independent sources (peckshield, wublockchain, CryptoBriefing) reported a ~$24M USDC bridge exploit on Arbitrum via oracle manipulation on Ostium DEX in the last 24h — cross-referenced across 4+ distinct news_items rows despite each individually tagged single_source.
- Same window also saw an AFX Trade exploit ($24.15M, bridged to Ethereum) and a Wanchain Cardano-BNB bridge exploit ($9M NIGHT drained) — a correlated cross-chain bridge-exploit cluster touching ARB, ETH, ADA, BNB.
- Not a specific trade call, but a reason to avoid fresh directional bets on these four names until the dust settles — flagged in production risk warnings as `block_requires_operator_review` for all four.

## 8. Best Candidates Ranked

Even with no clean A/B trade this window, per the anti-over-conservatism rule the routed picks are:

1. **Long-watch: AKE/USDT** — trigger: 1h close/hold inside 0.0017-0.0018 zone with confirming volume; invalidate below 0.0017.
2. **Short-watch: WLFI/USDT** — trigger: failed bounce / breakdown continuation with volume confirmation; exact level not defined this cycle, re-check the next cycle's report.
3. **Catalyst-watch: none clean** — trigger: a catalyst event reaching verification_status=primary_source with same-symbol RS/technical confirmation (current mapping rate is only 22%, both live narrative baskets are either bearish or headline-mismatched).
4. **Avoid: UNH** — open DOJ investigation, technical score irrelevant while unresolved.

## 9. Avoid / No Trade

This is a decision-window call only — scanning, data collection, tracking, and the scheduler continue unchanged.

- **UNH** — open federal DOJ investigation (Medicare billing), manual review required, avoid new exposure regardless of technical setup.
- **ARB, ETH, ADA, BNB** — correlated cross-chain bridge-exploit cluster in the last 24h; avoid fresh directional bets until resolved.
- **GOOGL, TSLA, LMT** — earnings today (2026-07-23); do not chase into the print.
- **MSFT** — active securities_fraud legal flag, demoted B→C; manual review required if it resurfaces as A/B.
- **Crypto scalp mode generally** — reproducibly losing this week (PF 0.72, 2W/14L, avgR -0.09); no scalp-mode idea should be treated as high-conviction without an unusually strong confirmation stack.

## 10. Main Risks

- **Macro/geopolitical:** Iran-US military escalation (missile strikes reported near Andimeshk, Iran claims a strike on an Amazon data center, Fed-rate-hike risk cited amid the crisis) — macro risk score 100/100. This can override crypto's bullish technical picture on short notice.
- **Cross-chain exploit cluster:** four correlated bridge/exploit headlines (ARB, ETH, ADA, BNB) in one 24h window — elevated tail risk for anything touching those chains.
- **Execution-lifecycle backlog:** 16/21 crypto and ~34/50 stocks "active" signals are past their tracked expires_at while still showing tp1/tp2_hit/triggered — worth a maintenance check on the resolution-job cadence (see §14 TODO-4), not confirmed as a bug this run.
- **Catalyst layer degraded:** 78% of today's catalyst events are unmapped, and the narrative-basket clustering mismatched an Iran-conflict headline into the "ai_narrative" bucket — treat catalyst-driven calls with extra skepticism this cycle.
- **Data staleness:** crypto swing report is ~27h old (no fresher source); stocks swing/invest reports are ~21 days old — swing/invest-mode candidates should not be treated as current.

## 11. Action Plan — Next 4 Hours

- Watch AKE/USDT for a confirmed pullback-zone hold before treating as actionable; do not force it below threshold.
- Watch WLFI/USDT for the next report cycle to see if a formal short structure gets published; don't freehand an entry today.
- No action needed on RE/USDT — already open and tracking to plan.
- Keep UNH and the ARB/ETH/ADA/BNB cluster on the avoid list through the Europe-open cycle (11:30 EEST) unless news changes.
- Monitor the Iran-US headline flow — a material de-escalation or further escalation both change the macro overlay materially before the next cycle.
- No changes to scoring, thresholds, or scanning — system continues running as-is.

## 12. Final Verdict per Mode

- **Scalp:** No A/B setups. Mode itself is a known loser this week (PF 0.72) — treat any future scalp idea with extra scrutiny.
- **Intraday:** No A/B setups this cycle; book carries several open/partially-booked B-tier longs (BANK, ONDO, ZAMA, ADA, VIRTUAL, ALLO, KITE, PENGU, PUMP, KAITO) plus RE/USDT freshly triggered. Watchlist-only for new entries (AKE/EPIC/DODO/ERA/TLM/OPN).
- **Swing:** Best-performing mode this week (PF 2.97) but the underlying report is ~27h stale — treat existing swing positions (OPN, ALLO) as tracking-only, don't originate new swing ideas off stale data.
- **Stocks intraday:** Market closed — all candidates planning-only (best longs: XOM, NVDA, AMD, AVGO; best shorts: META, XLV). GOOGL/TSLA/LMT earnings-today caveat applies at the open.
- **Stocks swing/invest:** Data ~21 days stale — do not use for any current decision (see §14 TODO-2).

## 13. Sources

- [UnitedHealth Group under DOJ investigation over Medicare billing practices](https://www.medicaleconomics.com/) — Medical Economics, 2026-07-16
- [UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices](https://finance.yahoo.com/) — Yahoo Finance, 2026-07-14
- [UnitedHealth Group (UNH) Faces Wider DOJ Antitrust Probe As Claritev Review Expands](https://finance.yahoo.com/) — Yahoo Finance, 2026-07-16
- Internal: `data/catalysts/2026-07-23/catalyst_cycle_01-38.md` (Arbitrum bridge exploit, AFX Trade exploit, Wanchain Cardano-BNB bridge exploit — cross-referenced across peckshield/wublockchain/CryptoBriefing/AMBCrypto Telegram + RSS sources)
- Internal: `data/reports/scalp/2026-07-23_01-20_scalp_report.md`, `data/reports/intraday/2026-07-23_01-28_intraday_report.md`, `data/reports/stocks/intraday/2026-07-22_22-47_stocks_intraday_report.md`
- Internal: CLI `active-signals`, `signal-stats`, `detect_untracked_legacy_alerts` (2026-07-23 04:4x runs)

External web research (WebSearch/WebFetch) was not invoked this run — internal `news_items`/report data was sufficiently fresh and consistent for every candidate touched (per §G: only escalate to external search when internal records are missing/stale/contradictory). No candidate here depended critically on external verification beyond what direct SQL/report reads already confirmed.

## 14. Fix Requests / TODO

### TODO-1: Catalyst symbol resolver missing tickers spelled out literally in the headline
- **issue:** Funding-rate-adjustment and new-listing notices (e.g. "Adjustment to RIFUSDT Funding Rate Settlement Frequency", "MEXC to List WOODUSDT Futures") are landing in `catalyst_events.jsonl` with a null symbol despite the ticker being present verbatim in the title.
- **evidence:** `data/catalysts/2026-07-23/catalyst_events.jsonl` — 390/500 (78%) unmapped this cycle; top 3 unmapped headlines all contain an explicit `*USDT` ticker.
- **suggested manual fix:** Extend the symbol resolver's regex/lookup to catch `#Trading_Updates` / `#New_Listings`-style Binance/MEXC announcement formats where the ticker appears as a single concatenated token (e.g. `RIFUSDT`) rather than the usual `RIF/USDT` form.
- **priority:** high
- **first observed:** 2026-07-23 04:48 EEST (pattern likely pre-existing; this is the first run this pattern was surfaced with specific evidence)

### TODO-2: Stocks swing/invest reports ~21 days stale
- **issue:** `data/reports/stocks/swing/` and `data/reports/stocks/invest/` have no report newer than 2026-07-02 — roughly 3 weeks stale, while crypto and stocks-intraday reports are generating normally on schedule.
- **evidence:** `ls -lat data/reports/stocks/swing/` and `data/reports/stocks/invest/` — latest files both dated `2026-07-02_13-0x`.
- **suggested manual fix:** Check whether the stocks swing/invest report-generation step is still wired into the scheduler cycle (it may have been intentionally paused per the stocks position-framework rework — cross-check against project memory `project_crypto_ai_desk_stocks_position_framework`) or if it's silently failing.
- **priority:** medium
- **first observed:** 2026-07-23 04:48 EEST

### TODO-3: Narrative-basket clustering mismatch
- **issue:** The `ai_narrative` basket (primary: NEAR/RENDER/TAO/FET) is populated with a sample headline about a US missile strike near Ahwaz, Iran — unrelated to AI-sector news. The clustering step appears to be grouping by some shared token/hashtag rather than actual topical relevance.
- **evidence:** `data/catalysts/2026-07-23/catalyst_cycle_01-38.md` line 29-32.
- **suggested manual fix:** Audit the narrative-basket keyword/embedding matching for the `ai_narrative` bucket; this basket should not be cited as catalyst support for AI-sector longs until fixed.
- **priority:** medium
- **first observed:** 2026-07-23 04:48 EEST

### TODO-4: Large volume of past-expiry signals still shown as active
- **issue:** 16/21 crypto and ~34/50 stocks entries returned by `active-signals` have an `expires_at` already in the past while still showing `tp1_hit`/`tp2_hit`/`triggered` status rather than a resolved outcome.
- **evidence:** Manual comparison of `active-signals --asset-class crypto/stocks` output `expires_at` column against current time (2026-07-23 ~01:39 UTC) during this review.
- **suggested manual fix:** Confirm whether this is expected (a separate nightly/weekly resolution job that hasn't run yet vs. real-time `active-signals`) or a genuine backlog needing a resolution-pass. Not treated as a confirmed bug this run — flagged for a human to check the resolution-job cadence.
- **priority:** low
- **first observed:** 2026-07-23 04:48 EEST

### Carried forward (not re-verified this run)
- Watchlist-alert signal-reuse bug (untracked-alert re-fire reusing a stale `signal_id`, confirmed previously on ALLO/USDT + BANK/USDT) remains open per project memory (`project_crypto_ai_desk_watchlist_alert_signal_reuse_bug`, raised high priority 2026-07-17). Today's `detect_untracked_legacy_alerts` run came back clean, but that detector checks a different failure mode (missing backing signal, not signal reuse) — this TODO was not independently re-verified this cycle and should stay on the human's list until closed.
