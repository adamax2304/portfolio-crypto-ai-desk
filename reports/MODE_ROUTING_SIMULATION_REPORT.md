# Mode Routing — Read-Only Simulation Report (PART 5)

**Date:** 2026-06-09 · **Scope:** Read-only simulation. No code/strategy/routing changes. Filters are applied to the *historical* signal set; TP/SL/horizon held fixed at what the tracker recorded.
**Sample window:** 14d (2026-05-26 → 2026-06-09).

## A. Crypto scalp variants

Baseline (Variant A = keep unchanged): **n=55, 1W/7L, 47 expired-or-not-triggered, netR=−6, PF=0.14, WR=12.5%.**

### Variant table
| Variant | Definition | n kept | W | L | netR | PF | Δ vs baseline |
|---|---|---:|---:|---:|---:|---:|---|
| **A** | keep unchanged | 55 | 1 | 7 | −6 | 0.14 | reference |
| **B** | news/catalyst only (`news_supported=1`) | 13 | 0 | 2 | −2 | 0.00 | removes the 1 win + 5 losses (n−42) |
| **C** | clean trend regime only (`market_regime` contains "trend", excludes "danger") | 8 | 0 | 1 | −1 | 0.00 | removes 1 win + 6 losses (n−47) |
| **D** | liquid only (binance OR BTC/ETH/SOL/BNB/XRP) | 55 | 1 | 7 | −6 | 0.14 | **no signals removed — all 55 are already liquid** |
| **E** | B OR C OR D (catalyst OR trend OR liquid) | 20 | 0 | 3 | −3 | 0.00 | removes 1 win + 4 losses (n−35) |
| **F** | watchlist-only (no actionable A/B) | 0 | 0 | 0 | 0 | n/a | suppresses everything |

### Crypto scalp simulation read

- **Every filter strips the single 14-day win.** The lone win (C/USDT, 2026-06-04, no news, no regime label, binance-listed) is the only victory and falls out of every restrictive subset except Variant F (which strips it together with everything else, leaving 0 actionable).
- **Variant B (news-only) actually performs worse than baseline** because the one win lacked a catalyst. The 13-row catalyst subset is 0W/2L.
- **Variant C (trend-regime-only) leaves a tiny 8-row subset** with 1 closure (−1R). Sample too thin to call directional.
- **Variant D is a no-op** in the 14d window — there are no MEXC-only thin-alt scalps fielded. The liquidity filter cannot discriminate because the data is already filtered upstream.
- **Variant E (combo)** approximates Variant B at the kept level (+1R less worse) but is functionally similar; same overfitting risk.
- **Variant F (watchlist-only)** removes all noise but also removes the entry-edge data that PART 2 identified (27 expired with positive MFE). Going watchlist-only locks in scalp's net-zero on actionable but **stops the diagnostic signal** the system needs to refine scalp parameters later.

### Risk of overfitting
- Total closed scalp = 8. Any 3- to 4-element variant is **under the noise floor**. Variants B/C/E are each filtering on 1–3 closures of evidence.
- A "+1R improvement" by stripping losses while also stripping the only win is not skill — it's removing 5–6 events and pretending the 2 left would have happened the same way.
- **Conclusion: none of B–E pass an overfitting smell test on the current sample.** Either keep (A) or pause-actionable (F).

## B. Stocks invest variants

Baseline (Variant A = keep unchanged): **n=39, 0W/7L, 32 expired-or-not-triggered, netR=−7, PF=0.00, WR=0%.**

### Variant table
| Variant | Definition | n kept | W | L | netR | PF | Δ vs baseline |
|---|---|---:|---:|---:|---:|---:|---|
| **A** | keep unchanged | 39 | 0 | 7 | −7 | 0.00 | reference |
| **B** | watchlist-only | 0 | 0 | 0 | 0 | n/a | suppresses all 39 |
| **C** | longer expiry / different evaluation horizon | 39 | 0 | 7 | −7 | 0.00 | **cannot simulate cleanly** — would require re-running tracker. Note: trigger→stop median is 2 d while window already runs to 30 d; expiry length is not the binding constraint. |
| **D** | news/earnings supported | **0** | 0 | 0 | 0 | n/a | **no invest A/B signal carries `news_supported=1` in 14d** — variant produces empty set |
| **E1** | ETF only | 11 | 0 | 4 | −4 | 0.00 | removes 28 single-names, keeps the worst-PF subset |
| **E2** | single-name only | 28 | 0 | 3 | −3 | 0.00 | removes ETFs (which lost 4) — better but still 0 wins |
| **F** | B-tier only (drop A-tier) | 37 | 0 | 7 | −7 | 0.00 | removes 2 A-tier (both expired flat, no R impact) — no improvement |

