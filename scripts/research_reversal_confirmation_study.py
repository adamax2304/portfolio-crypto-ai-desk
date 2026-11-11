"""Read-only comparison of reversal confirmation mechanics for stock and crypto sweeps.

This is a research harness only. It reads archived market data and writes isolated
artifacts under research_labs/reversal_confirmation_study_20261012 and reports/.
It does not mutate strategy configuration, Paper ledgers, or execution routes.
"""
from __future__ import annotations

import json
import sqlite3
import statistics
from collections import defaultdict, deque
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

from src.config import load_config
from src.data_collectors import fast_flush_research_store, stocks_liquidity_shock_research_store
from src.execution import crypto_fast_flush_reclaim_paper as crypto_strategy
from src.execution import crypto_liquidity_sweep_shadow as crypto_context_strategy
from src.execution import stocks_liquidity_shock_reclaim_paper as stock_strategy
from src.execution.shadow_strategy_common import normalize_frame
from src.stocks.configs.loader import load_stocks_config


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "research_labs" / "reversal_confirmation_study_20261012"
REPORT = ROOT / "reports" / "REVERSAL_CONFIRMATION_MICROSTRUCTURE_STUDY_2026-10-12.md"
INTELLIGENCE_DB = ROOT / "data" / "intelligence" / "market_intelligence.sqlite"
NY = ZoneInfo("America/New_York")
STOCK_VARIANTS = (
    "base_held_2x1m", "fast_1x1m", "vol_reclaim_1x1m",
    "higher_low_break_vol", "held_2x1m_with_vol", "anchored_vwap_reclaim",
    "confirm_1x5m",
)
CRYPTO_VARIANTS = (
    "base_fast_1x1m", "vol_reclaim_1x1m", "higher_low_break_vol",
    "held_2x1m", "confirm_1x5m",
)


def _read_only(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn


def _resample(frame: pd.DataFrame, minutes: int) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    work = normalize_frame(frame).set_index("timestamp")
    result = work.resample(f"{minutes}min", label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    ).dropna(subset=["open", "high", "low", "close"]).reset_index()
    return normalize_frame(result)


def _with_relative_volume(frame: pd.DataFrame, *, stock_session_clock: bool) -> pd.DataFrame:
    work = normalize_frame(frame).copy()
    work["volume"] = pd.to_numeric(work["volume"], errors="coerce").fillna(0.0)
    if stock_session_clock and not work.empty:
        local = pd.DatetimeIndex(work["timestamp"]).tz_convert(NY)
        work["_slot"] = local.hour * 60 + local.minute
        median = work.groupby("_slot", sort=False)["volume"].transform(
            lambda values: values.shift(1).rolling(20, min_periods=5).median()
        )
    else:
        median = work["volume"].shift(1).rolling(20, min_periods=5).median()
    work["_rvol_confirm"] = work["volume"] / median.where(median > 0)
    return work


def _candle_valid(candle: pd.Series, level: float, *, close_location: float = 0.60,
                  require_green: bool = True) -> bool:
    try:
        open_, high, low, close = (float(candle[key]) for key in ("open", "high", "low", "close"))
    except (TypeError, ValueError, KeyError):
        return False
    loc = (close - low) / max(high - low, 1e-12)
    return close >= level and loc >= close_location and (not require_green or close > open_)


def _confirmation(minute: pd.DataFrame, setup: dict[str, Any], variant: str,
                  *, window_minutes: int, stock_clock: bool) -> dict[str, Any] | None:
    if minute.empty:
        return None
    decision = pd.Timestamp(setup["decision_at"])
    end = decision + pd.Timedelta(minutes=window_minutes)
    work = (minute if "_rvol_confirm" in minute.columns
            else _with_relative_volume(minute, stock_session_clock=stock_clock))
    left = int(work["timestamp"].searchsorted(decision, side="left"))
    right = int(work["timestamp"].searchsorted(end - pd.Timedelta(minutes=1), side="right"))
    eligible = work.iloc[left:right]
    if eligible.empty:
        return None
    level = float(setup["reclaim_level"])
    valid_rows: list[tuple[int, pd.Series]] = []
    for index, candle in eligible.iterrows():
        close_at = pd.Timestamp(candle["timestamp"]) + pd.Timedelta(minutes=1)
        rvol = float(candle["_rvol_confirm"]) if pd.notna(candle["_rvol_confirm"]) else 0.0
        if variant in {"base_held_2x1m", "held_2x1m", "held_2x1m_with_vol"}:
            first = valid_rows[-1] if valid_rows else None
            valid = _candle_valid(candle, level)
            if first is not None:
                prior = first[1]
                adjacent = pd.Timestamp(candle["timestamp"]) - pd.Timestamp(prior["timestamp"]) == pd.Timedelta(minutes=1)
                confirms = (adjacent and _candle_valid(prior, level)
                            and float(candle["close"]) > float(prior["close"])
                            and float(candle["high"]) >= float(prior["high"]))
                if confirms and (variant != "held_2x1m_with_vol"
                                 or max(float(prior["_rvol_confirm"] or 0.0), rvol) >= 1.50):
                    return {"entry": float(candle["close"]), "entry_at": close_at,
                            "delay_seconds": (close_at - decision).total_seconds(), "rvol": rvol}
            valid_rows = [(int(index), candle)] if valid else []
            continue
        if variant == "fast_1x1m" or variant == "base_fast_1x1m":
            valid = _candle_valid(candle, level)
        elif variant == "vol_reclaim_1x1m":
            valid = _candle_valid(candle, level, close_location=0.70) and rvol >= 1.50
        elif variant == "higher_low_break_vol":
            position = int(work["timestamp"].searchsorted(candle["timestamp"], side="left"))
            previous = work.iloc[max(0, position - 1):position]
            valid = _candle_valid(candle, level, close_location=0.65)
            if valid and not previous.empty:
                prior = previous.iloc[0]
                valid = float(candle["low"]) > float(setup["sweep_extreme"])
                valid = valid and float(candle["close"]) > float(prior["high"])
                valid = valid and rvol >= 1.20
            else:
                valid = False
        elif variant == "anchored_vwap_reclaim":
            valid = _candle_valid(candle, level, close_location=0.65)
            start = pd.Timestamp(setup.get("shock_at", setup.get("sweep_at")))
            anchor_left = int(work["timestamp"].searchsorted(start, side="left"))
            anchor_right = int(work["timestamp"].searchsorted(close_at, side="left"))
            anchor = work.iloc[anchor_left:anchor_right]
            vol = pd.to_numeric(anchor["volume"], errors="coerce").fillna(0.0)
            if valid and float(vol.sum()) > 0:
                typical = (anchor["high"] + anchor["low"] + anchor["close"]) / 3.0
                anchored_vwap = float((typical * vol).sum() / vol.sum())
                valid = float(candle["close"]) > anchored_vwap
            else:
                valid = False
        else:
            valid = False
        if valid:
            return {"entry": float(candle["close"]), "entry_at": close_at,
                    "delay_seconds": (close_at - decision).total_seconds(), "rvol": rvol}
    return None


def _confirmation_5m(minute: pd.DataFrame, setup: dict[str, Any], *, window_minutes: int,
                     stock_clock: bool, already_5m: bool = False) -> dict[str, Any] | None:
    bars = (minute if "_rvol_confirm" in minute.columns else
            _with_relative_volume(minute if already_5m else _resample(minute, 5),
                                  stock_session_clock=stock_clock))
    if bars.empty:
        return None
    decision = pd.Timestamp(setup["decision_at"])
    end = decision + pd.Timedelta(minutes=window_minutes)
    left = int(bars["timestamp"].searchsorted(decision, side="left"))
    right = int(bars["timestamp"].searchsorted(end - pd.Timedelta(minutes=5), side="right"))
    rows = bars.iloc[left:right]
    for _, candle in rows.iterrows():
        rvol = float(candle["_rvol_confirm"]) if pd.notna(candle["_rvol_confirm"]) else 0.0
        if _candle_valid(candle, float(setup["reclaim_level"]), close_location=0.70) and rvol >= 1.25:
            close_at = pd.Timestamp(candle["timestamp"]) + pd.Timedelta(minutes=5)
            return {"entry": float(candle["close"]), "entry_at": close_at,
                    "delay_seconds": (close_at - decision).total_seconds(), "rvol": rvol}
    return None


def _stock_daily_frame(symbol: str) -> pd.DataFrame:
    path = ROOT / "data" / "raw" / "stocks" / "1d" / f"{symbol.upper()}.csv"
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(path)
    if frame.empty:
        return frame
    if "timestamp" not in {str(col).lower() for col in frame.columns}:
        frame = frame.rename(columns={str(frame.columns[0]): "timestamp"})
    frame.columns = [str(col).lower() for col in frame.columns]
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    return frame.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)


