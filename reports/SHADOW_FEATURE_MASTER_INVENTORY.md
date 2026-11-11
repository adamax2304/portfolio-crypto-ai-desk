# Shadow Feature Master Inventory (PART 1)

**Date:** 2026-06-24. Source of truth: `docs/SHADOW_MODE_REGISTRY.md` + `config/paper_features.yaml` (new) + code scan of `src/exits`, `src/risk`, `src/execution`, `src/intelligence`, `src/signals`, scheduler steps, Control Plane. READ-ONLY discovery.

| feature | module/file | status now | kind | what it does | affects trades? | ledger/data | tests | last decision | risk | recommendation |
|---|---|---|---|---|---|---|---|---|---|---|
| Model F / paper_execution_r | `src/execution/paper_execution_accounting.py` | ACTIVE paper accounting | accounting | early MFE-armed protection PnL | no | `paper_execution_outcomes` | yes | 2026-06-24 | low | keep active |
| touch_r relabel (optimistic) | `backend/app/books.py` | ACTIVE display | display | demote final_r to signal-quality | no | n/a | yes | 2026-06-24 | low | keep active |
| lifecycle status clarity | `src/status/display_status.py` | LIVE-DISPLAY | display | expired split, lifecycle R | no | n/a | yes | 2026-06-19 | low | keep active |
| close-alert lifecycle + paper line | `src/notifiers/close_alert.py` | LIVE-DISPLAY | display | honest close R + Model F line | no | signal_alerts | yes | 2026-06-24 | low | keep active |
| risk-guard warnings | `src/risk/risk_guards.py` (in `paper_entry.py`) | LIVE alert-only advisory | advisory | circuit-breaker/sector-cap/correlation/profit-hint as warning lines, fail-open | no (never blocks) | alert text | partial | 2026-06-19 | low | keep active (surface in panel) |
| circuit breaker (block) | `src/risk/circuit_breaker.py` | NEED_MORE_DATA (alert-only) | risk | would_pause computation | no | dry-run csv | yes | 2026-06-19 | med | keep shadow |
| sector/concentration/correlation caps (block) | `src/signals/sector_cap_shadow.py` | NEED_MORE_DATA (shadow) | risk | would-bind cap | no | shadow log | partial | 2026-06-19 | med | keep shadow |
| position/leverage advisor | `src/risk/position_advisor.py` | SHADOW label-only | risk | size/leverage hint | no | none | partial | 2026-06-19 | low | keep measuring |
| risk-off label | `src/risk/risk_off.py` | LIVE-ADVISORY measurement | data | risk-off regime label | no | csv | yes | 2026-06-19 | low | keep measuring |
| shadow exit manager variants A–I | `src/exits/shadow_exit_manager.py` | SHADOW research (NOT wired) | risk | BE/partial/trailing replay | no | ledger csv | n/a | 2026-06-24 | low | **archive (superseded by Model F)** |
| adaptive TP3 / TP policy | `scripts/tp_stop_replay.py` | research/advisory | risk | TP-count counterfactual | no | csv | yes | 2026-06-23 | low | keep measuring |
| cohort guard (crypto_intraday_catalyst) | `config/cohort_guard.yaml` | default-off → **warn** | display | weak-cohort label | no | n/a | yes | 2026-06-24 | low | **promote to warn (display)** |
| intelligence layer (timeline/derivatives/squeeze) | `src/intelligence/` | SHADOW/NEED_MORE_DATA | data/advisory | per-symbol context | no | data/intelligence | partial | 2026-06-19 | low | keep measuring |
| catalyst label refresh + integrity | `src/signals/catalyst_label_refresh.py`, catalyst scan | LIVE-ADVISORY (scheduler) | data | news_supported/integrity | no | news_items/labels | yes | 2026-06-19 | low | keep active |
| funding/OI archive | scheduler `ohlcv_archive`/`intelligence_update` | LIVE data | data | append-only archive | no | snapshots | yes | 2026-06-18 | low | keep active |
| crypto scalp actionable | `config/signal_tracking.yaml` | LOCKED-POLICY shadow | filter | scalp non-actionable | no | n/a | yes | 2026-06-18 | high | **dangerous — keep locked** |
| stocks C-tier actionable | `config/signal_tracking.yaml` | LOCKED-POLICY shadow | filter | C-tier shadow_review_only | no | n/a | yes | 2026-06-18 | high | **dangerous — keep locked** |
| stocks swing/invest actionable | `src/agents/trade_idea_agent.py` | LOCKED-POLICY paused | filter | swing/invest watchlist-only | no | n/a | yes | 2026-06-18 | high | **dangerous — keep locked** |
| no-chase / overextension filter | scoring rejection | LIVE production filter | filter | rejects chase entries | yes (prod, existing) | rejected_ideas | yes | shipped | — | not a shadow feature — keep |
| short-squeeze guard (cap→C) | scoring | LIVE production | filter | caps squeeze-risk to C | yes (prod, existing) | n/a | yes | shipped | — | not a shadow feature — keep |
| app keeper / scheduler health / live locks | operational tasks | LIVE | safety | persistence + locks | no | n/a | n/a | 2026-06-18 | low | keep |

**Count:** ~22 features. Already-active (paper/display/advisory/data): 8. Shadow/measuring: 6. Archive: 1. Dangerous/locked: 3 (+2 production filters that aren't shadow). New paper promotions this audit: cohort-guard warn + the unified registry/panel.

## Verdict
`SHADOW_FEATURE_INVENTORY_COMPLETE`
