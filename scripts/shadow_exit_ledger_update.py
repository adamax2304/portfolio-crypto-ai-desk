"""Shadow exit ledger update (FAST SAFE ACCELERATION PART 3).

Read-only over the trading DB. For each closed crypto intraday/swing trade, computes
all shadow exit variants (archive-first OHLCV) and append-merges them into
data/reports/shadow_exit_ledger.csv, idempotent by (signal_id, variant). Missing
OHLCV → coverage_status='missing_data' (never faked). Never changes real exits.
"""
from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.exits.shadow_exit_manager import load_path, shadow_rows_for_trade  # noqa: E402

DB = ROOT / "db" / "crypto_ai_desk.sqlite"
LEDGER = ROOT / "data" / "reports" / "shadow_exit_ledger.csv"
LOOKBACK_DAYS = 60
FIELDS = ["signal_id", "symbol", "asset_class", "mode", "tier", "direction",
          "entry_time", "exit_time", "entry", "stop", "tp", "actual_R", "variant",
          "shadow_R", "exit_reason", "touched_0_5R", "touched_1R", "moved_to_BE",
          "partial_taken_time", "stopped_after_BE", "winner_clipped", "loser_saved",
          "data_timeframe_used", "data_coverage_status"]


def load_trades(conn, since_ts):
    rows = conn.execute(
        """
        SELECT s.signal_id, s.symbol, s.asset_class, s.mode, s.tier, s.direction,
               s.entry_low, s.suggested_entry, s.entry_trigger, s.stop_loss,
               s.invalidation, s.tp1, s.tp2, s.tp3, s.created_at,
               o.entry_triggered_at, o.entry_price_used, o.final_r,
               COALESCE(o.stop_hit_at, o.tp3_hit_at, o.tp2_hit_at, o.tp1_hit_at,
                        o.checked_at) AS exit_at
        FROM proposed_signals s
        JOIN signal_outcomes o ON o.signal_id = s.signal_id
        WHERE o.id IN (SELECT MAX(id) FROM signal_outcomes GROUP BY signal_id)
          AND (s.asset_class='crypto' OR s.asset_class IS NULL)
          AND s.mode IN ('intraday','swing')
          AND o.entry_triggered=1
          AND o.final_outcome IN ('win','loss','partial_win')
        """).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        try:
            ct = datetime.fromisoformat(str(d["created_at"]).replace("Z", "+00:00"))
        except Exception:
            continue
        if ct.timestamp() >= since_ts:
            out.append(d)
    return out


def existing_keys():
    keys = set()
    if LEDGER.exists():
        try:
            for row in csv.DictReader(LEDGER.open(encoding="utf-8")):
                keys.add((row.get("signal_id"), row.get("variant")))
        except Exception:
            pass
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="cap trades processed (0=all)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    conn = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    trades = load_trades(conn, now.timestamp() - LOOKBACK_DAYS * 86400)
    conn.close()
    if args.limit:
        trades = trades[: args.limit]

    have = existing_keys()
    new_rows = []
    covered = missing = 0
    for t in trades:
        entry = (t["entry_price_used"] or t["suggested_entry"]
                 or t["entry_trigger"] or t["entry_low"])
        stop = t["stop_loss"] or t["invalidation"]
        trade = {
            "signal_id": t["signal_id"], "symbol": t["symbol"],
            "asset_class": t["asset_class"] or "crypto", "mode": t["mode"],
            "tier": t["tier"], "direction": t["direction"],
            "entry_time": t["entry_triggered_at"], "exit_time": t["exit_at"],
            "entry": entry, "stop": stop, "tp1": t["tp1"], "tp2": t["tp2"], "tp3": t["tp3"],
            "actual_R": t["final_r"],
        }
        df, ex, tf = load_path(t["symbol"])
        candles = None
        coverage_status = "missing_data"
        if df is not None and t["entry_triggered_at"]:
            try:
                import pandas as pd
                edt = pd.to_datetime(t["entry_triggered_at"], utc=True)
                xdt = pd.to_datetime(t["exit_at"], utc=True) if t["exit_at"] else None
                walk = df[df["timestamp"] >= edt]
                if len(walk):
                    candles = walk.to_dict("records")
                    # "covered" ONLY if the window spans entry AND reaches the exit
                    # (otherwise the path is truncated → partial, not decision-grade).
                    spans_entry = df["timestamp"].min() <= edt
                    reaches_exit = (xdt is None) or (df["timestamp"].max() >= xdt)
                    coverage_status = "covered" if (spans_entry and reaches_exit) else "partial_data"
            except Exception:
                candles = None
        if coverage_status == "covered":
            covered += 1
        else:
            missing += 1
        for row in shadow_rows_for_trade(trade, candles, exchange=ex, tf=tf,
                                         coverage_status=coverage_status):
            if (row["signal_id"], row["variant"]) in have:
                continue
            new_rows.append(row)

    summary = {"trades": len(trades), "covered": covered, "missing_data": missing,
               "new_ledger_rows": len(new_rows), "dry_run": args.dry_run}
    if not args.dry_run and new_rows:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        write_header = not LEDGER.exists()
        with LEDGER.open("a", newline="", encoding="utf-8") as fo:
            w = csv.DictWriter(fo, fieldnames=FIELDS, extrasaction="ignore")
            if write_header:
                w.writeheader()
            w.writerows(new_rows)
    import json
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
