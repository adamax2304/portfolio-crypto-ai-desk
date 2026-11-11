# Crypto Swing Breakout Refinements (Shadow)

- Forward-only `preentry_v2` new-logic breakout cohort; missing, late, and gap-tainted latency evidence is excluded.
- The native breakout control and each refinement use the same Model-F execution and fee profile.
- This report changes neither Paper geometry nor live routing. No profile is auto-promoted.

- generated_at: `2026-11-11T21:20:26.273688+00:00`
- source_signals: `226`; load skips: `{"bad_geometry": 0, "ohlcv_unavailable": 176}`

| profile | clean signals | entered | closed | skipped | net USD | paired delta USD | PF | win% |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| `control_clean` | 41 | 16 | 16 | 25 | 86.06 | 0.00 | 1.40 | 31% |
  - skips: `{"btc_swing_direction_not_confirmed": 14, "overlay_not_actionable": 10, "pre_entry_invalidation": 1, "unresolved": 1}`
| `long_reclaim_retest` | 41 | 0 | 0 | 41 | 0.00 | 0.00 | - | - |
  - skips: `{"btc_swing_direction_not_confirmed": 13, "direction_not_profile": 2, "overlay_not_actionable": 10, "retest_not_confirmed_in_window": 16}`
| `long_reclaim_retest_rvol` | 41 | 0 | 0 | 41 | 0.00 | 0.00 | - | - |
  - skips: `{"btc_swing_direction_not_confirmed": 13, "direction_not_profile": 2, "overlay_not_actionable": 10, "retest_not_confirmed_in_window": 1, "rvol_too_low_or_unavailable": 15}`
| `short_failed_retest` | 41 | 0 | 0 | 41 | 0.00 | 0.00 | - | - |
  - skips: `{"btc_swing_direction_not_confirmed": 1, "direction_not_profile": 39, "retest_not_confirmed_in_window": 1}`
| `short_failed_retest_rvol` | 41 | 0 | 0 | 41 | 0.00 | 0.00 | - | - |
  - skips: `{"btc_swing_direction_not_confirmed": 1, "direction_not_profile": 39, "rvol_too_low_or_unavailable": 1}`

A refinement needs at least 30 clean closed forward trades, 28 forward days, positive USD PnL, PF >= 1.25, and positive paired delta before human Paper review.
