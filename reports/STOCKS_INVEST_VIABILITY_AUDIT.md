# Stocks Invest — Viability Audit (PART 3)

**Date:** 2026-06-09 · **Scope:** Read-only. No code/strategy/TP/SL/routing touched.
**Sample window:** 14d (2026-05-26 → 2026-06-09). 94 deduped invest signals total (all tiers); 39 A/B.

## 1. Headline
| Tier | n | triggered | closed (W+L) | expired | not_triggered | pending | netR |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 2 | 2 | 0 | 2 | 0 | 0 | 0 |
| B | 37 | 35 | 7 | 28 | 2 | 0 | **−7** |
| C | 55 | 47 | 6 | 38 | 4 | 5 | −4 |
| **all** | **94** | **84** | **13** | **68** | **6** | **5** | **−11** |

A/B subset alone: **0W / 7L (WR 0%, netR −7)** across 7 closures over 14 days, against a 720h (30-day) validity window.

## 2. Sample size & horizon mismatch

- Validity window per signal: **720 h = 30 days** (uniform across all 94).
- Average trigger → expiry duration on the 83 signals with `entry_triggered_at`: **688.6 h ≈ 28.7 days**, min 559 h, max 731 h. The tracker is **NOT closing invest signals early**: when a signal expires it has run essentially its full 30-day window.
- But the 13 actual losses fired their stops within **1–6 days** of trigger (see §4). The thesis horizon (30 d) and the stop-out horizon (1–6 d) are decoupled: stops are tight enough that normal multi-week noise invalidates them well before the swing/invest thesis has time to play out.

## 3. MFE/MAE on expired signals

| Bucket | n | share |
|---|---:|---:|
| expired with MFE > 0 | 66 / 68 | 97% |
| expired with MFE ≥ 0.5R | 9 / 68 | 13% |
| expired with MFE ≥ 1.0R | **0 / 68** | **0%** |
| expired with MFE ≥ 2.0R | 0 / 68 | 0% |

Averages on expired: **MFE +0.24R, MAE −0.44R.** Invest signals never reach +1R favorable across the entire 30-day window — they grind sideways and time out near flat. That is the dominant outcome (68 of 84 triggered = 81%).

## 4. Loss anatomy

All 13 invest losses are **real stop hits** (`stop_hit=1`), not horizon-forced exits:

| created | symbol | tier | dir | hold before stop | R |
|---|---|---|---|---:|---:|
| 2026-06-03 | QQQ | C | long | 1.0 d | −1.0 |
| 2026-06-03 | SMCI | C | long | 1.0 d | −1.0 |
| 2026-06-03 | AVGO | C | long | 1.0 d | −1.0 |
| 2026-06-03 | XLK | B | long | 2.0 d | −1.0 |
| 2026-06-03 | SMH | B | long | 2.0 d | −1.0 |
| 2026-06-03 | SMCI | B | long | 2.0 d | −1.0 |
| 2026-06-03 | QQQ | B | long | 2.0 d | −1.0 |
| 2026-06-02 | AVGO | C | long | 1.0 d | −1.0 |
| 2026-06-02 | MSFT | B | long | 3.0 d | −1.0 |
| 2026-06-02 | XLK | B | long | 3.0 d | −1.0 |
| 2026-05-31 | AVGO | C | long | 4.0 d | −1.0 |
| 2026-05-31 | MSFT | B | long | 6.0 d | −1.0 |
| 2026-05-29 | TSLA | C | long | 4.0 d | −1.0 |

Median stop hold = **2 days**, max 6 days. The 30-day thesis horizon never gets a chance.

13/13 losses are LONGS in semiconductor/large-cap tech/QQQ/SMCI complex during the late-May → early-June tech weakness. The losses are concentrated in one tape sequence, not spread evenly across the period.

## 5. Slice cuts

### A vs B vs C
- **A-tier (2 signals)**: LLY A sc82, AAPL A sc81 — both triggered, both expired flat (MFE 0.20R/0.44R). Sample too small to judge A-tier on its own.
- **B-tier (37 signals)**: 0W/7L closed; 28 expired. All 7 losses inside the tech-long bucket above.
- **C-tier (55 signals)**: 2W/6L → but the 2 "wins" are in the wider 94-row set; in the strict A/B set there are 0 wins.

