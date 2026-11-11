# Crypto Signal Expansion v1 — Implementation Report

**Date:** 2026-06-09 · **Scope:** Read-only discovery layer that surfaces additional crypto candidates from RS / catalyst / narrative / volume / short-breakdown sources, routed through a shadow/C-tier safety lane. No scoring, threshold, TP/SL, or signal-generation logic changed. No auto-trade. No stocks touched.
**References:** [CRYPTO_SIGNAL_EXPANSION_PRECHECK.md](CRYPTO_SIGNAL_EXPANSION_PRECHECK.md) (baseline) · [STRATEGY_PLAYBOOK_AUDIT.md](STRATEGY_PLAYBOOK_AUDIT.md) (playbook contract).

## 1. What was built

### 1.1 New module
File: [src/agents/discovery_expansion_agent.py](../src/agents/discovery_expansion_agent.py) (~330 lines, pure stdlib + existing project imports).

Exposes:
- `DiscoveryExpansionAgent.run(...)` — reads candidates / catalysts / narratives / derivatives / top-setup-symbols and produces an `ExpansionResult`.
- `ExpansionResult.to_dict()` — JSON-friendly serialisation.
- `render_expansion_watchlist_markdown(result)` — markdown section ready to embed in a report or LLM packet.

### 1.2 Discovery sources (PART 2)
All seven sources run in parallel within the agent (no extra network calls — all data is already collected by the existing pipeline):

| # | Source | What it surfaces |
|---|---|---|
| 1 | `rs_btc_leader` | Top-5 symbols by `relative_strength_btc` above +2.5% threshold |
| 2 | `rs_eth_leader` | Top-5 by `relative_strength_eth` above +2.5% |
| 3 | `momentum_24h_leader` | Top-5 by `return_24h` above +5% |
| 4 | `momentum_7d_leader` | Top-5 by `return_7d` above +12% |
| 5 | `catalyst_backed` | Up to 10 symbols carrying catalyst events / fresh news |
| 6 | `narrative_basket` | Up to 5 narrative-basket members (perps_dex, ai_narrative, etc.) |
| 7 | `unusual_volume` | Top-5 by `volume_ratio` above 1.8× |
| 8 | `weak_rs_short` | Top-5 by `relative_strength_btc` BELOW −2.0% (short candidates) |

Max total watchlist = 25 entries per cycle, capped to prevent flooding.

### 1.3 PART 3 invariant — crypto scalp is NEVER expanded
`_playbook_for(direction, news_supported, mode)` deterministically maps every discovered candidate to one of:
- `crypto_failed_bounce_short` (for any short)
- `crypto_swing_narrative_rs_momentum` (for swing-mode longs)
- `crypto_intraday_catalyst_or_momentum` (for intraday-mode longs / news-backed)

There is **no path** in the code that produces `crypto_scalp_momentum_continuation`. A `result.skipped_scalp` counter is incremented if a scalp candidate would have been emitted — currently always 0. Verified by `test_scalp_playbook_is_never_produced_by_expansion`.

### 1.4 Shadow / C-tier safety lane (PART 4)
Every expansion candidate is evaluated against quality gates:
- **liquidity**: `quote_volume_24h_usd ≥ $5M`
- **active volume**: `volume_ratio ≥ 0.5×`
- **squeeze guard (shorts)**: `upper_wick_atr_max < 2.0×` AND `funding_rate > −5%` AND derivatives_available
- **derivatives availability** (for shorts / catalyst-backed)
- **playbook approved** (scalp blocked at routing layer)

Failed gates appear in `promotion_blockers` and the candidate is rendered with `status=shadow / C-tier` in the report. Passing all gates yields `status=ready-for-promotion`. **No automatic tier promotion happens** — the user manually decides whether to act, exactly as spec'd.

The render carries two human-readable columns:
- `Why not A/B yet` — first 3 blockers OR "Already in top-N deep setups".
- `Promotes when` — playbook-specific promotion checklist.

### 1.5 Wiring (PART 2-4 integration)
File: [src/agents/supervisor.py](../src/agents/supervisor.py)

The agent runs **after scoring** and **before** the trade-idea agent so it can see the already-narrowed top-N setups without affecting their tiering. The output:
1. Is persisted to `data/processed/agent_outputs/crypto_expansion_watchlist.json` for LLM-packet consumption.
2. Is passed as a new `expansion_result` kwarg to `ReportBuilder.build_daily()` and `build_context_for_llm()`.
3. Is rendered as a new section **"## 7e. Crypto Expansion Watchlist"** in the crypto report and appended to `context_for_llm.md`.

Failures in the agent are caught by `_log_secondary_failure` and never block the cycle.

### 1.6 ReportBuilder changes
File: [src/reports/report_builder.py](../src/reports/report_builder.py)
- New kwarg `expansion_result: Any = None` on `build_daily` and `build_context_for_llm`.
- Section 7e rendered before section 8 ("No-Trade Warnings").
- Section also appended to the end of `context_for_llm.md` so Opus sees it.

## 2. PART 5 — preserved protections

