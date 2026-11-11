from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


VERSION = "initial_stop_contract_v1"


def _f(value: Any, default: float | None = None) -> float | None:
    try:
        return default if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return default


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def entry_anchor(direction: str, entry_low: Any, entry_high: Any, fallback: Any = None) -> float | None:
    """Return the strategy-preferred entry price for stop/risk attribution."""
    low = _f(entry_low)
    high = _f(entry_high)
    fb = _f(fallback)
    direction = str(direction or "").lower()
    if direction == "long":
        return high if high is not None else low if low is not None else fb
    if direction == "short":
        return low if low is not None else high if high is not None else fb
    return fb


def _distance_pct(entry_price: float | None, stop_price: float | None) -> float | None:
    if entry_price is None or stop_price is None or entry_price <= 0:
        return None
    return abs(entry_price - stop_price) / entry_price


def _directional_geometry_ok(direction: str, entry_price: float | None, stop_price: float | None) -> bool:
    if entry_price is None or stop_price is None:
        return False
    direction = str(direction or "").lower()
    if direction == "long":
        return stop_price < entry_price
    if direction == "short":
        return stop_price > entry_price
    return False


def stop_contract_label(contract: dict[str, Any] | None) -> str:
    if not isinstance(contract, dict) or not contract:
        return "stop provenance missing"
    if contract.get("label"):
        return str(contract["label"])
    source = str(contract.get("stop_source") or contract.get("source") or "unknown")
    model = str(contract.get("stop_model") or "")
    tf = str(contract.get("structure_timeframe") or "")
    level_kind = str(contract.get("structure_level_kind") or "")
    if source in {"support_resistance", "structure_level"}:
        side = level_kind or "structure"
        return f"{tf + ' ' if tf else ''}{side} + buffer".strip()
    if source == "stock_intraday_structure":
        side = level_kind or "stock structure"
        return f"{tf + ' ' if tf else ''}{side} + ATR buffer".strip()
    if source == "liquidity_sweep_extreme":
        side = level_kind or "sweep extreme"
        return f"{tf + ' ' if tf else ''}{side} + sweep buffer".strip()
    if source == "atr_fallback":
        return "ATR fallback stop"
    if source == "legacy_atr_stop":
        return "legacy 1 ATR stop"
    if source == "regime_reclaim_rebased_unit_pct":
        return "invest unit-percent stop"
    if model:
        return f"{source} / {model}"
    return source.replace("_", " ")


def is_structural_stop_contract(contract: dict[str, Any] | None) -> bool:
    if not isinstance(contract, dict):
        return False
    if contract.get("fallback_used"):
        return False
    source = str(contract.get("stop_source") or "").lower()
    model = str(contract.get("stop_model") or "").lower()
    structural_sources = {
        "support_resistance",
        "structure_level",
        "stock_intraday_structure",
        "liquidity_sweep_extreme",
        "vwap_reclaim_structure",
        "swing_low_high_structure",
    }
    if source in structural_sources:
        return True
    return "structural" in model or "structure" in model or "sweep" in model


def normalize_stop_contract(
    contract: dict[str, Any] | None,
    *,
    symbol: str,
    asset_class: str,
    mode: str,
    direction: str,
    entry_price: float | None,
    stop_price: float | None,
    source: str | None = None,
) -> dict[str, Any]:
    data = dict(contract or {})
    data.setdefault("version", VERSION)
    data["symbol"] = str(data.get("symbol") or symbol or "")
    data["asset_class"] = str(data.get("asset_class") or asset_class or "")
    data["mode"] = str(data.get("mode") or mode or "")
    data["direction"] = str(data.get("direction") or direction or "").lower()
    data["entry_price"] = _f(data.get("entry_price"), entry_price)
    data["stop_price"] = _f(data.get("stop_price"), stop_price)
    data.setdefault("stop_source", source or "legacy_unknown")
    data.setdefault("stop_model", "unknown")
    data.setdefault("fallback_used", str(data.get("stop_source") or "").startswith("legacy"))
    data.setdefault("warnings", [])
    data.setdefault("computed_at", _iso_now())
    data["stop_distance_pct"] = _distance_pct(data.get("entry_price"), data.get("stop_price"))
    data["geometry_valid"] = _directional_geometry_ok(data["direction"], data.get("entry_price"), data.get("stop_price"))
    data["label"] = stop_contract_label(data)
    return data


