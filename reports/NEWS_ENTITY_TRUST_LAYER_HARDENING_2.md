# News/Entity Trust-Layer — Production Hardening (freshness + safety)

Date: 2026-07-08 · Scope: **read-model / enrichment / diagnostics only**. A/B logic, paper execution,
`final_r`, `signal_outcomes`, execution ledger, live routing, scoring, TP/SL **UNTOUCHED** (live LOCKED).
The catalyst linkage still only moves `proposed_signals.news_supported` 0→1 (additive, never 1→0).

Goal: after ingest, news rows should not sit with a `detected_symbols_json` but no
`resolution_status`/`trusted_symbols_json`. This adds **resolver freshness/coverage monitoring**, runs the
resolver **closer to ingest**, and tightens the cashtag-fallback policy.

---

## 1. Resolver freshness / coverage diagnostics — `news-entity-health`

New read-model `src/news/entity_health.py` (mirrors `source_health.py`): CLI `news-entity-health` →
`reports/NEWS_ENTITY_HEALTH.md` + `data/diagnostics/news_entity_health.json` (the control-plane contract,
same dir as `news_source_health.json`).

Metrics per **24h and 72h**: `rows`, `resolved` (`resolution_status IS NOT NULL`) + `resolved_pct`,
`symbol_tagged`, **`unresolved_symbol_tagged`** (`detected_symbols NOT IN ('[]','') AND resolution_status
IS NULL` — the backlog to keep at zero), `trusted_symbol_tagged`, `preexisting_unverified`. Plus
`resolver_last_run_at`/age (from `MAX(resolved_at)`), `max_unresolved_age_minutes`, oldest-unresolved
timestamp, and the newest unresolved examples (title/source/published_at/asset_class/detected_symbols).

**Severity** (one scheduler cycle = 120m):
- `OK` — `unresolved_symbol_tagged_24h == 0` or every unresolved row newer than one cycle.
- `WARN` — unresolved > 0 and oldest older than one cycle (resolver ran but missed some).
- `CRITICAL` — unresolved_24h ≥ 50, or unresolved share ≥ 50% (≥20 tagged), or the resolver has not
  written anything in 24h (`resolver_stale`).

Fail-open: on a pre-migration DB (no trust columns) it reports everything unresolved instead of crashing.
Read-only — never resolves, never touches score/tier/final_r/signal_outcomes/proposed_signals/live.

## 2. Scheduler integration — resolver closer to ingest

There is **no standalone news/rss/telegram ingest step** — ingest is baked into the report steps
(`RSSNewsCollector` runs inside scalp/intraday and the stock reports). So:
- The existing `news-entity-resolve --hours 72` stays **before** catalyst-scan (it already runs right
  after the crypto reports that ingest crypto news). Long-horizon pass stays **168h**.
- **New:** a lightweight `news-entity-resolve --hours 24 --limit 10000` runs **immediately after
  `stocks_report_steps()`** — the one ingest that happens *after* the main 72h resolver — so freshly
  landed stock news gets `resolution_status`/`trusted_symbols_json` **same-cycle** instead of waiting a
  full cycle. Idempotent, UNION-only, `command_nonfatal`.

Verified in the built cycle: `news entity resolve (72h)` → catalyst-scan/integrity/label-refresh →
`stocks intraday report` → `news entity resolve (fast 24h post-ingest)`; long-horizon crypto-only shows
`news entity resolve (168h)`.

## 3. Catalyst label-refresh safety — `direct_news_for_signal()`

- A row the resolver has **not processed** (`trusted_symbols_json IS NULL`, `resolution_status IS NULL`) is
  **not trusted** — only a resolver-written non-empty list counts.
- **Cashtag fallback is now asset-aware**: stocks trust only `$TICKER` (a `#TICKER` hashtag is social
  noise on equities); crypto trust `$TICKER` **or** `#TICKER`.
- Legacy behaviour is unchanged on a DB with no `trusted_symbols_json` column (fail-safe, not fail-open).

New regression tests (in `tests/test_news_entity_resolver.py`):
`test_null_trusted_symbols_json_not_trusted`, `test_stock_hashtag_does_not_flip_but_cashtag_does`
(`#DIA` → no flip, `$DIA` → flip), `test_crypto_hashtag_and_cashtag_both_flip` (`#ARB` → flip), plus
`test_entity_health_flags_unresolved_backlog` / `test_entity_health_ok_when_all_resolved`.

## 4. Docstrings corrected

`src/signals/catalyst_label_refresh.py` no longer calls `detected_symbols_json` the trusted source. New
truth documented on the module and on `direct_news_for_signal`: `detected_symbols_json` = broad candidate
set (union of resolver hits + naive ingest scan, used only to FIND rows); `trusted_symbols_json` = allowed
source for flipping `news_supported`; legacy membership only when the DB predates the trust layer.

## 5. UI / control-plane

The control plane is a separate app (trading-desk-control); this repo's integration surface is
`data/diagnostics/*.json`. `news_entity_health.json` is emitted in that standard location with `severity`,
`resolved %`, `unresolved_symbol_tagged`, `max_unresolved_age_minutes`, and resolver last-run — enough for a
compact "Entity resolver health" row alongside the existing source-health block. (No new screen; the JSON is
the contract, consistent with `news-source-health` which is also CLI-refreshed, not in the scheduler.)

---

## 6–7. Verification + real-DB acceptance

- **pytest (11 files): 161 passed** — `test_news_entity_resolver` (now incl. cashtag-policy + health),
  news_layer, catalyst_label_refresh, catalyst_layer, catalyst_integrity, catalyst_safe_fixes,
  stocks_news_tagging, news_detection, stocks_news_coverage, supervisor_smoke, supervisor_routing.
- `news-entity-health`: **severity OK**, 24h **1241 rows / 100% resolved / 0 unresolved symbol-tagged /
  219 trusted / 32 preexisting_unverified**; 72h 3829 / 100% / **0 unresolved** / 771 trusted / 78 pu;
  resolver last run ~25m ago (not stale). JSON + MD written.
- `news-entity-audit --hours 72` OK (crypto 29.3%, stocks 18.3%). Scheduler `--dry-run --crypto-only`
  clean, no Opus/Claude tokens; both resolver passes present in the plan.
- **DIA remains untrusted**: 9 DIA-tagged rows, **0 trusted** ("King Copper …DIA Approval" + market-wraps
  all blocked).
- **`unresolved_symbol_tagged_24h = 0`** — no backlog.
- **Invariants**: `proposed_signals` 3366 (unchanged), `news_supported=1` 770 (additive only, no
  downgrade), `signal_outcomes`/`SUM(final_r)` move only via the concurrent live-desk tracker. No changes
  to final_r / signal_outcomes / execution ledger / live routing / scoring / TP/SL.
