"""Orchestration for the isolated Stocks Position Swing V2 shadow scan."""
from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

from .config import load_config as load_v1_config
from .features import compute_features
from .runner import _frame_for, _market_context, _resolve_etf, _sector_context
from .v2_config import load_config, safety_invariants
from .v2_detector import classify_market, detect
from . import v2_store


@dataclass
class V2ScanResult:
    created_at: str
    universe_size: int = 0
    scanned: int = 0
    passed: list[dict[str, Any]] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    market: dict[str, Any] = field(default_factory=dict)
    data_notes: list[str] = field(default_factory=list)
    persisted: int = 0
    dry_run: bool = False

    @property
    def rejection_counts(self) -> dict[str, int]:
        counter: Counter[str] = Counter()
        for row in self.rejected:
            counter.update(row.get("rejection_reasons") or ["UNKNOWN_REJECTION"])
        return dict(counter)


def _load_earnings(
    pc,
    sc,
    symbols: list[str],
    *,
    today: date,
) -> tuple[dict[str, dict[str, Any]], bool]:
    result = {
        symbol: {"calendar_available": False, "days": None, "report_time": None}
        for symbol in symbols
    }
    try:
        from src.stocks.data_collectors.earnings_calendar_collector import EarningsCalendarCollector

        summary = EarningsCalendarCollector(pc, sc).collect(
            symbols=symbols, include_yfinance=True
        )
        from src.stocks.market_calendar import us_trading_days_until
        for event in getattr(summary, "events", []) or []:
            symbol = str(event.symbol).upper()
            if symbol not in result:
                continue
            result[symbol]["calendar_available"] = True
            try:
                event_date = datetime.strptime(str(event.date)[:10], "%Y-%m-%d").date()
            except Exception:
                continue
            days = us_trading_days_until(event_date, today=today)
            if days < 0:
                continue
            previous = result[symbol].get("days")
            if previous is None or days < previous:
                result[symbol].update(days=days, report_time=getattr(event, "report_time", None))
        failed = {str(symbol).upper() for symbol in getattr(summary, "failed_symbols", [])}
        for symbol in symbols:
            if symbol not in failed:
                result[symbol]["calendar_available"] = True
        return result, True
    except Exception:
        return result, False


def _symbols_from_json(value: Any) -> list[str]:
    try:
        return [str(item).upper() for item in json.loads(value or "[]")]
    except Exception:
        return []