def build_initial_stop_contract(
    *,
    symbol: str,
    asset_class: str,
    mode: str,
    direction: str,
    entry_price: float | None,
    stop_price: float | None,
    setup: dict[str, Any] | None = None,
    payload: dict[str, Any] | None = None,
    source: str | None = None,
) -> dict[str, Any]:
    setup = setup or {}
    payload = payload or {}
    for candidate in (
        payload.get("initial_stop_contract"),
        payload.get("stop_contract"),
        setup.get("initial_stop_contract"),
        setup.get("stop_contract"),
    ):
        if isinstance(candidate, dict) and candidate:
            return normalize_stop_contract(
                candidate,
                symbol=symbol,
                asset_class=asset_class,
                mode=mode,
                direction=direction,
                entry_price=entry_price,
                stop_price=stop_price,
                source=source,
            )

    atr_value = _f(setup.get("atr") or setup.get("atr14"))
    support = _f(setup.get("support"))
    resistance = _f(setup.get("resistance"))
    direction_l = str(direction or "").lower()
    stop_source = str(setup.get("stop_source") or "")
    stop_model = str(setup.get("stop_model") or "")
    structure_level = None
    structure_kind = ""
    buffer_atr = _f(setup.get("stop_buffer_atr"))
    fallback_used = False

    if not stop_source:
        if asset_class in {"stocks", "stock_futures"}:
            stop_source = "legacy_atr_stop"
            stop_model = stop_model or "atr_distance_v1"
            fallback_used = True
        elif direction_l == "long" and support is not None and atr_value:
            expected = support - 0.15 * atr_value
            if stop_price is not None and abs(expected - stop_price) <= max(abs(stop_price) * 0.01, atr_value * 0.1):
                stop_source = "support_resistance"
                stop_model = "support_minus_atr_buffer_v1"
                structure_level = support
                structure_kind = "support"
                buffer_atr = 0.15
            else:
                stop_source = "atr_fallback"
                stop_model = "atr_distance_v1"
                fallback_used = True
        elif direction_l == "short" and resistance is not None and atr_value:
            expected = resistance + 0.15 * atr_value
            if stop_price is not None and abs(expected - stop_price) <= max(abs(stop_price) * 0.01, atr_value * 0.1):
                stop_source = "support_resistance"
                stop_model = "resistance_plus_atr_buffer_v1"
                structure_level = resistance
                structure_kind = "resistance"
                buffer_atr = 0.15
            else:
                stop_source = "atr_fallback"
                stop_model = "atr_distance_v1"
                fallback_used = True
        else:
            stop_source = "atr_fallback" if atr_value else "legacy_unknown"
            stop_model = "atr_distance_v1" if atr_value else "unknown"
            fallback_used = True

    contract = {
        "version": VERSION,
        "symbol": symbol,
        "asset_class": asset_class,
        "mode": mode,
        "direction": direction_l,
        "entry_price": entry_price,
        "stop_price": stop_price,
        "stop_source": stop_source,
        "stop_model": stop_model or "unknown",
        "structure_timeframe": setup.get("timeframe") or setup.get("structure_timeframe"),
        "structure_level": structure_level if structure_level is not None else _f(setup.get("structure_level")),
        "structure_level_kind": structure_kind or str(setup.get("structure_level_kind") or ""),
        "atr": atr_value,
        "buffer_atr": buffer_atr,
        "raw_stop_price": stop_price,
        "fallback_used": bool(fallback_used or str(stop_source).startswith("legacy")),
        "fallback_reason": "no_explicit_stop_contract" if fallback_used else "",
        "confidence": "medium" if not fallback_used else "low",
        "warnings": [],
        "computed_at": _iso_now(),
        "point_in_time_cutoff": setup.get("decision_at") or setup.get("computed_at"),
    }
    return normalize_stop_contract(
        contract,
        symbol=symbol,
        asset_class=asset_class,
        mode=mode,
        direction=direction,
        entry_price=entry_price,
        stop_price=stop_price,
        source=source,
    )


