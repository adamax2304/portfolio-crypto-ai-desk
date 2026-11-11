# Shadow Feature Archive Report (PART 7)

**Date:** 2026-06-24. No data deleted; historical reports kept.

## Archived
| feature | action | status | why |
|---|---|---|---|
| `shadow_exit_manager` variants A–I (BE/partial/trailing/reentry) | header marked **ARCHIVED — SUPERSEDED_BY_MODEL_F**; `config/paper_features.yaml` `state: archived` | kept for research/replay only (used by `shadow_exit_ledger_update.py`, `tp_stop_replay.py`); NOT wired to tracker/scheduler | Variants arm protection at/after TP1 (~1R), inferior: actionable book −96..−137R. Model F arms at +0.6R favorable → +74.1R. |

## Left OFF / locked (not enabled — confirmed)
- crypto scalp actionable, stocks C-tier actionable, stocks swing/invest actionable → remain LOCKED-POLICY shadow (dangerous). Registry status unchanged.
- old touch-based TP-policy metrics → kept as research (touch R relabelled optimistic; not a headline).
- circuit-breaker block / sector-cap block → remain shadow (alert-only warnings stay).

## What was NOT done (deliberately)
- No scheduler step disabled (none of the archived features had a scheduler step; the research scripts remain runnable on demand).
- No dashboard headline removed — touch R already demoted to a labelled secondary; nothing misleading remains in the headline.
- No data/reports deleted.

## Registry update
`docs/SHADOW_MODE_REGISTRY.md`: shadow exits row annotated `ARCHIVED_SUPERSEDED_BY_MODEL_F`.

## Verdict
`BAD_SHADOW_FEATURES_ARCHIVED_OR_LEFT_OFF`
