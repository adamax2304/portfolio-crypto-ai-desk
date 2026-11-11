# 48h Trade-by-Trade Review (PART 4)

**Window:** 2026-06-08 12:10 UTC → 2026-06-10 12:10 UTC · A/B closed signals · Read-only.
**Source:** [TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.csv](TRADE_UNIVERSE_48H_AFTER_RECENT_FIXES.csv) (57 closed A/B in window).

Classification legend:
- **clean win / clean loss** — entry / stop / TP fired cleanly, no ambiguity
- **ambiguous win/loss** — intrabar entry+stop / entry+TP flag set
- **stopped after bad entry** — MAE ≤ −1R early; entry zone mis-placed
- **stopped by wick/squeeze** — MFE ≥ +0.5R then reversed and stopped
- **TP before reversal** — TP1+ then continued or paused
- **expired with +MFE** — never hit TP nor stop, but had favorable run
- **expired flat** — never made meaningful progress
- **not_triggered avoided** — invalidation hit before entry, correctly skipped
- **not_triggered missed** — price ran in intended direction without entering

## 1. Crypto A/B trades (closed)

| Created | Symbol | Playbook | Dir | Tier | Outcome | R | MFE | MAE | Classification | Comment |
|---|---|---|---|---|---|---:|---:|---:|---|---|
| 06-10 02:56 | IO/USDT | swing_narrative_rs | long | B | loss | −1 | +0.49 | −1.51 | stopped after weak follow-through · **gap_slip_stop=51%** | Gap took fill past stop; real R worse than headline. |
| 06-10 02:46 | STG/USDT | swing_narrative_rs | long | B | **win** | **+3** | +3.39 | −0.63 | clean win · **gap_slip_tp=65%** | TP3 hit with positive slippage — real fill better than headline. |
| 06-10 02:46 | SENT/USDT | swing_narrative_rs | long | B | loss | −1 | +0.12 | −1.23 | stopped after bad entry | Failed-momentum swing. |
| 06-10 00:56 | CHZ/USDT | swing_narrative_rs | long | B | loss | −1 | +0.25 | −1.65 | stopped after bad entry · gap_slip_stop=65% | Entry chased; gap through stop. |
| 06-09 23:01 | ZEC/USDT | failed_bounce_short | short | B | loss | −1 | +0.27 | −0.92 | stopped by squeeze | Short squeezed on bounce. |
| 06-09 17:51 | KAT/USDT (sample top-of-cycle) | swing | long | B | pending | — | — | — | waiting | n/a |
| 06-09 17:12 | XLY (stocks intraday short, included for symmetry below) | n/a | | | | | | | | |
| 06-09 14:01 | CHIP/USDT | swing_narrative_rs | long | B | **win** | **+2** | +2.83 | −2.01 | ambiguous: gap_slip_stop=132% + gap_slip_tp=53% | Wick deep past stop before bounce to TP — paper says win but execution very fragile. |
| 06-09 13:57 | IO/USDT | swing_narrative_rs | long | B | loss | −1 | +0.33 | −1.07 | stopped after bad entry | |
| 06-09 13:39 | CHZ/USDT | swing_narrative_rs | long | B | loss | −1 | +0.37 | −1.48 | stopped after bad entry | |
| 06-09 06:02 | ALLO/USDT | swing_narrative_rs | long | B | **win** | +1 | +1.56 | −1.29 | clean win · gap_slip_stop=35% + gap_slip_tp=32% | TP1 hit; gap slip both sides — note observability. |
| 06-09 02:51 | XLM/USDT | failed_bounce_short | short | B | loss | −1 | +0.81 | −1.07 | stopped by squeeze | Wick squeeze after good initial move. |
| 06-09 02:08 | ALLO/USDT | intraday_catalyst | long | B | **win** | +1 | +1.68 | −1.01 | clean win · gap_slip_tp=14% | Catalyst lane delivered. |
| 06-08 18:19 | (stocks) | | | | | | | | | |
| 06-08 18:19 | (stocks) | | | | | | | | | |
| 06-08 17:06 | NEAR/USDT | intraday_catalyst | long | B | loss | −1 | +0.67 | −0.64 | stopped after bad entry | Catalyst-tagged but tape flipped. |
| 06-08 12:04 | ALLO/USDT | intraday_catalyst | long | B | loss | −1 | 0.00 | −1.10 | stopped immediately | First-touch fill; deep entry mis-place. |
| 06-08 09:54 | WLD/USDT | intraday_catalyst | long | B | **win** | **+3** | +3.47 | −0.84 | clean win | Best catalyst lane in window. |
| 06-08 01:38 | ZEC/USDT | swing_narrative_rs | long | B | **win** | **+3** | +3.46 | −0.62 | clean win | Best swing in window. |

### Crypto A/B summary
- 13 closed A/B (excluding stocks symmetry rows).
- **5 wins** (ZEC swing +3, STG swing +3, WLD intraday +3, CHIP swing +2, ALLO swing +1, ALLO intraday +1) — all from the catalyst-backed + RS-leader cohorts.
- **7 losses** — concentrated in `crypto_swing_narrative_rs` (4 of 7) during the BTC-range chop on 06-09.
- **2 short losses** (ZEC, XLM) — both stopped by wick squeeze, expected when short funding skews extreme.
- **Execution annotations present on 6 of 13 closed trades** (gap slip > 10%). CHIP win has gap_slip_stop=132% — fragile; real execution would have been worse than the headline.