def stock_intraday_structural_stop_contract(
    *,
    symbol: str,
    direction: str,
    entry_price: float | None,
    exec_frame: Any,
    atr_value: float | None,
    vwap: float | None = None,
    timeframe: str = "15m",
    buffer_atr: float = 0.2,
    min_distance_atr: float = 0.6,
    max_distance_atr: float = 2.5,
) -> dict[str, Any]:
    direction_l = str(direction or "").lower()
    entry = _f(entry_price)
    atr_v = _f(atr_value)
    warnings: list[str] = []
    if entry is None or entry <= 0 or atr_v is None or atr_v <= 0 or direction_l not in {"long", "short"}:
        return normalize_stop_contract(
            {
                "stop_source": "legacy_atr_stop",
                "stop_model": "atr_distance_v1",
                "fallback_used": True,
                "fallback_reason": "missing_entry_or_atr",
                "warnings": ["cannot build structural stock stop"],
            },
            symbol=symbol,
            asset_class="stocks",
            mode="intraday",
            direction=direction_l,
            entry_price=entry,
            stop_price=None,
        )

    frame = exec_frame
    if frame is None or len(frame) < 3:
        fallback = entry - atr_v if direction_l == "long" else entry + atr_v
        return normalize_stop_contract(
            {
                "stop_source": "legacy_atr_stop",
                "stop_model": "atr_distance_v1",
                "fallback_used": True,
                "fallback_reason": "missing_exec_frame",
                "warnings": ["15m frame unavailable; structural stop not testable"],
            },
            symbol=symbol,
            asset_class="stocks",
            mode="intraday",
            direction=direction_l,
            entry_price=entry,
            stop_price=fallback,
        )

    lookback = frame.tail(20)
    levels: list[tuple[str, float]] = []
    try:
        if direction_l == "long":
            levels.append(("recent_swing_low", float(lookback["low"].min())))
            levels.append(("last_bar_low", float(lookback["low"].iloc[-1])))
            if vwap is not None and 0 < vwap < entry:
                levels.append(("vwap", float(vwap)))
            valid_levels = [(kind, value) for kind, value in levels if 0 < value < entry]
            level_kind, level = max(valid_levels, key=lambda item: item[1])
            raw_stop = level - buffer_atr * atr_v
            min_stop = entry - min_distance_atr * atr_v
            max_stop = entry - max_distance_atr * atr_v
            stop = min(raw_stop, min_stop)
            if stop < max_stop:
                warnings.append("structural stop wider than max_distance_atr; capped for research candidate")
                stop = max_stop
        else:
            levels.append(("recent_swing_high", float(lookback["high"].max())))
            levels.append(("last_bar_high", float(lookback["high"].iloc[-1])))
            if vwap is not None and vwap > entry:
                levels.append(("vwap", float(vwap)))
            valid_levels = [(kind, value) for kind, value in levels if value > entry]
            level_kind, level = min(valid_levels, key=lambda item: item[1])
            raw_stop = level + buffer_atr * atr_v
            min_stop = entry + min_distance_atr * atr_v
            max_stop = entry + max_distance_atr * atr_v
            stop = max(raw_stop, min_stop)
            if stop > max_stop:
                warnings.append("structural stop wider than max_distance_atr; capped for research candidate")
                stop = max_stop
    except (ValueError, KeyError, TypeError):
        fallback = entry - atr_v if direction_l == "long" else entry + atr_v
        return normalize_stop_contract(
            {
                "stop_source": "legacy_atr_stop",
                "stop_model": "atr_distance_v1",
                "fallback_used": True,
                "fallback_reason": "no_valid_structure_level",
                "warnings": ["valid stock structure level not found"],
            },
            symbol=symbol,
            asset_class="stocks",
            mode="intraday",
            direction=direction_l,
            entry_price=entry,
            stop_price=fallback,
        )

    return normalize_stop_contract(
        {
            "stop_source": "stock_intraday_structure",
            "stop_model": "nearest_15m_level_vwap_buffer_v1",
            "structure_timeframe": timeframe,
            "structure_level": level,
            "structure_level_kind": level_kind,
            "atr": atr_v,
            "buffer_atr": buffer_atr,
            "raw_stop_price": raw_stop,
            "fallback_used": False,
            "confidence": "medium",
            "warnings": warnings,
        },
        symbol=symbol,
        asset_class="stocks",
        mode="intraday",
        direction=direction_l,
        entry_price=entry,
        stop_price=stop,
    )


