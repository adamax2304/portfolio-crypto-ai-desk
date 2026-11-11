# News Block Completion Report

Generated: 2026-07-14 (Asia/Nicosia)

## Status

The production news block is operational and quality-gated. Raw ingest remains
fail-open; news enrichment cannot lose an article or stop paper trading. Live
remains locked.

## What is now authoritative

1. Every common RSS, Telegram and structured-row SQLite ingest commits the raw
   row first, then immediately resolves exact URLs and materializes canonical
   events. Scheduled 24/72/168h passes are repair/backfill only.
2. `news_asset_registry` separates curated `TRACKED` assets from exchange-seen
   `DISCOVERED` assets. Discovery never auto-promotes a symbol into trading.
3. `news_canonical_events` records subject symbols, all mentioned symbols,
   event type, direction, source/content quality, confidence, dedupe cluster,
   TTL, risk action and the fixed positive-linkage decision.
4. Headline-only secondary/social news cannot positively support paper size.
   Official structured exchange/regulator headlines have a narrow exception.
5. Social news needs independent non-social corroboration. Repeated copies are
   one cluster, not multiple confirmations.
6. Bearish news is separated from bullish support. The final signal direction
   is checked at registration and at catalyst-label refresh.
7. `NewsAgent` now uses resolver-enriched DB fields instead of restoring stale
   ingest symbols from `raw_json`. Positive and risk events are separate inputs.
8. Opus packets receive actual material canonical events with confidence,
   content level and risk policy, not only aggregate news counts.

## Production verification

- Gold regression: **31/31 passed**.
- Relevant automated regression: **291 passed, 0 failed**.
- Resolver health: **100% resolved** in 24h and 72h; unresolved symbol-tagged: **0**.
- Immediate-path latency from a real 18-feed RSS smoke:
  **n=33, p50=8.652s, p95=14.253s**.
- Source health: **44 OK, 5 STALE, 0 DEAD, 0 ERROR, 21 explicitly disabled**.
- Blocking coverage gaps: **0 unmapped impact, 0 pending persistence**.
- Review queues: 7 exchange-discovered/untracked crypto assets and 24 stocks
  outside the configured trade universe. These are visible but cannot trade.
- Content, 72h: 3,039 rows; 864 full body, 323 complete short messages,
  1,852 title-only. Title-only limitations are now enforced by policy.
- Canonical store: 9,981 rows / 9,024 primary clusters. Only 4 current
  directional events pass the strict positive-linkage contract; all other news
  remains available as context/risk/diagnostics rather than becoming a false
  catalyst boost.

## False-positive hardening

- Word-boundary taxonomy prevents `war` inside `software`.
- Full article prose no longer invents a headline event type.
- Subject symbols are separated from incidental mentions.
- Plaintiffs, analyst firms, former employers and generic DeFi `oracle` text do
  not become issuer risk/catalyst subjects.
- Crypto attacks/theft are classified as security risk, not geopolitics.
- Nasdaq equity delisting is not treated as a crypto-token delisting.

## Operations

The default scheduler includes asset-registry, canonical repair and gold/replay
quality steps every cycle. It was reloaded successfully (scheduler PID 1896).
The independent Telegram collector stayed running (PID 11320).

The 5 STALE sources are not transport failures: three were quiet for 24h but
have rows inside 72h; BWEnews and AstronomicaNews were reachable but published
no eligible message in the recovery window. ERROR/DEAD remains zero and the
existing transition monitor writes the error journal and alerts Telegram.

## Future maintenance

For a newly observed asset, the exchange universe creates a `DISCOVERED` row
automatically. To trust it, add its canonical name/aliases to the relevant
`config/*_entity_aliases.yaml` file and add one positive plus one collision case
to `config/news_gold_cases.yaml`. No resolver code change is normally needed.

New providers still require source configuration and may require an adapter if
their API/feed format changes. Event taxonomy should only change when a genuinely
new event class appears. The quality gate must remain green before claiming the
news block is reliable.

## Trading invariants

- `proposed_signals`: 3,641 before/after implementation.
- `news_supported`: 937 before/after production refresh (no historical rewrite).
- Live-status rows: 0.
- No news module writes `signal_outcomes`, `final_r`, TP/SL, entry geometry or
  order APIs. Outcome-count drift during verification came from the already
  running tracker, not this change.
