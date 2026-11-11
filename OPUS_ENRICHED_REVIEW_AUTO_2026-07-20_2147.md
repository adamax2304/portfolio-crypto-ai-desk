# Opus Enriched Review — late-session risk review — Auto Cycle 21:30 EEST

## 1. Executive Summary

**Slot: late-session risk review** (nominal 21:30 EEST; dispatched ~21:40, ~10 min jitter). US cash session has ~70 minutes left (close 23:00 EEST). **Advisory only — no auto-trade, no scoring/threshold/strategy changes made or implied.**

**Crypto:** short-term (intraday, data ~2h old) regime reads bullish trend/risk-on (BTC/ETH uptrend, breadth 57.5%), while the higher-timeframe swing view (data ~4h10m old, carry-forward) still reads range/chop — a genuine **intraday-vs-swing divergence**, not a clean risk-on call. 20 active B-tier positions, all long except one stale short (NEAR). Zero A-tier and zero fresh C→B/A upgrades this cycle. The four biggest 24h gainers driving "where money is flowing" (HEMI +28%, PROM +53%, ACE +84%, BANK +47%, PUMP +20%) are **confirmed no-catalyst** — verified directly against `news_items` (0 rows in 24h for all five symbols) — and are explicitly flagged by the system's own `momentum_breakout` narrative basket as `avoid_chase`. Several of these (ACE, BANK, HEMI, PUMP) are also currently open B-tier longs, so this is a "manage, don't add to" situation, not a new-entry green light.