def _stock_adv(daily: pd.DataFrame, at: datetime) -> float | None:
    if daily.empty:
        return None
    end = int(daily["timestamp"].searchsorted(pd.Timestamp(at), side="left"))
    visible = daily.iloc[max(0, end - 30):end]
    if len(visible) < 10:
        return None
    values = (pd.to_numeric(visible["close"], errors="coerce")
              * pd.to_numeric(visible["volume"], errors="coerce")).dropna()
    return float(values.mean()) if len(values) else None


def _stock_drop_map(frame: pd.DataFrame) -> dict[pd.Timestamp, float]:
    work = normalize_frame(frame)
    prior = work["close"].shift(1)
    drop = ((prior - work["low"]) / prior.replace(0, pd.NA) * 100.0).clip(lower=0)
    return {pd.Timestamp(ts): float(value) for ts, value in zip(work["timestamp"], drop)
            if pd.notna(value)}


def _stock_setup(frame: pd.DataFrame, index: int, market_drops: dict[pd.Timestamp, float],
                 sector_drops: dict[pd.Timestamp, float], adv: float | None,
                 interval: int, cfg: dict[str, Any]) -> dict[str, Any] | None:
    work = frame
    if index < max(int(cfg["level_lookback_bars"]), int(cfg["atr_periods"]), int(cfg["volume_lookback_bars"])):
        return None
    row = work.iloc[index]
    at = pd.Timestamp(row["timestamp"])
    decision = at + pd.Timedelta(minutes=interval)
    prior_close = float(work.iloc[index - 1]["close"])
    prior = work.iloc[index - int(cfg["level_lookback_bars"]):index]
    level = float(prior["low"].min())
    low, high, close, volume = (float(row[key]) for key in ("low", "high", "close", "volume"))
    atr = stock_strategy._atr(work, index - 1, int(cfg["atr_periods"]))
    if not atr or atr <= 0 or prior_close <= 0:
        return None
    flush = max(0.0, prior_close - low)
    flush_atr = flush / atr
    flush_pct = flush / prior_close * 100.0
    prior_vol = float(work.iloc[index - int(cfg["volume_lookback_bars"]):index]["volume"].median())
    rvol = volume / prior_vol if prior_vol > 0 else 0.0
    breach = max(0.0, level - low) / atr
    market_drop = market_drops.get(at)
    sector_drop = sector_drops.get(at)
    context_drop = max(float(market_drop or 0.0), float(sector_drop or 0.0))
    idio = flush_pct - context_drop
    bar_dollar = close * volume
    minimum_bar_dollars = 1_500_000.0 * interval / 15.0
    min_pct = {15: 0.80, 5: 0.40, 1: 0.20}[interval]
    min_rvol = {15: 1.20, 5: 1.20, 1: 2.00}[interval]
    min_idio = 0.20 if interval == 15 else 0.15
    if not stock_strategy._allowed_window(decision.to_pydatetime(), cfg):
        return None
    if close < 5.0 or adv is None or adv < float(cfg["min_avg_dollar_volume_30d"]):
        return None
    if bar_dollar < minimum_bar_dollars or not 1.10 <= flush_atr <= 3.50:
        return None
    if flush_pct < min_pct or rvol < min_rvol or breach < 0.15:
        return None
    if market_drop is None or market_drop > 0.60 or (sector_drop is not None and sector_drop > 1.10):
        return None
    if idio < min_idio:
        return None
    reclaim = max(level, low + (prior_close - low) * 0.40)
    return {"decision_at": decision.to_pydatetime(), "shock_at": at.to_pydatetime(),
            "sweep_extreme": low, "shock_extreme": low, "prior_close": prior_close,
            "structural_level": level, "atr": float(atr), "flush_atr": flush_atr,
            "flush_pct": flush_pct, "rvol": rvol, "level_breach_atr": breach,
            "market_drop_pct": market_drop, "sector_drop_pct": sector_drop,
            "idiosyncratic_drop_pct": idio, "bar_dollar_volume": bar_dollar,
            "avg_dollar_volume_30d": adv, "reclaim_level": reclaim,
            "stop": low - float(atr) * 0.10, "direction": "long"}


