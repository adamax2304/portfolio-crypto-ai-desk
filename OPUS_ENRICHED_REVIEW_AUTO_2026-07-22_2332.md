# Opus Enriched Review — post-close final daily review — Auto Cycle 23:32 EEST

## 1. Executive Summary

Slot: **post-close final daily review** (23:32 EEST / 20:32 UTC / ~16:32 ET, US cash session closed at 23:00 EEST). Advisory only — no auto-trade, no scoring/strategy changes. US cash close: SPX -0.1%, Nasdaq -0.5%, Dow ~flat, ahead of Alphabet/Tesla earnings. **GOOGL beat and traded up after-hours** (EPS $1.89 vs $1.84 est, revenue $84.74B +13.6%, Cloud $10.35B beat, YouTube ad revenue missed) — externally confirmed. **TSLA earnings call is at 5:30pm ET (00:30 EEST) — not yet held as of this review; no result to report, do not fabricate a reaction.** Crypto: BTC/ETH opened higher again today (+2%/+1.3%, 6th consecutive day of positive spot-ETF inflows) then **faded through the US morning** (BTC $66.5K→$65.6K, ETH $1,929→$1,918) before partially recovering into the evening (~$65.9K) — a 2nd consecutive session of "open strong, lose steam." Altcoin breadth improved through the day (68.4%→73.7% above EMA20). The desk's macro-risk score stays pinned at **100/100**; external research confirms this is not noise — it is the ongoing **2026 Strait of Hormuz war** (US/Israel strikes on Iran since Feb 28, sea mines, ~6,000 seafarers stranded, the June 17 truce broken by renewed strikes). **No A-tier setups anywhere** (crypto or stocks). Crypto's only genuinely fresh, current system signals are **RE/USDT and KITE/USDT** (`waiting_for_entry`); **VANA/USDT** moved to `triggered` (entered, unresolved) since the last review. The **known untracked-alert defect recurred a 5th consecutive cycle and widened again** — now **9** raw Telegram alerts with no backing `proposed_signal` (ERA×3, EPIC×3, OPN×1, BANK×1, **new** AKE×1) — notably including EPIC/USDT, today's single highest-scoring symbol (91.6), reinforcing this is systemic, not symbol-specific — escalated further in §14. Stocks: chop, VIX 16.98, **zero A/B actionable** all session — the same drawdown-guard/gate-demoted shortlist (XOM/AMD/NVDA/XLE/AVGO/JPM/MSTR/META/PLTR/XLV/LLY/NFLX/AMZN, MSFT legal-risk) carried through the close. UNH (DOJ Medicare investigation) and MSFT (securities-fraud flag) remain legal/headline AVOID, unchanged for a 5th+ consecutive cycle. Catalyst mapping remains weak (20.4% mapped, 5th+ consecutive weak cycle). Scanning, tracking, and all monitors continue overnight into the Asia session as normal.

## 2. Data Used

