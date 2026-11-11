# Useful vs Useless News

A working framework for the news intelligence journal.

## Categories

1. **Useful** — produced a tradable setup or confirmed an existing one.
2. **Useless** — did not move price; did not change attention meaningfully; consumed mental bandwidth.
3. **Market-moving** — produced a ≥ 2% move within 60 minutes; should be logged for pattern-finding even if you didn't trade it.
4. **Fake / unverified** — turned out false.
5. **Late / priced in** — verified but arrived after the move; useless in retrospect.
6. **Watch-only** — interesting but no immediate trade.

## Decision tree (apply after the fact)

```
Was the news verified?
  No → fake-or-unverified
  Yes → continue
Did price react within 60 min?
  No → useless (or late if reaction was earlier)
  Yes, ≥ 2% → market-moving
  Yes, < 2% → useful or watch-only depending on whether it confirmed a setup
Did the news create or confirm a trade you took?
  Yes → useful
  No → watch-only
```

## What "useful" learning looks like

Over weeks of logging, you should be able to answer:

- Which sources (channels / RSS feeds) actually produced useful news? Weight them higher.
- Which sources mostly produced useless or fake noise? Down-weight or ignore.
- Which categories (listings vs partnerships vs rumors) had the highest "useful" rate?
- Which time-of-day correlates with reliable news?

## Build the dataset

Every news item logged into `12_News_Intelligence_Journal/` with the matching template fills the dataset. Recommended cadence:

- Daily — file Telegram + RSS items as they arrive.
- Weekly — review classification (was it really useful? was the move sustained?).
- Monthly — re-rank sources / channels.

## Operator rule

- A source / channel that produced 3+ fake or unverified items in a month → mute it (mentally, since the desk doesn't yet weight by source).

## Related

- [[News_Item_Template]]
- [[News_That_Moved_Market]]
- [[News_That_Was_Noise]]
- [[News_Evaluation_Checklist_For_LLM]]
- [[Useful_News]]
- [[Useless_News]]
- [[Fake_or_Unverified_News]]

## Implemented status

- **Operator framework**, supported by the journal templates.
