"""Paper-only promotion of the isolated one-bar stock breakout control.

The producer reuses the regular stock analysis/news/actionability pipeline but
registers only the explicitly marked profile.  Entry is resolved separately by
the tracker on the close of one 15m candle beyond the structural breakout and
session VWAP.  The Shadow experiment is intentionally not modified.
"""
from __future__ import annotations

import json
import sqlite3
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CFG: dict[str, Any] = {
    "enabled": True, "live_enabled": True,
    "profile_id": "stocks_intraday_breakout_1bar_paper_v1",
    "source_shadow_profile": "breakout_confirm_1bar_15m_v1",
    "strategy_id": "stocks_intraday_breakout_1bar_paper_v1",
    "paper_lane": "paper_stocks_intraday_breakout_1bar",
    "activated_at": "", "timeframe": "15m", "confirmation_bars": 1,
    "require_vwap": True, "max_signals_per_symbol_session": 1,
    "include_preopen_ab_plans": True, "use_default_universe": True,
    "max_chase_r": 0.30, "symbols": [],
}


def load_cfg() -> dict[str, Any]:
    cfg = deepcopy(DEFAULT_CFG)
    path = ROOT / "config" / "stocks" / "intraday_breakout_1bar_paper.yaml"
    if yaml and path.exists():
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            supplied = raw.get("stocks_intraday_breakout_1bar_paper") or {}
            if isinstance(supplied, dict):
                cfg.update(supplied)
        except Exception:
            pass
    return cfg


def _utc(value: datetime | None = None) -> datetime:
    moment = value or datetime.now(timezone.utc)
    return moment.replace(tzinfo=timezone.utc) if moment.tzinfo is None else moment.astimezone(timezone.utc)


