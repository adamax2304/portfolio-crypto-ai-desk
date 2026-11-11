# Opus Enriched Review — crypto overnight / Asia review — Auto Cycle 04:30 EEST

## 1. Executive Summary

Advisory only / no auto-trade. **Crypto overnight / Asia review** — stocks are closed (next RTH open ~16:30 EEST); crypto is the only live actionable class this slot. Desk-internal macro/geopolitical risk score sits at the **maximum 100.0/100** (up from 95.8-95.9 at the 23:15 post-close review) as the US-Iran conflict continues to escalate overnight: Iran launched ballistic missiles from Tabriz/Urmia, struck Kuwait (hitting US-linked targets), the US Treasury froze $130M in Iran-linked crypto, and Trump ruled out a ground campaign while keeping the naval blockade in place. **External verification shows the crypto market reaction has been comparatively muted** — BTC is holding the low-$62k–64k range, with one source noting markets price a ~97% chance the Hormuz disruption persists through August, and ETF inflows continuing despite the headline risk. This muted-reaction-vs-maxed-internal-risk-score divergence is itself the key read into Asia hours. On the desk: **TAO/USDT swing short remains the standout continuing winner** (TP1 196.05 confirmed hit, still managing to TP2 193.6/TP3 191.15). Three fresh B-tier intraday longs triggered this cycle — **ZEC/USDT, KAITO/USDT, SXT/USDT** — but the *current* scan cycle (02:37-02:48 EEST) already flags ZEC as more than 2 ATR from EMA20 ("do not chase") and scores KAITO/SXT below the active threshold (50.8/100): manage the open positions, do not add fresh size. Zero A-tier and zero fresh B-tier anywhere in scalp/intraday this cycle beyond those three. **HEI/USDT's 3-cycle-old untracked Telegram alert is now resolved** — the detector found zero untracked legacy alerts this run. UNH remains AVOID/MANUAL REVIEW (DOJ probe + earnings tomorrow 07-16). Catalyst mapping is weak this run (84.6% unmapped, recomputed on a fresh 500-event scan since today's catalyst folder didn't exist yet) — context only, recurring and already tracked. Scanning, tracking, and the paper book continue uninterrupted in all moods.

## 2. Data Used

