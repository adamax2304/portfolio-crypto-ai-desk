# Adaptive TP Policy — Implementation Proposal (PART 9)

**Date:** 2026-06-23. **Status: NO production/paper change recommended now.** The replay does **not** support changing the TP count (removing TP3 is net-negative). What *is* worth doing is a **shadow-only measurement layer** + **display annotation**, both default-off, so the adaptive-TP3 / partial idea can be evaluated on forward data before any rule change.

## A. What is NOT proposed (replay does not support it)
- ❌ Do NOT switch production/paper to "2 TP default." It clips realized winners (−45R actionable) and saves no losers.
- ❌ Do NOT enable BE/partial/trailing in production (already shadow-disabled; evidence relative-only).

## B. Proposed SHADOW-ONLY measurement (default OFF, no trade impact)
Goal: collect honest forward evidence for the adaptive-TP3 + partial ideas without touching any real exit.

1. **Extend the existing shadow exit ledger** (`src/exits/shadow_exit_manager.py`, already shadow) to also record, per entered actionable trade: `cap_tp2_r`, `hold_tp1_r`, `partial_tp1_be_r`, alongside the current best-TP `final_r`. Pure measurement; writes to a research table/CSV, never to `signal_outcomes.final_r`.
2. **Per-playbook TP3 map (data-only, advisory):** a config draft, default-off:
```yaml
# config/tp_policy.yaml  (DRAFT — paper_only, default OFF, not loaded by tracker)
tp_policy:
  mode: shadow            # shadow | off | paper  (only 'shadow' allowed without sign-off)
  paper_only: true
  feature_flag: paper_tp_policy.adaptive_max_tp   # default false
  default_max_tps: 3      # UNCHANGED in production
  allow_tp3_when: [trend_runner, catalyst_confirmed, playbook_tp3_positive]
  disable_tp3_when: [chop, mixed, counter_regime, late_entry, no_chase, squeeze_against]
  per_playbook_overrides:
    crypto_swing_narrative_rs: keep_tp3        # earns +16R
    crypto_failed_bounce_short: keep_tp3       # earns +9R
    crypto_intraday_catalyst: keep_tp3_if_catalyst
    stocks_intraday_rth_momentum: max_tp2      # TP3 ~never reached
    stocks_swing_watchlist_rs: max_tp2
    stocks_invest_watchlist_30d: max_tp2
```
3. **Display annotation (read-model/UI only — allowed):** in Telegram alert + Control Plane trade detail, show an advisory line computed from the map, e.g. `TP policy (shadow): TP3 kept — trend-runner` or `TP3 advisory-capped — chop/counter-regime`. **Does not change levels or exits** — pure annotation. This is the only change that could ship now (display-only), and even that is optional.

## C. If/when it graduates (NOT now — requires sign-off)
- Files to touch later: `src/signals/tracker.py` (consume `tp_policy` only behind the flag), `src/notifiers/paper_entry.py`/`close_alert.py` (annotation), `config/tp_policy.yaml`.
- Tests needed: policy-map correctness; flag default-off no-op; shadow ledger never mutates `signal_outcomes`; per-playbook map matches the classification report.
- Rollback: delete `config/tp_policy.yaml` / set `mode: off`; flag default false → instant revert.
- Monitoring metrics: per-cohort TP3 reach-rate, TP3 add-R, give-back count, shadow cap-TP2 vs best-TP delta — weekly.

## Gates to graduate from shadow → paper-flag
n ≥ 30 closed actionable per affected playbook **AND** shadow cap/partial shows ≥ +2R improvement on forward data **AND** stable across ≥2 regimes. Currently unmet (TP3 reached only 45× across all actionable; per-playbook forward n small).

## Verdict
`NO_TP_POLICY_CHANGE_RECOMMENDED` (no production/paper change). Optional shadow-measurement + display-annotation proposal is ready (`ADAPTIVE_TP_PROPOSAL_READY` as a *shadow-only* artifact) — **implement only on explicit approval.**
