# Mode Viability — Stats Audit (PART 1)

**Date:** 2026-06-09 · **Scope:** Read-only audit. No code, scoring, thresholds, TP/SL, routing, or scheduler touched.
**Method:** Deduped `proposed_signals` joined with the latest `signal_outcomes` row per `signal_id` (one row per unique setup, not per tracker tick). Anchor `now = 2026-06-09T11:02:13 UTC` (newest `checked_at`).
**Sample base:** 1341 deduped signals total; 14d cutoff = 2026-05-26T11:02 UTC; data range 2026-05-22 → 2026-06-09.

## 1. Headline by window (A/B only)

| Window | Asset | n | W | L | closed | WR% | PF | netR | exp | not_tr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 48h | crypto | 19 | 8 | 4 | 12 | 66.7 | 3.75 | +11 | 5 | 2 |
| 48h | stocks | 9 | 1 | 0 | 1 | 100 | inf | +1 | 7 | 1 |
| 7d  | crypto | 75 | 16 | 20 | 36 | 44.4 | 1.85 | +17 | 20 | 19 |
| 7d  | stocks | 102 | 17 | 39 | 56 | 30.4 | 0.59 | −16 | 36 | 10 |
| 14d | crypto | 98 | 20 | 24 | 44 | 45.5 | 1.92 | +22 | 29 | 25 |
| 14d | stocks | 556 | 98 | 115 | 213 | 46.0 | 1.41 | +47 | 251 | 91 |
| ALL | crypto | 106 | 20 | 29 | 49 | 40.8 | 1.59 | +17 | 31 | 26 |
| ALL | stocks | 703 | 133 | 115 | 248 | 53.6 | 1.86 | +99 | 252 | 202 |

Net stocks ALL > 14d (+99 vs +47) because the early-window period (pre-2026-05-26) contained mostly intraday wins; the recent stocks weakness is concentrated in swing/invest.

## 2. Mode breakdown per window (A/B)

### 14d (primary judgment window)
| Asset | Mode | n | W | L | closed | WR% | PF | netR |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| crypto | **scalp** | 55 | 1 | 7 | 8 | **12.5** | **0.14** | **−6** |
| crypto | intraday | 28 | 7 | 14 | 21 | 33.3 | 1.29 | +4 |
| crypto | **swing** | 15 | 12 | 3 | 15 | **80.0** | **9.00** | **+24** |
| stocks | intraday | 463 | 93 | 72 | 165 | 56.4 | 2.17 | +84 |
| stocks | **swing** | 54 | 5 | 36 | 41 | **12.2** | **0.17** | **−30** |
| stocks | **invest** | 39 | 0 | 7 | 7 | **0.0** | **0.00** | **−7** |

### 7d (recent only)
| Asset | Mode | n | closed | WR% | PF | netR |
|---|---|---:|---:|---:|---:|---:|
| crypto | scalp | 41 | 7 | 14.3 | 0.17 | −5 |
| crypto | intraday | 24 | 19 | 36.8 | 1.50 | +6 |
| crypto | swing | 10 | 10 | 80.0 | 9.00 | +16 |
| stocks | intraday | 54 | 32 | 50.0 | 1.38 | +6 |
| stocks | swing | 26 | 20 | 5.0 | 0.05 | −18 |
| stocks | invest | 22 | 4 | 0.0 | 0.00 | −4 |

### 48h (smallest, noisiest)
- Crypto scalp 48h: n=7, **0 closed** — all expired or not-triggered. **Insufficient by itself.**
- Stocks invest 48h: n=2, **0 closed.** **Insufficient by itself.**

## 3. Crypto A/B 14d — extended slices

### By direction
| Direction | n | closed | WR% | PF | netR |
|---|---:|---:|---:|---:|---:|
| long | 55 | 29 | 48.3 | 1.87 | +13 |
| short | 43 | 15 | 40.0 | 2.00 | +9 |

### By news_supported
| news | n | closed | WR% | PF | netR |
|---|---:|---:|---:|---:|---:|
| news=1 | 25 | 12 | 50.0 | 2.83 | +11 |
| news=0 | 73 | 32 | 43.8 | 1.61 | +11 |

News-supported has higher PF and identical net R from 1/3 the sample → news is a **quality discriminator**, not a volume driver.

### Mode × news_supported (the most actionable cut)
| Mode | news | closed | WR% | PF | netR |
|---|---|---:|---:|---:|---:|
| scalp | 1 | 2 | 0 | 0.00 | −2 |
| scalp | 0 | 6 | 16.7 | 0.20 | −4 |
| intraday | 1 | 8 | 50.0 | 2.75 | +7 |
| intraday | 0 | 13 | 23.1 | 0.70 | −3 |
| swing | 1 | 2 | 100 | inf | +6 |
| swing | 0 | 13 | 76.9 | 7.00 | +18 |

