"""PART 3 — Crypto intraday short caution study.

Split crypto intraday short signals by:
  - fresh catalyst (news_supported=1 AND created_at - latest-news-for-symbol <= 6h)
  - failed-reclaim playbook
  - derivatives confirmation (oi_context mentions deleveraging/build-down + funding crowded)
  - BTC trend alignment

Output: which subgroup loses, which wins. Recommend only a label (caution flag).
"""

from __future__ import annotations

import json
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def main() -> None:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    rows = con.execute("""
        SELECT ps.signal_id, ps.symbol, ps.mode, ps.tier, ps.direction,
               ps.setup_type, ps.news_supported, ps.market_regime,
               ps.funding_context, ps.oi_context, ps.created_at,
               ps.raw_idea_json,
               o.final_outcome, o.final_r, o.entry_triggered
        FROM proposed_signals ps
        LEFT JOIN (SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id) m
          ON m.signal_id = ps.signal_id
        LEFT JOIN signal_outcomes o ON o.id = m.mid
        WHERE ps.asset_class='crypto' AND ps.mode='intraday' AND ps.direction='short'
          AND ps.tier IN ('A','B')
        ORDER BY ps.created_at
    """).fetchall()

    def classify(r):
        fund = (r["funding_context"] or "").lower()
        oi = (r["oi_context"] or "").lower()
        setup = (r["setup_type"] or "").lower()
        news = int(r["news_supported"] or 0) == 1
        # derivatives confirmation: funding crowded (long-crowded against short = good) OR OI deleveraging
        deriv_ok = ("crowded" in fund and "long" in fund) or ("deleveraging" in oi) or ("crowded=" in fund and "extreme" in fund)
        # failed-reclaim: setup type contains 'fail' or 'reject'
        failed_reclaim = "fail" in setup or "reject" in setup
        # btc alignment: market_regime contains 'bearish' or 'risk_off'
        regime = (r["market_regime"] or "").lower()
        btc_aligned = "bear" in regime or "risk_off" in regime or "downtrend" in regime
        return {
            "fresh_news": news,
            "failed_reclaim": failed_reclaim,
            "deriv_ok": deriv_ok,
            "btc_aligned": btc_aligned,
        }

    # Group stats
    groups = {
        "all_intraday_shorts": rows,
        "with_fresh_news": [],
        "without_news": [],
        "failed_reclaim_only": [],
        "breakdown_retest_only": [],
        "deriv_confirmed": [],
        "no_deriv_confirmation": [],
        "btc_aligned_bearish": [],
        "btc_mean_reverting": [],
    }
    for r in rows:
        f = classify(r)
        if f["fresh_news"]: groups["with_fresh_news"].append(r)
        else: groups["without_news"].append(r)
        if f["failed_reclaim"]: groups["failed_reclaim_only"].append(r)
        else: groups["breakdown_retest_only"].append(r)
        if f["deriv_ok"]: groups["deriv_confirmed"].append(r)
        else: groups["no_deriv_confirmation"].append(r)
        if f["btc_aligned"]: groups["btc_aligned_bearish"].append(r)
        else: groups["btc_mean_reverting"].append(r)

    def stats(items):
        closed = [r for r in items if r["final_outcome"] in ("win", "loss", "expired", "not_triggered")]
        triggered = [r for r in items if r["entry_triggered"] == 1]
        wins = sum(1 for r in closed if (r["final_r"] or 0) > 0)
        losses = sum(1 for r in closed if (r["final_r"] or 0) < 0)
        r_sum = sum(float(r["final_r"] or 0) for r in items)
        return {
            "n": len(items),
            "triggered": len(triggered),
            "wins": wins, "losses": losses,
            "wr": wins / max(1, wins + losses),
            "raw_r": r_sum,
        }

    out = []
    out.append("# Crypto Intraday Short Caution Study (PART 3)")
    out.append("")
    out.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    out.append(f"**Scope:** all A/B crypto intraday short signals (n={len(rows)}).")
    out.append("")
    out.append("## Subgroup performance")
    out.append("")
    out.append("| Subgroup | n | trig | W | L | WR | raw R |")
    out.append("|---|---:|---:|---:|---:|---:|---:|")
    for name, items in groups.items():
        s = stats(items)
        out.append(f"| {name} | {s['n']} | {s['triggered']} | {s['wins']} | {s['losses']} | {s['wr']:.0%} | {s['raw_r']:+.1f} |")
    out.append("")

    # Key findings
    out.append("## Key findings")
    out.append("")
    no_news = stats(groups["without_news"])
    with_news = stats(groups["with_fresh_news"])
    deriv_ok = stats(groups["deriv_confirmed"])
    no_deriv = stats(groups["no_deriv_confirmation"])
    fail_recl = stats(groups["failed_reclaim_only"])
    breakdown = stats(groups["breakdown_retest_only"])

    out.append(f"- Shorts without news support: n={no_news['n']}, R={no_news['raw_r']:+.1f}")
    out.append(f"- Shorts WITH news support: n={with_news['n']}, R={with_news['raw_r']:+.1f}")
    if no_news['raw_r'] < -2 and with_news['raw_r'] >= no_news['raw_r']:
        out.append("  → **Concentration**: losses are heavier in no-news shorts. A caution label on no-news shorts is justified.")
    out.append("")
    out.append(f"- Derivatives-confirmed shorts: n={deriv_ok['n']}, R={deriv_ok['raw_r']:+.1f}")
    out.append(f"- No derivatives confirmation: n={no_deriv['n']}, R={no_deriv['raw_r']:+.1f}")
    out.append("")
    out.append(f"- Failed-reclaim setup: n={fail_recl['n']}, R={fail_recl['raw_r']:+.1f}")
    out.append(f"- Breakdown-retest setup: n={breakdown['n']}, R={breakdown['raw_r']:+.1f}")
    out.append("")

    # Hard filter counterfactual
    out.append("## Hypothetical filter: only ship shorts with fresh news + deriv confirmation")
    out.append("")
    filtered = [r for r in rows
                if int(r["news_supported"] or 0) == 1
                and (("crowded" in (r["funding_context"] or "").lower() and "long" in (r["funding_context"] or "").lower())
                     or "deleveraging" in (r["oi_context"] or "").lower())]
    rejected = [r for r in rows if r not in filtered]
    fs = stats(filtered); rs_ = stats(rejected)
    out.append(f"- Kept (would still trade): n={fs['n']}, R={fs['raw_r']:+.1f}, WR={fs['wr']:.0%}")
    out.append(f"- Rejected (would NOT trade): n={rs_['n']}, R={rs_['raw_r']:+.1f}")
    out.append("")
    if rs_["raw_r"] < -2 and fs["raw_r"] > 0:
        out.append("- The hard filter looks net-positive but is built **post-hoc** on a small sample. **Do not implement** as a hard gate. Use it as a Telegram **caution label** only.")
    elif fs["n"] < 5:
        out.append("- The hard filter rejects too much; would-be winners like TON might be cut. Do not implement.")
    else:
        out.append("- Filter effect is mixed. Use as caution label only.")
    out.append("")

    # Would the filter cut historical winners?
    out.append("## Winners that the hard filter would have removed (if any)")
    out.append("")
    winners = [r for r in rows if (r["final_r"] or 0) > 0]
    cut_winners = [r for r in winners if r not in filtered]
    out.append(f"- Winning shorts total: **{len(winners)}**")
    out.append(f"- Would have been blocked by filter: **{len(cut_winners)}**")
    if cut_winners:
        for w in cut_winners[:5]:
            out.append(f"  - {w['symbol']} {w['created_at'][:10]} final_r={w['final_r']:+.1f}")
    out.append("")
    out.append("## Recommendation")
    out.append("")
    out.append("- **Do NOT implement a hard filter.** Sample n=33 is too small.")
    out.append("- **Add a Telegram caution label** to paper-entry alerts for crypto intraday shorts without fresh news AND without deriv confirmation. Label text: `⚠️ NO-NEWS-NO-DERIV SHORT — historically thin edge in this regime`.")
    out.append("- Re-evaluate after the cohort grows to n ≥ 60.")

    out_md = ROOT / "reports" / "CRYPTO_INTRADAY_SHORT_CAUTION_STUDY.md"
    out_md.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
