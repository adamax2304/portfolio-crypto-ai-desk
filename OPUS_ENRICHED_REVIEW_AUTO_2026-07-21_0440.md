# Opus Enriched Review — Crypto Overnight / Asia Review — Auto Cycle 04:40 EEST

## 1. Executive Summary

**Advisory only — no auto-trade.** Slot: crypto overnight / Asia review (04:30 EEST, US stocks closed). Scheduler is fresh (scheduler.log + cycle_03_03-32_summary.md both mtime 04:36 EEST, well under the 3h defer threshold). Crypto book: bullish trend / risk-on on both intraday (breadth 67.4%) and swing (breadth 79.6%) timeframes — BTC/ETH both uptrend — but macro/geopolitical score sits at 100/100 risk-off headwind (Iran/Strait of Hormuz escalation), a real divergence between price action and macro backdrop. No A-tier crypto or stocks signals exist right now; crypto scalp is fully kill-switched, crypto intraday is demoted to C-tier by the Asia dead-zone guard (00–06 UTC), crypto swing is untouched and carries 5 actionable B-tier longs (HEMI, VIRTUAL, INJ, ZAMA, PENGU — all RS-leader momentum). Stocks are closed; a broad basket of A-scored shorts (NVDA 88, XLF 87, XLK 87, META 86, QQQ 82, LLY 81) is demoted to C/planning-only pending RTH confirmation — worth watching at the open. Catalyst mapping is weak this run (82% unmapped) — treat catalyst layer as context only. One data-quality finding carried forward and reconfirmed: INJ/USDT's "fresh catalyst" framing is now ~31h stale (source news_items row from 2026-07-19T18:25 UTC) — do not treat INJ as catalyst-fresh this cycle.

## 2. Data Used

