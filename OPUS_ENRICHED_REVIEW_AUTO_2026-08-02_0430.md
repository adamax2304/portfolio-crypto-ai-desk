# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

Crypto overnight / Asia session review. **Advisory only / no auto-trade.** Today
(2026-08-02) is a **Sunday** — weekend mode, crypto-only; US cash markets are
closed and stocks are pure planning/carry-forward context (last stocks-intraday
report 2026-07-31 20:00, stocks-swing/invest 2026-07-02 — expected under the
weekend/deprecated-old-stocks-swing framework, not a freshness fault). Crypto
is the only live actionable class tonight.

BTC and ETH remain in **downtrend / range-chop**, macro risk is pinned at the
**max 100/100 (risk-off)**, and this is corroborated by external verification
tonight (see §13): the US-Iran conflict remains in active escalation with no
de-escalation signal — new US strikes on multiple Iranian provinces, Kuwait
intercepting Iranian drones, damaged vessels off Oman, and the Strait of
Hormuz partially blockaded (energy-market risk). Bitcoin itself is down
~3.25% over the trailing 24h per external sources, consistent with the local
downtrend read. Despite this, a cluster of alts (**EPIC, KAITO, HOME, AEVO,
BEAT, AKE**) is showing strong, catalyst-free RS/momentum — classic
low-quality breadth in a risk-off tape (the "no-catalyst intraday in chop"
playbook is structurally net-negative at 14d WR 23% / PF 0.70). Fresh scalp,
intraday, and swing scans all show **zero fresh A/B setups** again tonight —
same structural gap as prior cycles.

Five crypto swing positions are **OPEN** from earlier cycles and riding
tonight's move: **EPIC/USDT** long, **HOME/USDT** long, **AEVO/USDT** long,
**XRP/USDT** short (partial TP booked, runner open), and **COTI/USDT** long —
the last of which remains **technically contradicted** (held long, but
24h return is -14% to -17% and it carries a `weak_rs_short` discovery tag;
same unresolved flag as the last several cycles, now several cycles old,
raised to §14 TODO). Catalyst symbol-mapping is weak again (59.0% unmapped
today) — same recurring gap as prior cycles. Scanning, tracking, and monitors
continue into the Asia session regardless of mood; this review recommends
selective caution, not a pause.

## 2. Data Used

- Reports (crypto, weekend cycle 3, all fresh):
  - Scalp: `2026-08-02_01-34_scalp_report.md` (mtime 04:34 EEST, ~5min old) — 0 A/B.
  - Intraday: `2026-08-01_23-09_intraday_report.md` (mtime 02:09 EEST, ~2.5h old) — 0 A/B.
  - Swing: `2026-08-01_20-49_swing_report.md` (mtime 23:49 EEST, ~4.9h old — carry-forward, within 4-12h window) — 0 A/B.
- Stocks (weekend, planning-context only, all stale, excluded from actionable verdict):
  - Intraday last generated 2026-07-31 20:00 (market closed since Friday).
  - Swing/invest last generated 2026-07-02 (deprecated old-stocks-swing framework, expected).
