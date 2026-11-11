"""Portfolio-level risk guard — combined crypto+stocks kill-switch for NEW signal generation.

2026-07-13 audit: every existing guard is either per-symbol/per-mode (crypto_quality_overlay's
cooldowns/exposure caps) or per-asset-class-and-scope AND diagnostic_only (src/risk/circuit_breaker.py
-- it only ever labels, never blocks). Nothing looks at the combined crypto+stocks book and nothing
can actually pause new signal generation on a real drawdown. This module is the first REAL (non-
diagnostic) enforcement at that level: wired into src/signals/registry.register_ideas() -- the single
entry point both crypto and stocks reports funnel through (see that module's own docstring) -- so a
severe combined drawdown skips registering an entire batch of new ideas, for BOTH asset classes,
until the rolling window recovers.

Deliberately uses actionable, size-weighted paper_execution_r from paper_execution_outcomes
(Model F resolved through the authoritative paper_actionability contract), NOT the legacy
signal_outcomes.final_r that src/risk/circuit_breaker.py reads (known to overstate PnL by ~+100..
+143R per the touch_r_optimistic_label entry in config/paper_features.yaml) and NOT raw USD (crypto
and stocks use structurally different position-sizing/ledgers; R-multiples are already the common
unit both books are compared in elsewhere this session, e.g. src/stocks/intraday_guards.py).

Fails open (never blocks) on any read/config problem -- a broken guard must never itself become an
outage; the existing diagnostic circuit_breaker.py already covers the "something is wrong, warn"
case and is untouched by this module.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

_ROOT = Path(__file__).resolve().parents[2]

_DEFAULT_CFG = {
    "enabled": True,
    "lookback_hours": 24.0,
    "min_resolved_trades": 6,   # don't judge a combined drawdown off a handful of trades
    "pause_at_combined_r": -6.0,
}

_AUDIT_DDL = """
CREATE TABLE IF NOT EXISTS portfolio_guard_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluated_at TEXT NOT NULL,
    decision TEXT NOT NULL,
    would_pause INTEGER NOT NULL,
    candidate_count INTEGER NOT NULL DEFAULT 0,
    skipped_candidate_count INTEGER NOT NULL DEFAULT 0,
    report_id TEXT,
    asset_classes_json TEXT NOT NULL DEFAULT '[]',
    combined_r REAL,
    crypto_r REAL,
    stocks_r REAL,
    resolved_trades INTEGER NOT NULL DEFAULT 0,
    lookback_hours REAL NOT NULL,
    pause_at_combined_r REAL NOT NULL,
    reason TEXT NOT NULL,
    guard_version TEXT NOT NULL,
    context_json TEXT NOT NULL DEFAULT '{}'
)
"""
_GUARD_VERSION = "portfolio_guard_v3_actionable_sized_r"


def load_cfg() -> dict[str, Any]:
    path = _ROOT / "config" / "portfolio_guard.yaml"
    if yaml and path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return {**_DEFAULT_CFG, **((yaml.safe_load(fh) or {}).get("portfolio_guard") or {})}
        except Exception:
            pass
    return dict(_DEFAULT_CFG)


@dataclass(frozen=True)
class PortfolioGuardState:
    would_pause_new_signals: bool
    combined_r: float | None
    crypto_r: float | None
    stocks_r: float | None
    resolved_trades: int
    reason: str
    diagnostic_only: bool = False   # False == this CAN and DOES block, unlike circuit_breaker.py


_OK = PortfolioGuardState(False, None, None, None, 0, "ok")


def _cutoff_iso(lookback_hours: float, now: datetime) -> str:
    return (now.astimezone(timezone.utc) - timedelta(hours=float(lookback_hours))).isoformat()


def evaluate_portfolio_guard(rows: list[dict[str, Any]], *, cfg: dict[str, Any] | None = None) -> PortfolioGuardState:
    """Pure evaluator. ``rows``: each {"asset_class": str, "paper_execution_r": float}. Never raises."""
    c = cfg or _DEFAULT_CFG
    if not c.get("enabled", True):
        return _OK
    try:
        rs = [float(r["paper_execution_r"]) for r in rows if r.get("paper_execution_r") is not None]
    except (TypeError, ValueError, KeyError):
        return _OK
    n = len(rs)
    min_n = int(c.get("min_resolved_trades", 6))
    combined = round(sum(rs), 2) if rs else None
    crypto_r = round(sum(float(r["paper_execution_r"]) for r in rows
                        if str(r.get("asset_class") or "").lower() == "crypto"
                        and r.get("paper_execution_r") is not None), 2)
    stocks_r = round(sum(float(r["paper_execution_r"]) for r in rows
                         if str(r.get("asset_class") or "").lower() == "stocks"
                         and r.get("paper_execution_r") is not None), 2)
    if n < min_n:
        return PortfolioGuardState(False, combined, crypto_r, stocks_r, n,
                                   f"only {n} resolved trades in window (< {min_n}) -- not enough evidence")
    pause_at = float(c.get("pause_at_combined_r", -6.0))
    would_pause = combined <= pause_at
    reason = (f"combined {combined:g}R <= {pause_at:g}R over {n} resolved trades (crypto {crypto_r:g}R, "
              f"stocks {stocks_r:g}R)" if would_pause else f"combined {combined:g}R over {n} resolved trades -- ok")
    return PortfolioGuardState(would_pause, combined, crypto_r, stocks_r, n, reason)


def _load_rows(db_path: str, cutoff_iso: str) -> list[dict[str, Any]]:
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=5)
    conn.row_factory = sqlite3.Row
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(paper_execution_outcomes)")}
        if "paper_execution_r" not in cols or "close_reason" not in cols:
            return []
        proposed_cols = {r[1] for r in conn.execute("PRAGMA table_info(proposed_signals)")}
        tier_expr = "p.tier" if "tier" in proposed_cols else "'B'"
        mode_expr = "p.mode" if "mode" in proposed_cols else "'intraday'"
        # Mirrors src/stocks/intraday_guards.rolling_ab_performance's own precedent for the
        # created_at window (paper_execution_outcomes has no exit timestamp of its own), and
        # src/execution/crypto_overlay_counterfactual._closed_rows' own canonical resolved-check
        # (close_reason NOT IN ('open','no_entry')) rather than relying on paper_execution_r's
        # null-ness alone -- that's an incidental invariant of the current accounting module, not
        # a guaranteed contract, and this is a kill-switch, not a diagnostic, so it should use the
        # same explicit check the rest of this codebase already treats as authoritative.
        rows = conn.execute(
            f"SELECT p.signal_id AS signal_id, p.asset_class AS asset_class, {mode_expr} AS mode, "
            f"{tier_expr} AS tier, o.paper_execution_r AS paper_execution_r "
            "FROM paper_execution_outcomes o JOIN proposed_signals p ON p.signal_id = o.signal_id "
            "WHERE o.close_reason NOT IN ('open','no_entry') AND o.paper_execution_r IS NOT NULL "
            "AND p.created_at >= ?", (cutoff_iso,)
        ).fetchall()
        # The kill-switch protects the production paper book, not every shadow/counterfactual row.
        # Reuse the same authoritative resolver as the USD ledger: C-tier, scalp and shadow alert
        # statuses become 0x; crypto HALF_SIZE contributes half its raw R.
        from src.execution.paper_actionability import build_maps, resolve_paper_actionability
        maps = build_maps(conn)
        out: list[dict[str, Any]] = []
        for raw in rows:
            row = dict(raw)
            action = resolve_paper_actionability(
                conn, str(row["signal_id"]), str(row.get("asset_class") or "crypto"),
                str(row.get("mode") or "intraday"), row.get("tier"), maps=maps,
            )
            try:
                weight = max(0.0, min(1.0, float(action.get("size_weight") or 0.0)))
                raw_r = float(row["paper_execution_r"])
            except (TypeError, ValueError):
                continue
            if weight <= 0:
                continue
            out.append({
                "asset_class": row.get("asset_class"),
                "paper_execution_r": raw_r * weight,
                "raw_paper_execution_r": raw_r,
                "size_weight": weight,
                "paper_action": action.get("paper_action"),
            })
        return out
    finally:
        conn.close()


def portfolio_guard_state(*, db: str | None = None, now: datetime | None = None) -> PortfolioGuardState:
    """Store-free convenience wrapper (opens its own read-only connection). Fails open."""
    try:
        from src.config import load_config
        path = db or str(load_config().db_path)
        cfg = load_cfg()
        now = now or datetime.now(timezone.utc)
        cutoff = _cutoff_iso(cfg.get("lookback_hours", 24.0), now)
        rows = _load_rows(path, cutoff)
        return evaluate_portfolio_guard(rows, cfg=cfg)
    except Exception as exc:
        return PortfolioGuardState(
            False, None, None, None, 0,
            f"fail_open:{type(exc).__name__}",
        )


def record_guard_decision(*, db: str | None, state: PortfolioGuardState,
                          audit_context: dict[str, Any] | None = None,
                          now: datetime | None = None) -> None:
    """Append one reconstructable registry-batch decision. Never mutates trading tables.

    Audit failure must never change the guard decision or interrupt signal registration, so callers
    deliberately invoke this best-effort. The table is created/migrated independently from the core
    SQLite schema to keep this operational journal backwards-compatible with an existing database.
    """
    from src.config import load_config

    path = db or str(load_config().db_path)
    ctx = dict(audit_context or {})
    cfg = load_cfg()
    stamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    candidate_count = max(0, int(ctx.get("candidate_count") or 0))
    decision = "FAIL_OPEN" if str(state.reason).startswith("fail_open:") else (
        "BLOCK" if state.would_pause_new_signals else "ALLOW")
    skipped = candidate_count if state.would_pause_new_signals else 0
    asset_classes = sorted({str(x).lower() for x in (ctx.get("asset_classes") or []) if str(x)})
    conn = sqlite3.connect(path, timeout=10)
    try:
        conn.execute(_AUDIT_DDL)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_portfolio_guard_audit_time "
            "ON portfolio_guard_audit(evaluated_at)"
        )
        conn.execute(
            """
            INSERT INTO portfolio_guard_audit(
                evaluated_at,decision,would_pause,candidate_count,skipped_candidate_count,
                report_id,asset_classes_json,combined_r,crypto_r,stocks_r,resolved_trades,
                lookback_hours,pause_at_combined_r,reason,guard_version,context_json
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (stamp, decision, int(state.would_pause_new_signals), candidate_count, skipped,
             str(ctx.get("report_id") or ""), json.dumps(asset_classes), state.combined_r,
             state.crypto_r, state.stocks_r, int(state.resolved_trades),
             float(cfg.get("lookback_hours", 24.0)),
             float(cfg.get("pause_at_combined_r", -6.0)), state.reason, _GUARD_VERSION,
             json.dumps(ctx, default=str, sort_keys=True)),
        )
        conn.commit()
    finally:
        conn.close()


