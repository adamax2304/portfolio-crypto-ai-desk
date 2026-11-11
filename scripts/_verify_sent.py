from src.config import load_config
from src.storage.sqlite import SQLiteStore

db = SQLiteStore(load_config().db_path)
db.init_db()
with db.connect() as conn:
    rows = conn.execute(
        "SELECT symbol, tier, telegram_status, sent_at, signal_id "
        "FROM signal_alerts WHERE asset_class = 'stocks' "
        "ORDER BY sent_at DESC LIMIT 12"
    ).fetchall()
for r in rows:
    print(
        f"  {r['symbol']:6} {r['tier']} | telegram_status={r['telegram_status']:>6} | "
        f"signal_id={r['signal_id']} | sent_at={r['sent_at']}"
    )
