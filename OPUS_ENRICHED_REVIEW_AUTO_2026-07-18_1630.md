# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:30 EEST

## 1. Executive Summary

**Slot: pre-US-open decision review (nominal 16:20 EEST), completed ~16:30 EEST on Saturday 2026-07-18. Advisory only — no auto-trade, no code/scoring/routing changes.** Pipeline healthy and not deferred: `scheduler.log` / latest `cycle_05_14-30_summary.md` both mtime 15:03 EEST (~1h27m old at review start), well under the 3h defer threshold.

**Critical framing: today is Saturday — there is no US cash open today.** "Pre-US-open" is nominal only; US equities remain closed through the weekend. Every stocks reference below is planning/watchlist context for Monday 2026-07-20's open, not an actionable decision for this window. Crypto is the sole live actionable class.

**Headline finding — genuinely new since the last review** (`OPUS_ENRICHED_REVIEW_AUTO_2026-07-18_1548.md`, completed 15:48 EEST): a fresh B-tier crypto intraday long **triggered** on **TRUMP/USDT** (`sig_439295cfed1d5367`) between the two reviews — created 12:46:09 UTC (15:46 EEST), triggered/filled 13:00:10 UTC (16:00 EEST). The 14:44 EEST intraday report had explicitly *rejected* TRUMP/USDT as a chase (score 29.4, ">2 ATR from EMA20, do not chase"); the desk's own weekend-mode "require retest after impulse" logic then re-scored it as a valid B-tier **pullback** setup (score 65.1) once price retraced into the entry zone — this is the risk-gating system working as designed, not a data anomaly. It carries **no verified catalyst** (`news_supported=0`) and sits in the historically weaker "no-catalyst intraday momentum" cohort (WR 23% / PF 0.70 / −3R per the strategy-playbook table) — see §7.1 for the full caution.

