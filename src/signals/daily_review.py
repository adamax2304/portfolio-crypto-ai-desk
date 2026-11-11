"""Minimal daily review aggregator (PART 5 fix).

The Obsidian vault skeleton (`obsidian_vault/11_Trade_Journal/Templates/
Daily_Review_Template.md`) has existed since the original stage build, but
the `review-day` CLI was a stub that printed "not implemented". Nothing
auto-populated daily desk-state for the trader's review notebook.

This module fills the minimum useful gap:

* Aggregate the day's SQLite state — reports written, A/B/C registrations,
  Telegram alerts fired, signal outcomes booked, and per-tier verdicts.
* Render as plain Markdown.
* Caller writes it to ``obsidian_vault/11_Trade_Journal/Daily_Reviews/
  YYYY-MM-DD.md``. Pure file write — no auto-trade, no DB mutation, no
  schema change.

The aggregator is read-only with respect to scoring, configs, and
agent logic. It is safe to invoke at any time, idempotent, and survives
empty days (renders a skeleton with TODO blanks for manual notes).
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.storage.sqlite import SQLiteStore


VAULT_DAILY_REVIEWS = Path("obsidian_vault") / "11_Trade_Journal" / "Daily_Reviews"


@dataclass
class DailyReviewData:
    date: str  # YYYY-MM-DD UTC
    reports_written: list[dict[str, Any]] = field(default_factory=list)
    signals_by_tier: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    telegram_alerts: list[dict[str, Any]] = field(default_factory=list)
    outcomes_today: dict[str, int] = field(default_factory=dict)
    legal_blocks: list[dict[str, Any]] = field(default_factory=list)
    # Counts split by asset_class for the headline summary.
    counts_by_asset_class: dict[str, dict[str, int]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def aggregate_daily_review(
    db: SQLiteStore,
    *,
    date: str | None = None,
) -> DailyReviewData:
    """Collect today's desk state into a DailyReviewData.

    ``date`` is YYYY-MM-DD UTC; defaults to today.
    """

    target_date = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    start = f"{target_date}T00:00:00+00:00"
    end = f"{target_date}T23:59:59+00:00"

    review = DailyReviewData(date=target_date)
    with db.connect() as conn:
        conn.row_factory = sqlite3.Row

        # Reports — trade_ideas rows tag report_id. We collapse by report_id.
        ti_rows = conn.execute(
            """
            SELECT report_id, MIN(created_at) AS first_seen, COUNT(*) AS n_ideas
              FROM trade_ideas
             WHERE created_at >= ? AND created_at <= ?
             GROUP BY report_id
             ORDER BY first_seen
            """,
            (start, end),
        ).fetchall()
        review.reports_written = [dict(r) for r in ti_rows]

        # Signals registered today, grouped by tier.
        sig_rows = conn.execute(
            """
            SELECT signal_id, created_at, symbol, asset_class, direction, mode,
                   tier, score, status, entry_low, entry_high, invalidation,
                   no_entry_conditions_json
              FROM proposed_signals
             WHERE created_at >= ? AND created_at <= ?
             ORDER BY tier, created_at
            """,
            (start, end),
        ).fetchall()
        for row in sig_rows:
            d = dict(row)
            tier = d.get("tier") or "?"
            review.signals_by_tier.setdefault(tier, []).append(d)

            ac = (d.get("asset_class") or "crypto").lower()
            review.counts_by_asset_class.setdefault(ac, {})
            review.counts_by_asset_class[ac].setdefault(tier, 0)
            review.counts_by_asset_class[ac][tier] += 1

            # PART 3 marker — legal blocks visible per-row.
            try:
                conds = json.loads(d.get("no_entry_conditions_json") or "[]")
            except Exception:
                conds = []
            if any(
                isinstance(c, str) and c.startswith("ACTIVE_LEGAL_HEADLINE_RISK")
                for c in conds
            ):
                review.legal_blocks.append({
                    "symbol": d.get("symbol"),
                    "tier": tier,
                    "asset_class": ac,
                    "marker": next(
                        (c for c in conds if isinstance(c, str) and c.startswith("ACTIVE_LEGAL")),
                        "",
                    ),
                })

        # Telegram alerts — both legacy crypto path and modern stocks ledger.
        wl_rows = conn.execute(
            """
            SELECT sent_at, symbol, previous_tier, new_tier, score,
                   direction, mode, asset_class, payload_json
              FROM watchlist_alerts
             WHERE sent_at >= ? AND sent_at <= ?
             ORDER BY sent_at
            """,
            (start, end),
        ).fetchall()
        for row in wl_rows:
            d = dict(row)
            d["_ledger"] = "watchlist_alerts"
            review.telegram_alerts.append(d)

        try:
            sa_rows = conn.execute(
                """
                SELECT sent_at, signal_id, symbol, asset_class, tier, mode,
                       score, direction, alert_type, telegram_status
                  FROM signal_alerts
                 WHERE sent_at >= ? AND sent_at <= ?
                 ORDER BY sent_at
                """,
                (start, end),
            ).fetchall()
            for row in sa_rows:
                d = dict(row)
                d["_ledger"] = "signal_alerts"
                review.telegram_alerts.append(d)
        except sqlite3.OperationalError:
            # Stocks signal_alerts ledger may not exist on very old DBs.
            pass

        # Outcomes booked today (from signal_outcomes).
        try:
            outcomes = conn.execute(
                """
                SELECT outcome, COUNT(*) AS n
                  FROM signal_outcomes
                 WHERE evaluated_at >= ? AND evaluated_at <= ?
                 GROUP BY outcome
                """,
                (start, end),
            ).fetchall()
            review.outcomes_today = {r["outcome"]: int(r["n"]) for r in outcomes}
        except sqlite3.OperationalError:
            review.outcomes_today = {}

    return review


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_daily_review(data: DailyReviewData) -> str:
    """Render a Daily_Review markdown note. No external deps; pure text."""

    lines: list[str] = []
    lines.append(f"# Daily Review — {data.date}")
    lines.append("")
    lines.append(
        f"_Auto-generated by `review-day --write-obsidian` "
        f"at {datetime.now(timezone.utc).isoformat()}._"
    )
    lines.append("")

    # 1. Headline counts.
    lines.append("## Desk Output Headlines")
    if data.counts_by_asset_class:
        for ac, tiers in sorted(data.counts_by_asset_class.items()):
            parts = [f"{tier}={n}" for tier, n in sorted(tiers.items())]
            lines.append(f"- **{ac}**: {', '.join(parts)}")
    else:
        lines.append("- No signals registered today.")
    lines.append("")

    # 2. Reports written.
    lines.append("## Reports Generated")
    if data.reports_written:
        for r in data.reports_written:
            rid = r.get("report_id") or "?"
            n = r.get("n_ideas") or 0
            first = (r.get("first_seen") or "")[:19]
            lines.append(f"- `{rid}` — {n} ideas (first seen {first})")
    else:
        lines.append("- None.")
    lines.append("")

    # 3. A-tier signals.
    lines.append("## A-tier signals")
    a = data.signals_by_tier.get("A") or []
    if a:
        for sig in a:
            sym = sig.get("symbol")
            d = sig.get("direction")
            m = sig.get("mode")
            ac = sig.get("asset_class")
            score = sig.get("score")
            status = sig.get("status")
            inv = sig.get("invalidation")
            lines.append(
                f"- **{sym}** ({ac}/{m}/{d}) score `{score}`, "
                f"status `{status}`, inv `{inv}`"
            )
    else:
        lines.append("- None.")
    lines.append("")

    # 4. B-tier signals.
    lines.append("## B-tier signals")
    b = data.signals_by_tier.get("B") or []
    if b:
        for sig in b:
            sym = sig.get("symbol")
            d = sig.get("direction")
            m = sig.get("mode")
            ac = sig.get("asset_class")
            score = sig.get("score")
            lines.append(f"- {sym} ({ac}/{m}/{d}) score `{score}`")
    else:
        lines.append("- None.")
    lines.append("")

    # 5. Telegram alerts.
    lines.append("## Telegram alerts fired")
    if data.telegram_alerts:
        for a in data.telegram_alerts:
            ts = (a.get("sent_at") or "")[:19]
            sym = a.get("symbol")
            tier = a.get("new_tier") or a.get("tier")
            direction = a.get("direction")
            mode = a.get("mode") or "?"
            ledger = a.get("_ledger", "?")
            atype = a.get("alert_type") or "alert"
            lines.append(
                f"- `{ts}` **{sym}** ({tier}/{direction}/{mode}) "
                f"`{atype}` ({ledger})"
            )
    else:
        lines.append("- None.")
    lines.append("")

    # 6. Outcomes booked today.
    lines.append("## Outcomes booked today")
    if data.outcomes_today:
        for outcome, n in sorted(data.outcomes_today.items()):
            lines.append(f"- {outcome}: {n}")
    else:
        lines.append("- None.")
    lines.append("")

    # 7. PART 3 legal-block surface.
    lines.append("## Legal / headline-risk blocks")
    if data.legal_blocks:
        for lb in data.legal_blocks:
            lines.append(
                f"- **{lb['symbol']}** ({lb['asset_class']}/{lb['tier']}) — "
                f"`{lb['marker']}`"
            )
    else:
        lines.append("- None.")
    lines.append("")

    # 8. Manual review hooks (left blank).
    lines.append("## Manual notes")
    lines.append("- What I took / skipped:")
    lines.append("- What the desk got right today:")
    lines.append("- What it got wrong:")
    lines.append("- Lessons / follow-ups:")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "_Source: `proposed_signals`, `watchlist_alerts`, `signal_alerts`, "
        "`signal_outcomes`. Advisory-only export; no auto-trade implications._"
    )

    return "\n".join(lines) + "\n"
