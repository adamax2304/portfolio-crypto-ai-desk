# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:30 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context (11:30 EEST). Advisory only — no auto-trade.** Crypto is in a range/chop regime with a risk-off macro overlay (Iran/Hormuz tensions, rising Treasury yields); no A- or B-tier crypto ideas fired this cycle, but two RS-leader longs (POL, HEMI) sit `WAITING for entry`. Stocks cash session is still closed (opens 13:30 UTC / 16:30 EEST) — 20 C-tier planning-only signals queued for the open, headed by LRCX, CRCL, ASML, INTC. The standout catalyst this run is **GE Aerospace**: a confirmed JASSM engine (GEK800/F143) USAF contract win from Kratos+GE, already `tp1_hit` on the existing A-tier signal with a fresh continuation C-tier queued for the open. Best short-watch is **ADA/USDT**, both technically weak-vs-BTC and carrying a real bearish catalyst (Cardano governance-freeze risk, two-week deadline). Catalyst mapping is weak this run (70.3% unmapped) — treat the catalyst layer as context, not a final decision driver. No system-integrity anomalies found (no untracked legacy alerts).

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-17_default_schedule/scheduler.log` (actively writing as of 11:40 EEST)
- Reports: intraday (08:17 EEST, fresh), scalp (10:49 EEST, fresh), swing (08:11 EEST, fresh), stocks intraday (07:16 EEST, carry-forward)
- LLM packets: `llm_analysis_packet.md` (crypto), `llm_stocks_packet.md` (stocks)
- Catalyst layer: `data/catalysts/2026-08-18/catalyst_events.jsonl` (1,444 events), `narrative_baskets.jsonl` (4 baskets)
- CLI: `active-signals` (crypto ×46, stocks ×50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts`
- Internal DB: `news_items` table in `db/crypto_ai_desk.sqlite` (118,616 rows) queried for GE, LRCX, POL, HEMI, ADA
- External: WebSearch ×4, WebFetch ×1 (GE Aerospace press release primary source)

## 3. Scheduler / Data Freshness

