"""Verified on-chain risk cache used by the paper safety overlay."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import load_config, load_yaml
from src.data_collectors import market_intelligence_store as mi
from src.intelligence import store

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "onchain.yaml"


def config_status() -> dict[str, Any]:
    try:
        cfg = load_yaml(CONFIG)
        enabled = bool(cfg.get("enabled"))
        providers = [name for name, block in (cfg.get("providers") or {}).items()
                     if (block or {}).get("enabled", True)]
        return {"configured": enabled and bool(providers), "enabled": enabled,
                "providers": providers, "has_contracts": bool(cfg.get("assets")),
                "reason": "" if enabled and providers else "disabled_or_no_providers"}
    except Exception as exc:
        return {"configured": False, "reason": f"config_read_error:{exc}"}


def _unknown(symbol: str, reason: str = "no_verified_data") -> dict[str, Any]:
    return {
        "onchain_risk_status": "unknown", "onchain_chain": None, "onchain_contract": None,
        "holder_count": None, "top1_holder_pct": None, "top5_holder_pct": None,
        "top10_holder_pct": None, "contract_wallet_concentration_pct": None,
        "owner_risk": None, "mint_risk": None, "blacklist_risk": None,
        "honeypot_risk": None, "buy_tax": None, "sell_tax": None,
        "liquidity_lock_status": None, "exchange_deposit_detected": None,
        "exchange_deposit_usd_24h": None, "pre_pump_exchange_deposit_flag": None,
        "fake_mcap_risk": None, "thin_holder_base_flag": None, "onchain_risk_score": None,
        "onchain_data_confidence": "unknown", "onchain_data_freshness_sec": None,
        "onchain_missing_reason": reason, "contract_verified": False,
        "paper_guard_eligible": False, "diagnostic_only": True,
    }


def score_from_security(sec: dict[str, Any]) -> dict[str, Any]:
    out = _unknown("", reason="")
    try:
        def number(key, default=None):
            try:
                value = sec.get(key)
                return default if value is None else float(value)
            except (TypeError, ValueError):
                return default

        out["onchain_chain"] = sec.get("chain")
        out["onchain_contract"] = sec.get("contract") or sec.get("contract_address")
        out["holder_count"] = sec.get("holder_count")
        out["top10_holder_pct"] = number("top10_holder_pct")
        out["buy_tax"] = number("buy_tax")
        out["sell_tax"] = number("sell_tax")
        out["owner_risk"] = bool(sec.get("owner_change_balance")) if sec.get("owner_change_balance") is not None else None
        out["mint_risk"] = bool(sec.get("is_mintable")) if sec.get("is_mintable") is not None else None
        out["honeypot_risk"] = bool(sec.get("is_honeypot")) if sec.get("is_honeypot") is not None else None
        out["blacklist_risk"] = bool(sec.get("is_blacklisted")) if sec.get("is_blacklisted") is not None else None
        top10, holders, score = out["top10_holder_pct"] or 0.0, out["holder_count"] or 0, 0
        if out["honeypot_risk"]:
            score += 70
        if out["blacklist_risk"]:
            score += 50
        if out["mint_risk"]:
            score += 15
        if (out["sell_tax"] or 0) >= 25:
            score += 45
        elif (out["sell_tax"] or 0) >= 8:
            score += 15
        if top10 >= 70:
            score += 20
        elif top10 >= 50:
            score += 10
        if holders and holders < 300:
            score += 15
            out["thin_holder_base_flag"] = True
        out["onchain_risk_score"] = min(100, score)
        out["onchain_risk_status"] = "high" if score >= 50 else "elevated" if score >= 25 else "low"
        out["onchain_data_confidence"] = "high" if int(sec.get("security_provider_count") or 1) >= 2 else "medium"
        out["onchain_missing_reason"] = None
        return out
    except Exception:
        return _unknown("", reason="score_error")


def compute_onchain_risk(symbol: str, now: datetime | None = None,
                         db: str | Path | None = None) -> dict[str, Any]:
    cfg = config_status()
    if not cfg.get("configured"):
        return _unknown(symbol, cfg.get("reason") or "no_config")
    try:
        with mi.connect(db) as conn:
            context = mi.latest_onchain_context(conn, symbol, as_of=now)
        contract = context.get("contract") or {}
        if context.get("status") != "ok":
            out = _unknown(symbol, context.get("missing_reason") or "no_fresh_verified_data")
            out["contract_verified"] = bool(context.get("contract_verified"))
            return out
        if contract.get("contract_type") == "native":
            out = _unknown(symbol, reason="native_asset_network_metrics_only")
            out.update({
                "onchain_chain": contract.get("chain"), "onchain_contract": "native",
                "contract_verified": True, "network_metrics": context.get("metrics") or {},
                "onchain_data_confidence": "medium" if context.get("metrics") else "unknown",
                "onchain_missing_reason": None if context.get("metrics") else "network_metrics_missing",
            })
            return out
        fields = score_from_security({**context, "chain": contract.get("chain"),
                                      "contract": contract.get("contract_address")})
        fields.update({
            "contract_verified": True, "paper_guard_eligible": True,
            "diagnostic_only": False, "network_metrics": context.get("metrics") or {},
            "security_providers": context.get("security_providers") or [],
            "honeypot_confirmations": context.get("honeypot_confirmations") or 0,
            "honeypot_clear_confirmations": context.get("honeypot_clear_confirmations") or 0,
            "blacklist_confirmations": context.get("blacklist_confirmations") or 0,
            "extreme_sell_tax_confirmations": context.get("extreme_sell_tax_confirmations") or 0,
            "onchain_data_freshness_sec": context.get("security_age_sec"),
        })
        return fields
    except Exception as exc:
        return _unknown(symbol, f"store_error:{type(exc).__name__}")


def update_and_cache(symbol: str, now: datetime | None = None, conn=None) -> dict[str, Any]:
    fields = compute_onchain_risk(symbol, now=now)
    try:
        own = conn is None
        target = conn or store.connect()
        try:
            store.write_cache(target, "onchain_cache", symbol.split("/")[0].upper(),
                              (now or datetime.now(timezone.utc)).isoformat(), fields)
            if own:
                target.commit()
        finally:
            if own:
                target.close()
    except Exception:
        pass
    return fields


def onchain_risk_for_payload(symbol: str) -> dict[str, Any]:
    cached = store.read_cache("onchain_cache", symbol.split("/")[0].upper()) or _unknown(symbol)
    keys = ("onchain_risk_status", "onchain_risk_score", "top10_holder_pct", "honeypot_risk",
            "blacklist_risk", "mint_risk", "sell_tax", "thin_holder_base_flag",
            "onchain_data_confidence", "onchain_data_freshness_sec", "onchain_missing_reason",
            "contract_verified", "paper_guard_eligible", "security_providers", "honeypot_confirmations",
            "honeypot_clear_confirmations", "blacklist_confirmations", "extreme_sell_tax_confirmations",
            "network_metrics")
    return {key: cached.get(key) for key in keys}


def onchain_risk_health_report() -> dict[str, Any]:
    cfg = config_status(); cached = 0
    cache_conn = store.connect_ro()
    if cache_conn is not None:
        try:
            cached = cache_conn.execute("SELECT COUNT(*) n FROM onchain_cache").fetchone()["n"]
        except Exception:
            pass
        finally:
            cache_conn.close()
    verified = snapshots = 0
    try:
        with mi.connect() as conn:
            verified = conn.execute("SELECT COUNT(*) FROM asset_contract_registry WHERE verification_status='verified'").fetchone()[0]
            snapshots = conn.execute("SELECT COUNT(*) FROM token_security_snapshots").fetchone()[0]
    except Exception:
        pass
    return {"status": "ready" if cfg.get("configured") else "interface_ready_config_missing",
            "config": cfg, "cached_symbols": cached, "verified_contracts": verified,
            "security_snapshots": snapshots}
