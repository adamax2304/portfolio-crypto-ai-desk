"""Tests for the 2026-06-16 stocks concentration-cap overlay (src/signals/portfolio_caps.py)."""

from __future__ import annotations

from src.signals.portfolio_caps import apply_stock_concentration_caps
from src.stocks.risk_clusters import (
    get_stock_proxy_group,
    get_stock_risk_bucket,
    normalize_symbol,
)


def sig(symbol, *, tier="B", direction="long", score=70.0, mode="intraday",
        asset="stocks", day="2026-06-16", news=0, sid=None):
    return {
        "signal_id": sid or f"{symbol}_{direction}_{score}",
        "symbol": symbol, "asset_class": asset, "mode": mode, "tier": tier,
        "direction": direction, "score": score, "news_supported": news,
        "created_at": f"{day}T13:00:00+00:00",
        "entry_low": 100.0, "entry_high": 101.0, "stop_loss": 98.0, "tp1": 104.0,
    }


def _by_sym(out):
    return {r["signal_id"]: r for r in out}


# ---- risk_clusters helper -------------------------------------------------

def test_17_helper_known_and_unknown_symbols():
    assert get_stock_risk_bucket("AAPL") == "megacap_tech"
    assert get_stock_proxy_group("QQQ") == "qqq_xlk_proxy"
    assert get_stock_proxy_group("XLK") == "qqq_xlk_proxy"
    assert get_stock_risk_bucket("AMD") == "semis"
    assert normalize_symbol("aapl.us") == "AAPL"
    # unknown defaults safely, never crashes, own proxy bucket
    assert get_stock_risk_bucket("ZZZZ") == "unknown"
    assert "ZZZZ" in get_stock_proxy_group("ZZZZ")
    assert get_stock_risk_bucket(None) == "unknown"


# ---- Rule A: proxy collapse ----------------------------------------------

def test_1_qqq_xlk_collapse_keeps_best_score():
    out = _by_sym(apply_stock_concentration_caps([
        sig("QQQ", score=80, sid="qqq"), sig("XLK", score=70, sid="xlk"),
    ]))
    assert out["qqq"]["concentration_status"] in {"actionable", "half_size"}
    assert out["xlk"]["concentration_status"] == "shadow_proxy_duplicate"
    assert out["xlk"]["concentration_effective_weight"] == 0.0


def test_2_spy_dia_iwm_collapse_keeps_best():
    out = _by_sym(apply_stock_concentration_caps([
        sig("SPY", score=75, sid="spy"), sig("DIA", score=82, sid="dia"),
        sig("IWM", score=60, sid="iwm"),
    ]))
    assert out["dia"]["concentration_status"] != "shadow_proxy_duplicate"  # best kept
    assert out["spy"]["concentration_status"] == "shadow_proxy_duplicate"
    assert out["iwm"]["concentration_status"] == "shadow_proxy_duplicate"


# ---- Rule B: sector exposure cap -----------------------------------------

def test_3_4_5_first_second_third_sector_exposure():
    # 3 distinct semis names, same day/direction → 1.0 / 0.5 / 0.0
    out = _by_sym(apply_stock_concentration_caps([
        sig("AMD", score=90, sid="amd"), sig("NVDA", score=80, sid="nvda"),
        sig("SMCI", score=70, sid="smci"),
    ]))
    assert out["amd"]["concentration_effective_weight"] == 1.0
    assert out["amd"]["concentration_status"] == "actionable"
    assert out["nvda"]["concentration_effective_weight"] == 0.5
    assert out["nvda"]["concentration_status"] == "half_size"
    assert out["smci"]["concentration_effective_weight"] == 0.0
    assert out["smci"]["concentration_status"] == "shadow_sector_cap"


def test_6_existing_active_position_counts():
    existing = [{"symbol": "SMH", "asset_class": "stocks", "mode": "intraday",
                 "tier": "B", "direction": "long", "status": "triggered"}]
    out = _by_sym(apply_stock_concentration_caps([sig("AMD", sid="amd")], existing))
    # 1 existing semis long → new AMD long is 2nd → half
    assert out["amd"]["concentration_rank"] == 2
    assert out["amd"]["concentration_effective_weight"] == 0.5


