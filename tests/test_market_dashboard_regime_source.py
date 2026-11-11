from __future__ import annotations

import json
from datetime import datetime, timezone

import scripts.populate_market_dashboard_now as dashboard


def test_dashboard_prefers_fresh_asset_specific_regime_agents(tmp_path, monkeypatch):
    monkeypatch.setattr(dashboard, "AGENT_OUTPUTS", tmp_path)
    (tmp_path / "20260922_080000_market_regime_agent.json").write_text(
        json.dumps({
            "label": "high-volatility trend",
            "risk_mode": "cautious-risk-on",
            "confidence": 85.0,
        }),
        encoding="utf-8",
    )
    (tmp_path / "20260922_080000_stocks_stocks_market_regime.json").write_text(
        json.dumps({
            "regime": {
                "label": "transition",
                "bias": "neutral",
                "risk_on": False,
                "indices": [{}, {}, {}, {}],
            }
        }),
        encoding="utf-8",
    )
    now = datetime.now(timezone.utc)

    crypto = dashboard._canonical_agent_regime("crypto", now=now)
    stocks = dashboard._canonical_agent_regime("stocks", now=now)

    assert crypto is not None
    assert crypto[:3] == ("high-volatility trend", "trend", 0.85)
    assert stocks is not None
    assert stocks[:3] == ("transition", "unknown", 1.0)
