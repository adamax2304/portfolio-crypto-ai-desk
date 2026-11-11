from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any
from urllib.parse import quote, urlencode

import requests


class MexcAPIError(RuntimeError):
    def __init__(self, message: str, *, code: Any = None, status_code: int | None = None):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class MexcFuturesClient:
    def __init__(self, *, access_key: str = "", secret_key: str = "",
                 base_url: str = "https://api.mexc.com", recv_window_seconds: int = 10,
                 timeout_seconds: float = 8.0, session: requests.Session | None = None,
                 safe_read_retry_attempts: int = 1,
                 safe_read_retry_backoff_seconds: float = 0.25):
        self._access_key = access_key
        self._secret_key = secret_key
        self.base_url = base_url.rstrip("/")
        self.recv_window_seconds = min(max(int(recv_window_seconds), 1), 30)
        self.timeout_seconds = float(timeout_seconds)
        self.session = session or requests.Session()
        # GET requests only read contract/account state. Retrying them can make
        # a short MEXC transport wobble survivable before a live preflight is
        # rejected. POST submission remains exactly-once at this layer.
        self.safe_read_retry_attempts = max(1, int(safe_read_retry_attempts))
        self.safe_read_retry_backoff_seconds = max(0.0, float(safe_read_retry_backoff_seconds))

    @staticmethod
    def native_symbol(symbol: str) -> str:
        text = str(symbol or "").upper().replace("-", "/")
        if "/" in text:
            base, quote_asset = text.split("/", 1)
            return f"{base}_{quote_asset}"
        if "_" in text:
            return text
        if text.endswith("USDT"):
            return f"{text[:-4]}_USDT"
        return text

    @staticmethod
    def signature(access_key: str, secret_key: str, timestamp_ms: str,
                  parameter_string: str) -> str:
        target = f"{access_key}{timestamp_ms}{parameter_string}".encode("utf-8")
        return hmac.new(secret_key.encode("utf-8"), target, hashlib.sha256).hexdigest()

    @staticmethod
    def _query_string(params: dict[str, Any] | None) -> str:
        clean = {k: v for k, v in (params or {}).items() if v is not None}
        return urlencode(sorted(clean.items()), doseq=True)

    @staticmethod
    def _json_body(body: Any) -> str:
        return json.dumps(body if body is not None else {}, separators=(",", ":"), ensure_ascii=True)

    def _request(self, method: str, path: str, *, params: dict[str, Any] | None = None,
                 body: Any = None, private: bool = False) -> Any:
        method = method.upper()
        query = self._query_string(params)
        body_text = self._json_body(body) if method == "POST" else ""
        url = self.base_url + path + (f"?{query}" if query else "")
        attempts = self.safe_read_retry_attempts if method == "GET" else 1
        response = None
        last_transport_error: requests.RequestException | None = None
        for attempt in range(attempts):
            headers = {"Language": "en-US", "Accept": "application/json"}
            if private:
                if not self._access_key or not self._secret_key:
                    raise MexcAPIError("private MEXC credentials are not configured")
                # Each retry gets a fresh signature: a slow first read must not
                # consume the exchange receive window of the next one.
                ts = str(int(time.time() * 1000))
                parameter_string = body_text if method == "POST" else query
                headers.update({
                    "ApiKey": self._access_key,
                    "Request-Time": ts,
                    "Recv-Window": str(self.recv_window_seconds),
                    "Signature": self.signature(self._access_key, self._secret_key, ts, parameter_string),
                })
            try:
                response = self.session.request(
                    method, url, data=body_text if method == "POST" else None,
                    headers={**headers, **({"Content-Type": "application/json"} if method == "POST" else {})},
                    timeout=self.timeout_seconds,
                )
            except requests.RequestException as exc:
                last_transport_error = exc
                if attempt + 1 < attempts:
                    time.sleep(self.safe_read_retry_backoff_seconds * (attempt + 1))
                    continue
                raise MexcAPIError(f"MEXC transport error: {type(exc).__name__}") from exc
            # A failed safe read before an order exists may be retried. Do not
            # apply this rule to POST: a timed-out submit could already exist.
            if (method == "GET" and response.status_code in {408, 425, 429, 500, 502, 503, 504}
                    and attempt + 1 < attempts):
                time.sleep(self.safe_read_retry_backoff_seconds * (attempt + 1))
                continue
            break
        if response is None:
            error_name = type(last_transport_error).__name__ if last_transport_error else "Unknown"
            raise MexcAPIError(f"MEXC transport error: {error_name}")
        try:
            payload = response.json()
        except ValueError as exc:
            raise MexcAPIError("MEXC returned non-JSON response", status_code=response.status_code) from exc
        if response.status_code >= 400 or not isinstance(payload, dict) or payload.get("success") is not True:
            code = payload.get("code") if isinstance(payload, dict) else None
            message = payload.get("message") if isinstance(payload, dict) else None
            raise MexcAPIError(f"MEXC request rejected: {message or 'unknown error'}",
                               code=code, status_code=response.status_code)
        return payload.get("data")

    def contract_info(self, symbol: str) -> dict[str, Any]:
        # The regional catalogue retains closed legacy symbols. Individual
        # order preflight uses the documented tradable-contract endpoint.
        data = self._request("GET", "/api/v1/contract/detail",
                             params={"symbol": self.native_symbol(symbol)})
        if isinstance(data, list):
            wanted = self.native_symbol(symbol)
            data = next((x for x in data if str((x or {}).get("symbol")) == wanted), None)
        if not isinstance(data, dict):
            raise MexcAPIError("MEXC contract metadata missing")
        return data

    def contracts(self) -> list[dict[str, Any]]:
        """Return the public futures contract catalogue.

        The stock-futures Paper lane uses this to discover current MEXC
        contracts instead of assuming that ``TICKER_USDT`` exists. No private
        credentials are used.
        """
        data = self._request("GET", "/api/v1/contract/detail/country")
        if not isinstance(data, list):
            raise MexcAPIError("MEXC contract catalogue missing")
        return [item for item in data if isinstance(item, dict)]

    def depth(self, symbol: str, limit: int = 20) -> dict[str, Any]:
        native = quote(self.native_symbol(symbol), safe="_")
        data = self._request("GET", f"/api/v1/contract/depth/{native}", params={"limit": limit})
        if not isinstance(data, dict):
            raise MexcAPIError("MEXC order book missing")
        return data

    def ticker(self, symbol: str) -> dict[str, Any]:
        data = self._request("GET", "/api/v1/contract/ticker",
                             params={"symbol": self.native_symbol(symbol)})
        if isinstance(data, list):
            data = data[0] if data else None
        if not isinstance(data, dict):
            raise MexcAPIError("MEXC ticker missing")
        return data

    def recent_high(self, symbol: str, *, start_seconds: int, end_seconds: int | None = None) -> float | None:
        native = quote(self.native_symbol(symbol), safe="_")
        params = {"interval": "Min1", "start": int(start_seconds)}
        if end_seconds is not None:
            params["end"] = int(end_seconds)
        data = self._request("GET", f"/api/v1/contract/kline/{native}", params=params)
        highs = data.get("high") if isinstance(data, dict) else None
        values = [float(x) for x in (highs or []) if x not in (None, "")]
        return max(values) if values else None

    def recent_low(self, symbol: str, *, start_seconds: int, end_seconds: int | None = None) -> float | None:
        native = quote(self.native_symbol(symbol), safe="_")
        params = {"interval": "Min1", "start": int(start_seconds)}
        if end_seconds is not None:
            params["end"] = int(end_seconds)
        data = self._request("GET", f"/api/v1/contract/kline/{native}", params=params)
        lows = data.get("low") if isinstance(data, dict) else None
        values = [float(x) for x in (lows or []) if x not in (None, "")]
        return min(values) if values else None

    def klines(self, symbol: str, *, start_seconds: int, end_seconds: int,
               interval: str = "Min1") -> list[dict[str, float | int]]:
        """Return normalized public futures candles for the isolated parity ledger."""
        native = quote(self.native_symbol(symbol), safe="_")
        data = self._request(
            "GET",
            f"/api/v1/contract/kline/{native}",
            params={"interval": interval, "start": int(start_seconds), "end": int(end_seconds)},
        )
        if not isinstance(data, dict):
            raise MexcAPIError("MEXC kline response missing")
        fields = ("time", "open", "high", "low", "close")
        values = [data.get(name) or [] for name in fields]
        if len({len(value) for value in values}) != 1:
            raise MexcAPIError("MEXC kline arrays are inconsistent")
        rows: list[dict[str, float | int]] = []
        for candle_at, op, hi, lo, cl in zip(*values):
            rows.append({
                "candle_at": int(candle_at),
                "open": float(op),
                "high": float(hi),
                "low": float(lo),
                "close": float(cl),
            })
        return rows

    def account_asset(self, currency: str = "USDT") -> dict[str, Any]:
        data = self._request("GET", f"/api/v1/private/account/asset/{quote(currency, safe='')}",
                             private=True)
        if not isinstance(data, dict):
            raise MexcAPIError("MEXC account asset missing")
        return data

    def open_positions(self, symbol: str | None = None) -> list[dict[str, Any]]:
        params = {"symbol": self.native_symbol(symbol)} if symbol else None
        data = self._request("GET", "/api/v1/private/position/open_positions",
                             params=params, private=True)
        return [x for x in (data or []) if isinstance(x, dict)]

    def historical_positions(self, symbol: str | None = None, *, page_size: int = 100) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"page_num": 1, "page_size": min(max(page_size, 1), 100)}
        if symbol:
            params["symbol"] = self.native_symbol(symbol)
        data = self._request("GET", "/api/v1/private/position/list/history_positions",
                             params=params, private=True)
        if isinstance(data, dict):
            data = data.get("resultList") or data.get("data") or []
        return [x for x in (data or []) if isinstance(x, dict)]

    def position_mode(self) -> Any:
        return self._request("GET", "/api/v1/private/position/position_mode", private=True)

    def create_order(self, order: dict[str, Any]) -> dict[str, Any]:
        # MEXC Futures documents ``order/submit`` as the live order endpoint.
        # ``order/create`` can return an HTML/non-JSON response through some
        # gateways, leaving the client unable to prove whether an order exists.
        data = self._request("POST", "/api/v1/private/order/submit", body=order, private=True)
        # MEXC documents two successful response shapes for this endpoint:
        # ``{"orderId": ...}`` and a scalar order id in ``data``.  The latter
        # is common for close orders; normalise it before the caller decides a
        # real order is unknown or unsafe.
        if isinstance(data, (int, str)) and str(data).strip():
            return {"orderId": str(data)}
        if not isinstance(data, dict) or not data.get("orderId"):
            raise MexcAPIError("MEXC create-order response missing orderId")
        return data

    def order_by_external_id(self, symbol: str, external_oid: str) -> dict[str, Any]:
        native = quote(self.native_symbol(symbol), safe="_")
        oid = quote(str(external_oid), safe="")
        data = self._request("GET", f"/api/v1/private/order/external/{native}/{oid}", private=True)
        if not isinstance(data, dict):
            raise MexcAPIError("MEXC external order missing")
        return data

    def order_by_id(self, order_id: str | int) -> dict[str, Any]:
        oid = quote(str(order_id), safe="")
        data = self._request("GET", f"/api/v1/private/order/get/{oid}", private=True)
        if not isinstance(data, dict):
            raise MexcAPIError("MEXC order missing")
        return data

    def cancel_external(self, symbol: str, external_oid: str) -> Any:
        # Despite the singular endpoint's documentation showing a list example,
        # the live API accepts one object here (verified against MEXC Futures).
        return self._request("POST", "/api/v1/private/order/cancel_with_external",
                             body={"symbol": self.native_symbol(symbol), "externalOid": external_oid},
                             private=True)

    def cancel_order_ids(self, order_ids: list[str | int]) -> Any:
        return self._request("POST", "/api/v1/private/order/cancel",
                             body=[int(order_id) for order_id in order_ids], private=True)

    def open_tpsl_orders(self, symbol: str | None = None) -> list[dict[str, Any]]:
        params = {"symbol": self.native_symbol(symbol)} if symbol else None
        data = self._request("GET", "/api/v1/private/stoporder/open_orders",
                             params=params, private=True)
        return [x for x in (data or []) if isinstance(x, dict)]

    def place_position_tpsl(self, *, position_id: int, volume: float,
                            stop_loss: float | None, take_profit: float | None) -> Any:
        if not stop_loss and not take_profit:
            raise ValueError("at least one TP/SL price is required")
        body = {
            "lossTrend": 2, "profitTrend": 2, "positionId": position_id,
            "vol": volume, "stopLossPrice": stop_loss, "takeProfitPrice": take_profit,
            # A protective stop must not be suppressed by mark/index divergence.
            "priceProtect": 0, "profitLossVolType": "SAME", "volType": 2,
            "takeProfitType": 0, "takeProfitOrderPrice": take_profit,
            "stopLossType": 0, "stopLossOrderPrice": stop_loss,
        }
        return self._request("POST", "/api/v1/private/stoporder/place", body={
            key: value for key, value in body.items() if value is not None
        }, private=True)

    def place_close_limit(self, *, symbol: str, position_id: int, direction: str,
                          volume: float, price: float, leverage: int,
                          external_oid: str, open_type: int = 1) -> dict[str, Any]:
        """Place a documented partial close order against one hedge-mode position."""
        direction = str(direction).lower()
        if direction not in {"long", "short"}:
            raise ValueError("direction must be long or short")
        if volume <= 0 or price <= 0:
            raise ValueError("close-limit volume and price must be positive")
        return self.create_order({
            "symbol": self.native_symbol(symbol),
            "price": price,
            "vol": volume,
            "leverage": leverage,
            "side": 4 if direction == "long" else 2,
            "type": 1,
            "openType": open_type,
            "externalOid": external_oid,
            "positionId": position_id,
            "positionMode": 1,
        })

    def cancel_tpsl_order_ids(self, order_ids: list[str | int]) -> Any:
        return self._request(
            "POST", "/api/v1/private/stoporder/cancel",
            body=[{"stopPlanOrderId": int(order_id)} for order_id in order_ids],
            private=True,
        )

    def tpsl_orders(self, symbol: str | None = None, *, finished: bool | None = None,
                    page_size: int = 100) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "page_num": 1,
            "page_size": min(max(int(page_size), 1), 100),
        }
        if symbol:
            params["symbol"] = self.native_symbol(symbol)
        if finished is not None:
            params["is_finished"] = int(bool(finished))
        data = self._request(
            "GET", "/api/v1/private/stoporder/list/orders", params=params, private=True,
        )
        if isinstance(data, dict):
            data = data.get("resultList") or data.get("data") or []
        return [item for item in (data or []) if isinstance(item, dict)]

    def modify_tpsl(self, *, stop_plan_order_id: int, stop_loss: float,
                    take_profit: float | None = None) -> Any:
        body = {
            "lossTrend": 2,
            "stopPlanOrderId": stop_plan_order_id,
            "stopLossPrice": stop_loss,
        }
        if take_profit and float(take_profit) > 0:
            body.update({"profitTrend": 2, "takeProfitPrice": take_profit})
        return self._request("POST", "/api/v1/private/stoporder/change_plan_price",
                             body=body, private=True)

    def emergency_close_long(self, *, symbol: str, position_id: int,
                             volume: float, external_oid: str) -> dict[str, Any]:
        return self.emergency_close_position(
            symbol=symbol, position_id=position_id, volume=volume,
            external_oid=external_oid, direction="long",
        )

    def emergency_close_short(self, *, symbol: str, position_id: int,
                              volume: float, external_oid: str) -> dict[str, Any]:
        return self.emergency_close_position(
            symbol=symbol, position_id=position_id, volume=volume,
            external_oid=external_oid, direction="short",
        )

    def emergency_close_position(self, *, symbol: str, position_id: int,
                                 volume: float, external_oid: str,
                                 direction: str) -> dict[str, Any]:
        direction = str(direction).lower()
        if direction not in {"long", "short"}:
            raise ValueError("direction must be long or short")
        return self.create_order({
            "symbol": self.native_symbol(symbol), "price": 0, "vol": volume,
            "side": 4 if direction == "long" else 2,
            "type": 5, "openType": 1, "externalOid": external_oid,
            "positionId": position_id, "positionMode": 1,
        })
