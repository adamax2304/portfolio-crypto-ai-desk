# News That Was Noise

## Definition

Any news item that did **not** measurably move price within a reasonable window.

A working threshold:

- < 1% move in 60 minutes on the named symbol.
- No volume_ratio spike (≥ 1.5) on the corresponding bars.
- No OI / funding shift.
- Nothing in the corresponding crowd-attention stage moved.

## Why track these too

If you only log winners, you cannot tell which sources are reliable. You need the noise dataset to compute hit rate.

## Common noise archetypes

- **"Big news coming soon"** — no specifics. Almost always noise.
- **Generic partnership headlines** — see [[Partnerships]].
- **Re-posts of older news** — bridge dedups same-window, but cross-channel re-posts slip through.
- **"Insider says X"** — rumor, single source, no follow-up.
- **Old tokenomics summaries** — informational, not catalytic.
- **Project tweets praising themselves** — marketing noise.

## How to log

Use [[News_Item_Template]] with classification `Useless` and file into [[Useless_News]]. Keep the entry short — don't waste time on noise documentation.

## Source hygiene

When a source / channel repeatedly shows up in `Useless_News`, deprioritize it mentally. Recommended improvement: a per-source reliability score in the bridge.

## Related

- [[Useful_vs_Useless_News]]
- [[News_That_Moved_Market]]
- [[Telegram_Rumor_Risk]]

## Implemented status

- **Operator framework**, supported by `12_News_Intelligence_Journal/Useless_News/`.