def _stock_potential_indices(frame: pd.DataFrame, interval: int) -> list[int]:
    work = normalize_frame(frame)
    if work.empty:
        return []
    close = pd.to_numeric(work["close"], errors="coerce")
    high = pd.to_numeric(work["high"], errors="coerce")
    low = pd.to_numeric(work["low"], errors="coerce")
    volume = pd.to_numeric(work["volume"], errors="coerce").fillna(0.0)
    previous = close.shift(1)
    true_range = pd.concat([(high - low), (high - previous).abs(), (low - previous).abs()], axis=1).max(axis=1)
    atr = true_range.rolling(14, min_periods=14).mean().shift(1)
    flush = (previous - low).clip(lower=0)
    flush_atr = flush / atr
    flush_pct = flush / previous * 100.0
    prior_volume = volume.shift(1).rolling(20, min_periods=20).median()
    rvol = volume / prior_volume.where(prior_volume > 0)
    prior_low = low.shift(1).rolling(8, min_periods=8).min()
    breach = (prior_low - low).clip(lower=0) / atr
    minimum_bar_dollars = 1_500_000.0 * interval / 15.0
    min_pct = {15: 0.80, 5: 0.40, 1: 0.20}[interval]
    min_rvol = {15: 1.20, 5: 1.20, 1: 2.00}[interval]
    mask = (close >= 5.0) & (close * volume >= minimum_bar_dollars)
    mask &= flush_atr.between(1.10, 3.50) & (flush_pct >= min_pct)
    mask &= (rvol >= min_rvol) & (breach >= 0.15)
    return [int(index) for index in work.index[mask.fillna(False)]]


def _outcome_stock(symbol: str, setup: dict[str, Any], minute: pd.DataFrame,
                   confirmation: dict[str, Any], cfg: dict[str, Any],
                   profile: dict[str, Any], base_history: pd.DataFrame) -> dict[str, Any] | None:
    entry_at = pd.Timestamp(confirmation["entry_at"])
    geometry = stock_strategy.entry_geometry(
        setup, float(confirmation["entry"]), cfg, profile=profile,
        history=base_history,
    )
    if not geometry.get("ok"):
        return None
    future = minute[minute["timestamp"] >= entry_at].copy()
    if future.empty:
        return None
    local_date = entry_at.tz_convert(NY).date()
    future = future[(future["timestamp"].map(lambda ts: ts.tz_convert(NY).date() == local_date))
                    & (future["timestamp"] < entry_at + pd.Timedelta(minutes=60))].iloc[:60]
    if future.empty:
        return None
    outcome = stock_strategy.simulate_two_target(
        entry=float(confirmation["entry"]), stop=float(geometry["stop"]),
        tp1=float(geometry["tp1"]), tp2=float(geometry["tp2"]),
        candles=future, symbol=symbol, cfg=cfg, force_close=True,
    )
    if outcome.get("outcome_status") != "closed":
        return None
    return {**outcome, "entry": float(confirmation["entry"]),
            "entry_at": entry_at.to_pydatetime(),
            "decision_at": setup["decision_at"], "event_at": setup["shock_at"],
            "delay_seconds": float(confirmation["delay_seconds"]),
            "entry_rvol": float(confirmation.get("rvol") or 0.0),
            "stop_distance_pct": geometry.get("stop_distance_pct"),
            "flush_atr": setup["flush_atr"], "flush_pct": setup["flush_pct"],
            "event_rvol": setup["rvol"], "idiosyncratic_drop_pct": setup["idiosyncratic_drop_pct"]}


