# News/Entity Layer — Trust-Layer Hardening (safe state)

Date: 2026-07-08 · Scope: **production read-model / enrichment only**. Live A/B, paper execution,
`final_r`, `signal_outcomes`, live routing **UNTOUCHED** (live LOCKED). The linkage still only moves
`proposed_signals.news_supported` 0→1 (additive, never 1→0), never score/tier/TP/SL/actionability.

**Motivating regression:** GlobeNewswire *"King Copper Discovery Receives DIA Approval for 36,010-metre
Drill Program…"* was flipping `news_supported` for the **Dow-Jones ETF DIA** — because
`direct_news_for_signal` blindly trusted `detected_symbols_json`, which is a *union of resolver hits and a
naïve ingest bare-ticker scan*. "DIA" there is a regulatory approval acronym, not a tradable ticker.

---

## What changed (all additive, all read-model)

1. **Provenance split — "detected" vs "trusted" symbol.** The resolver now emits `trusted_symbols` (only
   symbols with real matcher provenance: company/token **alias**, **cashtag** `$TICKER`, **listing parser**,
   or **cross-asset** alias) separately from `detected_symbols` (union-kept, never destructive). Two new
   additive nullable columns on `news_items`: `trusted_symbols_json`, `resolution_status`.
2. **Honest provenance labels.** `entity_match_source` no longer writes a clean-looking `'none'` when nothing
   resolved. `resolution_status ∈ {resolver_confirmed, resolver_added, preexisting_unverified, macro_only,
   no_match}`; a row that arrived with a bare ingest tag but no trusted match is stamped
   `preexisting_unverified` (source label too), and `entity_match_confidence` is capped at 0.4 when there is
   no trusted symbol.
3. **Ambiguous-ticker guard.** Short ETF / acronym tickers (`DIA SPY QQQ IWM SMH XLF … ARB OP ONE NEAR LINK
   FLOW …`) are trusted **only** with a cashtag (`$DIA`) or an explicit descriptive/ETF/company alias
   ("SPDR Dow Jones ETF"). A bare uppercase token in prose never trusts them.
4. **Trust gate in `direct_news_for_signal`.** After the existing exact-membership check, a hit counts only
   if the ticker is in that row's `trusted_symbols_json` **or** a cashtag `$TICKER`/`#TICKER` is in the
   title. `entity_match_source` NULL/`none`/`preexisting_unverified` with confidence 0 can no longer flip
   `news_supported`. Pre-migration DBs (no `trusted_symbols_json` column) keep the legacy behaviour, so the
   gate is fail-safe, not fail-open.

---

## Real-DB verification (72h window, live production DB)

**Trust split** — 3,855 news rows; 854 carry `detected_symbols`:

| bucket | count |
|---|---|
| trusted (`resolver_confirmed` + `resolver_added`) | **775** |
| **untrusted preexisting** (`preexisting_unverified`, was silently trusted before) | **79** |

`resolution_status`: `resolver_confirmed` 773 · `resolver_added` 2 · `preexisting_unverified` 79 ·
`macro_only` 465 · `no_match` 2,536. `entity_match_source` is now honest — the 79 untrusted rows read
`preexisting_unverified`, **not** a fabricated clean `none`/`alias_*`.

**DIA false positive — gone.** Of **9** DIA-tagged rows in the DB, **0 are trusted**. "King Copper …DIA
Approval" and every market-wrap headline ("Dow, S&P, Nasdaq surge…", tagged from body) are `blocked`. DIA
can no longer flip `news_supported` for any signal.

**Old-vs-new linkage delta** (fresh recompute over the 1,081 in-scope signals — 7d + active):

| | news_supported would assert |
|---|---|
| OLD (no trust gate) | 484 |
| NEW (trust gate) | **148** |
| prevented (untrusted-only evidence) | **336** |

The 336 prevented are exactly what should be prevented: generic listicles ("Best Tech Stocks Right Now",
tickers tagged from an article body that `raw_json` doesn't persist), bare-ticker-only mentions, and
ambiguous ETFs (SMH×25, QQQ×11). **Genuine company-named catalysts still fire** — JPMorgan→JPM, Advanced
Micro Devices→AMD, Microsoft→MSFT, Oracle→ORCL, Micron→MU all stay `resolver_confirmed`/trusted. This is a
*display/measurement* flag, so tightening it makes the catalyst-supported stats honest without touching any
live or paper execution path. (Note: on the current live DB the flip candidates are 0/0 because everything
flippable was already flipped earlier today; the gate never **downgrades** an existing `=1`, it only
governs future flips.)

---

## Tests (7-file suite: **120 passed**)

New trust-layer regressions in `tests/test_news_entity_resolver.py`:
- `test_dia_approval_false_positive_not_trusted` — "…Receives DIA Approval" → DIA **not** trusted; source
  is `no_match`/`macro_tagger`, never a fake `alias_stocks`.
- `test_real_dia_cashtag_and_alias_are_trusted` — `$DIA` and "SPDR Dow Jones ETF" → DIA trusted.
- `test_refresh_marks_untrusted_preexisting` — preexisting bare `["DIA"]` → union keeps DIA,
  `trusted_symbols_json='[]'`, `resolution_status='preexisting_unverified'`.
- `test_untrusted_preexisting_stock_tag_does_not_flip` — untrusted `DIA` row → no flip; a trusted row for
  the same ticker → flips.
- `test_untrusted_preexisting_crypto_tag_does_not_flip` — untrusted `ARB` row → no flip; `$ARB` cashtag →
  flips (crypto side of the gate).

Date-dependent failures fixed (deterministic, now-relative fixtures): `test_news_layer.py`
taxonomy/dedupe (`normalized_events` has no `now` param) and the 3 `CompanyNewsAgent` stock tests (fresh
`published_at` so the 72h window keeps them). Full suite:
`tests/test_news_entity_resolver.py tests/news/test_news_layer.py tests/test_catalyst_label_refresh.py
tests/test_catalyst_layer.py tests/test_catalyst_integrity.py tests/test_catalyst_safe_fixes.py
tests/stocks/test_stocks_news_tagging.py` → **120 passed**.

`news-entity-audit --hours 72` OK; `run_default_market_schedule.py --dry-run --crypto-only` clean —
`news-entity-resolve` runs **before** catalyst-scan / catalyst-label-refresh, all 12 CLI validations OK,
no Opus/Claude tokens in the plan.

## Invariants (baseline → after)
- `proposed_signals` 3365 → 3366 (+1 concurrent live desk); `news_supported=1` 769 → 770 (+1, 0→1 only).
- `signal_outcomes` 818,186 → 818,359 and `SUM(final_r)` 980,718 → 980,957 — **concurrent live-desk
  tracker only**; this feature writes solely `news_items` enrichment + `news_supported` 0→1.
- No existing `news_supported=1` downgraded. Live/auto-live/manual-live **LOCKED**; no execution routing,
  `final_r`, or `signal_outcomes` code touched.

## Honest follow-up (unchanged from prior deliverable)
`news_items.raw_json` still persists title-only for ~33k rows. That is *why* legitimate bare-ticker
stories (e.g. "AMD Is 11% Away From the $1T Club") land in `preexisting_unverified` — the resolver only
sees the title. Persisting the feed summary/body additively would let the same resolver **recover** those
with real provenance (the full company name in the body), turning conservative suppressions back into
trusted flips. Flagged, not done here.
