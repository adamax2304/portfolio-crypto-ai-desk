# Catalyst / News → Signal Linkage Fix

**Date:** 2026-06-20 · **Scope:** display/measurement flags + derived label cache only.
**Not changed:** scoring, tier, TP/SL, entry/exit, routing/actionability, filters,
validity windows, scan-time enrichment — i.e. nothing that alters a trade decision
beyond correctly populating the catalyst/news flags.

## 1. Symptoms (verified read-only against the live DB)

1. **`signal_catalyst_labels` was frozen.** All 1,016 rows carried a single
   `computed_at = 2026-06-15T16:32:53` — the one-shot PART 9 backfill. No
   scheduler step ever rewrote it, so **0 of the 43** crypto signals from the
   last 2 days had a label row.
2. **`news_supported` was under-firing.** Only **5 of 43** last-2-day crypto
   signals had `news_supported=1`; **`telegram_supported` was 0** across all
   2,111 signals ever recorded.

## 2. Root cause (two independent failures)

### A. The derived label cache has no recurring writer
The PART 9 backfill report claimed "labels stay current going forward." They do
not — `signal_catalyst_labels` is only ever read (dashboard §14d); nothing
recomputes it. New signals therefore get no label at all.

### B. The scan-time news window is far too narrow for the desk's news volume
`news_supported` is set in `build_signal_from_idea` from
`idea.raw["catalyst"]["catalysts"]`, which the `CatalystAgent` fills from
`NewsAgent` over **`load_recent_news(limit=100)`**. The desk ingests ~460 crypto
news rows/day, so the freshest 100 rows ≈ the **last ~5 hours** (measured: the
100th-newest crypto row was published 2026-06-20T11:24 vs newest 16:22). Any
genuine, symbol-tagged catalyst published earlier the same day is **outside that
window** at scan time, so the symbol's `CatalystSummary` stays empty and
`news_supported` is left 0. The 24h/1000-row integrity monitor
(`news_catalyst_symbols`) would have seen them, but it only *reports* — it never
writes the flag.

### C. The original evidence's symbol counts were substring false positives
The triage counts ("ORDI=20, EDEN=8 … since 06-17") came from a naive
`title LIKE '%SYM%'`. Re-checked with the project's own word-boundary matcher
(`RSSNewsCollector._mentions_ticker`):

| Symbol | naive `LIKE` title | **whole-word** token | `detected_symbols_json` | genuine? |
|-------|----:|----:|----:|----|
| ORDI | 20 | **0** | 0 | ❌ "**Ordinals**" |
| EDEN | 8 | **0** | 0 | ❌ "Sweden"/"Eden" |
| ONDO | 9 | 0(title)/1(+body) | 1 | ✅ |
| TAO  | 1 | 0(title)/1(+body) | 2 | ✅ |

So **ORDI and EDEN have no real news catalyst** — flagging them would *fabricate*
one, exactly what the integrity layer forbids. The genuine under-fires are
symbols with real `detected_symbols_json` hits whose news fell outside the 5h
scan window (ONDO, TAO, WLD, XLM, AVAX, SUI, …).

## 3. Fix — `src/signals/catalyst_label_refresh.py` (per-cycle, post-scan)

A new operational step that, for signals created in the last `--days` (default 7)
plus any still-active signal:

- Re-derives "does this symbol have a direct catalyst near its creation time"
  via a **robust `detected_symbols_json` join** windowed `[created_at − 48h,
  created_at + 2h]` — the *same* word-boundary detection the collector already
  applied. **Never a title substring**, so "Ordinals" can't fabricate ORDI.
- **Additively** upgrades `news_supported` / `telegram_supported` `0 → 1`
  (telegram = a hit from a `t.me/*` source). It **never downgrades** `1 → 0`, so
  an in-flight position is never re-sized smaller.
- Recomputes `compute_labels` (overlaying the matched headline/source/published_at
  so freshness/strength/source are real) and upserts `signal_catalyst_labels`
  with a fresh `computed_at`.

Wired as:
- CLI: `python -m src.cli catalyst-label-refresh [--days N] [--lookback-hours H] [--labels-only]`
- Scheduler: non-fatal `catalyst label refresh` step in
  `scripts/run_default_market_schedule.py`, right after the catalyst integrity
  scan (so it rebuilds labels every cycle).

### Why this is decision-safe
`telegram_supported` has no scoring/routing/sizing consumer (display only).
`news_supported` does feed the playbook label → sizing weight, but: (a) correcting
the flag to its true value is the explicitly sanctioned change; (b) the update is
**additive-only** (never reduces a position); (c) the project is paper-trading;
(d) `detected_symbols_json` is the integrity layer's own source of truth, so the
refresh can only assert catalysts the integrity monitor would also confirm. The
scan-time enrichment is left untouched (widening it would change catalyst inputs
to scoring/risk/narrative — out of scope).

## 4. Result (live DB, before → after)

| Metric | Before | After |
|---|---:|---:|
| last-2-day crypto `news_supported=1` | 5 | **12** |
| last-2-day crypto `telegram_supported=1` | 0 | **5** |
| last-2-day signals with a label row | 0 / 43 | **43 / 43** |
| `signal_catalyst_labels` newest `computed_at` | 2026-06-15T16:32 | **2026-06-20T17:25** |
| ORDI / EDEN `news_supported` | 0 | **0** (correctly, no fabrication) |

One refresh pass: `scanned=781, news_flips=40, telegram_flips=14,
labels_written=781`. Flipped symbols (7-day scope) are all genuine
`detected_symbols_json` tokens — XLM, ZRO, WLD, ONDO, **ASTER**, SUI, NEAR, AVAX,
ADA, AAVE, SOL, PYTH, FET, TAO. (ASTER recovering its flag is the original
regression case.)

## 5. Test

`tests/test_catalyst_label_refresh.py` (6 cases): genuine detected hit →
`news_supported=1` + non-"none" label; **"Ordinals" title-only → stays 0** (no
fabrication); telegram source → `telegram_supported=1`; out-of-window hit
ignored; additive-only + idempotent; `--labels-only` rebuilds the cache without
touching flags. Full related suite (catalyst / playbook / sizing) green: 105 passed.

## 6. Follow-up (NOT done here — would touch trade decisions)

The deeper scan-time root cause (B) is `load_recent_news(limit=100)`. Widening it
(or switching `CatalystAgent` to a time-windowed load) would make `news_supported`
correct *at creation time* for new signals — but it also changes the catalyst
inputs to `data_confidence` / risk / narrative / scoring, so it needs its own
review and explicit sign-off. The per-cycle refresh corrects the flags and labels
operationally in the meantime.
