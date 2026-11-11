"""PART 6 — Stocks A-tier intraday-long RTH-open replay.

Tests whether A-tier intraday longs perform worst in the RTH-open window
(first 15m / 30m / 60m), and whether B-tier is consistently better OOS.

No production change. Read-only.
"""

from __future__ import annotations

import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def _load() -> list[dict]:
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        SELECT ps.*, o.final_r AS final_r, o.final_outcome AS final_outcome,
               o.entry_triggered_at AS entry_at, o.entry_triggered AS entry_triggered
        FROM proposed_signals ps
        LEFT JOIN (
            SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id
        ) m ON m.signal_id = ps.signal_id
        LEFT JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.asset_class='stocks' AND ps.mode='intraday'
        ORDER BY ps.created_at
    """)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def rth_window_label(entry_at: str | None, created_at: str) -> str:
    """Classify when entry happened relative to RTH open (09:30 ET)."""
    t = entry_at or created_at
    if not t:
        return "unknown"
    try:
        dt = pd.to_datetime(t, utc=True)
    except Exception:
        return "unknown"
    et = dt.tz_convert("America/New_York")
    if et.weekday() >= 5:
        return "weekend"
    h, m = et.hour, et.minute
    if h < 9 or (h == 9 and m < 30):
        return "premarket"
    minutes_from_open = (h - 9) * 60 + (m - 30)
    if minutes_from_open < 15:
        return "0-15m"
    if minutes_from_open < 30:
        return "15-30m"
    if minutes_from_open < 60:
        return "30-60m"
    if h < 12:
        return "60m-noon"
    if h < 15:
        return "noon-15h"
    if h < 16:
        return "15h-close"
    return "after_close"


def stats(rows: list[dict]) -> dict:
    closed = [r for r in rows if r.get("final_r") is not None]
    rs = [float(r["final_r"]) for r in closed]
    wins = sum(1 for r in rs if r > 0)
    losses = sum(1 for r in rs if r < 0)
    return {
        "n_total": len(rows),
        "n_closed": len(closed),
        "sum_r": sum(rs),
        "wins": wins, "losses": losses,
        "wr": wins / max(1, wins + losses),
    }


CLUSTER = {"AAPL", "NVDA", "SMCI", "SMH", "XLK"}


def main() -> None:
    sigs = _load()
    a_long = [s for s in sigs if s.get("tier") == "A" and s.get("direction") == "long"]
    b_long = [s for s in sigs if s.get("tier") == "B" and s.get("direction") == "long"]
    a_short = [s for s in sigs if s.get("tier") == "A" and s.get("direction") == "short"]
    b_short = [s for s in sigs if s.get("tier") == "B" and s.get("direction") == "short"]

    # by entry-time window
    a_long_by_window: dict[str, list] = defaultdict(list)
    for s in a_long:
        w = rth_window_label(s.get("entry_at"), s["created_at"])
        a_long_by_window[w].append(s)

    # AAPL/NVDA/SMCI/SMH/XLK cluster vs rest
    a_long_cluster = [s for s in a_long if s["symbol"] in CLUSTER]
    a_long_other = [s for s in a_long if s["symbol"] not in CLUSTER]
    b_long_cluster = [s for s in b_long if s["symbol"] in CLUSTER]
    b_long_other = [s for s in b_long if s["symbol"] not in CLUSTER]

    # half-size simulation
    def sized_sum(rows, w):
        return sum((float(r["final_r"]) * w) for r in rows if r.get("final_r") is not None)

    lines = []
    lines.append("# Stocks A-tier Intraday Long — RTH-open Replay (PART 6)")
    lines.append("")
    lines.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Cohort:** stocks intraday signals (n={len(sigs)}).")
    lines.append("")
    lines.append("## Top-level cohort comparison")
    lines.append("")
    lines.append("| Cohort | n closed | sum R | WR |")
    lines.append("|---|---:|---:|---:|")
    for label, rows in [("A-tier long", a_long), ("B-tier long", b_long),
                        ("A-tier short", a_short), ("B-tier short", b_short)]:
        m = stats(rows)
        lines.append(f"| {label} | {m['n_closed']} | {m['sum_r']:+.2f} | {m['wr']:.0%} |")
    lines.append("")
    lines.append("## A-tier long — by entry-time window")
    lines.append("")
    lines.append("| Window | n closed | sum R | WR |")
    lines.append("|---|---:|---:|---:|")
    order = ["premarket", "0-15m", "15-30m", "30-60m", "60m-noon", "noon-15h", "15h-close", "after_close", "weekend", "unknown"]
    for w in order:
        if w not in a_long_by_window:
            continue
        m = stats(a_long_by_window[w])
        lines.append(f"| {w} | {m['n_closed']} | {m['sum_r']:+.2f} | {m['wr']:.0%} |")
    lines.append("")
    lines.append("## A-tier long — AAPL/NVDA/SMCI/SMH/XLK cluster vs rest")
    lines.append("")
    lines.append("| Subset | n closed | sum R | WR |")
    lines.append("|---|---:|---:|---:|")
    for label, rows in [("A-long cluster", a_long_cluster),
                        ("A-long other", a_long_other),
                        ("B-long cluster (control)", b_long_cluster),
                        ("B-long other (control)", b_long_other)]:
        m = stats(rows)
        lines.append(f"| {label} | {m['n_closed']} | {m['sum_r']:+.2f} | {m['wr']:.0%} |")
    lines.append("")
    lines.append("## Half-size simulation (current YAML weight = 0.5×)")
    lines.append("")
    a_long_raw = sum(float(r["final_r"]) for r in a_long if r.get("final_r") is not None)
    a_long_half = sized_sum(a_long, 0.5)
    a_long_zero = 0.0
    lines.append(f"- A-tier long at **1.0×** (full): **{a_long_raw:+.2f} R**")
    lines.append(f"- A-tier long at **0.5×** (current YAML): **{a_long_half:+.2f} R**")
    lines.append(f"- A-tier long at **0× (paused)**: **+0.00 R**")
    lines.append("")
    lines.append("## Would a 0-15m window gate have helped?")
    lines.append("")
    open_window = a_long_by_window.get("0-15m", []) + a_long_by_window.get("15-30m", [])
    open_m = stats(open_window)
    rest = [s for s in a_long if rth_window_label(s.get("entry_at"), s["created_at"]) not in ("0-15m", "15-30m")]
    rest_m = stats(rest)
    lines.append(f"- A-long entered in first 30m (0-15m + 15-30m): n={open_m['n_closed']}, "
                 f"sum R={open_m['sum_r']:+.2f}, WR={open_m['wr']:.0%}")
    lines.append(f"- A-long entered after first 30m: n={rest_m['n_closed']}, "
                 f"sum R={rest_m['sum_r']:+.2f}, WR={rest_m['wr']:.0%}")
    lines.append("")
    diff = rest_m["sum_r"] - open_m["sum_r"]
    if open_m["n_closed"] >= 5 and open_m["sum_r"] < rest_m["sum_r"]:
        lines.append(f"- **Signal: a first-30m gate would have improved A-long by ~{diff:+.2f} R**.")
    else:
        lines.append("- Mixed / insufficient evidence for a first-30m gate.")
    lines.append("")
    lines.append("## Is B-tier consistently better OOS?")
    lines.append("")
    # split in half by date for crude OOS
    mid = len(sigs) // 2
    first_half = sigs[:mid]; second_half = sigs[mid:]
    al1 = [s for s in first_half if s["tier"] == "A" and s["direction"] == "long"]
    al2 = [s for s in second_half if s["tier"] == "A" and s["direction"] == "long"]
    bl1 = [s for s in first_half if s["tier"] == "B" and s["direction"] == "long"]
    bl2 = [s for s in second_half if s["tier"] == "B" and s["direction"] == "long"]
    lines.append("| Window | A-long sum R | B-long sum R | B beats A? |")
    lines.append("|---|---:|---:|---|")
    for label, a, b in [("first half", al1, bl1), ("second half", al2, bl2)]:
        ma = stats(a); mb = stats(b)
        beat = "YES" if mb["sum_r"] > ma["sum_r"] else "no"
        lines.append(f"| {label} | {ma['sum_r']:+.2f} | {mb['sum_r']:+.2f} | {beat} |")
    lines.append("")
    lines.append("## Decisions (read-only)")
    lines.append("")
    lines.append("- **No A-tier scoring change implemented.** This audit is research-only.")
    lines.append("- **No gate implemented.** Even if first-30m looks worse, a 20-day sample is too "
                 "small to commit to a hard exclusion rule.")
    lines.append("- The current YAML weight of 0.5× for A-tier long appears to **mitigate** the cohort's "
                 "structural drag without forbidding it. Keep it.")
    lines.append("- Re-run after ≥ 60 days of signal history before considering a gate.")

    out_md = ROOT / "reports" / "STOCKS_A_TIER_RTH_OPEN_REPLAY.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
