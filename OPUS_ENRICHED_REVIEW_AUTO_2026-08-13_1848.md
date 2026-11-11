# Opus Enriched Review — US open reaction review — Auto Cycle 18:48 EEST

## 1. Executive Summary
US-open-reaction slot, ~2h20m into RTH. **Advisory only — no auto-trade.** Crypto regime is range/chop (neutral, conf 100) with a persistent macro risk-off headwind (77/100) despite BTC +0.33% ($63,830) and mixed breadth (~55% above EMA20/50, 48.7% outperforming BTC). Stocks are cleanly bullish — SPY/QQQ uptrend, VIX 14.68, tech (XLK) leading. The standout finding this cycle is **internal book vs. tape contradiction**: the crypto signal book is ~92% long while at least two symbols (PROM/USDT, BICO/USDT) carry live LONG swing exposure against a market read of `bias=short`, deleveraging OI, and double-digit negative 24h moves; MMT/USDT has **simultaneous open LONG and SHORT swing signals**. No A-tier anywhere. Stocks A/B is 0-for-4 this week (−3R) — treat any fresh stocks A/B with extra scrutiny. AMAT reported earnings today; its only live signal is C-tier (non-actionable) but do not chase.

## 2. Data Used
- Scheduler: `data/scheduled_runs/2026-08-12_default_schedule/scheduler.log` (mtime 18:37 EEST, fresh)
- Latest cycle summary: `cycle_07_16-20_summary.md` (16:20 EEST)
- Reports: swing `2026-08-13_15-07` (llm packet gen 18:07 local), intraday `2026-08-13_13-43`, scalp `2026-08-13_13-35`, stocks intraday `2026-08-13_15-27` (18:27 local, 21 min old)
- `data/processed/llm_analysis_packet.md` (crypto, 18:07 local) and `llm_stocks_packet.md` (stocks, 17:27 local)
- `data/catalysts/2026-08-13/catalyst_events.jsonl` + `catalyst_cycle_13-52.md` + `narrative_baskets.jsonl`
- CLI: `active-signals` (crypto, stocks), `signal-stats` (crypto, stocks), `detect_untracked_legacy_alerts --since 2026-08-13`
- Direct read-only SQL against `db/crypto_ai_desk.sqlite` (`proposed_signals`, `watchlist_alerts`) for lifecycle counts and contradiction checks — no writes
- Prior review: `OPUS_ENRICHED_REVIEW_AUTO_2026-08-13_1558.md` (pre-US-open, 15:58 EEST)

