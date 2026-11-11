"""Shared, side-effect-limited helpers for independent shadow strategies.

The helpers in this module do not know about signal generation or routing.  They
provide deterministic confirmed-close execution, Model-F style protection,
realistic USD cost accounting, additive SQLite migration, and clean-forward
evaluation.  Strategy modules remain responsible for point-in-time eligibility.
"""
from __future__ import annotations

import json
import math
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
import yaml

from src.execution import profit_protection as pp
from src.execution.fees import trade_costs
from src.execution.position_sizing import size_position


MIN_REVIEW_CLOSED = 30
MIN_REVIEW_DAYS = 28.0
MIN_REVIEW_PF = 1.25


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_dt(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        out = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return out.replace(tzinfo=timezone.utc) if out.tzinfo is None else out.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def load_yaml_block(path: Path, key: str, defaults: dict[str, Any]) -> dict[str, Any]:
    cfg = dict(defaults)
    if path.exists():
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            block = raw.get(key) or {}
            if isinstance(block, dict):
                cfg.update(block)
        except Exception:
            pass
    return cfg


def ensure_columns(conn: sqlite3.Connection, table: str, columns: dict[str, str]) -> None:
    """Idempotently add nullable/defaulted columns without rebuilding a table."""
    existing = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    for name, ddl in columns.items():
        if name not in existing:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}")


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone())


def preserve_first_observation(conn: sqlite3.Connection, table: str, rows: list[dict[str, Any]]) -> None:
    """Keep first-seen evidence fields stable while an open outcome matures."""
    if not rows or not table_exists(conn, table):
        return
    existing = {
        str(row[0]): row[1:]
        for row in conn.execute(
            f"SELECT candidate_id,generated_at,window,latency_seconds FROM {table}"
        ).fetchall()
    }
    for row in rows:
        prior = existing.get(str(row.get("candidate_id")))
        if prior is None:
            continue
        row["generated_at"], row["window"], row["latency_seconds"] = prior


def normalize_frame(frame: Any, *, as_of: datetime | None = None) -> pd.DataFrame:
    if frame is None or getattr(frame, "empty", True):
        return pd.DataFrame()
    out = frame.copy()
    out.columns = [str(c).lower() for c in out.columns]
    if "timestamp" not in out.columns:
        return pd.DataFrame()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    out = out.dropna(subset=["timestamp"]).sort_values("timestamp")
    if as_of is not None:
        cutoff = pd.Timestamp(as_of)
        cutoff = cutoff.tz_localize("UTC") if cutoff.tzinfo is None else cutoff.tz_convert("UTC")
        out = out[out["timestamp"] <= cutoff]
    return out.reset_index(drop=True)


def profit_factor(values: Iterable[float]) -> float | None:
    vals = [float(v) for v in values]
    gains = sum(v for v in vals if v > 0)
    losses = abs(sum(v for v in vals if v < 0))
    if not vals:
        return None
    if losses == 0:
        return float("inf") if gains > 0 else 0.0
    return gains / losses


def max_drawdown(values: Iterable[float]) -> float:
    peak = equity = drawdown = 0.0
    for value in values:
        equity += float(value)
        peak = max(peak, equity)
        drawdown = max(drawdown, peak - equity)
    return round(drawdown, 4)


@dataclass
class ConfirmedCloseResult:
    status: str
    close_reason: str | None = None
    entry_price: float | None = None
    exit_price: float | None = None
    exit_ts: str | None = None
    net_r: float | None = None
    gross_pnl_usd: float | None = None
    net_pnl_usd: float | None = None
    fees_usd: float = 0.0
    slippage_usd: float = 0.0
    funding_usd: float = 0.0
    funding_source: str = "not_applicable"
    funding_estimated: bool = False
    funding_event_count: int = 0
    risk_usd: float | None = None
    mfe_r: float | None = None
    mae_r: float | None = None
    protection_armed: bool = False
    lock_armed: bool = False
    highest_tp_touched: int = 0
    bars_held: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _bar_value(row: Any, name: str) -> float | None:
    try:
        value = row.get(name) if hasattr(row, "get") else row[name]
        return None if value is None or pd.isna(value) else float(value)
    except (TypeError, ValueError, KeyError):
        return None


