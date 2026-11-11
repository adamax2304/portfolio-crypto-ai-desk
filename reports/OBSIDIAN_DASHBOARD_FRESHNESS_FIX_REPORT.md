# Obsidian Dashboard Freshness — Fix Report

**Date:** 2026-06-10 · Scope: technical reporting fixes only. No scoring, threshold, TP/SL, signal generation changes. No data deleted. No scheduler restart needed (changes will be picked up on next monitor relaunch).

## 1. Was Obsidian actually stale?
**Yes — by cadence, not by bug.** The full refresh runs once per scheduler cycle (every 2 h). Between cycles, fresh signals fired in the DB but the dashboard pages stayed at the timestamp of the last refresh. Probe at 16:09 UTC: tab 11 mtime was 15:21 UTC (≈48 min behind newest DB row 16:07 UTC).

## 2. Root cause
- Scheduler refreshes the 12 pinned tabs as the **last step of each 2 h cycle** (`scripts.refresh_obsidian_dashboard` → exit 0).
- During the cycle, monitor-watchlist and stocks-monitor-session keep generating fresh signals and sending Telegram alerts, but **no surface refreshes the dashboard between cycles**.
- The dashboard itself had **no self-warning** if it was stale — the user opens an old page and has no visual cue.

## 3. What was fixed
| Change | File |
|---|---|
| **Freshness banner** at the top of tab 11: shows newest-DB-row timestamp + minutes-behind, with a ⚠ STALE warning when age ≥ 30 min | `scripts/write_obsidian_current_state_dashboard.py` |
| **Canonical-path line**: `_Canonical dashboard file: obsidian_vault/11 📌 Trading Desk Current State.md_` at the top so the user can confirm they are reading the right page | same file |
| **`_compute_freshness(db)`** helper: aggregates newest `proposed_signals.created_at / updated_at`, `signal_outcomes.checked_at`, `signal_alerts.sent_at` and computes age vs `now()` | same file |
| **Auto-refresh of tab 11 on every monitor-watchlist tick** (every 10 min by default): the monitor's per-tick loop now calls `build_page()` and writes the canonical file. Best-effort — failure is logged and the tick continues. | `src/cli.py monitor_watchlist` |
| **4 smoke tests** covering: freshness math, stale-warning trigger, fresh-OK render, missing-freshness fallback | `tests/test_obsidian_dashboard_freshness.py` |

## 4. Which file is canonical?
**`obsidian_vault/11 📌 Trading Desk Current State.md`** — single source of truth, written by:
- the standalone CLI (`python -m scripts.write_obsidian_current_state_dashboard`)
- the dashboard refresh chain (`scripts/refresh_obsidian_dashboard.write_current_state()`)
- the new monitor-watchlist per-tick hook

All three import the same `build_page()` function; no path divergence.

## 5. Does manual regeneration work?
**Yes.** `python -m scripts.refresh_obsidian_dashboard` updates all 12 tabs in ~5 s, exit 0. `python -m scripts.write_obsidian_current_state_dashboard` updates tab 11 in ~2 s.

## 6. Does scheduler auto-refresh work?
**Yes** for the per-cycle full refresh (exit 0, three times today). After the new monitor hook is picked up on the next monitor relaunch, tab 11 will refresh **every 10 min** during monitor sessions — closing the cadence gap.

## 7. Do the latest Telegram trades now appear?
Yes. After the regeneration at 16:25 UTC, the page shows the newest signal at 16:07 UTC and the freshness banner reads "✅ 17 min behind newest DB row". Telegram alerts since 15:42 UTC are reflected.

## 8. Was any restart done?
**Not yet.** The freshness banner + canonical path are picked up on the **next** scheduled call (the monitor relaunches on the next cycle, or sooner if the user restarts the monitor manually). No process needed to be killed.

If the user wants the per-tick hook live **immediately**, the monitor-watchlist process needs to be relaunched. Otherwise it will be in effect at the start of the next monitor session.

## 9. What to watch next
- After the next monitor relaunch, tab 11 mtime should refresh roughly every 10 min.
- If the freshness banner reads `⚠ STALE: N min behind` and N keeps growing, that signals the monitor's tick hook is failing — check the `[yellow]dashboard refresh skipped this tick[/yellow]` console line in monitor output.
- Other tabs (00, 02-10) still rely on the per-cycle refresh; if those are also needed sub-hourly, that's a follow-up task.

## Verdict
```
OBSIDIAN_DASHBOARD_REFRESH_FIXED
```

Banner + canonical line + tick-hook + 4 new tests deployed. No strategy/scoring/TP/SL changes; no data deleted; no scheduler restarted by this fix (next monitor cycle picks it up automatically).
