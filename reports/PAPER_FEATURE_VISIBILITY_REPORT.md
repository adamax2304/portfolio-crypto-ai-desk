# Paper Feature Visibility (PART 8)

**Date:** 2026-06-24. App + Telegram surfacing of active paper features.

## Control Plane app
- **New "Paper Features" panel** (dashboard) — from `GET /api/paper-features`:
  - counts badges: active / shadow / archived / locked;
  - **active features** list: label · mode (cohort) · evidence · decision_date;
  - footer: dangerous/locked list ("do NOT enable"), `Live LOCKED · auto-live LOCKED`, and the safety note.
- **Per-trade feature effects** (closed-trade row + detail) — `paper_exec_flags`/`paper_feature_tags`:
  - `Model F protected` (BE armed / lock +0.5R), `giveback→protected`, **`weak cohort`** badge (cohort warn), highest-TP, original-stop-avoided.
  - Closed-detail already shows the old-vs-new Model F explanation + protection timeline (from the prior upgrade).
- **Inactive/dangerous shown separately** — shadow/measuring + archived + dangerous_locked buckets are returned and the locked list is rendered explicitly so nothing looks "available".
- **Why active** — each feature carries `evidence` (n / effect) + `decision_date`.
- Frontend `npm run build` (tsc + vite) passes clean.

## Telegram
- **Paper close alerts** already include the active feature effect per trade: `Paper exec R (Model F)`, `BE @ +0.6R` / `lock +0.5R @ +1R`, `Closed at protected stop`, and the touch-vs-paper line (from the paper-risk upgrade). The weak-cohort label is visible in the app per-trade view.
- **Daily/paper-monitor summary** surfaces Paper Execution R + protected/BE-scratch counts via the same `books.get_dashboard_summary` block; the authoritative active-feature list lives in the app panel (single source) rather than duplicated into every alert to avoid noise.

## Honest scope note
Per-trade Model F effects + the app feature panel are the primary visibility surface. A dedicated "active feature list" line inside the daily Telegram digest was intentionally not added to avoid alert bloat — the app panel is the canonical, always-current view (refetched on poll).

## Verdict
`PAPER_FEATURES_VISIBLE_IN_APP_AND_TELEGRAM`
