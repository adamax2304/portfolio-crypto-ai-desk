# Opus Enriched Review — US open reaction review — Auto Cycle 18:48 EEST

## 1. Executive Summary

Slot: **US open reaction review** (target 18:30 EEST / 11:30 ET, this run ~18:48 EEST / ~11:48 ET, ~2h18m into the RTH session). **Advisory only — no auto-trade.** Zero A-tier anywhere, crypto or stocks, this cycle — consistent with every prior review today. Crypto regime remains **bullish trend (risk-on)** on the freshest read (scalp report, 15:30 UTC data freshness, generated 18:42 EEST — 6 minutes before this review started): BTC uptrend, ETH transition_up, altcoin breadth 69.77% above EMA20/50 (up from 66.67% at 15:58). Macro/geopolitics risk **eased from 100/100 to 93.2/100** this cycle — still risk-off-leaning but the first genuine move off the 100 ceiling in four consecutive reviews. **BICO/USDT intraday long — the desk's own repeatedly-chase-flagged signal from earlier cycles — filled and then STOPPED OUT at 18:38 EEST (-1.0R), ten minutes before this review**, empirically vindicating the chase-flag warnings raised at 04:39, 11:39 and 15:58 (§14 TODO closed-loop). FIDA/USDT and TUT/USDT intraday longs (both flagged waiting_for_entry as of the 15:58 review) have since **filled** and remain open/unresolved. Two fresh intraday B-tier longs fired since the last review: **HFT/USDT** (74.9, 17:51 EEST) and **ZEC/USDT** (67.2, 17:12 EEST), both still waiting_for_entry — unlike the BICO/FIDA cases, the gap between the funnel's earlier chase-flag rejection and these live signals is 2+ hours (not 12-19 minutes), and the freshest scalp report no longer flags HFT for chase risk, so this is **not** treated as a new occurrence of the systemic timing-gap pattern (see §14 for the distinction). A **second internal weakest-symbol-vs-active-long contradiction** has emerged: **EPIC/USDT** now joins HOME/USDT on today's weakest-symbols table (bias short, -9.27%/-9.96% RS) while carrying an active triggered long B-tier swing position — the same class of contradiction first flagged on HOME/USDT, now confirmed on a second symbol (§7/§14, escalated). On the stocks side, RTH is ~2h18m old: VIX **16.34** (index breadth 100% above EMA20/50, bullish/risk-on), yet **zero A/B-tier setups are actionable** — all 6 raw A-tier names (NVDA, AMZN, MSFT, SMCI, JPM, DIA) and 6 raw B-tier names (AVGO, PLTR, NFLX, GOOGL, XLY, AAPL) were demoted to C by the SI-1..5 actionability gates (market-context conflict, sector-confirmation, lunch-confirmation, liquidity, no-catalyst) — the gates are doing exactly what they're designed to do (not chasing an early-session record-high tape without confirmation). MSFT and PLTR additionally carry active **legal-risk demotions** (class-action / SEC-DOJ) independent of the SI gates. LLY (earnings beat, stock reportedly popped per external search) and UBER (mixed/slid) both correctly stayed untouched by the system (do-not-chase gate, LLY scored 16.1/no_directional_setup) — a clean confirmation the earnings-avoidance logic worked today. The BAC pre-US BLOCK verdict from the 15:58 review **did persist to the DB this time** (partial fix of TODO-preus-ingest-db-locked) but its block window already expired (17:06 UTC); SMCI's verdict was never ingested at all — TODO stands, downgraded to informational since the pre-US window has passed for today.

## 2. Data Used

