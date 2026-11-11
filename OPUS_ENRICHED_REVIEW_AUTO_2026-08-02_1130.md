# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:30 EEST

## 1. Executive Summary

Europe / pre-US context review. **Advisory only / no auto-trade.** Today (2026-08-02) is a **Sunday** — US cash markets are closed all day; stocks are pure planning/carry-forward context (last stocks-intraday report 2026-07-31 20:00, stocks-swing/invest 2026-07-02, expected under the deprecated old-stocks-swing framework and the weekend closure, not a freshness fault). Crypto is the only live actionable class this window.

Crypto regime is **range/chop with a downtrend ETH** and macro risk pinned at **100/100 (risk-off)**, though breadth has ticked up slightly since the 04:30 review (~50% above EMA20 vs ~41-42% then) and the Iran-conflict headline mix is now genuinely two-sided (Trump "deal parameters to end Iran war" + "cancels planned military strike" alongside a fresh "Iran threatens regional energy strikes" wire) — read as tentative stabilization, not a confirmed risk-on turn. Scalp, intraday, and swing scans again show **zero fresh A/B setups** this cycle — same structural gap as the last several cycles. The BTC Coldcard hardware-wallet exploit continues spreading (now $88M+ across 4,500 addresses, operator-review flagged).

Five crypto positions remain **OPEN** from earlier cycles: **EPIC/USDT** long (swing) plus a **separate EPIC/USDT intraday B-tier signal still `waiting_for_entry`**, **HOME/USDT** long, **AEVO/USDT** long, **XRP/USDT** short (partial TP booked), and **COTI/USDT** long. COTI remains **direction-contradicted** for a 3rd consecutive review (23:26 → 04:30 → now) — and this cycle's swing snapshot shows its price (0.0146) **already below the position's stated invalidation (0.015355)**, which is new and more serious than the prior two mentions; raised in §14 with priority escalated to **high**. Catalyst symbol-mapping remains weak (56.9% unmapped today) — same recurring gap. Scanning, tracking, and monitors continue regardless of mood; this review recommends selective caution and one manual-review flag, not a pause.

## 2. Data Used

- Reports (crypto):
  - Scalp: `2026-08-02_07-01_scalp_report.md` (generated 10:01 EEST, ~1.6h old) — 0 A/B.
  - Intraday: `2026-08-02_07-07_intraday_report.md` (generated 10:07 EEST, ~1.5h old) — 0 A/B.
  - Swing: `2026-08-02_02-14_swing_report.md` (generated 05:14 EEST, ~6.4h old — **carry-forward**, within the 4-12h window, flagged) — 0 A/B.
- Stocks (weekend, planning-context only, all stale, excluded from actionable verdict):
  - Intraday last generated 2026-07-31 20:00 (market closed since Friday).
  - Swing/invest last generated 2026-07-02 (deprecated old-stocks-swing framework, expected).
