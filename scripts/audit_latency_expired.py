"""Read-only latency + expired-signal audit (2026-06-16).

Derives entry-detection latency and expired-signal classification tables from the
production SQLite DB. Writes:
  - reports/ENTRY_DETECTION_LATENCY.csv
  - reports/EXPIRED_SIGNAL_DETAILS.csv
and prints summary tables to stdout for the audit reports.

NO writes to the production DB. NO trading. NO history rewrite.
"""

from __future__ import annotations

import csv
import sqlite3
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "crypto_ai_desk.sqlite"
REPORTS = ROOT / "reports"

TERMINAL_STATUSES = {"tp1_hit", "tp2_hit", "tp3_hit", "stopped", "expired", "ambiguous"}
CLOSE_TYPES = {"close_tp", "close_stop", "close_expired", "close_ambiguous", "close_flat"}


def parse(t):
    if not t:
        return None
    try:
        return datetime.fromisoformat(str(t).replace("Z", "+00:00"))
    except Exception:
        return None


def now_utc():
    return datetime.now(timezone.utc)


def pct(n, d):
    return f"{(100.0 * n / d):.1f}%" if d else "—"


def classify_age(age_sec, already_closed):
    if already_closed:
        return "already_closed"
    if age_sec is None:
        return "unknown"
    m = age_sec / 60.0
    if m <= 2:
        return "fresh"
    if m <= 5:
        return "acceptable"
    if m <= 15:
        return "late"
    return "very_late"


def load_entry_rows(db):
    """One row per signal that ever triggered entry, with latency fields."""
    sigs = {r["signal_id"]: dict(r) for r in db.execute(
        "SELECT signal_id, created_at, symbol, mode, asset_class, tier, direction, "
        "news_supported FROM proposed_signals")}
    # outcomes: first entry-detection row + its status, plus entry_triggered_at
    first_entry = {}
    for r in db.execute(
        "SELECT signal_id, checked_at, status, entry_triggered_at, entry_price_used "
        "FROM signal_outcomes WHERE entry_triggered=1 ORDER BY checked_at ASC"):
        sid = r["signal_id"]
        if sid not in first_entry:
            first_entry[sid] = dict(r)
    # paper_entry alert time
    pe_alert = {}
    for r in db.execute(
        "SELECT signal_id, MIN(sent_at) AS sent_at, telegram_status FROM signal_alerts "
        "WHERE alert_type='paper_entry' GROUP BY signal_id"):
        pe_alert[r["signal_id"]] = dict(r)

    rows = []
    for sid, fe in first_entry.items():
        s = sigs.get(sid, {})
        touch = parse(fe.get("entry_triggered_at"))
        detected = parse(fe.get("checked_at"))
        pe = pe_alert.get(sid) or {}
        alert_at = parse(pe.get("sent_at"))
        already_closed = (fe.get("status") in TERMINAL_STATUSES)
        entry_age = (alert_at - touch).total_seconds() if (alert_at and touch) else None
        detect_lag = (detected - touch).total_seconds() if (detected and touch) else None
        emit_lag = (alert_at - detected).total_seconds() if (alert_at and detected) else None
        rows.append({
            "signal_id": sid,
            "asset_class": s.get("asset_class"),
            "mode": s.get("mode"),
            "tier": s.get("tier"),
            "direction": s.get("direction"),
            "news_supported": s.get("news_supported"),
            "created_at": s.get("created_at"),
            "entry_touch_at": fe.get("entry_triggered_at"),
            "tracker_detected_at": fe.get("checked_at"),
            "first_detect_status": fe.get("status"),
            "paper_entry_alert_at": pe.get("sent_at"),
            "paper_entry_status": pe.get("telegram_status"),
            "entry_price_used": fe.get("entry_price_used"),
            "detection_lag_sec": round(detect_lag) if detect_lag is not None else "",
            "alert_emit_lag_sec": round(emit_lag) if emit_lag is not None else "",
            "entry_age_sec": round(entry_age) if entry_age is not None else "",
            "already_closed_same_tick": int(already_closed),
            "classification": classify_age(entry_age, already_closed),
            "_touch_dt": touch,
        })
    return rows


