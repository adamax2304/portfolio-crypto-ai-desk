---
REVIEW: OPUS ENRICHED REVIEW — ⚠ ADVISORY ONLY — NO EXECUTION
SLOT: Late-session risk review · 2026-07-08 · 21:39 EEST (dispatched 21:39, ~9min jitter)
WRITTEN: 2026-07-08 21:50 EEST
PREV REVIEW: 2026-07-08 18:40 EEST (US open reaction review)
STATUS: AUTOMATED SCHEDULED RUN — NO HUMAN IN SESSION
---

# Opus Enriched Review — Late-Session Risk Review — Auto Cycle 21:39 EEST

## 1. Executive Summary

**Slot: late-session risk review — advisory only / no auto-trade.** External web research (WebSearch/WebFetch) was available this run and used for two candidates (UNH, VANRY).

It is ~21:39 EEST (~14:39 ET), well into the US regular session (closes ~23:00 EEST / 16:00 ET). The book is thin and mostly quiet: crypto has exactly **one** genuinely OPEN actionable position (SPELL/USDT long intraday/B, entry filled, ~2h remaining to window close) and **one** WAITING-for-entry (NEAR/USDT short swing/B). The four crypto **scalp** signals (BTC/ETH/SOL/NEAR shorts) that DB shows as `triggered` are **not** Telegram-actionable — the authoritative `PAPER_MONITOR_STATUS_LATEST.md` classifies them REVIEW/SHADOW (scalp is policy-gated to shadow, consistent with the scalp report's own "low confidence" banner). Two of the four (SOL, NEAR/BTC) are inside minutes of their 2h validity window closing; treat as about to age into NO-ENTRY/STALE, not as live risk.

**Stocks book is empty of A/B actionable setups.** Every stock idea (LLY, META, XLV, JPM, etc.) sits at C-tier, most demoted from A/B by the rolling 7-day drawdown guard (`stocks_intraday_7d_drawdown_guard`) — correctly so, since stocks signal-stats show longs at PF 0.41 / −16R over the week while shorts run PF 1.93. **UNH is the standout risk item**: a legal/headline-risk flag (DOJ Medicare-billing criminal + civil probe, confirmed both internally — multiple dated sources 2026‑07‑06/07 — and externally via CNBC/The Hill) sits alongside a **data-integrity anomaly**: `PAPER_MONITOR_STATUS_LATEST.md` flags today's UNH long (stocks/intraday/C) as `STATUS NEEDS REVIEW — inconsistent lifecycle fields`. Forced verdict: **AVOID / MANUAL REVIEW REQUIRED**.

**VANRY/USDT is the "don't chase" case of the run.** It's the #1 momentum/RS leader across every crypto report today (score 100, 24h +18–23%, RS vs BTC +21–23%, vol 3–4x) and anchors the `binance_ecosystem`-adjacent `momentum_breakout` narrative basket, but external research (CoinGabbar, 2026‑07‑07) shows the rally is a **short squeeze** (>$1.1M shorts liquidated July 7) happening **under an active Binance "Monitoring Tag"** placed ~July 3 for listing-standards concerns — a real overhang not present in the internal report. It is C-tier / watchlist-only, never entered a proposed_signal. Treat as catalyst-watch-with-caution, wait for a pullback into structure, not a chase.

**Catalyst mapping is weak this run**: 3,070/3,841 events unmapped (79.9%) — use catalyst layer as context, not a final-decision input.

**Overall verdict: CAUTION / WATCH_ONLY.** Crypto regime is bearish/risk-off (short bias favored, book aligned); the one open crypto long (SPELL) and one open short book (BTC/ETH swing, tp1_hit already) are working as designed. Stocks: nothing actionable, drawdown guard doing its job — do not fight it.

---

## 2. Data Used

External web research used this run (WebSearch, 2 queries; WebFetch, 2 fetches — 1 succeeded [CoinGabbar/VANRY], 2 blocked with HTTP 403 [CNBC, The Hill — paywalled/bot-blocked, used search-result summaries instead]).

| Source | File / Query | Age at 21:41 EEST | Quality |
|---|---|---|---|
| Scalp report | `2026-07-08_16-39_scalp_report.md` (gen 19:39 EEST) | ~2h02m | usable, no A/B this cycle anyway |
| Intraday report | `2026-07-08_16-45_intraday_report.md` (gen 19:45 EEST) | ~1h56m | usable |
| Swing report | `2026-07-08_12-38_swing_report.md` (gen 15:38 EEST) | ~6h03m | **CARRY-FORWARD** (4–12h band) — flagged, consistent direction with fresher reports |
| Stocks intraday | `2026-07-08_18-27_stocks_intraday_report.md` (gen 21:27 EEST) | ~14m | FRESH |
| Stocks swing/invest | `2026-07-02_13-0x_stocks_{swing,invest}_report.md` | ~6 days | **STALE** — excluded from swing/invest final verdict; nothing fresher exists (per rule, still referenced for continuity, not for a fresh decision) |
| Catalyst events / baskets | `data/catalysts/2026-07-08/catalyst_events.jsonl` (3,841 events), `narrative_baskets.jsonl` (3 baskets), `catalyst_cycle_16-46.md` | ~55m (last cycle write 19:46) | FRESH |
| LLM packets | `data/processed/llm_analysis_packet.md`, `llm_stocks_packet.md` | not separately re-read this cycle (superseded by fresher mode reports read directly) | n/a |
| Paper monitor status | `reports/PAPER_MONITOR_STATUS_LATEST.md` | mtime 19:57 EEST, ~1h44m | authoritative operator-vocabulary source for lifecycle status |
| Previous review | `OPUS_ENRICHED_REVIEW_AUTO_2026-07-08_1840.md` | ~3h01m | compared in §4 |
| DB queries | `active-signals`/`signal-stats` CLI (crypto+stocks) + direct read-only SQL on `proposed_signals`, `news_items`, `funding_snapshots` | live | used to work around CLI table truncation |
| Untracked legacy alerts | `detect_untracked_legacy_alerts --since 2026-07-08` | live | 0 found |
| External: UNH | CNBC (2025‑07‑24), The Hill (search summary; date unavailable via fetch, both 403-blocked on direct fetch) | live search | corroborates internal DOJ-probe record; **confirms** |
| External: VANRY | CoinGabbar, "Crypto Market Movers Today: VANRY Jumps 49%…", 2026‑07‑07 (fetched directly, 200 OK) | live | adds Binance Monitoring Tag + short-squeeze context **not present internally**; **confirms + weakens** the momentum thesis (chase risk) |

**Notes**: TradingView / manual chart check unavailable — all technical levels are from local OHLCV/ATR/EMA and DB fields. Onchain and social-attention feeds remain missing (longstanding, unchanged).

---

## 3. Scheduler / Data Freshness

- **Last completed cycle**: `cycle_02_17-42_summary.md` present; latest reports (stocks intraday 21:27, crypto scalp/intraday ~19:39–19:45, catalyst cycle 19:46) are all well under 3h old. Per dispatch instructions, freshness is confirmed — **not deferred**.
- **Paper monitor status** (`PAPER_MONITOR_STATUS_LATEST.md`, mtime 19:57 EEST, ~1h44m old — the single most useful lifecycle source this run):
  - OPEN actionable: **1** (SPELL/USDT long, crypto/intraday/B — entry filled, monitoring TP/SL)
  - WAITING for entry: **1** (NEAR/USDT short, crypto/swing/B — entry not touched yet)
  - Review/Shadow: **139** (all stocks C-tier + crypto scalp signals, not actionable by policy)
  - Entered unresolved (expired-after-entry, NOT missed entries): **17**
  - No-entry / stale / moved-away: **34**
  - Closed: **384 WIN / 72 LOSS / 0 FLAT**
  - Needs review (inconsistent): **1** — **UNH long (stocks/intraday/C)**, ambiguous lifecycle fields (see §7 candidate #1 and §14 TODO)
- **Untracked legacy crypto alerts**: **0** — stable, same as prior review.
- **Crypto week signal-stats (A/B headline, reliable, n=434)**: triggered 416, winrate 14.7%, PF **1.4352**, avgR 0.1235, totalR **+36.56**. By mode: swing PF 1.91/avgR +0.31 (working), intraday PF 1.64/avgR +0.19 (working), **scalp PF 0.44/avgR −0.12, totalR −11.8 (net-negative, longstanding, not new — consistent with the scalp report's own "low confidence" banner)**. Weekend-mode continues to underperform (14% WR, n=164) — tracked, not new.
- **Stocks week signal-stats (A/B headline, weak confidence, n=18)**: triggered 18, winrate **0%**, PF 0.0, totalR −3.0. Direction split is the notable new-ish read: shorts PF 1.93/+4.6R (n=62) vs longs PF 0.41/−16.0R (n=148) — **longs are the problem, not shorts**. C-tier (reliable, n=192): winrate 9%, PF 0.71 (below 0.8) — confirms C-tier correctly stays non-actionable.
- **Live prices (funding_snapshots, ~2h old, Binance)**: BTC $61,982.81 (16:41 UTC), ETH $1,734.56 (16:42 UTC). Both funding positive, long/short ratio elevated (BTC 1.82, ETH 2.09 — longs crowded), consistent with "deleveraging / long liquidation" derivatives read in the reports. No acute squeeze risk flagged against the open shorts.

---

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-07-08 21:39 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["onchain", "social_attention", "orderbook_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing report ~6h03m old (carry-forward band)", "stocks swing/invest reports ~6 days old (stale, excluded)", "catalyst mapping 20.1% (79.9% unmapped)"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["risk_off", "shorts_preferred", "chop"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: BTC/ETH trend transition_down, altcoin breadth 17% above EMA20, style=short bias or no trade", "stocks: regime label chop, bias neutral, VIX 16.71, breadth20 50%/breadth50 100%"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["mapping_weak", "stale_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["3841 events today, 771 mapped (20.1%)", "3 active baskets: binance_ecosystem_teaser (BNB, <1h), perps_dex_narrative (HYPE, <6h), momentum_breakout (VANRY/NFP, <1h)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["oi_supports", "funding_extreme"],
      "data_missing": ["liquidation_heatmap", "orderbook_depth"],
      "suggested_effect": "advisory_only",
      "facts_used": ["BTC funding +0.0081%, L/S 1.82 (longs crowded)", "ETH funding +0.0046%, L/S 2.09 (longs crowded)", "VANRY: external report of >$1.1M short-squeeze liquidation July 7, active Binance monitoring tag since ~July 3"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["stale_before_entry", "overextended", "entry_late"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["VANRY 24h +18-23%, RS+21-23%, reversed from -18% short-bias 6h earlier — parabolic, overextended", "BTC scalp short entry 62118-62308 vs live 61982.81 — already tracking toward TP1, not near invalidation"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "normal",
      "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "needs_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["OPEN=1 (SPELL long)", "WAITING=1 (NEAR swing short)", "REVIEW/SHADOW=139 (incl. all 4 crypto scalp triggers)", "ENTERED_UNRESOLVED=17", "NO_ENTRY=34", "NEEDS_REVIEW=1 (UNH intraday/C, inconsistent lifecycle)"]
    },
    {
      "agent": "risk_manager",
      "verdict": "manual_review",
      "confidence": 0.7,
      "reason_codes": ["legal_risk", "manual_review", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["UNH: DOJ criminal+civil Medicare-billing probe (internal 2026-07-06/07 + external CNBC/The Hill), plus NEEDS_REVIEW lifecycle flag on today's UNH long", "scalp shorts (BTC/ETH/SOL/NEAR) are policy-gated REVIEW/SHADOW, not live risk despite DB 'triggered' status", "stocks longs PF0.41/-16R vs shorts PF1.93/+4.6R this week — drawdown guard correctly suppressing new stocks longs"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto swing PF1.91 / intraday PF1.64 working; crypto scalp PF0.44 net-negative (-11.8R), longstanding known issue", "stocks A/B n=18 weak-confidence sample, PF0.0; stocks C-tier PF0.71 below 0.8"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["wait_for_trigger", "reduce_risk", "manual_review"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all 8 above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "shorts",
    "best_long_candidate": {"symbol": "SPELL/USDT", "trigger": "already OPEN (entry filled ~0.0001015-0.00010635); manage existing position toward TP1 0.00011926, stop 0.00009558", "reason": "only genuinely open actionable long in the book; note thesis assumed 'bullish trend' at entry (2026-07-07) vs today's 'bearish trend (risk-off)' regime — contradiction risk, tighten management, don't add"},
    "best_short_candidate": {"symbol": "NEAR/USDT", "trigger": "WAITING — swing/B short, entry zone ~1.883-1.896, invalidation 1.911; enter only on confirmed entry touch, news-supported", "reason": "only clean WAITING-for-entry candidate; aligned with bearish regime and BTC/ETH short book already tp1_hit"},
    "best_catalyst_candidate": {"symbol": "VANRY/USDT", "trigger": "wait for pullback into 0.0060-0.0067 retest zone (per swing watchlist); do not chase the +18-23% spike", "reason": "top RS/momentum leader and narrative-basket primary, but external research shows the rally is a short squeeze under an active Binance monitoring tag — catalyst-watch only, high chase risk right now"},
    "avoid_candidate": {"symbol": "UNH", "reason": "DOJ Medicare-billing criminal+civil probe (confirmed internal+external) plus a live data-integrity NEEDS_REVIEW flag on today's UNH long lifecycle — forced AVOID/MANUAL REVIEW regardless of technical score"},
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 4
  }
}
```

---

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | caution | 0.70 | scheduler_fresh, report_stale (swing carry-forward), catalyst_missing | advisory_only |
| market_regime | caution | 0.75 | risk_off, shorts_preferred, chop (stocks) | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, stale_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.55 | oi_supports, funding_extreme (longs crowded) | advisory_only |
| technical_entry | caution | 0.60 | stale_before_entry, overextended, entry_late | advisory_only |
| execution_lifecycle | normal | 0.80 | open_actionable, waiting_for_entry, review_shadow, needs_review | advisory_only |
| risk_manager | manual_review | 0.70 | legal_risk, manual_review, reduce_risk | advisory_only |
| playbook_performance | caution | 0.65 | playbook_working (swing/intraday), playbook_failing (scalp), low_sample (stocks A/B) | advisory_only |
| head_trader | caution | 0.65 | wait_for_trigger, reduce_risk, manual_review | advisory_only |

---

## 4. What Changed vs Previous Review (18:40 EEST)

- **Crypto book thinned out**: previous review had 3 OPEN actionable (BTC swing short, ETH swing short, SPELL intraday long) + 1 WAITING (NEAR swing short). Now only **1 OPEN** (SPELL) + **1 WAITING** (NEAR, unchanged) — BTC/ETH swing shorts have moved to `tp1_hit` (partial win, no longer counted as freshly "OPEN" in the monitor's group, they're progressing/closed-partial). **Confirmed working as designed**, not a concern.
- **New**: crypto scalp cohort (BTC/ETH/SOL/NEAR shorts) triggered this cycle (created 15:42–16:56 UTC) — all policy-gated REVIEW/SHADOW, not actionable. Two are inside minutes of window close (SOL 18:47:33 UTC, BTC/NEAR 18:56:29 UTC); ETH has ~1h12m left (19:56:15 UTC).
- **New TODO surfaced**: UNH intraday/C long flagged `NEEDS_REVIEW — inconsistent lifecycle fields` in the monitor status (was not present/flagged in the 18:40 review). Escalates UNH from "known legal-risk name" to an active data-integrity item.
- **JPM contradiction from 18:40 review persists but is now stale context**: JPM short (C-tier, was flagged bullish-fundamentals-vs-technical-short contradiction) is still C-tier/demoted this cycle (drawdown guard) — same non-actionable status, not re-verified externally this run (no material change expected within 3h, and it's not Telegram-actionable either way).
- **Catalyst mapping**: 20.1% mapped this run (771/3,841) vs 20.3% (previous review) — essentially unchanged, still weak, still a tracked longstanding issue (see TODO carried forward).
- **Thesis changes**: crypto short bias **confirmed continuing** (BTC/ETH progressing in favor). Stocks: still no A/B book — **confirmed**, unchanged. VANRY newly identified as a chase-risk / short-squeeze name this run (external research not done on it in the 18:40 review).

---

## 5. Catalyst Coverage

- Total catalyst events today (cumulative, `catalyst_events.jsonl`): **3,841**
- Mapped (non-null symbol): **771** (20.1%)
- Unmapped: **3,070** (79.9%)
- Narrative baskets active: **3** — `binance_ecosystem_teaser` (primary BNB/USDT, fresh <1h), `perps_dex_narrative` (primary HYPE/USDT, fresh <6h), `momentum_breakout` (primary VANRY/USDT + NFP/USDT, fresh <1h)

**Catalyst mapping weak this run — use catalyst layer as context, not final-decision input.**

Top 3 unmapped headlines (sample):
1. "/C O R R E C T I O N -- Vinitaly.USA/" (PR Newswire) — off-topic wire correction, not tradable.
2. "Switzerland advances to World Cup quarterfinals after penalty win over Colombia" — sports, not tradable.
3. "Russia advances crypto regulation bill, allowing foreign trade use" — potentially relevant macro/crypto-regulatory item that is currently unmapped to any symbol; worth a human spot-check (not urgent, no immediate price-actionable read).

No NULL-symbol catalyst events with importance ≥0.75 were found (0 count) — the unmapped pile is mostly noise, not high-importance headlines silently dropped.

---

## 6. Market Landscape

### Market Mood / Risk Routing
- **Crypto mood**: bearish trend / risk-off. BTC and ETH both `transition_down`; altcoin breadth only 17.0% above EMA20 (29.8% above EMA50). Recommended style per the desk's own regime read: "short bias or no trade; avoid weak altcoin longs." Funding positive with longs crowded (BTC L/S 1.82, ETH L/S 2.09) — consistent with further downside pressure if long unwind continues, not an acute short-squeeze setup against the open shorts.
- **Stocks mood**: chop, neutral bias. VIX 16.71 (calm), breadth mixed (50% above EMA20, 100% above EMA50 — index-level uptrend but shallow breadth). Sector rotation: healthcare/financials/utilities strong, energy weak, tech/communications mixed-to-weak.
- **Dominant narrative**: crypto — momentum/RS-leader rotation (VANRY, NFP) without durable catalyst backing (both flagged "pure momentum cluster, no confirmed news"); Binance-ecosystem teaser (BNB) fresh <1h. Stocks — legal/headline risk (UNH DOJ probe) is the dominant single-name story; broader tape is quiet/chop into the close.
- **Preferred side now**: crypto shorts (regime-aligned, working book); stocks — no directional preference, wait-for-trigger only (book is empty of A/B).
- **Best long candidate**: SPELL/USDT (already open, manage don't add — see contradiction note in §7).
- **Best short candidate**: NEAR/USDT (WAITING for entry, swing/B, news-supported, aligned with regime).
- **Best catalyst-backed candidate**: VANRY/USDT — wait for pullback, do not chase the current spike (short-squeeze + exchange monitoring-tag overhang).
- **What to avoid**: UNH (legal risk + lifecycle data inconsistency); chasing VANRY at the highs; adding to crypto scalp shorts (policy-gated shadow only, and 3 of 4 are about to age out of their window).
- **What would change the view**: a confirmed VANRY pullback into the 0.0060-0.0067 zone with basket confirmation would upgrade it from catalyst-watch to a real setup; a clean UNH lifecycle-status fix plus no further legal escalation would allow LLY/UNH-adjacent healthcare longs back into consideration; BTC reclaiming local resistance would invalidate the crypto short thesis and should trigger a re-review before the next scheduled slot.

---

## 7. Candidate Deep Dives

### 1. UNH (stocks) — LEGAL/HEADLINE RISK — AVOID / MANUAL REVIEW REQUIRED
- **Setup**: today's UNH long (stocks/intraday/C, score ~43 in the rejected list this cycle — no_directional_setup) is flagged by `PAPER_MONITOR_STATUS_LATEST.md` as `STATUS NEEDS REVIEW — inconsistent lifecycle fields` (touched=True, alerted=False, "ambiguous lifecycle — needs review"). This is a genuine system-integrity anomaly, not a trade thesis.
- **Legal/headline risk**: DOJ criminal + civil investigation into Medicare Advantage billing practices (inflated risk scores/diagnoses). Confirmed internally (`news_items`: CBS News, Yahoo Finance, The Globe and Mail/QuiverQuant, published 2026‑07‑06/07) and externally (CNBC, dated 2025‑07‑24, confirms the probe originated mid-2025 and has continued; The Hill, corroborating). Production risk-warning layer already tags UNH `block_requires_operator_review` for legal_risk.
- **Verdict**: **AVOID / MANUAL REVIEW REQUIRED**. Not Telegram-actionable (C-tier), but a human should resolve the lifecycle inconsistency before this name is trusted in any future A/B consideration.
- **Chase/price-reaction check**: N/A — no active entry; TradingView/manual chart check unavailable, no OHLCV chase read attempted given the legal override.

### 2. Crypto B-tier scalp short cohort — BTC/ETH/SOL/NEAR — REVIEW/SHADOW, late-session exposure check
- **Setup**: 4 scalp-mode short signals (all B-tier, all bearish-regime-aligned), created 15:42–16:56 UTC, 2h validity windows. DB `status='triggered'` for all four, but `PAPER_MONITOR_STATUS_LATEST.md` classifies them **REVIEW/SHADOW — not actionable by policy (C-tier / scalp / shadow)**, i.e. scalp mode is policy-gated regardless of tier. This matches the scalp report's own banner: "CRYPTO SCALP — low confidence... PF 0.14 [14d], treat with lower confidence than intraday/swing."
- **Levels**: BTC entry 62118–62308 / stop 62540.54 / TP1 61611.88 (live price 61982.81 — tracking toward TP1, not near invalidation). ETH entry 1735.41–1741.83 / stop 1749.69 / TP1 1718.27 (live 1734.56 — near entry, working). SOL and NEAR windows expire within minutes of this review (18:47:33 and 18:56:29 UTC respectively) — about to age into NO-ENTRY/STALE if unresolved.
- **Playbook performance**: scalp mode is net-negative over the trailing week (PF 0.44, avgR −0.12, totalR −11.8R, n=161) — a known, longstanding weak spot, not a new anomaly.
- **Verdict**: **WATCH ONLY / SCANNING** — these are shadow-lane data collection, not live risk. Do not treat as tradable even though price action is currently favorable for the shorts (aligned with the bearish regime).

### 3. SPELL/USDT (crypto) — OPEN actionable long, thesis/regime contradiction
- **Setup**: intraday/B long, entry filled 0.0001015–0.00010635 (created 2026‑07‑07T19:01:15, expires 2026‑07‑08T23:49:44 — ~2h remaining vs this review's 21:41 EEST / 18:41 UTC dispatch time). Stop/invalidation 0.00009558, TP1 0.00011926, TP2 0.00013003, TP3 0.00014079. This is the **only** genuinely OPEN actionable position in the entire book right now.
- **Contradiction risk**: the signal's own thesis text states "long continuation/pullback setup while the desk classifies the market as **bullish** trend" — that was true when it was created (2026‑07‑07), but every report generated today classifies the regime as **bearish trend (risk-off)**. This is a stale-thesis-vs-current-regime mismatch worth flagging for a human, though it does not itself invalidate the trade (price levels are what matter for management).
- **Chase/price-reaction check**: TradingView/manual chart check unavailable; no fresher OHLCV pulled for SPELL this cycle beyond the entry/stop/TP fields above.
- **Verdict**: **MANAGE, DO NOT ADD**. Let the existing position run to its stop/TP/window; do not treat the stale "bullish" framing as a reason to size up given today's bearish regime read.

### 4. VANRY/USDT (crypto) — catalyst/momentum leader, chase-risk, external short-squeeze context
- **Setup**: #1 RS/momentum symbol across scalp/intraday/swing reports all day (score 100, 24h +18.5–20.1%, RS vs BTC +21.5–23.5%, volume 3.3–4.0x). Primary symbol in the `momentum_breakout` narrative basket (fresh <1h) and in the crypto expansion watchlist ("ready-for-promotion", catalyst_backed). **Not** in any proposed_signal — C-tier/watchlist only, never actionable.
- **External verification** (CoinGabbar, 2026‑07‑07, fetched directly): the rally is explicitly characterized as a **short squeeze** — "over $1.1 million in short positions wiped out" — occurring while **Binance has VANRY under a "Monitoring Tag"** (placed ~July 3, 2026, for listing-standards/liquidity/regulatory concerns; not a delisting decision, but the article notes similar tags have preceded double-digit drawdowns for other tokens). This overhang is **not present anywhere in the internal reports**.
- **Reversal context**: the swing report (6h-old snapshot, data cut ~09:xx UTC) had VANRY with a **short bias**, 24h −18.14%, RS vs BTC −16.01% — meaning the symbol flipped from deeply red to strongly green intraday, consistent with a squeeze, not organic accumulation.
- **Verdict**: **CATALYST-WATCH WITH CAUTION, NOT A CHASE**. Wait for a pullback/retest into the 0.0060–0.0067 conditional zone flagged in the swing watchlist idea; treat the exchange monitoring tag as an active headline risk on any long thesis until resolved.

### 5. LLY (stocks) — was A-tier, demoted by drawdown guard, contrast case
- **Setup**: score 84.65, raw tier A, **demoted to C** by `stocks_intraday_7d_drawdown_guard` + `stocks_intraday_long_guard` (rolling paper-R drawdown guard on stocks-intraday longs). No legal/headline risk found — news this week is positive (record-high mentions, Motley Fool bullish pieces).
- **Why it matters**: this is the cleanest illustration this cycle of the drawdown guard doing its job — stocks-intraday longs are running PF 0.41/−16R over 30d (per §9 of the stocks intraday report), so even a technically-strong A-tier score is correctly suppressed system-wide rather than cherry-picked.
- **Verdict**: **NEEDS REVIEW (system-level, not name-level)** — not a UNH-style avoid, just correctly gated. A human could consider whether the global drawdown guard should ever allow a single strong exception, but that's a scoring/gating decision outside this review's advisory scope.

*(6 candidates were in scope per priority order; 5 selected as the strongest read. Runner-up not covered in depth: BNB/USDT — catalyst_backed, C-tier, "ready-for-promotion", primary of the fresh `binance_ecosystem_teaser` basket — folded into the VANRY discussion as the same narrative family, not a separate deep dive to stay within the 5-candidate cap.)*

---

## 8. Best Candidates Ranked

1. **Long-watch: SPELL/USDT** — already OPEN, manage to TP1 0.00011926 / stop 0.00009558, window closes ~23:49 UTC. Do not add size given the stale-bullish-thesis-vs-current-bearish-regime mismatch.
2. **Short-watch: NEAR/USDT** — WAITING for entry, swing/B, entry zone ~1.883–1.896, invalidation 1.911, news-supported. Enter only on confirmed touch.
3. **Catalyst-watch: VANRY/USDT** — do not chase the current spike; watch for pullback into 0.0060–0.0067 with basket/RS confirmation; treat the Binance monitoring tag as an active overhang.
4. Secondary short-watch (shadow-lane only, not actionable): BTC/USDT and ETH/USDT scalp shorts — tracking favorably but policy-gated, informational only.

No blanket "no clean candidates" — even in a thin, quiet late-session book, SPELL/NEAR/VANRY give one manage, one wait-for-trigger, and one catalyst-watch-with-caution.

---

## 9. Avoid / No Trade

*(This decision window only — advisory, never "stop the system".)*

- **UNH** — legal/headline risk (DOJ probe) + active lifecycle data-integrity flag. AVOID / MANUAL REVIEW.
- **VANRY/USDT at current price** — short-squeeze rally under an active exchange monitoring tag; avoid chasing, wait for the pullback zone.
- **New stocks-intraday longs generally** — the 7d drawdown guard is correctly suppressing this cohort (PF 0.41/−16R); do not override it manually this window.
- **Crypto scalp mode generally** — net-negative playbook (PF 0.44/−11.8R, 14d); shadow-lane data collection only, not a trading recommendation regardless of individual trigger direction.

---

## 10. Main Risks

- **Late-session exposure**: SPELL/USDT is the only live open risk; NEAR/USDT is a clean pending entry. Both are small, single-name, non-overlapping exposure — no correlation-cluster concern this window.
- **Data quality**: crypto swing report is 6h-old (carry-forward band, not stale) but still the basis for the NEAR WAITING signal's original context; direction is corroborated by fresher scalp/intraday reports so treated as reliable.
- **Catalyst mapping weak** (79.9% unmapped) — reduces confidence in catalyst-backed reasoning generally this cycle; used as context only.
- **UNH lifecycle inconsistency** — a live data-integrity bug, not just a legal-risk name; flagged to TODO.
- **Stocks longs underperforming** (PF 0.41/−16R, 30d) — guard is handling it, but worth continued monitoring if the guard is ever loosened.
- **WebFetch partial failure**: 2 of 3 external fetches (CNBC, The Hill) were blocked (HTTP 403); relied on WebSearch summaries for those two citations instead of full-article confirmation — lower-confidence than a direct fetch but multiple independent outlets agree, and internal news_items independently corroborate the same story.

---

## 11. Action Plan — next 4 hours

1. Let SPELL/USDT run to TP/stop/window close (~23:49 UTC / ~02:49 EEST) — no action needed, monitor only.
2. Watch NEAR/USDT for a confirmed entry touch in the 1.883–1.896 zone; if triggered, it's aligned with the current regime and existing short book.
3. Do not chase VANRY/USDT; re-check for a pullback into 0.0060–0.0067 at the next scheduled slot (~23:30 EEST / 04:30 EEST window, whichever comes first per the 6-slot cadence).
4. No action on UNH beyond the TODO below — it is not Telegram-actionable and the legal risk already suppresses it.
5. Re-verify at the next slot whether the SOL/NEAR/BTC scalp windows have closed and been correctly reclassified NO-ENTRY/STALE (ties to the TODO-eth-scalp-stale pattern from the prior review — watch for a repeat).

---

## 12. Final Verdict per Mode

- **Crypto scalp**: shadow/watch only — net-negative playbook, policy-gated non-actionable regardless of today's favorable direction.
- **Crypto intraday**: working (SPELL open, tracking; ETH intraday short tp1_hit) — manage existing, aligned with risk-off regime.
- **Crypto swing**: working (BTC/ETH shorts tp1_hit; NEAR short is the clean fresh watch idea) — carry-forward data band, direction corroborated by fresher reports.
- **Stocks intraday**: no A/B book — C-tier only, drawdown guard correctly active on longs; watch-only.
- **Stocks swing/invest**: data stale (~6 days, no fresher report exists) — excluded from a fresh verdict this cycle; do not treat as current.
- **Overall**: **CAUTION / WATCH_ONLY** — routed toward crypto shorts / manage-existing-long, not a blanket no-trade.

---

## 13. Sources

- [UnitedHealth facing DOJ investigation over Medicare billing — CNBC (2025-07-24)](https://www.cnbc.com/2025/07/24/unitedhealthcare-doj-investigation-medicare-billing.html) — confirms internal legal-risk record (fetch blocked HTTP 403; used search-result summary)
- [UnitedHealth acknowledges DOJ investigation into Medicare billing — The Hill](https://thehill.com/policy/healthcare/5418393-unitedhealth-doj-investigation-medicare-billing/) — corroborates (fetch blocked HTTP 403; used search-result summary)
- [Crypto Market Movers Today: VANRY Jumps 49% as YFI Rebounds on July 7 — CoinGabbar](https://www.coingabbar.com/en/crypto-currency-news/crypto-market-movers-today-vanry-edgex-yearn-ansem-monad-rally) — confirms momentum move, adds Binance monitoring-tag + short-squeeze context (fetched directly, 200 OK)
- Internal: `data/catalysts/2026-07-08/catalyst_events.jsonl`, `narrative_baskets.jsonl`, `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items`, `funding_snapshots`), `reports/PAPER_MONITOR_STATUS_LATEST.md`

---

## 14. Fix Requests / TODO

### TODO-unh-lifecycle-needs-review
- **issue**: today's UNH long (stocks/intraday/C) is flagged by `PAPER_MONITOR_STATUS_LATEST.md` as `STATUS NEEDS REVIEW — inconsistent lifecycle fields` (touched=True, alerted=False, "ambiguous lifecycle").
- **evidence**: `reports/PAPER_MONITOR_STATUS_LATEST.md` (mtime 2026-07-08 19:57 EEST), UNH long stocks/intraday/C line item.
- **suggested manual fix**: a human session should inspect the underlying `proposed_signals`/execution-tracking row for this UNH signal to determine why lifecycle fields are inconsistent (likely touched=True but no resolved status) and whether this is a one-off or systematic for signals colliding with a legal-risk `block_requires_operator_review` tag.
- **priority**: medium
- **first observed**: 2026-07-08 21:39 EEST

### TODO-crypto-stock-symbol-crosstagging
- **issue**: the crypto scalp/intraday/swing reports' "Structured Catalyst / Narrative" sections list catalyst notable-events under the symbol `UNH/USDT` — UNH is a stock ticker (UnitedHealth), not a crypto trading pair. This looks like a symbol-mapping bug where a stock-related legal_risk headline is being cross-tagged onto a synthetic "UNH/USDT" crypto symbol.
- **evidence**: `data/reports/scalp/2026-07-08_16-39_scalp_report.md` §5b, `data/reports/intraday/2026-07-08_16-45_intraday_report.md` §5b — "UNH/USDT [legal_risk] UnitedHealth stock sinks 4.7%…" appearing in the crypto catalyst section.
- **suggested manual fix**: review the catalyst symbol-resolver for cases where a stock ticker is being appended with "/USDT" and routed into the crypto catalyst pipeline instead of being filtered to stocks-only.
- **priority**: low
- **first observed**: 2026-07-08 21:39 EEST (likely present in earlier cycles too, not previously flagged in the two prior reviews read this session)

### TODO-rivian-headline-crosstagged-gs-jpm-ms
- **issue**: the identical headline "Rivian Shares Drop After News Of 75 Million Share Public Offering (Yahoo Finance Top Stories)" is applied as an `offering_dilution` risk_warning to three unrelated tickers — GS, JPM, and MS — none of which is Rivian (RIVN). This looks like an entity-extraction/symbol-cross-tagging bug in the news-risk pipeline rather than three separate real dilution events.
- **evidence**: `data/reports/stocks/intraday/2026-07-08_18-27_stocks_intraday_report.md` §"Production risk warnings" — GS, JPM, MS all carry the identical Rivian headline.
- **suggested manual fix**: review the entity-linking step that attaches risk_warning tags to tickers co-mentioned or embedding-matched near a headline; confirm GS/JPM/MS have no genuine standalone dilution story before trusting this risk flag for any of the three.
- **priority**: medium
- **first observed**: 2026-07-08 21:39 EEST (also present in the 18:40 review's underlying data, not previously flagged)

### TODO-catalyst-mapping-persistently-weak (carried forward)
- **issue**: catalyst symbol-mapping rate has been ~20% for at least three consecutive review cycles now (20.8% at 16:20, 20.3% at 18:40, 20.1% at 21:39) — stable but persistently well below the 50% weak threshold.
- **evidence**: `data/catalysts/2026-07-08/catalyst_events.jsonl` — 3,841 events, 771 mapped this run.
- **suggested manual fix**: unchanged from prior reviews — a human session should review the symbol resolver for common unmapped patterns; this run's unmapped sample was again mostly off-topic noise (sports, wire corrections), so likely not silently dropping tradable headlines, but should be confirmed rather than assumed.
- **priority**: medium
- **first observed**: tracked across multiple cycles; reconfirmed 2026-07-08 21:39 EEST

### TODO-telegram-send-skipped
- **issue**: no pre-approved, safe, code-free CLI entry point for sending an ad-hoc compact Telegram message was found within this run's permission scope. `src/notifiers/telegram.py` exposes a `TelegramNotifier.send()` method, but invoking it requires writing/running Python that imports production notifier code with live bot credentials — outside the explicitly whitelisted read-only CLI command list for this routine.
- **evidence**: searched `scripts/*.py` and `src/notifiers/telegram.py`; no standalone `send-telegram-message`-style script or CLI subcommand accepting an arbitrary text blob was found.
- **suggested manual fix**: if compact Telegram summaries are desired for this review slot going forward, add a narrow, explicitly-whitelisted CLI command (e.g. `python -m src.cli notify-telegram --text "..."`) that the permission contract can safely allow-list without granting broader notifier code access.
- **priority**: low
- **first observed**: 2026-07-08 21:39 EEST (same gap likely present in prior automated review cycles, not previously logged as a TODO)
