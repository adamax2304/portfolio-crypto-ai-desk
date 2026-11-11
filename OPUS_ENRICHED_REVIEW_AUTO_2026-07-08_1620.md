---
REVIEW: OPUS ENRICHED REVIEW — ⚠ ADVISORY ONLY — NO EXECUTION
SLOT: pre-US-open decision review · 2026-07-08 · 16:20 EEST
WRITTEN: 2026-07-08 16:24 EEST
PREV REVIEW: 2026-07-08 11:40 EEST (Europe / pre-US context)
STATUS: AUTOMATED SCHEDULED RUN — NO HUMAN IN SESSION
---

# Opus Enriched Review — pre-US-open decision review — Auto Cycle 16:20 EEST

## 1. Executive Summary

**Slot: pre-US-open decision review — advisory only / no auto-trade.** It is ~16:24 EEST (~09:24 ET), roughly 6 minutes before the US cash open (09:30 ET / 16:30 EEST).

**Major overnight/pre-open escalation confirmed externally: the Iran ceasefire is over.** President Trump declared the US–Iran ceasefire memorandum "over" following fresh American strikes on Iranian targets; the Treasury revoked Iran's oil export license. This is a materially bigger escalation than the "ships fired on in the Strait of Hormuz" story flagged at the 11:40 review. **US equity futures are down sharply into the open**: Dow futures ‑1.0% (~‑600pts), S&P 500 futures ‑0.8%, Nasdaq 100 futures ‑1.3%. Oil is up 5-6% (WTI >$74, Brent ~$78-82). VIX has jumped to 17.50 (+8.49%). This is **real, confirmed gap risk** — genuine risk-off pressure at the open, not a "no trade" excuse.

**Internal stocks regime read (risk_on / bias long, captured ~12:25 UTC) is now stale relative to this escalation** and should NOT be trusted as the opening read — re-validate SPY/QQQ direction and VIX at/after 09:30 ET before treating any long C-tier idea as fresh. Every current stocks signal is C-tier and demoted by `market_closed_intraday_planning_only` — none are actionable pre-open, which is the correct gate; the open re-evaluation is what matters now.

**Crypto: 3 positions remain OPEN and unchanged** (SPELL/USDT, BANANA/USDT, ZEC/USDT — all long, intraday/swing B) — no new triggers, no closes since 11:40. **One new development**: BTC/USDT short (intraday B) has moved from no-entry to **WAITING for entry** — directionally consistent with a risk-off macro tape. BTC ~$62,084 as of ~08:45 ET (down from the low-$63Ks referenced in recent daily context).

**UNH remains a hard AVOID** — DOJ criminal+civil Medicare Advantage billing investigation, unchanged this cycle (no fresh July 8 developments found beyond the already-confirmed picture); still appears long-only across the C-tier book. Legal/headline checks on the other near-A/B stock names (LLY, JPM, AMD, COIN, TSLA) surfaced **no fresh legal/headline risk** this cycle — clear for a technical-only read once RTH data confirms.

Catalyst mapping is weak this run (79.2% unmapped, 590/2841 mapped) — use as context, not a final-decision input.

---

## 2. Data Used

**External web research used this run** (WebSearch + WebFetch), cross-checked against internal data.

