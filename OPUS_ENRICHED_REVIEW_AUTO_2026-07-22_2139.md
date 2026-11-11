# Opus Enriched Review — late-session risk review — Auto Cycle 21:30 EEST

## 1. Executive Summary

Slot: **late-session risk review** (21:39 EEST / 18:39 UTC / ~14:39 ET, ~1h20m left in the US cash session). Advisory only — no auto-trade, no scoring/strategy changes. Crypto: BTC/ETH opened higher overnight (CLARITY Act optimism, 6 consecutive days of positive spot-ETF inflows) but **faded through the NY morning** — BTC ~$66.5K→$65.5K, ETH ~$1,929→$1,918 — while the desk's own macro-risk score stays pinned at **100/100** on the ongoing Iran-Hormuz/oil conflict (Brent >$95). Altcoin breadth ticked up to 68.4%>EMA20 (from 63–65% earlier today). **No A-tier setups anywhere** (crypto or stocks) and **no B-tier setups in the fresh scalp report** either. The crypto intraday report's only B-tier ideas (ZAMA/EPIC/AKE, all "no fresh catalyst") are now **~7h old — stale for fresh entry**, with no confirmation since; the two genuinely current system signals are `waiting_for_entry` on **VANA/USDT** and **KITE/USDT**. The **known untracked-alert defect recurred a 4th consecutive cycle today and widened** — now 7 raw Telegram alerts with no backing `proposed_signal` (ERA×3, EPIC×2, plus **new** OPN×1, BANK×1) — escalated further in §14. Stocks remain **chop, VIX 16.98**, zero A/B actionable; the same demoted shortlist (XOM/NVDA/XLE/AMD/AVGO/JPM/UNH/MSTR) is still blocked by the rolling paper-R drawdown guard, joined this cycle by PLTR/META/XLV/AMZN blocked on liquidity/sector/catalyst gates. TSLA, GOOGL, NOW reported/report earnings today — after-hours gap risk into the close. UNH (DOJ Medicare probe) and MSFT (securities-fraud flag) remain legal/headline AVOID. The Iran-Amazon-Bahrain claim followed up this cycle: still **unconfirmed by AWS/Bahrain/US officials, AWS status dashboard shows no service-level change** — closing that TODO per the prior review's own follow-up plan. Catalyst mapping remains weak (20.1% mapped, 5th+ consecutive weak cycle).

## 2. Data Used

