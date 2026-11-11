# Production News Entity/Narrative Resolution — Deliverable

Date: 2026-07-08 · Scope: **production read-model / enrichment / scoring-inputs**. NOT live trading
(live LOCKED). No `final_r` / `signal_outcomes` rewrite. No auto-promote/auto-trade from a news item.
Additive only: `news_items` enrichment (union) + `proposed_signals.news_supported`/`telegram_supported`
0→1 via the existing refresh.

**The core insight** was right — the problem wasn't "add more sources", it was **no real entity/narrative
resolution layer before scoring**. The news existed; the system didn't understand what it was about.
Diagnosis confirmed on the DB: 72h match-rate 17.6% (crypto 21.8% / stocks 15.4%); 91 stock signals with
direct stock news still stamped `news_supported=0` (root cause: `direct_news_for_signal` was crypto-only).

---

## What was built

1. **`src/news/entity_resolver.py`** — the resolver. Reads title + body/summary (defensive, future-proof)
   + **url slug** + structured SEC/DefiLlama fields; runs the boundary/case-safe crypto **and** stock
   matchers **cross-asset**; adds a crypto exchange-**listing parser** (`MEXC to list XYZUSDT` → XYZ/USDT
   tradable, else `untracked_entity`) and **macro/geopolitics** event tagging (never forces a symbol).
   Emits per row: `detected_symbols`, `detected_entities`, `detected_narratives`, `event_tags`,
   `entity_match_confidence/reason/source`, `asset_impact_scope`, `tradability_status`,
   `source_quality_hint`. Common-word safety preserved ("near"≠NEAR, "one"≠ONE, "link"≠LINK).
2. **Additive migration** — 9 nullable columns on `news_items` (idempotent `ALTER`, no drop, union-only on
   `detected_symbols_json`).
3. **Expanded alias dictionaries** — crypto (ENA/PENGU/JUP/BONK/PYTH/JTO/STRK) + stocks
   (INTC/HOOD/RIOT/MARA/CLSK/HUT/CIFR/WULF/CRCL) — the exact gaps behind the untagged `$HOOD` / "Intel" /
   crypto-miner headlines.
4. **CLI** — `news-entity-resolve` (--hours/--limit/--asset-class/--dry-run/--min-confidence, union-only) +
   `news-entity-audit` → `reports/NEWS_ENTITY_RESOLUTION_AUDIT.md`.
5. **Catalyst fixes** —
   * `direct_news_for_signal(..., asset_class=...)`: stocks now query stock news (+ cross-asset crypto-feed
     rows naming the bare ticker); crypto behaviour identical. Fixes the 91.
   * `catalysts/collector` fallback is **asset-aware** (stocks matcher for stock rows, crypto for crypto,
     no forced symbol for macro) over **combined text** (title + url slug), not crypto-title-only.
6. **Time-window loading** — `SQLiteStore.load_news_window(hours, limit, asset_class)` (robust mixed-format
   timestamp parse). Replaced the limit-only tails: supervisor 100→**72h/3000**, watchlist 50→**48h/2000**,
   CompanyNewsAgent 200→**72h** (+ new per-symbol cap of 8), position-framework 200→**90d symbol window**.
7. **Scheduler** — `news-entity-resolve` step runs **before** catalyst-scan / integrity / label-refresh
   (72h per cycle, 168h on the long-horizon pass). Non-fatal, no live, no LLM.

---

## Real-DB results (72h window, before → after)

| metric | before | after |
|---|---|---|
| symbol match-rate — overall | 17.6% | **22.4%** |
| — crypto | 21.8% | **28.7%** |
| — stocks | 15.4% | **18.9%** |
| newly symbol-tagged (resolver) | — | **169** |
| stock signals w/ direct stock news but `news_supported=0` | **91** | **3** (88 fixed, **97%**) |

`catalyst-label-refresh` flipped `news_supported` 0→1 across the real stock book (AMD×27, JPM×26, LLY×26,
SMH×25, UNH×22, AVGO×19, SMCI×17, …). Scope mix of resolved rows: 597 `symbol`, 365 `geopolitics`, 149
`sector`, 87 `macro`, 70 `crypto_market`, 2321 genuinely un-entity-able. Examples the resolver now catches:
`$HOOD`→HOOD, "Intel"→INTC, "Ripple"→XRP, "Coinbase"→COIN (cross-asset), "Broadcom"→AVGO, listing headlines
→ tracked/untracked correctly, and "Fed holds rates as inflation cools" → `macro_only` (no fake ticker).

---

## Tests + guardrails

- **`tests/test_news_entity_resolver.py`** (12): A resolver (title/body/slug extraction, crypto+stock
  alias, cross-asset, listing parser tracked/untracked, macro no-forced-symbol, common-word safety);
  B schema additive+idempotent + union-only; C stock signal flips `news_supported` 0→1, crypto unchanged,
  no substring fabrication; D collector asset-aware fallback; E `load_news_window` is a time window;
  G enrichment-only guardrail.
- Regression: news/supervisor/scoring/default-schedule (**60**) + catalyst/news suites
  (label-refresh / layer / aster-regression / safe-fixes / news-detection / stocks-news-coverage) (**101**)
  — all pass. Scheduler dry-run `--dry-run --crypto-only` OK; resolver confirmed to run before catalyst-scan.

## Invariants
- `proposed_signals` **count unchanged** (3349) — only `news_supported`/`telegram_supported` flip 0→1
  (allowed additive), never 1→0, never score/tier/TP/SL.
- `signal_outcomes` / `SUM(final_r)` moved only via the **concurrent live-desk tracker**; this feature
  writes solely `news_items` (enrichment), `proposed_signals.news_supported` (0→1), `signal_catalyst_labels`.
- Live **LOCKED**; no live-order code; post-signal refresh never rewrites score/tier/TP/SL/actionability.

## Success criteria
- ✅ 72h match-rate materially improves, especially stocks (and crypto most of all).
- ✅ Stock signals with real nearby stock news no longer stay `news_supported=0` (91→3).
- ✅ Agents use time-window context, not tiny latest-N tails (all 4 call sites migrated, per-symbol capped).
- ✅ No false-positive explosion — common words stay unmatched; macro/geopolitics carry tags, not fake tickers.
- ✅ Enriched review + future scoring context now see the same richer, resolved news world.

**Note / honest follow-up:** `news_items.raw_json` currently persists title-only (no article body), so the
resolver's biggest untapped lever is having ingest persist the feed summary/body additively — that would let
the same resolver recover materially more on the 2321 currently-unknown rows. Flagged, not done here.
