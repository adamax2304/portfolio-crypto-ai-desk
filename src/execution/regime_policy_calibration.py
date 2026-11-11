"""Leakage-safe read-model calibration for market-regime filters.

This module evaluates *frozen point-in-time* Paper decisions against their later
Paper outcomes.  It never scores, routes, alerts, opens orders, or mutates the
trading ledger.  The output answers a narrow operational question: which regime
states deserve a full-size, half-size, or blocked policy for each existing lane?

Only ``forward_postfreeze`` rows can support a runtime recommendation.  Older
or unresolved rows are kept out of that conclusion.  The forward cohort is split
chronologically: the oldest two thirds are the selection set and the newest third
is the validation set, so a rule cannot be selected on the outcome it is judged
against.
"""
from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


VERSION = "regime_policy_calibration_v1"
FORWARD = "forward_postfreeze"
VALID_EXECUTION = "valid"
RESOLVED_OUTCOMES = ("win", "loss", "breakeven")


@dataclass(frozen=True)
class EvidenceRow:
    asset_class: str
    mode: str
    direction: str
    regime: str
    raw_regime: str
    decided_at: datetime
    evidence_class: str
    net_r: float
    net_usd: float | None


def _parse_time(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def _number(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _normalized_label(value: Any) -> str:
    return str(value or "unknown").strip().lower().replace("-", "_").replace(" ", "_")


def crypto_regime(snapshot: dict[str, Any]) -> str:
    """Return a stable regime bucket from data available at the decision time.

    An explicit ``risk_off``/``chop`` label wins because that is what the
    production policy consumed.  An ``unknown`` label with healthy BTC returns
    is deliberately reclassified from price data; unknown is not a bearish vote.
    """
    label = _normalized_label(snapshot.get("btc_regime_state"))
    if label in {"risk_off", "btc_risk_off", "bearish", "downtrend", "weak"}:
        return "risk_off"
    if label in {"chop", "range", "ranging", "range/chop"}:
        return "chop"
    if label in {"risk_on", "bullish", "uptrend", "trend"}:
        return "risk_on"

    r15 = _number(snapshot.get("btc_15m_return"))
    r1h = _number(snapshot.get("btc_1h_return"))
    slope = _normalized_label(snapshot.get("btc_ema_slope_state"))
    if r15 is None or r1h is None:
        return "unknown"
    if r1h <= -0.20 and slope == "down" and r15 <= 0.10:
        return "risk_off"
    if r1h >= 0.20 and slope == "up" and r15 >= -0.10:
        return "risk_on"
    if slope == "flat" and abs(r1h) < 0.20 and abs(r15) < 0.12:
        return "chop"
    return "neutral"


def stocks_regime(value: Any) -> str:
    """Normalize StocksMarketRegimeAgent's decision-time vocabulary."""
    label = _normalized_label(value)
    if label in {"risk_on", "bullish", "uptrend", "trend"} or "bull" in label:
        return "risk_on"
    if label in {"risk_off", "bearish", "downtrend"} or "bear" in label:
        return "risk_off"
    if label in {"chop", "range", "ranging", "range/chop"} or "chop" in label or "range" in label:
        return "chop"
    if label in {"", "unknown"}:
        return "unknown"
    return "neutral"


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone())


def _ledger_usd_map(conn: sqlite3.Connection, fee_profile: str) -> dict[str, float]:
    if not _table_exists(conn, "paper_portfolio_ledger"):
        return {}
    rows = conn.execute(
        "SELECT l.signal_id,l.net_pnl_usdt FROM paper_portfolio_ledger l "
        "JOIN (SELECT signal_id,MAX(rowid) AS row_id FROM paper_portfolio_ledger "
        "      WHERE event_type='exit' AND fee_profile=? GROUP BY signal_id) x "
        "ON x.signal_id=l.signal_id AND x.row_id=l.rowid",
        (fee_profile,),
    ).fetchall()
    result: dict[str, float] = {}
    for signal_id, raw_value in rows:
        value = _number(raw_value)
        if value is not None:
            result[str(signal_id)] = value
    return result


def _decode(value: Any) -> dict[str, Any]:
    try:
        decoded = json.loads(value or "{}")
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}
    return decoded if isinstance(decoded, dict) else {}


