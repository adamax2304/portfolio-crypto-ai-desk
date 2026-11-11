from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

import pytest

from src.execution import paper_actionability as pa
from src.execution.crypto_quality_overlay import OverlayDecision
from src.execution.crypto_swing_paper_policy import (
    apply_breakout_paper_experiment,
    apply_main_paper_floor,
    apply_target_profile_to_setup,
    latency_gate,
    load_cfg,
    target_profile,
)
from src.models import TradeIdea
from src.signals.config import SignalTrackingConfig
from src.signals.registry import build_signal_from_idea


def _cfg() -> SignalTrackingConfig:
    return SignalTrackingConfig(
        enabled=True,
        track_tiers=("A", "B"),
        track_watchlist_with_trigger=True,
        default_validity_hours={"scalp": 2, "intraday": 24, "swing": 168, "invest": 720},
    )


def _signal(**kw):
    d = {
        "signal_id": "s1",
        "asset_class": "crypto",
        "mode": "swing",
        "tier": "B",
        "direction": "long",
        "tp1": 102.8,
        "tp2": 104.8,
        "tp3": 107.6,
        "raw_idea_json": json.dumps({"raw_setup": {"current_price": 100.0, "atr": 2.0}}),
    }
    d.update(kw)
    return d


def _db() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE proposed_signals (signal_id TEXT PRIMARY KEY, asset_class TEXT, mode TEXT, "
              "tier TEXT, direction TEXT, tp1 REAL, tp2 REAL, tp3 REAL, raw_idea_json TEXT)")
    c.execute("CREATE TABLE entry_latency_audit (signal_id TEXT PRIMARY KEY, cause TEXT, data_gap_min REAL)")
    c.execute("CREATE TABLE signal_alerts (signal_id TEXT, alert_type TEXT, telegram_status TEXT, "
              "sent_at TEXT, payload_json TEXT)")
    c.execute("CREATE TABLE crypto_quality_counterfactual (signal_id TEXT, overlay_action TEXT)")
    c.execute("CREATE TABLE crypto_quality_overlay_decisions (signal_id TEXT, quality_action TEXT, "
              "decision_context_type TEXT)")
    c.execute("CREATE TABLE signal_entry_mode (signal_id TEXT PRIMARY KEY, entry_mode TEXT)")
    return c


def _insert_signal(c: sqlite3.Connection, s: dict):
    c.execute("INSERT INTO proposed_signals VALUES (?,?,?,?,?,?,?,?,?)",
              (s["signal_id"], s["asset_class"], s["mode"], s["tier"], s["direction"],
               s["tp1"], s["tp2"], s["tp3"], s["raw_idea_json"]))


def _strict_cfg() -> dict:
    cfg = load_cfg()
    cfg["main_paper_enforcement_enabled"] = True
    cfg["production_profile"] = {
        "name": "strict_test_t140",
        "version": "strict_test_t140_v1",
        "target_multipliers": [1.40, 2.40, 3.80],
        "require_overlay_action": "FULL_SIZE",
        "require_latency_audit": True,
        "max_data_gap_min": 60,
        "reject_latency_causes": ["DATA_GAP_LATE", "LEGITIMATE_LATE", "NO_DATA", "DETECTION_LATENCY"],
        "reject_reason_substrings": ["symbol_cooldown"],
    }
    return cfg


def test_target_profile_long_and_short():
    prof = target_profile(_signal(direction="long"), profile="target_t140")
    assert prof["available"] is True
    assert (prof["tp1"], prof["tp2"], prof["tp3"]) == (102.8, 104.8, 107.6)
    short = target_profile(_signal(direction="short"), profile="target_t140")
    assert (short["tp1"], short["tp2"], short["tp3"]) == (97.2, 95.2, 92.4)


def test_apply_target_profile_to_setup_for_future_signal_creation():
    setup = {"current_price": 100.0, "atr": 2.0, "tp1": 101.0, "tp2": 102.0, "tp3": 103.0}
    cfg = load_cfg()
    cfg["canonical_target_override_enabled"] = True
    out, prof = apply_target_profile_to_setup(setup, direction="long", cfg=cfg)
    assert prof["available"] is True
    assert out["tp1"] == 102.6 and out["tp2"] == 104.6 and out["tp3"] == 107.2
    assert out["paper_target_profile_version"] == "crypto_swing_paper_t130_v1"


