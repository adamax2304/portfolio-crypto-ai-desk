# Crypto Signals — 12h Outcome Audit (READ-ONLY)

**Window:** last ~14h. Unique setups (deduped by signal_id, latest outcome).
**All crypto signals this window are B-tier** (no A-tier — correct in a
bearish/danger regime). Long + short both present. Every B alert has a backing
`proposed_signal` (untracked-legacy detector: **None**) ✅.

## A/B headline (week, signal-stats)
`A/B: n=45 PF 1.25 avgR +0.10 totalR +4 winrate 27.5% (stronger)` · C-tier n=0.
Marginally positive — small sample.

## B-tier signals (14h) — outcome table
| time(UTC) | symbol | mode | dir | score | status | R | mfe | mae | regime |
|---|---|---|---|---|---|---|---|---|---|
| 06-03 14:37 | NEAR | intraday | long | 65.3 | stopped | −1 | 0.90 | −1.25 | — |
| 06-03 14:48 | EPIC | intraday | long | 65.8 | stopped | −1 | 0.00 | −1.03 | — |
| 06-03 15:58 | ONDO | scalp | long | 65.6 | expired | 0 | 0.37 | −0.67 | — |
| 06-03 16:17 | ZRO | scalp | long | 65.0 | **tp1** | **+1** | 1.45 | −0.22 | — |
| 06-03 16:47 | XPL | scalp | long | 65.0 | **tp2** | **+2** | 2.81 | −0.28 | — |
| 06-03 18:18 | **SAHARA** | scalp | **short** | 67.8 | stopped | −1 | 0.84 | −1.32 | bearish |
| 06-03 19:28 | ZRO | intraday | long | 65.0 | **tp2** | **+2** | 2.22 | −2.02 | — |
| 06-03 20:57 | ENA | intraday | long | 65.2 | stopped | −1 | 0.26 | −1.37 | — |
| 06-03 23:57 | OPN | scalp | long | 67.5 | stopped | −1 | 0.38 | −1.15 | — |
| 06-04 00:04 | SUSHI | scalp | long | 67.2 | stopped | −1 | 0.20 | −1.27 | range/chop |
| 06-04 00:27 | SUSHI | intraday | long | 65.6 | stopped | −1 | 0.69 | −1.57 | — |
| 06-04 00:47 | ENA | intraday | long | 67.2 | stopped | −1 | 0.59 | −2.11 | — |
| 06-04 02:36 | BCH | intraday | **short** | 65.2 | stopped | −1 | 0.09 | −1.19 | — |
| 06-04 02:36 | OPG | intraday | **short** | 65.5 | stopped | −1 | 0.03 | −0.94 | — |
| 06-04 02:51 | GPS | scalp | **short** | 65.7 | expired | 0 | 0.18 | −0.36 | bearish |
| 06-04 02:58 | C | scalp | long | 68.2 | **tp1** | **+1** | 1.74 | −0.06 | — |
| 06-04 02:58 | EPIC | scalp | long | 66.0 | **win** | **+1** | 1.38 | −0.43 | — |
| 06-04 05:46 | DEXE | scalp | **short** | 65.9 | stopped | −1 | 0.07 | −1.05 | danger |
| (waiting/expired) | WLD, STO, OPN, ETH(short) | mixed | | | open/expired | 0 | | | |

## Wins vs losses
- **Wins (5):** ZRO ×2 (+1, +2), XPL (+2), C (+1), EPIC scalp (+1) → the
  **RS-leader longs that the funnel/RS-leader fix enabled produced the winners.**
- **Losses (≈10 stopped):** NEAR, EPIC(intraday), ENA ×2, OPN, SUSHI ×2, BCH(s),
  OPG(s), DEXE(s), SAHARA(s).
- **Expired flat (≈5):** ONDO, WLD ×2, STO, GPS(s), OPN.

## Fix verification
- **Funnel / RS-leader longs:** ✅ NEAR/EPIC/ONDO/ZRO/XPL all appeared,
  registered, tracked, alerted. ZRO/XPL/C/EPIC were the net winners.
- **Short side:** ✅ SAHARA, BCH, OPG, DEXE, GPS, ETH shorts generated,
  registered in `proposed_signals`, alerted. **But shorts went 0 wins / 4 stops
  / 2 expired this window** — see below.
- **Long vs short separated in stats:** ✅ (signal-stats `by direction`).

## Why losers lost (classified)
1. **Counter-tape / chop whipsaw (primary):** most stopped longs had
   **MFE < 1R** (NEAR 0.90, SUSHI 0.69, ENA 0.59 — went part-way to TP1 then
   reversed) in `range/chop` / `high-volatility danger`. Stops sit ~1.0–1.2 ATR
   from entry while ATR-percentile is **98–100**, so normal noise reaches the
   stop. → stop-in-noise + counter-tape entries.
2. **Shorts late/exhaustion:** SAHARA short MFE 0.84 then squeezed; BCH/OPG/DEXE
   shorts MFE ~0.0–0.09 (entered after the down-move, immediate adverse) —
   late-short into already-extended drops.
3. **ENA −2.11 MAE:** invalidation too wide / volatility spike (not stop-too-tight
   — opposite: it ran −2R before final).
4. **Not a registration/data failure** — all tracked correctly.

## Specifically requested
- **SAHARA short:** stopped −1 (MFE 0.84 → squeeze). Tape-aligned but late.
- **NEAR/EPIC/ONDO/ZRO/XPL:** ZRO+XPL+EPIC(scalp) won; NEAR+EPIC(intraday) lost;
  ONDO expired. Net RS-leader longs ≈ break-even-to-positive.
- **Missed shorts:** none obvious missed; shorts fired but underperformed.
- **No-trade periods:** the 12:42 cycle produced **zero** fresh A/B crypto setups
  (danger regime, breadth 22.9%) — correct risk-off behavior.

## Net
Crypto A/B ≈ **+4R, PF 1.25** over the week — the fixes (funnel, RS-leader,
shorts, registration) **work mechanically**; profitability is thin because the
regime is bearish/danger and counter-tape longs + late shorts get whipsawed.
**No logic change recommended yet** — small sample, behavior is regime-appropriate.
