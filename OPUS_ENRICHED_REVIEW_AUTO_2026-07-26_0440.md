# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:40 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (Sunday 2026-07-26, 04:40 EEST). Advisory only — no auto-trade. No fresh A/B crypto setup cleared the desk threshold this cycle (scalp, intraday, and the stale swing report all show "No A-tier / No B-tier setups found"). BTC stays in downtrend / ETH transition_down, macro-geopolitical risk score is pinned at 100/100 (Iran/Israel/Houthi escalation, Strait of Hormuz effectively closed 136 days, Brent >$100), externally corroborated. Altcoin breadth is only mildly improved (43.6% above EMA20) and not confirming a broad move either way. Since the 23:32 review, EUL/USDT long **closed WIN (tp3_hit, full target run)** and dropped off the active list; AERO/USDT short remains the only signal with a still-future expiry (09:54 EEST today, TP1 booked). Catalyst mapping is weak this run (64.8% unmapped, early in the new UTC day). Stocks are closed for the weekend — carry-forward/planning context only. No new TODOs beyond one re-raised data-integrity note on stale "active" signals.

## 2. Data Used

- Reports: `data/reports/scalp/2026-07-25_23-32_scalp_report.md`, `data/reports/intraday/2026-07-25_23-41_intraday_report.md` (both fresh, ~5h old at time of run), `data/reports/swing/2026-07-25_01-44_swing_report.md` (stale, ~27h old — carried for continuity only, no A/B present anyway).
- Stocks: `data/reports/stocks/intraday/2026-07-24_20-10_stocks_intraday_report.md` (stale, market closed — weekend, no fresher source possible), swing/invest reports from 2026-07-02 (very stale, market closed regardless).
- Catalysts: freshly generated this run via `catalyst-scan` (`data/catalysts/2026-07-26/catalyst_events.jsonl`, `narrative_baskets.jsonl`, `catalyst_cycle_01-40.md`) — folder was missing for today prior to this run (expected: run fired at 04:40, just after UTC day rollover).
- LLM packets: `data/processed/llm_analysis_packet.md` (fresh, 02:42 EEST), `data/processed/llm_stocks_packet.md` (stale, 2026-07-24 — market closed).
- CLI: `active-signals` (crypto ×16, stocks ×50), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts` (clean).
- Internal `news_items` spot-checks for EUL/BANK/ALLO/NEAR/RENDER/TAO/FET/ONDO (last 24h).
- External web research: 1 WebSearch (Iran/Hormuz/BTC macro cross-check) — see §13.
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-25_2332.md`.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 2026-07-26 03:42 EEST, latest `cycle_01_02-23_summary.md` mtime 03:42 EEST — both ~1h old at run time (04:40). Well under the 3h defer threshold; **not deferred**.
- `crypto_monitor` log active through 04:34 EEST; `derivatives_monitor` log active through ~04:38 EEST (last JSON entry 01:38 UTC=04:38 EEST) — monitors alive and writing.
- Scalp/intraday reports: fresh (~5h old at 23:30/23:41 generation vs 04:40 run — within the useful window for an overnight slot).
- Swing report: **stale** (>14h, generated 2026-07-25 01:44) — carried for reference only; contains no A/B anyway so exclusion has no practical effect.
- Stocks: all reports stale by design — market closed for the weekend since Friday's close; no fresher data possible until Monday pre-market.
- Catalyst folder for 2026-07-26 was absent before this run (expected — 04:40 slot fires shortly after the UTC catalyst-day rollover); regenerated cleanly via the one allowed CLI command (349 events, 5 baskets).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-26 04:40 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["stocks fresh RTH data (market closed)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle summary ~1h old", "scalp/intraday reports ~5h old", "swing report ~27h old, no A/B present", "catalyst folder regenerated cleanly, 349 events"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["risk_off", "chop", "wait_for_trigger"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend, ETH transition_down", "macro risk 100/100 (Iran/Hormuz)", "altcoin breadth 43.6% above EMA20 — mixed, not confirming broad risk-off", "external WebSearch corroborates Hormuz/oil>$100 backdrop"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mapping_weak", "stale_catalyst", "no_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["349 events, 226 unmapped (64.8%) — early-day sample", "5 baskets: ai_narrative fresh<1h (NEAR/RENDER/TAO/FET), rwa_narrative freshness unknown (ONDO/XLM), perps_dex_narrative fresh<6h (HYPE), binance_ecosystem_teaser fresh<6h (BNB), delisting_thin_liquidity fresh<6h (XRP)", "EUL/BANK/ALLO show zero fresh internal news in 24h; NEAR/TAO have only single-source generic articles"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable"], "data_missing": ["OI history for several watchlist names (n/a)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/ACE/AIXDROP/VANA all squeeze-capped by system guardrails in the scalp/intraday reports", "EUL/BANK funding near-flat, OI n/a via fallback_via_mexc"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["overextended", "chase_risk", "price_moved_away"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["EUL 7d +86.9%, BANK 7d +215.1% — extreme extension, no fresh catalyst backing either", "ALLO watchlist failed-bounce zone 0.3815-0.3913 vs current 0.3771 — price below zone, needs a bounce first"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["open_actionable", "entered_unresolved", "no_entry"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["AERO/USDT short OPEN, TP1 booked, expires 09:54 EEST today", "EUL/USDT long CLOSED WIN tp3_hit since 23:32 review, dropped off active list", "15 other crypto actives + ~49 stocks actives carry expires_at dates 4-23 days in the past while still showing tp1/tp2_hit/triggered status — same pattern flagged in prior reviews (TODO re-raised, see §14)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["macro risk 100/100 continues from last review", "HOOD/NVDA carry advisory exploit_hack operator-review flags (no crypto position implicated)", "stocks MSFT/TSLA legal flags carried forward unchanged, unverified this cycle — market closed"] },
    { "agent": "playbook_performance", "verdict": "bad", "confidence": 0.75,
      "reason_codes": ["playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto scalp mode: n=45, PF 0.72, avgR -0.086, totalR -3.10 — reproducibly losing bucket, past the report's own 20-signal re-audit threshold", "crypto short direction: n=7, PF 0.17, avgR -0.50 — anecdotal but consistently bad", "crypto swing: PF 4.46, avgR 1.08 — strong; crypto intraday: PF 1.90 — solid", "stocks C-tier all-comers: PF 0.56, winrate 3% — weak but explicitly non-actionable watchlist tier"] },
    { "agent": "head_trader", "verdict": "watch_only", "confidence": 0.6,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents below"] }
  ],
  "head_trader": {
    "overall_verdict": "watch_only",
    "confidence": 0.6,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "BANK/USDT", "trigger": "1h close holding 0.3343-0.3450 pullback zone on rising volume (currently 0.3498, just above the zone); invalidation on 1h close beyond 0.3213", "reason": "cleanest RS-BTC leader (+15.9-16.3%) among tonight's momentum names with a less-extreme 7d extension than EUL, but still no fresh verified catalyst — treat as C-tier watch only" },
    "best_short_candidate":    { "symbol": "ALLO/USDT", "trigger": "failed bounce/retest of 0.3815-0.3913 zone with rejection, then 1h close below 0.3552; invalidation on 1h close beyond 0.4034", "reason": "weak-RS short setup (-27.5% RS/BTC), deleveraging OI (-9.86%), but currently below its own entry zone and squeeze-cap risk is elevated across the whole weak-name cohort tonight" },
    "best_catalyst_candidate": { "symbol": "NEAR/USDT", "trigger": "needs a scored technical setup to clear the intraday/scalp funnel (not present tonight) before the ai_narrative basket (fresh<1h) becomes actionable — currently only a single-source 'buy signal' article, not a real event", "reason": "closest thing to a fresh catalyst-linked name; genuinely weak evidence, flagged as watch-only not a trigger" },
    "avoid_candidate":         { "symbol": "EUL/USDT", "reason": "7d +86.9%, 24h +64.6%, no fresh verified catalyst, score 51.9 explicitly below active-trade threshold in its own report — textbook chase risk; separately, already closed WIN tp3_hit on the prior signal so there is no open position to manage here, only the temptation to chase a fresh entry" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 1
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.65 | risk_off, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.60 | mapping_weak, stale_catalyst, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | overextended, chase_risk, price_moved_away | advisory_only |
| execution_lifecycle | needs_review | 0.70 | open_actionable, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | bad | 0.75 | playbook_failing, low_sample | advisory_only |
| head_trader | watch_only | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-25_2332.md` (post-close, ~5h ago).

- **EUL/USDT long CLOSED WIN** — tp3_hit (full target run) recorded 2026-07-25 18:24-18:26 UTC, dropped off the active-signals list. It was the other "open actionable" name in the 23:32 review; that review's TP1-booked management note for EUL is now resolved.
- **AERO/USDT short** remains the only truly OPEN position (TP1 booked), same as before, window now closer to expiry (09:54 EEST today, ~5h away).
- **BANK/USDT** long-watch thesis carries forward unchanged from 23:32 — still watchlist-only, still no fresh catalyst, price has drifted slightly (0.3379→0.3498, i.e. further from its pullback entry zone, marginally more extended).
- **ACE/USDT** (short-watch, provisional, in the 23:32 review) is no longer among tonight's top setups at all — it dropped off the strongest/weakest funnel this cycle; superseded by ALLO/USDT as this run's clearest weak-RS short-watch name.
- **HYPE/USDT** catalyst-watch (bearish, from 23:32) has no fresh price/technical data in tonight's funnel — carried as a stale, unconfirmed idea rather than repeated as a live trigger (see §7).
- Macro risk score unchanged at 100/100; BTC/ETH trend unchanged (downtrend / transition_down); altcoin breadth essentially flat (43.6% vs prior ~43.6%).
- Catalyst mapping: 64.8% unmapped tonight vs 67.1% unmapped at 23:32 — comparable, both above the 50% weak-mapping threshold, and both reflect early-in-day-cycle samples (tonight's catalyst folder was regenerated fresh at 04:40 for the new UTC day).
- Stocks: unchanged, still weekend-closed; carried MSFT/TSLA legal flags and UNH DOJ antitrust flag not re-verified this cycle (per prior review's own stated caveat).

## 5. Catalyst Coverage

- Today's (2026-07-26, fresh from 04:40 UTC-day-rollover regeneration) `catalyst_events.jsonl`: **349** total rows; mapped (non-empty symbol): **123** (35.2%); unmapped: **226** (**64.8%**).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Narrative baskets (5): `ai_narrative` (primary NEAR/RENDER/TAO/FET, playbook `related_beta_rotation`, fresh <1h), `delisting_thin_liquidity` (primary XRP, `avoid_low_liquidity`, fresh <6h), `binance_ecosystem_teaser` (primary BNB, `related_beta_rotation`, fresh <6h), `perps_dex_narrative` (primary HYPE, `wait_pullback`, fresh <6h), `rwa_narrative` (primary ONDO/XLM, `related_beta_rotation`, freshness unknown).
- Top 3 unmapped headlines by importance (mostly securities-fraud-lawsuit-deadline press-release noise, not tradeable catalysts):
  1. (0.73) "VRRM Deadline: VRRM Investors Have Opportunity to Lead Verra Mobility Corporation Securities Fraud Lawsuit" (2026-07-25 22:43 UTC)
  2. (0.712) "Zillow Deadline: Z, ZG Investors Have Opportunity to Lead Zillow Group, Inc. Securities Fraud Lawsuit" (Rosen Law Firm, 2026-07-25 21:02 UTC)
  3. (0.676) "BTU Deadline: BTU Investors Have Opportunity to Lead Peabody Energy Corporation Securities Fraud Lawsuit" (2026-07-25 15:31 UTC)

## 6. Market Landscape

**Crypto:** BTC trend `downtrend`, ETH trend `transition_down` (both scalp and intraday agree, both fresh at ~23:30-23:41 EEST last night, still the newest read available). Altcoin breadth 43.6% above EMA20/EMA50 — mixed, not confirming a broad breakdown. Macro/geopolitical risk score **100/100** (7 risk-off hits, 0 risk-on, 1 calendar/watch), driven by the ongoing Iran/Israel/Houthi conflict — externally corroborated (see §13): Brent crude above $100 for the first time since late May, the Strait of Hormuz effectively de-facto closed for 136 days per press reporting, Houthi strikes on Saudi tankers, and BTC holding near $65K despite the pressure rather than collapsing outright. Strongest names tonight: EUL (+64.6% 24h, +86.9% 7d), BANK (+16.3%/+215.1%), SHIB (+16.7%/+17.8%) — all RS leaders with thin volume confirmation (0.35x-0.48x) and zero fresh verified catalyst backing any of them. Weakest: ALLO (-27.1%), RIF (-25.3%), AIXDROP (-20.8%), ACE (-17.5%) — every one of these is squeeze-capped by the system's own guardrails, meaning it is a crowded-short tape rather than a clean bearish setup. Production risk warnings unchanged: HOOD and NVDA (exploit_hack, advisory-only), BTC (geopolitical_risk headline).

**Stocks:** Fully closed for the weekend. No fresh RTH data possible until Monday pre-market (2026-07-27, 16:30 EEST). Carried context, not re-verified this cycle: MSFT and TSLA remain flagged AVOID/manual-review on legal grounds (class-action/securities-fraud and going-concern respectively, per the prior review); UNH carries an active C-tier invest position with a DOJ antitrust advisory flag. No fresh stocks candidates possible or expected this slot.

### Market Mood / Risk Routing

- Crypto mood: **risk-off / chop** (BTC/ETH downtrend & transition_down, macro risk 100/100, but altcoin breadth only mildly negative — not a clean risk-off wipeout)
- Stocks mood: **closed** (weekend — reopens Monday 2026-07-27, 16:30 EEST)
- Dominant narrative: continued Iran/Israel/Houthi escalation and Strait-of-Hormuz risk pressuring macro sentiment; RS-leader alt names (EUL/BANK/SHIB) running counter-tape on thin volume with no catalyst confirmation
- Preferred side now: **wait-for-trigger** — no clean chase-free long or short; manage the one open position (AERO short) through its window
- Best long candidate: BANK/USDT — none actionable now, trigger: 1h close holding 0.3343-0.3450 pullback zone
- Best short candidate: ALLO/USDT — none actionable now, trigger: failed bounce/retest of 0.3815-0.3913 then close below 0.3552
- Best catalyst-backed candidate: NEAR/USDT (ai_narrative basket, fresh<1h) — weak evidence, needs a scored technical setup before it is watchable
- What to avoid: chasing EUL/USDT or BANK/USDT at current extension without a pullback; chasing any of the squeeze-capped short names (ALLO/RIF/AIXDROP/ACE) without a confirmed failed-bounce structure
- What would change the view: a de-escalation headline on Iran/Hormuz easing macro risk, or BTC reclaiming its local downtrend structure, or any of the watchlist names printing a fresh verified catalyst

## 7. Candidate Deep Dives

### 1. BANK/USDT (long-watch, C-tier, score 51.9)

- Has price already reacted to the catalyst? No catalyst exists — this is pure momentum/RS, not catalyst-driven.
- Is the setup chasing? Yes at current price (0.3498) — the report's own pullback zone (0.3343-0.3450) sits below spot.
- Retest/pullback structure? Defined but not yet reached; would need price to come back into 0.3343-0.3450 and hold.
- Overextended? 7d +215.1% is extreme; 24h +16.3% alone is not, but the multi-day move is a major chase-risk flag.
- Would entry now be late? Yes.
- Actionable level: 1h close holding 0.3343-0.3450 with improving volume (currently 0.35x average).
- Aligned with market mood? Partially — RS-leader longs fit a mixed/chop regime better than fresh breakouts, but the lack of any catalyst confirmation keeps this speculative.
- Long/short/wait: wait-for-trigger, long bias if triggered.
- Actionable now or after confirmation? After confirmation only (pullback + volume).
- Invalidation: 1h close beyond 0.3213.
- Chase risk: high at current price.
- Catalyst confirmation/contradiction: none — internal `news_items` show zero fresh (24h) hits for BANK.

### 2. ALLO/USDT (short-watch, C-tier, score 50.2)

- Has price reacted to a catalyst? No catalyst — pure weak-RS/momentum short thesis (-27.5% RS vs BTC).
- Chasing? Current price (0.3771) is below the failed-bounce entry zone (0.3815-0.3913), so a fresh short here without the bounce would itself be chasing the move down.
- Retest structure? Defined: needs a bounce into 0.3815-0.3913 that fails.
- Overextended? Already down significantly (24h -27.1%, 7d -16.2%); derivatives show deleveraging (OI -9.86%), consistent with long liquidation rather than fresh short pressure.
- Would entry now be late? Yes, for a fresh short without the retest.
- Actionable level: failed bounce/retest of 0.3815-0.3913, then 1h close below 0.3552.
- Aligned with market mood? Yes for a risk-off/chop tape, but squeeze risk is explicitly elevated — the system flags a heavily short-skewed global long/short ratio on this name, raising squeeze-covering risk.
- Long/short/wait: wait-for-trigger, short bias if triggered.
- Invalidation: 1h close beyond 0.4034.
- Chase risk: moderate — the setup requires patience for the retest, which mitigates but does not eliminate it.
- Catalyst confirmation/contradiction: none — no fresh internal news for ALLO in 24h.

## 8. Best Candidates Ranked

1. **BANK/USDT — long-watch** — trigger: 1h close holding 0.3343-0.3450 pullback zone with improving volume; invalidation 1h close beyond 0.3213.
2. **ALLO/USDT — short-watch** — trigger: failed bounce/retest of 0.3815-0.3913 then 1h close below 0.3552; invalidation 1h close beyond 0.4034.
3. **NEAR/USDT — catalyst-watch, low confidence** — trigger: needs a scored technical setup to clear the intraday/scalp funnel before the ai_narrative basket (fresh<1h) becomes actionable; currently only a weak single-source article, not a real event.
4. **AERO/USDT — manage existing OPEN short**, TP1 booked, window closes 09:54 EEST today; not a fresh idea.

_Stocks: market closed for the weekend — MSFT and TSLA (AVOID/manual-review, legal flags) and UNH (active C-tier invest position, DOJ antitrust flag) all carry forward unchanged into Monday's pre-open, not re-verified this cycle._

## 9. Avoid / No Trade

This decision window only — scanning, tracking, and the scheduler continue unaffected.

- **EUL/USDT** — avoid chasing a fresh long here: 7d +86.9%, 24h +64.6%, no fresh verified catalyst, own report score (51.9) explicitly below active-trade threshold. The prior EUL long already closed WIN (tp3_hit); this is a warning against chasing a new entry, not a position to manage.
- **ALLO/RIF/AIXDROP/ACE** — avoid fresh shorts without a confirmed failed-bounce structure; all four are squeeze-capped by the system's own guardrails tonight, meaning the short-crowding risk is elevated across this entire cohort.
- **Crypto scalp mode generally** — avoid treating any scalp-mode idea as more than data-collection; PF 0.72 / avgR -0.086 / totalR -3.10 on n=45, a reproducibly losing bucket (see §14).

## 10. Main Risks

- Geopolitical: Iran/Israel/Houthi conflict remains live and unresolved; a further escalation (or de-escalation) could move BTC sharply in either direction overnight while liquidity is thin (Asia session, weekend).
- Squeeze risk: the weak-name cohort (ALLO/RIF/AIXDROP/ACE/VANA) is uniformly squeeze-capped — a short squeeze across this basket is a live tail risk if any of them catches a bounce.
- Chase risk: EUL/BANK/SHIB are all extended RS leaders with no catalyst backing; a reversal from these levels would be sharp given thin volume confirmation (0.35x-0.48x average).
- Data-quality: many "active" signals (15 crypto, ~49 stocks) carry expires_at dates well in the past while still showing tp1/tp2_hit/triggered status — see §14 TODO; this does not change any live routing but could confuse manual review of "what's actually still open."
- Stocks: closed, so no intraday risk this window, but MSFT/TSLA legal flags and UNH's DOJ antitrust flag are carried unverified into Monday.

## 11. Action Plan — next 4 hours

- Monitor AERO/USDT short through its 09:54 EEST expiry; no action needed unless price structure changes materially.
- Watch BANK/USDT for a pullback into 0.3343-0.3450 with volume confirmation before considering it actionable.
- Watch ALLO/USDT for a failed bounce into 0.3815-0.3913 before considering a short.
- No new entries recommended without one of the above triggers or a fresh verified catalyst.
- Continue scanning, data collection, and tracking as normal — no system changes.

## 12. Final Verdict per Mode

- **Scalp:** No trade. Persistent losing bucket (PF 0.72, n=45) — data collection only, re-audit overdue per the report's own 20-signal threshold (carried TODO, §14).
- **Intraday:** No trade. No A/B setups; best watchlist names (BANK/EUL/SHIB/ALLO/DEXE) all below active-trade threshold.
- **Swing:** No trade; report stale (>14h) and contained no A/B setups regardless.
- **Stocks (all modes):** Closed for the weekend. No trade possible; carried legal/DOJ flags stand unverified into Monday.

## 13. Sources

- [Crypto Prices on Edge as Iran Claims Strait of Hormuz Closure — Again](https://cryptoticker.io/en/crypto-prices-iran-hormuz-closure-again-impact/)
- [Bitcoin holds near $65,000 as the Iran conflict sends oil to a two-month high: Crypto Markets Today](https://www.coindesk.com/markets/2026/07/24/bitcoin-settles-near-usd65-000-as-oil-s-march-toward-usd100-fails-to-spook-the-market)
- [Oil Hits $100 as Iran Tensions Escalate — Why Bitcoin and Altcoins Are Falling](https://cryptoticker.io/en/oil-hits-100-iran-tensions-bitcoin-altcoins-fall/)
- [Bitcoin breaks below $65K as Trump threatens massive Iran attack](https://crypto.news/bitcoin-breaks-below-65k-as-trump-threaten-iran-attack/)
- Internal: `data/reports/scalp/2026-07-25_23-32_scalp_report.md`, `data/reports/intraday/2026-07-25_23-41_intraday_report.md`, `data/catalysts/2026-07-26/catalyst_events.jsonl`, `db/crypto_ai_desk.sqlite` (news_items, proposed_signals, signal_outcomes queries), `OPUS_ENRICHED_REVIEW_AUTO_2026-07-25_2332.md`.

## 14. Fix Requests / TODO

### TODO-stale-active-signals (carried/re-raised)
- **issue:** `active-signals` continues to list many crypto (15 of 16) and stocks (majority of 50) signals with `expires_at` dates well in the past (crypto: 2026-07-17 to 2026-07-22, up to 9 days old; stocks: 2026-07-03 to 2026-07-21, up to 23 days old) while still showing `tp1_hit`/`tp2_hit`/`triggered` status rather than a terminal closed state. This is the same pattern noted in the prior review's TODO-2/TODO-3 lineage (scalp/track-signals overlap) but specifically about the "active" list's terminal-state hygiene, not the overlapping-invocation issue. Not necessarily a bug — may be correct-by-design if a signal stays "active" until a final TP/stop/max-hold event regardless of its display `expires_at` — but the mismatch makes manual review of "what's genuinely still open" harder without cross-referencing `signal_outcomes`.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` (16 rows, only `sig_f19116dc366e4110` AERO has a future `expires_at`); `python -m src.cli active-signals --asset-class stocks` (50 rows, only the 6 `invest`-mode rows with `2026-08-01`/`2026-07-31` expiries are future-dated).
- **suggested manual fix:** a human session should confirm whether `active-signals` is intended to filter on `expires_at` at all, or whether "active" correctly means "not yet formally closed" independent of the display expiry; if the latter, consider adding an explicit `past_expiry` flag column to the CLI output so reviews don't need to eyeball dates.
- **priority:** low (no functional/routing impact observed; readability issue for manual review only).
- **first observed:** carried context from multiple prior reviews' "entered unresolved" counts; explicitly raised as its own TODO 2026-07-26 04:40 EEST.

## Telegram

```
[AUTO-REVIEW crypto overnight / Asia review 04:40 EEST]

Mood:
- Crypto: risk-off/chop (BTC/ETH downtrend, macro risk 100/100, breadth mixed)
- Stocks: closed (Sunday, reopens Monday 2026-07-27)
- Prefer: wait-for-trigger / manage existing position

Status:
- Open actionable: 1 (AERO/USDT short, TP1 booked, window closes 09:54 EEST today)
- Waiting for entry: 0
- Review/Shadow: 5 (BANK/EUL/SHIB/ALLO/DEXE C-tier watchlist ideas)
- Entered unresolved: 15 crypto (TP touched, windows closed 07-17 to 07-22) + ~49 stocks (TP touched/triggered, windows closed, market shut)
- No-entry/stale/moved-away: 0 this cycle
- Needs review: 1 (stale-active display hygiene, see TODO)

Decisions:
- Long-watch:     BANK/USDT trigger 1h close holding 0.3343-0.3450 w/ rising volume
- Short-watch:    ALLO/USDT trigger failed bounce 0.3815-0.3913 then close <0.3552
- Catalyst-watch: NEAR/USDT trigger needs a scored technical setup (ai_narrative basket fresh<1h, weak evidence only)
- Avoid:          EUL/USDT — 7d +86.9%, no catalyst, chase risk

Risk:
- Iran/Israel/Houthi escalation live; Hormuz de-facto closed, Brent >$100 — macro risk 100/100, thin weekend liquidity.

Catalyst coverage: mapped 123/349 (35.2%), baskets 5
                   weak this run — context only, early UTC-day sample

File: OPUS_ENRICHED_REVIEW_LATEST.md
Advisory only. No auto-trade.
```
