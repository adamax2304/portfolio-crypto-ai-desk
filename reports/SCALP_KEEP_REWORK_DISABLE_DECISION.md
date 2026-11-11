# Scalp — Keep / Rework / Disable Decision (PART 8)

**Date:** 2026-06-15 · Based on a real 12-month, 1.55M-candle, 139k-trade backtest.

## Verdict

```
DISABLE_SCALP_ACTIONABLE_KEEP_SHADOW
```

The 12-month backtest decisively shows current crypto scalp **cannot beat realistic transaction costs on liquid majors** with this geometry — net −0.47R/trade, stable across train/validation/OOS, with no exit variant, regime gate, session gate, or symbol filter producing a net-positive subset. It should **never be promoted to actionable/live**. Keep generating it as **pure shadow/research** (the gross edge is real and worth tracking for a future low-cost rework), but downgrade its actionable footprint.

## Answers

1. **Profitable on 6–12m after fees?** **No.** −0.466R/trade net (gross ≈ +0.73R, fees ≈ −1.2R). PF 0.63. 139k trades, 12 months.
2. **Is TP1 +0.5R better than current?** **No — far worse.** −1.073R/trade, PF 0.01 (the win is smaller than the fee). Definitively kills the earlier small-sample hypothesis.
3. **Does partial TP improve PF/drawdown?** **No.** Partial @ +0.5R (C) = −0.675R, PF 0.23. Only **trailing after +0.7R (G)** helps (PF 0.93, MDD −9.6k vs −64.8k) but is still net-negative.
4. **Is the problem entry, exit, expiry, regime, or liquidity?** **Cost vs ATR-distance.** Entry has positive gross edge; exit/expiry tweaks don't fix it; every regime/session/symbol is negative. The binding constraint is the ~1.2R per-trade fee on the tight 5m ATR stop — worst on the lowest-ATR majors (BTC −1.85R).
5. **Stay paper-only?** **Yes**, at minimum — and ideally downgraded further (shadow-only).
6. **Disable entirely?** Not the candidate generation (the gross edge is research-worthy), but **disable any path to actionable/live**.
7. **Rework?** Only a **cost/instrument rework** could matter (maker-only fills, higher-ATR alts, wider stops). Exit/entry-filter reworks do NOT clear the cost hurdle — do not pursue them.
8. **Promote any variant later?** Not on this evidence. The least-bad (trail-exit G on higher-ATR mid-caps, US session) is still negative.
9. **Evidence required before any production change?** A variant must show **net-positive (PF > 1) after 15bps fees in TRAIN, VALIDATION, and OOS simultaneously**, on ≥ 6 months, ideally with 1m intrabar confirmation. Nothing tested meets this.

## Production implication (NOT implemented — would need approval)

Current production already neutralises scalp (sized 0.5×, setup Telegram silenced, paper-entry kept). The backtest supports going one step further: **set scalp sized weight to 0× and/or downgrade scalp paper-entry alerts to shadow** so the operator is never nudged to mirror a structurally-losing setup. This is a sizing/notification change → **NEEDS APPROVAL** and is not done here.

## What stays true

- Scalp's **entry scan has a real gross edge** — keep collecting it (shadow) for a future maker-fee / higher-ATR rework study.
- Under current cost assumptions, scalp on liquid majors is a **structural loser**; no amount of TP/SL/expiry tuning changes that.
