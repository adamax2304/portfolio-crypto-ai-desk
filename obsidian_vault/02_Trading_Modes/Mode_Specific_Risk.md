# Mode-Specific Risk

Risk parameters that should change per mode. Some are wired, some are not.

## Wired in code

- **Universe filters**: liquidity floor and ATR floor scale up from scalp → intraday → swing. See `config/universe.yaml`.
- **Max final trade ideas**: 3 / 4 / 3 — small enough that risk concentrates on quality.
- **Setup quality math**: `setup_quality = candidate.score * 0.45 + trend_bonus + rr_bonus`; lower-quality candidates are pruned before risk gate.
- **`RiskAgent` regime overlays** apply equally across modes (see [[Risk_Agent]]).

## Not wired (manual judgment required)

- **Position sizing** — the desk does not size positions. You must size manually.
- **Per-mode stop multiplier** — all modes default to 1.2 ATR stops; scalpers may need tighter (0.8 ATR), swing traders may need wider (1.5–1.8 ATR).
- **Holding-time risk** — overnight risk on a swing is real (gap, weekend, exchange downtime); the desk does not penalize swing for this.

## Practical multipliers (recommendation, not enforced)

Use these as mental ratios on top of what the desk produces:

| Mode | Suggested position size | Suggested stop multiplier | Time-stop |
|---|---|---|---|
| scalp | 1.0× base | 0.8–1.0 ATR | exit if no progress in 30m |
| intraday | 1.0× base | 1.0–1.2 ATR | exit if no progress in 4–6h |
| swing | 0.6× base | 1.2–1.8 ATR | re-evaluate at every 4h close |

`base` is your unit risk per trade (e.g. 0.5–1% of account). The desk has no opinion on `base`.

## Critical no-go conditions (per mode)

- **Scalp** — do not scalp in `high-volatility danger`. Whipsaws kill scalpers.
- **Intraday** — do not enter when `freshness > 3h` (the cap forces rejected).
- **Swing** — do not swing within 2 days of a confirmed token unlock; `CatalystAgent` flags it as `risk_events`.

## Related

- [[Risk_Management_Overview]]
- [[Risk_Agent]]
- [[Stop_Loss_Logic]]
- [[Funding_Risk]]
- [[Token_Unlocks]]

## Implemented status

- **Partially implemented** — filters and risk overlays exist; sizing and time-stops are manual.
