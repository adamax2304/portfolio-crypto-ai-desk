# Technical Analysis Audit — 2026-05-25

Idea-by-idea, is the technical setup actually valid? Are entries, stops, and TPs on real levels?

For each idea: `entry → invalidation → TP1/2/3 → R:R → verdict`. **The user must verify on a chart before acting.**

---

## CRYPTO SCALP / INTRADAY — Watchlist

### NIL/USDT (long, watch)
- **Current price**: 0.0801 (scalp report)
- **Conditional entry zone**: 0.0769–0.0791 (pullback)
- **Invalidation**: 1h close beyond 0.0727
- **TP1**: 0.0851 (R:R 1.31) / **TP2**: 0.0900 / **TP3**: 0.0949
- **Support**: 0.0734 / **Resistance**: 0.0899 / **ATR**: 0.0049
- **Entry vs noise**: entry zone is below current price and above support (0.0734) — valid pullback structure.
- **Stop vs wick**: invalidation 0.0727 is below the 0.0734 support — modest buffer (0.0007 = ~1 ATR/7). **Tight for a scalp**, may be wicked out on a fast retest.
- **R:R**: TP1 R:R 1.31 — **below the 1.5 floor the system uses to reject in stocks**. Crypto C-tier accepts it; if elevated to active, this would be borderline.
- **Volume confirm**: 1.16x — **weak**.
- **Verdict**: **acceptable as watchlist**; do not activate without volume > 1.5x and a clean 0.0769–0.0791 retest hold.

### SAHARA/USDT (long, watch)
- **Current**: 0.0358; **entry**: 0.0352–0.0356; **inv**: 0.0348; **TP1**: 0.0366 (R:R 1.84) / TP2 0.0374 / TP3 0.0382.
- **ATR**: 0.0008. Stop 0.0348 is **only 0.0008 below entry** — exactly 1 ATR. **Very tight**.
- **Support 0.0339 / Resistance 0.0364** — entry sits inside the range.
- **Verdict**: **weak** — entry zone is too close to invalidation; expect frequent stop hits on noise. Skip unless 5m structure confirms a clear higher-low.

### BSB/USDT (short, watch)
- **Current**: 0.9641; **entry zone**: 0.9770–1.006 (failed bounce / retest of breakdown); **inv**: 1.042; **TP1**: 0.8994 (R:R 1.84) / TP2 0.8346 / TP3 0.7699.
- **ATR**: 0.0647. Stop is 1 ATR above entry midpoint — **structurally OK**.
- **MEXC-only** — caution.
- **Derivatives**: OI +13.77% while price down → fresh shorts pressing → **possible squeeze if it reclaims**. The setup is essentially a fade of any bounce, which can be brutal if MEXC liquidity spikes.
- **Verdict**: **good structure but venue risk** — MEXC-only short on a "fresh shorts pressing" tape is exactly the kind of crowded trade that gets squeezed. Skip unless confirmed by a clean failure on a higher venue.

### TAO/USDT (long, watch)
- **Current**: 278.50; **entry**: 276.68–277.94; **inv**: 275.13; **TP1**: 281.31 (R:R 1.84) / TP2 284.11 / TP3 286.92.
- **ATR**: 2.807. Stop 275.13 is ~1.2 ATR below entry midpoint — **OK**.
- **R:R to TP1 only 1.84R, but TP1 is only ~3 above entry — small absolute move** — execution tax matters.
- **Volume**: 1.23x, weak.
- **Verdict**: **acceptable for tiny size**; the move is small and the catalyst is generic AI heat. Not a high-conviction watch.

### LTC/USDT (short, watch)
- **Current**: 52.820; **entry**: 52.866–52.971; **inv**: 53.155; **TP1**: 52.588 (R:R 1.4) / TP2 52.356 / TP3 52.124.
- **ATR**: 0.232. Entry zone is **above current price** — this is a "wait for it to come up and fail" trade.
- **Stop only 0.18 above entry midpoint — less than 1 ATR** — **too tight**.
- **Counter-trend** (BTC transition_up).
- **Verdict**: **weak**. Tight stop + counter-trend + small target = high churn risk. **Recommend skip**.