def test_build_signal_from_idea_applies_versioned_t130_paper_targets():
    idea = TradeIdea(
        symbol="BTC/USDT", direction="long", score=72.0, confidence="medium", risk_level="medium",
        timeframe="4h", tier="B", mode="swing", asset_class="crypto", exchange_focus="binance",
        exchanges_confirmed=["binance"], data_confidence="medium", thesis="x", evidence=["x"],
        counterarguments=[], entry_plan="x", invalidation="x", targets=[], what_to_monitor=[],
        avoid_conditions=[], data_sources_used=["binance"],
        raw={"setup": {"current_price": 100.0, "atr": 2.0, "entry_low": 98.7,
                       "entry_high": 99.6, "invalidation": 97.6,
                       "tp1": 102.0, "tp2": 104.0, "tp3": 106.0}},
    )
    sig = build_signal_from_idea(idea, config=_cfg(), report_id="r1", created_at="2026-07-12T00:00:00+00:00")
    assert sig is not None
    assert sig.tp1 == 102.6 and sig.tp2 == 104.6 and sig.tp3 == 107.2
    assert sig.expected_rr_tp1 is not None and sig.expected_rr_tp1 > 1.0
    raw = json.loads(sig.raw_idea_json)
    assert raw["paper_target_profile"]["version"] == "crypto_swing_paper_t130_v1"


def test_main_paper_floor_is_disabled_and_preserves_legacy_production():
    c = _db()
    s = _signal(tp1=101.0, tp2=102.0, tp3=103.0)
    _insert_signal(c, s)
    base = {"paper_action": "FULL_SIZE", "size_weight": 1.0, "source": "counterfactual_lookahead_safe",
            "reason": "ok"}
    out = apply_main_paper_floor(c, signal_id="s1", asset_class="crypto", mode="swing",
                                 tier="B", base=base, signal=s)
    assert out["size_weight"] == 1.0
    assert out["crypto_swing_main_policy_applied"] is False


def test_breakout_experiment_caps_only_clean_point_in_time_breakouts_at_half_size():
    c = _db()
    s = _signal()
    _insert_signal(c, s)
    c.execute("INSERT INTO signal_entry_mode VALUES ('s1','BREAKOUT_CONTINUATION')")
    c.execute("INSERT INTO entry_latency_audit VALUES ('s1','OK',0)")
    cfg = load_cfg()
    cfg["breakout_paper_experiment"]["enabled"] = True
    out = apply_breakout_paper_experiment(
        c, signal_id="s1", asset_class="crypto", mode="swing", signal=s,
        base={"paper_action": "FULL_SIZE", "size_weight": 1.0, "source": "alert_payload", "reason": "ok"},
        cfg=cfg,
    )
    assert out["paper_action"] == "HALF_SIZE"
    assert out["size_weight"] == 0.5
    assert out["crypto_swing_breakout_experiment_applied"] is True
    assert out["crypto_swing_breakout_experiment_id"] == "crypto_swing_breakout_paper_experiment_v1"


def test_breakout_experiment_blocks_data_gap_and_never_rescues_non_actionable_rows():
    c = _db()
    s = _signal()
    _insert_signal(c, s)
    c.execute("INSERT INTO signal_entry_mode VALUES ('s1','BREAKOUT_CONTINUATION')")
    c.execute("INSERT INTO entry_latency_audit VALUES ('s1','DATA_GAP_LATE',5)")
    cfg = load_cfg()
    cfg["breakout_paper_experiment"]["enabled"] = True
    out = apply_breakout_paper_experiment(
        c, signal_id="s1", asset_class="crypto", mode="swing", signal=s,
        base={"paper_action": "FULL_SIZE", "size_weight": 1.0, "source": "alert_payload", "reason": "ok"},
        cfg=cfg,
    )
    assert out["paper_action"] == "SHADOW_ONLY" and out["size_weight"] == 0.0
    untouched = apply_breakout_paper_experiment(
        c, signal_id="s1", asset_class="crypto", mode="swing", signal=s,
        base={"paper_action": "SHADOW_ONLY", "size_weight": 0.0}, cfg=cfg,
    )
    assert untouched["paper_action"] == "SHADOW_ONLY"
    assert untouched["crypto_swing_breakout_experiment_applied"] is False


