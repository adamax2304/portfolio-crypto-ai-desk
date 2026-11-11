# Post Catalyst Safe-Fix Verification (PART 11)

**Date:** 2026-06-15

## Invariant checklist

| # | Required | Result |
|---|---|---|
| 1 | No scoring changes | ✅ no scoring-agent edits; archive not referenced by scorers |
| 2 | No thresholds changed | ✅ |
| 3 | No TP/SL changed | ✅ |
| 4 | No routing changed | ✅ |
| 5 | No sizing changed | ✅ `config/sizing_weights.yaml` untouched |
| 6 | No C-tier/shadow promoted | ✅ |
| 7 | No stocks swing/invest unpaused | ✅ |
| 8 | No auto-trade path | ✅ |
| 9 | No historical outcomes changed | ✅ SUM(final_r)=75256.0 unchanged; backfill went to separate `signal_catalyst_labels` table |
| 10 | No Telegram spam during tests | ✅ tests use plain dataclass returns / dry paths; 0 live sends |
| 11 | crypto scalp setup Telegram remains suppressed | ✅ `should_suppress_setup_telegram` untouched |
| 12 | paper-entry alerts still enabled | ✅ + now carry catalyst block |
| 13 | close alerts still enabled | ✅ untouched |
| 14 | funding/OI archive writes are append-only | ✅ `INSERT OR IGNORE`, UNIQUE(exchange,symbol,fetched_at) |
| 15 | production scoring does not depend on archive tables | ✅ grep = 0 in both scoring agents |

## DB state (before → after)

| Metric | Before | After |
|---|---:|---:|
| proposed_signals | 1805 | 1805 |
| signal_outcomes | 101768 | 101768 |
| SUM(final_r) | 75256.0 | 75256.0 |
| funding_snapshots (new) | n/a | table created, 0 rows (fills next live cycle) |
| oi_snapshots (new) | n/a | table created, 0 rows |
| signal_catalyst_labels (new, derived) | n/a | 1016 rows |
| stocks news_supported=1 | 0 | 0 historical (fix is forward-only) |

Core trading data is byte-identical. Only additive tables + derived labels added.

## Files changed (all additive / display / archive)

| File | Change |
|---|---|
| `src/signals/registry.py` | news_supported also recognises stocks news_count (label) |
| `src/storage/sqlite.py` | + funding_snapshots / oi_snapshots / signal_catalyst_labels tables + 2 record methods |
| `src/data_collectors/derivatives_archive.py` | NEW best-effort archive helper |
| `src/agents/supervisor.py` | best-effort archive call after derivatives fetch |
| `src/signals/catalyst_labels.py` | NEW display-label helper |
| `src/notifiers/setup_alert.py` + `paper_entry.py` | + 3-line catalyst block |
| `src/analysis/packet.py` | + per-catalyst freshness/source tags |
| `src/stocks/llm_packet.py` | + company-news / analyst-action section |
| `src/stocks/agents/trade_idea_agent.py` | + catalyst_meta from news |
| `scripts/report_fast_move_latency.py` | NEW report tool |
| `scripts/write_obsidian_current_state_dashboard.py` | + §14 catalyst visibility |
| `tests/test_catalyst_safe_fixes.py` | NEW 14 tests |

No agent scoring logic, no threshold, no TP/SL, no routing file modified.

## Scheduler

Not restarted by this task. The supervisor + stocks trade-idea changes load
fresh on the next report subprocess (the scheduler spawns CLI subprocesses), so
the new `news_supported` label + archive writes + catalyst Telegram block go
live on the next cycle without a manual restart. Operator may restart to apply
immediately.

## Verdict

```
CATALYST_SAFE_FIXES_COMPLETE
```
