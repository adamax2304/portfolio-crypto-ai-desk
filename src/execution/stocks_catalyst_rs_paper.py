"""Paper adapter for fresh, clean Catalyst RS Shadow confirmations.

The strategy remains independently measured in Shadow. This adapter registers
only a fresh point-in-time confirmation and never replays historical outcomes
into Paper.
"""
from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.execution import stocks_intraday_breakout_1bar_paper as shared
from src.models import TradeIdea


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CFG: dict[str, Any] = {
    "enabled": True, "live_enabled": False,
    "profile_id": "stocks_catalyst_rs_paper_v1",
    "strategy_id": "stocks_catalyst_rs_paper_v1",
    "paper_lane": "paper_stocks_catalyst_rs",
    "source_shadow_profile": "stocks_catalyst_rs_profile_v2",
    "allowed_evidence_cohorts": ["strict_v1", "exploratory_v1"],
    "max_confirmation_age_minutes": 30, "max_signals_per_symbol_session": 1,
    "max_chase_r": 0.35, "exploratory_size_label": "HALF_SIZE",
    "strict_size_label": "FULL_SIZE", "use_default_universe": True,
}


def load_cfg() -> dict[str, Any]:
    cfg = deepcopy(DEFAULT_CFG)
    path = ROOT / "config" / "paper" / "stocks" / "catalyst_rs.yaml"
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        supplied = raw.get("stocks_catalyst_rs_paper") or {}
        if isinstance(supplied, dict):
            cfg.update(supplied)
    except Exception:
        pass
    return cfg


def _raw(signal: dict[str, Any]) -> dict[str, Any]:
    value = signal.get("raw_idea_json")
    if isinstance(value, dict):
        return dict(value)
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def matches_signal(signal: dict[str, Any], cfg: dict[str, Any] | None = None) -> bool:
    cfg = cfg or load_cfg()
    raw = _raw(signal)
    return bool(
        cfg.get("enabled", True)
        and str(signal.get("asset_class") or "").lower() == "stocks"
        and str(signal.get("mode") or "").lower() == "intraday"
        and raw.get("paper_entry_profile") == cfg.get("profile_id")
        and raw.get("paper_lane") == cfg.get("paper_lane")
    )


