"""Recent Signal Performance section — shared between crypto + stocks reports.

This module produces a compact Markdown block that summarises the desk's recent
signal outcomes. It is **read-only**: rendering it never mutates the registry
and never feeds back into scoring or rule changes.

Used by:
- ``src/reports/report_builder.py`` (crypto)
- ``src/stocks/reports/stocks_report_builder.py`` (stocks)
- ``src/analysis/packet.py`` (crypto LLM packet, via the existing helper)
- ``src/stocks/llm_packet.py`` (stocks LLM packet, via the existing helper)
"""

from __future__ import annotations

from typing import Any


def build_signal_performance_block(
    config,
    *,
    asset_class: str,
    period: str = "week",
    title: str = "Recent Signal Performance",
) -> str:
    """Return a compact Markdown section for the given asset_class.

    Schema:
        ## <title>
        - Period: week
        - Asset class: crypto
        - Sample size: 19 (confidence=weak)
        - A-tier: 8 | B-tier: 8 | C-tier: 3
        - Triggered: 0 / 19 (0.0%)
        - Wins: 0 | Losses: 0 | Ambiguous: 0
        - TP1 hit rate: n/a | Stop hit rate: n/a
        - Triggered winrate: n/a | Avg R: n/a | Total R: 0.0 | PF: n/a
        - Active right now: 19
        - Note: sample sizes are still small — treat metrics as anecdotal.

    Failure-safe: if the analytics layer raises (e.g. missing tables) the
    section returns a one-line "unavailable" stub so report generation keeps
    going.
    """

    # The signal performance block is a feedback panel. It must:
    #   - never mutate state;
    #   - never crash the surrounding report;
    #   - but ALSO never silently mask a schema bug — that hid the
    #     wrong-table issue caught in the audit verification.
    # Strategy: catch only ImportError / DB connection / analytics layer
    # failures into a visible "unavailable" stub; let assertion + value
    # errors propagate to the surrounding report builder where the test
    # suite will see them.
    import logging
    import sqlite3

    log = logging.getLogger("crypto_ai_desk")

    try:
        from src.signals.analytics import headline_split
        from src.signals.config import load_signal_tracking_config
        from src.storage.sqlite import SQLiteStore

        cfg = load_signal_tracking_config(config.root)
        store = SQLiteStore(config.db_path)
        store.init_db()
        # R1: headline performance reflects ACTIONABLE (A/B) signals only.
        # C-tier is watchlist/research quality (never Telegram-actionable) and
        # is reported separately so its losses don't dilute the headline PF.
        split = headline_split(store, config=cfg, period=period, asset_class=asset_class)
        ab = split["actionable"]
        c = split["watchlist"]
        allt = split["all_tier"]
        by_tier = split["by_tier"]

        active_ab = _count_active_signals(store, asset_class=asset_class, tiers=("A", "B"))
        active_c = _count_active_signals(store, asset_class=asset_class, tiers=("C",))

        def _trig_pct(s):
            n = int(s.get("sample_size") or 0)
            t = int(s.get("triggered") or 0)
            return f"{100.0 * t / n:.1f}%" if n > 0 else "n/a"

        lines: list[str] = [f"## {title}"]
        lines.append(f"- Period: {period} | Asset class: {asset_class}")

        # --- Headline: actionable A/B only ---
        lines.append("")
        lines.append("### Headline — Actionable Performance (A/B only)")
        lines.append(
            f"- Sample: {ab.get('sample_size', 0)} "
            f"(confidence={ab.get('confidence_level', 'anecdotal')}) | "
            f"Active now: {active_ab}"
        )
        lines.append(
            f"- Triggered: {ab.get('triggered', 0)} / {ab.get('sample_size', 0)} "
            f"({_trig_pct(ab)}) | Wins: {ab.get('wins', 0)} | Losses: {ab.get('losses', 0)}"
        )
        lines.append(
            f"- Winrate: {_fmt_pct(ab.get('winrate_triggered'))} | "
            f"Avg R: {_fmt_num(ab.get('average_r'))} | "
            f"Total R: {_fmt_num(ab.get('total_r'))} | "
            f"PF: {_fmt_num(ab.get('profit_factor'))} | "
            f"TP1: {_fmt_pct(ab.get('tp1_rate'))} | Stop: {_fmt_pct(ab.get('stop_rate'))}"
        )

        # --- C-tier watchlist / research, kept out of the headline ---
        lines.append("")
        lines.append("### C-tier Watchlist / Research Performance")
        lines.append(
            f"- Sample: {c.get('sample_size', 0)} "
            f"(confidence={c.get('confidence_level', 'anecdotal')}) | Active now: {active_c}"
        )
        lines.append(
            f"- Triggered: {c.get('triggered', 0)} | Wins: {c.get('wins', 0)} | "
            f"Losses: {c.get('losses', 0)} | Winrate: {_fmt_pct(c.get('winrate_triggered'))}"
        )
        lines.append(
            f"- Avg R: {_fmt_num(c.get('average_r'))} | "
            f"Total R: {_fmt_num(c.get('total_r'))} | PF: {_fmt_num(c.get('profit_factor'))}"
        )
        lines.append(
            "- Note: C-tier is watchlist/research quality, **not** "
            "Telegram-actionable. Excluded from the headline metric."
        )

        # --- Tier split ---
        lines.append("")
        lines.append("### Tier split")
        for t in ("A", "B", "C"):
            s = by_tier.get(t, {})
            lines.append(
                f"- {t}-tier: n={s.get('sample_size', 0)} | "
                f"Total R: {_fmt_num(s.get('total_r'))} | "
                f"PF: {_fmt_num(s.get('profit_factor'))} | "
                f"Winrate: {_fmt_pct(s.get('winrate_triggered'))}"
            )

        # --- All-tier diagnostic (NOT the headline) ---
        lines.append("")
        lines.append("### All-tier diagnostic (A/B/C — not the headline metric)")
        lines.append(
            f"- Sample: {allt.get('sample_size', 0)} | "
            f"Total R: {_fmt_num(allt.get('total_r'))} | "
            f"PF: {_fmt_num(allt.get('profit_factor'))} | "
            f"Winrate: {_fmt_pct(allt.get('winrate_triggered'))}"
        )

        ab_sample = int(ab.get("sample_size") or 0)
        lines.append("")
        if ab_sample < 10:
            lines.append("- Note: A/B sample is anecdotal (<10). Do not tune strategy on it.")
        elif ab_sample < 30:
            lines.append("- Note: A/B sample is weak (10–29). Directional only.")
        elif ab_sample < 50:
            lines.append("- Note: A/B sample is moderate (30–49). Wider sample needed before tuning.")
        else:
            lines.append("- Note: A/B sample is large enough for trend analysis. Still review manually.")
        lines.append(
            "- Strategy is **not** auto-modified from these numbers. "
            "Treat as feedback context only."
        )
        return "\n".join(lines)
    except (ImportError, sqlite3.Error) as exc:
        # Genuine "feature unavailable" — log it loud so the dev sees it,
        # but do not crash the report.
        log.warning(
            "signal performance block unavailable (%s): %s",
            exc.__class__.__name__,
            exc,
        )
        return (
            f"## {title}\n"
            f"- Asset class: {asset_class}\n"
            f"- Status: unavailable ({exc.__class__.__name__})\n"
            f"- Note: signal-stats could not be computed; reporter continued without it."
        )


