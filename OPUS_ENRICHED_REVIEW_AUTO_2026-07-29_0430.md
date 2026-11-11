# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

Slot: **crypto overnight / Asia review** (stocks closed — planning/watchlist context only; crypto is the live actionable class). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** Crypto stays risk-off/bearish (BTC downtrend, ETH uptrend divergence, altcoin breadth a weak 26.3% above EMA20), with macro risk pinned at 100/100 on the Iran missile-attack-on-US-forces headline, Senate Russia-sanctions vote, and an approaching Fed decision (external check: BTC range-bound ~$63.4K, ETH $1,850-1,970, both pressured into FOMC). Zero A/B-tier setups on any crypto mode this cycle (scalp/intraday/swing all report "No A-tier / No B-tier setups found") — this is now a C-tier watchlist-only night. The standing priority item, **ZEC/USDT short (catalyst-linked to the Zcash Ironwood upgrade)**, has progressed favorably from TRIGGERED to **TP1_HIT** overnight — a partial win, still running toward invalidation 476.29. Two recurring data-integrity issues escalate this cycle: the **XLE short-vs-strongest-sector contradiction** (now 5th+ consecutive cycle unresolved) and a **new, cleanly-evidenced legal-risk gate false-positive on META** (an "indictment" tag pulled from an unrelated James Comey story purely on the word "Instagram"), alongside the AMZN going-concern false-positive recurring for a 2nd cycle. Scanning, tracking, and monitors continue in all moods; this review recommends caution, never a stop.

## 2. Data Used

| File | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-29_00-37_scalp_report.md` | 03:37 EEST | ~1h |
| `data/reports/intraday/2026-07-29_00-47_intraday_report.md` | 03:47 EEST | ~52m |
| `data/reports/swing/2026-07-28_19-31_swing_report.md` | 22:31 EEST (Jul 28) | ~6h08m — **carry-forward** |
| `data/reports/stocks/intraday/2026-07-29_01-33_stocks_intraday_report.md` | 04:33 EEST | ~6m (market closed — planning only) |
| `data/reports/stocks/swing/…` / `invest/…` | 2026-07-02 | deprecated/removed playbooks — not treated as stale, see [[project_crypto_ai_desk_stocks_position_framework]] |
| `data/catalysts/2026-07-29/catalyst_cycle_00-53.md` + `catalyst_events.jsonl` + `narrative_baskets.jsonl` | 03:53 EEST | ~46m |
| `data/processed/llm_analysis_packet.md` | 03:48 EEST | ~51m |
| `data/processed/llm_stocks_packet.md` | 04:36 EEST | ~3m |
| `python -m src.cli active-signals --asset-class crypto` | live query | now |
| `python -m src.cli active-signals --asset-class stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` | live query | now |
| `python -m src.cli signal-stats --asset-class stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-29` | live query | now |
| `data/scheduled_runs/2026-07-29_default_schedule/scheduler.log` | 02:47 EEST | ~1h52m |
| `data/scheduled_runs/2026-07-28_default_schedule/cycle_02_00-37_summary.md` | 01:22 EEST | ~3h17m — last **completed** cycle (today's folder only has a dry-run so far) |
| WebSearch: BTC/ETH price action ahead of Fed decision | live, 2026-07-29 | for §6 external grounding |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-28_2330.md` | 23:30 EEST (Jul 28) | for §4 diff |

## 3. Scheduler / Data Freshness