- Crypto: `data/reports/scalp/2026-08-05_15-42_scalp_report.md` (data freshness 15:30 UTC, ~18min old at write time — freshest source this cycle), `data/reports/intraday/2026-08-05_12-37_intraday_report.md` (data freshness 12:30 UTC, ~3h18m old, still fresh <4h band), `data/reports/swing/2026-08-05_13-23_swing_report.md` (data freshness 13:15 UTC, ~2h33m old, fresh).
- Stocks: `data/reports/stocks/intraday/2026-08-05_15-38_stocks_intraday_report.md` (data freshness 15:37 UTC, ~10min old at write time — freshest RTH read of the day, generated live during this review's data-gathering pass).
- `data/catalysts/2026-08-05/catalyst_events.jsonl` (2,500 rows scanned, 1,605 null-symbol), `narrative_baskets.jsonl` (4 baskets, unchanged membership since 15:58).
- CLI: `active-signals --asset-class crypto` (36 rows), `active-signals --asset-class stocks` (50 rows, all past-expiry legacy remnants), `signal-stats --asset-class crypto` (weekly: n=89, PF 2.54), `signal-stats --asset-class stocks` (weekly: n=228, PF 0.60), `detect_untracked_legacy_alerts --since 2026-08-05` (0 untracked).
- DB (read-only queries): `proposed_signals` filtered to non-expired A/B rows (19 genuinely open crypto positions; 0 stocks), `signal_outcomes` for BICO/USDT's stop-out and scalp expiry detail, `stocks_preus_review` / `stocks_preus_review_blocks` (checked whether the 15:58 review's BAC/SMCI BLOCK verdicts persisted — BAC did, SMCI did not).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1558.md` (pre-US-open decision review, 15:58 EEST).
- **External web research invoked this cycle** (WebSearch x3, no WebFetch): US market tone/VIX context (results were dating-ambiguous across Aug 3-5 record-high headlines — treated as directional confirmation only, not a precise intraday quote, since the internal stocks report's own VIX=16.34 read is fresher and more reliable), BTC/ETH price/mood context (Yahoo Finance aggregate), LLY/UBER earnings-reaction confirmation (Yahoo Finance earnings-live-updates). Used because the prior review flagged an unresolved bull/bear tension (Burry crash-warning vs fresh ATH) worth checking whether it resolved into the RTH session; internal reports don't carry external opinion/sentiment context.

## 3. Scheduler / Data Freshness

- Nicosia-local cron target 18:30 EEST, actual fire ~18:39-18:48 EEST (this review's data-gathering window) — within tolerance, no DST drift (both zones on summer time as of 2026-08-05).
- `scheduler.log` mtime ~18:34 EEST (~14min old at review start) — fresh, not deferred. Latest `cycle_07_15-22_summary.md` mtime ~16:33 EEST (~2h15m old) — fresh (<3h), not deferred.
- Crypto scalp ~18min old (freshest source this cycle, landed mid-review), intraday ~3h18m old (fresh, <4h band), swing ~2h33m old (fresh) — all three usable for the fresh verdict, no stale-exclusion needed this cycle (unlike 15:58's stale swing report).
- Stocks intraday ~10min old — freshest RTH read of the day; market open, live SI-1..5 gate output usable directly (no pre-US overlay needed this slot — that overlay is reserved for the 16:20 EEST pre-open slot only).
- No monitor/paper-status file read this cycle (outside allowed read list) — data_missing, carried from every prior cycle.
- Data-quality anomalies this cycle: (1) catalyst-mapping still weak at 64.2% unmapped (unchanged vs 15:58 — the same daily cumulative file); (2) EPIC/USDT joins HOME/USDT as a second weakest-symbol-vs-active-long contradiction (§7/§14, escalated); (3) SMCI's pre-US BLOCK verdict from 15:58 was never persisted to `stocks_preus_review` (TODO stands, now informational since the pre-US window has closed); (4) BICO/USDT intraday's stop-out closes the loop on the chase-flag-recurrence TODO with a concrete loss outcome.
- **TradingView / manual chart check unavailable** — no chart MCP loaded this cycle; all price-structure statements are from local OHLCV/ATR/EMA fields already computed inside the reports, plus external WebSearch for general market-tone context only (no chart reads).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-05 18:48 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh"],
      "data_missing": ["monitor/paper-status file not read (outside allowed read list)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log ~14min old, cycle_07 summary ~2h15m old, both fresh", "crypto scalp ~18min old (freshest source, landed mid-review), intraday ~3h18m old (fresh <4h band), swing ~2h33m old (fresh)", "stocks intraday ~10min old, freshest RTH read of the day"] },
    { "agent": "market_regime", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["risk_on", "longs_preferred"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC uptrend, ETH transition_up, altcoin breadth 69.77% above EMA20/50 (up from 66.67% at 15:58) per freshest 15:30 UTC scalp read", "macro/geopolitics risk eased 100/100 -> 93.2/100 this cycle -- first move off the ceiling in 4 consecutive reviews", "stocks: bullish regime, bias long, risk-on true, VIX 16.34, breadth 100% above EMA20/50, all 4 major indices uptrend"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["64.2% unmapped today (1605/2500), unchanged vs 15:58 (same cumulative daily file)", "4 narrative baskets unchanged: delisting_thin_liquidity, binance_ecosystem_teaser (BNB), rwa_narrative (ONDO/XLM), momentum_breakout (HEI/FIDA/PUMP)", "every live crypto B-tier fire today explicitly carries 'no fresh verified catalyst detected' in its own evidence block -- pure momentum/RS thesis, consistent with prior cycles"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["no fresh per-symbol funding/OI beyond what the 15:42 EEST scalp and 15:37 EEST intraday reports embed"],
      "suggested_effect": "advisory_only",
      "facts_used": ["HFT/USDT: price up + OI up +45.23% (scalp), funding 0.00049 -- fresh positioning, crowding read as normal in the freshest report though an earlier report flagged elevated long crowding -- worth caution on the fresh waiting_for_entry fill", "FIDA/USDT (now triggered/filled): negative funding across external venues, elevated crowding per the 15:58 review's cross-check -- carried headwind on an already-filled position", "no fresh Hyperliquid whale-liquidation-level data this cycle (not in the allowed read list); prior ~$64,889 BTC level context from 15:58 not re-verified"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["chase_risk", "clean_retest", "entry_fresh", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BICO/USDT intraday: entered (filled), then STOPPED at 18:38 EEST, final_r=-1.0 -- the exact chase-flag pattern raised at 04:39/11:39/15:58 resolved as a confirmed loss, empirical support for treating chase-flagged same-pass fires with extra caution", "HFT/USDT and ZEC/USDT: both flagged 'do not chase, >2 ATR from EMA20' in the 12:37 EEST intraday report snapshot, but their live signals fired 2h14m and 1h42m later respectively -- a materially longer gap than the BICO/FIDA 12-19min pattern, and the freshest 15:42 EEST scalp report no longer flags HFT for the ATR-extension reason (only scalp-kill-switch + long/short skew) -- read as a legitimate later pullback, not a repeat of the systemic bug (§14)", "FIDA/USDT, TUT/USDT: both filled cleanly inside their previously-defined pullback zones, not market chases"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["open_actionable", "waiting_for_entry", "entered_unresolved", "closed_flat"],
      "data_missing": ["CLI does not label lifecycle state directly -- classification below is manual, from status + expires_at, filtered to non-expired rows only"],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto (19 genuinely open A/B rows, expires_at in the future): 16 OPEN actionable (11 triggered + 3 tp1_hit + 2 tp2_hit), 3 WAITING for entry (HFT, ZEC, SYN)", "Crypto closed this cycle: BICO/USDT intraday CLOSED LOSS (-1.0R, stopped 18:38 EEST); BICO/USDT scalp ENTERED UNRESOLVED (filled, no TP/SL before its 2h window expired, final_r display 0R/unresolved -- not a missed entry)", "Stocks: 0 OPEN, 0 WAITING among non-expired rows -- the 50-row legacy active-signals table is entirely past-expiry remnants (latest expiry 2026-08-04) from deprecated swing/invest modes or old intraday fills; 0 new A/B this RTH cycle (12 raw A/B demoted to C by SI-1..5 gates)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT (raw A, demoted to C): active legal-headline risk (class_action, securities_fraud) -- caught this time by the stocks-intraday gate directly, unlike the BAC/SMCI cases the hard pre-US gate missed at 15:58", "PLTR (raw B, demoted to C): active legal-headline risk (sec_doj)", "LLY, UBER: earnings today, both correctly gated do_not_chase_warning / block_requires_operator_review -- confirmed working as external search shows LLY beat+popped and UBER mixed/slid, and the desk took no position in either", "EPIC/USDT: second instance of the weakest-symbol-vs-active-long contradiction (after HOME/USDT) -- needs manual review before any fresh EPIC exposure either direction", "BAC pre-US BLOCK persisted to DB this run (partial fix of the 15:58 ingest-lock TODO) but its block_expires_at (17:06 UTC) is already past; SMCI verdict never made it to the DB at all"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto weekly (n=89, stronger): PF 2.54, avgR 0.40, winrate 27.2% -- healthy at the tier level even though individual scalp fires (now fully kill-switched, all rejections read crypto_scalp_disabled) remain the confirmed weak sub-bucket", "crypto by mode: intraday PF 3.72 (best), swing PF 2.20, scalp PF 0.16 (worst, kill-switched) -- consistent with every prior cycle", "stocks weekly (n=228, reliable): tier=C triggered winrate 4%, PF 0.60 -- both below the CLI's own flag thresholds; direction=short n=80 PF~0/avgR-0.5 vs direction=long n=148 PF 1.8 -- the same large, high-confidence losing short-direction bucket flagged at 15:58, unresolved TODO"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.6,
      "reason_codes": ["mixed", "longs_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime continues risk-on with macro risk easing (100->93.2) -- modestly more constructive than every prior cycle today, but the day's one closed trade (BICO intraday) was a loss that validates caution on chase-flagged fires", "stocks RTH gates correctly withheld all 12 raw A/B candidates despite a genuinely bullish tape (VIX 16.34, breadth 100%) -- the system is behaving conservatively as designed, not missing an obvious trade", "HFT/USDT is the highest-score fresh waiting_for_entry (74.9) with a defined pullback zone and no current chase flag -- best long-watch this cycle", "EPIC/USDT contradiction (2nd instance of the HOME/USDT pattern) needs a manual look before any fresh exposure"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "HFT/USDT", "trigger": "intraday B-tier waiting_for_entry (74.9), fill only inside 0.01576-0.01618, invalidation 0.01409 -- earlier chase-flag from the 12:37 EEST report no longer active in the 15:42 EEST scalp read; do not chase if price is already through the zone" },
    "best_short_candidate":    { "symbol": "none clean", "trigger": "BANK/USDT is today's weakest symbol (-23.75%/-24.43% RS) but the desk's own funnel rejects it (39.0, 'short setup fights a bullish tape', no catalyst); VIC/USDT similarly capped for short-squeeze risk -- both watch-only until a confirmed failed-bounce structure appears" },
    "best_catalyst_candidate": { "symbol": "FIDA/USDT", "trigger": "already filled/triggered (72.7) inside its defined zone, momentum_breakout narrative-basket primary -- no entity-specific news, basket-tag only; hold/monitor invalidation 0.02024, do not add without a fresh confirming catalyst" },
    "avoid_candidate":         { "symbol": "EPIC/USDT", "reason": "second internal contradiction: today's weakest-symbols table (bias short, -9.27%/-9.96% RS) vs an active triggered long B-tier swing position -- do not open fresh exposure either direction until reconciled" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.8 | scheduler_fresh | advisory_only |
| market_regime | ok | 0.65 | risk_on, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.5 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.5 | squeeze_risk, oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.6 | chase_risk, clean_retest, entry_fresh, entry_late | advisory_only |
| execution_lifecycle | caution | 0.6 | open_actionable, waiting_for_entry, entered_unresolved, closed_flat | advisory_only |
| risk_manager | caution | 0.6 | legal_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.6 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.6 | mixed, longs_preferred, wait_for_trigger | advisory_only |

## 4. What Changed vs Previous Review

Compared to `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1558.md` (15:58 EEST, pre-US-open decision review):

- **New:** HFT/USDT intraday long fired waiting_for_entry (74.9, 17:51 EEST); ZEC/USDT intraday long fired waiting_for_entry (67.2, 17:12 EEST). Both no-catalyst momentum, defined pullback zones, not yet filled.
- **Filled since last review:** TUT/USDT intraday (65.7, was waiting at 16:03, now triggered) and FIDA/USDT intraday (72.7, was waiting at 15:49, now triggered) both filled inside their defined zones.
- **Closed:** BICO/USDT intraday long — CLOSED LOSS, stopped at 18:38 EEST, final_r -1.0 (was triggered/filled at 15:58's review time). BICO/USDT scalp long — ENTERED UNRESOLVED, filled but expired its 2h window with no TP/SL hit (final_r display 0R/unresolved, not a missed entry).
- **Removed:** none of the prior cycle's core carried positions dropped.
- **Upgraded/downgraded:** macro/geopolitics risk eased 100/100 -> **93.2/100** (first move off the ceiling in 4 consecutive reviews). Altcoin breadth improved 66.67% -> 69.77% above EMA20/50. Stocks: fully into RTH now (was pre-open at 15:58); VIX read 16.34 internally (vs the ~17.9 external premarket estimate at 15:58 -- volatility compressed into/through the open, consistent with a clean record-high tape).
- **New contradiction:** EPIC/USDT joins HOME/USDT as a weakest-symbol-vs-active-long contradiction (2nd instance of the same pattern, §7/§14).
- **Confirmed:** no untracked legacy alerts (0, per detector). BICO/USDT's stop-out **confirms** the chase-flag-recurrence theory had real predictive value on at least this instance -- closes the loop on that specific symbol's TODO thread with a concrete loss.
- **Partially resolved:** the `stocks-preus-review-ingest` DB-lock TODO from 15:58 -- BAC's BLOCK verdict did persist to `stocks_preus_review_blocks` this time (blocked_at 13:06:12 UTC), though its block window has since expired; SMCI's verdict was never ingested at all (no SMCI row exists in `stocks_preus_review`) -- the fix is incomplete.
- **Invalidated:** none.
- Catalyst mapping unchanged at 64.2% unmapped (same cumulative daily file as 15:58).

## 5. Catalyst Coverage

- Total catalyst events today: **2,500**; mapped (non-null symbol): **895**; unmapped: **1,605** (**64.2%**) -- unchanged vs the 15:58 review (same cumulative daily file, no new file generated yet this cycle).
- Narrative baskets: **4**, unchanged membership -- `delisting_thin_liquidity` (avoid chasing low-float delisting dumps, no primary), `binance_ecosystem_teaser` (BNB/USDT), `rwa_narrative` (ONDO/USDT, XLM/USDT), `momentum_breakout` (HEI/USDT, FIDA/USDT, PUMP/USDT primary -- FIDA's presence here lines up with it being today's best catalyst-backed candidate by basket-tag, though no entity-specific news exists for it).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** Unmapped is 64.2%, unchanged from this morning's worst reading.
- Top unmapped headlines (sample): an Agthia (UAE F&B) German-language earnings release (PR Newswire), a $250M USDC mint (whale-alert bot), a Bybit BACUSDT perpetual-listing notice, South African crypto-remittance draft rules, a Western Union stablecoin-card launch -- the same macro-data/exchange-listing/small-cap-PR mix flagged every cycle today (§14).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **risk-on** — BTC uptrend, ETH transition_up, altcoin breadth 69.77% above EMA20/50 (up from 66.67% three hours ago). Macro/geopolitics overlay eased to 93.2/100 risk-off (from a 100/100 ceiling held for four straight reviews) — a genuine, if modest, easing. Scalp mode remains fully kill-switched (every scalp candidate today rejected on `crypto_scalp_disabled`, independent of setup quality). Recommended style: "selective longs; prefer pullbacks on relative strength."
- Stocks mood: **risk-on, RTH confirmed** — VIX 16.34, breadth 100% above EMA20/50, all 4 major indices (SPY/QQQ/IWM/DIA) in confirmed uptrend, ~2h18m into the session. Despite the constructive tape, the SI-1..5 actionability gates withheld all 12 raw A/B candidates (market-context conflict, sector-confirmation, lunch-confirmation, liquidity, no-catalyst) — a deliberately conservative posture during a fresh-highs, low-confirmation morning, not a data problem.
- Dominant narrative: crypto broadening its risk-on tape (altcoin breadth improving, macro fear easing) while stocks extend a record-highs rally that the desk's own gates refuse to chase without confirmation — both asset classes reward patience over chasing today.
- Preferred side now: **longs (crypto, selective)** / **wait-for-gate-confirmation (stocks)** — crypto's regime continues to favor RS-leader pullback longs (HFT, the carried STO/TUT swing runners); stocks needs either a pullback/retest or an SI-gate-clearing catalyst before any of today's 12 raw A/B names becomes genuinely actionable.
- Best long candidate: **HFT/USDT** (fresh waiting_for_entry, chase-flag resolved) — see §7/§8.
- Best short candidate: **none clean** — BANK/USDT is the standout weak-symbol read but is explicitly rejected by the desk's own gate ("short setup fights a bullish tape," no catalyst); treat as watch-only pending a confirmed failed-bounce structure.
- Best catalyst-backed candidate: **FIDA/USDT** (filled, momentum_breakout basket primary) — see §7.
- What to avoid: **EPIC/USDT** fresh exposure either direction (contradiction, §7); **BICO/USDT** any fresh re-entry today given the confirmed stop-out; **crypto scalp mode** entirely (fully kill-switched); **stocks short-direction ideas generally** (confirmed weak bucket, PF~0, n=80); chasing any of the 12 gate-demoted stocks C-tier names without a pullback/retest; LLY/UBER post-earnings moves without fresh confirmation.
- What would change the view: a clean retest/pullback structure forming on any of the 12 gate-demoted stocks names (would let SI-1..5 clear on a subsequent cycle); macro/geopolitics risk continuing to ease below 90; resolution (fill or expiry) of HFT/ZEC/SYN's defined pullback zones; a human reconciling the HOME/USDT and EPIC/USDT weakest-symbol-vs-active-long contradictions.

## 7. Candidate Deep Dives

### BICO/USDT (crypto intraday long, B-tier — CLOSED LOSS this cycle, stopped 18:38 EEST, final_r -1.0)
- Has price already reacted to a catalyst? No — pure no-catalyst momentum fire, consistent with its own evidence block at every prior cycle.
- Is the setup chasing? **This is now resolved, empirically, as yes.** The 04:39 and 11:39 reviews both flagged this exact symbol's funnel-rejection-then-live-fire pattern (chase-flagged at one data snapshot, a live signal firing minutes later at a materially higher score). The position filled, then stopped for a full -1.0R loss ten minutes before this review started.
- Retest/pullback structure? The original entry zone (0.0228-0.0236) was a defined pullback, not a naked chase — but per the 15:58 review's own note, price sat "just above" that zone at fill time, i.e. borderline extended even within the "defined zone" framing.
- Would a fresh entry now be late? Yes — do not re-enter BICO/USDT today off this signal thread; any new BICO/USDT idea needs a fresh, independent setup.
- What level would make a fresh BICO/USDT idea actionable? A new funnel-generated signal with no ATR-extension flag and RS confirmation not already exhausted by today's move.
- Mood alignment: the loss occurred inside an otherwise risk-on tape — a reminder that regime-level risk-on does not make every individual momentum fire safe, especially chase-flagged ones.
- Long/short/wait: **wait** — no fresh BICO/USDT exposure today.
- Chase-risk: confirmed high in hindsight. Catalyst confirmation/contradiction: none either way — a pure technical-quality lesson, not a news-driven failure.

### HOME/USDT & EPIC/USDT (crypto — weakest-symbol vs active-long contradiction, now 2 symbols)
- HOME/USDT (carried from 15:58): still appears on today's weakest-symbols table across all three fresh reports (bias short, 24h between -9.55% and -14.27% depending on report timestamp) while carrying 3 active long B-tier positions (2 triggered swing, 1 tp1_hit intraday). Unresolved since first flagged.
- **EPIC/USDT (new this cycle):** appears on the freshest (15:42 EEST) scalp report's weakest-symbols table (bias short, 24h -9.27%, RS vs BTC -9.96%) and also surfaces in the same report's Crypto Expansion Watchlist as a `weak_rs_short` candidate (score 75) — while the desk carries one active **triggered long** B-tier swing position in EPIC/USDT (69.5, opened 2026-08-01, invalidation 0.85933). This is the identical pattern to HOME/USDT, now confirmed on a second symbol in the same trading day.
- This is a genuine internal consistency question the review cannot resolve with read-only tools — it does not by itself mean either long is wrong (no invalidation has been hit on either symbol), but two symbols showing the same weakest-symbol/active-long conflict in one day raises the likelihood of a shared root cause (e.g., the momentum-ranking table and the swing-signal book reading different OHLCV windows) rather than two unrelated coincidences.
- Would a fresh entry now be late (for a hypothetical short on either)? Yes — no defined short setup exists for either symbol in any report; this is a flag, not a tradeable idea.
- What level would make a short actionable? Only after the desk's own scanner generates a confirmed failed-bounce/breakdown structure — none exists for either symbol yet.
- Mood alignment: both bias-short reads cut against today's broader crypto risk-on upgrade, reinforcing that these are idiosyncratic/technical flags rather than market-wide signals.
- Long/short/wait: **wait** on both — do not add fresh exposure to either symbol in either direction; monitor whether the existing longs' invalidations hold (HOME: 0.005879/0.008321/0.008703; EPIC: 0.85933).
- Chase-risk: N/A (no fresh entry recommended for either). Catalyst confirmation/contradiction: none found for either symbol; pure internal-consistency flag (§14, escalated).

### HFT/USDT (crypto intraday long, B-tier waiting_for_entry, 74.9, fresh — best long-watch this cycle)
- Has price already reacted to a catalyst? No — confirmed no fresh verified catalyst in any report today; pure RS/momentum thesis (24h +72-83% depending on report timestamp), `rs_btc_leader`/`rs_eth_leader`/`momentum_24h_leader` in the Crypto Expansion Watchlist at score 92.
- Is the setup chasing? The 12:37 EEST intraday report's funnel rejected HFT/USDT at score 40.5 ("more than 2 ATR from EMA20; do not chase") using its 12:30 UTC snapshot. The live B-tier signal (74.9) fired 2h14m later at 17:51 EEST. This is a materially longer gap than the confirmed BICO/FIDA same-pass pattern (12-19 minutes), and the freshest 15:42 EEST scalp report no longer cites the ATR-extension reason for HFT at all (its rejection there is scalp-kill-switch plus long/short skew only) — read as a legitimate pullback resolving the earlier extension, not a repeat of the systemic timing-gap issue.
- Retest/pullback structure? Yes — defined zone 0.01576-0.01618, not yet filled.
- Overextended? Not per the freshest read; derivatives show fresh positioning (OI +45.23%, funding modestly positive) without a crowding-elevated flag in the latest snapshot (an earlier snapshot today did flag elevated long crowding — a residual caution worth keeping in mind).
- Would entry now be late? Not yet — still waiting for the defined zone.
- What level makes it actionable cleanly? A fill inside 0.01576-0.01618 holding above invalidation 0.01409.
- Mood alignment: consistent with today's risk-on upgrade and improving altcoin breadth.
- Long/short/wait: **wait-for-entry**, treat as the cleanest fresh long idea this cycle if it fills inside the zone.
- Chase-risk: low per the current read (downgraded from earlier today). Catalyst confirmation/contradiction: none — clean no-catalyst RS/momentum thesis.

### Stocks RTH gate check — NVDA/AMZN/MSFT/SMCI/JPM/DIA (raw A) + AVGO/PLTR/NFLX/GOOGL/XLY/AAPL (raw B), all demoted to C
- Has price already reacted to a catalyst? Mixed — several of these (NVDA, AMZN, MSFT, JPM) are simply riding the broad-market record-highs tape rather than an entity-specific fresh catalyst; the gate's own `catalyst_none_and_not_exceptional_technical` reason confirms this for 8 of the 12.
- Is the setup chasing? Effectively yes for most — `market_context_conflict` (7 of 12) and `lunch_requires_strong_confirmation` (8 of 12) are both live this cycle, meaning the gate judges the broader tape/session-phase confirmation as not yet strong enough to trust an early-session record-highs breakout.
- Retest/pullback structure? None of the 12 have a defined pullback entry in this report — they are watchlist/C-tier only.
- Overextended? RR-based demotions confirm this for AVGO (rr_to_tp1=0.18) and GOOGL (rr_to_tp1=0.63), both well under the 1.5R minimum.
- Would entry now be late? For a market-order chase, yes; the gates exist specifically to prevent this.
- What level makes any of them actionable cleanly? A pullback/retest that resolves the market-context and sector-confirmation conflicts, or a later session-phase confirmation (afternoon vs the current late-morning window) plus a liquidity (RVOL) pickup.
- Mood alignment: nominally aligned (bullish regime, breadth 100%) but the gates are explicitly there to separate "the index is up" from "this specific name has a clean, confirmed setup" — and today they found none.
- Long/short/wait: **wait** on all 12 — this is the gates working as designed, not a missed trade. MSFT (class-action/securities-fraud) and PLTR (SEC-DOJ) additionally carry standing legal-risk demotions independent of the SI gates — treat both as avoid-for-new-A/B regardless of technical score, mirroring the BAC/SMCI legal-risk pattern from the pre-US overlay at 15:58.
- Chase-risk: high if forced; the system correctly did not force it. Catalyst confirmation/contradiction: no entity-specific catalyst for most; legal-risk contradiction live for MSFT/PLTR specifically.

### FIDA/USDT & TUT/USDT (crypto intraday longs, both filled since the 15:58 review — monitor)
- FIDA/USDT (72.7, filled inside 0.02100-0.02162): the chase-flag/live-signal tension flagged at 15:58 (funnel rejected it at 47.8 twelve minutes before the live signal fired) is now moot for this specific fill since it filled cleanly inside its defined zone rather than as a market chase — but the underlying pattern is exactly what BICO/USDT's stop-out (§7 above) just demonstrated can go wrong. Monitor invalidation 0.02024 closely; do not add.
- TUT/USDT (65.7, filled inside 0.02510-0.02559): layered on top of an already-open, tp2_hit swing position in the same symbol (different playbook, 14d WR 72%/PF 5.80) — the stronger of the two fills structurally. Monitor invalidation 0.02449; the swing runner continues toward TP3 (0.0264) or its own invalidation (0.0222).
- Neither position has hit stop or target yet; both are OPEN actionable / unresolved. Given BICO/USDT's outcome this cycle, neither should be treated as "safe" purely because it filled inside a defined zone — the zone discipline reduces but does not eliminate chase-adjacent risk in this no-catalyst-momentum sub-playbook (14d WR 23%/PF 0.70 per the playbook's own self-labeled failure mode).
- Long/short/wait: **hold/monitor** both, no new sizing on either.

*(Excess candidates not given a full deep dive, per the 5-candidate cap: ZEC/USDT and SYN/USDT — both fresh/carried intraday waiting_for_entry in the same no-catalyst-momentum playbook as FIDA/TUT above, lower priority than the contradiction/closed-loss findings; STO/USDT — carried swing long, unchanged, still the desk's steadiest open position, no new information this cycle; BANK/USDT, VIC/USDT — today's other weak-symbol reads, both explicitly gate-rejected for short (fights bullish tape / squeeze risk), covered in §6 as the "no clean short" finding.)*

## 8. Best Candidates Ranked

1. **HFT/USDT (crypto intraday long, waiting_for_entry, B-tier, fresh)** — best long-watch; fill only inside 0.01576-0.01618, invalidation 0.01409; earlier chase flag no longer active.
2. **STO/USDT (crypto swing long, triggered, B-tier, carried)** — steadiest open position, unchanged; hold, add only on a clean retest above invalidation 0.0392.
3. **TUT/USDT (crypto intraday + swing longs, filled/tp2_hit)** — hold both; the swing runner remains the stronger structural position.
4. **FIDA/USDT (crypto intraday long, filled, B-tier)** — hold/monitor invalidation 0.02024; best catalyst-backed candidate by narrative-basket tag only, no entity-specific news.
5. **ZEC/USDT, SYN/USDT (crypto intraday longs, waiting_for_entry, B-tier)** — same no-catalyst-momentum playbook as HFT/FIDA/TUT; fill only inside their defined zones, do not chase.

**BICO/USDT** (closed loss, -1.0R) and **EPIC/USDT** (contradiction, avoid) are this cycle's explicit avoid names — see §7/§9. No stocks name is actionable this cycle (§7 gate check).

## 9. Avoid / No Trade

*(This applies to this decision window / US-open-reaction only — scanning, tracking, and the scheduler continue unchanged.)*

- **BICO/USDT** — closed loss this cycle (-1.0R, stopped 18:38 EEST); do not re-enter off today's exhausted signal thread.
- **EPIC/USDT any fresh direction** — internal contradiction (weakest-symbol bias-short vs active long swing position), 2nd instance of this pattern today; needs manual review before new exposure either way.
- **HOME/USDT any fresh direction** — same contradiction, carried from 15:58, still unresolved.
- **All 12 raw A/B stocks candidates this cycle** (NVDA, AMZN, MSFT, SMCI, JPM, DIA, AVGO, PLTR, NFLX, GOOGL, XLY, AAPL) — gate-demoted to C, not actionable regardless of raw score; MSFT and PLTR additionally carry standing legal-risk flags.
- **Crypto scalp mode entirely** — fully kill-switched this cycle (every candidate rejected on `crypto_scalp_disabled`).
- **Stocks short-direction ideas generally** — confirmed weak bucket at reliable sample size (PF~0, n=80, avgR -0.5, carried TODO).
- **BANK/USDT, VIC/USDT** — today's weakest symbols but both explicitly gate-rejected for short (fights bullish tape / squeeze risk).
- **LLY, UBER post-earnings moves** — both reported today; avoid chasing either print without fresh confirmation.

## 10. Main Risks

- **BICO/USDT's stop-out is the first concrete, closed empirical data point on the chase-flag-recurrence pattern this desk has flagged three times today** — it lost. This strengthens the case for the standing TODO (funnel-scan and signal-writer likely need a shared price snapshot) but is only n=1; do not over-generalize to every chase-flagged fire (FIDA/TUT filled cleanly inside their zones and remain open/unresolved, not losses).
- **A second weakest-symbol-vs-active-long contradiction (EPIC/USDT) emerged today, alongside the still-unresolved HOME/USDT one** — two symbols in one day raises the likelihood of a shared root cause in how the momentum-ranking table and the swing-signal book read OHLCV data, worth a focused human check (§14).
- **Stocks: a genuinely bullish RTH tape (VIX 16.34, breadth 100%, all indices uptrend) produced zero actionable A/B setups** — this is very likely the SI-1..5 gates working correctly (avoiding an early-session record-highs chase), but it is worth periodically sanity-checking that the gate thresholds aren't systematically too conservative for genuinely strong tape days, since 12 consecutive demotions in one cycle is a notable cluster.
- **SMCI's pre-US BLOCK verdict from the 15:58 review was never persisted to the DB** — if a human doesn't investigate why (BAC's ingest succeeded, SMCI's did not, from the same batch), tomorrow's pre-US scan could re-surface SMCI as an apparently-clean candidate.
- Macro/geopolitics risk eased from 100/100 to 93.2/100 but remains elevated and risk-off-leaning — treat the improvement as directional, not a green light.
- Catalyst->symbol mapping remains stuck at 64.2% unmapped — treat all catalyst-basket framing as directional color only, unchanged guidance from every prior cycle.

## 11. Action Plan — next 4 hours

- Do not re-enter BICO/USDT today; let HFT/USDT, ZEC/USDT, and SYN/USDT either fill cleanly inside their defined zones or expire — do not force any of them.
- Hold FIDA/USDT and TUT/USDT (both intraday fills) and the TUT/USDT and STO/USDT swing runners into their respective invalidations/targets; no new sizing on any of the four.
- Do not open any fresh HOME/USDT or EPIC/USDT position (long or short) until both weakest-symbol/active-long contradictions are manually reconciled.
- Do not chase any of today's 12 gate-demoted stocks names; watch for a pullback/retest or an afternoon-session-phase re-evaluation that might clear the SI-1..5 gates on a later cycle.
- Investigate why SMCI's pre-US BLOCK verdict didn't persist to `stocks_preus_review` when BAC's did (same ingest batch, partial success) — needed before tomorrow's pre-US cycle.
- Continue scanning/tracking/monitors unchanged through the US session — this review recommends caution on specific entries only, never a pause of any kind.

## 12. Final Verdict per Mode

- **Crypto scalp:** no trade — fully kill-switched this cycle, every candidate rejected on `crypto_scalp_disabled` regardless of setup quality.
- **Crypto intraday:** caution — HFT/ZEC/SYN wait-for-entry, FIDA/TUT hold-only (filled, unresolved), BICO/USDT closed loss (no re-entry).
- **Crypto swing:** the desk's steadiest bucket — hold STO/USDT and TUT/USDT's runner; no fresh swing ideas fired this cycle; HOME/USDT and EPIC/USDT longs held but flagged for the weakest-symbol contradiction.
- **Stocks intraday:** no trade — RTH confirmed bullish (VIX 16.34, breadth 100%) but all 12 raw A/B candidates gate-demoted to C; wait for a pullback/retest or stronger session-phase/liquidity confirmation.
- **Stocks swing/invest:** not evaluated — reports stale/deprecated since 2026-07-02, excluded per standing policy.

## 13. Sources

- Internal: `data/reports/scalp/2026-08-05_15-42_scalp_report.md`, `data/reports/intraday/2026-08-05_12-37_intraday_report.md`, `data/reports/swing/2026-08-05_13-23_swing_report.md`, `data/reports/stocks/intraday/2026-08-05_15-38_stocks_intraday_report.md`, `data/catalysts/2026-08-05/catalyst_events.jsonl`, `data/catalysts/2026-08-05/narrative_baskets.jsonl`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `signal_outcomes`, `stocks_preus_review`, `stocks_preus_review_blocks` read-only queries), `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1558.md`.
- External (WebSearch, no WebFetch this cycle):
  - [Stock Market News for Aug 5, 2026 — Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/stock-market-news-aug-5-100300808.html) and [Stock Market Today (Aug. 5, 2026) — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-5-2026) — general record-highs market-tone context; dating across results was ambiguous between Aug 3-5, so treated as directional confirmation only, not a precise intraday quote (internal VIX 16.34 read from the 15:38 UTC stocks report is the primary, fresher source).
  - [Bitcoin and ethereum prices today, Wednesday, August 5, 2026 — Yahoo Finance](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-august-5-2026-crypto-prices-rise-as-investors-watch-hormuz-negotiations-and-jobs-report-closely-124640660.html) — general BTC/ETH price/mood context, used for directional confirmation only alongside the internal reports.
  - [Earnings live updates: Eli Lilly stock pops on upbeat guidance, Uber stock slides — Yahoo Finance](https://finance.yahoo.com/markets/live/earnings-live-updates-130425228.html) — confirms LLY beat/popped and UBER mixed/slid, used to verify the desk's do-not-chase gate on both was the correct call, not to size any position.
  - No new items ingested to `news_items` this cycle: the three external searches above returned general market-tone/index-level context rather than discrete entity-specific catalyst events fitting the existing narrative taxonomy (exploit_hack, legal_risk, geopolitical_risk, token_unlock, etc.) — forcing a narrative tag onto a generic "market is up" or "BTC price is X" read would risk a fabricated/inaccurate row, so none were built into a source JSON or ingested. Cited here for review-narrative context only.
- No chart/TradingView source this cycle (unavailable, §3).

## 14. Fix Requests / TODO

### TODO-chase-flag-recurrence-bico-closed-loss (priority: high, evidence upgraded)
- **issue:** BICO/USDT intraday (flagged as the recurring chase-flag/live-signal-timing pattern at 04:39 and 11:39, filled by 15:58) has now **closed as a confirmed loss**: entered, stopped 2026-08-05T15:38:03 UTC (18:38 EEST), final_r=-1.0. This is the first closed (not just flagged) instance of the pattern this desk has tracked all day, and it lost — concrete empirical support for the standing hypothesis that the funnel-scan pass and the signal-writer pass may be reading different price snapshots, producing "reject for chasing, then fire live minutes later" fires that carry elevated risk.
- **evidence:** `db/crypto_ai_desk.sqlite` `signal_outcomes` for BICO/USDT intraday signal (score 66.1, created 2026-08-05T07:38:20Z, `stop_hit=1`, `final_r=-1.0`, `checked_at=2026-08-05T15:38:03Z`); prior instances referenced in `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1558.md` §14 (TODO-chase-flag-recurrence-escalation) and `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1139.md` §14.
- **suggested manual fix:** unchanged from 15:58 — a human-driven session should measure the actual elapsed time between the funnel-scan data-freshness timestamp and the signal-writer's `created_at` across the last 1-2 weeks, and now specifically compare realized-R outcomes for short-gap (<20min) chase-flag-then-fire cases vs longer-gap cases (this review found HFT/ZEC today had 1.5-2h+ gaps and no longer carried the ATR-extension flag by fill time, unlike BICO's ~7h-earlier-same-day pattern) — if short-gap fires systematically underperform, prioritize fixing the shared-snapshot issue for those specifically.
- **priority:** high
- **first observed:** 2026-08-04 (swing instance); escalated 2026-08-05 15:58 EEST (2nd symbol, FIDA); closed-loss evidence added 2026-08-05 18:48 EEST (this cycle).

### TODO-weakest-symbol-active-long-contradiction-2nd-instance (priority: high, escalated from medium)
- **issue:** EPIC/USDT now shows the identical pattern first flagged on HOME/USDT at 15:58: it appears on the current weakest-symbols table (bias short, 24h -9.27%, RS vs BTC -9.96%, per the 15:42 EEST scalp report) while the desk carries an active **triggered long** B-tier swing position in the same symbol (score 69.5, opened 2026-08-01, invalidation 0.85933). Two symbols showing the same conflict in one trading day raises the likelihood of a shared root cause rather than two unrelated coincidences.
- **evidence:** `data/reports/scalp/2026-08-05_15-42_scalp_report.md` "Weakest Symbols" (EPIC/USDT) and "Crypto Expansion Watchlist" (`weak_rs_short`, score 75); `db/crypto_ai_desk.sqlite` `proposed_signals` EPIC/USDT swing row (created 2026-08-01T17:57:00Z, status=triggered); HOME/USDT's original flag in `OPUS_ENRICHED_REVIEW_AUTO_2026-08-05_1558.md` §14 (TODO-home-usdt-contradiction).
- **suggested manual fix:** a human-driven session should check whether the "weakest symbols" momentum-score calculation and the long-signal scoring pipeline are reading from the same OHLCV window/timeframe for both HOME/USDT and EPIC/USDT, and whether both symbols have genuinely reversed against their still-open longs (in which case the invalidations are the operative risk control) or whether one pipeline is systematically stale/misaligned with the other.
- **priority:** high (escalated from medium — now 2 symbols same day)
- **first observed:** HOME/USDT 2026-08-05 15:58 EEST; EPIC/USDT (2nd instance) 2026-08-05 18:48 EEST (this cycle).

### TODO-smci-preus-ingest-partial-failure (priority: medium, carried forward, downgraded from ingest-lock to ingest-gap)
- **issue:** The 15:58 review's `stocks-preus-review-ingest` DB-lock issue appears **partially resolved** — BAC's BLOCK verdict did persist to `stocks_preus_review_blocks` (blocked_at 2026-08-05T13:06:12Z), and BAC/MSTR/SPY/DIA/IWM/NFLX/AMAT all show rows in `stocks_preus_review` with `reviewed_at` timestamps around 13:06-13:07 UTC. **SMCI has no row in either table at all** — its BLOCK verdict from the same review batch never made it to the DB, unlike BAC's.
- **evidence:** `db/crypto_ai_desk.sqlite` `stocks_preus_review` (9 symbols present, SMCI absent) and `stocks_preus_review_blocks` (BAC present with blocked_at 2026-08-05T13:06:12Z, block_expires_at 2026-08-05T17:06:12Z — already expired by this review's write time).
- **suggested manual fix:** a human-driven session should check the ingest script's per-row error handling for the same batch that successfully wrote BAC but silently (or with an uncaptured error) skipped SMCI — likely worth adding per-row logging/retry rather than an all-or-nothing transaction, and manually re-ingest SMCI's verdict from `data/raw/enriched_review_sources/preus_review_2026-08-05T13-05.json` if still valid before tomorrow's pre-US cycle.
- **priority:** medium (downgraded from high — the DB-lock symptom from 15:58 is gone, this is now a narrower per-row gap; also the window this data was actionable for has passed for today)
- **first observed:** 2026-08-05 16:05 EEST (original lock issue); narrowed to SMCI-specific gap 2026-08-05 18:48 EEST (this cycle).

### TODO-stocks-short-direction-losing-bucket (priority: medium, carried forward)
- **issue:** `signal-stats --asset-class stocks` weekly, `direction=short`, n=80 (reliable-adjacent sample): PF near 0, avgR -0.5 — materially worse than `direction=long` (PF 1.8, n=148) in the same weekly window. Unchanged from the 15:58 quantification.
- **evidence:** `signal-stats --asset-class stocks` CLI output, "By direction" table, this cycle (n=80/148, matching 15:58's n=82/148 within normal week-window drift).
- **suggested manual fix:** unchanged from 15:58 — review whether stocks short-side entries need a stricter setup-quality or RS-confirmation gate, or should be demoted to watchlist-only pending further data.
- **priority:** medium
- **first observed:** carried/confirmed 2026-08-05 15:58 EEST; re-confirmed 2026-08-05 18:48 EEST (this cycle).

### TODO-stocks-12-consecutive-gate-demotions (priority: low, new observation)
- **issue:** This cycle's stocks-intraday run demoted all 12 raw A/B candidates to C in a single pass (6 raw A: NVDA, AMZN, MSFT, SMCI, JPM, DIA; 6 raw B: AVGO, PLTR, NFLX, GOOGL, XLY, AAPL) during a genuinely bullish RTH tape (VIX 16.34, breadth 100%, all indices uptrend). This is very likely the SI-1..5 gates working as intended (avoiding an early-session record-highs chase), but a 100% demotion rate on a strong-tape day is worth a periodic sanity check that the gate thresholds (especially `lunch_requires_strong_confirmation` firing well before actual lunch hours, and `liquidity_rvol_below_min`) aren't systematically too conservative for genuinely strong sessions.
- **evidence:** `data/reports/stocks/intraday/2026-08-05_15-38_stocks_intraday_report.md` §10 "Intraday Actionability Gates" — actionable A/B after gates: 0; raw-A/B demoted to C: 8 (of 12 total across both raw tiers); demotion reasons: `lunch_requires_strong_confirmation` x8, `liquidity_rvol_below_min` x8, `catalyst_none_and_not_exceptional_technical` x8, `market_context_conflict` x7.
- **suggested manual fix:** a human-driven session should pull the SI-1..5 demotion rate across several strong-tape RTH days (VIX <17, breadth >90%) to check whether the gates ever let anything through on days like this one, or whether the thresholds need recalibration for high-confidence broad-tape conditions specifically (as distinct from the chop/choppy conditions the gates were likely tuned against).
- **priority:** low
- **first observed:** 2026-08-05 18:48 EEST (this cycle).
