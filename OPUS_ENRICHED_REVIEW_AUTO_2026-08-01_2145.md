# Opus Enriched Review — late-session risk review — Auto Cycle 21:30 EEST

## 1. Executive Summary

Late-session risk review, Saturday weekend (crypto-only) mode. **Advisory
only / no auto-trade.** Crypto stays in range/chop with both BTC and ETH in
downtrend, macro risk pinned high at 88.1/100 (risk-off, geopolitical
headline-driven: Iraq/Iran/Jordan strike threat, Ukraine sinking a Rosatom
cargo ship). No A-tier setups cleared the bar in scalp, intraday, or swing
this cycle; scalp remains structurally weak (PF 0.14 over 14d) and posted
zero candidates again. Two active B-tier swing longs (EPIC, AEVO) are
genuine RS leaders but both sit at/above their pullback entry zones — chase
risk, not a clean add here. One active B-tier swing long, **COTI/USDT, is
now technically contradicted**: the fresh swing scan reclassifies it
WATCHLIST-ONLY with a short-leaning thesis after a -16.36% 24h reversal
following a +94% 7d spike (§7, candidate #1) — flag for manual review, do
not treat as a clean hold. The active B-tier XRP/USDT short (waiting for
entry) is aligned with today's fresh scan, which independently reaches the
same short-bias watchlist read. Stocks are closed (weekend); all "active"
stocks signals are stale C-tier carryover from before Saturday, treated as
planning context only. `track-signals` — which was failing 6 consecutive
times as of last night's post-close review — ran clean this cycle
(checked=194, tp_hits=130, expired=9); that outage looks resolved. A new,
first-time anomaly appeared instead: `paper-execution-refresh` timed out
after 300s (11 straight prior cycles ran in 47–182s) — read-model only, no
live impact (§14 TODO-1). Scanning, tracking, and monitors all continue
regardless of mood — this review recommends caution and selective entries,
not a pause.

**External web research not performed this cycle** — internal `news_items`
(24h window) and today's catalyst scan fully covered every candidate
touched below (XRP had fresh internal coverage; EPIC/AEVO/COTI confirmed to
have zero fresh news, verified directly against `news_items.detected_symbols_json`
rather than assumed).

## 2. Data Used

- Reports: scalp (mtime 20:04:56 EEST), intraday (20:09), swing (20:57) —
  crypto, weekend mode, stocks disabled for this cycle. Stocks intraday last
  generated 2026-07-31 20:00 (market closed since); stocks swing/invest last
  generated 2026-07-02 — expected: deprecated in favor of the shadow-only
  stocks position framework, not a freshness fault.
- Catalysts: `data/catalysts/2026-08-01/` — `catalyst_cycle_17-14.md` (mtime
  20:14), `catalyst_events.jsonl` (449 events), `narrative_baskets.jsonl` (5
  baskets).
- CLI: `active-signals` ×2 (crypto 20 rows, stocks 50 rows),
  `signal-stats` ×2, `detect_untracked_legacy_alerts --since 2026-08-01`
  (clean, 0 findings — every legacy crypto alert has a backing
  proposed_signal).
- DB (`db/crypto_ai_desk.sqlite`, read-only): `news_items` freshness checks
  for XRP/EPIC/AEVO/COTI (24h window).
- Reports (read-only artifacts): `CONTEXT_FILTERS_STATUS.md` (17:36),
  `OPEN_INTRADAY_LIFECYCLE_REVIEW.md` (17:58), `PAPER_MONITOR_STATUS_LATEST.md`
  (17:59) for lifecycle/status counts.
- Scheduler log + cycle summary: `data/scheduled_runs/2026-08-01_default_schedule/`
  (`scheduler.log`, `cycle_01_20-01_summary.md`).
- Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-31_2324.md` (post-close,
  23:24 EEST last night) — see §4.

## 3. Scheduler / Data Freshness

- `scheduler.log` mtime 21:01:41 EEST, latest `cycle_01_20-01_summary.md`
  mtime 21:01:40 EEST — both ~44 min old at review time (21:45). Well under
  the 3h defer threshold. **Not deferred.**
- Cycle 1 today: weekend (crypto-only), stocks disabled, 63/64 steps OK, 1
  FAIL (`paper-execution-refresh`, timeout — §14 TODO-1).
- `track-signals (pre)`: **OK** — checked=194, updated=13, tp_hits=130,
  stopped=1, expired=9, not_triggered=52, ambiguous=0, no_ohlcv=0. This
  resolves the multi-cycle failure streak flagged in last night's review
  (TODO-1 there); no longer an open issue tonight.
- Background monitors launched this cycle: crypto watchlist monitor (pid
  7500, 5m cadence), crypto pending monitor (pid 21448, 30s cadence), MEXC
  canary monitor (pid 11456, 3s cadence) — all reported OK at launch.
- Context filters (`CONTEXT_FILTERS_STATUS.md`): live **LOCKED**; stablecoin
  depeg NORMAL, cross-exchange consistency OK (BTC/ETH FULL_SIZE) — the only
  two filters that can reduce Paper entries are both healthy. Token
  unlock/IV-RV/GEX/insider-cluster filters are shadow/advisory only, one
  minor `stocks_options_yfinance_proxy` source error (pre-existing,
  stocks-only, irrelevant on a crypto-only weekend).
- Paper monitor status: OPEN_ACTIVE=1, WAITING_FOR_ENTRY=2,
  REVIEW_ONLY_SHADOW=25, ENTERED_UNRESOLVED_EXPIRED=6, NO_ENTRY_EXPIRED=39,
  CLOSED_WIN=150 / CLOSED_LOSS=15 / CLOSED_FLAT=23, UNKNOWN_INCONSISTENT=4.
- Untracked-alert detector: clean (0 findings) — no PART-1-style integrity
  regression tonight.
- Catalyst mapping coverage is weak this cycle (52.8% unmapped, §5) — treat
  the catalyst layer as context, not a final-decision input, until
  resolved.
- No `OPUS_ENRICHED_REVIEW_AUTO_*.md` file exists for the 04:30, 11:30, or
  18:30 EEST slots today — only this 21:30 run produced output so far (§14
  TODO-4).

## 3A. Agent Council JSON

```json
{
  "session_mode": "scheduled",
  "slot_type": "late_session",
  "as_of": "2026-08-01 21:45 EEST",
  "agents": [
    {
      "agent": "data_quality",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["scheduler_fresh"],
      "data_missing": [
        "paper-execution-refresh timed out this cycle (first time in 11+ prior cycles)",
        "scalp/intraday funnel show 'Scanned on binance/bybit/mexc: 0' — unclear if weekend-normal or a regression"
      ],
      "suggested_effect": "advisory_only",
      "facts_used": ["cycle_01_20-01_summary.md step 25 FAIL", "scalp/intraday report §0 exchange coverage"]
    },
    {
      "agent": "market_regime",
      "verdict": "caution",
      "confidence": 0.75,
      "reason_codes": ["risk_off", "chop", "wait_for_trigger"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing report §1 Market Regime (BTC/ETH downtrend, range/chop)", "swing report §4 macro risk 88.1/100 risk-off"]
    },
    {
      "agent": "catalyst_narrative",
      "verdict": "caution",
      "confidence": 0.55,
      "reason_codes": ["mapping_weak", "fresh_catalyst", "no_catalyst"],
      "data_missing": ["true symbol resolution for ~237 unmapped catalyst_events rows"],
      "suggested_effect": "advisory_only",
      "facts_used": ["catalyst_events.jsonl 449 total / 237 unmapped (52.8%)", "narrative_baskets.jsonl: binance_ecosystem_teaser, ai_narrative, rwa_narrative, perps_dex_narrative, delisting_thin_liquidity"]
    },
    {
      "agent": "derivatives_squeeze",
      "verdict": "caution",
      "confidence": 0.5,
      "reason_codes": ["oi_supports", "squeeze_risk", "data_unavailable"],
      "data_missing": ["Deribit BTC options context failed (ConnectionError) this cycle"],
      "suggested_effect": "advisory_only",
      "facts_used": ["swing report §3 derivatives: AEVO OI 24h +114.74% crowding unknown, funding negative; XRP OI +0.97%, 'fresh shorts pressing, possible squeeze if price reclaims'"]
    },
    {
      "agent": "technical_entry",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["chase_risk", "overextended", "entry_fresh"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["EPIC current 0.9144 vs entry zone 0.8846-0.9052 (above zone)", "AEVO current 0.0208 vs entry zone 0.0197-0.0204 (at/above zone)", "XRP current 1.059 sits inside its 1.0598-1.0610 entry zone"]
    },
    {
      "agent": "execution_lifecycle",
      "verdict": "ok",
      "confidence": 0.7,
      "reason_codes": ["open_actionable", "waiting_for_entry", "review_shadow", "entered_unresolved", "no_entry"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["PAPER_MONITOR_STATUS_LATEST.md operator splits", "active-signals CLI (crypto 20 rows, stocks 50 rows)"]
    },
    {
      "agent": "risk_manager",
      "verdict": "caution",
      "confidence": 0.65,
      "reason_codes": ["headline_risk", "reduce_risk"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["macro risk 88.1/100 (Iraq/Iran/Jordan strike threat, Ukraine sinks Rosatom ship)", "BTC exploit_hack catalyst importance 0.86 (CZ $70M wallet exploit warning)", "COTI reversal (-16.36% 24h after +94% 7d) contradicting the held long swing signal"]
    },
    {
      "agent": "playbook_performance",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": ["playbook_working", "playbook_failing", "low_sample"],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["signal-stats crypto: mode=swing PF 2.07 avgR 0.31; mode=intraday PF 4.71 avgR 1.30; mode=scalp PF 0.125 avgR -0.23 (n=20, weak confidence)"]
    },
    {
      "agent": "head_trader",
      "verdict": "caution",
      "confidence": 0.6,
      "reason_codes": [],
      "data_missing": [],
      "suggested_effect": "advisory_only",
      "facts_used": ["synthesis of all eight agents above"]
    }
  ],
  "head_trader": {
    "overall_verdict": "caution",
    "confidence": 0.6,
    "preferred_side": "mixed",
    "best_long_candidate": { "symbol": "AEVO/USDT", "trigger": "pullback fill into 0.0197-0.0204, hold above 0.0190 invalidation", "reason": "RS leader (+11.24% vs BTC), OI +114.74% (fresh positioning), negative funding (shorts crowded, squeeze fuel), but currently at/above entry zone — wait for the retest, don't chase at 0.0208" },
    "best_short_candidate": { "symbol": "XRP/USDT", "trigger": "already inside its 1.0598-1.0610 short entry zone with invalidation 1.0626 — fresh scan independently confirms the same failed-bounce short-bias read", "reason": "downtrend, RS -0.15% vs BTC, price sitting at the failed-bounce resistance zone; note OI+funding show fresh shorts pressing so a BTC reclaim could trigger a squeeze — keep size modest" },
    "best_catalyst_candidate": { "symbol": "BNB/USDT (binance_ecosystem_teaser basket, w/ ASTER/USDT related)", "trigger": "wait for a retest/pullback after the legal-action headline is digested — do not chase the news print", "reason": "fresh (<1h) basket: 'BNB Chain Takes Legal Action Against Former Employee Over Unauthorized Token Issuance' — sell-the-news / early-rotation risk flagged by the desk's own playbook label" },
    "avoid_candidate": { "symbol": "COTI/USDT", "reason": "held B-tier long swing signal from earlier in the week is now contradicted: -16.36% 24h reversal after a +94% 7d spike, and tonight's fresh scan independently reclassifies COTI as WATCHLIST-ONLY with a short-leaning counter-thesis" },
    "operator_action": "watch",
    "do_not_change": ["scoring", "TP/SL", "entry logic", "routing", "live execution"],
    "todo_count": 5
  }
}
```

## 3B. Agent Council Table

| Agent | Verdict | Confidence | Reason codes | Suggested effect |
|---|---|---:|---|---|
| data_quality | caution | 0.60 | scheduler_fresh | advisory_only |
| market_regime | caution | 0.75 | risk_off, chop, wait_for_trigger | advisory_only |
| catalyst_narrative | caution | 0.55 | mapping_weak, fresh_catalyst, no_catalyst | advisory_only |
| derivatives_squeeze | caution | 0.50 | oi_supports, squeeze_risk, data_unavailable | advisory_only |
| technical_entry | caution | 0.60 | chase_risk, overextended, entry_fresh | advisory_only |
| execution_lifecycle | ok | 0.70 | open_actionable, waiting_for_entry, review_shadow, entered_unresolved, no_entry | advisory_only |
| risk_manager | caution | 0.65 | headline_risk, reduce_risk | advisory_only |
| playbook_performance | caution | 0.60 | playbook_working, playbook_failing, low_sample | advisory_only |
| head_trader | caution | 0.60 | (synthesis) | advisory_only |

## 4. What Changed vs Previous Review

Previous review: `OPUS_ENRICHED_REVIEW_AUTO_2026-07-31_2324.md` (post-close,
23:24 EEST last night, ~22h ago — no intermediate 04:30/11:30/18:30 reviews
exist today, see §14 TODO-4).

- **Resolved:** `track-signals` was failing 6 consecutive times as of last
  night (TODO-1 in the prior review, backlog of 16/21 crypto + 167/175
  stocks signals stuck past `expires_at`). Tonight's cycle ran it clean
  (checked=194, tp_hits=130, expired=9). Worth a follow-up check next cycle
  to confirm the backlog itself has cleared, not just that today's run
  succeeded.
- **New:** `paper-execution-refresh` timeout — first failure in 11+ prior
  cycles (§14 TODO-1, new numbering this review).
- **New:** COTI/USDT long swing signal now technically contradicted by
  tonight's fresh scan (§7 candidate #1) — this signal was not called out
  as a concern in last night's review.
- **Unchanged:** Crypto regime still range/chop with BTC/ETH downtrend; no
  A-tier setups in any crypto mode again tonight (also true last night).
  Scalp mode still structurally weak.
- **Carried forward, not re-verified tonight:** last night's AMZN
  legal-risk false-positive TODO (stocks-only, market closed this weekend —
  will re-surface at the next stocks-enabled slot).

## 5. Catalyst Coverage

- Total `catalyst_events` today: **449**
- Mapped (non-null symbol): **212**
- Unmapped (null symbol): **237** (**52.8%**)
- `narrative_baskets`: **5** (binance_ecosystem_teaser, delisting_thin_liquidity,
  perps_dex_narrative, rwa_narrative, ai_narrative)

**Catalyst mapping weak this run — use catalyst layer as context, not final
decision.** Top 3 unmapped headlines (all Binance futures leverage-limit
notices whose embedded ticker is not being extracted into the symbol
field):
1. "Maximum Leverage Adjusted for JPMUSDT Futures [Aug 1, 2026, 06:00 UTC]"
2. "Maximum Leverage Adjusted for GEVUSDT Futures [Aug 1, 2026, 06:00 UTC]"
3. "Maximum Leverage Adjusted for HYUNDAITUSADT Futures [Aug 1, 2026, 06:00 UTC]"

## 6. Market Landscape

### Market Mood / Risk Routing

- Crypto mood: **risk-off / chop** — BTC and ETH both in downtrend, macro
  risk 88.1/100 driven by geopolitical headlines (Iraq warns of strikes on
  pro-Iran militias if they attack Jordan; Ukraine sinks a Rosatom cargo
  ship in the Black Sea), altcoin breadth thin (45% above EMA20 on swing
  scan, 0% on scalp/intraday scans).
- Stocks mood: **closed** (Saturday, weekend mode — all "active" stocks
  signals are stale C-tier carryover, planning context only).
- Dominant narrative: no single dominant theme — five live baskets
  (binance_ecosystem_teaser <1h fresh, ai_narrative <6h, perps_dex_narrative
  <24h, rwa_narrative, delisting_thin_liquidity <6h). Binance-ecosystem and
  AI-sector rotation are the freshest.
- Preferred side now: **mixed / selective** — favor RS-leader longs only on
  confirmed pullback fills (not at market), favor clean short retests on
  RS-weak names already at trigger zones; do not force new size into either
  side given the risk-off macro backdrop.
- Best long candidate: **AEVO/USDT** — not actionable at current price
  (extended); watch for pullback into 0.0197-0.0204.
- Best short candidate: **XRP/USDT** — already sitting in its 1.0598-1.0610
  entry zone; independently confirmed by both the held B-tier signal and
  tonight's fresh watchlist scan.
- Best catalyst-backed candidate: **BNB/USDT** (binance_ecosystem_teaser
  basket) — fresh legal-action headline, but flagged sell-the-news /
  early-rotation risk; wait for confirmation, don't chase the print.
- What to avoid: **COTI/USDT** (held long, now technically contradicted —
  see §7) and fresh entries into scalp mode generally (PF 0.14, structurally
  unproven).
- What would change the view: BTC reclaiming its local downtrend structure
  (would ease the risk-off tilt and reduce XRP short-squeeze risk); a
  cleaner pullback fill on EPIC/AEVO without a BTC breakdown; catalyst
  mapping recovering above 50% so the catalyst layer can be trusted at full
  weight again.

## 7. Candidate Deep Dives

### 1. COTI/USDT — held B-tier long swing (contradiction risk) — **flag for manual review**

- Held signal: `sig_06b6c2801005f29d`, B-tier, swing, long, score 65.9,
  status=triggered, entry 0.016109-0.016726, invalidation 0.015355, expires
  2026-08-07T14:23:46.
- Has price already reacted to a catalyst? No fresh catalyst verified for
  COTI in `news_items` in the last 24h (checked directly against
  `detected_symbols_json`, per prior guidance not to assert "no catalyst"
  without verification).
- Tonight's fresh swing scan independently re-scores COTI as **WATCHLIST
  ONLY** (score 56.2, low confidence) with a **short-leaning counter-thesis**:
  24h return -16.36% (vs +94.05% 7d — a sharp reversal off a large weekly
  pump), RS vs BTC -15.49%, trend labeled "transition_down," listed among
  tonight's "Weakest Symbols." Derivatives read: "price down + OI down:
  deleveraging or long liquidation."
- Is the setup chasing? The *held* long is now working against the current
  RS/momentum picture, not with it — this is a stale thesis, not a chase.
- Is this candidate aligned with current market mood? No — mood is
  risk-off/chop and COTI is now one of the weakest RS names on the board,
  the opposite of what the original long thesis needed.
- What would invalidate the idea (i.e. confirm the long is still fine)?
  A reclaim of RS leadership vs BTC and a resumption of the uptrend
  structure above the original entry zone; absent that, the long thesis
  looks aged-out.
- **Verdict: manual review required.** Not treated as a clean hold tonight.

### 2. EPIC/USDT — held B-tier long swing (RS leader, currently extended)

- Held signal: `sig_f6259f2dfc6f2f63`, B-tier, swing, long, score 69.5,
  status=triggered, entry 0.884570-0.905221, invalidation 0.859329.
- Current price 0.9144 vs. planned pullback entry zone 0.8846-0.9052 —
  price is **above** the zone (already ran). 24h +23.79%, 7d +33.22%, RS vs
  BTC +24.66%, volume 1.48x. Derivatives: price+OI both up ("fresh
  positioning confirms trend, monitor crowding"); funding mildly positive.
- No fresh catalyst verified for EPIC in the last 24h.
- Is this a chase-risk setup right now? Yes, at current price — the
  playbook's own known failure mode is explicitly "Chase risk after a
  vertical 24h move."
- Actionable now or only after confirmation? Only after a pullback holds
  the 0.8846-0.9052 zone without breaking the 0.859329 invalidation.
- Aligned with market mood? Partially — it's a genuine RS leader, which fits
  a "longs only if RS-leader" routed approach even in a risk-off tape, but
  the entry timing is late.

### 3. AEVO/USDT — held B-tier long swing (RS leader, at/above entry zone)

- Held signal: `sig_bd5eb3cef514b1bf`, B-tier, swing, long, score 67.1,
  status=triggered, entry 0.019748-0.020449, invalidation 0.018957.
- Current price 0.0208, just above the 0.0197-0.0204 entry zone. 24h
  +10.37%, RS vs BTC +11.24%, volume 2.93x. Derivatives: OI 24h **+114.74%**
  (large fresh positioning build), funding negative (-0.00107, "shorts may
  be crowded" per the report's own counter-thesis note — squeeze fuel for
  the long if it continues).
- No fresh catalyst verified for AEVO in the last 24h.
- Chase risk: moderate — closer to its zone than EPIC, but still technically
  outside the preferred pullback band.
- What would invalidate: 1h close beyond 0.0190.
- Aligned with market mood: same read as EPIC — a legitimate RS-leader long,
  entry timing is the open question, not the direction.

### 4. XRP/USDT — held B-tier short swing (waiting for entry, aligned with fresh scan)

- Held signal: `sig_c1e2871dd5fcaf1a`, B-tier, swing, short, score 67.4,
  status=waiting_for_entry, entry 1.0598-1.0610, invalidation 1.0626,
  expires 2026-08-08T18:02:16.
- Fresh internal news (verified in `news_items`, <24h): XRP Ledger upgrade
  coverage (BeInCrypto, CoinDesk) — narrative/technical, not a directional
  catalyst either way.
- Tonight's fresh swing scan independently produces the **same short-bias
  read** for XRP (watchlist idea, "failed bounce/retest zone 1.059-1.061,"
  current price 1.059 — i.e. already inside the zone). 24h -1.03%, RS vs BTC
  -0.15%, downtrend structure.
- Squeeze note: derivatives show "price down + OI up: fresh shorts
  pressing, possible squeeze if price reclaims" — and the report separately
  flags "global long/short ratio is heavily long skewed." Keep size modest;
  this is not a clean one-way short.
- **This is the desk's best short-watch tonight** — already at its trigger
  zone with two independent reads (held signal + fresh scan) agreeing.

## 8. Best Candidates Ranked

1. **Short-watch: XRP/USDT** — already inside entry zone 1.0598-1.0610,
   invalidation 1.0626; two independent reads agree on direction; modest
   size given squeeze risk noted above.
2. **Long-watch: AEVO/USDT** — wait for pullback fill into 0.0197-0.0204,
   invalidation 0.0190; do not chase at 0.0208.
3. **Long-watch: EPIC/USDT** — wait for pullback fill into 0.8846-0.9052,
   invalidation 0.859329; currently extended, higher chase risk than AEVO.
4. **Catalyst-watch: BNB/USDT** (binance_ecosystem_teaser, w/ ASTER/USDT
   related) — wait for retest after the legal-action headline is digested;
   flagged sell-the-news risk, do not chase the print.
5. **Manual review / avoid-as-is: COTI/USDT** — held long contradicted by
   tonight's fresh short-leaning read; not a clean hold.

## 9. Avoid / No Trade

This applies to the current decision window only — never a command to stop
scanning, tracking, or the scheduler.

- **COTI/USDT** (held long) — contradicted by fresh data, see §7 candidate 1.
- **Scalp mode, broadly** — PF 0.14 over 14d (1W/7L), regime itself labeled
  "short bias or no trade; avoid weak altcoin longs," zero candidates
  produced again tonight. Data collection continues; not a manual add
  target.
- **New market-entry chases on EPIC/AEVO at current price** — both are
  extended above their pullback zones; wait for the retest.
- **Stocks, broadly** — market closed; all "active" signals are stale
  carryover, planning/watchlist context only until Monday's open.

## 10. Main Risks

- Macro/geopolitical risk-off backdrop (88.1/100) could accelerate a BTC/ETH
  breakdown, which would invalidate both EPIC and AEVO long theses
  simultaneously (correlated risk — same playbook, same "BTC dump
  invalidating correlated swing longs" failure mode noted in both).
- XRP short carries squeeze risk if BTC reclaims local structure (long/short
  ratio heavily long-skewed, fresh shorts pressing per OI+funding read).
- BTC exploit_hack catalyst tonight (CZ warning re: $70M wallet exploit,
  importance 0.86) plus a separate Coldcard hardware-wallet theft story — a
  headline-driven BTC risk-off spike is a live tail risk this session.
- Catalyst mapping at 52.8% unmapped this cycle — any catalyst-driven
  decision (including the BNB/ASTER catalyst-watch above) should be treated
  as directionally useful but not fully verified coverage.
- `paper-execution-refresh` timeout (§14 TODO-1) means the paper P&L
  accounting read-model may be one cycle stale until it succeeds again —
  read-model only, does not affect live (live is locked) or the signals
  above.

## 11. Action Plan — next 4 hours

- Watch XRP/USDT for confirmation/rejection at the 1.0598-1.0610 zone;
  invalidation 1.0626.
- Watch AEVO/USDT and EPIC/USDT for a pullback retest into their stated
  entry zones; do not chase either at current price.
- Manually review the COTI/USDT held long against the fresh short-leaning
  read (§7 candidate 1) — decide whether to tighten, flag, or leave as-is;
  this review does not close or resize it.
- Re-check `paper-execution-refresh` on the next cycle to confirm the
  timeout was transient.
- Re-check catalyst mapping % on the next cycle; if still >50% unmapped,
  escalate TODO-2 priority.

## 12. Final Verdict per Mode

- **Scalp (crypto):** No trade. Structurally weak (PF 0.14); avoid weak
  altcoin longs; short bias only if a clean setup appears (none tonight).
- **Intraday (crypto):** No trade. Zero A/B candidates this cycle; BTC/ETH
  both capped to C-tier (squeeze risk / catalyst risk event respectively).
- **Swing (crypto):** Selective / watch-only. XRP short is the cleanest
  actionable read (already at trigger). EPIC/AEVO longs are real RS leaders
  but need a pullback, not a chase. COTI long needs manual review, not a
  clean hold.
- **Stocks (all modes):** Market closed. Planning/watchlist context only;
  no actionable verdict until Monday's session.

## 13. Sources

Internal sources only this cycle (no external web research performed —
internal coverage was sufficient and fresh, see §1/§2):

- [data/reports/swing/2026-08-01_17-57_swing_report.md](data/reports/swing/2026-08-01_17-57_swing_report.md) (2026-08-01 20:57 EEST)
- [data/reports/intraday/2026-08-01_17-09_intraday_report.md](data/reports/intraday/2026-08-01_17-09_intraday_report.md) (2026-08-01 20:09 EEST)
- [data/reports/scalp/2026-08-01_17-05_scalp_report.md](data/reports/scalp/2026-08-01_17-05_scalp_report.md) (2026-08-01 20:04 EEST)
- [data/catalysts/2026-08-01/catalyst_cycle_17-14.md](data/catalysts/2026-08-01/catalyst_cycle_17-14.md) (2026-08-01 20:14 EEST)
- [reports/CONTEXT_FILTERS_STATUS.md](reports/CONTEXT_FILTERS_STATUS.md) (2026-08-01 20:36 EEST)
- [reports/PAPER_MONITOR_STATUS_LATEST.md](reports/PAPER_MONITOR_STATUS_LATEST.md) (2026-08-01 20:59 EEST)
- [reports/OPEN_INTRADAY_LIFECYCLE_REVIEW.md](reports/OPEN_INTRADAY_LIFECYCLE_REVIEW.md) (2026-08-01 20:58 EEST)
- `db/crypto_ai_desk.sqlite` `news_items` table — direct query, XRP/EPIC/AEVO/COTI, 24h window (2026-08-01 21:4x EEST)
- `data/scheduled_runs/2026-08-01_default_schedule/cycle_01_20-01_summary.md` (2026-08-01 21:01 EEST)
- Prior review: [OPUS_ENRICHED_REVIEW_AUTO_2026-07-31_2324.md](OPUS_ENRICHED_REVIEW_AUTO_2026-07-31_2324.md)

## 14. Fix Requests / TODO

### TODO-1
- **issue:** `paper-execution-refresh` timed out after 300s this cycle —
  first failure after 11+ consecutive successful cycles (typical runtime
  47-182s).
- **evidence:** `data/scheduled_runs/2026-08-01_default_schedule/cycle_01_20-01_summary.md`
  step 25: `[FAIL] paper execution accounting refresh (exit=-1, 300.1s,
  attempts=1)` — `Command ... timed out after 300 seconds`. Compare to prior
  10 cycles in `data/scheduled_runs/2026-07-30_default_schedule/` and
  `2026-07-31_default_schedule/`, all `[OK]` with `scanned` counts steadily
  growing (3094 → 3135).
- **suggested manual fix:** Check whether the growing scanned-row count
  (3135+ and climbing) is approaching a query-performance cliff; consider
  adding an index or incremental/windowed scan instead of a full rescan
  each cycle. Read-model only — no live impact, but will keep failing if
  the table keeps growing at this rate.
- **priority:** medium
- **first observed:** 2026-08-01 21:01 EEST

### TODO-2
- **issue:** Catalyst symbol mapping is weak this cycle (52.8% unmapped,
  237/449 rows). Sample unmapped headlines are all Binance futures
  "Maximum Leverage Adjusted for `<TICKER>`USDT Futures" notices where the
  ticker is present in the headline text but not being extracted into the
  `symbol` field.
- **evidence:** `data/catalysts/2026-08-01/catalyst_events.jsonl` — direct
  count via script, 449 total / 212 mapped / 237 unmapped. Sample: "Maximum
  Leverage Adjusted for JPMUSDT Futures", "...GEVUSDT...", "...HYUNDAITUSADT...".
- **suggested manual fix:** Add a resolver rule for the recurring
  "Maximum Leverage Adjusted for `<TICKER>`USDT Futures" Binance
  announcement pattern in the catalyst symbol resolver — this looks like a
  narrow, high-volume, easily-parsed source rather than a general mapping
  problem.
- **priority:** medium
- **first observed:** 2026-08-01 21:45 EEST

### TODO-3
- **issue:** Scalp and intraday exchange-coverage funnels both show
  "Scanned on binance/bybit/mexc: 0" and `universe=0` this cycle, while the
  swing report (same cycle, same day) shows healthy universe/scanned
  counts (binance universe=456, scanned=60; etc). Intraday's `ohlcv_fetched`
  counts are non-zero (51/84/79) despite `universe=0`, which is internally
  inconsistent.
- **evidence:** `data/reports/scalp/2026-08-01_17-05_scalp_report.md` §0 and
  `data/reports/intraday/2026-08-01_17-09_intraday_report.md` §0.
- **suggested manual fix:** Confirm whether `universe=0` + `Scanned on X: 0`
  for scalp/intraday is expected weekend/mode-specific behavior (e.g. a
  smaller fixed universe by design) or a regression in the liquidity/momentum
  filter step for those two modes specifically. If expected, consider fixing
  the `universe` field display so it doesn't read as 0/broken.
- **priority:** low
- **first observed:** 2026-08-01 21:45 EEST

### TODO-4
- **issue:** No `OPUS_ENRICHED_REVIEW_AUTO_*.md` files exist for today's
  04:30, 11:30, or 18:30 EEST slots — only this 21:30 run has produced
  output so far today.
- **evidence:** `ls OPUS_ENRICHED_REVIEW_AUTO_2026-08-01*.md` returns no
  matches; most recent prior file is `OPUS_ENRICHED_REVIEW_AUTO_2026-07-31_2324.md`.
- **suggested manual fix:** Check the scheduled-task / cron history for
  `opus-enriched-review-4h` and its sibling pre-us/post-close tasks to
  confirm whether today's earlier slots fired and failed silently, or did
  not fire at all.
- **priority:** medium
- **first observed:** 2026-08-01 21:45 EEST

### TODO-5
- **issue:** COTI/USDT held B-tier long swing signal (`sig_06b6c2801005f29d`,
  triggered days ago) is now contradicted by a sharp reversal (-16.36% 24h
  after +94.05% 7d) and by tonight's independent fresh scan, which
  reclassifies COTI as WATCHLIST-ONLY with a short-leaning counter-thesis.
- **evidence:** `active-signals --asset-class crypto` (COTI row, status
  triggered, expires 2026-08-07); `data/reports/swing/2026-08-01_17-57_swing_report.md`
  lines ~48 (weakest symbols) and ~720-780 (Trade Idea #6, WATCHLIST ONLY
  COTI/USDT, short-leaning counter-thesis language).
- **suggested manual fix:** Manual review of the COTI position (see §7
  candidate 1, §11 action item). Separately worth considering: does the
  swing playbook need a rule to flag/demote an aging held signal when the
  symbol's RS flips from strongest-to-weakest between cycles?
- **priority:** medium
- **first observed:** 2026-08-01 21:45 EEST
