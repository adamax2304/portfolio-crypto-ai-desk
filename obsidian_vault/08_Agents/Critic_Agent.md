# CriticAgent

## File

[src/agents/critic_agent.py](../../src/agents/critic_agent.py).

## Role

Argues against each setup. Produces a counter-thesis, contradictions list, weak-signal flag, late-or-crowded flag, and a verdict.

## Inputs

- `setups`, `candidates`, `regime`, `derivatives`, `catalysts`, `risks`.

## Outputs

`dict[symbol, Critique]`:

- `symbol`, `verdict` ∈ {accept, watch, reject}.
- `counter_thesis`, `contradictions[]`.
- `weak_signal_dependency`, `late_or_crowded`.

## How it argues

- Reads setup warnings, candidate.warnings, derivative crowding, catalyst risk events, regime mismatches.
- `weak_signal_dependency = True` when the setup depends on a single noisy signal (e.g. single Telegram note, single derivative gauge).
- `late_or_crowded = True` when extension > 2 ATR or funding extreme.

## Used by agents

- `ScoringAgent`:
  - If `verdict == "reject"` → +10 risk_penalty.
  - If `weak_signal_dependency` → +4.
  - If `late_or_crowded` → +5.
- `TradeIdeaAgent._build_counterarguments` puts the critique into the trade idea.

## Common mistakes

- Treating `verdict = watch` as a soft yes — it pushes the trade to watchlist, not active.
- Ignoring contradictions — they often predict the failure path.

## Future improvements

- Multi-step LLM-augmented critique (out of scope for the deterministic desk).
- Track which critic flags correlate with actual losses (after-the-fact analysis).

## Related

- [[Risk_Agent]]
- [[Scoring_Overview]]

## Implemented status

- **Implemented**.