#: Status set matching ``SQLiteStore.load_active_signals`` — these are the
#: states that mean "this proposed signal still matters" (not closed, not
#: stopped, not expired, not missed). Kept in sync with the registry.
_ACTIVE_SIGNAL_STATUSES: tuple[str, ...] = (
    "generated",
    "waiting_for_entry",
    "triggered",
    "tp1_hit",
    "tp2_hit",
)


def _count_active_signals(store, *, asset_class: str, tiers: tuple[str, ...] | None = None) -> int:
    """Count proposed signals still in an active state for the asset class.

    Queries the canonical ``proposed_signals`` registry table. Raises on
    schema mismatch so the caller can flag the issue — silent fallbacks were
    masking a wrong-table bug (see REPORT_SECTION_FIX_REPORT.md).

    R1: optional ``tiers`` restricts the count (e.g. ("A","B") for the
    actionable headline, ("C",) for the watchlist block).
    """
    placeholders = ",".join("?" for _ in _ACTIVE_SIGNAL_STATUSES)
    sql = (
        "SELECT COUNT(*) AS n FROM proposed_signals "
        f"WHERE asset_class = ? AND status IN ({placeholders})"
    )
    params: tuple = (asset_class, *_ACTIVE_SIGNAL_STATUSES)
    if tiers:
        tier_ph = ",".join("?" for _ in tiers)
        sql += f" AND UPPER(tier) IN ({tier_ph})"
        params = (*params, *(t.upper() for t in tiers))
    with store.connect() as conn:
        row = conn.execute(sql, params).fetchone()
    if row is None:
        return 0
    # sqlite3.Row supports both index and key access.
    try:
        return int(row["n"])
    except (TypeError, KeyError, IndexError):
        return int(row[0])


def _fmt_pct(value: Any) -> str:
    if value is None:
        return "n/a"
    try:
        f = float(value)
    except (TypeError, ValueError):
        return "n/a"
    return f"{f * 100:.1f}%" if abs(f) <= 1.0 else f"{f:.1f}%"


def _fmt_num(value: Any) -> str:
    if value is None:
        return "n/a"
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(f) >= 100:
        return f"{f:.0f}"
    if abs(f) >= 1:
        return f"{f:.2f}"
    return f"{f:.3f}"