- Catalysts: `data/catalysts/2026-08-02/catalyst_cycle_07-09.md` (generated 10:09 EEST, ~1.5h old), `catalyst_events.jsonl` (1,315 cumulative events today, recomputed directly), `narrative_baskets.jsonl` (5 baskets).
- LLM packet: `data/processed/llm_analysis_packet.md` (mtime 10:07 EEST, fresh).
- CLI (read-only, §A.4 whitelist): `active-signals --asset-class crypto` (22 rows), `active-signals --asset-class stocks` (50 rows, planning-context), `signal-stats --asset-class crypto` (week period), `detect_untracked_legacy_alerts --since 2026-08-02` (clean, 0 findings).
- DB (`db/crypto_ai_desk.sqlite`, read-only): `news_items` 24h-freshness checks for ADA, EPIC, HOME, BANK, XRP, MMT and `catalyst_events.jsonl` direct symbol lookup for ADA.
- Scheduler: `data/scheduled_runs/2026-08-01_default_schedule/scheduler.log` (mtime 10:25 EEST) + `cycle_06_09-53_summary.md` (started 09:53, finished 10:25).
- No external WebSearch/WebFetch this cycle — internal records for all 5 candidates were present, recent (mostly <24h or explicitly checked against the 24h window), and internally consistent, so external verification was not triggered per §G. **External web research not attempted this run (not unavailable — simply not needed by policy).**
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-02_0430.md` (crypto overnight / Asia, 04:30 EEST) — see §4.

## 3. Scheduler / Data Freshness

- `scheduler.log` last write 10:25 EEST, ~1h14min before this review — well under the 3h defer threshold. `cycle_06_09-53_summary.md` (last completed cycle) finished 10:25 — also under threshold. **Not deferred.**
- Untracked-alert detector: clean (0 findings) — no PART-1-style integrity regression this cycle.
- Catalyst mapping coverage is **weak (56.9% unmapped, 748/1,315 events today, §5)** — recurring gap, largely Binance leverage-adjustment / futures-announcement headlines the symbol resolver doesn't parse, plus geopolitical wire items with no symbol to map to. Treat the catalyst layer as context, not a final-decision input.
- Swing report is 6.4h old (carry-forward window, not stale) — used with that caveat; scalp/intraday are fresh (~1.5-1.6h).
- **New finding this cycle:** the swing report's own snapshot (05:14 EEST) shows COTI/USDT's current price (0.0146) below its held long position's invalidation level (0.015355) — see §7 and §14. This is a possible stop-execution/tracking lag, not verified further this cycle (read-only constraint); flagged for operator review.
- Only one prior review exists for today (04:30); no earlier 11:xx-slot review to compare against beyond that one.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-02 11:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"],
      "data_missing": [
        "swing report is 6.4h old (carry-forward, not stale)",
        "HOME/USDT current absolute price not directly stated in today's reports (only 24h % return)"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 10:25", "cycle_06_09-53_summary.md completed 10:25", "active-signals crypto 22 rows / stocks 50 rows"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["risk_off", "chop", "mixed", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["intraday report §1: BTC range, ETH downtrend, altcoin breadth 50.0% above EMA20 (up from ~41-42% at 04:30)", "macro risk 100.0/100 risk-off (7 risk-off hits, 0 risk-on, 3 calendar hits)", "mixed Iran headlines: 'deal parameters to end Iran war' + 'cancels planned military strike' vs fresh 'Iran threatens regional energy strikes' wire"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "narrative_supported", "catalyst_confirmed"],
      "data_missing": ["true symbol resolution for 748/1,315 unmapped catalyst_events rows today"],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl recomputed: 1,315 total / 567 mapped / 748 unmapped (56.9%)", "momentum_breakout basket (fresh <1h): ADA/USDT explicitly flagged catalyst-backed (Cardano ecosystem news cluster, all single_source); HOME/USDT and ULTIMA/USDT in the same basket explicitly 'without confirmed catalyst'", "direct catalyst_events.jsonl lookup for ADA: 8 recent 'other_news' items (Leios testnet, RealFi testnet, whale accumulation) — soft ecosystem narrative, single_source, no hard breaking event"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["Bybit/OKX cross-check unavailable for most of today's strongest symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["EPIC/HOME/ADA: price up + OI up, fresh positioning, crowding normal", "SYN/USDT: price down + OI up, funding -0.00299 (deeply negative), fresh shorts pressing / squeeze risk if reclaims", "BANK/MMT/TLM: short squeeze risk capped to C (thin_liquidity + high_upper_wick tags)"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.62,
      "reason_codes": ["entry_late", "chase_risk", "overextended", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ADA/USDT rejected in both scalp and intraday reports: 'Price is more than 2 ATR from EMA20; do not chase'", "HOME/USDT similarly rejected for chase risk despite RS strength", "EPIC/USDT intraday B-tier signal (sig_c6ee879922b6a34b) still waiting_for_entry: entry zone 0.880285-0.903419, current price ~0.8699 (intraday report), i.e. ~0.010 below entry_low vs ATR 0.0297 — within 1 ATR, a genuine near-trigger watch"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "needs_review",
      "confidence": 0.65,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": ["no fresh PAPER_MONITOR_STATUS_LATEST.md-equivalent snapshot read this cycle (not in the §A.4 whitelist); counts below sourced directly from active-signals"],
      "suggested_effect": "advisory_only",
      "facts_used": ["active-signals crypto (22 total): 1 waiting_for_entry (EPIC/USDT intraday), 5 triggered/tp-hit-and-open swing/intraday positions from recent cycles (EPIC swing, HOME swing, AEVO swing, XRP swing, COTI swing), remainder are older tp1/tp2_hit signals from mid-July largely realized/closed-in-substance", "COTI/USDT (sig_06b6c2801005f29d) triggered/open but swing-report snapshot price (0.0146) sits below its stated invalidation (0.015355) — needs_review, not a clean open_actionable"]
    },
    {
      "agent": "risk_manager",
      "verdict": "manual_review",
      "confidence": 0.68,
      "reason_codes": ["headline_risk", "manual_review", "correlation_cluster", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/USDT held long, -9.62% 24h (swing snapshot) and price apparently through its own invalidation level — 3rd consecutive review flagging this, now with a more concrete stop-breach signal", "BTC exploit_hack risk (Coldcard, $88M+, 4,500 addresses, block_requires_operator_review) still active desk-wide", "EPIC/HOME/AEVO longs remain a correlated no-catalyst RS-momentum cluster — a BTC/ETH downdraft would likely hit all three together"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["signal-stats week: headline A/B PF 2.58, avgR 0.461, winrate 25.3% (n=98-99)", "by mode: intraday PF 4.71/avgR 1.30 (n=37, strong); swing PF 2.07/avgR 0.29 (n=42, weaker per-trade but the correlated-longs playbook); scalp PF 0.125/avgR -0.233 (n=19, structurally negative, matches 0 A/B scalp again this cycle)", "by exchange_confirmation: Binance-anchor PF 3.41 vs cross-exchange PF 0.33 — MEXC/cross-exchange-only setups meaningfully weaker"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.66,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.66,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "EPIC/USDT", "trigger": "Intraday B-tier signal still waiting_for_entry, entry zone 0.880285-0.903419, invalidation 0.852011; price is ~0.010 below entry_low (within 1 ATR) — let the entry come to the zone with volume confirmation, do not chase the parallel already-open swing long." },
    "best_short_candidate":    { "symbol": "SYN/USDT", "trigger": "Confirm bearish HTF structure on 15m-1h + break of the recent swing low with OI-supported downside; funding is deeply negative (-0.003) so shorts are already crowded — do not enter without a failed-bounce confirmation and a stop above the swing high." },
    "best_catalyst_candidate": { "symbol": "ADA/USDT", "trigger": "momentum_breakout basket, fresh <1h, catalyst-backed (Cardano ecosystem news cluster) but currently >2 ATR from EMA20 — wait for a pullback into value before treating as more than a watch; do not chase the current print." },
    "avoid_candidate":         { "symbol": "COTI/USDT", "reason": "Held long, direction-contradicted for a 3rd consecutive review, and this cycle's snapshot shows price already through the position's stated invalidation level — flag for immediate manual position review, do not add." },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | caution | 0.70 | risk_off, chop, mixed, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, narrative_supported, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.62 | entry_late, chase_risk, overextended, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.65 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | manual_review | 0.68 | headline_risk, manual_review, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.66 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-02_0430.md` (crypto overnight / Asia, 04:30 EEST, ~7h before this one).

