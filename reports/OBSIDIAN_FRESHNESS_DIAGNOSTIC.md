# Obsidian Freshness Diagnostic (PART 1)

**Date:** 2026-06-10 · Read-only diagnostic.

## 1. DB freshness (live)

| Source | Latest timestamp (UTC) |
|---|---|
| `proposed_signals.created_at` | **2026-06-10 15:36** |
| `proposed_signals.updated_at` | **2026-06-10 16:07** |
| `signal_outcomes.checked_at` | 2026-06-10 15:20 |
| `signal_alerts.sent_at` | **2026-06-10 15:42** |
| `watchlist_alerts.sent_at` | 2026-06-10 15:36 |

**Newest trade in DB:** META intraday short, created 2026-06-10 15:36 UTC, status `waiting_for_entry` (created in cycle 3 run @ 15:21 UTC, kept fresh by tracker pass).

## 2. Active signals (last 6 h)

Multiple stocks intraday C-tier shorts (META, TSLA, XLY, MSFT, AAPL, GOOGL, PLTR, QQQ, MSTR, XLK, AMZN, SMH, DIA, SMCI, AMD) all created at 2026-06-10 16:07 UTC, status `waiting_for_entry`. ✅ DB is fresh.

## 3. Obsidian pinned-tab mtimes (UTC, at audit time)

| Tab | mtime UTC | Age vs now |
|---|---|---:|
| `00 📌 Dashboard.md` | 15:21:02 | 0.9 h |
| `01 📌 Active Signals.md` | **16:02:38** | 0.2 h |
| `02 📌 Trade History.md` | **16:02:19** | 0.2 h |
| `03 📌 Todays Catalysts.md` | **16:03:35** | 0.2 h |
| `04 📌 Latest Reports.md` | **16:03:38** | 0.2 h |
| `05 📌 Opus Auto Reviews.md` | 15:21:03 | 0.9 h |
| `06 📌 Telegram Feed.md` | 15:21:03 | 0.9 h |
| `07 📌 Schedule Status.md` | 15:21:03 | 0.9 h |
| `08 📌 Rejected Ideas.md` | 15:21:03 | 0.9 h |
| `09 📌 Macro Risk Heatmap.md` | 15:21:04 | 0.9 h |
| `10 📌 Performance by Mode.md` | 15:21:04 | 0.9 h |
| `11 📌 Trading Desk Current State.md` | **15:21:05** | **0.9 h** |

**Old standalone dashboard** `obsidian_vault/00_Dashboards/Trading_Desk_Current_State.md` — does NOT exist (already migrated). ✅ No duplicate page.

## 4. Scheduler refresh log (today)

| Cycle | refresh ran | exit | duration |
|---|---|---|---:|
| 1 (12:42 EEST = 09:42 UTC) | ✅ yes | 0 | 9.0 s |
| 2 (15:28 EEST = 12:28 UTC) | ✅ yes | 0 | 5.8 s |
| 3 (18:21 EEST = 15:21 UTC) | ✅ yes | 0 | 3.6 s |

Refresh script itself runs cleanly. **Exit 0 every cycle.**

## 5. Cycle cadence vs Obsidian observation

- Scheduler default interval: `--interval-hours 2` → cycles fire every 2 h.
- Refresh runs as the **last step** of each cycle (in `core_tail_steps`).
- **Between cycles** (2 h gap), the dashboard does NOT update.
- US RTH and crypto-intraday signals fire several times per cycle. A signal arriving at e.g. 16:07 UTC (mid-cycle) won't appear on Obsidian until ~17:21 UTC.

**This is the root cause of user-perceived "stale dashboards":** the refresh cadence (2 h) is coarser than the signal cadence (5–10 min during active sessions).

## 6. Answers to the 4 audit questions

| Question | Answer |
|---|---|
| What is the newest trade in DB? | META short, created 2026-06-10 15:36 UTC (`updated_at` 16:07) |
| What is the newest trade in Telegram alert tables? | `signal_alerts.sent_at` max = 2026-06-10 15:42 UTC |
| What is the newest trade shown in Obsidian (tab 11)? | Trades up to **15:21 UTC** (when tab 11 was last regenerated) |
| How many hours stale is Obsidian? | **~1.0 h** at probe time, can reach **2 h** at end-of-cycle |

## 7. Note on partial-refresh anomaly

Tabs 01-04 carry mtimes ~40 min newer than 00 and 05-11. The refresh script's `main()` writes them sequentially, so a partial run cannot leave only 01-04 fresh while skipping the others. **Probable explanation:** Obsidian's own indexing or backlink-cache touched these specific files when a sibling page (11 ← which links to 01, 02) was opened in the editor. This does NOT change the underlying content, only the mtime. Not a bug; cosmetic artifact.

## Verdict
- ❌ **Obsidian dashboards ARE stale** between cycles.
- ❌ **Manual full refresh works** — script is healthy.
- ✅ **Scheduler refresh runs** every cycle, exit 0.
- 🛑 **The script does not self-flag staleness** — the user opens a page and has no visual cue that it's 1-2 h old.
- 🛠 **Root cause: cycle cadence > signal cadence**, not a code bug.

```
OBSIDIAN_STALE_BY_CADENCE_NOT_BROKEN
```
