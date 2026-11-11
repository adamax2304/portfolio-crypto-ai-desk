# Stocks-Intraday SI-1..SI-7 — Integration Fixes (Deliverable)

Date: 2026-07-08 · Scope: **stocks-intraday paper / read-model / actionability only**. Live / auto-live /
manual-live untouched. Crypto untouched. Old stocks swing/invest stay deprecated.

These were **integration bugs**, not cosmetics: until the first two were fixed, the SI-1..5 gates existed
in code but **did not actually protect** paper/actionable entries.

---

## Bugs fixed

**1. pandas DataFrame truthiness → gates silently fail-opened** (`src/stocks/intraday_gate_context.py`)
- `df = _load(...) or _load(...)` raised `ValueError: truth value of a DataFrame is ambiguous` **whenever
  15m data existed** (which is always, for SPY/QQQ). The exception propagated to the agent's `except` and
  the gate result was discarded — so the gate never ran when data was present.
- Fixed both sites (market path + sector path) to an explicit `df = _load(...); if df is None: df = _load(...)`.
- **Proof:** `market_context(now, cfg)` on real cached SPY/QQQ now returns a computed status
  (`stale`, spy −0.336% / qqq −0.667%) instead of raising.

**2. Silent fail-open in the agent gate hook** (`src/stocks/agents/trade_idea_agent.py`)
- The hook's `except Exception:` set `intraday_gate_fields = {}` and left the tier **unchanged** — an
  A/B could stay actionable with no real gate check.
- Now **fail-conservative**: on any gate exception the intraday A/B is demoted to **C**, with
  `cap_reason=intraday_actionability_gate_error`, an avoid-condition, and persisted diagnostics
  (`gate_error`, `gate_error_message`, `market_context_status=error`, `session_rule_status=error`,
  `liquidity_status=error`, `catalyst_quality=unknown`, `demote_reasons=[intraday_actionability_gate_error]`).
  Never re-raises (scheduler never crashes).
- **Proof:** `test_intraday_gate_error_fails_conservative` — with `build_context` forced to raise, a scored-A
  intraday idea comes out **C** with the gate_error fields; `test_swing_unaffected_by_gate_error` confirms
  non-intraday is untouched.

**3. Gate fields not persisted to `proposed_signals.raw_idea_json`** (`src/signals/registry.py`)
- `_safe_idea_payload()` dropped `intraday_actionability`, so the SI-7 classifier / SI-6 packet / report
  could not read *why* a candidate was demoted.
- Added `"intraday_actionability"` to the persisted payload.
- **Proof:** `test_intraday_actionability_round_trips_into_raw_idea_json` reads the field back out of the
  serialized `raw_idea_json`; crypto/non-gated ideas carry `{}` (never error).

**4. LLM-review routing helper existed but was never called** (`src/notifiers/paper_entry.py`)
- Wired `should_route_to_review()` into the paper-entry path, **config-gated and scoped to stocks-intraday
  A/B only**. A fresh `reject`/`wait` review routes the paper candidate to review-only/shadow
  (`telegram_status=shadow_llm_review`); with `require_fresh_llm_review_for_stocks_intraday_ab: true` a
  missing fresh review also routes to shadow (`no_fresh_llm_review`). Missing review does **not** block by
  default. Advisory only — no tier/score/TP/SL mutation, no live, never touches `proposed_signals`.
- **Proof:** `test_intraday_llm_routing.py` — fresh reject→shadow, fresh wait→shadow, missing→not blocked,
  require_fresh+missing→shadow, crypto unaffected.

**5. Post-trade diagnostics wrote `net_pnl_usdt = None`** (`src/stocks/intraday_post_trade_classifier.py`)
- Now LEFT-JOINs `paper_portfolio_ledger` and writes the **terminal (latest) `exit` row's**
  `net_pnl_usdt` as the authoritative USD PnL (`paper_execution_r` stays auxiliary). Missing ledger row →
  `NULL` (never fabricated). Read-only — no writes to the ledger / `final_r`.
- **Proof:** `test_refresh_writes_authoritative_usd_pnl_from_ledger` (latest exit wins; no-ledger→NULL).
  On the real DB: **404 / 1064** post-trade rows now carry USD PnL, sign-aligned with R
  (e.g. +21.79 USD @ +1.0R, −28.31 USD @ −1.0R).

**6. Market context could look fresh off a stale archive** (`src/stocks/intraday_gate_context.py`)
- `market_context()` now flags `status='stale'` when the newest SPY/QQQ bar is from a different NY
  trading day than `now`, or older than `market_context_max_age_sec` (config, default 1800s). The SI-1 gate
  demotes stale via `market_context_unknown_or_stale`.