def simulate_confirmed_close_entry(
    *,
    direction: str,
    entry: float,
    stop: float,
    tp1: float,
    tp2: float,
    tp3: float,
    future_candles: Any,
    symbol: str,
    fee_profile: str,
    funding_rate_8h: float | None = None,
    funding_intervals: float = 0.0,
    funding_events: list[dict[str, Any]] | None = None,
    entry_at: datetime | None = None,
    bar_minutes: int = 0,
    force_close: bool = True,
    equity_usd: float = pp.EQUITY_USD,
    risk_pct: float = pp.RISK_PCT,
) -> ConfirmedCloseResult:
    """Enter exactly at a known closed-candle price and walk only later bars.

    Protection is chronological and conservative: a stop active at the start of
    a candle is honoured before a protection level armed by that candle.  Model-F
    thresholds and partial weights are imported from the authoritative paper
    implementation.  A forced time exit realizes the remaining position at the
    final close instead of incorrectly assigning a flat 0R expiry.
    """
    long = str(direction).lower() != "short"
    entry, stop = float(entry), float(stop)
    risk = abs(entry - stop)
    if risk <= 0 or (long and stop >= entry) or (not long and stop <= entry):
        return ConfirmedCloseResult(status="skipped", close_reason="invalid_geometry")
    frame = normalize_frame(future_candles)
    if frame.empty:
        return ConfirmedCloseResult(status="open", close_reason="awaiting_future_bars", entry_price=entry)

    targets = [float(tp1), float(tp2), float(tp3)]
    target_r = [abs(t - entry) / risk for t in targets]
    remaining = 1.0
    realized_r = 0.0
    highest = 0
    mfe = 0.0
    mae = 0.0
    protection_armed = False
    lock_armed = False
    close_reason = None
    final_exit = None
    final_exit_ts: datetime | None = None
    bars_held = 0

    for _, row in frame.iterrows():
        high, low, close = (_bar_value(row, k) for k in ("high", "low", "close"))
        if high is None or low is None:
            continue
        bars_held += 1
        row_ts = parse_dt(row.get("timestamp")) if hasattr(row, "get") else None
        row_close_ts = row_ts + timedelta(minutes=bar_minutes) if row_ts else None
        active_stop_r = pp.LOCK_LEVEL_R if lock_armed else (0.0 if protection_armed else -1.0)
        active_stop = entry + active_stop_r * risk if long else entry - active_stop_r * risk
        stop_touched = low <= active_stop if long else high >= active_stop
        if stop_touched:
            realized_r += remaining * active_stop_r
            final_exit = active_stop
            final_exit_ts = row_close_ts
            close_reason = ("profit_lock_stop" if lock_armed else
                            "breakeven_stop" if protection_armed else "original_stop")
            remaining = 0.0
            break

        favorable = high - entry if long else entry - low
        adverse = entry - low if long else high - entry
        mfe = max(mfe, favorable / risk)
        mae = min(mae, -(adverse / risk))
        for idx, target in enumerate(targets, start=1):
            if idx <= highest:
                continue
            touched = high >= target if long else low <= target
            if not touched:
                break
            fraction = min(float(pp.PARTIALS[idx]), remaining)
            realized_r += fraction * target_r[idx - 1]
            remaining -= fraction
            highest = idx
            final_exit = target
            final_exit_ts = row_close_ts
        if mfe >= pp.ARM_BE_AT_R:
            protection_armed = True
        if mfe >= pp.LOCK_AT_R:
            lock_armed = True
        if remaining <= 1e-9:
            close_reason = "tp3_runner"
            remaining = 0.0
            break

    if remaining > 1e-9:
        if not force_close:
            return ConfirmedCloseResult(
                status="open", close_reason="still_open", entry_price=entry,
                net_r=round(realized_r, 4), mfe_r=round(mfe, 4), mae_r=round(mae, 4),
                protection_armed=protection_armed, lock_armed=lock_armed,
                highest_tp_touched=highest, bars_held=bars_held,
            )
        last_close = _bar_value(frame.iloc[-1], "close")
        if last_close is None:
            return ConfirmedCloseResult(status="open", close_reason="missing_forced_close", entry_price=entry)
        close_r = ((last_close - entry) / risk) if long else ((entry - last_close) / risk)
        realized_r += remaining * close_r
        final_exit = last_close
        last_ts = parse_dt(frame.iloc[-1].get("timestamp"))
        final_exit_ts = last_ts + timedelta(minutes=bar_minutes) if last_ts else None
        close_reason = "time_exit"

    size = size_position(
        equity_usdt=equity_usd, entry_price=entry, stop_price=stop,
        direction=direction, risk_pct=risk_pct, max_leverage=pp.MAX_LEV,
    )
    risk_usd = float(size.actual_risk_usdt)
    gross = realized_r * risk_usd
    exit_price = float(final_exit if final_exit is not None else entry)
    funding = 0.0
    funding_source = "not_applicable"
    funding_estimated = False
    funding_event_count = 0
    actual_rates = []
    if entry_at is not None and final_exit_ts is not None:
        for event in funding_events or []:
            event_at = parse_dt(event.get("event_at"))
            received = parse_dt(event.get("received_at"))
            rate = event.get("funding_rate_8h", event.get("funding_rate"))
            try:
                rate = float(rate)
            except (TypeError, ValueError):
                continue
            if event_at is not None and entry_at < event_at <= final_exit_ts \
                    and (received is None or received <= final_exit_ts):
                actual_rates.append(rate)
    if actual_rates:
        side = 1.0 if long else -1.0
        funding = float(size.notional_usdt) * sum(actual_rates) * side
        funding_source = "actual_funding_events"
        funding_event_count = len(actual_rates)
    elif funding_rate_8h is not None and funding_intervals:
        side = 1.0 if long else -1.0
        funding = float(size.notional_usdt) * float(funding_rate_8h) * float(funding_intervals) * side
        funding_source = "mode_interval_fallback"
        funding_estimated = True
    slices = [(pp.PARTIALS[i], "maker") for i in range(1, highest + 1)]
    if sum(x[0] for x in slices) < 1.0:
        slices.append((round(1.0 - sum(x[0] for x in slices), 4), "taker"))
    costs = trade_costs(
        notional_usdt=float(size.notional_usdt), exit_notional_usdt=float(size.qty) * exit_price,
        symbol=symbol, fee_profile=fee_profile, entry_order_type="taker", exit_order_type="taker",
        funding_usdt=funding, exit_slices=slices,
    )
    return ConfirmedCloseResult(
        status="closed", close_reason=close_reason, entry_price=round(entry, 8),
        exit_price=round(exit_price, 8), exit_ts=final_exit_ts.isoformat() if final_exit_ts else None,
        net_r=round(realized_r, 4),
        gross_pnl_usd=round(gross, 4), net_pnl_usd=round(gross - costs.total_cost_usdt, 4),
        fees_usd=costs.fee_usdt, slippage_usd=costs.slippage_usdt,
        funding_usd=costs.funding_usdt, funding_source=funding_source,
        funding_estimated=funding_estimated, funding_event_count=funding_event_count,
        risk_usd=round(risk_usd, 4),
        mfe_r=round(mfe, 4), mae_r=round(mae, 4), protection_armed=protection_armed,
        lock_armed=lock_armed, highest_tp_touched=highest, bars_held=bars_held,
    )


