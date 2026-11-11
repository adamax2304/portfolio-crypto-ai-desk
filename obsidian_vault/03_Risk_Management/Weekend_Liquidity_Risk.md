# Weekend Liquidity Risk

Operator-facing risk page. Weekend Mode (see [[Weekend_Mode]]) is the automated response; this page covers the underlying market reality + manual rules.

---

## What changes on weekends

- **Lower aggregate volume** — institutional desks closed; retail and Asia-prop dominate.
- **Wider spreads** — fewer market makers quote on smaller pairs.
- **More wicks** — books are thinner, so a single market order moves price further.
- **Slower funding adjustments** — perp funding can stay extreme longer.
- **News risk lingers** — Friday-late news hasn't been digested by US institutions.
- **Higher dependency on Asia tape** — Asia hours dominate weekend price action.

## Why this matters for the desk

- ATR-based stops set on Friday afternoon may be too tight for Saturday wicks.
- Volume_ratio anomalies are noisier (a low absolute volume bar can spike to 3x ratio without meaningful flow).
- Cross-exchange divergence (`price_divergence_across_exchanges`) is more common.
- MEXC-only signals are especially fragile — single-venue thin books + weekend wicks = whipsaw.

## Hard rules (operator)

1. **Halve normal per-trade risk on weekends.** A weekend B-tier was often a Friday A-tier; treat it accordingly.
2. **No new entries during the first 2 hours of the Asian Saturday session** unless the setup is exceptional.
3. **Demand structural invalidation** — recent support/resistance ± 0.15 ATR, not just `close ± 1.2 ATR`.
4. **Avoid scalp during weekend off-hours** (Saturday US evening / Sunday Asia early).
5. **Skip MEXC-only setups** unless liquidity is exceptional. Weekend Mode caps weak MEXC-only at C, but you should usually skip even C-tier MEXC-only.
6. **No swing entries in the 24h before Monday open** — Monday gap risk is real.
7. **Re-evaluate at Sunday US evening** — that's when Monday positioning starts.

## Indicators that get noisier on weekends

- Volume_ratio — single-bar spikes are common; demand 2+ consecutive bars.
- ATR percentile — can drop sharply during dead hours then spike on a single wick.
- Funding rate — may diverge between Binance and Bybit more than usual.
- OI change — moves slower; the 24h window is less informative.

## Indicators that stay reliable

- 4h / 1d EMA structure (slow enough to not be wick-distorted).
- Multi-day relative strength.
- Narrative attention (news_trader bridge over a 240-min window).
- Macro pulse (CPI/FOMC are weekday-only anyway).

## When Weekend Mode caps a setup

If `cap_reasons` includes "weekend: weak signal capped at B-tier" or similar:

- The desk thought the setup was structurally B+, but weekend evidence quality wasn't strong enough.
- You may still trade it, but at the lower tier's sizing.
- Do not override the cap unless you have outside evidence the desk doesn't see.

## When Weekend Mode demotes a chasing entry

If `notes` includes "weekend: chasing entry — downgraded to C":

- The setup is extended > 2 ATR from EMA20.
- Original tier could have been B (or even A).
- The correct action is to **wait for a pullback** into the entry zone.

## Operator rules of thumb

| Trade type | Weekend treatment |
|---|---|
| Scalp on majors (BTC/ETH/SOL) | Half size; tight invalidation; ≤ 1h hold |
| Scalp on alts | Skip unless A-tier survived the overlay |
| Intraday long | Demand pullback acceptance; no chasing |
| Intraday short | Acceptable if regime confirms; respect wick tolerance |
| Swing long | Acceptable on majors with 4h/1d structure |
| Swing short | Acceptable on broken structures |
| Invest / long-term | Wait for Monday open for entries; weekend wicks don't change thesis |
| MEXC-only | Skip |

## Worst-case scenarios to plan around

1. **Saturday night Asia flash crash** — common on small caps; have stop respected.
2. **Sunday US open weak** — late entries into a soft tape get caught in Monday gaps.
3. **Weekend exchange outage** — withdrawals paused; mid-trade you may be stuck. Reduce per-venue exposure on weekends.
4. **Late-Friday news still digesting** — re-evaluate the news after the Asia open Sunday.

## Related

- [[Weekend_Mode]]
- [[Weekend_Mode_Checklist]]
- [[Funding_Risk]]
- [[Liquidity_Risk]]
- [[Spread_Risk]]
- [[Exchange_Risk]]
- [[No_Trade_Conditions]]

## Implemented status

- **Operator framework**. Automated portion lives in [[Weekend_Mode]].
