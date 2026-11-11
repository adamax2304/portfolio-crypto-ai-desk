"""Risk-guard visibility fields + paper-entry wiring (profitability guardrails PART 2).

Asserts the add-only fields land in the payload, the circuit-breaker warning is
deduped per asset/mode/day/level, the diagnostic NEVER blocks the alert or changes
routing/size, and the assembler fails open.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta

from src.notifiers.paper_entry import send_paper_entry_alert
from src.risk.risk_guards import (
    assemble_risk_guard_fields, paper_risk_floor, profit_protection_hint)
from src.storage.sqlite import SQLiteStore

# Anchor to NOON UTC today: _seed_losing_day back-dates exits by 1-3h, and the circuit-breaker
# counts stops by UTC calendar day. Using the raw current time makes the test flaky in the first
# ~3h of a UTC day (back-dated exits roll into yesterday → breaker doesn't fire). Noon is safe.
NOW = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
TODAY = NOW.strftime("%Y-%m-%d")


def _fresh_ts() -> str:
    """A just-now entry-trigger timestamp. Entry freshness is computed against the REAL wall
    clock inside send_paper_entry_alert (not NOW), so pinning it to NOW=noon made the entry read
    'very late' → late_shadow whenever the suite ran after ~12:15 UTC. Use real now so the entry
    is genuinely fresh; NOW stays noon only for the circuit-breaker UTC-day seeding above."""
    return datetime.now(timezone.utc).isoformat()


class FakeNotifier:
    def __init__(self):
        self.messages = []

    def send(self, text, parse_mode="Markdown"):
        self.messages.append(text)
        return {"ok": True}


def _signal(sid, *, symbol="ETH/USDT", status="triggered"):
    return {
        "signal_id": sid, "created_at": NOW.isoformat(), "updated_at": NOW.isoformat(),
        "symbol": symbol, "direction": "long", "mode": "intraday", "tier": "B",
        "asset_class": "crypto", "score": 72.0, "status": status,
        "market_regime": "bullish trend",
        "entry_low": 100.0, "entry_high": 101.0, "stop_loss": 98.0,
        "tp1": 104.0, "tp2": 106.0, "tp3": 110.0, "news_supported": 0,
    }


def _seed_losing_day(store, n=3, *, accepted_paper=True):
    """Register n crypto-intraday stopped trades that exited today (-1R each)."""
    from src.execution.paper_portfolio import ensure_tables, load_cfg

    profile = str(load_cfg()["fee_profile"])
    for i in range(n):
        sid = f"loser_{i}_{uuid.uuid4().hex[:6]}"
        store.upsert_proposed_signal({
            "signal_id": sid, "created_at": NOW.isoformat(), "updated_at": NOW.isoformat(),
            "symbol": f"ALT{i}/USDT", "direction": "long", "mode": "intraday",
            "tier": "B", "asset_class": "crypto", "status": "stopped",
            "market_regime": "bullish trend",
        })
        exit_at = (NOW - timedelta(hours=i + 1)).isoformat()
        store.add_signal_outcome({
            "signal_id": sid, "checked_at": exit_at, "status": "stopped",
            "entry_triggered": 1, "stop_hit": 1, "stop_hit_at": exit_at,
            "final_r": -1.0, "final_outcome": "loss",
        })
        if accepted_paper:
            with store.connect() as conn:
                ensure_tables(conn)
                conn.execute(
                    """INSERT INTO paper_portfolio_ledger(
                        signal_id,economic_trade_key,timestamp,event_type,net_pnl_usdt,
                        risk_usdt,paper_execution_r,close_reason,fee_profile,
                        paper_action,actionability_source,exit_at
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (sid, f"paper-{sid}", exit_at, "exit", -100.0, 100.0, -1.0,
                     "original_stop", profile, "FULL_SIZE", "alert_payload", exit_at),
                )


def _make_store(tmp_path):
    store = SQLiteStore(tmp_path / "t.sqlite")
    store.init_db()
    return store


def _force_full_overlay(monkeypatch):
    """Risk-guard tests are about diagnostics, not the machine's current market session."""
    from src.execution.crypto_quality_overlay import OverlayDecision

    def _full(signal, **kwargs):
        return OverlayDecision(signal_id=signal["signal_id"], symbol=signal["symbol"],
                               mode=signal["mode"], action="FULL_SIZE", reasons=["test"])

    monkeypatch.setattr("src.execution.crypto_quality_overlay.decide_for_signal", _full)


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


