# Opus Enriched Review — late-session risk review — Auto Cycle 21:39 EEST

## 1. Executive Summary

Slot: **late-session risk review** (late US session, risk/exposure check), run **2026-07-16, 21:39 EEST** (~18:39 UTC / ~14:39 ET, ~1h20m before the 20:00 UTC / 16:00 ET US cash close). **Advisory only — no auto-trade, no code/scoring/routing changes.** Data pipeline is healthy: cycle 6 (19:31–20:03 EEST) completed **58/59 steps** with **one non-fatal failure** (`paper entry-mode classify`, exit=1 — see TODO-4); crypto scalp/intraday fresh (~2h old), crypto swing carry-forward (~4h12m, borderline), stocks intraday very fresh (~2min old at review start). **Crypto stays B-tier-only and 100% long-biased today** (19 signals, zero A-tier, zero shorts fired): 4 wins (VIRTUAL/USDT ×2, OPN/USDT ×2, all tp3_hit), 9 stopped, with **ONDO/USDT swing freshly triggered** (catalyst-confirmed — SBI tokenization deal + MEXC tokenized-stock listing, real 17% surge news) and **BANK/USDT swing waiting_for_entry** (explicitly flagged by the desk's own momentum-cluster basket as "**without confirmed catalyst**" — verified directly against `news_items`, zero hits in 24h). **Stocks stay 100% C-tier for the entire session** (35 signals, zero A/B) — root cause identified directly in the report's own tier-demotion log: the `stocks_intraday_7d_drawdown_guard` + `stocks_intraday_long_guard` combination demoted every B-scored name (AVGO, XOM, AMD, XLE, PLTR, AAPL, QQQ) to C-tier/non-actionable, and **TSLA short was separately gated for an active `going_concern` legal/headline flag** — both are the system working as designed, not a fault (carried-forward TODO-1 asks a human to confirm the drawdown-guard threshold is well-calibrated, not over-tight). **UNH stays AVOID/MANUAL REVIEW, now reinforced by outcome**: the DOJ-probe caution from the 18:39 review held, and today's UNH intraday long (score 66.06) **got stopped out**. **Three new stocks C-tier shorts fired in the last hour** (COIN, SPY, DIA, all `waiting_for_entry`, 18:15–18:36 UTC) — a late-session risk-off tilt consistent with QQQ's -2.34%/5d downtrend and weak semis/tech sector RS, though SPY/DIA shorts run counter to their own 20d uptrend label (mean-reversion/pullback plays, not trend continuation — treat as lower-confidence). Crypto Fear & Greed reads **25 (extreme fear)** despite BTC/ETH both in uptrend per the intraday report — a sentiment/price divergence worth flagging as ambient risk. Catalyst mapping stays weak (**19.6% mapped / 80.4% unmapped**, 3000 events today) — consistent with the known ~17-20% baseline, context only. **ALLO/USDT's untracked legacy alert is now unresolved for a 3rd consecutive review cycle** (first seen 18:39, still present 21:39) — a genuine system-integrity anomaly (see TODO-3). Scanning, tracking, and all 4 monitors continue unaffected — **no recommendation to pause anything.**

## 2. Data Used

- Reports: `2026-07-16_16-39_scalp_report.md` (crypto scalp, ~1h ago); `2026-07-16_16-44_intraday_report.md` (crypto intraday, ~1h ago, regime range/chop); `2026-07-16_14-27_swing_report.md` (crypto swing, ~4h12m old, carry-forward band); `2026-07-16_18-37_stocks_intraday_report.md` (stocks, ~2min old at review start, regular session).
- Catalyst: `data/catalysts/2026-07-16/catalyst_cycle_16-47.md`, `catalyst_events.jsonl` (3000 rows today), `narrative_baskets.jsonl` (6 baskets).
- LLM packets: `data/processed/llm_analysis_packet.md` (19:45), `data/processed/llm_stocks_packet.md` (19:58).
- DB (direct SQL, `db/crypto_ai_desk.sqlite`): `proposed_signals`, `news_items`, `watchlist_alerts`, `market_dashboard_snapshots`.
- CLI: `active-signals` ×2, `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-16`.
- Scheduler: `data/scheduled_runs/2026-07-16_default_schedule/scheduler.log`, `cycle_06_19-31_summary.md`.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-16_1839.md` (used for TODO carry-forward and the already-sourced UNH DOJ-probe citations — internal record reused per source-discipline rules since it is <3h old and uncontradicted by fresher `news_items`).

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime **20:03 EEST**, latest `cycle_06_19-31_summary.md` mtime **20:03 EEST** — both ~1h36m old at review start. **Not deferred** (well under the 3h threshold).
- Cycle 6: **58/59 steps ok, 1 non-fatal failure** (`paper entry-mode classify`, exit=1, 19:49:13 EEST — cycle continued). See TODO-4.
- Crypto scalp/intraday: fresh (~1h/1h ago). Crypto swing: ~4h12m old — **carry-forward band** (4–12h), used with that caveat.
- Stocks intraday: ~2min old — very fresh. Stocks swing/invest: last generated **2026-07-02** (14 days stale) — this is the known, intentionally-deprecated legacy framework (superseded by the shadow-only `stocks_position_candidates` framework), not a freshness fault.
- Monitors: crypto/pending/derivatives/stocks monitors were all restarted this cycle after stale-PID detection (`20:00:27–20:00:34`) — normal scheduler behavior, all 4 now running (lifetimes 90–180min at cycle end, healthy).
- Catalyst directory present for today, no CLI catalyst-scan needed.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-16 21:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle6 ended 20:03 EEST, 58/59 ok", "crypto swing ~4h12m carry-forward", "stocks intraday ~2min fresh", "stocks swing/invest deprecated framework, 14d stale by design"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH uptrend but regime label range/chop, altcoin breadth 50%/45%", "Fear&Greed 25 (extreme fear) vs price uptrend divergence", "stocks: regime=transition, bias neutral, risk-on False, VIX 16.42, SPY/DIA up vs QQQ down -2.34%/5d"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["fresh_catalyst", "no_catalyst", "mapping_weak", "narrative_supported", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 587/3000 = 19.6% mapped, 80.4% unmapped today", "RWA basket (ONDO+XLM) explicitly catalyst-confirmed via SBI/Tradable-Stellar deals", "momentum_breakout basket explicitly flags BANK/USDT and MANTRA/USDT as without confirmed catalyst"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "ok",
      "confidence": 0.5,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["OI 24h for BANK/USDT (fallback_via_mexc, n/a%)", "OI for most non-BTC/ETH symbols"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONDO/USDT: price up + OI up, funding 5.4e-06 (low, not extreme), long/short 1.376, crowding normal — fresh positioning not a squeeze", "BANK/USDT: funding 0.00017 (mildly elevated, not extreme), OI unavailable"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["entry_fresh", "chase_risk", "clean_retest", "price_moved_away"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ONDO/USDT swing just triggered 15:46 UTC, entry zone 0.3781-0.3821 — fresh, not yet extended", "BANK/USDT still waiting_for_entry at 14:27 UTC pullback zone 0.0561-0.0574, momentum score 91.6 but no catalyst = chase risk if it gaps through zone", "SPY/DIA new shorts (18:15/18:36 UTC) counter to their own 20d uptrend label — needs confirmation, not trend-following"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "closed_flat", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto today: open_actionable=3 (1 triggered + 2 tp2_hit running), waiting=1, closed_win(tp3_hit)=4, closed_loss(stopped)=9, no_entry=2", "stocks today: review/shadow(C-tier triggered+partial)=13, waiting(C-shadow)=3, closed_loss(stopped)=13, no_entry/stale=8, needs_review(ambiguous)=1"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: widened DOJ antitrust probe into Claritev unit (insurer collusion) — AVOID/MANUAL REVIEW carried forward, confirmed today by a stopped-out UNH long", "TSLA short internally gated for active going_concern legal/headline flag — correctly suppressed by the system", "stocks_intraday_7d_drawdown_guard + long_guard suppressing 100% of A/B-scored stock names system-wide today"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "bad",
      "confidence": 0.7,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto A/B weekly: n=161, winrate 22.3%, PF 1.81, avgR 0.24, totalR +29.2 — profitable via R:R asymmetry despite low winrate", "stocks A/B weekly: n=14 (weak confidence), winrate 28.6%, PF 0.67, avgR -0.125, totalR -1.0 — losing; C-tier watchlist PF 0.62, totalR -14.5 — supports the drawdown guard being reasonably calibrated, not obviously over-tight"]
    },
    {
      "agent": "head_trader",
      "verdict": "watch_only",
      "confidence": 0.65,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 agents"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "ONDO/USDT", "trigger": "already triggered (swing B), entry 0.3781-0.3821 filled zone — manage toward tp1 0.3929/tp2 0.4019/tp3 0.4109, stop 0.3731", "reason": "catalyst-confirmed (SBI tokenization deal + MEXC tokenized-stock listing, 17% surge news within 11h), OI+price both up = fresh positioning not a squeeze, RS +18% vs BTC" },
    "best_short_candidate":    { "symbol": "XLK", "trigger": "already triggered (stocks C-tier/shadow, not Telegram-actionable), entry 178.09, stop 179.90, tp1 175.38 — paper-track only given drawdown-guard demotion", "reason": "tech sector weakest RS vs SPY (-4.98% 20d), QQQ in confirmed downtrend, clean technical alignment with sector rotation" },
    "best_catalyst_candidate": { "symbol": "XLM/USDT", "trigger": "already running (swing B, tp2_hit) — for late entrants, wait for pullback toward 0.1876-0.1876 zone or a clean higher-high above tp2 (0.1927) on volume", "reason": "RWA/tokenization narrative basket co-primary with ONDO; Tradable's $1B Stellar deal adds institutional-tokenization support" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "widened DOJ antitrust probe (Claritev unit, insurer collusion) stacked on existing Medicare-billing probe; today's UNH intraday long (score 66.06) was stopped out, confirming the caution was warranted — AVOID / MANUAL REVIEW" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.60 | mixed, chop, longs_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | fresh_catalyst, no_catalyst, mapping_weak, narrative_supported, catalyst_confirmed | advisory_only |
| derivatives_squeeze | ok | 0.50 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_fresh, chase_risk, clean_retest, price_moved_away | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry, review_shadow, closed_flat, needs_review | advisory_only |
| risk_manager | caution | 0.75 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | bad | 0.70 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | watch_only | 0.65 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (18:39 EEST)

- **New**: 3 stocks C-tier shorts fired since 18:39 — COIN (18:36 UTC), SPY (18:15 UTC), DIA (18:36 UTC), all `waiting_for_entry`. ONDO/USDT swing long re-triggered fresh (15:46 UTC entry). PLTR long triggered (14:40 UTC, C-tier/drawdown-guard-demoted from B, score 77.59).
- **Confirmed**: UNH AVOID/MANUAL REVIEW thesis — today's UNH intraday long (score 66.06) got **stopped**, directly validating the DOJ-probe caution flagged at 18:39. Semiconductor/tech weakness thesis continues (QQQ -2.34%/5d, semis/tech remain weakest sectors).
- **Progressed**: ONDO/USDT (intraday) and XLM/USDT (swing) both advanced from tp2_hit (unchanged since 18:39) — still running toward tp3, no new resolution since last review. 4 crypto signals resolved to tp3_hit wins today (VIRTUAL ×2, OPN ×2) — all created before 05:00 UTC, resolved sometime in the last several hours.
- **Unresolved / carried forward**: ALLO/USDT untracked legacy alert — **still present, 3rd consecutive review** (18:39 → 21:39, same alert from 14:27 UTC, same root cause: signal_id reused from an older 02:27 alert instead of minting a fresh `proposed_signal`). Catalyst mapping stays weak (19.9%→19.6% mapped, materially unchanged). `stocks_intraday_7d_drawdown_guard` still suppressing 100% of A/B stock names, now spanning the full session (13:33 UTC through 18:37 UTC, 8+ hours).
- **New issue**: `paper entry-mode classify` step failed (exit=1) in cycle 6 — first occurrence noted this run.

## 5. Catalyst Coverage

- Catalyst events today: **3000** scanned, **587 mapped (19.6%)**, **2413 unmapped (80.4%)**. Narrative baskets: **6**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (Consistent with the known ~17-20% baseline documented in prior news-layer hardening work — not a new regression, but still flagged per protocol.)
- Top 3 unmapped headlines: "117,600,000 $USDT transferred from Bitfinex to Tether Treasury"; "Perp DEX Ostium pauses trading after oracle exploit drains $18M from its liquidity vault"; "103,711,520 $USDC transferred from Kraken to unknown wallet".
- Mapped/basket-confirmed narratives in play: RWA/tokenization (ONDO+XLM, primary), AI rotation (NEAR/RENDER/TAO/FET), perps-DEX (HYPE+DYDX/GMX/ASTER), Binance ecosystem teaser (BNB/ASTER), momentum cluster explicitly separating catalyst-backed (ONDO) from no-catalyst (BANK, MANTRA).

## 6. Market Landscape

### Crypto
- Regime: **range/chop (neutral)** per intraday report; BTC trend **uptrend**, ETH trend **uptrend**; altcoin breadth above EMA20 **50.0%**, above EMA50 **45.2%** (mixed/neutral breadth despite BTC/ETH strength — narrow leadership). Volatility normal (ATR percentile 51).
- Fear & Greed: **25 (extreme fear)** as of 19:51 EEST — notable divergence from the BTC/ETH uptrend read; treat as a sentiment headwind, not a reason to flip bearish on its own.
- Strongest: ONDO/USDT (score 91.6, +17% 24h, catalyst-confirmed), BANK/USDT (score 91.6, +18.2% 24h, no catalyst), MANTRA/USDT (score 88.3, +19.2%, no catalyst, volume 2.28x — flagged overextended). Weakest: DODO/USDT (-21.8% 24h), HOME/USDT (-21.4% 24h) — both bias-short in the report, no active signal, no fresh news either direction.

### Stocks
- Regime: **transition**, bias neutral, risk-on **False**, VIX **16.42** (low-normal), breadth 75% above EMA20/50 (healthy breadth despite neutral label). SPY uptrend (+0.03%/20d), DIA uptrend (+0.55%/20d), QQQ **downtrend** (-3.22%/20d), IWM range.
- Strongest sectors: healthcare (XLV, RS +5.81%), financials (XLF, +3.99%), energy (XLE, +3.23%). Weakest: semiconductors (SMH, -8.00%), technology (XLK, -4.98%), materials (XLB, -4.01%).
- Earnings today: NFLX, UNH (both swing-blocked). NFLX reported after the bell — "slid in Q2 despite strong results" per Yahoo Finance, no proposed_signal fired on it today.

### Market Mood / Risk Routing

- Crypto mood: **mixed** (price uptrend + range/chop regime label + extreme-fear sentiment — internally divergent; not a clean risk-on read)
- Stocks mood: **mixed** (neutral/transition regime, healthy breadth, but sector rotation out of tech/semis into healthcare/financials/energy, and a genuine risk guard suppressing all A/B actionability)
- Dominant narrative: RWA/tokenization (ONDO/XLM, catalyst-confirmed) in crypto; healthcare-vs-tech sector rotation in stocks
- Preferred side now: **longs (crypto, catalyst-backed only)** / **wait-for-trigger (stocks, drawdown-guard-suppressed)**
- Best long candidate: **ONDO/USDT** (already triggered, catalyst-confirmed)
- Best short candidate: **XLK** (stocks C-tier/shadow only — no A/B short is currently actionable; crypto has no active short signal, DODO/HOME are watch-only weak names)
- Best catalyst-backed candidate: **XLM/USDT** (RWA basket, running)
- What to avoid: **UNH** (legal/DOJ risk, confirmed by today's stop-out); **BANK/USDT** as a chase (no catalyst, momentum-only)
- What would change the view: fresh news_items hit on BANK/USDT confirming a real catalyst; a human recalibration decision on the drawdown guard (TODO-1); resolution of the DOJ probe (positive or negative) for UNH

## 7. Candidate Deep Dives

### 1. ONDO/USDT — long, swing, B-tier, **triggered** (catalyst-confirmed)
- Entry filled zone 0.37805-0.38210, stop 0.37311, tp1/tp2/tp3 0.39289/0.40189/0.41088. Created 15:46 UTC, expires 2026-07-23.
- Has price already reacted to the catalyst? Partially — +17% 24h already priced in, but SBI deal (10:59 UTC) and MEXC listing (08:31 UTC) news continued flowing through the day, suggesting the move has legs rather than being a single spike.
- Chasing? No — this is a fresh trigger at the desk's own defined entry zone, not a late add.
- Retest/pullback structure? Entry zone (0.378-0.382) is itself a pullback from the intraday high; RS vs BTC +18%.
- Overextended (>2 ATR from EMA20)? Not flagged by the report; momentum score 91.6 reflects strength, not exhaustion.
- Would entry now be late? No for the existing trigger; a fresh chaser above 0.382 would be late — wait for the next pullback.
- Actionable level: already actionable (triggered).
- Aligned with market mood? Yes — one of the only genuinely catalyst-confirmed longs in a mixed/chop tape.
- Long/short/wait: long, active.
- Invalidation: close below 0.3731 (stop).
- Chase risk: low for the current entry; moderate for late adds above tp1.
- Catalyst confirmation: **confirmed** — SBI tokenization deal, MEXC tokenized-stock trading pairs, RWA narrative basket primary.

### 2. BANK/USDT — long, swing, B-tier, **waiting_for_entry** (no catalyst — contradiction risk)
- Entry zone 0.05614-0.05736, stop 0.05464, tp1/2/3 0.06061/0.06333/0.06604. Created 14:27 UTC, still waiting 7+ hours later.
- Has price already reacted? Yes, +18.2% 24h — the momentum has already largely happened.
- Chasing? Elevated risk — momentum score 91.6 but **zero `news_items` hits in 24h** (directly verified, not assumed), and the desk's own `momentum_breakout` narrative basket explicitly labels this "**without confirmed catalyst**" alongside MANTRA/USDT.
- Retest/pullback structure? Yes, waiting at a defined pullback zone.
- Overextended? Funding is mildly elevated (0.00017) but not extreme; OI data unavailable (fallback via MEXC).
- Would entry now be late? If it fills at the stated zone, no — but this is a pure momentum/RS play with no fundamental backstop.
- Actionable level: fill of 0.0561-0.0574.
- Aligned with market mood? Marginal — fits a long-biased tape but lacks the catalyst confirmation that makes ONDO the stronger idea.
- Long/short/wait: long, waiting.
- Invalidation: close below 0.05464.
- Chase risk: **elevated** — this is the desk's own flagged no-catalyst momentum name.
- Catalyst confirmation: **contradicted/absent** — explicitly no confirmed catalyst per the basket classification and direct news check.

### 3. PLTR — long, intraday, C-tier (drawdown-guard-demoted from B), **triggered**
- Entry 132.60, stop 130.81, tp1/2/3 136.88/138.67/140.47. Score 77.59 pre-gate (was 78 pre-demotion). Created 14:40 UTC.
- Catalyst: weak — one opinion piece ("Does Palantir's Latest Partnership With Nvidia Make It a Screaming Buy?", Motley Fool, 06:00 ET) is analysis, not hard news. Mostly a technical setup.
- Demoted B→C by `stocks_intraday_7d_drawdown_guard` + `stocks_intraday_long_guard` — **not Telegram-actionable**, paper/shadow-tracked only.
- Chasing? No, fresh trigger mid-session.
- Aligned with market mood? Tech/growth name in a session where semis/tech are the weakest sectors — some sector-mood friction despite the individual setup looking clean.
- Actionable level: already filled; not a live recommendation given C-tier/guard status — research value only.
- Chase risk: low for entry timing, but tier status means this is explicitly not an operator action.

### 4. XLK — short, intraday, C-tier, **triggered**
- Entry 178.09, stop 179.90, tp1/2/3 175.38/173.57/170.86. Created 11:37 UTC, running most of the session.
- Aligned with sector weakness: technology RS vs SPY -4.98%/20d, one of the two weakest sectors alongside semiconductors.
- Chasing? No — this has been open since mid-session, tracking the sector-rotation-out-of-tech thesis that has held all day.
- Not Telegram-actionable (C-tier) — paper-tracked only, but the cleanest short-side technical alignment on the board today.
- Invalidation: close above 179.90.

### 5. COIN — short, intraday, C-tier, **waiting_for_entry** (new, 18:36 UTC)
- Entry 160.90, stop 164.52, tp1/2/3 160.33/151.85/146.42. Score 60.93 — weakest score among the new late-session shorts.
- Catalyst/narrative: competitive-pressure headlines (Robinhood competing directly, OUSD/CRCL stablecoin competition eating into Coinbase's positioning) — narrative-supportive of a short, but **not** legal/regulatory risk; no indictment, investigation, or delisting flag found in a direct 24h news check.
- Chasing? No — brand-new signal, not yet filled.
- Actionable level: fill at 160.90; not Telegram-actionable (C-tier), shadow-tracked.
- Would invalidate: reclaim above 164.52, or a positive surprise on the CRCL/OUSD competitive narrative.

**Excess candidates not deep-dived** (score/priority below the top 5): SPY short (waiting, 18:15 UTC, counter to its own 20d uptrend — lower-confidence mean-reversion idea), DIA short (waiting, same caveat), XLV long (triggered, aligned with strongest sector healthcare), AAPL long (triggered, drawdown-guard-demoted from B), ALLO/USDT (not a live candidate — already stopped; carried as a system-integrity item, see TODO-3).

## 8. Best Candidates Ranked

1. **ONDO/USDT long** (crypto, B, triggered) — catalyst-confirmed, actionable now (already filled). Trigger: N/A, manage existing position toward tp1/tp2/tp3.
2. **XLM/USDT long** (crypto, B, tp2_hit, running) — catalyst-confirmed (RWA basket). Trigger for late entrants: pullback to 0.1866-0.1876 or a clean break above 0.1927 (tp2) on volume.
3. **XLK short** (stocks, C-tier/shadow, triggered) — best short-side technical alignment on the board; not Telegram-actionable, watch/paper only. Trigger: already filled at 178.09; re-entry watch on any bounce failing at 178-179.
4. **COIN short** (stocks, C-tier/shadow, waiting) — competitive-narrative short, watch for fill at 160.90.
5. **BANK/USDT long-watch** (crypto, B, waiting) — momentum-only, no catalyst; trigger 0.0561-0.0574 fill, but treat as lower-confidence chase risk versus ONDO.

## 9. Avoid / No Trade (this decision window only)

- **UNH** — AVOID / MANUAL REVIEW. DOJ antitrust probe into the Claritev unit widened (insurer collusion allegations, stacked on the existing Medicare-billing probe); today's UNH intraday long (score 66.06) was stopped, directly confirming the risk. This applies to *this decision window* — not a call to stop scanning or tracking UNH.
- **BANK/USDT as a chase above the stated entry zone** — no confirmed catalyst, momentum score alone is not sufficient support per the desk's own basket classification.
- **TSLA short** — internally gated by the system for an active `going_concern` legal/headline flag; correctly suppressed, not overridden here.
- Scanning, candidate generation, tracking, and outcome recording continue unaffected across all of the above — this is a per-symbol/per-window caution, never a system-wide stop.

## 10. Main Risks

- Crypto Fear & Greed (25, extreme fear) diverging from BTC/ETH uptrend — a fragile-uptrend risk if sentiment catches down to price.
- `stocks_intraday_7d_drawdown_guard` has now suppressed 100% of A/B stock candidates for a full session (8+ hours) — TODO-1 asks whether this is correctly calibrated; until answered, the desk is effectively stocks-actionable-blind today (by design or by miscalibration — undetermined).
- UNH DOJ-probe overhang remains unresolved and could re-widen or resolve at any time — binary headline risk.
- ALLO/USDT untracked-alert integrity issue persisting 3 cycles unresolved — a symptom that could recur on other symbols if the root cause (signal_id reuse on re-fired watchlist alerts) is systemic rather than ALLO-specific.
- SPY/DIA new shorts are counter-trend to their own daily uptrend label — elevated whipsaw risk into the close.

## 11. Action Plan — next 4 hours

- Manage ONDO/USDT (swing, open) and XLM/USDT (swing, tp2_hit) toward their remaining TPs; no new action needed.
- Watch BANK/USDT fill; if filled, treat as a lower-confidence, no-catalyst position sized/managed accordingly.
- Watch COIN/SPY/DIA short fills into the close; note SPY/DIA are counter-trend ideas requiring confirmation, not blind fills.
- No stocks A/B expected to fire while the drawdown guard remains active — human review of TODO-1 would clarify whether that's expected to persist into tomorrow's session.
- Post-close review (23:15 EEST) should reconcile today's crypto 4-win/9-loss B-tier record and the all-C-tier stocks session against the weekly signal-stats numbers.

## 12. Final Verdict per Mode

- **Crypto scalp**: no scalp-tier signals fired today; mode effectively idle this session (last scalp report ~1h old, no new scalp candidates surfaced in the excerpt reviewed).
- **Crypto intraday**: watch-only — ONDO/USDT (intraday sibling) tp2_hit running; no new intraday-only trigger of note beyond the swing signals covered above.
- **Crypto swing**: **normal, longs-only bias** — ONDO/USDT actionable (catalyst-confirmed), BANK/USDT watch (no-catalyst chase risk), XLM/USDT managing existing tp2_hit position.
- **Stocks intraday**: **watch_only / paper_only** — zero A/B actionable all session due to the drawdown guard; C-tier shadow candidates (PLTR, XLK, COIN, XLV, AAPL) are research-only.
- **Stocks swing/invest**: dormant (deprecated legacy framework, superseded by shadow-only position framework) — no verdict needed.

## 13. Sources

- Internal: `data/reports/scalp/2026-07-16_16-39_scalp_report.md`, `data/reports/intraday/2026-07-16_16-44_intraday_report.md`, `data/reports/swing/2026-07-16_14-27_swing_report.md`, `data/reports/stocks/intraday/2026-07-16_18-37_stocks_intraday_report.md`, `data/catalysts/2026-07-16/catalyst_cycle_16-47.md`, `data/catalysts/2026-07-16/catalyst_events.jsonl`, `data/catalysts/2026-07-16/narrative_baskets.jsonl`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items`, `watchlist_alerts`, `market_dashboard_snapshots`), `data/scheduled_runs/2026-07-16_default_schedule/scheduler.log`.
- [Ondo Hits 1-Month High: Here Is What's Driving The 17% Surge — BeInCrypto](https://beincrypto.com/) (2026-07-16, 11:41 UTC, via internal news_items)
- [SBI extends onchain finance push with Ondo deal to tokenize Japanese stocks — The Block](https://www.theblock.co/) (2026-07-16, 10:59 EDT, via internal news_items)
- [MEXC to Launch Ondo Tokenized Stock Trading Pairs on Spot Markets — t.me/MEXC_OfficialAnnouncements](https://t.me/MEXC_OfficialAnnouncements) (2026-07-16, 08:31 UTC, via internal news_items)
- [CRCL rebounds as investors weigh OUSD competition and Coinbase talks — AMBCrypto](https://ambcrypto.com/) (2026-07-16, 15:12 UTC, via internal news_items)
- Reused from prior review (18:39 EEST, internal source, <3h old, no fresher contradicting news_items found this cycle): [UnitedHealth Group (UNH) Faces Wider DOJ Antitrust Probe As Claritev Review Expands — Yahoo Finance](https://finance.yahoo.com/healthcare/articles/unitedhealth-group-unh-faces-wider-221504204.html) (2026-07-16); [UnitedHealth (UNH) Faces Broader DOJ Antitrust Probe Into Claritev — Simply Wall St News](https://simplywall.st/stocks/us/healthcare/nyse-unh/unitedhealth-group/news/unitedhealth-unh-faces-broader-doj-antitrust-probe-into-clar) (2026-07-16); [UnitedHealth Group under DOJ investigation over Medicare billing practices — Medical Economics](https://www.medicaleconomics.com/view/unitedhealth-group-under-doj-investigation-over-medicare-billing-practices) (2026-07-16).

**External web research note**: Internal `news_items` data was fresh, present, and consistent for all deep-dive candidates this cycle (ONDO, BANK, COIN, UNH) — no fresh WebSearch/WebFetch calls were needed per source-discipline rules (§G). UNH citations are reused from the 18:39 EEST review's own already-externally-verified sources, uncontradicted by any fresher internal news this cycle.

## 14. Fix Requests / TODO

### TODO-1 (carried forward, unchanged)
- **issue:** The stocks-intraday `stocks_intraday_7d_drawdown_guard` / `stocks_intraday_long_guard` combination has now blocked 100% of A/B-scored candidates for a full session (13:33 UTC through 18:37 UTC, 8+ hours), including names scoring 74-93 pre-gate (AVGO, XOM, AMD, XLE, PLTR, AAPL, QQQ).
- **evidence:** `data/reports/stocks/intraday/2026-07-16_18-37_stocks_intraday_report.md` §6/§7 — every name in the C-tier watchlist section shows `tier demoted B→C: stocks_intraday_7d_drawdown_guard`.
- **suggested manual fix:** Have a human confirm whether the 7-day rolling drawdown guard threshold is correctly calibrated against the current stocks all-tier diagnostic (PF 0.62-0.67, weekly totalR negative) — i.e. confirm this is the guard working as intended against a genuinely weak track record, not an over-tight threshold suppressing every opportunity regardless of individual setup quality.
- **priority:** medium
- **first observed:** 2026-07-16 18:39 EEST review (still open, now spans the full session)

### TODO-2 (carried forward, unchanged)
- **issue:** Several stocks B-tier signals in `active-signals` show `expires_at` timestamps in the past while still displaying non-terminal statuses (`tp1_hit`, `tp2_hit`, `triggered`) rather than a closed/expired terminal state.
- **evidence:** `python -m src.cli active-signals --asset-class stocks --tier B` — examples cited in the 18:39 EEST review (XOM, SMH, UNH with expires_at 2 days to 6+ weeks in the past, still non-terminal).
- **suggested manual fix:** have a human check whether the lifecycle/track-signals job is correctly terminalizing stocks B-tier signals past their `expires_at`.
- **priority:** medium
- **first observed:** 2026-07-16 16:20 EEST review (still open)

### TODO-3 (carried forward, escalating)
- **issue:** `detect_untracked_legacy_alerts` still returns 1 result — ALLO/USDT swing B, 65.4, sent 2026-07-16T14:27:05 UTC — for the **3rd consecutive review** (18:39 → 21:39 EEST, 3+ hours unresolved). The alert's own payload references `signal_id: sig_a5508682970c4c22`, which is a **different, older signal** created at 02:27:49 UTC (already `stopped`) — the 14:27 watchlist re-fire appears to have reused a stale signal_id instead of minting a fresh `proposed_signal`, which is why the detector can't match it.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-16`; direct SQL on `watchlist_alerts` (id 1620 at 02:27:51 and id 1635 at 14:27:05, both `payload_json.signal_id = "sig_a5508682970c4c22"`) vs `proposed_signals` (that signal_id's `created_at` is 2026-07-16T02:27:49, status `stopped` — no proposed_signal exists near 14:27).
- **suggested manual fix:** have a human check the watchlist-alert re-fire path for symbols that re-cross a tier threshold (e.g. `report`→`B`) a second time in one day — it looks like the re-fire is copying the original alert's signal_id forward instead of creating (or looking up) the newer `proposed_signal` minted at 14:27:04 for the same symbol/report.
- **priority:** medium (raised from low — 3 consecutive review cycles unresolved)
- **first observed:** 2026-07-16 18:39 EEST review; still open at 21:39 EEST

### TODO-4 (new)
- **issue:** The `paper entry-mode classify` scheduler step failed (exit=1) in cycle 6, a non-fatal failure that let the cycle continue.
- **evidence:** `data/scheduled_runs/2026-07-16_default_schedule/scheduler.log` line ~766: `2026-07-16 19:49:13,785 [INFO] CMD END: paper entry-mode classify exit=1 23.5s (attempt 1)` / `[WARNING] non-fatal step failed: paper entry-mode classify (exit=1) — cycle continues`.
- **suggested manual fix:** have a human check the `paper entry-mode classify` script's logs/traceback for this cycle to determine root cause (first occurrence noted; may be transient).
- **priority:** low
- **first observed:** 2026-07-16 21:39 EEST review (cycle 6, 19:49 EEST)
