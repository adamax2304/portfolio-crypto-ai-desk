# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:46 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context (advisory only / no auto-trade).** Today is **Saturday** — US stocks are closed all day (weekend, no cash session at all today), so this cycle is crypto-actionable / stocks-planning-for-Monday only; the usual "build the US-session watchlist" framing does not apply until the Sunday-evening/Monday pre-market cycles. Scheduler is fresh (`scheduler.log` 11:37 EEST, ~9m old) — no defer. Freshest crypto reads (scalp 08:07 EEST / ~1h39m old, intraday 08:20 EEST / ~1h26m old) still show **market regime: transition (mixed)** — BTC/ETH both trend "range", altcoin breadth only 33.3%/62.5% above EMA20/50 — unchanged from the 04:40 overnight review. Macro/geopolitical risk has **eased from 100/100 (05:33 swing) to ~75/100** (scalp/intraday, unchanged framing: Iran/Israel tensions, US sanctions expansion, missile-stock commentary) — still a risk-off headwind but less acute than overnight. No fresh A/B signals fired this cycle in any crypto mode (scalp/intraday/swing all show "No A-tier / No B-tier setups found") — same book-only-carried-risk picture as 04:40. The **TUT/ONG bias-tag contradiction carried over from the last 6+ cycles has partially resolved**: **ONG/USDT has flipped from -15.1% to +15.9% 24h** (now in the "Strongest Symbols" / unusual-volume list, tagged overextended, funding still negative → a short squeeze in progress, not a contradicted long anymore) while **TUT/USDT is still bias=short but the adverse move has steadily moderated** (-20.5% → -14.4% → -12.6% → -12.0% across the last four cycles) — improving but still unresolved. `TRUMP/USDT`, last cycle's best-long-watch, **never filled and is now `entry_moved_away`** — no longer a clean watch idea. `RE/USDT` remains the desk's only `waiting_for_entry` swing long. `detect_untracked_legacy_alerts` again shows **zero** new untracked crypto alerts today — third consecutive clean read. Catalyst mapping is **63.6% unmapped** (864/1,359 events) — above the 50% "weak" trigger threshold, so still flagged context-only, but improving vs the ~69-71% seen in recent cycles. A new data-hygiene issue was found directly in the DB: **15 stocks C-tier `triggered` rows are stuck weeks past their `expires_at`** (oldest from 2026-07-20, one from 2026-08-03/04) without resolving to a closed state — watchlist/research-only, not Telegram-actionable, but a genuine pipeline gap. Scanning, tracking, and the scheduler continue as normal regardless of this window's verdict.

## 2. Data Used

- Crypto scalp report: `data/reports/scalp/2026-08-29_08-07_scalp_report.md` (11:07 EEST file mtime / data freshness ~08:00 EEST, ~1h39m old — **freshest**)
- Crypto intraday report: `data/reports/intraday/2026-08-29_08-20_intraday_report.md` (11:20 EEST mtime, ~1h26m old — **freshest**)
- Crypto swing report: `data/reports/swing/2026-08-29_02-33_swing_report.md` (05:33 EEST, ~6h13m old — **carry-forward**, still referenced for TUT bias-tag continuity)
- Stocks intraday report: `data/reports/stocks/intraday/2026-08-28_18-54_stocks_intraday_report.md` (21:54 EEST Aug 28, ~13h52m old — **carry-forward/stale band**; market closed all weekend regardless, planning-only for Monday)
- Stocks swing/invest reports: both dated 2026-07-02 — deprecated pipeline per `project_crypto_ai_desk_stocks_position_framework` memory, excluded
- `data/processed/llm_analysis_packet.md` (11:22 EEST, fresh); `data/processed/llm_stocks_packet.md` (21:56 EEST Aug 28, carry-forward)
- `data/catalysts/2026-08-29/catalyst_events.jsonl` (1,359 rows, direct-counted: 495 mapped / 864 unmapped), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_08-26.md`
- CLI: `active-signals --asset-class crypto` (50 rows shown, 53 total live), `active-signals --asset-class stocks` (50 rows, all resolved/historical), `signal-stats --asset-class crypto` (sample=384), `signal-stats --asset-class stocks` (sample=13 headline / 585 C-tier), `detect_untracked_legacy_alerts --since 2026-08-29`
- Direct read-only SQL against `db/crypto_ai_desk.sqlite`: `proposed_signals` (TUT/ONG/TRUMP/RE current status+invalidation; open-position counts by asset_class/direction/status; stale-triggered stocks C-tier audit)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-29_0440.md` (crypto overnight / Asia review, 04:40 EEST)
- **External web research not used this run** — internal reports, catalyst layer, and direct SQL were sufficient and internally consistent for every candidate reviewed; no candidate's verdict depended on unverified external claims.
- **TradingView / manual chart check unavailable** — all technical reads taken directly from report-stated OHLCV/ATR/EMA/RS/funding/OI fields and direct DB queries.

