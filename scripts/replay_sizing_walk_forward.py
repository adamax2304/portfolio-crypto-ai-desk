"""PART 5 — Playbook-aware sizing walk-forward backtest.

Tests 4 sizing configs on a temporal split of the signal history.
Weights are chosen using TRAIN only; performance reported on VALIDATION
and FORWARD windows. Out-of-sample only — no peeking.

CAVEAT: We have only ~20 days of signal history. Statistical power is
LOW. This backtest is a sanity check, not a conclusive validation.
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.signals.playbooks import label_for  # noqa: E402

DB = ROOT / "db" / "crypto_ai_desk.sqlite"


def _load_closed_signals() -> list[dict]:
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        SELECT ps.*, o.final_r AS final_r, o.final_outcome AS final_outcome
        FROM proposed_signals ps
        JOIN (
            SELECT signal_id, MAX(id) AS mid FROM signal_outcomes GROUP BY signal_id
        ) m ON m.signal_id = ps.signal_id
        JOIN signal_outcomes o ON o.id = m.mid
        WHERE o.final_outcome IN ('win', 'loss', 'expired', 'not_triggered')
          AND o.final_r IS NOT NULL
        ORDER BY ps.created_at
    """)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


CONFIGS = {
    "1_equal_1R": {  # equal 1× regardless of cohort
        "default": 1.0,
    },
    "2_current_yaml": {
        # mirrors config/sizing_weights.yaml at v1
        "crypto_scalp_momentum_continuation": 0.5,
        "stocks_swing_watchlist_rs_rotation": 0.0,
        "stocks_invest_watchlist_30d_thesis": 0.0,
        "C_tier_override": 0.0,
        "stocks_a_intraday_long": 0.5,
        "default": 1.0,
    },
    "3_conservative": {
        # halve all longs in non-edge cohorts; zero out all swing/invest
        "crypto_scalp_momentum_continuation": 0.25,
        "stocks_swing_watchlist_rs_rotation": 0.0,
        "stocks_invest_watchlist_30d_thesis": 0.0,
        "C_tier_override": 0.0,
        "stocks_a_intraday_long": 0.25,
        "stocks_intraday_rth_momentum_long": 0.5,
        "default": 1.0,
    },
    "4_aggressive": {
        # full size on profitable cohorts, zero on losers
        "crypto_scalp_momentum_continuation": 0.5,
        "stocks_swing_watchlist_rs_rotation": 0.0,
        "stocks_invest_watchlist_30d_thesis": 0.0,
        "C_tier_override": 0.0,
        "crypto_failed_bounce_short": 1.5,  # this cohort is +EV — push more
        "crypto_swing_narrative_rs_momentum": 1.5,
        "default": 1.0,
    },
}


def weight_for(signal: dict, config: dict) -> float:
    tier = (signal.get("tier") or "C").upper()
    if tier == "C" and "C_tier_override" in config:
        return config["C_tier_override"]
    try:
        pl = label_for(signal).playbook
    except Exception:
        pl = ""
    direction = (signal.get("direction") or "").lower()
    # fine routes
    if pl == "stocks_intraday_rth_momentum" and tier == "A" and direction == "long" \
            and "stocks_a_intraday_long" in config:
        return config["stocks_a_intraday_long"]
    if pl == "stocks_intraday_rth_momentum" and direction == "long" \
            and "stocks_intraday_rth_momentum_long" in config:
        return config["stocks_intraday_rth_momentum_long"]
    if pl in config:
        return config[pl]
    return config.get("default", 1.0)


def evaluate(signals: list[dict], config: dict) -> dict:
    sized_rs = []
    raw_rs = []
    wins = 0
    losses = 0
    for s in signals:
        raw = float(s["final_r"] or 0.0)
        w = weight_for(s, config)
        sized = raw * w
        raw_rs.append(raw)
        sized_rs.append(sized)
        if sized > 0:
            wins += 1
        elif sized < 0:
            losses += 1
    pf = (sum(r for r in sized_rs if r > 0) /
          abs(sum(r for r in sized_rs if r < 0))) if any(r < 0 for r in sized_rs) else float("inf")
    return {
        "n": len(signals),
        "sum_raw": sum(raw_rs),
        "sum_sized": sum(sized_rs),
        "wins": wins,
        "losses": losses,
        "wr": wins / max(1, wins + losses),
        "pf": pf,
    }


