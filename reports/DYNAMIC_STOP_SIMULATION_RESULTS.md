# Dynamic Stop Simulation Results (PART 6)

**Date:** 2026-06-23. Actionable book, 60d (n=583). **Relative ranking only** (granularity + same-candle + optimistic baseline). No production change.

## Dynamic-stop policies vs the three reference models
| policy | net R | vs legacy touch (+6.2) | vs hold-TP3 (−136.8) | vs first-TP-close (−104.8) |
|---|---|---|---|---|
| **A** stop→BE after TP1 (M3) | −109.8 | −116 | **+27** | −5 |
| **B** stop→+0.2R after TP1 (M4) | −104.4 | −111 | +32 | ≈0 |
| **C** stop→+0.5R after TP1 (dC) | **−96.3** | −103 | **+40** | **+8.5** |
| **D** stop→TP1 after TP2 (dD) | −119.6 | −126 | +17 | −15 |
| **E** partial 50% TP1 + BE runner (M5) | −107.3 | −114 | +30 | −2.5 |
| **F** partial 1/3·1/3·runner (M6) | −103.8 | −110 | +33 | +1 |
| **G** playbook-specific (runner for crypto swing/failed-bounce/catalyst, BE else) | −125.8 | −132 | +11 | −21 |

## Metrics (actionable, 60d)
- **Net R:** best dynamic policy = **C (+0.5R lock), −96.3R** — still net-negative.
- **PF / win rate:** resolved win rate ≈ 32% (133 TP1 reached vs 276 stops). No stop policy raises the win rate (it changes the R booked on already-won trades); PF stays < 1 under every realistic model.
- **Givebacks saved:** policies A–F rescue the 27 give-back trades from −27R (hold) up to 0…+15R → **+27 to +40R saved** vs naive hold.
- **Winners clipped / TP3 runners killed:** BE/partial caps the runner on trades that BE'd out then would have run — bounded by the 45 TP3 trades; policy **G** keeps runners for the crypto cohorts that earn TP3, but its tighter BE elsewhere costs more than it saves here (−125.8) because stocks-momentum give-backs are frequent.
- **Affected trades:** 88 (current−hold ≥1R) are where any policy matters; 495/583 unaffected.
- **Same-candle sensitivity:** 3 ambiguous trades; not decisive.
- **Sample by playbook:** crypto swing 98, crypto intraday 120, stocks intraday 364 (others below the actionable gate inside this book).

## Key reading
- **Dynamic stop helps a lot *relative to naively holding for TP3*** (+27 to +40R) and the **+0.5R-lock (C)** is the best realistic policy — but **no dynamic policy makes the actionable book positive** (best is −96R). The book is negative because the *entries* have negative expectancy at ~32% win rate; stop management redistributes R on the winners, it can't manufacture edge.
- Crucially, **every dynamic policy is still far below the recorded +2R / legacy +6.2R** — confirming that the recorded positivity is the optimism artifact, not something dynamic stops "give back."
- **Best practical takeaway:** IF the desk goes to real execution, a **+0.5R lock or 50% partial + BE after TP1** is the least-bad exit and protects the give-back cluster (crypto swing / stocks-momentum long pops) — but that is a forward-execution design choice, not a fix for current accounting.

## Verdict
`DYNAMIC_STOP_SIMULATION_COMPLETE` — +0.5R-lock (C) is the best realistic exit (+40R vs hold); none turns the actionable book positive.
