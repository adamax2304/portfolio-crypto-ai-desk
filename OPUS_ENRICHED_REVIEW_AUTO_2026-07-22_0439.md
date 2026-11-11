# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:39 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review (04:30 EEST)** — overnight crypto action and Asia-session regime check; stocks market is closed, carried forward as planning/watchlist context only. Advisory only — no auto-trade, no scoring/threshold changes.

Reports fresh: crypto intraday (00:31 EEST, ~4min), crypto swing (01:16 EEST, ~4min gen-time / fresh), crypto scalp (00:24 EEST, ~15min), stocks intraday (00:53 EEST, ~market-closed snapshot). Scheduler and last cycle (`cycle_03_03-16`) both fresh (~17min old). No A-tier setups anywhere in crypto or stocks this cycle — every actionable idea is B-tier (crypto) or C-tier (stocks, non-actionable while closed).

Crypto stayed technically risk-on (BTC/ETH uptrend, altcoin breadth 74.4%>EMA20) while the macro overlay held at risk-off extremes (95.9–100/100, driven by the ongoing US–Iran/Strait-of-Hormuz escalation). **External verification confirms the conflict is real and ongoing (strikes through mid-July), but crypto's reaction has visibly faded — initial shock knocked BTC from ~$65.5K to below $64K, but subsequent strikes have produced little further follow-through** (see §13). This technical/macro divergence persists unresolved into the Asia handoff.

Best long / catalyst-backed: **ONDO/USDT** — RWA-basket, RS +10.4% vs BTC, price+OI both rising (fresh positioning, not exhausted), and a same-day AMBCrypto catalyst ("entity buys $61M ONDO") that the report's own live scan window missed (known lookback-limitation, [[project_crypto_ai_desk_catalyst_linkage]]) but that direct `news_items` query confirms. Best short-watch (not a trigger): **RIF/USDT** — squeeze-prone (OI +63.7% while price fell −34% to −40%), and crypto shorts are 0-for-6 this week (PF 0.125) — avoid chasing. Avoid: **EPIC/USDT** as a fresh long above its pullback zone (vertical +20–22% 24h move, thin volume support, known no-catalyst-chop failure mode) and any of the exploit_hack-flagged symbols (ADA, BNB, BONK, ETH, SOL) for new entries.

Catalyst mapping is **weak this run (81.6% unmapped, 92/500 mapped)** — use the catalyst layer as context, not as a final decision driver (§5). Untracked-alert detector shows **0 new fires today** (early in the day; recurrence has historically resumed later — do not read this as resolved). The NVDA stocks signal status/expiry mismatch flagged in prior reviews is **still unresolved**, gap now ~13.5h (§14).

## 2. Data Used