- Catalysts: `data/catalysts/2026-08-01/catalyst_cycle_23-11.md` (mtime 02:11 EEST, ~2.5h old — day-boundary is UTC so "today" folder is still `2026-08-01`), `catalyst_events.jsonl` (1,449 cumulative events, recomputed directly), `narrative_baskets.jsonl` (5 baskets).
- LLM packet: `data/processed/llm_analysis_packet.md` (mtime 04:35 EEST, fresh).
- CLI (read-only, §A.4 whitelist): `active-signals --asset-class crypto` (22 rows), `signal-stats --asset-class crypto` (week period), `detect_untracked_legacy_alerts --since 2026-08-02` (clean, 0 findings).
- DB (`db/crypto_ai_desk.sqlite`, read-only): `news_items` 24h-freshness checks for EPIC, KAITO, HOME, AEVO, COTI, XRP, BEAT.
- Read-only artifacts (~2.2h old, carried forward as best-available): `reports/CONTEXT_FILTERS_STATUS.md` (02:23), `reports/OPEN_INTRADAY_LIFECYCLE_REVIEW.md` (02:24), `reports/PAPER_MONITOR_STATUS_LATEST.md` (02:25).
- Scheduler: `data/scheduled_runs/2026-08-01_default_schedule/scheduler.log` (mtime 04:35, live) + `cycle_03_01-54_summary.md` (started 01:54, finished 02:27, 56/56 steps OK).
- External web research (per §G, macro driver critical): 1 WebSearch + 1 WebFetch — Al Jazeera Iran-conflict status (verified, primary_source) + CoinGabbar Aug-1 market recap (single_source). See §13.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-01_2326.md` (post-close, 23:26 EEST) — see §4.

## 3. Scheduler / Data Freshness

- `scheduler.log` last write 04:35 EEST, well under the 3h defer threshold. `cycle_03_01-54_summary.md` (last completed cycle) finished 02:27, ~2h12min before this review — also under threshold. **Not deferred.**
- Cycle 3 (weekend, crypto-only, stocks disabled) completed clean: 56/56 steps OK, 0 failed. Track-signals pre-pass: checked=183, tp_hits=128, stopped=0, expired=0, not_triggered=50 — no losses this pass.
- Untracked-alert detector: clean (0 findings) — no PART-1-style integrity regression.
- Catalyst mapping coverage is **weak (59.0% unmapped, 855/1,449 events, §5)** — same recurring "Maximum Leverage Adjusted for X Futures" Binance-announcement parsing gap flagged in prior cycles. Treat the catalyst layer as context, not a final-decision input.
- Lifecycle artifacts (`PAPER_MONITOR_STATUS_LATEST.md`, `OPEN_INTRADAY_LIFECYCLE_REVIEW.md`, `CONTEXT_FILTERS_STATUS.md`) last regenerated ~02:23-02:25, ~2.2h before this review (cycle 3 doesn't appear to include these steps in the weekend/crypto-only path per the 56-step list above) — carried forward as best-available, flagged `data_missing` for `execution_lifecycle`.
- Minor data point (not elevated to a bug): `active-signals --asset-class crypto` shows `sig_c6ee879922b6a34b` (EPIC/USDT intraday, B) as `waiting_for_entry`, but the ~2.2h-old `PAPER_MONITOR_STATUS_LATEST.md` snapshot shows `WAITING_FOR_ENTRY=0` desk-wide. Likely just monitor-artifact staleness (that intraday signal may postdate the 02:23-02:25 snapshot) — not verified further this cycle, low priority.
- `OPEN_INTRADAY_LIFECYCLE_REVIEW.md` shows 11 stocks C-tier "needs review" carryovers held ~293-297h (~12.3 days) — these are all pre-existing artifacts from the deprecated old-stocks-intraday framework (per project history, C-tier is never Telegram-actionable) and stocks are closed this weekend regardless; not a fresh finding.
- No `OPUS_ENRICHED_REVIEW_AUTO_*.md` exists yet for the earlier part of today (2026-08-02) — this is the first review of the day (04:30 slot), so that is expected, not a gap.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-08-02 04:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"],
      "data_missing": [
        "lifecycle artifacts (PAPER_MONITOR_STATUS_LATEST.md etc) ~2.2h stale, not regenerated in the weekend crypto-only cycle path",
        "EPIC/USDT intraday waiting_for_entry vs PAPER_MONITOR WAITING_FOR_ENTRY=0 count mismatch, unresolved, low priority"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 04:35", "cycle_03_01-54_summary.md 56/56 OK", "active-signals crypto 22 rows"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.82,
      "reason_codes": ["risk_off", "chop", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scalp/intraday report §1: BTC/ETH downtrend, range/chop, altcoin breadth 41-42.5% above EMA20", "macro risk 100.0/100 risk-off (6 risk-off hits, 0 risk-on)", "external verification: Al Jazeera — active US strikes on 5+ Iranian provinces, Strait of Hormuz partially blockaded, no de-escalation (2026-08-01)"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": ["true symbol resolution for 855/1,449 unmapped catalyst_events rows"],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl recomputed: 1,449 total / 594 mapped / 855 unmapped (59.0%)", "catalyst_cycle_23-11.md: momentum_breakout basket (AKE, BEAT) explicitly 'without confirmed news catalyst'", "EPIC/KAITO/HOME/AEVO/BEAT all show catalyst_news score component of only 6.8-8.1/~15 — no fresh verified catalyst for any of tonight's movers"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["Bybit/OKX cross-check unavailable for tonight's strongest symbols (scalp report §3: 'No strongest-symbol external derivatives rows available')"],
      "suggested_effect": "advisory_only",
      "facts_used": ["EPIC/HOME/ADA/EUL: price up + OI up, fresh positioning, crowding normal", "SYN/USDT: price down + OI up, funding -0.00306 (deeply negative), fresh shorts pressing / squeeze risk if reclaims", "COTI/DEXE: price down + OI down, deleveraging/long liquidation (cleaner short structure than SYN)"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["EPIC/USDT already up 10.7-18.8% 24h across scalp/intraday reports — new entries here are chasing, not fresh", "intraday report C-tier pullback zones for EPIC (0.840-0.862), KAITO (1.160-1.178), HOME (0.0061-0.0062) are the only 'not-yet-late' entries and require price to come back to them", "BANK/USDT, MMT/USDT flagged 'more than 2 ATR from EMA20; do not chase' in rejected list"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "entered_unresolved", "no_entry"],
      "data_missing": ["counts sourced from ~2.2h-stale PAPER_MONITOR_STATUS_LATEST.md snapshot, not regenerated in this cycle's weekend path"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PAPER_MONITOR_STATUS_LATEST.md (mtime 02:25): OPEN_ACTIVE=5, WAITING_FOR_ENTRY=0, REVIEW_ONLY_SHADOW=25, ENTERED_UNRESOLVED_EXPIRED=6, NO_ENTRY_EXPIRED=39, CLOSED_WIN=150/LOSS=15/FLAT=23, UNKNOWN_INCONSISTENT=4", "active-signals crypto: EPIC(intraday) waiting_for_entry; EPIC/HOME/AEVO/COTI(swing) triggered/OPEN; XRP(swing) tp1_hit partial"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["headline_risk", "manual_review", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["COTI/USDT held long but tagged weak_rs_short (-13.99% to -16.61% 24h) — direction-contradicted position, unresolved across multiple cycles now", "macro geopolitical risk 100/100 pinned by active US-Iran war escalation — correlated downside risk across the whole alt basket if BTC breaks support", "EPIC/HOME/AEVO longs are correlated (all no-catalyst RS-momentum names in the same rotation) — a single BTC/ETH downdraft would hit all three together"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["signal-stats week: headline A/B PF 2.58, avgR 0.461, winrate 25.3% (n=99) — desk-level positive but low winrate/high-R-multiple pattern", "swing mode (crypto_swing_narrative_rs_momentum, per report): 14d WR 72% / PF 5.80 / +24R — strongest mode, matches tonight's open EPIC/HOME/AEVO longs", "scalp/no-catalyst-intraday: 14d WR 23% / PF 0.70 / -3R — structurally negative, matches the reason scalp/intraday show 0 A/B tonight"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.68,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.68,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "EPIC/USDT", "trigger": "Already open (swing long). New adds only on pullback into 0.840-0.862 (intraday C-tier zone) with volume confirmation — do not chase the current extended print." },
    "best_short_candidate":    { "symbol": "SYN/USDT", "trigger": "Confirm bearish HTF structure on 15m-1h + break of recent swing low with OI-supported downside; squeeze risk is elevated (funding -0.00306, thin-liquidity capped to C) so do not short into the current stretch without a failed-bounce confirmation and a stop above the swing high." },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "perps_dex_narrative basket, playbook wait_pullback; needs a confirmed pullback entry plus a second (non-single-source) catalyst confirmation before treating as more than a watch." },
    "avoid_candidate":         { "symbol": "COTI/USDT", "reason": "Held long but tagged weak_rs_short with -14% to -17% 24h reversal — direction-contradicted, unresolved across multiple cycles; do not add, flag for manual review of the existing position." },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | caution | 0.82 | risk_off, chop, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, overextended | advisory_only |
| execution_lifecycle | ok | 0.60 | open_actionable, waiting_for_entry, review_shadow, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, manual_review, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.68 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-01_2326.md` (post-close, 23:26 EEST, ~5h before this one).

