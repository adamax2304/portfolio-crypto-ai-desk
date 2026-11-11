# Scalp Exit Variant Backtest (PART 4)

**Date:** 2026-06-15 · 12mo 5m, 15 liquid symbols, 139,014 trades each. Fees = 15bps round-trip (constant −166,245R drag). Sized R = raw × 0.5. Source: `SCALP_EXIT_VARIANTS_SUMMARY.json`.

## Results (all policies, net of fees)

| Policy | Description | n | WR | PF | avg R | raw netR | sized netR | MDD | avg MFE |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **A** | current (TP1=1ATR, ATR stop, 2h) | 139,014 | 43% | 0.63 | **−0.466** | −64,765 | −32,383 | −64,853 | 2.43 |
| **B** | TP1 at +0.5R | 139,014 | 8% | 0.01 | **−1.073** | −149,125 | −74,562 | −149,125 | 1.76 |
| **C** | partial 50% @ +0.5R, rest to TP1 | 139,014 | 26% | 0.23 | **−0.675** | −93,898 | −46,949 | −93,904 | 2.07 |
| **D** | TP1 at +0.7R | 139,014 | 20% | 0.04 | **−0.947** | −131,619 | −65,810 | −131,619 | 1.78 |
| **E** | breakeven after +0.6R | 139,014 | 28% | 0.51 | **−0.509** | −70,752 | −35,376 | −70,781 | 2.08 |
| **F** | 4h expiry | 139,014 | 43% | 0.63 | **−0.464** | −64,464 | −32,232 | −64,551 | 2.43 |
| **G** | trail after +0.7R | 139,014 | 51% | 0.93 | **−0.044** | −6,098 | −3,049 | −9,635 | 1.78 |

## Reads

1. **Every exit policy is net-negative after fees.** None reaches PF ≥ 1.0.
2. **G (trail after +0.7R) is the best by far** — PF 0.93, avg −0.044R, MDD only −9,635 vs −64,853 for A. Letting winners run is the only thing that nearly offsets the fee drag, but it still does not clear breakeven.
3. **B (TP1 @ +0.5R) is the WORST — avg −1.073R, PF 0.01.** This decisively kills the earlier "TP1@+0.5R looks promising" hypothesis, which came from a 25-signal 5m-fallback sample. On 139k real trades, cutting to +0.5R means the win is *smaller than the ~1.2R fee*, so almost every "win" is a net loss (WR collapses to 8%). **Tighter TPs are strictly worse** under realistic costs.
4. C and D (partial / +0.7R) are also worse than current. Earlier-TP policies all lose because the small target cannot cover the fee.
5. F (4h expiry) ≈ A — extending expiry does nothing; the issue is cost, not time.

## Winner-cut vs reduced-loss

- Earlier-TP policies (B/C/D) **cut winners** below the fee threshold → catastrophic.
- Trailing (G) **lets winners run** → recovers most of the gap but not all.
- Breakeven (E) reduces some losses but also caps the winners that would have run → mildly worse than A.

## Conclusion

No exit variant rescues scalp to net-positive on liquid majors at 15bps round-trip. The closest (trail, PF 0.93) confirms the gross edge exists but cannot beat the cost. **The lever is cost/instrument selection, not exit geometry.**
