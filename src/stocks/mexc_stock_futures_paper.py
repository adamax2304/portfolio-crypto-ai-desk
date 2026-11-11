"""Paper execution lane for MEXC US stock futures.

The ordinary stocks pipeline remains the strategy authority. A recent stock
intraday signal whose pre-gate tier was A/B may be copied into this lane only
when a trusted directional catalyst supports it. Public MEXC contract metadata,
quotes, depth and one-minute candles are then used for deterministic Paper
orders and outcomes.

This module never calls a private MEXC endpoint and never writes live routing
tables. It also never changes the source signal, its tier, score or geometry.
"""
from __future__ import annotations

import hashlib
import json
import math
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo

import yaml

from src.config import load_config
from src.execution.position_sizing import size_position
from src.live_execution.mexc_client import MexcAPIError, MexcFuturesClient
from src.news.source_health import _parse_ts
from src.stocks.market_calendar import is_us_holiday


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "stocks" / "mexc_stock_futures_paper.yaml"
NY = ZoneInfo("America/New_York")
UTC = timezone.utc
PLAN_MARKER = "market_closed_intraday_planning_only"
TERMINAL_ORDER_STATES = {"FILLED", "EXPIRED", "CANCELLED", "REJECTED", "INVALIDATED"}
ACTIVE_ORDER_STATES = {"STAGED", "TRIGGERED"}

_DEFAULTS: dict[str, Any] = {
    "enabled": False,
    "strategy_id": "stocks_mexc_preopen_news_v1",
    "paper_lane": "paper_mexc_stock_futures",
    "execution_mode": "paper",
    "api_base_url": "https://api.mexc.com",
    "request_timeout_seconds": 8,
    "preopen_refresh_start_et": "08:50",
    "preopen_decision_start_et": "09:10",
    "preopen_decision_end_et": "09:30",
    # Pre-US plans may be prepared before the cash open, but must not become
    # entries during the thin pre-open auction. They need a confirmed first
    # opening bar before they can execute.
    "opening_protection_enabled": True,
    "opening_protection_minutes": 5,
    "opening_confirmation_min_close_location": 0.60,
    "opening_confirmation_min_body_fraction": 0.35,
    "opening_max_positions": 1,
    "opening_risk_multiplier": 0.50,
    "preopen_health_alert_after_et": "09:20",
    "intraday_event_end_et": "15:30",
    "force_flat_et": "15:55",
    "monitor_end_et": "16:05",
    "report_refresh_minutes": 15,
    "require_pre_gate_ab": True,
    "min_source_score": 70.0,
    "max_source_signal_age_hours": 18.0,
    "max_news_age_hours": 18.0,
    "min_news_confidence": 0.68,
    "allowed_source_qualities": ["regulator", "primary", "company_pr", "reputable"],
    "allowed_content_levels": ["full_body", "summary_only"],
    "allowed_event_types": [
        "guidance", "analyst_action", "mna", "fda_clinical",
        "product_launch", "partnership", "sec_filing",
    ],
    "blocked_event_types": [
        "earnings", "legal_risk", "offering_dilution", "management_change",
    ],
    "allowed_setup_types": ["continuation", "breakout", "pullback", "retest"],
    "allowed_directions": ["long", "short"],
    "max_orders_per_symbol_session": 1,
    "max_open_positions": 3,
    "active_contract_states": [0],
    "max_spread_bps": 35.0,
    "max_fair_index_deviation_bps": 60.0,
    "max_source_entry_drift_bps": 500.0,
    "min_top5_depth_usdt": 250.0,
    "min_hold_volume": 1000.0,
    # Optional only for a small-account Paper experiment. Disabling these
    # gates never permits a missing/invalid quote; bid/ask remain mandatory
    # for honest parity pricing.
    "execution_liquidity_gates_enabled": True,
    "contract_catalog_ttl_minutes": 30,
    "quote_health_ttl_minutes": 5,
    "health_probe_tickers": ["AAPL", "MSFT", "NVDA", "TSLA", "PLTR"],
    "premarket_range_minutes": 60,
    "pullback_setup_types": ["pullback", "retest"],
    "breakout_setup_types": ["continuation", "breakout"],
    "breakout_limit_cushion_bps": 8.0,
    "pullback_offset_bps": 20.0,
    "min_stop_distance_pct": 0.005,
    "normalize_too_tight_source_stop": True,
    "max_stop_distance_pct": 0.04,
    "default_target_r": [1.5, 2.5, 4.0],
    "order_ttl_minutes": 25,
    "preopen_order_ttl_minutes": 50,
    "max_replacements": 2,
    "risk_per_trade_pct": 0.005,
    "max_concurrent_risk_pct": 0.025,
    "max_margin_per_trade_pct": 0.25,
    "max_notional_per_trade_pct": 1.5,
    "max_leverage": 5,
    "liquidation_buffer_to_stop": 3.0,
    "fee_profile": "mexc_default_futures",
    "partial_take_profit": {"weights": [0.33, 0.33, 0.34]},
    "model_f": {
        "arm_breakeven_at_r": 0.6,
        "lock_profit_at_r": 1.0,
        "lock_level_r": 0.5,
    },
    "send_fill_telegram": False,
    "report_path": "reports/MEXC_STOCK_FUTURES_PAPER_LATEST.md",
}

_DDL = """
CREATE TABLE IF NOT EXISTS mexc_stock_futures_contracts (
    ticker TEXT PRIMARY KEY,
    mexc_symbol TEXT NOT NULL,
    native_symbol TEXT NOT NULL,
    state INTEGER,
    api_allowed INTEGER NOT NULL,
    price_unit REAL NOT NULL,
    vol_unit REAL NOT NULL,
    min_vol REAL NOT NULL,
    contract_size REAL NOT NULL,
    max_leverage INTEGER NOT NULL,
    maker_fee_rate REAL,
    taker_fee_rate REAL,
    bid REAL,
    ask REAL,
    fair_price REAL,
    index_price REAL,
    funding_rate REAL,
    hold_volume REAL,
    spread_bps REAL,
    top5_depth_usdt REAL,
    catalog_at TEXT,
    quote_at TEXT,
    snapshot_at TEXT NOT NULL,
    raw_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mexc_stock_futures_paper_orders (
    order_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    paper_lane TEXT NOT NULL,
    source_signal_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    session_date TEXT NOT NULL,
    ticker TEXT NOT NULL,
    mexc_symbol TEXT,
    direction TEXT NOT NULL,
    source_pre_gate_tier TEXT,
    source_score REAL,
    setup_type TEXT,
    entry_mode TEXT,
    status TEXT NOT NULL,
    reject_reason TEXT,
    decision_at TEXT NOT NULL,
    event_published_at TEXT,
    event_type TEXT,
    event_source TEXT,
    event_confidence REAL,
    trigger_price REAL,
    limit_price REAL,
    stop_price REAL,
    tp1 REAL,
    tp2 REAL,
    tp3 REAL,
    source_entry REAL,
    source_stop REAL,
    source_drift_bps REAL,
    spread_bps REAL,
    fair_index_deviation_bps REAL,
    funding_rate REAL,
    hold_volume REAL,
    top5_depth_usdt REAL,
    price_unit REAL,
    vol_unit REAL,
    min_vol REAL,
    contract_size REAL,
    contract_max_leverage INTEGER,
    expires_at TEXT,
    triggered_at TEXT,
    filled_at TEXT,
    fill_price REAL,
    replacement_count INTEGER NOT NULL DEFAULT 0,
    last_evaluated_at TEXT,
    last_error TEXT,
    snapshot_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(source_signal_id, event_id, strategy_id)
);

CREATE INDEX IF NOT EXISTS idx_mexc_stock_paper_orders_active
ON mexc_stock_futures_paper_orders(status, expires_at);
CREATE INDEX IF NOT EXISTS idx_mexc_stock_paper_orders_session
ON mexc_stock_futures_paper_orders(session_date, ticker);

CREATE TABLE IF NOT EXISTS mexc_stock_futures_paper_positions (
    position_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL UNIQUE,
    strategy_id TEXT NOT NULL,
    paper_lane TEXT NOT NULL,
    source_signal_id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    ticker TEXT NOT NULL,
    mexc_symbol TEXT NOT NULL,
    direction TEXT NOT NULL,
    entry_mode TEXT NOT NULL,
    status TEXT NOT NULL,
    entry_at TEXT NOT NULL,
    entry_price REAL NOT NULL,
    stop_initial REAL NOT NULL,
    stop_current REAL NOT NULL,
    tp1 REAL NOT NULL,
    tp2 REAL NOT NULL,
    tp3 REAL NOT NULL,
    qty REAL NOT NULL,
    contract_volume REAL NOT NULL,
    contract_size REAL NOT NULL,
    risk_usdt REAL NOT NULL,
    risk_pct REAL NOT NULL,
    notional_usdt REAL NOT NULL,
    margin_used_usdt REAL NOT NULL,
    leverage_used INTEGER NOT NULL,
    funding_rate_at_entry REAL,
    hold_volume_at_entry REAL,
    highest_tp_touched INTEGER NOT NULL DEFAULT 0,
    remaining_weight REAL NOT NULL DEFAULT 1.0,
    realized_r_accum REAL NOT NULL DEFAULT 0.0,
    max_favorable_r REAL NOT NULL DEFAULT 0.0,
    max_adverse_r REAL NOT NULL DEFAULT 0.0,
    protection_stage TEXT NOT NULL DEFAULT 'INITIAL',
    last_evaluated_at TEXT,
    exit_at TEXT,
    exit_price REAL,
    paper_execution_r REAL,
    close_reason TEXT,
    fee_profile TEXT NOT NULL,
    entry_order_type TEXT NOT NULL,
    evidence_class TEXT NOT NULL DEFAULT 'forward_post_activation',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(order_id) REFERENCES mexc_stock_futures_paper_orders(order_id)
);

CREATE INDEX IF NOT EXISTS idx_mexc_stock_paper_positions_status
ON mexc_stock_futures_paper_positions(status, entry_at);

CREATE TABLE IF NOT EXISTS mexc_stock_futures_quote_health (
    ticker TEXT PRIMARY KEY,
    checked_at TEXT NOT NULL,
    status TEXT NOT NULL,
    reason TEXT,
    mexc_symbol TEXT,
    bid REAL,
    ask REAL,
    fair_price REAL,
    top5_depth_usdt REAL
);
CREATE INDEX IF NOT EXISTS idx_mexc_stock_quote_health_checked
ON mexc_stock_futures_quote_health(checked_at);

CREATE TABLE IF NOT EXISTS mexc_stock_futures_quote_health_alerts (
    ticker TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    alerted_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mexc_stock_futures_preopen_health (
    session_date TEXT PRIMARY KEY,
    checked_at TEXT NOT NULL,
    actionable_count INTEGER NOT NULL,
    processed_count INTEGER NOT NULL,
    staged_count INTEGER NOT NULL,
    rejected_count INTEGER NOT NULL,
    status TEXT NOT NULL,
    reason TEXT,
    alerted_at TEXT
);
CREATE TABLE IF NOT EXISTS mexc_stock_futures_preopen_health_history (
    session_date TEXT NOT NULL,
    checked_at TEXT NOT NULL,
    actionable_count INTEGER NOT NULL,
    processed_count INTEGER NOT NULL,
    staged_count INTEGER NOT NULL,
    rejected_count INTEGER NOT NULL,
    status TEXT NOT NULL,
    reason TEXT,
    alerted_at TEXT,
    PRIMARY KEY(session_date, checked_at)
);
CREATE INDEX IF NOT EXISTS idx_mexc_stock_preopen_health_history_session
ON mexc_stock_futures_preopen_health_history(session_date, checked_at);
"""

_ORDER_COLS = (
    "order_id", "strategy_id", "paper_lane", "source_signal_id", "event_id",
    "session_date", "ticker", "mexc_symbol", "direction", "source_pre_gate_tier",
    "source_score", "setup_type", "entry_mode", "status", "reject_reason",
    "decision_at", "event_published_at", "event_type", "event_source",
    "event_confidence", "trigger_price", "limit_price", "stop_price", "tp1",
    "tp2", "tp3", "source_entry", "source_stop", "source_drift_bps",
    "spread_bps", "fair_index_deviation_bps", "funding_rate", "hold_volume",
    "top5_depth_usdt", "price_unit", "vol_unit", "min_vol", "contract_size",
    "contract_max_leverage", "expires_at", "triggered_at", "filled_at",
    "fill_price", "replacement_count", "last_evaluated_at", "last_error",
    "snapshot_json", "created_at", "updated_at",
)

