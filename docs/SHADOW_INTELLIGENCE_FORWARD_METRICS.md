# Shadow Intelligence — Forward Metrics

Weekly tracking of the shadow intelligence layer vs actual outcomes. Observation-only;
nothing here influences trades. Populate alongside `WEEKLY_FORWARD_METRICS.md`.

| Metric | Week of ____ | Week of ____ |
|---|---|---|
| signals analyzed | | |
| squeeze_phase coverage % | | |
| derivatives confidence coverage % | | |
| timeline confidence coverage % | | |
| thesis coverage % | | |
| onchain coverage % (0 until config) | | |
| no_chase_warning precision | | |
| phase_3 winners / losers | | |
| funding_turning_down winners / losers | | |
| thesis invalidation accuracy | | |
| potential R saved (hypothetical) | | |
| potential winners missed (hypothetical) | | |
| recommendation per field | | |

## How to populate
- `python -m scripts.intelligence_update` → caches + `reports/INTELLIGENCE_LAYER_HEALTH.md`
- Join `signal_alerts.payload_json` (intelligence_* / squeeze_* / thesis_* fields) with `signal_outcomes.final_r`.
- Use `reports/SHADOW_INTELLIGENCE_FORWARD_COMPARISON_TEMPLATE.md` for the full Friday write-up.

> Promotion gate: a field may be proposed for **soft warning / review-only** only after it shows forward predictive value across up+down regimes — and only with operator approval. Default = keep_shadow.
