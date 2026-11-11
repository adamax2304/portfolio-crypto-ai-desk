"""Runner — orchestrates the Stocks Position Framework scan (SHADOW-ONLY).

Flow: universe → daily OHLCV (+ SPY/QQQ/VIX + sector ETFs, reusing existing collectors) →
features → detector → persist passed candidates to the shadow tables. NEVER writes
proposed_signals, NEVER sends Telegram, NEVER touches live. Heavy imports (pandas/yfinance-backed
collectors) are lazy so the pure modules stay unit-testable without them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from typing import Any

from . import SOURCE_VERSION, SHADOW_STATUS
from .config import load_config
from .features import compute_features, sma, rs_vs
from .setup_detector import detect
from . import shadow_store


@dataclass
class ScanResult:
    created_at: str
    shadow_only: bool = True
    live_locked: bool = True
    universe_size: int = 0
    scanned: int = 0
    passed: list[dict[str, Any]] = field(default_factory=list)
    rejected: list[dict[str, Any]] = field(default_factory=list)
    market: dict[str, Any] = field(default_factory=dict)
    data_notes: list[str] = field(default_factory=list)
    persisted: int = 0
    dry_run: bool = False

    @property
    def passed_count(self) -> int:
        return len(self.passed)

    @property
    def rejected_count(self) -> int:
        return len(self.rejected)


def _frame_for(summary, cache_collector, symbol: str, interval: str = "1d"):
    """Prefer the freshly-fetched frame; fall back to the on-disk cache for `interval`."""
    key = f"{symbol}@{interval}"
    fetched = getattr(summary, "fetched", {}) if summary is not None else {}
    res = fetched.get(key)
    if res is not None and getattr(res, "dataframe", None) is not None:
        return res.dataframe
    return cache_collector.load_cached(symbol, interval)


def _market_context(frames: dict, cfg: dict) -> dict[str, Any]:
    spy, qqq, vix = frames.get("SPY"), frames.get("QQQ"), frames.get("VIX")
    ctx: dict[str, Any] = {"spy_above_50d": None, "spy_above_200d": None,
                           "qqq_above_50d": None, "vix": None, "label": "unknown"}
    if spy is not None and len(spy):
        last = float(spy["close"].iloc[-1])
        s50, s200 = sma(spy, 50), sma(spy, 200)
        ctx["spy_above_50d"] = None if s50 is None else last > s50
        ctx["spy_above_200d"] = None if s200 is None else last > s200
    if qqq is not None and len(qqq):
        q50 = sma(qqq, 50)
        ctx["qqq_above_50d"] = None if q50 is None else float(qqq["close"].iloc[-1]) > q50
    if vix is not None and len(vix):
        ctx["vix"] = float(vix["close"].iloc[-1])
    warn = float((cfg.get("market_filter") or {}).get("warn_if_vix_above", 22))
    if ctx["spy_above_50d"] and ctx["spy_above_200d"] and (ctx["vix"] is None or ctx["vix"] < warn):
        ctx["label"] = "risk_on"
    elif ctx["spy_above_200d"] is False:
        ctx["label"] = "risk_off"
    else:
        ctx["label"] = "caution"
    return ctx


def _resolve_etf(sc, symbol: str, sector_map: dict) -> str | None:
    """Framework-local sector_map wins; fall back to the shared StocksConfig sector mapping."""
    return (sector_map or {}).get(symbol) or (getattr(sc, "sector_etf_for", lambda s: "")(symbol) or None)


def _sector_context(sc, symbol: str, sector_frames: dict, spy_df, sector_map=None) -> dict[str, Any]:
    sector = getattr(sc, "sector_for", lambda s: "")(symbol) or None
    sector_etf = _resolve_etf(sc, symbol, sector_map or {})
    sdf = sector_frames.get(sector_etf) if sector_etf else None
    ctx: dict[str, Any] = {"sector": sector, "sector_etf": sector_etf,
                           "sector_above_50d": None, "sector_rs_positive": None}
    if sdf is not None and len(sdf):
        s50 = sma(sdf, 50)
        if s50 is not None:
            ctx["sector_above_50d"] = float(sdf["close"].iloc[-1]) > s50
        rs = rs_vs(sdf, spy_df, 63) if spy_df is not None else None
        if rs is not None:
            ctx["sector_rs_positive"] = rs > 0
    return ctx


def _earnings_map(pc, sc, symbols: list[str]) -> dict[str, str]:
    """symbol -> short earnings-risk label (context only). Best-effort; empty on any failure."""
    out: dict[str, str] = {}
    try:
        from src.stocks.data_collectors.earnings_calendar_collector import EarningsCalendarCollector
        summary = EarningsCalendarCollector(pc, sc).collect(symbols=symbols, include_yfinance=True)
        today = date.today()
        for ev in getattr(summary, "events", []) or []:
            try:
                d = datetime.strptime(ev.date, "%Y-%m-%d").date()
            except Exception:
                continue
            days = (d - today).days
            if 0 <= days <= 14 and (ev.symbol not in out):
                out[ev.symbol] = f"earnings in {days}d ({ev.report_time})"
    except Exception:
        pass
    return out


def scan(*, config: dict | None = None, symbols: list[str] | None = None, dry_run: bool = False,
         skip_update: bool = False, limit: int | None = None, db_path=None,
         verbose: bool = False) -> ScanResult:
    cfg = config or load_config()
    created_at = datetime.now(timezone.utc).isoformat()
    result = ScanResult(created_at=created_at, dry_run=dry_run,
                        shadow_only=bool(cfg.get("shadow_only", True)))

    # ---- lazy heavy imports (kept out of module import for offline unit tests) ----
    try:
        from src.config import load_config as load_project_config
        from src.stocks.configs.loader import load_stocks_config
        from src.stocks.data_collectors.stock_ohlcv_collector import StockOHLCVCollector
        from src.stocks.data_collectors.market_index_collector import MarketIndexCollector
        from src.stocks.data_collectors.sector_etf_collector import SectorETFCollector
    except Exception as exc:  # pragma: no cover
        result.data_notes.append(f"collector import failed: {exc}")
        shadow_store.record_scan_run(
            created_at=result.created_at, universe_size=0, scanned=0,
            candidate_count=0, rejected_count=0, persisted=0,
            market_label=None, dry_run=dry_run, data_notes=result.data_notes,
            db_path=db_path or None,
        )
        return result

    pc = load_project_config()
    sc = load_stocks_config()
    base = StockOHLCVCollector(pc, sc)

    # ---- universe ----
    uni_cfg = cfg.get("universe") or {}
    sector_map = {k.upper(): v for k, v in (cfg.get("sector_map") or {}).items()}
    explicit = [s.upper() for s in (uni_cfg.get("symbols") or [])]
    universe = [s.upper() for s in (symbols or explicit or list(getattr(sc, "default_symbols", []) or []))]
    if not uni_cfg.get("include_sector_etfs", False):
        universe = [s for s in universe if not getattr(sc, "is_etf", lambda x: False)(s)]
    universe = universe[: int(uni_cfg.get("max_symbols", 75))]
    result.universe_size = len(universe)
    if not universe:
        result.data_notes.append("empty universe")
        shadow_store.record_scan_run(
            created_at=result.created_at, universe_size=0, scanned=0,
            candidate_count=0, rejected_count=0, persisted=0,
            market_label=None, dry_run=dry_run, data_notes=result.data_notes,
            db_path=db_path or pc.db_path,
        )
        return result

    # ---- fetch (or use cache) daily bars ----
    stock_summary = market_summary = sector_summary = None
    if not skip_update:
        try:
            # daily + weekly (1wk) for the stock universe; weekly powers optional 10W/30W context
            stock_summary = base.collect(universe, ["1d", "1wk"], period="2y", throttle_seconds=0.0)
            market_summary = MarketIndexCollector(pc, sc).collect(intervals=["1d"])
            sector_summary = SectorETFCollector(pc, sc).collect(intervals=["1d"])
        except Exception as exc:
            result.data_notes.append(f"fetch failed, using cache: {exc}")
    else:
        result.data_notes.append("skip_update: using cached daily bars")

    # market frames (SPY/QQQ/VIX)
    vix_sym = getattr(sc, "volatility_index", "^VIX") or "^VIX"
    market_frames = {
        "SPY": _frame_for(market_summary, base, "SPY"),
        "QQQ": _frame_for(market_summary, base, "QQQ"),
        "VIX": _frame_for(market_summary, base, vix_sym),
    }
    market_ctx = _market_context(market_frames, cfg)
    result.market = market_ctx
    spy_df, qqq_df = market_frames["SPY"], market_frames["QQQ"]

    # sector ETF frames (keyed by ETF symbol) — union of StocksConfig ETFs + framework sector_map
    sector_frames: dict[str, Any] = {}
    for etf in set((getattr(sc, "sector_etfs", {}) or {}).values()) | set(sector_map.values()):
        sector_frames[etf] = _frame_for(sector_summary, base, etf)

    earnings = _earnings_map(pc, sc, universe)

    # ---- per-symbol detection ----
    for sym in universe:
        df = _frame_for(stock_summary, base, sym)
        if df is None or not len(df):
            result.rejected.append({"symbol": sym, "rejection_reasons": ["no daily data"]})
            continue
        # Strict data guard: a symbol with no sector-ETF mapping is SKIPPED with a reason (never
        # scanned with the sector gate silently bypassed). Missing data is a reject/skip, not a pass.
        etf = _resolve_etf(sc, sym, sector_map)
        if not etf:
            result.rejected.append({"symbol": sym, "rejection_reasons": ["no sector ETF mapping (skipped)"]})
            continue
        result.scanned += 1
        wdf = _frame_for(stock_summary, base, sym, "1wk")
        feats = compute_features(
            df, spy_df=spy_df, qqq_df=qqq_df, weekly_df=wdf,
            sector_df=sector_frames.get(etf),
            near_high_lookbacks=tuple((cfg.get("stock_filter") or {}).get(
                "near_high_lookbacks", (63, 126, 252))))
        sector_ctx = _sector_context(sc, sym, sector_frames, spy_df, sector_map=sector_map)
        cand = detect(sym, feats, market_ctx=market_ctx, sector_ctx=sector_ctx, cfg=cfg,
                      equity_usd=float(cfg.get("paper_equity_usd", 5000)),
                      earnings_risk=earnings.get(sym))
        try:
            from src.stocks.insider_context import ticker_context
            insider = ticker_context(sym, as_of=datetime.fromisoformat(created_at))
        except Exception as exc:
            insider = {"status": "unknown", "cluster_confirmed": False,
                       "reason": f"insider_context_error:{type(exc).__name__}"}
        cand["insider_context"] = insider
        if insider.get("cluster_confirmed"):
            cand.setdefault("reasons", []).append(
                f"opportunistic insider cluster: {insider.get('unique_insiders')} buyers, "
                f"${float(insider.get('purchase_value_usd') or 0):,.0f}")
        cand["status"] = SHADOW_STATUS
        cand["source_version"] = SOURCE_VERSION
        if cand.get("passed"):
            result.passed.append(cand)
        else:
            result.rejected.append({"symbol": sym,
                                    "rejection_reasons": cand.get("rejection_reasons", [])})

    result.passed.sort(key=lambda c: c.get("score", 0), reverse=True)
    if limit:
        result.passed = result.passed[: int(limit)]

    # ---- persist (never on dry-run) ----
    if not dry_run and result.passed:
        result.persisted = shadow_store.insert_candidates(
            result.passed, created_at=created_at, db_path=db_path or pc.db_path)
    elif dry_run:
        result.data_notes.append("dry-run: nothing persisted")
    shadow_store.record_scan_run(
        created_at=result.created_at, universe_size=result.universe_size,
        scanned=result.scanned, candidate_count=result.passed_count,
        rejected_count=result.rejected_count, persisted=result.persisted,
        market_label=(result.market or {}).get("label"), dry_run=dry_run,
        data_notes=result.data_notes, db_path=db_path or pc.db_path,
    )
    return result
