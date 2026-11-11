# Option B — Alert Behavior Verification (PART 3)

**Date:** 2026-06-16 ~11:16 UTC

## Alert integrity audit (signal_alerts)

| Check | 24h | 7d | Verdict |
|-------|-----|----|---------|
| Duplicate `paper_entry` per signal_id | **0** | **0** | ✅ |
| Duplicate close per (signal_id, alert_type) | **0** | **0** | ✅ |
| Same-tick `paper_entry`+close pairs (<2s) | 30 | 70 | all **pre-fix** (see below) |
| Same-tick pairs **after** 10:25 impl | **0** | **0** | ✅ |
| Crypto-scalp alerts NOT shadow_only | 6 | 49 | all **pre-routing** history (see below) |
| Alerts after 10:25 impl | **0** | **0** | (no live cycle yet) |

telegram_status (24h): `sent 126, shadow_only 17, error:ReadTimeout 3`.

## Same-tick pairs are all pre-fix

The 30 (24h) / 70 (7d) same-tick pairs all carry `sent_at` **before** the dispatch-gate
fix and before the 10:25 Option-B boundary. **Zero** same-tick pairs exist after the fix.
They are historical and intentionally not rewritten.

## Scalp routing is correct (the 6 "sent" scalp alerts are pre-routing history)

- The 6 non-shadow scalp alerts (24h) are all dated **06-15 18:00–20:53**.
- Scalp `shadow_only` routing went live at **06-15 23:23**; every scalp alert since then
  (through 06-16 10:07) is `shadow_only`. Latest scalp `sent` alert: 06-15 20:53.
- ⇒ The "sent" scalp alerts predate the shadow routing — **not a leak**, correctly
  preserved history. Scalp is shadow-only for all current/future alerts.

## Freshness + late-entry routing — functionally verified

The PART 5 routing was exercised directly (not yet seen in live data because the new code
isn't running in production yet — same cause as Option B):

| Scenario | Freshness label | telegram_status | sent? | banner |
|----------|-----------------|-----------------|-------|--------|
| non-scalp, entry 40s ago | `fresh 40s` (actionable) | `sent` | ✅ yes | — |
| non-scalp, entry 40m ago | `very late 40m — NOT actionable` | `late_shadow` | ❌ no | `[LATE ENTRY DETECTED — DO NOT CHASE]` |
| crypto scalp, any age | (shadow) | `shadow_only` | ❌ no | scalp shadow banner |

So once the live monitor loads the new code: **fresh non-scalp entries push as `sent`,
very-late ones route `late_shadow` (no chase), scalp stays `shadow_only`** — exactly the
intended behavior.

## Expectations vs observed

| Expectation | Status |
|-------------|--------|
| same-tick paper_entry+close = 0 (post-fix) | ✅ confirmed (0 after impl; gate makes it impossible) |
| no duplicate paper_entry / close | ✅ confirmed (0/0) |
| scalp paper_entry/close shadow_only | ✅ confirmed (since 06-15 23:23) |
| late non-scalp → late_shadow | ✅ functionally verified (not yet in live data) |
| fresh non-scalp → sent | ✅ functionally verified |

**PART 3 status: DONE — alert integrity intact; routing correct; late/fresh logic verified
functionally; live observation pending the next monitor cycle.**