- `data/reports/scalp/2026-07-21_00-40_scalp_report.md` (fresh, 03:40 EEST)
- `data/reports/intraday/2026-07-21_00-48_intraday_report.md` (fresh, 03:48 EEST)
- `data/reports/swing/2026-07-21_01-30_swing_report.md` (fresh, 04:30 EEST)
- `data/reports/stocks/intraday/2026-07-21_01-10_stocks_intraday_report.md` (fresh, 04:10 EEST)
- `data/reports/stocks/swing/2026-07-02_13-03_stocks_swing_report.md` (**stale**, 19 days old — excluded)
- `data/reports/stocks/invest/2026-07-02_13-05_stocks_invest_report.md` (**stale**, 19 days old — excluded)
- `data/catalysts/2026-07-21/catalyst_events.jsonl` (500 events), `narrative_baskets.jsonl` (5 baskets)
- `data/processed/llm_analysis_packet.md`, `llm_stocks_packet.md`
- CLI: `active-signals` (crypto 33 rows, stocks 50 rows), `signal-stats` (crypto + stocks), `detect_untracked_legacy_alerts` (0 findings)
- `db/crypto_ai_desk.sqlite` `news_items` direct queries (INJ, HEMI, SOL, ADA, PENGU, BONK freshness checks)
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_2330.md`
- External web research: not used this cycle — internal records were sufficient (fresh, consistent, and the divergences found were internal-data issues, not external-verification gaps).

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime 2026-07-21 04:36 EEST — fresh.
- `cycle_03_03-32_summary.md`: mtime 2026-07-21 04:36 EEST — fresh (this run does NOT defer).
- `crypto_monitor_1784597551.log`: actively appending, last line 04:40 EEST, watchlist re-scored this minute (PROM, ALLO, ADA, MUB, SYN, ACE, CRCLB, SNDKB, ETH, BONK all C/watchlist; BTC/RE/HOME/SPCXB/NIGHT rejected/no-trade) — monitor is alive.
- `derivatives_monitor_1784573174.log`: last line 04:39 EEST — alive.
- Swing/invest freshness: crypto swing fresh (<4h); stocks swing/invest **stale >14h** (19 days) — excluded from this run's actionable verdicts, carried as watchlist-only context.
- Paper/monitor status: crypto_monitor, derivatives_monitor, pending_monitor, mexc_canary_monitor all show recent `.pid`/log activity within the last cycle — no dead processes observed.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-21 04:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["stocks swing/invest reports (19d stale)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle summary mtime 04:36 EEST", "stocks swing/invest reports dated 2026-07-02"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_on", "mixed", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC/ETH uptrend, breadth 67.4% (intraday)/79.6% (swing)", "macro risk score 100/100 risk-off (Iran/Hormuz)", "stocks A-scored short basket NVDA/XLF/XLK/META/QQQ/LLY demoted to C, planning-only, market closed"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "stale_catalyst", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 500 total, 90 mapped/410 unmapped (82% unmapped)", "INJ news_items latest row 2026-07-19T18:25 UTC = ~31h old, reports still label it fresh", "ADA hard-fork news 2026-07-20T18:50 UTC = <24h fresh", "HEMI momentum_breakout basket explicitly flags symbols_overextended + avoid_chase, no news catalyst"] },
    { "agent": "derivatives_squeeze", "verdict": "ok", "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["CRCLB futures data unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZAMA/HEMI/PROM/ACE/KAITO: price+OI up, fresh positioning, crowding normal", "BANK: price up + OI down, short-covering (weaker continuation quality)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "entry_fresh", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HEMI +62.5% 24h, system's own momentum_breakout basket flags symbols_overextended + avoid_chase", "VIRTUAL/ZAMA 24h returns 6-9%, not overextended, swing B actionable"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 23 open-actionable (triggered/tp1/tp2, excl. 2 stale), 8 waiting_for_entry, 2 needs-review (ALLO/NEAR past expires_at)", "stocks: 41 open-position rows but US market closed (carry-forward only), 9 waiting_for_entry (pre-market planning)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BONK: exploiter still holds 2.4T tokens ($6.94M), -40% since Jul 6 hack, block_requires_operator_review active", "GOOGL/TSLA: earnings 2026-07-22 (tomorrow), do_not_chase_warning active", "ETH/SOL: exploit_hack risk flags (Allbridge $1.65M)"] },
    { "agent": "playbook_performance", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing 14d WR 72%/PF 5.80/+24R (strongest cohort)", "crypto B-tier all-mode winrate 31% low per system's own observation", "stocks C-tier winrate 15%, PF 0.73 — system flags this as weak", "weekend crypto signals underperform (WR 35%, n=32)"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate": { "symbol": "VIRTUAL/USDT", "trigger": "pullback into 0.636-0.647 entry zone already active (swing B, waiting_for_entry), RS-leader, not overextended", "reason": "RS-leader momentum score 80.5, 24h +6.6% (not extended), swing playbook 14d WR 72%/PF 5.80" },
    "best_short_candidate": { "symbol": "NVDA", "trigger": "RTH open confirmation — first 15-30min candle holds below 203.38, retest of breakdown level before entry", "reason": "highest-scored stocks short (87.8, was A, demoted to C only because market is closed) across a broad correlated short basket (XLF/XLK/META/QQQ/LLY)" },
    "best_catalyst_candidate": { "symbol": "ADA/USDT", "trigger": "already triggered B-tier intraday long (score 67.4-67.7), hold above invalidation 0.167-0.168", "reason": "genuinely fresh (<24h) Cardano hard-fork news (2026-07-20T18:50 UTC), unlike INJ whose catalyst framing is stale" },
    "avoid_candidate": { "symbol": "BONK/USDT", "reason": "ongoing exploit overhang — drainer still holds 2.4T tokens ($6.94M unsold), price -40% since the Jul 6 hack, operator-review flag active" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.75 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.65 | risk_on, mixed, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, stale_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, entry_fresh, clean_retest | advisory_only |
| execution_lifecycle | caution | 0.70 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, manual_review | advisory_only |
| playbook_performance | ok | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | longs_preferred, wait_for_trigger | advisory_only |

## 4. What Changed vs Previous Review

Comparing to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_2330.md` (23:30 EEST):

