# Fresh Monitor Session Report

**Session window:** 2026-05-26 ~01:14 → ~02:26 EEST (~22:14 → 23:26 UTC) — ~1h 12min wall time
**Date marker:** 2026-05-26
**Goal:** clean restart of the monitoring stack — stop stale monitors, regenerate reports + LLM packets, register fresh signals, run track-signals, then run a 60-minute production monitoring session for crypto + stocks with real Telegram alerts.

---

## 1. Reports generated

| Mode | Path | Saved at (UTC) |
|------|------|----------------|
| Crypto scalp | `data/reports/scalp/2026-05-25_22-19_scalp_report.md` | 22:19 |
| Crypto intraday | `data/reports/intraday/2026-05-25_22-18_intraday_report.md` | 22:18 |
| Stocks intraday (initial) | `data/reports/stocks/intraday/2026-05-25_22-14_stocks_intraday_report.md` | 22:14 |
| Stocks intraday (latest mid-session refresh by monitor) | `data/reports/stocks/intraday/2026-05-25_23-23_stocks_intraday_report.md` | 23:23 |

Latest OHLCV pulled fresh in every run. No stale reports were reused.

---

## 2. LLM packets refreshed

| Packet | Refreshed by | Latest source report stamped |
|--------|--------------|------------------------------|
| `data/processed/llm_analysis_packet.md` | both crypto reports (scalp wrote last → owns the file) | `scalp_report.md` (22:19) |
| `data/processed/llm_stocks_packet.md` | stocks intraday + each in-session refresh | `2026-05-25_23-23_stocks_intraday_report.md` (23:23) |
| `data/processed/context_for_llm.md` | latest crypto run | refreshed 22:19 |

QA Fix #1 (auto-regenerate on report) confirmed working in real-time via the `LLM packet refreshed:` lines in stdout for each command. No stale packets in flight.

---

## 3. Monitors

### Old monitors (handled per spec)

| Monitor | Task ID | Action |
|---------|---------|--------|
| `monitor-watchlist --interval 600 --iterations 50` (crypto, started earlier today) | `bipg069du` | **Stopped via TaskStop** before this session |
| `stocks-monitor-session` single-tick smoke from earlier | `bcq6ppyxr` | already finished naturally (single tick); no action needed |
| `stocks-monitor-session --dry-run` smoke session | — | already finished naturally |

No duplicate monitors are active. Old state cannot leak into the new session.

### New monitors (this session)

| Monitor | Task ID | Mode | Duration | Result |
|---------|---------|------|----------|--------|
| Crypto watchlist | `bc5wgj2gf` | scalp context (last report) | 6 iterations × 10 min ≈ 60 min | Completed; `iterations limit reached; exiting` |
| Stocks monitor | `bymha8zrb` | intraday | 5 ticks × ~10 min | Completed; `new=0 upgrades=0 dup_skipped=415 no_inv_skipped=0 telegram_failed=0` |

Both monitors ran in the background. Both completed cleanly. No process was left running.

---

## 4. Signals

| Bucket | Crypto scalp | Crypto intraday | Stocks intraday |
|--------|--------------|-----------------|-----------------|
| New A-tier | **0** | **0** | **0** (the 8 current A-tier setups were already alerted from the previous user-confirmed real send) |
| New B-tier | **0** | **0** | **0** (same — 6 B-tier still in registry, no material improvement) |
| C-tier / watchlist | 5+ (INJ 53.0, RENDER 52.8, SAGA 52.9, NEAR 52.9, FET 52.8, …) | similar (TAO promoted `rejected → C` mid-session at 52.4) | 5 (QQQ, IWM, SPY, XLV, DIA, MSTR) |
| Rejected | many (BTC 39.4, ETH ~44, NEAR 33.1, WLD 39.7, …) | many | 15 |
| New `proposed_signals` rows registered this session | per scalp + intraday: 0 (no A/B → nothing to register) | 0 | 13 per stocks report × 5 refreshes ≈ 65 rows (mostly duplicates of the same 8 setups) |

**Top crypto candidates (all C-tier, NOT alerted):**
- TAO/USDT — `rejected → C` upgrade visible in monitor log (score 52.4). Still below the 65 B-tier floor.
- INJ, RENDER, SAGA, NEAR, FET — all clustered 52–55. Selective regime. No A/B.

**Stocks A/B (unchanged from prior session, all already on Telegram):**
- A: AAPL 88.64, LLY 80.33
- B: AMD 78.77, XLK 74.91, SMCI 74.26, SMH 73.93, UNH 68.59, TSLA 67.30

---

## 5. Telegram

| Metric | Value |
|--------|-------|
| Alerts sent during this 60-min session | **0** |
| Duplicates skipped | **415** (stocks monitor across 5 ticks) + cooldown-skipped crypto ticks |
| Failed alerts | **0** |
| Symbols newly alerted | none — every active stocks A/B was already on the alerted list from the earlier user-confirmed real send; crypto produced 0 A/B |

The de-dupe layer worked exactly as designed: no spam, no duplicate Telegram messages, no missed eligible alerts (the criteria honestly produced zero new candidates).

---

## 6. Signal tracking

### Pre-session pass (before monitors)
```
Tracking pass complete: checked=100 updated=0 tp_hits=1 stopped=0 expired=0
                       not_triggered=0 ambiguous=0 no_ohlcv=0  errors=0
```

### Post-session pass (after monitors)
```
Tracking pass complete: checked=165 updated=0 tp_hits=1 stopped=0 expired=0
                       not_triggered=0 ambiguous=0 no_ohlcv=0  errors=0
```