- `scheduler.log`: live, last line at 11:40 EEST (< 1 min old) → **scheduler_fresh**, no defer.
- Latest cycle summary `cycle_04_05-45_summary.md`: mtime 08:20 EEST (~3h20m old) — within tolerance, not deferred.
- Crypto intraday report: 08:17 EEST generation, ~1h20m old → **fresh**.
- Crypto scalp report: 10:49 EEST → **fresh**.
- Crypto swing report: 08:11 EEST (~3h30m old) → **fresh** (<4h bracket).
- Stocks intraday report: 04:16 UTC / 07:16 EEST (~4h23m old) → **carry-forward** (4–12h bracket); regenerating now per scheduler log (`CMD START: stocks intraday report` at 11:40).
- Stocks swing/invest reports: dated 2026-07-02 → **expected stale** — these playbooks are deprecated/removed per prior audits, not a freshness bug.
- Paper portfolio ledger refresh: completed 11:36 EEST (exit=0). Market intelligence health check: OK (11:40).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-18 11:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "derivatives_sparse"],
      "data_missing": ["stocks index 5d/20d returns (NaN for SPY/QQQ/IWM/DIA)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log 11:40 EEST", "stocks intraday report mtime 07:16 EEST", "regime snapshot JSON showing NaN index returns"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chop", "risk_off", "mixed"],
      "data_missing": ["reliable SPY/QQQ trend (NaN return fields undermine the risk_off stocks label)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime label range/chop, breadth 52.5% above EMA20", "stocks regime risk_off, VIX 15.19 (calm, contradicts risk_off framing)", "macro risk score 100/100, Iran/Hormuz + yield headlines"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["70.3% of today's catalyst_events unmapped to a symbol", "GE JASSM/GEK800 contract confirmed via 6+ independent wire sources", "ADA Cardano governance-freeze risk confirmed via CryptoSlate"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["POL, ADA, GE, LRCX derivatives/OI not in current derivatives snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HEMI: price up + OI up 5.48%, long/short 1.214 — fresh positioning confirms trend"] },
    { "agent": "technical_entry", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["entry_fresh", "chase_risk", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["POL/HEMI intraday waiting_for_entry, close to trigger zone", "EDEN/USDT >2 ATR from EMA20, system-rejected for chase risk"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 2 waiting_for_entry, ~19 open/running, ~25 already closed (win) past expiry", "stocks: 20 waiting_for_entry (pre-open C-tier), ~9 open/running today, ~21 closed past expiry"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HD, PANW earnings today — block_requires_operator_review + do_not_chase_warning", "macro risk-off headwind: Hormuz Strait vessel attack, US 30y yields highest since 2007"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing: PF 6.00, avgR +0.79, n=43, stronger confidence", "crypto intraday: PF 0.77, avgR -0.175, n=25, weak", "crypto scalp: PF 0.50, avgR -0.045, n=13, weak", "stocks intraday month headline PF 0.0 (n=28) vs recent post-hardening 7d/14d cohort near-breakeven-to-positive, n=11-16 (low sample)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "HEMI/USDT", "trigger": "fill on pullback into 0.006708-0.006862 (intraday B, waiting_for_entry); confirm OI stays up", "reason": "RS leader (score 88, RS/BTC +7.0%), fresh positioning (OI +5.48%, price up), swing leg already triggered — but no confirmed fresh catalyst, treat as technical/RS-driven only" },
    "best_short_candidate":    { "symbol": "ADA/USDT", "trigger": "already triggered swing short 0.186906-0.187594, invalidation 0.188434 — hold, do not add on a bounce above invalidation", "reason": "weak-vs-market on today's regime scan (bias short, RS/BTC -2.39%) AND catalyst-confirmed: Cardano has a 2-week deadline to avoid a governance freeze (4 committee seats expiring)" },
    "best_catalyst_candidate": { "symbol": "GE", "trigger": "continuation C-tier queued 368.01-369.22 for the cash open; confirm RTH volume + no gap-fade", "reason": "GEK800/F143 JASSM engine EMD contract win confirmed by GE Aerospace, Kratos, GlobeNewswire, FlightGlobal, Benzinga (multi-source, 2026-08-17) — existing A-tier already tp1_hit" },
    "avoid_candidate":         { "symbol": "EDEN/USDT", "reason": "score 100 top mover but >2 ATR from EMA20 — system already rejects it for chase risk; entering now would be buying an extended move with no fresh confirmation" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, derivatives_sparse | advisory_only |
| market_regime | caution | 0.55 | chop, risk_off, mixed | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.45 | oi_supports, data_unavailable | advisory_only |
| technical_entry | ok | 0.65 | entry_fresh, chase_risk, overextended | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-18_0439.md` (04:39 EEST, crypto overnight slot).

- **Confirmed winners**: GPS/USDT (flagged as best long-watch at 04:39) is now `tp1_hit`; ACE/USDT (flagged as a holding) is now `tp2_hit`. Both continuation theses played out.
- **HEMI/USDT persists** as a top long candidate across both reviews — was "cleanest entry-proximity" at 04:39, still `waiting_for_entry` now with OI confirming fresh positioning.
- **New this cycle**: POL/USDT joined HEMI as a second intraday `waiting_for_entry` RS-leader long (not present in the prior review's candidate list).
- **XMR/USDT** (prior short-watch) has dropped out of the current top-movers/derivatives scan — no fresh data to re-confirm the short thesis this cycle; **ADA/USDT** replaces it as the best short-watch, now catalyst-confirmed (governance-freeze risk) rather than purely technical.
- **GE** is a new addition this cycle — did not appear in the 04:39 crypto-only review (stocks were closed/not in scope for that slot).
- No signals were invalidated or contradicted since the last review.

## 5. Catalyst Coverage

- Total catalyst_events today: **1,444**; mapped to a symbol: **429** (29.7%); unmapped: **1,015** (70.3%).
- Narrative baskets: **4** — `rwa_narrative` (ONDO, XLM), `ai_narrative` (NEAR, RENDER, TAO, FET), `binance_ecosystem_teaser` (BNB), `momentum_breakout` (TUT, EDEN).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (generic PR/local-news noise, not trading-relevant): "Enginprime Medical Closes $12M Series A Financing"; "Greenberg Traurig's Marissa A. Neufeld Appointed to Miami Homes For All Board of Directors"; "Aastro Roofing Company Named Deerfield Beach's Roofer of the Year".
- Production news_supported coverage for stocks (per packet): only 5.0% in the live ~5h scan window vs 84.9% in a 24h shadow exact-match test — the production scan window is materially under-firing (known issue, see TODO-2).

## 6. Market Landscape

Crypto: BTC trend transition_up, ETH uptrend, altcoin breadth 52.5% above EMA20 / 60% above EMA50 — range/chop regime, recommended style "mean reversion or wait for clean breakouts." Macro overlay is heavily risk-off: Iran/Hormuz Strait vessel-attack headlines, US 30y yields at highest since 2007, macro risk score 100/100 (7 risk-off hits vs 1 risk-on). No A/B crypto ideas generated this cycle — everything strong (EDEN, ACE) is capped for chase risk or lack of fresh catalyst.

Stocks: cash session still closed (opens 13:30 UTC / 16:30 EEST — ~2h away). Regime label is `risk_off` with VIX at a calm 15.19, but the underlying SPY/QQQ/IWM/DIA 5d/20d return fields are all `NaN` — this label should be treated with reduced confidence until the index data feed is fixed (see TODO-1). HD and PANW report earnings today — both blocked from new operator consideration and flagged "do not chase into the print." 20 C-tier pre-open candidates are queued, topped by LRCX (98.1), CRCL (96.4), ASML (93.3), INTC (89.9) on the long side and UBER (85.2), BA (85.2), AXP (81.7), V (81.5) on the short side — none of these are actionable until RTH confirmation.

### Market Mood / Risk Routing
- Crypto mood: **chop** (range regime, risk-off macro overlay)
- Stocks mood: **pre-market / risk_off-labelled but data-suspect** (index NaNs undermine confidence in the label; VIX itself is calm)
- Dominant narrative: momentum_breakout basket (TUT, EDEN) fresh <1h, but both already rejected/capped for chase risk
- Preferred side now: **catalyst-backed** (GE long, ADA short) over pure momentum chasing
- Best long candidate: HEMI/USDT — RS leader, fresh OI positioning, `waiting_for_entry`
- Best short candidate: ADA/USDT — weak-vs-market + catalyst-confirmed governance-freeze risk, already triggered
- Best catalyst-backed candidate: GE — confirmed JASSM/GEK800 USAF contract, multi-source
- What to avoid: chasing EDEN/USDT (>2 ATR extended) or any pre-open stocks C-tier before RTH confirmation
- What would change the view: a clean RTH open on GE/stocks watchlist confirming direction; HEMI/POL entries filling cleanly without OI reversing; any de-escalation or escalation on the Hormuz/Iran headline flow

## 7. Candidate Deep Dives

**TradingView / manual chart check unavailable this run** — all technical reads below (ATR extension, EMA distance, entry zones) come only from the local report/OHLCV fields already captured in §6, not from any chart inspection.

### GE (long) — stocks, catalyst-backed
- **Catalyst**: Kratos Defense + GE Aerospace's GEK800 engine received US military type designation F143-ZZ-100 and an EMD contract award as the second-source propulsion system for the JASSM missile — announced 2026-08-17, confirmed via GE Aerospace, Kratos, GlobeNewswire, FlightGlobal, Defence Blog, Benzinga, StockTitan (6+ independent sources). This is a positive, defense-revenue-diversifying announcement.
- **Has price already reacted?** Yes — the existing A-tier GE long (entry 367.10-368.33) already hit TP1 earlier today, and a fresh C-tier continuation signal (368.01-369.22, invalidation 366.81) has queued for the open.
- **Chase risk / retest?** The new signal sits just above the prior entry zone — this reads as a continuation retest rather than a fresh chase, but confirm the entry zone holds after the open before treating it as clean.
- **Legal/headline risk check**: no indictment, SEC/DOJ investigation, class action, or delisting risk found for GE in internal news or the catalyst-events legal_risk basket. One separate GE headline (Nelson Peltz activist push for a full GE breakup) is a governance narrative, not a legal risk, and does not override the engine-contract catalyst.
- **Note on system tagging**: the production risk layer tagged this same GEK800 headline as `geopolitical_risk` with a `risk_warning` — that mislabels a clean, positive defense-contract win as a risk event (see TODO-3).
- **Verdict**: catalyst-confirmed, actionable-on-continuation after RTH confirmation. Not a chase; wait for the open to confirm the level holds.

### LRCX (long) — stocks, pre-open watchlist
- Highest-scoring C-tier long in the pre-open queue (98.1), entry 341.69-343.92, invalidation 339.47.
- Internal news check: only sector-adjacent chatter (Applied Materials earnings commentary, Monolithic Power Stifel upgrade, a quant-ratings piece mentioning LRCX among Coatue holdings) — no LRCX-specific catalyst found in the last 24h.
- **Is this chasing?** Cannot assess yet — market is closed, no fresh RTH price action to compare against the ATR-based entry zone.
- **Verdict**: watch-only until the cash open; require RTH confirmation (volume, sector alignment via SMH/XLK) before treating as more than a planning level. No legal/headline risk found.

### POL/USDT (long) — crypto, RS-leader, technical
- Intraday B-tier, `waiting_for_entry` 0.078264-0.078926, score 69.7; a swing leg (score 65.3) is already `triggered`.
- External catalyst check: Polygon's Ithaca upgrade went live 2026-08-05 (13 days old — not fresh) and Polygon Labs' pivot to payments (Coinme acquisition) is a background thesis, not a same-day catalyst. No internal news_items hit in the last 24h.
- **Verdict**: technical/RS-driven only, not catalyst-backed this cycle. Fine as a small-size RS-leader long if the entry zone fills cleanly; do not treat as a catalyst play.

### HEMI/USDT (long) — crypto, RS-leader, technical
- Intraday B-tier `waiting_for_entry` 0.006708-0.006862, score 66.1; RS score 88.0 in today's top movers (RS/BTC +7.03%); a swing leg (score 73.5) is already `triggered`. Derivatives: price up + OI up 5.48%, long/short ratio 1.214 — fresh positioning confirms the trend, not yet crowded.
- External catalyst check: a widely-repeated web summary claimed a "Binance Hemi Booster Event, Aug 22" — this could **not** be confirmed as a 2026 event; the underlying source data traces to a 2025 Binance HODLer Airdrop/listing, not a fresh 2026 catalyst. **Do not cite this as a live catalyst.**
- **Verdict**: cleanest technical entry-proximity read this cycle (consistent with the prior review), but treat as RS/momentum-driven only — the catalyst claim is unverified and should be dropped.

### ADA/USDT (short) — crypto, catalyst-confirmed
- Swing B-tier, already `triggered` short at 0.186906-0.187594, invalidation 0.188434 (score 65.3).
- Aligns with today's regime scan: ADA is in the "weakest symbols" bucket (bias short, RS/BTC -2.39%, weak_vs_market tag).
- Internal news confirms a real bearish catalyst: Cardano has a two-week deadline to avoid a governance freeze as 4 committee seats expire (CryptoSlate, 2026-08-17), alongside a longer-horizon Dijkstra upgrade roadmap piece (CryptoBriefing, same day) that is neutral-to-constructive but doesn't offset the near-term governance risk.
- **Verdict**: hold the existing short; catalyst and technicals agree. Do not add above the invalidation level (0.188434).

## 8. Best Candidates Ranked

1. **GE (long)** — best catalyst-backed candidate; confirmed defense-contract win, already validated (TP1 hit on the prior leg), continuation queued for the open.
2. **ADA/USDT (short, holding)** — best short candidate; catalyst-confirmed governance-freeze risk plus weak-vs-market technicals; already triggered, just manage the existing position.
3. **HEMI/USDT (long-watch)** — best pure technical/RS long; `waiting_for_entry`, fresh OI positioning, no catalyst — size accordingly.
4. **POL/USDT (long-watch)** — secondary RS long, `waiting_for_entry`; catalyst is stale (13-day-old upgrade), technical-only.
5. **LRCX (long-watch, pre-open)** — highest-scoring stocks C-tier queued for the open; needs RTH confirmation before it means anything.

## 9. Avoid / No Trade (this decision window only)

- **EDEN/USDT** — top mover (score 100, 24h +24.5%) but >2 ATR from EMA20; system already rejects new entries here for chase risk. Re-check only on a clean pullback/retest, not the current extension.
- **All 20 stocks C-tier `waiting_for_entry` names** (NET, CRWD, XOM, GE-C, CRCL, PYPL, ASML, INTC, MSTR, GS, UBER, ISRG, BA, BX, V, META, ARM, AXP, XLF) other than the GE/LRCX watch items above — planning levels only, do not treat as actionable until the 13:30 UTC open plus RTH confirmation.
- **HD, PANW** — earnings today; do-not-chase warning is explicit in the production risk layer regardless of any technical setup.
- This is a decision-window call only — scanning, tracking, and monitor activity continue unchanged; nothing here pauses the system.

## 10. Main Risks

- Macro risk-off overlay (Hormuz Strait vessel attack, US-Iran ceasefire-expiry risk, 30y yields at 2007 highs) can pressure alt longs broadly regardless of individual setup quality.
- Stocks regime label (`risk_off`) is built on `NaN` index return data today — treat the stocks-wide mood read with reduced confidence until confirmed at the open (see TODO-1).
- Catalyst mapping is weak (70.3% unmapped) — don't let a "no catalyst found" read be mistaken for "no catalyst exists."
- HD and PANW earnings today carry event risk for the broader tech/retail tape even outside those two names.
- Two crypto playbooks (intraday, scalp) remain structurally weak this week (PF 0.77 and 0.50 respectively) — avoid over-weighting fresh intraday/scalp signals without catalyst support.

## 11. Action Plan — next 4 hours

1. Watch POL/HEMI intraday entry zones for a clean fill; do not chase if price gaps through the zone.
2. Hold ADA/USDT short; watch for a Cardano governance-freeze headline resolution that could reduce the catalyst edge.
3. At/after the 13:30 UTC (16:30 EEST) US cash open: confirm GE continuation level holds, and require RTH confirmation on LRCX, CRCL, ASML, INTC before treating any as more than watchlist.
4. Do not add new intraday/scalp crypto exposure without a confirmed catalyst, given this week's weak playbook stats.
5. Re-check macro/Hormuz headline flow before the pre-US-open (16:20 EEST) review — an escalation would reinforce the risk-off tilt further.

## 12. Final Verdict per Mode

- **Crypto scalp**: avoid new entries — playbook PF 0.50, avgR -0.045 this week (low_confidence per strategy playbook doc). Manage existing positions only.
- **Crypto intraday**: caution / wait-for-catalyst — PF 0.77, avgR -0.175 this week, no A/B ideas this cycle; POL/HEMI are RS-technical watch-only until filled.
- **Crypto swing**: actionable-primary — PF 6.00, avgR +0.79 this week; hold/manage ADA short and the RS-leader long book (GPS, ACE already realizing partial wins).
- **Stocks intraday**: manual review / wait-for-RTH-confirmation — market closed, all 20 candidates are C-tier planning levels; do not treat as actionable pre-open. Month headline stat is weak (PF 0.0) but the recent post-hardening forward cohort is near-breakeven-to-positive on a small sample (n11-16) — watch, don't yet trust.
- **Stocks swing/invest (old)**: deprecated/removed — never actionable.
- **stocks_swing_growth_breakout (new)**: shadow-only research — 5 open candidates (V, XOM, JNJ, COP, LLY); not actionable, not sized.

## 13. Sources

- [GE Aerospace and Kratos Win U.S. Air Force Award to Design Engine for Expendable Collaborative Combat Aircraft](https://www.geaerospace.com/news/press-releases/ge-aerospace-and-kratos-win-us-air-force-award-design-engine-expendable) — GE Aerospace, 2026-02-23 (background/context on GEK-series program)
- [Kratos and GE Aerospace's GEK800 Engine Receives U.S. Military Type Designation F143-ZZ-100 and EMD Contract Award for JASSM](https://www.globenewswire.com/news-release/2026/08/17/3345950/224/en/kratos-and-ge-aerospace-s-gek800-engine-receives-u-s-military-type-designation-f143-zz-100-and-emd-contract-award-for-jassm.html) — GlobeNewswire, 2026-08-17
- [USAF designates GE-Kratos engine as F143 and awards initial production contract](https://www.flightglobal.com/archive/2026/08/usaf-designates-ge-kratos-engine-as-f143-and-awards-initial-production-contract/) — FlightGlobal, 2026-08-17
- [What's Going On With GE Aerospace Stock Monday?](https://www.benzinga.com/markets/large-cap/26/08/61246221/ge-aerospace-kratos-land-us-air-force-contract) — Benzinga, 2026-08-17
- [August 2026 Polygon News Update: Top Highlights](https://www.coingabbar.com/en/crypto-currency-news/polygon-news-update) — CoinGabbar (Ithaca upgrade, AggLayer v0.3 catalyst context, date unavailable for exact publish)
- HEMI Binance Booster Event claim — **could not verify for 2026**; underlying evidence traces to a 2025 Binance HODLer Airdrop/listing. Not cited as a live catalyst.
- Cardano governance-freeze risk and Dijkstra upgrade — internal `news_items` (CryptoSlate, CryptoBriefing), 2026-08-17, not independently re-verified externally this run (internal record was fresh and consistent, per §G discipline).

## 14. Fix Requests / TODO

### TODO-1
- **issue:** Stocks market-regime snapshot has `NaN` for SPY/QQQ/IWM/DIA `return_5d`/`return_20d`/`last_close`, yet still emits a confident `risk_off` label with `0/4 indices trending up` — the NaN data appears to be silently defaulting to a bearish read rather than surfacing as unknown.
- **evidence:** `data/processed/agent_outputs/20260818_041456_stocks_stocks_market_regime.json` — all four index entries show `"return_5d": NaN, "return_20d": NaN, "last_close": NaN"`; VIX itself is a calm 15.19, which is inconsistent with a confident risk_off framing.
- **suggested manual fix:** Investigate the index data ingest (likely a yfinance fetch/parse issue for SPY/QQQ/IWM/DIA in the pre-market run) and make the regime label degrade to "unknown/insufficient data" rather than a confident risk_off when the underlying index returns are NaN.
- **priority:** high
- **first observed:** 2026-08-18 11:39 EEST

### TODO-2
- **issue:** Catalyst mapping remains weak (70.3% of today's 1,444 events unmapped to a symbol), and production news_supported coverage for stocks is only 5.0% in the live ~5h scan window vs 84.9% in a 24h shadow exact-match test — consistent with the previously-flagged catalyst-linkage under-firing issue.
- **evidence:** `data/catalysts/2026-08-18/catalyst_events.jsonl` (429/1444 mapped); `llm_stocks_packet.md` catalyst-linkage advisory block.
- **suggested manual fix:** Revisit the deferred widening of `load_recent_news` scan window (previously flagged, sign-off pending) now that the shadow evidence (84.9%/91.9% at 24h/48h) continues to show the production window is materially undercounting.
- **priority:** medium
- **first observed:** 2026-08-18 11:39 EEST (recurring, first flagged in project memory `project_crypto_ai_desk_catalyst_linkage.md`)

### TODO-3
- **issue:** The production news-risk layer tagged the GE/Kratos GEK800 JASSM engine contract win (a positive, revenue-generating defense-contract announcement) as `geopolitical_risk` with a `risk_warning` — this is a classification mismatch; the headline is not a risk event for GE.
- **evidence:** `data/reports/intraday/2026-08-18_08-17_intraday_report.md` §5c: "GE [geopolitical_risk]: risk_warning — Kratos Defense & Security Solutions And GE Aerospace Announce That The GEK800 Engine Has Been Awarded A U.S. Air Force C..."
- **suggested manual fix:** Review the `geopolitical_risk` classifier's keyword/entity rules — defense-contract-win headlines naming "Air Force," "engine," "award" are being caught by a geopolitical-risk pattern that should distinguish contract wins from actual geopolitical/conflict risk.
- **priority:** low
- **first observed:** 2026-08-18 11:39 EEST

### TODO-4
- **issue:** Crypto scalp playbook continues to show a structurally weak edge this week (PF 0.50, avgR -0.045, n=13, weak confidence) — consistent with its documented `low_confidence` status (WR 12% / PF 0.14 / -6R at 14d) in the strategy playbook doc.
- **evidence:** `signal-stats --asset-class crypto` this run, mode=scalp row.
- **suggested manual fix:** No action needed beyond continued monitoring — this is already correctly weighted at 0.5x in `config/sizing_weights.yaml` and labeled low-confidence. Flagging only to confirm the pattern is holding, not worsening.
- **priority:** low
- **first observed:** 2026-08-18 11:39 EEST (recurring pattern, not new)
