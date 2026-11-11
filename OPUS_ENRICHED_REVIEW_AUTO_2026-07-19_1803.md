# Opus Enriched Review — pre-US-open decision review — Auto Cycle 18:03 EEST

## 1. Executive Summary

**Slot: pre-US-open decision review** (nominal 16:20 EEST slot; this run dispatched at **18:03 EEST**, ~103 min of jitter — noted in §3, does not change the read). **Advisory only — no auto-trade, no scoring/threshold/strategy changes made or implied.**

**Critical framing correction:** today, **2026-07-19, is a Sunday.** US cash equities are **closed all day** — there is no same-day US open to prep for. The "pre-US-open" lens is therefore read forward to **Monday 2026-07-20's** gap risk, not an imminent same-day open. Per the routine's own weekend rule, all stock signals below are **planning/watchlist context only**; crypto is the sole live-actionable class this window.

**Dominant driver — macro risk-off, escalating:** the US-Iran conflict has reached its **8th consecutive night of US airstrikes** on Iran as of today (Al Jazeera, 2026-07-19), following an Iranian attack that killed 2 US service members in Jordan; strikes now target infrastructure threatening the **Strait of Hormuz**, oil sanctions have been reimposed, and BTC/ETH have been under sustained pressure through the week as a direct result (Yahoo Finance, 2026-07-17). This is the single biggest **gap-risk driver into Monday's open** (energy/risk-off spillover into equities) and the key context for every crypto read below.

**Crypto book:** 7 open, running B-tier long positions (LTC×2, ETH, ETHFI, CASHCAT, TRUMP, ALLO — all `tp1_hit`/`tp2_hit`, none freshly enterable now), no A-tier anywhere. One legacy short (NEAR/USDT scalp) is a **stale bookkeeping item, now 50h+ past its expiry unresolved** — needs review, not a live risk. **Internal regime read (bullish tape, capping all short ideas) conflicts with the verified external risk-off macro** — treat the internal regime label as macro-fragile (same caution raised in the 11:39 review, still unresolved).

**Integrity note (escalating, not new):** the untracked watchlist-alert bug flagged in prior sessions (Telegram alert fires, no `proposed_signal` minted) recurred again today on **ALLO/USDT (×2) and now HOME/USDT** — a second symbol added to the pattern. See §14 TODO-1.

**Stocks:** market closed; no A/B candidate is actionable. One open C-tier UNH invest long carries an **unresolved DOJ criminal Medicare-fraud probe** — an old, ongoing risk (not fresh breaking news) but still unaddressed against a live position; flagged as caution, see §9/§14.

**Catalyst mapping is weak this run (67.3% unmapped)** — use as context, not as a decision driver.

## 2. Data Used

