# Signal Tracking and Performance

This page documents the **passive** signal-tracking module added to the desk.

## What it is

A separate layer that records every A/B (and watchlist+trigger) trade idea the supervisor produces, then reconciles each one against later OHLCV to measure:

- whether entry triggered (and when)
- whether TP1/TP2/TP3 hit
- whether the stop hit (and whether same-candle ambiguity occurred)
- max favorable / adverse excursion in R
- time-to-entry
- final outcome: `win` / `loss` / `partial_win` / `expired` / `not_triggered` / `missed` / `ambiguous`

## What it is NOT

- **Not** a self-tuner. It NEVER changes scoring weights, NEVER edits stops/targets, NEVER disables strategies.
- **Not** the operator's PnL ledger. It tracks *what the system proposed*; real executed trades belong in their own ledger.

## Architecture

```
src/signals/
  __init__.py
  config.py            # loader for config/signal_tracking.yaml
  models.py            # ProposedSignal / SignalOutcome + lifecycle constants
  registry.py          # extract A/B/(C+trigger) from TradeIdea → upsert into DB
  tracker.py           # walk OHLCV → write SignalOutcome rows + update status
  analytics.py         # winrate / PF / breakdowns / sample-size labels
  obsidian_export.py   # render Signal_Log + Daily/Weekly reviews
```

Database tables (in `db/crypto_ai_desk.sqlite`):

- `proposed_signals` — one row per tracked idea (signal_id, entry, stop, TPs, validity, status, raw json).
- `signal_outcomes` — one row per tracker check (status, entry_triggered, tp/stop flags, MFE/MAE in R, final_r).
- `signal_performance_snapshots` — reserved for future periodic snapshots.

Auto-registration: the supervisor calls `_maybe_register_signals` right after `save_trade_ideas` for every report (daily/intraday/swing). Failures here log a warning but never block report generation.

## CLI

```
python -m src.cli register-signals [--agent-output PATH]
python -m src.cli active-signals [--mode X] [--tier A|B|C]
python -m src.cli signal-detail <signal_id>
python -m src.cli track-signals [--mode X | --all | --signal-id ID] [--verbose]
python -m src.cli signal-stats [--period today|week|month|all] [--mode X] [--tier X] [--weekend-mode]
python -m src.cli review-signals --period today|week|month [--write-obsidian] [--log-signals]
```

## Metric semantics

- R-based PF: `Σ(positive_R) / |Σ(negative_R)|`. Default R model (stop=-1, tp1=+1, tp2=+2, tp3=+3) lives in `config/signal_tracking.yaml`.
- `winrate_triggered = wins / triggered`. `capture_rate = triggered / total`. **Not-triggered is its own bucket**, never silently rolled into losses.
- Same-candle ambiguity: when stop and TP touched in one OHLCV bar, status is marked `ambiguous` and final_r defaults to -1R (conservative). Excluded from confident winrate by default.

## Sample-size policy

- < 10: anecdotal — quote only, do not draw conclusions.
- 10–29: weak observation.
- 30–49: moderate observation.
- 50–99: stronger observation.
- 100+: reliable — rule-change suggestions allowed.

**No automatic rule changes regardless of sample size.** Every observation in `signal-stats` and reviews carries `manual_approval_required: True`.

## Failure modes worth knowing

- **Empty OHLCV**: tracker skips the signal, increments `skipped_no_ohlcv`. Run `update-data` first.
- **Registration drift**: if the same idea regenerates with slightly different entry/stop, a new signal_id is created (different hash). This is intentional — we want to measure each generated plan.
- **Weekend Mode**: registration captures `weekend_mode_active` so we can later compare weekend vs weekday performance.

## Related
- [[Signal_Performance_Checklist]]
- `config/signal_tracking.yaml`
- Spec: see commit message for the Stage 1–5 series.
