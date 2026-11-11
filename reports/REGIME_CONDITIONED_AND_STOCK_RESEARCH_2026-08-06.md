# Regime-Conditioned Crypto and New Stocks Research

Date: 2026-08-06

## Executive verdict

- **Crypto Regime-Conditioned Relative Trend Reclaim v2:** promising historical
  candidate, running in isolated forward Shadow. It is not Paper/Live eligible.
- **Stocks long PEAD:** rejected after failing the frozen calendar-2024 validation.
- **Stocks negative PEAD short:** rejected in development; every profile lost money.
- **Stocks Residual Momentum Rotation v1:** best new stock candidate. It remained
  profitable in development, calendar-2024 validation and the 2025-2026 known
  audit, but is still underpowered and concentrated. It is running in isolated
  monthly forward Shadow and is not Paper/Live eligible.
- No production, Paper, Live, Telegram, `proposed_signals`, `signal_outcomes`,
  `final_r` or active ledger path was changed.

## Crypto: implemented hypothesis

The strategy reuses the lab's deterministic trend-reclaim mechanics and adds four
causal regime conditions:

1. BTC 4h EMA trend agrees with trade direction.
2. BTC 4h ADX and normalized EMA slope exceed fixed thresholds.
3. Symbol 24h return exceeds BTC by the configured relative-strength threshold.
4. Symbol 4h ATR percentage is not below its causal 30-day median regime.

Entry remains the next closed M15 reclaim after the first H1 FVG retest. Stop,
targets (1.3/2.3/3.6R), 72h maximum hold and Model F protection are deterministic.
Fresh funding/OI can veto a trade; missing derivatives data never confirms one.
The selected research profile is the simplest v2 combination: BTC ADX 10,
BTC slope 0.05 ATR, 24h RS +0.5%, volatility ratio 0.65.

### Crypto results

| Evidence stage | Trades | Net USD | PF | Win rate | Max DD |
|---|---:|---:|---:|---:|---:|
| Development | 58 | +$172.83 | 1.307 | 48.3% | 4.88R |
| Frozen validation, 2025-02 to 2025-08 | 31 | +$220.11 | 2.163 | 58.1% | 3.72R |
| Known audit, 2025-08 to 2026-08 | 49 | +$556.27 | 3.621 | 69.4% | 3.12R |

The original pooled report printed 9.36R because parallel worker-arrival order was
used for drawdown. The generator and regression test now sort by actual exit time;
the corrected chronological value is 4.88R. PnL, PF, fills and verdict are unchanged.

Development had only 58 trades and 47 unique days; the pre-registered machine
verdict was `REJECT`. Validation was run only after freezing the profile. The known
audit is explicitly not sealed evidence.

Direction is the main caveat:

- validation long: 20 trades, +$41.29, PF 1.235;
- validation short: 11 trades, +$178.83, PF 14.37;
- known-audit long: 15 trades, -$81.75, PF 0.38;
- known-audit short: 34 trades, +$638.02, PF 8.93.

Disabling long now would be post-hoc tuning, so forward Shadow records both sides
and reports them separately.

### Crypto execution stress

At 20 bps slippage, development becomes -$7.19/PF 0.989, while validation remains
+$124.92/PF 1.533 and the known audit +$376.04/PF 2.355. At 25 bps, validation is
only +$29.72/PF 1.106; the known audit remains +$195.81/PF 1.546. Long trades are
the fragile component. Full table: `artifacts/CRYPTO_FROZEN_PROFILE_STRESS.md`.

### Crypto forward evidence

`forward_shadow.py` is active, evaluates 45 symbols on closed 15-minute boundaries,
records source timestamps and MEXC quote parity, and writes only to the lab database.
The first completed boundary evaluated 45/45 symbols with no transport errors and
correctly recorded no synthetic trade when no setup existed.

Review eligibility requires at least 60 clean closed forward trades, 42 days,
positive net USD, PF >=1.25, DD <=10R, both directions, p90 decision latency <=60s
and acceptable observed MEXC execution. Passing only changes the verdict to
`REVIEW_ONLY`; it never promotes automatically.

## Stocks: failed hypotheses

### Long PEAD

The frozen 5-session profile looked strong in development (82 trades, +$606.98,
PF 2.14), but failed untouched calendar 2024: 24 trades, -$66.12, PF 0.60, WR
37.5%. It is rejected and was not retuned after validation.

