# Narrative Heatmap

## Where computed

`NarrativeAgent` (see [[Narrative_Agent]]) per configured narrative in `config/watchlist.yaml.narratives`. Currently configured: AI, RWA, L2, Memes, DePIN, Gaming.

## Inputs per narrative

- `representative_symbols` — candidates whose ticker matches the narrative's symbol list.
- News mentions: count of narrative-level news + count of symbol-level news.
- Catalyst importance sum across representative symbols.
- Average candidate momentum score.
- Average normalized volume ratio.
- Average per-candidate risk (extension, low volume, hot return).

## Output per narrative

- `attention_score` (0–100).
- `momentum_score`.
- `volume_score`.
- `risk_score`.
- `heat_score = attention*0.35 + momentum*0.35 + volume*0.15 - risk*0.15` clamped.
- `status` ∈ {hot, rising, crowded/watch carefully, quiet, mixed}.
- Evidence + warnings.

## Status rules

- `hot` — heat ≥ 70 and risk < 55.
- `rising` — heat ≥ 50.
- `crowded/watch carefully` — attention ≥ 60 and risk ≥ 55.
- `quiet` — heat ≤ 20.
- else → `mixed`.

## How it feeds scoring

`ScoringAgent._symbol_narrative_quality(symbol, narratives)`:

- Picks the highest-heat narrative the symbol belongs to.
- `quality = best.heat_score / 100`.
- If `best.risk_score ≥ 65`, subtract 0.2.
- Clamped 0.1–1.0.
- Used in the `narrative` component (weighted 10 base, 1.30× in swing).

## Reading the heatmap in the report

The report lists narratives ordered by heat_score, with attention / momentum / volume / risk side-by-side and representative leaders quoted.

## How to use it

- **Swing**: only trade swing in `hot` or `rising` narratives.
- **Intraday**: any narrative status is acceptable, but `crowded/watch carefully` should reduce size.
- **Scalp**: narrative is heavily muted (×0.75). Don't trade scalp based on narrative — use it as context.

## Common mistakes

- Chasing a `crowded/watch carefully` narrative because "all these names are pumping" — that is the warning.
- Skipping a `rising` narrative because it isn't `hot` yet — `rising` is often the best entry stage.
- Treating a narrative as static — heat scores shift bar-by-bar.

## Recommended improvements

- Auto-decay heat over time (current snapshot only).
- Per-narrative cooldown to suppress late swing entries after `hot` runs > 5 days.
- More narratives configured: Perp DEX, Bitcoin ecosystem, Exchange tokens, Stablecoin-related, Privacy.

## Related

- [[Narrative_Agent]]
- [[Sector_Overview]]
- [[Crowd_Attention]]
- [[Scoring_Overview]]

## Implemented status

- **Implemented**.
