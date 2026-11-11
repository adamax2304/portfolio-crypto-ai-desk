# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:28 EEST

## 1. Executive Summary

**Slot: pre-US-open decision review (nominal 16:20 EEST, ~10 min before the 09:30 ET cash open) — advisory only / no auto-trade.** This is the final pre-open read: gap risk, overnight/pre-market catalysts, and which stock A/B setups are actionable once the session opens vs which need first-15-30min confirmation.

**Scheduler healthy, all data fresh.** Active folder `2026-07-13_default_schedule`, `cycle_01` finished cleanly at 14:57 EEST (started 14:32). Crypto scalp/intraday (14:38/14:44 EEST) and stocks intraday (14:53 EEST) are all fresh this cycle. Crypto swing is carry-forward (~11h50m old, 04:40 EEST) — within the 4-12h window, use with the usual live-price re-check caveat.

**Gap risk has partially eased since the 11:46 review but is not resolved.** Verified pre-market futures as of ~09:20 ET this morning: Dow -0.36% (was -0.43% at 11:46), S&P -0.46% (was -0.58%), Nasdaq -0.91% (was -1.37%) — all three legs less negative than the morning read, but still red into the open. Nasdaq weakness is now more narrowly attributed to memory-chip names (MU, SNDK, SK Hynix's Nasdaq debut) than a broad tech selloff. **The underlying conflict has widened, not cooled**: overnight Iran retaliated with strikes against Kuwait, Jordan, and Qatar (sirens in Bahrain, Jordan intercepted 4 missiles) even as Brent crude pushes toward $80. VIX remains low-to-mid-teens (15-16), i.e. the tape is pricing this as contained, not panic — a genuine tension between "conflict is spreading geographically" and "equity/vol markets aren't (yet) treating it as systemic." The desk's own stocks-intraday regime label is still `risk_on` (VIX 16.27, breadth 100%, unchanged from 11:46's VIX 15.03/breadth 100%) and still produces the same **8 A-tier long candidates (META, DIA, AVGO, NVDA, TSLA, QQQ, AMD, SPY)** — all correctly demoted to C pre-open. **Do not treat Friday's-data A-tier scores as pre-cleared at the open; demand the first 15-30min of RTH price action to confirm the tape is holding, given the geopolitical widening.**

**Crypto remains short-biased, one fresh actionable-adjacent idea.** BTC `transition_down`, ETH `range`, altcoin breadth improved slightly to 40% above EMA20 (was 30% at 11:46) but style is still "short bias or no trade." The only fresh signal this cycle is **HYPE/USDT intraday short (B-tier, score 65.0)**, alerted 14:44 EEST, currently `waiting_for_entry` (entry zone 65.376-65.681, price at read-time 65.24 — below the zone, not yet triggered).

**EVAA/USDT (prior review's best short-watch) has dropped out of today's top-40 universe entirely** — no longer appears in the fresh scalp or intraday reports, so its unwind/retest thesis cannot be re-verified this cycle; treat as stale, not a live candidate until it resurfaces with fresh data (see §4, §14).

**ZEC/USDT catalyst thesis intact but level is 12h-stale.** Zcash Orchard-flaw scrutiny + Forbes Top-10 placement is still showing fresh in both of today's crypto reports; the conditional pullback zone (526.38-530.08, invalidation 521.86) is unchanged from the 04:40 EEST swing snapshot and needs live-price re-verification before treating as actionable.

**MSFT securities-fraud legal risk remains dormant but standing** (Aug 11 2026 lead-plaintiff deadline) — no live candidate today, route AVOID/MANUAL REVIEW immediately if it resurfaces. **JPM earnings tomorrow (2026-07-14)** — swing-blocked, do-not-chase, unchanged; also filed a routine 424B2 prospectus supplement today (informational, not a legal-risk item).

**Catalyst mapping continues to regress**: 85.0% unmapped (2511/2954) today, worse than 11:46's 81.5% and 04:44's 83.2% — a persistent, worsening resolver gap (see §14).

**Overall verdict: CAUTION, routed by side — not a blanket no-trade.** Crypto: short-biased, watch HYPE/USDT (waiting for entry) and ZEC/USDT (catalyst, needs live re-verify). Stocks: wait for RTH confirmation before trusting the A-tier long book; the conflict widening argues for a cautious first 15-30min even though futures have partially recovered from the morning low. Scanning, tracking, and the paper book continue uninterrupted in every mood.

## 2. Data Used

- Crypto scalp report: **fresh** — `2026-07-13_11-38_scalp_report.md` (generated 14:38 EEST; data as of 11:30 UTC). No A/B; regime bearish trend (risk-off), scalp remains kill-switch disabled.
- Crypto intraday report: **fresh** — `2026-07-13_11-44_intraday_report.md` (generated 14:44 EEST). 1 B-tier idea (HYPE/USDT short, actionable, currently waiting_for_entry).
- Crypto swing report: **carry-forward, ~11h50m old** — `2026-07-13_01-40_swing_report.md` (generated 04:40 EEST, data as of 01:30 UTC). Regime at the time: "transition (mixed)". ZEC/DEXE/LAB pullback zones quoted below are from this snapshot — re-check against live price before acting.
- Stocks intraday: **fresh** — `2026-07-13_11-53_stocks_intraday_report.md` (generated 14:53 EEST). Regime risk_on (VIX 16.27, breadth 100%), 8 A-tier + 7 B-tier candidates, all demoted to C by `market_closed_intraday_planning_only`. Stocks swing/invest: last generated 2026-07-02, ~11 days stale, known-deprecated legacy mode, not evaluated.
- Catalysts: `data/catalysts/2026-07-13/catalyst_events.jsonl` (2954 events cumulative today, direct count) + `narrative_baskets.jsonl` (3 active baskets as of the 14:44 EEST cycle: `perps_dex_narrative`/HYPE, `delisting_thin_liquidity`, `rwa_narrative`/ONDO+XLM). Mapped/unmapped computed directly from the JSONL (see §5).
- LLM packets: `data/processed/llm_analysis_packet.md` (crypto, refreshed 14:44 EEST) and `data/processed/llm_stocks_packet.md` (stocks, refreshed 14:54 EEST).
- CLI: `active-signals --asset-class crypto` (26 rows, all B-tier, all `tp1_hit`/`tp2_hit`/`waiting_for_entry` [HYPE only] — nothing new besides HYPE), `active-signals --asset-class stocks` (50 rows, all C-tier or legacy A/B, all historical tp/triggered outcomes from Jul 3-11 — nothing fresh today), `signal-stats` both asset classes (week), `detect_untracked_legacy_alerts --since 2026-07-13` (0 found).
- DB / logs (read-only): `data/scheduled_runs/2026-07-13_default_schedule/scheduler.log` (`cycle_01` clean finish 14:57 EEST, started 14:32); `reports/PAPER_MONITOR_STATUS_LATEST.md` (14:56 EEST — lifecycle counts, see §3); `obsidian_vault/11_Trade_Journal/Daily_Reviews/2026-07-13.md` (auto-generated 14:56 EEST — today's alert history and the standing MSFT legal-risk block).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_1146.md` (11:46 EEST, ~4h40m ago) — primary comparison baseline for §4.
- External: 3 WebSearch queries (US stock futures pre-market July 13 2026; Iran/Strait of Hormuz latest; BTC/ETH price today) + 1 WebFetch (Yahoo Finance futures live-blog, verified levels/VIX/oil/JPM-earnings context) — sources in §13.

## 3. Scheduler / Data Freshness

- `scheduler.log` (`2026-07-13_default_schedule`): `cycle_01` started 14:32 EEST, finished cleanly 14:57 EEST — **fresh, not deferred**.
- Crypto scalp/intraday: **fresh** this cycle (generated 14:38-14:44 EEST, data as of 11:30 UTC).
- Crypto swing: **carry-forward** (~11h50m old, 04:40 EEST) — within the 4-12h window, flagged in §1/§2.
- Stocks intraday: **fresh** (14:53 EEST) but pre-market — planning-only per the report's own banner; not a live regression, will go actionable at/after the 09:30 ET open.
- Untracked legacy crypto alerts: **0** (confirmed this cycle).
- Known non-blocking noise (unchanged, self-documented in every report): Reddit social-attention sources unavailable; Bybit/OKX futures partial coverage; token-unlock/liquidation-heatmap/order-book/on-chain blindspots not automated.
- Paper Monitor Status (14:56 EEST): **Open actionable 0 · Waiting for entry 1 (HYPE/USDT short) · Review/Shadow 99 · Entered unresolved (expired-after-entry) 6 · No-entry/stale/moved-away 55 · Closed 388W / 21L / 0flat · Needs review 0**.
- Today's crypto alert history (Obsidian daily review, 14:56 EEST): 6 B-tier alerts fired today (ZEC scalp long, ETH scalp long, OPN swing short, SOL scalp short, OPN scalp short, HYPE intraday short — the last one is today's only fresh, still-live idea). ZEC/ETH/OPN(scalp) all `close_stop`; VANRY intraday `close_stop`; VELVET intraday `close_tp` (+3R per paper monitor); SOL scalp short `paper_entry` → `close_expired` (entered-unresolved lifecycle, not a missed entry). No A-tier signal fired today.
- MSFT: prior `waiting_for_entry`/stale stocks long still shows `NO_ENTRY` (stale, never touched) — no live position, but the `ACTIVE_LEGAL_HEADLINE_RISK: securities_fraud` block for MSFT remains listed in today's Obsidian daily review.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-13 16:28 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh"],
      "data_missing": ["stocks swing/invest (~11 days stale, known deprecated mode)", "EVAA/USDT current derivatives/price (dropped from today's top-40 universe)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_01 started 14:32 EEST, finished cleanly 14:57 EEST (default schedule)", "crypto scalp/intraday fresh (14:38-14:44 EEST); crypto swing carry-forward (~11h50m, 04:40 EEST); stocks intraday fresh (14:53 EEST)", "0 untracked legacy crypto alerts"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.6,
      "reason_codes": ["risk_off", "shorts_preferred", "wait_for_trigger", "mixed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC transition_down, ETH range, altcoin breadth 40% above EMA20 (up from 30% at 11:46), style still 'short bias or no trade'", "stocks: desk labels risk_on (VIX 16.27, breadth 100%, essentially unchanged from 11:46's VIX 15.03); verified pre-market futures still down but less negative than the 11:46 read (Dow -0.36% vs -0.43%, S&P -0.46% vs -0.58%, Nasdaq -0.91% vs -1.37%) per Yahoo Finance/CNBC", "Iran-Israel-adjacent conflict has widened geographically (Kuwait/Jordan/Qatar struck overnight) even as futures pricing partially recovered from the morning low — VIX still calm (15-16), a genuine tension between spreading conflict and contained vol pricing"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "catalyst_confirmed", "narrative_supported", "no_catalyst"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl direct count: 2954 total, 443 mapped (15.0%), 2511 unmapped (85.0%) — worse than 11:46's 81.5% and 04:44's 83.2%, a worsening trend", "3 active baskets as of 14:44 EEST: perps_dex_narrative (HYPE primary), delisting_thin_liquidity (no primary), rwa_narrative (ONDO/XLM) — ai_narrative basket seen at 11:46 has rotated out", "ZEC/USDT retains a genuine external catalyst (Orchard pre-disclosure-trading scrutiny + Forbes 2026 Top-10) in both of today's fresh crypto reports, unchanged from 11:46", "EVAA/USDT (11:46's best short-watch) has no catalyst presence and has dropped out of today's fresh reports entirely — cannot re-verify its unwind thesis this cycle"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["data_unavailable", "oi_supports", "squeeze_risk"],
      "data_missing": ["EVAA/USDT current OI/funding (symbol not in today's fresh scanned universe)", "Bybit/OKX cross-check limited to a handful of symbols per report"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HYPE/USDT: external funding neutral (bybit 0.0001), crowding normal — no squeeze flag, consistent with the failed-bounce short thesis", "SXT/USDT: negative funding across external venues (bybit -0.00125), crowding elevated — a short-squeeze risk name to avoid chasing", "VANRY/USDT still capped short_squeeze_risk in the scalp report's rejected list", "ZEC/USDT (04:40 EEST swing snapshot): price up + OI up (+2.14%), modest positive funding — fresh, not crowded, unchanged directionally from 11:46"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["clean_retest", "stale_before_entry", "entry_fresh", "chase_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["HYPE/USDT: current price 65.24 sits just below the preferred failed-bounce/retest entry zone 65.376-65.681; invalidation 1h close beyond 66.053 — a rally into the zone with rejection is required, not a chase of the current print", "ZEC/USDT: pullback zone 526.38-530.08 (12h-stale swing snapshot, invalidation 521.86) — needs live-price re-check before treating as actionable; snapshot price was 531.72, just above the zone", "stocks A-tier longs (META/DIA/AVGO/NVDA/TSLA/QQQ/AMD/SPY): technically strong on Friday's data but the entry decision now hinges entirely on the first 15-30min of RTH price action against a still-negative-but-improving futures tape and a geographically widening conflict — textbook 'wait for confirmation, don't chase the open' setup"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.7,
      "reason_codes": ["waiting_for_entry", "review_shadow", "no_entry", "closed_flat"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Paper monitor (14:56 EEST): Open actionable 0, Waiting for entry 1 (HYPE/USDT short), Review/Shadow 99, Entered unresolved 6, No-entry/stale/moved-away 55, Closed 388W/21L/0flat, Needs review 0", "Today's alert history: ZEC/ETH/OPN(scalp) close_stop; VANRY intraday close_stop; VELVET intraday close_tp (+3R); SOL scalp entered-unresolved (close_expired); HYPE intraday short is the day's only still-live idea", "MSFT prior stocks long still NO_ENTRY (stale, never touched) — no live position", "26 crypto active-signals rows, 25 already tp1/tp2_hit, 1 (HYPE) waiting_for_entry"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT: verified active securities fraud class action (Aug 11 2026 lead-plaintiff deadline) — dormant today (no live signal, no fresh catalyst) but must route AVOID/MANUAL REVIEW if it resurfaces", "JPM: earnings tomorrow (2026-07-14), swing-blocked + do-not-chase-warning already active in production; filed a routine 424B2 prospectus supplement today (informational, not legal risk)", "Geopolitical: verified Iran retaliation has widened to strikes on Kuwait, Jordan, and Qatar overnight (sirens in Bahrain, Jordan intercepted missiles) even as Brent nears $80 and futures have partially recovered from the morning low — the open carries real headline-risk even though the desk's own regime label and VIX both currently read calm"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week headline A/B: winrate 13.4%, PF 1.03, avgR 0.012, totalR +2.0 — broadly unchanged in character from the 11:46 read (12.6%/0.96)", "by mode: scalp still worst (PF 0.32 in this cycle's report window), intraday mild negative (PF 0.99), swing best (PF 1.41, +9.1R)", "weekend-mode signals continue outperforming weekday this week (PF 3.29 vs 0.63, per signal-stats)", "stocks headline A/B anecdotal (n=6, PF 1.19, +0.57R); stocks C-tier watchlist PF 0.71, winrate 14.4%, week totalR -11.3 — weak but not Telegram-actionable, unchanged"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.55,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.55,
    "preferred_side": "shorts_preferred",
    "best_long_candidate":     { "symbol": "none clean in crypto; stocks A-tier longs (NVDA/AVGO/META) watch-only", "trigger": "first 15-30min RTH price action holding/reclaiming Friday's close despite the still-negative-but-improving futures tape and widening regional conflict" },
    "best_short_candidate":    { "symbol": "HYPE/USDT (waiting_for_entry, do not chase)", "trigger": "rally into failed-bounce/retest zone 65.376-65.681 with rejection, hold below invalidation 66.053" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "fill on live-re-verified pullback into ~526-530 zone, hold above ~522; catalyst (Orchard scrutiny + Forbes Top-10) still fresh today" },
    "avoid_candidate":         { "symbol": "MSFT (if it resurfaces) + chasing any stock A-tier long in the first minutes of the open", "reason": "MSFT carries an active securities fraud class action (Aug 11 2026 deadline); stock A-tier longs are scored on stale pre-weekend data against a still-negative futures tape and a geographically widening Iran conflict" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh | advisory_only |
| market_regime | mixed | 0.60 | risk_off, shorts_preferred, wait_for_trigger, mixed | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, catalyst_confirmed, narrative_supported, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | data_unavailable, oi_supports, squeeze_risk | advisory_only |
| technical_entry | caution | 0.55 | clean_retest, stale_before_entry, entry_fresh, chase_risk | advisory_only |
| execution_lifecycle | ok | 0.70 | waiting_for_entry, review_shadow, no_entry, closed_flat | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.55 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Comparison baseline: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_1146.md` (11:46 EEST, ~4h40m ago).

- **Gap risk partially eased, not resolved:** verified pre-market futures have improved from the 11:46 read (Dow -0.43%→-0.36%, S&P -0.58%→-0.46%, Nasdaq -1.37%→-0.91%) — still red into the open but less severe. Nasdaq weakness is now specifically tied to memory-chip names (MU, SNDK, SK Hynix) rather than a broad tech rout.
- **Underlying conflict widened, not cooled:** overnight Iran retaliated with strikes on Kuwait, Jordan, and Qatar (new this cycle — not in the 11:46 review, which only had the weekend's US-Iran/Hormuz exchange). Oil near $80. VIX still calm (15-16) — the market has not (yet) repriced the wider conflict as systemic risk.
- **EVAA/USDT dropped out entirely:** the 11:46 review's best short-watch (a live -27% unwind at the time) no longer appears anywhere in today's fresh scalp/intraday top-40 universe — its momentum/RS ranking has apparently decayed below the discovery threshold. Cannot confirm current price/OI this cycle; treat the prior thesis as stale until it resurfaces with fresh data (see §14).
- **New fresh signal:** HYPE/USDT intraday short (B-tier, score 65.0) fired at 14:44 EEST — this is the day's only fresh alert and is now the best short-watch, replacing EVAA.
- **Crypto breadth modestly improved:** altcoin breadth above EMA20 is now 40% (was 30% at 11:46) — still thin, still short-biased per the desk's own style recommendation, but less deteriorated.
- **Catalyst mapping regression continues:** 85.0% unmapped today vs 81.5% at 11:46 and 83.2% at 04:44 — the gap is now trending worse cycle over cycle, not better (see §14, priority raised).
- **Stocks A-tier book unchanged in composition:** same 8 names (META, DIA, AVGO, NVDA, TSLA, QQQ, AMD, SPY) still score A, still demoted to C pre-open — no new stock candidate emerged this cycle.
- **ZEC/DEXE/LAB:** thesis and zones unchanged from 11:46 (both reference the same 04:40 EEST swing snapshot) — needs the next swing refresh or a live-price check before acting.
- **MSFT:** unchanged (dormant, AVOID/MANUAL REVIEW if it resurfaces). **JPM:** unchanged (no-chase into tomorrow's earnings), plus a routine 424B2 filing noted today (non-material to the legal-risk thesis).

## 5. Catalyst Coverage

- Total `catalyst_events` today (JSONL, direct count, cumulative): **2954**.
- Mapped (non-null symbol): **443** (15.0%).
- Unmapped (null symbol): **2511** (85.0%).
- `narrative_baskets` active as of the 14:44 EEST cycle: **3** — `perps_dex_narrative` (HYPE/USDT primary), `delisting_thin_liquidity` (no primary), `rwa_narrative` (ONDO/USDT, XLM/USDT).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (85.0% unmapped, well above the 50% threshold; worse than both the 11:46 review's 81.5% and the 04:44 review's 83.2% — a worsening trend, not a one-off blip.)
- Top 3 unmapped headlines (sample): "Maximum Leverage Adjusted for BLASTUSDT Futures", "Adjustment to BLASTUSDT Funding Rate Settlement Frequency", "Adjustment to PARTIUSDT Funding Rate Settlement Frequency" — all exchange-notice boilerplate carrying a literal `<TICKER>USDT` substring that the resolver still fails to map, consistent with the persistent TODO from prior reviews.
- This continues to be a resolver-coverage issue, not a signal-quality issue.

## 6. Market Landscape

Crypto remains in a short-biased, low-breadth regime: BTC `transition_down`, ETH `range`, altcoin breadth 40% above EMA20 (modest improvement from 30% at 11:46), scalp and intraday both still explicitly recommending "short bias or no trade; avoid weak altcoin longs." The one fresh idea today is HYPE/USDT intraday short (B-tier, waiting for a rally into 65.376-65.681 to fail before it's tradeable — not a chase of the current -2.5%/24h print). EVAA/USDT, last cycle's confirmed unwind story, has fallen out of today's scanned universe entirely and cannot be re-verified — treat it as stale rather than assuming the retest thesis still holds. ZEC/USDT remains the one name with a genuine, repeatedly-verified external catalyst (Orchard-flaw pre-disclosure-trading scrutiny + Forbes 2026 Top-10 placement), unchanged in thesis from the last two reviews; its stated pullback zone (526-530) is now from a ~12h-old snapshot and needs a live-price re-check before treating as actionable. On the stocks side, the desk's own regime read is unchanged at risk_on (VIX 16.27, 100% breadth) and still surfaces the same 8 A-tier longs — but the decision-relevant fact for this slot is that verified pre-market futures, while still negative, have moderated meaningfully since this morning (Nasdaq -1.37%→-0.91%) even as the underlying US-Iran conflict has expanded geographically overnight (strikes reaching Kuwait, Jordan, Qatar). That combination — softening futures against a widening conflict, with VIX still calm — is exactly the setup where the first 15-30 minutes of RTH price action matters more than Friday's score: a clean open that holds argues the desk's risk_on read was directionally right; a fade or a headline-driven air-pocket argues the market is underpricing the regional escalation. JPM's earnings tomorrow (2026-07-14) remains a swing-blocked, do-not-chase name regardless of the open's tone. MSFT's securities-fraud legal risk carries forward but stays dormant (no live signal, no fresh catalyst today).

### Market Mood / Risk Routing

- Crypto mood: **risk-off / short-biased** (BTC transition_down, ETH range, breadth 40% above EMA20, scalp+intraday both still recommend short bias or no trade)
- Stocks mood: **internally risk-on, externally still-negative-but-improving** — desk regime says risk_on (VIX 16.27, breadth 100%), verified pre-market futures still red (Dow -0.36%, S&P -0.46%, Nasdaq -0.91%) though less severe than this morning; regional conflict widened overnight (Kuwait/Jordan/Qatar struck) — treat as **mixed/RTH-confirmation-required**, not pre-cleared
- Dominant narrative: crypto short bias into thin, no-catalyst altcoin weakness (EVAA thesis now stale/unconfirmed, HYPE fresh short); stocks — a real, still-present macro risk-off pulse from an escalating-not-cooling Iran conflict, only partially reflected in the desk's own risk_on label
- Preferred side now: **crypto: shorts on confirmed retest only (HYPE/USDT); stocks: wait for the first 15-30min of RTH price action, do not chase the desk's A-tier longs at the open**
- Best long candidate: none clean in crypto — stocks A-tier longs (NVDA/AVGO/META) are watch-only pending RTH confirmation
- Best short candidate: **HYPE/USDT**, trigger = failed bounce/retest into 65.376-65.681 with rejection, hold below invalidation 66.053 (current price 65.24, below the zone — do not chase the current level)
- Best catalyst-backed candidate: **ZEC/USDT**, trigger = fill on a live-re-verified pullback into ~526-530, hold above ~522, catalyst thesis (Orchard scrutiny + Forbes Top-10) still fresh today
- What to avoid: **MSFT** if it resurfaces (active securities fraud litigation); chasing any of the stock A-tier longs (META/DIA/AVGO/NVDA/TSLA/QQQ/AMD/SPY) in the first minutes of the open given the widening regional conflict; **JPM** ahead of tomorrow's earnings
- What would change the view: a clean RTH open that holds/reclaims Friday's close (supports the desk's risk_on read); a headline-driven air-pocket or a further widening of the Iran/Gulf-states conflict during the session (would argue the market is underpricing the risk); HYPE/USDT actually filling and rejecting its 65.4-65.7 retest zone; ZEC/USDT's zone re-verified against live price

## 7. Candidate Deep Dives

### 7.1 HYPE/USDT — best short-watch, waiting for entry (do not chase)

**Status:** B-tier intraday (score 65.0), the day's only fresh alert (14:44 EEST), currently `waiting_for_entry` per the paper monitor and active-signals CLI. 24h -2.5%, 7d -6.89%. RS vs BTC -0.88%. Volume 1.36x. Derivatives: external funding neutral (bybit 0.0001), crowding normal — no squeeze risk flagged. **Has price already reacted?** Modestly (-2.5%/24h), not extended. **Chasing?** Not at this level — the entry plan explicitly requires a bounce into the zone first. **Retest structure?** Yes — preferred entry is failed bounce/retest into 65.376-65.681; current price 65.24 sits just below that zone, meaning entry hasn't triggered yet (consistent with `waiting_for_entry` status). **Overextended?** No. **Would entry now be late?** No — price hasn't reached the entry zone. **Actionable now or after confirmation?** After the zone is tapped and rejected; not yet. **Aligned with mood?** Yes — fits the desk's own bearish-trend/short-bias regime call. **Invalidates the idea:** 1h close beyond 66.053. **Chase-risk:** low if the stated zone/invalidation are respected; the setup is specifically designed to avoid chasing a "late breakdown into exhausted sellers." **Catalyst confirmation/contradiction:** mild fresh attention (3 catalyst/news items, mostly Hyperliquid-listing chatter), not a directional confirmation either way.

### 7.2 ZEC/USDT — best catalyst-watch, thesis unchanged, level now 12h-stale

**Status:** C-tier watchlist, appearing with a genuine external catalyst in both of today's fresh crypto reports (Zcash Orchard-flaw pre-disclosure-trading scrutiny + Forbes 2026 Top-10 placement), unchanged across the last three reviews (04:44, 11:46, this cycle). 24h +3.8% (fresh scalp/intraday read), 7d +15.76% (12h-old swing read). Derivatives (from the 04:40 EEST snapshot): price up + OI up (+2.14%), modest positive funding — fresh, not crowded; no fresher derivatives read exists this cycle. **Has price already reacted to the catalyst?** Partially — moderate, not extended. **Chasing?** Not at the 24h scale seen today. **Retest structure?** Yes per the (now 12h-old) swing snapshot: conditional pullback zone 526.38-530.08, invalidation 521.86; snapshot price was 531.72 (just above the zone) — this needs a live-price re-check since the next swing refresh hasn't landed yet. **Overextended?** No. **Would entry now be late?** Only if filled without re-verifying the zone against current price. **Actionable now or after confirmation?** After a fill inside a re-verified pullback zone with improving volume (0.42x at last read, below the desk's own confirmation bar). **Aligned with mood?** Reasonably — a catalyst-backed name is the one category the desk's "short bias or no trade" crypto call doesn't automatically veto. **Invalidation:** 1h close beyond ~522 (subject to re-verification). **Chase-risk:** low if the zone is respected and re-verified. **Catalyst confirmation:** confirmed via two independent outlets (AMBCrypto, BeInCrypto), same as prior reviews, not contradicted.

### 7.3 Stocks A-tier long book (META, DIA, AVGO, NVDA, TSLA, QQQ, AMD, SPY) — watch-only, ~10 minutes from the open

**Status:** All 8 score A-tier (81-90) on the desk's own stocks-intraday model, all correctly demoted to C by the `market_closed_intraday_planning_only` gate; this cycle's list is essentially identical to the 11:46 review's (DIA newly A-tier, otherwise unchanged). **Has price already reacted to a catalyst?** These are RS/momentum/breadth-driven scores from Friday's data, not news-driven. **Chasing?** Not applicable pre-open, but treating the A-tier score as a green light in the first minutes would effectively be chasing stale data against fresh overnight escalation. **Retest structure?** Not established — this is a regime-confirmation question, not a technical-level question. **Overextended?** Not evaluated at this granularity in the source report. **Would entry now be late?** N/A pre-open — the question is whether to trust the open at all without waiting. **What makes it actionable?** The first 15-30min of RTH price/volume confirming the desk's risk_on read still holds despite the weekend/overnight escalation having widened (not narrowed) since Friday. **Aligned with mood?** This remains the open question: the desk's internal regime (risk_on, VIX 16.27) and the verified external futures tape (still red, though improved from this morning) partially disagree, while the underlying conflict has gotten geographically broader overnight. **Invalidates the idea:** a weak/gap-down open that fails to reclaim Friday's close on the indices; a fresh Iran/Gulf-states headline during the session. **Chase-risk:** high if any of these are treated as pre-cleared without RTH confirmation. **Catalyst confirmation/contradiction:** partially contradicted by the still-negative (if improving) pre-market futures move and the overnight conflict-widening — not yet reflected in the desk's own regime label (see §14 TODO, carried from 11:46).

## 8. Best Candidates Ranked

1. **Short-watch:** HYPE/USDT — trigger: failed bounce/retest into 65.376-65.681 with rejection, hold below invalidation 66.053. Currently waiting_for_entry; do not chase the current -2.5% print.
2. **Catalyst-watch:** ZEC/USDT — trigger: fill on a live-re-verified pullback into ~526-530, hold above ~522, catalyst thesis intact.
3. **Long-watch (stocks, conditional):** NVDA/AVGO/META — trigger: first 15-30min RTH confirmation that indices hold/reclaim Friday's close despite the still-negative futures tape and overnight conflict-widening; do not treat the A-tier score alone as sufficient.
4. **Stale-watch (not actionable, needs re-verification):** EVAA/USDT — dropped out of today's scanned universe; the 11:46 review's unwind/retest thesis cannot be confirmed this cycle. Do not act on the prior review's levels without fresh data.
5. **Chase-risk watch (not actionable):** DEXE/USDT — pullback zone 47.4-48.2 (12h-old snapshot) still unfilled, still capped "more than 2 ATR from EMA20; do not chase."

No A/B setup is cleanly actionable in crypto at this exact moment beyond HYPE waiting for its trigger — this reflects the current decision window only, not a call to pause the system.

## 9. Avoid / No Trade

- **MSFT (if it resurfaces as a candidate)** — verified active securities fraud class action (Aug 11 2026 lead-plaintiff deadline). No live position right now (prior signal still `NO_ENTRY`), but AVOID/MANUAL REVIEW must apply the moment it re-appears as an A/B candidate, regardless of score.
- **Stock A-tier longs in the first minutes of the open (META/DIA/AVGO/NVDA/TSLA/QQQ/AMD/SPY)** — do not treat Friday's-data scores as pre-cleared; verified futures are still negative (though improved from this morning) and the underlying Iran conflict widened overnight. Demand the first 15-30min of RTH confirmation.
- **HYPE/USDT (chase)** — do not short the current print without waiting for the stated failed-bounce/retest zone (65.376-65.681) to reject.
- **EVAA/USDT** — no longer in today's scanned universe; do not act on the prior review's levels without fresh confirming data.
- **DEXE/USDT (chase)** — still >2 ATR from EMA20 per the last full read; wait for the stated pullback zone and re-verify live price first (snapshot is ~12h old).
- **JPM** — earnings tomorrow (2026-07-14), swing-blocked + do-not-chase warning already active in production.
- This is a decision-window call only — scanning, tracking, and the paper book continue in every mood.

## 10. Main Risks

- **Geopolitical, widening, not cooling:** overnight Iran retaliation reached Kuwait, Jordan, and Qatar (sirens in Bahrain, intercepted missiles over Jordan); Brent crude near $80. Futures have partially recovered from this morning's steepest fear, but VIX (15-16) still reads calmer than the headline flow would suggest — a genuine risk that the market opens underpricing the conflict's scope.
- **Internal/external regime partial mismatch (improved but not closed):** the stocks-intraday desk report still labels the regime risk_on off Friday's data; verified pre-market futures are less negative than this morning but still red. Acting on the desk's A-tier long list without RTH confirmation still risks trusting a score that predates the conflict's overnight widening.
- **Catalyst mapping regression, now trending worse:** 85.0% unmapped today, up from 81.5% (11:46) and 83.2% (04:44) — a persistent resolver gap that has gotten worse across three consecutive cycles today, not stabilized (see §14, priority raised to high).
- **EVAA/USDT data gap:** last cycle's confirmed live-unwind thesis cannot be re-verified this cycle because the symbol dropped out of the scanned top-40 universe — a blind spot for any operator still holding that thesis from the 11:46 review.
- **Stale swing snapshot:** ZEC/DEXE/LAB pullback zones are all quoted from a ~12h-old swing report; live price should be re-verified before treating any of them as actionable once the next swing refresh lands.
- **MSFT legal risk (dormant but standing):** no live position today, but the underlying securities fraud litigation remains active through Aug 11 2026 — must be re-applied if MSFT resurfaces as a candidate.
- **JPM earnings tomorrow:** swing-blocked, do-not-chase in production; today's routine 424B2 filing is non-material to this risk.

## 11. Action Plan — next 4 hours

- Crypto: watch HYPE/USDT for a rally into 65.376-65.681 with rejection before considering the short; do not chase the current level. Watch ZEC/USDT for a re-verified pullback fill into 526-530.
- Do not force a DEXE/USDT entry; it remains chase-risk-capped and its stated zone is from a stale snapshot — wait for the next swing refresh to re-confirm levels.
- Do not carry forward the EVAA/USDT thesis from the 11:46 review without fresh data — it has dropped out of today's scanned universe; re-check at the next scalp/intraday cycle.
- Stocks: at/immediately after the 09:30 ET open, require the first 15-30min of RTH price action to hold/reclaim Friday's close before treating any of META/DIA/AVGO/NVDA/TSLA/QQQ/AMD/SPY as actionable — the futures tape has improved since this morning but the underlying conflict has widened, so this is not a green light by default.
- JPM: no chase ahead of tomorrow's earnings print regardless of any score.
- MSFT: no action needed today (no live signal), but flag for immediate AVOID/MANUAL REVIEW if it resurfaces as a new A/B candidate before Aug 11 2026.
- Operator: no urgent manual action required this cycle; the worsening catalyst-mapping trend and the EVAA data gap are read-model TODOs for a human-driven session (see §14), not live decisions.

## 12. Final Verdict per Mode

- **Crypto scalp:** disabled (kill-switch), no A/B — data collection only; today's alerts (ZEC, ETH, SOL, OPN) all already resolved (mostly stops, one entered-unresolved/expired).
- **Crypto intraday:** WATCH, short-biased — HYPE/USDT is the day's only fresh idea, currently waiting_for_entry; do not chase ahead of the retest.
- **Crypto swing:** WATCH (data ~12h stale) — ZEC/USDT (catalyst-backed) remains the cleanest of the last full snapshot's ideas; DEXE/USDT (chase-risk long) and LAB/USDT (squeeze-capped short) unchanged; re-verify all three against live price at the next refresh.
- **Stocks (all modes):** PRE-MARKET / WATCH-ONLY until the 09:30 ET open; desk regime says risk_on but futures remain net-negative (improved vs this morning) against a geographically widening Iran conflict — require the first 15-30min of RTH confirmation before treating any A-tier long as actionable; MSFT dormant-AVOID if it resurfaces; JPM no-chase into tomorrow's earnings.

## 13. Sources

- [Stock market today: Dow, S&P 500, Nasdaq futures slip as US and Iran exchange fire, oil jumps](https://finance.yahoo.com/markets/live/stock-market-today-monday-july-13-dow-sp-nasdaq-113249278.html) — Yahoo Finance, 2026-07-13 (pre-market futures: Dow -0.36%, S&P -0.46%, Nasdaq -0.91%; VIX 15.03/-5.11%; oil near $80; JPM earnings this week)
- [US Stock Market Prediction Today (July 13): Dow, S&P 500 & Nasdaq Futures Fall as US-Iran Conflict Escalates, Oil Prices Surge Near $80](https://sundayguardianlive.com/business/us-stock-market-prediction-today-july-13-dow-sp-500-nasdaq-futures-fall-as-us-iran-conflict-escalates-oil-prices-surge-near-80-and-investors-await-cpi-ppi-data-big-bank-earnings-235643/) — Sunday Guardian Live, 2026-07-13
- [Nasdaq, S&P 500 Futures Slip As Iran Tensions Rattle Markets Again: Why MU, TSLA, MSFT, TSM Are In Focus](https://finance.yahoo.com/markets/stocks/articles/nasdaq-p-500-futures-slip-084235519.html) — Yahoo Finance, 2026-07-13
- [Live updates: Ceasefire disintegrates as US and Iran trade strikes over Strait of Hormuz](https://www.cnn.com/2026/07/13/world/live-news/iran-war-trump) — CNN, 2026-07-13 (Kuwait/Jordan/Qatar strikes, Bahrain sirens, Jordan intercepted missiles)
- [US and Iran Trade Fresh Strikes, Dispute Whether Hormuz Is Open](https://www.bloomberg.com/news/articles/2026-07-13/us-and-iran-trade-fresh-strikes-dispute-whether-hormuz-is-open) — Bloomberg, 2026-07-13
- [Current price of Bitcoin for July 13, 2026](https://fortune.com/article/price-of-bitcoin-07-13-2026/) — Fortune, 2026-07-13 (BTC ~$63,042 as of 06:15 ET; ETH ~$1,807.80)
- Internal: `data/reports/scalp/2026-07-13_11-38_scalp_report.md`, `data/reports/intraday/2026-07-13_11-44_intraday_report.md`, `data/reports/swing/2026-07-13_01-40_swing_report.md`, `data/reports/stocks/intraday/2026-07-13_11-53_stocks_intraday_report.md`, `data/catalysts/2026-07-13/*`, `data/scheduled_runs/2026-07-13_default_schedule/scheduler.log`, `reports/PAPER_MONITOR_STATUS_LATEST.md`, `obsidian_vault/11_Trade_Journal/Daily_Reviews/2026-07-13.md`.

## 14. Fix Requests / TODO

### TODO-catalyst-symbol-resolver-gap-worsening
- **issue:** Catalyst mapping coverage has worsened across three consecutive cycles today — 83.2% unmapped (04:44) → 81.5% (11:46) → 85.0% unmapped (this cycle, 2511/2954). This is no longer a stable gap; it is trending in the wrong direction intraday.
- **evidence:** `data/catalysts/2026-07-13/catalyst_events.jsonl` — direct count via Python (443 mapped / 2511 unmapped out of 2954). Sample unmapped headlines are exchange-notice boilerplate ("Maximum Leverage Adjusted for BLASTUSDT Futures", "Adjustment to PARTIUSDT Funding Rate Settlement Frequency") carrying a literal `<TICKER>USDT` substring the resolver still fails to map.
- **suggested manual fix:** unchanged core ask from prior reviews (audit the symbol resolver for `<TICKER>USDT`-style substrings in exchange-notice headlines), but escalate priority given the worsening intraday trend — consider whether new event volume (2954 vs 1454 at 11:46, roughly double) is diluting an already-weak resolver rather than the resolver itself regressing.
- **priority:** high (raised from the 11:46/04:44 reviews given the worsening trend)
- **first observed:** recurring across multiple prior reviews; trend-worsening behavior first flagged this cycle, 2026-07-13 16:28 EEST.

### TODO-stocks-regime-vs-external-futures-mismatch-persisting
- **issue:** The stocks-intraday report's internal regime label (`risk_on`, VIX 16.27, breadth 100%) has not changed materially since the 11:46 review (VIX 15.03) despite verified pre-market futures remaining net-negative and the underlying Iran/Gulf-states conflict widening geographically overnight (Kuwait, Jordan, Qatar struck). The gap between internal regime label and external verified tape has narrowed (futures less negative than this morning) but not closed, and the regime classifier still shows no visible sensitivity to the conflict's expansion.
- **evidence:** `data/reports/stocks/intraday/2026-07-13_11-53_stocks_intraday_report.md` §1 (regime risk_on, VIX 16.27) and §5 (8 A-tier candidates); external verification via Yahoo Finance/Sunday Guardian Live pre-market futures and CNN/Bloomberg on the overnight Iran/Gulf-states escalation (see §13).
- **suggested manual fix:** unchanged from the 11:46 review — a human-driven session should check whether the stocks regime classifier ingests any weekend/overnight futures or VIX-futures signal, or is blind to overnight moves by design; if blind by design, document that limitation directly in the report's regime section so future reviews don't need to re-derive the gap every time there's an overnight news event.
- **priority:** high (unchanged from 11:46 EEST; will resolve naturally at the open when RTH data replaces the Friday-derived regime read)
- **first observed:** 2026-07-13 11:46 EEST; still open this cycle.

### TODO-evaa-usdt-data-gap
- **issue:** EVAA/USDT, flagged as the 11:46 review's best short-watch (a live -26.95%/24h unwind with falling OI), has dropped out of today's fresh scalp and intraday top-40 scanned universe entirely. No current price, OI, or funding data exists in either fresh report this cycle, so the prior unwind/retest thesis cannot be re-verified or acted on.
- **evidence:** `data/reports/scalp/2026-07-13_11-38_scalp_report.md` and `data/reports/intraday/2026-07-13_11-44_intraday_report.md` — no EVAA/USDT mention in either (checked via full-text search); last appearance was `data/reports/intraday/2026-07-13_06-20_intraday_report.md` (used in the 11:46 review).
- **suggested manual fix:** a human-driven session should check whether EVAA/USDT genuinely fell out of the top-40 momentum/RS ranking (i.e. the move has fully decayed) or whether this is a discovery-agent/liquidity-filter edge case worth a manual look — if the former, no action needed; if the latter, consider whether the discovery agent should retain recently-flagged high-conviction symbols for a few extra cycles even if they drop below the momentum cutoff.
- **priority:** low (informational — no live position or trade decision depends on this)
- **first observed:** 2026-07-13 16:28 EEST (this cycle).

### TODO-telegram-send-skipped-no-notifier-tool
- **issue:** Per the PERMISSION CONTRACT, this routine is allowed exactly one compact Telegram message via "the existing notifier" (§A.5), but no Telegram-send tool or an allowed CLI command for it was available in this session's tool/command set (§A.4 does not list one). Sending would require either an unlisted shell command or a tool not present this run.
- **evidence:** §A.4 allowed-CLI list contains no telegram-send command; no MCP/tool for Telegram messaging was available in this session's deferred-tool list.
- **suggested manual fix:** confirm whether the production scheduler's own Telegram-push step (used by `run_default_market_schedule.py` for cycle-completion alerts) is the intended "existing notifier" for this routine, and if so, expose a narrowly-scoped, read-only-safe CLI wrapper for it under §A.4 so future Opus review runs can send the required summary without needing broader shell permissions.
- **priority:** medium (blocks the routine's one write-side requirement each cycle; review itself completed successfully and was written to disk regardless)
- **first observed:** 2026-07-13 16:28 EEST (this cycle) — same constraint likely applied to prior cycles that also skipped the Telegram step; not independently re-verified against earlier reviews' text for whether they mentioned this specific gap.