def ensure_initial_stop_plan_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS signal_initial_stop_plan (
            signal_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            symbol TEXT,
            asset_class TEXT,
            mode TEXT,
            direction TEXT,
            entry_price REAL,
            stop_price REAL,
            stop_source TEXT,
            stop_model TEXT,
            structure_timeframe TEXT,
            structure_level REAL,
            stop_distance_pct REAL,
            fallback_used INTEGER DEFAULT 0,
            contract_json TEXT NOT NULL,
            source TEXT
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_signal_initial_stop_plan_source "
        "ON signal_initial_stop_plan(asset_class, mode, stop_source)"
    )


def upsert_signal_initial_stop_plan(
    conn: sqlite3.Connection,
    *,
    signal_id: str,
    contract: dict[str, Any],
    source: str = "registry",
) -> None:
    ensure_initial_stop_plan_table(conn)
    now = _iso_now()
    conn.execute(
        """
        INSERT INTO signal_initial_stop_plan(
            signal_id, created_at, updated_at, symbol, asset_class, mode, direction,
            entry_price, stop_price, stop_source, stop_model, structure_timeframe,
            structure_level, stop_distance_pct, fallback_used, contract_json, source
        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(signal_id) DO UPDATE SET
            updated_at=excluded.updated_at,
            symbol=excluded.symbol,
            asset_class=excluded.asset_class,
            mode=excluded.mode,
            direction=excluded.direction,
            entry_price=excluded.entry_price,
            stop_price=excluded.stop_price,
            stop_source=excluded.stop_source,
            stop_model=excluded.stop_model,
            structure_timeframe=excluded.structure_timeframe,
            structure_level=excluded.structure_level,
            stop_distance_pct=excluded.stop_distance_pct,
            fallback_used=excluded.fallback_used,
            contract_json=excluded.contract_json,
            source=excluded.source
        """,
        (
            signal_id,
            now,
            now,
            contract.get("symbol"),
            contract.get("asset_class"),
            contract.get("mode"),
            contract.get("direction"),
            _f(contract.get("entry_price")),
            _f(contract.get("stop_price")),
            contract.get("stop_source"),
            contract.get("stop_model"),
            contract.get("structure_timeframe"),
            _f(contract.get("structure_level")),
            _f(contract.get("stop_distance_pct")),
            1 if contract.get("fallback_used") else 0,
            json.dumps(contract, ensure_ascii=False, sort_keys=True),
            source,
        ),
    )