- **New:** COTI/USDT swing long now shows in `active-signals` as `triggered`/OPEN (it was not called out as an open position in the 23:26 review — its direction-contradiction is being raised as a formal §14 TODO this cycle since it has now persisted across at least 2 consecutive reviews).
- **Unchanged / carried forward:** EPIC/USDT and AEVO/USDT swing longs remain OPEN, still RS-leaders, still no fresh catalyst. XRP/USDT short remains OPEN (partial TP booked, runner open) — no new news, still non-catalytic (Ripple escrow-lock chatter only).
- **Removed:** none of the 23:26 review's named candidates dropped out of the active book.
- **New catalysts:** none material overnight — the momentum_breakout basket (AKE, BEAT) is explicitly flagged "without confirmed news catalyst" in tonight's catalyst cycle scan.
- **Thesis changed:** BTC's 24h decline accelerated externally (down ~3.25% per CoinGabbar, vs a milder read implied in the 23:26 review) — the risk-off macro thesis is confirmed, not weakened.
- **Confirmed:** Catalyst mapping remains weak (59.0% unmapped tonight vs 57.3% at 23:26) — persistent, unresolved.
- **Invalidated:** none.

## 5. Catalyst Coverage

- Total `catalyst_events` (cumulative day file, UTC-day boundary so still `data/catalysts/2026-08-01/`): **1,449**
- Mapped (non-null symbol): **594** (41.0%)
- Unmapped (null symbol): **855** (59.0%)
- `narrative_baskets`: **5** (perps_dex_narrative/HYPE, ai_narrative/NEAR+RENDER+TAO+FET, binance_ecosystem_teaser/BNB, delisting_thin_liquidity, momentum_breakout/AKE+BEAT)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped headlines (sample): "Maximum Leverage Adjusted for JPMUSDT Futures [Aug 1, 2026, 06:00 (UTC)]" / "...for GEVUSDT Futures..." / "...for HYUNDAITUSADT Futures..." — all Binance leverage-adjustment announcements the symbol resolver fails to parse (recurring root cause, same as prior cycles).

