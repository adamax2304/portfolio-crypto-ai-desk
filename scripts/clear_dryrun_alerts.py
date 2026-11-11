"""One-off: clear dry_run signal_alerts rows for the 8 current stocks A/B setups.

Strictly scoped:
- only ``asset_class = 'stocks'``
- only ``telegram_status = 'dry_run'``
- only the 8 ``signal_id`` values whitelisted below.

Prints a pre-check (what would be deleted) and a post-check (what
remains) so the operation is auditable. Does not touch
``proposed_signals``, crypto rows, or any ``telegram_status = 'sent'``
rows.
"""

from __future__ import annotations

from src.config import load_config
from src.storage.sqlite import SQLiteStore

TARGET_SIGNAL_IDS = (
    "sig_2771164d54b72b46",  # AAPL A
    "sig_f8684dbcc7a924d8",  # LLY A
    "sig_3f6d9a236a624d1e",  # AMD B
    "sig_326863601afbbb85",  # XLK B
    "sig_2b2220282e946a08",  # SMCI B
    "sig_8d97349402e11fbf",  # SMH B
    "sig_c6786172e71ab969",  # UNH B
    "sig_6b79cc342604cef3",  # TSLA B
)


def main() -> None:
    config = load_config()
    db = SQLiteStore(config.db_path)
    db.init_db()
    qmarks = ",".join("?" for _ in TARGET_SIGNAL_IDS)

    with db.connect() as conn:
        pre = conn.execute(
            f"""
            SELECT alert_id, signal_id, symbol, tier, telegram_status, sent_at
            FROM signal_alerts
            WHERE asset_class = 'stocks'
              AND telegram_status = 'dry_run'
              AND signal_id IN ({qmarks})
            ORDER BY symbol
            """,
            TARGET_SIGNAL_IDS,
        ).fetchall()

    print("=== PRE-DELETE — rows matching the whitelist ===")
    for row in pre:
        print(
            f"  {row['symbol']:6} {row['tier']} | "
            f"alert_id={row['alert_id']} | "
            f"signal_id={row['signal_id']} | "
            f"status={row['telegram_status']} | "
            f"sent_at={row['sent_at']}"
        )
    print(f"--- would delete: {len(pre)} row(s) ---")

    # Safety reverification — only delete rows that are dry_run AND in the
    # whitelist AND asset_class = stocks. Triple guard in the SQL.
    with db.connect() as conn:
        cursor = conn.execute(
            f"""
            DELETE FROM signal_alerts
            WHERE asset_class = 'stocks'
              AND telegram_status = 'dry_run'
              AND signal_id IN ({qmarks})
            """,
            TARGET_SIGNAL_IDS,
        )
        deleted_count = cursor.rowcount
    print(f"\n=== DELETE complete — rows deleted: {deleted_count} ===")

    # Post-check.
    with db.connect() as conn:
        remaining = conn.execute(
            f"""
            SELECT COUNT(*) AS n FROM signal_alerts
            WHERE asset_class = 'stocks'
              AND signal_id IN ({qmarks})
            """,
            TARGET_SIGNAL_IDS,
        ).fetchone()
        crypto_count = conn.execute(
            "SELECT COUNT(*) AS n FROM signal_alerts WHERE asset_class = 'crypto'"
        ).fetchone()
        sent_count = conn.execute(
            "SELECT COUNT(*) AS n FROM signal_alerts "
            "WHERE asset_class = 'stocks' AND telegram_status = 'sent'"
        ).fetchone()
        ps_count = conn.execute(
            "SELECT COUNT(*) AS n FROM proposed_signals WHERE asset_class = 'stocks'"
        ).fetchone()

    print("\n=== POST-DELETE invariants ===")
    print(f"  signal_alerts rows remaining for the 8 target ids: {remaining['n']} (expected 0)")
    print(f"  crypto signal_alerts rows untouched count:           {crypto_count['n']}")
    print(f"  stocks signal_alerts rows with telegram_status='sent': {sent_count['n']}")
    print(f"  proposed_signals (stocks) row count:                 {ps_count['n']}")


if __name__ == "__main__":
    main()
