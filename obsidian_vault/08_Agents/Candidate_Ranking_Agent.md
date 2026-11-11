# Candidate Ranking Agent

## Status

**Not a dedicated agent** in `src/agents/`. The functionality is split:

- **Stage 1 (broad discovery)** — `MultiExchangeUniverseCollector.discover` (or single-exchange fallback `BinanceUniverseCollector.discover_broad_universe`).
- **Stage 2 (rank)** — `MultiExchangeUniverseCollector.rank_candidates(mode, refresh, discovery)` or `BinanceUniverseCollector.rank_candidates`.
- **Per-symbol momentum scoring** — `MomentumScannerAgent`.

## Output files

- `data/processed/symbol_universe.json` — Stage 1 fused symbol list.
- `data/processed/universe/<exchange>.json` — per-exchange Stage 1 details.
- `data/processed/exchange_symbol_map.json` — canonical symbol → list of venues.
- `data/processed/candidates/universe_ranked_candidates.json` — Stage 2 fused.
- `data/processed/candidates/universe_ranked_candidates_<mode>.json` — per-mode Stage 2.
- `data/processed/candidates/latest_candidates.json` — final `MomentumCandidate` list (after agent).

## Stage 2 ranking factors (per candidate)

- 1h / 4h / 24h change.
- ATR %.
- Recent quote volume.
- Volume anomaly.
- Relative strength vs BTC.
- Breakout / range expansion.
- Liquidity score.
- Opportunity score (composite).
- Risk flags.

## How to debug a single symbol

```
python -m src.cli candidate-debug --symbol SOL/USDT --mode intraday
```

This prints:

- Whether the symbol made the ranked list and at what score.
- Per-exchange membership (accepted? quote_volume? spread%? exclude_reason?).
- Per-exchange opportunity score, change_24h, atr%, volume_anomaly, risk flags.
- `MomentumScannerAgent` candidate row if present.

## Related

- [[Momentum_Scanner_Agent]]
- [[Candidate_Debug_Guide]]
- [[Exchange_Overview]]

## Implemented status

- **Implemented** (split across collectors and momentum scanner).