def _float(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _raw(signal: dict[str, Any]) -> dict[str, Any]:
    value = signal.get("raw_idea_json") if isinstance(signal, dict) else None
    if isinstance(value, dict):
        return dict(value)
    try:
        parsed = json.loads(value or "{}")
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def configured_symbols(cfg: dict[str, Any] | None = None) -> list[str]:
    cfg = cfg or load_cfg()
    explicit = [str(item).upper() for item in (cfg.get("symbols") or [])]
    if explicit:
        return explicit
    if cfg.get("use_default_universe", True):
        try:
            raw = yaml.safe_load((ROOT / "config" / "stocks" / "universe.yaml").read_text(encoding="utf-8")) or {}
            benchmarks = {str(item).upper() for item in (raw.get("indices") or [])}
            benchmarks.update(str(item).upper() for item in (raw.get("sector_etfs") or {}).values())
            benchmarks.add(str(raw.get("volatility_index") or "").upper())
            return [str(item).upper() for item in (raw.get("default_symbols") or [])
                    if str(item).upper() not in benchmarks]
        except Exception:
            pass
    return explicit


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


def tag_idea(idea: Any, cfg: dict[str, Any] | None = None) -> Any:
    cfg = cfg or load_cfg()
    raw = deepcopy(getattr(idea, "raw", None) or {})
    raw.update({
        "paper_entry_profile": cfg["profile_id"],
        "paper_lane": cfg["paper_lane"],
        "paper_entry_policy_version": "stocks_breakout_confirm_1bar_v1",
        "evidence_cohort": cfg.get("evidence_cohort", "stocks_rth_breakout_research_v1"),
        "evidence_activated_at": cfg.get("evidence_activated_at"),
        "paper_entry_confirmation": "one_closed_15m_bar_beyond_trigger_and_vwap",
        "source_shadow_profile": cfg["source_shadow_profile"],
    })
    return idea.model_copy(update={"raw": raw})


def select_ideas(ideas: list[Any], cfg: dict[str, Any] | None = None) -> list[Any]:
    """Keep only the same broadly eligible breakout population as the control."""
    cfg = cfg or load_cfg()
    symbols = set(configured_symbols(cfg))
    selected: list[Any] = []
    for idea in ideas:
        raw = dict(getattr(idea, "raw", None) or {})
        setup = dict(raw.get("setup") or {})
        pre_gate = str(raw.get("pre_gate_tier") or getattr(idea, "tier", "")).upper()
        final_tier = str(getattr(idea, "tier", "")).upper()
        if str(getattr(idea, "symbol", "")).upper() not in symbols:
            continue
        if str(getattr(idea, "mode", "")).lower() != "intraday":
            continue
        if str(getattr(idea, "direction", "")).lower() not in {"long", "short"}:
            continue
        # The profile is a breakout experiment, never a silent pullback route.
        low, high = _float(setup.get("entry_low")), _float(setup.get("entry_high"))
        if low is None or high is None or _float(setup.get("invalidation")) is None:
            continue
        # Do not add a textual tag filter here.  The source Shadow profile
        # tested the deterministic breakout confirmation against this whole
        # A/B setup population; narrowing by wording would make Paper evidence
        # incomparable and create an un-audited extra strategy condition.
        # Keep final A/B.  A pre-open C is admitted only when it was a true
        # pre-gate A/B plan; existing pre-US review/actionability remains the
        # sole route that can make that narrow case executable.
        cap_reasons = [str(item) for item in (raw.get("cap_reasons") or [])]
        is_market_closed_plan = any(
            "market_closed_intraday_planning_only" in reason for reason in cap_reasons
        )
        is_preopen_ab_plan = bool(
            cfg.get("include_preopen_ab_plans", True)
            and final_tier == "C"
            and pre_gate in {"A", "B"}
            and is_market_closed_plan
        )
        if final_tier not in {"A", "B"} and not is_preopen_ab_plan:
            continue
        selected.append(tag_idea(idea, cfg))
    return selected


def _session_key(value: str) -> str | None:
    stamp = pd.to_datetime(value, utc=True, errors="coerce")
    if pd.isna(stamp):
        return None
    try:
        from src.stocks.market_calendar import stock_intraday_target_session
        opened, _closed = stock_intraday_target_session(stamp.to_pydatetime())
        return opened.astimezone(ZoneInfo("America/New_York")).date().isoformat()
    except Exception:
        return stamp.tz_convert("America/New_York").date().isoformat()


def _is_preopen_plan(*, tier: str, raw: dict[str, Any]) -> bool:
    return bool(
        str(tier or "").upper() == "C"
        and str(raw.get("pre_gate_tier") or "").upper() in {"A", "B"}
        and any(
            "market_closed_intraday_planning_only" in str(reason)
            for reason in (raw.get("cap_reasons") or [])
        )
    )


def _already_registered(
    conn: sqlite3.Connection,
    *,
    symbol: str,
    session: str,
    profile_id: str,
    candidate_tier: str = "A",
    candidate_raw: dict[str, Any] | None = None,
) -> bool:
    """Deduplicate executable candidates separately from pre-open plans.

    A C-tier planning row is useful for the pre-US review, but it must not
    consume the profile's one executable slot for the target session.  A
    fresh RTH A/B candidate may therefore follow the plan; repeated plans and
    repeated executable candidates remain deduplicated independently.
    """
    candidate_is_plan = _is_preopen_plan(
        tier=candidate_tier, raw=dict(candidate_raw or {})
    )
    rows = conn.execute(
        "SELECT created_at,tier,raw_idea_json FROM proposed_signals "
        "WHERE asset_class='stocks' AND mode='intraday' AND symbol=?",
        (symbol,),
    ).fetchall()
    for created_at, tier, raw_json in rows:
        if _session_key(str(created_at)) != session:
            continue
        try:
            raw = json.loads(raw_json or "{}")
        except (TypeError, ValueError, json.JSONDecodeError):
            raw = {}
        if not isinstance(raw, dict) or raw.get("paper_entry_profile") != profile_id:
            continue
        existing_is_plan = _is_preopen_plan(tier=str(tier or ""), raw=raw)
        if existing_is_plan == candidate_is_plan:
            return True
    return False


def _profile_guarded(
    candidates: list[Any], *, pipeline: Any, cfg: dict[str, Any], now: datetime,
) -> tuple[list[Any], dict[str, int]]:
    """Apply the rolling guard after the Paper profile is known.

    The shared stocks scan deliberately has no entry-policy identity.  Applying
    a portfolio-style guard there mixed BREAKOUT, PULLBACK and Catalyst RS
    evidence.  Here the profile id is immutable and the guard can use only its
    own clean forward executions.
    """
    try:
        from src.stocks import intraday_guards, load_stocks_config

        risk = load_stocks_config(pipeline.config.root).risk
    except Exception:
        return candidates, {}

    kept: list[Any] = []
    blocked: Counter[str] = Counter()
    for idea in candidates:
        if str(getattr(idea, "tier", "")).upper() not in {"A", "B"}:
            kept.append(idea)
            continue
        raw = dict(getattr(idea, "raw", None) or {})
        structured = dict(raw.get("structured") or {})
        actionability = dict(raw.get("intraday_actionability") or {})
        sector_confirmed = actionability.get("sector_confirmation_status") == "confirmed"
        confirmation_ok = intraday_guards.long_confirmation_ok({
            "rs_vs_spy": structured.get("rs_vs_spy"),
            "volume_ratio": structured.get("volume_ratio"),
            "sector_contradicts": False if sector_confirmed else None,
            "sector_weak": False if sector_confirmed else None,
            "atr_extension": structured.get("atr_extension"),
        }, risk)
        reasons = intraday_guards.guard_cap_reasons(
            pipeline.db,
            risk,
            direction=str(getattr(idea, "direction", "") or "").lower(),
            long_confirmation_ok=confirmation_ok,
            paper_entry_profile=str(cfg["profile_id"]),
            now=now,
        )
        if reasons:
            blocked.update(reasons)
            continue
        kept.append(idea)
    return kept, dict(blocked)


def register_result(
    *,
    pipeline: Any,
    result: Any,
    cfg: dict[str, Any] | None = None,
    now: datetime | None = None,
    selector: Any | None = None,
) -> dict[str, Any]:
    """Register one profile from an already-computed stocks report.

    The fast monitor uses this path so BREAKOUT/PULLBACK candidates inherit
    the same decision clock, news and SI-1..SI-5 context as the generic report
    without re-fetching the whole universe for each profile.
    """
    cfg = cfg or load_cfg()
    moment = _utc(now)
    if not cfg.get("enabled", True):
        return {"enabled": False, "registered": 0, "selected": 0, "signal_ids": []}
    from src.signals.config import load_signal_tracking_config
    from src.signals.registry import register_ideas
    from src.stocks.paper_funnel import snapshot_signals

    select = selector or select_ideas
    candidates = select(list(result.ideas), cfg)
    candidates, guard_blocked = _profile_guarded(
        candidates, pipeline=pipeline, cfg=cfg, now=moment,
    )
    decision_at = str(getattr(result, "decision_at", "") or moment.isoformat())
    session = _session_key(decision_at) or moment.astimezone(
        ZoneInfo("America/New_York")
    ).date().isoformat()
    with pipeline.db.connect() as conn:
        candidates = [
            idea for idea in candidates
            if not _already_registered(
                conn,
                symbol=str(idea.symbol).upper(),
                session=session,
                profile_id=str(cfg["profile_id"]),
                candidate_tier=str(getattr(idea, "tier", "")),
                candidate_raw=dict(getattr(idea, "raw", None) or {}),
            )
        ]
    registration = register_ideas(
        pipeline.db,
        candidates,
        config=load_signal_tracking_config(pipeline.config.root),
        report_id=f"{cfg['strategy_id']}_{session}",
        market_regime=(result.regime.get("regime") or {}).get("label", ""),
        asset_class="stocks",
        created_at=decision_at,
    )
    if registration.signal_ids:
        snapshot_signals(pipeline.config.db_path, registration.signal_ids, now=moment)
    return {
        "enabled": True,
        "selected": len(candidates),
        "registered": registration.inserted,
        "existing": registration.skipped_existing,
        "signal_ids": list(registration.signal_ids),
        "profile_id": cfg["profile_id"],
        "paper_lane": cfg["paper_lane"],
        "live_enabled": bool(cfg.get("live_enabled", False)),
        "decision_at": decision_at,
        "guard_blocked": guard_blocked,
    }


def refresh(*, project_config: Any | None = None, now: datetime | None = None,
            skip_data_update: bool = False, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run the normal stocks analysis for the isolated universe and register it.

    Registration preserves canonical-news linking, pre-US review eligibility,
    paper-funnel snapshots and all ordinary Paper guards.  It has no live path.
    """
    cfg = cfg or load_cfg()
    moment = _utc(now)
    if not cfg.get("enabled", True):
        return {"enabled": False, "registered": 0, "selected": 0, "signal_ids": []}
    from src.config import load_config
    from src.stocks.pipelines.stocks_pipeline import StocksPipeline

    project_config = project_config or load_config()
    pipeline = StocksPipeline(project_config)
    result = pipeline.run_report(
        mode="intraday", symbols=configured_symbols(cfg),
        skip_data_update=skip_data_update, shadow_only=True, now=moment,
        apply_intraday_guards=False,
    )
    return register_result(pipeline=pipeline, result=result, cfg=cfg, now=moment)


def _rth(frame: pd.DataFrame) -> pd.DataFrame:
    if frame is None or frame.empty or "timestamp" not in frame:
        return pd.DataFrame(columns=getattr(frame, "columns", None))
    work = frame.copy()
    work["timestamp"] = pd.to_datetime(work["timestamp"], utc=True, errors="coerce")
    work = work.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    local = work["timestamp"].dt.tz_convert("America/New_York")
    minutes = local.dt.hour * 60 + local.dt.minute
    return work.loc[(minutes >= 9 * 60 + 30) & (minutes < 16 * 60)].reset_index(drop=True)


def _vwap(frame: pd.DataFrame, idx: int) -> float | None:
    part = frame.iloc[:int(idx) + 1]
    volume = pd.to_numeric(part.get("volume"), errors="coerce").fillna(0.0)
    typical = (pd.to_numeric(part["high"], errors="coerce") + pd.to_numeric(part["low"], errors="coerce") + pd.to_numeric(part["close"], errors="coerce")) / 3.0
    total = float(volume.sum())
    return float((typical * volume).sum() / total) if total > 0 else None


def resolve_entry(*, signal: dict[str, Any], candles: pd.DataFrame, now: datetime,
                  timeframe_seconds: int, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    """Resolve one closed-candle confirmation without changing a database."""
    cfg = cfg or load_cfg()
    if not matches_signal(signal, cfg):
        return {"applied": False}
    if int(timeframe_seconds) != 15 * 60:
        return {"applied": True, "ready": False, "profile_id": cfg["profile_id"], "reason": "15m_confirmation_frame_unavailable"}
    created = pd.to_datetime(signal.get("created_at"), utc=True, errors="coerce")
    if pd.isna(created):
        return {"applied": True, "ready": False, "profile_id": cfg["profile_id"], "reason": "signal_timestamp_invalid"}
    frame = _rth(candles)
    if frame.empty:
        return {"applied": True, "ready": False, "profile_id": cfg["profile_id"], "reason": "rth_15m_bars_unavailable"}
    try:
        from src.stocks.market_calendar import stock_intraday_target_session
        target_open, _target_close = stock_intraday_target_session(created.to_pydatetime())
        session = target_open.astimezone(ZoneInfo("America/New_York")).date()
    except Exception:
        session = created.tz_convert("America/New_York").date()
    local_dates = frame["timestamp"].dt.tz_convert("America/New_York").dt.date
    frame = frame.loc[local_dates == session].reset_index(drop=True)
    close_times = frame["timestamp"] + pd.Timedelta(minutes=15)
    cutoff = pd.Timestamp(_utc(now))
    eligible = frame.index[(close_times > created) & (close_times <= cutoff)]
    low, high = _float(signal.get("entry_low")), _float(signal.get("entry_high"))
    if low is None or high is None:
        return {"applied": True, "ready": False, "profile_id": cfg["profile_id"], "reason": "setup_missing"}
    trigger = max(low, high) if str(signal.get("direction") or "long").lower() == "long" else min(low, high)
    direction = str(signal.get("direction") or "long").lower()
    run = 0
    for idx in eligible:
        row = frame.iloc[int(idx)]
        close, vwap = _float(row.get("close")), _vwap(frame, int(idx))
        confirmed = close is not None and vwap is not None and ((close >= trigger and close >= vwap) if direction == "long" else (close <= trigger and close <= vwap))
        run = run + 1 if confirmed else 0
        if run >= max(1, int(cfg.get("confirmation_bars") or 1)):
            entry_at = (row["timestamp"] + pd.Timedelta(minutes=15)).isoformat()
            later = frame.loc[frame["timestamp"] >= pd.Timestamp(entry_at)].reset_index(drop=True)
            return {
                "applied": True, "ready": True, "profile_id": cfg["profile_id"],
                "entry_mode": "BREAKOUT_CONTINUATION", "reason": "one_closed_15m_breakout_vwap_confirmed",
                "confirmation_at": entry_at, "entry_price": close, "entry_trigger": close,
                "max_chase_r": float(cfg.get("max_chase_r") or 0.30), "candles": later,
            }
    return {"applied": True, "ready": False, "profile_id": cfg["profile_id"], "entry_mode": "BREAKOUT_CONTINUATION", "reason": "breakout_confirmation_pending"}


__all__ = [
    "load_cfg", "configured_symbols", "matches_signal", "tag_idea",
    "select_ideas", "register_result", "refresh", "resolve_entry",
]
