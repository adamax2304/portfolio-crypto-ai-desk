# Stock Trade Idea Template

Every stock A/B-tier idea must include the fields below. The [src/stocks/agents/trade_idea_agent.py](../../src/stocks/agents/trade_idea_agent.py) orchestrator fills these from the upstream payloads. When writing ideas manually for the journal, copy this template.

## Required fields

```markdown
### {tier} {SYMBOL} {direction}

- **Asset class:** stocks
- **Mode:** intraday / swing / invest
- **Score:** 0–100
- **Confidence:** low / medium / high
- **Risk level:** low / medium / high
- **Timeframe:** e.g. 15m/1h (intraday), 1h/1d (swing), 1d/1wk (invest)

**Thesis** — single-sentence rationale, plus regime + sector context.

**Index context** — SPY/QQQ direction at evaluation time.
**Sector context** — sector ETF status (strong / mixed / weak).
**Company news / catalyst** — if any; cite source.
**Earnings risk** — severity (safe / this_week / next_session / active).

**Technical setup**
- Trend: uptrend / downtrend / range
- Last close: ...
- ATR: ...
- Prev day high / low: ...
- VWAP (intraday only): ...

**Entry plan** — zone {low}–{high}, or trigger {price}.
**Invalidation** — close beyond {price}.
**Targets** — TP1: {price}, TP2: {price}, TP3: {price}.
**Expected RR to TP1** — must be ≥ 1.5 for A/B.

**Counter-thesis** — what would invalidate the trade besides the stop.
**Conditions to avoid** — do-not-enter triggers (gap > 2 ATR, SPY breakdown, etc.).
**What to monitor** — index direction, sector ETF, relative volume.
**Caps applied** — if any (e.g. earnings active, data partial).
**Data confidence** — low / medium / high.
**Data sources used** — yfinance, rss_news, manual_earnings_calendar.
```

## What must be true to ship an A-tier idea

1. Score ≥ 80 post-caps.
2. Clean invalidation level.
3. RR to TP1 ≥ 1.5.
4. No `blocks` (no missing invalidation, no earnings_today for swing, etc.).
5. Index AND sector agree with direction (or symbol is leader-grade RS overriding the regime).
6. Verified catalyst (if news-driven).

## What disqualifies B → A promotion

- Missing one of: clean invalidation, index agreement, sector agreement.
- Earnings within the mode's blocking window.
- Data partial cap (`max_score_if_data_partial`) firing.
