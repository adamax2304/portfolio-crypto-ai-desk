# How to Adjust Filters

Where to tune universe / setup / scoring filters.

## Universe filters — `config/universe.yaml`

```yaml
min_24h_quote_volume_per_exchange:
  binance: 10000000   # raise to reduce noise
  bybit:    5000000
  mexc:     1500000

min_recent_candle_quote_volume:
  scalp:   20000     # lower to surface more scalp candidates
  intraday: 75000
  swing:   150000

max_spread_pct: 0.35    # lower to require tighter books

min_atr_percent:
  scalp:   0.12        # raise to require more volatility
  intraday: 0.35
  swing:   0.80
```

Effect: tighter filters → fewer candidates → fewer ideas. Loose filters → more ideas but more noise and rejections.

## Discovery overrides

```yaml
discovery_overrides:
  max_symbols_for_rank_scan: 250
  max_symbols_for_deep_analysis: 50
  max_symbols_for_trade_ideas: 20
  min_24h_quote_volume_per_exchange:
    binance: 5000000
    bybit:   2000000
    mexc:     500000
```

Activated via `--discovery` flag.

## Score thresholds — `config/scoring.yaml`

```yaml
thresholds:
  a_tier: 80     # increase to require even higher conviction A
  b_tier: 65     # increase to make B rarer
  c_tier: 50     # watchlist floor
```

⚠ Changing these has cascade effects. The current values are calibrated for current weights and caps.

## Component weights

```yaml
weights:
  market_regime:     15
  technical_setup:   20
  momentum:          15
  derivatives:       15
  catalyst_news:     15
  narrative:         10
  execution_quality: 10
```

Total should be ~100 so component scores remain comparable across configurations.

## Regime / mode multipliers

In `scoring.yaml.regime_weights` and `scoring.yaml.mode_weights`. Values between 0.7 and 1.3 are gentle nudges. Going outside that band changes the desk's character significantly.

## Risk penalties

```yaml
risk_penalties:
  regime_conflict:       8
  overextended:          8
  poor_risk_reward:     10
  low_liquidity:         8
  no_clear_invalidation:15  # hard rule — do not lower
  missing_derivatives:   2
  missing_news:          2
  too_many_warnings:     5
```

`no_clear_invalidation` is essentially an enforced rule. Do not lower it below 10.

## Score caps

Cap values are **hardcoded in `scoring_agent.py`**, not in YAML:

```python
caps.append((50.0, "no clean invalidation"))
caps.append((70.0, "MEXC-only listing"))
caps.append((75.0, "not listed on anchor"))
caps.append((60.0, "low liquidity"))
caps.append((50.0, "stale data (>3h old)"))
caps.append((55.0, "unverified rumor-only catalyst"))
caps.append((78.0, "extreme positive funding against long"))
caps.append((78.0, "extreme negative funding against short"))
```

To adjust them, edit the agent. Recommended improvement: move into `scoring.yaml`.

## Workflow

1. Edit the config (or agent).
2. Re-run `python -m src.cli update-universe` + `intraday-report`.
3. Compare outputs vs baseline.
4. Roll back if the new behavior is worse.

## Related

- [[Why_Too_Many_Watchlist]]
- [[Why_No_Trades]]
- [[Scoring_Overview]]

## Implemented status

- **Implemented** (filter editing). Caps-in-YAML is **Recommended**.
