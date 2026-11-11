# Shadow Promotion — Implementation Plan (PART 6)

**Date:** 2026-06-19.

## Classification of the PROMOTE_NOW set (all display/advisory)
Every feature that passes the gates this window is **display-only or advisory-only**, and **all are already implemented and LIVE** from prior sessions. So the "implementation" is *confirm + keep*, not new code:

| Feature | Type | Files | Config flag | Status |
|---|---|---|---|---|
| Status taxonomy / expired split | Display-only | `src/status/display_status.py` | — | LIVE |
| Close-alert lifecycle R | Display-only | `src/notifiers/close_alert.py` | — | LIVE (dedup-safe) |
| Paper-monitor Telegram Status | Display-only | `scripts/paper_monitor_status.py` + scheduler tail | `--cooldown-min 90` | LIVE (non-fatal) |
| Catalyst context / labels | Advisory-only | catalyst layer + notifiers | — | LIVE |
| Agent Council reason_codes + JSON | Advisory-only | scheduled SKILL + protocol §17 | — | LIVE |

**No new display/advisory work is required** — these were shipped in the status-clarity + Agent Council sessions.

## Trade-affecting candidates → NOT implemented now (proposal only)
Per the rules, any feature touching trade decision / routing / actionability needs a proof report first, then paper-only flag, then production only if gates pass. None passed (sample = 5). Proposals for when the window reaches ≥15–30 closed actionable decisions:

1. **Squeeze-phase / no-chase advisory gate (paper-only)** — when ≥30 closes, evaluate win-rate by `squeeze_phase` and `no_chase`; if net ≥ +2R counterfactual without killing winners, add a **default-off** config flag `paper_guards.squeeze_no_chase_review` that routes flagged setups to review-only (paper). Files: `config/signal_tracking.yaml` (flag), `paper_entry.py` (read flag, route to review). Rollback: flip flag off. Monitor: track flagged-vs-unflagged R weekly.
2. **Circuit-breaker as a paper pause** — needs actual `would_pause` fires (≈0 so far). When ≥10 fires observed, compare R saved vs missed; default-off flag only.
3. **Sector/concentration cap as a paper size-down** — needs binds to occur; default-off flag only.
4. **Profit-protection (BE/partial/trailing)** — remains shadow; requires a *forward* (not hindsight) net-positive result across ≥1 month and both regimes before any paper flag.

Each proposal: feature-flag default-off · reversible · paper-only first · tests added with the flag · explicit proof report required before enabling.

## Default values
All proposed flags default **off**. Nothing in this plan changes production trade math, scoring, TP/SL, entry, routing, or live.