def test_7_opposite_direction_not_capped():
    existing = [{"symbol": "SMH", "asset_class": "stocks", "mode": "intraday",
                 "tier": "B", "direction": "long", "status": "triggered"}]
    out = _by_sym(apply_stock_concentration_caps([sig("AMD", direction="short", sid="amd")], existing))
    assert out["amd"]["concentration_rank"] == 1
    assert out["amd"]["concentration_effective_weight"] == 1.0


def test_8_different_bucket_not_capped():
    out = _by_sym(apply_stock_concentration_caps([
        sig("AMD", sid="amd"), sig("LLY", sid="lly"),  # semis vs healthcare
    ]))
    assert out["amd"]["concentration_effective_weight"] == 1.0
    assert out["lly"]["concentration_effective_weight"] == 1.0


# ---- guardrails -----------------------------------------------------------

def test_9_ctier_not_promoted():
    out = _by_sym(apply_stock_concentration_caps([sig("AMD", tier="C", sid="amd")]))
    assert out["amd"]["concentration_status"] == "not_applicable"
    assert out["amd"]["concentration_effective_weight"] == out["amd"]["concentration_base_weight"]


def test_10_stocks_swing_invest_remain_zero():
    for mode in ("swing", "invest"):
        out = _by_sym(apply_stock_concentration_caps([sig("AMD", mode=mode, sid="amd")]))
        assert out["amd"]["concentration_status"] == "not_applicable"
        assert out["amd"]["concentration_effective_weight"] == 0.0  # paused playbook weight


def test_11_crypto_unaffected():
    out = _by_sym(apply_stock_concentration_caps([
        sig("ETH/USDT", asset="crypto", mode="intraday", sid="eth"),
    ]))
    assert out["eth"]["concentration_status"] == "not_applicable"
    assert out["eth"]["concentration_effective_weight"] == 1.0  # crypto intraday playbook 1.0


def test_12_crypto_scalp_stays_shadow_zero():
    out = _by_sym(apply_stock_concentration_caps([
        sig("ZEC/USDT", asset="crypto", mode="scalp", sid="zec"),
    ]))
    assert out["zec"]["concentration_effective_weight"] == 0.0  # scalp 0x preserved


def test_13_14_no_score_tpsl_modified_raw_r_preserved():
    s = sig("AMD", sid="amd", score=88.0)
    s["final_r"] = -1.0
    out = apply_stock_concentration_caps([s])[0]
    assert out["score"] == 88.0 and out["tier"] == "B"
    assert out["stop_loss"] == 98.0 and out["tp1"] == 104.0 and out["entry_low"] == 100.0
    assert out["final_r"] == -1.0  # raw R untouched
    assert out["original_raw_r"] == -1.0


def test_15_16_status_labels_for_telegram():
    out = _by_sym(apply_stock_concentration_caps([
        sig("AMD", score=90, sid="amd"), sig("NVDA", score=80, sid="nvda"),
        sig("SMCI", score=70, sid="smci"),
    ]))
    assert "0.5x" in out["nvda"]["concentration_reason"]            # half-size warning text
    assert "shadow" in out["smci"]["concentration_reason"]          # sector cap shadow text


def test_17b_unknown_symbol_actionable_not_capped():
    out = _by_sym(apply_stock_concentration_caps([
        sig("ZZZZ", sid="z1"), sig("YYYY", sid="y2"),
    ]))
    assert out["z1"]["concentration_status"] == "unknown_bucket_actionable"
    assert out["z1"]["concentration_effective_weight"] == out["z1"]["concentration_base_weight"]


def test_18_input_not_mutated():
    s = sig("AMD", sid="amd")
    snapshot = dict(s)
    apply_stock_concentration_caps([s])
    assert s == snapshot  # original dict untouched (overlay returns copies)


# ---- live paper-entry integration ----------------------------------------

import json
from unittest.mock import MagicMock


def _store(tmp_path):
    from src.storage.sqlite import SQLiteStore
    st = SQLiteStore(tmp_path / "t.sqlite"); st.init_db(); return st


