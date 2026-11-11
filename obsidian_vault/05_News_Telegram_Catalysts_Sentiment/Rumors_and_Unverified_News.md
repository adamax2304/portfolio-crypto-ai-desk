# Rumors and Unverified News

## How the desk identifies a rumor

- A manual social note with `verification: rumor` in `data/manual/social_notes.yaml`.
- A catalyst string containing the word "rumor" in `CatalystAgent.catalysts`.
- A bridge signal that did not reach `tier=strong` and no corroborating manual event.

## What the desk does with it

1. **`CrowdAttentionAgent`** flags `stage = "rumor_driven"` when `attention ≥ 15` and any manual note has `verification == "rumor"` or `sentiment == "rumor"`. Adds a warning "Rumor-driven attention; do not size up without verified catalyst."
2. **`ScoringAgent`** caps the final score at **55** if:
   - At least one catalyst string contains "rumor" (lowercased).
   - `verification_status ∈ {none, rumor, single_source}`.
   - No `risk_events` present (because if there's a risk event, the cap order shifts).
3. **`TradeIdeaAgent`** propagates `cap_reasons` so the report shows "unverified rumor-only catalyst" as the cap reason.

## Operator rules

- **Never size up on a rumor.** Rumors raise watchlist priority, not capital allocation.
- **Wait for a primary source.** If you cannot find one within a reasonable window (15–30 min for fast moves), assume false.
- **Time-decay rumors.** A rumor that hasn't been confirmed in 2 hours is almost certainly false or already priced in.
- **Triangulate.** A rumor across 3+ unrelated sources is closer to truth — but still not primary. Apply caution.

## Famous patterns to recognize

- **"Binance listing leak"** — frequent in Telegram; sometimes true. Wait for the official announcement.
- **"Whale wallet activity"** (lookonchain-style) — useful intelligence but does not predict direction reliably.
- **"Partnership soon"** — usually overhyped; the partnership often doesn't move price even when real.
- **"Mainnet imminent"** — buy the rumor, sell the news. Often a sell-the-news flush even on confirmed mainnets.

## What to write in the journal

For every rumor you track, drop a note into [[Fake_or_Unverified_News]] using [[News_Item_Template]] with:

- `Verification status: Rumor`.
- `Did the market care?` — answered later.
- `Final classification: useful / useless / fake-unverified / late-priced-in / watch-only`.

This builds the dataset that lets you (and the LLM) learn which channels and which rumor archetypes have predictive value.

## Related

- [[News_Verification]]
- [[Telegram_Rumor_Risk]]
- [[Crowd_Attention]]
- [[Useless_News]]
- [[Fake_or_Unverified_News]]

## Implemented status

- **Implemented** (cap + stage). Rumor-decay rule is operator discipline.
