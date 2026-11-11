# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

## 1. Executive Summary

**Crypto overnight / Asia-session review, 04:39 EEST (01:39 UTC) — stocks closed, crypto is the only live actionable class. Advisory only — no auto-trade.** Crypto regime is unchanged from the post-close review: bullish-trend/risk-on structure (BTC transition_up, ETH uptrend, altcoin breadth 65–70% above EMA20/50), but macro risk stays elevated (70–80/100, risk-off headwind) on Iran/Strait-of-Hormuz war headlines layered under the tape — treat the "bullish" label as short-term structure, not a green light to size up. No A-tier crypto or stocks setup exists. The only fresh actionable ideas are two no-catalyst B-tier intraday longs, **GPS/USDT** and **HEMI/USDT**, both `waiting_for_entry` essentially at their pullback zones (both are also already-triggered swing positions from earlier cycles, so a fresh add would be pyramiding an existing book position, not a new independent bet). Stocks show **zero A/B actionable** — the entire 15-name A-tier long cohort (XOM, AMGN, COP, LRCX, GE, CRCL, MRVL, PYPL, ASML, SMH, MU, GILD, TSM, INTC, VRTX) is correctly demoted to C by the market-closed gate; re-evaluate at the 09:30 ET open. **Catalyst mapping is weak this run** (66.8% of today's 500 events unmapped) — treat catalysts as context, not decision input. **TODO-1 (6-symbol crypto OHLCV freeze: HOLO, AVNT, PROM, LUNA, MMT, BABY) is now ~54h stale, unresolved for a 7th+ consecutive cycle** — these are live swing positions being tracked on frozen data, escalating. TODO-2 (duplicate signal_id rows) persists on historical stocks rows. **TODO-4 (stale tier classification on active-signals) is now RESOLVED** — GE/INTC current rows correctly show tier=C. Best long-watch: **GPS/USDT** (RS-leader, near entry). Best short-watch: **XMR/USDT** (weak-RS, ready-for-promotion short, needs bearish HTF confirmation). No catalyst-backed candidate is clean — two fresh narrative baskets (ai_narrative, binance_ecosystem_teaser) exist but no B-tier idea maps to either yet. Avoid new exposure to **BTC/USDT** pending resolution of its active exploit_hack/data-breach operator-review flags.

## 2. Data Used

- Scheduler: `data/scheduled_runs/2026-08-17_default_schedule/scheduler.log` (mtime 03:45:57 EEST, ~54min old — fresh). Latest `cycle_03_02-01_summary.md` (same mtime).
- Reports: scalp `2026-08-17_23-32` (mtime 02:32 EEST, ~2h07m old — clean no-trade, scalp mode disabled by kill-switch), intraday `2026-08-18_00-03` (mtime 03:03 EEST, ~1h36m old — fresh, GPS/HEMI B-tier), swing `2026-08-17_20-51` (mtime 23:51 EEST 2026-08-17, ~4h48m old — **carry-forward**, 4–12h band), stocks intraday `2026-08-18_00-31` (mtime 03:31 EEST, ~1h08m old — fresh, market-closed demotion active, all planning-only), stocks swing/invest `2026-07-02` (6+ weeks stale — expected, these playbooks are deprecated/removed).
- Catalysts: `data/catalysts/2026-08-18/catalyst_events.jsonl` (mtime 03:07 EEST, 500 events today), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_00-07.md`.
- CLI/direct-query: `active-signals --asset-class crypto` (n=50, 0 A-tier), `active-signals --asset-class stocks` (0 A/B actionable, all C), `signal-stats --asset-class crypto` (week: tier B n=83, PF 2.47, avgR 0.36, winrate 17.7%; by mode: swing PF 4.60/n46 strong, intraday PF 0.86/n24 weak-negative, scalp PF 0.50/n13 weak-negative), `detect_untracked_legacy_alerts --since 2026-08-18` → **clean, no untracked alerts**.
- Direct SQLite reads (`proposed_signals`, `news_items`) for current tier/status per symbol (active-signals CLI columns truncate too aggressively to be reliable standalone this cycle — cross-checked against direct queries).
- Direct file check: `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY,WLFI,CHIP,ETH}_USDT.csv` last-row timestamps — reconfirms the same 6-symbol freeze at `2026-08-15 22:30:00+00:00`; controls (WLFI, CHIP, ETH) fresh.
- Direct catalyst-file parse: `catalyst_events.jsonl` — 500 total / 166 mapped (33.2%) / 334 unmapped (66.8%).
- Prior review for comparison: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-17_2330.md` (post-close final daily review, 23:30 EEST).
- **External web research unavailable this run** (WebSearch/WebFetch tools not exercised — all candidates resolved from internal data with no stale/contradictory internal record requiring external verification per §G discipline; none of tonight's verdicts critically depend on external confirmation).

## 3. Scheduler / Data Freshness

- Scheduler fresh (mtime ~54min old, well under the 3h defer threshold).
- **TODO-1, confirmed again this cycle:** the same 6 crypto symbols (HOLO, AVNT, PROM, LUNA, MMT, BABY) remain frozen on 15m OHLCV at `2026-08-15 22:30:00 UTC` (~54h stale). Control symbols WLFI/CHIP/ETH are fresh (today's rows). All 6 are underlying live swing book positions per §7d discussion.
- `detect_untracked_legacy_alerts --since 2026-08-18`: **clean** — every legacy crypto alert has a backing proposed_signal.
- **TODO-4 resolved this cycle:** GE and INTC current stocks rows (created 2026-08-18T00:30 UTC, matching the fresh market-closed rescan) correctly show `tier='C'`, `status='waiting_for_entry'` — no stale A/B classification observed. The only remaining rows tagged tier='A' for GE are historical `tp1_hit` closes from 2026-08-17, which is expected archive behavior, not a live misclassification.
- **TODO-2, still present:** duplicate signal_id rows persist on historical/closed stocks positions (e.g., GE tier=A `tp1_hit` ×3, AMZN tier=B `tp1_hit` ×3, SMH tier=B `tp1_hit`/`tp2_hit` ×2–3, plus ~30 more C-tier groups). All duplicates observed this cycle are on already-resolved statuses (`tp1_hit`/`tp2_hit`), not on currently-open positions — lower urgency than when it affected `waiting_for_entry` rows.
- Swing crypto report (`2026-08-17_20-51`) is carry-forward (4h48m old, inside the 4–12h band) — used with that caveat; the intraday/scalp reports are fresh.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-18 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "onchain_config_missing"],
      "data_missing": ["6 crypto OHLCV symbols frozen ~54h", "stocks swing/invest 6wk+ stale (expected/deprecated)", "crypto swing report in 4-12h carry-forward band"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~54min old, well fresh", "crypto-intraday and crypto-scalp both refreshed within ~2h", "6-symbol OHLCV freeze confirmed again at 2026-08-15 22:30 UTC, controls fresh"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.6,
      "reason_codes": ["risk_on", "longs_preferred", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC transition_up, ETH uptrend, altcoin breadth 65-70% above EMA20/50, desk regime label bullish trend/risk-on", "macro risk score 70.4-79.5/100 (risk-off headwind) from Iran/Strait-of-Hormuz war headlines, 5-6 risk-off hits vs 2 risk-on hits", "stocks: closed (after-hours UTC), all planning-only, VIX 15.19, breadth 100% above EMA20/50 as last recorded"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["500 catalyst events today, 66.8% unmapped (166/500 mapped) - weak mapping, context only", "2 fresh narrative baskets <6h: ai_narrative (NEAR/RENDER/TAO/FET) and binance_ecosystem_teaser (BNB) - no B-tier idea currently maps to either", "GPS/HEMI/EDEN/ACE all explicitly 'no fresh verified catalyst detected' per their own report evidence, despite ACE carrying a 'catalyst_backed' discovery-agent source tag with zero matching news_items in 24h - flagged as a labeling inconsistency, see TODO"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.45,
      "reason_codes": ["data_unavailable", "funding_extreme", "oi_contradicts"],
      "data_missing": ["OI 24h% n/a for all fallback-derivatives symbols (GPS, HEMI, ACE, EDEN)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["GPS/USDT: funding slightly negative to neutral across bybit/mexc, crowding low-to-elevated depending on report vintage", "HEMI/USDT: funding neutral, crowding normal-to-elevated", "ACE/USDT: funding notably negative across venues (bybit -0.0016 to -0.0047, mexc -0.002 to -0.003), crowding elevated - shorts are paying to be short, some short-squeeze-risk backdrop even though ACE itself is scored long"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_fresh", "clean_retest", "chase_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["GPS/USDT intraday: current price 0.0165 vs pullback zone 0.0158-0.0163, essentially at the top of zone (~0.0002 away, well under 1 ATR of 0.0012) - low chase risk", "HEMI/USDT intraday: current price 0.0069 sits inside its 0.0067-0.0069 pullback zone - effectively at entry now", "GPS 24h move +49.9% to +62.0% depending on report vintage - a large recent move even though current entry proximity is clean; the 7d return context (+71-75%) argues this is a strong/extended trend, watch for exhaustion"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.6,
      "reason_codes": ["waiting_for_entry", "open_actionable", "no_entry"],
      "data_missing": ["schema has no clean 'entered-unresolved past validity window' status distinct from 'triggered'; treated triggered=open/in-progress"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 2 B-tier waiting_for_entry (GPS, HEMI intraday), 23 B-tier triggered/open (swing book, spanning 2026-08-11 to 2026-08-18), 0 A-tier anywhere", "stocks: 18 waiting_for_entry, all tier=C (market-closed demotion), 0 A/B actionable", "6 of the crypto triggered book's open positions (HOLO, AVNT, PROM, LUNA, MMT, BABY) run on the frozen OHLCV feed - needs_review"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC: active exploit_hack risk flags (Coldcard exploit, Galaxy Research estimate 1,778-2,055 BTC stolen across 3+ waves) plus a separate data-breach flag (250k crypto users) - both block_requires_operator_review, carried across scalp/intraday/swing reports", "stocks: HD and PANW have earnings today (2026-08-18) - do_not_chase_warning, moot tonight since market is closed but carries into the NY morning", "macro risk 70-80/100 risk-off headwind from ongoing Iran/Strait-of-Hormuz war headlines layered under an otherwise-bullish crypto structure read"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B week: sample=83, PF 2.47, avgR 0.36, totalR +23.6, winrate only 17.7% - edge is a small-winrate/big-avg-winner profile, not a high-hitrate one", "by mode: swing PF 4.60/n46 (edge concentrated here), intraday PF 0.86/n24 (net-negative), scalp PF 0.50/n13 (net-negative, and now kill-switch disabled entirely)", "stocks all-tier week: PF 0.269, totalR -9.50, winrate 8.8% - the market-closed/guard demotions on stocks A-tier longs are evidence-based, not overcautious"] },
    { "agent": "head_trader", "verdict": "advisory_synthesis_only", "confidence": 0.6,
      "reason_codes": [], "data_missing": [], "suggested_effect": "advisory_only",
      "facts_used": ["see section 8 below"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "GPS/USDT", "trigger": "already at/near pullback zone 0.0158-0.0163 (current ~0.0165); RS-leader tag (momentum 91.6, RS vs BTC +47-60%), no-catalyst intraday cohort so keep size small and require the zone to hold, not chase above 0.0175 resistance" },
    "best_short_candidate":    { "symbol": "XMR/USDT", "trigger": "discovery-agent 'ready-for-promotion' weak_rs_short (RS vs BTC -4.8% to -8.8%, score up to 76 in some report vintages); needs bearish HTF structure confirmation + a derivatives read + a stop clearly above the swing high before treating as more than a watch idea" },
    "best_catalyst_candidate": { "symbol": "none this window", "trigger": "watch ai_narrative (NEAR/RENDER/TAO/FET) and binance_ecosystem_teaser (BNB) baskets for an RS-leader breakout with volume confirmation - neither basket has a scored B-tier idea yet" },
    "avoid_candidate":         { "symbol": "BTC/USDT", "reason": "active exploit_hack (Coldcard, up to ~2,055 BTC estimated stolen) and separate data-breach operator-review flags; do not treat as a clean new long even though the fresh-catalyst framing elsewhere is constructive" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, onchain_config_missing | advisory_only |
| market_regime | mixed | 0.60 | risk_on, longs_preferred, chop | advisory_only |
| catalyst_narrative | caution | 0.45 | mapping_weak, fresh_catalyst, narrative_supported, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.45 | data_unavailable, funding_extreme, oi_contradicts | advisory_only |
| technical_entry | caution | 0.55 | entry_fresh, clean_retest, chase_risk | advisory_only |
| execution_lifecycle | needs_review | 0.60 | waiting_for_entry, open_actionable, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | advisory_synthesis_only | 0.60 | — | advisory_only |

## 4. What Changed vs Previous Review (vs 23:30 EEST post-close final daily review)

- **Resolved:** TODO-4 (stale tier classification on active-signals) — GE/INTC current rows now correctly show tier=C after the fresh market-closed rescan. No stale A/B rows observed this cycle.
- **Unchanged/escalating:** TODO-1, the 6-symbol crypto OHLCV freeze (HOLO, AVNT, PROM, LUNA, MMT, BABY), now confirmed for a 7th+ consecutive cycle (~54h stale, up from ~50h at 23:30).
- **Unchanged:** TODO-2, duplicate signal_id rows — still present, but now confirmed to be confined to already-resolved (`tp1_hit`/`tp2_hit`) historical rows rather than live `waiting_for_entry` positions.
- **New this cycle:** stocks flips from "one fresh actionable idea (UBER short, waiting_for_entry)" at 23:30 to **zero A/B actionable** now — the fresh 00:31 EEST rescan demotes UBER (and everything else) to C under the market-closed gate. This is the expected overnight state, not a regression.
- **Unchanged:** GPS/USDT and HEMI/USDT remain the desk's only fresh crypto B-tier ideas, same no-catalyst-cohort caveat as 23:30; swing-tier versions of both symbols continue to hold as triggered positions from earlier cycles.
- **Unchanged:** catalyst mapping remains weak (66.8% unmapped tonight vs 66.9% at 23:30) — persistent, not a one-off.
- **New this cycle:** flagging ACE/USDT's discovery-agent 'catalyst_backed' source tag against zero matching `news_items` rows in the last 24h — a labeling inconsistency not previously called out in recent reviews (see §14).

## 5. Catalyst Coverage

- Total catalyst events today: **500**. Mapped (non-null symbol): **166 (33.2%)**. Unmapped: **334 (66.8%)**.
- Narrative baskets: **3** (`ai_narrative`, `binance_ecosystem_teaser`, plus one additional basket not yet surfaced in the crypto reports read this cycle).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines (sample): "Enginprime Medical Closes $12M Series A Financing"; "Greenberg Traurig's Marissa A. Neufeld Appointed to Miami Homes For All Board of Directors"; "Aastro Roofing Company Named Deerfield Beach's Roofer of the Year" — all clearly off-topic small-cap/local-business PR noise, not crypto-relevant misses; the unmapped rate looks structural (broad-wire ingestion) rather than a symbol-resolver failure on relevant names.

## 6. Market Landscape

Crypto continues in a short-term bullish-trend structure (BTC transition_up, ETH uptrend, 65–70% of tracked alts above EMA20/50) that has held steady across the last several cycles. Underneath that structure, macro risk stays stubbornly elevated (70–80/100) on an active Iran/Strait-of-Hormuz conflict narrative generating a steady stream of risk-off headlines (oil prices rising on shipping-constraint fears, war-powers-resolution politics, Reuters/AMBCrypto coverage of ETF-outflow softness) — the desk's regime label should be read as "short-term structure permits selective longs," not "macro all-clear." No fresh catalyst is verified for any of the current B-tier crypto ideas; the edge that exists in this book is concentrated in the swing playbook (14d PF ~4.6–5.8) and continues to erode in intraday (PF 0.86) and especially scalp (PF 0.50, now fully disabled by kill-switch). Stocks are closed for the session; nothing here is actionable until 09:30 ET, and the entire scored A-tier stocks-long cohort is (correctly) held to C-tier planning-only status by the market-closed gate.

### Market Mood / Risk Routing
- Crypto mood: **mixed** (bullish short-term structure, risk-off macro headwind)
- Stocks mood: **closed** (after-hours UTC; A-tier long cohort exists but is planning-only until RTH)
- Dominant narrative: no single dominant theme — best-performing symbols (GPS, HEMI, SNXXB) are RS-leader momentum names without verified fresh catalysts; the two fresh narrative baskets (ai_narrative, binance_ecosystem_teaser) have not yet produced a scored idea
- Preferred side now: **longs, selectively** (RS-leaders on pullback), with a standing short-watch on weak-RS names
- Best long candidate: **GPS/USDT** — near/at its intraday pullback zone, RS-leader
- Best short candidate: **XMR/USDT** — ready-for-promotion weak-RS short, needs HTF confirmation before acting
- Best catalyst-backed candidate: **none clean** — watch the two fresh narrative baskets for a scored breakout
- What to avoid: new **BTC/USDT** exposure while its exploit_hack/data-breach flags are active; chasing any of the 15-name stocks A-tier long cohort off stale earlier-cycle context before RTH confirmation
- What would change the view: a scored idea emerging inside `ai_narrative` or `binance_ecosystem_teaser` with volume confirmation; BTC's exploit_hack flag clearing; the 6-symbol OHLCV freeze (TODO-1) resolving

## 7. Candidate Deep Dives

### 1. GPS/USDT — LONG (B-tier, intraday, waiting_for_entry)
- Has price already reacted to the catalyst? No verified catalyst exists; the move (24h +49.9% to +62.0% across report vintages, 7d +71–75%) is pure RS-leader momentum, not news-driven.
- Chasing? Marginal — current price (~0.0165) sits essentially at the top of the stated pullback zone (0.0158–0.0163), within ~0.0002 (well under 1 ATR of 0.0012). Not a fresh chase, but also not a deep pullback.
- Retest/pullback structure? Yes, a shallow one; support sits well below at 0.0121–0.0108 depending on report vintage.
- Overextended (>2 ATR from EMA20)? Not by the entry-zone math above, but the 7d return (+71–75%) argues the broader trend is stretched — treat as a continuation add, not a fresh discovery.
- Would entry now be late? Borderline — acceptable only inside the stated zone, not above 0.0175 resistance.
- What makes it actionable? Holding the 0.0158–0.0163 zone with volume; invalidation on a 1h close beyond 0.0151 (intraday) / 0.0146 (swing).
- Aligned with market mood? Yes — RS-leader long in a still-bullish short-term structure.
- Chase-risk setup? Low-to-moderate given zone proximity, elevated given the 7d extension.
- Catalyst confirmation/contradiction? None — explicitly no-catalyst cohort (14d WR 23%/PF 0.70/−3R for no-catalyst intraday specifically); the swing-mode version of this same symbol carries the stronger edge (14d WR 72%/PF 5.80).
- TradingView / manual chart check unavailable — using only local OHLCV/ATR/EMA fields from the report.

### 2. HEMI/USDT — LONG (B-tier, intraday, waiting_for_entry)
- Has price already reacted to the catalyst? No verified catalyst; 24h +10.7%, 7d +31.5–31.75%, more moderate than GPS.
- Chasing? No — current price (0.0069) sits inside the stated 0.0067–0.0069 pullback zone; effectively at entry already.
- Retest/pullback structure? Yes, clean; support at 0.0060–0.0065.
- Overextended? No — the 7d return is moderate relative to GPS, less stretched.
- Would entry now be late? No, this is close to the cleanest entry-proximity read of tonight's book.
- What makes it actionable? Holding above invalidation (1h close beyond 0.0065 intraday / 0.0065 swing).
- Aligned with mood? Yes — RS-leader long, less extended than GPS.
- Chase-risk? Low.
- Catalyst confirmation/contradiction? None — same no-catalyst intraday cohort caveat as GPS; the swing-tier version already triggered (created 08-14, still open) and carries the stronger swing-mode edge.
- TradingView / manual chart check unavailable.

### 3. EDEN/USDT — LONG (B-tier, swing, triggered/holding)
- Already entered (triggered 2026-08-17 20:51 EEST); entry ~0.04757, stop 0.04528, TP1 0.05101.
- Has price already reacted? No fresh catalyst; 24h +7.98%, 7d +10.29% — modest, not a vertical move, lower chase-risk profile than GPS/HEMI.
- Overextended? No — the most moderate move of the active swing book.
- Aligned with mood? Yes — RS-leader long inside the swing playbook, the strongest-edge mode tonight (14d WR 72%/PF 5.80).
- What would invalidate it? 1h close beyond 0.0453 (below stated stop 0.04528, consistent).
- Chase-risk? Low, already entered at a reasonable level; nothing new to do here besides managing the existing stop.
- Catalyst confirmation/contradiction? None verified.

### 4. ACE/USDT — LONG (B-tier, swing, triggered/holding) — **data-consistency flag**
- Already entered (triggered 2026-08-17 15:43 EEST); entry ~0.1601, stop 0.1452, TP1 0.1780.
- The `DiscoveryExpansionAgent` C-tier watchlist table tags this symbol's source as `catalyst_backed`, but a direct `news_items` query for ACE in the last 24h returns **zero rows**, and every report section for ACE explicitly states "no fresh verified catalyst detected." This is a labeling inconsistency between the discovery-agent source tag and the actual evidence base — not itself a trading risk (ACE is not being treated as catalyst-confirmed anywhere in scoring), but worth a manual look since an operator skimming only the discovery table could be misled into thinking ACE has news support it does not have. See TODO-3 below.
- Funding notably negative across venues (bybit -0.0016 to -0.0047, mexc -0.002 to -0.003) — shorts are paying, some underlying squeeze-prone backdrop even though ACE is scored long; watch for a violent two-way move.
- Overextended? Moderate — 24h +14–20%, 7d +27–38%; trend flagged `transition_down` in one report vintage (technical_setup subscore is the lowest component), a soft internal contradiction worth noting.

### 5. XMR/USDT — SHORT-WATCH (weak_rs_short, ready-for-promotion, not yet an active position)
- Discovery-agent watchlist status: `ready-for-promotion`, RS vs BTC -4.8% to -8.8% across report vintages, score up to 76 in the freshest scan.
- Has price already reacted? Weakness is already visible (24h -2.5% to -5.1%) but not a clean breakdown yet.
- Retest/pullback structure? Not established — this is a watch idea, not a confirmed setup.
- What would make it actionable? Per the playbook's own promotion condition: confirm bearish HTF structure + a usable derivatives read + a stop clearly above the swing high; squeeze-risk guard applies given XMR's typically thin short liquidity.
- Aligned with mood? Only as a tactical short inside an otherwise-long-leaning mood — treat as a hedge/watch idea, not a mood-confirming trade.
- Chase-risk? Low currently since nothing is triggered; the risk is entering before HTF confirmation.

## 8. Best Candidates Ranked

1. **GPS/USDT (long)** — best long-watch; near entry, RS-leader, but no-catalyst intraday cohort caveat applies — keep size small.
2. **HEMI/USDT (long)** — cleanest entry-proximity read tonight, less extended than GPS.
3. **EDEN/USDT (long, holding)** — already entered, lowest chase-risk of the active swing book, strongest-edge mode.
4. **XMR/USDT (short-watch)** — best short candidate available; needs HTF confirmation before treating as more than a watch idea.
5. **ACE/USDT (long, holding)** — already entered; flagged for the catalyst-tag inconsistency, otherwise unremarkable continuation hold.

## 9. Avoid / No Trade (this decision window only)

- **BTC/USDT** — active exploit_hack (Coldcard, up to ~2,055 BTC estimated stolen) and separate data-breach operator-review flags; avoid new long exposure until these clear, regardless of the otherwise-constructive fresh-catalyst framing elsewhere in the reports.
- **New crypto scalp ideas** — mode is kill-switch disabled in production (14d PF 0.50/win 19%, weakest mode); this is a standing config, not a per-cycle call.
- **Stocks A-tier long cohort (XOM, AMGN, COP, LRCX, GE, CRCL, MRVL, PYPL, ASML, SMH, MU, GILD, TSM, INTC, VRTX)** — do not treat as actionable off tonight's planning-only levels; wait for RTH confirmation at 09:30 ET.
- This is a decision-window call only — scanning, tracking, and monitors continue uninterrupted regardless.

## 10. Main Risks

- TODO-1: 6 live swing positions (HOLO, AVNT, PROM, LUNA, MMT, BABY) are being TP/SL-tracked on OHLCV frozen ~54h — if the paper-monitor is reading this frozen file rather than a live price source, exits for these positions could be wrong.
- Macro risk-off headwind (70–80/100) from the Iran/Strait-of-Hormuz conflict is a standing tail risk that could invalidate the desk's short-term-bullish crypto structure read with limited warning.
- BTC exploit_hack/data-breach headline risk could spread sentiment contagion to majors even without a direct symbol-level score impact yet.
- Catalyst mapping at 66.8% unmapped continues to limit how much weight the catalyst layer should carry in any of tonight's calls.
- ACE/USDT's derivatives crowding (negative funding, elevated crowding) sits awkwardly against its long score — a squeeze in either direction is plausible.

## 11. Action Plan — next 4 hours

- Monitor GPS/USDT and HEMI/USDT for entry-zone fills; do not chase above stated resistance (0.0175 / 0.0075 respectively).
- Watch for XMR/USDT HTF confirmation before treating the short idea as more than a watchlist entry.
- Re-check the 6-symbol OHLCV freeze (TODO-1) at the next cycle; escalate to a direct feed-restart investigation if still frozen past 60h.
- Re-evaluate stocks entirely at/after the 09:30 ET open — nothing here is actionable before then.
- Continue monitoring BTC's exploit_hack/data-breach flags for resolution or escalation.

## 12. Final Verdict per Mode

- **Crypto scalp:** disabled (kill-switch), no trade.
- **Crypto intraday:** watch-only / selective — GPS, HEMI near entry, no-catalyst cohort caveat, small size only.
- **Crypto swing:** hold existing book (EDEN, POL, ETH, HEMI, GPS, ACE, ZEC, PUMP, ONG, CHIP, WLFI×2, ETHFI, AVNT, MMT-short, PROM×2, HOLO, ADA-short, LUNA, VELVET, BABY); strongest-edge mode tonight, manage per-position stops; note 6 positions on frozen OHLCV (TODO-1).
- **Stocks intraday/swing/invest:** closed, planning-only; re-evaluate at RTH open.

## 13. Sources

- Internal only this cycle — no external web sources cited. See §2 for internal file/CLI/SQL sources used.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, escalating — 7th+ consecutive cycle)
- **issue:** 6 crypto swing positions (HOLO, AVNT, PROM, LUNA, MMT, BABY) remain open and are being monitored for TP/SL off 15m OHLCV frozen at `2026-08-15 22:30:00 UTC`.
- **evidence:** `data/raw/ohlcv/binance/15m/{HOLO,AVNT,PROM,LUNA,MMT,BABY}_USDT.csv` all last-row `2026-08-15 22:30:00+00:00`, checked 2026-08-18 ~04:39 EEST (~54h stale). Control symbols WLFI/CHIP/ETH fresh (last rows today).
- **suggested manual fix:** investigate the OHLCV ingest/refresh path for this specific symbol set; verify whether the paper-monitor TP/SL logic for these 6 positions is reading this frozen file or a separate live-price source.
- **priority:** high
- **first observed:** 2026-08-17 02:00 EEST (carried through many cycles, now ~54h)

### TODO-2 (carried forward, lower urgency — confined to closed rows)
- **issue:** Duplicate signal_id emission for the same underlying setup continues on stocks — this cycle observed on ~30+ symbol/tier/mode/status groups (e.g., GE tier=A `tp1_hit` ×3, AMZN tier=B `tp1_hit` ×3, SMH tier=B `tp1_hit`/`tp2_hit` ×2–3, LLY, JPM, UNH, XLF, XLV, DIA, NFLX and others).
- **evidence:** direct `proposed_signals` query grouping by (symbol, tier, mode, status) with count>1, 2026-08-18 ~04:39 EEST.
- **suggested manual fix:** investigate the stocks signal-generation path for a dedup gate on symbol+tier+mode+entry-zone within a short time window.
- **priority:** medium (downgraded from the 23:30 review — all observed duplicates this cycle are on already-resolved `tp1_hit`/`tp2_hit` statuses, not on currently-open `waiting_for_entry`/`triggered` rows)
- **first observed:** 2026-08-17 18:40 EEST (recurring, not yet fixed)

### TODO-3 (new this cycle)
- **issue:** the `DiscoveryExpansionAgent` C-tier watchlist table tags ACE/USDT's source as `catalyst_backed`, but a direct `news_items` query for ACE returns zero rows in the last 24h, and every crypto report's own evidence section for ACE states "no fresh verified catalyst detected." Same pattern likely affects other rows tagged `catalyst_backed` in the same watchlist table (BTC, ADA, BNB, CHIP, DOGE were also tagged `catalyst_backed` at low scores with the same "no fresh verified catalyst" language elsewhere in the report) — not independently re-verified for each symbol this cycle.
- **evidence:** `data/reports/intraday/2026-08-18_00-03_intraday_report.md` §7e (Crypto Expansion Watchlist row for ACE/USDT, source=`catalyst_backed`) vs direct `news_items` SQL query (`detected_symbols_json LIKE '%ACE%' AND published_at > -24h` → 0 rows) and the same report's own §6 evidence line for ACE ("Catalyst/news: no fresh verified catalyst detected").
- **suggested manual fix:** clarify what `catalyst_backed` actually means as a `DiscoveryExpansionAgent` source label (e.g., matched a catalyst_events.jsonl row rather than a scored/verified news_items row) and either rename the label or add a footnote distinguishing it from verified catalyst support, so operators skimming the table don't conflate the two.
- **priority:** low-medium (display-only inconsistency, does not affect scoring, tier, or routing)
- **first observed:** 2026-08-18 04:39 EEST

### TODO-5 (new this cycle)
- **issue:** `TelegramNotifier.send()` (`src/notifiers/telegram.py`) defaults `parse_mode="Markdown"`. Sending this cycle's compact review summary through that default returned `HTTP 400 Bad Request` from the Telegram API (message rejected outright); the same message sent with no `parse_mode` (plain text) via a direct API call using the same token/chat_id succeeded immediately. The summary text used ordinary characters (hyphens, slashes, brackets, a bulleted list) with no intentional Markdown — nothing unusual for an auto-generated report.
- **evidence:** first attempt via `TelegramNotifier(...).send(msg)` (default Markdown) → `requests.exceptions.HTTPError: 400 Client Error` on `sendMessage`. Second attempt, identical text, raw `requests.post` to the same `sendMessage` endpoint with `parse_mode` omitted from the payload → `200 OK`, message delivered (message_id 16465). A plain-ASCII control message with default Markdown also failed the same way before the fallback was tried.
- **suggested manual fix:** either default `TelegramNotifier.send()` to no `parse_mode` (plain text) for general-purpose alert bodies, or have the caller pre-escape Markdown special characters before sending; confirm which multi-line report-style callers (this routine, and any other place sending long free-text summaries) are affected.
- **priority:** medium (this cycle's Telegram delivery succeeded via a same-config raw-API fallback, so no message was lost, but the default path is silently failing for this message shape)
- **first observed:** 2026-08-18 04:39 EEST

_TODO-4 (stale tier classification on active-signals, first observed 2026-08-17 21:40 EEST) is RESOLVED this cycle — GE/INTC current rows correctly show tier=C after the fresh market-closed rescan. Not carried forward._
