"""Point-in-time options context for crypto IV/RV and stock GEX diagnostics."""
from __future__ import annotations

import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

from src.data_collectors import market_intelligence_store as mi
from src.intelligence.context_config import ROOT, section
from src.intelligence.context_store import connect, insert_named


OPTION_COLS = (
    "provider_ts", "received_at", "asset_class", "underlying", "source", "context_type",
    "spot_price", "iv30", "rv30", "iv_rank", "vrp", "net_gex", "gamma_flip",
    "call_wall", "put_wall", "zero_dte_share", "oi_as_of", "quality_status", "raw_json",
)


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _dt(value: Any) -> datetime | None:
    try:
        out = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return out.replace(tzinfo=timezone.utc) if out.tzinfo is None else out.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def realized_vol_from_closes(closes: list[float], periods_per_year: float = 365.0) -> float | None:
    values = [float(x) for x in closes if x is not None and float(x) > 0]
    if len(values) < 10:
        return None
    returns = [math.log(values[i] / values[i - 1]) for i in range(1, len(values))]
    mean = sum(returns) / len(returns)
    variance = sum((x - mean) ** 2 for x in returns) / max(1, len(returns) - 1)
    return math.sqrt(variance * periods_per_year) * 100.0


def _bs_gamma(spot: float, strike: float, years: float, volatility: float,
              risk_free_rate: float) -> float | None:
    if spot <= 0 or strike <= 0 or years <= 0 or volatility <= 0:
        return None
    sigma_sqrt_t = volatility * math.sqrt(years)
    if sigma_sqrt_t <= 0:
        return None
    d1 = (math.log(spot / strike) +
          (risk_free_rate + 0.5 * volatility * volatility) * years) / sigma_sqrt_t
    normal_pdf = math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi)
    return normal_pdf / (spot * sigma_sqrt_t)


def calculate_gex_proxy(contracts: list[dict[str, Any]], *, spot: float,
                        as_of: datetime, risk_free_rate: float = 0.045) -> dict[str, Any]:
    """Approximate dealer GEX from public OI/IV chains.

    The conventional customer-long assumption (calls positive, puts negative)
    is deliberately labelled a proxy; actual dealer inventory is unobservable.
    """
    specs: list[dict[str, Any]] = []
    call_by_strike: dict[float, float] = {}
    put_by_strike: dict[float, float] = {}
    total_oi = zero_dte_oi = 0.0
    ny_date = as_of.astimezone(ZoneInfo("America/New_York")).date()
    for raw in contracts:
        strike = _f(raw.get("strike"))
        iv = _f(raw.get("iv") or raw.get("impliedVolatility"))
        oi = _f(raw.get("open_interest") or raw.get("openInterest"))
        expiration = _dt(raw.get("expiration"))
        kind = str(raw.get("option_type") or raw.get("type") or "").lower()
        if kind not in {"call", "put"} or strike is None or iv is None or oi is None or expiration is None:
            continue
        if strike <= 0 or oi <= 0 or not 0.005 <= iv <= 5.0 or expiration <= as_of:
            continue
        years = max((expiration - as_of).total_seconds() / (365.0 * 86400.0), 1.0 / (365.0 * 24.0))
        gamma = _bs_gamma(spot, strike, years, iv, risk_free_rate)
        if gamma is None:
            continue
        gex = gamma * oi * 100.0 * spot * spot * 0.01
        bucket = call_by_strike if kind == "call" else put_by_strike
        bucket[strike] = bucket.get(strike, 0.0) + gex
        total_oi += oi
        if expiration.astimezone(ZoneInfo("America/New_York")).date() == ny_date:
            zero_dte_oi += oi
        specs.append({"strike": strike, "iv": iv, "oi": oi, "kind": kind,
                      "expiration": expiration, "years": years})
    if not specs:
        raise ValueError("no usable option contracts for GEX proxy")
    net_gex = sum(call_by_strike.values()) - sum(put_by_strike.values())
    call_wall = max(call_by_strike, key=call_by_strike.get) if call_by_strike else None
    put_wall = max(put_by_strike, key=put_by_strike.get) if put_by_strike else None

    expirations = sorted({spec["expiration"] for spec in specs})
    iv_exp = min(expirations, key=lambda exp: abs((exp - as_of).total_seconds() / 86400.0 - 30.0))
    iv_specs = [s for s in specs if s["expiration"] == iv_exp and abs(s["strike"] / spot - 1.0) <= 0.10]
    weights = [math.sqrt(max(1.0, s["oi"])) for s in iv_specs]
    iv30 = (sum(s["iv"] * w for s, w in zip(iv_specs, weights)) / sum(weights) * 100.0
            if weights and sum(weights) > 0 else None)

    grid = [spot * (0.70 + i * 0.01) for i in range(61)]
    curve: list[tuple[float, float]] = []
    for trial_spot in grid:
        value = 0.0
        for spec in specs:
            gamma = _bs_gamma(trial_spot, spec["strike"], spec["years"], spec["iv"], risk_free_rate)
            if gamma is None:
                continue
            leg = gamma * spec["oi"] * 100.0 * trial_spot * trial_spot * 0.01
            value += leg if spec["kind"] == "call" else -leg
        curve.append((trial_spot, value))
    crossings: list[float] = []
    for (left_spot, left), (right_spot, right) in zip(curve, curve[1:]):
        if left == 0:
            crossings.append(left_spot)
        elif left * right < 0:
            weight = abs(left) / (abs(left) + abs(right))
            crossings.append(left_spot + (right_spot - left_spot) * weight)
    gamma_flip = min(crossings, key=lambda value: abs(value - spot)) if crossings else None
    return {
        "net_gex": net_gex, "gamma_flip": gamma_flip, "call_wall": call_wall,
        "put_wall": put_wall, "zero_dte_share": zero_dte_oi / total_oi if total_oi else None,
        "iv30": iv30, "contracts_used": len(specs), "total_open_interest": total_oi,
        "expirations_used": [value.isoformat() for value in expirations],
        "method": "customer_long_call_positive_put_negative_black_scholes_gamma_proxy",
    }


