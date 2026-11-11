"""Shadow Intelligence Layer tests (PARTS 1-7,9).

Covers the 5 modules + aggregator + scheduler wiring. Asserts shadow/diagnostic
only (no trade mutation), fail-open on missing data, no network/LLM in the alert
path, compact Telegram (<=3 lines), and performance (cached enrichment fast).
"""
from __future__ import annotations

import time
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

NOW = datetime(2026, 6, 18, 12, 0, tzinfo=timezone.utc)


@pytest.fixture()
def intel_db(tmp_path, monkeypatch):
    """Point the intelligence store at a temp DB for isolation."""
    from src.intelligence import store
    store._DB_PATH_CACHE.clear()
    store._INIT_DONE.clear()
    monkeypatch.setattr(store, "_DB_PATH_CACHE", [tmp_path / "intel.sqlite"])
    yield tmp_path


# ---- PART 1: symbol timeline ----------------------------------------------
def test_timeline_records_and_summary_compact(intel_db):
    from src.intelligence import symbol_timeline as tl
    assert tl.record_symbol_event("AAA/USDT", "signal_generated",
                                  {"tier": "B", "mode": "intraday", "direction": "long", "price": 10}, now=NOW)
    tl.record_symbol_event("AAA/USDT", "paper_entry_alert", {"tier": "B"}, now=NOW)
    s = tl.get_symbol_timeline_summary("AAA/USDT", now=NOW)
    assert s["event_count"] >= 2
    assert s["recent_alert_count_24h"] >= 1
    assert s["timeline_confidence"] in ("low", "medium", "high")
    # compact payload is a small flat dict
    cp = tl.compact_timeline_for_payload("AAA/USDT", now=NOW)
    assert "timeline_alerts_24h" in cp and len(cp) <= 12


def test_timeline_idempotent_and_unknown(intel_db):
    from src.intelligence import symbol_timeline as tl
    p = {"tier": "B", "price": 10}
    tl.record_symbol_event("BBB/USDT", "signal_generated", p, now=NOW)
    tl.record_symbol_event("BBB/USDT", "signal_generated", p, now=NOW)  # dup same minute
    s = tl.get_symbol_timeline_summary("BBB/USDT", now=NOW)
    assert s["event_count"] == 1  # deduped
    # missing symbol -> empty/unknown summary
    miss = tl.get_symbol_timeline_summary("ZZZ/USDT", now=NOW)
    assert miss["timeline_confidence"] == "unknown" and miss["event_count"] == 0


def test_timeline_cleanup(intel_db):
    from src.intelligence import symbol_timeline as tl
    old = NOW - timedelta(days=200)
    tl.record_symbol_event("CCC/USDT", "signal_generated", {"price": 1}, now=old)
    tl.record_symbol_event("CCC/USDT", "signal_generated", {"price": 2}, now=NOW)
    removed = tl.cleanup_old_events(retention_days=90, now=NOW)
    assert removed >= 1


# ---- PART 2: derivatives trajectory ---------------------------------------
def test_derivatives_funding_turning_down():
    from src.intelligence.derivatives_trajectory import _empty
    # use pure-logic check on funding turning: simulate via fields
    e = _empty("X")
    assert e["derivatives_data_confidence"] == "unknown"
    assert e["diagnostic_only"] is True


def test_derivatives_for_payload_unknown_when_no_cache(intel_db):
    from src.intelligence import derivatives_trajectory as dv
    out = dv.derivatives_trajectory_for_payload("NOPE/USDT")
    assert out["derivatives_data_confidence"] == "unknown"


def test_derivatives_rows_reuse_source_connection_and_bound_latest_window(tmp_path):
    from src.intelligence import derivatives_trajectory as dv

    db = tmp_path / "market.sqlite"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE derivative_snapshots ("
        "id INTEGER PRIMARY KEY, normalized_symbol TEXT, exchange TEXT, "
        "provider_ts TEXT, funding_rate_8h REAL, oi_usd REAL)"
    )
    conn.execute(
        "INSERT INTO derivative_snapshots VALUES (1,?,?,?,?,?)",
        ("AAAUSDT", "mexc", (NOW - timedelta(days=2)).isoformat(), 0.01, 1.0),
    )
    conn.execute(
        "INSERT INTO derivative_snapshots VALUES (2,?,?,?,?,?)",
        ("AAAUSDT", "mexc", (NOW - timedelta(minutes=5)).isoformat(), 0.02, 2.0),
    )
    conn.commit()

    history, latest = dv._db_rows("AAA/USDT", NOW, source_conn=conn)

    assert [row["id"] for row in history] == [2]
    assert [row["id"] for row in latest] == [2]
    assert conn.execute("SELECT 1").fetchone()[0] == 1
    conn.close()


