"""Populate the Market dashboard NOW from available desk data (PAPER/display).

Stop-gap "turn it on" until the 4h Opus enriched-review final block takes over: builds a
real snapshot from recent news_items (top by importance), the most-common recent regime
per asset class, and the crypto Fear & Greed index (alternative.me, fail-open to null).
Writes one `market_dashboard_snapshots` row. No trading logic touched.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.market.market_dashboard import store_snapshot, fetch_market_extras, DB


ROOT = Path(__file__).resolve().parents[1]
AGENT_OUTPUTS = ROOT / "data" / "processed" / "agent_outputs"

_NEG = ("bear", "selloff", "sell-off", "slide", "outflow", "pulled", "dump", "down",
        "downgrade", "lawsuit", "hack", "liquidat", "crash", "fear", "risk")
_POS = ("bull", "upgrade", "rally", "inflow", "surge", "approval", "beat", "record high",
        "breakout", "pump", "buyback")
_LONGTERM = ("2030", "2027", "prediction", "long-term", "halving", "etf", "roadmap",
             "upgrade roadmap", "thesis", "macro", "fed", "rate")


def _impact(title: str) -> str:
    t = (title or "").lower()
    if any(k in t for k in _NEG):
        return "negative"
    if any(k in t for k in _POS):
        return "positive"
    return "mixed"


def _fear_greed():
    try:
        import urllib.request
        with urllib.request.urlopen("https://api.alternative.me/fng/?limit=1", timeout=6) as r:
            d = json.loads(r.read().decode())
        v = d["data"][0]
        return int(v["value"]), v.get("value_classification")
    except Exception:
        return None, None


def _mode_from_regime(reg: str, asset: str) -> str:
    r = (reg or "").lower()
    if "bear" in r or "risk_off" in r or "down" in r:
        return "risk_off"
    if "bull" in r or "risk_on" in r or "up" in r:
        return "risk_on" if asset == "stocks" else "trend"
    if "chop" in r or "range" in r:
        return "chop"
    return "unknown"


def _canonical_agent_regime(
    asset: str, *, now: datetime, max_age_minutes: float = 240.0,
) -> tuple[str, str, float, str] | None:
    """Read the fresh, asset-specific regime agent instead of stale signals."""
    pattern = (
        "*_stocks_stocks_market_regime.json"
        if asset == "stocks" else "*_market_regime_agent.json"
    )
    candidates = sorted(
        AGENT_OUTPUTS.glob(pattern), key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for path in candidates:
        modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        age_minutes = max(0.0, (now - modified).total_seconds() / 60.0)
        if age_minutes > max_age_minutes:
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if asset == "stocks":
            regime = payload.get("regime") or {}
            label = str(regime.get("label") or "").strip()
            bias = str(regime.get("bias") or "neutral").lower()
            mode = (
                "risk_on" if bool(regime.get("risk_on")) or bias == "long"
                else "risk_off" if bias == "short" or label == "risk_off"
                else "chop" if label in {"chop", "range"}
                else "unknown"
            )
            confidence = min(1.0, max(0.0, len(regime.get("indices") or []) / 4.0))
        else:
            label = str(payload.get("label") or "").strip()
            risk_mode = str(payload.get("risk_mode") or "").lower()
            mode = (
                "trend" if risk_mode in {"risk-on", "cautious-risk-on"}
                else "risk_off" if risk_mode in {
                    "risk-off", "cautious-risk-off", "danger"
                }
                else "chop" if label in {"range/chop", "chop", "range"}
                else "unknown"
            )
            confidence = min(1.0, max(0.0, float(payload.get("confidence") or 0.0) / 100.0))
        if label:
            return label, mode, confidence, path.name
    return None


def main() -> int:
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    now = datetime.now(timezone.utc)

    def top_regime(asset):
        r = con.execute(
            "SELECT market_regime reg, count(*) n FROM proposed_signals "
            "WHERE asset_class=? AND created_at>=datetime('now','-1 day') AND COALESCE(market_regime,'')!='' "
            "GROUP BY market_regime ORDER BY n DESC LIMIT 1", (asset,)).fetchone()
        return (r["reg"] if r else None) or "unknown"

    crypto_agent = _canonical_agent_regime("crypto", now=now)
    stocks_agent = _canonical_agent_regime("stocks", now=now)
    crypto_reg = crypto_agent[0] if crypto_agent else top_regime("crypto")
    stocks_reg = stocks_agent[0] if stocks_agent else top_regime("stocks")
    crypto_mode = crypto_agent[1] if crypto_agent else _mode_from_regime(crypto_reg, "crypto")
    stocks_mode = stocks_agent[1] if stocks_agent else _mode_from_regime(stocks_reg, "stocks")
    regime_confidence = min(
        crypto_agent[2] if crypto_agent else 0.5,
        stocks_agent[2] if stocks_agent else 0.5,
    )

    def news(asset, longterm, limit):
        rows = con.execute(
            "SELECT title, source, importance, detected_symbols_json, asset_class "
            "FROM news_items WHERE published_at>=datetime('now','-2 day') AND asset_class=? "
            "ORDER BY importance DESC, published_at DESC LIMIT 40", (asset,)).fetchall()
        out = []
        for r in rows:
            t = r["title"] or ""
            is_lt = any(k in t.lower() for k in _LONGTERM)
            if is_lt != longterm:
                continue
            syms = []
            try:
                syms = json.loads(r["detected_symbols_json"] or "[]")[:3]
            except Exception:
                pass
            out.append({"title": t[:140], "asset_or_sector": ", ".join(syms) or asset,
                        "_asset": asset,
                        "impact": _impact(t), "horizon": "multi_day_or_long_term" if longterm else "today",
                        "confidence": round(min(1.0, (r["importance"] or 0) / 4.0), 2),
                        "why_it_matters": f"{r['source']} · importance {r['importance']}"})
            if len(out) >= limit:
                break
        return out

    today = (news("crypto", False, 3) + news("stocks", False, 3))[:6]
    longterm = (news("crypto", True, 3) + news("stocks", True, 2))[:5]
    # PART 5 — main risk deduped strictly BY ASSET CLASS so stocks risk ≠ the crypto/BTC headline.
    crypto_risk = next((n["title"] for n in today if n["_asset"] == "crypto" and n["impact"] == "negative"), None) \
        or next((n["title"] for n in today if n["_asset"] == "crypto"), None) or f"crypto regime: {crypto_reg}"
    stocks_risk = next((n["title"] for n in today if n["_asset"] == "stocks" and n["impact"] == "negative"), None) \
        or next((n["title"] for n in today if n["_asset"] == "stocks"), None) or f"stocks regime: {stocks_reg}"
    if stocks_risk == crypto_risk:       # never show the same headline for both
        stocks_risk = f"stocks regime: {stocks_reg}"

    fng, fng_cls = _fear_greed()
    ex = fetch_market_extras()   # VIX / SPY / QQQ / ETH-BTC (deterministic, fail-open)
    snap = {
        "timestamp": now.isoformat(),
        "crypto_fear_greed": fng,
        "crypto_market_mode": crypto_mode,
        "stocks_market_mode": stocks_mode,
        "crypto_main_risk": crypto_risk[:200],
        "stocks_main_risk": stocks_risk[:200],
        "today_news": today, "long_term_news": longterm,
        "crypto_regime": crypto_reg, "stocks_regime": stocks_reg,
        "btc_dominance": ex.get("btc_dominance"), "eth_btc": ex.get("eth_btc"),
        "vix": ex.get("vix"), "spy_trend": ex.get("spy_trend"), "qqq_trend": ex.get("qqq_trend"),
        "confidence": regime_confidence,
        "source_summary": (f"desk news_items (2d) + canonical regime agents + alternative.me F&G + {ex.get('vix_source')}"
                           f"{'' if fng is not None else ' (F&G unavailable)'}"),
        "generated_by": "populate_market_dashboard_now",
        "raw_json": json.dumps({
            "crypto_reg": crypto_reg,
            "stocks_reg": stocks_reg,
            "crypto_regime_source": crypto_agent[3] if crypto_agent else "proposed_signals_fallback",
            "stocks_regime_source": stocks_agent[3] if stocks_agent else "proposed_signals_fallback",
            "fng_class": fng_cls,
            "vix_source": ex.get("vix_source"),
        }),
    }
    sid = store_snapshot(con, snap)
    con.close()
    print(f"stored snapshot id={sid}: crypto_mode={snap['crypto_market_mode']} "
          f"stocks_mode={snap['stocks_market_mode']} F&G={fng} VIX={ex.get('vix')} "
          f"SPY={ex.get('spy_trend')} QQQ={ex.get('qqq_trend')} ETH/BTC={ex.get('eth_btc')} "
          f"today_news={len(today)} long_term={len(longterm)}")
    print("crypto_main_risk:", snap["crypto_main_risk"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