Everything else is materially **unchanged** from the 15:48 EEST review: same fresh scalp/intraday reports (14:39/14:44 EEST), same catalyst-mapping weakness (82.6% unmapped, 2130/2579), same macro risk score (67.2/100, Iran/Gulf conflict ongoing but de-escalating in market reaction), same DODO/RE/ONDO watch-only picks, same TODO backlog. See §4 for the full delta.

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-18_11-39_scalp_report.md` (mtime 14:39 EEST, fresh), `data/reports/intraday/2026-07-18_11-44_intraday_report.md` (mtime 14:44 EEST, fresh), `data/reports/swing/2026-07-18_01-47_swing_report.md` (mtime 04:47 EEST, ~11h43m old, carry-forward), `data/reports/stocks/intraday/2026-07-17_21-56_stocks_intraday_report.md` (mtime 00:56 EEST 2026-07-18, ~15h34m old, **stale**, moot — market closed all weekend), `data/reports/stocks/swing/2026-07-02_13-03_stocks_swing_report.md` and `data/reports/stocks/invest/2026-07-02_13-05_stocks_invest_report.md` (both ~16 days old, **stale**, excluded, mentioned for continuity only).
- Catalyst: `data/catalysts/2026-07-18/catalyst_events.jsonl` (2579 rows, 449 mapped / 2130 unmapped), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_11-47.md` (latest cycle, mtime 14:47 EEST).
- LLM packet: `data/processed/llm_analysis_packet.md` (generated 11:44:51 UTC / 14:44 EEST, fresh). `data/processed/llm_stocks_packet.md` is ~26h old (generated 2026-07-17T14:25 EEST) — stale, not used for any live decision, market closed anyway.
- Internal CLI: `active-signals --asset-class crypto` (**3 rows** — up from 2 rows in the 15:48 review; new row is the TRUMP/USDT trigger), `active-signals --asset-class stocks` (50 rows, all resolved/expired/closed), `signal-stats --asset-class crypto` (week: A/B headline sample=87, PF 2.0353, totalR +17.6), `signal-stats --asset-class stocks` (week: A/B headline sample=11, PF 0.75, totalR −0.5), `detect_untracked_legacy_alerts --since 2026-07-18` (0 results, clean — consistent with the 15:48 review).
- SQLite direct reads (read-only, `db/crypto_ai_desk.sqlite`): `proposed_signals` row for `sig_439295cfed1d5367` (full field dump — entry/TP/stop/thesis/counter-thesis), `news_items` filtered on `TRUMP` (0 rows in last 24h — confirms no internal catalyst), `news_items` filtered on `BONK`/`UNH`/`TSLA` (context for risk section).
- External: WebSearch ×2 — "TRUMP token OFFICIAL TRUMP coin news July 18 2026" (no crypto-specific catalyst found; only an unrelated US Mint commemorative $1 coin story that must not be confused with the TRUMP/USDT token) and "UnitedHealth UNH DOJ criminal probe Medicare fraud July 2026" (confirms this is a well-established ongoing investigation since mid-2025, not a fresh escalation — included for continuity, UNH is not an active candidate this cycle). No WebFetch performed — search summaries were sufficient and internally consistent.

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime 2026-07-18 15:03 EEST — fresh (~1h27m old at review start).
- Latest cycle summary: `cycle_05_14-30_summary.md`, mtime 15:03 EEST, `CYCLE 5 END ok=51 failed=0 telegram=sent` — clean.
- Crypto monitor (pid 21064) and derivatives monitor (pid 6172) both confirmed running at end-of-cycle 15:03 EEST; the crypto monitor is the process that generated the fresh TRUMP/USDT trigger intra-cycle (12:46–13:00 UTC), after the last full report cycle ended — expected behavior.
- Paper monitor status (from cycle_05, 15:01 EEST): Open actionable 0, Waiting for entry 0, Entered unresolved 0, Review/Shadow 61, No-entry/stale/moved-away 29, Closed today 151W/17L/12flat, Needs review 0. (Snapshot predates the TRUMP trigger by ~45min; TRUMP will show as open-actionable in the next paper-monitor pass.)
- Reports: scalp/intraday fresh (~1h45m old); swing carry-forward (~11h43m, no live crypto idea from it this run); stocks intraday stale (~15h34m) and stocks swing/invest stale (~16d) — both excluded per the >14h rule, and moot regardless since the market is closed all weekend.
- **Not deferred.**

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-18 16:30 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "catalyst_missing"],
      "data_missing": ["stocks intraday/swing/invest reports (stale, market closed anyway)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_05 mtime 15:03 EEST", "scalp/intraday fresh ~1h45m old", "catalyst mapping 82.6% unmapped"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["mixed", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC uptrend / ETH range, altcoin breadth 39.5% above EMA20", "macro risk 67.2/100, risk-off headwind, Iran/Gulf conflict ongoing but market reaction de-escalating", "market_dashboard regime=transition matches report-level classifier"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["82.6% unmapped catalyst events today (2130/2579), unchanged from 15:48 review", "TRUMP/USDT trigger has news_supported=0, no internal or external catalyst found", "rwa_narrative basket fresh <6h, primary ONDO"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.4,
      "reason_codes": ["data_unavailable", "squeeze_risk"],
      "data_missing": ["order book depth/CVD", "liquidation heatmaps", "TRUMP/USDT live OI delta since trigger"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/USDT funding neutral (bybit 5e-05, okx -1.14e-04) as of 14:44 EEST report, crowding normal/low at that snapshot", "HOME/BANK short-squeeze-risk capped to C"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["entry_fresh", "clean_retest", "overextended"],
      "data_missing": ["live price vs entry/TP1 zone at time of writing"],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/USDT rejected at score 29.4 (chase) in the 14:44 EEST report, re-scored 65.1 (pullback, retest-confirmed) by 16:00 EEST per weekend-mode retest gating", "DODO/RE unchanged from 15:48 review — DODO not overextended but weak volume, RE overextended/chase-risk"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "needs_review",
      "confidence": 0.8,
      "reason_codes": ["open_actionable", "closed_flat", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/USDT status=triggered (filled), fresh, not yet in the 15:01 EEST paper-monitor snapshot", "NEAR/USDT tp1_hit and ONDO/USDT tp2_hit both still past expires_at with non-terminal status (TODO-2/10, recurring)"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["reduce_risk", "headline_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["TRUMP/USDT is a no-catalyst intraday-momentum cohort trade, that cohort's 14d edge is negative (WR 23%/PF 0.70/-3R)", "direction=short is a losing bucket this week (PF 0.20, totalR -4.0)", "macro risk elevated (67.2/100) though de-escalating", "UNH DOJ probe confirmed ongoing (not fresh) via external check, not an active candidate this cycle"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto mode=intraday overall PF 4.64 this week (strong)", "but crypto_intraday_catalyst_or_momentum (no-catalyst variant) 14d WR 23%/PF 0.70/-3R — the exact cohort TRUMP/USDT falls into", "crypto mode=scalp PF 0.17, 0W/7L this week — structurally losing, unchanged"]
    },
    {
      "agent": "head_trader",
      "verdict": "watch_only",
      "confidence": 0.55,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["one fresh, already-filled B-tier trigger (TRUMP/USDT) with a cohort-level negative historical edge — treat as research-grade per the packet's own sizing guidance (0.5x-equivalent caution), not a clean high-conviction alert", "no clean A-tier anywhere", "stocks fully closed, Saturday"]
    }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.55,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "TRUMP/USDT", "trigger": "already triggered/filled (entry 1.6603-1.6767, stop 1.6402, TP1 1.7205/RR1.2, TP2 1.757/RR2.2) — retest-confirmed pullback, RS-leader momentum 87, but no catalyst and the no-catalyst intraday cohort has a negative 14d edge (WR 23%/PF 0.70); treat as research-grade, respect the stop, do not add size on strength alone" },
    "best_short_candidate":    { "symbol": "RE/USDT", "trigger": "confirmed failed-bounce/retest of breakdown structure with a stop above the swing high; do not short the current extended print (unchanged from 15:48 review)" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "a fresh setup on continued RWA/tokenization narrative strength that explicitly prices the corroborated team-wallet-to-Coinbase sell-pressure risk; the existing sig_a914... is already closed (tp2_hit), not itself re-actionable" },
    "avoid_candidate":         { "symbol": "HOME/USDT", "reason": "-14.97% 24h, thin liquidity, short-squeeze-risk capped to C, no fresh catalyst — unchanged avoid from prior reviews" },
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
| market_regime | caution | 0.65 | mixed, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, squeeze_risk | advisory_only |
| technical_entry | caution | 0.55 | entry_fresh, clean_retest, overextended | advisory_only |
| execution_lifecycle | needs_review | 0.80 | open_actionable, closed_flat, needs_review | advisory_only |
| risk_manager | caution | 0.60 | reduce_risk, headline_risk | advisory_only |
| playbook_performance | caution | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | watch_only | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-18_1548.md` (2026-07-18 15:48 EEST, Europe/pre-US context, off-schedule catch-up). Only ~42 minutes elapsed — this review lands squarely on its own 16:20 EEST slot (unlike the prior off-schedule dispatch), a positive signal for TODO-11 (scheduling-gap finding) — see §14.

- **NEW: TRUMP/USDT crypto intraday long triggered** (`sig_439295cfed1d5367`, B-tier, score 65.1, pullback, weekend-mode-capped). Not present in the 15:48 review (which showed only 2 active crypto signals: NEAR tp1_hit, ONDO tp2_hit). Created 12:46 UTC, filled 13:00 UTC — i.e. it fired in the window right around/after the prior review was written. This is the one substantive new decision-relevant fact this cycle. See §7.1.
- **DODO/USDT, RE/USDT, ONDO/USDT (catalyst-watch), HOME/BANK (avoid), VIRTUAL/USDT (invalidated long thesis)** — all **unchanged** from the 15:48 review; same underlying 14:44 EEST intraday report, no fresher scan exists. Carried forward verbatim in §6–9 below.
- **Catalyst mapping** — unchanged at 82.6% unmapped (2130/2579 of the same rolling buffer).
- **Macro risk** — unchanged at 67.2/100.
- **TODO backlog** — unchanged (TODO-1, 2/10, 3, 6, 7, 8, 9, 11, 12 all carried forward, see §14; no new evidence to upgrade or close any of them this run beyond the scheduling-cadence note above).

## 5. Catalyst Coverage

- Total `catalyst_events` today (rolling buffer): **2579**
- Mapped (non-null symbol): **449 (17.4%)**
- Unmapped (null symbol): **2130 (82.6%)**
- `narrative_baskets` count: **5**

**Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (Unchanged from the 15:48 review; consistent with the project's known scan-time `news_supported` under-fire gap — symbol audit historically ~17% match rate.) Top unmapped headline categories: routine exchange trading-parameter notices (funding/margin adjustments), stablecoin mint alerts, and crypto-policy headlines (e.g. CLARITY Act Senate scheduling) that are relevant to the whole market but not symbol-attributable.

## 6. Market Landscape

- BTC trend: uptrend. ETH trend: range. Altcoin breadth above EMA20: 39.5%; above EMA50: 42.1%. Volatility: BTC ATR percentile 31.0 ("normal/unknown").
- Macro/geopolitical risk score: **67.2/100** (BTC bias: risk-off headwind). Dominant driver remains the US-Iran/Gulf conflict (missile/drone strikes, Strait of Hormuz tanker incidents, oil-price pressure); per the 15:48 review's external verification this is real and ongoing but the market's price reaction has become comparatively muted versus early-July drawdowns, with Fed policy competing as the primary driver.
- Exploit/security overhang: SOL bridge attack (Across Protocol, funds reported safe), ETH-side Ostium exploit ($23.75M USDC stolen, laundered via Tornado Cash), BONK post-exploit sell-pressure risk — none of these are active candidates this cycle but keep alt-long aggression capped.
- Stocks: closed (Saturday). Treat every stocks reference as Monday-planning-only.

### Market Mood / Risk Routing

- Crypto mood: **transition / mixed / chop** — BTC constructive but ETH range-bound, breadth under 40%, no clean one-sided edge.
- Stocks mood: **closed** (weekend).
- Dominant narrative: RWA/tokenization (ONDO/XLM) fresh <6h but contradicted by a corroborated ONDO team-wallet sell-pressure headline; secondary momentum-only cluster (XEC/BTW/ALLO/TRUMP) largely overextended and chase-risk, with TRUMP the one name where a genuine pullback/retest has now formed and triggered a real (if catalyst-less) entry.
- Preferred side now: **wait-for-trigger**, with one already-filled research-grade long (TRUMP/USDT) to manage rather than chase further.
- Best long candidate: **TRUMP/USDT** — already triggered on a retest-confirmed pullback; treat as research-grade (no catalyst, weak cohort edge), respect the existing stop at 1.6402.
- Best short candidate: **RE/USDT** — none clean yet; trigger: confirmed failed-bounce retest, not the current extended print.
- Best catalyst-backed candidate: **ONDO/USDT** — fresh setup only, existing signal already closed; watch for the sell-pressure risk to be priced into any new print.
- What to avoid: **HOME/USDT** / **BANK/USDT** (thin, squeeze-prone, no catalyst); avoid chasing XEC/BTW/ALLO at current extended prices.
- What would change the view: TRUMP/USDT hitting TP1/TP2 or stopping out (resolves the open question on the no-catalyst cohort this run), a volume-confirmed pullback entry on DODO, a confirmed failed-bounce on RE, a de-escalation/escalation headline on the Iran/Gulf conflict, or Monday's US cash open bringing stocks back into play.

## 7. Candidate Deep Dives

### 7.1 TRUMP/USDT (crypto, long, already triggered — primary focus this cycle)

- Has price already reacted? Yes — this was originally a chase-rejected extended move (score 29.4, >2 ATR from EMA20) in the 14:44 EEST report; price then pulled back into the desk's defined entry zone (1.6603-1.6767) and the signal was re-scored and triggered (filled) at 13:00 UTC / 16:00 EEST.
- Is the setup chasing? No, not anymore — that is precisely what the retest confirmation resolved. It would have been chasing 1-2 hours ago; it is not chasing at the confirmed entry.
- Retest/pullback structure? Yes — explicitly the `setup_type=pullback` classification and the reason this went from rejected to triggered.
- Overextended (>2 ATR from EMA20)? Not at the moment of trigger (that was the original rejection reason, since resolved by the pullback).
- Would entry now be late? Entry has already happened (status=triggered/filled) — the open question is management, not fresh entry. A fresh chase above the filled entry zone would be late.
- What level makes/kept it actionable? Retest-confirmed pullback into 1.6603-1.6767, RS-leader momentum score 87/100, cross-exchange confirmation (bybit+okx funding both neutral/low crowding).
- Aligned with current market mood? Partially — mood is wait-for-trigger/mixed; this is the one name that actually cleared its trigger condition this cycle, but on a structurally weaker no-catalyst cohort.
- Long, short, or wait-for-trigger? Long, already filled — not a fresh entry decision.
- Actionable now or after confirmation? Already confirmed/filled; the remaining decision is TP/stop management only (out of scope for this advisory review — no TP/SL changes proposed).
- What would invalidate it? A break below stop 1.6402, or BTC/broad-market reversal against the regime thesis.
- Chase-risk setup? No, resolved by the retest.
- Catalyst confirmation or contradiction? **Neither confirmed nor contradicted** — `news_supported=0` on the signal itself; internal `news_items` has zero TRUMP-tagged rows in the last 24h; external WebSearch found no TRUMP/USDT-specific catalyst today, only an unrelated US Mint physical commemorative $1 coin story (different asset entirely — do not conflate). **Caution flag**: this signal sits in the `crypto_intraday_catalyst_or_momentum` (no-catalyst variant) cohort, whose 14-day track record is WR 23% / PF 0.70 / −3R per the strategy-playbook table embedded in the LLM packet — a materially weaker edge than the catalyst-backed variant (WR 50%/PF 2.75/+7R) or the overall intraday-mode average (PF 4.64 this week). Playbook-aware sizing already reflects this via `sized_r` weighting; this review does not propose changing it.
- Data-quality note: an external CoinGecko snapshot quoted TRUMP/USDT around $1.54-1.56, roughly 5-8% below the signal's own entry/TP band (1.66-1.72) — likely a stale/cached external quote rather than a genuine discrepancy, but flagged so no one anchors on the wrong price when reviewing this live.
- **TradingView / manual chart check unavailable.** Using only local OHLCV/ATR/EMA fields from the report and the `proposed_signals` row.

### 7.2 DODO/USDT (crypto, long, watch-only — unchanged from 15:48 review)

- Cleanest RS long in today's scan without the >2ATR overextension tag carried by ALLO/XEC/BTW/TRUMP's original print; currently rejected only for weak volume confirmation (0.42x) and no catalyst.
- Trigger to become actionable: volume expansion to ≥1x the 20-period average, plus either a fresh verified catalyst or a clean 15m-1h pullback/retest entry structure — do not chase the existing +10.2% move.
- Not aligned with mood as a clean go yet; wait-for-trigger long. **TradingView unavailable.**

### 7.3 RE/USDT (crypto, short, watch-only — unchanged from 15:48 review)

- Already -8.3% to -9.5% 24h, RS -9.5% vs BTC, tagged overextended — shorting the current print would be chasing/late.
- Trigger: a confirmed failed-bounce/retest with bearish HTF structure and a clear stop above the swing high (per the `crypto_failed_bounce_short` playbook's "promotes when" condition).
- direction=short is a losing bucket this week (PF 0.20, totalR -4.0, n=12) — extra caution on any short right now. **TradingView unavailable.**

### 7.4 ONDO/USDT (crypto, catalyst-watch, existing signal closed — unchanged from 15:48 review)

- The tracked signal (`sig_a914...`, B, intraday, long) already hit `tp2_hit` before its 2026-07-17T08:36 UTC expiry — not itself re-actionable.
- Live contradiction: bullish RWA/DTCC/SBI institutional thesis (rwa_narrative basket fresh <6h) vs. a corroborated (multi-outlet) team-wallet-to-Coinbase transfer reported ~10:00 UTC 2026-07-18, historically a precursor to exchange-sale pressure.
- Actionable only if/when a fresh signal explicitly prices the sell-pressure risk. **TradingView unavailable.**

## 8. Best Candidates Ranked

1. **TRUMP/USDT (already triggered, manage don't chase)** — filled long at 1.6603-1.6767, stop 1.6402, TP1 1.7205 (RR 1.2)/TP2 1.757 (RR 2.2); research-grade given the no-catalyst cohort's weak historical edge (WR 23%/PF 0.70) — see §7.1.
2. **Best long-watch (fresh entry): DODO/USDT** — wait for volume ≥1x 20-period avg plus catalyst or clean pullback structure; do not chase the current print.
3. **Best short-watch: RE/USDT** — wait for a confirmed failed-bounce/retest with a stop above the swing high; direction=short is a losing bucket this week.
4. **Best catalyst-watch: ONDO/USDT** — RWA thesis vs. corroborated sell-pressure headline; watch for a fresh signal that prices the risk explicitly.
5. **Invalidated (drop from watch): VIRTUAL/USDT** — the earlier 04:47 EEST swing-long thesis (RS +4.3%) flipped to `bias short`/RS -2.70% by the 14:44 EEST scan; unchanged conclusion from 15:48 review.

## 9. Avoid / No Trade

This decision window only — never a system-stop signal; scanning/tracking continues in all cases.

- **HOME/USDT** — -14.97% 24h, thin liquidity, short-squeeze-risk capped to C, no fresh catalyst.
- **BANK/USDT** — -10.79% 24h, same short-squeeze-risk cap, thin volume (0.22x).
- **Any `momentum_breakout`-basket name at current extended price** (XEC/BTW/ALLO) — pure momentum, no verified catalyst, >2ATR from EMA20.
- **TRUMP/USDT as a *fresh* add-on entry above the already-filled zone** — the trigger has already happened; adding on strength above 1.6767 would itself be chasing.
- **Stocks, broadly** — market closed all weekend; every stocks reference is planning-only until Monday's RTH open.

## 10. Main Risks

- **No-catalyst-cohort risk on the live TRUMP/USDT trigger**: the exact playbook cohort (`crypto_intraday_catalyst_or_momentum`, no catalyst) this signal falls into has a negative 14-day track record (WR 23%/PF 0.70/-3R) despite the intraday mode's strong week-level aggregate (PF 4.64) — the aggregate is being carried by catalyst-backed and swing-momentum names, not this cohort specifically.
- **Geopolitical**: US-Iran/Gulf conflict remains the dominant macro overhang (risk 67.2/100); a fresh escalation could reverse the recent de-escalation in market reaction.
- **ONDO sell-pressure**: corroborated team-wallet-to-Coinbase transfer is a real, unresolved risk on the RWA narrative's cleanest name.
- **Exploit overhang**: SOL bridge attack and ETH-side Ostium exploit ($23.75M) both active this week — neither is a current candidate but both keep alt-long aggression capped per the report's own macro note.
- **Data-quality**: catalyst mapping at 17.4%; lifecycle hygiene gap (NEAR/ONDO past `expires_at` while non-terminal, TODO-2/10, recurring); `news_items.published_at` format inconsistency (TODO-12, unchanged) means raw SQL freshness filters remain unreliable — this review used report-embedded freshness labels and direct signal-row reads instead.
- **Live-execution-adjacent**: `mexc_canary_monitor` still crash-looping on `database is locked` per the 15:48 review's TODO-8 finding (not independently re-checked this run; carried forward, still high priority).

## 11. Action Plan — next 4 hours

1. Manage the existing TRUMP/USDT trigger per its own TP/SL (1.7205/1.757/1.7935 vs. stop 1.6402) — no size-adding above the filled zone; treat as research-grade given the no-catalyst cohort's weak 14d edge.
2. Monitor DODO/USDT for a volume pickup or fresh catalyst; no entry without one.
3. Monitor RE/USDT for a failed-bounce/retest structure; no entry on the current extended print.
4. Watch for a fresh ONDO/USDT scan-level score in the next scalp/intraday cycle now that the wallet-transfer headline is public.
5. Keep VIRTUAL/USDT off any active watchlist until it re-confirms a single direction.
6. No stocks action possible or expected until Monday 2026-07-20's RTH open.
7. Continue scanning/tracking/monitors as normal — no pause or stop recommended anywhere in this review.

## 12. Final Verdict per Mode

- **Crypto scalp**: No trade. Structurally losing bucket this week (PF 0.17, 0W/7L) — unchanged, treat any future scalp signal with extra skepticism.
- **Crypto intraday**: **Managing one live position** (TRUMP/USDT, research-grade, no-catalyst cohort — respect existing stop, no fresh chase). Mode performance strong this week overall (PF 4.64) but that strength is not representative of this specific cohort.
- **Crypto swing**: Watch-only, no trade. VIRTUAL/USDT thesis invalidated; no other swing idea this cycle (report 11h43m old).
- **Stocks (all modes)**: Closed / no trade. Planning-only until Monday's RTH open.

## 13. Sources

- [Official Trump Price: TRUMP/USD Live Price Chart, Market Cap & News Today | CoinGecko](https://www.coingecko.com/en/coins/official-trump) — CoinGecko, retrieved 2026-07-18 (used for the price-discrepancy caution in §7.1 only; not a catalyst).
- [US Mint to begin striking dollar coin featuring Trump](https://abcnews.com/Politics/us-mint-begin-striking-commemorative-coin-featuring-trump/story?id=134781344) — ABC News, ~2026-07-15/17 (unrelated physical coin, cited only to explicitly rule it out as a TRUMP/USDT catalyst).
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) — FierceHealthcare, undated (retrieved 2026-07-18).
- [UnitedHealth Group responds to Department of Justice investigation](https://www.unitedhealthgroup.com/newsroom/2025/2025-07-24-uhg-responds-to-doj-investigation.html) — UnitedHealth Group newsroom, 2025-07-24 (confirms the DOJ probe is a long-standing, not fresh, legal risk; UNH is not an active candidate this cycle).
- Internal: `db/crypto_ai_desk.sqlite` `proposed_signals` row `sig_439295cfed1d5367` (TRUMP/USDT full field dump).
- Internal: `data/catalysts/2026-07-18/narrative_baskets.jsonl`, `catalyst_cycle_11-47.md`.
- Carried forward from the 15:48 EEST review (unchanged facts, not independently re-verified this run): [US-Iran military escalation rocks crypto markets](https://cryptobriefing.com/us-iran-strikes-bitcoin-crypto-market-reaction/) — CryptoBriefing; [Iran Strikes Push Bitcoin Below $63K: Fed Policy Now Matters More Than War](https://www.techtimes.com/articles/320296/20260713/iran-strikes-push-bitcoin-below-63k-fed-policy-now-matters-more-war.htm) — Tech Times, 2026-07-13; [Ondo Finance moves $63.9mln: Is a sell-off looming?](https://ambcrypto.com/ondo-finance-moves-63-9mln-is-a-sell-off-looming/) — AMBCrypto; [Analyst Flags $49.56M ONDO Transfer from Team Wallet as Potential Sell-Off](https://cryptonews.net/news/altcoins/33048535/) — CryptoNews.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, unchanged, informational)
- **issue:** Stocks intraday A/B guard combination continues to demote technically-qualified candidates via the market-closed gate. Fully expected/by-design on a Saturday.
- **evidence:** `data/reports/stocks/intraday/2026-07-17_21-56_stocks_intraday_report.md` — `market_closed_intraday_planning_only` caps applied to NVDA/AVGO/NFLX/COIN/UNH.
- **suggested manual fix:** none needed; by-design.
- **priority:** low.
- **first observed:** 2026-07-16 18:39 EEST; re-confirmed 2026-07-18 16:30 EEST.

### TODO-2 / TODO-10 (carried forward, unchanged — still high)
- **issue:** Crypto and stocks signals continue to show `expires_at` timestamps in the past while still displaying non-terminal statuses.
- **evidence:** NEAR/USDT (`tp1_hit`, expires 2026-07-17T15:56 UTC) and ONDO/USDT (`tp2_hit`, expires 2026-07-17T08:36 UTC) both still non-terminal as of this run.
- **suggested manual fix:** human check of the lifecycle/track-signals terminalization job for both asset classes.
- **priority:** high.
- **first observed:** 2026-07-16 16:20 EEST (stocks); 2026-07-17 16:29 EEST (crypto); re-confirmed 2026-07-18 16:30 EEST.

### TODO-3 (not reproducing across 2 consecutive runs now — keep watching)
- **issue:** `detect_untracked_legacy_alerts` had returned 2 unresolved results (ALLO/USDT, BANK/USDT) across 4+ consecutive reviews.
- **evidence:** clean (0 results) at both the 15:48 EEST and this 16:30 EEST run.
- **suggested manual fix:** none needed if it stays clean over several more cycles.
- **priority:** medium.
- **first observed:** 2026-07-16 18:39 EEST; not reproducing as of 2026-07-18 16:30 EEST (2nd consecutive clean run).

### TODO-6 (carried forward, unchanged)
- **issue:** Crypto scalp mode remains a consistent losing bucket.
- **evidence:** `signal-stats --asset-class crypto` this cycle: `mode=scalp | n=22 | trig=20 | wins=0 losses=7 | PF 0.1667 | totalR -5.0` (identical to the 15:48 review — same underlying week window).
- **suggested manual fix:** human review of whether scalp (and/or short-direction plays) should carry an explicit non-actionable label.
- **priority:** medium.
- **first observed:** 2026-07-17 11:45 EEST.

### TODO-7 (carried forward, unchanged — still high)
- **issue:** Stocks earnings-calendar lookup failing broadly (10 tracked tickers, 0 events tracked).
- **evidence:** `data/reports/stocks/intraday/2026-07-17_21-56_stocks_intraday_report.md` §0 — unchanged since the 15:48 review, no fresher stocks report exists (market closed, none expected until Monday).
- **suggested manual fix:** human audit of the earnings-calendar source/ingestion.
- **priority:** high.
- **first observed:** 2026-07-17 11:45 EEST (narrow scope); widened 2026-07-18 15:48 EEST.

### TODO-8 (carried forward, unchanged — still high, not independently re-checked this run)
- **issue:** `mexc_canary_monitor` crash-looping on `sqlite3.OperationalError: database is locked` inside `ensure_tables()`.
- **evidence:** last confirmed via `data/scheduled_runs/2026-07-18_default_schedule/mexc_canary_monitor_*.log` at the 15:48 EEST review; not re-pulled this run (out of scope for the allowed read set beyond what §A permits without a fresh log check).
- **suggested manual fix:** human investigation of lock contention on `db/crypto_ai_desk.sqlite` around `mexc_canary_control` writes.
- **priority:** high.
- **first observed:** 2026-07-17 11:45 EEST.

### TODO-9 (not reproducing across 2 consecutive runs now — keep watching)
- **issue:** `market_dashboard_snapshots.crypto_market_mode` had looked decoupled from the report-level regime classifier.
- **evidence:** clean/consistent (`transition` matching report-level) at both the 15:48 EEST and this 16:30 EEST run.
- **suggested manual fix:** none needed if it stays consistent.
- **priority:** low.
- **first observed:** 2026-07-17 11:45 EEST; not reproducing as of 2026-07-18 16:30 EEST (2nd consecutive clean run).

### TODO-11 (carried forward, partially improving — still high until confirmed over more cycles)
- **issue:** This task and/or its sibling tasks (`opus-enriched-review-preus`/`-postclose`) appeared to skip six consecutive scheduled dispatches between 2026-07-17 16:29 EEST and 2026-07-18 15:48 EEST, with no DEFERRED/BLOCKED marker for any of them.
- **evidence:** **Positive signal this run**: this review (the `opus-enriched-review-preus` sibling task, nominal 16:20 EEST slot) dispatched on-schedule at ~16:2x EEST, unlike the prior off-schedule 15:48 EEST run. One clean on-time dispatch is not sufficient to close this — watch the next 2-3 scheduled slots (18:30, 21:30, 23:15 today) to see if the pattern holds.
- **suggested manual fix:** human check of the outer scheduling mechanism; continue monitoring dispatch timestamps across upcoming slots before downgrading priority.
- **priority:** high (unchanged pending further confirmation).
- **first observed:** 2026-07-18 15:48 EEST; partial positive signal 2026-07-18 16:30 EEST.

### TODO-12 (carried forward, unchanged — medium)
- **issue:** `news_items.published_at` stores inconsistent datetime formats (mixed UTC offsets, `Z` suffix, literal `date_unavailable` rows), breaking naive lexicographic freshness filtering.
- **evidence:** confirmed again this run — the TRUMP/USDT freshness check (`published_at > datetime('now','-24 hours')`) was run defensively assuming this bug is still present; returned 0 rows cleanly (no TRUMP news exists either way, so this run was not itself blocked by it, but the underlying format inconsistency was not re-audited/fixed).
- **suggested manual fix:** human audit of the `published_at` normalization step in the news ingestion pipeline.
- **priority:** medium.
- **first observed:** 2026-07-18 15:48 EEST.