| Protection | Verification |
|---|---|
| Short squeeze guard | Existing scoring agent path untouched. New module ALSO adds its own squeeze flag to expansion candidates (test `test_short_squeeze_guard_flags_upper_wick`). |
| Pending revalidation (`stale_before_entry`, `entry_moved_away`) | Untouched. Module never calls revalidator. |
| Pre-entry stale/moved-away logic | Untouched. |
| Playbook labels | Existing labeling utility used to route expansion candidates; no label-rendering change. |
| Untracked legacy alert detector | Untouched. Verified `0` after the report run. |
| Catalyst mapping warnings | Untouched — module reads existing catalyst output. |
| Low-confidence scalp banner | Untouched. Scalp banner still renders unmodified. |

A read-only invariant test (`test_agent_does_not_import_sqlite_writes_directly`) asserts the agent does not import `TelegramNotifier`, `SQLiteStore`, `register_ideas`, or `upsert_proposed_signal`. The agent **cannot** mutate state by construction.

## 3. Tests
File: [tests/test_crypto_signal_expansion.py](../tests/test_crypto_signal_expansion.py) — **15 tests, all pass**:

| Group | Coverage |
|---|---|
| Source coverage | RS-BTC, weak-RS-short, catalyst, narrative basket, unusual volume |
| PART 3 invariant | scalp playbook never emitted (4 different candidate combos tested) |
| Quality gates | thin liquidity blocks; squeeze upper-wick blocks shorts; extreme negative funding blocks shorts; missing derivatives blocks shorts |
| In-top-setups | marked but still surfaced (informational) |
| Capping | total ≤ 25 entries |
| Markdown rendering | required columns present; empty result renders safely |
| Read-only | agent source does not import any write path |

Focused regression (75 tests): all pass.

## 4. Live first-cycle measurement

Ran scalp + intraday + swing reports after deploy.

| Metric | Baseline (5-cycle median) | Post-expansion (first cycle) |
|---|---:|---:|
| Total scanned (cross-exchange) | 138 | 140 |
| Fused candidates | 86 | 88 |
| Deep analysis | 47 | 48 |
| Full agent analysis | 20 (cap unchanged) | 20 (cap unchanged) |
| **Expansion watchlist evaluated** | n/a (new) | **35** |
| Expansion: in-top setups (counted but flagged) | n/a | 27 |
| Expansion: shadow / C-tier new | n/a | **8** (genuinely new visibility) |
| Skipped (scalp playbook) | n/a | **0** ✅ |
| Expansion by source breakdown | n/a | rs_btc=5, rs_eth=5, momentum_24h=5, momentum_7d=5, catalyst=10, weak_rs_short=5 |
| Crypto A/B Telegram-actionable last cycle | unchanged | unchanged (expansion does not auto-register) |
| Crypto scalp A/B this cycle | 10 | 10 (**no inflation**) |
| Short squeeze guard rejections last 7d | ≥ 90 | ≥ 90 (unchanged) |
| Runtime (scalp report wall) | ~1119 s (last live) | comparable; no extra network calls in expansion |
| Untracked legacy alerts | 0 | 0 |

The "in-top" count (27) is high because many strong RS/momentum names already make it into the top-20 setups — the expansion correctly shows them with `Already in top-N deep setups` status. The **8 genuinely new shadow candidates** are the value-add: names the user couldn't see before without manually scanning rejected lists.

Sample shadow candidate (live, this cycle):
```
| BIO/USDT | catalyst_backed | crypto_intraday_catalyst_or_momentum | long |
  53 | -1.9% | 0.2x | shadow / C-tier | low_volume_ratio | Confirm fresh
  catalyst + RS not contradicting + entry structure on 15m–1h. |
```

## 5. Files added / changed
**Added (2):**
- `src/agents/discovery_expansion_agent.py`
- `tests/test_crypto_signal_expansion.py`
- `reports/CRYPTO_SIGNAL_EXPANSION_PRECHECK.md`
- `reports/CRYPTO_SIGNAL_EXPANSION_REPORT.md` (this)
- `reports/POST_CRYPTO_SIGNAL_EXPANSION_VERIFICATION.md` (sibling)

**Changed (2):**
- `src/agents/supervisor.py` — invoke discovery + pass `expansion_result` to ReportBuilder; saved to JSON.
- `src/reports/report_builder.py` — accept `expansion_result` kwarg; render section 7e + append to `context_for_llm`.

**Not touched:**
- Any scoring agent, technical setup agent, trade idea agent, risk agent, or critic agent.
- Any config YAML (no threshold edits).
- TradeIdeaAgent gates (swing pause, invest pause, market closed, etc.) — untouched.
- Telegram alert path.
- Revalidator.

## Verdict
```
CRYPTO_SIGNAL_EXPANSION_v1_DEPLOYED
```

Live evidence: first cycle produced 35 evaluated expansion candidates with 8 genuinely new shadow-lane discoveries; scalp playbook violations = 0; squeeze guard fires unchanged; A/B Telegram volume unchanged; untracked legacy alerts = 0. The expansion is purely additive observability — manual review is the next gate.
