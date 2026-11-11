# Final Paper-Monitor Telegram E2E (PART 2)

**Date:** 2026-06-19 · Ran `scripts.paper_monitor_status --send-telegram --compact --write-report --cooldown-min 0` → **"telegram sent"** + report written.

## Live output (verification send)
```
📊 Paper Monitor Status
Open actionable: 5
Waiting for entry: 2
Entered unresolved: 14
Review/Shadow: 151
No-entry/stale/moved-away: 26
Closed today: 269W / 33L / 0flat
Needs review: 0

Expired split:
  Expired after entry (entered, no TP/SL): 14
  No-entry / stale / moved-away: 26

(full details in report / Control Plane)
```

## Assertions — ALL PASS
| check | result |
|---|---|
| no `+-` | PASS |
| no bare "Expired: N" before the split | PASS |
| Open actionable present | PASS |
| Waiting for entry present | PASS |
| Entered unresolved present | PASS |
| Review/Shadow present | PASS |
| No-entry/stale/moved-away present | PASS |
| Closed today present | PASS |
| Needs review present | PASS |
| Expired split present | PASS |
| report written | PASS |
| no "no active trades" hiding states | PASS (explicit buckets) |

`Needs review: 0` here because the default 1-day window excludes the 3 historical `ambiguous` rows (they appear with `--window-days 2`).

## Verdicts
- **PAPER_MONITOR_TELEGRAM_SENT_OR_REPORT_OK** (both: sent + report written)
- **NO_DOUBLE_SIGN**
- **EXPIRED_SPLIT_VISIBLE**
- **STATUS_LANGUAGE_HUMAN_READABLE**
