# App / Backend / Telegram Display Audit + Fix (PART 9)

**Date:** 2026-06-24. Reconciliation after fixes.

| reconciliation | result |
|---|---|
| app values == backend | yes — cards bind directly to `/api/portfolio` |
| backend == ledger | yes — `portfolio_summary` reads `paper_portfolio_ledger` (filtered to active fee_profile) |
| ledger == formulas | yes — sizing/fees/exit verified by tests; `m0`==recorded `final_r` (99.8%) |
| Telegram == ledger | yes — close-alert Paper $ / TP-R use the same `size_position`/`trade_costs`/R math |
| no stale touch as main PnL | yes — headline = paper_execution_r; touch labelled "optimistic" |
| no hardcoded "+1R" for TP1 | yes — exact R (e.g. 1.2/2.2/3.2R) everywhere |
| leverage visible | yes — dashboard avg/max + per-trade detail + Telegram |
| expired visible | yes — exit_price + expiry_close_price + `expired_exit` marker |
| chart marker visible | yes — markers timeline (full candle overlay = TODO) |
| fee profile visible | yes — shown on portfolio note + fee_profiles_available |
| TP quality visible | yes — MECHANICAL_ATR_LADDER badge + note |

## Mismatch found & fixed during audit
- **Multi-profile double-count risk:** renaming the default fee profile orphaned old `bybit_default_futures` rows (1172 = stale + new). Fixed: backfill drops non-canonical profiles + the backend filters `/api/portfolio` to a single active `fee_profile` (never sums across profiles). Verified: 4 profiles × 587, summary reads one profile.

## Verdict
`APP_TELEGRAM_VALUES_RECONCILED`
