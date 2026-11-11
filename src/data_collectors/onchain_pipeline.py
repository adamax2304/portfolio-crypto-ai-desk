"""Free, keyless on-chain ingestion with contract-identity verification."""
from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from src.config import load_config, load_yaml
from src.data_collectors import market_intelligence_store as mi
from src.data_collectors.derivatives_pipeline import active_symbols

ROOT = Path(__file__).resolve().parents[2]


def _f(value: Any) -> float | None:
    try:
        return None if value in (None, "") else float(value)
    except (TypeError, ValueError):
        return None


def _flag(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(str(value).lower() in {"1", "true", "yes"})


def _pct(value: Any) -> float | None:
    number = _f(value)
    if number is None:
        return None
    return number * 100.0 if abs(number) <= 1.0 else number


class OnchainPipeline:
    def __init__(self, db_path: str | Path | None = None, session: requests.Session | None = None,
                 trading_db_path: str | Path | None = None):
        self.project = load_config()
        self.trading_db_path = Path(trading_db_path or self.project.db_path)
        self.db_path = Path(db_path or mi.default_db_path())
        self.cfg = load_yaml(ROOT / "config" / "onchain.yaml") or {}
        self.providers = self.cfg.get("providers") or {}
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": "crypto-ai-desk/1.0 research"})
        self._last_call: dict[str, float] = {}

    def _provider_url(self, provider: str, default: str) -> str:
        return str((self.providers.get(provider) or {}).get("base_url") or default).rstrip("/")

    def _wait(self, provider: str) -> None:
        minimum = float((self.providers.get(provider) or {}).get("min_interval_seconds") or 0)
        elapsed = time.monotonic() - self._last_call.get(provider, 0.0)
        if elapsed < minimum:
            time.sleep(minimum - elapsed)
        self._last_call[provider] = time.monotonic()

    def _get(self, provider: str, path: str, params: dict | None = None) -> Any:
        self._wait(provider)
        response = self.session.get(self._provider_url(provider, "") + path, params=params, timeout=20)
        response.raise_for_status()
        return response.json()

    def bootstrap_registry(self, symbols: list[str] | None = None) -> dict[str, Any]:
        wanted = {mi.base_symbol(s) for s in (symbols or active_symbols(80, self.trading_db_path))}
        assets = self.cfg.get("assets") or {}
        result = {"verified_native": 0, "verified_contracts": 0, "candidates": 0, "errors": {}}
        coin_list = []
        try:
            coin_list = self._get("coingecko", "/coins/list", {"include_platform": "true"}) or []
        except Exception as exc:
            result["errors"]["coingecko"] = str(exc)
        by_id = {str(c.get("id")): c for c in coin_list if isinstance(c, dict)}
        by_symbol: dict[str, list[dict]] = {}
        for coin in coin_list:
            by_symbol.setdefault(str(coin.get("symbol") or "").upper(), []).append(coin)

        with mi.connect(self.db_path) as conn:
            for base in sorted(wanted):
                spec = assets.get(base) or {}
                coin_id = spec.get("coingecko_id")
                if spec.get("native") and coin_id:
                    mi.upsert_contract(
                        conn, asset_symbol=base, canonical_asset_id=coin_id, chain=base.lower(),
                        chain_id=base.lower(), contract_address="native", contract_type="native",
                        source_primary="config:canonical_id", source_secondary="coingecko",
                        verification_status="verified", verified_at=mi.utc_now_iso(),
                        name=(by_id.get(coin_id) or {}).get("name"), symbol_reported=base,
                        metadata_json={"coinmetrics_asset": spec.get("coinmetrics_asset")},
                    )
                    result["verified_native"] += 1
                    conn.commit()
                    continue
                coin = by_id.get(str(coin_id)) if coin_id else None
                if not coin:
                    # A unique ticker match is stored only as a candidate.  It
                    # is never enough to affect paper decisions.
                    matches = by_symbol.get(base) or []
                    for candidate in matches[:3]:
                        for platform, address in (candidate.get("platforms") or {}).items():
                            if address:
                                chain = (self.cfg.get("chain_map") or {}).get(platform) or {}
                                mi.upsert_contract(
                                    conn, asset_symbol=base, canonical_asset_id=candidate.get("id"),
                                    chain=chain.get("name") or platform, chain_id=chain.get("chain_id"),
                                    contract_address=address, source_primary="coingecko_ticker_candidate",
                                    verification_status="candidate", name=candidate.get("name"),
                                    symbol_reported=candidate.get("symbol"),
                                    ambiguity_reason="ticker_only_mapping_forbidden",
                                    metadata_json={"platform": platform, "match_count": len(matches)},
                                )
                                result["candidates"] += 1
                    conn.commit()
                    continue
                platforms = coin.get("platforms") or {}
                preferred = spec.get("preferred_chain")
                if preferred:
                    platforms = {preferred: platforms.get(preferred)}
                for platform, address in platforms.items():
                    if not address:
                        continue
                    chain = (self.cfg.get("chain_map") or {}).get(platform) or {}
                    chain_id = str(chain.get("chain_id") or "")
                    verified, security = self._verify_goplus(chain_id, address, base)
                    mi.upsert_contract(
                        conn, asset_symbol=base, canonical_asset_id=coin_id,
                        chain=chain.get("name") or platform, chain_id=chain_id,
                        contract_address=address, source_primary="config+coingecko_contract",
                        source_secondary="goplus" if verified else None,
                        verification_status="verified" if verified else "candidate",
                        verified_at=mi.utc_now_iso() if verified else None,
                        name=coin.get("name"), symbol_reported=coin.get("symbol"),
                        ambiguity_reason=None if verified else "secondary_provider_did_not_confirm",
                        metadata_json={"platform": platform},
                    )
                    if verified:
                        result["verified_contracts"] += 1
                        self._write_goplus_security(conn, base, coin_id, chain.get("name") or platform,
                                                    address, security)
                    else:
                        result["candidates"] += 1
                # Do not hold a write lock while the next asset waits on the
                # rate-limited secondary verification API.
                conn.commit()
            mi.record_source_health(
                conn, "onchain:contract_registry", status="ok", success=True,
                records_written=result["verified_native"] + result["verified_contracts"] + result["candidates"],
                details=result,
            )
            conn.commit()
        return result

    def _verify_goplus(self, chain_id: str, address: str, base: str) -> tuple[bool, dict]:
        if not chain_id.isdigit():
            return False, {}
        try:
            payload = self._get("goplus", f"/token_security/{chain_id}",
                                {"contract_addresses": address})
            result = payload.get("result") or {}
            security = result.get(address.lower()) or result.get(address) or {}
            reported = str(security.get("token_symbol") or "").upper()
            return bool(security and reported == base), security
        except Exception:
            return False, {}

    def _write_goplus_security(self, conn, base: str, coin_id: str, chain: str,
                               address: str, sec: dict) -> int:
        holders = sec.get("holders") or []
        burn = {"0x0000000000000000000000000000000000000000",
                "0x000000000000000000000000000000000000dead"}
        filtered_holders = [h for h in holders if not _flag(h.get("is_contract"))
                            and str(h.get("address") or "").lower() not in burn]
        percents = sorted((_pct(h.get("percent")) or 0 for h in filtered_holders), reverse=True)
        top10 = sum(percents[:10]) if percents else None
        written = int(mi.insert_token_security(
            conn, asset_symbol=base, canonical_asset_id=coin_id, chain=chain,
            contract_address=address, provider="goplus", is_honeypot=_flag(sec.get("is_honeypot")),
            sell_tax=_pct(sec.get("sell_tax")), buy_tax=_pct(sec.get("buy_tax")),
            is_mintable=_flag(sec.get("is_mintable")),
            owner_change_balance=_flag(sec.get("owner_change_balance")),
            is_blacklisted=_flag(sec.get("is_blacklisted")), holder_count=int(sec.get("holder_count") or 0) or None,
            top10_holder_pct=top10, lp_locked_pct=_pct(sec.get("lp_holder_count")),
            confidence="high", raw_json=sec,
        ))
        if percents:
            written += int(mi.insert_holder_concentration(
                conn, asset_symbol=base, canonical_asset_id=coin_id, chain=chain,
                contract_address=address, provider="goplus", holder_count=int(sec.get("holder_count") or 0) or None,
                top1_pct=sum(percents[:1]), top5_pct=sum(percents[:5]), top10_pct=sum(percents[:10]),
                top20_pct=sum(percents[:20]), excluded_contracts=True,
                quality_status="contract_and_burn_addresses_excluded", raw_json=holders,
            ))
        return written

    def refresh(self, symbols: list[str] | None = None) -> dict[str, Any]:
        selected = symbols or active_symbols(40, self.trading_db_path)
        registry = self.bootstrap_registry(selected)
        result = {"registry": registry, "metrics": 0, "security": 0, "holders": 0, "errors": {}}
        with mi.connect(self.db_path) as conn:
            for base in sorted({mi.base_symbol(s) for s in selected}):
                spec = (self.cfg.get("assets") or {}).get(base) or {}
                if spec.get("coinmetrics_asset"):
                    try:
                        result["metrics"] += self._coinmetrics(conn, base, spec)
                        conn.commit()
                    except Exception as exc:
                        conn.rollback()
                        result["errors"][f"coinmetrics:{base}"] = str(exc)
                if spec.get("defillama_chain"):
                    try:
                        result["metrics"] += self._defillama(conn, base, spec)
                        conn.commit()
                    except Exception as exc:
                        conn.rollback()
                        result["errors"][f"defillama:{base}"] = str(exc)
                contract = mi.verified_contract(conn, base)
                if contract and contract.get("contract_type") != "native":
                    try:
                        result["security"] += self._refresh_contract_security(conn, contract)
                        if contract.get("chain") == "solana":
                            result["holders"] += self._solana_holders(conn, contract)
                        conn.commit()
                    except Exception as exc:
                        conn.rollback()
                        result["errors"][f"security:{base}"] = str(exc)
            mi.record_source_health(
                conn, "onchain:refresh", status="ok" if not result["errors"] else "degraded",
                success=True, records_written=result["metrics"] + result["security"] + result["holders"],
                details=result,
            )
            mi.record_source_health(
                conn, "onchain:wallet_flows", status="interface_ready_no_curated_wallets", success=True,
                details=(self.cfg.get("wallet_flows") or {}),
            )
            for provider in ("coinmetrics", "defillama", "security"):
                errors = {k: v for k, v in result["errors"].items() if k.startswith(provider + ":")}
                mi.record_source_health(
                    conn, f"onchain:{provider}", status="degraded" if errors else "ok",
                    success=not errors, error="; ".join(errors.values())[:500] if errors else None,
                    details={"errors": errors},
                )
            conn.commit()
        return result

    def _solana_holders(self, conn, contract: dict) -> int:
        url = str((self.providers.get("solana_rpc") or {}).get("url") or
                  "https://api.mainnet-beta.solana.com")
        def rpc(method: str, params: list) -> dict:
            response = self.session.post(url, json={"jsonrpc": "2.0", "id": 1,
                                                    "method": method, "params": params}, timeout=20)
            response.raise_for_status()
            return response.json()
        largest = rpc("getTokenLargestAccounts", [contract["contract_address"]])
        supply = rpc("getTokenSupply", [contract["contract_address"]])
        total = _f((((supply.get("result") or {}).get("value") or {}).get("uiAmountString")))
        values = []
        for row in ((largest.get("result") or {}).get("value") or []):
            amount = _f(row.get("uiAmountString"))
            if amount is not None and total:
                values.append(amount / total * 100.0)
        if not values:
            return 0
        values.sort(reverse=True)
        return int(mi.insert_holder_concentration(
            conn, asset_symbol=contract["asset_symbol"], canonical_asset_id=contract["canonical_asset_id"],
            chain="solana", contract_address=contract["contract_address"], provider="solana_rpc",
            top1_pct=sum(values[:1]), top5_pct=sum(values[:5]), top10_pct=sum(values[:10]),
            top20_pct=sum(values[:20]), excluded_contracts=False,
            quality_status="raw_largest_accounts_includes_contract_wallets", raw_json=largest,
        ))

    def _coinmetrics(self, conn, base: str, spec: dict) -> int:
        asset = spec["coinmetrics_asset"]
        catalog = self._get("coinmetrics_community", "/catalog/assets", {"assets": asset})
        available = set()
        for item in ((catalog.get("data") or [{}])[0].get("metrics") or []):
            if any(f.get("frequency") == "1d" and f.get("community") is True
                   for f in item.get("frequencies") or []):
                available.add(str(item.get("metric")))
        desired = ("AdrActCnt", "TxCnt", "TxTfrValAdjUSD", "TxTfrValUSD", "FeeTotUSD", "SplyCur")
        selected = [metric for metric in desired if metric in available]
        if not selected:
            return 0
        payload = self._get("coinmetrics_community", "/timeseries/asset-metrics", {
            "assets": asset, "metrics": ",".join(selected), "frequency": "1d", "page_size": 2,
        })
        written = 0
        units = {"AdrActCnt": "addresses", "TxCnt": "transactions", "TxTfrValAdjUSD": "usd",
                 "TxTfrValUSD": "usd", "FeeTotUSD": "usd", "SplyCur": "native"}
        for row in payload.get("data") or []:
            for metric in selected:
                value = _f(row.get(metric))
                if value is not None:
                    written += int(mi.insert_onchain_metric(
                        conn, provider_ts=row.get("time"), asset_symbol=base,
                        canonical_asset_id=spec.get("coingecko_id"), chain=base.lower(),
                        metric_name=metric, metric_value=value, unit=units[metric],
                        provider="coinmetrics_community", raw_json=row))
        return written

    def _defillama(self, conn, base: str, spec: dict) -> int:
        payload = self._get("defillama", f"/v2/historicalChainTvl/{spec['defillama_chain']}")
        written = 0
        for row in (payload or [])[-2:]:
            ts = datetime.fromtimestamp(float(row.get("date")), tz=timezone.utc).isoformat()
            written += int(mi.insert_onchain_metric(
                conn, provider_ts=ts, asset_symbol=base, canonical_asset_id=spec.get("coingecko_id"),
                chain=str(spec["defillama_chain"]).lower(), metric_name="chain_tvl_usd",
                metric_value=_f(row.get("tvl")), unit="usd", provider="defillama", raw_json=row))
        return written

    def _refresh_contract_security(self, conn, contract: dict) -> int:
        written = 0
        chain_id, address = str(contract.get("chain_id") or ""), contract["contract_address"]
        verified, sec = self._verify_goplus(chain_id, address, contract["asset_symbol"])
        if verified:
            written += self._write_goplus_security(
                conn, contract["asset_symbol"], contract["canonical_asset_id"],
                contract["chain"], address, sec)
            # Honeypot.is is a separate network call. Release the GoPlus write
            # before waiting for it so other paper writers can proceed.
            conn.commit()
        chain_cfg = next((v for v in (self.cfg.get("chain_map") or {}).values()
                          if str(v.get("chain_id")) == chain_id), {})
        hp_chain = chain_cfg.get("honeypot_chain_id")
        if hp_chain:
            try:
                hp = self._get("honeypot_is", "/IsHoneypot", {"address": address, "chainID": hp_chain})
                written += int(mi.insert_token_security(
                    conn, asset_symbol=contract["asset_symbol"],
                    canonical_asset_id=contract["canonical_asset_id"], chain=contract["chain"],
                    contract_address=address, provider="honeypot_is",
                    is_honeypot=_flag((hp.get("honeypotResult") or {}).get("isHoneypot")),
                    sell_tax=_f((hp.get("simulationResult") or {}).get("sellTax")),
                    buy_tax=_f((hp.get("simulationResult") or {}).get("buyTax")),
                    confidence="medium", raw_json=hp))
            except Exception:
                pass
        return written
