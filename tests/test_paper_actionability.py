"""Paper portfolio must reflect the SAME overlay decisions as the paper-entry alert.
Tests: HALF halves risk/PnL; SHADOW excluded; resolver priority; fallback; schema; fail-conservative;
current-snapshot decisions are NOT used as historical sizing evidence. READ-MODEL / paper only.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from src.execution import paper_actionability as pa
from src.execution.paper_portfolio import ensure_tables, load_cfg, simulate_portfolio

NOW = datetime(2026, 7, 8, 15, 0, tzinfo=timezone.utc)


def _trade(size_weight=1.0, **kw):
    d = {"signal_id": "x", "economic_trade_key": "k", "symbol": "DOGE/USDT", "asset_class": "crypto",
         "mode": "intraday", "direction": "long", "entry": 100.0, "stop": 98.0,
         "paper_execution_r": -1.0, "close_reason": "original_stop",
         "entry_at": "2026-07-08T15:00:00+00:00", "size_weight": size_weight}
    d.update(kw)
    return d


# ---- A. HALF_SIZE halves risk / PnL / notional in the ledger ------------------------------------
def test_half_size_halves_risk_and_pnl():
    cfg = load_cfg()
    full = simulate_portfolio([_trade(1.0)], cfg=cfg, fee_profile="bybit_non_vip_usdt_perp")["ledger"][0]
    half = simulate_portfolio([_trade(0.5)], cfg=cfg, fee_profile="bybit_non_vip_usdt_perp")["ledger"][0]
    assert half["risk_usdt"] == pytest.approx(full["risk_usdt"] * 0.5, rel=1e-6)
    assert half["position_notional_usdt"] == pytest.approx(full["position_notional_usdt"] * 0.5, rel=1e-6)
    assert half["net_pnl_usdt"] == pytest.approx(full["net_pnl_usdt"] * 0.5, abs=0.01)  # ledger rounds 4dp
    assert half["size_weight"] == 0.5


def test_crypto_intraday_breakeven_is_fee_aware_in_usd_ledger():
    cfg = load_cfg()
    t = _trade(1.0, paper_execution_r=0.0, close_reason="breakeven_stop",
               asset_class="crypto", mode="intraday")
    row = simulate_portfolio([t], cfg=cfg, fee_profile="bybit_non_vip_usdt_perp")["ledger"][0]
    assert row["paper_execution_r"] == 0.0          # Model-F evidence R is unchanged
    assert row["gross_pnl_usdt"] > 0               # USD execution moves enough to cover costs
    assert abs(row["net_pnl_usdt"]) <= 0.02


def test_fee_aware_breakeven_is_scoped_to_crypto_intraday():
    cfg = load_cfg()
    t = _trade(1.0, paper_execution_r=0.0, close_reason="breakeven_stop",
               asset_class="crypto", mode="swing")
    row = simulate_portfolio([t], cfg=cfg, fee_profile="bybit_non_vip_usdt_perp")["ledger"][0]
    assert row["paper_execution_r"] == 0.0
    assert row["net_pnl_usdt"] < 0


# ---- B. SHADOW_ONLY / BLOCK (size_weight 0) excluded from the ledger -----------------------------
def test_shadow_size_weight_zero_excluded_from_ledger():
    cfg = load_cfg()
    assert simulate_portfolio([_trade(0.0)], cfg=cfg)["ledger"] == []


# ---- resolver test DB ---------------------------------------------------------------------------
def _db(tmp_path):
    p = tmp_path / "pa.sqlite"
    c = sqlite3.connect(p)
    c.execute("CREATE TABLE signal_alerts (signal_id TEXT, alert_type TEXT, telegram_status TEXT, "
              "sent_at TEXT, payload_json TEXT)")
    c.execute("CREATE TABLE crypto_quality_counterfactual (signal_id TEXT, overlay_action TEXT)")
    c.execute("CREATE TABLE crypto_quality_overlay_decisions (signal_id TEXT, quality_action TEXT, "
              "decision_context_type TEXT)")
    c.commit()
    return p, c


def _resolve(c, sid, asset="crypto", mode="intraday", tier="B"):
    return pa.resolve_paper_actionability(c, sid, asset, mode, tier, maps=pa.build_maps(c))


# ---- D. resolver priority: alert payload beats counterfactual beats decisions --------------------
def test_alert_payload_beats_counterfactual(tmp_path):
    p, c = _db(tmp_path)
    c.execute("INSERT INTO signal_alerts VALUES ('s1','paper_entry','sent','2026-07-08T15:00:00+00:00',?)",
              (json.dumps({"cqo_quality_action": "HALF_SIZE", "size_weight": 0.5}),))
    c.execute("INSERT INTO crypto_quality_counterfactual VALUES ('s1','SHADOW_ONLY')")  # should be ignored
    c.commit()
    r = _resolve(c, "s1")
    assert r["source"] == "alert_payload" and r["size_weight"] == 0.5 and r["paper_action"] == "HALF_SIZE"


def test_point_in_time_overlay_floors_full_alert_payload(tmp_path):
    p, c = _db(tmp_path)
    c.execute("INSERT INTO signal_alerts VALUES ('s1','paper_entry','sent','2026-07-08T15:00:00+00:00',?)",
              (json.dumps({"cqo_quality_action": "FULL_SIZE", "size_weight": 1.0}),))
    c.execute("INSERT INTO crypto_quality_overlay_decisions VALUES ('s1','SHADOW_ONLY','point_in_time')")
    c.commit()
    r = _resolve(c, "s1")
    assert r["paper_action"] == "SHADOW_ONLY"
    assert r["size_weight"] == 0.0
    assert r["source"] == "alert_payload+overlay_floor"


def test_shadow_alert_excluded(tmp_path):
    p, c = _db(tmp_path)
    c.execute("INSERT INTO signal_alerts VALUES ('s1','paper_entry','shadow_crypto_quality','t',?)",
              (json.dumps({"cqo_quality_action": "SHADOW_ONLY", "cqo_reasons": ["symbol_cooldown"]}),))
    c.commit()
    r = _resolve(c, "s1")
    assert r["size_weight"] == 0.0 and r["paper_action"] == "SHADOW_ONLY"


@pytest.mark.parametrize("status", ["late_shadow", "shadow_llm_review", "shadow_sector_cap", "shadow_stocks_context",
                                     "shadow_risk_guard", "blocked_crypto_quality", "dry_run"])
def test_non_actionable_alert_status_is_excluded_for_every_asset(tmp_path, status):
    p, c = _db(tmp_path)
    c.execute("INSERT INTO signal_alerts VALUES ('s1','paper_entry',?,'t',?)", (status, json.dumps({})))
    c.commit()
    r = _resolve(c, "s1", asset="stocks", mode="intraday", tier="A")
    assert r["paper_action"] == "SHADOW_ONLY" and r["size_weight"] == 0.0


def test_half_size_payload_can_never_be_counted_as_full(tmp_path):
    p, c = _db(tmp_path)
    c.execute("INSERT INTO signal_alerts VALUES ('s1','paper_entry','sent','t',?)",
              (json.dumps({"cqo_quality_action": "HALF_SIZE", "size_weight": 1.0}),))
    c.commit()
    r = _resolve(c, "s1")
    assert r["paper_action"] == "HALF_SIZE" and r["size_weight"] == 0.5


def test_counterfactual_used_when_no_alert(tmp_path):
    p, c = _db(tmp_path)
    c.execute("INSERT INTO crypto_quality_counterfactual VALUES ('s2','HALF_SIZE')")
    c.commit()
    r = _resolve(c, "s2")
    assert r["source"] == "counterfactual_lookahead_safe" and r["size_weight"] == 0.5


# ---- G. current-snapshot decisions are NOT used as sizing evidence ------------------------------
def test_current_snapshot_decision_not_used_for_sizing(tmp_path):
    p, c = _db(tmp_path)
    # only a CURRENT snapshot exists (no alert, no counterfactual) → must fall through to legacy full-size,
    # never resize a trade off a current snapshot.
    c.execute("INSERT INTO crypto_quality_overlay_decisions VALUES ('s3','SHADOW_ONLY','current_snapshot')")
    c.commit()
    r = _resolve(c, "s3")
    assert r["source"] == "legacy_actionable" and r["size_weight"] == 1.0
    # a POINT-IN-TIME decision, by contrast, IS honoured
    c.execute("INSERT INTO crypto_quality_overlay_decisions VALUES ('s4','HALF_SIZE','point_in_time')")
    c.commit()
    r2 = _resolve(c, "s4")
    assert r2["source"] == "overlay_decision_point_in_time" and r2["size_weight"] == 0.5


# ---- C. fallback + stocks untouched + crypto scalp non-actionable -------------------------------
def test_fallback_legacy_when_no_overlay(tmp_path):
    p, c = _db(tmp_path)
    r = _resolve(c, "none", asset="crypto", mode="intraday", tier="B")
    assert r["source"] == "legacy_actionable" and r["size_weight"] == 1.0


def test_crypto_scalp_not_actionable(tmp_path):
    p, c = _db(tmp_path)
    r = _resolve(c, "sc", asset="crypto", mode="scalp", tier="A")
    assert r["size_weight"] == 0.0 and r["paper_action"] == "NOT_ACTIONABLE"


def test_stocks_use_legacy_only(tmp_path):
    p, c = _db(tmp_path)
    # even with a (spurious) counterfactual row, stocks resolve via legacy, never the crypto overlay.
    c.execute("INSERT INTO crypto_quality_counterfactual VALUES ('st','SHADOW_ONLY')")
    c.commit()
    r = pa.resolve_paper_actionability(c, "st", "stocks", "intraday", "A", maps=pa.build_maps(c))
    assert r["source"] == "legacy_actionable_non_crypto" and r["size_weight"] == 1.0
    r2 = pa.resolve_paper_actionability(c, "st2", "stocks", "swing", "B", maps=pa.build_maps(c))
    assert r2["size_weight"] == 0.0   # stocks swing stays non-actionable (unchanged)


def test_stock_paper_entry_alert_freezes_historical_actionability(tmp_path):
    p, c = _db(tmp_path)
    c.execute("INSERT INTO signal_alerts VALUES ('st','paper_entry','sent','t',?)", (json.dumps({}),))
    c.commit()
    r = pa.resolve_paper_actionability(c, "st", "stocks", "intraday", "C", maps=pa.build_maps(c))
    assert r["paper_action"] == "FULL_SIZE"
    assert r["source"] == "paper_entry_alert_point_in_time"


# ---- E. ledger schema has the additive columns + ensure_tables is idempotent ---------------------
def test_ledger_schema_additive_and_idempotent(tmp_path):
    db = str(tmp_path / "led.sqlite")
    # pre-create an OLD-shape ledger (missing the new columns) with a row to prove no data loss / no drop.
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE paper_portfolio_ledger (id INTEGER PRIMARY KEY AUTOINCREMENT, signal_id TEXT, "
              "economic_trade_key TEXT, timestamp TEXT, event_type TEXT, equity_before REAL, equity_after REAL, "
              "realized_pnl_usdt REAL, unrealized_pnl_usdt REAL, gross_pnl_usdt REAL, fees_usdt REAL, "
              "slippage_usdt REAL, funding_usdt REAL, net_pnl_usdt REAL, risk_usdt REAL, risk_pct REAL, "
              "position_notional_usdt REAL, margin_used_usdt REAL, leverage_used INTEGER, qty REAL, "
              "entry_price REAL, exit_price REAL, stop_initial REAL, stop_current REAL, paper_execution_r REAL, "
              "close_reason TEXT, risk_model TEXT, fee_profile TEXT, expiry_close_price REAL, "
              "expiry_close_price_source TEXT, fee_estimated INTEGER, fee_source TEXT, exit_maker_fraction REAL, "
              "created_at TEXT, UNIQUE(economic_trade_key, event_type, fee_profile))")
    c.execute("INSERT INTO paper_portfolio_ledger (signal_id, fee_profile, event_type) "
              "VALUES ('keep','bybit_structural_maker_first','exit')")
    c.commit()
    ensure_tables(c)      # additive ALTER, must NOT drop
    ensure_tables(c)      # idempotent second call
    cols = {r[1] for r in c.execute("PRAGMA table_info(paper_portfolio_ledger)")}
    for col in ("size_weight", "size_reason", "paper_action", "actionability_source", "overlay_version"):
        assert col in cols
    assert c.execute("SELECT COUNT(*) FROM paper_portfolio_ledger WHERE signal_id='keep'").fetchone()[0] == 1
    c.close()


# ---- F. fail-conservative paper_entry hook (overlay exception → HALF, not silent full-size) -------
def test_paper_entry_overlay_exception_fails_conservative(tmp_path, monkeypatch):
    from src.notifiers import paper_entry as pe

    class _Store:
        db_path = str(tmp_path / "s.sqlite")

        def connect(self):
            c = sqlite3.connect(self.db_path); c.row_factory = sqlite3.Row
            c.execute("CREATE TABLE IF NOT EXISTS signal_alerts (alert_id TEXT PRIMARY KEY, signal_id TEXT, "
                      "asset_class TEXT, mode TEXT, symbol TEXT, tier TEXT, score REAL, direction TEXT, "
                      "sent_at TEXT, alert_type TEXT, telegram_status TEXT, message_hash TEXT, payload_json TEXT)")
            c.commit(); return c

        def last_alert_by_type(self, *a, **k):
            return None

        def record_signal_alert(self, **kw):
            pass

    def _boom(*a, **k):
        raise RuntimeError("overlay down")

    monkeypatch.setattr("src.execution.crypto_quality_overlay.decide_for_signal", _boom)
    sig = {"signal_id": "z", "asset_class": "crypto", "symbol": "DOGE/USDT", "direction": "long",
           "mode": "intraday", "tier": "B", "score": 71, "entry_low": 100.0, "entry_high": 100.5,
           "entry_trigger": 100.5, "suggested_entry": 100.5, "stop_loss": 98.0, "invalidation": 98.0,
           "tp1": 103.0, "tp2": 105.0, "tp3": 108.0, "thesis": "x", "news_supported": 0,
           "setup_type": "breakout", "market_regime": "risk_on", "raw_idea_json": "{}"}
    out = pe.send_paper_entry_alert(
        store=_Store(), notifier=MagicMock(), signal=sig, prev_status="waiting_for_entry",
        outcome_entry_triggered=True, outcome_entry_triggered_at=datetime.now(timezone.utc).isoformat(),
        outcome_entry_price_used=100.5)
    payload = out["payload"] or {}
    assert payload.get("cqo_error") == "RuntimeError"
    assert payload.get("cqo_quality_action") == "HALF_SIZE"      # config default_unknown_data_action
    assert float(payload.get("size_weight", 1.0)) <= 0.5          # halved, not silent full-size