### Stocks invest simulation read

- **Variant B (watchlist-only) is mechanically equivalent to extending the stocks-swing pause to invest.** Removes the entire −7R but also removes any chance of future positive data without code changes.
- **Variant C (longer expiry) is mis-targeted.** The 7 losses fired their stops at median 2 days, max 6 days. Extending the validity window from 30 d to a longer horizon does not save those signals — they already invalidated. The binding constraint is **stop placement, not window length**. This variant cannot be meaningfully simulated read-only and would require strategy work.
- **Variant D (news/earnings only) collapses to n=0.** The pipeline does not currently flag invest signals with `news_supported=1` — the catalyst lane is not wired through to invest. This is an observability/feature gap rather than a routing decision.
- **Variant E1 (ETF only)** is the *worst* surviving subset — all 4 closures are losses in tech-sector ETFs (XLK, SMH).
- **Variant E2 (single-name only)** is slightly better (3 losses vs 4) but still 0W.
- **Variant F (B-tier only)** doesn't change the picture — A-tier invest signals (LLY A, AAPL A) are too few and both expired flat.

### Risk of overfitting
- Closed sample = 7 A/B losses. Splitting into ETF/single-name yields 4 vs 3 — that's not a real partition, that's reading tea leaves.
- The only filter that has a sound a-priori justification (Variant B = watchlist) is also the most aggressive (suppresses all signals).
- The "longer expiry" variant (C) cannot be tested without code changes and is the wrong cure for the observed problem (stops fire fast, not late).

## C. What the simulations do NOT tell us

These read-only simulations hold the existing TP/SL/horizon constant. They cannot tell us:

1. **Whether a wider stop on invest would convert "stop-out in 2 days" into "ride to thesis at 30 d".** This requires re-running the tracker against modified stop_loss/invalidation values — out of scope for read-only.
2. **Whether a closer TP1 + partial-take on scalp would convert "expired with MFE +0.5R" into a positive PF.** PART 2 ballparked this at "near break-even" but it requires actual code path changes.
3. **Whether changing scoring weights would shrink the negative subset.** Out of scope — no scoring changes.
4. **Whether crypto A-tier scalp would behave differently from B-tier scalp.** 14d sample contains zero crypto A-tier scalp signals.

## D. Summary table — what each variant actually accomplishes

| | Crypto scalp | Stocks invest |
|---|---|---|
| Best "PF improvement" filter | none (every restrictive variant strips the only win) | none (all variants keep 0 W) |
| Best "loss reduction" filter | C (clean trend) keeps −1R | E2 (single-name) keeps −3R |
| Cleanest "no decision" filter | A (keep) — sample too small to confidently switch | A (keep) — sample 7 closures |
| Cleanest "suppress" filter | F (watchlist) — guarantees 0R | B (watchlist) — guarantees 0R |
| Overfit risk for B-E | high — each filter touches ≤8 closures | high — each filter touches ≤7 closures |

## Verdict for PART 5
- Crypto scalp: **read-only simulation does not support any of B, C, D, E.** The choice is between **A (keep)** and **F (pause-actionable / watchlist)** — and B/C/E would all reduce sample size below any reasonable inference threshold while removing the only win. **Recommendation deferred to PART 6 leans toward A (keep & monitor) given the entry-edge evidence in PART 2.**
- Stocks invest: **read-only simulation does not support any of C, D, E.** Variant D collapses (no news flag); Variant C is mis-targeted (stops, not window); E1/E2 reshuffle 7 losses without finding a positive subset. The choice is between **A (keep)** and **B (watchlist)**. Given the strong qualitative parallel with the already-paused stocks swing (same A-tier-long pipeline, same symbols, same dates), watchlist-only is the structurally defensible move, but **the sample (7 A/B closures) is below the threshold for a hard verdict.** PART 6 will favor a soft-pause (watchlist-only) pending 1 more US trading week of data.