- Crypto reports: scalp (2026-07-22 20:08 EEST gen / 17:00 UTC freshness — **fresh, ~1h40m old**, no A/B setups), intraday (17:34 EEST gen / 14:15 UTC freshness — **stale for fresh entries, ~7h25m old**, no newer intraday cycle has run since), swing (04:16 EEST / 01:15 UTC — **stale, ~17h25m old, >14h threshold**; used for narrative cross-check only).
- Stocks intraday report (2026-07-22 21:29 EEST gen / 18:29 UTC freshness — **fresh, ~10min old**, market still open ~1h20m left in RTH). Stocks swing/invest reports stale since 2026-07-02 (20 days) — excluded per known deprecation of the old swing/invest pipeline ([[project_crypto_ai_desk_stocks_position_framework]]).
- `data/catalysts/2026-07-22/catalyst_events.jsonl` (3500 rows, 703 mapped/20.1%) and `narrative_baskets.jsonl` (5 baskets active per latest scalp report: perps_dex_narrative/HYPE, delisting_thin_liquidity/BTC, binance_ecosystem_teaser/BNB, ai_narrative/TAO, rwa_narrative/ONDO+XLM).
- `data/processed/llm_analysis_packet.md` (20:09 EEST), `llm_stocks_packet.md` (20:34 EEST).
- CLI: `active-signals --asset-class crypto` (22 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto` (headline PF 1.97/totalR +42.71/n=174 reliable), `signal-stats --asset-class stocks` (A/B headline sample=0; C-tier PF 0.955/totalR -0.5), `detect_untracked_legacy_alerts --since 2026-07-22` (**7 untracked**: ERA×3, EPIC×2, OPN×1, BANK×1).
- External web research: 2 WebSearch queries (BTC/ETH price+macro tape for today, Iran-Amazon-Bahrain status follow-up) + 1 WebFetch (Yahoo Finance BTC/ETH price piece, verified opened). No "external web research unavailable" fallback needed.
- Previous review for diff: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-22_1839.md` (US open reaction review, 18:39 EEST).

## 3. Scheduler / Data Freshness

- Scheduler folder: `data/scheduled_runs/2026-07-22_default_schedule/` (new folder rolled over today; `data/scheduled_runs/2026-07-21_default_schedule/` still holds today's cycle history up to cycle_09).
- `scheduler.log` mtime: 21:31 EEST in the new folder (~8min old — fresh) / 20:40 EEST in the prior folder (~59min old — fresh either way, well under 3h defer threshold).
- Latest cycle summary: `cycle_09_20-00_summary.md`, mtime 20:40 EEST (~59min old — fresh).
- Monitors alive and current: `crypto_monitor` (log 21:36 EEST), `derivatives_monitor` (21:37 EEST), `stocks_monitor` (21:39 EEST, live during RTH), `pending_monitor` (20:01 EEST), `mexc_canary_monitor` (20:01 EEST).
- No defer triggered.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-22 21:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.8,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_09 mtime 20:40 EEST, ~59min old — fresh", "crypto intraday report ~7h25m old — carry-forward/stale for fresh-entry timing, no newer cycle since 14:35", "crypto swing report ~17h25m old — stale (>14h), narrative cross-check only", "stocks swing/invest stale since 2026-07-02, known-deprecated pipeline", "stocks intraday report fresh, ~10min old"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["mixed", "risk_off", "chop", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH labelled uptrend, 68.4% breadth>EMA20 (up from 63-65%), macro risk still 100/100 on Iran/Hormuz/oil (Brent >$95)", "externally confirmed: BTC opened ~$66.5K, faded to ~$65.5K by US morning; ETH opened ~$1,929, faded to ~$1,918 — 'open higher, lose steam' pattern, not clean continuation", "stocks regime=chop, neutral bias, VIX 16.98, 0/4 indices trending up, breadth20=50%/breadth50=100% (index-level noise)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 20.1% mapped / 79.9% unmapped today (3500 rows, up from 19.7% last cycle) — 5th+ consecutive weak cycle", "ZAMA/EPIC/AKE B-tier ideas all explicitly 'no fresh verified catalyst detected', and now stale (7h old report)", "rwa_narrative (ONDO/XLM) basket still active <6h and consistent with ONDO/USDT's already-profitable intraday leg (tp2_hit)"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable", "funding_extreme"], "data_missing": ["OI history for MEXC-fallback symbols (n/a% OI change on most top movers)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["RIF/USDT: negative funding (-0.02 mexc), 24h -21.1%, crowding elevated externally — capped to C (thin_liquidity_short_squeeze_risk), same squeeze setup carried forward unresolved since prior cycle", "ZAMA/EPIC/AKE/BANK: funding neutral/normal, crowding normal-to-low — no squeeze signal on the long side, but stale data (7h)"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["stale_before_entry", "entry_late", "chase_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["Crypto intraday report (source of ZAMA/EPIC/AKE ideas) is ~7h25m old with zero re-confirmation since — treat as stale context, not a live trigger", "VANA/USDT and KITE/USDT are the only genuinely current signals (waiting_for_entry, real proposed_signal rows, not just report text) — entry zones 1.2126-1.2205 and 0.118921-0.119737 respectively, neither triggered yet", "BANK/USDT: recurring thin-volume chase pattern (0.05-0.19x volume on double-digit % moves) flagged across multiple cycles today"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.72,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["22 active crypto signals: 2 waiting_for_entry (VANA, KITE), 1 triggered-unresolved (MIRA), 12 tp1_hit, 7 tp2_hit", "1 crypto row (NEAR/USDT short) shows tp1_hit with an expires_at in the past (2026-07-17) — entered-unresolved past its nominal window, needs manual review of why it still shows as active", "50 active stocks signals, all legacy C-tier/research grade, 2 waiting_for_entry (DIA, AAPL shorts) — none current A/B", "7 untracked legacy alerts (ERA×3, EPIC×2, OPN×1, BANK×1) with no proposed_signal — needs_review, 4th consecutive cycle, widened to 2 new symbols this cycle"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: live DOJ criminal+civil Medicare-billing investigation, legal_headline_risk gate stands (C-tier, sec_doj)", "MSFT: securities_fraud legal_headline_risk gate, demoted B→C", "TSLA/GOOGL/NOW earnings today — do_not_chase_warning active into/after the print", "ADA/BNB: Wanchain Cardano-BNB bridge exploit (515M NIGHT / ~$9M drained) — operator-review warning active on both symbols", "AMZN Bahrain claim: followed up this cycle — still unconfirmed by AWS/Bahrain/US officials, AWS status dashboard shows no service-level change; closing out per prior review's own plan (§14)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week: swing PF 2.97/n50 and intraday PF 2.08/n84 both healthy actionable-primary; scalp PF 0.67/n40 negative (kill-switched already)", "crypto direction=short: PF 0.125/avgR -0.583/n8 (anecdotal but consistently bad) — avoid new shorts without very strong confirmation", "crypto headline (A/B): PF 1.97, totalR +42.71, winrate 34.3%, n=174 reliable — essentially flat vs last cycle (totalR 43.71→42.71, one closed loser since)", "stocks Model F forward_postfreeze (14d/30d): -2.5R/PF0.50/n11 — negative, small sample, but consistent with the guard correctly blocking new A/B this cycle"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.58,
      "reason_codes": ["wait_for_trigger", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.58,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "VANA/USDT", "trigger": "wait for fill inside 1.2126-1.2205 waiting_for_entry zone; invalidation 1.2030", "reason": "the only genuinely current (non-stale) crypto long signal in the active book — a real proposed_signal, not a 7h-old report idea" },
    "best_short_candidate":    { "symbol": "RIF/USDT", "trigger": "wait for a failed reclaim of prior support and confirmed OI unwind/funding normalization before shorting; still thin_liquidity_short_squeeze_risk-capped, same unresolved setup as last cycle", "reason": "highest raw weak_rs_short score among today's laggards, but squeeze risk has not cleared in two consecutive cycles" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "hold/retest of the rwa_narrative basket structure; the existing intraday leg is already tp2_hit, so this is about managing/adding on a fresh pullback, not a new blind entry", "reason": "multi-week RWA/tokenization institutional thesis, only crypto catalyst-linked name with a demonstrated profitable outcome this week" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "score 75 (was B) but carries a live DOJ criminal+civil Medicare-billing investigation — legal/headline risk overrides score; manual review required, unchanged for the 4th+ consecutive cycle today" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.80 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.62 | mixed, risk_off, chop, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable, funding_extreme | advisory_only |
| technical_entry | caution | 0.50 | stale_before_entry, entry_late, chase_risk | advisory_only |
| execution_lifecycle | needs_review | 0.72 | waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.68 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.58 | wait_for_trigger, longs_preferred | advisory_only |

## 4. What Changed vs Previous Review

Previous review (18:39 EEST, US open reaction review) named **ZAMA/USDT** best long (pullback watch), **RIF/USDT** best short-watch (squeeze must clear), **ONDO/USDT** best catalyst-backed, **UNH** avoid, and reported **5** untracked legacy alerts (ERA×3, EPIC×2).

- **Untracked alerts: escalated again, 5→7.** New this cycle: **OPN/USDT** (17:54:11 UTC) and **BANK/USDT** (18:05:30 UTC) both fired raw Telegram watchlist alerts with no backing `proposed_signal`. This is now the **4th consecutive cycle today** with this defect, and it has widened beyond ERA/EPIC to two new symbols — escalating priority in §14.
- **ZAMA/EPIC/AKE ("best idea" from 18:39):** no newer intraday cycle has run since 14:35, so this idea is now ~7h old with zero fresh confirmation. Downgrading from "watch, near-trigger" to "stale, do not treat as a fresh signal until the next intraday cycle (due imminently, cadence ~3h) refreshes it."
- **New this cycle:** VANA/USDT and KITE/USDT both entered `waiting_for_entry` — these are real system-generated signals (not report text), the first genuinely fresh crypto long ideas since the open-reaction review found zero waiting_for_entry rows. MIRA/USDT moved to `triggered` (entered, unresolved).
- **RIF/USDT:** unchanged, still squeeze-capped, still not a clean short — 2nd consecutive cycle with no resolution.
- **ONDO/USDT:** unchanged as the catalyst-backed pick; its intraday leg is confirmed `tp2_hit` (profitable), reinforcing the RWA thesis rather than just repeating it.
- **UNH:** unchanged, still legal/headline-risk AVOID (DOJ investigation).
- **AMZN Bahrain claim: closed out this cycle.** Re-checked per the 18:39 review's own follow-up plan — still unconfirmed by AWS/Bahrain/US officials, AWS's public status dashboard still shows no service-level change, roughly 24h+ since the original claim with no material impact materializing. Downgrading from "open TODO, low priority" to **closed** (§14).
- **Catalyst mapping:** 19.7%→20.1% — marginal, still far below the 50% usability bar, now a 5th+ consecutive weak cycle.
- **Stocks demoted shortlist widened:** XOM/NVDA/XLE/AMD/AVGO/JPM/UNH/MSTR carry forward on the drawdown guard/legal gates; **new this cycle** — PLTR, META, XLV, AMZN demoted via the SI-1..5 liquidity/sector/catalyst gates (4 fresh demotions this cycle per the report's own count).

## 5. Catalyst Coverage

- Total catalyst events in `catalyst_events.jsonl`: **3500** rows.
- Mapped (symbol present): **703** (20.1%). Unmapped: **2797** (79.9%).
- Narrative baskets: **5** active per the latest (20:08) scalp report (`perps_dex_narrative` primary HYPE; `delisting_thin_liquidity` primary BTC — avoid-low-liquidity playbook, not a BTC trade signal; `binance_ecosystem_teaser` primary BNB; `ai_narrative` primary TAO; `rwa_narrative` primary ONDO/XLM).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (5th+ consecutive cycle >50% unmapped — see TODO in §14.) Top unmapped items remain largely exchange operational notices (leverage adjustments, thin-pair delisting notices), not trade-relevant news.

## 6. Market Landscape

Crypto trend structure remains bullish (BTC/ETH uptrend labels, altcoin breadth now 68.4% above EMA20), but the session shape today was "open higher on CLARITY Act optimism + 6 days of ETF inflows, then fade through the US morning" — BTC $66.5K→$65.5K, ETH $1,929→$1,918 — while the macro-risk score stays pinned at 100/100 on the ongoing Iran-Hormuz conflict and Brent >$95. This is a market that wants to be risk-on structurally but keeps getting capped by a real, externally-confirmed geopolitical overhang. Stocks are in a chop regime (VIX 16.98, 0/4 major indices trending), energy and healthcare the only sectors with real relative strength (XLE +6.7% RS/20d, XLV +3.0% RS/20d), semiconductors/technology lagging. With ~1h20m left in the US cash session, this is a window for managing existing exposure and watching the two live crypto waiting_for_entry triggers — not for chasing anything new, crypto or stocks.

### Market Mood / Risk Routing
- Crypto mood:           mixed (bullish trend structure, fading morning strength, risk-off macro headwind persists)
- Stocks mood:           chop, ~1h20m left in RTH
- Dominant narrative:    RWA/tokenization (ONDO/XLM, already profitable this week) remains the strongest catalyst-linked thesis; momentum-only cluster (ZAMA/EPIC/AKE/BANK) is stale and lacks catalyst backing
- Preferred side now:    longs (crypto, selective, wait for VANA/KITE fills), wait-for-trigger (stocks, into the close)
- Best long candidate:   VANA/USDT (see §8)
- Best short candidate:  RIF/USDT — squeeze risk still not cleared, 2nd cycle unresolved (see §8)
- Best catalyst-backed candidate: ONDO/USDT — thesis reinforced by a confirmed tp2_hit outcome (see §8)
- What to avoid:         UNH (DOJ legal risk), MSFT (securities-fraud legal risk), BANK/USDT (recurring thin-volume chase + now an untracked-alert symbol), stale ZAMA/EPIC/AKE report ideas until re-confirmed next cycle
- What would change the view: a confirmed de-escalation headline on Iran/Hormuz, a fresh (non-stale) intraday cycle re-confirming ZAMA/EPIC/AKE, or the stocks drawdown guard lifting post-close review

## 7. Candidate Deep Dives

### 7.1 VANA/USDT (crypto, long, B-tier, intraday — score 66.1, waiting_for_entry)
- **Reacted already?** Unclear from active-signals alone (no fresh report line-item; this signal is more than 7h old itself if it traces to the same intraday cycle, but it remains genuinely `waiting_for_entry`, i.e. not yet filled).
- **Chasing?** No — by definition still waiting for price to reach the 1.2126-1.2205 entry zone.
- **Actionable level:** fill inside 1.2126-1.2205; invalidation 1.2030.
- **Mood alignment:** Consistent with "selective longs, wait for pullback fills" — this is exactly that: a standing limit-style wait, not a market chase.
- **Chase risk:** Low — the entry hasn't triggered yet, so there's no extension risk to manage.
- **Catalyst:** Not verified in today's reports; treat as momentum-class, size accordingly.
- **Data-quality caveat:** No fresh (same-day, current-hour) report text corroborates this specific signal's thesis; it is being read purely from the active-signals table. Chart/manual TradingView check unavailable (no chart MCP loaded this run).

### 7.2 KITE/USDT (crypto, long, B-tier, intraday — score 65.7, waiting_for_entry)
- Same structural profile as VANA: standing limit order, not yet filled, entry 0.118921-0.119737, invalidation 0.117923.
- **Note:** A separate, older KITE/USDT signal (different signal_id) already sits at tp1_hit in the same active-signals table — this is a fresh, distinct signal on the same symbol, not a duplicate.
- **Verdict:** Watch for fill; do not manually pre-position ahead of the zone.

### 7.3 MIRA/USDT (crypto, long, B-tier, intraday — score 67.1, triggered/entered-unresolved)
- Entry has been filled (entry zone was 0.050800-0.052739); position is open and unresolved as of this review — no TP/stop hit yet, expires 2026-07-23T17:15:26.
- **Status language:** ENTERED UNRESOLVED — not a missed entry, not yet a win/loss. Monitor for TP1/invalidation into the next cycle.

### 7.4 RIF/USDT (crypto, short-watch, C-tier — squeeze-capped)
- Unchanged for a 2nd consecutive cycle: 24h -21.1%, negative external funding (-0.02 mexc), crowding elevated — `thin_liquidity_short_squeeze_risk` cap still in force.
- **Actionable level:** wait for a failed reclaim of prior support plus visible OI unwind/funding normalization before treating as a clean short — chasing the existing weakness risks getting squeezed.
- **Legal/headline risk:** none flagged.

### 7.5 ONDO/USDT (crypto, catalyst-backed, RWA thesis)
- The scalp-mode leg is `tp1_hit`; the intraday-mode leg is `tp2_hit` — this thesis is working, not just theoretical.
- **rwa_narrative basket** remains active <6h with XLM as secondary.
- **Actionable level (for adding, not initiating):** wait for a fresh pullback into the basket's support structure before sizing further; do not chase the already-realized move.

### 7.6 UNH (stocks, avoid, C-tier demoted from B — score 75)
- **LEGAL/HEADLINE RISK** — live DOJ criminal+civil Medicare-billing investigation, tagged `legal_headline_risk: sec_doj`, unchanged across at least 4 consecutive review cycles today.
- Hard AVOID / manual-review-only regardless of technical setup.

### 7.7 NEAR/USDT (crypto, short, integrity flag — entered-unresolved past window)
- Active-signals shows this scalp-mode short at `tp1_hit` with `expires_at` = **2026-07-17T15:56:12**, i.e. **5 days in the past** relative to this review.
- **System-integrity issue:** a signal remaining in the "active" query result set past its own nominal expiry window is either (a) a genuinely still-open entered-unresolved position the system is correctly still tracking toward final resolution, or (b) a stale row that should have been closed/archived. Cannot distinguish from the CLI output alone — flagged for manual review, not treated as a live trading idea either way (§14).

## 8. Best Candidates Ranked

1. **VANA/USDT (long-watch)** — trigger: fill inside 1.2126-1.2205, invalidation below 1.2030. The only genuinely fresh, non-stale crypto long signal in the book right now.
2. **ONDO/USDT (catalyst-watch, add-only)** — trigger: fresh pullback into the rwa_narrative basket's support after the already-realized tp2_hit move; the strongest catalyst-linked thesis this week, evidenced not just claimed.
3. **KITE/USDT (long-watch)** — trigger: fill inside 0.118921-0.119737, invalidation below 0.117923. Same standing-wait profile as VANA, slightly lower score.
4. **RIF/USDT (short-watch)** — trigger: confirmed failed reclaim + OI unwind/funding normalization before shorting; still squeeze-prone for a 2nd cycle, not a clean short yet.
5. ZAMA/EPIC/AKE — downgraded to stale/context-only pending the next (fresher) intraday cycle; do not treat as live triggers off the current 7h-old report.
6. AVGO/UNH/MSFT (stocks) — unchanged carry-forwards, still blocked by guard/legal gates with ~1h20m left in RTH; nothing to chase into the close.

## 9. Avoid / No Trade

This is a decision-window call only — scanning, tracking, and data collection all continue regardless (see ALWAYS-SCAN rule; never a system-stop instruction).

- **UNH** — DOJ legal risk overrides score; manual review only.
- **MSFT** — securities-fraud legal risk flag; manual review only.
- **BANK/USDT** — recurring thin-volume chase pattern across multiple cycles today, and now also an untracked-alert symbol (data-integrity concern layered on top of the chase-risk concern).
- **ZAMA/EPIC/AKE** — stale (7h-old report); do not treat today's earlier "actionable" framing as still live without a fresh re-confirmation.
- **TSLA, GOOGL, NOW** — earnings today; do-not-chase into/after the print regardless of technical setup quality; after-hours gap risk into and past the close.
- **Crypto scalp mode generally** — kill-switched (mode off, any hour/day) and structurally negative (PF 0.67, -3.6R over 14d) even before the switch; the fresh 20:08 report itself found zero A/B setups worth surfacing.
- **ADA, BNB** — active `exploit_hack` operator-review warnings (Wanchain Cardano-BNB bridge, ~$9M/515M NIGHT drained); not a hard block but treat any new long thesis on these two with reduced confidence until the exploit fallout is understood.

## 10. Main Risks

- **Macro/geopolitical:** Iran-US/Hormuz conflict ongoing, oil >$95, macro risk score pinned at 100/100 for multiple consecutive cycles — a genuine, externally-confirmed risk-off overhang; today's price action (open higher, fade through the US morning) is consistent with that headwind capping an otherwise risk-on tape.
- **Data-integrity:** the untracked-alert defect is now a 4th-consecutive-cycle recurrence and has widened from 2 symbols (ERA/EPIC) to 4 (adding OPN/BANK) — any Telegram-driven manual action on any of these four today would be invisible to the desk's own performance tracking.
- **Stale-data risk:** the crypto intraday report (source of the ZAMA/EPIC/AKE ideas) is ~7h25m old with no re-confirmation cycle since — do not treat those ideas as live without the next cycle refreshing them.
- **Signal-lifecycle anomaly:** NEAR/USDT shows `tp1_hit` with an expiry 5 days in the past — needs a manual check on whether this is legitimate entered-unresolved tracking or a stale row (§7.7, §14).
- **Legal/headline:** UNH (DOJ) and MSFT (securities fraud) both carry live, unresolved legal risk; ADA/BNB carry a fresh exploit-related operator-review warning.
- **Earnings/gap risk:** TSLA, GOOGL, NOW report today; LMT tomorrow — after-hours and next-day gap risk on any of these names.

## 11. Action Plan — next 4 hours

- Watch for fills on VANA/USDT (1.2126-1.2205) and KITE/USDT (0.118921-0.119737); do not manually pre-position ahead of either zone.
- Monitor MIRA/USDT (entered-unresolved) into its next TP/invalidation checkpoint.
- Watch RIF/USDT for signs the short squeeze is exhausting (funding normalizing, OI rolling over) before treating the short as clean — 2nd consecutive cycle unresolved.
- Watch ONDO/USDT for a fresh pullback into the rwa_narrative basket structure if adding to the already-profitable thesis; do not chase the realized move.
- Flag the NEAR/USDT past-expiry entered-unresolved row and the widened untracked-alert defect (now 4 symbols) to a human-driven session for manual investigation (§14).
- Re-check the stocks demoted-C list (XOM/NVDA/XLE/AMD/AVGO/JPM/PLTR/META/XLV/AMZN) after the 23:00 EEST close for any drawdown-guard resolution or fresh operator sign-off ahead of tomorrow's session.
- No new-position urgency into the last ~80 minutes of RTH — this is a manage-and-monitor window, not a sourcing window.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade — kill-switched, structurally negative (PF 0.67, -3.6R/14d), fresh 20:08 report itself found nothing worth surfacing.
- **Crypto intraday:** Watch-only. Two genuinely fresh signals (VANA, KITE) waiting_for_entry; MIRA entered-unresolved; ZAMA/EPIC/AKE report ideas now stale (7h) — do not treat as live without next-cycle re-confirmation.
- **Crypto swing:** Stale report (17h25m old) — treat existing ONDO/OPN/ALLO swing positions (several already tp1/tp2_hit) as carry-forward context only, no fresh entries off this data.
- **Stocks intraday:** No trade — chop regime, 0 actionable A/B, demoted shortlist widened this cycle (PLTR/META/XLV/AMZN added), ~80min left in RTH, nothing to chase into the close.
- **Stocks swing/invest:** Data stale since 2026-07-02 (pipeline deprecated) — no view rendered.
- **System-wide:** Scanning, tracking, and monitors all continue normally; this is a manage-existing/watch-triggers window into the US close, not a stop-trading instruction.

## 13. Sources

- [Bitcoin and ethereum prices today, Wednesday, July 22, 2026: Both cryptos open higher before losing steam](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-july-22-2026-both-cryptos-open-higher-before-losing-steam-153454067.html) — fetched directly; BTC $66,508.87→$65,556.99, ETH $1,928.62→$1,918.35, CLARITY Act optimism + 6 days ETF inflows, 2026-07-22.
- [Iran targets Amazon Web Services data center in Bahrain](https://w.media/iran-targets-amazon-web-service-data-center-in-bahrain/) — Iran IRGC claim, still unconfirmed by Amazon/Bahrain/US, 2026-07-21/22.
- [Iran says it's struck offline AWS facility in Bahrain ... again](https://www.theregister.com/off-prem/2026/07/21/iran-says-its-struck-offline-aws-facility-in-bahrain-again/5275762) — notes AWS status dashboard shows no service-level change, no independent confirmation of damage, 2026-07-21.

## 14. Fix Requests / TODO

### TODO-untracked-alert-recurrence-4th-cycle-widened
- **issue:** Watchlist-alert/signal-reuse defect recurred for a **4th consecutive review cycle** today and **widened to two new symbols**: ERA/USDT ×3 (08:45, 09:26, 11:48 UTC), EPIC/USDT ×2 (12:35, 14:34 UTC), and **new this cycle** OPN/USDT ×1 (17:54:11 UTC) and BANK/USDT ×1 (18:05:30 UTC) — 7 raw Telegram alerts total today with no backing `proposed_signal`. Same defect class as the confirmed 2026-07-17 ALLO/BANK case ([[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]], already raised to high priority).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-22` → 7 untracked rows; cross-checked against `python -m src.cli active-signals --asset-class crypto` (22 rows, zero ERA/EPIC/OPN/BANK-matching untracked entries).
- **suggested manual fix:** Same root-cause investigation as the existing high-priority TODO, now more urgent given the widening pattern — confirm whether new symbols (OPN, BANK) hitting this same defect class rules out a symbol-specific cause and points at a systemic issue in the watchlist-alert re-fire path.
- **priority:** high (escalated — 4th cycle, widening symbol set)
- **first observed:** 2026-07-17 (this recurrence: 2026-07-22 21:39 EEST, 4th consecutive cycle today)

### TODO-near-usdt-past-expiry-unresolved-signal
- **issue:** `active-signals --asset-class crypto` shows a NEAR/USDT short (scalp, sig_b16bb9e54598333a) at status `tp1_hit` with `expires_at` = 2026-07-17T15:56:12 — 5 days in the past relative to this review. Cannot determine from CLI output alone whether this is legitimate entered-unresolved tracking (position still genuinely open) or a stale row that should have closed/archived.
- **evidence:** `python -m src.cli active-signals --asset-class crypto`, row `sig_b16bb9e54598333a | NEAR/USDT | crypto | B | scalp | short | 66.1 | tp1_hit | ... | 2026-07-17T15:56:12`.
- **suggested manual fix:** Manually inspect this signal_id in the signals DB to confirm whether it is still genuinely open (and if so, why the nominal expiry window didn't force a resolution/close) or whether it's a stale row that the active-signals query should be excluding.
- **priority:** medium
- **first observed:** 2026-07-22 21:39 EEST

### TODO-catalyst-mapping-persistent-weak
- **issue:** Catalyst symbol-mapping coverage has been below the 50% usability bar for 5+ consecutive review cycles (17.2%→18.9%→19.7%→20.1% across today's cycles).
- **evidence:** `data/catalysts/2026-07-22/catalyst_events.jsonl` — 3500 rows, 703 mapped (20.1%), 2797 unmapped (79.9%); majority of unmapped items are exchange operational notices (leverage adjustments, thin-pair delisting notices) rather than trade-relevant news.
- **suggested manual fix:** Unchanged from prior reviews — improve the symbol resolver in the catalyst layer, or bucket operational-notice-only sources separately so the mapped% metric isn't diluted by noise.
- **priority:** medium
- **first observed:** carried forward from prior reviews (multi-day pattern)

### TODO-amzn-bahrain-claim-status (CLOSED this cycle)
- **issue:** Follow-up on the 16:20/18:39-review TODO — the Iran-IRGC claim of a cruise-missile strike on AWS/Amazon's Bahrain data infrastructure. Re-checked this cycle per the 18:39 review's own plan.
- **evidence:** WebSearch "Amazon AWS Bahrain data center Iran strike confirmed status July 22 2026" — theregister.com and w.media both confirm the claim remains unconfirmed by Amazon/Bahrain/US officials, and AWS's public status dashboard shows no service-level change, ~24h+ after the original claim.
- **resolution:** Closing out as "claimed, never materially impactful" per the prior review's own criteria (still unconfirmed + no service impact by this review). No further follow-up planned unless new information surfaces.
- **priority:** closed
- **first observed:** 2026-07-22 16:20 EEST; closed 2026-07-22 21:39 EEST

### TODO-ake-exchange-listing-data-conflict (carried forward, unchanged)
- **issue:** Internal reports tag AKE/USDT as "MEXC-only listing (exchange confirmation missing)" and reject/cap it to C-tier on that basis; external sources (CoinGecko, CoinMarketCap, Gate, Phemex) described AKE ("Akedo") as heavily Binance-listed as of the 18:39 review. No new information this cycle (AKE has rolled off the active/report top-N again).
- **evidence:** See 18:39 review's TODO for full detail; unchanged this cycle.
- **suggested manual fix:** Unchanged — manually check whether the Binance exchange-universe fetch for AKE/USDT is failing silently, and re-run the exchange-confirmation classifier once resolved.
- **priority:** medium
- **first observed:** 2026-07-22 18:39 EEST
