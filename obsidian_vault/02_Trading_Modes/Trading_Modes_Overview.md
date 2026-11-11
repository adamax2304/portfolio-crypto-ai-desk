# Trading Modes Overview

The desk supports **three trading modes** in code: `scalp`, `intraday`, `swing`. Each mode controls:

- Timeframes loaded.
- Volume / ATR / spread filters during universe ranking.
- Scoring multipliers per component (`scoring.yaml.mode_weights`).
- Setup timeframe used by `TechnicalSetupAgent`.
- Horizon language in the rendered report.

A fourth mode — **long-term** — is **recommended / not implemented**. See [[Long_Term_Mode]].

## Mode summary (from `config/universe.yaml.modes`)

| Mode | Timeframes | Primary TF | Horizon | CLI |
|---|---|---|---|---|
| scalp | 1m, 5m, 15m | 5m | 1–2 hours (rendered as "30m–2h") | `scalp-report --auto-universe` |
| intraday | 15m, 1h, 4h | 1h | 4–24 hours | `intraday-report` |
| swing | 1h, 4h, 1d | 4h | several days | `swing-report --auto-universe` |

## Scoring multipliers per mode (`scoring.yaml.mode_weights`)

| Mode | momentum | execution_quality | catalyst_news | narrative | market_regime |
|---|---|---|---|---|---|
| scalp | 1.20 | 1.20 | 0.80 | 0.75 | 1.00 |
| intraday | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| swing | 0.90 | 1.00 | 1.20 | 1.30 | 1.15 |

Intraday is the **balanced default**. Scalp leans on momentum + execution. Swing leans on narrative + catalyst + regime.

## Mode-specific universe filters (`config/universe.yaml`)

| Filter | scalp | intraday | swing |
|---|---|---|---|
| min_recent_candle_quote_volume | 20,000 | 75,000 | 150,000 |
| min_atr_percent | 0.12 | 0.35 | 0.80 |
| max_final_trade_ideas | 3 | 4 | 3 |

## How mode is chosen

- Explicit: `python -m src.cli intraday-report` / `scalp-report` / `swing-report`.
- Auto: `--auto-universe` flag triggers Stage-1 + Stage-2 ranking with the matching mode's filters before deep analysis.
- `Supervisor.ask` infers from natural language (Russian + English keywords): "intraday", "morning", "still valid", "утро", "интрадей" → intraday-report.

## Mode constraints in code

- `TradeIdeaAgent._mode_normalised = mode if mode in {scalp, intraday, swing} else "intraday"`. Anything else (e.g. "long_term") silently falls back to intraday — **so the desk cannot accidentally produce a "long_term" trade**.
- `WatchlistMonitor` reads `mode` from the latest trade-idea agent payload; it does not invent a mode.

## Related

- [[Scalp_Mode]]
- [[Intraday_Mode]]
- [[Swing_Mode]]
- [[Long_Term_Mode]] (Recommended)
- [[Other_Implemented_Modes]]
- [[Mode_Selection_Logic]]
- [[Mode_Specific_Timeframes]]
- [[Mode_Specific_Risk]]
- [[Mode_Specific_Scoring]]
- [[When_To_Use_Each_Mode]]

## Implemented status

- **Implemented** — three modes only. Any reference to a fourth or fifth mode in this vault is marked Recommended.
