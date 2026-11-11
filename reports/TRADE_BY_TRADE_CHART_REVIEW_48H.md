# Trade-by-Trade Chart Review — 48h (A/B)

_Charts under `reports/trade_charts/48h/`. Diagnosis auto-derived from 15m OHLCV (same data a chart shows): entry-reach, late-entry, wick-vs-close stop, MFE milestones, stop-then-TP, overextension. Read-only._

| asset | sym | mode | dir | tier | sc | outcome | R | MFE | MAE | diagnosis |
|---|---|---|---|---|---|---|---|---|---|---|
| stocks | AAPL | intraday | long | B | 77 | loss | -1.0 | 0.17 | -1.05 | no_ohlcv |
| stocks | SMH | intraday | long | B | 78 | loss | -1.0 | 0.48 | -1.37 | no_ohlcv |
| stocks | AMD | intraday | long | B | 79 | loss | -1.0 | 0.12 | -1.32 | no_ohlcv |
| stocks | QQQ | intraday | long | B | 69 | win | 1.0 | 1.06 | -2.58 | no_ohlcv, MFE>=1R |
| stocks | XLK | intraday | long | B | 74 | win | 1.0 | 1.34 | -3.2 | no_ohlcv, MFE>=1R |
| stocks | SMCI | intraday | long | B | 71 | loss | -1.0 | 0 | -1.34 | no_ohlcv |
| stocks | NVDA | intraday | long | B | 78 | loss | -1.0 | 0.23 | -1.16 | no_ohlcv |
| stocks | AAPL | swing | long | B | 77 | expired | 0.0 | 0.33 | -0.63 | no_ohlcv |
| stocks | QQQ | swing | long | B | 75 | loss | -1.0 | 0.16 | -1.49 | no_ohlcv |
| stocks | AMD | swing | long | B | 75 | loss | -1.0 | 0.67 | -0.91 | no_ohlcv, MFE>=0.5R |
| stocks | SMCI | swing | long | B | 72 | loss | -1.0 | 0.13 | -0.87 | no_ohlcv |
| stocks | XLK | swing | long | B | 70 | loss | -1.0 | 0.08 | -1.36 | no_ohlcv |
| stocks | SMH | swing | long | B | 70 | loss | -1.0 | 0.34 | -1.27 | no_ohlcv |
| stocks | NVDA | swing | long | B | 70 | loss | -1.0 | 0.09 | -1.06 | no_ohlcv |
| stocks | AAPL | invest | long | B | 71 | expired | 0.0 | 0.14 | -0.27 | no_ohlcv |
| stocks | QQQ | invest | long | B | 71 | expired | 0.0 | 0.06 | -0.78 | no_ohlcv |
| stocks | AMD | invest | long | B | 70 | expired | 0.0 | 0.25 | -0.64 | no_ohlcv |
| stocks | SMCI | invest | long | B | 68 | loss | -1.0 | 0.06 | -0.96 | no_ohlcv |
| stocks | SMH | invest | long | B | 66 | expired | 0.0 | 0.18 | -0.9 | no_ohlcv |
| stocks | XLK | invest | long | B | 65 | loss | -1.0 | 0.04 | -1.12 | no_ohlcv |
| stocks | SMCI | intraday | long | A | 82 | loss | -1.0 | 0 | -1.34 | no_ohlcv |
| stocks | AVGO | intraday | long | B | 70 | win | 1.0 | 1.17 | -5.16 | no_ohlcv, MFE>=1R |
| stocks | NVDA | swing | long | A | 81 | loss | -1.0 | 0.09 | -1.06 | no_ohlcv |
| stocks | MSFT | swing | long | B | 75 | loss | -1.0 | 0.1 | -0.87 | no_ohlcv |
| stocks | TSLA | swing | long | B | 67 | loss | -1.0 | 0.69 | -0.79 | no_ohlcv, MFE>=0.5R |
| stocks | NVDA | invest | long | B | 75 | expired | 0.0 | 0 | -0.67 | no_ohlcv |
| stocks | MSFT | invest | long | B | 70 | expired | 0.0 | 0.01 | -0.43 | no_ohlcv |
| stocks | AAPL | intraday | long | A | 90 | loss | -1.0 | 0.4 | -1.11 | no_ohlcv |
| stocks | AMD | intraday | long | A | 88 | loss | -1.0 | 1.25 | -1.97 | no_ohlcv, MFE>=1R |
| stocks | SMH | intraday | long | A | 83 | loss | -1.0 | 0.83 | -2.53 | no_ohlcv, MFE>=0.8R |
| crypto | NEAR/USDT | intraday | long | B | 65 | loss | -1.0 | 0.9 | -1.25 | entry_reached, close_beyond_stop, MFE>=0.8R |
| crypto | EPIC/USDT | intraday | long | B | 66 | loss | -1.0 | 0 | -1.03 | entry_reached, close_beyond_stop |
| stocks | TSLA | intraday | long | B | 77 | loss | -1.0 | 0.12 | -1.07 | no_ohlcv |
| crypto | ONDO/USDT | scalp | long | B | 66 | expired | 0.0 | 0.37 | -0.67 | entry_reached, wick_only_stop |
| crypto | ZRO/USDT | scalp | long | B | 65 | not_triggered | 0.0 | 0 | 0 | entry_reached, wick_only_stop |
| crypto | XPL/USDT | scalp | long | B | 65 | not_triggered | 0.0 | 0 | 0 | entry_reached, close_beyond_stop |
| stocks | LLY | intraday | long | B | 73 | win | 3.0 | 3.09 | -0.29 | no_ohlcv, MFE>=2R |
| crypto | SAHARA/USDT | scalp | short | B | 68 | loss | -1.0 | 0.84 | -1.32 | entry_reached, close_beyond_stop, MFE>=0.8R |
| crypto | ZRO/USDT | intraday | long | B | 65 | win | 2.0 | 2.22 | -2.02 | entry_reached, wick_only_stop, MFE>=2R |
| crypto | ENA/USDT | intraday | long | B | 65 | loss | -1.0 | 0.26 | -1.37 | entry_reached, wick_only_stop |
| crypto | WLD/USDT | scalp | long | B | 68 | expired | 0.0 | 0.48 | -0.41 | entry_reached, wick_only_stop |
| crypto | OPN/USDT | scalp | long | B | 68 | loss | -1.0 | 0.38 | -1.15 | entry_reached, wick_only_stop |
| crypto | OPN/USDT | scalp | long | B | 68 | expired | 0.0 | 1.15 | -0.2 | entry_reached, MFE>=1R |
| crypto | SUSHI/USDT | scalp | long | B | 67 | loss | -1.0 | 0.2 | -1.27 | entry_reached, close_beyond_stop |
| crypto | SUSHI/USDT | intraday | long | B | 66 | loss | -1.0 | 0.69 | -1.57 | entry_reached, close_beyond_stop, MFE>=0.5R |
| stocks | AVGO | intraday | long | A | 90 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| stocks | AMD | intraday | long | B | 79 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| stocks | SMH | intraday | long | B | 70 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| stocks | XLK | intraday | long | B | 74 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| stocks | LLY | intraday | long | B | 73 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| crypto | OPN/USDT | intraday | long | B | 66 | win | 3.0 | 3.45 | -0.92 | entry_reached, MFE>=2R |
| crypto | ENA/USDT | intraday | long | B | 67 | loss | -1.0 | 0.59 | -2.11 | entry_reached, close_beyond_stop, MFE>=0.5R |
| crypto | OPG/USDT | intraday | short | B | 66 | loss | -1.0 | 0.03 | -0.94 | entry_reached, wick_only_stop |
| crypto | BCH/USDT | intraday | short | B | 65 | loss | -1.0 | 0.09 | -1.19 | entry_reached, close_beyond_stop |
| crypto | WLD/USDT | intraday | long | B | 66 | loss | -1.0 | 0.42 | -1.08 | entry_reached, wick_only_stop |
| crypto | GPS/USDT | scalp | short | B | 66 | expired | 0.0 | 0.18 | -0.36 | entry_reached |
| crypto | WLD/USDT | scalp | long | B | 69 | expired | 0.0 | 0.34 | -0.52 | entry_reached, wick_only_stop |
| crypto | EPIC/USDT | scalp | long | B | 66 | not_triggered | 0.0 | 0 | 0 | entry_reached, wick_only_stop |
| crypto | C/USDT | scalp | long | B | 68 | win | 1.0 | 1.74 | -0.06 | entry_reached, close_beyond_stop, MFE>=1R |
| crypto | STO/USDT | scalp | long | B | 67 | expired | 0.0 | 0.1 | -0.12 | entry_reached, wick_only_stop |
| stocks | AMD | intraday | long | A | 85 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| crypto | EPIC/USDT | intraday | long | B | 66 | win | 2.0 | 2.42 | -0.81 | entry_reached, MFE>=2R |
| crypto | DEXE/USDT | scalp | short | B | 66 | loss | -1.0 | 0.07 | -1.05 | entry_reached, wick_only_stop |
| stocks | LLY | intraday | long | A | 83 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| crypto | ETH/USDT | scalp | short | B | 66 | expired | 0.0 | 0.71 | -0.37 | entry_reached, wick_only_stop, MFE>=0.5R |
| crypto | NEAR/USDT | scalp | short | B | 67 | expired | 0.0 | 1.19 | -0.34 | entry_reached, MFE>=1R |
| crypto | HOME/USDT | scalp | short | B | 65 | loss | -1.0 | 0.16 | -1.17 | entry_reached, close_beyond_stop |
| crypto | RENDER/USDT | scalp | short | B | 65 | expired | 0.0 | 0.31 | -0.02 | entry_reached, close_beyond_stop |
| crypto | MEME/USDT | scalp | long | B | 65 | expired | 0.0 | 0.23 | -0.78 | entry_reached, close_beyond_stop |
| crypto | ICP/USDT | scalp | short | B | 67 | loss | -1.0 | 0.3 | -1.15 | entry_reached, close_beyond_stop |
| stocks | UNH | intraday | long | B | 76 | win | 1.0 | 1.06 | -0.26 | no_ohlcv, MFE>=1R |
| stocks | XLV | intraday | long | B | 73 | win | 2.0 | 2.11 | -0.61 | no_ohlcv, MFE>=2R |
| stocks | DIA | intraday | long | B | 69 | expired | 0.0 | 0.94 | -0.25 | no_ohlcv, MFE>=0.8R |
| crypto | FET/USDT | scalp | short | B | 65 | expired | 0.0 | 0.27 | -0.37 | entry_reached |
| crypto | NEAR/USDT | swing | short | B | 70 | win | 3.0 | 3.83 | -0.77 | entry_reached, MFE>=2R |
| crypto | FET/USDT | swing | short | B | 66 | win | 3.0 | 3.75 | -0.37 | entry_reached, MFE>=2R |
| stocks | AMD | swing | long | A | 82 | loss | -1.0 | 0 | -1.02 | no_ohlcv |
| stocks | UNH | swing | long | B | 74 | expired | 0.0 | 0.38 | -0.29 | no_ohlcv |
| stocks | MSFT | swing | long | B | 71 | expired | 0.0 | 0.02 | -0.58 | no_ohlcv |
| stocks | LLY | swing | long | B | 68 | expired | 0.0 | 0.7 | -0.2 | no_ohlcv, MFE>=0.5R |
| stocks | AAPL | swing | long | B | 67 | expired | 0.0 | 0.57 | -0.1 | no_ohlcv, MFE>=0.5R |
| stocks | SMH | swing | long | B | 66 | loss | -1.0 | 0 | -1.09 | no_ohlcv |
| stocks | XLK | swing | long | B | 66 | loss | -1.0 | 0 | -1.11 | no_ohlcv |
| stocks | AMD | invest | long | B | 78 | expired | 0.0 | 0.09 | -0.41 | no_ohlcv |
| stocks | UNH | invest | long | B | 71 | expired | 0.0 | 0.17 | -0.03 | no_ohlcv |
| stocks | NVDA | invest | long | B | 70 | expired | 0.0 | 0.02 | -0.33 | no_ohlcv |
| stocks | LLY | invest | long | B | 66 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| stocks | UNH | intraday | long | A | 81 | win | 1.0 | 1.01 | -0.39 | no_ohlcv, MFE>=1R |
| crypto | NEAR/USDT | intraday | short | B | 66 | not_triggered | 0.0 | 0 | 0 | NEVER_ENTERED |
| stocks | NVDA | intraday | long | B | 75 | loss | -1.0 | 0.44 | -1.43 | no_ohlcv |
| stocks | AAPL | intraday | long | B | 69 | win | 1.0 | 1.33 | -0.61 | no_ohlcv, MFE>=1R |
| crypto | SUI/USDT | scalp | short | B | 66 | expired | 0.0 | 1.07 | -0.1 | entry_reached, MFE>=1R |
| crypto | ETH/USDT | intraday | short | B | 67 | win | 3.0 | 3.59 | -0.61 | entry_reached, MFE>=2R |
| crypto | NEAR/USDT | scalp | short | B | 67 | not_triggered | 0.0 | 0 | 0 | entry_reached, close_beyond_stop |
| crypto | XLM/USDT | scalp | short | B | 67 | not_triggered | 0.0 | 0 | 0 | NEVER_ENTERED |
| crypto | FET/USDT | scalp | short | B | 66 | not_triggered | 0.0 | 0 | 0 | entry_reached, wick_only_stop |
| crypto | FET/USDT | intraday | short | B | 67 | not_triggered | 0.0 | 0 | 0 | NEVER_ENTERED |
| crypto | BTC/USDT | scalp | short | B | 66 | not_triggered | 0.0 | 0 | 0 | entry_reached, close_beyond_stop |
| crypto | ADA/USDT | scalp | short | B | 66 | not_triggered | 0.0 | 0 | 0 | NEVER_ENTERED |
| crypto | PUMP/USDT | scalp | short | B | 65 | expired | 0.0 | 0.53 | -0.15 | entry_reached, MFE>=0.5R |
| crypto | ADA/USDT | intraday | short | B | 66 | expired | 0.0 | 0.38 | -0.02 | entry_reached |
| crypto | BTC/USDT | intraday | short | B | 65 | win | 2.0 | 2.63 | -0.19 | entry_reached, MFE>=2R |
| crypto | PUMP/USDT | intraday | short | B | 67 | expired | 0.0 | 0.22 | -0.1 | entry_reached |
| crypto | NEAR/USDT | intraday | short | B | 67 | expired | 0.0 | 0.08 | -0.45 | entry_reached |
| crypto | TON/USDT | scalp | short | B | 68 | waiting_for_entry | None | 0 | 0 |  |
| crypto | ETH/USDT | scalp | short | B | 65 | win | 1.0 | 1.68 | -0.68 | entry_reached, MFE>=1R |
| crypto | DASH/USDT | scalp | short | B | 65 | waiting_for_entry | None | 0 | 0 |  |
| stocks | LLY | intraday | long | A | 91 | expired | 0.0 | 1.0 | -0.11 | no_ohlcv, MFE>=1R |
| stocks | AAPL | intraday | long | A | 86 | loss | -1.0 | 0.66 | -1.03 | no_ohlcv, MFE>=0.5R |
| stocks | XLV | intraday | long | B | 69 | expired | 0.0 | 0.29 | -0.74 | no_ohlcv |
| stocks | NVDA | intraday | long | B | 68 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| crypto | TON/USDT | intraday | short | B | 66 | waiting_for_entry | None | 0 | 0 |  |
| crypto | AVAX/USDT | swing | short | B | 66 | waiting_for_entry | None | 0 | 0 |  |
| crypto | INJ/USDT | scalp | short | B | 65 | waiting_for_entry | None | 0 | 0 |  |
| stocks | AAPL | swing | long | A | 84 | expired | 0.0 | 0.09 | -0.47 | no_ohlcv |
| stocks | LLY | swing | long | A | 84 | expired | 0.0 | 0.07 | -0.26 | no_ohlcv |
| stocks | AMD | swing | long | A | 82 | expired | 0.0 | 0.05 | -0.35 | no_ohlcv |
| stocks | XLK | swing | long | B | 66 | expired | 0.0 | 0.04 | -0.46 | no_ohlcv |
| stocks | SMH | swing | long | B | 66 | expired | 0.0 | 0.04 | -0.35 | no_ohlcv |
| stocks | XLV | swing | long | B | 66 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| stocks | QQQ | swing | long | B | 66 | expired | 0.0 | 0.04 | -0.53 | no_ohlcv |
| stocks | LLY | invest | long | A | 82 | waiting_for_entry | None | 0 | 0 | no_ohlcv |
| stocks | AAPL | invest | long | A | 81 | waiting_for_entry | None | 0 | 0 | no_ohlcv |
| stocks | AMD | invest | long | B | 79 | waiting_for_entry | None | 0 | 0 | no_ohlcv |
| stocks | SMH | invest | long | B | 67 | waiting_for_entry | None | 0 | 0 | no_ohlcv |
| stocks | XLK | invest | long | B | 65 | waiting_for_entry | None | 0 | 0 | no_ohlcv |
| crypto | ZEC/USDT | scalp | short | B | 65 | waiting_for_entry | None | 0 | 0 |  |
| stocks | JPM | intraday | long | B | 65 | expired | 0.0 | 0.11 | -0.87 | no_ohlcv |
| stocks | META | intraday | short | B | 77 | expired | 0.0 | 0.09 | -0.04 | no_ohlcv |
| stocks | TSLA | intraday | short | B | 75 | expired | 0.0 | 0.13 | -0.1 | no_ohlcv |
| stocks | AMZN | intraday | short | B | 70 | expired | 0.0 | 0.19 | -0.03 | no_ohlcv |
| stocks | SMH | intraday | short | B | 67 | expired | 0.0 | 0.13 | -0.26 | no_ohlcv |
| stocks | NVDA | intraday | short | B | 66 | not_triggered | 0.0 | 0 | 0 | no_ohlcv |
| stocks | COIN | intraday | short | B | 67 | expired | 0.0 | 0.16 | -0.17 | no_ohlcv |
| stocks | MSTR | intraday | short | B | 68 | expired | 0.0 | 0.24 | -0.12 | no_ohlcv |
| stocks | MSFT | intraday | short | B | 65 | expired | 0.0 | 0.2 | -0.22 | no_ohlcv |
| stocks | QQQ | intraday | short | B | 74 | waiting_for_entry | None | 0 | 0 | no_ohlcv |
| stocks | AMD | intraday | short | B | 70 | waiting_for_entry | None | 0 | 0 | no_ohlcv |
| stocks | XLK | intraday | short | B | 67 | waiting_for_entry | None | 0 | 0 | no_ohlcv |
| stocks | SPY | intraday | short | B | 68 | waiting_for_entry | None | 0 | 0 | no_ohlcv |