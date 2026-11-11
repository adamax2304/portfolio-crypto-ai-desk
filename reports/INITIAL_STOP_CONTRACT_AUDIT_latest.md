# Initial Stop Contract Audit

- DB: `C:\Users\adama\Documents\crypto-ai-desk\db\crypto_ai_desk.sqlite`
- Window: last 14 days

## Proposed Signals

| Asset | Mode | Stop source | Count |
|---|---|---|---|
| stocks | intraday | legacy_atr_stop | 1283 |
| crypto | intraday | atr_fallback | 210 |
| crypto | swing | atr_fallback | 183 |
| crypto | scalp | atr_fallback | 149 |
| crypto | scalp | support_resistance | 13 |
| crypto | swing | support_resistance | 10 |
| crypto | intraday | support_resistance | 8 |

## Live Decisions

| Asset | Mode | Stop source | Count |
|---|---|---|---|
| crypto | swing | missing | 152 |
| crypto | intraday | missing | 116 |
| stock_futures | stock_intraday | legacy_atr_stop | 36 |
| crypto | liquidity_sweep | liquidity_sweep_extreme | 1 |