- Reports: scalp (2026-07-19_11-31, ~2.5h old — fresh), intraday (2026-07-19_11-38, ~2.4h old — fresh), swing (2026-07-19_01-47, ~13h16m old — **borderline stale**, used with flag). Stocks intraday/swing/invest: all Jul 15–17 dated, market-closed weekend — planning-only, excluded from any actionable verdict.
- Catalysts: `data/catalysts/2026-07-19/catalyst_events.jsonl` (2,335 events today, cumulative), `narrative_baskets.jsonl` (5 baskets), latest `catalyst_cycle_11-40.md`.
- LLM packets: `llm_analysis_packet.md` (14:38, fresh, crypto). `llm_stocks_packet.md` (Jul 17 14:25, stale/weekend, planning-only).
- CLI: `active-signals` ×2 (crypto 8 rows, stocks 50 rows), `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-07-19` (**3 findings** — ALLO×2, HOME×1).
- DB reads: `news_items` (per-symbol 24–72h checks for NEAR, ALLO, HOME, BANK, HYPE, UNH), `watchlist_alerts` + `proposed_signals` for ALLO/HOME reuse-bug confirmation.
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-19_1139.md` (Europe/pre-US context slot).
- External: 4 WebSearch queries (BTC/ETH mood, Iran/Hormuz macro, UNH DOJ probe, HYPE/Hyperliquid news) + 2 WebFetch verifications (Al Jazeera, CryptoTimes). 4/4 sources ingested via `scripts.ingest_enriched_review_sources` (3 crypto, 1 stocks).

## 3. Scheduler / Data Freshness

- `scheduler.log`: mtime **18:03**, current at run time — fresh, **not deferred**.
- Latest cycle summary `cycle_05_14-23_summary.md`: mtime **14:59**, ~3h04m old at run time — just outside the "fresh" band but scheduler.log itself is current, so the defer rule (both >3h) does **not** trigger.
- Standalone monitors: `crypto_monitor` log active to 18:03, `derivatives_monitor` log active to 18:03, `pending_monitor` log active to 18:03, `mexc_canary_monitor` last restart-cycle log 14:24 (normal cadence) — all alive, healthy.
- Dispatch jitter: this run's nominal slot is 16:20 EEST; actual dispatch was 18:03 EEST (~103 min late). Content and candidates are unaffected (data freshness checked independently above), but flagged for data_quality.
- Scalp/intraday: fresh (~2.4–2.5h old). Swing: ~13h16m old — **borderline stale** band (12–14h), used with that flag, not excluded.
- Stocks (all modes): 2–4 days stale, market closed for the weekend — planning-only per the routine's own weekend rule, excluded from any actionable verdict.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-19 18:03 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["fresh derivatives snapshot beyond 11:38 report", "live intraday OHLCV newer than report generation"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 18:03", "swing report 13h16m old (borderline stale)", "dispatch jitter 103min vs nominal 16:20 slot"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mixed", "risk_off", "chop"],
      "data_missing": ["live BTC/ETH price newer than mid-week external snapshot"],
      "suggested_effect": "advisory_only",
      "facts_used": ["internal intraday report caps ALL short setups as 'fighting a bullish tape' (audit cap)", "external: BTC/ETH under sustained pressure, 8th night of US-Iran strikes, Strait of Hormuz threatened (Al Jazeera, Yahoo Finance)", "internal regime label conflicts with external risk-off macro — same divergence flagged in 11:39 review, still unresolved"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "catalyst_contradicted", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["764/2335 catalyst_events mapped = 32.7%, unmapped 67.3%", "HYPE fresh<6h perps_dex_narrative basket, externally confirmed (ETF inclusion vs unlock/MAS alert — mixed)", "NEAR/USDT false-tagged 5x in 24h from Iran-war Telegram headlines containing the word 'near' — zero genuine NEAR catalyst"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["squeeze_risk", "oi_supports", "funding_extreme"],
      "data_missing": ["live funding/OI updates newer than 11:38 report"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ALLO/USDT: price up + OI up (24h OI +5.38%, long/short 0.786) — fresh positioning confirms trend, not squeeze-prone", "internal squeeze-guard caps every scanned short candidate (LAB, TOFU, SYN, XEC, KITE, RE, DEXE, BDX) to C-tier — thin-liquidity/short-squeeze risk across the board"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["entry_late", "chase_risk", "clean_retest", "stale_before_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["all 7 open crypto longs are already tp1_hit/tp2_hit — fresh entry now would be late/chasing", "BANK/USDT +145.2%/24h pure momentum, no catalyst, explicit avoid_chase playbook", "no new clean B-tier entry trigger observed this cycle"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["open_actionable", "needs_review", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["7 open-actionable crypto B-tier longs (LTC x2, ETH, ETHFI, CASHCAT, TRUMP, ALLO)", "NEAR/USDT scalp short: tp1_hit but 50h+ past expires_at (2026-07-17T15:56), unresolved — needs_review, growing from 44h+ at 11:39", "ALLO/HOME untracked watchlist alerts (no proposed_signal) — needs_review", "stocks: 50 legacy signals, all market-closed/stale, no_entry/planning-only"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["headline_risk", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["US-Iran war escalating into the weekend — Monday gap-risk driver for both crypto and equities", "UNH open C-tier invest long sits against an ongoing (not fresh) DOJ criminal Medicare-fraud probe — unaddressed internally", "watchlist-alert reuse bug now spans 2 symbols (ALLO, HOME) — data-integrity risk to Telegram-actionable counts"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto week: intraday/swing PF 2.11/1.70 (working), scalp PF 0.525 avgR -0.17 (failing), short direction PF 0.20 avgR -0.44 (failing) — the one open short (NEAR) sits in the intersection of both failing buckets", "stocks week: overall PF 0.85 avgR -0.056 (failing), tier B PF 0.50 (n=9, anecdotal, negative), long-direction PF 0.725 vs short-direction flat PF 1.0"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "ALLO/USDT", "trigger": "already open (tp1_hit, entry 0.444129-0.451586, invalidation 0.435014) — hold while OI keeps expanding alongside price (24h OI +5.38%, long/short 0.786, crowding normal); no fresh add here, just the cleanest continuation long on the board", "reason": "only open long with a confirming derivatives read (price+OI both rising, no squeeze/crowding flag) in an otherwise stale/late book" },
    "best_short_candidate":    { "symbol": "XEC/USDT", "trigger": "watch-only — internal squeeze-guard caps it to C (thin-liquidity/short-squeeze risk) and it fights the system's own bullish-regime audit cap; would need a clean break + retest below the recent swing low on rising volume AND the squeeze-guard/regime cap to lift before it is actionable", "reason": "weakest RS vs BTC (-17.5%) among all scanned short setups, but every internal safeguard currently blocks it — correctly so, given historical short-direction PF is 0.20" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "wait_pullback playbook — basket primary, fresh<6h; wait for a pullback toward support with volume confirmation, not a chase at current levels", "reason": "genuine, externally-verified two-sided catalyst set (T. Rowe Price TKNZ ETF ~6% HYPE weighting + record $11.07B platform OI = bullish; $645M July 6 unlock + MAS Investor Alert List addition = bearish) — real news, not a mistagged headline" },
    "avoid_candidate":         { "symbol": "BANK/USDT", "reason": "momentum_breakout basket primary, +145.2%/24h with zero confirmed news catalyst (pure momentum cluster per catalyst_cycle_11-40.md); playbook is explicitly avoid_chase; same call stands from the 11:39 review" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.50 | mixed, risk_off, chop | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, catalyst_contradicted, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | squeeze_risk, oi_supports, funding_extreme | advisory_only |
| technical_entry | caution | 0.55 | entry_late, chase_risk, clean_retest, stale_before_entry | advisory_only |
| execution_lifecycle | caution | 0.65 | open_actionable, needs_review, no_entry | advisory_only |
| risk_manager | caution | 0.60 | headline_risk, reduce_risk, manual_review | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| **head_trader** | **caution (watch)** | **0.60** | synthesis of above | advisory_only |

## 4. What Changed vs Previous Review (11:39 EEST, Europe/pre-US context)

- **HOME/USDT closed out**: was `tp2_hit` and open at 11:39; no longer in the active-signals table — resolved/closed between cycles. A **new** C→B intraday watchlist alert fired for HOME at 11:57 (score 65.2) but, like ALLO, **no fresh `proposed_signal` was minted** — this is the same reuse bug widening to a second symbol (§14 TODO-1).
- **XLM/USDT and ZEC/USDT dropped off**: both were open/waiting at 11:39 (XLM triggered, ZEC waiting_for_entry); neither appears in the current active-signals table — resolved/expired between cycles, not carried into this window.
- **ETHFI/USDT is new** since 11:39 (swing B, tp1_hit, entry 0.446404-0.449586) — not mentioned in the prior review.
- **NEAR/USDT bookkeeping gap widened again**: was 44h+ past expiry at 11:39, now **50h+** past expiry (2026-07-17T15:56), still unresolved.
- **ALLO/USDT untracked-alert pattern repeated**: two more rejected→B watchlist alerts fired today (09:39 intraday score 67.1, 11:36 scalp score 70.4) with no backing `proposed_signal`, on top of the one already-open intraday position (sig_10088a4c71cae845, unchanged since 2026-07-18).
- **Macro thesis intensified, not resolved**: 11:39 review described an escalating US-Iran conflict (~90 targets struck Jul 13-14); this run confirms the **8th consecutive night** of strikes, 2 US service members killed, Strait of Hormuz shipping directly threatened, oil sanctions reimposed — the risk-off overhang for Monday's open is stronger, not weaker.
- **Catalyst mapping stayed weak**: 69.8% unmapped at 11:39 vs **67.3% unmapped** now (cumulative daily) — persistent, not improving.
- **BANK/USDT avoid call reaffirmed**: still the top no-catalyst momentum pump (basket primary again today, +145.2%/24h) — no change to the 11:39 verdict.

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative): **2,335**. Mapped (non-null symbol): **764 (32.7%)**. Unmapped: **1,571 (67.3%)**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (67.3% > 50% threshold)
- Top 3 unmapped headline samples: "Base memecoin $BRIAN surges after Brian Armstrong changes X avatar, then crashes 86%..."; "TODAY: The GENIUS Act marks its one-year anniversary..."; "LATEST: Rep. William Timmons says the CLARITY Act is 'on the one-yard line'..." — mostly legit macro/legal commentary without a single clean ticker mapping, not obviously erroneous, but they inflate the unmapped count.
- `narrative_baskets.jsonl`: 5 baskets — **perps_dex_narrative** (HYPE primary, fresh<6h, `wait_pullback`), **ai_narrative** (NEAR/RENDER/TAO/FET primary, fresh<6h — **contains the NEAR substring-match contamination**, see §7/§14), **rwa_narrative** (ONDO/XLM primary, freshness unknown), **delisting_thin_liquidity** (no symbols, `avoid_low_liquidity`), **momentum_breakout** (BANK/TLM/KAITO primary, fresh<1h, `avoid_chase`).

## 6. Market Landscape

Crypto tape: internal intraday report reads a **bullish-trend regime** strongly enough that it audit-caps every single scanned short setup today (LAB, TOFU, SYN, XEC, KITE, RE, DEXE, BDX all explicitly capped to C for "short setup fights a bullish tape" / squeeze risk). This directly conflicts with the externally-verified macro: BTC/ETH have been under sustained pressure all week as the US-Iran conflict escalated to an 8th consecutive night of strikes, with the Strait of Hormuz — a critical global shipping/energy corridor — directly threatened. **Treat the internal bullish-regime label as macro-fragile**, exactly as flagged in the 11:39 review; it has not been reconciled since.

Altcoin breadth: long-biased book (7/7 open crypto positions are longs) is currently working on paper (`tp1_hit`/`tp2_hit` across the board), consistent with the week's playbook stats showing intraday/swing long modes strongly positive (PF 2.11 / 1.70) while scalp and short direction are both negative-edge buckets (PF 0.525 / 0.20 respectively).

Stocks: market closed (Sunday). All 50 active-signal rows are 2+ day old carry-forward/expired remnants from Fri Jul 17 and earlier — no fresh pre-market or RTH data exists to confirm anything for Monday. UNH carries an unresolved DOJ criminal probe against an open C-tier invest long.

### Market Mood / Risk Routing

- Crypto mood: **mixed / risk-off leaning** — internal regime reads bullish, external macro (Iran war escalation) reads risk-off; treat internal label as stale/optimistic.
- Stocks mood: **closed** (weekend) — Monday gap risk elevated given oil/Hormuz escalation; UNH carries unresolved legal overhang.
- Dominant narrative: US-Iran war escalation (8th night of strikes) as the macro risk-off driver; HYPE's ETF-inclusion-vs-unlock tension as the cleanest genuine crypto-specific catalyst story.
- Preferred side now: **mixed / wait-for-trigger** — hold the existing long book (working), do not add fresh longs or shorts without confirmation; crypto is the only live-actionable class this window.
- Best long candidate: ALLO/USDT (already open, OI+price confirm continuation — see §8).
- Best short candidate: none clean — XEC/USDT is the best short-**watch** (squeeze-guard + bullish-regime cap both block it currently).
- Best catalyst-backed candidate: HYPE/USDT (wait_pullback).
- What to avoid: BANK/USDT (no-catalyst momentum pump, avoid_chase).
- What would change the view: a confirmed de-escalation of the US-Iran conflict (risk-on reversal) or a further escalation that closes the Strait of Hormuz outright (deeper risk-off, favor shorts/hedges); on Monday's open, RTH confirmation before treating any stock signal as live.

## 7. Candidate Deep Dives

**TradingView / manual chart check unavailable this run** — all price-structure reads below use only local OHLCV/ATR/EMA/RS/OI/funding fields already present in the scalp/intraday/swing reports and CLI outputs; no chart was visually inspected.

### ALLO/USDT (long, intraday, B-tier, open `tp1_hit`)
- Entry 0.444129–0.451586, invalidation 0.435014, active since 2026-07-18T15:21 (sig_10088a4c71cae845).
- Price has already reacted (tp1 hit); not a fresh entry — entering "now" would be late relative to the original trigger.
- Derivatives confirm, not squeeze: 24h OI +5.38%, long/short 0.786, crowding normal — "price up + OI up" per the intraday report, i.e. fresh positioning genuinely backing the move rather than a thin short-squeeze bounce.
- No internal `news_items` hit for ALLO in the past 72h — no catalyst backing, purely technical/derivatives-confirmed.
- **Integrity flag**: two additional watchlist alerts fired for ALLO today (09:39, 11:36) with no backing `proposed_signal` — see §14 TODO-1. This does not change the open position's validity, but it means Telegram-visible "signals" for ALLO today outnumber what the tracker will actually score.
- Verdict: hold existing position, no fresh add; aligned with mood only in the narrow sense that it's the one long with clean derivatives support in an otherwise stale book.

### HOME/USDT (closed prior position; new untracked alert, B-tier, intraday)
- Previous HOME position (open at 11:39, tp2_hit) has closed/resolved between cycles.
- A new C→B intraday watchlist alert fired at 11:57 (score 65.2) — **no `proposed_signal` exists for it** (confirmed via `proposed_signals` query: zero rows for HOME/USDT since the prior signal closed).
- No internal `news_items` hit for HOME in 72h — untraceable catalyst-wise.
- Verdict: **not actionable** — there is no trackable signal_id behind this alert. Flagged as a data-integrity gap, not a trade idea. See §14 TODO-1.

### NEAR/USDT (short, scalp, B-tier, `tp1_hit`, needs_review)
- Entry 1.9323–1.9441, invalidation 1.9585, `expires_at` 2026-07-17T15:56 — **50h+ past expiry**, still shown active/unresolved.
- This position sits at the intersection of the two weakest-edge buckets in this week's stats: scalp mode (PF 0.525, avgR -0.173) and short direction (PF 0.20, avgR -0.444) — historically the worst combination on the desk.
- **Catalyst contamination**: the only "NEAR" news in the past 24h (5 Telegram rows, `t.me/marketfeed` / `t.me/WalterBloomberg`) are Iran-war headlines ("...struck an area **near** Hajiabad...", "...attacks **near** Sirik...") where the symbol detector mistagged the English word "near" as `NEAR/USDT`. **Zero genuine NEAR catalyst exists internally right now** — the `ai_narrative` basket's NEAR primary listing should be read with this in mind (see §14 TODO-3).
- Verdict: this is a bookkeeping/closure gap, not a live trading risk — status display should not be read as "0R" or "expired"; it is `NEEDS REVIEW` (entered, tp1 hit, never formally closed).

### HYPE/USDT (catalyst-watch, no open position)
- Basket primary of `perps_dex_narrative`, fresh<6h, playbook `wait_pullback`.
- Externally verified two-sided catalyst (CryptoTimes, 2026-07-19; confirmed via WebFetch): platform fundamentals at a 2026 high ($11.07B OI, HIP-3 RWA growth) and T. Rowe Price's TKNZ ETF listing HYPE as a ~6% core holding (from Jul 17) are genuine bullish drivers; against that, a $645M token unlock (Jul 6) and Singapore MAS adding Hyperliquid to its Investor Alert List (late June) are real bearish/regulatory headwinds. Price is down 2.4%/24h, 11.7%/week, off its mid-June ATH (~$76.85) to ~$59.
- Not a chase: price has already corrected significantly; the `wait_pullback` playbook fits — a fresh long only makes sense on a confirmed pullback-and-hold at support with volume, not at current levels.
- Would invalidate: a break of support with rising volume, or a fresh negative regulatory action beyond the existing MAS alert.

### BANK/USDT (avoid — no open position)
- Basket primary of `momentum_breakout`, fresh<1h, playbook `avoid_chase`. +145.2%/24h, volume 2.23x — a pure momentum spike with **zero confirmed news catalyst** internally (no `news_items` hit in 72h) and none surfaced externally this pass either.
- This is the same call the 11:39 review made (externally confirmed then as a no-catalyst pump that had already round-tripped); nothing has changed to soften that verdict.
- Verdict: avoid / do not chase, consistent across both reviews today.

## 8. Best Candidates Ranked

1. **ALLO/USDT** (long, open, hold) — only position with confirming derivatives (OI+price both rising), no squeeze flag.
2. **HYPE/USDT** (catalyst-watch, wait_pullback) — genuine, externally-verified two-sided catalyst; not actionable at current levels, watch for a confirmed pullback-and-hold.
3. **XEC/USDT** (short-watch only) — weakest RS vs BTC among scanned shorts, but blocked by squeeze-guard + bullish-regime audit cap; would need both to clear plus a break/retest below the recent swing low on rising volume.
4. **BANK/USDT** (avoid) — no-catalyst momentum pump, avoid_chase.
5. **NEAR/USDT** (needs_review, not a trade idea) — stale bookkeeping remnant in the two weakest-edge buckets on the desk; catalyst linkage is a false positive.

## 9. Avoid / No Trade

*(this decision window only — never a command to stop the system)*

- **BANK/USDT**: no-catalyst momentum spike, avoid_chase playbook — avoid new entries.
- **All fresh short entries, crypto**: internal squeeze-guard is currently capping every scanned short candidate to C-tier, and the week's stats show short direction at PF 0.20 — no new shorts warranted until a clean setup clears both the guard and the historical edge concern.
- **UNH long (stocks, C-tier invest, open)**: unresolved DOJ criminal Medicare-fraud probe sits against this position; not a fresh headline, but unaddressed. Treat as **manual review required**, not a clean actionable, until the legal situation is explicitly reviewed.
- **All stock signals generally**: market closed for the weekend; nothing here is actionable until Monday RTH confirmation.

## 10. Main Risks

1. **Internal regime/external macro divergence**: the system's own bullish-trend read (capping every short) conflicts with an intensifying US-Iran war and its risk-off spillover into crypto — this has been flagged twice now (11:39 and this run) without reconciliation.
2. **Monday gap risk**: 8th consecutive night of US strikes on Iran, Strait of Hormuz directly threatened, oil sanctions reimposed — a real driver for a volatile Monday US cash open regardless of today's stock-market closure.
3. **Data-integrity/reuse bug widening**: untracked watchlist alerts now span two symbols in one day (ALLO, HOME) — Telegram-visible alert volume is outrunning what the tracker can actually score, risking silent under-counting of true performance.
4. **NEAR catalyst false-positive**: the `ai_narrative` basket's NEAR primary listing is currently 100% contaminated by unrelated Iran-war headlines; any downstream read that treats NEAR as "catalyst-supported" today would be wrong.
5. **UNH legal overhang unaddressed**: an open C-tier invest long sits against an active DOJ criminal probe with no internal legal-risk gate applied to C-tier positions (the routine's own legal-risk rule is scoped to A/B only).

## 11. Action Plan — next 4 hours

- Hold the existing 7 open crypto longs as-is; no fresh entries recommended without a confirmed pullback (HYPE) or a squeeze-guard-cleared short setup (XEC or similar).
- Do not chase BANK/USDT or any other unconfirmed momentum spike.
- Treat NEAR/USDT as a data-hygiene item for manual closure, not a live position to manage.
- Into Monday's open: watch Strait-of-Hormuz / Iran-war headlines as the primary gap-risk driver for both crypto continuation and the eventual US cash open; re-verify UNH's legal status before treating its invest position as routine.
- No scanner, monitor, or scheduler changes — all systems continue running as-is.

## 12. Final Verdict per Mode

- **Crypto scalp**: caution / no new entries — weakest edge bucket this week (PF 0.525), and its one open position (NEAR) is a stale bookkeeping item, not a live trade.
- **Crypto intraday**: watch / hold existing — strongest working mode (PF 2.11); ALLO is the cleanest continuation long.
- **Crypto swing**: watch / hold existing — solid edge (PF 1.70); LTC, ETHFI, TRUMP, CASHCAT all running as planned.
- **Stocks (all modes)**: no-entry / planning-only — market closed; re-confirm everything at Monday RTH open; UNH invest position needs manual legal review.

## 13. Sources

- [US hits Iran for 8th consecutive night; Tehran returns fire on Gulf bases](https://www.aljazeera.com/news/2026/7/19/us-launches-eighth-consecutive-night-of-attacks-on-iran) — Al Jazeera, 2026-07-19
- [Bitcoin and ethereum prices today, Friday, July 17, 2026: Prices ease as conflict in Iran escalates](https://finance.yahoo.com/personal-finance/investing/article/bitcoin-and-ethereum-prices-today-friday-july-17-2026-prices-ease-as-conflict-in-iran-escalates-125602208.html) — Yahoo Finance, 2026-07-17
- [HYPE Falls Despite Hyperliquid's Record Growth and SEC Talks](https://www.cryptotimes.io/2026/07/19/hype-falls-despite-hyperliquids-record-growth-and-sec-talks/) — CryptoTimes, 2026-07-19
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth) — FierceHealthcare, date unavailable (probe first disclosed ~mid-2025, ongoing)
- Internal: `data/catalysts/2026-07-19/catalyst_cycle_11-40.md`, `news_items` (NEAR/ALLO/HOME/BANK/HYPE/UNH queries), `watchlist_alerts` + `proposed_signals` (ALLO/HOME reuse-bug confirmation), `active-signals`/`signal-stats` CLI outputs.

## 14. Fix Requests / TODO

### TODO-1: watchlist-alert → proposed_signal reuse/drop bug, now spanning 2 symbols in one day
- **issue:** Telegram-visible tier-upgrade alerts fire (`previous_tier` → `new_tier=B`) without a matching `proposed_signal` being created, so `detect_untracked_legacy_alerts` cannot track them for PF/winrate/avgR.
- **evidence:** `python -m scripts.detect_untracked_legacy_alerts --since 2026-07-19` → 3 untracked alerts today: ALLO/USDT (09:39 intraday score 67.1, 11:36 scalp score 70.4), HOME/USDT (11:57 intraday score 65.2). `watchlist_alerts` rows id 1682/1687/1688 confirm `previous_tier='rejected'`/`'C'` → `new_tier='B'` with zero corresponding `proposed_signals` rows.
- **suggested manual fix:** investigate why the alert-tier-transition path and the proposed-signal-creation path can diverge; this was previously raised on ALLO/BANK — it now recurs on ALLO again and has spread to HOME, suggesting a systemic gap rather than a one-off.
- **priority:** high (already raised previously, recurrence + symbol-spread today)
- **first observed (recurrence dated):** 2026-07-19 18:03 EEST (original issue raised in an earlier session)

### TODO-2: NEAR/USDT scalp-short signal unresolved 50h+ past expiry
- **issue:** `sig_b16bb9e54598333a` (NEAR/USDT, scalp, short, tp1_hit) has `expires_at` 2026-07-17T15:56 but remains in the active-signals table 50h+ later, never formally closed.
- **evidence:** `active-signals --asset-class crypto` output, this run; was 44h+ past expiry at the 11:39 review, now 50h+.
- **suggested manual fix:** add an automated closure/expiry-sweep job for signals whose `expires_at` has passed but status hasn't been finalized, so "active signals" counts stay accurate.
- **priority:** medium-high
- **first observed:** 2026-07-19 04:40 EEST (growing since)

### TODO-3: NEAR/USDT symbol detector false-positives on the English word "near"
- **issue:** `detected_symbols_json` tags `NEAR/USDT` on unrelated Telegram geopolitical headlines that merely contain the word "near" (e.g., "struck an area near Hajiabad", "attacks near Sirik", "downed near U.S. Consulate").
- **evidence:** `news_items` query, past 24h: 5 rows from `t.me/marketfeed`/`t.me/WalterBloomberg`, all Iran-war content, all tagged `["NEAR/USDT"]` with zero genuine connection to the NEAR protocol.
- **suggested manual fix:** add word-boundary/context checks to the symbol resolver for common-English-word tickers (NEAR, ONE, ENJ, etc.) — flagged previously as a "known" issue in the 11:39 review; still unfixed.
- **priority:** medium (contaminates catalyst-linkage confidence, not scoring directly)
- **first observed:** prior to 2026-07-19 11:39 EEST (recurs again this cycle)

### TODO-4: catalyst mapping persistently weak (>65% unmapped, multiple cycles running)
- **issue:** unmapped catalyst_events share was 69.8% at 11:39 and is 67.3% now — no improvement across the day.
- **evidence:** `catalyst_events.jsonl` symbol-null count, this run: 1,571/2,335 (67.3%) unmapped.
- **suggested manual fix:** improve the symbol resolver's recall for macro/legal/sector commentary (GENIUS Act, CLARITY Act, tokenization-thesis pieces, etc.) that currently maps to nothing.
- **priority:** medium
- **first observed:** prior to 2026-07-19 (recurring across multiple reviews)

### TODO-5: no legal-risk gate on open C-tier stocks positions
- **issue:** the routine's legal/headline-risk check (§I) is scoped to A/B-tier stock candidates only; the open UNH C-tier invest long (DOJ criminal Medicare-fraud probe, ongoing) has no internal flag despite carrying real legal risk through 2026-08-01.
- **evidence:** `active-signals --asset-class stocks` — `sig_90b50ceef0d1ebd3` (UNH, C, invest, long, triggered, expires 2026-08-01) and `sig_4697b87c9845547f` (UNH, C, invest, long, tp1_hit, expires 2026-07-31); `catalyst_cycle_11-40.md` legal/regulatory section lists 5 UNH DOJ-probe headlines at importance 0.73.
- **suggested manual fix:** consider extending the legal-risk check to any open C-tier position with a multi-week holding window (invest/swing), not just A/B.
- **priority:** low-medium
- **first observed:** 2026-07-19 18:03 EEST
