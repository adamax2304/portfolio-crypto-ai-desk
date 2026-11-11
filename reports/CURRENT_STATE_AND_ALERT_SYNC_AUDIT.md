# Current State & Alert Sync Audit (PART 1)

**Date:** 2026-06-14 17:55 UTC

## 1. Active paper positions (entered, not yet closed)

- Total: **1**

| Symbol | Asset | Mode | Dir | Tier | Entry@ | Entry $ | R unrealized | MFE | MAE |
|---|---|---|---|---|---|---|---:|---:|---:|
| SMH | stocks | intraday | long | B | 2026-05-27T13:30 | 602.0399780273438 | -1.0 | 1.157588480206247 | -1.1180693735283722 |

## 2. Waiting / pending setups (last 3d)

- Total: **24**
- By status:
  - stale_before_entry: **20**
  - entry_moved_away: **3**
  - waiting_for_entry: **1**
- Truly waiting (entry still valid): **1**
- Stale_before_entry (do NOT manual-fill): **20**
- Entry_moved_away (do NOT manual-fill): **3**

### Active waiting setups (entry still valid):
| Symbol | Asset | Mode | Tier | Dir | Expires |
|---|---|---|---|---|---|
| OPG/USDT | crypto | intraday | B | long | 2026-06-15T17:17:08+00:00 |

## 3. Recently closed trades

| Window | n closed | wins | losses | expired | raw R |
|---|---:|---:|---:|---:|---:|
| 24h | 10 | 1 | 5 | 4 | -4.0 |
| 48h | 24 | 2 | 14 | 8 | -12.0 |
| 7d | 97 | 27 | 46 | 24 | +0.0 |

## 4. Telegram alerts (last 48h)

- Paper-entry alerts last 48h: **24**
  - status=sent: 24
- Paper-entry alerts today: **8**
- PE alerts whose signal has entry_triggered=1: **24** / 24 (100%)
- Duplicate paper-entry alerts (>1 per signal): **0**
- Untracked legacy alerts (alert_type IS NULL or empty): **0**

## 5. Obsidian dashboard

- Page mtime: 2026-06-14 17:17 UTC (38 min ago)
- Freshness: ✅ fresh
- File size: 22888 chars
- Has §12 low-risk diagnostics: yes
- Has Paper-entry alert lines: yes