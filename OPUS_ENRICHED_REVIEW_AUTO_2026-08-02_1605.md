# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:05 EEST

## 1. Executive Summary

Pre-US-open decision review. **Advisory only / no auto-trade.** Today (2026-08-02) is a **Sunday** — US cash markets are closed all day and the next open is **Monday 2026-08-03 ~09:30 ET (~24.5h away)**, not the ~10-minute pre-open window this slot is normally built for. Stocks are pure planning/carry-forward context (last stocks-intraday report Friday 2026-07-31 20:00 EEST, stocks-swing/invest report 2026-07-02 under the deprecated framework — both expected given the weekend closure, not a freshness fault). Crypto is the only live actionable class this window.

Crypto regime is **range/chop with BTC and ETH both in downtrend**, macro risk score 89.9/100 (risk-off headwind), and a spreading **BTC Coldcard hardware-wallet exploit** (~$89M / 4,585 addresses, attacker still holds the funds) is the dominant fresh risk narrative. Scalp and intraday scans again show **zero A-tier setups** this cycle (scalp structurally negative, 14d PF 0.14). The **COTI/USDT held swing long remains direction-contradicted and price-through-invalidation for a 4th consecutive review cycle** (23:26 Aug-1 → 04:30 → 11:30 → this 16:05 cycle) — escalated further in §14. On the stocks side, **UnitedHealth (UNH)** carries a verified, escalating DOJ antitrust probe (externally confirmed, dated 2026-07-16) relevant to the next actionable stocks session. No stocks pre-US overlay candidates were eligible this cycle (0 eligible / 0 excluded — market fully closed, no fresh intraday cycle to seed candidates). Scanning, tracking, and monitors continue regardless of mood; this review recommends selective caution and one escalated manual-review flag, not a pause.

## 2. Data Used

- Reports (crypto):
  - Scalp: `2026-08-02_12-04_scalp_report.md` (generated 15:04 EEST, ~1h old) — 0 A-tier.
  - Intraday: `2026-08-02_12-11_intraday_report.md` (generated 15:11 EEST, ~1h old) — 0 A-tier.
  - Swing: `2026-08-02_02-14_swing_report.md` (generated 05:14 EEST, ~10.75h old — **carry-forward**, within the 4–12h window, flagged).
- Stocks (weekend, planning-context only, all stale, excluded from actionable verdict):
  - Intraday last generated 2026-07-31 20:00 EEST (market closed since Friday).
  - Swing/invest last generated 2026-07-02 (deprecated old-stocks-swing framework, expected).
- Catalysts: `data/catalysts/2026-08-02/catalyst_cycle_12-13.md` (generated 15:13 EEST, fresh), `catalyst_events.jsonl` (1,991 cumulative events today, recomputed directly), `narrative_baskets.jsonl` (4 baskets).
- LLM packet: `data/processed/llm_analysis_packet.md` (mtime 15:11 EEST, fresh; Weekend Mode confirmed active). Stocks packet `llm_stocks_packet.md` last generated Fri 2026-07-31 22:55 (stale, weekend-expected).
- CLI (read-only, §A.4 whitelist): `active-signals --asset-class crypto` (24 rows), `active-signals --asset-class stocks` (50 rows, planning-context), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-08-02` (clean, 0 findings).
- Stocks pre-US overlay (new whitelisted commands, §STOCKS PRE-US REVIEW OVERLAY): `stocks-preus-candidates` → `reports/STOCKS_PREUS_REVIEW_CANDIDATES.md`, **0 eligible / 0 excluded** (market fully closed Sunday, no fresh stocks-intraday cycle this weekend to seed candidates). No ingest run — nothing to score.
- DB (`db/crypto_ai_desk.sqlite`, read-only): `news_items` 24h-freshness checks for COTI, HOME, EPIC, BANK, UNH, BTC — only BTC had fresh (<24h) internal rows (5, all Coldcard-exploit-related); COTI/HOME/EPIC/BANK/UNH had 0 fresh internal rows, triggering external research per §G.
- External research (triggered — internal records missing/stale for COTI, HOME, UNH): 3 WebSearch queries + 2 WebFetch verifications (see §13).
- Scheduler: `data/scheduled_runs/2026-08-01_default_schedule/scheduler.log` (mtime 15:30 EEST) + `cycle_08_14-57_summary.md` (started 14:57, finished 15:30).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-02_1130.md` (Europe / pre-US context, 11:30 EEST) — see §4.

## 3. Scheduler / Data Freshness

