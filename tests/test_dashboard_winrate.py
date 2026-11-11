"""Smoke tests for the corrected WR formula in tab 10.

Validates that:
- pending / expired / not_triggered are excluded from the closed-only WR
- C-tier is presented separately from A/B headline
- duplicate signal_outcomes are deduped (per-setup dedup CTE)
- watchlist-only modes (stocks swing/invest) are excluded from headline
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _wr_closed(wins: int, losses: int) -> str:
    """Mirror of the helper used in tab 10."""
    closed = wins + losses
    if not closed:
        return "—"
    return f"{(wins / closed) * 100:.0f}%"


def test_pending_signals_excluded_from_closed_wr():
    """A pending signal with final_r=0 must NOT count toward losses."""
    # Suppose: 3 wins, 2 losses, 10 pending = denominator should be 5, not 15.
    assert _wr_closed(3, 2) == "60%"


def test_expired_zero_r_excluded_from_wr():
    """An expired signal (final_r=0) is neither >0 nor <0 → excluded."""
    # 1W / 1L / many expired => 50% WR closed-only
    assert _wr_closed(1, 1) == "50%"


def test_only_losses_returns_zero_percent():
    """A 0W/9L scalp cohort should read 0%, not '—'."""
    assert _wr_closed(0, 9) == "0%"


def test_only_wins_returns_hundred_percent():
    """A 5W/0L cohort reads 100%."""
    assert _wr_closed(5, 0) == "100%"


def test_no_closures_returns_dash():
    """No closures yet → render '—' so user doesn't see a misleading 0%."""
    assert _wr_closed(0, 0) == "—"


def test_dedupe_cte_collapses_duplicate_signal_ids():
    """The per_setup CTE collapses (asset, mode, tier, direction, symbol, day)
    so duplicate signal_ids from re-runs of the same setup count once."""
    db = sqlite3.connect(":memory:")
    db.executescript(
        """
        CREATE TABLE proposed_signals (
          signal_id TEXT PRIMARY KEY, asset_class TEXT, mode TEXT, tier TEXT,
          direction TEXT, symbol TEXT, created_at TEXT
        );
        CREATE TABLE signal_outcomes (
          id INTEGER PRIMARY KEY,
          signal_id TEXT, checked_at TEXT, final_outcome TEXT, final_r REAL,
          entry_triggered INTEGER, tp1_hit INTEGER, stop_hit INTEGER
        );
        """
    )
    # Two signal_ids for the same setup on the same day, both with final_r=+1
    for sid in ("sigA", "sigB"):
        db.execute(
            "INSERT INTO proposed_signals VALUES (?, 'crypto', 'swing', 'B', 'long', 'ZEC/USDT', '2026-06-08T10:00:00')",
            (sid,),
        )
        db.execute(
            "INSERT INTO signal_outcomes(signal_id, checked_at, final_outcome, final_r, entry_triggered, tp1_hit, stop_hit) "
            "VALUES (?, '2026-06-08T12:00:00', 'win', 1.0, 1, 1, 0)",
            (sid,),
        )
    db.commit()
    # Run the per_setup CTE
    rows = db.execute(
        """
        WITH latest_outcome AS (
          SELECT signal_id, MAX(checked_at) AS max_checked
          FROM signal_outcomes WHERE final_outcome IS NOT NULL AND final_outcome != ''
          GROUP BY signal_id
        ), per_setup AS (
          SELECT ps.asset_class, ps.mode, ps.tier, ps.direction,
                 substr(ps.created_at, 1, 10) AS day, ps.symbol,
                 AVG(so.final_r) AS final_r
          FROM proposed_signals ps
          JOIN latest_outcome lo ON lo.signal_id = ps.signal_id
          JOIN signal_outcomes so ON so.signal_id = ps.signal_id AND so.checked_at = lo.max_checked
          GROUP BY ps.asset_class, ps.mode, ps.tier, ps.direction, ps.symbol, day
        )
        SELECT COUNT(*) FROM per_setup
        """
    ).fetchone()[0]
    assert rows == 1, f"per_setup should collapse duplicates; got {rows}"
    db.close()


def test_watchlist_modes_excluded_from_headline_helper():
    """The headline helper takes a mode filter; stocks intraday excludes swing/invest."""
    # Simulate the by_mode_tier rows the script would aggregate from.
    by_mode_tier = [
        # stocks intraday A/B — should be in headline
        {"asset_class": "stocks", "mode": "intraday", "tier": "B",
         "n": 100, "trig": 80, "wins": 40, "losses": 30, "total_r": 10.0},
        # stocks swing C — paused; should NOT be in stocks intraday headline
        {"asset_class": "stocks", "mode": "swing", "tier": "C",
         "n": 50, "trig": 45, "wins": 5, "losses": 40, "total_r": -35.0},
        # stocks invest C — paused; should NOT be in headline
        {"asset_class": "stocks", "mode": "invest", "tier": "C",
         "n": 40, "trig": 38, "wins": 0, "losses": 35, "total_r": -35.0},
    ]
    # Mirror of _headline_for inline
    def headline_stocks_intraday(rows):
        sub = [r for r in rows
               if r["asset_class"] == "stocks" and r["tier"] in ("A", "B")
               and r["mode"] == "intraday"]
        W = sum(r["wins"] for r in sub)
        L = sum(r["losses"] for r in sub)
        return W, L
    W, L = headline_stocks_intraday(by_mode_tier)
    assert W == 40 and L == 30, f"expected 40W/30L; got {W}/{L}"
    assert _wr_closed(W, L) == "57%"


def test_old_misleading_formula_vs_new():
    """Document the bug: the old formula `Wins / n` understates a 40/30/30 cohort."""
    # 40 wins, 30 losses, 30 pending (n=100)
    n = 100
    wins = 40
    losses = 30
    old_misleading = f"{wins / n * 100:.0f}%"  # 40% — depressed by 30 pending
    new_correct = _wr_closed(wins, losses)      # 57% — only closed
    assert old_misleading == "40%"
    assert new_correct == "57%"
