# Post-Downgrade Verification — Crypto Scalp SHADOW ONLY (PART 5)

**Date:** 2026-06-16
**Production DB:** `db/crypto_ai_desk.sqlite` (read-only inspection)

Each required invariant, with the evidence that confirms it.

## 1. No production TP/SL change ✅

`src/agents/technical_setup_agent.py` geometry constants intact:

```
entry_low  = close − 0.65 * atr        atr_stop = close − 1.2 * atr
tp1 = close + 1.0 * atr   tp2 = close + 2.0 * atr   tp3 = close + 3.0 * atr
```

Pinned by `test_9_no_tp_sl_scoring_change`. No edit was made to any setup/geometry
module.

## 2. No scoring change ✅

`grep -c "shadow_only|sizing_weight|SHADOW ONLY|0x size" src/agents/scoring_agent.py` →
**0**. The scoring agent (and `src/stocks/agents/scoring_agent.py`) were not touched.
Scores, tiers, and reject reasons are produced exactly as before.

## 3. No routing change except scalp actionability ✅

Functional re-test of both notifier entry points (fresh in-memory stores, mocked
notifier):

| Cohort            | paper-entry | close-alert |
|-------------------|-------------|-------------|
| crypto **scalp**  | `shadow_only`, not pushed, SHADOW banner | `shadow_only`, not pushed, SHADOW banner |
| crypto intraday   | `sent`, `notifier.send` called | `sent`, `notifier.send` called |
| crypto swing      | `sent` | (same path) |
| crypto short      | `sent` | (same path) |
| stocks intraday   | `sent`, `notifier.send` called | `sent`, `notifier.send` called |

The only behavioral change is the scalp branch. Everything else takes the identical
pre-existing path.

## 4. No historical outcomes changed ✅

- `signal_outcomes`: **103,468 rows** — read-only; nothing rewritten, nothing deleted.
- Pre-downgrade scalp paper-entry alerts already in `signal_alerts` with
  `telegram_status='sent'` (24 rows) were **left untouched** — historical records are
  not rewritten. Only *future* scalp alerts route to `shadow_only` (the code change is
  forward-only; the guardrail `test_3` proves the new path).

## 5. No C-tier / shadow promoted ✅

`config/sizing_weights.yaml` `tier_overrides` unchanged (`C: 0.0`, `rejected: 0.0`).
`test_c_tier_gets_zero` passes. Scalp moved **down** to 0× (it joins the shadow cohort);
nothing was promoted up.

## 6. No auto-trade path ✅

`grep -rE "place_order|create_order|ccxt\.|exchange\.(create|place)"` across
`src/notifiers/` and `src/signals/tracker.py` → **empty**. Pinned by
`test_10_no_auto_trade_path`. The system records and (for non-scalp) notifies; it never
places an order.

## 7. Non-scalp alerts unaffected ✅

Covered by §3 above and guardrails `test_5`/`test_6`/`test_7`/`test_8` (crypto intraday,
crypto swing, crypto failed-bounce short, stocks intraday all still `sent`). Non-scalp
sizing weights all unchanged (crypto swing/intraday/short = 1.0×, stocks intraday = 1.0×
with the pre-existing A-tier-long 0.5× override).

## 8. Crypto scalp generation still works ✅

`proposed_signals` (crypto) by mode:

```
scalp     n=136   last=2026-06-15T20:24:48+00:00
intraday  n= 92   last=2026-06-15T20:37:04+00:00
swing     n= 56   last=2026-06-15T17:26:04+00:00
```

Scalp is still generated, scored, and stored. It also still gets a recorded
`signal_alerts` row on entry/close (just `shadow_only`) — so research/journal keep full
visibility.

## 9. Crypto scalp is now shadow-only ✅

- **Sizing:** `size_decision` returns `weight=0.0`, `sized_r=0.0` for crypto scalp.
- **Telegram:** paper-entry and close alerts are `shadow_only` — never pushed to the
  phone; any rendered text carries `[SHADOW ONLY — DO NOT TRADE] / CRYPTO SCALP / Not
  actionable. Research only.`
- **Setup Telegram:** still suppressed (unchanged).
- **Dashboard/journal:** every scalp row flagged `SHADOW ONLY · 0x size · NOT for manual
  live shadow`; cockpit candidate list excludes scalp; forbidden-list entry + journal
  `actionability` field added.

## Test posture

- All 10 scalp-downgrade guardrails pass.
- Focused regression (sizing + scalp + catalyst + telegram-standardization +
  paper-entry) green: 43 + 38 passing.
- Full suite: **626 passed, 3 failed**. The 3 failures are pre-existing **stocks**
  Telegram-format assertions (old header format) that this task did not touch and that
  fail independently of the scalp change — see
  [CRYPTO_SCALP_DOWNGRADE_TEST_RESULTS.md](CRYPTO_SCALP_DOWNGRADE_TEST_RESULTS.md).

## Scheduler

No scheduler restart performed or required — the change is a config value + notifier
routing + presentation labels, all read fresh on each tracker tick / dashboard render.

**PART 5 status: DONE — all invariants hold.**