def clean_forward_summary(
    rows: list[dict[str, Any]], *, activated_at: str | None, now: datetime,
    min_closed: int = MIN_REVIEW_CLOSED, min_days: float = MIN_REVIEW_DAYS,
    min_pf: float = MIN_REVIEW_PF, max_review_drawdown_usd: float = 250.0,
    paired_delta_usd: float | None = None, paired_control_available: bool = False,
) -> dict[str, Any]:
    clean = [r for r in rows if r.get("window") == "forward_post_activation"
             and int(r.get("is_clean_for_edge") or 0) == 1]
    closed = [r for r in clean if r.get("outcome_status") == "closed"
              and r.get("net_pnl_usd") is not None]
    pnl = [float(r["net_pnl_usd"]) for r in sorted(closed, key=lambda x: str(x.get("entry_ts") or ""))]
    pf = profit_factor(pnl)
    activation = parse_dt(activated_at)
    days = max(0.0, (now - activation).total_seconds() / 86400.0) if activation else 0.0
    drawdown = max_drawdown(pnl)
    if len(closed) < min_closed:
        verdict = "INSUFFICIENT_CLEAN_SAMPLE"
    elif days < min_days:
        verdict = "ACCUMULATING_FORWARD_DAYS"
    elif (sum(pnl) <= 0 or pf is None or pf < min_pf
          or drawdown > float(max_review_drawdown_usd)):
        verdict = "KEEP_SHADOW"
    elif paired_control_available and (paired_delta_usd is None or paired_delta_usd <= 0):
        verdict = "KEEP_SHADOW"
    else:
        verdict = "REVIEW_ONLY"
    return {
        "forward_rows": len([r for r in rows if r.get("window") == "forward_post_activation"]),
        "clean_rows": len(clean), "clean_closed": len(closed),
        "dirty_rows": len([r for r in rows if r.get("window") == "forward_post_activation"
                            and int(r.get("is_clean_for_edge") or 0) == 0]),
        "net_pnl_usd": round(sum(pnl), 4),
        "net_r": round(sum(float(r.get("net_r") or 0.0) for r in closed), 4),
        "fees_usd": round(sum(float(r.get("fees_usd") or 0.0) for r in closed), 4),
        "slippage_usd": round(sum(float(r.get("slippage_usd") or 0.0) for r in closed), 4),
        "funding_usd": round(sum(float(r.get("funding_usd") or 0.0) for r in closed), 4),
        "profit_factor": pf, "winrate": (sum(v > 0 for v in pnl) / len(pnl) if pnl else None),
        "max_drawdown_usd": drawdown, "forward_days": round(days, 3),
        "paired_control_available": paired_control_available,
        "paired_delta_usd": paired_delta_usd,
        "review_checks": {
            "min_clean_closed": len(closed) >= min_closed,
            "min_forward_days": days >= min_days,
            "positive_net_pnl_usd": sum(pnl) > 0,
            "profit_factor": pf is not None and pf >= min_pf,
            "drawdown_within_limit": drawdown <= float(max_review_drawdown_usd),
            "paired_delta_positive_if_available": (not paired_control_available
                                                     or (paired_delta_usd is not None
                                                         and paired_delta_usd > 0)),
        },
        "verdict": verdict,
    }