def test_assembler_returns_expected_fields(tmp_path):
    store = _make_store(tmp_path)
    fields = assemble_risk_guard_fields(store, _signal("s1"), now=NOW)
    for key in ("circuit_breaker_state", "day_realized_r", "stops_today",
                "regime_context", "lifecycle_label", "would_bind_sector_cap",
                "profit_protection_hint", "catalyst_integrity_status"):
        assert key in fields
    assert fields["diagnostic_only"] is True


def test_profit_protection_hint_mapping():
    assert profit_protection_hint(0.0)["profit_protection_hint"] == "none"
    assert profit_protection_hint(0.6)["profit_protection_hint"] == "reached_+0.5R"
    assert profit_protection_hint(1.2)["would_move_to_BE"] is True
    assert profit_protection_hint(None)["profit_protection_hint"] == "unknown"


def test_paper_entry_l3_reduces_to_half_size_before_global_pause(tmp_path, monkeypatch):
    _force_full_overlay(monkeypatch)
    _force_live_queued(monkeypatch)
    store = _make_store(tmp_path)
    _seed_losing_day(store, n=3)  # -3R, would_pause L3
    res = send_paper_entry_alert(
        store=store, notifier=FakeNotifier(), signal=_signal("new1"),
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at=_fresh_ts(), outcome_entry_price_used=100.5,
    )
    # An ordinary L3 mode drawdown remains authoritative, but now collects
    # forward evidence at half size rather than pausing the entire crypto book.
    assert res["telegram_status"] == "sent"
    assert res["sent"] is True
    assert res["payload"]["telegram_channel"] == "live_handoff"
    assert res["payload"]["circuit_breaker_state"] == "would_pause"
    assert res["payload"]["would_pause_new_entries"] is True
    assert "LIVE QUEUED" in res["message"]
    assert res["payload"]["paper_risk_floor_action"] == "HALF_SIZE"
    assert res["payload"]["paper_risk_floor_size_weight"] == 0.5
    assert res["payload"]["size_weight"] == 0.5
    assert "PAPER_RISK_GUARD_HALF" in res["payload"]["paper_decision_reason_codes"]


def test_paper_entry_global_crypto_drawdown_still_pauses(tmp_path, monkeypatch):
    _force_full_overlay(monkeypatch)
    store = _make_store(tmp_path)
    _seed_losing_day(store, n=5)  # -5R reaches the configured portfolio-wide floor
    res = send_paper_entry_alert(
        store=store, notifier=FakeNotifier(), signal=_signal("global-pause"),
        prev_status="waiting_for_entry", outcome_entry_triggered=True,
        outcome_entry_triggered_at=_fresh_ts(), outcome_entry_price_used=100.5,
    )
    assert res["telegram_status"] == "shadow_risk_guard"
    assert res["payload"]["paper_risk_floor_action"] == "SHADOW_ONLY"
    assert "PAPER_RISK_GUARD_PAUSE" in res["payload"]["paper_decision_reason_codes"]


def test_paper_risk_floor_ignores_advisory_states():
    signal = _signal("floor-test")
    cfg = {
        "enabled": True, "paper_only": True, "live_enabled": False,
        "crypto_modes": ("intraday", "swing"),
        "circuit_breaker": {
            "enabled": True, "required_state": "would_pause",
            "min_level": 2, "action": "SHADOW_ONLY",
        },
    }
    for fields in (
        {"paper_circuit_breaker_state": "watch", "paper_circuit_breaker_level": 1},
        {"paper_circuit_breaker_state": "would_pause", "paper_circuit_breaker_level": 1},
        {"paper_circuit_breaker_state": "watch", "paper_circuit_breaker_level": 2,
         "btc_intraday_risk_off": True},
    ):
        assert paper_risk_floor(fields, signal, cfg=cfg)["paper_risk_floor_action"] is None


