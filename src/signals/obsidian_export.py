"""Generate human-readable Obsidian notes from signal data.

Two write paths:

1. Per-signal log under `obsidian_vault/11_Trade_Journal/Signal_Performance/Signal_Logs/`
2. Daily/weekly review notes under `Daily_Reviews/` and `Weekly_Reviews/`

The module is content-only — it doesn't touch scoring or strategy code.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.signals.analytics import BreakdownReport, observations
from src.signals.config import SignalTrackingConfig
from src.storage.file_store import FileStore
from src.storage.sqlite import SQLiteStore


VAULT_ROOT = Path("obsidian_vault") / "11_Trade_Journal" / "Signal_Performance"


def _safe_filename(value: str) -> str:
    return (
        value.replace("/", "_")
        .replace("\\", "_")
        .replace(":", "-")
        .replace(" ", "_")
    )


def _fmt(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        if value == float("inf"):
            return "∞"
        return f"{value:.4f}".rstrip("0").rstrip(".") or "0"
    return str(value)


def render_signal_log(signal: dict[str, Any], outcomes: list[dict[str, Any]]) -> str:
    """Markdown for one signal — uses the Signal_Log_Template structure."""

    latest = outcomes[-1] if outcomes else None
    lines = [
        f"# Signal Log — {signal.get('symbol')} — "
        f"{signal.get('mode')} — {signal.get('tier')} — "
        f"{str(signal.get('created_at', ''))[:10]}",
        "",
        "## Basic Info",
        f"- Signal ID: `{signal.get('signal_id')}`",
        f"- Date/time generated: {signal.get('created_at')}",
        f"- Symbol: {signal.get('symbol')}",
        f"- Direction: {signal.get('direction')}",
        f"- Mode: {signal.get('mode')}",
        f"- Tier: {signal.get('tier')}",
        f"- Score: {_fmt(signal.get('score'))}",
        f"- Confidence: {signal.get('confidence')}",
        f"- Data confidence: {signal.get('data_confidence')}",
        f"- Market regime: {signal.get('market_regime')}",
        f"- Weekend mode: {bool(signal.get('weekend_mode_active'))}",
        f"- Exchange confirmation: {signal.get('exchange_confirmation_type')} "
        f"(focus={signal.get('exchange_focus')})",
        f"- Sector/narrative: {signal.get('sector')} / {signal.get('narrative')}",
        "",
        "## Trade Plan",
        f"- Entry: {_fmt(signal.get('entry_low'))} – {_fmt(signal.get('entry_high'))}",
        f"- Stop/invalidation: {_fmt(signal.get('invalidation'))}",
        f"- TP1: {_fmt(signal.get('tp1'))}",
        f"- TP2: {_fmt(signal.get('tp2'))}",
        f"- TP3: {_fmt(signal.get('tp3'))}",
        f"- Validity window: {_fmt(signal.get('validity_window_hours'))}h "
        f"(expires {signal.get('expires_at')})",
        f"- Setup type: {signal.get('setup_type')}",
        "",
        "## Thesis",
        f"- Main thesis: {signal.get('thesis')}",
        f"- Counter-thesis: {signal.get('counter_thesis')}",
        f"- News supported: {bool(signal.get('news_supported'))}",
        f"- Telegram supported: {bool(signal.get('telegram_supported'))}",
        f"- Derivatives supported: {bool(signal.get('derivatives_supported'))} "
        f"(OI: {signal.get('oi_context')} | Funding: {signal.get('funding_context')})",
        "",
        "## Tracking Outcome",
    ]
    if latest is None:
        lines.append("- No outcomes recorded yet. Run `python -m src.cli track-signals`.")
    else:
        lines += [
            f"- Last checked at: {latest.get('checked_at')}",
            f"- Status: {latest.get('status')}",
            f"- Entry triggered: {bool(latest.get('entry_triggered'))} "
            f"({latest.get('entry_triggered_at') or '—'})",
            f"- TP1 hit: {bool(latest.get('tp1_hit'))} ({latest.get('tp1_hit_at') or '—'})",
            f"- TP2 hit: {bool(latest.get('tp2_hit'))} ({latest.get('tp2_hit_at') or '—'})",
            f"- TP3 hit: {bool(latest.get('tp3_hit'))} ({latest.get('tp3_hit_at') or '—'})",
            f"- Stop hit: {bool(latest.get('stop_hit'))} ({latest.get('stop_hit_at') or '—'})",
            f"- Legacy touch R (optimistic, NOT PnL): {_fmt(latest.get('final_r'))}",
            f"- Final outcome: {latest.get('final_outcome')}",
            f"- MFE (R): {_fmt(latest.get('max_favorable_excursion_r'))}",
            f"- MAE (R): {_fmt(latest.get('max_adverse_excursion_r'))}",
        ]

    lines += [
        "",
        "## Review",
        "- Was this a good signal?",
        "- Was entry too strict or too loose?",
        "- Was stop too tight or too wide?",
        "- Did news/Telegram help?",
        "- Did market regime support the idea?",
        "- Lesson:",
        "",
        "## Source",
        f"- Report: `{signal.get('source_report_path') or '(not recorded)'}`",
        f"- Context snapshot: `{signal.get('source_context_path') or '(not recorded)'}`",
    ]
    return "\n".join(lines) + "\n"


def render_review(
    *,
    period: str,
    breakdown: BreakdownReport,
    config: SignalTrackingConfig,
    headline: dict[str, Any] | None = None,
) -> str:
    overall = breakdown.overall
    obs = observations(breakdown, config=config)
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # R1: when a headline split is supplied, the actionable A/B metric leads
    # and the all-tier number is demoted to a diagnostic. C-tier (watchlist /
    # research) is shown separately so it never dilutes the headline PF.
    headline_lines: list[str] = []
    if headline:
        ab = headline.get("actionable", {}) or {}
        c = headline.get("watchlist", {}) or {}
        headline_lines = [
            "## Headline — Actionable Performance (A/B only)",
            f"- Sample: **{ab.get('sample_size', 0)}** "
            f"(confidence: `{ab.get('confidence_level', 'anecdotal')}`)",
            f"- Triggered: {ab.get('triggered', 0)} | "
            f"Wins / losses: {ab.get('wins', 0)} / {ab.get('losses', 0)}",
            f"- Winrate: {_fmt(ab.get('winrate_triggered'))} | "
            f"PF: {_fmt(ab.get('profit_factor'))} | "
            f"avg R / total R: {_fmt(ab.get('average_r'))} / {_fmt(ab.get('total_r'))}",
            "",
            "## C-tier Watchlist / Research Performance",
            f"- Sample: {c.get('sample_size', 0)} | "
            f"Wins / losses: {c.get('wins', 0)} / {c.get('losses', 0)} | "
            f"PF: {_fmt(c.get('profit_factor'))} | total R: {_fmt(c.get('total_r'))}",
            "- Note: C-tier is watchlist/research quality, **not** "
            "Telegram-actionable. Excluded from the headline metric.",
            "",
        ]

    overall_title = "## All-tier diagnostic (A/B/C — not the headline)" if headline else "## Overall"
    header = (
        f"# Signal Review — {period} — {now_iso[:10]}",
        "",
        "_Generated by `python -m src.cli review-signals`. Passive observation —"
        " all rule changes require manual approval._",
        "",
        *headline_lines,
        overall_title,
        f"- Sample: **{overall['sample_size']}** "
        f"(confidence: `{overall['confidence_level']}`)",
        f"- Triggered: {overall['triggered']} "
        f"(capture rate: {_fmt(overall['capture_rate'])})",
        f"- Wins / losses / ambiguous: "
        f"{overall['wins']} / {overall['losses']} / {overall['ambiguous']}",
        f"- TP1 / TP2 / TP3 hits: "
        f"{overall['tp1_hits']} / {overall['tp2_hits']} / {overall['tp3_hits']}",
        f"- Stop hits: {overall['stop_hits']}",
        f"- Winrate (triggered): {_fmt(overall['winrate_triggered'])}",
        f"- Profit factor: {_fmt(overall['profit_factor'])}",
        f"- Average R / total R: "
        f"{_fmt(overall['average_r'])} / {_fmt(overall['total_r'])}",
        f"- Average MFE / MAE (R): "
        f"{_fmt(overall['average_mfe_r'])} / {_fmt(overall['average_mae_r'])}",
        f"- Average time to entry: {_fmt(overall['average_time_to_entry_min'])} min",
        "",
    )
    sections: list[str] = list(header)

    def _section(title: str, rows: list[dict[str, Any]]) -> None:
        if not rows:
            return
        sections.append(f"## {title}")
        sections.append(
            "| label | n | confidence | triggered | wins | losses | "
            "winrate | PF | avg R | total R | capture | stop rate |"
        )
        sections.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for row in rows:
            sections.append(
                f"| {row.get('label')} | {row.get('sample_size')} | "
                f"{row.get('confidence_level')} | {row.get('triggered')} | "
                f"{row.get('wins')} | {row.get('losses')} | "
                f"{_fmt(row.get('winrate_triggered'))} | "
                f"{_fmt(row.get('profit_factor'))} | "
                f"{_fmt(row.get('average_r'))} | "
                f"{_fmt(row.get('total_r'))} | "
                f"{_fmt(row.get('capture_rate'))} | "
                f"{_fmt(row.get('stop_rate'))} |"
            )
        sections.append("")

    _section("By tier", breakdown.by_tier)
    _section("By mode", breakdown.by_mode)
    _section("By direction", breakdown.by_direction)
    _section("By exchange confirmation", breakdown.by_exchange_confirmation)
    _section("By weekend mode", breakdown.by_weekend_mode)
    _section("By sector", breakdown.by_sector)
    _section("By narrative", breakdown.by_narrative)
    _section("By setup type", breakdown.by_setup)

    if obs:
        sections.append("## Observations (manual approval required)")
        sections.append("")
        for note in obs:
            sections.append(
                f"- **{note['level']}** "
                f"(confidence={note['confidence']}, n={note['sample']}): {note['text']}"
            )
        sections.append("")
    else:
        sections.append("## Observations")
        sections.append("")
        sections.append(
            "_Sample sizes are still below the configured threshold "
            f"({config.minimum_sample_for_recommendations}). No observations produced._"
        )
        sections.append("")

    sections.append("## Notes")
    sections.append(
        "- This file is auto-generated. Edit freely below this line; the next "
        "review will write a new file rather than overwrite manual notes."
    )
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("### Manual notes")
    sections.append("")
    return "\n".join(sections) + "\n"


def write_review_to_vault(
    *,
    file_store: FileStore,
    breakdown: BreakdownReport,
    config: SignalTrackingConfig,
    period: str,
    headline: dict[str, Any] | None = None,
) -> Path:
    bucket = "Daily_Reviews" if period == "today" else (
        "Weekly_Reviews" if period == "week" else "Monthly_Reviews"
    )
    now = datetime.now(timezone.utc)
    fname = f"{now.strftime('%Y-%m-%d_%H-%M')}_{period}_review.md"
    relative = VAULT_ROOT / bucket / fname
    content = render_review(period=period, breakdown=breakdown, config=config, headline=headline)
    return file_store.save_markdown(relative, content)


def write_signal_logs(
    *,
    store: SQLiteStore,
    file_store: FileStore,
    signal_ids: list[str],
) -> list[Path]:
    written: list[Path] = []
    for sid in signal_ids:
        signal = store.load_signal(sid)
        if signal is None:
            continue
        outcomes = store.load_all_outcomes_for(sid)
        content = render_signal_log(signal, outcomes)
        symbol_part = _safe_filename(signal.get("symbol") or "UNKNOWN")
        date_part = str(signal.get("created_at", ""))[:10]
        fname = f"{date_part}_{symbol_part}_{sid}.md"
        relative = VAULT_ROOT / "Signal_Logs" / fname
        written.append(file_store.save_markdown(relative, content))
    return written


def write_templates(file_store: FileStore) -> list[Path]:
    """Write the canonical templates referenced in the spec, idempotently."""

    targets: list[tuple[Path, str]] = [
        (
            VAULT_ROOT / "Templates" / "Signal_Log_Template.md",
            _SIGNAL_LOG_TEMPLATE,
        ),
        (
            VAULT_ROOT / "Templates" / "Daily_Signal_Review_Template.md",
            _DAILY_REVIEW_TEMPLATE,
        ),
        (
            VAULT_ROOT / "Templates" / "Weekly_Signal_Review_Template.md",
            _WEEKLY_REVIEW_TEMPLATE,
        ),
        (VAULT_ROOT / "README.md", _README_TEMPLATE),
    ]
    written: list[Path] = []
    for rel_path, body in targets:
        # Resolve relative to project root via the file store.
        path = file_store.config.root / rel_path
        if path.exists():
            continue
        written.append(file_store.save_markdown(rel_path, body))
    # Ensure subfolders exist for daily/weekly/monthly + signal logs.
    for folder in (
        "Daily_Reviews",
        "Weekly_Reviews",
        "Monthly_Reviews",
        "Signal_Logs",
        "Stats",
        "Templates",
    ):
        (file_store.config.root / VAULT_ROOT / folder).mkdir(parents=True, exist_ok=True)
    return written


_SIGNAL_LOG_TEMPLATE = """# Signal Log — {{symbol}} — {{mode}} — {{tier}} — {{date}}

