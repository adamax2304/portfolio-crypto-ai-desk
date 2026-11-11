# Opus Enriched Review — US open reaction review — Auto Cycle 18:40 EEST

## 1. Executive Summary

**Slot: US open reaction review (nominal 18:30 EEST), completed ~18:40 EEST on Saturday 2026-07-18. Advisory only — no auto-trade, no code/scoring/routing changes.** Pipeline healthy, not deferred: `scheduler.log` / latest `cycle_06_17-03_summary.md` both mtime 17:34 EEST (~1h06m old at review start), well under the 3h defer threshold.

**Critical framing: today is Saturday — there is no US cash open.** "US open reaction" is nominal only; equities remain closed through the weekend. Every stocks reference below is Monday-planning context, not an actionable decision this window. Crypto is the sole live actionable class.

**Headline finding — genuinely new since the last review** (`OPUS_ENRICHED_REVIEW_AUTO_2026-07-18_1630.md`, 16:30 EEST): two things changed. (1) **TRUMP/USDT stopped out** at 13:37:41 UTC (16:37 EEST) — the prior review's one live position hit its stop (1.6402) for a clean **-1R loss**, resolving the "no-catalyst cohort" question the prior review flagged as the main risk. (2) A **fresh B-tier crypto intraday long triggered on ALLO/USDT** (`sig_10088a4c71cae845`, created 15:21:04 UTC / 18:21 EEST, `waiting_for_entry`) — and it is **structurally the same setup type that just lost**: same playbook (`crypto_intraday_catalyst_or_momentum`, no-catalyst variant), same weekend-mode retest-after-impulse gating, `news_supported=0`, similar score (65.9 vs TRUMP's 65.1). See §7.1 for the full caution — this is the primary decision point this cycle.

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-18_14-11_scalp_report.md` (mtime 17:11 EEST, fresh), `data/reports/intraday/2026-07-18_14-17_intraday_report.md` (mtime 17:17 EEST, fresh), `data/reports/swing/2026-07-18_01-47_swing_report.md` (mtime 04:47 EEST, ~13h53m old, **borderline stale**, its one B-tier idea VIRTUAL/USDT already `stopped` per direct signal lookup — dropped), `data/reports/stocks/intraday/2026-07-17_21-56_stocks_intraday_report.md` (mtime 00:56 EEST, ~17h44m old, **stale**, moot — market closed all weekend), `data/reports/stocks/swing/2026-07-02_13-03...` and `stocks/invest/2026-07-02_13-05...` (~16 days old, **stale**, mentioned for continuity only).
- Catalyst: `data/catalysts/2026-07-18/catalyst_events.jsonl` (2866 rows this run, 558 mapped / 2308 unmapped), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_14-19.md` (latest cycle, mtime 17:19 EEST, fresh).
- LLM packet: `data/processed/llm_analysis_packet.md` (mtime 17:17 EEST, fresh — cohort-performance table re-checked, unchanged from 16:30 review: `crypto_intraday_catalyst_or_momentum` no-catalyst variant WR 23%/PF 0.70/−3R). `llm_stocks_packet.md` ~28h old, stale, not used, market closed.
- Internal CLI: `active-signals --asset-class crypto` (3 rows: ALLO `waiting_for_entry` [new], NEAR `tp1_hit`, ONDO `tp2_hit` — TRUMP no longer listed, resolved to `stopped`), `active-signals --asset-class stocks` (50 rows, all resolved/closed, market shut), `signal-stats --asset-class crypto` (week: A/B headline sample=85, PF 1.72, totalR +12.9 — direction=short and mode=scalp both still structurally losing), `signal-stats --asset-class stocks` (week: A/B headline sample=11, PF 0.75, totalR −0.5), `detect_untracked_legacy_alerts --since 2026-07-18` (0 results, clean — 3rd consecutive clean run).
- SQLite direct reads (read-only, `db/crypto_ai_desk.sqlite`): full `proposed_signals` row dumps for `sig_439295cfed1d5367` (TRUMP, confirms `status=stopped`, `updated_at=2026-07-18T13:37:41Z`) and `sig_10088a4c71cae845` (ALLO, full entry/TP/stop/thesis), `proposed_signals` history for `VIRTUAL/USDT` (confirms the 04:47 swing long is `status=stopped`), `news_items` filtered on `ALLO`/`ONDO`/`NEAR` in the last 24h (ALLO: 0 rows — no internal catalyst; ONDO: 2 rows, team-wallet-to-Coinbase transfer risk, unchanged from prior review; NEAR: 0 rows).
- External: WebSearch ×1 ("ALLO token crypto news July 2026 catalyst") + WebFetch ×1 (coinpedia.org article, verified publish date). Finding: ALLO's rally traces to a real product catalyst — Allora Network's "Forge" launch on **2026-07-02**, part of a broader AI-narrative rotation (ALLO/BILL). This confirms the move is not baseless noise, but the catalyst is **~16 days old**, not a fresh trigger for today's specific +18% print — consistent with the internal system's `news_supported=0` / "no fresh verified catalyst" read for *today*.

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime 2026-07-18 17:34 EEST — fresh (~1h06m old at review start).
- Latest cycle summary: `cycle_06_17-03_summary.md`, mtime 17:34 EEST — clean.
- Paper monitor status (from cycle_06, 17:34 EEST snapshot, **predates** the 18:21 EEST ALLO trigger): Open actionable 0, Waiting for entry 0, Review/Shadow 60, Entered unresolved 0, No-entry/stale/moved-away 29, Closed today 151W/18L/13flat, Needs review 0. Losses/flats ticked up by +1/+1 vs the 16:30 review's cycle_05 snapshot (151W/17L/12flat) — consistent with the TRUMP/USDT stop-out landing inside this window.
- **Live delta not yet in a paper-monitor snapshot**: ALLO/USDT (`waiting_for_entry`, created 18:21 EEST) will show as Waiting-for-entry=1 in the next cycle's pass.
- Reports: scalp/intraday fresh (~1h20-30m); swing borderline stale (~13h53m, its one idea already invalidated); stocks intraday/swing/invest stale and excluded — moot, market closed.
- **Not deferred.**

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-18 18:40 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"],
      "data_missing": ["stocks intraday/swing/invest reports (stale, market closed anyway)", "live paper-monitor snapshot post-dates ALLO trigger"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_06 mtime 17:34 EEST", "scalp/intraday fresh ~1h20-30m old", "catalyst mapping 80.5% unmapped this run"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC uptrend / ETH range, altcoin breadth 34.2% above EMA20 (down from 39.5% at 16:30)", "macro risk 72.6/100, risk-off headwind (up from 67.2/100), fresh Iran/Gulf headlines (GCC condemnation, Iran suspends MoU, Kuwait/Iraq fuel-routing)", "market_dashboard regime=transition matches report-level classifier"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["80.5% unmapped catalyst events today (2308/2866)", "ALLO/USDT news_supported=0 for today specifically, but external WebSearch/WebFetch confirms a real underlying product catalyst (Forge launch, 2026-07-02, AI-narrative rotation) — dated, not fresh", "momentum_breakout basket (fresh <1h) names ALLO/USDT as sole primary", "ONDO team-wallet-to-Coinbase sell-pressure risk unchanged/unresolved"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "ok",
      "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["order book depth/CVD", "liquidation heatmaps"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/USDT: price up + OI up (fresh positioning confirms trend), funding neutral (5e-05), long/short 0.677, crowding normal — no squeeze-risk cap applied", "HOME/BANK/KITE/GRAM/SNDKB/SKHYB all short-squeeze-risk capped to C, unchanged"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["entry_fresh", "clean_retest", "chase_risk"],
      "data_missing": ["live price vs ALLO entry/TP1 zone at time of writing"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/USDT rejected at score 40.0 in the 17:17 EEST intraday report (\">2 ATR from EMA20, do not chase\"), re-scored 65.9 (pullback, retest-confirmed, weekend-mode) and triggered at 18:21 EEST — identical mechanism to the TRUMP/USDT trigger the prior review flagged", "entry zone 0.4441-0.4516, stop 0.4350, TP1 0.4715/RR1.2"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "needs_review",
      "confidence": 0.8,
      "reason_codes": ["waiting_for_entry", "closed_flat", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/USDT status=waiting_for_entry, fresh (18:21 EEST), not yet in any paper-monitor snapshot", "TRUMP/USDT resolved CLOSED LOSS (-1R, stop hit 13:37:41 UTC) since the 16:30 review", "NEAR/USDT (tp1_hit, expired 2026-07-17T15:56 UTC) and ONDO/USDT (tp2_hit, expired 2026-07-17T08:36 UTC) both still non-terminal-past-expiry — TODO-2/10, unresolved 2 days running"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["repeated_losses", "headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/USDT is the exact same cohort (no-catalyst weekend-retest intraday momentum) that just produced TRUMP/USDT's -1R loss — same playbook, same gating mechanism, same missing-catalyst flag", "direction=short still a losing bucket this week (PF 0.20, totalR -4.0)", "mode=scalp still structurally losing (PF 0.17, 0W/7L)", "macro risk ticked up to 72.6/100 (from 67.2) on fresh Iran/Gulf headlines"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "fresh_expired_problem"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_intraday_catalyst_or_momentum (no-catalyst variant) 14d WR 23%/PF 0.70/-3R, unchanged from the LLM packet — TRUMP/USDT's loss this cycle is a fresh, in-sample data point confirming this exact number", "weekend_mode=Y bucket overall still shows PF 4.8/avgR 0.69 (n=16, thin sample) — the aggregate weekend-retest mechanism has a positive track record even though this specific no-catalyst sub-cohort inside it is weak; the two stats are not contradictory, just different granularity", "mode=intraday overall still strong this week (PF 3.25)"]
    },
    {
      "agent": "head_trader",
      "verdict": "watch_only",
      "confidence": 0.55,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["one fresh, not-yet-filled B-tier setup (ALLO/USDT, waiting_for_entry) in a cohort that just produced a same-pattern loss two hours prior — treat as research-grade/reduced-size if it fills, not a clean high-conviction alert", "no clean A-tier anywhere", "stocks fully closed, Saturday"]
    }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "ALLO/USDT", "trigger": "waiting_for_entry, zone 0.4441-0.4516; if filled, respect stop 0.4350 and treat as research-grade — same no-catalyst weekend-retest cohort (WR 23%/PF 0.70) that just produced TRUMP/USDT's -1R loss two hours earlier; do not add size on strength alone" },
    "best_short_candidate":    { "symbol": "RE/USDT", "trigger": "still overextended (-10.1% 24h) and extreme negative funding against shorts per the 17:17 EEST report; needs a confirmed failed-bounce/retest with a stop above the swing high before it is actionable — unchanged from prior reviews" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "RWA/tokenization thesis (fresh <6h basket) still live but explicitly contradicted by the corroborated team-wallet-to-Coinbase transfer (~10:00 UTC today); existing signal already tp2_hit/closed — watch for a fresh print that prices the sell-pressure risk" },
    "avoid_candidate":         { "symbol": "HOME/USDT", "reason": "-18.5% 24h, thin liquidity, short-squeeze-risk capped to C, no fresh catalyst — unchanged avoid across every review this weekend" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 9
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, catalyst_missing | advisory_only |
| market_regime | caution | 0.60 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | entry_fresh, clean_retest, chase_risk | advisory_only |
| execution_lifecycle | needs_review | 0.80 | waiting_for_entry, closed_flat, needs_review | advisory_only |
| risk_manager | caution | 0.65 | repeated_losses, headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, playbook_working, fresh_expired_problem | advisory_only |
| head_trader | watch_only | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-18_1630.md` (16:30 EEST, pre-US-open decision review). ~2h10m elapsed — this lands on its own 18:30 EEST slot.

- **TRUMP/USDT resolved: stopped out (-1R)** at 13:37:41 UTC / 16:37 EEST — roughly 7 minutes after the prior review published its "manage, don't chase" guidance. Entry 1.6767, stop 1.6402 hit exactly (risk_per_unit = 0.0365, no slippage note visible). This is a real, in-sample data point confirming the no-catalyst-cohort caution the prior review raised.
- **NEW: ALLO/USDT crypto intraday long, `waiting_for_entry`** (`sig_10088a4c71cae845`, B-tier, score 65.9). Not present in the 16:30 review's 3-row active-signals list. Created 15:21 UTC / 18:21 EEST — the one substantive new decision-relevant fact this cycle, and structurally the same setup type that just failed (see §7.1).
- **Macro risk score up**: 67.2 → 72.6/100, on fresh Iran/Gulf headlines (GCC condemnation of strikes on Bahrain/Kuwait/Jordan, Iran suspending MoU commitments with the US, Iraq re-routing fuel trucks around the Strait of Hormuz). Altcoin breadth above EMA20 also softened, 39.5% → 34.2%.
- **DODO/USDT, RE/USDT, ONDO/USDT (catalyst-watch), HOME/BANK (avoid)** — unchanged from the 16:30 review; same underlying scan lineage (17:11-17:17 EEST reports supersede 14:39-14:44 EEST but the picture for these names is materially the same).
- **VIRTUAL/USDT** — confirmed via direct signal lookup: the 04:47 EEST swing-long thesis is `status=stopped`. Formally dropped from watch (was already flagged "invalidated" in the 16:30 review on softer evidence; now confirmed terminal).
- **Catalyst mapping** — 80.5% unmapped this run (2308/2866, rolling buffer refreshed) vs 82.6% (2130/2579) at 16:30 — same order of magnitude, still weak, still the known recurring gap.
- **TODO backlog** — unchanged (TODO-1, 2/10, 6, 7, 8, 11, 12 carried forward); TODO-3 and TODO-9 now have a **3rd consecutive clean run** — see §14.

## 5. Catalyst Coverage

- Total `catalyst_events` today (rolling buffer): **2866**
- Mapped (non-null symbol): **558 (19.5%)**
- Unmapped (null symbol): **2308 (80.5%)**
- `narrative_baskets` count: **5**

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Consistent with the project's known scan-time `news_supported` under-fire gap (historically ~17-20% match rate; TODO-12/known issue, not re-opened here). Top unmapped headline categories this run: Binance routine exchange trading-parameter notices (leverage/funding-frequency adjustments on low-float pairs like LRC), stablecoin mint alerts (USDC Treasury), and crypto-policy headlines (CLARITY Act Senate scheduling commentary) — all whole-market relevant but not symbol-attributable by the current resolver.

## 6. Market Landscape

- BTC trend: uptrend. ETH trend: range. Altcoin breadth above EMA20: 34.2% (down from 39.5% at 16:30); above EMA50: 36.8%. Volatility: BTC ATR percentile 24.0 ("normal/unknown").
- Macro/geopolitical risk score: **72.6/100** (BTC bias: risk-off headwind), up from 67.2 at 16:30. Dominant driver remains the US-Iran/Gulf conflict — fresh headlines this cycle: GCC condemns Iranian attacks on Bahrain/Kuwait/Jordan as war crimes, Iran suspends MoU commitments with the US amid renewed sanctions, Iraq routing fuel trucks through Syria to avoid the Strait of Hormuz. This reads as an *escalation* in headline flow versus the "de-escalating market reaction" framing of the 16:30 review — worth watching closely into Sunday/Monday.
- Exploit/security overhang unchanged: SOL bridge attack (Across Protocol, funds reported safe), ETH-side Ostium exploit ($23.75M USDC stolen, laundered via Tornado Cash), BONK post-exploit sell-pressure risk — none are active candidates, but they keep alt-long aggression capped.
- Stocks: closed (Saturday). Every stocks reference is Monday-planning-only.

### Market Mood / Risk Routing

- Crypto mood: **transition / mixed, tilting more risk-off than the 16:30 read** — macro score rising, breadth softening, BTC still technically up but ETH range-bound.
- Stocks mood: **closed** (weekend).
- Dominant narrative: AI-sector rotation (ALLO's real but dated Forge-launch catalyst) and momentum-only cluster (XEC/BTW/ALLO) remain the cleanest long-side story; RWA/tokenization (ONDO/XLM) stays contradicted by the unresolved sell-pressure headline.
- Preferred side now: **wait-for-trigger**, with one not-yet-filled research-grade long (ALLO/USDT) to watch rather than chase, and elevated caution given TRUMP/USDT's same-cohort loss two hours ago.
- Best long candidate: **ALLO/USDT** — `waiting_for_entry` zone 0.4441-0.4516; treat as research-grade, same weaker no-catalyst cohort that just lost on TRUMP.
- Best short candidate: **RE/USDT** — none clean yet; needs a confirmed failed-bounce/retest, not the current extended print.
- Best catalyst-backed candidate: **ONDO/USDT** — RWA thesis vs. corroborated sell-pressure headline, unresolved; existing signal already closed.
- What to avoid: **HOME/USDT** / **BANK/USDT** (thin, squeeze-prone, no catalyst); avoid chasing XEC/BTW/ALLO above the defined entry zone.
- What would change the view: ALLO/USDT filling and then hitting TP1/TP2 or stop (a second data point on this specific cohort within hours of the first), a volume-confirmed pullback on DODO, a confirmed failed-bounce on RE, a fresh escalation/de-escalation headline on Iran/Gulf, or Monday's US cash open.

## 7. Candidate Deep Dives

### 7.1 ALLO/USDT (crypto, long, waiting_for_entry — primary focus this cycle)

- Has price already reacted to the catalyst? The underlying catalyst (Forge launch) is from 2026-07-02, already fully priced in over two weeks; today's +18.3% 24h move is a fresh continuation leg, not a first reaction.
- Is the setup chasing? It *was* — rejected at score 40.0 in the 17:17 EEST report for being >2 ATR from EMA20. It has since pulled back into the desk's defined entry zone (0.4441-0.4516) and was re-scored to 65.9/B under weekend-mode retest-after-impulse gating, triggering at 18:21 EEST. Chasing *above* 0.4516 now would be late; the defined zone itself is not chasing.
- Retest/pullback structure? Yes — `setup_type=pullback`, same mechanism that converted TRUMP/USDT from rejected to triggered a few hours earlier.
- Overextended now? Not at the trigger print (that was the original rejection reason, since resolved by the pullback).
- Would a fresh entry now be late? Only above the entry-zone high (0.4516); within the zone it is the defined entry, not a chase.
- Aligned with current market mood? Partially — mood is wait-for-trigger/mixed-tilting-risk-off; ALLO is the one name that cleared its trigger condition this cycle, on a cohort with a below-average historical edge.
- Long, short, or wait-for-trigger? Long, not yet filled (`waiting_for_entry`) — a genuine forward entry decision, unlike TRUMP which was already filled by review time.
- Actionable now or after confirmation? Already trigger-confirmed by the desk's own retest logic; the only remaining question is whether price fills the zone.
- What would invalidate it? A 1h close beyond stop 0.4350, or a BTC breakdown against the uptrend thesis.
- Chase-risk setup? Resolved by the retest, same as TRUMP was.
- Catalyst confirmation or contradiction? `news_supported=0` for today specifically — no internal `news_items` row for ALLO in the last 24h. **External verification (WebSearch + WebFetch, coinpedia.org, confirmed publish date 2026-07-13) found a real underlying catalyst — Allora's "Forge" product launch on 2026-07-02, part of a broader AI-narrative rotation (ALLO+BILL) — but it is ~16 days old, not a fresh trigger.** This is genuine narrative support, not fabricated momentum, but it does not lift ALLO out of the `crypto_intraday_catalyst_or_momentum` **no-catalyst** scoring lane (which requires a *fresh*, dated-today catalyst to qualify for the stronger lane).
- **Primary caution — same cohort, same-day prior loss**: ALLO/USDT sits in the exact playbook/cohort (`crypto_intraday_catalyst_or_momentum`, no-catalyst variant, weekend-mode retest-after-impulse) that TRUMP/USDT occupied when it stopped out for -1R at 16:37 EEST, roughly two hours before this signal triggered. Cohort 14d track record: WR 23%/PF 0.70/−3R (LLM packet, unchanged this run). This does not make ALLO a bad trade by itself — the broader `weekend_mode=Y` bucket is PF 4.8/avgR 0.69 over a thin n=16 sample — but it is the second same-mechanism setup inside a few hours, and the first one just lost. Treat as research-grade; do not oversize.
- **TradingView / manual chart check unavailable.** Using only local OHLCV/ATR/EMA fields plus the signal row.

### 7.2 DODO/USDT (crypto, long, watch-only — unchanged from 16:30 review)

- Cleanest RS long in today's scan without the >2ATR overextension tag; rejected only for weak volume (0.1x per the 17:17 EEST report) and no catalyst.
- Trigger to become actionable: volume expansion toward the 20-period average, plus either a fresh verified catalyst or a clean 15m-1h pullback/retest structure — do not chase the existing +7.1% move.
- **TradingView unavailable.**

### 7.3 RE/USDT (crypto, short, watch-only — unchanged from 16:30 review)

- -10.1% 24h, RS -11.7% vs BTC, extreme negative funding against shorts (squeeze risk flagged explicitly in the rejected-setups list) — shorting the current print would be chasing/late and squeeze-prone.
- Trigger: a confirmed failed-bounce/retest with bearish HTF structure and a stop above the swing high.
- direction=short remains a losing bucket this week (PF 0.20, totalR -4.0, n=12) — extra caution on any short right now. **TradingView unavailable.**

### 7.4 ONDO/USDT (crypto, catalyst-watch, existing signal closed — unchanged from 16:30 review)

- Tracked signal `sig_a914cdba49291324` (B, intraday, long) already hit `tp2_hit`; its `expires_at` (2026-07-17T08:36 UTC) is now over a day in the past while status remains non-terminal — see TODO-2/10.
- Live contradiction unresolved: bullish RWA/DTCC/SBI institutional thesis (rwa_narrative basket, fresh <6h, primary ONDO+XLM) vs. the corroborated team-wallet-to-Coinbase transfer (~10:00 UTC today, AMBCrypto) — a historical precursor to exchange-sale pressure.
- Actionable only if/when a fresh signal explicitly prices the sell-pressure risk. **TradingView unavailable.**

## 8. Best Candidates Ranked

1. **ALLO/USDT (waiting_for_entry, research-grade)** — zone 0.4441-0.4516, stop 0.4350, TP1 0.4715 (RR 1.2)/TP2 0.4880 (RR 2.2); same no-catalyst cohort that lost on TRUMP/USDT two hours earlier — see §7.1 for the full caution.
2. **Best long-watch (fresh entry): DODO/USDT** — wait for volume pickup or a fresh catalyst; do not chase the current print.
3. **Best short-watch: RE/USDT** — wait for a confirmed failed-bounce/retest with a stop above the swing high; squeeze-risk flagged, and shorts are a losing bucket this week.
4. **Best catalyst-watch: ONDO/USDT** — RWA thesis vs. corroborated sell-pressure headline; watch for a fresh signal that prices the risk explicitly.
5. **Dropped from watch: VIRTUAL/USDT** — confirmed `status=stopped` via direct signal lookup; the 04:47 EEST swing-long thesis is terminally invalidated, not merely stale.

## 9. Avoid / No Trade

This decision window only — never a system-stop signal; scanning/tracking continues in all cases.

- **HOME/USDT** — -18.5% 24h, thin liquidity, short-squeeze-risk capped to C, no fresh catalyst.
- **BANK/USDT** — carried avoid from prior reviews, same squeeze-risk profile.
- **Any `momentum_breakout`-basket name above its defined entry zone** (ALLO above 0.4516, XEC/BTW at current extended prices) — chasing above the desk's own retest-confirmed zone.
- **TRUMP/USDT as a fresh re-entry** — already resolved CLOSED LOSS (-1R); no re-entry signal exists, and re-chasing this specific no-catalyst cohort twice in one session would compound the demonstrated edge weakness.
- **Stocks, broadly** — market closed all weekend; every stocks reference is planning-only until Monday's RTH open.

## 10. Main Risks

- **Same-cohort repeat risk**: ALLO/USDT is the second `crypto_intraday_catalyst_or_momentum` (no-catalyst, weekend-mode-gated) trigger today, immediately following TRUMP/USDT's -1R stop-out in the same cohort. The cohort's 14d edge (WR 23%/PF 0.70/−3R) is real and now has a fresh in-sample confirmation this cycle — one loss doesn't move the base rate meaningfully, but it is the most decision-relevant risk fact this run.
- **Geopolitical escalation**: macro risk score rose 67.2→72.6/100 on fresh Iran/Gulf headlines (GCC war-crimes condemnation, Iran suspending US MoU commitments, Strait of Hormuz fuel-routing workarounds) — a genuine escalation in headline flow, not just a continuation of prior de-escalating tone.
- **ONDO sell-pressure**: corroborated team-wallet-to-Coinbase transfer remains a real, unresolved risk on the RWA narrative's cleanest name.
- **Exploit overhang**: SOL bridge attack and ETH-side Ostium exploit ($23.75M) both still live this week; keep alt-long aggression capped per the report's own macro note.
- **Data-quality / lifecycle hygiene**: catalyst mapping at 19.5%; NEAR/ONDO both still non-terminal-past-expiry (TODO-2/10, now confirmed unresolved 2+ days running); `news_items.published_at` format inconsistency (TODO-12) means raw SQL freshness filters remain fragile — this review used direct signal-row reads and report-embedded freshness labels defensively.
- **Live-execution-adjacent**: `mexc_canary_monitor` crash-loop on `database is locked` (TODO-8) not independently re-checked this run — carried forward from the 16:30 review, still high priority, out of the allowed read scope to re-verify without an explicit log-check permission.

## 11. Action Plan — next 4 hours

1. Watch ALLO/USDT for a fill in the 0.4441-0.4516 zone; if filled, treat as research-grade given the same-cohort loss two hours ago — respect the stop at 0.4350, no size-adding on strength alone.
2. Monitor DODO/USDT for a volume pickup or fresh catalyst; no entry without one.
3. Monitor RE/USDT for a failed-bounce/retest structure; no entry on the current extended, squeeze-prone print.
4. Watch for a fresh ONDO/USDT scan-level score now that the wallet-transfer headline has had a full day to be priced in.
5. Keep VIRTUAL/USDT off any active watchlist — confirmed terminally stopped, not just stale.
6. Track whether the Iran/Gulf headline flow keeps escalating into Sunday/Monday; a further macro-risk jump would argue for tighter crypto risk routing next cycle.
7. No stocks action possible or expected until Monday 2026-07-20's RTH open.
8. Continue scanning/tracking/monitors as normal — no pause or stop recommended anywhere in this review.

## 12. Final Verdict per Mode

- **Crypto scalp**: No trade. Structurally losing bucket this week (PF 0.17, 0W/7L) — unchanged, treat any future scalp signal with extra skepticism.
- **Crypto intraday**: **Watching one not-yet-filled setup** (ALLO/USDT, research-grade, same no-catalyst cohort that lost on TRUMP/USDT two hours ago — respect the plan if it fills, no fresh chase). Mode performance strong this week overall (PF 3.25) but concentrated outside this specific weaker sub-cohort.
- **Crypto swing**: Watch-only, no trade. VIRTUAL/USDT thesis confirmed terminally invalidated; no other swing idea this cycle (report ~13h53m old).
- **Stocks (all modes)**: Closed / no trade. Planning-only until Monday's RTH open.

## 13. Sources

- [ALLO Price Jumps 40% While BILL Surges 45% as AI Crypto Narrative Accelerates](https://coinpedia.org/price-analysis/allo-price-jumps-40-while-bill-surges-45-as-ai-crypto-narrative-accelerates/) — Coinpedia, published 2026-07-13 (verified via WebFetch; confirms the Forge-launch catalyst is dated ~2026-07-02, not fresh for today).
- Internal: `db/crypto_ai_desk.sqlite` `proposed_signals` full rows for `sig_439295cfed1d5367` (TRUMP, confirms stop-out) and `sig_10088a4c71cae845` (ALLO, full entry/TP/stop/thesis).
- Internal: `data/catalysts/2026-07-18/catalyst_cycle_14-19.md`, `narrative_baskets.jsonl`.
- Carried forward from the 16:30 EEST review (unchanged facts, not independently re-verified this run): [US-Iran military escalation rocks crypto markets](https://cryptobriefing.com/us-iran-strikes-bitcoin-crypto-market-reaction/) — CryptoBriefing; [Analyst Flags $49.56M ONDO Transfer from Team Wallet as Potential Sell-Off](https://cryptonews.net/news/altcoins/33048535/) — CryptoNews; [Ondo Finance moves $63.9mln: Is a sell-off looming?](https://ambcrypto.com/ondo-finance-moves-63-9mln-is-a-sell-off-looming/) — AMBCrypto.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, unchanged, informational)
- **issue:** Stocks intraday A/B guard combination continues to demote technically-qualified candidates via the market-closed gate. Fully expected/by-design on a Saturday.
- **evidence:** `data/reports/stocks/intraday/2026-07-17_21-56_stocks_intraday_report.md` — `market_closed_intraday_planning_only` caps applied.
- **suggested manual fix:** none needed; by-design.
- **priority:** low.
- **first observed:** 2026-07-16 18:39 EEST; re-confirmed 2026-07-18 18:40 EEST.

### TODO-2 / TODO-10 (carried forward, unchanged — still high)
- **issue:** Crypto and stocks signals continue to show `expires_at` timestamps in the past while still displaying non-terminal statuses.
- **evidence:** NEAR/USDT (`tp1_hit`, expires 2026-07-17T15:56 UTC — now >2 days past expiry) and ONDO/USDT (`tp2_hit`, expires 2026-07-17T08:36 UTC — now >2 days past expiry) both still non-terminal as of this run.
- **suggested manual fix:** human check of the lifecycle/track-signals terminalization job for both asset classes.
- **priority:** high.
- **first observed:** 2026-07-16 16:20 EEST (stocks); 2026-07-17 16:29 EEST (crypto); re-confirmed 2026-07-18 18:40 EEST, gap widening (now >2 days for both symbols).

### TODO-3 (closed-out candidate — 3 consecutive clean runs)
- **issue:** `detect_untracked_legacy_alerts` had returned 2 unresolved results (ALLO/USDT, BANK/USDT) across 4+ consecutive reviews.
- **evidence:** clean (0 results) at the 15:48 EEST, 16:30 EEST, and this 18:40 EEST run — 3rd consecutive clean run. Notably ALLO/USDT itself produced a clean, correctly-minted fresh signal this cycle (`sig_10088a4c71cae845`), which is a positive signal specifically for the ALLO reuse-bug concern.
- **suggested manual fix:** none needed; recommend downgrading to low priority / closing if it stays clean through Sunday/Monday.
- **priority:** low (downgraded from medium).
- **first observed:** 2026-07-16 18:39 EEST; not reproducing as of 2026-07-18 18:40 EEST (3rd consecutive clean run).

### TODO-6 (carried forward, unchanged)
- **issue:** Crypto scalp mode remains a consistent losing bucket.
- **evidence:** `signal-stats --asset-class crypto` this cycle: `mode=scalp | n=22 | trig=20 | wins=0 losses=7 | PF 0.1667 | totalR -5.0` — identical to prior reviews, same underlying week window.
- **suggested manual fix:** human review of whether scalp (and/or short-direction plays) should carry an explicit non-actionable label.
- **priority:** medium.
- **first observed:** 2026-07-17 11:45 EEST.

### TODO-7 (carried forward, unchanged — still high)
- **issue:** Stocks earnings-calendar lookup failing broadly.
- **evidence:** unchanged since the 16:30 review, no fresher stocks report exists (market closed, none expected until Monday).
- **suggested manual fix:** human audit of the earnings-calendar source/ingestion.
- **priority:** high.
- **first observed:** 2026-07-17 11:45 EEST.

### TODO-8 (carried forward, unchanged — still high, not independently re-checked this run)
- **issue:** `mexc_canary_monitor` crash-looping on `sqlite3.OperationalError: database is locked` inside `ensure_tables()`.
- **evidence:** last confirmed via `mexc_canary_monitor_*.log` at the 15:48 EEST review; not re-pulled this run (out of scope for the allowed read set without a fresh log check).
- **suggested manual fix:** human investigation of lock contention on `db/crypto_ai_desk.sqlite` around `mexc_canary_control` writes.
- **priority:** high.
- **first observed:** 2026-07-17 11:45 EEST.

### TODO-9 (closed-out candidate — 3 consecutive clean runs)
- **issue:** `market_dashboard_snapshots.crypto_market_mode` had looked decoupled from the report-level regime classifier.
- **evidence:** clean/consistent (`transition` matching report-level) at the 15:48 EEST, 16:30 EEST, and this 18:40 EEST run.
- **suggested manual fix:** none needed; recommend closing if it stays consistent through Sunday/Monday.
- **priority:** low (downgraded from medium).
- **first observed:** 2026-07-17 11:45 EEST; not reproducing as of 2026-07-18 18:40 EEST (3rd consecutive clean run).

### TODO-11 (carried forward, improving — watch one more cycle before closing)
- **issue:** This task and/or its sibling tasks appeared to skip six consecutive scheduled dispatches between 2026-07-17 16:29 EEST and 2026-07-18 15:48 EEST, with no DEFERRED/BLOCKED marker.
- **evidence:** 2nd consecutive on-time dispatch this run (16:30 EEST slot landed on-time, and this 18:30 EEST slot also landed on-time, ~18:40 EEST completion). Two clean on-time dispatches in a row is a positive trend but the 21:30 and 23:15 slots today are still worth watching before downgrading further.
- **suggested manual fix:** human check of the outer scheduling mechanism; continue monitoring dispatch timestamps across the remaining slots today.
- **priority:** medium (downgraded from high — 2 consecutive on-time dispatches).
- **first observed:** 2026-07-18 15:48 EEST; 2nd positive signal 2026-07-18 18:40 EEST.

### TODO-12 (carried forward, unchanged — medium)
- **issue:** `news_items.published_at` stores inconsistent datetime formats (mixed UTC offsets, `Z` suffix, literal `date_unavailable` rows), breaking naive lexicographic freshness filtering.
- **evidence:** this run's `ALLO`/`ONDO`/`NEAR` freshness checks (`published_at > datetime('now','-24 hours')`) were run defensively assuming this bug is still present; returned clean results but the underlying format inconsistency was not re-audited/fixed.
- **suggested manual fix:** human audit of the `published_at` normalization step in the news ingestion pipeline.
- **priority:** medium.
- **first observed:** 2026-07-18 15:48 EEST.
