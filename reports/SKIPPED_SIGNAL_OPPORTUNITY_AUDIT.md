# Skipped / Near-Miss Opportunity Audit (PART 1)

**Date:** 2026-06-14 11:33 UTC
**Scope:** rejected_ideas (sampled 800/2833 last 14d) + C-tier (553 signals last 14d).
**Source-of-truth:** read-only join of `rejected_ideas`, `proposed_signals`, OHLCV candles.

## Headline

- Records analyzed: **1353**
- Skips that saved a likely loss (same symbol later A/B and lost): **219**
- Skips that missed a likely winner (same symbol later A/B+won OR price moved ≥ +1R proxy): **577**
- Net opportunity score: **+358** (positive = filter cost more than saved)

## Top skip reasons (last 14d)

| Reason | n |
|---|---:|
| Market regime is mixed; breakout failure risk is e | 347 |
| C-tier intraday | 344 |
| short squeeze risk → capped to C: thin_liquidity_s | 227 |
| Price is more than 2 ATR from EMA20; do not chase. | 162 |
| C-tier swing | 118 |
| C-tier invest | 91 |
| short squeeze risk → capped to C: high_upper_wick_ | 27 |
| short squeeze risk → capped to C: short_bounce_gua | 23 |
| extreme negative funding against short | 7 |
| MEXC-only listing (exchange confirmation missing) | 2 |
| RS-leader long vs bearish tape (counter-trend, cap | 2 |
| extreme positive funding against long crowding | 1 |
| crypto intraday long against bearish-trend regime  | 1 |
| Long setup conflicts with current market regime. | 1 |

## Interpretation

- The `move_*_pct` columns use **the last close before the decision time** as p0 and the high/low of the post-decision window. This is a **proxy**, not an exact replay.
- `reached_+0.5R_proxy` assumes risk = 1.5% (crypto) / 1% (stocks). If the move exceeded that, the price COULD have hit a typical TP1.
- `skip_saved_loss` is **conservative**: only counts when the same symbol later got A/B and that A/B turned into a real loss.
- `skip_missed_winner` triggers on either (a) same symbol later A/B and won, OR (b) price moved ≥ +1R proxy without ever becoming A/B (= filter missed a real move).

## What this DOES NOT do
- Does not promote C-tier or rejected ideas to A/B.
- Does not reduce existing filters.
- Does not write to production tables.
- Does not send Telegram.

## Read the full CSV

`reports\SKIPPED_SIGNAL_FOLLOWUP.csv`

## Recommendation

- Missed winners materially outnumber saved losses — consider opening a deeper study on the top skip reasons before any filter relaxation.