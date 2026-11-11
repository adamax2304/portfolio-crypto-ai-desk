# Paper Execution / Tracking Audit (PART 1)

**Date:** 2026-06-09 · **Scope:** Read-only audit of the signal-tracking engine. No code/strategy/scoring/TP/SL changes. No data deleted.
**Code surfaces inspected:**
- `src/signals/tracker.py` (564 lines) — `_evaluate_signal_walk`, `_classify`, `track_signal`, `track_active_signals`
- `src/signals/models.py` (266 lines) — `ProposedSignal`, `SignalOutcome`, lifecycle constants, deterministic `signal_id_for`
- `src/signals/config.py` (84 lines) — `SignalTrackingConfig`, R-model defaults, ambiguous policy
- `src/signals/registry.py` (398 lines) — `register_ideas`, idempotent upsert
- `src/storage/sqlite.py` — `upsert_proposed_signal`, `load_active_signals`, `update_signal_status`

## 1. What the tracker actually does
1. `track_active_signals` pulls `proposed_signals` with `status IN (generated, waiting_for_entry, triggered, tp1_hit, tp2_hit)` (sqlite.py:872).
2. For each signal it loads cached OHLCV from `file_store.load_ohlcv(exchange, symbol, tf)` (crypto) or `load_stocks_ohlcv` (stocks), picking the first available timeframe from a per-mode preference list (tracker.py:50-64).
3. `_filter_candles_after(frame, created_at)` keeps only bars at or after the signal's `created_at` — **entry cannot be detected in pre-creation history.** ✅
4. If `expires_at` is set, the candle window is trimmed to `<= expires_at` so an outcome reflects only what was possible inside the validity window (tracker.py:418-423). ✅
5. `_evaluate_signal_walk` iterates chronologically, switching between **pre-entry** mode (only checks entry zone + invalidation) and **in-position** mode (checks stop + TP1/2/3 + MFE/MAE).
6. `_classify` maps the touch flags + expiry flag into a final (`status`, `outcome`, `R`) triple.
7. `track_signal` writes one row into `signal_outcomes` (append-only) and updates `proposed_signals.status` if it changed.

## 2. Answers to the 15 audit questions

### 1. How does the system decide entry was triggered?
- If signal has `entry_low + entry_high` (a **zone**): on a candle where `low <= max(entry_low, entry_high) AND high >= min(entry_low, entry_high)` (geometric overlap).
- If signal has only `entry_trigger` (a **single trigger price**): for long, `high >= trigger`; for short, `low <= trigger`.
- Code: tracker.py:217-258.

### 2. High/low touch or close confirmation?
- **High/low wick touch** for both entry zone overlap and entry trigger. Close confirmation is NOT used.
- Same for stop: `low <= invalidation` for long, `high >= invalidation` for short.
- Same for TPs: `high >= tp` for long, `low <= tp` for short.

### 3. Entry zones vs single entry price?
- Zone path: detect overlap via the OHLC envelope, then pick entry price as:
  - **If candle open is inside the zone** → use the open price (tracker.py:228-230). This is realistic for limit-on-open.
  - **Otherwise** → use the "closer edge" heuristic (tracker.py:232-235). For long: entry = entry_high if low ≤ entry_high. For short: entry = entry_low if high ≥ entry_low.
- Trigger path: entry price = the trigger level itself.

### 4. For LONG signals, what exactly triggers:
| Event | Condition | Where |
|---|---|---|
| entry | candle low/high envelope overlaps entry zone, OR `high ≥ entry_trigger` | tracker.py:220-243 |
| stop | after entry: `low ≤ invalidation` | tracker.py:274-276 |
| TP1 | after entry: `high ≥ tp1` | tracker.py:279-284 |
| TP2 | after entry: `high ≥ tp2` | same |

### 5. For SHORT signals, what exactly triggers:
| Event | Condition |
|---|---|
| entry | overlap, OR `low ≤ entry_trigger` |
| stop | after entry: `high ≥ invalidation` |
| TP1 | after entry: `low ≤ tp1` |
| TP2 | after entry: `low ≤ tp2` |

### 6. If TP and stop both hit inside the same candle (after entry)?
- Detected at tracker.py:290.
- Default policy: `same_candle_conservative=True` (from `SignalTrackingConfig.outcome_ambiguous_same_candle == "conservative"`).
- Conservative path **sets BOTH** TP and stop flags, marks `ambiguous=True`, and `_classify` returns `(STATUS_AMBIGUOUS, OUTCOME_AMBIGUOUS, r_stop=-1R)`. ✅
- A non-conservative branch exists (tracker.py:309-319) but is **not the default** and never invoked unless config overrides.