- **New:** COTI/USDT's swing-report snapshot price (0.0146) now sits below its own invalidation level (0.015355) — more serious than the 04:30 review's "direction-contradicted" framing alone; escalated to a high-priority §14 TODO this cycle.
- **New:** Altcoin breadth improved from ~41-42% above EMA20 (04:30) to ~50% (this cycle) — tentative, not a confirmed regime flip.
- **New:** Iran-conflict headline mix is now genuinely two-sided (de-escalation language alongside a fresh "Iran threatens regional energy strikes" wire), vs a one-sided escalation read at 04:30.
- **Unchanged / carried forward:** EPIC/USDT, HOME/USDT, AEVO/USDT swing longs remain OPEN, still RS-leaders, still no fresh catalyst. XRP/USDT short remains OPEN (partial TP booked). EPIC/USDT intraday signal remains `waiting_for_entry` (was already waiting at 04:30; not yet filled ~7h later, expires 2026-08-03T00:51:46).
- **Removed:** none of the 04:30 review's named candidates dropped out of the active book.
- **New catalysts:** ADA/USDT's `momentum_breakout` basket membership is new/fresher this cycle (<1h) vs the 04:30 review where the basket's catalyst-backed member was AKE/BEAT (flagged "without confirmed catalyst").
- **Confirmed:** Catalyst mapping remains weak (56.9% unmapped today vs 59.0% at 04:30) — persistent, marginal improvement only.
- **Invalidated:** none formally, but see COTI above — its long thesis looks practically invalidated on the tape even though the position remains open in the system.

