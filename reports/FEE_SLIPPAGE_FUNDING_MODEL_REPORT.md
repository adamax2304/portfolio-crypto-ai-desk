# Fee / Slippage / Funding Model (PART 6)

**Date:** 2026-06-24. Config: `config/fee_profiles.yaml`. Module: `src/execution/fees.py`. PAPER ONLY.

## Profiles (configurable — NOT a universal/permanent rate)
| profile | maker | taker | note |
|---|---|---|---|
| bybit_default_futures | 0.02% | 0.055% | verify account rate |
| mexc_default_futures | 0.00% | 0.02% | varies by pair/account |
| mexc_conservative_api | 0.04% | 0.06% | conservative API tests |
| conservative | 0.04% | 0.08% | stress-test the edge |
| zero | 0 | 0 | no-cost baseline |
Default order type = taker. Each side (open AND close) is charged.

## Accounting
- open_fee = notional × rate; close_fee = notional × rate; fee_usdt = open+close.
- slippage per side: major 0.02% / liquid alt 0.05% / illiquid 0.10% (configurable; unknown symbols → liquid_alt, flagged).
- funding: included only if provided (else 0 + `funding_known=False`; future module reads the funding archive).
- `net_pnl_usdt = gross_pnl − fees − slippage − funding`.

Fields added: gross_pnl_usdt, fee_usdt, slippage_usdt, funding_usdt, net_pnl_usdt.

## Why this matters (measured)
Fees scale with **notional**, which is inversely proportional to stop distance — tight stops → huge notional → fees dwarf the $25 risk. Over the 586-trade backfill: fees+slippage = **$1770 (Bybit)** vs gross edge ~$2380 → fees eat ~74% of the gross edge. Under `conservative` fees the book is **net negative**. See PART 10.

## Verdict
`FEE_MODEL_READY_CONFIGURABLE`
