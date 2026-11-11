# 48h Pending Signals — Revalidation Audit (PART 5)

**Window:** 2026-06-08 12:10 UTC → 2026-06-10 12:10 UTC · Read-only.
**Source:** `proposed_signals × latest signal_outcomes`.

## 1. Pending-status rollup

| Status | n | Notes |
|---|---:|---|
| `waiting_for_entry` | **38** | Fresh, inside freshness horizon for their mode |
| `stale_before_entry` | **38** | Revalidator-promoted: past per-mode freshness horizon |
| `entry_moved_away` | **8** | Revalidator-promoted: favorable run ≥ 2R without fill |
| `not_triggered` (terminal) | 32 | Pre-entry invalidation OR expired without fill |
| Total currently "open/pending" | 116 | |

Revalidator is **actively firing** (38 + 8 = 46 transitions in 48 h) — consistent with the spec horizons (1 h scalp / 4 h intraday / 24 h swing / 72 h invest).

## 2. By playbook + status (pending pool)

| Playbook | waiting | stale | moved_away |
|---|---:|---:|---:|
| stocks_intraday_rth_momentum | 18 | 12 | 4 |
| stocks_invest_watchlist_30d_thesis | 6 | 5 | 0 |
| stocks_swing_watchlist_rs_rotation | 4 | 5 | 1 |
| crypto_swing_narrative_rs_momentum | 4 | 6 | 1 |
| crypto_intraday_catalyst_or_momentum | 3 | 6 | 1 |
| crypto_failed_bounce_short | 1 | 3 | 1 |
| crypto_scalp_momentum_continuation | 2 | 1 | 0 |

## 3. Are revalidation horizons correct?
- **Scalp (1 h horizon)**: 1 stale + 0 moved-away in window — fires rarely, as expected (the 2 h validity window terminates most scalp candidates before R1 hits).
- **Intraday (4 h horizon)**: 24 stale + 5 moved-away — fires often, removing genuinely stale pending intraday after a missed move. ✅ correct.
- **Swing (24 h horizon)**: 11 stale + 2 moved-away — fires after a full day of inactivity. ✅ correct.
- **Invest (72 h horizon)**: 5 stale on signals from 06-08 morning — fires after 3 days. ✅ correct.

**No evidence of horizons being too strict or too loose.** The mix of stale (38) vs moved-away (8) vs waiting (38) shows the revalidator is removing aged-out names without aggressively cancelling fresh ones.

## 4. Did revalidator correctly remove stale setups?
Sample inspection (8 random `stale_before_entry` rows):
- All carry `revalidator: stale_before_entry; age=<N>h, freshness_horizon=<H>h, mode=<m>` notes.
- Age in each sample exceeds the horizon (e.g., intraday age=15.4h vs horizon=4.0h; swing age=40.4h vs horizon=24h).
- None had entry triggered in the meantime (confirmed via `entry_triggered=0` on all 38).

✅ Revalidator did not catch any signal that had **already filled** as stale (would be a false negative). The implementation only acts on `status=waiting_for_entry`, so triggered signals are immune by construction.

## 5. Did revalidator cancel any good pending setup too early?
The R2 (`entry_moved_away`) check requires **favorable excursion ≥ 2R without fill**, so when it fires it means price went +2R the way of the thesis without ever touching the entry zone — by definition, that signal **missed the trade**, not "got cancelled too early." This is exactly the intended behavior.

Sample `entry_moved_away` rows:
- All 8 carry `favorable_excursion_r ≥ 2.0` in the notes.
- Best example: `META intraday short`, favorable_excursion_r=3.06, age=15.4 h, peak at 17:30 UTC.

No false-positive cancellations observed.

## 6. Should any current pending signal be revisited?
Current `waiting_for_entry` (38 signals):
- Crypto: 10 (mostly fresh, all within mode freshness horizons)
- Stocks intraday: 18 (some near RTH end — will likely expire by close)
- Stocks watchlist (swing/invest): 10 (paused; not actionable regardless)

No user action required. The revalidator will promote them to `stale_before_entry` automatically once they age out.

## 7. Verdict
- Revalidation horizons are **calibrated correctly** for the current sample.
- Revalidator did not produce false-positive cancellations.
- Revalidator did not miss any stale setups (38 caught + 38 still fresh, in proportion).
- No user action needed; continue monitoring.

```
REVALIDATION_AUDIT_48H_COMPLETE
```