## 6. Market Landscape

BTC/ETH both in downtrend, range/chop regime, altcoin breadth ~41-42.5% above EMA20 (mixed, not broad participation). Macro/geopolitical risk pinned at max (100/100) driven by the active US-Iran war (externally verified tonight, see §13) plus a spreading Bitcoin cold-wallet exploit (~$89M / 4,500 addresses). Despite the risk-off macro backdrop, a narrow cluster of no-catalyst alts (EPIC, KAITO, HOME, AEVO, BEAT, AKE) is showing strong RS/momentum — this is the desk's known-negative playbook (no-catalyst intraday chop: 14d WR 23%/PF 0.70), so it should be treated as low-quality breadth, not confirmation of a broader risk-on turn.

### Market Mood / Risk Routing

- Crypto mood:           risk-off / chop (BTC/ETH downtrend, macro 100/100 risk-off, but a narrow no-catalyst alt-momentum cluster is running counter-trend)
- Stocks mood:           closed (Sunday; last actionable data Friday, planning-context only)
- Dominant narrative:    Momentum-without-catalyst rotation (EPIC/KAITO/HOME/AEVO/BEAT/AKE) inside a risk-off macro tape driven by the active US-Iran conflict
- Preferred side now:    mixed — hold existing RS-leader longs (EPIC/HOME/AEVO), do not chase new longs into the extension; watch for confirmed failed-bounce shorts on weak-RS names (SYN/DEXE) once squeeze risk clears
- Best long candidate:   EPIC/USDT (already open; new adds only on pullback to 0.840-0.862 with volume confirmation)
- Best short candidate:  SYN/USDT (needs bearish HTF confirmation + break of swing low before entry; squeeze-prone until then)
- Best catalyst-backed candidate: HYPE/USDT (perps_dex_narrative basket; needs pullback entry + second-source catalyst confirmation)
- What to avoid:         COTI/USDT (held long, direction-contradicted by -14% to -17% 24h reversal); fresh longs on BANK/USDT, MMT/USDT, SYN/USDT, COTI/USDT, DEXE/USDT (all capped C-tier on thin-liquidity short-squeeze risk or >2 ATR extension)
- What would change the view: A confirmed US-Iran de-escalation headline or BTC reclaiming its local downtrend structure would lift the risk-off cap; a clean failed-bounce + bearish HTF break on SYN/DEXE would activate the short side; a pullback fill into EPIC's 0.840-0.862 zone with volume would activate a fresh long add.