### ETF vs single-name
| Bucket | n | closed | W | L | netR |
|---|---:|---:|---:|---:|---:|
| ETF (XLK/SMH/QQQ/SPY/DIA/XLV/XLE) | 11 | 4 | 0 | 4 | −4 |
| single-name (AAPL/LLY/AMD/NVDA/MSFT/META/AVGO/SMCI/PLTR/UNH/...) | 28 | 3 | 0 | 3 | −3 |

Both segments produced 0 wins. ETF losses run with tech-sector ETFs, not broad SPY/DIA — broad ETFs only expired.

### News-supported
**Zero** invest signals carry `news_supported=1` over the 14d window. The earnings/catalyst path the invest mode is meant to lean on **is not being populated for invest at the signal layer**. Either:
- the invest pipeline doesn't compute `news_supported`, or
- the news matcher is keyed to short-horizon catalysts that don't fit 30-d theses.
This is an observability gap, not a routing problem.

### Direction
| dir | n | closed | W | L | netR |
|---|---:|---:|---:|---:|---:|
| long | 85 | 15 | 2 | 13 | −11 |
| short | 9 | 0 | 0 | 0 | 0 |

**All losses are longs.** 9 shorts were all flat-expired or pending; no decisive short result. The directional asymmetry mirrors the tape (late-May tech rally faded into selloff).

## 6. Does invest duplicate swing logic?

Looking at signals from the same date (2026-06-05T14:55 batch):
- META C sc 51 short (invest) — same direction call as the META swing/intraday B-shorts that won in the 2026-06-05 selloff.
- LLY/AAPL/AMD A-tier longs (invest) — same A-tier names that came out of stocks-swing (which has since been paused).

**Invest and swing share the same fundamental thesis path** (Tier-A names, multi-day hold, structural moves). The differences are validity window (720 h vs 168 h for swing) and signal volume cap. Functionally the modes overlap; invest acts as "swing with a longer leash."

Given stocks swing is paused for the same reason (12 W / 4 % WR over 14d) and these signals come from the same trade-idea pipeline → invest is likely inheriting the same systematic failure (over-eager A-tier long calls on tops), with the only difference being that the longer window converts most of those into "expired flat" instead of "stop-out".

## 7. Answers to the assessment questions

- **Sample size:** 7 A/B closures over 14 d, 13 closures (all losses) including C-tier. Numerically thin but **not insufficient to reject A-tier invest longs** — 13/13 LONG losses with median 2-day stop hold is a strong signal that the thesis structurally doesn't survive the immediate noise.
- **Average holding time:** triggered → expiry **688 h (28.7 d)**; triggered → stop **2.0 d (median)**. The two outcomes have radically different time scales.
- **Expiry logic:** the tracker is honoring the 30-day window; it is *not* closing invest signals too early.
- **Evaluation pace:** correct in timing terms. The mismatch is between stop placement (tight) and thesis horizon (long).
- **Stops/TPs appropriate for invest horizon:** **No.** Stops invalidate in 1–6 days while the favorable thesis would need weeks. This is a strategy/risk-design issue, not a tracker issue.
- **Losses from pre-fix stale/market-closed/earnings:** all 13 losses pre-date the 2026-06-05T19:00 stocks Telegram/swing fix. Of the 13, 7 are from the 2026-06-02 to 2026-06-03 tech long batch (the same batch that triggered the stocks-swing pause). Invest is currently caught in the same pre-fix tech-long failure mode that stocks-swing was.
- **A-tier overpromotion:** the 2 A-tier invest signals (LLY/AAPL) expired flat, not lost. No A-tier loss yet — but the A-tier overpromotion problem identified for stocks-swing applies by design here (same A-tier pipeline).
- **Duplicates swing logic:** **Yes** — same underlying trade-idea pipeline, differing only in validity window. See §6.
- **Stay active / watchlist / longer outcome window:** the longer outcome window already exists (30 d); the problem is the stop. With 0 A/B wins across 7 closures and 13/13 long losses, the *current* invest config is effectively the same broken-A-tier-long-bias that stocks-swing was paused for. Recommendation deferred to PART 6.

## Verdict for PART 3
Stocks invest is **NOT a tracker/horizon problem** — the 30-day window is honored. It is the **same systematic A/B-long failure mode that triggered the stocks-swing pause**, just spread out over a longer tape: stops fire in 1–6 days, the rest grind flat for 30 days with MFE < 1R. Sample is thin for hard rejection (7 A/B closures) but the loss anatomy is identical to the failed pre-pause swing batch (same tickers, same direction, same dates). **NEED_MORE_DATA verdict is appropriate for routing, but the working hypothesis should be "invest inherits the same swing problem".** Concrete recommendation in PART 6.
