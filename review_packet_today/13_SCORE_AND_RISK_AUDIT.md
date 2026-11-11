# Score and Risk Audit — 2026-05-25

For each final idea (or notable rejection) in today's three reports: is the score justified by the underlying evidence?

Score component banding observed in code: `market_regime, technical_setup, momentum, derivatives, catalyst_news, narrative, execution_quality` with a separate `risk_penalty` subtracted.

---

## CRYPTO SCALP — Watchlist (C-tier)

### NIL/USDT — 60.4
- Components: market_regime 8.7, technical_setup 13.6, momentum 14.1, derivatives 13.6, catalyst_news 5.4, narrative 3.4, execution_quality 7.9. Risk penalty: −6.3.
- **Real components**: momentum, derivatives (OI +35.7%), technical_setup.
- **Weak components**: catalyst_news (5.4) on `no fresh verified catalyst`. narrative 3.4 is generic — NIL is not a representative of any sector heatmap.
- **Hard caps**: not applied (anchor-listed on Binance + Bybit derivatives → no MEXC cap).
- **Verdict on score**: **reasonable**. The raw momentum (91.6) was correctly compressed by the low-volume penalty (1.16x) and the mixed regime. 60.4 is C-tier honest.

### SAHARA/USDT — 57.9
- Components: similar shape, derivatives only 9.9 (OI declining, short covering, weaker continuation).
- **Verdict**: **reasonable**. Short covering = weaker continuation is correctly priced down.

### BSB/USDT — 54.4 (short)
- Derivatives 12.0 (fresh shorts pressing, possible squeeze) — interesting setup logic.
- MEXC-only — exchange confirmation 38.0/100 — system **correctly capped** at C-tier.
- **Verdict**: **reasonable** but the system is willing to recommend a SHORT on a MEXC-only token. Manual sanity check before action.

### TAO/USDT — 52.6
- Narrative 2.9 (AI sector is the warmest at heat 43.5/100).
- Technical_setup 11.6 (setup quality 58.2/100 — borderline).
- **Verdict**: **slightly high**. TAO 24h is only +1.09% — there is no real momentum. The system is rewarding it for being in a "warm" sector. Score could be 5–10 points lower.

### LTC/USDT — 51.7 (short)
- Short side in a transition_up BTC regime — counter-tape direction.
- Derivatives 12.0 — but short skew in a rising tape is risky.
- **Verdict**: **possibly too high**. Counter-trend shorts on majors should be capped harder in a transition_up regime. The risk_penalty of only −6.3 looks light for this.

### Rejected — SAGA (96.2), RENDER (95.7), INJ (91.5), NEAR (81.5)
- All correctly rejected as `>2 ATR from EMA20` → "do not chase, wait for pullback".
- **Verdict**: **risk gate worked as designed**. These would have been A-tier scores absent the extension penalty — the system saved itself from chasing.

---

## CRYPTO INTRADAY — Watchlist (C-tier)

### NIL/USDT — 57.8
- 24h +20.9%, RS vs BTC +20.2%, volume only 1.25x — momentum is real but volume is light.
- catalyst_news 6.8 (slightly higher than scalp version because attention-based) — narrative 4.5 — execution_quality 5.5.
- **Verdict**: **reasonable**. Slightly lower than scalp's 60.4 because intraday uses different weight blend.

### Other C-tier names not fully enumerated in read window
- The intraday report sorts the rest similarly to scalp — SAHARA, BSB, TAO, LTC patterns repeat.

### Rejected — RENDER (100.0), SAGA (99.4), NEAR (98.9), INJ (95.4)
- Same as scalp: rejected for overextension.
- **Verdict**: **risk gate working**.

### Note on "raw vs final" inflation
- The "Strongest Symbols" table shows raw scores up to 100. The actual final scored ideas (post-penalty, post-risk) sit at 50–60. There is a **wide gap (~40 points)** between raw momentum and final score. The user should understand: raw "score 100" in the Strongest table is **NOT** an A-tier signal — it is the momentum panel's standalone score before all the gates fire. This is potentially confusing.

---

## STOCKS INTRADAY — A/B-tier ideas

