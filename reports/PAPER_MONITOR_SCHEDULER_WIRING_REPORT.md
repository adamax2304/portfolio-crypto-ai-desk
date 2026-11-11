# Paper Monitor Scheduler Wiring Report (PART 4)

**Date:** 2026-06-19 · **Type:** scheduler wiring (display step). **No trade logic / execution / LLM added.**

## What was added
A non-fatal step in `support_tail_steps()` (`scripts/run_default_market_schedule.py`), placed **right after `track-signals (post)`** so counts reflect the freshest post-cycle state:
```python
("paper monitor status (telegram)",
 _script("scripts.paper_monitor_status", "--send-telegram", "--compact",
         "--write-report", "--cooldown-min", "90"),
 "command_nonfatal", 0),
```

## Rules satisfied
- **Non-fatal:** `command_nonfatal` — a failure (e.g. Telegram offline) never fails the cycle (the script is also fail-open internally).
- **No spam:** `--cooldown-min 90` (state in `data/autostart/paper_monitor_status_state.json`) → at most one send per cycle (cycles are ~2h apart).
- **Cadence:** once per 2h cycle, after track-signals finalizes statuses.
- **Not in entry critical path:** runs in the support tail, after monitors and tracking.
- **No live/execution/LLM:** read-only DB + Telegram send only.

## Dry-run verification
- Plan builds cleanly; weekday cycle **steps 24 → 25** (one added), weekend 16.
- `build_cycle_steps` inspection: **exactly one** `paper monitor status (telegram)` step, kind `command_nonfatal`; **no duplicate labels**.
- argv contains no `--live` / `execution` / `opus` / `anthropic` / `auto-live` tokens.
- Scheduler self-guard: **"LLM-auto-invoke check OK — no Opus/Claude tokens in plan"**.
- No live/exchange-execution step added.

## Verdict
**PAPER_MONITOR_SCHEDULER_READY**
