# Paper-Entry / Close Double-Alert Fix — Verification (PART 1)

**Date:** 2026-06-16 · Fix applied (tracker.py mtime): **2026-06-16T08:28 UTC**

## The fix (recap)

`src/signals/tracker.py` dispatch now keys on `status`, not on the placeholder
`final_outcome`:
- `should_alert_paper_entry(entry_triggered, status)` → fires only when
  `entry_triggered and status == STATUS_TRIGGERED` (entered **and** still open).
- `should_alert_close(status, prev_status)` → fires only when `status` is genuinely
  terminal **and** `prev_status == STATUS_TRIGGERED` (a trade previously announced open).

## Historical audit (alerts, last 7d / 24h)

| Window | paper_entry | close_* | signals with BOTH | same-tick (<2s) | pushed sent/sent same-tick | **post-fix same-tick** |
|--------|------------:|--------:|------------------:|----------------:|---------------------------:|-----------------------:|
| 24h    | 53          | 78      | 53                | 30              | 24                         | **0** |
| 7d     | 266         | 275     | 234               | 70              | 64                         | **0** |

alert_type (24h): close_expired 38, close_tp 20, close_stop 20, paper_entry 53,
entry_change 3, tier_upgrade 3, score_improvement 2, invalidation_change 1, new_signal 1.
telegram_status (24h): sent 123, shadow_only 14, error:ConnectTimeout 2, error:ReadTimeout 2.

**Interpretation:**
- The pre-fix same-tick pairs (30 in 24h, 70 in 7d; the close_expired-dominated bundles)
  are **historical and preserved** — not rewritten, per constraint.
- **0 same-tick pairs after the fix timestamp.** Caveat: the last recorded alert is
  08:10 (pre-fix 08:28), so few/no `track-signals` cycles have run post-fix yet — the
  live "0" is consistent with the fix but not yet a large post-fix sample. The
  authoritative proof is the gate logic + exhaustive test below.

## Tests (all passing — `tests/test_alert_dispatch_gates.py`, 10)

| Requirement | Test | Result |
|-------------|------|--------|
| paper-entry only when status==triggered & open | `test_paper_entry_fires_when_entered_and_open`, `test_paper_entry_suppressed_when_already_closed_same_tick` | ✅ |
| close only when status terminal & prev==triggered | `test_close_fires_on_terminal_transition_from_triggered`, `test_close_suppressed_for_open_trade_with_placeholder_outcome` | ✅ |
| **same tick cannot produce both** | `test_no_simultaneous_open_and_close_in_one_evaluation` (exhaustive over all 9×9 status pairs) | ✅ |
| scalp same-tick → no push; scalp legit open → shadow_only | `test_close_suppressed_for_same_tick_round_trip`, `test_scalp_legit_open_routes_shadow_only` | ✅ |
| non-scalp legit close after open still sends | `test_nonscalp_close_after_open_sends` | ✅ |

The exhaustive test proves it is **structurally impossible** for one evaluation
(status, prev_status) to satisfy both `should_alert_paper_entry` and `should_alert_close`
— the simultaneous open+close pair cannot recur.

## Edge behaviors confirmed

- **Scalp same-tick round trip** (`status=expired, prev=waiting`) → neither fires; and
  even a *legit* scalp open (`status=triggered`) routes `shadow_only` (never pushed).
- **Non-scalp legit close** (`status=expired/win/loss, prev=triggered`) → `sent`.
- **Open trade with placeholder** (`status=triggered, final_outcome='expired'`
  placeholder) → close suppressed (the exact production bug) ✅.

**PART 1 status: DONE — fix verified by audit + exhaustive tests; recurrence impossible.**