def strategy_diagnostics(rows: list[dict[str, Any]], *, group_keys: Iterable[str]) -> dict[str, Any]:
    """Operational and contextual metrics, kept separate from promotion evidence."""
    forward = [r for r in rows if r.get("window") == "forward_post_activation"]
    eligible = [r for r in forward if r.get("eligibility_status") == "eligible"]
    entered = [r for r in eligible if r.get("entry_ts")]
    closed = [r for r in eligible if r.get("outcome_status") == "closed"]
    skipped = [r for r in forward if r.get("outcome_status") == "skipped"]
    unresolved = [r for r in forward if r.get("outcome_status") in {"open", "unresolved"}]
    missed = [r for r in forward if r.get("outcome_status") == "missed"]
    stale = [r for r in forward if "STALE" in str(r.get("rejection_reason") or "")]
    latency = [float(r["latency_seconds"]) for r in eligible if r.get("latency_seconds") is not None]
    grouped: dict[str, dict[str, dict[str, float]]] = {}
    for key in group_keys:
        blocks: dict[str, dict[str, float]] = {}
        for row in forward:
            label = str(row.get(key) or "unknown")
            block = blocks.setdefault(label, {"rows": 0, "eligible": 0, "clean_closed": 0,
                                               "net_pnl_usd": 0.0})
            block["rows"] += 1
            block["eligible"] += int(row.get("eligibility_status") == "eligible")
            if row.get("outcome_status") == "closed" and int(row.get("is_clean_for_edge") or 0) == 1:
                block["clean_closed"] += 1
                block["net_pnl_usd"] += float(row.get("net_pnl_usd") or 0.0)
        grouped[key] = blocks
    executed_net = round(sum(float(r.get("net_pnl_usd") or 0.0) for r in closed), 4)
    return {
        "historical_backfill_rows": sum(r.get("window") == "historical_backfill" for r in rows),
        "forward_rows": len(forward), "eligible": len(eligible), "entered": len(entered),
        "closed": len(closed), "skipped": len(skipped), "unresolved_open": len(unresolved),
        "fill_rate": (len(entered) / len(eligible) if eligible else None),
        "missed_entry_rate": (len(missed) / (len(entered) + len(missed))
                              if entered or missed else None),
        "dirty_share": (sum(int(r.get("is_clean_for_edge") or 0) == 0 for r in forward) / len(forward)
                        if forward else None),
        "stale_data_share": (len(stale) / len(forward) if forward else None),
        "avg_latency_seconds": (sum(latency) / len(latency) if latency else None),
        "executed_only_net_pnl_usd": executed_net,
        "with_skips_net_pnl_usd": executed_net,  # skips are explicitly zero, never treated as executions
        "paired_control_status": "UNAVAILABLE_NO_IDENTICAL_EXECUTED_CONTROL",
        "groups": grouped,
    }