- Crypto reports: scalp (mtime 2026-07-15 02:42 EEST), intraday (mtime 02:48 EEST) — both ~1h50m-2h old at review time, well within the 4h fresh window; data freshness timestamp inside both reports is 2026-07-14 23:30/23:45 UTC
- Swing report: 2026-07-14 02:15 EEST gen (mtime 05:15 EEST) — **stale (>14h, ~23h old), excluded from fresh swing verdict per freshness rule, carry-forward only for existing open positions (TAO)**
- Stocks intraday report: mtime 2026-07-15 03:01 EEST (~1h40m old) — market closed, planning/watchlist context only per slot rules
- Stocks swing/invest reports: last dated 2026-07-02 (~13 days stale) — excluded; position-framework for stocks swing/invest remains deprecated per prior desk decision
- `data/catalysts/2026-07-15/` was missing at review start — ran the one allowed `catalyst-scan --no-print` CLI (500 news_items scanned, 500 events, 3 baskets, 0 rejected) to populate it; `catalyst_cycle_01-40.md`, `catalyst_events.jsonl`, `narrative_baskets.jsonl` all now present
- `data/processed/llm_analysis_packet.md` (mtime 02:48 EEST), `data/processed/llm_stocks_packet.md` (mtime 03:02 EEST)
- CLI: `active-signals --asset-class crypto` (22 rows, all B-tier), `active-signals --asset-class stocks` (50 rows, all C-tier except 2 B-tier tp2_hit), `signal-stats --asset-class crypto`, `signal-stats --asset-class stocks`, `detect_untracked_legacy_alerts --since 2026-07-15` (0 untracked found — HEI/USDT issue resolved)
- Direct read-only SQL against `db/crypto_ai_desk.sqlite` (`proposed_signals`, `news_items`) to confirm exact entry/stop/TP levels for TAO/ZEC/KAITO/SXT/HYPE and to check the freshest (last 2-6h) internal news for the Iran/Hormuz situation
- Direct Python scan of `catalyst_events.jsonl` for mapped/unmapped symbol coverage (84.6% unmapped, 500 events, recomputed on the freshly-scanned file — the pre-existing 82%+ figure from the last review was against yesterday's 4,499-event file, this is a smaller same-morning sample)
- External: WebSearch ×2 (Iran/Hormuz/Bitcoin market reaction, Bitcoin Asia-session price) — both resolved; no WebFetch needed since search summaries were internally consistent and sufficient to characterize the muted-reaction thesis
- `crypto_monitor_1784073824.log` / `derivatives_monitor_1784073824.log` mtimes ~04:37-04:38 EEST (essentially live at review time) — confirms scanning/scoring continues uninterrupted overnight
- Compared against previous review `OPUS_ENRICHED_REVIEW_AUTO_2026-07-14_2315.md` (post-close final daily review, ~5h14m prior)

## 3. Scheduler / Data Freshness

- `data/scheduled_runs/2026-07-15_default_schedule/scheduler.log` mtime 03:06 EEST (~1h38m before this review) — fresh, well under the 3h defer threshold
- Latest cycle summary `cycle_01_02-34_summary.md` (started 02:34, finished 03:06, 57/57 steps ok, 0 failed) — fresh
- `crypto_monitor_1784073824.log` and `derivatives_monitor_1784073824.log` both actively updating through ~04:37-04:38 EEST — monitors confirmed running live, well past the main cycle's completion
- `pending_monitor.log` / `stocks_monitor.log` present from cycle start (03:03 EEST); stocks monitor idle is expected — US cash session closed
- No deferral triggered — both freshness checks pass comfortably

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "crypto_overnight",
  "as_of": "2026-07-15 04:45 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "ok",
      "confidence": 0.82,
      "reason_codes": ["scheduler_fresh", "report_stale", "catalyst_missing"],
      "data_missing": ["today's catalyst folder had to be generated mid-review (now present)", "swing report stale >14h, no fresher source", "stocks swing/invest stale ~13d, deprecated"],
      "suggested_effect": "advisory_only",
      "facts_used": ["scheduler.log mtime 03:06 EEST", "crypto scalp/intraday reports ~2h old, within 4h window", "swing report mtime 2026-07-14 05:15 EEST (~23h old)", "crypto_monitor/derivatives_monitor logs live through 04:37-04:38 EEST"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["mixed", "chop", "risk_off", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto regime label transition (mixed), BTC/ETH both uptrend but altcoin breadth only 38.5%/43.6% above EMA20/50", "desk macro/geopolitical risk score 100.0/100 (max), up from 95.8-95.9 three reviews ago", "external search: BTC holding $62-64k, crypto reaction to Iran/Hormuz escalation described as muted/steady vs equities", "stocks regime risk_on (VIX 16.50, breadth 75%/100%) but market closed — planning only"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "no_catalyst", "narrative_supported"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["84.6% of 500 freshly-scanned catalyst_events unmapped this run (77 mapped)", "ai_narrative basket from the prior review has dropped off; active baskets now perps_dex_narrative (HYPE/USDT primary, fresh<6h), delisting_thin_liquidity, and new momentum_breakout (ZEC/USDT primary, no confirmed news catalyst)", "ZEC/KAITO/SXT all have no verified fresh catalyst backing per report §5 — pure momentum/RS plays, carrying the desk's own documented no-catalyst-chop failure mode (WR 23%/PF 0.70/-3R)"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.45,
      "reason_codes": ["data_unavailable", "oi_supports", "post_unwind_chop"],
      "data_missing": ["bybit/OKX cross-check for ZEC/USDT and TAO/USDT specifically at this hour"],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZEC/USDT: price up + OI up, fresh positioning confirms trend, funding neutral, crowding normal", "KAITO/USDT and SXT/USDT: derivatives via MEXC fallback only, OI n/a — thinner positioning data than ZEC", "ALLO/KITE/ZBT: price down + OI down, deleveraging/long-liquidation pattern persists"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["entry_late", "chase_risk", "entry_fresh", "overextended"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["ZEC/USDT: existing intraday long (entry 548.84-554.27, triggered 00:52) — current 02:48 scan cycle now scores it 35.9 and flags 'more than 2 ATR from EMA20, do not chase' — the open position is fine, fresh adds are not", "KAITO/USDT and SXT/USDT: existing intraday longs (triggered 00:06) both score only 50.8 in the current cycle — below the active threshold, watchlist-only language now attached to the same symbols", "TAO/USDT short: TP1 196.05 confirmed hit, EMA stack (206-219) still well above price, no exhaustion signal, invalidation 201.44 intact"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.8,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto active (DB, non-terminal): 22 total, all B-tier — 6 triggered + 13 tp1_hit + 3 tp2_hit, all OPEN actionable/managing, 0 waiting_for_entry", "stocks active (DB, non-terminal): 50 total — 2 B-tier OPEN actionable (both tp2_hit), 21 C-tier WAITING for entry (next session), 27 C-tier triggered/tp1_hit/tp2_hit REVIEW/SHADOW (never Telegram-actionable)", "detect_untracked_legacy_alerts: 0 found this run — HEI/USDT's 3-cycle-old orphaned alert is resolved/no longer flagged", "HYPE/USDT perps_dex primary signal itself is NO-ENTRY/STALE (entry_moved_away as of 2026-07-13), even though the narrative basket remains active"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.7,
      "reason_codes": ["headline_risk", "correlation_cluster", "legal_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["desk macro/geopolitical risk score 100.0/100 (maxed) on continued Iran/Hormuz/Kuwait escalation overnight", "external verification shows crypto price action comparatively muted (BTC $62-64k range) vs the maxed internal risk score — a real divergence worth tracking, not yet a confirmed all-clear", "22 active crypto signals remain concentrated in altcoin swing/intraday longs against weak breadth (38.5%/43.6%)", "UNH DOJ probe unchanged, now compounded by earnings tomorrow (07-16) — do-not-chase warning active on the ticker"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.72,
      "reason_codes": ["playbook_failing", "playbook_working", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["crypto signal-stats: tier=B triggered winrate 14.6% low (n=153 reliable), PF 1.31 overall; scalp mode PF 0.44/avgR -0.097 (data-collection-only by design, kill-switched for new entries); shorts overall PF 0.50 (n=20, weak); setup=breakout PF 0.125 (0/7 wins, anecdotal, worth watching not acting on)", "stocks signal-stats: tier=C triggered winrate 11.1% low, PF 0.670 below the 0.8 bar (n=207/228 reliable) — consistent with prior reviews, never actionable by design", "stocks A/B (Model F paper_execution_r) 7d/14d/30d all +4.7R/PF2.16/n9 forward_postfreeze — small-sample but consistently positive, unchanged from last review"]
    },
    {
      "agent": "head_trader",
      "verdict": "ok",
      "confidence": 0.68,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.68,
    "preferred_side": "wait_for_trigger",
    "best_long_candidate": { "symbol": "ZEC/USDT (existing, manage only)", "trigger": "no fresh add — current scan flags >2 ATR from EMA20; a fresh long needs a pullback retest toward EMA20 with volume confirmation before re-entry", "reason": "existing intraday long already open (entry 548.84-554.27) and working toward TP1 568.74; the setup is real (OI-confirmed uptrend) but the current cycle correctly withholds fresh entries as a chase" },
    "best_short_candidate": { "symbol": "TAO/USDT", "trigger": "hold below TP1 196.05 toward TP2 193.6, invalidate above 201.44; fresh adds only on a 1h failed-bounce retest into 198.99-200.09", "reason": "TP1 confirmed hit, thesis intact, EMA stack still well above price with no exhaustion signal — the desk's cleanest continuing position" },
    "best_catalyst_candidate": { "symbol": "HYPE/USDT", "trigger": "perps_dex_narrative basket still active (fresh <6h) but the actual signal is NO-ENTRY/STALE since 07-13 — needs a brand-new technical entry structure to be re-considered, not a re-chase of the old level", "reason": "only actively-tracked narrative basket with a named primary; not yet a scored A/B candidate and now going stale as an executable idea" },
    "avoid_candidate": { "symbol": "UNH", "reason": "active DOJ/Medicare legal-risk investigation plus earnings tomorrow (2026-07-16) — do-not-chase warning now layered on top of the existing legal-risk gate; no new entries" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 2
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---|---|---|
| data_quality | ok | 0.82 | scheduler_fresh, report_stale, catalyst_missing | advisory_only |
| market_regime | caution | 0.60 | mixed, chop, risk_off, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, no_catalyst, narrative_supported | advisory_only |
| derivatives_squeeze | caution | 0.45 | data_unavailable, oi_supports, post_unwind_chop | advisory_only |
| technical_entry | caution | 0.65 | entry_late, chase_risk, entry_fresh, overextended | advisory_only |
| execution_lifecycle | ok | 0.80 | open_actionable, waiting_for_entry, review_shadow, no_entry | advisory_only |
| risk_manager | caution | 0.70 | headline_risk, correlation_cluster, legal_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.72 | playbook_failing, playbook_working, low_sample | advisory_only |
| head_trader | ok | 0.68 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

vs `OPUS_ENRICHED_REVIEW_AUTO_2026-07-14_2315.md` (post-close final daily review, ~5h14m ago):

- **Macro/geopolitical risk score hit the ceiling**: 100.0/100 this run vs 95.8-95.9 at post-close — Iran launched ballistic missiles from Tabriz/Urmia, struck Kuwait (hitting a US-linked target), the US Treasury froze $130M in Iran-linked crypto, and Trump ruled out a ground campaign while keeping the blockade active. This is the third consecutive review showing escalation, not de-escalation.
- **External verification adds a genuinely new data point**: crypto's actual price reaction has been comparatively muted (BTC holding $62-64k) versus the maxed internal risk score — worth tracking as a divergence, not yet grounds to downgrade the caution stance.
- **HEI/USDT's untracked alert is resolved** — after 3 consecutive evening cycles (18:39 → 21:39 → 23:15) flagging the same orphaned Telegram alert, `detect_untracked_legacy_alerts` now returns zero. Root cause unconfirmed but the specific instance is gone.
- **Three fresh B-tier intraday longs registered overnight**: ZEC/USDT (00:52), KAITO/USDT (00:06), SXT/USDT (00:06) — new since the post-close review, which had no fresh triggers to report. All three are now flagged by the *current* scan cycle as chase-risk (ZEC, >2 ATR from EMA20) or below-threshold (KAITO/SXT, 50.8/100) — manage, don't add.
- **TAO/USDT short unchanged** — still TP1-hit, still managing toward TP2 193.6/TP3 191.15, still the cleanest position on the book.
- **Catalyst basket composition shifted**: the `ai_narrative` basket (TAO/RENDER/FET/NEAR defensive rotation) that was active at post-close has dropped out of the current scan; `perps_dex_narrative` (HYPE) persists, and a new `momentum_breakout` basket appeared (ZEC/USDT primary, pure momentum — no confirmed news catalyst).
- **Catalyst mapping recomputed on a fresh, smaller sample**: today's catalyst folder didn't exist yet at review start (ran the one allowed `catalyst-scan` CLI); the resulting 500-event scan shows 84.6% unmapped, in the same weak-mapping range as the 82-83% seen on larger multi-thousand-event days.
- **UNH gained a second reason to avoid**: earnings now confirmed tomorrow (2026-07-16) on top of the unchanged DOJ probe — do-not-chase warning layered on.
- **Stocks intraday candidate list refreshed for the next session**: JPM (100, but now flagged `stale_post_earnings_setup` since its 07-14 earnings print), META (98.5), NVDA (91.4), PLTR (90.3) remain the top raw scores, all still gated to C purely by `market_closed_intraday_planning_only` until the open.

## 5. Catalyst Coverage

- Total `catalyst_events` this scan: **500** (freshly generated this run — today's folder did not exist at review start)
- Mapped (non-null symbol): **77** (15.4%)
- Unmapped (null symbol): **423** (84.6%)
- `narrative_baskets`: **3** active (`perps_dex_narrative` primary HYPE/USDT, `delisting_thin_liquidity`, `momentum_breakout` primary ZEC/USDT)
- **Catalyst mapping weak this run — use catalyst layer as context, not final decision.** (unmapped > 50%, consistent with the 82-85% range seen across recent cycles — recurring, already tracked, not worsening)
- Top unmapped items (sample, mostly noise this run — only 12/423 are Telegram bot-welcome spam, the rest are genuine but symbol-unresolved headlines): "Guidewire's CEO Sold $166,000 in Stock — Here's What Investors Should Know" (The Motley Fool); assorted t.me/lookonchain bot-welcome messages; various single-source stock-legal PR-Newswire class-action notices with no ticker extraction

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **mixed/chop, elevated risk-off headwind** — BTC/ETH trend labels both uptrend, but altcoin breadth weak (38.5%/43.6% above EMA20/50) and desk macro/geopolitical risk score is maxed at 100.0/100 on the ongoing Iran/Hormuz/Kuwait escalation
- Stocks mood: **closed (risk_on regime label held from yesterday's close, VIX 16.50, breadth 75%/100%)** — planning/watchlist only until the 16:30 EEST open
- Dominant narrative: Iran/Hormuz/Kuwait conflict is the dominant overnight risk factor (unchanged direction from post-close, now escalated further); `perps_dex_narrative` (HYPE) and the new no-catalyst `momentum_breakout` (ZEC) are the only live crypto narrative baskets; `ai_narrative` defensive-rotation basket has quieted since post-close
- Preferred side now: **wait-for-trigger**, biased toward managing the existing TAO short and the three newly-open intraday longs (ZEC/KAITO/SXT) rather than adding fresh size into either direction
- Best long candidate: ZEC/USDT (existing, manage only — current scan flags it as extended, do not chase fresh)
- Best short candidate: TAO/USDT (existing, TP1 confirmed hit, managing toward TP2 193.6/TP3 191.15)
- Best catalyst-backed candidate: HYPE/USDT (perps_dex_narrative basket still active, but the tracked signal itself has gone stale since 07-13 — needs a fresh entry structure, not a re-chase)
- What to avoid: adding fresh size to ZEC/KAITO/SXT at current extended/below-threshold levels; any new UNH exposure (legal + earnings tomorrow); chasing the still-maxed macro-risk overnight tape generically
- What would change the view: a de-escalation headline on Iran/Hormuz/Kuwait; BTC reclaiming and holding above local resistance with EMA20/50 breadth expansion; a confirmed pullback-with-volume retest on ZEC/KAITO/SXT; JPM/XLF/GOOGL/etc. holding today's post-earnings gains with confirmed volume at tomorrow's US open

## 7. Candidate Deep Dives

### 1. TAO/USDT — existing swing short, TP1 confirmed hit (continuing standout, highest priority)
- Status: **OPEN actionable**, managing — entry 198.99-200.09, invalidation 201.44, **TP1 196.05 hit**, next target TP2 193.6, TP3 191.15
- Has price already reacted to the catalyst? Yes — thesis has played out cleanly across three consecutive reviews now
- Chasing? No — existing, already-profitable managed position
- Retest/pullback structure? A fresh short add would need a failed-bounce retest back into 198.99-200.09
- Overextended? No — EMA stack (206-219) still sits well above price, no exhaustion signal
- Aligned with market mood? Yes — fits the ongoing risk-off macro backdrop
- Long/short/wait? Short (existing, working as planned)
- Actionable now or after confirmation? Already actionable/open; fresh adds require the retest trigger above
- Invalidation: 1h close/reclaim above 201.44
- Chase-risk setup? No
- Catalyst confirmation/contradiction? No new fresh headline specific to TAO this cycle; thesis stands on the unchanged technical/derivatives picture, not a live catalyst

### 2. ZEC/USDT — fresh intraday long, now flagged as extended by the current scan (manage, do not add)
- Status: **OPEN actionable/triggered** — entry 548.84-554.27 (triggered 2026-07-15T00:52 UTC), stop 542.21, TP1 568.74/TP2 580.80/TP3 592.87
- Has price already reacted? Yes — +12.9% 24h, RS vs BTC +8.6%, volume 0.89x (real volume confirmation, unlike the other two names below)
- Chasing? The *existing* position is not a chase; a *fresh* add right now would be — the 02:48 EEST scan cycle scores this symbol 35.9 and explicitly flags "more than 2 ATR from EMA20; do not chase"
- Retest/pullback structure? None active; would need price to come back toward EMA20 with volume before a fresh add makes sense
- Overextended? Yes, per the current cycle's own gate
- Aligned with market mood? Marginal — this is the `momentum_breakout` basket primary with no confirmed news catalyst, carrying the desk's documented no-catalyst-momentum failure mode
- Actionable now for new size? No — manage the existing position toward TP1/TP2/TP3, do not add
- Catalyst confirmation? None — pure momentum cluster per the catalyst scan
- Derivatives: price up + OI up (fresh positioning confirms the move), funding neutral, crowding normal — supports the existing long, doesn't itself justify a fresh entry at these levels

### 3. KAITO/USDT & SXT/USDT — fresh intraday longs, both now below the active threshold (manage, do not add)
- Status: **OPEN actionable/triggered** — KAITO entry 0.7694-0.7819 (stop 0.7541, TP1 0.8151); SXT entry 0.00903-0.00920 (stop 0.00881, TP1 0.00967); both triggered 2026-07-15T00:06 UTC
- Has price already reacted? Yes for both — KAITO +19.6%/24h (RS +15.3%), SXT +18.3%/24h (RS +14.0%), both up further over 7d (KAITO +27.9%, SXT +40.2%)
- Chasing? A fresh add would be — the current 02:48 cycle scores both only 50.8/100 (below the active threshold) with volume ratios of just 0.03-0.24x, i.e. the move is not backed by strong current volume
- Retest/pullback structure for a fresh idea: KAITO conditional pullback 0.7589-0.7714 (invalidate above 0.7435, wait for volume); SXT conditional pullback 0.0090-0.0092 (invalidate above 0.0087)
- Overextended? Yes on both, per the current cycle's own risk-penalty scoring (-16.7 each)
- Aligned with market mood? Marginal — same no-catalyst-momentum-in-chop failure mode as ZEC, no verified fresh catalyst for either symbol in `news_items`
- Actionable now for new size? No — manage the existing triggered positions toward their stated TP ladders; wait for the pullback zones above before considering fresh size
- Catalyst confirmation? None found for either symbol

### 4. UNH — stocks, legal + earnings risk (avoid / manual review, existing exposure only)
- Status: **NEEDS REVIEW** — C-tier via `legal_headline_risk: sec_doj` gate demotion, now compounded by confirmed earnings tomorrow (2026-07-16); no A/B entries possible while either flag is live
- Legal/headline check: DOJ criminal probe (Optum Rx, physician reimbursement) unchanged since prior reviews; stock still carries the prior 4.7% DOJ-news drawdown
- Verdict: **AVOID / MANUAL REVIEW REQUIRED** for existing exposure — never a clean actionable while the legal gate is live, and now also carries an explicit `do_not_chase_warning` into tomorrow's earnings print
- What would change the view: DOJ probe resolution or materially narrowed scope (neither observed); post-earnings reaction would need its own fresh review regardless

### 5. HYPE/USDT — best catalyst-backed idea, but the tracked signal itself has gone stale
- Status: **NO-ENTRY/STALE** — the specific proposed_signal (short, entry 65.38-65.68) is `stale_before_entry` as of 2026-07-13T11:44 UTC, over a day old; the `perps_dex_narrative` basket around it remains active (fresh <6h) in today's catalyst scan
- Has price already reacted? Unclear from internal data alone — no fresh OHLCV check was run for HYPE this cycle (not in the top-8 deep-analysis set)
- Chasing? Not applicable — no live entry structure exists
- Actionable now? No — needs a brand new technical setup (entry/stop/TP) generated against current price before this becomes a real candidate again; do not act on the stale short level
- Catalyst confirmation? Yes at the basket level (Hyperliquid/perps-DEX narrative persists), but that alone does not create a tradeable signal
- Lesson: narrative baskets can stay "fresh" long after their attached signal has gone stale — treat the basket label and the signal-level status as two separate freshness clocks

## 8. Best Candidates Ranked

1. **TAO/USDT — best short (existing, TP1 confirmed hit, managing toward TP2/TP3).** Fresh-entry trigger for anyone not already in: a new 1h failed-bounce retest into 198.99-200.09, invalidate above 201.44.
2. **ZEC/USDT — best long (existing, manage only).** OI-confirmed uptrend with real volume backing, but the current cycle correctly flags it as extended (>2 ATR from EMA20) — manage toward TP1 568.74/TP2 580.80/TP3 592.87, do not chase fresh size.
3. **KAITO/USDT & SXT/USDT — manage-only watch.** Both triggered overnight, both now below the active threshold on thin volume (0.03-0.24x) — manage existing size toward stated TPs; wait for the pullback zones (KAITO 0.7589-0.7714, SXT 0.0090-0.0092) before considering fresh entries.
4. **HYPE/USDT — best catalyst-watch (not yet actionable).** perps_dex_narrative basket persists, but the underlying signal is stale since 07-13 — needs a fresh technical entry structure before this is a real candidate.
5. **UNH — avoid / manual review** for existing exposure; DOJ probe unchanged, now layered with a do-not-chase earnings warning for tomorrow (07-16).
6. **Stocks pre-market watchlist (planning only, market closed).** JPM (100, flagged stale-post-earnings), META (98.5), NVDA (91.4), PLTR (90.3) are the top raw scores for tomorrow's open — all currently C-tier purely on `market_closed_intraday_planning_only`; re-evaluate on fresh levels at/after the 09:30 ET / 16:30 EEST open, require rvol + trend-continuation confirmation in the first 15-30 minutes, not technical score alone.

## 9. Avoid / No Trade (this decision window only)

- **Adding fresh size to ZEC/USDT, KAITO/USDT, or SXT/USDT** at current extended/below-threshold levels — manage the existing triggered positions, wait for the stated pullback zones for anything new.
- **Chasing HYPE/USDT** off the stale 07-13 short level — no live entry structure exists; the narrative basket being "fresh" does not make the old level tradeable.
- **New UNH long or short exposure** without a fresh legal-risk and post-earnings review; both gates are live into tomorrow.
- **Treating the maxed macro-risk score (100/100) as license to short everything** — external verification shows the actual crypto price reaction has been comparatively muted so far; this is a "stay cautious and manage size" signal, not a "the sky is falling" signal.
- **Chasing tomorrow's US open off tonight's high raw stocks scores (JPM/META/NVDA/PLTR)** — every one of them is gated purely by `market_closed_intraday_planning_only`; require the gates to clear (rvol + trend continuation + catalyst where relevant) at the open, not just a high overnight technical score.
- **Fresh crypto or stocks entries generically into the Asia window** given the sustained macro-risk escalation — this is a decision-window-only call; scanning, tracking, candidate generation, and outcome recording continue in all cases; nothing here is a command to pause any part of the system.

## 10. Main Risks

- Geopolitical (elevated, at the desk's ceiling): Iran launched ballistic missiles from Tabriz/Urmia and struck Kuwait overnight; the US Treasury froze $130M in Iran-linked crypto; Trump ruled out a ground campaign while the naval blockade remains active. Desk macro/geopolitical risk score is now maxed at 100.0/100, the third consecutive review showing escalation. External verification shows crypto's actual price reaction has been comparatively muted (BTC $62-64k) — a real divergence between the desk's own maxed risk score and observed market behavior, worth continued tracking rather than treating as resolved either way.
- Concentration: 22 active crypto signals remain overwhelmingly B-tier altcoin swing/intraday longs against weak breadth (38.5%/43.6%) — an unwind-together correlation cluster if BTC breaks down during Asia hours.
- Execution quality: three fresh overnight triggers (ZEC/KAITO/SXT) have all already run past the point where the *current* scan would approve a fresh entry — a reminder that entries generated hours apart from the review can be stale relative to the freshest scan, even within the same "fresh" 2h report window.
- Catalyst-mapping weak this run (84.6% unmapped on a fresh 500-event scan) — treat the catalyst layer as context only, not a standalone decision input (recurring, already tracked, stable magnitude).
- Legal/headline: UNH's DOJ probe remains a live manual-review item, now compounded by confirmed earnings tomorrow (07-16) — do not chase either direction into the print.
- Historically weak buckets to lean against: crypto tier=B triggered winrate 14.6% (n=153); crypto scalp mode PF 0.44 (kill-switched for new entries, data-collection-only by design); crypto short direction overall PF 0.50 (n=20, weak sample); crypto setup=breakout PF 0.125 (0/7 wins, anecdotal); stocks tier=C triggered winrate 11.1% / PF 0.670 (both below the desk's own 0.8 bar, C-tier never actionable by design).

## 11. Action Plan — next 4 hours (through the Europe pre-open review)

- Manage TAO/USDT short toward TP2 193.6/TP3 191.15; only add on a fresh 1h failed-bounce retest into 198.99-200.09, invalidate above 201.44.
- Manage ZEC/USDT long toward TP1 568.74/TP2 580.80/TP3 592.87; do not add fresh size while the current scan flags it as >2 ATR extended — wait for a pullback toward EMA20 with volume.
- Manage KAITO/USDT and SXT/USDT longs toward their stated TP ladders; do not add fresh size at current levels (both scoring below threshold on thin volume); watch for the pullback zones (0.7589-0.7714 and 0.0090-0.0092 respectively).
- Continue treating UNH as manual-review-only; no new entries with both the DOJ gate and tomorrow's earnings live.
- Watch closely for the Asia-session reaction to the Iran/Hormuz/Kuwait escalation continuing into the Europe pre-open review (11:30 EEST) — external sources suggest crypto has so far absorbed the news better than expected; confirm whether that holds or breaks down as Asia trading progresses.
- Watch whether HYPE/USDT develops a genuinely new technical entry structure — the old 07-13 level is stale and should not be re-used.
- No data-integrity follow-up needed on HEI/USDT this cycle — the untracked-alert detector returned zero; continue monitoring for any recurrence.

## 12. Final Verdict per Mode

- **Crypto scalp**: Data-collection-only by design (PF 0.44 this week, historically PF 0.14); kill-switch remains active for new entries (`crypto_scalp_disabled`) — no change to that classification.
- **Crypto intraday**: Manage existing (ZEC/KAITO/SXT all open, all now flagged as chase-risk for fresh size by the current scan); zero fresh A/B this cycle beyond the three already-triggered names.
- **Crypto swing**: Manage existing book — TAO short remains the standout continuing winner (TP1 hit); underlying swing report itself is stale (>14h), so no fresh swing verdict issued this cycle, carry-forward only.
- **Stocks intraday**: No trade — market closed, 0 A/B actionable, all raw-A candidates (JPM/META/NVDA/PLTR/XLF/GOOGL/AMZN/COIN) gated purely by `market_closed_intraday_planning_only`; re-evaluate at the 16:30 EEST open with rvol + trend-continuation confirmation required.
- **Stocks swing/invest**: Deprecated / stale data source (2026-07-02) — no verdict issued, consistent with prior desk decision.

## 13. Sources

- [U.S.-Iran hostilities over Strait of Hormuz drag crypto lower after positive week: Crypto Markets Today](https://www.coindesk.com/markets/2026/07/13/profit-taking-mideast-hostilities-drag-crypto-lower-after-bullish-week) — CoinDesk, 2026-07-13
- [Bitcoin falls below $63,000 as markets give Hormuz traffic just 3% chance to normalize by August](https://cryptoslate.com/bitcoin-falls-below-63000-as-markets-price-a-97-chance-hormuz-stays-disrupted-through-july/) — CryptoSlate, 2026-07-14
- [Bitcoin Holds $62,000 Despite US Strikes, Strait of Hormuz Tensions](https://en.bloomingbit.io/feed/news/116214) — BloomingBit, 2026-07-14
- [BTC price news: What recent U.S.-Iran strikes mean for bitcoin, ether, solana](https://www.coindesk.com/markets/2026/07/13/bitcoin-holds-near-usd63-800-as-war-driven-selloff-hits-everything-but-crypto) — CoinDesk, 2026-07-13
- [Current price of Bitcoin for July 14, 2026](https://fortune.com/article/price-of-bitcoin-07-14-2026/) — Fortune, 2026-07-14 (reference price only, ~06:00 ET)
- Internal `news_items` (re-confirmed, all 2026-07-14 23:00-23:30 UTC): Iran ballistic missile launches from Tabriz/Urmia (CryptoBriefing); US Treasury freezes $130M Iran-linked crypto (CryptoBriefing); Iran strikes cause explosions in Kuwait, targets US military in Jordan (CryptoBriefing); Trump rules out US ground campaign in Iran (CryptoBriefing)

## 14. Fix Requests / TODO

### TODO-catalyst-mapping-weak-recurring
- **issue:** Catalyst→symbol mapping remains weak (84.6% of 500 freshly-scanned events unmapped this run) — consistent with the previously-documented ~17% match rate from the news-layer hardening project and the 82-83% unmapped range seen on larger multi-thousand-event days.
- **evidence:** Python scan of `data/catalysts/2026-07-15/catalyst_events.jsonl` (generated this run via the allowed `catalyst-scan` CLI): total=500, mapped=77, unmapped=423 (84.6%). Only 12/423 unmapped rows are Telegram bot-welcome spam (t.me/lookonchain "welcome to Lookonchain" messages) — the rest are genuine but symbol-unresolved headlines, so bot-noise filtering alone would not meaningfully move this number.
- **suggested manual fix:** No new action needed beyond what's already tracked in `project_crypto_ai_desk_news_layer_hardening` memory / prior audit reports — flagging only to confirm the condition is stable, not worsening.
- **priority:** low
- **first observed:** recurring, already tracked (this run only reconfirms current magnitude on a freshly-generated same-morning sample)

### TODO-catalyst-folder-not-pregenerated-overnight
- **issue:** `data/catalysts/2026-07-15/` did not exist when this review started at ~04:40 EEST, even though the default scheduler cycle (02:34-03:06 EEST) had already completed 57/57 steps successfully. This review used its one allowed `catalyst-scan --no-print` fallback to generate it, per the skill's own permission contract — but that means the overnight/Asia review slot (04:30) is structurally the one most likely to hit this gap, since it runs earliest after the first daily cycle.
- **evidence:** `ls data/catalysts/2026-07-15/` returned empty/missing at review start; `cycle_01_02-34_summary.md` step list did not include a distinct catalyst-folder-generation step producing today's date folder ahead of this review's run.
- **suggested manual fix:** Confirm whether the scheduler's own catalyst-scan step is intended to run before or after 04:30 EEST on the daily cycle, and if the ordering is expected to leave this gap every day, no fix is needed (the review's own fallback handles it cleanly); if the ordering was supposed to have already produced today's folder by 03:06, investigate why it didn't.
- **priority:** low
- **first observed:** 2026-07-15 04:40 EEST (this review)
