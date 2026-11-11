---
REVIEW: OPUS ENRICHED REVIEW — ⚠ ADVISORY ONLY — NO EXECUTION
SLOT: crypto overnight / Asia review · 2026-07-08 · 04:40 EEST
WRITTEN: 2026-07-08 04:47 EEST
PREV REVIEW: 2026-07-07 23:37 EEST (post-close final daily review)
STATUS: AUTOMATED SCHEDULED RUN — NO HUMAN IN SESSION
---

# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:40 EEST

## 1. Executive Summary

**Slot: crypto overnight / Asia review — advisory only / no auto-trade.** Stocks market is closed at this hour (04:40 EEST / 21:40 ET prior day) — all stocks data below is carry-forward/planning context only, crypto is the live actionable class.

**Crypto is holding a risk-on trend overnight, but a real macro shock landed a few hours ago.** BTC/ETH both in uptrend (altcoin breadth 55.8% above EMA20, 67.4% above EMA50), and 3 no-catalyst momentum longs (SPELL, BANANA, ZEC intraday B-tier) are already **OPEN** and being managed. Separately, the US launched strikes on Iranian targets (Sirik, Bandar Abbas, Qeshm) on 2026-07-08 after Iranian attacks on tankers in the Strait of Hormuz, and revoked Iran's oil-export sanctions waiver — confirmed via a working Al Jazeera source. BTC has not broken down (external print ~$61.8k-$63.7k, consistent with the internal ~$63.45k-$63.68k swing zone — no price-data contradiction), apparently offset by Fed-rate-cut hopes from weak US jobs data. This is a genuine, escalating geopolitical tail risk that the internal catalyst layer captures only as unmapped generic "other_news" (139 matching rows, no symbol, no dedicated category) — treat it as a live overnight risk factor, not noise.

**No A-tier signals anywhere** (crypto or stocks) and **crypto scalp remains disabled by policy** (`config/crypto_quality_overlay.yaml: disabled: true`; 14d audit −4.4R). Crypto week-level stats: intraday PF 1.70/avgR +0.20 (n=162) and swing PF 1.87/avgR +0.31 (n=107) both working; scalp PF 0.66/avgR −0.08 (n=161) still net-negative and correctly sidelined.

**Zero untracked legacy alerts today** (was 11 flat at the last review — the multi-review tracker-integrity gap appears resolved for now, monitored for recurrence). Swing report is now **stale ~23h44m** (last gen 2026-07-07 05:03 EEST) — 4th+ consecutive review flagging this, worsening each cycle.

**ZEC/USDT remains the best-verified catalyst** (Orchard shielded-pool bug fix / Ironwood upgrade narrative) and is already an OPEN intraday long. No clean new long or short entry this window — route to watch-list triggers (see §6/§8). UNH and SMCI carry forward as hard legal-risk AVOIDs.

**Notifier bug found and worked around this run**: the Telegram sender rejected (HTTP 400) any message containing the literal filename `OPUS_ENRICHED_REVIEW_LATEST.md` because its default `parse_mode="Markdown"` treats the filename's underscores as unbalanced italics markers; wrapping the filename in backticks fixed it for this run's send. See §14 TODO.

---

## 2. Data Used

| Source | File / Timestamp | Age at 04:47 EEST | Quality |
|--------|-------------------|--------------------|---------|
| Scalp report | `2026-07-07_23-43_scalp_report.md` (gen 02:43:xx EEST) | ~2h04m | FRESH — no A/B setups, scalp shadow-only |
| Intraday report | `2026-07-07_23-49_intraday_report.md` (gen 02:49:46 EEST) | ~1h58m | FRESH |
| Stocks intraday | `2026-07-07_23-57_stocks_intraday_report.md` (data freshness 23:57 UTC) | ~1h50m | FRESH but market-closed / planning-only (all A/B demoted to C) |
| Crypto swing | `2026-07-07_02-03_swing_report.md` (gen 05:03 EEST, 2026-07-07) | ~23h44m | **STALE** ✗ (>14h; only source — carried forward with heavy caveat; the one live BTC swing DB signal evaluated on its own merits) |
| Stocks swing/invest | `2026-07-02_13-0x` | 6d | **STALE** ✗ (excluded) |
| Cycle summary | `cycle_06_02-36_summary.md` (in `2026-07-07_default_schedule/`, day-rollover naming) | ~1h46m | FRESH, 32/32 steps OK, monitor window 90min (ends ~04:06-04:31, concluding just before this review) |
| Paper monitor | `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 03:00 EEST) | ~1h47m | FRESH |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-07_2337.md` (post-close) | ~5h10m | CONTEXT — compared in §4 |
| Catalyst events | `data/catalysts/2026-07-07/catalyst_events.jsonl` (day-rollover folder; latest cycle file `catalyst_cycle_23-50.md`, mtime 02:50 EEST) | ~1h57m | FRESH; 5477 events cumulative today, 977 mapped (17.8%), 5 active baskets |
| DB queries | `db/crypto_ai_desk.sqlite` (`news_items`, read-only) | live | ZEC catalyst confirmed <24h; Iran/Hormuz macro headline confirmed <24h |
| External: BTC price | Sunday Guardian Live, 2026-07-08 | live | single_source, cross-checked vs internal levels — consistent |
| External: Iran/Hormuz strikes | Al Jazeera live-blog, 2026-07-08 (WebFetch verified, 200) | live | primary_source |