def _load_crypto(conn: sqlite3.Connection) -> list[EvidenceRow]:
    required = ("crypto_quality_overlay_decision_snapshots", "proposed_signals", "paper_execution_outcomes")
    if not all(_table_exists(conn, table) for table in required):
        return []
    usd = _ledger_usd_map(conn, "bybit_non_vip_usdt_perp")
    rows = conn.execute(
        "SELECT s.signal_id,s.decision_json,s.decided_at,p.mode,p.direction,"
        "o.paper_execution_r,o.evidence_class,o.execution_validity,o.paper_execution_outcome "
        "FROM crypto_quality_overlay_decision_snapshots s "
        "JOIN proposed_signals p ON p.signal_id=s.signal_id "
        "JOIN paper_execution_outcomes o ON o.signal_id=s.signal_id "
        "WHERE lower(COALESCE(p.asset_class,''))='crypto'"
    ).fetchall()
    out: list[EvidenceRow] = []
    for signal_id, raw_snapshot, decided, mode, direction, net_r, evidence, validity, outcome in rows:
        if str(validity or "") != VALID_EXECUTION or str(outcome or "") not in RESOLVED_OUTCOMES:
            continue
        timestamp = _parse_time(decided)
        value = _number(net_r)
        if timestamp is None or value is None:
            continue
        snapshot = _decode(raw_snapshot)
        raw_regime = _normalized_label(snapshot.get("btc_regime_state"))
        out.append(EvidenceRow(
            asset_class="crypto", mode=str(mode or "unknown").lower(), direction=str(direction or "unknown").lower(),
            regime=crypto_regime(snapshot), raw_regime=raw_regime, decided_at=timestamp,
            evidence_class=str(evidence or "unclassified"), net_r=value, net_usd=usd.get(str(signal_id)),
        ))
    return out


def _load_stocks(conn: sqlite3.Connection) -> list[EvidenceRow]:
    required = ("stocks_paper_decision_snapshots", "proposed_signals", "paper_execution_outcomes")
    if not all(_table_exists(conn, table) for table in required):
        return []
    usd = _ledger_usd_map(conn, "stock_etf_default")
    rows = conn.execute(
        "SELECT s.signal_id,s.snapshot_json,s.decision_at,s.captured_at,p.mode,p.direction,"
        "o.paper_execution_r,o.evidence_class,o.execution_validity,o.paper_execution_outcome "
        "FROM stocks_paper_decision_snapshots s "
        "JOIN proposed_signals p ON p.signal_id=s.signal_id "
        "JOIN paper_execution_outcomes o ON o.signal_id=s.signal_id "
        "WHERE lower(COALESCE(p.asset_class,'')) IN ('stocks','stock','equity')"
    ).fetchall()
    out: list[EvidenceRow] = []
    for signal_id, raw_snapshot, decision_at, captured_at, mode, direction, net_r, evidence, validity, outcome in rows:
        if str(validity or "") != VALID_EXECUTION or str(outcome or "") not in RESOLVED_OUTCOMES:
            continue
        timestamp = _parse_time(decision_at) or _parse_time(captured_at)
        value = _number(net_r)
        if timestamp is None or value is None:
            continue
        snapshot = _decode(raw_snapshot)
        raw_regime = _normalized_label(snapshot.get("market_regime"))
        out.append(EvidenceRow(
            asset_class="stocks", mode=str(mode or "unknown").lower(), direction=str(direction or "unknown").lower(),
            regime=stocks_regime(raw_regime), raw_regime=raw_regime, decided_at=timestamp,
            evidence_class=str(evidence or "unclassified"), net_r=value, net_usd=usd.get(str(signal_id)),
        ))
    return out


def _metrics(rows: Iterable[EvidenceRow]) -> dict[str, Any]:
    values = list(rows)
    r_values = [row.net_r for row in values]
    wins = [value for value in r_values if value > 0]
    losses = [value for value in r_values if value < 0]
    usd = [row.net_usd for row in values if row.net_usd is not None]
    gross_loss = abs(sum(losses))
    return {
        "n": len(values),
        "net_r": round(sum(r_values), 4),
        "avg_r": round(sum(r_values) / len(r_values), 4) if r_values else None,
        "winrate": round(len(wins) / len(r_values), 4) if r_values else None,
        "profit_factor": round(sum(wins) / gross_loss, 4) if gross_loss else (
            float("inf") if wins else None
        ),
        "net_usd": round(sum(usd), 4) if usd else None,
        "usd_coverage": len(usd),
    }