def recent_guard_decisions(*, db: str | None = None, limit: int = 25) -> list[dict[str, Any]]:
    """Read the latest append-only decisions for operator diagnostics."""
    from src.config import load_config

    path = db or str(load_config().db_path)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=5)
    conn.row_factory = sqlite3.Row
    try:
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='portfolio_guard_audit'"
        ).fetchone()
        if not exists:
            return []
        return [dict(r) for r in conn.execute(
            "SELECT * FROM portfolio_guard_audit ORDER BY id DESC LIMIT ?", (max(1, int(limit)),)
        ).fetchall()]
    finally:
        conn.close()


def blocks_new_signals(*, db: str | None = None, now: datetime | None = None,
                       audit_context: dict[str, Any] | None = None) -> tuple[bool, str]:
    """The one thing callers need: (should_block, human_reason). Fails open (False, ...)."""
    state = portfolio_guard_state(db=db, now=now)
    if audit_context is not None:
        try:
            record_guard_decision(db=db, state=state, audit_context=audit_context, now=now)
        except Exception:
            # Observability cannot become an availability dependency for signal registration.
            pass
    return state.would_pause_new_signals, state.reason


__all__ = ["PortfolioGuardState", "evaluate_portfolio_guard", "portfolio_guard_state",
           "record_guard_decision", "recent_guard_decisions", "blocks_new_signals", "load_cfg"]
