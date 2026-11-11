# Status Language Grep Audit (PART 5)

**Date:** 2026-06-19 · Source-only (`src/`, `scripts/`, `*.py`); generated `data/`, `reports/`, logs excluded.

## Findings & classification
| Pattern | Hit | Class | Action |
|---|---|---|---|
| `+-` literal | comments in `close_alert.py`, `display_status.py` | harmless (doc) | none |
| `+-` literal | `scripts/_sector_diag.py` regex `[+-]?` char-class | harmless (regex) | none |
| manual `+{…r…}` | `stocks/agents/trade_idea_agent.py:375,377` RS evidence | **guarded** — emitted only `if rs > 0` → `+` always correct | none |
| manual `+{…}` | `stocks/monitor.py:181` score delta | guarded — only on score-improvement event (delta>0) | none |
| manual `+{…}` | `audit_expired_positive_mfe.py:104`, `write_obsidian_current_state_dashboard.py:1237` | inherently-positive uplift figures (report-only) | none |
| `no active signals` | `src/cli.py:969` | **CLI-only** — the literal `active-signals` list (terminal/scheduler-log, not Telegram). It IS the active list, not a claim that nothing exists | acceptable; Telegram clarity comes from `paper_monitor_status` |
| `no active trades` | only in `display_status.py` docstring (describing old style) + scheduler comment | harmless (doc) | none |
| bare `Expired:` | only `paper_monitor_status.py` docstring (describing the OLD bad style) | harmless (doc) | none |
| duplicate status mapping | none outside `src/status/display_status.py` (+ Control-Plane mirror) | single source | none |

## Live / user-facing bugs found
**None.** No `+-`, no bare-`Expired:`, no context-free `+0R`, and no "no active trades" can reach a live Telegram/app surface:
- The Telegram monitor summary is `scripts/paper_monitor_status.py` (canonical module) — verified clean (PART 2).
- Close alerts use `:+.1f` + lifecycle wording (PART 3).
- The only `no active signals` string is the CLI `active-signals` command (terminal output), which is the literal active list, not the operator Telegram summary.

## Verdict
**NO_OLD_STATUS_LANGUAGE_IN_LIVE_OUTPUT**