- **New:** HEMI/USDT has emerged as the dominant momentum story (+62.5% 24h), but the system's own `momentum_breakout` basket immediately flags it `symbols_overextended` + `avoid_chase` — not present as a headline theme in the prior review.
- **New:** ADA/USDT now carries a genuinely fresh (<24h) catalyst (Cardano hard fork) and has a triggered B-tier intraday long — a cleaner catalyst-backed candidate than the prior review's HYPE/USDT pick (which is not mentioned in this cycle's top reports).
- **Confirmed/escalated:** INJ/USDT catalyst staleness — prior review's `TODO-catalyst-freshness-not-rechecked-on-open-positions` (flagged at ~26h stale) is now ~31h stale and the reports still label it "fresh attention/catalyst detected" — same root cause, now a 2nd consecutive cycle observation.
- **Confirmed:** `TODO-signal-staleness-display` (ALLO/NEAR past `expires_at` still shown as live `tp1_hit`) persists unchanged — now the 5th+ consecutive cycle.
- **Confirmed:** `TODO-nvda-avgo-self-invalidation-lag` persists — AVGO scores `no_directional_setup` (40.69) again this cycle while `active-signals` still shows it `triggered` C-tier.
- **Changed:** stocks mood — prior review read risk-off (mild, VIX 18.46, broad down day). This cycle (pre-market, Asia hours) shows a **broad A-scored short basket** (NVDA/XLF/XLK/META/QQQ/LLY) all demoted to C only because the market is closed — a stronger, more directional risk-off tilt heading into the next RTH session than the prior review's "mild" read, worth confirming at the open.
- **Unresolved from prior review:** UNH (legal/DOJ), TSLA/GOOGL (earnings 2026-07-22, now tomorrow) still carry the same caution flags.

## 5. Catalyst Coverage

- Total catalyst events today: 500
- Mapped (symbol resolved): 90
- Unmapped (null symbol): 410
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (82% unmapped)
- Narrative baskets: 5 (`delisting_thin_liquidity`, `rwa_narrative`, `perps_dex_narrative`, `ai_narrative`, `momentum_breakout`)
- Top 3 unmapped headlines:
  1. "MEXC to Delist STM and WULF USDT-M Stock Futures #Delistings"
  2. "Delisting of UTYAUSDT Perpetual Futures Pair [Jul 23, 2026, 13:00 UTC]"
  3. "IREN raises AI cloud revenue target above $4B on $2.8B in new multi-year contracts"

## 6. Market Landscape

Crypto: BTC/ETH both uptrend, altcoin breadth 67.4% (intraday) / 79.6% (swing) above EMA20 — broad-based risk-on tape. Strongest symbols this cycle: ZAMA, HEMI, PROM, CRCLB, ACE, BANK, KAITO (all RS-leaders vs BTC). Weakest: NIGHT, TLM, HOME, RE, SPCXB — all short candidates but every one is capped by the system's own short-squeeze-risk / audit-cap gate (shorting into a bullish tape). Macro overlay is a genuine divergence: macro/geopolitical risk score is 100/100 risk-off (Iran retaliatory strikes, Strait of Hormuz tanker incident, oil at 1-month highs) even as crypto price action stays firmly bullish — a backdrop that could invalidate the risk-on read quickly if it escalates.

Stocks: market closed (Asia slot). The freshest stocks intraday scan (04:10 EEST) produced a broad, correlated short basket that would have been A-tier if the market were open: NVDA (87.8), XLF (87.2), XLK (86.7), META (85.5), QQQ (82.3), LLY (81.4) — all demoted to C/"planning only" purely because of the `market_closed_intraday_planning_only` gate, not because the underlying setups failed. This is a coherent tech/financials/healthcare-led short thesis to watch for confirmation at the US open. AVGO, by contrast, genuinely self-invalidated (`no_directional_setup`, 40.69) for a repeat cycle — do not confuse it with the NVDA/XLF/XLK/META/QQQ/LLY basket.

### Market Mood / Risk Routing