def _yf_stock_context(underlying: str, *, now: datetime,
                      cfg: dict[str, Any]) -> dict[str, Any]:
    import yfinance as yf

    ticker = yf.Ticker(underlying)
    intraday = ticker.history(period="5d", interval="1m", auto_adjust=False, prepost=False)
    if intraday is None or intraday.empty:
        intraday = ticker.history(period="5d", interval="5m", auto_adjust=False, prepost=False)
    if intraday is None or intraday.empty:
        raise ValueError("yfinance returned no underlying quote history")
    latest_index = intraday.index[-1]
    provider_ts = latest_index.to_pydatetime() if hasattr(latest_index, "to_pydatetime") else latest_index
    if provider_ts.tzinfo is None:
        provider_ts = provider_ts.replace(tzinfo=timezone.utc)
    provider_ts = provider_ts.astimezone(timezone.utc)
    spot = float(intraday["Close"].iloc[-1])

    daily = ticker.history(period="3mo", interval="1d", auto_adjust=False)
    closes = [] if daily is None or daily.empty else [float(x) for x in daily["Close"].dropna().tolist()]
    rv30 = realized_vol_from_closes(closes[-31:], periods_per_year=252.0)

    max_dte = int(cfg.get("stocks_chain_max_dte_days", 45))
    max_expirations = int(cfg.get("stocks_chain_max_expirations", 6))
    expirations: list[tuple[str, datetime]] = []
    for value in ticker.options:
        try:
            expiry = datetime.fromisoformat(str(value)).replace(hour=20, tzinfo=timezone.utc)
        except ValueError:
            continue
        dte = (expiry - now).total_seconds() / 86400.0
        if 0 < dte <= max_dte:
            expirations.append((str(value), expiry))
    expirations = expirations[:max_expirations]
    if not expirations:
        raise ValueError("yfinance returned no eligible future expirations")

    contracts: list[dict[str, Any]] = []
    for label, expiry in expirations:
        chain = ticker.option_chain(label)
        for kind, frame in (("call", chain.calls), ("put", chain.puts)):
            if frame is None or frame.empty:
                continue
            for _, item in frame.iterrows():
                contracts.append({
                    "option_type": kind, "expiration": expiry.isoformat(),
                    "strike": item.get("strike"), "iv": item.get("impliedVolatility"),
                    "open_interest": item.get("openInterest"), "volume": item.get("volume"),
                })
    proxy = calculate_gex_proxy(
        contracts, spot=spot, as_of=now,
        risk_free_rate=float(cfg.get("stocks_gex_risk_free_rate", 0.045)),
    )
    iv = _f(proxy.get("iv30"))
    return {
        "provider_ts": provider_ts.isoformat(), "received_at": now.isoformat(),
        "asset_class": "stocks", "underlying": underlying, "source": "yfinance_gex_proxy",
        "context_type": "gex_vrp_proxy", "spot_price": spot, "iv30": iv, "rv30": rv30,
        "iv_rank": None, "vrp": (iv - rv30 if iv is not None and rv30 is not None else None),
        "net_gex": proxy.get("net_gex"), "gamma_flip": proxy.get("gamma_flip"),
        "call_wall": proxy.get("call_wall"), "put_wall": proxy.get("put_wall"),
        "zero_dte_share": proxy.get("zero_dte_share"),
        "oi_as_of": provider_ts.date().isoformat(), "quality_status": "provisional_point_in_time",
        "raw_json": {**proxy, "limitations": [
            "unofficial delayed public chain", "open interest may be previous-session data",
            "dealer inventory sign is inferred, not observed", "shadow/advisory only",
        ]},
    }


