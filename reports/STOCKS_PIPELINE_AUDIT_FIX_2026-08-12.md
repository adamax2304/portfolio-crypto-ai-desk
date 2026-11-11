# Stocks Pipeline Audit Fix - 2026-08-12

Scope: paper/read-model/shadow diagnostics only. No live routing, no active
paper ledger execution, no `final_r` rewrite.

## Fixed

1. Pre-US actionability auditability
   - Added `stocks_preus_actionability_history`.
   - The current `stocks_preus_actionability` row may expire and become
     `BLOCKED`, but the point-in-time morning decision is now preserved.
   - This prevents later audits from looking contradictory.

2. False `PREUS_SOURCE_CHANGED_AFTER_REVIEW`
   - `source_decision_fingerprint()` now hashes only decision-relevant content:
     symbol, direction, setup type, entry/stop/target geometry.
   - It no longer rejects a valid plan just because `tier`, `score`, `status`,
     or `updated_at` changed after review.
   - Regression test covers score/tier recompute after review.

3. MEXC stock paper order snapshots
   - Staged and rejected stock orders now persist the source signal snapshot:
     geometry, raw actionability context, catalyst metadata, entry profile,
     confirmation, and reviewed/current fingerprints.
   - This makes post-trade review explainable without relying on a mutable
     `proposed_signals` row.

4. Stocks Position Framework lifecycle consistency
   - Superseded duplicate candidates now get an explicit terminal outcome:
     `status=no_entry`, `close_reason=superseded_duplicate`, NULL PnL.
   - No fake fills or fake profitability are created.
   - Real DB now has 15 candidates / 15 outcomes / 0 missing outcomes.

5. Catalyst label refresh latency
   - Added runtime/migration index `idx_news_canonical_effective_linkage`
     on `news_canonical_events(effective_at, linkage_allowed)`.
   - Added runtime index `idx_news_items_asset_published`.
   - Real refresh improved from timeout at >124s to 3.03s for 1207 scanned
     signals.

6. Fast-news latency
   - Removed slow `GlobeNewswire (Stocks)` from the 2-minute fast RSS lane.
   - It remains enabled in normal source health/RSS coverage.
   - Fast-news refresh changed from partial/timeout around 21.8s to OK around
     6.4s on the verification run.

## Current Observations

- MEXC stock-futures paper is active: 15 filled positions, 14 closed, 1 open.
- Closed MEXC stock paper result: +7.114R, estimated +$382.80 from
  `paper_execution_r * risk_usdt`.
- Catalyst RS shadow is still not promotable on evidence; keep in shadow/paper
  test only until sample and PF improve.
- News entity resolver health is OK: 99-100% resolved, only 1 symbol-tagged row
  unresolved and newer than one scheduler cycle.
- News source health has one remaining visible issue:
  `GlobeNewswire (Stocks)` latest transport timeout and no fresh 24h rows.
  This is now isolated from fast-news latency, but it should remain visible as
  a primary-source warning.

## Verification

- `python -m pytest tests\test_stocks_preus_review.py tests\stocks\test_mexc_stock_futures_paper.py -q`
  - 49 passed
- Extended stocks/pre-US regression
  - 113 passed
- Position Framework regression
  - 40 passed
- News/catalyst regression
  - 17 passed
- Combined verification
  - 164 passed
- Real DB:
  - `signal_catalyst_labels` max `computed_at` refreshed to 2026-08-12T17:27:29+00:00.
  - `stocks_preus_actionability_history` created and populated.
  - `stocks_position_candidates` orphan outcomes: 0.