- Crypto mood: **risk-on** (BTC/ETH uptrend, broad breadth, but macro geopolitical overlay at max risk-off reading — treat as risk-on with a macro tail-risk caveat)
- Stocks mood: **closed** — pre-market read leans risk-off (broad A-scored short basket across tech/financials/healthcare), unconfirmed until RTH
- Dominant narrative: `momentum_breakout` (HEMI, no news catalyst, overextended, avoid-chase) is the loudest "where money is flowing" signal; `perps_dex_narrative` (HYPE) freshness <1h but no open position; Iran/Hormuz geopolitical risk is the dominant macro overlay
- Preferred side now: **longs (crypto, selective)** / **wait-for-trigger (stocks, pending RTH)**
- Best long candidate: VIRTUAL/USDT (swing B, RS-leader, not overextended) — see §8
- Best short candidate: none clean in crypto (bullish tape caps every short); NVDA (stocks, planning-only until RTH confirms) — see §8
- Best catalyst-backed candidate: ADA/USDT (Cardano hard fork, <24h fresh, triggered B-tier intraday long) — see §8
- What to avoid: BONK/USDT (exploit overhang), chasing HEMI at +62.5% 24h, treating INJ as catalyst-fresh (it's ~31h stale)
- What would change the view: Iran/Hormuz de-escalation or further escalation; RTH confirmation (or failure) of the NVDA/XLF/XLK/META/QQQ/LLY short basket; a fresh (<6h) catalyst actually landing on HEMI to justify the extension; GOOGL/TSLA earnings tomorrow (2026-07-22) resolving current caution flags

## 7. Candidate Deep Dives

**1. VIRTUAL/USDT (crypto, B-tier swing, score 69.4, waiting_for_entry) — best actionable long**
- Has price already reacted to a catalyst? No catalyst found in `news_items` for VIRTUAL in the last 24h — this is a pure RS/momentum play, not catalyst-backed.
- Chasing? No — 24h +6.6%, 7d +18.3%, not overextended (contrast with HEMI's +62.5%/overextended flag).
- Retest/pullback structure? Entry zone 0.636-0.647 is the system's own waiting_for_entry band — treat that as the actionable retest zone.
- Overextended (>2 ATR from EMA20)? No indication in the report; not flagged.
- Would entry now be late? No — still waiting_for_entry, not yet triggered.
- Actionable now or after confirmation? Actionable per the system's own swing playbook (14d WR 72%/PF 5.80/+24R, strongest crypto cohort) — but this is a B-tier system-generated signal, apply normal position sizing discipline, not proof it will work.
- Aligned with mood? Yes — risk-on tape, RS-leader long, swing playbook is the desk's best-performing mode.
- Invalidation: 0.6361 (per active-signals row).
- Chase risk: low. Catalyst confirmation/contradiction: none — momentum-only thesis.

**2. NVDA (stocks, was-A intraday short, now C/planning-only, score 87.8) — best short-watch**
- Price reaction: N/A, market closed since the scoring.
- Chasing? Cannot assess until RTH — this is a pre-market/overnight read only.
- Retest structure: entry band 203.38-204.72 per active-signals; invalidation 206.06.
- Would entry now be late? Yes if attempted now — cash market is closed; this is planning-only per the system's own `market_closed_intraday_planning_only` cap.
- What makes it actionable: first 15-30min of RTH holding below the entry band with no gap-fill reclaim, ideally alongside XLF/XLK/META/QQQ/LLY confirming the same direction (correlated basket, not an isolated single-name bet).
- Legal/headline risk: none found — recent NVDA headlines are constructive (Nebius stake disclosure, Jensen Huang's Nvidia framing), which is itself a point of tension against the short thesis; no earnings/legal red flag though.
- Aligned with mood? Consistent with the broader risk-off pre-market short-basket read; contradicted by the crypto risk-on tape and constructive NVDA headlines — treat with caution, do not chase into the open.

**3. ADA/USDT (crypto, B-tier intraday, score 67.4-67.7, triggered) — best catalyst-backed candidate**
- Catalyst check: Cardano hard fork ("Van Rossum", first community-voted upgrade) reported by Decrypt and CoinDesk, both dated 2026-07-20 (14:31 and 18:50 UTC) — genuinely <24h fresh as of this review.
- Has price reacted? Position is already triggered (entry 0.169-0.170), so yes, some reaction priced in already.
- Chasing? Score sits mid-range (67-68), not an extreme move; no overextension flag in the report.
- Actionable now or after confirmation? Already triggered — this is a manage-the-position case, not a fresh entry decision. Invalidation ~0.167-0.168.
- Catalyst confirmation: confirmed via two independent, dated, named sources — stronger sourcing than most of this cycle's catalyst pool (82% of which is unmapped).

**4. AVGO (stocks, C-tier, score 90.7 in active-signals but freshest scan says `no_directional_setup` 40.69) — needs review, not a clean candidate**
- This is the recurring `TODO-nvda-avgo-self-invalidation-lag` case: the active-signals row is stale relative to the system's own freshest verdict. Do not treat the 90.7 score as current — the latest scan explicitly disagrees.
- Aligned with mood? Undetermined — the system itself has no directional view on AVGO right now.

**5. BONK/USDT (crypto, C-tier watchlist, score 50.8 per monitor) — avoid**
- Ongoing exploit overhang: the treasury drainer still holds 2.4T BONK (~$6.94M), has sold ~$21.2M+ already, price down ~40% since the July 6 incident. `block_requires_operator_review` flag is active.
- Not aligned with the risk-on long bias — this is a single-name idiosyncratic risk, not a market-mood-driven setup. Avoid new longs; a short thesis would need to weigh against the broader bullish tape (squeeze risk).

## 8. Best Candidates Ranked

1. **Long-watch: VIRTUAL/USDT** — trigger: hold/enter 0.636-0.647 (already the system's waiting_for_entry band), invalidation 0.6361, aligned with risk-on RS-leader thesis, not overextended.
2. **Catalyst-watch: ADA/USDT** — already triggered (0.169-0.170), manage toward invalidation 0.167-0.168; genuinely fresh <24h Cardano hard-fork catalyst, unlike INJ's stale framing.
3. **Short-watch: NVDA (+ correlated basket XLF/XLK/META/QQQ/LLY)** — trigger: RTH open, first 15-30min candle confirming below 203.38-204.72 without a gap-fill reclaim; planning-only until then.
4. **Long-watch (chase risk, do not enter fresh): HEMI/USDT** — trigger: a genuine pullback into a defined entry zone after the +62.5% 24h move cools; the system's own basket tags it `avoid_chase` right now.
5. **Avoid: BONK/USDT** — ongoing exploit-driven sell pressure, operator-review flag active.

## 9. Avoid / No Trade

This decision window only — never a command to stop the system:
- BONK/USDT: exploit overhang, operator-review flag.
- Chasing HEMI/USDT at current extension (+62.5% 24h, system-flagged overextended).
- Treating INJ/USDT as catalyst-fresh (it is not — ~31h stale).
- Any new stocks intraday entry before RTH confirmation (market is closed).
- GOOGL/TSLA: earnings tomorrow (2026-07-22) — do-not-chase warning active on both.

## 10. Main Risks

- Macro/geopolitical risk score at 100/100 (Iran retaliatory strikes, Strait of Hormuz tanker incident) is a real tail risk to the crypto risk-on read — a further escalation could flip the tape quickly.
- Catalyst mapping is weak (82% unmapped) this run — narrative-driven decisions should lean on directly-verified news_items rather than the raw catalyst feed.
- Two known data-integrity gaps persist unresolved across multiple cycles: signal-staleness display (ALLO/NEAR past expiry still shown live) and NVDA/AVGO self-invalidation lag (stale active-signals rows vs. the system's own freshest verdict) — see §14.
- GOOGL and TSLA both report earnings tomorrow (2026-07-22) — gap risk on any carried position.
- Weekend-mode crypto signals underperform per the system's own stats (WR 35%, n=32) — apply extra caution to any weekend-flagged row.

## 11. Action Plan — next 4 hours

- Monitor VIRTUAL/USDT and ADA/USDT positions per their existing invalidation levels; no new entries needed, both already actionable/triggered.
- Do not chase HEMI/USDT; wait for a defined pullback structure before considering entry.
- Watch Iran/Hormuz headlines for escalation — this is the most likely near-term catalyst to flip the crypto risk-on read.
- Ahead of the EU morning slot (11:30 EEST), re-check whether the NVDA/XLF/XLK/META/QQQ/LLY short basket is still coherent and whether any pre-market data has emerged.
- No action needed on BONK/AVGO beyond continued avoid/no-directional-view labeling.

## 12. Final Verdict per Mode

- **Crypto scalp:** disabled (kill-switch, all hours) — no verdict needed.
- **Crypto intraday:** demoted to C-tier by the Asia dead-zone guard (00-06 UTC) — watchlist only this slot, per design (not a bug).
- **Crypto swing:** actionable — 5 B-tier longs (HEMI, VIRTUAL, INJ, ZAMA, PENGU), all RS-leader momentum; VIRTUAL is the cleanest (least extended).
- **Stocks intraday:** planning-only (market closed) — broad short basket (NVDA/XLF/XLK/META/QQQ/LLY) to watch at RTH open; AVGO explicitly no-directional-view.
- **Stocks swing/invest:** stale data (19 days) — excluded from this cycle's verdict, needs a fresh report before being usable again.

## 13. Sources

- [Injective highlights SEC registration, Robinhood listing for INJ at Summit](https://cryptobriefing.com/injective-sec-registration-robinhood-listing-summit/) — CryptoBriefing, 2026-07-19 (internal news_items row; used to demonstrate staleness, not as a fresh catalyst)
- [Cardano Triggers Hard Fork With First Community-Voted Upgrade](https://decrypt.co/373858/cardano-van-rossem-hard-fork-live-community-upgrade) — Decrypt, 2026-07-20
- [Inside Cardano's 'Van Rossum' hard fork, and what it means for users](https://www.coindesk.com/markets/2026/07/20/inside-cardano-s-van-rossum-hard-fork-and-what-it-means-for-users) — CoinDesk, 2026-07-20
- [Morgan Stanley files for low-fee Solana ETF as SBI launches tokenized fund in Japan](https://cryptobriefing.com/morgan-stanley-files-for-low-fee-solana-etf-as-sbi-launches-tokenized-fund-in/) — CryptoBriefing, 2026-07-20
- Nebius rises as Nvidia discloses 9.3% stake — Seeking Alpha Market Currents, 2026-07-20 (URL not captured in internal record; source unavailable for direct link)
- Internal: `catalyst_events.jsonl`, `narrative_baskets.jsonl`, `news_items` table (db/crypto_ai_desk.sqlite) — 2026-07-21
- No new external sources ingested this cycle — all citations above are pre-existing `news_items` rows read directly, not fresh WebSearch/WebFetch results, so `scripts.ingest_enriched_review_sources` was not run (nothing new to upsert).

## 14. Fix Requests / TODO

### TODO-signal-staleness-display
- **issue:** ALLO/USDT (`sig_10088a4c71cae845`, expired 2026-07-19T15:21) and NEAR/USDT-short (`sig_b16bb9e54598333a`, expired 2026-07-17T15:56) are still returned by `active-signals` as live `tp1_hit` rows, well past their own `expires_at`. Same pair flagged across 5+ consecutive review cycles now.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` this run, same two rows; prior reviews `2026-07-19_2153`, `2026-07-20_1848`, `2026-07-20_2147`, `2026-07-20_2330` all flag the identical pair.
- **suggested manual fix:** investigate whether `active-signals` should filter/label rows past `expires_at`; may share a root cause with the previously-confirmed watchlist-alert/signal-reuse bug on ALLO/BANK.
- **priority:** high
- **first observed:** 2026-07-19 21:53 EEST (5th+ consecutive cycle unresolved)

### TODO-nvda-avgo-self-invalidation-lag
- **issue:** AVGO short setup self-invalidated again this cycle (`no_directional_setup`, score 40.69, `data/reports/stocks/intraday/2026-07-21_01-10_stocks_intraday_report.md`), but `active-signals` still shows it as `triggered` C-tier at score 90.7 (`sig_48899bb488411af9`). Same pattern flagged for 3+ consecutive cycles now.
- **evidence:** current stocks intraday report §Rejected/Not Ready vs. `active-signals --asset-class stocks` row `sig_48899bb488411af9`.
- **suggested manual fix:** consider whether `active-signals` should cross-check the latest report's per-symbol verdict and annotate/suppress rows the newest scan has already contradicted.
- **priority:** medium (consider escalating to high — this is now 4+ cycles)
- **first observed:** 2026-07-20 18:48 EEST

### TODO-catalyst-freshness-not-rechecked-on-open-positions
- **issue:** INJ/USDT's swing and intraday reports both describe its catalyst as "fresh attention/catalyst detected," but the underlying `news_items` row (SEC registration/Robinhood listing, CryptoBriefing) is dated 2026-07-19T18:25 UTC — by this review's query time (2026-07-21 01:44 UTC) it is ~31.3h old, well outside the system's own 24h freshness window. This is the same issue flagged in the prior review (then ~26h stale) — now a 2nd consecutive cycle, and the gap is widening rather than resolving.
- **evidence:** direct `news_items` query this run (`db/crypto_ai_desk.sqlite`) — INJ's latest row is 2026-07-19T18:25:08+00:00; `data/reports/swing/2026-07-21_01-30_swing_report.md` and `data/reports/intraday/2026-07-21_00-48_intraday_report.md` both still label INJ catalyst-fresh.
- **suggested manual fix:** open positions with a catalyst-backed thesis should have that freshness re-checked on each cycle rather than relying on a scoring-time snapshot that silently ages during the hold.
- **priority:** medium (raised from low — now recurring across 2 cycles)
- **first observed:** 2026-07-20 23:30 EEST