def _crypto_rv(underlying: str, lookback_days: int) -> tuple[float | None, float | None]:
    try:
        from src.config import load_config
        from src.storage.file_store import FileStore
        frame = FileStore(load_config()).load_ohlcv("binance", f"{underlying}/USDT", "1d")
        if frame is None or frame.empty:
            return None, None
        rows = frame.tail(max(10, lookback_days + 1))
        closes = [float(x) for x in rows["close"].tolist()]
        return realized_vol_from_closes(closes), closes[-1]
    except Exception:
        return None, None


def _deribit_dvol(underlying: str, now: datetime) -> dict[str, Any]:
    start = now - timedelta(days=370)
    daily_response = requests.get(
        "https://www.deribit.com/api/v2/public/get_volatility_index_data",
        params={"currency": underlying, "start_timestamp": int(start.timestamp() * 1000),
                "end_timestamp": int(now.timestamp() * 1000), "resolution": "1D"},
        timeout=30,
        headers={"User-Agent": "crypto-ai-desk options context"},
    )
    daily_response.raise_for_status()
    daily_payload = daily_response.json()
    daily_rows = list((daily_payload.get("result") or {}).get("data") or [])
    recent_response = requests.get(
        "https://www.deribit.com/api/v2/public/get_volatility_index_data",
        params={"currency": underlying,
                "start_timestamp": int((now - timedelta(days=2)).timestamp() * 1000),
                "end_timestamp": int(now.timestamp() * 1000), "resolution": "3600"},
        timeout=30, headers={"User-Agent": "crypto-ai-desk options context"},
    )
    recent_response.raise_for_status()
    recent_payload = recent_response.json()
    recent_rows = list((recent_payload.get("result") or {}).get("data") or [])
    if not daily_rows or not recent_rows:
        raise ValueError("empty Deribit DVOL response")
    latest = recent_rows[-1]
    closes = [float(row[4]) for row in daily_rows if len(row) >= 5 and _f(row[4]) is not None]
    iv = float(latest[4])
    rank_values = closes + [iv]
    rank = None
    if len(rank_values) >= 250 and max(rank_values) > min(rank_values):
        rank = (iv - min(rank_values)) / (max(rank_values) - min(rank_values)) * 100.0
    return {"provider_ts": datetime.fromtimestamp(float(latest[0]) / 1000.0, tz=timezone.utc).isoformat(),
            "iv30": iv, "iv_rank": rank, "iv_rank_observations": len(rank_values),
            "raw": {"daily": daily_payload, "recent": recent_payload}}