def test_breakout_experiment_allows_legitimate_swing_wait_when_trigger_is_fresh():
    c = _db()
    s = _signal()
    _insert_signal(c, s)
    c.execute("INSERT INTO signal_entry_mode VALUES ('s1','BREAKOUT_CONTINUATION')")
    c.execute("INSERT INTO entry_latency_audit VALUES ('s1','LEGITIMATE_LATE',36.2)")
    cfg = load_cfg()
    cfg["breakout_paper_experiment"]["enabled"] = True
    out = apply_breakout_paper_experiment(
        c, signal_id="s1", asset_class="crypto", mode="swing", signal=s,
        base={"paper_action": "FULL_SIZE", "size_weight": 1.0, "source": "alert_payload", "reason": "ok"},
        cfg=cfg,
    )
    assert out["paper_action"] == "HALF_SIZE" and out["size_weight"] == 0.5


@pytest.mark.parametrize(
    "base,cause,gap,expected",
    [
        ({"paper_action": "HALF_SIZE", "size_weight": 0.5, "source": "counterfactual_lookahead_safe",
          "reason": "half"}, "FAST", 10.0, "overlay action HALF_SIZE"),
        ({"paper_action": "FULL_SIZE", "size_weight": 1.0, "source": "legacy_actionable",
          "reason": "no overlay decision"}, "FAST", 10.0, "NO_OVERLAY"),
        ({"paper_action": "FULL_SIZE", "size_weight": 1.0, "source": "counterfactual_lookahead_safe",
          "reason": "ok"}, "DATA_GAP_LATE", 90.0, "latency cause rejected"),
        ({"paper_action": "FULL_SIZE", "size_weight": 1.0, "source": "counterfactual_lookahead_safe",
          "reason": "ok"}, "LEGITIMATE_LATE", 5.0, "latency cause rejected"),
    ],
)
def test_main_paper_floor_rejects_non_strict_cases(base, cause, gap, expected):
    c = _db()
    s = _signal()
    _insert_signal(c, s)
    c.execute("INSERT INTO entry_latency_audit VALUES ('s1',?,?)", (cause, gap))
    out = apply_main_paper_floor(c, signal_id="s1", asset_class="crypto", mode="swing",
                                 tier="B", base=base, signal=s, cfg=_strict_cfg())
    assert out["size_weight"] == 0.0
    assert out["paper_action"] == "SHADOW_ONLY"
    assert expected in out["reason"]


def test_main_paper_floor_rejects_legacy_targets_even_if_full_clean():
    c = _db()
    s = _signal(tp1=101.0, tp2=102.0, tp3=103.0)
    _insert_signal(c, s)
    c.execute("INSERT INTO entry_latency_audit VALUES ('s1','FAST',10.0)")
    base = {"paper_action": "FULL_SIZE", "size_weight": 1.0, "source": "counterfactual_lookahead_safe",
            "reason": "ok"}
    out = apply_main_paper_floor(c, signal_id="s1", asset_class="crypto", mode="swing",
                                 tier="B", base=base, signal=s, cfg=_strict_cfg())
    assert out["size_weight"] == 0.0
    assert "targets do not match" in out["reason"]


def test_latency_gate_missing_row_is_not_clean_for_enabled_strict_policy():
    c = _db()
    out = latency_gate(c, "missing", cfg=_strict_cfg())
    assert out["clean"] is False
    assert out["cause"] == "NO_LATENCY_ROW"


def test_resolver_keeps_legacy_paper_half_size_actionability():
    c = _db()
    s = _signal()
    _insert_signal(c, s)
    c.execute("INSERT INTO entry_latency_audit VALUES ('s1','FAST',10.0)")
    c.execute("INSERT INTO crypto_quality_counterfactual VALUES ('s1','HALF_SIZE')")
    c.commit()
    result = pa.resolve_paper_actionability(c, "s1", "crypto", "swing", "B",
                                            maps=pa.build_maps(c), signal=s)
    assert result["size_weight"] == 0.5 and result["paper_action"] == "HALF_SIZE"
    assert result["crypto_swing_main_policy_applied"] is False


