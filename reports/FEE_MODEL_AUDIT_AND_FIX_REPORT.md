# Fee Model Audit & Fix (PART 2)

**Date:** 2026-06-24.

## Bug found
`trade_costs` computed BOTH open and close fee on the ENTRY notional: `open_fee = close_fee = notional × rate`. The close fee should use the EXIT notional (qty × exit_price), which differs from entry notional by the trade's price move. Also: a single `order_type` for both sides; no source/last_verified metadata; no `fee_estimated` flag.

## Fix — `src/execution/fees.py` + `config/fee_profiles.yaml`
- `open_fee = entry_notional × entry_fee_rate`; `close_fee = exit_notional × exit_fee_rate`. Exit notional is passed from the sim (qty × implied exit price). If exit price is unknown → estimate from entry notional and flag `fee_estimated=true`.
- Per-side order types (`entry_order_type`, `exit_order_type`), maker/taker.
- Profiles carry `source_url` / `source_note` / `last_verified`: **bybit_non_vip_usdt_perp** (0.02% / 0.055%), **mexc_default_futures** (0.00% / 0.02%), **mexc_conservative_api**, **conservative_taker**, **custom_account_override** (edit-me), **zero**. Alias `bybit_default_futures -> bybit_non_vip_usdt_perp`.
- "Do not pretend a known account rate": rates have source notes + a manual override profile; nothing claims an account-pulled fee it doesn't have.
- New fields: fee_profile, entry_fee_rate, exit_fee_rate, entry_fee_usdt (open_fee), exit_fee_usdt (close_fee), slippage_usdt, funding_usdt, fee_estimated, fee_source.

## Effect on backfill
Bybit final equity shifted +2.94% -> **+2.72%** (close fee now on the larger exit notional for winners). `fee_estimated=0` for all backfilled trades (exit price implied from `paper_execution_r`).

## Verdict
`FEE_MODEL_AUDITED_AND_FIXED`
