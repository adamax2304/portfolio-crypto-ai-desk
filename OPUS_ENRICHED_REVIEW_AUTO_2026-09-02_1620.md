# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (target 08:50 ET / hand-off deadline 09:12 ET). **Advisory only — no auto-trade, no scoring/threshold changes.**
Pre-US-open time-critical hand-off completed: `stocks-preus-candidates` (32 eligible / 66 excluded) reviewed and ingested via `stocks-preus-review-ingest`; `stocks-preus-review-health` reports 33/33 reviewed, 0 missing, status `PENDING_DEADLINE` (healthy — deterministic 09:15 ET promotion window had not yet fired at check time).
Both crypto timeframes (intraday + swing) and the stocks regime read agree: **risk-off, short bias, no A/B-tier actionable setups** — only C-tier watchlist ideas. Macro overlay is the dominant driver: Israel/US-Iran escalation has pushed the crypto macro-risk score to 100/100.
Highest-priority item this cycle is **not a new candidate but a data-integrity flag**: PROM/USDT carries two open long positions (from 2026-08-30) while today's own regime read tags it bias=short with 24h -15.15% — the same systemic bias-tag contradiction logged previously (see [[project_crypto_ai_desk_bias_tag_contradiction]] equivalent, §14).
Stocks: US cash session closed at review time; all 32 pre-US candidates are capped to C-tier (`market_closed_intraday_planning_only`) pending RTH confirmation. One fresh legal/IP headline (DIS — InterDigital patent injunction, ~1h old) triggered a short-TTL BLOCK veto in the pre-US overlay.

## 2. Data Used

