# Intraday Measurement Hardening

Date: 2026-07-13

Scope: paper, shadow, accounting read-models, and diagnostics only. Live remains locked.

## Applied

- Added immutable, lookahead-safe pre-entry mode capture. The crypto quality overlay and crypto B shadow branch no longer use the post-entry `signal_entry_mode` classifier.
- Added the `preentry_v2` forward boundary. Crypto B rows produced with the legacy post-entry source are preserved as `historical_backfill`, never forward evidence.
- Added immutable point-in-time overlay decision snapshots for future paper alerts.
- Made `late_shadow` and other non-actionable alert statuses exclude a trade from the active paper ledger for every asset class.
- Enforced `HALF_SIZE <= 0.5` in actionability reconstruction, even if an old payload is inconsistent.
- Captured entry-latency diagnostics at the actual entry transition. Future snapshots cannot be overwritten by rolling-cache refreshes; historical rows remain explicitly labelled `backfill_refresh`.
- Corrected protection-evidence coverage to use only the clean, closed cohort that also supplies USD PnL and PF.
- Scheduled pre-entry classification every market cycle and retained an inline alert-path fallback.

## Production-State Checks

- `late_shadow` rows in active `bybit_non_vip_usdt_perp` ledger: 0.
- `HALF_SIZE` active rows with size weight above 0.5: 0.
- Legacy crypto B rows remaining in the forward window: 0.
- Crypto B `preentry_v2` forward rows: 0 at the time of the change. This is expected: the fair forward sample begins after activation and must accumulate naturally.
- Point-in-time snapshot table exists. It has no historical rows by design; it will append on the next paper-entry decision.
- Entry-transition frozen latency rows: 0 at the time of the change. They will begin on the next real waiting-to-triggered transition.

## Verification

- 247 targeted regression tests passed.
- All 11 changed Python modules compiled successfully.
- A controlled calibration refresh left `proposed_signals`, `signal_outcomes`, and `SUM(final_r)` unchanged.
- The full repository test run exceeded the 124-second execution limit without an observed assertion failure, so it is intentionally not claimed as a complete green run.

## Interpretation

Do not use the old crypto B forward statistics for promotion, sizing, or profitability claims. The next meaningful crypto B result is the `preentry_v2` cohort only, with entries captured under the new scheduler and alert-path provenance.
