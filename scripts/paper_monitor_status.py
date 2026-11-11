"""Paper Monitor Status — honest, lifecycle-aware Telegram/report summary (read-only).

Replaces the confusing "active trades: none / Expired: N / +0R" style with the
canonical display taxonomy: open-actionable vs waiting vs entered-unresolved vs
review/shadow vs no-entry, and an explicit `expired` split. Read-only on the DB;
NEVER changes any trade field. Safe to run manually or add as a scheduler step.

Usage:
  python -m scripts.paper_monitor_status                 # print
  python -m scripts.paper_monitor_status --send-telegram # push compact summary
  python -m scripts.paper_monitor_status --write-report  # reports/PAPER_MONITOR_STATUS_LATEST.md
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.status.display_status import (  # noqa: E402
    derive_display_status,
    format_paper_monitor_status,
    summarize_display_states,
)

DB = ROOT / "db" / "crypto_ai_desk.sqlite"
REPORT = ROOT / "reports" / "PAPER_MONITOR_STATUS_LATEST.md"
ACTIVE = ("generated", "waiting_for_entry", "triggered", "tp1_hit", "tp2_hit")


def load_rows(window_days: int = 1) -> list[dict]:
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    has_paper = bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='paper_execution_outcomes'"
    ).fetchone())
    paper_select = (
        ", pe.paper_execution_r, pe.paper_execution_outcome, "
        "pe.close_reason AS paper_close_reason, pe.evidence_class AS paper_evidence_class"
        if has_paper else
        ", NULL AS paper_execution_r, NULL AS paper_execution_outcome, "
        "NULL AS paper_close_reason, NULL AS paper_evidence_class"
    )
    paper_join = ("LEFT JOIN paper_execution_outcomes pe ON pe.signal_id = p.signal_id"
                  if has_paper else "")
    ph = ",".join("?" * len(ACTIVE))
    q = f"""
        WITH candidate_signals AS (
            SELECT signal_id, symbol, direction, asset_class, mode, tier,
                   status, created_at, updated_at
            FROM proposed_signals
            WHERE status IN ({ph})
               OR updated_at >= datetime('now', ?)
        )
        SELECT p.signal_id, p.symbol, p.direction, p.asset_class, p.mode, p.tier,
               p.status, p.created_at, p.updated_at,
               o.entry_triggered, o.final_outcome, o.final_r,
               (
                   SELECT MAX(m.max_favorable_excursion_r)
                   FROM signal_outcomes m
                   WHERE m.signal_id = p.signal_id
               ) AS max_favorable_excursion_r,
               (SELECT COUNT(*) FROM signal_alerts a WHERE a.signal_id = p.signal_id) AS alerts
               {paper_select}
        FROM candidate_signals p
        -- Resolve the latest outcome only for the monitor's candidate rows.
        -- The former window function ranked every historical outcome first,
        -- making a read-only dashboard wait behind a multi-million-row scan.
        LEFT JOIN signal_outcomes o ON o.id = (
            SELECT latest.id
            FROM signal_outcomes latest
            WHERE latest.signal_id = p.signal_id
            ORDER BY latest.checked_at DESC, latest.id DESC
            LIMIT 1
        )
        {paper_join}
        ORDER BY p.updated_at DESC
    """
    rows = [dict(r) for r in conn.execute(q, (*ACTIVE, f"-{int(window_days)} day"))]
    conn.close()
    return rows


def build_report(rows: list[dict]) -> str:
    s = summarize_display_states(rows)
    c = s["counts"]
    out = [
        "# Paper Monitor Status (latest)",
        "",
        "Lifecycle-aware view. Display semantics only — no trade field changed.",
        "",
        "## Counts by display group",
        "| group | count |", "|---|---|",
    ]
    for g, n in c.items():
        out.append(f"| {g} | {n} |")
    out += [
        "",
        "## Operator splits",
        f"- Open actionable: {s['open_actionable_count']}",
        f"- Waiting for entry: {s['waiting_for_entry_count']}",
        f"- Entered unresolved (expired-after-entry): {s['expired_after_entry_count']}",
        f"- Review/Shadow: {s['review_shadow_count']}",
        f"- No-entry / stale / moved-away: {s['no_entry_expired_count']}",
        f"- Closed: {c['CLOSED_WIN']}W / {c['CLOSED_LOSS']}L / {c['CLOSED_FLAT']}flat",
        f"- Needs review (inconsistent): {s['unknown_inconsistent_count']}",
        "",
        "## Items",
    ]
    for r in s["rows"]:
        d = derive_display_status(r)
        out.append(
            f"- **{r.get('symbol')}** {r.get('direction','')} ({r.get('asset_class')}/"
            f"{r.get('mode')}/{r.get('tier')}) — {d['operator_label']} · "
            f"touched={d['entry_touched']} · alerted={d['paper_alert_sent']} · "
            f"source={d['display_r_source']} · {d['display_reason']}"
        )
    return "\n".join(out)


STATE = ROOT / "data" / "autostart" / "paper_monitor_status_state.json"


def _cooldown_ok(cooldown_min: int) -> bool:
    """True if enough time has passed since the last Telegram send (anti-spam)."""
    if cooldown_min <= 0:
        return True
    try:
        import json
        from datetime import datetime, timezone
        if STATE.exists():
            last = json.loads(STATE.read_text(encoding="utf-8")).get("last_sent")
            if last:
                dt = datetime.fromisoformat(str(last))
                age_min = (datetime.now(timezone.utc) - dt).total_seconds() / 60.0
                if age_min < cooldown_min:
                    print(f"[paper_monitor_status] cooldown {age_min:.0f}<{cooldown_min}m — not sending")
                    return False
    except Exception:
        return True
    return True


def _mark_sent() -> None:
    try:
        import json
        from datetime import datetime, timezone
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps({"last_sent": datetime.now(timezone.utc).isoformat()}),
                         encoding="utf-8")
    except Exception:
        pass


def main() -> int:
    # Windows may expose a cp1252 console even though this report intentionally
    # contains Unicode status symbols. Keep the read-model command from failing
    # after it has successfully computed the lifecycle summary.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--send-telegram", action="store_true")
    ap.add_argument("--write-report", action="store_true")
    ap.add_argument("--window-days", type=int, default=1)
    ap.add_argument("--compact", action="store_true", help="header + key notes only (no item lists)")
    ap.add_argument("--no-items", action="store_true", help="drop per-item lists")
    ap.add_argument("--top-n", type=int, default=5, help="max items per bucket (0 = none)")
    ap.add_argument("--cooldown-min", type=int, default=90,
                    help="min minutes between Telegram sends (anti-spam; 0 = always)")
    args = ap.parse_args()

    rows = load_rows(args.window_days)
    top_n = 0 if args.no_items else args.top_n
    tg = format_paper_monitor_status(rows, top_n=top_n, compact=args.compact)
    print(tg)

    if args.write_report:
        REPORT.write_text(build_report(rows), encoding="utf-8")
        print(f"\n[paper_monitor_status] wrote {REPORT}")

    if args.send_telegram and _cooldown_ok(args.cooldown_min):
        try:
            from src.notifiers.trade_telegram import notifier_for
            n = notifier_for(ROOT)
            if getattr(n, "enabled", False) and getattr(n, "chat_id", None):
                n.send(tg, parse_mode="")
                _mark_sent()
                print("\n[paper_monitor_status] telegram sent")
            else:
                print("\n[paper_monitor_status] telegram not configured; not sent")
        except Exception as exc:  # never fail on telegram
            print(f"\n[paper_monitor_status] telegram send failed: {type(exc).__name__}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