- Reports: crypto intraday (`2026-07-22_00-31_intraday_report.md`, fresh), crypto swing (`2026-07-22_01-16_swing_report.md`, fresh), crypto scalp (`2026-07-22_00-24_scalp_report.md`, fresh)
- Stocks intraday: `2026-07-22_00-53_stocks_intraday_report.md` — market closed, chop regime, VIX 17.05, planning-only
- Stocks swing/invest: last dated 2026-07-02 — **excluded, deprecated framework** ([[project_crypto_ai_desk_stocks_position_framework]])
- Catalyst layer: `data/catalysts/2026-07-22/catalyst_cycle_00-37.md`, `catalyst_events.jsonl` (500 events), `narrative_baskets.jsonl` (5 baskets)
- LLM packets: `llm_analysis_packet.md` (04:17 EEST), `llm_stocks_packet.md` (03:55 EEST)
- CLI: `active-signals` (crypto ×33, stocks ×50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-07-22` (0 hits)
- Direct SQL read of `news_items` (via `db/crypto_ai_desk.sqlite`, read-only) for ONDO/EPIC/RIF — confirmed ONDO catalyst (AMBCrypto, 2026-07-21T15:00 UTC), zero symbol-specific hits for EPIC/RIF in the last 24h
- Direct computation of catalyst mapping ratio from `catalyst_events.jsonl` (500 total, 92 mapped, 408 unmapped = 81.6%)
- Heartbeat: `data/autostart/heartbeat_state.json` — last OK 2026-07-22T01:17:36Z (~22min ago), last warn 2026-07-20T12:57Z (>24h stale, not relevant)
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-21_2323.md` (post-close slot)
- **External web research invoked this run**: 1× WebSearch + 1× WebFetch to verify the macro Iran/Hormuz risk-off overlay driving the market-mood label (§13) — internal news_items records for the actual trade candidates (ONDO/EPIC/RIF) were fresh, internally consistent, and already source-attributed, satisfying the internal-first bar for those without needing a fresh search per candidate.

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-07-21_default_schedule/scheduler.log`: mtime 04:22 EEST (~17min ago) — **fresh**.
- Latest cycle summary: `cycle_03_03-16_summary.md` (finished 04:22:07 EEST, ~17min old) — **fresh**, steps ok=77 failed=2 (both counterfactual/shadow timeout steps — `crypto quality overlay report` and `crypto swing versioned shadow sweep`, exit=-1 @300s; read-model/advisory only, not live-signal-affecting).
- Heartbeat: OK 2026-07-22T01:17:36Z (~22min ago); no active warn.
- Crypto intraday/swing/scalp reports: all fresh (4–15min).
- Stocks intraday: fresh snapshot, but market closed — demoted to planning-only per the report's own banner.
- Stocks swing/invest: stale (20 days), excluded — deprecated framework.
- Monitors: crypto pending monitor, MEXC canary monitor, derivatives monitor, stocks monitor all confirmed running (background pids) in cycle_03.
- Minor: social-attention Reddit sources (CryptoCurrency/Bitcoin/Ethereum) returning 403 Blocked repeatedly this cycle — persistent, low-impact (reports already show "no symbol-level hits from configured free sources"), not new.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-22 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest fresh data (deprecated, excluded)", "TradingView/chart MCP not loaded", "liquidation heatmaps / order book depth / on-chain flows (never automated)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 04:22 EEST (~17min)", "cycle_03_03-16_summary.md ok=77 failed=2 (both shadow/counterfactual timeouts, non-live)", "crypto intraday/swing/scalp reports 4-15min fresh", "stocks intraday fresh but market closed (planning-only)", "heartbeat OK 01:17:36Z (~22min ago)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "risk_on", "shorts_preferred", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend, 74.4% breadth>EMA20, style=selective longs prefer pullbacks on RS", "macro risk 95.9-100/100 risk-off overlay (Iran/Hormuz), external search confirms real but crypto reaction fading since initial shock", "stocks: chop, VIX 17.05, 0/4 indices trending, market closed"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl: 500 total, 92 mapped (18.4%), 408 unmapped (81.6%) -> mapping weak, worse than yesterday's 23.0%", "ONDO: RWA basket fresh <6h, AMBCrypto '$61M entity buy' headline confirmed via direct news_items query (15:00 UTC Jul21, ~13.5h old, report's own live scan missed it - known lookback limitation)", "momentum_breakout basket (EPIC/SNDKB/SKHYB) fresh <1h, no catalyst, pure momentum", "ADA/BNB/BONK/ETH/SOL still carrying exploit_hack operator-review flags"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["squeeze_risk", "oi_supports", "oi_contradicts", "funding_extreme"],
      "data_missing": ["liquidation heatmap", "order book depth"],
      "suggested_effect": "advisory_only",
      "facts_used": ["RIF/USDT: price down -34% to -40%, OI 24h +63.67%, long/short 0.361 (heavily short-skewed) -> fresh shorts pressing, squeeze risk if price reclaims", "ONDO/USDT: price up + OI up +18.31%, long/short 1.705 -> fresh positioning confirms trend, not exhausted", "EPIC/USDT: funding neutral, OI data thin/fallback via MEXC only"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest", "entry_fresh", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["EPIC/USDT: 24h +20.98-22.52%, 7d +41%, price 0.542 vs swing entry zone 0.5296-0.5382 (already ~0.2 ATR above zone) -> late/chase risk", "ONDO/USDT: price 0.4042 essentially at swing entry zone 0.4003-0.4030 -> near-clean pullback entry, not extended", "FIL/USDT: 4.3x volume, tagged overextended, >2 ATR from EMA20 in scalp report -> avoid chasing", "RIF/USDT: >2 ATR extended short, capped to C for squeeze risk"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals (33): waiting_for_entry=7, triggered=5, tp1_hit=11, tp2_hit=10 (all open-actionable, in-progress toward further targets/stop)", "stocks active-signals (50): waiting_for_entry=5, triggered=20, tp1_hit=13, tp2_hit=12", "0 stopped/expired/closed visible in either active table this snapshot", "NVDA sig_e0fceb60a6327886 still status=triggered with expires_at 13.5h in the past -> needs_review"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk", "correlation_cluster"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["operator-review warnings live on ADA, BNB, BONK, ETH, SOL (all exploit_hack) -> avoid new entries in these names", "macro geopolitical risk 95.9-100/100 unresolved, correlated crypto-wide risk if it re-escalates", "TSLA/GOOGL earnings today (2026-07-22, US session) -> stocks do_not_chase_warning already active, relevant for later slots"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp mode: PF 0.658, avgR -0.117, totalR -4.10 (n=41) -> losing bucket, kill-switch already off (mode disabled) per scalp report", "crypto direction=short: PF 0.125, 0 wins/6 losses (n=8, anecdotal but consistent) -> reinforces caution on RIF short", "crypto swing mode: PF 2.70, avgR 0.44 (n=54, stronger) -> best-performing crypto mode, supports ONDO/EPIC swing framing", "stocks tier=C: PF 0.875, winrate 13% triggered (n=189, reliable) -> stocks C-tier remains weak, consistent with 'no A-tier this cycle'"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.7,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "catalyst_backed",
    "best_long_candidate":     { "symbol": "ONDO/USDT", "trigger": "already near swing entry zone 0.4003-0.4030 (current 0.4042); pullback close into zone with volume confirms", "reason": "RWA basket, RS+10.4% vs BTC, price+OI both rising (not exhausted), confirmed same-day whale-buy catalyst" },
    "best_short_candidate":    { "symbol": "RIF/USDT", "trigger": "wait for failed retest/rejection at resistance with OI stabilizing or rolling over; do not chase the current -34% to -40% move", "reason": "squeeze-prone (OI +63.7% into the drop, heavily short-skewed L/S), and crypto shorts are 0-for-6 this week" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "same as best-long — AMBCrypto $61M entity-buy catalyst confirmed via direct news_items read, RWA basket fresh <6h", "reason": "only symbol this cycle with a verified same-day catalyst plus RS leadership plus non-exhausted derivatives" },
    "avoid_candidate":         { "symbol": "EPIC/USDT (fresh long above entry zone)", "reason": "vertical +20-22% 24h move, volume support thin, no catalyst, playbook's own known-failure-mode note: no-catalyst intraday chop is net-negative (14d WR 23%/PF 0.70/-3R)" },
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
| market_regime | caution | 0.65 | mixed, risk_on, shorts_preferred, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, narrative_supported, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.60 | squeeze_risk, oi_supports, oi_contradicts, funding_extreme | advisory_only |
| technical_entry | caution | 0.65 | entry_late, chase_risk, clean_retest, entry_fresh, overextended | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk, correlation_cluster | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.65 | — | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-21_2323.md` (post-close, 23:23 EEST).

- **New**: ONDO/USDT promoted to this review's top catalyst-backed pick (was mentioned in passing at 23:23 as "now entered/triggered, unresolved" — now has a directly-confirmed catalyst via `news_items` and is near a clean swing entry).
- **Removed / no longer top-of-mind**: MKR/USDT (Movement Labs Chapter-11 legal-risk avoid at 23:23) — no longer appearing in this cycle's top catalyst/risk list; not re-verified this run, treat as stale unless it resurfaces.
- **Thesis unchanged**: macro risk-off (Iran/Hormuz) vs crypto technical risk-on divergence — same theme, now externally verified as a fading-reaction pattern rather than assumed.
- **Thesis changed**: crypto shorts framing — 23:23 review cited DEXE as best short-watch (exhausted breakdown); this run's data (0/6 losses this week, RIF's active squeeze setup) makes the case for shorts even weaker — no clean short anywhere in crypto right now.
- **Confirmed still unresolved**: NVDA stocks signal status/expiry mismatch (TODO carried forward, gap widened from ~8h to ~13.5h). Catalyst mapping weak (worsened from 23.0% mapped to 18.4% mapped).
- **Untracked-alert bug** ([[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]]): 0 new fires so far today (vs 9 total on 2026-07-21) — too early in the day to call this resolved; historically these accumulate through the session.

