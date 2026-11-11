# Post-Weekend Performance Audit (72h, deduped A/B)

**As of:** 2026-06-07 (Sun) · resolved = entry_triggered & outcome closed.
Confidence noted per bucket (n).

## Headline
| Class | n | trig | W/L/flat | PF | avgR | **totalR** | WR | confidence |
|---|---|---|---|---|---|---|---|---|
| **Crypto A/B** | 46 | 33 | 10/10/13 | **2.60** | +0.485 | **+16R** | 50% | medium (n=33 resolved) |
| **Stocks A/B** | 53 | 39 | 10/8/21 | **1.75** | +0.154 | **+6R** | 56% | medium |

**Paper trading is net positive and improved vs the 48h audit** (then: crypto
+6R, stocks −15R; now crypto **+16R**, stocks **+6R**).

## Crypto detail
| Cut | n | W/L | PF | totalR | WR | read |
|---|---|---|---|---|---|---|
| **shorts** | 34 | 8/6 | **3.67** | **+16R** | 57% | the engine (risk-off tape) |
| longs | 12 | 2/4 | 1.00 | 0R | 33% | flat (chop) |
| **intraday** | 15 | 6/6 | 2.67 | **+10R** | 50% | strong |
| **swing** | 3 | 3/0 | ∞ | +9R | 100% | great but tiny n |
| **scalp** | 28 | 1/4 | **0.25** | **−3R** | 20% | **laggard** (13 of 28 expired/no-fill) |
| catalyst-backed | 15 | 4/2 | **5.50** | +9R | 67% | catalyst edge persists |
| no-catalyst | 31 | 6/8 | 1.88 | +7R | 43% | |
| squeeze-capped shorts | 0 | — | — | — | — | none qualified this window |
- Best symbols: short side broadly (ETH/NEAR/FET-class trend shorts), catalyst
  names. Worst: scalp alt longs/shorts that expired or chopped.
- **Active crypto signals:** 5 open.
- A-tier crypto: **0** produced this window (funnel stayed B-tier in risk-off).

## Stocks detail
| Cut | n | W/L | PF | totalR | WR | read |
|---|---|---|---|---|---|---|
| **intraday** | 30 | 10/4 | **3.50** | **+10R** | 71% | best stock mode |
| **shorts** | 12 | 6/0 | ∞ | +9R | 100% | shorts working (small) |
| **B-tier** | 41 | 9/5 | 2.60 | +8R | 64% | healthy |
| **A-tier** | 12 | 1/3 | **0.33** | **−2R** | 25% | **overpromotion persists** |
| longs | 41 | 4/8 | 0.62 | −3R | 33% | weak in this tape |
| **swing** (pre-fix residual) | 14 | 0/4 | 0.00 | **−4R** | 0% | confirms pause was right |
| invest | 9 | 0/0 | — | 0R | — | 6 waiting, no data |
| ETF | 17 | 4/4 | 1.50 | +2R | 50% | |
| single | 36 | 6/4 | 2.00 | +4R | 60% | |
- **Swing confirmed non-actionable** — the only swing closes are the pre-fix
  residual (0W/4L); no new swing A/B. Pause is working and justified.
- **A-tier still underperforms B-tier** (PF 0.33 vs 2.60) — the known
  overpromotion issue (TODO, needs approval to touch scoring).
- C-tier (excluded from headline): −12R PF 0.25 — correctly non-actionable.
- **Active stocks signals:** 264 (mostly waiting/closed-market watchlist).
- Gate behavior: market-closed 48×, legal 9×, B→C 34×, swing-pause 2× — all
  firing.

## Confidence
Crypto +16R over 33 resolved = **medium** confidence (shorts + catalyst are
repeatable edges seen across multiple audits). Stocks +6R = **medium**, driven
by intraday; swing/invest samples too small or paused. A-tier negative is a
**recurring** signal (medium-high confidence it's real).