- **Pre-US schedule check:** target 08:55 ET, actual fire 08:59 ET (Δ+4min, within tolerance). DST window per the task note (2026-03-08→03-29, 2026-10-25→11-01) does not apply today; the fixed 15:55 Nicosia cron correctly maps to 08:55 ET in the current steady-state offset.
- **Slot-timing note (not a drift issue, a calendar fact):** today is Sunday; the "10 minutes before US cash open" framing this slot is designed for does not literally apply — the actual next US cash open is Monday 2026-08-03 ~09:30 ET, ~24.5h from this review. Continuing the review normally per routine instructions; stocks treated as closed/planning-only per the ALWAYS-SCAN / slot-awareness rules for non-trading days.
- `scheduler.log` last write 15:30 EEST, ~35min before this review — well under the 3h defer threshold. `cycle_08_14-57_summary.md` (last completed cycle) finished 15:30 — also under threshold. **Not deferred.**
- Untracked-alert detector: clean (0 findings) — no PART-1-style integrity regression this cycle.
- Catalyst mapping coverage recomputed directly from `catalyst_events.jsonl`: **53.4% unmapped (1,064/1,991)** — still weak (>50%), marginal improvement vs the 11:30 review's 56.9%. Treat catalyst layer as context, not final decision (see §5).
- Swing report is 10.75h old (carry-forward window, not stale) — used with that caveat; scalp/intraday are fresh (~1h).
- **Confirmed carry-forward finding:** COTI/USDT's held swing long (`sig_06b6c2801005f29d`, invalidation 0.015355) remains status=`triggered` (open) in `active-signals`, while both the 05:14 swing snapshot (failed-bounce zone 0.0147–0.0150) and the 15:11 intraday snapshot (failed-bounce zone 0.0135–0.0137) place COTI's price well below that invalidation level. This is now the **4th consecutive review** (23:26 Aug-1 → 04:30 → 11:30 → this cycle) to observe the same unresolved condition — see §14, priority escalated further.
- Stocks pre-US overlay ran cleanly: `stocks-preus-candidates` returned 0 eligible / 0 excluded (expected — no fresh stocks-intraday cycle ran over the weekend to seed candidates); `stocks-preus-review-ingest` was not run (nothing to ingest).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-08-02 16:05 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["swing report is 10.75h old (carry-forward, not stale)", "HOME/USDT current absolute price not directly stated in today's reports (only 24h %)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 15:30", "cycle_08_14-57_summary.md completed 15:30", "active-signals crypto 24 rows / stocks 50 rows", "stocks-preus-candidates: 0 eligible / 0 excluded"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["risk_off", "chop", "mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["intraday report §1: BTC downtrend, ETH downtrend, altcoin breadth 51.3% above EMA20", "macro risk 89.9/100 risk-off (9 risk-off hits, 1 risk-on, 2 calendar hits)", "BTC Coldcard exploit spreading, $89M / 4,585 addresses, attacker still holds funds"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "narrative_supported", "no_catalyst"],
      "data_missing": ["true symbol resolution for 1,064/1,991 unmapped catalyst_events rows today"],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl recomputed: 1,991 total / 927 mapped / 1,064 unmapped (53.4%)", "4 narrative baskets: perps_dex_narrative (HYPE primary, <1h fresh), binance_ecosystem_teaser (BNB primary, <1h fresh), rwa_narrative (ONDO/XLM, freshness unknown), ai_narrative (NEAR/RENDER/TAO/FET, freshness unknown)", "COTI/HOME/EPIC: 0 fresh (24h) internal news_items rows — pure technical/RS theses"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["Bybit/OKX cross-check unavailable for most of today's strongest symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOME/UAI/HYPER: price up + OI up, fresh positioning, crowding normal-to-elevated (UAI long/short 0.621, elevated long crowding)", "BANK/USDT: price down + OI up (7.27%), funding -0.00042, fresh shorts pressing, squeeze risk if price reclaims", "COTI/USDT: price down + OI down, funding -0.00019, deleveraging/long-liquidation pattern, crowding normal"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "overextended", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HOME/UAI/SHOT/HYPER rejected in scalp/intraday for chase risk (>2 ATR from EMA20)", "EPIC/USDT intraday B-tier signal (sig_c6ee879922b6a34b) still waiting_for_entry: entry zone 0.880285-0.903419, invalidation 0.852011 — genuine near-trigger watch, not yet filled since at least the 11:30 review", "COTI/USDT failed-bounce short zone moved from 0.0147-0.0150 (05:14 swing) to 0.0135-0.0137 (15:11 intraday) — the decline is continuing, not stabilizing"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "needs_review",
      "confidence": 0.62,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": ["no fresh PAPER_MONITOR_STATUS_LATEST.md-equivalent snapshot read this cycle (not in the §A.4 whitelist); counts sourced directly from active-signals"],
      "suggested_effect": "advisory_only",
      "facts_used": ["active-signals crypto (24 total): 1 WAITING FOR ENTRY (EPIC/USDT intraday), 5 open swing/intraday positions from recent cycles (EPIC swing TRIGGERED, HOME swing TRIGGERED, AEVO swing TRIGGERED, XRP swing TP1_HIT-partial, COTI swing TRIGGERED), remainder are older CLOSED-IN-SUBSTANCE tp1/tp2_hit signals from mid-July with expires_at already in the past", "COTI/USDT (sig_06b6c2801005f29d) status=TRIGGERED (open) but price sits below its own invalidation across two consecutive snapshots — NEEDS REVIEW, not a clean OPEN actionable"]
    },
    {
      "agent": "risk_manager",
      "verdict": "manual_review",
      "confidence": 0.7,
      "reason_codes": ["headline_risk", "manual_review", "correlation_cluster", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/USDT held long, price through its own invalidation for a 4th consecutive review — the clearest position-integrity item on the desk", "BTC exploit_hack risk (Coldcard, $89M, 4,585 addresses) still active desk-wide, block_requires_operator_review flagged in production risk layer", "EPIC/HOME/AEVO longs remain a correlated no-catalyst RS-momentum cluster — a BTC/ETH downdraft would likely hit all three together", "UNH DOJ antitrust probe into Claritev confirmed escalating as of 2026-07-16 (external, verified) — legal/headline risk carried into the next actionable stocks session"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto signal-stats: tier=B PF 2.46, avgR 0.44, winrate 25% (n=102)", "by mode: intraday PF 4.71/avgR 1.30 (n=39, strong); swing PF 2.07/avgR 0.29 (n=42); scalp PF 0.10/avgR -0.26 (n=21, structurally negative, matches 0 A-tier scalp again this cycle)", "weekend=Y cohort: PF 4.05 but winrate only 21% (n=17) — small sample, treat cautiously", "stocks signal-stats: tier=C triggered winrate 7%, PF 0.55 — reliable but weak (n=197); direction=short PF 0.17 (n=124, weak) vs direction=long PF 0.83 (n=79)"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "EPIC/USDT", "trigger": "Intraday B-tier signal, still WAITING FOR ENTRY, entry zone 0.880285-0.903419, invalidation 0.852011 — let the fill come to the zone with volume confirmation; do not chase the parallel already-open swing long, which is extended." },
    "best_short_candidate":    { "symbol": "BANK/USDT", "trigger": "Confirm bearish HTF structure + 1h close beyond failed-bounce retest zone 0.0480-0.0488 with a stop above 0.0497; funding is already negative and OI is rising (fresh shorts pressing) so a reclaim could squeeze — do not enter without confirmation." },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "perps_dex_narrative basket (fresh <1h, primary), playbook wait_pullback — no defined entry zone in today's deep-analysis output (not in the top-N deep-dive set this cycle); treat as catalyst-watch only until a concrete technical zone is published." },
    "avoid_candidate":         { "symbol": "COTI/USDT", "reason": "Held long, direction-contradicted and price apparently through its own invalidation level for a 4th consecutive review; do not add; flag for immediate manual position review." },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.68 | risk_off, chop, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, narrative_supported, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, overextended, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.62 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | manual_review | 0.70 | headline_risk, manual_review, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.68 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-02_1130.md` (Europe / pre-US context, 11:30 EEST, ~4.5h before this one).

- **New:** COTI/USDT's failed-bounce short zone moved from 0.0147-0.0150 (05:14 swing snapshot) to 0.0135-0.0137 (15:11 intraday snapshot) — the decline against the held long's invalidation (0.015355) is continuing, not stabilizing. This is the 4th consecutive review to flag this position; escalated further in §14.
- **New:** Macro risk score eased slightly from 100.0/100 (11:30) to 89.9/100 (this cycle) — still firmly risk-off, marginal improvement.
- **New:** Catalyst mapping improved marginally: 56.9% unmapped (11:30) → 53.4% unmapped (this cycle) — still weak (>50%), same recurring gap.
- **New:** UNH DOJ/legal risk externally verified and found to be escalating (new civil investigative demands re: Claritev, dated 2026-07-16) — added to this review's candidate set; was not covered in the 11:30 review.
- **Unchanged / carried forward:** EPIC/USDT, HOME/USDT, AEVO/USDT swing longs remain OPEN, still RS-leaders, still no fresh catalyst. XRP/USDT short remains OPEN (partial TP booked). EPIC/USDT intraday signal remains WAITING FOR ENTRY (entry zone unchanged: 0.880285-0.903419).
- **Removed:** ADA/USDT's momentum_breakout catalyst-backed tag from the 11:30 review is no longer present in this cycle's narrative baskets (basket composition rotated to perps_dex_narrative / binance_ecosystem_teaser / rwa_narrative / ai_narrative — 4 baskets vs 5 at 11:30). SYN/USDT (11:30's best short-watch) is also no longer among today's top movers; replaced by BANK/USDT as this cycle's cleanest short-watch.
- **Confirmed:** No fresh A-tier crypto or stocks setups this cycle either — same structural gap as the last several cycles.

## 5. Catalyst Coverage

- Total `catalyst_events` today (`data/catalysts/2026-08-02/catalyst_events.jsonl`, recomputed directly): **1,991**
- Mapped (non-null symbol): **927** (46.6%)
- Unmapped (null symbol): **1,064** (53.4%)
- `narrative_baskets`: **4** (perps_dex_narrative/HYPE+DYDX+GMX+ASTER, binance_ecosystem_teaser/BNB+ASTER, rwa_narrative/ONDO+XLM, ai_narrative/NEAR+RENDER+TAO+FET+WLD+ASTER)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top unmapped headlines (sample): "IRAN THREATENS REGIONAL ENERGY STRIKES..." (t.me/WalterBloomberg, geopolitical, structurally symbol-less) / "#ByBit News: Complete Your First Trade and Earn 40 OPG" (t.me/CexAlerts, promo noise) / IAEA Zaporizhzhya nuclear-plant power-outage wires (geopolitical, no symbol by design). As in prior cycles, a meaningful share of unmapped volume is inherently symbol-less macro/geopolitical wire content rather than a pure resolver bug.

### Pre-US Stocks Review Overlay

- candidates reviewed: 0 (SUPPORT 0 / NEUTRAL 0 / CAUTION 0 / BLOCK 0 / INSUFFICIENT_DATA 0)
- session-cap-only C's now eligible for pre-open Paper lane: 0
- excluded by hard gate: 0 — `stocks-preus-candidates` returned 0 eligible and 0 excluded this cycle; no fresh stocks-intraday cycle ran over the weekend to seed any candidates. No JSON built, no ingest run.

## 6. Market Landscape

BTC and ETH both in downtrend, altcoin breadth 51.3% above EMA20 (modest, not broad participation). Macro/geopolitical risk score 89.9/100 (risk-off headwind) — 9 risk-off hits vs 1 risk-on hit this cycle. The dominant fresh narrative is the spreading **BTC Coldcard hardware-wallet exploit** (~$89M across 4,585 addresses, attacker still holds the stolen BTC, CZ has publicly warned holders) — flagged `block_requires_operator_review` desk-wide. A narrow cluster of no-catalyst alts (HOME, UAI, SHOT, HYPER, KAITO) continues showing strong RS/momentum inside the chop — the same known-negative playbook pattern as prior cycles (no-catalyst intraday chop: 14d WR 23%/PF 0.70), so still low-quality breadth rather than confirmation of a broad risk-on turn. Weekend Mode is confirmed active (A-tier score penalty -5.0, confidence step-down, overextension penalty 1.25x, retest required after impulse).

### Market Mood / Risk Routing

- Crypto mood:           risk-off / chop, BTC+ETH both downtrend, elevated exploit-hack risk overlay
- Stocks mood:           closed (Sunday; last actionable data Friday 2026-07-31, planning-context only; next open Monday ~09:30 ET; UNH DOJ escalation is the key carry-forward watch item)
- Dominant narrative:    Momentum-without-catalyst rotation (HOME/UAI/SHOT/HYPER/KAITO) inside a still-risk-off tape, overlaid by the spreading BTC Coldcard exploit
- Preferred side now:    mixed — hold existing RS-leader longs (EPIC/HOME/AEVO), do not chase new longs into the extension; watch BANK/USDT for a confirmed failed-bounce short; watch HYPE/USDT for the perps-DEX catalyst basket to produce a concrete entry zone
- Best long candidate:   EPIC/USDT (intraday B-tier, still WAITING FOR ENTRY, entry zone 0.880285-0.903419, invalidation 0.852011 — genuine near-trigger watch, not a chase)
- Best short candidate:  BANK/USDT (failed-bounce retest zone 0.0480-0.0488, invalidation 0.0497 — fresh shorts pressing but funding/OI mix means a reclaim could squeeze; needs confirmation)
- Best catalyst-backed candidate: HYPE/USDT (perps_dex_narrative basket, fresh <1h, but no concrete technical zone published today — catalyst-watch, not yet actionable)
- What to avoid:         COTI/USDT (held long, price apparently through its own invalidation for a 4th consecutive review — flag for immediate manual review, do not add); fresh longs on HOME/UAI/SHOT/HYPER at current price (>2 ATR from EMA20, explicit chase-risk flags); fresh shorts on BANK without confirmation (squeeze-prone, fresh shorts already pressing)
- What would change the view: A confirmed slowdown/resolution of the BTC Coldcard exploit, or BTC/ETH reclaiming trend structure, would lift the risk-off cap; a clean failed-bounce + bearish HTF break on BANK would activate the short-watch; a fill into EPIC's 0.880-0.903 zone with volume would activate the long-watch; a published technical zone on HYPE while the perps-DEX basket stays fresh would activate the catalyst-watch; Monday's US cash open (~09:30 ET) is the next hard trigger for the stocks side.

## 7. Candidate Deep Dives

### COTI/USDT (long, OPEN swing position — **escalated further: 4th consecutive review, price through invalidation**)

- Has price already reacted? Yes — the position's short-side watchlist framing has moved from a 0.0147-0.0150 failed-bounce zone (05:14 swing snapshot) to a 0.0135-0.0137 zone (15:11 intraday snapshot) — the decline is continuing, both readings sit below the held long's stated invalidation (0.015355).
- Is this a chase-risk setup? N/A — position already held; the live question is whether it should still be held.
- Retest/pullback structure supporting the long? None — both today's watchlist entries for COTI (swing Trade Idea #7, intraday Trade Idea #6) are framed as **short** theses (failed bounce/retest), directly opposite the held long.
- Overextended? The move is extended against the position, not in its favor (7d return still +81.5% per the intraday report, so this reads as a fast retracement off a large prior pump, not a fresh breakdown).
- Actionable level: none for a fresh long; the existing position needs an operator to verify current live price against 0.015355 and decide hold/tighten/close.
- Aligned with market mood? No — both the macro tape and COTI's own two most recent snapshots argue against the long.
- Catalyst confirmation/contradiction: no fresh (24h) catalytic news found for COTI in internal `news_items`; a targeted WebSearch for "COTI crypto news August 2026" surfaced only routine product-roadmap coverage (Privacy Portal / Carbon DeFi MCP launches from late June) and general 2026-strategy commentary — nothing explaining the specific 24h move, and nothing contradicting the technical read. This is pure price action, not news-driven.
- **Status:** unchanged in substance from the 11:30 review, but now with a second consecutive snapshot (intraday, 15:11) independently confirming price below invalidation, on top of the swing snapshot (05:14) that first flagged it. Two internally-consistent, differently-timed report generators agreeing raises confidence this is a genuine tracking/stop-execution question, not a stale-snapshot artifact.

### EPIC/USDT (long, intraday B-tier `WAITING FOR ENTRY` + separate already-OPEN swing long — best long-watch)

- Has price already reacted to a catalyst? No fresh catalyst — pure RS/momentum thesis, consistent across scalp/intraday/swing reports and confirmed via a targeted internal `news_items` check (0 fresh rows in 24h).
- Is the setup chasing? No — the intraday signal remains WAITING FOR ENTRY; the desk has not filled it since at least the 11:30 review (entry zone unchanged: 0.880285-0.903419, expires 2026-08-03T00:51:46).
- Retest/pullback structure? Yes — that is exactly what the waiting-for-entry status represents.
- Overextended (>2 ATR from EMA20)? Not flagged for this specific signal.
- Would entry now be late? No — the entry zone and status are unchanged from the last review; still a genuine watch, not a chase.
- Actionable level: fill inside 0.880285-0.903419 with volume confirmation; invalidation 0.852011.
- Aligned with market mood? Partially — genuine RS-leader (`crypto_swing_narrative_rs_momentum`, the desk's strongest playbook, 14d WR 72%/PF 5.80), but correlated to the broader no-catalyst alt cluster and a risk-off macro tape.
- Chase risk: low for this specific signal.
- Catalyst confirmation/contradiction: none — pure technical/RS thesis.
- Separately, the already-OPEN EPIC/USDT swing long (entry 0.884570-0.905221, invalidation 0.859329) continues to ride the same move — hold, no action needed.

### HOME/USDT (long, OPEN swing position, no fresh action)

- Same profile as EPIC: no-catalyst RS/momentum long (24h +19.75% per this cycle's intraday report, RS +19.73% vs BTC), extended for **new** entries at current price — a targeted WebSearch ("HOME crypto token news catalyst August 2026") found no symbol-specific news for a token called HOME; general August-2026 crypto-catalyst coverage (token unlocks, MultiversX/LayerZero/Zano events) did not mention it either, consistent with the internal "no fresh catalyst" read.
- Derivatives: price up + OI up (fresh positioning, not exhausted), funding -8.7e-05 (roughly neutral), crowding normal — supportive, not yet crowded.
- No fresh (24h) internal `news_items` rows for HOME, and no external corroboration either — confidence in the "no catalyst" read is reasonably high for this symbol specifically.
- Aligned with mood: same caveat as EPIC — correlated no-catalyst alt-rotation risk if BTC breaks down further; hold, don't add at current price.

### XRP/USDT (swing, OPEN short, partial TP booked)

- Cleanest short expression of the desk's risk-off macro thesis among currently-held positions — already de-risked via a booked TP1.
- Entry 1.0598-1.0610, invalidation 1.0626, status TP1_HIT (partial) — hold, let the remainder run per existing TP ladder; no new action recommended.
- Aligned with mood: yes — BTC/ETH both downtrend, macro risk elevated, this is the one held position that benefits from the current regime rather than fighting it.

### UNH (stocks, held C-tier `invest` position, TP1_HIT — legal/headline risk carry-forward)

- **LEGAL/HEADLINE RISK.** Internal `news_items` had 0 fresh (24h) rows for UNH, triggering external verification per §G. WebSearch + two WebFetch checks confirmed: UnitedHealth is under an **escalating DOJ antitrust probe into its Claritev unit** — new civil investigative demands including allegations of collusion with major insurers, addressing both market competition and pricing practices, going beyond the company's previously-disclosed antitrust matters ([SahmCapital, dated 2026-07-16](https://www.sahmcapital.com/news/content/unitedhealth-unh-faces-broader-doj-antitrust-probe-into-claritev-2026-07-16)). This sits on top of a longer-running DOJ Medicare-billing-practices investigation first reported in 2025 ([Yahoo Finance, dated 2025-07-24](https://finance.yahoo.com/news/unitedhealth-stock-sinks-47-after-company-confirms-doj-investigation-into-medicare-billing-practices-133527260.html)) — this is a persistent, escalating risk, not a single fresh headline.
- Market is closed (Sunday) — no fresh price reaction to evaluate; this is carry-forward risk context for the next actionable stocks session, not a live trade signal.
- Per §I: because this legal risk is verified, UNH's final verdict is **AVOID / MANUAL REVIEW REQUIRED** — never treated as a clean actionable, regardless of its C-tier `invest` score (81.8, tp1_hit).
- Actionable level: none — this is a risk flag on an existing planning-context position, not a fresh idea.

## 8. Best Candidates Ranked

1. **EPIC/USDT** (intraday, WAITING FOR ENTRY — best long-watch) — cleanest, most concrete trigger of the cycle: unchanged entry zone since the 11:30 review, price still below it, on the desk's strongest playbook.
2. **EPIC/USDT / HOME/USDT / AEVO/USDT** (swing, OPEN — hold) — same RS-leader profile, no fresh catalyst, currently extended for adds; hold as-is.
3. **XRP/USDT** (swing, OPEN short, partial TP booked) — cleanest short expression of the risk-off macro thesis, already de-risked.
4. **BANK/USDT** (short-watch, not yet actionable) — needs a confirmed failed-bounce break below 0.0480-0.0488 with a stop above 0.0497; squeeze-prone until then (fresh shorts already pressing, OI +7.27%).
5. **HYPE/USDT** (catalyst-watch, not yet actionable) — perps_dex_narrative basket primary, fresh <1h, but no concrete technical zone published today; needs a defined entry before it clears watch status.

**COTI/USDT is explicitly excluded from this ranked list** — see §9 and §14; it is a manual-review item, not a ranked candidate. **UNH is excluded from actionable ranking** — see §7 and §9; legal/headline risk caps it at AVOID / MANUAL REVIEW REQUIRED regardless of score.

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and monitors continue regardless.

- **COTI/USDT** — avoid adding; existing long shows price through its own invalidation level across two independent, differently-timed snapshots today; flag for immediate manual position review (§14, priority remains high, now 4th-cycle-persistent).
- **UNH** — AVOID / MANUAL REVIEW REQUIRED per verified, escalating DOJ antitrust risk (§7, §I); not actionable regardless of its C-tier `invest` score.
- **BANK/USDT** — short-squeeze risk (fresh shorts pressing + funding negative + OI rising); do not short without a confirmed bearish HTF break.
- **HOME/USDT, UAI/USDT, SHOT/USDT, HYPER/USDT** — >2 ATR from EMA20, explicit chase-risk flags in today's rejected lists; do not chase fresh entries.
- No clean fresh long or short clears the A-tier bar this cycle — this applies to the current window only, not a system pause. Stocks are fully closed (Sunday) and carry no fresh actionable verdict either way.

## 10. Main Risks

- **COTI position integrity**: now a 4th-consecutive-review finding of an open long trading through its own invalidation level, independently corroborated by two differently-timed report snapshots today — the most concrete operator-attention item on the desk.
- **BTC Coldcard exploit**: ~$89M across 4,585 addresses, attacker still holds the funds, `block_requires_operator_review` flagged desk-wide — an active, spreading crypto-market risk overlay, not yet resolved.
- **UNH legal/regulatory exposure**: verified, escalating DOJ antitrust probe (Claritev) on top of a longer-running Medicare-billing investigation — material risk to carry into the next actionable stocks session.
- **Correlation cluster**: EPIC/HOME/AEVO are all no-catalyst RS-momentum longs in the same rotation — a single BTC/ETH downdraft would likely hit all three together.
- **Catalyst mapping at 53.4% unmapped**: reduces confidence in "no fresh catalyst" reads generally, though a meaningful share of unmapped volume is inherently symbol-less geopolitical wire content.
- **Squeeze risk on the short side**: BANK carries crowded fresh-short positioning; a short without confirmation risks a violent reclaim.
- **Slot-timing mismatch**: this is technically a Sunday run of a slot designed for "10 minutes before US open" — the next real US open is ~24.5h away, not imminent; treat this review's stocks content as weekend planning, not a live pre-open read.

## 11. Action Plan — next 4 hours

1. **Escalate COTI/USDT swing long for immediate manual review** — verify live price against invalidation (0.015355) and decide hold/tighten/close (§14 TODO, 4th consecutive cycle, priority remains high).
2. Hold EPIC/HOME/AEVO/XRP swing positions as-is; no new entries unless price returns to stated pullback/entry zones with volume confirmation.
3. Watch the EPIC/USDT intraday signal (WAITING FOR ENTRY, entry 0.880285-0.903419, expires 2026-08-03T00:51:46) — the cleanest concrete trigger this cycle; let it come to the zone.
4. Watch BANK/USDT for a confirmed bearish HTF break below the 0.0480-0.0488 failed-bounce zone before considering a short entry.
5. Watch HYPE/USDT for the perps-DEX catalyst basket to produce a concrete technical zone while it remains fresh (<1h window).
6. Note UNH's escalating DOJ/Claritev risk for the next actionable stocks session (Monday US open) — treat as AVOID / MANUAL REVIEW REQUIRED, not a clean position, regardless of its held C-tier score.
7. Continue scanning/tracking/monitoring uninterrupted into the Monday 2026-08-03 ~09:30 ET US cash open — no pause recommended.

## 12. Final Verdict per Mode

- **Scalp**: No trade. Structurally weak playbook (14d PF 0.10/avgR -0.26 this cycle's stats window); 0 A-tier this cycle.
- **Intraday**: No trade for fresh entries. 1 signal WAITING FOR ENTRY (EPIC/USDT) — the cleanest watch of the cycle.
- **Swing**: Hold existing RS-leader longs (EPIC, HOME, AEVO) and the XRP short; no fresh entries. **COTI long remains flagged for immediate manual review** — 4th consecutive cycle, escalating in severity (two independent snapshots today confirming price-through-invalidation).
- **Stocks (all modes)**: Closed (Sunday) — planning/carry-forward context only, no verdict. **UNH flagged AVOID / MANUAL REVIEW REQUIRED** for the next actionable session per verified escalating DOJ antitrust risk. Pre-US stocks overlay: 0 eligible candidates this cycle (no fresh weekend intraday cycle to seed it).

## 13. Sources

- Internal:
  - `data/catalysts/2026-08-02/catalyst_cycle_12-13.md`, `catalyst_events.jsonl` (recomputed), `narrative_baskets.jsonl`.
  - `news_items` table, direct queries for COTI/HOME/EPIC/BANK/UNH/BTC (24h window).
  - `data/reports/scalp/2026-08-02_12-04_scalp_report.md`, `data/reports/intraday/2026-08-02_12-11_intraday_report.md`, `data/reports/swing/2026-08-02_02-14_swing_report.md`.
  - `active-signals`/`signal-stats` CLI outputs (crypto + stocks), `detect_untracked_legacy_alerts` CLI output, `stocks-preus-candidates` CLI output.
- External (triggered per §G — internal records missing/stale for COTI, HOME, UNH):
  - [COTI (COTI) Price Today, News & Live Chart | Forbes Crypto Market Data](https://www.forbes.com/digital-assets/assets/coti-coti/) — general product/roadmap coverage, no explanation for the specific 24h move (single_source aggregation, date unavailable per-article).
  - [Best altcoins to watch in August 2026 - Crypto.com International](https://crypto.com/en/market-updates/best-altcoins-august-2026) — no mention of a "HOME" token; used to confirm absence of a fresh external catalyst.
  - [UnitedHealth stock sinks 4.7% after company confirms DOJ investigation into Medicare billing practices](https://finance.yahoo.com/news/unitedhealth-stock-sinks-47-after-company-confirms-doj-investigation-into-medicare-billing-practices-133527260.html) — verified via WebFetch, dated 2025-07-24, primary_source-adjacent (company statement quoted).
  - [UnitedHealth (UNH) Faces Broader DOJ Antitrust Probe Into Claritev](https://www.sahmcapital.com/news/content/unitedhealth-unh-faces-broader-doj-antitrust-probe-into-claritev-2026-07-16) — verified via WebFetch, dated 2026-07-16, single_source, confirms escalation (new civil investigative demands).

## 14. Fix Requests / TODO

### TODO-coti-invalidation-breach
- **issue:** COTI/USDT is held as an OPEN swing long (`sig_06b6c2801005f29d`, entry 0.016109-0.016726, invalidation 0.015355) but two independent, differently-timed report snapshots today (05:14 swing → failed-bounce zone 0.0147-0.0150; 15:11 intraday → failed-bounce zone 0.0135-0.0137) both place price below the stated invalidation, while the signal status remains `triggered` (open), not stopped/closed. This is the **4th consecutive review** to flag COTI's direction-contradiction/invalidation-breach (23:26 Aug-1 → 04:30 → 11:30 → this 16:05 cycle), and the second cycle to independently corroborate the breach with two different report generators agreeing.
- **evidence:** `active-signals --asset-class crypto` (status=triggered, invalidation=0.015355); `data/reports/swing/2026-08-02_02-14_swing_report.md` Trade Idea #7 (failed-bounce zone 0.0147-0.0150); `data/reports/intraday/2026-08-02_12-11_intraday_report.md` Trade Idea #6 (failed-bounce zone 0.0135-0.0137, continuing decline); `news_items` query showing 0 fresh (24h) catalytic news for COTI.
- **suggested manual fix:** An operator should immediately verify COTI/USDT's live price against the position's invalidation level and decide whether to hold, tighten, or close — and separately, engineering should check whether the stop/invalidation-monitoring job is running correctly for this signal (four consecutive review cycles observing the same unresolved condition, now independently corroborated across two report types, argues against this being a transient snapshot artifact).
- **priority:** high (unchanged — this remains a position-integrity question, not just a direction-contradiction narrative; now the longest-running single-position flag across this review series)
- **first observed:** 2026-08-01 23:26 EEST (4th consecutive cycle to flag it)

### TODO-catalyst-mapping-weak-recurring
- **issue:** Catalyst symbol-mapping has been >50% unmapped for multiple consecutive review cycles (57.3% → 59.0% → 56.9% → now 53.4%), a mix of unparsed Binance announcement templates and inherently symbol-less geopolitical/macro wire content.
- **evidence:** direct recomputation of `data/catalysts/2026-08-02/catalyst_events.jsonl` (1,991 total / 927 mapped / 1,064 unmapped); sample unmapped titles today include both promo noise ("#ByBit News: Complete Your First Trade...") and geopolitical wires (IAEA Zaporizhzhya power-outage reports, Iran energy-strike threats) with no symbol to map to by design.
- **suggested manual fix:** Improve the catalyst symbol resolver for the parseable subset (Binance leverage-adjustment / futures-announcement templates), and consider adding a "structurally symbol-less" classification (promo/geopolitical-macro) so the unmapped % metric doesn't conflate genuine resolver gaps with content that was never going to map to a symbol.
- **priority:** low (context-only impact, does not gate scoring/routing; trend is slowly improving)
- **first observed:** recurring across multiple prior reviews (at least 2026-07-31 21:45 onward); still open.

### TODO-preus-slot-weekend-mismatch
- **issue:** The `opus-enriched-review-preus` scheduled task fires daily at a fixed 15:55 Nicosia / 08:55 ET regardless of day-of-week, but the slot's design intent ("~10 min before US cash open, final pre-open read") only literally applies on trading days. On Saturday/Sunday runs (like this one), the "next open" is up to ~48h away rather than ~10 minutes, and the stocks pre-US overlay (`stocks-preus-candidates`) will always return 0 eligible/0 excluded since no weekend stocks-intraday cycle exists to seed it.
- **evidence:** this run (2026-08-02, Sunday): `stocks-preus-candidates` → 0 eligible / 0 excluded; last stocks-intraday report Friday 2026-07-31 20:00 EEST.
- **suggested manual fix:** Consider gating the weekend fires of this specific slot to a lighter-weight "carry-forward only" mode (skip the stocks overlay entirely on Sat/Sun rather than running it against stale/absent data), or leave as-is if the crypto-only content is still considered valuable on weekends — this is a design question for a human to decide, not a bug to silently fix.
- **priority:** low (no incorrect output produced — the overlay correctly reports 0/0 — but the review title/framing to a manual reader could be confusing on non-trading days without this context, which is why it's now stated explicitly in §1/§3 each weekend run)
- **first observed:** 2026-08-02 16:05 EEST (this cycle)
