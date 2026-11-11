from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "crypto_invest_universe.yaml"
SNAPSHOT_PATH = ROOT / "reports" / "crypto_invest_universe_latest.json"
USER_AGENT = "crypto-ai-desk-universe/1.0"


@dataclass(frozen=True)
class UniverseSnapshot:
    generated_at: str
    selected_symbols: list[str]
    ranked: list[dict[str, Any]]
    rejected_counts: dict[str, int]
    source_times: dict[str, str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "selected_symbols": self.selected_symbols,
            "ranked": self.ranked,
            "rejected_counts": self.rejected_counts,
            "source_times": self.source_times,
        }


def load_universe_config(path: str | Path | None = None) -> dict[str, Any]:
    selected = Path(path) if path else CONFIG_PATH
    payload = yaml.safe_load(selected.read_text(encoding="utf-8")) or {}
    return payload.get("crypto_invest_universe") or {}


def load_selected_symbols(path: str | Path | None = None) -> list[str]:
    cfg = load_universe_config(path)
    values = [str(value).strip().upper() for value in cfg.get("selected_symbols") or []]
    if len(values) != len(set(values)):
        raise ValueError("crypto invest universe contains duplicate symbols")
    expected = int(cfg.get("selection_count", 60))
    if len(values) != expected:
        raise ValueError(f"crypto invest universe expected {expected} symbols, got {len(values)}")
    return values


def _number(value: Any) -> float:
    try:
        return max(0.0, float(value or 0.0))
    except (TypeError, ValueError):
        return 0.0


def _aliases(base: str) -> tuple[str, ...]:
    return (f"{base}USDT", f"1000{base}USDT", f"{base}1000USDT")


def fetch_source_payloads(*, session: requests.Session | None = None,
                          config: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, str]]:
    cfg = config or load_universe_config()
    endpoints = cfg.get("source_endpoints") or {}
    client = session or requests.Session()
    client.headers.setdefault("User-Agent", USER_AGENT)
    source_times: dict[str, str] = {}

    def get(name: str, *, params: dict[str, Any] | None = None) -> Any:
        response = client.get(str(endpoints[name]), params=params, timeout=30)
        response.raise_for_status()
        source_times[name] = datetime.now(timezone.utc).isoformat()
        return response.json()

    coingecko = get("coingecko", params={
        "vs_currency": "usd", "order": "market_cap_desc", "per_page": 250,
        "page": 1, "sparkline": "false",
    })
    binance_tickers = get("binance_tickers")
    binance_contracts = get("binance_contracts")
    bybit_tickers = get("bybit_tickers", params={"category": "linear"})
    mexc_tickers = get("mexc_tickers")
    mexc_contracts = get("mexc_contracts")
    return {
        "coingecko": coingecko,
        "binance_tickers": binance_tickers,
        "binance_contracts": binance_contracts.get("symbols") or [],
        "bybit_tickers": ((bybit_tickers.get("result") or {}).get("list") or []),
        "mexc_tickers": mexc_tickers.get("data") or [],
        "mexc_contracts": mexc_contracts.get("data") or [],
    }, source_times


