# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:40 EEST

## 1. Executive Summary

**Slot: crypto overnight / Asia review (nominal 04:30 EEST), completed ~04:40 EEST on Sunday 2026-07-19. Advisory only — no auto-trade, no code/scoring/routing changes.** Pipeline healthy, not deferred: `scheduler.log` (mtime 04:39) and latest `cycle_10_03-13_summary.md` (mtime 04:00) are both well inside the 3h defer threshold.

Stocks markets are closed (weekend) — every stocks reference below is Monday-planning context only. Crypto is the sole live actionable class this window.

**Headline findings:**
1. **Overnight buildup, not a quiet Asia session.** 13 active B-tier crypto signals now live vs. 3 at the last review (18:48 EEST Sat) — TRUMP re-entered fresh (prior TRUMP signal stopped out -1R Saturday afternoon, per prior review), LTC and ETH are new, and **ALLO/USDT now has 4 separate live signals** (scalp/intraday×2/swing) and **BANK/USDT has 3** (scalp/swing/intraday) — a real correlation cluster on two symbols.
2. **Verified external macro overhang: US–Iran conflict, day six of airstrikes, Strait of Hormuz closed, oil up.** This is actively suppressing crypto risk appetite (Fear & Greed dropped 27→25) even while the internal technical regime reads "bullish trend / risk-on" (BTC/ETH uptrend, 57.9% of alts above EMA20). Treat the internal "risk-on" label as **technically true but macro-fragile** overnight.
3. **Confirmed bug (see §14 TODO-1, high priority): the news/symbol detector false-tagged NEAR/USDT** on Iran-conflict headlines (literal substring match on the word "near" in "AREA NEAR HAJIABAD") and this propagated into today's `ai_narrative` basket as a primary-symbol catalyst summary. Do not treat NEAR's presence in the AI-narrative basket as real catalyst support.
4. **BANK/USDT is chase risk**: +44.5% 24h / +169.7% 7d, no verified catalyst, volume ratio only 0.33x (weak confirmation) — flagged AVOID for new entries below.
5. **Best long-watch: TRUMP/USDT and LTC/USDT**, both on `crypto_swing_narrative_rs_momentum` — the desk's strongest playbook this run (14d WR 72% / PF 5.80 / +24R) — and neither is extended.
6. **Best catalyst-backed: ETH/USDT** — Bitmine (BMNR) institutional ETH accumulation (verified externally, 4.8% of ETH supply, "Alchemy of 5%" goal) is real and ongoing; signal is `waiting_for_entry`, not yet chased.

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-19_01-10_scalp_report.md` (fresh, ~30min old), `data/reports/intraday/2026-07-19_01-16_intraday_report.md` (fresh, ~24min old), `data/reports/swing/2026-07-19_00-58_swing_report.md` (fresh, ~42min old). Stocks intraday `2026-07-17_21-56` (~2 days old, stale, market closed all weekend — carry-forward context only). Stocks swing/invest (`2026-07-02`) are ~17 days stale — legacy/deprecated per prior audits, ignored.
- Catalyst: `data/catalysts/2026-07-19/catalyst_events.jsonl` (998 rows), `narrative_baskets.jsonl` (5 baskets), `catalyst_cycle_01-21.md` (latest, fresh).
- LLM packet: `data/processed/llm_analysis_packet.md` (mtime 04:17, fresh).
- Internal CLI: `active-signals --asset-class crypto` (13 rows), `active-signals --asset-class stocks` (50 rows, all closed/resolved, market shut), `signal-stats --asset-class crypto` (week: A/B headline sample=99, PF 1.19, totalR +4.0), `detect_untracked_legacy_alerts --since 2026-07-19` (0 results, clean).
- SQLite direct reads (read-only, `db/crypto_ai_desk.sqlite`): `news_items` lookups for ETH/BANK/ALLO/TRUMP/LTC/XEC/ETHFI/NEAR (last 24h), full-row inspection of the false-positive NEAR/Iran match.
- **External web research used** (2 WebSearch + 1 WebFetch, all loaded): Bitmine/BMNR ETH accumulation status (confirmed), Iran-conflict crypto market impact (confirmed via Yahoo Finance, fetched and verified).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-18_1840.md` (18:48 EEST Sat) — most recent available. **Note: the 21:30 and 23:15 Saturday slots produced no output file of any kind (no LATEST/AUTO/DEFERRED/BLOCKED artifact)** — see §14 TODO-3.

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime 04:39 EEST, **fresh** (~1 min old at review start).
- Latest cycle summary `cycle_10_03-13_summary.md`: mtime 04:00 EEST, **fresh** (~40 min old).
- Crypto reports (scalp/intraday/swing): all **fresh**, generated within the last hour.
- Stocks reports: intraday ~2 days old (market closed, moot); swing/invest ~17 days old (deprecated framework, per memory — replaced by shadow-only `stocks_swing_growth_breakout`).
- Catalyst layer: fresh (`catalyst_events.jsonl` mtime 04:21), but **mapping is weak this run — see §5**.
- Paper/monitor pipeline: scheduler log shows a full clean cycle 04:03-04:39 (paper execution accounting, structural TP/stop refresh, entry-mode classify, paper-shadow A/B, latency audit, derivatives backfill — all `exit=0`). No pipeline errors observed.
- Not deferred; review proceeds normally.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-19 04:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks_swing_and_invest_reports_deprecated_17d_stale"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 04:39", "cycle_10 summary mtime 04:00", "crypto reports <1h old"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["risk_on", "mixed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["internal: BTC/ETH uptrend, 57.9% alts above EMA20, regime=bullish trend risk-on", "external: Fear&Greed 25 (down from 27), sixth day of US airstrikes on Iran, Strait of Hormuz closed, oil up - risk aversion overhang"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["70.8% of catalyst_events unmapped (707/998)", "ETH Bitmine accumulation catalyst verified externally", "ALLO/BANK/TRUMP/LTC/XEC/ETHFI: no fresh verified catalyst in news_items 24h window", "NEAR falsely tagged into ai_narrative basket via Iran-headline substring bug"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.4,
      "reason_codes": ["oi_supports", "data_unavailable"],
      "data_missing": ["OI 24h change for BANK/XEC/ETHFI (n/a, MEXC fallback only)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO: price up + OI up (fresh positioning), crowding normal", "TRUMP/LTC: price up + OI up, crowding normal", "BANK: fallback_via_mexc, OI n/a - low confidence"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "entry_fresh", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BANK +44.5%/24h +169.7%/7d - overextended, volume ratio 0.33x", "TRUMP price 1.631 just above entry_high 1.6263 - marginal, not extended", "ETH waiting_for_entry, not yet chased"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["6 open_actionable (triggered, not expired)", "5 waiting_for_entry", "2 entered_unresolved past expiry (ALLO scalp sig_376be7 expired 02:26; NEAR scalp tp1_hit expired 07-17 15:56, still open 36h+ later)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["correlation_cluster", "headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO: 4 concurrent signals across scalp/intraday(x2)/swing - single-symbol correlation cluster", "BANK: 3 concurrent signals across scalp/swing/intraday - single-symbol correlation cluster", "Iran/Hormuz geopolitical tail risk verified externally, ongoing into Asia session"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "repeated_losses"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto_swing_narrative_rs_momentum (TRUMP/LTC): 14d WR 72%/PF 5.80/+24R - strongest cohort", "crypto_intraday_catalyst_or_momentum no-catalyst variant (ALLO/BANK): 14d WR 23%/PF 0.70/-3R - known losing cohort, same setup that stopped TRUMP out Saturday", "week signal-stats: mode=scalp PF 0.167 (losing), direction=short PF 0.20 (losing), weekend=Y PF 0.74/avgR -0.065 (losing) - most active signals are weekend-mode"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate": { "symbol": "TRUMP/USDT", "trigger": "already triggered at 1.6158-1.6263, current 1.631 - hold/add only on pullback into zone, invalidation 1h close below 1.604", "reason": "strongest playbook this run (WR72%/PF5.80/+24R), RS-leader, not extended, OI confirms trend" },
    "best_short_candidate": { "symbol": "ONDO/USDT", "trigger": "clean break + retest failure below 24h low, currently price down + OI down (deleveraging) - no B-tier signal live yet, watch for a fresh short trigger", "reason": "weakest RS symbol on desk (-10.24%/24h, -11.53% RS vs BTC), derivatives confirm long liquidation, RWA narrative rising elsewhere masks ONDO's own weakness" },
    "best_catalyst_candidate": { "symbol": "ETH/USDT", "trigger": "waiting_for_entry 1,855.44-1,858.65, invalidation 1,851.53", "reason": "Bitmine institutional accumulation verified externally (4.8% of ETH supply, ongoing), major-pair lower single-asset risk, not yet chased" },
    "avoid_candidate": { "symbol": "BANK/USDT", "reason": "+44.5%/24h +169.7%/7d with no verified catalyst and weak volume confirmation (0.33x) - classic chase risk; already has 3 concurrent signals stacked on it" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale (stocks only) | advisory_only |
| market_regime | caution | 0.55 | risk_on, mixed | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.40 | oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, entry_fresh, overextended | advisory_only |
| execution_lifecycle | caution | 0.70 | open_actionable, waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.60 | correlation_cluster, headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, repeated_losses | advisory_only |
| head_trader | watch_only | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-18_1840.md` (18:48 EEST Sat), which flagged TRUMP stopped out at -1R and a fresh ALLO intraday long as the one open caution.

- **New since then:** TRUMP re-entered (new signal_id, different from the one that stopped out), LTC/USDT new (same swing playbook as TRUMP), ETH/USDT new (catalyst-backed intraday), XEC/USDT and ETHFI/USDT new (swing, no catalyst), BANK/USDT expanded to 3 concurrent signals (was 0), ALLO/USDT expanded to 4 concurrent signals (was 1).
- **Resolved/dropped:** ONDO/USDT (was tp2_hit at last review) no longer in the active list - fully closed.
- **Unchanged/still open:** NEAR/USDT scalp short still shows `tp1_hit`, now over 36h past its 2026-07-17 15:56 expiry with no final resolution - needs_review (see §14 TODO-2).
- **Thesis continuity risk:** the prior review's core caution - "ALLO is structurally the same no-catalyst setup that just cost TRUMP -1R" - has **not been resolved, it has multiplied**: ALLO now has 4 live signals instead of 1, still in the same 14d WR23%/PF0.70/-3R cohort.

## 5. Catalyst Coverage

- Total catalyst_events today: **998**. Mapped (symbol present): **291**. Unmapped: **707** (**70.8%**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- narrative_baskets: 5 (`ai_narrative`, `perps_dex_narrative`, `delisting_thin_liquidity`, `rwa_narrative`, `binance_ecosystem_teaser`).
- Top unmapped headlines (sample): a memecoin-surge/crash post referencing a public figure's avatar change; a generic engagement poll; a GENIUS Act anniversary macro piece; a CLARITY Act legislative update; a tokenization-thesis quote from a public-company CEO.
- **`ai_narrative` basket integrity issue**: primary_symbols lists `NEAR/USDT` with catalyst_summary citing an Iran-conflict headline as a "sample headline" — this is the false-positive substring match described in §14 TODO-1, not genuine AI-sector catalyst support for NEAR.

## 6. Market Landscape

BTC and ETH are both in a technical uptrend (57.9% of tracked alts above EMA20, 52.6% above EMA50), and the internal regime classifier reads **bullish trend / risk-on**. External verification, however, surfaces a live and verified macro overhang: **day six of US airstrikes on Iran, the Strait of Hormuz closed, oil prices up, and the crypto Fear & Greed Index sliding from 27 to 25** — BTC and ETH both pulled back from local highs ($65k/$1,900 resistance) on Friday specifically on this news before partially recovering. The technical regime and the macro-sentiment regime are **not fully aligned** right now; treat the "risk-on" label as fragile rather than confirmed, especially into the Asia session where headline-driven volatility on this conflict is most likely to land.

### Market Mood / Risk Routing
- Crypto mood: **mixed — technically risk-on, macro/geopolitically fragile**
- Stocks mood: **closed (weekend)**
- Dominant narrative: RWA (heat 58.1/100, rising, led by ONDO — but ONDO itself is the weakest symbol on the desk right now, a narrative/price divergence); Bitmine/ETH institutional accumulation (verified, ongoing); AI narrative basket is currently **contaminated** by the NEAR mistagging bug and should not be trusted this cycle.
- Preferred side now: **longs, but selective — RS-leader/catalyst-backed only, not the extended no-catalyst momentum names**
- Best long candidate: **TRUMP/USDT** (see §8)
- Best short candidate: **ONDO/USDT** (watch-only, no live signal yet — see §8)
- Best catalyst-backed candidate: **ETH/USDT** (see §8)
- What to avoid: **BANK/USDT** (chase risk) and **adding further ALLO/USDT exposure** (already 4-deep in a historically -3R cohort)
- What would change the view: a de-escalation headline on the Iran/Hormuz conflict would likely re-confirm the bullish technical regime and make the no-catalyst momentum names (ALLO/BANK) safer to hold; a further escalation (e.g. a shipping incident in the Strait) would likely invalidate the current longs regardless of individual technicals

## 7. Candidate Deep Dives

### 7.1 TRUMP/USDT — LONG (best long candidate)
- Signal: `sig_ed642be146198f27`, B-tier swing, score 68.9, status `triggered`, entry 1.6158-1.6263, current price 1.631, invalidation 1h close below 1.604, TP1/2/3 1.654/1.678/1.701.
- Playbook: `crypto_swing_narrative_rs_momentum` — 14d WR 72% / PF 5.80 / +24R, the strongest cohort on the desk this run.
- Has price already reacted? Slightly — current price (1.631) is just above the top of the entry zone (1.6263), a marginal/fresh trigger, not a chase.
- Retest/pullback structure? Entry plan explicitly wants pullback into zone; price is right at the edge.
- Overextended (>2 ATR from EMA20)? No — RR to TP1 is 2.02R, ATR 0.0234, well within normal range.
- Aligned with market mood? Yes for the technical regime; carries the same geopolitical tail risk as everything else tonight.
- Actionable now or after confirmation? Already triggered; treat as actionable but size for the Iran-headline tail risk.
- Invalidation: 1h close below 1.604.
- Chase risk? Low — this is the strongest-stat cohort and not extended.
- Catalyst: none verified — this is a pure RS/momentum play, not catalyst-backed. Note this signal replaces one on the same symbol that **stopped out for -1R Saturday afternoon** — same symbol, new signal_id, same playbook; treat as a fresh independent trade, not a martingale re-entry.

### 7.2 LTC/USDT — LONG (correlated with TRUMP)
- Signal: `sig_8b5f4f60d2db9585`, B-tier swing, score 67.5, status `triggered`, entry 46.618-46.848, invalidation 1h close below 46.337, TP1/2/3 47.461/47.971/48.482.
- Same playbook as TRUMP (`crypto_swing_narrative_rs_momentum`, WR72%/PF5.80/+24R). RS vs BTC +2.68%, OI +14.24% (fresh positioning, crowding normal), volume ratio 0.67x.
- No fresh catalyst; global long/short ratio flagged as "heavily long skewed" in the counter-thesis — a mild crowding warning even though the derivatives read says "normal."
- **Correlation note**: TRUMP and LTC are both long, both swing, both on the same playbook, both no-catalyst RS plays. A BTC dump invalidates both simultaneously — this is not two independent bets, size accordingly.

### 7.3 ETH/USDT — LONG (best catalyst-backed candidate)
- Signal: `sig_771d50b27f45d674`, B-tier intraday, score 65.4, status `waiting_for_entry`, entry 1,855.44-1,858.65, invalidation 1,851.53.
- Catalyst: **verified externally** — Bitmine (BMNR) is at 4.8% of ETH's circulating supply as of its July Chairman's Message, actively pursuing a stated "5% of supply by end of 2026" goal via ongoing $35-123M transactions; internal `news_items` independently picked up the same story within the last 24h (CryptoBriefing + t.me/cointelegraph, both 2026-07-18 ~21:30-21:38 UTC).
- Not yet triggered — no chase risk. This is the cleanest catalyst-confirmed setup on the desk tonight, on a major pair (lower idiosyncratic risk than the alt cluster below).
- Caveat: same Iran/Hormuz macro overhang applies; ETH specifically pulled back from $1,900 resistance to ~$1,832-1,840 externally on Friday's escalation.

### 7.4 BANK/USDT — AVOID (chase risk / correlation cluster)
- Three concurrent signals: scalp `sig_fe9e05bc25e31c7d` (waiting_for_entry), swing `sig_d02970b63aaa8f08` (waiting_for_entry), intraday `sig_8e0a3fd89f698b81` (triggered).
- 24h return **+44.5%**, 7d return **+169.7%** — already vertical. Volume ratio only 0.33x vs 20-period average — the move is not backed by proportional volume.
- Playbook: `crypto_intraday_catalyst_or_momentum`, no-catalyst variant — 14d WR 23% / PF 0.70 / -3R, the desk's known losing cohort.
- No fresh verified catalyst in `news_items` (0 matches in 24h). Derivatives read is MEXC-fallback only (funding 5e-05, OI n/a) — low confidence.
- Report's own counter-thesis explicitly flags this as watchlist/no-trade-quality ("Score is below active-trade threshold") even though the DB shows live triggered/waiting signals on it.
- **Verdict: avoid new entries.** If already in a BANK position, treat as a trim/tighten candidate rather than an add — three concurrent stacked signals on one already-extended, no-catalyst, low-volume name is a correlation cluster, not diversification.

### 7.5 ALLO/USDT — AVOID / CAUTION (repeat of the exact cohort that stopped TRUMP out)
- Four concurrent signals: swing `sig_066727806332fc5e`, intraday `sig_cc270aceaa0df23d`, scalp `sig_376be709937f55ab` (now past expiry, unresolved), intraday `sig_10088a4c71cae845`.
- Same `crypto_intraday_catalyst_or_momentum` no-catalyst playbook as BANK — WR 23% / PF 0.70 / -3R (14d). 24h return +14.47%, 7d +21.11%, volume ratio only 0.13x (very thin).
- The prior review (18:48 Sat) already flagged this exact setup type as "structurally the same as the trade that just cost TRUMP -1R." Since then the desk has **added three more ALLO signals** rather than fewer. This is the clearest case of an unresolved caution point recurring and compounding — surfaced as a TODO (§14 TODO-4) rather than acted on, per the read-only mandate.
- **Verdict: do not add further ALLO exposure. If already in, this is the top trim candidate alongside BANK.**

## 8. Best Candidates Ranked

1. **TRUMP/USDT — LONG** (best long-watch): triggered 1.6158-1.6263, current 1.631, invalidation below 1.604, strongest playbook stats on the desk.
2. **ETH/USDT — LONG** (best catalyst-watch): waiting_for_entry 1,855.44-1,858.65, invalidation 1,851.53, Bitmine accumulation verified.
3. **LTC/USDT — LONG**: triggered 46.618-46.848, invalidation below 46.337, same playbook as #1, correlated — treat as shared risk with TRUMP, not independent size.
4. **ONDO/USDT — SHORT-WATCH** (no live signal yet): weakest symbol on the desk (-10.24%/24h, -11.53% RS vs BTC), derivatives show price-down+OI-down (deleveraging/long liquidation). Trigger: clean breakdown + failed retest of the prior 24h low with confirming volume. Do not short into strength — RWA narrative elsewhere is rising, so this needs its own confirmation, not a basket-wide short.
5. **BANK/USDT & ALLO/USDT — AVOID / no new entries**: both chase-risk, no-catalyst, correlation-clustered (3 and 4 concurrent signals respectively).

## 9. Avoid / No Trade

This applies to the current decision window only — scanning, tracking, and the scheduler continue uninterrupted regardless.

- **New BANK/USDT entries**: overextended (+44.5%/24h), thin volume, no catalyst, already 3-deep.
- **New ALLO/USDT entries**: same losing cohort (WR23%/PF0.70/-3R) that already cost the desk -1R on TRUMP Saturday, already 4-deep.
- **Any short entry generically**: direction=short is the week's weakest cohort overall (PF 0.20, 1W/7L) — the ONDO idea above is a watch-trigger, not a green light to short broadly.
- **New scalp-mode entries generically**: mode=scalp is the week's weakest mode (PF 0.167, 0W/7L) — NEAR's already-tp1_hit scalp short is a legacy position, not a template to repeat.

## 10. Main Risks

1. **Geopolitical tail risk (verified, live)**: US-Iran conflict day six, Strait of Hormuz closed, oil rising. Directly suppressed BTC/ETH Friday and could resume doing so at any point in the Asia session with no internal warning — the internal regime classifier has no macro/geopolitical input and will lag a fresh headline.
2. **Correlation clustering**: 7 of 13 active crypto signals sit on just two symbols (ALLO ×4, BANK ×3), both in the desk's known-losing no-catalyst momentum cohort. This concentrates risk far more than the signal count suggests.
3. **Weekend-mode drag**: signal-stats show weekend=Y cohort at PF 0.74 / avgR -0.065 (1W/10L) vs weekend=N at PF 1.33 / avgR +0.096 — most of tonight's active signals are tagged weekend=Y.
4. **Catalyst mapping degraded (70.8% unmapped)**: the catalyst layer is directionally useful (RWA/AI/perps themes visible) but should not be trusted for precise symbol-level catalyst confirmation this cycle — compounded by the NEAR mistagging bug in §14 TODO-1.
5. **Lifecycle hygiene**: NEAR scalp short (`tp1_hit`) has been unresolved for 36+ hours past its stated expiry with no closing record visible in active-signals — a minor data-hygiene gap, not a live risk, but worth a maintenance pass (§14 TODO-2).

## 11. Action Plan — next 4 hours

- Hold TRUMP/LTC swing longs as-is; no new adds unless a clean pullback retest forms — they are correlated, treat combined size as one bet.
- Let ETH's `waiting_for_entry` play out at 1,855.44-1,858.65; do not chase above the zone.
- Do not open new BANK or ALLO positions. If discretionary review of existing BANK/ALLO exposure happens, bias toward trimming rather than holding through the Asia window given the correlation stacking.
- Watch ONDO for a clean breakdown/failed-retest short trigger; no entry until that confirms.
- Monitor Iran/Hormuz headline flow through the Asia session — it is the single most likely source of a regime-invalidating surprise tonight, more than any individual signal's technicals.
- Re-check at the 11:30 EEST Europe slot for whether the geopolitical overhang has eased or escalated, and whether the ALLO/BANK cluster has resolved (TP/stop) on its own.

## 12. Final Verdict per Mode

- **Scalp**: avoid new entries — weakest mode this week (PF 0.167).
- **Intraday**: selective only — ETH (catalyst-backed) is fine to let trigger; avoid the no-catalyst ALLO/BANK intraday legs.
- **Swing**: preferred mode this cycle — TRUMP/LTC on the strongest playbook (PF 5.80); hold, don't add correlated size.
- **Stocks (all modes)**: closed, planning-only. Prior data is 2-17 days stale depending on report; nothing actionable until Monday's US session.

## 13. Sources

- [Bitmine Chairman Message: 4.8% of Ethereum Supply | BMNP Stock News](https://www.stocktitan.net/news/BMNP/bitmine-immersion-technologies-bmnr-releases-july-chairman-s-message-x4gvc8xykaym.html) — 2026-07 (July Chairman's Message)
- [Bitmine acquires additional 6,000 Ethereum for $11M as total holdings near 5% of total supply](https://cryptobriefing.com/bitmine-acquires-6000-ethereum-11-million/) — 2026-07-18 (also independently captured in internal `news_items`)
- [Bitcoin and ethereum prices today, Friday, July 17, 2026: Prices ease as conflict in Iran escalates](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-july-17-2026-prices-ease-as-conflict-in-iran-escalates-125602208.html) — 2026-07-17, verified via WebFetch (sixth day of US airstrikes on Iran, Strait of Hormuz closed, BTC/ETH pulled back from $65k/$1,900 resistance)
- Internal: `t.me/cointelegraph`, `CryptoBriefing` (2026-07-18 ~21:30-21:38 UTC) — ETH/Bitmine story, cross-checked against external sources above.

## 14. Fix Requests / TODO

### TODO-1: news/symbol detector false-tags NEAR/USDT on unrelated geopolitical headlines, corrupts narrative_baskets
- **issue:** the symbol detector appears to match the literal substring "near" (case-insensitive) inside headline text and tags it as `NEAR/USDT`, independent of actual token relevance. Confirmed on an Iran-conflict headline ("AREA NEAR HAJIABAD IN SOUTHERN IRAN") from `t.me/marketfeed`, published 2026-07-19T00:32:36Z, `detected_symbols_json = ["NEAR/USDT"]`. This propagated into today's `ai_narrative` narrative basket, which lists `NEAR/USDT` as a primary symbol with a catalyst_summary citing that same Iran headline as a "sample headline."
- **evidence:** `db/crypto_ai_desk.sqlite`, `news_items` table, `published_at='2026-07-19T00:32:36+00:00'`, `source='t.me/marketfeed'`; `data/catalysts/2026-07-19/narrative_baskets.jsonl`, `basket_name='ai_narrative'`.
- **suggested manual fix:** audit the symbol-detection regex/matcher for word-boundary and stopword handling around common English words that collide with ticker symbols (NEAR, ONE, FLOW, RUNE, etc. are all real tickers and common words). Add a denylist or require additional context (e.g. "$NEAR" or "NEAR Protocol") for ambiguous short tickers.
- **priority:** high
- **first observed:** 2026-07-19 04:40 EEST

### TODO-2: NEAR/USDT scalp short (`sig_b16bb9e54598333a`) unresolved 36+ hours past expiry
- **issue:** signal status shows `tp1_hit`, `expires_at=2026-07-17T15:56:12`, still appearing in `active-signals` output as of 2026-07-19 04:40 (36+ hours past expiry) with no closing/resolution record visible via the CLI.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` output, row `sig_b16bb9e54598333a`.
- **suggested manual fix:** investigate whether the structural TP/stop refresh or paper execution accounting job is failing to finalize expired `tp1_hit` positions, or whether this is expected pending-close behavior; if expected, consider surfacing a distinct "past-expiry pending-close" status so it doesn't read as ambiguous in reviews.
- **priority:** medium
- **first observed:** 2026-07-19 04:40 EEST

### TODO-3: no review artifact produced for the 21:30 and 23:15 EEST slots on 2026-07-18
- **issue:** the most recent prior review before this one is `OPUS_ENRICHED_REVIEW_AUTO_2026-07-18_1840.md` (18:48 EEST). No `OPUS_ENRICHED_REVIEW_AUTO_*`, `_DEFERRED_*`, or `_BLOCKED_*` file exists for the nominal 21:30 or 23:15 Saturday slots — a silent gap rather than a logged defer/block.
- **evidence:** directory listing of `OPUS_ENRICHED_REVIEW_*.md` at project root — no file with a `2026-07-18_21*` or `2026-07-18_23*` / `2026-07-19T00*` timestamp.
- **suggested manual fix:** check the scheduled-task dispatcher/cron logs for `opus-enriched-review-postclose` (23:15 slot) and the late-session 21:30 sibling task around those windows on 2026-07-18 for a crash, timeout, or misfire, since neither a normal review nor a defer/block artifact was written.
- **priority:** medium
- **first observed:** 2026-07-19 04:40 EEST

### TODO-4: ALLO/USDT and BANK/USDT correlation clusters recurring and compounding across review cycles
- **issue:** the 18:48 EEST Saturday review already flagged a fresh ALLO intraday long as "structurally the same no-catalyst setup that just cost TRUMP -1R." Rather than resolving, the desk added 3 more ALLO signals (now 4 total) and 3 BANK signals (now 3 total) overnight, all in the same historically negative (14d WR23%/PF0.70/-3R) no-catalyst momentum cohort.
- **evidence:** `signal-stats --asset-class crypto` (mode breakdown), `active-signals --asset-class crypto` (13 rows, 7 of which are ALLO/BANK).
- **suggested manual fix:** consider whether the `crypto_intraday_catalyst_or_momentum` no-catalyst variant should have a per-symbol concurrent-signal cap, or whether its entry threshold needs tightening given the persistent -3R 14d track record — this is a scoring/gating question for a human-driven session, not something this read-only review can change.
- **priority:** medium
- **first observed:** 2026-07-19 04:40 EEST