def backfill_signal_initial_stop_plans(
    db_path: str | Path,
    *,
    days: int = 14,
    limit: int = 5000,
) -> dict[str, Any]:
    path = Path(db_path)
    since = (datetime.now(timezone.utc) - timedelta(days=max(1, int(days)))).isoformat()
    inserted = 0
    by_source: dict[str, int] = {}
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        ensure_initial_stop_plan_table(conn)
        rows = conn.execute(
            """
            SELECT signal_id, symbol, asset_class, mode, direction, entry_low,
                   entry_high, entry_trigger, suggested_entry, stop_loss,
                   invalidation, raw_idea_json, created_at
            FROM proposed_signals
            WHERE created_at >= ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (since, int(limit)),
        ).fetchall()
        for row in rows:
            try:
                raw = json.loads(row["raw_idea_json"] or "{}")
                if not isinstance(raw, dict):
                    raw = {}
            except Exception:
                raw = {}
            setup = raw.get("raw_setup") or raw.get("setup") or {}
            if not isinstance(setup, dict):
                setup = {}
            direction = str(row["direction"] or "").lower()
            entry = entry_anchor(
                direction,
                row["entry_low"],
                row["entry_high"],
                row["entry_trigger"] or row["suggested_entry"],
            )
            stop = _f(row["stop_loss"] or row["invalidation"])
            contract = build_initial_stop_contract(
                symbol=str(row["symbol"] or ""),
                asset_class=str(row["asset_class"] or "crypto"),
                mode=str(row["mode"] or ""),
                direction=direction,
                entry_price=entry,
                stop_price=stop,
                setup=setup,
                payload=raw,
            )
            upsert_signal_initial_stop_plan(
                conn,
                signal_id=str(row["signal_id"]),
                contract=contract,
                source="historical_backfill",
            )
            inserted += 1
            source = str(contract.get("stop_source") or "unknown")
            by_source[source] = by_source.get(source, 0) + 1
    return {
        "db_path": str(path),
        "days": int(days),
        "processed": inserted,
        "by_stop_source": by_source,
    }


def _infer_live_decision_stop_source(row: sqlite3.Row) -> str:
    try:
        decision = json.loads(row["decision_json"] or "{}")
        if not isinstance(decision, dict):
            return "missing"
    except Exception:
        return "missing"
    contract = decision.get("stop_contract")
    if isinstance(contract, dict) and contract.get("stop_source"):
        return str(contract.get("stop_source"))
    mode = str(decision.get("mode") or row["mode"] or "").lower()
    asset = str(decision.get("asset_class") or "").lower()
    if asset == "stock_futures":
        return "legacy_atr_stop"
    if mode == "liquidity_sweep":
        return "liquidity_sweep_extreme"
    if mode == "invest":
        return "regime_reclaim_rebased_unit_pct"
    return "missing"


def audit_stop_contracts(
    db_path: str | Path,
    *,
    days: int = 14,
    write_report: bool = True,
    backfill: bool = False,
) -> dict[str, Any]:
    path = Path(db_path)
    backfill_result = None
    if backfill:
        backfill_result = backfill_signal_initial_stop_plans(path, days=days)
    since = (datetime.now(timezone.utc) - timedelta(days=max(1, int(days)))).isoformat()
    summary: dict[str, Any] = {"db_path": str(path), "days": int(days), "since": since}
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        ensure_initial_stop_plan_table(conn)
        rows = conn.execute(
            """
            SELECT COALESCE(p.asset_class, c.asset_class) AS asset_class,
                   COALESCE(p.mode, c.mode) AS mode,
                   COALESCE(c.stop_source, 'missing') AS stop_source,
                   COUNT(*) AS n
            FROM proposed_signals p
            LEFT JOIN signal_initial_stop_plan c ON c.signal_id = p.signal_id
            WHERE p.created_at >= ?
            GROUP BY 1, 2, 3
            ORDER BY n DESC
            """,
            (since,),
        ).fetchall()
        live_raw = conn.execute(
            """
            SELECT mode, decision_json
            FROM mexc_canary_decisions
            WHERE captured_at >= ?
            """,
            (since,),
        ).fetchall()
    live_counts: dict[tuple[str, str, str], int] = {}
    for row in live_raw:
        try:
            decision = json.loads(row["decision_json"] or "{}")
            if not isinstance(decision, dict):
                decision = {}
        except Exception:
            decision = {}
        key = (
            str(decision.get("asset_class") or ""),
            str(decision.get("mode") or row["mode"] or ""),
            _infer_live_decision_stop_source(row),
        )
        live_counts[key] = live_counts.get(key, 0) + 1
    live_rows = [
        {"asset_class": key[0], "mode": key[1], "stop_source": key[2], "n": value}
        for key, value in sorted(live_counts.items(), key=lambda item: item[1], reverse=True)
    ]
    summary["proposed_by_stop_source"] = [dict(row) for row in rows]
    summary["live_by_stop_source"] = live_rows
    if backfill_result is not None:
        summary["backfill"] = backfill_result
    summary["report_path"] = None
    if write_report:
        report_dir = path.parent.parent / "reports" if path.parent.name == "data" else Path("reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "INITIAL_STOP_CONTRACT_AUDIT_latest.md"
        lines = [
            "# Initial Stop Contract Audit",
            "",
            f"- DB: `{path}`",
            f"- Window: last {int(days)} days",
            "",
            "## Proposed Signals",
            "",
        ]
        if rows:
            lines += ["| Asset | Mode | Stop source | Count |", "|---|---|---|---|"]
            lines += [
                f"| {row['asset_class'] or ''} | {row['mode'] or ''} | {row['stop_source'] or ''} | {row['n']} |"
                for row in rows
            ]
        else:
            lines.append("No proposed signals in window.")
        lines += ["", "## Live Decisions", ""]
        if live_rows:
            lines += ["| Asset | Mode | Stop source | Count |", "|---|---|---|---|"]
            lines += [
                f"| {row['asset_class'] or ''} | {row['mode'] or ''} | {row['stop_source'] or ''} | {row['n']} |"
                for row in live_rows
            ]
        else:
            lines.append("No live decisions in window.")
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        summary["report_path"] = str(report_path)
    return summary
