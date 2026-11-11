# Agent Council Routine Prompt — Test Results (PART 10)

**Date:** 2026-06-19

## Prompt validator — `scripts/validate_agent_council_prompt.py`
Read-only checker over the scheduled SKILL.md + repo protocol. **Result: OK (exit 0), 52/52 checks PASS.**

Required checks — all PASS:
| Check | Result |
|---|---|
| Permission contract present | PASS |
| ALLOWED / FORBIDDEN sections present | PASS |
| No-permission-prompt absolute rule present | PASS |
| No code edits / no pytest / no scheduler restart / no auto-trade (forbidden) | PASS |
| ALWAYS-SCAN — never stop scanner/monitor/system | PASS |
| TODO-only maintenance section present | PASS |
| Agent Council mode section present | PASS |
| "one LLM run, not physical agents" present | PASS |
| All 9 virtual agents listed (data_quality … head_trader) | PASS |
| Agent Council JSON block present (head_trader, overall_verdict, suggested_effect) | PASS |
| JSON advisory_only present | PASS |
| Render structure has Agent Council JSON + Table (3A/3B) | PASS |
| Slot awareness preserved + all 6 slots (04:30…23:15) | PASS |
| Status-language section + expired split + no-bare-+0R + lifecycle terms | PASS |
| Telegram ≤ 3500 chars rule + Status block + advisory-only | PASS |
| Protocol §17 mirrors agents + status language + advisory-only | PASS |

## Regression (existing repo tests — confirm nothing broke)
- `pytest tests/test_project_state_docs.py tests/test_ingest_enriched_review_sources.py -q` → **14 passed**.
- `python scripts/check_project_state_docs.py` → **OK**.

## Notes
- The validator runs over the live scheduled SKILL at `~/.claude/scheduled-tasks/opus-enriched-review-4h/SKILL.md`; it skips gracefully (with a WARN) on a host where that routine isn't installed, and still validates the repo protocol §17.
- No forbidden command was run from inside any scheduled routine; this was a manual coding session with permission to run tests.

## Verdict
All required prompt invariants verified; no regression.
