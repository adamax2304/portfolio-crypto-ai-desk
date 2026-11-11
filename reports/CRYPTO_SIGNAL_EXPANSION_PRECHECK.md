# Crypto Signal Expansion — Pre-check (PART 1)

**Date:** 2026-06-09 · **Scope:** Read-only audit of current crypto funnel capacity. No code changed in this step. Baseline measurement to compare PART 7 against.

## 1. Funnel capacity over the last 5 crypto cycles

| Cycle (scalp) | binance | bybit | mexc | post-liquidity | post-momentum | fused | deep | full agent | trade ideas |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 14:19 | 64 | 2 | 70 | 60 | 25 | 85 | 43 | **20** | 10 |
| 16:48 | 67 | 2 | 67 | 60 | 28 | 84 | 47 | **20** | 11 |
| 17:51 | 68 | 2 | 69 | 63 | 7 | 88 | 48 | **20** | 10 |
| 18:21 | 68 | 2 | 69 | 63 | 7 | 88 | 48 | **20** | 10 |
| 20:21 | 70 | 2 | 68 | 63 | 31 | 88 | 46 | **20** | 10 |

Intraday and swing cycles use the same upstream universe and report nearly identical scan/fuse counts. Post-momentum varies (7 → 31) depending on whether breadth is in flush vs expansion state.

### What this tells us
- **Total cross-exchange scan = ~135–140 symbols** (binance ~68 + bybit ~2 + mexc ~68). Bybit contributes very little — the bybit universe is fetched but a strict liquidity threshold drops most.
- **Fused candidates = ~85–88**. The fusion already de-dupes the same base asset across venues.
- **Deep analysis = ~45–48** — about half the fused set survives the deep filters.
- **Full agent analysis = hard cap at 20** — this is a configured ceiling (`max_full_agent` in the report config).
- **Trade ideas rendered = 10–11** — A/B/C combined ideas surfaced in the report (not all become Telegram-actionable).

The **hard 20-cap on full agent analysis** is the dominant bottleneck. Discovery sources beyond that cap are silently dropped from idea generation.

## 2. Recent 24h proposed_signals (live)

| mode | tier | count |
|---|---|---:|
| intraday | B | 1 |
| scalp | B | 8 |
| swing | B | 5 |

14 A/B crypto signals over 24h, dominated by scalp (which is the LOW-CONFIDENCE playbook). Intraday actionable count is anemic (1).

## 3. Top rejection reasons (last 7d, `trade_ideas.tier=rejected`)

| Rank | Reason | Count |
|---|---|---:|
| 1 | _no cap reason_ (failed scoring threshold, below 50) | 582 |
| 2 | RS-leader long vs bearish tape (counter-trend cap) | 24 |
| 3 | short squeeze: thin liquidity + upper-wick | 21 |
| 4 | short squeeze: thin liquidity + upper-wick (+exhaustion) | 21 |
| 5 | short squeeze: thin liquidity only | 20 |
| 6 | short squeeze: high upper-wick only | 18 |
| 7 | extreme negative funding against short | 11 |
| 8 | various combos of the above | 10–8 |

The short-squeeze guard is firing **regularly** (≥90 hits/7d). This is the **expected protection** — do NOT weaken.

## 4. Source-exchange coverage breakdown

Per-exchange OHLCV from this cycle's `last_update.json` (most recent crypto report):
- binance: 72 ohlcv ok / 0 fail
- bybit: 47 ohlcv ok / 7 fail (symbols not listed there — normal)
- mexc: 72 ohlcv ok / 2 fail

OHLCV availability is healthy. Failures are symbol-listing differences, not infrastructure errors.

## 5. Catalyst pipeline coverage (today)

- News items collected today: **375**
- News items with detected symbols (entity-alias mapped): **113** (~30%)

70% of news items do not produce a symbol mapping. This means many catalyst-triggering names never reach the candidate funnel via the news lane, even though the data is there.

## 6. What is "lost" today (the symbols not getting traded)

Looking at the funnel: the system already discovers ~135 symbols per cycle. The dominant loss vectors are:
1. **Hard 20-cap on full agent analysis** — drops ~25 symbols that passed deep analysis.
2. **Catalyst→symbol mapping gap** — ~70% of news items don't map, so catalyst-tagged opportunities are partially invisible.
3. **Narrative basket members** — collected (perps_dex, ai_narrative, etc.) but only surface if they happen to score high in the existing momentum scanner.
4. **RS-vs-ETH leaders** — momentum_scanner_agent computes `relative_strength_eth` but does NOT use it to lift a symbol into the candidate set independently.
5. **Short candidates on MEXC** — derivatives quality on MEXC is partial; short squeeze guard correctly demotes those.

## 7. Baseline metrics to compare PART 7 against

| Metric | Baseline (5-cycle median) | Target after expansion |
|---|---:|---:|
| Total scanned (across exchanges) | 138 | ≥ 150 (more discovery sources, same liquidity gates) |
| Fused candidates | 86 | ≥ 100 |
| Deep analysis | 47 | ≥ 50 |
| Full agent analysis | 20 (hard cap) | 20 (cap unchanged in v1) |
| Trade ideas rendered (A/B/C combined) | 10 | 12–15 (extra C-tier shadow lane) |
| Crypto A/B Telegram-actionable (24h) | 14 | ≤ 18 (avoid spam; expansion mostly to C) |
| Crypto scalp A/B count (24h) | 8 | **= 8** (no scalp expansion per spec) |
| Short squeeze guard hits (7d) | ≥ 90 | ≥ 90 (must stay strong) |
| Catalyst-mapped news ratio | 30% | 30% (mapping fix out of scope) |
| Runtime (production crypto report, parallel) | ~1100–1500 s | ≤ 2500 s (well under 2700 s timeout) |

## 8. Verdict for PART 1
The funnel is **healthy and protections are firing**. The lever for expansion is **discovery breadth before the 20-cap**, not threshold weakening. v1 will add a parallel "expansion candidates" lane that surfaces additional names from catalyst / narrative / RS / volume / short-breakdown sources and routes them through the existing scoring pipeline — but caps them to C-tier shadow status unless they independently pass the normal A/B path.

```
CRYPTO_FUNNEL_PRECHECK_COMPLETE
```