def _scan_stocks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg = stock_strategy.load_strategy_config()
    stock_cfg = load_stocks_config(ROOT)
    symbols = stock_strategy.configured_symbols(cfg)
    db = _read_only(stocks_liquidity_shock_research_store.DEFAULT_PATH)
    trading = _read_only(load_config(ROOT).db_path)
    rows: list[dict[str, Any]] = []
    coverage = {"symbols_requested": len(symbols), "symbols_with_bars": 0,
                "shock_setups": 0, "news_blocked": 0, "timeframes": {}}
    try:
        spy_1m = stocks_liquidity_shock_research_store.load_frame(db, "SPY", "1m")
        sector_symbols = sorted(set(stock_cfg.sector_etfs.values()))
        context_1m = {"SPY": spy_1m}
        context_1m.update({etf: stocks_liquidity_shock_research_store.load_frame(db, etf, "1m")
                           for etf in sector_symbols})
        market15 = stocks_liquidity_shock_research_store.load_frame(db, "SPY", "15m")
        sector15 = {etf: stocks_liquidity_shock_research_store.load_frame(db, etf, "15m")
                    for etf in sector_symbols}
        minute_by_symbol: dict[str, pd.DataFrame] = {}
        daily_by_symbol: dict[str, pd.DataFrame] = {}
        base15_by_symbol: dict[str, pd.DataFrame] = {}
        for pos, symbol in enumerate(symbols, start=1):
            minute = stocks_liquidity_shock_research_store.load_frame(db, symbol, "1m")
            if minute.empty:
                continue
            minute_by_symbol[symbol] = _with_relative_volume(minute, stock_session_clock=True)
            confirm5_by_symbol = None
            daily_by_symbol[symbol] = _stock_daily_frame(symbol)
            base15_by_symbol[symbol] = stocks_liquidity_shock_research_store.load_frame(db, symbol, "15m")
            coverage["symbols_with_bars"] += 1
            sector_etf = stock_cfg.sector_etf_for(symbol)
            for minutes in (15, 5, 1):
                base = (base15_by_symbol[symbol]
                        if minutes == 15 else _resample(minute, minutes))
                market = (market15
                          if minutes == 15 else _resample(context_1m["SPY"], minutes))
                sector_raw = context_1m.get(sector_etf, pd.DataFrame())
                sector = (sector15.get(sector_etf, pd.DataFrame())
                          if minutes == 15 else _resample(sector_raw, minutes))
                if base.empty or market.empty:
                    continue
                market_drops = _stock_drop_map(market)
                sector_drops = _stock_drop_map(sector) if not sector.empty else {}
                minute_scan = minute_by_symbol[symbol]
                if confirm5_by_symbol is None:
                    confirm5_by_symbol = _with_relative_volume(_resample(minute_scan, 5), stock_session_clock=True)
                for idx in _stock_potential_indices(base, minutes):
                    at = base.iloc[idx]["timestamp"].to_pydatetime()
                    adv = _stock_adv(daily_by_symbol[symbol], at)
                    setup = _stock_setup(base, idx, market_drops, sector_drops, adv, minutes, cfg)
                    if setup is None:
                        continue
                    coverage["shock_setups"] += 1
                    news = stock_strategy.news_risk(trading, symbol, setup["decision_at"], cfg)
                    if news.get("blocked"):
                        coverage["news_blocked"] += 1
                        continue
                    profile = dict(cfg["confirmation_profiles"]["HELD_1M_RECLAIM"])
                    # The profile's 15m thresholds are normalized to each detector horizon above.
                    history = base.iloc[max(0, idx - 100):idx + 1].copy()
                    for variant in STOCK_VARIANTS:
                        if variant == "confirm_1x5m":
                            confirmation = _confirmation_5m(
                                confirm5_by_symbol, setup, window_minutes=15,
                                stock_clock=True, already_5m=True,
                            )
                        else:
                            window = 12 if variant in {"base_held_2x1m", "held_2x1m_with_vol"} else 8
                            confirmation = _confirmation(
                                minute_scan, setup, variant, window_minutes=window,
                                stock_clock=True,
                            )
                        if confirmation is None:
                            continue
                        outcome = _outcome_stock(symbol, setup, minute_scan, confirmation,
                                                cfg, profile, history)
                        if outcome is not None:
                            rows.append({"asset_class": "stocks", "variant": variant,
                                         "base_timeframe": f"{minutes}m", "symbol": symbol,
                                         "sector": sector_etf or "unknown", **outcome})
                key = f"{minutes}m"
                coverage["timeframes"][key] = coverage["timeframes"].get(key, 0) + len(base)
            if pos % 15 == 0:
                print(f"stocks: {pos}/{len(symbols)} symbols; {len(rows)} replay rows", flush=True)
    finally:
        db.close()
        trading.close()
    return rows, coverage


def _stock_drop_pct(row: pd.Series) -> float:
    return float(row["flush_pct"])


def _crypto_load_bar_frames(conn: sqlite3.Connection, symbol: str,
                            preferred_exchange: str | None = None) -> tuple[pd.DataFrame, str | None]:
    frames: list[tuple[int, int, str, pd.DataFrame]] = []
    exchanges = (preferred_exchange,) if preferred_exchange else ("bybit", "binance")
    for exchange in exchanges:
        raw = conn.execute(
            "SELECT ts,open,high,low,close,volume FROM ohlcv_1m "
            "WHERE exchange=? AND symbol=? ORDER BY ts", (exchange, symbol.upper()),
        ).fetchall()
        if not raw:
            continue
        frame = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
        frame = normalize_frame(frame)
        frames.append((int(frame["timestamp"].iloc[-1].timestamp()), len(frame), exchange, frame))
    if not frames:
        return pd.DataFrame(), None
    _, _, exchange, frame = max(frames, key=lambda item: (item[0], item[1], item[2] == "bybit"))
    return frame, exchange


def _clip_crypto_bar_window(frame: pd.DataFrame, start_ms: int, end_ms: int) -> pd.DataFrame:
    if frame.empty:
        return frame
    start = pd.to_datetime(start_ms, unit="ms", utc=True)
    end = pd.to_datetime(end_ms, unit="ms", utc=True)
    return frame[(frame["timestamp"] >= start) & (frame["timestamp"] <= end)].reset_index(drop=True)