- Latest scheduled-run folder: `data/scheduled_runs/2026-07-29_default_schedule/` — contains only a `DRY RUN` validation pass (02:40-02:41) plus the background derivatives monitor so far; the last **completed** production cycle is `cycle_02_00-37_summary.md` in yesterday's folder (finished 01:22 EEST, ~3h17m ago).
- `scheduler.log` mtime: 02:47:31 EEST — **fresh** (<3h rule easily met, ~1h52m old). Per §D, freshness only requires ONE of the two checks to be fresh — no defer.
- Reports: scalp/intraday **fresh** (<1h); stocks intraday **fresh** (<10m, but market closed — planning-only); swing **carry-forward** (~6h08m, inside the 4-12h window).
- Catalyst layer: fresh (<1h, scan `catalyst_cycle_00-53.md`). LLM packets: fresh (<1h).
- Last completed cycle (`cycle_02_00-37_summary.md`, 00:37→01:22 EEST window): **0 FAIL entries** — clean run. All monitors reported OK: crypto watchlist monitor (5m), crypto pending monitor (30s, entry→alert p90 20.0s), MEXC canary, derivatives monitor, fast Finnhub news monitor, stocks monitor, news source health monitor (OK 47 / ERROR 1 / alerts_sent 1 — one source degraded, non-blocking), news entity resolver health (0 unresolved symbol-tagged rows).
- Paper monitor status (from the same completed cycle, Telegram-sent 01:22 EEST): Open actionable 1 · Waiting for entry 0 · Entered unresolved 0 · Review/Shadow 30 · No-entry/stale/moved-away 92 · Needs review 1 · Closed today 162W/16L/22flat (paper P&L, not live).
- `detect_untracked_legacy_alerts --since 2026-07-29`: **None** — every legacy crypto alert has a backing proposed_signal; no integrity anomaly today.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-29 04:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh"],
      "data_missing": ["today's folder has no completed production cycle yet, only a dry-run — last completed cycle is in yesterday's folder", "swing report is carry-forward (~6h08m old, inside 4-12h window)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 02:47 EEST, ~1h52m old", "cycle_02_00-37_summary.md: 0 FAIL entries, all monitors OK", "scalp/intraday/stocks-intraday reports <1h old, catalyst scan <1h old"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.8,
      "reason_codes": ["risk_off", "mixed", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC downtrend, ETH uptrend divergence, altcoin breadth 26.3% above EMA20 (weak)", "macro risk 100/100: Iran missile attack on US forces, Senate Russia-sanctions vote, oil price jump", "stocks risk_off/short-bias regime carried forward (market closed): VIX 18.21, QQQ downtrend -4.72% 5d, energy/financials/healthcare strong vs semis/tech weak", "external WebSearch: BTC range-bound ~$63.4K, ETH $1,850-1,970, both pressured ahead of Fed decision"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "catalyst_contradicted"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["181/500 catalyst events mapped today (36.2%), 319 unmapped (63.8%) — weak-mapping threshold breached", "4 narrative baskets: perps_dex (HYPE), rwa (ONDO/XLM), ai (NEAR/RENDER/TAO/FET), momentum_breakout (ZIL, no news)", "ZEC/USDT Ironwood-upgrade catalyst now at TP1_HIT — sell-the-news thesis confirmed favorably", "META legal_risk tag (importance 0.86) traced to an unrelated James Comey indictment story matched purely on the word 'Instagram' — contradicted, false-positive"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["data_unavailable", "oi_supports", "squeeze_risk"],
      "data_missing": ["SNXXB/USDT, SOXLB/USDT, SNDKB/USDT, SKHYB/USDT, LA/USDT external futures data"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZIL/USDT: price up + OI up +80.08% 24h — fresh positioning confirms trend, crowding unknown", "ALLO/USDT: price down + OI down -5.75% — deleveraging/long liquidation", "BANK/USDT: OI 24h n/a this cycle, funding neutral, crowding normal — squeeze flag from prior cycles not repeated tonight"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["chase_risk", "overextended", "entry_fresh", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZIL/USDT +21-25% 24h, RS vs BTC +23.8%, momentum_breakout basket primary — already extended, chase risk on a fresh long, counter-tape (BTC downtrend) per report's own counter-thesis", "BANK/USDT -38 to -40% 24h — extended short, no fresh catalyst, watchlist only", "ZEC/USDT: entry already filled and TP1 realized; remainder is a running position, not a fresh entry decision"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["entered_unresolved", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 19/19 rows ENTERED UNRESOLVED (tp1_hit/tp2_hit), 0 open/waiting/triggered fresh", "stocks active-signals: 50 rows, 20 WAITING FOR ENTRY (all C-tier, not Telegram-actionable), rest closed/aged, 0 A/B", "paper monitor (01:22 EEST): open actionable 1, review/shadow 30, no-entry/stale/moved-away 92, needs review 1", "several crypto ENTERED UNRESOLVED rows aged 7-12+ days past their mode's typical horizon (NEAR scalp exp 2026-07-17, ONDO/OPN/FIL scalp exp 2026-07-22, ALLO intraday exp 2026-07-19 weekend)", "detect_untracked_legacy_alerts: none — clean"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["META tagged legal_headline_risk=indictment; the only META news item this cycle is 'Comey Attorneys Seek Dismissal Of Indictment Over 86 47 Instagram Post' — about James Comey, not Meta Platforms — false-positive gate", "AMZN tagged legal_headline_risk=going_concern for a 2nd consecutive observed cycle; AMZN's own news feed (store closures, Prime Day cookware) has no going-concern content — recurring false-positive", "UNH tagged legal_headline_risk=sec_doj; this cycle's UNH news feed (Buffett/Berkshire rally, Medicare drug pricing, Humana earnings) has no SEC/DOJ content — unsupported this cycle", "MSFT and META both report earnings TODAY (2026-07-29) — do_not_chase_warning active on both", "macro risk 100/100 (Iran missile attack on US forces)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week (tier=B, n=100): PF 2.47, winrate 26.3%, totalR +30.8", "by mode: swing PF 4.30/totalR +23.1 (strongest), intraday PF 2.30/totalR +11.7 (working), scalp PF 0.20/0W-5L/totalR -4.0 (net-negative, kill-switched, unchanged)", "stocks C-tier week (n=181): PF 0.43, winrate 5%, totalR -4.0 (weak; no A/B sample this week, headline n=0)"] },
    { "agent": "head_trader", "verdict": "manual_review", "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of agents 1-8"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "ZIL/USDT", "trigger": "confirmed pullback/retest into the 0.0028-0.0029 zone with rising volume; do not chase the current +21-25% 24h extension", "reason": "Top RS-leader (score up to 90.2) and sole `momentum_breakout` narrative-basket primary, but counter-tape against a BTC downtrend — reduce size and demand confirmation per the report's own counter-thesis" },
    "best_short_candidate":    { "symbol": "ZEC/USDT", "trigger": "already open, now TP1_HIT; manage the runner to invalidation 476.2871 or next TP, no new entry needed", "reason": "Catalyst-confirmed sell-the-news reaction to the Zcash Ironwood upgrade; only signal on the desk that has actually resolved favorably this window" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "same as best-short — catalyst and technical align, TP1 already realized", "reason": "Cross-confirmed by two independent sources in the prior cycle (CoinDesk upgrade-live + BeInCrypto price-reaction); internal-first bar satisfied again this cycle by the active-signals status update" },
    "avoid_candidate":         { "symbol": "BANK/USDT", "reason": "-38 to -40% 24h, already deeply extended on both sides, no fresh verified catalyst, score capped at watchlist-only (60/100) — chasing either direction here is late; distinct from the internally-contradictory tagging seen in the 23:30 cycle, which appears to have normalized tonight" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---:|---|---|
| data_quality | ok | 0.85 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.80 | risk_off, mixed, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, narrative_supported, catalyst_contradicted | advisory_only |
| derivatives_squeeze | caution | 0.50 | data_unavailable, oi_supports, squeeze_risk | advisory_only |
| technical_entry | caution | 0.65 | chase_risk, overextended, entry_fresh, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.70 | entered_unresolved, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (23:30 EEST, post-close final daily review)

- **ZEC/USDT short**: was `TRIGGERED` (entry 469.62-472.62 filled) → now **TP1_HIT** — the position has run favorably overnight; remaining size still open toward invalidation 476.2871, expires 2026-07-29T17:36 EEST.
- **COTI/USDT**: no longer appears as a live RS-leader long-watch name in tonight's reports (dropped out of the strongest-symbols table); **ZIL/USDT** has taken over as the desk's clearest RS-leader / momentum-basket long-watch candidate (+21-25% 24h, RS vs BTC +23.8%, sole `momentum_breakout` basket primary).
- **XLE short vs strongest-sector contradiction**: still open. XLE remains the raw "was A" short (score 89 this cycle) while energy stays the day's single strongest sector (RS +7.47% this cycle). This is now the **5th+ consecutive review cycle** with the same unresolved contradiction (first flagged 16:07 EEST yesterday) — escalated further in §14.
- **AMZN going_concern tag**: still present, still unsupported by AMZN's own news feed this cycle (store-closure/Prime-Day items only) — **2nd consecutive cycle observed with this exact pattern**, escalating priority in §14.
- **New this cycle**: **META tagged `legal_headline_risk=indictment`** — traced to a James Comey court story that only mentions "Instagram" in its headline, with zero connection to Meta Platforms itself. This is a clean, high-confidence false-positive and a new integrity flag (see §14).
- **Crypto desk**: still zero A/B-tier ideas on scalp/intraday/swing, same as 23:30 — no change in actionability, all C-tier watchlist only.
- **Stocks desk**: all previously-listed A/B-raw candidates remain demoted to C by the market-closed gate; UNH's `sec_doj` tag persists but is unsupported by this cycle's own news feed (rally/Medicare-pricing/Humana-earnings stories only) — worth the same false-positive scrutiny as AMZN/META, noted but not yet escalated to its own TODO pending one more observation.
- **Scheduler**: today's folder has not yet completed a production cycle (only a dry-run so far) — this review relies on yesterday's last completed cycle (01:22 EEST) for lifecycle/monitor counts, cross-checked against fresh live CLI queries and fresh reports for market data.

## 5. Catalyst Coverage

- Catalyst events today: **500** scanned this cycle; **181 mapped** (36.2%) / **319 unmapped** (63.8%).
- Narrative baskets: **4** — `perps_dex_narrative` (HYPE + DYDX/GMX/ASTER), `rwa_narrative` (ONDO/XLM), `ai_narrative` (NEAR/RENDER/TAO/FET + WLD/ASTER), `momentum_breakout` (ZIL, no confirmed news).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped 63.8% > 50% threshold)
- Top unmapped headlines by importance:
  1. `0.73` — "Thailand SEC accuses Bitkub executives of hiding $50 million hack losses in official reports" (t.me/whale_alert_io)
  2. `0.73` legal_risk — "PODD Investors Have Opportunity to Lead Insulet Corporation Securities Fraud Lawsuit" (PR Newswire)
  3. `0.73` legal_risk — "Badger Meter, Inc. (BMI) Investors Who Lost Money Have Opportunity to Lead Securities Fraud Lawsuit" (PR Newswire)
- Top *mapped* catalyst by importance this cycle is itself a flagged issue: `0.86` **META** [legal_risk] — the Comey/Instagram false-positive discussed in §4/§7/§14.

## 6. Market Landscape

Crypto: bearish trend / risk-off. BTC downtrend, ETH uptrend (mild divergence), altcoin breadth weak (26.3% above EMA20/EMA50). Macro risk score 100/100 driven by the Iran missile-attack-on-US-forces headline, a Senate vote to sanction Russia over Ukraine, and oil-price jump headlines; an FOMC decision is the dominant near-term catalyst per external check (BTC range-bound ~$63.4K, ETH $1,850-1,970, both pressured into the Fed). Stocks (closed, carry-forward context only): risk_off, bias short, VIX 18.21, breadth 25% above EMA20; QQQ in a clean downtrend (5d -4.72%, 20d -6.71%) while DIA/SPY/IWM range-bound. Sector split unchanged: energy/financials/healthcare strong (energy RS +7.47%), semiconductors/technology weak (SMH RS -16.18%). MSFT and META both report earnings **today** (2026-07-29); AAPL/AMZN/COIN/MSTR/LRCX/MA follow over the next 1-2 days — a live gap-risk cluster into the US session.

### Market Mood / Risk Routing
- Crypto mood: **risk-off / bearish trend**
- Stocks mood: **risk_off / closed (overnight, planning only)**
- Dominant narrative: geopolitical risk-off (Iran/Russia headlines) + FOMC-decision positioning + earnings kickoff (MSFT/META today)
- Preferred side now: **wait-for-trigger** (crypto: manage the open ZEC short, size-reduced RS-leader longs only on confirmed pullback; stocks: nothing actionable until RTH open)
- Best long candidate: **ZIL/USDT** (RS-leader, momentum-basket primary, but chase-risk at current extension — see §8)
- Best short candidate: **ZEC/USDT** (open, TP1_HIT, catalyst-confirmed — manage the runner)
- Best catalyst-backed candidate: **ZEC/USDT** (same name — catalyst and technical align)
- What to avoid: chasing ZIL/USDT at the current +21-25% extension; fresh entries on BANK/USDT (deeply extended both directions, no catalyst); any stock name into today's MSFT/META earnings prints or the AAPL/AMZN/COIN/MSTR/LRCX/MA prints over the next two days
- What would change the view: BTC reclaiming key resistance with altcoin breadth improving above 50% on EMA20; a dovish/neutral Fed surprise; a confirmed SPY/QQQ breakdown for a cleaner stocks-short entry after the reopen

## 7. Candidate Deep Dives

### 1. ZEC/USDT — crypto intraday short, B-tier, TP1_HIT (score 65.2)
- Entry zone: 469.6229-472.6218 (filled) · Invalidation: 476.2871 · Expires: 2026-07-29T17:36 EEST.
- Has price already reacted to the catalyst? Yes — confirmed sell-the-news fade on the Zcash Ironwood upgrade, and the trade has since realized TP1.
- Chasing? No — already open, no new entry decision required.
- Retest/pullback structure? N/A — managing an existing runner.
- Overextended? Not flagged.
- Would entry now be late? N/A — already filled and partially realized.
- Mood alignment: yes — risk-off crypto favors clean catalyst-backed shorts; this one has already paid.
- Long/short/wait: managing an open short.
- Actionable now or confirmation-only? Already actionable/open; monitor to invalidation or next TP.
- Chase-risk setup? No.
- Catalyst confirmation or contradiction? Confirmed, unchanged from the prior cycle — no new external verification needed (internal-first bar satisfied by the status transition itself).

### 2. ZIL/USDT — crypto intraday/scalp long-watch, RS-leader, C-tier watchlist (score up to 90.2 raw / 57.9 gated)
- Has price already reacted? Yes — +21 to +25% 24h, RS vs BTC +23.8%, OI +80.08% 24h (fresh positioning, not yet flagged as crowded).
- Chasing? Yes, at current levels — the report's own counter-thesis flags this explicitly ("counter-tape long — reduce size").
- Retest/pullback structure? Conditional pullback zone identified: 0.0028-0.0029.
- Overextended (>2 ATR from EMA20)? Not explicitly measured in the report, but the 24h move size argues for caution.
- Would entry now be late? Yes, at the current price.
- What level makes it actionable? A confirmed pullback into the 0.0028-0.0029 zone with rising volume, or score crossing the active-trade threshold (currently capped at 37/100 on the risk gate despite a 71.3 setup-quality read).
- Mood alignment: RS-leader longs are the correct risk-routing choice in a risk-off tape, but BTC is in a downtrend — this is explicitly a counter-tape trade, size-reduce only.
- Long/short/wait: long-watch, wait-for-trigger.
- Invalidation: 1h close below 0.0026, or the RS-leadership fading against BTC.
- Chase-risk setup? Yes, at current price.
- Catalyst confirmation/contradiction: no news catalyst — pure momentum (`momentum_breakout` basket, "top gainers without confirmed news catalyst").

### 3. META — stocks C-tier watchlist (was B, score 70), `legal_headline_risk=indictment` — **false-positive, integrity issue**
- Has price already reacted? Not evaluated — market closed; also moot, since the underlying tag does not describe a real Meta Platforms event.
- Legal/headline risk check (§I): the only META-tagged news item this cycle is "Comey Attorneys Seek Dismissal Of Indictment Over '86 47' Instagram Post" (t.me/zerohedge) — this is about James Comey's legal case and only mentions "Instagram" incidentally. There is no Meta Platforms indictment, investigation, or legal action in evidence.
- Per §I policy: because a legal/headline flag is present (even though it looks mislabeled), the verdict for this candidate stays **MANUAL REVIEW REQUIRED**, not a clean actionable — but the underlying tag itself should be treated as almost certainly spurious.
- Earnings: META reports **today** (2026-07-29) — an independent, valid reason for do-not-chase regardless of the legal-tag question.
- Mood alignment: n/a — not actionable either way tonight (market closed + earnings blackout + spurious legal tag).
- What would clear it: a human confirming the tag is a keyword-collision false-positive (see §14), or the earnings window passing with a clean post-print setup.

### 4. AMZN — stocks C-tier watchlist (was B, score 79), `legal_headline_risk=going_concern` — **recurring false-positive, 2nd cycle observed**
- Has price already reacted? Not evaluated; market closed.
- Legal/headline risk check (§I): AMZN's own news feed this cycle contains only "87-year-old grocery giant closing more stores" and two duplicate "Prime Day 2026 Home & Kitchen Winners" market-defense-report items — none support a going-concern, bankruptcy, auditor-resignation, or accounting-restatement label. This is the same pattern flagged at 23:30 EEST last cycle, now confirmed recurring rather than a one-off.
- Per §I policy: verdict stays **MANUAL REVIEW REQUIRED** until a human clears or confirms the tag.
- Earnings: AMZN reports in ~1 day — independent do-not-chase reason regardless.
- What would clear it: a human audit of the going_concern gate logic (see §14, now escalated to high priority given 2-cycle recurrence).

### 5. XLE — stocks C-tier watchlist (was A, score 89), sector-strength contradiction — **5th+ consecutive cycle unresolved**
- Has price already reacted? Sector rotation shows energy (XLE) as the **strongest** sector again tonight (RS vs SPY +7.47%, 20d return +7.45%) — this directly opposes a fresh short thesis, unchanged from every prior cycle since 16:07 EEST yesterday.
- Chasing? Would be chasing against the day's strongest sector.
- Mood alignment? **No** — same unresolved contradiction, now spanning at least five review cycles (16:07, 18:39, 21:41, 23:30, and tonight's 04:33 report) without the gate distinguishing "no sector info" from "sector info present and directionally opposed."
- Actionable now or after confirmation? After confirmation only, and specifically after the underlying gate-logic question is investigated (§14, escalated).
- Catalyst confirmation/contradiction: **contradicted** by the sector-rotation data itself, same as every prior cycle.

## 8. Best Candidates Ranked

1. **Best catalyst-backed / best short (crypto): ZEC/USDT short** — open, TP1_HIT, invalidation 476.2871, expires 2026-07-29T17:36 EEST. Manage the runner; no new entry needed.
2. **Best long-watch (crypto): ZIL/USDT** — trigger: confirmed pullback/retest into 0.0028-0.0029 with rising volume; do not chase the current +21-25% extension; counter-tape vs BTC downtrend, reduce size.
3. **Manual-review / avoid (stocks): META** — earnings today + a near-certainly spurious `indictment` legal tag (keyword collision on "Instagram" with an unrelated Comey story); needs a human call to clear the tag.
4. **Manual-review / avoid (stocks): AMZN** — earnings in ~1 day + `going_concern` tag unsupported by its own news feed for a 2nd straight cycle; escalated in §14.
5. **Avoid (stocks): XLE short** — contradicts the day's strongest sector for a 5th+ consecutive cycle; escalated in §14.

## 9. Avoid / No Trade

This is a **decision-window-only** call, not a system-wide stop — scanning, tracking, and monitors continue regardless.

- **META / AMZN shorts or any action** — both blocked by same-day/near-term earnings prints plus unresolved, likely-spurious legal-tag questions → MANUAL REVIEW REQUIRED.
- **XLE short** — directly contradicts the day's strongest sector for a 5th+ cycle; needs the gate-logic contradiction resolved before trusting the raw score.
- **Any fresh chase on ZIL/USDT** at the current +21-25% extension — wait for the pullback zone.
- **Fresh entries on BANK/USDT** — deeply extended both directions (-38 to -40% 24h), no catalyst, watchlist-only score.
- **Crypto scalp mode** — still net-negative on the historical/tracking series this week (PF 0.20, 0W-5L, totalR -4.0); no new scalp ideas expected or wanted.
- Nothing here is a command to pause the scanner, monitors, or data collection — all continue.

## 10. Main Risks

- **Earnings gauntlet**: MSFT/META today, AAPL/AMZN/COIN/MSTR/LRCX/MA over the next 1-2 days — do not hold or chase into any of these prints.
- **Geopolitical risk-off**: Iran missile-attack-on-US-forces + Russia-sanctions headlines keep the macro risk score pinned at 100/100.
- **FOMC decision looming** — external check confirms BTC/ETH both range-bound/pressured ahead of the Fed, a real catalyst for a regime shift in either direction.
- **Catalyst mapping is weak this run (63.8% unmapped)** — treat catalyst context as directional color, not proof.
- **Legal/headline gate false-positive pattern is spreading**: now 3 symbols in as many cycles (AMZN twice, UNH once, META new tonight) — confidence in the legal-risk gate keeps degrading (§14).
- **Aged ENTERED UNRESOLVED crypto signals**: several scalp/intraday B-tier rows are 7-12+ days past their mode's typical horizon without resolving to a terminal state (§14, carried).

## 11. Action Plan — next 4 hours

1. **Manage ZEC/USDT short** to invalidation (476.29) or next TP; no new entry needed, already TP1_HIT.
2. **Watch ZIL/USDT** for a pullback/retest into 0.0028-0.0029 with volume before considering it actionable; do not chase the current extension.
3. **Do not originate new crypto entries** on BANK/USDT or other deeply-extended no-catalyst names without a fresh signal.
4. **Stocks: nothing actionable** until the RTH open; re-evaluate XLE/META/AMZN/PLTR/AMD/AVGO/QQQ/UNH fresh at/after 09:30 ET — do not treat tonight's C-tier planning levels as pre-authorized entries.
5. **Flag META, AMZN, and XLE for human review** before the next US session per §14 — all three carry unresolved gate questions.
6. Continue all scanning/monitoring — no pause recommended in any mood.

## 12. Final Verdict per Mode

- **Crypto scalp**: NO-ENTRY / kill-switched — net-negative bucket this week, no change expected.
- **Crypto intraday**: NO-ENTRY this cycle (0 A/B ideas) — WATCHLIST ONLY (best long-watch: ZIL/USDT; best short-watch already open: ZEC/USDT).
- **Crypto swing**: NO-ENTRY this cycle (0 A/B ideas, report carry-forward ~6h old) — no fresh long-watch name identified in the carried report beyond the intraday-desk's ZIL/USDT read.
- **Crypto — open positions**: ZEC/USDT short TP1_HIT, manage the runner; remaining 18 active B-tier signals are ENTERED UNRESOLVED (tp1_hit/tp2_hit) — no new action needed, several aging well past their mode horizon (§14 carried TODO).
- **Stocks intraday**: MARKET CLOSED — planning/watchlist only; all A/B-raw candidates demoted to C by the market-closed gate; re-confirm fresh at RTH open; META and AMZN additionally blocked by likely-spurious legal tags pending human review.
- **Stocks swing/invest**: deprecated/removed, not evaluated (new `stocks_swing_growth_breakout` remains shadow-only research, not actionable).

## 13. Sources

- [Bitcoin, Ethereum and XRP Price Prediction (July 29): Can BTC Hold Above $63K Ahead of Fed Decision?](https://sundayguardianlive.com/business/bitcoin-ethereum-and-xrp-price-prediction-july-29-can-btc-hold-above-63k-ahead-of-fed-decision-check-btc-eth-and-xrp-forecast-key-support-resistance-market-outlook-more-248285/) — Sunday Guardian Live, accessed 2026-07-29
- [Bitcoin and ethereum prices today, Tuesday, July 28, 2026: Crypto prices slide ahead of Fed meeting](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-tuesday-july-28-2026-crypto-prices-slide-ahead-of-fed-meeting-125210301.html) — Yahoo Finance, 2026-07-28
- `data/reports/intraday/2026-07-29_00-47_intraday_report.md` §5 — internal source for the ZEC/USDT catalyst and Iran/Russia macro headlines
- `data/catalysts/2026-07-29/catalyst_cycle_00-53.md` — internal source for the META false-positive legal-risk tag and catalyst coverage stats
- `data/reports/stocks/intraday/2026-07-29_01-33_stocks_intraday_report.md` §2, §4, §7 — internal source for the XLE sector-strength contradiction and the AMZN/UNH news-feed checks
- Internal `active-signals`/`signal-stats` CLI outputs (live queries, this run) — for lifecycle status and playbook performance

## 14. Fix Requests / TODO

### TODO-meta-indictment-tag-keyword-collision-false-positive (new, high)
- **issue:** META is tagged `legal_headline_risk: indictment` (importance 0.86, the top *mapped* catalyst this cycle) purely on a headline containing the word "Instagram" — "Comey Attorneys Seek Dismissal Of Indictment Over '86 47' Instagram Post" (t.me/zerohedge). This story is about James Comey's legal proceedings and has zero connection to Meta Platforms Inc. This is a clean, high-confidence keyword-collision false-positive, the same class of bug as the recurring AMZN going_concern tag, now confirmed on a second, more obvious case.
- **evidence:** `data/catalysts/2026-07-29/catalyst_cycle_00-53.md` line "`0.86` **META/USDT** [legal_risk] Comey Attorneys Seek Dismissal Of Indictment..."; `data/reports/stocks/intraday/2026-07-29_01-33_stocks_intraday_report.md` §7 line 206 (`legal_headline_risk: indictment`) and §4 News section (only META-tagged item is the Comey/Instagram story).
- **suggested manual fix:** audit the symbol/entity resolver for product-name-vs-company false matches (e.g. "Instagram" → META, likely also "WhatsApp" → META, "YouTube" → GOOGL, etc.); the legal-risk gate should require the headline's subject entity to match the ticker's company, not just a product-name substring.
- **priority:** high
- **first observed:** 2026-07-29 04:39 EEST

### TODO-amzn-going-concern-tag-recurring-false-positive (escalated from medium → high)
- **issue:** AMZN's C-tier candidate (was B, score 79) is again tagged `legal_headline_risk: going_concern` this cycle, with the same pattern as 23:30 EEST yesterday: AMZN's own news feed (store-closure item, duplicate Prime-Day-cookware market-defense items) contains no going-concern, bankruptcy, auditor-resignation, or accounting-restatement content. This is now confirmed **recurring across at least 2 consecutive cycles**, not a one-off.
- **evidence:** `data/reports/stocks/intraday/2026-07-29_01-33_stocks_intraday_report.md` §7 (`legal_headline_risk: going_concern` on AMZN) vs §4 AMZN news block (no supporting content); same pattern in `data/reports/stocks/intraday/2026-07-28_20-02_stocks_intraday_report.md` per the 23:30 EEST review.
- **suggested manual fix:** same as previously suggested — audit the legal/headline-risk tagging logic for cross-contamination between adjacent news items in the same symbol's news block, or a stale/cached tag that isn't being refreshed per-cycle; confirm whether `going_concern` requires exact-symbol-matched going-concern language.
- **priority:** high (escalated — 2-cycle recurrence confirmed)
- **first observed:** 2026-07-28 23:30 EEST; recurrence confirmed 2026-07-29 04:39 EEST

### TODO-unh-sec-doj-tag-unsupported-this-cycle (new, low — watch for recurrence)
- **issue:** UNH is tagged `legal_headline_risk: sec_doj`, but this cycle's UNH news feed (Buffett/Berkshire rally story, Medicare drug pricing, Humana earnings) contains no SEC/DOJ content. UNH does have a known historical DOJ-scrutiny basis (noted in the 23:30 review as "plausible"), so this may be a legitimately stale/standing flag rather than a fresh false-positive — flagging for one more cycle of observation before escalating.
- **evidence:** `data/reports/stocks/intraday/2026-07-29_01-33_stocks_intraday_report.md` §7 (`legal_headline_risk: sec_doj` on UNH) vs §4 UNH news block (no SEC/DOJ content this cycle).
- **suggested manual fix:** if this persists next cycle with still no supporting headline, treat as the same class of bug as the AMZN/META tags above; if it clears once fresh DOJ-related news appears, no action needed.
- **priority:** low
- **first observed:** 2026-07-29 04:39 EEST

### TODO-xle-strongest-sector-contradiction-persists-5-plus-cycles (escalated — persistence continues)
- **issue:** The XLE short-vs-strongest-sector contradiction (first flagged 16:07 EEST yesterday) is still open at 04:39 EEST tonight — **5th+ consecutive review cycle** with no resolution. XLE is scored as a raw "was A" short (score 89 this cycle) while energy remains the day's single strongest sector (RS vs SPY +7.47%).
- **evidence:** `data/reports/stocks/intraday/2026-07-29_01-33_stocks_intraday_report.md` §2 (energy=strongest sector, RS+7.47%) vs §7 (XLE was-A short, score 89, C-tier Watchlist table).
- **suggested manual fix:** unchanged from prior cycles — audit whether the sector-confirmation gate for stocks-intraday distinguishes "no sector information" from "sector information present and directionally opposed to the trade"; 5+ cycle persistence across two calendar days suggests this is not self-resolving and is a standing gate-logic gap, not transient market noise.
- **priority:** high (unchanged/escalated — persistence now spans two calendar days)
- **first observed:** 2026-07-28 16:07 EEST; persistence re-observed 2026-07-29 04:39 EEST (5th+ cycle)

### TODO-scalp-intraday-entered-unresolved-aging (carried forward)
- **issue:** Several crypto scalp/intraday B-tier signals remain in `tp1_hit`/`tp2_hit` (ENTERED UNRESOLVED) 7-12+ days past their own mode's typical hours-scale horizon (e.g. NEAR/USDT scalp, expires_at 2026-07-17; ONDO/OPN/FIL scalp, expires_at 2026-07-22; ALLO/USDT intraday, expires_at 2026-07-19 weekend) without resolving to a terminal closed state.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` → same aged rows still present, unchanged from the 23:30 review.
- **suggested manual fix:** unchanged — confirm whether this is expected (open-ended ride to final stop/TP) or whether a lifecycle-closure job should finalize/archive these; consider a distinct "AGED UNRESOLVED" display state.
- **priority:** low
- **first observed:** 2026-07-28 21:41 EEST; still open 2026-07-29 04:39 EEST

### Source-discipline checklist
- Every external claim above has a source name + title + date + URL. ✓
- No uncited stats, no uncited legal claims. ✓
- No fabricated TradingView/chart observations — **TradingView / manual chart check unavailable this run**; only local OHLCV/ATR/EMA/score fields used. ✓
- No `test_source`/fixture URLs ingested. ✓
- §13 Sources section present. ✓
- External WebSearch was used once this cycle (BTC/ETH price context ahead of FOMC) to ground §6; no WebFetch was needed since the search results directly answered the query without requiring a follow-up fetch. Internal-first bar was otherwise satisfied for all candidate-specific findings (ZEC status update, META/AMZN/UNH news-block checks, XLE sector data) via fresh internal reports.
- Catalyst mapping-weak warning stated in both §5 and the Telegram summary. ✓
