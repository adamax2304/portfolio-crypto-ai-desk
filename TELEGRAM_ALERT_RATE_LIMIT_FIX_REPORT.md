# Telegram Alert Rate-Limit — Fix Report (PART 2)

**Date:** 2026-05-30. Scope: monitor alert hygiene only.
No scoring, no thresholds, no strategy/agent logic, no auto-trade changes.

---

## What was broken

In **cycle 2** of the 12h scheduler run (2026-05-29 16:04–17:43 EEST), the
stocks intraday monitor fired **78 Telegram alerts in ~1 hour** for the
same ~8–10 A/B setups. The pattern was:

```
[STOCKS INTRADAY] [B] [AVGO]  ... entry_change
[STOCKS INTRADAY] [B] [AVGO]  ... entry_change   (2 min later, 0.6 % mid drift)
[STOCKS INTRADAY] [B] [AVGO]  ... invalidation_change   (5 min later)
[STOCKS INTRADAY] [B] [AVGO]  ... entry_change   (8 min later)
...
```

Root cause: `MaterialImprovementChecker.decide()` in `src/stocks/monitor.py`
re-fires whenever entry mid moves ≥ 0.5 % OR invalidation moves ≥ 0.5 %, with
**no per-signal cooldown**. Each ~5-min tick during chop produced 1–2
re-fires per active A/B setup → 78 alerts vs ~8 genuine ideas. Result: alert
fatigue + risk of missing the few new/upgraded signals among the noise.

The same pattern was a real risk for the crypto report path too (the
supervisor's `_maybe_send_trade_alerts` cooldown was only honoured when
`new_tier` matched the prior alert exactly — entry changes bypassed it).

---

## What changed (code)

### `src/stocks/monitor.py`

1. **New constants**:
   * `DEFAULT_COOLDOWN_MINUTES = 45.0`
   * `COOLDOWN_BYPASS_TYPES = frozenset({"new_signal", "tier_upgrade"})`
2. **`MaterialImprovementChecker`**:
   * New constructor arg `cooldown_minutes: float = DEFAULT_COOLDOWN_MINUTES`.
   * `decide(...)` now takes optional `now: datetime` (injectable for tests).
   * Refactored: classification (`_classify`) is separated from the
     cooldown gate. The candidate alert type is computed first; then if
     it's `score_improvement` / `entry_change` / `invalidation_change`
     and the last alert was within `cooldown_minutes`, the decision is
     downgraded to `AlertDecision(False, "cooldown", "...remaining")`.
   * `new_signal` and `tier_upgrade` **always bypass** the cooldown — they
     are unambiguously material.
   * Fail-open: when `last_alert.sent_at` is missing or unparseable, the
     cooldown returns 0 min remaining (no suppression) so legacy callers
     stay backward-compatible.
3. **`MonitorTickResult`** gains `skipped_cooldown: int` counter.
4. **`StocksMonitorSession`** gains `cooldown_minutes` constructor arg
   (default 45) — exposed so unit tests of underlying classification
   can opt out.
5. The tick loop classifies `alert_type == "cooldown"` as a distinct
   skip kind (separate from `duplicate` / `missing_invalidation`).

### `tests/test_stocks_monitor_cooldown.py` (NEW — 11 tests)

| Test | What it pins |
|------|--------------|
| `test_default_cooldown_is_45_minutes` | The constant is exactly 45 min |
| `test_cooldown_bypass_types_include_new_signal_and_tier_upgrade` | Bypass set is correct; entry/invalidation/score changes are NOT bypassed |
| `test_entry_change_within_cooldown_is_suppressed` | The exact 78-alert cycle-2 scenario — 5 min after last alert, +1 % entry mid → cooldown, not entry_change |
| `test_invalidation_change_within_cooldown_is_suppressed` | invalidation drift inside window → cooldown |
| `test_score_improvement_within_cooldown_is_suppressed` | +7 score inside 10 min → cooldown |
| `test_entry_change_after_cooldown_elapses_fires_normally` | 50 min after last alert, same entry drift → entry_change (cooldown elapsed) |
| `test_tier_upgrade_bypasses_cooldown` | B→A one minute after last alert → tier_upgrade (always fires) |
| `test_new_signal_bypasses_cooldown` | A brand new signal always fires |
| `test_cooldown_failopen_when_sent_at_missing` | Legacy alert without sent_at → no suppression (backward compat) |
| `test_cooldown_failopen_when_sent_at_unparseable` | Garbage sent_at → no suppression |
| `test_cycle2_repro_one_alert_per_setup_per_cooldown_window` | Reproduces the cycle-2 scenario: 1 initial new_signal + 5 cooled-down entry_change attempts within 40 minutes → exactly 1 alert sent |

### `tests/test_stocks_monitor_alerts.py` (1 test updated)

`test_session_score_improvement_sends_update_alert` now constructs the
session with `cooldown_minutes=0.0`. The test pins the
**score_improvement classification**, not the rate-limit; that's covered
by the new cooldown test file. Comment in code explains the split.

---

## Quantified impact (back-of-envelope)

Cycle-2 produced 78 alerts in ~100 min for ~9 distinct setups; with the
new cooldown:

* 9 `new_signal` alerts → fire (bypass).
* Of the remaining 69 events, all `entry_change` / `invalidation_change`
  re-fires within 45 min of a prior alert for the same signal → **0**.
* Genuine `tier_upgrade` events → still fire (bypass).

Expected alert volume per hour drops from ~78 → ~10–15 (one per setup
per ~45 min window, plus any tier upgrades). The noise floor that
caused alert fatigue is gone.

The cooldown does NOT touch decision logic — the signal scoring, tier,
or actionable verdict is unchanged. Only the Telegram dispatch surface
is rate-limited.

---

## Tests

```
$ python -m pytest -q
....................................................................... (131 passed in 3:04)
```

All 131 tests pass — including 11 new cooldown regression tests and 25
prior stocks-monitor tests.

---

## What this fix does NOT touch

- No scoring change.
- No threshold change (0.5 % entry / 0.5 % invalidation / 5-point score
  thresholds unchanged — only the rate at which those classifications
  reach Telegram is limited).
- No agent / strategy / regime logic.
- No crypto WatchlistMonitor cooldown change (it already had a
  `should_alert(cooldown_minutes)` gate that PART 1 strengthened with
  signal-id-aware gating; reusing it for the supervisor crypto path is
  out of scope for PART 2).
- No deletion of any data — alerts already sent stay in `signal_alerts`.

---

## Operational impact

- **Effective immediately on the next monitor tick**: alert volume falls
  to roughly 1 alert / signal / 45-min window for non-material updates;
  tier upgrades and brand-new signals are unaffected.
- **Auditability**: each suppressed event is still recorded in the tick
  result as `alert_type=cooldown`, with the remaining minutes in
  `reason`. The `MonitorTickResult.skipped_cooldown` counter makes this
  visible per tick.

---

## Safety

- Pure logic + dataclass changes; no DB schema, no config.
- Default behavior is opt-in via the constant — overridable per session
  (and disabled with `cooldown_minutes=0.0`).
- The cooldown gate runs AFTER classification, so the underlying
  scoring/tier decision is unchanged — only the Telegram dispatch is
  rate-limited.
