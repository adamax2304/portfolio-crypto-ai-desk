# Rejected Setups

## Definition

- `final_score < 50`, OR
- `cap_reasons` includes "no clean invalidation" (forced rejected), OR
- `cap_reasons` includes "stale data" (forced rejected).

The trade idea is created with `direction = "no trade"`, `status = "no_trade"`, and a parallel `RejectedIdea` is emitted with reasons.

## Why the desk surfaces rejected ideas

Rejected isn't silence. It's **informative silence**. Knowing *why* the desk doesn't want a setup is at least as useful as knowing why it does.

`RejectedIdea`:

- `symbol`, `tier`, `score`, `direction_bias`.
- `primary_reason` — top cap or warning.
- `reasons[]` — up to 6 supporting reasons.
- `exchanges[]` — which venues list it.
- `risk_flags[]` — fusion flags.

The report renders the rejected block under "Rejected ideas with reasons".

## Common rejection patterns

| Pattern | Likely root cause |
|---|---|
| `primary_reason = "no clean invalidation"` | Setup wasn't structural. ATR missing or extended setup. |
| `primary_reason = "stale data"` | Run `update-data`. |
| `primary_reason = "MEXC-only listing"` | The setup may still be valid on its venue, just capped. |
| `primary_reason = "unverified rumor-only catalyst"` | Wait for primary-source verification. |
| `primary_reason = "low liquidity"` | Thin book; skip or size tiny. |
| `primary_reason = "extreme positive funding against long crowding"` | Wait for funding to normalize. |
| `score below tier-C threshold` | No specific cap; the components were weak across the board. |

## LLM behavior

- An LLM evaluating a rejected idea should explain the `primary_reason` and `risk_flags`, not argue for the trade.
- If asked "should I trade X?" and X is rejected, the answer is **no**. State the reason.

## When a rejected becomes tradable

- Run a fresh report after a data refresh.
- The next `WatchlistMonitor` tick can flip a rejected → B/A if scoring improves enough.

## Related

- [[Scoring_Overview]]
- [[Score_Caps]]
- [[No_Trade_Conditions]]
- [[Why_No_Trades]]

## Implemented status

- **Implemented**.
