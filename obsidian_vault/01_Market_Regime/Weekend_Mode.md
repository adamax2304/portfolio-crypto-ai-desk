# Weekend Mode

Weekend Mode is a **risk/scoring overlay** that automatically activates on Saturdays and Sundays. It does not block trading. It makes the desk more selective, safer, and more skeptical because weekend crypto markets have:

- Thinner liquidity.
- More random wicks.
- Worse execution.
- Less reliable short-term moves.
- Fewer institutional participants.

This page is the **vault-side documentation**. Authoritative behavior lives in [src/analysis/weekend_mode.py](../../src/analysis/weekend_mode.py) and [config/weekend_mode.yaml](../../config/weekend_mode.yaml).

---

## Activation

- Triggered automatically when current day in the project timezone (`config/settings.yaml.project.timezone`, default `Asia/Nicosia`) is in `active_days` (Saturday, Sunday).
- Controlled by `config/weekend_mode.yaml.enabled` (default true).
- Check live status: `python -m src.cli weekend-status`.

## What it changes

| Adjustment | Default value | Effect |
|---|---|---|
| `a_tier_score_penalty` | 5 | Subtracted from any score ≥ 80. Re-evaluates tier, so borderline A-tier becomes B. |
| `confidence_penalty` | 0.10 | Steps confidence label down one band (high → medium-high, medium-high → medium, etc). |
| `overextension_penalty_multiplier` | 1.25× | Extra penalty for setups extended > 2 ATR from EMA20. |
| `max_tier_for_weak_signals` | B | Weak signals (acceptable data quality, risk_penalty ≥ 12, or weak technical_setup component) capped at B. |
| `max_tier_for_weak_mexc_only_signals` | C | Weak + MEXC-only capped at C (watchlist). |
| `downgrade_chasing_entries` | true | Any A/B-tier with extension > 2 ATR is demoted to C. |

Plus informational warnings:

- `tight_stop_warning` — warns when stop is < 0.8 ATR from price (wick risk).
- `require_retest_after_impulse` — warns when 24h move ≥ 6% (demand retest acceptance).
- `prefer_structure_or_atr_stops` — recommend structural invalidation over fixed ATR stop.

## Mode-specific magnitude

The overlay is **strictest in scalp**, **lightest in invest / long-term**.

| Mode | a_tier_score_penalty | confidence_penalty | Notes |
|---|---|---|---|
| scalp | 7 | 0.15 | Strictest. Demand immediate trigger + confirmation; avoid entries after vertical 1m/5m candles; explicit max holding time. |
| intraday | 5 | 0.10 | Default. Prefer pullback/retest setups. Avoid chasing breakouts without 15m/1h acceptance. |
| swing | 2 | 0.05 | Light. Higher-timeframe thesis still applies; wicks are noise. |
| invest | 0 | 0.0 | Informational only. Weekend execution is worse but thesis isn't invalidated by wicks. |

## How a typical trade idea is affected

Before overlay (Friday):

```
ETH/USDT  intraday  short  score 81.5  tier A  conf high  caps: none
```

After overlay (Saturday):

```
ETH/USDT  intraday  short  score 76.5  tier B  conf medium-high  caps: weekend...
warnings:
  - Weekend Mode (intraday): prefer pullback / retest setups...
  - Weekend Mode: prefer structural invalidation over fixed ATR stop.
reasons:
  - Weekend Mode applied: original score 81.5/A -> 76.5/B. Notes: weekend: -5 a-tier margin penalty
```

## What it does NOT do

- **Does not block trades.** It downgrades borderline ones.
- **Does not change direction.** Long stays long, short stays short.
- **Does not modify market data, indicators, or agent outputs other than the score block.**
- **Does not increase score for any idea.**

## When the overlay no-ops

- `enabled: false` in `config/weekend_mode.yaml`.
- Today (in project timezone) is not in `active_days`.
- The config file is missing or malformed (defensive default = disabled).
- Any exception during overlay → logged warning, original scores preserved.

## Inspecting the effect

After a daily/intraday/scalp/swing report runs while Weekend Mode is active, the desk persists:

```
data/processed/weekend_mode_latest.json
```

Schema:

```json
{
  "status": {
    "enabled": true,
    "active": true,
    "day_name": "Saturday",
    "now_local": "2026-05-23T17:00:00+03:00",
    "timezone": "Asia/Nicosia",
    "active_days": ["Saturday", "Sunday"]
  },
  "adjustments": {
    "SOL/USDT": {
      "symbol": "SOL/USDT",
      "original_score": 82.0,
      "new_score": 77.0,
      "original_tier": "A",
      "new_tier": "B",
      "notes": ["weekend: -5 a-tier margin penalty"],
      "downgraded": true
    }
  }
}
```

`prepare-analysis` also embeds the live status into `data/processed/llm_analysis_packet.md`.

## Common operator mistakes

- Forgetting Weekend Mode is active and wondering why the otherwise-A-tier setup came out B.
- Trying to force an A-tier by pushing the score in another component — caps apply regardless.
- Treating a weekend B-tier as equivalent to a weekday B-tier — weekend B may have been a weekday A; size accordingly.
- Ignoring tight-stop warnings — weekend wicks really do hit them more often.

## Future improvements

- Per-hour granularity (e.g. extra caution during late Saturday US night).
- Detect actual liquidity drops via spread/quote-volume snapshots instead of a calendar rule.
- Add an "Asian-session weekend" sub-overlay for very thin liquidity windows.

## Related

- [[Weekend_Liquidity_Risk]]
- [[Weekend_Mode_Checklist]]
- [[Market_Regime_Overview]]
- [[Score_Caps]]
- [[Risk_Management_Overview]]

## Implemented status

- **Implemented**. Module at [src/analysis/weekend_mode.py](../../src/analysis/weekend_mode.py); CLI: `weekend-status`; integrated into Supervisor + WatchlistMonitor + prepare-analysis packet.
