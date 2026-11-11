# MacroGeopoliticsAgent

## File

[src/agents/macro_geopolitics_agent.py](../../src/agents/macro_geopolitics_agent.py).

## Role

Scan recent news headlines for macro / geopolitical risk-on or risk-off keywords.

## Inputs

- `news_output: dict` from `NewsAgent`.
- Keyword config in `config/sources.yaml.macro_keywords` (risk_off / risk_on / neutral_watch).

## Outputs

Summary structure with:

- Recent risk-off / risk-on / neutral matches.
- Top categories (war, sanctions, rate cut, ETF, etc.).
- Notes for the report.

## Used by agents

- Report renders a macro / geopolitics block.
- Does **not** modify score directly.

## Common mistakes

- Treating "risk_off keyword" as automatic short signal — needs price confirmation.
- Ignoring this block — geopolitical shocks can override the entire setup.

## Future improvements

- Wire macro keywords into `MarketRegimeAgent` so a sudden risk-off cluster can force a regime downgrade.
- Add a calendar-aware module (CPI, FOMC, NFP).

## Related

- [[News_System_Overview]]
- [[Telegram_Integration]] (bridge `macro_pulse` is the parallel feed)

## Implemented status

- **Implemented** (keyword-based).
