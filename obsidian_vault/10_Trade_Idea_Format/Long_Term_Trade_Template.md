# Long-Term Trade Template (Recommended / Not enforced by desk)

Use for weeks-to-months positions. The desk does **not** have a long-term mode (see [[Long_Term_Mode]]), so this template is operator-only.

```
# Long-Term — {{symbol}} — {{date}}

## Thesis
- One-sentence thesis (mandatory):
- Why now:
- Why this symbol over alternatives:
- Time horizon: weeks / months / quarters
- Maximum drawdown I will accept: __ %
- Decisive exit signal (one line): __

## Macro / Sector
- Sector narrative status (from desk swing report)
- BTC dominance trend
- Real-rates / dollar context (external)
- ETF flow context (external)

## Structural entry
- Anchor exchange listing required (no MEXC-only)
- 1d trend (uptrend / accumulation)
- Weekly close > weekly EMA20 (or similar slow filter)
- Entry zone (multi-day):
- Stop level (weekly close):

## Position sizing
- Risk per position (% account): __ (typically 1–3%)
- Max position size (% account): __
- Average-in tranches: __ of N

## Cold storage plan
- Threshold above which I move to cold storage: __
- Custody venue:

## Re-evaluation cadence
- Weekly check on thesis
- Monthly deep review
- Quarterly position resize if thesis sustained

## Hard exits (immediate)
- Verified bearish catalyst (rugpull / SEC action / unlock disaster)
- Anchor exchange delisting
- Weekly close past stop
- Macro regime decisive flip
```

## Caveat

The desk's CLI does **not** generate this template. Build it manually from a swing report + your own thesis work.

## Related

- [[Long_Term_Mode]]
- [[Long_Term_Risk]]
- [[Trade_Idea_Template]]

## Implemented status

- **Recommended template** (operator-only).
