# Stocks-Intraday Paper/Actionability Hardening — SI-1..SI-7 (Deliverable)

Date: 2026-07-08 · Scope: **stocks-intraday paper/read-model only**. Live/auto-live/manual-live untouched.
Crypto logic untouched. Old stocks swing/invest stay deprecated (never re-enabled).

---

## 1. What changed

**New modules**
- `src/stocks/intraday_actionability_gates.py` — SI-1..5 pure, fail-conservative, **demote-only** gates
  (market context / sector confirmation / RTH session rules / RVOL+liquidity / catalyst quality) +
  `session_phase()` (DST-safe RTH phases) + `evaluate()` composer returning a full diagnostic `fields` dict.
- `src/stocks/intraday_gate_context.py` — builds the gate inputs from cached OHLCV + already-computed
  idea fields (SPY/QQQ market context cached per (date,hour); RVOL/$-volume/spread-proxy/freshness from
  the name's own 15m bars; sector ETF direction/RS; catalyst-quality mapping). Read-model only.
- `src/stocks/intraday_post_trade_classifier.py` — SI-7 deterministic post-trade classifier
  (why a closed **paper** trade won/lost/expired) over `paper_execution_r` (Model F) + recorded gate
  context. Writes only `stocks_intraday_post_trade_diagnostics`.
- `src/stocks/intraday_llm_review.py` — SI-6 **scheduled (not realtime)** LLM-review packet builder +
  advisory verdict ingest + advisory routing helper. The LLM never trades / changes score/tier/TP/SL /
  unlocks live — it writes an advisory row only.

**Wiring**
- `src/stocks/agents/trade_idea_agent.py` — SI-1..5 demotion hook runs for `mode=="intraday"` A/B ideas
  after the rolling guard, before `TradeIdea` build. Any un-confirmed gate → **A/B→C** (+ named
  `cap_reasons` + an `avoid_conditions` note). Fail-open. Persists `raw.intraday_actionability` (the full
  gate `fields`) so SI-6/SI-7 and the report can read exactly why a candidate was demoted.
- `src/stocks/reports/stocks_report_builder.py` — new **§10 "Intraday Actionability Gates — demotions +
  post-trade diagnostics"**: this-cycle A/B-after-gates count, raw-A/B demoted count, per-reason tally,
  the demoted-candidate watchlist, and the SI-7 post-trade diagnostics block.
- `scripts/run_default_market_schedule.py` — two new scheduler steps (both `command_nonfatal`, stocks-gated):
  `stocks-intraday-post-trade-refresh` (SI-7, before the report) and `stocks-intraday-review-refresh
  --cycle <phase>` (SI-6 packet, after the report). Cycle label auto-derived from the US RTH clock
  (pre_open / after_open / midday / power_hour / eod).
- `src/cli.py` — 3 new commands: `stocks-intraday-post-trade-refresh`, `stocks-intraday-review-refresh`,
  `ingest-stocks-intraday-review`.

**Config** — `config/stocks/risk.yaml` → `intraday_guards.actionability_gates` (enabled, RVOL/$-volume/
spread/data-age thresholds, catalyst strong/medium type lists, `allow_pure_technical_ab`) +
`intraday_guards.llm_review` (`require_fresh_llm_review_for_stocks_intraday_ab: false`, `freshness_minutes: 90`).

**DB (additive only)** — `stocks_intraday_post_trade_diagnostics` (18 cols) and, on first ingest,
`stocks_intraday_llm_reviews`. No schema change to `proposed_signals` / `signal_outcomes` / any live table.

---

## 2. Exact demotion rules (SI-1..5) — each demotes A/B→C, never promotes

| Gate | Demotes A/B→C when | Reason key |
|---|---|---|
| SI-1 Market context | SPY/QQQ context unknown/stale | `market_context_unknown_or_stale` |
| | long into trend_down / both-indices-down (or short into trend_up) | `market_context_conflict` |
| SI-2 Sector | sector ETF direction contradicts trade | `sector_confirmation_conflict` |
| | sector weak/unknown **and** no strong catalyst | `sector_confirmation_weak_or_unknown` |
| SI-3 Session (RTH) | outside RTH | `outside_rth` |
| | premarket (no RTH confirmation) | `premarket_watchlist_only` |
| | first 15m without ORB/opening-drive | `first_15m_requires_orb_or_opening_drive` |
| | lunch without strong confirmation | `lunch_requires_strong_confirmation` |
| | last 30m without trend continuation | `last_30m_requires_trend_continuation` |
| SI-4 RVOL/liquidity | DATA_GAP_LATE / stale data | `data_gap_late` / `data_stale` |
| | RVOL < `min_rvol` (1.5) | `rvol_below_min` |
| | $-volume < `min_dollar_volume` ($20M) | `dollar_volume_below_min` |
| | spread unknown (non-whitelisted) / > `max_spread_bps` (25) | `spread_unknown` / `spread_too_wide` |
| SI-5 Catalyst | medium catalyst without full confirmation; weak/none without exceptional all-confirmed | `catalyst_gate` reason |

**Fail-conservative:** whenever the confirming datum is missing or stale, the produced status is
`unknown`/`stale`, which demotes. Missing data is **never** read as confirmation. C-tier remains
structurally non-actionable (only A/B flow onward).

---

## 3. Current A/B count after gates

- The gates apply at **signal-creation time** to **new** intraday A/B ideas; they do **not** retroactively
  re-tier the 1,721 historical stock-intraday rows already in `proposed_signals`.
- Standalone render of §10 (synthetic 3-idea cycle: 2 A/B + 1 raw-A with market+sector conflict) →
  **actionable A/B after gates: 2 · raw-A/B demoted to C: 1** (reasons `market_context_conflict`,
  `sector_confirmation_weak_or_unknown`), demoted `AMD long` listed as watchlist/review-only. Confirms the
  end-to-end path (persisted `raw.intraday_actionability` → report demotion tally) is correct.
- A live before/after A/B count will populate as the next scheduled `stocks-intraday-report` runs during
  RTH with the hook active.

---

## 4. What remains shadow / advisory

- **SI-6 LLM review is advisory and out-of-band.** The scheduler only builds the packet
  (`reports/STOCKS_INTRADAY_LLM_REVIEW_LATEST.md`); it does not call the LLM. Ingested verdicts land in
  `stocks_intraday_llm_reviews` and only affect routing when the operator opts in via
  `require_fresh_llm_review_for_stocks_intraday_ab` (default **false**) — so by default a missing review
  never blocks anything, and a fresh reject/wait routes a candidate to review-only (advisory demote).
- **SI-7 post-trade classifier is a read-model.** It explains outcomes; it never changes tier/score or
  feeds back into scoring.
- Post-trade classification of the 1,064 closed historical paper trades honestly reports
  **`no_gate_context`** for all 576 losses+expired (they predate the gates) rather than fabricating a
  cause — cause attribution begins with trades created under the SI-1..5 hook.

---

## 5. Tests run

- `tests/stocks` — **105 passed** (incl. 15 gate tests, 9 post-trade tests, 5 LLM-review tests).
- Crypto/cross regression — `test_scoring`, `test_supervisor_smoke`, `test_supervisor_routing`,
  `test_crypto_alert_registration`, `test_crypto_scalp_low_confidence`, `test_intraday_lifecycle`,
  `test_stocks_intraday_hardening` → **66 passed**.
- Scheduler contract — `test_default_market_schedule` → **29 passed**.
- AST parse of all 8 edited/new files → clean. 3 new CLI commands register. Scheduler dry-run places
  post-trade→report→review-packet in the correct order with the right cycle label.
- Guardrail tests assert the SI-6/SI-7 modules contain no `create_order(` / `auto_live` /
  `update proposed_signals` / `update signal_outcomes` / `final_r =` / `insert into proposed_signals`.

---

## 6. Confirmation — live untouched

Invariants captured before and after running both read-model commands against the production DB:

| Invariant | Before | After |
|---|---|---|
| `proposed_signals` total | 3324 | **3324** |
| `signal_outcomes` total | 772738 | **772738** |
| `signal_outcomes` SUM(final_r) | 922116.0 | **922116.0** |

Only the additive read-model table `stocks_intraday_post_trade_diagnostics` (1064 rows) was written.
No writes to `signal_outcomes` / `final_r` / any live/execution table. Live remains **LOCKED**.