### Negative PEAD short

All 16 development profiles lost money. The broadest 5-session profile had 23
trades, -$106.66 and PF 0.585. No profile was frozen and validation was not opened.

## Stocks: Residual Momentum Rotation v1

This is a monthly portfolio strategy, not another breakout/retest:

1. At completed month-end, rank liquid stocks by 6/12-month return minus SPY.
2. Test the academic one-month skip as a pre-registered dimension.
3. Require positive residual momentum, stock above SMA200 and SPY above SMA200.
4. Enter the top 3/5 at the next session open, never at the ranking close.
5. Risk $25 before the 1.25 overnight-gap multiplier; stop at 3/4.5 ATR.
6. Stop wins daily-bar ambiguity; otherwise exit after 21 sessions.
7. Charge 6 bps taker fee and 15 bps slippage per side separately.

The best robust research candidate was frozen as `UNDERPOWERED_RESEARCH_ONLY`:
6-month formation, no one-month skip, top 3, 3 ATR stop.

| Evidence stage | Trades | Net USD | PF | WR | Mean excess vs SPY | DD |
|---|---:|---:|---:|---:|---:|---:|
| Development 2020-2023 | 70 | +$309.25 | 1.528 | 51.4% | +2.44% | 7.27R |
| Validation 2024 | 18 | +$204.36 | 2.872 | 66.7% | +3.50% | 1.71R |
| Known audit 2025-2026 | 17 | +$154.56 | 2.360 | 64.7% | +2.76% | 1.69R |

All four development folds were positive and the weakest fold PF was 1.036.
However, the candidate had only 70 development trades, day-cluster bootstrap
p=0.114 and multiple-test FDR q=0.802. It therefore did not pass the machine gate.
Validation is also concentrated: PLTR produced $156 of the $204 result. The known
audit depends mainly on AVGO/LRCX/AMAT. At 25 bps slippage the signs remain positive
(development +$274.81/PF 1.456; validation +$193.34/PF 2.706; audit
+$146.45/PF 2.257), so costs are not the main weakness.

The forward scanner has a separate immutable ledger. It calculates ranks only
after the final RTH month-end bar, does not require or know the next open at
decision time, and resolves entry/outcome later. A dry-run caught and fixed an
initial look-ahead requirement before any evidence was persisted. The current
mid-month forced smoke test fetched 69/69 symbols without errors and identified
AMD/MRVL/MU as the top three, but it was not persisted and is not evidence.

Forward review requires 60 clean closes and 126 forward days. The monthly cadence
means this will take substantially longer than crypto; that is intrinsic to the
hypothesis, not a scheduler fault.

## Data and limitations

- Crypto: 45 symbols, 1,095 calendar days, 135 OHLCV series (M15/H1/H4), no
  detected internal OHLCV gaps. Funding exists for 45 symbols and OI for 43;
  historical depth is uneven and FET/TON OI is missing.
- Stocks: 69 daily series from 2019 and current-universe constituents. This creates
  survivorship bias. Yahoo earnings timestamps and surprise data are historical
  reconstruction, not point-in-time vendor snapshots.
- Stock historical execution uses adjusted Yahoo OHLCV with conservative MEXC-like
  costs; it does not claim historical MEXC stock-contract quote parity.
- A backtest can reject a strategy and estimate historical robustness. It cannot
  prove future edge. Only immutable forward observations remove reconstruction,
  selection and latency ambiguity.

## Recommendation

1. Keep both candidates Shadow-only and freeze all parameters.
2. Do not split crypto to short-only until the predeclared forward report confirms
   that direction asymmetry; report the split every cycle.
3. Collect crypto forward evidence until at least 60 clean closes/42 days.
4. Collect stock momentum evidence through at least six month-end decisions and
   the stricter 60-close/126-day gate. Add point-in-time historical constituents
   before treating its backtest as institutional-grade evidence.
5. Revisit Paper only through manual review after the gates pass. No auto-promotion.

## Research basis

- Chan, Jegadeesh and Lakonishok, *Momentum Strategies*, NBER Working Paper 5375:
  https://www.nber.org/papers/w5375
- Blitz, Huij and Martens, *Residual Momentum*, Journal of Empirical Finance:
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2319861
- Ehsani and Linnainmaa's later critique is also relevant: residual momentum can
  embed beta bets and firm-specific momentum weakened after 2002:
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4059632
