# Opus Enriched Review — Europe / pre-US context — Auto Cycle 11:30 EEST

## 1. Executive Summary

Slot: **Europe / pre-US context** (building the US-session watchlist; stocks are pre-market/closed — planning context only until the 16:30 EEST / 09:30 ET cash open). **Advisory only — no auto-trade, no scoring/threshold/strategy changes.** Crypto stays in the same "transition/mixed" regime as the overnight review: BTC ~$63.9K (+0.28% 24h per external check), ETH ~$1,900, both pinned ahead of today's FOMC decision (odds genuinely split — CME FedWatch ~36% hike vs CoinDesk-cited 70% hold/30% hike — a real two-sided volatility event landing later today). Altcoin breadth is weak (31.6% above EMA20, 27% outperforming BTC) and zero fresh A/B-tier crypto ideas were minted this cycle (only one no-trade EUL/USDT card). The standing **ZEC/USDT short** (Zcash Ironwood-upgrade catalyst) has progressed further, now **TP2_HIT**, still running toward invalidation 476.29. Stocks are pre-market/closed with a genuine earnings gauntlet today (MSFT, META, LRCX) and tomorrow (AAPL, AMZN, COIN, MA, MSTR, XOM) — nothing there is actionable pre-open. The scheduler itself is healthy (cycle 5 completed 10:42 EEST, 0/69 steps failed, all monitors alive) but is writing into **yesterday's dated folder** instead of rolling to today's — a display/bookkeeping bug, not a pipeline outage (§14). Legal/headline-risk false-positive tags on META (indictment/"Instagram" keyword collision), AMZN (going_concern) and UNH (sec_doj) persist unchanged from the last two reviews — now escalating further. Catalyst mapping is weak this run (63.9% unmapped) — treat catalyst context as color, not proof. Scanning, tracking, and monitors continue in every mood; this review recommends caution and pre-open preparation, never a stop.

## 2. Data Used

