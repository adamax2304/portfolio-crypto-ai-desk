# ETF Earnings False-Positive — Fix Report (PART 18)

**Date:** 2026-06-03
**Severity:** MEDIUM (data quality / signal noise)
**Scope:** `EarningsRiskAgent` + `StocksConfig` only.

## Problem

Every ETF in our universe (SPY, QQQ, IWM, DIA, SMH, XLK, XLF, XLE,
XLV, XLY) was emitted with `severity='unknown'` by the earnings-risk
agent. Downstream that became an "earnings UNKNOWN — undated event
risk" line in the intraday/swing reports and counted against the
candidate's evidence score even though ETFs don't report earnings.

## Root cause

`EarningsRiskAgent` called `yfinance.Ticker(sym).calendar` for every
symbol. ETFs return an empty calendar (no earnings date). The agent
interpreted "no calendar" as `severity='unknown'` ("we don't know if
there's an event in the next 7 days") instead of "not applicable"
("this instrument doesn't have earnings to begin with").

## Fix

### 1. `StocksConfig.is_etf(symbol)` — `src/stocks/configs/loader.py`

```python
@property
def etf_universe(self) -> set[str]:
    return set(self.indices) | {v for v in self.sector_etfs.values()}

def is_etf(self, symbol: str) -> bool:
    return (symbol or "").upper() in self.etf_universe
```

Drawn from the existing `stocks_universe.yaml` (`indices:` +
`sector_etfs:`); zero new config files, zero new YAML keys.

### 2. ETF gate at start of `EarningsRiskAgent.run()`

Before the future-earnings lookup attempts yfinance at all:

```python
if self.stocks_config.is_etf(up):
    risks.append(EarningsRisk(
        symbol=up,
        next_earnings_date=None, days_ahead=None,
        report_time="n/a",
        severity="not_applicable",
        note="ETF — does not report earnings",
        blocks_swing=False,
        intraday_high_risk=False,
    ))
    continue
```

### 3. Evidence line + thesis tag — `trade_idea_agent.py`

`_earnings_evidence_line()` recognises `severity == "not_applicable"`
and renders:

```
earnings: N/A (ETF — does not report earnings)
```

`_thesis()` excludes `"not_applicable"` from the "earnings UNKNOWN"
tag so the warm thesis stays clean for ETFs.

## Verification

Live `stocks-intraday-report` run (2026-06-03 ~15:15 ET):

```
### Idea #2 — B SMH long
  - earnings: N/A (ETF — does not report earnings)
### Idea #4 — B XLK long
  - earnings: N/A (ETF — does not report earnings)
### Idea #7 — B QQQ long
  - earnings: N/A (ETF — does not report earnings)

### Idea #N — C SMCI long
  - earnings: safe   ← single-name path preserved
```

9 new tests in `tests/test_stocks_etf_earnings.py`:

- All 4 indices recognised as ETFs.
- All 6 sector ETFs recognised as ETFs.
- 7 single-name stocks NOT classified as ETFs.
- `is_etf()` is case-insensitive.
- ETFs without calendar events → `severity=not_applicable`.
- Single-name stocks without calendar events → `severity=unknown`
  (regression guard — PART 12 logic preserved).
- ETF with a bogus calendar row injected → ETF gate still fires first
  and overrides.
- Evidence line renders "N/A" + "ETF" and does NOT say "UNKNOWN".
- Single-name with severity unknown still says "UNKNOWN".

## Safety contract — preserved

- ✅ No auto-trade.
- ✅ No global threshold change.
- ✅ No crypto-side change.
- ✅ No filter weakening (the ETF path was a false-positive WARNING,
  not a real filter; we removed noise, not a guard).
- ✅ No historical data deleted.

## Files touched

- `src/stocks/configs/loader.py` — `is_etf()`, `etf_universe`
- `src/stocks/agents/earnings_risk_agent.py` — ETF gate
- `src/stocks/agents/trade_idea_agent.py` — evidence line + thesis tag
- `tests/test_stocks_etf_earnings.py` — NEW (9 tests)
