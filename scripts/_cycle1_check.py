"""Read-only: inspect signals registered during 12h-monitor cycle 1.

Cycle 1 window: 2026-05-29 13:10–14:04 EEST = 10:10–11:04 UTC.
"""
import sqlite3
from src.config import load_config

# created_at stored in UTC ISO. Cycle-1 window in UTC:
LO = "2026-05-29T10:10"
HI = "2026-05-29T11:05"

con = sqlite3.connect(load_config().db_path)
con.row_factory = sqlite3.Row


def rows(sql, *p):
    return con.execute(sql, p).fetchall()


print("=== Cycle-1 proposed_signals (created 10:10–11:05 UTC) ===")
for ac in ("crypto", "stocks"):
    for tier in ("A", "B", "C"):
        n = con.execute(
            "SELECT COUNT(*) AS n FROM proposed_signals "
            "WHERE asset_class=? AND tier=? AND created_at>=? AND created_at<?",
            (ac, tier, LO, HI)).fetchone()["n"]
        print(f"  {ac:6} tier {tier}: {n}")

print()
print("=== Cycle-1 A/B detail ===")
for r in rows(
    "SELECT signal_id, asset_class, symbol, mode, direction, tier, score, "
    "entry_low, entry_high, invalidation, tp1, tp2, tp3, status, created_at, "
    "source_report_path FROM proposed_signals "
    "WHERE tier IN ('A','B') AND created_at>=? AND created_at<? "
    "ORDER BY asset_class, tier, score DESC", LO, HI):
    src = (r["source_report_path"] or "")
    src = src.split("\\")[-1] if src else "(none)"
    print(f"  {r['asset_class']:6} {r['symbol']:12} {r['tier']} {r['mode']:8} "
          f"{r['direction']:5} score={r['score']} "
          f"entry={r['entry_low']}-{r['entry_high']} inv={r['invalidation']} "
          f"tp1={r['tp1']} status={r['status']}")
    print(f"         id={r['signal_id']} created={r['created_at']} src={src}")

print()
print("=== Cycle-1 C-tier: actionable check (entry+invalidation present?) ===")
c_rows = rows(
    "SELECT symbol, asset_class, entry_low, invalidation FROM proposed_signals "
    "WHERE tier='C' AND created_at>=? AND created_at<?", LO, HI)
with_entry = sum(1 for r in c_rows if r["entry_low"] is not None and r["invalidation"] is not None)
print(f"  C-tier registered: {len(c_rows)} | with entry+invalidation: {with_entry}")

print()
print("=== Telegram alerts during cycle 1 (signal_alerts, sent 10:10–11:05 UTC) ===")
for r in rows(
    "SELECT symbol, asset_class, mode, tier, signal_id, telegram_status, alert_type, sent_at "
    "FROM signal_alerts WHERE sent_at>=? AND sent_at<? ORDER BY sent_at", LO, HI):
    print(f"  {r['asset_class']:6} {r['symbol']:12} {r['tier']} {r['mode']:8} "
          f"type={r['alert_type']:16} status={r['telegram_status']:6} "
          f"sig={r['signal_id'][:18]}")
# crypto legacy
print()
print("=== Crypto legacy watchlist_alerts during cycle 1 ===")
for r in rows(
    "SELECT symbol, new_tier, score, direction, mode, sent_at FROM watchlist_alerts "
    "WHERE asset_class='crypto' AND sent_at>=? AND sent_at<? ORDER BY sent_at", LO, HI):
    print(f"  {r['symbol']:12} tier={r['new_tier']} score={r['score']} "
          f"{r['direction']} {r['mode']} sent={r['sent_at']}")

# Alert integrity: any signal_alerts row without a matching proposed_signal?
print()
print("=== Alert integrity check ===")
orphans = con.execute(
    "SELECT COUNT(*) AS n FROM signal_alerts a "
    "WHERE a.sent_at>=? AND a.sent_at<? "
    "AND NOT EXISTS (SELECT 1 FROM proposed_signals p WHERE p.signal_id=a.signal_id)",
    (LO, HI)).fetchone()["n"]
ctier_alerts = con.execute(
    "SELECT COUNT(*) AS n FROM signal_alerts WHERE tier='C' AND sent_at>=? AND sent_at<?",
    (LO, HI)).fetchone()["n"]
print(f"  alerts without matching proposed_signal: {orphans} (expect 0)")
print(f"  C-tier alerts sent: {ctier_alerts} (expect 0)")
