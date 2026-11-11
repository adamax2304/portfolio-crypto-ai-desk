# Post-Weekend Trade-by-Trade Review — A/B (72h)

_OHLCV-derived diagnosis from 15m bars (entry-reach, wick-vs-close stop, MFE milestone, stop-then-TP, overextension). Charts omitted (diagnosis-only run); crypto charts available via `_audit48_charts.py`. Stocks 15m cache path limited (TODO-stocks-chart-ohlcv-path).

## Findings summary (94 A/B triggered-or-closed diagnosed)
**Loss classification:** 11 `faded_no_mfe` (late entry / weak candidate — never
ran in favor), 4 `normal_chop`, 2 `wick_only_stop` (thin alt shorts OPG, DEXE —
stop clipped by a wick then reverted), 1 `gave_back_winner` (stocks LLY A-tier:
MFE ≥1R then reversed to stop — TP too far / no trail).
**Flags:** 43 entry_reached, 13 close_beyond_stop (legit invalidations), 11
wick_only_stop, 7 stop_then_TP (stop slightly tight — price stopped then reached
TP1; 2 are thin alts), 3 NEVER_ENTERED (correct no-fills), 48 no_ohlcv (**all
stocks** — `TODO-stocks-chart-ohlcv-path`; production tracker still has MFE/MAE
so stock diagnosis is MFE/MAE-based).

**Reads:**
- Crypto losers cluster in **scalp/intraday alt chop and late/faded entries**,
  not stop geometry. The 2 wick-only stops are thin alts (OPG, DEXE) — the same
  thin-liquidity pattern the squeeze guard targets; too few to act on.
- `stop_then_TP` (7) hints a handful of crypto stops are marginally tight, but
  the short book is net **+16R** → no stop-geometry change warranted.
- Stocks losers = the **pre-fix swing residual** (AMD/SMH/XLK/QQQ, MFE≈0, faded
  immediately — validates the pause) + **A-tier givebacks** (LLY MFE 1R→stop,
  AAPL chop). A-tier overpromotion again.
- No "stop-then-TP disaster", no stale/market-closed fills, no catalyst
  contradicting a winner.