def _crypto_liquidations(conn: sqlite3.Connection, symbols: list[str], start: str) -> dict[str, list[tuple[datetime, float]]]:
    result: dict[str, list[tuple[datetime, float]]] = {}
    for display in symbols:
        normalized = display.replace("/", "").upper()
        found = conn.execute(
            "SELECT event_at,side,notional_usd FROM liquidation_events "
            "WHERE normalized_symbol=? AND exchange IN ('binance','bybit') AND event_at>=? "
            "ORDER BY event_at", (normalized, start),
        ).fetchall()
        grouped: dict[int, float] = defaultdict(float)
        for row in found:
            if str(row["side"]).upper() != "SELL":
                continue
            at = datetime.fromisoformat(str(row["event_at"]).replace("Z", "+00:00")).astimezone(timezone.utc)
            minute_bucket = int(at.timestamp() // 60) * 60
            grouped[minute_bucket] += float(row["notional_usd"] or 0.0)
        result[display] = [(datetime.fromtimestamp(ts, timezone.utc), amount)
                          for ts, amount in sorted(grouped.items())]
    return result


def _depth_imbalance(conn: sqlite3.Connection, symbol: str, at: datetime) -> tuple[float | None, float | None]:
    normalized = symbol.replace("/", "").upper()
    cutoff = (at - timedelta(minutes=12)).isoformat()
    rows = conn.execute(
        "SELECT exchange,provider_ts,spread_bps,bid_depth_10bps_usd,ask_depth_10bps_usd "
        "FROM liquidity_snapshots WHERE normalized_symbol=? AND provider_ts>=? AND provider_ts<=? "
        "AND quality_status='ok' ORDER BY provider_ts DESC,id DESC",
        (normalized, cutoff, at.isoformat()),
    ).fetchall()
    newest: dict[str, sqlite3.Row] = {}
    for row in rows:
        newest.setdefault(str(row["exchange"]), row)
    if not newest:
        return None, None
    spreads = [float(row["spread_bps"]) for row in newest.values() if row["spread_bps"] is not None]
    bids = sum(float(row["bid_depth_10bps_usd"] or 0.0) for row in newest.values())
    asks = sum(float(row["ask_depth_10bps_usd"] or 0.0) for row in newest.values())
    imbalance = (bids - asks) / (bids + asks) if bids + asks > 0 else None
    return (statistics.median(spreads) if spreads else None), imbalance


def _crypto_scan(*, preferred_exchange: str | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg = crypto_strategy.load_strategy_config()
    fast_profile = dict(cfg["confirmation_profiles"]["FAST_1M_RECLAIM"])
    archive = _read_only(fast_flush_research_store.DEFAULT_PATH)
    intelligence = _read_only(INTELLIGENCE_DB)
    symbols = [str(row[0]) for row in archive.execute(
        "SELECT symbol FROM candidate_events GROUP BY symbol ORDER BY COUNT(*) DESC LIMIT 40"
    )]
    bars: dict[str, pd.DataFrame] = {}
    venues: dict[str, str] = {}
    liqs = _crypto_liquidations(intelligence, symbols, "2026-09-12T00:00:00+00:00")
    rows: list[dict[str, Any]] = []
    coverage: dict[str, Any] = {"symbols": len(symbols), "symbols_with_bars": 0,
                                "ohlcv_period": None,
                                "liquidation_bins": 0, "contexts_available": 0,
                                "context_missing": 0, "base_candidates": {}}
    try:
        start_ms = int(datetime(2026, 9, 12, tzinfo=timezone.utc).timestamp() * 1000)
        end_ms = int(datetime(2026, 10, 13, tzinfo=timezone.utc).timestamp() * 1000)
        for symbol in symbols:
            frame, venue = _crypto_load_bar_frames(archive, symbol, preferred_exchange)
            if frame.empty:
                continue
            frame = _clip_crypto_bar_window(frame, start_ms, end_ms)
            if frame.empty:
                continue
            bars[symbol] = frame
            venues[symbol] = str(venue)
            coverage["symbols_with_bars"] += 1
        if bars:
            first_bar = min(frame["timestamp"].iloc[0] for frame in bars.values())
            last_bar = max(frame["timestamp"].iloc[-1] for frame in bars.values())
            coverage["ohlcv_period"] = [first_bar.isoformat(), last_bar.isoformat()]
        candidate_profiles = {
            "strict_fast": {"min_flush_atr": 1.25, "max_flush_atr": 3.25,
                            "min_flush_pct": 0.75, "max_flush_pct": 2.50,
                            "min_rvol": 1.05, "min_oi_drop_pct": 0.50,
                            "max_oi_drop_pct": 3.00, "min_liquidation_percentile": 0.90,
                            "sessions": {"us"}, "min_stop_distance_pct": 0.010,
                            "max_stop_distance_pct": 0.015},
            "medium_deep": {"min_flush_atr": 2.00, "max_flush_atr": 5.00,
                            "min_flush_pct": 1.50, "max_flush_pct": 2.75,
                            "min_rvol": 1.00, "min_oi_drop_pct": 0.25,
                            "max_oi_drop_pct": 5.00, "min_liquidation_percentile": 0.90,
                            "sessions": {"europe", "us"}, "min_stop_distance_pct": 0.0075,
                            "max_stop_distance_pct": 0.015},
        }
        coverage["liquidation_bins"] = sum(len(liqs.get(symbol, [])) for symbol in symbols)
        for base_minutes in (5, 1):
            candidates: list[dict[str, Any]] = []
            bucket_seconds = base_minutes * 60
            for symbol in symbols:
                minute = bars.get(symbol)
                if minute is None or minute.empty:
                    continue
                minute = _with_relative_volume(minute, stock_session_clock=False)
                base = _resample(minute, base_minutes)
                if base.empty:
                    continue
                base = base.reset_index(drop=True)
                five_minute = _with_relative_volume(_resample(minute, 5), stock_session_clock=False)
                idx_by_ts = {int(pd.Timestamp(ts).timestamp()): idx
                             for idx, ts in enumerate(base["timestamp"])}
                # Rolling liquidation percentile uses only prior 14-day event bins.
                historical: deque[tuple[int, float]] = deque()
                event_map: dict[int, float] = defaultdict(float)
                for event_at, amount in liqs.get(symbol, []):
                    ts = int(event_at.timestamp())
                    event_bucket = ts - ts % bucket_seconds
                    event_map[event_bucket] += amount
                for bucket, notional in sorted(event_map.items()):
                    at = datetime.fromtimestamp(bucket, timezone.utc)
                    while historical and historical[0][0] < bucket - 14 * 86400:
                        historical.popleft()
                    prior_amounts = [amount for _, amount in historical]
                    percentile = (sum(value <= notional for value in prior_amounts) / len(prior_amounts)
                                  if len(prior_amounts) >= 10 else 0.0)
                    historical.append((bucket, notional))
                    if at < datetime(2026, 9, 29, tzinfo=timezone.utc) or notional < 20_000 or percentile < 0.90:
                        continue
                    index = idx_by_ts.get(bucket)
                    if index is None or index < 21:
                        continue
                    decision = at + timedelta(minutes=base_minutes)
                    # Price-only preliminary gate avoids querying derivative snapshots on non-setups.
                    dummy = {"ok": True, "oi_change_pct": -1.0, "spread_bps": 0.1}
                    permissive = dict(cfg)
                    permissive.update(
                        min_flush_atr=0.0, max_flush_atr=100.0, min_flush_pct=0.0,
                        min_rvol=0.0, min_liquidation_notional_usd=0.0,
                        min_liquidation_percentile=0.0, min_liquidation_history_episodes=0,
                        min_oi_drop_pct=-1000.0, max_oi_drop_pct=1000.0,
                        max_spread_bps=100_000.0, allowed_sessions=["asia", "europe", "us", "off"],
                    )
                    event_rows = [{"side": "SELL", "notional_usd": notional, "event_at": at.isoformat()}]
                    setup = crypto_strategy.detect_flush(
                        base, index, event_rows, dummy, permissive,
                        liquidation_percentile=percentile, liquidation_history_count=len(prior_amounts),
                    )
                    if not setup.get("ok"):
                        continue
                    setup["decision_at"] = decision
                    setup["sweep_at"] = at
                    setup["liquidation_percentile"] = percentile
                    union_session = crypto_strategy._session(decision)  # noqa: SLF001
                    if union_session not in {"europe", "us"}:
                        continue
                    if not (1.25 <= float(setup["flush_atr"]) <= 5.0
                            and 0.45 <= float(setup["flush_pct"]) <= 2.75
                            and float(setup["rvol"]) >= 1.0):
                        continue
                    setup["liquidation_notional_usd"] = notional
                    # The 1m detector's candidate decision is the closed minute, not the shared 5m default.
                    context = crypto_context_strategy._contexts(intelligence, symbol, decision, permissive)  # noqa: SLF001
                    if not context.get("ok"):
                        coverage["context_missing"] += 1
                        continue
                    coverage["contexts_available"] += 1
                    spread, depth = _depth_imbalance(intelligence, symbol, decision)
                    if spread is not None:
                        context["spread_bps"] = spread
                    setup["oi_change_pct"] = float(context.get("oi_change_pct"))
                    setup["spread_bps"] = spread if spread is not None else context.get("spread_bps")
                    setup["depth_imbalance"] = depth
                    setup["liquidation_percentile"] = percentile
                    setup["decision_at"] = decision
                    setup["sweep_at"] = at
                    candidates.append({"symbol": symbol, "base": base, "minute": minute,
                                       "five_minute": five_minute,
                                       "setup": setup, "base_minutes": base_minutes,
                                       "venue": venues[symbol], "notional": notional,
                                       "depth_imbalance": depth, "spread": setup["spread_bps"]})
            coverage["base_candidates"][f"{base_minutes}m"] = len(candidates)
            for candidate in candidates:
                symbol, minute, setup = candidate["symbol"], candidate["minute"], candidate["setup"]
                decision = setup["decision_at"]
                for cohort_name, gate in candidate_profiles.items():
                    session = crypto_strategy._session(decision)  # noqa: SLF001
                    if session not in gate["sessions"]:
                        continue
                    if not (gate["min_flush_atr"] <= float(setup["flush_atr"]) <= gate["max_flush_atr"]):
                        continue
                    if not (gate["min_flush_pct"] <= float(setup["flush_pct"]) <= gate["max_flush_pct"]):
                        continue
                    if float(setup["rvol"]) < gate["min_rvol"]:
                        continue
                    if not gate["min_liquidation_percentile"] <= float(setup["liquidation_percentile"]):
                        continue
                    if setup.get("spread_bps") is None or float(setup["spread_bps"]) > 18.0:
                        continue
                    oi = float(setup["oi_change_pct"])
                    # Compare no OI gate to the profile gate using the same observed event/context set.
                    oi_pass = -gate["max_oi_drop_pct"] <= oi <= -gate["min_oi_drop_pct"]
                    confirmation_variants = list(CRYPTO_VARIANTS)
                    for variant in confirmation_variants:
                        window = 8 if variant != "held_2x1m" else 12
                        confirmation = (_confirmation_5m(candidate["five_minute"], setup, window_minutes=20,
                                                         stock_clock=False, already_5m=True)
                                        if variant == "confirm_1x5m" else
                                        _confirmation(minute, setup, variant,
                                                      window_minutes=window, stock_clock=False))
                        if confirmation is None:
                            continue
                        geometry_profile = {
                            "min_stop_distance_pct": gate["min_stop_distance_pct"],
                            "max_stop_distance_pct": gate["max_stop_distance_pct"],
                            "target_policy": "fixed_r", "target_r": [0.80, 1.35],
                        }
                        geometry = crypto_strategy.entry_geometry(
                            setup, float(confirmation["entry"]), cfg, profile=geometry_profile,
                            frame=minute, entry_at=confirmation["entry_at"],
                        )
                        if not geometry.get("ok"):
                            continue
                        entry_at = pd.Timestamp(confirmation["entry_at"])
                        future = minute[(minute["timestamp"] >= entry_at)
                                        & (minute["timestamp"] < entry_at + pd.Timedelta(minutes=45))]
                        if future.empty:
                            continue
                        outcome = crypto_strategy.simulate_two_target(
                            entry=float(confirmation["entry"]), stop=float(geometry["stop"]),
                            tp1=float(geometry["tp1"]), tp2=float(geometry["tp2"]),
                            candles=future, symbol=symbol, cfg=cfg, bar_minutes=1, force_close=True,
                        )
                        if outcome.get("outcome_status") != "closed":
                            continue
                        base_row = {"asset_class": "crypto", "variant": variant,
                                    "cohort": cohort_name + "_no_oi_gate", "base_timeframe": f"{candidate['base_minutes']}m",
                                    "symbol": symbol, "venue": candidate["venue"],
                                    "event_at": setup["sweep_at"], "decision_at": decision,
                                    "entry_at": entry_at.to_pydatetime(),
                                    "delay_seconds": float(confirmation["delay_seconds"]),
                                    "entry_rvol": float(confirmation.get("rvol") or 0.0),
                                    "flush_atr": setup["flush_atr"], "flush_pct": setup["flush_pct"],
                                    "event_rvol": setup["rvol"], "oi_change_pct": oi,
                                    "oi_gate_pass": oi_pass, "spread_bps": setup.get("spread_bps"),
                                    "depth_imbalance": candidate["depth_imbalance"],
                                    "liquidation_percentile": setup["liquidation_percentile"],
                                    **outcome}
                        rows.append(base_row)
                        if oi_pass:
                            rows.append({**base_row, "cohort": cohort_name + "_oi_gate"})
                        if candidate["depth_imbalance"] is not None and candidate["depth_imbalance"] > 0:
                            rows.append({**base_row, "cohort": cohort_name + "_positive_depth"})
                            if oi_pass:
                                rows.append({**base_row, "cohort": cohort_name + "_oi_positive_depth"})
            print(f"crypto: {base_minutes}m setups={len(candidates)}; total replay rows={len(rows)}", flush=True)
    finally:
        archive.close()
        intelligence.close()
    return rows, coverage


def _drawdown(values: list[float]) -> float:
    equity = peak = dd = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        dd = max(dd, peak - equity)
    return dd


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    rows = sorted(rows, key=lambda row: row["entry_at"])
    pnl = [float(row["net_pnl_usd"]) for row in rows]
    wins = sum(value for value in pnl if value > 0)
    losses = -sum(value for value in pnl if value < 0)
    return {"trades": len(rows), "net_usd": round(sum(pnl), 2),
            "net_r": round(sum(float(row["net_r"]) for row in rows), 3),
            "pf": round(wins / losses, 3) if losses else (None if not wins else "inf"),
            "winrate_pct": round(100.0 * sum(value > 0 for value in pnl) / len(pnl), 1) if pnl else 0.0,
            "max_drawdown_usd": round(_drawdown(pnl), 2),
            "median_entry_delay_sec": round(statistics.median(float(row["delay_seconds"]) for row in rows), 1) if rows else None,
            "median_rvol_at_confirm": round(statistics.median(float(row.get("entry_rvol") or 0.0) for row in rows), 3) if rows else None,
            "median_mfe_r": round(statistics.median(float(row.get("mfe_r") or 0.0) for row in rows), 3) if rows else None,
            "median_mae_r": round(statistics.median(float(row.get("mae_r") or 0.0) for row in rows), 3) if rows else None,
            "costs_usd": round(sum(float(row.get("fees_usd") or 0.0) + float(row.get("slippage_usd") or 0.0) for row in rows), 2)}


def _independent(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_symbol_day: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for row in sorted(rows, key=lambda value: value["entry_at"]):
        at = row["entry_at"]
        if isinstance(at, pd.Timestamp):
            at = at.to_pydatetime()
        if at.tzinfo is None:
            at = at.replace(tzinfo=timezone.utc)
        session_date = at.astimezone(NY).date().isoformat() if row["asset_class"] == "stocks" else at.date().isoformat()
        key = (row["asset_class"], row.get("base_timeframe", ""), row["variant"],
               row["symbol"] + "|" + session_date)
        by_symbol_day.setdefault(key, row)
    selected = list(by_symbol_day.values())
    by_market_time: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in selected:
        decision = row.get("decision_at") or row["event_at"]
        if isinstance(decision, pd.Timestamp):
            decision = decision.to_pydatetime()
        minutes = 15 if row["asset_class"] == "stocks" and row.get("base_timeframe") == "15m" else 5
        bucket_minute = decision.minute - decision.minute % minutes
        bucket = decision.replace(minute=bucket_minute, second=0, microsecond=0).isoformat()
        by_market_time[(row["asset_class"], row.get("base_timeframe", ""), row["variant"], bucket)].append(row)
    capped: list[dict[str, Any]] = []
    for group in by_market_time.values():
        capped.extend(sorted(group, key=lambda row: float(row.get("flush_atr") or 0.0), reverse=True)[:3])
    return sorted(capped, key=lambda row: row["entry_at"])


def _to_iso(value: Any) -> str:
    if isinstance(value, pd.Timestamp):
        value = value.to_pydatetime()
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def _pack_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    packed = []
    for row in rows:
        packed.append({key: _to_iso(value) if isinstance(value, (datetime, pd.Timestamp)) else value
                       for key, value in row.items()})
    return packed


def _results(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["asset_class"], row.get("base_timeframe", ""), row["variant"],
                row.get("cohort", ""))].append(row)
    results: dict[str, Any] = {}
    for key, values in sorted(groups.items()):
        thinned = _independent(values)
        event_dates = sorted({(row["event_at"].date() if isinstance(row["event_at"], datetime)
                               else pd.Timestamp(row["event_at"]).date()) for row in values})
        split_date = event_dates[int((len(event_dates) - 1) * 0.70)] if event_dates else None
        train = [row for row in thinned if (row["event_at"].date() if isinstance(row["event_at"], datetime)
                                                  else pd.Timestamp(row["event_at"]).date()) <= split_date] if split_date else []
        test = [row for row in thinned if (row["event_at"].date() if isinstance(row["event_at"], datetime)
                                                else pd.Timestamp(row["event_at"]).date()) > split_date] if split_date else []
        name = "|".join(key)
        results[name] = {"asset_class": key[0], "base_timeframe": key[1], "variant": key[2],
                         "cohort": key[3], "raw": _summary(values),
                         "thinned": _summary(thinned), "train": _summary(train),
                         "holdout": _summary(test), "split_date": str(split_date) if split_date else None}
    return results


def _markdown(payload: dict[str, Any]) -> str:
    crypto_symbols_by_venue: dict[str, set[str]] = defaultdict(set)
    for row in payload.get("trade_rows", []):
        if row.get("asset_class") == "crypto" and row.get("venue"):
            crypto_symbols_by_venue[str(row["venue"])].add(str(row["symbol"]))
    venue_summary = ", ".join(f"{venue}: {len(symbols)} symbols" for venue, symbols in sorted(crypto_symbols_by_venue.items())) or "no crypto trades"
    bybit_path = LAB / "bybit_price_sensitivity.json"
    bybit_note = ""
    if bybit_path.exists():
        bybit = json.loads(bybit_path.read_text(encoding="utf-8"))
        bybit_cov = bybit.get("coverage", {})
        bybit_note = (f"- Bybit-only sensitivity: {bybit_cov.get('contexts_available', 0)} eligible-context instances "
                      f"across {bybit_cov.get('base_candidates', {})}; just {len(bybit.get('trade_rows', []))} raw outcome rows, "
                      "so its apparent positive small-N cells cannot validate venue robustness.")
    lines = ["# Reversal Confirmation Microstructure Study", "",
             f"- Generated: {payload['generated_at']}",
             "- Scope: historical research only; production Paper/Live settings unchanged.",
             "- Stock minute archive: point-in-time OHLCV; no trade-side order flow.",
             f"- Crypto OHLCV archive period after filtering: {payload['coverage']['crypto'].get('ohlcv_period')}; usable overlap is narrower where historical liquidation/OI/depth snapshots are absent.",
             f"- Crypto trade rows used price bars from: {venue_summary}. Fees were modeled with the configured Bybit non-VIP profile for all rows, so this is a signal comparison, not venue-specific execution replay.",
             *([bybit_note] if bybit_note else []),
             "- Fill model: signal enters at the next fully closed confirmation bar close; stop-first for same-bar stop/target ambiguity; fixed $10 risk; configured fees/slippage; no future bars are used for entry.",
             "- Crowding-thinned diagnostic: keep the first trade per symbol/session day, then at most three highest-flush candidates per same decision-time bucket; this reduces duplicate/crowding exposure but does not create statistically independent observations. Raw results are also shown.",
             "- Train/holdout split is chronological at 70% of event dates; variants are fixed a priori and no parameters were selected on holdout.", "",
             "## Executive Findings", ""]
    headline = (
        ("Stocks: 15m shock + 2x1m hold", "stocks|15m|base_held_2x1m|"),
        ("Stocks: same setup + confirmation-volume gate", "stocks|15m|held_2x1m_with_vol|"),
        ("Crypto: strict FAST 1m + higher-low/prior-high break + volume, OI gate", "crypto|1m|higher_low_break_vol|strict_fast_oi_gate"),
        ("Crypto: strict FAST 1m + immediate one-bar entry, no OI threshold", "crypto|1m|base_fast_1x1m|strict_fast_no_oi_gate"),
        ("Crypto: strict FAST 5m base + immediate one-bar entry, no OI threshold", "crypto|5m|base_fast_1x1m|strict_fast_no_oi_gate"),
    )
    for label, key in headline:
        result = payload["results"].get(key)
        if not result:
            continue
        m, h = result["thinned"], result["holdout"]
        lines.append(f"- **{label}:** {m['trades']} thinned trades, {m['net_r']:+.2f}R, PF {m['pf']}; chronological holdout {h['trades']} trades, {h['net_r']:+.2f}R, PF {h['pf']}.")
    lines.extend(["- The crypto structural-confirmation/OI result is a research lead only: its holdout contains very few trades; the broad immediate-entry and medium-deep variants are mostly negative.",
                  "- No Paper or Live settings were changed. Do not promote from these short and correlated samples.",
                  "", "## Results", "",
             "| Asset | Base | Cohort | Confirmation | N thinned | Net R | Net $ | PF | Win % | DD $ | Median delay | Holdout N / R / PF |",
             "|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|"])
    for result in payload["results"].values():
        m, h = result["thinned"], result["holdout"]
        lines.append(f"| {result['asset_class']} | {result['base_timeframe']} | {result['cohort'] or '-'} | {result['variant']} | {m['trades']} | {m['net_r']:+.2f} | ${m['net_usd']:+.2f} | {m['pf']} | {m['winrate_pct']:.1f} | ${m['max_drawdown_usd']:.2f} | {m['median_entry_delay_sec']}s | {h['trades']} / {h['net_r']:+.2f}R / {h['pf']} |")
    lines.extend(["", "## Data and Interpretation", "",
                  "- Confirmation variants: current two-bar hold, one-bar reclaim, relative-volume strong-close reclaim, higher-low plus prior-high break with volume, anchored VWAP reclaim, and a 5-minute confirmation close.",
                  "- Crypto cohorts separate strict FAST from medium-deep flushes. OI-threshold and positive bid-depth filters are shown as separate ablations; the no-OI-threshold cohort still requires contemporaneous OI/liquidity data to keep the event universe comparable.",
                  "- OHLCV volume is not aggressor-side volume. Historical depth snapshots are sparse snapshots rather than order-book event flow; they cannot reconstruct queue dynamics or intrabar fills.",
                  "- A positive in-sample or short holdout PF is not proof of edge. Sample size, regime concentration, single-name clustering, and data-feed limitations remain material.",
                  "", "## Coverage", "", "```json", json.dumps(payload["coverage"], indent=2, default=str), "```", "",
                  "## Full Variant Metrics", "", "```json", json.dumps(payload["results"], indent=2, default=str), "```", ""])
    return "\n".join(lines)


def run() -> dict[str, Any]:
    stock_rows, stock_coverage = _scan_stocks()
    crypto_rows, crypto_coverage = _crypto_scan()
    rows = stock_rows + crypto_rows
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(),
               "coverage": {"stocks": stock_coverage, "crypto": crypto_coverage},
               "results": _results(rows), "trade_rows": _pack_rows(rows),
               "method_version": "reversal_confirmation_v1_readonly"}
    LAB.mkdir(parents=True, exist_ok=True)
    (LAB / "results.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    pd.DataFrame(_pack_rows(rows)).to_csv(LAB / "trades.csv", index=False)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(_markdown(payload), encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = run()
    print(json.dumps({"generated_at": result["generated_at"],
                      "coverage": result["coverage"], "results": result["results"]}, indent=2, default=str))