def _stock_rows(path: Path, received_at: str) -> list[dict[str, Any]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    rows = raw if isinstance(raw, list) else list(raw.get("snapshots") or [])
    out = []
    for item in rows:
        if not isinstance(item, dict) or not item.get("underlying"):
            continue
        provider_ts = _dt(item.get("provider_ts") or item.get("as_of"))
        if provider_ts is None:
            continue
        iv, rv = _f(item.get("iv30")), _f(item.get("rv30"))
        out.append({
            "provider_ts": provider_ts.isoformat(), "received_at": received_at,
            "asset_class": "stocks", "underlying": str(item["underlying"]).upper(),
            "source": str(item.get("source") or "operator_import"), "context_type": "gex_vrp",
            "spot_price": _f(item.get("spot_price")), "iv30": iv, "rv30": rv,
            "iv_rank": _f(item.get("iv_rank")), "vrp": (iv - rv if iv is not None and rv is not None else None),
            "net_gex": _f(item.get("net_gex")), "gamma_flip": _f(item.get("gamma_flip")),
            "call_wall": _f(item.get("call_wall")), "put_wall": _f(item.get("put_wall")),
            "zero_dte_share": _f(item.get("zero_dte_share")), "oi_as_of": item.get("oi_as_of"),
            "quality_status": str(item.get("quality_status") or "unknown"), "raw_json": item,
        })
    return out


def refresh(*, db_path=None, now: datetime | None = None) -> dict[str, Any]:
    cfg = section("options_context")
    now = now or datetime.now(timezone.utc)
    received = now.isoformat()
    rows: list[dict[str, Any]] = []
    stock_proxy_rows: list[dict[str, Any]] = []
    errors: list[str] = []
    if cfg.get("enabled", True):
        for underlying in cfg.get("crypto_underlyings", ["BTC", "ETH"]):
            symbol = str(underlying).upper()
            try:
                dvol = _deribit_dvol(symbol, now)
                rv, spot = _crypto_rv(symbol, int(cfg.get("realized_vol_lookback_days", 30)))
                iv = _f(dvol.get("iv30"))
                rows.append({
                    "provider_ts": dvol["provider_ts"], "received_at": received,
                    "asset_class": "crypto", "underlying": symbol, "source": "deribit",
                    "context_type": "dvol_vrp", "spot_price": spot, "iv30": iv, "rv30": rv,
                    "iv_rank": dvol.get("iv_rank"), "vrp": (iv - rv if iv is not None and rv is not None else None),
                    "net_gex": None, "gamma_flip": None, "call_wall": None, "put_wall": None,
                    "zero_dte_share": None, "oi_as_of": dvol["provider_ts"],
                    "quality_status": "ok", "raw_json": dvol.get("raw"),
                })
            except Exception as exc:
                errors.append(f"deribit:{symbol}:{type(exc).__name__}")
        if cfg.get("stocks_public_fallback_enabled", False):
            for underlying in cfg.get("stocks_public_underlyings", ["SPY", "QQQ"]):
                symbol = str(underlying).upper()
                try:
                    stock_proxy_rows.append(_yf_stock_context(symbol, now=now, cfg=cfg))
                except Exception as exc:
                    errors.append(f"yfinance_gex_proxy:{symbol}:{type(exc).__name__}")
    rows.extend(stock_proxy_rows)
    stock_path = ROOT / str(cfg.get("stocks_source_path") or "data/reference/stocks_options_context.json")
    manual_rows = _stock_rows(stock_path, received)
    rows.extend(manual_rows)
    written = 0
    with connect(db_path) as conn:
        for row in rows:
            written += int(insert_named(conn, "options_context_snapshots", row, OPTION_COLS))
        crypto_ok = any(r["asset_class"] == "crypto" for r in rows)
        stocks_ok = bool(stock_proxy_rows or manual_rows)
        mi.record_source_health(conn, "context:deribit_dvol", status="ok" if crypto_ok else "error",
                                success=crypto_ok, records_written=sum(r["asset_class"] == "crypto" for r in rows),
                                latest_provider_ts=received if crypto_ok else None,
                                error=";".join(errors) or None)
        mi.record_source_health(conn, "context:stocks_options_import",
                                status="ok" if manual_rows else "disabled_no_current_file",
                                success=True, records_written=len(manual_rows),
                                latest_provider_ts=received if manual_rows else None)
        proxy_errors = [x for x in errors if x.startswith("yfinance_gex_proxy:")]
        mi.record_source_health(
            conn, "context:stocks_options_yfinance_proxy",
            status="ok_provisional" if stock_proxy_rows else "error",
            success=bool(stock_proxy_rows), records_written=len(stock_proxy_rows),
            latest_provider_ts=max((r["provider_ts"] for r in stock_proxy_rows), default=None),
            error=";".join(proxy_errors) or None,
            details={"quality_status": "provisional_point_in_time", "shadow_only": True},
        )
        conn.commit()
    return {"at": received, "rows": len(rows), "written": written,
            "stock_proxy_rows": len(stock_proxy_rows), "manual_stock_rows": len(manual_rows),
            "errors": errors}


def latest(asset_class: str, underlying: str, *, as_of: datetime | None = None,
           db_path=None, cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or section("options_context")
    now = as_of or datetime.now(timezone.utc)
    with connect(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM options_context_snapshots WHERE asset_class=? AND underlying=? "
            "AND provider_ts<=? ORDER BY provider_ts DESC,id DESC LIMIT 1",
            (str(asset_class).lower(), str(underlying).upper(), now.isoformat()),
        ).fetchone()
    if not row:
        return {"status": "unknown", "reason": "no_point_in_time_options_context"}
    item = dict(row)
    provider_ts = _dt(item.get("provider_ts"))
    max_age = timedelta(minutes=float(cfg.get(
        "crypto_max_age_minutes" if str(asset_class).lower() == "crypto" else "stocks_max_age_minutes", 30)))
    if provider_ts is None or not timedelta(0) <= now - provider_ts <= max_age:
        return {**item, "status": "stale", "reason": "options_context_stale"}
    return {**item, "status": "ok", "reason": "options_context_fresh"}


__all__ = ["refresh", "latest", "realized_vol_from_closes", "calculate_gex_proxy",
           "OPTION_COLS", "_stock_rows"]
