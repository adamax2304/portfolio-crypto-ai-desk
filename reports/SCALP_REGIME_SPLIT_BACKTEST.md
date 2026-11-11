# Scalp Regime Split Backtest (PART 6)

**Date:** 2026-06-15 · Policy A, 12mo 5m, 139,014 trades. Source: `SCALP_SPLIT_SUMMARY.json`.

## By trend / direction

| Subset | n | WR | PF | avg R |
|---|---:|---:|---:|---:|
| downtrend (shorts) | 70,710 | 44% | 0.68 | −0.387 |
| uptrend (longs) | 68,304 | 41% | 0.58 | −0.548 |

Shorts mildly less bad than longs; both clearly negative.

## By session

| Session (UTC) | n | WR | PF | avg R |
|---|---:|---:|---:|---:|
| US (14:00–24:00) | 58,251 | 43% | 0.70 | −0.357 |
| Europe (08:00–14:00) | 35,361 | 43% | 0.60 | −0.517 |
| Asia (00:00–08:00) | 45,402 | 42% | 0.57 | −0.566 |

US session best, Asia worst; **all negative**.

## By symbol (liquidity / ATR% proxy)

| Symbol | n | WR | PF | avg R |
|---|---:|---:|---:|---:|
| NEAR | 9,240 | 45% | 0.92 | −0.082 |
| ARB | 9,191 | 44% | 0.87 | −0.139 |
| LINK | 9,842 | 45% | 0.85 | −0.157 |
| OP | 9,056 | 43% | 0.84 | −0.164 |
| SUI / APT / AVAX / ADA / TON / DOGE | — | 43-46% | 0.71-0.80 | −0.22 … −0.34 |
| SOL | 9,357 | 44% | 0.65 | −0.423 |
| XRP | 9,148 | 43% | 0.54 | −0.606 |
| ETH | 9,294 | 40% | 0.45 | −0.809 |
| BNB | 8,853 | 36% | 0.29 | −1.278 |
| BTC | 8,787 | 32% | 0.18 | **−1.854** |

**The clearest pattern in the whole study.** The lowest-volatility majors (BTC, BNB, ETH) are catastrophic; higher-ATR mid-caps approach breakeven. This is the fee mechanism made visible: smaller ATR% → tighter stop in price terms → 15bps round-trip is a larger fraction of 1R → worse net.

## Answers

- **When does scalp work?** Never net-positive in any tested slice. Closest-to-breakeven: higher-ATR mid-caps (NEAR/ARB/LINK), US session, short side — but still < 0.
- **When does it fail worst?** Low-ATR majors (BTC/BNB/ETH), Asia session, long side.
- **Session-gate it?** US-only helps marginally (−0.36 vs −0.57 Asia) but doesn't fix it.
- **Regime-gate it?** No regime is positive.
- **Weekend-disable?** Not separately split here, but session/regime gates don't rescue net R, so a weekend gate alone wouldn't either.
- **Symbol/liquidity-gate it?** Excluding BTC/BNB/ETH would roughly halve the loss but not flip it positive.

**No gate makes scalp net-positive under realistic fees.**
