# News Verification

## Verification fields in code

- `CatalystSummary.verification_status` — set by `CatalystAgent`. Possible values:
  - `none` — no catalyst found.
  - `news_mention` — RSS news mention only.
  - `manual_event` — manual event from `manual_events.yaml` (highest in this enum).
- `manual_social_notes[*].verification` — from `data/manual/social_notes.yaml` or from `news_trader_bridge.to_manual_social_notes`. Possible values:
  - `confirmed` — bridge cluster had a `tier=strong` signal.
  - `single_source` — bridge cluster did not.
  - `rumor` — manual note tag.
- The combination of catalyst verification + manual social note `rumor` flag drives the **rumor cap (55)** in `ScoringAgent`.

## Score cap interaction

```
if catalyst has any catalyst string containing "rumor"
   and verification_status in {none, rumor, single_source}
   and no risk_events:
       cap = 55  ("unverified rumor-only catalyst")
```

## Verification ladder in practice

| Source | Default verification |
|---|---|
| RSS Binance Announcements (primary_source: true) | best — typically `news_mention` upgraded by operator to `confirmed` |
| Other RSS | `news_mention` |
| Manual event (`manual_events.yaml`) | `manual_event` |
| Manual social note tagged `verification: confirmed` | `confirmed` |
| news_trader bridge with `tier=strong` | `confirmed` |
| news_trader bridge without strong tier | `single_source` |
| Manual rumor note | `rumor` (triggers cap) |

## Hard rules

- Never promote an idea past the rumor cap because a chart looks good.
- An LLM evaluating an idea must read `cap_reasons` and surface the rumor cap if present.
- A "confirmed" tag should be reserved for primary sources, not for "I trust this Telegram channel".

## Manual upgrade flow

If you confirm a Telegram headline via a primary source (e.g. official exchange page), you can:

1. Add a line to `data/raw/events/manual_events.yaml`:
   ```yaml
   - date: 2026-MM-DD
     ticker: SYMBOL
     event: "<short event>"
     type: listing       # or unlock / partnership / etc
     source: "<URL>"
     importance: 3
   ```
2. Re-run `update-data` to load it into SQLite events.
3. The next report will see `verification_status = "manual_event"` for that symbol.

## What this **doesn't** do

- It does not change the historical timeline of the trade idea. If a trade was opened before the manual event was added, the original score still reflects what the desk saw at the time.
- It does not weight sources differently — that's a recommended improvement.

## Related

- [[News_System_Overview]]
- [[Score_Caps]]
- [[Catalyst_Agent]]
- [[Primary_vs_Secondary_Sources]]
- [[Rumors_and_Unverified_News]]

## Implemented status

- **Implemented** as described.
