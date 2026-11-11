# Crypto Scalp — Actionable / Sizing Downgrade (PART 1)

**Date:** 2026-06-16
**Trigger:** 12-month, 1.55M-candle, 139k-trade scalp historical backtest → verdict
`DISABLE_SCALP_ACTIONABLE_KEEP_SHADOW`
(see [SCALP_KEEP_REWORK_DISABLE_DECISION.md](SCALP_KEEP_REWORK_DISABLE_DECISION.md)).

## What changed

Single line in the **reporting/sizing layer** — `config/sizing_weights.yaml`:

```yaml
crypto_scalp_momentum_continuation: 0.0   # was 0.5
```

with an inline comment recording the reason (12mo backtest net-negative after fees:
WR 43% / PF 0.63 / avg −0.466R; train+val+OOS all negative; no exit/regime/session/
symbol variant flips positive; root cause = cost vs tight ATR-distance, not entry).

The weight is consumed by `src/signals/sizing.py::size_decision`, which now returns:

| field         | crypto scalp (after) |
|---------------|----------------------|
| `weight`      | `0.0`                |
| `sized_r`     | `0.0` (regardless of `raw_r`) |
| `playbook`    | `crypto_scalp_momentum_continuation` (unchanged) |
| `raw_r`       | echoed verbatim from tracker (unchanged) |

Verified live:

```
crypto scalp     weight=0.0  playbook=crypto_scalp_momentum_continuation
crypto intraday  weight=1.0  playbook=crypto_intraday_catalyst_or_momentum
crypto swing     weight=1.0  playbook=crypto_swing_narrative_rs_momentum
stocks intraday  weight=1.0  playbook=stocks_intraday_rth_momentum
```

## Why the sizing layer (and only the sizing layer)

`config/sizing_weights.yaml` is explicitly a **reporting / paper-PnL layer**. Its own
header states it does NOT influence generation, scoring, tier thresholds, TP/SL
geometry, Telegram eligibility, or the `proposed_signals` / `signal_outcomes` tables.
Setting scalp to `0×` therefore:

- removes scalp from sized portfolio R, WR, and PF math (it no longer contributes
  any actionable risk allocation), **and**
- changes nothing about how scalp signals are generated, scored, or stored.

`0.0` already carries the documented semantic "not traded in this scheme (paused mode,
watchlist, shadow)" — the same value used for paused stocks swing/invest. Scalp now
joins that cohort.

## What is explicitly preserved (expected behavior)

| Capability                              | State after downgrade |
|-----------------------------------------|-----------------------|
| Scalp signal **generation**             | ✅ kept — 136 scalp rows in `proposed_signals`, latest 2026-06-15T20:24Z |
| Scalp signal **recording**              | ✅ kept |
| Scalp signal **tracking** (outcomes)    | ✅ kept — `raw_r` still echoed |
| Scalp in **Obsidian / journal / research** | ✅ kept (now flagged SHADOW ONLY — PART 3) |
| Scalp counted as **actionable**         | ❌ no — `sized_r = 0` |
| Scalp recommended for **manual live shadow** | ❌ no — dashboard says "NOT for manual live shadow" |

## Non-scalp modes — untouched

All other playbook weights are byte-for-byte unchanged:

- `crypto_swing_narrative_rs_momentum: 1.0`
- `crypto_intraday_catalyst_or_momentum: 1.0`
- `crypto_failed_bounce_short: 1.0`
- `crypto_rs_leader_long: 1.0`
- `crypto_catalyst_backed_setup: 1.0`
- `stocks_intraday_rth_momentum: 1.0` (A-tier-long `0.5` fine-override unchanged)
- `stocks_swing_watchlist_rs_rotation: 0.0` (already paused — unchanged)
- `stocks_invest_watchlist_30d_thesis: 0.0` (already paused — unchanged)
- `tier_overrides` (C→0, rejected→0) unchanged.

## Guardrail

`tests/test_scalp_downgrade.py::test_1_scalp_sizing_weight_is_zero` and
`tests/test_sizing.py::test_crypto_scalp_gets_zero_shadow_only` pin
`weight == 0.0` / `sized_r == 0.0` so the weight cannot silently drift back up.

**PART 1 status: DONE.**
