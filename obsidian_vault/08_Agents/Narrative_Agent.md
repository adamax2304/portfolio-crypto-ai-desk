# NarrativeAgent

## File

[src/agents/narrative_agent.py](../../src/agents/narrative_agent.py).

## Role

Per-narrative heatmap from candidates + news + catalysts.

## Inputs

- `candidates: list[MomentumCandidate]`.
- `news_output: dict` — from NewsAgent.
- `catalysts: dict[symbol, CatalystSummary]`.
- Config `watchlist.yaml.narratives` defines named narratives + symbols + keywords.

## Outputs

`dict[narrative_name, NarrativeSummary]`:

- `narrative`, `attention_score`, `momentum_score`, `volume_score`, `risk_score`, `heat_score`.
- `representative_symbols`, `status`, `evidence[]`, `warnings[]`.

## How it makes decisions

- Counts narrative-level + symbol-level news mentions per narrative.
- Sums catalyst importance across representative symbols.
- Averages candidate momentum score / volume score / per-candidate risk.
- Combines into heat_score and status (`hot / rising / crowded/watch carefully / quiet / mixed`).

## Used by agents

- `ScoringAgent._symbol_narrative_quality` reads the highest-heat narrative for the symbol → narrative component contribution.
- `TradeIdeaAgent._symbol_narrative` picks the best narrative for evidence rendering.
- Report builder renders the heatmap.

## Common mistakes

- Treating a `hot` narrative as a buy signal — it's a context input, not a trade trigger.
- Missing symbols in `watchlist.yaml.narratives` — they don't get narrative attribution.

## Future improvements

- Auto-decay narrative scores over time.
- Per-narrative cooldown to suppress late entries.
- More narratives configured by default (see [[Sector_Overview]]).

## Related

- [[Narrative_Heatmap]]
- [[Sector_Overview]]
- [[Scoring_Overview]]

## Implemented status

- **Implemented**.