- Crypto reports: intraday (2026-07-22 22:04 EEST gen / 19:00 UTC freshness — **fresh, ~1h30m old**), scalp (20:08 EEST gen / 17:00 UTC freshness — **fresh, ~3h25m old**, own banner flags scalp as low-confidence, PF 0.14 over 14d), swing (04:16 EEST / 01:15 UTC — **stale, ~19h15m old, >14h threshold**, narrative cross-check only, excluded from final verdict).
- Stocks intraday report (2026-07-22 22:56 EEST gen / 19:55 UTC freshness — **fresh, ~35min old**, covers the full regular session into the close). Stocks swing/invest stale since 2026-07-02 (20 days) — excluded per known deprecation of the old swing/invest pipeline ([[project_crypto_ai_desk_stocks_position_framework]]).
- `data/catalysts/2026-07-22/catalyst_events.jsonl` (4000 rows, 814 mapped/20.4%) and `narrative_baskets.jsonl` (5 active baskets per latest intraday report: perps_dex_narrative/HYPE, delisting_thin_liquidity/BTC, binance_ecosystem_teaser/BNB, ai_narrative/TAO+RENDER+FET+NEAR, rwa_narrative/ONDO+XLM).
- `data/processed/llm_analysis_packet.md` (22:05 EEST), `llm_stocks_packet.md` (22:44 EEST).
- CLI: `active-signals --asset-class crypto` (22 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto` (headline PF 1.9269/totalR +41.71/n=175 reliable), `signal-stats --asset-class stocks` (A/B headline sample=0; C-tier PF 1.0455/totalR +0.5/n=185), `detect_untracked_legacy_alerts --since 2026-07-22` (**9 untracked**: ERA×3, EPIC×3, OPN×1, BANK×1, AKE×1).
- External web research: 6 WebSearch queries (BTC/ETH price+macro tape, US stock close + TSLA/GOOGL earnings, TSLA-specific results, GOOGL-specific results, Iran/Hormuz status, live BTC level) + 2 WebFetch (Yahoo Finance BTC/ETH price piece — verified opened; TSLA/GOOGL earnings blog on Yahoo — used for context). CNBC live-blog fetch returned HTTP 403 (blocked, not usable as a citation).
- Previous review for diff: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-22_2139.md` (late-session risk review, 21:39 EEST).

## 3. Scheduler / Data Freshness

- Scheduler folder: `data/scheduled_runs/2026-07-22_default_schedule/`.
- `scheduler.log` mtime: 22:55 EEST (~37min old — fresh, well under the 3h defer threshold).
- Latest cycle summary: `cycle_01_21-49_summary.md`, mtime 22:55 EEST (~37min old — fresh).
- Monitors alive and current: `crypto_monitor` (23:26 EEST), `derivatives_monitor` (23:31 EEST), `stocks_monitor` (22:59 EEST), `mexc_canary_monitor` (21:51 EEST), `pending_monitor` (21:51 EEST), `watchlist_monitor` (23:27 EEST). All within the last ~1h40m.
- No defer triggered.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "post_close",
  "as_of": "2026-07-22 23:32 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle mtime 22:55 EEST, ~37min old — fresh", "all 6 monitors alive within last ~1h40m", "crypto intraday/scalp fresh (~1.5h/~3.4h), swing ~19h15m old — stale (>14h), stocks swing/invest stale since 2026-07-02 (known-deprecated pipeline)", "stocks intraday report fresh, ~35min old, covers full session into the close"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["mixed", "risk_off", "chop", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH labelled uptrend, breadth improved 68.4%→73.7%>EMA20 through the day, macro risk still 100/100", "externally confirmed: BTC opened $66,508.87 (+2%), faded to $65,556.99 by NY morning, recovered to ~$65,900 by evening — still below the open, 2nd consecutive 'fade' session", "externally confirmed: 2026 Strait of Hormuz war (US/Israel strikes on Iran since Feb 28), truce broken, shipping near-standstill — the macro-risk score reflects a real sustained conflict, not headline noise", "stocks closed: SPX -0.1%, Nasdaq -0.5%, Dow ~flat; regime label chop, VIX 16.98, 0/4 indices trending"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 20.4% mapped / 79.6% unmapped today (4000 rows, up slightly from 20.1% last cycle) — 5th+ consecutive weak cycle", "RE/KITE/ZAMA/AKE B-tier ideas all explicitly 'no fresh verified catalyst detected'", "rwa_narrative (ONDO/XLM) basket active <6h and consistent with ONDO/USDT's already-profitable outcomes (tp1_hit scalp, tp2_hit intraday)", "ADA/BNB carry an active exploit_hack operator-review warning (Wanchain Cardano-BNB bridge, ~$9M drained), unresolved since earlier today"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable", "funding_extreme"], "data_missing": ["OI history for MEXC-fallback symbols (n/a% OI change on most top movers)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["RIF/USDT: negative funding (-0.0052 mexc), 24h -27.2%, crowding elevated externally — same unresolved squeeze setup carried forward at least a 3rd consecutive cycle", "MIRA/USDT: heavily negative funding (-0.0167), crowding elevated externally, but no matching system signal exists for it (see technical_entry)", "RE/EPIC/ZAMA/AKE/BANK: funding neutral/normal, crowding normal — no squeeze signal on the long side"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_fresh", "stale_before_entry", "chase_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["RE/USDT and KITE/USDT are genuinely current: real proposed_signal rows, status waiting_for_entry, entry zones matching the fresh 22:04 intraday report line items exactly", "VANA/USDT moved from waiting_for_entry (21:39 review) to triggered (entered, unresolved) this cycle — no chase risk to manage, already filled", "MIRA/USDT: the 22:04 report's own #1 Trade Idea (score 66.7) has NO matching row in active-signals — a report-idea/system-signal mismatch; treat as unconfirmed context, not a live trigger", "BANK/USDT: recurring thin-volume pattern (0.02-0.05x volume on 27%+ moves) across multiple cycles today, plus it is itself one of today's untracked-alert symbols"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.72,
      "reason_codes": ["waiting_for_entry", "entered_unresolved", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["22 active crypto signals: 2 waiting_for_entry (RE, KITE), 1 entered-unresolved (VANA), 18 open/TP-progressing (tp1_hit or tp2_hit, still tracked), 1 needs_review (NEAR/USDT, tp1_hit with expires_at 5 days in the past)", "50 active stocks signals, all legacy C-tier/research grade, zero current A/B", "9 untracked legacy alerts (ERA×3, EPIC×3, OPN×1, BANK×1, AKE×1) with no proposed_signal — needs_review, 5th consecutive cycle, widened again this cycle (AKE new)"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.62,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": ["TSLA earnings result (call not yet held)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: live DOJ criminal+civil Medicare-billing investigation, legal_headline_risk gate stands, unchanged 5th+ consecutive cycle", "MSFT: securities_fraud legal_headline_risk gate, demoted B→C, unchanged", "GOOGL beat Q2 estimates and traded up after-hours (externally verified) — not swing-actionable in this system (market closed, RTH-only stocks intraday), planning context only for tomorrow", "TSLA earnings call is at 5:30pm ET / 00:30 EEST — has not happened yet as of this review; explicitly no result to report", "ADA/BNB: Wanchain Cardano-BNB bridge exploit operator-review warning remains active, unresolved"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.68,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week: swing PF 2.97/n=50 and intraday PF 1.99/n=85 both healthy actionable-primary; scalp PF 0.67/n=40, totalR -3.60 — negative, matches the scalp report's own banner (14d PF 0.14, 1W/7L, 'low confidence')", "crypto direction=short: n=8, anecdotal but consistently bad — avoid new shorts without very strong confirmation", "crypto headline (A/B): PF 1.9269, totalR +41.71, winrate 34.1%, n=175 reliable — signal-stats' own observation flags B-tier 34% winrate as low, worth reviewing entries", "stocks C-tier: PF 1.0455, totalR +0.5, n=185 — near-breakeven watchlist grade only, A/B sample still 0"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["wait_for_trigger", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "RE/USDT", "trigger": "fill inside 0.4754-0.4857 (waiting_for_entry); invalidation 1h close beyond 0.4628", "reason": "freshest genuinely current crypto long signal in the book — real proposed_signal from the 22:04 intraday cycle, not stale report text" },
    "best_short_candidate":    { "symbol": "RIF/USDT", "trigger": "wait for a failed reclaim of prior support plus confirmed OI unwind/funding normalization before shorting; still crowding-elevated/squeeze-prone for a 3rd+ consecutive cycle", "reason": "persistent weakest-symbol laggard (-27% 24h) across both today's scalp and intraday reports, but squeeze risk has not cleared" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "hold/retest of the rwa_narrative basket structure on a fresh pullback; the existing legs are already tp1_hit(scalp)/tp2_hit(intraday), so this is about managing/adding, not a new blind entry", "reason": "the only crypto catalyst-linked name with demonstrated, repeated profitable outcomes this week" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "live DOJ criminal+civil Medicare-billing investigation overrides any technical score; manual review required, unchanged for the 5th+ consecutive cycle today" },
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
| market_regime | caution | 0.60 | mixed, risk_off, chop, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable, funding_extreme | advisory_only |
| technical_entry | caution | 0.55 | entry_fresh, stale_before_entry, chase_risk | advisory_only |
| execution_lifecycle | needs_review | 0.72 | waiting_for_entry, entered_unresolved, needs_review | advisory_only |
| risk_manager | caution | 0.62 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.68 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | wait_for_trigger, longs_preferred | advisory_only |

## 4. What Changed vs Previous Review

Previous review (21:39 EEST, late-session risk review) named **VANA/USDT** best long-watch, **RIF/USDT** best short-watch, **ONDO/USDT** best catalyst-backed, **UNH** avoid, and reported **7** untracked legacy alerts (ERA×3, EPIC×2, OPN×1, BANK×1).

- **Untracked alerts: escalated again, 7→9.** New this cycle: **EPIC/USDT** fired a 3rd alert (19:04:09 UTC) and **AKE/USDT** fired its first (19:04:13 UTC) with no backing `proposed_signal`. This is now the **5th consecutive cycle today** with this defect. Notably, EPIC/USDT is today's single highest-scoring symbol (91.6) in both the scalp and intraday reports — a top-scoring symbol repeatedly failing to convert into a tracked signal reinforces that this is systemic, not a low-quality-symbol artifact. Escalated further in §14.
- **VANA/USDT:** moved from `waiting_for_entry` (prior review) to `triggered` — entered, unresolved. No longer a "watch" candidate; now a position to manage.
- **New this cycle:** RE/USDT entered `waiting_for_entry` (fresh, matches the 22:04 intraday report's Trade Idea #5 exactly) — the new best long-watch candidate. KITE/USDT (the `waiting_for_entry` signal, distinct from the older tp1_hit KITE row) is unchanged, still waiting.
- **RIF/USDT:** unchanged, still squeeze-capped, still the weakest symbol in both today's scalp (-27.98%) and intraday (-27.20%) reports — 3rd+ consecutive cycle with no resolution.
- **ONDO/USDT:** unchanged as the catalyst-backed pick; both legs remain profitable (tp1_hit scalp, tp2_hit intraday).
- **UNH / MSFT:** unchanged, still legal/headline-risk AVOID.
- **New this cycle:** MIRA/USDT surfaced as the intraday report's #1 Trade Idea (score 66.7) but has **no matching active-signals row** — a report-idea/system-signal mismatch, flagged in §7 rather than treated as a live trigger.
- **Catalyst mapping:** 20.1%→20.4% — marginal, still far below the 50% usability bar, now a 5th+ consecutive weak cycle.
- **Macro context deepened:** external research this cycle confirmed the Iran/Hormuz macro-risk driver is the ongoing **2026 Strait of Hormuz war** (active since Feb 28, truce broken), not a transient headline — the 100/100 macro-risk score is now understood as reflecting sustained conflict risk.
- **Stocks:** market closed for the day; the same demoted shortlist from the last cycle carried through unchanged to the close. GOOGL reported and beat (after-hours, externally confirmed); TSLA has not yet reported (call pending 00:30 EEST).

## 5. Catalyst Coverage

- Total catalyst events in `catalyst_events.jsonl`: **4000** rows.
- Mapped (symbol present): **814** (20.4%). Unmapped: **3186** (79.6%).
- Narrative baskets: **5** active per the latest (22:04) intraday report (`perps_dex_narrative` primary HYPE; `delisting_thin_liquidity` primary BTC — avoid-low-liquidity playbook, not a BTC trade signal; `binance_ecosystem_teaser` primary BNB; `ai_narrative` primary TAO/RENDER/FET/NEAR; `rwa_narrative` primary ONDO/XLM).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (5th+ consecutive cycle >50% unmapped — see TODO in §14.) Top unmapped items remain largely exchange operational notices (leverage adjustments, thin-pair delisting notices), not trade-relevant news.

## 6. Market Landscape

The US cash session closed slightly lower — SPX -0.1%, Nasdaq -0.5%, Dow roughly flat — as investors positioned into Alphabet/Tesla earnings and rising oil prices weighed on sentiment. Alphabet beat on EPS ($1.89 vs $1.84 est), revenue (+13.6% to $84.74B), and Cloud ($10.35B vs $10.2B est), with shares trading up after-hours; YouTube ad revenue missed. Tesla's results are not yet public (earnings call at 5:30pm ET / 00:30 EEST) — no reaction to report. Sector rotation into the close favored energy (XLE, RS +6.7%/20d) and healthcare (XLV, RS +2.7%/20d), with semiconductors (SMH, RS -7.4%/20d) and technology (XLK, RS -3.9%/20d) lagging. Crypto's session shape mirrored yesterday: open higher on ETF-inflow and CLARITY-Act optimism, fade through the US morning (BTC $66.5K→$65.6K, ETH $1,929→$1,918), partial recovery into the evening (~$65.9K, still below the open). Altcoin breadth improved through the day (68.4%→73.7% above EMA20) even as BTC itself stayed net-negative on the day — a sign of selective alt strength inside a still-capped macro backdrop. That macro cap is real and structural: the Strait of Hormuz war (US/Israel vs. Iran, active since Feb 28, truce broken by renewed strikes in recent weeks) keeps oil elevated and the desk's macro-risk score pinned at 100/100. Heading into the Asia session overnight, this is a market that wants to be risk-on on crypto technicals but keeps getting capped by a real, unresolved geopolitical conflict — not a headline that will resolve by morning.

### Market Mood / Risk Routing
- Crypto mood:           mixed (bullish trend structure, improving breadth, but a real sustained macro/geopolitical risk-off overhang)
- Stocks mood:            closed (chop into the close, VIX 16.98); planning-only until tomorrow's pre-market
- Dominant narrative:    RWA/tokenization (ONDO/XLM, repeatedly profitable this week) remains the strongest catalyst-linked thesis; momentum-only cluster (RE/KITE/ZAMA/AKE/BANK) lacks catalyst backing
- Preferred side now:    longs (crypto, selective, wait for RE/KITE fills), wait-for-next-session (stocks)
- Best long candidate:   RE/USDT (see §8)
- Best short candidate:  RIF/USDT — squeeze risk still not cleared, 3rd+ cycle unresolved (see §8)
- Best catalyst-backed candidate: ONDO/USDT — thesis reinforced by repeated tp1/tp2 outcomes (see §8)
- What to avoid:         UNH (DOJ legal risk), MSFT (securities-fraud legal risk), BANK/USDT (thin-volume chase pattern + untracked-alert symbol), MIRA/USDT (report idea with no backing system signal — do not chase off report text alone)
- What would change the view: a confirmed de-escalation headline on Iran/Hormuz, TSLA's earnings result and reaction (pending), or the stocks drawdown guard lifting in tomorrow's pre-US-open review

## 7. Candidate Deep Dives

### 7.1 RE/USDT (crypto, long-watch, B-tier, intraday — score 65.1, waiting_for_entry)
- **Reacted already?** Yes — 24h return +29.88%, RS vs BTC +30.5% — the move has already happened; this is a pullback-entry plan, not a breakout chase.
- **Chasing?** No — the plan explicitly waits for price to retrace into the 0.4754-0.4857 zone; current price 0.4903 is just above the zone.
- **Actionable level:** fill inside 0.4754-0.4857; invalidation 1h close beyond 0.4628.
- **Mood alignment:** Consistent with "selective longs, prefer pullbacks on relative strength" — the desk's own recommended style for a bullish-trend/risk-on-technical regime.
- **Chase risk:** Low if the fill discipline is respected; high if entered at the current extended price.
- **Catalyst:** No fresh verified catalyst — momentum/RS-only setup, size accordingly (known failure mode: no-catalyst intraday in chop nets negative per the playbook's own 14d note, WR 23%/PF 0.70).
- **Legal/headline risk:** none flagged.

### 7.2 KITE/USDT (crypto, long-watch, B-tier, intraday — score 65.7, waiting_for_entry)
- Same structural profile as RE: standing limit order, not yet filled, entry 0.118921-0.119737, invalidation 0.117923.
- **Note:** a separate, older KITE/USDT signal (different signal_id) already sits at tp1_hit in the active-signals table — this is a distinct, fresh signal, not a duplicate.
- **Verdict:** watch for fill; do not manually pre-position ahead of the zone.

### 7.3 VANA/USDT (crypto, long, B-tier, intraday — score 66.1, ENTERED UNRESOLVED)
- Entry has been filled (zone was 1.2126-1.2205); position is open and unresolved as of this review — no TP/stop hit yet, expires 2026-07-23T17:54:10.
- **Status language:** ENTERED UNRESOLVED — not a missed entry, not yet a win/loss. Monitor into the next cycle.

### 7.4 MIRA/USDT (crypto, report idea only — score 66.7, NO matching system signal)
- The 22:04 intraday report's #1 Trade Idea, but `active-signals --asset-class crypto` shows no row for it — a report-text/system-signal mismatch.
- **Verdict:** treat as unconfirmed context only; do not act on the report's entry plan (pullback 0.0466-0.0485) as if it were a live tracked signal. Flagged in §14.

### 7.5 RIF/USDT (crypto, short-watch, C-tier — squeeze-capped)
- Unchanged for a 3rd+ consecutive cycle: 24h -27.2%(intraday)/-28.0%(scalp), negative external funding (-0.0052 mexc), crowding elevated — `thin_liquidity_short_squeeze_risk` cap still in force.
- **Actionable level:** wait for a failed reclaim of prior support plus visible OI unwind/funding normalization before treating as a clean short.
- **Legal/headline risk:** none flagged.

### 7.6 ONDO/USDT (crypto, catalyst-backed, RWA thesis)
- Scalp-mode leg `tp1_hit`; intraday-mode leg `tp2_hit` — this thesis keeps working, not just theoretical.
- **rwa_narrative basket** remains active <6h with XLM as secondary.
- **Actionable level (for adding, not initiating):** wait for a fresh pullback into the basket's support structure; do not chase the already-realized move.

### 7.7 UNH (stocks, avoid, C-tier demoted from B — score 75)
- **LEGAL/HEADLINE RISK** — live DOJ criminal+civil Medicare-billing investigation, tagged `legal_headline_risk: sec_doj`, unchanged across 5+ consecutive review cycles today.
- Hard AVOID / manual-review-only regardless of technical setup.

### 7.8 NEAR/USDT (crypto, short, integrity flag — entered-unresolved past window, carried forward)
- Active-signals shows this scalp-mode short at `tp1_hit` with `expires_at` = **2026-07-17T15:56:12**, now **5 days in the past** relative to this review, unchanged status since the last cycle's flag.
- **System-integrity issue:** unresolved for a 2nd consecutive review cycle — flagged for manual review, not treated as a live idea (§14).

## 8. Best Candidates Ranked

1. **RE/USDT (long-watch)** — trigger: fill inside 0.4754-0.4857, invalidation below 0.4628. The freshest genuinely current crypto long signal in the book.
2. **KITE/USDT (long-watch)** — trigger: fill inside 0.118921-0.119737, invalidation below 0.117923. Same standing-wait profile as RE.
3. **ONDO/USDT (catalyst-watch, add-only)** — trigger: fresh pullback into the rwa_narrative basket's support after the already-realized tp1/tp2 moves.
4. **RIF/USDT (short-watch)** — trigger: confirmed failed reclaim + OI unwind/funding normalization before shorting; still squeeze-prone for a 3rd+ cycle.
5. **VANA/USDT (manage, not a new entry)** — ENTERED UNRESOLVED; monitor toward TP1/invalidation 1.2030 into the next cycle.

## 9. Avoid / No Trade

This is a decision-window verdict only — it never means stopping the scanner or data collection, which continue overnight into the Asia session as normal.

- **UNH** — live DOJ Medicare-billing investigation; hard avoid regardless of score.
- **MSFT** — securities-fraud legal-headline flag; hard avoid.
- **BANK/USDT** — recurring thin-volume (0.02-0.05x) chase pattern on double-digit moves, and itself an untracked-alert symbol today; do not treat as a clean entry off report text.
- **MIRA/USDT** — report idea with no backing system signal; do not act on the report's entry plan as if it were live.
- **ADA/USDT, BNB/USDT** — active exploit_hack operator-review warning (Wanchain Cardano-BNB bridge exploit); avoid new exposure pending resolution.
- **Crypto shorts generally** — direction=short bucket is anecdotal but consistently negative this week (n=8); avoid new shorts without very strong confirmation.
- **All stocks intraday candidates** — market closed; the entire demoted shortlist (XOM/AMD/NVDA/XLE/AVGO/JPM/MSTR/META/PLTR/XLV/LLY/NFLX/AMZN) remains blocked by the drawdown guard or liquidity/sector/catalyst gates; nothing actionable until tomorrow's session.

## 10. Main Risks

- **Geopolitical/macro:** the Strait of Hormuz war is active and unresolved (truce broken, sea mines, shipping near-standstill) — oil stays elevated and the macro-risk score stays pinned at 100/100; this can flare further overnight with no warning.
- **TSLA earnings (pending):** call at 00:30 EEST, options market pricing an 8% post-earnings swing either way — outsized overnight volatility risk for anything correlated to mega-cap tech sentiment, even though TSLA itself is not a tracked crypto-desk position.
- **Untracked-alert defect (systemic, 5th cycle):** 9 Telegram alerts today, including the day's top-scoring symbol (EPIC), are not being captured by PF/winrate/avgR tracking — this both understates true system activity and represents a real operator-facing gap (alerts sent that don't get outcome-tracked).
- **Catalyst mapping weak (20.4%):** the catalyst layer is context-only this cycle, not a reliable final-decision input.
- **RE/KITE:** genuinely fresh but unconfirmed by any catalyst — pure momentum/RS setups with the playbook's own documented negative base rate in chop (WR 23%/PF 0.70 over 14d for no-catalyst intraday).

## 11. Action Plan — next 4 hours (overnight into Asia)

- Monitor RE/USDT and KITE/USDT for fills inside their stated entry zones; do not chase if price extends beyond ~2 ATR from the zone.
- Manage VANA/USDT toward TP1 (1.2126 zone entry) or invalidation (1.2030); no fresh action needed, just tracking.
- Watch for TSLA's earnings result and reaction after the 00:30 EEST call — planning context only, not a crypto-desk position; feed into tomorrow's pre-US-open review (16:20 EEST slot).
- Watch Iran/Hormuz headlines for any confirmed de-escalation — this is the single biggest lever on the macro-risk score and the crypto risk-on/risk-off routing.
- Do not initiate new RIF/USDT shorts until a failed-reclaim + funding-normalization signal appears.
- Scanning, tracking, and all monitors continue overnight into the Asia session — no pause, regardless of this review's caution stance.

## 12. Final Verdict per Mode

- **Crypto scalp:** caution / low-conviction data-collection mode only (PF 0.67 week, PF 0.14 over 14d per the report's own banner) — not for fresh entries.
- **Crypto intraday:** watch / selective longs — RE and KITE are the live waiting_for_entry triggers; VANA is an open position to manage.
- **Crypto swing:** stale (>14h) this cycle — carry-forward context only, no fresh verdict.
- **Stocks intraday:** no A/B actionable, market closed — wait for tomorrow's session; nothing to chase overnight.
- **Stocks swing/invest:** deprecated pipeline, stale 20 days — excluded.

## 13. Sources

- [Bitcoin and ethereum prices today, Wednesday, July 22, 2026: Both cryptos open higher before losing steam](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-wednesday-july-22-2026-both-cryptos-open-higher-before-losing-steam-153454067.html) — Yahoo Finance, 2026-07-22, verification: primary_source (WebFetch-verified).
- [Stock market today: Dow, S&P 500, Nasdaq slip as oil prices rise, Alphabet and Tesla earnings loom](https://finance.yahoo.com/markets/live/stock-market-today-wednesday-july-22-dow-sp-500-nasdaq-alphabet-tesla-earnings-083644887.html) — Yahoo Finance, 2026-07-22, verification: single_source.
- [googl earnings alphabet gains after beating q2 estimates](https://www.tipranks.com/news/googl-earnings-alphabet-gains-after-beating-q2-estimates) — TipRanks, 2026-07-22, verification: single_source.
- [Alphabet Reports Q2 Results After the Bell Today. The Number That Decides the Stock Isn't Revenue or Earnings -- It's Capex.](https://www.fool.com/investing/2026/07/22/alphabet-reports-q2-results-after-the-bell-today-t/) — The Motley Fool, 2026-07-22, verification: single_source.
- [Tesla (TSLA) Q2 2026 earnings report](https://www.cnbc.com/2026/07/22/tesla-tsla-q2-2026-earnings-report.html) — CNBC, 2026-07-22, verification: single_source (results not yet confirmed public as of this review; call at 00:30 EEST).
- [2026 Strait of Hormuz crisis](https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis) — Wikipedia, date unavailable (continuously updated), verification: single_source.
- [US-Iran war leaves shipping at near-standstill in Hormuz again](https://news.un.org/en/story/2026/07/1167905) — UN News, 2026-07, verification: primary_source (UN agency reporting).
- Internal: `data/reports/intraday/2026-07-22_19-04_intraday_report.md`, `data/reports/scalp/2026-07-22_17-08_scalp_report.md`, `data/reports/stocks/intraday/2026-07-22_19-56_stocks_intraday_report.md`, `data/catalysts/2026-07-22/catalyst_events.jsonl`.

## 14. Fix Requests / TODO

### TODO-untracked-alert-recurrence-5th-cycle-widened
- **issue:** Watchlist-alert/signal-reuse defect recurred for a **5th consecutive review cycle** today and **widened again**: ERA/USDT ×3 (08:45, 09:26, 11:48 UTC), EPIC/USDT ×3 (12:35, 14:34, **19:04:09 new** UTC), OPN/USDT ×1 (17:54:11 UTC), BANK/USDT ×1 (18:05:30 UTC), and **new this cycle** AKE/USDT ×1 (19:04:13 UTC) — 9 raw Telegram alerts total today with no backing `proposed_signal`. Notably EPIC/USDT is today's single highest-scoring symbol (91.6 in both scalp and intraday reports) and still cannot convert into a tracked signal — this rules out a low-quality/low-score-symbol explanation and points at a systemic path issue. Same defect class as the confirmed 2026-07-17 ALLO/BANK case ([[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]], already high priority).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-22` → 9 untracked rows; cross-checked against `python -m src.cli active-signals --asset-class crypto` (22 rows, zero ERA/EPIC/OPN/BANK/AKE-matching entries).
- **suggested manual fix:** Unchanged root-cause direction, now more urgent — a top-scoring symbol (EPIC, score 91.6) still hitting this defect strongly suggests the watchlist-alert re-fire path itself is broken (stale/closed signal_id reuse), not a score or symbol-quality gate. Prioritize a direct code-path trace of the watchlist-alert → proposed_signal linkage next manual session.
- **priority:** high (escalated — 5th cycle, widening symbol set, now includes today's top-scoring symbol)
- **first observed:** 2026-07-17 (this recurrence: 2026-07-22 23:32 EEST, 5th consecutive cycle today)

### TODO-mira-report-idea-no-system-signal
- **issue:** The 22:04 EEST intraday report's #1 Trade Idea (MIRA/USDT, score 66.7, `status: actionable`) has no corresponding row in `active-signals --asset-class crypto`. Cannot determine from available read-only data whether this is a timing artifact (signal not yet registered), a scoring-vs-registration threshold mismatch, or a pipeline gap between report generation and signal persistence.
- **evidence:** `data/reports/intraday/2026-07-22_19-04_intraday_report.md` §6 Trade Idea #1 (LONG MIRA/USDT); `python -m src.cli active-signals --asset-class crypto` (22 rows, no MIRA/USDT row).
- **suggested manual fix:** Manually inspect whether MIRA/USDT was evaluated for signal registration this cycle and, if so, why it didn't persist as a `proposed_signal` despite being the report's top idea.
- **priority:** medium
- **first observed:** 2026-07-22 23:32 EEST

### TODO-near-usdt-past-expiry-unresolved-signal (carried forward, unchanged)
- **issue:** `active-signals --asset-class crypto` shows a NEAR/USDT short (scalp, sig_b16bb9e54598333a) at status `tp1_hit` with `expires_at` = 2026-07-17T15:56:12 — 5 days in the past relative to this review, unchanged since the 21:39 review's flag.
- **evidence:** `python -m src.cli active-signals --asset-class crypto`, row `sig_b16bb9e54598333a | NEAR/USDT | crypto | B | scalp | short | 66.1 | tp1_hit | ... | 2026-07-17T15:56:12`.
- **suggested manual fix:** Unchanged — manually inspect this signal_id to confirm whether it is legitimately still open or a stale row the active-signals query should be excluding.
- **priority:** medium
- **first observed:** 2026-07-22 21:39 EEST

### TODO-catalyst-mapping-persistent-weak (carried forward, unchanged)
- **issue:** Catalyst symbol-mapping coverage has been below the 50% usability bar for 5+ consecutive review cycles (17.2%→18.9%→19.7%→20.1%→20.4% across today's cycles).
- **evidence:** `data/catalysts/2026-07-22/catalyst_events.jsonl` — 4000 rows, 814 mapped (20.4%), 3186 unmapped (79.6%); majority of unmapped items are exchange operational notices rather than trade-relevant news.
- **suggested manual fix:** Unchanged from prior reviews — improve the symbol resolver in the catalyst layer, or bucket operational-notice-only sources separately so the mapped% metric isn't diluted by noise.
- **priority:** medium
- **first observed:** carried forward from prior reviews (multi-day pattern)

### TODO-ake-exchange-listing-data-conflict (carried forward, now more relevant — AKE re-entered top-N and untracked alerts)
- **issue:** Internal reports tag AKE/USDT as "MEXC-only listing (exchange confirmation missing)" and reject/cap it to C-tier on that basis; external sources previously described AKE ("Akedo") as heavily Binance-listed. This cycle AKE rolled back into the top-N (score 88.1, #4 strongest symbol) AND fired its first untracked alert — the exchange-confirmation gap is now directly relevant to a live top-scoring symbol.
- **evidence:** `data/reports/intraday/2026-07-22_19-04_intraday_report.md` §2 (AKE/USDT score 88.1); `detect_untracked_legacy_alerts` (AKE/USDT ×1, 19:04:13 UTC). See the 18:39 review's TODO for full external-source detail.
- **suggested manual fix:** Unchanged — manually check whether the Binance exchange-universe fetch for AKE/USDT is failing silently, and re-run the exchange-confirmation classifier once resolved.
- **priority:** medium
- **first observed:** 2026-07-22 18:39 EEST
