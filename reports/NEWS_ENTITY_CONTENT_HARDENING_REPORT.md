# News Entity And Content Hardening Report

Generated 2026-07-13. Scope: production news ingest/enrichment, source-health, and diagnostics only.
No trading score, tier, actionability, paper execution, PnL, live routing, or order path was changed.

## Delivered

- Entity resolver v4 adds safe issuer/CIK resolution for structured SEC/provider rows and exact canonical issuer names.
- The alias tables now cover `J.P. Morgan Asset Management` / `Campbell Global -> JPM` and vetted established
  crypto assets `HBAR`, `LPT`, `MAGIC`, `MASK`, `SUSHI`, and `SKY`.
- Crypto listing parsing now requires a crypto-exchange context or an explicit USDT/USDC pair. Dynamic local-exchange
  symbols are recognised as candidates but never become trusted tradeable catalysts without curated confirmation.
- `NEWS_CONTENT_COVERAGE.md` and `news_content_coverage.json` distinguish `full_body`, `body_equals_title`,
  `summary_only`, and true `title_only` by source and asset class.
- `NEWS_COVERAGE_GAPS.md` and JSON report high-impact rows with no trusted entity. Generic legal/earnings prose with
  no issuer/project/ticker is excluded as non-symbol context; explicit stocks outside the configured trade universe
  are labelled separately instead of being called resolver failures.
- Targeted Telegram recovery is scheduler-wired. It only catches up ERROR/DEAD sources or STALE channels with zero
  rows in 72h, uses a copied Telethon session, has a six-hour cooldown, records telemetry/error-journal events, and
  relies on the existing transition-based Telegram health alerts for actual failures.

## Current Read Model Snapshot

- Resolver health: OK. In the last 72h, 2,990 rows were resolved and none of the symbol-tagged rows remained
  unresolved; 538 rows had trusted symbols.
- Content coverage: 2,988 rows. 781 had retained additional body text, 297 were complete short messages whose body
  equals the title, and 1,910 were truly title-only (64%). The largest title-only sources are CryptoBriefing, Yahoo
  Finance Top Stories, Motley Fool, PR Newswire, and Seeking Alpha. This is an explicit evidence limitation, not a
  claim that their original websites lack article bodies.
- Coverage-gap queue: 23 rows: 7 untracked crypto listing/project entities and 16 explicit stocks outside the current
  trade universe. There are no remaining unresolved-persistence cases in the queue.
- Telegram recovery: BWEnews and AstronomicaNews were reached successfully but had zero eligible messages in the
  72h window. Health keeps them STALE for freshness, while reporting the successful targeted verification so they are
  not misdiagnosed as broken/auth-failed. Three other Telegram channels are only stale over 24h and are not needlessly
  backfilled.

## Verification

- `python -m pytest tests/news tests/test_news_entity_resolver.py tests/test_news_content_hardening.py tests/test_stocks_news_coverage.py tests/test_default_market_schedule.py -q`
  -> 130 passed.
- Scheduler dry run completes, and unit tests verify the targeted recovery plus both diagnostics are present in every
  normal cycle.
- During the production enrichment run, `proposed_signals` and the paper ledger remained unchanged. Background
  trackers continued to update `signal_outcomes/final_r` independently; the news modules contain no SQL or code path
  that writes those tables.

## Remaining Constraint

The system is materially more observable and safer to trust, but it is not correct to claim that every news item is
fully understood. Title-only coverage is still 64%. The next evidence-based improvement would be source-specific
body adapters for the highest-volume title-only providers, subject to their access rules, rather than broad scraping.