Counter to intuition: **news does NOT rescue scalp** (catalyst-backed scalp still 0W/2L). For intraday and swing it sharply improves PF.

### Tier (crypto 14d A/B)
- All 98 crypto A/B in 14d are **B-tier**. **No A-tier crypto signals fired in 14d** — the bar is high enough that A is rare.

### Regime
Most signals carry empty `market_regime` (73 of 98 = legacy/unset). Among labelled:
- `bearish trend`: 4 closed, WR 50%, +4R (small sample)
- `range/chop`: 4 closed, WR 25%, −2R
- `high-volatility danger`: 3 closed, WR 33%, +1R

## 4. Stocks A/B 14d — extended slices

### By tier
| Tier | n | closed | WR% | PF | netR |
|---|---:|---:|---:|---:|---:|
| A | 66 | 32 | 18.8 | 0.31 | −18 |
| B | 490 | 181 | 50.8 | 1.73 | +65 |

⚠ **A-tier stocks underperforms B-tier by 32 points of WR and −83R net.** Most A-tier signals are pre-pause swing/invest A's (LLY A sc82–84, AAPL A sc81–84, AMD A sc79–82) that took the −1R losses on June 4–5.

### ETF vs single-name
| Bucket | n | closed | WR% | PF | netR |
|---|---:|---:|---:|---:|---:|
| ETF | 162 | 58 | 51.7 | 1.54 | +15 |
| single-name | 394 | 155 | 43.9 | 1.37 | +32 |

Both positive; single-name slightly less consistent but more volume.

### Direction
| Direction | n | closed | WR% | PF | netR |
|---|---:|---:|---:|---:|---:|
| long | 541 | 207 | 44.4 | 1.33 | +38 |
| short | 15 | 6 | 100 | inf | +9 |

**Stocks shorts: 6/6 wins (small sample, but a 100% post-fix WR is worth noting).** All from the June 5 selloff bracket (META, AMZN, SPY, QQQ, XLK, MSFT).

## 5. Pre-fix vs post-fix (stocks swing pause = 2026-06-05T19:00 UTC)

| Period | Any-tier n | A/B n | A/B closed | A/B netR |
|---|---:|---:|---:|---:|
| PRE pause | 91 | 54 | 41 | **−30R** |
| POST pause | 25 | **0** ✅ | 0 | 0 |
| POST C-tier (counterfactual) | 25 | — | 1 | +1R (24 still open/expired) |

**Leak check: 0 post-pause A/B swing signals.** Gate verified at the data layer.
Post-pause C-tier counterfactual is too thin (1 closure) to validate or invalidate the pause yet.

## 6. Pre-fix vs post-fix (Telegram 400 = 2026-06-05T19:00)

Out of scope here (covered in `POST_P1_STOCK_FIXES_RESTART_VERIFICATION.md`).

## 7. Sector / liquidity buckets

- `proposed_signals.sector` is empty for **all** stocks A/B (signals don't persist sector at insert) — cannot slice by sector from DB without rebuilding via report files. Noted as a separate observability gap; not in scope of this audit.
- Crypto liquidity proxy: `liquid_major` (BTC/ETH/SOL/BNB/XRP) = 4 scalp signals, none closed. `other_liquid` (binance non-major) = 51 of 55 scalp. Effectively all scalp is "binance non-major" — the liquidity cut does not separate scalp performance in 14d.

## 8. Confidence notes

- 14d window is the primary one — sample is large enough for crypto (98) and stocks (556) A/B and produces stable PFs.
- 7d is directionally consistent with 14d for every mode.
- 48h is too noisy to base routing on; reported only as a heartbeat.
- Crypto **A-tier is absent** in 14d — only B-tier judgements available.
- Stocks **A-tier is concentrated in failed pre-pause swing/invest batches**; A-tier intraday alone has insufficient post-pause sample.

## Verdict for PART 1
Headline shape confirmed:
- crypto swing **strongly positive** (PF 9.00 on 15 closures);
- crypto intraday **net positive but thin** (PF 1.29 — driven entirely by catalyst-backed);
- crypto scalp **−6R / PF 0.14 / WR 12.5% on 8 closures** — confirmed weak, but small absolute closure count;
- stocks intraday **+84R / PF 2.17 on 165 closures** — strongly positive;
- stocks swing **−30R / PF 0.17** before pause, **0 leaks** after;
- stocks invest **0W/7L** but every closure happened well within the 720h validity window and the sample is 7.

Deep-dive justifications follow in PART 2 (`CRYPTO_SCALP_VIABILITY_AUDIT.md`) and PART 3 (`STOCKS_INVEST_VIABILITY_AUDIT.md`).