## 3. Scheduler / Data Freshness

- `scheduler.log`: 2026-08-29 11:37 EEST (~9m old) — **fresh**.
- Latest `cycle_*_summary.md`: `cycle_05_07-44` (written 08:54 EEST) — ~2h52m old; scheduler.log itself is fresh so no defer per the "both stale" rule.
- Crypto scalp: 08:07 EEST data freshness (~1h39m) — **fresh**.
- Crypto intraday: 08:20 EEST data freshness (~1h26m) — **fresh**.
- Crypto swing: 05:33 EEST (~6h13m) — **carry-forward** (4-12h band); TUT bias-tag detail confirmed still present in fresher scalp/intraday reads too, so no material staleness risk this cycle.
- Stocks intraday: 21:54 EEST Aug 28 (~13h52m) — carry-forward/borderline-stale band; market closed all weekend regardless.
- Stocks swing/invest: 2026-07-02 — stale/deprecated, excluded.
- No monitor-process-uptime file was read this run (not in the allowed CLI/read list).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-08-29 11:46 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["swing report ~6h old, only carry-forward source for some TUT derivatives detail (though bias tag itself confirmed fresher)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 11:37 EEST", "scalp/intraday reports both ~1.5h old", "swing report 05:33 EEST is ~6h13m old (carry-forward band)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mixed", "chop", "risk_off", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["market regime: transition (mixed) unchanged since overnight; BTC/ETH both trend range", "altcoin breadth 33.3%/62.5% above EMA20/50", "macro/geopolitics risk eased 100→~75/100 but still risk-off headwind (Iran/Israel tensions, US sanctions expansion)", "active book remains 100% long, zero shorts armed"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["63.6% unmapped in catalyst_events.jsonl (864/1359), improving vs ~69-71% in recent cycles", "5 active narrative baskets (rwa, perps_dex, ai, binance_ecosystem, momentum_breakout)", "top unmapped headlines are sector-wide/stablecoin-flow/macro, not single-asset (USDC mint, browser-extension malware, SBI/JPYSC stablecoin)", "SOL/USDT still the only active signal with a traceable fresh catalyst"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "oi_contradicts", "funding_extreme"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONG/USDT: price +15.93% 24h, volume 2.13x, but funding still negative (bybit -0.00119, mexc -0.000673) — classic short-squeeze signature, tagged 'overextended' (>2 ATR from EMA20, do-not-chase for new entries)", "TUT/USDT: still bias=short but 24h move improving (-20.5%→-14.4%→-12.6%→-12.0%), funding -0.000627, OI +9.01% (fresh shorts pressing, squeeze risk if price reclaims)", "TUT short setup itself capped to C tier on high_upper_wick_short_squeeze_risk (score 48.1) — neither side clean"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["stale_before_entry", "entry_late", "price_moved_away", "chase_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/USDT swing long (last cycle's best-long-watch) is now status=entry_moved_away — never filled, price left the zone", "RE/USDT swing long remains the only waiting_for_entry crypto row (zone 0.5682-0.5745, invalidation 0.5606)", "51 of 53 active crypto rows already status=triggered, most 3-8 days into a swing validity window scored under a more bullish regime read", "no new A-tier or B-tier setups fired in scalp, intraday, or swing this cycle"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.65,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 51 open_actionable (triggered) + 2 waiting_for_entry (RE + 1 other) rows, 0 shorts armed", "stocks: 6 long + 9 short status=triggered rows, but ALL are C-tier (watchlist/research, not Telegram-actionable) and stuck weeks past their expires_at (oldest 2026-07-20) — a pipeline-hygiene gap, not live exposure", "TUT/ONG both still status=triggered, not stopped, despite historically adverse moves — unresolved but ONG's move has now reversed favorably"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["repeated_losses", "correlation_cluster", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TUT/USDT open long still contradicted by bias=short tag, 6th+ consecutive cycle, though adverse move is decelerating", "ONG/USDT contradiction has effectively resolved itself (price reversed +15.9% 24h) — downgrade from AVOID to WATCH/monitor-for-exhaustion", "book remains 100% long with zero diversification into shorts in a still-mixed regime", "VRT (stocks) still carries the Pomerantz Law Firm legal-risk flag from 2026-08-27, unchanged, market closed so no new action needed"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["low_sample", "playbook_working", "playbook_failing"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto headline actionable (A/B): sample=384, winrate 10.71%, PF 1.144, avgR 0.0359, totalR +10.8R — thin but positive edge, unchanged from overnight", "one crypto mode bucket in the by-mode breakdown shows PF≈0.0, 0 wins/11 losses, totalR≈-10.x — a reliably losing bucket worth root-causing", "stocks headline sample=13 (weak confidence), winrate 60%, PF inf, totalR +12.0R — too small to trust", "stocks C-tier watchlist: sample=585, PF 0.4, 14W/8L, totalR -6.0R — consistent with prior reviews' 'reliably poor' C-tier read"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "RE/USDT", "trigger": "confirmed fill in zone 0.5682-0.5745 with volume; invalidate below 0.5606", "reason": "only remaining waiting_for_entry crypto row now that TRUMP/USDT has moved away from its zone; hasn't chased yet" },
    "best_short_candidate":    { "symbol": "TUT/USDT", "trigger": "watch only — desk's own scanner already caps a TUT short to C on high_upper_wick_short_squeeze_risk; would need a clean low break on rising volume with no upper-wick rejection", "reason": "still the desk's clearest bearish-bias name, though the adverse move against the open long is decelerating, not accelerating" },
    "best_catalyst_candidate": { "symbol": "SOL/USDT", "trigger": "RS vs BTC/market turning positive (still weak_vs_market per swing report) before treating the DeFi Development 'State of Solana' catalyst as tradeable strength", "reason": "only active signal with a traceable fresh news catalyst; unchanged from overnight" },
    "avoid_candidate":         { "symbol": "ONG/USDT", "reason": "no longer a bias contradiction (price reversed +15.9% 24h) but now tagged overextended (>2 ATR from EMA20) with negative funding despite the pump — classic squeeze-exhaustion setup; do not chase a new long here, and treat the open position's gains as fragile, not confirmed trend" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.70 | mixed, chop, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, oi_contradicts, funding_extreme | advisory_only |
| technical_entry | caution | 0.60 | stale_before_entry, entry_late, price_moved_away, chase_risk | advisory_only |
| execution_lifecycle | needs_review | 0.65 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.65 | repeated_losses, correlation_cluster, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | low_sample, playbook_working, playbook_failing | advisory_only |
| head_trader | watch_only | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

(vs `OPUS_ENRICHED_REVIEW_AUTO_2026-08-29_0440.md`, 04:40 EEST crypto overnight / Asia review)

- **Improved / effectively resolved:** ONG/USDT's bias-tag contradiction has flipped — 24h move went from -15.12% (04:40) to +15.93% (current intraday report), now in "Strongest Symbols" with 2.13x volume. The open long is no longer fighting the tape; the new concern is the opposite one (chasing an overextended, funding-negative squeeze).
- **Improving but still open:** TUT/USDT's adverse move has decelerated across four consecutive report reads: -20.47% → -14.41% → -12.56% → -11.97%. Bias tag is still "short" against the open long, so the TODO stays open, downgraded from "escalating" to "improving."
- **New negative:** TRUMP/USDT (04:40's best-long-watch) never filled — `status` is now `entry_moved_away`. Replaced as best-long-watch by RE/USDT, the desk's only remaining `waiting_for_entry` crypto row.
- **Unchanged:** No new A/B setups fired in any crypto mode this cycle (same as 04:40 and every cycle since Aug 28 19:59 EEST's DEXE tier-up).
- **Improved:** Macro/geopolitical risk score eased from 100/100 (05:33 swing) to ~75/100 (08:07-08:20 scalp/intraday) — still risk-off framing (Iran/Israel tensions, US sanctions on Iran) but less acute.
- **Improved:** Catalyst mapping 63.6% unmapped (864/1359), down from ~69-71% in the last several cycles — still above the useful-decision-grade bar but trending the right direction.
- **Unchanged:** `detect_untracked_legacy_alerts --since 2026-08-29` still returns zero rows — third consecutive clean read (00:00, 04:40, now 11:46 EEST) — the untracked-alert TODO can likely be downgraded further if it stays clean through Monday's active session.
- **New finding (this run):** direct DB audit of stocks `proposed_signals` found 15 C-tier `triggered` rows stuck weeks past their `expires_at` (oldest created 2026-07-20, one from 2026-08-03/04) without transitioning to a resolved status — watchlist/research-only, no live-exposure impact, but a genuine pipeline gap not previously flagged in recent reviews.
- **Regime:** unchanged at "transition (mixed)" since 22:37 EEST Aug 28 — no material shift across the whole overnight-into-morning window.

## 5. Catalyst Coverage

- Total catalyst events today (`catalyst_events.jsonl`, direct count): **1,359**
- Mapped (non-null symbol): **495** (36.4%)
- Unmapped (null symbol): **864** (63.6%)
- `narrative_baskets.jsonl`: **5** baskets (rwa_narrative, perps_dex_narrative, ai_narrative, binance_ecosystem_teaser, momentum_breakout)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (63.6% unmapped is above the 50% "weak" threshold, though improving vs recent cycles.)
- Top unmapped headlines (no symbol resolved), by frequency:
  1. "💵 250,000,000 $USDC (249,993,124 USD) minted at USDC Treasury" — stablecoin-mint flow, no single-asset attribution
  2. "📉 Malicious Chrome and Edge extensions targeted crypto wallets and crypto platform logins" — sector-wide security risk
  3. "LATEST: 🇯🇵 SBI Holdings plans to buy a 20% stake in Indonesian brokerage Ajaib Group for $270M to expand its yen-pegged JPYSC stablecoin" — macro/corporate, no listed-asset match
  4. "LATEST: 🇺🇸 California's Senate has unanimously passed a bill that would ban platforms from listing public officials' memecoins..." — regulatory/sector-wide, not single-symbol

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed / chop** (transition regime, BTC/ETH both range, breadth 33.3%/62.5% >EMA20/50), macro risk-off headwind **easing** (100→~75/100) but not cleared.
- Stocks mood: **closed** (Saturday, no session today at all) — Friday's close context (VRT legal-risk short, CRCL demoted A→C via short_bounce_guard, LLY positive FDA/Mounjaro news) carries forward as Monday-planning context only.
- Dominant narrative: momentum/relative-strength continuation, same as overnight — only SOL/USDT carries a traceable fresh catalyst (still weak-vs-market technically); ONG/USDT's reversal is derivatives-driven (squeeze), not catalyst-driven.
- Preferred side now: **wait-for-trigger / selective longs only** — book remains 100% long with zero shorts armed; the regime hasn't confirmed a return to "bullish trend" (breadth still <65% above EMA20), so treat existing longs as carried risk, not fresh conviction.
- Best long candidate: **RE/USDT** (waiting_for_entry, zone 0.5682-0.5745, invalidation 0.5606) — the one clean pre-entry idea left after TRUMP/USDT moved away.
- Best short candidate: **none armed** — TUT/USDT remains the closest short-watch, still capped to C on squeeze risk.
- Best catalyst-backed candidate: **SOL/USDT** — same as overnight, still weak-vs-market technically.
- What to avoid: **new ONG/USDT longs** (chasing an overextended, funding-negative squeeze) and **new stocks positions** (market closed).
- What would change the view: a fresh swing scan confirming TUT's bias tag has flipped too (like ONG's did); BTC/ETH breaking range in either direction; breadth crossing back above ~50%/70% to re-confirm "bullish trend"; Monday pre-market stocks data for VRT/CRCL/LLY.

## 7. Candidate Deep Dives

### 7.1 ONG/USDT (swing long, B, score 73.9, `triggered`) — WATCH / MONITOR FOR EXHAUSTION (downgraded from AVOID)
- Entry 0.09561-0.09824, stop/invalidation 0.09240, TP1 0.10700. Created 2026-08-26T02:59 UTC.
- Has price already reacted to a catalyst? No catalyst exists — pure relative-strength/momentum move; now in the intraday report's "Strongest Symbols" (score 87.2, 24h +15.93%, RS vs BTC +18.45%, volume 2.13x) and flagged "unusual_volume" with tags relative_strength, volume_expansion, breakout, **overextended**.
- Is the setup chasing? For a *new* entry, yes — the rejected-setups section explicitly disqualifies a fresh ONG long on "Price is more than 2 ATR from EMA20; do not chase." The *existing* open long benefits from the move but should not be treated as freshly confirmed trend.
- Retest/pullback structure? Not observable without a fresher chart read; no pullback yet visible in the report.
- Overextended? Yes, explicitly flagged (>2 ATR from EMA20).
- Would a new entry now be late? Yes — this is a "don't chase" setup per the desk's own rejection logic.
- Aligned with current market mood? Mixed — bullish on this single name, but funding is still negative (bybit -0.00119, mexc -0.000673) despite the +15.9% pump — a squeeze signature (shorts still positioned against the move), which can reverse sharply once exhausted.
- Long, short, or wait-for-trigger? Existing long only; no new size recommended in either direction.
- Actionable now or after confirmation? The open position's prior bias-contradiction concern has resolved; new concern is squeeze-exhaustion risk. Downgrade from "manual review required" to "monitor" — no longer an urgent TODO, but keep watching funding/OI for a reversal signal.
- Invalidation: 0.09240 — not at risk given the favorable move; if anything, consider whether the desk should trail protection (out of scope for this advisory review).
- Catalyst confirmation or contradiction? No catalyst; purely technical/derivatives-driven (short squeeze).

### 7.2 TUT/USDT (swing long, B, score 69.2, `triggered`) — WATCH / IMPROVING, still contradicted
- Entry 0.05164-0.05250, stop/invalidation 0.05058, TP1 0.05539. Created 2026-08-27T04:46 UTC.
- 24h move improving across four consecutive reads: -20.47% (04:40) → -14.41% (05:33 swing) → -12.56% (08:20 intraday) → -11.97% (08:07 scalp, most recent). RS vs BTC -9.49% (most recent), funding -0.000627, OI +9.01% (fresh shorts pressing — squeeze risk if price reclaims), volume 0.02x (very thin).
- Report bias tag: still **short** (score 80.2), directly contradicting the open long — 6th+ consecutive cycle unresolved, but the trend is deceleration of the adverse move, not acceleration.
- The system's own scanner separately evaluated a TUT short and again capped it to C tier on `high_upper_wick_short_squeeze_risk` (score 48.1) — neither direction is clean; do not add to either side.
- Actionable now or after confirmation? Neither — continue to hold-and-monitor only; escalate for a direct price-vs-invalidation check outside this run's permission scope (see §14 TODO, carried forward but downgraded).

### 7.3 RE/USDT (swing long, B, score 71.0, `waiting_for_entry`) — WATCH, cleanest pre-entry long
- Entry zone 0.5682-0.5745, invalidation 0.5606, expires 2026-09-01. Created 2026-08-31... (actually 2026-08-28T21:29 per prior record) — still waiting, hasn't chased.
- Chasing? No — still pre-entry, the only such row left in the crypto book after TRUMP/USDT moved away.
- Aligned with market mood? Same caveat as any new long in a mixed regime — demand volume confirmation on fill, don't treat the zone touch alone as entry.
- Catalyst confirmation/contradiction? None found; technical-only setup, consistent with the rest of the book.

### 7.4 TRUMP/USDT (swing long, B, score 77.7, `entry_moved_away`) — NO LONGER ACTIONABLE
- Zone 2.7908-2.8422, invalidation 2.72803 never filled; price left the zone without triggering. Was the prior review's best-long-watch; now closed out as a missed opportunity, not a loss (0R / no entry).
- No action needed; superseded by RE/USDT as the desk's best pre-entry long idea.

### 7.5 SOL/USDT (swing long, B, score 71.9, `triggered`) — WATCH, catalyst present but momentum still contradicts
- Entry 96.017-96.649, stop/invalidation 95.244, TP1 98.757. Unchanged from overnight review.
- Catalyst: DeFi Development's "State of Solana" real-time intelligence platform (The Block) — still tagged "weak_vs_market" on momentum. No material change since 04:40.

## 8. Best Candidates Ranked

1. **Long-watch: RE/USDT** — trigger: filled entry in 0.5682-0.5745 with volume confirmation; invalidate below 0.5606.
2. **Catalyst-watch: SOL/USDT** — trigger: RS vs BTC/market turning positive to confirm the DeFi Development catalyst as tradeable strength (unchanged from overnight).
3. **Short-watch: TUT/USDT** — trigger: clean break of the recent low on rising volume with no upper-wick rejection (system currently caps this short to C on squeeze risk).
4. **Monitor, not new entry: ONG/USDT** — open long now favorable but overextended/squeeze-driven; do not chase a new long, watch funding for exhaustion signal.
5. **Needs-review (not new entry): TUT/USDT open long** — see §14 TODO; hold status improving but still bias-contradicted.
6. **No longer relevant: TRUMP/USDT** — entry_moved_away, dropped from active watch list.

## 9. Avoid / No Trade

- **New ONG/USDT longs** — chasing an overextended (>2 ATR from EMA20), funding-negative squeeze; the desk's own rejection logic already disqualifies a fresh entry here. This does not apply to the existing open position, which is currently favorable.
- **New crypto shorts in general** — the desk has zero shorts armed and the one short setup evaluated this cycle (TUT) is squeeze-capped; avoid manually forcing a short until the scanner itself clears one.
- **New stocks positions** — market closed all weekend (Saturday); nothing to avoid or take today, purely Monday-planning context (VRT legal-risk, CRCL short_bounce_guard demotion, LLY positive-catalyst carry forward).
- This verdict applies to *this decision window only* — it is not a command to close any position, nor to pause the scanner, tracking, or scheduler.

## 10. Main Risks

- **TUT unresolved contradiction, now 6th+ cycle / ~19h**: adverse move is decelerating (good sign) but still bias-contradicted; if the invalidation was in fact breached earlier and not recorded, the position carries unrecognized risk in downstream paper/monitor accounting.
- **ONG squeeze-exhaustion risk**: the open long is now favorable but the setup (negative funding despite +15.9% price, "overextended" tag) is exactly the profile of a squeeze that can reverse sharply once short-covering exhausts — treat current gains as fragile, not confirmed trend.
- **Regime drift without book re-screen**: 51 open long signals still scored under a more bullish read than the current "transition (mixed)" regime (unchanged since 22:37 EEST Aug 28) — carried forward from the overnight review, no new evidence this cycle to resolve it either way.
- **Macro risk-off headwind persists**, though eased from 100/100 to ~75/100 — still a standing tailwind for downside volatility (Iran/Israel tensions, US sanctions expansion).
- **Catalyst mapping still weak (63.6% unmapped)** — improving but still reduces confidence that "no catalyst" tags are true absence of news vs. an unmapped headline.
- **New: stale-triggered stocks C-tier rows (15 found)** — pipeline hygiene gap, no live-exposure impact but degrades trust in `active-signals` output for historical stocks review (see §14 TODO).

## 11. Action Plan — next 4 hours

- Watch RE/USDT for a confirmed fill in its entry zone with volume; treat as the cleanest new-long idea if it triggers cleanly.
- Watch ONG/USDT's funding/OI for a reversal signal (funding turning positive, OI dropping sharply) as an early exhaustion warning on the existing open long — do not add new size regardless.
- Monitor for a fresher crypto swing report to confirm whether TUT/USDT's bias tag flips the same way ONG's did.
- No new stocks action until Monday pre-market; VRT (legal risk), CRCL (short_bounce_guard demotion), LLY (positive FDA/Mounjaro catalyst) carry forward as watch names for the pre-US-open review.
- Continue scanning/tracking as normal through the rest of the weekend — no scanner or scheduler changes recommended.

## 12. Final Verdict per Mode

- **Crypto scalp**: caution / selective only — regime mixed, no new A/B this cycle; macro risk-off headwind easing but not cleared.
- **Crypto intraday**: caution / wait-for-trigger — same mixed-regime caveat, no new A/B this cycle.
- **Crypto swing**: caution / hold-existing-only — 51 open_actionable + 2 waiting_for_entry rows; ONG's contradiction has resolved favorably, TUT's is improving but still open; RE/USDT is the cleanest pre-entry idea.
- **Stocks (all modes)**: closed all weekend — planning-only until Monday pre-market; VRT/CRCL/LLY carry forward as watch names.

## 13. Sources

No external sources were cited this run (internal-only cycle — see §2). Internal sources used, with paths and timestamps, are listed in full in §2 above.

## 14. Fix Requests / TODO

### TODO-tut-invalidation-unresolved (carryover, improving — 6th+ cycle)
- **issue:** Open swing long `sig_c7ce9835f38c40a8` (TUT/USDT, invalidation 0.05058) still shows `status=triggered` despite the desk's own bias tag reading "short" for 6th+ consecutive cycle. The adverse move is decelerating (-20.47% → -14.41% → -12.56% → -11.97% across four reads since 04:40) rather than worsening, but the contradiction itself remains unresolved.
- **evidence:** `proposed_signals` direct query (status=triggered, invalidation unchanged from prior reviews); scalp/intraday/swing reports' bias-tag lines for TUT/USDT across 2026-08-29 04:16, 02:33, 08:07, 08:20 EEST reads.
- **suggested manual fix:** a human-driven session should query current TUT/USDT price directly against invalidation 0.05058, confirm whether the stop was ever actually hit and simply not recorded as a `signal_outcome`, and investigate why the monitor hasn't closed/recorded it if so. Lower urgency than the 04:40 review given the improving trend, but still open.
- **priority:** medium (downgraded from high — trend is improving, not worsening)
- **first observed:** 2026-08-28 18:39 EEST — still open at 2026-08-29 11:46 EEST.

### TODO-stocks-stale-triggered-rows (new)
- **issue:** Direct SQL audit of `proposed_signals` found **15 stocks rows with `status='triggered'`** whose `expires_at` is weeks in the past (oldest created 2026-07-20T14:16-17:31 UTC, one batch created 2026-08-03/07 expiring 2026-08-04/08) that have never transitioned to a resolved status (`stopped`/`tp*_hit`/`expired`). All are C-tier (watchlist/research quality, not Telegram-actionable), so there is no live-exposure impact, but the `active-signals` / raw `proposed_signals` view is carrying stale rows that could confuse a reviewer scanning for genuinely open positions.
- **evidence:** `SELECT signal_id, symbol, tier, mode, direction, status, created_at, expires_at FROM proposed_signals WHERE asset_class='stocks' AND status='triggered'` — 15 rows returned, e.g. `sig_09d07ae42ae362db` (NOC, created 2026-08-03, expired 2026-08-04, still `triggered` as of 2026-08-29).
- **suggested manual fix:** a human-driven session should check whether the stocks C-tier resolution/monitor job is failing to sweep `triggered` rows past `expires_at` into a closed state, and backfill/close the 15 identified rows if confirmed stale.
- **priority:** low (no live-exposure impact, C-tier/research-only, but a data-hygiene gap worth fixing before it grows)
- **first observed:** 2026-08-29 11:46 EEST.

### TODO-catalyst-mapping-weak (carryover, improving)
- **issue:** `data/catalysts/2026-08-29/catalyst_events.jsonl` unmapped rate is 63.6% (864/1,359) — still above the 50% "weak mapping" threshold but improving vs ~69-71% seen in the last several days.
- **evidence:** direct count of `catalyst_events.jsonl` (495 mapped / 864 unmapped); comparable figures in prior reviews (69.0% Aug 29 04:40, 70.9% Aug 28).
- **suggested manual fix:** unchanged from prior reviews — audit the symbol-resolver in the catalyst layer; consider whether stablecoin-flow / sector-wide headlines (like the top-4 unmapped examples in §5) should be a distinct "no-symbol-expected" category rather than counted against the mapping rate at all.
- **priority:** medium
- **first observed:** 2026-08-28 18:39 EEST (recurring, improving as of 2026-08-29 11:46 EEST).
