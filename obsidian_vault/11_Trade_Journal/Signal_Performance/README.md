# Signal Performance

Passive performance journal for proposed A/B (and C+trigger) signals.

- Source of truth (numbers): `db/crypto_ai_desk.sqlite` tables `proposed_signals`,
  `signal_outcomes`, `signal_performance_snapshots`.
- Source of truth (narrative): this folder.

## Subfolders

- `Signal_Logs/` — one note per signal, fed by `review-signals` or `register-signals`.
- `Daily_Reviews/` — written by `review-signals --period today --write-obsidian`.
- `Weekly_Reviews/` — written by `review-signals --period week --write-obsidian`.
- `Monthly_Reviews/` — same idea, period=month.
- `Stats/` — anything you save manually from the JSON output of `signal-stats`.
- `Templates/` — copy these by hand when journaling individual ideas.

## Rules

1. The signal tracker is **passive**. It never changes scoring or stops.
2. Always look at `sample_size` and `confidence_level` before reading any rate.
   Less than 10 signals is `anecdotal`. Less than 30 is `weak`.
3. Observations carry a `manual_approval_required` flag. Treat them as questions,
   not commands.
4. Proposed signals != executed trades. This folder is about *signal quality*.

## Useful commands

```
python -m src.cli register-signals            # backfill from latest agent output
python -m src.cli active-signals              # what's still waiting/triggered
python -m src.cli signal-detail <signal_id>   # full plan + outcome history
python -m src.cli track-signals --all         # walk OHLCV for outcomes
python -m src.cli signal-stats --period week  # breakdowns + observations
python -m src.cli review-signals --period today --write-obsidian
```