## 5. Catalyst Coverage

- Total `catalyst_events` today (`data/catalysts/2026-08-02/catalyst_events.jsonl`, recomputed directly): **1,315**
- Mapped (non-null symbol): **567** (43.1%)
- Unmapped (null symbol): **748** (56.9%)
- `narrative_baskets`: **5** (binance_ecosystem_teaser/BNB+ASTER, perps_dex_narrative/HYPE+DYDX+GMX+ASTER, ai_narrative/NEAR+RENDER+TAO+FET, delisting_thin_liquidity, momentum_breakout/HOME+ULTIMA+ADA)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top unmapped headlines (sample): "IRAN THREATENS REGIONAL ENERGY STRIKES..." (t.me/WalterBloomberg, geopolitical, no symbol to map to by design) / "#ByBit News: Complete Your First Trade and Earn 40 OPG" (t.me/CexAlerts, promo, unmappable noise) / IAEA Zaporizhzhya power-outage wires (geopolitical, no symbol). Unlike the 04:30 review's sample (mostly parseable Binance leverage-announcement titles), a chunk of today's unmapped volume is genuinely symbol-less macro/geopolitical wire content — the resolver gap is real but partially structural, not purely a parsing bug.

## 6. Market Landscape

BTC range, ETH downtrend, altcoin breadth ~50% above EMA20 (improved from ~41-42% at 04:30 but still not broad participation). Macro/geopolitical risk remains pinned at max (100/100) — the US-Iran situation is now genuinely mixed (de-escalation language from Trump alongside a fresh Iranian energy-strike threat), plus the spreading Bitcoin cold-wallet exploit (~$88M / 4,500 addresses, roughly flat vs 04:30 — possibly stabilizing). A narrow cluster of no-catalyst alts (EPIC, HOME, KAITO, 1000SATS, ULTIMA) continues showing strong RS/momentum inside the chop — same known-negative playbook pattern as prior cycles (no-catalyst intraday chop: 14d WR 23%/PF 0.70), so still low-quality breadth rather than confirmation of a broad risk-on turn.

### Market Mood / Risk Routing