## 7. Candidate Deep Dives

### EPIC/USDT (long, OPEN swing position + separate C-tier watchlist re-confirmation)

- Has price already reacted to the catalyst? No fresh catalyst exists — this is a pure RS/momentum move (rs_btc_leader, rs_eth_leader, momentum_24h_leader, momentum_7d_leader tags across three separate reports tonight).
- Is the setup chasing? Yes, for a **new** entry — up 10.7-18.8% 24h depending on report snapshot. The existing open swing position is not chasing (it was filled on an earlier pullback).
- Retest/pullback structure? Yes — intraday report gives an explicit conditional pullback zone (0.840-0.862) for a fresh watch entry.
- Overextended (>2 ATR from EMA20)? Not flagged as such in the rejected-list reasons (unlike BANK/MMT), but momentum score (91.6/100) and RS (+10-19% vs BTC) both signal a stretched move.
- Would entry now be late? Yes, for a new position at current price.
- Actionable level: 0.840-0.862 pullback with volume confirmation; invalidation 1h close beyond 0.813-0.852 range depending on snapshot.
- Aligned with market mood? Partially — it's a genuine RS-leader (the one playbook that works, 14d WR 72%/PF 5.80 for `crypto_swing_narrative_rs_momentum`), but it's running counter to the broader risk-off macro tape, which raises correlation risk if BTC breaks down.
- Long/short/wait: existing long — hold; wait-for-trigger for adds.
- Chase risk: high for new entries at current price.
- Catalyst confirmation/contradiction: no catalyst either way — pure technical/RS thesis.
- Derivatives: price up + OI up (fresh positioning, not exhausted), funding neutral-to-slightly-positive, crowding normal — supportive, not yet crowded.

### COTI/USDT (long, OPEN swing position — **direction-contradicted, flag for manual review**)

- Has price already reacted? Yes — 24h return -13.99% to -16.61% across tonight's reports, the opposite direction of the held long.
- Is this a chase-risk setup? N/A — the position is already held; the question is whether it should still be held.
- Retest/pullback structure? None supporting the long thesis; discovery watchlist explicitly tags COTI/USDT `weak_rs_short` (`crypto_failed_bounce_short` playbook, score 80) tonight.
- Overextended? The move is now extended in the *opposite* direction from the position.
- Actionable level: none for a fresh long; the existing position's invalidation/stop should be re-checked by an operator.
- Aligned with market mood? No — risk-off macro plus its own -14% to -17% reversal both argue against the long thesis.
- Long/short/wait: existing long is contradicted; do not add; flag for manual close/hold review.
- Would invalidate: it already looks invalidated on the tape; formal stop/invalidation level needs an operator check against current price.
- Chase risk: N/A (existing position).
- Catalyst confirmation/contradiction: no catalyst news found in the last 24h for COTI (`news_items` query: 0 rows) — the reversal is pure price action, not news-driven, which makes it harder to explain away.

### XRP/USDT (short, OPEN swing position, partial TP booked)

- Has price already reacted to the catalyst? No fresh catalytic news — 3 fresh items in the last 24h are all routine Ripple escrow-lock whale-alert posts (500M + 200M XRP locked) plus one generic "should you buy XRP" opinion piece; none contradict the short thesis.
- Chasing? No — this is a held position with partial profit already booked (tp1_hit).
- Retest structure? Tonight's swing scan independently re-confirmed the same 1.0598-1.0610 zone in prior cycles (not refreshed as a new candidate this cycle since XRP isn't in tonight's top-movers list — not a red flag, just quiet).
- Actionable level: runner stop/invalidation should track the original plan; no new action needed tonight.
- Aligned with mood: yes — clean short expression of the risk-off macro thesis, unlike COTI's contradicted long.
- Catalyst confirmation/contradiction: no contradiction found.

### HOME/USDT & AEVO/USDT (long, OPEN swing positions)

