"""Compare shallow and deep crypto fast-flush reclaim filters.

The replay rows are produced by research_fast_flush_reclaim_v3.py. This study
does not regenerate entries or outcomes; it changes only the pre-entry sweep
depth filters and keeps the original point-in-time context, execution costs,
stop-first intrabar assumption, and exit mechanics intact.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from scripts.research_fast_flush_reclaim_v3 import _cascade_adjusted, _filter, _summary


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "research_labs" / "fast_flush_reclaim_v3"
SOURCE = LAB / "replay_trades.csv"
OUTPUT = LAB / "depth_sensitivity_result.json"
REPORT = ROOT / "reports" / "CRYPTO_FAST_FLUSH_DEPTH_SENSITIVITY.md"
PROFILE = "FAST_1M_RECLAIM"


COMMON = {
    "min_rvol": 1.0,
    "min_oi_drop_pct": 0.25,
    "max_oi_drop_pct": 5.0,
    "min_liq_percentile": 0.90,
    "max_spread_bps": 18.0,
    "min_stop_distance_pct": 0.0075,
    "max_stop_distance_pct": 0.015,
    "sessions": ("europe", "us"),
}


def _params(*, min_atr: float, max_atr: float, min_pct: float, max_pct: float,
            **overrides: Any) -> dict[str, Any]:
    value = {
        **COMMON,
        "min_flush_atr": min_atr,
        "max_flush_atr": max_atr,
        "min_flush_pct": min_pct,
        "max_flush_pct": max_pct,
    }
    value.update(overrides)
    return value


def _load_rows(path: Path) -> list[dict[str, Any]]:
    frame = pd.read_csv(path)
    frame["event_at"] = pd.to_datetime(frame["event_at"], utc=True)
    rows = frame.to_dict("records")
    for row in rows:
        row["event_at"] = row["event_at"].to_pydatetime()
    return rows


def _split(rows: list[dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, str]]:
    times = sorted({row["event_at"] for row in rows})
    if len(times) < 10:
        raise RuntimeError("insufficient event timestamps for a 60/20/20 chronological split")
    train_cut = times[max(0, int(len(times) * 0.60) - 1)]
    validation_cut = times[max(0, int(len(times) * 0.80) - 1)]
    parts = {
        "train": [row for row in rows if row["event_at"] <= train_cut],
        "validation": [row for row in rows if train_cut < row["event_at"] <= validation_cut],
        "test": [row for row in rows if row["event_at"] > validation_cut],
        "all": rows,
    }
    return parts, {
        "train_end": train_cut.isoformat(),
        "validation_end": validation_cut.isoformat(),
    }


def _evaluate(rows: list[dict[str, Any]], params: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    selected = _cascade_adjusted(_filter(rows, params, PROFILE))
    return selected, _summary(selected)


def _evaluate_parts(parts: dict[str, list[dict[str, Any]]], params: dict[str, Any]) -> dict[str, Any]:
    return {name: _evaluate(rows, params)[1] for name, rows in parts.items()}


def _axis_bands(parts: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    pct_bands = {
        "micro_0.20_0.60pct": (0.20, 0.60),
        "shallow_0.60_1.00pct": (0.60, 1.00),
        "ordinary_1.00_1.50pct": (1.00, 1.50),
        "deep_1.50_2.75pct": (1.50, 2.75),
        "ultra_2.75_5.00pct": (2.75, 5.00),
    }
    atr_bands = {
        "small_0.65_1.50atr": (0.65, 1.50),
        "moderate_1.50_2.50atr": (1.50, 2.50),
        "deep_2.50_4.00atr": (2.50, 4.00),
        "extreme_4.00_7.00atr": (4.00, 7.00),
        "disorderly_7.00_12.00atr": (7.00, 12.00),
    }
    pct_results = {
        name: _evaluate_parts(parts, _params(min_atr=0.65, max_atr=12.0, min_pct=low, max_pct=high))
        for name, (low, high) in pct_bands.items()
    }
    atr_results = {
        name: _evaluate_parts(parts, _params(min_atr=low, max_atr=high, min_pct=0.20, max_pct=5.0))
        for name, (low, high) in atr_bands.items()
    }
    return {"flush_pct_bands": pct_results, "flush_atr_bands": atr_results}


def _neighborhood(parts: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    summaries: list[dict[str, Any]] = []
    for values in itertools.product(
        (2.0, 2.5, 3.0),
        (4.0, 5.0, 6.0),
        (1.25, 1.50, 1.75, 2.0),
        (2.50, 2.75, 3.25),
        (0.25, 0.50, 0.75),
        (3.0, 5.0),
        (0.80, 0.90, 0.95),
        (0.005, 0.0075, 0.010),
        (("us",), ("europe", "us")),
    ):
        min_atr, max_atr, min_pct, max_pct, min_oi, max_oi, liq, min_stop, sessions = values
        if min_atr >= max_atr or min_pct >= max_pct:
            continue
        params = _params(
            min_atr=min_atr, max_atr=max_atr, min_pct=min_pct, max_pct=max_pct,
            min_oi_drop_pct=min_oi, max_oi_drop_pct=max_oi,
            min_liq_percentile=liq, min_stop_distance_pct=min_stop,
            sessions=sessions,
        )
        result = _evaluate_parts(parts, params)
        if result["train"]["trades"] < 6 or result["validation"]["trades"] < 3 or result["test"]["trades"] < 2:
            continue
        summaries.append(result)

    def positive(block: dict[str, Any]) -> bool:
        return block["net_r"] > 0 and (block["pf"] is None or block["pf"] > 1.0)

    if not summaries:
        return {"eligible_configurations": 0}
    return {
        "eligible_configurations": len(summaries),
        "positive_train_pct": round(sum(positive(item["train"]) for item in summaries) / len(summaries), 4),
        "positive_validation_pct": round(sum(positive(item["validation"]) for item in summaries) / len(summaries), 4),
        "positive_test_pct": round(sum(positive(item["test"]) for item in summaries) / len(summaries), 4),
        "positive_all_three_pct": round(
            sum(positive(item["train"]) and positive(item["validation"]) and positive(item["test"])
                for item in summaries) / len(summaries), 4
        ),
        "median_test_trades": float(pd.Series([item["test"]["trades"] for item in summaries]).median()),
        "median_test_net_r": round(float(pd.Series([item["test"]["net_r"] for item in summaries]).median()), 3),
        "median_all_net_r": round(float(pd.Series([item["all"]["net_r"] for item in summaries]).median()), 3),
    }


def _concentration(rows: list[dict[str, Any]], params: dict[str, Any]) -> dict[str, Any]:
    selected, summary = _evaluate(rows, params)
    symbols = Counter(str(row["symbol"]) for row in selected)
    top_symbol, top_count = symbols.most_common(1)[0] if symbols else (None, 0)
    without_top = [row for row in selected if row["symbol"] != top_symbol]
    return {
        "summary": summary,
        "unique_symbols": len(symbols),
        "symbol_counts": dict(symbols.most_common()),
        "top_symbol_share": round(top_count / len(selected), 4) if selected else 0.0,
        "without_top_symbol": _summary(without_top),
    }


def _fmt(summary: dict[str, Any]) -> str:
    return (f"n={summary['trades']}, {summary['net_r']:+.3f}R, PF={summary['pf']}, "
            f"win={summary['winrate']:.1%}, DD=${summary['max_drawdown_usd']:.2f}")


def _write_report(result: dict[str, Any]) -> None:
    lines = [
        "# Crypto Fast Flush - Sweep Depth Sensitivity",
        "",
        f"- generated: `{result['generated_at']}`",
        f"- source period: `{result['period'][0]}` to `{result['period'][1]}`",
        f"- split: train through `{result['split']['train_end']}`, validation through "
        f"`{result['split']['validation_end']}`, then chronological test",
        f"- replay rows: `{result['source_rows']}`; distinct events: `{result['distinct_events']}`",
        "",
        "All figures are net of modeled fees and slippage. The replay remains point-in-time, uses "
        "stop-first handling inside ambiguous bars, and counts one strongest trade per 15-minute "
        "market liquidation cascade.",
        "",
        "Important limitation: these historical rows were used by earlier fast-flush research. The "
        "last 20% is chronological out-of-development evidence for this depth comparison, but it is "
        "not a never-before-seen final holdout for the overall strategy.",
        "",
        "## Fixed Candidates",
        "",
    ]
    for name in ("shallow", "deep"):
        block = result["candidates"][name]
        lines.extend([
            f"### {name.title()}",
            "",
            f"- parameters: `{json.dumps(block['parameters'], sort_keys=True)}`",
            f"- train: {_fmt(block['results']['train'])}",
            f"- validation: {_fmt(block['results']['validation'])}",
            f"- test: {_fmt(block['results']['test'])}",
            f"- all: {_fmt(block['results']['all'])}",
            "",
        ])
    lines.extend(["## One-Dimensional Sensitivity", ""])
    for title, axis in (("Move size", "flush_pct_bands"), ("ATR depth", "flush_atr_bands")):
        lines.extend([f"### {title}", "", "| Band | All | Latest test |", "|---|---:|---:|"])
        for band, block in result["axis_bands"][axis].items():
            lines.append(f"| `{band}` | {_fmt(block['all'])} | {_fmt(block['test'])} |")
        lines.append("")
    n = result["deep_neighborhood"]
    c = result["deep_concentration"]
    lines.extend([
        "## Robustness",
        "",
        f"- eligible nearby deep configurations: `{n['eligible_configurations']}`",
        f"- positive in train: `{n['positive_train_pct']:.1%}`",
        f"- positive in validation: `{n['positive_validation_pct']:.1%}`",
        f"- positive in latest test: `{n['positive_test_pct']:.1%}`",
        f"- positive in all three slices: `{n['positive_all_three_pct']:.1%}`",
        f"- median latest-test result: `{n['median_test_net_r']:+.3f}R` over "
        f"`{n['median_test_trades']:.0f}` trades",
        f"- deep candidate uses `{c['unique_symbols']}` symbols; largest symbol share "
        f"`{c['top_symbol_share']:.1%}`",
        f"- after removing the most frequent symbol: {_fmt(c['without_top_symbol'])}",
        "",
        "## Verdict",
        "",
        "The shallow variant is rejected: it was positive in development but lost money in the "
        "latest chronological test. The very deepest/extreme sweeps also underperformed. The useful "
        "zone is bounded rather than monotonic: roughly 2.5-4 ATR and 1.5-2.75% flushes.",
        "",
        "The broader deep candidate (2-5 ATR, 1.5-2.75%, strong liquidation percentile, Europe/US) "
        "is suitable for a separate Paper profile. It is not ready for Live: the full sample is still "
        "small and the final slice is not a globally untouched holdout.",
    ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(path: Path = SOURCE) -> dict[str, Any]:
    rows = _load_rows(path)
    parts, split = _split(rows)
    shallow = _params(
        min_atr=1.25, max_atr=2.25, min_pct=0.60, max_pct=1.20,
        min_oi_drop_pct=1.0, min_liq_percentile=0.80,
        min_stop_distance_pct=0.005,
    )
    deep = _params(min_atr=2.0, max_atr=5.0, min_pct=1.50, max_pct=2.75)
    event_times = sorted({row["event_at"] for row in rows})
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "period": [event_times[0].isoformat(), event_times[-1].isoformat()],
        "source_rows": len(rows),
        "distinct_events": len({row["event_id"] for row in rows}),
        "profile": PROFILE,
        "split": split,
        "method": {
            "chronological_split": "60/20/20",
            "cascade_adjustment": "one strongest trade per 15-minute market episode",
            "intrabar_assumption": "stop_first",
            "costs": "preserved from original point-in-time replay",
        },
        "axis_bands": _axis_bands(parts),
        "candidates": {
            "shallow": {"parameters": shallow, "results": _evaluate_parts(parts, shallow)},
            "deep": {"parameters": deep, "results": _evaluate_parts(parts, deep)},
        },
        "deep_neighborhood": _neighborhood(parts),
        "deep_concentration": _concentration(rows, deep),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    _write_report(result)
    return result


def main() -> None:
    result = run()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
