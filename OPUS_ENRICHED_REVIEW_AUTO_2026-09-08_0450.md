# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:30 EEST

## 1. Executive Summary

**Slot: crypto overnight / Asia review. Advisory only — no auto-trade, no code/scoring changes.**
No A-tier or B-tier "armed" setups cleared the score gate this cycle in either intraday or swing reports — everything sits in C-tier/watchlist. Three fresh B-tier longs (SOPH, PENDLE, AERO) armed ~01:39 EEST and remain `waiting_for_entry`, with PENDLE essentially sitting inside its entry zone right now. BTC is range-bound, ETH trending up, altcoin breadth strong (81–93% above EMA20/50), but macro risk sits elevated (56–77/100) on active Iran/Houthi/Israel-UK escalation headlines — a genuine mixed tape, not a clean risk-on read. Catalyst mapping is weak this run (68.2% unmapped) — treat the catalyst layer as context only. RAY/USDT's DB-status contradiction (flagged in the last several cycles) persists. Route the decision — do not default to blanket no-trade.

## 2. Data Used

- Intraday report: `data/reports/intraday/2026-09-08_00-58_intraday_report.md` (generated 03:57 EEST, data freshness 00:45 UTC)
- Swing report: `data/reports/swing/2026-09-07_22-37_swing_report.md` (generated 01:36 EEST, data freshness 22:15 UTC prior day)
- Stocks intraday report: `data/reports/stocks/intraday/2026-09-07_21-19_stocks_intraday_report.md` (stale — last trading session was pre-Labor-Day; US markets closed 2026-09-07 Labor Day, pre-market 2026-09-08 at time of this review)
- Catalyst layer: `data/catalysts/2026-09-08/catalyst_events.jsonl` (500 events), `narrative_baskets.jsonl` (4 active baskets)
- CLI: `active-signals --asset-class crypto` (50 open-window rows), `active-signals --asset-class stocks` (context only, all stale from Sep 2–5), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-09-08`
- Direct read: `proposed_signals` (status distribution, RAY/USDT history), `news_items` (ARB/USDT freshness check)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_2334.md`
- **External web research not performed this run** — all candidates below had internal `news_items`/catalyst records that were recent (<24h) and internally consistent, so per the skill's internal-first rule, external WebSearch/WebFetch was not triggered. No claim below depends on unverified external data.

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime 2026-09-08 04:38 EEST — fresh (~1 min old).
- Latest cycle summary `cycle_01_22-48_summary.md`: mtime 2026-09-08 01:49 EEST — ~2.8h old, under the 3h defer threshold. **Not deferred.**
- Intraday report: ~1h stale relative to now (fresh, <4h bar N/A for intraday but well within useful window).
- Swing report: ~3h old — **fresh** (<4h bar).
- Stocks intraday: last generated Sep 7 21:19 EEST, but underlying session data is from before the Labor Day closure — **stale/carry-forward, planning context only**; stocks swing/invest reports are deprecated (last real content July 2, per project history) and excluded.
- Catalyst scan: ran today at 04:05 EEST, current.
- No monitor/paper-status file was read this cycle beyond the above; no blocker encountered.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-09-08 04:50 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"], "data_missing": ["stocks intraday session data (Labor Day closure)"],
      "suggested_effect": "advisory_only", "facts_used": ["scheduler.log mtime 04:38", "cycle_01 summary mtime 01:49", "catalyst scan ran 04:05"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["BTC trend=range", "ETH trend=uptrend", "altcoin breadth 81-93% above EMA20/50", "macro risk 55.9-76.8/100 risk-off headwind"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "stale_catalyst", "narrative_supported"], "data_missing": ["symbol-level social/KOL data"],
      "suggested_effect": "advisory_only", "facts_used": ["500 catalyst_events today, 341 unmapped (68.2%)", "4 active narrative baskets: ai_narrative, perps_dex_narrative, rwa_narrative, momentum_breakout", "SOL/USDT StonkFun catalyst uncontradicted", "ARB/USDT fresh bullish news (Robinhood Chain revenue share, Uniswap AnchoredFi integration) vs -11% 24h price"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "funding_extreme", "oi_supports", "data_unavailable"], "data_missing": ["OI 24h% for several fallback_via_mexc symbols"],
      "suggested_effect": "advisory_only", "facts_used": ["SOPH funding 0.00054-0.00066, elevated long crowding flagged", "ACE funding -0.0032 to -0.0059 (negative, external-confirmed), crowding elevated/unknown", "ORCA funding -0.00149, price up + OI up +50.3%"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_fresh", "entry_late", "clean_retest", "stale_before_entry"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["PENDLE current 2.198 sits inside armed entry zone 2.1849-2.2051", "AERO current ~0.6036 near armed entry zone 0.6012-0.6110", "SOPH just armed 01:39 EEST, not yet at entry", "RAY/USDT has a parallel 'stale_before_entry'-status signal alongside a frozen 'triggered' one"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": ["entry-fill timestamp field to cleanly split expired-entered vs expired-no-entry"],
      "suggested_effect": "advisory_only", "facts_used": ["open-window crypto B-tier: triggered=36, waiting_for_entry=10, stopped=28, entry_moved_away=18, expired=11, tp1/2/3_hit=11, stale_before_entry=2, missed_no_entry=1"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "manual_review", "correlation_cluster"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["Iran hypersonic-missile-over-carrier / Houthi-Saudi / Israel-UK sanctions headlines all fresh", "BTC/TAO/XRP carry exploit_hack operator-review flags (Liquid Network hack, Bittensor RedTeam, XRP Healthcare)", "RAY/USDT DB-status contradiction unresolved across multiple cycles"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.75,
      "reason_codes": ["playbook_working", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["crypto B-tier headline: winrate 18.8%, PF 2.34, avgR 0.31, totalR +45.5 (n=225, reliable)", "swing sub-mode PF 3.00 / long direction PF 2.47 vs short direction PF 0.25 (n=3, anecdotal, all losses)", "weekend-mode signals underperform sharply: PF 1.31/WR 9% vs weekday PF 3.81/WR 31% (today is a weekday, so full-weight regime applies)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only", "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "PENDLE/USDT", "trigger": "already armed B-tier waiting_for_entry, price 2.198 inside stated zone 2.1849-2.2051; treat as actionable only on a clean acceptance inside the zone, invalidation 1h close beyond 2.1603", "reason": "freshest armed long (~01:39 EEST) with price already sitting in the planned zone, backed by the swing desk's RS-leader/narrative playbook (14d WR 72% / PF 5.80 on this cohort)" },
    "best_short_candidate":    { "symbol": "ZAMA/USDT", "trigger": "confirmed failed bounce/retest of 0.0509-0.0514 with a 1h close beyond 0.0519 invalidated (i.e. rejection held), or a clean breakdown continuation; do not chase the existing -10% move", "reason": "cleanest bias-short leader with no fresh catalyst contradiction (unlike ARB), still in the Weakest Symbols list on both intraday and swing reports" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "StonkFun launchpad volume surge (The Block) remains uncontradicted; watch for a proposed_signal to form on a confirmed pullback rather than chasing the news print", "reason": "same cleanest single-direction catalyst read as the prior cycle — still no internal contradiction and no proposed_signal has formed yet" },
    "avoid_candidate":         { "symbol": "RAY/USDT", "reason": "unresolved DB-status contradiction: an older 'triggered' long signal (sig_2545637e5925f4c0, created 2026-09-06T20:09) sits open in the armed-watch table while newer overlapping signals for the same symbol already resolved to 'stale_before_entry' and 'stopped' — genuinely unclear whether a live position exists; treat as manual-review, not a fresh entry" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | caution | 0.65 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, stale_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, funding_extreme, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_fresh, entry_late, clean_retest, stale_before_entry | advisory_only |
| execution_lifecycle | needs_review | 0.70 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, manual_review, correlation_cluster | advisory_only |
| playbook_performance | ok | 0.75 | playbook_working, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review (23:34 EEST, 2026-09-07): overall_verdict `caution`, best long WLD/USDT, best short ARB/USDT (already noted as a "genuinely mixed short case" that cycle), best catalyst SOL/USDT, avoid RAY/USDT.

- **New:** SOPH/USDT, PENDLE/USDT, AERO/USDT armed as fresh B-tier waiting_for_entry longs (~01:39 EEST) — none of these existed as fresh signals in the prior review.
- **Carried forward unchanged:** SOL/USDT catalyst thesis (StonkFun) — still uncontradicted, still no proposed_signal formed. RAY/USDT avoid-candidate status — contradiction is now confirmed to be a genuine multi-signal overlap issue (see §9), not just a stale display artifact.
- **Downgraded / rotated out:** WLD/USDT — was previous best-long, now shows `tp2_hit` in the armed table (already played out); no longer the freshest idea, replaced by PENDLE as best long-watch.
- **Thesis changed:** ARB/USDT — moved from "best short candidate (mixed case)" last cycle to fully demoted this cycle. Fresh news since (Robinhood Chain revenue share, Uniswap/AnchoredFi tokenized-stocks integration) strengthens the bullish-contradiction case further; ARB is now a manual-review/avoid-for-shorts symbol rather than a short-watch, and ZAMA/USDT takes over as best short-watch instead.
- **Catalyst mapping:** 68.2% unmapped this run — consistent with the ongoing weak-mapping pattern flagged across recent cycles (see §14 TODO, still open).

## 5. Catalyst Coverage

- Total catalyst events today: **500**
- Mapped (symbol present): **159** (31.8%)
- Unmapped (null symbol): **341 (68.2%)**
- Narrative baskets active: **4** — `ai_narrative` (NEAR, RENDER, TAO, FET), `perps_dex_narrative` (HYPE), `rwa_narrative` (ONDO, XLM), `momentum_breakout` (UNI, CFG, AUCTION)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.**

Top 3 unmapped headlines (illustrative, symbol resolver miss):
- "Investigators recover black boxes from cargo plane crash in Miami" (Reuters)
- "30-YEAR JAPANESE GOVERNMENT BOND YIELD DROPS 4.0 BPS TO 3.980%..."
- "5-YEAR JAPANESE GOVERNMENT BOND YIELD DROPS 2.0 BPS TO 2.230%..."

These are macro/bond-market wires with no crypto ticker to map to — not a resolver failure on crypto-specific news, but they inflate the unmapped percentage. The resolver-quality question (§14 TODO) remains open regardless.

## 6. Market Landscape

BTC is range-bound near $79,280 (-0.67% Monday), ETH holding $2,484 (-0.41%), market cap $2.79T, BTC dominance 57.2%. Altcoin breadth is strong — 81–93% of tracked symbols above EMA20/50 — but macro risk score sits at 56–77/100 on active geopolitical escalation (Iran hypersonic missile test over a US carrier, an ended Ukraine ceasefire with fresh Kyiv attacks, the most extensive Houthi attack on Saudi Arabia in years, Israel–UK sanctions rhetoric over the Falklands). This is a genuinely mixed tape: broad participation and an uptrending ETH argue for selective long exposure, while the headline stack argues against complacency or size.

Exploit/hack overhang is elevated but diffuse: BTC (Liquid Network $320M hack, still being negotiated on-chain), TAO (Bittensor RedTeam ethical-hacking framing + upcoming Exploit Summit), XRP (XRP Healthcare $452K drain from a staking-seed bug) all carry `block_requires_operator_review` flags. None of these are new A/B candidates tonight, so they are risk-context rather than active blockers.

### Market Mood / Risk Routing

- Crypto mood: **mixed** (strong breadth + uptrending ETH vs elevated macro/geopolitical risk and a range-bound BTC)
- Stocks mood: **closed** (pre-market Tuesday following the Labor Day 2026-09-07 closure; treat all stocks context as planning-only)
- Dominant narrative: AI (NEAR/RENDER/TAO/FET) and RWA (ONDO/XLM) baskets both fresh <24h; L2 heat highest (55.9/100) but driven mostly by ARB attention rather than volume
- Preferred side now: **longs, selectively** — RS-leaders with playbook backing (crypto_swing_narrative_rs_momentum, 72% WR / PF 5.80) over chasing 24h movers with thin volume confirmation
- Best long candidate: PENDLE/USDT (armed, in-zone — see §3A/§7)
- Best short candidate: ZAMA/USDT (clean weakness, no catalyst contradiction — see §3A/§7)
- Best catalyst-backed candidate: SOL/USDT (StonkFun volume surge, uncontradicted, no signal formed yet)
- What to avoid: RAY/USDT (signal-integrity contradiction), ARB/USDT (technical short thesis now contradicted by fresh bullish news flow — do not treat as a clean short)
- What would change the view: A verified de-escalation headline on the Iran/Houthi/Israel-UK front would lower macro risk and could unlock a cleaner risk-on read; a confirmed BTC breakout out of range (either direction) would resolve the "transition (mixed)" regime label into a tradeable trend.

## 7. Candidate Deep Dives

### 1. PENDLE/USDT — armed long, near/in entry zone
- **Status:** WAITING for entry (armed B-tier, created 2026-09-07T23:46 UTC / ~01:46 EEST)
- Entry zone 2.1849–2.2051, invalidation 1h close beyond 2.1603, current price 2.198 (inside zone)
- Playbook: `crypto_swing_narrative_rs_momentum` — 14d WR 72% / PF 5.80 / +24R cohort; known failure mode is chasing after a vertical 24h move or a BTC dump invalidating correlated swing longs.
- Has price already reacted to a catalyst? No fresh verified catalyst on PENDLE specifically — this is a pure RS/momentum thesis (24h +5.1%, 7d +25.5%, RS vs BTC +6.2%).
- Chasing risk? Low — price sits inside, not above, the planned zone.
- Retest/pullback structure? Yes, this is the pullback zone itself.
- Overextended (>2 ATR from EMA20)? No indication in the report; setup quality scored 67.4/100.
- Would entry now be late? No — this is the intended entry.
- What makes it actionable? Acceptance (not just a wick) inside 2.1849–2.2051 with BTC/ETH not breaking down against the mixed-regime thesis.
- Aligned with market mood? Yes — selective long, RS-leader cohort, not a chase.
- Long, short, or wait-for-trigger? Long, essentially at trigger already.
- Actionable now or after confirmation? After a clean acceptance candle in-zone; do not treat the bare "waiting_for_entry" DB status alone as a fill.
- Invalidation: 1h close beyond 2.1603.
- Chase-risk setup? No.
- Catalyst confirmation or contradiction? None either way — pure technical/RS thesis.

### 2. AERO/USDT — armed long, near entry zone
- **Status:** WAITING for entry (armed B-tier, created ~01:46 EEST)
- Entry zone 0.601209–0.610964, invalidation 1h close beyond 0.589286.
- Playbook: same `crypto_swing_narrative_rs_momentum` cohort (72% WR / PF 5.80).
- 24h +12.0%, 7d +30.2%, RS vs BTC +13.1%, but volume ratio only 0.01x-0.07x of the 20-period average across both reports — **relative strength not backed by strong current volume**, the counter-thesis both reports flag explicitly.
- Has price reacted to a catalyst? No fresh verified catalyst detected for AERO.
- Chase risk: moderate — the 24h move is already large relative to the thin volume confirming it.
- What makes it actionable? A volume-confirmed retest of the zone, not just price sitting near it on low turnover.
- Aligned with mood? Marginally — fits "longs selectively" but the volume gap is a real quality concern.
- Actionable now or after confirmation? After confirmation — the volume caveat argues for waiting rather than treating the bare in-zone price as sufficient.
- Invalidation: 1h close beyond 0.589286.
- Catalyst: none, pure RS thesis, same known failure mode as PENDLE (chase after vertical move / BTC dump).

### 3. SOPH/USDT — armed long, not yet at entry, crowding flag
- **Status:** WAITING for entry (armed B-tier, created ~01:59 EEST)
- Entry zone 0.005481–0.005633, invalidation 1h close beyond 0.005296.
- 24h +34–38% (varies slightly between the two report snapshots), funding 0.00054–0.00066 (positive, elevated), **derivatives layer explicitly flags "elevated long crowding."**
- Derivatives_squeeze concern: this is the one candidate this cycle carrying a live crowding flag rather than "normal."
- Has price reacted to a catalyst? No fresh verified catalyst.
- Chase risk: elevated — a 34%+ 24h move plus crowded long positioning is the textbook setup for a long-squeeze/unwind on any BTC wobble.
- What makes it actionable? A cooldown in funding/crowding plus a controlled pullback into the zone, not a fresh breakout add.
- Aligned with mood? Borderline — this is the least clean of the three fresh longs given the crowding read.
- Actionable now or after confirmation? After confirmation; treat crowding as a live caution flag, not just a footnote.
- Catalyst: none verified.

### 4. RAY/USDT — signal-integrity contradiction (AVOID / MANUAL REVIEW)
- Three overlapping `proposed_signals` rows exist for RAY/USDT: `sig_2545637e5925f4c0` (created 2026-09-06T20:09 UTC, status still `triggered`, expires 2026-09-13T20:09), `sig_aeaff50a6148b3be` (created 2026-09-06T22:54 UTC, status `stale_before_entry`), and `sig_27c909d5cb4e26bc` (created 2026-09-07T02:11 UTC, status `stopped`).
- This is the same integrity issue flagged across multiple prior cycles (bias-tag contradiction / stale DB status), now confirmed at the row level rather than just via the bias-tag mismatch: the oldest signal remains `triggered` (open) in the armed-watch table while two newer signals for the same symbol have already resolved.
- **Execution_lifecycle read:** NEEDS REVIEW — it is not possible from these three rows alone to say whether a live RAY position exists in reality.
- **Head Trader verdict:** AVOID as a fresh idea; do not treat the open `triggered` row as either a valid open position or as cover to enter fresh. Route to manual review, not a scoring/code fix (see §14 TODO — already tracked, still open).

### 5. ARB/USDT — catalyst-vs-technical contradiction (AVOID for shorts / MANUAL REVIEW)
- 24h return -11.1% (intraday) / -10.5% (swing), RS vs BTC ~-9 to -10%, in the Weakest Symbols list on both reports — a textbook short-side technical read.
- But `news_items` in the last 24h shows: "Arbitrum gets 10% of Robinhood Chain revenue — can it fuel ARB's rally?" (AMBCrypto, 23:00 UTC 2026-09-07), "Uniswap integrates AnchoredFi's tokenized stocks on Arbitrum" (CryptoBriefing, 15:21 UTC), plus the already-known Sunrise/Wormhole NTT listing catalyst — all bullish-leaning, none contradicted internally.
- This is the same "genuinely mixed short case" flagged in the prior review, now reinforced with an additional fresh bullish headline (Robinhood Chain revenue share) since that review.
- Has price reacted to the catalyst? Not yet — price is still weak despite the bullish news flow, which is itself informative (either the market hasn't digested it, or the news is being discounted).
- Is this a clean short? No — do not treat ARB as a short on technical weakness alone while three independent bullish catalysts sit unresolved against it.
- What would make it actionable either way? A short only becomes clean on a confirmed breakdown *despite* the news being fully priced in (e.g., a failed pop on the Robinhood Chain headline); a long only becomes attractive on a reclaim of RS vs BTC alongside the catalyst.
- **Verdict: MANUAL REVIEW REQUIRED**, not a routine short-watch.

## 8. Best Candidates Ranked

1. **PENDLE/USDT (long-watch)** — armed, in-zone, RS-leader playbook backing. Trigger: clean acceptance inside 2.1849–2.2051.
2. **AERO/USDT (long-watch, needs volume confirmation)** — armed, near-zone, but thin volume. Trigger: volume-confirmed retest of 0.6012–0.6110.
3. **SOL/USDT (catalyst-watch)** — StonkFun catalyst uncontradicted, no signal formed. Trigger: a proposed_signal forming on a confirmed pullback, not the news print itself.
4. **ZAMA/USDT (short-watch)** — clean weakness, no catalyst contradiction. Trigger: confirmed failed bounce/retest of 0.0509–0.0514, or continuation below invalidation 0.0519.
5. **SOPH/USDT (long-watch, crowding caution)** — armed but crowded-long flag. Trigger: crowding/funding cooldown plus a controlled pullback into 0.005481–0.005633.

No clean A/B-tier trade exists outright this window — every idea above is watch/confirmation-gated, which is the correct read given the score gate, not a system failure.

## 9. Avoid / No Trade

*(This decision window only — scanning, tracking, and the scheduler continue regardless.)*

- **RAY/USDT** — signal-integrity contradiction (three overlapping DB rows, oldest still shows `triggered`). Manual review, not a fresh entry.
- **ARB/USDT** — catalyst-vs-technical contradiction (bearish price, three unresolved bullish headlines). Manual review, not a routine short.
- Broader caution: do not chase any of tonight's large 24h movers (IOST +30%, SOPH +38%, DASH -9% to -19% territory on some cross-report deltas) without volume or crowding confirmation — this cycle's derivatives layer is flagging thin-volume RS reads as the dominant failure mode.

## 10. Main Risks

- Geopolitical escalation (Iran/Houthi/Israel-UK) is live and could move macro risk sharply in either direction intraday — this is the single largest tail risk tonight.
- Catalyst mapping at 68.2% unmapped this run reduces confidence in any catalyst-backed read beyond the specific symbols manually cross-checked here (SOL, ARB).
- SOPH's crowded-long positioning raises squeeze/unwind risk on any BTC wobble.
- RAY/USDT's unresolved multi-signal contradiction is a data-integrity risk, not a market risk — flagged to TODO, not fixed here.
- Stocks context is fully stale (pre-Labor-Day) — treat as zero-weight for this decision window.

## 11. Action Plan — next 4 hours

- Watch PENDLE/USDT for a clean in-zone acceptance candle before treating it as filled.
- Watch AERO/USDT and SOPH/USDT for volume/crowding confirmation before adding size; do not chase the existing 24h move on either.
- Watch ZAMA/USDT for a failed-bounce confirmation as the cleanest short idea on the board.
- Watch SOL/USDT for a proposed_signal to form around the StonkFun catalyst on a pullback.
- Flag RAY/USDT and ARB/USDT for manual review before the next cycle touches either.
- Re-check macro headlines (Iran/Houthi/Israel-UK) at the next scheduled slot (11:30 EEST) for escalation/de-escalation before revising the mood read.

## 12. Final Verdict per Mode

- **Crypto intraday:** No A/B setups; C-tier watchlist only. Caution / selective-longs-only routing.
- **Crypto swing:** No A/B setups; three fresh armed B-tier longs (PENDLE, AERO, SOPH) in `waiting_for_entry` — watch for confirmation, do not force fills.
- **Stocks intraday/swing/invest:** Closed / stale (post-Labor-Day pre-market) — planning-only, zero-weight this window.
- **System-wide:** Scanning, tracking, and the scheduler continue uninterrupted regardless of the above — this is a decision-window caution, not a stop instruction.

## 13. Sources

- Internal: [data/reports/intraday/2026-09-08_00-58_intraday_report.md](data/reports/intraday/2026-09-08_00-58_intraday_report.md)
- Internal: [data/reports/swing/2026-09-07_22-37_swing_report.md](data/reports/swing/2026-09-07_22-37_swing_report.md)
- Internal: `news_items` table — AMBCrypto, "Arbitrum gets 10% of Robinhood Chain revenue — Can it fuel ARB's rally?", published 2026-09-07T23:00:39 UTC
- Internal: `news_items` table — CryptoBriefing, "Uniswap integrates AnchoredFi's tokenized stocks on Arbitrum", published 2026-09-07T15:21:59 UTC
- Internal: The Block (via intraday/swing report catalyst section), "STONK surges 250% to $140 million market cap as stock-paired Solana launchpad StonkFun pulls volume to Raydium and Jupiter" — date as captured in report, not independently re-fetched this cycle
- Internal: `data/catalysts/2026-09-08/catalyst_events.jsonl`, `narrative_baskets.jsonl`
- Previous review: [OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_2334.md](OPUS_ENRICHED_REVIEW_AUTO_2026-09-07_2334.md)

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak
- **issue:** Catalyst symbol-resolver mapping remains weak — 68.2% of today's 500 catalyst_events have no mapped symbol.
- **evidence:** `data/catalysts/2026-09-08/catalyst_events.jsonl` — 341/500 unmapped; sample misses include macro/bond-market wires (JGB yield moves, plane-crash investigation) that arguably shouldn't need crypto-symbol mapping at all, suggesting the denominator itself may be inflated by non-crypto wire noise rather than pure resolver failure.
- **suggested manual fix:** Audit whether the catalyst ingest pipeline should pre-filter obviously non-crypto macro wires before computing the mapped/unmapped ratio, separately from improving the symbol resolver itself for genuinely crypto-relevant unmapped items.
- **priority:** medium
- **first observed:** recurring across multiple recent cycles (see prior reviews); this run 2026-09-08 04:50 EEST.

### TODO-ray-usdt-signal-overlap
- **issue:** RAY/USDT has three overlapping `proposed_signals` rows spanning 2026-09-06T20:09–2026-09-07T02:11 UTC with inconsistent statuses (`triggered` still open on the oldest, `stale_before_entry` and `stopped` on two newer ones for the same symbol/direction).
- **evidence:** `db/crypto_ai_desk.sqlite`, `proposed_signals` table: `sig_2545637e5925f4c0` (triggered), `sig_aeaff50a6148b3be` (stale_before_entry), `sig_27c909d5cb4e26bc` (stopped) — all RAY/USDT long.
- **suggested manual fix:** Investigate whether the signal-issuance pipeline is minting duplicate/overlapping signals for the same symbol within a short window instead of recognizing an existing open signal — likely related to the previously-flagged watchlist-alert signal-reuse bug (TODO-3, raised high on 2026-07-17).
- **priority:** high
- **first observed:** contradiction visible across multiple cycles; row-level confirmation this run 2026-09-08 04:50 EEST.

### TODO-derivatives-oi-coverage-gap
- **issue:** Several `fallback_via_mexc` derivatives rows (IOST, AERO, SOLV, PENDLE and others) show OI 24h% as "n/a" — open-interest coverage is incomplete for MEXC-routed symbols, reducing the derivatives_squeeze agent's confidence for a meaningful share of tonight's candidates.
- **evidence:** `data/reports/intraday/2026-09-08_00-58_intraday_report.md` §3 — "OI 24h n/a%" appears on all `fallback_via_mexc` rows.
- **suggested manual fix:** Confirm whether MEXC's OI endpoint is unavailable/unwired for these symbols or whether the fallback path simply isn't populating the field, and wire it up or document the gap explicitly in the report template.
- **priority:** low
- **first observed:** 2026-09-08 04:50 EEST (likely present in prior cycles too, not previously called out explicitly in this section).