def _load_event_context(
    pc,
    symbols: list[str],
    cfg: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    output = {
        symbol: {"blocking": False, "blocking_types": [], "event_types": []}
        for symbol in symbols
    }
    try:
        from src.storage.sqlite import SQLiteStore

        store = SQLiteStore(pc.db_path)
        lookback_days = int((cfg.get("event_risk") or {}).get("event_lookback_days", 30))
        rows = store.load_news_window(
            hours=lookback_days * 24, limit=10000, asset_class="stocks"
        )
        blocking = {
            str(item).lower()
            for item in (cfg.get("event_risk") or {}).get("blocking_event_types", [])
        }
        for row in rows:
            event_type = str(row.get("event_type") or "").lower()
            if not event_type:
                continue
            for symbol in _symbols_from_json(row.get("detected_symbols_json")):
                if symbol not in output:
                    continue
                if event_type not in output[symbol]["event_types"]:
                    output[symbol]["event_types"].append(event_type)
                if event_type in blocking:
                    output[symbol]["blocking"] = True
                    if event_type not in output[symbol]["blocking_types"]:
                        output[symbol]["blocking_types"].append(event_type)
        # Legal risk uses the existing persistent legal reader as a second,
        # independent source and cannot be cleared by an empty news tail.
        try:
            from src.stocks.legal_risk import load_active_legal_news, detect_legal_risk

            legal = load_active_legal_news(store, symbols, lookback_days=lookback_days)
            for symbol in symbols:
                assessment = detect_legal_risk(legal.get(symbol, []))
                if getattr(assessment, "blocking", False):
                    output[symbol]["blocking"] = True
                    if "legal_risk" not in output[symbol]["blocking_types"]:
                        output[symbol]["blocking_types"].append("legal_risk")
        except Exception:
            pass
    except Exception:
        for symbol in symbols:
            output[symbol]["event_data_unavailable"] = True
    return output


def _last_market_date(frame) -> date | None:
    if frame is None or not len(frame):
        return None
    try:
        import pandas as pd

        stamp = pd.to_datetime(frame.index[-1], utc=True, errors="coerce")
        if pd.isna(stamp):
            return None
        return stamp.tz_convert(ZoneInfo("America/New_York")).date()
    except Exception:
        return None


def _expected_completed_session_date(now: datetime) -> date:
    from src.stocks.market_calendar import latest_us_cash_session

    opened, closed, complete = latest_us_cash_session(now)
    if not complete:
        _, closed, _ = latest_us_cash_session(opened - timedelta(seconds=1))
    return closed.astimezone(ZoneInfo("America/New_York")).date()


def _corporate_action_rejections(frame, cfg: dict[str, Any]) -> list[str]:
    """Fail closed when raw bars contain a split-like discontinuity."""
    quality = cfg.get("data_quality") or {}
    lookback = int(quality.get("corporate_action_lookback_days", 252))
    tolerance = float(quality.get("split_ratio_tolerance_pct", 8)) / 100.0
    split_ratios = [
        float(value)
        for value in quality.get(
            "split_ratios", [0.2, 0.25, 0.333333, 0.5, 2.0, 3.0, 4.0, 5.0]
        )
    ]
    try:
        close = frame["close"].astype(float).tail(lookback + 1)
        ratios = close / close.shift(1)
        for ratio in ratios.dropna():
            if any(abs(float(ratio) - split) / split <= tolerance for split in split_ratios):
                return ["UNADJUSTED_CORPORATE_ACTION"]
    except Exception:
        return ["CORPORATE_ACTION_CHECK_UNAVAILABLE"]
    return []


def _apply_portfolio_caps(
    candidates: list[dict[str, Any]],
    *,
    cfg: dict[str, Any],
    open_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Admit highest-score candidates without exceeding configured V2 risk."""
    risk_cfg = cfg.get("risk") or {}
    equity = float(risk_cfg.get("paper_equity_usd", 5000))
    max_positions = int(risk_cfg.get("max_open_positions", 5))
    max_risk = equity * float(risk_cfg.get("max_total_open_risk_pct", 0.0125))
    max_sector_notional = equity * float(
        risk_cfg.get("max_sector_exposure_pct", 35)
    ) / 100.0
    open_count = len(open_rows)
    open_risk = sum(float(row.get("risk_usd") or 0) for row in open_rows)
    sector_notional: dict[str, float] = {}
    for row in open_rows:
        sector = str(row.get("sector") or "UNKNOWN")
        sector_notional[sector] = sector_notional.get(sector, 0.0) + (
            float(row.get("qty") or 0) * float(row.get("entry_price") or 0)
        )

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for candidate in sorted(
        candidates, key=lambda row: float(row.get("score") or 0), reverse=True
    ):
        plan = candidate.get("risk_plan") or {}
        risk_usd = float(plan.get("risk_usd") or 0)
        notional = float(plan.get("qty") or 0) * float(candidate.get("entry_price") or 0)
        sector = str(candidate.get("sector") or "UNKNOWN")
        reasons: list[str] = []
        if open_count >= max_positions:
            reasons.append("PORTFOLIO_MAX_POSITIONS")
        if open_risk + risk_usd > max_risk + 1e-9:
            reasons.append("PORTFOLIO_TOTAL_RISK_CAP")
        if sector_notional.get(sector, 0.0) + notional > max_sector_notional + 1e-9:
            reasons.append("PORTFOLIO_SECTOR_EXPOSURE_CAP")
        if reasons:
            rejected.append({
                "symbol": candidate.get("symbol"),
                "rejection_reasons": reasons,
                "data_clean": candidate.get("data_clean", True),
            })
            continue
        accepted.append(candidate)
        open_count += 1
        open_risk += risk_usd
        sector_notional[sector] = sector_notional.get(sector, 0.0) + notional
    return accepted, rejected


def _primary_stock_news_health(db_path) -> tuple[list[str], list[str]]:
    """Return blocking primary-source failures and non-blocking health notes."""
    try:
        from src.news.source_health import compute_source_health

        health = compute_source_health(str(db_path))
        blockers: list[str] = []
        notes: list[str] = []
        for row in health.get("sources") or []:
            asset = str(row.get("asset_class") or "").lower()
            if asset not in {"stocks", "all", "mixed"} or not row.get("primary_source"):
                continue
            status = str(row.get("stale_status") or "").upper()
            if status in {"DEAD", "ERROR"}:
                blockers.append(f"PRIMARY_STOCK_NEWS_{status}:{row.get('source')}")
            elif status == "STALE":
                notes.append(f"primary_stock_news_stale:{row.get('source')}")
        return blockers, notes
    except Exception as exc:
        return ["STOCK_NEWS_HEALTH_UNAVAILABLE"], [
            f"stock_news_health_failed:{type(exc).__name__}"
        ]


def scan(
    *,
    config: dict[str, Any] | None = None,
    symbols: list[str] | None = None,
    dry_run: bool = False,
    skip_update: bool = False,
    limit: int | None = None,
    db_path=None,
) -> V2ScanResult:
    cfg = config or load_config()
    issues = safety_invariants(cfg)
    if issues:
        raise ValueError("; ".join(issues))
    now_utc = datetime.now(timezone.utc)
    created_at = now_utc.isoformat()
    result = V2ScanResult(created_at=created_at, dry_run=dry_run)

    from src.config import load_config as load_project_config
    from src.stocks.configs.loader import load_stocks_config
    from src.stocks.data_collectors.stock_ohlcv_collector import StockOHLCVCollector
    from src.stocks.data_collectors.market_index_collector import MarketIndexCollector
    from src.stocks.data_collectors.sector_etf_collector import SectorETFCollector

    pc = load_project_config()
    sc = load_stocks_config()
    db_path = db_path or pc.db_path
    base = StockOHLCVCollector(pc, sc)
    v1 = load_v1_config()
    v1_universe = list((v1.get("universe") or {}).get("symbols") or [])
    configured = v1_universe if (cfg.get("universe") or {}).get(
        "use_position_framework_universe", True
    ) else list((cfg.get("universe") or {}).get("symbols") or [])
    universe = [str(symbol).upper() for symbol in (symbols or configured)]
    universe = universe[: int((cfg.get("universe") or {}).get("max_symbols", 75))]
    result.universe_size = len(universe)
    sector_map = {
        str(key).upper(): str(value)
        for key, value in (v1.get("sector_map") or {}).items()
    }

    stock_summary = market_summary = sector_summary = None
    if not skip_update:
        try:
            stock_summary = base.collect(
                universe, ["1d", "1wk"], period="2y", throttle_seconds=0.0
            )
            market_summary = MarketIndexCollector(pc, sc).collect(intervals=["1d"])
            sector_summary = SectorETFCollector(pc, sc).collect(intervals=["1d"])
        except Exception as exc:
            result.data_notes.append(f"fetch_failed_using_cache:{type(exc).__name__}")
    else:
        result.data_notes.append("cache_only")

    vix_symbol = getattr(sc, "volatility_index", "^VIX") or "^VIX"
    market_frames = {
        "SPY": _frame_for(market_summary, base, "SPY"),
        "QQQ": _frame_for(market_summary, base, "QQQ"),
        "VIX": _frame_for(market_summary, base, vix_symbol),
    }
    market_ctx = _market_context(market_frames, {
        "market_filter": {
            "warn_if_vix_above": (cfg.get("market") or {}).get("warn_vix_above", 22)
        }
    })
    market_ctx["v2_regime"] = classify_market(market_ctx, cfg)
    result.market = market_ctx
    spy, qqq = market_frames["SPY"], market_frames["QQQ"]
    expected_session_date = _expected_completed_session_date(now_utc)
    market_data_fresh = _last_market_date(spy) == expected_session_date
    sector_frames = {}
    for etf in set(sector_map.values()):
        sector_frames[etf] = _frame_for(sector_summary, base, etf)

    earnings, earnings_available = _load_earnings(
        pc,
        sc,
        universe,
        today=now_utc.astimezone(ZoneInfo("America/New_York")).date(),
    )
    if not earnings_available:
        result.data_notes.append("earnings_calendar_unavailable")
    events = _load_event_context(pc, universe, cfg)
    news_health_rejections, news_health_notes = _primary_stock_news_health(db_path)
    result.data_notes.extend(news_health_notes)

    for symbol in universe:
        frame = _frame_for(stock_summary, base, symbol)
        if frame is None or not len(frame):
            result.rejected.append({
                "symbol": symbol,
                "rejection_reasons": ["DATA_UNAVAILABLE"],
            })
            continue
        etf = _resolve_etf(sc, symbol, sector_map)
        if not etf:
            result.rejected.append({
                "symbol": symbol,
                "rejection_reasons": ["SECTOR_MAPPING_UNAVAILABLE"],
            })
            continue
        weekly = _frame_for(stock_summary, base, symbol, "1wk")
        feats = compute_features(
            frame,
            spy_df=spy,
            qqq_df=qqq,
            sector_df=sector_frames.get(etf),
            weekly_df=weekly,
        )
        sector_ctx = _sector_context(
            sc, symbol, sector_frames, spy, sector_map=sector_map
        )
        data_rejections: list[str] = []
        data_rejections.extend(news_health_rejections)
        if not market_data_fresh:
            data_rejections.append("STALE_MARKET_DAILY_BAR")
        if _last_market_date(frame) != expected_session_date:
            data_rejections.append("STALE_SYMBOL_DAILY_BAR")
        if _last_market_date(sector_frames.get(etf)) != expected_session_date:
            data_rejections.append("STALE_SECTOR_DAILY_BAR")
        data_rejections.extend(_corporate_action_rejections(frame, cfg))
        candidate = detect(
            symbol,
            frame,
            feats,
            market_ctx=market_ctx,
            sector_ctx=sector_ctx,
            earnings=earnings[symbol],
            event_ctx=events[symbol],
            cfg=cfg,
            data_ctx={"clean": not data_rejections, "rejection_reasons": data_rejections},
        )
        result.scanned += 1
        if candidate.get("passed"):
            result.passed.append(candidate)
        else:
            result.rejected.append({
                "symbol": symbol,
                "rejection_reasons": candidate.get("rejection_reasons") or ["UNKNOWN"],
                "data_clean": candidate.get("data_clean", True),
            })

    result.passed.sort(key=lambda row: float(row.get("score") or 0), reverse=True)
    admitted, cap_rejections = _apply_portfolio_caps(
        result.passed,
        cfg=cfg,
        open_rows=v2_store.open_candidates(db_path),
    )
    result.passed = admitted
    result.rejected.extend(cap_rejections)
    if limit is not None:
        result.passed = result.passed[: int(limit)]
    if not dry_run:
        result.persisted = v2_store.insert_candidates(
            result.passed, created_at=created_at, db_path=db_path
        )
    v2_store.record_scan(
        created_at=created_at,
        cfg=cfg,
        universe_size=result.universe_size,
        scanned=result.scanned,
        candidate_count=len(result.passed),
        rejected_count=len(result.rejected),
        persisted=result.persisted,
        market_regime=market_ctx["v2_regime"],
        rejection_counts=result.rejection_counts,
        data_notes=result.data_notes,
        dry_run=dry_run,
        db_path=db_path,
    )
    return result