---

## STOCKS INTRADAY — A/B-tier ideas

### AAPL (long, A, 88.64)
- **Entry**: 308.04–308.88 / **Inv**: 306.35 / **TP1**: 311.41 / TP2 313.10 / TP3 315.64
- **R:R to TP1**: stated 1.0 (system flagged "RR to TP1 below 1.5")
- **Stop vs noise**: 306.35 is ~1.7 below entry midpoint. With AAPL's typical 1.5–2.5 intraday ATR, this is **borderline tight**.
- **TP1 only 3 above entry** — for a $308 stock, a 1% target. Reasonable scalp into resistance, but R:R 1.0 means you need 50%+ hit-rate to break even.
- **Verdict**: **acceptable as scalp, weak as A-tier**. The score 88.64 implies confidence; the R:R 1.0 implies low edge per trade. User should size accordingly.
- **Manual check**: prior day high, opening range, news (real buyback or test fixture? — confirm).

### LLY (long, A, 80.33)
- **Entry**: 1060.83–1065.65 / **Inv**: 1051.18 / **TP1**: 1080.12 / TP2 1089.77 / TP3 1104.24
- Spread: ~$5 entry zone, ~$10 to stop, ~$15 to TP1 → **R:R ~1.5–1.8 if entered at the bottom of zone**.
- **Verdict**: **good**. LLY is a known low-vol leader; this is a clean retest-and-go structure.
- **Manual check**: LLY 1h chart for prior swing low at 1051, and any pharma sector news.

### AMD (long, B, 78.77)
- **Entry**: 463.37–467.51 / **Inv**: 455.09 / **TP1**: 479.93 / TP2 488.21 / TP3 500.63
- Entry spread is wide (~$4), stop ~$10 below entry, TP1 ~$13 above → **R:R ~1.0–1.3** — system flagged "below 1.5". Demotes to B.
- **Verdict**: **acceptable**. Reflects an extended move. Wait for retest into 463 or skip.
- **Manual check**: AMD has been an RS leader (+30% vs SPY). Watch for blow-off vs continuation.

### XLK (long, B, 74.91)
- **Entry**: 179.75–180.34 / **Inv**: 178.57 / **TP1**: 182.11 / TP2 183.29 / TP3 185.06
- Tiny moves: $0.6 entry zone, $1.5 stop, $1.8 TP1 → **R:R ~1.0** — ETF.
- **Verdict**: **acceptable as regime confirmation** but a 1% intraday ETF trade is execution-tax-heavy.

### SMCI (long, B, 74.26)
- **Entry**: 35.25–35.58 / **Inv**: 34.58 / **TP1**: 36.58 / TP2 37.24 / TP3 38.24
- SMCI is high-vol. Stop $0.6 below entry; TP1 $1.0 above. **R:R ~1.5–1.6** — borderline.
- **Verdict**: **acceptable** but stop is **tight for SMCI's 5–8% daily range**. Size down.

### SMH (long, B, 73.93)
- **Entry**: 573.42–575.99 / **Inv**: 568.28 / **TP1**: 583.70 / TP2 588.83 / TP3 596.54
- $2.5 entry zone, $7 stop, $8 TP1 → **R:R ~1.1**.
- **Verdict**: **acceptable as semi regime trade**.

### UNH (long, B, 68.59)
- **Entry**: 387.36–388.58 / **Inv**: 384.93 / **TP1**: 392.23 / TP2 394.67 / TP3 398.32
- $1.2 entry zone, $3.5 stop, $4 TP1 → **R:R ~1.1**.
- **Verdict**: **borderline**. UNH is RS=follower per the report. Lowest-conviction B-tier here.