| File | mtime (local) | Age |
|---|---|---|
| `data/reports/scalp/2026-07-29_07-03_scalp_report.md` | 10:03 EEST | ~1h36m |
| `data/reports/intraday/2026-07-29_07-11_intraday_report.md` | 10:11 EEST | ~1h28m |
| `data/reports/swing/2026-07-29_01-58_swing_report.md` | 04:58 EEST | ~6h41m — **carry-forward** (inside 4-12h window) |
| `data/reports/stocks/intraday/2026-07-29_07-34_stocks_intraday_report.md` | 10:34 EEST | ~1h05m (market pre-market/closed — planning only) |
| `data/reports/stocks/swing/…` / `invest/…` | 2026-07-02 | deprecated/removed playbooks — not treated as stale, see [[project_crypto_ai_desk_stocks_position_framework]] |
| `data/catalysts/2026-07-29/catalyst_cycle_07-14.md` + `catalyst_events.jsonl` (1500 rows) + `narrative_baskets.jsonl` | 10:14 EEST | ~1h25m |
| `data/processed/llm_analysis_packet.md` | 10:11 EEST | ~1h28m |
| `data/processed/llm_stocks_packet.md` | 10:36 EEST | ~1h03m |
| `python -m src.cli active-signals --asset-class crypto` | live query | now |
| `python -m src.cli active-signals --asset-class stocks` | live query | now |
| `python -m src.cli signal-stats --asset-class crypto` | live query | now |
| `python -m src.cli signal-stats --asset-class stocks` | live query | now |
| `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-29` | live query | now |
| `data/scheduled_runs/2026-07-28_default_schedule/scheduler.log` (live scheduler, misnamed folder — see §14) | 10:42 EEST | ~57m |
| `data/scheduled_runs/2026-07-28_default_schedule/cycle_05_09-52_summary.md` | last completed cycle, ended 10:42 EEST | ~57m |
| WebSearch: "Bitcoin Ethereum price today July 29 2026 Fed rate decision" | live, 2026-07-29 | for §6 external grounding |
| Prior review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-29_0430.md` | 04:39 EEST | for §4 diff |

## 3. Scheduler / Data Freshness

- **Folder-naming bug (see §14):** `data/scheduled_runs/2026-07-29_default_schedule/` contains only a `DRY RUN` validation pass from 02:40-02:41 plus the background derivatives monitor logs — it never received a real production cycle. The **actual live scheduler is still writing into yesterday's `2026-07-28_default_schedule/scheduler.log`**, which is fresh (last write 10:42:28 EEST, ~57m old) and shows **CYCLE 5 END ok=69 failed=0 telegram=sent**. All five background monitors (crypto watchlist, mexc-canary, derivatives, fast-news, stocks) reported still running with healthy lifetimes at end-of-cycle.
- Cross-checked against report mtimes: scalp/intraday reports both <1h36m old, stocks-intraday <1h05m old (pre-market, planning-only), catalyst scan <1h25m old, both LLM packets <1h30m old — **all consistent with a healthy, actively-cycling pipeline**. Per §D the literal scheduler.log+cycle_summary check inside today's folder would read as "stale" (both >3h because the folder is empty of real cycles), but the fresher, more authoritative live-scheduler-log and report-mtime evidence overrides that false reading — **no defer**.
- Last completed cycle (`cycle_05_09-52_summary.md`, ended 10:42:28 EEST): **0 FAIL / 69 OK** — clean run. Paper monitor status (Telegram-sent 10:40 EEST): Open actionable 0 · Waiting for entry 0 · Entered unresolved 0 · Review/Shadow 23 · No-entry/stale/moved-away 48 · Needs review 1 · Closed today 152W/7L/22flat (paper P&L, not live).
- `detect_untracked_legacy_alerts --since 2026-07-29`: **None** — every legacy crypto alert has a backing proposed_signal; no integrity anomaly this run.
- Swing report is carry-forward (~6h41m old, inside the 4-12h window) — used for context, flagged.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us",
  "as_of": "2026-07-29 11:45 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["today's dated folder has no completed production cycle — only a dry-run; live scheduler is writing under yesterday's folder name (§14)", "swing report is carry-forward (~6h41m old, inside 4-12h window)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log (2026-07-28 folder) last write 10:42:28 EEST, CYCLE 5 END ok=69 failed=0", "scalp/intraday/stocks-intraday reports 1h05m-1h36m old, catalyst scan 1h25m old", "detect_untracked_legacy_alerts: none"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["mixed", "chop", "shorts_preferred", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime label=transition, risk mode=mixed, breadth 31.6% above EMA20, 27.0% outperforming BTC (weak)", "macro risk score 96.5/100: Iran/Strait-of-Hormuz escalation, Russia sanctions vote, Fed decision live today", "stocks regime risk_off/short bias, VIX 18.25, breadth 0.0% above EMA20/EMA50 (weaker than the 04:30 review's 25%)", "external WebSearch: BTC ~$63.9K (+0.28% 24h), ETH ~$1,900, FOMC odds genuinely split (36% hike CME vs 70% hold/30% hike CoinDesk-cited)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "narrative_supported", "catalyst_confirmed"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["1500 catalyst events today; 541 mapped (36.1%), 959 unmapped (63.9%) — weak-mapping threshold breached again", "4 narrative baskets in narrative_baskets.jsonl", "ZEC/USDT Ironwood-upgrade catalyst: position now TP2_HIT (was TP1_HIT at 04:30) — catalyst thesis continuing to pay", "ZIL/USDT and EUL/USDT both top movers with no fresh verified catalyst — pure momentum"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["data_unavailable", "squeeze_risk", "oi_contradicts"],
      "data_missing": ["external futures data on several lower-cap names (SNXXB, SOXLB, SNDKB, SKHYB)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZIL/USDT: negative funding across bybit/mexc/okx, crowding=elevated — shorts increasingly crowded, squeeze risk for a long thesis", "ETH/XRP/SOL: price up + OI down = short covering, weaker continuation quality (all three tagged)", "EUL/USDT: negative funding across venues, crowding=elevated"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry", "clean_retest"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["EUL/USDT: only fresh trade-idea-agent output this cycle, scored 48.3, tier=rejected/no_trade — 'evidence not strong enough', watch only", "ZIL/USDT 24h move has cooled to +18.69% (from +21-25% at 04:30) — still extended, no confirmed pullback yet per swing report's conditional 0.0025-0.0027 zone", "BANK/USDT now -46.13% 24h (deeper than -37/-40% at 04:30) — further extended short, no fresh catalyst", "ZEC/USDT: existing runner, TP2_HIT, no new entry decision needed"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.7,
      "reason_codes": ["entered_unresolved", "waiting_for_entry", "no_entry", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active-signals: 18/18 rows ENTERED UNRESOLVED (tp1_hit/tp2_hit), 0 fresh open/waiting/triggered", "stocks active-signals: 50 rows, mostly aged C-tier ENTERED UNRESOLVED/waiting, 0 A/B", "paper monitor (10:40 EEST): open actionable 0, review/shadow 23, no-entry/stale/moved-away 48, needs review 1, closed today 152W/7L/22flat", "several crypto ENTERED UNRESOLVED rows 7-12+ days past their mode's typical horizon (NEAR scalp exp 2026-07-17, ONDO/OPN/FIL scalp exp 2026-07-22, ALLO intraday exp 2026-07-19) — unchanged, carried"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["META still tagged legal_headline_risk=indictment this cycle — news block shows only Anthropic-AI-compute and Microsoft/Caterpillar power stories, no indictment content; keyword-collision false-positive persists unchanged", "AMZN still tagged legal_headline_risk=going_concern — news block (OceanBase AI push, UPS shipping-cuts pressure, grocery-chain-closures story) has no going-concern content; now confirmed across 3+ consecutive cycles", "UNH still tagged legal_headline_risk=sec_doj — news block (AI-medical-coding market report, Berkshire/Buffett rally story) has no SEC/DOJ content", "MSFT, META, LRCX all report earnings TODAY; AAPL/AMZN/COIN/MA/MSTR/XOM tomorrow — 9-name earnings gauntlet across two days", "macro risk 96.5/100, FOMC decision live today"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week (tier=B, n=96): PF 2.425, winrate 26.1%, totalR +28.5", "by mode: swing PF 3.83/totalR +19.8 (strongest), intraday PF 2.59/totalR +12.7 (working), scalp PF 0.20/0W-5L/totalR -4.0 (net-negative, unchanged, no new scalp ideas this cycle either)", "stocks: headline A/B sample=0 this week (no actionable stocks A/B sample); C-tier n=181, PF 0.429, totalR -4.0 (weak, unchanged)"] },
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
    "best_long_candidate":     { "symbol": "ZIL/USDT", "trigger": "confirmed pullback/retest into 0.0025-0.0028 with rising volume; do not chase the current +18.7% 24h extension; shorts increasingly crowded across venues (elevated) argues for a squeeze-driven continuation IF the retest holds", "reason": "Top RS-leader (score 87.9), sole momentum-basket primary, cooling slightly from the overnight extension but still no confirmed entry" },
    "best_short_candidate":    { "symbol": "ZEC/USDT", "trigger": "already open, now TP2_HIT; manage the runner to invalidation 476.2871 or next TP, no new entry needed", "reason": "Catalyst-confirmed sell-the-news reaction to the Zcash Ironwood upgrade; the one desk idea that has actually kept paying this window" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "same as best-short — catalyst and technical remain aligned, TP2 already realized", "reason": "Cross-confirmed catalyst, now resolving favorably for a second consecutive review cycle" },
    "avoid_candidate":         { "symbol": "BANK/USDT", "reason": "-46.1% 24h, RS vs BTC -47.6%, deeper extension than the overnight review, no fresh verified catalyst, watchlist-only score — chasing this short here is late" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 6
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---:|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.75 | mixed, chop, shorts_preferred, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, narrative_supported, catalyst_confirmed | advisory_only |
| derivatives_squeeze | caution | 0.50 | data_unavailable, squeeze_risk, oi_contradicts | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, stale_before_entry, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.70 | entered_unresolved, waiting_for_entry, no_entry, needs_review | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | manual_review | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (04:39 EEST, crypto overnight / Asia review)

- **ZEC/USDT short**: was `TP1_HIT` → now **TP2_HIT** — the runner keeps paying overnight into the EU morning; remaining size still open toward invalidation 476.2871, expires 2026-07-29T17:36 EEST.
- **ZIL/USDT**: 24h move has cooled from +21-25% to +18.69% — still the desk's clearest long-watch RS-leader/momentum name, no confirmed pullback yet. Funding has gone **negative across external venues with crowding=elevated** (new this cycle) — shorts are increasingly crowded, raising squeeze-continuation odds if the retest holds.
- **BANK/USDT**: extension has deepened from -37/-40% 24h to **-46.13%** — still no catalyst, still watchlist-only, now even later to chase on the short side.
- **META / AMZN / UNH legal-tag false positives**: **all three persist unchanged** this cycle — same tags, same lack of supporting news content in each symbol's own feed. This is now confirmed recurring across 3+ consecutive review cycles for AMZN, 2nd for META, 2nd for UNH (escalated further in §14).
- **Stocks breadth**: weaker than overnight — 0.0% above EMA20/EMA50 this cycle vs 25% at 04:30 (pre-market data can be noisy; flagged, not over-interpreted).
- **New this cycle — sector-rotation data gap**: the stocks-intraday report's §2 Sector Rotation table now returns `+nan%` for every sector's RS/20d-return field, so the previously-tracked "XLE short vs strongest-sector" contradiction (5th+ cycle unresolved at 04:30) **cannot be evaluated this cycle** — the underlying data feed appears to have broken rather than the contradiction having resolved (new TODO, §14).
- **New this cycle — scheduler folder-naming bug identified**: root-caused this run — the live scheduler process has not rolled over to a `2026-07-29_default_schedule/` folder at all; it is still actively writing into `2026-07-28_default_schedule/scheduler.log` past midnight (confirmed via a live 10:42 EEST cycle-end log line inside the "yesterday" folder). Previously this just looked like scheduler staleness; now confirmed as a folder-naming/day-rollover defect, not an outage (new TODO, §14).
- **FOMC**: external check confirms the Fed decision is live today (July 28-29 meeting), with genuinely split odds (36% hike per CME FedWatch vs a 70% hold / 30% hike estimate cited elsewhere) — this is the dominant near-term risk event for both crypto and stocks today.
- **Crypto desk**: still zero fresh A/B-tier ideas on scalp/intraday/swing this cycle (only one no-trade EUL/USDT card) — unchanged in actionability from the overnight review.
- **Stocks desk**: still zero A/B-tier actionable candidates; market remains pre-market/closed until 16:30 EEST.

## 5. Catalyst Coverage

- Catalyst events today: **1,500** scanned this cycle; **541 mapped** (36.1%) / **959 unmapped** (63.9%).
- Narrative baskets: **4** entries in `narrative_baskets.jsonl`.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped 63.9% > 50% threshold, consistent with the overnight review's 63.8%)
- Top unmapped headlines (by presence in the feed, representative sample):
  1. "250,000,000 $USDC (249,982,000 USD) minted at USDC Treasury" — Whale Alert (t.me)
  2. "Thailand SEC accuses Bitkub executives of hiding $50 million hack losses in official reports"
  3. "LATEST: Senate Majority Leader John Thune says the Senate will 'probably have a vote on the CLARITY [Act]'..."
- Best *mapped* catalyst quality check this cycle: ZEC/USDT (Ironwood upgrade, confirmed/paying) is the standout clean example; META's mapped legal-risk tag remains the standout false-positive (§7/§14).

## 6. Market Landscape

Crypto: regime label "transition", risk mode "mixed". BTC ~$63.9K (+0.28% 24h, external check), ETH ~$1,900 — both range-bound ahead of today's FOMC decision. Altcoin breadth weak (31.6% above EMA20, 27.0% outperforming BTC). Macro risk score 96.5/100, driven by Iran/Strait-of-Hormuz escalation headlines, the Senate Russia/Iran sanctions vote, and the live Fed decision — CME FedWatch shows ~36% hike odds vs a separately-cited 70% hold/30% hike split; both crypto desks and outside commentary flag this as an unusually hard-to-call meeting. Stocks (pre-market/closed): risk_off, bias short, VIX 18.25, breadth 0.0% above EMA20/EMA50, all four major indices range-bound this cycle; sector-rotation data is currently broken (all-NaN, see §14) so no reliable strongest/weakest sector read this cycle. MSFT, META, and LRCX report earnings **today**; AAPL, AMZN, COIN, MA, MSTR, and XOM follow tomorrow — a 9-name, two-day earnings gauntlet layered on top of the FOMC decision.

### Market Mood / Risk Routing
- Crypto mood: **mixed / transition, risk-off-leaning into FOMC**
- Stocks mood: **risk_off / pre-market-closed (planning only until 16:30 EEST / 09:30 ET)**
- Dominant narrative: FOMC-decision positioning (genuinely two-sided) + Iran/Russia geopolitical risk-off + a two-day earnings gauntlet (MSFT/META/LRCX today; AAPL/AMZN/COIN/MA/MSTR/XOM tomorrow)
- Preferred side now: **wait-for-trigger** (crypto: manage the open ZEC short, size-reduced RS-leader longs only on a confirmed pullback; stocks: nothing actionable until the RTH open, and even then treat every earnings-adjacent name as chase-risk)
- Best long candidate: **ZIL/USDT** (RS-leader, momentum-basket primary, cooling from its overnight extension but still no confirmed retest — see §8)
- Best short candidate: **ZEC/USDT** (open, TP2_HIT, catalyst-confirmed — manage the runner)
- Best catalyst-backed candidate: **ZEC/USDT** (same name — catalyst and technical remain aligned)
- What to avoid: chasing ZIL/USDT before a confirmed pullback; fresh entries on BANK/USDT (now -46.1% 24h, no catalyst); any stock name into today's MSFT/META/LRCX prints or tomorrow's AAPL/AMZN/COIN/MA/MSTR/XOM prints; any crypto or stock position sized aggressively ahead of today's FOMC decision given the genuinely split odds
- What would change the view: a confirmed FOMC outcome removing the two-sided uncertainty; BTC reclaiming key resistance with altcoin breadth improving meaningfully above 50% on EMA20; a clean SPY/QQQ direction once RTH data replaces the broken pre-market sector feed

## 7. Candidate Deep Dives

### 1. ZEC/USDT — crypto intraday short, B-tier, TP2_HIT (score 65.2)
- Entry zone: 469.6229-472.6218 (filled) · Invalidation: 476.2871 · Expires: 2026-07-29T17:36 EEST.
- Has price already reacted to the catalyst? Yes — confirmed sell-the-news fade on the Zcash Ironwood upgrade; the trade has since realized both TP1 and TP2.
- Chasing? No — already open, no new entry decision required.
- Retest/pullback structure? N/A — managing an existing runner.
- Overextended? Not flagged this cycle.
- Would entry now be late? N/A — already filled, two targets realized.
- Mood alignment: yes — a risk-off-leaning tape into FOMC favors clean catalyst-backed shorts that have already paid.
- Long/short/wait: managing an open short.
- Actionable now or confirmation-only? Already actionable/open; monitor to invalidation or next TP.
- Chase-risk setup? No.
- Catalyst confirmation or contradiction? Confirmed, unchanged — internal-first bar satisfied by the continued favorable status transition.

### 2. ZIL/USDT — crypto intraday/scalp long-watch, RS-leader, C-tier watchlist (score 87.9 raw)
- Has price already reacted? Yes — +18.69% 24h (cooling from +21-25% at 04:30), RS vs BTC +17.27%, vol ratio 0.06x.
- Chasing? Still elevated, but less extreme than overnight.
- Retest/pullback structure? Conditional pullback zone from the carried swing report: 0.0025-0.0027 (+/- 0.0028 band).
- Overextended? Not explicitly re-measured this cycle; the cooling trend argues the picture is improving but not yet clean.
- Would entry now be late? At current levels, yes — no confirmed retest has printed.
- What level makes it actionable? A confirmed 1h close into the 0.0025-0.0028 pullback zone with rising volume, or the risk-gated score clearing its cap.
- Mood alignment: RS-leader longs are the correct risk-routing choice generally, but this remains a counter-tape trade relative to BTC/ETH's own range-bound-to-weak posture into FOMC — reduce size, demand confirmation.
- Long/short/wait: long-watch, wait-for-trigger.
- Invalidation: 1h close below 0.0023 (carried from swing report) / RS-leadership fading vs BTC.
- Chase-risk setup? Yes, moderating.
- Catalyst confirmation/contradiction: no news catalyst — pure momentum (`momentum_breakout` basket). New this cycle: funding has gone **negative across bybit/mexc/okx with crowding=elevated** — shorts are increasingly crowded, which raises squeeze-continuation odds specifically if the pullback holds rather than breaks down.

### 3. META — stocks C-tier watchlist (was B, score ~59), `legal_headline_risk=indictment` — **false-positive, unchanged 2nd+ cycle**
- Has price already reacted? Not evaluated — market pre-market/closed; also moot, the underlying tag does not describe a real Meta Platforms event.
- Legal/headline risk check (§I): this cycle's META news block is "Meta in early talks to lease $10B of AI compute to Anthropic," a Microsoft/Caterpillar power story, and a Hong Kong data-center loan story — **no indictment content whatsoever**. The tag traces back to the same Comey/"Instagram" keyword-collision identified at 04:30 and remains unresolved.
- Per §I policy: verdict stays **MANUAL REVIEW REQUIRED**, not a clean actionable.
- Earnings: META reports **today** (2026-07-29) — independent do-not-chase reason regardless of the legal-tag question.
- What would clear it: a human confirming the keyword-collision false-positive (§14), or the earnings window passing with a clean post-print setup.

### 4. AMZN — stocks C-tier watchlist (was B, score ~71), `legal_headline_risk=going_concern` — **recurring false-positive, 3rd+ cycle observed**
- Has price already reacted? Not evaluated; market pre-market/closed.
- Legal/headline risk check (§I): this cycle's AMZN news block (OceanBase AI-funding story, UPS-shipping-cuts pressure story, grocery-chain-store-closures story) again has **no going-concern, bankruptcy, auditor-resignation, or accounting-restatement content**. Same pattern as the 23:30 and 04:30 reviews — now confirmed across at least 3 consecutive cycles.
- Per §I policy: verdict stays **MANUAL REVIEW REQUIRED** until a human clears or confirms the tag.
- Earnings: AMZN reports tomorrow — independent do-not-chase reason regardless.
- What would clear it: a human audit of the going_concern gate logic (§14, priority unchanged at high given continued recurrence).

### 5. UNH — stocks C-tier watchlist (score ~52), `legal_headline_risk=sec_doj` — **unresolved, 2nd+ cycle, watch for pattern confirmation**
- Has price already reacted? Not evaluated; market pre-market/closed.
- Legal/headline risk check (§I): this cycle's UNH news block (AI-medical-coding market report, Berkshire/Buffett rally follow-up story) again has no SEC/DOJ content. Flagged at 04:30 as "possibly a legitimately stale/standing flag rather than a fresh false-positive, watch one more cycle" — that watch period has now passed with the same unsupported result, so this is escalated from low to medium priority in §14.
- Per §I policy: verdict stays **MANUAL REVIEW REQUIRED**.
- What would clear it: fresh DOJ-related UNH news appearing (would validate the tag), or continued absence (would confirm false-positive, matching the AMZN/META pattern).

## 8. Best Candidates Ranked

1. **Best catalyst-backed / best short (crypto): ZEC/USDT short** — open, TP2_HIT, invalidation 476.2871, expires 2026-07-29T17:36 EEST. Manage the runner; no new entry needed.
2. **Best long-watch (crypto): ZIL/USDT** — trigger: confirmed 1h close into the 0.0025-0.0028 pullback zone with rising volume; do not chase the current +18.7% extension; crowded external shorts raise squeeze-continuation odds if the retest holds.
3. **Manual-review / avoid (stocks): META** — earnings today + a persistent, near-certainly spurious `indictment` legal tag (keyword collision on "Instagram").
4. **Manual-review / avoid (stocks): AMZN** — earnings tomorrow + `going_concern` tag unsupported by its own news feed for a 3rd+ straight cycle.
5. **Avoid (stocks): UNH** — earnings-adjacent legal tag (`sec_doj`) unsupported for a 2nd straight cycle; treat as likely false-positive pending human review.
6. **Avoid (crypto): BANK/USDT** — -46.1% 24h, deeply extended, no catalyst — chasing this short here is late.

## 9. Avoid / No Trade

This is a **decision-window-only** call, not a system-wide stop — scanning, tracking, and monitors continue regardless.

- **META / AMZN / UNH shorts or any action** — all three blocked by same-day/near-term earnings prints plus unresolved, likely-spurious legal-tag questions → MANUAL REVIEW REQUIRED.
- **Any fresh chase on ZIL/USDT** before a confirmed pullback into 0.0025-0.0028 with volume.
- **Fresh entries on BANK/USDT** — deeply extended (-46.1% 24h), no catalyst, watchlist-only score.
- **Crypto scalp mode** — still net-negative on the historical/tracking series this week (PF 0.20, 0W-5L, totalR -4.0); no new scalp ideas expected or wanted.
- **Any aggressively-sized new position (crypto or stocks) ahead of today's FOMC decision** — odds are genuinely split (36% hike vs 70% hold/30% hike across sources); this is a two-sided event, not a call to avoid the market entirely.
- Nothing here is a command to pause the scanner, monitors, or data collection — all continue.

## 10. Main Risks

- **FOMC decision live today** — genuinely split odds (CME FedWatch ~36% hike vs a separately-cited 70% hold/30% hike) make this the dominant, two-sided risk event for both crypto and stocks; do not pre-commit size to either outcome.
- **Earnings gauntlet**: MSFT/META/LRCX today, AAPL/AMZN/COIN/MA/MSTR/XOM tomorrow — do not hold or chase into any of these prints.
- **Geopolitical risk-off**: Iran/Strait-of-Hormuz escalation + Russia-sanctions headlines keep the macro risk score pinned at 96.5/100.
- **Catalyst mapping is weak this run (63.9% unmapped)** — treat catalyst context as directional color, not proof.
- **Legal/headline gate false-positive pattern continues spreading and persisting**: META (2nd+ cycle), AMZN (3rd+ cycle), UNH (2nd+ cycle) — confidence in the legal-risk gate keeps degrading (§14).
- **Stocks sector-rotation data feed appears broken this cycle** (all-NaN RS/20d fields) — no reliable sector read available for pre-open planning (new, §14).
- **Scheduler day-folder rollover defect** — cosmetic/bookkeeping only (the live process itself is healthy), but left unfixed it will keep making every subsequent review's §D freshness check read as falsely stale (§14).
- **Aged ENTERED UNRESOLVED crypto signals**: several scalp/intraday B-tier rows are 7-12+ days past their mode's typical horizon without resolving to a terminal state (§14, carried).

## 11. Action Plan — next 4 hours

1. **Manage ZEC/USDT short** to invalidation (476.29) or next TP; no new entry needed, already TP2_HIT.
2. **Watch ZIL/USDT** for a confirmed 1h close into 0.0025-0.0028 with rising volume before considering it actionable; do not chase.
3. **Do not originate new crypto entries** on BANK/USDT or other deeply-extended no-catalyst names.
4. **Do not add size ahead of the FOMC decision** — treat the outcome as genuinely unresolved; re-assess routing once the decision and initial market reaction are known.
5. **Stocks: nothing actionable pre-open.** Build the RTH watchlist from AMD/XLE/XLK/QQQ/PLTR/SMH/SMCI/AVGO (today's top C-tier short reads, all demoted only by the market-closed gate) and re-confirm fresh at/after 09:30 ET (16:30 EEST); flag every earnings-adjacent name (MSFT/META/LRCX today, AAPL/AMZN/COIN/MA/MSTR/XOM tomorrow) as do-not-chase.
6. **Flag META, AMZN, and UNH for human review** before treating any of their fresh setups as actionable post-open — all three carry unresolved, likely-spurious legal-tag questions (§14).
7. Continue all scanning/monitoring — no pause recommended in any mood.

## 12. Final Verdict per Mode

- **Crypto scalp**: NO-ENTRY / kill-switched — net-negative bucket this week (PF 0.20), no change expected.
- **Crypto intraday**: NO-ENTRY this cycle (0 fresh A/B ideas, one rejected no-trade card) — WATCHLIST ONLY (best long-watch: ZIL/USDT; best short-watch already open: ZEC/USDT).
- **Crypto swing**: NO-ENTRY this cycle (report carry-forward ~6h41m old, no fresh A/B ideas) — no new long-watch name beyond ZIL/USDT.
- **Crypto — open positions**: ZEC/USDT short TP2_HIT, manage the runner; remaining 17 active B-tier signals are ENTERED UNRESOLVED (tp1_hit/tp2_hit) — no new action needed, several aging well past their mode horizon (§14 carried TODO).
- **Stocks intraday**: MARKET PRE-MARKET/CLOSED — planning/watchlist only; all A/B-raw candidates demoted to C by the market-closed gate; re-confirm fresh at RTH open; META, AMZN, and UNH additionally blocked by likely-spurious legal tags pending human review.
- **Stocks swing/invest**: deprecated/removed, not evaluated (new `stocks_swing_growth_breakout` remains shadow-only research, not actionable — latest shadow scan: UNH pullback_21d_50d score 87, AAPL reclaim_after_shakeout score 77, USD-net outcomes pending).

## 13. Sources

- [Crypto Prices Today: Bitcoin Holds Near $65,260, Ethereum Jumps Over 3.6% as Traders Brace for Fed Decision](https://www.analyticsinsight.net/price-analysis/crypto-prices-today-bitcoin-holds-near-65260-ethereum-jumps-over-36-as-traders-brace-for-fed-decision) — Analytics Insight, accessed 2026-07-29
- [Bitcoin, Ethereum and XRP Price Prediction (July 29): Can BTC Hold Above $63K Ahead of Fed Decision?](https://sundayguardianlive.com/business/bitcoin-ethereum-and-xrp-price-prediction-july-29-can-btc-hold-above-63k-ahead-of-fed-decision-check-btc-eth-and-xrp-forecast-key-support-resistance-market-outlook-more-248285/) — Sunday Guardian Live, accessed 2026-07-29
- [Fed Meeting News: Will Federal Reserve Interest Rates Impact Bitcoin?](https://www.coingabbar.com/en/crypto-currency-news/fed-meeting-news-today-fomc-rate-cut-expectations-july-29-2026) — CoinGabbar, accessed 2026-07-29
- `data/reports/intraday/2026-07-29_07-11_intraday_report.md` — internal source for ZIL/USDT derivatives/crowding data and macro/catalyst context
- `data/catalysts/2026-07-29/catalyst_cycle_07-14.md` + `catalyst_events.jsonl` — internal source for catalyst coverage stats and the ZEC/USDT catalyst
- `data/reports/stocks/intraday/2026-07-29_07-34_stocks_intraday_report.md` §2, §4, §7 — internal source for the META/AMZN/UNH news-block checks and the sector-rotation data-gap finding
- `data/scheduled_runs/2026-07-28_default_schedule/scheduler.log` — internal source for the folder-naming bug and cycle-5 completion status
- Internal `active-signals`/`signal-stats` CLI outputs (live queries, this run) — for lifecycle status and playbook performance

## 14. Fix Requests / TODO

### TODO-scheduler-day-folder-rollover-bug (new, high)
- **issue:** The scheduler creates a per-day folder `data/scheduled_runs/<YYYY-MM-DD>_default_schedule/`, but the *live, actively-running* scheduler process did not roll over to today's (`2026-07-29`) folder at midnight — it is still writing production cycles into **yesterday's** `2026-07-28_default_schedule/scheduler.log` past 10:42 EEST today. Meanwhile a separate, apparently unrelated process created `2026-07-29_default_schedule/` containing only a one-off `DRY RUN` validation pass (02:40-02:41) and background derivatives-monitor logs, with no real cycle output. This makes the routine's own §D freshness check (which looks at "the latest folder by mtime") read the pipeline as falsely stale, when in fact cycle 5 completed cleanly (0/69 failed) at 10:42 EEST under the old folder name.
- **evidence:** `data/scheduled_runs/2026-07-28_default_schedule/scheduler.log` line `2026-07-29 10:42:28,952 [INFO] CYCLE 5 END ok=69 failed=0 telegram=sent` (timestamped today, inside yesterday's folder); `data/scheduled_runs/2026-07-29_default_schedule/` contains only `scheduler.log` (dry-run, 02:40-02:41) and `derivatives_monitor_*.log` files, no `cycle_*_summary.md`.
- **suggested manual fix:** audit the scheduler's day-folder-naming logic (likely computes the folder name once at process start rather than per-cycle, or a separate dry-run/validation launcher created the empty new-day folder without the main loop following it) — ensure the folder name is derived from the current date at each cycle boundary, or otherwise make the "latest folder by mtime" freshness check in this SKILL robust to a live process writing into a stale-named folder (e.g. also check the mtime of the scheduler.log with the single most recent mtime across all dated folders, not just the most-recently-created one).
- **priority:** high
- **first observed:** 2026-07-29 11:39 EEST (this cycle)

### TODO-stocks-sector-rotation-data-nan (new, high)
- **issue:** `data/reports/stocks/intraday/2026-07-29_07-34_stocks_intraday_report.md` §2 Sector Rotation now returns `+nan%` for every sector's "RS vs SPY 20d" and "20d return" field (technology, semiconductors, financials, consumer_staples, materials, real_estate all `status=mixed, +nan%`), and the SPY-benchmark 20d return itself is `+nan%`. This is a data-quality regression, not a market condition — it also makes the previously-tracked "XLE short vs strongest-sector" contradiction (5th+ cycle unresolved as of the 04:30 review) impossible to evaluate this cycle, since there is no longer a reported "strongest sector" to compare against.
- **evidence:** `data/reports/stocks/intraday/2026-07-29_07-34_stocks_intraday_report.md` lines 33-43 (all `+nan%`).
- **suggested manual fix:** investigate the sector-ETF 20d-return calculation in the stocks pipeline for a missing/stale OHLCV window (likely insufficient trading-day history for a 20d lookback at this data-freshness point, or a divide-by-zero/None propagation bug); confirm whether this is transient (pre-market data gap) or a standing regression by checking whether the next RTH-hours report resolves it.
- **priority:** high
- **first observed:** 2026-07-29 11:39 EEST (this cycle)

### TODO-meta-indictment-tag-keyword-collision-false-positive (escalated, persists 2nd+ cycle)
- **issue:** META remains tagged `legal_headline_risk: indictment` this cycle. As identified at 04:30 EEST, this traces to a headline containing the word "Instagram" in an unrelated James Comey legal story, with zero connection to Meta Platforms Inc. This cycle's own META news block (Anthropic AI-compute lease talks, Microsoft/Caterpillar power story, Hong Kong data-center loan story) confirms there is still no real indictment-related content for META.
- **evidence:** `data/reports/stocks/intraday/2026-07-29_07-34_stocks_intraday_report.md` §7 (`legal_headline_risk: indictment` on META) vs §4 META news block (no indictment content).
- **suggested manual fix:** unchanged from 04:30 — audit the symbol/entity resolver for product-name-vs-company false matches (e.g. "Instagram"/"WhatsApp" → META, "YouTube" → GOOGL); the legal-risk gate should require the headline's subject entity to match the ticker's company, not just a product-name substring.
- **priority:** high
- **first observed:** 2026-07-29 04:39 EEST; recurrence confirmed 2026-07-29 11:39 EEST

### TODO-amzn-going-concern-tag-recurring-false-positive (escalated, persists 3rd+ cycle)
- **issue:** AMZN remains tagged `legal_headline_risk: going_concern` this cycle, with the same pattern as the 23:30 and 04:30 reviews: AMZN's own news feed (OceanBase AI-funding story, UPS shipping-cuts pressure story, grocery-chain-closures story) contains no going-concern, bankruptcy, auditor-resignation, or accounting-restatement content. Now confirmed recurring across **at least 3 consecutive cycles**.
- **evidence:** `data/reports/stocks/intraday/2026-07-29_07-34_stocks_intraday_report.md` §7 (`legal_headline_risk: going_concern` on AMZN) vs §4 AMZN news block (no supporting content); same pattern in the 23:30 and 04:30 reviews.
- **suggested manual fix:** unchanged — audit the legal/headline-risk tagging logic for cross-contamination between adjacent news items in the same symbol's news block, or a stale/cached tag that isn't being refreshed per-cycle.
- **priority:** high (unchanged — 3rd+ cycle recurrence confirmed)
- **first observed:** 2026-07-28 23:30 EEST; recurrence confirmed 2026-07-29 04:39 EEST and 2026-07-29 11:39 EEST

### TODO-unh-sec-doj-tag-unsupported-2nd-cycle (escalated low → medium)
- **issue:** UNH remains tagged `legal_headline_risk: sec_doj` this cycle. The 04:30 review flagged this as "possibly a legitimately stale/standing flag, watch one more cycle before escalating" — that watch cycle has now passed with the same unsupported result (UNH's news feed this cycle: AI-medical-coding market report, Berkshire/Buffett rally follow-up — no SEC/DOJ content either time).
- **evidence:** `data/reports/stocks/intraday/2026-07-29_07-34_stocks_intraday_report.md` §7 (`legal_headline_risk: sec_doj` on UNH) vs §4 UNH news block (no SEC/DOJ content, 2nd consecutive cycle observed).
- **suggested manual fix:** same class of fix as the AMZN/META tags — if a 3rd cycle also shows no supporting content, treat as confirmed false-positive of the same root cause; if fresh DOJ-related news appears, the tag is validated and this TODO can be closed.
- **priority:** medium (escalated from low — 2nd unsupported cycle observed)
- **first observed:** 2026-07-29 04:39 EEST; recurrence confirmed 2026-07-29 11:39 EEST

### TODO-scalp-intraday-entered-unresolved-aging (carried forward)
- **issue:** Several crypto scalp/intraday B-tier signals remain in `tp1_hit`/`tp2_hit` (ENTERED UNRESOLVED) 7-12+ days past their own mode's typical hours-scale horizon (e.g. NEAR/USDT scalp, expires_at 2026-07-17; ONDO/OPN/FIL scalp, expires_at 2026-07-22; ALLO/USDT intraday, expires_at 2026-07-19 weekend) without resolving to a terminal closed state.
- **evidence:** `python -m src.cli active-signals --asset-class crypto` → same aged rows still present, unchanged from the 04:30 and 23:30 reviews.
- **suggested manual fix:** unchanged — confirm whether this is expected (open-ended ride to final stop/TP) or whether a lifecycle-closure job should finalize/archive these; consider a distinct "AGED UNRESOLVED" display state.
- **priority:** low
- **first observed:** 2026-07-28 21:41 EEST; still open 2026-07-29 11:39 EEST

### Source-discipline checklist
- Every external claim above has a source name + title + date + URL. ✓
- No uncited stats, no uncited legal claims. ✓
- No fabricated TradingView/chart observations — **TradingView / manual chart check unavailable this run**; only local OHLCV/ATR/EMA/score fields used. ✓
- No `test_source`/fixture URLs ingested. ✓
- §13 Sources section present. ✓
- External WebSearch was used once this cycle (BTC/ETH/FOMC price context) to ground §6; no WebFetch was needed since the search results directly answered the query without requiring a follow-up fetch. Internal-first bar was otherwise satisfied for all candidate-specific findings (ZEC status update, META/AMZN/UNH news-block checks, sector-rotation data-gap) via fresh internal reports.
- Catalyst mapping-weak warning stated in both §5 and the Telegram summary. ✓