### 7. Does it track whether entry happened before stop/TP?
- **Yes.** The walk uses a boolean `result.triggered`; while False, the only check is invalidation-before-entry (tracker.py:247-254). Stop/TP cannot accumulate before entry.
- ⚠️ **Representation issue:** When invalidation is hit BEFORE entry, the code sets `result.stop_hit=True` and returns. This is then persisted into `signal_outcomes.stop_hit=1` even though no entry happened. `_classify` correctly returns `STATUS_MISSED_NO_ENTRY, OUTCOME_NOT_TRIGGERED, 0.0R` so headline stats are unaffected, but the `stop_hit=1` flag with `entry_triggered=0` is paradoxical when reading raw rows. **Cosmetic, not stat-affecting.**

### 8. Does it ever mark TP before entry?
- **No.** TPs are checked only inside the in-position branch, which only runs after `result.triggered=True` is set on the same iteration. The pre-entry branch does NOT touch TP fields. ✅

### 9. Does it handle gaps through entry/stop/TP?
- **Entry gaps:**
  - Gap-down BELOW long entry zone (open and close both below the zone, but no overlap): geometric check fails → no entry. ✅ Realistic — a limit buy at a lower zone would not have filled if price gapped below it on the open.
  - Gap-up ABOVE long entry zone: no overlap detected → no entry. ✅
  - Gap-through entry zone (open inside zone after prior bar outside): uses **open price** as fill. ✅
- **Stop gaps:** if `low` is far below stop (long), `stop_hit=True`. But the recorded R is the flat `tracker_config.stop_loss_r=-1.0` — **slippage past the stop is NOT modeled**. The reported R is "what we said the stop was worth", not "what we actually got out at the low/open." Minor for thick liquidity, materially understated for thin alts and stock gaps.
- **TP gaps:** symmetric — credited as a TP1/TP2/TP3 win at flat `+1R/+2R/+3R`, not at the gap-through price. Probably *understates* good wins (and *over*states clean fills).
- **Recommendation (deferred):** record `entry_price_used` vs `tp1` / `stop_loss` for slip-aware audit; do not change R-model yet.

### 10. Bid/ask/spread/slippage or only OHLCV?
- **OHLCV only.** No bid/ask, no spread, no fee model, no slippage curve. Cached OHLCV bars are the only source.

### 11. Stock sessions and market-closed correctly?
- yfinance hourly stock data **only covers RTH** (regular trading hours). Pre-market / after-hours bars are absent from the cache. The tracker implicitly **walks only RTH bars** for stocks. So a stocks intraday signal created during pre-market gets evaluated starting at the 09:30 ET open, which is structurally correct.
- However, **there is no explicit guard** — the tracker doesn't know "this is a stock outside RTH"; it just walks whatever's in the CSV. If a future data source ever included pre-market hourly bars, the tracker would treat them as live without any session-awareness layer.
- Stocks daily bars (4h/1d for swing/invest) include the entire RTH day; that's fine.

### 12. Crypto 24/7 correctly?
- Yes — exchange OHLCV is genuinely 24/7, and the tracker has no special weekend logic. The crypto path is consistent with how the cache is populated.

### 13. Does it update waiting_for_entry setups if the chart structure changes?
- **No.** The tracker is purely candle-walker: it answers "did the levels get touched?", not "is the thesis still valid given the new tape?".
- There is **no regime-change check**, no "price moved away without filling" check, no catalyst-staleness check, no "BTC regime flipped" check.
- The only auto-cancellation is **expiry** (created_at + validity_window_hours → expires_at).
- Feature gap → PART 5/6 spec.

### 14. Does it cancel stale pending signals before expiry?
- **No.** Pending signals stay in `waiting_for_entry` until either:
  - entry triggers (→ `triggered`), or
  - invalidation triggers without entry (→ `missed_no_entry`), or
  - `expires_at` passes (→ `expired` / `missed_no_entry` depending on whether entry happened).
- No early cancellation exists.

### 15. Does it ever move entry/stop/TP after signal creation?
- **Yes — silently, via the registry `ON CONFLICT(signal_id) DO UPDATE` upsert path** (sqlite.py:856-857). 
- Post the PART 10 signal-id fix (models.py:210-261), `signal_id` is now deterministic on `(symbol, mode, direction, tier, calendar_day)` — entry/stop/TP/report_id/HH:MM are deliberately **excluded from the identity hash**. The docstring (models.py:222-246) calls them "trading metadata that mutate as the system re-evaluates."
- This means: if the same (symbol, mode, direction, tier) setup re-fires on the same calendar day, the `ON CONFLICT … DO UPDATE` clause **overwrites** entry_low / entry_high / stop_loss / tp1 / tp2 / tp3 / expires_at with the new cycle's values. The PK is preserved; the levels are updated.
- The tracker then walks against the **latest** levels, while older `signal_outcomes` rows (which are append-only) were computed against earlier levels.
- ⚠️ **This is a known, deliberate design choice** (per the docstring), but is **NOT a version-aware history**: the old levels are gone from `proposed_signals` and there is no `signal_versions` table. The audit trail is implicit (timestamps on `signal_outcomes` rows + git history of report files), not explicit.

## 3. Summary of findings