- Same profile as EPIC: no-catalyst RS/momentum longs (HOME +13.5-19.9% 24h, AEVO +7.6% 24h), both filled on earlier pullbacks, both currently extended for **new** entries.
- Derivatives: HOME price up + OI up (fresh positioning), funding slightly negative (-5.6e-05, shorts mildly crowded, supportive for the long); AEVO similar profile, no OI data available in tonight's scalp snapshot.
- No fresh catalyst news for either symbol in the last 24h (`news_items` query: 0 rows each).
- Aligned with mood: same caveat as EPIC — correlated no-catalyst alt-rotation risk if BTC breaks down; hold, don't add at current price.

### SYN/USDT (best short-watch, not yet actionable)

- 24h -12.5% to -16.6% across reports, `weak_rs_short` + `catalyst_backed` tags (score 80) in tonight's discovery watchlist, but capped to C-tier by `thin_liquidity_short_squeeze_risk` — funding deeply negative (-0.00306 to -0.00187) meaning shorts are already crowded, raising squeeze risk on any bounce.
- Not actionable as-is: needs confirmed bearish HTF structure + a clean break of the recent swing low with a stop above the swing high before entry.
- Catalyst confirmation/contradiction: none found tonight; the move looks purely technical/RS-driven, same category as the long-side movers but in reverse.

## 8. Best Candidates Ranked

1. **EPIC/USDT** (long, OPEN — hold; watch 0.840-0.862 for adds) — clearest RS-leader with the strongest-performing playbook (`crypto_swing_narrative_rs_momentum`, 14d WR 72%/PF 5.80) backing it, but no catalyst and currently extended.
2. **HOME/USDT** (long, OPEN — hold) — same profile, slightly less liquid confirmation than EPIC (MEXC-fallback derivatives only).
3. **AEVO/USDT** (long, OPEN — hold) — same profile, most modest of the three (7.6% 24h vs 10-20% for EPIC/HOME).
4. **XRP/USDT** (short, OPEN — hold runner) — cleanest short expression of the risk-off macro thesis, already de-risked with partial TP.
5. **SYN/USDT** (short-watch, not yet actionable) — best short candidate pending bearish HTF + swing-low-break confirmation; squeeze-prone until then.

No fresh A/B tonight. Best long-watch = EPIC/USDT pullback zone (see above). Best short-watch = SYN/USDT pending confirmation (see above). Best catalyst-watch = HYPE/USDT (perps_dex_narrative, needs a confirmed pullback + second-source catalyst validation).

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and monitors continue regardless.

- **COTI/USDT** — avoid adding; existing long is direction-contradicted (-14% to -17% 24h vs a held long), flag for manual position review.
- **BANK/USDT, MMT/USDT** — >2 ATR from EMA20, chase risk explicitly flagged in tonight's rejected list.
- **DEXE/USDT, ZAMA/USDT, 1000SATS/USDT, GRVT/USDT** — thin-liquidity short-squeeze risk, capped to C-tier; do not short without confirmation.
- No clean fresh long or short clears the A/B bar tonight — this applies to the current 2.5h window only, not a system pause.

## 10. Main Risks

- **Macro/geopolitical**: active US-Iran war escalation (verified externally, §13), Strait of Hormuz partially blockaded — a genuine tail risk to broad risk assets, not yet priced into the alt-momentum cluster currently running.
- **Correlation cluster**: EPIC/HOME/AEVO are all no-catalyst RS-momentum longs in the same rotation — a single BTC/ETH downdraft would likely hit all three together.
- **COTI direction-contradiction**: unresolved across multiple cycles now; genuine operator-attention item, not just a data artifact.
- **Catalyst mapping at 59% unmapped**: reduces confidence in "no fresh catalyst" reads generally — treat as best-available, not exhaustive.
- **Squeeze risk on the short side**: SYN/DEXE/COTI(as short) all carry crowded-funding squeeze risk; a short without confirmation risks a violent reclaim.

## 11. Action Plan — next 4 hours