**Stocks:** internal regime label is **risk_off / short bias** again (VIX 17.89, breadth-above-EMA20 0.0%), producing a wide basket of C-tier short candidates (NVDA, AVGO, GOOGL, META, JPM, TSLA, SMH, XLK, QQQ, DIA, UNH, NFLX, SMCI...). **Externally verified this run: today was actually a mixed/flat session** — Dow -0.5%, S&P +0.1%, Nasdaq +0.3%, chips recovering ahead of this week's Big Tech earnings (GOOGL/TSLA/INTC/IBM) — which is the **second consecutive review cycle** where the internal risk_off/short-bias label has diverged from the day's actual tape. This is now a repeat pattern worth a TODO (§14). Zero A/B-tier stocks signals triggered in the last 24h (all 44 today's-window signals are C-tier watchlist, correctly non-actionable).

**Legal/headline risk:** UNH remains internally demoted B→C on an active `sec_doj` legal-risk cap — consistent with last cycle's externally-confirmed DOJ/Claritev antitrust probe. Treat as **AVOID**, not a clean short, regardless of its "triggered" DB status. NVDA and AVGO's own short setups have **self-invalidated** in the freshest scan (AVGO → `no_directional_setup`, score 38.4; NVDA demoted A→C on sector/liquidity/catalyst gates) — same finding as the 18:30 review, now unresolved two cycles running; do not treat their `active-signals` "triggered" rows as live.

**Data hygiene:** ALLO/USDT (crypto, expired 2026-07-19, ~30h past its own window) and NEAR/USDT-short (crypto, expired 2026-07-17, ~3.3 days past) are still displayed as active `tp1_hit` rows — the same staleness pattern flagged in the last two reviews, now unresolved across 3+ consecutive cycles. Catalyst mapping is **weak this run (72.2% unmapped, 728/2,621 mapped)** — use catalyst layer as directional context only, not as a final gate.

## 2. Data Used

- Reports: crypto scalp/intraday (`2026-07-20_16-44` / `2026-07-20_16-51`, data ~16:45 UTC = 19:45 EEST, ~2h old, fresh), crypto swing (`2026-07-20_14-30`, data 14:30 UTC = 17:30 EEST, ~4h10m old — carry-forward per freshness rule), stocks intraday (`2026-07-20_18-27`, data 18:24 UTC = 21:24 EEST, ~23 min old — freshest possible). Stocks swing/invest still `2026-07-02` (18 days stale) — excluded, planning-only, not referenced.
- Catalysts: `data/catalysts/2026-07-20/catalyst_events.jsonl` (2,621 cumulative events today), `narrative_baskets.jsonl` (5 baskets), latest `catalyst_cycle_16-53.md` (19:53 EEST).
- LLM packets: `llm_analysis_packet.md` (19:51 EEST, fresh), `llm_stocks_packet.md` (20:13 EEST, fresh).
- CLI: `active-signals` ×2 (crypto 20 rows, stocks 50 rows — many historical tail beyond today), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-20` (0 findings — clean, no untracked crypto alerts today).
- DB reads (read-only): `news_items` 24h symbol search for ACE/USDT, BANK/USDT, HEMI/USDT, PUMP/USDT, PROM/USDT (all 0 rows — confirmed genuinely uncovered, not a mapping gap); `proposed_signals` status counts by tier for last 24h, both asset classes (crypto: all B-tier, 7 triggered/4 waiting/7 closed-win/7 stopped/2 expired/1 moved-away; stocks: all C-tier, 20 triggered/1 waiting/3 closed-win/2 stopped/21 stale_before_entry).
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_1848.md` (US open reaction slot) — used for §4 comparison.
- External: 3 WebSearch queries (US stock market close today, BTC/ETH price today, ACE/BANK/HEMI crypto news check). No WebFetch needed — search snippets from CNBC/Yahoo Finance/Bloomberg-linked aggregation and Yahoo Finance crypto column were sufficient and internally consistent; no contradicting single source found. Sources ingested via `scripts.ingest_enriched_review_sources`.

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime ~20:18 EEST, ~1h29m old at review start — well under the 3h defer threshold. Not deferred.
- Latest completed cycle: `cycle_08_19-34_summary.md` (started 19:34 EEST, finished 20:18 EEST, 66/66 steps ok, 0 failed).
- Crypto scalp/intraday: ~2h old (normal ~3.3h cadence, not stale). Swing: ~4h10m old — carry-forward, flagged, still used for regime cross-check only (no fresh swing candidates cited).
- Stocks intraday: ~23 min old — freshest possible this cycle. Stocks swing/invest: 18 days stale, unused.
- Monitor/paper-portfolio live status not directly queried (outside the allowed read-only CLI set this run); no anomaly signal from `detect_untracked_legacy_alerts` (clean).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-20 21:47 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["monitor/paper-portfolio live status (outside allowed read-only CLI set)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~1h29m old", "stocks intraday report 23min old", "crypto scalp/intraday ~2h old", "crypto swing ~4h10m old (carry-forward)", "stocks swing/invest 18 days stale, unused"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["mixed", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto intraday: bullish uptrend, breadth 57.5%", "crypto swing (carry-forward): range/chop, breadth 48.7%", "stocks internal label: risk_off/short, breadth-above-EMA20 0%", "external: Dow -0.5%/S&P +0.1%/Nasdaq +0.3%, mixed/flat session ahead of Big Tech earnings", "BTC ~$64.7k/ETH ~$1,875, roughly flat vs weekend, mixed 2H26 sentiment"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["mapping_weak", "no_catalyst", "fresh_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 72.2% unmapped (728/2,621) this run", "momentum_breakout basket: ACE/BANK/HEMI/PUMP/PROM flagged avoid_chase, confirmed 0 news_items in 24h for all five", "perps_dex_narrative basket: HYPE primary, wait_pullback, fresh <6h", "rwa_narrative basket: ONDO/XLM primary, related_beta_rotation, fresh <6h", "UNH sec_doj catalyst confirmed and already gated"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.4,
      "reason_codes": ["data_unavailable", "oi_supports"],
      "data_missing": ["OI 24h% for HEMI/BANK/ACE/PROM (n/a)", "long/short ratios for most symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HEMI/BANK/ACE/PROM: funding near-zero, OI n/a, crowding normal/unknown", "PENGU: price up + OI up +1.98%, long/short 0.885, fresh positioning confirms trend"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HEMI/PROM/XPL tagged overextended + volume_expansion in intraday report", "ACE +84.4% 24h on 0.56x volume (thin participation for the size of the move)", "BANK/HEMI/ACE/PUMP already open B-tier longs — adding here would be chasing an existing position"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto 24h: 7 triggered, 4 waiting_for_entry, 7 closed-win (tp1/2/3), 7 stopped, 2 expired(entered-unresolved), 1 no-entry/moved-away — all B-tier", "stocks 24h: 20 triggered(review/shadow, C-tier), 1 waiting, 3 closed-win, 2 stopped, 21 stale_before_entry(no-entry) — zero A/B triggered", "ALLO/USDT and NEAR/USDT-short still shown active tp1_hit despite expires_at 30h and 3.3 days in the past respectively — needs_review, recurring across 3+ cycles"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: active sec_doj cap, demoted B->C, confirmed DOJ/Claritev probe last cycle", "NVDA/AVGO shorts self-invalidated by fresher scan (no_directional_setup / sector-liquidity-catalyst gates) but still shown triggered in active-signals", "TSLA/GOOGL earnings ~July 22 (2 trading days out), swing-blocked; intraday holds into that window carry gap risk", "geopolitical tail risk live: US-Iran tit-for-tat strikes over the weekend, oil touched $90/bbl before easing"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto direction=short: PF 0.25, avgR -0.43, n=10 — weak, avoid new crypto shorts absent an exceptional clean setup", "crypto tier=B triggered winrate 32% (n=126, reliable) — low; PF still 2.04 on winner size, not win rate", "stocks tier=C: PF 0.73, winrate 21% (n=193, reliable) — negative edge, watchlist-only by design", "stocks tier=A/B: n=7 only, anecdotal, not decision-grade"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "ONDO/USDT or XLM/USDT", "trigger": "rwa_narrative basket fresh <6h, related_beta_rotation — enter only on a pullback into structure with RS confirmation, not a fresh breakout chase", "reason": "institutional RWA/tokenization thesis (DTCC/Stellar-linked), catalyst-backed and not part of the no-catalyst momentum cluster" },
    "best_short_candidate": { "symbol": "SMH/XLK (stocks sector)", "trigger": "failed retest of today's session high with RVOL clearing the stocks-intraday confirmation gate", "reason": "genuinely weakest sector on 20d RS (-14.3%/-7.2% vs SPY) even though today's tape was flat-to-up; do not short the bounce itself" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "clean pullback into structure per perps_dex_narrative's own wait_pullback playbook, basket still <6h fresh", "reason": "carried forward unchanged from the 18:30 review — narrative still fresh, no new information this cycle" },
    "avoid_candidate": { "symbol": "UNH, NVDA-short, AVGO-short", "reason": "UNH: confirmed active DOJ/Claritev legal risk. NVDA/AVGO: self-invalidated by the system's own fresher re-scan; the DB's triggered/tier-C rows are stale, not live ideas" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.55 | mixed, chop | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, no_catalyst, fresh_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.40 | data_unavailable, oi_supports | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, entry_late | advisory_only |
| execution_lifecycle | caution | 0.75 | open_actionable, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_1848.md` (18:30, US open reaction):

- **Crypto regime upgraded** from "range/chop, neutral" (18:30, based on then-current intraday) to "bullish trend, risk-on" in the new intraday report, while swing is still range/chop (carry-forward) — a divergence, not a clean flip. Treat with the same caution as before.
- **BANK/USDT thesis progressed**: was "long-watch, do not chase" at 18:30 (48% 24h move) — now already **triggered** on both intraday and swing B-tier signals, and the move has continued to +47% (roughly unchanged in magnitude, still no catalyst). Same "manage, don't add" caution applies, now with live exposure.
- **NVDA/AVGO self-invalidation persists**, now visible in a second consecutive fresh scan (AVGO explicitly `no_directional_setup` 38.4 this cycle vs. demoted-but-still-scored last cycle). **Escalating** — see §14 TODO.
- **UNH legal risk unchanged** — still correctly gated, no new developments this cycle.
- **ALLO/NEAR staleness unchanged and unresolved** — flagged at 18:30, still present verbatim this cycle (same expiry timestamps, same tp1_hit display).
- **Catalyst mapping essentially unchanged**: 71.0% unmapped at 18:30 vs 72.2% now — still weak, not materially improved or worsened.
- **New this cycle**: `rwa_narrative` (ONDO/XLM) and confirmed-clean `news_items` check on the momentum-cluster symbols (ACE/BANK/HEMI/PUMP/PROM all verified 0 news in 24h, satisfying the no-catalyst claim with direct evidence rather than inference).
- **Stocks risk_off/short-bias label vs. actual flat/mixed tape** is now a **second consecutive** divergence (18:30 review found the same pattern with chip-stock strength; today's tape was milder — Dow -0.5%/S&P +0.1%/Nasdaq +0.3% — but still not the clean risk_off the internal label implies).

## 5. Catalyst Coverage

- Total `catalyst_events` today: **2,621**
- Mapped (non-null symbol): **728** (27.8%)
- Unmapped (null symbol): **1,893** (72.2%)
- `narrative_baskets`: **5** (delisting_thin_liquidity, ai_narrative, perps_dex_narrative, rwa_narrative, momentum_breakout)

**Catalyst mapping weak this run — use the catalyst layer as context, not final decision.**

Top 3 unmapped headlines (sample):
- "Tradfin: *SEOUL STOCK MARKET'S KOSPI FALLS 4%..." (macro/index headline, no single-symbol mapping expected)
- "FSTA vs. XLP: How These Popular Consumer Staples ETFs Compare for Investors" (comparison piece, ambiguous primary symbol)
- "CoreWeave vs. Applied Digital: Evaluating Disparities in Revenue Scale..." (comparison piece, two tickers, resolver picks neither)

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed** — intraday timeframe reads risk-on/uptrend (breadth 57.5%), swing/higher-timeframe carry-forward reads range/chop (breadth 48.7%); external BTC/ETH price action today is roughly flat ($64.7k / $1,875, "mixed" 2H26 sentiment per Yahoo Finance). Treat as a short-term bullish tilt inside a broader range, not a confirmed trend change.
- Stocks mood: **mixed** (internal label risk_off/short-bias, breadth-above-EMA20 0%; external actual tape flat-to-slightly-up, Dow -0.5%/S&P +0.1%/Nasdaq +0.3%, chips recovering into this week's Big Tech earnings). Do not take the internal short-bias label as license to chase shorts into a flat/up tape.
- Dominant narrative: no-catalyst momentum cluster (ACE/BANK/HEMI/PUMP/PROM, avoid_chase) dominating crypto "where money is flowing"; semis/tech relative weakness (SMH -14.3%, XLK -7.2% RS vs SPY) still the cleanest multi-day thesis on the stocks side, energy/healthcare/financials the strongest sectors.
- Preferred side now: **wait-for-trigger / catalyst-backed** — neither book has a clean, fresh, un-chased setup this window.
- Best long candidate: ONDO/USDT or XLM/USDT (rwa_narrative, related_beta_rotation) — only on a pullback, not a chase of the fresh basket.
- Best short candidate: SMH/XLK (stocks) — only after a failed retest of today's bounce high with RVOL confirmation; do not short a flat/up tape on the internal label alone.
- Best catalyst-backed candidate: HYPE/USDT (perps_dex_narrative, wait_pullback), carried forward unchanged.
- What to avoid: UNH (legal risk), NVDA/AVGO shorts (self-invalidated, stale DB rows), chasing ACE/BANK/HEMI/PUMP/PROM at current extension.
- What would change the view: a confirmed catalyst hitting the momentum cluster (would flip avoid_chase to catalyst-backed); a clean multi-timeframe crypto trend alignment (intraday + swing both uptrend); stocks breadth-above-EMA20 recovering off 0%; UNH DOJ resolution or escalation.

## 7. Candidate Deep Dives

**1. BANK/USDT (crypto, B-tier, intraday triggered score 72.0 + swing triggered score 67.4) — MANAGE, do not add**
- Price has already reacted to its own momentum (no external catalyst found; confirmed 0 `news_items` in 24h). This is chasing if treated as a new entry — the move is the same one flagged at 18:30, now 3+ hours further extended.
- No retest/pullback structure visible in the report; funding near-zero, OI n/a, crowding "normal" (derivatives data thin).
- Aligned with market mood only in the loose sense that crypto intraday reads risk-on; not aligned with the "avoid_chase" narrative-basket verdict for this exact symbol.
- Actionable now only as an existing-position management question (trail toward invalidation 0.2399–0.2679 depending on mode), not as a new entry.
- Invalidator: close back below entry_low on either timeframe, or a break of the intraday invalidation 0.2399.
- Chase-risk: **yes**, for any new entry.

**2. ACE/USDT (crypto, B-tier, intraday triggered 68.6 + swing triggered 74.9) — MANAGE, do not add**
- +84.4% 24h on only 0.56x volume — a thin-volume blow-off move, not confirmed by proportional participation. Confirmed 0 `news_items` in 24h.
- Overextended by any reasonable ATR/EMA measure implied by the scale of the move (report doesn't give exact ATR-multiple here, but the 24h% alone flags it).
- Not aligned with current mood beyond generic risk-on; explicitly named in the `momentum_breakout`/`avoid_chase` basket.
- A fresh entry now would be very late. Existing position: manage toward its own invalidation (0.1015 intraday / 0.1103 swing).

**3. HYPE/USDT (crypto, catalyst-watch, not yet in active-signals) — WAIT FOR PULLBACK**
- `perps_dex_narrative` basket (HYPE primary; DYDX/GMX/ASTER related), playbook explicitly `wait_pullback`, fresh <6h.
- No open position yet; this is a watch-only idea, not a live signal.
- Catalyst confirmation: yes (Hyperliquid prediction-market expansion headlines, multiple independent outlets per the catalyst cycle file).
- Actionable only after a clean pullback into structure — chasing the current level would violate the basket's own playbook.
- What would invalidate: basket goes stale (>24h) without a pullback occurring, or HYPE breaks down through recent structure instead of pulling back.

**4. UNH (stocks, tier C, short, triggered 75.5) — AVOID**
- Legal/headline risk: **active DOJ/Claritev antitrust investigation**, externally confirmed last cycle (multiple independent outlets: Simply Wall St, PYMNTS, Medical Economics). System itself already caps this signal (`sec_doj`, demoted B→C).
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED** — never a clean actionable, per the legal-risk rule regardless of technical score.
- No change from last cycle; carried forward.

**5. NVDA / AVGO shorts (stocks, tier C) — AVOID, treat DB rows as stale**
- AVGO: fresh scan this cycle explicitly returns `no_directional_setup` (score 38.4) — the setup the DB still shows as "triggered" (score 90.7, tier C) no longer exists in the system's own latest read.
- NVDA: demoted A→C this cycle on `sector_confirmation_weak_or_unknown`, `liquidity_rvol_below_min`, `catalyst_none_and_not_exceptional_technical` gates — same self-invalidation pattern as AVGO, second consecutive cycle.
- Price action context: chip stocks were recovering into this week's Big Tech earnings per external search — directionally inconsistent with a fresh short thesis on either name today.
- Not actionable; do not treat the `active-signals` CLI rows for these two as live ideas.

## 8. Best Candidates Ranked

1. **Catalyst-watch: HYPE/USDT** — trigger: clean pullback into structure while `perps_dex_narrative` stays fresh (<24h); playbook says wait, not chase. Unchanged from 18:30 review.
2. **Long-watch: ONDO/USDT or XLM/USDT** — trigger: pullback into structure with RS confirmation, per `rwa_narrative`'s `related_beta_rotation` playbook; do not chase a fresh breakout in this basket.
3. **Short-watch: SMH/XLK (stocks)** — trigger: failed retest of today's session high with RVOL clearing the stocks-intraday gate; sector RS is genuinely weak (-14.3%/-7.2%) even though today's tape itself was flat-to-up — don't short the bounce, wait for the rejection.
4. No new clean actionable entry on either book this window beyond managing the 20 existing crypto B-tier positions — both books are gated by their own confirmation rules, functioning as designed given a mixed/chase-risk tape.

## 9. Avoid / No Trade

This window only — never a command to stop the system:

- **UNH** — confirmed, active DOJ/Claritev antitrust probe. Avoid until resolved.
- **NVDA / AVGO shorts** — self-invalidated by the system's own fresher re-scan, second consecutive cycle; do not treat `active-signals`' triggered/tier-C rows as live.
- **ACE/BANK/HEMI/PUMP/PROM** — confirmed no-catalyst momentum cluster (`avoid_chase`), thin-volume moves on ACE/PUMP specifically; manage existing positions, do not add or chase fresh entries.
- **TSLA/GOOGL** — earnings ~July 22 (2 trading days out); avoid initiating or holding new intraday positions through that window regardless of technical score.
- **NEAR/USDT short** — stale 3.3 days past expiry, weak historical crypto-short performance (PF 0.25, n=10); needs manual review, not a fresh entry.
- Scanning, candidate generation, tracking, and the scheduler continue uninterrupted — none of the above is a stop-the-system finding.

## 10. Main Risks

- **Recurring signal-lifecycle staleness** (ALLO/NEAR past-expiry-but-still-shown-active) is now unresolved across 3+ consecutive review cycles — see §14 TODO, escalated to high.
- **NVDA/AVGO self-invalidation persisting** two cycles running without the DB reflecting the newer, contradicting scan — operator risk if the active-signals table is read without cross-checking the freshest report.
- **Stocks internal risk_off/short-bias label diverging from actual tape** for a second consecutive cycle — reduces confidence in using the stocks regime label alone to route decisions this week.
- **Catalyst mapping stuck around 71-72% unmapped** across the last two cycles — catalyst-backed framing should stay secondary to technical/lifecycle signals until this improves.
- **Crypto direction=short historically weak** (PF 0.25, n=10) — avoid new crypto shorts absent an exceptional, clean, catalyst-confirmed setup.
- **Live geopolitical tail risk**: US-Iran tit-for-tat strikes continued over the weekend, oil touched $90/bbl before easing — a risk factor internal technical labels don't price in directly.
- **Earnings-week overhang**: GOOGL/TSLA (and market-wide INTC/IBM) report this week — elevated gap risk for any position held through those prints.

## 11. Action Plan — next 4 hours

- Manage existing crypto B-tier positions (ACE, BANK, HEMI, PUMP, ZAMA, SUI, XRP, PENGU, XPL, SYN, KAITO, LTC) toward their own invalidation/TP levels; do not add to the no-catalyst momentum names (ACE/BANK/HEMI/PUMP/PROM).
- Watch HYPE/USDT and ONDO/XLM for pullback confirmation per their own basket playbooks; no forced entries into the close.
- Do not initiate new stocks intraday shorts off the internal risk_off label alone — require an RTH failed-retest + RVOL confirmation, especially into a week with GOOGL/TSLA earnings ahead.
- Manually confirm the true status of ALLO/USDT and NEAR/USDT-short — both display as active well past their own expiry; this has now repeated across three review cycles.
- Continue treating NVDA/AVGO short ideas as invalid regardless of `active-signals` display, given two consecutive fresh-scan self-invalidations.
- No new stocks swing/invest scan (18 days stale) — do not reference stocks swing/invest data for decisions this window.

## 12. Final Verdict per Mode

- **Crypto scalp/intraday/swing:** no new trade this window; manage the 20 existing B-tier longs, avoid adding to the no-catalyst momentum cluster, avoid new crypto shorts given weak historical short performance.
- **Stocks intraday:** no A/B actionable (0 in the last 24h); 44 C-tier watchlist names correctly gated. Treat NVDA/AVGO as stale/invalid, UNH as legally avoid, and the broader short basket as unconfirmed given today's actual flat/mixed tape.
- **Stocks swing/invest:** no fresh data (18 days stale) — do not use for decisions this window.
- **Overall:** watch-only / wait-for-trigger across both books, into a thin remaining ~70-minute RTH window. Advisory only, no auto-trade.

## 13. Sources

- [Stock market today: Dow, S&P 500, Nasdaq mixed as chip stocks rise in wait for Big Tech earnings — Yahoo Finance](https://finance.yahoo.com/markets/live/stock-market-today-monday-july-20-dow-sp-500-nasdaq-111429441.html) (2026-07-20)
- [Bitcoin and ethereum prices today, Monday, July 20, 2026: Crypto prices mixed as second half 2026 outlooks conflict — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-july-20-2026-crypto-prices-mixed-as-second-half-2026-outlooks-conflict-151956982.html) (2026-07-20)
- Internal: `data/reports/intraday/2026-07-20_16-51_intraday_report.md`, `data/reports/swing/2026-07-20_14-30_swing_report.md`, `data/reports/stocks/intraday/2026-07-20_18-27_stocks_intraday_report.md`, `data/catalysts/2026-07-20/catalyst_cycle_16-53.md`, `proposed_signals` / `news_items` DB tables (read-only).
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_1848.md` (used for §4 comparison).

## 14. Fix Requests / TODO

### TODO-signal-staleness-display
- **issue:** ALLO/USDT (crypto, expired 2026-07-19T15:21) and NEAR/USDT-short (crypto, expired 2026-07-17T15:56) are still returned by `active-signals` as live `tp1_hit` rows, well past their own `expires_at`. Same pair flagged in the 18:30 and prior reviews — unresolved across 3+ consecutive cycles.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` output this run, rows `sig_10088a4c71cae845` (ALLO) and `sig_b16bb9e54598333a` (NEAR); prior review text at `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_2153.md` and `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_1848.md` flagging the identical pair.
- **suggested manual fix:** investigate whether `active-signals` should filter or clearly label rows past `expires_at`, and whether this is the same root cause as the previously-confirmed watchlist-alert/signal-reuse bug on ALLO/BANK (per prior session notes) — worth a joint root-cause session.
- **priority:** high
- **first observed:** 2026-07-19 21:53 EEST (this is the 3rd consecutive automated review to observe it unresolved)

### TODO-nvda-avgo-self-invalidation-lag
- **issue:** NVDA and AVGO short setups have self-invalidated in the freshest scan two cycles running (AVGO → `no_directional_setup` score 38.4 this cycle; NVDA demoted A→C on sector/liquidity/catalyst gates), but `active-signals` still returns both as `triggered`/tier-C rows with no indication the underlying setup no longer exists per the system's own latest read.
- **evidence:** `data/reports/stocks/intraday/2026-07-20_18-27_stocks_intraday_report.md` line 192 (`AVGO (no_trade): 38.39 — no_directional_setup`) and line 171 (NVDA demotion note) vs. `active-signals --asset-class stocks` rows `sig_48899bb488411af9` (AVGO) and `sig_e0fceb60a6327886` (NVDA) still shown triggered.
- **suggested manual fix:** consider whether `active-signals` should cross-check the latest report's per-symbol verdict and annotate/suppress rows the newest scan has already contradicted, to reduce operator misread risk.
- **priority:** medium
- **first observed:** 2026-07-20 18:48 EEST (2nd consecutive cycle)

### TODO-stocks-regime-label-divergence
- **issue:** The internal stocks regime classifier has labeled `risk_off / short bias` for two consecutive review cycles (18:30 and 21:30) while the actual session tape both times was flat-to-slightly-up (18:30: chip-led rebound, +0.6%/+1.3%/+3.1% SPX/NDX/SOX; 21:30: Dow -0.5%/S&P +0.1%/Nasdaq +0.3%). Breadth-above-EMA20 reads 0.0% both times, which may be driving the label independent of actual index returns.
- **evidence:** `data/reports/stocks/intraday/2026-07-20_18-27_stocks_intraday_report.md` §1 (`Label: risk_off`, `Breadth above EMA20: 0.0%`) vs. external search confirming a mixed/flat close; same pattern noted in `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_1848.md` §1.
- **suggested manual fix:** a human review session should check whether the breadth-above-EMA20 input feeding the regime label is stale, miscalculated, or simply a legitimately noisy signal this week (large day-to-day swings without net breadth improvement) — worth sanity-checking against 2-3 more cycles before treating it as a bug.
- **priority:** medium
- **first observed:** 2026-07-20 18:48 EEST (2nd consecutive cycle)