def main() -> None:
    signals = _load_closed_signals()
    print(f"closed signals: {len(signals)}")

    # split temporally
    n = len(signals)
    train_end = int(n * 0.6)
    val_end = int(n * 0.9)
    train = signals[:train_end]
    val = signals[train_end:val_end]
    forward = signals[val_end:]

    def window_dates(rows):
        if not rows:
            return ("", "")
        return (rows[0]["created_at"][:10], rows[-1]["created_at"][:10])

    lines = []
    lines.append("# Playbook Sizing — Walk-Forward Backtest (PART 5)")
    lines.append("")
    lines.append(f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Total closed signals:** {n}")
    lines.append("")
    lines.append("## Temporal split (60% / 30% / 10%)")
    lines.append("")
    lines.append(f"- Train: {train_end} signals · {window_dates(train)[0]} → {window_dates(train)[1]}")
    lines.append(f"- Validation: {val_end - train_end} signals · {window_dates(val)[0]} → {window_dates(val)[1]}")
    lines.append(f"- Forward: {len(forward)} signals · {window_dates(forward)[0]} → {window_dates(forward)[1]}")
    lines.append("")
    lines.append("Weights for each config are chosen with awareness of TRAIN data only. "
                 "Performance is reported on VALIDATION and FORWARD windows — out-of-sample.")
    lines.append("")
    lines.append("## CRITICAL caveat")
    lines.append("")
    lines.append(f"- Only **~20 days** of signal history. Statistical power is LOW. ")
    lines.append("- Use this as a *direction check*, not a conclusive OOS validation.")
    lines.append("- Do NOT optimize weights against validation outputs.")
    lines.append("")
    lines.append("## Results — sum sized R per window")
    lines.append("")
    lines.append("| Config | Train sum R | Val sum R | Forward sum R | Val WR | Val PF |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for cname, cfg in CONFIGS.items():
        m_t = evaluate(train, cfg)
        m_v = evaluate(val, cfg)
        m_f = evaluate(forward, cfg)
        lines.append(f"| {cname} | {m_t['sum_sized']:+.2f} | {m_v['sum_sized']:+.2f} | "
                     f"{m_f['sum_sized']:+.2f} | {m_v['wr']:.0%} | {m_v['pf']:.2f} |")
    lines.append("")
    lines.append("## Interpretation rules")
    lines.append("")
    lines.append("- A config is OOS-positive if **both** validation and forward sums are positive.")
    lines.append("- A config that improves train sum R but degrades forward sum R is overfit and rejected.")
    lines.append("- `1_equal_1R` is the **baseline**; any other config must beat it OOS to justify the complexity.")
    lines.append("")
    lines.append("## Verdict per config")
    lines.append("")
    for cname, cfg in CONFIGS.items():
        m_v = evaluate(val, cfg)
        m_f = evaluate(forward, cfg)
        m_v_eq = evaluate(val, CONFIGS["1_equal_1R"])
        m_f_eq = evaluate(forward, CONFIGS["1_equal_1R"])
        beat_v = m_v["sum_sized"] > m_v_eq["sum_sized"]
        beat_f = m_f["sum_sized"] > m_f_eq["sum_sized"]
        pos = m_v["sum_sized"] > 0 and m_f["sum_sized"] > 0
        verdict = []
        if pos:
            verdict.append("OOS-positive")
        else:
            verdict.append("OOS not consistently positive")
        if cname != "1_equal_1R":
            if beat_v and beat_f:
                verdict.append("beats baseline both windows")
            elif beat_v or beat_f:
                verdict.append("beats baseline in one window only — INCONCLUSIVE")
            else:
                verdict.append("does NOT beat baseline")
        lines.append(f"- **{cname}** — {'; '.join(verdict)}")
    lines.append("")
    lines.append("## Recommendation")
    lines.append("")
    lines.append("- The current YAML config (`2_current_yaml`) is the deployed sizing layer. Its "
                 "OOS performance above is the source of truth for whether to keep, retune, or revert it.")
    lines.append("- Re-run this script weekly as the signal history grows beyond 6-8 weeks; only then "
                 "will sample size give a real OOS verdict.")
    lines.append("- Do NOT change weights based on a single OOS window of <100 signals.")

    out_md = ROOT / "reports" / "PLAYBOOK_SIZING_WALK_FORWARD_BACKTEST.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_md}")


if __name__ == "__main__":
    main()
