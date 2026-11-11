"""Contracts for the strictly read-only Telegram Paper/Shadow dashboard."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from src.notifiers.telegram_dashboard.config import DashboardConfig
from src.notifiers.telegram_dashboard.data import DashboardData
from src.notifiers.telegram_dashboard.service import TelegramDashboardAPI, TelegramDashboardService
from src.notifiers.telegram_dashboard.views import shadow_overview


class FakeAPI:
    def __init__(self):
        self.calls: list[tuple[str, dict]] = []

    def call(self, method: str, payload: dict | None = None) -> dict:
        payload = payload or {}
        self.calls.append((method, payload))
        if method == "sendMessage":
            return {"message_id": 77}
        return {}


def test_api_surfaces_telegram_error_description(monkeypatch):
    class Response:
        ok = False
        status_code = 400

        @staticmethod
        def json():
            return {"ok": False, "description": "Bad Request: chat not found"}

    monkeypatch.setattr(
        "src.notifiers.telegram_dashboard.service.requests.post",
        lambda *args, **kwargs: Response(),
    )
    with pytest.raises(RuntimeError, match="chat not found"):
        TelegramDashboardAPI("test-token").call("sendMessage", {"chat_id": "42"})


def _seed(root: Path) -> Path:
    db_dir = root / "db"
    db_dir.mkdir(parents=True)
    db = db_dir / "crypto_ai_desk.sqlite"
    conn = sqlite3.connect(db)
    conn.executescript(
        """
        CREATE TABLE proposed_signals (
          signal_id TEXT PRIMARY KEY, symbol TEXT, direction TEXT, mode TEXT,
          asset_class TEXT, tier TEXT, created_at TEXT
        );
        CREATE TABLE paper_portfolio_ledger (
          signal_id TEXT, event_type TEXT, equity_before REAL, equity_after REAL,
          net_pnl_usdt REAL, fees_usdt REAL, slippage_usdt REAL, funding_usdt REAL,
          entry_at TEXT, exit_at TEXT, timestamp TEXT, close_reason TEXT
        );
        CREATE TABLE paper_execution_outcomes (
          signal_id TEXT PRIMARY KEY, entry_at TEXT, entry_price_used REAL,
          stop_initial REAL, lifecycle_state TEXT, paper_execution_outcome TEXT,
          computed_at TEXT
        );
        CREATE TABLE paper_shadow_execution_outcomes (
          signal_id TEXT, shadow_lane TEXT, asset_class TEXT, playbook TEXT,
          mode_source TEXT, outcome_status TEXT, is_clean_for_edge INTEGER,
          net_pnl_usdt REAL, fees_usdt REAL, slippage_usdt REAL,
          created_at TEXT, updated_at TEXT, symbol TEXT, side TEXT,
          entry_fill_time TEXT, entry_fill_status TEXT, skipped_shadow_reason TEXT,
          close_reason TEXT, entry_mode TEXT
        );
        """
    )
    now = "2099-01-01T12:00:00+00:00"
    conn.execute(
        "INSERT INTO proposed_signals VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("paper-1", "BTC/USDT", "long", "swing", "crypto", "B", now),
    )
    conn.execute(
        "INSERT INTO paper_portfolio_ledger VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("paper-1", "exit", 1000.0, 1025.0, 25.0, 2.0, 1.0, 0.5,
         now, now, now, "tp3_runner"),
    )
    conn.execute(
        "INSERT INTO paper_execution_outcomes VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("paper-1", now, 100.0, 95.0, "OPEN", "open", now),
    )
    conn.execute(
        "INSERT INTO paper_shadow_execution_outcomes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("shadow-1", "shadow_test", "crypto", "PULLBACK_LIMIT", "B", "closed", 1,
         12.5, 0.5, 0.2, now, now, "ETH/USDT", "long", now, "filled", None,
         "tp1", "PULLBACK_LIMIT"),
    )
    conn.commit()
    conn.close()
    (root / "config").mkdir(exist_ok=True)
    (root / "config" / "notifications.yaml").write_text(
        "telegram:\n  enabled: true\n  bot_token: test-token\n  chat_id: '42'\n",
        encoding="utf-8",
    )
    return db


def _service(root: Path, db: Path, api: FakeAPI) -> TelegramDashboardService:
    cfg = DashboardConfig(
        enabled=True, bot_token="dashboard-token", chat_id="42",
        state_path=root / "data" / "telegram" / "state.json",
        poll_timeout_seconds=1, refresh_seconds=300, page_size=10, pin_message=True,
    )
    return TelegramDashboardService(root, config=cfg, api=api, data=DashboardData(db))


def test_dashboard_reads_authoritative_exit_pnl_and_never_writes_trade_db(tmp_path):
    db = _seed(tmp_path)
    before = db.read_bytes()
    snapshot = DashboardData(db).snapshot()
    assert snapshot["paper"]["week_closed"] == 1
    assert snapshot["paper"]["week_pnl"] == 25.0
    assert snapshot["paper"]["costs"] == {"fees": 2.0, "slippage": 1.0, "funding": 0.5}
    assert snapshot["shadow"]["lanes"][0]["clean_closed"] == 1
    assert db.read_bytes() == before


def test_dashboard_uses_only_the_active_fee_scenario(tmp_path):
    db = _seed(tmp_path)
    conn = sqlite3.connect(db)
    conn.execute("ALTER TABLE paper_portfolio_ledger ADD COLUMN fee_profile TEXT")
    conn.execute(
        "UPDATE paper_portfolio_ledger SET fee_profile='bybit_non_vip_usdt_perp'"
    )
    conn.execute(
        "INSERT INTO paper_portfolio_ledger("
        "signal_id,event_type,equity_before,equity_after,net_pnl_usdt,fees_usdt,"
        "slippage_usdt,funding_usdt,entry_at,exit_at,timestamp,close_reason,fee_profile"
        ") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
        ("paper-1", "exit", 1000.0, 9999.0, 999.0, 0.0, 0.0, 0.0,
         "2099-01-01T12:00:00+00:00", "2099-01-01T12:00:00+00:00",
         "2099-01-01T12:00:00+00:00", "scenario_only", "zero"),
    )
    conn.commit()
    conn.close()

    snapshot = DashboardData(db).snapshot()["paper"]
    assert snapshot["week_closed"] == 1
    assert snapshot["week_pnl"] == 25.0
    assert snapshot["balance"] == 1025.0


def test_health_exposes_mexc_queue_only_when_live_tables_exist(tmp_path):
    db = _seed(tmp_path)
    assert DashboardData(db).health_summary()["mexc_live"] is None
    conn = sqlite3.connect(db)
    conn.executescript(
        """
        CREATE TABLE mexc_canary_decisions (state TEXT);
        CREATE TABLE mexc_canary_outbox (status TEXT);
        CREATE TABLE mexc_canary_control (control_key TEXT, control_value TEXT, updated_at TEXT);
        INSERT INTO mexc_canary_decisions VALUES ('SUBMITTED');
        INSERT INTO mexc_canary_decisions VALUES ('REJECTED_PREFLIGHT');
        INSERT INTO mexc_canary_outbox VALUES ('QUEUED');
        INSERT INTO mexc_canary_control VALUES ('monitor_heartbeat', '{"status":"OK"}', '2099-01-01T12:00:00+00:00');
        """
    )
    conn.commit()
    conn.close()
    live = DashboardData(db).health_summary()["mexc_live"]
    assert live["pending"] == 1
    assert live["submitted"] == 1
    assert live["rejected_preflight"] == 1
    assert live["heartbeat"]["status"] == "OK"


def test_latest_trade_list_is_not_limited_to_the_seven_day_summary_window(tmp_path):
    db = _seed(tmp_path)
    conn = sqlite3.connect(db)
    conn.execute(
        "UPDATE paper_portfolio_ledger SET exit_at = '2020-01-01T00:00:00+00:00', timestamp = '2020-01-01T00:00:00+00:00'"
    )
    conn.commit()
    conn.close()
    assert DashboardData(db).paper_trades(limit=10)["total"] == 1
    assert DashboardData(db).paper_trades(days=7, limit=10)["total"] == 0


def test_shadow_keeps_raw_pnl_visible_when_coverage_is_not_applicable(tmp_path):
    db = _seed(tmp_path)
    conn = sqlite3.connect(db)
    conn.execute("UPDATE paper_shadow_execution_outcomes SET is_clean_for_edge = NULL")
    conn.commit()
    conn.close()
    lane = DashboardData(db).shadow_summary()["lanes"][0]
    assert lane["raw_closed"] == 1
    assert lane["raw_pnl"] == 12.5
    assert lane["clean_closed"] == 0
    assert lane["unclassified_closed"] == 1


def test_same_lane_across_assets_gets_distinct_shadow_callbacks():
    _text, keyboard = shadow_overview({"lanes": [
        {"key": "crypto:ab_main", "lane": "ab_main", "asset_class": "crypto", "label": "Crypto - ab_main",
         "raw_closed": 1, "raw_pnl": 1.0, "clean_closed": 0, "pnl": 0.0, "dirty_closed": 0,
         "dirty_pnl": 0.0, "unclassified_closed": 1, "unclassified_pnl": 1.0,
         "profit_factor": None, "verdict": "MEASUREMENT_ONLY"},
        {"key": "stocks:ab_main", "lane": "ab_main", "asset_class": "stocks", "label": "Stocks - ab_main",
         "raw_closed": 1, "raw_pnl": 2.0, "clean_closed": 1, "pnl": 2.0, "dirty_closed": 0,
         "dirty_pnl": 0.0, "unclassified_closed": 0, "unclassified_pnl": 0.0,
         "profit_factor": None, "verdict": "MEASUREMENT_ONLY"},
    ]})
    assert keyboard[0][0]["callback_data"] != keyboard[1][0]["callback_data"]


def test_show_creates_and_pins_one_message_with_external_state(tmp_path):
    db = _seed(tmp_path)
    api = FakeAPI()
    service = _service(tmp_path, db, api)
    result = service.show("home")
    assert result["message_id"] == 77
    assert [method for method, _ in api.calls] == ["sendMessage", "pinChatMessage"]
    state = json.loads((tmp_path / "data" / "telegram" / "state.json").read_text(encoding="utf-8"))
    assert state["message_id"] == 77
    assert state["page"] == "home"


def test_persistent_bottom_keyboard_is_installed_separately_from_pinned_panel(tmp_path):
    db = _seed(tmp_path)
    api = FakeAPI()
    service = _service(tmp_path, db, api)
    result = service.install_persistent_keyboard()
    assert result["status"] == "installed"
    method, payload = api.calls[-1]
    assert method == "sendMessage"
    assert payload["reply_markup"]["is_persistent"] is True
    assert payload["reply_markup"]["keyboard"][0][0]["text"] == "📘 Paper"


def test_unchanged_evidence_does_not_edit_pinned_message(tmp_path):
    db = _seed(tmp_path)
    api = FakeAPI()
    service = _service(tmp_path, db, api)
    service.show("home")
    api.calls.clear()
    result = service.refresh_existing()
    assert result["status"] == "unchanged"
    assert api.calls == []


def test_scheduler_refresh_is_noop_until_operator_created_dashboard(tmp_path):
    db = _seed(tmp_path)
    api = FakeAPI()
    result = _service(tmp_path, db, api).refresh_existing()
    assert result == {"status": "not_created"}
    assert api.calls == []


def test_poller_lock_reclaims_stale_process_but_rejects_an_active_one(tmp_path):
    db = _seed(tmp_path)
    service = _service(tmp_path, db, FakeAPI())
    fd = service.state.acquire_poll_lock()
    try:
        try:
            service.state.acquire_poll_lock()
            assert False, "second live dashboard poller must be rejected"
        except RuntimeError as exc:
            assert "already running" in str(exc)
    finally:
        service.state.release_poll_lock(fd)
    stale = service.state.path.with_suffix(service.state.path.suffix + ".poll.lock")
    stale.write_text("999999", encoding="ascii")
    fd = service.state.acquire_poll_lock()
    service.state.release_poll_lock(fd)


def test_poller_lock_reclaims_a_reused_non_dashboard_pid(tmp_path, monkeypatch):
    """A live but unrelated Windows PID cannot block callback polling."""
    import os
    import src.notifiers.telegram_dashboard.state as dashboard_state

    db = _seed(tmp_path)
    service = _service(tmp_path, db, FakeAPI())
    stale = service.state.path.with_suffix(service.state.path.suffix + ".poll.lock")
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text(str(os.getpid()), encoding="ascii")
    monkeypatch.setattr(
        dashboard_state, "_pid_is_dashboard_poller", lambda _pid: False
    )
    fd = service.state.acquire_poll_lock()
    service.state.release_poll_lock(fd)


def test_allowlisted_callback_sends_a_fresh_report_and_rejects_other_chat(tmp_path):
    db = _seed(tmp_path)
    api = FakeAPI()
    service = _service(tmp_path, db, api)
    service.show("home")
    api.calls.clear()

    accepted = service.handle_update({
        "update_id": 1,
        "callback_query": {
            "id": "ok", "data": "td:paper",
            "message": {"chat": {"id": 42}},
        },
    })
    assert accepted is True
    assert [method for method, _ in api.calls] == ["answerCallbackQuery", "sendMessage"]
    assert "📘 PAPER · 7D" in api.calls[1][1]["text"]

    api.calls.clear()
    rejected = service.handle_update({
        "update_id": 2,
        "callback_query": {
            "id": "bad", "data": "td:paper",
            "message": {"chat": {"id": 999}},
        },
    })
    assert rejected is False
    assert [method for method, _ in api.calls] == ["answerCallbackQuery"]
    assert api.calls[0][1]["text"] == "Not authorized"


def test_malformed_callback_is_safe_and_renders_home(tmp_path):
    db = _seed(tmp_path)
    api = FakeAPI()
    service = _service(tmp_path, db, api)
    service.show("home")
    api.calls.clear()
    assert service.handle_update({
        "update_id": 3,
        "callback_query": {
            "id": "malformed", "data": "td:pt:not-a-page",
            "message": {"chat": {"id": 42}},
        },
    }) is True
    assert "🧭 AI DESK" in api.calls[1][1]["text"]


def test_expired_callback_ack_does_not_block_the_fresh_report(tmp_path):
    class ExpiredAckAPI(FakeAPI):
        def call(self, method: str, payload: dict | None = None) -> dict:
            payload = payload or {}
            self.calls.append((method, payload))
            if method == "answerCallbackQuery":
                raise RuntimeError("query is too old")
            if method == "sendMessage":
                return {"message_id": 77}
            return {}

    db = _seed(tmp_path)
    api = ExpiredAckAPI()
    service = _service(tmp_path, db, api)
    assert service.handle_update({
        "update_id": 44,
        "callback_query": {"id": "old", "data": "td:paper", "message": {"chat": {"id": 42}}},
    }) is True
    assert [method for method, _ in api.calls] == ["answerCallbackQuery", "sendMessage"]


def test_run_advances_offset_when_a_single_update_handler_fails(tmp_path):
    class OneUpdateAPI(FakeAPI):
        def __init__(self):
            super().__init__()
            self.sent = False

        def call(self, method: str, payload: dict | None = None) -> dict:
            payload = payload or {}
            self.calls.append((method, payload))
            if method == "getUpdates" and not self.sent:
                self.sent = True
                return [{"update_id": 91, "message": {"chat": {"id": 42}, "text": "Paper"}}]
            return []

    db = _seed(tmp_path)
    api = OneUpdateAPI()
    service = _service(tmp_path, db, api)
    service.handle_update = lambda _update: (_ for _ in ()).throw(RuntimeError("simulated send failure"))
    service.run(duration_seconds=0.01)
    state = json.loads((tmp_path / "data" / "telegram" / "state.json").read_text(encoding="utf-8"))
    assert state["update_offset"] == 92


def test_textless_service_message_does_not_crash_poller_handler(tmp_path):
    db = _seed(tmp_path)
    service = _service(tmp_path, db, FakeAPI())
    assert service.handle_update({
        "update_id": 4,
        "message": {"chat": {"id": 42}, "new_chat_members": []},
    }) is False


def test_bottom_keyboard_text_sends_report_without_replacing_pinned_dashboard(tmp_path):
    db = _seed(tmp_path)
    api = FakeAPI()
    service = _service(tmp_path, db, api)
    service.show("home")
    api.calls.clear()
    assert service.handle_update({
        "update_id": 5,
        "message": {"chat": {"id": 42}, "text": "Paper"},
    }) is True
    assert api.calls[0][0] == "sendMessage"
    assert "📘 PAPER · 7D" in api.calls[0][1]["text"]
    state = json.loads((tmp_path / "data" / "telegram" / "state.json").read_text(encoding="utf-8"))
    assert state["page"] == "home"


def test_latest_paper_report_uses_configured_ten_trade_page(tmp_path):
    db = _seed(tmp_path)
    api = FakeAPI()
    service = _service(tmp_path, db, api)
    service.handle_update({
        "update_id": 6,
        "message": {"message_id": 66, "chat": {"id": 42}, "text": "📘 Paper"},
    })
    service.handle_update({
        "update_id": 7,
        "callback_query": {"id": "latest", "data": "td:pt:0", "message": {"chat": {"id": 42}}},
    })
    latest_message = next(payload for method, payload in reversed(api.calls)
                          if method == "sendMessage")
    assert "📜 PAPER · LAST 10 CLOSED" in latest_message["text"]
