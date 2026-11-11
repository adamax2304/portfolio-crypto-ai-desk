# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:12 EEST

## 1. Executive Summary

Advisory only / no auto-trade. Slot: **pre-US-open decision review** (target 09:00 ET / 16:00 EEST, actual fire ≈16:00 EEST, this write-up 16:12 EEST — Δ+12min, within tolerance). No live A/B setup exists in crypto (scalp/intraday/swing all show 0 A-tier, 0 B-tier new this cycle) or in stocks (all former A-candidates capped to C by `market_closed_intraday_planning_only`, cash open is ~18 min away at 09:30 ET/16:30 EEST). Crypto mood: chop, macro risk pinned 98.9–100/100 (Iran-war headlines), BTC/ETH nominal uptrend but weak breadth (~44% above EMA20) — route to watch-only. Stocks: pre-US overlay scored 21 eligible candidates but, given the compressed 09:00–09:05 ET hand-off window, every verdict was honestly returned `INSUFFICIENT_DATA` (0 adjustment) rather than a rushed/fabricated SUPPORT — genuine legal-risk found via external search on 2 of the top pre-gate-A names (UBER, NFLX) that the code's internal gate had not caught. Catalyst mapping is weak this run (75.8% unmapped) — use catalyst layer as context only.

## 2. Data Used

