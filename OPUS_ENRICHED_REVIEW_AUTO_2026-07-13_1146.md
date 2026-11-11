# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:46 EEST

## 1. Executive Summary

**Slot: Europe / pre-US context (nominal 11:30 EEST) — advisory only / no auto-trade.** Building the US-session watchlist; crypto is the only live-actionable class right now, stocks remain pre-market/planning until the cash open (~16:30 EEST).

**Scheduler is healthy.** The active folder (`2026-07-12_default_schedule`) shows `cycle_07` completed cleanly at 09:34 EEST (`ok=40 failed=0`, Telegram sent), and `cycle_08` is mid-run right now (started 11:34 EEST, crypto scalp/intraday already regenerating) — normal overlap, not a stall.

**No A- or B-tier crypto setup is live.** Fresh scalp/intraday reports (~09:14-09:20 EEST) show the regime has **flipped more bearish** since the last review's stale swing snapshot: BTC `transition_down`, ETH `range`, altcoin breadth only 30% above EMA20, style explicitly "short bias or no trade; avoid weak altcoin longs." Every watchlist idea today is a short (EVAA, TLM, VANRY, ADA, T, GRAM, SXT, CASHCAT), all capped to C for weak volume/no catalyst/squeeze risk.

**EVAA/USDT's blow-off call from the 04:44 review has now played out**: it was +85% 24h then (short-covering, -34% OI, flagged blow-off-risk); today it is **-26.95% 24h**, derivatives now reading outright deleveraging — a clean confirmation the desk's own risk read was correct, not yet a fresh short (needs a failed-bounce retest, see §7).

**Important contradiction found and verified externally:** the stocks-intraday report labels the regime **risk_on** (VIX 15.03, breadth 100% above EMA20/50) and surfaces 7 A-tier long candidates (META, AVGO, NVDA, TSLA, QQQ, AMD, SPY) — all correctly demoted to C by the market-closed gate. But verified pre-market data (CNBC, this morning) shows **US futures down meaningfully**: Dow -0.43%, S&P -0.58%, **Nasdaq -1.37%**, driven by a third consecutive weekend of Iran-US strikes (NPR, Wikipedia "2026 Strait of Hormuz crisis", Irish Times) and Iran again declaring the Strait of Hormuz closed while CENTCOM disputes it. The desk's own risk-on read likely predates this weekend's escalation and should not be trusted at face value into the pre-US-open review — treat every one of those A-scored stock longs as **gap-risk, RTH-confirmation-required**, not a green light.

**MSFT legal risk carries forward, currently dormant.** No fresh MSFT catalyst today; the paper monitor shows the prior MSFT `waiting_for_entry` long expired `NO_ENTRY` (stale, never touched) — no live position. If MSFT resurfaces as an A/B candidate before the securities-fraud class action resolves (Aug 11 2026 deadline), it must still be routed AVOID/MANUAL REVIEW regardless of score.

**Catalyst mapping remains weak but modestly improved**: 81.5% unmapped (1185/1454) vs 83.2% at 04:44 — still well above the 50% threshold, use as context only.

**Overall verdict: CAUTION, routed by side — not a no-trade call.** Crypto: short bias per the desk's own regime read; best short-watch is `EVAA/USDT` on a failed-bounce retest, best catalyst-watch is `ZEC/USDT` (unchanged genuine catalyst). Stocks: pre-market only, do not treat the desk's risk-on/A-tier read as confirmed until RTH price action is seen against a materially weaker external futures tape. Scanning, tracking, and the paper book continue uninterrupted regardless of this call.

## 2. Data Used

