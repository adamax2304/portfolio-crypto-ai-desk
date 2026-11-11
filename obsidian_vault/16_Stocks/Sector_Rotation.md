# Sector Rotation

[src/stocks/agents/sector_rotation_agent.py](../../src/stocks/agents/sector_rotation_agent.py) ranks the sector ETFs by 20-day RS vs SPY and 20-day return, then tags each as strong / mixed / weak.

## Sector ETF map (config/stocks/universe.yaml)

| Sector | ETF |
|---|---|
| technology | XLK |
| semiconductors | SMH |
| financials | XLF |
| energy | XLE |
| consumer_discretionary | XLY |
| healthcare | XLV |
| communications | XLC |
| industrials | XLI |
| utilities | XLU |
| real_estate | XLRE |
| materials | XLB |
| consumer_staples | XLP |

## Status thresholds

- **strong** — RS vs SPY 20d ≥ +3%, ETF above EMA50
- **weak** — RS vs SPY 20d ≤ -3%, ETF below EMA50
- **mixed** — anywhere in between

## How it affects per-symbol scoring

For each candidate symbol, the scoring agent reads the symbol's sector from `symbol_sector_map` and looks up that sector's status:

- Long in a **strong** sector → +1.0 raw on `sector_confirmation` (full weight)
- Short in a **weak** sector → +1.0 raw
- Long in a **weak** sector → -6 penalty (`contradicts_sector_trend`)
- Short in a **strong** sector → -6 penalty
- Both index and sector contradict → **reject** (rule in `config/stocks/risk.yaml → confirmation.both_contradict`)

## Crypto-equity proxies

COIN and MSTR are mapped to `crypto_equity` (not in the standard sector ETF list). The scoring agent treats their sector status as `mixed` (raw=0.5) until we wire a BTC/ETH benchmark for them in a later stage.

## How to read the report's Section 2

The report shows top 3 strongest + bottom 3 weakest with their `rs_vs_spy_20d` and `return_20d`. Use this to:
1. Bias your picks toward strong-sector names for long ideas.
2. Confirm short candidates are in weak sectors before sizing up.
3. Identify rotation: if XLK was strong last week but mixed now, fading XLK breakouts is favored.