## 5. Catalyst Coverage

- Total catalyst events today: **500**
- Mapped (non-null symbol): **92** (18.4%)
- Unmapped (null symbol): **408** (81.6%)
- Narrative baskets: **5** (delisting_thin_liquidity, perps_dex_narrative, ai_narrative, binance_ecosystem_teaser, momentum_breakout)

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Top 3 unmapped headlines:
1. "Adjustment to Maximum Leverage for ONEUSDT Futures" (exchange-ops notice, likely genuinely unmappable to a directional thesis)
2. "Delisting of SOLANGELESUSDT Perpetual Futures Pair" (exchange-ops notice)
3. "Hedge funds cut US tech exposure at the fastest pace in a decade as AI infrastructure volatility rises" (macro wire copy, not a single-symbol catalyst)

This continues a multi-day pattern already tracked as TODO-catalyst-mapping-persistent-weak (§14) — mapping rate actually worsened vs yesterday's 23.0%.

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed** — technically risk-on (BTC/ETH uptrend, 74.4% breadth>EMA20) but macro risk-off overlay at 95.9-100/100 (Iran/Strait-of-Hormuz escalation, externally verified as ongoing but with fading market reaction — see §13).
- Stocks mood: **closed** (overnight) — last live regime was chop, VIX 17.05, 0/4 indices trending; TSLA and GOOGL report earnings today (2026-07-22, US session) — planning-only until RTH.
- Dominant narrative: **RWA** (ONDO, catalyst-confirmed whale buy) and a **momentum_breakout cluster** (EPIC/SNDKB/SKHYB, no catalyst backing) running in parallel; secondary AI-sector rotation (NEAR/RENDER/TAO/FET) and a perps-DEX narrative (HYPE/DYDX/GMX/ASTER) both still forming, no active signals riding either yet.
- Preferred side now: **catalyst-backed longs first** (ONDO), RS-leader longs only on confirmed pullback (not chase) second; **avoid fresh shorts** — crypto shorts are 0-for-6 this week and the one live short setup (RIF) is squeeze-prone.
- Best long candidate: **ONDO/USDT** (near entry, catalyst-confirmed).
- Best short candidate: **none clean** — RIF/USDT is the best short-watch but only after a failed retest with OI stabilizing; do not trigger on the current move.
- Best catalyst-backed candidate: **ONDO/USDT**.
- What to avoid: chasing EPIC/USDT above its entry zone; chasing RIF/USDT short into the squeeze; any fresh long/short on ADA, BNB, BONK, ETH, SOL while their exploit_hack operator-review flags are live.
- What would change the view: a confirmed Iran/Hormuz de-escalation headline (would remove the macro overlay and could unlock more aggressive long sizing), BTC breaking uptrend structure (would flip the whole regime), or RIF's OI beginning to unwind while price fails to reclaim resistance (would confirm the short rather than just flag it).