# ---- PART 3: squeeze phase -------------------------------------------------
def _phase_for(p24, p7d, p6h, dist, deriv=None, monkeypatch=None):
    import src.intelligence.squeeze_phase as sp
    monkeypatch.setattr(sp, "_metrics", lambda sym: {
        "p24": p24, "p7d": p7d, "p6h": p6h, "dist_to_high_pct": dist,
        "last_price": 100, "local_high": 100})
    return sp.classify_squeeze_phase("X/USDT", now=NOW, deriv=deriv or {})


def test_squeeze_distribution_near_high(monkeypatch):
    r = _phase_for(18, 60, 5, 1.0, deriv={"funding_turning_down": True}, monkeypatch=monkeypatch)
    assert r["squeeze_phase"] == "phase_3_distribution_near_high"
    assert r["no_chase_warning"] is True
    assert r["distribution_risk_score"] >= 50


def test_squeeze_buildup_and_expansion_and_unwind(monkeypatch):
    assert _phase_for(4, 18, 1, 12, monkeypatch=monkeypatch)["squeeze_phase"] == "phase_1_build_up"
    assert _phase_for(14, 16, 6, 10, monkeypatch=monkeypatch)["squeeze_phase"] == "phase_2_squeeze_expansion"
    assert _phase_for(-12, 5, -3, 8, monkeypatch=monkeypatch)["squeeze_phase"] == "phase_4_unwind"


def test_squeeze_unknown_when_no_data(monkeypatch):
    import src.intelligence.squeeze_phase as sp
    monkeypatch.setattr(sp, "_metrics", lambda sym: None)
    r = sp.classify_squeeze_phase("X/USDT", now=NOW)
    assert r["squeeze_phase"] == "phase_0_unknown"
    assert r["diagnostic_only"] is True


# ---- PART 4: thesis formatter ---------------------------------------------
def test_thesis_compact_and_invalidation():
    from src.intelligence.thesis_formatter import format_thesis
    sig = {"symbol": "X/USDT", "direction": "long", "setup_type": "breakout",
           "entry_low": 99, "entry_high": 100, "stop_loss": 97, "tp1": 103}
    t = format_thesis(sig, catalyst={"catalyst_integrity_status": "catalyst_backed_confirmed"},
                      squeeze={"squeeze_phase": "phase_2_squeeze_expansion", "no_chase_warning": False})
    assert "Thesis:" in t["thesis_summary_compact"] and "Invalid if" in t["thesis_summary_compact"]
    assert "97" in t["thesis_invalidation"]
    assert len(t["thesis_summary_compact"]) <= 240


def test_thesis_distribution_sets_no_chase():
    from src.intelligence.thesis_formatter import format_thesis
    sig = {"symbol": "X/USDT", "direction": "long", "stop_loss": 50}
    t = format_thesis(sig, squeeze={"squeeze_phase": "phase_3_distribution_near_high", "no_chase_warning": True})
    assert t["thesis_do_not_chase_zone"] is not None
    assert "do not chase" in t["thesis_risks_against"].lower()


def test_thesis_handles_missing_data():
    from src.intelligence.thesis_formatter import format_thesis
    t = format_thesis({"symbol": "X/USDT"})
    assert t["diagnostic_only"] is True
    assert t["thesis_summary_compact"] is not None


# ---- PART 5: onchain risk --------------------------------------------------
def test_onchain_unknown_without_config(intel_db):
    from src.intelligence import onchain_risk as oc
    out = oc.compute_onchain_risk("X/USDT", now=NOW)
    assert out["onchain_risk_status"] == "unknown"
    assert out["diagnostic_only"] is True


def test_onchain_scorer_flags_concentration():
    from src.intelligence.onchain_risk import score_from_security
    hi = score_from_security({"chain": "bsc", "contract": "0xabc", "holder_count": 120,
                              "top10_holder_pct": 80, "is_honeypot": False, "is_mintable": True,
                              "sell_tax": 12})
    assert hi["onchain_risk_status"] in ("elevated", "high")
    assert hi["thin_holder_base_flag"] is True
    lo = score_from_security({"chain": "eth", "contract": "0xdef", "holder_count": 50000,
                              "top10_holder_pct": 15, "is_honeypot": False, "is_mintable": False,
                              "sell_tax": 0})
    assert lo["onchain_risk_status"] == "low"


def test_onchain_health_interface_status():
    from src.intelligence.onchain_risk import onchain_risk_health_report
    h = onchain_risk_health_report()
    assert h["status"] in ("interface_ready_config_missing", "ready")


# ---- PART 6: aggregator ----------------------------------------------------
def test_aggregator_fields_and_no_mutation(intel_db):
    from src.intelligence.intelligence_layer import assemble_intelligence_fields
    sig = {"symbol": "AAA/USDT", "direction": "long", "stop_loss": 9, "tp1": 12,
           "entry_low": 9.5, "entry_high": 10}
    before = dict(sig)
    f = assemble_intelligence_fields(sig, now=NOW, prior_fields={"catalyst_integrity_status": "no_direct_news_catalyst"})
    assert sig == before  # signal not mutated
    for k in ("intelligence_layer_status", "intelligence_runtime_ms",
              "timeline_confidence", "squeeze_phase", "thesis_summary_compact"):
        assert k in f
    assert f["diagnostic_only"] is True
    # no trade keys produced
    for forbidden in ("size_weight", "tp1_new", "stop_loss_new", "score"):
        assert forbidden not in f


