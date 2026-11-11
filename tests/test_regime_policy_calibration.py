from datetime import datetime, timezone

from src.execution import regime_policy_calibration as rpc


def test_crypto_unknown_label_uses_available_btc_data_instead_of_bearish_default():
    assert rpc.crypto_regime({
        "btc_regime_state": "unknown", "btc_15m_return": 0.04,
        "btc_1h_return": 0.35, "btc_ema_slope_state": "up",
    }) == "risk_on"


def test_crypto_explicit_risk_off_and_chop_remain_distinct():
    assert rpc.crypto_regime({"btc_regime_state": "risk_off"}) == "risk_off"
    assert rpc.crypto_regime({"btc_regime_state": "chop"}) == "chop"


def test_stocks_regime_normalizes_transition_without_calling_it_risk_off():
    assert rpc.stocks_regime("transition") == "neutral"
    assert rpc.stocks_regime("bullish") == "risk_on"
    assert rpc.stocks_regime("risk_off") == "risk_off"


def test_metrics_and_recommendations_require_chronological_confirmation():
    def metric(n, pf, net_r):
        return {"n": n, "profit_factor": pf, "net_r": net_r, "usd_coverage": 0}

    crypto = {
        ("intraday", "long", "risk_off", "all"): metric(10, 0.2, -6.0),
        ("swing", "long", "chop", "train"): metric(12, 1.8, 4.0),
        ("swing", "long", "chop", "validation"): metric(6, 1.4, 2.0),
        ("intraday", "long", "chop", "validation"): metric(7, 0.7, -1.0),
    }
    recs = rpc._recommendations(crypto, {})
    policies = {item["scope"]: item["policy"] for item in recs}
    assert policies["crypto intraday long / risk_off"] == "KEEP_CURRENT_UNTIL_USD_EVIDENCE"
    assert policies["crypto swing long / chop"] == "KEEP_CURRENT_INSUFFICIENT_USD_EVIDENCE"
    assert policies["crypto intraday long / chop"] == "KEEP_CURRENT_INSUFFICIENT_USD_EVIDENCE"
