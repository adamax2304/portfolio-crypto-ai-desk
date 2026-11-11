# OpenRouter Quality Agents Wiring

Generated: 2026-09-20

## What Changed

- Added OpenRouter-backed advisory refresh for quality agents.
- The API key is expected only in `OPENROUTER_API_KEY`; it is not stored in YAML, SQLite payloads, or launcher files.
- Added `quality_agent_llm_assessments` for structured cached verdicts.
- Added `llm_cached_advisory` to the quality-agent registry. It only reads cached SQLite verdicts in the live hot path.
- Added CLI command: `python -m src.cli quality-agents-openrouter-refresh`.
- Added scheduler step: `quality agents openrouter advisory cache refresh` on long-horizon cycles.
- Added a single-instance guard for `scripts.monitor_heartbeat --event check` so overlapping watchdog runs skip instead of spawning duplicate restart chains.

## Safety Contract

- OpenRouter is never called synchronously during live order routing.
- Cached LLM verdicts are shadow/advisory only.
- LLM reason codes are prefixed as `LLM_*`, so they cannot accidentally become enforced hard-block reason codes.
- API/network/model failures are non-fatal and write `ERROR` rows only.
- Watchdog checks are serialized with `monitor_heartbeat_check.restart.lock`; concurrent checks return `SKIPPED`.

## Current Config

- Config: `config/quality_agents.yaml`
- Provider: OpenRouter
- Env var: `OPENROUTER_API_KEY`
- Model alias: `~anthropic/claude-sonnet-latest`
- Refresh scope: recent canonical news events
- Cache TTL: 360 minutes

## Smoke Result

- `quality-agents-openrouter-refresh --lookback-hours 72 --max-events 1 --force`
- Result: `status=OK`, `targets=1`, `recorded=1`, `errors=0`
- Latest row: provider `openrouter`, status `OK`, symbol `BTC/USDT`

## Verification

- `python -m pytest tests/test_quality_agents.py tests/test_quality_agents_live_integration.py tests/test_default_market_schedule.py tests/test_agent_output_retention.py -q`
- Result: `73 passed`
- Full suite before the watchdog serialization patch: `2489 passed`
- Targeted watchdog/scheduler suite after serialization patch: `84 passed`