def _windowed_slices(rows: list[EvidenceRow], *, asset_class: str) -> tuple[datetime | None, dict[tuple[str, str, str, str], dict[str, Any]]]:
    forward = sorted(
        (row for row in rows if row.asset_class == asset_class and row.evidence_class == FORWARD),
        key=lambda row: row.decided_at,
    )
    cutoff = forward[int(len(forward) * 2 / 3)].decided_at if len(forward) >= 3 else None
    groups: dict[tuple[str, str, str, str], list[EvidenceRow]] = defaultdict(list)
    for row in forward:
        groups[(row.mode, row.direction, row.regime, "all")].append(row)
        if cutoff is not None:
            groups[(row.mode, row.direction, row.regime, "train" if row.decided_at < cutoff else "validation")].append(row)
    return cutoff, {key: _metrics(value) for key, value in groups.items()}


def _metric(slices: dict[tuple[str, str, str, str], dict[str, Any]], mode: str, direction: str,
            regime: str, window: str) -> dict[str, Any]:
    return dict(slices.get((mode, direction, regime, window)) or _metrics([]))


def _pf_positive(metrics: dict[str, Any]) -> bool:
    value = metrics.get("profit_factor")
    return value == float("inf") or (value is not None and value >= 1.10)


def _has_authoritative_usd(metrics: dict[str, Any], *, minimum_rows: int = 20,
                           minimum_coverage: float = 0.80) -> bool:
    n = int(metrics.get("n") or 0)
    coverage = int(metrics.get("usd_coverage") or 0)
    return n >= minimum_rows and coverage >= minimum_rows and coverage / n >= minimum_coverage


def _recommendations(crypto: dict[tuple[str, str, str, str], dict[str, Any]],
                     stocks: dict[tuple[str, str, str, str], dict[str, Any]]) -> list[dict[str, str]]:
    recs: list[dict[str, str]] = []
    risk_off_long = _metric(crypto, "intraday", "long", "risk_off", "all")
    recs.append({
        "scope": "crypto intraday long / risk_off",
        "policy": "KEEP_CURRENT_UNTIL_USD_EVIDENCE",
        "reason": ("R diagnostics are negative, so there is no case to relax the existing protective block; "
                   "USD coverage is still below the threshold for any policy rewrite."),
    })

    chop_train = _metric(crypto, "swing", "long", "chop", "train")
    chop_valid = _metric(crypto, "swing", "long", "chop", "validation")
    chop_all = _metric(crypto, "swing", "long", "chop", "all")
    if (_has_authoritative_usd(chop_all) and chop_train["n"] >= 10 and chop_valid["n"] >= 5
            and _pf_positive(chop_train) and _pf_positive(chop_valid)):
        recs.append({"scope": "crypto swing long / chop", "policy": "REVIEW_HALF_SIZE",
                     "reason": "Chronological R evidence and authoritative USD coverage both pass; operator review required."})
    else:
        recs.append({"scope": "crypto swing long / chop", "policy": "KEEP_CURRENT_INSUFFICIENT_USD_EVIDENCE",
                     "reason": "R-only splits are encouraging, but terminal USD coverage is not sufficient to change routing or size."})

    intraday_chop_valid = _metric(crypto, "intraday", "long", "chop", "validation")
    recs.append({
        "scope": "crypto intraday long / chop",
        "policy": "KEEP_CURRENT_INSUFFICIENT_USD_EVIDENCE",
        "reason": ("Validation is not consistently positive; keep BREAKOUT confirmation and do not upgrade chop to FULL_SIZE."
                   if not _pf_positive(intraday_chop_valid) else "Evidence is still too small to loosen breakout confirmation."),
    })
    recs.append({"scope": "crypto valid data + unknown label", "policy": "NO_FALSE_WEAK_DEMOTION",
                 "reason": "Unknown is a data-classification state, not affirmative risk-off evidence."})

    stocks_all = [metrics for (mode, _direction, _regime, window), metrics in stocks.items()
                  if mode == "intraday" and window == "all"]
    stock_r = sum(float(item.get("net_r") or 0.0) for item in stocks_all)
    stock_n = sum(int(item.get("n") or 0) for item in stocks_all)
    recs.append({
        "scope": "stocks intraday / all regimes",
        "policy": "KEEP_CURRENT_INSUFFICIENT_USD_EVIDENCE",
        "reason": ("Forward point-in-time outcomes are not profitable across the observed regimes; improve entry/exit quality before reducing gates."
                   if stock_n and stock_r <= 0 else "Not enough clean forward evidence for a regime-policy relaxation."),
    })
    return recs