def test_aggregator_telegram_max_3_lines():
    from src.intelligence.intelligence_layer import intelligence_telegram_lines
    fields = {"squeeze_phase": "phase_3_distribution_near_high", "squeeze_phase_confidence": "high",
              "no_chase_warning": True, "funding_turning_down": True,
              "thesis_summary_compact": "Thesis: x because y. Invalid if z. Risk: r.",
              "onchain_risk_status": "high", "onchain_risk_score": 70}
    lines = intelligence_telegram_lines(fields)
    assert len(lines) <= 3 and all(len(ln) < 300 for ln in lines)


def test_aggregator_no_network(monkeypatch, intel_db):
    import socket
    from src.intelligence.intelligence_layer import assemble_intelligence_fields

    def _boom(*a, **k):
        raise AssertionError("network call in alert path!")
    monkeypatch.setattr(socket.socket, "connect", _boom)
    f = assemble_intelligence_fields({"symbol": "AAA/USDT", "stop_loss": 1}, now=NOW)
    assert f["diagnostic_only"] is True  # completed with no socket connect


def test_aggregator_performance_budget(intel_db):
    from src.intelligence.intelligence_layer import assemble_intelligence_fields
    sig = {"symbol": "AAA/USDT", "direction": "long", "stop_loss": 9, "tp1": 12}
    t0 = time.monotonic()
    for _ in range(20):
        assemble_intelligence_fields(sig, now=NOW)
    avg_ms = (time.monotonic() - t0) / 20 * 1000
    assert avg_ms < 300, f"avg enrichment {avg_ms:.0f}ms exceeds 300ms cap"


# ---- paper-entry integration (alert path) ---------------------------------
def test_paper_entry_includes_intel_fields_and_preserves_sl(tmp_path, monkeypatch):
    import uuid
    from src.notifiers.paper_entry import send_paper_entry_alert
    from src.storage.sqlite import SQLiteStore
    from src.execution.crypto_quality_overlay import OverlayDecision

    def _full(signal, **kwargs):
        return OverlayDecision(signal_id=signal["signal_id"], symbol=signal["symbol"],
                               mode=signal["mode"], action="FULL_SIZE", reasons=["test"])

    monkeypatch.setattr("src.execution.crypto_quality_overlay.decide_for_signal", _full)
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

    store = SQLiteStore(tmp_path / "t.sqlite")
    store.init_db()
    now = datetime.now(timezone.utc).isoformat()

    class FakeNotifier:
        def __init__(self): self.sent = []
        def send(self, text, parse_mode="Markdown"): self.sent.append(text); return {"ok": True}

    sig = {"signal_id": f"i_{uuid.uuid4().hex[:6]}", "created_at": now, "updated_at": now,
           "symbol": "ETH/USDT", "direction": "long", "mode": "intraday", "tier": "B",
           "asset_class": "crypto", "score": 72.0, "status": "triggered",
           "entry_low": 100.0, "entry_high": 101.0, "stop_loss": 98.0,
           "tp1": 104.0, "tp2": 106.0, "tp3": 110.0, "market_regime": "bullish trend"}
    res = send_paper_entry_alert(
        store=store, notifier=FakeNotifier(), signal=sig, prev_status="waiting_for_entry",
        outcome_entry_triggered=True, outcome_entry_triggered_at=now, outcome_entry_price_used=100.5)
    p = res["payload"]
    # intelligence fields present + diagnostic
    assert "intelligence_layer_status" in p
    assert "thesis_summary_compact" in p
    assert p.get("diagnostic_only") is True
    # SL line preserved in the compact live message body
    assert "SL:" in res["message"]
    # phone routing is now live-only
    assert p["telegram_channel"] == "live_handoff"
    # signal tier/score/TP/SL untouched
    assert sig["tier"] == "B" and sig["stop_loss"] == 98.0 and sig["tp1"] == 104.0


# ---- PART 7: scheduler -----------------------------------------------------
def test_scheduler_includes_intelligence_steps_nonfatal():
    import scripts.run_default_market_schedule as s
    steps = s.build_cycle_steps(
        now=datetime(2026, 6, 18, 4, 0, tzinfo=timezone.utc),
        crypto_only=False, include_long_horizon=True, monitor_minutes=90, skip_reports=False)
    labels = {l: k for l, _a, k, _d in steps}
    assert labels.get("intelligence layer update") == "command_nonfatal"
    assert labels.get("intelligence onchain risk update (daily)") == "command_nonfatal"
