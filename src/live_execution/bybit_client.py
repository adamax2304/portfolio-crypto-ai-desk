from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any
from urllib.parse import urlencode

import requests


class BybitAPIError(RuntimeError):
    def __init__(self, message: str, *, code: Any = None, status_code: int | None = None):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class BybitFuturesClient:
    """Small V5 USDT-perpetual adapter used by the shared live router.

    POST requests are never retried here. A timed-out submission is resolved
    by its deterministic ``orderLinkId`` before the caller may do anything
    else, preventing a second venue from receiving the same trade.
    """

    def __init__(self, *, access_key: str = "", secret_key: str = "",
                 base_url: str = "https://api.bybit.com", recv_window_ms: int = 5000,
                 timeout_seconds: float = 4.0, session: requests.Session | None = None,
                 safe_read_retry_attempts: int = 2,
                 safe_read_retry_backoff_seconds: float = 0.2):
        self._access_key = access_key
        self._secret_key = secret_key
        self.base_url = base_url.rstrip("/")
        self.recv_window_ms = max(1000, min(int(recv_window_ms), 20000))
        self.timeout_seconds = float(timeout_seconds)
        self.session = session or requests.Session()
        self.safe_read_retry_attempts = max(1, int(safe_read_retry_attempts))
        self.safe_read_retry_backoff_seconds = max(0.0, float(safe_read_retry_backoff_seconds))

    @staticmethod
    def native_symbol(symbol: str) -> str:
        text = str(symbol or "").strip().upper().replace("-", "/").replace("_", "/")
        if "/" in text:
            base, quote = text.split("/", 1)
            return f"{base}{quote}"
        return text

    @staticmethod
    def signature(secret_key: str, timestamp_ms: str, access_key: str,
                  recv_window_ms: int, payload: str) -> str:
        raw = f"{timestamp_ms}{access_key}{recv_window_ms}{payload}"
        return hmac.new(secret_key.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()

    @staticmethod
    def _query(params: dict[str, Any] | None) -> str:
        clean = {key: value for key, value in (params or {}).items() if value is not None}
        return urlencode(sorted(clean.items()), doseq=True)

    @staticmethod
    def _body(body: dict[str, Any] | None) -> str:
        return json.dumps(body or {}, separators=(",", ":"), ensure_ascii=True)

    @staticmethod
    def _is_retryable_read_response(*, status_code: int, payload: Any) -> bool:
        """Return whether a pre-submission GET can be safely re-signed and retried.

        A Bybit timestamp-window rejection means no request was accepted. It is
        safe to issue the same read again with a new timestamp, but this rule
        must never apply to a POST: after a submission timeout the exchange may
        already hold the order.
        """
        if status_code in {408, 425, 429, 500, 502, 503, 504}:
            return True
        if not isinstance(payload, dict):
            return False
        code = payload.get("retCode")
        message = str(payload.get("retMsg") or "").lower()
        return bool(
            code == 10002
            or "server timestamp" in message
            or "recv_window" in message
            or "timestamp or recv" in message
        )

    def _request(self, method: str, path: str, *, params: dict[str, Any] | None = None,
                 body: dict[str, Any] | None = None, private: bool = False) -> dict[str, Any]:
        method = method.upper()
        query = self._query(params)
        body_text = self._body(body) if method == "POST" else ""
        payload_to_sign = body_text if method == "POST" else query
        url = self.base_url + path + (f"?{query}" if query else "")
        attempts = self.safe_read_retry_attempts if method == "GET" else 1
        response: requests.Response | None = None
        for attempt in range(attempts):
            headers = {"Accept": "application/json"}
            if private:
                if not self._access_key or not self._secret_key:
                    raise BybitAPIError("private Bybit credentials are not configured")
                timestamp = str(int(time.time() * 1000))
                headers.update({
                    "X-BAPI-API-KEY": self._access_key,
                    "X-BAPI-TIMESTAMP": timestamp,
                    "X-BAPI-RECV-WINDOW": str(self.recv_window_ms),
                    "X-BAPI-SIGN": self.signature(
                        self._secret_key, timestamp, self._access_key,
                        self.recv_window_ms, payload_to_sign,
                    ),
                })
            if method == "POST":
                headers["Content-Type"] = "application/json"
            try:
                response = self.session.request(
                    method, url, headers=headers,
                    data=body_text if method == "POST" else None,
                    timeout=self.timeout_seconds,
                )
            except requests.RequestException as exc:
                if attempt + 1 < attempts:
                    time.sleep(self.safe_read_retry_backoff_seconds * (attempt + 1))
                    continue
                raise BybitAPIError(f"Bybit transport error: {type(exc).__name__}") from exc
            try:
                data = response.json()
            except ValueError as exc:
                raise BybitAPIError("Bybit returned non-JSON response",
                                    status_code=response.status_code) from exc
            if (method == "GET" and attempt + 1 < attempts
                    and self._is_retryable_read_response(
                        status_code=response.status_code, payload=data,
                    )):
                time.sleep(self.safe_read_retry_backoff_seconds * (attempt + 1))
                continue
            break
        if response is None:
            raise BybitAPIError("Bybit transport error: no response")
        code = data.get("retCode") if isinstance(data, dict) else None
        if response.status_code >= 400 or not isinstance(data, dict) or code != 0:
            message = data.get("retMsg") if isinstance(data, dict) else None
            raise BybitAPIError(
                f"Bybit request rejected: {message or 'unknown error'}",
                code=code, status_code=response.status_code,
            )
        result = data.get("result")
        return result if isinstance(result, dict) else {}

    def contract_info(self, symbol: str) -> dict[str, Any]:
        native = self.native_symbol(symbol)
        result = self._request(
            "GET", "/v5/market/instruments-info",
            params={"category": "linear", "symbol": native},
        )
        rows = result.get("list") or []
        item = next((row for row in rows if str(row.get("symbol")) == native), None)
        if not isinstance(item, dict):
            raise BybitAPIError("Bybit contract metadata missing")
        price_filter = item.get("priceFilter") or {}
        lot = item.get("lotSizeFilter") or {}
        leverage = item.get("leverageFilter") or {}
        risk = item.get("riskParameters") or {}
        return {
            "symbol": native,
            "state": 0 if str(item.get("status")) == "Trading" else -1,
            "apiAllowed": str(item.get("status")) == "Trading",
            "futureType": 1,
            "quoteCoin": item.get("quoteCoin"),
            "baseCoin": item.get("baseCoin"),
            "symbolType": item.get("symbolType"),
            "conceptPlate": [item.get("symbolType")] if item.get("symbolType") else [],
            "displayName": item.get("displayName") or item.get("baseCoin"),
            "preMarket": str(item.get("contractType")) == "LinearPreMarket",
            "typeLabel": 0,
            "contractSize": 1.0,
            "priceUnit": float(price_filter.get("tickSize") or 0),
            "volUnit": float(lot.get("qtyStep") or 0),
            "minVol": float(lot.get("minOrderQty") or 0),
            "maxVol": float(lot.get("maxOrderQty") or lot.get("maxMktOrderQty") or 0),
            "limitMaxVol": float(lot.get("maxOrderQty") or 0),
            "minLeverage": float(leverage.get("minLeverage") or 1),
            "maxLeverage": float(leverage.get("maxLeverage") or 1),
            "countryConfigContractMaxLeverage": 0,
            "maintenanceMarginRate": float(risk.get("maintenanceMarginRate") or 0.005),
            "liquidationFeeRate": 0.0,
            "raw": item,
        }

    def depth(self, symbol: str, limit: int = 20) -> dict[str, Any]:
        result = self._request(
            "GET", "/v5/market/orderbook",
            params={"category": "linear", "symbol": self.native_symbol(symbol), "limit": limit},
        )
        asks = [[float(price), float(qty)] for price, qty in (result.get("a") or [])]
        bids = [[float(price), float(qty)] for price, qty in (result.get("b") or [])]
        if not asks or not bids:
            raise BybitAPIError("Bybit order book missing")
        return {"asks": asks, "bids": bids, "timestamp": result.get("ts")}

    def ticker(self, symbol: str) -> dict[str, Any]:
        result = self._request(
            "GET", "/v5/market/tickers",
            params={"category": "linear", "symbol": self.native_symbol(symbol)},
        )
        rows = result.get("list") or []
        if not rows:
            raise BybitAPIError("Bybit ticker missing")
        row = rows[0]
        return {
            "fairPrice": row.get("markPrice"),
            "lastPrice": row.get("lastPrice"),
            "bid1": row.get("bid1Price"),
            "ask1": row.get("ask1Price"),
            "raw": row,
        }

    def account_asset(self, currency: str = "USDT") -> dict[str, Any]:
        result = self._request(
            "GET", "/v5/account/wallet-balance",
            params={"accountType": "UNIFIED", "coin": currency}, private=True,
        )
        rows = result.get("list") or []
        if not rows:
            raise BybitAPIError("Bybit account balance missing")
        account = rows[0]
        coins = [row for row in (account.get("coin") or []) if isinstance(row, dict)]
        coin = next((row for row in coins if str(row.get("coin") or "") == currency), {})
        total_available = account.get("totalAvailableBalance")
        if total_available not in (None, ""):
            available = float(total_available)
            available_basis = "account_total_available"
        else:
            # UTA isolated margin intentionally leaves account-wide margin
            # fields blank. Use only free USDT wallet funds and subtract every
            # explicit reservation exposed by the coin row.
            available = max(
                0.0,
                float(coin.get("walletBalance") or 0)
                - float(coin.get("totalOrderIM") or 0)
                - float(coin.get("totalPositionIM") or 0)
                - float(coin.get("locked") or 0),
            )
            available_basis = "isolated_coin_wallet_less_reserved"
        return {
            "equity": account.get("totalEquity") or coin.get("equity"),
            "availableOpen": available,
            "availableOpenBasis": available_basis,
            "raw": account,
        }

    def fee_rate(self, symbol: str) -> dict[str, float]:
        result = self._request(
            "GET", "/v5/account/fee-rate", private=True,
            params={"category": "linear", "symbol": self.native_symbol(symbol)},
        )
        rows = result.get("list") or []
        if not rows:
            raise BybitAPIError("Bybit account fee rate missing")
        row = rows[0]
        return {
            "makerFeeRate": float(row.get("makerFeeRate") or 0),
            "takerFeeRate": float(row.get("takerFeeRate") or 0),
        }

    def api_key_info(self) -> dict[str, Any]:
        return self._request("GET", "/v5/user/query-api", private=True)

    def sign_stock_perpetuals_agreement(self) -> dict[str, Any]:
        """Accept Bybit's single TradFi terms block for stock perpetuals.

        Bybit categoryV2=1 covers the shared precious-metals/stock-perpetual
        agreement. This is intentionally separate from order submission: it is
        an account-level, one-time operation and must never be retried by the
        execution worker.
        """
        return self._request(
            "POST", "/v5/user/agreement", private=True,
            body={"agree": True, "categoryV2": 1},
        )

    def open_positions(self, symbol: str | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"category": "linear"}
        if symbol:
            params["symbol"] = self.native_symbol(symbol)
        else:
            params["settleCoin"] = "USDT"
        result = self._request("GET", "/v5/position/list", params=params, private=True)
        output = []
        for item in result.get("list") or []:
            size = float(item.get("size") or 0)
            if size <= 0:
                continue
            side = str(item.get("side") or "")
            position_idx = int(item.get("positionIdx") or 0)
            native = str(item.get("symbol") or "")
            output.append({
                "positionId": f"{native}:{position_idx}:{side}",
                "symbol": native,
                "positionIdx": position_idx,
                "positionType": 1 if side == "Buy" else 2,
                "holdVol": size,
                "openAvgPrice": item.get("avgPrice"),
                "liquidatePrice": item.get("liqPrice"),
                "leverage": item.get("leverage"),
                "stopLoss": item.get("stopLoss"),
                "takeProfit": item.get("takeProfit"),
                "raw": item,
            })
        return output

    def set_leverage(self, symbol: str, leverage: int) -> dict[str, Any]:
        value = str(int(leverage))
        try:
            return self._request(
                "POST", "/v5/position/set-leverage", private=True,
                body={"category": "linear", "symbol": self.native_symbol(symbol),
                      "buyLeverage": value, "sellLeverage": value},
            )
        except BybitAPIError as exc:
            if str(exc.code) == "110043":
                return {"unchanged": True}
            raise

    def create_entry(self, *, symbol: str, direction: str, qty: float, price: float,
                     order_link_id: str, position_idx: int = 0) -> dict[str, Any]:
        body = {
            "category": "linear", "symbol": self.native_symbol(symbol),
            "side": "Buy" if direction == "long" else "Sell",
            "orderType": "Limit", "qty": str(qty), "price": str(price),
            "timeInForce": "IOC", "positionIdx": int(position_idx),
            "orderLinkId": order_link_id, "reduceOnly": False,
        }
        result = self._request("POST", "/v5/order/create", body=body, private=True)
        if not result.get("orderId"):
            raise BybitAPIError("Bybit create-order response missing orderId")
        return {"orderId": str(result["orderId"]), "orderLinkId": order_link_id, "raw": result}

    def order_by_external_id(self, symbol: str, order_link_id: str) -> dict[str, Any]:
        params = {"category": "linear", "symbol": self.native_symbol(symbol),
                  "orderLinkId": order_link_id}
        result = self._request("GET", "/v5/order/realtime", params=params, private=True)
        rows = result.get("list") or []
        if not rows:
            result = self._request("GET", "/v5/order/history", params=params, private=True)
            rows = result.get("list") or []
        if not rows:
            raise BybitAPIError("Bybit external order missing")
        row = rows[0]
        status = str(row.get("orderStatus") or "")
        filled_qty = float(row.get("cumExecQty") or 0)
        terminal = status in {"Filled", "Cancelled", "Rejected", "Deactivated", "PartiallyFilledCanceled"}
        if status == "Filled":
            state = 3
        elif terminal and filled_qty > 0:
            state = 5
        elif terminal:
            state = 4
        else:
            state = 2
        return {
            "orderId": str(row.get("orderId") or ""),
            "externalOid": str(row.get("orderLinkId") or order_link_id),
            "state": state,
            "dealAvgPrice": row.get("avgPrice"),
            "dealVol": row.get("cumExecQty"),
            "leavesQty": row.get("leavesQty"),
            "terminal": terminal,
            "orderStatus": status,
            "raw": row,
        }

    def set_full_stop(self, *, symbol: str, stop_loss: float,
                      position_idx: int = 0) -> dict[str, Any]:
        return self._request(
            "POST", "/v5/position/trading-stop", private=True,
            body={"category": "linear", "symbol": self.native_symbol(symbol),
                  "tpslMode": "Full", "positionIdx": int(position_idx),
                  "stopLoss": str(stop_loss), "slTriggerBy": "MarkPrice",
                  "slOrderType": "Market"},
        )

    def place_reduce_only_limit(self, *, symbol: str, direction: str, qty: float,
                                price: float, order_link_id: str,
                                position_idx: int = 0) -> dict[str, Any]:
        result = self._request(
            "POST", "/v5/order/create", private=True,
            body={"category": "linear", "symbol": self.native_symbol(symbol),
                  "side": "Sell" if direction == "long" else "Buy",
                  "orderType": "Limit", "qty": str(qty), "price": str(price),
                  "timeInForce": "GTC", "positionIdx": int(position_idx),
                  "orderLinkId": order_link_id, "reduceOnly": True},
        )
        if not result.get("orderId"):
            raise BybitAPIError("Bybit TP order response missing orderId")
        return {"orderId": str(result["orderId"]), "orderLinkId": order_link_id, "raw": result}

    def cancel_order(self, *, symbol: str, order_id: str | None = None,
                     order_link_id: str | None = None) -> dict[str, Any]:
        body = {"category": "linear", "symbol": self.native_symbol(symbol)}
        if order_id:
            body["orderId"] = str(order_id)
        elif order_link_id:
            body["orderLinkId"] = str(order_link_id)
        else:
            raise ValueError("order identity required")
        return self._request("POST", "/v5/order/cancel", body=body, private=True)

    def close_market(self, *, symbol: str, direction: str, qty: float,
                     order_link_id: str, position_idx: int = 0) -> dict[str, Any]:
        result = self._request(
            "POST", "/v5/order/create", private=True,
            body={"category": "linear", "symbol": self.native_symbol(symbol),
                  "side": "Sell" if direction == "long" else "Buy",
                  "orderType": "Market", "qty": str(qty),
                  "timeInForce": "IOC", "positionIdx": int(position_idx),
                  "orderLinkId": order_link_id, "reduceOnly": True,
                  "closeOnTrigger": True},
        )
        if not result.get("orderId"):
            raise BybitAPIError("Bybit emergency close response missing orderId")
        return {"orderId": str(result["orderId"]), "orderLinkId": order_link_id, "raw": result}

    def closed_pnl(self, symbol: str, limit: int = 50) -> list[dict[str, Any]]:
        result = self._request(
            "GET", "/v5/position/closed-pnl", private=True,
            params={"category": "linear", "symbol": self.native_symbol(symbol), "limit": limit},
        )
        return [row for row in (result.get("list") or []) if isinstance(row, dict)]

    def klines(self, symbol: str, *, start_ms: int, end_ms: int,
               interval: str = "1") -> list[dict[str, float | int]]:
        result = self._request(
            "GET", "/v5/market/kline",
            params={"category": "linear", "symbol": self.native_symbol(symbol),
                    "interval": interval, "start": int(start_ms), "end": int(end_ms), "limit": 1000},
        )
        rows = []
        for item in result.get("list") or []:
            rows.append({"candle_at": int(item[0]), "open": float(item[1]),
                         "high": float(item[2]), "low": float(item[3]), "close": float(item[4])})
        return sorted(rows, key=lambda row: int(row["candle_at"]))

    def recent_high(self, symbol: str, *, start_seconds: int,
                    end_seconds: int | None = None) -> float | None:
        end_ms = int((end_seconds or time.time()) * 1000)
        rows = self.klines(symbol, start_ms=int(start_seconds * 1000), end_ms=end_ms)
        values = [float(row["high"]) for row in rows]
        return max(values) if values else None

    def recent_low(self, symbol: str, *, start_seconds: int,
                   end_seconds: int | None = None) -> float | None:
        end_ms = int((end_seconds or time.time()) * 1000)
        rows = self.klines(symbol, start_ms=int(start_seconds * 1000), end_ms=end_ms)
        values = [float(row["low"]) for row in rows]
        return min(values) if values else None
