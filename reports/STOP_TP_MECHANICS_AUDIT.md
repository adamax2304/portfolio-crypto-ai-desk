# Stop / TP Mechanics — 12h Audit (READ-ONLY)

Method: for each stopped/loss signal use the tracked **MFE_R** (max favorable
excursion) and **MAE_R** (max adverse) to infer post-entry behavior.
Heuristic: MFE ≥ ~0.8R but final = −1R ⇒ price went **most of the way to TP1
then reversed into the stop** (candidate "stop-too-tight / TP-not-reached").
MFE ≈ 0 ⇒ price went **immediately adverse** (entry on wrong side / stale data,
stop was correct).

## Crypto stopped (13)
| symbol | dir | mfe | mae | reading |
|---|---|---|---|---|
| NEAR | long | 0.90 | −1.25 | near-miss: went +0.9R then reversed → stop a touch tight / TP1 just out of reach |
| SAHARA | short | 0.84 | −1.32 | near-miss then squeeze |
| SUSHI(intra) | long | 0.69 | −1.57 | partial then reversed |
| ENA(00:47) | long | 0.59 | −2.11 | partial; **very wide adverse** (not tight) |
| WLD(intra) | long | 0.42 | −1.08 | mid |
| OPN(scalp) | long | 0.38 | −1.15 | mid |
| ENA(20:57) | long | 0.26 | −1.37 | shallow favorable |
| SUSHI(scalp) | long | 0.20 | −1.27 | shallow |
| GPS/BCH/OPG/DEXE | short | ~0.0–0.18 | −0.9 to −1.2 | **immediate adverse** — late shorts, stop correct |
| EPIC(intra) | long | 0.00 | −1.03 | immediate adverse — stop correct |

## Stocks stopped (≈15)
| symbol | tier | mfe | mae | reading |
|---|---|---|---|---|
| SMH | B | 0.48 | −1.37 | partial |
| AAPL(A 13:46) | A | 0.40 | −1.11 | partial |
| NVDA | B | 0.23 | −1.16 | shallow |
| AAPL(B 01:06) | B | 0.17 | −1.05 | shallow / overnight |
| AMD | B | 0.12 | −1.32 | shallow / overnight |
| TSLA | B | 0.12 | −1.07 | shallow |
| SMCI(A/B) | A/B | **0.00** | −1.34 | immediate adverse (overnight + legal) |
| SMH/SPY/DIA(C) | C | 0.00 | −1.1..−1.4 | immediate adverse — overnight stale |

## Grouping
- **Stop correctly protected (MFE ≈ 0, immediate adverse):** crypto late shorts
  (BCH/OPG/DEXE/GPS), EPIC intraday; stocks SMCI + the 01:06 overnight cluster.
  These were **right to stop** — entries were on the wrong side / stale data.
- **Stop a touch tight / TP1 just out of reach (MFE 0.6–0.9R, final −1R):**
  crypto NEAR (0.90), SAHARA (0.84), SUSHI (0.69), ENA (0.59). A handful of
  near-misses — but all in `range/chop` / `high-volatility danger` where ATR
  noise ≈ the stop distance. **Not a systematic stop-width bug**; it's the
  regime.
- **TP too ambitious:** not the main pattern — winners (ZRO +2, XPL +2, C/EPIC
  +1) reached TP cleanly with MFE 1.4–2.8R, so TP placement is fine when the
  move is real.
- **Invalidation too wide:** ENA MAE −2.11 / ZRO MAE −2.02 — a few setups let
  price run **beyond −1R adverse** before resolving (ZRO still won). Wide-stop
  outliers, not tight-stop.
- **Entry too late:** crypto shorts (BCH/OPG/DEXE, MFE≈0) entered after the drop.
- **Expiry too short:** several flat-expired (ONDO, WLD, OPN, GPS, STO) — moved
  <1R either way inside the validity window; acceptable (no loss).
- **Data unavailable / stale:** the stocks 01:06 UTC cluster — signals built on
  after-hours/stale prices while the US market was closed (the dominant stocks
  loss driver).

## Conclusion
- Crypto stops are **mostly correct**; the losses are **regime (chop/danger)
  whipsaw + late shorts**, with a *minority* of ~0.8R near-misses. **Do NOT
  widen stops generically** — it would worsen the immediate-adverse majority.
- Stocks stops are **correct**; the real defect is **generating intraday stock
  signals on stale, market-closed prices** (overnight cluster) and the **AVGO
  stale-pre-earnings entry** — both data/timing issues, not stop/TP geometry.
- **No stop/TP geometry change recommended.** The actionable fixes are
  upstream (don't issue/hold intraday stock entries while the cash session is
  closed; block stale post-earnings setups).