def calibrate(*, db: str | None = None) -> dict[str, Any]:
    """Read only historical evidence and return an auditable regime-policy analysis."""
    if db is None:
        from src.config import load_config
        db = str(load_config().db_path)
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        crypto_rows = _load_crypto(conn)
        stock_rows = _load_stocks(conn)
    finally:
        conn.close()
    crypto_cutoff, crypto_slices = _windowed_slices(crypto_rows, asset_class="crypto")
    stocks_cutoff, stock_slices = _windowed_slices(stock_rows, asset_class="stocks")
    return {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "crypto": {"rows": crypto_rows, "cutoff": crypto_cutoff, "slices": crypto_slices},
        "stocks": {"rows": stock_rows, "cutoff": stocks_cutoff, "slices": stock_slices},
        "recommendations": _recommendations(crypto_slices, stock_slices),
    }


def _fmt(value: Any, digits: int = 2) -> str:
    if value is None:
        return "n/a"
    if value == float("inf"):
        return "inf"
    return f"{float(value):.{digits}f}"


def _render_slices(title: str, analysis: dict[str, Any]) -> list[str]:
    rows: list[str] = [f"## {title}", "", "Only valid, resolved, point-in-time forward Paper outcomes are shown. R is diagnostic only; "
                 "a policy change additionally requires adequate authoritative net-USD coverage.", ""]
    cutoff = analysis["cutoff"]
    rows.append(f"Chronological split: `{cutoff.isoformat() if cutoff else 'insufficient sample'}` (oldest 2/3 train, newest 1/3 validation).")
    rows.extend(["", "| Mode | Side | Regime | All n / USD rows / R / PF | Train n / R / PF | Validation n / R / PF |", "|---|---|---|---|---|---|"])
    slices = analysis["slices"]
    keys = sorted({key[:3] for key in slices})
    for mode, direction, regime in keys:
        def cell(window: str) -> str:
            metric = _metric(slices, mode, direction, regime, window)
            if window == "all":
                return f"{metric['n']} / {metric['usd_coverage']} / {_fmt(metric['net_r'])} / {_fmt(metric['profit_factor'])}"
            return f"{metric['n']} / {_fmt(metric['net_r'])} / {_fmt(metric['profit_factor'])}"
        rows.append(f"| {mode} | {direction} | {regime} | {cell('all')} | {cell('train')} | {cell('validation')} |")
    if not keys:
        rows.append("| n/a | n/a | n/a | n/a | n/a | n/a |")
    return rows


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Market-Regime Policy Calibration",
        "",
        f"Generated: `{result['generated_at']}`  ",
        f"Version: `{result['version']}`",
        "",
        "This is a read-model calibration. It does not modify scores, Paper routing, live routing, orders, "
        "`proposed_signals`, `signal_outcomes`, or `final_r`. Results from historical/backfill rows are never used "
        "for a runtime recommendation. A runtime change additionally requires at least 20 exact USD rows covering at "
        "least 80% of the selected forward cohort.",
        "",
    ]
    lines.extend(_render_slices("Crypto", result["crypto"]))
    lines.extend(["", *(_render_slices("Stocks", result["stocks"])), "", "## Policy Conclusions", ""])
    for rec in result["recommendations"]:
        lines.append(f"- **{rec['scope']}**: `{rec['policy']}`. {rec['reason']}")
    lines.extend([
        "",
        "## Guardrails",
        "",
        "- `unknown` is not treated as a confirmed weak regime when BTC price data are present.",
        "- A regime action is only considered stable after a chronological validation split; small cohorts remain size-capped.",
        "- This analysis does not infer a tradable edge for any disabled Shadow-only lane, especially scalp.",
    ])
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], path: str | Path | None = None) -> Path:
    destination = Path(path) if path else Path(__file__).resolve().parents[2] / "reports" / "REGIME_POLICY_CALIBRATION.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_markdown(result), encoding="utf-8")
    return destination


__all__ = [
    "EvidenceRow", "VERSION", "calibrate", "crypto_regime", "render_markdown", "stocks_regime", "write_report",
]
