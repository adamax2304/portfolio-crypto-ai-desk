# Post-Weekend Mode Comparison (72h, A/B)

| asset / mode | n | PF | totalR | avgR | WR | common failure | verdict |
|---|---|---|---|---|---|---|---|
| crypto **intraday** | 15 | 2.67 | **+10R** | +0.83 | 50% | normal chop | **continue** |
| crypto **swing** | 3 | ∞ | +9R | +3.0 | 100% | — | continue (need more data, n3) |
| crypto **scalp** | 28 | **0.25** | **−3R** | −0.17 | 20% | expire/no-fill + faded entries | **review / lowest priority** |
| stocks **intraday** | 30 | 3.50 | **+10R** | +0.46 | 71% | A-tier giveback | **continue** |
| stocks **swing** (watchlist-only) | 14* | 0.00 | −4R | −0.29 | 0% | faded into pullback | **stay paused** |
| stocks **invest** | 9 | — | 0R | — | — | n/a (6 waiting) | **need more data** |

*stocks swing n=14 are all **pre-fix** residual; no new swing A/B are produced
(pause active).

## Answers
- **Continue:** crypto **intraday**, crypto **swing** (small but clean), crypto
  **shorts** (cross-mode +16R), stocks **intraday** (+10R PF 3.5 WR 71%).
- **Stay paused:** stocks **swing** — fresh evidence (0W/4L residual) reconfirms
  the pause; keep watchlist-only.
- **Need more data:** crypto **swing** (n3), stocks **invest** (n9, 6 waiting).
- **Need fix / review:** crypto **scalp** (PF 0.25, −3R, 13/28 expired) — the
  no-fill/expire rate is the issue; **scalp quality/entry, not stops**. Also the
  scalp *report* timeout (infra). Both = TODO, no strategy change without
  approval.
- **Not worth trading now:** nothing to hard-stop beyond the already-paused
  stocks swing. Scalp is the weakest active mode but still small negative, not a
  capital sink — flag for review, don't pause yet.

## Cross-cutting
- **Shorts > longs** in both classes this weekend (risk-off tape): crypto shorts
  +16R vs longs 0R; stocks shorts +9R vs longs −3R.
- **Catalyst-backed > no-catalyst** (crypto +9R PF 5.5 vs +7R PF 1.88).
- **A-tier < B-tier** (stocks A −2R PF 0.33 vs B +8R PF 2.60) — recurring.