def _insert_open(st, symbol, direction="long", tier="B"):
    with st.connect() as c:
        c.execute(
            "INSERT INTO proposed_signals(signal_id, created_at, updated_at, symbol, "
            "direction, mode, tier, score, asset_class, status) "
            "VALUES(?,?,?,?,?,?,?,?,?,?)",
            (f"open_{symbol}", "2026-06-16T13:00:00+00:00", "2026-06-16T13:00:00+00:00",
             symbol, direction, "intraday", tier, 75.0, "stocks", "triggered"),
        )
        c.commit()


def _pe_signal(symbol, direction="long", tier="B"):
    return {
        "signal_id": f"pe_{symbol}", "asset_class": "stocks", "symbol": symbol,
        "direction": direction, "mode": tier and "intraday", "tier": tier, "score": 72.0,
        "entry_low": 100.0, "entry_high": 101.0, "entry_trigger": 100.5, "stop_loss": 98.0,
        "tp1": 104.0, "tp2": 106.0, "tp3": 110.0, "news_supported": 0,
        "raw_idea_json": json.dumps({}),
    }


def _send(st, signal):
    from datetime import datetime, timezone, timedelta
    from src.notifiers.paper_entry import send_paper_entry_alert
    fresh = (datetime.now(timezone.utc) - timedelta(seconds=40)).isoformat()  # actionable
    n = MagicMock()
    out = send_paper_entry_alert(
        store=st, notifier=n, signal=signal, prev_status="waiting_for_entry",
        outcome_entry_triggered=True,
        outcome_entry_triggered_at=fresh,
        outcome_entry_price_used=100.5,
    )
    return out, n


def _force_live_queued(monkeypatch):
    monkeypatch.setattr(
        "src.live_execution.service.capture_paper_candidate",
        lambda **_kwargs: {
            "status": "QUEUED",
            "queued": True,
            "decision_id": "live-test-decision",
            "reasons": [],
            "execution_mode": "live",
        },
    )


def test_live_first_exposure_sends(tmp_path, monkeypatch):
    _force_live_queued(monkeypatch)
    out, n = _send(_store(tmp_path), _pe_signal("AMD"))
    assert out["telegram_status"] == "sent"
    n.send.assert_called_once()


def test_live_second_exposure_half_size_warning(tmp_path, monkeypatch):
    _force_live_queued(monkeypatch)
    st = _store(tmp_path); _insert_open(st, "SMH")          # 1 open semis long
    out, n = _send(st, _pe_signal("AMD"))                   # 2nd semis long
    assert out["telegram_status"] == "sent"                 # still pushed
    assert out["payload"]["concentration_status"] == "half_size"
    assert "0.5x" in out["message"]


def test_live_third_exposure_shadow_not_pushed(tmp_path):
    st = _store(tmp_path); _insert_open(st, "SMH"); _insert_open(st, "NVDA")  # 2 open semis
    out, n = _send(st, _pe_signal("AMD"))                   # 3rd → shadow
    assert out["telegram_status"] == "shadow_sector_cap"
    assert out["sent"] is False
    n.send.assert_not_called()
    assert "SECTOR CAP" in out["message"]


def test_live_proxy_duplicate_shadow(tmp_path):
    st = _store(tmp_path); _insert_open(st, "QQQ")          # open Nasdaq proxy
    out, n = _send(st, _pe_signal("XLK"))                   # redundant proxy
    assert out["telegram_status"] == "shadow_sector_cap"    # routed shadow
    assert out["sent"] is False
    assert "SECTOR CAP" in out["message"]


def test_live_crypto_unaffected(tmp_path, monkeypatch):
    from src.execution import crypto_quality_overlay as cqo
    monkeypatch.setattr(
        cqo, "decide_for_signal",
        lambda *args, **kwargs: cqo.OverlayDecision(action="FULL_SIZE", reasons=["test_fixture"]),
    )
    _force_live_queued(monkeypatch)
    st = _store(tmp_path)
    sigc = {"signal_id": "c1", "asset_class": "crypto", "symbol": "ETH/USDT",
            "direction": "long", "mode": "intraday", "tier": "B", "score": 70.0,
            "entry_low": 1.0, "entry_high": 1.1, "entry_trigger": 1.05, "stop_loss": 0.9,
            "tp1": 1.2, "tp2": 1.3, "tp3": 1.4, "news_supported": 1,
            "raw_idea_json": json.dumps({})}
    out, n = _send(st, sigc)
    assert out["telegram_status"] == "sent"
    n.send.assert_called_once()
