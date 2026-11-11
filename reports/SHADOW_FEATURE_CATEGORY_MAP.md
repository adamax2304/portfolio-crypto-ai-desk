# Shadow Feature Category Map (PART 2)

**Date:** 2026-06-24.

## A. Risk / exit / protection
- **Model F / early MFE protection / paper_execution_r** — ACTIVE paper accounting.
- BE / partial / trailing / profit protection (`shadow_exit_manager` A–I) — research, **superseded by Model F → archive**.
- TP policy / adaptive TP3 — research/advisory, keep measuring.
- short-squeeze guard — LIVE production scoring (cap→C). Not shadow.
- concentration / sector / correlation caps — shadow (alert-only as warnings).
- circuit breaker — alert-only (block kept shadow).

## B. Signal / playbook filters
- crypto scalp — LOCKED-POLICY shadow (dangerous).
- crypto_intraday_catalyst_or_momentum — weak cohort → **warn label (paper display)**.
- failed_bounce_short / swing_narrative_rs — actionable playbooks (production), the viability core. Not shadow.
- C-tier — LOCKED shadow_review_only (dangerous).
- stocks swing/invest — LOCKED paused (dangerous).
- no-chase / overextension / market-regime gates — LIVE production filters. Not shadow.

## C. Data / catalyst / intelligence
- catalyst label refresh + integrity monitoring — LIVE-ADVISORY (scheduler), keep active.
- news_supported / telegram_supported — LIVE-ADVISORY flags.
- funding/OI archive — LIVE data.
- market-regime labels — LIVE-ADVISORY (sparse ~30% coverage) — keep measuring (coverage TODO).
- intelligence layer (timeline / derivatives trajectory / squeeze phase) — SHADOW/NEED_MORE_DATA, keep measuring.
- risk-off label — LIVE-ADVISORY measurement.

## D. Reporting / app / Telegram
- realistic_r / paper_execution_r display — ACTIVE.
- touch_r relabel (optimistic) — ACTIVE.
- status clarity / lifecycle labels — LIVE-DISPLAY.
- close-alert clarity + Model F line — LIVE-DISPLAY.
- catalyst context lines — LIVE-ADVISORY.
- **Paper Features panel + per-trade feature tags (NEW)** — ACTIVE display.

## E. Safety / operational
- circuit breaker / daily-loss guard (warnings) — alert-only advisory.
- scheduler health / heartbeat / app keeper — LIVE operational.
- live / auto-live locks — LIVE-LOCKED (hard).
- stale/expired signal handling — LIVE-DISPLAY.

## Verdict
`SHADOW_FEATURES_CATEGORIZED`
