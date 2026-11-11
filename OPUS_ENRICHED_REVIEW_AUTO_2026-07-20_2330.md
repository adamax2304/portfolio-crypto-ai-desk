# Opus Enriched Review — post-close final daily review — Auto Cycle 23:30 EEST

## 1. Executive Summary

**Slot: post-close final daily review** (nominal 23:15 EEST; dispatched ~23:30, ~15 min jitter). US cash session closed at 23:00 EEST. **Advisory only — no auto-trade, no scoring/threshold/strategy changes made or implied.**

**Stocks — how the session actually closed:** externally verified this run — Dow -0.59% (51,839.26), S&P 500 -0.19% (7,443.28), Nasdaq -0.05% (25,508.07). A **mild, genuine down day**, driven by fading chip-sector strength and weekend US-Iran tit-for-tat strikes (oil briefly touched $90/bbl). This is the first cycle in 3+ reviews where the internal `risk_off/short bias` label (VIX 18.46, breadth-above-EMA20 0.0%) roughly **converges** with the actual tape — though the move was still modest, not the sharp rout the internal breadth-0% reading implied. The system correctly produced **zero A/B-tier actionable stocks-intraday setups today**: all 15 raw A/B candidates (NVDA, GOOGL, XLK, META, XLF, TSLA, QQQ, SMH, DIA, UNH, LLY, NFLX, XLY, XLV, PLTR) were gate-demoted to C-tier watchlist on liquidity/trend-continuation/catalyst/legal grounds — a conservative, correctly-functioning outcome on a session that only moved modestly. TSLA/GOOGL now swing-blocked with earnings confirmed **Wednesday July 22 after the close** (externally verified) — 2 trading days out, gap-risk window opening.

**Crypto:** intraday regime reads bullish trend/risk-on (BTC/ETH uptrend, altcoin breadth 68.3%), while the swing (carry-forward, ~6h old) still reads range/chop — the same intraday-vs-swing divergence flagged the last two cycles, unresolved. 22 active B-tier positions, 21 long + 1 stale short (NEAR, 3.4 days past expiry). Zero A-tier signals. The no-catalyst momentum cluster (ACE, BANK, HEMI, PUMP — `momentum_breakout` basket, `avoid_chase`) is **re-confirmed 0 news_items in 24h** via direct DB query this run; several remain open B-tier longs — manage, don't add. **New finding this cycle:** INJ/USDT's catalyst (SEC transfer-agent registration / Robinhood listing, cited as "fresh" in the 19:09 EEST intraday report) is now **>24h old** (published 2026-07-19T18:25 UTC, ~26h ago at DB-query time) — the open INJ B-tier position's catalyst backing has just aged out; treat as a technical-only hold now, not catalyst-backed.

**Legal/headline risk unchanged:** UNH remains AVOID on active `sec_doj` legal cap (DOJ/Claritev probe, externally confirmed prior cycles). NVDA/AVGO shorts remain self-invalidated in the freshest scan for a **3rd consecutive cycle** (AVGO → `no_directional_setup` 38.4; NVDA demoted on sector/liquidity/catalyst gates) while `active-signals` still shows both `triggered` — escalating data-hygiene concern, see §14.

**Data hygiene:** ALLO/USDT (expired 2026-07-19, ~32h past) and NEAR/USDT-short (expired 2026-07-17, ~3.4 days past) are still displayed as active `tp1_hit` rows — now **4th+ consecutive** review cycle flagging this unresolved. Catalyst mapping **weak this run**: 851/3,121 mapped (27.3%), 2,270 unmapped (72.7%).

## 2. Data Used