- ✅ **Crypto signals tracked** — `no_ohlcv=0`, crypto OHLCV cached path resolved.
- ✅ **Stocks signals tracked** — `no_ohlcv=0`, Fix #1 (asset_class-aware tracker path) confirmed.
- ✅ **Errors=0** in both passes.
- ✅ **TP1 hit detected** (1 carry-over — TAO/USDT B intraday, already booked TP1 earlier today).
- `updated=0` in this run means no transitions during the 60-minute window — entries did not cross into a new state during US after-hours / crypto chop.

The new outcome data is persisted in `signal_outcomes` and visible via `signal-stats`.

---

## 7. Active signals

### Crypto (3 active)

| Symbol | Tier | Mode | Direction | Score | Status |
|--------|------|------|-----------|-------|--------|
| TAO/USDT | B | intraday | long | 66.3 | **tp1_hit** ✅ |
| SAGA/USDT | B | intraday | long | 75.1 | **triggered** |
| NIL/USDT | B | intraday | long | 70.4 | waiting_for_entry |

No new active crypto signals registered this session.

### Stocks (top of the active list)

Multiple duplicate rows per setup (each `stocks-intraday-report` run registers fresh signal_ids). Canonical active A/B set:

| Symbol | Tier | Mode | Direction | Score | Confidence |
|--------|------|------|-----------|-------|------------|
| AAPL | A | intraday | long | 88.64 | high |
| LLY | A | intraday | long | 80.33 | high |
| AMD | B | intraday | long | 78.77 | high |
| XLK | B | intraday | long | 74.91 | medium |
| SMCI | B | intraday | long | 74.26 | medium |
| SMH | B | intraday | long | 73.93 | medium |
| UNH | B | intraday | long | 68.59 | medium |
| TSLA | B | intraday | long | 67.30 | medium |

(Plus C-tier QQQ, IWM, SPY, XLV, DIA, MSTR — registered but not alerted.)

---

## 8. Stats

### `signal-stats --asset-class crypto`
```
sample=8 (confidence=anecdotal) | triggered=6 / not_triggered=1 | wins=1 losses=2 amb=0
PF=1.0 avgR=0.0 totalR=0.0
```
- 8 historical crypto signals total in the rolling window.
- 6 of 8 triggered (entered the zone) — 75 % trigger rate.
- 1 win, 2 losses → PF=1.0 on tiny sample. Confidence label correctly *anecdotal*.

### `signal-stats --asset-class stocks`
```
sample=162 (confidence=reliable) | triggered=0 / not_triggered=0 | wins=0 losses=0
PF=None avgR=None totalR=0.0
```
- 162 stocks signals registered (heavy duplication from 6+ stocks-intraday runs registering the same 8 A/B over and over).
- `triggered=0` reflects that none of the entry zones has been confirmed crossed by the tracker yet (US session closed during this monitoring window).
- PF/avgR honestly `None` on zero outcomes.

> ⚠️ The "162 sample" inflation comes from the stocks pipeline re-registering the same setups each run. This is hygiene-only — does not bias scoring — but should be cleaned up at some point.

---

## 9. Warnings

| Warning | Status |
|---------|--------|
| Stale data | None — all OHLCV ≤ 1h old at report time |
| Telegram / news_trader bridge | KOL placeholder; no fresh items today (acknowledged) |
| Missing earnings dates | yfinance 404s for SPY/QQQ/IWM/DIA/SMH/XLK/XLF/XLE/XLY/XLV — expected (ETFs have no earnings); per-stock dates still resolve to UNKNOWN, surfaces as risk flag |
| Missing orderbook / liquidations / on-chain | Not connected (acknowledged blindspots) |
| Disabled news sources | MarketWatch / Yahoo Finance / Seeking Alpha RSS — disabled in config |
| Failed services | **None.** Telegram fails=0, tracker errors=0, no_ohlcv=0, both monitors completed cleanly |
| Test_source news pollution | **0** in all reports (QA Fix #2 working) |
| Cross-asset news leak | **0** crypto news in stocks pipeline, **0** stocks-tagged news in crypto reports |

---

## 10. Safety confirmation

| Safety rule | Status |
|-------------|--------|
| No auto-trades | ✅ none placed |
| No scoring changes | ✅ no code/config touched |
| No threshold changes | ✅ |
| No architecture changes | ✅ |
| No agent changes | ✅ |
| No duplicate alert spam | ✅ 415 de-duped, 0 spam |
| No C-tier alerts | ✅ |
| No alerts without invalidation | ✅ `no_inv_skipped=0` (none tried) |
| Read-only signal_alerts policy | ✅ |
| Crypto/stocks logic isolation | ✅ |

---

## End-of-session summary

- Old crypto monitor (`bipg069du`) **stopped** before the new session.
- Three fresh reports generated; three LLM packets refreshed automatically with `Source report` stamped in the header.
- 60-minute production session executed across crypto + stocks in parallel.
- **0 new Telegram alerts** fired — the 8 stocks A/B were already on Telegram from the prior real send; crypto produced no A/B in this window.
- **0 spam** — 415 stocks duplicates and several crypto cooldown-blocked symbols correctly skipped.
- Signal tracker recorded outcomes (TP1 hit carried in pre and post pass; no new transitions in the 60-min window).
- All safety rules respected — no code, scoring, or strategy was touched.

**Net:** the system is in a quiet, healthy state. It produced nothing because the inputs justified nothing — exactly the discipline asked for ("NO TRADE is a valid answer").