def _fresh_rows(rows: list[dict[str, Any]], *, now: datetime, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    cutoff = now - timedelta(minutes=float(cfg.get("max_confirmation_age_minutes") or 30))
    allowed = {str(item) for item in (cfg.get("allowed_evidence_cohorts") or [])}
    selected: list[dict[str, Any]] = []
    for row in rows:
        entry_at = pd.to_datetime(row.get("entry_ts"), utc=True, errors="coerce")
        if pd.isna(entry_at) or not (pd.Timestamp(cutoff) <= entry_at <= pd.Timestamp(now)):
            continue
        if str(row.get("eligibility_status")) != "eligible" or int(row.get("is_clean_for_edge") or 0) != 1:
            continue
        if str(row.get("evidence_cohort")) not in allowed:
            continue
        if any(row.get(key) in (None, "") for key in ("entry_price", "stop_price", "tp1", "tp2", "tp3")):
            continue
        selected.append(row)
    return selected


def _idea(row: dict[str, Any], cfg: dict[str, Any], now: datetime) -> TradeIdea:
    cohort = str(row.get("evidence_cohort") or "exploratory_v1")
    score = 78.0 if cohort == "strict_v1" else 69.0
    size_label = (cfg.get("strict_size_label") if cohort == "strict_v1"
                  else cfg.get("exploratory_size_label"))
    entry = float(row["entry_price"])
    stop = float(row["stop_price"])
    raw = {
        "pre_gate_tier": "B", "final_tier": "B", "demoted_by_gate": False,
        "paper_entry_profile": cfg["profile_id"], "paper_lane": cfg["paper_lane"],
        "paper_entry_policy_version": "stocks_catalyst_rs_confirmed_v1",
        "paper_entry_confirmation": "fresh_clean_catalyst_rs_15m_confirmation",
        "paper_max_chase_r": float(cfg.get("max_chase_r") or 0.35),
        "paper_size_label": size_label,
        "source_shadow_profile": cfg["source_shadow_profile"],
        "source_shadow_candidate_id": row.get("candidate_id"),
        "source_news_event_id": row.get("news_event_id"),
        "catalyst_type": row.get("catalyst_type"),
        "catalyst_source_quality": row.get("catalyst_source_quality"),
        "evidence_cohort": cohort,
        "confirmation_at": row.get("entry_ts"), "confirmation_price": entry,
        "setup": {"entry_low": entry, "entry_high": entry, "invalidation": stop,
                  "tp1": float(row["tp1"]), "tp2": float(row["tp2"]), "tp3": float(row["tp3"])},
        "catalyst_rs_features": {key: row.get(key) for key in (
            "gap_or_impulse_pct", "rvol", "rs_spy_pct", "rs_sector_pct",
            "market_regime", "sector", "sector_etf")},
    }
    return TradeIdea(
        symbol=str(row["symbol"]).upper(), direction="long", score=score,
        confidence="high" if cohort == "strict_v1" else "medium", risk_level="medium",
        timeframe="15m", tier="B", mode="intraday", asset_class="stocks",
        exchange_focus="US", exchanges_confirmed=["US"], data_confidence="high",
        thesis=(f"Fresh {row.get('catalyst_type') or 'company'} catalyst with relative-strength "
                "continuation above SPY and sector."),
        evidence=[f"cohort={cohort}", f"RVOL={row.get('rvol')}",
                  f"RS_SPY={row.get('rs_spy_pct')}%", f"RS_sector={row.get('rs_sector_pct')}%"],
        counterarguments=["Same-day continuation can fade after the opening impulse."],
        entry_plan=f"Use fresh quote after confirmed 15m close near {entry:.6g}",
        invalidation=f"{stop:.6g}",
        targets=[f"{float(row['tp1']):.6g}", f"{float(row['tp2']):.6g}", f"{float(row['tp3']):.6g}"],
        what_to_monitor=["VWAP", "SPY and sector relative strength", "catalyst validity"],
        avoid_conditions=["stale quote", "price beyond no-chase window", "catalyst invalidated"],
        data_sources_used=["canonical_news", "Finnhub_quote", "yfinance_OHLCV"], raw=raw,
    )


def refresh(*, db: str | None = None, now: datetime | None = None,
            refresh_shadow: bool = True, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_cfg()
    moment = shared._utc(now)
    if not cfg.get("enabled", True) or not cfg.get("new_signals_enabled", True):
        return {"enabled": False, "selected": 0, "registered": 0, "signal_ids": []}
    from src.config import load_config
    from src.execution import stocks_catalyst_rs_shadow as shadow
    from src.signals.config import load_signal_tracking_config
    from src.signals.registry import register_ideas
    from src.stocks.paper_funnel import snapshot_signals

    project = load_config()
    path = Path(db) if db else Path(project.db_path)
    result = shadow.refresh(db=str(path), persist=True, now=moment) if refresh_shadow else {"rows": []}
    rows = [dict(row) for row in (result.get("rows") or [])]
    if not rows:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            rows = [dict(row) for row in conn.execute(
                "SELECT * FROM stocks_catalyst_rs_shadow_outcomes WHERE profile_id=?",
                (cfg["source_shadow_profile"],),
            )]
        except sqlite3.OperationalError:
            rows = []
        finally:
            conn.close()
    selected_rows = _fresh_rows(rows, now=moment, cfg=cfg)
    session = shared._session_key(moment.isoformat()) or moment.date().isoformat()
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        selected_rows = [row for row in selected_rows if not shared._already_registered(
            conn, symbol=str(row["symbol"]).upper(), session=session, profile_id=str(cfg["profile_id"])
        )]
    except sqlite3.OperationalError:
        pass
    finally:
        conn.close()
    ideas = [_idea(row, cfg, moment) for row in selected_rows]
    from src.storage.sqlite import SQLiteStore
    database = SQLiteStore(path)
    registration = register_ideas(
        database, ideas, config=load_signal_tracking_config(project.root),
        report_id=f"{cfg['strategy_id']}_{session}", market_regime="catalyst_rs",
        asset_class="stocks", created_at=moment.isoformat(),
    )
    if registration.signal_ids:
        snapshot_signals(path, registration.signal_ids, now=moment)
    return {"enabled": True, "selected": len(ideas), "registered": registration.inserted,
            "existing": registration.skipped_existing, "signal_ids": list(registration.signal_ids),
            "profile_id": cfg["profile_id"], "paper_lane": cfg["paper_lane"],
            "live_enabled": False, "decision_at": moment.isoformat()}


def resolve_entry(*, signal: dict[str, Any], candles: Any, now: datetime,
                  timeframe_seconds: int, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_cfg()
    if not matches_signal(signal, cfg):
        return {"applied": False}
    raw = _raw(signal)
    confirmed = pd.to_datetime(raw.get("confirmation_at"), utc=True, errors="coerce")
    if pd.isna(confirmed):
        return {"applied": True, "ready": False, "profile_id": cfg["profile_id"],
                "reason": "confirmation_timestamp_missing"}
    age = (pd.Timestamp(shared._utc(now)) - confirmed).total_seconds() / 60.0
    if age > float(cfg.get("max_confirmation_age_minutes") or 30):
        return {"applied": True, "ready": False, "profile_id": cfg["profile_id"],
                "reason": "catalyst_rs_confirmation_stale"}
    price = float(raw.get("confirmation_price") or signal.get("entry_trigger") or signal.get("entry_high"))
    return {"applied": True, "ready": True, "profile_id": cfg["profile_id"],
            "entry_mode": "CATALYST_RS_CONTINUATION", "reason": "fresh_clean_catalyst_rs_confirmation",
            "confirmation_at": confirmed.isoformat(), "entry_price": price, "entry_trigger": price,
            "max_chase_r": float(cfg.get("max_chase_r") or 0.35),
            "candles": pd.DataFrame()}


__all__ = ["load_cfg", "matches_signal", "refresh", "resolve_entry"]
