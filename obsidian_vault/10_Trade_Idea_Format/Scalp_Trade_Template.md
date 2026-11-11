# Scalp Trade Template

Mode-specific overlay on top of the canonical idea template. Use for 30m–2h horizons.

```
# Scalp — {{symbol}} — {{date}} {{time}}

## Snapshot
- Direction: {{long|short}}
- Mode: scalp
- Timeframes: 1m/5m/15m thesis, 5m execution
- Tier: {{A|B|C|rejected}}
- Score: {{score}} (caps: ...)
- Data confidence: {{high|medium|low}}

## Why scalp
- Session: {{Asia|EU|US}} open / mid / close
- Active candidate: leader by 5m RS in {{narrative}}
- Volume ratio: {{>= 1.5x required}}
- ATR % on 5m: {{>= 0.12%}}
- Setup trigger: {{breakout|reclaim|failed_breakout|range_fade}}

## Execution
- Entry zone (acceptance into): {{entry_low}} – {{entry_high}}
- Invalidation (5m close): beyond {{invalidation}}
- Time stop: 30 minutes if no progress
- TP1 (1 ATR): {{tp1}} — take 50%
- TP2 (2 ATR): {{tp2}} — take remainder
- Stop to entry after TP1

## Derivatives
- Funding: {{funding_rate}} (must not be > +0.001 for long, < -0.001 for short)
- OI direction agrees with the trade?

## Telegram / news
- Treat as attention only; do not size on news.
- Avoid scalp 5 min before/after CPI/FOMC/major listing.

## Avoid
- Holding into the next major session if no progress
- Adding to a losing scalp
- Trading in `high-volatility danger` regime

## Notes
- {{free text}}
```

## Related

- [[Scalp_Mode]]
- [[Trade_Idea_Template]]
- [[Stop_Loss_Logic]]

## Implemented status

- **Template**.
