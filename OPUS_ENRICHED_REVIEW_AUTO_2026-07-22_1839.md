# Opus Enriched Review — US open reaction review — Auto Cycle 18:30 EEST

## 1. Executive Summary

Slot: **US open reaction review** (18:39 EEST / 15:39 UTC / ~11:39 ET, ~2h10m into the US cash session). Advisory only — no auto-trade, no scoring/strategy changes. Crypto regime is still "bullish trend/risk-on" on trend structure (BTC/ETH uptrend, 63–65% breadth>EMA20) but macro risk stays pinned at **100/100** on the ongoing Iran-US/Hormuz conflict (Brent >$95, externally confirmed BTC ~$65.9K with Fear&Greed=33/fear). **No A-tier setups anywhere** (crypto or stocks); crypto's own best-current-idea per the 14:34 intraday report is a modest B-tier long, ZAMA/USDT. The **known untracked-alert defect recurred again today** — ERA/USDT (×3) and EPIC/USDT (×2), 5 raw Telegram alerts with no backing `proposed_signal` (same class as the 2026-07-17 and 16:20-today recurrences; escalating in §14). New this cycle: external verification found the internal "MEXC-only, exchange confirmation missing" tag on **AKE/USDT is likely wrong** — AKE ("Akedo") is heavily Binance-listed ($303M vol) per public sources, a possible symbol-resolution bug (§14). Stocks remain **chop, VIX 16.90**, zero A/B actionable after the open; the same pre-open demoted shortlist (XOM/NVDA/XLE/COIN/AMD/AVGO) is still blocked by the rolling paper-R drawdown guard — nothing chased, nothing confirmed. GOOGL/NOW/TSLA report earnings today — still do-not-chase. UNH and MSFT remain legal/headline-risk AVOID (DOJ Medicare probe / securities-fraud flag). The Iran-Amazon-Bahrain claim from the prior cycle is **still unconfirmed** by AWS/US officials — but AWS's own status dashboard shows no service-level change, which meaningfully lowers real operational risk even though the headline risk stays open. Catalyst mapping is weak again (19.7% mapped).

## 2. Data Used