def _paper_entry_signal(signal_id="s-alert"):
    return {
        "signal_id": signal_id, "asset_class": "crypto", "symbol": "BTC/USDT",
        "direction": "long", "mode": "swing", "tier": "B", "score": 74.0,
        "entry_low": 98.7, "entry_high": 99.6, "entry_trigger": 99.6,
        "suggested_entry": 99.6, "stop_loss": 97.6, "invalidation": 97.6,
        "tp1": 102.6, "tp2": 104.6, "tp3": 107.2, "thesis": "x",
        "news_supported": 1, "setup_type": "pullback", "market_regime": "risk_on",
        "raw_idea_json": json.dumps({"raw_setup": {"current_price": 100.0, "atr": 2.0}}),
    }


class _AlertStore:
    def __init__(self, path, signal_id="s-alert"):
        self.db_path = str(path)
        c = sqlite3.connect(self.db_path)
        c.execute("CREATE TABLE signal_alerts (alert_id TEXT PRIMARY KEY, signal_id TEXT, "
                  "asset_class TEXT, mode TEXT, symbol TEXT, tier TEXT, score REAL, direction TEXT, "
                  "sent_at TEXT, alert_type TEXT, telegram_status TEXT, message_hash TEXT, payload_json TEXT)")
        c.execute("CREATE TABLE entry_latency_audit (signal_id TEXT PRIMARY KEY, cause TEXT, data_gap_min REAL)")
        c.commit()
        c.close()

    def connect(self):
        c = sqlite3.connect(self.db_path)
        c.row_factory = sqlite3.Row
        return c

    def last_alert_by_type(self, *args, **kwargs):
        return None

    def record_signal_alert(self, **kw):
        with self.connect() as c:
            c.execute(
                "INSERT INTO signal_alerts(alert_id, signal_id, asset_class, mode, symbol, tier, score, "
                "direction, sent_at, alert_type, telegram_status, message_hash, payload_json) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (kw["alert_id"], kw["signal_id"], kw["asset_class"], kw.get("mode"),
                 kw["symbol"], kw["tier"], kw.get("score"), kw.get("direction"),
                 kw["sent_at"], kw["alert_type"], kw.get("telegram_status"),
                 kw.get("message_hash"), json.dumps(kw.get("payload") or {})),
            )


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


def test_paper_entry_labels_the_active_t130_paper_profile(tmp_path, monkeypatch):
    from src.notifiers import paper_entry as pe
    notifier = pytest.importorskip("unittest.mock").MagicMock()

    def _full(signal, **kwargs):
        return OverlayDecision(signal_id=signal["signal_id"], symbol=signal["symbol"],
                               mode=signal["mode"], action="FULL_SIZE", reasons=["ok"])

    monkeypatch.setattr("src.execution.crypto_quality_overlay.decide_for_signal", _full)
    _force_live_queued(monkeypatch)
    out = pe.send_paper_entry_alert(
        store=_AlertStore(tmp_path / "a.sqlite"), notifier=notifier,
        signal=_paper_entry_signal(), prev_status="waiting_for_entry",
        outcome_entry_triggered=True, outcome_entry_triggered_at=datetime.now(timezone.utc).isoformat(),
        outcome_entry_price_used=99.6,
    )
    assert out["sent"] is True
    notifier.send.assert_called_once()
    assert out["payload"].get("crypto_swing_main_policy_applied") is False
    assert out["payload"]["paper_entry_profile"] == "crypto_swing_paper_t130_v1"
    assert out["payload"]["telegram_channel"] == "live_handoff"


def test_paper_entry_keeps_legacy_half_size_at_half_not_quarter(tmp_path, monkeypatch):
    from src.notifiers import paper_entry as pe
    notifier = pytest.importorskip("unittest.mock").MagicMock()

    def _half(signal, **kwargs):
        return OverlayDecision(signal_id=signal["signal_id"], symbol=signal["symbol"],
                               mode=signal["mode"], action="HALF_SIZE", reasons=["weak_session"])

    monkeypatch.setattr("src.execution.crypto_quality_overlay.decide_for_signal", _half)
    _force_live_queued(monkeypatch)
    out = pe.send_paper_entry_alert(
        store=_AlertStore(tmp_path / "b.sqlite"), notifier=notifier,
        signal=_paper_entry_signal(), prev_status="waiting_for_entry",
        outcome_entry_triggered=True, outcome_entry_triggered_at=datetime.now(timezone.utc).isoformat(),
        outcome_entry_price_used=99.6,
    )
    assert out["sent"] is True
    assert out["telegram_status"] == "sent"
    notifier.send.assert_called_once()
    assert out["payload"]["size_weight"] == 0.5
    assert "0.5x" in out["message"]