## 7. Candidate Deep Dives

### 7.1 ONDO/USDT — LONG (swing, B-tier, score 67.5; also 2 intraday legs already triggered)

- Has price already reacted to the catalyst? Partially — the AMBCrypto "$61M entity buy" headline is ~13.5h old (2026-07-21T15:00 UTC) and ONDO is +12.34% 24h / +27.07% 7d, so some of the move has already happened, but price (0.4042) is essentially sitting right at the swing entry zone (0.4003-0.4030), not chasing.
- Is the setup chasing? No — current price is within ~0.2 ATR of the entry zone, not extended.
- Retest/pullback structure? Yes — this is a live pullback-into-zone setup per the swing playbook (`crypto_swing_narrative_rs_momentum`, 14d WR 72% / PF 5.80 in backtest).
- Overextended (>2 ATR from EMA20)? No.
- Would entry now be late? No — this is close to the textbook entry.
- What level makes it actionable? A close into or below 0.4030 (top of stated entry zone) with volume, invalidation at 0.397069 (swing) / 0.390214-0.397206 (intraday legs already filled).
- Aligned with market mood? Yes — catalyst-backed long is the preferred side this cycle.
- Long, short, or wait-for-trigger? Long, near-actionable (already has 2 active intraday legs filled; swing leg is waiting_for_entry).
- Actionable now or after confirmation? Effectively already actionable at current levels for the swing leg (price is inside/at the edge of the zone).
- What would invalidate? 1h close below 0.397 (swing invalidation), or the RWA narrative basket flipping from "mixed" to outright bearish.
- Chase risk? Low.
- Catalyst confirmation or contradiction? **Confirmed** via direct `news_items` query (AMBCrypto, single_source, 2026-07-21T15:00 UTC) — note the swing/intraday reports themselves say "no fresh verified catalyst detected" for ONDO because their live scan window (~5h lookback) missed this ~13.5h-old item; this is a known, already-tracked lookback limitation ([[project_crypto_ai_desk_catalyst_linkage]]), not a new issue.
- Derivatives: price up + OI up +18.31%, long/short 1.705 — fresh positioning confirms the trend, not an exhausted crowd.