## Basic Info
- Signal ID:
- Date/time generated:
- Symbol:
- Direction:
- Mode:
- Tier:
- Score:
- Confidence:
- Data confidence:
- Market regime:
- Weekend mode:
- Exchange confirmation:
- Sector/narrative:

## Trade Plan
- Entry:
- Stop/invalidation:
- TP1:
- TP2:
- TP3:
- Validity window:
- Setup type:

## Thesis
- Main thesis:
- Supporting evidence:
- News/Telegram context:
- Derivatives context:
- Risk notes:
- Counter-thesis:

## Tracking Outcome
- Entry triggered:
- Entry time:
- TP1 hit:
- TP2 hit:
- TP3 hit:
- Stop hit:
- Final status:
- Final R:
- MFE:
- MAE:

## Review
- Was this a good signal?
- Was entry too strict or too loose?
- Was stop too tight or too wide?
- Did news/Telegram help?
- Did market regime support the idea?
- Lesson:
"""


_DAILY_REVIEW_TEMPLATE = """# Daily Signal Review — {{date}}

_Generated and refreshed by `python -m src.cli review-signals --period today --write-obsidian`._

## Summary
- Total A/B signals generated today:
- Triggered count:
- Wins / losses / expired / not triggered:
- Best signal:
- Worst signal:

## Performance breakdowns
- By mode (scalp / intraday / swing / invest):
- By tier (A / B / watchlist+trigger):
- By direction (long / short):
- News / Telegram impact:
- Weekend Mode effect:

## Lessons
-

## Follow-ups (manual approval required)
-
"""


_WEEKLY_REVIEW_TEMPLATE = """# Weekly Signal Review — {{week}}

_Generated and refreshed by `python -m src.cli review-signals --period week --write-obsidian`._

## Sample size
-

## A-tier performance
-

## B-tier performance
-

## Mode performance
-

## Direction performance
-

## Exchange confirmation performance
-

## Sector / narrative performance
-

## Weekend vs weekday performance
-

## Useful observations
-

## Low-confidence observations
-

## Recommendations (require manual approval)
-
"""


_README_TEMPLATE = """# Signal Performance

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
"""
