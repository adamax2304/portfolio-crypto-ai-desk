# Catalyst Quality Labels — Dashboard & Journal (PART 3)

**Date:** 2026-06-15 · Display-only. No scoring/tier/filter change.

## What was added

**`src/signals/catalyst_labels.py`** — shared pure helper:
- `compute_labels(signal)` → `CatalystLabels(catalyst_freshness, catalyst_strength, source_quality, symbol_mapping, derivatives_label, headline_short)`.
- `telegram_block(signal)` → 3-line plain-text block.
- `move_type(signal)` → catalyst-backed / technical momentum / chase risk.

### Label dimensions (all computed from existing data)
| Dimension | Levels |
|---|---|
| Catalyst | fresh(≤1h) / recent(≤6h) / old(>6h) / none |
| Strength | strong (imp≥7) / medium (4-7) / weak (<4) / none |
| Source | official / reputable / social / unknown / none |
| Mapping | exact / inferred / ambiguous / missing |
| Derivatives | OI-up / funding-supportive / no-squeeze / squeeze-risk / missing / not-available (stocks) |

Example one-liner:
`catalyst: recent(2.5h) · strength: medium · source: reputable · map: exact · deriv: OI-up`

## Where it shows

- **Obsidian dashboard §14** — catalyst-backed vs technical split, archive status, label distribution.
- **Derived table `signal_catalyst_labels`** — per-signal labels (1,016 backfilled).
- **Telegram** — 3-line block in setup + paper-entry (PART 4).
- **Opus packet** — per-catalyst age tags (PART 6).

## Safety

`test_14` confirms `compute_labels` does not mutate the signal and returns no score/tier fields. Pure display.