**Notes**: TradingView/manual chart check unavailable — all technical levels from local OHLCV/ATR/EMA. Onchain config missing, social attention missing (Reddit sources failing). Both `data/crypto_ai.db` and `data/crypto_ai_desk.db` at the project root are 0-byte stubs — the live DB is `db/crypto_ai_desk.sqlite` (used for the read-only news_items query above).

---

## 3. Scheduler / Data Freshness

- **Last completed cycle**: `cycle_06_02-36_summary.md` — started 02:36:58, finished 03:01:11 EEST (~1h46m before this review), 32/32 steps OK, 90-min monitor window (ends ~04:06-04:31 EEST, i.e. right around this review's dispatch).
- **Scheduler health**: FRESH. Not deferred — both `scheduler.log` (mtime 03:01 EEST, ~1h46m) and the latest cycle summary are well under the 3h defer threshold. (Note: the freshest scheduler.log/cycle file currently live under the `2026-07-07_default_schedule/` folder rather than a `2026-07-08_default_schedule/` folder — a day-rollover naming quirk, see §14.)
- **Paper monitor status** (operator vocabulary, from `PAPER_MONITOR_STATUS_LATEST.md`, ~1h47m old):
  - OPEN actionable: **3** (BANANA/USDT, SPELL/USDT, ZEC/USDT — all crypto intraday B, entry filled, monitoring TP/SL)
  - WAITING for entry: **1** (BTC/USDT swing B, $63,451-$63,680)
  - REVIEW/SHADOW: **138**
  - ENTERED UNRESOLVED (entry filled, no TP/SL before window — NOT missed entries): **8**
  - NO-ENTRY / STALE / MOVED-AWAY: **22**
  - CLOSED: **382 WIN / 51 LOSS / 0 FLAT**
  - NEEDS REVIEW: **0**
- **Untracked legacy alerts**: **0** today (`detect_untracked_legacy_alerts --since 2026-07-08` → "None. Every legacy crypto alert has a backing proposed_signal"). This resolves the 3+ review carried-forward TODO — kept under watch for recurrence, not closed permanently.
- **Crypto week signal-stats** (headline, A/B only): sample 430, triggered 409, WR 15.65%, PF 1.4874, avgR 0.1407, totalR 40.94. By mode: scalp PF 0.658/avgR −0.078 (n=161, net negative, correctly disabled), intraday PF 1.70/avgR +0.20 (n=162), swing PF 1.87/avgR +0.31 (n=107).
- **Stocks week signal-stats** (headline, A/B only): sample 18 (confidence=weak), WR 0%, PF 0.0, avgR −0.2143, totalR −3.0. C-tier watchlist: PF 0.92, totalR −1.89 (n=203).

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-08 04:47 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.78,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "tradingview_unavailable", "social_attention_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Cycle 06 (02:36) finished 03:01:11 EEST, 32/32 OK, ~1h46m before this review",
        "Scalp/intraday/stocks-intraday reports FRESH (~1h50m-2h04m)",
        "Crypto swing STALE 23h44m (last gen 2026-07-07 05:03 EEST) - 4th+ consecutive review flagging this, worsening",
        "Catalyst folder present with fresh data (cycle_23-50, 02:50 EEST, ~1h57m) but filed under prior-day directory name due to a rollover naming quirk",
        "0 untracked legacy alerts today (was 11 at last review)"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": ["risk_on", "longs_preferred", "mixed"],
      "data_missing": ["etf_flows", "dxy_yields", "onchain_whale_flows"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "BTC uptrend, ETH uptrend, altcoin breadth 55.81% above EMA20 / 67.44% above EMA50 (internal, intraday report)",
        "Macro risk score 63/100 (3 risk-off hits, 0 risk-on, 2 calendar/watch) per internal report",
        "External (Al Jazeera, verified via WebFetch): US struck Iranian targets (Sirik, Bandar Abbas, Qeshm) 2026-07-08 after Iranian tanker attacks in Strait of Hormuz; US revoked Iran oil-export waiver (wind-down deadline July 17)",
        "External (Sunday Guardian Live): BTC ~$61.8k-$63.7k on weak-jobs-data Fed-cut hopes, consistent with internal $63.45k-$63.68k swing zone - no price contradiction found",
        "Stocks market closed at this hour - no fresh regime read"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["fresh_catalyst", "no_catalyst", "mapping_weak", "catalyst_confirmed", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "ZEC Orchard-bug-fix catalyst confirmed fresh <24h internally (news_items, The Block, 2026-07-07T14:12 -04:00) and externally reconfirmed in the prior review",
        "Catalyst mapping weak this run: 5477 events today, 977 mapped (17.8%), 4500 unmapped (82.2%) - above the 50% weak threshold",
        "5 active narrative baskets: perps_dex_narrative (HYPE, wait_pullback), rwa_narrative (ONDO/XLM), ai_narrative (NEAR/RENDER/TAO/FET), delisting_thin_liquidity (no primary), momentum_breakout (SPELL, wait_pullback)",
        "The dominant overnight macro story (US-Iran strikes/Hormuz) is present internally only as unmapped generic other_news (139 matching rows, no symbol, no dedicated geopolitical category)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "data_unavailable"],
      "data_missing": ["oi_24h_change", "liquidation_heatmap", "order_book_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SPELL/USDT: funding -0.0187 (mexc), crowding elevated (negative funding across external venues)",
        "BANANA/USDT: funding -0.0012 to -0.0024 (bybit/mexc), crowding elevated",
        "ZEC/USDT: funding neutral (~0.0001 across bybit/okx/mexc), crowding low",
        "OI 24h change unavailable (n/a) across all tracked symbols this cycle - a standing blindspot"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "overextended"],
      "data_missing": ["tradingview_manual_check"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SPELL/USDT +21.91% 24h, RS vs BTC +22.86%, entry plan explicitly says pullback only / no market buy if extended - already OPEN (entered) per paper monitor",
        "BANANA/USDT +6.97% 24h, similar pullback-only entry plan, already OPEN",
        "ZEC/USDT pullback zone $477.11-$482.26 vs already OPEN status - existing position, not a fresh chase decision",
        "No B-tier short setups exist in either scalp or intraday report this cycle"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "PAPER_MONITOR_STATUS_LATEST.md (~1h47m old): OPEN_ACTIVE=3, WAITING_FOR_ENTRY=1, REVIEW_ONLY_SHADOW=138, ENTERED_UNRESOLVED_EXPIRED=8, NO_ENTRY_EXPIRED=22, CLOSED_WIN=382, CLOSED_LOSS=51, CLOSED_FLAT=0, UNKNOWN_INCONSISTENT=0",
        "0 untracked legacy alerts today (detect_untracked_legacy_alerts --since 2026-07-08)"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "UNH: confirmed multi-source DOJ criminal + civil Medicare-billing fraud investigation - carried forward, hard legal block",
        "SMCI: federal securities lawsuit / export-control violations flag - carried forward, legal cap active",
        "NEW/escalating: US-Iran war strikes on Bandar Abbas/Sirik/Qeshm (2026-07-08), Strait of Hormuz tanker attacks, Iran oil-export waiver revoked - genuine geopolitical tail risk overlay for the overnight/Asia window, confirmed via primary source",
        "Reduce sizing recommended on any new overnight crypto swing hold given this macro overlay"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto scalp disabled by policy (config/crypto_quality_overlay.yaml disabled:true; 14d audit -4.4R/-$110); week-level PF 0.658/avgR -0.078 (n=161) confirms continued negative edge",
        "Crypto intraday PF 1.70/avgR +0.204 (n=162) and swing PF 1.87/avgR +0.307 (n=107) both working",
        "Stocks A/B headline PF 0.0/WR 0%/totalR -3.0 (n=18, weak sample); stocks C-tier PF 0.92/totalR -1.89 (n=203) - stocks playbook still underperforming, consistent with prior carried-forward TODO"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.62,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "BTC/USDT", "trigger": "pullback into live swing entry zone $63,451-$63,680", "reason": "Only live WAITING swing signal; BTC/ETH uptrend intact, altcoin breadth constructive, but no fresh confirmation yet at current print" },
    "best_short_candidate":    { "symbol": "TLM/USDT", "trigger": "confirmed failed bounce + BTC loses $63,000 support", "reason": "Weakest RS in the intraday universe (-16.23% vs BTC), but currently squeeze-capped / no B-tier short exists - pass until BTC weakens" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "already OPEN (entered) on the Orchard-fix/Ironwood-upgrade narrative; fresh add-on only on a clean pullback, not the current extended print", "reason": "Best-verified catalyst this cycle, catalyst_confirmed, live tracked position" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "Confirmed multi-source DOJ criminal + civil Medicare-billing fraud investigation - hard legal block regardless of score (100/100 raw)" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.78 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.68 | risk_on, longs_preferred, mixed | advisory_only |
| catalyst_narrative | caution | 0.55 | fresh_catalyst, no_catalyst, mapping_weak, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, overextended | advisory_only |
| execution_lifecycle | ok | 0.85 | open_actionable, waiting_for_entry, review_shadow | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, legal_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution (synthesis) | 0.62 | (synthesises all 8 above) | advisory_only |

---

## 4. What Changed vs Previous Review

Comparison vs `OPUS_ENRICHED_REVIEW_AUTO_2026-07-07_2337.md` (post-close, 23:37 EEST):

- **New**: US launched strikes on Iranian targets (Bandar Abbas/Sirik/Qeshm) overnight, 2026-07-08, in response to tanker attacks in the Strait of Hormuz; Iran oil-export sanctions waiver revoked. Not present in the prior review — this is the single biggest new development this cycle.
- **Resolved**: Untracked legacy alerts dropped to **0** (was flat at 11 for 3+ consecutive reviews). Kept under watch, not declared permanently fixed.
- **Changed status — 0 open → 3 open**: BANANA, SPELL, and ZEC (all crypto intraday B) went from "0 open actionable" at 23:37 to all three **OPEN** now (entries filled, monitoring TP/SL). This is the expected overnight-into-Asia entry activity, not new information about them.
- **Confirmed**: ZEC/USDT catalyst thesis unchanged (Orchard fix / Ironwood upgrade) — still the best-verified crypto catalyst.
- **Confirmed unchanged**: UNH (DOJ legal block), SMCI (legal/export-control block), swing report staleness (now worse, 23h44m vs 21h34m).
- **Worsened**: Catalyst mapping unmapped % ticked up slightly (82.2% now vs 82.2% at 23:37 — flat/no material change, still weak).
- **New candidate not previously live**: none — SPELL/BANANA/ZEC were already flagged as watch-only at 23:37; they have simply since triggered and entered.

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative, `data/catalysts/2026-07-07/catalyst_events.jsonl`): **5477**
- Mapped (non-null symbol): **977** (17.8%)
- Unmapped (null symbol): **4500** (82.2%)
- `narrative_baskets` (latest cycle): **5**
- **⚠ Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (82.2% unmapped, above the 50% threshold)
- Top 3 unmapped headlines by importance: "INVESTOR ALERT: GeneDx Holdings Corp. (WGS) Investors with Substantial Losses Have Opportunity to Lead the GeneDx Class Action Lawsuit" (0.748); "Trader loses $2M in 'same-block backrun extraction' exploit" (0.748); "WGS Investors Have Opportunity to Lead GeneDx Holdings Corp. Securities Fraud Lawsuit with the Schall Law Firm" (0.748)
- Active baskets: `perps_dex_narrative` (HYPE, playbook wait_pullback, related DYDX/GMX/ASTER), `rwa_narrative` (ONDO/XLM, playbook related_beta_rotation), `ai_narrative` (NEAR/RENDER/TAO/FET, related WLD/ASTER), `delisting_thin_liquidity` (playbook avoid_low_liquidity, no primary), `momentum_breakout` (SPELL, playbook wait_pullback)
- The Iran/Hormuz war — today's dominant macro story — is present in the raw feed (139 matching rows) but every one is classified generic `other_news` with a null symbol; it is not surfaced as its own basket or geopolitical category. Use §1/§6 for the verified read instead of the catalyst layer for this specific story.

---

## 6. Market Landscape

- BTC/ETH: both uptrend; BTC ~$63.5k region (internal swing zone $63,451-$63,680; external print $61.8k-$63.7k, consistent)
- Altcoin breadth: 55.81% above EMA20, 67.44% above EMA50 — constructive but not extreme
- Macro risk score: 63/100 (3 risk-off hits) — driven by the Iran/Hormuz escalation and Fed-cut-hope crosscurrent
- Recommended local trading style (per internal report): selective longs, prefer pullbacks on relative strength

### Market Mood / Risk Routing

- **Crypto mood**: risk-on / holding trend, but overlaid with a genuine escalating geopolitical shock (US-Iran strikes, Strait of Hormuz, oil-sanctions waiver revoked) that has not yet broken BTC's structure — treat as an active overnight tail-risk, not resolved
- **Stocks mood**: closed — carry-forward context only; last session's read was risk-off-into-close on a chip/semis rotation (AMD/TSLA short ideas queued for planning, not actionable)
- **Dominant narrative**: ZEC's Orchard-fix/Ironwood-upgrade story remains the cleanest verified crypto catalyst; SPELL/BANANA are pure no-catalyst momentum (both already open); the Iran/Hormuz war is the dominant macro headline of the night but is under-captured by the internal catalyst layer
- **Preferred side now**: longs, selectively — manage the 3 existing OPEN intraday longs; no fresh chase; wait-for-trigger on anything new
- **Best long candidate**: none new/clean — best long-**watch**: BTC/USDT swing on pullback into $63,451-$63,680
- **Best short candidate**: none clean — best short-**watch**: TLM/USDT only on confirmed failed bounce + BTC losing $63,000 (currently squeeze-capped, pass tonight)
- **Best catalyst-backed candidate**: ZEC/USDT — already OPEN; further size only on a clean pullback, not the current print
- **What to avoid**: UNH (DOJ fraud, confirmed), SMCI (legal/export-control), chasing SPELL/BANANA/ZEC at current extension
- **What would change the view**: BTC daily close below $63,000 → demote crypto intraday/scalp aggression (Asia dead-zone guard already active 00:00-06:00 UTC); a material widening of the Iran/Hormuz conflict (e.g. a Strait of Hormuz closure attempt, oil spiking >10% in a session) → reassess crypto risk-on read entirely; VIX materially higher at the next US pre-market read → escalate stocks caution

---

## 7. Candidate Deep Dives

### Candidate 1: ZEC/USDT — catalyst-backed intraday long — OPEN, MANAGE ONLY

**Status**: OPEN actionable per paper monitor (entry filled, monitoring TP/SL), B-tier intraday, score 65.0, entry zone was $477.11-$482.26, invalidation $470.82, TP1 $496.00/TP2 $507.44/TP3 $518.89.

**Catalyst**: Orchard shielded-pool counterfeit-bug fix / Ironwood-upgrade narrative — confirmed internally via `news_items` (The Block, 2026-07-07T14:12 -04:00, "ZEC jumps 12% as Zcash nears mathematical proof against hidden counterfeit bugs"), consistent with the prior review's external CoinGecko reconfirmation. `catalyst_confirmed`, not contradicted.

**Price reaction / structure**: Has price already reacted to the catalyst? Yes, up sharply this week (+21.3% 7d per last snapshot). Is the setup chasing? No — this is an already-filled managed position, not a fresh decision. Overextended? Volume is below average (0.39x 20-period), a soft spot noted in the report's own counter-thesis. Would a *fresh add* now be late? Yes — do not add at the current extended print.

**Verdict**: MANAGE ONLY — do not add to size; let TP1/TP2/TP3 and the $470.82 invalidation do the work overnight.

---

### Candidate 2: SPELL/USDT — no-catalyst momentum intraday long — OPEN, MANAGE ONLY / DO NOT ADD

**Status**: OPEN actionable, B-tier intraday, score 72.6, +21.91% 24h, RS vs BTC +22.86%, volume 0.9x.

Has price already reacted? Yes, strongest mover across all crypto reports tonight. Is the setup chasing? Explicitly yes per the report's own entry plan ("no market buy if extended"). Retest/pullback structure? Not established. Overextended? Consistent with the report's framing (RS extension well past the stated pullback zone). Catalyst support? None — pure momentum; this symbol sits inside the net-negative no-catalyst-intraday bucket (14d WR 23%/PF 0.70/-3R cited in the report).

**Verdict**: MANAGE ONLY on the existing filled position; do not add size; would only be a fresh long-watch on a confirmed pullback into the stated zone with volume.

---

### Candidate 3: BANANA/USDT — no-catalyst momentum intraday long — OPEN, MANAGE ONLY

**Status**: OPEN actionable, B-tier intraday, score 71.8, +6.97% 24h, RS vs BTC +7.93%, volume 1.19x, entry $3.183-$3.294, invalidation $3.048, targets $3.592/$3.840/$4.088.

Same no-catalyst-momentum profile as SPELL, less extended (RS +7.93% vs +22.86%). Funding negative across external venues (bybit -0.0024, mexc -0.0012) — crowding elevated, a mild squeeze-risk flag for the short side, not the long.

**Verdict**: MANAGE ONLY — no fresh action; watch the $3.048 invalidation.

---

### Candidate 4: BTC/USDT swing — WAITING FOR ENTRY — long-watch

**Status**: WAITING for entry (live, DB-confirmed), B-tier swing, score 66.8, entry zone $63,451-$63,680, invalidation $63,171, expires 2026-07-14.

Is this aligned with market mood? Yes — BTC/ETH uptrend, but the mood is now overlaid with the Iran/Hormuz macro shock, so a fresh swing hold carries more overnight tail risk than usual. Is it actionable now or only after confirmation? Only on the stated pullback into the entry zone. What would invalidate it? A 1h/4h close through $63,171, or a material escalation of the Iran/Hormuz conflict that breaks the current risk-on tape.

**Verdict**: WATCH — best long-watch this cycle; reduce size vs normal if triggered, given the live geopolitical overlay.

---

### Candidate 5: UNH / SMCI — LEGAL/HEADLINE RISK — AVOID (carried forward, stocks closed)

**Status**: C-tier (both were A/C raw, demoted by legal gate); stocks market closed — planning only.

UNH: confirmed multi-source (Globe and Mail/QuiverQuant, CBS News, TheHill, TipRanks per prior review's reconfirmation) active DOJ criminal + civil investigation into Medicare Advantage billing (diagnosis-upcoding). SMCI: federal securities lawsuit / export-control violations flag (TipRanks). Both unchanged since the last review; no new internal news_items rows for either symbol this cycle.

**Verdict**: AVOID, no score overrides this. Also queued for planning (not actionable, market closed): AMD short / TSLA short on the chip/semis-weakness thesis from the last stocks session.

---

## 8. Best Candidates Ranked

**No new clean entries this window** — 3 OPEN actionable positions to manage (ZEC/BANANA/SPELL intraday), 1 WAITING signal to track (BTC swing).

| Rank | Symbol | Status | Why | Trigger |
|------|--------|--------|-----|---------|
| 1 | ZEC/USDT | OPEN actionable (manage) | Best verified catalyst tonight (Orchard fix/Ironwood) | Manage to TP1 $496.00 / invalidation $470.82; no add at current print |
| 2 | SPELL/USDT | OPEN actionable (manage) | Strongest momentum but no catalyst, net-negative bucket | Manage to targets/invalidation; do not add |
| 3 | BANANA/USDT | OPEN actionable (manage) | No-catalyst momentum, less extended than SPELL | Manage to $3.048 invalidation |
| 4 | BTC/USDT swing | WAITING FOR ENTRY (live) | Only live swing signal; uptrend intact | Pullback into $63,451-$63,680; reduce size given Iran/Hormuz overlay |
| 5 | TLM/USDT | SHORT-WATCH | Weakest RS (-16.23% vs BTC), no B-tier setup exists | Confirmed failed bounce + BTC loses $63,000 |

**Best long-watch**: BTC/USDT swing on pullback (see above)
**Best short-watch**: TLM/USDT only if BTC loses $63,000 and a genuine failed bounce confirms — pass in current tape
**Best catalyst-watch**: ZEC/USDT — already open; fresh add only on a clean pullback

---

## 9. Avoid / No Trade

*This decision window only — scanning, tracking, and monitoring continue regardless.*

- **UNH**: Confirmed multi-source DOJ criminal + civil fraud investigation. Legal block — no entry regardless of score.
- **SMCI**: Federal securities lawsuit / export-control violations flag — legal cap active.
- **SPELL / BANANA / ZEC at current extension**: Not an "avoid the coin" call — the positions are already open and being managed; avoid **adding size** at the current print.
- **All new stocks A/B**: Market closed — planning-only, not actionable until RTH confirmation.
- **Any fresh crypto swing hold sized as normal**: Given the live, escalating Iran/Hormuz conflict, prefer reduced sizing on new overnight swing exposure until the conflict's market impact stabilizes.

---

## 10. Main Risks

1. **Escalating US-Iran war / Strait of Hormuz strikes (2026-07-08, confirmed via primary source)**: US strikes on Bandar Abbas/Sirik/Qeshm, oil-export sanctions waiver revoked (wind-down deadline July 17) — a live, unresolved geopolitical shock with real oil-market and risk-sentiment implications overnight into Asia hours.
2. **Catalyst layer does not capture the above**: 139 related headlines are all unmapped `other_news` — do not rely on the internal catalyst layer to flag further escalation; this review's external check is the only source of this risk right now.
3. **Swing report stale 23h44m** (4th+ consecutive review, worsening each cycle) — no fresh crypto swing perspective since 05:03 EEST the prior morning; the one live BTC swing signal is tracked from that stale run.
4. **Stocks A/B playbook still failing** (PF 0.0, WR 0%, n=18 weak sample, totalR -3.0 over the week) — carried-forward underperformance, not resolved.
5. **SPELL/BANANA/ZEC are all no-catalyst-or-thin-volume-supported longs** now open simultaneously — correlated crypto-beta exposure if BTC turns.
6. **Derivatives crowding elevated on SPELL/BANANA** (negative funding across external venues) — some squeeze-unwind risk on those two longs specifically.
7. **OI 24h-change data unavailable** across the board this cycle — a standing blindspot on crowding/squeeze confirmation.

---

## 11. Action Plan — Next 4 Hours (04:47-08:47 EEST / deep overnight into Europe open)

**Crypto**:
- Manage the 3 OPEN positions (ZEC, SPELL, BANANA) against their stated invalidation/target levels; do not add size to any of them at current prices.
- Track the 1 WAITING signal (BTC swing, $63,451-$63,680) — if triggered, size below normal given the live Iran/Hormuz overlay.
- Watch BTC $63,000 as the key level into Europe — a loss of this level should further demote crypto intraday/scalp aggression per the existing Asia dead-zone guard logic (00:00-06:00 UTC).
- No new swing action — data stale >23h; wait for the next scheduled swing run.
- Monitor for any further Iran/Hormuz escalation (oil price spikes, additional strikes, Strait of Hormuz closure attempts) — this is the single biggest wildcard for the next 4 hours.

**Stocks**:
- Market closed — no live action. AMD short / TSLA short remain planning-only ideas from the last session pending RTH confirmation. UNH/SMCI legal blocks carry forward unchanged.

**Risk management**:
- Reduce sizing on any new overnight crypto swing hold given the live geopolitical overlay.
- Legal blocks (UNH, SMCI) unchanged.
- 0 untracked alerts today — continue monitoring for recurrence, not urgent.

---

## 12. Final Verdict per Mode

| Mode | Verdict | Rationale |
|------|---------|-----------|
| Crypto scalp | DISABLED | Kill-switch active by policy (`crypto_quality_overlay.yaml`); 14d audit -4.4R, week PF 0.658/avgR -0.078 (n=161) confirms continued negative edge |
| Crypto intraday | MANAGE OPEN POSITIONS / NO NEW ENTRIES | 3 OPEN (ZEC/SPELL/BANANA); no fresh B-tier setups this cycle beyond those already triggered |
| Crypto swing | MONITOR ONE LIVE SIGNAL / NO NEW ENTRIES | Report stale >23h, excluded from fresh verdict; the one live BTC swing DB signal ($63,451-$63,680) tracked on its own merits, reduced size if triggered |
| Stocks intraday | CLOSED / PLANNING ONLY | Market closed; AMD/TSLA short ideas queued for RTH confirmation only |
| Stocks swing/invest | STALE DATA | >6d stale; excluded from all verdicts |
| C-tier / watchlist | SCANNING CONTINUES | Research/tracking active overnight; no Telegram-actionable entries |

---

## 13. Sources

**Internal project files**:
- `data/reports/scalp/2026-07-07_23-43_scalp_report.md`
- `data/reports/intraday/2026-07-07_23-49_intraday_report.md`
- `data/reports/stocks/intraday/2026-07-07_23-57_stocks_intraday_report.md`
- `data/reports/swing/2026-07-07_02-03_swing_report.md` (stale, carried forward with caveat)
- `data/scheduled_runs/2026-07-07_default_schedule/cycle_06_02-36_summary.md`
- `data/catalysts/2026-07-07/catalyst_events.jsonl`, `narrative_baskets.jsonl`, `catalyst_cycle_23-50.md`
- `reports/PAPER_MONITOR_STATUS_LATEST.md`
- `OPUS_ENRICHED_REVIEW_AUTO_2026-07-07_2337.md` (prior review, compared in §4)
- `db/crypto_ai_desk.sqlite` (`news_items`, read-only query)
- `config/crypto_quality_overlay.yaml`, `config/session_risk.yaml` (read-only, scalp kill-switch confirmation)
- `data/raw/enriched_review_sources/2026-07-08T0440_crypto_overnight.json` (this review's external citations, ingested)

**External sources**:
- [Iran war live: US bombs Sirik, Qeshm, Bandar Abbas over Hormuz attacks](https://www.aljazeera.com/news/liveblog/2026/7/8/iran-war-live-us-bombs-sirik-qeshm-bandar-abbas-over-hormuz-attacks) — Al Jazeera, 2026-07-08 (primary_source, WebFetch-verified)
- [Bitcoin Price Today (July 8, 2026): BTC Crosses Above $61,800...](https://sundayguardianlive.com/business/bitcoin-price-today-july-7-2026-btc-crosses-above-61800-ethereum-surges-over-5-as-fed-rate-cut-expectations-lift-crypto-market-heres-what-investors-should-know-230450/) — Sunday Guardian Live, 2026-07-08 (single_source, BTC price cross-check)
- [ZEC jumps 12% as Zcash nears mathematical proof against hidden counterfeit bugs] — The Block, 2026-07-07 (internal `news_items` row, primary_source per prior review's reconfirmation)

---

## 14. Fix Requests / TODO

### TODO-stocks-ab-playbook-failing [HIGH] (carried forward)
- **issue:** Stocks A/B WR 0% (n=18, weak sample), PF 0.0, totalR -3.0 over the week — unchanged pattern from prior reviews; underlying scoring for the `continuation` setup type remains net-negative.
- **evidence:** `signal-stats --asset-class stocks` headline: sample=18, wins=0, losses=4, PF=0.0, avgR=-0.2143, totalR=-3.0; C-tier watchlist PF=0.92, totalR=-1.89 (n=203).
- **suggested manual fix:** Review stocks intraday scoring for the `continuation` setup, particularly the no-catalyst cohort vs news-supported split (flagged in the prior review); consider tightening the no-catalyst stocks intraday bucket specifically.
- **priority:** high
- **first observed:** 2026-07-02 (recurring across prior reviews)

### TODO-swing-report-freshness [MEDIUM] (carried forward, worsening)
- **issue:** Crypto swing report is now stale 23h44m at the overnight slot — worse than 21h34m at the last post-close review. The single daily swing run at ~02:00-05:00 EEST leaves the entire day+overnight window without fresh swing data.
- **evidence:** `data/reports/swing/2026-07-07_02-03_swing_report.md` mtime 05:03 EEST 2026-07-07; cycle logs show `daily_long_horizon_swing_invest: False` for weekday cycles.
- **suggested manual fix:** Evaluate adding a second swing-report run (e.g. ~13:00-14:00 EEST) so afternoon/evening/overnight slots have swing data under 12h old instead of the current ~16-24h blind spot.
- **priority:** medium
- **first observed:** 2026-07-07 18:39 EEST

### TODO-catalyst-mapping-macro-gap [MEDIUM] (new, observed this run)
- **issue:** The night's dominant macro/geopolitical story (US strikes on Iran, Bandar Abbas/Sirik/Qeshm, Strait of Hormuz tanker attacks, oil-sanctions waiver revoked) is present in the raw catalyst feed but every matching row (139 total) is classified generic `other_news` with a null symbol — it is not surfaced as its own basket or geopolitical/macro category, and would be invisible to a review that relied on the catalyst layer alone instead of independent web verification.
- **evidence:** `python` query over `data/catalysts/2026-07-07/catalyst_events.jsonl` for "iran"/"hormuz"/"bandar" → 139 matches, all `catalyst_type=other_news`, `symbol=null`.
- **suggested manual fix:** Add a `geopolitical_macro` catalyst_type category (or basket) keyed on keywords like Iran/Hormuz/sanctions/oil-strike/war, distinct from generic `other_news`, so macro-shock events surface in the structured catalyst layer instead of only in raw text.
- **priority:** medium
- **first observed:** 2026-07-08 04:47 EEST

### TODO-day-folder-rollover-naming [LOW] (new, observed this run)
- **issue:** `data/scheduled_runs/<today>/` and `data/catalysts/<today>/` (literal calendar-date folders) can be effectively empty for several hours after local midnight while the actual freshest scheduler/catalyst data continues to be written under the *prior* day's folder name (a rollover boundary tied to something other than local midnight). A review that strictly checked only the literal `<today>` folder path would have incorrectly deferred or run a redundant catalyst-scan tonight.
- **evidence:** At 04:40 EEST 2026-07-08, `data/scheduled_runs/2026-07-08_default_schedule/` contained only `scheduler.log` (mtime 02:05) with no cycle summaries, while `data/scheduled_runs/2026-07-07_default_schedule/` held the actually-freshest cycle summary (`cycle_06_02-36_summary.md`, mtime 03:01). Same pattern for `data/catalysts/2026-07-08/` (missing) vs `data/catalysts/2026-07-07/` (fresh, mtime 02:50).
- **suggested manual fix:** Clarify/align the scheduler's day-rollover boundary with local midnight, or document the actual boundary so downstream tooling (including this review routine) checks the right folder without needing a fallback scan.
- **priority:** low
- **first observed:** 2026-07-08 04:47 EEST

### TODO-telegram-markdown-underscore-escape [MEDIUM] (new, observed this run — reproducible bug)
- **issue:** `TelegramNotifier.send()` (`src/notifiers/telegram.py`, `send()` default `parse_mode="Markdown"`) sends raw, unescaped text to Telegram's `sendMessage` with Markdown parsing on. Any message containing an odd number of literal underscores (e.g. the filename `OPUS_ENRICHED_REVIEW_LATEST.md`, which this review's own Telegram template is instructed to include) is parsed as an unbalanced italics marker and Telegram rejects the whole message with HTTP 400 "Bad Request" — the send silently fails from the caller's perspective unless the exception text is inspected.
- **evidence:** Reproduced directly this run via `python -m src.cli telegram-test --message "File: OPUS_ENRICHED_REVIEW_LATEST.md"` → `Send failed: 400 Client Error: Bad Request`. Wrapping the same filename in backticks (`` `OPUS_ENRICHED_REVIEW_LATEST.md` ``, a balanced code-span) sends successfully. All other message blocks (Mood/Status/Decisions/Risk/Catalyst) sent fine standalone; only the block containing the bare filename failed.
- **suggested manual fix:** Either (a) escape Markdown special characters (`_`, `*`, `` ` ``, `[`, `]`) in `TelegramNotifier.send()` before submitting when `parse_mode="Markdown"`, or (b) switch default `parse_mode` to `"MarkdownV2"` with proper escaping, or (c) simplest — have callers wrap literal filenames/identifiers in backticks before calling `send()`. This run worked around it by wrapping the filename in backticks in the outgoing message; future scheduled runs should do the same until the notifier itself is fixed, since this could otherwise have been silently degrading previous scheduled sends whenever a message happened to contain an odd count of underscores.
- **priority:** medium
- **first observed:** 2026-07-08 04:52 EEST
