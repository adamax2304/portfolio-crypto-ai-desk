"""Read-only data gathering for the Profitability Levers Audit (PARTS 2-5).

Emits JSON summaries the markdown reports consume. No DB writes, no Telegram,
no auto-trade, no scoring changes.
"""
from __future__ import annotations

import csv
import json
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
DB = REPO / "db" / "crypto_ai_desk.sqlite"
OUT = REPO / "reports" / "_levers_audit_data.json"


def main() -> int:
    db = sqlite3.connect(DB, timeout=60)
    db.row_factory = sqlite3.Row

    # ── PART 2: scalp exit simulation on triggered signals ─────────────
    triggered = db.execute(
        """
        SELECT ps.signal_id, ps.symbol, ps.direction, ps.created_at,
               so.final_outcome, so.final_r,
               so.max_favorable_excursion_r as mfe,
               so.max_adverse_excursion_r as mae,
               so.notes
        FROM proposed_signals ps
        LEFT JOIN signal_outcomes so
          ON so.signal_id = ps.signal_id
         AND so.id = (SELECT MAX(id) FROM signal_outcomes WHERE signal_id=ps.signal_id)
        WHERE ps.asset_class='crypto' AND ps.mode='scalp' AND ps.tier IN ('A','B')
          AND ps.created_at >= '2026-05-15' AND so.entry_triggered = 1
        """
    ).fetchall()
    triggered = [dict(r) for r in triggered]

    def simulate(policy: str):
        netR = 0.0
        W = L = 0
        reduced_losses = 0
        lost_wins = 0
        for r in triggered:
            mfe = r.get("mfe") or 0
            mae = r.get("mae") or 0
            original = r.get("final_r") or 0
            fo = r.get("final_outcome") or ""
            sim_r = original

            if policy == "baseline":
                if fo == "win":
                    W += 1
                elif fo == "loss":
                    L += 1
            elif policy == "tp1_at_0.5R":
                if fo == "expired":
                    sim_r = 0.5 if (mfe >= 0.5 and mae > -0.5) else 0
                    if sim_r > 0:
                        W += 1
                elif fo == "win":
                    sim_r = 0.5
                    W += 1
                    lost_wins += 1
                elif fo == "loss":
                    sim_r = -1
                    L += 1
            elif policy == "partial_at_0.5R":
                # 50% off at +0.5R, leave 50% on original TP/SL
                if fo == "expired":
                    if mfe >= 0.5:
                        sim_r = 0.25
                        W += 1
                    else:
                        sim_r = 0
                elif fo == "win":
                    sim_r = 0.25 + 0.5 * original
                    W += 1
                elif fo == "loss":
                    if mfe >= 0.5:
                        sim_r = 0.25 - 0.5
                        reduced_losses += 1
                        L += 1
                    else:
                        sim_r = -1
                        L += 1
            elif policy == "be_after_0.6R":
                if fo == "expired":
                    sim_r = 0
                elif fo == "win":
                    sim_r = original
                    W += 1
                elif fo == "loss":
                    if mfe >= 0.6 and mae > -0.6:
                        sim_r = 0
                        reduced_losses += 1
                    else:
                        sim_r = -1
                        L += 1
            elif policy == "trail_after_0.7R":
                if fo == "expired":
                    if mfe >= 0.7:
                        sim_r = 0.35
                        W += 1
                    else:
                        sim_r = 0
                elif fo == "win":
                    sim_r = original
                    W += 1
                elif fo == "loss":
                    if mfe >= 0.7 and mae > -0.7:
                        sim_r = 0.35
                        reduced_losses += 1
                        W += 1
                    else:
                        sim_r = -1
                        L += 1
            elif policy == "expiry_4h":
                # Approximation: expired-with-MFE>=0.5 might convert to small win
                if fo == "expired":
                    sim_r = 0.25 if mfe >= 0.5 else 0
                    if sim_r > 0:
                        W += 1
                elif fo == "win":
                    sim_r = original
                    W += 1
                elif fo == "loss":
                    sim_r = -1
                    L += 1
            netR += sim_r
        closed = W + L
        return {
            "policy": policy,
            "n_triggered": len(triggered),
            "W": W, "L": L, "closed": closed,
            "netR": round(netR, 2),
            "avgR": round(netR / max(len(triggered), 1), 3),
            "WR_closed": round(W / max(closed, 1) * 100, 0),
            "reduced_losses": reduced_losses,
            "lost_wins": lost_wins,
        }

    policies = [
        "baseline", "tp1_at_0.5R", "partial_at_0.5R",
        "be_after_0.6R", "trail_after_0.7R", "expiry_4h",
    ]
    sim_results = [simulate(p) for p in policies]

    # Intrabar exclusion subset
    clean = [r for r in triggered
             if not (r.get("notes") and ("intrabar_entry_stop" in r["notes"]
                                          or "intrabar_entry_tp" in r["notes"]))]
    intrabar = len(triggered) - len(clean)
    clean_win = sum(1 for r in clean if r.get("final_outcome") == "win")
    clean_loss = sum(1 for r in clean if r.get("final_outcome") == "loss")
    clean_netR = sum((r.get("final_r") or 0) for r in clean
                     if r.get("final_outcome") in ("win", "loss"))

    # ── PART 3: expansion watchlist quality ─────────────────────────────
    exp_path = REPO / "data" / "processed" / "agent_outputs" / "crypto_expansion_watchlist.json"
    expansion = {}
    if exp_path.exists():
        with exp_path.open(encoding="utf-8") as f:
            expansion = json.load(f)

    # Did any expansion symbol later become A/B?
    exp_syms = [c.get("symbol") for c in (expansion.get("candidates") or [])]
    promoted = []
    for sym in exp_syms:
        row = db.execute(
            """
            SELECT signal_id, tier, created_at FROM proposed_signals
            WHERE symbol = ? AND tier IN ('A','B') AND asset_class='crypto'
              AND created_at >= datetime('now','-2 days')
            ORDER BY created_at DESC LIMIT 1
            """,
            (sym,),
        ).fetchone()
        if row:
            promoted.append({"symbol": sym, "tier": row["tier"], "created_at": row["created_at"]})

    # ── PART 4: news_items missing symbol mapping ───────────────────────
    unmapped_samples = db.execute(
        """
        SELECT title, source, published_at FROM news_items
        WHERE asset_class='crypto'
          AND published_at >= datetime('now','-3 days')
          AND (detected_symbols_json IS NULL OR detected_symbols_json='[]'
               OR detected_symbols_json='')
        ORDER BY published_at DESC LIMIT 80
        """
    ).fetchall()
    unmapped = [{"title": r["title"], "source": r["source"], "published_at": r["published_at"]}
                for r in unmapped_samples]

    # Heuristic: pull capitalised tokens from titles to suggest candidate aliases.
    import re
    TICKER_PAT = re.compile(r"\b([A-Z]{3,8})\b")
    SAFE_BLACKLIST = {"USD", "USDT", "USDC", "ETF", "SEC", "CEO", "CTO", "CFO",
                      "IPO", "NFT", "API", "AI", "BTC", "ETH", "LLC", "INC",
                      "USA", "UK", "EU", "DAO", "DEX", "CEX", "DeFi", "TVL",
                      "WSJ", "FED", "CFTC", "AML", "KYC", "WAGMI", "ICO",
                      "POS", "POW", "RPC", "ATH", "ATL", "FOMO"}
    candidate_counts: dict[str, int] = defaultdict(int)
    candidate_titles: dict[str, list[str]] = defaultdict(list)
    for n in unmapped:
        for tok in TICKER_PAT.findall(n["title"] or ""):
            if tok in SAFE_BLACKLIST:
                continue
            candidate_counts[tok] += 1
            if len(candidate_titles[tok]) < 3:
                candidate_titles[tok].append((n["title"] or "")[:120])
    alias_candidates = sorted(candidate_counts.items(), key=lambda x: -x[1])[:30]

    # ── PART 5: sizing simulation on existing per-setup R outcomes ──────
    # Use the same deduped CTE so we don't double-count duplicate signal_ids.
    CTE = """
    WITH latest_outcome AS (
      SELECT signal_id, MAX(checked_at) AS max_checked
      FROM signal_outcomes
      WHERE final_outcome IS NOT NULL AND final_outcome != ''
      GROUP BY signal_id
    ), per_setup AS (
      SELECT ps.asset_class, ps.mode, ps.tier, ps.direction, ps.news_supported,
             substr(ps.created_at,1,10) AS day, ps.symbol,
             AVG(so.final_r) AS final_r
      FROM proposed_signals ps
      JOIN latest_outcome lo ON lo.signal_id = ps.signal_id
      JOIN signal_outcomes so ON so.signal_id = ps.signal_id AND so.checked_at = lo.max_checked
      GROUP BY ps.asset_class, ps.mode, ps.tier, ps.direction, ps.symbol, day
    )
    """
    setups = db.execute(CTE + " SELECT * FROM per_setup").fetchall()
    setups = [dict(r) for r in setups]

    def playbook_for(r):
        ac = r.get("asset_class") or "crypto"
        mode = r.get("mode") or ""
        direction = r.get("direction") or ""
        news = r.get("news_supported") or 0
        if ac == "stocks":
            if mode == "intraday":
                return "stocks_intraday_rth_momentum"
            if mode == "swing":
                return "stocks_swing_watchlist_rs_rotation"
            return "stocks_invest_watchlist_30d_thesis"
        if mode == "scalp":
            return "crypto_scalp_momentum_continuation"
        if direction == "short":
            return "crypto_failed_bounce_short"
        if mode == "swing":
            return "crypto_swing_narrative_rs_momentum"
        return "crypto_intraday_catalyst_or_momentum"

    # Tier overlay (A-tier stocks long is the special weak cohort)
    def size_for(r, scheme):
        pb = playbook_for(r)
        tier = (r.get("tier") or "").upper()
        ac = r.get("asset_class") or ""
        mode = r.get("mode") or ""
        direction = r.get("direction") or ""

        if scheme == "equal_1R":
            return 1.0 if tier in ("A", "B") else 0.0
        if scheme == "playbook_aware":
            if tier == "C":
                return 0.0  # watchlist disabled
            if ac == "stocks" and mode in ("swing", "invest"):
                return 0.0  # paused
            if pb == "crypto_scalp_momentum_continuation":
                return 0.5  # low-confidence
            if ac == "stocks" and mode == "intraday" and tier == "A" and direction == "long":
                return 0.5  # A-tier long overpromotion
            if pb in ("crypto_swing_narrative_rs_momentum", "crypto_intraday_catalyst_or_momentum"):
                return 1.0
            return 1.0
        if scheme == "aggressive":
            if tier == "C" or (ac == "stocks" and mode in ("swing", "invest")):
                return 0.0
            if pb == "crypto_scalp_momentum_continuation":
                return 0.5
            if pb in ("crypto_swing_narrative_rs_momentum",
                      "stocks_intraday_rth_momentum"):
                return 1.5  # lean into best playbooks
            return 1.0
        return 1.0

    def sim_size(scheme):
        total = 0.0
        rs = []
        for r in setups:
            size = size_for(r, scheme)
            if size <= 0:
                continue
            r_pnl = size * (r.get("final_r") or 0)
            total += r_pnl
            rs.append(r_pnl)
        rs.sort()
        # Simple drawdown proxy: max negative cumulative streak (signed)
        cum = 0.0
        peak = 0.0
        max_dd = 0.0
        for x in rs:
            cum += x
            peak = max(peak, cum)
            max_dd = min(max_dd, cum - peak)
        # Std dev proxy of per-trade pnl
        if rs:
            mean = sum(rs) / len(rs)
            var = sum((x - mean) ** 2 for x in rs) / len(rs)
            sd = var ** 0.5
        else:
            sd = 0.0
        wins = sum(1 for x in rs if x > 0)
        losses = sum(1 for x in rs if x < 0)
        return {
            "scheme": scheme, "n_sized": len(rs),
            "totalR": round(total, 1),
            "max_dd_R": round(max_dd, 1),
            "vol_per_trade": round(sd, 2),
            "wins": wins, "losses": losses,
            "WR_closed": round(wins / max(wins + losses, 1) * 100, 0),
            "PF": round(
                (sum(x for x in rs if x > 0) /
                 abs(sum(x for x in rs if x < 0) or 1e-9)),
                2,
            ),
        }

    sizing_schemes = ["equal_1R", "playbook_aware", "aggressive"]
    sizing_results = [sim_size(s) for s in sizing_schemes]

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scalp_simulation": {
            "n_triggered": len(triggered),
            "policies": sim_results,
            "intrabar_excluded": {
                "n_clean": len(clean),
                "n_intrabar": intrabar,
                "W": clean_win, "L": clean_loss,
                "WR_closed_clean": round(clean_win / max(clean_win + clean_loss, 1) * 100, 0),
                "netR_clean": round(clean_netR, 2),
            },
        },
        "expansion_quality": {
            "expansion_n": len(expansion.get("candidates") or []),
            "skipped_scalp": expansion.get("skipped_scalp"),
            "skipped_in_top_setups": expansion.get("skipped_in_top_setups"),
            "promoted_to_ab_within_48h": promoted,
        },
        "alias_candidates": [
            {"token": tok, "count": cnt,
             "sample_titles": candidate_titles.get(tok, [])}
            for tok, cnt in alias_candidates
        ],
        "unmapped_news_count": len(unmapped),
        "sizing_simulation": sizing_results,
    }
    OUT.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"wrote {OUT.name}")

    # Print summary
    print()
    print("=== Scalp exit policies ===")
    for s in sim_results:
        print(f"  {s['policy']:<22} n={s['n_triggered']} W={s['W']} L={s['L']} "
              f"netR={s['netR']:+.1f} avgR={s['avgR']:+.2f} "
              f"redL={s['reduced_losses']} lostW={s['lost_wins']}")
    print()
    print("=== Sizing schemes ===")
    for s in sizing_results:
        print(f"  {s['scheme']:<18} n_sized={s['n_sized']} totalR={s['totalR']:+.1f} "
              f"WR={s['WR_closed']}% PF={s['PF']} maxDD={s['max_dd_R']} vol={s['vol_per_trade']}")
    print()
    print(f"Expansion: candidates={len(expansion.get('candidates') or [])}, "
          f"promoted_to_AB_within_48h={len(promoted)}")
    print(f"Unmapped news: {len(unmapped)}, top alias candidates: "
          f"{[t for t, _ in alias_candidates[:8]]}")
    db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