1. Hold EPIC/HOME/AEVO/XRP swing positions as-is; no new entries unless price returns to the stated pullback zones with volume confirmation.
2. Flag COTI/USDT swing long for manual review given the persisting direction contradiction (§14 TODO).
3. Watch SYN/USDT and DEXE/USDT for a confirmed bearish HTF break before considering a short entry.
4. Watch HYPE/USDT for a pullback entry plus a second-source catalyst confirmation before treating the perps_dex_narrative basket as more than a watch.
5. Monitor US-Iran headlines into the Europe-open (11:30 review) — any de-escalation or Strait-of-Hormuz resolution would materially change the risk-off routing.
6. Continue scanning/tracking/monitoring uninterrupted — no pause recommended.

## 12. Final Verdict per Mode

- **Scalp**: No trade. Structurally weak playbook (14d PF 0.14 per report banner); 0 A/B tonight.
- **Intraday**: No trade. 0 A/B; best watchlist name BEAT/USDT at 57.2/100, not actionable.
- **Swing**: Hold existing RS-leader longs (EPIC, HOME, AEVO) and the XRP short; no fresh entries. COTI long flagged for manual review.
- **Stocks (all modes)**: Closed (Sunday) — planning/carry-forward context only, no verdict.

## 13. Sources

- [Iran warns against 'flames of war' amid US strike threats on energy sites](https://www.aljazeera.com/news/2026/8/1/iran-warns-against-fire-of-war-amid-us-strike-threats-on-energy-sites) — Al Jazeera, 2026-08-01, primary_source. Confirms active US-Iran escalation, US strikes on 5+ Iranian provinces, Strait of Hormuz partially blockaded, no de-escalation signal.
- [Crypto News August 1: Bitcoin Down 3.25%, AnthropicAI Token Gains 775%](https://www.coingabbar.com/en/crypto-currency-news/crypto-news-today-1-august-bitcoin-eth-drops-anthropic-gains) — CoinGabbar, 2026-08-01, single_source. BTC -3.25%/24h, ETH -3.18%/24h, corroborates the local downtrend read.
- Internal: `data/catalysts/2026-08-01/catalyst_cycle_23-11.md`, `catalyst_events.jsonl`, `narrative_baskets.jsonl`.
- Internal: `news_items` table, direct queries for EPIC/KAITO/HOME/AEVO/COTI/XRP/BEAT (24h window).

## 14. Fix Requests / TODO

### TODO-coti-direction-contradiction
- **issue:** COTI/USDT is held as an OPEN swing long (`sig_06b6c2801005f29d`, entry 0.0161-0.0167) but has shown a -13.99% to -16.61% 24h reversal and carries a `weak_rs_short` discovery-watchlist tag across at least the last 2 consecutive reviews (23:26 and this one).
- **evidence:** `active-signals --asset-class crypto` (status=triggered), `reports/PAPER_MONITOR_STATUS_LATEST.md` line 88 (🟢 OPEN), scalp/intraday/swing reports §2 "Weakest Symbols" listing COTI/USDT at -14% to -17%/24h, `news_items` query showing 0 fresh (24h) catalytic news for COTI.
- **suggested manual fix:** An operator should manually review the COTI/USDT position's current price vs its invalidation level and decide whether to hold, tighten the stop, or close — this is a position-management decision the automated review cannot make.
- **priority:** medium
- **first observed:** 2026-08-01 23:26 EEST (this review is the second consecutive cycle to flag it, unresolved)

### TODO-catalyst-mapping-weak-recurring
- **issue:** Catalyst symbol-mapping has been >50% unmapped for multiple consecutive review cycles (57.3% at 23:26, 59.0% now), consistently traced to unparsed Binance "Maximum Leverage Adjusted for X Futures" announcement headlines.
- **evidence:** direct recomputation of `data/catalysts/2026-08-01/catalyst_events.jsonl` (1,449 total / 594 mapped / 855 unmapped); sample unmapped titles: "Maximum Leverage Adjusted for JPMUSDT Futures...", "...GEVUSDT Futures...", "...HYUNDAITUSADT Futures...".
- **suggested manual fix:** Improve the catalyst symbol resolver to special-case Binance's "Maximum Leverage Adjusted for {SYMBOL} Futures" announcement template, or add a dedicated regex/parser for it, since it appears to be a large, easily-classifiable chunk of the unmapped volume.
- **priority:** low (context-only impact, does not gate scoring/routing)
- **first observed:** recurring across multiple prior reviews (at least 2026-07-31 21:45 onward); still open.
