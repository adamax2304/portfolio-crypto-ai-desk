# Token Unlocks

## Why this is a risk event, not a catalyst

`CatalystAgent` treats `type: unlock` as a **risk_event**, not a regular catalyst:

```python
if event_type in {"unlock", "delisting", "migration"}:
    summary.risk_events.append(text)
    summary.warnings.append(f"Event risk detected: {text}")
```

Effect:

- `catalyst_quality` drops by 0.25 in `ScoringAgent`.
- `RiskAgent` adds +15 risk_score and a "Catalyst risk event is near the trading window." line.
- `catalyst.warnings` are surfaced in `RiskAssessment` and the report.

## How unlocks are detected

Only via `data/raw/events/manual_events.yaml`. There is **no automated unlock calendar API**. This is a known recommended improvement (TokenUnlocks API key is reserved in `.env.example`).

## How to record an unlock

```yaml
- date: 2026-05-30
  ticker: APT
  event: "Linear unlock ~24M APT (~$120M @ current)"
  type: unlock
  source: "https://token.unlocks.app/.../apt"
  importance: 3
```

`CatalystAgent._parse_date` accepts ISO dates. Events within `today - 2 days` to `today + 7 days` are considered active.

## Operator rules

- **Never swing-long within 7 days of a known unlock** for that symbol.
- **Reduce intraday size** within 2 days of a known unlock.
- **Watch for late-cycle insider distribution** — unlock + abnormal Telegram positive sentiment = potential sell-the-news flush.
- **Unlocks are not automatic shorts** — many priced-in unlocks have no real price impact. Look at the unlock size relative to circulating supply and average daily volume.

## Common mistakes

- Trading a long into an unlock because "it'll bounce after the dip". The dip doesn't always come.
- Trusting a single Telegram unlock alert without confirming the date.
- Ignoring small cliff unlocks — they accumulate.

## Recommended improvements

- Pull TokenUnlocks API (or similar) automatically.
- Surface unlock proximity per candidate in the report header.
- Cap A-tier for any symbol with unlock within 5 days.

## Related

- [[News_Risk]]
- [[Catalyst_Agent]]
- [[Risk_Agent]]
- [[News_System_Overview]]

## Implemented status

- **Implemented** via manual events. **Recommended**: automated calendar.