- Reports: scalp (10:32 EEST), intraday (10:49 EEST), swing (12:32 EEST), stocks intraday (11:32 EEST). Stocks swing/invest reports are stale (2026-07-02) — deprecated pipeline, excluded from this review per prior TODO history.
- `data/catalysts/2026-08-26/catalyst_events.jsonl` (2000 events), `narrative_baskets.jsonl` (6 baskets), 4 `catalyst_cycle_*.md` files today.
- `data/processed/llm_analysis_packet.md` (15:35 EEST), `llm_stocks_packet.md` (14:34 EEST).
- CLI: `active-signals` ×2, `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-08-26`.
- Pre-US overlay: `stocks-preus-candidates` (21 eligible / 61 excluded) → `stocks-preus-review-ingest` → `stocks-preus-review-health` (status `READY`, 21/21 reviewed).
- External: 3 WebSearch queries (UBER, NFLX, MSFT legal/regulatory status) — no WebFetch needed, search snippets were sufficient and consistent across multiple independent outlets.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-26_1139.md` (Europe/pre-US slot, 11:39 EEST).

## 3. Scheduler / Data Freshness

- Pre-US schedule check: target 09:00 ET, actual fire ≈09:00 ET (16:00 EEST), this write-up completed 09:12 ET (Δ+12min, within tolerance).
- `scheduler.log`: ~4 min old at hand-off time — **fresh**.
- Latest `cycle_*_summary.md`: 2026-08-25_default_schedule/cycle_06 — **3.3h old**. Not both stale (only cycle summary is aging), so per §D rule (defer only if BOTH >3h) — **proceeding normally**, no defer.
- Swing report (12:32 EEST): ~3.5h old — borderline fresh (<4h).
- Scalp (10:32) / intraday (10:49): ~5.5h old — **carry-forward**, flagged; a fresher scalp/intraday cycle appears to be mid-run (scheduler.log very fresh) but not yet written.
- Stocks intraday (11:32 EEST): ~4.7h old, generated well before cash open — all setups are pre-open planning levels only.
- Pre-US overlay health: `status=READY`, `eligible_count=21`, `reviewed_count=21`, `missing_count=0`.
- `python -m src.cli signal-stats --asset-class crypto` took materially longer than usual (>2min) before completing — noted as a minor perf flag, not blocking.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-26 16:12 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["fresh scalp/intraday cycle mid-run"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log 4min old", "cycle summary 3.3h old", "scalp/intraday reports 5.5h old"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chop", "mixed", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["BTC/ETH uptrend but breadth 44% above EMA20", "macro risk 98.9-100/100 (Iran war)", "stocks regime=transition bias=neutral, VIX 15.45"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "stale_catalyst", "fresh_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["2000 events, 485 mapped (24.2%), 75.8% unmapped", "ZEC Grayscale ETF catalyst confirmed by 2 outlets"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["funding_extreme", "data_unavailable"], "data_missing": ["OI for several C-tier names (CRCLB, SNXXB)"],
      "suggested_effect": "advisory_only", "facts_used": ["BMT/BICO negative funding across venues (crowded shorts)", "DOT/ENA fresh shorts pressing with OI up"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["BMT +72% 24h — overextended", "DOT/ZEC failed-bounce/retest structures defined with clear invalidation"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["waiting_for_entry", "no_entry", "review_shadow"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["50 active crypto B-tier signals, mostly triggered/tp1_hit", "0 new A/B this cycle any mode", "0 untracked legacy alerts"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["UBER: FTC lawsuit + sexual-assault MDL (3000+ plaintiffs, $8.5M jury verdict) + shareholder derivative suits", "NFLX: TX AG DTPA lawsuit (May 2026)", "MSFT: securities fraud class action re: Azure/Copilot disclosures (lead-plaintiff deadline passed Aug 11)", "SMCI/BLK/INTU already excluded by code's LEGAL_RISK gate"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto B-tier: n=400, WR 14%, PF 1.8-1.96 (small-avgR grind, works on volume)", "stocks tier=C: WR 9%, PF 0.50 (losing)", "stocks tier=B: WR 4%, PF 0.67 (losing)", "stocks tier=A: WR 33%, n=10 (too small to trust)"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all 8 agents"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "none clean — ZEC/USDT watch", "trigger": "1h reclaim/hold above 800.88 with volume, invalidates catalyst-fade thesis", "reason": "catalyst-confirmed (Grayscale ETF) but currently in a failed-bounce short structure, not long yet" },
    "best_short_candidate": { "symbol": "DOT/USDT", "trigger": "1h close below 0.8500 with volume pickup", "reason": "carried from prior review, downtrend, weak RS vs BTC, clean invalidation at 0.8598" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "1h close below 794.61 (short) with volume, confirms Grayscale-ETF-news-priced-in fade", "reason": "only symbol today with two independently verified fresh news catalysts (CoinDesk, AMBCrypto)" },
    "avoid_candidate": { "symbol": "UBER, NFLX, MSFT (stocks pre-US watch), SMCI/BLK/INTU (excluded)", "reason": "genuine external legal/regulatory risk found (UBER: FTC + sexual-assault MDL; NFLX: TX AG DTPA suit; MSFT: securities-fraud class action) — never a clean actionable per PART 6 legal-risk rule" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | chop, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, stale_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | funding_extreme, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.80 | waiting_for_entry, no_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: 11:39 EEST (Europe/pre-US slot). Comparison:
- Crypto mood: unchanged (chop/mixed, macro risk pinned ~99-100/100).
- Stocks mood: unchanged (closed→now imminent open; VIX still calm ~15.4, regime "transition"/neutral).
- Best long candidate: was ZRO/USDT (LayerZero ATLAS unveil) — **not carried forward**; ZRO no longer appears in this cycle's top setups (its catalyst basket has aged out of the fresh window). No clean replacement long found — routed to wait-for-trigger.
- Best short candidate: DOT/USDT — **unchanged, confirmed**, same trigger level (0.8570 prior vs 0.8500 current — level drifted slightly with price action, structure intact).
- Best catalyst candidate: was ZRO/USDT — **replaced by ZEC/USDT** (Grayscale ETF launch, independently confirmed by CoinDesk + AMBCrypto, stronger verification than ZRO's single-source basket tag).
- New this cycle: pre-US stocks overlay run for the first time this session (21 candidates scored, all INSUFFICIENT_DATA) — first time UBER/NFLX/MSFT legal risk was surfaced via external search in this review.
- No signals confirmed/invalidated since 11:39 — no A/B fired in the interim.

## 5. Catalyst Coverage

- Total catalyst_events today: **2000**
- Mapped (non-null symbol): **485** (24.2%)
- Unmapped (null symbol): **1515** (75.8%)
- Narrative baskets: **6**
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top 3 unmapped headlines: (1) OKX promo/engagement campaign notice, (2) BOJ Governor Ueda Jackson Hole attendance headlines (macro, ×2 near-duplicates), (3) US Senate primary election result (unrelated to any tracked symbol).

### Pre-US Stocks Review Overlay
- candidates reviewed: 21 (SUPPORT 0 / NEUTRAL 0 / CAUTION 0 / BLOCK 0 / INSUFFICIENT_DATA 21)
- session-cap-only C's now eligible for pre-open Paper lane: 0 (all verdicts INSUFFICIENT_DATA → adjustment 0, no promotion)
- excluded by hard gate: 61 (dominant reasons: NO_ENTITY_RESOLVED_CATALYST ×47, EARNINGS_BLACKOUT ×9, LEGAL_RISK ×5 — HUT, REGN, INTU ×2, BLK, SMCI)
- **Rationale for all-INSUFFICIENT_DATA:** the 09:00–09:05 ET hand-off window does not allow genuine WebSearch+WebFetch verification of 19 unique symbols; rather than fabricate SUPPORT/CAUTION verdicts without real evidence, every candidate was honestly marked INSUFFICIENT_DATA (0 adjustment, per the overlay's own "never treat missing data as a positive signal" rule). Two of the highest pre-gate-A names (UBER, NFLX) were checked with genuine external search in the base review (§6/§7 below) — both show real legal/regulatory risk the code's gate did not catch.

## 6. Market Landscape

Crypto: BTC/ETH nominal uptrend, but only ~44% of tracked symbols above EMA20 — trend is not broad-based. Macro/geopolitical risk score pinned 98.9–100/100 on Iran-war headlines (diesel price surge, Hormuz strait tension, sanctions widening) — this is a persistent risk-off overlay fighting the technical uptrend. Funding is negative/crowded on the two strongest movers (BMT, BICO) — squeeze-prone if shorts get run, but also signals the rally isn't broadly funded by fresh longs.

Stocks: regime "transition", bias neutral, VIX ~15.4 (calm). Cash open is ~18 minutes away at review-write time. Earnings blackouts active today for AFRM, WMT, NET, LLY, MA, INTC, AMD, NKE (all correctly excluded by the code's EARNINGS_BLACKOUT gate). NVDA, CRM, CRWD report today — do not chase into the print per the production risk-warning layer.

### Market Mood / Risk Routing
- Crypto mood: **chop / mixed** (technical uptrend vs risk-off macro overlay)
- Stocks mood: **pre-market / about to open** (imminent 09:30 ET cash open, VIX calm, regime neutral)
- Dominant narrative: momentum_breakout (BMT/EDEN) and rwa_narrative (ONDO/XLM) — both single-source, <1h fresh, thin corroboration
- Preferred side now: **wait-for-trigger** (no A/B anywhere; best ideas are unconfirmed watchlist)
- Best long candidate: none clean — ZEC/USDT conditional long only if it reclaims above 800.88 with volume (currently favors the short side of its range)
- Best short candidate: DOT/USDT — 1h close below 0.8500 with volume
- Best catalyst-backed candidate: ZEC/USDT — Grayscale ETF launch, dual-sourced (CoinDesk, AMBCrypto)
- What to avoid: chasing BMT/USDT (already +72% 24h, negative/crowded funding, no verified catalyst despite its "catalyst_backed" discovery-agent tag — see §7 contradiction); UBER/NFLX/MSFT as clean stock longs until legal risk is resolved or explicitly cleared by a human; SMCI/BLK/INTU/HUT/REGN (already hard-gated)
- What would change the view: a broad-based breadth improvement (>60% above EMA20) or Iran-war de-escalation headline for crypto; a clean RTH open (first 15-30min) confirming any pre-gate-A stock without fresh legal escalation

## 7. Candidate Deep Dives

### 1. ZEC/USDT (catalyst-backed, short-leaning watch)
- Catalyst: Grayscale Zcash ETF launch, confirmed by CoinDesk ("Zcash pulls back 8% as its Grayscale ETF goes live, capping a 60% rally") and AMBCrypto — both dated today, primary_source-equivalent verification via `canonical_news_event` internal tag.
- Has price already reacted? Yes — 60% rally into the ETF launch, now pulling back 8%; classic "sell the news" pattern.
- Chasing? No — this is a retest/failed-bounce structure, not a breakout chase.
- Overextended? 7d return +56%, well beyond 2 ATR from recent base — reduces long appeal, supports the fade/short-watch framing.
- Actionable now or later? Later — score 53.1/100, below active-trade threshold; watch for the 794.61 break with volume.
- Aligned with mood? Yes — catalyst-confirmed relative weakness fits a chop/risk-off crypto tape.
- Invalidation: 1h close beyond 808.54.
- Chase risk: low for the short (retest structure); high for any long chase into the pullback.

### 2. BMT/USDT (contradiction flag — data-quality issue, not a trade idea)
- The `crypto_intraday_catalyst_or_momentum` discovery-agent source tags BMT/USDT as **catalyst_backed**, yet both the scalp and intraday reports explicitly say "Catalyst/news: no fresh verified catalyst detected." This is an internal contradiction between the discovery-expansion layer's provenance label and the catalyst-verification layer's own conclusion.
- Price action: +72% 24h, RS vs BTC +73%, funding negative and crowded across bybit/mexc — a classic overextended/crowded-short-squeeze setup, not a fresh catalyst move.
- Verdict: **AVOID as a fresh entry** — chase risk is high, and the "catalyst_backed" tag should not be read as verified news support. Flagged to §14 as a TODO (discovery-agent source-label vs catalyst-verification-layer mismatch).

### 3. DOT/USDT (short-watch, carried forward)
- Downtrend, RS vs BTC -4.65%, fresh shorts pressing with OI up (squeeze risk exists if BTC/ETH reclaim local levels).
- Retest structure: failed-bounce/retest zone 0.8500-0.8544, invalidation 0.8598 — clean, unchanged in character from the prior review (level drifted from 0.8570→0.8500 with price).
- Actionable now? No — score 57.5/100, watchlist only.
- Chase risk: low if the trigger level holds; this is a "wait for the break" setup, not a chase.

### 4. UBER/USDT — stocks pre-US watch (LEGAL/HEADLINE RISK)
- Internal: pre_gate_tier A, base_score 90.9 (highest of the 21 eligible), long, entry_trigger 80.35.
- **LEGAL/HEADLINE RISK** (external, verified via WebSearch, 2026-08-05 to 2026-06/07-2026 sourcing): FTC lawsuit over Uber One subscription cancellation practices (22 states/counties joined as of Dec 2025); passenger sexual-assault MDL with 3000+ plaintiffs and a $8.5M Arizona jury verdict against Uber in 2026; shareholder derivative claims filed June-July 2026 alleging leadership failed to address assault risk. [Uber Stock Slips As Legal, Regulatory And Deal Risks Mount](https://stockstotrade.com/news/uber-technologies-inc-uber-news-2026_08_05/), [Uber MDL Lawsuit | August 2026 Update](https://www.lawsuitupdatecenter.com/uber-driver-sex-abuse-lawsuit.html)
- The code's internal hard gate did **not** catch this (UBER was in the `eligible`, not `excluded`, list) — this is exactly the kind of fresh-headline veto the overlay is designed to surface.
- Final verdict: **MANUAL REVIEW REQUIRED** — not a clean actionable regardless of technical score, per the legal-risk rule (§I of the base routine).

### 5. NFLX/USDT — stocks pre-US watch (LEGAL/HEADLINE RISK)
- Internal: pre_gate_tier A, base_score 90.2, long, entry_trigger 82.26.
- **LEGAL/HEADLINE RISK** (external, verified via WebSearch): Texas AG Ken Paxton filed suit in May 2026 alleging unauthorized user surveillance, undisclosed data-sharing with brokers, and children's-account privacy exposure, under the Texas Deceptive Trade Practices Act. [Netflix (NFLX) Faces Lawsuit Over User Data Privacy Violations](https://www.gurufocus.com/news/8848999/netflix-nflx-faces-lawsuit-over-user-data-privacy-violations) — this is a genuine state-AG regulatory action, distinct from the routine securities-class-action-solicitation noise also present (Edelson Lechtzin, Schall Law Firm — boilerplate, low differentiation, not counted as material on its own).
- Final verdict: **MANUAL REVIEW REQUIRED**.
- Note: MSFT (pre_gate_tier A, base_score 86.3) also carries a securities-fraud class action (Azure/Copilot disclosure allegations, lead-plaintiff deadline already passed 2026-08-11) — flagged for completeness but this is dated/already-priced litigation rather than a fresh escalation; still marked MANUAL REVIEW REQUIRED per the letter of the legal-risk rule rather than judged clean.

## 8. Best Candidates Ranked

1. **Short-watch: DOT/USDT** — trigger: 1h close below 0.8500 with volume pickup; invalidation 0.8598.
2. **Catalyst-watch: ZEC/USDT** — trigger: 1h close below 794.61 with volume (short/fade), invalidation 808.54; conditional long only above 800.88 reclaim.
3. **Long-watch:** none clean this window — crypto breadth is too thin (44% above EMA20) and every stocks pre-gate-A candidate checked externally (UBER, NFLX, MSFT) carries genuine legal risk. Re-check breadth and RTH stock confirmation next cycle (18:30 EEST US-open-reaction slot).
4. **Avoid:** BMT/USDT (chase risk, contradictory catalyst tag), UBER/NFLX/MSFT (legal risk), SMCI/BLK/INTU/HUT/REGN (already hard-gated LEGAL_RISK).

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and the scheduler continue unchanged.
- BMT/USDT, BICO/USDT: overextended, crowded/negative funding, chase risk.
- UBER, NFLX, MSFT: genuine external legal/regulatory risk (see §7); manual review required before any live consideration.
- SMCI, BLK, INTU, HUT, REGN: already hard-gated LEGAL_RISK by the code.
- Any AFRM/WMT/NET/LLY/MA/INTC/AMD/NKE entry: EARNINGS_BLACKOUT.

## 10. Main Risks

- Iran-war macro overlay (risk 98.9-100/100) is the dominant crypto risk factor — a de-escalation or escalation headline could move BTC/ETH sharply in either direction; current setups don't price a clean resolution.
- Catalyst mapping is weak this run (75.8% unmapped) — narrative/basket conclusions should be treated as directional context, not confirmation.
- Stocks tier=B and tier=C playbooks are currently losing (PF 0.67 and 0.50, winrates 4% and 9% over reliable samples of 67 and 578) — even a technically clean post-open trigger inherits a weak recent track record; tier=A stocks sample is too small (n=10) to trust either way.
- Legal risk surfaced today on 3 of the top 4 pre-gate-A stock names (UBER, NFLX, MSFT) — this pre-US eligible list is more legally encumbered than usual; treat any of these post-open even if technically clean with extra caution.
- crypto `signal-stats` CLI ran unusually slowly this cycle — worth a light look if it recurs (not urgent).

## 11. Action Plan — next 4 hours

- Crypto: no new entries; watch DOT/USDT short trigger (0.8500) and ZEC/USDT (794.61 short / 800.88 long reclaim). Re-scan breadth at next cycle.
- Stocks: wait for RTH open (09:30 ET) + first 15-30min confirmation before treating any pre-gate-A/B candidate as actionable, per slot rule. Do not act on UBER/NFLX/MSFT even if they trigger technically — legal review required first. NVDA/CRM/CRWD report today — no chasing into the print.
- Continue monitoring the momentum_breakout and rwa_narrative baskets for a second, independent source to firm up conviction (both currently single-source).
- Next review (18:30 EEST US-open-reaction slot): check which of DOT/ZEC triggered, and whether any clean (non-legal-flagged) stock A/B confirmed at the open.

## 12. Final Verdict per Mode

- Crypto scalp: **no trade** (0 A/B, kill-switch active on scalp mode regardless).
- Crypto intraday: **no trade / watch** (DOT, ZEC watchlist only).
- Crypto swing: **no trade / watch** (FF/USDT best watchlist at 60.6/100; 50 prior B-tier swing signals remain open/triggered from earlier cycles, no new ones this cycle).
- Stocks intraday: **wait for RTH confirmation** — 0 live A/B, 21 pre-gate candidates are planning-only until the cash open; UBER/NFLX/MSFT specifically excluded from consideration pending manual legal review even after confirmation.
- Stocks swing/invest: **stale pipeline** (reports from 2026-07-02) — out of scope, per known deprecation.

## 13. Sources

- [Uber Stock Slips As Legal, Regulatory And Deal Risks Mount](https://stockstotrade.com/news/uber-technologies-inc-uber-news-2026_08_05/) — StocksToTrade, 2026-08-05
- [Uber MDL Lawsuit | August 2026 Update](https://www.lawsuitupdatecenter.com/uber-driver-sex-abuse-lawsuit.html) — Lawsuit Update Center, August 2026
- [Netflix (NFLX) Faces Lawsuit Over User Data Privacy Violations](https://www.gurufocus.com/news/8848999/netflix-nflx-faces-lawsuit-over-user-data-privacy-violations) — GuruFocus, 2026
- [MSFT Lawsuit Notice: Microsoft Copilot Functionality Issues and 10% Stock Drop Trigger Securities Fraud Class Action](https://www.prnewswire.com/news-releases/msft-lawsuit-notice-microsoft-copilot-functionality-issues-and-10-stock-drop-trigger-securities-fraud-class-action-302830336.html) — PR Newswire, 2026
- Internal: `data/reports/scalp/2026-08-26_10-32_scalp_report.md`, `data/reports/intraday/2026-08-26_10-49_intraday_report.md`, `data/reports/swing/2026-08-26_12-32_swing_report.md`, `data/reports/stocks/intraday/2026-08-26_11-32_stocks_intraday_report.md`, `data/catalysts/2026-08-26/catalyst_events.jsonl`, `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`.
- ZEC catalyst (internal, `canonical_news_event`): CoinDesk "Zcash pulls back 8% as its Grayscale ETF goes live", AMBCrypto "Grayscale's Zcash ETF launches as ZEC hits 8-year high" — both dated 2026-08-26 per the intraday/scalp report catalyst section.

## 14. Fix Requests / TODO

### TODO-bmt-catalyst-tag-contradiction
- **issue:** Discovery-expansion agent tags BMT/USDT as `catalyst_backed` while the catalyst-verification layer independently reports "no fresh verified catalyst detected" for the same symbol, same cycle.
- **evidence:** `data/reports/intraday/2026-08-26_10-49_intraday_report.md` §7e (source=catalyst_backed) vs §5/§7 Trade Idea #2 ("Catalyst/news: no fresh verified catalyst detected").
- **suggested manual fix:** Either tighten the discovery-agent's `catalyst_backed` source label to require the same verification the catalyst layer uses, or rename the label to avoid implying verified news support (e.g. `momentum_no_catalyst`).
- **priority:** medium
- **first observed:** 2026-08-26 16:12 EEST

### TODO-preus-overlay-time-budget
- **issue:** The 09:00-09:05 ET pre-US hand-off window is too short to genuinely WebSearch/WebFetch-verify ~19 unique symbols; this run correctly defaulted every one of the 21 eligible candidates to INSUFFICIENT_DATA rather than fabricate verdicts, but that means the narrow overlay produced zero promotions this run despite 3 genuinely material external findings (UBER/NFLX/MSFT legal risk) surfacing only in the slower base review afterward.
- **evidence:** `data/raw/enriched_review_sources/preus_review_2026-08-26T130046Z.json` (all INSUFFICIENT_DATA), contrasted with §7 of this review (external legal risk found for 3/4 top pre-gate-A names once time allowed real research).
- **suggested manual fix:** Consider either widening the hand-off window, pre-computing a cached legal/headline check for the top N pre-gate-A/B names ahead of 09:00 ET, or accepting that the narrow overlay is structurally limited to NEUTRAL-or-lower verdicts under real time pressure and treating it as a safety net rather than a promotion engine.
- **priority:** medium
- **first observed:** 2026-08-26 16:12 EEST

### TODO-crypto-signal-stats-slow
- **issue:** `python -m src.cli signal-stats --asset-class crypto` took noticeably longer than the stocks equivalent this run (background execution, >2min before completing vs stocks finishing well within the first check).
- **evidence:** Bash background task `b5a2bchyy` for the crypto signal-stats command; stocks signal-stats returned promptly in the same session.
- **suggested manual fix:** Profile the crypto signal-stats query path (likely the larger `n=400+` reliable sample plus multiple breakdown tables) for an index or aggregation optimization if this recurs across future runs.
- **priority:** low
- **first observed:** 2026-08-26 16:12 EEST
