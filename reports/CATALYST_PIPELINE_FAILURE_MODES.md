# Catalyst Pipeline — Failure Modes (PART 9)

**Date:** 2026-06-15 · Read-only.

| # | Failure mode | Evidence | Severity | Est. R impact | Safe fix |
|---|---|---|---|---|---|
| 1 | **Stocks `news_supported` flag never set** | 533/533 closed stocks A/B signals have `news_supported=0` despite 7,547 stock news items/14d | **MEDIUM** | unmeasurable (blocks the catalyst-vs-not analysis entirely) | label-only: set the flag from the scorer's news_payload |
| 2 | **No catalyst freshness gate (crypto)** | scorer has no age cutoff; old (>6h) catalysts remain fully actionable | MEDIUM | unknown — stale catalysts may back late entries | scoring change (NEEDS APPROVAL) — do not implement now; add freshness label first |
| 3 | **Funding/OI latest-cache, no archive** | no `funding_snapshots`/`oi_snapshots` table; only string blob per signal | MEDIUM | blocks historical replay + funding-cost modelling | archive-only: add snapshot tables written per cycle |
| 4 | **Catalyst context not in Telegram** | messages show cautions but not positive catalyst/source/freshness | LOW | operator can't tell catalyst-backed from technical at a glance | label-only (needs approval — changes message) |
| 5 | **No options/OI for stocks** | only earnings (yfinance) + company news; no options data source | LOW | stocks lack a derivatives confirmation axis | no action (no free data source); just label "options/OI: not available" |
| 6 | **Analyst actions classified but unused** | `classifier.py` detects analyst_action; never wired to scoring or packet | LOW | minor missed signal | dashboard/packet-only: surface analyst actions |
| 7 | **Source quality not surfaced** | `classify_source_quality` computed, not shown to operator/Opus | LOW | operator can't weight social vs official | label-only |
| 8 | **Fast intraday moves entered late or rejected** | 2h cycle; #1 reject reason `>2 ATR from EMA20` (446/14d) | LOW (working as designed) | chase-rejection is net-protective | no action; optional fast-move report |
| 9 | **Symbol detected but no signal** | 202/400 symbol-tagged news produced no A/B signal | LOW | mostly macro/non-universe — expected | no action |
| 10 | **Individual catalyst not age-flagged in packet** | baskets carry freshness; high-conf catalyst list does not | LOW | Opus may over-weight stale catalyst | packet-only: add age tag to each high-conf catalyst |

## Severity summary

- **No CRITICAL failures.** The pipeline collects, classifies, packets, scores, and labels (crypto) correctly.
- **3 MEDIUM**: stocks news flag unset (#1), no freshness gate (#2), no derivatives archive (#3). All have **safe additive fixes** except the freshness gate (scoring change → needs approval).
- The rest are LOW / working-as-designed.

## What is NOT broken

- News collection (13.7k items, both asset classes, real-time Telegram + RSS).
- Crypto catalyst → scoring → `news_supported` label (and it WORKS: +15R vs −3R).
- Funding/OI coverage (100% on crypto A/B).
- Chase-rejection (net-protective).