### 7.2 EPIC/USDT — LONG (swing + intraday, B-tier, score 65.6-75.7) — chase-risk, watch only

- Has price already reacted to the catalyst? There is no catalyst — this is pure momentum (top gainer in the `momentum_breakout` basket, no news_items hits in the last 24h).
- Is the setup chasing? **Yes at current price.** 24h +20.98% to +22.52%, 7d +41%, current price 0.5420 vs swing entry zone 0.5296-0.5382 — already above the planned pullback zone.
- Retest/pullback structure? Not yet — would need to fall back into the 0.5296-0.5382 zone.
- Overextended? Borderline — not flagged >2 ATR in the swing report, but volume ratio is thin (0.08-1.21x depending on report) despite the vertical move, meaning the rally isn't backed by proportional volume.
- Would entry now be late? Yes.
- What level makes it actionable? A genuine pullback close into 0.5296-0.5382 with volume, not a market buy at current price.
- Aligned with market mood? Only partially — momentum without catalyst confirmation is the weaker of this cycle's two long setups.
- Long, short, or wait-for-trigger? Wait-for-trigger (pullback).
- Actionable now? No — chase risk is real.
- What would invalidate? 1h close below 0.5191 (swing invalidation) or the momentum_breakout basket rolling over.
- Chase risk? **High** — the playbook's own known-failure-mode note flags this explicitly: "no-catalyst intraday in chop is net-negative — needs RS-leader or breakout confirmation" (14d WR 23% / PF 0.70 / −3R for the no-catalyst cohort).
- Catalyst confirmation or contradiction? No catalyst found (confirmed via direct `news_items` query, 0 hits in 24h).

### 7.3 RIF/USDT — SHORT-WATCH (C-tier, rejected/capped, score 47.8-86 depending on report) — squeeze risk, avoid chasing

- Has price already reacted? Yes, heavily — 24h -34.44% to -39.97%, 7d correspondingly weak.
- Is the setup chasing? Yes if entered now — the move is already extreme.
- Retest/pullback structure? None yet; would need a failed bounce/rejection.
- Overextended? Yes by any reasonable measure for a fresh short entry.
- Would entry now be late? Yes.
- What level makes it actionable? A clean failed retest of resistance with OI stabilizing or starting to roll over (currently OI is still building into the drop, the opposite of what a clean short wants to see).
- Aligned with market mood? No — shorts are out of favor this week (0/6 losses, PF 0.125) and this specific short is doubly risky.
- Long, short, or wait-for-trigger? Short-watch only, wait-for-trigger.
- Actionable now? No.
- What would invalidate the idea entirely? A reclaim of the pre-drop range, which would trigger the squeeze the derivatives data already warns about.
- Chase risk? High (on the short side).
- Catalyst confirmation or contradiction? No catalyst found for RIF (0 news_items hits in 24h); this is pure derivatives-driven price action. Both scalp and swing reports independently flag "short squeeze risk → capped to C" and "Global long/short ratio is heavily short skewed" / "fresh shorts pressing, possible squeeze if price reclaims."

## 8. Best Candidates Ranked