### Strengths (working as designed) ✅
- TP and stop cannot fire before entry (strict chronological gating).
- Same-candle TP+stop after entry is correctly flagged ambiguous with conservative loss.
- Candle window is trimmed by `created_at` lower bound and `expires_at` upper bound.
- Entry-zone overlap uses the OHLC envelope, with a sensible open-inside-zone fast path.
- MFE/MAE tracked per-candle against the actual filled entry price.
- Idempotent re-registration via deterministic `signal_id`.
- Tracker is read-mostly: never modifies scoring, never sends Telegram.

### Issues / gaps (ranked) ⚠️
| # | Issue | Severity | Stat impact | Recommendation |
|---|---|---|---|---|
| A | **Same-candle ENTRY+STOP** (entry and stop both inside one candle, AFTER trigger): NOT flagged ambiguous. The walk sets `triggered=True` then immediately checks stop on the same bar, producing a clean `STATUS_STOPPED, OUTCOME_LOSS, -1R` without any ambiguity marker. | **HIGH** | overstates losses for scalp signals with stops < 1 bar wide | mark `execution_ambiguous=intrabar_entry_stop` |
| B | **Same-candle ENTRY+TP**: symmetric — entry and TP1 fire in the same bar are credited as a clean `STATUS_TP1, OUTCOME_WIN, +1R`. | **HIGH** | overstates wins for scalp signals where TP1 is close to entry | mark `execution_ambiguous=intrabar_entry_tp` |
| C | **Gap slippage past stop**: stop fill recorded at flat `-1R` even if the candle low pierced well past the stop. | MEDIUM | understates losses for gap-prone alts/stocks | record realized R as `(entry_price_used - low) / risk` (long) and flag `gap_slippage=1`; do NOT change reported R-model in headline stats yet |
| D | **Gap slippage past TP**: symmetric — TP fill recorded at flat `+1R/+2R/+3R` even if the candle high pierced through. | LOW | understates wins | same |
| E | **Pre-entry invalidation recorded as `stop_hit=1` with `entry_triggered=0`** — semantically confusing on raw rows. | LOW (cosmetic) | none — outcome is correctly `not_triggered`, R=0 | rename internal flag to `pre_entry_invalidation` or add a separate column |
| F | **No pending-signal revalidation**: no thesis-stale, no regime-change, no chase-detected, no chart-structure-changed checks. Only static expiry. | **HIGH** | no stat impact today (outcomes are still correct) but user experience suffers — stale pending signals clutter dashboards | new pending-revalidation pass (PART 5) |
| G | **Silent level mutation via upsert**: if same setup re-fires on the same day, entry/stop/TP can be rewritten. The new levels are then used by the next tracker walk. There is no `signal_versions` audit trail. | **MEDIUM** | makes historical R less interpretable when a setup was repriced | add a `signal_revisions` table OR refuse the upsert to mutate levels once the signal is `triggered` |
| H | **No stock-session awareness**: the tracker walks whatever yfinance returns; relies on yfinance excluding pre-market. Brittle to data-source changes. | LOW (today) | none | add an explicit RTH gate for stocks (out of scope for this PR) |
| I | **MFE/MAE → R conversion uses `suggested_entry`, not `entry_price_used`** (tracker.py:449). The MFE pct was computed relative to `entry_price_used`, so the conversion can drift. | LOW | typically <2% error on R | use `entry_price_used` consistently |

## 4. What we will and will not change in PART 7

| Change | Status |
|---|---|
| Detect & flag same-candle entry+stop / entry+TP as ambiguous | ✅ in-scope (additive, conservative) |
| Mark gap slippage past stop/TP with a `notes` annotation; do NOT change headline R | ✅ in-scope |
| Add pending-signal revalidation pass that marks (not mutates) stale/cancelled/needs_reprice statuses | ✅ in-scope |
| Refuse upserts that mutate entry/stop/TP after `STATUS_TRIGGERED` | ✅ in-scope (defensive) |
| Add `signal_revisions` table | ✅ in-scope as additive schema |
| Change R-model (slip-aware R) | ❌ out of scope (would silently rewrite history) |
| Change scoring / thresholds / TP/SL geometry | ❌ out of scope |
| Backfill historical outcomes | ❌ out of scope (no silent rewrite) |
| Re-run tracker against historical OHLCV with new policy | ✅ allowed for diagnostics only — must NOT overwrite existing signal_outcomes rows |

## Verdict
The tracker is **honest and chronologically correct** in the major sense — entry must precede TP/stop, same-candle stop+TP after entry is ambiguous-flagged, expiry trims the candle window. The **two material bugs** are (A) same-candle entry+stop and (B) same-candle entry+TP not being ambiguous-flagged. There is also a structural gap (F) — no pending-signal revalidation — and a silent level-mutation behavior (G) that should be defended against.

These issues will be addressed additively (no historical rewrite, no scoring change) in PART 7 once the reconstruction (PART 3) confirms the bug rate.