- Crypto scalp report: **fresh** — `2026-07-13_06-14_scalp_report.md` (generated 09:14 EEST; data as of 06:00 UTC). Regime: bearish trend (risk-off). No A/B; scalp remains kill-switch disabled (14d PF 0.14, 1W/7L per its own header).
- Crypto intraday report: **fresh** — `2026-07-13_06-20_intraday_report.md` (generated 09:20 EEST). No A/B; 8 C-tier watchlist shorts, all "no fresh verified catalyst" except ADA (weak catalyst).
- Crypto swing report: **carry-forward, ~7h old** — `2026-07-13_01-40_swing_report.md` (generated 04:40 EEST, data as of 01:30 UTC). Regime at the time: "transition (mixed)" — since superseded by the fresher bearish scalp/intraday read; DEXE/ZEC/LAB pullback zones quoted below are from this stale snapshot (unfilled, unchanged from the prior review) and should be re-checked against live price before acting.
- Stocks intraday: **fresh** — `2026-07-13_06-30_stocks_intraday_report.md` (generated 09:30 EEST). Regime risk_on/long bias per internal data — see §1 caveat on staleness vs verified weekend escalation. 7 A-tier + 8 B-tier candidates, all demoted to C by `market_closed_intraday_planning_only`. Stocks swing/invest: last generated 2026-07-02, ~11 days stale — known deprecated legacy mode, not evaluated.
- Catalysts: `data/catalysts/2026-07-13/catalyst_events.jsonl` (1454 events cumulative today) + `narrative_baskets.jsonl` (2 active baskets as of the 09:21 EEST cycle: `rwa_narrative`, `ai_narrative` — `momentum_breakout`/DODO and `delisting_thin_liquidity`/XRP baskets seen in the 09:14-09:20 reports have since rotated out). Mapped/unmapped computed directly from the JSONL (see §5).
- LLM packets: `data/processed/llm_analysis_packet.md` (crypto, refreshed 09:20 EEST) and `data/processed/llm_stocks_packet.md` (stocks, refreshed 09:31 EEST).
- CLI: `active-signals --asset-class crypto` (28 rows, all B-tier, all `tp1_hit`/`tp2_hit` — none waiting_for_entry), `active-signals --asset-class stocks` (50 rows, all C-tier or legacy, all historical tp/triggered outcomes from Jul 3-11 — nothing fresh today), `signal-stats` both asset classes (week), `detect_untracked_legacy_alerts --since 2026-07-13` (0 found).
- DB / logs (read-only): `data/scheduled_runs/2026-07-12_default_schedule/scheduler.log` (cycle_07 clean finish 09:34 EEST, cycle_08 mid-run from 11:34 EEST); `reports/PAPER_MONITOR_STATUS_LATEST.md` (09:33 EEST — lifecycle counts, see §3); `obsidian_vault/11_Trade_Journal/Daily_Reviews/2026-07-13.md` (auto-generated 09:33 EEST — today's alert history and the standing MSFT legal-risk block).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_0444.md` (04:44 EEST, ~7h ago) — primary comparison baseline for §4.
- External: 3 WebSearch queries (BTC/ETH price context; US stock futures Monday July 13 2026; Iran/Strait of Hormuz weekend status) — sources in §13. No WebFetch needed; results were mutually consistent across CNBC, NPR, Wikipedia, Irish Times, Japan Times so a follow-up fetch wasn't required for verification.

## 3. Scheduler / Data Freshness

- `scheduler.log` (`2026-07-12_default_schedule`, still the active folder): `cycle_07` finished cleanly 09:34 EEST (`ok=40 failed=0`, Telegram sent); `cycle_08` started 11:34 EEST and is mid-run (crypto scalp/intraday regenerating as of this review) — **fresh, not deferred**.
- Crypto scalp/intraday: **fresh** this cycle (generated 09:14-09:20 EEST, data as of 06:00-06:15 UTC).
- Crypto swing: **carry-forward** (~7h old, 04:40 EEST) — flagged in §1/§2; regime read here is stale relative to the fresher bearish scalp/intraday snapshot.
- Stocks intraday: **fresh** (09:30 EEST) but pre-market — planning-only per the report's own banner; not a live regression.
- Untracked legacy crypto alerts: **0** (confirmed this cycle).
- Known non-blocking noise (unchanged, self-documented in every report): Reddit social-attention sources 403; Bybit/OKX futures partial coverage; SEC EDGAR listed DEAD in the stocks report's source-health block (4 configured sources DEAD, enabled but not writing).
- Paper Monitor Status (09:33 EEST, Telegram-pushed): **Open actionable 0 · Waiting for entry 0 · Review/Shadow 99 · Entered unresolved (expired-after-entry) 6 · No-entry/stale/moved-away 55 · Closed today 392W/17L/0flat · Needs review 0**.
- Today's crypto alert history (Obsidian daily review, 09:33 EEST): 5 B-tier alerts fired overnight/this morning (ZEC scalp long, ETH scalp long, OPN swing short, SOL scalp short, OPN scalp short) — ZEC and ETH both already `close_stop`; VANRY/USDT intraday long also `close_stop`; VELVET/USDT intraday long `close_tp` (+1R); SOL/USDT scalp short `paper_entry` → `close_expired` (entered-unresolved lifecycle, not a missed entry); OPN/USDT scalp short `paper_entry` → `close_stop`. No A-tier signal fired today.
- MSFT: prior `waiting_for_entry` long now shows `NO_ENTRY` (stale, never touched) in the paper monitor — no live position, but the `ACTIVE_LEGAL_HEADLINE_RISK: securities_fraud` block for MSFT is still listed in today's Obsidian daily review.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-13 11:46 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["stocks swing/invest (~11 days stale, known deprecated mode)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_07 finished cleanly 09:34 EEST (ok=40 failed=0), cycle_08 mid-run from 11:34 EEST", "crypto scalp/intraday fresh (09:14-09:20 EEST); crypto swing carry-forward (~7h, 04:40 EEST); stocks intraday fresh (09:30 EEST)", "0 untracked legacy crypto alerts"] },
    { "agent": "market_regime", "verdict": "mixed", "confidence": 0.6,
      "reason_codes": ["risk_off", "shorts_preferred", "chop", "wait_for_trigger"],
      "data_missing": ["fresh intraday-timeframe derivatives/OI beyond the 8 symbols covered per report"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC transition_down, ETH range, altcoin breadth 30% above EMA20, style 'short bias or no trade' (fresh, 09:14-09:20 EEST) — a flip from the stale swing snapshot's 'transition (mixed)'", "stocks: desk labels risk_on (VIX 15.03, breadth 100%) but this predates verified weekend Iran/Hormuz escalation; external futures down (Dow -0.43%, S&P -0.58%, Nasdaq -1.37%) per CNBC this morning", "EVAA/USDT reversed from +85% 24h (04:40 EEST) to -26.95% 24h (09:14 EEST) — a live, confirmed blow-off unwind"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "no_catalyst", "catalyst_confirmed", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl direct count: 1454 total, 269 mapped (18.5%), 1185 unmapped (81.5%) — above the 50% weak-mapping threshold, modestly better than 04:44's 83.2%", "2 active baskets as of 09:21 EEST: rwa_narrative (ONDO/XLM), ai_narrative (NEAR/RENDER/TAO/FET) — momentum_breakout/DODO and delisting_thin_liquidity/XRP baskets from earlier cycles have rotated out", "ZEC/USDT retains a genuine external catalyst (Orchard pre-disclosure-trading scrutiny + Forbes 2026 Top-10) in both fresh 09:14-09:20 reports", "ai_narrative basket's catalyst_summary field contains an unrelated Iran-explosion headline bled in from a different topic — a tagging-quality issue, see §14"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["unwind", "post_unwind_chop", "oi_contradicts", "squeeze_risk"],
      "data_missing": ["Bybit/OKX cross-check limited to ~8 symbols per report"],
      "suggested_effect": "advisory_only",
      "facts_used": ["EVAA/USDT: price down + OI down (-3.4%) — deleveraging, confirms the unwind from the earlier blow-off top, not fresh short conviction yet", "VANRY/USDT: price down + OI down (-15.86%) — deleveraging/long liquidation", "VELVET/USDT, DEXE/USDT, PUMP/USDT: price up + OI up — fresh positioning, none yet flagged crowded", "LAB/USDT (stale, swing-only): still squeeze-capped from the 04:40 snapshot, not re-confirmed live today (not in today's top-40 scalp/intraday universe)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "clean_retest", "entry_late", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["EVAA/USDT: current price 0.953, stated failed-bounce/retest zone 0.9795-1.039 not yet filled — a short now would chase the decline, not confirm a retest", "ZEC/USDT: pullback zone 526.38-530.08 (stale swing snapshot, invalidation 521.86) — needs re-check against live price before treating as actionable", "DEXE/USDT: pullback zone 47.385-48.234 (stale swing snapshot) still unfilled, 7d +98% at last read — chase risk unchanged", "stocks A-tier longs (META/AVGO/NVDA/TSLA/QQQ/AMD/SPY): technically strong on Friday's data but entry now would be blind to a weaker weekend macro tape — RTH confirmation required, not a chase"] },
    { "agent": "execution_lifecycle", "verdict": "ok", "confidence": 0.65,
      "reason_codes": ["review_shadow", "no_entry", "closed_flat", "entered_unresolved"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Paper monitor (09:33 EEST): Open actionable 0, Waiting for entry 0, Review/Shadow 99, Entered unresolved 6, No-entry/stale/moved-away 55, Closed today 392W/17L/0flat, Needs review 0", "Today's alert history: ZEC/ETH scalp both close_stop; VANRY intraday close_stop; VELVET intraday close_tp (+1R); SOL scalp entered-unresolved (close_expired); OPN scalp close_stop", "MSFT prior stocks long now NO_ENTRY (stale, never touched) — no live position", "28 crypto active-signals rows, all tp1_hit/tp2_hit — 0 in waiting_for_entry"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "legal_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MSFT: verified active securities fraud class action (Aug 11 2026 lead-plaintiff deadline) — dormant today (no live signal, no fresh catalyst) but must route AVOID/MANUAL REVIEW if it resurfaces", "JPM: earnings tomorrow (2026-07-14), swing-blocked + do_not_chase_warning already active in production", "Geopolitical: verified third consecutive weekend of Iran-US strikes, Iran again declaring Hormuz closed, CENTCOM disputing — driving a materially weaker pre-market futures tape (Nasdaq -1.37%) that the desk's own risk_on stocks regime label does not yet reflect"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week headline A/B: winrate 12.6%, PF 0.963, avgR -0.0134, totalR -2.20", "by mode: scalp catastrophic (0W/13L, PF 0.18), intraday mild negative (PF 0.91), swing best (PF 1.41, +9.1R)", "weekend-mode signals outperform this week (PF 3.07, n=50) vs weekday (PF 0.59, n=161) — recurring seasonal pattern, consistent with prior reviews", "stocks headline A/B anecdotal (n=6, PF 1.19, +0.57R); stocks C-tier watchlist PF 0.71, winrate 14.4%, week totalR -11.3 — weak but not Telegram-actionable"] },
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
    "best_long_candidate":     { "symbol": "none clean in crypto; stocks A-tier longs (NVDA/AVGO/META) watch-only", "trigger": "RTH open confirmation against the weaker external futures tape — do not treat Friday's A-tier score as pre-cleared" },
    "best_short_candidate":    { "symbol": "EVAA/USDT (watch, do not chase the decline)", "trigger": "failed bounce/retest into 0.9795-1.039 with rejection, hold below invalidation 1.112" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "fill on pullback into ~526-530 zone (stale swing snapshot — re-check live price), hold above ~522, catalyst (Orchard scrutiny + Forbes Top-10) still fresh in today's reports" },
    "avoid_candidate":         { "symbol": "MSFT (if it resurfaces) + chasing any stock A-tier long at the open", "reason": "MSFT carries an active securities fraud class action (Aug 11 2026 deadline); stock A-tier longs are scored on stale pre-weekend data against a verified weaker futures tape" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | mixed | 0.60 | risk_off, shorts_preferred, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, no_catalyst, catalyst_confirmed, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | unwind, post_unwind_chop, oi_contradicts, squeeze_risk | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, clean_retest, entry_late, overextended | advisory_only |
| execution_lifecycle | ok | 0.65 | review_shadow, no_entry, closed_flat, entered_unresolved | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, legal_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.55 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.55 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Comparison baseline: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-13_0444.md` (04:44 EEST, ~7h ago).

- **Regime flip:** crypto scalp/intraday regime moved from the 04:44 review's "range/chop (neutral)"/"transition (mixed)" to explicitly **bearish trend (risk-off)**, BTC now `transition_down` (was `range`), style now "short bias or no trade" (was "selective only; demand clean invalidation"). This is a genuine deterioration, not noise — altcoin breadth is unchanged-thin (30% vs 28-47% range before).
- **EVAA/USDT thesis confirmed:** the 04:44 review flagged EVAA's +85%/-34%OI move as a "short-covering/blow-off-risk shape, not fresh conviction." Seven hours later it is -26.95% 24h with OI now also falling (-3.4%, outright deleveraging) — the call played out. Not yet a fresh short (needs the failed-bounce retest), but the risk read was right.
- **New this cycle:** verified, materially weaker external stock-futures tape (Dow -0.43%, S&P -0.58%, Nasdaq -1.37%) on a third consecutive weekend of Iran-US strikes — not present in the 04:44 review (which was written before the weekend's fresh escalation was fully priced) and **not yet reflected in the desk's own stocks risk_on regime label**. This is the single most important new finding this cycle — flagged in §1, §6, and §14.
- **Removed / resolved:** DODO/USDT and ANSEM/USDT have dropped out of the `momentum_breakout` narrative basket (no longer an active basket as of the 09:21 EEST cycle) — DODO's 24h move has also decayed from +45% (04:40 EEST) to +25% (09:14 EEST), consistent with the desk's own "no confirmed catalyst" read cooling off rather than continuing.
- **Upgraded / downgraded:** none of DEXE/ZEC/LAB's pullback zones have changed (all from the same 04:40 EEST swing snapshot, still unfilled) — thesis unchanged, just needs a live-price re-check before the next swing refresh.
- **Catalyst mapping:** improved slightly, 81.5% unmapped vs 83.2% at 04:44 — still a recurring, high-priority gap (see §14, unchanged from prior escalation).
- **MSFT:** thesis unchanged (AVOID/MANUAL REVIEW if it resurfaces) but the specific `waiting_for_entry` signal referenced at 04:44 has since expired `NO_ENTRY` (stale, never touched) — no live position to act on right now.
- **Confirmed / invalidated:** the 04:44 review's catalyst-symbol-resolver TODO remains open, not independently re-verified this cycle beyond the raw mapped/unmapped count (stayed within the read-only CLI budget).

## 5. Catalyst Coverage

- Total `catalyst_events` today (JSONL, direct count, cumulative): **1454**.
- Mapped (non-null symbol): **269** (18.5%).
- Unmapped (null symbol): **1185** (81.5%).
- `narrative_baskets` active as of the 09:21 EEST cycle: **2** — `rwa_narrative` (ONDO/XLM), `ai_narrative` (NEAR/RENDER/TAO/FET).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (81.5% unmapped, well above the 50% threshold; modest improvement vs the 04:44 review's 83.2%, still the same underlying resolver gap.)
- Data-quality note: the `ai_narrative` basket's `catalyst_summary` field contains a stray, unrelated headline ("SEVERAL EXPLOSIONS HEARD NEAR IRAN'S SIRIK -STATE TV") bled in alongside genuine AI-sector headlines — a basket-summary tagging issue, not just a resolver gap (see §14).
- This continues to be a resolver-coverage issue, not a signal-quality issue.

## 6. Market Landscape

Crypto has turned meaningfully more cautious since the last review: BTC is now reading `transition_down` (was `range`), ETH has cooled from uptrend to `range`, and altcoin breadth remains thin at 30% above EMA20 — the scalp and intraday reports both now explicitly recommend "short bias or no trade; avoid weak altcoin longs," a harder stance than the 04:44 review's "selective only." The loudest mover overnight, EVAA/USDT, has round-tripped from +85% 24h (a short-covering blow-off top flagged as risk in the last review) to -26.95% 24h now, with OI also falling — a live, in-progress unwind, not yet a clean short (needs the market to rally back into the stated 0.98-1.04 zone and fail before that's tradeable). DODO/USDT's momentum has decayed from +45% to +25% 24h and dropped out of the active narrative-basket list — consistent with "no confirmed catalyst" fading rather than continuing. ZEC/USDT remains the one name with a genuine, repeatedly-verified external catalyst (Orchard-flaw pre-disclosure-trading scrutiny + Forbes 2026 Top-10 placement), still showing up fresh in both of today's crypto reports; its stated pullback zone (526-530, from a 7h-old snapshot) needs a live-price re-check before treating as actionable. On the stocks side, the desk's own data reads risk_on (VIX 15.03, 100% breadth, 7 A-tier long candidates) — but this is Friday's-close-derived and does **not** yet reflect a verified, materially weaker weekend macro tape: US stock futures are down meaningfully this morning (Dow -0.43%, S&P -0.58%, Nasdaq -1.37%) on a third consecutive weekend of Iran-US strikes, with Iran again declaring the Strait of Hormuz closed and CENTCOM disputing it. That gap between the desk's internal regime label and the verified external tape is the single most decision-relevant fact for the 16:20 pre-US-open review — every one of the desk's A-tier stock longs (META, AVGO, NVDA, TSLA, QQQ, AMD, SPY) should be treated as gap-risk / RTH-confirmation-required, not pre-cleared by Friday's score. JPM's earnings tomorrow (2026-07-14) remains a swing-blocked, do-not-chase name regardless. MSFT's securities-fraud legal risk carries forward but is currently dormant (no live signal, no fresh catalyst today).

### Market Mood / Risk Routing

- Crypto mood: **risk-off / short-biased** (BTC transition_down, ETH range, breadth 30% above EMA20, scalp+intraday both explicitly recommend short bias or no trade)
- Stocks mood: **internally risk-on but externally contradicted** — desk regime says risk_on (VIX 15.03, breadth 100%), verified pre-market futures say otherwise (Dow -0.43%, S&P -0.58%, Nasdaq -1.37%) on fresh Iran/Hormuz escalation; treat as **mixed/unconfirmed** until RTH price action is observed
- Dominant narrative: crypto short bias into thin, no-catalyst altcoin weakness (EVAA unwind, DODO fading); stocks — a real but internally-unrecognized macro risk-off pulse from the weekend's Iran-US strikes
- Preferred side now: **crypto: shorts on confirmed retest only; stocks: wait for RTH confirmation, do not chase the desk's stale A-tier longs**
- Best long candidate: none clean in crypto — stocks A-tier longs (NVDA/AVGO/META) are watch-only pending RTH confirmation against the weaker futures tape
- Best short candidate: none clean yet — best short-watch: **EVAA/USDT**, trigger = failed bounce/retest into 0.9795-1.039 with rejection, hold below invalidation 1.112 (current price 0.953, below the zone — do not chase the current level)
- Best catalyst-backed candidate: none clean actionable — catalyst-watch: **ZEC/USDT**, trigger = fill on pullback into ~526-530 (re-verify live price, snapshot is 7h old), hold above ~522, catalyst thesis (Orchard scrutiny + Forbes Top-10) still fresh today
- What to avoid: **MSFT** if it resurfaces as a candidate (active securities fraud litigation); chasing any of the stock A-tier longs (META/AVGO/NVDA/TSLA/QQQ/AMD/SPY) right at the open given the verified weaker futures tape; JPM ahead of tomorrow's earnings
- What would change the view: RTH open reaction confirming or refuting the weaker futures tape; BTC reclaiming range/uptrend structure; EVAA/USDT actually filling and rejecting the 0.98-1.04 retest zone; a resolution (either direction) on the Hormuz/Iran dispute before the US open

## 7. Candidate Deep Dives

### 7.1 EVAA/USDT — best short-watch, live unwind in progress (do not chase)

**Status:** C-tier watchlist (score 60.0 intraday), the desk's single biggest reversal today — 24h -26.95% (was +85.11% at 04:40 EEST), 7d still +4.68%. RS vs BTC -25.37%. Volume 0.09x (thin). Derivatives: price down + OI down (-3.43%), "deleveraging or long liquidation" — a genuine unwind, not fresh short pressure. **Has price already reacted?** Yes — this is the unwind of the blow-off top flagged in the prior review, already well underway. **Chasing?** A fresh short at the current level (0.953) chases an already -27% move. **Retest structure?** Yes — the intraday report's stated conditional failed-bounce/retest zone is 0.9795-1.039, which price has not yet reached from below; a clean entry needs a rally into that zone and a rejection, not a chase of the current print. **Overextended?** To the downside, yes. **Would entry now be late?** Yes, without the retest. **Actionable now or after confirmation?** After a failed bounce into the stated zone with volume/rejection confirmation — currently below threshold (score 60, confidence low). **Aligned with mood?** Yes — a short fits the desk's own "short bias or no trade" crypto regime call better than any long candidate today. **Invalidates the idea:** 1h close beyond 1.112, or a reclaim suggesting the unwind is done and fresh demand is stepping in. **Chase-risk:** high if entered now; low if the stated retest zone is respected. **Catalyst confirmation/contradiction:** none — pure unwind mechanics, no verified news either way.

### 7.2 ZEC/USDT — best catalyst-watch, thesis unchanged and still fresh

**Status:** C-tier watchlist, appearing with a genuine external catalyst in both of today's fresh crypto reports (Zcash Orchard-flaw pre-disclosure-trading scrutiny + Forbes 2026 Top-10 placement). 24h +3.8% (intraday/scalp, fresh), 7d +15.76% (per the 7h-old swing snapshot). Derivatives: price up + OI up (+2.1-2.7%), modest positive funding — fresh, not crowded. **Has price already reacted to the catalyst?** Partially — moderate, not extended. **Chasing?** Not at the 24h scale seen today. **Retest structure?** Yes per the (stale) swing snapshot: conditional pullback zone 526.38-530.08, invalidation 521.86 — this needs a live-price re-check since the snapshot is 7h old and today's fresher reports don't re-quote exact levels. **Overextended?** No. **Would entry now be late?** Only if filled without re-verifying the zone against current price. **Actionable now or after confirmation?** After a fill inside a re-verified pullback zone with improving volume (0.42x at last read, below the desk's own confirmation bar). **Aligned with mood?** Reasonably — a catalyst-backed name is the one category the desk's own "short bias or no trade" crypto call doesn't automatically veto, since it isn't a directional long chase against the regime. **Invalidation:** 1h close beyond ~522 (subject to re-verification). **Chase-risk:** low if the zone is respected and re-verified. **Catalyst confirmation:** confirmed via two independent outlets (AMBCrypto, BeInCrypto), same as the prior review, not contradicted.

### 7.3 Stocks A-tier long book (META, AVGO, NVDA, TSLA, QQQ, AMD, SPY) — watch-only, gap-risk into the open

**Status:** All 7 score A-tier (82-90) on the desk's own stocks-intraday model, all correctly demoted to C by the `market_closed_intraday_planning_only` gate. **Has price already reacted to a catalyst?** These are RS/momentum/breadth-driven scores from Friday's data, not news-driven. **Chasing?** Not applicable pre-open, but treating the A-tier score as a green light at the open would effectively be chasing stale data. **Retest structure?** Not established — this is a regime-confirmation question, not a technical-level question. **Overextended?** Not evaluated at this level of granularity in the source report. **Would entry now be late?** N/A pre-open. **What makes it actionable?** RTH price/volume confirmation that the desk's risk_on read still holds despite the weekend's escalation — specifically, indices need to open and hold rather than gap down and continue. **Aligned with mood?** This is exactly the open question: the desk's internal regime (risk_on) and the verified external futures tape (down meaningfully, Nasdaq futures -1.37%) disagree. **Invalidates the idea:** a weak/gap-down open that fails to reclaim Friday's close on the indices; continued Iran/Hormuz escalation headlines into the open. **Chase-risk:** high if any of these are treated as pre-cleared without RTH confirmation. **Catalyst confirmation/contradiction:** contradicted by the verified pre-market futures move — not yet reflected in the desk's own regime label (see §14 TODO).

## 8. Best Candidates Ranked

1. **Short-watch:** EVAA/USDT — trigger: failed bounce/retest into 0.9795-1.039 with rejection, hold below 1.112. Do not chase the current decline.
2. **Catalyst-watch:** ZEC/USDT — trigger: fill on a re-verified pullback into ~526-530, hold above ~522, catalyst thesis intact.
3. **Long-watch (stocks, conditional):** NVDA/AVGO/META — trigger: RTH open confirmation that indices hold/reclaim Friday's close despite the weaker futures tape; do not treat the A-tier score alone as sufficient.
4. **Chase-risk watch (not actionable):** DEXE/USDT — 7d +98% (stale snapshot), still capped "more than 2 ATR from EMA20; do not chase," pullback zone 47.4-48.2 unfilled.
5. **Momentum-fading watch (not actionable):** DODO/USDT — 24h momentum decayed from +45% to +25%, dropped out of the active narrative-basket list, no confirmed catalyst at any point today.

No A/B setup is cleanly actionable at this moment — this reflects the current decision window only, not a call to pause the system.

## 9. Avoid / No Trade

- **MSFT (if it resurfaces as a candidate)** — verified active securities fraud class action (Aug 11 2026 lead-plaintiff deadline). No live position right now (prior signal expired `NO_ENTRY`), but AVOID/MANUAL REVIEW must apply the moment it re-appears as an A/B candidate, regardless of score.
- **Stock A-tier longs at the open (META/AVGO/NVDA/TSLA/QQQ/AMD/SPY)** — do not treat Friday's-data scores as pre-cleared; the verified weekend futures tape is meaningfully weaker (Nasdaq -1.37%) than the desk's own risk_on regime label reflects. Demand RTH confirmation.
- **EVAA/USDT (chase)** — do not short the current -27% print without waiting for the stated failed-bounce/retest zone.
- **DEXE/USDT (chase)** — still >2 ATR from EMA20 per the last full read; wait for the stated pullback zone and re-verify live price first (snapshot is 7h old).
- **JPM** — earnings tomorrow (2026-07-14), swing-blocked + do-not-chase warning already active in production.
- This is a decision-window call only — scanning, tracking, and the paper book continue in every mood.

## 10. Main Risks

- **Geopolitical / macro, verified and escalating:** third consecutive weekend of Iran-US strikes, Iran again declaring the Strait of Hormuz closed, CENTCOM disputing — US stock futures down meaningfully this morning (Dow -0.43%, S&P -0.58%, Nasdaq -1.37%) as a direct result. This is the dominant risk into the 16:20 pre-US-open review.
- **Internal/external regime mismatch:** the stocks-intraday desk report labels the regime risk_on off Friday's data; the verified pre-market tape says otherwise. Acting on the desk's A-tier long list without RTH confirmation risks chasing into a weaker open than the score implies (see §14).
- **Crypto regime deterioration:** BTC has moved from range to transition_down since the 04:44 review, with the scalp/intraday reports now both explicitly recommending short bias or no trade — a genuine, not cosmetic, shift.
- **Catalyst mapping regression (persistent):** 81.5% unmapped today, still far above the 50% weak-mapping threshold — a longstanding resolver gap (see §14, carried from prior reviews).
- **Stale swing snapshot:** DEXE/ZEC/LAB pullback zones are all quoted from a 7h-old swing report; live price should be re-verified before treating any of them as actionable once the next swing refresh lands.
- **MSFT legal risk (dormant but standing):** no live position today, but the underlying securities fraud litigation remains active through Aug 11 2026 — must be re-applied if MSFT resurfaces as a candidate.

## 11. Action Plan — next 4 hours

- Crypto: no new longs; the desk's own regime call is short-bias-or-no-trade. Watch EVAA/USDT for a failed-bounce retest into 0.98-1.04 before considering a short; watch ZEC/USDT for a re-verified pullback fill.
- Do not force a DEXE/USDT entry; it remains chase-risk-capped and its stated zone is from a stale snapshot — wait for the next swing refresh to re-confirm levels.
- Stocks: do not pre-position for the open based on the desk's A-tier score list alone. Treat the verified weaker pre-market futures tape as the dominant input; require RTH confirmation (first 15-30 min) before treating any of META/AVGO/NVDA/TSLA/QQQ/AMD/SPY as actionable, and carry this explicitly into the 16:20 pre-US-open review.
- JPM: no chase ahead of tomorrow's earnings print regardless of any score.
- MSFT: no action needed today (no live signal), but flag for immediate AVOID/MANUAL REVIEW if it resurfaces as a new A/B candidate before Aug 11 2026.
- Operator: no urgent manual action required this cycle; the stocks regime/futures mismatch and the catalyst-mapping gap are read-model TODOs for a human-driven session (see §14), not live decisions.

## 12. Final Verdict per Mode

- **Crypto scalp:** disabled (kill-switch), no A/B — data collection only; today's alerts (ZEC, ETH, SOL, OPN) all already resolved (mostly stops, one entered-unresolved/expired).
- **Crypto intraday:** WATCH, short-biased — no A/B; EVAA/USDT best short-watch (unwind confirmed, needs retest), VELVET/USDT closed +1R today.
- **Crypto swing:** WATCH (data 7h stale) — ZEC/USDT (catalyst-backed), DEXE/USDT (chase-risk long), LAB/USDT (stale, squeeze-capped short) remain the cleanest of the last full snapshot's ideas; re-verify against live price at the next refresh.
- **Stocks (all modes):** PRE-MARKET / WATCH-ONLY into the US session; desk regime says risk_on but this is unconfirmed against a verified weaker weekend futures tape — carry the RTH-confirmation-required flag into the 16:20 pre-US-open review; MSFT dormant-AVOID if it resurfaces; JPM no-chase into tomorrow's earnings.

## 13. Sources

- [Stock market today: Live updates](https://www.cnbc.com/2026/07/12/stock-market-today-live-updates.html) — CNBC, 2026-07-12/13 (pre-market futures: Dow -0.43%, S&P -0.58%, Nasdaq -1.37%, driven by Iran/Hormuz tensions)
- [Stock market next week: Outlook for July 13-17, 2026](https://www.cnbc.com/2026/07/10/stock-market-next-week-outlook-for-july-13-17-2026.html) — CNBC, 2026-07-10
- [U.S. launches fresh strikes on Iran as Tehran says it has closed Strait of Hormuz](https://www.npr.org/2026/07/11/g-s1-133212/us-iran-vessel-attack-strait-hormuz-gulf) — NPR, 2026-07-11
- [2026 Strait of Hormuz crisis](https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis) — Wikipedia, updated through 2026-07-12
- [US and Iran exchange fresh strikes as Tehran says Strait of Hormuz is closed](https://www.irishtimes.com/world/us/2026/07/12/us-and-iran-exchange-fresh-strikes-as-tehran-says-strait-of-hormuz-is-closed/) — Irish Times, 2026-07-12
- [U.S. strikes Iran, Tehran hits Gulf states, says Strait of Hormuz closed](https://www.japantimes.co.jp/news/2026/07/12/world/us-strikes-iran-ship-strait-of-hormuz/) — Japan Times, 2026-07-12
- [Iran expands attacks on Gulf states after US strikes, says Strait of Hormuz closed](https://www.yahoo.com/news/articles/iran-declares-strait-hormuz-closed-232134793.html) — Yahoo/AP, 2026-07-12
- Bitcoin/Ethereum price check: no July 13-dated article located; most recent available reference ~$62.7-64k BTC / ~$1,740-1,800 ETH (CoinDesk/Yahoo Finance, week of July 7-9 2026) — treat as directional context only, not an exact same-day print.
- Internal: `data/reports/scalp/2026-07-13_06-14_scalp_report.md`, `data/reports/intraday/2026-07-13_06-20_intraday_report.md`, `data/reports/swing/2026-07-13_01-40_swing_report.md`, `data/reports/stocks/intraday/2026-07-13_06-30_stocks_intraday_report.md`, `data/catalysts/2026-07-13/*`, `data/scheduled_runs/2026-07-12_default_schedule/scheduler.log`, `reports/PAPER_MONITOR_STATUS_LATEST.md`, `obsidian_vault/11_Trade_Journal/Daily_Reviews/2026-07-13.md`.

## 14. Fix Requests / TODO

### TODO-stocks-regime-vs-external-futures-mismatch
- **issue:** The stocks-intraday report's internal regime label (`risk_on`, VIX 15.03, breadth 100%) does not reflect a verified, materially weaker pre-market futures tape this morning (Dow -0.43%, S&P -0.58%, Nasdaq -1.37%) driven by a third consecutive weekend of Iran-US strikes and a disputed Strait of Hormuz closure. This produced 7 A-tier long candidates (META, AVGO, NVDA, TSLA, QQQ, AMD, SPY) that read as technically strong but are blind to the weekend's macro deterioration.
- **evidence:** `data/reports/stocks/intraday/2026-07-13_06-30_stocks_intraday_report.md` §1 (regime risk_on, VIX 15.03) and §5 (7 A-tier candidates); external verification via CNBC pre-market futures report and NPR/Wikipedia/Irish Times/Japan Times on the weekend Iran/Hormuz escalation (see §13).
- **suggested manual fix:** a human-driven session should check whether the stocks regime classifier ingests a weekend/overnight futures or VIX-futures signal at all, or only RTH-session data as of Friday's close — if it's blind to weekend macro moves by design, that's a known limitation worth documenting explicitly in the report's own regime section (e.g. "regime computed from last RTH session, not current pre-market") so future Opus reviews don't need to independently re-derive this gap every time there's a weekend news event.
- **priority:** high (directly affects whether the A-tier stock long list should be trusted at the open)
- **first observed:** 2026-07-13 11:46 EEST (this cycle).

### TODO-catalyst-symbol-resolver-gap-persistent
- **issue:** Catalyst mapping coverage remains weak — 81.5% unmapped (1185/1454) today, only modestly improved from 83.2% at the 04:44 EEST review. This is the same recurring resolver gap flagged across multiple prior reviews (escalated to high priority at 04:44 EEST).
- **evidence:** `data/catalysts/2026-07-13/catalyst_events.jsonl` — direct count via Python (269 mapped / 1185 unmapped out of 1454).
- **suggested manual fix:** unchanged from the 04:44 EEST review — audit the symbol resolver for literal `<TICKER>USDT`-style substrings in exchange-notice headlines that still fail to resolve to a symbol.
- **priority:** high (unchanged/carried forward)
- **first observed:** recurring across multiple prior reviews; last escalated 2026-07-13 04:44 EEST.

### TODO-narrative-basket-summary-tagging-bleed
- **issue:** The `ai_narrative` basket's `catalyst_summary` field (in `data/catalysts/2026-07-13/narrative_baskets.jsonl`) contains an unrelated headline — "SEVERAL EXPLOSIONS HEARD NEAR IRAN'S SIRIK -STATE TV" — mixed in alongside genuine AI-sector headlines (Bittensor/Render). This looks like a summary-generation bleed across unrelated topics, not a resolver-mapping issue.
- **evidence:** `data/catalysts/2026-07-13/narrative_baskets.jsonl`, `ai_narrative` record, `catalyst_summary` field, created_at 2026-07-13T06:21:00+00:00.
- **suggested manual fix:** a human-driven session should check the narrative-basket summarizer's headline-selection logic for cross-topic contamination — low priority, cosmetic, but could confuse an operator reading the basket summary at face value.
- **priority:** low
- **first observed:** 2026-07-13 11:46 EEST (this cycle).