1. **ONDO/USDT — LONG** (best long-watch and best catalyst-watch): near entry zone 0.4003-0.4030, catalyst-confirmed, non-exhausted derivatives.
2. **EPIC/USDT — LONG, wait-for-pullback only**: trigger = 1h close/hold inside 0.5296-0.5382 with volume; do not chase current price.
3. **RIF/USDT — SHORT-WATCH only**: trigger = failed retest of resistance + OI stabilizing/rolling over; do not chase the current move (squeeze risk).

No clean fourth/fifth candidate this cycle — every other B-tier active signal is either already deep in-position (tp1/tp2_hit, being managed, not a fresh decision) or C-tier/rejected without a clean setup.

## 9. Avoid / No Trade (this decision window only)

- **EPIC/USDT at current price** — chase risk, no catalyst, known losing cohort in backtest.
- **RIF/USDT short at current price** — squeeze-prone, crowded, crypto shorts 0-for-6 this week.
- **ADA, BNB, BONK, ETH, SOL** — all carrying live exploit_hack operator-review warnings; avoid new entries until the warnings clear.
- **Crypto scalp mode generally** — PF 0.658 / totalR -4.10 this week (n=41); mode is already kill-switched off in production, consistent with this data.
- This is a decision-window verdict only — the scanner, tracking, and monitors continue running normally; nothing here is a system-stop instruction.

## 10. Main Risks

- Macro/geopolitical: Iran/Strait-of-Hormuz conflict remains live and unresolved (95.9-100/100 risk score); externally verified as real, with a fading-but-not-zero market impact — a fresh escalation headline could still hit BTC/ETH sharply given the earlier ~2% drop on the initial strikes.
- Catalyst-layer mapping is weak (81.6% unmapped) and getting worse — treat any catalyst-driven thesis as context, not confirmation, unless independently verified (as done for ONDO this run).
- Crypto shorts are a demonstrably losing bucket this week (0/6, PF 0.125) — any short bias should be treated skeptically regardless of how compelling the setup looks.
- Stocks: TSLA and GOOGL both report earnings today (2026-07-22) during the US session — expect elevated single-name and index-ETF volatility once the cash market opens; existing do-not-chase warnings are already live in the system for both.
- NVDA stocks signal (`sig_e0fceb60a6327886`) lifecycle gap persists — a genuine monitor/sweep issue, not just a display artifact at this point (§14).

## 11. Action Plan — next 4 hours

- Watch ONDO/USDT for the swing entry to fill (price is essentially at the zone already); no action needed beyond monitoring — the system will fill/track it.
- Do not manually chase EPIC/USDT; wait for the pullback trigger.
- Do not initiate a RIF/USDT short; wait for a failed-retest confirmation with OI evidence.
- No stocks action — market closed; re-evaluate at the 11:30 EEST Europe/pre-US context review, and again at 16:20 EEST pre-US-open review ahead of TSLA/GOOGL earnings reactions.
- Monitor for any Iran/Hormuz de-escalation or fresh-escalation headline — either would meaningfully change the macro overlay driving this review's "mixed" mood label.

## 12. Final Verdict per Mode

- **Crypto scalp**: no trade (mode disabled in production; backtest confirms PF<1 this week).
- **Crypto intraday**: watch-only; no fresh A/B trigger this cycle; manage existing triggered/tp-hit positions per their own stops/targets.
- **Crypto swing**: **watch ONDO/USDT** (near-actionable, catalyst-confirmed); EPIC/USDT wait-for-pullback only.
- **Crypto short bias (any mode)**: avoid; RIF/USDT is short-watch only pending a failed-retest confirmation.
- **Stocks (all modes)**: closed, planning/watchlist only; earnings risk (TSLA, GOOGL) flagged for the US session ahead.

## 13. Sources