- Reports: crypto scalp (`2026-07-20_18-58`, data ~21:58 EEST, ~1.5h old, fresh), crypto intraday (`2026-07-20_19-09`, data ~22:09 EEST, ~1.3h old, fresh), crypto swing (`2026-07-20_14-30`, data 17:30 EEST, ~6h old — carry-forward per freshness rule, still within 4–12h band), stocks intraday (`2026-07-20_19-54`, data ~22:54 EEST, ~35 min old, freshest possible). Stocks swing/invest still `2026-07-02` (18 days stale) — excluded, planning-only, not referenced (consistent with the deprecated legacy stocks swing/invest framework).
- Catalysts: `data/catalysts/2026-07-20/catalyst_events.jsonl` (3,121 cumulative events today, directly counted this run), `narrative_baskets.jsonl` (5 baskets), latest `catalyst_cycle_19-13.md` (22:13 EEST).
- LLM packets: `llm_analysis_packet.md` (22:10 EEST, fresh), `llm_stocks_packet.md` (22:38 EEST, fresh).
- CLI: `active-signals` ×2 (crypto 22 rows, stocks 50 rows — many historical tail beyond today), `signal-stats` ×2 (week-level; no daily-granularity flag in the allowed command set — see §3 note), `detect_untracked_legacy_alerts --since 2026-07-20` (0 findings — clean, no untracked crypto alerts today).
- DB reads (read-only): `news_items` 24h symbol search for ACE, BANK, HEMI, PUMP, INJ (all 0 rows in the last 24h — ACE/BANK/HEMI/PUMP confirmed genuinely uncovered; INJ's most recent hit is 2026-07-19T18:25 UTC, ~26h old, i.e. just outside the 24h window — catalyst has aged out); `catalyst_events.jsonl` direct count (3,121 total / 851 mapped / 2,270 unmapped).
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_2147.md` (late-session risk review slot) — used for §4 comparison.
- External: 3 WebSearch queries (US stock market close today, Bitcoin/Ethereum price today, Tesla/Alphabet earnings date) + 1 WebFetch (Yahoo Finance live-blog close numbers; TheStreet fetch returned 403, Yahoo Finance page substituted successfully). Sources ingested via `scripts.ingest_enriched_review_sources`.

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime ~23:16 EEST, ~14 min old at review start — well under the 3h defer threshold. Not deferred.
- Latest completed cycle: `cycle_01_21-44_summary.md` in the `2026-07-20_default_schedule` folder (folder rolled over at 21:44 EEST; prior day's folder was active until then) — mtime ~22:47 EEST, ~43 min old.
- Crypto scalp/intraday: ~1.3–1.5h old (normal cadence, fresh). Swing: ~6h old — carry-forward, flagged, used for regime cross-check only, no fresh swing candidates cited.
- Stocks intraday: ~35 min old — freshest possible this cycle. Stocks swing/invest: 18 days stale, unused.
- Monitor logs (supporting freshness signal, not a scored input): `crypto_monitor` mtime 23:22 EEST, `derivatives_monitor` 23:24 EEST, `stocks_monitor` 22:59 EEST — all recently active, no dead-process signal observed.
- No anomaly from `detect_untracked_legacy_alerts` (clean, 0 findings).
- Note on §D (all-mode signal-stats): the allowed CLI set has no `--period day` flag; `signal-stats` returns week-level aggregates by design. Today's daily wrap below is built from the week-level headline plus today-dated rows visible in `active-signals` (expiry/entry timestamps dated 2026-07-20), not a separate daily-only query.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-07-20 23:30 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["daily-only (non-week) signal-stats breakdown — not in allowed CLI set", "monitor/paper-portfolio live status beyond log mtimes"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~14min old", "stocks intraday report ~35min old", "crypto scalp/intraday ~1.3-1.5h old", "crypto swing ~6h old (carry-forward)", "stocks swing/invest 18 days stale, unused", "monitor logs all touched within the last ~30min"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["mixed", "chop", "risk_off"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto intraday: bullish uptrend, breadth 68.3%", "crypto swing (carry-forward): range/chop, breadth 48.7%", "stocks internal label: risk_off/short, breadth-above-EMA20 0%, VIX 18.46", "external confirmed close: Dow -0.59%/S&P -0.19%/Nasdaq -0.05% — a mild down day, converging with (not sharply confirming) the internal label", "BTC ~$64.7k/ETH ~$1,875 at Monday's open, holding through the day per external search, Iran tensions capping upside, Fed meeting July 28-29 ahead"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["mapping_weak", "no_catalyst", "stale_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 72.7% unmapped (2,270/3,121) this run, direct count", "momentum_breakout basket: ACE/PUMP flagged avoid_chase (BANK dropped out of the basket this cycle), ACE tagged overextended, confirmed 0 news_items in 24h for ACE/BANK/HEMI/PUMP via direct DB query", "INJ/USDT catalyst now stale: most recent news_items hit 2026-07-19T18:25 UTC, ~26h old at query time, outside the 24h freshness window used by the scoring report", "perps_dex_narrative basket: HYPE primary, wait_pullback, fresh <1h, unchanged 3rd cycle running with no position taken", "rwa_narrative basket: ONDO/XLM primary, aged from <6h to <24h since last cycle, still no fresh confirmation"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.45,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["long/short crowding classification for ACE/ALICE (unknown)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE/PUMP/HEMI/ZAMA/VIRTUAL/ALICE/INJ: price up + OI up, fresh positioning confirms trend per report, crowding mostly normal (ACE/ALICE unknown)", "BANK/USDT: price up + OI down — short-covering pattern, weaker continuation quality, flagged in report itself"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ACE/USDT +90.7% 24h on only 0.57x volume — thin-participation blow-off, explicitly tagged overextended in momentum_breakout basket", "ACE/BANK/HEMI/PUMP already open B-tier longs — a fresh entry now would be chasing an existing position further", "stocks: all 15 raw A/B candidates demoted on last_30m_requires_trend_continuation + liquidity_rvol_below_min + catalyst_none gates — no clean stocks entry existed all session"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 22 active rows — 8 triggered/open-actionable, 4 waiting_for_entry, 1 tp1_hit(closed-partial-win) plus several tp1/tp2_hit rows further along, 1 stale short (NEAR, no-entry-lifecycle-stale)", "stocks: 50 active rows, current-cycle ones (expires 2026-07-21) all C-tier triggered/tp1_hit/review-shadow — zero A/B triggered today", "ALLO/USDT (expired 2026-07-19, ~32h past) and NEAR/USDT-short (expired 2026-07-17, ~3.4 days past) still shown active tp1_hit — needs_review, recurring 4th+ consecutive cycle"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: active sec_doj cap, demoted B->C, confirmed DOJ/Claritev probe prior cycles, unchanged", "TSLA: going_concern legal-risk cap active this cycle, demoted A->C independent of earnings timing", "NVDA/AVGO shorts self-invalidated by fresher scan for a 3rd consecutive cycle but still shown triggered in active-signals", "TSLA/GOOGL earnings externally confirmed Wednesday 2026-07-22 after market close — 2 trading days out, gap-risk window now open", "geopolitical tail risk live: weekend US-Iran tit-for-tat strikes, oil touched ~$90/bbl before easing"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto direction=short: PF 0.25, avgR -0.43, n=9 (week) — weak, avoid new crypto shorts absent an exceptional clean setup", "crypto tier=B triggered winrate 32% (n=131, reliable, week) — low, but PF still 2.09 on winner size", "crypto mode=scalp: PF 1.13, only 2 wins/9 losses (week) — weakest crypto mode this week", "stocks tier=C (week): PF 0.73, winrate 15.2% (n=191, reliable) — negative edge, watchlist-only by design, consistent with today's zero-A/B outcome", "stocks tier=A/B (week): n=7 only, anecdotal, not decision-grade"]
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
    "best_long_candidate": { "symbol": "ONDO/USDT or XLM/USDT", "trigger": "rwa_narrative basket, related_beta_rotation — enter only on a pullback into structure with RS confirmation, basket has aged from <6h to <24h without a fresh confirmation, do not chase", "reason": "institutional RWA/tokenization thesis, catalyst-backed and outside the no-catalyst momentum cluster, though freshness is now weakening" },
    "best_short_candidate": { "symbol": "SMH/XLK (stocks, semiconductors/tech sector)", "trigger": "failed retest of tomorrow's session high with RVOL clearing the stocks-intraday confirmation gate", "reason": "genuinely weakest sector on 20d RS (-14.75%/-7.56% vs SPY); today's actual close was a mild down day, partially validating sector weakness, but do not short a bounce on the internal label alone" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "clean pullback into structure per perps_dex_narrative's own wait_pullback playbook", "reason": "carried forward unchanged for a 3rd consecutive cycle — narrative still technically fresh (<1h basket re-tag) but no new information and no position taken; treat as aging, watch for it to either resolve into a pullback or go stale" },
    "avoid_candidate": { "symbol": "UNH, TSLA (stocks legal risk), NVDA/AVGO-short (stale DB rows)", "reason": "UNH: confirmed active DOJ/Claritev legal risk. TSLA: active going_concern cap plus earnings gap risk (2 days out). NVDA/AVGO: self-invalidated by the system's own fresher re-scan for a 3rd consecutive cycle; the DB's triggered/tier-C rows are stale, not live ideas" },
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
| market_regime | caution | 0.55 | mixed, chop, risk_off | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, no_catalyst, stale_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.45 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, entry_late | advisory_only |
| execution_lifecycle | caution | 0.75 | open_actionable, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | legal_risk, headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_2147.md` (21:30, late-session risk review):

- **Stocks close finally verified externally**: the close (Dow -0.59%/S&P -0.19%/Nasdaq -0.05%) is a genuine, if modest, down day — the first cycle in 3 reviews where the internal `risk_off/short bias` label roughly converges with the actual tape rather than diverging from a flat/up read. TODO-stocks-regime-label-divergence is **partially resolved this cycle**, though the magnitude gap (0% breadth vs. a sub-1% index move) is still worth one more cycle of observation before closing the TODO outright.
- **INJ catalyst aged out**: was cited as "fresh attention/catalyst detected" in the 19:09 EEST intraday report (importance 0.95); direct DB check this run shows the underlying news_items row is now ~26h old, i.e. outside the 24h freshness window. New finding this cycle — INJ's open B-tier position should now be read as technical-only, not catalyst-backed.
- **momentum_breakout basket composition changed**: BANK/USDT dropped out of the basket (was ACE/PROM/BANK at 21:30, now ACE/PUMP only) — PROM and BANK's 24h moves apparently cooled below the basket's re-scan threshold. ACE/PUMP unchanged, still avoid_chase.
- **rwa_narrative basket aged**: freshness moved from <6h (21:30) to <24h (this cycle) with no new confirming headline — the same ONDO/XLM idea, getting stale without a pullback occurring.
- **NVDA/AVGO self-invalidation now a 3rd consecutive cycle** (was 2nd at 21:30) — escalating, see §14.
- **ALLO/NEAR staleness now a 4th+ consecutive cycle** (was 3rd at 21:30) — escalating, see §14.
- **Catalyst mapping essentially unchanged**: 72.2% unmapped at 21:30 vs. 72.7% now (direct recount) — still weak.
- **TSLA/GOOGL earnings date externally confirmed this cycle**: Wednesday 2026-07-22 after market close (was "~2 trading days out, unknown exact date" per internal report at 21:30) — now a hard external date, gap-risk framing sharpens.
- **UNH legal risk unchanged**, carried forward verbatim.

## 5. Catalyst Coverage

- Total `catalyst_events` today: **3,121** (direct count from `catalyst_events.jsonl`)
- Mapped (non-null symbol): **851** (27.3%)
- Unmapped (null symbol): **2,270** (72.7%)
- `narrative_baskets`: **5** (delisting_thin_liquidity, ai_narrative, perps_dex_narrative, rwa_narrative, momentum_breakout)

**Catalyst mapping weak this run — use the catalyst layer as context, not final decision.**

Top unmapped headlines (sample):
- "Tradfin: *SEOUL STOCK MARKET'S KOSPI FALLS 4%..." (macro/index headline, no single-symbol mapping expected)
- "FSTA vs. XLP: How These Popular Consumer Staples ETFs Compare for Investors" (comparison piece, ambiguous primary symbol)
- "Oil Pulls the Market Lower Again" (macro headline, no symbol mapping expected)
- "CoreWeave vs. Applied Digital: Evaluating Disparities in Revenue Scale..." (comparison piece, two tickers, resolver picks neither)

This is a known, previously-flagged limitation (per project memory: scan-time `news_supported` under-fires because `load_recent_news` uses a ~5h lookback window; a wider-window fix has been scoped but is deferred pending sign-off) — not a new finding, carried forward as context only.

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed** — intraday timeframe reads risk-on/uptrend (breadth 68.3%), swing/higher-timeframe carry-forward still reads range/chop (breadth 48.7%); external color: BTC holding ~$64.7k, Iran tensions capping the rally, Fed meeting July 28-29 ahead, sentiment "mixed" for 2H26 outlooks. Treat as a short-term bullish tilt inside a broader range, not a confirmed trend change.
- Stocks mood: **risk-off (mild)** — internal label risk_off/short-bias (breadth-above-EMA20 0%, VIX 18.46) now roughly converges with the externally-confirmed close (Dow -0.59%/S&P -0.19%/Nasdaq -0.05%), a modest down day driven by fading chip strength and weekend Iran-related oil volatility. Do not read this as license for aggressive shorting tomorrow — the move itself was mild, and the system's own gates correctly found zero clean A/B entries all session.
- Dominant narrative: no-catalyst momentum cluster (ACE/PUMP, avoid_chase) still the loudest "where money is flowing" signal in crypto; semis/tech relative weakness (SMH -14.75%, XLK -7.56% RS vs SPY) the cleanest multi-day stocks thesis; energy/healthcare/financials the strongest stocks sectors.
- Preferred side now: **wait-for-trigger / catalyst-backed** — neither book produced a clean, fresh, un-chased setup today.
- Best long candidate: ONDO/USDT or XLM/USDT (rwa_narrative) — only on a pullback; basket aging (<6h → <24h) without confirmation.
- Best short candidate: SMH/XLK (stocks) — only after a failed retest with RVOL confirmation; do not short the internal label alone.
- Best catalyst-backed candidate: HYPE/USDT (perps_dex_narrative, wait_pullback), unchanged for a 3rd consecutive cycle.
- What to avoid: UNH (legal), TSLA (legal cap + earnings gap risk now 2 days out, confirmed Wed 2026-07-22), NVDA/AVGO shorts (self-invalidated, stale DB rows, 3rd cycle), chasing ACE/PUMP at current extension.
- What would change the view: a confirmed fresh catalyst hitting the ACE/PUMP cluster; a clean multi-timeframe crypto trend alignment (intraday + swing both uptrend); stocks breadth-above-EMA20 recovering meaningfully off 0%; UNH DOJ resolution or escalation; GOOGL/TSLA earnings Wednesday resolving the current gap-risk overhang either direction.

## 7. Candidate Deep Dives

**1. INJ/USDT (crypto, B-tier intraday, triggered score 66.2) — MANAGE, catalyst has just aged out**
- Price has reacted to a real catalyst (SEC transfer-agent registration + Robinhood listing at Summit, importance 0.95, `canonical_news_event`) — but the underlying news_items row is now ~26h old (published 2026-07-19T18:25 UTC), just outside the 24h freshness window used for scoring.
- Not a chase (entry was taken at 5.3509-5.3842, current price ~5.40, still inside range); this is an existing-position management question, not a new entry.
- Actionable now only as hold-toward-invalidation (5.3101) / expiry (2026-07-21T19:46); do not treat the aging catalyst as a reason to add size.
- What would invalidate: 1h close below 5.3101, or the position's own expiry.
- Catalyst confirmation: **was** confirmed (verified via internal `news_items`, importance 0.95, multiple related headlines 07-16 through 07-19); now stale, not contradicted — just aged.

**2. ACE/USDT & PUMP/USDT (crypto, B-tier, multiple active rows) — MANAGE, do not add, confirmed no-catalyst**
- ACE +90.7% 24h on 0.57x volume (thin-participation blow-off, explicitly tagged `overextended` in the `momentum_breakout` basket); confirmed 0 `news_items` in 24h via direct DB query this run.
- PUMP +15.8% 24h on 0.93x volume — less extreme but still in the same no-catalyst basket, `avoid_chase` playbook.
- Not aligned with current mood beyond generic risk-on; both explicitly named in `avoid_chase`.
- A fresh entry now would be very late on ACE specifically. Existing positions: manage toward their own invalidation levels (ACE swing 0.1103 / intraday 0.1015 depending on which row; PUMP swing 0.001906 / intraday 0.001891).

**3. HYPE/USDT (crypto, catalyst-watch, not yet in active-signals) — WAIT FOR PULLBACK, aging**
- `perps_dex_narrative` basket (HYPE primary; DYDX/GMX/ASTER related), playbook explicitly `wait_pullback`.
- No open position; unchanged for a 3rd consecutive review cycle (18:30 → 21:30 → now) with no pullback occurring and no fresh confirming headline beyond the original Hyperliquid prediction-market items.
- Catalyst confirmation: yes, but getting old without price action confirming the thesis — if this repeats another cycle or two with no pullback, consider it stale rather than fresh.
- What would invalidate: basket goes fully stale without a pullback, or HYPE breaks down through structure instead of pulling back.

**4. UNH (stocks, tier C, short, triggered 75.5) — AVOID**
- Legal/headline risk: active DOJ/Claritev antitrust investigation, externally confirmed in a prior cycle, unchanged this cycle. System itself caps this signal (`sec_doj`, demoted B→C).
- Final verdict: **AVOID / MANUAL REVIEW REQUIRED** — never a clean actionable, regardless of technical score. No change from last cycle.

**5. TSLA (stocks, tier C, short, triggered 81.7) — AVOID (legal + earnings)**
- Active `going_concern` legal-risk cap this cycle (demoted A→C), **plus** externally-confirmed earnings Wednesday 2026-07-22 after close — 2 trading days out. Two independent reasons to avoid, not one.
- Not actionable regardless of the 81.7 raw score.

**6. NVDA / AVGO shorts (stocks, tier C) — AVOID, treat DB rows as stale (3rd consecutive cycle)**
- AVGO: this cycle's fresh scan again returns `no_directional_setup` (score 38.4) — the DB still shows it "triggered" (score 90.7, tier C).
- NVDA: demoted A→C again this cycle on `sector_confirmation_weak_or_unknown`, `last_30m_requires_trend_continuation`, `liquidity_rvol_below_min`, `catalyst_none_and_not_exceptional_technical` — identical gate set to the last two cycles.
- Not actionable; do not treat the `active-signals` rows for these two as live ideas. Now a 3-cycle pattern — see §14.

## 8. Best Candidates Ranked

1. **Catalyst-watch: HYPE/USDT** — trigger: clean pullback into structure while `perps_dex_narrative` stays confirmed; unchanged for a 3rd cycle, getting old — treat as lower-confidence than the first time it was flagged.
2. **Long-watch: ONDO/USDT or XLM/USDT** — trigger: pullback into structure with RS confirmation per `rwa_narrative`'s `related_beta_rotation` playbook; basket has aged from <6h to <24h without confirmation — do not chase a fresh breakout.
3. **Short-watch: SMH/XLK (stocks)** — trigger: failed retest of tomorrow's session high with RVOL clearing the stocks-intraday gate; sector RS genuinely weak (-14.75%/-7.56%) and today's actual close partially validated broad stocks softness, but the move was mild — wait for the rejection, don't pre-position on the label.
4. No new clean actionable entry on either book today beyond managing the 22 existing crypto B-tier positions and INJ's now-aging catalyst hold — both books are gated by their own confirmation rules, functioning as designed on a session that moved only modestly in both asset classes.

## 9. Avoid / No Trade

This window / today only — never a command to stop the system:

- **UNH** — confirmed, active DOJ/Claritev antitrust probe. Avoid until resolved.
- **TSLA** — active going_concern legal cap plus confirmed earnings 2026-07-22 after close (2 trading days out); avoid new positions and reduce/close any live exposure through the print.
- **NVDA / AVGO shorts** — self-invalidated by the system's own fresher re-scan, 3rd consecutive cycle; do not treat `active-signals`' triggered/tier-C rows as live.
- **ACE / PUMP** — confirmed no-catalyst momentum cluster (`avoid_chase`), ACE specifically thin-volume/overextended; manage existing positions, do not add or chase fresh entries.
- **GOOGL** — earnings 2026-07-22 after close alongside TSLA; same gap-risk caution.
- **NEAR/USDT short** — stale 3.4 days past expiry, weak historical crypto-short performance (PF 0.25, n=9, week); needs manual review, not a fresh entry.
- Scanning, candidate generation, tracking, and the scheduler continue uninterrupted overnight into the Asia session — none of the above is a stop-the-system finding.

## 10. Main Risks

- **Recurring signal-lifecycle staleness** (ALLO/NEAR past-expiry-but-still-shown-active) now unresolved across **4+ consecutive** review cycles — see §14, priority escalated.
- **NVDA/AVGO self-invalidation persisting a 3rd cycle** without the DB reflecting the newer, contradicting scan — operator risk if `active-signals` is read without cross-checking the freshest report.
- **INJ catalyst aging out mid-hold** — a live position's thesis quietly shifted from catalyst-backed to technical-only between cycles; worth a general note that catalyst freshness should be re-checked against open positions, not just new candidates (see §14).
- **Catalyst mapping stuck around 72-73% unmapped** for multiple consecutive cycles — known, deferred issue (widening fix scoped, pending sign-off per project history) — catalyst framing should stay secondary to technical/lifecycle signals until resolved.
- **Crypto direction=short historically weak** (PF 0.25, n=9, week) — avoid new crypto shorts absent an exceptional, clean, catalyst-confirmed setup.
- **Earnings-window risk now live, not just approaching**: GOOGL/TSLA report Wednesday 2026-07-22 after close — 2 trading days out; gap risk applies to any position held through that print.
- **Geopolitical tail risk continues**: weekend US-Iran strikes, oil briefly ~$90/bbl; Fed meeting July 28-29 is the next major macro catalyst for both books.
- **Intraday-vs-swing crypto regime divergence unresolved** — 3rd consecutive cycle with intraday reading uptrend and swing reading range/chop; treat crypto risk-on as short-term/tactical only, not a confirmed trend regime change.

## 11. Action Plan — next 4 hours (overnight into Asia)

- Manage existing crypto B-tier positions (INJ, XPL, VIRTUAL, ACE, ZAMA, HEMI, BANK, PENGU, PUMP, SYN, KAITO, LTC, ALLO*, NEAR*-short) toward their own invalidation/TP levels; do not add to the ACE/PUMP no-catalyst cluster. (*ALLO/NEAR need manual status confirmation per §14.)
- Re-flag INJ's catalyst as aged (>24h) in any manual monitoring of that position — hold on technical merit only from here.
- Watch HYPE/USDT and ONDO/XLM for pullback confirmation overnight; both narratives are aging without price action confirming them — if neither resolves in the next cycle or two, treat as stale rather than fresh.
- No new stocks intraday positions overnight (US market closed); tomorrow, do not initiate shorts off the internal risk_off label alone — require an RTH failed-retest + RVOL confirmation, and treat GOOGL/TSLA as earnings-blocked through Wednesday's print.
- Manually confirm the true status of ALLO/USDT and NEAR/USDT-short — both display as active well past their own expiry; this has now repeated across 4+ review cycles.
- Continue treating NVDA/AVGO short ideas as invalid regardless of `active-signals` display, given a 3rd consecutive fresh-scan self-invalidation.
- Overnight-into-Asia crypto watch: no confirmed fresh catalyst driving the current altcoin strength cluster; BTC/ETH holding steady per external color, Iran-related headline risk remains the main wildcard.

## 12. Final Verdict per Mode

- **Crypto scalp/intraday/swing:** no new trade this window; manage the 22 existing B-tier positions (21 long + 1 stale short), avoid adding to the ACE/PUMP no-catalyst cluster, avoid new crypto shorts given weak historical short performance, treat INJ's catalyst as aged.
- **Stocks intraday:** no A/B actionable (0 today, all 15 raw A/B candidates gate-demoted to C); UNH and TSLA both carry active legal-risk caps (AVOID), NVDA/AVGO shorts stale/invalid for a 3rd cycle, GOOGL/TSLA now earnings-blocked with a confirmed Wednesday print.
- **Stocks swing/invest:** no fresh data (18 days stale) — do not use for decisions.
- **Overall:** watch-only / wait-for-trigger across both books overnight into the Asia session and tomorrow's US pre-market. Advisory only, no auto-trade.

## 13. Sources

- [US Stock Market Close — July 20, 2026 (Yahoo Finance live blog)](https://finance.yahoo.com/markets/live/stock-market-today-monday-july-20-dow-sp-500-nasdaq-111429441.html) (2026-07-20)
- [Bitcoin and ethereum prices today, Monday, July 20, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-monday-july-20-2026-crypto-prices-mixed-as-second-half-2026-outlooks-conflict-151956982.html) (2026-07-20)
- [Tesla Q2 2026 Earnings Call Set for July 22 — Time Zone Guide](https://www.basenor.com/blogs/news/tesla-q2-2026-earnings-call-set-for-july-22-time-zone-guide) (2026-07-15)
- [Alphabet and Tesla earnings put AI spending and Bitcoin holdings under the microscope — CryptoBriefing](https://cryptobriefing.com/alphabet-tesla-earnings-ai-spending-bitcoin/) (2026-07)
- Internal: `data/reports/intraday/2026-07-20_19-09_intraday_report.md`, `data/reports/swing/2026-07-20_14-30_swing_report.md`, `data/reports/stocks/intraday/2026-07-20_19-54_stocks_intraday_report.md`, `data/catalysts/2026-07-20/catalyst_cycle_19-13.md`, `catalyst_events.jsonl` (direct count), `news_items` DB table (read-only, direct query for ACE/BANK/HEMI/PUMP/INJ).
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_2147.md` (used for §4 comparison).

## 14. Fix Requests / TODO

### TODO-signal-staleness-display
- **issue:** ALLO/USDT (crypto, expired 2026-07-19T15:21) and NEAR/USDT-short (crypto, expired 2026-07-17T15:56) are still returned by `active-signals` as live `tp1_hit` rows, well past their own `expires_at`. Same pair flagged across the last 3+ review cycles — still unresolved.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` output this run, rows `sig_10088a4c71cae845` (ALLO, weekend=Y) and `sig_b16bb9e54598333a` (NEAR); prior reviews `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_2153.md`, `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_1848.md`, `OPUS_ENRICHED_REVIEW_AUTO_2026-07-20_2147.md` flag the identical pair.
- **suggested manual fix:** investigate whether `active-signals` should filter or clearly label rows past `expires_at`; may share a root cause with the previously-confirmed watchlist-alert/signal-reuse bug on ALLO/BANK per project history — worth a joint root-cause session.
- **priority:** high
- **first observed:** 2026-07-19 21:53 EEST (this is the 4th+ consecutive automated review to observe it unresolved)

### TODO-nvda-avgo-self-invalidation-lag
- **issue:** NVDA and AVGO short setups have self-invalidated in the freshest scan for a 3rd consecutive cycle (AVGO → `no_directional_setup` score 38.4 again this cycle; NVDA demoted A→C on the same sector/liquidity/catalyst gate set again), but `active-signals` still returns both as `triggered`/tier-C rows with no indication the underlying setup no longer exists per the system's own latest read.
- **evidence:** `data/reports/stocks/intraday/2026-07-20_19-54_stocks_intraday_report.md` (`AVGO (no_trade): 38.39 — no_directional_setup`; NVDA demotion note in §7 watchlist) vs. `active-signals --asset-class stocks` rows `sig_48899bb488411af9` (AVGO) and `sig_e0fceb60a6327886` (NVDA) still shown triggered.
- **suggested manual fix:** consider whether `active-signals` should cross-check the latest report's per-symbol verdict and annotate/suppress rows the newest scan has already contradicted, to reduce operator misread risk.
- **priority:** medium (consider escalating to high if a 4th cycle repeats this)
- **first observed:** 2026-07-20 18:48 EEST (3rd consecutive cycle now)

### TODO-catalyst-freshness-not-rechecked-on-open-positions
- **issue:** INJ/USDT's open B-tier intraday position was scored with a "fresh" catalyst (importance 0.95, `canonical_news_event`) at 19:09 EEST, but the underlying `news_items` row is dated 2026-07-19T18:25 UTC — by this review's DB-query time (~20:28 UTC) it was already ~26h old, i.e. outside the scoring system's own 24h freshness window. The position itself is not wrong, but its catalyst-backed framing quietly went stale without any re-check, since freshness gates are applied at candidate-scoring time, not re-evaluated against already-open positions.
- **evidence:** `data/reports/intraday/2026-07-20_19-09_intraday_report.md` §Trade Idea #6 INJ/USDT ("fresh attention/catalyst detected; verification canonical_news_event; importance 0.95") vs. direct `news_items` query this run: most recent INJ row `2026-07-19T18:25:08+00:00`, `datetime('now')` = `2026-07-20 20:28:42` UTC (~26.1h gap).
- **suggested manual fix:** consider whether open positions with a catalyst-backed thesis should carry a periodic re-check (e.g. surfaced in a monitor or the next scoring cycle) so operators aren't relying on a scoring-time freshness snapshot that silently ages during the hold.
- **priority:** low
- **first observed:** 2026-07-20 23:30 EEST (new finding this cycle)
