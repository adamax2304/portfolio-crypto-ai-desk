# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:07 EEST

## 1. Executive Summary

Slot: **pre-US-open decision review** (16:20 EEST slot, fired ~15:59 EEST / 08:59-09:00 ET — on schedule, no DST drift). **Advisory only — no auto-trade, no scoring/threshold/routing changes.**

Time-critical hand-off completed first: `stocks-preus-candidates` found 28 eligible / 54 excluded stock candidates; all 28 were reviewed against internal news_items (no candidate met the strict SUPPORT bar — entity-resolved + fresh + market-context-fresh + RS-confirmed — so all landed **NEUTRAL** except **BA** and **GE** at **CAUTION** for catalyst contradiction, and 3 at **INSUFFICIENT_DATA** for false symbol matches); ingested via `stocks-preus-review-ingest --review-cycle preus_0900`; `stocks-preus-review-health` reports **READY** (28/28 reviewed, 0 missing).

Crypto stays technically risk-on (BTC/ETH uptrend, breadth 91.7% above EMA20) but the desk's own macro layer scores geopolitical risk **100/100** (Iran/Strait-of-Hormuz sanctions, Ukraine missile escalation, US-Canada trade friction) — a real, not noise, tension. No A-tier crypto exists; all 50 open crypto positions are **B-tier long** — the system genuinely isn't finding shorts right now.

Stocks: US cash session is **closed** pre-open — every stocks A-idea (V, LMT, MSTR, NOW, PEP, COST, GOOGL, COIN, HOOD, UBER, TSLA) is capped to C (`market_closed_intraday_planning_only`). Realized performance this week is a stark, not subtle, signal: stocks longs are **PF≈0.0 / −16.5R (n=334)** vs shorts **PF≈1.3 / +1.5R (n=384)**, and *every* stocks tier (A/B/C) currently shows single-digit-to-low-teens win rates — this is a book-wide stocks-intraday quality problem, not one bad tier. Route hard toward shorts and RTH-confirmed setups only; do not chase longs at the open.

One external-verification catch: a Telegram headline this morning cites Strategy/MSTR building a "**$1.6B cash war chest**" — WebSearch + WebFetch (TipRanks, CryptoTimes) show the actual disclosed reserve is **$3.75–4.8B as of Aug 16–20**, several days old, not a fresh $1.6B event. Treated as a **stale/inaccurate recycled headline**, not a real catalyst (§7.5).

Catalyst mapping is weak this run (**75.5% unmapped**, 367/1500 mapped) — use as context only, not decision input. 9 fresh untracked legacy crypto alerts detected (Telegram-sent, no proposed_signal) — same open integrity gap as prior reviews, still unresolved (§14).

## 2. Data Used

- Reports: crypto scalp (2026-08-24 13:07 EEST, ~2h55m old), crypto intraday (13:18, ~2h44m), crypto swing (14:35, ~1h27m — fresh), stocks intraday (13:56, ~2h6m — fresh, pre-open at generation and now).
- Stocks swing/invest: deprecated framework, stale since 2026-07-02 — excluded.
- `data/processed/llm_analysis_packet.md` (14:35), `data/processed/llm_stocks_packet.md` (13:56).
- `data/catalysts/2026-08-24/catalyst_events.jsonl` (1500 rows, growing), `narrative_baskets.jsonl` (4 baskets).
- CLI: `active-signals` ×2 (crypto 50 rows all B-long; stocks 50 rows, all `expires_at` in the past — historical/entered-unresolved, not live triggers), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-08-24` (9 findings).
- Pre-US overlay: `stocks-preus-candidates` (28 eligible/54 excluded) → `stocks-preus-review-ingest` (28/28 OK) → `stocks-preus-review-health` (READY).
- External: WebSearch ×1 (MSTR cash-reserve figure verification) + WebFetch ×1 (CryptoTimes, confirmed content); WebFetch ×1 to TipRanks returned HTTP 403 (noted, not treated as confirming or denying anything).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-24_1204.md` (Europe/pre-US context, 12:04 EEST, ~4h ago) — used for §4 comparison.

## 3. Scheduler / Data Freshness