- [US-Iran military escalation sends Bitcoin below $64K as crypto markets feel the heat](https://cryptobriefing.com/us-iran-strikes-bitcoin-crypto-market-drop/) — CryptoBriefing, confirms initial strike (2026-07-07) and BTC drop from ~$65.5K to below $64K, ~$350M liquidations. Fetched and verified this run.
- [Iran vows to keep Strait of Hormuz closed after US strikes, and crypto markets barely flinch](https://cryptobriefing.com/iran-strait-hormuz-closed-crypto-markets/) — CryptoBriefing, supports the "fading market reaction to subsequent strikes" framing used in §1 and §6.
- [US strikes on Iran's Qeshm Island rattle oil markets and test crypto's geopolitical immunity](https://cryptobriefing.com/us-strikes-qeshm-island-crypto-oil-markets/) — CryptoBriefing.
- Internal: `data/reports/swing/2026-07-22_01-16_swing_report.md`, `data/reports/intraday/2026-07-22_00-31_intraday_report.md`, `data/reports/scalp/2026-07-22_00-24_scalp_report.md`, `data/reports/stocks/intraday/2026-07-22_00-53_stocks_intraday_report.md` (2026-07-22).
- Internal: `data/catalysts/2026-07-22/catalyst_cycle_00-37.md`, `catalyst_events.jsonl`, `narrative_baskets.jsonl`.
- Internal: `news_items` table (AMBCrypto, "Ondo Finance up 14% as entity buys $61M ONDO", 2026-07-21T15:00:13 UTC) — read via direct SQL query, `db/crypto_ai_desk.sqlite`.

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-persistent-weak (carried forward, worsening)
- **issue:** Catalyst mapping has been below 50% for multiple consecutive review cycles across multiple days; today's rate (18.4% mapped, 81.6% unmapped) is worse than yesterday's 23.0% mapped.
- **evidence:** direct computation from `data/catalysts/2026-07-22/catalyst_events.jsonl` — 92/500 mapped.
- **suggested manual fix:** revisit the symbol resolver in the catalyst layer, as previously flagged; also worth checking whether the resolver's match rate is trending down over time (today vs yesterday) or is just daily noise — if it's a real downward trend it deserves higher priority than "low."
- **priority:** low-to-medium (trending worse; escalate if the downward trend continues 2+ more days)
- **first observed:** recurring pattern, reconfirmed 2026-07-22 04:39 EEST (previously reconfirmed 2026-07-21 23:23 EEST)

### TODO-nvda-signal-status-expiry-mismatch (carried forward, gap widening)
- **issue:** Tracked stocks signal `sig_e0fceb60a6327886` (NVDA, C-tier, short, score 87.8) still shows `status=triggered` with `expires_at=2026-07-21T15:03:27` UTC — now ~13.5h in the past relative to this 04:39 EEST review (was ~8h at the 23:23 EEST review, ~3.5h at 21:39 EEST). No resolution to a closed/stopped/expired state across four consecutive checkpoints now.
- **evidence:** `python -m src.cli active-signals --asset-class stocks` output, this run (row for NVDA short, `sig_e0fceb60a6327886`).
- **suggested manual fix:** as previously flagged — check whether the stocks pending/outcome monitor is correctly resolving C-tier intraday signals once their `expires_at` passes. Four consecutive review cycles without resolution strongly suggests a genuine lifecycle-sweep gap rather than a display artifact.
- **priority:** high (escalating — was "medium, escalate if unresolved at tomorrow's pre-open review"; tomorrow's pre-open review is today's 16:20 EEST slot, still open)
- **first observed:** 2026-07-21 21:39 EEST (reconfirmed 23:23 EEST and again 2026-07-22 04:39 EEST)

### TODO-shadow-counterfactual-step-timeouts
- **issue:** Heavy shadow/counterfactual scheduler steps have timed out (exit=-1 @ 300s) in each of the last 3 cycles, but a *different* step each time: `refresh obsidian dashboard` (cycle_02), `crypto quality overlay report` + `crypto swing versioned shadow sweep` (cycle_03, both same cycle). These are read-model/advisory-only steps, not live-signal-affecting, but the pattern (different heavy step failing each cycle) suggests resource contention rather than a single broken step.
- **evidence:** `data/scheduled_runs/2026-07-21_default_schedule/cycle_02_00-29_summary.md` step 66, `cycle_03_03-16_summary.md` steps 59-60.
- **suggested manual fix:** check whether these steps are competing for the same resource (DB lock, CPU, network) during the cycle window, and whether raising the 300s timeout or staggering these specific steps would help; low urgency since none of them affect live signals or the Telegram-actionable path.
- **priority:** low
- **first observed:** 2026-07-22 04:39 EEST (this run; pattern visible across the last 2 cycles inspected)