- Crypto reports: scalp (2026-07-22 17:28 EEST gen / 14:15 UTC freshness), intraday (17:34 EEST / 14:15 UTC — fresh, ~4h20m old), swing (04:16 EEST / 01:15 UTC — **stale, ~17h20m old, >14h threshold; used for narrative cross-check only, excluded from fresh-entry timing**).
- Stocks intraday report (2026-07-22 18:29 EEST gen / 15:29 UTC freshness — **fresh**, market open, ~2h into RTH). Stocks swing/invest reports stale since 2026-07-02 (20 days) — excluded per known deprecation of the old swing/invest pipeline ([[project_crypto_ai_desk_stocks_position_framework]]).
- `data/catalysts/2026-07-22/catalyst_events.jsonl` (3000 rows in file, 592 mapped/19.7%) and `narrative_baskets.jsonl` (6 baskets: perps_dex/HYPE, delisting_thin_liquidity/BTC, binance_ecosystem_teaser/BNB, ai_narrative/NEAR+RENDER+TAO+FET, rwa_narrative/ONDO+XLM, momentum_breakout/TLM).
- `data/processed/llm_analysis_packet.md` (17:37 EEST), `llm_stocks_packet.md` (17:52 EEST).
- CLI: `active-signals --asset-class crypto` (20 rows), `active-signals --asset-class stocks` (50 rows), `signal-stats --asset-class crypto` (headline PF 1.98/totalR +43.21/n=173), `signal-stats --asset-class stocks` (A/B headline sample=0; C-tier PF 0.95/totalR -0.5), `detect_untracked_legacy_alerts --since 2026-07-22` (**5 untracked**: ERA×3, EPIC×2).
- External web research: 3 WebSearch queries (BTC price/macro tape, AKE/Akedo token verification, Iran-Amazon-Bahrain claim follow-up) + 1 WebFetch (CoinDesk daybook, verified opened; a BeInCrypto URL returned 403 and was not used). No "external web research unavailable" fallback needed.
- Previous review for diff: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-22_1620.md` (pre-US-open decision review, 16:20 EEST).

## 3. Scheduler / Data Freshness

- Scheduler folder: `data/scheduled_runs/2026-07-21_default_schedule/` (rolls over by creation date, currently holding today's cycles too — **fresh**).
- `scheduler.log` mtime: 18:00 EEST (~39min old at review time — well under 3h defer threshold).
- Latest cycle summary: `cycle_08_17-20_summary.md`, mtime 17:20 EEST (~1h19m old — fresh).
- Monitors alive and current: `crypto_monitor` (log 18:41 EEST), `derivatives_monitor` (18:46 EEST), `stocks_monitor` (18:46 EEST, live during RTH), `pending_monitor` (17:21 EEST), `mexc_canary_monitor` (17:21 EEST).
- Transient local resource contention observed while running CLI commands (OpenBLAS memory-allocation errors, shell fork failures) during this review — resolved on retry with wider terminal width; did not block data collection, noted for awareness only (§14).
- No defer triggered.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-07-22 18:39 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log/cycle_08 mtime 17:20 EEST, ~1h19m old — fresh", "crypto swing report ~17h20m old — stale (>14h), used for narrative cross-check only", "stocks swing/invest stale since 2026-07-02, known-deprecated pipeline", "transient OpenBLAS/fork resource contention during CLI runs, resolved on retry"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.65,
      "reason_codes": ["mixed", "risk_off", "chop", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH labelled uptrend, 63-65% breadth>EMA20, macro risk 100/100 on Iran/oil escalation (externally confirmed: Brent >$95, BTC ~$65.9K, Fear&Greed=33)", "stocks regime=chop, neutral bias, VIX 16.90, 0/4 indices trending up, breadth20=75%/breadth50=100% (index-level noise, not a clean trend)"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "no_catalyst", "narrative_supported"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst mapping 19.7% mapped / 80.3% unmapped today (3000 rows in jsonl)", "ZAMA/EPIC/AKE B-tier ideas all explicitly 'no fresh verified catalyst detected'", "rwa_narrative (ONDO/XLM, <6h) and momentum_breakout (TLM, <1h) baskets active and internally consistent across scalp/intraday/swing reports"] },
    { "agent": "derivatives_squeeze", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["squeeze_risk", "data_unavailable", "funding_extreme"], "data_missing": ["OI history for MEXC-fallback symbols (n/a% OI change on most top movers)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["RIF/USDT: negative funding (-0.02) + OI +125.5% = fresh shorts pressing, squeeze risk if price reclaims — capped to C (thin_liquidity_short_squeeze_risk)", "TLM/USDT: negative funding (-0.0074), crowding elevated externally (bybit/mexc)", "ZAMA/EPIC/AKE: funding neutral, crowding normal — no squeeze signal on the long side"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZAMA/USDT: current price 0.0430 sits just above the 0.0422-0.0427 pullback entry zone — near-trigger, not yet chasing", "BANK/USDT: +22.3% 24h on only 0.19x volume — thin, extended, classic chase-risk, RR unattractive at market", "AKE/USDT: +16.7% 24h / reportedly +120-770% 7d depending on source — extended, plus exchange-listing data conflict lowers entry confidence"] },
    { "agent": "execution_lifecycle", "verdict": "needs_review", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["20 active crypto signals: 3 triggered, 9 tp1_hit, 8 tp2_hit — 0 waiting_for_entry (AKE's prior waiting_for_entry slot from 16:20 has since resolved/rolled off)", "50 active stocks signals: 2 waiting_for_entry (DIA, AAPL shorts), 23 triggered, 13 tp1_hit, 12 tp2_hit — all C-tier legacy/research grade, none current A/B", "5 untracked legacy alerts (ERA×3, EPIC×2) with no proposed_signal — needs_review, third consecutive cycle showing this defect"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review"], "data_missing": ["confirmed AWS service-status impact from the Bahrain claim (checked: dashboard shows no change)"],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: live DOJ criminal+civil Medicare-billing investigation, legal_headline_risk gate stands (C-tier, sec_doj)", "MSFT: securities_fraud legal_headline_risk gate, demoted B→C", "GOOGL/NOW/TSLA earnings today — do_not_chase_warning active", "AMZN Bahrain claim: still unconfirmed by AWS/US/Bahrain officials as of this review, but AWS status dashboard shows no service-level change — real operational impact appears low despite open headline risk"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week: intraday PF 2.08/n81, swing PF 2.96/n50 (both healthy actionable-primary), scalp PF 0.71/n42 negative (known-bad, kill-switched already)", "crypto headline (A/B): PF 1.98, totalR +43.2, winrate 33.5%, n=173 reliable", "stocks: A/B headline sample=0 this week (nothing actionable fired); C-tier PF 0.95/totalR -0.5, roughly flat/slightly negative"] },
    { "agent": "head_trader", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["wait_for_trigger", "longs_preferred"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "longs",
    "best_long_candidate":     { "symbol": "ZAMA/USDT", "trigger": "1h close/hold inside 0.0422-0.0427 pullback zone (current 0.0430, just above zone) with volume pickup; invalidation 1h close below 0.0415", "reason": "the intraday report's own top idea (score 71.7), cross-confirmed as strongest symbol across scalp/intraday/swing reports today; no fresh catalyst so treat as momentum-only, size small" },
    "best_short_candidate":    { "symbol": "RIF/USDT", "trigger": "wait for a failed reclaim of prior support (~-21% 24h zone) and confirmed OI unwind before shorting; do not short into the squeeze — RIF is flagged thin_liquidity_short_squeeze_risk with OI +125.5% and negative funding, a classic short-squeeze setup, not a clean short yet", "reason": "highest raw weak_rs_short score (80) among today's laggards, but squeeze risk must clear first per the derivatives_squeeze agent" },
    "best_catalyst_candidate": { "symbol": "ONDO/USDT", "trigger": "confirm hold above the rwa_narrative basket's implied support after any pullback; basket still primary/active <6h with XLM as secondary", "reason": "multi-week RWA/tokenization institutional thesis, consistently the top or near-top symbol in both intraday and swing reports across the last several cycles" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "score 76 (was B) but carries a live DOJ criminal+civil Medicare-billing investigation — legal/headline risk overrides score; manual review required, not a clean long even mid-session" },
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
| market_regime | caution | 0.65 | mixed, risk_off, chop, longs_preferred | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.50 | squeeze_risk, data_unavailable, funding_extreme | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, clean_retest | advisory_only |
| execution_lifecycle | needs_review | 0.75 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.60 | legal_risk, headline_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.70 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader (synthesis) | caution | 0.60 | wait_for_trigger, longs_preferred | advisory_only |

## 4. What Changed vs Previous Review

Previous review (16:20 EEST, pre-US-open decision review) named **AKE/USDT** best long (waiting_for_entry, zone 0.001713-0.001761), **AVGO** best short-watch (blocked by drawdown guard), **COIN** best catalyst-backed candidate, **UNH** avoid, and reported **4** untracked legacy alerts (ERA×3, EPIC×1).

- **AKE/USDT**: no longer waiting_for_entry — that signal slot has rolled off the active-signals list entirely (either triggered-and-closed or expired since 16:20; not visible in the current 20-row active book). New this cycle: external verification found the internal "MEXC-only" exchange-confirmation tag likely **wrong** — see §14 TODO.
- **AVGO**: unchanged. Still on the stocks demoted-C list, still blocked by `stocks_intraday_long_guard` (rolling paper-R drawdown guard). No confirmation or invalidation since pre-open — genuinely still "wait."
- **COIN**: unchanged. Still demoted A→C by the same drawdown guard; the Clarity Act / regulatory-positive catalyst from 16:20 has not produced a fresh actionable signal post-open.
- **Untracked alerts: escalated further.** 16:20 review found 4 (ERA×3, EPIC×1); this review finds **5** (ERA×3, EPIC×2) — a new EPIC alert fired at 14:34:42 UTC with no backing signal. Third consecutive cycle with this defect (§14).
- **UNH**: unchanged, still legal/headline-risk AVOID (DOJ investigation).
- **AMZN Bahrain claim**: followed up per the 16:20 TODO — still unconfirmed by AWS/US/Bahrain officials, but AWS's own status dashboard shows no service-level change. Downgrading from "urgent open item" to "watch, low confirmed operational impact" (§14 TODO updated, not closed).
- Catalyst mapping: 19.7% mapped now vs 18.9% at 16:20 — marginal, still far below the 50% usability bar (persistent multi-day pattern, carried forward in §14).
- New top movers this cycle not present at 16:20: EPIC/USDT and AKE/USDT both climbed into the B-tier top-3 (scores 66.1 each), alongside ZAMA/USDT which is now the desk's own stated best idea.

## 5. Catalyst Coverage

- Total catalyst events in `catalyst_events.jsonl`: **3000** rows (rolling file, not strictly "today-only" — report itself states 1018 unique events today).
- Mapped (symbol present): **592** (19.7%). Unmapped: **2408** (80.3%).
- Narrative baskets: **6** (`perps_dex_narrative` primary HYPE <6h; `delisting_thin_liquidity` primary BTC <6h — avoid-low-liquidity playbook, not a BTC trade signal; `binance_ecosystem_teaser` primary BNB <6h; `ai_narrative` primary NEAR/RENDER/TAO/FET <6h; `rwa_narrative` primary ONDO/XLM <6h; `momentum_breakout` primary TLM <1h).
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (4th+ consecutive cycle >50% unmapped — see TODO in §14.) Top unmapped-type headlines are largely exchange operational notices (leverage adjustments, thin-pair delistings), not trade-relevant news.

## 6. Market Landscape

Crypto trend structure remains bullish (BTC/ETH uptrend, altcoin breadth 63-65% above EMA20) but the macro backdrop is a genuine, externally-confirmed risk-off headwind: Iran-US/Hormuz conflict ongoing, Brent >$95, and BTC trading around $65.9K with a Fear&Greed reading of 33 (fear zone) — a market that is technically "risk-on" by trend labels but psychologically cautious. Stocks are in a chop regime (VIX 16.90, 0/4 major indices trending), with energy and healthcare as the only sectors showing real relative strength (XLE +6.6% RS/20d, XLV +3.1% RS/20d) and semiconductors/technology lagging (SMH -7.2% RS/20d). Two hours into the US cash session, nothing from the pre-open demoted shortlist has cleared its gates — this is a session of managing existing positions and watching triggers, not chasing new ones.

### Market Mood / Risk Routing
- Crypto mood:           mixed (bullish trend structure, risk-off macro headwind)
- Stocks mood:           chop
- Dominant narrative:    RWA/tokenization (ONDO/XLM) and AI-sector rotation (NEAR/RENDER/TAO/FET) both fresh <6h; momentum-only cluster (ZAMA/EPIC/AKE/TLM) lacks catalyst backing
- Preferred side now:    longs (crypto, selective pullback-only), wait-for-trigger (stocks)
- Best long candidate:   ZAMA/USDT (see §8)
- Best short candidate:  RIF/USDT — squeeze risk must clear first, not a chase (see §8)
- Best catalyst-backed candidate: ONDO/USDT (see §8)
- What to avoid:         UNH (DOJ legal risk), BANK/USDT (thin-volume chase, +22% on 0.19x volume), AKE/USDT until the exchange-listing data conflict is resolved manually
- What would change the view: a confirmed de-escalation headline on Iran/Hormuz (would lift macro risk score off 100/100), or a clean breakout-with-volume on any of today's B-tier crypto ideas

## 7. Candidate Deep Dives

### 7.1 ZAMA/USDT (crypto, long, B-tier, intraday — score 71.7)
- **Reacted already?** Partially — 24h +9.8%, 7d +27.3%, currently trading 0.0430, just above the 0.0422-0.0427 planned pullback zone.
- **Chasing?** Not yet — price sits close to, not far beyond, the entry zone.
- **Retest/pullback structure?** Yes, this is explicitly a pullback-continuation setup; RR to TP1 1.84R.
- **Overextended (>2 ATR from EMA20)?** No red flag raised for ZAMA specifically.
- **Late if entered now?** Borderline — entering at 0.0430 (above the top of the stated 0.0422-0.0427 zone) would be slightly early/at-the-edge; better to wait for a print back inside the zone.
- **Actionable level:** 1h close/hold inside 0.0422-0.0427; invalidation 1h close below 0.0415.
- **Mood alignment:** Consistent with "selective longs, prefer pullbacks on RS" market style.
- **Long/short/wait:** Long, wait-for-pullback.
- **Now vs after confirmation:** After a retest print, not at market.
- **Invalidates if:** 1h close below 0.0415, or BTC breaks its local support (regime thesis fails).
- **Chase risk:** Low-moderate.
- **Catalyst:** None verified — pure momentum/RS play (14d no-catalyst intraday cut: WR 23%/PF 0.70, a known-weak playbook bucket). Size accordingly.
- Chart/manual TradingView check: unavailable (no chart MCP loaded this run); relying only on local OHLCV/ATR/EMA fields above.

### 7.2 EPIC/USDT (crypto, long, B-tier, intraday — score 66.1) — integrity flag
- Same momentum/no-catalyst profile as ZAMA (24h +13.5%, RS vs BTC +15.3%, volume only 0.36x — weaker volume confirmation than ZAMA).
- **System-integrity issue:** EPIC/USDT fired 2 raw Telegram watchlist alerts today (12:35 and 14:34 UTC) with **no backing `proposed_signal`** — confirmed via `detect_untracked_legacy_alerts` cross-checked against the active-signals table (zero EPIC/USDT rows). This means any operator who saw the Telegram alert and acted on it would have no signal_id to track PF/R against, and the desk's own reported performance stats will not reflect that action.
- **Verdict:** Treat any Telegram EPIC/USDT alert from today with reduced trust until the tracking defect is fixed manually (§14) — this is a data-integrity problem, not a trade-quality problem, but it changes how much weight to give the "actionable" label on this symbol specifically.
- Actionable level (if trading the report idea rather than the raw alert): pullback into 0.5830-0.5980, invalidation 1h close below 0.5646.

### 7.3 AKE/USDT (crypto, long, B-tier, intraday — score 66.1) — data-quality flag
- Internal report tags AKE/USDT "MEXC-only listing (exchange confirmation missing)" and caps it to C-tier/rejected on that basis.
- **External verification contradicts this**: public sources (CoinGecko/CoinMarketCap/Gate/Phemex) describe AKE ("Akedo") as a real, actively-traded token concentrated on **Binance** (~$303M reported volume), with LBank and Bybit as secondary venues — not MEXC-only. This looks like a symbol-resolution or exchange-universe data bug on the internal side, not a token-quality problem (see §14).
- Separately, external sources show early-contributor/investor token-supply cliffs ending Q1 2026 that could roughly double circulating supply within 12 months — a real medium-term dilution risk independent of the exchange-listing question.
- **Verdict:** Do not treat as tradeable off the current internal tier framing until the exchange-listing conflict is resolved manually. If the Binance listing is confirmed correct, this symbol's whole risk profile (liquidity, confirmation quality) needs re-scoring — that is a manual/code task, not something this review can or should change.

### 7.4 AVGO (stocks, short-watch, C-tier demoted from B — score 90.7)
- Unchanged since the 16:20 pre-open review: still on the demoted list, still blocked by `stocks_intraday_long_guard` (rolling paper-R drawdown guard blocks new A/B of both directions while the cohort is weak).
- Sector context: semiconductors remain the weakest sector today (SMH RS vs SPY 20d -7.2%), which supports a short thesis on rallies, not on breakdowns already in progress.
- **Actionable level:** wait for the drawdown guard to lift, or an explicit operator manual-review sign-off, then confirm with a failed bounce/rejection at resistance — not a chase of the existing move.
- **Legal/headline risk:** none currently flagged for AVGO.

### 7.5 UNH (stocks, avoid, C-tier demoted from B — score 75.92)
- **LEGAL/HEADLINE RISK** — live DOJ criminal+civil Medicare-billing investigation, tagged `legal_headline_risk: sec_doj` in today's 15:30 EEST stocks intraday report, unchanged from the 16:20 review.
- Score alone (76, medium confidence) would otherwise be watchlist-adjacent, but the legal flag makes this a hard AVOID / manual-review-only candidate regardless of technical setup.
- Source: internal production risk-warning tag, consistent across at least the last 3 review cycles today.

## 8. Best Candidates Ranked

1. **ZAMA/USDT (long-watch)** — trigger: 1h hold inside 0.0422-0.0427, invalidation below 0.0415. Cleanest, most cross-confirmed idea in the crypto book right now; no catalyst, so treat as a small-size momentum trade only.
2. **ONDO/USDT (catalyst-watch)** — trigger: hold/retest of the rwa_narrative basket's pullback zone; multi-week institutional RWA thesis remains intact and fresh.
3. **RIF/USDT (short-watch)** — trigger: confirmed failed reclaim + OI unwind before shorting; currently squeeze-prone, not a clean short yet.
4. EPIC/USDT and AKE/USDT — both watch-only pending resolution of their respective integrity/data-quality flags (§7.2, §7.3); do not treat Telegram alerts on these two as fully trustworthy today.
5. AVGO (stocks short-watch, blocked by guard) and UNH (stocks avoid) — unchanged carry-forwards from the pre-open review, confirming nothing has moved on either since the US open.

## 9. Avoid / No Trade

This is a decision-window call only — scanning, tracking, and data collection all continue regardless (see ALWAYS-SCAN rule; never a system-stop instruction).

- **UNH** — DOJ legal risk overrides score; manual review only.
- **MSFT** — securities-fraud legal risk flag; manual review only.
- **BANK/USDT** — +22.3% 24h on just 0.19x volume; thin, extended, classic chase-risk with no catalyst.
- **AKE/USDT** — pending resolution of the exchange-listing data conflict (§7.3); do not size this as if it were a confirmed MEXC-only speculative name.
- **GOOGL, NOW, TSLA** — earnings today; do-not-chase into the print regardless of technical setup quality.
- **Crypto scalp mode generally** — kill-switched (mode off, any hour/day) and structurally negative (PF 0.71, -3.1R over 14d) even before the switch; not a source of new ideas.

## 10. Main Risks

- **Macro/geopolitical:** Iran-US/Hormuz conflict ongoing, oil >$95, macro risk score pinned at 100/100 for multiple consecutive cycles — a genuine, externally-confirmed risk-off overhang on both crypto and equities, not a stale/noise reading.
- **Data-integrity:** the untracked-alert defect (ERA/EPIC) is now a 3rd-consecutive-cycle recurrence; any Telegram-driven manual action on these symbols today would be invisible to the desk's own performance tracking.
- **Exchange-listing data quality:** the AKE/USDT MEXC-only tag conflicts with external sources; if this is a systemic symbol-resolution bug it could be misclassifying other tokens too (worth a broader manual audit, §14).
- **Legal/headline:** UNH (DOJ) and MSFT (securities fraud) both carry live, unresolved legal risk; do not treat either as a clean setup even if the technical score looks attractive.
- **Earnings:** GOOGL, NOW, TSLA report today; LMT tomorrow — gap risk on any of these names into/after the print.
- **Chase risk:** BANK/USDT and, pending the listing question, AKE/USDT are both extended moves on thin confirmed volume.

## 11. Action Plan — next 4 hours

- Watch ZAMA/USDT for a clean retest of 0.0422-0.0427 before considering size; do not chase above the zone.
- Watch RIF/USDT for signs the short squeeze is exhausting (funding normalizing, OI rolling over) before treating the short as clean.
- Monitor ONDO/USDT and the rwa_narrative basket for any fresh catalyst refresh (currently <6h, will start aging into "stale" territory by the next cycle).
- Re-check AVGO and the broader stocks demoted-C list post-3pm ET for any drawdown-guard resolution or fresh operator sign-off.
- Flag the AKE/USDT exchange-listing conflict to a human-driven session for manual investigation (§14) — do not act on AKE size decisions based on the current internal tier framing until resolved.
- Continue watching for GOOGL/NOW/TSLA earnings reactions after today's close/tomorrow's pre-market — do not pre-position into the print.

## 12. Final Verdict per Mode

- **Crypto scalp:** No trade — kill-switched, structurally negative even pre-switch.
- **Crypto intraday:** Watch-only. Best idea ZAMA/USDT on a pullback; EPIC/AKE flagged for integrity/data issues; no A-tier.
- **Crypto swing:** Stale report (17h old) — treat existing OPN/ONDO/EPIC swing positions as carry-forward context only, no fresh entries off this data.
- **Stocks intraday:** No trade — chop regime, 0 actionable A/B, same demoted shortlist unchanged since pre-open.
- **Stocks swing/invest:** Data stale since 2026-07-02 (pipeline deprecated) — no view rendered.
- **System-wide:** Scanning, tracking, and monitors all continue normally; this is a "manage existing, watch triggers" window, not a stop-trading instruction.

## 13. Sources

- [Bitcoin price today: recovering, but still $8,000 from the 200-day](https://cryptonews.net/news/bitcoin/33185465/) — BTC ~$65,901.68, Fear&Greed=33, 2026-07-22.
- [Crypto Market Slips 1.24% as US Strikes on Iran Lift Oil](https://finance.yahoo.com/markets/crypto/articles/crypto-market-slips-1-24-015817549.html) — Iran/oil impact on crypto, July 2026.
- [U.S.-Iran escalation weighs on bitcoin (BTC) price, stocks as oil climbs: Crypto Daily](https://www.coindesk.com/daybook-us/2026/07/14/u-s-iran-escalation-weighs-on-bitcoin-stocks-as-oil-climbs) — fetched directly; Hormuz conflict background, Brent/BTC levels, Fed rate-hike linkage, 2026-07-14.
- [Latest AKEDO News (AKE)](https://coinmarketcap.com/cmc-ai/akedo/latest-updates/) and [AKEDO price/volume context](https://www.coingecko.com/en/coins/akedo) — AKE exchange/volume verification contradicting internal MEXC-only tag.
- [Amazon data center in Bahrain struck and destroyed by Iranian cruise missiles, state media claims](https://www.tomshardware.com/tech-industry/data-centers/amazon-data-center-in-bahrain-struck-and-destroyed-by-iranian-cruise-missiles-state-media-claims-attacks-launched-against-aws-site-in-response-to-alleged-us-strikes-on-an-under-construction-nuclear-plant) — claim still unconfirmed by AWS, no service-status-page change, 2026-07-21/22.

## 14. Fix Requests / TODO

### TODO-untracked-alert-recurrence-3rd-cycle
- **issue:** Watchlist-alert/signal-reuse defect recurred for a 3rd consecutive review cycle today — ERA/USDT fired 3 raw Telegram watchlist alerts (08:45, 09:26, 11:48 UTC) and EPIC/USDT fired 2 (12:35, 14:34 UTC), none with a backing `proposed_signal`. Same defect class as the confirmed 2026-07-17 ALLO/BANK case ([[project_crypto_ai_desk_watchlist_alert_signal_reuse_bug]], already raised to high priority).
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-22` → 5 untracked rows; cross-checked against `python -m src.cli active-signals --asset-class crypto` (20 rows, zero ERA/EPIC entries).
- **suggested manual fix:** Same root-cause investigation as the existing high-priority TODO — confirm whether this is the stale-signal_id-reuse bug already raised 2026-07-17, or a distinct code path for symbols not currently tracked in the DB (ERA/USDT does not appear in any report's top-N or watchlist tables today, only in the untracked-alert detector, which suggests a separate/discovery-path alert source).
- **priority:** high
- **first observed:** 2026-07-17 (this recurrence: 2026-07-22 18:39 EEST, 3rd consecutive cycle today)

### TODO-ake-exchange-listing-data-conflict
- **issue:** Internal reports tag AKE/USDT as "MEXC-only listing (exchange confirmation missing)" and reject/cap it to C-tier on that basis. External sources (CoinGecko, CoinMarketCap, Gate, Phemex) describe AKE ("Akedo") as heavily Binance-listed (~$303M reported volume), with LBank and Bybit as secondary venues — not MEXC-only. This looks like either a symbol-resolution collision (a different AKE ticker) or a stale/incomplete exchange-universe fetch for this symbol.
- **evidence:** scalp report `data/reports/scalp/2026-07-22_14-28_scalp_report.md` §7c "AKE/USDT [rejected]: exchanges=['mexc']..."; external WebSearch "AKE token crypto news July 2026" returning CoinGecko/CoinMarketCap/Gate pages describing Binance as the dominant venue.
- **suggested manual fix:** Manually check whether `src/` exchange-universe fetch for AKE/USDT on Binance is failing silently (e.g., delisted-then-relisted, rate-limited, or a ticker mismatch), and re-run the exchange-confirmation classifier once resolved. Worth spot-checking a few other MEXC-only-tagged symbols for the same issue given this was found by chance.
- **priority:** medium
- **first observed:** 2026-07-22 18:39 EEST

### TODO-catalyst-mapping-persistent-weak
- **issue:** Catalyst symbol-mapping coverage has been below the 50% usability bar for 5+ consecutive review cycles (17.2%→18.9%→19.7% across today's cycles).
- **evidence:** `data/catalysts/2026-07-22/catalyst_events.jsonl` — 3000 rows, 592 mapped (19.7%), 2408 unmapped (80.3%); majority of unmapped items are exchange operational notices (leverage adjustments, thin-pair delisting notices) rather than trade-relevant news.
- **suggested manual fix:** Unchanged from prior reviews — improve the symbol resolver in the catalyst layer, or bucket operational-notice-only sources separately so the mapped% metric isn't diluted by noise.
- **priority:** medium
- **first observed:** carried forward from prior reviews (multi-day pattern)

### TODO-amzn-bahrain-claim-status-update (informational, not new)
- **issue:** Follow-up on the 16:20-review TODO — the Iran-IRGC claim of a cruise-missile strike on AWS/Amazon's Bahrain data infrastructure remains unconfirmed by AWS, Bahrain, or US officials as of this review. New information: AWS's own public status dashboard shows **no service-level change**, which meaningfully lowers the probability of real operational impact even though the headline-risk/claim itself is still open.
- **evidence:** WebSearch "Iran Amazon AWS Bahrain data center attack confirmed OR retracted" — CNBC/TheRegister/DCD/Euronews sources all describe the claim as unconfirmed with no AWS dashboard change.
- **suggested manual fix:** No code fix needed. Next scheduled review (21:30 EEST late-session risk review) should do one more check; if still unconfirmed and no service impact by then, this can likely be closed out as "claimed, never materially impactful."
- **priority:** low (downgraded from medium at 16:20)
- **first observed:** 2026-07-22 16:20 EEST (this update: 18:39 EEST)
