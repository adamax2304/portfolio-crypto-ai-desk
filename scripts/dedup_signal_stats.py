"""Dedup signal performance analysis — manual companion to ``signal-stats``.

Read-only. Builds:
  - raw stats per asset_class × tier × mode (what ``signal-stats`` shows);
  - deduped stats: one canonical signal per unique setup
    ``(symbol, asset_class, mode, direction, tier, day)`` with entry zone
    and invalidation within tolerance.

Canonical pick rule:
  - take the earliest A/B signal of the setup;
  - replace it only if a later signal materially improved by tier (rank up),
    score (>=5), entry mid (>=0.5%), or invalidation (>=0.5%).

Outputs JSON on stdout — the caller writes the human report.
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

from src.config import load_config
from src.storage.sqlite import SQLiteStore

SCORE_DELTA = 5.0
ENTRY_PCT = 0.5
INV_PCT = 0.5


def _tier_rank(t: str) -> int:
    return {"A": 3, "B": 2, "C": 1}.get((t or "").upper(), 0)


def _mid(sig: dict[str, Any]) -> float | None:
    lo = sig.get("entry_low")
    hi = sig.get("entry_high")
    try:
        if lo is not None and hi is not None:
            return (float(lo) + float(hi)) / 2.0
        if lo is not None:
            return float(lo)
        if hi is not None:
            return float(hi)
    except (TypeError, ValueError):
        return None
    return None


def _day(sig: dict[str, Any]) -> str:
    return str(sig.get("created_at") or "")[:10]


def _improved(later: dict[str, Any], current: dict[str, Any]) -> bool:
    """Did ``later`` materially improve over ``current``? Mirrors the
    MaterialImprovementChecker logic but without the AlertDecision wrapper."""
    if _tier_rank(later.get("tier", "")) > _tier_rank(current.get("tier", "")):
        return True
    try:
        if float(later.get("score") or 0) - float(current.get("score") or 0) >= SCORE_DELTA:
            return True
    except (TypeError, ValueError):
        pass
    cur_mid = _mid(current)
    new_mid = _mid(later)
    if cur_mid and new_mid:
        denom = max(abs(cur_mid), 1e-9)
        if abs(new_mid - cur_mid) / denom * 100.0 >= ENTRY_PCT:
            return True
    try:
        cur_inv = float(current.get("invalidation") or 0)
        new_inv = float(later.get("invalidation") or 0)
        if cur_inv and new_inv:
            denom = max(abs(cur_inv), 1e-9)
            if abs(new_inv - cur_inv) / denom * 100.0 >= INV_PCT:
                return True
    except (TypeError, ValueError):
        pass
    return False


def _agg(signals: list[dict[str, Any]], outcomes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Aggregate stats over a list of signals."""
    sample = len(signals)
    triggered = 0
    wins = 0
    losses = 0
    tp1 = 0
    tp2 = 0
    tp3 = 0
    stopped = 0
    not_triggered = 0
    sum_r = 0.0
    sum_pos = 0.0
    sum_neg_abs = 0.0
    for sig in signals:
        out = outcomes.get(sig["signal_id"]) or {}
        status = (sig.get("status") or "").lower()
        if int(out.get("entry_triggered") or 0) or status in {
            "triggered", "tp1_hit", "tp2_hit", "tp3_hit", "stopped"
        }:
            triggered += 1
        else:
            if status in {"missed_no_entry", "expired"} and not int(out.get("entry_triggered") or 0):
                not_triggered += 1
        if int(out.get("tp1_hit") or 0):
            tp1 += 1
        if int(out.get("tp2_hit") or 0):
            tp2 += 1
        if int(out.get("tp3_hit") or 0):
            tp3 += 1
        if int(out.get("stop_hit") or 0):
            stopped += 1
        final_outcome = (out.get("final_outcome") or "").lower()
        if final_outcome == "win":
            wins += 1
        elif final_outcome == "loss":
            losses += 1
        r = out.get("final_r")
        if r is not None:
            try:
                rv = float(r)
                sum_r += rv
                if rv > 0:
                    sum_pos += rv
                elif rv < 0:
                    sum_neg_abs += -rv
            except (TypeError, ValueError):
                pass
    closed = wins + losses
    winrate = (wins / closed) if closed else None
    tp1_rate = (tp1 / triggered) if triggered else None
    stop_rate = (stopped / triggered) if triggered else None
    avg_r = (sum_r / closed) if closed else None
    pf = (sum_pos / sum_neg_abs) if sum_neg_abs > 0 else (float("inf") if sum_pos > 0 else None)
    return {
        "sample": sample,
        "triggered": triggered,
        "not_triggered": not_triggered,
        "wins": wins,
        "losses": losses,
        "tp1_hits": tp1,
        "tp2_hits": tp2,
        "tp3_hits": tp3,
        "stopped": stopped,
        "winrate": winrate,
        "tp1_hit_rate": tp1_rate,
        "stop_rate": stop_rate,
        "avg_r": avg_r,
        "total_r": sum_r,
        "profit_factor": pf if pf != float("inf") else "inf",
    }


