# Catalyst / Narrative — 12h Audit (READ-ONLY)

**Window:** last ~14h. Source: `news_items` (DB) + `data/catalysts/2026-06-04/*.jsonl`.

## Volumes
- **news_items (14h):** 1,101 — crypto 499 / stocks 602. Healthy ingest.
- **catalyst_events.jsonl (today):** 1,424 rows (629 unique per report dedup).
- **narrative_baskets.jsonl:** 3 baskets.
- **events table (earnings, 14h):** 17.
- Telegram collector: Running (PID 26656); feeding the bridge.

## Importance scoring — WORKS ✅
- All 1,424 events carry **non-zero importance** (min 0.331, max 0.82, avg 0.44).
- Top events ranked sensibly:
  - 0.82 — "US Treasury to establish Bitcoin Reserve, urges CLARITY Act" → BTC
  - 0.785 — "Broadcom outlines $29.4B Q3 revenue outlook driven by $16B AI" → AVGO
  - 0.748 — "Bessent backs summer push for Clarity Act" → BTC
- Distribution is reasonable (no all-zero / all-equal degeneracy).

## Symbol mapping — STILL THE WEAK SPOT ⚠️
- **Mapped to a symbol: 339 / 1,424 = 24%** (76% unmapped). Opus independently
  reported the same (~22%). Useful for the top mega-narratives (BTC, AVGO,
  Broadcom, Bitcoin reserve) but the long tail is symbol-less.
- Minor schema quirk: stock catalysts inherit the crypto `/USDT` suffix
  (e.g. `AVGO/USDT`) — cosmetic, not blocking; the alias matched Broadcom→AVGO.
- `catalyst_type`/`category` populated per-row but the quick scan key was
  `category` (None) — categories live under `catalyst_type`; not a data gap.

## Did it catch the important narratives? — YES
- **BTC Treasury reserve / CLARITY Act** (top importance) — caught.
- **AVGO post-earnings** (Broadcom AI outlook) — caught, and Opus used it to
  flag the stale AVGO A-tier long.
- **BTC risk-off** (ETF outflow streak, $1.5B liquidations, sub-$63k) — caught
  in macro/news headlines and reflected in regime.

## Social-only / weak-source handling — OK
- Catalyst rows carry `source_quality`, `confidence`, `sell_the_news_risk`,
  `contradicts_internal_signal` flags. Opus reviews treat unmapped / social-only
  catalysts as "context, not final decision" (source discipline holding).

## Did catalysts reach reports + packets? — YES
- Reports include "Structured Catalyst / Narrative (auto-collected)" section;
  LLM packets reference `catalyst_events.jsonl` + narrative baskets; Opus
  reviews consume the JSONL directly.

## Verdict
Narrative/importance layer is **useful now** for the high-signal mega-narratives
and feeds Opus well. The **one persistent weakness is symbol mapping (24%)** —
worth improving for the long tail, but it is **context-only** and does not gate
trades, so it is **P2 (not urgent)**. No missed *obvious* narrative this window.

### TODO (evidence, do not implement yet)
- `TODO-catalyst-symbol-mapping`: raise catalyst→symbol coverage above ~24%
  (extend alias lists / fuzzy company-name match). Evidence: 1085/1424 unmapped.
- `TODO-catalyst-stock-suffix`: stock catalysts tagged `AVGO/USDT` — strip the
  crypto `/USDT` suffix for `asset_class=stocks` rows (cosmetic).