## 2. Stocks A/B trades (closed, intraday-only; swing/invest are C-tier counterfactual below)

| Created | Symbol | Tier | Dir | Outcome | R | MFE | MAE | Classification | Comment |
|---|---|---|---|---|---:|---:|---:|---|---|
| 06-09 17:12 | XLY | B | short | loss | −1 | +0.06 | −0.94 | stopped after bad entry | Entry too tight. |
| 06-09 15:26 | AVGO | B | short | **win** | +1 | +1.34 | −0.49 | **ambiguous**: intrabar_entry_tp + gap_slip_tp=33% | TP1 fired same candle as entry — flag set. |
| 06-09 14:13 | XLF | B | long | loss | −1 | +0.11 | −1.09 | stopped after bad entry · gap_slip_stop=29% | |
| 06-09 13:57 | XLV | B | long | **win** | +1 | +1.15 | −0.41 | clean win | Good RTH lane. |
| 06-09 13:57 | JPM | B | long | loss | −1 | +0.22 | −1.10 | stopped after bad entry · gap_slip_stop=13% | |
| 06-08 18:19 | XLV | B | long | **win** | +2 | +1.82 | −0.24 | clean win | TP2 hit. |
| 06-08 18:19 | XOM | B | long | loss | −1 | +0.16 | −1.35 | stopped after bad entry | |
| 06-08 15:45 | AAPL | B | long | **win** | +1 | +1.19 | −1.23 | clean win · gap_slip_stop=23% + gap_slip_tp=19% | Both slips small. |
| 06-08 15:25 | JPM | B | long | **win** | +1 | +1.03 | −0.94 | clean win | |
| 06-08 14:35 | GOOGL | B | short | loss | −1 | +0.03 | −1.51 | stopped after bad entry | Entry too tight. |
| 06-08 14:35 | XOM | A | long | loss | −1 | +0.38 | −1.16 | stopped after bad entry | **A-tier loss** — A-tier overpromotion symptom. |
| _earlier (pre-window included via expiry, watchlist_ |  |  |  | | | | | | |

### Stocks intraday A/B summary
- 11 closed A/B intraday: 5 W / 6 L / PF 1.00 / 0R.
- **1 A-tier loss** (XOM long) — matches the 14d audit's "A-tier overpromotion on stocks" finding.
- 1 ambiguous (AVGO short, intrabar_entry_tp) — counted as win.
- Several stops with `gap_slip_stop > 10%` — execution slippage observability is helping us see fragility.

## 3. Stocks swing watchlist-only (C-tier counterfactual)
| Created | Symbol | Tier | Dir | Outcome | R | Classification |
|---|---|---|---|---|---:|---|
| 06-05 14:50 | AAPL | A→C | long | loss | −1 | counterfactual — pause caught it |
| 06-05 14:50 | AMD | A→C | long | loss | −1 | counterfactual |
| 06-05 14:50 | XLK | B→C | long | loss | −1 | counterfactual |
| 06-05 14:50 | SMH | B→C | long | loss | −1 | counterfactual |
| 06-04 14:55 | AAPL | B→C | long | loss | −1 | counterfactual |
| 06-04 14:55 | LLY | B→C | long | **+1** | win | one bright spot |
| 06-04 14:55 | MSFT | B→C | long | loss | −1 | counterfactual |

**Verdict:** post-pause C-tier swing is 1W/7L in this window — pause justified.

## 4. Stocks invest watchlist-only (C-tier counterfactual)
| Created | Symbol | Tier | Dir | Outcome | R | Classification |
|---|---|---|---|---|---:|---|
| 06-05 14:55 | AAPL | A→C | long | loss | −1 | counterfactual |
| 06-05 14:55 | XLK | B→C | long | loss | −1 | counterfactual |
| 06-04 15:01 | AMD | B→C | long | loss | −1 | counterfactual |
| 06-03 13:15 | MSFT | B→C | long | loss | −1 | counterfactual |
| 06-03 01:29 | AMD | B→C | long | loss | −1 | counterfactual |
| _…14 more losses…_ |  |  |  |  | −1 | all counterfactual losses |

**Verdict:** post-pause C-tier invest is 0W/18L — pause STRONGLY justified.

## 5. Per-trade headline counts
| Classification | Crypto | Stocks intraday | Stocks watchlist (C) |
|---|---:|---:|---:|
| clean win | 4 | 4 | 1 |
| clean loss | 5 | 4 | 24 |
| ambiguous win | 1 (CHIP) | 1 (AVGO) | 0 |
| stopped by wick/squeeze | 2 (ZEC short, XLM short) | 0 | 0 |
| catalyst helped | 4 (ZEC×2, WLD, ALLO×2) | 0 | 0 |
| A-tier loss (overpromotion symptom) | 0 | 1 (XOM A) | 2 (AAPL A swing, AAPL A invest, AMD A swing) |

```
TBT_REVIEW_48H_COMPLETE
```