def latency_audit(db):
    rows = load_entry_rows(db)
    # write CSV
    REPORTS.mkdir(exist_ok=True)
    cols = ["signal_id", "asset_class", "mode", "tier", "direction", "news_supported",
            "created_at", "entry_touch_at", "tracker_detected_at", "first_detect_status",
            "paper_entry_alert_at", "paper_entry_status", "entry_price_used",
            "detection_lag_sec", "alert_emit_lag_sec", "entry_age_sec",
            "already_closed_same_tick", "classification"]
    with open(REPORTS / "ENTRY_DETECTION_LATENCY.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in cols})
    print(f"[wrote] reports/ENTRY_DETECTION_LATENCY.csv ({len(rows)} entered signals)")

    for label, hours in [("24h", 24), ("7d", 168), ("14d", 336)]:
        cut = now_utc() - timedelta(hours=hours)
        win = [r for r in rows if r["_touch_dt"] and r["_touch_dt"] >= cut]
        print(f"\n===== ENTRY LATENCY — {label} (n={len(win)} entered) =====")
        # classification distribution
        cls = defaultdict(int)
        for r in win:
            cls[r["classification"]] += 1
        order = ["fresh", "acceptable", "late", "very_late", "already_closed", "unknown"]
        print("  classification:", {k: cls[k] for k in order if cls[k]})
        # entry_age stats (excl already_closed/unknown)
        ages = [r["entry_age_sec"] / 60.0 for r in win
                if isinstance(r["entry_age_sec"], (int, float))]
        if ages:
            ages_s = sorted(ages)
            print(f"  entry_age min (n={len(ages)}): median={statistics.median(ages):.1f}m "
                  f"mean={statistics.mean(ages):.1f}m p90={ages_s[int(len(ages_s)*0.9)]:.1f}m "
                  f"max={max(ages):.1f}m")
        # by asset/mode
        bm = defaultdict(lambda: defaultdict(int))
        for r in win:
            bm[(r["asset_class"], r["mode"])][r["classification"]] += 1
        print("  by asset/mode (fresh/acceptable/late/very_late/already_closed):")
        for k in sorted(bm, key=lambda x: (str(x[0]), str(x[1]))):
            c = bm[k]
            print(f"    {str(k[0]):7s} {str(k[1]):9s} "
                  f"{c['fresh']}/{c['acceptable']}/{c['late']}/{c['very_late']}/{c['already_closed']}")
    return rows


def _fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def expired_audit(db):
    """Classify expired/no-entry signals + MFE/MAE → CSV + summary tables."""
    # latest outcome per signal
    rows = []
    latest = {}
    for r in db.execute(
        "SELECT signal_id, checked_at, status, entry_triggered, final_outcome, "
        "max_favorable_excursion_r, max_adverse_excursion_r, "
        "ROW_NUMBER() OVER (PARTITION BY signal_id ORDER BY checked_at DESC) rn "
        "FROM signal_outcomes"):
        if r["rn"] == 1:
            latest[r["signal_id"]] = dict(r)
    sigs = {r["signal_id"]: dict(r) for r in db.execute(
        "SELECT signal_id, created_at, symbol, mode, asset_class, tier, direction, "
        "news_supported, validity_window_hours FROM proposed_signals")}

    EXPIRY_STATUSES = {"expired", "missed_no_entry"}
    out_rows = []
    for sid, o in latest.items():
        st = o.get("status")
        if st not in EXPIRY_STATUSES:
            continue
        s = sigs.get(sid, {})
        entered = bool(o.get("entry_triggered"))
        if st == "missed_no_entry":
            etype = "setup_expired_no_entry"   # never entered — protective by nature
        elif entered:
            etype = "entered_then_expired_flat"
        else:
            etype = "expired_no_entry"
        mfe = _fnum(o.get("max_favorable_excursion_r"))
        mae = _fnum(o.get("max_adverse_excursion_r"))
        out_rows.append({
            "signal_id": sid, "asset_class": s.get("asset_class"), "mode": s.get("mode"),
            "tier": s.get("tier"), "direction": s.get("direction"),
            "news_supported": s.get("news_supported"),
            "validity_h": s.get("validity_window_hours"),
            "created_at": s.get("created_at"), "checked_at": o.get("checked_at"),
            "status": st, "entered": int(entered), "expiry_type": etype,
            "mfe_r": round(mfe, 3) if mfe is not None else "",
            "mae_r": round(mae, 3) if mae is not None else "",
            "_created": parse(s.get("created_at")),
        })
    # CSV
    cols = ["signal_id", "asset_class", "mode", "tier", "direction", "news_supported",
            "validity_h", "created_at", "checked_at", "status", "entered",
            "expiry_type", "mfe_r", "mae_r"]
    with open(REPORTS / "EXPIRED_SIGNAL_DETAILS.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in out_rows:
            w.writerow({k: r.get(k, "") for k in cols})
    print(f"[wrote] reports/EXPIRED_SIGNAL_DETAILS.csv ({len(out_rows)} expired/no-entry signals)")

    # also total signals per window for % computation
    all_latest_status = [(sigs.get(sid, {}), o) for sid, o in latest.items()]

    for label, hours in [("24h", 24), ("7d", 168), ("14d", 336), ("all", 10**6)]:
        cut = now_utc() - timedelta(hours=hours)
        win = [r for r in out_rows if r["_created"] and r["_created"] >= cut]
        # total signals created in window (for expired %)
        total_win = sum(1 for s, _o in all_latest_status
                        if parse(s.get("created_at")) and parse(s.get("created_at")) >= cut)
        print(f"\n===== EXPIRED — {label} (expired/no-entry={len(win)} of {total_win} tracked = {pct(len(win), total_win)}) =====")
        by_type = defaultdict(int)
        for r in win:
            by_type[r["expiry_type"]] += 1
        print("  by type:", dict(by_type))
        # by asset/mode
        bm = defaultdict(lambda: [0, 0])  # [no_entry, entered_flat]
        for r in win:
            bm[(r["asset_class"], r["mode"])][1 if r["entered"] else 0] += 1
        print("  by asset/mode [no_entry / entered_then_flat]:")
        for k in sorted(bm, key=lambda x: (str(x[0]), str(x[1]))):
            print(f"    {str(k[0]):7s} {str(k[1]):9s} {bm[k][0]} / {bm[k][1]}")
        # entered_then_expired_flat: MFE/MAE + missed-opportunity analysis
        flat = [r for r in win if r["expiry_type"] == "entered_then_expired_flat"]
        mfes = [r["mfe_r"] for r in flat if isinstance(r["mfe_r"], (int, float))]
        maes = [r["mae_r"] for r in flat if isinstance(r["mae_r"], (int, float))]
        if flat:
            n = len(flat)
            r03 = sum(1 for m in mfes if m >= 0.3)
            r05 = sum(1 for m in mfes if m >= 0.5)
            r10 = sum(1 for m in mfes if m >= 1.0)
            protective = sum(1 for m in maes if m <= -1.0)  # would've stopped if held
            print(f"  entered-then-flat (n={n}): "
                  f"avgMFE={statistics.mean(mfes):.2f}R avgMAE={statistics.mean(maes):.2f}R "
                  f"reached+0.3R={pct(r03, n)} +0.5R={pct(r05, n)} +1R={pct(r10, n)} "
                  f"would-have-stopped(MAE<=-1R)={pct(protective, n)}")


if __name__ == "__main__":
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    cmd = sys.argv[1] if len(sys.argv) > 1 else "latency"
    if cmd == "latency":
        latency_audit(db)
    elif cmd == "expired":
        expired_audit(db)
    elif cmd == "all":
        latency_audit(db)
        expired_audit(db)