## 3. Scheduler / Data Freshness
- Scheduler: **fresh** (log + latest cycle both < 3h old — no defer triggered).
- Crypto reports: scalp/intraday ~2h old (fine for intraday cadence), swing ~40 min old (fresh).
- Stocks intraday report: 21 min old (fresh, mid-RTH).
- Stocks swing/invest: last touched 2026-07-02 — these modes are **deprecated/removed per prior sign-off** (replaced by the shadow-only `stocks_swing_growth_breakout` framework); not a freshness bug, excluded from this review by design.
- Catalyst layer: current cycle `catalyst_cycle_13-52.md` (16:52 local), fresh.
- `detect_untracked_legacy_alerts`: **clean** — no untracked crypto watchlist alerts without a backing `proposed_signal`.
- Monitor note: latest `pending_monitor` log shows 4× `tracker:OperationalError` (retried) and 1× `PermissionError: [WinError 5]` on worker recycle — low frequency, not blocking, logged as TODO-monitor-recycle-error below.

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "us_open_reaction",
  "as_of": "2026-08-13 18:48 EEST",
  "agents": [
    { "agent": "data_quality", "verdict": "ok", "confidence": 0.85,
      "reason_codes": ["scheduler_fresh", "report_stale"], "data_missing": ["stocks_swing_invest_deprecated"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 18:37", "stocks intraday report 18:27", "swing packet gen 18:07", "stocks swing/invest last 2026-07-02 (deprecated by design)"] },
    { "agent": "market_regime", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["mixed", "chop", "risk_off"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime range/chop neutral conf 100", "macro risk 77/100 risk-off headwind", "breadth 55% above EMA20/50, 48.7% outperform BTC", "stocks: SPY/QQQ uptrend, VIX 14.68, XLK RS +3.98%"] },
    { "agent": "catalyst_narrative", "verdict": "caution", "confidence": 0.5,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "no_catalyst"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["74.7% unmapped catalyst events today", "perps_dex_narrative basket fresh <1h (HYPE primary)", "momentum_breakout basket fresh <1h, no confirmed news (BTW/BANK/ATM)"] },
    { "agent": "derivatives_squeeze", "verdict": "bad", "confidence": 0.6,
      "reason_codes": ["oi_contradicts", "unwind"], "data_missing": ["MMT OI/funding not directly captured this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["PROM/USDT: price down + OI down -16.4% = long deleveraging/liquidation", "BICO/USDT: price down + OI down -10.25% = long deleveraging/liquidation", "PROM/BICO long/short ratio near 1.0/0.5 respectively"] },
    { "agent": "technical_entry", "verdict": "caution", "confidence": 0.55,
      "reason_codes": ["chase_risk", "overextended", "entry_late"], "data_missing": ["TradingView / manual chart check unavailable"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ATM/HOME/NBISB/AKE momentum leaders tagged overextended, 24h +10% to +50%", "PROM -26.31% 24h vs open long entries at 2.08-2.59"] },
    { "agent": "execution_lifecycle", "verdict": "caution", "confidence": 0.75,
      "reason_codes": ["open_actionable", "waiting_for_entry", "needs_review"], "data_missing": ["entered-unresolved vs no-entry split for expired rows not separately computed this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto: 46 triggered(B) + 17 tp1_hit(B) + 9 tp2_hit(B) + 1 waiting(B), all open-risk B-tier, 0 A-tier", "stocks: 20 triggered(C) + 6 waiting(C) + 12 tp1/tp2(B) + 150 tp1/tp2(C), 0 A/B triggered"] },
    { "agent": "risk_manager", "verdict": "caution", "confidence": 0.7,
      "reason_codes": ["correlation_cluster", "manual_review", "headline_risk"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["MMT/USDT simultaneous open long+short swing signals (sig_be8481b801a2506a long vs sig_6f5d3799c4e660c1 short)", "PROM/USDT two open longs vs bias=short/-26% tape", "AMAT earnings today, do_not_chase + block_requires_operator_review flags active", "XRP block_requires_operator_review (bridge exploit headline)"] },
    { "agent": "playbook_performance", "verdict": "caution", "confidence": 0.6,
      "reason_codes": ["playbook_failing", "low_sample", "playbook_working"], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto tier=B: PF 2.59, n=233, triggered-winrate 18% flagged low by system", "stocks A/B headline: sample=12, wins=0 losses=4 this week, PF=0, totalR=-3.0", "crypto MEXC-only exchange_confirmation: PF 7.5 n=18 (weak confidence, promising)"] },
    { "agent": "head_trader", "verdict": "ok", "confidence": 0.7,
      "reason_codes": [], "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all above"] }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.65,
    "preferred_side": "mixed",
    "best_long_candidate":     { "symbol": "ACE/USDT", "trigger": "already triggered/open, swing long, score 79.3 (highest live B score), catalyst-adjacent (RWA/exchange narrative cluster); manage existing risk, do not add on weakness", "reason": "highest-conviction live long by score with no tape contradiction found" },
    "best_short_candidate":    { "symbol": "MMT/USDT", "trigger": "the short leg (sig_6f5d3799c4e660c1) is already open and aligned with tape (bias=short, score 74.2, 24h -17.24%, overextended tag); the long leg on the same symbol should be reviewed for closure, not added to", "reason": "market-confirmed weak_vs_market + overextended read supports the short, contradicts the parallel long" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "perps_dex_narrative basket freshness <1h; no live signal yet — needs a confirmed pullback/retest entry per playbook wait_pullback before it becomes actionable", "reason": "freshest basket this cycle, playbook explicitly says wait for pullback, not chase" },
    "avoid_candidate":         { "symbol": "PROM/USDT", "reason": "two open LONG swing signals against a bias=short, -26.31% 24h, OI-down/deleveraging tape — worst book/tape contradiction this cycle; do not add, flag for manual review" },
    "operator_action": "manual_review",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 3
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.85 | scheduler_fresh, report_stale | advisory_only |
| market_regime | caution | 0.70 | mixed, chop, risk_off | advisory_only |
| catalyst_narrative | caution | 0.50 | mapping_weak, fresh_catalyst, no_catalyst | advisory_only |
| derivatives_squeeze | bad | 0.60 | oi_contradicts, unwind | advisory_only |
| technical_entry | caution | 0.55 | chase_risk, overextended, entry_late | advisory_only |
| execution_lifecycle | caution | 0.75 | open_actionable, waiting_for_entry, needs_review | advisory_only |
| risk_manager | caution | 0.70 | correlation_cluster, manual_review, headline_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_failing, low_sample, playbook_working | advisory_only |
| head_trader | ok | 0.70 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review (15:58 EEST, pre-US-open)
- **BANK/USDT** — was the previous long-watch (score 63.5, no fresh catalyst); now **confirmed**: live swing long hit tp2, and today's catalyst scan independently tags BANK/USDT inside the fresh `momentum_breakout` basket (+22.0% 24h). Thesis validated.
- **MMT/USDT** — was the previous short-watch (gated do-not-chase, >2 ATR extended); situation has **worsened, not resolved**: it now has a live open LONG (score 68.0) sitting alongside the live open SHORT (score 65.6) on the same symbol. This needs operator attention this cycle, not just a watch note.
- **XOM / COP / BX** (previous stocks long/catalyst candidates, RTH-confirmation required) — **none appear in today's fresh active-signals list**; no evidence they triggered or resolved this session. Not claiming they failed — just that there's no fresh follow-through data to confirm or deny this cycle.
- **TUT/USDT, HEI/USDT, ZBT/USDT, ACE/USDT** — previously flagged as "triggered status stale 4-7 days, system-integrity item." Still `triggered` now, 2.5h later. This is very likely normal swing-mode behavior (multi-day validity windows extending to 2026-08-14/17/18), not a new finding — carried forward as a low-priority data-quality note, not re-escalated without further evidence.
- **Crypto macro risk** improved slightly: 77/100 now vs 100/100 previously (same Iran/Hormuz/Ukraine themes, one fewer risk-off hit). BTC recovered from the prior downtrend read to +0.33% today.
- **New this cycle**: PROM/USDT and BICO/USDT book/tape contradictions were not flagged in the prior review — first observation this session.

## 5. Catalyst Coverage
- Catalyst events today: **2,500** total; mapped (has symbol) **633**, unmapped **1,867** → **74.7% unmapped**.
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.**
- Top 3 unmapped headlines by importance (all `legal_risk`, ticker-in-title but symbol not resolved — likely a resolver gap, see TODO):
  1. (0.75) "Futu Holdings Limited Investor Alert... Securities Fraud Lawsuit" — PR Newswire
  2. (0.75) "BTU Investors Have Opportunity to Lead Peabody Energy... Securities Fraud Lawsuit" — PR Newswire
  3. (0.75) "FSLR Investors Have Opportunity to Lead First Solar... Securities Fraud Lawsuit" — PR Newswire
  (Note: these read as standard law-firm "shareholder rights" solicitation boilerplate common after any stock decline — not confirmed material fraud findings; treat as noise unless corroborated.)
- Narrative baskets today (4): `binance_ecosystem_teaser` (BNB/ASTER, <6h), `perps_dex_narrative` (HYPE + DYDX/GMX/ASTER, **<1h**), `rwa_narrative` (ONDO/XLM, <6h), `momentum_breakout` (BTW/BANK/ATM, **<1h**, no confirmed news).
- Highest-importance mapped catalyst: ETH/USDT exploit_hack, importance 0.84 — PeckShield reports $25.6M hack, funds swapped to DAI/ETH (t.me/whale_alert_io, single_source, unverified beyond the one channel).

## 6. Market Landscape

### Market Mood / Risk Routing
- Crypto mood: **range/chop, neutral** (regime confidence 100) with a **risk-off macro headwind** (77/100) — mixed, not a clean directional read.
- Stocks mood: **risk-on / bullish** — SPY +1.37% 5d / +3.78% 20d uptrend, QQQ +2.50% 5d / +3.76% 20d uptrend, VIX 14.68 (calm), technology (XLK) leading +7.76% 20d, utilities/communications lagging.
- Dominant narrative: crypto — perps/DEX rotation (HYPE, fresh <1h) and a pure-momentum cluster (BTW/BANK/ATM, no confirmed news, fresh <1h); stocks — tech/AI leadership continuing into the open, AMAT earnings-day volatility.
- Preferred side now: **mixed / wait-for-trigger in crypto, longs-with-confirmation in stocks** — crypto's live long-heavy book (92%+ long) is not well supported by the neutral/risk-off regime read; stocks trend supports longs but this week's stocks A/B track record (0-for-4) argues for tight selectivity.
- Best long candidate: **ACE/USDT** (crypto, already open, highest live score 79.3) — no contradiction found; manage, don't add.
- Best short candidate: **MMT/USDT** (crypto, already open short leg aligned with tape) — the parallel open long on the same symbol should be reviewed, not treated as a fresh short opportunity to add to.
- Best catalyst-backed candidate: **HYPE/USDT** — freshest basket (<1h) but playbook says wait for pullback; not yet actionable.
- What to avoid: **PROM/USDT** longs (deleveraging tape, -26% 24h) and **BICO/USDT** longs (deleveraging tape, -15.7% 24h) — both contradict two live long positions; also avoid chasing AMAT into its earnings-day print.
- What would change the view: a BTC breadth improvement above ~60% EMA20 with OI confirmation would support the long-heavy crypto book; resolution of the PROM/BICO deleveraging (OI stabilizing) would remove the contradiction flag; RTH confirmation of a clean SPY/QQQ hold above the open would strengthen the stocks-long case further.

## 7. Candidate Deep Dives (≤5)

### 1. MMT/USDT — crypto, contradiction risk (HIGH priority)
- Two live open swing signals on the same symbol, opposite directions: `sig_be8481b801a2506a` LONG (score 68.0, triggered, entry 0.2123-0.2168) and `sig_6f5d3799c4e660c1` SHORT (score 65.6, triggered, entry 0.2024-0.2044).
- Current market read (fresh, this cycle): bias **short**, score 74.2, 24h **-17.24%**, RS/BTC -17.96%, tags `weak_vs_market, overextended`.
- Has price already reacted to the "catalyst"? No confirmed catalyst — this is pure weak-vs-market technical action.
- Is the setup chasing? The short is not chasing (aligned with the tape); the long is effectively fighting the tape.
- Retest/pullback structure? Not evaluated — TradingView/manual chart check unavailable, only OHLCV/ATR/EMA fields used.
- Aligned with market mood? Short = yes; long = no.
- Actionable now or after confirmation? Both are already open (live risk), not new entries — this is a **manage/review** item, not a fresh trade idea.
- What would invalidate: a reclaim of the long's invalidation level with OI confirmation would validate the long instead.
- Chase-risk: n/a (already open).
- Verdict: **MANUAL REVIEW REQUIRED** — simultaneous opposite-direction open risk on one symbol is a risk-manager flag, not a scoring bug by itself, but worth a human look at position sizing/netting.

### 2. PROM/USDT — crypto, contradiction risk (HIGH priority)
- Two live open LONG swing signals: score 65.1 (entry 2.4894-2.5909) and score 69.5 (entry 2.0822-2.1991), both `triggered`.
- Current market read: bias **short**, score 80.2, 24h **-26.31%**, RS/BTC -27.04%, tag `weak_vs_market`.
- Derivatives: **price down + OI down -16.4%** = long deleveraging / liquidation in progress — not a squeeze setup, genuine long-side capitulation.
- Has price reacted to any catalyst? No catalyst found for PROM this cycle; this looks like organic weakness, not news-driven.
- Chase risk: n/a (already open, both entries now well above current tape based on the -26% move).
- Aligned with market mood? No — actively fighting a confirmed deleveraging downtrend.
- What would invalidate the short-side concern: OI stabilizing + a reclaim of the entry_low levels.
- Verdict: **AVOID adding**; flag both open longs for manual review — worst tape contradiction this cycle.

### 3. BICO/USDT — crypto, mixed exposure
- Three signals across modes: intraday **SHORT** tp1_hit (aligned with tape), scalp **LONG** tp1_hit, swing **LONG** triggered (score 72.4, entry 0.03369-0.03540).
- Current market read: bias **short**, score 80.2, 24h **-15.69%**, RS/BTC -16.41%, tag `weak_vs_market`; derivatives: price down + OI down -10.25% (long deleveraging).
- The intraday short already reflects the correct read; the scalp/swing longs do not.
- Verdict: **CAUTION** — same pattern as PROM but smaller magnitude; note for review, not urgent as PROM.

### 4. ACE/USDT — crypto, best clean long
- Live swing long, score **79.3** (highest live B-tier score today), triggered, entry 0.1204-0.1284.
- No tape contradiction found in this cycle's top-movers/leaders lists (ACE not flagged bias=short or weak_vs_market).
- Chase risk: n/a, already open. Manage existing risk per plan; no fresh add recommended without a specific new catalyst.
- Verdict: **OPEN ACTIONABLE — hold per plan**, cleanest of the live book this cycle.

### 5. AMAT — stocks, earnings/headline risk
- Only live signal is **C-tier** intraday long (score 51.0, waiting_for_entry) — not actionable per tier gate regardless of the earnings event.
- Confirmed internal risk flags today: `do_not_chase_warning` — "earnings today, avoid chasing into the print"; `block_requires_operator_review` — "earnings today: new A/B here needs operator review."
- Legal/headline check: no fraud/investigation/delisting signal found for AMAT specifically this cycle (the legal_risk headlines found were for FUTU/BTU/FSLR, unrelated).
- Verdict: **NO-ENTRY / WATCH ONLY** — earnings-day volatility, C-tier gate already prevents action; do not chase any post-print move without RTH confirmation.

## 8. Best Candidates Ranked
1. **ACE/USDT (crypto, long, open)** — cleanest live position this cycle, highest score (79.3), no tape contradiction. Manage per plan.
2. **MMT/USDT short leg (crypto, open)** — tape-aligned (bias=short, -17.24% 24h, overextended); the parallel long leg on the same symbol needs manual review, not addition.
3. **Long-watch (crypto): HYPE/USDT** — trigger: confirmed pullback/retest per the `perps_dex_narrative` basket's own `wait_pullback` playbook (freshness <1h); do not chase the initial move.
4. **Short-watch (crypto): PROM/USDT or BICO/USDT (new short entries only, not adding to existing longs)** — trigger: a clean 1h retest into prior breakdown structure with continued OI decline; currently both are mid-deleveraging, chase risk is high on a fresh short right now.
5. **Catalyst-watch (crypto): BANK/USDT continuation** — already confirmed (tp2 hit); watch for a second push if `momentum_breakout` basket volume follows through (+22.0% 24h as of the 16:52 catalyst cycle).
6. **Stocks: none clean this cycle** — no fresh A/B triggered; all fresh stocks activity today is C-tier (non-actionable by design). AMAT is watch-only due to earnings.

## 9. Avoid / No Trade
This applies to the **current decision window only** — never a system-stop; scanning, tracking, and monitors all continue regardless.
- **Adding to PROM/USDT or BICO/USDT longs** — both fighting a confirmed OI-down deleveraging tape at -26% and -15.7% 24h respectively.
- **Chasing AMAT** — earnings-day print, internal `do_not_chase_warning` and `block_requires_operator_review` both active; C-tier gate already blocks it from Telegram-actionable status.
- **Chasing the momentum_breakout basket names (BTW/BANK/ATM) into further extension** — no confirmed news catalyst behind the move; treat as pure momentum, wait for pullback per playbook.
- **Treating XRP as tradeable right now** — internal `block_requires_operator_review` flag active on a bridge-exploit headline ("fake deposits treated as real"); not in the active book today, but avoid fresh XRP exposure until this clears.
- **Any fresh stocks A/B this week without extra scrutiny** — headline stats show 0 wins / 4 losses / PF 0 / -3R over the last 12 A/B stocks signals; small sample (weak confidence) but consistent with caution.

## 10. Main Risks
- **MMT/USDT and PROM/USDT book/tape contradictions** — largest identified risk this cycle; live directional exposure fighting confirmed market reads on both symbols.
- **Crypto book concentration**: 55/60+ live crypto signals sampled are long-direction, in a regime the system itself labels "neutral/range-chop" with a risk-off macro overlay — concentration risk if the regime breaks down rather than resolves up.
- **Stocks A/B playbook underperforming this week** (0-for-4, -3R) — small sample, but worth tightening scrutiny on any new A/B before treating as actionable.
- **Catalyst mapping at 74.7% unmapped today** — reduces confidence in catalyst-backed candidate selection; treat the catalyst layer as context only this cycle.
- **AMAT earnings-day volatility** — already gated by tier and internal warnings, low incremental risk given C-tier status.
- **Geopolitical/macro overhang** (Iran/Strait of Hormuz, Ukraine, missile-defense headlines) continues to weigh on the macro risk score (77/100) — no material change vs prior cycle.

## 11. Action Plan — next 4 hours
- Surface MMT/USDT (opposite-direction open exposure) and PROM/USDT (long-vs-deleveraging-tape) for manual/human review — these are the two highest-value items from this cycle.
- Watch HYPE/USDT for a pullback/retest entry per its basket's own playbook; do not chase the initial <1h move.
- Watch for RTH confirmation/failure on the current stocks C-tier leaders (SNOW, KO, IBM, PLTR — all high-score C-tier, non-actionable but useful research signal) into the rest of the US session.
- Re-check AMAT post-earnings reaction next cycle once the print has been digested by the tape.
- No scoring, threshold, or routing changes recommended — all findings are advisory.

## 12. Final Verdict per Mode
- **Crypto scalp**: NO fresh actionable signal this cycle; existing book unchanged.
- **Crypto intraday**: NO fresh actionable signal this cycle (TST/USDT remains the only live intraday B, ~7h old, unchanged).
- **Crypto swing**: MANUAL REVIEW REQUIRED for MMT/USDT and PROM/USDT specifically; rest of the book (ACE/USDT best) is WATCH/HOLD per plan, no new adds recommended given the neutral/risk-off regime read.
- **Stocks intraday**: WATCH ONLY — all fresh signals are C-tier (non-actionable by design); AMAT specifically NO-ENTRY due to earnings.
- **Stocks swing/invest**: N/A — deprecated modes, no data this cycle.

## 13. Sources
- Internal: [catalyst_cycle_13-52.md](data/catalysts/2026-08-13/catalyst_cycle_13-52.md), [catalyst_events.jsonl](data/catalysts/2026-08-13/catalyst_events.jsonl), [llm_analysis_packet.md](data/processed/llm_analysis_packet.md), [llm_stocks_packet.md](data/processed/llm_stocks_packet.md), `db/crypto_ai_desk.sqlite` (`proposed_signals`, `watchlist_alerts` — read-only queries).
- No external WebSearch/WebFetch performed this cycle — all findings sourced from internal, already-collected data (news_items-derived catalyst layer, derivatives/OI snapshots, signal book) which was sufficiently fresh (<6h) and internally consistent for every candidate discussed; no candidate's verdict depended on unverified external claims.

## 14. Fix Requests / TODO

### TODO-catalyst-symbol-resolver-legal-risk
- **issue:** Legal-risk catalyst events for FUTU, BTU, FSLR have the ticker plainly in the title but `symbol` field is empty — resolver miss for `legal_risk` catalyst_type specifically (PR Newswire source).
- **evidence:** `data/catalysts/2026-08-13/catalyst_events.jsonl` — 3 rows, catalyst_type=legal_risk, importance=0.75, source="PR Newswire (Stocks)", titles contain "Futu Holdings", "BTU Investors", "FSLR Investors" respectively, symbol="".
- **suggested manual fix:** extend the symbol resolver's title-parsing rules to cover the "$TICKER Investors Have Opportunity to Lead... Securities Fraud Lawsuit" boilerplate pattern common to PR Newswire law-firm solicitations.
- **priority:** medium
- **first observed:** 2026-08-13 18:48 EEST

### TODO-mmt-simultaneous-long-short
- **issue:** MMT/USDT currently has two live open swing signals in opposite directions simultaneously (long score 68.0 + short score 65.6), both status=triggered.
- **evidence:** `proposed_signals` rows `sig_be8481b801a2506a` (long, created 2026-08-13T02:56:13Z) and `sig_6f5d3799c4e660c1` (short, created similar window) — both currently triggered per `active-signals --asset-class crypto`.
- **suggested manual fix:** review whether the signal generator should block/flag same-symbol opposite-direction concurrent signals, or whether this is intentional (e.g. different timeframe theses) and just needs clearer surfacing to the operator.
- **priority:** high
- **first observed:** 2026-08-13 18:48 EEST

### TODO-monitor-recycle-permission-error
- **issue:** `pending_monitor` log shows repeated `tracker:OperationalError` (4x, retried) and one `PermissionError: [WinError 5] Access is denied` on worker recycle.
- **evidence:** `data/scheduled_runs/2026-08-12_default_schedule/pending_monitor_1786627282.log`, lines near end of file (worker rotation section).
- **suggested manual fix:** investigate whether this is a transient file-lock (e.g. antivirus, another process holding a handle) or a recurring resource leak; low frequency so far but worth a manual look if it increases.
- **priority:** low
- **first observed:** 2026-08-13 18:48 EEST
