# Candidate Debug

```powershell
python -m src.cli candidate-debug --symbol SOL/USDT --mode intraday
python -m src.cli candidate-debug --symbol PEPE/USDT --mode scalp
python -m src.cli candidate-debug --symbol APT/USDT --mode swing
```

## Output sections

1. Symbol + mode header.
2. `ranked_match` — Stage 2 fused candidate row if present (rank, opportunity_score, exchanges, best_exchange, risk_flags, per-exchange rows).
3. `per_exchange_universe` — Stage 1 row per enabled exchange (accepted? quote_volume? spread%? exclude_reason).
4. `momentum_candidate` — `MomentumCandidate` row from `latest_candidates.json`.

## See full guide

[[Candidate_Debug_Guide]].

## Related

- [[Why_No_Trades]]
- [[Why_Too_Many_Watchlist]]
- [[Daily_Commands]]

## Implemented status

- **Implemented**.
