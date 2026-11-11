from __future__ import annotations

import math
from collections import defaultdict
from typing import Any

import numpy as np


def _profit_factor(values: list[float]) -> float | None:
    gains = sum(float(value) for value in values if float(value) > 0)
    losses = -sum(float(value) for value in values if float(value) < 0)
    if not values:
        return None
    if losses == 0:
        return float("inf") if gains > 0 else 0.0
    return gains / losses


def _max_drawdown(values: list[float]) -> float:
    equity = peak = drawdown = 0.0
    for value in values:
        equity += float(value)
        peak = max(peak, equity)
        drawdown = max(drawdown, peak - equity)
    return round(drawdown, 6)


def _concentration(rows: list[dict[str, Any]]) -> tuple[float | None, float | None]:
    positive = [float(row.get("net_pnl_usd") or 0.0) for row in rows if float(row.get("net_pnl_usd") or 0.0) > 0]
    total = sum(positive)
    top5 = sum(sorted(positive, reverse=True)[:5]) / total if total > 0 else None
    by_symbol: dict[str, float] = defaultdict(float)
    for row in rows:
        pnl = float(row.get("net_pnl_usd") or 0.0)
        if pnl > 0:
            by_symbol[str(row.get("symbol") or "unknown")] += pnl
    symbol_share = max(by_symbol.values()) / total if total > 0 and by_symbol else None
    return top5, symbol_share


def _metric(run_id: str, variant_id: str, fold_id: str, trades: list[dict[str, Any]],
            candidates: list[dict[str, Any]]) -> dict[str, Any]:
    closed = [row for row in trades if row.get("exit_at") or row.get("close_reason")]
    pnl = [float(row.get("net_pnl_usd") or 0.0) for row in closed]
    net_r = [float(row.get("net_r") or 0.0) for row in closed]
    rejections: dict[str, int] = defaultdict(int)
    for row in candidates:
        if str(row.get("status")) == "rejected":
            rejections[str(row.get("rejection_reason") or "UNKNOWN")] += 1
    import json
    return {
        "run_id": run_id,
        "variant_id": variant_id,
        "fold_id": fold_id,
        "clean_closed": len(closed),
        "net_pnl_usd": round(sum(pnl), 6),
        "net_r": round(sum(net_r), 6),
        "profit_factor": _profit_factor(pnl),
        "winrate": (sum(value > 0 for value in pnl) / len(pnl)) if pnl else None,
        "max_drawdown_r": _max_drawdown(net_r),
        "top5_profit_share": _concentration(closed)[0],
        "max_symbol_profit_share": _concentration(closed)[1],
        "rejection_counts_json": json.dumps(dict(sorted(rejections.items())), sort_keys=True),
    }


def _bh_adjust(pvalues: dict[str, float | None]) -> dict[str, float | None]:
    valid = sorted((key, float(value)) for key, value in pvalues.items() if value is not None)
    if not valid:
        return {key: None for key in pvalues}
    m = len(valid)
    adjusted: dict[str, float] = {}
    running = 1.0
    for rank_from_end, (key, pvalue) in enumerate(reversed(valid), start=1):
        rank = m - rank_from_end + 1
        running = min(running, pvalue * m / rank)
        adjusted[key] = min(1.0, running)
    return {key: adjusted.get(key) for key in pvalues}


def _bootstrap_control_delta_p(rows: list[dict[str, Any]], control: list[dict[str, Any]],
                               samples: int, seed: int) -> tuple[float | None, float]:
    pnl = np.asarray([float(row.get("net_pnl_usd") or 0.0) for row in rows], dtype=float)
    control_pnl = np.asarray([float(row.get("net_pnl_usd") or 0.0) for row in control], dtype=float)
    delta = float(pnl.sum() - control_pnl.sum())
    if len(pnl) < 5 or len(control_pnl) < 5:
        return None, delta
    rng = np.random.default_rng(seed)
    count = max(100, int(samples))
    wins = 0
    for _ in range(count):
        left = rng.choice(pnl, len(pnl), replace=True).sum()
        right = rng.choice(control_pnl, len(control_pnl), replace=True).sum()
        if left - right <= 0:
            wins += 1
    return (wins + 1) / (count + 1), delta


def _neighbors(variant: dict[str, Any], variants: list[dict[str, Any]]) -> list[str]:
    ignored = {"variant_id", "parameter_hash"}
    out: list[str] = []
    for other in variants:
        if other is variant:
            continue
        differences = [
            key for key in set(variant) | set(other)
            if key not in ignored and variant.get(key) != other.get(key)
        ]
        if len(differences) == 1:
            out.append(str(other.get("variant_id")))
    return out

