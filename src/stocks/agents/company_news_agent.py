"""CompanyNewsAgent — filter and tag news for stock symbols.

Reuses the shared SQLite news_items table (rows tagged asset_class='stocks'
are matched directly; crypto rows are scanned only if their detected_symbols
includes a ticker that's also in our stocks universe — that handles e.g.
Bloomberg posts that mention both COIN and BTC).

This is intentionally minimal in Stage 4. The full classification matrix
(company / sector / index / analyst / earnings / etc.) is deferred to
Stage 5 once the supervisor wires news_trader bridge into stocks.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any

from src.stocks.agents.base import StocksBaseAgent


@dataclass
class StockNewsHit:
    symbol: str
    title: str
    source: str
    url: str
    published_at: str
    importance: float | None


class CompanyNewsAgent(StocksBaseAgent):
    name = "stock_company_news"

    def run(
        self,
        symbols: list[str] | None = None,
        *,
        lookback_limit: int = 200,
        prefer_stocks_tagged: bool = True,
    ) -> dict[str, Any]:
        """Surface news hits for the requested stocks.

        Strategy:
          1. Strongly prefer rows tagged asset_class='stocks' — they're known
             to come from stock-relevant feeds.
          2. Fall back to crypto-tagged rows that mention a tracked stock
             ticker (cross-asset coverage, e.g. a CoinDesk piece naming COIN
             or MSTR). Detected_symbols intersection with our universe is the
             gate.
        """
        symbols = [s.upper() for s in (symbols or self.stocks_config.default_symbols)]
        sym_set = set(symbols)

        # Time-window (72h) instead of a latest-N tail, so a busy hour of PR-Newswire noise can't push a
        # real company catalyst out of the lookback. Per-symbol capped below so the packet stays bounded.
        try:
            rows = self.db.load_news_window(hours=72, limit=max(lookback_limit, 4000))
        except Exception:
            rows = self.db.load_recent_news(limit=lookback_limit)
        _MAX_HITS_PER_SYMBOL = 8
        hits: dict[str, list[StockNewsHit]] = {s: [] for s in symbols}
        counted_stocks_tagged = 0
        counted_cross_asset = 0

        for row in rows:
            row_asset_class = (row.get("asset_class") or "crypto").lower()
            try:
                detected = json.loads(row.get("detected_symbols_json") or "[]")
            except Exception:
                detected = []
            matched = {
                str(s).split("/")[0].upper() for s in detected
            } & sym_set
            if not matched:
                continue

            # Stocks-tagged rows always count. Other rows count when the
            # cross-asset gate is open (default true) AND the symbol matches.
            if row_asset_class == "stocks":
                counted_stocks_tagged += 1
            elif prefer_stocks_tagged:
                counted_cross_asset += 1
            else:
                continue

            for symbol in matched:
                if len(hits[symbol]) >= _MAX_HITS_PER_SYMBOL:   # per-symbol cap (bounds the packet)
                    continue
                hits[symbol].append(
                    StockNewsHit(
                        symbol=symbol,
                        title=str(row.get("title") or ""),
                        source=str(row.get("source") or ""),
                        url=str(row.get("url") or ""),
                        published_at=str(row.get("published_at") or ""),
                        importance=(
                            float(row["importance"])
                            if row.get("importance") is not None
                            else None
                        ),
                    )
                )

        payload = {
            "symbols": symbols,
            "lookback_limit": lookback_limit,
            "counts": {
                "stocks_tagged": counted_stocks_tagged,
                "cross_asset": counted_cross_asset,
            },
            "hits_by_symbol": {
                sym: [asdict(h) for h in items] for sym, items in hits.items()
            },
            "has_catalyst": [sym for sym, items in hits.items() if items],
        }
        self.save_output(payload)
        return payload
