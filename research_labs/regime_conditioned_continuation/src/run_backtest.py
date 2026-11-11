from __future__ import annotations

import argparse
import json
import math
import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from research_labs.technical_trend_reclaim.src.common import (
    LEDGER_PATH as ARCHIVE_LEDGER_PATH,
    archive_path,
    file_sha256 as shared_file_sha256,
    load_symbols_from_project,
)
from research_labs.technical_trend_reclaim.src.engine import Fold, evaluate_variant, load_bundle
from research_labs.technical_trend_reclaim.src.run_backtest import (
    _bh_adjust,
    _bootstrap_control_delta_p,
    _concentration,
    _max_drawdown,
    _metric,
    _neighbors,
    _profit_factor,
)

from .common import (
    ARTIFACT_ROOT,
    LAB_ROOT,
    connect,
    digest,
    file_sha256,
    insert_many,
    load_config,
    parameter_grid,
    stable_json,
    utc_now,
)
from .regime import classify_snapshot, regime_snapshot


CONTROL_ID = "control_unconditioned"
SNAPSHOT_ID = "__structural_snapshot__"
FROZEN_PROFILE_PATH = ARTIFACT_ROOT / "FROZEN_DEVELOPMENT_SHORTLIST_CRYPTO.json"


def _chronological_trades(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            str(row.get("exit_at") or row.get("entry_at") or ""),
            str(row.get("entry_at") or ""),
            str(row.get("trade_id") or row.get("candidate_id") or ""),
        ),
    )


def _archive_hash(symbols: list[str]) -> str:
    import sqlite3

    if not ARCHIVE_LEDGER_PATH.exists():
        return "manifest_missing"
    conn = sqlite3.connect(ARCHIVE_LEDGER_PATH)
    conn.row_factory = sqlite3.Row
    wanted = set(symbols)
    rows = conn.execute(
        "SELECT asset,source,symbol,timeframe,sha256,collected_at FROM data_series_manifest "
        "WHERE asset IN ('crypto','crypto_derivatives') ORDER BY collected_at DESC"
    ).fetchall()
    latest: dict[tuple[str, str, str], tuple[str, str]] = {}
    for row in rows:
        symbol = str(row["symbol"])
        if symbol not in wanted:
            continue
        key = (str(row["asset"]), symbol, str(row["timeframe"]))
        latest.setdefault(key, (str(row["source"]), str(row["sha256"])))
    return digest(sorted((key, value) for key, value in latest.items()))


def _code_hash() -> str:
    files = list((LAB_ROOT / "src").glob("*.py"))
    shared = Path(__file__).resolve().parents[2] / "technical_trend_reclaim" / "src"
    files.extend(shared / name for name in ("engine.py", "features.py", "simulator.py"))
    return digest({str(path): shared_file_sha256(path) for path in sorted(files)})


def _folds(start: pd.Timestamp, end: pd.Timestamp, stage: str, cfg: dict[str, Any]) -> list[Fold]:
    exp = cfg["experiment"]
    dev_end = pd.Timestamp(exp["development_end"])
    validation_end = pd.Timestamp(exp["validation_end"])
    audit_end = min(pd.Timestamp(exp["known_audit_end"]), end.ceil("D"))
    if stage == "validation":
        return [Fold("historical_validation", dev_end, validation_end)]
    if stage == "known_audit":
        return [Fold("audit_known_period", validation_end, audit_end)]
    evaluation_start = start.floor("D") + pd.Timedelta(days=int(exp["warmup_days"]))
    if evaluation_start >= dev_end:
        raise RuntimeError("archive does not contain enough pre-development history")
    count = int(exp["development_folds"])
    span_days = int((dev_end - evaluation_start).days)
    boundaries = [evaluation_start]
    for index in range(1, count):
        boundaries.append(evaluation_start + pd.Timedelta(days=int(span_days * index / count)))
    boundaries.append(dev_end)
    return [Fold(f"development_oos_{index + 1}", boundaries[index], boundaries[index + 1]) for index in range(count)]


