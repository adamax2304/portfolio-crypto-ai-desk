# Catalyst Integrity — Daily Summary (PART 7)

**As of:** 2026-11-11T20:21:42.567798+00:00 · **Status:** `ok` · **Confidence:** high · **Warning:** False

## Counts
- High-importance (>=1.0) symbol-tagged news_items (all-time): **83443**
- Catalyst symbols in last 24h: **100** — AAPL, AAVE, ABBV, ABNB, ADBE, AMAT, AMD, AMGN, AMZN, APP, AVGO, BA, BAC, BIIB, BKNG, BLK, BNB, BTC, BX, CMCSA, COIN, COP, COST, CRM, CRV …
- Mapped into today's catalyst_events: 128
- **Raw-news symbols outside the narrower catalyst artifact scope:** 1 — DOGE
- **No-catalyst basket symbols with direct news hits (regression signature):** none

## Warnings
- none — catalyst mapping consistent

## Interpretation
- `direct_news_items_checked` is True — the no-catalyst label is only applied after a direct `news_items` lookup (the ASTER fix).
- A non-empty *regression signature* list means a momentum/no-catalyst basket still contains a symbol that has a direct high-importance news hit. If this is from an on-disk artifact written before the fix, re-run the catalyst-scan to regenerate `narrative_baskets.jsonl` with the fixed builder; if it persists after a fresh scan, the fix has regressed — investigate.
- Raw-news symbols not emitted into `catalyst_events` are reported as coverage diagnostics only: that artifact intentionally excludes diffuse/non-actionable headlines. They are not a mapping failure unless the regression signature is also present.
- This monitor never promotes a symbol to actionable; ASTER-like names remain catalyst-backed watch-on-pullback.