def test_mode_isolated_floor_does_not_spill_intraday_losses_into_swing():
    cfg = {
        "enabled": True, "paper_only": True, "live_enabled": False,
        "crypto_modes": ("intraday", "swing"),
        "circuit_breaker": {
            "enabled": True, "required_state": "would_pause", "min_level": 2,
            "scope": "mode_isolated", "l2_action": "HALF_SIZE", "l3_action": "HALF_SIZE",
            "global_pause_daily_r": -5.0, "global_pause_action": "SHADOW_ONLY",
        },
    }
    # The aggregate crypto book is down from intraday, but swing itself is
    # clean. It must remain actionable until the true portfolio floor fires.
    fields = {
        "paper_circuit_breaker_state": "would_pause", "paper_circuit_breaker_level": 3,
        "paper_day_realized_r_asset": -3.0,
        "paper_mode_circuit_breaker_state": "ok", "paper_mode_circuit_breaker_level": 0,
    }
    swing = {**_signal("swing-clean"), "mode": "swing"}
    assert paper_risk_floor(fields, swing, cfg=cfg)["paper_risk_floor_action"] is None
    fields["paper_day_realized_r_asset"] = -5.0
    assert paper_risk_floor(fields, swing, cfg=cfg)["paper_risk_floor_action"] == "SHADOW_ONLY"


def test_paper_risk_floor_is_crypto_only_and_never_live():
    cfg = {
        "enabled": True, "paper_only": True, "live_enabled": False,
        "crypto_modes": ("intraday", "swing"),
        "circuit_breaker": {
            "enabled": True, "required_state": "would_pause",
            "min_level": 2, "action": "SHADOW_ONLY",
        },
    }
    fields = {"paper_circuit_breaker_state": "would_pause", "paper_circuit_breaker_level": 3}
    assert paper_risk_floor(fields, {**_signal("stock-floor"), "asset_class": "stocks"}, cfg=cfg)[
        "paper_risk_floor_action"] is None
    assert paper_risk_floor(fields, _signal("crypto-floor"), cfg={**cfg, "live_enabled": True})[
        "paper_risk_floor_action"] is None


def test_circuit_breaker_warning_is_deduped_per_day_level(tmp_path, monkeypatch):
    _force_full_overlay(monkeypatch)
    _force_live_queued(monkeypatch)
    store = _make_store(tmp_path)
    _seed_losing_day(store, n=3)
    n = FakeNotifier()
    r1 = send_paper_entry_alert(
        store=store, notifier=n, signal=_signal("a1"), prev_status="waiting_for_entry",
        outcome_entry_triggered=True, outcome_entry_triggered_at=_fresh_ts(),
        outcome_entry_price_used=100.5)
    r2 = send_paper_entry_alert(
        store=store, notifier=n, signal=_signal("a2"), prev_status="waiting_for_entry",
        outcome_entry_triggered=True, outcome_entry_triggered_at=_fresh_ts(),
        outcome_entry_price_used=100.5)
    assert "LIVE QUEUED" in r1["message"]
    assert "Circuit breaker" not in r1["message"]       # compact phone copy
    assert "Circuit breaker" not in r2["message"]
    # the FIELD is still present on both; only phone copy is condensed
    assert r2["payload"]["circuit_breaker_state"] == "would_pause"


def test_shadow_or_legacy_losses_do_not_activate_paper_floor(tmp_path):
    store = _make_store(tmp_path)
    _seed_losing_day(store, n=3, accepted_paper=False)
    fields = assemble_risk_guard_fields(store, _signal("legacy-only"), now=NOW)
    assert fields["circuit_breaker_state"] == "would_pause"  # diagnostic remains visible
    assert fields["paper_circuit_breaker_state"] == "ok"
    assert fields["paper_circuit_breaker_evidence_count"] == 0
    assert paper_risk_floor(fields, _signal("legacy-only"))["paper_risk_floor_action"] is None


def test_assembler_fails_open(tmp_path):
    class BadStore:
        def load_recent_terminal_outcomes(self, since): raise RuntimeError("x")
        def load_recent_paper_terminal_outcomes(self, since, *, fee_profile): raise RuntimeError("x")
        def load_signals_for_period(self, **k): raise RuntimeError("x")
        def connect(self): raise RuntimeError("x")
    fields = assemble_risk_guard_fields(BadStore(), _signal("s9"), now=NOW)
    assert fields["diagnostic_only"] is True
    assert fields.get("circuit_breaker_state") == "ok"