_POSITION_COLS = (
    "position_id", "order_id", "strategy_id", "paper_lane", "source_signal_id",
    "event_id", "ticker", "mexc_symbol", "direction", "entry_mode", "status",
    "entry_at", "entry_price", "stop_initial", "stop_current", "tp1", "tp2",
    "tp3", "qty", "contract_volume", "contract_size", "risk_usdt", "risk_pct",
    "notional_usdt", "margin_used_usdt", "leverage_used",
    "funding_rate_at_entry", "hold_volume_at_entry", "highest_tp_touched",
    "remaining_weight", "realized_r_accum", "max_favorable_r",
    "max_adverse_r", "protection_stage", "last_evaluated_at", "exit_at",
    "exit_price", "paper_execution_r", "close_reason", "fee_profile",
    "entry_order_type", "evidence_class", "created_at", "updated_at",
)

_CONTRACT_ADDITIVE_COLUMNS = (
    ("catalog_at", "TEXT"),
    ("quote_at", "TEXT"),
)


@dataclass(frozen=True)
class Quote:
    bid: float
    ask: float
    fair: float
    index: float
    funding_rate: float
    hold_volume: float
    spread_bps: float
    top5_depth_usdt: float


def load_cfg() -> dict[str, Any]:
    cfg = dict(_DEFAULTS)
    if CONFIG_PATH.exists():
        try:
            raw = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
            cfg.update(raw.get("mexc_stock_futures_paper") or {})
        except Exception:
            pass
    return cfg


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(_DDL)
    existing = {
        str(row[1])
        for row in conn.execute("PRAGMA table_info(mexc_stock_futures_contracts)")
    }
    for column, column_type in _CONTRACT_ADDITIVE_COLUMNS:
        if column not in existing:
            conn.execute(
                f"ALTER TABLE mexc_stock_futures_contracts "
                f"ADD COLUMN {column} {column_type}"
            )
    missing_catalog_at = conn.execute(
        "SELECT 1 FROM mexc_stock_futures_contracts "
        "WHERE catalog_at IS NULL LIMIT 1"
    ).fetchone()
    if missing_catalog_at:
        conn.execute(
            "UPDATE mexc_stock_futures_contracts "
            "SET catalog_at=snapshot_at WHERE catalog_at IS NULL"
        )


def _utc(value: datetime | None = None) -> datetime:
    moment = value or datetime.now(UTC)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC)


