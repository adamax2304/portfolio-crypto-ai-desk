# Candidate Debug Guide

How to diagnose why a specific symbol passed / failed / capped.

## The command

```
python -m src.cli candidate-debug --symbol SOL/USDT --mode intraday
```

Modes: `scalp`, `intraday`, `swing`.

## What it prints

1. **Symbol header** — `SOL/USDT (mode=intraday)`.
2. **ranked_match** — Stage 2 fused candidate row if present:
   - Rank, opportunity_score, exchanges, best_exchange.
   - Per-exchange row: opportunity_score, change_24h%, atr%, vol_anomaly, risk_flags.
3. **per_exchange_universe** — Stage 1 membership per venue:
   - For each enabled exchange: accepted? quote_volume? spread%? exclude_reason.
4. **momentum_candidate** — if present in `latest_candidates.json`:
   - direction_bias, score, return_24h, RS/BTC, volume_ratio, reason_tags.

## How to read the output

- **"not in the latest ranked candidate file"** — re-run `python -m src.cli scan-universe --mode intraday`.
- **`accepted = False` on every venue** — symbol failed Stage 1 (volume / spread / keywords). Check `exclude_reason`.
- **Stage 1 OK, Stage 2 empty** — passed Stage 1 but failed liquidity / ATR / spread filter at Stage 2.
- **`risk_flags` contains `mexc_only`** — even if ranked, the score is capped at 70 (65 if structure weak).
- **`risk_flags` contains `not_on_anchor`** — capped at 75.
- **`vol_anomaly < 1.0`** — volume is below average; setup will be weak.
- **`atr_percent` < mode floor** — filter rejected this on Stage 2.

## What is NOT here

- The full ScoreBreakdown — that's in `data/processed/agent_outputs/<latest>_scoring_agent.json` for the symbol.
- The setup details (entry / invalidation / TPs) — `<latest>_technical_setup_agent.json`.
- The trade idea text — `<latest>_trade_idea_agent.json`.

To inspect those, open the JSON files directly. Tip: `grep "SOL/USDT" data/processed/agent_outputs/*.json`.

## Common scenarios

| Output | Likely cause |
|---|---|
| Not in any ranked file | Stage 1 failed; check volume / spread / keywords. |
| In universe, not in candidates | Stage 2 filter failed (ATR % or quote volume). |
| In candidates, score low | Setup quality low or RS/volume weak. |
| In candidates, score high, tier C | Cap active or warnings ≥ 3 or risk_penalty high. |
| Per-exchange divergence | Likely `price_divergence_across_exchanges` flag. |

## Related

- [[Momentum_Scanner_Agent]]
- [[Exchange_Fusion_Agent]]
- [[Score_Breakdown]]
- [[Score_Caps]]

## Implemented status

- **Implemented** — CLI exists.
