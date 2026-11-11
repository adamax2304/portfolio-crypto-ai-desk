# Score Breakdown

How to read a `ScoreBreakdown` object surfaced in the report or stored in SQLite.

## Fields

```json
{
  "final_score": 71.4,
  "confidence": "medium",
  "data_quality": "good",
  "tier": "B",
  "components": {
    "market_regime": 11.7,
    "technical_setup": 14.4,
    "momentum": 9.3,
    "derivatives": 8.0,
    "catalyst_news": 6.0,
    "narrative": 4.5,
    "execution_quality": 6.5
  },
  "risk_penalty": 5.0,
  "score_cap": 70.0,
  "cap_reasons": ["MEXC-only listing (exchange confirmation missing)"],
  "reasons": [
    "Score capped at 70 (MEXC-only listing (exchange confirmation missing)).",
    "Technical setup is doing real work in the score.",
    "Some evidence streams are missing or weak; confidence is reduced."
  ],
  "warnings": [
    "Derivatives data unavailable for this symbol."
  ]
}
```

## How to read each field

- **final_score** — the number after weights + multipliers + penalties + caps + clamp. Compare to thresholds (80/65/50).
- **confidence** — derived from score (≥85 high, ≥75 medium-high, ≥60 medium, else low).
- **data_quality** — `strong` (0 missing) / `good` (1 missing) / `acceptable` (≥2 missing).
- **tier** — A/B/C/rejected. A requires score ≥ 80 AND no caps.
- **components** — see [[Scoring_Overview]] for what each weight × quality means.
- **risk_penalty** — sum of all risk penalties.
- **score_cap** — the minimum active cap value (lowest wins). `null` if none.
- **cap_reasons** — labels for caps that hit the score_cap value.
- **reasons** — narrative explanations from the agent (good for showing the user).
- **warnings** — surfaced concerns (often duplicated from setup warnings).

## What an LLM should do with this

- If `tier = rejected` and `score_cap < 80`, that's the reason. State the cap.
- If `cap_reasons` includes "no clean invalidation" or "stale data" — the idea is structurally invalid, not just low-scoring.
- If `components.derivatives` is at baseline (~9 = 0.6 × 15), derivatives data was missing.
- If `risk_penalty` exceeds 15, multiple risks compounded.

## Common patterns

| Pattern | Likely interpretation |
|---|---|
| score ~70, cap 70, cap_reasons MEXC-only | Otherwise A-tier idea pinned by venue risk |
| score 55, cap 55, cap_reasons rumor | Unverified catalyst — wait for primary source |
| score 50, cap 50, cap_reasons stale | Run `update-data` and retry |
| score 50, cap 50, cap_reasons no invalidation | Setup wasn't structural enough |
| score 78, cap 78, cap_reasons extreme funding | Crowded direction — skip |

## Related

- [[Scoring_Overview]]
- [[Score_Caps]]
- [[Data_Confidence]]

## Implemented status

- **Implemented**.
