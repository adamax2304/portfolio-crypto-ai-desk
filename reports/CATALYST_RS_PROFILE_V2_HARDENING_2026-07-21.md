# Catalyst RS Shadow profile v2 hardening

Generated: 2026-07-21

## Scope and invariants

- Strategy remains isolated Shadow-only: `stocks_catalyst_rs_v1` / `shadow_catalyst_rs`.
- New rules use `stocks_catalyst_rs_profile_v2`; v1 rows are retained and cannot be overwritten.
- Candidate IDs include the profile ID.
- No Paper, live, `proposed_signals`, `signal_outcomes`, `final_r`, or paper-ledger write path was added.
- The strict source/5% impulse/1.5x RVOL cohort is the only promotion evidence. Exploratory results are measurement-only.

## Implemented changes

1. Added an auditable upstream funnel over all point-in-time canonical stock events, including explicit pre-trade rejection counts.
2. Added local Shadow-only taxonomy recovery for product launches, partnerships, contract awards and strategic investments, plus a correction for false management-change labels.
3. Added conservative subject-role resolution. Exact title-leading tickers and configured issuer aliases are accepted; customers, competitors and secondary partners after the event anchor are not treated as the traded issuer.
4. Added source cohorts: trusted/reputable, corroborated secondary, exploratory factual secondary, and untrusted. Speculative or title-only secondary stories remain blocked.
5. Added an exploratory observation profile: impulse 2.0%, RVOL 1.25x, RS vs SPY 0.10%, RS vs sector 0.05%. Original strict thresholds remain 5.0%, 1.5x, 0.25%, and 0.15%.
6. Added sector benchmark overrides for AI hardware, AI software and crypto-equity buckets and exposed missing benchmark rows in the funnel.
7. Fixed point-in-time coverage. A current `SESSION_WARMUP` can no longer mark a historical trade dirty; a real late first bar after an RTH catalyst is still rejected as dirty.
8. Fixed readiness reporting: it now counts cluster-primary, linkage-allowed events instead of presenting every raw canonical row as a usable catalyst.
9. Added historical-backfill metrics separately from forward evidence and split reports by strict/exploratory cohort.
10. Wired Catalyst RS into the RTH stocks monitor after data/coverage refresh. It now evaluates every 10 minutes during the monitor session, in addition to the normal scheduler step.

## Real database verification

- v2 activation: `2026-07-21T13:55:17.206013+00:00`.
- Historical v2 candidates: 15; one clean closed exploratory simulation, net USD `-15.6357`. This is backfill and cannot count as forward proof.
- First post-activation candidate: NFLX M&A, exploratory secondary. It was evaluated and rejected at `IMPULSE_BELOW_THRESHOLD` because the observed impulse was 0.62% versus the 2.0% exploratory minimum.
- Current 24h readiness: 914 raw canonical stock rows, but only 2 linked cluster-primary events (1 reputable, 1 secondary). The old display materially overstated usable catalyst supply.
- Working monitor persisted a fresh profile-v2 evaluation after restart.
- Removed two orphan duplicate stocks-monitor processes; one scheduler-owned RTH monitor remains active.
- First live forward observation is present: NFLX, exploratory M&A candidate, rejected at 0.62% impulse versus the 2.0% minimum. This proves the lane is receiving new events without admitting sub-threshold noise.

## Tests

- Focused Catalyst/variant/monitor batches: 89 passed.
- News/entity/gate/stocks-agent batch: 219 passed.
- `tests/stocks`: 133 passed.
- Telegram transport isolation suite: 5 passed.
- Scheduler dry-run: 79 steps; Catalyst RS and intraday variants CLI surfaces valid; no automatic LLM invocation.

## Current interpretation

The lane is operational and more observable, but it has no proven forward edge yet. Frequency was increased without admitting sub-2% noise or allowing exploratory trades to promote the strategy. Continue collecting forward candidates; do not move this lane to Paper until the existing minimum sample and manual-review gates are met.
