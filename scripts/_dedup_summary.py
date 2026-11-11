"""Render dedup dump as a compact summary."""
import json

with open("scripts/_dedup_dump_today.json", encoding="utf-8-sig") as f:
    data = json.load(f)

print(f"{'bucket':<25} {'raw_n':>6} {'dedup_n':>8} {'PF':>8} {'totalR':>8} {'winrate':>8}")
print("-" * 75)
for k in ("crypto_AB", "crypto_scalp_AB", "crypto_intraday_AB",
          "stocks_AB", "stocks_A_only", "stocks_B_only", "stocks_C_only"):
    b = data.get(k, {})
    raw_n = b.get("raw_count", 0)
    ded_n = b.get("dedup_count", 0)
    ded = b.get("dedup_stats", {})
    pf = ded.get("profit_factor")
    tr = ded.get("total_r")
    wr = ded.get("winrate")
    pf_s = f"{pf:.2f}" if isinstance(pf, (int, float)) else str(pf)
    tr_s = f"{tr:+.1f}" if isinstance(tr, (int, float)) else str(tr)
    wr_s = f"{wr * 100:.0f}%" if isinstance(wr, (int, float)) else "n/a"
    print(f"{k:<25} {raw_n:>6} {ded_n:>8} {pf_s:>8} {tr_s:>8} {wr_s:>8}")
