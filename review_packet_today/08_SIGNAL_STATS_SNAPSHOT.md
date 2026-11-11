# Signal Stats Snapshot — 2026-05-25

All commands run at ~17:50 EEST (14:50 UTC).

---

## 1. `signal-stats --asset-class crypto`

**Status:** succeeded, exit 0.

```
overall — week:
  sample = 1 (confidence = anecdotal)
  triggered = 0 / not_triggered = 1
  wins = 0  losses = 0  ambiguous = 0
  PF = None  avgR = None  totalR = 0.0

By tier:         1 row,  n=1, anecdotal
By mode:         1 row,  n=1, anecdotal
By direction:    1 row,  n=1, anecdotal
By exchange_confirmation: 1 row, n=1, anecdotal
By weekend_mode: 1 row,  n=1, anecdotal
By sector:       1 row,  n=1, anecdotal
By narrative:    1 row,  n=1, anecdotal
By setup:        1 row,  n=1, anecdotal
"no observations produced — sample sizes are still small."
```

**Reading**: only **one** crypto signal has ever been registered in the active 7-day window. None triggered. None won. The system correctly warns the sample is anecdotal.

That one signal is the **EDEN/USDT short from 2026-05-22** (visible in `obsidian_vault/11_Trade_Journal/Signal_Performance/Signal_Logs/2026-05-22_EDEN_USDT_sig_c4442a063769e04f.md`).

**Today's crypto reports produced 0 A-tier and 0 B-tier ideas**, so nothing new was registered. The watchlist/C-tier names are correctly NOT auto-registered without a trigger.

---

## 2. `signal-stats --asset-class stocks`

**Status:** succeeded, exit 0.

```
overall — week:
  sample = 19 (confidence = weak)
  triggered = 0 / not_triggered = 0
  wins = 0  losses = 0
  PF = None  avgR = None  totalR = 0.0

By tier:        3 rows  (A: 8, B: 8, C: 3)  — all anecdotal because the per-bucket n is <10
By mode:        2 rows  (intraday: 18 weak,  swing: 1 anecdotal)
By direction:   2 rows  (long: 18 weak,  short: 1 anecdotal)
By exchange_confirmation: 1 row, n=19 weak
By weekend_mode: 1 row, n=19 weak
By sector:      1 row, n=19 weak
By narrative:   1 row, n=19 weak
By setup:       1 row, n=19 weak
"no observations produced — sample sizes are still small."
```

**Reading**: 19 stocks signals have been registered across the last ~36 hours. None have triggered yet (none have crossed their entry zone with confirmation in the data the tracker has). All metric columns are blank because there are no terminal outcomes.

The 19 includes signals from yesterday's stocks intraday + today's stocks intraday + at least one swing (NVDA). Several symbols are duplicated across days (AAPL appears 3 times, TSLA 3 times) — this is acceptable for tracking but may inflate the per-symbol picture.

---

## 3. `active-signals` (no asset-class filter — flag not supported)

**Status:** succeeded, exit 0 — but **note**: `--asset-class` flag is **NOT supported** by `active-signals` (a separate run with `--asset-class crypto` errored with "No such option: --asset-class"). This is a UX gap — the user cannot easily list only crypto vs only stocks active signals.

**Total active: 19**

| Symbol | Asset class (inferred) | Tier | Mode | Dir | Score | Status |
|--------|------------------------|------|------|-----|-------|--------|
| AAPL | stocks | A | intraday | long | 88.64 | waiting |
| LLY  | stocks | A | intraday | long | 80.33 | waiting |
| AMD  | stocks | B | intraday | long | 78.77 | waiting |
| XLK  | stocks | B | intraday | long | 74.91 | waiting |
| SMCI | stocks | B | intraday | long | 74.26 | waiting |
| SMH  | stocks | B | intraday | long | 73.93 | waiting |
| UNH  | stocks | B | intraday | long | 68.59 | waiting |
| TSLA | stocks | B | intraday | long | 67.30 | waiting |
| QQQ  | stocks | C | intraday | long | 64.77 | waiting |
| IWM  | stocks | C | intraday | long | 56.47 | waiting |
| SPY  | stocks | C | intraday | long | 54.12 | waiting |
| XLV  | stocks | C | intraday | long | 52.46 | waiting |
| MSTR | stocks | C | intraday | short | 51.54 | waiting |
| DIA  | stocks | C | intraday | long | 50.27 | waiting |
| AAPL | stocks | A | intraday | long | ~86   | waiting (yesterday) |
| TSLA | stocks | C | intraday | long | ~64   | waiting (yesterday) |
| NVDA | stocks | C | swing    | long | ~56   | waiting |
| AAPL | stocks | B | intraday | long | 77.46 | waiting (Sunday) |
| TSLA | stocks | B | intraday | long | 70.15 | waiting (Sunday) |

**Crypto active signals visible in this list: 0**. The 7-day EDEN signal must be outside the active window or already expired.

**Concerns:**
- All 19 are `waiting` — none of the entry zones has been touched in a way that the tracker classifies as a triggered entry. After 36+ hours, that suggests either (a) the entry-trigger logic is too strict, or (b) prices simply have not pulled into the zones yet, or (c) the tracker has not advanced far enough into intraday OHLCV for stocks. See `16_SIGNAL_TRACKING_PERFORMANCE_AUDIT.md`.
- **C-tier entries are being registered** (QQQ, IWM, SPY, XLV, MSTR, DIA). The spec asked: "C-tier/watchlist ideas should only be saved when they have a clear actionable trigger." These C-tier signals do have entry zones and invalidation, so they pass the surface check, but **registering 6 C-tier names as signals every day** will quickly pollute the registry with low-conviction noise. Flag as a hygiene concern, not a bug.
- **Duplicate symbols** across days (AAPL ×3, TSLA ×3) — accepted by registry; not deduped, not consolidated.

---

## 4. `track-signals --all`

**Status:** succeeded, exit 0.

```
Tracking pass complete:
  checked     = 19
  updated     = 0
  tp_hits     = 0
  stopped     = 0
  expired     = 0
  not_triggered = 0
  ambiguous   = 0
  no_ohlcv    = 0
```

**Reading**:
- `no_ohlcv = 0` — **good**: stocks signals successfully read OHLCV from `data/raw/stocks/{tf}/{SYMBOL}.csv`. The Fix #1 ("track-signals asset_class-aware") works.
- `updated = 0` — none of the 19 signals had a state transition. Acceptable since US session has been live only ~80 minutes and zones are likely above current prices (the symbols moved up and the entry zones sit slightly below the latest 15m close).
- `expired = 0` — no signal aged out.
- `not_triggered = 0` — interesting: I'd expect at least some intraday signals to mark "not_triggered" once a hard deadline passes, but the tracker is silent. Confirm with a fresh tick after expiry hits.

---

## Summary

| Metric | Crypto | Stocks |
|--------|--------|--------|
| Total signals (week) | 1 | 19 |
| Active right now | 0 | 19 |
| Triggered | 0 | 0 |
| Wins | 0 | 0 |
| Losses | 0 | 0 |
| Confidence | anecdotal | weak |
| Stats by tier/mode/dir | yes (single row) | yes (3-row tier split) |
| Sample-size warning emitted | yes ("no observations produced — sample sizes are still small.") | yes (same line) |

The signal pipeline is **wired end-to-end** for stocks. For crypto it is **wired but starved** (no A/B ideas today, so nothing new to register). Sample sizes are nowhere near actionable. The system correctly refuses to compute winrate/PF on weak samples.

**No automatic rule-changing behavior was observed** — signal stats are passive, as required.