| asset | sym | mode | dir | tier | sc | outcome | R | MFE | MAE | catalyst | diagnosis |
|---|---|---|---|---|---|---|---|---|---|---|---|
| crypto | OPN/USDT | scalp | long | B | 68 | expired | 0.0 | 1.15 | -0.2 | - | entry_reached, close_beyond_stop, MFE>=1R |
| crypto | SUSHI/USDT | scalp | long | B | 67 | loss | -1.0 | 0.2 | -1.27 | - | entry_reached, close_beyond_stop, DIAG:faded_no_mfe(late/bad-candidate) |
| crypto | SUSHI/USDT | intraday | long | B | 66 | loss | -1.0 | 0.69 | -1.57 | - | entry_reached, close_beyond_stop, MFE>=0.5R, DIAG:normal_chop |
| crypto | OPN/USDT | intraday | long | B | 66 | win | 3.0 | 3.45 | -0.92 | - | entry_reached, wick_only_stop, MFE>=2R |
| crypto | ENA/USDT | intraday | long | B | 67 | loss | -1.0 | 0.59 | -2.11 | news | entry_reached, close_beyond_stop, MFE>=0.5R, DIAG:normal_chop |
| crypto | OPG/USDT | intraday | short | B | 66 | loss | -1.0 | 0.03 | -0.94 | - | entry_reached, wick_only_stop, DIAG:wick_stop |
| crypto | BCH/USDT | intraday | short | B | 65 | loss | -1.0 | 0.09 | -1.19 | - | entry_reached, stop_then_TP, DIAG:faded_no_mfe(late/bad-candidate) |
| crypto | WLD/USDT | intraday | long | B | 66 | loss | -1.0 | 0.42 | -1.08 | - | entry_reached, close_beyond_stop, DIAG:faded_no_mfe(late/bad-candidate) |
| crypto | GPS/USDT | scalp | short | B | 66 | expired | 0.0 | 0.18 | -0.36 | - | entry_reached |
| crypto | WLD/USDT | scalp | long | B | 69 | expired | 0.0 | 0.34 | -0.52 | - | entry_reached, wick_only_stop |
| crypto | EPIC/USDT | scalp | long | B | 66 | not_triggered | 0.0 | 0 | 0 | - | entry_reached, stop_then_TP |
| crypto | C/USDT | scalp | long | B | 68 | win | 1.0 | 1.74 | -0.06 | - | entry_reached, close_beyond_stop, MFE>=1R |
| crypto | STO/USDT | scalp | long | B | 67 | expired | 0.0 | 0.1 | -0.12 | - | entry_reached, wick_only_stop |
| crypto | EPIC/USDT | intraday | long | B | 66 | not_triggered | 0.0 | 0 | 0 | - | entry_reached |
| crypto | DEXE/USDT | scalp | short | B | 66 | loss | -1.0 | 0.07 | -1.05 | - | entry_reached, wick_only_stop, DIAG:wick_stop |
| crypto | ETH/USDT | scalp | short | B | 66 | expired | 0.0 | 0.71 | -0.37 | news | entry_reached, MFE>=0.5R |
| crypto | NEAR/USDT | scalp | short | B | 67 | expired | 0.0 | 1.19 | -0.34 | news | entry_reached, MFE>=1R |
| crypto | HOME/USDT | scalp | short | B | 65 | loss | -1.0 | 0.16 | -1.17 | - | entry_reached, close_beyond_stop, DIAG:faded_no_mfe(late/bad-candidate) |
| crypto | RENDER/USDT | scalp | short | B | 65 | expired | 0.0 | 0.31 | -0.02 | - | entry_reached |
| crypto | MEME/USDT | scalp | long | B | 65 | expired | 0.0 | 0.23 | -0.78 | - | entry_reached, close_beyond_stop |
| crypto | ICP/USDT | scalp | short | B | 67 | loss | -1.0 | 0.3 | -1.15 | news | entry_reached, stop_then_TP, DIAG:faded_no_mfe(late/bad-candidate) |
| crypto | FET/USDT | scalp | short | B | 65 | expired | 0.0 | 0.27 | -0.37 | - | entry_reached |
| crypto | NEAR/USDT | swing | short | B | 70 | win | 3.0 | 3.83 | -0.77 | news | entry_reached, MFE>=2R |
| crypto | FET/USDT | swing | short | B | 66 | win | 3.0 | 3.75 | -0.37 | - | entry_reached, MFE>=2R |
| crypto | NEAR/USDT | intraday | short | B | 66 | not_triggered | 0.0 | 0 | 0 | news | NEVER_ENTERED |
| crypto | SUI/USDT | scalp | short | B | 66 | expired | 0.0 | 1.07 | -0.1 | - | entry_reached, MFE>=1R |
| crypto | ETH/USDT | intraday | short | B | 67 | win | 3.0 | 3.59 | -0.61 | news | entry_reached, MFE>=2R |
| crypto | NEAR/USDT | scalp | short | B | 67 | not_triggered | 0.0 | 0 | 0 | news | entry_reached, close_beyond_stop, stop_then_TP |
| crypto | XLM/USDT | scalp | short | B | 67 | not_triggered | 0.0 | 0 | 0 | - | entry_reached, close_beyond_stop |
| crypto | FET/USDT | scalp | short | B | 66 | not_triggered | 0.0 | 0 | 0 | news | entry_reached, wick_only_stop, stop_then_TP |
| crypto | FET/USDT | intraday | short | B | 67 | not_triggered | 0.0 | 0 | 0 | - | NEVER_ENTERED |
| crypto | BTC/USDT | scalp | short | B | 65 | not_triggered | 0.0 | 0 | 0 | news | entry_reached, wick_only_stop, stop_then_TP |
| crypto | ADA/USDT | scalp | short | B | 66 | not_triggered | 0.0 | 0 | 0 | - | NEVER_ENTERED |
| crypto | PUMP/USDT | scalp | short | B | 65 | expired | 0.0 | 0.53 | -0.15 | - | entry_reached, MFE>=0.5R |
| crypto | ADA/USDT | intraday | short | B | 66 | win | 2.0 | 3.02 | -0.02 | news | entry_reached, MFE>=2R |
| crypto | BTC/USDT | intraday | short | B | 65 | win | 3.0 | 3.35 | -0.19 | news | entry_reached, MFE>=2R |
| crypto | PUMP/USDT | intraday | short | B | 67 | win | 3.0 | 3.32 | -0.38 | - | entry_reached, MFE>=2R |
| crypto | NEAR/USDT | intraday | short | B | 67 | win | 2.0 | 2.48 | -0.45 | - | entry_reached, MFE>=2R |
| crypto | TON/USDT | scalp | short | B | 68 | not_triggered | 0.0 | 0 | 0 | - | entry_reached, close_beyond_stop |
| crypto | ETH/USDT | scalp | short | B | 65 | not_triggered | 0.0 | 0 | 0 | news | entry_reached, close_beyond_stop, stop_then_TP |
| crypto | DASH/USDT | scalp | short | B | 65 | not_triggered | 0.0 | 0 | 0 | - | entry_reached, wick_only_stop |
| crypto | TON/USDT | intraday | short | B | 66 | loss | -1.0 | 0.69 | -1.39 | - | entry_reached, close_beyond_stop, MFE>=0.5R, DIAG:normal_chop |
| crypto | AVAX/USDT | swing | short | B | 66 | win | 3.0 | 4.58 | -0.17 | - | entry_reached, MFE>=2R |
| crypto | INJ/USDT | scalp | short | B | 65 | not_triggered | 0.0 | 0 | 0 | - | entry_reached, wick_only_stop |
| crypto | ZEC/USDT | scalp | short | B | 65 | expired | 0.0 | 0.18 | -0.53 | news | entry_reached, wick_only_stop |
| crypto | BTC/USDT | scalp | short | B | 67 | expired | 0.0 | 0.52 | -0.34 | news | entry_reached, wick_only_stop, MFE>=0.5R |
| stocks | AVGO | intraday | long | A | 90 | not_triggered | 0.0 | 0 | 0 | - | no_ohlcv |
| stocks | AMD | intraday | long | B | 79 | not_triggered | 0.0 | 0 | 0 | - | no_ohlcv |
| stocks | SMH | intraday | long | B | 70 | not_triggered | 0.0 | 0 | 0 | - | no_ohlcv |
| stocks | XLK | intraday | long | B | 74 | not_triggered | 0.0 | 0 | 0 | - | no_ohlcv |
| stocks | LLY | intraday | long | B | 73 | not_triggered | 0.0 | 0 | 0 | - | no_ohlcv |
| stocks | AMD | intraday | long | A | 85 | not_triggered | 0.0 | 0 | 0 | - | no_ohlcv |
| stocks | LLY | intraday | long | A | 83 | not_triggered | 0.0 | 0 | 0 | - | no_ohlcv |
| stocks | UNH | intraday | long | B | 76 | win | 1.0 | 1.06 | -0.26 | - | no_ohlcv, MFE>=1R |
| stocks | XLV | intraday | long | B | 73 | win | 2.0 | 2.11 | -0.61 | - | no_ohlcv, MFE>=2R |
| stocks | DIA | intraday | long | B | 69 | expired | 0.0 | 0.94 | -0.25 | - | no_ohlcv, MFE>=0.8R |
| stocks | AMD | swing | long | A | 82 | loss | -1.0 | 0 | -1.02 | - | no_ohlcv, DIAG:faded_no_mfe(late/bad-candidate) |
| stocks | UNH | swing | long | B | 74 | expired | 0.0 | 0.38 | -0.29 | - | no_ohlcv |
| stocks | MSFT | swing | long | B | 71 | expired | 0.0 | 0.02 | -0.79 | - | no_ohlcv |
| stocks | LLY | swing | long | B | 68 | expired | 0.0 | 0.7 | -0.2 | - | no_ohlcv, MFE>=0.5R |
| stocks | AAPL | swing | long | B | 67 | expired | 0.0 | 0.57 | -0.39 | - | no_ohlcv, MFE>=0.5R |
| stocks | SMH | swing | long | B | 66 | loss | -1.0 | 0 | -1.09 | - | no_ohlcv, DIAG:faded_no_mfe(late/bad-candidate) |
| stocks | XLK | swing | long | B | 66 | loss | -1.0 | 0 | -1.11 | - | no_ohlcv, DIAG:faded_no_mfe(late/bad-candidate) |
| stocks | AMD | invest | long | B | 78 | expired | 0.0 | 0.09 | -0.51 | - | no_ohlcv |
| stocks | UNH | invest | long | B | 71 | expired | 0.0 | 0.17 | -0.03 | - | no_ohlcv |
| stocks | NVDA | invest | long | B | 70 | expired | 0.0 | 0.02 | -0.42 | - | no_ohlcv |
| stocks | LLY | invest | long | B | 66 | not_triggered | 0.0 | 0 | 0 | - | no_ohlcv |
| stocks | UNH | intraday | long | A | 81 | win | 1.0 | 1.01 | -0.39 | - | no_ohlcv, MFE>=1R |
| stocks | NVDA | intraday | long | B | 75 | loss | -1.0 | 0.44 | -1.43 | - | no_ohlcv, DIAG:faded_no_mfe(late/bad-candidate) |
| stocks | AAPL | intraday | long | B | 69 | win | 1.0 | 1.33 | -1.12 | - | no_ohlcv, MFE>=1R |
| stocks | LLY | intraday | long | A | 91 | loss | -1.0 | 1.0 | -0.76 | - | no_ohlcv, MFE>=1R, DIAG:gave_back_winner(TP-too-far/trail) |
| stocks | AAPL | intraday | long | A | 86 | loss | -1.0 | 0.66 | -1.03 | - | no_ohlcv, MFE>=0.5R, DIAG:normal_chop |
| stocks | XLV | intraday | long | B | 69 | loss | -1.0 | 0.29 | -1.02 | - | no_ohlcv, DIAG:faded_no_mfe(late/bad-candidate) |
| stocks | NVDA | intraday | long | B | 68 | not_triggered | 0.0 | 0 | 0 | - | no_ohlcv |
| stocks | AAPL | swing | long | A | 84 | expired | 0.0 | 0.09 | -0.77 | - | no_ohlcv |
| stocks | LLY | swing | long | A | 84 | expired | 0.0 | 0.07 | -0.54 | - | no_ohlcv |
| stocks | AMD | swing | long | A | 82 | expired | 0.0 | 0.05 | -0.5 | - | no_ohlcv |
| stocks | XLK | swing | long | B | 66 | expired | 0.0 | 0.04 | -0.83 | - | no_ohlcv |
| stocks | SMH | swing | long | B | 66 | expired | 0.0 | 0.04 | -0.66 | - | no_ohlcv |
| stocks | XLV | swing | long | B | 66 | expired | 0.0 | 0.15 | -0.34 | - | no_ohlcv |
| stocks | QQQ | swing | long | B | 66 | loss | -1.0 | 0.04 | -0.83 | - | no_ohlcv, DIAG:faded_no_mfe(late/bad-candidate) |
| stocks | JPM | intraday | long | B | 65 | expired | 0.0 | 0.17 | -0.87 | - | no_ohlcv |
| stocks | META | intraday | short | B | 77 | win | 2.0 | 2.62 | -0.25 | - | no_ohlcv, MFE>=2R |
| stocks | TSLA | intraday | short | B | 75 | expired | 0.0 | 1.03 | -0.1 | - | no_ohlcv, MFE>=1R |
| stocks | AMZN | intraday | short | B | 70 | win | 2.0 | 2.27 | -0.17 | - | no_ohlcv, MFE>=2R |
| stocks | SMH | intraday | short | B | 67 | expired | 0.0 | 0.87 | -0.23 | - | no_ohlcv, MFE>=0.8R |
| stocks | NVDA | intraday | short | B | 66 | expired | 0.0 | 0.76 | -0.29 | - | no_ohlcv, MFE>=0.5R |
| stocks | COIN | intraday | short | B | 67 | expired | 0.0 | 0.4 | -0.66 | - | no_ohlcv |
| stocks | MSTR | intraday | short | B | 68 | expired | 0.0 | 0.63 | -0.66 | - | no_ohlcv, MFE>=0.5R |
| stocks | MSFT | intraday | short | B | 65 | win | 1.0 | 1.13 | -0.38 | - | no_ohlcv, MFE>=1R |
| stocks | QQQ | intraday | short | B | 74 | win | 1.0 | 1.56 | -0.22 | - | no_ohlcv, MFE>=1R |
| stocks | AMD | intraday | short | B | 70 | expired | 0.0 | 0.53 | -0.15 | - | no_ohlcv, MFE>=0.5R |
| stocks | XLK | intraday | short | B | 67 | win | 1.0 | 1.12 | -0.18 | - | no_ohlcv, MFE>=1R |
| stocks | SPY | intraday | short | B | 68 | win | 2.0 | 2.29 | -0.34 | - | no_ohlcv, MFE>=2R |