"""Circuit-breaker dry-run (operational deploy PART 1).

Read-only. Loads today's terminal outcomes from the live DB and prints the
would-pause circuit-breaker state per asset/mode WITHOUT sending any Telegram and
WITHOUT touching trades. Writes reports/OPERATIONAL_CIRCUIT_BREAKER_DRY_RUN.md.
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.risk.circuit_breaker import evaluate_circuit_breaker  # noqa: E402

DB = ROOT / "db" / "crypto_ai_desk.sqlite"
OUT = ROOT / "reports" / "OPERATIONAL_CIRCUIT_BREAKER_DRY_RUN.md"


def _today_terminal_rows(conn, since_iso):
    rows = conn.execute(
        """
        SELECT o.signal_id, o.final_r, o.final_outcome, o.stop_hit,
               COALESCE(o.stop_hit_at, o.tp3_hit_at, o.tp2_hit_at, o.tp1_hit_at,
                        o.checked_at) AS exit_at,
               s.asset_class, s.mode, s.tier, s.direction, s.market_regime
        FROM signal_outcomes o
        JOIN proposed_signals s ON s.signal_id = o.signal_id
        WHERE o.id IN (SELECT MAX(id) FROM signal_outcomes GROUP BY signal_id)
          AND o.final_outcome IN ('win','loss','partial_win')
          AND COALESCE(o.stop_hit_at, o.tp3_hit_at, o.tp2_hit_at, o.tp1_hit_at,
                       o.checked_at) >= ?
        ORDER BY exit_at ASC
        """,
        (since_iso,),
    ).fetchall()
    return [dict(r) for r in rows]


def main():
    now = datetime.now(timezone.utc)
    since = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    rows = _today_terminal_rows(conn, since)
    conn.close()

    scopes = sorted({(r["asset_class"] or "crypto", r["mode"] or "?") for r in rows})
    lines = [
        "# Circuit Breaker — Dry Run (PART 1)", "",
        f"**As of:** {now.isoformat()} · UTC day start: {since[:10]} · DRY-RUN (no Telegram, no trade effect)",
        f"**Closed (terminal) outcomes today:** {len(rows)}", "",
        "| asset | mode | state | level | day_R | stops | consec | crypto_long_streak | would_pause | reason |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    any_pause = False
    for asset, mode in scopes:
        st = evaluate_circuit_breaker(rows, scope_asset=asset, scope_mode=mode,
                                      scope_regime=None, now=now)
        if st["circuit_breaker_state"] == "would_pause":
            any_pause = True
        lines.append(
            f"| {asset} | {mode} | {st['circuit_breaker_state']} | "
            f"{st['circuit_breaker_level']} | {st['day_realized_r']} | "
            f"{st['stops_today']} | {st['consecutive_stops']} | "
            f"{st['crypto_long_streak_count']} | {st['would_pause_new_entries']} | "
            f"{st['circuit_breaker_reason']} |")
    if not scopes:
        lines.append("| — | — | ok | 0 | 0 | 0 | 0 | 0 | False | no closed trades today |")
    lines += ["",
              f"**Would-pause today:** {'YES — ' if any_pause else 'no'}"
              + ("at least one asset/mode breached the alert-only threshold."
                 if any_pause else "all scopes within thresholds."),
              "",
              "_Dry-run only: this never sends Telegram, never blocks a trade, never changes size/routing._"]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} · scopes={len(scopes)} · would_pause={any_pause}")


if __name__ == "__main__":
    main()
