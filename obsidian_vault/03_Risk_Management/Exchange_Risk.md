# Exchange Risk

## Per-venue trust

From `config/exchanges.yaml`:

| Exchange | Role | Trust | High-risk |
|---|---|---|---|
| binance | anchor | 0.95 | no |
| bybit | derivatives | 0.85 | no |
| mexc | discovery | 0.50 | **yes** |

Trust is exposed to humans but does not directly multiply scores. The harder enforcement is:

- MEXC tagged as `high_risk_exchanges` in `universe.yaml`.
- MEXC-only listings cap at 70 in `ScoringAgent` (65 if structure is weak).
- Not-on-anchor caps at 75.

## Risks per venue

### Binance

- Geo-restrictions (US users, others).
- Occasional API outage / `429` rate limits.
- Withdrawal halts on small caps.

### Bybit

- Smaller spot books than Binance.
- Funding rate methodology subtly different from Binance — DerivativesAgent uses Binance funding for the cap threshold.

### MEXC

- Pump-prone listings.
- Books can thin out very quickly.
- Higher chance of single-venue manipulation (capped at B-tier for a reason).
- Withdrawal pauses on suspicious listings.

## Exchange failure handling

`Supervisor.update_data` runs collectors in sequence:

1. Binance — anchor; failures recorded in `summary.failed`.
2. Bybit — secondary; failures swallowed into `secondary_summaries[exchange].failed`.
3. MEXC — secondary; same.
4. Binance + Bybit + multi-exchange derivatives — failures into respective summaries.

If anchor (Binance) totally fails, the entire downstream pipeline degrades. `CoverageAuditAgent` will surface this in the report.

## What to do when an exchange is degraded

- `python -m src.cli exchange-status` — quick view of per-venue status, last update, failure counts.
- If anchor failed, run `update-data` again later; do not trust the report until anchor is fresh.
- If only Bybit / MEXC are down, the anchor report is still valid but derivatives confidence drops.

## Position risk during exchange events

- If you have a position on a venue and that venue's withdrawal / deposit pauses: do not size up; consider closing.
- If the anchor (Binance) goes into maintenance mid-trade, structure references freeze; the desk's report becomes stale.

## Related

- [[Exchange_Overview]]
- [[Binance_Role]] · [[Bybit_Role]] · [[MEXC_Role]]
- [[Exchange_Data_Confidence]]
- [[Exchange_Failure_Handling]]

## Implemented status

- **Implemented**.
