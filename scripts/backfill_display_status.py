"""Display-status backfill / report (read-only by default).

Reads proposed_signals + their latest outcome, derives the canonical display
group via src.status.display_status, and writes reports/DISPLAY_STATUS_BACKFILL_REPORT.md.

This is PURELY display semantics. It NEVER edits status / entry_triggered /
final_r / final_outcome / alerts or any trading field. It only writes the optional
display_* columns IF they already exist in proposed_signals (they do not by
default → no migration, report-only). Use --add-columns to opt into creating the
optional display-only columns (safe, additive, never touches existing columns).
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.status.display_status import DISPLAY_GROUPS, derive_display_status  # noqa: E402

DB = ROOT / "db" / "crypto_ai_desk.sqlite"
REPORT = ROOT / "reports" / "DISPLAY_STATUS_BACKFILL_REPORT.md"
DISPLAY_COLS = ("display_status", "display_group", "display_reason", "display_updated_at")


def _has_columns(conn: sqlite3.Connection) -> bool:
    cols = {r[1] for r in conn.execute("PRAGMA table_info(proposed_signals)")}
    return all(c in cols for c in DISPLAY_COLS)


def _add_columns(conn: sqlite3.Connection) -> None:
    cols = {r[1] for r in conn.execute("PRAGMA table_info(proposed_signals)")}
    for c in DISPLAY_COLS:
        if c not in cols:
            conn.execute(f"ALTER TABLE proposed_signals ADD COLUMN {c} TEXT")
    conn.commit()


def _rows(conn: sqlite3.Connection, limit: int | None) -> list[dict]:
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
    q = f"""
        SELECT p.signal_id, p.symbol, p.direction, p.asset_class, p.mode, p.tier,
               p.status, p.created_at, p.updated_at,
               o.entry_triggered, o.final_outcome, o.final_r,
               m.max_favorable_excursion_r
               {paper_select}
        FROM proposed_signals p
        -- Use the LATEST outcome row (by checked_at) for entry_triggered/outcome/R so
        -- the display reflects the authoritative final state, not a transient earlier
        -- touch. (MAX(entry_triggered) over all rows produced false inconsistencies.)
        LEFT JOIN (
            SELECT signal_id, entry_triggered, final_outcome, final_r,
                   ROW_NUMBER() OVER (PARTITION BY signal_id
                                      ORDER BY checked_at DESC, id DESC) AS rn
            FROM signal_outcomes
        ) o ON o.signal_id = p.signal_id AND o.rn = 1
        LEFT JOIN (
            SELECT signal_id, MAX(max_favorable_excursion_r) AS max_favorable_excursion_r
            FROM signal_outcomes GROUP BY signal_id
        ) m ON m.signal_id = p.signal_id
        {paper_join}
        ORDER BY p.created_at DESC
    """
    if limit:
        q += f" LIMIT {int(limit)}"
    return [dict(r) for r in conn.execute(q)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="cap rows (default all)")
    ap.add_argument("--add-columns", action="store_true",
                    help="opt-in: create optional display_* columns (additive, safe)")
    ap.add_argument("--write", action="store_true",
                    help="write derived display_* into the columns (requires columns to exist)")
    args = ap.parse_args()

    conn = sqlite3.connect(str(DB))
    if args.add_columns:
        _add_columns(conn)
    cols_present = _has_columns(conn)

    rows = _rows(conn, args.limit)
    counts: Counter = Counter()
    inconsistent: list[dict] = []
    now_iso = datetime.now(timezone.utc).isoformat()
    written = 0

    for r in rows:
        d = derive_display_status(r)
        counts[d["display_group"]] += 1
        if d["display_group"] == "UNKNOWN_INCONSISTENT":
            inconsistent.append({**r, **d})
        if args.write and cols_present:
            conn.execute(
                "UPDATE proposed_signals SET display_status=?, display_group=?, "
                "display_reason=?, display_updated_at=? WHERE signal_id=?",
                (d["display_status"], d["display_group"], d["display_reason"], now_iso,
                 r["signal_id"]),
            )
            written += 1
    if args.write and cols_present:
        conn.commit()
    conn.close()

    total = sum(counts.values())
    lines = [
        "# Display-Status Backfill Report",
        "",
        f"**Generated:** {now_iso} · rows analysed: {total} · "
        f"display columns present: {cols_present} · rows written: {written}",
        "",
        "> Display semantics only. Original `status` / `entry_triggered` / `final_r` / "
        "`final_outcome` are untouched. This is the lifecycle-aware view, not a rewrite.",
        "",
        "## Counts by display group",
        "",
        "| display_group | count |",
        "|---|---|",
    ]
    for g in DISPLAY_GROUPS:
        lines.append(f"| {g} | {counts.get(g, 0)} |")
    lines += [
        "",
        "## Key splits (for reports / Telegram)",
        f"- expired_after_entry_count: **{counts.get('ENTERED_UNRESOLVED_EXPIRED', 0)}**",
        f"- no_entry_expired_count: **{counts.get('NO_ENTRY_EXPIRED', 0)}**",
        f"- open_actionable_count: **{counts.get('OPEN_ACTIVE', 0)}**",
        f"- waiting_for_entry_count: **{counts.get('WAITING_FOR_ENTRY', 0)}**",
        f"- review_shadow_count: **{counts.get('REVIEW_ONLY_SHADOW', 0)}**",
        f"- closed_flat_count: **{counts.get('CLOSED_FLAT', 0)}**",
        f"- unknown_inconsistent_count: **{counts.get('UNKNOWN_INCONSISTENT', 0)}**",
        "",
        "## Inconsistent rows (need review — not auto-fixed)",
    ]
    if inconsistent:
        lines.append("| symbol | mode | status | entry_triggered | display_reason |")
        lines.append("|---|---|---|---|---|")
        for r in inconsistent[:50]:
            lines.append(
                f"| {r.get('symbol')} | {r.get('mode')} | {r.get('status')} | "
                f"{r.get('entry_triggered')} | {r.get('display_reason')} |"
            )
        if len(inconsistent) > 50:
            lines.append(f"| … | … | … | … | (+{len(inconsistent)-50} more) |")
    else:
        lines.append("None. ✅")
    lines += [
        "",
        "## Notes",
        "- `ENTERED_UNRESOLVED_EXPIRED` = `expired` + `entry_triggered=1` → the trade was "
        "entered but didn't hit TP/SL before the window ended (NOT a missed entry).",
        "- `NO_ENTRY_EXPIRED` = no-entry / stale / moved-away / expired-without-touch.",
        "- Inconsistent = a no-entry status carrying `entry_triggered=1`, or an `ambiguous` "
        "status — surfaced for review; the underlying rows are left exactly as-is.",
        "- No migration is required for display; columns are optional (`--add-columns`).",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[backfill_display_status] analysed {total} rows; wrote {REPORT}")
    print(f"  counts: {dict(counts)}")
    print(f"  display columns present: {cols_present}; rows written: {written}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