- Crypto mood:           risk-off / chop, tentatively stabilizing (breadth ticking up, headline mix now two-sided)
- Stocks mood:           closed (Sunday; last actionable data Friday, planning-context only; note PLTR earnings tomorrow 2026-08-03 — do-not-chase flag already active in the production risk layer for the next actionable stocks session)
- Dominant narrative:    Momentum-without-catalyst rotation (EPIC/HOME/KAITO/1000SATS/ULTIMA) inside a still-risk-off but stabilizing macro tape
- Preferred side now:    mixed — hold existing RS-leader longs (EPIC/HOME/AEVO), do not chase new longs into the extension; watch SYN/USDT for a confirmed failed-bounce short; watch ADA/USDT for a pullback catalyst-backed long
- Best long candidate:   EPIC/USDT (intraday B-tier `waiting_for_entry`, entry zone 0.880285-0.903419, invalidation 0.852011, price within 1 ATR below entry — a genuine near-trigger watch, not a chase)
- Best short candidate:  SYN/USDT (needs bearish HTF confirmation + break of swing low; funding deeply negative so squeeze-prone until confirmed)
- Best catalyst-backed candidate: ADA/USDT (momentum_breakout basket, fresh <1h, but currently overextended — wait for pullback)
- What to avoid:         COTI/USDT (held long, price apparently through its own invalidation — flag for manual review, do not add); fresh longs on BANK/USDT, MMT/USDT, TLM/USDT, BTW/USDT (all capped C-tier on thin-liquidity short-squeeze risk); fresh entries on ADA/HOME/1000SATS at current price (all >2 ATR from EMA20, chase risk)
- What would change the view: A confirmed US-Iran de-escalation headline (formal ceasefire/deal signing) or BTC reclaiming its local range/downtrend structure would lift the risk-off cap further; a clean failed-bounce + bearish HTF break on SYN would activate the short side; a fill into EPIC's 0.880-0.903 zone with volume would activate the long-watch; a pullback fill on ADA with the catalyst basket still active would activate the catalyst-watch.

## 7. Candidate Deep Dives

### EPIC/USDT (long, intraday B-tier `waiting_for_entry` + separate already-OPEN swing long)

- Has price already reacted to the catalyst? No fresh catalyst — pure RS/momentum (rs_btc_leader, rs_eth_leader, momentum_24h_leader tags across scalp/intraday/swing today).
- Is the setup chasing? For the intraday signal, no — price (~0.8699 per the 10:07 intraday snapshot) is currently *below* the entry zone (0.880285-0.903419), i.e. waiting for the market to come up into the zone, not chasing an extended print.
- Retest/pullback structure? Yes — this is exactly what the waiting_for_entry status represents.
- Overextended (>2 ATR from EMA20)? Not flagged for this specific signal; the separate C-tier EPIC watchlist entry in the intraday report (score 50.6, different conditional zone 0.8506-0.8640) is a lower-conviction duplicate of the same underlying move.
- Would entry now be late? No — price is still below the stated entry zone.
- Actionable level: fill inside 0.880285-0.903419 with volume confirmation; invalidation 0.852011.
- Aligned with market mood? Partially — genuine RS-leader (the strongest playbook, 14d WR 72%/PF 5.80 for `crypto_swing_narrative_rs_momentum`), but still correlated to the broader no-catalyst alt cluster and to a risk-off macro tape.
- Chase risk: low for this specific signal (price is below, not above, the zone).
- Catalyst confirmation/contradiction: none — pure technical/RS thesis, consistent across all three reports today.
- Derivatives: price up + OI up (fresh positioning, not exhausted), funding roughly neutral (5e-05), crowding normal — supportive, not yet crowded.
- Separately, the already-OPEN EPIC/USDT swing long (entry 0.884570-0.905221, invalidation 0.859329) continues to ride the same move — hold, no action needed.

### COTI/USDT (long, OPEN swing position — **escalated: price apparently through invalidation, flag for immediate manual review**)