### TSLA (long, B, 67.30)
- **Entry**: 423.33–425.95 / **Inv**: 418.09 / **TP1**: 433.81 / TP2 439.04 / TP3 446.90
- $2.6 entry zone, $7 stop, $10 TP1 → **R:R ~1.4**.
- **Important**: TSLA's evidence list **does not** include "above prev day high" (the other 7 ideas do). This is a structural weakness.
- **Verdict**: **slightly weak B**. Verify TSLA opening range and prior day high before treating as intraday long.

---

## Cross-cutting technical issues

### 1. **Entry zones are aggressive** for most stocks ideas
The entry midpoints sit just below or at current price. With the US session ~80 min in by report time, the price may already be at or above the zone. **The user must check current price vs zone before entry.**

### 2. **Stops are tight relative to ATR**
Several setups (SAHARA, LTC, SMCI, UNH) have stops within 1 ATR of entry. This produces frequent stop-outs in chop. The Weekend Mode overlay's "prefer structural / ATR stops" rule would catch this — but Weekend Mode is off today.

### 3. **R:R to TP1 ≤ 1.5 on every single B-tier stocks idea**
The system flagged this ("RR to TP1 below 1.5 (1.0)") on every idea but did not reject. The R:R cap acts as a soft signal in this regime, not a hard block. That is **inconsistent with** the explicit `rr_below_1.5` reject reason applied to JPM, XLF, XLY, PLTR, META longs. Why those get rejected and the B-tier names with the same R:R issue do not — unclear from the report. Possible code: the R:R rule is a tiebreaker, not a gate.

### 4. **Scalp execution requirement**
Scalp ideas should have a clear **5m or 1m trigger** ("buy on first higher-high after retest of 0.0791", e.g.). Today's scalp watchlist ideas describe pullback zones but **no explicit execution trigger**. The user has to interpret the zone.

### 5. **Intraday 15m/1h/4h structure**
Crypto intraday ideas reference 1h thesis + 15m execution. **No 4h context** in the per-idea evidence. For a 4–24h trade, a 4h structural read would help.

### 6. **No "What to Monitor" section in stocks ideas**
Crypto C-tier ideas all have "What To Monitor" bullets. Stocks A/B ideas do not. Hygiene gap.

---

## Verdict per idea

| Idea | Tech verdict | Reason | Manual check |
|------|--------------|--------|--------------|
| NIL crypto | Acceptable | Pullback structure but tight stop, weak volume | 0.0769–0.0791 retest hold + volume > 1.5x |
| SAHARA crypto | Weak | Stop too close to entry | Skip unless 5m higher-low confirmed |
| BSB crypto short | Acceptable but venue risk | MEXC-only short on shorts-pressing tape | Look for confirmation on Binance/Bybit |
| TAO crypto | Acceptable, tiny | Small absolute move, weak volume | Position size accordingly |
| LTC crypto short | Weak | Counter-trend + tight stop | Skip |
| AAPL stocks | Acceptable scalp | R:R 1.0 limits edge | Verify real buyback news + prior day high |
| LLY stocks | **Good** | Clean RS leader + sensible R:R | Pharma sector news + 1051 swing low |
| AMD stocks | Acceptable | Extended; wait for retest | 463 retest behavior |
| XLK stocks | Regime confirm | ETF, low edge | Treat as macro position, not trade |
| SMCI stocks | Acceptable | Stop tight for vol | Size down |
| SMH stocks | Regime confirm | ETF | Macro position |
| UNH stocks | Borderline | "Follower" RS, low R:R | Skip unless gives clean breakout |
| TSLA stocks | Weak | Missing "above prev day high" flag | Verify opening range manually |

**Bottom line**: only **LLY** stands out as a clean technical setup today. The rest range from acceptable scalps to borderline B-tiers that demand manual chart verification before any execution.