def rank_universe(payloads: dict[str, Any], *, config: dict[str, Any] | None = None,
                  now: datetime | None = None,
                  source_times: dict[str, str] | None = None) -> UniverseSnapshot:
    cfg = config or load_universe_config()
    rules = cfg.get("selection_rules") or {}
    weights = rules.get("score_weights") or {}
    selected_count = int(cfg.get("selection_count", 60))
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    now_ms = now.timestamp() * 1000.0
    excluded = {str(value).upper() for value in cfg.get("excluded_bases") or []}
    rejected: dict[str, int] = {}

    def reject(reason: str) -> None:
        rejected[reason] = rejected.get(reason, 0) + 1

    binance_contracts = {
        str(row.get("symbol") or "").upper(): row
        for row in payloads.get("binance_contracts") or []
        if row.get("status") == "TRADING" and row.get("contractType") == "PERPETUAL"
    }
    binance_volume = {
        str(row.get("symbol") or "").upper(): _number(row.get("quoteVolume"))
        for row in payloads.get("binance_tickers") or []
    }
    bybit_volume = {
        str(row.get("symbol") or "").upper(): _number(row.get("turnover24h"))
        for row in payloads.get("bybit_tickers") or []
    }
    mexc_contracts = {
        str(row.get("symbol") or "").upper(): row
        for row in payloads.get("mexc_contracts") or []
        if int(row.get("state", -1)) == 0 and row.get("apiAllowed") is True
        and str(row.get("quoteCoin") or "").upper() == "USDT"
    }
    mexc_volume = {
        str(row.get("symbol") or "").upper(): _number(row.get("amount24"))
        for row in payloads.get("mexc_tickers") or []
    }
    min_binance_age = float(rules.get("min_binance_futures_age_days", 365))
    min_mexc_age = float(rules.get("min_mexc_contract_age_days", 180))
    max_rank = int(rules.get("max_market_cap_rank", 250))
    min_cap = float(rules.get("min_market_cap_usd", 200_000_000))
    min_global_volume = float(rules.get("min_global_volume_24h_usd", 5_000_000))
    min_venues = int(rules.get("min_active_derivatives_venues", 2))

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for coin in payloads.get("coingecko") or []:
        base = str(coin.get("symbol") or "").upper()
        if not base or base in seen:
            reject("duplicate_or_missing_symbol")
            continue
        seen.add(base)
        rank = int(coin.get("market_cap_rank") or 999_999)
        if base in excluded:
            reject("excluded_asset")
            continue
        if rank > max_rank:
            reject("market_cap_rank")
            continue
        cap = _number(coin.get("market_cap"))
        global_volume = _number(coin.get("total_volume"))
        if cap < min_cap or global_volume < min_global_volume:
            reject("market_cap_or_global_volume")
            continue

        mexc_symbol = f"{base}_USDT"
        mexc = mexc_contracts.get(mexc_symbol)
        if mexc is None:
            reject("mexc_contract_unavailable")
            continue
        mexc_age = (now_ms - _number(mexc.get("createTime"))) / 86_400_000.0
        if mexc_age < min_mexc_age:
            reject("mexc_contract_too_new")
            continue

        binance_symbol = None
        for alias in _aliases(base):
            contract = binance_contracts.get(alias)
            if contract is None:
                continue
            age = (now_ms - _number(contract.get("onboardDate"))) / 86_400_000.0
            if age >= min_binance_age:
                binance_symbol = alias
                break
        if binance_symbol is None:
            reject("binance_contract_unavailable_or_too_new")
            continue

        binance_turnover = binance_volume.get(binance_symbol, 0.0)
        bybit_turnover = max((bybit_volume.get(alias, 0.0) for alias in _aliases(base)), default=0.0)
        mexc_turnover = mexc_volume.get(mexc_symbol, 0.0)
        venue_count = sum(value > 0 for value in (
            binance_turnover, bybit_turnover, mexc_turnover,
        ))
        if venue_count < min_venues or binance_turnover <= 0 or mexc_turnover <= 0:
            reject("insufficient_derivatives_venues")
            continue
        derivatives_turnover = binance_turnover + bybit_turnover + mexc_turnover
        score = (
            float(weights.get("global_volume", 0.45)) * math.log10(max(global_volume, 1.0))
            + float(weights.get("aggregate_derivatives_volume", 0.30))
            * math.log10(max(derivatives_turnover, 1.0))
            + float(weights.get("market_cap", 0.20)) * math.log10(max(cap, 1.0))
            + float(weights.get("venue_breadth", 0.05)) * venue_count / 3.0
        )
        rows.append({
            "rank": 0, "symbol": f"{base}/USDT", "base": base,
            "name": str(coin.get("name") or base), "score": round(score, 8),
            "market_cap_rank": rank, "market_cap_usd": cap,
            "global_volume_24h_usd": global_volume,
            "binance_turnover_24h_usd": binance_turnover,
            "bybit_turnover_24h_usd": bybit_turnover,
            "mexc_turnover_24h_usd": mexc_turnover,
            "active_derivatives_venues": venue_count,
            "binance_symbol": binance_symbol, "mexc_symbol": mexc_symbol,
            "binance_age_days": round((now_ms - _number(
                binance_contracts[binance_symbol].get("onboardDate"))) / 86_400_000.0, 1),
            "mexc_age_days": round(mexc_age, 1),
        })
    rows.sort(key=lambda row: (-float(row["score"]), int(row["market_cap_rank"]), row["symbol"]))
    for index, row in enumerate(rows, start=1):
        row["rank"] = index
    selected = rows[:selected_count]
    if len(selected) != selected_count:
        raise RuntimeError(f"only {len(selected)} assets passed universe rules; need {selected_count}")
    return UniverseSnapshot(
        generated_at=now.isoformat(),
        selected_symbols=[str(row["symbol"]) for row in selected],
        ranked=rows,
        rejected_counts=rejected,
        source_times=dict(source_times or {}),
    )


def refresh_universe(*, apply: bool = False, config_path: str | Path | None = None,
                     snapshot_path: str | Path | None = None,
                     session: requests.Session | None = None) -> dict[str, Any]:
    path = Path(config_path) if config_path else CONFIG_PATH
    cfg = load_universe_config(path)
    payloads, source_times = fetch_source_payloads(session=session, config=cfg)
    snapshot = rank_universe(payloads, config=cfg, source_times=source_times)
    out = Path(snapshot_path) if snapshot_path else SNAPSHOT_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    previous = [str(value).upper() for value in cfg.get("selected_symbols") or []]
    membership_changed = set(snapshot.selected_symbols) != set(previous)
    rank_order_changed = snapshot.selected_symbols != previous
    if apply:
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        block = document.setdefault("crypto_invest_universe", {})
        block["selected_symbols"] = snapshot.selected_symbols
        block["last_reviewed_at"] = snapshot.generated_at
        path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=False), encoding="utf-8")
    return {
        "generated_at": snapshot.generated_at,
        "selected_count": len(snapshot.selected_symbols),
        "selected_symbols": snapshot.selected_symbols,
        "changed": membership_changed,
        "membership_changed": membership_changed,
        "rank_order_changed": rank_order_changed,
        "applied": bool(apply),
        "snapshot_path": str(out),
    }