- Has price already reacted? Yes — the 05:14 EEST swing snapshot shows COTI/USDT at 24h -9.62% (down from -13.99% to -16.61% at 04:30, i.e. the decline has moderated somewhat) but the same snapshot's desk notes for the COTI short-watchlist idea state current price 0.0146, which is *below* the held long position's invalidation of 0.015355.
- Is this a chase-risk setup? N/A — position already held; question is whether it should still be held.
- Retest/pullback structure supporting the long? None — the swing report's own COTI watchlist entry (Trade Idea #7) is framed as a **short** thesis (failed bounce/retest zone 0.0147-0.0150, targets below), directly opposite the held long.
- Overextended? The move is extended against the position, not in its favor.
- Actionable level: none for a fresh long; the existing position needs an operator to verify current live price against 0.015355 and decide hold/close/tighten.
- Aligned with market mood? No — both the macro tape and COTI's own price action argue against the long.
- Catalyst confirmation/contradiction: no fresh (24h) catalytic news found for COTI in `news_items` — this is pure price action, not news-driven, which makes it harder to explain away as noise.
- **Caveat:** this read is based on a 6.4h-old swing snapshot (05:14 EEST); the live price at the time of this review (11:39 EEST) may differ and should be re-verified by an operator before any action — but a snapshot showing price already through the stop, on an open position, is itself the finding worth surfacing regardless of the current live number.

### ADA/USDT (best catalyst-backed watch, not yet actionable — overextended)

- Has price already reacted to the catalyst? Yes — 24h +8-10% across today's reports, RS +8-9% vs BTC, and the `momentum_breakout` narrative basket (fresh <1h) explicitly tags ADA as catalyst-backed (as opposed to HOME/ULTIMA in the same basket, which are flagged "without confirmed catalyst").
- Is the setup chasing? Yes, at current price — both scalp and intraday reports reject ADA for "Price is more than 2 ATR from EMA20; do not chase."
- Retest/pullback structure? Not given a specific numeric zone in today's reports (ADA converted to watchlist-only, "wait for pullback," no explicit levels published).
- Catalyst quality: soft — direct `catalyst_events.jsonl` lookup for ADA shows a cluster of ecosystem news (Leios testnet launch, RealFi testnet, "why is ADA up 15% this week" explainer pieces), all `single_source`, `other_news` type — a real narrative but not a hard, verified, high-importance event.
- Aligned with market mood? Partially — it's the cleanest catalyst-tagged mover today, but the catalyst itself is soft and the entry is currently late.
- Would invalidate: a reversal below the recent breakout structure or the basket losing its "fresh <1h" status without a pullback fill.
- Chase risk: high at current price; this is a watch, not an active idea.

### HOME/USDT (long, OPEN swing position)

