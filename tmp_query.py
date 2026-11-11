import sqlite3

conn = sqlite3.connect('db/crypto_ai_desk.sqlite')

rows = conn.execute("""
    SELECT symbol, tier, mode, direction, score, status, expires_at, invalidation
    FROM proposed_signals
    WHERE asset_class='crypto' AND status NOT IN ('closed_win','closed_loss','closed_flat','expired')
    ORDER BY score DESC
    LIMIT 15
""").fetchall()
print(f'ACTIVE CRYPTO SIGNALS ({len(rows)}):')
for r in rows:
    print(f"  {r[0]} | tier={r[1]} | {r[2]} | {r[3]} | score={r[4]:.0f} | status={r[5]} | expires={r[6]} | inv={r[7]}")

rows2 = conn.execute("""
    SELECT symbol, tier, mode, direction, score, status, expires_at, invalidation
    FROM proposed_signals
    WHERE asset_class='stocks' AND tier IN ('A','B') AND status NOT IN ('closed_win','closed_loss','closed_flat','expired')
    ORDER BY score DESC
    LIMIT 10
""").fetchall()
print(f'\nACTIVE STOCKS A/B SIGNALS ({len(rows2)}):')
for r in rows2:
    print(f"  {r[0]} | tier={r[1]} | {r[2]} | {r[3]} | score={r[4]:.0f} | status={r[5]} | expires={r[6]} | inv={r[7]}")
