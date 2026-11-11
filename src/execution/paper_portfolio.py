"""Paper portfolio ledger + equity simulation (PAPER / ACCOUNTING ONLY).

Turns paper trades (each carrying `paper_execution_r` from Model F) into a USD
equity curve with $5000 start, 0.5%-of-equity risk per trade, position sizing,
dynamic leverage, and fees/slippage. Derived/read-model — NO real orders, NO
production exit/TP/SL change, NEVER mutates `signal_outcomes.final_r`.

Equity uses **net USD** = `paper_execution_r × actual_risk_usdt − costs`. It
never uses touch_r.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from src.execution.position_sizing import size_position
from src.execution.fees import trade_costs

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

_ROOT = Path(__file__).resolve().parents[2]
_TABLE = "paper_portfolio_ledger"

_DEFAULT_CFG = {
    "initial_equity_usdt": 5000, "risk_per_trade_pct": 0.005, "risk_basis": "equity",
    "max_margin_per_trade_pct": 0.20, "max_notional_per_trade_pct": 1.50,
    "max_leverage": 5, "liquidation_buffer_to_stop": 1.5,
    "fee_profile": "bybit_default_futures",
    "default_slippage": {"major": 0.0002, "liquid_alt": 0.0005, "illiquid_alt": 0.0010},
    "majors": ["BTC", "ETH", "SOL", "BNB", "XRP"],
    # PART 3 (compute): stocks/ETFs must NOT be priced as crypto perps. Separate commission +
    # (wider) slippage; large-caps are the "majors" (tighter spread).
    "stock_fee_profile": "stock_etf_default",
    "stock_slippage": {"major": 0.0003, "liquid_alt": 0.0008, "illiquid_alt": 0.0015},
    "stock_majors": ["SPY", "QQQ", "IWM", "DIA", "AAPL", "MSFT", "NVDA", "AMZN", "META",
                     "GOOGL", "TSLA", "AMD", "AVGO", "NFLX"],
    # MEXC stock futures are derivatives, not commission-free cash equities.
    "stock_futures_fee_profile": "mexc_default_futures",
    "stock_futures_slippage": {
        "major": 0.0003, "liquid_alt": 0.0008, "illiquid_alt": 0.0015,
    },
    # PART 10: approximate crypto-perp funding by typical hold (funding interval ~8h). Stocks = 0.
    "funding": {"default_rate_per_interval": 0.0001, "interval_hours": 8,
                "intervals_by_mode": {"scalp": 0, "intraday": 1, "swing": 6, "invest": 0},
                "actual_events_enabled": True,
                "exchange_by_fee_profile": {"bybit_non_vip_usdt_perp": "bybit",
                                            "bybit_structural_maker_first": "bybit",
                                            "mexc_default_futures": "mexc"}},
    # USD-accounting guard: a Model-F breakeven stop is not really breakeven after fees/slippage/funding.
    # For crypto intraday paper, lift the implied BE exit just enough to cover execution costs in the
    # authoritative USD ledger. This does NOT rewrite paper_execution_outcomes / Model-F evidence R.
    "fee_aware_breakeven": {"enabled": True, "asset_modes": ["crypto:intraday"]},
}


def load_cfg() -> dict[str, Any]:
    path = _ROOT / "config" / "paper_portfolio.yaml"
    if yaml and path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return {**_DEFAULT_CFG, **((yaml.safe_load(fh) or {}).get("paper_portfolio") or {})}
        except Exception:
            pass
    return dict(_DEFAULT_CFG)


# ----------------------------------------------------------------- storage ----
_COLS = (
    "id", "signal_id", "economic_trade_key", "timestamp", "entry_at", "exit_at",
    "exit_at_source", "decision_at", "first_executable_price", "entry_drift_bps", "event_type",
    "equity_before", "equity_after", "realized_pnl_usdt", "unrealized_pnl_usdt",
    "gross_pnl_usdt", "fees_usdt", "slippage_usdt", "funding_usdt", "net_pnl_usdt",
    "risk_usdt", "risk_pct", "position_notional_usdt", "margin_used_usdt",
    "leverage_used", "qty", "entry_price", "exit_price", "stop_initial",
    "stop_current", "paper_execution_r", "close_reason", "risk_model",
    "fee_profile", "expiry_close_price", "expiry_close_price_source",
    "fee_estimated", "fee_source", "exit_maker_fraction", "funding_source",
    "funding_estimated", "funding_event_count", "created_at",
    # overlay-authoritative paper sizing (2026-07-08) — additive, nullable.
    "size_weight", "size_reason", "paper_action", "actionability_source", "overlay_version",
    "overlay_config_hash",
)

# additive nullable columns (idempotent ALTER; never drops — preserves the structural B-book rows).
_ADDITIVE_COLUMNS = (
    ("size_weight", "REAL"), ("size_reason", "TEXT"), ("paper_action", "TEXT"),
    ("actionability_source", "TEXT"), ("overlay_version", "TEXT"),
    ("funding_source", "TEXT"), ("funding_estimated", "INTEGER"),
    ("funding_event_count", "INTEGER"),
    ("entry_at", "TEXT"), ("exit_at", "TEXT"), ("exit_at_source", "TEXT"),
    ("decision_at", "TEXT"), ("first_executable_price", "REAL"),
    ("entry_drift_bps", "REAL"), ("overlay_config_hash", "TEXT"),
)


def ensure_tables(conn) -> None:
    # Derived table — if an older schema is present (missing the bugfix columns),
    # drop + recreate. Safe: it is rebuilt from signal_outcomes, never source data.
    try:
        cols = {r[1] for r in conn.execute(f"PRAGMA table_info({_TABLE})")}
        if cols and ("expiry_close_price" not in cols or "exit_maker_fraction" not in cols):
            conn.execute(f"DROP TABLE {_TABLE}")
    except Exception:
        pass
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_id TEXT, economic_trade_key TEXT, timestamp TEXT,
            entry_at TEXT, exit_at TEXT, exit_at_source TEXT, decision_at TEXT,
            first_executable_price REAL, entry_drift_bps REAL, event_type TEXT,
            equity_before REAL, equity_after REAL, realized_pnl_usdt REAL,
            unrealized_pnl_usdt REAL, gross_pnl_usdt REAL, fees_usdt REAL,
            slippage_usdt REAL, funding_usdt REAL, net_pnl_usdt REAL,
            risk_usdt REAL, risk_pct REAL, position_notional_usdt REAL,
            margin_used_usdt REAL, leverage_used INTEGER, qty REAL,
            entry_price REAL, exit_price REAL, stop_initial REAL, stop_current REAL,
            paper_execution_r REAL, close_reason TEXT, risk_model TEXT,
            fee_profile TEXT, expiry_close_price REAL, expiry_close_price_source TEXT,
            fee_estimated INTEGER, fee_source TEXT, exit_maker_fraction REAL,
            funding_source TEXT, funding_estimated INTEGER, funding_event_count INTEGER, created_at TEXT,
            size_weight REAL, size_reason TEXT, paper_action TEXT, actionability_source TEXT,
            overlay_version TEXT, overlay_config_hash TEXT,
            UNIQUE(economic_trade_key, event_type, fee_profile)
        )
        """
    )
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{_TABLE}_key ON {_TABLE}(economic_trade_key)")
    # additive migration for pre-existing ledgers (idempotent — never drops, preserves B-book rows).
    existing = {r[1] for r in conn.execute(f"PRAGMA table_info({_TABLE})")}
    for col, typ in _ADDITIVE_COLUMNS:
        if col not in existing:
            try:
                conn.execute(f"ALTER TABLE {_TABLE} ADD COLUMN {col} {typ}")
            except Exception:
                pass