- `data/reports/intraday/2026-09-02_11-41_intraday_report.md` (fresh, ~1h20m old)
- `data/reports/swing/2026-09-02_03-15_swing_report.md` (carry-forward, ~9h45m old)
- `data/reports/stocks/intraday/2026-09-02_12-33_stocks_intraday_report.md` (fresh, ~30min old)
- `data/reports/stocks/swing` and `stocks/invest` — both dated 2026-07-02, >2 months stale; per project history these modes are deprecated/replaced by the shadow-only stocks position framework — excluded from this review, not treated as live coverage gaps.
- `data/reports/scalp/2026-08-30_13-18_scalp_report.md` — 3 days stale, excluded.
- `data/catalysts/2026-09-02/catalyst_events.jsonl` (2500 events today), `narrative_baskets.jsonl` (5 active baskets)
- `data/processed/llm_analysis_packet.md` (fresh, 14:43 EEST), `data/processed/llm_stocks_packet.md` (fresh, 15:36 EEST)
- `python -m src.cli active-signals --asset-class crypto` (50 rows) / `--asset-class stocks` (50 rows)
- `python -m src.cli signal-stats --asset-class crypto` / `--asset-class stocks`
- `python -m scripts.detect_untracked_legacy_alerts --since 2026-09-02` — clean
- `python -m src.cli stocks-preus-candidates` / `stocks-preus-review-ingest` / `stocks-preus-review-health` (this slot's hand-off)
- `news_items` / `proposed_signals` SQLite queries (read-only) for candidate freshness and lifecycle counts
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-02_1130.md` (11:30 EEST Europe/pre-US slot)
- **External web research unavailable this cycle** — WebSearch/WebFetch were not exercised in this pass; all catalyst/legal reads below are internal-DB-first (`news_items`, `catalyst_events.jsonl`). Any verdict resting critically on external confirmation is marked manual-review rather than asserted.

## 3. Scheduler / Data Freshness

- Pre-US schedule check: target 08:50 ET, actual fire ~08:54 ET (Δ+4min, within tolerance; UTC 12:54 → ET 08:54, steady-state 7h EEST offset holds, outside both 2026 DST-mismatch windows).
- Scheduler folder: `data/scheduled_runs/2026-09-01_default_schedule/` (most recent by mtime despite the date-stamped name — session spans the day boundary).
- `scheduler.log` mtime: 2026-09-02 15:48:54 EEST (~17min old at review start) — **fresh**.
- Latest `cycle_06_14-26_summary.md` mtime: 2026-09-02 15:48:47 EEST — **fresh**. No deferral triggered (both well under the 3h rule).
- Crypto intraday report: ~1h20m old (fresh, <4h). Crypto swing report: ~9h45m old (**carry-forward**, 4-12h bucket, used with flag). Stocks intraday report: ~30min old (fresh, especially valuable this close to the open).
- Stocks swing/invest reports: >2 months stale — excluded (deprecated legacy mode, per prior project history, not a fresh regression).
- Scalp report: 3 days stale — excluded from this cycle's candidate funnel.
- Pre-US review health: `eligible_count=33, reviewed_count=33, missing_count=0, status=PENDING_DEADLINE, reason=structured_preus_review_not_yet_due` — not literally `READY`/`NO_ELIGIBLE` per the spec's two named states, but functionally healthy (full coverage, zero gaps); the deterministic 09:15 ET window had not yet closed at check time (~09:03 ET). Flagged, not treated as a promotion.
- Untracked legacy crypto alerts: **0** — clean.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-09-02 16:05 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh"], "data_missing": ["stocks_swing_stale", "stocks_invest_stale", "scalp_stale"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 15:48 EEST", "cycle_06_14-26_summary.md mtime 15:48 EEST", "intraday report 1h20m old", "stocks intraday report 30min old"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH trend transition_down both timeframes", "altcoin breadth 29.17% above EMA20", "SPY/QQQ range with negative 20d, IWM downtrend", "macro risk 100/100 from Iran/Israel escalation headlines"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_contradicted"], "data_missing": ["external_verification_not_run"],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 2500 total, 915 mapped, 1585 unmapped (63.4% unmapped)", "HUT/VRT/DIS/GOOGL/HOOD short signals carry catalysts that read bullish for the underlying, contradicting the short bias", "ENA/USDT canonical_news_event catalyst (Ethena Pay launch) still the cleanest catalyst-backed crypto idea"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["data_unavailable", "oi_supports"], "data_missing": ["OI 24h n/a for most fallback_via_mexc symbols", "VIX not pulled this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["FIL price up + OI up (fresh positioning)", "TAO/PENGU/NEAR/XRP price down + OI down (deleveraging, not a squeeze setup)", "funding near-neutral across watchlist names, no extreme readings"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["clean_retest", "price_moved_away", "chase_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["all crypto C-tier ideas explicitly require a failed-bounce/retest, not a chase", "PROM/USDT current price 4.621 vs original long entry zone 6.58-6.84 (price moved far away from the open long)", "stocks: all 32 pre-US candidates are planning-levels-only pending RTH confirmation"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entered_unresolved", "waiting_for_entry", "needs_review"], "data_missing": ["stocks 'expired' bucket not split entered-vs-no-entry this cycle (no entry-fill timestamp column)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto last 24h: 4 stopped, 4 triggered(entered-unresolved), 1 entry_moved_away(no-entry), 1 tp2_hit(closed win), 1 tp3_hit(closed win), 1 waiting_for_entry", "stocks last 24h: 101 missed_no_entry, 38 stale_before_entry, 13 expired(split not resolved), 9 tp1_hit, 6 tp2_hit, 3 stopped, 2 tp3_hit, 1 triggered"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "manual_review", "correlation_cluster"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["DIS fresh InterDigital patent-injunction headline (~1h old, single Telegram source) -> BLOCK veto in pre-US overlay", "BA carries a geopolitical_risk warning tied to the active Iran conflict", "PROM/USDT open longs vs bias=short tag is a repeat of a known unresolved systemic issue"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto signal-stats: reliable tier B triggered winrate 12% (n=178); weekend signals underperform 12% winrate (n=35, stronger confidence)", "stocks signal-stats: reliable tier C triggered winrate 6% / PF 0.36 (n=612); stronger tier B triggered winrate 3% (n=85)", "crypto no-catalyst intraday momentum playbook (used by every C-tier idea this cycle): known 14d cut WR 23% / PF 0.70 / -3R"] },
    { "agent": "head_trader", "verdict": "advisory_only-synthesis-see-below", "confidence": 0.6,
      "reason_codes": [], "data_missing": [], "suggested_effect": "advisory_only", "facts_used": [] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "shorts",
    "best_long_candidate":     { "symbol": "none clean", "trigger": "no crypto long clears the risk-off short-bias regime filter this cycle; watch AR/USDT-style RS-leader longs only if breadth reclaims >40% above EMA20", "reason": "regime explicitly recommends 'short bias or no trade; avoid weak altcoin longs' on both timeframes" },
    "best_short_candidate":    { "symbol": "0G/USDT", "trigger": "1h close back below 0.1832-0.1868 failed-bounce/retest zone after a confirmed rejection; invalidation 0.1901", "reason": "weakest-symbols list both timeframes, 24h -14.53%, RS vs BTC -12.64%, aligned with risk-off regime; not yet confirmed, do not chase the current print" },
    "best_catalyst_candidate": { "symbol": "ENA/USDT", "trigger": "pullback fill inside 0.1520-0.1537 with 1h close confirmation; invalidation 0.1557", "reason": "only crypto symbol this cycle with a canonical_news_event catalyst (Ethena Pay app launch, importance 1.75); carried over from the 11:30 review, still the cleanest catalyst-backed idea" },
    "avoid_candidate":         { "symbol": "PROM/USDT / DIS", "reason": "PROM/USDT: two open crypto longs directly contradicted by today's own bias=short tag and -15.15% 24h move -- manual review, not a new trade either direction. DIS: fresh single-source legal/patent-injunction headline triggered a pre-US BLOCK veto -- treat as avoid until RTH-confirmed and independently verified." },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.75 | risk_off, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.45 | data_unavailable, oi_supports | advisory_only |
| technical_entry | caution | 0.55 | clean_retest, price_moved_away, chase_risk | advisory_only |
| execution_lifecycle | caution | 0.60 | entered_unresolved, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, manual_review, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.60 | playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review (11:30 EEST)

- **Carried over:** ENA/USDT remains the best catalyst-backed idea (same Ethena Pay catalyst, still below active-trade threshold). Regime read unchanged: risk-off, short bias, no A/B setups. PROM/USDT manual-review flag (bias-tag contradiction) **persists unresolved**.
- **New / different:** Best short-watch idea is still 0G/USDT (carried, price has drifted slightly further down since 11:30: was 0.1919, now 0.1829). Best long-watch dropped — AR/USDT (11:30's pick) no longer appears in the top intraday/swing tables this cycle; today's watchlist top slots are TRUMP/USDT and TAO/USDT (both short-bias failed-bounce setups, not longs) — **no clean long-watch candidate survives this cycle** (see §6/§8).
- **New this slot only:** the structured pre-US stocks overlay (32 candidates reviewed: 0 SUPPORT / 4 NEUTRAL / 2 CAUTION / 1 BLOCK / 25 INSUFFICIENT_DATA — see §5). This overlay did not exist in the 11:30 general review.
- Macro risk unchanged at 100/100 (same Iran/Israel escalation driving both cycles).
- Thesis change: none contradicted; PROM/USDT thesis (manual review) confirmed again.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **2500**. Mapped (non-null symbol): **915**. Unmapped: **1585** (**63.4%**).
- `narrative_baskets` count: **5** (delisting_thin_liquidity/AVAX, perps_dex_narrative/HYPE, rwa_narrative/ONDO+XLM, binance_ecosystem_teaser/BNB, momentum_breakout/FF+UNI+AUCTION).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (63.4% > 50% threshold)
- Top 3 unmapped headlines (symbol-agnostic macro/FX noise, correctly left unmapped):
  1. "TAKATA SAYS THE BOJ MUST REMAIN ALERT TO THE RISK OF STRONGER-THAN-EXPECTED INFL..."
  2. "BOJ'S TAKATA SAYS THE WAY THE CENTRAL BANK MANAGES ITS EXIT FROM MONETARY EASING..."
  3. "TAKATA SAYS THE BOJ SHOULD BRING ITS POLICY RATE NEARER TO THE NEUTRAL LEVEL IN..."

### Pre-US Stocks Review Overlay
- candidates reviewed: 32 (SUPPORT 0 / NEUTRAL 4 / CAUTION 2 / BLOCK 1 / INSUFFICIENT_DATA 25)
- session-cap-only C's now eligible for pre-open Paper lane: 0 promoted to SUPPORT this cycle — all held to NEUTRAL/CAUTION/BLOCK/INSUFFICIENT_DATA given no genuine RS-vs-sector or fresh-market-context confirmation was pulled in the time-critical window; several verdicts were preserved from an earlier same-day baseline review by the ingest command's `IGNORED_INSUFFICIENT_PRESERVED_BASELINE` guard rather than overwritten (JPM, RIOT, COP, VRTX, XOM, AMGN, HOOD, ARM, MSTR, PLTR, XLK, MS, BA, GS, SHOP, plus 2 duplicate signal_ids) — actual enforced values, not my requested ones, are what's reported here.
- excluded by hard gate: 66 (LEGAL_RISK: UNH, REGN, NVDA x2, SMCI, BLK, ORCL, INTU; EARNINGS_BLACKOUT: ISRG x2, LLY, MRVL, AMZN, PANW, COST, AMD, COIN, TSM, V, IBM, ASML, DELL, UBER, NET, CMCSA; NO_ENTITY_RESOLVED_CATALYST: remaining ~44 — full list in `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`)
- CAUTION detail: HUT (short; catalyst is Anthropic's $35B compute deal referencing Hut 8 — reads bullish, contradicts short bias), GOOGL (short; Gemini 3.8 unveiling + Berkshire's Abel calling Alphabet a "significant AI player" — both bullish, contradict short bias)
- BLOCK detail: DIS (short; fresh ~1h-old single-source Telegram headline — InterDigital patent injunction — legal/IP risk the static hard-gate list could not have seen; short-TTL veto, not a permanent block)
- Not caught by this pass but worth a follow-up note (not re-ingested, out of scope for a second pass this cycle): HOOD (short candidate) also carries a same-morning Morgan Stanley upgrade headline in `news_items` that was not folded into this cycle's verdict set — flagged in §14.

## 6. Market Landscape

**Crypto (intraday + swing, both agree):** BTC trend `transition_down`, ETH trend `transition_down`. Altcoin breadth above EMA20 29.17% (intraday) / 33.3% (swing) — both well under the ~50% risk-on threshold. Volatility normal (ATR percentile ~39). Regime explanation is identical on both timeframes: "short bias or no trade; avoid weak altcoin longs." No A-tier, no B-tier active setups on either report — only C-tier/watchlist ideas, all structured as short-side failed-bounce/retest theses (TRUMP, TAO, PROM, 0G, PENGU, NEAR, XRP, ENA, FF on intraday; TRUMP, PUMP, 0G and others on swing).

**Stocks:** Regime `risk_off`, bias `short`. SPY range (5d -0.54%, 20d -1.24%), QQQ range (5d -0.43%, 20d -2.24%), IWM downtrend (5d -2.89%, 20d -3.69%). Strongest sectors: energy (XLE, RS+11.92%), healthcare (XLV, RS+7.14%). Weakest: industrials (XLI, RS-6.10%), semiconductors (SMH, RS-4.06%). No A/B-tier actionable setups — market is closed, all candidates capped to planning-only C-tier pending the 09:30 ET open.

**Macro overlay (dominant driver both asset classes):** Macro/geopolitics risk score **100/100** — Israel/US vs Iran escalation (missile strikes near the Strait of Hormuz, a wedding struck in Kuhestak per Telegram sourcing), reported as the explicit BTC bias risk-off headwind in the intraday report. This is the same driver behind both the crypto short bias and part of the stocks risk-off tone (BA specifically carries a geopolitical_risk tag tied to this).

### Market Mood / Risk Routing
- Crypto mood: **risk-off** (both timeframes agree; macro risk 100/100 reinforcing)
- Stocks mood: **risk-off / pre-market — closed at review time**, planning-only until RTH confirmation
- Dominant narrative: geopolitical escalation (Iran/Israel) overriding sector-specific narratives; secondary: AI-datacenter-power narrative (VRT/Vertiv UIG acquisition) and stablecoin-infrastructure narrative (BAC/Wall Street stablecoin custody race)
- Preferred side now: **shorts** (crypto: failed-bounce retests only, not chases; stocks: wait for RTH confirmation, do not chase pre-market)
- Best long candidate: **none clean** — regime explicitly discourages weak altcoin longs; no RS-leader long survived either crypto report's top-10 this cycle
- Best short candidate: **0G/USDT** (crypto, watch-only, needs confirmed failed bounce below 0.1832-0.1868)
- Best catalyst-backed candidate: **ENA/USDT** (crypto, Ethena Pay launch catalyst, needs pullback-fill confirmation)
- What to avoid: chasing any of the C-tier short ideas at the current print instead of waiting for a confirmed retest; new PROM/USDT exposure in either direction pending manual review of the bias-tag contradiction; DIS pre-open (fresh unverified legal headline); HUT/GOOGL shorts as-is (catalyst contradicts direction)
- What would change the view: a confirmed Israel-Iran de-escalation headline or Brent/oil giving back its recent gains would ease macro risk-off pressure; altcoin breadth reclaiming >40-50% on EMA20 would flip the crypto read toward neutral; a clean RTH open with SPY reclaiming its 20d range highs would flip the stocks read

## 7. Candidate Deep Dives

### 1. PROM/USDT (crypto, manual review — bias-tag contradiction)
Two open long positions: id 59160 (swing, triggered 2026-08-30 04:34 UTC, entry zone 6.58-6.84) and a related scalp position (expired). Current price 4.621 — roughly 30%+ below the original entry zone, 24h -15.15%, RS vs BTC -13.25%. Today's own money-flow tables list PROM/USDT in *both* "Strongest Symbols" (score 96.2, largest move) *and* "Weakest Symbols" (bias short) simultaneously — the same systemic bias-tag contradiction flagged in the 11:30 review and in prior project history. Has price already reacted to a catalyst? No fresh verified catalyst found internally. Is this chase-risk? N/A — this is an existing open position, not a new entry. What would invalidate/resolve: a human-driven session correcting the bias tag or manually reviewing whether the open longs should be closed given the adverse 24h move. **Verdict: MANUAL REVIEW REQUIRED, not a new trade either direction.**

### 2. 0G/USDT (crypto, short-watch)
Price 0.1829 (down from 0.1919 at 11:30 review), 24h -14.53%, RS vs BTC -12.64%, volume 1.56x. Weakest-symbols list both timeframes. Has price reacted to a catalyst? No fresh catalyst detected (score breakdown catalyst_news=5.7/very low). Is the setup chasing? Yes if entered now — price is below the stated 0.1832-0.1868 zone already at print; needs a confirmed 1h close back below the zone after a failed bounce, not a straight short at market. Overextended? Not yet flagged as such in the report. Aligned with mood: yes (risk-off, short-preferred). Actionable now or after confirmation: **after confirmation only.** Invalidation: 1h close beyond 0.1901.

### 3. TRUMP/USDT (crypto, short-watch — top score both timeframes)
Score 64.9 (intraday) / 62.7 (swing), price ~2.215, 24h -6.1%, RS vs BTC -4.21%, volume roughly at average (0.98x). No fresh verified catalyst. Setup: failed bounce/retest short thesis, watch zone 2.223-2.240, invalidation 1h close beyond 2.261. Known failure mode explicitly logged in the report itself: "No-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation" (14d cut: WR 23% / PF 0.70 / -3R). **Not actionable without a catalyst or RS-leader confirmation this cycle — treat as low-conviction watch, not the top pick despite the highest raw score.**

### 4. ENA/USDT (crypto, catalyst-watch — carried from 11:30)
Score 57.1, price 0.1513, 24h -8.58%. The only crypto symbol this cycle with a `canonical_news_event` catalyst (Ethena Pay app launch on Avalanche, up to 6% yield / 10% cashback — importance 1.75). Watch zone 0.1520-0.1537 pullback fill, invalidation 0.1557. Counter-thesis explicitly notes RS not backed by strong volume (0.47x) and price below average — genuine catalyst, weak technical confirmation. **Watch, not yet actionable; best catalyst-backed idea by elimination (no other crypto candidate has a resolved catalyst this cycle).**

### 5. DIS (stocks, avoid / pre-US BLOCK)
Short candidate, pre_gate_tier A, base_score 92.65 — but a fresh (~1h old at review time) single-source Telegram headline reports a third UPC/patent injunction from InterDigital against Disney. This is exactly the kind of fresh, code-hard-gate-invisible legal/IP risk the pre-US overlay's BLOCK verdict exists for. Not independently verified via a second source or WebFetch this cycle (external research unavailable this pass). **Short-TTL veto applied (expires ~2026-09-02T16:56 UTC per the ingest command's clamp); treat as avoid pending independent verification, do not use the pre-gate A score as a green light.**

## 8. Best Candidates Ranked

1. **PROM/USDT (manual review, open positions)** — top priority: resolve the bias-tag contradiction on the existing open longs before any new PROM exposure.
2. **0G/USDT (short-watch, C-tier)** — best clean short idea; needs a confirmed failed bounce below 0.1832-0.1868, not a chase.
3. **ENA/USDT (catalyst-watch, C-tier)** — best (only) catalyst-backed crypto idea; needs a confirmed pullback fill.
4. **TRUMP/USDT (short-watch, C-tier, low conviction)** — highest raw score but explicitly flagged by its own playbook as a historically net-negative no-catalyst setup; watch only if a catalyst or RS-leader signal appears.
5. **DIS (stocks, avoid-watch)** — best-scoring pre-US stocks candidate on paper (base_score 92.65) but currently vetoed by a fresh unverified legal headline; re-evaluate only after independent source verification and RTH confirmation.

If none of the above trigger: no other crypto or stocks candidate cleared even watchlist-quality this cycle — the honest read is genuinely thin, not a false "no trade."

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and the scheduler continue regardless, in all moods.

- **PROM/USDT** — do not add new exposure in either direction until the bias-tag contradiction on the existing open longs is manually resolved.
- **DIS** — fresh unverified single-source legal/IP headline; BLOCK veto active until independently verified.
- **HUT, GOOGL (stocks, short signals)** — catalyst read contradicts the short direction (Anthropic compute-deal beneficiary for HUT; Gemini 3.8 launch + bullish Berkshire commentary for GOOGL) — avoid as-is.
- **Chasing any crypto C-tier short** (0G, TRUMP, TAO, PENGU, NEAR, XRP, ENA) at the current print instead of waiting for the stated retest/pullback confirmation.
- **New pre-open stocks exposure generally** — market closed at review time; all 32 candidates are planning-levels-only pending RTH confirmation, per the regime's own hard cap.

## 10. Main Risks

- **Geopolitical escalation (Iran/Israel):** macro risk 100/100, actively cited as the BTC risk-off driver and tagged directly on BA (geopolitical_risk). Headline risk for gap moves at the US open.
- **Catalyst mapping weak this run (63.4% unmapped):** catalyst layer should be treated as context, not a final decision input, this cycle.
- **PROM/USDT bias-tag contradiction unresolved across multiple review cycles** — a recurring, symbol-agnostic pattern (per prior project history: ZBT/ACE in August, now recurring on PROM) that has not been fixed at the code level; advisory-only reviews keep re-flagging it without resolution.
- **Playbook base rates are weak:** crypto no-catalyst intraday momentum (used by every crypto C-tier idea this cycle) has a logged 14d cut of WR 23% / PF 0.70 / -3R. Stocks reliable tier-C triggered winrate is 6% (PF 0.36, n=612); stronger tier-B triggered winrate is 3% (n=85). None of today's ideas should be treated as high-probability without a genuine catalyst or RS-leader confirmation.
- **Single-source/unverified headlines** feeding both the DIS BLOCK and the HUT/GOOGL catalyst-contradiction reads — external web verification was not run this cycle; confidence on these specific reads is moderate, not high.

## 11. Action Plan — next 4 hours

1. Watch 0G/USDT for a confirmed 1h close back below 0.1832-0.1868 after a failed bounce before considering the short.
2. Watch ENA/USDT for a pullback fill inside 0.1520-0.1537 with 1h close confirmation.
3. Do not add new PROM/USDT exposure; flag the open longs for a human-driven manual-review session.
4. At/after the 09:30 ET open: re-run RTH confirmation on the pre-US stocks candidates, especially the CAUTION (HUT, GOOGL) and BLOCK (DIS) items — none should be treated as actionable purely on their pre-gate score.
5. Watch for Iran/Israel de-escalation headlines or oil giving back gains as the main catalyst that would flip the macro risk-off read.
6. No action on TRUMP/USDT, TAO/USDT, or the remaining C-tier crypto watchlist beyond passive monitoring — none have a catalyst or RS-leader confirmation yet.

## 12. Final Verdict per Mode

- **Crypto swing:** manual review required on PROM/USDT's two open longs; hold the existing book; no new entries recommended beyond watching ENA/USDT for confirmation.
- **Crypto intraday:** wait_for_trigger — 0G/USDT short-watch and ENA/USDT catalyst-watch are the cleanest ideas; neither confirmed yet; avoid chasing TRUMP/USDT despite its top raw score.
- **Crypto scalp:** report stale (3 days) — not evaluated this cycle; no action.
- **Stocks intraday:** planning-only, market closed — 32 pre-US candidates reviewed (0 SUPPORT / 4 NEUTRAL / 2 CAUTION / 1 BLOCK / 25 INSUFFICIENT_DATA); re-evaluate all after RTH confirmation; DIS and the CAUTION items (HUT, GOOGL) need independent verification before any action.
- **Stocks swing / invest:** deprecated legacy reports (>2 months stale) — not evaluated; shadow-only position framework continues separately per prior project history.

## 13. Sources

- [reports/STOCKS_PREUS_REVIEW_CANDIDATES.md](reports/STOCKS_PREUS_REVIEW_CANDIDATES.md) — generated 2026-09-02T12:54:28Z
- Internal `news_items` (Finnhub company-news, CNBC Markets, Yahoo Finance Top Stories, t.me/marketfeed, CryptoBriefing, t.me/CexAlerts) — HUT: "Anthropic To Acquire Computing Power From Hut 8" (Finnhub company-news, 2026-09-01T14:56:00Z); VRT: "Vertiv drops $1.45B to acquire microgrid specialist UIG..." (CryptoBriefing, 2026-09-02T10:47:36Z) + SEC EDGAR 8-K same day; GOOGL: "Berkshire CEO Abel says Alphabet a 'significant player' in AI..." (CNBC Markets, 2026-09-02T11:33:08Z); DIS: "DISNEY GETS THIRD UPC INJUNCTION FROM INTERDIGITAL" (t.me/marketfeed, 2026-09-02T12:03:59Z, single-source, unverified externally)
- `data/catalysts/2026-09-02/catalyst_events.jsonl`, `narrative_baskets.jsonl` — internal structured catalyst store, 2500 events / 915 mapped
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-02_1130.md`

## 14. Fix Requests / TODO

### TODO-preus-pending-deadline-status
- **issue:** `stocks-preus-review-health` returned `PENDING_DEADLINE` rather than one of the two documented terminal states (`READY` / `NO_ELIGIBLE`) even with 33/33 reviewed and 0 missing.
- **evidence:** health check output: `"status": "PENDING_DEADLINE", "reason": "structured_preus_review_not_yet_due"`, `reviewed_count: 33, missing_count: 0`.
- **suggested manual fix:** confirm this is expected behavior (deadline gate not yet reached) rather than a status-enum gap; if expected, consider documenting `PENDING_DEADLINE` alongside `READY`/`NO_ELIGIBLE` in the routine's health-check contract so future runs don't need to infer it.
- **priority:** low
- **first observed:** 2026-09-02 09:03 ET (this run)

### TODO-prom-bias-tag-contradiction-recurs
- **issue:** PROM/USDT again shows in both "Strongest Symbols" and "Weakest Symbols" (bias=short) simultaneously today, with two open long positions from 2026-08-30 now 30%+ underwater vs entry — the same systemic bias-tag contradiction pattern flagged repeatedly in project history (ZBT/ACE in August) and in the 11:30 review today.
- **evidence:** `data/reports/intraday/2026-09-02_11-41_intraday_report.md` §2 (PROM/USDT in both Strongest and Weakest lists); `proposed_signals` id 59160 (triggered swing long, entry 6.58-6.84, created 2026-08-30T04:34:08Z) vs current price 4.621.
- **suggested manual fix:** a human-driven session should investigate the regime/bias-tagging logic for symbols with open positions that have since reversed hard, and decide whether the open PROM/USDT longs should be manually closed or held.
- **priority:** high
- **first observed:** 2026-09-02 09:03 ET (this run); recurring since at least August per project history.

### TODO-stocks-expired-lifecycle-split
- **issue:** stocks lifecycle language requires splitting "expired" into entered-unresolved vs no-entry, but `proposed_signals` has no entry-fill timestamp column to do this programmatically; 13 stocks signals in the last 24h are status=`expired` with no clean split available.
- **evidence:** `PRAGMA table_info(proposed_signals)` has no `entered_at`/`filled_at` column; only `entry_trigger` (a price level, not a timestamp).
- **suggested manual fix:** add an entry-fill timestamp column (or reuse an existing status-history table if one exists) so future reviews can programmatically report the mandated entered-unresolved vs no-entry split instead of leaving it as `NEEDS REVIEW`.
- **priority:** medium
- **first observed:** 2026-09-02 09:03 ET (this run)

### TODO-hood-upgrade-not-in-preus-verdict-set
- **issue:** HOOD (short candidate in the pre-US stocks overlay) has a same-morning Morgan Stanley upgrade headline in `news_items` ("Morgan Stanley Just Upgraded Robinhood Markets Inc. (HOOD)", Yahoo Finance Top Stories, 2026-09-02T10:42:59Z) that reads bullish and was not folded into this cycle's verdict (HOOD was marked INSUFFICIENT_DATA, not CAUTION, in the time-critical hand-off pass).
- **evidence:** `news_items` row above; `preus_review_2026-09-02T125700Z.json` verdict for `sig_3b4f25cf63677442` (HOOD) = INSUFFICIENT_DATA.
- **suggested manual fix:** a follow-up manual session (not this scheduled run, per the "don't repeat ingest" rule) could re-score HOOD with this catalyst factored in, or wait for the next scheduled slot's fresh candidate set.
- **priority:** low
- **first observed:** 2026-09-02 09:04 ET (this run)