def _control_variant(base: dict[str, Any]) -> dict[str, Any]:
    row = dict(base)
    row["variant_id"] = CONTROL_ID
    row["parameter_hash"] = digest(row)
    return row


def _load_frozen_variant(path: str | Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    frozen_path = Path(path) if path else FROZEN_PROFILE_PATH
    if not frozen_path.exists():
        raise RuntimeError(
            "validation/audit requires the profile frozen by a full-universe development run"
        )
    payload = json.loads(frozen_path.read_text(encoding="utf-8"))
    variant = payload.get("variant")
    if not isinstance(variant, dict) or not variant.get("variant_id"):
        raise RuntimeError("frozen profile is missing a valid variant")
    if payload.get("next_stage") not in {"historical_validation_only", "known_audit_only"}:
        raise RuntimeError("frozen profile has an invalid stage transition")
    return dict(variant), payload


def _evaluate_symbol_worker(
    symbol: str, cfg: dict[str, Any], variants: list[dict[str, Any]], folds: list[Fold], run_id: str,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    bundle = load_bundle("crypto", symbol, cfg["strategy"])
    btc = load_bundle("crypto", "BTC/USDT", cfg["strategy"])
    if bundle is None or btc is None:
        return symbol, [], []
    candidates: list[dict[str, Any]] = []
    trades: list[dict[str, Any]] = []
    snapshot_variant = dict(variants[0])
    snapshot_variant["variant_id"] = SNAPSHOT_ID
    for fold in folds:
        def snapshot_gate(current: Any, at: pd.Timestamp, direction: str, params: dict[str, Any]):
            return True, None, regime_snapshot(current, btc.context, at, direction, cfg["strategy"])

        base_rows, base_fills = evaluate_variant(
            run_id=run_id, bundle=bundle, variant=snapshot_variant, fold=fold, cfg=cfg,
            regime_gate=snapshot_gate, ignore_symbol_busy=True,
        )
        control_rows, control_fills = _materialize_profile(
            base_rows, base_fills, CONTROL_ID, fold, variant=None,
        )
        candidates.extend(control_rows)
        trades.extend(control_fills)
        for variant in variants:
            rows, fills = _materialize_profile(
                base_rows, base_fills, str(variant["variant_id"]), fold, variant=variant,
            )
            candidates.extend(rows)
            trades.extend(fills)
    return symbol, candidates, trades


def _materialize_profile(
    base_rows: list[dict[str, Any]], base_fills: list[dict[str, Any]],
    variant_id: str, fold: Fold, variant: dict[str, Any] | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fills_by_candidate = {str(row["candidate_id"]): row for row in base_fills}
    rows_out: list[dict[str, Any]] = []
    fills_out: list[dict[str, Any]] = []
    busy_until: pd.Timestamp | None = None
    for source in base_rows:
        row = dict(source)
        row["variant_id"] = variant_id
        features = json.loads(str(row["features_json"]))
        snapshot = features.get("regime_conditioned")
        if variant is not None and snapshot is not None:
            gate_reason = classify_snapshot(snapshot, variant)
            if gate_reason is not None:
                row.update({
                    "decision_at": snapshot.get("at") or row["decision_at"],
                    "entry_at": None, "status": "rejected",
                    "rejection_reason": gate_reason,
                    "source_quality": "HISTORICAL_RECONSTRUCTION",
                    "geometry_json": "{}",
                })
                rows_out.append(row)
                continue

        fill = fills_by_candidate.get(str(row["candidate_id"]))
        if fill is not None:
            entry_at = pd.to_datetime(fill["entry_at"], utc=True)
            if busy_until is not None and entry_at <= busy_until:
                row.update({
                    "status": "rejected", "rejection_reason": "SYMBOL_POSITION_ALREADY_OPEN",
                    "geometry_json": "{}",
                })
                rows_out.append(row)
                continue
            copied_fill = dict(fill)
            copied_fill["variant_id"] = variant_id
            fills_out.append(copied_fill)
            busy_until = (
                pd.to_datetime(fill["exit_at"], utc=True) if fill.get("exit_at") else fold.end
            )
        rows_out.append(row)
    return rows_out, fills_out


def _bootstrap_p(rows: list[dict[str, Any]], samples: int, seed: int) -> float | None:
    by_day: dict[str, float] = defaultdict(float)
    for row in rows:
        by_day[str(row.get("exit_at") or row["entry_at"])[:10]] += float(row["net_pnl_usd"])
    values = np.asarray(list(by_day.values()), dtype=float)
    if len(values) < 10:
        return None
    rng = np.random.default_rng(seed)
    means = np.asarray([rng.choice(values, len(values), replace=True).mean() for _ in range(samples)])
    return float((np.sum(means <= 0.0) + 1) / (samples + 1))


def _select(
    run_id: str, cfg: dict[str, Any], variants: list[dict[str, Any]],
    metrics: list[dict[str, Any]], trades: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    selection = cfg["selection"]
    by_variant: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_metrics: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in trades:
        by_variant[str(row["variant_id"])].append(row)
    for row in metrics:
        by_metrics[str(row["variant_id"])].append(row)
    control = by_variant.get(CONTROL_ID, [])
    tests = {
        str(variant["variant_id"]): _bootstrap_control_delta_p(
            by_variant.get(str(variant["variant_id"]), []), control,
            int(cfg["experiment"]["bootstrap_samples"]), int(cfg["experiment"]["random_seed"]),
        ) for variant in variants
    }
    raw_p = {
        variant_id: _bootstrap_p(
            by_variant.get(variant_id, []), int(cfg["experiment"]["bootstrap_samples"]),
            int(cfg["experiment"]["random_seed"]),
        ) for variant_id in tests
    }
    qvalues = _bh_adjust(raw_p)
    pooled: dict[str, dict[str, Any]] = {}
    for variant in variants:
        variant_id = str(variant["variant_id"])
        rows = _chronological_trades(by_variant.get(variant_id, []))
        pnl = [float(row["net_pnl_usd"]) for row in rows]
        net_r = [float(row["net_r"]) for row in rows]
        top5, symbol_share = _concentration(rows)
        fold_rows = by_metrics.get(variant_id, [])
        positive_folds = sum(float(row["net_pnl_usd"]) > 0 for row in fold_rows)
        fold_pf = [float(row["profit_factor"]) for row in fold_rows if row["profit_factor"] is not None]
        fold_expectancy = [float(row["net_pnl_usd"]) / int(row["clean_closed"]) for row in fold_rows if row["clean_closed"]]
        pooled[variant_id] = {
            "clean_closed": len(rows), "net_pnl_usd": sum(pnl), "net_r": sum(net_r),
            "profit_factor": _profit_factor(pnl), "max_drawdown_r": _max_drawdown(net_r),
            "winrate": (sum(value > 0 for value in pnl) / len(pnl)) if pnl else None,
            "top5_profit_share": top5, "max_symbol_profit_share": symbol_share,
            "positive_folds": positive_folds, "min_fold_pf": min(fold_pf) if fold_pf else None,
            "median_fold_expectancy": float(np.median(fold_expectancy)) if fold_expectancy else None,
            "unique_days": len({str(row.get("exit_at") or row["entry_at"])[:10] for row in rows}),
            "unique_symbols": len({str(row["symbol"]) for row in rows}),
            "control_frequency_retention": len(rows) / len(control) if control else None,
            "control_with_skips_delta_usd": tests[variant_id][1],
        }

    results: list[dict[str, Any]] = []
    for variant in variants:
        variant_id = str(variant["variant_id"])
        p = pooled[variant_id]
        reasons: list[str] = []
        if p["clean_closed"] < int(selection["min_clean_trades"]): reasons.append("INSUFFICIENT_CLEAN_TRADES")
        if p["unique_days"] < int(selection["min_unique_days"]): reasons.append("INSUFFICIENT_UNIQUE_DAYS")
        if p["unique_symbols"] < int(selection["min_unique_symbols"]): reasons.append("INSUFFICIENT_UNIQUE_SYMBOLS")
        if p["net_pnl_usd"] <= 0 or p["net_r"] <= 0: reasons.append("NON_POSITIVE_NET_RESULT")
        if p["profit_factor"] is None or p["profit_factor"] < float(selection["pooled_profit_factor_min"]): reasons.append("POOLED_PF_BELOW_GATE")
        if p["positive_folds"] < int(selection["min_positive_folds"]): reasons.append("INSUFFICIENT_POSITIVE_FOLDS")
        if p["min_fold_pf"] is None or p["min_fold_pf"] < float(selection["per_fold_profit_factor_floor"]): reasons.append("FOLD_COLLAPSE")
        if p["max_drawdown_r"] > float(selection["max_drawdown_r"]): reasons.append("DRAWDOWN_TOO_HIGH")
        if p["median_fold_expectancy"] is None or p["median_fold_expectancy"] <= 0: reasons.append("MEDIAN_FOLD_EXPECTANCY_NOT_POSITIVE")
        if p["top5_profit_share"] is None or p["top5_profit_share"] > float(selection["max_top5_profit_share"]): reasons.append("TOP5_CONCENTRATION")
        if p["max_symbol_profit_share"] is None or p["max_symbol_profit_share"] > float(selection["max_symbol_profit_share"]): reasons.append("SYMBOL_CONCENTRATION")
        if p["control_frequency_retention"] is None or p["control_frequency_retention"] < float(selection["min_control_frequency_retention"]): reasons.append("FREQUENCY_COLLAPSE")
        if p["control_with_skips_delta_usd"] <= 0: reasons.append("CONTROL_DELTA_NOT_POSITIVE")
        if qvalues.get(variant_id) is None or float(qvalues[variant_id]) > float(cfg["experiment"]["fdr_q"]): reasons.append("ABSOLUTE_EDGE_FDR_NOT_PASSED")
        neighbours = _neighbors(variant, variants)
        stable = sum(
            pooled[other]["net_pnl_usd"] > 0 and (pooled[other]["profit_factor"] or 0) >= 1.0
            for other in neighbours
        )
        plateau_ok = stable >= max(1, math.ceil(len(neighbours) / 2))
        if not plateau_ok: reasons.append("PARAMETER_KNIFE_EDGE")
        results.append({
            "run_id": run_id, "variant_id": variant_id,
            "verdict": "SHORTLIST_ELIGIBLE" if not reasons else "REJECT",
            "reasons_json": stable_json(reasons), "pooled_metrics_json": stable_json(p),
            "bootstrap_p": raw_p.get(variant_id), "fdr_q": qvalues.get(variant_id),
            "plateau_ok": int(plateau_ok), "selected": 0,
        })

    eligible = [row for row in results if row["verdict"] == "SHORTLIST_ELIGIBLE"]
    if eligible:
        best_expectancy = max(pooled[row["variant_id"]]["median_fold_expectancy"] for row in eligible)
        plateau = [row for row in eligible if pooled[row["variant_id"]]["median_fold_expectancy"] >= 0.90 * best_expectancy]
        lookup = {str(row["variant_id"]): row for row in variants}
        def complexity(row: dict[str, Any]) -> tuple[float, float]:
            variant = lookup[row["variant_id"]]
            score = (
                float(variant["btc_adx_min"]) / 22.0
                + float(variant["btc_slope_min_atr"]) / 0.15
                + float(variant["rs_24h_min_pct"]) / 2.0
                + float(variant["vol_ratio_min"]) / 1.10
            )
            return score, pooled[row["variant_id"]]["max_drawdown_r"]
        selected = min(plateau, key=complexity)
        selected["selected"] = 1
        selected["verdict"] = "FROZEN_DEVELOPMENT_SHORTLIST"
    return results


def _render_report(
    run_id: str, stage: str, config_hash: str, code_hash: str, archive_hash: str,
    selections: list[dict[str, Any]], metrics: list[dict[str, Any]],
) -> str:
    lines = [
        "# Regime-Conditioned Continuation backtest", "",
        f"- run: `{run_id}`", f"- stage: `{stage}`", f"- config hash: `{config_hash}`",
        f"- code hash: `{code_hash}`", f"- archive hash: `{archive_hash}`", "",
        "Historical reconstruction is research evidence only.", "",
        "| variant | verdict | trades | net USD | PF | WR | DD R | positive folds | reasons |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    if selections:
        for row in selections:
            pooled = json.loads(row["pooled_metrics_json"])
            reasons = ", ".join(json.loads(row["reasons_json"])) or "-"
            lines.append(
                f"| {row['variant_id']} | {row['verdict']} | {pooled['clean_closed']} | "
                f"{pooled['net_pnl_usd']:.2f} | {pooled['profit_factor'] or 0:.3f} | "
                f"{(pooled['winrate'] or 0) * 100:.1f}% | {pooled['max_drawdown_r']:.2f} | "
                f"{pooled['positive_folds']} | {reasons} |"
            )
    else:
        for row in metrics:
            if row["variant_id"] == CONTROL_ID:
                continue
            lines.append(
                f"| {row['variant_id']} | MEASUREMENT_ONLY | {row['clean_closed']} | "
                f"{row['net_pnl_usd']:.2f} | {row['profit_factor'] or 0:.3f} | "
                f"{(row['winrate'] or 0) * 100:.1f}% | {row['max_drawdown_r']:.2f} | 1 | - |"
            )
    return "\n".join(lines) + "\n"


def run(
    stage: str, config_path: str | Path | None = None, workers: int | None = None,
    symbols_override: list[str] | None = None, frozen_path: str | Path | None = None,
) -> dict[str, Any]:
    cfg = load_config(config_path)
    all_variants = parameter_grid(cfg)
    frozen_payload: dict[str, Any] | None = None
    if stage == "development":
        variants = all_variants
    else:
        frozen_variant, frozen_payload = _load_frozen_variant(frozen_path)
        known = {str(row["variant_id"]): row for row in all_variants}
        frozen_id = str(frozen_variant["variant_id"])
        if frozen_id not in known or stable_json(known[frozen_id]) != stable_json(frozen_variant):
            raise RuntimeError("frozen profile does not match the current parameter grid/config")
        variants = [known[frozen_id]]
    crypto, _ = load_symbols_from_project()
    if symbols_override:
        wanted = {value.upper() for value in symbols_override}
        crypto = [symbol for symbol in crypto if symbol.upper() in wanted]
    bundles = [bundle for symbol in crypto if (bundle := load_bundle("crypto", symbol, cfg["strategy"])) is not None]
    if not bundles:
        raise RuntimeError("no crypto archive bundles")
    start = min(pd.to_datetime(bundle.context["bar_open_at"].min(), utc=True) for bundle in bundles)
    end = max(pd.to_datetime(bundle.context["bar_close_at"].max(), utc=True) for bundle in bundles)
    folds = _folds(start, end, stage, cfg)
    selected_config = Path(config_path) if config_path else LAB_ROOT / "config" / "crypto_v1.yaml"
    config_hash = file_sha256(selected_config)
    code_hash = _code_hash()
    archive_hash = _archive_hash(crypto)
    created = utc_now().isoformat()
    run_id = digest({"created": created, "stage": stage, "config": config_hash, "archive": archive_hash})[:24]
    run_row = {
        "run_id": run_id, "created_at": created, "stage": stage,
        "config_hash": config_hash, "code_hash": code_hash, "archive_hash": archive_hash,
        "status": "RUNNING", "notes_json": stable_json({
            "symbols": len(bundles), "folds": [fold.fold_id for fold in folds],
            "scope": "subset_smoke" if symbols_override else "full_universe",
            "frozen_development_run_id": (frozen_payload or {}).get("run_id"),
        }),
    }
    with connect() as conn:
        insert_many(conn, "experiment_runs", [run_row])
        insert_many(conn, "parameter_sets", [{
            "run_id": run_id, "variant_id": row["variant_id"], "parameter_hash": row["parameter_hash"],
            "parameters_json": stable_json(row),
        } for row in variants])
    all_candidates: list[dict[str, Any]] = []
    all_trades: list[dict[str, Any]] = []
    worker_count = max(1, int(workers or min(8, max(1, (os.cpu_count() or 2) - 1))))
    try:
        if worker_count == 1:
            evaluated = [_evaluate_symbol_worker(symbol, cfg, variants, folds, run_id) for symbol in crypto]
        else:
            with ProcessPoolExecutor(max_workers=worker_count) as pool:
                pending = {
                    pool.submit(_evaluate_symbol_worker, symbol, cfg, variants, folds, run_id): symbol
                    for symbol in crypto
                }
                evaluated = [future.result() for future in as_completed(pending)]
        for symbol, candidates, trades in evaluated:
            all_candidates.extend(candidates)
            all_trades.extend(trades)
            print(f"evaluated {symbol}: candidates={len(candidates)} trades={len(trades)}")
    except BaseException as exc:
        with connect() as conn:
            conn.execute(
                "UPDATE experiment_runs SET status='FAILED',notes_json=? WHERE run_id=?",
                (stable_json({"error": f"{type(exc).__name__}: {exc}"}), run_id),
            )
        raise

    metrics: list[dict[str, Any]] = []
    variant_ids = [CONTROL_ID] + [str(row["variant_id"]) for row in variants]
    for fold in folds:
        for variant_id in variant_ids:
            fold_trades = _chronological_trades([
                row for row in all_trades
                if row["fold_id"] == fold.fold_id and row["variant_id"] == variant_id
            ])
            fold_candidates = [row for row in all_candidates if row["fold_id"] == fold.fold_id and row["variant_id"] == variant_id]
            metrics.append(_metric(run_id, variant_id, fold.fold_id, fold_trades, fold_candidates))
    selections = (
        _select(run_id, cfg, variants, metrics, all_trades)
        if stage == "development" and not symbols_override else []
    )
    with connect() as conn:
        insert_many(conn, "candidates", all_candidates)
        insert_many(conn, "trades", all_trades)
        insert_many(conn, "fold_metrics", metrics)
        insert_many(conn, "selection_results", selections)
        conn.execute("UPDATE experiment_runs SET status='COMPLETE' WHERE run_id=?", (run_id,))
    report = ARTIFACT_ROOT / f"BACKTEST_CRYPTO_{stage.upper()}_{run_id}.md"
    report.write_text(_render_report(run_id, stage, config_hash, code_hash, archive_hash, selections, metrics), encoding="utf-8")
    selected = [row for row in selections if row["selected"]]
    if selected:
        selected_id = selected[0]["variant_id"]
        variant = next(row for row in variants if row["variant_id"] == selected_id)
        FROZEN_PROFILE_PATH.write_text(stable_json({
            "run_id": run_id, "frozen_at": utc_now().isoformat(), "config_hash": config_hash,
            "code_hash": code_hash, "archive_hash": archive_hash, "variant": variant,
            "selection": selected[0], "next_stage": "historical_validation_only",
        }) + "\n", encoding="utf-8")
    summary = {
        "run_id": run_id, "stage": stage, "bundles": len(bundles),
        "candidates": len(all_candidates), "trades": len(all_trades),
        "selected": [row["variant_id"] for row in selected], "report": str(report),
    }
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("development", "validation", "known_audit"), required=True)
    parser.add_argument("--config", default=None)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--symbols", nargs="*")
    parser.add_argument("--frozen", default=None)
    args = parser.parse_args()
    run(args.stage, args.config, args.workers, args.symbols, args.frozen)


if __name__ == "__main__":
    main()