def replace_ledger(conn, rows: list[dict[str, Any]], fee_profile: str) -> int:
    """Idempotent: clear this fee_profile's rows and re-insert. Never touches
    signal_outcomes."""
    ensure_tables(conn)
    conn.execute(f"DELETE FROM {_TABLE} WHERE fee_profile = ?", (fee_profile,))
    cols = [c for c in _COLS if c != "id"]
    ph = ", ".join("?" for _ in cols)
    conn.executemany(
        f"INSERT INTO {_TABLE} ({', '.join(cols)}) VALUES ({ph})",
        [[r.get(c) for c in cols] for r in rows],
    )
    return len(rows)


# -------------------------------------------------------------- simulation ----
def _f(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


# PART 4: split the exit into realistic slices — TP partials fill as MAKER (limit), while the
# stop / expiry remainder fills as TAKER (market). Uses the tracked tp1/2/3-hit flags. This changes
# only the EXECUTION COST realism; gross/net R stays driven by paper_execution_r (unchanged).
_PARTIALS = {1: 0.33, 2: 0.33, 3: 0.34}


def _exit_slices(t: dict) -> list[tuple[float, str]]:
    slices: list[tuple[float, str]] = []
    remaining = 1.0
    for i in (1, 2, 3):
        if t.get(f"tp{i}_hit"):
            frac = _PARTIALS[i]
            slices.append((frac, "maker"))       # TP exits are limit/maker
            remaining -= frac
    if remaining > 1e-9:
        slices.append((round(remaining, 6), "taker"))   # stop / expiry remainder = market/taker
    return slices or [(1.0, "taker")]


def resolve_cost_context(*, asset_class, mode, notional_usdt: float,
                         fee_profile: str, cfg: dict) -> tuple[str, dict, list, float | None]:
    """Asset-aware execution-cost context. SHARED by the A-book portfolio sim and the
    structural/maker B-book backfill so both price a trade the same, honest way:

      * stocks/ETFs → the equity/ETF fee profile + (wider) stock slippage + NO perp funding
      * crypto perps → the chosen futures profile + crypto slippage + approximate funding
      * "zero" → a true no-cost baseline

    Returns (eff_profile, eff_slip, eff_majors, funding_usdt). funding_usdt is None when the
    hold length (mode) is unknown, so callers can surface funding_known=False rather than a
    fake zero. Stocks always return funding 0.0 (known-zero: equities have no perp funding)."""
    if fee_profile == "zero":
        return "zero", {"major": 0.0, "liquid_alt": 0.0, "illiquid_alt": 0.0}, cfg.get("majors"), 0.0
    normalized_asset = str(asset_class or "").lower()
    if normalized_asset == "stock_futures":
        return (
            cfg.get("stock_futures_fee_profile", "mexc_default_futures"),
            cfg.get("stock_futures_slippage") or cfg.get("stock_slippage")
            or cfg.get("default_slippage"),
            cfg.get("stock_majors") or cfg.get("majors"),
            None,
        )
    if normalized_asset.startswith("stock"):
        return (cfg.get("stock_fee_profile", "stock_etf_default"),
                cfg.get("stock_slippage") or cfg.get("default_slippage"),
                cfg.get("stock_majors") or cfg.get("majors"), 0.0)
    _fcfg = cfg.get("funding") or {}
    _iv = (_fcfg.get("intervals_by_mode") or {}).get(str(mode or "").lower())
    fund = (None if _iv is None else
            float(notional_usdt) * float(_fcfg.get("default_rate_per_interval", 0.0001)) * float(_iv))
    return fee_profile, cfg.get("default_slippage"), cfg.get("majors"), fund


def _fee_aware_be_enabled(t: dict, cfg: dict) -> bool:
    be = cfg.get("fee_aware_breakeven") or {}
    if not be.get("enabled", True):
        return False
    key = f"{str(t.get('asset_class') or 'crypto').lower()}:{str(t.get('mode') or '').lower()}"
    return key in {str(x).lower() for x in (be.get("asset_modes") or [])}


def _funding_for_trade(t: dict, *, notional_usdt: float, fee_profile: str,
                       approximate: float | None, cfg: dict) -> dict[str, Any]:
    """Resolve actual settlement events first, with an explicit estimate fallback."""
    if fee_profile == "zero":
        return {"funding_usdt": 0.0, "source": "zero_profile", "estimated": 0, "events": 0}
    normalized_asset = str(t.get("asset_class") or "").lower()
    if normalized_asset == "stock_futures":
        rate = _f(t.get("entry_funding_rate"))
        if rate is None:
            return {
                "funding_usdt": None,
                "source": "mexc_entry_rate_unavailable",
                "estimated": 1,
                "events": 0,
            }
        side = 1.0 if str(t.get("direction") or "long").lower() != "short" else -1.0
        return {
            "funding_usdt": rate * notional_usdt * side,
            "source": "mexc_entry_rate_estimate",
            "estimated": 1,
            "events": 1,
        }
    if normalized_asset.startswith("stock"):
        return {"funding_usdt": 0.0, "source": "not_applicable_equity", "estimated": 0, "events": 0}
    funding_cfg = cfg.get("funding") or {}
    exchange = (funding_cfg.get("exchange_by_fee_profile") or {}).get(fee_profile)
    if funding_cfg.get("actual_events_enabled", True) and exchange and t.get("entry_at") and t.get("exit_at"):
        key = (exchange, str(t.get("symbol") or "").upper().replace("/", ""))
        if cfg.get("_funding_index_loaded"):
            try:
                start = datetime.fromisoformat(str(t["entry_at"]).replace("Z", "+00:00"))
                end = datetime.fromisoformat(str(t["exit_at"]).replace("Z", "+00:00"))
                if start.tzinfo is None: start = start.replace(tzinfo=timezone.utc)
                if end.tzinfo is None: end = end.replace(tzinfo=timezone.utc)
                events = [(ts, rate) for ts, rate in (cfg.get("_funding_event_index") or {}).get(key, [])
                          if start < ts <= end]
                if events:
                    side = 1.0 if str(t.get("direction") or "long").lower() != "short" else -1.0
                    return {"funding_usdt": sum(rate * notional_usdt * side for _, rate in events),
                            "source": f"actual_{exchange}_funding_events", "estimated": 0,
                            "events": len(events)}
            except Exception:
                pass
            return {"funding_usdt": approximate,
                    "source": "mode_interval_fallback" if approximate is not None else "unavailable",
                    "estimated": 1, "events": 0}
        try:
            from src.data_collectors import market_intelligence_store as mi
            with mi.connect(cfg.get("market_intelligence_db") or cfg.get("db_path")) as conn:
                actual = mi.actual_funding_cost(
                    conn, symbol=str(t.get("symbol") or ""), exchange=exchange,
                    direction=str(t.get("direction") or "long"), notional_usdt=notional_usdt,
                    entry_at=t["entry_at"], exit_at=t["exit_at"],
                )
            if actual.get("known"):
                return {"funding_usdt": float(actual["funding_usdt"]), "source": actual["source"],
                        "estimated": 0, "events": int(actual["events"])}
        except Exception:
            pass
    return {"funding_usdt": approximate,
            "source": "mode_interval_fallback" if approximate is not None else "unavailable",
            "estimated": 1, "events": 0}


def _load_funding_index(cfg: dict, trades: list[dict], fee_profile: str) -> None:
    cfg["_funding_index_loaded"] = True
    cfg["_funding_event_index"] = {}
    exchange = ((cfg.get("funding") or {}).get("exchange_by_fee_profile") or {}).get(fee_profile)
    if not exchange or not any(t.get("exit_at") for t in trades):
        return
    try:
        from src.data_collectors import market_intelligence_store as mi
        with mi.connect(cfg.get("market_intelligence_db") or cfg.get("db_path")) as conn:
            rows = conn.execute(
                "SELECT normalized_symbol,event_at,funding_rate FROM funding_rate_events "
                "WHERE exchange=? ORDER BY event_at", (exchange,)).fetchall()
        index: dict[tuple, list] = {}
        for symbol, event_at, rate in rows:
            ts = datetime.fromisoformat(str(event_at).replace("Z", "+00:00"))
            if ts.tzinfo is None: ts = ts.replace(tzinfo=timezone.utc)
            index.setdefault((exchange, str(symbol)), []).append((ts, float(rate)))
        cfg["_funding_event_index"] = index
    except Exception:
        cfg["_funding_event_index"] = {}


def simulate_portfolio(trades: Iterable[dict], *, cfg: dict | None = None,
                       fee_profile: str | None = None, now_iso: str = "") -> dict[str, Any]:
    """Chronological equity sim. `trades` must be sorted by entry time and each
    carry: signal_id, economic_trade_key, symbol, direction, entry, stop,
    paper_execution_r (None=skip), close_reason, stop_current_r, entry_at.

    Returns {equity_curve, ledger, summary}. Pure (no DB)."""
    cfg = {**_DEFAULT_CFG, **(cfg or {})}
    fee_profile = fee_profile or cfg["fee_profile"]
    trades = list(trades)
    _load_funding_index(cfg, trades, fee_profile)
    equity = float(cfg["initial_equity_usdt"])
    peak = equity
    max_dd = 0.0
    curve, ledger = [], []
    wins = losses = be = 0
    total_fees = total_gross = total_net = 0.0
    total_exch = total_slip = total_fund = 0.0   # PART 1/10: split execution costs

    for t in trades:
        per = _f(t.get("paper_execution_r"))
        entry = _f(t.get("entry"))
        stop = _f(t.get("stop"))
        if per is None or entry is None or stop is None or entry <= 0 or abs(entry - stop) <= 0:
            continue  # unresolved / no geometry → not counted (no silent zero)
        # Overlay-authoritative paper sizing: HALF_SIZE halves risk (→ notional / qty / PnL / costs all
        # scale). size_weight<=0 (SHADOW_ONLY/BLOCK) is excluded upstream, but skip defensively here too.
        size_weight = _f(t.get("size_weight"))
        size_weight = 1.0 if size_weight is None else max(0.0, min(1.0, size_weight))
        if size_weight <= 0.0:
            continue
        eff_risk_pct = float(cfg["risk_per_trade_pct"]) * size_weight
        risk_usdt = equity * eff_risk_pct if cfg["risk_basis"] == "equity" \
            else float(cfg["initial_equity_usdt"]) * eff_risk_pct
        sz = size_position(
            equity_usdt=equity, entry_price=entry, stop_price=stop,
            direction=str(t.get("direction") or "long"), risk_pct=eff_risk_pct,
            max_leverage=int(cfg["max_leverage"]), max_margin_pct=float(cfg["max_margin_per_trade_pct"]),
            max_notional_pct=float(cfg["max_notional_per_trade_pct"]),
            liquidation_buffer_to_stop=float(cfg["liquidation_buffer_to_stop"]),
        )
        fixed_qty = _f(t.get("fixed_qty"))
        if fixed_qty is not None and fixed_qty > 0:
            qty = fixed_qty
            actual_risk_usdt = _f(t.get("fixed_risk_usdt"))
            actual_risk_usdt = (
                actual_risk_usdt
                if actual_risk_usdt is not None
                else qty * abs(entry - stop)
            )
            notional_usdt = _f(t.get("fixed_notional_usdt"))
            notional_usdt = (
                notional_usdt
                if notional_usdt is not None
                else qty * entry
            )
            leverage_used = max(1, int(_f(t.get("fixed_leverage")) or 1))
            margin_used_usdt = _f(t.get("fixed_margin_used_usdt"))
            margin_used_usdt = (
                margin_used_usdt
                if margin_used_usdt is not None
                else notional_usdt / leverage_used
            )
            actual_risk_pct = actual_risk_usdt / equity if equity else 0.0
        else:
            qty = sz.qty
            actual_risk_usdt = sz.actual_risk_usdt
            actual_risk_pct = sz.actual_risk_pct
            notional_usdt = sz.notional_usdt
            margin_used_usdt = sz.margin_used_usdt
            leverage_used = sz.leverage_used
        gross = per * actual_risk_usdt
        # Implied exit/close price from the resolved R (1R = |entry-stop| in price).
        # For expired-after-entry, paper_execution_r is the protected level, so this
        # is the expiry close price (source: implied_from_paper_execution_r).
        risk_abs = abs(entry - stop)
        long = str(t.get("direction") or "long").lower() != "short"
        exit_price = entry + (per * risk_abs if long else -per * risk_abs)
        exit_notional = qty * exit_price
        # PART 3 (compute) + PART 10: asset-aware execution cost (shared with the B-book).
        eff_profile, eff_slip, eff_majors, fund_arg = resolve_cost_context(
            asset_class=t.get("asset_class"), mode=t.get("mode"),
            notional_usdt=notional_usdt, fee_profile=fee_profile, cfg=cfg)
        funding = _funding_for_trade(t, notional_usdt=notional_usdt,
                                     fee_profile=fee_profile, approximate=fund_arg, cfg=cfg)
        fund_arg = funding["funding_usdt"]
        exit_slices = _exit_slices(t)          # PART 4: maker-TP / taker-stop exit split
        maker_frac = round(sum(f for f, ot in exit_slices if ot == "maker"), 6)
        cost = trade_costs(notional_usdt=notional_usdt, exit_notional_usdt=exit_notional,
                           symbol=str(t.get("symbol") or ""), fee_profile=eff_profile,
                           entry_order_type=str(t.get("entry_order_type") or "taker"),
                           exit_order_type="taker",
                           slip_cfg=eff_slip, majors=eff_majors, funding_usdt=fund_arg,
                           exit_slices=exit_slices)
        if str(t.get("close_reason") or "") == "breakeven_stop" and abs(per) < 1e-12 \
                and _fee_aware_be_enabled(t, cfg) and actual_risk_usdt > 0:
            per_for_usd = cost.total_cost_usdt / actual_risk_usdt
            exit_price = entry + (per_for_usd * risk_abs if long else -per_for_usd * risk_abs)
            exit_notional = qty * exit_price
            cost = trade_costs(notional_usdt=notional_usdt, exit_notional_usdt=exit_notional,
                               symbol=str(t.get("symbol") or ""), fee_profile=eff_profile,
                               entry_order_type=str(t.get("entry_order_type") or "taker"),
                               exit_order_type="taker",
                               slip_cfg=eff_slip, majors=eff_majors, funding_usdt=fund_arg,
                               exit_slices=exit_slices)
            gross = cost.total_cost_usdt
        net = gross - cost.total_cost_usdt
        _reason = str(t.get("close_reason") or "")
        _is_expiry = "expired" in _reason   # genuine expiry close (not BE/lock stop closes)
        equity_before = equity
        equity = round(equity + net, 6)
        peak = max(peak, equity)
        dd = (peak - equity) / peak if peak > 0 else 0.0
        max_dd = max(max_dd, dd)
        if net > 0: wins += 1
        elif net < 0: losses += 1
        else: be += 1
        total_fees += cost.fee_usdt + cost.slippage_usdt
        total_exch += cost.fee_usdt
        total_slip += cost.slippage_usdt
        total_fund += cost.funding_usdt
        total_gross += gross
        total_net += net

        ledger.append({
            "signal_id": t.get("signal_id"), "economic_trade_key": t.get("economic_trade_key"),
            # Realized PnL belongs to the exit date. Entry time is retained
            # separately for sizing chronology and hold/funding calculations.
            "timestamp": t.get("exit_at") or t.get("entry_at"),
            "entry_at": t.get("entry_at"), "exit_at": t.get("exit_at"),
            "exit_at_source": t.get("exit_at_source"), "decision_at": t.get("decision_at"),
            "first_executable_price": t.get("first_executable_price"),
            "entry_drift_bps": t.get("entry_drift_bps"), "event_type": "exit",
            "equity_before": round(equity_before, 4), "equity_after": round(equity, 4),
            "realized_pnl_usdt": round(net, 4), "unrealized_pnl_usdt": 0.0,
            "gross_pnl_usdt": round(gross, 4), "fees_usdt": cost.fee_usdt,
            "slippage_usdt": cost.slippage_usdt, "funding_usdt": cost.funding_usdt,
            "net_pnl_usdt": round(net, 4), "risk_usdt": actual_risk_usdt,
            "risk_pct": actual_risk_pct, "position_notional_usdt": notional_usdt,
            "margin_used_usdt": margin_used_usdt, "leverage_used": leverage_used,
            "qty": qty, "entry_price": entry, "exit_price": round(exit_price, 10),
            "stop_initial": stop, "stop_current": t.get("stop_current_r"),
            "paper_execution_r": round(per, 4), "close_reason": t.get("close_reason"),
            "risk_model": "early_mfe_protection_v1", "fee_profile": fee_profile,
            "expiry_close_price": round(exit_price, 10) if _is_expiry else None,
            "expiry_close_price_source": "implied_from_paper_execution_r" if _is_expiry else None,
            "fee_estimated": int(cost.fee_estimated), "fee_source": cost.fee_source,
            "exit_maker_fraction": maker_frac,   # PART 4: share of exit filled as maker (TP limits)
            "funding_source": funding["source"], "funding_estimated": funding["estimated"],
            "funding_event_count": funding["events"],
            "created_at": now_iso,
            # overlay-authoritative paper sizing (2026-07-08): risk/notional/PnL above are already
            # scaled by size_weight; these record WHY and by how much (0.5 = HALF_SIZE).
            "size_weight": round(size_weight, 4), "size_reason": t.get("size_reason"),
            "paper_action": t.get("paper_action"), "actionability_source": t.get("actionability_source"),
            "overlay_version": t.get("overlay_version"),
            "overlay_config_hash": t.get("overlay_config_hash"),
        })
        curve.append({"timestamp": t.get("exit_at") or t.get("entry_at"), "equity": round(equity, 4),
                      "symbol": t.get("symbol"), "net_pnl_usdt": round(net, 4)})

    n = wins + losses + be
    summary = {
        "fee_profile": fee_profile, "initial_equity_usdt": float(cfg["initial_equity_usdt"]),
        "final_equity_usdt": round(equity, 2), "net_pnl_usdt": round(total_net, 2),
        "gross_pnl_usdt": round(total_gross, 2), "total_fees_slippage_usdt": round(total_fees, 2),
        "total_exchange_fees_usdt": round(total_exch, 2), "total_slippage_usdt": round(total_slip, 2),
        "total_funding_usdt": round(total_fund, 2),
        "return_pct": round((equity / float(cfg["initial_equity_usdt"]) - 1) * 100, 2),
        "max_drawdown_pct": round(max_dd * 100, 2), "trades": n,
        "wins": wins, "losses": losses, "breakeven": be,
        "win_rate_pct": round(100 * wins / n, 1) if n else 0.0,
    }
    return {"equity_curve": curve, "ledger": ledger, "summary": summary}
