# Short Squeeze / Scam-Wick Risk Table (READ-ONLY)

Window: last 48h crypto shorts. Metrics from cached 15m OHLCV at/around entry.
`distEMA20` in ATR (negative = below mean); `1h%` = 15m×4 return at entry;
`uw/atr` = upper-wick ÷ ATR over last 48 candles; `stop/ATR` = stop distance in
ATR; `stop/p90wick` = stop distance ÷ 90th-pctile upper wick (>1 = stop outside
normal wick noise). No live-logic change.

| symbol | mode | 24h vol $M | vol_ratio | ATR% | 24h% | 4h% | **1h%** | distEMA20 | avg uw/atr | **max uw/atr** | stop/ATR | stop/p90wick | wick-only stop | hit TP1 after stop | class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **SAHARA** | scalp | **5.4** | 0.86 | 0.48 | −7.5 | −1.0 | −0.8 | −1.80 | 0.25 | 1.09 | +2.54 | 2.8 | No | **Yes** | near-miss → squeeze |
| **OPG** | intraday | **6.2** | 0.78 | 2.48 | −2.4 | −6.7 | **−4.0** | −1.51 | 0.24 | 1.67 | +1.25 | 3.8 | Yes | No | late breakdown chase |
| **BCH** | intraday | 84.8 | 0.64 | 1.56 | −7.5 | −0.4 | **+2.2** | +0.39 | 0.20 | 0.64 | +1.34 | 4.2 | No | No | short into bounce |
| **GPS** | scalp | 14.8 | 0.73 | 2.90 | **−20.4** | +2.1 | **+6.4** | +0.39 | 0.23 | 1.09 | +2.10 | 2.4 | (expired) | — | bounce after crash |
| **DEXE** | scalp | **9.2** | **2.10** | 1.73 | −12.8 | +1.7 | **+6.4** | +1.25 | 0.23 | **2.01** | +1.92 | 3.8 | Yes | No | squeeze (vol spike) |
| ETH | scalp | 1237.7 | 1.41 | 0.67 | −6.4 | −2.3 | −0.9 | −1.98 | 0.17 | 0.63 | +2.26 | 4.5 | (expired) | — | near-miss, flat |
| NEAR | scalp | — | — | 2.02 | −17.0 | +1.9 | +1.5 | +0.84 | 0.23 | 0.68 | +1.75 | 3.5 | (waiting) | — | not triggered |

## Read of the table
- **Thin liquidity is the common thread of the losers:** SAHARA $5.4M, OPG
  $6.2M, DEXE $9.2M, GPS $14.8M — all sub-$15M 24h quote volume → squeeze-prone.
  BCH is liquid but its breakdown ran on **contracting** volume (0.64×). ETH
  (the only deep-liquidity name, $1.2B) is the only one that did **not** lose.
- **Most losers were shorted into a BOUNCE:** BCH +2.2%, DEXE +6.4%, GPS +6.4%
  on the 1h at entry; DEXE/BCH were even **above** their EMA20 (distEMA20 +1.25 /
  +0.39) — i.e. price had already bounced when the short fired.
- **DEXE = textbook squeeze:** thin ($9M) + already −12.8% on 24h + bouncing
  +6.4% 1h + **2.10× volume spike** + **max upper wick 2.0× ATR** → shorted
  straight into an upward squeeze candle.
- **Stops were NOT too tight:** every stop sat **2.4–4.5×** the 90th-pctile
  upper wick and **1.25–2.54 ATR** away. SAHARA's stop was breached by a real
  candle **close** (not a wick). Widening stops would not have rescued OPG/BCH/
  DEXE (they never reached TP1 after stopping).
- **Only SAHARA was "right but stopped"** (hit_tp1_after_stop = Yes): it was a
  correct thesis squeezed out first. The other three losses were genuinely
  wrong-side/late (price bounced and did not return to TP1).