- Same profile as EPIC: no-catalyst RS/momentum long (24h +30-33% across today's reports, RS +29-32% vs BTC), filled on an earlier pullback, currently extended for **new** entries (rejected in both scalp and intraday reports for "Price is more than 2 ATR from EMA20; do not chase").
- Derivatives: price up + OI up (fresh positioning), funding slightly negative (-3.8e-05 to -6.7e-05, shorts mildly crowded, supportive for the long), crowding normal.
- No fresh (24h) catalyst news found for HOME in `news_items` — consistent with the momentum_breakout basket's "without confirmed catalyst" tag for this symbol.
- Current absolute price not directly stated in today's reports (only 24h %); position status (hold, no add) is unaffected by this gap since no fresh entry is being considered.
- Aligned with mood: same caveat as EPIC — correlated no-catalyst alt-rotation risk if BTC breaks down; hold, don't add at current price.

### SYN/USDT (best short-watch, not yet actionable)

- 24h -13.7% to -14.0% across today's reports (moderated slightly from -14.0% to -14.5% at 04:30), `weak_rs_short` tag, capped to C-tier by `thin_liquidity_short_squeeze_risk` + `high_upper_wick_short_squeeze_risk` — funding deeply negative (-0.00299), meaning shorts are already crowded and a bounce could squeeze hard.
- Not actionable as-is: needs confirmed bearish HTF structure + a clean break of the recent swing low with a stop above the swing high before entry.
- Catalyst confirmation/contradiction: none found today; purely technical/RS-driven, same category as the long-side movers but in reverse.

## 8. Best Candidates Ranked

1. **EPIC/USDT** (intraday, waiting_for_entry — best long-watch) — cleanest, most concrete trigger of the cycle: price sits within 1 ATR below a defined entry zone on the desk's strongest playbook.
2. **EPIC/USDT / HOME/USDT / AEVO/USDT** (swing, OPEN — hold) — same RS-leader profile, no fresh catalyst, currently extended for adds; hold as-is.
3. **XRP/USDT** (swing, OPEN short, partial TP booked) — cleanest short expression of the risk-off macro thesis, already de-risked.
4. **ADA/USDT** (catalyst-watch, not yet actionable) — best catalyst-backed name today, but overextended; wait for pullback.
5. **SYN/USDT** (short-watch, not yet actionable) — best short candidate pending bearish HTF + swing-low-break confirmation; squeeze-prone until then.

**COTI/USDT is explicitly excluded from this ranked list** — see §9 and §14; it is a manual-review item, not a ranked candidate.

No fresh A/B this cycle. Best long-watch = EPIC/USDT intraday entry zone (see above). Best short-watch = SYN/USDT pending confirmation. Best catalyst-watch = ADA/USDT pending a pullback.

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and monitors continue regardless.

- **COTI/USDT** — avoid adding; existing long shows a snapshot price through its own invalidation level; flag for immediate manual position review (§14, priority raised to high).
- **BANK/USDT, MMT/USDT, TLM/USDT, BTW/USDT** — short-squeeze risk (thin liquidity + high upper wick), capped to C-tier; do not short without confirmation.
- **ADA/USDT, HOME/USDT, 1000SATS/USDT, SOXLB/USDT** — >2 ATR from EMA20, explicit chase-risk flags in today's rejected lists; do not chase fresh entries.
- No clean fresh long or short clears the A/B bar this cycle — this applies to the current window only, not a system pause.

## 10. Main Risks

- **COTI position integrity**: a snapshot showing an open long trading through its own invalidation level is the most concrete operator-attention item this cycle — needs verification against live price, not just a "direction-contradicted" narrative flag as in the last two reviews.
- **Macro/geopolitical**: US-Iran situation remains genuinely two-sided (de-escalation language vs a fresh energy-strike threat) — still a live tail risk, not yet resolved either direction.
- **Correlation cluster**: EPIC/HOME/AEVO are all no-catalyst RS-momentum longs in the same rotation — a single BTC/ETH downdraft would likely hit all three together.
- **Catalyst mapping at 56.9% unmapped**: reduces confidence in "no fresh catalyst" reads generally, though a meaningful share of today's unmapped volume is inherently symbol-less geopolitical wire content rather than a pure parsing failure.
- **Squeeze risk on the short side**: SYN/BANK/MMT/TLM all carry crowded-funding squeeze risk; a short without confirmation risks a violent reclaim.
- **BTC exploit_hack**: Coldcard-related theft continues (~$88M/4,500 addresses), operator-review flagged desk-wide.

## 11. Action Plan — next 4 hours

1. **Flag COTI/USDT swing long for immediate manual review** — verify live price against invalidation (0.015355) and decide hold/tighten/close (§14 TODO, priority raised to high this cycle).
2. Hold EPIC/HOME/AEVO/XRP swing positions as-is; no new entries unless price returns to stated pullback/entry zones with volume confirmation.
3. Watch the EPIC/USDT intraday signal (waiting_for_entry, entry 0.880285-0.903419) — the cleanest concrete trigger this cycle; let it come to the zone.
4. Watch SYN/USDT for a confirmed bearish HTF break before considering a short entry.
5. Watch ADA/USDT for a pullback entry while the momentum_breakout catalyst basket remains fresh (<1h window closing).
6. Monitor US-Iran headlines into the US-open review (16:20 slot) — a formal de-escalation or a fresh escalation would materially change the risk-off routing either direction.
7. Continue scanning/tracking/monitoring uninterrupted — no pause recommended.

## 12. Final Verdict per Mode

- **Scalp**: No trade. Structurally weak playbook (14d PF 0.14 per report banner); 0 A/B this cycle.
- **Intraday**: No trade for fresh entries. 1 signal waiting_for_entry (EPIC/USDT) — best watchlist name BEAT/USDT at 58.0/100, not actionable.
- **Swing**: Hold existing RS-leader longs (EPIC, HOME, AEVO) and the XRP short; no fresh entries. **COTI long flagged for immediate manual review** (escalated from "monitor" to "manual review required" this cycle).
- **Stocks (all modes)**: Closed (Sunday) — planning/carry-forward context only, no verdict. Note PLTR earnings 2026-08-03 for the next actionable session's do-not-chase handling.

## 13. Sources

- Internal only this cycle (no external WebSearch/WebFetch triggered — see §2 and §G rationale):
  - `data/catalysts/2026-08-02/catalyst_cycle_07-09.md`, `catalyst_events.jsonl`, `narrative_baskets.jsonl`.
  - `news_items` table, direct queries for ADA/EPIC/HOME/BANK/XRP/MMT (24h window).
  - `data/reports/scalp/2026-08-02_07-01_scalp_report.md`, `data/reports/intraday/2026-08-02_07-07_intraday_report.md`, `data/reports/swing/2026-08-02_02-14_swing_report.md`.
  - `active-signals`/`signal-stats` CLI outputs (crypto + stocks), `detect_untracked_legacy_alerts` CLI output.

## 14. Fix Requests / TODO

### TODO-coti-invalidation-breach
- **issue:** COTI/USDT is held as an OPEN swing long (`sig_06b6c2801005f29d`, entry 0.016109-0.016726, invalidation 0.015355) but the same-day swing report's own snapshot (05:14 EEST) shows COTI/USDT current price at 0.0146 — below the stated invalidation level — while the signal status remains `triggered` (open), not stopped/closed. This is the 3rd consecutive review to flag COTI's direction-contradiction (23:26 → 04:30 → 11:30), and the first to observe price apparently through the stop.
- **evidence:** `active-signals --asset-class crypto` (status=triggered, invalidation=0.015355); `data/reports/swing/2026-08-02_02-14_swing_report.md` Trade Idea #7 Desk Notes ("Current price: 0.0146"); same report §2 "Weakest Symbols" listing COTI/USDT at -9.62% to -10.10% RS; `news_items` query showing 0 fresh (24h) catalytic news for COTI.
- **suggested manual fix:** An operator should immediately verify COTI/USDT's live price against the position's invalidation level and decide whether to hold, tighten, or close — and separately, engineering should check whether the stop/invalidation-monitoring job is running correctly for this signal (whether it's a genuine tracking lag or the snapshot price was transiently stale).
- **priority:** high (escalated from medium — this is now a position-integrity question, not just a direction-contradiction narrative)
- **first observed:** 2026-08-01 23:26 EEST (this is the 3rd consecutive cycle to flag it; escalated this cycle)

### TODO-catalyst-mapping-weak-recurring
- **issue:** Catalyst symbol-mapping has been >50% unmapped for multiple consecutive review cycles (57.3% → 59.0% → now 56.9%), a mix of unparsed Binance announcement templates and inherently symbol-less geopolitical/macro wire content.
- **evidence:** direct recomputation of `data/catalysts/2026-08-02/catalyst_events.jsonl` (1,315 total / 567 mapped / 748 unmapped); sample unmapped titles today include both promo noise ("#ByBit News: Complete Your First Trade...") and geopolitical wires (IAEA Zaporizhzhya power-outage reports) with no symbol to map to by design.
- **suggested manual fix:** Improve the catalyst symbol resolver for the parseable subset (Binance leverage-adjustment / futures-announcement templates), and consider adding a "structurally symbol-less" classification (promo/geopolitical-macro) so the unmapped % metric doesn't conflate genuine resolver gaps with content that was never going to map to a symbol.
- **priority:** low (context-only impact, does not gate scoring/routing)
- **first observed:** recurring across multiple prior reviews (at least 2026-07-31 21:45 onward); still open.