def _iso(value: datetime) -> str:
    return _utc(value).isoformat()


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    try:
        decoded = json.loads(value or "{}")
        return decoded if isinstance(decoded, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


def _hhmm(value: str) -> int:
    hour, minute = str(value).split(":", 1)
    return int(hour) * 60 + int(minute)


def _ny_minutes(now: datetime) -> tuple[datetime, int]:
    local = _utc(now).astimezone(NY)
    return local, local.hour * 60 + local.minute


def _trading_day(now: datetime) -> bool:
    local, _ = _ny_minutes(now)
    return local.weekday() < 5 and not is_us_holiday(_utc(now))


def in_refresh_window(now: datetime | None = None, cfg: dict[str, Any] | None = None) -> bool:
    cfg = cfg or load_cfg()
    moment = _utc(now)
    if not _trading_day(moment):
        return False
    _, minute = _ny_minutes(moment)
    return _hhmm(cfg["preopen_refresh_start_et"]) <= minute <= _hhmm(
        cfg.get("monitor_end_et") or cfg["force_flat_et"]
    )


def in_candidate_window(now: datetime | None = None, cfg: dict[str, Any] | None = None) -> bool:
    cfg = cfg or load_cfg()
    moment = _utc(now)
    if not _trading_day(moment):
        return False
    _, minute = _ny_minutes(moment)
    return _hhmm(cfg["preopen_decision_start_et"]) <= minute <= _hhmm(cfg["intraday_event_end_et"])


def _session_date(now: datetime) -> str:
    return _utc(now).astimezone(NY).date().isoformat()


def _force_flat_at(now: datetime, cfg: dict[str, Any]) -> datetime:
    local = _utc(now).astimezone(NY)
    total = _hhmm(cfg["force_flat_et"])
    return local.replace(hour=total // 60, minute=total % 60, second=0, microsecond=0).astimezone(UTC)


def _is_preus_actionability_order(order: dict[str, Any]) -> bool:
    """Whether an order was created from the pre-US review hand-off."""
    return str(order.get("event_source") or "") == "stocks_preus_actionability"


def _opening_protection_applies(order: dict[str, Any], cfg: dict[str, Any]) -> bool:
    return bool(cfg.get("opening_protection_enabled", True)) and _is_preus_actionability_order(order)


def _cash_open_at(now: datetime) -> datetime:
    local = _utc(now).astimezone(NY)
    return local.replace(hour=9, minute=30, second=0, microsecond=0).astimezone(UTC)


def _opening_confirmation_at(now: datetime, cfg: dict[str, Any]) -> datetime:
    return _cash_open_at(now) + timedelta(minutes=int(cfg.get("opening_protection_minutes", 5)))


def _opening_confirmation(
    order: dict[str, Any],
    candles: Iterable[dict[str, Any]],
    *,
    now: datetime,
    cfg: dict[str, Any],
) -> tuple[str, str | None, datetime | None]:
    """Gate a pre-US plan on the completed first cash-session bar."""
    if not _opening_protection_applies(order, cfg):
        return "passed", None, None
    confirmation_at = _opening_confirmation_at(now, cfg)
    if _utc(now) < confirmation_at:
        return "pending", None, confirmation_at

    opening_at = _cash_open_at(now)
    first_bar = [
        candle for candle in sorted(candles, key=_candle_time)
        if opening_at <= _candle_time(candle) < confirmation_at
    ]
    required = int(cfg.get("opening_protection_minutes", 5))
    if len(first_bar) < required:
        return "failed", "OPENING_CONFIRMATION_DATA_MISSING", confirmation_at

    op = _float(first_bar[0].get("open"))
    close = _float(first_bar[-1].get("close"))
    high = max(_float(candle.get("high")) for candle in first_bar)
    low = min(_float(candle.get("low")) for candle in first_bar)
    bar_range = high - low
    if op <= 0 or close <= 0 or bar_range <= 0:
        return "failed", "OPENING_CONFIRMATION_DATA_INVALID", confirmation_at

    direction = str(order.get("direction") or "").lower()
    close_location = (close - low) / bar_range if direction == "long" else (high - close) / bar_range
    body_fraction = abs(close - op) / bar_range
    trigger = _float(order.get("trigger_price") or order.get("limit_price"))
    through_trigger = close >= trigger if direction == "long" else close <= trigger
    directional = close > op if direction == "long" else close < op
    if not (
        through_trigger
        and directional
        and close_location >= float(cfg.get("opening_confirmation_min_close_location", 0.60))
        and body_fraction >= float(cfg.get("opening_confirmation_min_body_fraction", 0.35))
    ):
        return "failed", "OPENING_DRIVE_NOT_CONFIRMED", confirmation_at
    return "passed", None, confirmation_at


def _client(cfg: dict[str, Any]) -> MexcFuturesClient:
    return MexcFuturesClient(
        base_url=str(cfg.get("api_base_url") or "https://api.mexc.com"),
        timeout_seconds=float(cfg.get("request_timeout_seconds", 8)),
    )


def _is_stock_contract(meta: dict[str, Any]) -> bool:
    raw_plates = meta.get("conceptPlate") or []
    if isinstance(raw_plates, str):
        raw_plates = [raw_plates]
    plates = {str(value).lower() for value in raw_plates}
    return any("stock" in plate or "tradfi" in plate for plate in plates)


def _ticker_from_contract(meta: dict[str, Any]) -> str:
    name = str(meta.get("baseCoinName") or "").strip().upper()
    if name and name != "USDT":
        return name
    base = str(meta.get("baseCoin") or "").upper()
    return base[:-5] if base.endswith("STOCK") else base


def _contract_row(meta: dict[str, Any], now: datetime) -> dict[str, Any]:
    native = str(meta.get("symbol") or "").upper()
    return {
        "ticker": _ticker_from_contract(meta),
        "mexc_symbol": native.replace("_", "/"),
        "native_symbol": native,
        "state": int(meta.get("state") or 0),
        "api_allowed": int(bool(meta.get("apiAllowed"))),
        "price_unit": max(_float(meta.get("priceUnit"), 0.01), 1e-9),
        "vol_unit": max(_float(meta.get("volUnit"), 1.0), 1e-9),
        "min_vol": max(_float(meta.get("minVol"), 1.0), 0.0),
        "contract_size": max(_float(meta.get("contractSize"), 1.0), 1e-12),
        "max_leverage": max(1, int(_float(meta.get("maxLeverage"), 1))),
        "maker_fee_rate": _float(meta.get("makerFeeRate")),
        "taker_fee_rate": _float(meta.get("takerFeeRate")),
        "bid": None, "ask": None, "fair_price": None, "index_price": None,
        "funding_rate": None, "hold_volume": None, "spread_bps": None,
        "top5_depth_usdt": None, "catalog_at": _iso(now), "quote_at": None,
        "snapshot_at": _iso(now),
        "raw_json": json.dumps(meta, sort_keys=True),
    }


def refresh_contract_catalog(
    conn: sqlite3.Connection,
    *,
    client: MexcFuturesClient,
    now: datetime | None = None,
) -> int:
    moment = _utc(now)
    rows: dict[str, dict[str, Any]] = {}
    for meta in client.contracts():
        if not _is_stock_contract(meta):
            continue
        row = _contract_row(meta, moment)
        ticker = row["ticker"]
        if not ticker or not row["native_symbol"].endswith(("_USDT", "_USDC")):
            continue
        current = rows.get(ticker)
        # Prefer USDT and the explicit STOCK contract when duplicates exist.
        priority = (
            int(row["native_symbol"].endswith("_USDT")),
            int("STOCK_" in row["native_symbol"]),
        )
        old_priority = (
            int(bool(current) and current["native_symbol"].endswith("_USDT")),
            int(bool(current) and "STOCK_" in current["native_symbol"]),
        )
        if current is None or priority > old_priority:
            rows[ticker] = row
    cols = tuple(rows[next(iter(rows))].keys()) if rows else ()
    if cols:
        placeholders = ",".join("?" for _ in cols)
        updates = ",".join(
            f"{column}=excluded.{column}" for column in cols if column != "ticker"
        )
        conn.executemany(
            f"INSERT INTO mexc_stock_futures_contracts({','.join(cols)}) "
            f"VALUES({placeholders}) ON CONFLICT(ticker) DO UPDATE SET {updates}",
            [tuple(row[column] for column in cols) for row in rows.values()],
        )
    return len(rows)


def _catalog_stale(conn: sqlite3.Connection, now: datetime, cfg: dict[str, Any]) -> bool:
    row = conn.execute(
        "SELECT MAX(COALESCE(catalog_at,snapshot_at)) "
        "FROM mexc_stock_futures_contracts"
    ).fetchone()
    last = _parse_ts(row[0]) if row and row[0] else None
    return last is None or now - last > timedelta(
        minutes=float(cfg.get("contract_catalog_ttl_minutes", 30))
    )


def _depth_notional(depth: dict[str, Any], contract_size: float) -> float:
    total = 0.0
    for side in ("bids", "asks"):
        for level in (depth.get(side) or [])[:5]:
            if not isinstance(level, (list, tuple)) or len(level) < 2:
                continue
            total += _float(level[0]) * _float(level[1]) * contract_size
    return total


def _fetch_quote_once(
    client: MexcFuturesClient,
    contract: dict[str, Any],
) -> Quote:
    symbol = str(contract["mexc_symbol"])
    ticker = client.ticker(symbol)
    depth = client.depth(symbol, limit=5)
    bids = depth.get("bids") or []
    asks = depth.get("asks") or []
    if not bids or not asks:
        raise ValueError("empty_order_book")
    bid, ask = _float(bids[0][0]), _float(asks[0][0])
    if bid <= 0 or ask <= 0 or ask < bid:
        raise ValueError("invalid_order_book")
    mid = (bid + ask) / 2.0
    fair = _float(ticker.get("fairPrice"), _float(ticker.get("lastPrice"), mid))
    index = _float(ticker.get("indexPrice"), fair)
    if fair <= 0 or index <= 0:
        raise ValueError("invalid_ticker_price")
    return Quote(
        bid=bid,
        ask=ask,
        fair=fair,
        index=index,
        funding_rate=_float(ticker.get("fundingRate")),
        hold_volume=_float(ticker.get("holdVol")),
        spread_bps=(ask - bid) / mid * 10_000.0,
        top5_depth_usdt=_depth_notional(depth, _float(contract.get("contract_size"), 1.0)),
    )


def fetch_quote(
    client: MexcFuturesClient,
    contract: dict[str, Any],
) -> Quote:
    """Read a public MEXC quote, tolerating transient exchange rejections.

    Public stock-futures endpoints occasionally reject a short burst while the
    next request succeeds. A transient endpoint error must not make a tradable
    future look unavailable. Data-shape failures deliberately do not retry:
    an empty or invalid book remains an unsafe quote.
    """
    last_error: MexcAPIError | None = None
    for attempt in range(3):
        try:
            return _fetch_quote_once(client, contract)
        except MexcAPIError as exc:
            last_error = exc
            if attempt == 2:
                break
            time.sleep(0.25 * (attempt + 1))
    raise last_error or MexcAPIError("mexc_quote_unavailable")


def _update_quote(
    conn: sqlite3.Connection,
    ticker: str,
    quote: Quote,
    now: datetime,
) -> None:
    conn.execute(
        "UPDATE mexc_stock_futures_contracts SET bid=?,ask=?,fair_price=?,index_price=?,"
        "funding_rate=?,hold_volume=?,spread_bps=?,top5_depth_usdt=?,"
        "quote_at=?,snapshot_at=? "
        "WHERE ticker=?",
        (
            quote.bid, quote.ask, quote.fair, quote.index, quote.funding_rate,
            quote.hold_volume, quote.spread_bps, quote.top5_depth_usdt,
            _iso(now), _iso(now), ticker,
        ),
    )


def _record_quote_health(
    conn: sqlite3.Connection,
    *,
    ticker: str,
    now: datetime,
    status: str,
    reason: str | None = None,
    contract: dict[str, Any] | None = None,
    quote: Quote | None = None,
) -> None:
    """Persist MEXC public-market readiness, separately from order results."""
    conn.execute(
        "INSERT INTO mexc_stock_futures_quote_health("
        "ticker,checked_at,status,reason,mexc_symbol,bid,ask,fair_price,top5_depth_usdt) "
        "VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(ticker) DO UPDATE SET "
        "checked_at=excluded.checked_at,status=excluded.status,reason=excluded.reason,"
        "mexc_symbol=excluded.mexc_symbol,bid=excluded.bid,ask=excluded.ask,"
        "fair_price=excluded.fair_price,top5_depth_usdt=excluded.top5_depth_usdt",
        (ticker, _iso(now), status, reason,
         (contract or {}).get("mexc_symbol"),
         quote.bid if quote else None, quote.ask if quote else None,
         quote.fair if quote else None, quote.top5_depth_usdt if quote else None),
    )


def probe_quote_health(
    conn: sqlite3.Connection,
    *,
    client: MexcFuturesClient,
    now: datetime,
    cfg: dict[str, Any],
) -> dict[str, int]:
    """Probe a tiny fixed stock basket, never an expensive full catalog scan."""
    ttl = timedelta(minutes=float(cfg.get("quote_health_ttl_minutes", 5)))
    last = conn.execute("SELECT MAX(checked_at) FROM mexc_stock_futures_quote_health").fetchone()
    checked = _parse_ts(last[0]) if last and last[0] else None
    if checked is not None and now - checked < ttl:
        return {"probed": 0, "healthy": 0, "unhealthy": 0, "status": "fresh_cache"}
    contracts = {str(row["ticker"]): dict(row) for row in conn.execute(
        "SELECT * FROM mexc_stock_futures_contracts"
    )}
    probed = healthy = unhealthy = 0
    for ticker_raw in cfg.get("health_probe_tickers") or []:
        ticker = str(ticker_raw).upper()
        if not ticker:
            continue
        probed += 1
        contract = contracts.get(ticker)
        if contract is None:
            _record_quote_health(conn, ticker=ticker, now=now, status="UNHEALTHY",
                                 reason="MEXC_STOCK_CONTRACT_UNAVAILABLE")
            unhealthy += 1
            continue
        try:
            quote = fetch_quote(client, contract)
            _update_quote(conn, ticker, quote, now)
            _record_quote_health(conn, ticker=ticker, now=now, status="HEALTHY",
                                 contract=contract, quote=quote)
            healthy += 1
        except Exception as exc:  # noqa: BLE001 - health diagnostics only
            _record_quote_health(conn, ticker=ticker, now=now, status="UNHEALTHY",
                                 reason=f"MEXC_QUOTE_UNAVAILABLE:{type(exc).__name__}",
                                 contract=contract)
            unhealthy += 1
        # The next ticker begins with an HTTP request. Persist this probe and
        # release the writer lease before that request starts.
        conn.commit()
    return {"probed": probed, "healthy": healthy, "unhealthy": unhealthy, "status": "ok"}


def consume_new_quote_health_alerts(conn: sqlite3.Connection, *, now: datetime) -> list[dict[str, Any]]:
    """Return each unhealthy state once; recovery resets its future alert."""
    rows = [dict(row) for row in conn.execute(
        "SELECT ticker,status,reason,mexc_symbol,checked_at FROM mexc_stock_futures_quote_health"
    )]
    alerts: list[dict[str, Any]] = []
    for row in rows:
        ticker = str(row["ticker"])
        if str(row.get("status")) == "HEALTHY":
            conn.execute("DELETE FROM mexc_stock_futures_quote_health_alerts WHERE ticker=?", (ticker,))
            continue
        previous = conn.execute(
            "SELECT status FROM mexc_stock_futures_quote_health_alerts WHERE ticker=?", (ticker,)
        ).fetchone()
        if previous is not None and str(previous[0]) == str(row.get("status")):
            continue
        conn.execute(
            "INSERT INTO mexc_stock_futures_quote_health_alerts(ticker,status,alerted_at) VALUES(?,?,?) "
            "ON CONFLICT(ticker) DO UPDATE SET status=excluded.status,alerted_at=excluded.alerted_at",
            (ticker, str(row.get("status")), _iso(now)),
        )
        alerts.append(row)
    return alerts


def _recent_events(
    conn: sqlite3.Connection,
    now: datetime,
    cfg: dict[str, Any],
) -> list[dict[str, Any]]:
    exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='news_canonical_events'"
    ).fetchone()
    if not exists:
        return []
    cutoff = now - timedelta(hours=float(cfg["max_news_age_hours"]))
    allowed_types = {str(v).lower() for v in cfg["allowed_event_types"]}
    blocked_types = {str(v).lower() for v in cfg["blocked_event_types"]}
    qualities = {str(v).lower() for v in cfg["allowed_source_qualities"]}
    content = {str(v).lower() for v in cfg["allowed_content_levels"]}
    rows = conn.execute(
        "SELECT * FROM news_canonical_events WHERE asset_class='stocks' "
        "AND linkage_allowed=1 AND is_cluster_primary=1 ORDER BY published_at DESC"
    ).fetchall()
    out = []
    for raw in rows:
        event = dict(raw)
        published = _parse_ts(event.get("published_at"))
        if published is None or published < cutoff or published > now + timedelta(minutes=2):
            continue
        expires = _parse_ts(event.get("expires_at"))
        if expires is not None and expires < now:
            continue
        event_type = str(event.get("event_type") or "").lower()
        if event_type in blocked_types or event_type not in allowed_types:
            continue
        if str(event.get("source_quality") or "").lower() not in qualities:
            continue
        if str(event.get("content_level") or "").lower() not in content:
            continue
        if _float(event.get("confidence")) < float(cfg["min_news_confidence"]):
            continue
        if str(event.get("direction_hint") or "") not in {"bullish", "bearish"}:
            continue
        try:
            symbols = json.loads(event.get("trusted_symbols_json") or "[]")
        except (TypeError, ValueError, json.JSONDecodeError):
            symbols = []
        event["trusted_tickers"] = sorted({
            str(value).split("/", 1)[0].upper() for value in symbols if value
        })
        if not event["trusted_tickers"]:
            continue
        out.append(event)
    return out


def _signal_cap_reasons(raw: dict[str, Any]) -> list[str]:
    return [str(value) for value in (raw.get("cap_reasons") or []) if value]


def _only_session_cap(reasons: Iterable[str]) -> bool:
    for reason in reasons:
        low = str(reason).lower()
        if PLAN_MARKER in low:
            continue
        if "tier demoted" in low and PLAN_MARKER in low:
            continue
        return False
    return True


def _latest_signal(
    conn: sqlite3.Connection,
    *,
    ticker: str,
    direction: str,
    event: dict[str, Any],
    now: datetime,
    cfg: dict[str, Any],
) -> dict[str, Any] | None:
    rows = conn.execute(
        "SELECT * FROM proposed_signals WHERE asset_class='stocks' AND mode='intraday' "
        "AND symbol=? AND direction=? AND created_at<=? ORDER BY created_at DESC LIMIT 30",
        (ticker, direction, _iso(now)),
    ).fetchall()
    event_at = _parse_ts(event.get("published_at")) or now
    max_age = timedelta(hours=float(cfg["max_source_signal_age_hours"]))
    allowed_setups = {str(value).lower() for value in cfg["allowed_setup_types"]}
    for raw_row in rows:
        signal = dict(raw_row)
        created = _parse_ts(signal.get("created_at"))
        if created is None or now - created > max_age:
            continue
        # The strategy must have been recomputed after the catalyst appeared.
        if created < event_at - timedelta(minutes=2):
            continue
        raw = _json(signal.get("raw_idea_json"))
        tier = str(raw.get("pre_gate_tier") or signal.get("tier") or "").upper()
        if cfg.get("require_pre_gate_ab", True) and tier not in {"A", "B"}:
            continue
        if _float(signal.get("score")) < float(cfg["min_source_score"]):
            continue
        if str(signal.get("setup_type") or "").lower() not in allowed_setups:
            continue
        reasons = _signal_cap_reasons(raw)
        if str(signal.get("tier") or "").upper() not in {"A", "B"} and not _only_session_cap(reasons):
            continue
        news = raw.get("news_influence_contract") or {}
        if not news.get("supported"):
            continue
        if str(news.get("event_type") or "") != str(event.get("event_type") or ""):
            continue
        if str(news.get("direction_hint") or "") != str(event.get("direction_hint") or ""):
            continue
        signal["_raw"] = raw
        signal["_pre_gate_tier"] = tier
        return signal
    return None


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone() is not None


def _preus_actionable_candidates(
    conn: sqlite3.Connection,
    *,
    now: datetime,
    cfg: dict[str, Any],
) -> list[tuple[dict[str, Any], dict[str, Any], str | None]]:
    """Return today's materialized pre-US permissions with an auditable outcome.

    The source signal remains immutable. This route deliberately consumes only
    the server-side ``ACTIONABLE`` permission, whose validity window and hard
    gates were computed by ``stocks_preus_review``. It never treats an ordinary
    C-tier overnight plan as executable.
    """
    if not _table_exists(conn, "stocks_preus_actionability"):
        return []

    snapshot_tier = "NULL AS snapshot_pre_gate_tier"
    if _table_exists(conn, "stocks_paper_decision_snapshots"):
        snapshot_tier = (
            "(SELECT s.pre_gate_tier FROM stocks_paper_decision_snapshots s "
            "WHERE s.signal_id=p.signal_id ORDER BY s.decision_at DESC LIMIT 1) "
            "AS snapshot_pre_gate_tier"
        )
    rows = conn.execute(
        "SELECT p.*,a.target_session_open_at,a.target_session_close_at,"
        "a.effective_score,a.effective_tier,a.valid_until,a.current_signal_updated_at,"
        "a.source_fingerprint,a.geometry_json,"
        f"{snapshot_tier} "
        "FROM stocks_preus_actionability a "
        "JOIN proposed_signals p ON p.signal_id=a.signal_id "
        "WHERE a.decision='ACTIONABLE' AND a.valid_until>=? "
        "AND p.asset_class='stocks' AND p.mode='intraday'",
        (_iso(now),),
    ).fetchall()
    allowed_setups = {str(value).lower() for value in cfg["allowed_setup_types"]}
    allowed_directions = {str(value).lower() for value in cfg["allowed_directions"]}
    current_session = now.astimezone(NY).date()
    result: list[tuple[dict[str, Any], dict[str, Any], str | None]] = []

    for raw_row in rows:
        signal = dict(raw_row)
        # Compare a pre-US permission with the source content, not merely with
        # its housekeeping timestamp. See `source_decision_fingerprint`.
        from src.execution.stocks_preus_review import source_decision_fingerprint
        current_source_fingerprint = source_decision_fingerprint(signal)
        target_open = _parse_ts(signal.get("target_session_open_at"))
        if target_open is None or target_open.astimezone(NY).date() != current_session:
            continue
        try:
            geometry = json.loads(signal.get("geometry_json") or "{}")
        except (TypeError, ValueError, json.JSONDecodeError):
            geometry = {}
        raw = _json(signal.get("raw_idea_json"))
        pre_gate = str(
            signal.get("snapshot_pre_gate_tier") or raw.get("pre_gate_tier") or ""
        ).upper()
        effective_tier = str(signal.get("effective_tier") or "").upper()
        effective_score = _float(signal.get("effective_score"))
        signal.update({
            "tier": effective_tier,
            "score": effective_score,
            "suggested_entry": geometry.get("suggested_entry"),
            "entry_trigger": geometry.get("entry_trigger"),
            "entry_low": geometry.get("entry_low"),
            "stop_loss": geometry.get("stop_loss"),
            "invalidation": geometry.get("invalidation"),
            "tp1": geometry.get("tp1"),
            "tp2": geometry.get("tp2"),
            "tp3": geometry.get("tp3"),
            "_raw": raw,
            "_pre_gate_tier": pre_gate,
            "_preus_actionability": {
                "target_session_open_at": signal.get("target_session_open_at"),
                "valid_until": signal.get("valid_until"),
                "effective_tier": effective_tier,
                "effective_score": effective_score,
                "reviewed_source_fingerprint": str(signal.get("source_fingerprint") or ""),
                "current_source_fingerprint": current_source_fingerprint,
            },
            "_reviewed_source_fingerprint": str(signal.get("source_fingerprint") or ""),
            "_current_source_fingerprint": current_source_fingerprint,
        })
        direction = str(signal.get("direction") or "").lower()
        reason: str | None = None
        if cfg.get("require_pre_gate_ab", True) and pre_gate not in {"A", "B"}:
            reason = "PREUS_PRE_GATE_NOT_AB"
        elif effective_tier not in {"A", "B"}:
            reason = "PREUS_EFFECTIVE_TIER_NOT_AB"
        elif effective_score < float(cfg["min_source_score"]):
            reason = "PREUS_EFFECTIVE_SCORE_BELOW_MIN"
        elif direction not in allowed_directions:
            reason = "PREUS_DIRECTION_NOT_ALLOWED"
        elif str(signal.get("setup_type") or "").lower() not in allowed_setups:
            reason = "PREUS_SETUP_NOT_ALLOWED"
        else:
            reviewed_fingerprint = str(signal.get("source_fingerprint") or "")
            if reviewed_fingerprint:
                if reviewed_fingerprint != current_source_fingerprint:
                    reason = "PREUS_SOURCE_CHANGED_AFTER_REVIEW"
            elif (
                signal.get("updated_at")
                and signal.get("current_signal_updated_at")
                and str(signal["updated_at"]) != str(signal["current_signal_updated_at"])
            ):
                # Legacy rows predate content fingerprints. Keep their old,
                # stricter timestamp behaviour rather than silently widening
                # a permission we cannot verify.
                reason = "PREUS_SOURCE_CHANGED_AFTER_REVIEW"

        session_key = target_open.astimezone(NY).date().isoformat()
        event = {
            "event_id": f"preus_actionability:{signal.get('signal_id')}:{session_key}",
            "published_at": signal.get("target_session_open_at"),
            "event_type": "preus_actionability",
            "source": "stocks_preus_actionability",
            "confidence": 1.0,
            "route": "preus_actionability",
        }
        result.append((signal, event, reason))
    return result


def _source_signal_snapshot(signal: dict[str, Any]) -> dict[str, Any]:
    raw = signal.get("_raw") or _json(signal.get("raw_idea_json"))
    return {
        "signal_id": signal.get("signal_id"),
        "symbol": signal.get("symbol"),
        "direction": signal.get("direction"),
        "mode": signal.get("mode"),
        "status": signal.get("status"),
        "tier": signal.get("tier"),
        "score": signal.get("score"),
        "pre_gate_tier": signal.get("_pre_gate_tier") or raw.get("pre_gate_tier"),
        "setup_type": signal.get("setup_type"),
        "created_at": signal.get("created_at"),
        "updated_at": signal.get("updated_at"),
        "source_fingerprint_reviewed": (
            signal.get("_reviewed_source_fingerprint")
            or signal.get("source_fingerprint")
        ),
        "source_fingerprint_current": signal.get("_current_source_fingerprint"),
        "geometry": {
            "suggested_entry": signal.get("suggested_entry"),
            "entry_trigger": signal.get("entry_trigger"),
            "entry_low": signal.get("entry_low"),
            "entry_high": signal.get("entry_high"),
            "stop_loss": signal.get("stop_loss"),
            "invalidation": signal.get("invalidation"),
            "tp1": signal.get("tp1"),
            "tp2": signal.get("tp2"),
            "tp3": signal.get("tp3"),
        },
        "raw_context": {
            "cap_reasons": raw.get("cap_reasons"),
            "structured": raw.get("structured"),
            "setup": raw.get("setup"),
            "intraday_actionability": raw.get("intraday_actionability"),
            "catalyst_meta": raw.get("catalyst_meta"),
            "paper_entry_profile": raw.get("paper_entry_profile"),
            "paper_entry_confirmation": raw.get("paper_entry_confirmation"),
            "news_influence_contract": raw.get("news_influence_contract"),
        },
    }


def _store_preus_rejection(
    conn: sqlite3.Connection,
    *,
    signal: dict[str, Any],
    event: dict[str, Any],
    now: datetime,
    cfg: dict[str, Any],
    reason: str,
) -> None:
    row = _rejection_row(signal=signal, event=event, now=now, cfg=cfg, reason=reason)
    row["snapshot_json"] = json.dumps({
        "reason": reason,
        "route": "preus_actionability",
        "actionability": signal.get("_preus_actionability") or {},
        "source_signal": _source_signal_snapshot(signal),
    }, sort_keys=True)
    _store_order(conn, row)


def _round_step(value: float, step: float, *, upward: bool = False) -> float:
    if step <= 0:
        return value
    units = value / step
    rounded = math.ceil(units - 1e-12) if upward else math.floor(units + 1e-12)
    return round(rounded * step, max(0, min(12, int(abs(math.log10(step))) + 2)))


def _target_rs(signal: dict[str, Any], cfg: dict[str, Any]) -> tuple[float, float, float]:
    entry = _float(
        signal.get("suggested_entry") or signal.get("entry_trigger") or signal.get("entry_low")
    )
    stop = _float(signal.get("stop_loss") or signal.get("invalidation"))
    risk = abs(entry - stop)
    defaults = tuple(float(v) for v in cfg["default_target_r"])
    if entry <= 0 or risk <= 0:
        return defaults
    out: list[float] = []
    direction = str(signal.get("direction") or "long").lower()
    for index, key in enumerate(("tp1", "tp2", "tp3")):
        target = _float(signal.get(key))
        if target <= 0:
            out.append(defaults[index])
            continue
        r_value = ((target - entry) / risk if direction == "long" else (entry - target) / risk)
        out.append(r_value if r_value > 0 else defaults[index])
    out[1] = max(out[1], out[0] + 0.5)
    out[2] = max(out[2], out[1] + 0.75)
    return tuple(out[:3])  # type: ignore[return-value]


def _market_range(
    client: MexcFuturesClient,
    symbol: str,
    now: datetime,
    cfg: dict[str, Any],
) -> tuple[float, float]:
    start = now - timedelta(minutes=int(cfg["premarket_range_minutes"]))
    rows = client.klines(
        symbol,
        start_seconds=int(start.timestamp()),
        end_seconds=int(now.timestamp()),
        interval="Min1",
    )
    highs = [_float(row.get("high")) for row in rows if _float(row.get("high")) > 0]
    lows = [_float(row.get("low")) for row in rows if _float(row.get("low")) > 0]
    if not highs or not lows:
        raise ValueError("mexc_range_missing")
    return max(highs), min(lows)


def _plan_prices(
    *,
    signal: dict[str, Any],
    contract: dict[str, Any],
    quote: Quote,
    client: MexcFuturesClient,
    now: datetime,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    direction = str(signal.get("direction") or "long").lower()
    setup = str(signal.get("setup_type") or "").lower()
    tick = _float(contract.get("price_unit"), 0.01)
    source_entry = _float(
        signal.get("suggested_entry") or signal.get("entry_trigger") or signal.get("entry_low")
    )
    source_stop = _float(signal.get("stop_loss") or signal.get("invalidation"))
    if source_entry <= 0 or source_stop <= 0:
        raise ValueError("source_geometry_missing")
    stop_pct = abs(source_entry - source_stop) / source_entry
    original_stop_pct = stop_pct
    stop_normalization = None
    if stop_pct < float(cfg["min_stop_distance_pct"]):
        if not bool(cfg.get("normalize_too_tight_source_stop", True)):
            raise ValueError("source_stop_too_tight")
        stop_pct = float(cfg["min_stop_distance_pct"])
        stop_normalization = "source_stop_too_tight_normalized_to_min_distance"
    if stop_pct > float(cfg["max_stop_distance_pct"]):
        raise ValueError("source_stop_too_wide")
    source_drift = abs(quote.index - source_entry) / source_entry * 10_000.0
    if source_drift > float(cfg["max_source_entry_drift_bps"]):
        raise ValueError("mexc_source_entry_drift_too_large")

    if setup in {str(v).lower() for v in cfg["pullback_setup_types"]}:
        entry_mode = "PULLBACK_LIMIT"
        offset = float(cfg["pullback_offset_bps"]) / 10_000.0
        raw_limit = quote.bid * (1.0 - offset) if direction == "long" else quote.ask * (1.0 + offset)
        limit_price = _round_step(raw_limit, tick, upward=direction == "short")
        trigger_price = None
        entry_anchor = limit_price
        order_type = "maker"
    else:
        entry_mode = "BREAKOUT_CONTINUATION"
        high, low = _market_range(client, str(contract["mexc_symbol"]), now, cfg)
        cushion = float(cfg["breakout_limit_cushion_bps"]) / 10_000.0
        if direction == "long":
            trigger_price = _round_step(max(high, quote.ask) + tick, tick, upward=True)
            limit_price = _round_step(trigger_price * (1.0 + cushion), tick, upward=True)
        else:
            trigger_price = _round_step(min(low, quote.bid) - tick, tick, upward=False)
            limit_price = _round_step(trigger_price * (1.0 - cushion), tick, upward=False)
        entry_anchor = trigger_price
        order_type = "taker"

    risk_abs = entry_anchor * stop_pct
    target_rs = (
        tuple(float(v) for v in cfg["default_target_r"])
        if stop_normalization
        else _target_rs(signal, cfg)
    )
    if direction == "long":
        stop = _round_step(entry_anchor - risk_abs, tick, upward=False)
        targets = [_round_step(entry_anchor + risk_abs * r, tick, upward=False) for r in target_rs]
    else:
        stop = _round_step(entry_anchor + risk_abs, tick, upward=True)
        targets = [_round_step(entry_anchor - risk_abs * r, tick, upward=True) for r in target_rs]
    return {
        "entry_mode": entry_mode,
        "trigger_price": trigger_price,
        "limit_price": limit_price,
        "stop_price": stop,
        "tp1": targets[0],
        "tp2": targets[1],
        "tp3": targets[2],
        "source_entry": source_entry,
        "source_stop": source_stop,
        "source_drift_bps": source_drift,
        "source_stop_pct": original_stop_pct,
        "effective_stop_pct": stop_pct,
        "stop_normalization": stop_normalization,
        "entry_order_type": order_type,
    }


def _order_id(strategy_id: str, signal_id: str, event_id: str) -> str:
    digest = hashlib.sha256(f"{strategy_id}|{signal_id}|{event_id}".encode("utf-8")).hexdigest()[:20]
    return f"msp_{digest}"


def _store_order(conn: sqlite3.Connection, row: dict[str, Any]) -> None:
    values = {column: row.get(column) for column in _ORDER_COLS}
    conn.execute(
        f"INSERT INTO mexc_stock_futures_paper_orders({','.join(_ORDER_COLS)}) "
        f"VALUES({','.join('?' for _ in _ORDER_COLS)}) "
        "ON CONFLICT(source_signal_id,event_id,strategy_id) DO UPDATE SET "
        "status=excluded.status,reject_reason=excluded.reject_reason,"
        "mexc_symbol=excluded.mexc_symbol,entry_mode=excluded.entry_mode,"
        "trigger_price=excluded.trigger_price,limit_price=excluded.limit_price,"
        "stop_price=excluded.stop_price,tp1=excluded.tp1,tp2=excluded.tp2,tp3=excluded.tp3,"
        "source_drift_bps=excluded.source_drift_bps,spread_bps=excluded.spread_bps,"
        "fair_index_deviation_bps=excluded.fair_index_deviation_bps,"
        "funding_rate=excluded.funding_rate,hold_volume=excluded.hold_volume,"
        "top5_depth_usdt=excluded.top5_depth_usdt,expires_at=excluded.expires_at,"
        "replacement_count=excluded.replacement_count,last_evaluated_at=excluded.last_evaluated_at,"
        "last_error=excluded.last_error,snapshot_json=excluded.snapshot_json,"
        "updated_at=excluded.updated_at "
        "WHERE mexc_stock_futures_paper_orders.status<>'FILLED'",
        tuple(values[column] for column in _ORDER_COLS),
    )


def _rejection_row(
    *,
    signal: dict[str, Any],
    event: dict[str, Any],
    now: datetime,
    cfg: dict[str, Any],
    reason: str,
    contract: dict[str, Any] | None = None,
    quote: Quote | None = None,
) -> dict[str, Any]:
    strategy = str(cfg["strategy_id"])
    signal_id = str(signal.get("signal_id") or "")
    event_id = str(event.get("event_id") or "")
    raw = signal.get("_raw") or _json(signal.get("raw_idea_json"))
    return {
        "order_id": _order_id(strategy, signal_id, event_id),
        "strategy_id": strategy,
        "paper_lane": str(cfg["paper_lane"]),
        "source_signal_id": signal_id,
        "event_id": event_id,
        "session_date": _session_date(now),
        "ticker": str(signal.get("symbol") or "").upper(),
        "mexc_symbol": contract.get("mexc_symbol") if contract else None,
        "direction": str(signal.get("direction") or "").lower(),
        "source_pre_gate_tier": str(raw.get("pre_gate_tier") or signal.get("tier") or ""),
        "source_score": _float(signal.get("score")),
        "setup_type": str(signal.get("setup_type") or ""),
        "entry_mode": None,
        "status": "REJECTED",
        "reject_reason": reason,
        "decision_at": _iso(now),
        "event_published_at": event.get("published_at"),
        "event_type": event.get("event_type"),
        "event_source": event.get("source"),
        "event_confidence": _float(event.get("confidence")),
        "spread_bps": quote.spread_bps if quote else None,
        "funding_rate": quote.funding_rate if quote else None,
        "hold_volume": quote.hold_volume if quote else None,
        "top5_depth_usdt": quote.top5_depth_usdt if quote else None,
        "price_unit": contract.get("price_unit") if contract else None,
        "vol_unit": contract.get("vol_unit") if contract else None,
        "min_vol": contract.get("min_vol") if contract else None,
        "contract_size": contract.get("contract_size") if contract else None,
        "contract_max_leverage": contract.get("max_leverage") if contract else None,
        "replacement_count": 0,
        "snapshot_json": json.dumps({
            "reason": reason,
            "event": {k: event.get(k) for k in (
                "event_id", "title", "source", "published_at", "event_type",
                "direction_hint", "source_quality", "content_level", "confidence",
            )},
            "preus_actionability": signal.get("_preus_actionability") or None,
            "source_signal": _source_signal_snapshot(signal),
        }, sort_keys=True),
        "created_at": _iso(now),
        "updated_at": _iso(now),
    }


def _stage_signal_event(
    conn: sqlite3.Connection,
    *,
    signal: dict[str, Any],
    event: dict[str, Any],
    contracts: dict[str, dict[str, Any]],
    client: MexcFuturesClient,
    now: datetime,
    cfg: dict[str, Any],
    explicit_capacity_rejection: bool = False,
) -> str:
    """Stage one already-eligible source and return its durable outcome."""
    ticker = str(signal.get("symbol") or "").upper()
    existing = conn.execute(
        "SELECT * FROM mexc_stock_futures_paper_orders "
        "WHERE source_signal_id=? AND event_id=? AND strategy_id=?",
        (signal["signal_id"], event["event_id"], cfg["strategy_id"]),
    ).fetchone()
    if existing and str(existing["status"]) not in {"EXPIRED", "REJECTED"}:
        return "already_processed"
    replacement = int(existing["replacement_count"] or 0) + 1 if existing else 0
    if existing and replacement > int(cfg["max_replacements"]):
        return "replacement_limit"
    contract = contracts.get(ticker)
    if contract is None:
        _record_quote_health(conn, ticker=ticker, now=now, status="UNHEALTHY",
                             reason="MEXC_STOCK_CONTRACT_UNAVAILABLE")
        _store_order(conn, _rejection_row(
            signal=signal, event=event, now=now, cfg=cfg,
            reason="MEXC_STOCK_CONTRACT_UNAVAILABLE",
        ))
        return "rejected"
    if (
        int(contract.get("state") or 0) not in {int(v) for v in cfg["active_contract_states"]}
        or not bool(contract.get("api_allowed"))
    ):
        _store_order(conn, _rejection_row(
            signal=signal, event=event, now=now, cfg=cfg,
            reason="MEXC_STOCK_CONTRACT_NOT_TRADABLE", contract=contract,
        ))
        return "rejected"
    try:
        quote = fetch_quote(client, contract)
        _update_quote(conn, ticker, quote, now)
        _record_quote_health(conn, ticker=ticker, now=now, status="HEALTHY",
                             contract=contract, quote=quote)
        # `_plan_prices` fetches the current range from the exchange. Do not
        # hold a SQLite writer lease while that request is in flight.
        conn.commit()
    except Exception as exc:
        _record_quote_health(conn, ticker=ticker, now=now, status="UNHEALTHY",
                             reason=f"MEXC_QUOTE_UNAVAILABLE:{type(exc).__name__}",
                             contract=contract)
        _store_order(conn, _rejection_row(
            signal=signal, event=event, now=now, cfg=cfg,
            reason=f"MEXC_QUOTE_UNAVAILABLE:{type(exc).__name__}", contract=contract,
        ))
        return "rejected"
    fair_index_bps = abs(quote.fair - quote.index) / quote.index * 10_000.0
    reject_reason = None
    if fair_index_bps > float(cfg["max_fair_index_deviation_bps"]):
        reject_reason = "MEXC_FAIR_INDEX_DIVERGENCE"
    elif bool(cfg.get("execution_liquidity_gates_enabled", True)):
        if quote.spread_bps > float(cfg["max_spread_bps"]):
            reject_reason = "MEXC_SPREAD_TOO_WIDE"
        elif quote.top5_depth_usdt < float(cfg["min_top5_depth_usdt"]):
            reject_reason = "MEXC_DEPTH_TOO_THIN"
        elif quote.hold_volume < float(cfg["min_hold_volume"]):
            reject_reason = "MEXC_HOLD_VOLUME_TOO_LOW"
    if reject_reason:
        row = _rejection_row(
            signal=signal, event=event, now=now, cfg=cfg,
            reason=reject_reason, contract=contract, quote=quote,
        )
        row["fair_index_deviation_bps"] = fair_index_bps
        _store_order(conn, row)
        return "rejected"
    try:
        prices = _plan_prices(
            signal=signal, contract=contract, quote=quote, client=client,
            now=now, cfg=cfg,
        )
    except Exception as exc:
        row = _rejection_row(
            signal=signal, event=event, now=now, cfg=cfg,
            reason=str(exc), contract=contract, quote=quote,
        )
        row["fair_index_deviation_bps"] = fair_index_bps
        _store_order(conn, row)
        return "rejected"

    session_count = conn.execute(
        "SELECT COUNT(*) FROM mexc_stock_futures_paper_orders "
        "WHERE session_date=? AND ticker=? AND status IN ('STAGED','TRIGGERED','FILLED')",
        (_session_date(now), ticker),
    ).fetchone()[0]
    if session_count >= int(cfg["max_orders_per_symbol_session"]) and not existing:
        if not explicit_capacity_rejection:
            return "capacity_skipped"
        _store_order(conn, _rejection_row(
            signal=signal, event=event, now=now, cfg=cfg,
            reason="MAX_ORDERS_PER_SYMBOL_SESSION", contract=contract, quote=quote,
        ))
        return "rejected"
    order_ttl = float(cfg["order_ttl_minutes"])
    if _is_preus_actionability_order({"event_source": event.get("source")}):
        # A standard 25-minute TTL can expire while the first opening bar is
        # being evaluated. Retain the reviewed plan only until that decision.
        order_ttl = max(order_ttl, float(cfg.get("preopen_order_ttl_minutes", order_ttl)))
    expires = min(
        now + timedelta(minutes=order_ttl),
        _force_flat_at(now, cfg),
    )
    order = _rejection_row(
        signal=signal, event=event, now=now, cfg=cfg,
        reason="", contract=contract, quote=quote,
    )
    order.update(prices)
    order.update({
        "status": "STAGED",
        "reject_reason": None,
        "fair_index_deviation_bps": fair_index_bps,
        "expires_at": _iso(expires),
        "replacement_count": replacement,
        "snapshot_json": json.dumps({
            "paper_only": True,
            "private_mexc_calls_allowed": False,
            "source_route": event.get("route") or "canonical_event",
            "event": {k: event.get(k) for k in (
                "event_id", "title", "source", "published_at", "event_type",
                "direction_hint", "source_quality", "content_level", "confidence",
            )},
            "preus_actionability": signal.get("_preus_actionability") or None,
            "quote": quote.__dict__,
            "source_signal": {
                **_source_signal_snapshot(signal),
            },
            "entry_order_type": prices["entry_order_type"],
            "stop_normalization": prices.get("stop_normalization"),
        }, sort_keys=True),
    })
    _store_order(conn, order)
    return "staged"


def stage_candidates(
    conn: sqlite3.Connection,
    *,
    client: MexcFuturesClient,
    now: datetime | None = None,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = {**load_cfg(), **(cfg or {})}
    moment = _utc(now)
    empty = {"status": "outside_candidate_window", "evaluated": 0, "staged": 0,
             "rejected": 0, "preus_actionable": 0, "preus_processed": 0}
    if not cfg.get("enabled", False) or not in_candidate_window(moment, cfg):
        return empty
    if str(cfg.get("execution_mode")) != "paper":
        return {**empty, "status": "blocked_non_paper_config"}

    if _catalog_stale(conn, moment, cfg):
        refresh_contract_catalog(conn, client=client, now=moment)
    contracts = {
        str(row["ticker"]): dict(row)
        for row in conn.execute("SELECT * FROM mexc_stock_futures_contracts")
    }
    evaluated = staged = rejected = preus_processed = 0
    seen_signal_ids: set[str] = set()
    for event in _recent_events(conn, moment, cfg):
        direction = "long" if event["direction_hint"] == "bullish" else "short"
        if direction not in {str(v).lower() for v in cfg["allowed_directions"]}:
            continue
        for ticker in event["trusted_tickers"]:
            signal = _latest_signal(
                conn, ticker=ticker, direction=direction, event=event, now=moment, cfg=cfg
            )
            if signal is None:
                continue
            seen_signal_ids.add(str(signal["signal_id"]))
            evaluated += 1
            # The preceding candidate may have written a staged/rejected
            # order. Release it before this candidate requests market data.
            conn.commit()
            outcome = _stage_signal_event(
                conn, signal=signal, event=event, contracts=contracts, client=client,
                now=moment, cfg=cfg,
            )
            conn.commit()
            staged += outcome == "staged"
            rejected += outcome == "rejected"

    preus_candidates = _preus_actionable_candidates(conn, now=moment, cfg=cfg)
    for signal, event, precheck_reason in preus_candidates:
        signal_id = str(signal.get("signal_id") or "")
        if signal_id in seen_signal_ids:
            preus_processed += 1
            continue
        evaluated += 1
        if precheck_reason is not None:
            _store_preus_rejection(
                conn, signal=signal, event=event, now=moment, cfg=cfg,
                reason=precheck_reason,
            )
            rejected += 1
            preus_processed += 1
            continue
        conn.commit()
        outcome = _stage_signal_event(
            conn, signal=signal, event=event, contracts=contracts, client=client,
            now=moment, cfg=cfg, explicit_capacity_rejection=True,
        )
        conn.commit()
        staged += outcome == "staged"
        rejected += outcome == "rejected"
        if outcome not in {"replacement_limit", "capacity_skipped"}:
            preus_processed += 1
    return {
        "status": "ok", "evaluated": evaluated, "staged": staged, "rejected": rejected,
        "preus_actionable": len(preus_candidates), "preus_processed": preus_processed,
    }


def _et_minutes(value: str) -> int:
    hour, minute = str(value).split(":", 1)
    return int(hour) * 60 + int(minute)


def preopen_health(
    conn: sqlite3.Connection,
    *,
    now: datetime,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """Persist whether today's ACTIONABLE pre-open plans reached MEXC Paper.

    A direct canonical-event route and the materialized pre-US route may both
    process the same source signal.  The health check deliberately keys on the
    source signal id, so either route counts as an auditable hand-off.
    """
    moment = _utc(now)
    session_date = _session_date(moment)
    candidates = _preus_actionable_candidates(conn, now=moment, cfg=cfg)
    signal_ids = sorted({str(signal.get("signal_id") or "") for signal, _, _ in candidates})
    signal_ids = [signal_id for signal_id in signal_ids if signal_id]
    if signal_ids:
        placeholders = ",".join("?" for _ in signal_ids)
        processed = int(conn.execute(
            "SELECT COUNT(DISTINCT source_signal_id) "
            "FROM mexc_stock_futures_paper_orders "
            f"WHERE session_date=? AND source_signal_id IN ({placeholders})",
            (session_date, *signal_ids),
        ).fetchone()[0] or 0)
        staged = int(conn.execute(
            "SELECT COUNT(DISTINCT source_signal_id) "
            "FROM mexc_stock_futures_paper_orders "
            f"WHERE session_date=? AND status IN ('STAGED','TRIGGERED','FILLED') "
            f"AND source_signal_id IN ({placeholders})",
            (session_date, *signal_ids),
        ).fetchone()[0] or 0)
        rejected = int(conn.execute(
            "SELECT COUNT(DISTINCT source_signal_id) "
            "FROM mexc_stock_futures_paper_orders "
            f"WHERE session_date=? AND status='REJECTED' "
            f"AND source_signal_id IN ({placeholders})",
            (session_date, *signal_ids),
        ).fetchone()[0] or 0)
    else:
        processed = staged = rejected = 0

    local = moment.astimezone(NY)
    minute_of_day = local.hour * 60 + local.minute
    alert_after = _et_minutes(str(cfg["preopen_health_alert_after_et"]))
    decision_end = _et_minutes(str(cfg["preopen_decision_end_et"]))
    if not signal_ids:
        status = "NO_ACTIONABLE"
        reason = None
    elif processed:
        status = "OK"
        reason = None
    elif minute_of_day < alert_after:
        status = "PENDING_DECISION_WINDOW"
        reason = "preus_actionable_candidates_not_yet_due"
    elif minute_of_day <= decision_end:
        status = "ACTIONABLE_UNPROCESSED"
        reason = "preus_actionable_candidates_unprocessed"
    else:
        status = "ACTIONABLE_UNPROCESSED"
        reason = "preus_actionable_candidates_missed_window"

    previous = conn.execute(
        "SELECT status,alerted_at FROM mexc_stock_futures_preopen_health WHERE session_date=?",
        (session_date,),
    ).fetchone()
    alerted_at = previous["alerted_at"] if previous and status == "ACTIONABLE_UNPROCESSED" else None
    row = {
        "session_date": session_date,
        "checked_at": _iso(moment),
        "actionable_count": len(signal_ids),
        "processed_count": processed,
        "staged_count": staged,
        "rejected_count": rejected,
        "status": status,
        "reason": reason,
        "alerted_at": alerted_at,
    }
    conn.execute(
        "INSERT INTO mexc_stock_futures_preopen_health("
        "session_date,checked_at,actionable_count,processed_count,staged_count,"
        "rejected_count,status,reason,alerted_at) VALUES(?,?,?,?,?,?,?,?,?) "
        "ON CONFLICT(session_date) DO UPDATE SET "
        "checked_at=excluded.checked_at,actionable_count=excluded.actionable_count,"
        "processed_count=excluded.processed_count,staged_count=excluded.staged_count,"
        "rejected_count=excluded.rejected_count,status=excluded.status,"
        "reason=excluded.reason,alerted_at=excluded.alerted_at",
        tuple(row[column] for column in (
            "session_date", "checked_at", "actionable_count", "processed_count",
            "staged_count", "rejected_count", "status", "reason", "alerted_at",
        )),
    )
    # The current row powers the watchdog. Keep an immutable run history too:
    # after the decision window expires its current state becomes
    # NO_ACTIONABLE, which must not erase evidence of the morning hand-off.
    conn.execute(
        "INSERT OR IGNORE INTO mexc_stock_futures_preopen_health_history("
        "session_date,checked_at,actionable_count,processed_count,staged_count,"
        "rejected_count,status,reason,alerted_at) VALUES(?,?,?,?,?,?,?,?,?)",
        tuple(row[column] for column in (
            "session_date", "checked_at", "actionable_count", "processed_count",
            "staged_count", "rejected_count", "status", "reason", "alerted_at",
        )),
    )
    return row


def consume_new_preopen_health_alerts(
    conn: sqlite3.Connection,
    *,
    health: dict[str, Any],
    now: datetime,
) -> list[dict[str, Any]]:
    """Return one alert per missed pre-open hand-off and mark it delivered."""
    if health.get("status") != "ACTIONABLE_UNPROCESSED" or health.get("alerted_at"):
        return []
    moment = _utc(now)
    conn.execute(
        "UPDATE mexc_stock_futures_preopen_health SET alerted_at=? WHERE session_date=?",
        (_iso(moment), health["session_date"]),
    )
    result = dict(health)
    result["alerted_at"] = _iso(moment)
    return [result]


def _paper_equity(conn: sqlite3.Connection) -> float:
    active_profile = None
    try:
        from src.execution.paper_portfolio import load_cfg as load_paper_cfg

        paper_cfg = load_paper_cfg()
        active_profile = str(paper_cfg.get("fee_profile") or "")
    except Exception:
        paper_cfg = {}
    try:
        if active_profile:
            row = conn.execute(
                "SELECT equity_after FROM paper_portfolio_ledger "
                "WHERE event_type='exit' AND fee_profile=? ORDER BY rowid DESC LIMIT 1",
                (active_profile,),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT equity_after FROM paper_portfolio_ledger "
                "WHERE event_type='exit' ORDER BY rowid DESC LIMIT 1"
            ).fetchone()
        if row and _float(row[0]) > 0:
            return _float(row[0])
    except sqlite3.OperationalError:
        pass
    try:
        return float(paper_cfg.get("initial_equity_usdt") or 5000.0)
    except Exception:
        return 5000.0


def _active_risk(conn: sqlite3.Connection) -> tuple[int, float]:
    row = conn.execute(
        "SELECT COUNT(*),COALESCE(SUM(risk_usdt),0) "
        "FROM mexc_stock_futures_paper_positions WHERE status='OPEN'"
    ).fetchone()
    return int(row[0] or 0), _float(row[1])


def _position_from_fill(
    conn: sqlite3.Connection,
    *,
    order: dict[str, Any],
    fill_at: datetime,
    fill_price: float,
    cfg: dict[str, Any],
) -> dict[str, Any] | None:
    equity = _paper_equity(conn)
    open_count, active_risk = _active_risk(conn)
    risk_multiplier = (
        float(cfg.get("opening_risk_multiplier", 0.50))
        if _opening_protection_applies(order, cfg)
        else 1.0
    )
    effective_risk_pct = float(cfg["risk_per_trade_pct"]) * risk_multiplier
    target_risk = equity * effective_risk_pct
    if open_count >= int(cfg["max_open_positions"]):
        return None
    if active_risk + target_risk > equity * float(cfg["max_concurrent_risk_pct"]) + 1e-9:
        return None
    stop = _float(order["stop_price"])
    max_lev = min(int(cfg["max_leverage"]), int(order.get("contract_max_leverage") or 1))
    sizing = size_position(
        equity_usdt=equity,
        entry_price=fill_price,
        stop_price=stop,
        direction=str(order["direction"]),
        risk_pct=effective_risk_pct,
        max_leverage=max_lev,
        max_margin_pct=float(cfg["max_margin_per_trade_pct"]),
        max_notional_pct=float(cfg["max_notional_per_trade_pct"]),
        liquidation_buffer_to_stop=float(cfg["liquidation_buffer_to_stop"]),
    )
    if sizing.skip_recommended or sizing.qty <= 0:
        return None
    contract_size = _float(order.get("contract_size"), 1.0)
    vol_unit = _float(order.get("vol_unit"), 1.0)
    min_vol = _float(order.get("min_vol"), 1.0)
    raw_volume = sizing.qty / contract_size
    volume = math.floor(raw_volume / vol_unit + 1e-12) * vol_unit
    if volume < min_vol:
        return None
    qty = volume * contract_size
    risk_usdt = qty * abs(fill_price - stop)
    notional = qty * fill_price
    if risk_usdt <= 0:
        return None
    now_iso = _iso(fill_at)
    position_id = f"msp_pos_{str(order['order_id']).removeprefix('msp_')}"
    snapshot = _json(order.get("snapshot_json"))
    row = {
        "position_id": position_id,
        "order_id": order["order_id"],
        "strategy_id": order["strategy_id"],
        "paper_lane": order["paper_lane"],
        "source_signal_id": order["source_signal_id"],
        "event_id": order["event_id"],
        "ticker": order["ticker"],
        "mexc_symbol": order["mexc_symbol"],
        "direction": order["direction"],
        "entry_mode": order["entry_mode"],
        "status": "OPEN",
        "entry_at": now_iso,
        "entry_price": fill_price,
        "stop_initial": stop,
        "stop_current": stop,
        "tp1": _float(order["tp1"]),
        "tp2": _float(order["tp2"]),
        "tp3": _float(order["tp3"]),
        "qty": qty,
        "contract_volume": volume,
        "contract_size": contract_size,
        "risk_usdt": risk_usdt,
        "risk_pct": risk_usdt / equity,
        "notional_usdt": notional,
        "margin_used_usdt": notional / max(1, sizing.leverage_used),
        "leverage_used": sizing.leverage_used,
        "funding_rate_at_entry": order.get("funding_rate"),
        "hold_volume_at_entry": order.get("hold_volume"),
        "highest_tp_touched": 0,
        "remaining_weight": 1.0,
        "realized_r_accum": 0.0,
        "max_favorable_r": 0.0,
        "max_adverse_r": 0.0,
        "protection_stage": "INITIAL",
        "last_evaluated_at": now_iso,
        "exit_at": None,
        "exit_price": None,
        "paper_execution_r": None,
        "close_reason": None,
        "fee_profile": str(cfg["fee_profile"]),
        "entry_order_type": str(snapshot.get("entry_order_type") or "taker"),
        "evidence_class": "forward_post_activation",
        "created_at": now_iso,
        "updated_at": now_iso,
    }
    conn.execute(
        f"INSERT INTO mexc_stock_futures_paper_positions({','.join(_POSITION_COLS)}) "
        f"VALUES({','.join('?' for _ in _POSITION_COLS)})",
        tuple(row[column] for column in _POSITION_COLS),
    )
    return row


def _candle_time(candle: dict[str, Any]) -> datetime:
    raw = candle.get("candle_at")
    value = _float(raw)
    if value > 10_000_000_000:
        value /= 1000.0
    return datetime.fromtimestamp(value, tz=UTC)


def _order_fill(
    order: dict[str, Any],
    candles: Iterable[dict[str, Any]],
    *,
    not_before: datetime | None = None,
) -> tuple[str, datetime | None, float | None]:
    direction = str(order["direction"])
    mode = str(order["entry_mode"])
    status = str(order["status"])
    trigger = _float(order.get("trigger_price"))
    limit_price = _float(order["limit_price"])
    stop = _float(order["stop_price"])
    for candle in sorted(candles, key=_candle_time):
        op = _float(candle.get("open"))
        high = _float(candle.get("high"))
        low = _float(candle.get("low"))
        at = _candle_time(candle)
        if not_before is not None and at < not_before:
            continue
        stop_hit = low <= stop if direction == "long" else high >= stop
        if mode == "PULLBACK_LIMIT":
            touched = low <= limit_price if direction == "long" else high >= limit_price
            if touched:
                # If entry and stop are both touched in one 1m candle, count
                # the conservative loss. Treating it as "invalidated before
                # entry" would silently remove the worst fills from evidence.
                return ("FILLED_STOP" if stop_hit else "FILLED"), at, limit_price
            if stop_hit:
                return "INVALIDATED", at, None
            continue
        if status == "STAGED":
            crossed = high >= trigger if direction == "long" else low <= trigger
            if not crossed:
                if stop_hit:
                    return "INVALIDATED", at, None
                continue
            status = "TRIGGERED"
        if status == "TRIGGERED":
            if direction == "long":
                if op > limit_price and low > limit_price:
                    if stop_hit:
                        return "INVALIDATED", at, None
                    continue
                fill = min(limit_price, max(trigger, op if op > 0 else trigger))
            else:
                if op < limit_price and high < limit_price:
                    if stop_hit:
                        return "INVALIDATED", at, None
                    continue
                fill = max(limit_price, min(trigger, op if op > 0 else trigger))
            return ("FILLED_STOP" if stop_hit else "FILLED"), at, fill
    return status, None, None


def _close_position(
    position: dict[str, Any],
    *,
    exit_at: datetime,
    exit_price: float,
    close_reason: str,
    terminal_r: float,
) -> dict[str, Any]:
    row = dict(position)
    row.update({
        "status": "CLOSED",
        "exit_at": _iso(exit_at),
        "exit_price": exit_price,
        "paper_execution_r": terminal_r,
        "close_reason": close_reason,
        "last_evaluated_at": _iso(exit_at),
        "updated_at": _iso(exit_at),
    })
    return row


def _process_position_candles(
    position: dict[str, Any],
    candles: Iterable[dict[str, Any]],
    *,
    cfg: dict[str, Any],
    force_flat_at: datetime,
) -> dict[str, Any]:
    row = dict(position)
    entry = _float(row["entry_price"])
    risk_abs = abs(entry - _float(row["stop_initial"]))
    if risk_abs <= 0:
        return row
    long = str(row["direction"]) == "long"
    weights = [float(v) for v in (cfg.get("partial_take_profit") or {}).get(
        "weights", [0.33, 0.33, 0.34]
    )]
    model = cfg.get("model_f") or {}
    arm_r = float(model.get("arm_breakeven_at_r", 0.6))
    lock_r = float(model.get("lock_profit_at_r", 1.0))
    lock_level = float(model.get("lock_level_r", 0.5))

    for candle in sorted(candles, key=_candle_time):
        at = _candle_time(candle)
        if at <= (_parse_ts(row.get("last_evaluated_at")) or _parse_ts(row["entry_at"]) or at):
            continue
        op, high, low, close = (
            _float(candle.get("open")), _float(candle.get("high")),
            _float(candle.get("low")), _float(candle.get("close")),
        )
        if at >= force_flat_at:
            # The timestamp is the start of the one-minute candle. Exit at
            # its open so no post-15:55 price movement can leak into the
            # same-day strategy's official outcome.
            time_exit = op if op > 0 else close
            exit_r = (
                (time_exit - entry) / risk_abs
                if long
                else (entry - time_exit) / risk_abs
            )
            total_r = (
                _float(row["realized_r_accum"])
                + _float(row["remaining_weight"]) * exit_r
            )
            return _close_position(
                row,
                exit_at=at,
                exit_price=time_exit,
                close_reason="same_day_time_exit",
                terminal_r=total_r,
            )
        favorable = (high - entry) / risk_abs if long else (entry - low) / risk_abs
        adverse = (entry - low) / risk_abs if long else (high - entry) / risk_abs
        row["max_favorable_r"] = max(_float(row["max_favorable_r"]), favorable)
        row["max_adverse_r"] = max(_float(row["max_adverse_r"]), adverse)

        # Conservative path rule: an active stop wins any same-bar ambiguity.
        stop = _float(row["stop_current"])
        stop_hit = low <= stop if long else high >= stop
        if stop_hit:
            stop_r = (stop - entry) / risk_abs if long else (entry - stop) / risk_abs
            total_r = _float(row["realized_r_accum"]) + _float(row["remaining_weight"]) * stop_r
            return _close_position(
                row, exit_at=at, exit_price=stop,
                close_reason=("original_stop" if row["protection_stage"] == "INITIAL"
                              else "protective_stop"),
                terminal_r=total_r,
            )

        highest = int(row["highest_tp_touched"] or 0)
        for index, key in enumerate(("tp1", "tp2", "tp3"), start=1):
            if index <= highest:
                continue
            target = _float(row[key])
            touched = high >= target if long else low <= target
            if not touched:
                break
            target_r = (target - entry) / risk_abs if long else (entry - target) / risk_abs
            weight = weights[index - 1]
            row["realized_r_accum"] = _float(row["realized_r_accum"]) + weight * target_r
            row["remaining_weight"] = max(0.0, _float(row["remaining_weight"]) - weight)
            row["highest_tp_touched"] = index
            highest = index
        if highest >= 3 or _float(row["remaining_weight"]) <= 1e-9:
            return _close_position(
                row, exit_at=at, exit_price=_float(row["tp3"]),
                close_reason="tp3", terminal_r=_float(row["realized_r_accum"]),
            )

        mfe = _float(row["max_favorable_r"])
        if mfe >= lock_r:
            protected = entry + risk_abs * lock_level if long else entry - risk_abs * lock_level
            if long:
                row["stop_current"] = max(_float(row["stop_current"]), protected)
            else:
                row["stop_current"] = min(_float(row["stop_current"]), protected)
            row["protection_stage"] = "LOCK_PROFIT"
        elif mfe >= arm_r:
            if long:
                row["stop_current"] = max(_float(row["stop_current"]), entry)
            else:
                row["stop_current"] = min(_float(row["stop_current"]), entry)
            row["protection_stage"] = "BREAKEVEN"

        row["last_evaluated_at"] = _iso(at)
        row["updated_at"] = _iso(at)
    return row


def _save_position(conn: sqlite3.Connection, row: dict[str, Any]) -> None:
    updates = (
        "status", "stop_current", "highest_tp_touched", "remaining_weight",
        "realized_r_accum", "max_favorable_r", "max_adverse_r",
        "protection_stage", "last_evaluated_at", "exit_at", "exit_price",
        "paper_execution_r", "close_reason", "updated_at",
    )
    conn.execute(
        "UPDATE mexc_stock_futures_paper_positions SET "
        + ",".join(f"{column}=?" for column in updates)
        + " WHERE position_id=?",
        tuple(row.get(column) for column in updates) + (row["position_id"],),
    )


def process_active(
    conn: sqlite3.Connection,
    *,
    client: MexcFuturesClient,
    now: datetime | None = None,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = {**load_cfg(), **(cfg or {})}
    moment = _utc(now)
    filled = expired = invalidated = closed = 0
    fill_rows: list[dict[str, Any]] = []

    orders = [
        dict(row) for row in conn.execute(
            "SELECT * FROM mexc_stock_futures_paper_orders "
            "WHERE status IN ('STAGED','TRIGGERED') "
            "ORDER BY CASE WHEN event_source='stocks_preus_actionability' THEN 0 ELSE 1 END, "
            "source_score DESC, decision_at"
        )
    ]
    for order in orders:
        # `client.klines` below is network I/O. Previous order transitions
        # must not keep a SQLite write transaction open while it is fetched.
        conn.commit()
        expires = _parse_ts(order.get("expires_at"))
        if expires is not None and moment >= expires:
            conn.execute(
                "UPDATE mexc_stock_futures_paper_orders SET status='EXPIRED',"
                "last_evaluated_at=?,updated_at=? WHERE order_id=?",
                (_iso(moment), _iso(moment), order["order_id"]),
            )
            expired += 1
            continue
        start = _parse_ts(order.get("last_evaluated_at") or order.get("decision_at"))
        start = (start or moment - timedelta(minutes=2)) - timedelta(minutes=1)
        if _opening_protection_applies(order, cfg):
            start = min(start, _cash_open_at(moment))
        try:
            candles = client.klines(
                str(order["mexc_symbol"]),
                start_seconds=int(start.timestamp()),
                end_seconds=int(moment.timestamp()),
                interval="Min1",
            )
            confirmation, confirmation_reason, not_before = _opening_confirmation(
                order, candles, now=moment, cfg=cfg
            )
            if confirmation == "pending":
                conn.execute(
                    "UPDATE mexc_stock_futures_paper_orders SET last_evaluated_at=?,updated_at=? "
                    "WHERE order_id=?",
                    (_iso(moment), _iso(moment), order["order_id"]),
                )
                continue
            if confirmation == "failed":
                conn.execute(
                    "UPDATE mexc_stock_futures_paper_orders SET status='INVALIDATED',"
                    "reject_reason=?,last_evaluated_at=?,updated_at=? WHERE order_id=?",
                    (confirmation_reason, _iso(moment), _iso(moment), order["order_id"]),
                )
                invalidated += 1
                continue
            if _opening_protection_applies(order, cfg):
                opening_positions = int(conn.execute(
                    "SELECT COUNT(*) FROM mexc_stock_futures_paper_positions p "
                    "JOIN mexc_stock_futures_paper_orders o ON o.order_id=p.order_id "
                    "WHERE o.session_date=? AND o.event_source='stocks_preus_actionability'",
                    (_session_date(moment),),
                ).fetchone()[0] or 0)
                if opening_positions >= int(cfg.get("opening_max_positions", 1)):
                    conn.execute(
                        "UPDATE mexc_stock_futures_paper_orders SET status='REJECTED',"
                        "reject_reason='OPENING_BASKET_CAP',last_evaluated_at=?,updated_at=? "
                        "WHERE order_id=?",
                        (_iso(moment), _iso(moment), order["order_id"]),
                    )
                    continue
            status, fill_at, fill_price = _order_fill(order, candles, not_before=not_before)
        except Exception as exc:
            conn.execute(
                "UPDATE mexc_stock_futures_paper_orders SET last_error=?,updated_at=? "
                "WHERE order_id=?",
                (f"{type(exc).__name__}:{exc}", _iso(moment), order["order_id"]),
            )
            continue
        if status == "INVALIDATED":
            conn.execute(
                "UPDATE mexc_stock_futures_paper_orders SET status='INVALIDATED',"
                "last_evaluated_at=?,updated_at=? WHERE order_id=?",
                (_iso(fill_at or moment), _iso(moment), order["order_id"]),
            )
            invalidated += 1
            continue
        if status == "TRIGGERED" and order["status"] != "TRIGGERED":
            conn.execute(
                "UPDATE mexc_stock_futures_paper_orders SET status='TRIGGERED',"
                "triggered_at=?,last_evaluated_at=?,updated_at=? WHERE order_id=?",
                (_iso(fill_at or moment), _iso(moment), _iso(moment), order["order_id"]),
            )
        elif status in {"FILLED", "FILLED_STOP"} and fill_at is not None and fill_price is not None:
            position = _position_from_fill(
                conn, order=order, fill_at=fill_at, fill_price=fill_price, cfg=cfg
            )
            if position is None:
                conn.execute(
                    "UPDATE mexc_stock_futures_paper_orders SET status='REJECTED',"
                    "reject_reason='PAPER_RISK_OR_CONTRACT_SIZE_BLOCK',"
                    "last_evaluated_at=?,updated_at=? WHERE order_id=?",
                    (_iso(moment), _iso(moment), order["order_id"]),
                )
                continue
            conn.execute(
                "UPDATE mexc_stock_futures_paper_orders SET status='FILLED',"
                "filled_at=?,fill_price=?,last_evaluated_at=?,updated_at=? WHERE order_id=?",
                (
                    _iso(fill_at), fill_price, _iso(fill_at), _iso(moment),
                    order["order_id"],
                ),
            )
            filled += 1
            if status == "FILLED_STOP":
                position = _close_position(
                    position,
                    exit_at=fill_at,
                    exit_price=_float(position["stop_initial"]),
                    close_reason="same_bar_original_stop",
                    terminal_r=-1.0,
                )
                _save_position(conn, position)
                closed += 1
            fill_rows.append(position)
        else:
            conn.execute(
                "UPDATE mexc_stock_futures_paper_orders SET status=?,"
                "last_evaluated_at=?,updated_at=? WHERE order_id=?",
                (status, _iso(moment), _iso(moment), order["order_id"]),
            )

    positions = [
        dict(row) for row in conn.execute(
            "SELECT * FROM mexc_stock_futures_paper_positions "
            "WHERE status='OPEN' ORDER BY entry_at"
        )
    ]
    for position in positions:
        # Same rule for live Paper-position monitoring: fetch candles without
        # retaining the writer lease from a prior state transition.
        conn.commit()
        start = _parse_ts(position.get("last_evaluated_at") or position.get("entry_at"))
        start = (start or moment - timedelta(minutes=2)) - timedelta(minutes=1)
        try:
            candles = client.klines(
                str(position["mexc_symbol"]),
                start_seconds=int(start.timestamp()),
                end_seconds=int(moment.timestamp()),
                interval="Min1",
            )
        except Exception:
            continue
        entry_at = _parse_ts(position.get("entry_at")) or moment
        position_flat_at = _force_flat_at(entry_at, cfg)
        updated = _process_position_candles(
            position, candles, cfg=cfg, force_flat_at=position_flat_at
        )
        _save_position(conn, updated)
        if position["status"] == "OPEN" and updated["status"] == "CLOSED":
            closed += 1
    return {
        "filled": filled, "expired": expired, "invalidated": invalidated,
        "closed": closed, "fill_rows": fill_rows,
    }


def reconcile_session_symbol_duplicates(
    conn: sqlite3.Connection,
    *,
    now: datetime,
) -> dict[str, int]:
    """Invalidate duplicate unfilled orders while preserving audit history.

    Multiple scheduler processes used to race between the per-symbol capacity
    check and INSERT. Never delete those rows. Keep the strongest/oldest order
    (FILLED, then TRIGGERED, then STAGED) and invalidate only surplus orders
    that have not filled. Duplicate FILLED rows are reported but not rewritten.
    """
    session = _session_date(now)
    rows = [dict(row) for row in conn.execute(
        "SELECT rowid,* FROM mexc_stock_futures_paper_orders "
        "WHERE session_date=? AND status IN ('STAGED','TRIGGERED','FILLED') "
        "ORDER BY ticker,created_at,rowid",
        (session,),
    )]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("ticker") or ""), []).append(row)
    invalidated = unresolved_filled = 0
    priority = {"FILLED": 0, "TRIGGERED": 1, "STAGED": 2}
    for ticker_rows in grouped.values():
        if len(ticker_rows) <= 1:
            continue
        ordered = sorted(
            ticker_rows,
            key=lambda row: (
                priority.get(str(row.get("status") or ""), 9),
                str(row.get("created_at") or ""),
                int(row.get("rowid") or 0),
            ),
        )
        for duplicate in ordered[1:]:
            if str(duplicate.get("status") or "") == "FILLED":
                unresolved_filled += 1
                continue
            conn.execute(
                "UPDATE mexc_stock_futures_paper_orders "
                "SET status='INVALIDATED',reject_reason=?,last_error=?,updated_at=? "
                "WHERE rowid=?",
                (
                    "DUPLICATE_SYMBOL_SESSION_RECONCILED",
                    "concurrent staging race repaired; no fill retained",
                    _iso(now),
                    int(duplicate["rowid"]),
                ),
            )
            invalidated += 1
    return {"invalidated": invalidated, "unresolved_filled": unresolved_filled}


def reconcile_order_position_lifecycle(
    conn: sqlite3.Connection,
    *,
    now: datetime,
) -> dict[str, int]:
    """Keep the source order terminal once a position has been created."""
    rows = conn.execute(
        "SELECT o.order_id,p.entry_at,p.entry_price "
        "FROM mexc_stock_futures_paper_orders o "
        "JOIN mexc_stock_futures_paper_positions p ON p.order_id=o.order_id "
        "WHERE o.status<>'FILLED'"
    ).fetchall()
    for row in rows:
        conn.execute(
            "UPDATE mexc_stock_futures_paper_orders "
            "SET status='FILLED',reject_reason=NULL,filled_at=COALESCE(filled_at,?),"
            "fill_price=COALESCE(fill_price,?),updated_at=? WHERE order_id=?",
            (row["entry_at"], row["entry_price"], _iso(now), row["order_id"]),
        )
    return {"orders_restored_to_filled": len(rows)}


def _tick_with_lease(
    *,
    path: Path,
    moment: datetime,
    public_client: MexcFuturesClient,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    with sqlite3.connect(path, timeout=30.0) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout=30000")
        ensure_tables(conn)
        lifecycle_repair = reconcile_order_position_lifecycle(conn, now=moment)
        duplicate_repair = reconcile_session_symbol_duplicates(conn, now=moment)
        # Catalog/quote paths make public HTTP calls. Finalize the small local
        # repair transaction before entering those network-bound paths.
        conn.commit()
        if _catalog_stale(conn, moment, cfg):
            refresh_contract_catalog(conn, client=public_client, now=moment)
            conn.commit()
        health = probe_quote_health(conn, client=public_client, now=moment, cfg=cfg)
        health_alerts = consume_new_quote_health_alerts(conn, now=moment)
        conn.commit()
        stage = stage_candidates(conn, client=public_client, now=moment, cfg=cfg)
        preopen = preopen_health(conn, now=moment, cfg=cfg)
        preopen_health_alerts = consume_new_preopen_health_alerts(
            conn, health=preopen, now=moment
        )
        conn.commit()
        active = process_active(conn, client=public_client, now=moment, cfg=cfg)
        conn.commit()
    return {
        "status": "ok", "evaluated_at": _iso(moment), "health": health,
        "health_alerts": health_alerts, "duplicate_repair": duplicate_repair,
        "lifecycle_repair": lifecycle_repair,
        "preopen_health": preopen, "preopen_health_alerts": preopen_health_alerts,
        "stage": stage, "active": active,
    }


def tick(
    *,
    db: str | Path | None = None,
    now: datetime | None = None,
    client: MexcFuturesClient | None = None,
    cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = {**load_cfg(), **(cfg or {})}
    moment = _utc(now)
    if not cfg.get("enabled", False):
        return {"status": "disabled", "stage": {}, "active": {}}
    if str(cfg.get("execution_mode")) != "paper":
        return {"status": "blocked_non_paper_config", "stage": {}, "active": {}}
    project_config = load_config()
    path = Path(db or project_config.db_path)
    public_client = client or _client(cfg)
    from src.signals.pending_monitor import leader_lock

    with leader_lock(
        project_config.root,
        "mexc_stock_futures_paper",
        worker_id=f"mexc-stock-paper-{id(public_client)}",
        ttl_sec=180.0,
    ) as heartbeat:
        if heartbeat is None:
            return {
                "status": "leader_active",
                "evaluated_at": _iso(moment),
                "stage": {"status": "skipped_concurrent_tick"},
                "active": {},
            }
        heartbeat()
        return _tick_with_lease(
            path=path, moment=moment, public_client=public_client, cfg=cfg
        )


def closed_trade_rows(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return terminal rows in the shape consumed by the common Paper ledger."""
    exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' "
        "AND name='mexc_stock_futures_paper_positions'"
    ).fetchone()
    if not exists:
        return []
    rows = conn.execute(
        "SELECT * FROM mexc_stock_futures_paper_positions "
        "WHERE status='CLOSED' AND paper_execution_r IS NOT NULL ORDER BY entry_at"
    ).fetchall()
    out = []
    for raw in rows:
        row = dict(raw)
        highest = int(row.get("highest_tp_touched") or 0)
        out.append({
            "signal_id": row["source_signal_id"],
            "economic_trade_key": f"mexc-stock-futures:{row['position_id']}",
            "symbol": row["ticker"],
            "mexc_symbol": row["mexc_symbol"],
            "asset_class": "stock_futures",
            "mode": "intraday",
            "direction": row["direction"],
            "entry": row["entry_price"],
            "stop": row["stop_initial"],
            "tp1": row["tp1"], "tp2": row["tp2"], "tp3": row["tp3"],
            "paper_execution_r": row["paper_execution_r"],
            "close_reason": row["close_reason"],
            "stop_current_r": (
                (_float(row["stop_current"]) - _float(row["entry_price"]))
                / abs(_float(row["entry_price"]) - _float(row["stop_initial"]))
                * (1 if row["direction"] == "long" else -1)
            ),
            "entry_at": row["entry_at"],
            "exit_at": row["exit_at"],
            "exit_at_source": "mexc_public_1m",
            "decision_at": row["created_at"],
            "first_executable_price": row["entry_price"],
            "entry_drift_bps": 0.0,
            "tp1_hit": highest >= 1,
            "tp2_hit": highest >= 2,
            "tp3_hit": highest >= 3,
            "playbook": row["strategy_id"],
            "regime": "mexc_stock_futures",
            "size_weight": 1.0,
            "paper_action": "FULL_SIZE",
            "size_reason": "mexc_stock_futures_paper_point_in_time",
            "actionability_source": row["paper_lane"],
            "overlay_version": row["strategy_id"],
            "entry_order_type": row["entry_order_type"],
            "entry_funding_rate": row["funding_rate_at_entry"],
            # Contract volume is discrete on MEXC. Preserve the point-in-time
            # filled size in common Paper accounting instead of re-sizing it
            # later as though fractional contracts had been tradable.
            "fixed_qty": row["qty"],
            "fixed_risk_usdt": row["risk_usdt"],
            "fixed_notional_usdt": row["notional_usdt"],
            "fixed_margin_used_usdt": row["margin_used_usdt"],
            "fixed_leverage": row["leverage_used"],
        })
    return out


def render_report(
    *,
    db: str | Path | None = None,
    now: datetime | None = None,
) -> str:
    path = Path(db or load_config().db_path)
    moment = _utc(now)
    cfg = load_cfg()
    try:
        from src.live_execution.stocks_breakout_bridge import load_stocks_live_bridge_config
        bridge_cfg = load_stocks_live_bridge_config()
    except Exception:
        bridge_cfg = {}
    bridge_enabled = bool(bridge_cfg.get("enabled", False))
    bridge_route = str(bridge_cfg.get("route_id") or "not configured")
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        ensure_tables(conn)
        order_counts = dict(conn.execute(
            "SELECT status,COUNT(*) FROM mexc_stock_futures_paper_orders GROUP BY status"
        ).fetchall())
        positions = [
            dict(row) for row in conn.execute(
                "SELECT * FROM mexc_stock_futures_paper_positions ORDER BY entry_at DESC LIMIT 30"
            )
        ]
        recent_orders = [
            dict(row) for row in conn.execute(
                "SELECT ticker,direction,event_type,entry_mode,status,reject_reason,"
                "decision_at,spread_bps,source_drift_bps "
                "FROM mexc_stock_futures_paper_orders "
                "ORDER BY decision_at DESC LIMIT 30"
            )
        ]
        contracts = conn.execute(
            "SELECT COUNT(*),MAX(snapshot_at) FROM mexc_stock_futures_contracts"
        ).fetchone()
        quote_health = [dict(row) for row in conn.execute(
            "SELECT ticker,checked_at,status,reason,mexc_symbol,bid,ask,top5_depth_usdt "
            "FROM mexc_stock_futures_quote_health ORDER BY checked_at DESC,ticker ASC LIMIT 20"
        )]
    lines = [
        "# MEXC Stock Futures Paper",
        "",
        f"- generated_at: `{_iso(moment)}`",
        "- strategy authority: `PAPER` (public MEXC market data)",
        (
            f"- live mirror: `ENABLED` via `{bridge_route}` — only fresh, filled, "
            "version-pinned Paper breakouts may enter the separate MEXC canary preflight"
            if bridge_enabled else
            "- live mirror: `DISABLED`"
        ),
        f"- source warmup: `{cfg['preopen_refresh_start_et']} ET`",
        f"- mandatory fresh decision: `{cfg['preopen_decision_start_et']} ET` "
        "(20 minutes before RTH)",
        f"- force-flat: `{cfg['force_flat_et']} ET`",
        f"- discovered stock contracts: `{int(contracts[0] or 0)}`",
        f"- contract snapshot: `{contracts[1] or 'none'}`",
        f"- order states: `{json.dumps(order_counts, sort_keys=True)}`",
        "",
        "| ticker | direction | entry mode | status | entry | exit | R | reason |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]
    if quote_health:
        lines.extend([
            "", "## MEXC Quote Health", "",
            "| ticker | status | checked | bid / ask | depth | reason |",
            "|---|---|---|---:|---:|---|",
        ])
        for row in quote_health:
            prices = ("" if row.get("bid") is None else f"{_float(row['bid']):.4f}") + \
                     " / " + ("" if row.get("ask") is None else f"{_float(row['ask']):.4f}")
            depth = "" if row.get("top5_depth_usdt") is None else f"{_float(row['top5_depth_usdt']):.0f}"
            lines.append(
                f"| {row.get('ticker') or ''} | {row.get('status') or ''} | "
                f"{row.get('checked_at') or ''} | {prices} | {depth} | {row.get('reason') or ''} |"
            )
        lines.append("")
    for row in positions:
        result_r = (
            ""
            if row.get("paper_execution_r") is None
            else f"{_float(row['paper_execution_r']):.3f}"
        )
        lines.append(
            f"| {row['ticker']} | {row['direction']} | {row['entry_mode']} | "
            f"{row['status']} | {_float(row['entry_price']):.4f} | "
            f"{_float(row.get('exit_price')):.4f} | {result_r} | "
            f"{row.get('close_reason') or ''} |"
        )
    lines.extend([
        "",
        "## Recent Decisions",
        "",
        "| time | ticker | side | event | entry mode | status | spread bps | drift bps | reason |",
        "|---|---|---|---|---|---|---:|---:|---|",
    ])
    for row in recent_orders:
        lines.append(
            f"| {row.get('decision_at') or ''} | {row.get('ticker') or ''} | "
            f"{row.get('direction') or ''} | {row.get('event_type') or ''} | "
            f"{row.get('entry_mode') or ''} | {row.get('status') or ''} | "
            f"{_float(row.get('spread_bps')):.2f} | "
            f"{_float(row.get('source_drift_bps')):.2f} | "
            f"{row.get('reject_reason') or ''} |"
        )
    return "\n".join(lines) + "\n"


def write_report(
    *,
    db: str | Path | None = None,
    now: datetime | None = None,
    cfg: dict[str, Any] | None = None,
) -> Path:
    cfg = {**load_cfg(), **(cfg or {})}
    target = ROOT / str(cfg["report_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_report(db=db, now=now), encoding="utf-8")
    return target


def format_fill_message(position: dict[str, Any]) -> str:
    return (
        "PAPER ENTRY - MEXC STOCK FUTURES\n\n"
        f"{position['ticker']} {str(position['direction']).upper()} "
        f"({position['mexc_symbol']})\n"
        f"Mode: {position['entry_mode']}\n"
        f"Entry: {_float(position['entry_price']):.4f}\n"
        f"Stop: {_float(position['stop_initial']):.4f}\n"
        f"TP: {_float(position['tp1']):.4f} / {_float(position['tp2']):.4f} / "
        f"{_float(position['tp3']):.4f}\n"
        f"Risk: ${_float(position['risk_usdt']):.2f} "
        f"({_float(position['risk_pct']) * 100:.2f}%)\n"
        f"Funding/OI: {_float(position.get('funding_rate_at_entry')):.6f} / "
        f"{_float(position.get('hold_volume_at_entry')):.0f}\n\n"
        "Paper simulation only. No real MEXC order was placed."
    )


__all__ = [
    "ACTIVE_ORDER_STATES",
    "TERMINAL_ORDER_STATES",
    "Quote",
    "closed_trade_rows",
    "ensure_tables",
    "fetch_quote",
    "format_fill_message",
    "in_candidate_window",
    "in_refresh_window",
    "load_cfg",
    "process_active",
    "reconcile_session_symbol_duplicates",
    "refresh_contract_catalog",
    "render_report",
    "stage_candidates",
    "tick",
    "write_report",
]