- **Proof:** `test_market_context_stale_when_data_is_yesterday`, `..._when_bar_too_old_same_day`,
  and the fresh path (`..._does_not_raise_on_dataframe` → status `ok`).

Config: added `intraday_guards.actionability_gates.market_context_max_age_sec: 1800` to `config/stocks/risk.yaml`.

---

## Tests run

| Suite | Result |
|---|---|
| `tests/stocks` (full, incl. 5 new files) | **120 passed** |
| new: gate_context / gate_failclosed / actionability_persist / llm_routing / post_trade | **24 passed** |
| `test_stocks_intraday_hardening` + `test_paper_entry_mode_policy` + `test_paper_shadow_engine` + `test_paper_entry_alerts` | **50 passed** |
| crypto regression (scoring / supervisor / routing / alert / scalp / lifecycle / schedule) | **72 passed** |

**One expected test-only follow-on:** the DataFrame fix made the gate actually run inside
`test_stocks_intraday_hardening.py` (those tests had been passing *because* the bug fail-opened them). Since
that file targets the RR/ATR/structural tiering in isolation, an autouse fixture now neutralizes the
actionability gate there — the gate's real behavior is covered by the dedicated new test files. No production
code was weakened.

---

## Proof gates no longer fail-open

- Bug #1 fix: `market_context` computes on real cached SPY/QQQ (no `ValueError`).
- Bug #2 fix: forced gate exception now **demotes A→C** with an explainable `gate_error` (unit-proven),
  instead of leaving the idea actionable.

## Confirmation — crypto & live untouched

DB invariants immediately before/after running the modified post-trade refresh on the production DB:

| Invariant | Before | After |
|---|---|---|
| `proposed_signals` | 3324 | **3324** |
| `signal_outcomes` | 774155 | **774155** |
| `SUM(final_r)` | 923854.0 | **923854.0** |

Only the additive read-model `stocks_intraday_post_trade_diagnostics` was written. No writes to
`signal_outcomes` / `final_r` / any live/execution table. Crypto regression green. Live remains **LOCKED**.

---

## Follow-up refinements (2026-07-08, round 2)

**R1 — Market-context freshness is now per-symbol (SPY *and* QQQ).** Previously the freshness check
used `newest_last_ts` (the newer of the two legs), so a fresh SPY could mask a stale QQQ and present a
"confirmed" regime. Now each leg's last bar is tracked independently (`spy_last_ts` / `qqq_last_ts`
exposed for diagnostics) and status is `ok` only when **both** legs pass (`all_fresh`); any stale leg
(different NY trading day or too old) → `status='stale'` → SI-1 demotes. Missing leg → `unknown`
(unchanged). **Proof:** `test_market_context_stale_when_one_leg_is_yesterday` (SPY today + QQQ
yesterday → status ≠ `ok`).

**R2 — Post-trade USD PnL now reads the authoritative active fee profile deterministically.** The
ledger holds **one exit row per fee profile** per signal (production: 5 profiles, 850 multi-profile
signals), so the earlier `MAX(timestamp)` selection was non-deterministic. USD PnL is now filtered to
the **active** profile — `config/paper_portfolio.yaml:paper_portfolio.fee_profile` (default
`bybit_non_vip_usdt_perp`, the same key the UI/control-plane headline uses) — and among that profile's
exit rows takes the terminal one by `MAX(rowid)`. No active-profile exit → `net_pnl_usdt=NULL` with
`net_pnl_usdt_source=unavailable_active_profile_missing` (never another profile). The chosen profile is
recorded in `notes_json.fee_profile`. **Proof:**
`test_refresh_writes_authoritative_usd_pnl_from_active_profile` (ignores a 999.0 `zero`-profile row,
NULL when only a non-active exit exists) and `test_usd_pnl_is_deterministic_across_fee_profiles` (same
signal_id, same timestamp, 4 profiles → always the active profile's PnL across repeated runs). On the
real DB: 1063/1064 diagnostics now tagged `fee_profile=bybit_non_vip_usdt_perp`; invariants unchanged.

**Round-2 tests:** `tests/stocks` + `test_stocks_intraday_hardening` → **145 passed**; paper + crypto
regression (`paper_entry_alerts` / `paper_entry_mode_policy` / `paper_shadow_engine` / `scoring` /
`supervisor_smoke` / `intraday_lifecycle`) → **53 passed**. Live still **LOCKED**.
