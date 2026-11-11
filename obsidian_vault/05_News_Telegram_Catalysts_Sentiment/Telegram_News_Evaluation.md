# Telegram News Evaluation

How to read a Telegram-derived signal and decide what to do with it.

## Step 1 — Classify the signal

| Trait | Source field | Decision rule |
|---|---|---|
| Tier strong | `signal.tier == "strong"` | Treat as `confirmed` for verification |
| Tier missing / medium | `signal.tier != "strong"` | Treat as `single_source` |
| Re-post of same headline | dedup key matches | Ignore (bridge auto-dedups within window) |
| Source `t.me/...` and source_name matches a fraud-monitor channel | `source_name` | High weight for bearish signals (e.g. zachxbt) |
| Macro keyword present | headline match | Increment `riskoff_count` / `riskon_count` |

## Step 2 — Confirm price / volume

A Telegram signal alone does not make a trade. Confirm against:

- **Price**: did the symbol move in the headline's direction within 15–30 minutes? If yes → confirmation. If no → noise.
- **Volume**: volume_ratio ≥ 1.5 after the signal? Yes → confirmation. No → noise.
- **OI / funding**: do they move with the price? Yes → fresh positioning. No → likely fake / late.

## Step 3 — Map to action

| Confirmation level | Action |
|---|---|
| Verified (`tier=strong` + price/volume confirms within 30 min) | Treat as a real catalyst; update CrowdAttention to `growing_hype`; the system may flip a C → B via attention; LLM can recommend an active idea |
| Single-source + price confirms | Use as attention input only; do not raise score |
| Single-source + no price confirmation | Noise; do not act; log in [[Useless_News]] if revisited |
| `tier=strong` but price does the opposite | Late / contra signal; check if news was already priced in |
| Headline contains rumor language ("might", "could", "rumour", "according to insider") | Cap at 55 via rumor cap |

## Step 4 — Sentiment direction

- Bullish keyword + bullish price action = aligned; raises attention.
- Bullish keyword + bearish price action = potential sell-the-news; flag.
- Bearish keyword + bearish price action = aligned shorts; treat as confirmation.
- Bearish keyword + bullish price action = squeeze / bear trap; watch carefully.

## Step 5 — Time horizon match

- Most Telegram signals matter for **scalp** and **intraday**.
- For **swing**, only confirmed catalysts (listings, mainnet, partnerships, unlocks) have multi-day impact.
- For "long-term" (not a real mode here), narrative-level repeated mentions over days/weeks matter, not single headlines.

## Step 6 — Log into the journal

Use [[Templates/Telegram_News_Template|Telegram_News_Template]] (in `12_News_Intelligence_Journal/Templates/`). File into:

- `12_News_Intelligence_Journal/Useful_News/` — if it created or confirmed a trade.
- `12_News_Intelligence_Journal/Useless_News/` — if it produced no measurable price reaction.
- `12_News_Intelligence_Journal/Fake_or_Unverified_News/` — if it later proved fake.
- `12_News_Intelligence_Journal/Market_Moving_News/` — if it produced a > 2% move within 1 hour.
- `12_News_Intelligence_Journal/Telegram_News/` — default landing folder.

## Hard rules

1. Telegram never produces an A-tier idea on its own.
2. A "fresh" Telegram message > 60 minutes old without price reaction is noise.
3. Repeated reposting of the same headline is not new information.
4. Source channel reputation matters more than message content; the desk does not weight this yet — judge manually.

## Related

- [[Telegram_Integration]]
- [[News_Verification]]
- [[Rumors_and_Unverified_News]]
- [[Crowd_Attention]]
- [[News_Evaluation_Checklist_For_LLM]]
- [[Useful_vs_Useless_News]]

## Implemented status

- **Implemented** for the pipeline; **operator discipline** for the evaluation flow.