### AAPL — 88.64 (A-tier)
- Evidence: above prev day high, RS vs SPY +9.49%, RS vs sector +1.34%, 1 news catalyst (test_source share buyback).
- Risk penalty: −4.0 (flat constant).
- **Components NOT shown in the stocks report** — unlike crypto, the stocks pipeline does not print a numeric score breakdown. We see only "Score 88.64, Confidence high, Risk level low".
- **Real evidence**: above prev day high, RS, sector lead.
- **Placeholder evidence**: test_source news (fake), earnings:unknown.
- **Missing evidence**: volume confirmation not surfaced per idea (Fix #2 added relative volume — is it being factored in? Not visible in the per-idea Evidence block).
- **Verdict**: **slightly high**. 88.64 with fake news + earnings unknown is generous. Real value is probably ~82–85 (still A-tier on score floor, but with caveat).
- **Risk warning visible?** "earnings risk: unknown" — yes, but as a 1-liner not a downgrade.

### LLY — 80.33 (A-tier)
- Evidence: above prev day high, RS vs SPY +16.04%, RS vs sector +16.52%.
- No news at all.
- Risk penalty −4.0.
- **Verdict**: **reasonable**. LLY is a real RS leader vs both index and sector. 80 floor is justified.

### AMD — 78.77 (B-tier)
- RS vs SPY +29.98% (best in the report), RS vs sector +20.62%.
- **Why only B?** Per the report, "RR to TP1 below 1.5 (1.0)". So the R:R cap pulled it under A.
- **Verdict**: **reasonable**. The R:R rule is doing what it should. AMD's 1.0 R:R reflects entry close to a stretched level.

### XLK — 74.91 (B-tier)
- Sector ETF, RS +8.15% vs SPY.
- **Verdict**: **acceptable** but ETF B-tier intraday is unusual — XLK is a basket, not a stock. Treat as a regime confirmation, not a trade.

### SMCI — 74.26 (B-tier)
- RS +17.91% vs SPY.
- **Verdict**: **reasonable** if you accept SMCI's volatility profile. The −4.0 risk penalty is flat and probably too low for SMCI's historical 2–3x SPY beta. Manual position sizing required.

### SMH — 73.93 (B-tier)
- Semiconductor ETF.
- **Verdict**: **acceptable**, same caveat as XLK — ETF tradeability.

### UNH — 68.59 (B-tier)
- RS vs SPY +5.01%, RS vs sector +5.49%, "RS=follower" (not leader).
- **Verdict**: **borderline**. A "follower" RS label and 68.59 score is the weakest B-tier here. Manual review.

### TSLA — 67.30 (B-tier)
- RS vs SPY +8.77%, RS vs sector +12.80%, "RS=leader".
- Notably **not** above prev day high (this line is absent from TSLA's evidence block while present for the others).
- **Verdict**: **slightly high**. Without above-prev-day-high, TSLA should arguably be C-tier intraday. The 67 score is suspiciously close to the 65 B-tier floor.

### Watchlist (C-tier)
- QQQ 64.77, IWM 56.47, SPY 54.12, XLV 52.46, MSTR 51.54 (short), DIA 50.27.
- **MSTR short at 51.54**: short_in_bullish_regime but it survived rejection — the score is right at the **rejection edge**. The B-tier rule "no shorts in bullish regime" appears to apply only as a soft signal (it shows up in COIN's rejected reasons but not in MSTR's). Inconsistent? Worth a code check.

### Rejected (14 names)
- `both_index_and_sector_contradict` was applied to NVDA short (41.33) and AVGO short (23.93). Good — Fix #4 working.
- `short_in_bullish_regime` blocked COIN, GOOGL, NFLX, XOM shorts.
- `weak_relative_strength, rr_below_1.5` blocked JPM, XLF, XLY, PLTR longs.
- `long_in_weak_sector, weak_relative_strength, rr_below_1.5` blocked META.
- `no_directional_setup` filtered AMZN, MSFT, XLE.
- **Verdict on rejection logic**: **solid**. Reasons are explicit and the system kills clearly bad ideas.

---

## Score component freshness check

| Component | Real or placeholder today? |
|-----------|--------------------------|
| Crypto market_regime | Real (BTC/ETH 1h structure) |
| Crypto technical_setup | Real (ATR, EMA, entry zones) |
| Crypto momentum | Real (24h, RS vs BTC, volume_ratio) |
| Crypto derivatives | Real (OI %, funding, long/short, crowding) |
| Crypto catalyst_news | **Thin**: mostly tagging big-cap RSS items; small-cap movers get 0 catalyst |
| Crypto narrative | Real heatmap, thin sector coverage |
| Crypto execution_quality | Real (setup_quality 0–100) |
| Crypto risk_penalty | Real (extension, OHLCV gaps) |
| Stocks scoring components | **Not individually printed** in the report — only the aggregate score. Internal logic exists but is not transparent in the user-facing report |
| Stocks risk penalty | Flat −4.0 long / −12.0 short — **looks like a constant, not per-symbol risk** |
| Earnings risk | Placeholder ("unknown" everywhere) |
| Company news | Placeholder (test_source only) |

---

## Hard-block / cap verification

| Cap | Triggered today? | Evidence |
|-----|-----------------|----------|
| A-tier requires ≥80 + no caps | Yes (AAPL 88.64, LLY 80.33 both got A) | OK |
| Missing invalidation → cap 50 | Not triggered — all ideas have invalidation | N/A |
| Stale data > 3h → cap 50 | Not triggered — data is fresh | N/A |
| MEXC-only → cap 70 | Triggered on BSB/USDT (capped at C) | OK |
| Anchor missing → cap 75 | Not visibly triggered | Inconclusive |
| Rumor-only → cap 55 | **NOT triggered visibly**. AAPL's "test_source" share buyback is `verification single_source` — the rumor cap should arguably apply but did not | **Possible gap** |
| Extreme adverse funding → cap 78 | No symbol crossed the threshold today | N/A |
| Weekend Mode penalties | **Not applied today** — Monday, mode inactive | OK |
| both_index_and_sector_contradict (stocks) | Triggered on NVDA short, AVGO short | OK |
| short_in_bullish_regime (stocks) | Triggered on COIN, GOOGL, NFLX, XOM shorts; MSTR short survived | **Inconsistent** — MSTR short scored 51.54 and survived to C-tier despite same rule applying. Verify code path |
| rr_below_1.5 → reject | Triggered on 5+ names | OK |

---

## Idea-by-idea verdict

| Idea | Score | Tier | Verdict | Key concern |
|------|-------|------|---------|-------------|
| AAPL long | 88.64 | A | **Slightly high** | Test_source news inflates evidence; earnings unknown |
| LLY long | 80.33 | A | **Reasonable** | Clean RS leader vs index + sector |
| AMD long | 78.77 | B | **Reasonable** | R:R cap honest |
| XLK long | 74.91 | B | **Reasonable as regime confirm**, not as trade |
| SMCI long | 74.26 | B | **Reasonable; risk underweight** for SMCI vol |
| SMH long | 73.93 | B | **Reasonable as regime confirm** |
| UNH long | 68.59 | B | **Borderline** — "follower" RS, lowest B |
| TSLA long | 67.30 | B | **Slightly high** — missing above-prev-day-high |
| NIL crypto | 60.4 | C | **Reasonable** |
| SAHARA crypto | 57.9 | C | **Reasonable** |
| BSB crypto short | 54.4 | C | **Reasonable but MEXC-only** |
| TAO crypto | 52.6 | C | **Slightly high** — no actual momentum |
| LTC crypto short | 51.7 | C | **Possibly too high** — counter-trend short |
| MSTR short | 51.54 | C | **Should likely be rejected** by `short_in_bullish_regime` rule that hit COIN |

---

## Net assessment

- **Crypto scoring is conservative and honest today**. The risk gates worked: the system refused to chase 4 obvious overextended movers.
- **Stocks scoring is more permissive** in a strongly bullish tape. 8 A/B ideas may be 1–2 too many. AAPL leans on fake news; UNH and TSLA are borderline B's.
- **Hard-cap discipline** is mostly OK but two specific gaps surfaced:
  1. Rumor cap (55) does not appear to bite test_source / single-source AAPL news.
  2. `short_in_bullish_regime` was applied to COIN but not to MSTR — verify code path.
- **Per-idea data_confidence is implemented but invisible** in user-facing output. The user has to trust the score; component transparency is high in crypto, low in stocks reports.