| Source | File / Timestamp | Age at 16:24 EEST | Quality |
|--------|-------------------|--------------------|---------|
| Scalp report | `2026-07-08_12-11_scalp_report.md` (gen 15:11 EEST) | ~1h13m | FRESH |
| Intraday report | `2026-07-08_12-17_intraday_report.md` (gen 15:17 EEST) | ~1h7m | FRESH |
| Swing report | `2026-07-08_12-38_swing_report.md` (gen 15:38 EEST) | ~46m | FRESH (resolved — was >33h stale as of 11:40 review) |
| Stocks intraday | `2026-07-08_12-25_stocks_intraday_report.md` (gen 15:25 EEST) | ~59m | FRESH, but pre-market snapshot — regime read now stale vs the fresh escalation (see §6) |
| Stocks swing/invest | `2026-07-02_13-0x` | ~6d | **STALE ✗** (excluded, per policy — not swing-actionable class anyway) |
| Cycle summary | `cycle_01_15-04_summary.md` (`2026-07-08_default_schedule/`) | started 15:04, finished 15:42 EEST, ~42m ago | FRESH, 41/42 steps OK, 1 fail (see §14), 90-min monitor window |
| Paper monitor | `PAPER_MONITOR_STATUS_LATEST.md` (mtime 15:41 EEST) | ~43m | FRESH |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-08_1140.md` | ~4h44m | CONTEXT — compared in §4 |
| Catalyst events | `data/catalysts/2026-07-08/catalyst_events.jsonl`, cycle file `catalyst_cycle_12-17.md` | ~1h7m | FRESH; 2841 events cumulative today, 590 mapped (20.8%) |
| DB queries | `active-signals`, `signal-stats` (crypto+stocks) via CLI | live | crypto/stocks book confirmed, no untracked legacy alerts |
| External: US futures / Iran ceasefire | Yahoo Finance, TheStreet search snippet (WebSearch/WebFetch) | live | multi-source; Dow -1.0%, S&P -0.8%, Nasdaq -1.3%, VIX 17.50 (+8.49%), oil +5-6% |
| External: Iran/Hormuz | Britannica, Wikipedia (2026 Strait of Hormuz crisis), Bloomberg (search snippets) | live | confirms new strikes 2026-07-07/08, Treasury revoked Iran oil export permits |
| External: UNH DOJ probe | Phemex, Healthcare Dive, Medical Economics, Yahoo Finance, FierceHealthcare (WebSearch) | live | confirms prior picture (criminal+civil DOJ probe, Optum Rx); no material new July 8 development found |
| External: BTC price | Fortune, SundayGuardianLive (WebSearch) | live | BTC ~$62,084 at 08:45 ET, down ~$1,145 vs prior morning |
| External: AMD / COIN / LLY / JPM legal-headline check | WebSearch (per-symbol) | live | no fresh legal/headline risk found for any of the four; LLY earnings not until August (safe); JPM analyst target raised on LLY (unrelated to JPM's own risk) |

**Notes**: TradingView/manual chart check unavailable — all technical levels from local OHLCV/ATR/EMA. Onchain config and social attention still missing (unchanged). VIX 17.50 in the internal stocks report matches the externally-confirmed post-escalation VIX read, i.e. the internal snapshot did capture some of the move, but the regime *label* (risk_on/long bias) has not caught up to it — see §6.

---

## 3. Scheduler / Data Freshness

- **Last completed cycle**: `cycle_01_15-04_summary.md` (`2026-07-08_default_schedule/`) — started 15:04:28, finished 15:42:26 EEST (~42m before this review), **41/42 steps OK, 1 failed** (`stock coverage gate + prewarm/archive`, timeout at 300s — see §14), 90-min monitor window, Telegram sent.
- **Scheduler health**: FRESH — not deferred. Day-rollover folder issue flagged in the last two reviews **appears resolved**: today's real cycle (cycle_01, started 15:04 EEST) is correctly filed under `2026-07-08_default_schedule/` (the 00:31 EEST dry-run entry in the same log is a separate, harmless earlier line) — no more cross-day fallback needed this cycle.
- **Paper monitor status** (operator vocabulary, `PAPER_MONITOR_STATUS_LATEST.md`, ~43m old):
  - OPEN actionable: **3** (SPELL/USDT, BANANA/USDT, ZEC/USDT — crypto intraday/swing B, long, entry filled, monitoring TP/SL)
  - WAITING for entry: **1** (BTC/USDT short, intraday B — new since 11:40 review, entry not yet touched)
  - REVIEW/SHADOW: **135**
  - ENTERED UNRESOLVED (entry filled, no TP/SL before window — NOT missed entries): **15**
  - NO-ENTRY / STALE / MOVED-AWAY: **45**
  - CLOSED: **378 WIN / 54 LOSS / 0 FLAT**
  - NEEDS REVIEW: **0**
- **Untracked legacy alerts**: **0** today (stable).
- **Crypto week signal-stats** (A/B, headline): sample 428, triggered 408, winrate 14.5%, PF 1.4151, avgR 0.1192, totalR 34.4551. By mode: **scalp PF 0.47/avgR ‑0.12 (n≈157, net-negative, policy-disabled)**, intraday PF ~1.8-1.9/avgR +0.2-0.3 (working), swing PF ~1.6-1.9/avgR +0.1-0.3 (working). Observation flagged by the tool: tier=B triggered winrate 14% is low (expected given low-winrate/high-PF R-multiple structure — not a new anomaly).
- **Stocks week signal-stats**: headline A/B sample=18 (weak confidence), winrate 0%, PF 0.0, totalR ‑3.0 — small sample, consistent with the pre-open C-tier demotion pattern (very few true A/B fire while the market is closed intraday). C-tier triggered winrate 6% (n=180, reliable) — confirms C-tier is correctly never actionable. Tier=B n=14 (weak), winrate 0%, PF 0.00 — same small-sample flag as last review, still worth watching, not yet actionable data.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "pre_us_open",
  "as_of": "2026-07-08 16:24 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale"],
      "data_missing": ["onchain_config_missing", "tradingview_unavailable", "social_attention_missing"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Cycle 01 (15:04-15:42 EEST) 41/42 steps OK, correctly filed under today's folder - day-rollover TODO appears resolved",
        "Swing report now FRESH (~46m, resolved from >33h stale at 11:40 review)",
        "Stocks swing/invest still STALE (~6d), excluded",
        "0 untracked legacy alerts today"
      ]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["risk_off", "wait_for_trigger", "mixed"],
      "data_missing": ["post-open RTH confirmation", "etf_flows", "dxy_yields"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "External (Yahoo Finance/WebSearch): Iran ceasefire declared over by Trump, fresh US strikes, Iran oil export license revoked",
        "Dow futures -1.0%, S&P 500 futures -0.8%, Nasdaq 100 futures -1.3% ahead of the 09:30 ET open",
        "Oil +5-6% (WTI >$74, Brent ~$78-82), VIX 17.50 (+8.49%)",
        "Internal stocks regime snapshot (12:25 UTC) still labelled risk_on/bias long - regime label has NOT caught up to the fresh escalation, demote confidence until RTH confirms",
        "Crypto BTC/ETH range-bound per 15:11-15:38 EEST reports; BTC ~$62,084 per external check (08:45 ET)"
      ]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["fresh_catalyst", "catalyst_confirmed", "mapping_weak", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Iran/Hormuz/ceasefire-over story is the dominant fresh macro catalyst this cycle, externally reconfirmed and materially escalated vs 11:40",
        "ZEC Ironwood/Tachyon catalyst carried forward, unchanged, still intact",
        "Catalyst mapping weak this run: 2841 events cumulative today, 590 mapped (20.8%), 2251 unmapped (79.2%) - above the 50% weak threshold",
        "4 active narrative baskets this cycle: perps_dex_narrative (HYPE primary), binance_ecosystem_teaser (BNB primary), delisting_thin_liquidity (no primary), momentum_breakout (KAITO/SYN primary)"
      ]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.45,
      "reason_codes": ["squeeze_risk", "oi_supports", "data_unavailable"],
      "data_missing": ["oi_24h_change (most symbols)", "liquidation_heatmap", "order_book_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SPELL/USDT and ZEC/USDT already OPEN, no fresh derivatives read needed for entry (monitor only)",
        "HMSTR/USDT: price down + OI down (deleveraging), not the fresh-shorts-pressing setup seen at 11:40 - squeeze risk lower now but still >2 ATR extended, do-not-chase stands",
        "BTC/USDT: price down + OI up per swing-mode derivatives read - fresh shorts pressing into the risk-off tape, consistent with the new WAITING short signal",
        "Most symbols still lack OI 24h change data this cycle - standing blindspot"
      ]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["entry_late", "chase_risk", "stale_before_entry", "clean_retest"],
      "data_missing": ["tradingview_manual_check"],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "SPELL/USDT, ZEC/USDT, BANANA/USDT all already OPEN and unchanged since 11:40 - monitor-only, no fresh entry decision",
        "BTC/USDT short intraday now WAITING for entry - not yet touched, no chase decision needed yet, aligns directionally with the fresh risk-off macro read",
        "Stocks: every current signal is C-tier and gated market_closed_intraday_planning_only - no live entries possible pre-open; the near-A/B demoted list (LLY, UNH, JPM, META, COIN, XLV, AMD) needs a FRESH technical re-read at/after 09:30 ET, not the pre-market snapshot",
        "No fresh B-tier crypto triggers this cycle beyond the BTC short moving to waiting"
      ]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.85,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "entered_unresolved", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Paper monitor (15:41 EEST): OPEN_ACTIVE=3, WAITING=1 (new: BTC/USDT short), REVIEW/SHADOW=135, ENTERED_UNRESOLVED_EXPIRED=15, NO_ENTRY_EXPIRED=45, CLOSED=378W/54L/0flat, NEEDS_REVIEW=0",
        "0 untracked legacy alerts",
        "track-signals pass this cycle: checked=515, updated=0, tp_hits=377 (cumulative), stopped=0, expired=0 - no fresh state changes to the open book this cycle"
      ]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["legal_risk", "headline_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "UNH: DOJ criminal+civil Medicare Advantage probe, unchanged and reconfirmed this cycle (no new July 8 development found) - still a hard AVOID, appears long-only across the C-tier book",
        "Geopolitical tail risk (Iran ceasefire over, new strikes) is now the dominant cross-asset risk factor for the open - real gap risk into 09:30 ET, not a manufactured caution",
        "AMD, COIN, LLY, JPM checked individually this cycle - no fresh legal/headline risk found for any",
        "SMCI: no fresh evidence this cycle either way - carried forward as softer caution, unchanged"
      ]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Crypto scalp still net-negative (PF ~0.47), correctly policy-disabled",
        "Crypto intraday/swing both working (PF >1.4 blended, avgR positive)",
        "Stocks headline A/B sample tiny (n=18, weak confidence) with PF 0.0 this week - too small to act on but consistent with intraday demotion pattern; stocks C-tier winrate 6% (n=180, reliable) reconfirms never-actionable status",
        "Stocks tier=B n=14 still 0% winrate / PF 0.00 - unchanged small-sample flag from 11:40 review"
      ]
    },
    {
      "agent": "head_trader",
      "verdict": null,
      "confidence": 0.65,
      "reason_codes": ["risk_off", "wait_for_trigger", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": [
        "Synthesis of all 8 agents above - see §6/§7/§8/§9 for full routing and candidates",
        "Dominant story this cycle: confirmed Iran-ceasefire-over escalation driving a real pre-open equity gap-down and oil/VIX spike - this is the key input for the next 30-60 minutes, more than any single symbol",
        "No new crypto entries fired; BTC short moved to waiting, consistent with the risk-off tape",
        "UNH is the clearest hard-avoid; ZEC is the clearest catalyst-backed hold; SPELL is the clearest RS-leader hold; BTC short-watch is the clearest fresh crypto trigger to watch into the open"
      ]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate":     { "symbol": "SPELL/USDT", "trigger": "already OPEN (intraday B); do not add fresh size — only a pullback into the entry zone with RS still intact would justify a fresh long add", "reason": "RS leader vs BTC/ETH, but stretched and not aligned with the fresh risk-off tape" },
    "best_short_candidate":    { "symbol": "BTC/USDT", "trigger": "WAITING for entry (intraday B) — let the system's own entry trigger confirm; do not pre-empt it manually, but this is the cleanest directional alignment with the Iran-ceasefire-over risk-off macro read", "reason": "price down + OI up (fresh shorts pressing) per swing derivatives read, consistent with a genuine external macro catalyst rather than a stale internal signal" },
    "best_catalyst_candidate": { "symbol": "ZEC/USDT", "trigger": "already OPEN (intraday/swing B); catalyst intact and previously reconfirmed externally (Ironwood/Tachyon)", "reason": "clearest verified fundamental catalyst still active in the book" },
    "avoid_candidate":         { "symbol": "UNH", "reason": "DOJ criminal+civil Medicare Advantage fraud probe, unchanged and reconfirmed; appears long-only in the C-tier book; avoid regardless of any tier upgrade at the open" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh, report_stale (stocks swing/invest) | advisory_only |
| market_regime | caution | 0.55 | risk_off, wait_for_trigger, mixed | advisory_only |
| catalyst_narrative | caution | 0.55 | fresh_catalyst, catalyst_confirmed, mapping_weak, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | squeeze_risk, oi_supports, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | entry_late, chase_risk, stale_before_entry, clean_retest | advisory_only |
| execution_lifecycle | ok | 0.85 | open_actionable, waiting_for_entry, review_shadow, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.75 | legal_risk, headline_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution (synthesis) | 0.65 | risk_off, wait_for_trigger, manual_review | advisory_only |

---

## 4. What Changed vs Previous Review (11:40 EEST, Europe / pre-US context)

- **Iran/Hormuz story escalated materially**: 11:40 review had "ships fired on ~19h ago, BTC reaction muted." This review externally confirms a bigger step: **Trump declared the ceasefire "over,"** the US launched fresh strikes, and Treasury revoked Iran's oil export license. This is a new, confirmed escalation, not a continuation of the same story.
- **US equity futures now show a real pre-open gap-down**: Dow ‑1.0%, S&P ‑0.8%, Nasdaq ‑1.3%, oil +5-6%, VIX +8.49% to 17.50 — none of this was known at 11:40 (US futures weren't checked in that review; markets were still ~5h from open).
- **Crypto book unchanged**: SPELL/BANANA/ZEC remain OPEN, no closes, no new intraday/swing triggers.
- **New crypto development**: BTC/USDT short (intraday B) moved from not-present to **WAITING for entry** — first fresh directional signal since 11:40, and it's aligned with the fresh risk-off macro read.
- **Swing report staleness RESOLVED**: was >33h stale (5th+ consecutive flag) at 11:40; now fresh (~46m old, gen 15:38 EEST).
- **Day-rollover scheduler TODO appears RESOLVED**: today's cycle (cycle_01, 15:04-15:42 EEST) is correctly filed under `2026-07-08_default_schedule/`, unlike the last two reviews which had to fall back to a prior day's folder.
- **UNH unchanged**: no new July 8 development found beyond the already-confirmed DOJ criminal+civil probe; verdict stands (AVOID).
- **Catalyst mapping**: 20.8%→20.8% (flat, still weak).
- **New minor infra issue**: cycle_01 had 1 failed step (`stock coverage gate + prewarm/archive`, 300s timeout) — not present as a flag in the 11:40 review's cycle (which reported 32/32 OK).

---

## 5. Catalyst Coverage

- Total `catalyst_events` today (cumulative): **2841**
- Mapped (symbol present): **590 (20.8%)**
- Unmapped: **2251 (79.2%)**
- `narrative_baskets` (latest cycle): **4** — `perps_dex_narrative` (primary HYPE/USDT; related DYDX/GMX/ASTER; `wait_pullback`), `binance_ecosystem_teaser` (primary BNB/USDT; related ASTER/USDT; `related_beta_rotation`), `delisting_thin_liquidity` (no primary; `avoid_low_liquidity`), `momentum_breakout` (primary KAITO/SYN; `wait_pullback`)

**⚠ catalyst mapping weak this run — use catalyst layer as context, not final decision.** (79.2% unmapped, above the 50% threshold — unchanged from 11:40.)

Top 3 unmapped/low-signal headlines this cycle:
1. "New Book 'Stop the Hack!' Helps Anyone Improve Their Security Online and Off — Especially Seniors" (PR Newswire) — tagged exploit_hack by keyword match, not an actual crypto exploit.
2. "China issues backdoor security risk over Anthropic's Claude Code" (Seeking Alpha) — sector/tech headline, no tradeable symbol.
3. RBLX investor-deadline securities-class-action solicitation (PR Newswire) — law-firm noise, not a fresh legal development.

---

## 6. Market Landscape

**The dominant story this cycle is macro, not any single symbol.** The Iran-ceasefire-over escalation, externally confirmed with specific futures/oil/VIX numbers, is a genuine cross-asset risk-off catalyst arriving in the last ~10-15 minutes before the US cash open. This is materially different from a routine "risk-off headwind" — it's a fresh, dated, multi-source-confirmed event with real futures/VIX/oil moves attached, not a stale internal macro score.

**Crypto**: BTC/ETH still range-bound per the 15:11-15:38 EEST internal reports (captured before the full weight of today's escalation), external BTC read ~$62,084 (down ~$1,145 vs the prior morning). The three open positions (SPELL, BANANA, ZEC) are unchanged and being monitored, not chased. The one new fact is BTC/USDT short moving to WAITING — the system's own entry-quality gate has not yet triggered it, so no manual pre-emption is warranted, but it is the cleanest crypto expression of the current macro read if/when it triggers.

**Stocks**: every active signal is C-tier and correctly gated `market_closed_intraday_planning_only` — none are live entries pre-open, which is the right behavior. But the *regime label* underlying those C-tier scores (risk_on/bias long, captured 12:25 UTC) has not caught up to the escalation that broke afterward; the review must NOT treat any of the near-A/B demoted longs (LLY, JPM, AAPL, META, XLV, GOOGL, MSFT) as "ready to go long at the open" without a fresh regime + index-direction re-check once RTH data comes in. Legal/headline checks on AMD, COIN, LLY, JPM this cycle surfaced nothing new — these names are technically clear, but the macro backdrop (futures gap-down) argues for caution on any long regardless of clean legal status.

### Market Mood / Risk Routing

- Crypto mood: **chop, tilting risk-off** (BTC/ETH still range per internal reports, but the external macro escalation and BTC's ~$1,145 pullback argue for a risk-off lean into the open)
- Stocks mood: **pre-open gap-down / risk-off** (Dow futures ‑1.0%, S&P ‑0.8%, Nasdaq ‑1.3%, VIX 17.50 — this supersedes the stale internal "risk_on" label; re-confirm at/after 09:30 ET)
- Dominant narrative: **Iran ceasefire declared over — fresh US strikes, oil export license revoked, oil/VIX spike** (overrides AI-rotation/perps-DEX narratives as the top cross-asset story this cycle)
- Preferred side now: **wait-for-trigger, tilt toward shorts/defensive** — do not chase the futures gap either direction; let the open's first 15-30 minutes confirm whether this is a fade or a trend day
- Best long candidate: **SPELL/USDT** (already open; hold/monitor, no fresh add without a pullback)
- Best short candidate: **BTC/USDT** (waiting for entry; the cleanest crypto short expression of the fresh risk-off catalyst, but let the system's own trigger confirm — do not chase manually)
- Best catalyst-backed candidate: **ZEC/USDT** (already open; catalyst intact, unrelated to today's macro story)
- What to avoid: **UNH** (legal/headline, unchanged); chasing any stock long at the open purely off the stale pre-market C-tier snapshot without a fresh index/VIX re-check; energy-name longs chasing the oil spike without a clean setup
- What would change the view: any de-escalation statement out of Washington/Tehran; RTH open confirming (or reversing) the futures gap in the first 15-30 minutes; BTC/ETH breaking their current range in either direction; the BTC/USDT short actually triggering

---

## 7. Candidate Deep Dives

### Macro / gap-risk (cross-asset, not a single symbol — the dominant story this cycle)
- Has the market already reacted? Yes, futures have moved (Dow ‑1.0%, S&P ‑0.8%, Nasdaq ‑1.3%, VIX 17.50, oil +5-6%) — this is priced into futures but NOT yet into the internal stocks regime label or any C-tier score.
- Is it a chase to act on this pre-open? Yes — futures gaps frequently mean-revert or extend unpredictably in the first 15-30 minutes; the correct action is to wait for RTH confirmation, not to pre-position off futures alone.
- What would make it actionable? A clean RTH open with confirmed direction (index + breadth + VIX behavior) in the first 15-30 minutes; any explicit de-escalation or further-escalation headline.
- Aligned with market mood? This *is* the market mood driver this cycle.
- Invalidation: a walk-back statement, a ceasefire restoration, or oil/VIX unwinding sharply intraday.

### UNH (stocks, C-tier, long, multiple entries in book — AVOID / LEGAL RISK, unchanged)
- Carried forward unchanged: DOJ criminal+civil Medicare Advantage billing investigation (Optum Rx, physician reimbursement), stock down >45% YTD, CEO departed May, guidance suspended.
- **External re-check this cycle** (Phemex, Healthcare Dive, Medical Economics, Yahoo Finance, FierceHealthcare): confirms the same picture; no new July-8-specific development found — the most recent substantive updates are from the 2025-2026 period already known.
- Actionable now? No — C-tier, gated pre-open; still hard AVOID regardless of any future tier upgrade at the open. Legal risk overrides technicals per §I discipline.
- Invalidation: none plausible short-term; would require a formal investigation closure/settlement announcement.

### SPELL/USDT (crypto, intraday B, long, OPEN — unchanged)
- Still open since prior reviews; no fresh entry decision. RS leader vs BTC/ETH, but the position was entered on an already-extended move (chase-risk flagged previously).
- Is it aligned with the current mood? Partially — RS-leader in an otherwise choppy/tilting-risk-off tape, exactly the kind of idea PART 2 favors even in mixed conditions, but do not add fresh size into a macro-driven risk-off tape.
- Actionable now? Monitor only; a fresh add requires a genuine pullback into the entry zone.
- Invalidation: loss of RS leadership vs BTC/ETH or reversal through the tracked invalidation band.

### ZEC/USDT (crypto, intraday/swing B, long, OPEN — unchanged)
- Ironwood/Tachyon catalyst reconfirmed at 11:40, unchanged and unrelated to today's macro story — genuinely fundamental, not macro-driven.
- Actionable now? Monitor only; already open.
- Invalidation: a genuine fresh whale-short buildup (the earlier $14.9M short-bet headline is stale/superseded) or a verification setback on the Tachyon proof effort.

### BTC/USDT (crypto, intraday B, short, WAITING for entry — new this cycle)
- New development: moved from absent to WAITING since the 11:40 review. Swing-mode derivatives read shows price down + OI up (fresh shorts pressing), which is directionally consistent with the confirmed macro escalation.
- Has price already reacted? Partially — BTC is down ~$1,145 vs the prior morning per the external check, but has not broken its internal range per the 15:11-15:38 EEST reports.
- Is this a chase-risk setup? Not yet — it hasn't triggered. The system's own entry-quality gate has not fired; do not manually pre-empt it.
- What would make it actionable? The system's own entry trigger firing (price reaching the tracked entry zone) with the macro backdrop still risk-off.
- Aligned with market mood? Yes — this is the cleanest crypto short candidate given the confirmed geopolitical/macro catalyst.
- Invalidation: a de-escalation headline reversing the risk-off tone, or BTC reclaiming range highs before the short triggers.

---

## 8. Best Candidates Ranked

1. **ZEC/USDT** — best catalyst-backed idea; already open, catalyst unrelated to today's macro noise and still intact. Action: hold/monitor.
2. **BTC/USDT short** — best short-watch; not yet actionable (WAITING), but the cleanest directional alignment with the confirmed Iran-ceasefire-over macro escalation. Exact trigger: the system's own entry zone being touched — do not chase manually before then.
3. **SPELL/USDT** — best RS-leader long; already open, hold/monitor only, no fresh add without a clean pullback.
4. **BANANA/USDT** — open, technical momentum, catalyst unconfirmed in the live feed. Action: hold/monitor for TP/SL.
5. No clean *new* stock entry exists pre-open by definition (market closed); the best stocks long-watch for after the open is the near-A/B demoted cohort (LLY, JPM, AAPL, META, XLV) **conditional on** a fresh RTH regime re-check confirming the futures gap has stabilized/reversed — do NOT treat the stale pre-market risk_on snapshot as sufficient on its own.

---

## 9. Avoid / No Trade

*(This decision window only — scanning, tracking, and monitoring continue regardless.)*

- **UNH** (stocks) — hard avoid, DOJ criminal+civil fraud probe, unchanged and reconfirmed. Any future UNH long idea needs manual legal-risk review before promotion, independent of score.
- **SMCI** (stocks) — softer carry-forward caution, no fresh evidence either way this cycle.
- **Any stock long chased purely off the stale pre-market C-tier snapshot** (LLY, JPM, AAPL, META, XLV, GOOGL, MSFT, etc.) — wait for RTH confirmation given the confirmed futures gap-down; legal/headline checks on AMD, COIN, LLY, JPM came back clean, but macro backdrop argues for patience regardless.
- **Chasing the futures gap in either direction** — pre-open futures moves frequently reverse or extend unpredictably in the first 15-30 minutes; wait for the open to confirm.
- **HMSTR/USDT and similar >2-ATR-extended breakdown names** — not actionable now (price down + OI down = deleveraging, not fresh-shorts-pressing); not a "no trade forever," just not the current cleanest short (BTC/USDT is, given the macro alignment).

---

## 10. Main Risks

- **Confirmed, live geopolitical/macro tail risk**: Iran ceasefire declared over, fresh strikes, oil export license revoked — real futures gap-down and VIX/oil spike heading into the open. This could either fade quickly (common for geopolitical futures gaps) or extend into a genuine risk-off session; the first 15-30 minutes of RTH will tell.
- **Internal stocks regime label is stale relative to the fresh escalation** — the risk_on/long-bias classification (12:25 UTC) predates the market's post-escalation reaction; do not trust it at face value once RTH opens.
- **UNH-style legal/headline risk remains invisible to the technical scoring layer** — the C-tier gate protects against acting on it today, but any future tier upgrade needs a manual legal check first.
- **Catalyst mapping remains weak (79.2% unmapped)** — absence of a mapped catalyst is a data gap, not proof of absence.
- **Stocks tier=B sample remains tiny (n=14, 0% winrate, PF 0.00)** — too small to act on, still just a watch item.
- **One scheduler step failed this cycle** (`stock coverage gate + prewarm/archive`, 300s timeout) — did not block report generation this cycle but worth monitoring for recurrence.

---

## 11. Action Plan — next 4 hours

- **At/after 09:30 ET (16:30 EEST) cash open**: re-run the regime read for SPY/QQQ/VIX before treating any stock C-tier idea as fresh; confirm whether the futures gap-down holds, fades, or extends in the first 15-30 minutes.
- Continue monitoring the 3 open crypto positions (SPELL, BANANA, ZEC) for TP/SL; no manual intervention needed.
- Watch the BTC/USDT short for its entry trigger — if it fires, treat it as the highest-conviction, macro-aligned crypto idea this session; do not manually pre-empt before the system's own trigger.
- Re-check the Iran/ceasefire story before the 18:30 US-open-reaction slot — this is the single most likely source of a regime confirmation or reversal today.
- Re-verify UNH and SMCI legal status has not changed once fresh news cycles through post-open.
- No scoring, threshold, or code changes — advisory only.

---

## 12. Final Verdict per Mode

- **Crypto scalp**: correctly disabled by policy (net-negative). No change recommended.
- **Crypto intraday**: working; 3 positions open and healthy, 1 new short waiting for entry aligned with the macro escalation; stay selective, no chasing.
- **Crypto swing**: data now FRESH (resolved from prior stale flag) — can be treated as a live input again.
- **Stocks intraday/swing/invest**: pre-open, C-tier only, none actionable; UNH flagged AVOID regardless of any tier upgrade at the open; do not treat the pre-market regime snapshot as valid once RTH data lands given the confirmed futures gap-down.

---

## 13. Sources

- [Stock market today: S&P 500, Nasdaq, Dow futures fall as oil surges, Trump declares ceasefire 'over' — Yahoo Finance](https://finance.yahoo.com/markets/stocks/live/stock-market-today-wednedsay-july-8-230111117.html) (2026-07-08)
- [Stock Market Today (July 8, 2026): Nasdaq futures tumble after Trump says Iran ceasefire over — TheStreet](https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-july-8-2026) (2026-07-08, title/snippet only — full fetch blocked HTTP 403)
- [2026 Strait of Hormuz crisis — Wikipedia](https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis)
- [2026 Iran war — Britannica](https://www.britannica.com/event/2026-Iran-war)
- [UnitedHealth Group (UNH) Stock in 2026: DOJ Probe, Medicare Reset, Key Risks — Phemex](https://phemex.com/academy/unitedhealth-group-unh-stock-2026)
- [DOJ's criminal probe into UnitedHealth extends to Optum Rx, physician reimbursement — FierceHealthcare](https://www.fiercehealthcare.com/payers/wsj-report-doj-interviewing-former-employees-about-medicare-billing-practices-unitedhealth)
- [UnitedHealth Group under DOJ investigation over Medicare billing practices — Medical Economics](https://www.medicaleconomics.com/view/unitedhealth-group-under-doj-investigation-over-medicare-billing-practices)
- [Current price of Bitcoin for July 8, 2026 — Fortune](https://fortune.com/article/price-of-bitcoin-07-08-2026/)
- [JPMorgan Raises Eli Lilly Price Target Amid Strong Earnings Outlook — GuruFocus](https://www.gurufocus.com/news/8947284/lly-jpmorgan-raises-eli-lilly-price-target-amid-strong-earnings-outlook) (2026-07-07)
- [SEC Strategy Shift: Coinbase Case Collapse, Binance Stay Mark Crypto Regulatory Turning Point — Manatt, Phelps & Phillips](https://www.manatt.com/insights/newsletters/client-alert/sec-strategy-shift-coinbase-case-collapse-binance-stay-mark-crypto-regulatory-turning-point)

---

## 14. Fix Requests / TODO

### TODO-scheduler-coverage-gate-timeout
- **issue:** The `stock coverage gate + prewarm/archive` step in cycle_01 (2026-07-08 15:04-15:42 EEST) failed with a 300s timeout (exit=-1). Did not block report generation this cycle (41/42 steps still completed OK), but is a new failure not seen in the last two reviews' cycle summaries.
- **evidence:** `data/scheduled_runs/2026-07-08_default_schedule/cycle_01_15-04_summary.md`, step 26: `[FAIL] stock coverage gate + prewarm/archive (exit=-1, 300.0s, attempts=1)`.
- **suggested manual fix:** Investigate whether this step is hitting a slow data source or a hung subprocess; consider a shorter internal timeout with retry, or move it to a non-blocking/best-effort position in the pipeline if it isn't critical-path.
- **priority:** low (non-blocking this cycle, but worth watching for recurrence)
- **first observed:** 2026-07-08 16:24 EEST (this review)

### TODO-catalyst-mapping-still-weak
- **issue:** Catalyst symbol-mapping coverage remains well under the 50% target (20.8% mapped, 2251/2841 unmapped this cycle) — flat vs the 11:40 review, still a recurring issue across many reviews.
- **evidence:** `data/catalysts/2026-07-08/catalyst_events.jsonl`: 2841 total, 590 mapped, 2251 unmapped.
- **suggested manual fix:** Improve the symbol resolver in the catalyst layer (ticker/company-name matching against a broader universe; several unmapped headlines this cycle contain a resolvable ticker in the text, e.g. WGS/GeneDx from the 11:40 review).
- **priority:** medium (recurring across many reviews)
- **first observed:** prior reviews; still present 2026-07-08 16:24 EEST

### TODO-notifier-underscore-workaround-not-yet-fixed
- **issue:** The Telegram notifier's default `parse_mode="Markdown"` rejects (HTTP 400) any message containing the literal filename `OPUS_ENRICHED_REVIEW_LATEST.md` (unbalanced-underscore parsing). A backtick-wrapping workaround has been applied manually across multiple reviews; underlying code not yet fixed.
- **evidence:** Observed and worked around in the 04:47 and 11:40 EEST reviews; same workaround applied in this review's Telegram send.
- **suggested manual fix:** Escape underscores, switch to `parse_mode="MarkdownV2"` with proper escaping, or use `parse_mode=None` in the notifier's message-building code path used by this routine.
- **priority:** low (workaround reliable, but recurring)
- **first observed:** 2026-07-08 04:47 EEST; still unresolved 2026-07-08 16:24 EEST
