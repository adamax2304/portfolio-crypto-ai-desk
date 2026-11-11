# Update Universe

Refresh the multi-exchange symbol universe (Stage 1 + Stage 2 funnel).

## Commands

```powershell
# Stage 1 only: discover active USDT symbols across enabled exchanges
python -m src.cli update-universe

# Stage 1 + Stage 2 rank with a specific mode's filters
python -m src.cli scan-universe --mode intraday
python -m src.cli scan-universe --mode scalp
python -m src.cli scan-universe --mode swing

# Stage 2 only (reuse last Stage 1)
python -m src.cli rank-candidates --mode intraday
python -m src.cli rank-candidates --mode swing --refresh-universe
```

## Outputs

```
data/processed/symbol_universe.json
data/processed/universe/<exchange>.json
data/processed/exchange_symbol_map.json
data/processed/candidates/universe_ranked_candidates.json
data/processed/candidates/universe_ranked_candidates_<mode>.json
```

## When to run

- First run of the day before any report.
- After a major listing event (Binance / Coinbase) to pick up new symbols.
- When `python -m src.cli candidate-debug --symbol X` says the symbol is not in the universe.

## Discovery mode

```powershell
python -m src.cli intraday-report --auto-universe --discovery
```

`--discovery` flag activates `discovery_overrides` in `universe.yaml`: wider scan (250 symbols), lower volume floor (Binance 5M / Bybit 2M / MEXC 0.5M), larger deep-analysis bucket (50). Useful for catching small-cap rotations.

## Tuning

See [[How_to_Adjust_Filters]] for the knobs.

## Related

- [[Daily_Commands]]
- [[Candidate_Debug]]
- [[Exchange_Overview]]

## Implemented status

- **Implemented**.
