# Paper Monitor Telegram Sample (PART 3)

**Date:** 2026-06-19 · `scripts/paper_monitor_status.py` is Telegram-ready.

## Flags
`--send-telegram` (push) · `--compact` (header + notes only) · `--no-items` / `--top-n N` (cap items) · `--cooldown-min N` (anti-spam, default 90) · `--write-report` · `--window-days N`. Fail-open: if Telegram is unconfigured/unavailable it prints and continues — never raises. Plain text (`parse_mode=""`) — no markdown crash. No `+-` possible (PART 1).

## Compact sample (what the scheduler will push)
```
📊 Paper Monitor Status
Open actionable: 5
Waiting for entry: 0
Entered unresolved: 35
Review/Shadow: 138
No-entry/stale/moved-away: 44
Closed today: 271W / 56L / 0flat
Needs review: 1

Expired split:
  Expired after entry (entered, no TP/SL): 35
  No-entry / stale / moved-away: 44

(full details in report / Control Plane)
```

## Non-compact adds (manual use)
- **Legend** (3 short lines): entered-unresolved ≠ miss · no-entry = never touched/stale/moved · review/shadow = not actionable by policy.
- **Top-5 per bucket** for Open actionable / Waiting / Entered-unresolved, each line: `symbol direction — label · entry touched · paper alerted · reason · lifecycle-R`.

## Clarity guarantees
- "Open actionable: 0" never hides waiting/review/entered-unresolved — an explicit "No open actionable trades, but there are X waiting and Y review/shadow setups (and Z entered-unresolved)." line is added.
- `expired` is always split (entered-after-entry vs no-entry); never one raw "Expired: N".
- `+0R` never shown bare for unresolved (handled by lifecycle-aware R).
- Anti-spam: ≤ 1 send per `--cooldown-min` (state in `data/autostart/paper_monitor_status_state.json`).

## Verdict
**PAPER_MONITOR_TELEGRAM_READY**