def _select_canonical(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group by (symbol, asset_class, mode, direction, tier, day) and apply
    the canonical-pick rule."""
    by_key: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    for sig in signals:
        key = (
            sig.get("symbol"),
            sig.get("asset_class"),
            sig.get("mode"),
            sig.get("direction"),
            sig.get("tier"),
            _day(sig),
        )
        by_key[key].append(sig)
    canonicals: list[dict[str, Any]] = []
    for key, group in by_key.items():
        group.sort(key=lambda r: r.get("created_at") or "")
        canonical = group[0]
        for later in group[1:]:
            if _improved(later, canonical):
                canonical = later
        canonicals.append(canonical)
    return canonicals


def main() -> None:
    config = load_config()
    db = SQLiteStore(config.db_path)
    db.init_db()

    with db.connect() as conn:
        signals = [dict(r) for r in conn.execute("SELECT * FROM proposed_signals").fetchall()]
        outcome_rows = [dict(r) for r in conn.execute(
            "SELECT * FROM signal_outcomes ORDER BY checked_at ASC"
        ).fetchall()]

    # Latest outcome per signal_id.
    latest_outcome: dict[str, dict[str, Any]] = {}
    for row in outcome_rows:
        latest_outcome[row["signal_id"]] = row

    # Filter A/B for performance views (C-tier kept as own bucket).
    def _bucket(filt) -> dict[str, Any]:
        raw = [s for s in signals if filt(s)]
        dedup = _select_canonical(raw)
        return {
            "raw_count": len(raw),
            "dedup_count": len(dedup),
            "raw_stats": _agg(raw, latest_outcome),
            "dedup_stats": _agg(dedup, latest_outcome),
        }

    out = {
        "totals": {
            "all_signals": len(signals),
            "outcome_rows": len(outcome_rows),
            "unique_signals_with_outcomes": len(latest_outcome),
        },
        "stocks_all": _bucket(lambda s: s.get("asset_class") == "stocks"),
        "stocks_AB": _bucket(lambda s: s.get("asset_class") == "stocks" and s.get("tier") in {"A", "B"}),
        "stocks_A_only": _bucket(lambda s: s.get("asset_class") == "stocks" and s.get("tier") == "A"),
        "stocks_B_only": _bucket(lambda s: s.get("asset_class") == "stocks" and s.get("tier") == "B"),
        "stocks_C_only": _bucket(lambda s: s.get("asset_class") == "stocks" and s.get("tier") == "C"),
        "stocks_intraday_AB": _bucket(lambda s: s.get("asset_class") == "stocks" and s.get("mode") == "intraday" and s.get("tier") in {"A", "B"}),
        "crypto_all": _bucket(lambda s: s.get("asset_class") == "crypto"),
        "crypto_AB": _bucket(lambda s: s.get("asset_class") == "crypto" and s.get("tier") in {"A", "B"}),
        "crypto_A_only": _bucket(lambda s: s.get("asset_class") == "crypto" and s.get("tier") == "A"),
        "crypto_B_only": _bucket(lambda s: s.get("asset_class") == "crypto" and s.get("tier") == "B"),
        "crypto_scalp_AB": _bucket(lambda s: s.get("asset_class") == "crypto" and s.get("mode") == "scalp" and s.get("tier") in {"A", "B"}),
        "crypto_intraday_AB": _bucket(lambda s: s.get("asset_class") == "crypto" and s.get("mode") == "intraday" and s.get("tier") in {"A", "B"}),
    }
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
