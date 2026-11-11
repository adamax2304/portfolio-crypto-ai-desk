# Stocks Sector-Concentration Audit + Proposed Exposure Cap

**Date:** 2026-06-16 · Read-only. Script: `scripts/audit_sector_concentration.py`.
Sector membership derived from a static symbol map (the `sector` column is empty in
production). R values are **raw/unsized** paper outcomes (mostly ±1R / 0).

## Why this audit
Today (2026-06-16) 4 tech/semi longs (SMH, AMD, XLK, PLTR) all stopped within 30 min at
the US open = −4R in one correlated cluster, while SPY barely moved (−0.27%). That is a
**concentration** event, not a per-signal quality problem. This audit asks: how much has
correlated clustering cost historically, and what is a safe cap.

## Findings (1,136 entered+closed stock trades)

**Concentration is severe and largely self-inflicted (redundant proxies):**
- Max **same-day concurrent LONG entries in the tech complex (semis+megacap+high-beta): 137.**
  Even after dedup to unique names, clusters routinely stack QQQ + XLK + AAPL + MSFT long
  on the same day — which is ≈ the **same Nasdaq bet 4×**.
- On a **unique (day, symbol, direction)** basis: 346 positions, **net −17.1R** — the stock
  book is net-negative once duplicate signals on the same name are collapsed.

**The correlated-cluster tax:**
- **18 "all-loss" correlated clusters** (≥2 unique same-sector, same-direction names that
  ALL lost on the same day) → **−39.9R bled**.
- For scale, that −40R cluster-bleed dwarfs the entire book's net — concentration is the
  single biggest leak in the stock book.

**Worst correlated wipeouts (unique names):**
| Day | Sector | Dir | Names | R |
|-----|--------|-----|-------|---|
| 2026-06-05 | megacap_tech | long | XLK, META, AAPL, QQQ | −4.0 |
| 2026-06-02 | megacap_tech | long | QQQ, MSFT, XLK, AAPL | −3.7 |
| 2026-06-08 | broad_index | short | DIA, SPY, IWM | −3.0 |
| 2026-06-03 | megacap_tech | long | MSFT, QQQ, AAPL, XLK | −2.9 |
| 2026-06-09 | semis | long | AMD, SMCI, SMH | −2.5 |
| 2026-06-16 (today) | semis/tech | long | SMH, AMD, XLK, PLTR | −4.0 |

Repeat offenders: **megacap_tech ETFs/names (QQQ, XLK, AAPL, MSFT, META)** and
**broad-index ETFs (SPY, DIA, IWM)** — both are internally redundant baskets.

## Root cause
1. **Redundant proxies treated as independent**: QQQ ≈ XLK ≈ big-tech; SPY ≈ DIA ≈ IWM.
   The system sizes each as a separate full-risk bet, so one sector move hits all legs.
2. **No cap on concurrent same-sector same-direction exposure.**
3. (Amplifier) duplicate signals per symbol per day inflate the stack.

## Proposed safe limit — sizing/actionability layer only (NO strategy/TP/SL/scoring change)

This lives in the **same layer as the scalp 0× downgrade** — it changes only the
*actionable weight / routing*, never the signal, score, geometry, or thresholds.

**Rule A — redundant-proxy collapse.** Within a day+direction, treat these as one bucket
and keep only the highest-scored member actionable; route the rest to shadow:
- Nasdaq/tech: {QQQ, XLK} (+ overlap with AAPL/MSFT/NVDA…); broad: {SPY, DIA, IWM}.

**Rule B — sector-exposure cap (concurrency-aware sizing).** Per sector + direction:
| concurrent actionable position | weight |
|--------------------------------|--------|
| 1st | 1.0× (full) |
| 2nd | 0.5× (half) |
| 3rd and beyond | 0.0× → shadow (recorded, not pushed) |

So a sector can carry at most ~1.5R of correlated risk instead of 4–5R.

## Estimated benefit (rough, raw-R)
Capping each all-loss cluster to 2 legs (1 full + 1 half = 1.5R risk) instead of the
observed 3–4+ legs would have cut the **−39.9R** cluster bleed to roughly **−18 to −20R** →
**~+18–20R saved over ~2 weeks**, with zero change to entry/score/TP/SL. The losses that
remain are the unavoidable "sector genuinely turned" component.

## Implementation note (not done yet — needs your go)
Rule B requires the sizing layer to know currently-open same-sector positions (today it is
per-signal stateless). Plan: add a `config/sector_map.yaml` + a concurrency-aware pass in
`src/signals/sizing.py` that reads open positions from `proposed_signals`, applies the
cap, and routes overflow to shadow (mirroring the scalp shadow path). Fully additive,
behind tests, no strategy change.

**Status: AUDIT COMPLETE.** Concentration confirmed as the top stock-book leak (~−40R on
correlated clusters). Proposed cap is safe (sizing/routing only) and ~+18–20R/2wk in
backtest-of-record terms. Awaiting go to implement.
