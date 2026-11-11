# Risk and Scoring Protocol

The constitutional layer of the desk. These rules are enforced in code (`src/agents/scoring_agent.py`, `src/agents/risk_agent.py`) and must not be relaxed by an LLM.

---

## Mandatory fields on every approved trade

Never approve a trade idea without:

- **Direction** (`long` / `short`)
- **Entry zone or trigger**
- **Invalidation** (timeframe close beyond a specific level)
- **Risk explanation** (what's the worst case, how much can be lost on stop)
- **Why this trade can fail** (counter-thesis)
- **Tier classification** (A / B / C / rejected)
- **Data confidence** (high / medium / low)
- **Caps active** (list cap_reasons or "none")

If any of these are missing → no trade.

## Score components and weights

From `config/scoring.yaml`:

| Component | Base weight |
|---|---|
| market_regime | 15 |
| technical_setup | 20 |
| momentum | 15 |
| derivatives | 15 |
| catalyst_news | 15 |
| narrative | 10 |
| execution_quality | 10 |

Final per-component weight = `base * regime_multiplier * mode_multiplier`.

Component value = `quality_factor * final_weight`.

Total = `sum(components) - risk_penalty`, then clamped to `[0, 100]`, then capped (lowest active cap wins).

## Tier thresholds

```
a_tier: 80   AND no active caps
b_tier: 65
c_tier: 50
rejected: anything else, OR forced by invalidation/stale-data cap.
```

## Score caps (lowest active cap wins)

| Condition | Cap |
|---|---|
| No clean invalidation AND direction ∈ {long, short} | 50 (forces rejected) |
| Stale data (>180 min) | 50 (forces rejected) |
| Unverified rumor-only catalyst | 55 |
| Low liquidity (RiskAgent low_liquidity warning) | 60 |
| MEXC-only listing (weak structure) | 65 |
| MEXC-only listing | 70 |
| Not on anchor exchange (and not MEXC-only) | 75 |
| Extreme adversarial funding (>+0.001 long or <-0.001 short) | 78 |

A-tier requires score ≥ 80 **and zero active caps**. Score 90 with any cap is **not** A-tier.

## Risk penalties (subtracted from total)

| Trigger | Penalty |
|---|---|
| regime_conflict | 8 |
| overextended (> 2 ATR from EMA20) | 8 |
| poor_risk_reward (rr_to_tp1 < 1) | 10 |
| low_liquidity | 8 |
| no_clear_invalidation | 15 |
| missing_derivatives | 2 |
| missing_news | 2 |
| too_many_warnings (≥ 3) | 5 |
| `risk.risk_score * 0.18` (capped at 18) | dynamic |
| critic verdict = reject | 10 |
| critic weak_signal_dependency | 4 |
| critic late_or_crowded | 5 |

## Regime alignment factor (multiplied into market_regime component)

| Direction | bullish trend | bearish trend | range/chop | transition | high-vol danger | other |
|---|---|---|---|---|---|---|
| long | 0.90 | 0.25 | 0.58 | 0.58 | 0.35 | 0.35 |
| short | 0.25 | 0.88 | 0.58 | 0.58 | 0.58 | 0.40 |

## Mode multipliers (`scoring.yaml.mode_weights`)

| Mode | momentum | execution_quality | catalyst_news | narrative | market_regime |
|---|---|---|---|---|---|
| scalp | 1.20 | 1.20 | 0.80 | 0.75 | 1.00 |
| intraday | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| swing | 0.90 | 1.00 | 1.20 | 1.30 | 1.15 |

## Regime multipliers (excerpt)

| Regime | momentum | technical_setup | derivatives | catalyst_news | narrative | execution_quality |
|---|---|---|---|---|---|---|
| bullish trend | 1.25 | 1.10 | 0.95 | 1.00 | 1.00 | 1.00 |
| bearish trend | 1.15 | 1.10 | 1.00 | 0.85 | 0.85 | 1.00 |
| range/chop | 0.75 | 1.15 | 1.00 | 1.00 | 0.85 | 1.20 |
| transition | 0.85 | 1.00 | 1.10 | 1.00 | 0.90 | 1.00 |
| high-volatility danger | 0.85 | 1.00 | 1.15 | 1.00 | 0.80 | 1.25 |
| low-volatility compression | 0.90 | 1.15 | 1.05 | 1.00 | 1.00 | 1.00 |

(Note: `low-volatility compression` is defined in scoring.yaml but `MarketRegimeAgent` does not currently emit it — see `Improvement_Backlog`.)

## Weekend Mode overlay (automatic Saturdays + Sundays)

Applied **after** all caps and penalties above by `src/analysis/weekend_mode.py`:

- Score ≥ 80 → subtract `a_tier_score_penalty` (default 5; scalp 7; swing 2; invest 0). Tier re-evaluated.
- Weak signals (data_quality=acceptable OR risk_penalty ≥ 12 OR technical_setup component < 12) → tier capped at B.
- Weak + MEXC-only → tier capped at C.
- Setup > 2 ATR extended from EMA20 with `downgrade_chasing_entries=true` → tier demoted to C.
- `confidence_penalty` shifts the confidence label down one band.
- Tight stop warning (< 0.8 ATR from price), retest-after-impulse warning (24h move ≥ 6%), structural-stop preference all surface as warnings.

See `obsidian_vault/01_Market_Regime/Weekend_Mode.md` for the full overlay spec. Check status: `python -m src.cli weekend-status`.

## Hard rules

1. **A-tier requires score ≥ 80 AND no caps.** If any cap is active, max tier is B.
2. **No invalidation → tier = rejected.**
3. **Stale data > 3h → tier = rejected.**
4. **Telegram never raises trade score directly.** Only attention staging.
5. **Caps are global.** Do not "override for one symbol".
6. **Risk penalty is deterministic** — re-applying weights or removing penalties by hand is forbidden.
7. **NO TRADE is valid.** Often it is the correct answer.

## When the LLM should downgrade an automated tier

The desk's tier is authoritative. The LLM should only downgrade (not upgrade) if it finds:

- Stale data the agent didn't catch (verify `last_update.json`).
- News risk window the agent didn't know about (e.g. operator-known CPI in 30 min).
- Position sizing that would breach the operator's per-day risk cap.

The LLM should **never upgrade** a desk-assigned tier. If you think the desk is wrong about a cap, file an `Improvement_Backlog` entry — do not silently bypass.

## Confidence labels

- score ≥ 85 → `high`
- score ≥ 75 → `medium-high`
- score ≥ 60 → `medium`
- else → `low`

## Data confidence

`TradeIdeaAgent._data_confidence`:

| Condition | +points |
|---|---|
| derivatives available | +1 |
| catalyst present | +1 |
| anchor listed | +1 |
| derivatives listed | +1 |
| data_quality == "strong" | +1 |

≥ 4 → high. ≥ 2 → medium. Else low.

## Operator-layer risk (LLM enforces)

- Per-trade risk: ≤ 1% of account.
- Per-day risk: ≤ 3% of account; stop adding after 3 losers.
- Correlation: 3 SOL-ecosystem ideas = 1 trade for risk-budget purposes.
- No new entries during `high-volatility danger` regime unless size halved.
- Time stops per mode: 30m / 4h / re-evaluate at 4h close.

## Related

- [[AI_TRADING_DESK_SYSTEM_PROMPT]]
- [[WATCHLIST_AND_TIER_PROTOCOL]]
- [[ANALYSIS_WORKFLOW_PROTOCOL]]