- **Pre-US schedule check:** target 09:00 ET, actual fire ~08:59–09:00 ET (Δ≈0, within tolerance) — steady-state 7h Nicosia/NY offset holds, not inside either 2026 DST-mismatch window (2026-03-08→03-29, 2026-10-25→11-01).
- Active scheduler folder: `data/scheduled_runs/2026-08-24_default_schedule/`. `scheduler.log` mtime ~14:49 EEST (~1h18m old), latest `cycle_01_12-54_summary.md` same mtime — well inside the 3h defer threshold. **Not deferred.**
- All four crypto reports + stocks intraday fresh (<3h). No swing/invest stocks reports used (deprecated, >1200h old).
- Catalyst data fresh, same-day, actively growing (1500 events now vs 1000 at 12:04 EEST run).
- No monitor/paper-portfolio status file read this run (outside allowed read set); lifecycle inferred from `active-signals` + reports.
- Cadence: this run is ~1h44m after the 12:04 EEST run — normal cadence, no gap (prior 5-day gap from TODO-1 in the 12:04 review appears resolved).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-24 16:07 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh"],
      "data_missing": ["live monitor/paper-portfolio status file", "live SPY/QQQ futures print (no chart/quote MCP loaded)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log + cycle_01 summary ~1h18m old", "all crypto + stocks-intraday reports <3h", "catalyst dir fresh, 1500 events", "pre-US health=READY, 28/28 reviewed"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "risk_off", "shorts_preferred", "wait_for_trigger"],
      "data_missing": ["live pre-market SPY/QQQ tape", "live VIX print (report VIX=15.90 is from 13:56 EEST snapshot)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: desk label 'bullish trend (risk-on)', breadth 91.7%/93.75% above EMA20/50, but macro-geopolitical risk 100/100", "stocks: desk regime label 'transition/neutral', risk_on=False, VIX 15.90 (calm), SPY/IWM uptrend but QQQ/DIA range", "sector rotation: consumer_discretionary/healthcare/energy strong; semiconductors/industrials/utilities weak", "stocks direction stats: longs PF~0.0 −16.5R (n=334) vs shorts PF~1.3 +1.5R (n=384)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "no_catalyst", "catalyst_contradicted", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 367/1500 mapped (75.5% unmapped) this cycle", "NEAR/USDT: fresh regulatory/partnership catalyst (quantum-resistant transfer pilot) persists from prior cycle", "GILD: EU approval of Trodelvy+Keytruda combo, fresh <2h, entity-resolved", "MSTR: WebSearch+WebFetch show the 't.me' $1.6B war-chest figure does not match verified $3.75-4.8B disclosed Aug 16-20 - stale/inaccurate recycled headline, not fresh news", "BA/GE stocks candidates: catalyst found but framed bullish while the desk signal is short — contradiction, not confirmation"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["stocks options/OI data (not available for stocks per packet)", "OI for MEXC-fallback names"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: VIRTUAL/PENGU/MORPHO/POL price up + OI up, funding near-neutral (~5e-05), crowding normal", "TUT/FF: price up + OI down, short covering, weaker continuation quality", "no funding_extreme reading anywhere today"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "clean_retest", "overextended", "stale_before_entry"],
      "data_missing": ["intraday tick data for chase/retest confirmation (no chart MCP)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/PORTAL/POL momentum-breakout basket 10-34% extended over 24h, several tagged 'overextended'", "VIRTUAL/USDT swing signal is waiting_for_entry at a defined pullback zone (0.7382-0.7469), not chasing", "TSLA/PLTR/ABNB show strong RS-vs-SPY (12-43%) but all capped C pending RTH confirmation (market closed)"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals (50): 28 triggered, 10 waiting_for_entry, 8 tp1_hit, 4 tp2_hit — all open/tracked, none formally closed", "stocks active-signals (50): every row has expires_at in the past (as far back as 2026-07-21) — these are entered-unresolved/stale-tracked positions, not live triggers; needs-review candidate for §14", "9 untracked legacy crypto alerts today (Telegram-sent, no proposed_signal) — recurring integrity gap"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["headline_risk", "correlation_cluster", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["SMCI still excluded LEGAL_RISK this cycle — prior review (12:04 EEST) flagged this as possibly stale vs. a concluded/cleared Aug-20 investigation (TODO-3, carried forward unresolved)", "PUMP/USDT: open B-tier swing LONG position, but today's internal RS data tags it bias=short with 24h -5.94% / RS vs BTC -6.65% — a bias-tag contradiction matching a previously-escalated HIGH-priority pattern ([[project_crypto_ai_desk_bias_tag_contradiction]])", "MAR/HUT/INTU/BAC/REGN/BLK also excluded LEGAL_RISK this cycle (unreviewed further, per contract — exclusion is final)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto by-mode: scalp PF~0.1/-4.5R (n=98, weak), intraday PF~1.6/+14.6R (n=120), swing PF~2.4/+49.8R (n=156, best) — matches known playbook ranking", "crypto weekend-mode signals underperform (PF~1.5 vs 2.3 non-weekend) — system-flagged observation", "stocks: ALL tiers weak this week — A n=18 WR8%/PF0.00, B n=89 WR3%/PF0.06, C n=611 WR11%/PF0.58 — system-flagged observations, escalated severity vs the 12:04 EEST review which only flagged the direction split"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "NEAR/USDT", "trigger": "already triggered/open (swing, entry ~1.99-2.01), catalyst-backed", "reason": "genuine regulatory/partnership catalyst persists from prior cycle, RS-leader-adjacent, crypto breadth supportive" },
    "best_short_candidate":    { "symbol": "AMAT (stocks, watch)", "trigger": "RTH confirmation of continued weakness below entry_trigger 492.51 with semiconductors sector still weak (RS vs SPY -3.76%, below EMA50)", "reason": "sector-aligned short, but pre-US review verdict was NEUTRAL (no entity-resolved catalyst) — needs RTH technical confirmation, not catalyst-driven" },
    "best_catalyst_candidate": { "symbol": "GILD", "trigger": "already fresh (EU Trodelvy+Keytruda approval, <2h old, entity-resolved) — long, but pre-US ingest kept NEUTRAL pending RS-vs-sector confirmation", "reason": "cleanest entity-resolved fresh catalyst of the 28 reviewed candidates" },
    "avoid_candidate":         { "symbol": "MSTR / stocks-longs-at-the-open generally", "reason": "MSTR: catalyst cited by desk news is a stale/inaccurate recycled figure (verified via WebSearch+WebFetch); stocks longs broadly: PF~0.0, -16.5R (n=334) this week, and every tier (A/B/C) shows single-digit-to-low-teens win rates today" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.65 | mixed, risk_off, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, no_catalyst, catalyst_contradicted, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, clean_retest, overextended, stale_before_entry | advisory_only |
| execution_lifecycle | caution | 0.70 | open_actionable, waiting_for_entry, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, correlation_cluster, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.75 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (12:04 EEST)

- **New this run:** the pre-US stocks overlay (28 candidates scored NEUTRAL/CAUTION/INSUFFICIENT_DATA) — did not exist in the 12:04 review, which only had the base candidate list.
- **Confirmed:** crypto stays all-B-tier-long, no A-tier anywhere; catalyst mapping still weak (74.6%→75.5% unmapped, essentially unchanged); crypto scalp mode still the weak playbook (PF~0.1-0.17 both runs); stocks direction split (longs weak / shorts positive) persists and has widened in evidence (now every stocks tier shows weak win rates, not just the direction split).
- **New finding:** MSTR's "fresh" $1.6B cash-war-chest headline verified as stale/inaccurate (actual disclosed figure $3.75-4.8B, dated Aug 16-20) — not flagged in the 12:04 review since MSTR wasn't in its candidate set.
- **New finding:** PUMP/USDT bias-tag contradiction (open long, today's data tags bias=short) — recurrence of a pattern previously escalated to HIGH in [[project_crypto_ai_desk_bias_tag_contradiction]] (last seen 2026-08-08), not mentioned in the 12:04 review.
- **Upgraded/downgraded:** none — no signal changed tier between the two runs (both prior and current snapshot show the same 50 crypto B-longs; the same stocks A/B are still capped C by the market-closed gate).
- **Thesis unchanged:** NEAR/USDT remains the strongest catalyst-backed crypto long across both reviews. SMCI legal-flag-vs-resolved-investigation tension (TODO-3 from 12:04 review) remains open and unresolved this run too.

## 5. Catalyst Coverage

- Total catalyst events today: **1500**; mapped (non-null symbol): **367**; unmapped: **1133** (**75.5% unmapped**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets: **4** active (perps_dex_narrative, binance_ecosystem_teaser, ai_narrative, momentum_breakout).
- Top 3 unmapped headlines (sample): "Bybit now supports $GROVE deposits..." (exchange-listing noise, no equity/crypto-asset symbol to map); "NOMURA INTERNATIONAL FUNDING SECURED AN 'A-' CREDIT RATING..." (macro/credit, no tracked symbol); "LACK OF FED COMMUNICATION FUELING BOND YIELD SURGE-WSJ" (macro, no symbol).

### Pre-US Stocks Review Overlay
- candidates reviewed: 28 (SUPPORT 0 / NEUTRAL 24 / CAUTION 2 / BLOCK 0 / INSUFFICIENT_DATA 2)
- session-cap-only C's now eligible for pre-open Paper lane: 0 (no SUPPORT verdicts issued — none of the 28 met the full entity-resolved + fresh + market-context-fresh + RS-confirmed bar)
- excluded by hard gate: 54 (NO_ENTITY_RESOLVED_CATALYST: 45 incl. AAPL, NVDA(earnings)†, QQQ, SPY, JPM, ORCL, CRM, PLTR, ADBE, SHOP, ABNB and others; LEGAL_RISK: 8 — MAR, HUT, INTU, BAC, REGN, BLK, SMCI, plus WMT/NVDA under EARNINGS_BLACKOUT)
  - † NVDA and WMT excluded under EARNINGS_BLACKOUT, not LEGAL_RISK — corrected grouping.

## 6. Market Landscape

Crypto: BTC/ETH in uptrend, 91.7% of tracked symbols above EMA20, desk regime label "bullish trend (risk-on)," confidence 100/100 — but this confidence score reflects trend-following mechanics, not macro context. The macro/geopolitical layer separately scores risk at 100/100 (7 risk-off hits, 0 risk-on) driven by Iran/Strait-of-Hormuz sanctions escalation, France/UK missile support to Ukraine, and a Canada-US trade dispute — a genuine two-layer tension: technically bullish, macro-fragile.

Stocks: regime label "transition," bias neutral, risk_on=False. VIX 15.90 (calm, not stressed). SPY/IWM in uptrend, QQQ/DIA range — index leadership is narrower than crypto's breadth suggests. Sector rotation: consumer_discretionary/healthcare/energy strong (RS+3-4% vs SPY); semiconductors/industrials/utilities weak (RS -4% to -11%, below EMA50). This sector split directly supports the AMAT/INTC short candidates (both semis) and argues caution on MU (long, also semis, swimming against a weak sector).

### Market Mood / Risk Routing
- Crypto mood: **mixed** (technically risk-on, macro risk-off — the two layers disagree; treat as chop/danger for aggressive sizing, not a clean risk-on stance)
- Stocks mood: **closed / pre-market** (regime label neutral/transition once open; VIX calm; longs realized-PF is weak book-wide this week — treat as risk-off-leaning for longs specifically, not for the whole book)
- Dominant narrative: crypto — AI/RWA/Memes all "mixed" status, momentum_breakout basket (VIRTUAL/ZAMA) the most active; stocks — no single dominant theme, sector rotation into cyclicals/healthcare/energy away from semis/industrials/utilities
- Preferred side now: **crypto: selective longs, RS-leader + catalyst-confirmed only; stocks: shorts preferred (PF 1.3 vs 0.0 this week), longs require RTH confirmation and real RS + sector alignment, not chase**
- Best long candidate: NEAR/USDT (crypto, catalyst-backed, already open) — stocks: TSLA/PLTR watch-only pending RTH (strong RS, no catalyst)
- Best short candidate: crypto — none clean (all-long book, no active short signals); trigger: 1h-close breakdown in ENA/USDT (weakest today, -10% 24h, RS -10.7% vs BTC) or a confirmed break of BTC/ETH uptrend structure. Stocks — AMAT/INTC watch, trigger: RTH confirmation of weakness below their entry_trigger levels while semis sector stays below EMA50.
- Best catalyst-backed candidate: GILD (EU approval, entity-resolved, fresh <2h) — long, watch for RS-vs-sector confirmation before treating as clean.
- What to avoid: MSTR long on the stale $1.6B headline; PUMP/USDT (bias-tag contradiction — do not add to the open long); chasing the momentum-breakout basket (TUT/PORTAL/POL, 10-34% extended) at spot; new stocks longs before RTH confirms (book-wide PF≈0 this week).
- What would change the view: a de-escalation headline on Iran/Hormuz (would resolve the crypto mixed-mood tension toward genuine risk-on); a clean RTH open above pre-market highs with rising relative volume on TSLA/PLTR (would upgrade them from watch to actionable); reversal of the stocks long-side PF this week (currently -16.5R).

## 7. Candidate Deep Dives

### 7.1 NEAR/USDT — LONG (crypto, swing, triggered, B-tier, score 67.4)
- Catalyst: regulatory/partnership — banks/regulators joining a quantum-resistant crypto transfer pilot on NEAR testnet (CryptoBriefing), part of the `ai_narrative` basket, fresh <6h, entity-resolved, unchanged from the 12:04 review.
- Price reaction: already triggered and open; not a fresh chase — position was entered on this catalyst.
- Chase/retest: N/A (already in position). Aligned with mood: yes — crypto breadth is bullish, this is a catalyst-confirmed name inside that trend, not a low-quality momentum-only add.
- Actionable: yes, already open. Invalidation: below ~1.97 per active-signals row.
- Would invalidate: 1h close below invalidation level, or a reversal/contradiction of the quantum pilot story.

### 7.2 VIRTUAL/USDT — LONG (crypto, swing + intraday, B-tier, score up to 77.2)
- No verified catalyst — part of the `momentum_breakout` narrative basket, previously labeled by the desk as a "pure momentum cluster" without confirmed news.
- Price reaction: already up 8.29% 24h, RS vs BTC +7.58%, volume 1.24x — real strength, not manufactured, but purely technical.
- Chase/retest: swing signal is `waiting_for_entry` at a defined pullback zone (0.7382-0.7469), not chasing at spot — this is the correct posture.
- Actionable: only at the stated pullback zone; not a market-buy at current price if extended.
- Would invalidate: 1h close beyond 0.7275, or the pullback zone never fills before signal expiry (2026-08-31).

### 7.3 TSLA — LONG-WATCH (stocks, intraday, pre_gate_tier A, base_score 93.0, capped to C)
- Catalyst: none material found (only generic listicles/hold-rating opinion pieces) — pre-US review verdict NEUTRAL.
- Market context: sector consumer_discretionary is one of today's strongest (RS+4.24% vs SPY, 20d +7.87%); TSLA itself carries RS vs SPY +12.29% per the demoted-near-A/B list — strong technical alignment even without a catalyst.
- Setup quality: rr_to_tp1 1.5, atr_measured target, volume_ratio 1.13 — clean structure. Entry_trigger 362.88, stop 357.77.
- Is this chasing? No — has not yet had RTH confirmation; the question at the open is whether it holds/extends above pre-market levels on real volume, not whether it's already extended.
- Actionable: **only after RTH confirmation** (first 15-30min), per the slot's own governing rule — do not chase the pre-market print.
- Would invalidate: opens below entry_trigger, or fails to hold sector-relative strength in the first 30 minutes.

### 7.4 BA — SHORT, contradiction flagged (stocks, intraday, pre_gate_tier B, base_score 77.66, capped to C)
- Catalyst found: a Motley Fool opinion piece ("A Win-Win Deal") framing the Archer Aviation-Boeing partnership positively — published ~06:45 UTC, single opinion source, not primary.
- **Contradiction:** the catalyst tone (bullish) contradicts the desk's short direction on BA. Pre-US review verdict: **CAUTION**, requested adjustment -4 (clamped by the ingest code, not this review).
- Is this chasing? Cannot assess without RTH confirmation; the short thesis specifically needs to be re-validated against the bullish framing before treating it as clean.
- Actionable: **no** — manual review preferred; if shorting at all, require a technical failure at the open, not the catalyst as support.
- Would invalidate the short: a confirmed pre-market/RTH pop on real volume tied to the Archer deal.

### 7.5 MSTR — LONG, catalyst found stale (stocks, intraday, pre_gate_tier A, base_score 81.9, capped to C)
- Catalyst as reported internally: t.me/marketfeed + t.me/WalterBloomberg, ~1h old, "$1.6 billion cash war chest."
- **External verification (WebSearch + WebFetch, CryptoTimes):** Strategy's actual disclosed USD reserve was **$4.8B as of Aug 16, 2026**, later reported at $3.75B (TipRanks headline, fetch blocked HTTP 403) and $3B (Motley Fool, Aug 3) — none of these match $1.6B, and the news itself is 4-8 days old, not a fresh event. This is a **stale/inaccurate recycled headline**, not real fresh news, despite passing the desk's freshness/entity-resolution checks on timestamp alone.
- Pre-US ingest verdict was NEUTRAL (correctly conservative — the strict SUPPORT bar was not met due to missing RS confirmation), but the review record should note the catalyst itself does not hold up under verification.
- Actionable: **no** — treat as a plain technical name if considered at all post-open; do not cite the cash-reserve headline as a reason to go long.
- Would invalidate/change the view: a genuinely new, dated, sourced disclosure (SEC filing or company IR release) with a verifiable figure.

## 8. Best Candidates Ranked

1. **NEAR/USDT** — LONG, catalyst-backed, already open/actionable. Best overall candidate this cycle (unchanged from 12:04 review).
2. **VIRTUAL/USDT** — LONG-WATCH, best pure-RS/momentum name, but wait for the stated 0.7382-0.7469 pullback zone; no catalyst.
3. **TSLA** — LONG-WATCH (stocks), best technical/sector-alignment candidate for post-open; needs RTH confirmation, no catalyst yet.
4. **Short-watch (crypto):** none live. Trigger: confirmed 1h-close breakdown in ENA/USDT (weakest today, -10% 24h) or a volume-confirmed break of BTC/ETH uptrend structure.
5. **Short-watch (stocks):** AMAT / INTC. Trigger: RTH confirmation of continued weakness below their entry_trigger levels (492.51 / 90.06) while the semiconductors sector (SMH) stays below its 50-day EMA; realized stats this week strongly favor shorts (PF~1.3) over longs (PF~0.0) once confirmed.
6. **Catalyst-watch:** GILD (EU Trodelvy+Keytruda approval, entity-resolved, fresh) — long, watch for RS-vs-sector confirmation before treating as clean; not yet SUPPORT-grade.

## 9. Avoid / No Trade

*(This decision window only — never a command to stop scanning, tracking, or the scheduler.)*

- **MSTR long on the "$1.6B war chest" headline** — verified stale/inaccurate; do not use as a reason to enter (§7.5).
- **PUMP/USDT** — existing open long carries a bias-tag contradiction (today's data tags it bias=short, 24h -5.94%); do not add to this position; flag for manual review (§14).
- **SMCI** — still excluded LEGAL_RISK this cycle; prior review flagged the flag as possibly stale vs. a concluded/cleared investigation — unresolved, not actionable either way today.
- **Momentum-breakout cluster at spot** (TUT, PORTAL, POL — 10-34% extended over 24h) — only actionable at stated pullback zones, not at market price.
- **New stocks longs before RTH confirmation** — realized PF≈0.0 / -16.5R this week across all 334 long signals, and every stocks tier (A/B/C) shows single-digit-to-low-teens win rates today; do not chase the pre-open C-tier watchlist.
- **BA short on the current catalyst read** — the only catalyst found contradicts the short thesis; needs a technical trigger, not catalyst support (§7.4).

## 10. Main Risks

- **Macro/crypto mood mismatch:** crypto technicals are bullish but the macro-geopolitical score is maxed at 100/100 (Iran/Hormuz, Ukraine, Canada-US trade friction) — a de-escalation or escalation headline could move price faster than the technical picture implies.
- **Stocks book-wide quality problem:** not just a long/short split — every stocks tier (A/B/C) shows weak realized stats this week (win rates 3-11%, PF 0.00-0.58). Treat all stocks A/B ideas today with elevated skepticism regardless of catalyst quality.
- **Catalyst mapping weak (75.5% unmapped)** — the catalyst layer materially undercounts what's actually happening; do not treat "no catalyst found" as proof nothing is happening.
- **Untracked alert leakage:** 9 crypto Telegram alerts today have no backing proposed_signal — those outcomes will never be counted in PF/winrate stats, silently understating (or overstating) true performance.
- **Entity-resolution ambiguity:** the GE short signal's catalyst match ("GE Vernova... AI datacenter UPS") may actually refer to GEV (GE Vernova, spun off from GE Aerospase in 2024), a distinct entity from the GE ticker in this system — flagged as possible mismatch, not confirmed as genuine GE-specific news (§14 TODO).

## 11. Action Plan — next 4 hours

1. Hold NEAR/USDT long; do not add size on the catalyst alone — it is already priced into the open position.
2. Watch VIRTUAL/USDT for a fill in the 0.7382-0.7469 pullback zone; do not chase at spot.
3. At/after the 09:30 ET cash open: require RTH confirmation (first 15-30min) before treating TSLA, GILD, or any capped-C stock idea as actionable — this applies to every stocks A/B this cycle, none are pre-cleared.
4. Prefer stocks shorts over longs if a clean RTH setup appears (AMAT/INTC watch first, given sector alignment); avoid fresh stocks longs without RS + sector confirmation.
5. Do not add to PUMP/USDT; flag for manual bias-tag review.
6. Do not cite the MSTR "$1.6B" headline as a reason for any action.
7. Continue scanning/tracking as normal in all modes — no pause, no stop, regardless of the caution verdicts above.

## 12. Final Verdict per Mode

- **Crypto scalp:** caution — playbook PF~0.1 this week, treat any new scalp alert as research-grade only.
- **Crypto intraday:** watch — PF~1.6, acceptable but not the strongest lane; prefer catalyst-backed names.
- **Crypto swing:** watch/actionable — PF~2.4, the strongest crypto lane this week; NEAR/USDT and VIRTUAL/USDT (at its pullback zone) are the cleanest current ideas.
- **Stocks intraday:** manual_review — market closed pre-open; once open, require RTH confirmation and prefer shorts (PF~1.3) over longs (PF~0.0) given this week's book-wide weak tier performance.
- **Stocks swing/invest (old):** not applicable — deprecated/removed, never actionable.
- **Stocks swing growth-breakout (new):** shadow-only research — 5 open candidates (JPM, BAC, BLK, MRK, LLY per the packet); not actionable, no change to that status this run.

## 13. Sources

- [MicroStrategy (MSTR) Shifts Strategy, Sells Shares to Boost Cash Reserves — GuruFocus](https://www.gurufocus.com/news/9038939/microstrategy-mstr-shifts-strategy-sells-shares-to-boost-cash-reserves) — 2026-08 (exact date not stated on snippet)
- [Strategy (MSTR) Stock Jump 5% After Fresh Cash Raise and STRC Buybacks — CryptoTimes](https://www.cryptotimes.io/2026/08/18/strategy-mstr-stock-jump-5-after-fresh-cash-raise-and-strc-buybacks/) — 2026-08-18, confirms $4.8B reserve as of 2026-08-16; fetched and content-verified
- [MicroStrategy Soars As Massive Cash War Chest Calms Fears — TipRanks](https://www.tipranks.com/news/catalyst/microstrategy-soars-as-massive-cash-war-chest-calms-fears) — fetch attempt returned HTTP 403, not used as a confirming source, listed for completeness
- [Michael Saylor's Strategy Just Boosted Its Cash Reserve to $3.75 Billion — The Motley Fool](https://www.fool.com/investing/2026/08/03/michael-saylors-strategy-just-boosted-its-cash-res/) — 2026-08-03
- Internal: `data/catalysts/2026-08-24/catalyst_events.jsonl`, `narrative_baskets.jsonl`; `news_items` table queries (t.me/marketfeed, t.me/WalterBloomberg, Seeking Alpha Market Currents, Finnhub company-news, The Motley Fool Investing, PR Newswire (Stocks)) — dates as cited inline in §7.

## 14. Fix Requests / TODO

### TODO-A: PUMP/USDT bias-tag contradiction (recurrence)
- **issue:** Open B-tier swing LONG on PUMP/USDT, but today's internal RS/weakest-symbols data tags it bias=short (24h -5.94%, RS vs BTC -6.65%). This matches a previously-escalated HIGH-priority pattern documented in memory ([[project_crypto_ai_desk_bias_tag_contradiction]]) — open longs tagged bias=short with negative 24h, last confirmed 2026-08-08 across 3 consecutive reviews.
- **evidence:** `active-signals --asset-class crypto` row `sig_8248725e0a086fc9 PUMP/USDT B swing long triggered`; `llm_analysis_packet.md` §Weakest Symbols row "PUMP/USDT: bias short, 24h -5.94%, RS vs BTC -6.65%".
- **suggested manual fix:** investigate whether the bias-tagging logic and the open-position tracker are reading from different/stale snapshots, or whether this is a genuine trend reversal not yet reflected in position management.
- **priority:** high (recurrence of an already-escalated pattern)
- **first observed (this recurrence):** 2026-08-24 16:07 EEST

### TODO-B: Catalyst mapping stuck at ~75-80% unmapped (recurring)
- **issue:** Unmapped rate 75.5% today, 74.6% at 12:04 EEST, 79.8% on 2026-08-19 — persistent, not one-off.
- **evidence:** this run: 1133/1500 unmapped; prior reviews as cited.
- **suggested manual fix:** unchanged from prior reviews — consider a macro/no-symbol bucket for headlines that are genuinely non-ticker-specific instead of forcing a mapping attempt.
- **priority:** medium
- **first observed:** carried forward, first noted 2026-08-19 or earlier.

### TODO-C: SMCI legal/headline-risk flag still unresolved vs. concluded investigation
- **issue:** SMCI is still excluded LEGAL_RISK this cycle; the 12:04 EEST review flagged that the underlying investigation reportedly concluded and cleared management on 2026-08-20, meaning the internal flag may be stale. Not re-verified externally this run (time-budget prioritized toward the MSTR catalyst check).
- **evidence:** `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md` excluded list, `sig_2c51aef5422f26ad SMCI LEGAL_RISK`; prior review §7.3/TODO-3.
- **suggested manual fix:** unchanged — review the SMCI legal-risk record source and refresh against the Aug-20 resolution if confirmed.
- **priority:** medium
- **first observed:** carried forward from 2026-08-24 12:04 EEST.

### TODO-D: Possible GE / GE Vernova (GEV) entity-resolution conflation
- **issue:** The catalyst matched to the GE short signal ("GE Vernova: introduces medium-voltage UPS...") appears to reference GE Vernova (GEV), a company spun off from GE Aerospace in 2024 and a distinct ticker/entity from GE. If the catalyst resolver is matching "GE Vernova" headlines to the GE symbol, that is a false entity match, not genuine GE-specific news.
- **evidence:** `news_items` row matched to `sig_98befbb12be39cb8` (GE short), title "GE VERNOVA: INTRODUCES MEDIUM-VOLTAGE UPS TO HELP ACCELERATE BUILDOUT OF AI FACTORIES..." (t.me/marketfeed, 2026-08-24T09:22:18+00:00).
- **suggested manual fix:** check whether the symbol-detection layer distinguishes GE (GE Aerospace) from GEV (GE Vernova) as separate entities; if not, add that distinction.
- **priority:** medium
- **first observed:** 2026-08-24 16:07 EEST

### TODO-E: Stocks book-wide tier performance has worsened, not just the direction split
- **issue:** The 12:04 EEST review flagged the stocks long/short direction split (PF 0.08 vs 1.30). This run's `signal-stats` additionally shows every stocks tier is weak: A n=18 WR8%/PF0.00, B n=89 WR3%/PF0.06, C n=611 WR11%/PF0.58 — the problem looks broader than a directional bias, closer to a book-wide stocks-intraday quality issue this week.
- **evidence:** `python -m src.cli signal-stats --asset-class stocks` → "observations (manual approval required)" block, this run.
- **suggested manual fix:** a human review of whether this is regime-appropriate (route around, no code change) or a real degradation needing recalibration — same framing as TODO-5 in the 12:04 EEST review, now with tier-level evidence added.
- **priority:** medium
- **first observed:** 2026-08-24 16:07 EEST (escalates 12:04 EEST TODO-5 with new evidence)
