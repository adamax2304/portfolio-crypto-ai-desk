# Airdrops

## Status

`CatalystAgent` recognizes `type: airdrop` as a regular catalyst. No special handling.

## Why airdrops matter for trading (not for farming)

- Airdrop announcements pre-event can run the underlying token (if eligibility is tied to holding).
- Airdrop **claim/distribution day** often produces a dump as recipients sell.
- Cross-asset airdrop sentiment can spill into related sectors (e.g. SOL airdrops lift SOL ecosystem).

## How to evaluate

1. **Eligibility window** — has it closed? If yes, the speculation is over.
2. **Distribution date** — within 24h? Expect distribution-day selling.
3. **Airdrop size relative to FDV** — large drops vs FDV create heavy selling pressure.
4. **Recipient profile** — DeFi farmers (sell fast) vs long-term holders (slower sells).

## Trade patterns

- **Pre-snapshot run-up** on holder requirement — can be tradable long if structure agrees.
- **Distribution dump** — possible short setup if the token is liquid and structure aligns.
- **Post-dump recovery** — sometimes a clean bounce setup 24–48h after distribution.

## Operator rules

- The desk does not auto-flag airdrop distribution dates. Add them as manual events.
- Treat airdrop-claim day on small caps as a `high-volatility danger` window for that symbol.

## Logging

Treat like a catalyst event. Log Telegram-driven airdrop messages in [[Telegram_News/README|Telegram_News]]. After the event, classify as useful / useless.

## Related

- [[Catalyst_Agent]]
- [[Token_Unlocks]] — distribution shares mechanics
- [[News_Verification]]

## Implemented status

- **Implemented** via manual event type.
