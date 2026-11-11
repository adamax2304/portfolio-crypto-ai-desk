"""Quick read-only audit of today's signal + alert counts."""
import sqlite3
from src.config import load_config

today = "2026-05-27"
con = sqlite3.connect(load_config().db_path)
con.row_factory = sqlite3.Row


def n(sql, *params):
    return con.execute(sql, params).fetchone()["n"]


print("=== crypto today ===")
print("  A/B registered:", n(
    "SELECT COUNT(*) AS n FROM proposed_signals "
    "WHERE asset_class='crypto' AND tier IN ('A','B') AND created_at LIKE ?",
    today + "%"))
print("  C registered:", n(
    "SELECT COUNT(*) AS n FROM proposed_signals "
    "WHERE asset_class='crypto' AND tier='C' AND created_at LIKE ?",
    today + "%"))
print("  signal_alerts (new ledger):", n(
    "SELECT COUNT(*) AS n FROM signal_alerts "
    "WHERE asset_class='crypto' AND sent_at LIKE ?", today + "%"))
print("  watchlist_alerts (legacy):", n(
    "SELECT COUNT(*) AS n FROM watchlist_alerts "
    "WHERE asset_class='crypto' AND sent_at LIKE ?", today + "%"))

print()
print("=== stocks today ===")
print("  A/B registered:", n(
    "SELECT COUNT(*) AS n FROM proposed_signals "
    "WHERE asset_class='stocks' AND tier IN ('A','B') AND created_at LIKE ?",
    today + "%"))
print("  C registered:", n(
    "SELECT COUNT(*) AS n FROM proposed_signals "
    "WHERE asset_class='stocks' AND tier='C' AND created_at LIKE ?",
    today + "%"))
print("  signal_alerts (new ledger):", n(
    "SELECT COUNT(*) AS n FROM signal_alerts "
    "WHERE asset_class='stocks' AND sent_at LIKE ?", today + "%"))
print("  signal_alerts SENT:", n(
    "SELECT COUNT(*) AS n FROM signal_alerts "
    "WHERE asset_class='stocks' AND telegram_status='sent' AND sent_at LIKE ?",
    today + "%"))

# Latest crypto A/B in registry (any date) - so we know what we're missing
print()
print("=== latest crypto A/B in registry (any date, top 5) ===")
for row in con.execute(
    "SELECT symbol, tier, mode, direction, score, status, created_at "
    "FROM proposed_signals WHERE asset_class='crypto' AND tier IN ('A','B') "
    "ORDER BY created_at DESC LIMIT 5"
).fetchall():
    print(f"  {row['symbol']:14} {row['tier']} {row['mode']:8} {row['direction']:5} "
          f"score={row['score']} status={row['status']} created={row['created_at']}")
