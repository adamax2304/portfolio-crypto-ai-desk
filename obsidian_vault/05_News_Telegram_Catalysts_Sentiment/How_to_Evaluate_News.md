# How to Evaluate News (general)

A 5-question framework applicable to any news item — RSS, Telegram, manual.

## The 5 questions

1. **Is the source primary or secondary?**
   - Primary: official project blog, exchange announcement, regulator filing. Trust higher.
   - Secondary: news aggregator, Telegram repost. Trust lower.
2. **Is the event fresh?**
   - < 30 min old: likely tradable.
   - 30 min – 2 h: monitor for confirmation, do not chase.
   - > 2 h: probably priced in.
3. **Did price + volume confirm?**
   - Move in direction + volume_ratio ≥ 1.5 within the relevant window = confirmation.
   - Otherwise = noise or fake.
4. **Does it support or contradict the desk's setup?**
   - Supports + verified = increase confidence.
   - Contradicts + verified = exit / skip.
   - Contradicts + unverified = warning; size down.
5. **Is the catalyst the trade, or is the structure the trade?**
   - If you would not take the same setup without the headline, the catalyst is the trade — and that means you need stronger verification.
   - If the setup stood without the headline, the catalyst is bonus.

## Verification ladder

```
unverified rumor
  → unverified manual note
    → single-source RSS / Telegram
      → multiple sources (RSS + Telegram + manual)
        → primary source (exchange / project)
          → primary source + on-chain confirmation
            → confirmed and price-confirmed (best)
```

The desk caps idea score at 55 when verification ∈ {none, rumor, single_source} and a rumor flag is present. Each step up unlocks more headroom.

## Common evaluation mistakes

- Treating a Telegram channel as primary — it is at most secondary.
- Treating an exchange announcement as automatically bullish — sometimes the move was already done.
- Mistaking volume on news bar as confirmation — volume needs to persist 2+ bars.

## Where to write the analysis

Use [[News_Item_Template]] in `12_News_Intelligence_Journal/Templates/`. File into the matching folder per the classification.

## Related

- [[News_Verification]]
- [[Primary_vs_Secondary_Sources]]
- [[Rumors_and_Unverified_News]]
- [[Telegram_News_Evaluation]]
- [[News_Evaluation_Checklist_For_LLM]]

## Implemented status

- **Implemented** as operator framework; partial in code via verification ladder + caps.
