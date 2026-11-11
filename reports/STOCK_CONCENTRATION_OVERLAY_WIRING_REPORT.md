# Concentration Overlay — Wiring (PART 4)

**Date:** 2026-06-16

## Where it lives
`src/signals/portfolio_caps.py` — a **portfolio-aware overlay**, separate from scoring:
- `apply_stock_concentration_caps(signals, existing_positions, now)` — batch (Rule A+B),
  used by the counterfactual + any candidate-selection/reporting path.
- `concentration_for_live_signal(store, signal)` — per-signal live decision (queries open
  positions from the store), used at paper-entry time.

## Preserved fields (never modified)
`original_score`, `original_tier`, `original_playbook`, `original_raw_r` (when present),
entry/stop/TP, `created_at`. The overlay returns **copies**; inputs are not mutated
(`test_18_input_not_mutated`).

## Added fields
`risk_bucket`, `proxy_group`, `concentration_rank`, `concentration_base_weight`,
`concentration_effective_weight`, `concentration_status` ∈ {actionable, half_size,
shadow_proxy_duplicate, shadow_sector_cap, unknown_bucket_actionable, not_applicable},
`concentration_reason`.

## Live wiring (no schema migration)
Wired into `src/notifiers/paper_entry.py::send_paper_entry_alert` — for each stocks-intraday
A/B paper entry it calls `concentration_for_live_signal` and:
- writes all `concentration_*` fields into the **`signal_alerts.payload_json`** (derived
  storage — no `proposed_signals` schema change);
- routes `shadow_proxy_duplicate` / `shadow_sector_cap` → **not pushed** (`telegram_status
  = "shadow_sector_cap"`, channel `shadow_only_sector_cap`, `[SHADOW ONLY — SECTOR CAP]`);
- `half_size` → still pushed, with a `Correlation cap: … — 0.5x only` warning prefix.

Precedence in the alert router: scalp-shadow → sector-cap-shadow → late-entry-shadow →
half-size-warning → normal. Fails open (never blocks an alert on overlay error).

## Not yet wired (follow-up)
Batch use in the stocks report builder and the Obsidian "Stocks Concentration Guard"
dashboard section are **spec'd** (PART 5) and read the same `concentration_*` payload
fields; given the shadow-first verdict they are the remaining low-risk wiring step.

**PART 4 status: DONE (live paper-entry + payload); dashboard section spec'd.**
