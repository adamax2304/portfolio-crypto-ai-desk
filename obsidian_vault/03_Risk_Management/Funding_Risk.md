# Funding Risk

## Source

Binance USD-M futures `premium_index.lastFundingRate` per symbol, fetched by `BinanceDerivativesCollector` and interpreted by `DerivativesAgent`.

## Thresholds used in code

| funding_rate | Label | DerivativesAgent action |
|---|---|---|
| `≥ +0.001` | "extreme long crowding" | warning + alignment −0.35 |
| `≥ +0.0005` | "elevated long crowding" | warning + alignment −0.15 |
| `≤ -0.0005` | "short squeeze potential" | warning + alignment +0.15 |
| else | "normal" | no warning |

`RiskAgent` adds +18 for `extreme`, +8 for `elevated`.

## Score caps

- Long + funding > +0.001 → cap 78.
- Short + funding < -0.001 → cap 78.

These are "adverse" crowding caps — they exist to prevent A-tier from chasing crowded longs into a flush.

## How to read it

- Funding represents perp positioning skew. Positive funding = longs paying shorts (longs crowded).
- A bull move with `funding > 0.0005` is **less safe to chase** than a bull move with funding near zero.
- A short setup with funding near zero is healthier than with funding very negative (squeeze risk).

## When funding is missing

- `data_available = False` → +6 risk penalty, warning "Derivatives data unavailable".
- The cap is not applied (you cannot punish what you don't see), but `derivatives` component drops to a baseline (default 0.6 × weight).

## Practical rules

| Setup | Healthy funding band | Avoid |
|---|---|---|
| Long (intraday) | -0.0003 to +0.0004 | `> +0.001` (cap), heavy positive |
| Short (intraday) | -0.0003 to +0.0004 | `< -0.001` (cap), heavy negative |
| Scalp | tighter — prefer near zero | extreme either side |
| Swing | accept slight positive on momentum names | extreme positive |

## Long/short ratio

`BinanceDerivativesCollector` also collects the global long/short ratio. `DerivativesAgent` warns on:

- `ls_ratio ≥ 2` — heavily long skew.
- `ls_ratio ≤ 0.5` — heavily short skew.

These are warnings, not caps. They feed `warnings[]` and the report.

## Common mistakes

- Treating "high positive funding" as bullish confirmation — it's the opposite.
- Ignoring negative funding when shorting — heavy negative = squeeze fuel.

## Related

- [[Derivatives_Agent]]
- [[Open_Interest]]
- [[Score_Caps]]
- [[Crowd_Attention]]

## Implemented status

- **Implemented**.