def diagnostics_markdown(diagnostics: dict[str, Any]) -> list[str]:
    def pct(value: Any) -> str:
        return "-" if value is None else f"{float(value) * 100:.1f}%"

    def num(value: Any) -> str:
        return "-" if value is None else f"{float(value):.1f}"

    lines = [
        "## Execution diagnostics", "",
        "| backfill | forward | eligible | entered | closed | skipped | open | fill | missed | dirty | stale | avg latency s |",
        "|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|",
        f"| {diagnostics.get('historical_backfill_rows', 0)} | {diagnostics.get('forward_rows', 0)} | "
        f"{diagnostics.get('eligible', 0)} | {diagnostics.get('entered', 0)} | "
        f"{diagnostics.get('closed', 0)} | {diagnostics.get('skipped', 0)} | "
        f"{diagnostics.get('unresolved_open', 0)} | {pct(diagnostics.get('fill_rate'))} | "
        f"{pct(diagnostics.get('missed_entry_rate'))} | {pct(diagnostics.get('dirty_share'))} | "
        f"{pct(diagnostics.get('stale_data_share'))} | {num(diagnostics.get('avg_latency_seconds'))} |",
        "",
        f"Executed-only net USD: `{diagnostics.get('executed_only_net_pnl_usd', 0.0)}`; "
        f"with-skips net USD: `{diagnostics.get('with_skips_net_pnl_usd', 0.0)}`.",
        f"Paired control: `{diagnostics.get('paired_control_status', 'UNAVAILABLE')}`.",
    ]
    for key, blocks in (diagnostics.get("groups") or {}).items():
        lines.extend(["", f"### By {key}", "", "| value | rows | eligible | clean closed | net USD |",
                      "|---|--:|--:|--:|--:|"])
        for label, block in sorted(blocks.items()):
            lines.append(f"| {label} | {block['rows']} | {block['eligible']} | "
                         f"{block['clean_closed']} | {block['net_pnl_usd']:.2f} |")
    return lines


def json_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str, ensure_ascii=True)


__all__ = [
    "ConfirmedCloseResult", "MIN_REVIEW_CLOSED", "MIN_REVIEW_DAYS", "MIN_REVIEW_PF",
    "clean_forward_summary", "diagnostics_markdown", "ensure_columns", "json_text", "load_yaml_block", "max_drawdown",
    "normalize_frame", "parse_dt", "preserve_first_observation", "profit_factor",
    "simulate_confirmed_close_entry", "strategy_diagnostics",
    "table_exists", "utc_now",
]
