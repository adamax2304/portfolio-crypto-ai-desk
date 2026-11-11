# Crypto Quality Overlay → Paper Portfolio — Authoritative Sizing Integration

Date: 2026-07-08 · Scope: **paper / read-model / accounting only**. Live LOCKED · no live orders ·
`signal_outcomes.final_r` never rewritten · no historical signal/tier/score/TP/SL change · no data deleted.

**The gap this closes:** the overlay routed the paper-entry *alert*, but the paper equity **ledger** still
sized every entered trade full-size — so the app balance/PnL did **not** reflect the overlay's decisions.
Now the ledger is authoritative-consistent with the alert.

---

## What changed

1. **`src/execution/paper_actionability.py` (new)** — `resolve_paper_actionability(conn, signal_id, asset,
   mode, tier)` → `{paper_action, size_weight ∈ {1.0,0.5,0.0}, source, reason, overlay_version}`. Priority:
   1. **Actual paper_entry alert payload** (`cqo_quality_action` / `size_weight` /
      `telegram_status='shadow_crypto_quality'`) — what production really did. Forward trades.
   2. **Lookahead-safe counterfactual reconstruction** (`crypto_quality_counterfactual.overlay_action`) —
      the overlay decision as it WOULD have been at entry. Honest sizing for PRE-overlay historical trades.
   3. **Point-in-time** overlay decision only (`decision_context_type='point_in_time'`). A **current
      snapshot is never used to size a trade** (item 7).
   4. Legacy `actionable()`. **Non-crypto (stocks) always uses legacy only** — never resized.
2. **`scripts/paper_portfolio_backfill.py`** — refreshes the counterfactual first, then `load_trades()`
   calls the resolver per trade: `size_weight ≤ 0` (SHADOW_ONLY/BLOCK) is **excluded** from the actionable
   book; others carry `size_weight / paper_action / size_reason / actionability_source / overlay_version`.
   Prints `full / half / shadow_excluded` + `by_source`.
3. **`src/execution/paper_portfolio.py::simulate_portfolio`** — risk is scaled by `size_weight`
   (`eff_risk_pct = risk_per_trade_pct × size_weight`) so **risk / notional / qty / PnL / costs all halve**
   for HALF_SIZE; `size_weight ≤ 0` skipped defensively. Ledger writes the 5 new fields.
4. **Ledger schema** — 5 nullable columns (`size_weight, size_reason, paper_action, actionability_source,
   overlay_version`) via **additive idempotent `ALTER TABLE ADD COLUMN`** (never drops → the structural
   maker B-book is preserved).
5. **`crypto_quality_overlay_decisions`** — new `decision_context_type` column; `refresh()` writes
   `current_snapshot` (documented as a routing snapshot, NOT historical evidence; the counterfactual is the
   lookahead-safe evidence).
6. **Fail-conservative paper-entry hook** — an overlay exception now applies `default_unknown_data_action`
   (HALF_SIZE) and records `cqo_error` + `cqo_reasons`, instead of silently riding full-size.
7. **Config/docstrings synced** — unknown data lowers confidence + can't upgrade a risky entry mode, but
   does not blanket-demote a clean primary setup (matches the surgical calibration).

---

## Real-DB rebuild — before → after (active profile `bybit_non_vip_usdt_perp`)

Rebuild classified **837** deduped actionable trades: **full=740 · half=97 · shadow_excluded=13**
(`by_source`: `counterfactual_lookahead_safe`=446 crypto, `legacy_actionable_non_crypto`=404 stocks).

| metric | before | after |
|---|---|---|
| net PnL (USD) | +1643.81 | **+1548.98** (−94.83) |
| final equity (USD) | 6643.81 | **6548.98** |
| max drawdown | — | 13.62% |
| tp3 runners in ledger | 80 | **80** (0 excluded; 64 full + 16 halved) |
| structural maker B-book rows | 656 | **656** (preserved) |
| size_weight split | — | 740×1.0 · 97×0.5 |

The −$94.83 is the overlay's paper cost: 13 SHADOW crypto trades removed + 97 halved. It matches the
counterfactual (−$64…−$96 on calm windows) — the honest insurance cost of the soft breaker. **All 80 tp3
runners are retained** (none shadowed; 16 halved), so the runner/profit-lock cohort is preserved.

Sample HALF trade: `WLD/USDT size_weight=0.5 risk_usdt=12.01` (≈ half of the ~25 full-size risk),
`paper_action=HALF_SIZE`, `source=counterfactual_lookahead_safe`. **20/20** sampled SHADOW/BLOCK crypto
signals are **absent** from the active ledger (they no longer inflate/deflate paper PnL).

---

## Tests + verification

- **`tests/test_paper_actionability.py` (new, 11)** — A: HALF halves risk/notional/PnL; B: SHADOW
  (size 0) excluded from ledger; C: legacy fallback + crypto scalp non-actionable + stocks legacy-only;
  D: resolver priority (alert > counterfactual; shadow alert → 0); E: ledger schema additive + idempotent
  (no drop, B-book row preserved); F: overlay exception in the hook → `cqo_error` + HALF (not full);
  G: current-snapshot decisions NOT used for sizing (point-in-time IS).
- **`tests/test_crypto_quality_overlay.py` (18)** + paper_portfolio / paper_entry_alerts /
  paper_execution_accounting / default_market_schedule — **96 passed** total.
- Scheduler dry-run (`--dry-run --crypto-only`) — OK, no auto-LLM tokens.

## Invariants
- `proposed_signals` count **unchanged** (3348) — the read-model adds no signals.
- `signal_outcomes` / `SUM(final_r)` grew only via the **concurrently-running live desk tracker**; the
  ledger rebuild + resolver + counterfactual write **only** `paper_portfolio_ledger` and the additive
  `crypto_quality_*` tables — never `signal_outcomes` / `final_r` / proposed_signals / live.
- Live remains **LOCKED**; no live-order code touched; every behaviour reversible via
  `config/crypto_quality_overlay.yaml`.

## Success criteria
- ✅ Paper-entry actionability and app balance now agree (ledger sized by the same overlay decisions).
- ✅ SHADOW_ONLY/BLOCK crypto trades no longer enter the actionable paper ledger.
- ✅ HALF_SIZE actually halves risk / notional / PnL / costs.
- ✅ Counterfactual runner-safety holds — 0 runners excluded (16 halved, 64 full).
- ✅ System not strangled — 740/837 full size; B-book + stocks untouched.
